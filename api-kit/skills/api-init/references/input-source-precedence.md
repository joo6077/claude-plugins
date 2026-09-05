# 입력 소스 우선순위

`/api-init` 이 여러 입력을 하나의 operation 인벤토리로 합칠 때 쓰는 탐색 경로, 신뢰도, 충돌 판정 절차.

근거는 `docs/api/discovery/api-inventory-normalization.md` 와 `docs/api/discovery/artifact-interop-import-export.md` 다. 이 문서는 그 규칙을 초기화 실행 순서로 옮긴 것이다.

---

## 1. 스펙 탐색 경로

### 로컬 파일 (먼저)

```bash
find . -maxdepth 4 \
  \( -name 'openapi.json' -o -name 'openapi.yaml' -o -name 'openapi.yml' \
     -o -name 'swagger.json' -o -name 'swagger.yaml' -o -name 'swagger.yml' \
     -o -name 'api-docs.json' \) \
  -not -path './node_modules/*' -not -path './.git/*' \
  -not -path './target/*' -not -path './build/*' -not -path './dist/*'
```

프레임워크별 관례 경로도 같이 본다.

| 위치 | 흔한 출처 |
|------|-----------|
| `docs/` · `api/` · `spec/` · `openapi/` | 수동 관리 스펙 |
| `src/main/resources/` | Spring |
| `static/` · `public/` | 빌드 산출물이 그대로 서빙되는 경우 |
| `.talend/` · `*.postman_collection.json` | GUI 도구 export |
| `*.har` | 브라우저·프록시 캡처 |

### 라이브 엔드포인트 (baseUrl 확정 후에만)

`allowHosts` 가 정해지기 전에는 조회하지 않는다. 이 시점엔 안전 게이트가 없다.

| 경로 | 프레임워크 |
|------|-----------|
| `/v3/api-docs` · `/v3/api-docs.yaml` | springdoc |
| `/openapi.json` · `/openapi.yaml` | FastAPI, utoipa, 다수 |
| `/swagger/v1/swagger.json` | ASP.NET Core |
| `/swagger.json` | 구형 springfox 등 |
| `/api-docs` | Rails rswag 등 |

응답이 200 이어도 OpenAPI/Swagger 스키마가 아니면 버린다. `openapi` 또는 `swagger` 최상위 필드 존재를 확인한다.

---

## 2. 소스 신뢰도 매트릭스

| 소스 | 기본 confidence | 성격 | 상한 |
|------|-----------------|------|------|
| 유효한 OpenAPI/Swagger | `1.00` | 계약 설명 | — |
| curl · Talend · HAR (관측 덤프) | `0.80` | 실제로 본 호출 증거 | curl import 는 `0.85` |
| 사람이 쓴 md · 노션 · 스크린샷 | `0.55` | 설명 증거 | — |
| 추론으로 만든 값 (synthetic) | `0.35` | 근거 없음 | 계약 근거로 승격 금지 |

**신뢰도는 정렬 기준이지 덮어쓰기 권한이 아니다.** 1.00 짜리 소스가 0.80 짜리 값을 자동으로 대체하면 스펙과 실호출의 drift 가 사라진다. 인벤토리의 존재 이유가 바로 그 drift 를 남기는 것이다.

모든 필드에 `provenance`(소스 타입 + 원본 위치)를 붙인다. provenance 없는 필드는 인벤토리에 넣지 않는다.

### 소스별 성격 차이

- **OpenAPI** — 유일하게 schema 계약을 주장할 수 있는 소스다. 다만 문서와 실제 응답이 어긋나는 게 정상이라는 게 이 킷의 전제이므로, "스펙이 이러니 맞다" 로 probe 결과를 기각하지 않는다.
- **curl / Talend / HAR** — 실행 예시다. 요청 형태의 증거로는 강하지만 schema 계약의 근거는 아니다. operation 후보의 신뢰도를 보강하는 용도로만 쓴다.
- **md** — 설명 증거다. auth·baseUrl·환경을 생략하는 게 보통이므로 누락 필드를 채우지 말고 `unknown` 으로 남긴다.
- **HAR** — transaction archive 이지 operation 계약이 아니다. OpenAPI 대체물로 쓰지 마라.

---

## 3. 소스별 파싱 주의

### curl

