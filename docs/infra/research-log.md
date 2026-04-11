---
version: 1.0.0
last_updated: 2026-04-11
---

# Infra Kit Research Log

> infra-kaizen 실행 시 리서치한 외부 소스와 채택 여부를 누적 기록한다.

---

## 2026-04-11

**트리거:** kaizen-orchestrator Phase 8 (research-mode rerun)

### 조사한 소스

| # | 제목 | URL | 유형 | 신뢰도 | 결과 |
| - | ---- | --- | ---- | ------ | ---- |
| 1 | Kubernetes Pod Security Admission | <https://kubernetes.io/docs/concepts/security/pod-security-admission/> | 공식 | 높음 | 채택 |
| 2 | Kubernetes Ingress / Gateway API | <https://kubernetes.io/docs/concepts/services-networking/ingress/> | 공식 | 높음 | 채택 |
| 3 | Kubernetes Sidecar Containers (v1.33 GA) | <https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers> | 공식 | 높음 | 채택 |
| 4 | Terraform 1.10+ ephemeral values | <https://developer.hashicorp.com/terraform/language/ephemeral> | 공식 | 높음 | 채택 |
| 5 | Terraform test framework | <https://developer.hashicorp.com/terraform/language/tests> | 공식 | 높음 | 채택 |
| 6 | OpenTofu 1.7+ state encryption | <https://opentofu.org/docs/v1.11/language/state/encryption/> | 공식 | 높음 | 채택 |
| 7 | OpenTofu for_each meta-argument | <https://opentofu.org/docs/language/meta-arguments/for_each/> | 공식 | 높음 | 채택 |
| 8 | SLSA provenance spec | <https://slsa.dev/provenance> | 공식 | 높음 | 채택 |
| 9 | SLSA v1.0 spec | <https://slsa.dev/spec> | 공식 | 높음 | 채택 |
| 10 | Sigstore Cosign attestation | <https://docs.sigstore.dev/cosign/verifying/attestation/> | 공식 | 높음 | 채택 |
| 11 | Trivy SBOM supply chain | <https://trivy.dev/docs/dev/guide/supply-chain/sbom/> | 공식 | 높음 | 채택 |
| 12 | Anchore Syft SBOM generator | <https://github.com/anchore/syft> | 공식 | 높음 | 채택 |
| 13 | Falco runtime security | <https://falco.org/> | 공식 | 높음 | 채택 |
| 14 | Tetragon eBPF runtime security | <https://tetragon.io/> | 공식 | 높음 | 채택 |
| 15 | Chainguard images overview | <https://edu.chainguard.dev/chainguard/chainguard-images/overview/> | 공식 | 높음 | 채택 |
| 16 | PyPI Trusted Publishers | <https://docs.pypi.org/trusted-publishers/> | 공식 | 높음 | 채택 |
| 17 | GitHub OIDC hardening | <https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect> | 공식 | 높음 | 채택 |
| 18 | GitHub OIDC reusable workflows | <https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/using-openid-connect-with-reusable-workflows> | 공식 | 높음 | 채택 |
| 19 | OpenTelemetry signals status | <https://opentelemetry.io/docs/specs/status/> | 공식 | 높음 | 채택 (logs/traces/metrics 3 stable) |
| 20 | OpenTelemetry semantic conventions | <https://opentelemetry.io/docs/specs/semconv/> | 공식 | 높음 | 채택 |
| 21 | Argo Rollouts | <https://argoproj.github.io/argo-rollouts/> | 공식 | 높음 | 채택 |
| 22 | Flux v2.6 release | <https://fluxcd.io/blog/2025/05/flux-v2.6.0/> | 공식 | 높음 | 채택 |

### 채택한 인사이트

- **Kubernetes Pod Security Admission (PSA) restricted** 이 2026 표준. `pod-security.kubernetes.io/enforce: restricted` 라벨로 네임스페이스 단위 강제. 적용: infra-audit Kubernetes 카테고리, init-checklist.
- **Gateway API 우선** (Ingress deprecated 방향 전환 아님, 하지만 Gateway API 가 HTTPRoute / TCPRoute / GRPCRoute 분리로 훨씬 유연). 적용: infra-guide.
- **Sidecar containers v1.33 GA**: init containers 중에 `restartPolicy: Always` 설정 시 sidecar 로 동작. istio proxy / log collector 패턴 표준화. 적용: init-checklist.
- **Terraform 1.10+ ephemeral values**: 민감 정보 (password, token) 를 state 파일에 저장하지 않음. `ephemeral = true` 선언으로 메모리에서만 존재. 적용: infra-audit IaC 카테고리, init-checklist.
- **Terraform test framework**: `terraform test` CLI 로 HCL 네이티브 단위 테스트. 적용: init-checklist.
- **OpenTofu 1.7+ state encryption**: Terraform 이 제공하지 않는 네이티브 state encryption 기능. HashiCorp 라이선스 대안 경로. 적용: infra-audit IaC 카테고리, init-checklist.
- **Supply Chain 카테고리 신설**: SLSA provenance (빌드 출처 증명) + Cosign attestation (서명 검증) + Syft SBOM (소프트웨어 자재 명세서) + Trusted Publishers (OIDC 기반 secretless 배포) + Falco/Tetragon (런타임 security). 2026 공급망 보안의 최소 기본값. 적용: audit-criteria 신규 섹션 5 rules + principle-index 신규 카테고리.
- **OpenTelemetry 3 signals stable**: Logs / Traces / Metrics 모두 stable 단계. 단일 Collector 파이프라인으로 통합 가능. 적용: infra-audit Observability.
- **GitOps 단일 소스 원천**: Argo CD / Flux v2.6+ 을 통한 배포. `kubectl apply` 직접 금지. Progressive delivery (Argo Rollouts) 로 canary / blue-green. 적용: infra-audit Deployment 카테고리.
- **Platform Engineering 카테고리 신설**: Internal Developer Platform (IDP), Backstage scaffolder, golden path. 적용: principle-index 신규 카테고리.

### 신규 스킬 갭 분석

| 제안 스킬 | 아키타입 | 근거 | 우선순위 | 상태 |
| --------- | -------- | ---- | -------- | ---- |
| `infra-supply-chain` | 런북 | SLSA + Cosign + Syft 스캐폴딩 파이프라인 | 높음 | backlog |
| `infra-gitops` | 코드 스캐폴딩 | Argo CD / Flux 부트스트랩 | 중간 | backlog |

### 폐기 사유

없음.

### PR

- <https://github.com/joo6077/claude-plugins/pull/6>
