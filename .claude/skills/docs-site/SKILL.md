---
name: docs-site
description: >
  플러그인 문서 사이트(docs/)의 HTML 시각 페이지를 생성·관리한다.
  .md 리서치/가이드 소스를 읽어 standalone HTML로 변환하고 index.html에 등록한다.
  생성 후 sprint-contract + qa-evaluator를 실행하여 품질을 보증한다.
  "문서 사이트", "visual docs", "docs site", "HTML 문서 생성",
  "페이지 추가", "docs page" 같은 요청 시 트리거.
  기존 페이지 내용 수정, 단순 오타 수정에는 트리거하지 않는다.
argument-hint: "[plugin-name] [page-name]"
user-invocable: true
---

# Gotchas

1. **외부 리소스 금지** — 페이지는 반드시 standalone HTML이어야 한다. 외부 CSS/JS/font CDN 링크를 절대 추가하지 마라. 모든 스타일은 `<style>` 내 인라인.
2. **index.html 등록 필수** — 페이지를 생성했는데 `docs/index.html`의 `categories` 배열에 등록하지 않으면 네비게이션에 표시되지 않는다. 아이콘도 `getIcon()` 함수에 추가해야 한다.
3. **플러그인 accent 컬러 준수** — `references/css-tokens.md`의 플러그인별 accent 매핑을 따라라. Harness에 Design Kit 컬러를 쓰면 안 된다.
4. **iframe 경로는 index.html 기준 상대경로** — `docs/index.html`에서 iframe으로 로드하므로 `file` 값은 `design-kit/typography-scale.html` 형태여야 한다.
5. **sprint contract + QA 필수** — 페이지 추가 후 반드시 `/sprint-contract` → 구현 → qa-evaluator 순서를 수행한다. QA 없이 완료 선언하지 마라.
6. **design-kit 원칙 적용 필수** — HTML 생성 시 design-kit의 디자인 원칙을 반드시 따른다. 특히 `design-kit/skills/design-audit/references/audit-criteria.md`의 7개 카테고리(Typography, Color, Spacing, Accessibility, Interaction, Motion, Authenticity) 기준을 충족해야 한다. 생성 후 `/design-audit`으로 검증하라.
7. **1 문서 = 1 페이지 원칙** — 리서치 문서 N개가 있으면 HTML 페이지 N개를 만든다. 여러 문서를 하나로 묶거나 overview 하나로 통합하지 마라. design-kit(22개 주제 → 22개 페이지)이 유일한 기준이다.
8. **최소 콘텐츠 밀도 400줄** — 각 HTML 페이지는 최소 400줄 이상이어야 한다. 167줄짜리 overview는 리서치 문서 내용을 충분히 시각화하지 못한 것이다. hero + 원칙 카드(출처 URL 포함) + 수치 테이블 + 안티패턴 bad/good 비교 + Gotchas 체크리스트는 필수 섹션이다.
9. **원칙 카드에 출처 URL 누락 금지** — 모든 원칙 카드 하단에 `<a class="card-source" href="URL">출처명</a>` 링크 필수. 리서치 문서의 `> **출처:**` 인용을 HTML로 옮겨라. QA가 가장 자주 REJECT하는 항목이다.
10. **가로 오버플로 4 규칙은 하드 제약** — Step 4 에서 페이지별 CSS 를 직접 쓸 때도 아래를 **반드시** 포함한다. 이 규칙이 없어 146 페이지 중 66 개가 375px 에서 오버플로했다. 템플릿을 골격으로만 쓰고 bespoke CSS 를 쓰는 구조라, 템플릿에 있다는 것만으로는 전파되지 않는다.
    - **grid/flex 자식에 `min-width:0`** — 기본값 `auto`(= min-content)가 긴 코드·표·안 끊기는 토큰의 최소폭을 트랙 폭으로 전파시킨다. 그 페이지의 **실제 그리드 클래스명**에 적용하라 (`.grid-2` 가 아니라 `.cards` 일 수 있다).
    - **표는 `<div class="table-wrap">` 로 감싸라** — `.table-wrap{overflow-x:auto;max-width:100%}` + `.table-wrap>table{min-width:max-content}`.
    - **`pre{overflow-x:auto;max-width:100%}`** — `white-space:pre` 의 내용폭이 전파되지 않게 한다.
    - **좁은 뷰포트 단일 컬럼 스택** — `@media(max-width:600px){ <그리드클래스>{grid-template-columns:1fr} }`.
