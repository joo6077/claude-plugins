---
name: api-ui
description: >
  `.api/` 산출물 전체를 읽어 의존성 0 단일 파일 계약 뷰어 `.api/ui.html` 을 생성하고 연다.
  엔드포인트 트리 · 요청 폼 · 응답 본문(인라인 diff) · 데이터 구조 표 · 커맨드 팔레트를
  브라우저에서 탐색하게 만든다. 브라우저는 요청을 쏘지 않는다 — `실행` 은 커맨드 복사다.
  "뷰어 열어줘", "api ui", "결과 화면", "리포트 열어" 같은 요청 시 트리거.
  요청을 실제로 쏘는 작업에는 트리거하지 않는다 — `/api-probe` · `/api-verify` 를 쓴다.
  계약·마스킹 규칙을 고치는 작업에도 트리거하지 않는다 — `/api-contract` 를 쓴다.
argument-hint: "[--env <name>] [--no-open]"
user-invocable: true
---

## Gotchas

- **브라우저가 요청을 쏘게 만들지 마라.** `fetch` · XHR · WebSocket · 프록시 · "Try it" 버튼을 넣는 순간 세 문제가 동시에 생긴다: CORS 실패가 기본값이고(`Authorization` 이 `Access-Control-Allow-Headers` 에 없거나 preflight 가 401), 우회용 프록시 운영자가 URL·헤더·베어러 토큰·본문을 전부 보게 되고, 토큰을 브라우저 저장소에 두게 된다(OWASP 는 `localStorage`/`sessionStorage` 에 토큰 저장을 금지한다). 요청 실행은 이미 Hurl + CLI 가 한다. `실행` 버튼의 유일한 동작은 **커맨드를 클립보드에 복사**하는 것이다.
- **`file://` 는 opaque origin 이다.** `fetch('./data.json')` 로 사이드카를 읽는 순간 리포트가 빈 화면이 된다. 같은 폴더의 파일조차 same-origin 이 아니다. 모든 데이터는 HTML 안에 인라인한다. 그래서 §스냅샷 상한이 필요하다.
- **`<script type="application/json">` 도 escape 없이는 안전하지 않다.** 실행되지 않을 뿐, 본문에 `</script` 가 있으면 블록이 조기 종료되어 이후 마크업이 파서에 노출된다. 인라인 전에 `<`, `</script`, `<!--` 세 패턴을 반드시 escape 한다.
- **응답 본문은 신뢰할 수 없는 입력이다.** raw body 를 `innerHTML` 에 넣지 마라. 대상 API 가 돌려준 문자열이 리포트를 여는 사람의 브라우저에서 실행된다. `textContent` 또는 HTML entity encoding 으로만 렌더한다. 확정 시안은 `esc()` 한 함수를 모든 값 경로에 통과시킨다.
- **scrubber 를 통과한 데이터만 인라인한다 — fail-closed.** Hurl 의 `--secret` 이 exact match 로 가린다고 확인된 곳은 stderr 로그 · JSON 리포트의 `report.json` · `--curl` 파일이다(실측 2026-09-05 · 2026-09-24). stdout 응답, `--include`, `--output <file>`, `--json` 출력, 리포트의 `store/*_response.json` 같은 저장된 raw body 는 **가리지 않는다**. 마스킹 검증에서 known secret pattern 이 1건이라도 남으면 `ui.html` 을 **쓰지 마라**. "일단 만들고 나중에 지운다" 는 없다.
- **CSP `<meta>` 를 `default-src 'none'` 만 넣으면 페이지가 죽는다.** `script-src`/`style-src` 는 `default-src` 로 폴백하므로 인라인 `<style>`·`<script>`·`style=` 속성이 전부 차단된다. 뷰어는 인라인만으로 구성되므로 최소 정책은 `default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'` 이다. 그리고 **`<meta>` CSP 는 헤더의 완전한 대체가 아니다** — `frame-ancestors` · `sandbox` · `report-uri` 는 `<meta>` 로 적용되지 않는다. CSP 를 넣었다는 사실만으로 "네트워크 차단을 보증했다" 고 보고하지 마라. 보증 근거는 §자기 검증의 실측 0건이다.
- **경로는 말줄임하지 않는다.** 트리·헤더·데이터 구조 표의 경로에 `text-overflow: ellipsis` 를 걸지 마라. 경로가 곧 식별자라서 `/v1/products/{sku}/inv…` 는 아무것도 식별하지 못한다. 줄을 넘겨서라도 전문을 보여준다.
- **JSON 행 안에 스키마 열을 넣지 마라.** 먼저 시도했다가 폐기한 설계다. 1280px 에서 스키마 열이 코드 열을 밀어 값이 통째로 사라진다(`"orderId":"or…`). 한 행에 "실제 값" 과 "계약이 아는 정보" 를 같이 넣으면 좁은 폭에서 반드시 하나가 죽는다. **JSON 본문 블록 아래에 데이터 구조 표를 따로 둔다.**
- **`구조 diff` 탭을 만들지 마라.** 같은 정보를 본문 트리가 인라인 거터로 이미 보여준다. 탭을 남기면 사용자가 두 곳을 번갈아 보게 되고 어느 쪽이 정본인지 흐려진다. 응답 탭은 `본문` · `헤더` · `타이밍` 이고, 실패 시 `실패 원인` 이 **맨 앞에** 붙는다.
- **검색은 커맨드 팔레트 하나뿐이다.** 사이드바에 검색 입력창을 추가하지 마라. 입구가 둘이면 정본이 둘이 된다. `⌘K` / `Ctrl+K` / `/` 로 열고 스코프 4종(`실패` · `최근 실행` · `pin` · `단축키`)을 둔다.
- **요청 폼은 행을 더할 수 있어야 한다.** "편집 가능" 만 구현하면 픽스처 값만 고치는 폼이 나오고, 실제로 그렇게 만들었다가 쓸 수 없었다. 인벤토리에 없는 **쿼리·헤더를 그 자리에서 추가**할 수 있고, `GET` 처럼 본문이 없는 엔드포인트에도 **JSON 본문을 붙일** 수 있어야 한다. 본문을 더하면 `Content-Type: application/json` 이 자동으로 붙는다.
- **prettier 를 브라우저에 번들하지 마라.** JSON 만 해도 `standalone 82.5kB + babel 319kB + estree 213kB = 615kB` 이고 HTML 169kB, YAML 136kB 가 더 붙는다. **생성 시점에만** 포맷하고 결과 문자열을 인라인한다. prettier 가 없는 환경이면 `JSON.stringify(obj, null, 2)` 로 폴백한다 — 표시 품질만 조금 떨어지고 기능은 같다.
- **화면 표시 포맷으로 diff 를 계산하지 마라.** 비교 기준선은 RFC 8785 JCS canonical JSON(키 재귀 정렬)이고, 화면 표시는 prettier 다. prettier 는 **키를 정렬하지 않는다**(공식 rationale 이 범위 밖으로 명시). 표시본으로 diff 를 뜨면 서버의 키 순서 변경이 전부 회귀로 보고된다.
- **런타임에 리소스를 요청하는 라이브러리는 배제한다.** WASM 을 따로 로드하는 도구(`curlconverter` 등)는 `file://` 에서 로드되지 않는다. 인라인해도 되는 것은 `microdiff`(minified 1kB 미만, 의존성 0, MIT) 정도다.
- **트리를 ARIA `role=tree` 로 반쯤 구현하지 마라.** APG Tree View 는 `treeitem`·`group`·`aria-expanded`·roving focus 또는 `aria-activedescendant`·방향키·Home/End·typeahead 를 전부 요구한다. 반쪽 구현은 평범한 `nav > ul > button` accordion 보다 접근성이 나쁘다. **시각은 VSCode 탐색기, 마크업은 accordion** 이다.
- **잘라낸 본문에 diff 를 그리지 마라.** 스냅샷 본문 상한은 256KB 다. 초과분은 잘라내고 **원본 파일 경로를 표시**한다. 잘린 구간은 "변경 없음" 이 아니라 "미측정" 이므로 그 구간의 거터를 비워 두고 잘림 사실을 명시한다.
- **prod 스냅샷을 인라인하지 마라.** prod 응답에는 실 고객 데이터가 들어온다. prod 환경 뷰는 **계약 스키마와 마스킹된 형태만** 보여준다. `snapshots/prod/` 는 커밋 대상도 아니다.
- **prod + 쓰기 메서드는 커맨드 생성 자체를 막는다.** 복사 버튼이 눌려도 커맨드가 만들어지면 안 된다. 확정 시안은 `buildCommand()` 가 `null` 을 돌려주고 커맨드 바에 차단 메시지를, 클릭 시 토스트를 띄운다. 복사 경로는 함수 하나뿐이어야 우회가 생기지 않는다.
- **스냅샷이 없는 엔드포인트를 목록에서 빼지 마라.** `미실행` 상태로 트리에 남기고 상단 요약 칩에도 센다. 빼면 아직 안 때려본 엔드포인트가 사라져 커버리지 착시가 생긴다.
- **`ui.html` 커밋 여부는 미결이다.** dev/stg 스냅샷이 인라인되므로 커밋은 가능하지만 diff 가 매우 시끄럽다. 기본은 `.gitignore` 등록이고, 사용자가 커밋을 원하면 그때 빼준다. 임의로 결정해서 커밋하지 마라.

