# design-kit 산출물 템플릿 + docs site 페이지 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 4개 스킬에 산출물 템플릿을 추가하고, docs site에 TaskFlow 예시 페이지 4개를 생성한다.

**Architecture:** 기존 design-kit 스킬의 templates/ 패턴(design-tokens.md, audit-report.md)을 따라 Markdown 템플릿을 추가. docs HTML 페이지는 기존 design-kit 페이지의 CSS 변수/클래스를 인라인으로 복사하여 일관성 유지.

**Tech Stack:** Markdown, HTML/CSS (인라인, CDN 없음), JavaScript (ID 오버레이)

**Spec:** `docs/superpowers/specs/2026-04-07-design-kit-templates-docs-design.md`

---

## 파일 구조

```
design-kit/skills/
├── design-concept/templates/
│   ├── concept.md                    # 신규
│   └── moodboard.html                # 신규
├── design-reference/templates/
│   ├── references.md                 # 신규
│   └── reference-catalog.html        # 신규
├── design-mockup/templates/
│   └── mockup.html                   # 신규
└── design-component/templates/
    └── catalog.md                    # 신규

design-kit/skills/
├── design-concept/SKILL.md           # 수정 (Process + References)
├── design-reference/SKILL.md         # 수정 (Process + References)
├── design-mockup/SKILL.md            # 수정 (Process + References)
└── design-component/SKILL.md         # 수정 (Process + References)

docs/
├── design-kit/
│   ├── design-concept.html           # 신규
│   ├── design-reference.html         # 신규
│   ├── design-mockup.html            # 신규
│   └── design-component.html         # 신규
└── index.html                        # 수정 (사이드바 카테고리 추가)
```

---

### Task 1: Markdown 템플릿 4개 생성

**Files:**
- Create: `design-kit/skills/design-concept/templates/concept.md`
- Create: `design-kit/skills/design-reference/templates/references.md`
- Create: `design-kit/skills/design-component/templates/catalog.md`
- Create: `design-kit/skills/design-mockup/templates/.gitkeep`

스펙 §1-1, §1-3, §1-6의 Markdown 코드 블록을 그대로 파일로 생성한다. design-mockup은 HTML 템플릿만 있으므로 templates/ 디렉토리에 .gitkeep을 둔다.

- [ ] **Step 1: 디렉토리 생성**

```bash
mkdir -p design-kit/skills/design-concept/templates
mkdir -p design-kit/skills/design-reference/templates
mkdir -p design-kit/skills/design-mockup/templates
mkdir -p design-kit/skills/design-component/templates
```

- [ ] **Step 2: concept.md 생성**

스펙 §1-1의 Markdown 코드 블록 전문을 `design-kit/skills/design-concept/templates/concept.md`에 작성.

- [ ] **Step 3: references.md 생성**

스펙 §1-3의 Markdown 코드 블록 전문을 `design-kit/skills/design-reference/templates/references.md`에 작성.

- [ ] **Step 4: catalog.md 생성**

스펙 §1-6의 Markdown 코드 블록 전문을 `design-kit/skills/design-component/templates/catalog.md`에 작성.

- [ ] **Step 5: .gitkeep 생성**

```bash
touch design-kit/skills/design-mockup/templates/.gitkeep
```

- [ ] **Step 6: 검증**

```bash
ls design-kit/skills/design-concept/templates/concept.md
ls design-kit/skills/design-reference/templates/references.md
ls design-kit/skills/design-component/templates/catalog.md
ls design-kit/skills/design-mockup/templates/.gitkeep
```

- [ ] **Step 7: 커밋**

