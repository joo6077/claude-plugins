# design-kit 신규 스킬 3종 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** design-kit 플러그인에 design-concept, design-mockup, design-component 3개 스킬과 references 파일을 추가한다.

**Architecture:** 기존 design-kit 스킬(design-system, design-guide, design-audit)과 동일한 디렉토리 구조(SKILL.md + references/ + templates/)를 따른다. 각 스킬은 독립 호출 가능하며, 이전 단계 산출물을 자동 감지한다.

**Tech Stack:** Markdown (SKILL.md, references), 플러그인 구조

---

## 파일 구조

```
design-kit/skills/
├── design-concept/
│   ├── SKILL.md                          # 신규
│   └── references/
│       └── concept-criteria.md           # 신규
├── design-mockup/
│   ├── SKILL.md                          # 신규
│   └── references/
│       └── mockup-guidelines.md          # 신규
└── design-component/
    ├── SKILL.md                          # 신규
    └── references/
        └── component-spec-template.md    # 신규
```

---

### Task 1: design-concept SKILL.md

**Files:**
- Create: `design-kit/skills/design-concept/SKILL.md`

- [ ] **Step 1: 디렉토리 생성**

Run: `mkdir -p design-kit/skills/design-concept/references`

- [ ] **Step 2: SKILL.md 작성**

```markdown
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
- **컬러 방향**: 톤 계열, 채도 수준, 포인트 컬러 방향 (hex 값 아님)
- **타이포 방향**: 서체 분류(sans-serif/serif/mono), 웨이트 활용 방향
- **UI 패턴 스타일**: 카드형/리스트형, 네비게이션 패턴, 정보 밀도 수준

## Step 4: 컨셉 문서 생성

`.design/concept.md`를 생성(또는 갱신)한다:

```markdown
# 디자인 컨셉

> 생성일: {{date}}
> 프로젝트: {{project-name}}

## 무드 키워드
{{키워드 목록 + 각 키워드의 의미}}

## 컬러 방향
{{톤 계열, 채도, 포인트 컬러 방향}}

## 타이포그래피 방향
{{서체 분류, 웨이트 활용, 스케일 방향}}

## UI 패턴
{{레이아웃 패턴, 네비게이션, 정보 밀도}}

## 레퍼런스
{{참고 사이트/앱 목록 + 각각에서 참고할 요소}}
```

## Step 5: 비주얼 무드보드 HTML 생성

`.design/moodboard.html`을 생성한다:
- 컬러 방향을 시각화한 팔레트 샘플
- 타이포그래피 샘플 (서체 분류별 예시)
- 레이아웃 패턴 스케치
- 브라우저에서 바로 열어 확인 가능한 standalone HTML

## Step 6: 사용자 피드백

- 컨셉 문서와 무드보드를 사용자에게 제시
- 피드백을 받아 수정 반복
- 사용자가 확정하면 다음 단계 안내

## Step 7: 다음 단계 안내

> "컨셉이 확정되었습니다. 다음 단계로 `/design-system`을 사용하여 이 컨셉 기반의 디자인 토큰을 정의할 수 있습니다."

# References

- `references/concept-criteria.md` — 컨셉 도출 기준 상세
```

- [ ] **Step 3: 파일 생성 확인**

Run: `cat design-kit/skills/design-concept/SKILL.md | head -5`
Expected: frontmatter 시작 (`---`, `name: design-concept`)

- [ ] **Step 4: 커밋**

```bash
git add design-kit/skills/design-concept/SKILL.md
git commit -m "feat(design-kit): design-concept SKILL.md 추가

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: design-concept references

**Files:**
- Create: `design-kit/skills/design-concept/references/concept-criteria.md`

- [ ] **Step 1: concept-criteria.md 작성**

```markdown
# 컨셉 도출 기준

design-concept 스킬이 참조하는 컨셉 도출 카테고리와 기준.

## 무드 키워드 분류

