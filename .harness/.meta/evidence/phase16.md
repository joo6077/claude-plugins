---
phase: 16
title: "Phase 16 api-kit — 확보된 외부 근거"
collected: 2026-09-24
method: Claude 에이전트(WebFetch · WebSearch · curl) — Codex 사용 한도 소진, 사용자 지시 「코덱스 대신에 그냥 너가 알아서 진행하라고」(세션 기록 user 2026-09-24T11:54:58.940Z)
inputs: 처리 배정표(.claude/kaizen-input/insights-report.md)의 Phase 16 행 · phase-research-templates.md Phase 16 필수 출처 · 현행화 점검
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치를 지어내지 마라. 없으면 미반영으로 남긴다.
---

조회 수단: Claude(WebFetch·WebSearch·curl) — Codex 한도 소진으로 대체
(실제로 쓴 것: curl · gh · 로컬 `hurl 8.0.1` 실행 · Playwright MCP(브라우저를 조종하는 도구 연결 규약). WebFetch · WebSearch · Context7 은 쓰지 않았다. 레포는 읽기만 했다.)

# Phase 16 api-kit 외부 근거 (2026-09-24)

비교 기준 레포: `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/kaizen-0924`
지시문은 "직전 카이젠 2026-08-13" 이라 했지만 api-kit 은 2026-09-04 에 만들어졌다(`docs/api/research-log.md` 첫 절). 그래서 이번이 이 킷의 첫 카이젠이고, 대조 기준은 킷을 만들 때 적은 값이다.

---

## 1. 출처 목록

### 외부 (실제로 가져온 것만, 25 건)

| # | URL | 가져온 것 |
| --- | --- | --- |
| S1 | https://hurl.dev/docs/manual.html | 설정 우선순위, 옵션 기본값, 옵션별 환경변수 이름, 종료 코드 표 |
| S2 | https://hurl.dev/docs/templates.html#secrets | `--secret` 가리는 범위 기재 |
| S3 | https://hurl.dev/docs/asserting-response.html | 판정식(predicate) 값에 템플릿 사용, 같은 요청의 capture 를 `variable` 로 검사하는 예시 |
| S4 | https://github.com/Orange-OpenSource/hurl/blob/master/CHANGELOG.md | 8.0.0 깨지는 변경, 8.0.1, 미출시 8.1.0 |
| S5 | https://github.com/Orange-OpenSource/hurl/releases | 최신 릴리스 태그와 게시 시각 |
| S6 | https://github.com/Orange-OpenSource/hurl/issues/5077 | 8.0 jsonpath 결과가 1 개면 배열을 벗기는 동작 |
| S7 | https://github.com/Orange-OpenSource/hurl/issues/5118 | 다른 호스트로 넘어갈 때 쿠키가 안 벗겨지는 결함 (제목·상태만) |
| S8 | https://www.rfc-editor.org/rfc/rfc8785.json | RFC(인터넷 표준 문서) 8785 상태 |
| S9 | https://www.rfc-editor.org/errata/rfc8785 | RFC 8785 정정 사항 2 건 |
| S10 | https://www.rfc-editor.org/rfc/rfc9110.json | RFC 9110 상태 |
| S11 | https://www.rfc-editor.org/errata/rfc9110 | RFC 9110 정정 사항 14 건 |
| S12 | https://www.rfc-editor.org/rfc/rfc7493.json | I-JSON(JSON 호환성 제한 규칙) 상태 |
| S13 | https://www.rfc-editor.org/rfc/rfc9535.json | JSONPath 표준 상태 |
| S14 | https://spec.openapis.org/oas/ (+ `/oas/latest.html`) | OpenAPI 게시 버전 목록, 최신 판 제목 |
| S15 | https://github.com/OAI/OpenAPI-Specification/releases/tag/3.2.0 | 3.2.0 변경 내용 |
| S16 | https://github.com/OAI/OpenAPI-Specification/releases/tag/3.2.1 | 3.2.1 변경 내용 |
| S17 | https://json-schema.org/specification | 현재 판 |
| S18 | https://docs.pact.io/pact_broker/advanced_topics/pending_pacts | pending 상태가 풀리는 조건 |
| S19 | https://github.com/microsoft/playwright-mcp (README) | `file://` 차단 기본값, `browser_console_messages` · `browser_evaluate` 설명 |
| S20 | https://github.com/microsoft/playwright-mcp/releases | 최신 버전 |
| S21 | https://www.w3.org/TR/WCAG22/ | WCAG(웹 접근성 지침) 2.2 게시일, 누르는 자리 크기 기준 2 개 |
| S22 | https://pitest.org/ | 변이 시험(일부러 결함을 넣어 검사가 잡는지 보는 방법) 정의 |
| S23 | https://github.com/schemathesis/schemathesis/releases | 최신 버전 |
| S24 | https://github.com/oasdiff/oasdiff/releases | 최신 버전 |
| S25 | https://github.com/AsyncBanana/microdiff/releases | 최신 버전 |

