---
feature: "카이젠 2026-09-24 Phase 5 계약 — codegen 필터 제거와 전후 삭제 수 · widget-inspector 관례 대조 · 위젯 시험 함정 · 카탈로그 타일 높이 · 특정 이름 빼기 · [미검증] 네 칸 · 틀린 버전 사실"
slug: kaizen-0924-p05-flutter-toolkit
created: "2026-09-25 05:22"
complexity: "복잡"
conditions: 26
status: done
owner_session: de8c7935-a5b6-4df5-9106-fafa73c288a0
conditions_digest: sha256:66138070ffba6c9a
locked_at: "2026-09-25 06:16"
---

## 배경

이 Phase 의 외부 근거는 `.harness/.meta/evidence/phase5.md` 하나다. 처리 배정표(`.claude/kaizen-input/insights-report.md`)에서
`배정` 칸이 `Phase 5` 인 행은 열이다. 러닝북 Phase 5 추가 과제가 셋이고, 앞 Phase 가 넘긴 것이 셋이다(`phase1-notes.md` ·
`phase3-notes.md` · `phase4-notes.md` 의 Phase 5 줄). 근거 파일 §3 현행화 점검도 입력이다.

| 키 | 내용 | 이번 처리 |
| --- | --- | --- |
| `F06` · `flutter:P-F06-codegen-delete-count` · `user-setup:P1` | build-filter 한 번이 생성물 267 개를 지웠다(§0-b `e19c3133`). 두 제안의 방향이 반대다 — 조건부로 남기기 대 전부 없애기. 대상 목록도 서로 하나씩 빠졌다(flutter-l10n · project-detection.md) | 반영 — **킷이 필터를 스스로 붙이지 않는다**(user-setup:P1 방향, 근거 §2 「킷이 자동 선택하지 않음」). 사용자가 프로젝트 전용 필터 명령을 이름으로 부를 때만 쓴다. 킷이 codegen 을 직접 돌리는 다섯 자리(run · build · preflight · l10n · transition)는 전후 삭제 수를 매번 센다(P-F06). 사용자에게 명령을 안내만 하는 세 자리는 다음 사이클(ER-01). 대상은 두 목록의 합집합에 transition 을 더한 것 — SK-01 · SK-02 · SK-03 · AR-01 |
| `F02` · `flutter:P-INSPECTOR-convention` | 기존 관례 무시 · 없는 위젯 지어냄 · 아이콘 뜻 오용(§0-b `00f4e982` · `cfa1f76f`). 대조할 기존 화면 수가 2 대 3 으로 갈린다 | 반영 — widget-inspector 감지 기준 7 (SK-04 · SK-05). 에이전트는 화면 수를 정하지 않고 호출 스킬의 관례 표만 읽는다(근거 §2 · §4.3) — 그래서 2 대 3 을 여기서 다시 정하지 않는다. 플러터 규약은 「2 개 이상」 그대로이고, 러닝북이 Phase 6 에 이 숫자로 맞추라고 했다 |
| `F24` · `flutter:P-TEST-locale-buildmod` | 기본 로캘 · 빌드 도중 provider 수정 때문에 시험 실패(§0-b `e19c3133`) | 반영 — flutter-test Gotcha 둘 (SK-06) |
| `F22` · `flutter:P-CATALOG-tile-height` | 카탈로그 타일 높이를 내용보다 낮게 고정 · 파일 이름 변경과 겹친 ProviderScope 로 스크롤이 멈춘 듯 보임(§0-b `cfa1f76f`) | 타일 높이는 반영 — flutter-widget 카탈로그 등록 절 (SK-07). 겹친 ProviderScope 부분은 미반영 — 근거 파일에 없다. 이름 변경 뒤 재시작 실패는 이번 스프린트 규약 Step 2 가 맡는다(처리 배정표 비고) |
| `F25` | 그룹 설정 시안 21 종 | 미반영 — 근거 §2 F25 · §4 6 번이 이번 Phase 에서 규칙을 만들지 말라고 권한다. 한 프로젝트 기억(「여러 개 다 만들어 나란히」)과 방향이 반대라 사용자 확인이 먼저다 (ER-01 이 notes 에 남긴다) |
| 러닝북 (1) | build-filter 방향을 하나로 | 위 `F06` 행 |
| 러닝북 (2) | 인사이트 스프린트가 넣은 것(편집 파일 포맷 훅 · flutter-ui-verify · 규약 보강)을 다시 넣지 않는다 | 셋 다 건드리지 않는다. 규약은 Step 4 의 `[미검증]` 두 줄과 증거 블록 한 줄 · 예시 한 줄만 고친다 (SK-09) |
| 러닝북 (3) | `flutter-transition/SKILL.md` 에 특정 앱 이름 | 반영 — 같은 종류를 킷 파일 전부에서 뺀다: 앱 이름 `fit-pal` 9 줄 · 프로젝트 이름 `apps` 4 줄 · 특정 화면 조종 도구 이름 2 줄 (SK-08) |
| Phase 1 넘김 | `visual-evidence-protocol.md:136` 「`[미검증]` 마커 + 사유 한 줄」 | 반영 — 같은 모양 여덟 줄을 같이 찾아 아홉 줄 전부 네 칸으로 (SK-09) |
| Phase 3 넘김 | `F31` 의 UI 관례 대조 | SK-04 가 받는다 |
| Phase 4 넘김 | `flutter-preflight` 에 기준 커밋 비교가 없다 — 「필요하면」 | 미반영 — 이 Phase 근거 파일에 기준 커밋 비교 근거가 없고(`git merge-base` 근거는 `phase4.md`), 선택 과제라 이번 묶음 수를 늘리지 않는다. 다음 사이클 (ER-01) |
| 근거 §3 현행화 | Freezed 「최신 stable 3.2.5」 · Flutter 「현재 stable 3.47.0」 | 지금 틀린 문장 아홉 줄만 고친다 (SK-10). go_router 18 · auto_route 11.1 은 새 내용을 더하는 일이고, Riverpod 3.4.1 두 줄은 조회 날짜가 붙어 틀리지 않았다 — 다음 사이클 (ER-01) |
| 근거 §3 `--delete-conflicting-outputs` | build_runner 2.16 부터 제거된 호환 옵션 | 「플래그 필수」 Gotcha 와 「항상 포함」 MUST 두 줄만 고친다 (SK-03). 명령 줄의 플래그를 판에 따라 뺄지는 다음 사이클 — 2.16 에서 이 옵션이 경고인지 오류인지 근거 파일이 밝히지 않았다 (ER-01) |

고칠 것은 일곱 갈래다.

1. **codegen 필터 (F06).** `flutter-run/SKILL.md:44` · `flutter-build/SKILL.md:48` · `flutter-preflight/SKILL.md:79` 이 feature 인자를 받으면
   `--build-filter="lib/features/$FEATURE/**"` 를 붙이고, `flutter-l10n/SKILL.md:125` 는 Slang 에 `--build-filter="lib/**/i18n/**"` 를,
   `project-detection.md:52` 는 `app-codegen-filter FILTER=...` 를 자동 대안으로 둔다. `flutter-transition/SKILL.md:303`(§5)은 날 codegen 한 줄을 그대로 돌린다.
   삭제를 세는 자리는 어디에도 없다.
   `flutter-run/SKILL.md:139` 는 「항상 `--delete-conflicting-outputs` 플래그 포함」 을 MUST 로, `flutter-build/SKILL.md:16` 은 「플래그 필수」 를 Gotcha 로 둔다
2. **관례 대조 (F02).** `widget-inspector.md` 감지 기준 여섯에 관례 대조가 없다. 부르는 두 스킬(`flutter-widget/SKILL.md:258` · `flutter-screen/SKILL.md:276`)이 관례 표를 넘기지 않는다
3. **시험 함정 (F24).** `flutter-test/SKILL.md` Gotchas(`:15-27`)에 로캘 고정 · 빌드 도중 provider 수정이 없다
4. **카탈로그 타일 (F22).** `flutter-widget/SKILL.md:226-235` 카탈로그 등록 절에 타일 높이 이야기가 없다
5. **특정 이름 (러닝북).** `fit-pal` 이 킷 파일 일곱 개 아홉 줄, `apps` 가 네 줄, 화면 조종 도구 이름이 `figma-parity-self-verify.md:46` · `:58` 에 있다
6. **`[미검증]` 사유 한 줄 (Phase 1 넘김).** 설계 가이드 §3.7 5 조항 3 항은 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 요구하는데
   규약 `:136` 과 스킬 일곱 줄 · 평가 사례 한 줄이 「마커와 사유」 로 남아 있다
7. **틀린 버전 사실 (근거 §3).** Freezed 「최신 stable 3.2.5」 여섯 줄(지금 4.0.2), Flutter 「현재 stable 3.47.0」 세 줄(지금 3.47.5)

카이젠 스킬 Gotcha 「Phase 1~4 신규 원칙 감사」: 이번 사이클 Phase 1 이 설계 가이드 §3.7 에 넣은 네 칸은 6 번으로 받는다. 같은 Phase 의
「알려진 답 대조」 는 이 킷에서 새 측정을 가르치는 자리가 codegen 블록 하나뿐이고, 그 블록은 이 계약이 알려진 답(SK-02)으로 잰다.
Phase 2 · 3 의 변경(계약 크기 · 평가자 확인 목록)은 flutter 스킬에 닿는 자리가 없다. Phase 4 의 `/sprint` 원인 가르기는 위 표의 넘김 행이다.

## 리서치 소스

외부 조회 0 회. 아래 URL 은 전부 근거 파일 `.harness/.meta/evidence/phase5.md` 에서 가져왔다.

