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

11. **셸 검증 스크립트는 결과 상태를 exit code 로 전파해야 한다** — 이 스킬이 생성하는 스크립트는 CI 게이트로 쓰인다. 결함을 발견하고도 `echo "WARN: ..."` 만 하고 0 으로 끝나면 파이프라인은 항상 통과하고, 스크립트는 검증하는 척만 한다. **상태어 5 종(`PASS` · `VIOLATION` · `SKIP_NO_TARGET` · `TOOL_OR_ENV_MISSING` · `EXECUTION_ERROR`)과 exit 매핑, 머리말 4 카운터, 핵심/선택 도구 분리는 `../../references/gate-result-taxonomy.md` 가 SSOT 다 — 여기서 다시 정의하지 마라.** 그 위에 아래 4 가지를 **생성하는 모든 셸 스크립트에 동시에** 적용하라.

    | 항목 | 규칙 | 근거 |
    |------|------|------|
    | 파이프 실패 | `set -euo pipefail` 없이 파이프를 쓰지 마라. 파이프는 **마지막 명령의 exit code 만** 평가한다 | [Docker best practices](https://docs.docker.com/build/building/best-practices/) 가 `RUN` 파이프에 `set -o pipefail &&` 선행을 명시 |
    | GH Actions 기본 셸 | 워크플로 `run` 스텝은 `shell: bash` 를 **명시**하라. 비-Windows 기본 셸은 `bash -e {0}` 로 **pipefail 이 없다**. 명시해야 `bash --noprofile --norc -eo pipefail {0}` 가 된다 | [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) |
    | 실패 누적 후 종료 | 첫 실패에서 죽지 말고 `fail=1` 로 누적하고 마지막에 `exit "$fail"`. 전수 리포트를 잃지 않으면서 게이트는 유지된다 | — |
    | 매칭 없는 glob | `shopt -s nullglob` 또는 배열 길이 검사 없이 `for f in dir/*.yml` 을 쓰지 마라. 매칭이 없으면 **리터럴 패턴 한 번**으로 루프가 돌아 존재하지 않는 파일을 오보한다 | POSIX glob 비확장 동작 |

12. **검사 도구 미설치는 PASS 가 아니라 `[미검증]` 이다 (Completion Evidence Gate · skill-design-guide §3.7)** — `hadolint` · `actionlint` · `kubeconform` · `conftest` · `container-structure-test` 는 미설치가 흔하다. 도구를 못 돌렸으면 "검증 항목 N 건 통과" 에 넣지 마라. 완료 보고에는 **실행한 명령과 그 출력**을 인용하고, 돌리지 못한 항목은 `[미검증] TOOL_OR_ENV_MISSING: <도구> 미설치 — 재검증: <명령>` 으로 개별 표기한다. "테스트를 생성했으니 검증됐다" 는 자기보고이지 증거가 아니다. **분기·상태어는 `../../references/gate-result-taxonomy.md`, 마커 의미·임계값·카운터 분리는 `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol 이 SSOT 다 — 어느 쪽도 이 스킬에서 재정의하지 마라.**

13. **핵심 도구 부재를 rule 위반으로 오보하지 마라 (실측 회귀)** — `grep -q ... "$f"` 는 grep 이 **없을 때도** 비영으로 끝난다. 그래서 `grep` 이 PATH 에 없는 환경에서 스크립트가 "checkout 스텝 없음 VIOLATION" 을 오보하고 exit 1 로 끝났다 (실제 관측). 게이트 자체가 의존하는 **핵심 도구**(`grep` · YAML 파서용 `python3`)는 머리말 출력 직후 · 첫 rule 실행 **전**에 `command -v` 로 검사하고, 없으면 rule 을 하나도 돌리지 말고 `EXECUTION_ERROR` + exit 2 로 끝내라. `hadolint` 같은 **선택 도구**는 그 rule 만 `TOOL_OR_ENV_MISSING` 으로 표기하고 나머지 검사는 계속한다 (층 구분 근거: `../../references/gate-result-taxonomy.md` §핵심 도구 / 선택 도구 분리).

14. **워크플로 액션 핀닝을 grep 으로 검사하지 마라 (실측 오탐)** — 앵커 있는 grep 조차 정책을 코드에 숨긴다. `grep -vE 'uses:[[:space:]]*actions/'` 는 GitHub-owned 액션을 **정책 질문으로 남기지 않고 조용히 면제**하므로, 모든 `uses:` 가 뮤터블 태그인 레포에서도 "미핀닝 0 건" 을 보고한다 (실측: 6 건 전부 미검출). YAML 파서로 **`jobs.<id>.uses`(재사용 워크플로 호출)와 `jobs.<id>.steps[].uses`(스텝 액션)를 둘 다** 열거하고, 로컬 `./`·`../` 만 면제하며, 원격 참조는 **40 자 커밋 SHA** 를, `docker://` 는 `@sha256:` digest 를 기본 요구로 둔다. GitHub-owned `actions/*` 면제는 **명시적 opt-in 플래그**로만 열고 그 상태를 출력에 찍어라 — 정책 선택을 숨기지 않는다. 출처: [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use) (full-length commit SHA 만 immutable release 로 취급하며 태그는 이동·삭제 위험이 있다).

15. **Dependabot 은 실제 manifest/lockfile 이 있는 생태계만 등록하라** — `.github/dependabot.yml` 에 없는 생태계를 넣으면 Dependabot 이 매 실행마다 실패하고, 그 실패가 일상화되면 진짜 알림도 무시된다. `github-actions` 는 워크플로가 있으면 항상 검토 대상이고, 나머지는 **탐지된 파일이 있을 때만** 추가한다 (`package-lock.json`/`yarn.lock` → `npm`, `Dockerfile` → `docker`, `requirements.txt`/`poetry.lock` → `pip`, `Cargo.lock` → `cargo`, `go.sum` → `gomod`). 로컬 액션과 `docker://` 참조는 업데이트 대상에서 제한이 있다. 출처: [Dependabot options reference](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference).

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

**구조 검증 스크립트** — Gotcha 11 의 4 항목 + Gotcha 13(핵심/선택 도구 분리) + Gotcha 14(YAML 파서 핀닝) 을
모두 적용한 골격이다. **이 골격을 그대로 따르라.** 상태어·exit 매핑은 `../../references/gate-result-taxonomy.md` 를
인용한 것이며 스크립트 안에서 재정의하지 않는다.

```bash
#!/usr/bin/env bash
# tests/ci-validation.sh — 검사 결과를 상태 taxonomy 로 분류해 exit code 로 CI 에 전파한다.
# 상태·exit 정의 SSOT: infra-kit/references/gate-result-taxonomy.md — 여기서 재정의하지 않는다.
set -euo pipefail
shopt -s nullglob

WF_DIR="${WF_DIR:-.github/workflows}"
PIN_ALLOW_FIRST_PARTY_TAGS="${PIN_ALLOW_FIRST_PARTY_TAGS:-0}"
CORE_TOOLS="grep"          # 없으면 검사 자체가 불가 → EXECUTION_ERROR
OPTIONAL_TOOLS="python3"   # 없으면 해당 rule 만 [미검증]

have() { command -v "$1" >/dev/null 2>&1; }
# 외부 명령에 의존하지 않고 공백 구분 토큰 수를 센다 — 머리말은 도구가 없는 환경에서도 찍혀야 한다
# shellcheck disable=SC2086  # 의도적 단어 분리
count() { set -- ${1:-}; echo "$#"; }

workflows=("$WF_DIR"/*.yml "$WF_DIR"/*.yaml)

tools_ok=""; tools_missing=""
for t in $CORE_TOOLS $OPTIONAL_TOOLS; do
  if have "$t"; then tools_ok="$tools_ok $t"; else tools_missing="$tools_missing $t"; fi
done

echo "=== CI Workflow Gate ==="
echo "대상 워크플로 수 : ${#workflows[@]}  (${WF_DIR})"
echo "규칙 소스 수     : 2  (checkout-존재 · 원격-action-SHA핀닝)"
echo "사용 가능 도구 수: $(count "$tools_ok") [${tools_ok:- 없음} ]"
echo "미설치 도구 수   : $(count "$tools_missing") [${tools_missing:- 없음} ]"

# 핵심 도구 부재는 "위반 0" 이 아니다 — 검사를 수행하지 못한 것이므로 EXECUTION_ERROR 다.
for t in $CORE_TOOLS; do
  have "$t" || { echo "EXECUTION_ERROR : 핵심 도구 '$t' 미설치 — 검사 미수행"; exit 2; }
done

if [ "${#workflows[@]}" -eq 0 ]; then
  echo "SKIP_NO_TARGET  : ${WF_DIR} 에 워크플로 파일 0 개 — 검사 대상 없음"
  exit 3
fi

violation=0; unverified=0; exec_error=0

# 규칙 1: checkout 스텝 존재
for f in "${workflows[@]}"; do
  if grep -q 'actions/checkout' "$f"; then
    echo "PASS            : $f checkout 존재"
  else
    echo "VIOLATION       : $f checkout 스텝 없음"; violation=$((violation + 1))
  fi
done

# 규칙 2: 원격 action 핀닝 — YAML 파서로 jobs.*.uses 와 jobs.*.steps[].uses 를 **둘 다** 열거한다.
# grep 은 로컬 `./` · `docker://` · 잡 레벨 재사용 워크플로를 구분하지 못해 오탐/누락을 낸다.
if ! have python3; then
  echo "[미검증] TOOL_OR_ENV_MISSING: python3 미설치 — 핀닝 rule 미검사 (재검증: python3 설치 후 bash $0)"
  unverified=$((unverified + 1))
else
  set +e
  pin_out=$(PIN_ALLOW_FIRST_PARTY_TAGS="$PIN_ALLOW_FIRST_PARTY_TAGS" python3 - "${workflows[@]}" <<'PY'
import os, re, sys
try:
    import yaml
except ImportError:
    print("[미검증] TOOL_OR_ENV_MISSING: PyYAML 미설치 (재검증: python3 -m pip install pyyaml)")
    sys.exit(3)

SHA = re.compile(r"@[0-9a-f]{40}$")
allow_first_party = os.environ.get("PIN_ALLOW_FIRST_PARTY_TAGS") == "1"
refs, bad, err = [], [], 0

for path in sys.argv[1:]:
    try:
        with open(path, encoding="utf-8") as fh:
            doc = yaml.safe_load(fh)
    except Exception as exc:
        print(f"EXECUTION_ERROR : {path} — YAML 파싱 실패: {exc}"); err += 1; continue
    if not isinstance(doc, dict):
        print(f"EXECUTION_ERROR : {path} — 최상위가 매핑이 아니다"); err += 1; continue
    jobs = doc.get("jobs")
    if not isinstance(jobs, dict):
        continue
    for jid, job in jobs.items():
        if not isinstance(job, dict):
            continue
        if isinstance(job.get("uses"), str):          # 재사용 워크플로 호출
            refs.append((path, f"jobs.{jid}.uses", job["uses"]))
        steps = job.get("steps")
        if isinstance(steps, list):                    # 스텝 액션
            for i, st in enumerate(steps):
                if isinstance(st, dict) and isinstance(st.get("uses"), str):
                    refs.append((path, f"jobs.{jid}.steps[{i}].uses", st["uses"]))

for path, loc, ref in refs:
    if ref.startswith(("./", "../")):
        continue                                       # 로컬 — 레포 커밋에 종속
    if ref.startswith("docker://"):
        if "@sha256:" not in ref:
            bad.append((path, loc, ref, "docker 참조가 digest 고정 아님"))
        continue
    if SHA.search(ref):
        continue
    if allow_first_party and re.match(r"^(actions|github)/", ref):
        continue                                       # 정책 선택 — 기본값 아님
    bad.append((path, loc, ref, "40 자 커밋 SHA 고정 아님"))

print(f"열거된 uses 참조 수: {len(refs)}  (정책: first-party 태그 허용={allow_first_party})")
for path, loc, ref, why in bad:
    print(f"VIOLATION       : {path} {loc} -> {ref} ({why})")
sys.exit(2 if err else (1 if bad else 0))
PY
  )
  pin_rc=$?
  set -e
  printf '%s\n' "$pin_out"
  case "$pin_rc" in
    0) echo "PASS            : 원격 uses 참조 전부 SHA/digest 고정" ;;
    1) violation=$((violation + 1)) ;;
    3) unverified=$((unverified + 1)) ;;
    *) exec_error=$((exec_error + 1)) ;;
  esac
