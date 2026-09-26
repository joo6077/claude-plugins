---
version: 0.3.0
last_updated: 2026-09-24
---

# api-kit Research Log

## [2026-09-04] — 최초 리서치 (킷 생성)

`/create-kit` Phase 1. 외부 조회는 Codex 5 런(read-only, foreground)으로 수행했고,
그 결과가 `docs/api/` 12 문서의 유일한 외부 근거다.

### 리서치 런

| 런 | 범위 | 소요 | 산출 |
| --- | --- | --- | --- |
| Step 1.1 | 영역 분석 + 12 주제 선정 | 4m 5s | P1 8 + P2 4 주제, Top 10 자동화 대상 |
| 배치 A | 인벤토리 정규화 · Probe/Hurl 의미론 · 상호운용 | 4m 40s | 190 줄 |
| 배치 B | 안전 게이트 · 인증/시크릿 · 오류 계약 | 3m 40s | 192 줄 |
| 배치 C | 스냅샷 봉인 · 계약 추출 모드 · 다중 샘플 | 4m 15s | 167 줄 |
| 배치 D | 회귀 diff · 정적 뷰어 · baseline 거버넌스 | 4m 55s | 237 줄 |

고유 출처 URL **108 개**. 1 차 출처(RFC · 공식 사양 · 공식 문서) 우선.

### 이 사이클에서 뒤집힌 결정

**`pin` 의 의미.** 설계문서 초안은 "지정 필드는 값까지 고정" 이라고 적었는데, 픽스처에서 pin 을
건 `$.meta.total`(주문 총건수)이 매 호출 변하는 값이라 자기모순이었다. 리서치 결과 `pin` 은
조사한 주류 도구 어디에서도 그 뜻으로 쓰이지 않는다 — 발견된 용례는 버전 pin 과 기준 snapshot pin 뿐이다.
필드별 검증 강도의 실제 어휘는 Hurl assert + predicate, Karate schema marker, Pact matcher,
JSON Schema `const`/`enum` 이다.

이름은 UI 전반에 아이콘이 깔려 있어 `pin` 으로 유지하되 **의미를 '경로별 명시 assertion' 으로
재정의**했다. 값 고정은 pin 이 표현할 수 있는 assertion 한 종류일 뿐이다. 상세는 설계문서 §9.2.

### 미검증 항목 — 구현 단계에서 실측 대조 필요

로컬에 `hurl` 바이너리가 없어 아래는 **공식 문서 기재를 옮긴 것이고 실행으로 확인하지 않았다.**
`/api-probe` 구현 시 실제 Hurl 8.0.1 로 대조하라.

| 항목 | 문서에 기재한 값 | 출처 |
| --- | --- | --- |
| 옵션 우선순위 | `env < CLI < [Options]` | hurl.dev/docs/manual.html#configuration |
| `--retry-interval` 기본 | `1000 ms` | hurl.dev/docs/manual.html#run-options |
| `--max-redirs` 기본 | `50` (`-1` 은 무제한) | hurl.dev/docs/manual.html#http-options |
| exit code | `0` 성공 / `1` CLI 파싱 / `2` 입력 파싱 / `3` 런타임 / `4` assert | hurl.dev/docs/manual.html#exit-codes |
| `--secret` 마스킹 범위 | stderr 로그·리포트만. **stdout 응답과 `--json` stdout 은 가리지 않음** | hurl.dev/docs/templates.html#secrets |

마지막 항목이 가장 중요하다 — api-kit 의 redaction 설계 전체가 여기 걸린다.
Hurl 에 맡기지 않고 킷이 자체 scrubber 를 거친 데이터만 저장·렌더한다는 결정(설계문서 §8.2)의
근거이므로, 실측에서 다르게 나오면 §8.2 를 다시 봐야 한다.

> **[2026-09-05 해소]** 아래 사이클에서 5 건 전부 실측했다. 4 건은 문서와 일치했고
> `--secret` 마스킹 범위는 **문서보다 새는 면적이 넓었다.** 이 표는 그때 무엇을 몰랐는지를
> 남기려고 원문 그대로 둔다.

### 사용자 확정 (2026-09-04)

리서치가 남긴 열린 질문 4 건에 대한 결정이다. 상세는 설계문서 §12.