- [build_runner CLI 옵션 소스](https://github.com/dart-lang/build/blob/master/build_runner/lib/src/build_runner_command_line.dart) · [build-filter 통합시험](https://github.com/dart-lang/build/blob/master/build_runner/test/integration_tests/build_command_build_filter_test.dart) — `--build-filter` 는 공식 옵션이다. 필터 밖 기존 생성물을 남긴다는 보장은 공식 자료에 없다 (SK-01)
- [build_runner CHANGELOG](https://raw.githubusercontent.com/dart-lang/build/master/build_runner/CHANGELOG.md) — 2.16.0 부터 잘못되거나 고쳐진 생성물을 기본으로 고치고, `--delete-conflicting-outputs` 는 제거된 호환 옵션 목록으로 옮겨졌다 (SK-03)
- [git-status](https://git-scm.com/docs/git-status) — `--porcelain=v1` 은 스크립트용 고정 형식이고 두 자리 가운데 어느 쪽의 `D` 도 삭제다. `grep -c` 는 0 건에 종료 코드 1 을 내 `set -e` 흐름을 끊는다 — 근거 파일의 `awk` 세기를 쓴다 (SK-02)
- [Flutter 국제화](https://docs.flutter.dev/ui/accessibility-and-internationalization/internationalization) · [WidgetsApp.locale](https://api.flutter.dev/flutter/widgets/WidgetsApp/locale.html) · [TestPlatformDispatcher.locale](https://api.flutter.dev/flutter/flutter_test/TestPlatformDispatcher/locale.html) — 기본 번역은 미국 영어뿐, locale 이 null 이면 시스템 로캘, 지원하지 않으면 `supportedLocales` 첫 항목, 시험 플랫폼 로캘은 바꿀 수 있다 (SK-06)
- [Riverpod DO/DON'T](https://riverpod.dev/docs/root/do_dont) · [useEffect](https://pub.dev/documentation/flutter_hooks/latest/flutter_hooks/useEffect.html) — 위젯이 provider 를 초기화하지 않는다, `useEffect` 는 build 중 동기로 불린다 (SK-06)
- [ListView](https://api.flutter.dev/flutter/widgets/ListView-class.html) · [NestedScrollView](https://api.flutter.dev/flutter/widgets/NestedScrollView-class.html) · [ScrollView.shrinkWrap](https://api.flutter.dev/flutter/widgets/ScrollView/shrinkWrap.html) — 겹친 스크롤은 저절로 협조하지 않는다, `shrinkWrap` 은 비용이 크다 (SK-07)
- [Flutter 배포 메타데이터](https://storage.googleapis.com/flutter_infra_release/releases/releases_macos.json) — stable 3.47.5 (2026-09-18) · [Freezed pub API](https://pub.dev/api/packages/freezed) · [Freezed CHANGELOG](https://raw.githubusercontent.com/rrousselGit/freezed/master/packages/freezed/CHANGELOG.md) — 4.0.2, Dart 3.13 · Analyzer 14, 생성자 파라미터 `final` 미지원 breaking (SK-10)

근거 파일이 스스로 밝힌 한계를 그대로 옮긴다: 필터가 필터 밖 생성물을 지운다는 공식 문장은 없다 — 267 개는 내부 실측이다(§5).
「고정 높이가 낮으면 안쪽이 스크롤을 먹는다」 는 공식 문장도 없다 — 겹친 스크롤이 협조하지 않는다는 공식 설명과 내부 실측을 합친 추론이다(§2 · §5).
그래서 SK-07 문장은 「멈춘 듯 보일 수 있다」 로 쓰고 적용 범위를 「안쪽이 따로 스크롤되길 의도하지 않은 타일」 로 좁혔다(근거 §2 반대 근거).
관례 대조와 시안 개수에는 외부 표준 근거가 없다(§5) — SK-04 는 규칙을 새로 정하지 않고 호출 스킬이 넘긴 표를 읽기만 한다.
삭제 수만으로 삭제의 옳고 그름은 가를 수 없다(§5) — SK-02 는 늘어난 경로를 열거하고 되돌리지 말라고 쓴다.

내부 입력: 데이터 풀 §0 처리 배정표 · §0-b (`e19c3133` · `00f4e982` · `cfa1f76f` · `3ac429d0`) · §0.5 [flutter] 세 건(참고만, `미분류` 는 근거로 쓰지 않는다) ·
§1 (`insights-0924-kaizen` DG-02 — `flutter-ui-verify/SKILL.md:23` MD025 는 시작 커밋에서 이미 고쳐져 있다: 시작 커밋 판에 markdownlint 경고 0).
앞 Phase notes 넷. 카탈로그 실측은 내부 피드백 `sprint-feedback-statistics-catalog.md:149`(2026-08-02 — 타일 높이 88 · 92 → 96, 렌더 시험 `+183 -2` → `+189`)를 직접 읽었다.

## GAP 분석 · 개선안 초안

### 1.1 복잡도 4 축

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 3 — 스킬 문서 열다섯 · 에이전트 하나 · 참조 문서 다섯(감지 절차 포함) · 평가 사례 |
| 공개 API·계약 변경 | 외부에 노출된 형태가 바뀌는가 | 예 — codegen 스킬 셋의 동작(필터를 안 붙이고 삭제 수를 센다)과 보고 형식, widget-inspector 리포트에 새 절 |
| 소비면 존재 | 이 형태를 받아 쓰는 반대편이 있는가 | 예 — 아래 Counterpart 표 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — flutter-toolkit 을 쓰는 모든 프로젝트의 codegen 이 필터 없이 돈다(느려질 수 있다), 새 멈춤 조건(`new` 가 0 이 아니면 멈춘다) |

네 축 가운데 셋이 「예」이고 공개 형태 변경과 소비면이 둘 다 「예」라 **복잡**이다. Step 2.5 Counterpart 조건을 넣는다
(SK-05 · SK-09 (c) · AR-01). 기능 조건은 16 개다 — 복잡 9~20 안이다 (SKILL.md Step 6.2 둘째 명령으로 이 파일을 세면 16).

카이젠 스킬 Gotcha 「scope-creep 은 unit(관심사) 수로」: 묶음은 일곱이다. 1 ~ 4 는 처리 배정표, 5 는 러닝북, 6 은 Phase 1 넘김이 이 Phase 에 준 것이고,
7 은 근거 파일이 짚은 **지금 틀린 문장**의 정정이다(새 내용을 더하지 않는다). 새 내용 추가(go_router 18 · auto_route 11.1)와 선택 넘김(preflight 기준 커밋 비교)은 다음 사이클로 미룬다.

### 1.2 설정 리터럴 대조표

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A 사유에 그대로 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A 사유에 그대로 |
| `diagnostics.ide_exclude` | `[]` | DG-02 에 그대로 |
| `contract_categories[].id` / `prefix` | `Skill`/`SK` · `Script`/`SC` · `Error`/`ER` · `Architecture`/`AR` | 조건 섹션 제목과 접두 그대로 |
| `anti_patterns[].id` / `message` | AP-01 · AP-02 · AP-03 · AP-04 | AP-01 · AP-03 · AP-04 선별, message 원문 그대로. AP-02(force push)는 이 Phase 가 밀어 넣지 않아서 뺀다 |

### 1.4 편집 전 감사 (실제로 읽은 줄 — 시작 커밋 `7925890` 판)

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 |
| --------- | ---------------------------- | ------------------- | ----------- |
| `flutter-toolkit/skills/flutter-run/SKILL.md` | `:18` (partial codegen Gotcha) · `:22` (앱 이름) · `:33-51` (codegen 절, `:44` 필터) · `:139` (플래그 MUST) | 필터 자동 · 삭제 세기 없음 · 앱 이름 | SK-01 · SK-02 · SK-03 · SK-08 |
| `flutter-toolkit/skills/flutter-build/SKILL.md` | `:16` (플래그 필수) · `:33` (Input) · `:37-49` (codegen, `:48` 필터) · `:69` (보고) | 필터 자동 · 삭제 세기 없음 · 2.16 과 어긋난 Gotcha | SK-01 · SK-02 · SK-03 |
| `flutter-toolkit/skills/flutter-preflight/SKILL.md` | `:18` (앱 이름) · `:40` (Input) · `:68-82` (codegen, `:79` 필터) · `:112` (보고) | 필터 자동 · 삭제 세기 없음 · 앱 이름 · 기준 커밋 비교 없음(넘김) | SK-01 · SK-02 · SK-08 |
| `flutter-toolkit/skills/flutter-l10n/SKILL.md` | `:121-127` (Codegen 표, `:125` Slang 필터) | i18n 폴더 필터 | SK-01 |
| `flutter-toolkit/references/project-detection.md` | `:36` (앱 이름 둘) · `:44` (타겟 목록) · `:52` (필터 타겟 자동 대안) · `:57` (app-build) | 필터 타겟 자동 · Make 타겟 안 codegen 을 세지 않음 | SK-01 · SK-08 |
| `flutter-toolkit/evals/evals.json` | `:8` · `:12-13` (사례 1 이 필터와 플래그를 기대) · `:66` (사례 5) · `:203` (사례 16) | 옛 동작을 기대 | AR-01 · SK-09 |
| `flutter-toolkit/agents/widget-inspector.md` | `:99` (프로젝트 이름) · `:101-120` (기준 6) · `:138-146` (Step 2) · `:172-176` (리포트) · `:209-220` (Rules) | 관례 대조 없음 | SK-04 · SK-08 |
| `flutter-toolkit/skills/flutter-widget/SKILL.md` | `:31` (3.47.0) · `:226-235` (카탈로그 등록) · `:256-258` (inspector 호출) · `:263` (사유) | 타일 높이 없음 · 관례 표 안 넘김 · 사유 한 줄 · 틀린 버전 | SK-05 · SK-07 · SK-09 · SK-10 |
| `flutter-toolkit/skills/flutter-screen/SKILL.md` | `:276` (inspector 호출) · `:282` (사유) | 관례 표 안 넘김 · 사유 한 줄 | SK-05 · SK-09 |
| `flutter-toolkit/skills/flutter-feature/SKILL.md` | `:191-193` (inspector 호출) | 관례 표를 만들지 않는 스킬 — 바꾸지 않는다 | SK-05 (c) |
| `flutter-toolkit/skills/flutter-extract/SKILL.md` | `:35` · `:41` (inspector 리포트를 읽는다) | 추출 후보만 읽는다 — 새 절은 후보가 아니라 바꾸지 않는다 | — (Counterpart 표) |
| `flutter-toolkit/skills/flutter-transition/SKILL.md` | `:16` (앱 이름) · `:19` (3.47.0) · `:299-304` (§5 codegen, `:303` 날 codegen) · `:315` (사유) | 앱 이름 · 틀린 버전 · 삭제 세기 없는 codegen · 사유 한 줄 | SK-01 · SK-08 · SK-09 · SK-10 |
| `flutter-toolkit/skills/flutter-api` · `flutter-feature` · `flutter-screen` 의 `SKILL.md` | `:336` · `:151` · `:272` (사용자에게 보여 주는 codegen 안내) | 전후 삭제 수 블록을 가리키지 않는다 — 킷이 직접 돌리지 않는 안내라 이번에 바꾸지 않는다 | ER-01 (다음 사이클) |
| `flutter-toolkit/skills/flutter-skeleton/SKILL.md` · `flutter-responsive/SKILL.md` | `:184` · `:152` (사유) | 사유 한 줄 | SK-09 |
| `flutter-toolkit/skills/flutter-test/SKILL.md` | `:15-27` (Gotchas) · `:155` (사유) | 로캘 · 빌드 도중 수정 없음 · 사유 한 줄 | SK-06 · SK-09 |
| `flutter-toolkit/skills/flutter-hooks/SKILL.md` | `:21` · `:25` (프로젝트 이름) · `:27` (사유) · `:28` (3.2.5) | 이름 · 사유 · 틀린 버전 | SK-08 · SK-09 · SK-10 |
| `flutter-toolkit/skills/flutter-provider/SKILL.md` · `flutter-api` · `flutter-error` · `flutter-audit` | provider `:21` · `:31` · api `:20` · error `:20` · audit `:179` | 3.2.5 · 앱 이름 | SK-08 · SK-10 |
| `flutter-toolkit/references/flutter-ai-rules.md` | `:55` (codegen 예시 — 바꾸지 않는다) · `:83-90` (Freezed 절, `:86` 3.2.5) · `:103` (3.47.0) · `:111` (제목의 이름) | 틀린 버전 · 이름 | SK-08 · SK-10 |
| `flutter-toolkit/references/primitive-substitution-gate.md` · `figma-parity-self-verify.md` | `:13` · `:46` · `:58` | 앱 · 도구 이름 | SK-08 |
| `flutter-toolkit/references/visual-evidence-protocol.md` | `:3` (판) · `:121-142` (Step 4, `:136-137`) · `:156` · `:164` | 사유 한 줄 | SK-09 |
| `docs/flutter/research-log.md` | `:7` (제목) · `:9` (직전 항목 2026-08-13) | 이번 항목 없음 | AR-02 |
| `harness/docs/guides/skill-design-guide.md` (읽기만) | `:302-310` (§3.7 5 조항 3 항 네 칸 · `[미검증:INVALID]`) | 규약이 인용할 원문 — 이 Phase 가 고치지 않는다 | SK-09 (d) |

구현 후보가 둘 이상이었던 곳의 선택:

- **build-filter 방향** — 조건부 유지(P-F06) 대 전부 없애기(user-setup:P1). **킷이 스스로 붙이지 않는다.** 근거 §2 가 「필터 사용 자체 금지」 보다
  「킷이 자동 선택하지 않음」 이 정확한 문구라고 권한다 — 사용자가 프로젝트 전용 필터 명령을 이름으로 부르면 그 명령을 첫 codegen 줄에 넣고,
  두 번째 줄은 필터 없는 전체로 둔다. 삭제 세기는 두 방향 어느 쪽이든 필요해 둘 다 반영한다
- **삭제를 무엇으로 셀지** — 개수 대 경로 집합. **경로 집합**(`comm -13`)이다. 개수로만 비교하면 하나가 돌아오고 다른 하나가 지워진 경우를 놓친다.
  다시 돌린 뒤에는 **첫 `BEFORE` 와** 비교한다 — 다시 재면 늘어난 삭제가 기준에 섞여 늘 0 이 된다(`회귀 게이트` 절 변이 N1 이 이 실수를 잡는다).
  다시 돌리기를 블록 안에 넣었다 — Bash 도구는 호출 사이에 셸 변수를 넘기지 않아, 「같은 블록을 한 번 더」 로 쓰면 `BEFORE` 가 사라진다.
  블록의 끝 줄은 종료 코드 판정이다 — codegen 명령 하나였던 옛 판은 실패를 종료 코드로 알렸는데, 세기 줄을 덧붙이면 마지막 `printf` 가 성공해 그 실패가 가려진다
- **블록을 어디 둘지** — `flutter-run` 한 곳 대 세 스킬. **세 스킬에 글자 그대로 사본**이다. `flutter-preflight` 의 fix 블록이 이미 `flutter-run` 사본이라
  같은 방식을 따른다. 사본이 갈라지는 것은 SK-02 (a) 가 해시로 막는다
- **`--delete-conflicting-outputs`** — 명령 줄에서 뺄지 대 규칙 두 줄만 고칠지. **규칙 두 줄만.** 근거 §4 2 번은 「MUST 로 두지 않는다」 까지만 권하고,
  2.16 에서 이 옵션이 경고인지 오류인지는 근거 파일에 없다. 명령 줄 열한 곳을 판에 따라 가르는 일은 다음 사이클이다
- **관례 대조를 어느 모드에서** — quick 만. 근거 §4 3 번. deep 은 호출 스킬의 표가 없다
- **`[미검증]` 네 칸 범위** — 규약 한 줄(넘김 원문) 대 같은 모양 전부. **전부 아홉 줄.** 같은 규칙이 박힌 자리를 한 곳씩 고치면 안 고친 곳에서 같은 일이 난다.
  평가 측 자리(`flutter-audit/SKILL.md:50` · `widget-inspector` 의 `[미검증]` 줄)는 모양이 다르고 평가 쪽 가이드와 함께 볼 일이라 다음 사이클로 넘긴다(ER-01)
- **틀린 버전 사실** — 모든 버전 줄 대 지금 틀린 문장만. **지금 틀린 문장만**(Freezed 여섯 · Flutter 셋). 조회 날짜가 붙은 옛 사실(Riverpod 3.4.1 두 줄 ·
  go_router 17.2.2)은 날짜 기준으로 참이라 고치지 않는다
- **특정 이름** — `flutter-transition` 한 줄 대 킷 전부. **킷 파일 전부**(러닝북 규칙 「특정 앱 이름·특정 MCP 서버 이름을 킷 파일에 넣지 마라」). `docs/` 의 옛 조사 기록은
  지난 사이클 기록이라 건드리지 않는다

### Counterpart — 바뀌는 형태를 받아 쓰는 반대편

| 파일 | 인용 | 이번 처리 |
| --- | --- | --- |
| `flutter-toolkit/evals/evals.json` 사례 1 · 5 · 16 | codegen 필터 · 사유 한 줄 · inspector 리포트를 기대 | 새 동작으로 바꾼다 — AR-01 · SK-09 (c) |
| `flutter-toolkit/skills/flutter-widget` · `flutter-screen` (inspector 호출) | quick 모드로 부른다 | 관례 표를 넘긴다 — SK-05 |
| `flutter-toolkit/skills/flutter-feature/SKILL.md:193` | quick 모드로 부른다 | 관례 표를 만들지 않는 스킬이라 그대로 — 에이전트가 `[미검증] 관례 표 없음` 을 적는다. SK-05 (c) 가 이 절이 안 바뀌었는지 잰다 |
| `flutter-toolkit/skills/flutter-extract/SKILL.md:41` | inspector 리포트의 추출 후보를 읽는다 | 새 절은 추출 후보가 아니다(SK-04 「Total 에 더하지 않고」) — 그대로 |
| `flutter-toolkit/references/project-detection.md:57-58` | `$MAKE app-build` · `$MAKE app-preflight` 가 안에서 codegen 을 돌린다 | 그 타겟을 블록의 codegen 줄 자리에 넣어 센다 — SK-01 (b) |
| `harness/docs/guides/skill-design-guide.md` §3.7 | 네 칸 원문 | 읽기만 — SK-09 (d) 가 `$END` 판에 원문이 있는지 잰다 |
| `docs/flutter/*.md`(research-log 밖) · `docs/kaizen/flutter-*.md` | 지난 사이클 기록 | 건드리지 않는다. `docs/kaizen/flutter-changelog.md` · `flutter-research-log.md` 는 Final 이 notes 로 쓴다 — ER-01 |

### 개선안 초안

정확한 문구는 스크래치 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p5draft/mock.py`
가 시작 커밋 판 스물세 파일에 적용하는 62 치환 그대로다(`python3 mock.py <트리>` — 옛 문자열이 정확히 한 번 있어야 적용하고, 아니면 멈춘다).
검토 반영 전 판은 같은 폴더의 `mock-v1.py`(61 치환)다. BUILD 는 `mock.py` 를 기준으로 적용한다. 요지:

- `flutter-run` · `flutter-build` · `flutter-preflight` — feature 인자를 받아도 필터를 안 붙인다는 문장, 전후 삭제 수 블록(세 파일 같은 글자),
  `new` 가 남으면 멈추고 목록을 보이되 되돌리지 않는다는 문장, 생성물을 git 에 올리지 않는 프로젝트에서는 세기가 늘 0 이라 `new=0` 을 통과로 쓰지 말라는 문장(블록 바로 아래 문단),
  보고 줄. `flutter-run` Gotcha · Rules MUST, `flutter-build` Gotcha(2.16), 두 Input 줄
- `flutter-l10n` — Slang 줄 필터 제거와 한 문장. `project-detection.md` — 매핑 줄과 Make 타겟 안 codegen 한 문장, 앱 이름 두 곳
- `flutter-transition` `### 5. Codegen (필요 시)` — 날 codegen bash 블록을 「`HAS_GO_ROUTER_BUILDER`이면 route codegen 을 `flutter-run` codegen 절의 블록으로 돌린다 — 전후 삭제 수를 센다.」 한 문장으로 바꾼다
- `widget-inspector.md` — `### 7. 관례 대조` 절, Step 2 일곱 가지, 리포트 틀 `Convention Match`, Rules MUST 한 줄, 출처 줄 이름
- `flutter-widget` · `flutter-screen` — inspector 호출에 관례 표 넘기기. `flutter-widget` 카탈로그 타일 문단
- `flutter-test` — Gotcha 둘
- 이름 빼기 열한 곳, `[미검증]` 네 칸 아홉 곳(규약 판 1.2.0), 버전 정정 아홉 곳과 `flutter-ai-rules.md` Freezed 4.0 한 줄
- `evals.json` 사례 1 · 5 · 16. `docs/flutter/research-log.md` 머리에 2026-09-25 항목(「킷이 codegen 을 직접 돌리는 다섯 자리는 전후 삭제 수를 매번 센다」 로 적는다)

## 범위 경계

- 이 Phase 시작 HEAD: `79258900de00e621412e4c436b44028a77d7fb64`. 범위 상한은 개정 파일 `.harness/sprint-amendments-kaizen-0924-p05-flutter-toolkit.md` 의 `end_sha:`
  마지막 값이다. 여러 Phase 가 같은 가지 `kaizen/2026-09-24` 에 동시에 커밋하므로 `HEAD` 로 재지 않는다
- 고치는 파일은 스물셋이다 — `docs/flutter/research-log.md` · `flutter-toolkit/agents/widget-inspector.md` · `flutter-toolkit/evals/evals.json` ·
  `flutter-toolkit/references/` 의 `figma-parity-self-verify.md` · `flutter-ai-rules.md` · `primitive-substitution-gate.md` · `project-detection.md` · `visual-evidence-protocol.md` ·
  `flutter-toolkit/skills/` 의 `flutter-api` · `flutter-audit` · `flutter-build` · `flutter-error` · `flutter-hooks` · `flutter-l10n` · `flutter-preflight` · `flutter-provider` ·
  `flutter-responsive` · `flutter-run` · `flutter-screen` · `flutter-skeleton` · `flutter-test` · `flutter-transition` · `flutter-widget` 의 `SKILL.md`. 새 파일은 없다.
  `.harness/` 쪽은 이 계약 · 개정 파일 · QA 피드백 · `.harness/.meta/kaizen-0924/phase5-notes.md` · `.harness/.meta/kaizen-0924/phase5-review.md` 를 쓴다 — 슬러그를 나열하지 않고 AR-03 ③ `verify_seal` 로 잰다
- **이 Phase 의 커밋 메시지에는 전부 `Co-Authored-By` 줄 바로 위에 서명 줄 `Kaizen-Phase: kaizen-0924-p05-flutter-toolkit` 한 줄을 넣는다** (봉인 커밋 포함).
  AR-03 · ER-01 · SC-00 · DG-01 · DG-03 · DG-04 · RE-01 이 이 줄로 이 Phase 커밋을 가린다(`harness/references/contract-schema.md` §여러 주체가 한 가지에 커밋할 때 선택지 B).
  서명을 빠뜨린 커밋은 서명 줄 목록에 안 보이므로 AR-03 ① 과 ER-01 넷째 측정은 경로로 직접 센다.
  FIX 가 커밋을 더할 때도 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다(옛 줄은 지우지 않는다). notes 커밋도 이 Phase 커밋이다 — notes 를 커밋한 뒤 그 sha 로
  `end_sha:` 줄을 하나 더 덧붙여 커밋한다
- 구현 커밋은 **`git add -- <파일…> && git commit -o -- <파일…>` 로 스물셋 파일만** 싣는다. 한 커밋에 킷 하나 — `flutter-toolkit/` 스물둘과 `docs/flutter/research-log.md` 는
  한 커밋이어도 되고 둘로 나눠도 된다(`docs/flutter/` 는 킷 폴더가 아니다)
- 측정이 기대는 제목은 이름을 바꾸지 않는다: `### codegen [feature]` · `## Gotchas` · `## Rules` (flutter-run) · `### 1. codegen [feature]` · `### 3. Report` (flutter-build) ·
  `### 2. codegen [feature]` · `### 5. Report` (flutter-preflight) · `### 6. Codegen 실행` (flutter-l10n) · `### Step 2b.` (project-detection) · `### Step 2: 감지 실행` ·
  `### Step 3: 리포트 생성` · `## Rules` · 새로 만드는 `### 7. 관례 대조` (widget-inspector) · `## Post-Creation: Widget Inspector` · `## Post-Creation: Visual Evidence` · `### 7. Widgetbook/Storybook 등록` (flutter-widget) ·
  `## Post-Creation: Widget Inspector` · `## Post-Creation: Visual Evidence` (flutter-screen) · `## Post-Creation: Widget Inspector` (flutter-feature) ·
  `### 5. Codegen` · `## Gotchas` · `## Rules` (flutter-transition) · `## Gotchas` (flutter-hooks) · `## Rules` (flutter-responsive) ·
  `### 5. 체크리스트` (flutter-skeleton) · `## Gotchas` · `### 5. 결과 제시` (flutter-test) · `## Step 4` · `## Visual Evidence Block` (규약) · `### Freezed` (flutter-ai-rules) ·
  `## 3.7.` (skill-design-guide — 읽기만). 이름이 바뀌면 `sect` 가 빈 글을 내 값이 0 이 된다 — FAIL 쪽으로 틀린다 (2 회차 검토 D4 로 transition · hooks · responsive · test 제목을 더했다)
- 공유 파일(`marketplace.json` · `plugin.json` 버전 · 루트 README · 루트 CLAUDE.md · `docs/` HTML · 처리 배정표 · 감사 로그 · 실패 횟수 파일 · `docs/kaizen/*.md` ·
  `.github/workflows/ci.yml`)과 다른 Phase 소관 파일(`harness/` 전부)은 건드리지 않는다 — ER-01 셋째 · 넷째 측정. flutter-toolkit README 의 AUTO 구간은 스킬 frontmatter 를
  읽는데 frontmatter 를 바꾸지 않는다. 문서 사이트 재생성은 Final F2 몫이다 — 이 Phase 는 `harness/docs/guides/` · `harness/references/` 를 건드리지 않아 `docs-site-regen` 은 SKIP 이다
- 넘기는 것 — BUILD 가 notes(`.harness/.meta/kaizen-0924/phase5-notes.md`)에 아래 스물두 문자열을 **각각 한 번 이상** 적는다(ER-01 이 센다 — 짧은 키 일곱 `F02` · `F06` · `F22` · `F24` · `F25` · `F31` · `user-setup:P1` 은 낱말 경계로 세므로 백틱으로 감싸거나 뒤를 띄어 쓴다. `F06은` 처럼 조사를 바로 붙이면 0 이다):
  처리 배정표 키 열 `F02` · `F06` · `F22` · `F24` · `F25` · `flutter:P-F06-codegen-delete-count` · `flutter:P-INSPECTOR-convention` · `flutter:P-TEST-locale-buildmod` ·
  `flutter:P-CATALOG-tile-height` · `user-setup:P1` 과 넘김 열둘 — `visual-evidence-protocol.md:136` (Phase 1 넘김, 반영) · `F31` (Phase 3 넘김, SK-04 로 반영) ·
  `flutter-preflight` (Phase 4 넘김 미반영 — 다음 사이클 Phase 5, 근거 파일에 기준 커밋 비교 근거가 오면 `/sprint` Step 3 판정 세 줄을 옮긴다) ·
  `ProviderScope` (F22 의 겹친 ProviderScope 부분 — 근거 없음) · `go_router` · `auto_route` (근거 §3 의 새 내용 — 다음 사이클) ·
  `--delete-conflicting-outputs` (명령 줄의 플래그를 판에 따라 뺄지 — 다음 사이클, 2.16 에서 경고인지 오류인지 근거 필요) ·
  `flutter-audit/SKILL.md:50` (평가 측 `[미검증]` 형식 — 평가 쪽 가이드와 함께 다음 사이클) ·
  `flutter-feature/SKILL.md:151` (사용자에게 보여 주는 codegen 안내 셋 `flutter-api/SKILL.md:336` · `flutter-feature/SKILL.md:151` · `flutter-screen/SKILL.md:272` 은 전후 삭제 수 블록을 가리키지 않는다 — 다음 사이클) ·
  `$DART test` (evals 사례 18 의 「생성 후 $DART test로 검증한다」 가 flutter-test Step 4 의 `$FLUTTER test` 와 어긋난다 — 다음 사이클) ·
  `docs/kaizen/flutter-changelog.md` (Final 이 notes 의 changelog 단락으로 쓴다) · `Phase 6` (대조할 기존 화면 수는 플러터 규약 「2 개 이상」 · 스스로 고치기 상한 「3 회」 그대로다 — 이 Phase 가 바꾸지 않았다).
  **그 가운데 셋은 사유와 한 줄에 쓴다** — `flutter-preflight` 는 `기준 커밋` 과, `--delete-conflicting-outputs` 는 `경고인지 오류인지` 와, `Phase 6` 은 `2 개 이상` 과 같은 줄에.
  세 낱말은 바꾼 파일 목록 · changelog 단락 · 다른 메모에도 거의 반드시 나와서, 낱말만 세면 넘김 줄을 빠뜨려도 1 이 나온다(검토 실측 2026-09-25 — ER-01 봉인 전 실측).
  러닝북이 적게 한 나머지(바꾼 파일 · changelog 한 단락 · 킷 로그 한 단락 · 다음 사이클 메모)도 notes 에. 다음 사이클 메모에는 두 줄을 더 적는다(ER-01 이 세지 않는다):
  §0-b 의 `3ac429d0` 세션(기기 경합 · 스크롤 대상 재시도)은 인사이트 스프린트가 넣은 flutter-ui-verify 몫이라 이번에 손대지 않았다 ·
  규약 `visual-evidence-protocol.md` 판이 1.2.0 으로 올라 Final F2 의 문서 사이트 재생성 대상에 그대로 든다.
  `.github/workflows/ci.yml` 에 넣을 줄은 없다 — 새 시험 파일이 없다.
  Final 이 더 할 것: flutter-toolkit `plugin.json` 버전 — 카이젠 스킬 버전 판단표로 스킬 프롬프트 · eval 기준 변경이라 minor
- QA(`harness:qa-evaluator`)는 설치본이다 — 이 Phase 가 고치는 파일에 harness 파일은 없다
- 사용자 승인(Step 5) 대체: 사용자가 「자동으로 끝까지 알아서 진행해 내 허락이 필요한건 코덱스로 리서치나 검토받고」라고 위임했다(세션
  `de8c7935-a5b6-4df5-9106-fafa73c288a0` 기록 queued_command `2026-09-24T04:04:16.964Z`). Codex 사용량 한도가 소진돼(오류 원문 「You've hit your usage limit … try
  again at 11:05 PM」, 2026-09-24) 독립 Claude 검토자(REVIEW 에이전트)가 대신한다. 이어 사용자가 「코덱스 대신에 그냥 너가 알아서 진행하라고」라고 명시했다(같은 세션
  기록 user `2026-09-24T11:54:58.940Z`). 검토 결과 파일: `.harness/.meta/kaizen-0924/phase5-review.md`. 검토 VERDICT: 1 회차 `CHANGES` — 고칠 것 넷(C1 bash 가 아니면 멈춤 ·
  C2 ER-01 세 낱말을 사유와 한 줄로 · C3 transition §5 codegen · C4 생성물을 추적하지 않는 저장소)과 막지 않는 제안 셋(O1~O3)을 초안이 전부 반영했다. 2 회차 `APPROVE` —
  봉인을 막을 결함 없음. 막지 않는 권장 넷(D1~D4)은 BUILD 가 봉인 전에 반영했다 — D1 은 이 절 「넘기는 것」 의 괄호, D4 는 「측정이 기대는 제목」 목록(산문),
  D2 · D3 은 SK-01 조건 줄과 측정을 넓혔다(l10n 두 문장 · 따옴표 없는 필터). D2 · D3 으로 바뀐 값은 BUILD 가 시작 커밋 판 · 모의본 · 양성 대조 · 문장 삭제 대조로 다시 쟀다(`회귀 게이트` 절)
- 오라클 해소: SK-01 (b) · SK-02 (c) · SK-03 · SK-04 · SK-05 · SK-06 · SK-07 · SK-08 (c) · SK-09 (b)(c)(d) · SK-10 (b)(c) — 산출물이 스킬 · 문서 문장 자체라 정해진 절 구간에
  정해진 문장이 있는지가 판정이다. `sect` 가 코드 펜스 안 `#` 줄을 제목으로 보지 않고 절을 잘라 재며, 시작 커밋 판에서 새 문장 0 · 옛 문장 1 을 봉인 전에 확인했다.
  문장 하나만 지운 사본에서 그 값이 1 → 0 으로 떨어지는지 62 경우 전부 돌렸다(`회귀 게이트` 절)
- 오라클 해소: SK-02 (b) — 블록을 떼어 답을 아는 다섯 저장소에서 실제로 돌린 출력이다. 알려진 답(손으로 센 삭제 수)과 변이 다섯(N1 ~ N5)의 음성 대조가 붙어 있다.
  블록 awk 의 `$(0)` · `${1}` 을 `$0` · `$1` 로 되돌리면 알려진 답은 그대로 통과하지만 DG-05 (a) 의 V9(`arg-substitution`)가 `3 arg-substitution hazard(s)` 로 잡는다(검토 변이 2026-09-25)
- 오라클 해소: SK-01 (a) · SK-01 (b) 의 transition 옛 codegen 줄 · SK-08 (a)(b) · SK-09 (a) · SK-10 (a) — 0 이 기대값이고, 시작 커밋 판이 각각 1 이상을 낸다(양성 대조)
- 오라클 해소: AR-01 — `evals.json` 을 파싱해 필드를 비교한 출력과 `run-evals.py` 출력이다. AR-02 — 더한 줄의 URL 을 근거 파일 URL 과 대조한 출력이다
- 오라클 해소: ER-01 · AR-03 · SC-00 · DG-01 · DG-03 · DG-04 · RE-01 — 커밋 기록(`git log`)과 notes 문자열 · 봉인 검증 함수를 실제로 돌린 출력이다
- 오라클 해소: DG-02 · DG-05 · DG-06 — 린터 · 검사 스크립트를 실제로 돌린 출력이다
- 오라클 해소: SK-09 — 산출물이 규약 · 스킬 문장 자체다. (a) 는 옛 모양이 시작 커밋 판에서 9 줄 나오는 양성 대조를, (b)(c) 는 문장 삭제 대조 열한 경우를 봉인 전에 돌렸다
- 오라클 해소: AP-01 — 더한 줄을 실제로 뽑아 버전 문자열을 센다. 양성 대조(버전 줄 한 줄을 더한 사본에서 1)를 봉인 전에 돌렸다
- 오라클 해소: AP-03 — `validate-plugin.py` V6 상태기계를 실제로 돌린 출력이다. 양성 대조(맨 펜스를 더한 사본에서 `1 bare`)를 봉인 전에 돌렸다
- 오라클 해소: DG-05 — 검사 스크립트 다섯과 훅 시험을 실제로 돌린 종료 코드 · 출력이다. 뒤따르는 대조는 그 출력의 파일 경로를 이 Phase 파일과 맞출 뿐이다
- 커버리지 해소: SK-01 ~ SK-10 · AR-01 · AR-02 — 산문의 파일 이름은 측정의 `"$RUN"` · `"$BLD"` · `"$PRF"` · `"$L10N"` · `"$PD"` · `"$WI"` · `"$WG"` · `"$SCR"` · `"$TST"` ·
  `"$TRN"` · `"$VEP"` · `"$AIR"` · `"$EV"` · `"$S/flutter-<이름>/SKILL.md"` 다. 공통 정의가 그 이름으로 `$END` 판을 꺼낸다. 도우미 이름(`delgate.sh` · `new-warnings.sh` · `ar01.sh`)은 측정의 `"$K/…"` 로 부른다
- 커버리지 해소: SK-01 — 검출기가 짚은 `flutter-toolkit/` 과 그 안의 `flutter-run/SKILL.md` · `flutter-build/SKILL.md` · `flutter-preflight/SKILL.md` · `flutter-l10n/SKILL.md` · `evals.json` 은 (a) 첫 측정의 `"$E/$FT"`(킷 전체를 `grep -r` 로 훑는다)이고,
  `project-detection.md` 는 (a) 둘째 측정의 `"$PD"` 다. (b) 는 같은 파일을 `"$RUN"` · `"$BLD"` · `"$PRF"` · `"$L10N"` · `"$PD"` · `"$TRN"` 으로 연다(공통 정의가 `$END` 판 경로로 푼다)
- 커버리지 해소: SK-09 — `evals.json` 은 `"$EV"`, `flutter-toolkit/` 은 (a) 의 `"$E/$FT"`, `harness/docs/guides/skill-design-guide.md` 는 (d) 의 `"$E/harness/docs/guides/skill-design-guide.md"` 다
- 커버리지 해소: SK-10 — `flutter-ai-rules.md` 는 `"$AIR"`, `flutter-toolkit/` 은 (a) 의 `"$E/$FT"` 다
- 커버리지 해소: SK-08 — `fit-pal` · `apps` · 도구 이름은 측정의 `grep` 정규식 인자다. SK-09 — 스킬 일곱 개는 측정 (c) 의 `sect` 인자 순서 그대로다
- 커버리지 해소: ER-01 — notes 경로 `.harness/.meta/kaizen-0924/phase5-notes.md` 는 공통 정의의 `$NOTES`, 스물두 문자열(`flutter-audit/SKILL.md:50` · `flutter-feature/SKILL.md:151` 포함)은
  측정 `for t in …` 두 줄과 같은 줄 세기 한 줄(`flutter-preflight` · `--delete-conflicting-outputs` · `Phase 6`)의 인자다
- 검출기는 공백 든 코드 조각 안의 인자를 읽지 못한다 — 위 해소 줄이 전부 그 경우다
- 편집 전부터 있던 마크다운 경고(MD060 · MD032 등)는 범위 밖이다 — DG-02 는 더한 줄에 새로 걸린 경고만 잰다
- 기능 조건 16 · 전체 조건 줄 26

## 회귀 게이트 — 측정 공통 정의와 봉인 전 실측

모든 조건의 측정은 아래 블록을 먼저 실행한 **bash** 셸에서 돈다 — 블록과 측정을 한 `bash -c` 안에 넣거나 블록을 파일로 저장해 `. 파일` 뒤에 잇는다.
`END_UNRESOLVED` 가 찍히면 셸이 종료 코드 2 로 끝난다. 이 절의 도우미 코드 블록 셋은 각 블록 첫 `#` 주석 줄(셔뱅 다음)에 적힌 이름 그대로 한 폴더에 저장하고,
그 폴더를 공통 정의 블록을 돌리기 전에 `K` 에 넣는다. `new-warnings.sh` 옆에는 `node_modules` 를
`/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p1build/node_modules` 로 잇고
`cfg.markdownlint-cli2.jsonc` = `{ "config": { "MD013": false } }` 를 둔다 — 준비 단계 실측: 그 자리의 `.bin/markdownlint-cli2 --version` 첫 줄이
`markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)` (2026-09-25). 없으면 그 폴더에서 `npm install --no-save markdownlint-cli2@0.23.2` 부터 돌린다.
준비 단계 실측(2026-09-25): `command -v zsh` → `/bin/zsh` (5.9) · `/bin/bash --version` 3.2.57 · `git --version` 2.53.0 · `command -v comm` → `/usr/bin/comm` · `python3 --version` 3.x.
Claude Code 의 zsh 는 `grep` 을 다른 검색 프로그램으로 바꿔 부른다 — SK-08 (b) 가 시작 커밋 판에서 bash 4 · zsh 0 으로 갈렸다(검토 실측 2026-09-25, 초안 재실측 같음). 그래서 블록은 bash 가 아니면 멈춘다.

```bash
# 측정 공통 정의 — bash 로 실행한다 (zsh 는 배열 첨자가 1 부터이고 따옴표 없는 변수를 쪼개지 않는다)
[ -n "${BASH_VERSION:-}" ] || { echo "NOT_BASH — 이 블록과 측정을 bash -c 안에서 다시 돌린다"; exit 2; }
export LC_ALL=C.UTF-8
cd /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/kaizen-0924 || exit 2
B=79258900de00e621412e4c436b44028a77d7fb64                  # 이 Phase 시작 HEAD
SIG='Kaizen-Phase: kaizen-0924-p05-flutter-toolkit'
CF=.harness/sprint-contract-kaizen-0924-p05-flutter-toolkit.md
AM=.harness/sprint-amendments-kaizen-0924-p05-flutter-toolkit.md
NOTES=.harness/.meta/kaizen-0924/phase5-notes.md
EVID=.harness/.meta/evidence/phase5.md
: "${K:?도우미 폴더를 K 에 넣는다}"
FT=flutter-toolkit
END=$( [ -f "$AM" ] && sed -n 's/^end_sha:[[:space:]]*//p' "$AM" | tail -1 )
if [ -z "$END" ] || ! git rev-parse -q --verify "$END^{commit}" >/dev/null; then
  echo "END_UNRESOLVED — 측정을 멈추고 BUILD 에 묻는다. HEAD 로 바꿔 재지 않는다"; exit 2
fi
T=$(mktemp -d); mkdir -p "$T/B" "$T/E"
# 두 판을 풀어 둔 폴더에서 잰다 — 작업 폴더에 남은 다른 Phase 의 미커밋 변경이 끼지 않는다
git archive "$B" | tar -x -C "$T/B"; git archive "$END" | tar -x -C "$T/E"
E=$T/E
FILES=(docs/flutter/research-log.md
  $FT/agents/widget-inspector.md $FT/evals/evals.json
  $FT/references/figma-parity-self-verify.md $FT/references/flutter-ai-rules.md
  $FT/references/primitive-substitution-gate.md $FT/references/project-detection.md
  $FT/references/visual-evidence-protocol.md
  $FT/skills/flutter-api/SKILL.md $FT/skills/flutter-audit/SKILL.md $FT/skills/flutter-build/SKILL.md
  $FT/skills/flutter-error/SKILL.md $FT/skills/flutter-hooks/SKILL.md $FT/skills/flutter-l10n/SKILL.md
  $FT/skills/flutter-preflight/SKILL.md $FT/skills/flutter-provider/SKILL.md $FT/skills/flutter-responsive/SKILL.md $FT/skills/flutter-run/SKILL.md
  $FT/skills/flutter-screen/SKILL.md $FT/skills/flutter-skeleton/SKILL.md $FT/skills/flutter-test/SKILL.md
  $FT/skills/flutter-transition/SKILL.md $FT/skills/flutter-widget/SKILL.md)
FRE='docs/flutter/research-log\.md|flutter-toolkit/(agents/widget-inspector\.md|evals/evals\.json|references/(figma-parity-self-verify|flutter-ai-rules|primitive-substitution-gate|project-detection|visual-evidence-protocol)\.md|skills/flutter-(api|audit|build|error|hooks|l10n|preflight|provider|responsive|run|screen|skeleton|test|transition|widget)/SKILL\.md)'
S=$E/$FT/skills; R=$E/$FT/references
RUN=$S/flutter-run/SKILL.md; BLD=$S/flutter-build/SKILL.md; PRF=$S/flutter-preflight/SKILL.md; L10N=$S/flutter-l10n/SKILL.md
PD=$R/project-detection.md; WI=$E/$FT/agents/widget-inspector.md; WG=$S/flutter-widget/SKILL.md; SCR=$S/flutter-screen/SKILL.md
TST=$S/flutter-test/SKILL.md; TRN=$S/flutter-transition/SKILL.md; VEP=$R/visual-evidence-protocol.md; AIR=$R/flutter-ai-rules.md
EV=$E/$FT/evals/evals.json
# sect <파일> <제목 앞부분> — 그 제목부터 같은 깊이 이하의 다음 제목 전까지. 코드 펜스 안의 `#` 줄은 제목으로 보지 않는다
sect() { awk -v h="$2" '
  /^[[:space:]]*(```|~~~)/ { fence = !fence }
  !f && !fence && index($0, h) == 1 { f = 1; lvl = match($0, /[^#]/) - 1; print; next }
  f && !fence && /^#+ / { l = match($0, /[^#]/) - 1; if (l <= lvl) exit }
  f' "$1"; }
toks()  { local s="$1"; shift; for t in "$@"; do printf '%s ' "$(printf '%s\n' "$s" | grep -cF -- "$t")"; done; echo; }
url()   { grep -oE 'https?://[^ )>"`]+' | sed -E 's/[.,;:]+$//' | sort -u; }
added() { for f in "${FILES[@]}"; do git diff --no-index -U0 "$T/B/$f" "$E/$f"; done | grep '^+' | grep -v '^+++'; }
# 시작 커밋 판 스물세 파일 어디에도 없던 URL — 고친 줄에 원래 있던 URL 은 빼고 센다
newurls() { comm -23 <(added | url) <(for f in "${FILES[@]}"; do cat "$T/B/$f"; done | url); }
# blk <SKILL.md> — 전후 삭제 수 블록(`deleted() {` 가 든 첫 bash 블록)의 본문
blk()   { awk '/^```bash$/{b=1; buf=""; next} b&&/^```$/{if (buf ~ /deleted\(\) \{/) {printf "%s", buf; exit} b=0; next} b{buf=buf $0 "\n"}' "$1"; }
mine() { git log --format= --name-only "${1}..${2}" --grep="^${3}\$" | grep . | LC_ALL=C sort -u; }
unsigned_on() { _b=${1}; _u=${2}; _s=${3}; shift 3
  git log --format=%H "${_b}..${_u}" -- "$@" | while read -r _c; do git log -1 --format=%B "$_c" | grep -qxF "$_s" || echo "$_c"; done; }
my() { mine "$B" "$END" "$SIG"; }
fm_get() { awk -v k="^$2:[[:space:]]*" 'NR==1 && /^---[[:space:]]*$/ { fm=1; next } fm && /^---[[:space:]]*$/ { exit } fm && $0 ~ k { sub(k, "", $0); print; exit }' "$1" | sed -e "s/[[:space:]]*$//" -e "s/^['\"]//" -e "s/['\"]\$//"; }
sha256_16() { if command -v sha256sum >/dev/null 2>&1; then sha256sum; elif command -v shasum >/dev/null 2>&1; then shasum -a 256; else python3 -c 'import hashlib,sys; print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())'; fi | cut -c1-16; }
contract_digest() { grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$1" | sed -E 's/^- \[[ x]\]/- [ ]/' | sha256_16; }
verify_seal() { rec=$(fm_get "$1" conditions_digest); rec=${rec#sha256:}; if [ -z "$rec" ]; then echo "SEAL_ABSENT $1"; return 0; fi
  act=$(contract_digest "$1"); if [ "$rec" = "$act" ]; then echo "SEAL_OK $1"; else echo "SEAL_BROKEN $1 recorded=$rec actual=$act"; fi; }
FOUR='`[미검증]` 에 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령'
NOF='feature 인자가 와도 `--build-filter` 를 붙이지 않는다 — 인자는 보고에 적기만 하고 범위를 좁히지 않는다'
KEEP='맞는 삭제일 수 있으니 되돌리지 말고 목록을 보인다'
FRZ='지금 stable 은 4.0.2 · 2026-09-24 조회 — 4.0 의 breaking 은 `references/flutter-ai-rules.md` 의 Freezed 절'
REL='https://storage.googleapis.com/flutter_infra_release/releases/releases_macos.json'
```

SK-02 (b) 알려진 답 — 세 스킬의 전후 삭제 수 블록을 떼어 답을 아는 네 저장소에서 돌린다:

```bash
#!/usr/bin/env bash
# delgate.sh <SKILL.md> — codegen 절의 전후 삭제 수 블록을 떼어 답을 아는 다섯 저장소에서 돌린다.
# codegen 줄(`$DART run build_runner build --delete-conflicting-outputs`)은 가짜 생성기로 바꾼다. 답은 손으로 센 삭제 수다:
#   K1 아무것도 안 지움                         → before=0 after=0 new_first=0 new=0 codegen_exit=0 · 목록 0 · 종료 0
#   K2 부를 때마다 생성물 셋을 지움              → before=0 after=3 new_first=3 new=3 codegen_exit=0 · 목록 3 · 종료 1
#   K3 첫 번째만 셋을 지우고 두 번째에 되돌림    → before=0 after=0 new_first=3 new=0 codegen_exit=0 · 목록 0 · 종료 0
#   K4 미리 셋이 지워져 있고(목록 1 · 작업 폴더 2) 생성기가 둘을 더 지움 → before=3 after=5 new_first=2 new=2 codegen_exit=0 · 목록 2 · 종료 1
#   K5 생성기가 아무것도 안 지우고 종료 코드 3 으로 실패 → before=0 after=0 new_first=0 new=0 codegen_exit=3 · 목록 0 · 종료 1
# RUNNER 로 해석기를 바꾼다(기본 bash). `bash -e` 로 돌려도 다섯 줄이 다 나와야 한다 — 0 건에 멈추는 세기는 여기서 떨어진다.
skill=${1:?}
runner=${RUNNER:-bash}
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@e GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@e
w=$(mktemp -d); trap 'rm -rf "$w"' EXIT
blk=$(awk '/^```bash$/{b=1; buf=""; next} b&&/^```$/{if (buf ~ /deleted\(\) \{/) {printf "%s", buf; exit} b=0; next} b{buf=buf $0 "\n"}' "$skill")
[ -n "$blk" ] || { echo "NO_BLOCK"; exit 2; }
n=$(printf '%s\n' "$blk" | grep -cF '$DART run build_runner build --delete-conflicting-outputs')
[ "$n" = 2 ] || { echo "CODEGEN_LINES=$n (2 가 아니다)"; exit 2; }
blk=${blk//\$DART run build_runner build --delete-conflicting-outputs/\"\$FAKEGEN\"}
printf '%s\n' "$blk" > "$w/gate.sh"

cat > "$w/fakegen" <<'EOF'
#!/usr/bin/env bash
# FAKE=none|persist|transient|two|fail — 부른 횟수를 .calls 에 센다
c=$(( $(cat .calls 2>/dev/null || echo 0) + 1 )); echo "$c" > .calls
case "$FAKE" in
  persist)   rm -f lib/a.g.dart lib/b.g.dart lib/c.g.dart ;;
  transient) if [ "$c" = 1 ]; then rm -f lib/a.g.dart lib/b.g.dart lib/c.g.dart; else git checkout -q -- lib; fi ;;
  two)       rm -f lib/a.g.dart lib/b.g.dart ;;
  fail)      exit 3 ;;
esac
EOF
chmod +x "$w/fakegen"

mkrepo() {  # mkrepo <이름>
  local r=$w/$1
  { git init -q "$r"; mkdir -p "$r/lib"
    for f in a b c; do echo "$f" > "$r/lib/$f.g.dart"; done
    for f in x y z; do echo "$f" > "$r/lib/$f.dart"; done
    echo .calls > "$r/.gitignore"
    git -C "$r" add -A; git -C "$r" commit -qm init; } >/dev/null 2>&1
  echo "$r"
}
run_case() {  # run_case <이름> <FAKE> [미리 지우기]
  local r; r=$(mkrepo "$1")
  if [ "${3:-}" = pre ]; then (cd "$r" && git rm -q lib/x.dart && rm -f lib/y.dart lib/z.dart); fi
  out=$(cd "$r" && FAKE=$2 FAKEGEN="$w/fakegen" $runner "$w/gate.sh" 2>&1); st=$?
  line=$(printf '%s\n' "$out" | grep '^삭제 ' || echo '줄 없음')
  listed=$(printf '%s\n' "$out" | awk '/^늘어난 삭제:/{f=1; next} f&&NF{n++} END{print n+0}')
  echo "$1 $line 목록=$listed 종료=$st"
}
run_case K1 none
run_case K2 persist
run_case K3 transient
run_case K4 two pre
run_case K5 fail
```

DG-02 — 더한 줄에 걸린 경고만 센다:

```bash
#!/usr/bin/env bash
# new-warnings.sh <옛 파일> <새 파일> — 새 파일에서 더한 줄에 걸린 경고만 센다. 줄이 밀리므로 전체 수 차이로 세지 않는다
# 줄 번호는 경로 뒤 첫 번째 숫자다. 탐욕 매치(^[^ ]*:)로 뽑으면 열 번호가 줄 번호로 둔갑한다 (실측 2026-09-24)
# 린터가 안 돌면 경고 0 이 조용히 나온다 — 돌았다는 줄(Linting: 1 file)이 없으면 멈춘다 (실측 2026-09-25: 옆에 node_modules 가 없어 0)
set -u
DIR=$(cd "$(dirname "$0")" && pwd)
ADDED=$(git diff --no-index -U0 -- "$1" "$2" | awk '/^@@/{split($3,a,","); s=substr(a[1],2)+0; n=(a[2]==""?1:a[2]+0); for(i=0;i<n;i++) print s+i}' | sort -u)
OUT=$("$DIR/node_modules/.bin/markdownlint-cli2" --config "$DIR/cfg.markdownlint-cli2.jsonc" "$2" 2>&1)
printf '%s\n' "$OUT" | grep -q '^Linting: 1 file' || { echo "LINT_NOT_RUN $2"; exit 2; }
LINES=$(printf '%s\n' "$OUT" | grep -E ':[0-9]+(:[0-9]+)? (error|warning) ' | sed -E 's#^([^:]*):([0-9]+).*#\2#' | sort -u)
NEWW=$(comm -12 <(printf '%s\n' "$ADDED" | grep . | sort) <(printf '%s\n' "$LINES" | grep . | sort) | wc -l | tr -d ' ')
echo "total_warning_lines=$(printf '%s\n' "$LINES" | grep -c .) added_lines=$(printf '%s\n' "$ADDED" | grep -c .) new_warnings=$NEWW"
```

AR-01 — `evals.json` 을 파싱해 여덟 값을 낸다:

```bash
#!/usr/bin/env bash
# ar01.sh <evals.json> — 사례 수 · 사례 1 기대 출력 · 사례 1 단언 셋 · 사례 5 · 사례 16 두 값을 한 줄로 낸다 (파싱 실패는 JSON_ERROR)
python3 - "${1:?}" <<'PY'
import json, sys
try:
    d = json.load(open(sys.argv[1], encoding='utf-8'))
except Exception as e:
    print('JSON_ERROR', e); sys.exit(0)
ev = {e['id']: e for e in d['evals']}
c1 = ev[1]; c5 = ev[5]; c16 = ev[16]
t1 = [a['text'] for a in c1['assertions']]
print(len(d['evals']),
      int('--build-filter=' not in c1['expected_output'] and '전후 삭제 수' in c1['expected_output']),
      int('--build-filter 를 붙이지 않고 전체 codegen 을 돌린다 — auth 인자는 보고에 적기만 한다' in t1),
      int(any(t.startswith('codegen 전후 삭제 수 줄(before · after · new_first · new)을 보고하고') for t in t1)),
      int(not any('--build-filter에 auth' in t or '플래그가 포함된다' in t for t in t1)),
      int(any('[미검증] 에 네 칸' in a['text'] for a in c5['assertions'])),
      int(any('[미검증] 관례 표 없음' in a['text'] for a in c16['assertions'])), len(c16['assertions']))
PY
```

**봉인 전 실측 (2026-09-25).** 모의본 = 시작 커밋 판에 `mock.py` 62 치환을 적용한 트리(스크래치 `p5draft/M` — 검토 반영 뒤 다시 만들었다. 반영 전 판은 `p5draft/M-v1`).
공통 정의의 `END` 줄 대신 그 트리를 `$T/E` 로 복사해 같은 측정을 돌렸다(예행 전용 `common.sh` 의 `PRE_E`). 커밋을 재는 측정(AR-03 · ER-01 · SC-00 · DG-01 · DG-03 · DG-04 · DG-06 · RE-01)은 아래 `예행` 줄이다.
검토 반영(C1~C4 · O1)으로 바뀐 값은 SK-01 (a)(b) · SK-02 (c) · ER-01 과 문장 삭제 대조 수다. 나머지 값은 새 모의본에서 다시 재어 반영 전과 같았다.
2 회차 검토 D2 · D3 은 BUILD 가 봉인 전에 SK-01 에 넣고 다시 쟀다(스크래치 `p5build/d23.sh` — 시작 커밋 판을 새로 풀고 `mock.py` 를 다시 적용한 트리가 `p5draft/M` 과 `diff -rq` 차이 0):
(a) 넓힌 정규식 시작 커밋 판 `6` · 모의본 `0` · 모의본에 따옴표 없는 필터 한 줄 더한 사본 `1` · 따옴표 든 필터 한 줄 더한 사본 `1` / (b) l10n 세 값 시작 커밋 판 `0 0 0` · 모의본 `1 1 1`.

| 측정 | 시작 커밋 판 | 모의본 |
| --- | --- | --- |
| SK-01 (a) 킷 전체 `--build-filter=` · 띄어 쓴 필터 줄 · 감지 절차 `app-codegen-filter FILTER=` | `6` · `1` | `0` · `0` |
| SK-01 (b) 열한 문장 · transition 옛 codegen 줄 | 전부 0 · `1` | 전부 1 · `0` |
| SK-02 (a) 세 블록 해시 | `EMPTY` (블록 없음) | 1 종 (`15839f98ccc530a0`) |
| SK-02 (b) `delgate.sh` 세 스킬 · `bash -e` · `zsh` | `NO_BLOCK` 종료 코드 2 | 다섯 번 모두 다섯 줄이 알려진 답과 같다 |
| SK-02 (c) 열세 자리 | 전부 0 | 전부 1 |
| SK-03 옛 둘 · 새 넷 | `1 1` · `0 0 0 0` | `0 0` · `1 1 1 1` |
| SK-04 열 문장 | 전부 0 | 전부 1 |
| SK-05 (a)(b) · (c) | `0 0` · 같음 | `1 1` · 같음 |
| SK-06 네 문장 · URL 다섯 | 전부 0 | 전부 1 |
| SK-07 네 문장 · URL 셋 | 전부 0 | 전부 1 |
| SK-08 (a) · (b) · (c) | `9` · `4` · `0` | `0` · `0` · `1` |
| SK-09 (a) · (b) 새 일곱 · 옛 하나 · (c) 여덟 · (d) 다섯 | `9` · `0…` · `1` · `0…` · `1 1 1 1 1` | `0` · `1…` · `0` · `1…` · `1 1 1 1 1` |
| SK-10 (a) · (b) 여덟 · (c) 여섯 · (d) | `9` · `0…` · `0…` · `1` | `0` · `1…` · `1…` · `1` |
| AR-01 파이썬 여덟 값 · `run-evals.py flutter-toolkit` | `22 0 0 0 0 0 0 6` · 22 통과 | `22 1 1 1 1 1 1 7` · 22 통과 |
| AR-02 근거 밖 URL · 새 URL · 로그 머리 | `0` · `0` · `0` | `0` · `14` · `1` |
| AP-01 · AP-03 · AP-04 | — | `0` · V6 `0 bare` · 더한 줄 펜스 `0` · `0` |
| DG-02 스물두 마크다운 | — | 전부 `new_warnings=0`, `LINT_NOT_RUN` 0 |
| DG-05 (a)~(d) | V1~V10 `OK` | V1~V10 `OK` · 표·펜스 `FAIL` 0 · 세 검사 0 · 문서 계약 0(git 초기화한 사본) · 옛 값 0 · 훅 시험 `불일치 0` |

- **문장 삭제 대조** (`p5draft/deletion.py`): SK-01 · SK-02 (c) · SK-03 · SK-04 · SK-05 · SK-06 · SK-07 · SK-08 (c) · SK-09 (b)(c) · SK-10 (b) 의 62 문장을 하나씩 지운 사본에서 1 → 0. 62/62
  (반영 전 56 에 transition 한 문장 · 생성물 미추적 세 문장을 더했고, 2 회차 검토 D2 로 l10n 두 문장을 더했다 — BUILD 재실측 `p5build/deletion.py` `cases=62 bad=0`)
- **bash 가드** (검토 C1): 공통 정의 블록을 파일로 저장해 Claude Code 의 zsh 에서 `. 파일` → `NOT_BASH …` 한 줄 · 종료 코드 2. 같은 파일을 `bash -c` 에서 `. 파일` → 통과.
  가드 없는 반영 전 블록으로 SK-08 (b) 를 재면 시작 커밋 판이 zsh `0` · bash `4` 다(초안 재실측 — 검토 실측과 같다)
- **SK-02 음성 대조** (변이): N1 다시 돌리기 앞에서 `BEFORE` 를 다시 재면 K2 가 `new=0` (답 3) · N2 목록 쪽 `D` 를 안 세면 K4 가 `before=2` (답 3) · N3 세기를 `grep -c .` 로 바꾸면
  `bash -e` 에서 K1 이 `줄 없음` · N4 첫 codegen 줄의 `|| RC=$?` 를 빼면 K5 가 `codegen_exit=0 … 종료=0` (답 3 · 1) · N5 마지막 종료 코드 줄을 빼면 K2 가 `종료=0` (답 1).
  다섯 변이 모두 알려진 답에서 떨어진다. 첫 초안 블록은 끝 명령이 `printf` 라 codegen 이 실패해도 종료 코드 0 이었다 — 예행 중에 찾아 N4 · N5 · K5 를 더했다
- **양성 대조**: AR-02 — 모의본에 근거 파일 밖 URL 한 줄을 더하면 `1`. AP-01 — `0.8.0` 이 든 줄을 더하면 `1`. AP-03 — 맨 펜스를 더하면 V6 `1 bare`. AP-04 — `name:` 을 `nam:` 으로
  바꾸면 그 파일이 나오고 V1 `1 FAIL`. DG-02 — 첫 모의본은 `research-log.md` `new_warnings=1`(MD060) · `widget-inspector.md` `2`(MD032) 였다 — 고친 뒤 0.
  SK-01 (a) · SK-01 (b) 옛 줄 · SK-08 · SK-09 (a) · SK-10 (a) — 시작 커밋 판이 각각 1 이상(위 표). SK-01 (a) — 모의본 `flutter-widget/SKILL.md` 끝에
  `--build-filter "lib/**"` 한 줄을 더하면 첫 값 `1`(`p5draft/o1.sh`)
- **준비 단계**: `delgate.sh` 는 `git` · `comm` · `awk` 만 쓴다. 가짜 생성기는 `git checkout -q -- lib` 로 되돌린다. `validate-doc-contracts.py` 는 git 저장소가 아니면
  `NOT RUN` 으로 종료 코드 2 다 — 예행은 사본에 `git init` 뒤 돌렸고, 실제 측정은 작업 폴더에서 돈다
- **예행** (`p5draft/rehearse.sh` · `rh-measure.sh` · `rh-neg.sh`): 시작 커밋에서 뗀 복제본에 BUILD 순서(봉인 커밋 → 구현 커밋 → `end_sha` → notes → `end_sha`)대로
  서명 줄 커밋 다섯을 쌓고, **이 계약 원문의 공통 정의 블록과 도우미 블록 둘을 그대로 떼어**(`cd` 줄만 복제본으로 바꿔) 모든 측정을 돌렸다. 텍스트 조건 값은 위 표의 모의본 열과 같고,
  SK-02 (b) 스물다섯 줄 전부 답과 같다. 커밋을 재는 값: AR-03 ① 0 · ② 0 · 23 · ③ 0 · `SEAL_OK` / ER-01 22 값 전부 1 이상(일곱 값 `1 1 2 1 1 1 1` · 열둘 전부 1 · 같은 줄 `1 1 1`) · 셋째 0 · 넷째 0 / SC-00 0 · DG-01 0 · DG-04 0 · RE-01 0 ·
  RE-02 `1 0` / DG-06 `scope-isolation` PASS(5 커밋) · `doc-contracts` PASS · `docs-site-regen` SKIP. 음성 대조: 서명 없는 `flutter-toolkit/README.md` 커밋 → AR-03 ① 1 ·
  서명 없는 루트 `README.md` 커밋 → ER-01 넷째 1 · 같은 커밋에 `Kaizen-Phase: kaizen-0924-p06-design-kit` → 넷째 0. 셋째 · SC-00 · DG-01 · DG-04 · RE-01 의 경로 거르개에
  가짜 목록을 넣은 양성 대조는 각 조건 절에 적은 값과 같다

## Skill

- [ ] SK-01: codegen 스킬 셋과 l10n · 감지 절차가 `--build-filter` 를 스스로 붙이지 않고, 프로젝트 전용 필터 명령은 사용자가 이름으로 부를 때만 쓴다고 적으며, l10n Slang 줄과, 킷이 codegen 을 직접 돌리는 다섯째 자리인 transition §5 도 전후 삭제 수 블록으로 돌린다 (F06 · flutter:P-F06-codegen-delete-count · user-setup:P1) — (a) `$END` 판 `flutter-toolkit/` 전체(`flutter-run/SKILL.md` · `flutter-build/SKILL.md` · `flutter-preflight/SKILL.md` · `flutter-l10n/SKILL.md` · `evals.json` 포함)에서 `--build-filter=` 모양이나 `--build-filter` 뒤에 띄어 쓴 값(따옴표 · 영문 · 숫자 · 경로 문자로 시작)이 든 줄 수와 `project-detection.md` 의 `app-codegen-filter FILTER=` 줄 수가 둘 다 0 (b) 열한 문장이 정해진 절에 각각 1 건이고, `flutter-transition` 의 `### 5. Codegen` 절에 `build_runner build` 가 든 줄이 0 [exact, enumerated]
      (측정: (a) ``grep -rnE -- '--build-filter(=|[[:space:]]+["'"'"'A-Za-z0-9_$/.*{])' "$E/$FT" | grep -c .`` 0 · ``grep -c 'app-codegen-filter FILTER=' "$PD"`` 0
       (b) ``toks "$(sect "$RUN" '### codegen [feature]')" "$NOF" '`app-codegen-filter` 같은 프로젝트 전용 필터 명령은 사용자가 그 이름을 직접 부를 때만 쓴다'`` ·
       ``toks "$(sect "$RUN" '## Gotchas')" '**codegen 에 `--build-filter` 를 스스로 붙이지 마라**'`` · ``toks "$(sect "$BLD" '### 1. codegen [feature]')" "$NOF"`` ·
       ``toks "$(sect "$PRF" '### 2. codegen [feature]')" "$NOF"`` · ``toks "$(sect "$L10N" '### 6. Codegen 실행')" 'Slang 도 `--build-filter` 로 i18n 폴더만 돌리지 않는다' '`flutter-run` codegen 절의 블록으로 돌린다' '전체를 돌리고 전후 삭제 수를 센다'`` ·
       ``toks "$(sect "$PD" '### Step 2b.')" '`app-codegen-filter` 는 사용자가 그 이름을 직접 부를 때만 쓴다' '그 타겟을 flutter-run codegen 절 블록의 codegen 줄 자리에 넣어 전후 삭제 수를 센다'`` ·
       ``toks "$(sect "$TRN" '### 5. Codegen')" '`flutter-run` codegen 절의 블록으로 돌린다'`` 열한 값 전부 1 · ``sect "$TRN" '### 5. Codegen' | grep -c 'build_runner build'`` 0.
       봉인 전 실측: 시작 커밋 판 (a) `6` · `1` (b) 열한 값 0 · 옛 줄 `1` · 모의본 (a) `0` · `0` (b) 열한 값 1 · 옛 줄 `0`. 문장 삭제 대조 열한 경우 1 → 0.
       (a) 의 킷 전체 세기가 잡는 시작 커밋 판 여섯 줄은 옛 다섯 파일 세기(`2 1 1 1 1`)와 같은 줄이다. 양성 대조: 모의본 `flutter-widget/SKILL.md` 끝에 `--build-filter "lib/**"` 한 줄을 더하면 (a) 첫 값 1 — `=` 없이 띄어 쓴 필터와 다섯 파일 밖에 새로 생긴 필터도 잡는다(검토 O1).
       같은 자리에 따옴표 없는 `--build-filter lib/features/**` 한 줄을 더해도 1 이다(2 회차 검토 D3). 값의 첫 글자를 영문 목록으로 적는 까닭: `[:alnum:]` 로 쓰면 `C.UTF-8` 에서 한글이 들어가
       evals 사례 1 단언의 「--build-filter 를」 이 걸려 모의본이 1 이 된다(BUILD 재실측 2026-09-25 — `[:alnum:]` 판 모의본 `1`, 영문 판 `0`).
       l10n 두 문장(표 칸 · 끝 문장)은 2 회차 검토 D2 로 더했다 — 그 둘을 뺀 사본에서도 옛 l10n 한 값은 1 이라 따로 잰다)
- [ ] SK-02: 세 codegen 스킬이 같은 전후 삭제 수 블록을 갖고, 그 블록이 늘어난 삭제를 경로로 세고 한 번 더 돌린 뒤에도 첫 기준과 비교하며, codegen 실패와 남은 삭제를 종료 코드로 드러내고, 남으면 멈추되 되돌리지 말라고 적는다 (F06 · flutter:P-F06-codegen-delete-count) — (a) `flutter-run` · `flutter-build` · `flutter-preflight` 의 `deleted() {` 블록이 셋 다 있고 해시가 1 종 (b) `delgate.sh` 를 세 스킬에 bash 로, `flutter-run` 에 `bash -e` · `zsh` 로 돌린 다섯 번 모두 다섯 줄이 `K1 삭제 before=0 after=0 new_first=0 new=0 codegen_exit=0 목록=0 종료=0` · `K2 삭제 before=0 after=3 new_first=3 new=3 codegen_exit=0 목록=3 종료=1` · `K3 삭제 before=0 after=0 new_first=3 new=0 codegen_exit=0 목록=0 종료=0` · `K4 삭제 before=3 after=5 new_first=2 new=2 codegen_exit=0 목록=2 종료=1` · `K5 삭제 before=0 after=0 new_first=0 new=0 codegen_exit=3 목록=0 종료=1` (c) 정해진 절 열세 자리에 정해진 문장이 각각 1 건 — 마지막 세 자리는 생성물을 git 에 올리지 않는 프로젝트에서 이 세기가 늘 0 이라 `new=0` 을 통과로 쓰지 말라는 문장이다 [exact, enumerated]
      (측정: (a) ``for f in "$RUN" "$BLD" "$PRF"; do b=$(blk "$f"); [ -n "$b" ] && printf '%s\n' "$b" | sha256_16 || echo EMPTY; done | sort -u`` 이 한 줄이고 `EMPTY` 가 아니다
       (b) ``for f in "$RUN" "$BLD" "$PRF"; do bash "$K/delgate.sh" "$f"; done; RUNNER='bash -e' bash "$K/delgate.sh" "$RUN"; RUNNER=zsh bash "$K/delgate.sh" "$RUN"`` 스물다섯 줄이 위 다섯 줄의 다섯 번 되풀이
       (c) ``toks "$(sect "$RUN" '### codegen [feature]')" '`codegen_exit` 가 0 이 아니면 codegen 실패다 — 다시 돌리지 않고 멈춘다' '`new` 가 0 이면 통과다' '두 번째 실행으로 돌아온 것이라 복구로 보고한다' "$KEEP"`` ·
       ``toks "$(sect "$BLD" '### 1. codegen [feature]')" '`new` 가 0 이 아니면 analyze 로 가지 않고 멈춰서 `늘어난 삭제` 목록을 보고한다' "$KEEP"`` ·
       ``toks "$(sect "$BLD" '### 3. Report')" '1. codegen : success · 삭제 before=N after=N new_first=N new=0 codegen_exit=0'`` ·
       ``toks "$(sect "$PRF" '### 2. codegen [feature]')" '`new` 가 0 이 아니면 그것도 실패다' "$KEEP"`` · ``toks "$(sect "$PRF" '### 5. Report')" '2. codegen : success · 삭제 before=N after=N new_first=N new=0 codegen_exit=0'`` ·
       ``toks "$(sect "$RUN" '### codegen [feature]')" '이 세기가 생성물 삭제를 보지 못해 늘 0 이다'`` · ``toks "$(sect "$BLD" '### 1. codegen [feature]')" '이 세기가 생성물 삭제를 보지 못해 늘 0 이다'`` ·
       ``toks "$(sect "$PRF" '### 2. codegen [feature]')" '이 세기가 생성물 삭제를 보지 못해 늘 0 이다'`` 열세 값 전부 1.
       봉인 전 실측: 시작 커밋 판 (a) `EMPTY` (b) `NO_BLOCK` 종료 코드 2 (c) 전부 0 · 모의본 (a) 1 종 (b) 스물다섯 줄 전부 답과 같다 (c) 전부 1.
       마지막 세 문장의 이유: 블록은 git 이 추적하는 파일의 삭제만 센다. `*.g.dart` 를 무시하는 저장소에서 생성기가 생성물 셋을 지워도 블록이
       `삭제 before=0 after=0 new_first=0 new=0 codegen_exit=0` · 종료 0 을 낸다(검토 실측 2026-09-25 `p5review/k6`, 초안 재실측 `p5draft/k6` 같음) — 알려진 답 `K1`~`K5` 는 모두 생성물을 추적하는 저장소라 이 경우를 보지 못한다.
       음성 대조: 변이 다섯이 각각 답에서 떨어진다 — N1 다시 돌리기 앞에서 `BEFORE` 를 다시 잼 → K2 `new=0` · N2 목록 쪽 `D` 를 안 셈 → K4 `before=2` ·
       N3 세기를 `grep -c .` 로 → `bash -e` 에서 K1 · K5 `줄 없음` · N4 첫 codegen 줄의 `|| RC=$?` 를 뺌 → K5 `codegen_exit=0 … 종료=0` · N5 마지막 종료 코드 줄을 뺌 → K2 · K4 · K5 `종료=0`. 문장 삭제 대조 열세 경우 1 → 0. 반영 전 초안은 이 값 수를 「아홉」 으로 적었지만 실제 측정은 열 값이었다 — 이번에 바로잡았다)
- [ ] SK-03: codegen 규칙 두 줄이 `--delete-conflicting-outputs` 를 필수로 두지 않고 build_runner 2.16 사실과 전후 삭제 수로 바뀐다 (근거 §2 · §3 · §4 2 번) — `flutter-run` `## Rules` 에 옛 문장 ``codegen은 항상 `--delete-conflicting-outputs` 플래그 포함`` 0 · 새 문장 `**MUST** codegen 은 전후 삭제 수를 세어` 1, `flutter-build` `## Gotchas` 에 옛 문장 `플래그 필수 — 없으면` 0 · 새 문장 셋(``**`--delete-conflicting-outputs` 로 생성물이 안전하다고 믿지 마라**`` · `이 플래그는 제거된 호환 옵션 목록으로 옮겨졌다` · build_runner CHANGELOG URL) 각각 1 [exact, enumerated]
      (측정: ``toks "$(sect "$RUN" '## Rules')" 'codegen은 항상 `--delete-conflicting-outputs` 플래그 포함' '**MUST** codegen 은 전후 삭제 수를 세어'`` 이 `0 1` ·
       ``toks "$(sect "$BLD" '## Gotchas')" '플래그 필수 — 없으면' '**`--delete-conflicting-outputs` 로 생성물이 안전하다고 믿지 마라**' '이 플래그는 제거된 호환 옵션 목록으로 옮겨졌다' 'https://raw.githubusercontent.com/dart-lang/build/master/build_runner/CHANGELOG.md'`` 이 `0 1 1 1`.
       봉인 전 실측: 시작 커밋 판 `1 0` · `1 0 0 0` · 모의본 `0 1` · `0 1 1 1`. 문장 삭제 대조 세 경우 1 → 0. URL 이 근거 파일에 있는지는 AR-02)
- [ ] SK-04: widget-inspector 에 관례 대조 감지 기준 7 이 생기고, 호출 스킬이 넘긴 관례 표만 읽으며 화면 수를 정하지 않고, 결과를 칸마다 맞음 · 어긋남 · `[미검증]` 으로 적되 추출 후보 수에 더하지 않는다 (F02 · flutter:P-INSPECTOR-convention · F31 UI 부분) — `### 7. 관례 대조` 절에 여섯 문장, `### Step 2: 감지 실행` 에 둘, `### Step 3: 리포트 생성` 에 하나, `## Rules` 에 하나가 각각 1 건 [exact, enumerated]
      (측정: ``toks "$(sect "$WI" '### 7. 관례 대조')" '호출한 스킬이 넘긴 관례 표(`references/visual-evidence-protocol.md` Step 0 의 6 번)만 입력으로 쓴다.' '이 에이전트가 대조할 화면 수를 정하거나 표 밖의 화면으로 범위를 넓히지 않는다' 'deep 모드에서는 돌지 않는다' '줄 모양(카드인지 평평한 줄인지) · 칩·뱃지 모양 · 아이콘 뜻(닫기·끝내기·접기)' '`[미검증] 관례 표 없음`' '`어긋남` 은 추출 후보가 아니다 — Total 에 더하지 않고 따로 보고한다'`` ·
       ``toks "$(sect "$WI" '### Step 2: 감지 실행')" '감지 기준 7가지를 순서대로 적용한다' '7. 관례 대조 (quick 모드 · 호출 스킬이 넘긴 관례 표만)'`` · ``toks "$(sect "$WI" '### Step 3: 리포트 생성')" 'Convention Match (관례 대조 · quick)'`` ·
       ``toks "$(sect "$WI" '## Rules')" '**MUST** 관례 대조는 호출 스킬이 넘긴 관례 표의 경로만 읽는다'`` 열 값 전부 1.
       봉인 전 실측: 시작 커밋 판 전부 0 · 모의본 전부 1. 문장 삭제 대조 열 경우 1 → 0)
- [ ] SK-05: 관례 표를 만드는 두 스킬이 inspector 를 부를 때 그 표를 넘기고, 관례 표를 만들지 않는 flutter-feature 의 호출 절은 그대로다 (F02 Counterpart) — (a) `flutter-widget` (b) `flutter-screen` 의 `## Post-Creation: Widget Inspector` 절에 `편집 전에 만든 관례 표(규약 Step 0 의 6 번)를 함께 넘긴다` 가 각각 1 건 (c) `flutter-feature` 의 같은 절이 시작 커밋 판과 글자까지 같다 [exact, enumerated]
      (측정: ``for f in "$WG" "$SCR"; do toks "$(sect "$f" '## Post-Creation: Widget Inspector')" '편집 전에 만든 관례 표(규약 Step 0 의 6 번)를 함께 넘긴다'; done`` 두 값 1 ·
       ``[ "$(sect "$T/B/$FT/skills/flutter-feature/SKILL.md" '## Post-Creation: Widget Inspector')" = "$(sect "$S/flutter-feature/SKILL.md" '## Post-Creation: Widget Inspector')" ] && echo same`` 이 `same`.
       봉인 전 실측: 시작 커밋 판 `0 0` · 모의본 `1 1` · (c) 두 판 모두 `same`. 문장 삭제 대조 두 경우 1 → 0)
- [ ] SK-06: flutter-test Gotchas 가 위젯 시험의 로캘을 고정하게 하고, `initState` · `build` · `useEffect` 에서 provider 상태를 바꾸지 말라고 가르친다 (F24 · flutter:P-TEST-locale-buildmod) — `## Gotchas` 절에 네 문장과 근거 URL 다섯이 각각 1 건 [exact, enumerated]
      (측정: ``toks "$(sect "$TST" '## Gotchas')" '**위젯 시험의 로캘을 고정하지 않으면 결과가 실행 환경을 따라간다 (2026-09-25 추가)**' '한 언어의 문자열을 그대로 단언하지 말고, 생성된 번역 접근자로 기대값을 만들거나 시험 하네스에서 로캘을 명시한다' '**`initState` · `build` · `useEffect` 본문에서 provider 상태를 바꾸지 마라' '초기화는 provider 안으로 옮기고, 파생값은 `ref.watch` 나 `useMemoized` 로 계산한다' 'https://docs.flutter.dev/ui/accessibility-and-internationalization/internationalization' 'https://api.flutter.dev/flutter/widgets/WidgetsApp/locale.html' 'https://api.flutter.dev/flutter/flutter_test/TestPlatformDispatcher/locale.html' 'https://riverpod.dev/docs/root/do_dont' 'https://pub.dev/documentation/flutter_hooks/latest/flutter_hooks/useEffect.html'`` 아홉 값 전부 1.
       봉인 전 실측: 시작 커밋 판 전부 0 · 모의본 전부 1. 문장 삭제 대조 네 경우 1 → 0)
- [ ] SK-07: flutter-widget 카탈로그 등록 절이 타일 높이를 미리보기 내용보다 낮게 고정하지 말라고 가르치되, 적용 범위를 안쪽 스크롤을 의도하지 않은 타일로 좁히고 높이 숫자 대신 내용의 아래 끝을 재게 한다 (F22 · flutter:P-CATALOG-tile-height) — `### 7. Widgetbook/Storybook 등록` 절에 네 문장과 근거 URL 셋이 각각 1 건 [exact, enumerated]
      (측정: ``toks "$(sect "$WG" '### 7. Widgetbook/Storybook 등록')" '**카탈로그 타일 높이는 미리보기 내용보다 낮게 고정하지 않는다 (2026-09-25 추가).**' '안쪽이 따로 스크롤되길 의도하지 않은' '높이 숫자만 올려 맞추지 말고 미리보기 내용의 아래 끝이 타일 안에 드는지 시험으로 잰다.' '안쪽 스크롤이 필요한 타일이면 높이 규칙 대신' 'https://api.flutter.dev/flutter/widgets/ListView-class.html' 'https://api.flutter.dev/flutter/widgets/NestedScrollView-class.html' 'https://api.flutter.dev/flutter/widgets/ScrollView/shrinkWrap.html'`` 일곱 값 전부 1.
       봉인 전 실측: 시작 커밋 판 전부 0 · 모의본 전부 1. 문장 삭제 대조 네 경우 1 → 0)
- [ ] SK-08: 킷 파일에 특정 앱 · 프로젝트 · 화면 조종 도구 이름이 남지 않는다 (러닝북 Phase 5 과제) — `$END` 판 `flutter-toolkit/` 전체에서 (a) `fit-pal` · `fitpal` · `fit_pal` · `flutter-playwright` · `flutter_playwright` 가 든 줄 0 (b) 낱말 `apps` 가 든 줄 0 (c) `flutter-transition` `## Gotchas` 에 `커스텀 페이지 전환을 금지하는 프로젝트가 있다` 1 [exact]
      (측정: (a) ``grep -rniE 'fit-?pal|fit_pal|flutter[-_]playwright' "$E/$FT" | grep -c .`` 0 (b) ``grep -rnE '(^|[^[:alnum:]_])apps([^[:alnum:]_]|$)' "$E/$FT" | grep -c .`` 0
       (c) ``toks "$(sect "$TRN" '## Gotchas')" '커스텀 페이지 전환을 금지하는 프로젝트가 있다'`` 1.
       봉인 전 실측: 시작 커밋 판 (a) 9 (b) 4 (c) 0 — 양성 대조 · 모의본 (a) 0 (b) 0 (c) 1. 문장 삭제 대조 (c) 1 → 0)
- [ ] SK-09: 생성 측 `[미검증]` 이 사유 한 줄이 아니라 설계 가이드 §3.7 의 네 칸을 요구한다 (Phase 1 넘김 `visual-evidence-protocol.md:136`) — (a) `$END` 판 `flutter-toolkit/` 에서 「`[미검증]` 마커와 사유 · 마커 + 사유 · + 사유」 모양의 줄 0 (b) 규약 `## Step 4` 에 새 문장 여섯이 각각 1, `## Visual Evidence Block` 에 새 줄 1 · 옛 줄 `- 미검증: N 건 [항목 — 사유 — 시도한 fallback]` 0 (c) 스킬 일곱(`flutter-widget` · `flutter-screen` · `flutter-transition` · `flutter-skeleton` · `flutter-test` · `flutter-hooks` · `flutter-responsive`)의 정해진 절과 `evals.json` 에 네 칸 문구가 각각 1 (d) 규약이 가리키는 원문 — `$END` 판 `harness/docs/guides/skill-design-guide.md` `## 3.7.` 에 네 칸 이름과 `[미검증:INVALID]` 가 각각 1 이상 [exact, enumerated]
      (측정: (a) ``grep -rnE '\[미검증\]`? ?(마커)? ?(와|\+) ?사유' "$E/$FT" | grep -c .`` 0
       (b) ``toks "$(sect "$VEP" '## Step 4')" '해당 항목에 `[미검증]` 을 달고 네 칸을 채운다' '**막는 것**(실행한 명령과 그 실패 출력)' '**시도한 우회**' '**통제 불가 사유**' '**재검증 명령**' '평가 측이 `[미검증:INVALID]` 로 센다'`` 여섯 값 1 ·
       ``toks "$(sect "$VEP" '## Visual Evidence Block')" '- 미검증: N 건 [항목 — 막는 것 — 시도한 우회 — 통제 불가 사유 — 재검증 명령]' '- 미검증: N 건 [항목 — 사유 — 시도한 fallback]'`` 이 `1 0`
       (c) ``toks "$(sect "$WG" '## Post-Creation: Visual Evidence')" "$FOUR"`` · ``toks "$(sect "$SCR" '## Post-Creation: Visual Evidence')" "$FOUR"`` · ``toks "$(sect "$TRN" '## Rules')" "$FOUR"`` ·
       ``toks "$(sect "$S/flutter-skeleton/SKILL.md" '### 5. 체크리스트')" "$FOUR"`` · ``toks "$(sect "$TST" '### 5. 결과 제시')" "$FOUR"`` · ``toks "$(sect "$S/flutter-hooks/SKILL.md" '## Gotchas')" "$FOUR"`` ·
       ``toks "$(sect "$S/flutter-responsive/SKILL.md" '## Rules')" "$FOUR"`` · ``grep -cF '[미검증] 에 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)' "$EV"`` 여덟 값 1
       (d) ``toks "$(sect "$E/harness/docs/guides/skill-design-guide.md" '## 3.7.')" '**막는 것**' '**시도한 우회**' '**통제 불가 사유**' '**재검증 명령**' '`[미검증:INVALID]`'`` 다섯 값 1 이상.
       봉인 전 실측: 시작 커밋 판 (a) 9 — 양성 대조 (b) 새 0 · 옛 1 (c) 전부 0 (d) `1 1 1 1 1` · 모의본 (a) 0 (b) 새 1 · 옛 0 (c) 전부 1 (d) `1 1 1 1 1`. 문장 삭제 대조 (b)(c) 열한 경우 1 → 0)
- [ ] SK-10: 지금 틀린 버전 문장 아홉 줄이 근거 파일 조회값으로 바뀐다 (근거 §3) — (a) `$END` 판 `flutter-toolkit/` 에서 `최신 stable 3.2.5` · `최신 stable 은 3.2.5` · `현재 stable 은 3.47.0` · `현재 stable 은 Flutter 3.47.0` 모양의 줄 0 (b) `flutter-api` · `flutter-error` · `flutter-audit` · `flutter-hooks` · `flutter-provider` 에 Freezed 새 문구가 각각 1, `flutter-ai-rules.md` `### Freezed` 절에 새 문장 셋이 각각 1 (c) `flutter-ai-rules.md` · `flutter-transition` 에 `현재 stable 은 3.47.5`, `flutter-widget` 에 `현재 stable 은 Flutter 3.47.5` 가 각각 1이고 세 파일에 배포 메타데이터 URL 이 각각 1 (d) 스킬 다섯이 가리키는 `### Freezed` 제목이 `flutter-ai-rules.md` 에 1 [exact, enumerated]
      (측정: (a) ``grep -rnE '최신 stable (은 )?3\.2\.5|현재 stable 은 (Flutter )?3\.47\.0' "$E/$FT" | grep -c .`` 0
       (b) ``for s in api error audit hooks provider; do printf '%s ' "$(grep -cF "$FRZ" "$S/flutter-$s/SKILL.md")"; done`` 다섯 값 1 ·
       ``toks "$(sect "$AIR" '### Freezed')" '지금 stable 은 4.0.2 다(2026-09-24 조회)' '- **4.0 (2026-09-24 조회 stable 4.0.2)**' '생성자 파라미터에 `final` 을 붙이는 형태는 지원하지 않는다(breaking)'`` 세 값 1
       (c) ``grep -cF '현재 stable 은 3.47.5' "$AIR"; grep -cF '현재 stable 은 3.47.5' "$TRN"; grep -cF '현재 stable 은 Flutter 3.47.5' "$WG"; for f in "$AIR" "$TRN" "$WG"; do grep -cF "$REL" "$f"; done`` 여섯 값 1
       (d) ``grep -c '^### Freezed' "$AIR"`` 1.
       봉인 전 실측: 시작 커밋 판 (a) 9 — 양성 대조 (b)(c) 전부 0 (d) 1 · 모의본 (a) 0 (b)(c) 전부 1 (d) 1. 문장 삭제 대조 (b) 셋 1 → 0)

## Script

- [ ] SC-00: N/A (Script 카테고리는 `release.sh` 연동 · 버전 올림 · `marketplace.json` 갱신이다. 이 Phase 는 그 파일을 건드리지 않는다 — 버전은 Final 몫. 측정: `type my >/dev/null || exit 2;` 뒤 `my | grep -cE '^(scripts/release\.sh|\.claude-plugin/marketplace\.json|[^/]+/\.claude-plugin/plugin\.json)$'` 이 0. 양성 대조: 같은 `grep -cE` 에 `scripts/release.sh` · `.claude-plugin/marketplace.json` · `flutter-toolkit/.claude-plugin/plugin.json` · `flutter-toolkit/README.md` 네 줄을 넣으면 3)

## Error

- [ ] ER-01: 이 Phase 범위 밖과 미반영 키를 명시적 미완으로 넘기고, 공유 파일 · 다른 Phase 소관 파일을 건드리지 않는다 — `.harness/.meta/kaizen-0924/phase5-notes.md` 에 스물두 문자열(처리 배정표 키 `F02` · `F06` · `F22` · `F24` · `F25` · `flutter:P-F06-codegen-delete-count` · `flutter:P-INSPECTOR-convention` · `flutter:P-TEST-locale-buildmod` · `flutter:P-CATALOG-tile-height` · `user-setup:P1` 과 넘김 `visual-evidence-protocol.md:136` · `F31` · `flutter-preflight` · `ProviderScope` · `go_router` · `auto_route` · `--delete-conflicting-outputs` · `flutter-audit/SKILL.md:50` · `flutter-feature/SKILL.md:151` · `$DART test` · `docs/kaizen/flutter-changelog.md` · `Phase 6`)이 각각 1 회 이상 있고 — 그 가운데 `flutter-preflight` · `--delete-conflicting-outputs` · `Phase 6` 은 같은 줄에 `기준 커밋` · `경고인지 오류인지` · `2 개 이상` 이 함께 있어야 한다 —, 이 Phase 커밋이 공유 파일 · `harness/` 를 하나도 건드리지 않는다. 서명 줄 커밋 목록으로 재고, 서명을 빠뜨린 커밋도 보이게 공유 파일을 건드린 구간 안 커밋을 직접 센다 [exact, enumerated]
      (Given: BUILD 가 notes 를 쓰고 커밋한 뒤 · 측정: `git cat-file -e "$END:$NOTES"` exit 0 ·
       짧은 키 일곱은 낱말 경계로 센다 — `F06` 은 `flutter:P-F06-codegen-delete-count` 안에도 있어 글자 그대로 세면 `F06` 줄이 없어도 1 이 나온다(예행 실측 2) —
       ``for t in 'F02' 'F06' 'F22' 'F24' 'F25' 'F31' 'user-setup:P1'; do printf '%s ' "$(git show "$END:$NOTES" | grep -cE -- "(^|[^[:alnum:]-])$t([^[:alnum:]-]|$)")"; done`` 일곱 값 ·
       ``for t in 'flutter:P-F06-codegen-delete-count' 'flutter:P-INSPECTOR-convention' 'flutter:P-TEST-locale-buildmod' 'flutter:P-CATALOG-tile-height' 'visual-evidence-protocol.md:136' 'ProviderScope' 'go_router' 'auto_route' 'flutter-audit/SKILL.md:50' 'flutter-feature/SKILL.md:151' '$DART test' 'docs/kaizen/flutter-changelog.md'; do printf '%s ' "$(git show "$END:$NOTES" | grep -cF -- "$t")"; done`` 열둘 값 ·
       세 낱말은 사유와 한 줄로 센다 — 바꾼 파일 목록 · changelog · 다른 메모에도 나와 낱말만 세면 넘김 줄을 빠뜨려도 1 이다 —
       ``N=$(git show "$END:$NOTES"); printf '%s %s %s\n' "$(printf '%s\n' "$N" | grep -F 'flutter-preflight' | grep -cF '기준 커밋')" "$(printf '%s\n' "$N" | grep -F -- '--delete-conflicting-outputs' | grep -cF '경고인지 오류인지')" "$(printf '%s\n' "$N" | grep -F 'Phase 6' | grep -cF '2 개 이상')"`` 세 값 — 22 값 전부 1 이상 ·
       셋째 — `type my >/dev/null || exit 2;` 뒤 `my | grep -cE '^(\.claude-plugin/|[^/]+/\.claude-plugin/plugin\.json$|README\.md$|CLAUDE\.md$|\.github/|\.claude/|docs/kaizen/|docs/.+\.html$|harness/|\.harness/\.meta/(orchestrator-audit-log\.md|kaizen-failure-count\.yaml)$)'` 0 ·
       넷째(직접 세기) — `git log --format=%H "$B..$END" -- .claude-plugin flutter-toolkit/.claude-plugin README.md CLAUDE.md .github .claude docs/kaizen .harness/.meta/orchestrator-audit-log.md .harness/.meta/kaizen-failure-count.yaml | while read -r c; do git log -1 --format=%B "$c" | grep -qE '^Kaizen-Phase: kaizen-0924-p(0[1-46-9]|[1-9][0-9])-' || echo "$c"; done | grep -c .` 0.
       다른 Phase 서명 줄이 달린 커밋은 그 Phase 몫이라 뺀다. `harness/` 와 `docs/` HTML 은 다른 Phase 가 제 범위를 고치며 건드려 넷째에서 빼고 셋째로만 잰다.
       봉인 전 실측: notes 없음 — 구현이 만들 파일이라 면제. 바꾼 파일 목록 · 반영 · 미반영 · changelog · 다음 사이클 메모 다섯 부분을 갖춘 가짜 notes(`p5draft/er01/notes-full.md`)를
       예행 복제본에 커밋해 재면 일곱 값 `1 1 2 1 1 1 1` · 열둘 값 전부 1 · 같은 줄 세 값 `1 1 1`. 그 사본에서 한 곳씩 지우면 그 값만 0 이다 — 낱말 `F06` 만(긴 키는 남김) → 일곱 값 둘째 0 ·
       `user-setup:P1` → 일곱째 0 · `go_router` → 열둘 값 일곱째 0 · `flutter-feature/SKILL.md:151` 줄 → 열둘 값 열째 0 · 넘김 세 줄 → 같은 줄 세 값 `0 0 0`.
       넘김 세 줄을 지운 사본에서 낱말만 세는 옛 측정은 `1 1 1` 로 못 잡는다(검토 실측과 같다). 낱말 경계 전에는 `F06` 줄을 빼도 1 이었다. 셋째는 가짜 목록 한 줄씩 `harness/skills/sprint/SKILL.md` · `.claude-plugin/marketplace.json` · `flutter-toolkit/.claude-plugin/plugin.json` · `README.md` ·
       `docs/kaizen/flutter-changelog.md` · `docs/flutter/state.html` · `.github/workflows/ci.yml` 각각 1, 이 Phase 파일 스물셋 · 계약 · 개정 · notes · 검토 목록은 0.
       넷째는 예행 0 · 예행 사본에 서명 없이 루트 `README.md` 를 고친 커밋을 얹으면 1 · 같은 커밋에 다른 Phase 서명 줄을 달면 0)

## Architecture

- [ ] AR-01: `evals.json` 이 새 동작을 기대하고 평가 러너를 통과한다 (F06 · F02 Counterpart) — `$END` 판 `evals.json` 을 파싱한 여덟 값이 `22 1 1 1 1 1 1 7` 이다 — 사례 수 22 · 사례 1 기대 출력에 `--build-filter=` 가 없고 `전후 삭제 수` 가 있다 · 사례 1 단언에 필터를 안 붙인다는 문장 · 삭제 수 줄 문장이 있다 · 사례 1 단언에 `--build-filter에 auth` · `플래그가 포함된다` 가 없다 · 사례 5 단언에 `[미검증] 에 네 칸` · 사례 16 단언에 `[미검증] 관례 표 없음` · 사례 16 단언 수 7. 그리고 작업 폴더에서 `python3 scripts/run-evals.py flutter-toolkit` 이 종료 코드 0 에 `22 passed, 0 failed` [exact]
      (측정: `bash "$K/ar01.sh" "$EV"` 한 줄이 `22 1 1 1 1 1 1 7` · 작업 폴더에서 `python3 scripts/run-evals.py flutter-toolkit; echo $?` 의 끝 두 줄이 `Total: 22 passed, 0 failed` · `0`.
       봉인 전 실측: 시작 커밋 판 `22 0 0 0 0 0 0 6` · 모의본 `22 1 1 1 1 1 1 7`, 두 판 모두 `22 passed, 0 failed` — 러너는 구조만 보므로 단언 문장은 파이썬 값이 잰다)
- [ ] AR-02: 이 Phase 가 새로 들인 URL 이 전부 근거 파일에 있고, 킷 조사 기록 머리에 이번 항목이 있다 (러닝북 「근거 파일에 없는 URL 을 지어내지 마라」 · 오케스트레이터 per-kit research-log) — `newurls` 가운데 근거 파일 URL 밖이 0 개이고 새 URL 이 1 개 이상이며, `$END` 판 `docs/flutter/research-log.md` 의 첫 `## [` 제목이 `## [2026-09-25] — Phase 5 kaizen` [exact]
      (측정: ``newurls | comm -23 - <(url < "$EVID") | grep -c .`` 0 · ``newurls | grep -c .`` 1 이상 · ``grep -m1 '^## \[' "$E/docs/flutter/research-log.md" | grep -cF '## [2026-09-25] — Phase 5 kaizen'`` 1.
       봉인 전 실측: 시작 커밋 판 `0` · `0` · `0` · 모의본 `0` · `14` · `1`. 양성 대조: 모의본에 `<https://example.com/not-in-evidence>` 한 줄을 더하면 첫 값 1)
- [ ] AR-03: 이 Phase 의 변경이 허용 경로 안에 머물고 이 계약이 봉인돼 있다 [exact, enumerated]
      (Given: BUILD 가 개정 파일에 `end_sha:` 를 적은 뒤 · 이 Phase 커밋 메시지마다 서명 줄 `Kaizen-Phase: kaizen-0924-p05-flutter-toolkit` · 측정 셋 —
       ① `type unsigned_on >/dev/null || exit 2;` 뒤 `unsigned_on "$B" "$END" "$SIG" flutter-toolkit docs/flutter | grep -c .` 0 (`flutter-toolkit/` · `docs/flutter/` 를 건드린 구간 안 커밋이 전부 서명했다 — 이 구간에 두 폴더를 고칠 수 있는 Phase 는 5 하나다)
       ② `.harness/` 밖은 스물셋 파일뿐이다 — `type my >/dev/null || exit 2;` 뒤 `my | grep -vE "^(\.harness/|($FRE)$)" | grep -c .` 0 · `my | grep -cxE "$FRE"` 23
       ③ `harness/references/contract-schema.md` §`.harness/` 범위 조건 의 권장 형태 — `type verify_seal >/dev/null || exit 2;` 뒤 `find .harness -type f -name 'sprint-contract*.md' -print0 | while IFS= read -r -d '' f; do verify_seal "$f"; done | awk '$1=="SEAL_BROKEN"{print $2}' | sed 's#^\./##' | sort -u | comm -12 - <( { my; echo "$CF"; } | sort -u) | grep -c .` 0 이고
       이 계약 자신이 봉인돼 있다 — `verify_seal "$CF" | cut -d' ' -f1` 이 `SEAL_OK` (`SEAL_ABSENT` 는 봉인을 건너뛴 것이라 FAIL).
       봉인 전 실측(예행): ① 0 · ② 0 · 23 · ③ 0 · 이 계약 `SEAL_OK`. 음성 대조: 예행 사본에 서명 없이 `flutter-toolkit/README.md` 를 고친 커밋을 얹고 `end_sha` 를 옮기면 ① 1 —
       그 파일은 스물셋 밖이고 서명이 없어 ② 는 못 본다. 봉인 전인 지금 작업 폴더의 이 계약은 `SEAL_ABSENT` — 봉인을 빠뜨리면 ③ 이 떨어진다)

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다. 이번 변경에 적용: 스물세 파일에 더한 줄에 flutter-toolkit 플러그인 버전 문자열(`$END` 판 `flutter-toolkit/.claude-plugin/plugin.json` 의 `version` 값)이 0 건이다 — 외부 라이브러리 버전(Freezed · Flutter · build_runner)은 조회 날짜와 출처를 단 사실 문장이라 이 패턴의 대상이 아니다 [exact]
      (측정: `V=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["version"])' "$E/$FT/.claude-plugin/plugin.json"); added | grep -cF -- "$V"` 0.
       봉인 전 실측: `V=0.8.0` · 모의본 0. 양성 대조: 모의본에 `버전 0.8.0 을 적는다` 한 줄을 더하면 1)
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (\`\`\`text, \`\`\`bash, \`\`\`yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 이번 변경에 적용: `python3 scripts/validate-plugin.py flutter-toolkit --check=code-fence` 가 `0 bare` 이고, V6 가 읽지 않는 `docs/flutter/research-log.md` 에 더한 줄에는 펜스가 없다 [exact]
      (측정: 작업 폴더에서 `python3 scripts/validate-plugin.py flutter-toolkit --check=code-fence | grep -c '0 bare'` 1 · ``git diff --no-index -U0 "$T/B/docs/flutter/research-log.md" "$E/docs/flutter/research-log.md" | grep '^+' | grep -v '^+++' | grep -c '```'`` 0.
       봉인 전 실측: 모의본 `0 bare` · 0. 양성 대조: 모의본 `flutter-run/SKILL.md` 끝에 맨 펜스 한 쌍을 더하면 V6 `1 bare`)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL. 이번 변경에 적용: 고친 SKILL.md 열다섯과 `widget-inspector.md` 의 첫 frontmatter 블록 `name:` 값이 폴더 이름 · 파일 이름과 같다 [exact]
      (측정: ``for f in "${FILES[@]}"; do case $f in */SKILL.md) n=$(basename "$(dirname "$f")");; */agents/*.md) n=$(basename "$f" .md);; *) continue;; esac; [ "$(fm_get "$E/$f" name)" = "$n" ] || echo "$f"; done | grep -c .`` 0.
       봉인 전 실측: 모의본 0. 양성 대조: 모의본 `flutter-run/SKILL.md` 의 `name:` 을 `nam:` 으로 바꾸면 그 파일 한 줄이 나오고 V1 `1 FAIL`)

## Reusability

- [ ] RE-01: N/A (산출물에 재사용 단위 코드 파일이 없다 — 스킬 문서 · 에이전트 문서 · 참조 문서 · 평가 사례 · 조사 기록뿐이다. 측정: `type my >/dev/null || exit 2;` 뒤 `my | grep -cE '\.(dart|py|sh|js|ts|tsx|rs|go)$'` 이 0. 양성 대조: 같은 `grep -cE` 에 `scripts/x.py` · `a.sh` · `b.md` 세 줄을 넣으면 2)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다. 이번 변경에 적용: 세 스킬의 전후 삭제 수 블록은 새 변형 없이 한 블록의 글자 그대로 사본이고(SK-02 (a) 해시 1 종), 삭제 세기는 근거 파일 §2 의 `git status --porcelain=v1 --untracked-files=no` + `awk` 형태를 그대로 쓴다 — 주석 줄을 뺀 블록 본문에 `git status --porcelain=v1 --untracked-files=no` 1 · `grep -c` 0 [exact]
      (측정: ``blk "$RUN" | grep -vE '^[[:space:]]*#' | grep -cF 'git status --porcelain=v1 --untracked-files=no'`` 1 · ``blk "$RUN" | grep -vE '^[[:space:]]*#' | grep -c 'grep -c'`` 0.
       봉인 전 실측: 모의본 1 · 0. 음성 대조: 변이 N3(세기를 `grep -c .` 로)에서 둘째 값 1)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `type my >/dev/null || exit 2;` 뒤 `my | grep -c '^scripts/release.sh$'` 이 0. 양성 대조: 같은 `grep -c` 에 `scripts/release.sh` · `scripts/release.sh.bak` 두 줄을 넣으면 1. 실제 분석은 DG-02 · DG-05)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (`diagnostics.ide_exclude` 값 `[]`) — 이번 변경에 적용: 편집기 마크다운 확장과 같은 조건(markdownlint-cli2 0.23.2 · MD013 끔)으로 마크다운 스물두 파일의 **더한 줄**에 걸린 경고가 0 이고, 린터가 스물두 번 다 돌았다. `evals.json` 은 AR-01 이 파싱한다. 편집 전부터 있던 경고는 `범위 경계` 절에 적은 대로 범위 밖이다 [exact]
      (측정: ``for f in "${FILES[@]}"; do case $f in *.md) printf '%s ' "$f"; bash "$K/new-warnings.sh" "$T/B/$f" "$E/$f";; esac; done`` 스물두 줄 전부 `new_warnings=0` 이고 `LINT_NOT_RUN` 0.
       봉인 전 실측: 모의본 스물두 줄 전부 `new_warnings=0`. 양성 대조: 첫 모의본은 `docs/flutter/research-log.md` 1(MD060) · `widget-inspector.md` 2(MD032) — 고친 뒤 0)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: DG-01 과 같은 명령 `type my >/dev/null || exit 2;` 뒤 `my | grep -c '^scripts/release.sh$'` 이 0. 실제 시험은 SK-02 (b) · AR-01 · DG-05)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 바뀐 파일은 마크다운 스물둘과 JSON 하나다. codegen 블록은 SK-02 (b) 가 시험 저장소에서 실제로 돌린다. 측정: `type my >/dev/null || exit 2;` 뒤 `my | grep -cE '\.(dart|ts|tsx|js|rs|go)$'` 이 0. 양성 대조: 같은 `grep -cE` 에 `a/b.dart` · `c.ts` · `d.md` 세 줄을 넣으면 2)
- [ ] DG-05: 저장소 검사가 이 Phase 파일을 문제로 가리키지 않는다 (Given: 구현 커밋 뒤 작업 폴더에서) — (a) `python3 scripts/validate-plugin.py flutter-toolkit` 출력에 `V1` ~ `V10` 열 줄이 있고 하나도 `ERROR` · `FAIL` 이 아니다 (b) 전체 킷 `--check=table-integrity,code-fence` 의 `FAIL` 줄 가운데 이 Phase 파일을 가리키는 줄 0 (c) `sync-docs.py --check-only` · `sync-evals.py --check-only` · `validate-doc-contracts.py` 가 종료 코드 0 이고 `check-stale-values.py` 가 0 또는 1 이며 출력에 이 Phase 파일 0 건 (d) `bash flutter-toolkit/evals/hooks/format-edited-dart-test.sh` 가 종료 코드 0 에 끝 줄 `결과: 12 경우 중 불일치 0` [exact]
      (측정: (a) ``python3 scripts/validate-plugin.py flutter-toolkit | grep -E '^  V([1-9]|10) ' | grep -cvE 'FAIL|ERROR'`` 10
       (b) ``python3 scripts/validate-plugin.py --check=table-integrity,code-fence 2>&1 | grep 'FAIL' | grep -cE "$FRE"`` 0
       (c) 세 명령 각각 `; echo $?` 가 0 · ``python3 scripts/check-stale-values.py 2>&1 | grep -cE "$FRE"`` 0
       (d) `bash flutter-toolkit/evals/hooks/format-edited-dart-test.sh; echo $?` 의 끝 두 줄.
       봉인 전 실측: 모의본 (a) 10 (b) 0 (c) 셋 0(문서 계약은 git 초기화한 사본) · 옛 값 0 건 (d) `결과: 12 경우 중 불일치 0` · 0. 시작 커밋 판 작업 폴더도 같다)
- [ ] DG-06: `python3 scripts/validate-post-kaizen.py --since 79258900de00e621412e4c436b44028a77d7fb64` 출력의 `scope-isolation` · `doc-contracts` 줄이 `FAIL` · `ERROR` 가 아니다. `docs-site-regen` 은 이 Phase 가 `harness/` 원본을 건드리지 않아 `SKIP` 이지만 판정에서 뺀다(Final F2 몫). 다른 Phase 커밋 때문에 `scope-isolation` 이 FAIL 이면 `--verbose` 위반 커밋 목록에 서명 줄 커밋이 없을 때 이 조건은 PASS 다. `doc-contracts` 가 `FAIL` · `ERROR` 이면 `python3 scripts/validate-doc-contracts.py -v` 의 `검사:` 줄에 나온 경로를 `my` 와 대조해, 겹치는 경로가 0 개면 다른 Phase 몫으로 근거에 적고 이 조건은 PASS 다 [exact]
      (측정: 위 명령의 두 줄. 봉인 전 실측: 시작 커밋에서 `scope-isolation` PASS(0 커밋) · `doc-contracts` PASS(1 블록 · violation 0) · `docs-site-regen` SKIP)
