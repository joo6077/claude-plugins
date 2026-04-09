---
name: design-audit
description: >
  완성된 UI를 디자인 원칙 기준으로 체계적으로 감사한다.
  카테고리별 PASS/FAIL 판정과 근거를 포함한 리포트를 생성한다.
  design-reviewer 에이전트를 Agent 도구로 호출하여 독립 평가한다.
  "디자인 감사", "UI 검수", "design audit", "디자인 품질 검사" 같은 요청 시 트리거.
  코드 품질/아키텍처 검사에는 트리거하지 않는다 — 각 toolkit의 audit 사용.
argument-hint: "<target-path> [quick|deep]"
user-invocable: true
---

# Gotchas

1. **코드 품질 평가 금지** — 아키텍처, 성능, 코드 스타일을 평가하지 마라. 디자인 원칙 준수 여부만 판정한다.
2. **토큰 미사용 FAIL 남발 금지** — 디자인 토큰이 없는 프로젝트에서 "토큰 미사용"으로 FAIL을 남발하지 마라. 토큰 체계가 없으면 design-system 스킬 사용을 권장하는 NOTE로 남겨라.
3. **접근성 카테고리 필수** — 시각적으로 문제없어 보여도 반드시 검사한다: contrast ratio(WCAG AA 4.5:1), 터치 타겟(최소 44×44pt), 포커스 인디케이터, 폼 라벨 연결. 생략하면 REJECT.
4. **AI 안티패턴 검사 포함** — Authenticity 카테고리를 반드시 포함하라. 균일 border-radius, 제네릭 보라-파랑 팔레트, 동일 구조 반복, 목적 없는 장식 효과는 FAIL 사유다.
5. **심각도 분류 필수** — FAIL 항목마다 심각도를 표기한다: `Critical`(접근성·윤리), `Major`(위계·일관성), `Minor`(세부 조정). 심각도 없는 FAIL 리포트는 불완전하다.
6. **주관적 판정 금지** — "보기 좋다", "이 정도면 괜찮다"는 근거가 될 수 없다. 모든 PASS/FAIL은 audit-criteria.md에 정의된 원칙과 수치 기준에 근거해야 한다.
7. **상태/예외 화면 포함** — 기본 화면만 검사하지 마라. 빈 상태, 에러 상태, 로딩 상태, 데이터 과다/과소 상태가 코드에 존재하면 함께 검사한다.
8. **코드 미확인 항목 구분** — 런타임 렌더링, 실제 인터랙션처럼 정적 분석으로 판정 불가한 항목은 PASS/FAIL이 아닌 `[미검증]`으로 표기하고 수동 확인 방법을 안내한다.
9. **휴리스틱-카테고리 혼동 금지** — Nielsen 10 휴리스틱은 평가 관점 프레임이다. 실제 판정은 반드시 audit-criteria.md의 10개 카테고리 기준(Typography, Color, Spacing, Accessibility, Interaction, Motion, Visual Hierarchy, Layout & Grid, Ethical Design, Authenticity)으로 매핑하여 수행한다.

# Process

## Step 1: 대상 범위 및 모드 결정

사용자가 지정한 경로와 모드를 기준으로 감사 범위를 결정한다:
- 파일 경로 → 해당 파일만
- 디렉토리 경로 → 하위 UI 관련 파일 전체
- 미지정 → 최근 변경된 UI 파일 (git diff 기준)

모드:
- `quick` (기본) — 전체 10개 카테고리를 빠르게 검사. Critical/Major FAIL에 집중.
- `deep` — 상태/예외 화면, 반응형 breakpoint, 다크 모드, 접근성 세부 항목까지 전수 검사.

## Step 2: 감사 카테고리 확인

10개 카테고리를 순서대로 검사한다. 각 카테고리의 핵심 체크포인트:

| 카테고리 | 핵심 체크포인트 | 심각도 기준 |
|----------|-----------------|-------------|
| **Typography** | 타이포 스케일 일관성, 행간 1.2~1.6배, 본문 최소 14px(모바일)/16px(웹) | Major |
| **Color** | 텍스트 대비 4.5:1, 시맨틱 토큰 사용, 다크모드 대비 유지 | Critical(대비) / Major(토큰) |
| **Spacing** | 스페이싱 스케일 일관성, 터치 타겟 44×44pt, 그룹 간/내 여백 위계 | Critical(터치) / Major(스케일) |
| **Accessibility** | 색상만으로 상태 전달 금지, 포커스 인디케이터, 폼 라벨, 대체 텍스트 | Critical |
| **Interaction** | 액션 피드백, 로딩 인디케이터, 에러 표시, 취소/되돌리기 경로 | Major |
| **Motion** | 애니메이션 목적성, 듀레이션 200~500ms, prefers-reduced-motion 대응 | Major |
| **Visual Hierarchy** | 제목/본문/캡션 비율 차이, 핵심 콘텐츠 대비 강조, 그룹 여백 분리 | Major |
| **Layout & Grid** | 그리드 정렬, 거터 일관성, 주요 breakpoint 반응형 전략 | Major |
| **Ethical Design** | 다크 패턴 12유형 부재, 동의 명시성, 가입·탈퇴 경로 대칭성 | Critical |
| **Authenticity** | 동일 구조 3회 이상 반복, 제네릭 팔레트, 목적 없는 장식, 범용 카피 | Minor~Major |

## Step 3: design-reviewer 에이전트 호출

Agent 도구를 사용하여 design-reviewer 서브에이전트를 생성한다:

```
Agent 도구 호출:
- subagent_type: design-reviewer
- prompt: "다음 파일을 디자인 원칙 기준으로 [quick|deep] 모드로 평가하라: [대상 파일 목록]"
```

에이전트가 읽기 전용으로 분석 후 카테고리별 PASS/FAIL/미검증 결과를 반환한다.

## Step 4: 리포트 포맷팅

에이전트 결과를 templates/audit-report.md 포맷으로 정리한다.

각 FAIL 항목에 반드시 포함:
- 파일:라인 위치
- 심각도 (`Critical` / `Major` / `Minor`)
- 위반한 원칙 (출처 포함)
- 구체적 개선 방향 (스택 무관 수준)

## Step 5: 최종 판정

- 모든 카테고리 PASS → **APPROVE**
- Critical FAIL 1개 이상 → **REJECT** (즉시)
- Major/Minor FAIL만 있음 → **REJECT** + 우선순위별 개선 목록

REJECT 리포트 구조:
1. Critical FAIL 목록 (즉시 수정 필요)
2. Major FAIL 목록 (다음 스프린트 전 수정)
3. Minor FAIL 목록 (개선 권장)
4. [미검증] 항목 (수동 확인 필요)

# References

- `references/audit-criteria.md` — 카테고리별 감사 기준 상세
- `templates/audit-report.md` — 리포트 출력 포맷