| 축 | 예시 키워드 |
|----|-------------|
| 온도 | warm, cool, neutral |
| 무게감 | light, bold, heavy |
| 형식성 | formal, casual, playful |
| 복잡도 | minimal, rich, dense |
| 시대감 | classic, modern, futuristic |

3-5개 키워드를 선정하여 프로젝트의 디자인 톤을 정의한다.

## 컬러 방향 체계

컨셉 단계에서는 구체적 hex 값이 아닌 **방향**만 정의한다:

| 요소 | 정의 내용 | 예시 |
|------|-----------|------|
| 톤 계열 | warm/cool/neutral | "따뜻한 뉴트럴 베이스" |
| 채도 수준 | muted/vivid/mixed | "전반적으로 muted, 포인트만 vivid" |
| 포인트 방향 | 강조색의 역할과 느낌 | "에너지를 주는 오렌지 계열 포인트" |
| 다크 모드 방향 | 다크 모드의 성격 | "순수 검정 아닌 다크 그레이 베이스" |

> **참조:** `docs/design/foundations/color.md` — 컬러 시스템 원칙
> **참조:** `docs/design/foundations/authentic-design.md` — 제네릭 컬러 방지

## 타이포그래피 선택 기준

| 요소 | 선택지 | 고려 사항 |
|------|--------|-----------|
| 서체 분류 | sans-serif / serif / mono / mixed | 프로젝트 성격, 가독성 |
| 본문 서체 | 시스템 폰트 / 웹폰트 | 로딩 성능, 브랜드 |
| 제목 서체 | 본문과 동일 / 대비 서체 | 시각 위계, 브랜드 개성 |
| 웨이트 활용 | 2단계(regular/bold) / 3단계+ | 위계 표현 필요도 |

> **참조:** `docs/design/foundations/typography.md` — 타이포그래피 원칙

## UI 패턴 카테고리

| 카테고리 | 선택지 |
|----------|--------|
| 레이아웃 기본 형태 | 카드 그리드 / 리스트 / 매거진 / 대시보드 |
| 네비게이션 패턴 | 탭바 / 사이드바 / 햄버거 / 탑바 |
| 정보 밀도 | 낮음(여백 중심) / 중간 / 높음(데이터 중심) |
| 카드 스타일 | 플랫 / 엘리베이션 / 보더 / 글래스모피즘 |
| 버튼 스타일 | 필드 / 아웃라인 / 텍스트 / 라운드 |
| 인풋 스타일 | 언더라인 / 아웃라인 / 필드 |

> **참조:** `docs/design/systems/material-design.md` — Material Design 패턴
> **참조:** `docs/design/systems/apple-hig.md` — Apple HIG 패턴
> **참조:** `docs/design/systems/open-source-systems.md` — 오픈소스 디자인 시스템 패턴
```

- [ ] **Step 2: 파일 생성 확인**

Run: `ls design-kit/skills/design-concept/references/`
Expected: `concept-criteria.md`

- [ ] **Step 3: 커밋**

```bash
git add design-kit/skills/design-concept/references/concept-criteria.md
git commit -m "feat(design-kit): design-concept references 추가

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: design-mockup SKILL.md

**Files:**
- Create: `design-kit/skills/design-mockup/SKILL.md`

- [ ] **Step 1: 디렉토리 생성**

Run: `mkdir -p design-kit/skills/design-mockup/references`

- [ ] **Step 2: SKILL.md 작성**