### 로컬 실측 (이번 세션, 외부 호출 없음)

`hurl 8.0.1 (x86_64-apple-darwin25.0) libcurl/8.7.1`, 픽스처 서버는 `127.0.0.1:8732` 에 고정 JSON 을 돌려주는 파이썬 서버. 파일은 전부 스크래치패드 `p16lab/` 에 있다.

| # | 한 일 | 결과 |
| --- | --- | --- |
| L1 | 같은 요청 안에서 `[Captures] total: jsonpath "$.meta.total"` 을 잡고 `[Asserts] jsonpath "$.data" count <= {{total}}` 로 비교 | total=47·항목 10 → 종료 0 / total=-1 → 종료 4, 출력 `actual: integer <10>` · `expected: less or equal than integer <-1>` / `$.meta` 가 없음 → **종료 3**, `No query result` (capture 단계에서 멈춤) |
| L2 | 없는 경로를 바로 검사 `jsonpath "$.meta.total" >= 10` | 종료 4, `actual: none` |
| L3 | 항목 1 개짜리 `$.data` 에 `jsonpath "$.data[*].id" count == 1` | 종료 4, `Filter error … actual: integer, expected: list, bytes or nodeset`. 항목 10 개일 때 `count == 10` 은 종료 0 |
| L4 | 환경변수로 변수 넣기 | `HURL_who=from-env` → `actual: none` (종료 4). `HURL_VARIABLE_who=from-env` → 종료 0. 둘을 겹쳐 `--variable who=from-cli` 를 주면 `from-cli` 가 이긴다. `HURL_SECRET_tok=…` 도 `--secret` 처럼 `***` 로 가려진다 |
| L5 | 시크릿이 담긴 응답을 두 채널에서 확인 | `--curl <파일>` → 헤더 값이 `***`. `--error-format long` stderr 의 응답 본문 → `{"token": "***", "marker": "plain-marker"}` (시크릿 0 건, 시크릿 아닌 값은 그대로) |
| L6 | `hurl --help` | `--retry-interval … [default: 1000]`, `--max-redirs … [default: 50]` |
| L7 | Playwright MCP(프로젝트 설정 `--headless`, 설치본 0.0.80)로 확정 시안 `.mockups/api-ui-v7.html` 열기 | `file://` 로 열기 → `Error: Access to "file:" protocol is blocked`. `python3 -m http.server --bind 127.0.0.1` 로 띄워 열기 → 콘솔 오류 1 건, 내용은 `favicon.ico` 404. 인라인 `EP` 키 14 개 = 화면에 보이는 `[data-ep]` 14 개. 창 크기 1280×720 |

부작용 한 건: L7 에서 Playwright MCP 가 메인 레포의 `.playwright-mcp/` (`.gitignore` 6 행에 등록된 폴더)에 기록 파일 2 개를 썼다. 이번에 생긴 그 2 개만 지웠고 다른 파일은 건드리지 않았다.

---

## 2. 항목별 관찰 사실

### other-kits:P7 — 경로 간 조건에 양쪽 값을 적고, '판정 불가' 를 따로 센다

**(a) 양쪽 값을 적는 것.**
- Hurl 자신도 실패하면 양쪽을 찍는다. L1 의 실패 출력은 `actual: integer <10>` 와 `expected: less or equal than integer <-1>` 두 줄이다. 다만 **경로 이름은 찍지 않는다** — `<-1>` 이 `$.meta.total` 에서 왔다는 건 출력에 없다(L1).
- "경로=값 · 경로=값 → PASS" 같은 줄 형식을 규정한 외부 표준은 **못 찾았다**. 이 형식은 킷이 정하는 것이다.