# `.api/ui.html` 정적 뷰어 생성

## 0. 프로젝트 감지

`../../references/project-detection.md` 의 절차를 실행한다. 최소한 아래를 확정한 뒤 진행한다.

| 변수 | 출처 |
|------|------|
| `API_ROOT` | `.api/` 디렉토리 경로 |
| `ENV` | `--env` 인자 → 없으면 `project.yaml` 의 기본 환경 |
| `TIER` | 해당 환경의 `tier` (`dev`/`stg`/`prod`) |
| `HAS_PRETTIER` | prettier 실행 가능 여부 (없으면 `JSON.stringify` 폴백) |

`.api/` 가 없으면 중단하고 `/api-init` 을 안내한다. 뷰어는 산출물을 렌더하는 스킬이지 만들어내는 스킬이 아니다.

## 1. 입력 수집

`.api/` 를 읽는다. 레이아웃 정본은 `../../references/api-layout.md` 다.

| 파일 | 뷰어에서의 역할 |
|------|-----------------|
| `project.yaml` | 환경 목록 · baseUrl · tier · read-only 여부 → 상단 환경 선택기 |
| `auth.yaml` | 프로파일 이름 · 만료 정보 → 토큰 만료 미터, 인증 탭 (**값은 읽지 않는다**) |
| `inventory.yaml` | 그룹 · 엔드포인트 · 파라미터 · 헤더 → 트리와 요청 폼 |
| `contracts/*.yaml` | 모드(partial/pin/exact) · pin assertion · required/optional/설명 → 배지, `*` 마크, 데이터 구조 표 |
| `snapshots/<ENV>/*.json` | 응답 본문 · 상태코드 · 헤더 · 타이밍 |
| `masks/*.yaml` | sentinel 치환 규칙 → 값 옆 `정규화됨` 힌트 |
| `reports/` 최신 실행 | PASS/FAIL/미실행 · 위반 목록 → 요약 칩, `실패 원인` 탭 |

