---
name: design-system
description: >
  프로젝트에 디자인 토큰 체계(컬러, 타이포, 스페이싱, 라디우스 등)를 세팅한다.
  기존 디자인 시스템이 있으면 리서치 기준과 비교하여 개선점을 제안한다.
  스택 무관 — 원칙만 정의하고, 구체적 코드 생성은 해당 toolkit에 위임한다.
  "디자인 시스템 세팅", "디자인 토큰", "컬러 팔레트 만들어줘",
  "design system init", "토큰 체계" 같은 요청 시 트리거.
  단순 색상 변경, 기존 토큰 값 수정에는 트리거하지 않는다.
argument-hint: "[project-path]"
user-invocable: true
---

# Gotchas

1. **토큰 네이밍에 구체적 값 금지** — `blue-500` ✗ → `primary` ✓. 값이 바뀌면 이름과 괴리가 생긴다. semantic 네이밍만 사용하라.
2. **스페이싱 스케일 근거 필수** — 4px 베이스가 아니면 반드시 근거를 명시하라. 임의 값(5px, 7px)은 시스템을 깨뜨린다.
3. **다크 모드 선행 설계** — 다크 모드를 고려하지 않고 컬러 토큰을 설계하면 전면 재작업이 필요하다. semantic 토큰(surface, on-surface)을 먼저 정의하라.
4. **스택별 코드 생성 금지** — 이 스킬은 원칙과 토큰 명세만 출력한다. Flutter/React/CSS 코드를 직접 생성하지 마라. 해당 toolkit 플러그인에 위임하라.

# Process

## Step 1: 프로젝트 디자인 시스템 감지

프로젝트 루트에서 디자인 토큰/테마 파일을 탐색한다:

```
# 탐색 패턴 (스택 무관)
**/theme/**
**/tokens/**
**/design/**
**/styles/**
**/colors.*
**/typography.*
```

- 발견되면: HAS_DS=true, 기존 토큰 구조를 분석
- 미발견: HAS_DS=false, 신규 토큰 체계 제안 모드

## Step 2: 토큰 카테고리 정의

references/token-principles.md를 참조하여 카테고리별 토큰을 정의한다:

| 카테고리 | 필수 여부 | 예시 |
|----------|-----------|------|
| Color | 필수 | primary, secondary, surface, on-surface, error |
| Typography | 필수 | display-lg, heading-md, body-sm, label-xs |
| Spacing | 필수 | xs(4), sm(8), md(16), lg(24), xl(32) |
| Radius | 필수 | none(0), sm(4), md(8), lg(16), full(9999) |
| Elevation | 선택 | level-0, level-1, level-2, level-3 |
| Motion | 선택 | duration-fast, duration-normal, easing-standard |

## Step 3: HAS_DS=true → 기존 시스템 분석

기존 토큰을 리서치 기준과 비교하여 리포트 출력:
- 누락된 카테고리
- semantic 네이밍 미준수 항목
- 다크 모드 미대응 토큰
- 스케일 일관성 위반

## Step 4: HAS_DS=false → 토큰 명세 생성

templates/design-tokens.md 포맷으로 토큰 명세를 생성한다.
사용자에게 각 카테고리별 선택지를 제시하고 합의를 받는다.

## Step 5: 산출물 확인

- 토큰 명세 문서가 생성/분석되었는지 확인
- 모든 필수 카테고리가 포함되었는지 확인
- semantic 네이밍 규칙이 준수되었는지 확인

# References

- `references/token-principles.md` — 토큰 설계 원칙 상세
- `templates/design-tokens.md` — 토큰 명세 출력 포맷
