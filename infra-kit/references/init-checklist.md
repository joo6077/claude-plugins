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

권장 베이스 이미지: distroless, Chainguard Images, 또는 alpine/slim 계열 — CVE 대응 SLA 확인
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
- [ ] **SBOM 생성** (Syft 또는 Trivy — CycloneDX 또는 SPDX 포맷, 아티팩트로 저장)
- [ ] **이미지 서명** (Sigstore Cosign keyless + OIDC, 저장 후 `cosign verify` 배포 게이트)
- [ ] **SLSA provenance** (in-toto attestation 생성 → 레지스트리에 첨부 → 배포 전 `verify-attestation`)
- [ ] deploy (환경별 분기)
- [ ] **Actions SHA 핀닝** — 서드파티 액션은 SHA 해시로 고정, 조직 정책으로 뮤터블 태그 차단
- [ ] **Arm runner 검토** — GitHub Actions `ubuntu-24.04-arm` / `windows-11-arm` 러너로 멀티아키텍처 CI 표준화 (2026 가격 최대 39% 인하)

시크릿: 소스코드 직접 포함 금지. **secretless CI 우선** — 클라우드/레지스트리 인증은 OIDC short-lived federation, 공개 패키지 배포는 PyPI Trusted Publishers / npm provenance. reusable workflow + environment protection으로 신뢰 경계 고정.

참조:

- `docs/infra/platform/cicd.md`
- 출처: [SLSA spec](https://slsa.dev/spec)
- 출처: [Sigstore Cosign](https://docs.sigstore.dev/cosign/verifying/attestation/)
- 출처: [PyPI Trusted Publishers](https://docs.pypi.org/trusted-publishers/)

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
- [ ] **OpenTelemetry Collector + OTLP** — 3 신호(메트릭/로그/트레이스)를 OTel Collector로 통합 export, `service.name` 등 semantic conventions 준수 (Logs spec 2025 stable)
- [ ] **Grafana Alloy 마이그레이션** — Grafana Agent/Operator 2025-11 EOL → Alloy(120+ 컴포넌트, Prometheus 파이프라인 내장) 또는 vanilla OTel Collector로 전환
- [ ] **연속 프로파일링 (권장)** — eBPF 기반 `pyroscope.ebpf` 또는 동등 도구로 CPU/메모리 핫스팟 상시 수집

참조:

- `docs/infra/operations/observability.md`
- 출처: [OpenTelemetry spec status](https://opentelemetry.io/docs/specs/status/)
- 출처: [Grafana Alloy](https://grafana.com/oss/alloy-opentelemetry-collector/)

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
- [ ] **Pod Security Admission 라벨** — 네임스페이스에 `pod-security.kubernetes.io/enforce=baseline` 최소, 신규는 `restricted` 목표. `warn`/`audit` 단계적 도입
- [ ] **Gateway API 우선** — 신규 North-South 트래픽은 `gateway.networking.k8s.io` 사용 (Ingress API는 frozen, 기존 리소스만 유지)
- [ ] **Sidecar containers (v1.33+ stable)** — 사이드카는 `initContainers` + `restartPolicy: Always` 네이티브 사이드카 패턴 사용 (레거시 shared-termination hack 금지)
- [ ] **In-Place Pod Resource Updates (v1.35+ GA)** — CPU/메모리 변경 시 `resize` 서브리소스 활용, Pod 재시작 없이 동적 조정 (KEP #1287)
- [ ] **Karpenter 오토스케일러 검토** — NodePool CRD 선언적 프로비저닝 + 미사용 노드 자동 교체, Cluster Autoscaler 대비 빠른 스케일업
- [ ] **DRA (Dynamic Resource Allocation)** — v1.35 GA, GPU 등 특수 하드웨어 표준화된 할당 인터페이스

참조:

- `docs/infra/platform/kubernetes.md`
- 출처: [Pod Security Admission](https://kubernetes.io/docs/concepts/security/pod-security-admission/)
- 출처: [Ingress → Gateway API 권장](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- 출처: [Sidecar containers (stable v1.33)](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers)
- 출처: [Kubernetes v1.35 Release](https://kubernetes.io/blog/2025/12/17/kubernetes-v1-35-release/)
- 출처: [Karpenter v1.11](https://karpenter.sh/)

---

### IaC (선택 — Terraform/OpenTofu/Pulumi/CDK 사용 시)

- [ ] 표준 모듈 구조 (`main.tf`, `variables.tf`, `outputs.tf`)
- [ ] Remote backend 설정 (S3+DynamoDB / GCS / Terraform Cloud)
- [ ] State locking 활성화
- [ ] `.gitignore`에 `*.tfstate`, `.terraform/` 추가
- [ ] **State encryption** — OpenTofu 1.7+는 native state encryption, Terraform은 backend-level 암호화(SSE-S3/CMEK)
- [ ] **Ephemeral values** — Terraform 1.10+ `ephemeral` 블록 / write-only arguments로 시크릿이 state/plan에 저장되지 않게 구성
- [ ] **모듈 테스트** — `terraform test` / `tofu test` 모듈 테스트 프레임워크 도입 (1.7+ mocking 지원)
- [ ] **OpenTofu 대안 검토** — v1.7+ native state encryption, v1.9+ provider-level `for_each`, v1.10+ OCI Registry 지원 + S3 네이티브 state locking (DynamoDB 불필요)
- [ ] **Crossplane v2 검토 (대규모)** — K8s CRD 기반 인프라 합성 + 플랫폼 팀 선언적 API 엔진, namespaced XR/MR 기본값

참조:

- `docs/infra/platform/iac.md`
- 출처: [Terraform Ephemeral values](https://developer.hashicorp.com/terraform/language/ephemeral)
- 출처: [Terraform tests](https://developer.hashicorp.com/terraform/language/tests)
- 출처: [OpenTofu state encryption](https://opentofu.org/docs/v1.11/language/state/encryption/)
- 출처: [OpenTofu provider for_each](https://opentofu.org/docs/language/meta-arguments/for_each/)

---

### Supply Chain (권장)

- [ ] **SBOM 생성** — CI에서 Syft 또는 Trivy로 CycloneDX(ECMA-424) 또는 SPDX SBOM 자동 생성 + 아티팩트 보존
- [ ] **이미지 서명** — Sigstore Cosign v3 keyless + OIDC, 번들 포맷(서명+오프라인 검증 단일 파일) + trusted-root
- [ ] **SLSA provenance** — in-toto attestation 생성 → L3 목표(격리 빌드, 서명 provenance) 진행
- [ ] **EU CRA 대응** (EU 대상 제품) — **2026-09 취약점 보고 의무 시행**, 직접+전이 의존성 SBOM 필수
- [ ] **베이스 이미지 거버넌스** — distroless/Chainguard Images 사용, CVE 대응 SLA 확인

참조:

- `docs/infra/platform/container.md`
- 출처: [EU CRA SBOM](https://craevidence.com/blog/sbom-requirements-under-cra)
- 출처: [CycloneDX ECMA-424](https://cyclonedx.org/)
- 출처: [Cosign v3](https://blog.sigstore.dev/cosign-3-0-available/)

---

### Backup & DR (권장 — 프로덕션 시)

- [ ] **데이터 백업** — RPO/RTO 정의 + 자동 백업 스케줄
- [ ] **K8s 백업** — Velero로 etcd + PV 이중 백업, 스케줄 + 보존 정책 + pre/post 훅
- [ ] **크로스 리전 복구** — 크로스 리전 또는 크로스 클러스터 복구 경로 검증
- [ ] **복구 드릴** — 주기적 복구 테스트 일정 수립

참조:

- `docs/infra/operations/backup-dr.md`
- 출처: [Velero](https://velero.io/)

---

### Cost Optimization (권장)

- [ ] **리소스 태깅 전략** — team, env, service, cost-center 태그 일관 적용
- [ ] **Shift-Left 비용 예측** — IaC plan 단계에서 비용 변화 예측(Infracost 등), PR 코멘트로 가시화
- [ ] **FOCUS 표준 검토** (멀티클라우드) — 멀티 벤더 비용 데이터 정규화
- [ ] **AI 워크로드 비용 분리** — GPU/TPU에 별도 태그 + 사용률 모니터링

참조:

- `docs/infra/operations/cost-optimization.md`
- 출처: [State of FinOps 2026](https://data.finops.org/)

---

## 우선순위 결정 가이드

| 프로젝트 규모 | 필수 | 권장 | 선택 |
|--------------|------|------|------|
| 소규모 (1-3인) | Container + CI/CD + 시크릿 | 관측성 | — |
| 중규모 (4-10인) | 위 + 배포 전략 + 관측성 | K8s 또는 IaC 중 택1 | — |
| 대규모 (10인+) | 전체 필수 + 권장 | — | 모두 검토 |

K8s: 컨테이너 오케스트레이션이 필요한 경우만 도입. 단일 서비스에 K8s 강제 금지.
IaC: 인프라가 코드로 반복 생성되어야 할 때 도입. 소규모 단일 서비스는 콘솔/CLI로 충분.
