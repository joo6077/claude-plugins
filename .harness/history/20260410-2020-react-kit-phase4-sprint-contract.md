---
feature: "react-kit Phase 4: G3 Performance Skills (2종)"
created: "2026-04-10T20:10:00+09:00"
complexity: "복잡"
conditions: 14
scope: "react-kit/skills/ 에 2개 G3 스킬 (/react-wasm, /react-tauri) SKILL.md 추가. 소스: docs/react/kit-design/g3-performance.md"
---

## Skill
- [ ] SK-01: `react-kit/skills/react-wasm/SKILL.md` 존재. frontmatter 에 name=react-wasm, description (트리거 키워드 포함), user-invocable=true, argument-hint 명시
- [ ] SK-02: `react-kit/skills/react-tauri/SKILL.md` 존재. frontmatter 유효 + name=react-tauri
- [ ] SK-03: 두 스킬 description 에 한국어/영어 트리거 키워드 3개 이상 포함
- [ ] SK-04: 각 스킬의 Gotchas 섹션이 g3-performance.md 의 §1.6 (react-wasm) 또는 §2.6 (react-tauri) 내용 반영
- [ ] SK-05: 각 스킬의 Process 섹션이 g3-performance.md 의 §X.3~§X.5 (자동 판정 / End-to-End 파이프라인 / Feature detection) 반영

## Script
- [ ] SC-01: 두 SKILL.md 의 frontmatter YAML 이 parse 가능
- [ ] SC-02: `python3 scripts/sync-docs.py --check-only react-kit` 실행 시 AUTO:skills 블록이 Phase 2+3+4 합계 10개 스킬 포함

## Architecture
- [ ] AR-01: `/react-wasm` 이 `references/wasm-catalog.md` (또는 `docs/react/wasm-catalog.md`) 를 참조하여 이식 판정을 한다는 내용 명시
- [ ] AR-02: `/react-tauri` 가 `src/infrastructure/tauri/` 경로에만 `@tauri-apps/*` import 를 허용한다는 레이어 경계 규칙 명시 (clean-arch-layout.md 와 일관)

## Anti-patterns
- [ ] AP-01: `/react-wasm` 에 "JS↔WASM 경계 비용 (50-100ns call, 600-2500ns 문자열 마샬링) 고려" 언급 — 고빈도 콜백이나 tiny 함수 WASM 이식 안티패턴 방지
- [ ] AP-02: `/react-tauri` 에 "feature detection gating 필수 (`isTauri()` 가드)" 규칙 명시 — 브라우저에서 Tauri API 직접 호출 시 런타임 에러 방지
- [ ] AP-03: `/react-wasm` 에 "Rust panic → Result 변환 경로" 명시 (g3 §1.5 반영) — panic 전파 금지

## Reusability
- [ ] RE-01: SKILL.md 구조 기존 스킬과 일관 (frontmatter → Gotchas → Process → References)
- [ ] RE-02: Phase 2+3+4 총 10개 스킬 트리거 키워드 상호 배타적 (완전 일치 중복 없음)

## Diagnostics
- [ ] DG-01: SKILL.md 파일 내 placeholder (TODO, TBD, FIXME) 0건
- [ ] DG-02: 모든 fenced code block 에 언어 힌트 명시 (빈 ` ``` ` 금지)
