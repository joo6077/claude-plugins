---
title: Kaizen Changelog
version: 1.6.0
last_updated: 2026-08-13
---

## [2026-08-13] — 사실 정정 사이클 (14/14 CHANGED)

### 트리거

사용자가 `/insights` 재실행 후 카이젠 오케스트레이션 요청. 리포트(2026-08-13, 62일 · 81 세션 중
71 분석 · 1,551 메시지 · 241 커밋)를 §0 으로 주입. Step 0.6 선별에서 low-signal 4킷
(infra/react/planning/onboarding) 제외를 제안했으나 사용자가 **전체 14 Phase** 를 선택.

### 이번 사이클의 핵심 판단 — §0 재승격 금지

`/insights` Friction #1~#3 은 **직전 사이클(2026-07-27)에 이미 구조적으로 승격된 주제**였고,
리포트 관측 윈도(2026-06-12~08-12)가 그 수정 착지일(2026-07-28) **이전을 대부분 포함**한다.
→ **재출현 = 미측정이지 무효화가 아니다.** 같은 규칙을 다시 추가하는 것을 사이클 하드 규칙으로
금지하고, 유효 신호를 (a) §0 신규 델타 D1~D5 (b) 2026-08-11~12 글로벌 REJECT
(c) 2026-08 reflection 태그 세 곳으로 한정했다.

그 제약의 결과로 이번 사이클은 **새 규칙을 쓰는 대신 우리 문서가 틀렸던 것을 정정하는** 성격이 됐다.
각 Phase 는 codex 로 확보한 외부 근거 파일 하나만 읽고 그 안의 인용으로만 사실을 뒤집었다.

### Phase 결과 (14/14 CHANGED)

- **Phase 1 설계 가이드** — 공식 스펙 정정: 서브에이전트 중첩은 "불가" 가 아니라 **main 아래 3층까지
  허용**(`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1` 로 차단), frontmatter 공식 15 필드에 필수는
  `name`·`description` 둘뿐. skill-design-guide §5.6 **Variant Budget**(상한 3 · primary axis 1(+1) ·
  Variant Matrix 5열 · 부대 산출물 금지) + 유형 11 "탐색형 생성" 아키타입 — D2 대응.
  §3.8 **User-Reported Failure Gate**(REOPENED · 반박 금지 · 오라클 6축 대조 우선) — D3 대응.
- **Phase 2 Contract** — 경로 화이트리스트 5회 재발을 문장 추가가 아니라 등급 상향으로 처리.
  `conditions_digest` **봉인**(E1→E3)으로 계약 자기편집을 탐지하고, amendment 를
  **direction × consent 2축**으로 분리해 `narrowing·unanchored` 만 PASS 근거가 되게 했다.
  측정 커버리지 검출기 · 인자 매트릭스 · 음성 대조 추가. 기존 계약 109개 봉인 검사 회귀 0.
- **Phase 3 Evaluator** — `[미검증]` 3분기를 4분기로 쪼개 **UNVERIFIED_ENV** 를
  **UNVERIFIED_INVALID_EVIDENCE** 와 다른 장부에 적는다. 자동 REJECT 임계 2 는 후자에만 적용하고,
  전자는 검증 커버리지 게이트(< 0.60 → BLOCKED)에만 쓴다 (2026-08-11~12 REJECT 4건이 전부
  "도구 부재로 정당하나 임계 초과" 였다). **Discriminating Evidence Gate** +
  **Canonical User-Reported Failure Protocol** 신설. 사실 정정: binary PASS/FAIL 근거로 오인용하던
  scoring bias 논문을 **CheckEval**(decomposed binary Q → evaluator agreement 평균 +0.45)로 교체.
- **Phase 4 Harness** — 문서가 주장하는 CLI 와 실제 구현이 갈린 것을 **`docs-contract` 선언 블록 +
  `validate-doc-contracts.py`** 로 묶었다(실체가 SSOT). 게이트 exit **taxonomy**
  (`harness/evals/gate-exit-codes.md` — 0 pass / 1 policy_violation / 2 usage_or_infra_error /
  3 no_data_not_run) 신설 후 조용히 통과하던 게이트 5종을 수정(아래 별도 절).
  Phase 번호와 충돌하던 후속 단계를 **Step 11/11.5/11.6/12 → F1~F4** 로 개명.
- **Phase 5 flutter** — 버전 사실 정정 3종: Freezed `when`/`map` 은 3.0 에서 제거됐다가
  **3.1.0 에서 재추가**(최신 stable 3.2.5) · Flutter stable 3.44.7 → **3.47.0**
  (Java 17 · KGP 2.4.0 · AGP 9.1.0 · Gradle 9.3.1) · Impeller 는 3.47 부터 **macOS/Linux/Windows 기본**.
  **Primitive Substitution Gate** SSOT(E1→E2) · invalidate 경계 · 위젯 테스트 하네스 ·
  성능 **Environment Exclusion Checklist**(D5 성공 사례의 절차화).
- **Phase 6 design** — `visual-change-protocol.md` §5~§7 을 append-only 로 신설.
  §5 **Variant Distinctiveness Gate**(축 선언만으로는 부족 — pairwise Hamming 판정식. 글로벌
  REJECT UI-04 를 hamming=0 으로 재현해 exit 1) · §6 **Decision Propagation Manifest**
  (`decisions.yaml` + coverage rule, manifest 부재를 통과로 접지 않고 NO_MANIFEST exit 3) ·
  §7 **Evidence Channels** 4종. design-mockup 의 고정 "시안 5개" 를 개수 계약으로 교체.
  WCAG 터치 타겟을 **AA 24×24(SC 2.5.8) / AAA·Apple HIG 44×44(SC 2.5.5)** 로 귀속 정정.
- **Phase 7 backend** — `write-path-integrity-protocol.md` SSOT 신설: 경합 invariant 3유형 → DB
  primitive 매핑 · "트랜잭션으로 감쌌다" 만으로 PASS 금지 · 제약↔upsert 대상 정합 ·
  **멱등 쓰기 계약 6항** · Integration Target Proof(E3) · outbox at-least-once. D4(TOCTOU 를 앱이
  아니라 SQL 술어로) 반영. 사실 정정 3종 — outbox+CDC "exactly-once 보장" → at-least-once +
  consumer idempotency 필수 · Stripe 멱등에 payload 비교/24h pruning · backend-reviewer 의
  canonical 블록이 "복제" 를 주장하면서 v4.0 으로 stale → v5.0 재동기화.
- **Phase 8 infra** — "도구 부재 = 위반 0" 을 **gate-result-taxonomy.md 5상태**로 승격
  (PASS / VIOLATION / SKIP_NO_TARGET / TOOL_OR_ENV_MISSING / EXECUTION_ERROR).
  핀닝 검사를 grep → **YAML 파서**로 교체 — 현행 grep 오라클은 이 레포 워크플로의 미핀닝 6건을
  전부 0건으로 보고하고 있었다. fixture 8종 전수 검증. 사실 정정 4종(카테고리 순서 드리프트 ·
  stale 사본 참조 · OTel signal 별 status 분해 · USE×RED).
- **Phase 9 rust** — 사실 정정: `#[sqlx::test]` 는 "독립 트랜잭션" 이 아니라 **테스트별 새 DB +
  자동 migration + 성공 시 cleanup** · Axum 0.8 발표일 2024-12-01 → **2025-01-01** ·
  MockDatabase 는 SQL predicate 의미를 검증하지 못함. unwrap/expect 제거를 `?` 치환에서
  **타입 설계 우선**으로 전환하고 workspace clippy deny 5 lint 로 등급 상향(E1→E3).
  `concurrency-guard-protocol.md` SSOT(D4).
- **Phase 10 react** — low-signal Phase. **새 규칙 0건**, evidence 가 확인한 stale 지점만 정정.
  템플릿 4종(vite ^6→^8 · @hookform/resolvers ^3→^5.1 · zod ^3→^4 · `@lingui/macro` 제거 —
  unmaintained) · Zod v4 resolver workaround 를 legacy resolver 전용으로 강등 ·
  scroll-driven/View Transitions 지원 수치 갱신 · react-animation §6 **표준 커버리지 공백 8종**
  신설(처리 경로는 직접 구현·fallback·사전 렌더 자산 3종뿐 — 라이브러리 0개 원칙 유지).
