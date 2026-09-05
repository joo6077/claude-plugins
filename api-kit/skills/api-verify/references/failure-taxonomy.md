# 실패 분류 체계

`/api-verify` 가 실패를 **계약 실패 · 환경 실패 · 인증 실패 · 데이터 부재** 로 나눌 때 쓰는 유일한 기준.
"무엇이 깨졌는가" 와 "게이트를 깨야 하는가" 는 다른 질문이며, 이 문서는 둘을 분리해 판정한다.
원 규칙은 `../../../../docs/api/verification/regression-diff-failure-policy.md` 다.

---

## 1. exit code 계약

Hurl 의 종료 코드를 그대로 승계한다. **임의 재매핑 금지.**

| exit code | 의미 | 분류 | 계약 판정 | CI 처리 | 재시도 |
|---|---|---|---|---|---|
| `0` | 성공 | — | PASS | pass | — |
| `1` | CLI 옵션 파싱 오류 | 도구 사용 오류 | 판정 없음 | 실행 중단 | **금지** |
| `2` | 입력(`.hurl`) 파싱 오류 | 계약 파일 오류 | 판정 없음 | 실행 중단 | 금지 |
| `3` | 런타임 오류 (DNS/TLS/connect/timeout) | **환경 실패** | **보류** | `error` | 조건부 |
| `4` | assert 실패 | **계약 실패** | FAIL | `failure` | 멱등만 1회 |

CI 가 "서버가 죽었다"(`3`)와 "계약이 깨졌다"(`4`)를 다르게 다룰 수 있어야 한다. 이 구분이 이 킷의 존재 이유 중 하나다.

`/api-verify` 는 실행 결과 중 **가장 심각한 코드**를 반환한다. 심각도 순서: `4` > `3` > `2` > `1` > `0`.

### exit code `3` 은 그 자체로는 정보가 없다

`3` 은 DNS·TLS·timeout·connect 를 전부 포함한다. 리포트에 **subreason** 을 반드시 별도 필드로 남긴다.

```text
3 / dns-failure          호스트 해석 실패
3 / tls-cert-expired     인증서 만료 — 일시 장애 아님
3 / tls-handshake        핸드셰이크 실패
3 / connect-refused      포트 닫힘 / 서비스 다운
3 / timeout-connect      connect-timeout 초과
3 / timeout-total        max-time 초과
```

subreason 없이 `3` 만 남기면 일시적 타임아웃과 인증서 만료가 구분되지 않는다.

---

## 2. 실패 4분류

| 분류 | 트리거 | 게이트 | 다음 행동 |
|---|---|---|---|
| **계약 실패** | exit `4`, 또는 정규화 후 남은 status/schema/value drift | **깬다** (accepted baseline 일 때) | diff 확인 → 서버 버그면 수정, 의도된 변경이면 promote |
| **환경 실패** | exit `3`, `5xx` 반복, 네트워크·TLS·타임아웃 | 보류 | 인프라 확인 후 재실행. 계약 판정 아님 |
| **인증 실패** | `401 invalid_token`, `403 insufficient_scope`, 토큰 발급 실패 | 보류 | 토큰 재발급 / scope 확인. 회귀로 집계하지 않는다 |
| **데이터 부재** | `404`, 빈 컬렉션, 픽스처 소멸 | 보류 | 대상 데이터 확인. `403` 대체 정책 가능성 병기 |

**하나로 묶지 마라.** 만료 토큰과 정상적인 데이터 부재가 계약 위반으로 둔갑하면 게이트가 노이즈로 채워지고, 그 다음부터 아무도 게이트를 보지 않는다.

---

## 3. status drift 판정

상태 변화는 문자열 diff 가 아니라 **클래스 단위**로 본다.

| 변화 | 분류 | 심각도 | 비고 |
|---|---|---|---|
| `2xx → 5xx` | 환경 실패 우선 검토 → 반복되면 계약 실패 | 높음 | 5xx 본문은 계약 대상 아님 |
| `2xx → 4xx` | 원인 후보를 **병기**하고 단정하지 않는다 | 중간 | 아래 4xx 표 참조 |
| `2xx → 3xx` | 리다이렉트 정책 확인 | 중간 | Hurl 은 redirect follow 가 기본 꺼짐 — 계약 위반처럼 보이지만 설정 문제일 수 있다 |
| `4xx → 2xx` | 계약 변경 신호 | 중간 | 오류 계약이 낡았을 수 있다 |
| 같은 클래스 내 코드 변경 (`400 → 422`) | 계약 실패 (status policy 가 `exact` 일 때) | 낮음~중간 | `class` 정책이면 통과 |

