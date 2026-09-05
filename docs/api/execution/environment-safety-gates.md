---
title: 환경 안전 게이트
version: 0.1.0
last_updated: 2026-09-04
---

# 환경 안전 게이트

실제 API를 호출하기 전에 무엇을 허용할지 판정하는 규칙. 메서드 분류, prod 정책, 재시도·리다이렉트·부하 예산을 실행 직전에 결정한다.

---

## 원칙

### 1. Safe 메서드 기본 허용

기본 실행 허용 메서드는 `GET`, `HEAD`, `OPTIONS` 세 개다. 나머지는 allowlist 없이 실행하지 않는다.
RFC 9110은 `TRACE`도 safe로 분류하지만 api-kit 기본값에서는 보안 예외로 뺀다.

> **출처:** [RFC 9110 §9.2.1 Safe Methods](https://datatracker.ietf.org/doc/html/rfc9110#section-9.2.1)

### 2. TRACE 기본 제외

`TRACE`는 요청을 그대로 loop-back 하므로 쿠키나 `Authorization` 헤더가 응답 본문에 실려 돌아온다.
OWASP는 이를 Cross-Site Tracing 위험으로 다룬다. 기본 허용 횟수는 0이며, 사용자가 명시 요청해도 자격증명이 붙는 프로파일에서는 거부한다.

> **출처:** [OWASP Cross-Site Tracing](https://owasp.org/www-community/attacks/Cross_Site_Tracing)

### 3. prod는 read-only 우선

prod 실행 자체는 허용한다. 다만 기본값은 read-only이고, prod에서의 상태 변경은 명시적 승격이 있을 때만 열린다.
read-only의 정확한 범위는 아직 확정되지 않았다 — 현재는 `GET`/`HEAD`/`OPTIONS`로 두고, allowlist로 넓힐 여지만 남긴다.

> **출처:** [RFC 9110 §9.2.1 Safe Methods](https://datatracker.ietf.org/doc/html/rfc9110#section-9.2.1)

### 4. unsafe 메서드는 4중 키 allowlist

`POST`, `PUT`, `PATCH`, `DELETE`는 env + host + path + method 네 값이 모두 일치하는 항목이 allowlist에 있을 때만 실행한다.
`PUT`/`DELETE`가 idempotent라는 사실은 재시도 판단 근거이지 실행 허용 근거가 아니다 — 둘 다 상태 변경 메서드다.

> **출처:** [RFC 9110 §9.3 Method Definitions](https://datatracker.ietf.org/doc/html/rfc9110#section-9.3)

### 5. 재시도는 멱등 요청만

자동 재시도는 safe 메서드, `PUT`, `DELETE`, 그리고 명시적으로 idempotent 태깅된 요청에만 허용한다. 그 외는 0회다.
Hurl `--retry`는 HTTP 실패뿐 아니라 assert·capture·runtime 오류에도 재시도하므로, 파일 전체에 걸지 말고 게이트가 더 좁게 잘라야 한다.

> **출처:** [RFC 9110 §9.2.2 Idempotent Methods](https://datatracker.ietf.org/doc/html/rfc9110#section-9.2.2) · [Hurl Manual](https://hurl.dev/docs/manual.html)

### 6. 크로스 호스트 리다이렉트 차단

리다이렉트 추종은 same-origin이거나 명시적으로 allow된 host일 때만 허용한다. 크로스 호스트는 0회다.
Hurl `--location-trusted`는 리다이렉트된 모든 host로 인증 정보를 전달하므로 기본 금지 옵션으로 취급한다.

> **출처:** [Hurl Manual](https://hurl.dev/docs/manual.html) · [RFC 6750 §5.2 Threat Mitigation](https://datatracker.ietf.org/doc/html/rfc6750#section-5.2)

### 7. 요청량 예산을 실행 전에 계산

env별 최대 요청 수를 `파일 수 × 요청 수 × --repeat × --jobs` 기준으로 실행 전에 계산하고 상한과 비교한다.
Hurl test mode는 파일 단위 병렬 실행이 기본이고 `--jobs` 기본값이 CPU 수 기반이라, 단일 파일 감각으로 잡으면 prod 부하가 예상보다 커진다.

> **출처:** [Hurl Manual](https://hurl.dev/docs/manual.html) · [RFC 6585 §4 429 Too Many Requests](https://datatracker.ietf.org/doc/html/rfc6585#section-4)

### 8. 타임아웃 예산 강제

모든 실제 호출에는 연결 타임아웃(`connect-timeout`)과 전체 실행 상한(`max-time`)이 둘 다 지정되어야 한다.
Hurl이 두 옵션을 제공하므로, 값이 비어 있으면 게이트가 env 기본값을 주입하고 그래도 없으면 실행을 막는다.

> **출처:** [Hurl Manual](https://hurl.dev/docs/manual.html)

### 9. 폭발 반경 태깅

실행 항목마다 env, host, auth profile, method class, retry 횟수, concurrency, 최대 요청 수를 태깅하고 이 태그로 게이트를 판정한다.
safe 메서드도 반복·병렬이면 서버에 "unusual burden"이 되므로, 메서드 하나가 아니라 총 부하로 판단해야 한다.

> **출처:** [RFC 9110 §9.2.1 Safe Methods](https://datatracker.ietf.org/doc/html/rfc9110#section-9.2.1) · [RFC 6585 §4](https://datatracker.ietf.org/doc/html/rfc6585#section-4)

---

## 판정 순서

```text
1. method class 판정  (safe / unsafe)
2. env 정책 조회      (prod = read-only 기본)
3. allowlist 조회     (env + host + path + method 4중 일치)
4. retry 정책 판정    (멱등 아니면 0)
5. redirect 정책 판정 (cross-host면 차단)
6. 부하 예산 계산     (파일 × 요청 × repeat × jobs)
7. 타임아웃 주입 확인 (connect-timeout + max-time)
```

---

## 수치 기준

| 항목 | 값 | 근거 |
|------|-----|------|
| 기본 safe allowlist | `GET`, `HEAD`, `OPTIONS` (3개) | RFC 9110 §9.2.1 + OWASP XST |
| `TRACE` 허용 | 0회 | OWASP Cross-Site Tracing |
| non-idempotent 재시도 | 0회 | RFC 9110 §9.2.2 |
| Hurl 재시도 간격 기본값 | 1000ms | Hurl Manual |
| prod `--jobs` | 1 | 추론 — 병렬 기본값이 CPU 수 기반이라 상한 고정 |
| prod unsafe 요청 | 0건 (allowlist 승격 시에만) | 추론 — prod read-only 기본 정책 |
| cross-host 리다이렉트 | 0회 | 추론 — 토큰 audience 가정 붕괴 |
| same-origin 리다이렉트 상한 | 3회 | 추론 |
| prod `connect-timeout` | 5s | 추론 |
| prod `max-time` | 30s | 추론 |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| prod에서 `POST`/`DELETE`를 "계약 검증"이라며 기본 실행 | 검증 목적이 상태 변경 면책이 되지 않는다. 실데이터가 바뀐다 |
| `--retry`를 Hurl 파일 전체에 지정 | non-idempotent 요청까지 재시도되어 중복 생성·중복 결제가 난다 |
| 인증 요청에 `--location-trusted` 사용 | 리다이렉트된 임의 host로 자격증명이 전송된다 |
| `GET /delete?id=...`를 메서드만 보고 safe로 판정 | 메서드는 safe여도 서버 동작은 mutation이다. path 패턴도 함께 봐야 한다 |
| `--repeat` + test mode 병렬을 예산 없이 실행 | 파일 수 × jobs 배로 부하가 늘어 rate limit 또는 장애를 유발한다 |

---

## Gotchas

- **`TRACE`는 RFC상 safe다** — 표준만 보고 기본 safe set에 넣으면 XST 경로가 열린다. 분류(safe)와 허용(allow)을 분리해서 판단하라.
- **Hurl `--test`는 파일 단위 병렬이 기본** — 단일 파일 기준으로 계산한 요청 수는 실제 부하와 다르다. `--jobs`를 곱해서 계산하라.
- **`PUT`/`DELETE`는 재시도 후보이지 prod 기본 허용 후보가 아니다** — idempotent와 read-only는 다른 축이다.
- **리다이렉트로 host가 바뀌면 토큰 audience 가정도 깨진다** — 실행이 성공해도 검증 대상이 의도한 서버가 아닐 수 있다.
