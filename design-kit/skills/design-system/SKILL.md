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

1. **토큰 네이밍에 구체적 값 금지** — `blue-500`, `primary-blue` ✗ → `color.text.primary`, `color.background.brand` ✓. 값이 바뀌면 이름과 괴리가 생기고, 리브랜딩/다크모드 전환 때 즉시 무너진다.
2. **semantic 없이 primitive만 쓰면 안 됨** — `color.green.500`을 컴포넌트에 직접 연결하면 테마 교체가 불가능해진다. 반드시 `primitive → semantic(alias) → component` 3계층을 거쳐야 한다.
3. **다크모드를 토큰 이름에 박지 마라** — `color-dark-text-primary`, `color-light-surface` ✗. 이러면 소비자가 theme-conditional이 된다. semantic 토큰 하나에 mode별 값을 매핑하는 것이 정석이다.
4. **스케일 없이 임의 수치 추가 금지** — `10px, 14px, 18px, 22px`처럼 임의 spacing/radius가 쌓이면 시스템이 무너진다. `2/4/8/12/16/24/32`처럼 유한한 scale을 먼저 확정하고 그 밖은 거부하라.
5. **컴포넌트 토큰을 글로벌처럼 재사용하지 마라** — `button.primary.background`를 다른 컴포넌트에서 끌어 쓰면 결합도가 올라간다. 여러 컴포넌트에 공통으로 필요할 때만 semantic global로 승격하라.
6. **typography는 개별 수치보다 묶음 토큰** — `font-size-14`, `line-height-20`을 각각 쓰면 조합 오류가 생긴다. `font.body.medium`처럼 size/weight/line-height를 묶은 semantic style token을 우선 제공하라.
7. **스페이싱 base 근거 명시 필수** — 4px base가 아니면 반드시 근거를 문서화하라. base 숫자보다 "허용 scale만 사용하는 일관성"이 더 중요하다.
8. **DTCG 금지 문자 사용 주의** — 토큰 이름에 `.` `{` `}` `$` 같은 DTCG 예약 문자를 섞으면 파서 오류가 난다. 경로 구분은 `/` 또는 `.`만 사용하고, `$` 접두사는 메타 키(`$value`, `$type`)에만 허용된다.
9. **스택별 코드 생성 금지** — 이 스킬은 원칙과 토큰 명세만 출력한다. Flutter/React/CSS 코드를 직접 생성하지 마라. 해당 toolkit 플러그인에 위임하라.
10. **DTCG `$extends` 그룹 상속 활용** — DTCG 2025.10에서 추가된 `$extends` 키워드로 그룹 간 deep merge 상속이 가능하다. 동일한 primitive 값을 여러 semantic 그룹에서 반복 정의하지 말고, 공통 그룹을 만들어 `$extends`로 참조하라. 순환 참조는 금지되며 파서가 감지해야 한다. 출처: research-log §A.
11. **HTML 예시 `:root` CSS 변수는 design-kit 기존 파일과 정합해야 한다** — Step 4에서 토큰 명세 예시로 HTML 스니펫을 포함할 경우, `:root { --color-*: ...; }` 값이 `design-kit/docs/` 또는 `design-kit/templates/` 내 기존 HTML 파일의 CSS 변수 값과 일치해야 한다. 값 불일치는 시스템 분열의 시작이며 실제 REJECT 사유였다 (AR-06). 새 변수를 추가할 때는 기존 파일에도 동시에 반영하거나 불일치 이유를 명시하라.
12. **컬러 primitive는 OKLCH 권장 (2026 표준)** — Tailwind CSS v4(2026 Production Ready)가 기본 팔레트를 HSL→OKLCH로 전환했고, shadcn/ui v4도 HSL→`oklch()` 전환을 완료했다. OKLCH는 지각적 lightness(L)·chroma(C)·hue(H) 축으로 램프가 균일하고 P3 wide gamut을 활용해 sRGB 제약을 풀 수 있다. primitive 정의 시 `oklch(L% C H)` 표기를 우선하고, 레거시 브라우저 fallback이 필요하면 sRGB hex를 병기하라. **브라우저 지원:** Safari 16.4+ / Chrome 111+ / Firefox 128+ (Tailwind v4 지원 범위와 동일). **Figma 주의:** Figma Variables는 OKLCH 미지원이라 hex 근사치를 병기하는 것이 관행(Obra shadcn kit 등). 출처: [Tailwind v4 blog](https://tailwindcss.com/blog/tailwindcss-v4), [shadcn Tailwind v4](https://ui.shadcn.com/docs/tailwind-v4), [Evil Martians OKLCH](https://evilmartians.com/chronicles/better-dynamic-themes-in-tailwind-with-oklch-color-magic), [MDN oklch()](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/oklch).
13. **Enumerate-before-Act — 토큰 수정 전 전수 나열 필수** — 기존 디자인 시스템 개선 요청(예: "다크모드 대응해줘", "semantic 토큰 정리해줘") 시 편집 전에 반드시 아래 순서로 enumerate 한다. (1) 기존 token 파일 전체 목록 + 카테고리별 개수, (2) Tier 1 primitive / Tier 2 semantic / Tier 3 component 분포, (3) 누락 카테고리 · 네이밍 위반 · 다크모드 미대응 항목을 **위반 리스트** 로 제시, (4) 사용자 승인 후 편집. 일부만 수정하고 "이후는 따라 하면 됩니다" 로 넘기는 안티패턴을 방지한다 (insights-report #1 "Proactive quality gaps" 대응 · skill-design-guide §5.5 Enumerate-before-Act 원칙).
14. **DTCG v1 스키마 준수 — alias 는 중괄호 참조다** — Design Tokens Community Group이 2025-10-28에 **Design Tokens Format Module 2025.10**을 첫 stable "Final Community Group Report"로 공개했다 (DTCG v1). JSON 포맷은 `$value`, `$type`, `$description` prefix를 사용하며, 그룹 객체(`$value` 없음)는 그룹 단위 `$type` 기본값을 설정할 수 있다. `$extensions`는 툴 벤더 메타데이터, `$schema`는 validation 용이다.

    **alias 표기 (자주 틀리는 지점):** 스펙의 참조 문법은 **중괄호로 감싼 문자열** `{group.token}` 이다. Gotcha 8 이 `{` `}` 를 금지하는 것은 **토큰 이름**에 대한 규칙이며, 중괄호가 참조 래퍼로 예약돼 있기 때문이다 — 참조 **값**에는 중괄호를 반드시 쓴다. 두 규칙은 충돌하지 않는다. 맨몸 dot-notation 문자열(`"color.background.surface"`)은 참조가 아니라 그냥 문자열 값으로 해석된다. 중괄호 참조는 **완전한 토큰(`$value` 를 가진 객체)만** 가리킬 수 있고, 토큰 값 내부의 개별 속성을 가리키려면 JSON Pointer(RFC 6901) 형식의 `$ref`(`#/path/to/target`)를 쓴다.

    ```json
    {
      "color": {
        "brand": { "$type": "color", "$value": { "colorSpace": "srgb", "components": [0, 0.4, 0.8], "hex": "#0066cc" } },
        "surface": { "$value": "{color.brand}" }
      }
    }
    ```

    **금지:** legacy `value`/`type` 키(prefix 없음), 커스텀 `$` prefix 키, 중괄호 없는 맨몸 dot-notation alias. color 토큰 값은 `colorSpace` / `components` / `hex`(선택) / `alpha`(선택) 를 가진 객체 구조를 쓴다 — hex 문자열 단독 형식은 스펙에 없다. Tokens Studio / Style Dictionary / zeroheight 등 다운스트림 도구가 이 포맷을 가정한다. 출처: [W3C DTCG v1 announcement 2025-10-28](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/), [W3C Final Report](https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/), [DTCG Format Module (drafts)](https://www.designtokens.org/TR/drafts/format/), [Tokens Studio DTCG vs Legacy](https://docs.tokens.studio/manage-settings/token-format).

15. **기존 앱 색상을 새 팔레트로 갈아엎지 마라 (Visual Source of Truth Precedence)** — 이미 색상 체계가 돌아가고 있는 프로젝트에 토큰을 도입할 때, 리서치 기반 "더 나은" 팔레트를 새로 생성하지 마라. **먼저 기존에 실제 사용 중인 값을 전수 추출해 제시**하고, 그 값을 토큰으로 감싸는 것을 기본안으로 삼는다. 값 자체를 바꾸는 것은 별도 제안이며 사용자 승인이 필요하다. 사용자가 브라우저에서 확인하고 승인한 시안 색상(`.design/approvals/` 기록)이 있으면 그것이 프로젝트 팔레트보다 **우선**한다 — 승인된 값을 단일 tint 나 기존 accent 토큰으로 정규화하는 것은 회귀다. 우선순위 표: `../../references/visual-change-protocol.md` §1.

    ```text
    Bad:  "배경색 토큰을 정의했습니다" (기존 앱 배경을 읽지 않고 새 뉴트럴 램프 생성)
          → "배경색 아직도 이상함, 원래 사용하던 색들이 있을거 아니야?"
    Bad:  승인된 시안의 accent → 프로젝트 accent 토큰으로 치환 → "왜 다른 색을 쓰는건데"
    Good: 기존 값 전수 추출 → 표로 제시 → "이 값들을 semantic 토큰으로 감싸겠습니다.
          값 조정이 필요한 항목이 있으면 알려주세요"
    ```

16. **부분 변경 요청은 그 토큰만 — 주변 값 동시 조정 금지** — "이 보더 색만 진하게", "surface 만 한 단계 어둡게" 같은 요청에서 지목되지 않은 토큰(배경, fill, 텍스트, radius, elevation)을 함께 조정하지 마라. 램프 일관성을 이유로 인접 스텝까지 재계산하는 것도 요청 범위 밖이다. 편집 전에 `변경 / 보존` 목록을 남기고, 편집 후 보존 목록의 값이 그대로인지 확인한다. 의도 외 토큰이 변했으면 되돌리고 지목된 것만 다시 적용한다. "색은 지금이 맞는데 그라디언트만 이전으로" 같은 부분 롤백은 지목된 축만 되돌린다. 상세: `../../references/visual-change-protocol.md` §2.

17. **요청한 토큰 카테고리만 정의 — 풀 시스템 스캐폴딩 임의 확장 금지** (insights-report #1 스코프 오독 · #3 과잉설계 대응) — "컬러 팔레트만 만들어줘", "spacing scale 잡아줘" 처럼 **특정 카테고리** 만 요청받으면 그 카테고리만 정의하라. 요청하지 않은 typography·radius·elevation·motion 토큰까지 전체 체계를 한꺼번에 스캐폴딩하지 마라. "완전한 토큰 체계" 요구(다른 Gotcha의 3계층·semantic 강제)는 **요청된 카테고리 내부의 완전성**을 의미하지, 카테고리 자체의 임의 확장을 의미하지 않는다. 범위가 모호하면 추측해서 확장하지 말고 "컬러만 정의할지, 전체 토큰 체계를 세팅할지" 한 줄로 확인하라. 확장 제안이 가치 있다고 판단되면 산출물에 박지 말고 "추가로 typography/spacing 토큰도 세팅을 권장합니다 — 진행할까요?" 형태의 **별도 제안**으로 분리하라. 3계층(primitive→semantic→component) 풀 빌드도 마찬가지다 — 2026 리서치 기준 대부분의 팀은 primitive+semantic 2계층으로 충분하며 component 토큰 계층은 엔터프라이즈 규모에서만 필요하다. 요청·규모 근거 없이 3계층을 기본 출력하지 마라. 출처: [zeroheight Design Systems Report 2026](https://report.zeroheight.com/) (two-tier가 실무 표준, full three-tier는 절반 정도 팀만), material-design.md:273 (점진적 도입).

# Process

## Step 1: 프로젝트 디자인 시스템 감지

프로젝트 루트에서 디자인 토큰/테마 파일을 탐색한다:

```text
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

## Step 2: 3계층 토큰 아키텍처 설계

모든 토큰은 아래 3계층으로 분리한다. 계층을 건너뛰어 연결하지 않는다.

```text
Tier 1 — Primitive (값 저장소)
  예: color.palette.green.500 = #22c55e
      space.scale.4 = 4px

Tier 2 — Semantic (역할/의도 alias)
  예: color.text.success → {color.palette.green.500}
      color.background.surface → {color.palette.neutral.50}  (light mode)
      color.background.surface → {color.palette.neutral.900} (dark mode)

Tier 3 — Component (컴포넌트 예외 오버라이드)
  예: button.primary.background → {color.background.brand}
      card.border.radius → {radius.md}
  ※ 여러 컴포넌트에 공통으로 필요해질 때만 Tier 2로 승격
```

카테고리별 필수/선택 및 semantic 네이밍 기준:

| 카테고리 | 필수 여부 | Semantic 예시 | Scale 기준 |
|----------|-----------|---------------|------------|
| Color | 필수 | text.primary, text.secondary, text.disabled, background.surface, background.brand, border.default, border.subtle | — |
| Typography | 필수 | font.display.lg, font.heading.md, font.body.sm, font.label.xs (size+weight+line-height 묶음) | Modular Scale 비율 권장 (1.125 Major Second ~ 1.618 Golden Ratio). Fluid: `clamp(min, preferred, max)` |
| Spacing | 필수 | space.xs(4), space.sm(8), space.md(16), space.lg(24), space.xl(32), space.2xl(48) | 4px base. Fluid spacing: `clamp()` 기반 연속 간격도 고려 |
| Radius | 필수 | radius.none(0), radius.sm(4), radius.md(8), radius.lg(16), radius.full(9999) | 유한 scale |
| Elevation | 선택 | elevation.level-0 ~ level-4 (shadow값) | — |
| Motion | 선택 | motion.duration.fast(100ms), motion.duration.normal(200ms), motion.easing.standard | — |

**참고 — Material 3 Expressive (2025-05 발표, Android 16):** MD3 Expressive는 HCT(Hue-Chroma-Tone) 기반 **tonal palette 정교화**로 primary/secondary/tertiary 분리를 강화했고, 46개 연구/18,000명 참가를 근거로 더 풍부한 컬러 토큰 세트와 동적 컬러 개인화를 유지한다. 타이포는 variable font axes(예: Roboto Flex)로 weight/width를 시스템화하고, 모션은 springy 애니메이션으로 표현력을 강화했다. MD3 tonal 구조를 채택할 때는 HCT 톤 스텝을 semantic alias에 매핑하여 primitive로 저장한다. 출처: [Supercharge MD3 Expressive](https://supercharge.design/blog/material-3-expressive), [Dezeen Google Expressive](https://www.dezeen.com/2025/05/28/google-ushers-in-age-of-expressive-interfaces-with-material-design-update/).

## Step 3: HAS_DS=true → 기존 시스템 분석

기존 토큰을 3계층 아키텍처 기준으로 비교하여 리포트 출력:

- **계층 누락**: primitive를 컴포넌트에 직접 연결한 항목
- **네이밍 위반**: 값이 이름에 포함된 토큰 (`blue-500`, `color-dark-*`)
- **다크모드 미대응**: mode alias가 없는 color semantic 토큰
- **스케일 이탈**: 허용 scale 외 임의 수치 사용
- **컴포넌트 토큰 오남용**: component 토큰을 다른 컴포넌트에서 재사용
- **typography 분리 문제**: size/weight/line-height를 개별 토큰으로만 제공하는 경우

## Step 4: HAS_DS=false → 토큰 명세 생성

templates/design-tokens.md 포맷으로 토큰 명세를 생성한다.
사용자에게 아래 순서로 각 카테고리별 선택지를 제시하고 합의를 받는다:

1. 브랜드 컬러 팔레트 (primitive) 확정
2. semantic color 토큰 — light/dark 양쪽 매핑 포함
3. spacing scale (4px base 기본, 변경 시 근거 명시)
4. typography 스타일 토큰 묶음
5. radius scale
6. elevation/motion (필요 시)

## Step 5: 산출물 확인

- 모든 필수 카테고리가 3계층으로 구분되었는지 확인
- semantic 토큰이 primitive alias로 정의되었는지 확인 (값 직접 기입 ✗)
- light/dark 양쪽 semantic 매핑이 존재하는지 확인
- 허용 scale 외 임의 수치가 없는지 확인
- component 토큰이 있다면 스코프가 해당 컴포넌트로만 제한되었는지 확인
- **:root CSS 변수 정합성 체크** (Gotcha #11) — 산출물에 HTML `:root` 스니펫이 포함된 경우, `design-kit/docs/` 및 `design-kit/templates/` 내 기존 HTML 파일의 CSS 변수 값과 대조하여 불일치 항목이 없는지 확인한다. 불일치 발견 시 기존 파일을 동시에 갱신하거나 이유를 명시한다.
- **Figma Variables → Tokens Studio → Style Dictionary v4 파이프라인 안내** — 토큰 명세 생성 시, Figma Variables(primitive + semantic) → Tokens Studio DTCG JSON 내보내기 → Style Dictionary v4 플랫폼별 변환 → Git 동기화 파이프라인을 사용자에게 안내한다. Code Syntax 활성화, Description 필드 활용, Scope 제한을 권장한다. 출처: research-log §I.
- **Fluid Typography 가이드** — typography 토큰 정의 시, 고정 크기 외에 `clamp(min, preferred, max)` 기반 fluid scale 옵션을 제시한다. Modular Scale 비율(1.125 Major Second ~ 1.618 Golden Ratio) 중 프로젝트 성격에 맞는 비율을 추천하고, Utopia 접근법(소형/대형 화면 두 스케일 보간)을 참조한다. 출처: research-log §E.
- **Fluid Spacing 가이드** — spacing 토큰에 Fixed(고정) 외에 Fluid(`clamp()`) 및 Adaptive(breakpoint별 전환) 옵션을 제시한다. Internal ≤ External 규칙(요소 내부 여백 ≤ 외부 여백)을 명시한다. 출처: research-log §F.

# References

- `references/token-principles.md` — 토큰 설계 원칙 상세
- `templates/design-tokens.md` — 토큰 명세 출력 포맷
- `../../references/visual-change-protocol.md` — 시각 우선순위 · 부분 변경 격리 (SSOT)
