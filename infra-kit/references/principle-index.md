# Infra-Kit 원칙 인덱스

infra-guide 스킬이 카테고리별 원칙 문서 경로를 찾을 때 참조한다.
각 항목은 `docs/infra/` 하위 리서치 문서로 연결된다.

| 카테고리 | 키워드 | 문서 경로 |
|----------|--------|-----------|
| container | Docker, Dockerfile, Compose, 이미지, 컨테이너 | `docs/infra/platform/container.md` |
| cicd | GitHub Actions, GitLab CI, 파이프라인, workflow, runner | `docs/infra/platform/cicd.md` |
| kubernetes | K8s, Pod, Deployment, Helm, Kustomize, RBAC | `docs/infra/platform/kubernetes.md` |
| iac | Terraform, Pulumi, CDK, 모듈, state, plan | `docs/infra/platform/iac.md` |
| networking | VPC, 서브넷, NAT, DNS, 로드밸런서, ALB, NLB | `docs/infra/operations/networking.md` |
| tls-secrets | TLS, 인증서, cert-manager, Vault, 시크릿 | `docs/infra/security/tls-secrets.md` |
| backup-dr | 백업, DR, RTO, RPO, PITR, 장애 복구 | `docs/infra/operations/backup-dr.md` |
| deployment-strategies | 배포, rolling, blue-green, canary, GitOps, ArgoCD, Flux, Argo Rollouts | `docs/infra/operations/deployment-strategies.md` |
| observability | 모니터링, 로그, 메트릭, 트레이스, Prometheus, Grafana, SLO | `docs/infra/operations/observability.md` |
| incident-response | 인시던트, 장애 대응, 온콜, postmortem, runbook | `docs/infra/operations/incident-response.md` |
| cost-optimization | 비용, rightsizing, Spot, Reserved, FinOps, 태그 | `docs/infra/operations/cost-optimization.md` |
| service-mesh | Istio, Linkerd, sidecar, mTLS, 서비스 메시 | `docs/infra/operations/service-mesh.md` |
| supply-chain | SBOM, Cosign, SLSA, 서명, attestation, 공급망, Syft, Trivy, Chainguard | `docs/infra/platform/container.md` |
| platform-engineering | IDP, Backstage, Port, Cortex, Humanitec, golden path, self-service, scorecard | `docs/infra/platform/cicd.md` |

## 사용 방법

1. 사용자 요청에서 키워드를 매칭해 카테고리를 결정한다.
2. 위 테이블에서 해당 카테고리의 문서 경로를 찾는다.
3. 해당 `docs/infra/` 문서를 읽고, 원칙과 출처 URL을 가이드에 인용한다.
4. 복수 카테고리가 매칭되면 해당 문서 모두 읽는다.

## 주의

- 문서 경로는 레포 루트 기준 상대 경로다.
- 원칙 인용 시 반드시 문서 내 `> **출처:**` 링크를 함께 제시한다.