## 2. 데이터 모델 조립

`references/viewer-spec.md` §데이터 모델의 형태로 정규화한다. 핵심은 다섯 덩어리다.

```text
ENVS     환경 목록 (id · baseUrl · label · readOnly)
GROUPS   그룹 → 엔드포인트 id 배열
EP       엔드포인트별 method · path · state · contract · pins · resp · params · pathParams · reqBody · body · timing · violations · diff
SCHEMA   엔드포인트별 JSONPath → { req, t, removed, d } — 값만 봐서는 알 수 없는 것만 적는다
RECENT   최근 실행 id 배열 (팔레트 `최근 실행` 스코프)
```

`SCHEMA` 에는 **타입을 적지 마라**. 타입은 실제 값에서 유도한다. 여기에 적는 것은 필수 여부, enum 후보, 설명, 그리고 `removed: true`(응답에는 없지만 계약에는 남아 있는 필드)뿐이다.

## 3. 마스킹 게이트 (fail-closed)

인라인 대상 전체(본문 · 헤더 · 요청 폼 초기값 · 커맨드 문자열)에 킷 scrubber 를 적용한다.

1. 키 이름 deny list — `token`, `password`, `authorization`, `secret`, `ssn` 등
2. **값 형태 정규식** — 키 이름만으로는 못 잡는다. JWT 형태, `Bearer ...`, 이메일, 전화번호, 카드번호 형태
3. `credentials.local.json` 에 적힌 값은 자동으로 deny list 에 등록
4. 마스킹된 값은 `<TOKEN>` · `<SECRET>` 같은 sentinel 로 치환하고 힌트를 붙인다

