---
version: 0.2.0
last_updated: 2026-09-05
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
