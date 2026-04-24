# Sprint Contract — Kaizen Phase 10 (react-kit)

Feature: react-kit에 Phase 1~9 신규 원칙 전수 + react-kit 4 REJECT reason 전수 해소
Created: 2026-04-24
Scope: react-kit/skills/*, react-kit/agents/*, react-kit/references/*, .claude/skills/react-kaizen/SKILL.md

## Completion Criteria

### Category: DG (REJECT Resolution)

- [ ] **DG-01**: react-feature/SKILL.md + react-widget/SKILL.md 코드 템플릿 내 "TODO" 문자열 + "구현 대기" 형태 주석 전수 처리. `grep -rn "TODO\|FIXME\|XXX" react-kit/skills/react-feature react-kit/skills/react-widget` 결과 0건. "필요한 ... 추가"/"DTO → Domain 매핑 추가" 형태의 확장 포인트 주석은 Gotchas에 "확장 포인트 주석이지 TODO가 아니다" 명시로 예외 처리.
- [ ] **DG-02**: react-init, react-run, react-build, react-preflight, react-audit SKILL.md + react-reviewer.md 모든 opening fence에 언어 힌트 명시. `python3 scripts/validate-plugin.py react-kit --check=code-fence` 결과 0 bare.
- [ ] **AP-01**: react-form/SKILL.md Gotchas에 "Zustand vs TanStack Query 상태 분리 원칙" 을 독립 항목으로 명시(기존 #9 유지·강화). "서버 상태 = TanStack Query" + "클라이언트 UI 상태 = Zustand" + "폼 로컬 상태 = React Hook Form" 3-way 분리 원칙 기술.
- [ ] **RE-02**: react-api, react-feature 트리거 키워드 substring 중복 제거. "API 연동 화면" 제거/대체. `python3 scripts/validate-plugin.py react-kit --check=triggers` 결과 중복 0건. react-feature와 react-api description에 서로 "~필요하면 트리거하지 않는다" 상호 배타 명시 보강.

### Category: PH (Phase 1~9 원칙 전수)

- [ ] **PH-01**: Phase 1 skill-design-guide §3.5 "계약 모호성 방지" 적용 — react-audit, react-reviewer, react-audit의 Report Format 을 "체크리스트 + 항목별 근거 + 라인 번호" 구조로 통일 (이미 일부 적용됨, 보강).
- [ ] **PH-02**: Phase 2 contract-design-guide "측정 가능한 조건" 적용 — react-audit Rules 에 "모호 표현(대체로/거의/대부분/충분히) 금지" 원칙 명시.
- [ ] **PH-03**: Phase 3 qa-evaluation-guide "L3 verification" 적용 — react-reviewer 핵심 규칙에 "L3 verification: 파일:라인 직접 확인 없이 PASS 금지" 추가.
- [ ] **PH-04**: Phase 4 harness "I-02 예외 목록" 적용 — react-kit common-gotchas에 "I-02 예외: package.json, tsconfig*.json, Tauri capabilities, lingui/src/generated/* 생성물" 명시.
- [ ] **PH-05**: Phase 5 flutter-toolkit "Context7 우선 리서치" 적용 — common-gotchas에 React 19 / TanStack Query v5 / Tauri 2 / Tailwind v4 Context7 조회 우선 원칙 포함.
- [ ] **PH-06**: Phase 6 design-kit "WCAG 2.2 SC 2.5.8 24×24 터치타겟" 적용 — 이미 react-widget / react-audit 에 있음. react-responsive, react-form 에도 동일 원칙 명시 (반응형 breakpoint 내에서 터치타겟 보장).
- [ ] **PH-07**: Phase 7 backend-kit "ER-01 run-evals exit code" 적용 — N/A (react-kit은 run-evals 없음). react-run 에 "비활성 서브커맨드 호출시 exit non-zero" 원칙 이미 존재하므로 유지 확인.
- [ ] **PH-08**: Phase 8 infra-kit "overview 금지 원칙" 적용 — react-audit Report Format 에 "카테고리별 독립 리포트, 통합 overview 금지" 원칙 명시.
- [ ] **PH-09**: Phase 9 rust-kit "Sibling Group N-way parity" 적용 — react-run / react-build / react-preflight 세 스킬의 Gotchas·Report Format·Rules 섹션 구조 동일성 확인·보강.

### Category: LP (Library Policy — 강화만 허용)

- [ ] **LP-01**: react-audit Library Policy 카테고리의 금지 라이브러리 목록 유지·확장. 기존 (`motion`, `framer-motion`, `@dnd-kit/*`, `react-spring`, `react-transition-group`, `react-dnd`, `react-beautiful-dnd`, `gsap`, `lottie-react`, `@formkit/auto-animate`, `animate.css`) 삭제 금지.
- [ ] **LP-02**: animation-architect-react 에이전트의 Tier 판정 시 "라이브러리 0개" 원칙을 명시적 Gate로 재확인.
- [ ] **LP-03**: react-reviewer 핵심 규칙에 "Library Policy 위반은 ⚠️ WARN이 아니라 ❌ FAIL로 분류" 원칙 명시.
- [ ] **LP-04**: references/common-gotchas.md G2 금지 목록과 react-audit §6 동기화 — 양쪽 전부 동일 목록 유지.

### Category: TT (Tier Audit — 3계층)

- [ ] **TT-01 Tier 1 (REJECT 직접)**: react-feature, react-widget, react-form, react-api, react-init, react-run, react-build, react-preflight, react-audit, react-reviewer — 파일별 구체 변경사항 적용 완료.
- [ ] **TT-02 Tier 2 (Phase 원칙 핵심)**: animation-architect-react, widget-inspector-react, react-kaizen, react-kaizen ` references` — Phase 1~9 원칙 반영 감사 완료.
- [ ] **TT-03 Tier 3 (경량 audit)**: react-screen, react-store, react-query, react-wasm, react-tauri, react-error, react-l10n, react-responsive, react-skeleton, react-extract, react-animation, react-test — 경량 감사 완료 (구조적 이슈만 점검).

### Category: I (Integrity)

- [ ] **I-01**: `python3 scripts/validate-plugin.py react-kit` 전체 7 체크 OK.
- [ ] **I-02**: Working tree에 react-kit/, .claude/skills/react-kaizen/, .harness/ 외 modified 0건. (sprint-contract, feedback 파일은 예외).
- [ ] **I-03**: 커밋 메시지 `chore(kaizen-phase10): ...`, trailer 포함.

## Scope (explicit)

**In scope**:
- `react-kit/skills/*/SKILL.md` (21개)
- `react-kit/agents/*.md` (3개)
- `react-kit/references/*.md` (6개, 필요 시)
- `.claude/skills/react-kaizen/SKILL.md`

**Out of scope**:
- docs/react/* (리서치 문서 — 이번 범위 제외, 필요 시 최소 갱신만)
- 다른 플러그인 전체
- Library Policy 완화 (금지 라이브러리 삭제) — 엄격히 금지
- plugin.json version bump (release 스킬 담당)

## Anti-patterns

- ❌ 금지 애니메이션 라이브러리 목록 삭제 또는 "exception" 명목 추가
- ❌ Library Policy를 ⚠️ WARN 으로 완화
- ❌ "TODO" 주석을 그대로 두고 Gotchas에만 예외 명시 (반드시 본문 주석을 변환 후 예외 명시 병행)
- ❌ 범위 밖 플러그인/파일 수정
- ❌ 측정 가능한 조건 대신 "거의", "대체로" 등 모호 표현 사용
