---
name: infra-audit
description: >
  인프라 설정(Docker, CI/CD, K8s, Terraform 등)을 원칙 기준으로 체계적으로 감사한다.
  카테고리별 PASS/FAIL 판정과 근거를 포함한 리포트를 생성한다.
  infra-reviewer 에이전트를 Agent 도구로 호출하여 독립 평가한다.
  "인프라 감사", "Docker 검수", "CI 보안 검사", "infra audit" 같은 요청 시 트리거.
  백엔드 코드 품질 검사에는 트리거하지 않는다 — backend-kit 사용.
argument-hint: "<target-path>"
user-invocable: true
---

# Gotchas

1. **백엔드 코드 평가 금지** — 앱 로직은 평가하지 마라. 인프라 설정/구성 원칙만 판정.
2. **벤더 특정 기능 FAIL 금지** — AWS-only 기능이 없다고 FAIL 주지 마라. 범용 원칙만 기준.
3. **보안 검사 생략 금지** — "내부용"이어도 non-root, 시크릿 관리, OIDC, TLS는 반드시 검사.
4. **프로덕션 vs 개발 구분** — 개발용 docker-compose에 리소스 제한 미설정은 FAIL이 아니다. 프로덕션 설정만 엄격 적용.
5. **PASS/FAIL 근거에 파일:라인 필수** — "Container FAIL — non-root 미설정"만으로는 수정 위치를 알 수 없다. `Dockerfile:15`처럼 구체적 위치를 포함해야 한다.
6. **N/A 카테고리도 이유를 명시하라** — Kubernetes를 N/A로 표시할 때 "프로젝트에 K8s 매니페스트가 없음"처럼 근거를 함께 적어라. 단순히 N/A만 표기하면 검사를 빠뜨린 것인지 실제로 해당 없는 것인지 구분이 불가능하다.
7. **CI 워크플로우의 시크릿 처리 감사 필수** — GitHub Actions/GitLab CI에서 `${{ secrets.XXX }}`가 아니라 평문으로 시크릿을 노출하는 경우가 많다. 환경변수, 파이프라인 설정에서 시크릿이 평문 노출되는지 반드시 확인한다.
8. **이미지 태그 `latest` 사용 FAIL** — 프로덕션 Dockerfile/compose에서 `FROM node:latest`, `image: postgres:latest`처럼 `latest` 태그를 사용하면 재현 불가능한 빌드가 된다. 반드시 구체적 버전 태그(`postgres:16-alpine`)를 사용하라.
9. **Binary Decidability Pre-Check (agent-design-guide §3.5 대응)** — 각 카테고리를 평가하기 전에 "이 기준은 설정 파일에서 객관적으로 PASS/FAIL 판정 가능한가?"를 먼저 자문하라. "보안이 충분해 보인다"처럼 주관 해석 여지가 남는 기준은 **카테고리 평가 시작 시점에** 근거 제약(파일:라인 + 출처 URL)을 추가하여 이진 판정으로 재정식화한 뒤 평가한다. 예: "K8s 네임스페이스 보안이 좋은지"가 아니라 "네임스페이스에 `pod-security.kubernetes.io/enforce=baseline` 라벨이 있는지 (Kubernetes PSA)"로 좁힌다.
10. **Rule-by-Rule Audit 프로토콜 (skill-design-guide §3.6 대응)** — `audit-criteria.md` 10 카테고리 × N 체크항목을 한 번에 묶어 "대체로 PASS/FAIL" 로 리포트하지 말고, 각 체크항목 단위로 개별 판정과 근거를 생성하라. 묶음 판정은 PASS 세부가 가려지고 FAIL 누락 추적이 불가능해진다. 리포트 표의 각 row 는 한 체크항목에 대응한다.
11. **미검증 항목 마커 프로토콜** — 런타임 환경/외부 시스템 접근 불가(예: production K8s 클러스터 kubectl 접근 · 실제 Cosign 서명 검증 · terraform state 파일 열람)로 L3 검증이 불가능한 항목은 **조용히 PASS 처리하지 말고** `[미검증:ENV]` 태그를 붙이고 근거에 이유를 기술하라 (예: `[미검증:ENV] production cluster kubectl 접근 불가 — manifest 정적 리뷰만 수행`). 마커 의미·4 분기·카운터 분리(`invalid_evidence` / `env_gaps`)·임계값·커버리지 게이트는 `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol 이 SSOT 이며, `infra-kit/agents/infra-reviewer.md` §9 가 그 복제본이다. **이 스킬에서 임계값이나 분류어를 다시 정의하지 마라.**

12. **도구·규칙 소스 부재를 "위반 0" 으로 집계하지 마라** — 인프라 감사는 검사 도구가 없는 환경이 흔하다(`hadolint` · `actionlint` · `kubeconform` · `conftest` · `cosign` · `trivy` 미설치, kubectl/레지스트리 접근 불가). **검사하지 못한 것과 검사해서 위반이 없는 것은 다르다.** 도구가 없어 돌리지 못한 rule 은 PASS 도 N/A 도 아니고 `[미검증]` 이다. 같은 원칙이 규칙 소스에도 적용된다 — `../../references/audit-criteria.md` 를 읽지 못했다면 그 카테고리는 검사하지 않은 것이므로 `[미검증] TOOL_OR_ENV_MISSING: audit-criteria.md 소스 부재 — 미검사` 로 명시하고 위반 0 으로 보고하지 마라. 빈 결과를 통과로 읽는 것이 이 마찰의 실제 사고 형태다. 상태어 5 종과 머리말 4 카운터는 `../../references/gate-result-taxonomy.md` 가 SSOT 다 — Step 3a 가 그것을 소비한다.

# Process

## Step 1: 대상 범위 결정

- 파일 경로 → 해당 파일만
- 디렉토리 경로 → 하위 인프라 관련 파일 전체 (Dockerfile, *.yml, *.yaml, *.tf, *.hcl)
- 미지정 → 최근 변경된 인프라 파일 (git diff 기준)

## Step 2: infra-reviewer 에이전트 호출

- subagent_type: infra-reviewer
- prompt: "다음 파일을 인프라 원칙 기준으로 평가하라: [대상 파일 목록]"

## Step 3: 리포트 생성 (Rule-by-Rule 표)

### Step 3a: 감사 범위 머리말 (표보다 먼저 · Gotcha 12)

표를 쓰기 전에 아래 머리말을 그대로 출력한다. 포맷 SSOT 는 `../../references/gate-result-taxonomy.md` §머리말 4 카운터다. 도구 유무는 추측하지 말고 `command -v <tool>` 로 확인한 결과만 적는다. **이 머리말이 없으면 리포트의 "위반 0" 은 해석 불가다 — 분모를 모르기 때문이다.**

```text
대상 인프라 파일 수: <n>  (<탐색 경로 — Step 1 이 확정한 범위>)
규칙 소스 수       : <n>  [<실제로 읽은 파일 절대경로 나열>]
사용 가능 도구 수  : <n>  [<command -v 로 확인된 도구 — 없으면 "없음">]
미설치 도구 수     : <n>  [<확인 실패한 도구 — 해당 rule 은 전부 [미검증:ENV]>]
[미검증] 규칙 소스 : <읽지 못한 소스 나열 — 없으면 "없음">
```

**대상 인프라 파일 수가 0 이면** 표를 만들지 말고 `SKIP_NO_TARGET` 으로 종결한다 (감사 대상 없음). 이것을 "위반 0 · APPROVE" 로 보고하지 마라 — 검사한 적 없는 레포가 green 으로 기록된다.

### Step 3b: Rule-by-Rule 표

카테고리 순서는 `../../references/audit-criteria.md` 의 `^## ` 섹션 순서와 **정확히** 일치시킨다 (총 10 카테고리 · 스킬 디렉토리 기준 상대 경로를 쓰지 마라 — 그러면 stale 사본을 읽는다). 각 row 는 **하나의 체크항목(rule)** 에 대응하며, 카테고리 단위로 묶지 않고 개별 판정·근거·출처를 생성한다 (Gotcha 10 참조). 표 자리표시자(`...`) 금지.

