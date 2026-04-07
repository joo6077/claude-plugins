# design-kit 산출물 템플릿 + docs site 페이지 설계

## 개요

신규 4개 스킬(design-concept, design-reference, design-mockup, design-component)에 산출물 템플릿을 추가하고, docs site에 각 스킬의 예시 페이지를 생성한다. 모든 예시는 "미니멀 SaaS 대시보드" 가상 프로젝트를 기준으로 통일한다.

## 작업 범위

1. **4개 스킬에 templates/ 디렉토리 추가** — 산출물 포맷을 고정 템플릿으로 정의
2. **docs site에 스킬별 HTML 페이지 4개 추가** — 템플릿 기반 예시 산출물 포함
3. **docs/index.html 업데이트** — 사이드바에 "Design Kit — 워크플로우" 카테고리 추가
4. **SKILL.md 업데이트** — Process에서 templates/ 참조 추가

---

## 1. 템플릿 파일 목록

| 스킬 | 템플릿 파일 | 산출물 경로 |
|------|------------|------------|
| design-concept | `templates/concept.md` | `.design/concept.md` |
| design-concept | `templates/moodboard.html` | `.design/moodboard.html` |
| design-reference | `templates/references.md` | `.design/references.md` |
| design-reference | `templates/reference-catalog.html` | `.design/reference-catalog.html` |
| design-mockup | `templates/mockup.html` | `.design/mockups/{name}.html` |
| design-component | `templates/catalog.md` | `.design/components/catalog.md` |

### 템플릿 포맷 규칙

- `{{placeholder}}` 형태로 채울 부분 표시
- 기존 design-system의 `templates/design-tokens.md`와 동일한 패턴
- 각 템플릿은 실행 시 해당 경로에 생성됨

### 1-1. design-concept/templates/concept.md

```markdown
# 디자인 컨셉

> 생성일: {{date}}
> 프로젝트: {{project-name}}
> 모드: {{신규 생성 | 수정/확장}}

## 무드 키워드

| 키워드 | 의미 | 축 |
|--------|------|-----|
| {{keyword}} | {{description}} | {{온도/무게감/형식성/복잡도/시대감}} |

## 컬러 방향

| 요소 | 방향 |
|------|------|
| 톤 계열 | {{warm/cool/neutral + 설명}} |
| 채도 수준 | {{muted/vivid/mixed + 설명}} |
| 포인트 방향 | {{강조색 역할과 느낌}} |
| 다크 모드 방향 | {{다크 모드 성격}} |

## 타이포그래피 방향

| 요소 | 선택 | 근거 |
|------|------|------|
| 서체 분류 | {{sans-serif/serif/mono/mixed}} | {{이유}} |
| 본문 서체 | {{시스템/웹폰트 + 이름}} | {{이유}} |
| 제목 서체 | {{본문과 동일/대비}} | {{이유}} |
| 웨이트 활용 | {{2단계/3단계+}} | {{이유}} |

## UI 패턴

| 카테고리 | 선택 | 근거 |
|----------|------|------|
| 레이아웃 기본 형태 | {{카드 그리드/리스트/매거진/대시보드}} | {{이유}} |
| 네비게이션 패턴 | {{탭바/사이드바/햄버거/탑바}} | {{이유}} |
| 정보 밀도 | {{낮음/중간/높음}} | {{이유}} |
| 카드 스타일 | {{플랫/엘리베이션/보더/글래스모피즘}} | {{이유}} |
| 버튼 스타일 | {{필드/아웃라인/텍스트/라운드}} | {{이유}} |
| 인풋 스타일 | {{언더라인/아웃라인/필드}} | {{이유}} |

## 레퍼런스

| # | 소스 | URL | 참고 포인트 |
|---|------|-----|-------------|
| 1 | {{소스명}} | {{URL}} | {{참고 요소}} |
```

### 1-2. design-concept/templates/moodboard.html

