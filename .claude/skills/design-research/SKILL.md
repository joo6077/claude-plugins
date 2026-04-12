---
name: design-research
description: >
  디자인 레퍼런스 소스를 크롤링/분석하여 design-kit/docs/design/ 문서를 갱신한다.
  이 레포 개발용 스킬이며, design-kit 플러그인에 포함되지 않는다.
  "디자인 리서치", "레퍼런스 크롤링", "design research",
  "디자인 문서 갱신" 같은 요청 시 트리거.
argument-hint: "[category or source]"
user-invocable: true
---

# Gotchas

1. **출처 없는 원칙 금지** — 모든 원칙에 인라인 출처 `> **출처:** [이름](URL)`를 반드시 남겨라. 출처가 없는 내용은 작성하지 않는다.
2. **frontmatter 갱신 필수** — 문서 내용을 수정하면 `last_updated`와 `version`을 반드시 업데이트하라.
3. **기존 내용 보존** — 이전 리서치 내용을 덮어쓰지 마라. 업데이트/보완만 한다. 삭제가 필요하면 근거를 커밋 메시지에 명시하라.
4. **수치 없는 원칙 금지** — "적절한 대비를 유지하라" 같은 모호한 표현 금지. 반드시 구체적 수치를 포함하라 (예: "WCAG AA 4.5:1", "최소 44pt 터치 타겟", "200~500ms 애니메이션").
5. **카테고리 미지정 시 전체 순회 금지** — 사용자가 카테고리를 지정하지 않으면 전체를 한 번에 갱신하지 말고 우선순위가 높은 카테고리를 사용자에게 제안하여 확인받아라. 전체 순회는 토큰 소진과 품질 저하를 유발한다.

# Process

## Step 1: 대상 카테고리 결정

사용자가 카테고리를 지정하면 해당 문서만, 미지정이면 전체 design-kit/docs/design/ 순회.

## Step 2: 소스 크롤링

카테고리별 관련 소스를 WebSearch + WebFetch로 조사한다:

| 카테고리 | 우선 소스 |
|----------|-----------|
| foundations/ | Apple HIG, Material Design 3, Fluent Design |
| interaction/ | NNGroup, Baymard Institute |
| accessibility/ | WCAG 2.1/2.2, Apple HIG Accessibility |
| systems/ | 각 디자인 시스템 공식 문서 |

추가 소스: Laws of UX, Dribbble/Behance 수상작 분석, Radix/Shadcn/Tailwind 문서.

## Step 3: 분석 및 정리

크롤링 결과를 해당 design-kit/docs/design/ 문서에 반영:
- 각 원칙에 `> **출처:**` 인라인 태그
- 섹션 구조는 기존 스켈레톤을 따름
- 수치/기준값은 명확하게 (예: "4.5:1", "44pt", "200~500ms")

## Step 4: frontmatter 업데이트

수정한 문서의 frontmatter에서:
- `last_updated` → 오늘 날짜
- `version` → patch bump (내용 추가) 또는 minor bump (구조 변경)

## Step 5: 커밋

```bash
git add design-kit/docs/design/
git commit -m "docs(design): [카테고리] 리서치 갱신 — [소스 요약]"
```

# References

- 크롤링 대상 소스 목록은 Process Step 2 테이블 참조
- 기존 design-kit/docs/design/ 문서의 섹션 구조를 따를 것