```markdown
---
name: design-mockup
description: >
  특정 화면 요청 시 하이파이 HTML 시안 5개를 생성하여 제시한다.
  정의된 디자인 컨셉과 토큰이 있으면 자동으로 로드하여 반영한다.
  각 시안의 UI 요소에 유니크 ID를 부여하여 사용자가 특정 컴포넌트를
  지칭하거나 추출할 수 있다. 선택한 시안/컴포넌트를 Figma MCP로 전송 가능.
  "시안 만들어줘", "목업", "mockup", "화면 시안", "디자인 시안",
  "레이아웃 제안", "시안 보여줘" 같은 요청 시 트리거.
  기존 UI 코드 리뷰/가이드에는 트리거하지 않는다 — design-guide 사용.
argument-hint: "<page-name or description>"
user-invocable: true
---

# Gotchas

1. **컬러 변형만으로 시안 구분 금지** — 5개 시안은 서로 다른 레이아웃/구성 접근이어야 한다. 같은 레이아웃에 컬러만 바꾸면 선택지가 아니라 색상 팔레트 비교가 된다.
2. **ID 중복 금지** — 시안 5개에 걸쳐 모든 컴포넌트 ID는 전역 유니크여야 한다. `{컴포넌트명}-{짧은해시}` 포맷을 사용하라. 같은 해시가 나오면 재생성한다.
3. **접근성 원칙 무시 금지** — 하이파이 시안이라도 WCAG AA 대비 비율(4.5:1), 최소 터치 타겟(44×44pt)을 준수하라. 시각적으로 예뻐도 접근성 위반이면 안 된다.
4. **Figma MCP 미설정 시 에러 금지** — Figma 전송 요청 시 MCP가 미설정이면 에러가 아닌 안내로 처리하라. "Figma 전송을 원하면 Figma MCP 설정이 필요합니다"와 함께 HTML 파일 경로를 안내한다.

# Process

## Step 1: 화면 요구사항 파악

사용자의 요청에서 파악한다:
- 어떤 페이지/화면인지 (로그인, 대시보드, 설정 등)
- 주요 기능과 정보 요소
- 대상 사용자

불명확하면 사용자에게 확인한다.

## Step 2: 자동 감지 및 로드

프로젝트에서 이전 단계 산출물을 탐색한다:

```
# 감지 대상
.design/concept.md          → 컨셉 로드
**/theme/** **/tokens/**    → 디자인 토큰 로드
**/design-tokens.*          → 디자인 토큰 로드
```

- 컨셉 존재 → 무드 키워드, 컬러/타이포 방향, UI 패턴을 시안에 반영
- 토큰 존재 → 구체적 컬러값, 타이포 스케일, 간격을 시안에 적용
- 둘 다 없음 → 사용자 요구사항만으로 시안 생성

## Step 3: 하이파이 HTML 시안 5개 생성

references/mockup-guidelines.md를 참조하여 시안을 생성한다:

각 시안은 standalone HTML 파일로 생성:
- `.design/mockups/{페이지명}-{특징}.html` (예: `dashboard-sidebar.html`)
- 실제 컬러, 타이포, 간격이 반영된 하이파이 수준
- 모든 UI 요소에 `{컴포넌트명}-{4자리해시}` ID 부여
- 호버 시 ID를 표시하는 JavaScript 오버레이 포함

시안별 레이아웃 차별화 예시:
1. 사이드바 네비게이션 + 메인 콘텐츠
2. 탑바 + 카드 그리드
3. 탭 기반 + 리스트 뷰
4. 풀스크린 히어로 + 스크롤 섹션
5. 대시보드 + 위젯 패널

## Step 4: 디자인 의도 설명

각 시안에 대해 설명한다:
- 레이아웃 선택 이유
- 정보 구조와 시각적 강조 포인트
- 어떤 사용 시나리오에 적합한지

## Step 5: 사용자 선택 및 수정

- 사용자가 시안을 선택하거나 피드백을 준다
- ID를 사용한 소통: "card-product-a3f2를 더 크게 해줘"
- 수정 후 HTML 파일 갱신
- 확정 시 `.design/mockups/` 에 최종본 유지

## Step 6: Figma 전송 (선택)

사용자가 Figma 전송을 요청하면:
- Figma MCP 설정 확인
- 설정됨 → 선택한 시안 또는 개별 컴포넌트(ID 기준)를 Figma로 전송
- 미설정 → "Figma 전송을 원하면 Figma MCP 설정이 필요합니다" 안내 + HTML 파일 경로 재안내
- 전송 실패 → 에러 메시지 + HTML 파일 경로 안내

# References

- `references/mockup-guidelines.md` — 시안 생성 기준 상세
```