### 4xx 세분

| 코드 | 의미 | 분류 |
|---|---|---|
| `400` | malformed request | 계약 실패 (요청 합성 오류일 수도 — 케이스 먼저 확인) |
| `401` | 유효한 인증 정보 없음 / 실패. `WWW-Authenticate` 동반 | **인증 실패** |
| `403` | 요청은 이해했으나 거부. `insufficient_scope` | **인증(권한) 실패** |
| `404` | **원인이 둘이다** — 진짜 데이터 부재 / 존재를 감추는 `403` 대체 | **데이터 부재** (두 후보 모두 기록) |
| `429` | rate limit. `Retry-After` 를 읽는다 (delay-seconds 또는 HTTP-date) | 환경 실패 |

`401` / `403` / `invalid_token` / `insufficient_scope` 를 하나로 합치면 **토큰 갱신으로 풀리는 실패**와 **권한 자체가 없는 실패**가 섞인다.

---

## 4. schema drift 판정

응답 본문의 구조 변화는 API 표면 변화이며 value diff 와 **별도 카테고리**다.

| 변화 | partial | pin | exact |
|---|---|---|---|
| 필드 삭제 | 계약 실패 | 계약 실패 | 계약 실패 |
| 타입 변경 | 계약 실패 | 계약 실패 | 계약 실패 |
| nullable 위반 | 계약 실패 | 계약 실패 | 계약 실패 |
| **필드 추가 (additive)** | 통과 (정상) | 통과 (정상) | **계약 실패** |
| 확정 enum 밖의 값 | 계약 실패 | 계약 실패 | 계약 실패 |
| `enumCandidate`(미확정) 밖의 값 | **경고만** | 경고만 | 계약 실패 |

additive field 는 모드에 따라 판정이 뒤집힌다. **어떤 모드로 실행했는지 리포트에 반드시 함께 남긴다.**

---

## 5. value drift 판정

normalize 를 먼저 적용하고, **그 이후에도 남는 차이만** assertion failure 로 판정한다.

| 항목 | 처리 |
|---|---|
| timestamp · uuid · nonce · cursor | 마스크 대상. 남아 있으면 마스크 누락 — 계약 실패로 올리기 전에 마스크부터 점검 |
| 배열 순서 | 정렬 보장이 있으면 계약 실패, 없으면 **variance 신호** |
| 부동소수 정밀도 | 마스크의 round 규칙 적용 후 판정 |
| 경로 간 불변식 (`$.meta.total >= len($.data)`) | Hurl 로 표현 불가 — 후처리에서 검사, 실패 시 계약 실패 |
| 컬렉션 skip/duplicate | item schema 위반 아님. **컬렉션 variance** 로 분류 |

적용된 normalize 규칙은 diff 결과의 일부다. 리포트에 함께 출력하지 않으면 다음 사람이 결과를 재현할 수 없다.

---

## 6. severity — 게이트를 깨는가

같은 실패라도 baseline 상태에 따라 결과가 다르다.

| baseline state | 실패 처리 | 근거 |
|---|---|---|
| `pending` (첫 성공 verification 전) | 기록하되 **게이트를 깨지 않는다** | 새 계약이 빌드를 불필요하게 막지 않도록 |
| `accepted` (첫 성공 이후) | **회귀. 게이트 파괴** | 한 번 통과한 계약의 실패는 breaking |
| observe 모드 | 기록만 | 관찰 목적 |
| 만료 baseline (`>30일`) | 경고 동반 | 검증했다는 착각 방지 |
| 만료 baseline (`>90일`) | 차단 | 기준이 이미 다른 곳에 있다 |

브랜치 축도 같다 — main/release baseline 과 feature/WIP baseline 을 섞지 않는다. feature branch baseline 을 main truth 로 승격하면 실제 배포된 API 와 어긋난 기준이 게이트를 통과시킨다.

---

## 7. flaky 분류

