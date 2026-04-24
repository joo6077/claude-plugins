---
name: infra-test
description: >
  인프라/DevOps 설정 파일을 분석하여 테스트 코드를 자동 생성한다.
  IaC 검증(Terraform validate/test, Pulumi test, CDK synth),
  Dockerfile lint, CI 파이프라인 검증, K8s manifest 검증 등
  프로젝트 인프라 스택에 맞는 테스트를 생성한다.
  "인프라 테스트", "Terraform 테스트", "Dockerfile 테스트", "CI 테스트",
  "infra test", "IaC 검증", "K8s manifest 검증" 같은 요청 시 트리거.
  인프라 원칙 가이드는 infra-guide, 전수 감사는 infra-audit를 사용한다.
argument-hint: "<file-or-directory> [iac|container|cicd|k8s|security]"
user-invocable: true
---

## Gotchas

1. **스택 감지 없이 테스트 생성 금지** — Terraform 프로젝트에 Pulumi 테스트를 생성하면 안 된다. Step 0 감지 필수
2. **`terraform validate`만으로 충족 선언 금지** — validate는 구문 검사일 뿐이다. 실제 인프라 로직 검증은 `terraform test` (HCL 기반) 또는 Terratest (Go 기반)로 해야 한다
3. **프로덕션 인프라에 직접 테스트 실행 금지** — IaC 테스트는 반드시 plan/dry-run 모드 또는 격리된 테스트 환경에서 실행한다. `terraform apply`를 테스트에서 호출하면 안 된다 (Terratest의 auto-destroy 제외)
4. **Dockerfile lint와 빌드 테스트 혼동 금지** — hadolint는 정적 분석, 실제 빌드 테스트는 `docker build --target test` 또는 multi-stage test 스테이지로 분리한다
5. **CI 파이프라인 테스트에서 시크릿 노출 주의** — `act` (GitHub Actions 로컬 실행) 사용 시 `.secrets` 파일을 .gitignore에 포함. CI 테스트 결과에 환경 변수 덤프를 남기지 마라
6. **K8s manifest 검증 도구 혼용 주의** — kubeval은 deprecated. kubeconform 또는 `kubectl --dry-run=server`를 사용하라. Helm 차트는 `helm template | kubeconform` 파이프라인으로
7. **보안 스캔을 테스트로 대체하지 마라** — Trivy/Snyk/Checkov는 보안 스캔 도구이지 테스트가 아니다. 스캔 결과를 CI에 게이트로 넣되, 별도 단계로 분리하라
8. **OpenTofu/Terraform 호환성 주의** — OpenTofu 1.7+는 `tofu test`에서 mocking 지원. Terraform은 1.6+에서 `terraform test` 지원. 프로젝트가 어떤 걸 쓰는지 확인하라
9. **Sibling Consistency (backend-test parity)** — Step 0 스택 감지 독립 단계 + 기존 테스트 패턴 탐색 + 외부 실환경 강제 금지 세 항목은 infra-test / backend-test 공통으로 유지해야 한다. 한쪽만 변경하면 sibling drift 로 평가 불일치 발생 (Phase 7/8 동기화 규칙).
10. **Ephemeral values 기반 테스트 fixture (Phase 8 리서치)** — Terraform 1.10+ `ephemeral` 블록이나 OpenTofu 1.7+ write-only 인수로 시크릿을 다루는 모듈은 `terraform test` fixture 에서 평문 주입 금지. 테스트도 동일하게 `run "xxx" { variables { secret = ... } }` 블록 대신 환경변수/Vault dev 모드를 사용하라. 출처: [Terraform ephemeral](https://developer.hashicorp.com/terraform/language/ephemeral).

## Process

### Step 0: 인프라 스택 감지

프로젝트 루트에서 아래 파일/디렉토리를 탐색한다:

| 감지 대상 | 스택 | 테스트 도구 |
|-----------|------|-----------|
| `*.tf` / `.terraform/` | Terraform | `terraform test`, Terratest |
| `Pulumi.yaml` / `Pulumi.*.yaml` | Pulumi | `pulumi preview --expect-no-changes`, Policy as Code |
| `cdk.json` / `lib/*.ts` (CDK) | AWS CDK | `cdk synth` + snapshot test |
| `Dockerfile` / `docker-compose*.yml` | Container | hadolint, docker build, container-structure-test |
| `.github/workflows/*.yml` | GitHub Actions CI | actionlint, act (로컬 실행) |
| `.gitlab-ci.yml` | GitLab CI | gitlab-ci-lint |
| `k8s/` / `helm/` / `kustomize/` | Kubernetes | kubeconform, `helm template`, kustomize build |
| `ansible/` / `*.yml` (playbook) | Ansible | ansible-lint, molecule |

### Step 1: 대상 분석

`$ARGUMENTS`에서 대상 파일/디렉토리와 테스트 유형을 파싱한다.

**유형 미지정 시 자동 추론:**

| 대상 파일 | 테스트 유형 |
|-----------|-----------|
| `*.tf` 모듈 | iac (terraform test) |
| `Dockerfile` | container (hadolint + build) |
| `docker-compose*.yml` | container (config validate + up --dry-run) |
| `.github/workflows/*.yml` | cicd (actionlint + 구조 검증) |
| `k8s/*.yaml`, `helm/` | k8s (kubeconform + template) |
| `*` (보안 관련 요청) | security (Checkov/tfsec/Trivy config) |

### Step 2: 기존 테스트 탐색

프로젝트에 이미 인프라 테스트가 있는지 확인한다:
- `tests/` 또는 `test/` 내 `*.tftest.hcl`, `*_test.go` (Terratest)
- `Makefile` 또는 `Taskfile.yml`의 test/lint/validate 타겟
- CI 파이프라인 내 lint/validate 단계
- `.hadolint.yaml`, `.trivyignore` 등 설정 파일

기존 패턴이 있으면 그 구조와 네이밍을 따른다.

### Step 3: IaC 테스트 생성

#### Terraform / OpenTofu

```hcl
# tests/{module}.tftest.hcl
run "verify_resource_creation" {
  command = plan

  variables {
    environment = "test"
    instance_type = "t3.micro"
  }

  assert {
    condition     = aws_instance.main.instance_type == "t3.micro"
    error_message = "Instance type mismatch"
  }
}

run "verify_output_format" {
  command = plan

  assert {
    condition     = can(regex("^[a-z]", output.resource_name))
    error_message = "Resource name must start with lowercase"
  }
}
```

**Terratest (Go 기반, 복잡한 검증용):**

```go
// test/{module}_test.go
package test

import (
    "testing"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
)

func TestModule(t *testing.T) {
    opts := &terraform.Options{
        TerraformDir: "../modules/{module}",
        Vars: map[string]interface{}{
            "environment": "test",
        },
    }
    defer terraform.Destroy(t, opts)
    terraform.InitAndPlan(t, opts)
    // Plan만 검증. Apply가 필요하면 격리 환경에서만
}
```

#### Pulumi

```typescript
// __tests__/infra.test.ts
import * as pulumi from "@pulumi/pulumi/runtime";
import { describe, it, expect, beforeAll } from "vitest";

pulumi.setMocks({ /* mock provider */ });

describe("Infrastructure", () => {
  it("should create bucket with versioning", async () => {
    const { bucket } = await import("../index");
    const versioning = await new Promise(resolve =>
      bucket.versioning.apply(v => resolve(v))
    );
    expect(versioning?.enabled).toBe(true);
  });
});
```

### Step 4: Container 테스트 생성

#### Dockerfile lint

```yaml
# .hadolint.yaml (설정 파일 생성)
ignored:
  - DL3008  # Pin versions in apt-get (프로젝트 정책에 따라)
trustedRegistries:
  - docker.io
```

실행: `hadolint Dockerfile`

#### Container Structure Test

```yaml
# container-structure-test.yaml
schemaVersion: "2.0.0"
metadataTest:
  exposedPorts: ["8080"]
  cmd: []
  user: "nonroot"
fileExistenceTests:
  - name: "app binary exists"
    path: "/app/server"
    shouldExist: true
commandTests:
  - name: "healthcheck endpoint"
    command: "curl"
    args: ["-f", "http://localhost:8080/health"]
    exitCode: 0
```

실행: `container-structure-test test --image {image} --config container-structure-test.yaml`

### Step 5: CI 파이프라인 테스트 생성

#### GitHub Actions

```bash
# actionlint 정적 분석
actionlint .github/workflows/*.yml
```

**구조 검증 스크립트:**

```bash
#!/usr/bin/env bash
# tests/ci-validation.sh
set -euo pipefail

echo "=== CI Workflow Validation ==="

# 1. YAML 구문 검사
for f in .github/workflows/*.yml; do
  python3 -c "import yaml; yaml.safe_load(open('$f'))" || {
    echo "FAIL: $f YAML syntax error"; exit 1
  }
done

# 2. 필수 단계 존재 확인
for f in .github/workflows/*.yml; do
  grep -q "actions/checkout" "$f" || echo "WARN: $f missing checkout step"
done

# 3. SHA 고정 확인 (third-party actions)
grep -rn "uses:" .github/workflows/ | grep -v "@[a-f0-9]\{40\}" | grep -v "actions/" && {
  echo "WARN: third-party actions not pinned to SHA"
}

echo "=== Validation Complete ==="
```

### Step 6: K8s Manifest 테스트 생성

```bash
# kubeconform 검증
kubeconform -strict -kubernetes-version 1.30.0 k8s/*.yaml

# Helm chart 검증
helm template my-release helm/chart/ | kubeconform -strict

# kustomize 빌드 검증
kustomize build k8s/overlays/dev | kubeconform -strict
```

**Policy 테스트 (OPA/Rego):**

```rego
# policy/no-latest-tag.rego
package main

deny[msg] {
  input.kind == "Deployment"
  container := input.spec.template.spec.containers[_]
  endswith(container.image, ":latest")
  msg := sprintf("Container '%s' uses :latest tag", [container.name])
}
```

실행: `conftest test k8s/*.yaml --policy policy/`

### Step 7: 실행 검증

감지된 스택에 맞는 테스트를 실행한다:

| 스택 | 실행 명령 |
|------|----------|
| Terraform | `terraform test` 또는 `tofu test` |
| Terratest | `cd test && go test -v -timeout 30m` |
| Pulumi | `pulumi preview --expect-no-changes` |
| Dockerfile | `hadolint Dockerfile` |
| Container Structure | `container-structure-test test --image {img} --config {cfg}` |
| GitHub Actions | `actionlint .github/workflows/*.yml` |
| K8s | `kubeconform -strict k8s/*.yaml` |
| Helm | `helm lint helm/chart/` |
| Ansible | `ansible-lint ansible/` |

도구 미설치 시 설치 안내를 제시한다. CI에 통합할 수 있는 명령 형태로 제공한다.

### Step 8: 결과 보고

생성된 파일 목록, 검증 항목 수, 실행 결과를 사용자에게 제시한다.
CI 파이프라인에 통합하는 방법을 안내한다.

## References

- `../../references/principle-index.md` — 인프라 원칙 인덱스
- `../../references/init-checklist.md` — 인프라 세팅 체크리스트