- **Phase 11 planning** — 사실 정정 3종. Projects v2 는 "GraphQL only" 가 아니라
  **REST `/projectsV2` 도 제공**(금지 대상은 sunset 경과한 classic) · "한 시나리오 = one When" 은
  Cucumber 원문에 없으므로 **planning-kit 내부 원자성 규칙으로 라벨링**(규칙 자체는 보존) ·
  HBR premortem 의 "개별 기록 → 공유" 절차를 **[미확인]** 으로 강등하고 인용 범위를 기법 자체로 한정.
- **Phase 12 reflect** — 태그 정규화를 LLM 부탁에서 **결정론적 5단계 pass** 로 승급(E1→E3,
  `tag-lemma-map.tsv` + `_lib-tag-canon.sh`). 재발 증가를 문구 문제로 오진하지 않도록
  `hook_coverage_audit` 를 등급 상향보다 먼저 돌게 라우팅. 파편화 지표를 `fold_ratio`(아무것도 못
  묶으면 1.00 이라 영원히 "정상") → **`singleton_share`** 로 교체하고, low confidence 에서는
  demotion 산출을 금지(E2→E3). 실측 회수: 원시 71 → 클러스터 110.
- **Phase 13 bambu** — D1(곡면 계단현상 · voronoi 스트링잉 · 바닥 박리). 근본원인은 **사용자 자신의
  직전 출력 실패가 다음 프로파일로 들어오는 경로 자체가 없었던 것** — 규칙 문장이 아니라
  **Phase 1.9 Failure-Mode Detector**(L1/L2/L3) 를 신설했다. **Phase 3.0 Supportability Split** —
  `adaptive_layer_height` 는 `PrintConfig.cpp` 에서 주석 처리 + legacy ignore set 이라 넣어도
  무시된다 → 근사 구현 금지, notes only 로 명시 보고. E3 게이트 금지 키 4종 확장.
- **Phase 14 onboarding** — setup-guide 는 가이드를 영속 아티팩트로 생산하는데 **이미 배포된 가이드를
  다시 재는 경로가 없었다.** 그 결과 킷 쇼케이스 예제가 킷 자신의 evals 6 중 3을 3개월간 위반한 채
  배포돼 있었다. **Guide Conformance Gate**(E3, LLM 미호출 4 판정) + Phase 1 Regeneration Drift 신설.
  사실 정정: Flutter 예제의 `AppDelegate.swift`+`FirebaseApp.configure()` 필수 단계는 현행 FlutterFire
  절차에 없다 → 제거하되 **Capability/Background Modes 는 여전히 iOS 프로젝트 작업**임을 구분 명시.
  `.p12` deprecated 단정 제거, Apple 두 사이트 구분을 작업별 7행 표로 교체.

### 우리 문서가 틀렸던 것 (Phase 횡단 요약)

| 정정 | 내용 |
| --- | --- |
| 서브에이전트 중첩 | "불가" 단정 → 공식은 main 아래 3층까지 허용, frontmatter 15 필드 중 필수는 2개 |
| scoring bias 논문 | binary PASS/FAIL 근거로 오인용 → 실제 근거는 CheckEval (agreement 평균 +0.45) |
| Freezed | "3부터 `when`/`map` 영구 제거" → 3.1.0 에서 재추가 (최신 stable 3.2.5) |
| Flutter stable | 3.44.7 → 3.47.0 (Java 17 · KGP 2.4.0 · AGP 9.1.0 · Gradle 9.3.1) |
| Impeller | "macOS 실험적 · 데스크톱 미지원" → macOS/Linux/Windows 는 3.47 부터 기본, Web 만 Skia |
| WCAG 터치 타겟 | 44×44 를 AA 로 표기 → 24×24 가 AA(SC 2.5.8), 44×44 는 AAA(SC 2.5.5) |
| `#[sqlx::test]` | "독립 트랜잭션" → 테스트별 새 DB + 자동 migration + 성공 시 cleanup |
| Axum 0.8 발표일 | 2024-12-01 → 2025-01-01 |
| GitHub Projects v2 | "GraphQL only" → REST `/projectsV2` 도 제공. 금지 대상은 classic |
| Cucumber one-When | "공식 규칙" 으로 인용 → 원문에 없음. planning-kit 내부 규칙으로 라벨링 |
| HBR premortem 절차 | 단정 인용 → [미확인] 강등, 인용 범위는 기법 자체로 한정 |
| outbox + CDC | "exactly-once 보장" → at-least-once + consumer idempotency 필수 |
| react-kit 템플릿 | vite ^6→^8 · @hookform/resolvers ^3→^5.1 · zod ^3→^4 · `@lingui/macro` 삭제 |
| FlutterFire | Flutter 예제에 네이티브 `FirebaseApp.configure()` 를 필수로 둠 → 현행 절차에 없음 |
| `adaptive_layer_height` | process JSON 키로 취급 → 주석 처리 + legacy ignore set. 넣어도 무시됨 |

### 이 사이클이 잡은 실제 코드 결함

전부 "조용히 통과" 계열이다 — 실패를 성공으로 보고하던 경로다.

- `harness/evals/kaizen/feedback-system/aggregation-test.sh` — `yq` 부재 시 SKIP 후
  "ALL TESTS PASSED". **이 머신에 yq 가 없어 그동안 실제로 무검증 통과 상태였다.**
- `save-test.sh` — 네거티브 테스트가 stderr 를 버려 엉뚱한 이유의 실패도 통과로 집계.
- `scripts/finalize-phase.sh --help` — `mktemp` 가 help 출력보다 먼저 실행돼 read-only 환경에서 실패.
- `scripts/sync-orchestrator.py` — substring `find()` 로 마커를 찾아 Gotchas 산문 불릿 안에
  자동생성 블록 92행을 주입해 왔고, 그 결과 **Process 절에 Phase 12·13 헤딩이 아예 없었다.**
  그런데도 `--check-only` 는 exit 0. 행 앵커 + 유일성 강제로 교체.
- `scripts/validate-post-kaizen.py` — `git_diff_names()` 가 실패 시 `[]` 를 돌려줘 diff 기반 검사
  3건이 조용히 통과. ERROR 상태 신설 + scope-isolation 킷 prefix 를 marketplace.json 에서 유도
  (누락돼 있던 4킷 커버).
- react-kit §5.4 가 "접근성이 내장된 라이브러리 사용을 고려한다" 로 **라이브러리 0개 원칙과 자기모순**.

### 프로세스 상 특기사항

- **Phase 3 계약 폐기·재작성.** AR-01(scope 열거)과 AR-02(frontmatter 버전 일치)가 상호배타였다.
  `contract-design-guide.md` 는 생성 이래 frontmatter 가 없어 AR-02 의 PASS 집합이 공집합이었고,
  근본 해소는 scope 밖 수정을 요구해 AR-01 을 위반했다. 구현자가 `relaxing · unanchored` 로
  자기신고했고 **규칙대로 PASS 근거가 되지 못했다** — 이번 사이클이 도입한 봉인·2축 amendment 가
  의도대로 작동한 사례다. 사용자 승인을 앵커로 오케스트레이터가 v2 재작성.
- **오케스트레이터 자신도 같은 게이트에 걸렸다.** 감사 로그를 Step F1 이 아닌 사이클 도중에 커밋해
  Phase 3 의 scope 측정에 부기 커밋이 섞였다. 계약을 고치지 않고 **커밋을 되돌려** 해소했다.
- 독립 평가자의 진단: **"파일 단위 exact enumeration 은 다중 커밋 오케스트레이션 스프린트에
  구조적으로 취약하다."** 같은 형상의 결함이 3회 재발했다. Phase 4 가 구조 수정안을
  `.harness/.meta/phase4-handoff-to-contract.md` 에 남겼다 (Phase 2 소관이라 직접 수정하지 않음).
- 외부 근거는 codex 를 **foreground 11회** 호출해 확보하고 `.harness/.meta/evidence/phase1~14.md` 에
  파일로 고정한 뒤, 각 Phase 서브에이전트가 그 파일만 읽게 했다(백그라운드 실행 중 네트워크 조회 금지).
  이 방식으로 배치 A(Phase 8·9·10)는 QA REJECT 0회로 통과했다.
- 14 Phase 전부 CHANGED + QA APPROVE, 미검증 0건. 14 Phase 완료 시점 기준 31 커밋 · 154 파일 ·
  +13,525/−1,562.

### 버전

11킷 전부 minor bump. harness 0.7.0 · flutter-toolkit 0.7.0 · design-kit 0.4.0 · backend-kit 0.3.0 ·
infra-kit 0.3.0 · rust-kit 0.3.0 · react-kit 0.3.0 · planning-kit 0.5.0 · reflect-kit 0.6.0 ·
bambu-kit 0.6.0 · onboarding-kit 0.3.0

