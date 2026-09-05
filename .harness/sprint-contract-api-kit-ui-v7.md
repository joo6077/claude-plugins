---
feature: "api-kit UI 시안 v7 — v1 골격 + v2 팔레트 검색 + 응답·스키마 병기 + diff 토글"
slug: api-kit-ui-v7
created: "2026-09-03 14:53"
complexity: "중간"
conditions: 29
status: done
owner_session: b73539b5-dec8-43a8-8604-c683edc766a3
conditions_digest: sha256:ed2fef9c7229b5b3
locked_at: "2026-09-03 14:58"
---

## 배경

사용자가 v1(워크스페이스형)을 베이스로 확정했다. v3 는 참고만 하고, v2·v4·v5·v6 은 폐기다.
v2 에서 두 가지를 가져온다.

1. **응답 JSON 트리에 붙는 인라인 diff** — 좌측 거터 `+/−/~`, 행 배경 틴트, 삭제 필드의 취소선 유령 행.
2. **커맨드 팔레트 검색** — v1 의 사이드바 검색창을 **제거하고** 이것으로 대체한다. 엔드포인트뿐
   아니라 액션·최근 실행·pin 필드·단축키까지 fuzzy 로 찾는다.

최종 결정: 응답 **본문 탭에서 데이터와 스키마를 같이 본다.** 각 행에 실제 값과 함께 타입·필수
여부가 붙고, **diff 표시는 on/off 토글**로 켜고 끈다. off 면 순수한 응답+스키마 뷰가 되고,
on 이면 v2 식 인라인 마크가 얹힌다. v1 의 「구조 diff」 탭은 경로 단위 요약으로 그대로 둔다.

**스키마 16 행의 근거** — orders.list 응답의 스칼라 경로는 15 개다. 여기에 직전 스냅샷에만 있던
`$.data[].items[].legacyCode` 1 개를 더해 **계약이 아는 필드가 16 개**다. 사라진 필드도 계약의
일부이므로 스키마에 남는다. 따라서 16 행은 diff ON 상태에서 관측된다 (OFF 면 유령 행이 숨어 15 행).

## 리서치 소스

- `docs/superpowers/specs/2026-09-02-api-kit-design.md` §11 (UI 레이어), §12 (확정된 결정)
- `.mockups/api-ui-v1-workspace.html` — 2390 줄, 베이스 골격
- `.mockups/api-ui-v2-command.html:527-607, 1291-1360` — 인라인 diff 렌더러 (거터·틴트·유령 행)
- `.mockups/api-ui-v2-command.html:671-735, 939-960, 1926-2160` — 커맨드 팔레트 (CSS·마크업·fuzzy·스코프)

## 범위 경계

- 생성물은 `.mockups/api-ui-v7.html` 1 개뿐이다. v1·v2 원본은 수정하지 않는다.
- 설계문서 §11 갱신과 `/create-kit` 파이프라인 실행은 이번 스프린트 밖이다.
- 응답 픽스처(엔드포인트 14 · 변경 3 · pin 2)는 v1 과 **동일하게 유지**한다. 필드를 더하거나 빼지 않는다.
- `.mockups/` 는 `.gitignore:5` 대상이라 git 기반 diff-scope oracle 을 쓸 수 없다. AR-04 는
  `find` + mtime 으로 측정한다.
- 커버리지 해소: DG-01 / DG-03 — `project.yaml` 의 analyze/test 명령이 셸 스크립트 대상인데
  이번 변경 파일은 `.html` 뿐이라 대상이 없다. 무결성 확인용으로만 실행하고 예외를 조건에 인라인했다.

## 회귀 게이트

v1 에서 이미 동작하던 것이 v7 에서 깨지지 않아야 한다: 응답 탭 5 종 동적 구성, 좌우 리사이저,
라이트·다크 전환, `.hit` 44px 타깃, 외부 요청 0, JSON 접기/펼치기.

## Skill

- [ ] SK-01: v1 골격 요소 8 종이 v7 에 모두 존재한다 — 환경 선택 · 토큰 미터 · 검증 요약 칩 · 테마 토글 · 엔드포인트 트리 · 요청 탭 · 커맨드 바 · 좌우 리사이저 [exact, enumerated] (측정: id 문자열 `env-picker` `token-meter` `verify-summary` `theme-toggle` `endpoint-tree` `request-tabs` `command-bar` `pane-resizer` 를 각각 `grep -c` 하여 8/8 이 1 이상). 예외: v1 의 사이드바 검색창(`search-wrap`)은 SK-07 팔레트로 대체되므로 이 목록에서 제외하며, v7 에 남아 있으면 안 된다
- [ ] SK-02: 응답 본문 탭의 JSON 행에 실제 값과 **스키마 타입 표기가 함께** 나타난다 [structural] (측정: Playwright 로 임의의 스칼라 행에서 값 노드와 타입 배지 노드가 동시에 존재)
- [ ] SK-03: diff 토글 ON 상태에서 orders.list 의 스키마 경로 16 개가 트리에 타입 표기와 함께 나타난다 [exact] (측정: Playwright `browser_evaluate` 로 타입 배지를 가진 스칼라 행의 고유 `data-path` 수 == 16. fallback ① 소스에서 스키마 경로 배열 길이 확인, ② 둘 다 불가하면 `[미검증]`)
- [ ] SK-04: diff 토글 ON 상태에서 add · del · chg 마크가 각 1 건 이상 총 3 건 렌더된다 — `$.data[].items[].discountRate`(add) · `$.data[].items[].legacyCode`(del) · `$.meta.total`(chg) [exact, enumerated] (측정: Playwright 로 각 종류 거터 노드 수를 세어 add>=1, del>=1, chg>=1)
- [ ] SK-05: orders.list 의 pin 필드 2 개(`$.meta.total` · `$.data[].status`)가 트리에서 pin 표시로 구분된다 [exact, enumerated]
- [ ] SK-06: v1 의 「구조 diff」 탭이 3 건 카드 목록과 계약 갱신 callout 문구를 그대로 유지한다 [exact] (측정: `data-k="add"` `data-k="rm"` `data-k="chg"` 각 존재 + 문구 `계약 갱신이 필요합니다` 존재)
- [ ] SK-07: 커맨드 팔레트가 v1 사이드바 검색창을 대체한다 — (a) `search-wrap` 이 v7 에 0 건이고 (b) `role="dialog"` + `aria-modal="true"` 팔레트가 존재하며 (c) 입력이 `role="combobox"` 로 마크업되고 (d) 검색 대상이 엔드포인트 · 액션 2 종 이상이다 [exact, enumerated]
- [ ] SK-08: 팔레트 스코프 4 종(`fail` · `recent` · `pin` · `help`)이 모두 진입 가능하고 각각 결과 목록을 렌더한다 [exact, enumerated] (측정: Playwright 로 각 스코프 진입 후 결과 행 수 >= 1)

