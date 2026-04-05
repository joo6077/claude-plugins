---
title: 보안
version: 0.1.0
last_updated: 2026-04-04
---

# 보안

OWASP Top 10, 주요 공격 벡터(SQLi, XSS, SSRF), 의존성 스캔, rate limiting, 보안 헤더, 시크릿 관리, PII 마스킹을 다룬다.

---

## 원칙

### 1. OWASP Top 10을 체크리스트로 사용한다

OWASP Top 10(2021)은 웹 애플리케이션 보안 위협의 업계 표준 분류다. 2021 버전 기준 **A01: Broken Access Control**이 1위로, 94%의 애플리케이션에서 발견되었다. A02는 Cryptographic Failures, A03은 Injection이다. 모든 백엔드 프로젝트는 릴리스 전 Top 10 항목을 최소 1회 점검한다.

> **출처:** [OWASP Top 10 — 2021](https://owasp.org/Top10/)

### 2. SQL Injection은 파라미터화된 쿼리로 방어한다

문자열 연결로 SQL을 구성하면 공격자가 임의 쿼리를 실행할 수 있다. 파라미터화된 쿼리(prepared statement)가 유일한 방어법이다. ORM을 사용하더라도 raw query 메서드(`raw()`, `execute()`, `$queryRaw` 등)에서 문자열 보간을 쓰면 동일한 취약점이 발생한다.

> **출처:** [OWASP — SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)

### 3. XSS는 출력 인코딩 + CSP로 방어한다

XSS는 3종이 있다: **Stored**(DB에 저장된 악성 스크립트), **Reflected**(URL 파라미터 반사), **DOM-based**(클라이언트 JS에서 발생). 서버 측 출력 인코딩이 1차 방어이고, Content-Security-Policy 헤더가 2차 방어다. `innerHTML` 직접 삽입은 가장 흔한 DOM XSS 원인이다.

> **출처:** [OWASP — XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)

### 4. SSRF는 URL 허용목록 + 내부 네트워크 차단으로 방어한다

서버가 사용자 입력 URL을 fetch하면 내부 네트워크(메타데이터 서비스, 내부 API)에 접근할 수 있다. AWS 메타데이터 엔드포인트(`169.254.169.254`)가 대표적 타겟이다. 허용된 도메인/IP 범위만 접근 가능하도록 허용목록을 적용하고, private IP 대역(10.x, 172.16-31.x, 192.168.x, 127.x)을 차단한다.

> **출처:** [OWASP — SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)

### 5. 의존성 취약점은 자동 스캔으로 관리한다

알려진 취약점(CVE)이 있는 패키지를 사용하면 공격 표면이 된다. Dependabot(GitHub 내장)은 취약점 발견 시 자동 PR을 생성하고, Snyk는 더 세밀한 분석과 fix suggestion을 제공한다. `npm audit`, `pip audit`, `cargo audit` 등 언어별 CLI 도구도 CI에 통합한다.

> **출처:** [GitHub Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)

### 6. 보안 헤더를 설정한다

응답 헤더로 브라우저 보안 정책을 강제한다. 필수 헤더 4종:

- **Content-Security-Policy**: 스크립트/스타일 소스 제한. XSS 2차 방어선
- **Strict-Transport-Security**: `max-age=31536000; includeSubDomains`. HTTPS 강제
- **X-Content-Type-Options**: `nosniff`. MIME 스니핑 방지
- **X-Frame-Options**: `DENY` 또는 `SAMEORIGIN`. 클릭재킹 방지

> **출처:** [OWASP — HTTP Headers Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html)

### 7. 로그에서 PII를 마스킹한다

이메일, 전화번호, IP 주소, 신용카드 번호 등 개인식별정보(PII)가 로그에 평문으로 기록되면 로그 유출 시 개인정보 침해가 된다. 구조화된 로깅(structured logging)에서 민감 필드를 자동 마스킹하는 미들웨어를 적용한다. 이메일은 `j***@example.com`, 전화번호는 `010-****-1234` 형태로 마스킹한다.

> **출처:** [OWASP — Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)

---

## 수치 기준

| 항목 | 기준값 | 비고 |
|------|--------|------|
| HSTS max-age | 최소 31536000초 (1년) | `includeSubDomains` 권장 |
| CSP | `default-src 'self'` 시작 | `report-uri`로 위반 모니터링 |
| Rate limiting — 일반 API | 100 req/min/IP | 비인증 엔드포인트 기준 |
| Rate limiting — 인증 API | 10 req/min/IP | 로그인, 비밀번호 재설정 등 |
| 의존성 스캔 주기 | 매일 자동 (Dependabot 기본) | Critical/High는 24시간 내 대응 |
| 시크릿 로테이션 | 90일 주기 | API 키, DB 비밀번호 등 |

---

## 안티패턴

### 문자열 연결 SQL

`"SELECT * FROM users WHERE id = '" + userId + "'"` — 가장 고전적이면서도 여전히 발생하는 취약점. ORM의 raw query에서도 동일하게 발생한다.

### innerHTML 직접 삽입

사용자 입력을 `innerHTML`이나 `dangerouslySetInnerHTML`에 직접 전달하면 DOM XSS가 발생한다. 반드시 새니타이저(DOMPurify 등)를 거친다.

### SSRF 방어 없는 URL fetch

사용자가 입력한 URL을 검증 없이 서버에서 fetch하면 내부 네트워크 탐색, 메타데이터 서비스 접근이 가능하다. webhook URL, 이미지 URL, OAuth callback 등이 대표적 공격 지점이다.

### 시크릿 하드코딩

소스 코드에 API 키, DB 비밀번호를 직접 작성하면 git 히스토리에 영구 기록된다. 환경 변수 또는 시크릿 매니저(AWS Secrets Manager, HashiCorp Vault)를 사용한다. `.env` 파일은 `.gitignore`에 반드시 포함한다.

---

## Gotchas

- **ORM도 raw query 쓰면 injection 가능** — Prisma의 `$queryRaw`, Django의 `raw()`, SQLAlchemy의 `text()`에서 f-string/문자열 보간을 사용하면 파라미터화가 무력화된다
- **CSP 도입 시 인라인 스크립트 깨짐** — `script-src 'self'` 설정 시 인라인 `<script>` 태그와 `onclick` 핸들러가 차단된다. nonce 또는 hash 기반 허용이 필요하며, 기존 프로젝트에 CSP를 도입할 때는 `Content-Security-Policy-Report-Only`로 먼저 모니터링한다
- **Dependabot auto-merge는 breaking change 위험** — patch 버전만 auto-merge하고, minor/major는 수동 리뷰한다. 특히 보안 패치가 API 변경을 동반하는 경우가 있다
