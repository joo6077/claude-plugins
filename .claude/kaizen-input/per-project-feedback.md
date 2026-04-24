# Per-Project Recent Feedback

## apps

### sprint-contract.md (excerpt)
```markdown
---
feature: "위젯 리팩토링 — 터치 효과 추출, 셀렉트 통합, 캐러셀 분리"
created: "2026-04-12 17:30"
complexity: "중간"
conditions: 14
---

## UI
- [ ] UI-01: 관리자 측 터치 효과 적용 위젯(버튼, 날짜 필드 등)이 리팩토링 전과 동일한 탭 피드백(축소 애니메이션)을 표시한다
- [ ] UI-02: 언어 선택/서버 선택 메시지 박스의 옵션 리스트가 리팩토링 전과 동일하게 표시된다 (스트립 강조, 간격, 텍스트 스타일)
- [ ] UI-03: 캐러셀 위젯의 PageView와 인디케이터가 리팩토링 전과 동일하게 표시된다

## Logic
- [ ] LG-01: Given 관리자 측 터치 효과 위젯이 disabled 상태, When 탭하면, Then 축소 애니메이션과 onTap 콜백이 발생하지 않는다
- [ ] LG-02: Given 언어 선택 박스에서 옵션을 탭, When 닫기 버튼을 누르면, Then 선택된 언어 코드가 반환된다
- [ ] LG-03: Given 서버 선택 박스에서 옵션을 탭, When 닫기 버튼을 누르면, Then 선택된 index가 반환된다
- [ ] LG-04: 캐러셀 인디케이터가 별도 StatelessWidget으로 분리되어 있다

## Architecture
- [ ] AR-01: 공통 터치 효과 위젯이 ui/widgets/ 경로에 위치한다 (admin/user 공용)
- [ ] AR-02: 공통 셀렉트 옵션 리스트 위젯이 ui/admin/widgets/messagebox/ 경로에 위치한다
- [ ] AR-03: 기존 위젯의 public API(Props, show 함수)가 변경되지 않는다

## Anti-patterns
- [ ] AP-03: Opacity 위젯 사용 자제
- [ ] AP-04: setState 사용 자제 — hooks + Riverpod 사용

## Reusability
- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics
- [ ] DG-01: `fvm flutter analyze --no-fatal-infos apps/app_kiosk` 워닝 0개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (스펠체크 제외)
- [ ] DG-03: N/A (test 디렉토리 미존재)
- [ ] DG-04: 앱 실행 시 에러 0개

```

### sprint-feedback.md (last 3000 chars)
```markdown
import 'package:freezed_annotation/freezed_annotation.dart';

    import 'package:app_kiosk/ui/admin/theme/styles/colors.dart';
    import 'package:app_kiosk/ui/widgets/pressable_widget.dart';
    ```
- [x] CG-06: Nullable 변수 `= null` 명시적 초기화 금지 — PASS
- [x] CG-07: `== true/false` 불리언 비교 금지 — PASS (주석 내 텍스트 제외)
- [x] CG-08: on절 없는 catch 금지 — PASS (catch 사용 없음)
- [x] CG-13: setState 금지 — PASS
- [x] CG-14: const 생성자 적극 사용 — PASS
- [x] CG-15: 재사용 UI는 StatelessWidget/HookWidget — PASS
- [x] CG-16: Opacity 위젯 사용 자제 — PASS (AnimatedOpacity 사용)
- [x] CG-17: 둥근 모서리는 BoxDecoration.borderRadius — PASS
- [x] CG-18: ListView/GridView builder 방식 — PASS (PageView.builder)
- [x] CG-19: 모델은 @freezed immutable — PASS
- [x] CG-23: ref.watch는 build()에서만 — PASS (ref 사용 없음)

### Project Conventions (6/6)

- [x] PJ-01: 화면 위젯은 HookConsumerWidget — PASS (버튼/다이얼로그 위젯은 화면 아님, 해당 없음)
- [x] PJ-02: Viewmodel 네이밍 — PASS (변경 없음)
- [x] PJ-03: 화면 Props는 @freezed *ScreenProps — PASS (변경 없음)
- [x] PJ-04: Admin/User 접두사 컨벤션 — PASS (`AdmSelectOptionListWidget`, `PressableWidget`(공용))
- [x] PJ-07: Admin/User 테마 완전 분리 — PASS
- [x] PJ-08: riverpod_generator 사용 — PASS (변경 파일에 @riverpod 불필요)

