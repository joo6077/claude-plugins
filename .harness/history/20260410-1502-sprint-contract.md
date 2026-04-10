---
feature: "kaizen-orchestrator 9-Phase 확장 + kaizen-flow.html 동기화"
created: "2026-04-10 14:20"
complexity: "중간"
conditions: 12
---

## Skill
- [ ] SK-01: `.claude/skills/kaizen-orchestrator/SKILL.md`의 "Phase 의존성" 다이어그램에 backend, infra, rust 3개 Phase가 Design-kit(Phase 6) 다음·Final 이전 순서(Phase 7→8→9)로 포함된다
- [ ] SK-02: "Process" 섹션에 각 신규 Phase(backend/infra/rust)의 범위·호출 서브에이전트(`/backend-kaizen`, `/infra-kaizen`, `/rust-kaizen`)·대상 경로가 명시된 Step이 존재한다
- [ ] SK-03: "수동" 트리거 목록에 `/kaizen-orchestrator phase7|phase8|phase9` 엔트리가 있고, frontmatter `argument-hint`도 새 Phase 번호(phase1~phase9|final)를 포함한다
- [ ] SK-04: `references/phase-dependencies.md`의 업데이트 순서 다이어그램, 상세 의존성 테이블, 스킵 전파 규칙이 9-Phase 기준으로 갱신되며 `docs/backend/`, `docs/infra/`, `docs/rust/` 리서치 문서 의존성이 반영된다

## Script
- [ ] SC-01: SKILL.md "Step 8: PR 생성" 블록에 `backend-kit/`, `infra-kit/`, `rust-kit/` 각각의 `.claude-plugin/plugin.json` 버전 bump 지침과 `marketplace.json` 갱신 지침이 추가된다. rust-kaizen 스킬 자체는 이 레포 개발용이므로 rust-kit 플러그인에 포함되지 않는다는 주석이 남는다
- [ ] SC-02: SKILL.md에서 참조하는 모든 서브 스킬 파일이 실재한다 — `.claude/skills/backend-kaizen/SKILL.md`, `.claude/skills/infra-kaizen/SKILL.md`, `.claude/skills/rust-kaizen/SKILL.md`가 Read로 확인 가능해야 한다

## Error
- [ ] ER-01: 신규 Phase 7/8/9에도 기존 규칙(피드백 0건이면 SKIP하지 않고 리서치 전용 모드 진행)이 명시적으로 적용된다는 사실이 Process 또는 Phase 스킵 규칙 섹션에 남는다
- [ ] ER-02: `.harness/.meta/kaizen-failure-count.yaml` 연속 실패 카운터 규칙이 신규 Phase에도 그대로 적용된다는 것이 "모든 Phase" 또는 명시적 Phase 7~9 기술로 확인된다

## Architecture
- [ ] AR-01: `docs/process/kaizen-flow.html`의 subtitle, `<h2>` 제목, 본문 설명, 시뮬레이션 안내문의 "6-Phase" 표기가 모두 "9-Phase"로 일관 갱신되고, 트리거 테이블의 "Full Phase 1→2→3→4→5→6→Final" 문자열도 Phase 9까지 포함되도록 수정된다
- [ ] AR-02: kaizen-flow.html `.phase-grid`에 backend/infra/rust 각 Phase `.phase-card`가 design-kit(`#phase-6`) 다음·`#phase-final` 이전에 삽입되고, 카드 id는 `phase-7`, `phase-8`, `phase-9`로 지정되며, 카드 간 연결선 인덱스가 Phase 순서와 일치한다
- [ ] AR-03: `<style>`에 `.phase-badge.p7`, `.phase-badge.p8`, `.phase-badge.p9` CSS 클래스가 추가되고 각 신규 카드에서 사용된다
- [ ] AR-04: "개별 Phase 실행" 코드 블록에 `/kaizen-orchestrator phase7|phase8|phase9` 라인이 각각 추가되고, 상단 트리거 테이블에 backend/infra/rust 수동 실행 행이 추가된다
- [ ] AR-05: 시뮬레이션 스크립트(`startSim`)의 Phase 6 블록 다음에 Phase 7/8/9의 `activate → log → complete → activateConn` 시퀀스가 연속된 T+m 시간축으로 추가되고, "✅ 카이젠 사이클 완료" 로그가 Final 종료 후에 출력된다

## Anti-patterns
- [ ] AP-01: 버전 문자열을 하드코딩하지 않는다 — 모든 버전 참조는 해당 plugin.json 또는 marketplace.json에서 읽는 지침으로 기술한다
- [ ] AP-02: `git push --force` 지침이 추가되지 않는다

## Reusability
- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: HTML 카드는 기존 `.phase-card` 클래스 재사용, 신규 CSS는 배지 색상만 추가

## Diagnostics
- [ ] DG-01: `python3 -c "from html.parser import HTMLParser; HTMLParser().feed(open('docs/process/kaizen-flow.html', encoding='utf-8').read())"` 실행 시 파싱 에러 0개
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (수정 파일 대상)
- [ ] DG-03: `python3 scripts/sync-docs.py --check-only` 실행 시 에러 0개
- [ ] DG-04: kaizen-flow.html을 열었을 때 JavaScript 콘솔 에러 없음을 육안/Playwright로 확인 (Phase 1→9→Final 순서로 카드가 순차 활성화됨)