standalone HTML. 구조:
- 헤더: 프로젝트명 + 무드 키워드 태그
- 컬러 팔레트 섹션: 방향을 시각화한 컬러 스워치 (hex 확정 아닌 방향 표현)
- 타이포 섹션: 서체 분류별 샘플 텍스트
- UI 패턴 섹션: 선택한 패턴의 간략 스케치
- `{{placeholder}}`로 동적 부분 표시

### 1-3. design-reference/templates/references.md

```markdown
# 디자인 레퍼런스

> 생성일: {{date}}
> 키워드: {{keywords}}
> 수집 수: {{count}}/{{target}}

## 디자인 갤러리

| # | 소스 | URL | 레이아웃 | 컬러 | 타이포 | 참고 포인트 |
|---|------|-----|----------|------|--------|-------------|
| 1 | {{source}} | {{url}} | {{layout}} | {{color}} | {{typo}} | {{point}} |

## 실제 프로덕트

| # | 서비스명 | URL | 네비게이션 | 정보 구조 | 컴포넌트 패턴 | 참고 포인트 |
|---|----------|-----|-----------|-----------|---------------|-------------|
| 1 | {{name}} | {{url}} | {{nav}} | {{structure}} | {{components}} | {{point}} |

## 오픈소스 DS 컴포넌트

| # | DS명 | 컴포넌트 | 시각 스타일 | variant | 상태 표현 | 참고 포인트 |
|---|------|----------|------------|---------|-----------|-------------|
| 1 | {{ds}} | {{component}} | {{style}} | {{variants}} | {{states}} | {{point}} |
```

### 1-4. design-reference/templates/reference-catalog.html

standalone HTML. 구조:
- 헤더: 키워드 + 수집 수 요약
- 필터 바: 소스 채널별 토글 (갤러리/프로덕트/DS)
- 카드 그리드: 각 레퍼런스의 핵심 시각 요소를 CSS로 재현
- `{{placeholder}}`로 동적 부분 표시

### 1-5. design-mockup/templates/mockup.html

standalone HTML. 구조:
- 시안 콘텐츠 (하이파이 레이아웃)
- 모든 UI 요소에 `id="{컴포넌트명}-{4자리해시}"` 부여
- 호버 오버레이 JavaScript:
  - 우하단 토글 버튼 (기본 OFF)
  - 활성화 시 호버된 요소의 ID를 툴팁으로 표시
  - 툴팁 클릭 시 클립보드 복사
- `{{placeholder}}`로 페이지별 콘텐츠 부분 표시

### 1-6. design-component/templates/catalog.md

```markdown
# 컴포넌트 카탈로그

> 생성일: {{date}}
> 프로젝트: {{project-name}}
> 컴포넌트 수: {{count}}

## {{컴포넌트명}}

> 출처 시안 ID: {{mockup-id}}

### 역할
{{이 컴포넌트의 목적과 사용 맥락}}

### Variants

| Variant | 설명 | 사용 맥락 |
|---------|------|-----------|
| {{name}} | {{description}} | {{context}} |

### 상태

| 상태 | 시각적 변화 |
|------|-------------|
| default | {{description}} |
| hover | {{description}} |
| active/pressed | {{description}} |
| disabled | 투명도 0.38, 인터랙션 불가 |
| loading | {{description}} |
| focused | 포커스 링 표시 |

### 사이즈

| 사이즈 | 높이 | 패딩 | 폰트 |
|--------|------|------|------|
| sm | {{value}} | {{value}} | {{token}} |
| md | {{value}} | {{value}} | {{token}} |
| lg | {{value}} | {{value}} | {{token}} |

### 토큰 매핑

| 속성 | 토큰 |
|------|------|
| 배경색 (default) | {{token}} |
| 배경색 (hover) | {{token}} |
| 텍스트 컬러 | {{token}} |
| 보더 라디우스 | {{token}} |
| 패딩 | {{token}} |
| 폰트 | {{token}} |

### 사용 가이드라인

- **DO:** {{권장 사용법}}
- **DON'T:** {{금지 사용법}}
```