| 질문 | 결정 |
| --- | --- |
| `exact` 모드가 헤더까지 보는가 | **본문만.** 헤더는 `Date`·`X-Request-Id` 등이 매번 변해 상시 실패한다. 필요한 헤더는 pin 으로 개별 지정 |
| prod read-only 범위 | **미확정.** 기본 GET/HEAD/OPTIONS 로 두고 allowlist 여지만 남긴다 |
| enum 승격 최소 샘플 | **1 샘플은 후보 표시만(경고), 3 샘플 이상에서 승격.** 오탐 실패가 도구 신뢰를 가장 빨리 깎는다 |
| baseline 에 raw 보관 여부 | **보관.** 단 시크릿 값만 마스킹한 raw |

## [2026-09-05] — Hurl 8.0.1 실측 대조

`brew install hurl` (8.0.1, `x86_64-apple-darwin25.0`, libcurl/8.7.1) 로 로컬 바이너리를 확보하고,
`127.0.0.1:8731` 에 고정 JSON 을 돌려주는 로컬 픽스처 서버를 띄워 대조했다. 외부 호출은 없다.
픽스처 본문은 `{"token":"sekret-abc123","data":[{"id":1,"status":"paid"}],"meta":{"total":1}}` 로,
시크릿 값이 **응답 본문에 그대로 들어 있는** 형태다. 마스킹 여부를 재려면 가릴 것이 있어야 한다.

판정: **CHANGED 1 건 · NO-CHANGE 4 건.** 외부 조회 0 회 (전부 로컬 실행).

### 4 건은 문서와 일치했다

| 항목 | 문서 기재 | 실측 | 방법 |
| --- | --- | --- | --- |
| 옵션 우선순위 | `env < CLI < [Options]` | 일치 | `HURL_MAX_REDIRS=3` → `--max-redirs 5` → `[Options] max-redirs: 7` 를 겹쳐 걸고 `--json` 의 `curl_cmd` 에서 3 / 5 / 7 을 순서대로 관측 |
| `--retry-interval` 기본 | `1000 ms` | 일치 | `hurl --help` → `[default: 1000]` |
| `--max-redirs` 기본 | `50`, `-1` 무제한 | 일치 | `hurl --help` → `[default: 50]`; man → "-1 to make it unlimited" |
| exit code | `0`/`1`/`2`/`3`/`4` | 일치 | 5 종을 각각 재현 — 정상 실행 / `--no-such-flag` / 깨진 `[Asserts` 블록 / 닫힌 포트 9999 / 틀린 jsonpath |

우선순위 항목에는 문서에 없던 단서가 하나 붙는다. 이 규칙은 **옵션에만** 적용된다.
`HURL_who=from-env` 를 걸어도 `{{who}}` 변수는 채워지지 않고 assert 가 `actual: none` 으로 실패한다.
변수는 `--variable` / `--variables-file` / `--secret` / `--secrets-file` / `[Options] variable:` 로만 들어온다.

> **[2026-09-24 정정]** 이 단서는 `HURL_who` 만 재서 나온 것이다. Hurl 8.0.0 부터 변수 접두는 `HURL_VARIABLE_` 이고,
> `HURL_VARIABLE_who` 는 `{{who}}` 를 채운다. 아래 2026-09-24 절에 다시 잰 값이 있다. 이 문단은 그때 무엇을 몰랐는지 남기려고 원문 그대로 둔다.

### `--secret` 은 문서보다 새는 면적이 넓다 (CHANGED)

"stderr 로그·리포트만 가린다" 는 기재는 **리포트 쪽이 부정확**하다. 리포트는 두 종류의 파일을 쓰고
그 둘의 처리가 다르다. 그리고 문서가 아예 언급하지 않은 유출 경로가 둘 더 있다.

| 채널 | 본문/값을 담나 | 시크릿 |
| --- | --- | --- |
| stdout 기본 응답 출력 | 담는다 | **평문** |
| `--include` stdout | 담는다 | **평문** |
| `--output <file>` | 담는다 | **평문** — 문서에 없던 경로 |
| `--json` stdout 의 `curl_cmd` · 요청 헤더 · `captures[].value` | 담는다 | **평문** — 문서에 없던 경로 |
| `--report-json` 의 `store/*_response.json` | 원본 응답 본문 | **평문** |
| `--report-json` 의 `report.json` (`curl_cmd` · 헤더) | 담는다 | `***` 로 마스킹 |
| stderr `--very-verbose` | 담는다 | `***` 로 마스킹 |
| stderr `--verbose` | **본문을 안 찍는다** | 해당 없음 |
| `--report-html` | **본문을 안 담는다** | 해당 없음 |

