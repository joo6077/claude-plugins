---
name: infra-research
description: >
  인프라/DevOps 레퍼런스 소스를 크롤링/분석하여 docs/infra/ 문서를 갱신한다.
  이 레포 개발용 스킬이며, infra-kit 플러그인에 포함되지 않는다.
  "인프라 리서치", "infra research", "인프라 문서 갱신" 같은 요청 시 트리거.
argument-hint: "[category]"
user-invocable: true
---

# Gotchas

1. **할루시네이션 출처 금지** — 모든 원칙에 검증된 URL 출처 필수.
2. **기존 문서 덮어쓰기 금지** — 기존 docs/infra/ 문서를 읽고 새 정보만 추가/갱신.
3. **블로그 단독 인용 금지** — CNCF/공식 문서/RFC와 교차 검증 필수.
4. **벤더 편향 주의** — AWS/GCP/Azure 문서 인용 시 벤더 관점 편향 명시.
5. **frontmatter 갱신 누락 금지** — 문서 내용을 수정하면 `last_updated`와 `version`(patch bump)을 반드시 함께 갱신하라. 내용만 바꾸고 메타데이터를 그대로 두면 다음 카이젠에서 변경 시점을 추적할 수 없다.
6. **보안 권고(CVE) 정보는 날짜 태그 필수** — 보안 관련 원칙이나 수치를 추가할 때 발행 날짜를 `[dated: YYYY-MM]`로 반드시 태그하라. 보안 권고는 빠르게 변경되므로 시점 정보 없이는 가치가 없다.

# Process

## Step 1: 리서치 범위 결정

사용자가 카테고리를 지정하면 해당 문서만, 미지정이면 전체 docs/infra/ 갱신.

현재 문서 목록:
- platform/: container, cicd, kubernetes, iac
- operations/: networking, backup-dr, deployment-strategies, observability, incident-response, cost-optimization, service-mesh
- security/: tls-secrets

## Step 2: 현재 문서 읽기

대상 문서의 현재 원칙·출처·수치를 파악한다.

## Step 3: 외부 리서치

Codex(codex:rescue)에 리서치 태스크를 위임한다:
- CNCF 프로젝트 업데이트
- K8s/Terraform/Docker 버전 변경
- 보안 권고 (CVE, 설정 변경)

## Step 4: 문서 갱신

- 새 원칙 추가 (출처 필수)
- 수치 업데이트
- deprecated 정보 표시
- version bump (patch)
- last_updated 갱신

## Step 5: 변경 커밋

```text
research(infra): [카테고리] 문서 갱신
```
