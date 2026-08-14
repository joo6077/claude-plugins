---
feature: "카이젠 Phase 8 — infra-kit 게이트 결과 상태 taxonomy(I1) + YAML 파서 핀닝·Dependabot(I2) + Phase 3 canonical 전파 + 사실 정정 4종"
created: "2026-08-13 14:35"
complexity: "복잡"
conditions: 23
slug: kaizen-phase8-infra-gate-taxonomy
status: done
owner_session: df1b3e15-30b3-4825-a3c4-4ac44c686e94
conditions_digest: sha256:31e7986a1a812bca
locked_at: "2026-08-13 14:35"
---

## 배경

`.harness/.meta/evidence/phase8.md` 가 이번 Phase 의 **유일한 외부 근거**다. 외부 조회 0 회.

이 Phase 는 `/insights` 2026-08-13 §0 에 직접 신호가 없다(low-signal). 따라서 새 원칙을 만들지
않고 **직전 사이클이 고친 버그의 근본원인 하나**를 구조로 승격하는 데 집중한다.

**I1 — "도구 부재 = 위반 0" 구조.** 2026-07-27 Phase 8 은 `infra-test` 가 생성해주는 CI 검증
스크립트에서 실제 버그 3 건(grep 앵커 누락 · WARN 후 exit 0 · 빈 glob 오보)을 고쳤다. 셋의 공통
뿌리는 **검사 결과에 "검사를 수행하지 못했다" 라는 상태가 없다**는 것이다. 상태가 없으면 도구
부재도, 대상 부재도, 실행 실패도 전부 "위반 0" 으로 접힌다. 문장을 또 추가하는 대신 **상태 taxonomy
를 아티팩트(E2)로 고정하고 exit code 로 강제(E3)** 한다.

**정합 대상 2 곳.** 어휘를 새로 만들지 않는다.

- 이번 사이클 Phase 3 이 `harness/docs/guides/qa-evaluation-guide.md` 에 **4 분기 + 카운터 분리**
  (`UNVERIFIED_ENV` / `UNVERIFIED_INVALID_EVIDENCE` · `env_gaps` · `verified_coverage` 0.60 게이트)
  를 신설했고, 그 문서 §전파 목록이 `infra-reviewer` 를 **미전파 상태**로 명시한다.
- 이번 사이클 Phase 4 가 `harness/evals/gate-exit-codes.md` 를 **exit code SSOT** 로 신설했다
  (0 pass / 1 policy_violation / 2 usage_or_infra_error / 3 no_data_not_run). infra 상태어는 이
  4 값에 **매핑만** 하고 숫자를 재정의하지 않는다.

**I2 — 핀닝 검사가 grep 이라 못 잡는다 (실측).** 현행 `infra-test` 스켈레톤의 grep 오라클을 이
레포 워크플로에 그대로 돌리면 **미핀닝 6 건 전부를 0 건으로 보고**한다 (사전 측정 출력은 아래 GAP
표 I2 행). 원인은 `grep -vE 'uses:[[:space:]]*actions/'` 가 GitHub-owned 액션을 **정책 질문으로
남기지 않고 조용히 면제**하기 때문이다. evidence 는 "로컬 `./` 만 제외하고 원격은 full SHA 기본
요구, GitHub-owned 예외 여부는 정책 질문으로 남겨라" 를 권고한다.

**범위 주의.** 이 레포의 `.github/` · `scripts/` 는 Phase 4 소관이며 **고치지 않는다.** 여기서
고치는 것은 infra-kit 이 **생성해주는 산출물의 품질**이다. 이 레포 워크플로는 오라클 fixture 로만
읽는다.

## 리서치 소스 (evidence 파일 한정 — 외부 조회 0 회)

- `.harness/.meta/evidence/phase8.md` §1~§4 — I1/I2/I3 관찰 사실 · 권장 상태 5 종 · **넣지 말 것**
  5 항목 · 트레이드오프 · 열린 질문. 인용 URL 8 종:
  `conftest.dev/options` · `docs.github.com/.../secure-use` ·
  `docs.github.com/.../openid-connect` · `docs.github.com/.../dependabot-options-reference` ·
  `brendangregg.com/usemethod.html` · `opentelemetry.io/docs/specs/status/` ·
  `kubernetes.io/docs/concepts/security/pod-security-admission/` ·
  `developer.hashicorp.com/terraform/language/ephemeral` ·
  `opentofu.org/docs/v1.11/language/state/encryption/` · `slsa.dev/provenance` ·
  `docs.sigstore.dev/cosign/verifying/attestation/`
