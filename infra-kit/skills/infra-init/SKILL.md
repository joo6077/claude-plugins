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
9. **Enumerate-before-Act (skill-design-guide §5.5 대응)** — 기존 프로젝트의 인프라 기반을 세팅할 때 "감지 → 필수/권장 카테고리 → 현재/권장/개선" 을 rule-by-rule 로 **한 번에 모두 나열** 후 사용자 승인. 카테고리 하나 세팅하고 사용자 답변 기다리는 round-trip 금지 (/insights 마찰점 #1 재발 방지).
10. **OIDC + SHA 핀닝 동시 명시 (Phase 8 리서치)** — CI 세팅 시 OIDC 인증(장기 키 제거) 과 서드파티 Actions SHA 핀닝을 **둘 다** 기본 권장에 포함하라. 둘 중 하나만 제안하면 공급망 공격 창구가 남는다. 출처: [GitHub Actions OIDC](https://docs.github.com/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect) · [SHA Pinning Policy](https://github.blog/changelog/2025-08-15-github-actions-policy-now-supports-blocking-and-sha-pinning-actions/).
11. **IaC 시크릿은 Ephemeral 또는 참조만 (Phase 8 리서치)** — Terraform/OpenTofu 세팅 시 시크릿을 state 에 평문 저장하지 말고 `ephemeral` 블록(Terraform 1.10+) 또는 write-only 인수, OpenTofu 1.7+ native state encryption 을 권장 규격에 포함한다. `sensitive` 마킹만으로는 state 평문 저장이 유지된다. 출처: [Terraform ephemeral](https://developer.hashicorp.com/terraform/language/ephemeral) · [OpenTofu state encryption](https://opentofu.org/docs/v1.11/language/state/encryption/).

12. **반복 셸 명령은 YAML 인라인이 아니라 스크립트/Makefile 로 코드화하라** — CI 스텝에 긴 인라인 셸을 박으면 로컬에서 그대로 재현할 수 없고, 파이프 실패·따옴표 파손·exit code 유실이 워크플로 안에 숨는다. 초기 세팅 시 `Makefile` 또는 `scripts/*.sh` 타겟으로 빼고 워크플로는 그 타겟만 호출하게 하라. 코드화할 때 아래 둘은 **함께** 넣어야 의미가 있다.

    - 스크립트 첫 줄에 `set -euo pipefail` — 파이프는 마지막 명령의 exit code 만 평가한다. 출처: [Docker best practices](https://docs.docker.com/build/building/best-practices/) (`RUN` 파이프에 `set -o pipefail &&` 선행 권고).
    - 워크플로 `run` 스텝에 `shell: bash` **명시** — 비-Windows 기본 셸은 `bash -e {0}` 라 pipefail 이 없고, 명시했을 때만 `bash --noprofile --norc -eo pipefail {0}` 가 된다. 출처: [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).

    트레이드오프: 파일이 늘고 CI YAML 이 얇아진다. 대신 같은 검증을 로컬에서 한 명령으로 재현할 수 있다.

13. **Dependabot 은 탐지된 생태계만 등록하라 (Phase 8 리서치)** — `.github/dependabot.yml` 을 만들 때 존재하지 않는 생태계를 넣으면 Dependabot 이 매 실행마다 실패하고, 그 실패가 일상화되면 진짜 알림도 무시된다. `github-actions` `/` 는 워크플로가 있으면 항상 넣고, 나머지는 **Step 1 탐색에서 실제 lockfile/manifest 를 확인한 뒤에만** 추가한다 (`package-lock.json`/`yarn.lock` → `npm`, `Dockerfile` → `docker`, `requirements.txt`/`poetry.lock` → `pip`, `Cargo.lock` → `cargo`, `go.sum` → `gomod`). 로컬 액션과 `docker://` 참조는 업데이트 대상에서 제한이 있다. 출처: [Dependabot options reference](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference).

14. **핀닝 정책을 조용히 정하지 마라 (Phase 8 리서치)** — 원격 `uses:` 는 40 자 커밋 SHA 고정이 기본이고, 여기에는 `jobs.<id>.steps[].uses`(스텝 액션)뿐 아니라 `jobs.<id>.uses`(재사용 워크플로 호출)도 포함된다. GitHub 공식 지침은 **full-length commit SHA 만 immutable release 로 취급**하며 태그는 이동·삭제 위험이 있다고 본다. GitHub-owned `actions/*` 를 예외로 둘지는 **팀이 명시적으로 결정하고 기록할 정책 질문**이다 — 검사 스크립트에 기본 면제로 숨기면 미핀닝을 통째로 놓친다. 트레이드오프: SHA 핀닝은 업데이트 운영성을 떨어뜨리므로 `@<sha> # v5.0.0` 처럼 같은 줄 주석으로 원 태그를 남기고 Dependabot 에 갱신을 맡긴다. 출처: [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use).

15. **게이트 스텝은 결과 상태를 구분해 exit code 로 전파하게 세팅하라 (Phase 8 리서치)** — CI 검증 스텝이 "위반 0" 과 "검사 못 함" 을 같은 exit 0 으로 내면 그 게이트는 없는 것보다 나쁘다. 초기 세팅부터 `PASS` / `VIOLATION` / `SKIP_NO_TARGET` / `[미검증] TOOL_OR_ENV_MISSING` / `EXECUTION_ERROR` 5 상태를 쓰고 exit 를 매핑한다. 상태·exit 정의는 `../../references/gate-result-taxonomy.md` 가 SSOT 이며 여기서 재정의하지 않는다.

# Process (3-Step · 탐색 → 진단 → 처방)

## Step 1: 탐색 — 프로젝트 인프라 감지

- 컨테이너: Dockerfile, docker-compose.yml
- CI/CD: .github/workflows/, .gitlab-ci.yml
- K8s: k8s/, helm/, kustomize/
- IaC: *.tf, pulumi.*, cdk.*
- 배포: ArgoCD, Flux, Vercel, Railway 설정

## Step 2: 진단 — 필수/권장 카테고리 Rule-by-Rule 열거

`infra-kit/references/init-checklist.md`를 참조하여 필요한 카테고리를 rule 단위로 한 번에 나열한다 (Gotcha 9). 현재 상태와 리서치 기준의 차이를 한 번에 열거.

| 카테고리 | 필수 여부 | 산출물 |
|----------|-----------|--------|
| Container | 필수 | Dockerfile + .dockerignore + compose (멀티스테이지 + non-root + healthcheck) |
| CI/CD | 필수 | 파이프라인 설정 (build→test→deploy) + OIDC + 원격 `uses:` SHA 핀닝 (Gotcha 10·14) + `.github/dependabot.yml` (Gotcha 13) + 게이트 상태 taxonomy (Gotcha 15) |
| 배포 전략 | 권장 | 배포 방식 선택 + 롤백 절차 + GitOps(Argo CD 3.x / Flux v2.8+) |
| 관측성 | 권장 | 로깅 포맷 + 헬스체크 + 기본 메트릭 + OTel Collector |
| 시크릿 | 필수 | .env 패턴 + Ephemeral values / Vault 참조 (Gotcha 11) |
| Supply Chain | 권장 | SBOM 생성 + Cosign v3 이미지 서명 + SLSA provenance |
| Cost Optimization | 권장 | 태깅 전략 + Shift-Left 비용 예측 |

## Step 3: 처방 — 규격 문서 출력

각 카테고리별로 아래 포맷으로 출력한다 (현재 상태 / 권장 규격 / 개선 사항):

1. **현재 상태** — 있으면 분석, 없으면 "미설정"
2. **권장 규격** — 리서치 문서 기반 원칙 + 수치 + 출처 URL
3. **개선 사항** — 현재 상태와 권장 규격의 차이점 + 우선순위 + 트레이드오프

예시:

### Container

**현재:** `Dockerfile:1-20` 존재, 단일 스테이지, `USER` 미지정 (root 실행), `FROM node:latest`
**권장:** 멀티스테이지(`FROM node:22-alpine AS builder` → `FROM node:22-alpine`) + `USER 1001:1001` + `.dockerignore` + `HEALTHCHECK` (출처: [Docker best practices](https://docs.docker.com/build/building/best-practices/))
**개선:**
- P0: `latest` 태그 → 구체 버전 태그 (재현성)
- P0: `USER` 지시어 추가 (컨테이너 탈출 방지)
- P1: 멀티스테이지 분리 (이미지 크기 감소)
- 트레이드오프: 멀티스테이지는 빌드 시간 약간 증가, 이미지 크기 수배 감소

### CI/CD

**현재:** `.github/workflows/deploy.yml:1-50` 존재, `AWS_ACCESS_KEY_ID` 시크릿 사용, `actions/checkout@v4` 태그 참조, `.github/dependabot.yml` 부재
**권장:** OIDC federation(`id-token: write` + `aws-actions/configure-aws-credentials`) + 원격 `uses:` SHA 핀닝 + Dependabot(탐지된 생태계만) + 의존성 캐시 (출처: [GitHub Actions OIDC](https://docs.github.com/en/actions/concepts/security/openid-connect) · [secure use](https://docs.github.com/en/actions/reference/security/secure-use) · [Dependabot options](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference))
**개선:**
- P0: 장기 AWS 키 제거 → OIDC 교체
- P0: 원격 액션 SHA 고정 (`@v4` → `@<40-char sha> # v4`). `jobs.<id>.uses` 재사용 워크플로도 포함. `actions/*` 면제 여부는 팀이 결정해 기록
- P1: `.github/dependabot.yml` 에 `github-actions` `/` 추가 (나머지 생태계는 lockfile 확인 후)
- P1: Docker layer cache + 언어 런타임 캐시 추가
- 트레이드오프: OIDC 초기 IAM Role 설정 필요 (키 회전 부담 제거 대가). SHA 핀닝은 업데이트 운영성이 떨어지므로 Dependabot 과 함께 도입해야 실효가 있다

### IaC

**현재:** 미설정 (인프라 리소스 수동 콘솔 관리)
**권장:** Terraform 1.10+ 또는 OpenTofu 1.11+ + remote backend(S3+SSE-KMS 또는 OpenTofu native encryption) + `terraform test` + `ephemeral` 블록 시크릿 (출처: [Terraform ephemeral](https://developer.hashicorp.com/terraform/language/ephemeral))
**개선:**
- P1: IaC 도입 여부 먼저 팀 합의 (수동 운영이 더 단순할 수 있음)
- P0 (도입 시): state 파일 평문 시크릿 금지 (`ephemeral` + KMS 암호화)
- 트레이드오프: IaC 학습 비용 vs 드리프트 방지/PR 리뷰 가능성

# References

- ../../references/init-checklist.md
- ../../references/gate-result-taxonomy.md — 게이트 결과 상태 5 종 · exit 매핑 (SSOT)
