---
name: api-verify
description: >
  계약 전체(또는 필터)를 다시 실행해 baseline 과 대조하고 PASS/FAIL 리포트 + canonical diff 를 낸다.
  계약 실패 · 환경 실패 · 인증 실패 · 데이터 부재를 구분해 보고하고, Hurl exit code 계약(0/1/2/3/4)을 그대로 승계한다.
  "회귀 검증", "계약 검증", "api verify", "다시 때려서 비교" 같은 요청 시 트리거.
  계약·스키마를 새로 뽑는 일에는 트리거하지 않는다 — `/api-contract` 가 담당한다.
  baseline 을 새 truth 로 승격하는 일에도 트리거하지 않는다 — 별도 promote 승인 경로다.
argument-hint: "[endpoint-id|group] [--env dev|stg|prod] [--spec-conformance] [--spec-diff <base>]"
user-invocable: true
---

## Gotchas

- **exit code 3 과 4 를 절대 합치지 마라.** `3`(런타임 — DNS/TLS/connect/timeout)은 **환경 실패**이고 계약 판정을 보류해야 한다. `4`(assert)만 **계약 위반**이고 게이트를 깬다. non-zero 를 전부 계약 실패로 보고하면 회귀 diff 가 노이즈로 덮이고, CI 가 "서버가 죽음" 과 "계약이 깨짐" 을 구분할 수 없게 된다. `2`(입력 파싱)는 probe/계약 파일 버그이지 계약 판정이 아니다. Hurl 의 코드 체계를 승계하고 **임의로 재매핑하지 않는다**. 출처: `docs/api/verification/regression-diff-failure-policy.md` §5.
- **401 / 403 / 404 를 자동으로 회귀라고 부르지 마라.** 만료된 토큰(`invalid_token` 401)은 인증 실패, 권한 부족(`insufficient_scope` 403)은 권한 실패, `404` 는 데이터 부재일 수도 존재를 감추는 `403` 대체 정책일 수도 있다 — **후보 원인 둘을 모두 리포트에 남기고 단정하지 않는다**. malformed 는 `400`. 이걸 하나로 합치면 게이트가 노이즈로 채워진다. 출처: `regression-diff-failure-policy.md` §1·§4 · Gotchas 3행.
- **CI 에서 baseline 자동 갱신은 0회다.** diff 가 실패한 순간 baseline 을 덮어쓰면 회귀가 새 truth 로 승격되어 다음 실행부터 green 이 된다. `/api-verify` 는 어떤 경우에도 `.api/contracts/` 와 승인본을 쓰지 않는다 — 갱신은 명시적 promote 명령 + 리뷰 메타데이터(old/new diff, 승인자, 이유, 근거 run)의 책임이다. 출처: `regression-diff-failure-policy.md` §9, `baseline-governance-promotion.md` §4·§6.
- **retry 로 성공한 실패를 green 으로 숨기지 마라.** 동일 커밋·동일 입력에서 결과가 뒤집히면 그건 "안정" 이 아니라 **불안정 신호**다. `flaky-confirmed` 로 별도 카운터에 남기고 실패 기록을 지우지 않는다. 확인 재실행은 `initial + 1 replay` 이며, 계속 실패하면 원 분류를 유지한다. 출처: `regression-diff-failure-policy.md` §7.
- **같은 실패라도 baseline 상태에 따라 게이트 파괴 여부가 다르다.** `state: pending`(첫 성공 verification 전) 계약과 관찰 모드는 실패를 **기록하되 게이트를 깨지 않는다**. `accepted` baseline 이 있는 계약의 실패만 회귀로 게이트를 깬다. 이 구분 없이 전부 깨면 새로 뽑은 계약이 빌드를 막고, 전부 통과시키면 진짜 회귀가 샌다. 출처: `regression-diff-failure-policy.md` §6, `baseline-governance-promotion.md` §5·§7.
- **리포트를 만들기 전에 redaction 을 끝낸다.** 실패 artifact 에는 stdout 과 raw body 가 들어가고, Hurl `--secret` 은 **stderr 로그와 리포트만** exact match 로 가린다 — stdout HTTP 응답, `--include`, `--json` 출력, JSON 리포트의 raw dump 는 가리지 않는다. base64 변형·대소문자 변형·`Bearer ` 접두 포함본은 각각 별도 secret 으로 등록해야 하고, `--very-verbose` 는 body 를 stderr 에 그대로 뿌린다. 생성 후 마스킹은 이미 파일·CI 로그에 남은 뒤다. 출처: `regression-diff-failure-policy.md` Gotchas 4행, `auth-secret-lifecycle.md` §5·§6.
- **실행 모드와 normalize 규칙을 리포트에 함께 남긴다.** additive field(서버가 필드 추가)는 partial 에서는 정상이고 exact 에서는 실패다 — 모드를 모르면 같은 diff 를 읽고 반대 결론이 나온다. normalize 규칙 자체가 diff 결과의 일부이므로 어떤 마스크가 적용됐는지도 함께 출력한다. 출처: `regression-diff-failure-policy.md` §3 · Gotchas 2행.
- **Hurl 실행 파라미터를 기본값에 맡기지 마라.** `--test` 는 파일 단위 **병렬** 실행이고 `--jobs` 기본값은 CPU 수 기반이라, 단일 파일 감각으로 잡으면 실제 부하가 예상보다 크다. 실행 전에 `파일 수 × 요청 수 × --repeat × --jobs` 로 요청량 예산을 계산해 상한과 비교한다. 순차가 필요하면 `--jobs 1`. `connect-timeout` 과 `max-time` 이 둘 다 없으면 env 기본값을 주입하고, 그래도 없으면 실행을 막는다. `--retry` 는 assert·capture·runtime 오류에도 재시도하므로 파일 전체에 걸지 않는다. 옵션 우선순위는 env < CLI < per-entry `[Options]`. 출처: `environment-safety-gates.md` §5·§7·§8, `probe-synthesis-hurl-semantics.md` §6.
- **prod 는 실행 전에 게이트를 통과해야 한다.** 기본 허용 메서드는 `GET`/`HEAD`/`OPTIONS` 뿐이고(범위는 2026-09-04 기준 미확정), unsafe 메서드는 **env + host + path + method 4중 키 allowlist** 에 있고 사용자 확인을 받은 것만 실행한다. `allowHosts` 밖으로 나가는 요청은 무조건 차단하고, 크로스 호스트 리다이렉트는 0회, `--location-trusted` 는 기본 금지다(리다이렉트된 모든 host 로 인증 정보가 전달된다). `TRACE` 는 기본 제외 — 요청을 loop-back 해 `Authorization` 이 응답 본문에 실려 돌아온다. `PUT`/`DELETE` 가 idempotent 라는 사실은 재시도 근거이지 실행 허용 근거가 아니다. 출처: `environment-safety-gates.md` §1~§6.
- **`--spec-conformance` 와 `--spec-diff` 는 옵트인이다. 기본 실행 경로에 넣지 마라.** 둘 다 OpenAPI 스펙이 있을 때만 의미가 있고, 스펙 없는 프로젝트에서 실패로 잡히면 안 된다. Schemathesis 를 켤 때는 read-only allowlist + seed 고정 + 실패 케이스 저장을 강제한다 — 실무 오탐이 스펙 느슨함·auth·destructive endpoint·정렬 불안정에서 나온다. 이 결과는 **본체 PASS/FAIL 과 별도 섹션**으로 보고하고 게이트에 섞지 않는다. 출처: 설계문서 §5.2.

