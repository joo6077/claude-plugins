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

# Process

## Step 1: 대상 식별

사용자 요청에서 플러그인명과 페이지명을 파악한다:

| 플러그인 | 소스 위치 | 출력 위치 |
|----------|-----------|-----------|
| harness | `harness/docs/guides/`, `harness/references/` | `docs/harness/` |
| flutter-toolkit | `flutter-toolkit/references/` | `docs/flutter-toolkit/` |
| design-kit | `design-kit/docs/design/` | `docs/design-kit/` |
| process | (공유) | `docs/process/` |

## Step 2: 소스 .md 읽기

해당 .md 파일을 읽어 핵심 내용을 파악한다:
- 제목, 버전, 주요 섹션
- 표, 코드 블록, 다이어그램 요소
- 다른 문서와의 참조 관계

## Step 3: HTML 생성

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

## Step 4: 파일 저장 + index.html 등록

1. `docs/{plugin-name}/{page-name}.html`에 저장
2. `docs/index.html`의 해당 플러그인 카테고리에 페이지 항목 추가:
   ```javascript
   { id: '{page-name}', title: '{한국어 제목}', file: '{plugin-name}/{page-name}.html' }
   ```
3. `getIcon()` 함수에 SVG 아이콘 추가

## Step 5: 자가 검증

Sprint Contract 전에 다음을 확인한다:
1. Glob `docs/{plugin-name}/{page-name}.html` → 파일 존재 확인
2. Read `docs/index.html` → categories 배열에 해당 `id` 항목이 추가되었는지 확인
3. Read `docs/index.html` → `getIcon()` 함수에 해당 `id` 키가 존재하는지 확인
4. Grep `:root` → 생성된 HTML의 `--accent` 값이 `references/css-tokens.md`의 플러그인 매핑과 일치하는지 확인

하나라도 실패하면 수정 후 재검증한다.

## Step 6: Sprint Contract + QA

1. `/sprint-contract` 실행 — 페이지 존재, iframe 로딩, 컬러 토큰 정합성 등 조건 정의
2. 구현 완료 확인
3. `qa-evaluator` 실행 — 계약 기준 APPROVE/REJECT

# References

- `references/page-template.html` — HTML 페이지 골격 템플릿
- `references/css-tokens.md` — Claude 컬러 시스템 + 플러그인별 accent 매핑
- `design-kit/skills/design-audit/references/audit-criteria.md` — 디자인 감사 7개 카테고리 기준
