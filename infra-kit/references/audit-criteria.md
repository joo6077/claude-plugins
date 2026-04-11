# Infra-Audit 판정 기준

infra-audit 스킬과 infra-reviewer 에이전트가 카테고리별 PASS/FAIL 판정 시 참조한다.
각 기준은 `docs/infra/` 리서치 문서에서 추출한 원칙이다.

---

## Container

| 기준 | PASS | FAIL |
|------|------|------|
| 멀티스테이지 빌드 | `COPY --from=builder` 패턴 사용 | 단일 스테이지로 빌드 도구 포함 |
| non-root 실행 | `USER` 지시어로 비특권 사용자 지정 | root 실행 또는 USER 없음 |
| .dockerignore | `.git`, `node_modules`, `.env` 제외 | .dockerignore 없음 또는 미설정 |
| 헬스체크 | `HEALTHCHECK` 지시어 또는 compose healthcheck | 없음 |
| 이미지 태그 | 고정 태그 또는 digest 핀닝 | `latest` 태그 사용 |

참조: `docs/infra/platform/container.md`

---

## CI/CD

| 기준 | PASS | FAIL |
|------|------|------|
| 파이프라인 단계 | build → test → deploy 순서 준수 | 테스트 없이 바로 배포 |
| 시크릿 관리 | Secrets/Vault 사용, 환경변수 주입 | 소스코드 또는 로그에 시크릿 노출 |
| OIDC 인증 | OIDC로 클라우드 인증 (장기 키 없음) | 장기 액세스 키 사용 |
| 캐싱 | 의존성 캐시 레이어 설정 | 매 실행 전체 재설치 |
| 아티팩트 보존 | 빌드 산출물 저장 설정 | 없음 |

참조: `docs/infra/platform/cicd.md`

---

## Kubernetes

| 기준 | PASS | FAIL |
|------|------|------|
| 리소스 제한 | `resources.requests` + `limits` 설정 | 미설정 |
| 활성/준비 프로브 | `livenessProbe` + `readinessProbe` | 없음 |
| RBAC | 최소 권한 ServiceAccount, ClusterRole 금지 | 와일드카드 권한 또는 cluster-admin |
| 시크릿 분리 | Secret 오브젝트 사용, 환경변수 주입 | ConfigMap에 시크릿 저장 |
| 네임스페이스 분리 | 환경별(dev/staging/prod) 네임스페이스 분리 | 전부 default 네임스페이스 |

참조: `docs/infra/platform/kubernetes.md`

---

## IaC

| 기준 | PASS | FAIL |
|------|------|------|
| 모듈 구조 | `main.tf`, `variables.tf`, `outputs.tf` 분리 | 단일 파일에 전부 |
| Remote backend | S3+DynamoDB, GCS, Terraform Cloud 등 | local state |
| State locking | DynamoDB lock 또는 동등 메커니즘 | locking 없음 |
| plan → apply | plan 파일 저장 후 apply | 직접 apply |
| 시크릿 제외 | sensitive 마킹, Vault/SSM 참조 | state에 평문 시크릿 |

참조: `docs/infra/platform/iac.md`

---

## Security

| 기준 | PASS | FAIL |
|------|------|------|
| TLS | 모든 외부 엔드포인트 TLS 1.2+ | HTTP 평문 또는 TLS 1.0/1.1 |
| 시크릿 로테이션 | 자동 로테이션 설정 | 수동/무기한 유효 시크릿 |
| 네트워크 격리 | private subnet, Security Group 최소 개방 | 0.0.0.0/0 인바운드 허용 |
| 이미지 스캔 | Trivy/Snyk 등 CI 통합 | 스캔 없음 |

참조: `docs/infra/security/tls-secrets.md`

---

## Observability

| 기준 | PASS | FAIL |
|------|------|------|
| 구조화 로그 | JSON 포맷, severity/trace_id 포함 | 평문 로그 |
| 메트릭 노출 | `/metrics` 엔드포인트 또는 사이드카 | 없음 |
| 알림 규칙 | SLO 기반 alerting rules 정의 | 없음 또는 임계값 없는 알림 |
| 분산 트레이싱 | OpenTelemetry 또는 동등 도구 | 없음 |

참조: `docs/infra/operations/observability.md`

---

## Deployment

| 기준 | PASS | FAIL |
|------|------|------|
| 배포 전략 | rolling/blue-green/canary 중 하나 | 단순 재시작 |
| 롤백 절차 | 자동 롤백 또는 명확한 수동 절차 | 롤백 방법 없음 |
| 헬스체크 연동 | 배포 완료 판정에 헬스체크 사용 | 시간 기반 대기 |

참조: `docs/infra/operations/deployment-strategies.md`

---

## Backup & DR

| 기준 | PASS | FAIL |
|------|------|------|
| 백업 주기 | 데이터 중요도에 맞는 RPO 정의 | 백업 없음 |
| 복구 테스트 | 주기적 복구 드릴 실시 | 테스트 없음 |
| RTO 문서화 | 허용 다운타임 문서화 | 미정의 |

참조: `docs/infra/operations/backup-dr.md`

---

## 판정 규칙

- **PASS**: 모든 기준 충족
- **FAIL**: 하나 이상 기준 미충족 — 구체적 파일:라인과 위반 기준 명시
- **N/A**: 해당 카테고리 인프라 미사용 (예: K8s 미사용 프로젝트의 Kubernetes)
- 개발 환경 설정은 프로덕션 기준 FAIL 제외 — 항목별 주석으로 환경 구분
