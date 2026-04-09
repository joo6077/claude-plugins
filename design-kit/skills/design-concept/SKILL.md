---
name: design-concept
description: >
  프로젝트의 디자인 방향성(무드, 컬러 방향, 타이포 방향, UI 패턴)을 정의하고
  비주얼 무드보드로 시각화한다. design-system의 상위 레이어이자 입력값 역할.
  사용자 설명, 레퍼런스 URL, 자체 웹 리서치를 조합하여 컨셉을 도출한다.
  "디자인 컨셉", "무드보드", "컨셉 잡아줘", "design concept",
  "디자인 방향", "톤앤매너", "무드 정의" 같은 요청 시 트리거.
  기존 디자인 토큰 값 수정에는 트리거하지 않는다 — design-system 사용.
  기존 UI 코드 리뷰에는 트리거하지 않는다 — design-guide 사용.
argument-hint: "[keywords, reference-url, or both]"
user-invocable: true
---

# Gotchas

1. **스택별 코드 생성 금지** — 이 스킬은 방향과 원칙만 정의한다. Flutter/React/CSS 코드를 직접 생성하지 마라. HTML 무드보드는 시각화 목적이므로 예외.
2. **근거 없는 제안 금지** — "이 컬러가 좋을 것 같습니다" ✗. 반드시 리서치 문서 또는 웹 리서치 출처를 명시하라. `docs/design/` 리서치 문서와 웹 리서치 결과를 근거로 제안한다.
3. **컬러 값 직접 지정 금지** — 컨셉 단계에서 hex 값을 확정하지 마라. "따뜻한 뉴트럴 계열, 높은 채도의 포인트 컬러" 같은 방향만 제시한다. 구체적 값은 design-system 스킬에서 정한다.
4. **기존 컨셉 무시 금지** — `.design/concept.md`가 이미 존재하면 반드시 로드하여 수정/확장 모드로 진입하라. 기존 내용을 무시하고 새로 만들면 이전 합의가 사라진다.
5. **무드 키워드를 시각 속성으로 번역하지 않으면 의미 없음** — "미니멀", "따뜻함" 같은 키워드는 반드시 `color / type / image / shape / layout / motion` 각각에 대한 구체적 방향으로 번역해야 한다. 키워드만 나열하고 시각 규칙이 없으면 팀마다 다르게 해석되어 무드보드가 장식으로 끝난다.
6. **컨셉 시안은 컬러 교체가 아니라 레이아웃 차별화** — 여러 컨셉 안을 제시할 때 색상만 바꾸는 것은 "스타일 옵션"이지 "컨셉 옵션"이 아니다. hero 구조, 그리드, 콘텐츠 밀도, 타이포 위계, 이미지 비중 중 최소 2개 이상이 달라야 검토 가치가 생긴다.
7. **컬러 방향은 역할 기반으로 정의** — "예쁜 5색" 조합이 아니라 Primary/Secondary/Accent/Neutral/Semantic 역할로 나눠야 한다. 컨셉 단계에서도 "어떤 역할의 컬러가 어떤 톤인지"를 명시해야 design-system 단계에서 토큰 체계로 이어진다.
8. **접근성 대비율을 컬러 방향 단계에서 언급** — 컨셉 단계에서 "고대비/저대비 무드"를 결정할 때 WCAG AA 기준(일반 텍스트 4.5:1, 큰 텍스트 3:1)을 제약으로 고려하라. 나중에 토큰 단계에서 브랜드색이 접근성을 통과 못해 방향을 바꾸는 일이 생긴다.
9. **무드보드 HTML의 필수 섹션 누락 금지** — Step 5에서 생성하는 무드보드 HTML은 Mood Keywords, Color Palette, Typography, Imagery Direction, Texture/Material, Layout Cues, Do/Don't 섹션을 모두 포함해야 한다. 섹션이 빠지면 무드보드가 시각 자료 모음에 그친다.

# Process

## Step 0: 기존 컨셉 감지

`.design/concept.md`가 존재하는지 확인한다:
- 존재 → 로드하여 수정/확장 모드로 진입. 기존 컨셉 내용을 사용자에게 요약하고 변경할 부분을 확인한다.
- 미존재 → 신규 생성 모드로 진행.

## Step 1: 사용자 입력 분석

사용자의 입력을 3가지 경로로 분류한다:
- **키워드/분위기 설명**: "미니멀하고 따뜻한 SaaS 대시보드"
- **레퍼런스 URL**: WebFetch로 사이트를 분석하여 시각적 특징 추출
- **둘 다**: 키워드 + URL을 조합

입력이 불명확하면 사용자에게 다음을 확인한다:
- 프로젝트 성격 (앱 유형, 대상 사용자)
- 원하는 분위기 키워드 2-3개
- 참고할 사이트/앱이 있는지

## Step 2: 웹 리서치