```bash
git add design-kit/skills/*/templates/
git commit -m "feat(design-kit): 4개 스킬 Markdown 산출물 템플릿 추가

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: HTML 템플릿 3개 생성

**Files:**
- Create: `design-kit/skills/design-concept/templates/moodboard.html`
- Create: `design-kit/skills/design-reference/templates/reference-catalog.html`
- Create: `design-kit/skills/design-mockup/templates/mockup.html`

스펙 §1-2, §1-4, §1-5의 구조를 따라 standalone HTML 템플릿 생성. 모든 HTML은 외부 CDN 없이 인라인 `<style>`로 작성. `{{placeholder}}`로 동적 부분 표시.

- [ ] **Step 1: moodboard.html 생성**

standalone HTML. 스펙 §1-2 구조:
- 헤더: `{{project-name}}` + 무드 키워드 태그
- 컬러 팔레트 섹션: `{{color-direction}}` 방향을 시각화한 스워치 플레이스홀더
- 타이포 섹션: `{{font-family}}` 서체별 샘플 텍스트
- UI 패턴 섹션: `{{layout-pattern}}` 패턴 스케치 플레이스홀더
- 인라인 CSS, CDN 없음

- [ ] **Step 2: reference-catalog.html 생성**

standalone HTML. 스펙 §1-4 구조:
- 헤더: `{{keywords}}` + `{{count}}/{{target}}` 요약
- 필터 바: 소스 채널별 토글 (갤러리/프로덕트/DS) JavaScript
- 카드 그리드: `{{reference-cards}}` 플레이스홀더
- 인라인 CSS, CDN 없음

- [ ] **Step 3: mockup.html 생성**

standalone HTML. 스펙 §1-5 구조:
- `{{mockup-content}}` 시안 콘텐츠 영역
- ID 오버레이 JavaScript:
  - 우하단 토글 버튼 (기본 OFF)
  - 활성화 시 `[id]` 속성이 있는 요소 호버 → 툴팁으로 ID 표시
  - 툴팁 클릭 시 `navigator.clipboard.writeText(id)` 복사
- 인라인 CSS, CDN 없음

- [ ] **Step 4: 검증**

```bash
ls design-kit/skills/design-concept/templates/moodboard.html
ls design-kit/skills/design-reference/templates/reference-catalog.html
ls design-kit/skills/design-mockup/templates/mockup.html
```

- [ ] **Step 5: 커밋**

```bash
git add design-kit/skills/*/templates/*.html
git commit -m "feat(design-kit): 3개 스킬 HTML 산출물 템플릿 추가

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: SKILL.md 4개 업데이트

**Files:**
- Modify: `design-kit/skills/design-concept/SKILL.md`
- Modify: `design-kit/skills/design-reference/SKILL.md`
- Modify: `design-kit/skills/design-mockup/SKILL.md`
- Modify: `design-kit/skills/design-component/SKILL.md`

스펙 §4의 수정 사항을 각 SKILL.md에 적용한다. Process 단계에 templates/ 참조 추가 + References 섹션에 templates/ 파일 경로 추가.

- [ ] **Step 1: design-concept/SKILL.md 수정**

Process Step 4에서 "`.design/concept.md`를 생성(또는 갱신)한다:" → "templates/concept.md 포맷으로 `.design/concept.md`를 생성(또는 갱신)한다:"

Process Step 5에서 "`.design/moodboard.html`을 생성한다:" → "templates/moodboard.html 포맷으로 `.design/moodboard.html`을 생성한다:"

References 섹션에 추가:
```
- `templates/concept.md` — 컨셉 문서 출력 포맷
- `templates/moodboard.html` — 비주얼 무드보드 출력 포맷
```

- [ ] **Step 2: design-reference/SKILL.md 수정**

Process Step 3에서 "`.design/references.md`를 생성한다:" → "templates/references.md 포맷으로 `.design/references.md`를 생성한다:"

Process Step 4에서 "`.design/reference-catalog.html`을 생성한다:" → "templates/reference-catalog.html 포맷으로 `.design/reference-catalog.html`을 생성한다:"

References 섹션에 추가:
```
- `templates/references.md` — 레퍼런스 분석 문서 출력 포맷
- `templates/reference-catalog.html` — 비주얼 카탈로그 출력 포맷
```

- [ ] **Step 3: design-mockup/SKILL.md 수정**

Process Step 3에서 "references/mockup-guidelines.md를 참조하여 시안을 생성한다:" → "references/mockup-guidelines.md를 참조하고 templates/mockup.html 포맷으로 시안을 생성한다:"

References 섹션에 추가:
```
- `templates/mockup.html` — 시안 HTML 출력 포맷 (ID 오버레이 JavaScript 포함)
```

- [ ] **Step 4: design-component/SKILL.md 수정**

Process Step 3에서 "컴포넌트 카탈로그를 사용자에게 제시" → "templates/catalog.md 포맷으로 컴포넌트 카탈로그를 생성하고 사용자에게 제시"

References 섹션에 추가:
```
- `templates/catalog.md` — 컴포넌트 카탈로그 출력 포맷
```

- [ ] **Step 5: 검증**

각 SKILL.md에서 "templates/" 문자열이 Process + References에 존재하는지 확인:
```bash
grep -c "templates/" design-kit/skills/design-concept/SKILL.md
grep -c "templates/" design-kit/skills/design-reference/SKILL.md
grep -c "templates/" design-kit/skills/design-mockup/SKILL.md
grep -c "templates/" design-kit/skills/design-component/SKILL.md
```

Expected: 각각 3 이상 (concept: 4, reference: 4, mockup: 2, component: 2)

- [ ] **Step 6: 커밋**

```bash
git add design-kit/skills/*/SKILL.md
git commit -m "feat(design-kit): SKILL.md에 templates/ 참조 추가

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: docs site — design-concept.html

