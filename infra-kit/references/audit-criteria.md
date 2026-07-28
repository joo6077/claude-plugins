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
| 시크릿 관리 — Secretless 우선 | Secrets/Vault 사용 + OIDC short-lived federation / Reusable workflow 신뢰 경계 / PyPI/npm Trusted Publishers | 소스코드 또는 로그에 시크릿 노출, 장기 정적 키 |
| OIDC 인증 | OIDC로 클라우드 인증 (장기 키 없음) + reusable workflow 단위로 신뢰 조건 고정 | 장기 액세스 키 사용, workflow 전역 권한 |
| SLSA provenance | 빌드 시 in-toto provenance(attestation) 생성 및 레지스트리 서명 + 배포 전 `verify-attestation` 검증 | provenance 미생성 또는 미검증 |
| 캐싱 | 의존성 캐시 레이어 설정 | 매 실행 전체 재설치 |
| 아티팩트 보존 | 빌드 산출물 저장 설정 + SBOM/provenance 동시 보존 | 없음 |
| Actions SHA 핀닝 | 서드파티 액션을 SHA 해시로 고정 (`uses: actions/checkout@<sha>`) — 조직 정책으로 뮤터블 태그 차단 | 뮤터블 태그(`@v4`)만 사용, SHA 미고정 |
| Immutable Releases | GitHub Actions 2026 Immutable Releases 적용 — 발행 후 에셋/태그 변경 불가 + `dependencies:` 섹션으로 직접+전이 의존성 SHA 잠금 | 릴리스 에셋 변조 가능 상태 |
| 셸 실패 전파 | 파이프를 쓰는 `run` 스텝에 `shell: bash` 명시(= `bash --noprofile --norc -eo pipefail {0}`), 또는 스크립트 첫 줄 `set -euo pipefail` | 기본 셸(`bash -e {0}`, pipefail 없음)에서 파이프 사용 — 중간 명령 실패가 통과로 집계됨 |
| 검증 스텝 exit code | 게이트 역할 스텝/스크립트가 결함 발견 시 비영 exit 로 종료 | 결함을 `echo WARN` 만 하고 exit 0 — 파이프라인이 항상 통과 |

참조:

