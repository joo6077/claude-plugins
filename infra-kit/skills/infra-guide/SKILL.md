---
name: infra-guide
description: >
  인프라/DevOps 설정·코드를 받아 관련 인프라 원칙을 참조하여 가이드한다.
  스택 무관 — 원칙과 이유만 설명하고 구현은 프로젝트 환경에 맞게 적용.
  "인프라 가이드", "이 Dockerfile 괜찮아?", "CI 파이프라인 조언",
  "K8s 설정 리뷰" (가벼운 리뷰) 같은 요청 시 트리거.
  체계적 전수 검사에는 트리거하지 않는다 — infra-audit 사용.
argument-hint: "[file-path or description]"
user-invocable: true
---

# Gotchas

1. **클라우드 벤더 특정 코드 강제 금지** — AWS/GCP/Azure 특정 설정을 강제하지 마라. 원칙만 설명하고 벤더 선택은 사용자에게 맡겨라. `supply-chain`(Chainguard Images / Sigstore), `platform-engineering`(Backstage / Port / Cortex / Humanitec) 카테고리에서도 특정 벤더·배포판을 강제 처방하지 마라 — 원칙과 상호운용 표준(CycloneDX/SPDX, in-toto attestation, OCI)을 기준으로 설명하고 선택지는 제시만 한다.
2. **주관적 피드백 금지** — "잘 구성됐다" 같은 표현 금지. 반드시 출처가 있는 원칙을 근거로 제시하라.
3. **카테고리 과잉 방지** — Dockerfile 질문에 K8s/Terraform 원칙을 섞지 마라. 맥락에 관련된 원칙만 집중.
4. **리서치 문서 없이 답변 금지** — principle-index.md를 통해 해당 원칙 문서를 읽은 후 답변하라.
5. **보안 관련 질문에 "나중에 하면 된다" 금지** — Dockerfile의 root 실행, 시크릿 하드코딩, TLS 미설정 같은 보안 이슈는 "개발 단계니까 나중에"라고 미루지 마라. 초기부터 non-root, 환경변수 기반 시크릿, TLS 설정을 권장해야 한다.
6. **특정 도구 버전을 강제하지 마라** — "Terraform 1.8을 써라" 대신 "OpenTofu/Terraform 1.x 이상에서 `ephemeral` 변수를 활용하라"처럼 기능 기준으로 설명하라. 사용자의 기존 도구 버전을 먼저 확인한다.
7. **비용 영향 없이 인프라 변경 권고 금지** — NAT Gateway 추가, 멀티 AZ 전환, CDN 도입 등을 권고할 때 비용 증가 예상치를 함께 언급해야 한다. "모범 사례이므로 적용하라"만으로는 부족하다.
8. **원칙과 구현을 혼동하지 마라** — "컨테이너는 non-root로 실행하라"(원칙)와 "USER 1001:1001을 Dockerfile에 추가하라"(구현)를 구분하라. 이 스킬은 원칙만 설명하고, 구체적 Dockerfile 코드 작성은 프로젝트 환경에 맞게 사용자가 결정한다.
9. **Enumerate-before-Act (skill-design-guide §5.5 대응)** — 가이드 제공 전에 해당 설정/설명에서 **관련 원칙 위반 후보를 전부 나열** 한 뒤 한 번에 제시하라. "하나 고치면 다음에 또 지적"의 round-trip 을 차단한다 (/insights 마찰점 #1). 예: CI workflow 를 보면 장기 AWS 키 / 서드파티 액션 태그 참조 / 시크릿 로그 출력 / 의존성 캐시 미설정 을 한 번에 모두 나열하고 사용자 승인을 기다린다.
10. **3-Step Process (Phase 5/7 backend-guide parity)** — 가이드형 스킬은 반드시 탐색(설정/설명 맥락 파악) → 진단(원칙 위반 rule-by-rule 열거) → 처방(우선순위 + 트레이드오프 + 출처) 3단계를 **순서 고정** 으로 따른다. 맥락 없이 바로 처방을 내지 말 것.
11. **트레이드오프 없이 "~해야 한다"만 쓰지 마라** — 인프라 결정에는 항상 트레이드오프가 있다. "Gateway API 로 전환하라" 가 아니라 "Gateway API v1.4 는 BackendTLSPolicy GA 로 L4 TLS 분리 가능. 반면 Ingress 대비 리소스 타입이 늘어 초기 학습 비용 증가" 처럼 양면을 제시.

# Process (3-Step · 탐색 → 진단 → 처방)

## Step 1: 탐색 — 맥락 파악

사용자가 제공한 설정/설명에서 관련 인프라 카테고리를 식별한다:

| 카테고리 | 키워드 |
|----------|--------|
| container | Docker, Dockerfile, Compose, 이미지, 컨테이너 |
| cicd | GitHub Actions, GitLab CI, 파이프라인, workflow, runner |
| kubernetes | K8s, Pod, Deployment, Helm, Kustomize, RBAC, Pod Security, Gateway API, TLSRoute, Sidecar, Karpenter, In-Place Resize, DRA |
| iac | Terraform, Pulumi, CDK, OpenTofu, Crossplane, 모듈, state, plan, ephemeral, Pulumi ESC |
| networking | VPC, 서브넷, NAT, DNS, 로드밸런서, ALB, NLB |
| tls-secrets | TLS, 인증서, cert-manager, Vault, 시크릿 |
| backup-dr | 백업, DR, RTO, RPO, PITR, Velero, etcd, 크로스 리전, 장애 복구 |
| deployment-strategies | 배포, rolling, blue-green, canary, GitOps, ArgoCD 3.x, Flux v2.8, Argo Rollouts, progressive delivery |
| observability | 모니터링, 로그, 메트릭, 트레이스, Prometheus, Grafana, Alloy, OpenTelemetry, SLO, eBPF profiling |
| incident-response | 인시던트, 장애 대응, 온콜, postmortem, runbook |
| cost-optimization | 비용, rightsizing, Spot, Reserved, FinOps, FOCUS, shift-left, 태그, AI 비용 |
| service-mesh | Istio, Linkerd, Cilium, eBPF, sidecar, mTLS, 서비스 메시 |
| supply-chain | SBOM, Cosign v3, SLSA, 서명, attestation, 공급망, Syft, Trivy, CycloneDX, EU CRA |
| platform-engineering | IDP, Backstage, Port, Cortex, Crossplane, Dagger, golden path, self-service, scorecard |
| sustainability | Green Software, 탄소, RTC, SCI, 탄소 추적 |
| devenv | Dev Containers, Codespaces, Nix, 재현 가능한 개발환경 |

## Step 2: 진단 — 원칙 위반 Rule-by-Rule 열거

`infra-kit/references/principle-index.md`에서 해당 카테고리의 원칙 문서 경로를 찾아 읽고, 사용자 설정/설명에 적용되는 원칙 위반 후보를 **개별 row 단위로 모두 열거** 한다 (Gotcha 9 Enumerate-before-Act). 카테고리 단위 묶음 평가 금지.

## Step 3: 처방 — 가이드 제시 (우선순위 · 트레이드오프 · 출처)

각 피드백 항목은 반드시 이 포맷을 따른다:

### [카테고리] 항목 제목

**원칙:** [원칙 이름]
**근거:** [구체적 설명 + 수치 기준]
**권장:** [개선 방향 + 트레이드오프]

> **출처:** [출처명](URL)

# References

- ../../references/principle-index.md
