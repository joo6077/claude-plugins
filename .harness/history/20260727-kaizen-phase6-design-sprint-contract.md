# Sprint Contract — Phase 6 (design-kit) Kaizen

- **날짜**: 2026-07-27
- **브랜치**: kaizen/2026-07-27
- **범위**: `design-kit/**` + `.claude/skills/design-kaizen/SKILL.md` + `docs/design/research-log.md`
- **금지 범위**: 다른 kit, `harness/`, `.claude/skills/kaizen-orchestrator/`, marketplace.json, plugin.json, `docs/kaizen/changelog.md`

## 0. Triage — 이번 사이클 신호 선별

`insights-report.md §0` 은 Friction #1·#3 이 직전 사이클 승격분과 중복이며 **새 문장 규칙 추가가 아니라
enforcement 등급 상향이 정답**이라고 명시했다. 따라서 본 Phase 는 다음 두 축만 다룬다.

1. **Friction #2 (신규 최상위) — 시각·런타임 검증 신뢰 불가.** design-kit 은 UI 를 다루는 킷이므로
   Phase 3 이 "가장 직접 매핑" 이라 지목한 1순위 대상이다.
2. **Phase 1~4 정합화 (drift 해소).** 실측된 불일치만 처리하고 새 개념을 발명하지 않는다.

중복 회피 대상 (이미 승격 완료 — 재작성 금지): 최소변경/스코프크립 일반 규칙, Enumerate-before-Act,
가이드형 Process 순서 고정. design-kit 은 이미 Gotcha 로 보유 중이며 문장을 다시 다듬지 않는다.

## 1. GAP 분석

| # | GAP | 근거 (실측) | 대상 | Enforcement 판정 |
|---|-----|------------|------|-----------------|
| G1 | `design-reviewer` 미검증 임계 **3 건** vs canonical **2 건**. 게다가 같은 킷의 `design-audit` Gotcha 11 은 이미 2 건 — **킷 내부 불일치** | Phase 3 §Canonical Unverified-Evidence Protocol 의 "현재 drift" 블록 | `agents/design-reviewer.md` | E1 → **E2** (조항 복제 + 건별 집계 의무) |
| G2 | Evidence Validity Gate 4 검사(비공백/활성화/반증가능성/출처) 부재. 증거 *존재*만 보고 *유효성* 을 보지 않음 | Phase 3 §Evidence Validity Gate + Friction #2 | `design-reviewer`, `design-audit` | **E2** |
| G3 | before/after 증거 규약 및 "의도 외 영역 변화 = FAIL" 판정 부재 | §0 on_the_horizon 1 (baseline→변경→재캡처→diff→self-reject) | `references/` 신설 + `design-audit`, `design-test` | audit **E2** / test **E3** |
| G4 | 시안 승인 기록 artifact 생성 절차 부재 → 글로벌 REJECT `UI-06` | §1 UI-06 + evaluator 개선 제안 "`.harness/` 내 시안 승인 기록 파일을 evaluator 증거로 남기는 관례 수립" | `design-mockup`, `design-concept` | **E2** |
| G5 | "승인된 시각 결과물(브라우저 시안·기존 앱 색상) > 프로젝트 토큰" 우선순위 규칙 부재 | digest `preserve-original-colors`, `browser-approved-colors-ignored` (둘 다 usc=true) | `references/` 신설 + `design-system`, `design-mockup`, `design-guide` | **E2** |
| G6 | 부분 시각 변경 요청 시 나머지 시각 속성 보존 규칙 부재 | digest `border-only-changed-fill` / `-background` / `-scope-creep`, `ignored-visual-correction` | `references/` 신설 + 위 3 스킬 | **E2** |
| G7 | **사실 오류** — DTCG alias 를 "dot notation 문자열" 로 기술. 실제 spec 은 curly-brace `{group.token}` | 리서치 R2·R3 (DTCG CG-FINAL / drafts 원문) | `design-system` G13, `design-component` G3 | 사실 정정 |
| G8 | 시각 회귀 테스트 첫 실행 `--update-snapshots` 직후 실행 = **항상 통과**. Evidence Validity 검사 2(활성화)·3(반증가능성) 실패 = vacuous pass | 리서치 R6 (Playwright 문서: 첫 실행 시 baseline 자동 기록) + Phase 3 §0 매치 규칙 | `design-test` | **E3** (LLM 없는 결정론적 픽셀 판정) |
| G9 | `design-kaizen` "7 카테고리" 표기 (실제 V1~V8 = 8), parity 표 "미검증 3항" stale | Phase 4 전달 + `validate-plugin.py design-kit` 실측 출력 | `.claude/skills/design-kaizen/SKILL.md` | 사실 정정 |
| G10 | Gotcha 번호 중복이 **라이브 내부 참조를 모호하게 만듦** — `design-system` Step 5 의 "Gotcha #10" 은 #10 이 두 개, `design-concept` Step 5 의 "Gotcha #9" 도 #9 가 두 개 | 정적 검증 (`grep -oE '^[0-9]+\.'`) | `design-system`, `design-concept`, `design-mockup` | 사실 정정 |
| G11 | `docs/design/research-log.md` 최신 엔트리가 2026-04-12 | 파일 실측 | `docs/design/research-log.md` | — |

