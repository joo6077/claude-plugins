---
name: backend-research
description: >
  백엔드 레퍼런스 소스를 크롤링/분석하여 docs/backend/ 문서를 갱신한다.
  이 레포 개발용 스킬이며, backend-kit 플러그인에 포함되지 않는다.
  "백엔드 리서치", "backend research", "백엔드 문서 갱신" 같은 요청 시 트리거.
argument-hint: "[category]"
user-invocable: true
---

# Gotchas

1. **할루시네이션 출처 금지** — 모든 원칙에 검증된 URL 출처 필수. URL 존재 확인 후 인용.
2. **기존 문서 덮어쓰기 금지** — 기존 docs/backend/ 문서를 읽고, 새 정보만 추가/갱신. 기존 검증된 내용 삭제 금지.
3. **블로그 단독 인용 금지** — 일반 블로그는 공식 문서/RFC와 교차 검증 후에만 인용.
4. **6개월 이상 된 정보 태그** — `[dated: YYYY-MM]` 태그 필수.

# Process

## Step 1: 리서치 범위 결정

사용자가 카테고리를 지정하면 해당 문서만, 미지정이면 전체 docs/backend/ 갱신.

현재 문서 목록:
- fundamentals/: api-design, database, auth, error-handling, testing, security
- patterns/: caching, event-driven
- protocols/: api-lifecycle, graphql, grpc, realtime

## Step 2: 현재 문서 읽기

대상 문서의 현재 원칙·출처·수치를 파악한다.

## Step 3: 외부 리서치

Codex(codex:rescue)에 리서치 태스크를 위임한다:
- 공식 문서 업데이트 확인
- 새 RFC/표준 발행 여부
- 주요 엔지니어링 블로그 신규 사례

## Step 4: 문서 갱신

- 새 원칙 추가 (출처 필수)
- 수치 업데이트 (변경 시 이전 값 주석)
- deprecated 정보 표시
- version bump (patch)
- last_updated 갱신

## Step 5: 변경 커밋

```
research(backend): [카테고리] 문서 갱신
```
