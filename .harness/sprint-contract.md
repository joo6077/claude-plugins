# Sprint Contract — Phase 8 Kaizen Research Mode (infra-kit)

Feature: infra-kit 3 스킬 + infra-reviewer 에이전트 + references 2026 최신 K8s/Terraform/DevOps/Supply Chain 트렌드 반영 카이젠
Created: 2026-04-11
Branch: kaizen/2026-04-11-research
Iteration: 1

## Context

Phase 1~7 완료 (commit 4587154 → 465234b). Phase 8은 infra-kit 플러그인의 3개 스킬(infra-init, infra-guide, infra-audit), `agents/infra-reviewer.md`, 그리고 플러그인 수준 references (`infra-kit/references/*.md` — audit-criteria, principle-index, init-checklist)를 2026 K8s/Terraform/OpenTofu/DevOps/Supply Chain 생태계에 맞춰 갱신한다.

데이터 풀 §1 글로벌 feedback에서 infra-kit 스킬/에이전트에 직접 귀속된 REJECT는 없다. §5 validate-plugin 스냅샷 — infra-kit v0.1.0, 3 skills + 1 agent, V1~V7 OK. 회귀 금지 기준선.

외부 리서치 (Codex, 2026-04-11):

- **Kubernetes 1.30~1.33 주요 변경점**: Pod Security Admission은 2026 기본 내장 표준 (PSP 제거, 네임스페이스 라벨 enforce/audit/warn). Sidecar containers는 **v1.33 stable(GA)**. In-place Pod resize는 v1.33 Beta, **v1.35 GA(2025-12-19)**. Ingress는 API frozen — 공식 문서가 Gateway API 사용을 권장. Structured Authentication Config는 v1.30 Beta → v1.34 stable. ValidatingAdmissionPolicy는 v1.30 stable. 1.32에서 `flowcontrol.apiserver.k8s.io/v1beta3` 제거, 1.33에서 Endpoints API 공식 deprecation. ([Sidecar containers stable](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers), [In-place Pod resize GA blog](https://kubernetes.io/blog/2025/12/19/kubernetes-v1-35-in-place-pod-resize-ga/), [Ingress deprecated in favor of Gateway API](https://kubernetes.io/docs/concepts/services-networking/ingress/), [ValidatingAdmissionPolicy stable](https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy), [PSA 문서](https://kubernetes.io/docs/concepts/security/pod-security-admission/), [Endpoints deprecation](https://kubernetes.io/blog/2025/04/24/endpoints-deprecation/))

- **Terraform 1.9~1.11+ 2026**: Stacks는 HCP Terraform 정식 문서 체계에 편입. `terraform test` 프레임워크는 1.7+ mocking으로 실전성 확보. **Ephemeral values / resources (1.10+)**가 핵심 변화 — write-only arguments, `ephemeralasnull`, state/plan 비저장 패턴. Provider-defined functions는 1.8+ 확장 포인트로 정착. ([Terraform Stacks](https://developer.hashicorp.com/terraform/language/stacks), [terraform test](https://developer.hashicorp.com/terraform/language/tests), [Ephemeral values](https://developer.hashicorp.com/terraform/language/ephemeral), [Provider-defined functions](https://developer.hashicorp.com/terraform/plugin/framework/functions))

- **OpenTofu 1.7~1.10 2026**: **State/plan encryption native (1.7+)** 정착. **Provider iteration `for_each` (1.9)** — 멀티리전/멀티어카운트 provider duplication 해결. 1.10은 OCI registry, native S3 state locking, OTel tracing (experimental). Terraform 대비 호환성은 "v1 compatibility promises" — 넓게 유지하되 신규 OpenTofu 기능 도입 시 drift 존재. ([State encryption](https://opentofu.org/docs/v1.11/language/state/encryption/), [Provider for_each](https://opentofu.org/docs/language/meta-arguments/for_each/), [OpenTofu 1.10 what's new](https://opentofu.org/docs/v1.10/intro/whats-new/), [v1 compatibility promises](https://opentofu.org/docs/language/v1-compatibility-promises/), [Migration guide](https://opentofu.org/docs/intro/migration/))

- **Platform Engineering / IDP 2026**: 공통 패턴 = golden path + self-service + scorecards/catalog. Backstage는 scaffolder/templates, Port/Cortex는 scorecards. 2026 IDP 설계 원칙은 "포털 자체"보다 **개발자 흐름 자동화**가 핵심 — golden path 템플릿 + score 기반 표준 준수 측정. ([Backstage software templates](https://backstage.io/docs/features/software-templates), [Port scorecards](https://docs.port.io/scorecards/overview/), [Cortex scorecards](https://docs.cortex.io/scorecards), [Humanitec platform engineering](https://humanitec.com/platform-engineering))

- **GitOps 2026 — Argo CD 3.x / Flux 2.6**: Argo CD는 2026 초 기준 이미 **3.x 라인**. Flux **v2.6 GA (2025-05-29)** — OCI artifacts GA, object-level workload identity. Argo Rollouts 1.8.x가 canary/blue-green/analysis 실운영 축. ([Argo CD releases](https://github.com/argoproj/argo-cd/releases), [Flux 2.6 release](https://fluxcd.io/blog/2025/05/flux-v2.6.0/), [Argo Rollouts](https://argoproj.github.io/argo-rollouts/))

- **Container Security 2026 — Supply Chain**: Cosign + in-toto attestation이 2026 이미지 서명 기본축 — `verify-attestation`까지 포함한 attest/verify 워크플로우 기본. **SLSA provenance**는 L3/L4 기준점. Distroless는 유효하나 **Chainguard Images**가 "distroless + provenance + 업데이트 체계"로 운영 친화적. **SBOM 툴체인 = Trivy + Syft/Grype + CycloneDX/SPDX**. **eBPF runtime security (Falco/Tetragon)**는 정적 스캔 보완 레이어. ([Cosign verifying attestation](https://docs.sigstore.dev/cosign/verifying/attestation/), [SLSA provenance](https://slsa.dev/provenance), [Chainguard Images](https://edu.chainguard.dev/chainguard/chainguard-images/overview/), [Trivy SBOM](https://trivy.dev/docs/dev/guide/supply-chain/sbom/), [Syft](https://github.com/anchore/syft), [Falco](https://falco.org/), [Tetragon](https://tetragon.io/))

- **Observability 2026 — OpenTelemetry**: **OTel Logs는 2025년 안정화 완료** (Bridge API/SDK/Protocol stable). **Semantic Conventions는 1.x 릴리스 체계 + 일부 도메인 안정화 진행 중**. **Grafana LGTM (Loki/Mimir/Tempo/Pyroscope)**이 OSS 조합 축. **Beyla + OTel eBPF OBI**로 zero-code instrumentation. **OTel Profiles는 2026-03-26 public alpha** — continuous profiling 표준화 진행형. ([OTel status summary](https://opentelemetry.io/docs/specs/status/), [OTel Logs SDK](https://opentelemetry.io/docs/specs/otel/logs/sdk/), [OTel semantic conventions](https://opentelemetry.io/docs/specs/semconv/), [Grafana LGTM OTel](https://grafana.com/blog/otel-lgtm/), [OTel OBI zero-code](https://opentelemetry.io/docs/zero-code/obi/), [OTel Profiles pprof](https://opentelemetry.io/docs/specs/otel/profiles/pprof/))

- **CI/CD 2026 보안 — SLSA / OIDC / Trusted Publishers**: SLSA provenance가 2026 CI/CD 기본 산출물. GitHub Actions OIDC는 secretless CI 핵심 — short-lived federation. Reusable workflows + OIDC로 배포 표준화. Environment protection은 PyPI Trusted Publishers / OIDC와 같이 사용 시 의미 커짐. **PyPI Trusted Publishers**는 2026 매우 성숙 (id-token: write + project/workflow binding). ([SLSA spec](https://slsa.dev/spec), [GitHub Actions OIDC](https://docs.github.com/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect), [Reusable workflows + OIDC](https://docs.github.com/en/actions/how-tos/security-for-github-actions/security-hardening-your-deployments/using-openid-connect-with-reusable-workflows), [PyPI Trusted Publishers](https://docs.pypi.org/trusted-publishers/))

## Scope

### 수정 대상

- `infra-kit/skills/infra-init/SKILL.md`
- `infra-kit/skills/infra-guide/SKILL.md`
- `infra-kit/skills/infra-audit/SKILL.md`
- `infra-kit/agents/infra-reviewer.md`
- `infra-kit/references/audit-criteria.md`
- `infra-kit/references/principle-index.md`
- `infra-kit/references/init-checklist.md`

### 수정 금지 (Phase 1~7 파일 / 범위 외)

- `harness/**`, `flutter-toolkit/**`, `design-kit/**`, `backend-kit/**` (Phase 1~7)
- `docs/infra/**` — 범위 외 (docs 갱신은 `/infra-research` 스킬 영역)
- `infra-kit/.claude-plugin/plugin.json` — 버전 bump는 Final Phase에서
- `.harness/` 파일 (`.harness/sprint-contract.md` 외)
- `.harness/.meta/kaizen-data-pool.md` 수정 금지
- `infra-kit/skills/*/references/**` — 플러그인 루트의 `infra-kit/references/` 만 사용 (skills 하위 references 디렉토리는 비어 있음을 유지)

## Goal

2026 K8s(Sidecar GA / Gateway API / PSA restricted / VAP stable) + Terraform 1.10+ 및 OpenTofu 1.7+ (ephemeral, state encryption, provider for_each) + GitOps(Argo CD 3 / Flux 2.6 / Argo Rollouts) + Supply Chain(Cosign/SLSA/SBOM/Chainguard) + Observability(OTel Logs stable / Profiles alpha / LGTM / eBPF) + CI/CD(OIDC secretless / Trusted Publishers)를 infra-kit 3 스킬 + infra-reviewer + 3 references에 반영한다. validate-plugin 7 OK / bare fence 0건 / markdownlint 주요 규칙을 유지해야 한다.

## 완료 조건

### SC: Supply Chain 카테고리 신설

- [ ] **SC-01**: `infra-kit/references/principle-index.md` 카테고리 표에 `supply-chain` 행 1개 추가 — 키워드 최소 3개 (`SBOM`, `Cosign`, `SLSA`, `서명`, `attestation`, `공급망` 중 3개 이상) + 문서 경로는 기존 `docs/infra/platform/container.md` 또는 `docs/infra/platform/cicd.md` 중 1개 연결(신규 docs 파일 금지). 기존 12개 카테고리는 유지 — 총 13개.
- [ ] **SC-02**: `infra-guide/SKILL.md` Step 1 카테고리 표에 `supply-chain` 행 1개 추가 — 키워드 SC-01과 정합(최소 3개 공통). 기존 12개 카테고리 유지 + supply-chain 포함 13개.
- [ ] **SC-03**: `infra-kit/references/audit-criteria.md`에 `## Supply Chain` 섹션 신설 — 최소 3개 기준 표 항목 (예: "이미지 서명(Cosign)", "SBOM 생성(Syft/Trivy CycloneDX/SPDX)", "SLSA provenance"). 각 항목에 PASS / FAIL 조건 명시. 참조 URL 최소 2개 (sigstore.dev, slsa.dev, trivy.dev 중 2개).
- [ ] **SC-04**: `infra-kit/agents/infra-reviewer.md` 평가 카테고리 목록에 `Supply Chain` 카테고리 1개 추가. 기존 8개 카테고리 뒤(또는 Security 바로 뒤)에 위치. 총 9개 카테고리.
- [ ] **SC-05**: `infra-audit/SKILL.md` Step 3 리포트 테이블 예시에 `Supply Chain` 행 1개 추가 (PASS/FAIL/N/A 표기 예시 포함).
- [ ] **SC-06**: `infra-kit/references/init-checklist.md`에 Supply Chain 카테고리 섹션 1개 신설 또는 CI/CD 섹션 체크리스트에 **서명(Cosign)**, **SBOM(Syft/Trivy CycloneDX/SPDX)**, **SLSA provenance** 3개 체크 항목 추가. 출처 URL 최소 1개 (sigstore.dev 또는 slsa.dev).

### PE: Platform Engineering (IDP) 카테고리 신설

- [ ] **PE-01**: `infra-kit/references/principle-index.md`에 `platform-engineering` 카테고리 행 1개 추가 — 키워드 최소 3개 (`IDP`, `Backstage`, `golden path`, `self-service`, `scorecard`, `Port`, `Humanitec` 중 3개 이상). 문서 경로는 기존 `docs/infra/platform/cicd.md` 또는 `docs/infra/operations/deployment-strategies.md` 중 근접한 것 연결.
- [ ] **PE-02**: `infra-guide/SKILL.md` Step 1 카테고리 표에 `platform-engineering` 행 1개 추가 — 키워드 PE-01과 정합(최소 3개 공통).

### K8: Kubernetes 2026 반영

- [ ] **K8-01**: `infra-kit/references/audit-criteria.md` `## Kubernetes` 표에 **Pod Security Admission(restricted 우선, baseline 허용)** 기준 1줄 추가. 출처 URL 1개 (kubernetes.io/docs/concepts/security/pod-security-admission/).
- [ ] **K8-02**: `infra-kit/references/audit-criteria.md` Kubernetes 표 또는 networking 관련 항목에 **Gateway API 권장 (Ingress frozen)** 기준 1줄 추가. 출처 URL 1개 (kubernetes.io/docs/concepts/services-networking/ingress/ 또는 Gateway API 공식).
- [ ] **K8-03**: `infra-kit/references/init-checklist.md` Kubernetes(선택) 섹션에 **Gateway API 사용 권장 (신규 프로젝트)**, **PodSecurity 라벨 설정(enforce/audit/warn)** 2개 체크 항목 추가.
- [ ] **K8-04**: `infra-kit/references/init-checklist.md` Kubernetes 섹션에 **Sidecar containers(v1.33 GA) 공식 native sidecar 사용 권장 — 레거시 multi-container + shared termination 패턴 대체** 1줄 주석 추가. 출처 URL 1개 (kubernetes.io/docs/concepts/workloads/pods/sidecar-containers).

### IA: IaC (Terraform 1.10+ / OpenTofu 1.7+) 반영

- [ ] **IA-01**: `infra-kit/references/audit-criteria.md` `## IaC` 표에 **Ephemeral values / write-only arguments (Terraform 1.10+ / OpenTofu)** 기준 1줄 추가 또는 기존 "시크릿 제외" 행을 확장. 출처 URL 1개 (developer.hashicorp.com/terraform/language/ephemeral).
- [ ] **IA-02**: `infra-kit/references/audit-criteria.md` IaC 표에 **State encryption (OpenTofu 1.7+ native 또는 backend 암호화)** 기준 1줄 추가. 출처 URL 1개 (opentofu.org state encryption 또는 Terraform backend 암호화).
- [ ] **IA-03**: `infra-kit/references/audit-criteria.md` IaC 표에 **`terraform test` / OpenTofu test 프레임워크 도입** 기준 1줄 추가. 출처 URL 1개 (developer.hashicorp.com/terraform/language/tests).
- [ ] **IA-04**: `infra-kit/references/init-checklist.md` IaC 섹션에 **OpenTofu 대안 명시 (v1.7+ state encryption native, v1.9+ provider for_each)** 1줄 주석 추가. 출처 URL 1개 (opentofu.org).
- [ ] **IA-05**: `infra-guide/SKILL.md` Step 1 카테고리 표 `iac` 키워드에 `OpenTofu` 또는 `ephemeral` 1개 추가 (기존 키워드 유지).

### CD: CI/CD 2026 (OIDC / SLSA / Trusted Publishers)

- [ ] **CD-01**: `infra-kit/references/audit-criteria.md` `## CI/CD` 표에 **SLSA provenance 생성/검증** 기준 1줄 추가. 출처 URL 1개 (slsa.dev/provenance 또는 slsa.dev/spec).
- [ ] **CD-02**: `infra-kit/references/audit-criteria.md` CI/CD 표에 **Secretless publish — PyPI Trusted Publishers / npm provenance / reusable workflow + OIDC** 기준 1줄 추가 또는 기존 `OIDC 인증` 행을 확장. 출처 URL 1개 (docs.pypi.org/trusted-publishers 또는 GitHub reusable workflows + OIDC).
- [ ] **CD-03**: `infra-kit/references/init-checklist.md` CI/CD 섹션에 **SLSA provenance**, **Trusted Publishers (해당 시)** 2개 항목 추가 (SC-06과 중복 허용 — 한 체크리스트에 SBOM과 함께 그룹화해도 무방).

### GO: GitOps 2026 (Argo CD 3 / Flux 2.6 / Argo Rollouts)

- [ ] **GO-01**: `infra-kit/references/principle-index.md` `deployment-strategies` 행 키워드에 **Flux** 1개 추가 (기존 키워드 유지). `ArgoCD`는 기존 유지.
- [ ] **GO-02**: `infra-kit/references/audit-criteria.md` `## Deployment` 표에 **GitOps source-of-truth (ArgoCD/Flux) — 클러스터 직접 변경 금지** 기준 1줄 추가. 출처 URL 1개 (fluxcd.io 또는 argoproj.github.io).

### OB: Observability 2026 (OTel Logs stable / eBPF)

- [ ] **OB-01**: `infra-kit/references/audit-criteria.md` `## Observability` 표에 **OpenTelemetry (Logs stable 2025, semantic conventions 1.x)** 기준 1줄 추가 또는 기존 "분산 트레이싱" 행을 OTel 3 신호 통합으로 확장. 출처 URL 1개 (opentelemetry.io/docs/specs/status/ 또는 semconv).
- [ ] **OB-02**: `infra-kit/references/init-checklist.md` 관측성 섹션에 **OpenTelemetry Collector / OTLP export** 1줄 추가. 출처 URL 1개 (opentelemetry.io).

### RV: infra-reviewer 에이전트 동기화

- [ ] **RV-01**: `infra-kit/agents/infra-reviewer.md` 핵심 규칙에 "audit-criteria.md가 유일한 진실원천"이라는 기존 문장 유지 + SC-04에서 추가된 Supply Chain 카테고리가 평가 카테고리 목록에 반영됨.
- [ ] **RV-02**: `infra-kit/agents/infra-reviewer.md` 출력 포맷 테이블은 기존 일반 컬럼(카테고리/판정/파일:라인/근거/출처)을 유지 — Supply Chain도 자연스럽게 표현 가능. 추가 수정 불필요 (self-audit 명시).

### GQ: Gotcha — 과복잡도 경고 / 벤더 중립

- [ ] **GQ-01**: `infra-init/SKILL.md` Gotcha #2(과도한 복잡도 경고)에 **"Supply chain(Cosign/SLSA) / IDP(Backstage) / Service Mesh / Istio는 규모·위험도에 맞을 때만 제안"** 맥락 1문장 추가. 기존 K8s/Terraform 문구 유지.
- [ ] **GQ-02**: `infra-guide/SKILL.md` Gotcha #1(벤더 중립)을 유지하되, 새로 추가된 `supply-chain`/`platform-engineering` 카테고리에서도 특정 벤더(Chainguard, Backstage 등)를 강제하지 말라는 1문장 추가. 기존 AWS/GCP/Azure 문구 유지.

### I: 인프라 / 품질 게이트

- [ ] **I-01**: `python3 scripts/validate-plugin.py infra-kit` → V1~V7 전부 OK.
- [ ] **I-02**: `python3 scripts/validate-plugin.py` (전체 7 킷) → Total 7 OK, Exit 0. 회귀 금지.
- [ ] **I-03**: `python scripts/sync-docs.py --check-only` → infra-kit 영역 "모두 최신 상태" 또는 sync 필요 없음. 필요 시 sync 후 재실행하여 통과.
- [ ] **I-04**: bare code fence 0건 (V6 code-fence OK로 검증) — 새로 추가하는 모든 fenced block은 반드시 언어 힌트 명시 (`bash`, `markdown`, `text`, `yaml` 등).
- [ ] **I-05**: 변경된 파일들에 MD031/MD032/MD060/MD028/MD034/MD033 markdownlint 규칙 위반 0건 — 수정 영역 주변 context 기준.
- [ ] **I-06**: git working tree modified 파일이 위 Scope 외로 벗어나지 않는다. `scripts/__pycache__/`, `.harness/sprint-contract.md` 는 허용. `.harness/.meta/kaizen-data-pool.md` 수정 금지.
- [ ] **I-07**: git commit 메시지 prefix `kaizen(phase8-research):` 형식 + 한국어 본문. commit hash 리포트에 기재.
- [ ] **I-08**: 브랜치 유지 — `kaizen/2026-04-11-research`, push 금지.

### TR: Trace / 출처 / 2026 트렌드

- [ ] **TR-01**: 새로 추가된 출처 URL 최소 **8개 이상** 순증 (Kubernetes 2+ / Terraform 1 / OpenTofu 1 / Supply Chain 2 / IDP 1 / Observability 1 이상 mix). 중복 URL은 1회만 카운트, sprint-contract.md 외 실제 변경 파일 내 인용 기준.
- [ ] **TR-02**: `infra-kit` 변경 파일 내에 해당 출처 URL이 실제 인용되어 있어야 한다 (단순 sprint-contract.md 인용은 카운트하지 않는다).
- [ ] **TR-03**: 리포트에 리서치 출처 URL 목록 (최소 8개) 명시.

## Rollback

Self-audit FAIL 3회 연속 또는 validate-plugin 회귀 발생 시 `git checkout -- infra-kit/` 로 롤백. commit 전이면 working tree만 버리면 된다.

## Notes

- `docs/infra/**`는 이번 Phase 범위 외 — 해당 갱신은 별도 `/infra-research` Phase 책임. 이번 Phase는 스킬/에이전트/references 레벨 갱신만.
- SC-01, PE-01의 문서 경로는 기존 `docs/infra/**`의 근접 파일로 연결 (신규 docs 파일 생성 금지). 향후 `/infra-research`에서 신규 docs(`platform/supply-chain.md`, `operations/platform-engineering.md`)가 생성되면 후속 Phase에서 경로를 교체한다.
- `infra-kit/skills/*/references/` 하위 디렉토리는 비어 있으므로 건드리지 않는다 — 플러그인 루트의 `infra-kit/references/` 만 SSOT로 사용한다.
- 카테고리가 12→13으로 증가하는 변경은 infra-guide Step 1의 카테고리 표와 principle-index.md 양쪽에 반드시 sync 되어야 한다. 하나만 변경하면 REJECT.
- infra-init Gotcha #2 수정은 "추가 경고" 한 문장만 넣는 최소 침습 변경 — 기존 경고를 삭제하지 않는다.
