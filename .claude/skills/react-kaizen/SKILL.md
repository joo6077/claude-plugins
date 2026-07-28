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
4. **범위는 파일 수가 아니라 unit(관심사) 수로 센다** — 한 세션에 다루는 **관심사 1~2 개**로 제한한다. "스킬 1~2 개" 로 세면 안 된다. 하나의 관심사(예: 미검증 마커 규약 전파, sibling parity 동기화)는 본질적으로 여러 스킬을 동시에 건드리며, 그때 파일 수를 이유로 절반만 고치면 **부분 적용된 원칙**이 남아 Gotcha 7 sibling parity 와 정면으로 충돌한다. 반대로 서로 무관한 관심사 3 개를 한 세션에 묶으면 파일이 2 개여도 품질이 떨어진다.

    ```text
    Bad:  "파일 3 개 넘으니 5 개 UI 스킬 중 2 개에만 렌더 증거 규약 추가"
          → 나머지 3 개는 규약 없음 → 어느 쪽이 정식인지 알 수 없어짐
    Good: 관심사 = "렌더 증거 규약 전파" 1 개 → 해당되는 스킬 5 종 전수 적용 (파일 수 무관)
    ```
5. **/react-audit 자체 검증 필수** — 개선 후 `/react-audit` 카테고리에 영향을 주는 변경이면 6 카테고리 체크리스트를 재확인한다.
6. **Large Kit Priority Tiering (Phase 9 rust-kit 전수)** — react-kit 은 21 스킬 + 3 에이전트 = 24 surface 로 최대 규모다. 한 세션에 전수 감사하지 말고 3 계층으로 분할:
   - **Tier 1 (REJECT 직접 대응)**: REJECT reason 이 가리키는 파일만 집중 수정.
   - **Tier 2 (Phase 원칙 핵심)**: audit / reviewer / kaizen / init 같은 메타·초기화 스킬.
   - **Tier 3 (경량 audit)**: 나머지 스킬은 구조적 이슈만 Grep 기반으로 확인.
7. **Sibling Group 내부 N-way parity** — react-run / react-build / react-preflight 처럼 동일 그룹 스킬은 구조가 동일해야 한다. 한 쪽만 고치면 sibling 도 같이 동기화.
8. **공식 문서 우선 리서치 — Context7 → WebFetch → codex-rescue (Phase 5 전수)** — React 19 / TanStack Query v5 / Tauri 2 / Tailwind v4 / Lingui v5 / Zustand v5 / RHF v7 / Vite / Vitest / Playwright 관련 내용은 학습 데이터 대신 현재 공식 문서를 조회 후 인용한다. 1순위는 Context7 `resolve-library-id` → `query-docs` 다. **Context7 MCP 가 OAuth 미인증이면 호출이 실패하고 비대화형 세션에서는 인증 플로우를 실행할 수 없으므로, 복구를 기다리지 말고 즉시 WebFetch 로 공식 문서 URL 을 직접 조회한다** (2026-07-27 실측). 그래도 1차 출처를 못 찾으면 `codex-rescue` 에 리서치를 위임한다. **조회하지 못한 항목은 버전·기본값을 단정하지 않는다.** 상세는 `react-kit/references/common-gotchas.md` G9.
9. **I-02 예외 목록 (Phase 4 전수)** — Sprint Contract I-02 작성 시 react-kit 스킬 실행으로 생성되는 `package.json`, `tsconfig*.json`, `src-tauri/capabilities/*.json`, `src/locales/*`, `src/routeTree.gen.ts`, `src/wasm/core/*` 를 예외로 명시. 자세한 목록은 `react-kit/references/common-gotchas.md` G7.

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

상위 **관심사 1~2 개**를 개선한다 (Gotcha 4 — 파일 수 아닌 unit 수 기준). 한 관심사에 해당하는 스킬은 전수 적용한다. 각 개선마다:
1. 변경 전 내용
2. 변경 후 내용
3. 변경 근거 (리서치 문서 출처 파일:라인)

## Step 5: 검증

- `python3 scripts/sync-docs.py --check-only react-kit` 실행
- 변경된 스킬의 frontmatter YAML parse 재검증
- TODO/TBD/FIXME 0건 유지
- `/react-audit` 카테고리 관련 변경이면 6 카테고리 체크리스트 재검토

## Step 6: harness qa 연동

카이젠 작업도 일반 개발과 동일하게 Sprint Contract 를 작성하고 `harness:qa-evaluator` 로 APPROVE 를 받은 후 commit 한다.

**계약 파일 경로**: 단독 실행이면 `.harness/sprint-contract.md`, **오케스트레이터의 Phase 로 실행될 때는 `.harness/history/<YYYYMMDD>-kaizen-phase10-react-sprint-contract.md`** 를 쓴다. 여러 Phase 가 병렬로 도는 상황에서 `.harness/sprint-contract.md` 단일 경로를 쓰면 마지막에 쓴 Phase 가 앞선 Phase 의 계약을 덮어써 QA 근거가 소실된다 (2026-07-27 사이클 실측 제약).

**병렬 실행 중 git 쓰기 금지**: 오케스트레이터 Phase 로 실행될 때는 `git add`/`commit`/`tag`/`push` 를 호출하지 않는다. 같은 레포에서 다른 Phase 가 동시에 작업하므로 index.lock 이 충돌한다. 커밋은 오케스트레이터가 직렬로 처리한다.

## Step 7: Plugin Validation 결과 반영

카이젠 세션 시작/종료 시 `python3 scripts/validate-plugin.py react-kit` 을 실행하여 **8 카테고리 (V1~V8)** 상태를 확인하고 결과를 개선 우선순위에 반영한다.

| 체크 | 대상 |
|------|------|
| V1 frontmatter | SKILL.md / agents 의 YAML frontmatter |
| V2 templates | `templates/` 파싱 가능 여부 |
| V3 refs | References 링크 실존 |
| V4 triggers | description 트리거 키워드 중복 |
| V5 placeholders | 미완성 마커 잔존 (백틱으로 감싼 인용은 제외) |
| V6 code-fence | 언어 힌트 없는 bare fence |
| V7 plugin-json | plugin.json 과 marketplace.json 버전 일치 |
| V8 hook-exec | hooks.json 이 직접 실행하는 `.sh` 의 실행 비트(0755) |

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
- `harness/docs/guides/plugin-validation-guide.md` — 플러그인 품질 8 카테고리(V1~V8) 기준 (SSOT)
- `scripts/validate-plugin.py` — 플러그인 검증 자동화 도구
- `react-kit/references/render-evidence-protocol.md` — 렌더 산출물 증거 규약 (react-kit SSOT)
- `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol — `[미검증]` 마커·임계값 정본. react-reviewer 는 이 절을 문구 변형 없이 복제한다
- `harness/docs/guides/skill-design-guide.md` §3.7 Completion Evidence Gate — Enforcement 등급(E1/E2/E3) 정본
- `harness/docs/guides/skill-design-guide.md` §5.5 Counterpart Enumeration — 소비면 열거 원칙 정본
