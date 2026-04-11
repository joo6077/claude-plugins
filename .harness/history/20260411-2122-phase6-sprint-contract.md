# Sprint Contract — Phase 6 Kaizen Research Mode (design-kit)

Feature: design-kit 7 스킬 + design-reviewer 에이전트 + references 2026 최신 디자인 시스템 트렌드 반영 카이젠
Created: 2026-04-11
Branch: kaizen/2026-04-11-research
Iteration: 1

## Context

Phase 1~5 완료 (commit 4587154 → 73416ab). Phase 6은 design-kit 플러그인의 7개 스킬(design-guide, design-audit, design-system, design-concept, design-component, design-mockup, design-reference), `agents/design-reviewer.md`, 관련 `references/**` 파일을 2026 최신 디자인 시스템 생태계에 맞춰 갱신한다.

데이터 풀 §1 최근 REJECT 사유 — SK-06: `concept.md` Accent 행에 `#E8965A` 구체 hex 확정값 기재 — Gotcha #3 위반. 현재 `design-concept/SKILL.md` Gotcha #3가 이미 서술형 방향만 허용 + Good/Bad 예시를 포함하고 있으나, **Step 4 완료 직후 자동 검증 체크포인트**가 없어 Claude가 실제로 놓칠 수 있다. 재발 방지용 검증 명령 추가 필요.

데이터 풀 §5 validate-plugin 스냅샷 — design-kit v0.2.0, 7 skills + 1 agent, V1~V7 전부 OK. 회귀 금지 기준선.

외부 리서치 (Codex rescue + WebSearch, 2026-04-11):

