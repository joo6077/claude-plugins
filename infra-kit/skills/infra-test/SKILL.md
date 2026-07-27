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

11. **셸 검증 스크립트는 exit code 를 게이트로 전파해야 한다** — 이 스킬이 생성하는 스크립트는 CI 게이트로 쓰인다. 결함을 발견하고도 `echo "WARN: ..."` 만 하고 0 으로 끝나면 파이프라인은 항상 통과하고, 스크립트는 검증하는 척만 한다. 아래 4 가지를 **생성하는 모든 셸 스크립트에 동시에** 적용하라.

    | 항목 | 규칙 | 근거 |
    |------|------|------|
    | 파이프 실패 | `set -euo pipefail` 없이 파이프를 쓰지 마라. 파이프는 **마지막 명령의 exit code 만** 평가한다 | [Docker best practices](https://docs.docker.com/build/building/best-practices/) 가 `RUN` 파이프에 `set -o pipefail &&` 선행을 명시 |
    | GH Actions 기본 셸 | 워크플로 `run` 스텝은 `shell: bash` 를 **명시**하라. 비-Windows 기본 셸은 `bash -e {0}` 로 **pipefail 이 없다**. 명시해야 `bash --noprofile --norc -eo pipefail {0}` 가 된다 | [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) |
    | 실패 누적 후 종료 | 첫 실패에서 죽지 말고 `fail=1` 로 누적하고 마지막에 `exit "$fail"`. 전수 리포트를 잃지 않으면서 게이트는 유지된다 | — |
    | 매칭 없는 glob | `shopt -s nullglob` 또는 배열 길이 검사 없이 `for f in dir/*.yml` 을 쓰지 마라. 매칭이 없으면 **리터럴 패턴 한 번**으로 루프가 돌아 존재하지 않는 파일을 오보한다 | POSIX glob 비확장 동작 |

12. **검사 도구 미설치는 PASS 가 아니라 `[미검증]` 이다 (Completion Evidence Gate · skill-design-guide §3.7)** — `hadolint` · `actionlint` · `kubeconform` · `conftest` · `container-structure-test` 는 미설치가 흔하다. 도구를 못 돌렸으면 "검증 항목 N 건 통과" 에 넣지 마라. 완료 보고에는 **실행한 명령과 그 출력**을 인용하고, 돌리지 못한 항목은 `[미검증] <도구> 미설치 — <설치 명령>` 으로 개별 표기한다. "테스트를 생성했으니 검증됐다" 는 자기보고이지 증거가 아니다. `[미검증]` 2 건 이상이면 완료가 아니라 **부분 완료**로 보고한다 (마커·임계값 SSOT: `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol).

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

**구조 검증 스크립트** (Gotcha 11 의 4 항목을 모두 적용한 형태 — 이 골격을 그대로 따르라):

```bash
#!/usr/bin/env bash
# tests/ci-validation.sh — 발견한 결함을 exit code 로 CI 에 전파한다 (Gotcha 11)
set -euo pipefail
shopt -s nullglob   # 매칭 없는 glob 이 리터럴 패턴으로 남지 않게 한다

workflows=(.github/workflows/*.yml .github/workflows/*.yaml)
if [ ${#workflows[@]} -eq 0 ]; then
  echo "SKIP: .github/workflows 에 워크플로 파일 없음"
  exit 0
fi

fail=0
echo "=== CI Workflow Validation (${#workflows[@]} files) ==="

# 1. YAML 구문 검사 — 파일명은 argv 로 넘긴다 (셸 인용 파손 방지)
for f in "${workflows[@]}"; do
  python3 -c 'import sys,yaml; yaml.safe_load(open(sys.argv[1]))' "$f" \
    || { echo "FAIL: $f YAML syntax error"; fail=1; }
done

# 2. 필수 단계 존재 확인
for f in "${workflows[@]}"; do
  grep -q "actions/checkout" "$f" || { echo "FAIL: $f missing checkout step"; fail=1; }
done

# 3. 서드파티 액션 SHA 핀닝 확인
#    first-party 는 `uses: actions/<repo>@` 와 로컬 `uses: ./` 만 제외한다.
#    `aws-actions/`, `google-github-actions/` 는 서드파티이므로 반드시 검사 대상이다.
unpinned=$(grep -HnE '^[[:space:]]*-?[[:space:]]*uses:' "${workflows[@]}" \
  | grep -vE 'uses:[[:space:]]*actions/' \
  | grep -vE 'uses:[[:space:]]*\./' \
  | grep -vE '@[0-9a-f]{40}' || true)
if [ -n "$unpinned" ]; then
  echo "FAIL: third-party actions not pinned to a 40-char commit SHA"
  printf '%s\n' "$unpinned"
  fail=1
fi

echo "=== Validation Complete (fail=$fail) ==="
exit "$fail"
```

**이 골격에서 빼면 안 되는 것** — 아래 넷은 각각 실제로 관측된 오보/누락을 막는다.

| 요소 | 빼면 생기는 일 |
|------|----------------|
| `shopt -s nullglob` + 배열 길이 검사 | 워크플로가 없는 프로젝트에서 리터럴 `.github/workflows/*.yml` 을 열려다 "YAML syntax error" 를 오보 |
| `grep -vE 'uses:[[:space:]]*actions/'` (접두 앵커) | 앵커 없는 `grep -v "actions/"` 는 `aws-actions/*` · `google-github-actions/*` 같은 **서드파티까지 제외**해 미핀닝을 놓친다 |
| `fail=1` 누적 + `exit "$fail"` | `echo "WARN"` 만 하면 스크립트가 항상 0 으로 끝나 CI 게이트가 무력화된다 |
| `python3 -c '...' "$f"` (argv 전달) | 파일명을 문자열에 보간하면 따옴표·공백 포함 경로에서 파손된다 |

워크플로 자체에서 이 스크립트를 부를 때도 `shell: bash` 를 명시한다 — 기본 셸 `bash -e {0}` 에는 pipefail 이 없다 (Gotcha 11).

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

먼저 `command -v <tool>` 로 각 도구의 존재를 확인하고, **확인된 도구만 실행한다.** 미설치 도구는 설치 안내를 제시하되 해당 항목을 통과로 세지 마라 (Gotcha 12). CI에 통합할 수 있는 명령 형태로 제공한다.

### Step 8: 결과 보고 (증거 블록 필수)

아래 3 블록을 모두 채운다. "검증 완료" 같은 서술만으로 끝내지 마라 — 자기보고는 증거가 아니다 (Gotcha 12).

1. **생성된 파일** — 경로 목록.
2. **실행 증거** — 실행한 명령과 그 출력(또는 exit code)을 인용한다. 실패분은 수정 후 재실행하고, 통과 전에는 완료를 선언하지 않는다.
3. **미검증 항목** — `[미검증] <도구> 미설치 — <설치 명령>` 형태로 개별 나열 + `미검증 N 건` 집계. **2 건 이상이면 완료가 아니라 부분 완료로 보고한다.**

```text
실행 증거:
  $ actionlint .github/workflows/deploy.yml
  (출력 없음 · exit 0)
  $ bash tests/ci-validation.sh
  === Validation Complete (fail=0) === · exit 0
미검증 2 건:
  [미검증] kubeconform 미설치 — brew install kubeconform
  [미검증] container-structure-test 미설치 — gcloud components install container-structure-test
→ 부분 완료 (미검증 2 건)
```

CI 파이프라인에 통합하는 방법을 안내한다.

## References

- `../../references/principle-index.md` — 인프라 원칙 인덱스
- `../../references/init-checklist.md` — 인프라 세팅 체크리스트