## [2026-07-28] — 병렬 스프린트 안전성 (harness v0.6.0, 카이젠 후속 스프린트)

### 트리거

사용자 지적 — "스프린트를 병렬로 처리가 안 되는 거 같은데? 세션을 병렬로 돌리면 같은 플젝 내에서
이거 수정이 필요할 거 같은데." 2026-07-27 카이젠에서 Phase 5~14 를 병렬로 돌릴 때 서브에이전트마다
"고정 경로 쓰지 말고 phase 별 경로에 써라" 를 손으로 프롬프트에 박아야 했던 것이 증거였다.

### 근본원인 3 종

1. 계약·QA 산출물이 단일 고정 경로(`sprint-contract.md` / `sprint-feedback.md`)라 병렬 세션이 충돌.
   `scripts/spawn-kaizen-phase.sh` 가 모든 서브에이전트에 그 고정 경로를 **적극 주입**하고 있었다.
2. 글로벌 피드백 identity 를 LLM 이 생성 + fallback 이 `pwd` 기반 →
   `claude-plugins` 하나에 `project_hash` 43 종, `ea3aeacd` 하나가 3 개 프로젝트에 공유, `a1b2c3d4` 같은 날조값.
3. 계약이 write-once 라 실행 중 사용자 교정을 담을 자리가 없음 (digest usc=true 재위반 12 건,
   그중 계약 본문을 코드에 맞춰 넓혀 위반을 소거한 사례 1 건).

### 설계 — 접두형이 아니라 접미형

배포본 fit-pal 3 곳에 `sprint-contract-<slug>.md` 40 개 · `sprint-feedback-<slug>.md` 7 개가
이미 있었고 계약↔피드백이 슬러그로 짝지어져 있었다 (최종 수정 2026-07-27). **사용자가 이미 손으로
쓰던 관행**이라 접두형은 이 40 개를 고아로 만든다. 설계 패널(3 안 × 9 심사)이 이 근거로 초기
접두형 안을 기각했고, Codex diagnose 3 회로 교차 검증했다.

### 확정 규약

- 경로 `sprint-contract-<slug>.md` / `sprint-feedback-<slug>.md` / `sprint-amendments-<slug>.md`.
  슬러그 없으면 plain 계속 유효 (마이그레이션 강제 없음)
- frontmatter `slug` / `status: active|done` / `owner_session`
- **`status: active` 명시분만 active. 필드 없으면 레거시로 제외** — 배포본 40 개가 전부 status 가
  없어서 파일 개수를 세면 fit-pal 이 후보 27 개로 영구 BLOCKED 된다
- ladder: 1 명시경로 / 2 세션소유 유일 / 3 active 유일 / **3.5-a 레거시 plain 우선** /
  **3.5-b plain 없고 레거시 유일** / 4 BLOCKED. TOCTOU 는 `경로+sha256+status` 지문 고정으로 방지
- CONTRACT_ROOT 를 **"처음 만나는 `.harness/` 에서 멈춤"** 으로 개정 (v5.1 의 `project.yaml` 기준이
  조용한 오귀속을 만들었다)
- `status: done` 전환 주체 = qa-evaluator (APPROVE 직후)
- amendment 는 **사이드카** (계약 본문에 `##` 추가 금지 — schema 허용 헤더 위반 방지)
- User Correction Audit — 읽기 전용·보고 전용, 로그 부재 시 degrade

### 이 스프린트가 남긴 가장 큰 교훈

**1 차 구현은 계약 25 조건이 전부 PASS 인데 기능이 동작하지 않았다.** 계약 oracle 이 죄다
"문서에 서술이 N 건 이상 존재하는가" 라 런타임 파손을 재지 못했다. 이번 카이젠이 Phase 3 에 도입한
Evidence Validity Gate 가 막으려던 함정에 계약 자신이 빠진 것이다.
→ 검증을 "**실행 결과만이 증거**" 로 바꾸자 blocking 7 건이 드러났다 (zsh nomatch 로 glob 이 명령을
통째로 죽임 · 따옴표 불일치로 ladder 2 영구 불성립 · status done 전환 주체 부재 · 0-active BLOCKED
회귀 · 조용한 오귀속 · ladder 1 존재검사 누락 · 파서 range 재점화).
→ Evidence Validity Gate 를 4 → **5 검사**로 확장 (신규: 실행 가능성 — 셸 이식성 포함).

### QA 3 회전

- iter1 REJECT — CONTRACT_ROOT 규칙을 읽기 측만 고치고 쓰기 측(`sprint-contract/SKILL.md`) 누락
- iter2 REJECT — **같은 결함의 세 번째 표면** (`save-feedback.sh resolve_contract_root()`)
- iter3 **APPROVE 25/25** — 한 곳씩 고치는 대신 전수 조사로 전환. 4 표면 × 16 디렉토리 × 2 셸 =
  32 run, SAME=32 / DIFF=0

### 검증 (전부 실행 기반)

배포본 `.harness` **13 곳 × zsh·bash = 26 run → BLOCKED 0** (project.yaml 없이 계약만 있던 4 곳도
자기 계약을 찾는다 — 9 곳에서 13 곳으로 확대) · 조용한 오귀속 소멸(app_kiosk sha256 일치) ·
셸 스니펫 32 개 × 2 셸 = 64 run nomatch 사망 0 · 외부 배포본 무수정(접미형 계약 40 개 불변)

### 부수

- eval 픽스처 5 종 + 실행 절차를 새 ladder 에서 실행 가능하도록 갱신
- `sprint/SKILL.md` iteration 카운터가 슬러그 대응 피드백을 세도록 — 방치하면 매 라운드 N=1 로
  리셋되어 REJECT 3 회 에스컬레이션 가드가 영구 무력화된다
- sprint-contract 에 `conditions:` **계산** 단계 추가 — 이 세션에 계약 작성자가 조건 수를 3 회
  연속 틀렸다 (18→22, 19→27, 22→25). 사람이 타이핑하게 두면 안 되는 값이다

## [2026-07-27] — enforcement 등급화 전면 도입 + 크로스 Phase 회귀 4건 수정 (14/14 CHANGED)

### 트리거

사용자가 "인사이트 돌려서 카이젠 진행" 요청. `/insights` 재실행(2026-07-27, 51세션·187커밋·53일)
+ `/reflect-digest` 30일 집계(760 엔트리) 를 §0 으로 주입. Step 0.6 선별에서 low-signal 4킷
(infra/react/planning/onboarding) 제외를 제안했으나 사용자가 **전체 14 Phase** 를 선택.

### 이번 사이클의 핵심 판단

인사이트 Friction #1(의도 확인 전 편집)·#3(스코프 드리프트)은 **직전 사이클에 이미 승격된 주제**인데
세션당 발생 비율이 줄지 않았다. 따라서 "규칙 문장을 또 추가"가 아니라 **enforcement 방식 전환**을
사이클 전체의 프레이밍으로 잡았다 — soft reminder → 구조적 게이트.

### Phase 결과 (14/14 CHANGED)

- **Phase 1 설계 가이드** — **Enforcement 3등급(E1 문장 / E2 아티팩트 / E3 결정론적 게이트)** 신설.
  승급 규칙: 재발 2회→E2, 3회 또는 비가역·신뢰손상→E3. §3.7 **Completion Evidence Gate**
  ("빈 스냅샷은 PASS 증거가 아니라 검증 실패 신호"), §5.5 **Counterpart Enumeration**.
  **사실 오류 정정**: 가이드 4곳이 "서브에이전트 중첩 불가"로 단언했으나 공식은 기본 3층 허용.
- **Phase 2 Contract** — digest 결함 5종을 전부 등급 상향으로 처리(E1→E2/E3).
  `## Notes` 금지 규칙이 실사용(카이젠 계약의 배경·GAP 섹션)과 어긋나 있던 것이 재위반의
  근본원인이었음을 발견 → 2계층 헤더로 재정의 + 결정론적 검사. contract-schema v3→v4.
- **Phase 3 Evaluator** — **Evidence Validity Gate** 신설. 증거의 *존재*가 아니라 *유효성* 판정
  (빈 캡처/0매치/0테스트/출처). `[미검증]` 3분기 triage 로 "미구현을 미검증으로 세탁"하는 경로 차단.
  각 kit reviewer 가 복제할 **Canonical Unverified-Evidence Protocol** 정본 고정.
  피드백 저장 경로 ladder + degraded 저장(저장 실패가 verdict 를 무효화하지 않음).