- Phase 3 산출물 `harness/docs/guides/qa-evaluation-guide.md` — §증거 분류 triage(4 분기) ·
  §Canonical Unverified-Evidence Protocol(2026-08-13 개정) · §Canonical User-Reported Failure
  Protocol · §전파 대기 목록(infra-reviewer 명시)
- Phase 4 산출물 `harness/evals/gate-exit-codes.md` — exit code 4 값 SSOT + 우선순위 규칙
- `harness/references/contract-schema.md` v5.3 — 본 계약의 포맷 SSOT
- `.claude/kaizen-input/insights-report.md` — 직전 사이클 흡수분 표(재승격 금지)
- `docs/kaizen/changelog.md` `[2026-07-27]` Phase 8 항목 — 직전 사이클이 고친 버그 3 건

## GAP 분석 (전부 실측 · 명령 출력 기준)

| # | 갭 | 실측 근거 (사전 측정 출력) | 처리 |
| --- | --- | --- | --- |
| I1 | 게이트 결과 상태 taxonomy 부재 | `infra-test` 스켈레톤에 `SKIP_NO_TARGET` · `EXECUTION_ERROR` 문자열 0 건. 대상 0 건일 때 `exit 0` 으로 PASS 와 동일 | `references/gate-result-taxonomy.md` 신설(E2) + 스켈레톤 exit 매핑(E3) |
| I1b | 게이트 머리말에 대상 수 없음 | `infra-audit` Step 3a 는 4 줄이나 **대상 수**가 없어 "위반 0" 의 분모를 알 수 없다 | 4 카운터로 교체 (대상·규칙 소스·도구·미설치 도구) |
| I2 | 핀닝 검사 grep 오탐 | 현행 grep 오라클을 이 레포에 실행 → `(0 건 — 미핀닝 없음으로 보고됨)`. 실제 `uses:` 6 건 전부 `@v7` 태그 | YAML 파서(`jobs.*.uses` + `jobs.*.steps[].uses`)로 교체, first-party 면제는 opt-in |
| I2b | Dependabot 조항 0 건 | `grep -ri dependabot infra-kit/` → 0 건 | init-checklist · infra-init · audit-criteria 3 표면에 신설 (실제 manifest 있는 생태계만) |
| P3 | Phase 3 canonical 미전파 | `infra-reviewer.md` 에 `UNVERIFIED_ENV` 0 건 · `env_gaps` 0 건 · `verified_coverage` 0 건. §9 는 구 3 분기/단일 임계 | 개정 5 조항 복제 + 도메인 매핑 갱신 |
| F1 | 카테고리 순서 드리프트 | `audit-criteria.md` `^## ` 순서 6~10 = Observability·Deployment·Backup&DR·Cost·Supply Chain / `infra-reviewer` 6~10 = Supply Chain·Backup&DR·Deployment·Observability·Cost — **5 개 불일치** | reviewer·audit 예시표를 SSOT 순서로 정렬 |
| F2 | stale 참조 경로 | `infra-audit/SKILL.md` 2 곳이 백틱 `references/audit-criteria.md` — 스킬 디렉토리 기준으로는 Apr-04 **7 카테고리 stale 사본**을 가리킨다 (SSOT 는 10 카테고리) | `../../references/` 로 명시 |
| F3 | OTel status 과잉 단정 | `docs/infra/operations/observability.md` 에 `profiles` 0 건 — signal 별 status 구분 없음 | signal 별 status 기재 + spec status URL |
| I3 | 환경 요인 선배제 절차 부재 | `observability.md` 에 USE Method · saturation 0 건 | 원칙 1 개 신설 (USE 출처 확정 · RED 는 출처 미확인 명시) |

**넣지 않는 것 (evidence §2 경계 준수)** — K8s/Gateway API/Karpenter/DRA/service mesh/IDP/FinOps/
sustainability 를 신호 없는 레포의 새 FAIL 규칙으로 강제하지 않는다. SLSA/Cosign/SBOM 을 릴리스
산출물 없는 레포의 필수 FAIL 로 만들지 않는다. `pull_request_target` 을 기본값으로 넣지 않는다.
SARIF 는 OASIS 원문 미확인이므로 **이번 사이클 미반영**으로 남긴다.

## 범위 경계

수정 허용: `infra-kit/skills/*/SKILL.md` · `infra-kit/agents/*.md` · `infra-kit/references/` ·
`docs/infra/` · 본 계약 파일.

