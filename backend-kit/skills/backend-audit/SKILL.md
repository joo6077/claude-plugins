---
name: backend-audit
description: >
  백엔드 코드를 원칙 기준으로 체계적으로 감사한다.
  카테고리별 PASS/FAIL 판정과 근거를 포함한 리포트를 생성한다.
  backend-reviewer 에이전트를 Agent 도구로 호출하여 독립 평가한다.
  "백엔드 감사", "API 검수", "backend audit", "보안 감사" 같은 요청 시 트리거.
  디자인/UI 검사에는 트리거하지 않는다 — design-kit 사용.
argument-hint: "<target-path>"
user-invocable: true
---

# Gotchas

1. **디자인/UI 평가 금지** — UI 디자인 원칙은 평가하지 마라. 백엔드 원칙 준수 여부만 판정한다.
2. **스택 특정 린트 규칙 강제 금지** — ESLint/Pylint 규칙을 강제하지 마라. 아키텍처·보안·성능 원칙만 평가.
3. **N+1 탐지 시 ORM 코드 필수 확인** — 쿼리 패턴을 보지 않고 "N+1일 수 있다"는 추측성 FAIL 금지. 실제 코드에서 루프 내 쿼리를 확인해야 한다.
4. **보안 검사 생략 금지** — 코드가 "내부용"이어도 injection, 시크릿 노출, CORS 설정은 반드시 검사한다.

# Process

## Step 1: 대상 범위 결정

사용자가 지정한 경로를 기준으로 감사 대상을 결정한다:
- 파일 경로 → 해당 파일만
- 디렉토리 경로 → 하위 백엔드 관련 파일 전체
- 미지정 → 최근 변경된 백엔드 파일 (git diff 기준)

## Step 2: backend-reviewer 에이전트 호출

Agent 도구를 사용하여 backend-reviewer 서브에이전트를 생성한다:

- subagent_type: backend-reviewer
- prompt: "다음 파일을 백엔드 원칙 기준으로 평가하라: [대상 파일 목록]"

에이전트가 읽기 전용으로 분석 후 카테고리별 PASS/FAIL 결과를 반환한다.

## Step 3: 리포트 생성

| 카테고리 | 판정 | 근거 |
|----------|------|------|
| Architecture | PASS/FAIL | 구체적 파일:라인 + 원칙 (Hexagonal/Clean/DDD) |
| API Design | PASS/FAIL | 구체적 파일:라인 + 원칙 |
| Database | PASS/FAIL | ... |
| ... | ... | ... |

카테고리 순서는 `references/audit-criteria.md`의 섹션 순서와 일치시킨다 (Architecture → API Design → Database → Auth → Error → Security → Caching → Event-Driven → Testing, 총 9 카테고리).

## Step 4: 최종 판정

- 모든 카테고리 PASS → **APPROVE**
- 1개 이상 FAIL → **REJECT** + 개선 사항 목록

# References

- references/audit-criteria.md — 카테고리별 PASS/FAIL 체크리스트