- [ ] **Step 3: 파일 생성 확인**

Run: `cat design-kit/skills/design-mockup/SKILL.md | head -5`
Expected: frontmatter 시작 (`---`, `name: design-mockup`)

- [ ] **Step 4: 커밋**

```bash
git add design-kit/skills/design-mockup/SKILL.md
git commit -m "feat(design-kit): design-mockup SKILL.md 추가

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: design-mockup references

**Files:**
- Create: `design-kit/skills/design-mockup/references/mockup-guidelines.md`

- [ ] **Step 1: mockup-guidelines.md 작성**

```markdown
# 시안 생성 기준

design-mockup 스킬이 참조하는 시안 생성 가이드라인.

## 레이아웃 다양성 규칙

5개 시안은 반드시 서로 다른 레이아웃/구성 접근을 사용한다:

| 차별화 축 | 설명 |
|-----------|------|
| 네비게이션 위치 | 사이드바 / 탑바 / 탭바 / 없음 |
| 콘텐츠 구조 | 그리드 / 리스트 / 매거진 / 대시보드 |
| 정보 위계 | 히어로 중심 / 균등 배분 / 점진적 공개 |
| 밀도 수준 | 여백 중심 / 균형 / 데이터 밀도 |

최소 2개 축에서 차이가 나야 별도 시안으로 인정한다.
단순 컬러 변형, 폰트 크기 변형만으로는 시안 구분 불가.

## 하이파이 수준 정의

| 요소 | 요구 수준 |
|------|-----------|
| 컬러 | 실제 컬러값 적용 (토큰 존재 시 토큰 값, 미존재 시 합리적 기본값) |
| 타이포 | 실제 폰트 패밀리, 크기, 행간, 두께 적용 |
| 간격 | 스페이싱 스케일 기반 실제 패딩/마진 적용 |
| 콘텐츠 | 실제 텍스트 사용 (Lorem ipsum 최소화, 맥락에 맞는 텍스트) |
| 아이콘 | 실제 아이콘 또는 의미 있는 플레이스홀더 |
| 이미지 | 의미 있는 플레이스홀더 (크기/비율 정확) |

## 컴포넌트 ID 부여 규칙

모든 의미 있는 UI 요소에 ID를 부여한다:

**포맷:** `{컴포넌트명}-{4자리해시}`
- 컴포넌트명: 역할을 나타내는 kebab-case (예: `card-product`, `btn-primary`, `header-nav`)
- 해시: 4자리 hex (전역 유니크 보장)

**ID 부여 대상:**
- 모든 버튼, 링크
- 카드, 리스트 아이템
- 네비게이션 요소
- 입력 필드, 폼
- 섹션 컨테이너
- 헤더, 푸터

**ID 미부여 대상:**
- 순수 장식 요소 (구분선, 배경 그래디언트)
- 래퍼/스페이서 div

**호버 오버레이 구현:**

시안 HTML에 다음 JavaScript를 포함한다:
- 요소 호버 시 해당 요소의 ID를 보여주는 툴팁 표시
- 툴팁 클릭 시 ID가 클립보드에 복사됨
- 오버레이 토글 버튼 (우하단 고정, 기본 OFF)

## 디자인 원칙 체크리스트

시안 생성 후 자동으로 확인할 항목:

