---
title: Probe 합성과 Hurl 실행 의미론
version: 0.2.0
last_updated: 2026-09-05
---

# Probe 합성과 Hurl 실행 의미론

인벤토리의 operation 에서 실행 가능한 `.hurl` probe 를 합성할 때의 값 생성 순서, 직렬화 규칙, 그리고 Hurl 8.0.1 실행 엔진의 의미론을 다룬다.

---

## 원칙

### 1. Example-Default-Enum Precedence

값 생성 우선순위는 media type 의 explicit `example` / `examples` → schema `example` → JSON Schema `default` → `const` / `enum` 순이다. `default` 는 validation 키워드가 아니라 annotation 이므로 그 값이 schema 를 만족한다는 보장이 없다. `enum` 에서 값을 고른 뒤에도 schema 검증을 한 번 더 돌린다.

> **출처:** [OpenAPI 3.1.0 Media Type Object](https://spec.openapis.org/oas/v3.1.0#media-type-object), [JSON Schema 2020-12 Validation](https://json-schema.org/draft/2020-12/json-schema-validation)

### 2. Deterministic Query Serialization

query 는 URL 문자열과 `[Query]` 섹션 중 **한 경로만** 쓴다. Hurl 은 둘 다 있으면 둘 다 전송하므로 파라미터가 중복된다. 기본은 `[Query]` 섹션이고, OpenAPI 의 `style` / `explode` / `allowReserved` 를 반영해 직렬화한다.

> **출처:** [Hurl Request](https://hurl.dev/docs/request.html), [OpenAPI 3.1.0 Parameter Object](https://spec.openapis.org/oas/v3.1.0#parameter-object)

### 3. Explicit Accept/Content-Type/Authorization

이 세 헤더는 추론에 맡기지 않고 명시적으로 생성한다. `Accept` 는 기대 response media type, `Content-Type` 은 requestBody media type, `Authorization` 은 해당 operation 에 적용되는 security requirement 에서 각각 파생시킨다. 생략하면 클라이언트 기본값이 끼어들어 실패 원인이 계약인지 전송인지 구분되지 않는다.

> **출처:** [RFC 9110 Accept](https://www.rfc-editor.org/rfc/rfc9110.html#name-accept), [OpenAPI 3.1.0 Parameter Object](https://spec.openapis.org/oas/v3.1.0#parameter-object)

### 4. Dependency Capture

앞 entry 의 응답에서 필요한 값만 `[Captures]` 로 뽑아 이후 entry 의 변수로 쓴다. Hurl 은 status, header, cookie, body, jsonpath, xpath, duration 등을 capture 할 수 있다. 같은 이름으로 다시 capture 하면 새 값이 이전 값을 덮으므로, 체인 안에서 이름을 재사용하지 않는다.

> **출처:** [Hurl Capturing Response](https://hurl.dev/docs/capturing-response.html)

### 5. Entry Isolation

상태를 공유해야 하는 흐름(로그인 → 조회 → 삭제 등)은 반드시 한 `.hurl` 파일 안에 둔다. Hurl 은 같은 파일 안에서 cookie store 를 공유하고, `--test` 모드는 파일 단위로 병렬 실행하므로 파일 간 의존은 실행 순서를 보장받지 못한다. 파일 경계 = 격리 경계다.

> **출처:** [Hurl Entry](https://hurl.dev/docs/entry.html), [Hurl Manual](https://hurl.dev/docs/manual.html)

### 6. Hurl Option Precedence

설정 우선순위는 environment variable < command-line option < per-entry `[Options]` 다. 뒤쪽이 앞쪽을 이긴다. cli-only 옵션은 `[Options]` 로 내려쓰지 않는다 — 파일에 적혀 있어도 적용되지 않아 문서와 실제 실행이 어긋난다.

이 규칙은 **옵션에만** 적용된다. `HURL_INSECURE` 가 `--insecure` 가 되는 식이고, 변수에는 해당되지 않는다 — `HURL_who` 를 걸어도 `{{who}}` 는 채워지지 않는다. 변수는 `--variable` / `--variables-file` / `--secret` / `--secrets-file` / `[Options] variable:` 로만 들어온다.

> **출처:** [Hurl Manual — Configuration](https://hurl.dev/docs/manual.html#configuration) · 실측 (hurl 8.0.1, 2026-09-05)

### 7. Response Capture Policy

최소 assert 는 expected HTTP status 하나다. body 전체 capture 는 downstream dependency 가 실제로 그 값을 쓰거나 진단 목적일 때만 켠다. 일반 body/query capture 는 decompressed·decoded 본문 기준이고, 원본 바이트가 필요하면 `rawbytes` 를 쓴다.

> **출처:** [Hurl Response](https://hurl.dev/docs/response.html), [Hurl Capturing Response](https://hurl.dev/docs/capturing-response.html)

### 8. Continue-on-error Strategy

기본 동작은 assert error 발생 시 해당 파일 실행 중단이다. `--continue-on-error` 는 assert error 에도 파일 끝까지 진행시키지만, dependency chain 에서는 오염된 변수로 후속 요청이 돌아 전이 실패를 만든다. 서로 독립인 probe 배치에만 켠다.

> **출처:** [Hurl Manual — Run Options](https://hurl.dev/docs/manual.html#run-options)

### 9. Exit Code 기반 실패 분류

Hurl 종료 코드로 실패 종류를 나눈다. `4`(assert)만 계약 위반이고, `2`(input parse)는 probe 생성 버그, `3`(runtime)은 네트워크·환경 문제다. 이 구분 없이 non-zero 를 전부 계약 실패로 보고하면 회귀 diff 가 노이즈로 덮인다.

> **출처:** [Hurl Manual — Exit Codes](https://hurl.dev/docs/manual.html#exit-codes)

---

## 수치 기준

`확인` 열은 값의 출처가 아니라 **어떻게 확인했는지**다. `실측` 은 로컬 hurl 8.0.1 로 실행해 관측한 것,
`문서` 는 아직 실행으로 확인하지 않은 것이다.

| 항목 | 값 | 확인 | 근거 |
|------|-----|------|------|
| Hurl 엔진 버전 | `8.0.1` (release `2026-04-28`) | 실측 | `hurl --version` → `hurl 8.0.1 (x86_64-apple-darwin25.0) libcurl/8.7.1` |
| 옵션 우선순위 랭크 | `1` env < `2` CLI < `3` per-entry `[Options]` | 실측 | `HURL_MAX_REDIRS=3` < `--max-redirs 5` < `[Options] max-redirs: 7` 을 `curl_cmd` 로 관측 |
| 옵션 우선순위의 적용 대상 | **옵션만.** 변수는 `HURL_*` 로 안 들어온다 | 실측 | `HURL_who=…` → assert `actual: none` |
| `--max-redirs` 기본값 | `50` (`-1` = unlimited) | 실측 | `hurl --help` → `[default: 50]`, man → "-1 to make it unlimited" |
| retry 기본값 | `0` = no retry, `-1` = unlimited | 문서 | [Hurl Manual — Run Options](https://hurl.dev/docs/manual.html#run-options) |
| `--retry-interval` 기본값 | `1000 ms` | 실측 | `hurl --help` → `[default: 1000]` |
| entry 번호 시작값 | `1` (`--from-entry` / `--to-entry`) | 문서 | [Hurl Manual — Run Options](https://hurl.dev/docs/manual.html#run-options) |
| `--test` 실행 모드 | 병렬. 순차가 필요하면 `--jobs 1` | 문서 | [Hurl Manual — Run Options](https://hurl.dev/docs/manual.html#run-options) |
| exit code | `0` success / `1` CLI parse / `2` input parse / `3` runtime / `4` assert | 실측 | 5 종을 각각 재현 — 정상 / `--no-such-flag` / 깨진 `[Asserts` / 닫힌 포트 / 틀린 jsonpath |
| operation 당 자동 생성 probe 수 | 기본 `1` (preferred media type), explicit examples 다수 시 최대 `3` | 추론 | 이 킷의 설계 결정 |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| URL query 와 `[Query]` 섹션을 동시에 생성 | Hurl 이 둘 다 전송해 같은 파라미터가 중복된다 |
| dependent flow 를 여러 `.hurl` 파일로 분할 | `--test` 가 파일을 병렬 실행해 순서 보장이 깨진다 |
| cli-only 옵션을 `[Options]` 에 기입 | 무시되어 파일에 적힌 실행 의미와 실제 실행이 달라진다 |
| 모든 response body 를 capture | 리포트가 비대해지고 토큰·시크릿이 로그에 남는다 |
| auth 실패 뒤에도 continue-on-error 로 진행 | 이후 probe 실패가 계약 위반이 아니라 인증 전이 실패가 된다 |

---

## Gotchas

- **`[Options]` 의 `variable` 만 다음 entry 로 이어진다** — 다른 `[Options]` 항목은 그 entry 에서만 유효한데 `variable` 은 예외다. entry 별로 같은 이름 변수를 다르게 주면 뒤 entry 가 앞 값을 조용히 상속하거나 덮는다.
- **`rawbytes` 가 아닌 capture/assert 는 decoded·decompressed 본문 기준이다** — gzip 응답의 바이트 길이나 원본 인코딩을 검증하려 했는데 디코딩된 값이 비교돼 통과해 버린다. 바이트 수준 계약은 `rawbytes` 로 명시한다.
- **redirect follow 는 기본으로 꺼져 있다** — `3xx` 를 받고 assert 가 실패하면 계약 위반처럼 보이지만 실제로는 follow 미설정이다. 필요하면 entry 의 `location: true` 또는 `--location` 을 켠다.
- **`--very-verbose` 는 request/response body 를 stderr 에 출력한다** — 다만 `--secret` 을 걸어두면 그 값은 `***` 로 바뀐다(실측). 문제는 등록하지 않은 변형본이다 — base64 본은 그대로 남는다.
- **`--verbose` 로는 body 가 안 찍힌다** — 그래서 `--verbose` 로그에 토큰이 없다는 관측은 마스킹의 증거가 아니다. body 가 찍히는 건 `--very-verbose` 부터다.
- **`redact` capture 와 `--very-verbose` 는 함께 못 쓴다** — Hurl 8.0.1 이 `redacted secret not authorized in verbose` 로 실행을 거부한다.
- **exit code `1` 은 계약과 무관하다** — CLI 파싱 실패다. 오타 난 플래그 하나로 `1` 이 나오는데, 이걸 실패 통계에 넣으면 계약 회귀처럼 보인다.
