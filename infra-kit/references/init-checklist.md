# Infra-Init 세팅 체크리스트

infra-init 스킬이 카테고리별 세팅 범위를 결정할 때 참조한다.
각 카테고리의 필수/권장 여부와 최소 산출물을 정의한다.

---

## 카테고리별 체크리스트

### Container (필수)

- [ ] `Dockerfile` — 멀티스테이지 빌드, non-root USER, HEALTHCHECK
- [ ] `.dockerignore` — `.git`, `node_modules`, `.env`, 테스트 디렉토리 제외
- [ ] `docker-compose.yml` (개발용) — 서비스 의존성, 볼륨, 환경변수 분리
- [ ] `docker-compose.prod.yml` (프로덕션용) — 리소스 제한, 재시작 정책

권장 베이스 이미지: distroless 또는 alpine/slim 계열
참조: `docs/infra/platform/container.md`

---

### CI/CD (필수)

플랫폼별 최소 파이프라인:

| 플랫폼 | 파일 위치 |
|--------|-----------|
| GitHub Actions | `.github/workflows/ci.yml` |
| GitLab CI | `.gitlab-ci.yml` |
| Bitbucket Pipelines | `bitbucket-pipelines.yml` |

최소 파이프라인 단계:
- [ ] build (컴파일/이미지 빌드)
- [ ] test (단위/통합 테스트)
- [ ] security scan (Trivy/Snyk 이미지 스캔)
- [ ] deploy (환경별 분기)

시크릿: 소스코드 직접 포함 금지, Secrets 또는 OIDC 사용
참조: `docs/infra/platform/cicd.md`

---

### 배포 전략 (권장)

- [ ] 배포 방식 선택 및 문서화
  - rolling: 순차 교체 (다운타임 최소, 롤백 느림)
  - blue-green: 트래픽 전환 (즉시 롤백, 리소스 2배)
  - canary: 점진적 트래픽 이동 (안전, 설정 복잡)
- [ ] 롤백 절차 문서화 (runbook 또는 README)
- [ ] 헬스체크 연동 확인

참조: `docs/infra/operations/deployment-strategies.md`

---

### 관측성 (권장)

- [ ] 구조화 로그 포맷 정의 (JSON, severity 필드 포함)
- [ ] 헬스체크 엔드포인트 (`/health`, `/readyz`)
- [ ] 메트릭 노출 (`/metrics` 또는 사이드카 에이전트)
- [ ] 기본 알림 규칙 (에러율, 응답 시간 임계값)

참조: `docs/infra/operations/observability.md`

---

### 시크릿 관리 (필수)

- [ ] `.env.example` — 필요한 환경변수 목록 (값 제외)
- [ ] `.gitignore`에 `.env` 추가 확인
- [ ] 시크릿 저장소 결정 (AWS Secrets Manager / GCP Secret Manager / Vault / GitHub Secrets)
- [ ] 로컬 개발용 시크릿 전달 방법 문서화

참조: `docs/infra/security/tls-secrets.md`

---

### Kubernetes (선택 — K8s 사용 시)

- [ ] `Deployment` — replicas, resources.requests/limits, probes
- [ ] `Service` — ClusterIP/LoadBalancer 선택
- [ ] `ConfigMap` / `Secret` — 환경별 분리
- [ ] `HorizontalPodAutoscaler` — 트래픽 기반 자동 확장
- [ ] RBAC — 최소 권한 ServiceAccount

참조: `docs/infra/platform/kubernetes.md`

---

### IaC (선택 — Terraform/Pulumi/CDK 사용 시)

- [ ] 표준 모듈 구조 (`main.tf`, `variables.tf`, `outputs.tf`)
- [ ] Remote backend 설정 (S3+DynamoDB / GCS / Terraform Cloud)
- [ ] State locking 활성화
- [ ] `.gitignore`에 `*.tfstate`, `.terraform/` 추가

참조: `docs/infra/platform/iac.md`

---

## 우선순위 결정 가이드

| 프로젝트 규모 | 필수 | 권장 | 선택 |
|--------------|------|------|------|
| 소규모 (1-3인) | Container + CI/CD + 시크릿 | 관측성 | — |
| 중규모 (4-10인) | 위 + 배포 전략 + 관측성 | K8s 또는 IaC 중 택1 | — |
| 대규모 (10인+) | 전체 필수 + 권장 | — | 모두 검토 |

K8s: 컨테이너 오케스트레이션이 필요한 경우만 도입. 단일 서비스에 K8s 강제 금지.
IaC: 인프라가 코드로 반복 생성되어야 할 때 도입. 소규모 단일 서비스는 콘솔/CLI로 충분.
