---
feature: "design-kit 신규 스킬 3종 (design-concept, design-mockup, design-component)"
created: "2026-04-06 22:30"
complexity: "중간"
conditions: 15
---

## Skill
- [ ] SK-01: design-concept, design-mockup, design-component 각각 독립된 SKILL.md가 `design-kit/skills/` 아래에 존재한다
- [ ] SK-02: 각 SKILL.md의 frontmatter에 name, description, user-invocable: true가 포함된다
- [ ] SK-03: 각 스킬의 description에 스펙에 정의된 트리거 키워드가 모두 포함된다
- [ ] SK-04: 3개 스킬 모두 이전 단계 산출물(`.design/concept.md`, 디자인 토큰, `.design/mockups/`)이 없어도 단독 실행이 가능하다
- [ ] SK-05: 3개 스킬 모두 이전 단계 산출물이 있으면 자동으로 로드하여 반영하는 프로세스 단계가 있다

## Error
- [ ] ER-01: design-mockup에서 컨셉/토큰이 없을 때 에러 없이 요구사항만으로 시안을 생성하는 fallback 경로가 프로세스에 명시되어 있다
- [ ] ER-02: design-component에서 시안이 없을 때 사용자 직접 정의로 진행하는 fallback 경로가 프로세스에 명시되어 있다

## Architecture
- [ ] AR-01: 3개 스킬의 디렉토리 구조가 기존 design-kit 스킬(design-system, design-guide, design-audit)의 레이아웃 패턴을 따른다
- [ ] AR-02: 산출물 저장 위치가 `.design/` 하위로 통일되어 있다
- [ ] AR-03: 기존 스킬(design-system, design-guide, design-audit)의 트리거 키워드와 신규 스킬의 트리거 키워드가 겹치지 않는다

## Anti-patterns
- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다
- [ ] AP-02: 스킬 내에서 스택 특정 코드(Flutter, React 등)를 직접 생성하지 않는다 (HTML 시각화 제외)

## Reusability
- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics
- [ ] DG-01: bash -n scripts/release.sh 워닝 0개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개
- [ ] DG-03: 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개