**통과 기준은 known secret pattern unredacted match `0건`이다.** 1건이라도 남으면 파일을 쓰지 않고 어떤 경로에서 걸렸는지 보고한다.

## 4. 생성 시점 precompute

브라우저는 렌더만 한다. 무거운 계산은 전부 여기서 끝낸다.

| 계산 | 방법 |
|------|------|
| 비교 기준선 | RFC 8785 JCS canonical JSON (키 재귀 정렬 · 공백 0) |
| 화면 표시본 | prettier `json` parser → 없으면 `JSON.stringify(obj, null, 2)` |
| 구조 diff | `microdiff` 로 baseline ↔ 현재 스냅샷 비교 → 경로 단위 `add`/`rm`/`chg` 목록 |
| 검색 인덱스 | 엔드포인트 id · 경로 · 그룹 · 메서드 fuzzy 매칭 대상 문자열 |
| 타이밍 세그먼트 | DNS · TCP · TLS · TTFB · 본문 다운로드 (ms) |
| 커맨드 초기값 | 폼 기본값이 반영된 `/api-probe ...` 문자열 |

diff 결과는 **본문 트리의 인라인 거터**와 **데이터 구조 표의 행 마크** 두 곳에 같은 데이터로 쓴다. 두 번 계산하지 마라.

## 5. 상한 적용

| 항목 | 상한 | 초과 시 |
|------|------|---------|
| 단일 스냅샷 본문 | `256KB` | 잘라내고 원본 파일 경로 표시 + 잘림 배너. 잘린 구간 diff 거터는 비운다 |
| 단일 HTML evidence payload | `10MiB` | 경고 후 진행 |
| 〃 | `50MiB` | split · excerpt 모드로 전환 (엔드포인트 그룹별 분할) |

상한 근거는 관행이지 측정치가 아니다. 실제 응답 크기 분포를 보고 조정한다.

## 6. 렌더

`references/viewer-spec.md` 를 그대로 따라 단일 HTML 을 쓴다. 확정 시안은 `.mockups/api-ui-v7.html` 이고, 레이아웃·토큰·상호작용의 정본이다. **시안에 없는 영역을 발명하지 마라.**

골격은 이렇다.

```text
상단바   환경 선택 · 토큰 만료 미터 · PASS/FAIL/미실행 요약 칩(클릭 시 필터) · 테마 토글
좌측     엔드포인트 트리 (그룹 accordion → 엔드포인트, 실패 배지, 경로 전문)
우측     좌: 요청 폼(파라미터·헤더·인증 탭) + 커맨드 바 / 우: 응답
응답 탭  [실패 원인] · 본문 · 헤더 · 타이밍
본문 탭  JSON 본문(값 + 타입 배지 + 필수 `*` + 인라인 diff) → 그 아래 데이터 구조 표
팔레트   ⌘K · Ctrl+K · / — 스코프 4종
하단     status bar (base URL · read-only 표시)
```

## 7. 자기 검증 (건너뛰기 금지)

파일을 쓴 직후 아래를 **실행**하고 결과를 보고에 인용한다. 서술로 대체하지 마라.

```bash
UI=.api/ui.html
# positive control — 패턴이 실제로 매치되는지 먼저 증명한다
printf '<script src="x"></script>' | grep -c '<script src'      # 기대 1
# 본 측정
grep -c '<script src' "$UI"                                      # 기대 0
grep -c '<link rel="stylesheet"' "$UI"                           # 기대 0
grep -c 'fetch(' "$UI"                                           # 기대 0
grep -c 'XMLHttpRequest' "$UI"                                   # 기대 0
grep -cE 'WebSocket|EventSource|sendBeacon|navigator\.sendBeacon' "$UI"   # 기대 0
grep -oE 'src="https?://|href="https?://[^"]*\.(css|js)' "$UI" | sort -u  # 기대 출력 없음
wc -c "$UI"                                                      # 10MiB 이하
```

