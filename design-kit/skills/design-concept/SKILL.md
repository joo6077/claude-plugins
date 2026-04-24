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
3. **컬러 값 직접 지정 금지 (concept.md)** — `.design/concept.md`의 "컬러 방향" 표에는 hex 값을 쓰지 마라. "따뜻한 뉴트럴 계열, muted 채도, 번트 앰버 계열 포인트" 같은 **서술형 방향**만 쓴다. 구체적 hex(또는 oklch) 확정과 WCAG 수치 계산은 design-system 단계에서 수행한다.

   **재발 방지 — SK-06 (2026-04-10 글로벌 피드백):** 드라이런에서 Claude가 `| Accent | #E8965A |` 형태로 hex 확정값을 concept.md에 기재하여 REJECT된 사례가 있다. Gotcha 본문에 원칙만 적고 검증 명령이 없으면 다음 세션의 Claude가 동일 실수를 반복한다.

   **Bad (concept.md에서 REJECT 사유):**

   ```text
   | Accent | #E8965A |   — hex 확정값 기재 → REJECT (SK-06)
   ```

   **Good (서술형 방향):**

   ```text
   | Accent | 번트 앰버 계열, muted 채도, WCAG 2.2 AA 통과 가능한 중간 명도 |
   ```

   **검증 체크리스트** (Step 4에서 concept.md 생성/갱신 직후 반드시 실행):

   ```bash
   # 1) concept.md 본문에 hex 리터럴(#rgb, #rrggbb, #rrggbbaa) 0건
   grep -nE '#[0-9a-fA-F]{3,8}\b' .design/concept.md   # → 0 match

   # 2) 컬러 방향 표에 5개 역할 행 모두 존재 (Primary/Secondary/Accent/Neutral/Semantic)
   grep -cE '^\|\s*(Primary|Secondary|Accent|Neutral|Semantic)\s*\|' .design/concept.md   # → 5

   # 3) oklch() 리터럴도 concept 단계에서는 사용 금지 (서술형만 허용)
   grep -cE 'oklch\(' .design/concept.md   # → 0
   ```

   매치가 1건이라도 나오면 즉시 해당 행을 서술형으로 되돌려라. 재생성 후 동일 명령을 재실행하여 0건/5건/0건을 확인한 뒤 Step 5로 넘어간다.

   **예외:** 무드보드 HTML(`.design/moodboard.html`)은 시각화 목적상 hex placeholder를 채울 수 있으나 **반드시 상단에 "방향 시각화용 참조값" disclaimer 배너가 렌더링되어야 한다**. 템플릿(`design-kit/templates/moodboard.html`)은 `.mb-disclaimer` 섹션과 `data-i18n="disclaimer.color"` 문구를 포함하며 생성 시 삭제 금지. 이 배너가 없으면 무드보드 hex가 "확정값"으로 오독된다 (Phase B 드라이런에서 실제 REJECT 근거였다).
