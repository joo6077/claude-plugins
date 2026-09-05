---
name: api-probe
description: >
  인벤토리의 엔드포인트를 실제로 호출해서 응답을 눈으로 확인하고 스냅샷으로 봉인한다.
  `.hurl` 을 합성해 실행하고, 시크릿을 스크러빙한 뒤 마크다운 리포트와 `.api/snapshots/*.json` 을 남긴다.
  "API 때려봐", "엔드포인트 찔러봐", "api probe", "응답 찍어줘" 같은 요청 시 트리거.
  `.api/inventory.yaml` 이 없으면 트리거하지 않는다 — `/api-init` 을 먼저 돌린다.
  이미 만들어진 계약을 회귀 실행하는 요청에는 트리거하지 않는다 — `/api-verify` 를 쓴다.
argument-hint: "<endpoint|group> [--env dev] [--query k=v] [--header 'K: V'] [--body '{...}']"
user-invocable: true
---

## Gotchas

- **Hurl `--secret` 은 stdout 을 가리지 않는다. 스냅샷 저장 전에 킷 자체 scrubber 를 반드시 거친다** — `--secret` 이 마스킹하는 건 stderr 로그와 리포트뿐이다. 기본 stdout, `--include`, `--json` stdout, JSON 리포트의 raw response body 에는 토큰이 평문으로 남는다. Hurl 이 응답 stdout 을 "unaltered output" 으로 취급하기 때문이다. 응답을 파일로 남기는 **모든** 경로에 자체 redaction 을 걸어라. 같은 이유로 `--very-verbose` 를 무심코 켜지 마라 — request/response body 를 stderr 로 뱉으므로 CI 로그에 그대로 남는다. 진단으로 켤 때는 redaction 을 함께 걸고 그 출력을 artifact 로 흘리지 않는다. (`docs/api/execution/auth-secret-lifecycle.md` §6, `probe-synthesis-hurl-semantics.md` Gotchas)
- **redaction 에 실패하면 스냅샷을 저장하지 않는다 (fail-closed)** — 부분 마스킹 결과를 "일단 저장하고 나중에 정리" 하지 마라. 리포트를 만든 뒤 마스킹하면 이미 파일과 CI 로그에 비밀이 남는다. redaction 은 저장 파이프라인의 마지막 보정이 아니라 **통과해야 하는 게이트**다. (`docs/api/verification/regression-diff-failure-policy.md` Gotchas)
- **`--secret` 은 exact value 매칭이다** — 값 하나당 등록 하나. base64 인코딩본, 대소문자 변환본, `Bearer ` 접두를 포함한 형태는 각각 별도 secret 으로 등록해야 한다. 하나라도 빠지면 그 형태로 로그에 노출된다. 자체 scrubber 의 deny 패턴에도 같은 변형을 넣어라. (`auth-secret-lifecycle.md` §5)
- **prod 는 기본 GET/HEAD/OPTIONS 만이고, 그 판정을 메서드 이름에만 맡기지 마라** — 쓰기 메서드는 env + host + path + method 4중 일치 allowlist 항목이 있을 때만 열린다. `PUT`/`DELETE` 가 idempotent 라는 사실은 재시도 판단 근거이지 실행 허용 근거가 아니고, "검증 목적" 은 상태 변경 면책이 되지 않는다. 반대 방향의 함정도 있다 — `GET /orders/{id}/refresh-cache` 처럼 메서드는 safe 인데 서버 동작이 mutation 인 엔드포인트가 실무에 존재한다. 인벤토리의 `sideEffect: true` 를 먼저 보고, 표시가 없어도 path 패턴이 의심스러우면 사용자에게 확인한다. `TRACE` 는 RFC 상 safe 로 분류되지만 요청을 loop-back 해 `Authorization` 헤더가 응답 본문에 실려 오므로 허용 0회다. prod read-only 의 정확한 범위는 아직 미확정이니 임의로 넓히지 마라. (`docs/api/execution/environment-safety-gates.md` §1~§4)
- **URL 문자열 query 와 `[Query]` 섹션을 동시에 만들지 마라** — Hurl 은 둘 다 있으면 둘 다 전송한다. 같은 파라미터가 중복되어 서버가 뭘 받았는지 알 수 없게 된다. 기본은 `[Query]` 섹션 한 경로로 통일한다. (`docs/api/execution/probe-synthesis-hurl-semantics.md` §2)
- **상태를 공유하는 흐름은 반드시 한 `.hurl` 파일 안에 둔다** — Hurl 은 같은 파일 안에서만 cookie store 를 공유하고, `--test` 는 파일 단위 **병렬** 실행이 기본이다. 로그인 → 조회 → 삭제를 파일 세 개로 쪼개면 실행 순서를 보장받지 못한다. 파일 경계가 곧 격리 경계다. (`probe-synthesis-hurl-semantics.md` §5)
- **exit code 로 실패를 분류하고, non-zero 를 전부 계약 실패로 보고하지 마라** — `4`(assert)만 계약 위반이다. `3`(runtime)은 DNS/TLS/timeout/connect 를 전부 포함하는 환경 실패이므로 계약 판정을 보류하고, `2`(input parse)는 probe 생성 버그이며, `1`은 CLI 옵션 오류라 재시도해도 소용없다. `3` 은 exit code 만으로 원인을 알 수 없으니 리포트에 subreason 필드를 따로 남긴다. (`probe-synthesis-hurl-semantics.md` §9, `regression-diff-failure-policy.md`)
- **redirect follow 는 기본으로 꺼져 있다** — `3xx` 를 받고 assert 가 실패하면 계약 위반처럼 보이지만 실제로는 follow 미설정인 경우가 많다. 필요하면 entry 의 `location: true` 또는 `--location` 을 켜되, cross-host redirect 는 0회다. `--location-trusted` 는 리다이렉트된 임의 host 로 자격증명을 전달하므로 기본 금지 옵션으로 취급한다. (`environment-safety-gates.md` §6)
- **부하와 타임아웃은 쏘기 전에 숫자로 확정한다** — 부하는 메서드 하나가 아니라 총량이다. 실행 전에 `파일 수 × 요청 수 × --repeat × --jobs` 를 계산해 상한과 비교하라. `--jobs` 기본값이 CPU 수 기반이라 단일 파일 감각으로 잡으면 prod 부하가 배로 커진다(prod 는 `--jobs 1` 고정). safe 메서드도 반복·병렬이면 서버에 부담이다. 그리고 `connect-timeout` 과 `max-time` 은 **둘 다** 있어야 한다 — 하나만 있으면 나머지가 무한이다. `project.yaml` 의 env 기본값을 주입하고, 그래도 비어 있으면 실행을 막는다. (`environment-safety-gates.md` §7·§8·§9)
- **스냅샷은 pretty-print 결과가 아니라 시크릿만 마스킹한 raw 를 보관한다** — 화면 표시용 포매팅은 비교 기준선이 될 수 없다. 표시 포매터가 바뀌면 계약이 통째로 깨진다. 원본 헤더 라인, 상태코드, 바이트 digest 를 그대로 남기고, 비교 기준선(JCS canonical)은 거기서 파생시킨다. 배열을 "안정화한다며" 정렬하지 마라 — JCS 는 object property 만 정렬하고 array order 는 보존한다. (`docs/api/contract/snapshot-sealing-canonicalization.md` §1·§2, 안티패턴)
- **probe 는 계약을 확정하지 않는다** — 스냅샷 하나로 `required` 나 `enum` 을 단정하면 optional 필드가 required 로 굳는다. enum 은 1 샘플에서는 후보 표시 + 경고까지만이고 승격은 독립 샘플 3개 이상에서 한다. 타입 추론 표는 초안이라는 걸 리포트에 명시하고, 확정은 `/api-contract` 로 넘긴다. (`docs/api/contract/contract-extraction-modes.md` 수치 기준)
- **`GET` 에 requestBody 를 기본으로 만들지 마라** — 스펙에 `GET` + requestBody 가 적혀 있어도 문법상 허용될 뿐 의미가 정의돼 있지 않다. 서버·프록시마다 처리가 달라 실패가 계약 위반인지 전송 계층 문제인지 구분되지 않는다. 사용자가 `--body` 로 명시할 때만 붙인다. (`docs/api/discovery/api-inventory-normalization.md` Gotchas)

