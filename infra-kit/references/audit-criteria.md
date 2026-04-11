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

참조:

- `docs/infra/platform/cicd.md`
- 출처: [SLSA Spec](https://slsa.dev/spec)
- 출처: [GitHub Actions OIDC](https://docs.github.com/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- 출처: [PyPI Trusted Publishers](https://docs.pypi.org/trusted-publishers/)
- 출처: [Reusable workflows + OIDC](https://docs.github.com/en/actions/how-tos/security-for-github-actions/security-hardening-your-deployments/using-openid-connect-with-reusable-workflows)

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
| 네트워킹 — Gateway API 우선 | 신규 North-South 트래픽은 Gateway API(`gateway.networking.k8s.io`) 사용 — Ingress API는 frozen, 기존 리소스만 유지 | 신규 프로젝트가 Ingress에만 의존 (대안 미검토) |
| Sidecar containers | 1.33+ 네이티브 사이드카(`restartPolicy: Always` initContainer) 사용 — 로깅/프록시/메쉬 주입 | 레거시 shared-termination hack, PID 관리 커스텀 |

참조:

- `docs/infra/platform/kubernetes.md`
- 출처: [Pod Security Admission](https://kubernetes.io/docs/concepts/security/pod-security-admission/)
- 출처: [Ingress (Gateway API 권장)](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- 출처: [Sidecar containers (stable v1.33)](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers)

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
| GitOps source of truth | Argo CD / Flux가 클러스터 상태를 Git에서 동기화 — 클러스터 직접 변경 금지(drift 감지) | kubectl 직접 apply/edit 운영 |

참조:

- `docs/infra/operations/deployment-strategies.md`
- 출처: [Argo Rollouts](https://argoproj.github.io/argo-rollouts/)
- 출처: [Flux v2.6 release](https://fluxcd.io/blog/2025/05/flux-v2.6.0/)

---

## Backup & DR

| 기준 | PASS | FAIL |
|------|------|------|
| 백업 주기 | 데이터 중요도에 맞는 RPO 정의 | 백업 없음 |
| 복구 테스트 | 주기적 복구 드릴 실시 | 테스트 없음 |
| RTO 문서화 | 허용 다운타임 문서화 | 미정의 |

참조: `docs/infra/operations/backup-dr.md`

---

## Supply Chain

| 기준 | PASS | FAIL |
|------|------|------|
| 이미지 서명(Cosign) | Sigstore Cosign으로 이미지 서명 + 배포 전 `cosign verify` (또는 Kyverno/Policy Controller로 미서명 이미지 차단) | 서명 없음 또는 검증 생략 |
| SBOM 생성 | Trivy / Syft로 CycloneDX 또는 SPDX SBOM 생성 + 아티팩트 저장 + 취약점 스캔(Grype/Trivy) 연동 | SBOM 없음 |
| SLSA provenance | 빌드 시스템이 in-toto attestation(provenance)을 생성 → L3 목표(격리된 빌드, 서명된 provenance) 진행 | provenance 미생성 |
| 런타임 탐지 | eBPF 기반 런타임 보안(Falco / Tetragon) 또는 동등 도구로 정적 스캔 보완 | 런타임 탐지 부재 (정적 스캔만 의존) |
| 베이스 이미지 거버넌스 | distroless 또는 Chainguard Images 같은 minimal + 지속 패치되는 베이스 사용 — CVE 대응 SLA 존재 | unsupported 대형 베이스(`ubuntu:latest`, `debian:latest`) 무기한 사용 |

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

---

## 판정 규칙

- **PASS**: 모든 기준 충족
- **FAIL**: 하나 이상 기준 미충족 — 구체적 파일:라인과 위반 기준 명시
- **N/A**: 해당 카테고리 인프라 미사용 (예: K8s 미사용 프로젝트의 Kubernetes)
- 개발 환경 설정은 프로덕션 기준 FAIL 제외 — 항목별 주석으로 환경 구분
