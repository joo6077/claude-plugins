# Kaizen Data Pool

Generated: 2026-04-11T18:25:24
Generator: `scripts/collect-kaizen-data.py`

카이젠 오케스트레이션의 Phase 별 서브에이전트가 참조할 통합 데이터 풀이다. 이 파일은 `scripts/collect-kaizen-data.py` 로 재생성된다 — 수동 수정 금지.

## 1. 글로벌 Evaluator Feedback

- 경로: `/Users/jackson/.harness/feedback/evaluator`
- 총 파일: **70**

### Verdict 분포

- **APPROVE**: 42
- **REJECT**: 28

### Skill 분포

- `qa-evaluator`: 70

### Project 분포

- `claude-plugins`: 70

### 최근 REJECT 사유 (Top 20)

- [2026-04-10] **claude-plugins**: SK-06: concept.md Accent 행에 #E8965A 구체 hex 확정값 기재 — Gotcha #3 위반
- [2026-04-10] **claude-plugins**: SK-05: react-run/SKILL.md:5의 트리거 키워드 'wasm-pack 빌드'가 react-wasm/SKILL.md:5와 중복. 기존 17개 스킬과 상호 배타 불충족
- [2026-04-10] **claude-plugins**: SC-02: package.json.template 라이브러리 버전 4건이 ^X.0.0 형식 위반 (^0.4.0, ^0.400.0, ^0.7.0, ^5.5.0)
- [2026-04-10] **claude-plugins**: RE-02: react-api의 트리거 키워드 '"API 연동"'이 react-feature의 '"API 연동 화면"'과 부분 중복 — 배타성 위반
- [2026-04-10] **claude-plugins**: RE-02: 21개 스킬 트리거 키워드 상호 배타 불충족 (react-run vs react-wasm 'wasm-pack 빌드' 겹침)
- [2026-04-10] **claude-plugins**: PU-04: sync-docs.py에서 regex 기반 frontmatter 파싱이 plugin_utils.parse_frontmatter()로 교체되지 않음. _parse_frontmatter_file() 함수가 L45-92에 존재하며 collect_skills/collect_agents에서 계속 사용됨.
- [2026-04-10] **claude-plugins**: PU-04: sync-docs.py가 plugin_utils.parse_frontmatter() (pyyaml 기반) 대신 parse_frontmatter_raw() (regex 기반)를 호출함. 계약이 명시한 함수명 및 구현 방식 불일치.
- [2026-04-10] **claude-plugins**: PH-01: agent-design-guide.md에 계약 모호성 방지 원칙 누락 (skill-design-guide.md §3.5 대응 항목 없음)
- [2026-04-10] **claude-plugins**: KZ-04: react-kaizen References 섹션에 docs/react/kit-design/ 7개 그룹 문서(g1~g6, g5b) 개별 미명시. 폴더 경로 하나로 포괄 처리됨
- [2026-04-10] **claude-plugins**: I-02: Working tree modified 2건 (.harness/sprint-contract.md, .harness/.meta/kaizen-data-pool.md) — 계약 'modified 0건' 미충족
- [2026-04-10] **claude-plugins**: DG-02: react-init/SKILL.md line 178, 190 코드블록 언어 힌트 누락
- [2026-04-10] **claude-plugins**: DG-02: 5개 파일 모두에서 언어 힌트 없는 fenced code block 존재 (react-run 2개, react-build 3개, react-preflight 3개, react-audit 4개+, react-reviewer 6개+)
- [2026-04-10] **claude-plugins**: DG-01: react-feature/SKILL.md(5건)와 react-widget/SKILL.md(2건)에서 코드 템플릿 내 TODO 7건 발견 — 계약 0건 조건 불충족
- [2026-04-10] **claude-plugins**: CD-03: integration.html card-source 0건; 일부 파일 원칙 카드 하단 card-source URL 링크 누락
- [2026-04-10] **claude-plugins**: CD-02: wasm-catalog.html 원칙 카드 없음(callout으로 대체) + Gotchas 체크리스트 없음
- [2026-04-10] **claude-plugins**: CD-02: integration.html 안티패턴 bad·good 비교 없음(compare-bad 0건)
- [2026-04-10] **claude-plugins**: CD-02: integration.html Gotchas 섹션 없음; scaffolding/performance/ui-patterns/wasm-catalog에 bad·good 비교 섹션(compare-bad/compare-good) 없음
- [2026-04-10] **claude-plugins**: CD-02: build-audit.html — compare-bad/compare-good 비교 0건 (테이블 형식으로 대체됨)
- [2026-04-10] **claude-plugins**: CD-02: build-audit.html — Gotchas 체크리스트 섹션(id=gotchas) 없음
- [2026-04-10] **claude-plugins**: AR-03: moodboard.html 필수 7개 섹션 중 5개만 존재 (Texture/Material, Layout Cues, Do/Don't 누락) — Gotcha #9 위반, 최솟값 6개 미충족

### 최근 Improvement Suggestions (Top 15)

- [2026-04-11] **claude-plugins**: scripts/__pycache__/ 를 .gitignore에 추가 권장
- [2026-04-10] **claude-plugins**: 표현 변형이 있는 조건(Layout shift vs 레이아웃 shift)은 계약 작성 시 한국어/영어 병기 권장
- [2026-04-10] **claude-plugins**: 메이저 0 패키지(next-themes, lucide-react, cva)에 대한 버전 정책 명확화 필요
- [2026-04-10] **claude-plugins**: 다음 Phase에서 SKILL.md 추가 시 각 스킬별 트리거/인자 계약 조건 추가 권장
- [2026-04-10] **claude-plugins**: 구체성 레벨 L1/L2/L3 명칭이 qa-evaluator 검증 깊이 L1/L2/L3과 혼용 가능 — 향후 네이밍 충돌 모니터링 필요
- [2026-04-10] **claude-plugins**: 계약 조건 KZ-04가 '개별 명시'와 '포괄 경로' 중 어느 형식을 요구하는지 명시적으로 기술하면 모호성을 줄일 수 있음
- [2026-04-10] **claude-plugins**: 계약 작성 시 특정 함수 이름을 고정하기보다 동작 목표(SSOT, 중복 제거)를 기술하면 구현 유연성이 생김
- [2026-04-10] **claude-plugins**: §3.3 rollback label 'format-check 실패'를 'fix 단계 실패 (prettier/eslint 실행 오류)' 등으로 갱신 권장 (stale after SK-04 fix)
- [2026-04-10] **claude-plugins**: wasm-catalog.html에 card 형식 원칙 섹션과 Gotchas 체크리스트 추가 필요
- [2026-04-10] **claude-plugins**: react-test Gotcha에 cleanup() 자동 동작 항목 추가 검토 (소스 §1.8 기재 있음)
- [2026-04-10] **claude-plugins**: integration.html은 Final 통합 페이지로 성격이 달라 Gotchas 조건 적용 여부를 계약에서 명확히 해야 함
- [2026-04-10] **claude-plugins**: integration.html에 compare-bad/compare-good 안티패턴 비교 섹션 추가 필요
- [2026-04-10] **claude-plugins**: evals.json id 12-15의 description 필드가 비어있음 — assertion 텍스트만 있고 설명이 없어 evals 가독성이 낮다
- [2026-04-10] **claude-plugins**: build-audit.html에 ul.check-list 형식의 Gotchas 섹션 추가
- [2026-04-10] **claude-plugins**: build-audit.html에 compare-bad/good 형식 안티패턴 비교 2쌍 이상 추가

## 2. 외부 프로젝트 (`Hub/10_Dev`) 피드백

- Hub 루트: `/Users/jackson/Hub/10_Dev`
- 발견된 프로젝트: **2**

### `apps`

- 경로: `/Users/jackson/Hub/10_Dev/apps`
- sprint-feedback.md: 136 lines
- history sprint-contracts: 15
- 최근 contracts:
  - 20260411-1339-sprint-contract.md
  - 20260411-1531-sprint-contract.md
  - 20260411-1616-sprint-contract.md
  - 20260411-1656-sprint-contract.md
  - 20260411-1815-sprint-contract.md

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: AdmHtmlEditorWidget 실구현 (html_editor_enhanced 2.7.1 + 피그마 참고 이미지 스타일)
Evaluated: 2026-04-11 21:00
Verdict: APPROVE
Iteration: 4

---

## Results

### UI (6/7)

- [x] UI-01: dev_widget_admin_screen line 417 섹션에 실제 HtmlEditor 위젯 렌더 — PASS [L3]
  - 근거: `dev_widget_admin_screen.dart:417` `const Text('--- 팝업 공지 html 편집기(AdmHtmlEditorWidget) ---')` / `:418-423` `const AdmHtmlEditorWidget(AdmHtmlEditorWidgetProps(hint: '팝업 공지 내용을 입력하세요', height: 400))` — 빈 Container가 아닌 실구현 위젯.

- [x] UI-02: 툴바에서 InsertButtons 계열 7종 완전 제거 — PASS [L3]
  - 근거: `html_editor_widget.dart:78-86` `defaultToolbarButtons: [StyleButtons(), FontSettingButtons(), FontButtons(), ColorButtons(), ListButtons(), ParagraphButtons(), OtherButtons()]` — InsertButtons 클래스 미포함.

- [x] UI-03: 텍스트 효과 버튼 그룹 7개 모두 포함 — PASS [L3]
  - 근거: `html_editor_widget.dart:78-86` StyleButtons / FontSettingButtons / FontButtons / ColorButtons / ListButtons / ParagraphButtons / OtherButtons 전부 기본 생성자.
```

</details>

### `fit-pal`

- 경로: `/Users/jackson/Hub/10_Dev/fit-pal`
- sprint-feedback.md: 109 lines
- history sprint-contracts: 0

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: Monorepo Makefile
Evaluated: 2026-03-30 16:00
Verdict: APPROVE
Iteration: 2

## Results

### Flutter App 커맨드 (15/15)
- [x] app-run (dev, dart-define + observatory-port 포함): PASS
  - 근거: `Makefile:24` — `--dart-define-from-file=.dart_defines.json --observatory-port=8181` 모두 포함. launch.json:13과 일치
- [x] app-run-staging: PASS
  - 근거: `Makefile:29-30`
- [x] app-run-prod: PASS
  - 근거: `Makefile:32-33`
- [x] app-run-profile: PASS
  - 근거: `Makefile:26-27` — launch.json:22(App: Dev Profile)에 observatory-port 없음, Makefile도 동일하게 없음. 일치
- [x] app-test: PASS
  - 근거: `Makefile:39-40`
- [x] app-analyze: PASS
```

</details>


## 3. Followup 문서

- `docs/superpowers/followup-2026-04-11-plugin-validation-findings.md`

## 4. 현재 레포 최근 Sprint Contracts

- `.harness/history/20260411-1327-kaizen-orchestrator-expansion-sprint-contract.md`
- `.harness/history/20260411-1537-docs-site-react-kit-sprint-contract.md`
- `.harness/history/20260411-1632-simplify-refactor-sprint-contract.md`
- `.harness/history/20260411-1649-session-comprehensive-qa-sprint-contract.md`
- `.harness/history/20260411-1725-kaizen-phase1-design-guides-sprint-contract.md`
- `.harness/history/20260411-1733-kaizen-phase2-contract-sprint-contract.md`
- `.harness/history/20260411-1737-kaizen-phase3-evaluator-sprint-contract.md`
- `.harness/history/20260411-1815-phase6-residue-sprint-contract.md`
- `.harness/history/20260411-kaizen-phase6-design-kit-sprint-contract.md`
- `.harness/history/20260411-phase5-flutter-toolkit-sprint-contract.md`

## 6. Phase 별 참조 가이드

각 Phase subagent 는 아래 매핑을 참고하여 자신의 범위에 맞는 섹션을 우선 읽는다.

| Phase | 스킬 | 주요 참조 섹션 |
|-------|------|---------------|
| 1 설계 가이드 | skill-design-guide, agent-design-guide | §1 Improvement Suggestions |
| 2 Contract | contract-design-guide + sprint-contract | §1 Reject 사유 (계약 모호성) |
| 3 Evaluator | qa-evaluation-guide + qa-evaluator | §1 Improvement (L3, set intersection) |
| 4 Harness | harness/skills/* (sprint-contract, qa-evaluator 제외) | §5 validate-plugin 현재 상태 |
| 5 Flutter | flutter-toolkit/skills/* | §2 Hub 외부 프로젝트 (fit-pal, apps) |
| 6 Design | design-kit/skills/* | §5 validate-plugin 현재 상태 |
| 7 Backend | backend-kit/skills/* | §1 Backend 관련 feedback (있다면) |
| 8 Infra | infra-kit/skills/* | §5 validate-plugin 현재 상태 |
| 9 Rust | rust-kit/skills/* | §2 Hub 외부 프로젝트 (fit-pal server) |
| 10 React | react-kit/skills/* | §3 followup-2026-04-11, §5 |