### Diagnostics (4/4)

- [x] DG-01: analyze warning 0개 (변경/생성 파일 대상) — PASS
  - 근거: `fvm flutter analyze --no-fatal-infos` 7개 대상 파일 모두 `No issues found`.

- [x] DG-02: IDE diagnostics warning/info 0개 (스펠체크 제외) — PASS

- [x] DG-03: N/A (test 디렉토리 미존재) — PASS

- [x] DG-04: 앱 실행 시 에러 0개 — PASS (정적 분석 기준 런타임 에러 없음, L2 수준 검증)

---

## Summary

- Total: Sprint Contract 조건 18/18 통과, Coding Guideline CG-05 위반 5건
- Verdict: **REJECT**

### REJECT 사유

| ID | 분류 | 파일 |
|----|------|------|
| CG-05 | Coding Guideline | `select_option_list_widget.dart:12-14` |
| CG-05 | Coding Guideline | `round_rect_button_widget.dart:14-20` |
| CG-05 | Coding Guideline | `drop_down_list_button_widget.dart:12-19` |
| CG-05 | Coding Guideline | `image_button_widget.dart:14-19` |
| CG-05 | Coding Guideline | `date_range_field_widget.dart:17-24` |

### 필수 수정 항목

**CG-05: 5개 파일의 import 순서 교정**

규칙: 외부 패키지(`flutter`, `flutter_hooks`, `freezed_annotation`, `go_router` 등) → 빈줄 → 내부 패키지(`app_kiosk/`)

`pressable_widget.dart`는 Iteration 2에서 이미 올바르게 수정됐으나, 동일 작업 범위에 포함된 나머지 5개 파일은 수정되지 않았다.

각 파일별 올바른 순서:

**select_option_list_widget.dart:**
```dart
import 'package:flutter/material.dart';

import 'package:app_kiosk/ui/admin/theme/styles/colors.dart';
import 'package:app_kiosk/ui/admin/theme/styles/sizes.dart';
```

**round_rect_button_widget.dart:**
```dart
import 'package:flutter/material.dart';
import 'package:freezed_annotation/freezed_annotation.dart';

import 'package:app_kiosk/ui/admin/theme/styles/colors.dart';
import 'package:app_kiosk/ui/admin/theme/styles/sizes.dart';
import 'package:app_kiosk/ui/admin/theme/styles/text_styles.dart';
import 'package:app_kiosk/ui/ui_defs.dart';
import 'package:app_kiosk/ui/widgets/pressable_widget.dart';
```

(drop_down_list_button_widget, image_button_widget, date_range_field_widget도 동일 패턴 적용)

```

## claude-plugins

### sprint-contract.md (excerpt)
```markdown
---
feature: "reflect-kit v0.3.0 — Hybrid project_id (backward-compatible)"
created: "2026-04-17 17:17"
complexity: "중간"
conditions: 20
---

## Skill
- [ ] SK-01: `/reflect-digest project=<basename>` 와 `/reflect-digest project=<basename>-<hash6>` 가 동일한 스캔 대상 디렉토리 집합을 선택하고, 집계된 reflections 엔트리 수가 일치한다 [goal]
- [ ] SK-02: reflect-digest SKILL.md 에서 "레거시 버킷" 관련 분류 섹션이 제거되고, 정규화 쿼리 동작(basename → basename + basename-<hash6> glob union)이 명시된다 [structural]
- [ ] SK-03: `/reflect-digest project=all` cross-project 집계 로직이 신규 basename 디렉토리와 기존 `*-<hash6>` 디렉토리를 모두 포함하도록 glob 패턴이 확장된다 [structural]

