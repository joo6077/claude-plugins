---
feature: "Phase B — /design-concept 드라이런 on claude-plugins docs site"
created: "2026-04-10 13:38"
complexity: "중간"
conditions: 14
---

## Skill
- [ ] SK-01: Given `.design/concept.md`를 열었을 때, Then 한 문장짜리 "컨셉 선언"이 존재하고 "왜 이 방향인가"가 설명되어 있다 (SKILL.md Step 4 구조)
- [ ] SK-02: Given `.design/concept.md`의 무드 키워드 섹션에서, Then 3-5개(본 산출물은 6개) 키워드 각각이 concept-criteria.md의 5개 축(온도/무게감/형식성/복잡도/시대감) 중 하나에 분류되어 있다
- [ ] SK-03: Given `.design/concept.md`의 "키워드 → 시각 언어 매핑" 섹션에서, Then 각 키워드가 color/type/layout/image-shape/motion 중 최소 5개 컬럼에 대해 번역되어 있다 (Gotcha #5 준수)
- [ ] SK-04: Given `.design/concept.md`의 컬러 방향 섹션에서, Then Primary/Secondary/Accent/Neutral/Semantic **역할별**로 톤 계열/채도/WCAG 체크가 기술되어 있다 (Gotcha #7 준수 — "예쁜 5색" 금지)
- [ ] SK-05: Given 컬러 방향 섹션에서, Then WCAG AA 대비율(본문 4.5:1, 큰 텍스트 3:1)이 **컨셉 단계에서** 언급되어 있다 (Gotcha #8 준수)
- [ ] SK-06: Given 컬러 방향 섹션에서, Then 구체적 hex 값이 **확정되지 않았거나 방향 수준**(레퍼런스 예시만)이다 (Gotcha #3 준수 — hex 확정은 design-system 단계)
- [ ] SK-07: Given `.design/concept.md`에 여러 컨셉 안(A/B)이 제시될 때, Then 두 안이 hero 구조/그리드/콘텐츠 밀도/타이포 위계/이미지 비중 중 **최소 2개 축**에서 차별화되어 있다 (Gotcha #6 준수)
- [ ] SK-08: Given `.design/concept.md`의 레퍼런스 섹션에서, Then 최소 3개 이상의 소스(URL 또는 리서치 문서 경로)가 명시되어 있다 (Gotcha #2 — 근거 없는 제안 금지)
- [ ] SK-09: Given `.design/concept.md`에, Then "Do / Don't" 섹션이 존재하고 각각 최소 3개 항목이 있다

## Architecture
- [ ] AR-01: Given 산출물 경로가, Then `.design/concept.md`와 `.design/moodboard.html` 두 파일이 존재한다 (SKILL.md Step 4, Step 5 명시 경로)
- [ ] AR-02: Given `.design/moodboard.html`이, Then standalone HTML (브라우저에서 바로 열림, 외부 JS 의존 최소)이며 미치환 `{{PLACEHOLDER}}` 0개이다
- [ ] AR-03: Given `.design/moodboard.html`이, Then SKILL.md Step 5가 요구하는 7개 섹션(Mood Keywords, Color Palette, Typography, Imagery Direction, Texture/Material, Layout Cues, Do/Don't) 중 최소 6개가 포함되어 있다 (Gotcha #9 준수)

## Error
- [ ] ER-01: Given 스킬 산출물에, Then 스택별 Flutter/React/CSS 구현 코드가 직접 생성되지 **않았다** (Gotcha #1 준수 — HTML 무드보드는 시각화 목적 예외)
- [ ] ER-02: Given `.design/moodboard.html` 생성 과정이, Then Python 생성기가 unresolved placeholder 경고를 출력하지 않았고 최종 grep `{{` count가 0이다

## Anti-patterns
- [ ] AP-01: 버전/날짜 하드코딩이 의심스러운 위치 없음 — concept.md의 생성일은 명시적 메타데이터로 허용
- [ ] AP-02: `git push --force`를 사용하지 않았다 (Phase B는 git push 없음 — N/A)

## Reusability
- [ ] RE-01: 재사용 가능한 컴포넌트를 private으로 만들지 않았다 — 산출물은 `.design/` 단일 위치
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 재사용 — `design-kit/templates/moodboard.html`을 소스로 재사용했다 (새로 만들지 않음)

## Diagnostics
- [ ] DG-01: `bash -n scripts/release.sh` 문법 에러 0개 (Phase A와 동일, 회귀 없음 확인)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개
- [ ] DG-03: `.design/moodboard.html`을 브라우저에서 열어 JS 콘솔 에러 0개 (런타임 검증 가능 시)
- [ ] DG-04: 실제 구동 시 에러 0개 — `.design/moodboard.html`이 file:// 스킴에서 렌더링 가능 (외부 폰트 CDN 차단 시 fallback 작동)