# 계약 회귀 검증

## 0. 대상 선정

`$ARGUMENTS` 에서 파싱하거나 기본값을 쓴다.

| 항목 | 예시 | 기본값 |
|---|---|---|
| 대상 | `orders.list` · `orders.*` · 생략(전체) | 전체 |
| 환경 | `--env dev` | `.api/project.yaml` 기본 env |
| 옵트인 레일 | `--spec-conformance` · `--spec-diff <base>` | 꺼짐 |

`.api/contracts/*.yaml` 을 읽어 실행 목록을 만든다. 계약이 0개면 중단하고 `/api-contract` 를 안내한다.

**만료 검사**: `baseline.expiresAt` 이 지난 계약은 `30일` 경과 warning, `90일` 경과 block 으로 분류한다. 만료된 baseline 을 green signal 로 계속 쓰면 검증했다는 착각만 남는다.

---

## 1. 실행 전 안전 게이트

아래를 순서대로 판정하고, 하나라도 막히면 **실행하지 않고** 이유를 보고한다.

```text
1  env / tier 확인            prod 이면 read-only 정책 적용
2  method 분류                GET·HEAD·OPTIONS 기본 허용 / TRACE 제외
3  unsafe 메서드 allowlist    env + host + path + method 4중 키 일치 필요
4  allowHosts 화이트리스트     목록 밖 호스트는 무조건 차단
5  리다이렉트 정책             크로스 호스트 0회, --location-trusted 금지
6  요청량 예산                 파일 수 × 요청 수 × repeat × jobs ≤ env 상한
7  타임아웃                    connect-timeout + max-time 둘 다 필수
```

prod 에서 쓰기 메서드가 포함되면 **대상 목록을 보여주고 사용자 확인을 받는다.** 확인 없이 실행하지 않는다.
각 실행 항목에 env · host · auth profile · method class · retry · concurrency · 최대 요청 수를 폭발 반경 태그로 붙인다.

