---
title: 생태계 입출력 상호운용
version: 0.1.0
last_updated: 2026-09-04
---

# 생태계 입출력 상호운용

curl·Talend·HAR·OpenAPI 를 읽어들이고 `.hurl`·HAR·JUnit 으로 내보낼 때의 변환 규칙. 재현 단위, 원본 linkback, 손실 경고 정책을 다룬다.

---

## 원칙

### 1. Curl Import Fidelity

curl 덤프는 shell tokenization 과 curl option 의미론을 보존해 파싱한다. 옵션은 URL 앞뒤 어디에나 올 수 있고 `--header`, `--url-query` 처럼 반복 가능한 옵션이 있으므로, 공백 split 기반 파서를 쓰지 않는다. quoting, 줄바꿈 이어쓰기, `@file` 참조를 모두 처리한다.

> **출처:** [curl manpage](https://curl.se/docs/manpage.html), [everything.curl.dev — Command line options](https://everything.curl.dev/cmdline/options/index.html)

### 2. Curl Body/Form Semantics Boundary

`--data`, `--data-binary`, `--data-urlencode`, `--form`, `--get` 은 서로 다른 wire 결과를 만든다. 하나로 뭉뚱그리지 않고 각각의 인코딩을 그대로 재현한다. 다만 curl 한 줄은 실행 예시이지 schema 계약이 아니므로, operation 후보의 신뢰도를 **보강하는 증거** 로만 쓰고 계약의 근거로 승격하지 않는다.

> **출처:** [curl manpage](https://curl.se/docs/manpage.html)

### 3. Talend Dump Mapping

Talend API Tester 는 Swagger/OpenAPI/HAR import 를 지원하고, Talend portal 의 Try flow 는 operation, query/header, `BaseUrl`, auth 환경변수를 함께 생성한다. 따라서 Talend 덤프의 project / service / scenario 계층은 평탄화하지 말고 provenance 와 환경 매핑으로 보존한다.

> **출처:** [Talend API Tester — Importing requests](https://help.qlik.com/talend/en-US/api-tester-user-guide/Cloud/importing-requests), [Talend Qlik Developer Portal](https://talend.qlik.dev/getting-started/)

### 4. OpenAPI Linkback

변환된 probe 와 export artifact 에는 원본으로 되돌아갈 참조를 반드시 저장한다. 가능하면 `operationRef`(JSON Pointer)를, 없으면 `operationId` 를 쓴다. OpenAPI 는 name clash 가능성 때문에 external reference 에서 `operationRef` 를 선호한다.

> **출처:** [OpenAPI 3.1.0 Link Object](https://spec.openapis.org/oas/v3.1.0#link-object)

### 5. HAR Export

실행된 HTTP transaction 은 HAR 1.2 `entries` 로 내보낸다. request 에는 method, absolute URL, headers, cookies, queryString, postData 를 넣고, response 에는 status, headers, content, timing 을 넣는다. HAR 는 실행 관측 기록이고 계약이 아니다.

> **출처:** [HAR 1.2 Spec](https://w3c.github.io/web-performance/specs/HAR/Overview.html)

### 6. JUnit Export

JUnit XML 은 재현 artifact 가 아니라 CI 결과 요약이다. Hurl 8.0.1 의 JUnit report 는 `.hurl` 파일 하나를 testcase 하나로 매핑하며, assert error 는 `failure`, runtime error 는 `error` 로 표현한다. 이 매핑을 임의로 바꾸면 CI 대시보드의 실패 분류가 계약 실패와 환경 실패를 구분하지 못한다.

> **출처:** [Hurl Running Tests](https://hurl.dev/docs/running-tests.html), [hurl::report::junit](https://docs.rs/hurl/latest/hurl/report/junit/index.html)

### 7. Hurl Reproducer Export

api-kit 의 재현 단위는 `.hurl` 파일이다. Hurl 은 plain-text HTTP request, response assert, capture, variable chaining 을 한 파일에 담으므로 실패를 그대로 재실행할 수 있다. 외부 공유용으로 curl 명령이 필요하면 `--curl` 로 부가 산출물을 뽑되, 재현 SSOT 는 `.hurl` 로 유지한다.

> **출처:** [Hurl Manual](https://hurl.dev/docs/manual.html), [Hurl File Format](https://hurl.dev/docs/hurl-file.html)

### 8. Lossy Conversion Warning

import/export 마다 source type, source version, 원본 hash, 처리하지 못한 필드 목록을 기록한다. unsupported/unknown 필드가 하나라도 있으면 경고를 낸다. 블랙박스 계약 검증에서 조용한 필드 손실은 곧 false pass 이므로, 손실은 무시가 아니라 보고 대상이다.

> **출처:** [HAR 1.2 Spec](https://w3c.github.io/web-performance/specs/HAR/Overview.html)

### 9. Artifact Schema Versioning

모든 artifact 는 버전 필드를 갖는다. OpenAPI 는 `openapi`, HAR 는 `log.version` 을 요구하며, api-kit 자체 artifact 도 `schemaVersion` 을 명시한다. 스펙이 정의하지 않는 부가 정보는 임의 필드로 흘리지 말고 OpenAPI 의 `x-` prefix 확장으로 보존한다.

> **출처:** [OpenAPI 3.1.0 OpenAPI Object](https://spec.openapis.org/oas/v3.1.0#openapi-object), [HAR 1.2 Spec](https://w3c.github.io/web-performance/specs/HAR/Overview.html)

---

## 수치 기준

| 항목 | 값 | 근거 |
|------|-----|------|
| HAR export 버전 | `log.version` required, api-kit 은 `1.2`. UTF-8 저장 required | [HAR 1.2 Spec](https://w3c.github.io/web-performance/specs/HAR/Overview.html) |
| HAR entry cardinality | HTTP request `1개` → HAR entry `1개` | [HAR 1.2 Spec](https://w3c.github.io/web-performance/specs/HAR/Overview.html) |
| HAR timing 단위 | milliseconds. unavailable / not applicable 은 `-1` | [HAR 1.2 Spec](https://w3c.github.io/web-performance/specs/HAR/Overview.html) |
| HAR `postData.text` 와 `postData.params` | 상호 배타 — 둘 중 하나만 채운다 | [HAR 1.2 Spec](https://w3c.github.io/web-performance/specs/HAR/Overview.html) |
| Talend portal contract download 포맷 | OAS `3.0` 또는 Swagger `2.0` | [Talend Qlik Developer Portal](https://talend.qlik.dev/getting-started/) |
| Hurl JUnit 매핑 | `.hurl` 파일 `1개` → `<testcase>` `1개` | [hurl::report::junit](https://docs.rs/hurl/latest/hurl/report/junit/index.html) |
| artifact `schemaVersion` 호환 정책 | major mismatch = reject, newer minor = warn, patch = accept | 추론 |
| lossy conversion 경고 임계 | unsupported/unknown field `> 0` | 추론 |
| curl import confidence 상한 | `0.85` | 추론 |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| curl 덤프를 공백 split 으로 파싱 | quoting, `@file` 참조, 반복 옵션이 깨져 잘못된 요청을 생성한다 |
| HAR 를 OpenAPI 대체물로 사용 | HAR 는 transaction archive 이지 schema/operation 계약이 아니다 |
| JUnit 만 저장하고 `.hurl`·HAR 를 폐기 | CI 요약만 남아 실패를 재현할 수 없다 |
| Talend 환경변수·auth 값을 `.hurl` 에 inline | 시크릿이 파일에 박히고 환경이 고정돼 다른 stage 에서 못 돌린다 |
| linkback 없는 export | 실패를 원래 OpenAPI operation 으로 되돌릴 수 없어 계약 diff 가 불가능하다 |

---

## Gotchas

- **HAR `queryString` 은 같은 name 이 반복될 수 있다** — map/dict 로 변환하면 `?tag=a&tag=b` 의 뒤 값만 남아 조용히 손실된다. 배열(list of `{name, value}`)로 유지한다.
- **HAR request URL 은 absolute URL 이고 fragment 를 포함하지 않는다** — 상대 경로나 `#` 이후를 그대로 넣으면 스펙 위반이다. base URL 을 합쳐 절대 URL 로 만들고 fragment 는 버린다.
- **Hurl `--curl` 은 export 전용이다** — Hurl 에서 curl 명령을 뽑는 기능이지 curl 을 읽어들이는 기능이 아니다. curl import 는 별도 파서가 필요하다.
- **Talend 의 operation-level Try 는 draft request 만 만든다** — 전체 project 가 생성된다고 가정하고 project/service 계층을 찾으면 비어 있다. 단건 draft 는 "불완전한 관측치" 로 취급한다.