수정 금지 (읽기만): 이 레포의 `.github/**` · `scripts/**` (Phase 4 소관) ·
`harness/**` (Phase 1~4 소관) · `infra-kit/README.md` · `infra-kit/skills/*/references/**`
(스킬 로컬 stale 사본 — 3 개 킷 공통 구조 이슈라 Final 소관으로 보고만 한다).

## 회귀 게이트

- `python3 scripts/validate-plugin.py infra-kit` 가 8 카테고리 OK 를 유지한다.
- 스켈레톤 fixture 8 종의 exit code 가 설계값과 일치한다 (아래 DG-03).
- 임계값(`[미검증]` 1/2 · `verified_coverage` 0.60) · exit 숫자(0/1/2/3) 를 infra-kit 이 **자체
  정의하지 않는다** — 두 SSOT 인용만 한다.

## Skill

- [ ] SK-01: `infra-kit/references/gate-result-taxonomy.md` 가 신설되고 상태 5 종
      `PASS`, `VIOLATION`, `SKIP_NO_TARGET`, `TOOL_OR_ENV_MISSING`, `EXECUTION_ERROR` 를 각각
      정의한다 [exact, enumerated]
      (측정: 5 토큰 각각 `grep -c` 결과 >= 1)
- [ ] SK-02: 같은 파일이 exit 숫자를 자체 정의하지 않고 `harness/evals/gate-exit-codes.md` 와
      `harness/docs/guides/qa-evaluation-guide.md` 두 SSOT 를 인용한다 [exact, enumerated]
      (측정: 두 경로 문자열 각각 `grep -c` >= 1)
- [ ] SK-03: `infra-kit/skills/infra-test/SKILL.md` 스켈레톤이 YAML 파서 기반이며
      `jobs.{jid}.uses` 와 `jobs.{jid}.steps[{i}].uses` 를 **둘 다** 열거한다 [exact, enumerated]
      (측정: `yaml.safe_load` · `jobs.{jid}.uses` · `steps[{i}].uses` 3 토큰 각각 `grep -cF` >= 1)
- [ ] SK-04: 같은 스켈레톤이 검사 시작 전 4 카운터를 출력한다 [exact, enumerated]
      (측정: `대상 워크플로 수`, `규칙 소스 수`, `사용 가능 도구 수`, `미설치 도구 수`
      4 문자열 각각 `grep -cF` >= 1)
- [ ] SK-05: Dependabot 조항이 `infra-kit/references/init-checklist.md`,
      `infra-kit/skills/infra-init/SKILL.md`, `infra-kit/references/audit-criteria.md`
      3 파일에 각각 존재하고, 세 곳 모두 `lockfile` 또는 `manifest` 제한 낱말을 포함한다
      [exact, enumerated]
      (측정: 3 파일 각각 `grep -ci dependabot` >= 1 이고 `grep -ciE 'lockfile|manifest'` >= 1)
- [ ] SK-06: `infra-kit/skills/infra-audit/SKILL.md` Step 3a 머리말이 4 카운터로 확장되어
      **대상 수**를 포함한다 [exact]
      (측정: Step 3a 블록에 `대상` 을 포함한 머리말 줄 >= 1)

## Error

- [ ] ER-01: 핵심 도구 부재가 PASS 나 "위반 0" 으로 집계되지 않는다 [goal]
      (측정: `PATH` 에서 `grep` 을 제거한 fixture F 실행 → 출력에 `EXECUTION_ERROR` 포함 +
      `VIOLATION=` 줄 미출력 + exit 2 ·
      음성 대조: 핵심 도구 사전 검사 블록을 제거하면 같은 fixture 가 `checkout 스텝 없음`
      VIOLATION 을 오보하고 exit 1 이 된다 — 실제로 관측한 회귀다)
- [ ] ER-02: 검사 대상 0 건이 PASS 와 구분된다 [goal]
      (측정: 워크플로 0 개 fixture B 실행 → `SKIP_NO_TARGET` 출력 + exit 3 ·
      음성 대조: `${#workflows[@]}` 가드를 제거하면 exit 0 으로 PASS 와 동일해진다)
- [ ] ER-03: 선택 도구 부재가 `[미검증]` 으로 집계되고 실행 불완전으로 종료한다 [goal]
      (측정: `python3` 만 제거한 fixture G 실행 → `[미검증] TOOL_OR_ENV_MISSING` 출력 +
      `[미검증]=1` 집계 + exit 2)

## Architecture

- [ ] AR-01: `infra-kit/agents/infra-reviewer.md` §9 가 Phase 3 개정 canonical 을 복제한다
      [exact, enumerated]
      (측정: `UNVERIFIED_ENV`, `UNVERIFIED_INVALID_EVIDENCE`, `env_gaps`, `verified_coverage`
      4 토큰 각각 `grep -c` >= 1)