---

## 2. 인증 준비

- env 별 auth profile 을 사용한다. 한 profile 을 여러 env 가 공유하지 않고, prod 토큰 캐시는 분리한다.
- 토큰은 캐시 우선. `expires_at = 응답시각 + expires_in`, `refresh_at = expires_at - expirySkewSeconds`(기본 60초).
- `expires_in` 이 응답에도 profile 기본값(`fallbackTtlSeconds`)에도 없으면 자동 갱신을 **추측하지 말고 금지** — 매 실행 재발급으로 되돌린다.
- 발급 후 임시 `--secrets-file` 로 Hurl 에 넘긴다. `.hurl` 본문에는 `Authorization: Bearer {{access_token}}` 만 남는다.
- 토큰과 그 **변형값**(base64 인코딩본, `Bearer ` 접두 포함본, 대소문자 변환본)을 각각 secret 으로 등록한다.
- 병렬 실행 시 토큰 발급에 파일 락을 건다. 동시 시작이 IdP 를 두들기는 걸 막는다.
- `401` 재시도는 1회, `WWW-Authenticate` 가 `error="invalid_token"` 일 때만. 재발급 후에도 `401` 이면 즉시 실패 — 무한 루프를 막는다.

---

## 3. Hurl 실행

```bash
hurl --test \
  --jobs 1 \
  --connect-timeout 5 \
  --max-time 30 \
  --secrets-file "$TMP_SECRETS" \
  --report-json .api/reports/run-$(date +%Y%m%dT%H%M%S) \
  .api/cases/orders.list.hurl
```

- 의존 흐름은 이미 한 파일 안에 있어야 한다(계약 생성 단계 책임). 파일 경계 = 격리 경계.
- `--continue-on-error` 는 **서로 독립인 probe 배치에만** 켠다. dependency chain 에 켜면 오염된 변수로 후속 요청이 돌아 전이 실패를 만든다.
- 리포트 산출물은 `reports/`(gitignore) 밖으로 내보내지 않는다.

---

## 4. exit code 판정 (재매핑 금지)

| exit code | 의미 | 분류 | 게이트 | CI 처리 |
|---|---|---|---|---|
| `0` | 성공 | — | 통과 | pass |
| `1` | CLI 옵션 파싱 오류 | 도구 사용 오류 | — | 실행 중단, 재시도 금지 |
| `2` | 입력(`.hurl`) 파싱 오류 | 계약 파일 오류 | — | 실행 중단, 계약 파일 수정 |
| `3` | 런타임 오류 (DNS/TLS/connect/timeout) | **환경 실패** | **판정 보류** | `error` 로 기록 |
| `4` | assert 실패 | **계약 실패** | **게이트 파괴** | `failure` 로 기록 |

`3` 은 하위 원인을 구분하지 못하므로 리포트에 **subreason 필드**를 별도로 남긴다(일시적 타임아웃 / 인증서 만료 / DNS 실패 / connect refused). 없으면 다음 사람이 같은 조사를 처음부터 반복한다.

`/api-verify` 의 종료 코드는 실행 결과 중 **가장 심각한 코드**를 그대로 반환한다.

---

## 5. 응답 정규화

계약 생성과 **동일한 파이프라인**을 쓴다. 다르면 diff 가 의미를 잃는다.

```text
redaction  →  masks/*.yaml 적용  →  I-JSON 게이트  →  JCS 직렬화
```

- I-JSON 게이트 실패(중복 키·NaN·lone surrogate)는 계약 실패가 아니라 **비교 불가**로 분류한다.
- 배열은 정렬하지 않는다.
- 적용된 마스크 목록을 리포트에 함께 출력한다.

---

## 6. drift 분류

정규화 이후 남은 차이만 판정 대상이다. 세 축으로 나눈다.

| 축 | 내용 | 판정 |
|---|---|---|
| **Status drift** | 상태 클래스 단위로 분류. `200→500` 과 `200→404` 를 같은 심각도로 묶지 않는다 | `2xx→5xx` 는 심각, `2xx→4xx` 는 후보 원인 병기 |
| **Schema drift** | 필드 추가·삭제·타입 변경 = API 표면 변화 | value diff 와 **별도 카테고리**의 계약 실패 |
| **Value drift** | normalize 이후에도 남은 값 차이 | assertion failure |

pin 항목 중 `.hurl` 로 표현되지 않은 **경로 간 불변식**(`$.meta.total >= len($.data)`)은 여기서 후처리로 검사한다.
컬렉션은 envelope / item / pagination marker 를 나눠 판정한다 — skip/duplicate 는 schema 위반이 아니라 variance 신호다.