아래 두 줄은 "0 건" 을 통과로 읽으면 안 되는 자리다.

- `--json` stdout 의 `response` 에는 **`body` 필드 자체가 없다.** 여기서 시크릿이 안 보이는 것은
  마스킹이 아니라 미수록이다. 대신 같은 출력의 `curl_cmd` · 요청 헤더 · `captures` 가 평문이다.
- `--verbose` stderr 에도 본문이 안 찍힌다. 본문이 찍히는 건 `--very-verbose` 부터이고, 거기서는
  실제로 `***` 로 바뀐다.

exact match 라는 기재도 실측으로 확인했다. `--secret token=sekret-abc123` 을 걸고 같은 값의
base64 본(`c2VrcmV0LWFiYzEyMw==`)을 별도 헤더로 보내면 원본은 `***` 가 되지만 base64 본은
stderr · `curl_cmd` · 리포트 3 곳에 평문으로 남는다.

### `redact` capture 의 사정거리는 더 좁다

문서는 `redact` 를 "이후 로그·리포트 마스킹 대상에 넣는다" 고만 적었다. 실측은 다르다.

- `--json` stdout 의 `captures[].value` 가 평문이다.
- 캡처값을 다음 entry 의 `Authorization` 헤더로 넘기면 `--json` 의 `curl_cmd` 와 요청 헤더에 평문으로 나타난다.
- `--report-json` 의 `store/*_response.json` 도 평문이다.
- **`--very-verbose` 와 함께 쓰면 Hurl 이 실행을 거부한다** — `error: Invalid redacted secret ...
  redacted secret not authorized in verbose`. 진단하려고 verbose 를 켜는 순간 파일이 안 돈다.

### 설계에 미치는 영향

§8.2 의 결정(Hurl 에 맡기지 않고 킷 자체 scrubber 를 통과한 데이터만 저장·렌더)은 **뒤집히지 않고
오히려 강화된다.** 다만 scrubber 를 걸어야 할 경로 목록이 늘었다 — `--output` 과
`--report-json` 의 `store/` 디렉토리, 그리고 `--json` stdout 을 artifact 로 남기는 경우다.
`/api-probe` 가 리포트를 켜면 시크릿이 파일로 떨어진다는 뜻이므로, 리포트 디렉토리도 스냅샷과
같은 fail-closed 게이트를 지나야 한다.

### 재현 방법

`hurl 8.0.1` 과 로컬 픽스처 서버만 있으면 된다. 서버는 고정 JSON 하나를 200 으로 돌려주면 충분하고,
그 본문에 시크릿으로 등록할 값을 넣어 두는 것이 요점이다. 채널별 판정은
`grep -c '<시크릿>' <출력>` 으로 하되, **그 채널이 본문을 담기는 하는지** 를 먼저 확인해야 한다
(비밀 아닌 값 하나를 같이 넣어 두고 그것으로 채널의 수록 여부를 재는 편이 안전하다).

### 다음 사이클 후보

- JSON Schema 역추론 도구(quicktype · GenSON · json-schema-inferrer) 최신 버전 pinning —
  설계문서 §13 이 이미 미해결로 표시한 항목
- `exact` 모드의 배열 순서 정책 — 순서 보장 없는 컬렉션에 exact 를 허용할지
- `--secrets-file` 의 파일 권한·수명 실측 — 이번 사이클에서 `--secret` 만 봤다
- Hurl 리포트 디렉토리에 대한 scrubber 게이트 설계 (2026-09-05 실측에서 새로 생긴 요구)

## [2026-09-24] — 첫 카이젠 (Phase 16)

카이젠 2026-09-24 Phase 16. 외부 근거는 `.harness/.meta/evidence/phase16.md` 하나이고, 이 절의 실측은 로컬
`hurl 8.0.1` 과 `127.0.0.1` 픽스처 서버, 헤드리스 크로미엄(Playwright 1.58.2)으로만 돌렸다. 외부 요청은 없다.
처리 배정표 키는 `other-kits:P7`(경로 간 조건에 양쪽 값 · 판정 불가)과 `other-kits:P8`(뷰어를 브라우저로 여는 확인)이다.
실측은 2026-09-24(근거 수집)와 2026-09-25(계약 초안 · 검토)에 돌렸다. 소제목 날짜는 절을 연 날이다.

