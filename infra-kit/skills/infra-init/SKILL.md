---
name: infra-init
description: >
  프로젝트에 인프라 기반(Docker, CI/CD, 배포 설정 등)을 초기 세팅한다.
  기존 인프라가 있으면 리서치 기준과 비교하여 개선점을 제안한다.
  스택 무관 — 원칙만 정의하고, 구체적 설정은 프로젝트 환경에 맞게 적용.
  "인프라 세팅", "Docker 초기화", "CI 파이프라인 만들어줘",
  "infra init" 같은 요청 시 트리거.
  기존 설정 내 단순 수정에는 트리거하지 않는다.
argument-hint: "[project-path]"
user-invocable: true
---

# Gotchas

1. **벤더 강제 금지** — AWS/GCP/Azure 중 하나를 강제하지 마라. 사용자의 기존 환경을 먼저 감지하고 그에 맞춰라.
2. **과도한 복잡도 경고** — K8s, 서비스 메시, Terraform/OpenTofu는 프로젝트 규모에 맞을 때만 제안. 소규모 프로젝트에 K8s를 강제하지 마라. **Supply chain 강화(Cosign v3/SLSA/SBOM/EU CRA), Internal Developer Platform(Backstage/Crossplane), Service Mesh(Cilium eBPF/Istio/Linkerd), FinOps(FOCUS 표준/Shift-Left) 같은 2026 고도화 항목도 규모·위험도·팀 역량이 준비된 경우에만 제안**한다. 1~3인 소규모 팀에 Backstage/IDP 포털이나 Crossplane을 강요하지 마라.
3. **프로덕션 설정 강제 금지** — 초기 세팅은 개발 환경부터. 프로덕션 최적화는 별도로.
4. **기존 설정 덮어쓰기 금지** — 이미 Dockerfile/CI가 있으면 분석 후 개선점만 제안.
5. **시크릿을 예시 값으로 하드코딩하지 마라** — docker-compose.yml이나 CI 파이프라인에 `password: mypassword123` 같은 예시 시크릿을 넣으면 그대로 프로덕션에 배포되는 사고가 발생한다. `.env.example`에 키 이름만 남기고 실제 값은 비워둬야 한다.
6. **healthcheck 없이 depends_on만 쓰지 마라** — `depends_on`은 컨테이너 시작 순서만 보장하고 서비스 준비 상태는 보장하지 않는다. DB가 실제로 커넥션을 받을 준비가 될 때까지 기다리려면 `depends_on.condition: service_healthy` + `healthcheck`를 반드시 함께 설정해야 한다.
7. **CI 파이프라인에 캐시 설정 누락 금지** — Docker layer cache, npm/pip/cargo cache를 설정하지 않으면 매 빌드마다 의존성을 처음부터 다운로드하여 빌드 시간이 수배 늘어난다. 초기 세팅 시 캐시 전략을 함께 구성해야 한다.
8. **멀티스테이지 빌드 미적용 경고** — 빌더와 런타임을 분리하지 않으면 컴파일러, 소스코드, dev-dependencies가 프로덕션 이미지에 포함되어 이미지 크기가 수배 커지고 공격 표면이 늘어난다. Dockerfile 초기 세팅 시 멀티스테이지를 기본으로 구성하라.

# Process

## Step 1: 프로젝트 인프라 감지

- 컨테이너: Dockerfile, docker-compose.yml
- CI/CD: .github/workflows/, .gitlab-ci.yml
- K8s: k8s/, helm/, kustomize/
- IaC: *.tf, pulumi.*, cdk.*
- 배포: ArgoCD, Flux, Vercel, Railway 설정

## Step 2: 카테고리별 세팅

`infra-kit/references/init-checklist.md`를 참조하여 필요한 카테고리를 결정:

| 카테고리 | 필수 여부 | 산출물 |
|----------|-----------|--------|
| Container | 필수 | Dockerfile + .dockerignore + compose |
| CI/CD | 필수 | 파이프라인 설정 (build→test→deploy) |
| 배포 전략 | 권장 | 배포 방식 선택 + 롤백 절차 |
| 관측성 | 권장 | 로깅 포맷 + 헬스체크 + 기본 메트릭 + OTel Collector |
| 시크릿 | 필수 | .env 패턴 + 시크릿 관리 방침 |
| Supply Chain | 권장 | SBOM 생성 + 이미지 서명 + SLSA provenance |
| Cost Optimization | 권장 | 태깅 전략 + Shift-Left 비용 예측 |

## Step 3: 규격 문서 출력

각 카테고리별로:
1. **현재 상태** — 있으면 분석, 없으면 "미설정"
2. **권장 규격** — 리서치 문서 기반 원칙과 수치
3. **개선 사항** — 현재 상태와 권장 규격의 차이점

예시:
```markdown
### Container
**현재:** Dockerfile 존재, 단일 스테이지, root 실행
**권장:** 멀티스테이지, non-root, .dockerignore
**개선:** USER 지시어 추가, 빌드/런타임 분리
```

# References

- ../../references/init-checklist.md
