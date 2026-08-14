---
phase: 8
title: "Phase 8 infra-kit — 확보된 외부 근거"
collected: 2026-08-13
method: codex (foreground, 직접 호출)
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치를 지어내지 마라.
---

출처 유형: WebSearch fallback

**1. 관찰 사실**
- I1 게이트 무력화: 현재 `infra-test`는 이미 `set -euo pipefail`, `nullglob`, 실패 누적 후 `exit "$fail"`, 미설치 도구 `[미검증]` 표기를 반영하고 있다. 다만 표준화할 내부 taxonomy가 아직 “정책 위반”과 “검사 실행 실패”를 명확히 분리하는 형식으로 고정되지는 않았다. Conftest는 기본적으로 정책 실패 시 exit 1이며, `--fail-on-warn`에서는 0=실패/경고 없음, 1=경고 있음, 2=실패 있음으로 구분한다: https://www.conftest.dev/options/
- SARIF `executionSuccessful`: 이번 웹 하드캡 안에서 OASIS SARIF 원문 확인은 미확인. 추론: SARIF 채택 시 “결과 0건”과 “분석 도구 실행 실패”를 같은 빈 results로 내보내면 안 되며, OASIS SARIF 2.1.0 원문 확인 후 `invocations[].executionSuccessful`/notification 정책을 넣어야 한다.
- I2 로컬 부채 확인: `.github/dependabot.yml` 없음. `.github/workflows/ci.yml`은 `permissions: read-all`은 있으나 `actions/checkout@v7`, `actions/setup-python@v7`, `actions/setup-node@v7`, `actions/upload-artifact@v7`가 모두 태그 참조다. GitHub 공식 문서는 full-length commit SHA pinning만 immutable release로 취급하고, 태그는 이동/삭제 위험이 있다고 한다: https://docs.github.com/en/actions/reference/security/secure-use
- GitHub Actions 보안 현행: GitHub는 `GITHUB_TOKEN` 최소 권한, `pull_request_target`에서 untrusted checkout 회피, third-party actions full SHA pinning, OIDC short-lived token 사용을 권장한다. OIDC는 job마다 토큰을 만들고 클라우드가 short-lived access token을 발급하는 모델이다: https://docs.github.com/en/actions/concepts/security/openid-connect
- Dependabot 현행: GitHub 공식 options reference는 `dependabot.yml`의 `version: 2`, `updates`, `package-ecosystem`, `directory`/`directories`, `schedule` 기반 설정을 문서화한다. GitHub Actions도 Dependabot 업데이트 대상이며, 로컬 액션과 `docker://` 참조는 제한이 있다: https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference
- I3 절차: USE Method는 “모든 리소스에 대해 utilization, saturation, errors를 확인”하는 초기 병목 배제 절차다. CPU run queue, memory paging/swap, disk queue, network drops 같은 saturation/error 지표를 먼저 본다: https://www.brendangregg.com/usemethod.html
- RED Method 1차 출처는 이번 하드캡 안에서 미확인. 추론: RED는 서비스 단위 request rate, error rate, duration을 보고, USE는 호스트/런타임 리소스 병목을 보는 절차로 분리해 쓰는 것이 맞다.
- OTel 현행 상태: OpenTelemetry는 signal별로 개발되고, tracing은 stable, metrics는 API/protocol stable이지만 SDK는 mixed, logging은 stable, profiles protocol은 development다. 따라서 로컬 문서의 “OTel 3 signals stable”류 표현은 과잉 단정일 수 있다: https://opentelemetry.io/docs/specs/status/
- 1차 출처 6건 기준 낡을 수 있는 지점:
  - Kubernetes PSA는 v1.25 stable, namespace label로 `enforce`/`audit`/`warn` 및 `privileged`/`baseline`/`restricted`를 설정한다. 로컬 PSA 기준은 대체로 유효하나, Gateway API/Karpenter/DRA/v1.35 GA 등은 이번 지정 PSA 출처로 확인한 사실이 아니므로 별도 확인 전 강한 FAIL 규칙으로 두면 안 된다: https://kubernetes.io/docs/concepts/security/pod-security-admission/
  - Terraform ephemeral은 현재 `/language/block/ephemeral`로 리다이렉트되며, ephemeral/write-only 값은 state/plan에 저장되지 않는다고 문서화되어 있다. 최소 버전 번호는 이번 조회 라인에서 미확인: https://developer.hashicorp.com/terraform/language/ephemeral
  - OpenTofu v1.11 state/plan encryption은 `state`, `plan`, `enforced`, `fallback` migration을 문서화한다. “OpenTofu 1.7+” 도입 버전은 이번 조회에서 미확인: https://opentofu.org/docs/v1.11/language/state/encryption/
  - SLSA provenance는 v1.2 Approved이며 산출물이 어디서/언제/어떻게 만들어졌는지 추적하는 검증 가능 정보다. 모든 레포에 L3를 즉시 FAIL로 강제할 근거는 아니다: https://slsa.dev/provenance
  - Sigstore Cosign 출처는 `cosign attest`와 `cosign verify-attestation`, CUE/Rego predicate validation을 확인한다. 로컬의 “Cosign v3 bundle/trusted-root”는 이 URL만으로는 미확인: https://docs.sigstore.dev/cosign/verifying/attestation/

