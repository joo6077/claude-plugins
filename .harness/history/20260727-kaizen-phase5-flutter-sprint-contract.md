# Sprint Contract — Kaizen Phase 5 (flutter-toolkit)

Feature: Friction #2(시각·런타임 검증 신뢰 불가) enforcement 승급 + digest 결함 해소 + Flutter 3.44 정합화
Date: 2026-07-27
Branch: `kaizen/2026-07-27`
Scope: `flutter-toolkit/skills/*/SKILL.md`, `flutter-toolkit/references/*`, `flutter-toolkit/agents/widget-inspector.md`, `flutter-toolkit/evals/evals.json`, `docs/flutter/research-log.md`
Scope-out: 다른 kit 전부, `harness/**`, `.claude/skills/kaizen-orchestrator/**`, `.claude-plugin/marketplace.json`, `flutter-toolkit/.claude-plugin/plugin.json`, `docs/kaizen/changelog.md`, `flutter-toolkit/README.md`

## 배경

`/insights` 2026-07-27 (53일 · 51세션) 의 **Friction #2 "시각·런타임 검증을 신뢰할 수 없음"** 이
신규 최상위 신호이며, 사례가 전부 Flutter 다 — 빈 카탈로그를 MCP 스냅샷 근거로 "정상 렌더링"
반복 주장(실제로는 unbounded-height ListView collapse), AOT + multi-VM vmservice race 로 런타임
검증 자체 실패, 사용자가 "MCP 를 UI/e2e 검증에 쓰지 않는 재발 습관을 영구히 고쳐달라" 는 전용
세션 개설. 신뢰 손상으로 욕설 종료 세션 2 건.

Friction #1(의도 확인 전 편집) · #3(스코프 드리프트) 은 **직전 사이클에 이미 승격된 주제**이며
빈도가 줄지 않았다. 따라서 본 Phase 의 원칙은 **새 규칙 추가가 아니라 enforcement 등급 상향**
(E1 문장 → E2 아티팩트) 이다 (skill-design-guide §3.7 승급 규칙: 2 회 재발 → E1→E2).

## 리서치 소스 (전부 WebFetch 실측 · Context7 은 OAuth 미인증으로 미사용)

1. <https://docs.flutter.dev/release/release-notes> — stable 3.44.7 (page updated 2026-07-10)
2. <https://docs.flutter.dev/release/release-notes/release-notes-3.44.0> — `TestWidgetsApp` / `TestTextField` 테스트 헬퍼, `ReorderableListView.onReorder` deprecated, `ScrollCacheExtent`, 무한 Carousel, `AnimatedCrossFade.onEnd`, Impeller SDF
3. <https://api.flutter.dev/flutter/flutter_test/matchesGoldenFile.html> — golden 비교 매처 · `--update-goldens` · 폰트/플랫폼/버전 차이가 CI 실패 원인
4. <https://pub.dev/packages/golden_toolkit> — **discontinued**, 최신 0.15.0, 마지막 업데이트 3년 전
5. <https://pub.dev/packages/alchemist> — 0.14.0, 4개월 전 갱신, 유지보수 중 (Very Good Ventures / Betterment)
6. <https://pub.dev/packages/flutter_riverpod> · <https://pub.dev/packages/flutter_riverpod/changelog> — 3.4.1 (2026-07-27), 3.2.0 `family.overrideWith` deprecated → `overrideWith2`, 3.4.0 `SyncProviderTransformerMixin` deprecated, mutations/offline 여전히 experimental
7. <https://pub.dev/packages/go_router/changelog> — 17.3.0
8. <https://pub.dev/packages/flutter_hooks> — 0.21.3+1

## GAP 분석