11. **오버플로를 잘라서 없애지 마라** — `overflow:hidden` / `overflow-x:hidden` / `display:none` 으로 억제하는 것은 내용 손실이므로 FAIL 이다. 특히 `body`/`html` 에 `overflow-x:hidden` 을 걸면 증상만 가려지고 원인이 남는다. 표·코드는 **끝까지 스크롤 도달 가능**해야 한다.
12. **경계값 튜닝 금지** — 페이지별 고유 하드코딩 폭(`width:340px` 류)으로 맞추지 마라. CI(Linux)가 로컬(macOS)보다 나쁘게 렌더된다 (실측: 오버플로 CI 11 / 로컬 7). **0px 를 목표로** 하라.
13. **테마 토글을 넣으면 영속화까지** — `localStorage` 키는 `dk-theme` 로 통일하고 로드 시 복원 IIFE 를 넣는다. 저장값이 없으면 `prefers-color-scheme` 을 따른다. 키를 새로 만들지 마라 (현재 레포에 `dk-theme`/`theme`/`vs-theme`/`cp-theme` 4 종이 갈려 있다).

# Process

## Step 1: 대상 식별

사용자 요청에서 플러그인명과 페이지명을 파악한다:

| 플러그인 | 소스 위치 | 출력 위치 |
|----------|-----------|-----------|
| harness | `harness/docs/guides/`, `harness/references/` | `docs/harness/` |
| flutter-toolkit | `flutter-toolkit/references/` | `docs/flutter-toolkit/` |
| design-kit | `design-kit/docs/design/` | `docs/design-kit/` |
| backend-kit | `docs/backend/` | `docs/backend-kit/` |
| infra-kit | `docs/infra/` | `docs/infra-kit/` |
| tone-kit | `docs/tone/` | `docs/tone-kit/` |
| process | (공유) | `docs/process/` |

신규 킷이면 `references/css-tokens.md`의 플러그인 매핑에 새 accent를 추가한 뒤 진행한다.

## Step 2: 페이지 개수 결정

**원칙: 리서치 문서 1개 = HTML 페이지 1개.**

design-kit 패턴이 유일한 기준이다. 22개 리서치 문서가 있으면 22개 페이지를 만든다. 12개면 12개. 4개면 4개.

**문서를 묶거나 단일 overview로 만들지 마라.** 콘텐츠 밀도가 떨어지고 네비게이션에서 찾기 어려워진다.

예시:
- design-kit 22개 문서 → 22개 페이지 (color.md → color-palette.html)
- backend-kit 12개 문서 → 12개 페이지 (api-design.md → api-design.html, database.md → database.html ...)
- infra-kit 12개 문서 → 12개 페이지

페이지 파일명은 소스 .md 파일명과 일치시키거나 더 서술적으로 변경하되, 1:1 매핑을 유지한다.

## Step 3: 소스 .md 읽기

해당 .md 파일을 읽어 핵심 내용을 파악한다:
- 제목, 버전, 주요 섹션
- 표, 코드 블록, 다이어그램 요소
- 원칙 리스트와 출처 URL (반드시 HTML에 옮겨야 함)
- 수치 기준, 안티패턴, Gotchas
- 다른 문서와의 참조 관계

## Step 4: HTML 생성

`references/page-template.html`을 골격으로 사용한다:
- `:root`의 `--accent`/`--accent2`를 `references/css-tokens.md`의 플러그인 매핑에 따라 설정
- `.md` 내용을 시각적 HTML 섹션으로 변환 (카드, 테이블, 비교 패널, 체크리스트 등)
- 제목에 `h1` + gradient, 섹션에 `.section-label`, 내용에 `.card` + `.grid-2/3` 패턴 사용