- **Phase 4 Harness** — **회귀 규명**: `finalize-phase.sh` 가 없는 CLI 인자를 넘겨 argparse exit 2 로
  **3 사이클간 무증상 실패**했고 `2>/dev/null` 이 은폐. MAX_PHASE 하드코딩 10 이라 Phase 11~14 는
  아예 거부. 둘 다 수정. `/sprint` 핸드오프 git 재검증 + iteration 3회 escalation(E2).
- **Phase 5 flutter** — 시각 증거 규약(E2)을 UI 5종에 전수 적용 + `visual-evidence-protocol.md` SSOT.
  MCP 도구명 하드코딩 대신 project-detection 감지 ladder 로 일반화.
  실측 버그: `$DART test` 는 widget test 실행 불가 · 무출처 주장 → 실측 URL 교체.
- **Phase 6 design** — `visual-change-protocol.md` SSOT 신설. 승인 시안 값이 프로젝트 토큰보다
  상위(§1), **의도 외 영역 변화 = 실패**(§2), 승인기록 artifact 규격(§4, 글로벌 REJECT UI-06 대응).
  design-reviewer 미검증 임계 3항 → canonical 2건 정합.
- **Phase 7 backend** — Counterpart Enumeration 도메인 일반화(E2). 빈 상태 상태코드(RFC 9110),
  timestamp 타임존(RFC 3339), write-path idempotency, mock-only 통합테스트 주장 차단,
  backend-audit Step 0 스택 감지(Rust 는 rust-audit 리다이렉트).
- **Phase 8 infra** — 문서가 아니라 **실제 버그 3건 수정**. infra-test 가 생성해주는 CI 검증
  스크립트에서 grep 앵커 누락(미핀닝 3건 중 1건만 검출) · WARN 후 exit 0(게이트 무력화) ·
  빈 glob 오보. fixture 재현 → 수정 → 3 fixture 재검증. 도구 부재를 위반 0 으로 집계 금지.
- **Phase 9 rust** — 명령 실행·증거 규약 신설. `cargo metadata` 타깃 감지(bin-only 에 `--lib` 금지),
  pipefail 규약 E2 승급, 가드 우회 금지, 마이그레이션 선적용(`#[sqlx::test]` 는 불필요함을 공식
  문서로 구분). rust-api 예시의 axum path 문법 오류 수정.
- **Phase 10 react** — reviewer 6종 중 react 만 canonical 조항이 0건이었음 → 신설.
  `render-evidence-protocol.md` SSOT. **0매치 판정 규칙** — react-reviewer 는 도구가
  Read/Grep/Glob 뿐이라 "스코프가 없어서 0" 과 "위반이 없어서 0" 이 구분되지 않던 구조적 공백.
  **Library Policy 완화 0건을 3중 검증**(금지 12항목 언급 수 전후 대조 포함).
- **Phase 11 planning** — planning-reviewer 의 "미검증 0" 요구가 canonical 1건 허용과 충돌 → 해소.
  `plan-audit` 분모 규칙이 셋(Step 4 / 템플릿 / reviewer)이 서로 모순이던 것도 정정.
  INVEST T 를 **반증가능성** 판정으로 강화 + `## Surfaces` 양면 열거 템플릿.
- **Phase 12 reflect** — 이번 사이클 최고신호. 훅 실패 351건(40%)이 54종 태그로 파편화.
  **hook(예방)+digest(복구)+ledger(측정) 3점 수정.** digest 단독 해결을 기각한 근거: ledger 의
  `post_freq` 가 `mistake_tag` 를 키로 재발을 세므로, 파편화는 **효과 측정을 구조적으로 과소집계**하여
  실패한 규칙이 "효과 있음"으로 살아남게 만든다. 닫힌 라벨 집합은 label collapse 연구 근거로 기각.
  `actionability` 1필드 + LLM 미호출 결정론적 dedup(fail-open, 억제분은 `.env-issues.tsv` 에 누적).
- **Phase 13 bambu** — **SSOT 자체가 틀려 있었음**을 규명. `xy_hole_compensation` 은 경계 오프셋이라
  지름 변화가 2× 인데 SSOT 가 이를 명시하지 않아 계약(지름)과 구현(오프셋)이 갈렸다(REJECT PL-01).
  더 중요하게 §7 의 예시 수치 자체가 틀렸고 **그 값이 실제 출력한 프로파일에 박혀** 사용자 실측
  보고("베어링이 안 맞음")와 수치가 일치. 3MF 파싱 견고화 + 생성물 E3 게이트(주입 결함 4종 검출 확인).
- **Phase 14 onboarding** — **evals 가 사용자 피드백 메모리와 정면 모순**하던 상태 수정
  (Flutter FCM 가이드 테스트가 Flutter 에 존재하지 않는 네이티브 Swift 호출을 요구).
  출처 원장(Step별 URL+조회일, E2) + 경로·파일명 날조 금지(E2) 신설.

### 크로스 Phase 회귀 4건 (오케스트레이터 직접 수정)

1. **validate-plugin V5 백틱 오탐** — canonical 조항이 금지 동의어로 열거한 `TBD` 를 미완성
   placeholder 로 오탐해 3킷 Exit 2. 더 위험한 것은 `--fix` 가 그 문구를 조용히 변조하는 것.
   검사·치환 양쪽에서 인라인 코드 스팬 제외("인용은 백틱"). 음성 테스트 + `--fix` 불변성 검증.
2. **finalize-phase 중첩 키 미갱신** — 정규식이 열 0 을 요구해 `phases:` 하위 카운터를 못 찾고
   최상위에 중복 키를 생성. Phase 4 가 무증상 실패를 고치자 드러난 선재 버그.
3. **orchestrator 참조 drift** — onboarding research-sources 경로가 존재하지 않는 위치를 가리킴 ·
   Stripe 구 호스트(크로스호스트 리다이렉트라 fetch 실패).
4. **Phase 번호 자기모순** — AUTO 블록은 Step 13=bambu/14=onboarding 인데 수기 본문은
   "Phase 13 — onboarding". 템플릿에는 **Phase 12·13 섹션이 아예 없었다** → 신설 + 번호 정정.

### 버전

11킷 전부 minor bump (14/14 CHANGED). harness 0.5.0 · flutter-toolkit 0.6.0 · design-kit 0.3.0 ·
backend-kit 0.2.0 · infra-kit 0.2.0 · rust-kit 0.2.0 · react-kit 0.2.0 · planning-kit 0.4.0 ·
reflect-kit 0.5.0 · bambu-kit 0.5.0 · onboarding-kit 0.2.0

### 부산물

`.claude/kaizen-input/fit-pal-hook-diagnosis-2026-07-27.md` — digest 노이즈 40% 의 근본원인을
fit-pal 레포에서 실측 진단(리포트만, 해당 레포 무수정). 원인이 2종이며 상대경로 훅이
서브디렉토리 cwd 에서 해석 실패하는 쪽이 145건/41% 로 더 크다.

## [2026-06-11] — hook permission-denied 근본원인 + validate-plugin V8 가드 (인사이트 주도 부분 카이젠)

### 트리거

사용자가 "전체 인사이트 + 카이젠" 요청. reflect-digest `project=all` 30일 cross-project 집계(27 프로젝트 / 2,586 엔트리)에서 **hook permission-denied 계열이 24개 프로젝트 957건(전체 friction의 38%)으로 단일 최대 마찰원**임을 발견. 근본원인은 harness/design-kit 플러그인의 `hooks.json`이 직접 실행하는 `.sh` 4종이 git mode 100644(비실행)로 커밋된 것 — 모든 SessionStart·PreToolUse:Bash hook이 "Permission denied"로 실패하고 있었다 (오늘까지 진행 중).

### 선행 조치 (main 직접 — 사용자 승인)

- `harness/scripts/{env-check,run-guard,sdk-guard}.sh` + `design-kit/scripts/env-check.sh` mode 100644→100755 복원 (소스 + cache + marketplace 복사본). 음성·양성 실행 검증.
- harness v0.4.4 + design-kit v0.2.5 릴리스로 향후 설치본에 전파.

### Step 0~0.6 (Self-Audit + Triage)

- 데이터 풀 재수집(insights 6d / global feedback 190 / hub 5). orchestrator↔marketplace sync drift(릴리스로 발생) 해소.
- **Triage 판정**: 직전 풀 사이클이 6일 전(2026-06-05)이고 /insights도 동일 데이터 윈도우 → "신선함 ≠ 새 신호". validate-plugin 전 kit OK. 고신호는 hook-exec 회귀 가드뿐.