# 엔드포인트 탐색 실행

## 0. 사전 조건 확인

```bash
test -f .api/inventory.yaml || echo "NO_INVENTORY"
test -f .api/project.yaml   || echo "NO_PROJECT"
hurl --version || echo "NO_HURL"
```

- `NO_INVENTORY` 또는 `NO_PROJECT` 면 중단하고 `/api-init` 을 먼저 실행하도록 안내한다.
- `NO_HURL` 이면 설치 안내 후 중단한다. 대체 도구로 우회하지 마라 — 재현 SSOT 가 `.hurl` 이다.
- 자격증명 파일을 쓰는 프로파일이면 매 실행 전에 추적 여부를 검사한다.

```bash
git ls-files --error-unmatch .api/credentials.local.json 2>/dev/null && echo TRACKED_ABORT
```

`TRACKED_ABORT` 면 즉시 중단한다.

---

## 1. 대상 확정

`$ARGUMENTS` 를 인벤토리 키로 해석한다.

| 입력 형태 | 해석 |
|-----------|------|
| `orders.list` | 그룹 `orders` 의 operation 별칭 |
| `GET /orders` | canonical key 직접 지정 |
| `orders` | 그룹 전체 — operation 목록을 보여주고 확인받는다 |

- 매칭 후보가 여러 개면 임의로 고르지 말고 목록을 제시한다.
- `needsReview: true` 인 operation 이면 어떤 필드가 충돌 중인지 먼저 보여준다. 그래도 실행할지 확인받는다.
- `--query` / `--header` / `--body` 로 들어온 추가 값은 인벤토리에 없더라도 그대로 반영한다. `--body` 가 있으면 `Content-Type: application/json` 을 자동으로 붙인다.

