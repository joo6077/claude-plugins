---
name: design-guide
description: >
  개발 중 UI 코드/설명을 받아 관련 디자인 원칙을 참조하여 가이드한다.
  스택 무관 — 원칙과 이유만 설명하고 구현은 해당 toolkit에 위임한다.
  "디자인 가이드", "이 레이아웃 괜찮아?", "UX 조언",
  "디자인 리뷰해줘" (가벼운 리뷰) 같은 요청 시 트리거.
  체계적 전수 검사에는 트리거하지 않는다 — design-audit 사용.
argument-hint: "[file-path or description]"
user-invocable: true
---

# Gotchas

1. **스택별 코드 제시 금지** — 원칙과 이유만 설명하라. Flutter/React/CSS 코드를 직접 제시하지 마라. "WCAG 2.2 SC 2.5.8 AA 기준 24×24 CSS px 이상의 터치 타겟이 필요합니다"는 ✓, "SizedBox(height: 24)"는 ✗. (AA 는 24×24, AAA SC 2.5.5 는 Apple HIG 권장치와 같은 44×44 다 — 44 를 AA 요구로 쓰지 마라.)
2. **주관적 피드백 금지** — "보기 좋다", "깔끔하다" 같은 표현 금지. 반드시 출처가 있는 원칙을 근거로 제시하라. 원칙 없는 의견은 피드백이 아니라 취향이다.
3. **카테고리 과잉 방지** — 한 번에 모든 카테고리를 언급하지 마라. 사용자가 물어본 맥락과 관련된 원칙만 집중해서 답하라. 질문이 타이포그래피에 관한 것이면 컬러 원칙은 언급하지 않는다.
4. **우선순위 없는 피드백 나열 금지** — 피드백은 반드시 Critical / Important / Minor로 분류하라. 기준은 미관이 아니라 사용자 피해 크기: 핵심 task 완료를 막으면 Critical, 반복 혼란/속도 저하면 Important, 국소적 어색함이면 Minor.
5. **이슈 1개 = 코멘트 1개** — 피드백 하나에 여러 문제를 섞지 마라. 각 항목은 `위치`, `깨진 시나리오`, `위반 원칙`, `추천 수정`을 독립적으로 포함해야 개발자가 바로 행동할 수 있다.
6. **해법만 강요하지 마라** — 문제를 먼저 설명하고 제안은 하나의 가능성으로 제시하라. "이렇게 바꿔야 합니다"가 아니라 "이 문제는 X 원칙을 위반합니다. 한 가지 방법은..."으로 말하라.
7. **접근성·에러 케이스 누락 금지** — 시각적 레이아웃에만 집중하다 키보드 접근, 스크린리더, 에러 상태, 빈 상태를 빠뜨리는 실수를 하지 마라. WCAG 위반은 가장 높은 우선순위다.
8. **픽셀 nitpick에 갇히지 마라** — 고영향 이슈가 있는데 픽셀 정렬이나 사소한 간격에 집착하지 마라. 한 세션에서는 상위 1~3개 blocking issue에만 집중하고 나머지는 Minor로 분류한다.
9. **디자인 시스템 우회 지적** — 커스텀 one-off override나 토큰 외 하드코딩된 값이 있으면 반드시 언급하라. 일관성 붕괴는 단기적으로는 Minor처럼 보이지만 장기적으로 유지보수 비용을 높인다.
10. **APCA Lc 참조 안내** — 접근성 대비 가이드 시 WCAG 2.2 AA(4.5:1) 기준을 우선 적용하되, 추가로 APCA Lc 임계값을 informational로 제시하라. 본문 텍스트 Lc 75~90, 비본문 Lc 60 이상. APCA는 폰트 크기+굵기별 차등 대비를 요구하므로 가는 폰트(300w)에 더 높은 Lc가 필요하다. 법적 표준은 WCAG 2.2 AA이며 APCA는 WCAG 3.0 WD 참고용. 출처: research-log §C.
11. **Fluid Typography/Spacing 가이드** — 타이포그래피나 간격 질문 시 고정 크기 외에 `clamp(min, preferred, max)` 기반 fluid scale 옵션을 언급하라. Modular Scale 비율(1.125~1.618)과 Utopia 접근법을 참고로 안내한다. 출처: research-log §E, §F.
12. **Compound Component 패턴 인식** — 컴포넌트 구조 관련 질문 시 Compound Components(Context API로 상태 공유) + Slot Pattern(named slot 분리) 패턴을 인지하고 안내하라. "prop soup" 문제가 보이면 compound 패턴을 제안한다. 출처: research-log §G.
13. **가이드형 스킬도 Process Step 순서 고정 (탐색→진단→처방)** — 본 스킬은 원칙 안내형이지만 적용 시 3-Step 순서를 반드시 따른다. (1) **탐색:** 사용자가 제시한 코드/설명에서 관련 카테고리·디자인 토큰·기존 컴포넌트·출처를 Grep/Read 로 전수 파악 (Step 1). (2) **진단:** 위반 항목을 파일:라인 + 위반 원칙 + 우선순위(Critical/Important/Minor) 로 목록화 (Step 2~3). (3) **처방:** 각 진단에 대해 권장 방향을 "하나의 가능성" 으로 제시하고 근거·출처를 첨부 (Step 3 포맷). 진단 단계를 생략하고 바로 "이렇게 바꾸세요" 로 넘어가면 Gotcha #6 의 "해법만 강요" 안티패턴이 된다. flutter-error · flutter-hooks 가이드 스킬 sibling parity 와 동일 원칙 (Phase 5 원칙 2).
14. **Enumerate-before-Act — 리뷰 대상 전수 나열 우선** — 여러 파일/위젯에 걸친 리뷰 요청(예: "이 디렉토리 UI 다 봐줘")에서는 편집/피드백 전에 대상 파일 목록 + 카테고리별 후보 위반 개수를 **먼저 리스트업** 하고 사용자 승인 후 진단으로 넘어간다. 부분 피드백 → 재지적 → 추가 피드백 루프를 방지한다 (insights-report #1 마찰점 대응).
15. **승인된 시각 결과물이 토큰보다 우선한다 (Visual Source of Truth Precedence)** — "이 색이 토큰과 다르다" 를 무조건 일관성 위반으로 지적하지 마라. Gotcha #9(디자인 시스템 우회 지적)를 적용하기 전에 그 값이 **사용자가 승인한 시안이나 기존 앱에서 실제 사용 중인 값**인지 확인한다. 승인 기록(`.design/approvals/`)이나 기존 테마 파일에 근거가 있으면 그것이 토큰 명세보다 상위 근거이며, 이때 권장 방향은 "토큰에 맞춰 값을 바꿔라" 가 아니라 "이 값을 토큰으로 등록해 체계에 편입하라" 다. 우선순위 표: `../../references/visual-change-protocol.md` §1.
16. **부분 변경 요청에는 그 축만 진단 — 나머지는 보존 대상으로 명시** — 사용자가 특정 시각 속성 하나를 지목해 물으면(보더만·색만·간격만) 진단도 그 축에 한정하고, 같은 요소의 나머지 시각 속성은 **"보존 대상"** 으로 명시하라. "이왕이면 배경도" 식 제안은 Gotcha #3(카테고리 과잉) 위반이며, 실제로 보더 요청에 배경까지 바뀐 재발 사례의 출발점이다. 부분 롤백 요청("색은 맞는데 그라디언트만 이전이 나았다")은 지목된 축만 되돌리도록 진단한다. 상세: `../../references/visual-change-protocol.md` §2.

# Process

## Step 1: 맥락 파악

사용자가 제공한 코드/설명에서 관련 디자인 카테고리를 식별한다:

| 카테고리 | 키워드 |
|----------|--------|
| typography | 글꼴, 크기, 행간, 텍스트, font |
| color | 컬러, 색상, 팔레트, 다크모드 |
| spacing | 간격, 패딩, 마진, 정렬 |
| interaction | 버튼, 탭, 스와이프, 제스처 |
| accessibility | 접근성, a11y, 대비, 터치 타겟, APCA, contrast |
| motion | 애니메이션, 전환, transition, 마이크로인터랙션 |
| visual hierarchy | 위계, 강조, 눈에 띄게, 중요도, 시선 |
| layout & grid | 그리드, 열, 정렬, 레이아웃, 반응형, breakpoint, container query, `@container`, inline-size, self-aware component, cqw, cqi, fluid |
| image | 이미지, 일러스트, 사진, 아이콘 스타일 |
| ethical design | 다크 패턴, 윤리, 동의, 탈퇴, 구독 해지 |
| authenticity | AI스러운, 제네릭, 템플릿, 개성, 진정성, 브랜드 톤 |

## Step 2: 원칙 참조

references/principle-index.md에서 해당 카테고리의 원칙 문서 경로를 찾아 읽는다. 경로는 플러그인 내부 리서치 문서를 가리킨다.

## Step 3: 가이드 제시

각 피드백 항목은 반드시 이 포맷을 따른다:

```text
### [우선순위] [카테고리] 항목 제목

**문제:** [현재 어떤 사용자 시나리오에서 무엇이 잘못됐는지]
**원칙:** [위반된 원칙 이름 — Nielsen Heuristic / WCAG / Gestalt 등]
**출처:** [출처 URL 또는 문서명]
**제안:** [권장 방향 — 하나의 가능성으로 제시]
**근거:** [왜 이 방향이 사용자에게 유리한지]
```

우선순위 기호: `[Critical]` `[Important]` `[Minor]`  
분류 기준: 핵심 task 완료를 막으면 Critical, 반복 혼란/접근성 위반은 Important, 국소적 어색함은 Minor.

## Step 4: 요약

- Critical / Important / Minor 항목 수를 명시한다
- 이번 리뷰 범위에서 다루지 않은 카테고리가 있으면 한 줄로 언급한다
- 필요한 경우 다음 단계로 `design-audit`(전수 감사)를 제안한다

# References

- `references/principle-index.md` — 카테고리별 원칙 문서 인덱스
- `../../references/visual-change-protocol.md` — 시각 우선순위 · 부분 변경 격리 (SSOT)