| 항목 | 기대값 | 근거 |
|------|--------|------|
| `<script src` 매치 라인 | 0 | 확정 시안 실측 0 |
| `<link rel="stylesheet"` 매치 라인 | 0 | 확정 시안 실측 0 |
| `fetch(` 매치 라인 | 0 | 확정 시안 실측 0 |
| `XMLHttpRequest` 매치 라인 | 0 | 확정 시안 실측 0 |
| 외부 리소스 URL | 0 | 확정 시안의 `https://` 출현은 전부 baseUrl **텍스트** 3건뿐이며 리소스 로드가 아니다 |
| known secret pattern unredacted | 0 | 마스킹 게이트 (Step 3) |
| 누르는 자리 최소 크기 | 요소 상자 24×24 CSS px 미만 `0` 개 (아래 `under24`). 44 는 권장값 | WCAG 2.2 2.5.8 (AA, 24) · 2.5.5 (AAA, 44). 확정 시안 실측은 44 미만 39/56 · 24 미만 0 (2026-09-25) |
| 텍스트 대비 | 일반 `4.5:1` · large `3:1` · UI component `3:1` | WCAG 2.2 |
| 테마 | 라이트·다크 양립 (둘 다 대비 충족) | 확정 시안 실측 |
| 인라인 항목 수 = 화면 항목 수 | `ep` = `shown` | 확정 시안 실측 14 = 14 (2026-09-24) |
| 콘솔 error 메시지 | `0` (`favicon.ico` 404 한 건은 뺀다) | 확정 시안 실측 — 아이콘을 부르는 브라우저에서 `favicon.ico` 404 한 건 |

**0 매치를 근거로 쓰려면 positive control 이 먼저다.** 경로 오타나 빈 파일로 생긴 0 은 PASS 증거가 아니라 측정 실패다.

**브라우저로 열어 확인한다.** 글자 검사는 화면이 실제로 그려지는지 보지 못한다. 파일을 쓴 뒤 브라우저를 조종하는 도구로 열어 아래 셋을 재고, 받은 숫자를 보고에 그대로 인용한다.

1. **여는 방법** — 브라우저 조종 도구 가운데 기본 설정에서 `file://` 주소를 막는 것이 있다(오류 예: `Access to "file:" protocol is blocked`). `D=$(mktemp -d) && cp .api/ui.html "$D/"` 로 `ui.html` 한 장만 든 빈 폴더를 만들고 `python3 -m http.server 8765 --bind 127.0.0.1 --directory "${D:?폴더 변수가 비었다 — 두 명령을 한 셸에서 잇는다}" & sleep 1; kill -0 $! 2>/dev/null && echo "SERVING pid=$! dir=$D" || echo "NOT_SERVING 8765"` 로 **뒤에서** 띄운 뒤 `http://127.0.0.1:8765/ui.html` 을 열거나, 도구의 로컬 파일 허용 설정을 켜고 `file://` 로 연다. 두 명령은 한 번의 셸 호출에서 잇는다 — 명령마다 새 셸이 뜨는 도구에서는 `$D` 가 비어 지금 폴더(`.api/` 포함)를 띄운다. 앞에서 띄우면 셸이 서버에 묶여 다음 단계로 못 간다. 뒤에서 띄운 파이썬의 `Address already in use` 는 도구 출력에 안 실릴 수 있어 같은 호출 끝의 판정 줄로 가른다. `NOT_SERVING` 이면 8765 를 다른 서버(앞 실행이 남긴 서버일 수 있다)가 쥐고 있으니 그 주소를 열지 않는다 — 그 서버는 끄지 말고 빈 포트로 바꿔 다시 띄우고 여는 주소의 포트도 같이 바꾼다. 어느 쪽으로 열었는지 보고에 적는다. 확인이 끝나면 `SERVING` 줄에 찍힌 번호와 폴더로 `kill <번호>` · `rm -rf <폴더>` 를 돌린다 — 다른 셸 호출에서 `kill $!` 를 쓰지 마라(zsh 는 빈 `$!` 가 `0` 이라 `kill 0` 이 된다). `.api/` 를 통째로 띄우지 마라 — `credentials.local.json`(아이디 · 비밀번호) · `reports/`(가리지 않은 원본 응답) · `snapshots/prod/` 가 HTTP 로 열리고, 출처가 `http://127.0.0.1` 로 바뀌어 옆 파일 `fetch` 가 성공해 버린다. 한 장만 든 폴더에서는 옆 파일 `fetch` 가 404 콘솔 오류로 드러난다(실측 2026-09-25). 그래도 외부 참조 0 건은 위 `grep` 검사로 잰다 — 브라우저 확인으로 대신하지 마라.
2. **콘솔 오류** — error 등급 메시지가 0 개다. 웹 서버로 열었을 때 `favicon.ico` 를 가리키는 404 한 건은 빼고 세되 뺀 건수를 따로 적는다 — 아이콘 링크가 없어 브라우저가 기본 경로를 부른 것이지 뷰어 결함이 아니다.
3. **항목 수 · 누르는 자리** — 필터와 검색을 건드리지 않은 첫 화면에서 아래 식을 페이지 안에서 돌린다. `ep` 와 `shown` 이 같고 `under24` 가 0 이어야 한다. `under44` 는 권장값 44 에 못 미치는 수라 판정에 쓰지 않고 보고에만 적는다.