### 경로 간 불변식을 Hurl 에 적어 본 결과 (2026-09-24)

`len($.data) <= $.meta.total` 을 한 요청 안에서 `[Captures] total: jsonpath "$.meta.total"` 다음
`[Asserts] jsonpath "$.data" count <= {{total}}` 로 적었다.

| 응답 | 종료 코드 | 출력 |
| --- | --- | --- |
| `total=47` · 항목 10 | `0` | — |
| `total=-1` · 항목 10 | `4` | `actual: integer <10>` · `expected: less or equal than integer <-1>` — `-1` 이 `$.meta.total` 에서 왔다는 말은 없다 |
| `$.meta` 없음 | `3` | `No query result` — capture 에서 멈춘다 |
| `$.meta` 없음, `jsonpath "$.meta.total" >= 10` 을 바로 검사 | `4` | `actual: none` |

적을 수는 있다. 그래서 킷이 네 곳에 적어 둔 「Hurl 로 표현 불가」 는 틀렸다. 그러나 경로가 없으면 `3`(킷 분류로
환경 실패) 또는 `4`(계약 실패) 가 되고 셋째 상태가 없다. 후처리에 두는 결론은 그대로이고 이유가 바뀌었다 —
표현할 수 없어서가 아니라 `판정 불가` 를 가를 곳이 후처리뿐이라서다.

### 뷰어를 브라우저로 연 결과 (2026-09-24)

확정 시안 `.mockups/api-ui-v7.html` 사본(sha256 앞 16 자리 `c4bd563ec8b71a95`)을 1280×720 창에서 열었다.

| 항목 | 값 |
| --- | --- |
| 인라인 `EP` 키 · 화면에 보이는 `[data-ep]` | 14 · 14 |
| 보이는 누르는 요소 (버튼 · 링크 · 입력 · 탭 · 스위치 · 메뉴 항목 · 선택지) | 56 |
| 요소 상자 가로나 세로가 24 CSS px 미만 | 0 |
| 44 CSS px 미만 | 39 |
| 콘솔 error — `127.0.0.1` 웹 서버, 아이콘을 부르는 크로미엄 | 1 (`favicon.ico` 404) |
| 콘솔 error — 헤드리스 셸 | 0 (아이콘을 부르지 않는다) |

누르는 요소 56 은 `/api-ui` §7 식이 센 수다(버튼 53 · 입력칸 2 · 선택 상자 1). 근거 파일 L7 은 셀 대상을 다르게 골라 59 개로 셌다 —
44 미만 39 · 24 미만 0 은 두 셈이 같다.
근거 수집 때 브라우저 조종 도구로 `file://` 를 열자 `Access to "file:" protocol is blocked` 가 났다(근거 파일 L7).
킷이 적어 둔 누르는 자리 44px 의 근거 「확정 시안 실측」 은 이 값과 맞지 않는다. WCAG 2.2 는 2.5.8(AA)이 24,
2.5.5(AAA)가 44 다.

### 문서와 실측이 어긋난 것 (2026-09-24)

| 항목 | 킷에 적혀 있던 것 | 실측 · 출처 |
| --- | --- | --- |
| 환경변수로 넣는 변수 | `HURL_*` 는 변수에 안 붙는다 (2026-09-05 절 · 스킬 참조 문서 · 문서 둘) | `HURL_who` 는 안 채우지만 `HURL_VARIABLE_who` 는 채운다. `HURL_SECRET_tok` 은 `***` 로 가려진다. `--variable` 을 겹치면 명령줄 값. Hurl 8.0.0 에서 접두가 바뀌었다 |
| 경로 간 불변식 | Hurl 로 표현 불가 (스킬 둘 · 참조 문서 둘) | 위 표 — 적을 수 있다 |
| 누르는 자리 | 44px, 확정 시안 실측 (스킬 · 뷰어 스펙 · 뷰어 계약) | 위 표 — 44 미만 39 |
| `--secret` 이 가리는 곳 | stderr 와 리포트 (스킬 셋 · README) | 2026-09-05 절 실측 — 리포트 가운데 `report.json` 만 가린다. 스킬 Gotcha 네 곳이 그 실측을 안 따라갔다 |
| I-JSON 게이트 목록 | `-0` 없음 | RFC 8785 정정 7920 (기술 정정, 2024-05-15 확인) — `-0` 은 `0` 으로 적히므로 파서가 오류를 내야 한다 |