### NO ACTION 로 확정한 항목 (억지 변경 금지)

- **Counterpart Conditions 의 evaluator 측 대응 절** — Phase 3 parity 표 12 번이 **의도된 부재**로
  명시했다. "누락" 으로 오인해 design-kit 에 대응 절을 만들지 않는다.
- **Friction #1 / #3 계열 신규 문장** — 이미 승격 완료. `design-system` G12·G14, `design-component`
  G12, `design-guide` G13·G14 가 이미 보유. 문장 재다듬기는 개선이 아니다 (§3.7 승급 규칙).
- **`design-component` / `design-reference`** — 이번 사이클 직접 신호 없음. 변경하지 않는다
  (단 G7 사실 오류는 `design-component` 에도 존재하므로 그 한 줄만 정정).

## 2. 예방적 분석 (sibling parity)

`design-kaizen` Gotcha 6 의 sibling group 기준으로 신규 원칙의 전파 대상을 열거한다
(Phase 1 §5.5 Counterpart Enumeration — 편집 전 양면 열거).

| 신규 원칙 | 전파 대상 (counterpart) | 미전파 대상 + 사유 |
|-----------|------------------------|-------------------|
| Evidence Validity Gate 4 검사 | `design-audit` (skill 측) ↔ `design-reviewer` (agent 측) — **쌍으로 동시 반영** | 나머지: 감사/판정 스킬이 아님 |
| Visual Source of Truth Precedence | `design-system` · `design-mockup` · `design-guide` | `design-concept`: hex 금지 스킬이라 색상 확정 주체가 아님 |
| Partial Visual Change Isolation | `design-system` · `design-mockup` · `design-guide` | 동일 |
| Design Approval Record (UI-06) | `design-mockup` · `design-concept` (사용자 확정 단계를 가진 두 스킬) | `design-reference`: 승인 게이트 없음 |
| Before/After Evidence Block | `design-audit` · `design-test` | — |

중복 문장 확산을 막기 위해 위 4 원칙은 **`design-kit/references/visual-change-protocol.md` 를 SSOT**
로 두고, 각 스킬은 Gotcha 1 줄 + References 링크로 인용한다 (킷 내 기존 `references/visual-styles.md`
와 동일 패턴).

## 3. 리서치 (필수 3 건 이상 — 실제 7 건)

| # | 소스 | URL | 조회 결과 |
| - | ---- | --- | -------- |
| R1 | W3C WCAG 2.2 Understanding SC 2.5.8 | https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html | AA / 24×24 CSS px / 예외 5 종(Spacing·Equivalent·Inline·User Agent Control·Essential). 페이지 "Updated 11 May 2026" — 기존 킷 기재와 일치, 변경 불필요 |
| R2 | DTCG Format Module — Final CG Report (2025-10-28) | https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/ | `$value` 필수, `$extends` 그룹 상속(deep merge), alias 는 **curly brace `{group.token}`**, `$ref` 는 JSON Pointer. color 는 `colorSpace`/`components`/`hex` 객체 |
| R3 | DTCG Format Module — drafts | https://www.designtokens.org/TR/drafts/format/ | R2 확인. "Curly brace references can ONLY target complete tokens" 명시. color 값은 객체 구조 |
| R4 | MDN CSS Container Queries | https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries | baseline 안정. `container-type: size\|inline-size\|normal`, 단위 `cqw/cqh/cqi/cqb/cqmin/cqmax`. 기존 킷 기재는 `cqw/cqi` 만 언급 — 축소 기재이나 오류는 아님 |
| R5 | MDN prefers-reduced-motion | https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion | Baseline 2020-01. `reduce` 는 **"모든 애니메이션 제거" 가 아니라 vestibular trigger(scale·pan) 를 muted 대안으로 교체**. 킷의 "reduced-motion 대응" 체크가 이 뉘앙스를 잃고 있음 |
| R6 | Playwright Visual Comparisons | https://playwright.dev/docs/test-snapshots | 첫 실행 시 baseline 이 **자동 기록되고 테스트는 통과 처리**. `--update-snapshots` 로 갱신. → G8 vacuous pass 근거 |
| R7 | MDN `oklch()` | https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklch | Widely available 2023-05. L 0–1, C 0–0.4, H 0–360(red≈41°). 모던 브라우저는 fallback 불필요, 레거시만 필요 |

