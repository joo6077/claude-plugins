---
feature: "Phase B v2 — /design-concept 카이젠 후 회귀 검증"
created: "2026-04-10 14:10"
complexity: "중간"
conditions: 14
iteration: 2
previous_verdict: "REJECT (11/14)"
kaizen_changes:
  - "design-kit/templates/moodboard.html — disclaimer 배너 + 3섹션(Texture/Layout/DoDont) 추가"
  - "design-kit/skills/design-concept/SKILL.md — Gotcha #3, #9 강화 + Step 5 검증 체크리스트"
  - "design-kit/skills/design-concept/templates/concept.md — Step 4 필수 섹션 전부 포함"
  - "design-kit/evals/evals.json — design-concept assertion 4개 추가 (id 12-15)"
  - ".design/concept.md — 컬러 방향 표에서 hex 제거 (서술형만)"
  - ".design/moodboard.html — 카이젠된 템플릿으로 재생성"
---

## Skill
- [ ] SK-01: Given `.design/concept.md`를 열었을 때, Then "컨셉 선언" 섹션이 존재하고 "왜 이 방향인가"가 설명되어 있다
- [ ] SK-02: Given 무드 키워드 섹션에서, Then 각 키워드가 concept-criteria.md의 5개 축 중 하나에 분류되어 있다
- [ ] SK-03: Given "키워드 → 시각 언어 매핑" 섹션에서, Then 각 키워드가 color/type/layout/image-shape/motion 중 최소 5개 컬럼에 번역되어 있다 (Gotcha #5)
- [ ] SK-04: Given 컬러 방향 섹션에서, Then Primary/Secondary/Accent/Neutral/Semantic **역할 기반**으로 나눠져 있다 (Gotcha #7)
- [ ] SK-05: Given 컬러 방향 섹션에서, Then WCAG AA 대비율이 언급되어 있다 (Gotcha #8)
- [ ] SK-06: **(v2 재평가)** Given `.design/concept.md`의 컬러 방향 표에서, Then **hex 값(#RRGGBB)이 0개**이다. `grep -cE '#[0-9A-Fa-f]{6}' .design/concept.md` → 0 (Gotcha #3 엄격 준수)
- [ ] SK-07: Given A/B 컨셉 안이 제시될 때, Then 두 안이 hero 구조/그리드/콘텐츠 밀도/타이포 위계/이미지 비중 중 최소 2개 축에서 차별화되어 있다 (Gotcha #6)
- [ ] SK-08: Given 레퍼런스 섹션에서, Then 최소 3개 이상 소스(URL 또는 리서치 문서 경로)가 명시되어 있다 (Gotcha #2)
- [ ] SK-09: Given `.design/concept.md`에, Then Do/Don't 각각 최소 3개 항목이 있다

## Architecture
- [ ] AR-01: Given 산출물 경로가, Then `.design/concept.md`와 `.design/moodboard.html` 두 파일이 존재한다
- [ ] AR-02: Given `.design/moodboard.html`에, Then 미치환 `{{PLACEHOLDER}}` 0개이다. `grep -c '{{' .design/moodboard.html` → 0
- [ ] AR-03: **(v2 재평가)** Given `.design/moodboard.html`에, Then SKILL.md Step 5 필수 7개 섹션의 `data-i18n="section.*"` 키가 모두 존재한다. `grep -cE 'data-i18n="section\.(keywords|palette|typography|references|texture|layout|dodont)"' .design/moodboard.html` → 7 (Gotcha #9 엄격 준수)
- [ ] AR-04: **(신규 v2)** Given `.design/moodboard.html`에, Then color disclaimer 배너가 렌더링된다. `grep -c 'data-i18n="disclaimer.color"' .design/moodboard.html` → 1

## Error
- [ ] ER-01: Given 스킬 산출물에, Then Flutter/React/CSS 구현 코드가 직접 생성되지 않았다 (Gotcha #1, HTML 무드보드 예외)
- [ ] ER-02: Given `.design/moodboard.html` 생성 과정이, Then unresolved placeholder 경고 출력 없음

## Anti-patterns
- [ ] AP-01: 버전/날짜 하드코딩 없음 (concept.md 생성일은 명시적 메타데이터로 허용)
- [ ] AP-02: `git push --force` 미사용 (Phase B N/A)

## Reusability
- [ ] RE-01: 재사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: `design-kit/templates/moodboard.html`을 재사용하여 생성 (새로 만들지 않음)

## Diagnostics
- [ ] DG-01: `bash -n scripts/release.sh` 문법 에러 0개 (회귀 없음)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개
- [ ] DG-03: `python3 -c "import json; json.load(open('design-kit/evals/evals.json'))"` 성공 (evals JSON 유효)
- [ ] DG-04: 카이젠 대상 파일 수정 후 실제 `.design/` 재생성 1회 성공