| 상황 | 분류 |
|---|---|
| 최초 실패 → replay 성공 | `flaky-confirmed` (별도 카운터). **원 실패 기록 유지** |
| 최초 실패 → replay 도 실패 | 원 분류 유지 (계약/환경/인증/데이터) |
| 멱등하지 않은 요청 | replay `0회`. 최초 결과로 확정 |

확인 재실행은 `initial + 1 replay`, 동일 커밋·동일 입력에서만. retry 성공을 pass 로 덮어쓰면 flaky 신호가 사라지고 같은 불안정이 무한 반복된다.

---

## 8. CI artifact 매핑

```text
계약 assertion mismatch      → <failure>
실행 불능 · 환경 · 인프라 오류 → <error>
quarantine · 의도된 미실행     → <skipped>
통과                          → result child 없음
```

| 실패 분류 | JUnit 요소 |
|---|---|
| 계약 실패 (exit `4`, drift) | `failure` |
| 환경 실패 (exit `3`) | `error` |
| 인증 실패 | `error` |
| 데이터 부재 | `error` 또는 `skipped` (픽스처 미준비면 `skipped`) |
| pending baseline 실패 | `skipped` + 사유 (게이트 미파괴) |
| 계약 파일 오류 (exit `2`) | `error` |

전부 `failure` 로 밀어 넣으면 서버 다운과 계약 파손이 같은 통계로 합쳐져 집계가 무의미해진다.

---

## 9. baseline 승격 게이트 (verify 의 책임 아님)

`/api-verify` 는 어떤 경우에도 baseline 을 쓰지 않는다. CI 자동 갱신은 `0회`.

승격 시 남겨야 하는 기록:

| 항목 | 내용 |
|---|---|
| diff | old / new 전체 |
| 승인자 | 기본 `1명`. breaking schema drift 또는 prod lineage 변경은 `2명` |
| 이유 | "expected updated" 만으로는 6개월 뒤 판단 근거가 없다 |
| 근거 run | 어떤 실행 결과를 보고 승인했는가 |
| lineage | env · branch · provider/API 버전 · 배포 시점 |

승인본은 소스 컨트롤에, 실행 산출물(`.received.*`)은 커밋 `0건`. prod evidence 커밋 `0건`(스키마 계약만).

---

## 10. 안티패턴

| 안티패턴 | 문제 |
|---|---|
| 모든 차이를 `diff failed` 한 줄로 출력 | 상태·스키마·값 중 무엇이 깨졌는지 알 수 없어 대응 우선순위를 못 정한다 |
| non-zero exit code 를 전부 계약 실패로 보고 | 환경 실패가 회귀 통계를 오염시키고, 진짜 회귀가 묻힌다 |
| `401/403/404` 를 무조건 API regression 으로 처리 | 만료 토큰·정상적 데이터 부재가 계약 위반으로 둔갑한다 |
| retry 성공 시 실패 기록 삭제 | flaky 신호가 사라져 같은 불안정이 무한 반복된다 |
| CI 실패 시 baseline 자동 갱신 | 회귀가 새 truth 로 승격되어 다음 실행부터 green 이 된다 |
| JUnit XML 에서 런타임·인프라 오류를 `failure` 로 기록 | 서버 다운과 계약 파손이 같은 통계로 합쳐진다 |
| 리포트 생성 후 마스킹 | 이미 파일·CI 로그에 시크릿이 남은 뒤다 |
| 실행 모드 없이 diff 만 보고 | additive field 판정이 모드에 따라 뒤집혀 반대 결론이 나온다 |

---

## 11. 출처

- [regression-diff-failure-policy.md](../../../../docs/api/verification/regression-diff-failure-policy.md) — drift 분류, exit code 계약, JUnit 매핑, flaky
- [baseline-governance-promotion.md](../../../../docs/api/verification/baseline-governance-promotion.md) — 승격 게이트, lineage, 만료
- [error-status-contracts.md](../../../../docs/api/contract/error-status-contracts.md) — 4xx/5xx 해석, `Retry-After`, problem+json
- [environment-safety-gates.md](../../../../docs/api/execution/environment-safety-gates.md) — 재시도 허용 범위, 요청량 예산
- [auth-secret-lifecycle.md](../../../../docs/api/execution/auth-secret-lifecycle.md) — 인증 실패 분리, 마스킹 한계
- [api-kit 설계문서](../../../../docs/superpowers/specs/2026-09-02-api-kit-design.md) — §7.4 · §8