**Files:**
- Create: `docs/design-kit/design-concept.html`

기존 `docs/design-kit/accessibility.html`의 CSS `:root` 블록과 공통 클래스를 그대로 복사하여 베이스로 사용. 스펙 §2 공통 HTML 스켈레톤 구조를 따른다.

- [ ] **Step 1: 기존 CSS 읽기**

`docs/design-kit/accessibility.html`의 `<style>` 블록 전체를 읽어 `:root` 변수와 공통 클래스를 확보한다.

- [ ] **Step 2: design-concept.html 생성**

스펙 §2-1 + §5(TaskFlow 컨텍스트) 기준:

섹션 구성:
1. **Hero**: "디자인 컨셉" + "프로젝트의 디자인 방향성을 정의하고 비주얼 무드보드로 시각화한다"
2. **Workflow**: `[design-concept] → design-system → design-mockup → design-component` 다이어그램 (현재 스킬 accent 하이라이트)
3. **Template**: concept.md 포맷의 테이블 구조 설명 (무드 키워드, 컬러 방향, 타이포 방향, UI 패턴, 레퍼런스 섹션)
4. **Example**: TaskFlow 컨셉 예시 — minimal/warm/professional 키워드, warm neutral 컬러 방향, Inter sans-serif 타이포, 사이드바 대시보드 UI 패턴. concept.md 템플릿이 채워진 결과물 형태로 표시.
5. **Next**: `/design-system`으로 토큰 정의 또는 `/design-reference`로 레퍼런스 수집 안내

인라인 CSS, CDN 없음, `<html lang="ko" data-theme="dark">`.

- [ ] **Step 3: 검증**

```bash
ls docs/design-kit/design-concept.html
```

- [ ] **Step 4: 커밋**

```bash
git add docs/design-kit/design-concept.html
git commit -m "docs(design-kit): design-concept docs 페이지 추가

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: docs site — design-reference.html

**Files:**
- Create: `docs/design-kit/design-reference.html`

- [ ] **Step 1: design-reference.html 생성**

스펙 §2-2 + §5(TaskFlow) 기준. Task 4에서 사용한 CSS를 동일하게 사용.

섹션 구성:
1. **Hero**: "디자인 레퍼런스" + "실제 프로덕트/서비스의 시각 디자인을 체계적으로 크롤링하고 비주얼 카탈로그로 정리한다"
2. **Workflow**: `design-concept → [design-reference] → design-system → design-mockup` (현재 하이라이트)
3. **Template**: references.md 포맷 + catalog HTML 구조 설명 (3개 소스 채널 테이블, 기본 30개)
4. **Example**: TaskFlow 기준 대표 레퍼런스 5개 — 갤러리 2개(Dribbble SaaS dashboard, Awwwards minimal), 프로덕트 2개(Linear, Notion), DS 1개(shadcn/ui Button). references.md 템플릿이 채워진 테이블로 표시.
5. **Next**: `/design-mockup`으로 시안 생성 안내

- [ ] **Step 2: 커밋**

```bash
git add docs/design-kit/design-reference.html
git commit -m "docs(design-kit): design-reference docs 페이지 추가

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 6: docs site — design-mockup.html

**Files:**
- Create: `docs/design-kit/design-mockup.html`

- [ ] **Step 1: design-mockup.html 생성**

스펙 §2-3 + §5(TaskFlow) 기준.

섹션 구성:
1. **Hero**: "디자인 목업" + "하이파이 HTML 시안 5개를 생성하여 제시한다"
2. **Workflow**: `design-concept → design-system → [design-mockup] → design-component` (현재 하이라이트)
3. **Template**: mockup.html 포맷 설명 — ID 시스템(`{컴포넌트명}-{4자리해시}`), 호버 오버레이, Figma 연동
4. **Example**: TaskFlow 대시보드 시안 1개를 인라인으로 포함. 사이드바 네비게이션 + 카드 그리드 레이아웃. 주요 요소에 ID 부여 (`sidebar-nav-a1b2`, `card-task-c3d4`, `btn-create-e5f6` 등). ID 오버레이 토글 버튼 작동하는 인터랙티브 데모.
5. **Next**: `/design-component`로 컴포넌트 정의 또는 Figma 전송 안내