- [ ] AR-02: `infra-kit/skills/infra-audit/SKILL.md` Step 4 verdict 가 카운터 분리를 반영한다
      [exact]
      (측정: `invalid_evidence` · `env_gaps` · `insufficient_verified_coverage` 3 토큰 각각
      `grep -c` >= 1 이고, 구 문구 `` `[미검증]` 2 건 이상 `` 이 `grep -cF` 결과 0)
- [ ] AR-03: `infra-reviewer` 평가 카테고리 목록이 `audit-criteria.md` `^## ` 순서와 정확히
      일치한다 [exact]
      (측정: 아래 두 목록의 `diff` 가 무출력 ·
      `grep '^## ' infra-kit/references/audit-criteria.md | grep -v '판정 규칙' | sed 's/^## //'`
      vs reviewer §평가 카테고리 번호 목록의 카테고리명)
- [ ] AR-04: `infra-audit` 이 stale 스킬 로컬 사본을 가리키지 않는다 [exact]
      (측정: `grep -cF '`references/audit-criteria.md`' infra-kit/skills/infra-audit/SKILL.md`
      결과 0 · 사전값 2)
- [ ] AR-05: OTel signal 별 status 가 기재된다 [exact, enumerated]
      (측정: `docs/infra/operations/observability.md` 에 `traces`, `metrics`, `logs`,
      `profiles`, `development`, `opentelemetry.io/docs/specs/status/` 6 토큰 각각
      `grep -c` >= 1)
- [ ] AR-06: `docs/infra/operations/observability.md` 에 환경 요인 선배제 원칙이 신설된다
      [exact]
      (측정: `brendangregg.com/usemethod.html` `grep -c` >= 1 이고 `saturation` `grep -c` >= 1)

## Anti-patterns

- [ ] AP-03: 이번 스프린트가 추가·수정한 마크다운에 bare code fence 가 없다
      (측정: `python3 scripts/validate-plugin.py infra-kit` V6 `0 bare`)
- [ ] AP-04: 수정한 SKILL.md 4 종 + agents 1 종의 frontmatter `name` 필드가 보존된다
      (측정: `python3 scripts/validate-plugin.py infra-kit` V1 `4 skills + 1 agent — OK`)

## Reusability

- [ ] RE-01: 상태 5 종의 **정의**가 infra-kit 안에서 `references/gate-result-taxonomy.md`
      1 파일에만 존재하고, 소비 표면 3 종(`infra-test` · `infra-audit` · `infra-reviewer`)은
      그 파일을 경로로 참조만 한다 [exact, enumerated]
      (측정: 소비 표면 3 파일 각각 `grep -cF 'gate-result-taxonomy.md'` >= 1)
- [ ] RE-02: infra-kit 이 `[미검증]` 임계값과 커버리지 임계를 재정의하지 않는다 [exact]
      (측정: infra-kit 하위에서 `verified_coverage` 를 포함한 줄 중 `0.60` 을 함께 쓰는 줄이
      전부 `qa-evaluation-guide` 인용 문맥임을 육안 확인 + `임계값을 다시 정의하지 않는다`
      류 인용 선언이 `infra-reviewer.md` 에 `grep -c` >= 1)

## Diagnostics

- [ ] DG-01: `python3 scripts/validate-plugin.py infra-kit` 가 exit 0 · `1 plugins, 1 OK`
- [ ] DG-02: 스켈레톤 스크립트가 `bash -n` 과 `shellcheck`(기본 severity) 를 모두 통과한다
      (측정: SKILL.md 의 스켈레톤을 파일로 추출해 `bash -n` rc 0 · `shellcheck` rc 0)
- [ ] DG-03: 스켈레톤이 fixture 8 종에서 설계 exit code 를 낸다 [exact, enumerated]
      (측정: A=1(실레포 미핀닝 6) · B=3(대상 0) · C=1(재사용WF+서드파티+docker 무digest) ·
      D=2(YAML 파손) · E=0(전부 SHA+로컬) · F=2(핵심도구 부재) · G=2(python3 부재) ·
      H=0(first-party 면제 opt-in))
- [ ] DG-04: 커밋에 scope 밖 경로가 0 건이다
      (측정: `git show --name-only --format= HEAD` 결과가 `infra-kit/` · `docs/infra/` ·
      `.harness/sprint-contract-kaizen-phase8-` 접두로만 구성)
