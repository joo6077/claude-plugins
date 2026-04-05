---
title: TLS & 시크릿 관리
version: 0.1.0
last_updated: 2026-04-04
---

# TLS & 시크릿 관리

TLS 1.3, ACME 자동화(cert-manager), 시크릿 관리(Vault, AWS SM, GCP SM), 키 로테이션, 환경별 분리, sealed-secrets, external-secrets-operator를 다룬다.

---

## 원칙

### 1. 공개 종단은 TLS 1.3 우선, TLS 1.2는 호환성 예외만 허용한다

TLS 1.3은 핸드셰이크 왕복을 줄이고(1-RTT, 0-RTT 지원), 취약한 암호 스위트를 제거했다. 공개 엔드포인트는 TLS 1.3을 기본으로 하고, 레거시 클라이언트 지원이 불가피한 경우에만 TLS 1.2를 병행한다. TLS 1.1 이하는 완전히 차단한다.

> **출처:** [RFC 8446 — The Transport Layer Security (TLS) Protocol Version 1.3](https://www.rfc-editor.org/rfc/rfc8446)

### 2. 인증서 발급과 갱신은 ACME로 자동화한다

수동 인증서 관리는 갱신 누락과 만료 사고의 근본 원인이다. Kubernetes 환경에서는 cert-manager가 Let's Encrypt 등 ACME CA와 연동하여 인증서 생명주기를 자동화한다. 비-K8s 환경에서도 certbot이나 acme.sh를 cron으로 구성한다.

> **출처:** [cert-manager — ACME Configuration](https://cert-manager.io/docs/configuration/acme/)

### 3. HTTP-01과 DNS-01은 도메인 제어 방식에 맞춰 선택한다

HTTP-01 챌린지는 웹 서버가 공개 접근 가능해야 하며, 단일 도메인 인증서에 적합하다. DNS-01 챌린지는 DNS TXT 레코드를 생성하여 검증하며, 와일드카드 인증서(`*.example.com`)는 DNS-01만 가능하다. 내부 서비스나 private 네트워크는 DNS-01을 사용한다.

> **출처:** [cert-manager — ACME Challenge Types](https://cert-manager.io/docs/configuration/acme/)

### 4. 애플리케이션은 시크릿의 참조자이며, 중앙 시크릿 매니저에서 주입한다

시크릿(DB 비밀번호, API 키, 토큰)은 코드, 이미지, 환경변수에 하드코딩하지 않는다. AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault 등 중앙 저장소에서 런타임에 주입하거나 사이드카로 마운트한다. 앱은 시크릿의 소유자가 아니라 소비자다.

> **출처:** [AWS Secrets Manager — Rotating Secrets](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html)

### 5. 로테이션 주기는 앱 재배포보다 짧게, 무중단 교체 경로를 설계한다

시크릿 로테이션은 "언젠가 유출될 수 있다"는 전제에서 폭발 반경(blast radius)을 줄이는 장치다. 로테이션 Lambda/함수가 새 시크릿을 생성하고, 이전 버전을 유예 기간 동안 유지한 뒤 폐기하는 이중 시크릿(dual-secret) 패턴을 적용한다. 소비자(앱)는 캐시된 시크릿을 주기적으로 갱신하거나 실패 시 재조회해야 한다.

> **출처:** [AWS Secrets Manager — Rotation Schedule](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_schedule.html)

### 6. 환경별 시크릿은 계정, 프로젝트, 네임스페이스 경계로 분리한다

dev/staging/production 시크릿이 동일한 저장소나 네임스페이스에 있으면 권한 오설정으로 교차 접근이 발생한다. AWS는 계정 분리, GCP는 프로젝트 분리, Kubernetes는 네임스페이스 + RBAC로 환경별 시크릿 격리를 보장한다.

> **출처:** [GitHub — Sharing Secrets with Your Organization](https://docs.github.com/en/actions/how-tos/administering-github-actions/sharing-workflows-secrets-and-runners-with-your-organization)

---

## 수치/기준값

- TLS 1.3은 0-RTT 재개(resumption)를 지원하나, 0-RTT 데이터는 replay 공격에 취약하므로 비멱등 요청(POST 등)에는 사용하지 않는다
- AWS Secrets Manager 자동 로테이션: 최소 주기 **4시간**, rotation window 최소 **1시간**
- `AutomaticallyAfterDays` 설정 범위: **1~1,000일**
- cert-manager 기본 인증서 갱신 시점: 만료 **30일 전** (renewBefore로 조정 가능)
- Let's Encrypt 인증서 유효기간: **90일** (짧은 유효기간으로 자동화를 강제)
- AWS SM/GCP SM 시크릿 버전은 자동 보관되며, 이전 버전 조회 가능 (staging label/version alias)

---

## 안티패턴

- **인증서나 키를 git 리포지토리/이미지 레이어에 포함**: git history에 남아 영구 노출. `.gitignore`와 이미지 빌드 단계 분리 필수
- **장기 정적 자격증명을 환경변수로 영구 주입**: 로테이션 불가, 유출 시 폭발 반경 무한. 단기 토큰 또는 IAM 역할 기반 인증으로 전환
- **와일드카드 인증서를 HTTP-01 챌린지로 시도**: HTTP-01은 와일드카드를 지원하지 않는다. DNS-01로 전환 필요
- **로테이션만 켜고 소비자 재로딩 경로 없음**: 시크릿이 교체되어도 앱이 이전 값을 캐시하면 인증 실패. 재조회 로직 또는 시그널 기반 리로드 필수

---

## Gotchas

- TLS 1.3 0-RTT는 비멱등 요청(결제, 주문 등)에 replay 위험이 있다. 서버 측에서 0-RTT 데이터에 대해 멱등성 키 검증을 하거나 0-RTT를 비활성화한다
- cert-manager는 Kubernetes 인증서 생명주기 자동화 도구이지, 시크릿 관리의 단일 해법이 아니다. TLS 인증서와 애플리케이션 시크릿은 별개 파이프라인으로 관리한다
- sealed-secrets와 external-secrets-operator(ESO)는 시크릿의 배포 메커니즘이지 거버넌스 자체가 아니다. 감사 로그, 접근 제어, 로테이션 정책은 별도로 구성해야 한다
- AWS SM 로테이션 Lambda가 실패하면 시크릿이 중간 상태(AWSPENDING)에 머문다. CloudWatch 알람으로 로테이션 실패를 감시해야 한다
- cert-manager의 DNS-01 solver가 DNS 전파 지연으로 챌린지에 실패할 수 있다. propagationTimeout과 dns01RecursiveNameservers 설정을 조정한다
