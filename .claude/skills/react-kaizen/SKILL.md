---
name: react-kaizen
description: >
  react-kit 스킬 품질을 docs/react/ 리서치 문서 기준으로 주기적으로 개선한다.
  이 레포 개발용 스킬이며, react-kit 플러그인에 포함되지 않는다.
  harness-kaizen, flutter-kaizen, design-kaizen, rust-kaizen 과 동일한 패턴.
  "/react-kaizen", "React 카이젠", "react-kit 개선" 같은 요청 시 트리거.
  단순 버그 수정이나 기능 구현 요청에는 트리거하지 않는다.
argument-hint: ""
user-invocable: true
---

# Gotchas

1. **리서치 문서 없이 개선 금지** — `docs/react/kit-design/` 의 G1~G6 + G5b 설계 문서를 먼저 읽고, 그 기준으로만 개선한다. 근거 없는 개선은 금지.
2. **스킬 삭제 금지** — 기존 21개 스킬을 삭제하지 않는다. 개선만 한다.
3. **라이브러리 0개 원칙 보존** — G5b 애니메이션과 /react-audit Library Policy 의 금지 라이브러리 목록은 절대 완화하지 않는다. 신규 금지 라이브러리 추가는 허용.
4. **한 번에 1~2개 스킬만 개선** — 전체를 한 번에 수정하면 품질이 떨어진다.
5. **/react-audit 자체 검증 필수** — 개선 후 `/react-audit` 카테고리에 영향을 주는 변경이면 6 카테고리 체크리스트를 재확인한다.

# Process

## Step 1: 현황 분석

`react-kit/skills/` 의 21개 SKILL.md 와 `react-kit/agents/` 의 3개 에이전트를 읽고 현재 상태를 파악한다.

## Step 2: 리서치 문서 비교

`docs/react/kit-design/` 의 해당 그룹 문서 (g1~g6, g5b) 와 스킬의 Gotchas, Process, 코드 예시를 비교한다. 차이가 있는 부분을 목록화한다.

| 스킬 그룹 | 소스 문서 |
|-----------|----------|
| G1 스캐폴딩 (4) | docs/react/kit-design/g1-scaffolding.md |
| G2 상태/데이터 (4) | docs/react/kit-design/g2-state-data.md |
| G3 성능 (2) | docs/react/kit-design/g3-performance.md |
| G4 품질 (3) | docs/react/kit-design/g4-quality.md |
| G5 UI 패턴 (3) | docs/react/kit-design/g5-ui-patterns.md |
| G5b 애니메이션 (1) | docs/react/kit-design/g5b-animation.md |
| G6 빌드/감사 (4) | docs/react/kit-design/g6-build-audit.md |

## Step 3: 개선 우선순위

| 우선순위 | 기준 |
|----------|------|
| 높음 | 잘못된 정보, deprecated API, 안티패턴 포함, Library Policy 위반 우려 |
| 중간 | 누락된 Gotchas, 불완전한 Process, 트리거 키워드 충돌 |
| 낮음 | 코드 예시 개선, References 보강 |

## Step 4: 개선 실행

상위 1~2개 스킬을 개선한다. 각 개선마다:
1. 변경 전 내용
2. 변경 후 내용
3. 변경 근거 (리서치 문서 출처 파일:라인)

## Step 5: 검증

- `python3 scripts/sync-docs.py --check-only react-kit` 실행
- 변경된 스킬의 frontmatter YAML parse 재검증
- TODO/TBD/FIXME 0건 유지
- `/react-audit` 카테고리 관련 변경이면 6 카테고리 체크리스트 재검토

## Step 6: harness qa 연동

카이젠 작업도 일반 개발과 동일하게 `.harness/sprint-contract.md` 를 작성하고 `harness:qa-evaluator` 로 APPROVE 를 받은 후 commit 한다.

## Step 7: Plugin Validation 결과 반영

카이젠 세션 시작/종료 시 `scripts/validate-plugin.py react-kit` 을 실행하여 7 카테고리 상태를 확인하고 결과를 개선 우선순위에 반영한다.

**실행 패턴, 우선순위 매핑, 통합 규칙**은 `harness/docs/guides/plugin-validation-guide.md §7` 에서 정의한다 (SSOT) — 해당 섹션을 그대로 따른다.

### react-kit 특화 규칙 — Library Policy 절대 완화 금지

`react-animation`, `animation-architect-react`, `react-audit` 의 Library Policy 카테고리에 정의된 **라이브러리 0개 원칙** (Motion/framer-motion/dnd-kit/react-spring/react-transition-group 등 빌드 게이트급 금지 목록) 은 이 검증 단계에서도, 그 어떤 카이젠 세션에서도 **절대 완화하지 않는다**. Plugin Validation 결과와 무관하게 이 원칙은 고정이다. 신규 금지 라이브러리 추가만 허용한다.

# References

- `docs/react/kit-design/g1-scaffolding.md` — G1 스캐폴딩 그룹 설계 (react-init/react-screen/react-feature/react-widget)
- `docs/react/kit-design/g2-state-data.md` — G2 상태/데이터 그룹 설계 (react-store/react-api/react-query/react-form)
- `docs/react/kit-design/g3-performance.md` — G3 성능 그룹 설계 (react-wasm/react-tauri)
- `docs/react/kit-design/g4-quality.md` — G4 품질 그룹 설계 (react-test/react-error/react-l10n)
- `docs/react/kit-design/g5-ui-patterns.md` — G5 UI 패턴 그룹 설계 (react-responsive/react-skeleton/react-extract + widget-inspector-react)
- `docs/react/kit-design/g5b-animation.md` — G5b 애니메이션 그룹 설계 (react-animation + animation-architect-react)
- `docs/react/kit-design/g6-build-audit.md` — G6 빌드/감사 그룹 설계 (react-run/react-build/react-preflight/react-audit + react-reviewer)
- `docs/react/wasm-catalog.md` — WASM 이식 카탈로그 (이식 판정 SSOT)
- `react-kit/skills/` — 개선 대상 21개 스킬
- `react-kit/agents/` — 개선 대상 3개 에이전트
- `react-kit/evals/evals.json` — 테스트 케이스 (향후 추가)
- `harness/docs/guides/plugin-validation-guide.md` — 플러그인 품질 7 카테고리 기준 (SSOT)
- `scripts/validate-plugin.py` — 플러그인 검증 자동화 도구