## Script
- [ ] SC-01: 충돌 없는 경우 `compute_project_id` 는 `<basename>` 만 반환한다 (hash suffix 없음). "충돌 없는 경우" = `~/.claude/logs/<basename>/` 디렉토리가 없거나, 존재하면 해당 디렉토리의 `.project-root` 마커가 현재 git root와 일치할 때 [structural]
- [ ] SC-02: 충돌 감지 시 `<basename>-<hash6>` 로 fallback 하고 stderr 에 경고를 출력한다. "1회 보장" = 단일 스크립트 실행 프로세스 단위, `${TMPDIR:-/tmp}/.reflect-kit-warn-<basename>-<PID>` 마커 파일 기반 [structural]
- [ ] SC-03: `scripts/legacy-id-migrate.sh --scan` 결과에서 `_cron`, `.*`, `_*` 내부 디렉토리가 제외된다 [structural, enumerated]
- [ ] SC-04: reflect-digest 의 cross-project 스캔에서 SC-03 과 동일한 필터(`_cron`, dot-prefix, underscore-prefix)가 적용된다 [structural, enumerated]

## Error
- [ ] ER-01: git 미설치 또는 비-repo 환경에서 `compute_project_id` 는 cwd basename 을 반환하며 기존 fallback 경로(cwd → hash input)가 유지된다 [goal]
- [ ] ER-02: `hooks/log-*.sh` 의 쓰기 경로가 `compute_project_id` 결과를 그대로 사용하므로, SC-02 충돌 감지 충족 시 기존 `<basename>/` 디렉토리를 덮어쓰지 않고 자동으로 `
```

### sprint-feedback.md (last 3000 chars)
```markdown
(3/3)
- [x] ER-01: git 미설치/비-repo 환경에서 cwd basename 반환 + 기존 fallback 유지 — PASS
  - 근거: `_lib-project-id.sh:62-63` — `git ... 2>/dev/null` 실패 시 `repo_root="$cwd"` fallback. 실행: `/tmp` 전달 시 `"tmp"` 반환 [L3]
- [x] ER-02: `log-*.sh` 쓰기 경로가 `compute_project_id` 결과 그대로 사용 — PASS
  - 근거: `log-prompt.sh:26-27`, `log-tool-failure.sh:27-28` — `project_id=$(compute_project_id "$cwd")` → `log_dir="$HOME/.claude/logs/$project_id"`. SC-02에서 충돌 시 hash fallback이 반환되므로 기존 `<basename>/` 덮어쓰기 없음 [L3]
- [x] ER-03: glob 매칭 0개 시 "no matching buckets" stderr 출력 — PASS
  - 근거: `SKILL.md:62,104` — 두 군데서 `no matching buckets for project=<query>` stderr 출력 후 종료 명시 [L3, structural — LLM-driven skill]

### Architecture (4/4)
- [x] AR-01: glob union으로 기존 hash 디렉토리 read — 마이그레이션 불필요 — PASS
  - 근거: `SKILL.md:45,102` — backward-compat glob union 보증. `DESIGN.md:231-236` — 마이그레이션 스크립트 불필요 명시 [L3]
- [x] AR-02: plugin.json version=0.3.0, marketplace.json description `[v0.3.0 · 2026-04-17]` 접두사 — PASS
  - 근거: `reflect-kit/.claude-plugin/plugin.json:4` `"version": "0.3.0"`. `marketplace.json:51` description starts with `[v0.3.0 · 2026-04-17]` — Python 검증 `True` [exact]
- [x] AR-03: DESIGN.md "결정 #3 Hybrid 전환" 섹션 + 독립 리뷰 근거 + backward-compat 보증 — PASS
  - 근거: `DESIGN.md:210-248` — `## 결정 #3 상세 — Hybrid project_id (v0.3.0 전환)` 섹션. A/B/C안 비교(lines 217-220), backward-compat 표(lines 224-229), 보증 목록(lines 231-236) [L3]
- [x] AR-04: README.md v0.3.0 변경 요약(Hybrid 전환 + 정규화 쿼리 + 내부 디렉토리 제외) — PASS
  - 근거: `README.md:9-15` — `## v0.3.0 변경 요약` 섹션에 Hybrid project_id, 정규화 쿼리, 내부 디렉토리 제외 세 항목 모두 명시 [L3]

### Anti-patterns (2/2)
- [x] AP-01: 버전 하드코딩 없음 — PASS
  - 근거: `grep -rn 'hardcoded.*version'` → no match [L2]
- [x] AP-03: bare code fence 없음 — PASS
  - 근거: `grep -Pn '^```\s*$'` on SKILL.md, DESIGN.md, README.md → no match [L2]

