# EX-7 — Codex 원문 대조 (2026-09-26, gpt-5.6-sol, 읽기 전용)

## 물은 것

확인할 것:
- OpenAPI 최신 판 번호와 3.1 계열 표기(3.1.x)의 뜻
- AsyncAPI 3.1.0 발표 여부와 날짜, 주요 변경

저장소 근거(읽어서 무엇을 주장했는지 먼저 확인):
- /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/evidence/phase7.md 24행 · 135행

원문: https://spec.openapis.org/oas/latest.html , https://github.com/asyncapi/spec/releases/tag/v3.1.0

## 답

## 1. 출처 목록

- 저장소 근거: `phase7.md` 24행·135행, 2026-09-26 확인
- [OpenAPI Specification 최신판](https://spec.openapis.org/oas/latest.html), 2026-09-26 가져옴
- [AsyncAPI v3.1.0 GitHub Release](https://github.com/asyncapi/spec/releases/tag/v3.1.0), 2026-09-26 가져옴

## 2. 질문별 검증

### OpenAPI 최신 판 번호

- 원문 인용: “OpenAPI Specification v3.2.1”
- 원문 URL: [spec.openapis.org/oas/latest.html](https://spec.openapis.org/oas/latest.html)
- 가져온 날짜: 2026-09-26
- 저장소 주장: 135행에서 “최신 3.2.1”
- 판정: **맞음**

### OpenAPI `3.1.x`의 뜻

- 원문 인용: “Tooling which supports OAS 3.1 SHOULD be compatible with all OAS 3.1.* versions.”
- 원문 URL: [spec.openapis.org/oas/latest.html](https://spec.openapis.org/oas/latest.html)
- 가져온 날짜: 2026-09-26
- 저장소 주장: `OpenAPI 3.1`이 최소 호환 기준이라면 반드시 낡은 표기라고 볼 수 없다는 조건부 판단
- 판정: **맞음**
- 추론: 원문은 `major.minor`가 기능 집합을 나타내고, 패치 버전은 오류 수정·명확화를 위한 것이므로 도구가 `3.1.0`과 `3.1.1` 등을 구별하지 말아야 한다고 규정한다. 따라서 `3.1`을 3.1 계열 전체의 호환 기준으로 사용하는 해석은 타당하다. 다만 “낡았다고 볼 수 없다”는 표현 자체는 원문에 없다.

### AsyncAPI 3.1.0 발표 여부와 날짜

- 원문 인용: “3.1.0 (2026-01-31)”
- 원문 URL: [github.com/asyncapi/spec/releases/tag/v3.1.0](https://github.com/asyncapi/spec/releases/tag/v3.1.0)
- 가져온 날짜: 2026-09-26
- 저장소 주장: 24행에서 `AsyncAPI 3.1.0 release`를 출처로 제시
- 판정: **맞음**
- 비고: 페이지에는 `Latest` 표시도 있었다.

### AsyncAPI 3.1.0 주요 변경

- 원문 인용: “add ROS 2 bindings to the official specification”
- 원문 URL: [github.com/asyncapi/spec/releases/tag/v3.1.0](https://github.com/asyncapi/spec/releases/tag/v3.1.0)
- 가져온 날짜: 2026-09-26
- 저장소 주장: 관련 검증 표에서 “3.1.0의 확인된 추가 기능은 ROS 2 binding”
- 판정: **맞음**
- 추론: 지정된 릴리스 페이지의 `Features`에는 ROS 2 binding 추가만 열거되어 있으므로, 이를 이 페이지에서 확인되는 주요 변경으로 요약할 수 있다.

## 3. 저장소에 반영할 문장 제안

- OpenAPI: `2026-09-26 조회 기준 최신 OAS는 3.2.1이며, 3.1.x는 같은 3.1 기능 집합의 패치 버전들을 뜻해 3.1 지원 도구는 모든 3.1.* 버전과 호환되어야 한다.`
- AsyncAPI: `AsyncAPI 3.1.0은 2026-01-31 발표됐으며, 릴리스 페이지에 명시된 기능 변경은 공식 명세의 ROS 2 binding 추가이다.`

## 4. 못 가져온 것 / 열린 질문

- 없음. 지정된 두 원문에서 질문별 인용을 모두 확보했다.
- AsyncAPI 릴리스 페이지가 연결하는 별도 블로그 릴리스 노트는 가져오지 않았으므로, 그 문서에 있을 수 있는 추가 상세 변경은 이번 판정 범위에 포함하지 않았다.