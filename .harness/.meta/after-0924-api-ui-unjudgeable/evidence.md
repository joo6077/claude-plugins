# after-0924-api-ui-unjudgeable 확인 기록

U 판 `6ab405a` · 캡처는 `m PROBE v8 "$V8"` · `m PROBE example "U:api-kit/evals/fixtures/unjudged/.api/ui.html"` 가 `cap/` 에 남긴 것을 한 장씩 열어 봤다 (2026-09-26 15:27).
375 캡처는 측정기가 서랍을 연 뒤 찍는다. 375 에서 칩 글자는 화면에서만 감추므로(접근 이름에는 남는다) 칩은 숫자와 모양으로 읽었다.

## 캡처에서 눈으로 본 것

| 캡처 | 본 상태 글자 · 모양 | 비고 |
| --- | --- | --- |
| `v8-1280-light.png` | 칩 `10 PASS` · `1 FAIL` · `2 미실행` · `1 판정 불가`, 트리 `/v1/products` 에 파란 물음표 | 첫 화면 `orders.list` 는 `PASS` 배지 |
| `v8-1280-dark.png` | 칩 `10 PASS` · `1 FAIL` · `2 미실행` · `1 판정 불가`, 판정 불가 모양은 밝은 파랑 | 네 칩 모양이 넷 다 다르다 |
| `v8-375-light.png` | 칩 둘째 줄에 숫자 `10` · `1` · `2` · `1` 과 체크(PASS) · 엑스(FAIL) · 점선(미실행) · 물음표(판정 불가) 모양, 서랍 트리에 같은 모양 | 테마 버튼을 덮지 않는다 |
| `v8-375-dark.png` | 위와 같은 네 모양 · 숫자 — PASS · FAIL · 미실행 · 판정 불가 | 어두운 테마 대비 문제 없음 |
| `example-1280-light.png` | 칩 `2 PASS` · `2 FAIL` · `1 미실행` · `1 판정 불가`, 트리 6 줄 | `expect` 와 같다 |
| `example-1280-dark.png` | 칩 `2 PASS` · `2 FAIL` · `1 미실행` · `1 판정 불가` | 판정 불가 모양 밝은 파랑 |
| `example-375-light.png` | 칩 둘째 줄 `2` · `2` · `1` · `1` — PASS · FAIL · 미실행 · 판정 불가 모양, 서랍 트리 6 줄 | `/v1/products` 물음표 · `/v1/products/{sku}/inventory` · `/v1/users/me` 엑스 |
| `example-375-dark.png` | 위와 같은 네 모양 · 숫자 — PASS · FAIL · 미실행 · 판정 불가 | |

판정 불가 엔드포인트를 고른 캡처(`*-1280-*-unjudged.png` 네 장)에서 `본문` 탭 맨 위 파란 알림 상자에
`$.meta.total=(없음) · len($.data)=3 → 판정 불가` 가 글자 그대로 있고 `실패 원인` 탭이 없다. ws 머리 배지는 `판정 불가`.

## tone-kit:tone-guide 5 단계 전수 대조

대상: `api-kit/skills/api-ui/SKILL.md` · `api-kit/skills/api-ui/references/viewer-spec.md` · `api-kit/references/api-layout.md` ·
시험 파일 `api-kit/evals/api-ui.spec.js` · `api-kit/evals/evals.json` · `.github/workflows/ci.yml` · 예시 입력 `report.md` · git 밖 `api-ui-v8.html` 에서 v7 대비 더한 줄.
프로젝트 오버레이 `.claude/tone-project.md` — 어댑터 없음, 주석 언어 ko. 그래서 코어 네 파일과 `locale-korean.md` 만 대조했다.
더한 줄은 `git diff -U0 f81568d 6ab405a` 212 줄과 v7 → v8 차이 57 줄이다.

| 패턴 / 규칙 | 건수 | 판정 |
| --- | --- | --- |
| C-01 what 대신 why | 0 | 통과 — 더한 주석 7 개(ci.yml 2 · 시험 파일 2 · v8 3)는 모두 이유나 깨지는 모양을 적는다 |
| C-02 이름 · 시그니처 반복 | 0 | 통과 — 주석이 식별자를 다시 말하지 않는다 |
| C-04 · 안티패턴 F 구분선 블록 (§6 G1) | 0 | 통과 — 새 구분선 없음. v8 의 `/* ==== */` 머리는 v7 것을 그대로 둔 것 |
| C-12 계산 근거 주석 (§6 G6) | 0 | 통과 |
| C-07 해설 3 줄 초과 | 0 | 통과 |
| C-10 디자인 툴 참조 (G2 · G3 · G4) | 0 | 통과 — 주석에 노드 ID · 색 값 없음. 색 값은 토큰 선언에만 있다 |
| C-13 자화자찬 (G5) | 0 | 통과 |
| C-15 주석 종결형 | 0 | 통과 — 파편형 · 단문 |
| N-01 외형 대신 역할 | 0 | 통과 — 새 토큰 `--unj` · 상태 값 `unjudged` 는 역할 이름 |
| N-07 fallback 접두사 (G-1) | 0 | 통과 |
| N-08 한 글자 이름 (G-6) | 3 | 유지 — v8 `stIcon = s =>` · `stText = s =>` · `filter(x =>` 는 v7 이 같은 자리에 쓰던 이름(S-12 같은 파일 같은 패턴). 새 코드(시험 파일 · §7 식 · `unjudgedHTML`)는 `label` · `chip` · `row` · `line` 으로 썼다 |
| N-09 무역할 파일명 | 0 | 통과 — `api-ui.spec.js` 는 design-kit `visuals.spec.js` 와 같은 꼴 |
| N-12 공식 어휘 | 0 | 통과 — Playwright `getByRole` · `toHaveCount` 등 공식 이름 그대로 |
| S-01 · S-03 추출 판정 | 1 | 유지 — `unjudgedHTML` 는 본문 탭 · 실패 원인 탭 두 자리가 같은 알림 상자를 써야 해서(계약 정한 것 10) 한 함수로 뒀다 |
| S-04 pass-through | 1 | 유지 — `stIcon` · `stText` 는 v7 이름을 호출처 세 곳에서 그대로 쓰려고 남긴 조회 함수. 새로 만든 층이 아니다 |
| S-06 헬퍼 체인 | 1 | 관측 컨벤션이라 위반으로 단정하지 않음 — `failHTML → unjudgedHTML` 한 단 |
| S-07 일어나지 않는 방어 분기 | 0 | 통과 — `d.unjudged \|\| []` 는 판정 불가 줄이 없는 엔드포인트(대부분)에서 실제로 탄다. §7 식의 `label && !extra.length` 는 글자가 둘 걸린 줄을 세지 않으려는 측정 규칙 |
| S-12 같은 카테고리 같은 패턴 | 0 | 통과 — 새 칩 · 상태 아이콘 · 배지 · 알림 상자 모두 v7 규칙에 `data-` 값만 더했다(`new_classes=0`) |
| K-02 번역투 6 종 (locale §8 G-1) | 0 | 통과 |
| K-11 새로 지은 이름 | 0 | 통과 — `판정 불가 알림` 은 알림 상자를 풀어 쓴 말 |
