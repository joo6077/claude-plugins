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
2. **과도한 복잡도 경고** — K8s, 서비스 메시, Terraform/OpenTofu는 프로젝트 규모에 맞을 때만 제안. 소규모 프로젝트에 K8s를 강제하지 마라. **Supply chain 강화(Cosign/SLSA/SBOM), Internal Developer Platform(Backstage/Port), Service Mesh(Istio/Linkerd) 같은 2026 고도화 항목도 규모·위험도·팀 역량이 준비된 경우에만 제안**한다. 1~3인 소규모 팀에 Backstage/IDP 포털을 강요하지 마라.
3. **프로덕션 설정 강제 금지** — 초기 세팅은 개발 환경부터. 프로덕션 최적화는 별도로.
4. **기존 설정 덮어쓰기 금지** — 이미 Dockerfile/CI가 있으면 분석 후 개선점만 제안.

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
| 관측성 | 권장 | 로깅 포맷 + 헬스체크 + 기본 메트릭 |
| 시크릿 | 필수 | .env 패턴 + 시크릿 관리 방침 |

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