4. **기존 컨셉 무시 금지** — `.design/concept.md`가 이미 존재하면 반드시 로드하여 수정/확장 모드로 진입하라. 기존 내용을 무시하고 새로 만들면 이전 합의가 사라진다.
5. **무드 키워드를 시각 속성으로 번역하지 않으면 의미 없음** — "미니멀", "따뜻함" 같은 키워드는 반드시 `color / type / image / shape / layout / motion` 각각에 대한 구체적 방향으로 번역해야 한다. 키워드만 나열하고 시각 규칙이 없으면 팀마다 다르게 해석되어 무드보드가 장식으로 끝난다.
6. **컨셉 시안은 컬러 교체가 아니라 레이아웃 차별화** — 여러 컨셉 안을 제시할 때 색상만 바꾸는 것은 "스타일 옵션"이지 "컨셉 옵션"이 아니다. hero 구조, 그리드, 콘텐츠 밀도, 타이포 위계, 이미지 비중 중 최소 2개 이상이 달라야 검토 가치가 생긴다.
7. **컬러 방향은 역할 기반으로 정의** — "예쁜 5색" 조합이 아니라 Primary/Secondary/Accent/Neutral/Semantic 역할로 나눠야 한다. 컨셉 단계에서도 "어떤 역할의 컬러가 어떤 톤인지"를 명시해야 design-system 단계에서 토큰 체계로 이어진다.
8. **접근성 대비율을 컬러 방향 단계에서 언급** — 컨셉 단계에서 "고대비/저대비 무드"를 결정할 때 WCAG AA 기준(일반 텍스트 4.5:1, 큰 텍스트 3:1)을 제약으로 고려하라. 나중에 토큰 단계에서 브랜드색이 접근성을 통과 못해 방향을 바꾸는 일이 생긴다. 추가로 APCA Lc 임계값(본문 Lc 75~90, 비본문 Lc 60)도 참고하면 폰트 크기+굵기별 대비 가이드가 더 정밀해진다.
9. **OKLCH 색상 공간 인식** — 컬러 방향 서술 시, OKLCH(Lightness-Chroma-Hue) 축으로 사고하면 지각적으로 균일한 팔레트 방향을 잡기 쉽다. "밝기 L=0.6~0.7 범위, 낮은 채도 C<0.1" 같은 서술이 "파스텔 톤"보다 design-system 단계로 이어질 때 정밀하다. hex 값은 여전히 concept 단계에서 기재 금지이며 서술형만 허용. 출처: research-log §D.
9. **무드보드 HTML의 필수 섹션 누락 금지** — Step 5에서 생성하는 무드보드 HTML은 **7개 필수 섹션**을 모두 포함해야 한다. 섹션이 빠지면 무드보드가 시각 자료 모음에 그친다.

   **필수 섹션 ↔ 템플릿 매핑** (`design-kit/templates/moodboard.html` 기준):

   | # | SKILL.md 요구 섹션 | 템플릿 섹션명 (`data-i18n="section.*"`) | 한글 라벨 |
   |---|---------------------|-----------------------------------------|-----------|
   | 1 | Mood Keywords       | `section.keywords`                      | 무드 키워드 |
   | 2 | Color Palette       | `section.palette`                       | 컬러 팔레트 |
   | 3 | Typography          | `section.typography`                    | 타이포그래피 |
   | 4 | Imagery Direction   | `section.references`                    | 레퍼런스 (inspiration 이미지 그리드) |
   | 5 | Texture / Material  | `section.texture`                       | 질감 & 소재 |
   | 6 | Layout Cues         | `section.layout`                        | 레이아웃 큐 |
   | 7 | Do / Don't          | `section.dodont`                        | Do / Don't |

   **검증 체크리스트** (Step 5 완료 직후 반드시 실행):
   ```bash
   # 1) 미치환 placeholder 없어야 함
   grep -c '{{' .design/moodboard.html   # → 0

   # 2) 7개 섹션 모두 존재해야 함 (7개 매치)
   grep -cE 'data-i18n="section\.(keywords|palette|typography|references|texture|layout|dodont)"' .design/moodboard.html  # → 7

   # 3) color disclaimer 배너 존재 (Gotcha #3)
   grep -c 'data-i18n="disclaimer.color"' .design/moodboard.html   # → 1
   ```
   하나라도 어긋나면 즉시 템플릿 치환을 재실행하고 누락 placeholder를 채워라.

   **주의:** 과거 템플릿에 Tone & Manner 섹션(`section.tone`)이 있었고 Texture/Layout/DoDont가 없었다. Phase B 드라이런에서 이 불일치 때문에 REJECT를 받았다. 7개 필수 섹션과 Tone & Manner(선택)는 별개다.

# Process

## Step 0: 자동 감지 및 로드

프로젝트에서 이전 단계 산출물을 탐색한다 (sibling parity — design-component/design-mockup Step 0 동일 패턴):

```text
# 감지 대상
.design/concept.md          → 기존 컨셉 로드 (수정/확장 모드)
**/theme/** **/tokens/**    → 이미 토큰 체계가 있으면 컨셉 방향 제약으로 활용
```

- `.design/concept.md` 존재 → 로드하여 수정/확장 모드로 진입. 기존 컨셉 내용을 사용자에게 요약하고 변경할 부분을 확인한다.
- `.design/concept.md` 미존재 → 신규 생성 모드로 진행.

**이 Step 0 은 독립 Process 단계다 (SK-05 재발 방지)** — Gotchas 의 "기존 컨셉 무시 금지" 지침(Gotcha #4) 과 별개로 Process 첫 단계에서 반드시 수행한다. 자동 로드 로직을 Gotchas 섹션에만 기재하면 평가자가 "프로세스 단계" 요건 미충족으로 판정한다 (2026-04 design-kit REJECT 사유).

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
<!-- ⚠ hex 값 직접 기재 금지 — 서술형 방향만 허용. hex 확정은 design-system 단계에서 수행. -->
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

**생성/갱신 직후 반드시 Gotcha #3의 검증 체크리스트 3개를 실행하라.** hex 리터럴 0건, 5개 역할 행, oklch() 0건이 모두 충족되어야 Step 5로 넘어간다. 미충족 시 해당 행을 서술형으로 되돌리고 재실행. 이 체크포인트는 SK-06 재발 방지의 핵심이므로 "나중에" 미루지 마라.

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

**생성 직후 반드시 Gotcha #9의 3개 검증 명령을 실행하라.** 미치환 placeholder 0개, 7개 섹션 매치, disclaimer 배너 1개 — 하나라도 어긋나면 재생성.

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
