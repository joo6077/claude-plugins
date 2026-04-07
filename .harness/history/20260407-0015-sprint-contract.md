---
feature: "design-reference 스킬 — 실제 프로덕트 시각 디자인 크롤링"
created: "2026-04-07 00:15"
complexity: "중간"
conditions: 18
---

## Skill
- [ ] SK-01: `design-kit/skills/design-reference/SKILL.md`이 존재하고 frontmatter에 name, description, user-invocable: true가 포함된다
- [ ] SK-02: description에 트리거 키워드가 포함되고, 비트리거 조건으로 design-research/design-concept과의 경계가 명시되어 있다
- [ ] SK-03: Given 이전 단계 산출물(`.design/concept.md`)이 없을 때, When 스킬이 호출되면, Then 사용자 입력 키워드만으로 단독 실행이 가능하다
- [ ] SK-04: Given 이전 단계 산출물이 있을 때, When 스킬이 호출되면, Then 자동으로 로드하여 반영하는 프로세스 단계가 있다
- [ ] SK-05: 크롤링 기본 수량이 30개로 명시되어 있고 사용자가 조절 가능하다

## Error
- [ ] ER-01: 크롤링 대상 사이트에 접근 불가 시 에러 없이 건너뛰고 다른 소스로 대체하는 fallback 경로가 프로세스에 명시되어 있다

## Architecture
- [ ] AR-01: 디렉토리 구조가 기존 design-kit 스킬의 레이아웃 패턴(SKILL.md + references/)을 따른다
- [ ] AR-02: 산출물 저장 위치가 `.design/` 하위로 통일되어 있다
- [ ] AR-03: 기존 6개 스킬(design-system, design-guide, design-audit, design-concept, design-mockup, design-component)의 트리거 키워드와 겹치지 않는다
- [ ] AR-04: Given `.claude/skills/design-research/SKILL.md`의 크롤링 소스 목록과 비교했을 때, When 동일 소스(Dribbble, Behance, 오픈소스 DS)를 크롤링할 때, Then 수집 목적이 명확히 구분된다 (design-research: 원칙/가이드라인 추출, design-reference: 비주얼 사례 수집)
- [ ] AR-05: Given `design-concept/SKILL.md`의 Step 2 웹 리서치와 비교했을 때, When 동일한 웹 리서치를 수행할 때, Then 범위가 구분된다 (design-concept: 컨셉 도출용 소수 레퍼런스, design-reference: 체계적 30개 비주얼 카탈로그)
- [ ] AR-06: Gotchas에 기존 스킬과의 경계 규칙이 최소 2개 명시되어 있다 (원칙 추출 금지, 오픈소스 DS API/구조 분석 금지)

## Anti-patterns
- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다
- [ ] AP-02: 스킬 내에서 스택 특정 코드(Flutter, React 등)를 직접 생성하지 않는다 (HTML 비주얼 카탈로그 제외)

## Reusability
- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics
- [ ] DG-01: bash -n scripts/release.sh 워닝 0개
- [ ] DG-02: IDE diagnostics 워닝/인포 0개
- [ ] DG-03: 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개
