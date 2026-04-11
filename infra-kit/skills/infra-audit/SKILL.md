---
name: infra-audit
description: >
  인프라 설정(Docker, CI/CD, K8s, Terraform 등)을 원칙 기준으로 체계적으로 감사한다.
  카테고리별 PASS/FAIL 판정과 근거를 포함한 리포트를 생성한다.
  infra-reviewer 에이전트를 Agent 도구로 호출하여 독립 평가한다.
  "인프라 감사", "Docker 검수", "CI 보안 검사", "infra audit" 같은 요청 시 트리거.
  백엔드 코드 품질 검사에는 트리거하지 않는다 — backend-kit 사용.
argument-hint: "<target-path>"
user-invocable: true
---

# Gotchas

1. **백엔드 코드 평가 금지** — 앱 로직은 평가하지 마라. 인프라 설정/구성 원칙만 판정.
2. **벤더 특정 기능 FAIL 금지** — AWS-only 기능이 없다고 FAIL 주지 마라. 범용 원칙만 기준.
3. **보안 검사 생략 금지** — "내부용"이어도 non-root, 시크릿 관리, OIDC, TLS는 반드시 검사.
4. **프로덕션 vs 개발 구분** — 개발용 docker-compose에 리소스 제한 미설정은 FAIL이 아니다. 프로덕션 설정만 엄격 적용.

# Process

## Step 1: 대상 범위 결정

- 파일 경로 → 해당 파일만
- 디렉토리 경로 → 하위 인프라 관련 파일 전체 (Dockerfile, *.yml, *.yaml, *.tf, *.hcl)
- 미지정 → 최근 변경된 인프라 파일 (git diff 기준)

## Step 2: infra-reviewer 에이전트 호출

- subagent_type: infra-reviewer
- prompt: "다음 파일을 인프라 원칙 기준으로 평가하라: [대상 파일 목록]"

## Step 3: 리포트 생성

에이전트 결과를 카테고리별 테이블로 정리한다:

| 카테고리 | 판정 | 근거 |
|----------|------|------|
| Container | PASS/FAIL | 구체적 파일:라인 + 원칙 |
| CI/CD | PASS/FAIL | ... |
| Kubernetes | PASS/FAIL/N/A | ... |
| IaC | PASS/FAIL/N/A | ... |
| Security | PASS/FAIL | ... |
| Supply Chain | PASS/FAIL/N/A | 이미지 서명(Cosign) / SBOM / SLSA provenance |
| Backup & DR | PASS/FAIL/N/A | ... |
| Deployment | PASS/FAIL | ... |
| Observability | PASS/FAIL | ... |

해당 없는 카테고리(K8s 미사용, Cosign/SLSA 도입 전 초기 단계 등)는 N/A로 표시하고 판정에서 제외한다.

## Step 4: 최종 판정

- 모든 카테고리 PASS → **APPROVE**
- 1개 이상 FAIL → **REJECT** + 개선 사항 목록

# References

- ../../references/audit-criteria.md