| 원칙 | 기준 | 참조 |
|------|------|------|
| 시각 위계 | 제목/본문/캡션 크기 비율 1.2배 이상 | `docs/design/foundations/visual-hierarchy.md` |
| 간격 일관성 | 정의된 스케일 값만 사용 | `docs/design/foundations/spacing-layout.md` |
| 그리드 정렬 | 요소가 그리드에 정렬됨 | `docs/design/foundations/grid-alignment.md` |
| 대비 비율 | WCAG AA 4.5:1 이상 | `docs/design/accessibility/accessibility.md` |
| 터치 타겟 | 인터랙티브 요소 44×44pt 이상 | `docs/design/accessibility/accessibility.md` |
| 인증성 | 동일 구조 3회 이상 반복 없음 | `docs/design/foundations/authentic-design.md` |
| 피드백 | 인터랙티브 요소에 hover/active 상태 존재 | `docs/design/interaction/feedback.md` |
```

- [ ] **Step 2: 파일 생성 확인**

Run: `ls design-kit/skills/design-mockup/references/`
Expected: `mockup-guidelines.md`

- [ ] **Step 3: 커밋**

```bash
git add design-kit/skills/design-mockup/references/mockup-guidelines.md
git commit -m "feat(design-kit): design-mockup references 추가

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: design-component SKILL.md

**Files:**
- Create: `design-kit/skills/design-component/SKILL.md`

- [ ] **Step 1: 디렉토리 생성**

Run: `mkdir -p design-kit/skills/design-component/references`

- [ ] **Step 2: SKILL.md 작성**