| # | 신호 | 현행 flutter-toolkit | GAP | 처방 (등급) |
|---|------|---------------------|-----|-------------|
| G1 | Friction #2 시각 검증 | UI 생성 스킬 5종에 완료 증거 규약 **전무**. `figma-parity-self-verify.md` 는 Figma 전용이며 어떤 스킬 Process 도 참조하지 않음 | 시각 산출물 스킬이 증거 없이 완료 선언 가능 | 신규 SSOT `references/visual-evidence-protocol.md` + 5 스킬에서 참조 (**E2**) |
| G2 | Friction #2 / `false-positive-static-verification` | 정적 확인을 "동작 확인" 으로 보고 | 빈 캡처·0 매치를 PASS 로 읽음 | Evidence Validity Gate 4 검사를 flutter-audit · widget-inspector 에 도입 (**E2**) |
| G3 | Phase 3 지시 (canonical 복제) | flutter-audit 이 `[미검증]` 임계 2 건을 **자기 문서에서 재정의** | 킷별 임계 drift | canonical 5 조항 문구 변형 없이 복제 + 자체 재정의 삭제 (**E2**) |
| G4 | Friction #1 / `preserve-original-colors`(usc) | flutter-widget 은 "새로 만들기" 전제. 기존 위젯 수정 기본값 규약 없음 | play 아이콘 → CircularProgressIndicator 교체 같은 전면 재작업 | flutter-widget 에 "기존 위젯 수정이 기본값" Gotcha (**E2** — 응답 체크리스트) |
| G5 | digest `mismatched-provider-skill` | flutter-provider description 이 "신규/기존" 구분 없음 | 기존 코어 컨트롤러 수정에 feature 스캐폴딩 스킬 오적용 | description 비트리거 조건 + Step 1 중단 분기 (**E2**) |
| G6 | 글로벌 REJECT `AR-01` | codegen 산출물이 `git diff --stat` 에 섞여 scope 조건 위반 | flutter 특유 (`.g.dart`/`.freezed.dart`) | flutter-run codegen 에 산출물 분리 보고 규약 (**E2**) |
| G7 | flutter-test 결함 | Step 4 검증이 `$DART test` — widget test 는 Flutter SDK 필요 | 생성한 테스트 검증이 항상 실패 | `$FLUTTER test` 로 수정 (**버그**) |
| G8 | 출처 없는 주장 | flutter-test Gotcha 가 "출처: community 2025-12" — flutter-kaizen GATE 1 위반 | 자기 스킬의 3중 게이트 자체 위반 | 실측 URL 2 건으로 교체 (**증거**) |
| G9 | Flutter 3.44 stable | 스킬들이 3.41 기준 | 테스트 헬퍼 · deprecated 미반영 | flutter-test / flutter-widget 최신화 |
| G10 | Phase 4 전달 | flutter-kaizen SKILL.md "7 카테고리" 2 곳 | V8 hook-exec 추가로 8 | 8 (V1~V8) 로 정정 |

## Completion Conditions

### VP (Visual Evidence Protocol — Friction #2 핵심)

- [ ] VP-01: `flutter-toolkit/references/visual-evidence-protocol.md` 가 신규 생성되고, frontmatter(title/version/last_updated) + 다음 5 요소를 모두 포함한다 — (a) 시각 검증 채널 **프로젝트 감지 기반** 결정 절차, (b) baseline→변경→재캡처→대조 4 스텝 루프, (c) "빈 캡처·빈 목록·플레이스홀더만 있는 캡처는 PASS 증거가 아니라 검증 실패 신호", (d) 캡처 불가 시 `[미검증]` + "멈추고 말하라 — 추측 금지", (e) 응답에 복사해 채우는 **Visual Evidence Block** 체크리스트. [exact]
- [ ] VP-02: VP-01 문서는 특정 MCP 서버/도구 이름(`fitpal-mobile` 등)을 **하드코딩하지 않는다**. 감지 소스(`.mcp.json` / `.claude/settings.json` / `integration_test/` / `test/**/*golden*`)로만 기술한다. [exact] — `grep -in "fitpal\|mcp__" flutter-toolkit/references/visual-evidence-protocol.md` 결과 0 건
- [ ] VP-03: `flutter-widget` · `flutter-screen` · `flutter-skeleton` · `flutter-transition` · `flutter-responsive` **5 종 전부** 에 `references/visual-evidence-protocol.md` 참조 문자열이 존재한다. [exact, enumerated] — 5/5 Grep 확인
- [ ] VP-04: 위 5 종 전부에서 참조가 Gotchas 한 줄로 끝나지 않고 **완료 단계(Steps/Post-Creation/Rules 중 하나)** 에도 걸려 있어 완료 선언 직전에 실행되도록 한다. [structural, enumerated]
- [ ] VP-05: `references/figma-parity-self-verify.md` 가 신규 프로토콜을 상위 규약으로 인용하여 두 문서의 역할 경계(일반 시각 증거 vs Figma SSIM 수렴)가 명시된다. [structural]