- `docs/infra/platform/cicd.md`
- 출처: [GitHub Actions workflow syntax — default shell](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- 출처: [Docker best practices — pipefail](https://docs.docker.com/build/building/best-practices/)
- 출처: [SLSA Spec](https://slsa.dev/spec)
- 출처: [GitHub Actions OIDC](https://docs.github.com/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- 출처: [PyPI Trusted Publishers](https://docs.pypi.org/trusted-publishers/)
- 출처: [Reusable workflows + OIDC](https://docs.github.com/en/actions/how-tos/security-for-github-actions/security-hardening-your-deployments/using-openid-connect-with-reusable-workflows)
- 출처: [GitHub Actions SHA Pinning Policy](https://github.blog/changelog/2025-08-15-github-actions-policy-now-supports-blocking-and-sha-pinning-actions/)
- 출처: [GitHub Actions 2026 Security Roadmap](https://github.blog/news-insights/product-news/whats-coming-to-our-github-actions-2026-security-roadmap/)

---

## Kubernetes

| 기준 | PASS | FAIL |
|------|------|------|
| 리소스 제한 | `resources.requests` + `limits` 설정 | 미설정 |
| 활성/준비 프로브 | `livenessProbe` + `readinessProbe` | 없음 |
| RBAC | 최소 권한 ServiceAccount, ClusterRole 금지 | 와일드카드 권한 또는 cluster-admin |
| 시크릿 분리 | Secret 오브젝트 사용, 환경변수 주입 | ConfigMap에 시크릿 저장 |
| 네임스페이스 분리 | 환경별(dev/staging/prod) 네임스페이스 분리 | 전부 default 네임스페이스 |
| Pod Security Admission | 네임스페이스에 `pod-security.kubernetes.io/enforce` 라벨로 `baseline` 이상 (신규는 `restricted` 목표) — warn/audit 단계적 승격 | PSA 라벨 없음 또는 `privileged` enforce |
| 네트워킹 — Gateway API 우선 | 신규 North-South 트래픽은 Gateway API(`gateway.networking.k8s.io`) 사용 — v1.4 BackendTLSPolicy GA, v1.5 TLSRoute Standard Channel. Ingress API는 frozen, 기존 리소스만 유지 | 신규 프로젝트가 Ingress에만 의존 (대안 미검토) |
| Sidecar containers | 1.33+ 네이티브 사이드카(`restartPolicy: Always` initContainer) 사용 — 로깅/프록시/메쉬 주입 | 레거시 shared-termination hack, PID 관리 커스텀 |
| In-Place Pod Resource Updates | v1.35+ 리소스 변경 시 `resize` 서브리소스 활용 — Pod 재시작 없이 CPU/메모리 동적 조정 (KEP #1287 GA) | 리소스 변경마다 Pod 재배포 (v1.35+ 클러스터에서) |
| 노드 오토스케일링 | Karpenter(v1.11+) 또는 Cluster Autoscaler 구성 — NodePool CRD 선언적 프로비저닝 + 미사용 노드 자동 교체 | 오토스케일러 미설정으로 수동 노드 관리 |

참조:

- `docs/infra/platform/kubernetes.md`
- 출처: [Pod Security Admission](https://kubernetes.io/docs/concepts/security/pod-security-admission/)
- 출처: [Ingress (Gateway API 권장)](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- 출처: [Gateway API v1.4 — BackendTLSPolicy GA](https://kubernetes.io/blog/2025/11/06/gateway-api-v1-4/)
- 출처: [TLSRoute — Gateway API v1.5](https://gateway-api.sigs.k8s.io/api-types/tlsroute/)
- 출처: [Sidecar containers (stable v1.33)](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers)
- 출처: [Kubernetes v1.35 In-Place Pod Resource Updates GA](https://kubernetes.io/blog/2025/12/17/kubernetes-v1-35-release/)
- 출처: [Karpenter v1.11](https://karpenter.sh/)

---

## IaC

| 기준 | PASS | FAIL |
|------|------|------|
| 모듈 구조 | `main.tf`, `variables.tf`, `outputs.tf` 분리 | 단일 파일에 전부 |
| Remote backend | S3+DynamoDB, GCS, Terraform Cloud 등 | local state |
| State locking | DynamoDB lock 또는 동등 메커니즘 | locking 없음 |
| plan → apply | plan 파일 저장 후 apply | 직접 apply |
| 시크릿 제외 — Ephemeral values 우선 | Terraform 1.10+ `ephemeral` 블록 / write-only arguments / `ephemeralasnull` 사용 또는 Vault/SSM 참조 (state 비저장) | state 또는 plan JSON에 평문 시크릿, sensitive 마킹만 의존 |
| State encryption | OpenTofu 1.7+ native state encryption 또는 backend-level 암호화(SSE-S3/CMEK/Cloud KMS) + 접근 제어 | 암호화 미설정 remote state |
| 테스트 프레임워크 | `terraform test` / OpenTofu `tofu test` 모듈 테스트(1.7+ mocking 포함) 존재 | 모듈 테스트 전혀 없음 |
| S3 네이티브 State Locking | OpenTofu 1.10+는 S3 네이티브 locking 지원 (DynamoDB 불필요) — 해당 버전 사용 시 DynamoDB 제거 검토 | OpenTofu 1.10+ 사용하면서 DynamoDB 불필요 유지 |
| OCI Registry 모듈 | OpenTofu 1.10+는 OCI Registry에서 모듈/프로바이더 배포 지원 — 에어갭 환경에서 활용 | 에어갭 환경에서 HTTP 미러 수동 관리 |

참조:

- `docs/infra/platform/iac.md`
- 출처: [Terraform Ephemeral values](https://developer.hashicorp.com/terraform/language/ephemeral)
- 출처: [OpenTofu State encryption](https://opentofu.org/docs/v1.11/language/state/encryption/)
- 출처: [Terraform tests](https://developer.hashicorp.com/terraform/language/tests)

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
| OpenTelemetry 3 신호 통합 | OTel SDK/Collector로 메트릭·로그·트레이스 수집 (Logs spec 2025 stable), `service.name`/`trace_id` semantic conventions 준수 | 트레이스만 있고 로그·메트릭과 trace_id 연결 불가, semconv 미준수 |
| OTel Collector 마이그레이션 | Grafana Agent/Operator 2025-11 EOL → Grafana Alloy 또는 vanilla OTel Collector로 마이그레이션 완료 | EOL된 Grafana Agent/Operator 계속 사용 |
| 연속 프로파일링 (권장) | eBPF 기반 연속 프로파일링(Grafana Alloy `pyroscope.ebpf` 또는 동등) — CPU/메모리 핫스팟 상시 수집 | 프로파일링 도구 없음 (장애 시 ad-hoc 분석만 의존) |

참조:

- `docs/infra/operations/observability.md`
- 출처: [OpenTelemetry spec status (Logs stable)](https://opentelemetry.io/docs/specs/status/)
- 출처: [OpenTelemetry Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/)

---

## Deployment

| 기준 | PASS | FAIL |
|------|------|------|
| 배포 전략 | rolling/blue-green/canary 중 하나 | 단순 재시작 |
| 롤백 절차 | 자동 롤백 또는 명확한 수동 절차 | 롤백 방법 없음 |
| 헬스체크 연동 | 배포 완료 판정에 헬스체크 사용 | 시간 기반 대기 |
| GitOps source of truth | Argo CD 3.x / Flux v2.8+가 클러스터 상태를 Git에서 동기화 — 클러스터 직접 변경 금지(drift 감지). Argo CD v2.14 EOL(2025-11) 이전 마이그레이션 완료 | kubectl 직접 apply/edit 운영, 또는 EOL된 Argo CD v2.x 사용 |
| Progressive Delivery | Argo Rollouts로 canary/blue-green 자동 분석 — 메트릭 기반 자동 프로모션/롤백 | 수동 트래픽 전환 또는 rolling만 사용 |

참조:

- `docs/infra/operations/deployment-strategies.md`
- 출처: [Argo Rollouts](https://argoproj.github.io/argo-rollouts/)
- 출처: [Flux v2.8 release](https://fluxcd.io/blog/2026/02/flux-v2.8.0/)
- 출처: [Argo CD 3.0 Upgrade](https://argo-cd.readthedocs.io/en/latest/operator-manual/upgrading/2.14-3.0/)

---

## Backup & DR

| 기준 | PASS | FAIL |
|------|------|------|
| 백업 주기 | 데이터 중요도에 맞는 RPO 정의 | 백업 없음 |
| 복구 테스트 | 주기적 복구 드릴 실시 | 테스트 없음 |
| RTO 문서화 | 허용 다운타임 문서화 | 미정의 |
| K8s 백업 도구 | Velero(또는 동등)로 etcd + PV 이중 백업 — 스케줄 백업 + 보존 정책 + pre/post 훅 구성 | K8s 클러스터 사용하면서 백업 도구 미설정 |
| 크로스 리전 복구 | 크로스 리전 또는 크로스 클러스터 복구 경로 검증 — Velero + Restic 증분 백업으로 RPO/RTO 최소화 | 단일 리전 백업만 존재 |

참조: `docs/infra/operations/backup-dr.md`

---

## Cost Optimization / FinOps

| 기준 | PASS | FAIL |
|------|------|------|
| 리소스 태깅 전략 | 모든 클라우드 리소스에 일관된 태깅(team, env, service, cost-center) — 비용 귀속 가능 | 태그 없거나 비일관적 |
| Shift-Left 비용 예측 | IaC plan/preview 단계에서 비용 변화 예측(Infracost 등) — PR 코멘트로 비용 영향 가시화 | 배포 후에만 비용 확인 |
| FOCUS 표준 (권장) | 멀티 벤더 비용 데이터를 FOCUS(FinOps Open Cost and Usage Specification)로 정규화 | 벤더별 개별 비용 포맷 수동 비교 |
| AI 워크로드 비용 추적 | GPU/TPU 워크로드에 별도 비용 태그 + 사용률 모니터링 — FinOps 2026 기준 AI 관리 98% | AI 워크로드 비용이 일반 컴퓨팅에 묻혀 추적 불가 |

참조:

- `docs/infra/operations/cost-optimization.md`
- 출처: [State of FinOps 2026](https://data.finops.org/)
- 출처: [FOCUS Specification](https://www.finops.org/insights/finops-x-2025-cloud-announcements/)

---

## Supply Chain

| 기준 | PASS | FAIL |
|------|------|------|
| 이미지 서명(Cosign) | Sigstore Cosign으로 이미지 서명 + 배포 전 `cosign verify` (또는 Kyverno/Policy Controller로 미서명 이미지 차단) | 서명 없음 또는 검증 생략 |
| SBOM 생성 | Trivy / Syft로 CycloneDX 또는 SPDX SBOM 생성 + 아티팩트 저장 + 취약점 스캔(Grype/Trivy) 연동 | SBOM 없음 |
| SLSA provenance | 빌드 시스템이 in-toto attestation(provenance)을 생성 → L3 목표(격리된 빌드, 서명된 provenance) 진행 | provenance 미생성 |
| 런타임 탐지 | eBPF 기반 런타임 보안(Falco / Tetragon) 또는 동등 도구로 정적 스캔 보완 | 런타임 탐지 부재 (정적 스캔만 의존) |
| 베이스 이미지 거버넌스 | distroless 또는 Chainguard Images 같은 minimal + 지속 패치되는 베이스 사용 — CVE 대응 SLA 존재 | unsupported 대형 베이스(`ubuntu:latest`, `debian:latest`) 무기한 사용 |
| EU CRA SBOM 규정 | EU 시장 대상 제품은 CycloneDX(ECMA-424) 또는 SPDX 머신리더블 SBOM 필수 — 직접+전이 의존성 전부 포함, **2026-09 취약점 보고 의무 시행** | EU 대상 제품이면서 SBOM 미생성 또는 전이 의존성 누락 |
| Cosign v3 번들 포맷 | Cosign v3 번들(서명+오프라인 검증 단일 파일) + trusted-root(키 회전 시 클라이언트 업데이트 불필요) 사용 | Cosign v2 레거시 포맷 사용 또는 키 회전 미대응 |

참조:

- `docs/infra/platform/container.md`
- `docs/infra/platform/cicd.md`
- 출처: [Sigstore Cosign — verifying attestation](https://docs.sigstore.dev/cosign/verifying/attestation/)
- 출처: [SLSA provenance](https://slsa.dev/provenance)
- 출처: [Trivy SBOM guide](https://trivy.dev/docs/dev/guide/supply-chain/sbom/)
- 출처: [Syft](https://github.com/anchore/syft)
- 출처: [Falco](https://falco.org/)
- 출처: [Tetragon](https://tetragon.io/)
- 출처: [Chainguard Images](https://edu.chainguard.dev/chainguard/chainguard-images/overview/)
- 출처: [EU Cyber Resilience Act SBOM](https://craevidence.com/blog/sbom-requirements-under-cra)
- 출처: [CycloneDX ECMA-424](https://cyclonedx.org/)
- 출처: [Cosign v3 릴리스](https://blog.sigstore.dev/cosign-3-0-available/)

---

## 판정 규칙

- **PASS**: 모든 기준 충족
- **FAIL**: 하나 이상 기준 미충족 — 구체적 파일:라인과 위반 기준 명시
- **N/A**: 해당 카테고리 인프라 미사용 (예: K8s 미사용 프로젝트의 Kubernetes, EU 비대상 제품의 CRA SBOM)
- 개발 환경 설정은 프로덕션 기준 FAIL 제외 — 항목별 주석으로 환경 구분
- **(권장)** 표시 항목은 미충족 시 WARN (FAIL 아님) — 단, 프로덕션 대규모 환경에서는 FAIL 승격 가능