### Reusability (2/2)
- [x] RE-01: 재사용 가능한 컴포넌트 private 처리 없음 — PASS
  - 근거: `_lib-project-id.sh`의 `normalize_project_query`, `compute_project_id`, `is_internal_logs_dir` 모두 `source`로 공유. `legacy-id-migrate.sh`에서 재사용 확인 [L3]
- [x] RE-02: 중복 컴포넌트 없음 — PASS
  - 근거: hash 계산은 `_rk_hash6()` 단일 함수로 중앙화. 필터는 `is_internal_logs_dir()` 단일 함수. 중복 구현 없음 [L3]

### Diagnostics (4/4)
- [x] DG-01: `bash -n` 문법 검사 워닝 0개 — PASS
  - 근거: `bash -n` on `_lib-project-id.sh`, `legacy-id-migrate.sh`, `log-prompt.sh`, `log-tool-failure.sh`, `log-reflection.sh` 모두 OK [L2]
- [x] DG-02: IDE diagnostics 워닝 0개 — PASS [정적]
  - ⚠️ 런타임 검증 미수행 — MCP 서버 미설정
- [x] DG-03: `scripts/release.sh` 리허설 에러 0개 — PASS
  - 근거: `bash -n scripts/release.sh` → OK [L2]
- [x] DG-04: 충돌 시뮬레이션 — basename 반환 + hash fallback + 1회 경고 — PASS
  - 근거: SC-02 실행 검증 결과와 동일. `.project-root`에 다른 경로 기록 후 `compute_project_id` 호출 → `claude-plugins-701489` + stderr 경고 1회 출력. `_rk_warn_once` PID 마커(`${TMPDIR:-/tmp}/.reflect-kit-warn-<basename>-<PID>`) 확인 [L3]

## Summary
- Total: 20/20 conditions passed
- Anti-patterns: 2/2 PASS
- Reusability: 2/2 PASS
- Diagnostics: 4/4 PASS
- Verdict: APPROVE

⚠️ 런타임 검증 미수행 — MCP 서버 미설정. 모든 판정은 정적/실행 검증 기반.

```

## fit-pal

## flutter_playwright

### sprint-contract.md (excerpt)
```markdown
---
feature: "V2 Phase D — find_widget Element-level selector 확장"
created: "2026-04-24 10:33"
revised: "2026-04-24 10:45"
complexity: "중간"
conditions: 24
---

## Architecture
- [ ] AR-D1: `find_widget` MCP tool 의 inputSchema `properties.by.enum` 배열에 정확히 `text | type | key | semantic | role | placeholder | tooltip | testId` 8 개 value 가 열거된다 [exact, enumerated]
- [ ] AR-D2: `tools/list` 총 개수는 정확히 47 (server 17 + toolkit 30, dynamic registry 관리 도구 `listClientToolsAndResources` / `runClientTool` / `runClientResource` / `getRegistryStats` 4개 제외). Phase C ACCEPT 시점 대비 변경 없음 [exact]
- [ ] AR-D3a: Element-level 접근 레이어 결정 근거가 `.harness/history/20260424-phase-d-layer-decision.md` 파일에 기록된다. 파일은 (1) 선택된 옵션 (A server-only / B toolkit 경로 / C hybrid), (2) Codex 리서치 요약, (3) 선택 근거의 3 개 섹션을 포함한다 [structural]
- [ ] AR-D3b: `AR-D3a` 파일에 기록된 선택 옵션이 실제 구현 PR 의 코드 경로와 일치한다. 옵션 A 기록 시 server 측 inspector RPC 확장만, 옵션 B 기록 시 toolkit 서비스 확장 경로 필수, 옵션 C 기록 시 양쪽 모두 존재 [goal]
- [ ] AR-D4: **조건부** — AR-D3a 에서 옵션 B 또는 C 선택 시에만 판정 (옵션 A → N/A, PASS 처리). 선택된 경우 신규 서비스 확장 이름은 `ext.flutter.playwright.*` 네임스페이스 + verb_object snake_case 컨벤션 (예: `ext.flutter.playwright.find_widget_by_element`) [structural]

## Logic
- [ ] LG-D1: 기존 `by=text` / `by=type` 호출에 대한 Phase C tool_contract_test 스위트와 find_widget 관련 기존 테스트가 변경 없이 green 을 유지한다 [structural]
- [ ] LG-D2: 신규 6 selector 각각의 매칭 semantics 가 아래와 정확히 일치한다 [exact, enumerated]:
  - `by=key`: `ValueKey(value).toString() == query` 인 Widget
  - `by=semantic`: `Semantics.p
```