```markdown
---
name: design-component
description: >
  반복되는 UI 요소를 컴포넌트로 정의하고 카탈로그화한다.
  확정된 시안에서 추출하거나 사용자가 직접 지정한 요소를 대상으로,
  variant, 상태, 토큰 매핑을 포함한 디자인 스펙을 생성한다.
  컨셉, 토큰, 시안이 있으면 자동으로 로드하여 일관성을 유지한다.
  "컴포넌트 정의", "컴포넌트 리스트", "design component",
  "UI 컴포넌트 정리", "컴포넌트 만들어줘", "컴포넌트 카탈로그" 같은 요청 시 트리거.
  실제 코드 구현에는 트리거하지 않는다 — 해당 toolkit 플러그인 사용.
argument-hint: "[component-name or mockup-id]"
user-invocable: true
---

# Gotchas

1. **구현 코드 생성 금지** — 이 스킬은 디자인 스펙만 출력한다. Flutter/React/CSS 컴포넌트 코드를 직접 생성하지 마라. 해당 toolkit 플러그인에 위임하라.
2. **상태 누락 금지** — 모든 인터랙티브 컴포넌트에 default, hover, active, disabled 상태를 정의하라. loading 상태가 필요한 경우(버튼, 카드) 포함한다. 상태가 1-2개만 정의된 컴포넌트는 불완전하다.
3. **토큰 매핑 누락 금지** — 디자인 토큰이 존재하면 모든 컴포넌트의 컬러, 타이포, 간격, 라디우스를 토큰에 매핑하라. 하드코딩 값은 토큰 체계를 무력화한다.
4. **시안 ID 무시 금지** — 확정된 시안에서 컴포넌트를 추출할 때, 해당 컴포넌트의 시안 ID(`{컴포넌트명}-{해시}`)를 카탈로그에 기록하라. 출처 추적에 필요하다.

# Process

## Step 1: 자동 감지 및 로드

프로젝트에서 이전 단계 산출물을 탐색한다:

```
# 감지 대상
.design/concept.md              → 컨셉 로드 (컬러/타이포/UI 패턴 방향)
**/theme/** **/tokens/**        → 디자인 토큰 로드
.design/mockups/*.html          → 확정 시안 로드
```

- 시안 존재 → 시안에서 반복되는 UI 요소를 자동 식별하여 제안
- 토큰 존재 → 컴포넌트별 토큰 매핑 자동 생성
- 둘 다 없음 → 사용자가 직접 컴포넌트 목록을 지정

## Step 2: 대상 파악

컴포넌트 대상을 결정한다:
- **시안에서 추출**: 사용자가 시안 ID로 지정 (예: "card-product-a3f2를 컴포넌트화해줘")
- **자동 식별**: 시안에서 2회 이상 반복되는 UI 패턴을 제안
- **사용자 직접 지정**: "버튼, 카드, 입력 필드 정의해줘"

## Step 3: 컴포넌트 분류 및 정의

references/component-spec-template.md의 포맷으로 각 컴포넌트를 정의한다:

분류 카테고리:
- **액션**: 버튼, 링크, FAB
- **입력**: 텍스트 필드, 체크박스, 라디오, 드롭다운, 스위치
- **표시**: 카드, 리스트 아이템, 배지, 칩, 태그
- **네비게이션**: 탭, 사이드바 아이템, 브레드크럼
- **피드백**: 토스트, 다이얼로그, 바텀시트
- **레이아웃**: 디바이더, 스페이서, 컨테이너

## Step 4: 사용자 피드백

- 컴포넌트 카탈로그를 사용자에게 제시
- 피드백을 받아 수정 (variant 추가/제거, 상태 조정, 토큰 변경)
- 확정 시 `.design/components/catalog.md`에 저장

# References

- `references/component-spec-template.md` — 컴포넌트 정의 템플릿
```

- [ ] **Step 3: 파일 생성 확인**

Run: `cat design-kit/skills/design-component/SKILL.md | head -5`
Expected: frontmatter 시작 (`---`, `name: design-component`)

- [ ] **Step 4: 커밋**

```bash
git add design-kit/skills/design-component/SKILL.md
git commit -m "feat(design-kit): design-component SKILL.md 추가

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 6: design-component references

**Files:**
- Create: `design-kit/skills/design-component/references/component-spec-template.md`

- [ ] **Step 1: component-spec-template.md 작성**

```markdown
# 컴포넌트 정의 템플릿

design-component 스킬이 출력하는 컴포넌트 카탈로그의 포맷.

## 컴포넌트 카탈로그 포맷

```markdown
# 컴포넌트 카탈로그

> 생성일: {{date}}
> 프로젝트: {{project-name}}
> 컴포넌트 수: {{count}}

## {{컴포넌트명}}

> 출처 시안 ID: {{mockup-id}} (있는 경우)

### 역할
{{이 컴포넌트의 목적과 사용 맥락}}

### Variants

| Variant | 설명 | 사용 맥락 |
|---------|------|-----------|
| primary | 주요 액션 | CTA, 핵심 동작 |
| secondary | 보조 액션 | 취소, 대안 동작 |
| ghost | 최소 강조 | 텍스트 링크 대체 |

### 상태

| 상태 | 시각적 변화 |
|------|-------------|
| default | 기본 표시 |
| hover | {{변화 설명}} |
| active/pressed | {{변화 설명}} |
| disabled | 투명도 0.38, 인터랙션 불가 |
| loading | {{변화 설명}} (해당 시) |
| focused | 포커스 링 표시 |

### 사이즈

| 사이즈 | 높이 | 패딩 | 폰트 |
|--------|------|------|------|
| sm | {{값}} | {{값}} | {{토큰}} |
| md | {{값}} | {{값}} | {{토큰}} |
| lg | {{값}} | {{값}} | {{토큰}} |

### 토큰 매핑

| 속성 | 토큰 |
|------|------|
| 배경색 (default) | {{토큰명}} |
| 배경색 (hover) | {{토큰명}} |
| 텍스트 컬러 | {{토큰명}} |
| 보더 라디우스 | {{토큰명}} |
| 패딩 | {{토큰명}} |
| 폰트 | {{토큰명}} |

### 사용 가이드라인

- **DO:** {{권장 사용법}}
- **DON'T:** {{금지 사용법}}
```

## 컴포넌트 카테고리별 필수 상태

| 카테고리 | 필수 상태 |
|----------|-----------|
| 버튼 | default, hover, active, disabled, loading, focused |
| 입력 필드 | default, hover, focused, error, disabled, filled |
| 카드 | default, hover (인터랙티브인 경우) |
| 네비게이션 | default, active/selected, hover |
| 토글/스위치 | off, on, disabled |
| 체크박스 | unchecked, checked, indeterminate, disabled |
```

- [ ] **Step 2: 파일 생성 확인**

Run: `ls design-kit/skills/design-component/references/`
Expected: `component-spec-template.md`

- [ ] **Step 3: 커밋**

```bash
git add design-kit/skills/design-component/references/component-spec-template.md
git commit -m "feat(design-kit): design-component references 추가

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 7: README 동기화 및 최종 검증

**Files:**
- Modify: `design-kit/README.md`

- [ ] **Step 1: sync-docs 실행**

Run: `python scripts/sync-docs.py design-kit`
Expected: README가 신규 스킬 3종을 반영하여 갱신됨

- [ ] **Step 2: 트리거 키워드 충돌 검사**

기존 스킬의 트리거 키워드와 신규 스킬의 트리거 키워드가 겹치지 않는지 확인:

Run: `grep -n "트리거" design-kit/skills/*/SKILL.md`

각 스킬의 description에서 트리거 키워드를 추출하여 교차 비교한다.

- [ ] **Step 3: 디렉토리 구조 확인**

Run: `find design-kit/skills -name "*.md" | sort`

Expected:
```
design-kit/skills/design-audit/SKILL.md
design-kit/skills/design-audit/references/audit-criteria.md
design-kit/skills/design-audit/templates/audit-report.md
design-kit/skills/design-component/SKILL.md
design-kit/skills/design-component/references/component-spec-template.md
design-kit/skills/design-concept/SKILL.md
design-kit/skills/design-concept/references/concept-criteria.md
design-kit/skills/design-guide/SKILL.md
design-kit/skills/design-guide/references/principle-index.md
design-kit/skills/design-mockup/SKILL.md
design-kit/skills/design-mockup/references/mockup-guidelines.md
design-kit/skills/design-system/SKILL.md
design-kit/skills/design-system/references/token-principles.md
design-kit/skills/design-system/templates/design-tokens.md
```

- [ ] **Step 4: 최종 커밋**

```bash
git add design-kit/README.md
git commit -m "docs(design-kit): README 동기화 — 신규 스킬 3종 반영

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 8: Sprint Contract 검증