> **[2026-09-26 보탬]** 이때 `-0` 을 I-JSON 게이트 목록에 넣었지만 RFC 7493 에는 없는 규칙이었다. 게이트 다음의 -0 검사로 옮겼다 — 맨 아래 「[2026-09-26] — I-JSON 게이트와 -0 검사를 가름」 절.

`--curl <파일>` 과 `--error-format long` stderr 도 등록한 시크릿을 `***` 로 가렸다. 시크릿으로 등록하지 않은 값은 그대로다. 이 `--curl` 결과를 `hurl-execution.md` §6 표와 `auth-secret-lifecycle.md` 세 자리(§6 문장 · 수치 표 · Gotcha 머리)에 더했다.

### 이번에 정한 것 (2026-09-24)

- `판정 불가` 는 PASS 로도 FAIL 로도 세지 않고 따로 세며, 그 자체로는 게이트를 깨지 않는다. 사라진 경로가
  `required` 면 schema drift(필드 삭제 = 계약 실패)가 따로 잡는다. I-JSON 게이트 실패를 「비교 불가」 로 따로
  두는 기존 규칙과 같은 모양이다
- 누르는 자리의 통과선은 요소 상자 24×24 CSS px 미만 0 개다. 44 는 권장값으로 보고에만 적는다
- 경로 간 불변식은 후처리에 둔다(확정 결정 유지). 바뀐 것은 이유다

### 이월 — 다음 사이클 후보 (2026-09-24)

- OpenAPI 3.2(최신 3.2.1) 의 `query` 메서드 · `additionalOperations` · `in: querystring` · `itemSchema` 대응 —
  `query` 를 안전 메서드로 볼 근거를 이번에 가져오지 않았다
- Hurl 8 은 jsonpath 결과가 1 개면 배열을 벗긴다 — 항목 1 개 목록에 `[*]` 와 `count` 를 쓰면 `4` 다.
  `/api-contract` §9 예시 `jsonpath "$.data[0].id" isString` 이 같은 파일 Gotcha 의 index assertion 금지와 어긋나는데,
  바꿀 표현이 이 동작에 걸리는지 hurl 로 먼저 재야 한다
- 뷰어 텍스트 대비 · 테마 실측
- Pact pending 은 공급자 브랜치별로 풀린다 — baseline `state` 에 브랜치 축을 둘지
- Hurl 8.1.0(미출시) 의 보안 수정 두 건과 `--no-jsonpath-coercion`
- 2026-09-05 절 후보 넷(역추론 도구 버전 · exact 배열 순서 · `--secrets-file` 권한 · 리포트 폴더 scrubber)은 그대로 남았다

## [2026-09-26] — I-JSON 게이트와 -0 검사를 가름

근거 파일: `.harness/.meta/evidence/rfc7493-ijson-2026-09-26.md` (Codex 가 rfc-editor.org 에서 RFC 7493 · RFC 8259 · RFC 8785 · 정정 7920 원문을 받아 인용했다).

- RFC 7493 §2.1 은 surrogate 와 noncharacter 를 MUST NOT 으로 막는다. noncharacter 를 api-verify · api-probe 목록에도 넣었다 — 전에는 api-contract 표에만 있었다.
- `-0` 은 RFC 7493 에 없다(전문 검색 0 건). RFC 8259 문법상 올바른 JSON 숫자다. 막는 근거는 RFC 8785 정정 7920 의 SHOULD 다 — JCS 가 `0` 으로 적어 부호가 사라진다.
- 그래서 `-0` 을 I-JSON 게이트 목록에서 빼고 게이트 다음의 -0 검사로 따로 적었다. 분류(봉인 불가 · 비교 불가)는 그대로다.
- binary64 밖 숫자는 RFC 7493 §2.2 가 SHOULD NOT 으로 둔다. 이 킷은 실패로 막는다 — 표준보다 엄격한 쪽이다. NaN/Infinity 는 JSON 문법이 막는다.