**(b) '판정 불가' 를 PASS 도 FAIL 도 아닌 셋째 상태로 두는 것.**
- Hurl 에는 셋째 상태가 없다. 없는 경로를 바로 검사하면 종료 4(검사 실패)로 센다(L2, `actual: none`). 없는 경로를 capture 하면 종료 3(실행 오류)으로 센다(L1).
- 종료 코드 표는 그대로다: 0 성공 · 1 명령줄 옵션 오류 · 2 입력 파일 오류 · 3 실행 오류 · 4 검사 실패 (S1 "Exit Codes").
- 킷은 종료 3 을 "환경 실패" 로 분류한다(`failure-taxonomy.md:18`). 그래서 경로 간 조건을 `.hurl` 로 옮기면 `$.meta.total` 이 빠진 응답이 **환경 실패로 잘못 분류된다**(L1 + 킷 표). 바로 검사하면 계약 실패로 분류된다(L2). 어느 쪽도 '판정 불가' 가 아니다.
- 추론: P7 이 말하는 '판정 불가' 는 Hurl 밖, 곧 `/api-verify` 후처리에서만 만들 수 있다. 후처리에 두는 지금 설계가 이 점에서 맞다.

**(c) "경로 간 조건은 Hurl 로 표현할 수 없다" 는 기재 — 실측과 어긋난다.**
- 문서: 판정식 값에 템플릿을 쓸 수 있고(`jsonpath "$.createdAt" toDate "%+" > {{ a_date }}`), 같은 요청에서 잡은 capture 를 바로 검사하는 예시가 있다(`[Captures] pets: xpath "//pets"` 다음 `[Asserts] variable "pets" count == 200`) (S3).
- 실측: 두 기능을 합치면 `len($.data) <= $.meta.total` 이 한 요청 안에서 된다. 정상 값이면 종료 0, total 을 -1 로 바꾸면 종료 4 (L1).
- 추론: 새로 늘어난 문법이 아니라 기존 기능의 조합이다. 한계는 셋이다. 한쪽이 capture 로 잡힌 값 하나여야 하고, 덧셈 같은 계산은 안 되고, 경로가 없으면 종료 3 으로 떨어진다(L1).
- 이 기재가 있는 자리는 네 곳이다: `api-contract/SKILL.md:24`, `api-contract/references/strictness-modes.md:84`(표 "**불가**")·`:88`, `api-verify/SKILL.md:133`, `api-verify/references/failure-taxonomy.md:107`.
- 지시문의 주의 2 는 "Hurl 로 표현할 수 없다" 를 전제로 둔다. 실측은 **적을 수는 있다**는 쪽이다. 다만 (b) 때문에 후처리에 두는 결론은 그대로 설 수 있다. 확정 결정 5 건과는 무관하다.

**(d) pin 을 새로 만들면 스냅샷 사본 값을 한 번 망가뜨려 FAIL 이 나는지 본다.**
- 변이 시험의 정의: 결함을 일부러 넣고 시험을 돌린다. 시험이 실패하면 그 결함은 "잡힌" 것이고, 통과하면 "살아남은" 것이다. 살아남으면 시험 묶음에 문제가 있다는 신호다 (S22).
- Hurl 형태로는 해봤다: total → -1 로 바꾸면 종료 0 이 종료 4 로 바뀌었다(L1).
- 킷의 후처리 쪽은 **재지 못했다**. 레포에 `.api/` 실측 산출물이 0 개이고(`find -name .api` 결과 없음), 후처리는 스크립트가 아니라 스킬 본문 지시로만 있다.
- 추론: 망가뜨릴 대상은 봉인된 기준선이 아니라 사본이어야 한다. 킷의 "CI(자동 검사 서버)에서 기준선 자동 갱신 0 회" 규칙(`api-verify/SKILL.md:17`)과 맞는다.

### other-kits:P8 — 뷰어를 브라우저로 열어 항목 수와 콘솔 오류를 확인한다