---

## 7. severity 판정

```text
baseline state = pending   → 실패를 기록하되 게이트를 깨지 않는다 (observe)
baseline state = accepted  → 실패는 회귀. 게이트 파괴
mode = partial             → additive field 는 정상
mode = exact               → additive field 는 실패
```

계약 실패(`4`)만 게이트를 깨고, 환경 실패(`3`)·인증 실패·데이터 부재는 게이트 판정을 보류한 채 별도 카운터로 집계한다.
분류 상세는 `references/failure-taxonomy.md`.

---

## 8. flaky 확인 재실행

- 대상: **멱등 요청만** (safe 메서드 · `PUT` · `DELETE` · 명시적 idempotent 태깅). 그 외는 0회.
- 횟수: `initial + 1 replay` (동일 커밋·동일 입력).
- 결과가 뒤집히면 `flaky-confirmed` 로 분류하고 **원 실패 기록을 남긴다.** 계속 실패하면 원 분류 유지.
- retry 성공을 pass 로 덮어쓰지 않는다.

---

## 9. 리포트 생성

**redaction 을 마친 데이터로만** 생성한다.

리포트에 반드시 포함할 항목:

1. 실행 요약 — 대상 수, PASS / FAIL / 보류 / flaky, 실행 모드, 환경
2. 실패별 분류 — 계약 실패 · 환경 실패 · 인증 실패 · 데이터 부재 (섞지 않는다)
3. canonical diff — JCS 기준선 대비. 경로 단위 추가/삭제/변경
4. exit code 와 subreason
5. 적용된 normalize 규칙과 baseline lineage(env·branch·capturedAt·samples)
6. baseline 만료 경고

JUnit XML 로 내보낼 때 매핑을 지킨다.

```text
계약 assertion mismatch   → <failure>
실행 불능 · 환경 오류      → <error>
quarantine · 의도된 미실행 → <skipped>
통과                      → result child 없음
```

전부 `failure` 로 밀어 넣으면 서버 다운과 계약 파손이 같은 통계로 합쳐져 원인 분석이 불가능해진다.

---

## 10. 옵트인 레일 (요청 시에만)

| 플래그 | 도구 | 조건 | 보고 위치 |
|---|---|---|---|
| `--spec-conformance` | Schemathesis | OpenAPI 스펙 존재 | 별도 섹션. 게이트에 섞지 않는다 |
| `--spec-diff <base>` | oasdiff | OpenAPI 스펙 존재 | 별도 섹션. breaking change 목록 |

스펙이 없으면 플래그가 있어도 **실행하지 않고 이유를 보고**한다. 실패로 잡지 않는다.
Schemathesis 는 read-only allowlist + seed 고정 + 실패 케이스 저장을 함께 켠다.

---

## 11. 보고와 다음 단계

1. 판정 요약 (PASS/FAIL/보류/flaky 카운트 + 종료 코드)
2. 게이트를 깬 계약 실패 목록 — 각각 status/schema/value 중 어느 축인지 명시
3. 게이트를 깨지 않은 항목 — pending baseline, 환경 실패, 데이터 부재
4. 다음 단계 안내:
   - 실패가 **의도된 변경**이면 diff 를 확인한 뒤 promote 로 승격하세요. `/api-verify` 는 baseline 을 쓰지 않습니다.
   - 승격에는 old/new diff · 승인자 · 이유 · 근거 run 이 기록되어야 합니다. breaking schema drift 또는 prod lineage 변경은 승인자 2명입니다.
   - 환경 실패(`3`)는 계약 판정이 아닙니다. 네트워크·인증서·타임아웃을 먼저 확인하세요.

# References

- references/failure-taxonomy.md — 실패 분류 체계와 exit code 계약
- ../../../docs/api/verification/regression-diff-failure-policy.md — drift 분류·exit code·CI artifact 매핑
- ../../../docs/api/verification/baseline-governance-promotion.md — baseline 승격 게이트·lineage·만료
- ../../../docs/api/execution/environment-safety-gates.md — prod 게이트·요청량 예산·타임아웃
- ../../../docs/api/execution/auth-secret-lifecycle.md — 토큰 갱신·마스킹 한계
- ../../../docs/api/execution/probe-synthesis-hurl-semantics.md — Hurl 실행 의미론·옵션 우선순위
- ../../../docs/api/contract/snapshot-sealing-canonicalization.md — 정규화 파이프라인
- ../../../docs/api/contract/error-status-contracts.md — 오류·상태 코드 해석
- ../../../docs/superpowers/specs/2026-09-02-api-kit-design.md — §7.4 스킬 정의 · §5.2 옵트인 레일 · §8 안전 가드