- 공백 split 파서 금지. quoting, 줄바꿈 이어쓰기(`\`), `@file` 참조를 처리한다.
- 옵션은 URL 앞뒤 어디에나 올 수 있고 `--header`, `--url-query` 는 반복 가능하다.
- `--data` / `--data-binary` / `--data-urlencode` / `--form` / `--get` 은 서로 다른 wire 결과를 만든다. 하나로 뭉치지 말고 인코딩을 그대로 기록한다.
- Hurl 의 `--curl` 은 **export 전용**이다. curl 을 읽어들이는 기능이 아니므로 import 에 쓰지 마라.

### Talend

- project / service / scenario 계층을 평탄화하지 않는다. provenance 와 환경 매핑으로 보존한다.
- operation-level Try 로 만든 draft 는 project 계층이 비어 있다. "불완전한 관측치" 로 취급한다.
- Talend portal 의 contract download 포맷은 OAS `3.0` 또는 Swagger `2.0` 이다.
- 환경변수·auth 값을 `.hurl` 이나 인벤토리에 inline 하지 마라. 환경 매핑으로만 남긴다.

### HAR

- `log.version` 은 required, api-kit 은 `1.2` 를 쓴다. UTF-8 저장 required.
- HTTP request 1개 = HAR entry 1개.
- `queryString` 은 같은 name 이 반복될 수 있다. map 으로 바꾸면 `?tag=a&tag=b` 의 뒤 값만 남아 조용히 손실된다. 배열(`{name, value}` 리스트)로 유지한다.
- request URL 은 absolute URL 이고 fragment 를 포함하지 않는다. 상대 경로면 base URL 을 합치고 `#` 이후는 버린다.
- `postData.text` 와 `postData.params` 는 상호 배타다.
- timing 단위는 ms, unavailable/not applicable 은 `-1`.

### OpenAPI

- `servers` 가 없으면 기본 server URL 은 `/` 다.
- operation-level `security` 가 top-level `security` 를 override 한다. 배열 원소 간은 OR, 한 객체 안 여러 scheme 은 AND.
- OAuth2/OIDC scheme 의 값 배열은 scope 목록이고, 그 외 scheme 은 빈 배열이어야 한다.
- linkback 은 가능하면 `operationRef`(JSON Pointer), 없으면 `operationId` 로 저장한다. name clash 가능성 때문에 external reference 에서는 `operationRef` 를 선호한다.

---

## 4. 충돌 판정 절차

```text
1. canonical key 생성
   METHOD + 정규화된 path template
   operationId 는 aliases 컬럼으로만

2. path 우선순위
   concrete > templated                     /users/me  >  /users/{id}
   변수명만 다른 동일 hierarchy 는 무효      /users/{id} vs /users/{name}
   모호하면 임의 선택 금지 → conflict

3. 파라미터 정규화
   키는 (in, name) 쌍
   in 은 path / query / header / cookie 넷으로만
   in: path 는 required 강제
   header 만 case-fold 비교, 나머지는 원문 그대로

4. 예약 헤더 분리
   Accept          ← 기대 response media type
   Content-Type    ← requestBody media type
   Authorization   ← security requirement
   셋 다 파라미터 테이블에 넣지 않는다

5. media type 선택
   가장 구체적인 key 하나만 적용     text/plain > text/*
   wildcard 는 fallback 후보 목록에만

6. auth scope 매핑
   operation-level security 가 top-level 을 override

7. auto-collapse 판정
   method·path-template exact match
   AND param-set Jaccard >= 0.80
   → 하나로 합친다

8. conflict 판정
   method / path template / parameter location / auth scheme / media type
   중 하나라도 충돌 → 병합하지 않고 conflict 레코드 보존
   top-2 후보 confidence 차이 < 0.15 → needs_review
```

### 허용치

| 항목 | 값 |
|------|-----|
| operation 내 `(name, in)` 중복 | `0` |
| 같은 hierarchy 내 path template ambiguity | `0` |
| header name case 구분 | `0` (case-insensitive 비교) |
| lossy conversion 경고 임계 | unsupported/unknown field `> 0` |

---

## 5. 커버리지 3축

합산하지 않는다. 합치면 스펙에 없는 실호출이 커버리지에 흡수되어 블랙박스 검증의 핵심 신호가 사라진다.

| 축 | 세는 것 |
|----|---------|
| OpenAPI operation | 스펙에 정의된 operation 수 |
| observed-only request | 스펙에 없는데 덤프·probe 에서 관측된 호출 |
| generated probe | 실제로 `.hurl` 이 합성된 operation |

`needs_review`, "불완전한 관측치", lossy conversion 경고는 커버리지와 별도로 센다.

---

## 6. 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| `operationId` 만으로 dedupe | 선택 필드라 외부 덤프에는 대부분 없어 dedupe 가 동작하지 않는다 |
| raw path 문자열만 비교 | `/users/me` 와 `/users/{id}` 우선순위를 놓쳐 잘못된 operation 에 probe 를 붙인다 |
| path/query/header/cookie 를 한 namespace 에 병합 | 이름이 같고 위치가 다른 파라미터가 서로를 덮어써 사라진다 |
| `Authorization` 을 일반 header parameter 로 저장 | auth scheme·scope 판단 경로가 끊겨 인증 요구사항을 재현할 수 없다 |
| 충돌 시 가장 최신 파일만 채택 | 스펙과 실호출의 drift 를 숨긴다 |
| md·curl 의 누락 필드를 기본값으로 채움 | 스펙과의 diff 가 가짜로 사라진다 |
| linkback 없이 인벤토리 생성 | 실패를 원래 OpenAPI operation 으로 되돌릴 수 없다 |

---

## 7. artifact 버전 정책

모든 산출물에 `schemaVersion` 을 넣는다. 읽을 때의 호환 정책은 다음과 같다.

| 상황 | 처리 |
|------|------|
| major mismatch | reject |
| newer minor | warn 후 진행 |
| patch 차이 | accept |

스펙이 정의하지 않는 부가 정보는 임의 필드로 흘리지 말고 OpenAPI 의 `x-` prefix 확장으로 보존한다.