**(a) 브라우저 도구로 `ui.html` 을 여는 것.**
- Playwright MCP 는 기본값에서 `file://` 주소로 가는 것을 막는다. `--allow-unrestricted-file-access` 를 주면 풀린다. README 는 이 설정이 "보안 경계가 아니라 실수 방지용" 이라고 적는다 (S19, 옵션 표와 `allowUnrestrictedFileAccess` 주석).
- 이 맥의 프로젝트 설정(`--headless`, 0.0.80)으로 `file:///…/api-ui-v7.html` 을 열면 `Access to "file:" protocol is blocked` 가 났다(L7). 최신은 v0.0.82 (2026-09-18) (S20).
- 추론: "ui.html 을 연다" 는 단계에는 둘 중 하나를 적어야 한다. MCP 를 그 옵션으로 띄우거나, `127.0.0.1` 에 작은 웹 서버를 띄워 연다.
- 추론: 웹 서버로 열면 출처가 `file://`(출처 없음)에서 `http://127.0.0.1` 로 바뀐다. 킷의 Gotcha "`file://` 는 opaque origin" (`api-ui/SKILL.md:17`)이 막으려는 실패, 예를 들어 옆 파일 `fetch` 는 웹 서버에서는 **성공해 버린다**. 그래서 §7 의 `grep -c 'fetch('` 같은 글자 검사는 브라우저 확인과 별개로 계속 필요하다.

**(b) 콘솔 오류 0 개.**
- 웹 서버로 연 확정 시안의 콘솔 오류는 1 건이었고, 그 1 건은 `favicon.ico` 404 였다(L7). 시안에는 `<link rel="icon">` 이 없다(L7 `favicon: false`).
- 추론: "콘솔 오류 0 개" 를 그대로 조건으로 두면 뷰어에 문제가 없어도 이 한 건 때문에 떨어진다. 파비콘 404 를 빼고 세거나, 생성물에 파비콘을 넣어야 한다. 파비콘을 `data:` 로 넣는 것이 킷의 CSP(페이지가 불러올 수 있는 자원을 제한하는 규칙, `api-ui/SKILL.md:21`)와 충돌하지 않는지는 **재지 않았다**.
- 도구: `browser_console_messages` 는 `level` 인자로 그 등급 이상만 돌려준다 (S19). L7 에서는 `level: error` 로 1 건을 받았다.

**(c) 화면 항목 수 = 인라인 항목 수.**
- `browser_evaluate` 로 페이지 안에서 식을 돌려 값을 받는다 (S19).
- 확정 시안에서 인라인 `EP` 키 14 개, 화면에 보이는 `[data-ep]` 14 개로 같았다(L7). 비교 식은 `Object.keys(EP).length` 와, 크기가 0 보다 크고 `display`·`visibility` 가 숨김이 아닌 `[data-ep]` 수다.

**(d) 기대값 표의 '누르는 자리 44px · 대비 · 테마' 세 줄.**
- WCAG 2.2 는 2024-12-12 권고판이다. 누르는 자리 크기는 AA 등급(2.5.8, 기본 준수 등급)이 **24×24 CSS px**, AAA 등급(2.5.5, 최고 준수 등급)이 **44×44 CSS px** 다 (S21).
- 킷은 44px 를 "확정 시안 실측" 이라 적는다(`api-ui/SKILL.md:158`, `api-ui/references/viewer-spec.md:19`). 시안 CSS 에는 `.hit::after{…min-width:44px;height:44px}` 가 있다(시안 245~248 행).
- 1280×720 에서 쟀더니 보이는 버튼·링크·입력칸 59 개 가운데, 요소 상자 기준으로 39 개가 가로나 세로 한쪽이 44 미만이었다. `::after` 로 넓힌 영역까지 쳐도 **25 개가 44 미만**이었다. 예: 그룹 버튼 세로 36, 탭 43, 입력칸 40. **24 미만은 0 개**였다 (L7).
- 추론: 이 줄을 브라우저로 재면 지금 기대값 44px 로는 떨어진다. 먼저 기대값을 AA 등급 24px 로 둘지 AAA 등급 44px 로 둘지 정해야 한다. 또 무엇을 "누르는 자리" 로 셀지(입력칸 포함 여부)도 정해야 한다.
- 대비와 테마는 **재지 않았다**.