```js
(() => {
  const shown = el => { const r = el.getBoundingClientRect(), s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility !== 'hidden'; };
  const hits = [...document.querySelectorAll('button, a[href], input, select, textarea, [role="tab"], [role="switch"], [role="menuitem"], [role="option"]')].filter(shown);
  const under = n => hits.filter(el => { const r = el.getBoundingClientRect(); return r.width < n || r.height < n; }).length;
  return { ep: Object.keys(EP).length, shown: [...document.querySelectorAll('[data-ep]')].filter(shown).length,
           targets: hits.length, under24: under(24), under44: under(44) };
})()
```

확정 시안 1280×720 실측(2026-09-25): `ep 14 · shown 14 · targets 56 · under24 0 · under44 39`. 콘솔 error 는 헤드리스 셸 0 건, 아이콘을 부르는 브라우저에서 `favicon.ico` 404 한 건.

브라우저 조종 도구가 없어 이 확인을 못 하면 조용히 건너뛰지 말고 `[미검증]` 에 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 붙여 보고한다.

## 8. 열기와 보고

`--no-open` 이 없으면 기본 브라우저로 연다.

```bash
open .api/ui.html          # macOS
xdg-open .api/ui.html      # Linux
start .api/ui.html         # Windows
```

보고에는 아래를 포함한다.

- 인라인된 엔드포인트 수 · 스냅샷 수 · 환경
- PASS / FAIL / 미실행 카운트
- 잘라낸 스냅샷이 있으면 그 목록과 원본 경로
- Step 7 측정 결과 (명령 출력 인용)
- Step 7 브라우저 확인 — 연 방법 · 콘솔 error 수와 뺀 `favicon.ico` 건수 · `ep` · `shown` · `under24` · `under44`. 못 했으면 `[미검증]` 과 네 칸
- 마스킹 게이트 통과 여부

# References

- `references/viewer-spec.md` — 뷰어 구조·데이터 모델·토큰·상호작용 정본
- `../../references/api-layout.md` — `.api/` 산출물 레이아웃
- `../../references/project-detection.md` — 프로젝트 감지 절차
- `.mockups/api-ui-v7.html` — 확정 UI 시안 (레이아웃·토큰·상호작용 실측 기준)
- `docs/api/verification/static-evidence-viewer-contract.md` — 정적 증거 뷰어 계약 (원칙 10 · 수치 기준 · 안티패턴)
- `docs/superpowers/specs/2026-09-02-api-kit-design.md` §11 — UI 레이어 설계 근거
