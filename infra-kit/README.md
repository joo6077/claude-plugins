# infra-kit

스택 무관 인프라/DevOps 가이드, 감사, 초기 세팅 플러그인.

## 개요

인프라 설정(Docker, CI/CD, K8s, Terraform 등)에 대해 원칙 기반 가이드를 제공하고, 체계적 감사를 수행하며, 프로젝트 인프라 기반을 초기 세팅한다. 특정 클라우드 벤더(AWS, GCP, Azure)에 종속되지 않는 범용 원칙을 다룬다.

## 스킬

| 스킬 | 용도 |
|------|------|
| `/infra-guide` | 인프라 설정에 대한 원칙 기반 가이드 (가벼운 리뷰) |
| `/infra-audit` | 인프라 설정을 카테고리별 PASS/FAIL로 체계적 감사 |
| `/infra-init` | 프로젝트 인프라 기반 초기 세팅 (Docker, CI/CD, 시크릿 등) |
| `/infra-test` | 인프라 설정 테스트 자동 생성 (Terraform test, hadolint, actionlint, kubeconform 등) |

## 에이전트

| 에이전트 | 용도 |
|---------|------|
| `infra-reviewer` | infra-audit에서 호출하는 읽기 전용 독립 평가 에이전트 |

## 리서치 문서

`docs/infra/` 디렉토리에 12개 원칙 문서가 있으며, 모든 스킬이 이를 SSOT로 참조한다.

### Platform
- **container** — Dockerfile best practices, 멀티스테이지, non-root, 리소스 제한
- **cicd** — GitHub Actions/GitLab CI, OIDC, 최소 권한, 캐싱, self-hosted runner
- **kubernetes** — requests/limits, 프로브, RBAC, Pod Security, HPA/VPA, Helm/Kustomize
- **iac** — Terraform 모듈, 상태 관리, drift, plan/apply, policy as code

### Operations
- **networking** — VPC/서브넷, CIDR, NAT, SG/NACL, ALB/NLB, DNS
- **backup-dr** — RTO/RPO, PITR, 멀티리전 DR, 장애 복구 runbook
- **deployment-strategies** — Rolling/Blue-Green/Canary, GitOps, SLI/SLO 기반 롤백
- **observability** — 메트릭/로그/트레이스, OpenTelemetry, SLI/SLO, 알림 설계
- **incident-response** — Severity 분류, 온콜, runbook, postmortem, chaos engineering
- **cost-optimization** — FinOps, rightsizing, Reserved/Spot, 스토리지 티어링
- **service-mesh** — Istio/Linkerd, sidecar/ambient, mTLS, 트래픽 관리

### Security
- **tls-secrets** — TLS 1.3, cert-manager, 시크릿 관리, 키 로테이션

## 카이젠

- `/infra-research` — 외부 소스 크롤링으로 docs/infra/ 문서 갱신
- `/infra-kaizen` — 리서치 문서 기준으로 스킬 품질 점진 개선

## 검증

- `python3 scripts/run-evals.py infra-kit` — 4 스킬 assertion 전수 검증 (exit 0 = PASS, 1 = FAIL, 2 = 파싱 오류)
- `python3 scripts/validate-plugin.py infra-kit` — 7 카테고리 구조 감사 (refs/placeholders/code-fence 등)

## Phase 8 kaizen (2026-04-24)

- Phase 1~7 누적 원칙 전수 반영 (Binary Decidability · Rule-by-Rule Audit · Enumerate-before-Act · Cross-Surface Parity · CONDITIONAL APPROVE · L3 Coverage Honesty · 미검증 마커)
- 리서치 반영: Kubernetes PSA · Terraform 1.10+ ephemeral · OpenTelemetry 3 signals stable · OpenTofu state encryption · SLSA provenance · Sigstore Cosign v3
- REJECT reason 해소: AR-03 · AR-04 · SK-07 · SK-08 · SK-13
- Sibling Parity: infra-test ↔ backend-test Step 0 스택 감지 + 기존 패턴 탐색 + 외부 실환경 금지 3 항목 동기화

## Phase 8 kaizen (2026-05-07)

- Phase 1 v1.3.0 신규 원칙 흡수 — `/insights` Friction #1·#2·#3 의 infra-kit 측 reframe
- 적용 매핑은 **harness/references/cross-kit-principles.md** infra-kit 열 참조
- infra-audit ANALYZE ↔ Pre-Edit Batch Audit, infra-reviewer self-check ↔ Self-Evaluator Audit, PostToolUse hadolint/actionlint ↔ Hook-Triggered Auto-Correction