- [ ] **Step 1: 계약 조건 체크**

`.harness/sprint-contract.md`의 모든 조건을 하나씩 검증한다:

| 조건 | 검증 방법 |
|------|-----------|
| SK-01 | `ls design-kit/skills/design-concept/SKILL.md design-kit/skills/design-mockup/SKILL.md design-kit/skills/design-component/SKILL.md` |
| SK-02 | 각 SKILL.md에서 `grep -c "user-invocable: true"` |
| SK-03 | 각 SKILL.md description에서 트리거 키워드 존재 확인 |
| SK-04 | 각 SKILL.md Process에서 "없으면"/"미존재" fallback 경로 확인 |
| SK-05 | 각 SKILL.md Process에서 자동 감지/로드 단계 확인 |
| ER-01 | design-mockup Process Step 2의 "둘 다 없음" 분기 확인 |
| ER-02 | design-component Process Step 1의 "둘 다 없음" 분기 확인 |
| AR-01 | 디렉토리 구조가 기존 스킬과 동일 패턴인지 확인 |
| AR-02 | 산출물 경로가 `.design/` 하위인지 SKILL.md에서 확인 |
| AR-03 | 트리거 키워드 교차 비교 |

- [ ] **Step 2: QA Evaluator 실행**

qa-evaluator 에이전트를 호출하여 최종 APPROVE/REJECT 판정을 받는다.

- [ ] **Step 3: 결과에 따라 수정 또는 완료**

APPROVE → 완료
REJECT → FAIL 항목 수정 후 재검증
