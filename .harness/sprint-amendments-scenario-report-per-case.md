---
slug: scenario-report-per-case
created: "2026-09-30 12:50"
---

## A-01 — AR-02 브라우저 확인을 `file://` 대신 이 컴퓨터 안 간이 서버로 연다

**앵커**: AR-02 측정 절 — "`file://$T/example/index.html` 을 열고".

**무엇이 부딪혔나**: 브라우저 도구(`mcp__playwright__browser_navigate`)가 `file:` 주소를 막는다. 실측 오류 원문 `Access to "file:" protocol is blocked`.

**어떻게 읽나**: 같은 예시 폴더를 `python3 -m http.server 8765 --bind 127.0.0.1` 로 띄우고 `http://127.0.0.1:8765/index.html` 을 연다. 여는 파일 · 누르는 링크 · 보는 것(케이스 제목, 콘솔 오류 0 건, 캡처 두 장)은 원문 그대로다.

간이 서버로 열면 브라우저가 `favicon.ico` 를 따로 요청해 404 콘솔 오류가 1 건 난다(첫 방문 실측). 이것은 여는 방식 때문이라 페이지 틀에 `<link rel="icon" href="data:,">` 를 넣어 없앴다 — 틀은 범위 경계 안(`flutter-toolkit/skills/flutter-scenario-report/`)이고 예시 보고서를 다시 만들어 SC-07 바이트 대조를 통과시켰다. 넣은 뒤 목록 페이지와 케이스 페이지 모두 콘솔 메시지 0 건.

증거: 세션 임시 폴더 `evidence/scenario-per-case-01-list.png` · `evidence/scenario-per-case-02-case.png`.

**amend_direction_oracle**: `unchanged` — 재는 대상(예시 폴더의 두 페이지)과 통과 기준(제목 보임 · 콘솔 오류 0 · 캡처 두 장)이 같고 여는 주소 모양만 바뀐다.

**consent**: 방향이 느슨해지지 않아 따로 묻지 않았다. 구현 착수 지시 — 사용자 「ㄱㄱ」(2026-09-30, 세션 `97f28e34-99ea-4a74-9baa-3288b7964458`).