fi

echo "--- 집계 ---"
echo "VIOLATION=$violation  [미검증]=$unverified  EXECUTION_ERROR=$exec_error"
# 실행 불완전(2)이 정책 위반(1)보다 우선한다 — harness/evals/gate-exit-codes.md §규칙
if [ "$exec_error" -gt 0 ] || [ "$unverified" -gt 0 ]; then exit 2; fi
if [ "$violation" -gt 0 ]; then exit 1; fi
exit 0
```

**이 골격에서 빼면 안 되는 것** — 각 요소는 실제로 관측된 오보/누락을 막는다. 오른쪽 열은 그 요소를
제거하고 fixture 를 돌렸을 때 실제로 나온 결과다 (음성 대조).

| 요소 | 빼면 생기는 일 |
|------|----------------|
| 머리말 4 카운터 | "위반 0" 의 분모를 알 수 없다. 대상 0 건인지, 도구가 없어 못 돈 건지 리포트만 보고 구분 불가 |
| 핵심 도구 사전 검사 (`CORE_TOOLS`) | `grep` 부재 환경에서 `grep -q` 가 비영 종료해 **`checkout 스텝 없음` VIOLATION 을 오보**하고 exit 1 로 끝난다 |
| `${#workflows[@]}` 가드 + `exit 3` | 워크플로 0 개 프로젝트가 **exit 0(PASS)** 이 되어 검사한 적 없는 레포가 green 으로 기록된다 |
| `shopt -s nullglob` | 매칭 없는 glob 이 리터럴 패턴으로 남아 존재하지 않는 파일을 열려다 "YAML syntax error" 를 오보 |
| YAML 파서 (`yaml.safe_load`) | grep 은 `jobs.<id>.uses`(재사용 워크플로)·로컬 `./`·`docker://` 를 구분하지 못한다. 앵커 있는 grep 도 `actions/*` 를 조용히 면제해 **미핀닝 6 건 전부를 0 건으로 보고**했다 (실측) |
| `PIN_ALLOW_FIRST_PARTY_TAGS` 를 **기본 0** 으로 두고 상태를 출력 | 면제 정책이 코드에 숨는다. 기본 면제는 GitHub 공식 지침(full SHA 만 immutable)과 어긋난다 |
| `violation`/`unverified`/`exec_error` **3 카운터 분리** | 도구 부재가 "위반 0" 에 흡수된다. 종료 코드가 하나여도 세 카운트는 모두 출력해야 한다 |
| `python3 - "${workflows[@]}"` (argv 전달) | 파일명을 문자열에 보간하면 따옴표·공백 포함 경로에서 파손된다 |
| `count()` 를 외부 명령 없이 구현 | `wc` 조차 없는 축소 PATH 에서 머리말 자체가 깨져 "무엇이 없어서 못 했는지" 를 볼 수 없다 (실측) |

워크플로 자체에서 이 스크립트를 부를 때도 `shell: bash` 를 명시한다 — 기본 셸 `bash -e {0}` 에는
pipefail 이 없다 (Gotcha 11).

**Dependabot 동반 산출물** (Gotcha 15) — 워크플로가 있으면 `.github/dependabot.yml` 에 최소
`github-actions` `/` 를 넣고, 나머지 생태계는 **실제 manifest/lockfile 이 탐지될 때만** 추가한다.

```yaml
# .github/dependabot.yml — 탐지된 생태계만 등록한다 (없는 생태계는 매 실행 실패)
version: 2
updates:
  - package-ecosystem: "github-actions"   # .github/workflows/* 가 있으면 항상 검토
    directory: "/"
    schedule:
      interval: "weekly"
  # 아래는 예시 — 해당 lockfile/manifest 가 실재할 때만 남긴다
  # package-lock.json / yarn.lock → npm · Dockerfile → docker
  # requirements.txt / poetry.lock → pip · Cargo.lock → cargo · go.sum → gomod
```

출처: [Dependabot options reference](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference) ·
[GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use)

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

실행 전에 `../../references/gate-result-taxonomy.md` §머리말 4 카운터를 그대로 출력해 **검사 범위를 먼저 고정**한다 — 대상 수 · 규칙 소스 수 · 사용 가능 도구 수 · 미설치 도구 수. 그 다음 각 스택의 결과를 상태 5 종 중 하나로 분류한다:

| 관측 | 상태 | exit |
|------|------|------|
| 도구가 돌았고 위반 없음 | `PASS` | 0 |
| 도구가 돌았고 위반 발견 | `VIOLATION` | 1 |
| 그 스택의 대상 파일이 0 개 | `SKIP_NO_TARGET` | 3 |
| 도구 미설치 · 클러스터/레지스트리 접근 불가 | `[미검증] TOOL_OR_ENV_MISSING` (+ 재검증 명령) | 2 |
| 도구는 있는데 실행·파싱·권한 실패 | `EXECUTION_ERROR` | 2 |

한 run 에 `VIOLATION` 과 실행 불완전이 같이 나오면 **2 가 우선**한다. 세 카운트는 모두 출력한다 (SSOT: `../../references/gate-result-taxonomy.md` §우선순위).

### Step 8: 결과 보고 (증거 블록 필수)

아래 4 블록을 모두 채운다. "검증 완료" 같은 서술만으로 끝내지 마라 — 자기보고는 증거가 아니다 (Gotcha 12).

1. **검사 범위 머리말** — 4 카운터 (대상 수 · 규칙 소스 수 · 사용 가능 도구 수 · 미설치 도구 수).
2. **생성된 파일** — 경로 목록.
3. **실행 증거** — 실행한 명령과 그 출력(또는 exit code)을 인용한다. 실패분은 수정 후 재실행하고, 통과 전에는 완료를 선언하지 않는다.
4. **미검증 항목** — `[미검증] TOOL_OR_ENV_MISSING: <도구> 미설치 — 재검증: <명령>` 형태로 개별 나열 + `미검증 N 건` 집계. 재검증 명령이 없으면 그 항목은 `UNVERIFIED_ENV` 로 인정되지 않는다 (`../../references/gate-result-taxonomy.md` §재검증 명령 의무). **2 건 이상이면 완료가 아니라 부분 완료로 보고한다.**

```text
검사 범위:
  대상 워크플로 수  : 3  (.github/workflows)
  규칙 소스 수      : 2  (checkout-존재 · 원격-action-SHA핀닝)
  사용 가능 도구 수 : 2  [grep python3]
  미설치 도구 수    : 2  [kubeconform container-structure-test]
실행 증거:
  $ actionlint .github/workflows/deploy.yml
  (출력 없음 · exit 0)
  $ bash tests/ci-validation.sh
  VIOLATION=0  [미검증]=0  EXECUTION_ERROR=0 · exit 0
미검증 2 건:
  [미검증] TOOL_OR_ENV_MISSING: kubeconform 미설치 — 재검증: brew install kubeconform && kubeconform -strict k8s/
  [미검증] TOOL_OR_ENV_MISSING: container-structure-test 미설치 — 재검증: gcloud components install container-structure-test && container-structure-test test --image app:dev --config container-structure-test.yaml
→ 부분 완료 (미검증 2 건)
```

CI 파이프라인에 통합하는 방법을 안내한다.

## References

- `../../references/gate-result-taxonomy.md` — 게이트 결과 상태 5 종 · exit 매핑 · 머리말 4 카운터 (SSOT)
- `../../references/principle-index.md` — 인프라 원칙 인덱스
- `../../references/init-checklist.md` — 인프라 세팅 체크리스트
- `harness/evals/gate-exit-codes.md` — exit 숫자 정의 (상위 SSOT · 인용 전용)
- `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol — `[미검증]` 마커·임계값 (상위 SSOT · 인용 전용)
