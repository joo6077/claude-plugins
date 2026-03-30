---
name: design-audit
description: >
  완성된 UI를 디자인 원칙 기준으로 체계적으로 감사한다.
  카테고리별 PASS/FAIL 판정과 근거를 포함한 리포트를 생성한다.
  design-reviewer 에이전트를 Agent 도구로 호출하여 독립 평가한다.
  "디자인 감사", "UI 검수", "design audit", "디자인 품질 검사" 같은 요청 시 트리거.
  코드 품질/아키텍처 검사에는 트리거하지 않는다 — 각 toolkit의 audit 사용.
argument-hint: "<target-path>"
user-invocable: true
---

# Gotchas

1. **코드 품질 평가 금지** — 아키텍처, 성능, 코드 스타일을 평가하지 마라. 디자인 원칙 준수 여부만 판정한다.
2. **토큰 미사용 FAIL 남발 금지** — 디자인 토큰이 없는 프로젝트에서 "토큰 미사용"으로 FAIL을 남발하지 마라. 토큰 체계가 없으면 design-system 스킬 사용을 권장하는 NOTE로 남겨라.
3. **접근성 생략 금지** — 시각적으로 문제없어 보여도 contrast ratio(WCAG AA 4.5:1), 터치 타겟 크기(최소 44×44pt)는 반드시 검사한다.

# Process

## Step 1: 대상 범위 결정

사용자가 지정한 경로를 기준으로 감사 대상을 결정한다:
- 파일 경로 → 해당 파일만
- 디렉토리 경로 → 하위 UI 관련 파일 전체
- 미지정 → 최근 변경된 UI 파일 (git diff 기준)

## Step 2: design-reviewer 에이전트 호출

Agent 도구를 사용하여 design-reviewer 서브에이전트를 생성한다:

```
Agent 도구 호출:
- subagent_type: design-reviewer
- prompt: "다음 파일을 디자인 원칙 기준으로 평가하라: [대상 파일 목록]"
```

에이전트가 읽기 전용으로 분석 후 카테고리별 PASS/FAIL 결과를 반환한다.

## Step 3: 리포트 포맷팅

에이전트 결과를 templates/audit-report.md 포맷으로 정리한다.

## Step 4: 최종 판정

- 모든 카테고리 PASS → **APPROVE**
- 1개 이상 FAIL → **REJECT** + 개선 사항 목록

REJECT 시 각 FAIL 항목에 대해:
- 파일:라인 위치
- 위반한 원칙 (출처 포함)
- 구체적 개선 방향 (스택 무관 수준)

# References

- `references/audit-criteria.md` — 카테고리별 감사 기준 상세
- `templates/audit-report.md` — 리포트 출력 포맷