### sprint-feedback.md (last 3000 chars)
```markdown
che`, `InspectorRpcClient`, `ScreenshotRegistry`, `ImageFileSaver`, `saveOrEmbedImage`, `formatTree`, `TreeFormat`, `parseTreeFormat` 모두 public 선언. (L2)

- [x] RE-02: 기존 컴포넌트 재사용 — PASS
  - 근거: `saveOrEmbedImage`는 `ImageFileSaver` 활용. `SnapshotCache`는 `InspectorRpcClient` 재사용. `ScreenshotRegistry`는 LG-03에서 재사용. `formatTree`는 `snapshot_widgets_handler`에서 사용. toolkit entries들은 기존 service 클래스들(`NavigationService`, `SharedPrefsService`, 등) 재사용. (L3)

### Diagnostics (3/4)

- [x] DG-01: fvm dart analyze (server) 워닝 0개 — PASS
  - 근거: `fvm dart analyze packages/flutter_playwright_server` → "No issues found!" (L1)

- [x] DG-02: fvm flutter analyze (toolkit) 워닝 0개 — PASS
  - 근거: `fvm flutter analyze packages/flutter_playwright_toolkit` → "No issues found! (ran in 1.4s)" (L1)

- [ ] DG-03: 6개 시나리오 커버 — FAIL (부분)
  - (a) snapshot_widgets format=yaml YAML 출력 — PASS: `tree_formatter_test.dart:97-136` LG-01 계약 예시와 동일 nested 트리 검증.
  - (b) saveImagesToFiles=true 시 take_screenshot/screenshot_widget 응답 path/resourceUri + image 부재 — FAIL [미검증]: `screenshot_widget_handler_test.dart:118-147`는 handler 레벨 검증. `take_screenshot` tool response(`CallToolResult`)에서 path 포함 + image 없음을 검증하는 tool-level 테스트 없음. `image_payload_test.dart`는 helper 레벨 검증.
  - (c) --embed-images 경로 응답 shape AR-07 구조 일치 — FAIL: AR-07 bounds 미구현으로 테스트도 bounds 검증 없음.
  - (d) 그룹화 11개 도구 각 2개 action 분기 = 22개 이상 서브테스트 — FAIL: `tool_contract_test.dart`는 tool 이름과 enum schema만 검증. 실제 action 분기 dispatch 결과를 검증하는 서브테스트 22개가 존재하지 않음. navigate, set_checkbox 등 toolkit tool-level 동작 테스트 없음.
  - (e) 구 도구 이름 Unknown tool — 조건부 PASS: dart_mcp 기본 동작 의존. `evaluate` 제외 46/47개는 PASS. evaluate는 여전히 활성 도구로 ER-03 연계 FAIL.
  - (f) take_screenshot 저장 후 screenshot:// URI가 MCP resource list에 포함 — [미검증]: 런타임 검증 불가. 정적으로는 `flutter_inspector_tools.dart:86-101` resource template 등록 확인 가능하나 `take_screenshot`은 `flutter_screenshots.dart`를 통해 `ScreenshotResourceRegistry`에 등록하지 않음 — `_inspectorImageSaver` + `_screenshotRegistry`는 inspector tools 전용. `take_screenshot`(구 get_screenshots) 응답은 FileUrl 경로만 반환하며 screenshot:// URI 형식 없음.
  - 수정 우선순위: (d) 22개 action 분기 서브테스트 추가. (b) take_screenshot tool response level 테스트. (c) AR-07 bounds 구현 후 테스트. (f) take_screenshot을 ScreenshotResourceRegistry에 연결.

- [x] DG-04: 기존 전체 테스트 green — PASS
  - 근거: server `fvm dart test` → 196/196 PASS. toolkit `fvm flutter test` → 152/152 PASS. (L1)

## Summary

- Total: 13/24 conditions passed
- Verdict: **REJECT**

### Critical FAILs (수정 우선순위 순)