---

## 2. 안전 게이트 판정

`references/hurl-execution.md` §안전 게이트의 7단계를 순서대로 실행한다.

```text
1. method class 판정   safe(GET·HEAD·OPTIONS) / unsafe(POST·PUT·PATCH·DELETE) / 금지(TRACE)
2. env 정책 조회       tier: prod → read-only 기본
3. allowlist 조회      env + host + path + method 4중 일치
4. retry 정책 판정     멱등 아니면 0회
5. redirect 정책 판정  cross-host 차단, same-origin 상한 3회
6. 부하 예산 계산      파일 × 요청 × repeat × jobs
7. 타임아웃 주입 확인  connect-timeout + max-time 둘 다
```

호스트 검사는 별도로 한 번 더 건다. 최종 URL 의 호스트가 `allowHosts` 에 없으면 **무조건 차단**한다. baseUrl 변수 오염으로 stg 케이스가 prod 를 때리는 사고를 막는 장치다.

prod 에서 unsafe 메서드를 실행해야 하면, 실행 전에 대상 목록(메서드 + 전체 URL + 예상 요청 수)을 보여주고 사용자 확인을 받는다. 확인 없이 진행하지 마라.

`sideEffect: true` 인 operation 은 메서드가 GET 이어도 unsafe 로 취급한다.

---

## 3. 토큰 발급

환경의 `authProfile` 로 토큰을 확보한다. 별도 스킬을 부르지 않는다 — 이 단계가 인증 담당이다.

```text
1. 캐시 조회      ~/.cache/api-kit/<키해시>
                  키 = env + profile + tokenUrl + clientId + scope + usernameHash
2. 유효성 판정    now < refresh_at 이면 캐시 사용
                  refresh_at = expires_at - max(60s, TTL의 10%)
3. 재발급         client_credentials 는 refresh token 이 없다 (RFC 6749 §4.4.3)
                  custom_login 은 credentialsFile 을 다시 읽어 재로그인
4. 락             병렬 실행 시 파일 락. 여러 케이스가 동시에 IdP 를 두들기지 않게
5. 저장           디렉토리 0700 / 파일 0600
```

- `expires_in` 이 응답에도 프로파일 기본값(`fallbackTtlSeconds`)에도 없으면 **자동 갱신을 추측하지 말고 금지**한다. 매 실행 재발급으로 되돌린다.
- TTL 이 skew 보다 짧으면 캐시를 세션 한정으로 전환한다.
- 발급 실패는 리소스 접근 실패와 다른 축으로 분류한다. token endpoint 오류는 `invalid_client` / `invalid_grant` / `invalid_scope`, 리소스 접근 오류는 `invalid_token`(401) / `insufficient_scope`(403). 전부 "login failed" 로 합치면 재시도 판단이 불가능해진다.
- 응답 scope 가 요청과 다르면 요청값이 아니라 **실제 granted scope** 를 기준으로 이후 판정을 한다.