- **OKLCH / Tailwind v4 / shadcn**: Tailwind CSS v4 (2026 Production Ready, v4.1.18+)이 전체 기본 팔레트를 **OKLCH**로 전환. `@theme` / `@theme inline` directive. shadcn/ui의 v4 integration도 HSL→OKLCH (`--background` 등 semantic 토큰을 `oklch()`로 직접 정의). P3 wide gamut 활용으로 sRGB 제약 해제. 브라우저: Safari 16.4+/Chrome 111+/Firefox 128+. Figma Variables는 OKLCH 미지원이라 hex 근사치 병기가 관행 (Obra shadcn kit) ([Tailwind v4 blog](https://tailwindcss.com/blog/tailwindcss-v4), [shadcn Tailwind v4](https://ui.shadcn.com/docs/tailwind-v4), [Evil Martians OKLCH](https://evilmartians.com/chronicles/better-dynamic-themes-in-tailwind-with-oklch-color-magic), [MDN oklch()](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/oklch))

- **DTCG v1 Stable (2025-10-28)**: Design Tokens Community Group이 2025-10-28에 **Design Tokens Format Module 2025.10**을 "Final Community Group Report"로 공개 — DTCG v1 첫 stable version (단, W3C Recommendation은 아님). 포맷: `$value`, `$type`, `$description` prefix, 그룹 단위 `$type` 기본값, alias는 dot notation 문자열, `$extensions` 메타데이터, `$schema` validation. Tokens Studio for Figma가 legacy vs DTCG v1 선택 가능하며 Style Dictionary / zeroheight 등 다운스트림 도구는 DTCG JSON 가정. Figma 자체도 DTCG 1.0 호환 native variable import/export 로드맵 ([W3C DTCG v1 announcement](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/), [W3C Final Report 2025-10-28](https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/), [Design Tokens Format Module 2025.10](https://www.designtokens.org/tr/drafts/format/), [Tokens Studio DTCG vs Legacy](https://docs.tokens.studio/manage-settings/token-format))

- **WCAG 2.2 신규 SC** (2023-10 W3C Recommendation, 2026 기준 AA 컴플라이언스 타겟):
  - **SC 2.5.8 Target Size (Minimum) — AA 24×24 CSS px** (예외: sufficient spacing / inline text / user-agent / essential). 기존 SC 2.5.5 Enhanced 44×44 CSS px는 여전히 AAA. Apple HIG 44pt는 터치 디바이스 실용 권장치이지 WCAG 2.2 AA 요구는 24 CSS px.
  - **SC 2.4.11 Focus Not Obscured (Minimum) — AA** — 키보드 포커스가 author content로 완전히 가려지지 않아야 함 (부분 가림 허용)
  - **SC 2.4.12 Focus Not Obscured (Enhanced) — AAA** — 전혀 가려지지 않음
  - **SC 2.4.13 Focus Appearance — AAA** — 포커스 인디케이터 최소 크기/대비 명시
  - **SC 2.5.7 Dragging Movements — AA**, **SC 3.2.6 Consistent Help — A**, **SC 3.3.7 Redundant Entry — A**, **SC 3.3.8 Accessible Authentication (Minimum) — AA** ([W3C WCAG 2.2 What's New](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/), [W3C WCAG 2.2 TR](https://www.w3.org/TR/WCAG22/), [Deque University WCAG 2.2](https://dequeuniversity.com/resources/wcag-2.2/))

- **APCA / WCAG 3 상태**: WCAG 3.0은 2026 현재 Working Draft이며 Recommendation은 2028~2030 예상. **WCAG 2.2 AA가 2026 컴플라이언스 타겟**이며 APCA는 보조 체크(대규모 리프레시, 다크 모드, 작은 텍스트 튜닝)로 권장. APCA는 폰트 크기·굵기·극성을 고려한 지각 대비 Lc 점수(body min Lc 60, preferred Lc 75, body text Lc 90 thresholds) ([WCAG 3 status 2026](https://web-accessibility-checker.com/en/blog/wcag-3-0-guide-2026-changes-prepare), [Eric Eggert WCAG 3 not ready](https://yatil.net/blog/wcag-3-is-not-ready-yet), [APCA easy intro](https://git.apcacontrast.com/documentation/APCAeasyIntro.html))

- **Material Design 3 Expressive** (2025-05 발표, Android 16): HCT(Hue-Chroma-Tone) 기반 **tonal palette 정교화**, 46개 연구/18,000명 참가 근거. 더 풍부한 컬러 토큰 세트 + 동적 컬러 개인화 유지하면서 primary/secondary/tertiary 분리 강화. 타이포는 variable font axes (예: Roboto Flex)로 weight/width 시스템화. 모션은 springy 애니메이션 ([Supercharge MD3 Expressive](https://supercharge.design/blog/material-3-expressive), [Dezeen Google Expressive](https://www.dezeen.com/2025/05/28/google-ushers-in-age-of-expressive-interfaces-with-material-design-update/), [developer.android.com design language](https://developer.android.com/design/ui/wear/guides/get-started/design-language))

- **Container Queries 2026**: MDN 기준 "Baseline – widely available", Chrome 105+/Firefox 110+/Safari 16+ 95%+ 커버리지. `container-type: inline-size;` + named containers + `@container` scoped rules. Self-Aware 컴포넌트 아키텍처 핵심. 글로벌 레이아웃/OS 레벨(reduced-motion, color-scheme)은 media query, 컴포넌트 내부는 container query 하이브리드 권장. `block-size`/`size` 쿼리는 layout loop 위험 → `inline-size` 권장 ([MDN CSS Container Queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_container_queries), [LogRocket container queries 2026](https://blog.logrocket.com/container-queries-2026/), [web.dev container queries](https://web.dev/blog/how-to-use-container-queries-now))

- **Apple Liquid Glass / HIG 2026** (참고): 2025-06 iOS 26/iPadOS 26/macOS Tahoe/watchOS 26/tvOS 26/visionOS 통합 software design update. Liquid Glass는 visionOS 영감 dynamic translucent material — 실시간 specular highlight, light/dark 자동 대응. HIG Materials 가이드는 Liquid Glass를 controls/navigation 레이어에 한정하고 content 레이어는 standard materials 유지 권장 (hierarchy 보전). 이번 Phase에서는 "참고"로만 간략히 노출 ([Apple Newsroom Liquid Glass](https://www.apple.com/newsroom/2025/06/apple-introduces-a-delightful-and-elegant-new-software-design/), [Apple HIG Materials](https://developer.apple.com/design/human-interface-guidelines/materials))

## Scope

### 수정 대상

- `design-kit/skills/design-concept/SKILL.md`
- `design-kit/skills/design-system/SKILL.md`
- `design-kit/skills/design-audit/SKILL.md`
- `design-kit/skills/design-guide/SKILL.md`
- `design-kit/skills/design-component/SKILL.md`
- `design-kit/skills/design-mockup/SKILL.md`
- `design-kit/skills/design-reference/SKILL.md` (검토 후 필요 시)
- `design-kit/agents/design-reviewer.md`
- `design-kit/skills/design-system/references/token-principles.md`
- `design-kit/skills/design-audit/references/audit-criteria.md`

### 수정 금지 (Phase 1~5 파일 / 범위 외)

- `harness/**` (Phase 1~4)
- `flutter-toolkit/**` (Phase 5)
- `design-kit/docs/design/**` — 범위 외 (docs 갱신은 `/design-research` 스킬 영역)
- `design-kit/.claude-plugin/plugin.json` — 버전 bump는 Final Phase에서
- `.harness/` 파일 (`.harness/sprint-contract.md` 외)
- `design-kit/templates/**` — HTML 템플릿 수정은 별도 범위

## Goal

데이터 풀 REJECT 사유(SK-06) 재발 방지 + 2026 디자인 시스템 트렌드(OKLCH, DTCG v1, WCAG 2.2, Material 3 Expressive, Container Queries, APCA 보조)를 design-kit 스킬 + 에이전트 + references에 반영한다. 계약 기준 완료 조건을 모두 충족하고 validate-plugin 7 OK / markdownlint 주요 규칙 / bare fence 0건을 유지해야 한다.

## 완료 조건

### SK: design-concept SKILL.md SK-06 재발 방지

- [ ] **SK-01**: `design-concept/SKILL.md` Gotcha #3 본문에 **SK-06 글로벌 피드백 인용(2026-04-10)** + 재발 방지 검증 명령 블록 포함. 검증 명령 최소 2개: (1) `grep -nE '#[0-9a-fA-F]{3,8}' .design/concept.md` → 0 match 기대, (2) 컬러 방향 표의 5개 역할 행 존재 확인. 해당 코드블록은 `bash` 언어 힌트 명시.
- [ ] **SK-02**: `design-concept/SKILL.md` Step 4 완료 직후 **"concept.md 생성/갱신 직후 Gotcha #3 검증 명령을 반드시 실행"** 체크포인트 문장을 Step 4 본문 말미 또는 Step 4 말미 별도 줄로 추가한다. Gotcha #9의 moodboard 검증 체크포인트와 동일 패턴.
- [ ] **SK-03**: `design-concept/SKILL.md` Gotcha #3 Bad 예시 코드블록(`text` 언어 힌트)과 Good 예시 코드블록이 유지되며 전체 파일 bare fence 0건.

### DS: design-system SKILL.md + references — OKLCH + DTCG v1 + MD3 Expressive

- [ ] **DS-01**: `design-system/SKILL.md` Gotcha에 **OKLCH 권장** 항목 추가 (신규 Gotcha 또는 기존 항목 확장 허용). 필수 문구 요소: OKLCH 표기 권장, Tailwind v4/shadcn v4 기본, Safari 16.4+/Chrome 111+/Firefox 128+ 브라우저 지원, Figma Variables hex 근사치 병기 관행. 출처 URL 최소 1개 (Tailwind v4 blog 또는 evilmartians 또는 MDN oklch).
- [ ] **DS-02**: `design-system/SKILL.md` Gotcha에 **DTCG v1 스키마 준수** 항목 추가 — "DTCG v1 (2025-10-28 stable) 포맷은 `$value`, `$type`, `$description` prefix와 그룹 단위 `$type` 기본값, alias dot notation을 사용한다. Legacy `value`/`type` 키나 커스텀 `$` prefix 금지." 요지. 출처 URL 1개 (W3C DTCG 2025-10 announcement 또는 designtokens.org 2025.10 format).
- [ ] **DS-03**: `design-system/SKILL.md` Step 2 또는 Step 4에 **Material 3 Expressive HCT tonal palette** 언급 1건 — "Material 3 Expressive(2025-05)는 HCT 기반 tonal palette 정교화 + variable font axes + springy motion" 요지. 출처 URL 1개.
- [ ] **DS-04**: `design-system/references/token-principles.md`에 **"DTCG v1 포맷 (2025-10-28 stable)"** 섹션 추가 — `$value`, `$type`, `$description`, alias 예시 JSON 코드블록 1개 이상(`json` 언어 힌트 명시). 출처 URL 최소 1개. 파일 내 기존 섹션 유지.

### AU: design-audit SKILL.md + references — WCAG 2.2 반영

- [ ] **AU-01**: `design-audit/SKILL.md` Gotcha #3 본문에 **WCAG 2.2 SC 2.5.8 Target Size (Minimum) 24×24 CSS px AA** 기준을 명시적으로 추가. 기존 "44×44pt" 문구 유지하되 "Apple HIG 44pt는 터치 디바이스 실용 권장, WCAG 2.2 AA는 24 CSS px. AAA는 SC 2.5.5 Enhanced 44×44" 맥락 추가.
- [ ] **AU-02**: `design-audit/SKILL.md` Step 2 카테고리 표의 Accessibility 행 또는 신규 행/열에 WCAG 2.2 신규 SC 중 **최소 2개 이상**을 체크포인트로 추가 (예: 2.4.11 Focus Not Obscured AA, 2.5.7 Dragging Movements AA, 3.3.8 Accessible Authentication Min AA, 2.5.8 24px AA).
- [ ] **AU-03**: `design-audit/references/audit-criteria.md` Accessibility 섹션의 "터치 타겟" 행 출처를 `WCAG 2.2 SC 2.5.8 (24×24 CSS px AA) / SC 2.5.5 Enhanced (44×44 AAA) / Apple HIG 44pt 터치 권장` 으로 갱신. "색상 대비 AA" 출처 WCAG 2.1→2.2 문서로 갱신.
- [ ] **AU-04**: `design-audit/references/audit-criteria.md`에 **WCAG 2.2 신규 SC 섹션** 추가 — 최소 3개 기준을 표로: SC 2.4.11 Focus Not Obscured (AA), SC 2.5.7 Dragging Movements (AA), SC 3.3.8 Accessible Authentication Min (AA). 각 PASS 조건 1줄 이상 + 출처 URL. 출처 링크 필수.
- [ ] **AU-05**: `design-audit/references/audit-criteria.md`에 **APCA 보조 체크 NOTE** 1문단 추가 — "APCA/WCAG 3은 2026 Working Draft, WCAG 2.2 AA가 현재 컴플라이언스 타겟. 대규모 디자인 시스템 리프레시 / 다크 모드 튜닝 시 APCA Lc 사이드 체크(body min 60, preferred 75)를 권장한다" 요지. 출처 URL 1개.

### DR: design-reviewer 에이전트 — WCAG 2.2 반영

- [ ] **DR-01**: `design-reviewer.md` 카테고리 3 Spacing 또는 카테고리 4 Accessibility 본문에 "WCAG 2.2 SC 2.5.8 (AA = 24×24 CSS px) / SC 2.5.5 Enhanced (AAA = 44×44) / Apple HIG 44pt 터치 권장" 형식으로 명시적 추가. 기존 44pt 문구 유지.
- [ ] **DR-02**: `design-reviewer.md` 카테고리 4 Accessibility에 **Focus Not Obscured (WCAG 2.2 SC 2.4.11 AA)** 체크포인트 1줄 추가. 또는 기존 "포커스 인디케이터" 항목 하단에 병기.

### RE: design-responsive — Container Queries 반영

- [ ] **RE-01**: `design-audit/references/audit-criteria.md` Layout & Grid 섹션(또는 `design-audit/SKILL.md` Step 2 표)에 **Container Queries / inline-size 권장** 기준 1개 추가 — "컴포넌트 수준 반응형은 `container-type: inline-size` + `@container` 권장, 글로벌 레이아웃은 media query" 요지. 출처 URL 1개 (MDN 또는 LogRocket 또는 web.dev).
- [ ] **RE-02**: `design-guide/SKILL.md` Gotcha 또는 Step 1 카테고리 매핑 표의 "layout & grid" 행에 **container query / `@container` / self-aware component** 키워드 최소 1개 반영.

### GU: design-component / design-mockup / design-reference — 기타 갱신

- [ ] **GU-01**: `design-component/SKILL.md` Gotcha 또는 Process에 **DTCG v1 alias 포맷** 권장 1줄 추가 — "토큰 매핑 시 DTCG v1 alias dot notation (예: `color.background.surface`) 사용 권장, legacy value/type 키 금지" 요지.
- [ ] **GU-02**: `design-mockup/SKILL.md` Gotcha #3 (접근성 WCAG AA 4.5:1, 44×44pt) 문장에 **"WCAG 2.2 기준 최소 터치 타겟 24×24 CSS px (AA) — Apple HIG 44pt는 터치 실용치 권장"** 맥락 1문장 추가. 기존 문장 유지.
- [ ] **GU-03**: `design-reference/SKILL.md`는 시각 사례 수집 스킬로 트렌드 반영 범위가 제한적이며, 검토 결과 변경 사항이 없으면 "변경 없음" 사유를 self-audit 리포트에 명시 (ZERO change 허용).

### I: 인프라 / 품질 게이트

- [ ] **I-01**: `python3 scripts/validate-plugin.py design-kit` → V1~V7 전부 OK.
- [ ] **I-02**: `python3 scripts/validate-plugin.py` (전체 7 킷) → Total 7 OK, Exit 0. 회귀 금지.
- [ ] **I-03**: `python scripts/sync-docs.py --check-only` → design-kit 영역 "모두 최신 상태" 또는 sync 필요 없음. 필요 시 sync 후 재실행하여 통과.
- [ ] **I-04**: bare code fence 0건 (V6 code-fence OK로 검증) — 새로 추가하는 모든 fenced block은 반드시 언어 힌트 명시 (`bash`, `json`, `text`, `markdown`, `yaml` 등).
- [ ] **I-05**: 변경된 파일들에 MD031/MD032/MD060/MD028/MD034/MD033 markdownlint 규칙 위반 0건 — 수정 영역 주변 context 기준.
- [ ] **I-06**: git working tree modified 파일이 위 Scope 외로 벗어나지 않는다. `scripts/__pycache__/`, `.harness/sprint-contract.md` 등은 허용. `.harness/.meta/kaizen-data-pool.md`는 수정 금지.
- [ ] **I-07**: git commit 메시지 prefix `kaizen(phase6-research):` 형식 + 한국어 본문. commit hash 리포트에 기재.
- [ ] **I-08**: 브랜치 유지 — `kaizen/2026-04-11-research`, push 금지.

### TR: Trace / 출처 / 2026 트렌드

- [ ] **TR-01**: 새로 추가된 출처 URL 최소 **5개 이상** (OKLCH 1 + DTCG 1 + WCAG 2.2 1 + MD3 Expressive 1 + Container Queries 1). 중복 URL은 1회만 카운트.
- [ ] **TR-02**: SK-06 재발 방지 Gotcha 본문에 "SK-06 (2026-04-10)" 또는 유사한 피드백 식별자 참조 명시.
- [ ] **TR-03**: 리포트에 리서치 출처 URL 목록 (최소 5개) 명시.

## Rollback

Self-audit FAIL 3회 연속 또는 validate-plugin 회귀 발생 시 `git checkout -- design-kit/` 로 롤백. commit 전이면 working tree만 버리면 된다.

## Notes

- docs/design/**는 이번 Phase 범위 외 — 해당 갱신은 별도 `/design-research` Phase 책임. 이번 Phase는 스킬/에이전트/references 레벨 갱신만.
- design-concept Gotcha #3는 이미 완성도 높게 작성되어 있어 SK-01 추가 작업은 "검증 명령 강화" 중심으로 최소 침습 수정.
- APCA는 권장 보조 체크이며 필수 컴플라이언스 타겟 아님 — "NOTE" 레벨로만 추가한다 (오해 방지).
- Apple Liquid Glass는 참고 정보로만 확보하고 이번 Phase 필수 적용 범위에 포함하지 않는다 (design-kit은 스택 무관 원칙 유지).