1. **AR-05 / ER-03** — toolkit `expression_entries.dart:38` `name: 'evaluate'` → `'evaluate_expression'` 미적용. 1줄 수정.
2. **AR-07 / AP-01** — embed 모드 응답에 `bounds` 필드 없음. `saveOrEmbedImage` + handler 수정 필요.
3. **AR-02c / AR-01** — `get_network_log` server 이전. 총 도구 수 49 → 47 범위.
4. **LG-08 / AR-08** — `_yamlFallback` 중복 YAML 구현. dump_tree 등 format 파라미터 미처리.
5. **AR-08** — `default: "json"` 미지정 (dart_mcp library 제약).
6. **DG-03(d)** — 그룹화 11개 도구 22개 action 분기 서브테스트 없음.

⚠️ 런타임 검증 미수행 — project.yaml 미설정. 모든 판정은 정적 검증 기반.

```

## iyaki-zip-dev

### sprint-contract.md (excerpt)
```markdown
---
feature: "sprint5-relationship-view + positions-migration + snapshot-scaffold"
created: "2026-04-21 00:05"
complexity: "복잡"
conditions: 38
---

# Sprint 5 Contract

## UI

- [ ] UI-01a: T1 구조 — 포트 hover/drag 핸들러, `createEdge`(또는 동명) 함수, edge 클릭 선택 핸들러, Delete/Backspace 핸들러가 각각 존재하며 EdgeLayer 에서 소비된다 [structural]
- [ ] UI-01b: T1 시나리오 — 포트 drag→drop 1 edge 생성, 직선 + 화살표 끝점 렌더, edge 클릭 선택, Delete/Backspace 삭제까지 순회 동작 [goal]
- [ ] UI-02a: T2 구조 — `EdgeStyle` enum(straight/bezier/orthogonal/step) 정의 + 스타일 전환 인라인 팝오버 컴포넌트 + `E` 키 글로벌 핸들러 존재 [structural]
- [ ] UI-02b: T2 시나리오 — 팝오버에서 4종 스타일 전환 반영 + 2+ 카드 선택 후 `E` 키로 선택 순서대로 체인 연결(A→B→C) [goal]
- [ ] UI-03a: T3 구조 — Force 뷰 진입/이탈 토글, 4 트리거 모드(`once | live | smart | off`) enum, drag-pin 3모드(`while-drag | permanent | disabled`) enum, 기본값 `pin-permanent` 상수 존재 [structural]
- [ ] UI-03b: T3 시나리오 — Force 뷰 진입 후 1000 노드 live 시뮬 수렴, 기본 drag-pin(pin-permanent) 동작, 4 트리거 모드 설정값 반영 [goal]
- [ ] UI-04a: T4 구조 — edge 라벨 렌더 컴포넌트 + `label.mode` 필드(`always | hover | never`) + `Edge.color/width` override 필드 + 생성 draw-in / 삭제 fade-out 애니메이션 훅 존재 [structural]
- [ ] UI-04b: T4 시나리오 — 라벨 모드 3종 전환 반영, per-edge 색상/굵기 override 렌더, edge 생성/삭제 애니메이션 재생 [goal]
- [ ] UI-05a: 뷰 전환 구조 — `ViewTransition` 모듈 + `transitionDurationMs` 설정 필드(기본값 200~400 범위) + easing 함수 참조가 존재 [structural]
- [ ] UI-05b: 뷰 전환 시나리오 — graph ↔ force 전환 시 카드/edge 좌표가 tween 으로 보간 이동(즉시 점프 0), 전환 duration ≥ 200ms, easing 적용, 전환 중 입력 이벤트는 블록 또는 현재 뷰 기준 처리, 완료 시점에 최종 뷰 활성 [goal]
- [ ] UI-0
```

### sprint-feedback.md (last 3000 chars)
```markdown
te.ts`가 `canvas-engine/src/` 하위 존재, react/tanstack/zustand import 0건 — PASS
  - 근거: 파일 위치 확인 (`apps/web/packages/canvas-engine/src/smartGuides.ts`, `alignDistribute.ts`). Grep 결과: react/tanstack/zustand import 없음.

- [x] AR-02: CanvasContextMenu가 `presentation/canvas/components/` 하위 존재 — PASS
  - 근거: `apps/web/src/presentation/canvas/components/CanvasContextMenu.tsx` 존재 확인.

- [ ] AR-03: OverlayCommand union에 `guideLine`, `distanceLabel` kind 추가 — FAIL
  - 근거: `types.ts:52-95` — `guideLine` kind 존재 (line 91-94). `distanceLabel` kind가 union에 없음. 계약은 두 kind 모두 요구. commit `70f1313`에서 descope되어 제거됨. 그러나 최종 계약(`sprint-contract.md` line 32)은 `distanceLabel`을 명시적으로 요구.
  - 수정: `distanceLabel` variant를 union에 추가 (최소한 미사용 placeholder로라도). 또는 계약 AR-03 텍스트를 `guideLine` only로 수정. 계약 수정은 사용자 권한.

### Anti-patterns (2/2)

- [x] AP-01: `: any`, `as any`, `<any>` 0건 (변경 파일 전체) — PASS
  - 근거: 13개 변경 파일 전체 grep — 매칭 없음.

- [x] AP-02: 가이드 선이 OverlayLayer 단일 Graphics에 렌더, 드래그 중 `new PIXI.Graphics()` 호출 0 — PASS
  - 근거: `DragController.ts` — Graphics 인스턴스 생성 없음. `Engine.ts:227` — overlayGraphics는 초기화 시 1회 생성. `OverlayLayer.ts` — 단일 graphics 재사용하여 `clear()` + redraw 패턴.

### Reusability (2/2)

- [x] RE-01: settings.smartGuides 필드 존재, updateSettings로 런타임 변경 가능 — PASS
  - 근거: `canvasStore.ts:173-178` — `settings.smartGuides: { ...DEFAULT_SMART_GUIDE_CONFIG }`. `canvasStore.ts:206-215` — `updateSettings` merges `partial.smartGuides`. Engine bridge (`useEngineBridge.ts:33`) — `engine.updateSmartGuideConfig(cfg)` 연결. `Engine.ts:495` — `updateSmartGuideConfig(partial)` 구현됨.

- [x] RE-02: align/distribute 함수 순수 함수 시그니처로 export — PASS
  - 근거: `index.ts:33-38` — 8개 함수 모두 named export. `canvasStore.test.ts`에서 직접 import하여 사용.

### Diagnostics (2/4)

- [x] DG-01: `pnpm typecheck && pnpm lint` 워닝 0개 — PASS
  - 근거: 두 명령 모두 에러/워닝 없이 종료.

- [ ] DG-02: IDE diagnostics 워닝/인포 0개 — [미검증]
  - 런타임 IDE 확인 불가.

- [x] DG-03: `pnpm test` 통과 + 콘솔 에러 0 — PASS
  - 근거: 70 tests passed (8 test files). "Not implemented: HTMLCanvasElement's getContext()" 메시지는 JSDOM 환경 제한 (canvas npm 미설치) — 실제 에러 아님, 테스트는 모두 통과.

- [ ] DG-04: 수동 스모크 에러 0 — [미검증]
  - MCP 서버 없음. 수동 실행 필요.

## Summary

- Total: 15 PASS / 20 조건 (LG-06, ER-03, DG-02, DG-04 미검증 제외 시 15/20)
- FAIL: LG-03, LG-04, AR-03 (3건)
- 미검증: LG-06, ER-03, DG-02, DG-04 (4건, 미검증 2건 이상 → REJECT 조건 추가 충족)
- Verdict: **REJECT**

## REJECT 사유 (우선순위순)

1. **LG-03 FAIL** — Alt+drag undo가 clone+move를 1 step으로 되돌리지 못함. `duplicateCardsInPlace`가 captureCommand를 사용하지 않아 clone 자체의 undo entry가 없음.

2. **LG-04 FAIL** — SmartGuides unit test에 3개 필수 케이스 누락 (경계값 exact, 동일좌표, 원점근방). 더불어 zoom != 1 시 threshold 스케일 미구현 (DragController가 threshold를 zoom으로 나누지 않음).

3. **AR-03 FAIL** — `distanceLabel` OverlayCommand union variant 미존재. 최종 계약이 명시적으로 요구. UI-02 descope가 계약 AR-03 조건까지 커버하지 않음.

4. **미검증 4건** — LG-06 (FPS), ER-03 (console.error), DG-02 (IDE), DG-04 (smoke). 미검증 2건 이상으로 REJECT 조건 추가 충족. (단, LG-06/DG-04는 "수동 측정 결과 기록" 조건이므로 인간 검증 후 별도 확인 필요)

⚠️ 런타임 검증 미수행 — MCP 서버 미설정

```