### EV (Evidence Validity Gate — Phase 3 정합화)

- [ ] EV-01: `flutter-audit/SKILL.md` 에서 `[미검증]` **임계값·마커 의미 자체 재정의 문장이 삭제**되고, 대신 `harness/docs/guides/qa-evaluation-guide.md §Canonical Unverified-Evidence Protocol` 앵커 인용 + 5 조항이 **문구 변형 없이** 복제된다. [exact]
- [ ] EV-02: `flutter-audit/SKILL.md` 에 Evidence Validity Gate **4 검사(비공백/활성화/반증가능성/출처)** 가 도입되고, "0 매치 grep 은 위반 없음이 아니라 검사되지 않음" 규칙이 포함된다. [exact]
- [ ] EV-03: `agents/widget-inspector.md` 의 "Clean — 추출 후보 없음" 리포트 경로에 **vacuous pass 차단** 규칙이 추가된다 — 스캔 대상 파일 수를 먼저 세어 보고하고, 0 파일이면 Clean 이 아니라 `[미검증]`. [exact]
- [ ] EV-04: widget-inspector 의 `[미검증]` 마커 설명이 자체 임계 재정의를 하지 않고 canonical 앵커를 인용한다. [structural]

### FR (Friction #1/#3 enforcement 승급 — 중복 금지 준수)

- [ ] FR-01: `flutter-widget/SKILL.md` 에 **"기존 위젯 수정이 기본값"** Gotcha 가 추가된다 — 시각 변경 요청은 (a) 대상 위젯을 파일:라인으로 지목, (b) 유지할 속성(색상·크기·모션)을 명시 열거, (c) 기존 위젯을 Flutter 기본 위젯으로 **교체**하려면 사전 승인. [exact]
- [ ] FR-02: FR-01 은 기존 Enumerate-before-Act Gotcha 를 **삭제·재작성하지 않고** append 된다 (직전 사이클 승격분 보존). [structural]
- [ ] FR-03: `flutter-widget` 의 Enumerate-before-Act 항목에 **enum/카탈로그/공용 헬퍼 중복 생성 방지** grep 대상이 추가된다 (`_SkinScreen` vs 기존 `UserModeScreen` 중복 사례). [exact]

### SK (digest 결함 · 스킬 오적용)

- [ ] SK-01: `flutter-provider/SKILL.md` frontmatter description 에 **비트리거 조건**("기존 컨트롤러/서비스 수정에는 트리거하지 않는다" 취지) 이 명시된다. [exact]
- [ ] SK-02: `flutter-provider/SKILL.md` Step 1 에 대상이 **기존 파일 수정**이면 스킬을 중단하고 안내하는 분기가 추가된다. [structural]
- [ ] SK-03: `flutter-provider/SKILL.md` Code Rules 에 **편집 전 Read 의무**(edit-before-read 대응) 가 MUST 로 추가된다. [exact]
- [ ] SK-04: `flutter-hooks/SKILL.md` 3-Step(탐색→진단→처방) 뒤에 **검증 스텝**이 추가되어, 정적 확인만으로 "동작 확인" 을 주장하지 못하게 한다 (`false-positive-static-verification`). [exact]
- [ ] SK-05: `flutter-run/SKILL.md` codegen 서브커맨드에 **codegen 산출물과 수기 변경 분리 보고** 규약이 추가된다 (글로벌 REJECT `AR-01`). exclude pathspec 명령이 포함되어야 한다. [exact]

### UP (최신화 · 버그)