### design-kit 원칙 적용

`design-kit/skills/design-audit/references/audit-criteria.md`를 읽고 다음을 준수한다:
- **Typography**: 타이포 스케일 일관성, line-height 1.2~1.6배, 본문 최소 16px
- **Color**: 텍스트/배경 대비 WCAG AA 4.5:1 이상, 시맨틱 토큰 사용
- **Spacing**: 스페이싱 스케일 일관성, 같은 레벨 요소 동일 간격
- **Accessibility**: 색상 대비 AA, 포커스 인디케이터
- **Interaction**: 인터랙티브 요소에 시각적 피드백 존재, 상태 전환 가시성
- **Motion**: 애니메이션 200~500ms 범위, prefers-reduced-motion 대응
- **Authenticity**: 연속 섹션 동일 구조 3회 반복 금지, 레이아웃 변주

## Step 5: 파일 저장 + index.html 등록

1. `docs/{plugin-name}/{page-name}.html`에 저장
2. `docs/index.html`의 해당 플러그인 카테고리에 페이지 항목 추가:
   ```javascript
   { id: '{page-name}', title: '{한국어 제목}', file: '{plugin-name}/{page-name}.html' }
   ```
3. `getIcon()` 함수에 SVG 아이콘 추가

## Step 6: 자가 검증

Sprint Contract 전에 다음을 확인한다:
1. Glob `docs/{plugin-name}/{page-name}.html` → 파일 존재 확인
2. Read `docs/index.html` → categories 배열에 해당 `id` 항목이 추가되었는지 확인
3. Read `docs/index.html` → `getIcon()` 함수에 해당 `id` 키가 존재하는지 확인
4. Grep `:root` → 생성된 HTML의 `--accent` 값이 `references/css-tokens.md`의 플러그인 매핑과 일치하는지 확인
5. **가로 오버플로 실측 (Gotcha 10~12 검증 — 코드에 CSS 가 있다는 것은 증거가 아니다)**

   생성한 페이지를 브라우저로 열어 실제 값을 측정한다. `375px` 에서 `> 2` 면 FAIL:

   ```bash
   node -e '
   const { chromium } = require(process.cwd() + "/node_modules/playwright-core");
   const files = process.argv.slice(1);
   (async () => {
     const b = await chromium.launch();
     for (const f of files) {
       const ctx = await b.newContext({ viewport: { width: 375, height: 812 } });
       const p = await ctx.newPage();
       const errs = [];
       p.on("console", m => m.type() === "error" && errs.push(m.text()));
       p.on("pageerror", e => errs.push(String(e)));
       await p.goto("file://" + require("path").resolve(f));
       const o375 = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
       await p.setViewportSize({ width: 768, height: 1024 });
       const o768 = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
       console.log(`${o375 <= 2 && o768 <= 2 && !errs.length ? "OK  " : "FAIL"} ${f}  375=${o375}px 768=${o768}px errors=${errs.length}`);
       await ctx.close();
     }
     await b.close();
   })();
   ' docs/{plugin-name}/{page-name}.html
   ```

   FAIL 이면 Gotcha 10 의 4 규칙 중 빠진 것을 찾아 넣는다. **`overflow:hidden` 으로 덮지 마라** (Gotcha 11).

하나라도 실패하면 수정 후 재검증한다.

## Step 7: Sprint Contract + QA

1. `/sprint-contract` 실행 — 페이지 존재, iframe 로딩, 컬러 토큰 정합성 등 조건 정의
2. 구현 완료 확인
3. `qa-evaluator` 실행 — 계약 기준 APPROVE/REJECT

# References

- `references/page-template.html` — HTML 페이지 골격 템플릿
- `references/css-tokens.md` — Claude 컬러 시스템 + 플러그인별 accent 매핑
- `design-kit/skills/design-audit/references/audit-criteria.md` — 디자인 감사 7개 카테고리 기준