- [ ] **Step 2: 커밋**

```bash
git add docs/design-kit/design-mockup.html
git commit -m "docs(design-kit): design-mockup docs 페이지 추가

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 7: docs site — design-component.html

**Files:**
- Create: `docs/design-kit/design-component.html`

- [ ] **Step 1: design-component.html 생성**

스펙 §2-4 + §5(TaskFlow) 기준.

섹션 구성:
1. **Hero**: "컴포넌트 카탈로그" + "반복되는 UI 요소를 컴포넌트로 정의하고 카탈로그화한다"
2. **Workflow**: `design-concept → design-system → design-mockup → [design-component]` (현재 하이라이트)
3. **Template**: catalog.md 포맷 설명 — 역할, Variants, 상태, 사이즈, 토큰 매핑, 사용 가이드라인
4. **Example**: TaskFlow 버튼(Button) + 태스크 카드(TaskCard) 2개 컴포넌트 완성된 정의.
   - Button: primary/secondary/ghost variant, 6개 상태(default~focused), sm/md/lg 사이즈, 토큰 매핑
   - TaskCard: default/hover 상태, 제목+상태배지+담당자+기한 구성, 토큰 매핑
5. **Next**: toolkit 플러그인(flutter-toolkit 등)으로 실제 코드 구현 안내

- [ ] **Step 2: 커밋**

```bash
git add docs/design-kit/design-component.html
git commit -m "docs(design-kit): design-component docs 페이지 추가

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 8: index.html 업데이트 + README 동기화

**Files:**
- Modify: `docs/index.html` (~line 333)
- Modify: `design-kit/README.md` (via sync-docs)

- [ ] **Step 1: index.html 사이드바 카테고리 추가**

`docs/index.html`의 `categories` 배열에서 "Design Kit — 접근성" 카테고리 바로 뒤 (Backend Kit 카테고리 앞, ~line 333)에 삽입:

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
},
```

- [ ] **Step 2: sync-docs 실행**

```bash
python scripts/sync-docs.py design-kit
```

- [ ] **Step 3: 검증**

브라우저에서 `docs/index.html` 열어 사이드바에 "Design Kit — 워크플로우" 카테고리가 표시되고 4개 페이지가 로드되는지 확인.

- [ ] **Step 4: 커밋**

```bash
git add docs/index.html design-kit/README.md
git commit -m "docs(design-kit): index.html 워크플로우 카테고리 + README 동기화

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 9: Sprint Contract 검증 + QA

- [ ] **Step 1: 계약 조건 체크**

`.harness/sprint-contract.md`의 16개 조건을 하나씩 검증:

| 조건 | 검증 방법 |
|------|-----------|
| SK-01 | `ls design-kit/skills/*/templates/` |
| SK-02 | `grep -l "{{" design-kit/skills/*/templates/*` |
| SK-03 | `grep "templates/" design-kit/skills/*/SKILL.md` — Process 섹션에 존재 확인 |
| SK-04 | `grep "templates/" design-kit/skills/*/SKILL.md` — References 섹션에 존재 확인 |
| AR-01 | 기존 design-system/templates/design-tokens.md 패턴과 비교 |
| AR-02 | `ls docs/design-kit/design-*.html` |
| AR-03 | `grep "워크플로우" docs/index.html` |
| AR-04 | `grep -l "TaskFlow" docs/design-kit/design-*.html` — 4개 파일 모두 |
| AR-05 | `grep "section-label" docs/design-kit/design-*.html` — WORKFLOW/TEMPLATE/EXAMPLE/NEXT 4개 섹션 |
| AR-06 | 기존 accessibility.html의 CSS 변수와 신규 페이지의 CSS 변수 비교 |
| AP-01 | 버전 하드코딩 없음 확인 |
| AP-02 | `grep -l "cdn\|googleapis\|jsdelivr\|unpkg" docs/design-kit/design-*.html` — 결과 없어야 함 |

- [ ] **Step 2: QA Evaluator 실행**

qa-evaluator 에이전트를 호출하여 최종 APPROVE/REJECT 판정.

- [ ] **Step 3: APPROVE 시 완료, REJECT 시 수정 후 재검증**