발급한 토큰과 그 변형(`Bearer ` 접두본, base64 본)을 전부 secret 등록 목록에 넣는다. 자격증명 파일의 id/password 값도 같이 넣는다.

---

## 4. `.hurl` 합성

`references/hurl-execution.md` §파일 합성 규칙을 따른다. 값 생성 우선순위는 media type 의 explicit `example`/`examples` → schema `example` → JSON Schema `default` → `const`/`enum` 이다. `default` 는 annotation 이라 schema 를 만족한다는 보장이 없으므로, 값을 고른 뒤 schema 검증을 한 번 더 돌린다.

```hurl
# .api/cases/orders.list.hurl
GET {{baseUrl}}/orders
[Query]
status: active
limit: 10
[Headers]
Accept: application/json
Authorization: Bearer {{access_token}}
[Options]
connect-timeout: 5
max-time: 30

HTTP 200
```

- `Accept` · `Content-Type` · `Authorization` 세 헤더는 추론에 맡기지 말고 명시한다. 생략하면 클라이언트 기본값이 끼어들어 실패 원인이 계약인지 전송인지 구분되지 않는다.
- 토큰 값은 파일에 쓰지 않는다. `{{access_token}}` 만 남기고 실제 값은 임시 `--secrets-file` 로 넘긴다.
- probe 단계의 최소 assert 는 expected HTTP status 하나다. body 전체 capture 는 켜지 않는다 — 리포트가 비대해지고 토큰이 로그에 남는다.
- 의존 흐름이면 한 파일에 entry 를 이어 쓰고 `[Captures]` 로 필요한 값만 뽑는다. 체인 안에서 capture 이름을 재사용하지 마라 — 뒤 값이 앞 값을 덮는다.
- operation 당 생성 probe 는 기본 1개(preferred media type), explicit examples 가 여럿이면 최대 3개다.

---

## 5. 실행

```bash
hurl --test \
     --jobs 1 \
     --secrets-file "$SECRETS" \
     --connect-timeout 5 \
     --max-time 30 \
     --json \
     .api/cases/orders.list.hurl > "$RAW_OUT" 2> "$LOG_OUT"
echo "exit=$?"
```

- 옵션 우선순위는 environment variable < command-line option < per-entry `[Options]` 다. 뒤쪽이 이긴다. cli-only 옵션을 `[Options]` 에 적지 마라 — 무시되어 파일에 적힌 실행 의미와 실제 실행이 달라진다.
- `--continue-on-error` 는 서로 독립인 probe 배치에만 켠다. dependency chain 에서 켜면 오염된 변수로 후속 요청이 돌아 전이 실패가 난다. auth 실패 뒤에는 절대 켜지 않는다.
- `--retry` 를 파일 전체에 걸지 마라. Hurl 의 재시도는 HTTP 실패뿐 아니라 assert·capture·runtime 오류에도 걸리므로, 게이트가 멱등 요청만 좁게 잘라야 한다.
- 실행 직후 `$SECRETS` 임시 파일을 지운다.

---

## 6. 실패 분류

| exit | 의미 | 분류 | 처리 |
|------|------|------|------|
| `0` | 성공 | — | 스냅샷 저장 진행 |
| `1` | CLI 옵션 파싱 오류 | 도구 사용 오류 | 실행 중단, 재시도 금지 |
| `2` | 입력(.hurl) 파싱 오류 | probe 생성 버그 | 합성 로직 수정 |
| `3` | 런타임 오류 (DNS/TLS/connect/timeout) | 환경 실패 | 계약 판정 보류, subreason 기록 |
| `4` | assert 실패 | 계약 신호 | 리포트에 기록, 스냅샷은 저장 |

`404` 는 원인이 둘이다 — 진짜 데이터 부재일 수도, 존재를 감추는 `403` 대체 정책일 수도 있다. 한쪽으로 단정하지 말고 두 후보를 리포트에 남긴다.

`4xx`/`5xx` 응답도 스냅샷 대상이다. 다만 오류 본문은 최대 8KB 샘플까지만 비교 대상으로 잡고, 5xx 본문에 exact 를 걸지 않는다.

---

## 7. 스크러빙 → 정규화 → 저장

**순서를 바꾸지 마라.** 이 순서가 곧 fail-closed 게이트다.