---

## 2. docs site 페이지

4개 HTML 페이지. 가상 프로젝트: "미니멀 SaaS 대시보드 (TaskFlow)".

### CSS/스타일 규칙

- 모든 HTML 파일은 외부 CSS/JS CDN을 사용하지 않는다 (standalone)
- 스타일은 `<style>` 태그 인라인으로 포함한다
- 기존 `docs/design-kit/` 페이지의 CSS 변수와 공통 클래스를 재사용한다
- 기존 패턴상 각 페이지가 인라인 CSS를 갖는 구조이므로, 신규 페이지도 동일하게 인라인 CSS로 작성한다 (공유 CSS 파일 추출 안 함)

### 공통 페이지 HTML 스켈레톤

기존 design-kit 페이지와 동일한 CSS 변수/클래스 체계를 따른다:

```html
<html lang="ko" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{스킬명}}</title>
  <style>
    /* :root CSS 변수는 기존 docs/design-kit/ 페이지(예: accessibility.html)의 :root 블록을 그대로 복사하라.
       값을 임의로 변경하거나 새로 정의하지 않는다. */
    /* 기존 클래스: .page, .hero, .hero-badge, .section-label, .section-title, .section-desc, .card, .grid-2/.grid-3, .table-wrap, table, .badge 등도 기존 페이지에서 그대로 복사하여 재사용 */
  </style>
</head>
<body>
  <div class="page">
    <section class="hero">
      <div class="hero-badge">{{카테고리}}</div>
      <h1>{{스킬명}}</h1>
      <p class="hero-desc">{{한 줄 설명}}</p>
    </section>

    <section>
      <div class="section-label">WORKFLOW</div>
      <div class="section-title">워크플로우 위치</div>
      <!-- 전체 흐름 다이어그램, 현재 스킬 하이라이트 -->
    </section>

    <section>
      <div class="section-label">TEMPLATE</div>
      <div class="section-title">산출물 템플릿</div>
      <!-- 템플릿 구조 설명 -->
    </section>

    <section>
      <div class="section-label">EXAMPLE</div>
      <div class="section-title">예시: TaskFlow</div>
      <!-- TaskFlow 프로젝트 기준 실제 예시 -->
    </section>

    <section>
      <div class="section-label">NEXT</div>
      <div class="section-title">다음 단계</div>
      <!-- 다음 스킬 안내 -->
    </section>
  </div>
</body>
</html>
```

### 2-1. design-concept.html

- 워크플로우: `[design-concept] → design-system → design-mockup → design-component`
- 템플릿 구조: concept.md 포맷 설명
- 예시: TaskFlow 컨셉 — "미니멀, 뉴트럴 warm, sans-serif, 사이드바 대시보드"
- 무드보드 HTML 스크린샷/임베드
- 다음 단계: `/design-system`으로 토큰 정의 또는 `/design-reference`로 레퍼런스 수집

### 2-2. design-reference.html

- 워크플로우: `design-concept → [design-reference] → design-system → design-mockup`
- 템플릿 구조: references.md + catalog HTML 포맷 설명
- 예시: TaskFlow 기준 30개 레퍼런스 중 대표 3-5개 (갤러리/프로덕트/DS 각 1-2개)
- 카탈로그 HTML 스크린샷
- 다음 단계: `/design-mockup`으로 시안 생성

### 2-3. design-mockup.html

- 워크플로우: `design-concept → design-system → [design-mockup] → design-component`
- 템플릿 구조: mockup.html 포맷 + ID 시스템 설명
- 예시: TaskFlow 대시보드 시안 1개 (인터랙티브 ID 오버레이 데모 포함)
- 다음 단계: `/design-component`로 컴포넌트 정의 또는 Figma 전송

### 2-4. design-component.html

- 워크플로우: `design-concept → design-system → design-mockup → [design-component]`
- 템플릿 구조: catalog.md 포맷 설명
- 예시: TaskFlow에서 버튼(Button)과 태스크 카드(TaskCard) 2개 컴포넌트의 완성된 정의
- 다음 단계: toolkit 플러그인으로 실제 코드 구현

