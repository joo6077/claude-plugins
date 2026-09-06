---
version: 1.3.0
last_updated: 2026-08-13
---

# Infra Kit Research Log

## [2026-08-13] - Phase 8 kaizen

CHANGED. Step 0.6 선별에서 infra-kit 은 low-signal 제외 후보였으나 사용자가 전체 14 Phase 를 선택해 실행했다.
외부 근거는 codex 를 foreground 로 호출해 `.harness/.meta/evidence/phase8.md` 에 파일로 고정한 뒤 그 파일만
읽고 작업했다 (백그라운드 실행 중 네트워크 조회 금지). 커밋 `73ef4e7` — 11 파일.

### 조회한 외부 소스 (근거 파일 `.harness/.meta/evidence/phase8.md`)

| # | 소스 | 조회 결과 | 채택 |
| --- | ---- | --------- | ---- |
| 1 | [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use) | **full-length commit SHA 만 immutable release 로 취급**. 태그는 이동·삭제 위험 | **채택** — 핀닝 rule 을 grep → YAML 파서 기반으로 재작성 |
| 2 | [Dependabot options reference](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference) | `version: 2` · `updates` · `package-ecosystem` · `directory`/`directories` · `schedule`. GitHub Actions 도 업데이트 대상이며 로컬 액션과 `docker://` 참조는 제한 | **채택** — 탐지된 생태계만 등록하는 rule 을 3 표면에 신설 |
| 3 | [GitHub Actions OIDC 개념](https://docs.github.com/en/actions/concepts/security/openid-connect) | job 마다 토큰을 만들고 클라우드가 short-lived access token 을 발급하는 모델 | **채택** — audit-criteria·infra-init 의 OIDC 링크를 현행 경로로 갱신 |
| 4 | [USE Method — Brendan Gregg](https://www.brendangregg.com/usemethod.html) | 모든 리소스에 대해 utilization · saturation · errors 를 확인하는 초기 병목 배제 절차. CPU run queue, memory paging/swap, disk queue, network drops | **채택** — `observability.md` §8 신설 |
| 5 | [OpenTelemetry spec status](https://opentelemetry.io/docs/specs/status/) | signal 별로 성숙도가 다르다 — traces stable / metrics API·protocol stable + SDK mixed / logs stable / profiles protocol development | **채택** — "3 신호 stable" 과잉 단정을 signal 별로 분해 |
| 6 | [Conftest options](https://www.conftest.dev/options/) | 기본은 정책 실패 시 exit 1, `--fail-on-warn` 에서는 0=없음 / 1=경고 / 2=실패 | 참조 — 도구별 native exit 를 wrapper 가 내부 상태로 번역해야 한다는 근거 |
| 7 | [Kubernetes PSA](https://kubernetes.io/docs/concepts/security/pod-security-admission/) | v1.25 stable, namespace 라벨로 `enforce`/`audit`/`warn` × `privileged`/`baseline`/`restricted` | 재확인 — 변경 없음. Gateway API·Karpenter·DRA 는 이 출처로 확인한 사실이 아니므로 FAIL 규칙화하지 않음 |
| 8 | [Terraform ephemeral](https://developer.hashicorp.com/terraform/language/ephemeral) | ephemeral / write-only 값은 state·plan 양쪽에 저장되지 않음. **최소 버전 번호는 이번 조회에서 미확인** | 재확인 — 버전 서술을 추가하지 않음 |
| 9 | [OpenTofu state encryption](https://opentofu.org/docs/v1.11/language/state/encryption/) | `state` · `plan` · `enforced` · `fallback` migration 문서화. **"1.7+" 도입 버전은 이번 조회에서 미확인** | **채택** — audit-criteria 의 "OpenTofu 1.7+ native encryption" 버전 단정을 제거 |
| 10 | [SLSA provenance](https://slsa.dev/provenance) | v1.2 Approved. 모든 레포에 L3 를 즉시 FAIL 로 강제할 근거는 아님 | **채택** — 릴리스 워크플로가 실재할 때만 게이트로 승격 |
| 11 | [Sigstore Cosign attestation](https://docs.sigstore.dev/cosign/verifying/attestation/) | `cosign attest` / `verify-attestation` + CUE/Rego predicate validation. **"v3 bundle/trusted-root" 는 이 URL 로 미확인** | 재확인 — v3 전용 서술을 강화하지 않음 (2026-07-27 판단 유지) |

RED Method 1 차 출처와 SARIF `executionSuccessful` 원문은 이번 하드캡 안에서 확보하지 못해 **미확인**으로 남겼다.

### 실행 증거 — 현행 핀닝 오라클이 이 레포에서 오탐 6 건

기존 `grep` 기반 핀닝 검사를 이 레포 워크플로에 그대로 돌린 결과 **미핀닝 6 건을 전부 0 건으로 보고**했다.
원인은 `grep -vE 'uses:[[:space:]]*actions/'` 가 GitHub-owned 액션을 정책 질문으로 남기지 않고 조용히
면제하는 것이다. `jobs.<id>.uses`(재사용 워크플로 호출)는 애초에 열거되지도 않았다.

새 골격을 `infra-test/SKILL.md` 에서 그대로 추출해 fixture 8 종으로 전수 검증했다:
A 실레포(미핀닝 6)=1 · B 대상 0=3 · C 혼합=1 · D YAML 파손=2 · E 전부 핀닝=0 · F 핵심 도구 부재=2 ·
G python3 부재=2 · H first-party 면제=0. `bash -n` 0 · `shellcheck` 0.

음성 대조: 핵심 도구 사전 검사를 제거하면 `grep` 부재 환경에서 `grep -q` 가 비영 종료해
**"checkout 스텝 없음" VIOLATION 을 오보**한다 (실제 관측한 회귀).

### 변경 내역

- `infra-kit/references/gate-result-taxonomy.md` **신설** — infra-kit 안에서 상태어 SSOT. 5 상태
  (`PASS` / `VIOLATION` / `SKIP_NO_TARGET` / `TOOL_OR_ENV_MISSING` / `EXECUTION_ERROR`) + 검사 시작
  **전** 출력하는 머리말 4 카운터(대상 수 · 규칙 소스 수 · 사용 가능 도구 수 · 미설치 도구 수) +
  핵심 도구(`grep`·`python3`)와 선택 도구(`hadolint`·`actionlint`·`kubeconform`·`conftest`·`cosign`·`trivy`)
  분리 + 재검증 명령 의무. exit 숫자는 `harness/evals/gate-exit-codes.md`, `[미검증]` 임계값은
  `qa-evaluation-guide.md` 를 **인용만** 하고 재정의하지 않는다. 실행 불완전이 정책 위반을 이긴다
  (한 run 에 둘 다 있으면 exit 2, 단 세 카운트를 모두 출력).
- `skills/infra-test/SKILL.md` — Gotcha 11 을 taxonomy 위임형으로 정정, Gotcha 13(핵심/선택 도구 분리) ·
  14(YAML 파서 핀닝) · 15(Dependabot 생태계 정합) 신설. Step 5 샘플 스크립트를 머리말 4 카운터 +
  5 상태 + YAML 파서 골격으로 교체하고 first-party 면제를 `PIN_ALLOW_FIRST_PARTY_TAGS` opt-in 으로 표면화.
- `skills/infra-audit/SKILL.md` — Gotcha 11 을 `[미검증:ENV]` / `[미검증:INVALID]` 4 분기로 정합,
  Gotcha 12 를 taxonomy SSOT 위임으로 정정. Step 3a 머리말을 4 카운터 포맷으로 교체하고 대상 0 건은
  표를 만들지 않고 `SKIP_NO_TARGET` 으로 종결. 예시 rule 표에 Dependabot 행 신설.
- `skills/infra-init/SKILL.md` — Gotcha 13(Dependabot 은 탐지된 생태계만) · 14(핀닝 정책을 조용히
  정하지 마라) · 15(게이트 스텝은 결과 상태를 구분해 exit 전파) 신설.
- `skills/infra-guide/SKILL.md` — Gotcha 12(USE × RED 환경 선배제) · 13(OTel 성숙도를 한 문장으로
  단정 금지) 신설. observability 라우팅 키워드에 "느려요 · 지연 · saturation · USE · RED" 추가.
- `agents/infra-reviewer.md` — §9 를 Phase 3 canonical 2026-08-13 개정본으로 갱신 (4 분기 ·
  `UNVERIFIED_ENV` / `UNVERIFIED_INVALID_EVIDENCE` 카운터 분리 · 남용 방지 4 요건 ·
  `verified_coverage` 0.60 → BLOCKED · verdict 우선순위) + §9b User-Reported Failure Protocol 신설.
- `references/audit-criteria.md` — `##` 섹션 순서가 리포트 카테고리 순서의 SSOT 임을 명시.
  원격 `uses:` SHA 핀닝 rule 재작성 + Dependabot 생태계 정합 rule 신설. Observability 를 signal 별
  판정으로 분해하고 USE 선배제 rule(권장) 추가. 판정 기준에 `[미검증]` 분기와 "도입 전 단계를 FAIL 로
  강제하지 마라" 를 추가.
- `references/init-checklist.md` · `references/principle-index.md` — 위 규칙에 맞춰 라우팅·체크리스트 정합.
- `docs/infra/operations/observability.md` (v0.2.0) — §8 "성능 조사는 환경 요인을 먼저 배제한다
  (USE × RED)" 신설. 리소스별 saturation/error 지표 표 포함. RED 는 1 차 출처 미확인임을 문서에 명시.
  Gotchas 에 OTel signal 별 상태 항목 추가.

### 사실 정정 4 종

- **카테고리 순서 드리프트** — `infra-reviewer` 6~10 번이 `audit-criteria.md` SSOT 순서와 어긋나 있었다
  (Supply Chain / Backup & DR / Deployment / Observability / Cost → SSOT 순서로 정렬).
- **stale 사본 참조** — `infra-audit` 의 백틱 `references/audit-criteria.md` 2 건이 스킬 디렉토리 기준
  상대 경로여서 Apr-04 7 카테고리 사본을 가리켰다 (SSOT 는 10 카테고리).
- **OTel 과잉 단정** — "3 신호 통합" 단일 문장을 signal 별 status 로 분해.
- **OpenTofu 버전 단정** — "1.7+ native encryption" 은 지정 출처로 확인되지 않아 버전 표기를 제거.

### 경계 준수 — 넣지 않은 것

- **K8s · Gateway API · Karpenter · DRA · service mesh · IDP · FinOps 를 신호 없는 레포의 새 FAIL
  규칙으로 만들지 않았다.** 해당 인프라가 없으면 N/A 다.
- **SLSA provenance · Cosign 서명 · SBOM 은 릴리스·배포 워크플로가 실재할 때만 게이트로 승격**하도록
  두었다. 도입 전 단계를 FAIL 로 강제하지 않는다.
- **SARIF `executionSuccessful` 은 미반영으로 남겼다** — OASIS SARIF 원문을 확보하지 못했다. 채택하려면
  원문에서 `invocations[].executionSuccessful` 과 notification 정책을 먼저 확인해야 한다.
- Cosign v3 전용 플래그와 Terraform ephemeral 최소 버전도 지정 출처로 확인되지 않아 서술을 강화하지 않았다.
- `pull_request_target` 을 일반 PR 검증 기본값으로 넣지 않았다.

### 다음 사이클 후보 (이번에 미반영)

- **SARIF 채택 여부** — 산출 포맷으로 쓸지 결정하고, 쓴다면 OASIS SARIF 2.1.0 원문으로
  `executionSuccessful` / notification 정책을 확정할 것.
- **RED Method 1 차 출처 확보** — `observability.md` §8 이 현재 RED 를 출처 없이 절차 이름으로만 쓴다.
- **docs 드리프트 게이트** — `docs/infra/` 변경 시 대응 `docs/infra-kit/` HTML 의 존재·등록·갱신을
  검사할 것. 현재 `validate-post-kaizen.py` 의 HTML 검사는 harness 전용이라 infra 산출물 누락을 막지 못한다.
- **열린 정책 질문 2 건** — (a) 필수 도구 부재를 즉시 exit 2 로 막을지, `[미검증]` 누적 임계로 막을지
  (b) GitHub-owned `actions/*` 핀닝 면제를 조직 기본값으로 둘지.
- `distroless-builder-glibc-mismatch` — 2026-07-27 부터 이월. 여전히 1 차 출처 미확보.

---

## [2026-07-27] - Phase 8 kaizen

CHANGED. Step 0.6 에서 infra-kit 은 LOW signal 이었으나, (a) Phase 3 이 `infra-reviewer` 를
canonical drift 대상으로 실명 지목했고 (b) digest 의 exit-code 캡처 3 회 반복 신호가 infra-test
샘플 스크립트의 실제 결함으로 재현되어 변경했다.

### 조회한 외부 소스 (Context7 은 OAuth 미인증 — 전부 WebFetch 직접 조회)

| # | 소스 | 조회 결과 | 채택 |
| --- | ---- | --------- | ---- |
| 1 | [Kubernetes PSA](https://kubernetes.io/docs/concepts/security/pod-security-admission/) | PSA `v1.25 [stable]`. 라벨 `pod-security.kubernetes.io/<MODE>: <LEVEL>`, MODE=enforce/audit/warn, LEVEL=privileged/baseline/restricted, `-version` 라벨은 선택 | 현행 기준과 일치 — 변경 없음 |
| 2 | [Terraform ephemeral](https://developer.hashicorp.com/terraform/language/ephemeral) | ephemeral 블록 · write-only 인수 · `ephemeral = true` 변수. state·plan 양쪽에서 완전 누락, `locals` 참조 시 재귀 적용. 문서 최신 표기 v1.15.x | 현행 기준과 일치 — 변경 없음 |
| 3 | [OpenTofu state encryption](https://opentofu.org/docs/v1.11/language/state/encryption/) | key provider 6 종(PBKDF2 · AWS KMS · GCP KMS · Azure Vault · OpenBao · External(experimental)). 프로덕션 method 는 AES-GCM 만. PBKDF2 기본 600,000 iteration(최소 200,000) | 현행 기준과 일치 — 변경 없음 |
| 4 | [SLSA provenance](https://slsa.dev/provenance) | 스펙 v1.2 Approved. build provenance / source provenance 2 종 분리 | 현행 기준과 일치 — 변경 없음 |
| 5 | [Sigstore Cosign attestation](https://docs.sigstore.dev/cosign/verifying/attestation/) | `cosign verify-attestation` + CUE/Rego `--policy`. 검증 대상은 predicate 부분 | **v3 전용 플래그 근거 없음** → audit-criteria 의 Cosign 서술 강화하지 않음 (추측 금지) |
| 6 | [OpenTelemetry spec status](https://opentelemetry.io/docs/specs/status/) | traces API/SDK/protocol Stable · logs bridge API/SDK/protocol Stable · metrics API·protocol Stable / SDK Mixed · profiles protocol Development | "3 신호 stable" 서술 유지 가능 — 변경 없음 |
| 7 | [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) | 비-Windows 기본 셸은 `bash -e {0}` 로 **pipefail 없음**. `shell: bash` 명시 시에만 `bash --noprofile --norc -eo pipefail {0}` | **채택** — audit-criteria CI/CD 신규 rule 2 행, infra-test Gotcha 11, infra-init Gotcha 12 |
| 8 | [Docker build best practices](https://docs.docker.com/build/building/best-practices/) | 파이프는 마지막 명령 exit code 만 평가 → `set -o pipefail &&` 선행 필요. digest 핀닝은 `FROM alpine:3.21@sha256:...` 권장하되 수동 유지보수·자동 보안패치 포기 트레이드오프 명시 | pipefail **채택**. digest 는 트레이드오프 근거로 "고정 태그 **또는** digest" 현행 표현 유지 |

### 실행 증거 — infra-test Step 5 샘플 스크립트 결함 3 건 (재현 완료)

기존 `tests/ci-validation.sh` 원문을 fixture 로 실행한 결과:

- 서드파티 SHA 핀닝 검사가 `grep -v "actions/"` 앵커 부재로 `aws-actions/*` · `google-github-actions/*` 를 제외 → 미핀닝 3 건 중 1 건만 검출.
- WARN 출력 후에도 최종 `exit 0` → CI 게이트 무력화.
- 매칭 없는 glob 이 리터럴 1 회로 순회 → 워크플로 없는 프로젝트에서 "YAML syntax error" 오보 + `exit 1`.
- 반증: `set -e` 가 `A && { ... }` 에서 A 실패 시 스크립트를 종료시킨다는 가설은 **거짓**으로 확인(`EXIT=0`). 해당 가설 기반 수정은 하지 않았다.

수정본은 3 fixture(미핀닝 3 건 / 전부 핀닝 / 워크플로 없음)로 재검증하여 각각 `exit 1` · `exit 0` · `SKIP exit 0` 를 확인했다.

### 변경 내역

- `agents/infra-reviewer.md` — §9 를 qa-evaluation-guide §Canonical Unverified-Evidence Protocol 5 조항 정본 복제로 교체. 핵심규칙 5 의 임계값 중복 서술 제거. 인프라 도메인 적용 노트(FAIL / N/A / `[미검증]` 3 분기 매핑) 추가.
- `skills/infra-audit/SKILL.md` — Gotcha 11 을 SSOT 위임형으로 정정, Gotcha 12 신설(도구·규칙 소스 부재를 "위반 0" 으로 집계 금지). Step 3a 감사 범위 머리말 4 줄 신설. Step 4 를 canonical 조항 3 임계값으로 정합.
- `skills/infra-test/SKILL.md` — Gotcha 11(셸 실패 전파 4 항목) · Gotcha 12(도구 미설치 = `[미검증]`, 증거 블록 의무) 신설. Step 5 샘플 스크립트 3 결함 수정 + "빼면 안 되는 것" 표. Step 7 도구 존재 확인 선행, Step 8 증거 블록 3 종 의무화.
- `skills/infra-init/SKILL.md` — Gotcha 12 신설(반복 셸 명령을 스크립트/Makefile 로 코드화 + `set -euo pipefail` + `shell: bash` 병기).
- `references/audit-criteria.md` — CI/CD 에 "셸 실패 전파" · "검증 스텝 exit code" rule 2 행 + 출처 2 건 추가.
- `.claude/skills/infra-kaizen/SKILL.md` — validate-plugin "7 카테고리" → 8(V1~V8) 3 곳 정정. scope-creep 을 파일 수 → unit(관심사) 기준으로 재정의. Gotcha 7 에 `.harness/history/` 병렬 예외 추가. Gotcha 8 에 §3.7 / E1~E3 / Counterpart Enumeration + SSOT 인용 표 추가.

### 다음 사이클 후보 (이번에 미반영)

- `distroless-builder-glibc-mismatch` — builder 와 distroless 런타임의 glibc/ABI 불일치. 실재하는 결함 클래스이나 이번 사이클에 1 차 출처를 확보하지 못해 추측 서술을 피하고 보류. distroless 공식 저장소의 base variant 매트릭스를 확보한 뒤 `audit-criteria.md` Container 의 "베이스 이미지 거버넌스" 행에 붙일 것.
- `port-already-in-use`, `wrong-infra-path-assumption` — 단발 태그이고 infra-kit 산출물과 인과가 연결되지 않아 미반영.

---

## [2026-06-05] — Phase 8

NO_CHANGE. infra-init Gotcha #2/#4/#9 에 가드 포화. infra-test↔backend-test parity 3항목 대칭 확인. SKIP.


> infra-kaizen 실행 시 리서치한 외부 소스와 채택 여부를 누적 기록한다.

## [2026-05-07] — Phase 8 kaizen (infra, /insights 흡수)

### 데이터 소스

- 데이터 풀 §0 `/insights` 30 일 분석 (3 friction · 3 pattern · 3 feature)
- `harness/references/cross-kit-principles.md` v1 매트릭스의 infra 열

### Phase 8 변경

- infra/README.md 에 cross-kit-principles 매트릭스 cross-reference 섹션 추가
- plugin.json patch bump (이번 사이클)
- 매핑: infra-audit ANALYZE ↔ Pre-Edit Batch Audit, infra-reviewer self-check ↔ Self-Evaluator Audit, PostToolUse 정적 검증 ↔ Hook-Triggered Auto-Correction

### 외부 리서치 인용 (이전 사이클 보존, 이번 사이클 추가 없음)

이전 카이젠 사이클의 리서치 인용은 본 로그 하단 + cross-kit-principles 매트릭스로 보존된다.

---


---

## 2026-04-12

**트리거:** infra-research 수동 실행 (12개 카테고리 확충)

### 조사한 소스

| # | 제목 | URL | 유형 | 태그 | 결과 |
| - | ---- | --- | ---- | ---- | ---- |
| 23 | Kubernetes v1.35 Release (Timbernetes) | <https://kubernetes.io/blog/2025/12/17/kubernetes-v1-35-release/> | 공식 | [official] [dated: 2025-12] | 채택 |
| 24 | Kubernetes v1.33 Sneak Peek | <https://kubernetes.io/blog/2025/03/26/kubernetes-v1-33-upcoming-changes/> | 공식 | [official] [dated: 2025-04] | 채택 |
| 25 | Kubernetes Security: 2025 Stable Features and 2026 Preview | <https://www.cncf.io/blog/2025/12/15/kubernetes-security-2025-stable-features-and-2026-preview/> | CNCF | [blog] [dated: 2025-12] | 채택 |
| 26 | Karpenter v1 GA — CNCF Blog | <https://www.cncf.io/blog/2024/11/06/karpenter-v1-0-0-beta/> | CNCF | [blog] [dated: 2024-11] | 채택 |
| 27 | Karpenter 공식 사이트 (v1.11) | <https://karpenter.sh/> | 공식 | [official] [dated: 2026-03] | 채택 |
| 28 | Gateway API v1.4 — BackendTLSPolicy GA | <https://kubernetes.io/blog/2025/11/06/gateway-api-v1-4/> | 공식 | [official] [dated: 2025-10] | 채택 |
| 29 | OpenTofu 1.10.0 릴리스 | <https://opentofu.org/blog/opentofu-1-10-0/> | 공식 | [official] [dated: 2025-06] | 채택 |
| 30 | OpenTofu 1.9.0 — provider for_each | <https://opentofu.org/blog/opentofu-1-9-0/> | 공식 | [official] [dated: 2025-01] | 채택 |
| 31 | Pulumi 2025 Product Launches (Neo, ESC, IDP) | <https://www.pulumi.com/blog/2025-product-launches/> | 공식 | [blog] [dated: 2025-12] | 채택 |
| 32 | Pulumi ESC Rotated Secrets | <https://www.pulumi.com/blog/pulumi-release-notes-117/> | 공식 | [blog] [dated: 2025-10] | 채택 |
| 33 | Pulumi ESC Open Approvals (JIT Access) | <https://www.pulumi.com/blog/esc-open-approvals/> | 공식 | [blog] [dated: 2025-08] | 채택 |
| 34 | Dagger — Programmable CI/CD Engine | <https://dagger.io/> | 공식 | [official] [dated: 2026-04] | 채택 |
| 35 | Dagger Overview Docs | <https://docs.dagger.io/> | 공식 | [official] [dated: 2026-04] | 채택 |
| 36 | Argo CD v3.2 Stable Release | <https://github.com/argoproj/argo-cd/releases> | 공식 | [official] [dated: 2025-11] | 채택 |
| 37 | Argo CD v2.14 → 3.0 Upgrade Guide | <https://argo-cd.readthedocs.io/en/latest/operator-manual/upgrading/2.14-3.0/> | 공식 | [official] [dated: 2025-06] | 채택 |
| 38 | Flux v2.8 GA — Helm v4, Web UI | <https://fluxcd.io/blog/2026/02/flux-v2.8.0/> | 공식 | [official] [dated: 2026-02] | 채택 |
| 39 | Flux v2.5 — CEL Integration, GitHub App Auth | <https://www.infoq.com/news/2025/03/flux-gitops-release/> | 뉴스 | [blog] [dated: 2025-03] | 채택 |
| 40 | Cosign v3 릴리스 | <https://blog.sigstore.dev/cosign-3-0-available/> | 공식 | [official] [dated: 2025-06] | 채택 |
| 41 | GitHub Actions SHA Pinning Policy | <https://github.blog/changelog/2025-08-15-github-actions-policy-now-supports-blocking-and-sha-pinning-actions/> | 공식 | [official] [dated: 2025-08] | 채택 |
| 42 | GitHub Actions 2026 Security Roadmap | <https://github.blog/news-insights/product-news/whats-coming-to-our-github-actions-2026-security-roadmap/> | 공식 | [official] [dated: 2026-01] | 채택 |
| 43 | GitHub Actions OIDC + Repository Custom Properties | <https://github.blog/changelog/2026-03-12-actions-oidc-tokens-now-support-repository-custom-properties/> | 공식 | [official] [dated: 2026-03] | 채택 |
| 44 | GitHub Actions Immutable Actions (publish-immutable-action) | <https://github.com/actions/publish-immutable-action> | 공식 | [official] | 채택 |
| 45 | Grafana Alloy — OTel Collector 배포판 | <https://grafana.com/oss/alloy-opentelemetry-collector/> | 공식 | [official] [dated: 2026-04] | 채택 |
| 46 | Grafana Alloy at 1: What's New | <https://grafana.com/blog/alloy-one-year/> | 공식 | [blog] [dated: 2025-04] | 채택 |
| 47 | Grafana Observability Survey 2025 | <https://grafana.com/observability-survey/2025/> | 공식 | [blog] [dated: 2025-06] | 채택 |
| 48 | Cilium Service Mesh 공식 문서 | <https://docs.cilium.io/en/stable/network/servicemesh/> | 공식 | [official] [dated: 2026-03] | 채택 |
| 49 | Cilium eBPF Security — CNCF Blog | <https://www.cncf.io/blog/2025/01/02/unlocking-cloud-native-security-with-cilium-and-ebpf/> | CNCF | [blog] [dated: 2025-01] | 채택 |
| 50 | Backstage Wrapped 2025 | <https://backstage.io/blog/2025/12/30/backstage-wrapped-2025/> | 공식 | [official] [dated: 2025-12] | 채택 |
| 51 | Backstage 89% IDP Market Share | <https://byteiota.com/backstage-hits-89-idp-market-share-what-it-means/> | 뉴스 | [blog] [dated: 2026-02] | 참조 |
| 52 | Platform Engineering in 2026 — Roadie.io | <https://roadie.io/blog/platform-engineering-in-2026-why-diy-is-dead/> | 블로그 | [blog] [dated: 2026-01] | 참조 |
| 53 | State of FinOps 2026 Report | <https://data.finops.org/> | 공식 | [official] [dated: 2026-03] | 채택 |
| 54 | FinOps X 2025 Cloud Announcements | <https://www.finops.org/insights/finops-x-2025-cloud-announcements/> | 공식 | [official] [dated: 2025-06] | 채택 |
| 55 | FOCUS (FinOps Open Cost and Usage Specification) | <https://www.finops.org/insights/finops-x-2025-cloud-announcements/> | 공식 | [spec] [dated: 2025-06] | 채택 |
| 56 | Velero 공식 사이트 | <https://velero.io/> | 공식 | [official] [dated: 2026-04] | 채택 |
| 57 | EU Cyber Resilience Act — SBOM Requirements | <https://craevidence.com/blog/sbom-requirements-under-cra> | 뉴스 | [blog] [dated: 2025-09] | 채택 |
| 58 | OpenSSF — SBOMs in the Era of CRA | <https://openssf.org/blog/2025/10/22/sboms-in-the-era-of-the-cra-toward-a-unified-and-actionable-framework/> | 공식 | [official] [dated: 2025-10] | 채택 |
| 59 | CycloneDX ECMA-424 표준 | <https://cyclonedx.org/> | 공식 | [spec] [dated: 2026-04] | 채택 |
| 60 | CNCF State of Cloud Native Development 2025 | <https://www.cncf.io/announcements/2025/11/11/cncf-and-slashdata-survey-finds-cloud-native-ecosystem-surges-to-15-6m-developers/> | CNCF | [official] [dated: 2025-11] | 채택 |
| 61 | KubeEdge — CNCF Graduated Edge Project | <https://blog.easecloud.io/containers/kubernetes-edge-guide-kubeedge-edge-computing/> | 블로그 | [blog] [dated: 2025-08] | 채택 |
| 62 | CNCF CTO 2026 Cloud Native Predictions | <https://www.techedubyte.com/cncf-cto-2026-cloud-native-trends-insights/> | 뉴스 | [blog] [dated: 2026-01] | 참조 |

### 채택한 인사이트

#### Container Orchestration — Kubernetes

- **Kubernetes v1.35 (2025-12) In-Place Pod Resource Updates GA**: CPU/메모리를 Pod 재시작 없이 동적 조정 가능 (KEP #1287). 수직 스케일링의 다운타임 제거. 적용: infra-audit Kubernetes 카테고리, init-checklist.
- **Kubernetes v1.35 DRA (Dynamic Resource Allocation) Core APIs GA**: GPU 등 특수 하드웨어를 표준화된 할당 인터페이스로 관리. 적용: infra-guide GPU/특수 워크로드 섹션.
- **Kubernetes v1.35 Pod Certificates for Workload Identity (Beta)**: Kubelet이 자동으로 키를 생성하고 PodCertificateRequest로 인증서 요청. cert-manager 없이 네이티브 워크로드 ID 가능. 적용: infra-audit Security 카테고리 (watch).
- **Karpenter v1.11 (2026-03)**: CNCF 산하 Kubernetes 노드 오토스케일러. NodePool + EC2NodeClass CRD로 선언적 프로비저닝. Cluster Autoscaler 대비 빠른 스케일업 + 비용 최적화 (underutilized 노드 자동 교체). Salesforce 1,000+ EKS 클러스터 마이그레이션 사례. 적용: infra-guide Kubernetes 노드 관리, cost-optimization.
- **Gateway API v1.4 (2025-10) Standard Channel**: BackendTLSPolicy GA (게이트웨이→백엔드 TLS 암호화), supportedFeatures in GatewayClass (구현체 기능 선언), Named Rules for Routes. Mesh 리소스 실험적 도입. 4개월 릴리스 주기. 적용: infra-audit Networking, infra-guide.

#### IaC Tools

- **OpenTofu 1.10.0 (2025-06)**: OCI Registry 지원 (에어갭 환경), S3 네이티브 상태 잠금 (DynamoDB 불필요), OpenTelemetry 트레이싱, 외부 키 프로바이더 (state encryption 확장), deprecated 변수/출력 지원, CI/CD용 글로벌 프로바이더 캐시 잠금. 적용: infra-audit IaC 카테고리, init-checklist.
- **OpenTofu 1.9.0 (2025-01)**: provider for_each — 멀티존 배포를 하나의 모듈에서 관리. 코드 중복 감소. 적용: infra-guide IaC 패턴.
- **Pulumi ESC (Environment, Secrets, Configuration)**: Rotated Secrets (AWS IAM 자동 회전), Customer-Managed Keys (BYOK/KMS), Open Approvals (JIT 접근 제어), Versioning (불변 리비전 히스토리), ESC Connect (임의 시크릿 소스 연동). 적용: infra-guide IaC 카테고리 시크릿 관리 비교.

#### CI/CD Patterns

- **Dagger — 프로그래머블 CI/CD 엔진**: Go/Python/TypeScript SDK로 빌드 파이프라인을 코드로 작성. 컨테이너 내 실행으로 로컬-CI 동일 동작 보장. BuildKit 기반 DAG, 자동 캐싱, OpenTelemetry 스팬 내장. 적용: infra-guide CI/CD 카테고리 (YAML 대안).
- **GitHub Actions SHA Pinning 정책 (2025-08)**: 조직 수준에서 SHA 고정을 강제하고 뮤터블 태그 사용을 차단하는 정책 지원. 적용: infra-audit CI/CD Security.
- **GitHub Actions 2026 Security Roadmap**: Immutable Releases (발행 후 에셋/태그 변경 불가), `dependencies:` 섹션 (직접+전이 의존성 SHA 잠금), OIDC 토큰에 repository custom properties 클레임 추가. 적용: infra-audit CI/CD Security, init-checklist.
- **GitHub Actions OIDC 확장 (2026-03)**: repository custom properties를 OIDC 토큰 클레임에 포함 → 클라우드 제공자 신뢰 정책을 더 세밀하게 설정. 적용: infra-audit CI/CD Security.

#### GitOps

- **Argo CD 3.x (2025)**: 3.0 — 아키텍처 개선, RBAC 정제, 리소스 제외 개선. 3.1 — 네이티브 OCI 레지스트리 지원, CLI 플러그인, Source Hydrator. 3.2 (2025-11) — 안정 릴리스. v2.14 EOL (2025-11-04). 적용: infra-guide GitOps 섹션, 마이그레이션 가이드 필요.
- **Flux v2.8 (2026-02)**: Helm v4 서버사이드 적용 + kstatus 헬스 체크, Cosign v3 OCI 검증, CEL 기반 헬스 체크, Flux Operator Web UI, PR/MR 코멘트 프리뷰 환경. K8s 1.33-1.35 지원. 적용: infra-guide GitOps 섹션, infra-audit Deployment.
- **Flux v2.5 (2025-03)**: CEL 통합 (커스텀 리소스 헬스 체크), GitHub App 인증, 이벤트 메타데이터 어노테이션 강화. 적용: infra-guide GitOps.

#### Cloud-Native Security — Supply Chain

- **Cosign v3**: 새 번들 포맷 (서명 자료 + 오프라인 검증 정보 단일 파일), trusted-root (키 회전 시 클라이언트 업데이트 불필요), signing-config (투명성 로그 샤드 회전). v4 예고 — CLI 대폭 단순화, 플래그 50% 제거. 적용: infra-audit Supply Chain.
- **EU Cyber Resilience Act (CRA) SBOM 의무화**: 디지털 요소가 포함된 모든 EU 판매 제품에 SBOM 필수. CycloneDX 또는 SPDX 머신리더블 포맷. 직접+전이 의존성 전부 포함. **2026-09 취약점 보고 마감 임박**. 적용: infra-audit Supply Chain, init-checklist. [dated: 2026-09]
- **CycloneDX ECMA-424 국제표준**: SBOM/SaaSBOM/CBOM/HBOM/AI-ML BOM 지원. 260+ 도구 생태계. 20+ 프로그래밍 언어 지원. 적용: infra-audit Supply Chain.
- **OpenSSF — CRA 시대 SBOM 통합 프레임워크 (2025-10)**: SPDX + CycloneDX 공존 전략, EU 규정과 OpenSSF 사이 정합성 확보. 적용: infra-guide Security 참조.

#### Observability Infrastructure

- **Grafana Alloy — OTel Collector 배포판**: 120+ 컴포넌트로 메트릭/로그/트레이스/프로파일 수집. Prometheus 파이프라인 내장. Grafana Agent/Operator 2025-11 EOL → Alloy 마이그레이션 필수. 적용: infra-audit Observability, init-checklist.
- **Grafana 11 통합 쿼리 빌더**: 모든 데이터소스에 걸친 단일 쿼리 빌더, 메트릭-트레이스-로그 자동 상관관계 엔진, AI 기반 이상 탐지. 적용: infra-guide Observability.

#### Networking — Service Mesh / eBPF

- **Cilium v1.19 (2026-03)**: eBPF 기반 네트워킹 + 서비스 메시 + 보안 + 옵저버빌리티. 사이드카 없이 커널 레벨에서 mTLS (SPIFFE ID), L7 정책, 로드밸런싱, Hubble 옵저버빌리티. GKE Dataplane V2, AKS Azure CNI, EKS 기본 CNI 채택 확대. 적용: infra-audit Networking, infra-guide Service Mesh.
- **eBPF vs 사이드카 전환**: 2026년 핵심 질문은 "어떤 서비스 메시를 쓸까"가 아니라 "서비스 메시가 필요한가". eBPF 기반 CNI가 정책, 텔레메트리, 트래픽 관리를 커널에서 직접 처리. 적용: infra-guide Service Mesh 카테고리 관점 전환.

#### Platform Engineering

- **Backstage IDP 89% 시장 점유율**: CNCF Graduated 프로젝트. 2025 New Frontend System adoption-ready, Actions Registry + MCP 서버 지원 (AI 에이전트 통합), Backstage UI 디자인 시스템 알파. 적용: infra-guide Platform Engineering.
- **Gartner: 2026년 대형 조직 80%가 플랫폼 팀 설립 예측** (2022년 45%에서 증가). 2025년 55% 조직이 플랫폼 엔지니어링 도입. 적용: infra-guide Platform Engineering 원칙.
- **AI 통합**: CIO 92%가 플랫폼에 AI 통합 계획, DevOps 팀 76%가 2025 말까지 CI/CD에 AI 통합. IDP가 AI 에이전트 오케스트레이션 + LLMOps 워크플로우 제어 평면으로 진화. 적용: infra-guide Platform Engineering (향후 방향).

#### Cost Optimization — FinOps

- **State of FinOps 2026**: 범위 확장 — SaaS 90%, 라이선싱 64%, 프라이빗 클라우드 57%, 데이터센터 48% 관리. AI 관리 98% (2년 전 31%). 78% FinOps 팀이 CTO/CIO 직속. 적용: infra-guide Cost Optimization.
- **Shift-Left FinOps**: 배포 후 최적화가 아닌 배포 전 비용 예측. 구조적 FinOps 프로그램은 월 클라우드 비용 25-30% 절감, 성숙 프로그램은 낭비를 40%→15-20%로 감소. 적용: infra-audit Cost Optimization.
- **FOCUS 표준 (FinOps Open Cost and Usage Specification)**: 멀티 벤더 비용 데이터 정규화. AI 워크로드, 데이터센터, PaaS/SaaS 확장 요청 증가. 적용: infra-guide Cost Optimization.

#### Disaster Recovery & Backup

- **Velero 1.11**: K8s 리소스 + PV 백업/복원. etcd + 퍼시스턴트 볼륨 이중 백업. 크로스 리전/크로스 클러스터 복구 지원. 스케줄 백업 + 보존 정책 + pre/post 훅. 적용: infra-guide Backup/DR, init-checklist.
- **Velero + Restic 통합**: CDC (Content-Defined Chunking)로 PVC 40-70% 스토리지 절감. 증분 백업으로 RPO 초 단위, RTO 75% 감소. 적용: infra-audit Backup/DR.

#### Multi-Cloud & Hybrid Cloud

- **CNCF State of Cloud Native 2025**: 클라우드 네이티브 개발자 1,560만명. 하이브리드 클라우드 32%, 멀티클라우드 26%, 분산 클라우드 15%. 적용: infra-guide Multi-Cloud 원칙.
- **전략적 전환**: 임의적 멀티클라우드에서 의도적 인프라 전략으로 성숙. 워크로드 요구사항 + 비용 + 성능 + 회복력 기반 결정. 적용: infra-guide Multi-Cloud.

#### Edge Computing & CDN

- **KubeEdge CNCF Graduated (2024)**: K8s 기반 엣지 배포 패턴 표준화. 중앙 컨트롤 플레인 → 분산 엣지 노드 아키텍처. 적용: infra-guide Edge Computing.
- **엣지 아키텍처 4계층**: 디바이스 엣지 (센서) → 게이트웨이 엣지 (로컬 처리) → 리전 엣지 (마이크로 DC/CDN PoP) → 클라우드 (장기 저장/분석). 하이브리드 접근: 엣지에서 레이턴시 민감 처리, 클라우드에서 오케스트레이션. 적용: infra-guide Edge Computing.
- **엣지 컴퓨팅 시장**: 2025년 $21.4B → 2026년 $28.5B (CAGR 28%). CDN 시장 2025년 $32.7B. CDN 제공자의 엣지 컴퓨팅 기능 통합 (PoP에서 코드 실행) 가속. 적용: infra-guide Edge Computing (시장 맥락).

### 신규 스킬 갭 분석

| 제안 스킬 | 아키타입 | 근거 | 우선순위 | 상태 |
| --------- | -------- | ---- | -------- | ---- |
| `infra-supply-chain` | 런북 | SLSA + Cosign v3 + CycloneDX SBOM + EU CRA 대응 파이프라인 | 높음 | backlog |
| `infra-gitops` | 코드 스캐폴딩 | Argo CD 3.x / Flux v2.8 부트스트랩 | 중간 | backlog |
| `infra-finops` | 가이드 | FOCUS 표준 + shift-left FinOps + 태깅 전략 | 중간 | backlog |
| `infra-edge` | 가이드 | KubeEdge + 4계층 엣지 아키텍처 + CDN 통합 | 낮음 | backlog |
| `infra-platform` | 코드 스캐폴딩 | Backstage IDP 부트스트랩 + golden path 템플릿 | 중간 | backlog |

### 폐기 사유

없음.

---

## 2026-04-11

**트리거:** kaizen-orchestrator Phase 8 (research-mode rerun)

### 조사한 소스

| # | 제목 | URL | 유형 | 신뢰도 | 결과 |
| - | ---- | --- | ---- | ------ | ---- |
| 1 | Kubernetes Pod Security Admission | <https://kubernetes.io/docs/concepts/security/pod-security-admission/> | 공식 | 높음 | 채택 |
| 2 | Kubernetes Ingress / Gateway API | <https://kubernetes.io/docs/concepts/services-networking/ingress/> | 공식 | 높음 | 채택 |
| 3 | Kubernetes Sidecar Containers (v1.33 GA) | <https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers> | 공식 | 높음 | 채택 |
| 4 | Terraform 1.10+ ephemeral values | <https://developer.hashicorp.com/terraform/language/ephemeral> | 공식 | 높음 | 채택 |
| 5 | Terraform test framework | <https://developer.hashicorp.com/terraform/language/tests> | 공식 | 높음 | 채택 |
| 6 | OpenTofu 1.7+ state encryption | <https://opentofu.org/docs/v1.11/language/state/encryption/> | 공식 | 높음 | 채택 |
| 7 | OpenTofu for_each meta-argument | <https://opentofu.org/docs/language/meta-arguments/for_each/> | 공식 | 높음 | 채택 |
| 8 | SLSA provenance spec | <https://slsa.dev/provenance> | 공식 | 높음 | 채택 |
| 9 | SLSA v1.0 spec | <https://slsa.dev/spec> | 공식 | 높음 | 채택 |
| 10 | Sigstore Cosign attestation | <https://docs.sigstore.dev/cosign/verifying/attestation/> | 공식 | 높음 | 채택 |
| 11 | Trivy SBOM supply chain | <https://trivy.dev/docs/dev/guide/supply-chain/sbom/> | 공식 | 높음 | 채택 |
| 12 | Anchore Syft SBOM generator | <https://github.com/anchore/syft> | 공식 | 높음 | 채택 |
| 13 | Falco runtime security | <https://falco.org/> | 공식 | 높음 | 채택 |
| 14 | Tetragon eBPF runtime security | <https://tetragon.io/> | 공식 | 높음 | 채택 |
| 15 | Chainguard images overview | <https://edu.chainguard.dev/chainguard/chainguard-images/overview/> | 공식 | 높음 | 채택 |
| 16 | PyPI Trusted Publishers | <https://docs.pypi.org/trusted-publishers/> | 공식 | 높음 | 채택 |
| 17 | GitHub OIDC hardening | <https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect> | 공식 | 높음 | 채택 |
| 18 | GitHub OIDC reusable workflows | <https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/using-openid-connect-with-reusable-workflows> | 공식 | 높음 | 채택 |
| 19 | OpenTelemetry signals status | <https://opentelemetry.io/docs/specs/status/> | 공식 | 높음 | 채택 (logs/traces/metrics 3 stable) |
| 20 | OpenTelemetry semantic conventions | <https://opentelemetry.io/docs/specs/semconv/> | 공식 | 높음 | 채택 |
| 21 | Argo Rollouts | <https://argoproj.github.io/argo-rollouts/> | 공식 | 높음 | 채택 |
| 22 | Flux v2.6 release | <https://fluxcd.io/blog/2025/05/flux-v2.6.0/> | 공식 | 높음 | 채택 |

### 채택한 인사이트

- **Kubernetes Pod Security Admission (PSA) restricted** 이 2026 표준. `pod-security.kubernetes.io/enforce: restricted` 라벨로 네임스페이스 단위 강제. 적용: infra-audit Kubernetes 카테고리, init-checklist.
- **Gateway API 우선** (Ingress deprecated 방향 전환 아님, 하지만 Gateway API 가 HTTPRoute / TCPRoute / GRPCRoute 분리로 훨씬 유연). 적용: infra-guide.
- **Sidecar containers v1.33 GA**: init containers 중에 `restartPolicy: Always` 설정 시 sidecar 로 동작. istio proxy / log collector 패턴 표준화. 적용: init-checklist.
- **Terraform 1.10+ ephemeral values**: 민감 정보 (password, token) 를 state 파일에 저장하지 않음. `ephemeral = true` 선언으로 메모리에서만 존재. 적용: infra-audit IaC 카테고리, init-checklist.
- **Terraform test framework**: `terraform test` CLI 로 HCL 네이티브 단위 테스트. 적용: init-checklist.
- **OpenTofu 1.7+ state encryption**: Terraform 이 제공하지 않는 네이티브 state encryption 기능. HashiCorp 라이선스 대안 경로. 적용: infra-audit IaC 카테고리, init-checklist.
- **Supply Chain 카테고리 신설**: SLSA provenance (빌드 출처 증명) + Cosign attestation (서명 검증) + Syft SBOM (소프트웨어 자재 명세서) + Trusted Publishers (OIDC 기반 secretless 배포) + Falco/Tetragon (런타임 security). 2026 공급망 보안의 최소 기본값. 적용: audit-criteria 신규 섹션 5 rules + principle-index 신규 카테고리.
- **OpenTelemetry 3 signals stable**: Logs / Traces / Metrics 모두 stable 단계. 단일 Collector 파이프라인으로 통합 가능. 적용: infra-audit Observability.
- **GitOps 단일 소스 원천**: Argo CD / Flux v2.6+ 을 통한 배포. `kubectl apply` 직접 금지. Progressive delivery (Argo Rollouts) 로 canary / blue-green. 적용: infra-audit Deployment 카테고리.
- **Platform Engineering 카테고리 신설**: Internal Developer Platform (IDP), Backstage scaffolder, golden path. 적용: principle-index 신규 카테고리.

### 신규 스킬 갭 분석

| 제안 스킬 | 아키타입 | 근거 | 우선순위 | 상태 |
| --------- | -------- | ---- | -------- | ---- |
| `infra-supply-chain` | 런북 | SLSA + Cosign + Syft 스캐폴딩 파이프라인 | 높음 | backlog |
| `infra-gitops` | 코드 스캐폴딩 | Argo CD / Flux 부트스트랩 | 중간 | backlog |

### 폐기 사유

없음.

### PR

- <https://github.com/joo6077/claude-plugins/pull/6>

---

## 2026-04-12

**트리거:** infra-research 수동 실행 (12개 카테고리 추가 조사)

### 조사한 소스

| # | 제목 | URL | 유형 | 태그 | 결과 |
| - | ---- | --- | ---- | ---- | ---- |
| 63 | TLSRoute - Kubernetes Gateway API | <https://gateway-api.sigs.k8s.io/reference/api-types/tlsroute/> | 공식 | [spec] | 채택 |
| 64 | Terraform MCP server overview | <https://developer.hashicorp.com/terraform/mcp-server> | 공식 | [official] | 채택 |
| 65 | OpenTofu Registry | <https://opentofu.org/registry/> | 공식 | [official] | 채택 |
| 66 | Infrastructure AI - Pulumi Docs | <https://www.pulumi.com/docs/ai/> | 공식 | [official] | 채택 |
| 67 | GitHub-hosted runners reference | <https://docs.github.com/en/actions/reference/runners/github-hosted-runners> | 공식 | [official] | 채택 |
| 68 | Pricing changes for GitHub Actions | <https://resources.github.com/actions/2026-pricing-changes-for-github-actions/> | 공식 | [official] [dated: 2025-12] | 채택 |
| 69 | Dagger Cloud - Observability for Delivery Workflows | <https://dagger.io/cloud/> | 공식 | [official] | 채택 |
| 70 | Introducing Module Catalog & Insights | <https://dagger.io/blog/module-catalog-insights/> | 공식 | [blog] [dated: 2025-05] | 채택 |
| 71 | NixOS Reproducible Builds | <https://reproducible.nixos.org/> | 공식 | [official] | 채택 |
| 72 | Dropping upstream Nix from Determinate Nix Installer | <https://determinate.systems/blog/installer-dropping-upstream> | 블로그 | [blog] [dated: 2025-09] | 채택 |
| 73 | Releases - WebAssembly/WASI | <https://github.com/WebAssembly/WASI/releases> | 공식 | [official] | 채택 |
| 74 | Overview - SpinKube | <https://www.spinkube.dev/docs/overview/> | 공식 | [official] | 채택 |
| 75 | pyroscope.ebpf - Grafana Alloy documentation | <https://grafana.com/docs/alloy/latest/reference/components/pyroscope/pyroscope.ebpf/> | 공식 | [official] | 채택 |
| 76 | Operating System Integrity - Tetragon | <https://tetragon.io/features/operating-system-integrity/> | 공식 | [official] | 채택 |
| 77 | Support Matrix - Talos Linux | <https://www.talos.dev/latest/introduction/support-matrix/> | 공식 | [official] | 채택 |
| 78 | What's New in v2? - Crossplane v2.2 | <https://docs.crossplane.io/latest/whats-new/> | 공식 | [official] | 채택 |
| 79 | Crossplane v2.2 - More Capable, More Reliable, More Observable | <https://blog.crossplane.io/crossplane-v2-2-more-capable-more-reliable-more-observable/amp/> | 공식 | [blog] [dated: 2026-03] | 채택 |
| 80 | Supporting tools and services - Development Containers | <https://containers.dev/supporting.html> | 공식 | [spec] | 채택 |
| 81 | Setting a minimum specification for codespace machines | <https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/configuring-dev-containers/setting-a-minimum-specification-for-codespace-machines> | 공식 | [official] | 채택 |
| 82 | From Standards to Adoption: Introducing the GSF 2025 Annual Report | <https://greensoftware.foundation/articles/introducing-the-gsf-2025-annual-report/> | 공식 | [official] [dated: 2026-01] | 채택 |
| 83 | Real Time Cloud standard story | <https://greensoftware.foundation/stories/real-time-cloud/> | 공식 | [official] [dated: 2025-04] | 채택 |

### 채택한 인사이트

#### Container Orchestration - Kubernetes / Gateway API

- **Gateway API v1.5 성숙도 확장**: 기존 `Gateway`/`HTTPRoute` 안정화에 더해 `TLSRoute` 가 Standard Channel since `v1.5.0` 로 승격. Gateway API 성숙도가 L7 HTTP 중심에서 TLS passthrough/종단 제어까지 확장되며, "Ingress 대체"가 아니라 범용 서비스 네트워킹 API 로 굳어지는 흐름. 적용: infra-guide Networking, infra-audit Kubernetes Networking.

#### IaC Tools

- **Terraform vs OpenTofu split 는 이제 도구 체인 레벨 분리**: HashiCorp 는 Terraform Registry/HCP 에 붙는 `Terraform MCP server` 를 제공해 AI 생성 경로를 자사 생태계에 묶고, OpenTofu 는 별도 공개 Registry 를 운영하며 3,900+ providers / 23,600+ modules 규모를 전면에 내세움. 즉 분기는 라이선스 논쟁을 넘어 레지스트리, AI 보조도구, 배포 경로가 갈라진 상태. 적용: infra-guide IaC 비교, tool-selection 기준.
- **Pulumi AI 는 단순 코드 생성기를 넘는 운영형 IaC 에이전트로 진화**: Pulumi Neo 는 자연어 요청에서 PR 생성, preview, 멀티스텝 운영 작업까지 연결하고 RBAC 범위 내에서 동작. "AI codegen" 보다는 승인 가능한 인프라 작업 자동화 계층으로 보는 편이 정확함. 적용: infra-guide IaC + Platform Engineering + AI automation.

#### CI/CD Patterns

- **GitHub Actions Arm runners 가 표준 러너 선택지로 확대**: 공식 러너 레퍼런스에 `ubuntu-24.04-arm`, `ubuntu-22.04-arm`, `windows-11-arm` 이 명시됨. Arm 지원이 macOS 전용/실험 단계에서 Linux+Windows 전반으로 넓어져 멀티아키텍처 CI 를 표준 YAML 안에서 처리하기 쉬워짐. 적용: infra-guide CI/CD runner 전략.
- **GitHub Actions 성능 개선은 가격 정책까지 포함**: 2026-01-01 부터 hosted runner 가격을 최대 39% 인하한다고 공지. 고성능/대형 runner 사용 장벽이 낮아져, 느린 self-hosted fleet 를 억지 유지하기보다 hosted large/arm runner 로 재평가할 근거가 생김. 적용: infra-audit CI/CD cost/performance.
- **Dagger Cloud 는 "관측" 도구를 넘어 조직 단위 파이프라인 표준화 계층으로 확장**: Cloud 가 워크플로 trace 를 통합 제공하고, Module Catalog & Insights 가 GitHub 저장소를 스캔해 조직 내부 모듈 카탈로그와 사용 현황을 노출. 핵심은 YAML 템플릿 공유보다 "재사용 가능한 delivery module" 을 표준 자산으로 관리하는 모델. 적용: infra-guide CI/CD standardization, platform-team golden paths.

#### Reproducible Builds / Developer Environments

- **Nix/NixOS 채택 신호는 재현성 검증 + 상용 배포판 확장으로 강화**: `reproducible.nixos.org` 는 NixOS 최소 설치 ISO 의 독립 재현 현황을 지속 공개하고, Determinate Nix Installer 는 2025-09 기준 월 거의 100만 설치를 언급하며 자체 배포판 중심 전략으로 전환 중. 커뮤니티 도구에서 공급망/엔터프라이즈 경로로 이동하는 신호. 적용: infra-guide Reproducibility, dev environment 전략.
- **Dev Containers 는 사실상 공통 표준 계층이 되었고 Codespaces 가 이를 실행 계약으로 구체화**: `containers.dev` 가 지원 도구 목록을 공식화했고, GitHub Codespaces 는 `hostRequirements` 로 CPU/메모리/스토리지를 `devcontainer.json` 에 명시하게 함. 개발환경 정의가 "에디터 설정"이 아니라 저장소 수준 실행 계약으로 이동. 적용: infra-guide Developer Experience, repo bootstrap.

#### WebAssembly / Emerging Runtime

- **서버사이드 Wasm 은 "Preview 2 실험"에서 "WASI 0.2.x 릴리스 라인"으로 정착**: WebAssembly/WASI 저장소는 `v0.2.x` 호환 릴리스를 계속 발행 중이며, Preview 2 가 사실상 유지보수되는 표준 인터페이스 계층으로 운영되고 있음. 즉 이제 논점은 "Preview 2 가 오나?"가 아니라 "어떤 런타임/플랫폼이 0.2 생태계를 안정적으로 구현하나?"에 가까움. 적용: infra-guide Runtime alternatives.
- **SpinKube 는 Wasm on Kubernetes 의 운영 모델을 구체화**: Spin Operator + runtime class manager + runwasi 기반으로 CRD, DNS, probes, autoscaling(HPA/KEDA), metrics 를 K8s 기본기와 연결. Wasm 이 컨테이너 대체물이 아니라 K8s 배포 표면에 편입되는 방식이 명확해짐. 적용: infra-guide Kubernetes workload options, edge/serverless 비교.

#### Security / Observability

- **eBPF 의 무게중심이 네트워킹 밖으로 확실히 이동**: Grafana Alloy 의 `pyroscope.ebpf` 는 호스트/컨테이너 연속 프로파일링을 제공하고, Tetragon 은 eBPF subsystem activity, kernel module load/unload, privilege/capability 사용을 감시함. eBPF 는 이제 CNI 가 아니라 profiling + runtime security + kernel debugging 기반 기술로 봐야 함. 적용: infra-guide Observability/Security, infra-audit Runtime detection.

#### Kubernetes Platform / Node OS

- **Talos Linux 는 immutable Kubernetes node OS 패턴을 Arm/SecureBoot 포함 운영 경로로 밀고 있음**: 최신 support matrix 기준 Talos 1.11 은 Kubernetes 1.34/1.33 과 amd64/arm64 를 지원하고 bare metal 에서 SecureBoot 경로까지 제공. 범용 Linux hardening 보다 API-managed 전용 node OS 로의 전환 논의가 실전 레벨에 있음. 적용: infra-guide Kubernetes node OS, edge/bare-metal 운영.
- **Crossplane v2 는 인프라 합성을 넘어 control plane composition 으로 확장**: v2 에서 XR/MR namespaced 기본값, 임의 Kubernetes resource composition, claims 제거가 이뤄졌고, v2.2 는 Operations 와 pipeline inspector 를 추가. Crossplane 을 "클라우드 리소스 프로비저너"로만 보면 부족하고, 플랫폼 팀의 선언적 API/운영 워크플로 엔진으로 봐야 함. 적용: infra-guide Platform Engineering, infra-guide IaC/Kubernetes control plane.

#### Sustainability / FinOps Adjacent

- **Green Software Foundation 흐름은 캠페인보다 표준화 단계**: 2025 연차보고서 기준 Real Time Energy and Carbon Standard for Cloud Providers (RTC), SOFT, SCI for AI 등 5개 핵심 프로젝트가 ratified 되었고, RTC 는 AWS/Azure/GCP 가 공통 포맷의 실시간 에너지/탄소 데이터를 제공하도록 요구하는 규격으로 정리됨. 클라우드 탄소 추적은 "월별 대시보드"에서 "표준화된 실시간 데이터 계약"으로 넘어가는 중. 적용: infra-guide Sustainability, cost/carbon observability.

### 신규 스킬 갭 분석

| 제안 스킬 | 아키타입 | 근거 | 우선순위 | 상태 |
| --------- | -------- | ---- | -------- | ---- |
| `infra-devenv` | 코드 스캐폴딩 | Dev Containers + Codespaces + Nix 기반 재현 가능한 개발환경 부트스트랩 | 중간 | backlog |
| `infra-runtime-alt` | 가이드 | WASI 0.2 + SpinKube + Talos + eBPF 기반 런타임 대안 비교 | 중간 | backlog |
| `infra-carbon` | 가이드 | RTC + SOFT + SCI for AI 기반 탄소/비용 관측 프레임워크 | 낮음 | backlog |

### 폐기 사유

없음.
