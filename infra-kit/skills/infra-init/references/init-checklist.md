# Infra Init Checklist

프로젝트 인프라 초기 세팅 시 참조하는 체크리스트.

설치본 플러그인에는 `docs/infra/` 가 없다 — 아래 상대 경로를 열 수 없으면 앞의 `../` 를 떼고 `https://raw.githubusercontent.com/joo6077/claude-plugins/main/` 뒤에 `docs/infra/...` 를 붙여 읽고, 그래도 못 읽으면 원칙을 지어내지 말고 못 읽었다고 적는다.

## 필수

| 항목 | 참조 문서 | 핵심 |
| ------ | ----------- | ------ |
| Dockerfile | ../../../../docs/infra/platform/container.md | 멀티스테이지, non-root, .dockerignore |
| CI 파이프라인 | ../../../../docs/infra/platform/cicd.md | OIDC, 최소 권한, 캐시/아티팩트 분리 |
| 시크릿 관리 | ../../../../docs/infra/security/tls-secrets.md | .env, vault 참조, git 미포함 |

## 권장

| 항목 | 참조 문서 | 도입 기준 |
| ------ | ----------- | ----------- |
| K8s | ../../../../docs/infra/platform/kubernetes.md | 컨테이너 오케스트레이션 필요 시 |
| IaC | ../../../../docs/infra/platform/iac.md | 클라우드 리소스 관리 필요 시 |
| 배포 전략 | ../../../../docs/infra/operations/deployment-strategies.md | 무중단 배포 필요 시 |
| 관측성 | ../../../../docs/infra/operations/observability.md | 프로덕션 운영 시 |
| 백업/DR | ../../../../docs/infra/operations/backup-dr.md | 데이터 보존 필요 시 |