- [ ] UP-01: `flutter-test/SKILL.md` Step 4 검증 명령이 `$DART test` → `$FLUTTER test` 로 수정된다. [exact]
- [ ] UP-02: `flutter-test/SKILL.md` 의 "출처: community 2025-12" 무출처 주장이 실측 URL(golden_toolkit discontinued · alchemist 0.14.0) 로 교체된다. [exact]
- [ ] UP-03: `flutter-test/SKILL.md` 에 Flutter 3.44 신규 테스트 헬퍼(`TestWidgetsApp`, `TestTextField`) 와 golden test 플랫폼 의존 주의사항이 출처 URL 과 함께 추가된다. [exact]
- [ ] UP-04: `flutter-widget/SKILL.md` 의 Riverpod 버전 언급이 실측 3.4.1 기준으로 갱신되고, 3.44 신규 위젯/deprecated 항목이 출처와 함께 추가된다. [exact]

### KZ (Phase 4 전달 사항)

- [ ] KZ-01: `flutter-toolkit/skills/flutter-kaizen/SKILL.md` 의 "7 카테고리" 표기 **2 곳 모두** 8 (V1~V8) 로 정정된다. [exact, enumerated] — `grep -c "7 카테고리"` 결과 0
- [ ] KZ-02: flutter-kaizen Gotchas 에 scope-creep 판정 기준이 **파일 수가 아니라 unit(관심사) 수** 임이 명시된다. [exact]

### EL (Eval)

- [ ] EL-01: `flutter-toolkit/evals/evals.json` 에 시각 증거 프로토콜 assertion 이 최소 1 개 스킬에 추가된다. [exact]
- [ ] EL-02: `flutter-toolkit/evals/evals.json` 에 flutter-provider 오적용(기존 파일 수정 요청) 케이스가 추가된다. [exact]
- [ ] EL-03: evals.json 이 유효한 JSON 으로 파싱된다. [exact] — `python3 -c "import json;json.load(open(...))"`

### DOC (리서치 로그)

- [ ] DOC-01: `docs/flutter/research-log.md` 에 `## [2026-07-27]` 엔트리가 추가되고 **리서치 소스 URL 5 건 이상**을 포함한다. [exact, enumerated]

### RG (회귀 게이트)

- [ ] RG-01: `python3 scripts/validate-plugin.py flutter-toolkit` 이 V1~V8 전부 OK. [exact]
- [ ] RG-02: 범위 밖 파일이 수정되지 않음 — `git diff --name-only` 에 `harness/`, 타 kit, `marketplace.json`, `plugin.json`, `docs/kaizen/changelog.md` 미포함. [exact]
- [ ] RG-03: 모든 신규 code fence 에 언어 태그가 있다 (validate-plugin V6 = 0 bare). [exact]

## Anti-patterns (즉시 REJECT)

- 직전 사이클에 이미 승격된 Friction #1/#3 문장을 **같은 등급(E1)으로 재추가**
- 기존 Gotchas 삭제·재작성 (canonical 정합화를 위한 **자체 임계 재정의 삭제는 예외 · EV-01 에 명시**)
- 특정 프로젝트 MCP 서버/도구명 하드코딩
- 출처 URL 없는 버전·API 주장 (flutter-kaizen GATE 1)
- git add / commit / tag / push / finalize 실행
- 범위 밖 파일 수정

## Verification Method

- **L3** `grep -c "visual-evidence-protocol" flutter-toolkit/skills/{flutter-widget,flutter-screen,flutter-skeleton,flutter-transition,flutter-responsive}/SKILL.md` → 5/5 ≥ 1
- **L3** `grep -in "fitpal\|mcp__" flutter-toolkit/references/visual-evidence-protocol.md` → 0
- **L3** `grep -c "7 카테고리" flutter-toolkit/skills/flutter-kaizen/SKILL.md` → 0
- **L3** `python3 -c "import json; json.load(open('flutter-toolkit/evals/evals.json'))"` → 무예외
- **L3** `python3 scripts/validate-plugin.py flutter-toolkit` → V1~V8 OK, Exit 0
- **L3** `git diff --name-only` → scope-out 미포함