references/concept-criteria.md를 참조하여 관련 디자인 레퍼런스를 조사한다:
- WebSearch 또는 Codex로 관련 디자인 트렌드/사례 검색
- 유사한 성격의 프로덕트 디자인 분석
- 검색 결과에서 컬러 방향, 타이포 트렌드, UI 패턴 추출
- 모든 리서치 결과에 출처 URL 기록

## Step 3: 컨셉 요소 도출

references/concept-criteria.md의 카테고리별로 컨셉 요소를 정리한다:
- **무드 키워드**: 3-5개 핵심 형용사 (예: minimal, warm, professional)
- **키워드→시각 번역**: 각 키워드를 color / type / image / shape / layout / motion으로 매핑한다
  - 예: `Calm` → 저채도 컬러, 넓은 여백, 부드러운 코너, 느린 모션
  - 예: `Bold` → 고대비, 큰 타이포, 강한 그리드, 비대칭 레이아웃
  - 예: `Premium` → 절제된 팔레트, 큰 여백, 소재감 있는 이미지
- **컬러 방향**: Primary/Secondary/Accent/Neutral/Semantic 역할별 톤 계열과 채도 방향 (hex 값 아님). WCAG AA 대비율 충족 가능한 톤인지 방향 단계에서 확인
- **타이포 방향**: 서체 분류(sans-serif/serif/mono), display/body 페어링 방향, 위계 구성(weight/size/tracking으로 처리할지 폰트 수로 처리할지)
- **레이아웃 방향**: hero 구조, 그리드 밀도, 콘텐츠 흐름, 이미지 비중 — 여러 컨셉 안이면 이 축에서 차별화
- **UI 패턴 스타일**: 카드형/리스트형, 네비게이션 패턴, 정보 밀도 수준, 컴포넌트 톤(sharp/rounded/fluid)

## Step 4: 컨셉 문서 생성

templates/concept.md 포맷으로 `.design/concept.md`를 생성(또는 갱신)한다:

```markdown
# 디자인 컨셉

> 생성일: {{date}}
> 프로젝트: {{project-name}}

## 컨셉 선언
{{한 문장으로 이 디자인이 무엇을 표현하는지 — "왜 이 방향인가"를 담는다}}

## 무드 키워드
{{키워드 목록 + 각 키워드의 의미}}

## 키워드 → 시각 언어 매핑
| 키워드 | Color | Type | Layout | Image/Shape | Motion |
|--------|-------|------|--------|-------------|--------|
| {{keyword}} | ... | ... | ... | ... | ... |

## 컬러 방향
{{Primary/Secondary/Accent/Neutral/Semantic 역할별 톤 계열과 채도 방향. WCAG AA 대비 가능성 메모}}

## 타이포그래피 방향
{{서체 분류, display/body 페어링, 위계 구성 방향, 스케일 방향}}

## 레이아웃 방향
{{hero 구조, 그리드 밀도, 콘텐츠 흐름, 이미지 비중}}

## UI 패턴
{{레이아웃 패턴, 네비게이션, 정보 밀도, 컴포넌트 톤}}

## Do / Don't
- Do: {{이 컨셉에서 의도적으로 강조할 것}}
- Don't: {{이 컨셉에서 피해야 할 것}}

## 레퍼런스
{{참고 사이트/앱 목록 + 각각에서 참고할 요소}}
```

## Step 5: 비주얼 무드보드 HTML 생성

../../templates/moodboard.html 포맷으로 `.design/moodboard.html`을 생성한다. 아래 섹션을 모두 포함해야 한다:

- **Mood Keywords** — 컨셉 선언 + 키워드 태그
- **Color Palette** — Primary/Secondary/Accent/Neutral/Semantic 역할별 컬러 스와치 (방향 시각화, hex 확정값 아님)
- **Typography** — display/body 서체 분류 예시, 위계 샘플 (H1~body 레벨)
- **Imagery Direction** — 이미지 톤/스타일 설명 + 대표 분위기 시각화
- **Texture / Material** — 질감, 표면, 소재 방향 시각화
- **Layout Cues** — hero 구조, 그리드, 콘텐츠 흐름 스케치 (여러 컨셉 안이면 각각 별도 블록)
- **Do / Don't** — 이 컨셉에서 의도적으로 강조할 것 vs 피할 것

브라우저에서 바로 열어 확인 가능한 standalone HTML로 생성한다.

## Step 6: 사용자 피드백

- 컨셉 문서와 무드보드를 사용자에게 제시
- 피드백을 받아 수정 반복
- 사용자가 확정하면 다음 단계 안내

## Step 7: 다음 단계 안내

> "컨셉이 확정되었습니다. 다음 단계로 `/design-system`을 사용하여 이 컨셉 기반의 디자인 토큰을 정의할 수 있습니다."

# References

- `references/concept-criteria.md` — 컨셉 도출 기준 상세
- `templates/concept.md` — 컨셉 문서 출력 포맷
- `../../templates/moodboard.html` — 비주얼 무드보드 출력 포맷 (공유 템플릿)
