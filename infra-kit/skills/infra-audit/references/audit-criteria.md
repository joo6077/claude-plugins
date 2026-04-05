# Infra Audit Criteria

## 1. Container
| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 멀티스테이지 | 빌드/런타임 분리 | Docker docs |
| Non-root | USER 지시어 존재 | Docker best practices |
| 헬스체크 | HEALTHCHECK 또는 orchestrator 프로브 | Docker docs |
| 리소스 제한 | CPU/메모리 limit 명시 (프로덕션) | Docker resource constraints |
| 로깅 | stdout/stderr 출력, json-file 무제한 아님 | Docker logging |

## 2. CI/CD
| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| OIDC 인증 | 장기 클라우드 키 대신 OIDC 토큰 | GitHub OIDC docs |
| 최소 권한 | GITHUB_TOKEN/job token 최소 권한 | GitHub security |
| 캐시/아티팩트 분리 | 캐시≠아티팩트 혼용 없음 | GitHub caching docs |
| Runner 보안 | self-hosted는 ephemeral 또는 격리 | GitLab runner security |

## 3. Kubernetes
| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| Requests/Limits | 모든 워크로드에 명시 | K8s resource docs |
| Probe 분리 | liveness/readiness/startup 역할 구분 | K8s probe docs |
| RBAC | namespace-scoped, wildcard 없음 | K8s RBAC practices |
| Pod Security | restricted 또는 baseline 적용 | K8s PSS |

## 4. IaC
| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| Remote state | local state 미사용 (팀 작업 시) | Terraform state docs |
| 모듈 버전 pin | 최신 추종 아닌 고정 버전 | Terraform registry |
| Plan 검토 | CI에서 plan 결과 리뷰 | Terraform CLI |

## 5. Security
| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| TLS | 공개 종단에 TLS 1.2+ | RFC 8446 |
| 시크릿 | git/이미지에 시크릿 미포함 | cert-manager docs |
| 키 로테이션 | 자동 로테이션 설정 존재 | AWS SM docs |

## 6. Backup & DR
| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| RTO/RPO 정의 | 문서화 존재 | AWS prescriptive guidance |
| PITR | 핵심 DB에 PITR 활성 | AWS RDS docs |
| Restore 테스트 | 정기 테스트 기록 | SRE practices |

## 7. Deployment
| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 롤백 절차 | 문서화 또는 자동화 존재 | Argo Rollouts |
| 배포 모니터링 | SLI 기반 자동 롤백 또는 수동 체크 | Argo analysis |

## 8. Observability
| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 구조화 로깅 | JSON/ECS 포맷, trace_id 포함 | ECS docs |
| SLI/SLO | 핵심 서비스에 정의 존재 | SRE workbook |
| 알림 설계 | 증상 기반 paging, 인프라는 티켓 | Grafana alerting |