## Script

- [ ] SC-01: diff 토글을 끄면 거터 마크 · 행 배경 틴트 · 삭제 유령 행이 모두 사라지고, 켜면 다시 나타난다 [goal] (측정: Playwright 로 OFF 상태 거터 노드 0 건 → ON 상태 3 건. 음성 대조: 토글 핸들러가 클래스만 바꾸고 유령 행을 렌더하지 않으면 ON 에서 del 이 0 건이라 FAIL 한다)
- [ ] SC-02: 다른 엔드포인트로 이동했다가 돌아와도 diff 토글 상태가 유지된다 [goal] (음성 대조: 토글을 전역 state 가 아닌 렌더 지역변수로 두면 복귀 시 기본값으로 돌아가 FAIL 한다)
- [ ] SC-03: diff 토글이 `role="switch"` + `aria-checked` 로 마크업되고 키보드 Enter/Space 로 조작된다 [structural]
- [ ] SC-04: 팔레트가 키보드로 완결된다 — ⌘K/Ctrl+K 로 열림, `/` 로 열림, Esc 로 닫힘, ArrowUp/Down 으로 행 이동, Enter 로 선택 [exact, enumerated] (측정: Playwright `browser_press_key` 로 5 종 각각 확인)

## Error

- [ ] ER-01: diff 0 건 엔드포인트(`auth.token`)에서 토글이 ON 이어도 거터 마크가 0 건이고, 스키마 타입 표기는 정상 렌더된다 [structural]
- [ ] ER-02: `state:'pending'` 엔드포인트(`products.create` · `users.patch`)에서는 본문 탭 자체가 나타나지 않고 미실행 빈 상태만 보인다 — v1 동작 유지 [exact, enumerated]
- [ ] ER-03: 팔레트에서 어떤 것과도 일치하지 않는 문자열을 입력하면 "일치하는 …" 빈 상태 문구가 나타나고 결과 수가 0 으로 표시된다 [structural]

## Architecture

- [ ] AR-01: 단일 HTML 파일이고 외부 요청이 0 이다 — `<script src=` · `<link rel="stylesheet"` · `fetch(` · `XMLHttpRequest` 각 0 건 [exact, enumerated] (측정: 4 패턴 각각 `grep -c` == 0)
- [ ] AR-02: `file://` 로 열었을 때 콘솔 에러 0 건 [exact] (측정: Playwright `browser_console_messages` 의 error 레벨 0 건)
- [ ] AR-03: 라이트·다크 양쪽에서 diff ON/OFF 가 모두 정상 렌더되고, 신규 CSS 에 하드코딩 hex 색상이 0 건이다 (기존 `--` 토큰만 사용) [exact]
- [ ] AR-04: 이번 스프린트가 생성한 파일은 `.mockups/api-ui-v7.html` 정확히 1 개다 [exact] — Given: `.mockups/` 는 `.gitignore:5` 대상이라 `git diff` 로 관측 불가. 측정: `find .mockups -maxdepth 1 -type f -newermt '2026-09-03 14:53'` 결과가 이 1 개와 정확히 일치
- [ ] AR-05: 신규 클릭 타깃 2 종(diff 토글 · 팔레트 결과 행)의 실제 크기가 44px 이상이다 [exact, enumerated] (측정: Playwright `getBoundingClientRect().height >= 44`)
- [ ] AR-06: 신규 텍스트(타입 배지 · 거터 · diff 노트 · 팔레트 섹션 라벨)의 전경/배경 대비가 라이트·다크 각각 4.5:1 이상이다 [exact] (측정: Playwright 로 computed color 를 읽어 WCAG 상대휘도 공식으로 계산)

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다. 예외: 시안 파일명 `v7` 과 화면 표시용 라벨은 허용하되, JS 로직 분기에 버전 문자열을 쓰지 않는다
- [ ] AP-02: force push 금지 — 이번 스프린트는 커밋·푸시를 수행하지 않는다

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — v1 의 `.sec-head` · `.callout` · `.j-pin` · `.btn` 스타일을 재사용하고 동일 역할의 CSS 클래스를 중복 정의하지 않는다

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0개 (변경/생성 파일 대상). 예외: 이번 변경 파일이 `.html` 뿐이라 해당 셸 스크립트는 미변경 — 무결성 확인용으로만 실행한다
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (제외 목록 `[]`, 스펠체크 항목 제외)
- [ ] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 로그에 에러/예외 0개. 예외: DG-01 과 동일 사유로 이번 변경과 무관하며 무결성 확인용이다
- [ ] DG-04: 실제 브라우저 구동 시 에러 0개