**2. 권장안**
- I1: infra-test/infra-audit 공통으로 결과 상태를 고정한다: `PASS`, `VIOLATION`, `SKIP_NO_TARGET`, `[미검증] TOOL_OR_ENV_MISSING`, `EXECUTION_ERROR`. CI exit는 예: 0=검사 실행 성공+위반 없음, 1=정책 위반, 2=검사 실행 실패/구성 오류/필수 도구 부재. 단, Conftest 같은 도구별 native exit는 wrapper에서 내부 상태로 번역한다.
- 모든 게이트 스크립트는 대상 수, 규칙 소스 수, 실행 도구 수, 미설치 도구 수를 먼저 출력한다. 대상 0건은 `SKIP_NO_TARGET`, 도구 부재는 `[미검증]`, 실행 실패는 `EXECUTION_ERROR`로 분리한다.
- GitHub workflow 검사는 grep보다 YAML parser로 `jobs.*.steps[].uses`와 `jobs.*.uses`를 모두 열거한다. 로컬 `uses: ./...`만 제외하고, 원격 action은 full SHA를 기본 요구로 둔다. GitHub-owned `actions/*`를 예외로 둘지는 정책 질문으로 남겨야 한다.
- Dependabot은 최소 `.github/dependabot.yml`에 `github-actions` `/`를 추가하고, 실제 lockfile/manifest가 있는 생태계만 추가한다. 예: npm lockfile이 있으면 `npm`, Dockerfile이 있으면 `docker`, GitHub Actions는 항상 검토.
- CI에는 `scripts/detect-docs-drift.py --json` 결과를 이용해 `docs/infra/**` 변경 시 대응 `docs/infra-kit/*.html` 존재/등록/변경 여부를 검사하는 게이트를 추가한다. 현재 `validate-post-kaizen.py`의 HTML 검사는 harness 전용이라 infra 산출물 누락을 막지 못한다.
- I3: observability 원칙에 “환경 요인 선배제” 절차를 추가한다. RED로 사용자 영향(rate/errors/duration)을 확인하고, 동시에 USE로 host/runtime/container의 CPU run queue, memory pressure/swap, disk I/O queue/errors, network drops/retransmits, process/runtime GC/thread/event-loop 지표를 확인한다. 호스트/런타임 saturation 증거가 있으면 앱 코드 원인 단정 금지.

넣지 말아야 할 것:
- K8s, Gateway API, Karpenter, DRA, service mesh, IDP, FinOps, sustainability를 신호 없는 레포에 새 FAIL 규칙으로 강제하지 말 것.
- SLSA/Cosign/SBOM을 릴리스·배포 산출물이 없는 레포의 필수 FAIL로 만들지 말 것. 해당 workflow가 있을 때 게이트로 승격.
- OTel “3 signals 모두 stable” 같은 단일 문장으로 덮지 말 것. signal/component별 status를 유지.
- 도구 미설치를 “위반 0” 또는 “PASS”로 세지 말 것.
- `pull_request_target`을 일반 PR 검증 기본값으로 넣지 말 것.

**3. 트레이드오프**
- SHA pinning은 공급망 안전성은 높지만 업데이트가 불편하고 Dependabot alerts와의 상호작용이 제한된다. 같은 줄 주석으로 원래 tag를 남기면 업데이트 운영성이 나아진다.
- 미설치 도구를 exit 2로 강하게 막으면 CI 재현성은 좋아지지만 기여자 진입 장벽이 오른다. 필수 게이트와 권장 스캔을 나눠야 한다.
- YAML parser 기반 workflow 검사는 grep보다 정확하지만 구현량이 늘어난다.
- 환경 선배제 절차는 조사 시간을 초기에 늘리지만, iOS simulator jank 같은 호스트/swap 원인 오진을 줄인다.

**4. 열린 질문**
- Actions SHA pinning 범위: 모든 원격 action인가, third-party만인가?
- 필수 도구 부재를 즉시 exit 2로 막을지, `[미검증]` 누적 임계로 막을지?
- Dependabot 대상 생태계: 이 레포에서 GitHub Actions 외에 npm만 포함할지, Docker/Python도 포함할지?
- SARIF는 실제 산출 포맷으로 채택할지? 채택한다면 OASIS SARIF 원문으로 `executionSuccessful` 필드를 추가 확인해야 한다.
- SLSA/Cosign은 릴리스 workflow가 생길 때까지 권장으로 둘지, 현재 CI에도 provenance/SBOM 생성만 먼저 넣을지?