판정 열에는 `PASS` / `FAIL` / `N/A`(카테고리 미해당 · 사유 필수) / `[미검증:ENV]`(도구·접근 부재) 중 하나만 쓴다 — 분기 정의는 `../../references/gate-result-taxonomy.md`.

| # | 카테고리 | 체크항목 | 판정 | 근거(파일:라인) | 출처 URL |
|---|----------|---------|------|-----------------|----------|
| 1 | Container | 멀티스테이지 빌드 | PASS/FAIL | `Dockerfile:1-30` 에 `COPY --from=builder` 확인 | [Docker best practices](https://docs.docker.com/build/building/best-practices/) |
| 2 | Container | non-root 실행 | PASS/FAIL | `Dockerfile:25` `USER 1001:1001` | [Docker USER](https://docs.docker.com/reference/dockerfile/#user) |
| 3 | Container | 이미지 태그 핀닝 | PASS/FAIL | `docker-compose.yml:12` `postgres:16-alpine` (digest 권장) | [OCI Image spec](https://github.com/opencontainers/image-spec) |
| 4 | CI/CD | OIDC 인증 (장기 키 부재) | PASS/FAIL | `.github/workflows/deploy.yml:40` `id-token: write` | [GitHub Actions OIDC](https://docs.github.com/en/actions/concepts/security/openid-connect) |
| 5 | CI/CD | 원격 `uses:` SHA 핀닝 (YAML 파서로 `jobs.*.uses` + `jobs.*.steps[].uses` 둘 다 열거) | PASS/FAIL | `.github/workflows/deploy.yml` 원격 참조 전부 40 자 SHA · 로컬 `./` 만 면제 | [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use) |
| 6 | CI/CD | Dependabot — 탐지된 생태계만 등록 | PASS/FAIL | `.github/dependabot.yml:1` `github-actions` + 실제 lockfile/manifest 있는 생태계만 | [Dependabot options reference](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference) |
| 7 | CI/CD | SLSA provenance 생성+검증 | PASS/FAIL/N/A | `.github/workflows/release.yml` in-toto attestation + `verify-attestation` (릴리스 워크플로가 있을 때만 게이트) | [SLSA provenance](https://slsa.dev/provenance) |
| 8 | Kubernetes | Pod Security Admission 라벨 | PASS/FAIL/N/A | `k8s/namespace.yaml:5` `pod-security.kubernetes.io/enforce=baseline` | [Kubernetes PSA](https://kubernetes.io/docs/concepts/security/pod-security-admission/) |
| 9 | Kubernetes | 리소스 requests/limits | PASS/FAIL/N/A | `k8s/deployment.yaml:30` resources 블록 확인 | [Kubernetes PSA](https://kubernetes.io/docs/concepts/security/pod-security-admission/) |
| 10 | Kubernetes | Gateway API vs Ingress | PASS/FAIL/N/A | `k8s/gateway.yaml:1` `gateway.networking.k8s.io/v1` 사용 | [Gateway API v1.4](https://kubernetes.io/blog/2025/11/06/gateway-api-v1-4/) |
| 11 | IaC | Ephemeral values for secrets | PASS/FAIL/N/A | `infra/vault.tf:15` `ephemeral` 블록 또는 write-only 인수 사용 | [Terraform ephemeral](https://developer.hashicorp.com/terraform/language/ephemeral) |
| 12 | IaC | State 암호화 | PASS/FAIL/N/A | `infra/backend.tf:1` OpenTofu native state encryption 또는 KMS SSE | [OpenTofu state encryption](https://opentofu.org/docs/v1.11/language/state/encryption/) |
| 13 | IaC | `terraform test` 존재 | PASS/FAIL/N/A | `tests/module.tftest.hcl:1` run 블록 | [Terraform tests](https://developer.hashicorp.com/terraform/language/tests) |
| 14 | Security | TLS 1.2+ 외부 엔드포인트 | PASS/FAIL | `k8s/ingress.yaml:20` tls 블록 + cert-manager ClusterIssuer | [cert-manager](https://cert-manager.io/docs/) |
| 15 | Security | 시크릿 로테이션 | PASS/FAIL | `infra/secrets.tf:10` auto-rotation lifecycle 또는 Vault 동적 시크릿 | OWASP Secrets |
| 16 | Observability | signal 별 수집 상태 (traces·metrics·logs 를 **각각** 판정 — 한 줄로 "3 신호 통합" 묶지 마라) | PASS/FAIL | `otel-collector.yaml:1` 각 pipeline 존재 + `service.name` semconv | [OpenTelemetry spec status](https://opentelemetry.io/docs/specs/status/) |
| 17 | Deployment | GitOps source of truth | PASS/FAIL | `argo/application.yaml:1` Argo CD 3.x / Flux v2.8+ sync | [Argo CD 3.0 Upgrade](https://argo-cd.readthedocs.io/en/latest/operator-manual/upgrading/2.14-3.0/) |
| 18 | Backup & DR | K8s 백업 도구 (Velero) | PASS/FAIL/N/A | `k8s/velero-schedule.yaml:1` 스케줄 백업 + 보존 정책 | Velero docs |
| 19 | Cost Optimization / FinOps | 리소스 태깅 전략 | PASS/FAIL/N/A | `infra/variables.tf:1` `default_tags` 블록(team/env/service/cost-center) | [State of FinOps 2026](https://data.finops.org/) |
| 20 | Supply Chain | Cosign 이미지 서명 | PASS/FAIL/N/A | `.github/workflows/release.yml:80` `cosign sign` + `cosign verify` (릴리스 산출물이 있을 때만 게이트) | [Sigstore Cosign](https://docs.sigstore.dev/cosign/verifying/attestation/) |
| 21 | Supply Chain | SBOM (CycloneDX/SPDX) | PASS/FAIL/N/A | `.github/workflows/release.yml:50` Trivy/Syft 산출물 저장 | [CycloneDX ECMA-424](https://cyclonedx.org/) |

위 표는 대표 rule 예시이며, 실제 리포트는 `../../references/audit-criteria.md` 의 모든 기준 rule 을 빠짐없이 열거해야 한다 (Rule-by-Rule Audit · Gotcha 10). 해당 없는 카테고리(K8s 미사용, EU 비대상 등)는 N/A 로 표시하고 판정에서 제외한다.

**릴리스 산출물이 없는 레포에 Supply Chain 을 FAIL 로 강제하지 마라.** SLSA provenance · Cosign 서명 · SBOM 은 배포·릴리스 워크플로가 실재할 때 게이트로 승격하고, 그 전에는 N/A(사유: 릴리스 워크플로 부재) 로 둔다. 마찬가지로 K8s 매니페스트가 없는 레포에 Gateway API·PSA 를 FAIL 로 주지 마라 — 카테고리 미해당이다.

## Step 4: 최종 판정

판정은 `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol 조항 3 과 §카운팅 및 자동 REJECT 임계의 **카운터 분리**를 그대로 적용한다 (임계값·분류어 재정의 금지 · Gotcha 11).

먼저 미검증을 두 카운터로 나눈다:

- `invalid_evidence` — 4 요건 미충족 도구부재 주장 + 증거 무효(공허한 출력·0 매치를 "위반 없음" 으로 읽음). 인프라에서는 `cosign verify` 가 attestation 0 건을 돌려준 것을 PASS 로 읽는 경우가 전형이다.
- `env_gaps` — 4 요건을 충족한 정당한 `[미검증:ENV]`. 자동 REJECT 카운터에 **합산하지 않는다.**

verdict 는 아래 순서로 확정하고 **위에서 성립하는 첫 항에서 멈춘다**:

1. 감사 전제 붕괴(대상 0 건 · 규칙 소스 전부 로드 실패) → **BLOCKED** (`SKIP_NO_TARGET` 또는 소스 부재 사유 명시)
2. FAIL ≥ 1 → **REJECT** — 각 FAIL 에 구체적 개선 액션(파일:라인 + 권장 변경 + 출처) 을 제시한다
3. `invalid_evidence` ≥ 2 → **REJECT** (개별 FAIL 이 0 건이어도)
4. `verified_coverage = (rule 총수 − env_gaps) / rule 총수` 가 **0.60 미만** → **BLOCKED** (`insufficient_verified_coverage`). 원인이 구현이 아니라 환경이므로 REJECT 로 기록하지 않는다. 복구책은 각 `env_gaps` 항목의 **재검증 명령**을 실행한 뒤 재감사다
5. `invalid_evidence` == 1 · FAIL 0 → **CONDITIONAL APPROVE** (이 조합에서만 유효하다)
6. 그 외 → **APPROVE** (`env_gaps: N` 을 본문에 노출)

리포트 말미에 아래를 집계한다 (canonical 조항 5):

```text
## Unverifiable Summary
- invalid_evidence: K   [체크항목 ID, 분기(B2|C), 사유, 시도한 fallback 단계]
- env_gaps: M           [체크항목 ID, 1차 도구 시도, fallback 시도, 실패 로그, 통제 불가 사유 + 재검증 명령]
- verified_coverage: (rule 총수 - env_gaps) / rule 총수 = 0.xx (임계 0.60)
```

같은 체크항목이 **2 회 연속 감사에서 `env_gaps`** 면 그것은 환경 문제가 아니라 감사 기준의 검증 경로 미기재다 — `invalid_evidence` 쪽으로 이관하고 `audit-criteria.md` 개선 제안으로 올린다.

# References

- ../../references/audit-criteria.md — 카테고리별 PASS/FAIL 체크리스트 (10 카테고리 · 순서 SSOT)
- ../../references/gate-result-taxonomy.md — 결과 상태 5 종 · 머리말 4 카운터 (SSOT)
- `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol — 마커·카운터 분리·임계값 (상위 SSOT · 인용 전용)