```text
1. scrub      키 이름 deny list + 값 형태 정규식(JWT·이메일·전화·카드번호) + 등록된 시크릿 값
              → 하나라도 처리 실패하면 여기서 중단. 저장하지 않는다
2. I-JSON 검문 중복 키 · lone surrogate · NaN/Infinity · binary64 표현 불가 숫자
              → 정규화 대상이 아니라 실패/fallback 대상
3. raw 봉인    상태코드 · 원본 헤더 라인 · 바이트 digest · 시크릿만 마스킹한 본문
4. normalized  타임스탬프·UUID·커서를 sentinel 로, 부동소수 정밀도 고정
              → RFC 8785 JCS canonical JSON 으로 직렬화 (비교 기준선)
5. manifest    raw digest · normalized JCS digest · redaction registry 버전
              · media type · extraction mode → 이 매니페스트의 digest 가 baseline id
```

저장 위치:

```text
.api/snapshots/dev/orders.list.json     커밋한다 — 회귀 diff 기준선
.api/snapshots/prod/orders.list.json    커밋하지 않는다 — 실 고객 데이터
```

`Content-Encoding: gzip` 이면 digest 가 둘이다. raw content bytes digest 와 decoded representation digest 를 구분해 매니페스트에 기록한다. `application/json; charset=utf-8` 의 charset 은 파싱 근거가 아니지만 증거에는 원문 그대로 남긴다.

Unicode normalization(NFC/NFD)은 하지 않는다. 화면상 같아 보여도 JCS digest 는 다르다.

---

## 8. 리포트

마크다운으로 출력한다. 스냅샷 파일 경로를 반드시 포함한다.

```markdown
## GET /orders — dev

- 상태: `200 OK` · 412ms · exit `0`
- 스냅샷: `.api/snapshots/dev/orders.list.json` (baseline `sha-256:8f3a…`)
- 실행: `hurl --test --jobs 1` · 요청 1건

### 헤더 (요약)

| 이름 | 값 |
|------|-----|
| content-type | application/json |
| x-request-id | `<masked>` |

### 본문

(스크러빙·정규화 후 표시용 포매팅. 비교 기준선은 JCS 산출물이며 이 표시가 아니다)

### 추론된 필드 타입 — 초안

| 필드 | 타입 | 관측 | 비고 |
|------|------|------|------|
| `$.data[].id` | string | 1/1 | 패턴 `^ord_` 후보 |
| `$.data[].status` | string | 1/1 | enum 후보 (1 샘플 — 승격 불가, 3 샘플 필요) |
| `$.meta.total` | integer | 1/1 | 변동 수치 — 값 고정 금지 |

> 이 표는 초안이다. `required` / `optional` / enum 확정은 `/api-contract` 에서 한다.
```

- 필드 타입 표에 `required` 를 단정해 쓰지 마라. 1 샘플에서는 presence 만 적는다.
- 실패했으면 `실패 원인` 을 본문보다 **앞에** 둔다.
- 리포트를 만들기 전에 §7 의 스크러빙이 끝나 있어야 한다. 리포트 생성 후 마스킹하면 이미 늦다.

다음 단계를 안내한다.

> 같은 엔드포인트를 3회 이상 샘플링하면 `/api-contract` 가 enum·required 를 승격할 수 있습니다.
> 스냅샷이 준비되면 `/api-contract orders.list` 로 계약을 뽑으세요.

## References

- `../../../docs/api/execution/probe-synthesis-hurl-semantics.md` — 값 생성 우선순위, query 직렬화, capture, entry 격리, 옵션 우선순위, exit code
- `../../../docs/api/execution/environment-safety-gates.md` — safe/unsafe 메서드 분류, prod read-only, allowlist, 재시도·리다이렉트·부하 예산·타임아웃
- `../../../docs/api/execution/auth-secret-lifecycle.md` — 토큰 캡처·갱신, `--secret` 의 stdout 한계, bearer 전달 방식, 인증 실패 분류
- `../../../docs/api/contract/snapshot-sealing-canonicalization.md` — raw 증거 보존, JCS 정규화, I-JSON 게이트, 매니페스트 해싱
- `../../../docs/api/verification/regression-diff-failure-policy.md` — exit code 별 실패 분류, redaction 선행 원칙
- `references/hurl-execution.md` — 안전 게이트 7단계, `.hurl` 합성 규칙, 실행 커맨드, 시크릿 배선