**(e) 도구가 없을 때.** '[미검증] + 시도한 도구' 표기의 근거가 되는 외부 자료는 찾지 않았다. 이건 킷이 정하는 규칙이다.

---

## 3. 현행화 — 낡은 곳

| 파일:줄 | 지금 적힌 값 | 최신 / 실측 값 | 출처 |
| --- | --- | --- | --- |
| `api-kit/skills/api-probe/references/hurl-execution.md:312` | "`HURL_*` 환경변수는 옵션에만 붙고 변수에는 안 붙는다" | 8.0.0 에서 `HURL_foo` 가 `HURL_VARIABLE_foo` 로 바뀌었다(깨지는 변경). `HURL_VARIABLE_who` 는 `{{who}}` 를 채운다. 명령줄 `--variable` 이 환경변수를 이긴다. `HURL_SECRET_name` 은 시크릿으로 동작한다 | S1(`--variable` 환경변수 `HURL_VARIABLE_name`, `--secret` 환경변수 `HURL_SECRET_name`), S4(8.0.0 Breaking Changes), L4 |
| `docs/api/execution/auth-secret-lifecycle.md:131` | 같은 기재 + "변수는 `--variable`/…/`[Options] variable:` 로만 들어간다" | 같음. 환경변수 경로가 하나 더 있다 | S1, S4, L4 |
| `docs/api/execution/probe-synthesis-hurl-semantics.md:49`, `:82` | 같은 기재 | 같음 | S1, S4, L4 |
| `api-kit/skills/api-verify/SKILL.md:20` | "`--secret` 은 **stderr 로그와 리포트만** 가린다 … `--very-verbose` 는 body 를 stderr 에 그대로 뿌린다" | 킷의 2026-09-05 실측(`docs/api/research-log.md` "`--secret` 은 문서보다 새는 면적이 넓다")은 이렇다. `--very-verbose` stderr 는 `***` 로 가려지고, `--output` 파일 · `--json` 의 `curl_cmd`·`captures` · `--report-json` 의 `store/` 는 평문이다. 이번에 두 채널을 더 쟀다. `--curl` 파일과 `--error-format long` stderr 도 가려진다. 공식 문서 기재는 그대로다 | 내부 research-log, S2, L5 |
| `api-kit/skills/api-ui/SKILL.md:20` | "`--secret` 은 stderr 로그와 리포트만 … 가린다" | 위와 같음. 이 기재는 리포트 쪽이 틀렸다(`report.json` 은 가리지만 `store/*_response.json` 은 평문) | 내부 research-log |
| `api-kit/skills/api-probe/SKILL.md:15` | "`--very-verbose` … body 를 stderr 로 뱉으므로 CI 로그에 그대로 남는다" | 본문은 찍히지만 **등록한 시크릿은 `***`**. 시크릿으로 등록 안 한 값(개인정보 등)은 그대로 남는다 | 내부 research-log, L5(같은 동작을 `--error-format long` 에서 확인) |
| `api-contract/SKILL.md:24`, `api-contract/references/strictness-modes.md:84`·`:88`, `api-verify/SKILL.md:133`, `api-verify/references/failure-taxonomy.md:107` | 경로 간 조건은 "Hurl 로 표현 불가" / "**불가**" / "경로 하나에 predicate 하나" | capture + 템플릿 판정식으로 **적을 수 있다**. 한계: 한쪽은 capture 값 하나, 계산 불가, 경로가 없으면 종료 3 | S3, L1 |
| `api-contract/SKILL.md:225` | `.hurl` 합성 예시 `jsonpath "$.data[0].id" isString` | 같은 파일 `:20` 이 "`$.data[0].id` 같은 index assertion 금지" 라고 적는다. 파일 안에서 서로 어긋난다(외부 근거가 아니라 내부 모순) | 레포 파일 |
| `api-contract/SKILL.md:20`·`:68`, `docs/api/contract/snapshot-sealing-canonicalization.md:35` | I-JSON 검문 목록: 중복 키 · NaN/Infinity · lone surrogate · 부동소수 표준으로 못 담는 숫자 | RFC 8785 정정 7920 (Technical, 2024-05-15 확인됨): -0 은 0 으로 적히므로, 읽는 쪽은 -0 을 만나면 오류를 내야 한다(SHOULD). 목록에 -0 이 없다 | S9 |
| `docs/api/discovery/api-inventory-normalization.md:19`~`:78` (OpenAPI 3.1.0 인용 다수), `docs/api/execution/probe-synthesis-hurl-semantics.md:19`·`:25`·`:31`, `docs/api/discovery/artifact-interop-import-export.md:37`·`:67` | OpenAPI 3.1.0 | 최신은 **3.2.1** (2026-09-10). 3.2.0 은 2025-09-19, 3.1 줄의 최신은 3.1.2 (2025-09-19). 3.2 에 새로 생긴 것: `query` 메서드, 목록에 없는 메서드를 담는 `additionalOperations`, 쿼리 문자열 전체를 하나로 받는 `in: querystring`, 한 줄씩 이어지는 응답을 적는 `itemSchema`(`text/event-stream`, `application/jsonl` 등). 킷 파일에서 이 넷은 한 번도 안 나온다(grep 0 건) | S14, S15, S16 |
| (지금 기재 없음) `.hurl` 합성 규칙 | — | Hurl 8.0 부터 jsonpath 결과가 1 개면 배열을 벗긴다. 항목 1 개짜리 목록에 `[*]` + `count` 를 쓰면 종료 4 로 떨어진다. 벗기지 않는 옵션 `--no-jsonpath-coercion` 은 미출시 8.1.0 에 들어 있다. 킷 파일에 `[*]` 는 지금 0 건이라 당장 영향은 없다 | S4, S6, L3 |
| `api-kit/skills/api-probe/references/hurl-execution.md:5` | Hurl `8.0.1` (릴리스 2026-04-28) | **여전히 최신**. 변경 기록 날짜 2026-04-28, GitHub 게시 2026-04-29T09:12Z. master 에 8.1.0 (날짜 미정)이 쌓여 있다. 보안 수정 2 건 포함: CVE-2026-63481(공개 보안 결함 번호, `[Cookies]` 섹션 쿠키를 다른 호스트로 넘어갈 때 안 벗긴 문제, #5118 closed), HTML 리포트의 헤더 값 escape 수정. 그 밖에 `--fail-with-body`, `--no-jsonpath-coercion` | S4, S5, S7 |
| `api-kit/skills/api-ui/SKILL.md:158`, `api-ui/references/viewer-spec.md:19` | 누르는 자리 `44px`, 근거 "확정 시안 실측" | WCAG 2.2 기준은 AA 등급 24px, AAA 등급 44px. 시안을 쟀더니 59 개 중 25 개가 44 미만(`::after` 포함), 24 미만 0 개 | S21, L7 |
| (킷 파일 아님) `~/.claude.json` 프로젝트 Playwright MCP | 설치본 0.0.80 | 최신 v0.0.82 (2026-09-18) | S20 |
| 바뀐 것 없음 | JSON Schema 2020-12 · RFC 9110 · RFC 8785 · RFC 7493 · WCAG 2.2 · Hurl 옵션 기본값·우선순위·종료 코드 | JSON Schema 는 "The current version is 2020-12" (S17). RFC 9110 은 Internet Standard 이고 대체 문서 없음. 확인된 기술 정정 3 건은 12.5.1(Accept 예시 표)·14.1.1·8.3.2 이고, 킷이 쓰는 4xx·`Retry-After` 절(15.5.x, 10.2.3)은 아니다 (S10, S11). RFC 8785 는 Informational, 대체 문서 없음 (S8). RFC 7493·9535 대체 문서 없음 (S12, S13). Hurl 우선순위 "Environment variables → Command-line options → Options section" 순으로 뒤가 이긴다, `--retry-interval` 1000ms, `--max-redirs` 50 (−1 무제한), 종료 코드 0~4 (S1, L6) | S1, S8, S10–S13, S17, L6 |
| 버전 고정 없음 (참고) | Schemathesis · oasdiff · microdiff | Schemathesis v4.28.0 (2026-09-22), oasdiff v1.32.1 (2026-09-15), microdiff v1.6.0 (2026-08-02). 킷 파일에는 이 셋의 버전 표기가 없다(grep 0 건) | S23, S24, S25 |

참고로 Pact 는 여전히 pending 기능을 켜야 쓰는 옵션으로 두고 "앞으로 기본값이 된다" 고만 적는다 (S18). pending 이 풀리는 단위는 **공급자 브랜치별**이다. 첫 검증 성공을 올린 브랜치와 그 뒤 새로 만든 브랜치에서만 풀리고, 이미 있던 다른 브랜치에서는 pending 이 유지된다 (S18). 킷의 `state: pending | accepted` (`api-contract/SKILL.md:252`, `failure-taxonomy.md:120`·`:121`)에는 브랜치 축이 없다. 브랜치를 섞지 말라는 문장만 따로 있다(`failure-taxonomy.md:126`).

---

## 4. 권장안 (이 Phase 가 계약 조건으로 삼을 만한 것)

1. **P7 — 양쪽 값 한 줄.** `api-verify/SKILL.md` §6(133 행 근처)과 `failure-taxonomy.md` §5(107 행) 두 곳에 같은 규칙을 넣는다: "경로 간 조건은 한 줄마다 양쪽 실제 값을 적는다. 예: `$.meta.total=47 · len($.data)=10 → PASS`". 잴 때는 두 파일 각각의 해당 절 안에서 예시 문자열을 찾는다. 파일 전체가 아니라 절 범위로 자른다. 근거: Hurl 출력도 경로 이름 없이 값만 찍는다(L1).
2. **P7 — '판정 불가' 는 후처리 전용 셋째 상태.** 한쪽 경로라도 없으면 '판정 불가' 로 따로 센다. §9 리포트 첫 줄 집계(`PASS / FAIL / 보류 / flaky`)에 이 칸을 더한다. 근거: Hurl 은 경로 부재를 종료 4(L2) 또는 종료 3(L1)으로만 낸다. 판정 불가가 막는 검사를 깨는지는 열린 질문이다(§5).
3. **P7 — "표현 불가" 기재 고치기.** 네 곳(§3 표 7 행)을 이렇게 바꾼다: "capture + 템플릿 판정식으로 적을 수는 있다. 하지만 경로가 없으면 종료 3 이 되어 환경 실패로 잘못 분류되고, 판정 불가를 표현할 수 없다. 그래서 후처리로 둔다". 결론(후처리)은 바꾸지 않는다. 근거는 S3, L1.
4. **P7 — `api-contract` §11 보고에 변이 한 줄.** "pin 을 새로 만들었으면 스냅샷 **사본**의 그 값을 한 번 망가뜨려(total → -1) `/api-verify` 가 FAIL 을 내는지 확인한다. 사본에 변이가 실제로 들어갔는지 먼저 값으로 확인한다." 근거는 S22. 봉인된 기준선은 건드리지 않는다.
5. **P8 — §7 브라우저 단계의 여는 방법을 명시.** `file://` 는 Playwright MCP 기본값에서 막힌다(S19, L7). 그래서 둘 중 하나를 적는다. (i) `python3 -m http.server --bind 127.0.0.1 --directory .api` 로 띄워 연다. (ii) MCP 를 `--allow-unrestricted-file-access` 로 띄운다. 어느 쪽으로 열었는지를 보고에 적는다.
6. **P8 — 콘솔 오류 기준.** "error 등급 0 개. 단 웹 서버로 열었을 때의 `favicon.ico` 404 는 뺀다" 로 쓰거나, 생성물에 파비콘을 넣어 뺄 것 자체를 없앤다. 후자는 CSP 와 맞는지 먼저 재야 한다(미측정). 근거: L7 실측 1 건 = 파비콘 404.
7. **P8 — 항목 수 대조 식을 고정.** `Object.keys(EP).length` 와 보이는 `[data-ep]` 수가 같은지 본다(L7 에서 14 = 14). 두 숫자를 보고에 그대로 인용한다.
8. **P8 — 44px 줄.** 이번 파일에서 재지 않을 거면 '시안에서 잰 값 — 이번 파일은 재지 않음' 으로 표시한다. 잴 거라면 먼저 기대값(AA 등급 24 / AAA 등급 44)과 세는 대상을 정한다. 지금 44 로 재면 시안부터 25/59 로 떨어진다(L7). 근거 문구 "확정 시안 실측" 은 L7 과 맞지 않는다.
9. **현행화 — `HURL_VARIABLE_*` 기재 고치기** 4 곳(§3 표 1~3 행). 조건: 네 파일 모두에서 "변수에는 안 붙는다" 류 문장이 0 건이고, `HURL_VARIABLE_` 이 1 건 이상. 근거 S1, S4, L4.
10. **현행화 — `--secret` 옛 기재 3 곳 맞추기** (`api-verify/SKILL.md:20`, `api-ui/SKILL.md:20`, `api-probe/SKILL.md:15`). 킷 자신의 2026-09-05 실측과 이번 L5 에 맞춘다. 결론(킷 자체 scrubber 를 거친 것만 저장, 설계문서 §8.2)은 그대로이고 오히려 강해진다.
11. **현행화 — I-JSON 검문 목록에 -0 추가** (`api-contract/SKILL.md:20`·`:68`, `snapshot-sealing-canonicalization.md:35`). 근거 S9 정정 7920. JCS(JSON 을 비교용 한 가지 모양으로 적는 규칙) 기준선을 쓴다는 확정 결정과는 충돌하지 않는다. 추론: 목록에 한 줄 더하는 것이다.
12. **선택 — OpenAPI 3.2 대응 한 줄.** 인벤토리 정규화 문서에 3.2.1 이 최신이고 `query` · `additionalOperations` · `in: querystring` · `itemSchema` 가 생겼다는 사실만 적는다. `query` 메서드를 안전 메서드로 분류할지는 근거를 못 가져왔으니 정하지 않는다(§5).
13. **선택 — `.hurl` 합성 Gotcha.** Hurl 8 의 1 개 결과 배열 벗기기 때문에 `[*]` + `count` 를 쓰지 않는다(S6, L3).

---

## 5. 못 가져온 것 / 열린 질문

- **`.api/` 실측 산출물**: 레포에 없다. 그래서 킷 후처리의 경로 간 조건 판정과 변이 확인을 실제로 돌리지 못했다. 돌린 건 Hurl 형태(L1)뿐이다.
- **대비·테마 측정**: 재지 않았다.
- **`file://` 로 열었을 때의 콘솔 오류**: MCP 가 막아서 재지 못했다. 웹 서버로 연 결과(L7)만 있다.
- **파비콘을 `data:` 로 넣는 것이 킷 CSP 와 맞는지**: 재지 않았다.
- **HTTP `QUERY` 메서드가 안전하고 여러 번 보내도 결과가 같은 메서드로 정의돼 있는지**: 해당 표준 초안을 가져오지 않았다. 안전 검사의 허용 메서드 분류에 넣을지는 근거 없이 정하지 마라.
- **CVE-2026-63481 상세**: 변경 기록 한 줄과 #5118 의 제목·closed 상태만 봤다. 영향 범위는 가져오지 않았다. 킷은 다른 호스트로의 리다이렉트를 0 회로 막으므로(`api-verify/SKILL.md:23`) 영향이 작을 것으로 본다(추론).
- **Hurl 8.1.0 출시일**: 변경 기록에 "TBD" 로만 적혀 있다.
- **"경로=값 → 판정" 줄 형식이나 판정 불가 셋째 상태를 규정한 외부 표준**: 못 찾았다. 없다는 뜻은 아니다.
- **열린 질문 1**: '판정 불가' 가 막는 검사를 깨는가? Hurl 은 경로 부재를 실패로 센다(L2). 킷이 셋째 상태를 두면 이 부분에서 Hurl 과 갈린다. 깨지 않게 두면 경로가 사라지는 회귀가 조용히 지나갈 수 있다(추론). 사용자 결정이 필요하다.
- **열린 질문 2**: 누르는 자리 기대값을 AA 등급 24px 로 둘지 AAA 등급 44px 로 둘지. 입력칸·탭까지 셀지.
- **열린 질문 3**: 기준선 `state` 에 브랜치 축을 둘지. Pact 는 브랜치별로 푼다(S18). 확정 결정 5 건에는 없는 항목이다.