## 4. 완료 조건 (Acceptance Criteria)

| ID | 조건 | 측정 방법 | 유형 |
|----|------|----------|------|
| D-01 | `design-reviewer` 의 "미검증 3항 프로토콜" 이 제거되고 canonical 5 조항이 **문구 변형 없이** 복제되었으며 임계값이 2 다 | `grep -c '미검증 3항' agents/design-reviewer.md` → 0 · `grep -c '임계값은 2 다' agents/design-reviewer.md` → 1 | exact |
| D-02 | 판정 규칙 표의 미검증 분기가 canonical 3 항(0 통상 / 1 PASS+경고 / 2 이상 REJECT)과 일치한다 | 최종 판정 블록 육안 대조 + `grep -c '미검증 ≥ 2' ` ≥ 1 | structural |
| D-03 | Evidence Validity Gate 4 검사가 `design-reviewer` 와 `design-audit` **양쪽**에 존재한다 (counterpart 쌍) | `grep -lc 'Evidence Validity' agents/design-reviewer.md skills/design-audit/SKILL.md` → 2 파일 | structural, enumerated |
| D-04 | `design-kit/references/visual-change-protocol.md` 가 신설되고 4 개 절(Precedence / Isolation / Evidence Block / Approval Record)을 모두 포함한다 | `grep -cE '^## ' references/visual-change-protocol.md` ≥ 4 | exact |
| D-05 | `design-mockup` 과 `design-concept` 이 확정 단계에서 **승인 기록 아티팩트 파일**을 생성하는 Process 지시를 갖는다 (UI-06) | 두 SKILL.md 의 Process 에 `.design/approvals/` 경로 문자열 존재 | structural, enumerated |
| D-06 | Visual Source of Truth Precedence 와 Partial Visual Change Isolation 이 `design-system`·`design-mockup`·`design-guide` 3 스킬에 모두 인용된다 | `grep -l 'visual-change-protocol' skills/design-system/SKILL.md skills/design-mockup/SKILL.md skills/design-guide/SKILL.md` → 3 파일 | structural, enumerated |
| D-07 | DTCG alias 표기가 curly-brace 로 정정되었고 bare dot-notation 권장 문구가 남아 있지 않다 | `grep -n 'dot notation' skills/design-system/SKILL.md skills/design-component/SKILL.md` 결과에 "alias" 권장 맥락 0 건 | exact |
| D-08 | `design-test` 에 baseline→변경→재캡처→diff→self-reject 루프와 negative control(첫 실행 vacuous pass 차단)이 포함된다 | `grep -c 'negative control' skills/design-test/SKILL.md` ≥ 1 · self-reject 문자열 존재 | structural |
| D-09 | `.claude/skills/design-kaizen/SKILL.md` 의 "7 카테고리" 가 8(V1~V8)로 정정되고 parity 표의 "미검증 3항" 이 갱신된다 | `grep -c '7 카테고리' ` → 0 · `grep -c 'V1~V8'` ≥ 1 · `grep -c '미검증 3항'` → 0 | exact |
| D-10 | Gotcha 번호 중복 0 — `design-system`·`design-concept`·`design-mockup` | 각 파일 `grep -oE '^[0-9]+\.' \| sort \| uniq -d` → 빈 출력 | exact |
| D-11 | `docs/design/research-log.md` 에 `## [2026-07-27] - Phase 6 kaizen` 엔트리 + 리서치 URL 5 건 이상 | `grep -c 'https' ` 신규 섹션 ≥ 5 | exact |
| D-12 | `evals.json` 에 신규 원칙 assertion 이 추가되고 JSON 이 유효하다 | `python3 -c "import json;json.load(open(...))"` 성공 + 신규 assertion ≥ 3 | structural |
| D-13 | `python3 scripts/validate-plugin.py design-kit` 8 카테고리 전부 OK, exit 0 | 명령 출력 | exact |
| D-14 | 범위 밖 파일 변경 0 건 | `git status --short` 에 design-kit / .claude/skills/design-kaizen / docs/design/research-log.md / .harness/history 외 항목 없음 | exact |

## 5. 비목표 (Non-goals)

- 새 스킬·에이전트 추가
- `design-component`·`design-reference` 의 신규 원칙 도입 (신호 없음 — G7 한 줄 정정 제외)
- `harness/` 가이드 수정 (canonical 은 harness 소유, 여기서는 복제만)
- Counterpart Conditions evaluator 대응 절 신설 (의도된 부재)
- git add/commit/tag (오케스트레이터 직렬 처리)