### Phase 결과 (1 CHANGED / 13 NO_CHANGE)

- **Phase 1~3** 설계가이드/Contract/Evaluator: NO_CHANGE — 인사이트 테마(Scope-Bound Edits, Binary Decidability, 측정 정밀도 git-ls-files/scope enumerate, 조용한 PASS 금지)가 6일 전 사이클에 이미 흡수됨(파일 라인 단위 확인).
- **Phase 4** Harness: **validate-plugin V8 `hook-exec` 신규** — hooks.json 직접 실행 `.sh`의 exec 비트(0755) 검증. bash/sh/source 경유 제외. 음성 테스트(mode 0644→FAIL Exit 2) 통과. plugin-validation-guide §3.8 + v1.1.0. 권위 카운트 7→8 동기화, 운영 참조는 number-agnostic("전 카테고리")로 drift 방지.
- **Phase 5~14** per-kit(flutter/design/backend/infra/rust/react/planning/reflect/bambu/onboarding): **전 10 NO_CHANGE** — 병렬 triage 에이전트가 데이터풀 귀속 신호·도메인 currency·hook-exec·설계가이드 drift 4축을 실제 파일 점검. kit별 콘텐츠 결함 0건(REJECT 80건은 전부 외부 프로젝트 실사용 QA).

## [2026-05-07b] — fresh /insights followup kaizen (Gap 1~6 흡수)

## [2026-06-05] — /insights 2026-06-04 마찰 패턴 카이젠 (13 Phase)

### 트리거

사용자가 `/insights` 리포트(2026-06-04, 168 세션) 기반 오케스트레이션 요청. §0 fresh 주입 후 13 Phase 전수 실행. 선행으로 인사이트 마찰 패턴을 1차 승격(글로벌 가드레일 + flutter-extract/provider Gotcha + 프로젝트 memory, QA APPROVE 11/11).

### Phase 결과 (11 CHANGED / 2 NO_CHANGE)

