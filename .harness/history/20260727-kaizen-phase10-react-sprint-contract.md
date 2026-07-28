# Sprint Contract — Kaizen Phase 10 (react-kit)

Feature: Phase 1~4 신규 원칙(Completion Evidence Gate · Canonical Unverified-Evidence Protocol · Evidence Validity Gate · Counterpart Enumeration) react-kit 전수 정합화
Created: 2026-07-27
Branch: kaizen/2026-07-27
Signal: **LOW** (사용자 외부 프로젝트에 React/Tauri 사용 흔적 0건 · 글로벌 feedback react 언급 4건 대부분 부수적)
Scope: react-kit/skills/*, react-kit/agents/*, react-kit/references/*, .claude/skills/react-kaizen/SKILL.md, docs/react/research-log.md

## 왜 LOW signal 인데 CHANGED 인가

억지 변경이 아니다. 아래 3 건은 **상위 Phase 가 남긴 하위 전파 지시**이며, react-kit 이 유일하게
미이행 상태다 (Phase 3 실측 인용: "`react-reviewer` 는 이 조항 자체가 아예 없다").

1. Phase 3 `qa-evaluation-guide.md` v4.0 §하위 전파 대기 — `*-kit/agents/*-reviewer.md` 6 종 중
   react-reviewer 만 §Canonical Unverified-Evidence Protocol 조항 **0 건**.
   실측: `grep -rn "미검증" react-kit/` → 0 hit.
2. Phase 3 명시 지시 — §Evidence Validity Gate 는 "UI 를 다루는 design/react/flutter 계열이 가장
   직접 매핑된다". react-kit UI 스킬 5 종의 검증 섹션은 `Strict TS 검증` 뿐이고 렌더 증거 규약 0 건.
3. Phase 1 `skill-design-guide.md` §5.5 Counterpart Enumeration — react-kit 은
   Enumerate-before-Act(producer 자기 레이어 스캔) 9 스킬만 있고 consumer 측 열거는 0 건.
   실측: `grep -rn "Counterpart\|양면" react-kit/` → 0 hit.
4. Phase 4 지시 — react-kaizen SKILL.md 의 "7 카테고리" 표기 → 8 (V1~V8) 정정.

## Completion Criteria

### Category: CP (Canonical Protocol 전파 — Phase 3 소관 이관분)

- [ ] **CP-01**: `react-kit/agents/react-reviewer.md` 에 §Canonical Unverified-Evidence Protocol
  5 조항을 **문구 변형 없이** 신설한다. 정본은
  `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol.
  조항 1 의 마커 동의어 목록(`미확인`/`N/A`/`TBD`/`unverified`)은 **전부 백틱으로 감싼다**
  (validate-plugin V5 백틱 인식 회피). 임계값·마커 의미를 react-reviewer 안에서 재정의하지 않는다.
  검증: `grep -c '미검증' react-kit/agents/react-reviewer.md` ≥ 5 이고 임계값 표기가 `2` 단일.
- [ ] **CP-02**: react-reviewer 출력 포맷(`yaml` 블록)에 `unverified:` 집계 필드를 추가한다.
  건별로 `category` / `rule` / `reason` / `fallback` 4 키를 갖는다. 조항 5(집계 의무) 대응.
- [ ] **CP-03**: `react-kit/skills/react-audit/SKILL.md` Report Format 에 `🔍 미검증 (<N>)` 섹션과
  Rules 에 미검증 임계 2 건 REJECT 규칙을 추가한다 (reviewer 출력의 수신면 — 없으면 조항 5 가
  audit 리포트에서 소실된다). 임계값은 재정의하지 않고 정본을 인용한다.
- [ ] **CP-04**: `[미검증]` 이외 동의어 마커를 react-kit 전체에 신규 도입하지 않는다.
  검증: `grep -rnE '\[(미확인|unverified|TBD)\]' react-kit/` → 0 건.

### Category: EV (Evidence Validity Gate — 렌더 증거 규약)

- [ ] **EV-01**: `react-kit/references/render-evidence-protocol.md` 를 신설한다. react-kit 의
  렌더·런타임 증거 SSOT. **임계값/마커/등급을 재정의하지 않고** 상위 SSOT 3 개를 앵커로 인용한다
  (qa-evaluation-guide §Canonical Unverified-Evidence Protocol · §Evidence Validity Gate ·
  skill-design-guide §3.7). enforcement 등급은 **E2**(체크리스트 아티팩트) 로 명시.
  Phase 5 flutter `visual-evidence-protocol.md` · Phase 6 design `visual-change-protocol.md` 와
  동일 계열 파일이며 킷 간 구조 일관성을 유지한다.
- [ ] **EV-02**: EV-01 문서는 react 고유의 **공허한 증거(vacuous pass) 4 유형**을 실제 도구 동작
  근거와 함께 명시한다. 일반론 반복 금지 — 아래 4 개는 조회한 공식 문서에 근거한다:
  (a) `queryBy*` 가 `null` / `queryAllBy*` 가 `[]` 를 반환하는 부재 단정 — 컴포넌트가 애초에
  렌더 실패해도 통과, (b) Vitest `--passWithNoTests` (기본 `false`) 를 켠 0 테스트 green run,
  (c) Vitest `allowOnly` 기본값 `!process.env.CI` — 로컬에서 `.only` 1 개만 돈 green run,
  (d) Playwright `toHaveScreenshot()` 를 `--update-snapshots` 로 갱신해 **빈 화면을 baseline 으로
  고정**한 자기충족 통과.
- [ ] **EV-03**: 렌더 결과가 산출물인 UI 스킬 **5 종 전수**에 EV-01 을 참조하는 Gotcha 를 1 개씩
  추가한다: `react-screen` · `react-widget` · `react-skeleton` · `react-responsive` ·
  `react-animation`. Phase 5 flutter 가 지정한 5 종(widget/screen/skeleton/transition/responsive)의
  react 대응이며 부분 적용을 만들지 않는다.
  검증: `grep -l 'render-evidence-protocol' react-kit/skills/*/SKILL.md` 결과가 위 5 종 + react-test 를 포함.
- [ ] **EV-04**: `react-kit/skills/react-test/SKILL.md` Gotchas 에 EV-02 (a)~(d) 를 측정 측 규칙으로
  추가한다. 테스트를 **작성하는** 스킬이 vacuous 통과를 만드는 지점이므로 생성 측 짝이 필요하다.
  bad → good 대조를 포함한다 (common-gotchas G6 준수).
- [ ] **EV-05**: `react-kit/references/common-gotchas.md` 에 G11 로 EV-01 포인터를 추가한다.
  내용 중복 금지 — 3~6 줄 포인터만. common-gotchas 는 킷 인덱스 역할을 유지한다.

### Category: CE (Counterpart Enumeration — Friction #4)

- [ ] **CE-01**: `react-kit/skills/react-api/SKILL.md` 에 Counterpart Enumeration Gotcha 를
  추가한다. producer(datasource/model/repository/usecase) 변경 시 consumer 측
  (`presentation/**/hooks/use*.ts` 쿼리 훅 · `react-hook-form` 스키마 · 컴포넌트 렌더 지점) 을
  **편집 전에 경로로 열거**하고 체크리스트로 남긴다. 기존 Gotcha 11(Enumerate-before-Act) 을
  대체하지 않고 **반대 방향**임을 명시한다.
- [ ] **CE-02**: `react-kit/skills/react-query/SKILL.md` 에 queryKey 팩토리 변경의 consumer 열거
  Gotcha 를 추가한다. 근거: `invalidateQueries` 는 **prefix 매칭이 기본**이므로 key 배열 앞부분을
  바꾸면 mutation 쪽 무효화 blast radius 가 조용히 변한다. TanStack 공식 문서는 팩토리 정합성
  가이드를 제공하지 않으므로 킷이 규정해야 한다.
- [ ] **CE-03**: CE-01/CE-02 는 enforcement **E2**(열거 결과를 체크리스트 아티팩트로 제출) 로
  기술한다. "확인한다" 수준의 E1 문장으로 끝내지 않는다 (skill-design-guide §5.5 절차 2 항).

### Category: LP (Library Policy — 완화 0건 · 강화만 허용)

- [ ] **LP-01**: 금지 라이브러리 12 항목(`motion` `framer-motion` `@dnd-kit/*` `react-spring`
  `react-transition-group` `react-dnd` `react-beautiful-dnd` `gsap` `lottie-react`
  `@formkit/auto-animate` `animate.css` `shadcn-ui`) 의 react-kit 내 언급 수가 **작업 전 baseline
  이상**을 유지한다. baseline (2026-07-27 실측):
  motion 62 / framer-motion 13 / dnd-kit 17 / react-spring 14 / react-transition-group 11 /
  react-dnd 11 / react-beautiful-dnd 10 / gsap 11 / lottie-react 11 / auto-animate 11 /
  animate.css 8 / shadcn-ui 8. `Library Policy` 계열 라인 수 baseline 37.
- [ ] **LP-02**: `❌ FAIL` → `⚠️ WARN` 재분류 0 건. `git diff` 에서 Library Policy 문맥의
  `FAIL`/`❌`/`REJECT` 가 제거된 라인 0 건임을 확인한다.
- [ ] **LP-03**: `react-animation` Gotcha #1 · `animation-architect-react` 금지 목록 ·
  `react-audit` §6 · `common-gotchas` G2/G10 5 개 정전 소스의 목록이 서로 모순 없이 유지된다.

### Category: KZ (react-kaizen 스킬 정정 — Phase 4 지시)

- [ ] **KZ-01**: `.claude/skills/react-kaizen/SKILL.md` Step 7 의 "7 카테고리" → "8 카테고리
  (V1~V8)" 로 정정한다. 검증: `grep -n '7 카테고리' .claude/skills/react-kaizen/SKILL.md` → 0 건.
- [ ] **KZ-02**: Step 6 의 계약 경로를 `.harness/sprint-contract.md` 단일 경로에서
  `.harness/history/<날짜>-...` 형태로 바꾼다 — 병렬 Phase 실행 시 단일 경로는 상호 덮어쓰기를
  일으킨다 (이번 사이클 실측 제약).
- [ ] **KZ-03**: Gotcha 8 (Context7 우선 리서치) 에 **WebFetch fallback** 을 추가한다.
  근거: 이번 사이클 Context7 MCP 가 OAuth 미인증으로 사용 불가했고, 비대화형 세션에서는 OAuth
  플로우를 실행할 수 없다. `common-gotchas.md` G9 도 동일하게 동기화한다 (양쪽 문구 정합).
- [ ] **KZ-04**: scope-creep 판정 기준을 "파일 수" 가 아니라 **unit(관심사) 수** 로 기술한다
  (Phase 4 지시). 해당 표현이 react-kaizen 에 없으면 신규 추가하지 않고 "부재" 로 보고한다.

### Category: RL (Research Log)

- [ ] **RL-01**: `docs/react/research-log.md` 에 `## [2026-07-27] - Phase 10 kaizen` 엔트리를
  추가한다. 조회 URL **최소 5 건** 전문 기재 + 각 URL 이 어느 조건(CP/EV/CE)에 쓰였는지 매핑.
- [ ] **RL-02**: 버전·기본값 서술은 **조회 결과에만** 근거한다. 학습 데이터 기반 버전 단정 0 건.
  조회로 확인하지 못한 항목은 서술하지 않는다.

### Category: I (Integrity)

- [ ] **I-01**: `python3 scripts/validate-plugin.py react-kit` 8 체크(V1~V8) 전부 OK.
- [ ] **I-02**: `git status --porcelain` 에서 아래 경로 외 modified/untracked 0 건 —
  `react-kit/`, `.claude/skills/react-kaizen/`, `docs/react/research-log.md`, `.harness/history/`.
  react-kit 스킬 실행 산출물 예외 목록(common-gotchas G7)은 이번 작업에서 발생하지 않는다
  (문서 편집만 수행).
- [ ] **I-03**: **git 쓰기 명령 0 건**. 병렬 Phase 실행 중이므로 `git add`/`commit`/`tag`/`push`/
  `finalize-phase.sh` 를 호출하지 않는다. 커밋은 오케스트레이터가 직렬 처리한다.
- [ ] **I-04**: 범위 밖 파일 수정 0 건 — `harness/`, 다른 kit, `scripts/`, `marketplace.json`,
  `plugin.json`, `docs/kaizen/changelog.md`, `.claude/skills/kaizen-orchestrator/` 무변경.

## Scope (explicit)

**In scope**:
- `react-kit/skills/*/SKILL.md` (21 종 중 8 종 편집 예정: react-screen · react-widget ·
  react-skeleton · react-responsive · react-animation · react-test · react-api · react-query ·
  react-audit)
- `react-kit/agents/react-reviewer.md`
- `react-kit/references/render-evidence-protocol.md` (신규) · `common-gotchas.md`
- `.claude/skills/react-kaizen/SKILL.md`
- `docs/react/research-log.md`

**Out of scope (엄금)**:
- `harness/` 전체 (Phase 1·3 산출물 — 인용만 하고 수정 금지)
- 다른 kit 전체 · `scripts/` · `marketplace.json` · `plugin.json` · `docs/kaizen/changelog.md`
- `.claude/skills/kaizen-orchestrator/`
- **Library Policy 완화** — 금지 라이브러리 삭제·WARN 재분류·예외 부여 전부 금지
- git 쓰기 명령 전체

## 비목표 (하지 않는 것)

- 새 스킬/에이전트 신설 — 21 + 3 구성 유지
- 기존 Enumerate-before-Act 9 스킬 가드 재작성 (직전 사이클 승격분 · 중복 금지)
- Counterpart Conditions 의 evaluator 측 대응 절 신설 — Phase 3 parity item 12 의 **의도된 부재**
- `react-audit` 6 카테고리를 7 개로 늘리기 — 미검증은 카테고리가 아니라 리포트 축
