# 계약 작성

요구사항을 만족하는 구현의 완료 조건 계약서와, 그 조건을 실제로 재는 측정 묶음을 쓴다. 구현은 하지 않는다. 정해진 JSON 모양으로만 답한다.

## 읽을 것

- 요구사항: {{REQUIREMENTS}}
- 계약 형식 규칙: {{SCHEMA_DOC}}
- 작성 절차와 함정: {{SKILL_DOC}}
- 프로젝트 설정(카테고리 · 금지 패턴 · 명령): {{PROJECT}}
- 저장소: {{REPO}} (읽기만 한다)

## 답

- contract: 계약 파일 전문(frontmatter 포함). slug 는 {{SLUG}} 이다. 봉인 칸(conditions_digest · measurement_digest · locked_at)은 쓰지 않는다.
- measurements: 측정 묶음 파일. path 는 상대 경로, content 는 파일 내용이다. 묶음은 {{META}} 에 놓인다.
- 조건은 밖에서 관찰되는 동작으로 쓰고, 조건마다 PASS/FAIL 이 갈리는 측정을 붙인다. 구현 전인 지금 측정을 돌리면 구현이 필요한 조건은 FAIL 이 나야 한다.
- 모르는 것은 추측하지 말고 계약 `## 배경` 에 「확인 못 함:」 으로 적는다.