- **Phase 1** 설계가이드: agent-design-guide v1.4.0 Fan-out 상한·Exploration Budget(Friction #6) + faithful-reasoning self-audit.
- **Phase 2** Contract: 측정 명령 oracle 타당성(semantic match + precondition) 원칙(LG-07/AR-01 방지).
- **Phase 3** Evaluator: Execution-Grounded Evidence — 실행 주장 조건의 산출물 능동 요구(Friction #5).
- **Phase 4** Harness: tool-call-evidence-verification 절차 신설(Friction #5 운영).
- **Phase 5** flutter: flutter-feature/screen 과잉설계 방지 Gotcha(Friction #3).
- **Phase 6** design: design-system/component 스코프 명시 Gotcha.
- **Phase 7** backend: NO_CHANGE(가드 포화).
- **Phase 8** infra: NO_CHANGE(가드 포화 + parity 확인).
- **Phase 9** rust: rust-model Enumerate-before-Act 가드 누락(sibling drift) 차단.
- **Phase 10** react: 생성형 9스킬 §5.5 가드 전수 보강(0/9→9/9) + U+FFFD 4곳 복구, Library Policy 완화 0.
- **Phase 11** planning: 생성형 8스킬 scope-discipline 가드.
- **Phase 12** reflect: user_stated_constraint fast-track 승격(rule #0) — Friction #2 근본 대응.
- **Phase 13** onboarding: setup-guide 스코프 가드 Gotcha 7.

### 공통 원칙

프로젝트-특정 금지(no ValueNotifier/useState)는 글로벌 가드레일에만, kit에는 stack-agnostic 일반화분만 반영. 1차 승격분 중복 금지 전 Phase 준수.


### 트리거

사용자 지적: 첫 번째 PR (PR #8) 은 13일 전 stale 추출본 (`.claude/kaizen-input/insights-report.md`, 2026-04-24자) 기반이었다. 진짜 fresh `/insights` 산출물은 `~/.claude/usage-data/report-ko.html` (2026-05-07 23:00, 0.0h ago, VERY FRESH ✓) 였다. fresh 와 stale 의 차이로 인해 **6 개의 신규 항목이 누락**되었다 — 이를 followup 사이클로 흡수.

### Step 0 강화 — fresh report 자동 탐색 경로 박기

- `scripts/collect-kaizen-data.py` `INSIGHTS_CANDIDATES` 에 4 경로 우선순위:
  1. `~/.claude/usage-data/report-ko.html` (한국어 fresh) — linter 가 제거함, 사용자 의도로 판단
  2. `~/.claude/usage-data/report.html` (영문 fresh)
  3. `<repo>/.claude/kaizen-input/insights-report.md` (repo 추출본)
  4. `~/.claude/kaizen-input/insights-report.md` (글로벌 추출본)

- `_extract_html_text()` 신규 — script/style 제거 + tag strip + html unescape (표준 라이브러리만)
- VERY FRESH (24h 이내) 마커 + STALE (60d 초과) 마커
- 데이터 풀 §0 출력에 fresh marker + format 표기

### Fresh insights 6 갭 흡수

- **Gap 1 — Scope-Bound Edits** (Friction "과욕적 범위 확장 — 허락 없는 삭제, 요청 안 한 디자인 선택"): skill-design-guide §3.6 신규 sub-section. 시작 전 경계 한 줄 명시 + 인접 위반 별도 list + Hard-stop 액션 5 종 (file deletion, package removal, branch deletion, force push, main push, schema migration, secret rotation). §11 parity 표 9번째 행 추가.
- **Gap 2 — PreToolUse 훅 3 종** (Quick Win "PreToolUse 훅으로 origin/좀비 MCP 차단"): `.claude/settings.json` Edit/Write 매처에 보호 브랜치 가드, Origin Sync 가드, 좀비 MCP 가드. 모두 `exit 0` graceful degradation (stderr 경고만).
- **Gap 3 — `/sprint` 스킬** (Quick Win "/sprint 스킬로 contract-QA-push 루프 승격"): harness/skills/sprint/SKILL.md 신규. Pre-Sprint Sync Check + Contract + Implement + QA + Commit + Push 6단계, 5 체크포인트마다 사용자 확인.
- **Gap 4 — `/refactor-checklist` 스킬** (Quick Win "/refactor-widget anti-AI-tone 체크리스트"): harness/skills/refactor-checklist/SKILL.md 신규. 이름은 stack-agnostic 하게 일반화. 편집 절대 안 하고 체크리스트만 산출.
- **Gap 5 — PreToolUse 가드 패턴** (agent guide 보강): agent-design-guide §6 패턴 7 끝에 PostToolUse 의 보완 패턴으로 PreToolUse 3 영역 (Origin Sync / 좀비 / 보호 브랜치) 명시.
- **Gap 6 — Flutter-Figma SSIM 자가검증 루프** (야심찬 워크플로우 "5h+ Figma parity 작업의 measurable optimization reframe"): flutter-toolkit/references/figma-parity-self-verify.md 신규. 5-step loop (capture → ssim → diff → param adjust → re-measure → 수렴), 위젯별 파라미터 chain, 한 번에 한 파라미터 attribution 보전.

### 버전 업데이트

| 플러그인 | 이전 → 이후 |
| --------- | ------------- |
| harness | 0.4.1 → 0.4.2 (스킬 2개 추가, 가이드 보강) |

### 자기 모순 인정 (이번 사이클의 self-application 결과)

- 첫 번째 PR (PR #8) 진행 중 사용자 확인 없이 main 직접 push → Scope-Bound Edits Hard-stop 사례. 본 followup 사이클이 같은 anti-pattern 을 가이드/훅으로 명문화.
- 카이젠 시작 직전 git fetch 안 함 → Pre-Sprint Sync Check 위반. PreToolUse Origin Sync 가드가 다음 사이클부터 자동 경고.

### 다음 사이클 백로그

- HTML extracted text 의 가독성 추가 개선 (현재는 모든 텍스트를 단일 흐름으로 추출 — 섹션 구조 보전 가능)
- /sprint 스킬에 evaluator REJECT → iteration 자동 카운트 + 3회 한계 escalation
- /refactor-checklist 의 스택별 규칙 자동 로드 로직 확장 (현재는 reference 명시만, 실제 자동 로드는 미구현)

---

## [2026-05-07] — kaizen cycle (Phase 1~12, /insights 산출물 자동 통합 파이프라인 구축)

### 요약

12-Phase 카이젠. **이번 사이클의 "/insights" 부분은 스킬 실행이 아니라 산출물 활용 + 자동 통합 파이프라인 구축** 이다. `/insights` 슬래시 커맨드 자체는 Claude Code CLI 사용자 직접 실행 명령으로, 메인 세션이 invoke 할 수 없다. 따라서 (1) 13일 전 사용자가 생성해둔 `.claude/kaizen-input/insights-report.md` (mtime 2026-04-24) 를 입력으로 사용하고, (2) 다음 사이클부터 동일 경로의 신선한 산출물이 자동 통합되도록 `collect-kaizen-data.py` 에 자동 탐색 로직을 영구 추가했다. 신규 Phase 12 (reflect-kit) 가 정식 카이젠 대상에 포함되어 11→12 Phase 확장. Phase 1 가이드 v1.2.0 → v1.3.0 신규 원칙 5 건 도출 후 Phase 2~12 에 cross-surface parity 매트릭스로 전수 적용.

### `/insights` 산출물 자동 통합 (Step 0 확장)

- `scripts/collect-kaizen-data.py` 에 `collect_insights_report()` 신규 — `<repo>/.claude/kaizen-input/insights-report.md` → `~/.claude/kaizen-input/insights-report.md` 자동 탐색 (60일 stale 경고)
- 데이터 풀 §0 신규 — 모든 Phase subagent 최우선 참조 섹션
- 데이터 풀 §6 매핑 표 — 12 Phase 모두 §0 우선
- orchestrator SKILL.md Step 0 Gotchas 6 건 추가
- **이번 사이클 사용 산출물:** 13 일 전 (2026-04-24 자) 생성된 insights-report.md. fresh `/insights` 는 사용자가 다음 사이클 전에 CLI 에서 직접 재실행 권장 (60일 STALE 임계 미만이라 자동 차단은 안 됨)

### Phase 별 변경

- **Phase 1 (skill-design-guide v1.3.0, agent-design-guide v1.3.0)**: 5 건 신규 원칙 — Pre-Edit Batch Audit (Friction #1+#2), Pre-Sprint Sync Check (Pattern #2), Session Lifecycle 카테고리 (Feature #1), Hook-Triggered Auto-Correction 패턴 7 (Feature #2), Self-Evaluator Rule-by-Rule Audit gotcha. §11 Cross-Surface Parity 표 5 → 8 행 확장.
- **Phase 2 (contract-design-guide v3.1, sprint-contract)**: Friction #2 흡수 — Pre-Edit Batch Audit 의 계약-시점 적용 cross-reference. Gotcha 1 건.
- **Phase 3 (qa-evaluation-guide v3.1, qa-evaluator)**: Step 3.5 Self-Evaluator Audit 신규 (verdict 직전 의무).
- **Phase 4 (kaizen-orchestrator SKILL.md)**: Phase 12 reflect-kit 전수 누락 보정 + failure-count.yaml phase_12.
- **Phase 5~12 (각 kit)**: cross-kit-principles 매트릭스 SSOT 도입. 각 kit README cross-reference. 8 kit 일괄. react-kit Library Policy 보존.

### 버전 업데이트

| 플러그인 | 이전 → 이후 |
| --------- | ------------- |
| harness | 0.4.0 → 0.4.1 |
| flutter-toolkit | 0.5.2 → 0.5.3 |
| design-kit | 0.2.2 → 0.2.3 |
| backend-kit | 0.1.2 → 0.1.3 |
| infra-kit | 0.1.2 → 0.1.3 |
| rust-kit | 0.1.2 → 0.1.3 |
| react-kit | 0.1.2 → 0.1.3 |
| planning-kit | 0.3.0 → 0.3.1 |
| reflect-kit | 0.3.0 → 0.3.1 (Phase 12 첫 카이젠 포함) |

### Sprint Contract 자기평가

DG-01~07 7건 전수 PASS. Phase 1 신규 5 건 cross-reference 검증 완료.

### Meta-issues — 이번 사이클 재발 없음

이전 (2026-04-24) 5 건 meta-issue 해소 유지. 신규 meta-issue 는 audit-log 별도 append.

---

## [2026-04-24] — kaizen cycle (Phase 1~11)

### 요약

11-Phase 카이젠 전 사이클 완료. 30일치 `/insights` 리포트 + 138 evaluator 피드백 + 1798 reflections + 5개 외부 프로젝트 QA 데이터를 기반으로 전수 개선.

### Phase별 변경

- **Phase 1 (skill-design-guide v1.2.0, agent-design-guide v1.2.0)**: Rule-by-Rule Audit, Substring containment 트리거, Enumerate-before-Act, Code Examples 품질, Sibling Consistency, Long-Running Skills 체크포인트, Cross-Surface Parity Checklist, Binary Decidability Pre-Check, Unverifiable 3항 (총 11개 신규 원칙)
- **Phase 2 (contract-design-guide v3, sprint-contract, contract-schema v3)**: Scope Range 인라인 명시, Verification Method 3단계 fallback, Sibling enumerated 검증, `[미검증]` 마커 정책
- **Phase 3 (qa-evaluation-guide, qa-evaluator)**: Binary Decidability Pre-Check (Step 1.5), Rule-by-Rule Audit, `[미검증]` 2건 자동 REJECT, Sibling Enumerated Verification, L3 Coverage Honesty, User-Value/Business-Intent 관점
- **Phase 4 (harness 6 support skills)**: create-skill/create-agent/init/*-kaizen에 Phase 1~3 원칙 전수 주입
- **Phase 5 (flutter-toolkit 18 skills)**: Sibling Consistency (widget/screen/feature), Stack vs Column 의사결정 트리, Riverpod 3.0.2·Freezed 3·go_router 17.2.2 Context7 출처 반영
- **Phase 6 (design-kit 8 skills + reviewer)**: 5 REJECT 해소 (자동 로드 Step 0 독립, modified 예외, HTML 산출물 명시), CONDITIONAL APPROVE 판정
- **Phase 7 (backend-kit 4 skills + reviewer)**: 5 REJECT 해소 (README/evals/Step 3/References), ER-01 run-evals exit 2, Outbox/CB/OAuth 2.1 sibling
- **Phase 8 (infra-kit 4 skills + reviewer)**: 5 REJECT 해소, Kubernetes PSA·Terraform 1.10+·OTel Rule-by-Rule 표
- **Phase 9 (rust-kit 17 skills + reviewer)**: 4 REJECT 해소 (PgPool→trait DI, Composition Root, 리서치 수 통일), Sibling rust↔backend 3-pair parity
- **Phase 10 (react-kit 21 skills + 3 agents)**: 4 REJECT 해소 (TODO 템플릿 정책, Zustand/Query/Hook Form 3-way 상태 분리, Trigger substring 제거), Library Policy 원칙 보존
- **Phase 11 (planning-kit 10 skills + reviewer)**: Phase 1~10 누적 원칙 흡수 (예방적 감사), 12-카테고리 통일, 4-way verdict + CONDITIONAL + NEEDS_VERIFICATION

### 버전 업데이트

| 플러그인 | 이전 → 이후 |
| --------- | ------------- |
| harness | 0.3.6 → 0.4.0 (minor — guides v1.2.0 + schema v3) |
| flutter-toolkit | 0.5.1 → 0.5.2 |
| design-kit | 0.2.1 → 0.2.2 |
| backend-kit | 0.1.1 → 0.1.2 |
| infra-kit | 0.1.1 → 0.1.2 |
| rust-kit | 0.1.1 → 0.1.2 |
| react-kit | 0.1.1 → 0.1.2 |
| planning-kit | 0.2.0 → 0.3.0 (minor — 12-category + 4-way verdict) |

### 메트릭

- 전체 REJECT 이력 해소: 22건 (design-kit 5 + backend-kit 5 + infra-kit 5 + rust-kit 4 + react-kit 4 + harness 다수)
- 각 Phase QA verdict: APPROVE (11/11)
- validate-plugin.py: 9/9 OK
- docs-site 재생성: 5 HTML (harness guides + contract-schema v3)

### Meta-issues (Step 0.5 audit log 기준)

이전 사이클(2026-04-11) meta-issues 3건 모두 이번 사이클에서 재발 없음:

- ✅ docs-site 재생성 Step 11.5 실행됨
- ✅ per-kit research-log 필요 시 생성 (해당 없음)
- ✅ flutter-changelog 갱신 (해당 없음, Phase 5 변경만)

# Kaizen Changelog

> harness-kaizen 스킬이 적용한 모든 변경의 이력.
> 각 엔트리는 버전, 변경 유형, 연구 근거, Before/After를 포함한다.

---

<!-- 엔트리는 최신순으로 추가 -->

## [2026-04-12] - kaizen research-log 확충 + Phase 1~10 카이젠

### 변경 유형: minor (355개 소스 기반 리서치 확충 + 전 Phase 카이젠)

### 변경 범위

- **리서치 확충**: 6개 kit research-log 200줄+로 확충 (Claude+Codex 교차검증, 355소스)
- **자동화 성숙도**: 23/35(66%)→32/35(91%), 5개 영역 5/5 달성
- **Phase 2 (Contract)**: 경계값 측정법, 스코프 세분화 GAP 추가
- **Phase 3 (Evaluator)**: 수량/경계값 조건 검증 프로토콜 추가
- **Phase 4 (Harness)**: init.sh sed -i 크로스 플랫폼 버그 수정
- **Phase 5 (Flutter)**: 9스킬 Gotchas (Riverpod 3.0, Dart macros 중단, Impeller 등)
- **Phase 6 (Design)**: 6스킬 (APCA, DTCG $extends, Container Queries, Fluid Typography)
- **Phase 7 (Backend)**: 8파일 (FAPI 2.0, Passkeys, OTel Logs GA, Kafka 4.x, Modular Monolith)
- **Phase 8 (Infra)**: 7파일 (K8s 1.35, Cilium eBPF, EU CRA SBOM, Cost Optimization)
- **Phase 9 (Rust)**: 12스킬 (Rust 2024, Axum 0.8, SeaORM, async closures, cargo-mutants)
- **Phase 10 (React)**: 15파일 (React Compiler v1.0, Vite Rolldown, View Transitions, animate.css 금지)

### 인프라 개선

- kaizen-state.yaml 자동 갱신 (spawn/finalize 연동)
- validate-post-kaizen.py FAIL 힌트 14개 추가
- finalize-phase.sh --auto-revert 플래그 추가
- settings.json PostToolUse에 validate-plugin + docs-site 알림 훅 추가

---

## [2026-04-11] - kaizen research-mode rerun (Phase 1~10 + Final)

### 변경 유형: minor (2026 최신 생태계 반영 전면 카이젠)

### 변경 범위

7개 플러그인 전체를 2026-04-11 기준 공식 문서/릴리스 노트/학술 논문 리서치 기반으로 갱신. Phase 1~10 각 단계별 독립 qa-evaluator 서브에이전트 평가로 197/199 조건 PASS.

- **harness v0.3.5 → v0.3.6**: skill/agent design guide에 Anthropic 공식 2026 패턴 반영, LLM-as-judge 2026 연구(arxiv 12건) 기반 평가 방법론 재설계, contract-design-guide 네이밍 태그 전환(L1/L2/L3 → [exact]/[structural]/[goal]), Aggregation Mode([enumerated]/[collective]) 도입, feedback-schema 누적 분석 필드 확장.
- **flutter-toolkit v0.5.0 → v0.5.1**: Riverpod 3.0 Notifier 라이프사이클 + Freezed 3.0 sealed switch expression + go_router StatefulShellRoute preload + Flutter 3.29 context.mounted async gap + Makefile monorepo 감지.
- **design-kit v0.2.0 → v0.2.1**: Tailwind v4 OKLCH 기본 팔레트, DTCG v1 stable (2025-10-28), WCAG 2.2 신규 SC 8건 (SC 2.5.8 24×24 터치타겟 등), Container Queries Baseline, Material 3 Expressive, SK-06 재발 방지 검증 명령.
- **backend-kit v0.1.0 → v0.1.1**: Hexagonal/Clean/DDD 2026 실무 + 하이브리드 API 경계 기준 + OpenAPI 3.1 + AsyncAPI 3.0 + RFC 9700 OAuth 2.1 BCP + DPoP/mTLS sender-constrained + Outbox relay batch + Pact v4 + Testcontainers.
- **infra-kit v0.1.0 → v0.1.1**: Kubernetes PSA restricted + Gateway API + Sidecar native(v1.33 GA), Terraform 1.10+ ephemeral + test framework + OpenTofu state encryption, Supply Chain 신규 섹션 (SLSA + Cosign + Syft + Trusted Publishers + Falco), OpenTelemetry 3 signals stable, GitOps(Argo CD/Flux) + Platform Engineering.
- **rust-kit v0.1.0 → v0.1.1**: Rust 2024 edition 기본, Axum 0.8 `{id}` 경로 + `async_trait` 제거, SQLx 0.8 + SeaORM 1.1 이중 지원 + MockDatabase 테스트, Tonic 0.13, Clippy 2026 lint 세트 (workspace.lints SSOT), cargo-deny v2, Consumer-Owned Port + Composition Root 단일화 + Domain event/outbox 패턴.
- **react-kit v0.1.0 → v0.1.1**: React 19 stable (ref as prop + Actions), TanStack Query v5 object-form + queryOptions, Tauri 2 GA ACL `core:default`, Tailwind v4 `@theme` + OKLCH, Vite 8 Rolldown, Zustand v5 useShallow 강제, Lingui v5 macro split, Zod v4 + RHF 호환성 workaround, WCAG 2.2 SC 2.5.8 24×24 터치타겟, 라이브러리 0개 원칙 강화 (animate.css 추가).

### QA 결과

- Phase 1 APPROVE 23/23, Phase 2 APPROVE 29/29, Phase 3 APPROVE 27/27, Phase 4 APPROVE 22/22, Phase 5 APPROVE 16/16, Phase 6 APPROVE 28/29, Phase 7 APPROVE 32/32, Phase 8 APPROVE 40/40, Phase 9 APPROVE 29/29 (iter2), Phase 10 APPROVE 22/22, Final APPROVE 10/10.
- validate-plugin: 7 plugins, 7 OK, Exit 0 (전 Phase 유지)
- sync-docs --check-only: 모든 README 동기화 상태

### 주요 리서치 소스 (research-log.md 참조)

공식 문서: Anthropic skill best practices, React 19 blog, Tauri 2.0 stable, Tailwind v4, W3C DTCG v1 Final Report, W3C WCAG 2.2, Kubernetes PSA docs, Terraform/OpenTofu docs, Axum/SQLx/SeaORM changelogs, TanStack Query v5 migration. 학술: arxiv 2412.05579 (LLMs-as-Judges Survey), 2506.13639 (LLM-as-Judge Reliability), 2510.24358 (AAA Benchmarking), 2506.10467 (Multi-Agent Spec), 2411.15594 (LLM-as-Judge Survey), 2410.21819 (Self-Preference Bias), 2506.22316 (Scoring Bias), 2602.05125 (Recursive Rubric Decomposition), 2403.18771 (CheckEval).

---

## [2026-04-10] - kaizen Phase 1~10 + Final (전체 9 Phase 오케스트레이션)

### 변경 유형: patch (code-fence, gotchas, guides, disambiguation)

### 변경 범위

- **Phase 1** (a925a31): kaizen-orchestrator Step 0 pre-flight 데이터 수집
- **Phase 2** (0af5ecc): contract-design-guide 구체성 레벨 [L1/L2/L3] + 예외 조항 패턴 추가
- **Phase 3** (1f73810): qa-evaluator L1~L3 검증 깊이 vs 계약 구체성 레벨 용어 분리 + set intersection 키워드 배타성 절차 추가
- **Phase 4** (07c6074): harness README/create-skill/init bare code fence 7건 언어 힌트 추가
- **Phase 5** (6a43a5e): flutter-toolkit Gotchas 강화 + cross-kit disambiguation
- **Phase 6** (31808d4): design-kit bare fences 7건 수정 + Gotchas 강화
- **Phase 7**: SKIPPED (backend-kit — 이번 카이젠 범위 외)
- **Phase 8** (a45a7b7): infra-kit bare fence 수정 + references 디렉토리 생성
- **Phase 9** (ec00e20): rust-kit bare fences + todo!() false positive fix + fit-pal monorepo insights
- **Phase 10** (6ded56a): react-kit bare fence 수정 + 세션 REJECT 패턴 공통 Gotchas 문서화
- **Final** (이번): harness V5 (TODO→미완성 마커) + V6 (bare fence line 86) residue 해결

### 핵심 개선

- 전체 7 플러그인 validate-plugin: ERROR 0 (before: 1 ERROR harness), WARNING은 cross-kit 허용 케이스
- Phase 2↔3 L 기호 충돌 해소: 계약 구체성 레벨 [L1/L2/L3] vs evaluator 검증 깊이 L1~L3 용어 분리 명시
- react-kit 라이브러리 0개 원칙 회귀 없음 확인

## [0.3.5] - 2026-03-30 (evaluator-kaizen)

### 변경 유형: patch (guide, agent-prompt)

### 연구 기반

- [A Survey on LLM-as-a-Judge](https://arxiv.org/abs/2411.15594) — LLM 판정자 편향 분류 + 완화 전략 체계
- [CheckEval: Robust Evaluation Framework](https://arxiv.org/abs/2403.18771) `EMNLP 2025` — Boolean 체크리스트 분해로 평가자 간 일치도 0.45 향상
- [Understanding LLM-Driven Test Oracle Generation](https://arxiv.org/abs/2601.05542) `AIware 2025` — LLM이 구현을 정답으로 추종하는 편향 발견
- [A Statistical Approach to Model Evaluations](https://www.anthropic.com/research/statistical-approach-to-model-evals) (Anthropic) — 평가 신뢰도 측정 통계적 프레임워크

### 변경 내역

- **docs/guides/qa-evaluation-guide.md**: 편향 테이블 3개 → 6개로 확장
  - Before: 위치 편향, 장황함 편향, 자기강화 편향 (3개)
  - After: + 구체성 편향, 구현 추종 편향, 지시 해석 불일치 (6개). 각 편향별 완화 전략 명시
  - 근거: [LLM-as-a-Judge Survey](https://arxiv.org/abs/2411.15594), [Test Oracle Generation](https://arxiv.org/abs/2601.05542)
- **docs/guides/qa-evaluation-guide.md**: 구현 추종 편향 경고 blockquote 추가
  - Before: 구현 추종 편향에 대한 명시적 경고 없음
  - After: LLM이 코드를 읽을 때 구현을 정답으로 추종하는 편향 경고 + 출처 URL 포함
  - 근거: [Test Oracle Generation](https://arxiv.org/abs/2601.05542)
- **docs/guides/qa-evaluation-guide.md**: CheckEval 3단계 분해 프로토콜 체계화
  - Before: 단일 예시만 제공 ("로그인 실패 시 HTTP 401")
  - After: 3단계 프로토콜 (Aspect Selection → Checklist Generation → Boolean Evaluation) + 복합 조건 분해 예시 + 적용 기준
  - 근거: [CheckEval](https://arxiv.org/abs/2403.18771)
- **docs/guides/qa-evaluation-guide.md**: "판정 신뢰도 평가" 섹션 신설
  - Before: 판정 확신도에 대한 가이드라인 없음
  - After: 확신도 3단계(높음/중간/낮음) 테이블 + 규칙 + Specification-First 검증 순서 원칙
  - 근거: [Anthropic Statistical Approach](https://www.anthropic.com/research/statistical-approach-to-model-evals), [Test Oracle Generation](https://arxiv.org/abs/2601.05542)
- **harness/agents/qa-evaluator.md**: Specification-First 원칙을 Step 2에 추가
  - Before: 검증 순서에 대한 명시적 지침 없음
  - After: "코드를 보기 전에 각 조건의 기대 행동을 먼저 확립한다" 원칙 명시
  - 근거: [Test Oracle Generation](https://arxiv.org/abs/2601.05542)
- **harness/agents/qa-evaluator.md**: 복합 조건 분해(CheckEval) 프로토콜 참조 추가
  - Before: 복합 조건에 대한 체계적 분해 가이드 없음
  - After: CheckEval 프로토콜 4단계 요약 + qa-evaluation-guide.md 상세 참조
- **harness/agents/qa-evaluator.md**: Red Flags + Rationalization Table에 구현 추종 편향 항목 추가
  - Before: 구현 추종 편향에 대한 변명 차단 없음
  - After: "코드가 이렇게 동작하니까 맞다" 변명 차단 + Red Flag 항목 추가

### 버전 판단 근거
> 편향 테이블 확장, 분해 프로토콜 체계화, 확신도 체계 추가는 기존 판정 로직의 구조를 변경하지 않고 가이드라인을 보강한 것이므로 patch bump

---

## [0.3.4] - 2026-03-30 (contract-kaizen)

### 변경 유형: patch (guide, skill-prompt)

### 연구 기반

- [Spec-driven development](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices) `[blog]` — semi-structured specs가 LLM 할루시네이션 감소
- [SpecFix: Automated Repair of Ambiguous Problem Descriptions](https://arxiv.org/abs/2505.07270) `[preprint]` — 문제 기술의 43.58%에 수정 가능한 모호성 존재
- [ATDD for Claude Code](https://github.com/swingerman/atdd) `[community]` — External Observables Only 원칙 (구현 누수 방지)
- [Given-When-Then Acceptance Criteria Guide](https://www.parallelhq.com/blog/given-when-then-acceptance-criteria) `[blog]` — NFR 누락이 일반적 안티패턴

### 변경 내역

- **docs/guides/contract-design-guide.md**: "외부 관찰 가능성" 섹션 신규 추가
  - Before: 조건에 구현 상세 포함 여부를 점검하는 가이드라인 없음
  - After: 금지 요소 목록(클래스명/메서드명/DB명/프레임워크 용어) + 좋은 예/나쁜 예 제시
  - 근거: [ATDD for Claude Code](https://github.com/swingerman/atdd)
- **docs/guides/contract-design-guide.md**: GWT 적용 기준 명확화
  - Before: "모든 조건에 강제는 아니지만" (선택 사항)
  - After: 복잡도 중간 이상 필수, 단순은 권장. 반구조화 조건이 할루시네이션 감소
  - 근거: [Thoughtworks SDD](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)
- **docs/guides/contract-design-guide.md**: 모호성 분류 체계 추가
  - Before: "ambiguous_conditions" 체크만 존재, 구체적 분류 없음
  - After: 어휘적/구문적/의미적 3단계 모호성 분류 + 예시 + 수정 방법
  - 근거: [SpecFix](https://arxiv.org/abs/2505.07270)
- **docs/guides/contract-design-guide.md**: 안티패턴 테이블에 2개 추가 (구현 누수, NFR 누락)
- **docs/guides/contract-design-guide.md**: 진단 체크리스트에 2개 추가 (implementation_leakage, nfr_coverage)
- **harness/skills/sprint-contract/SKILL.md**: Gotchas 3개 추가 (구현 누수, GWT 필수화, NFR)
- **harness/skills/sprint-contract/SKILL.md**: 자기진단 체크리스트에 2개 항목 추가

### 버전 판단 근거
> Gotchas 추가와 설계 가이드 보완은 기존 동작을 변경하지 않으므로 patch bump

---

## [0.3.3] - 2026-03-30

### 변경 유형: patch (guide, skill-prompt, agent-logic)

### 연구 기반

- [Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices) — "Give Claude a way to verify its work"가 단일 최고 레버리지 행동
- [Agentic AI Coding: Best Practice Patterns](https://codescene.com/blog/agentic-ai-coding-best-practice-patterns-for-speed-with-quality) — Multi-Level Code Safeguards (3단계 검증)
- [agentic-code](https://github.com/shinpr/agentic-code) — "LLMs cannot reliably review their own outputs within the same context"

### 변경 내역

- **docs/guides/skill-design-guide.md**: Section 3.5 "검증 가능한 성공 기준을 제공하라" 추가
  - Before: 검증 관련 원칙 없음
  - After: 스킬별 검증 기준 예시 테이블 + 자가 검증 흐름 추가
  - 근거: [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)
- **harness/skills/sprint-contract/SKILL.md**: Gotchas에 다단계 검증 시점 항목 추가
  - Before: 검증 시점 관련 Gotcha 없음
  - After: "가능하면 다단계 검증 시점을 조건에 반영해라" Gotcha 추가
  - 근거: [CodeScene](https://codescene.com/blog/agentic-ai-coding-best-practice-patterns-for-speed-with-quality)
- **harness/agents/qa-evaluator.md**: Rationalization Table에 self-review 편향 경고 추가
  - Before: Generator self-review 관련 변명 차단 없음
  - After: "Generator가 자가 검증했으니 PASS" 변명 차단 항목 추가
  - 근거: [agentic-code](https://github.com/shinpr/agentic-code)

### 버전 판단 근거
> Gotchas 추가와 설계 가이드 보완은 기존 동작을 변경하지 않으므로 patch bump