---

## 3. index.html 업데이트

사이드바 `categories` 배열에서 "Design Kit — 접근성" 카테고리 바로 뒤 (Backend Kit 카테고리 앞, `docs/index.html:333` 부근)에 삽입:

```javascript
{
  label: 'Design Kit — 워크플로우',
  accent: '#E8965A',
  pages: [
    { id: 'design-concept', title: '디자인 컨셉', file: 'design-kit/design-concept.html' },
    { id: 'design-reference', title: '디자인 레퍼런스', file: 'design-kit/design-reference.html' },
    { id: 'design-mockup', title: '디자인 목업', file: 'design-kit/design-mockup.html' },
    { id: 'design-component', title: '컴포넌트 카탈로그', file: 'design-kit/design-component.html' },
  ]
}
```

---

## 4. SKILL.md 업데이트

각 SKILL.md에 다음 수정을 적용한다:

### design-concept/SKILL.md

**Process 수정:**
- Step 4 현재: "`.design/concept.md`를 생성(또는 갱신)한다:"
- Step 4 수정: "templates/concept.md 포맷으로 `.design/concept.md`를 생성(또는 갱신)한다:"
- Step 5 현재: "`.design/moodboard.html`을 생성한다:"
- Step 5 수정: "templates/moodboard.html 포맷으로 `.design/moodboard.html`을 생성한다:"

**References 섹션 추가:**
```
- `templates/concept.md` — 컨셉 문서 출력 포맷
- `templates/moodboard.html` — 비주얼 무드보드 출력 포맷
```

### design-reference/SKILL.md

**Process 수정:**
- Step 3 현재: "`.design/references.md`를 생성한다:"
- Step 3 수정: "templates/references.md 포맷으로 `.design/references.md`를 생성한다:"
- Step 4 현재: "`.design/reference-catalog.html`을 생성한다:"
- Step 4 수정: "templates/reference-catalog.html 포맷으로 `.design/reference-catalog.html`을 생성한다:"

**References 섹션 추가:**
```
- `templates/references.md` — 레퍼런스 분석 문서 출력 포맷
- `templates/reference-catalog.html` — 비주얼 카탈로그 출력 포맷
```

### design-mockup/SKILL.md

**Process 수정:**
- Step 3 현재: "references/mockup-guidelines.md를 참조하여 시안을 생성한다:"
- Step 3 수정: "references/mockup-guidelines.md를 참조하고 templates/mockup.html 포맷으로 시안을 생성한다:"

**References 섹션 추가:**
```
- `templates/mockup.html` — 시안 HTML 출력 포맷 (ID 오버레이 JavaScript 포함)
```

### design-component/SKILL.md

**Process 수정:**
- Step 3 현재: "컴포넌트 카탈로그를 사용자에게 제시"
- Step 3 수정: "templates/catalog.md 포맷으로 컴포넌트 카탈로그를 생성하고 사용자에게 제시"
- 주의: 이 참조는 무조건적이다. "확정 시"는 저장 시점에만 적용되고 포맷 참조는 생성 시점부터 적용된다.

**References 섹션 추가:**
```
- `templates/catalog.md` — 컴포넌트 카탈로그 출력 포맷
```

---

## 가상 프로젝트: TaskFlow

docs 예시에 사용할 통일 컨텍스트:

- **이름**: TaskFlow
- **성격**: 팀 태스크 관리 SaaS
- **컨셉 키워드**: minimal, warm, professional
- **컬러 방향**: warm neutral 베이스, amber 포인트
- **타이포**: Inter (sans-serif), 3단계 웨이트
- **UI 패턴**: 사이드바 네비게이션, 카드 그리드 대시보드, 플랫 카드, 필드 버튼
- **주요 화면**: 대시보드 (태스크 목록, 상태별 분류, 팀 현황)
