# 카이젠 2026-09-24 Phase 5 (flutter-toolkit) — notes

- 계약: `.harness/sprint-contract-kaizen-0924-p05-flutter-toolkit.md` (조건 26 · 기능 조건 16, 봉인 `sha256:66138070ffba6c9a` · `locked_at` 2026-09-25 06:16)
- 개정: `.harness/sprint-amendments-kaizen-0924-p05-flutter-toolkit.md` (조건 변경 0 건, `end_sha` 만)
- 검토: `.harness/.meta/kaizen-0924/phase5-review.md` (1 회차 CHANGES 고칠 것 넷 · 제안 셋은 초안이 반영, 2 회차 APPROVE 권장 넷은 BUILD 가 봉인 전에 반영)
- 시작 커밋 `79258900de00e621412e4c436b44028a77d7fb64`
- 계약 피드백: `~/.harness/feedback/contract/5a24cc99-2026-09-25T062025-de8c7935-49233.yaml` (`verify-feedback.sh` PASS)

## 커밋

| 커밋 | 내용 | 파일 |
| --- | --- | --- |
| `58e0943` | 봉인 커밋 | 계약 1 개 |
| `cb7d99d` | research-log 2026-09-25 Phase 5 항목 | `docs/flutter/research-log.md` |
| `ef351d2` | codegen 필터 제거 · 전후 삭제 수 · 관례 대조 · 시험 함정 · 타일 높이 · `[미검증]` 네 칸 · 이름 빼기 · 버전 정정 · 평가 사례 | `flutter-toolkit/` 스물둘 |
| `573fecc` | 개정 파일에 `end_sha` (`ef351d2`) | 개정 1 개 |
| 이 파일의 커밋 | notes · 검토 기록 | `.harness/` 두 개 |
| 그다음 커밋 | 개정 파일에 notes 커밋 sha 로 `end_sha` 한 줄 더 | 개정 1 개 |

모든 커밋 메시지 끝 문단에 `Kaizen-Phase: kaizen-0924-p05-flutter-toolkit` 줄이 있다. 구현 커밋은 `git add -- <파일…> && git commit -o -- <파일…>` 로 내 경로만 실었다.
**FIX 가 커밋을 더할 때도 서명 줄을 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다.**

봉인 전에 BUILD 가 계약에 넣은 것 — 2 회차 검토의 막지 않는 권장 넷. D1 「넘기는 것」 괄호(짧은 키 뒤 조사), D4 「측정이 기대는 제목」 목록(산문),
D2 · D3 SK-01 조건 줄과 측정(l10n 두 문장 · 따옴표 없는 필터). D2 · D3 은 시작 커밋 판 · 모의본 · 양성 대조 둘 · 문장 삭제 대조 62/62 를 다시 재고 봉인했다.

구현은 초안의 모의 편집(스크래치 `p5draft/mock.py`, 치환 62)을 작업 폴더에 그대로 돌렸다 — `edits=62 bad=0`. 스물세 파일이 새로 푼 모의본(`p5build/M`)과 글자까지 같다.
26 조건 측정은 봉인 판 계약에서 떼어 낸 묶음으로 돌렸다 — 스크래치 `p5build/`: `common.sh` · `K/`(`delgate.sh` · `new-warnings.sh` · `ar01.sh`, 네 블록 모두 봉인 판에서 글자 그대로) ·
`conds.sh` · `extra.sh` · `commit-measures.sh` · `dg05.sh`. 조건 줄의 측정 조각 66 개 가운데 네 개(SK-05 두 개 · SK-10 (c)(d))는 `extra.sh` 에 원문 그대로 따로 넣었다.
QA 는 `cd <작업 폴더> && bash -c "K=<p5build>/K; . <p5build>/common.sh; . <p5build>/conds.sh; . <p5build>/extra.sh; . <p5build>/commit-measures.sh"` 로 다시 돌릴 수 있다.

## 바꾼 파일

- `docs/flutter/research-log.md` — `## [2026-09-25] — Phase 5 kaizen` 항목(외부 조회 0 회, URL 여덟은 근거 파일에서)
- `flutter-toolkit/skills/flutter-run/SKILL.md` — Gotcha 「codegen 에 `--build-filter` 를 스스로 붙이지 마라」, codegen 절을 필터 없는 전체 + 전후 삭제 수 블록으로, 생성물을 추적하지 않는 저장소 문장, Rules MUST, 앱 이름
- `flutter-toolkit/skills/flutter-build/SKILL.md` — Gotcha 를 build_runner 2.16 사실로, Input 줄, codegen 절 블록, 보고 줄
- `flutter-toolkit/skills/flutter-preflight/SKILL.md` — Input 줄, codegen 절 블록, 보고 줄, 앱 이름
- `flutter-toolkit/skills/flutter-l10n/SKILL.md` — Slang 줄에서 i18n 폴더 필터를 빼고 블록을 가리킨다
- `flutter-toolkit/skills/flutter-transition/SKILL.md` — §5 날 codegen 을 블록으로, Gotcha 앱 이름, Flutter 3.47.5, `[미검증]` 네 칸
- `flutter-toolkit/references/project-detection.md` — Make 매핑 줄과 타겟 안 codegen 한 문장, 앱 이름 두 곳
- `flutter-toolkit/agents/widget-inspector.md` — 감지 기준 7 `### 7. 관례 대조`, Step 2 일곱 가지, 리포트 `Convention Match`, Rules MUST, 출처 줄 이름
- `flutter-toolkit/skills/flutter-widget/SKILL.md` — inspector 에 관례 표 넘기기, 카탈로그 타일 높이 문단, `[미검증]` 네 칸, Flutter 3.47.5
- `flutter-toolkit/skills/flutter-screen/SKILL.md` — inspector 에 관례 표 넘기기, `[미검증]` 네 칸
- `flutter-toolkit/skills/flutter-test/SKILL.md` — Gotcha 둘(위젯 시험 로캘 · build 도중 provider 수정), `[미검증]` 네 칸
- `flutter-toolkit/references/visual-evidence-protocol.md` 1.1.0 → 1.2.0 — Step 4 네 칸, 증거 블록 미검증 줄, 예시 한 줄
- `flutter-toolkit/skills/flutter-skeleton/SKILL.md` · `flutter-responsive/SKILL.md` · `flutter-hooks/SKILL.md` — `[미검증]` 네 칸 (hooks 는 프로젝트 이름 둘 · Freezed 도)
- `flutter-toolkit/skills/flutter-api/SKILL.md` · `flutter-error/SKILL.md` · `flutter-audit/SKILL.md` · `flutter-provider/SKILL.md` — Freezed 4.0.2 (provider 는 앱 이름도)
- `flutter-toolkit/references/flutter-ai-rules.md` — Freezed 4.0 한 줄 · 4.0.2, Flutter 3.47.5, 제목의 이름
- `flutter-toolkit/references/primitive-substitution-gate.md` · `figma-parity-self-verify.md` — 앱 이름 · 화면 조종 도구 이름
- `flutter-toolkit/evals/evals.json` — 사례 1(필터 없는 전체 · 전후 삭제 수) · 5(`[미검증]` 네 칸) · 16(관례 대조 단언 하나 더, 단언 7 개)

스킬 · 에이전트 frontmatter 는 그대로다(AP-04). flutter-toolkit README 의 AUTO 구간은 frontmatter 를 읽는다 — `sync-docs.py --check-only` 종료 코드 0.

## 반영한 처리 배정표 키

| 키 | 반영 |
| --- | --- |
| `F06` · `flutter:P-F06-codegen-delete-count` · `user-setup:P1` | build-filter 방향을 하나로 정했다 — 킷이 필터를 스스로 붙이지 않는다(근거 §2 「킷이 자동 선택하지 않음」). 사용자가 프로젝트 전용 필터 명령을 이름으로 부를 때만 쓴다. 킷이 codegen 을 직접 돌리는 다섯 자리(run · build · preflight · l10n · transition)는 전후 삭제 수 블록으로 돈다 — 경로 집합으로 세고, 두 번째 실행 뒤에도 첫 기준과 비교하고, codegen 실패와 남은 삭제를 종료 코드로 드러낸다. 대상은 두 제안 목록의 합집합(flutter-l10n · project-detection.md 포함)에 transition 을 더했다 (SK-01 · SK-02 · SK-03 · AR-01) |
| `F02` · `flutter:P-INSPECTOR-convention` | widget-inspector 감지 기준 7. 호출 스킬이 넘긴 관례 표만 읽고 화면 수를 정하지 않는다. `어긋남` 은 추출 후보 수에 더하지 않는다 (SK-04 · SK-05) |
| `F31` (UI 관례 대조 부분 · Phase 3 넘김) | 위 행과 같은 자리 (SK-04) |
| `F24` · `flutter:P-TEST-locale-buildmod` | flutter-test Gotcha 둘 (SK-06) |
| `F22` · `flutter:P-CATALOG-tile-height` | 타일 높이 부분만 — flutter-widget 카탈로그 등록 절, 안쪽 스크롤을 의도하지 않은 타일로 범위를 좁히고 높이 숫자 대신 내용 아래 끝을 잰다 (SK-07) |
| `visual-evidence-protocol.md:136` (Phase 1 넘김) | 같은 모양 여덟 줄을 같이 찾아 아홉 줄 전부 설계 가이드 §3.7 네 칸으로. 규약 판 1.2.0 (SK-09) |
| 러닝북 Phase 5 과제 셋 | 필터 방향(위 `F06` 행) · 인사이트 스프린트가 넣은 것(편집 파일 포맷 훅 · flutter-ui-verify · 규약 보강)을 다시 넣지 않음 · `flutter-transition` 앱 이름(킷 파일 전부에서 앱 · 프로젝트 · 화면 조종 도구 이름 빼기, SK-08) |

그 밖에 받은 것 — 근거 파일 §3 현행화 가운데 지금 틀린 문장 아홉 줄(Freezed 「최신 stable 3.2.5」 여섯 → 4.0.2, Flutter 「현재 stable 3.47.0」 셋 → 3.47.5, SK-10)과
build_runner 2.16 에서 `--delete-conflicting-outputs` 를 필수로 두던 두 줄(SK-03).

## 미반영 키와 사유

- `F25` (그룹 설정 시안 21 종) — 근거 파일 §2 F25 · §4 6 번이 이번 Phase 에서 규칙을 만들지 말라고 권한다. 한 프로젝트 기억(「여러 개 다 만들어 나란히」)과 방향이 반대라 사용자 확인이 먼저다
- `F22` 의 겹친 `ProviderScope` 부분 — 근거 파일에 없다. 이름 변경 뒤 재시작 실패는 인사이트 스프린트 규약 Step 2 가 맡는다(처리 배정표 비고)

## 넘기는 것 (명시적 미완)

| 대상 | 누가 | 할 일 |
| --- | --- | --- |
| `flutter-preflight` | 다음 사이클 Phase 5 | Phase 4 넘김(「필요하면」) — 기준 커밋 비교 근거가 이 Phase 근거 파일에 없어 미반영. 근거 파일에 기준 커밋 비교 근거가 오면 `/sprint` Step 3 판정 세 줄을 옮긴다 |
| `go_router` · `auto_route` | 다음 사이클 Phase 5 | 근거 §3 의 새 내용(go_router 18 · auto_route 11.1)을 더하는 일 — 지금 틀린 문장이 아니라 이번 묶음에서 뺐다. Riverpod 3.4.1 두 줄은 조회 날짜가 붙어 틀리지 않았다 |
| `--delete-conflicting-outputs` | 다음 사이클 Phase 5 | 명령 줄 열한 곳에서 이 플래그를 판에 따라 뺄지 — build_runner 2.16 에서 이 옵션이 경고인지 오류인지 근거 파일이 밝히지 않아 규칙 두 줄만 고쳤다 |
| `flutter-audit/SKILL.md:50` | 다음 사이클 (평가 쪽 가이드와 함께) | 평가 측 `[미검증]` 형식(이 줄과 widget-inspector 의 `[미검증]` 줄)은 생성 측과 모양이 달라 이번 네 칸 정리에서 뺐다 |
| `flutter-feature/SKILL.md:151` | 다음 사이클 Phase 5 | 사용자에게 보여 주는 codegen 안내 셋(`flutter-api/SKILL.md:336` · `flutter-feature/SKILL.md:151` · `flutter-screen/SKILL.md:272`)은 전후 삭제 수 블록을 가리키지 않는다 — 킷이 직접 돌리지 않는 안내라 이번에 바꾸지 않았다 |
| `$DART test` | 다음 사이클 Phase 5 | evals 사례 18 의 「생성 후 $DART test로 검증한다」 가 flutter-test Step 4 의 `$FLUTTER test` 와 어긋난다 |
| `docs/kaizen/flutter-changelog.md` · `docs/kaizen/flutter-research-log.md` | Final | 아래 changelog 단락 · 킷 로그 단락으로 Phase 5 항목을 쓴다 |
| `plugin.json` | Final | flutter-toolkit 버전(지금 0.8.0). 카이젠 스킬 버전 판단표로 스킬 프롬프트 · eval 기준 변경이라 minor |
| `docs/flutter-toolkit/` 문서 사이트 | Final F2 | 원본을 고친 참조 문서 넷의 페이지 — `visual-evidence-protocol.html`(규약 1.2.0 · 네 칸) · `flutter-ai-rules.html`(Freezed 4.0.2 · Flutter 3.47.5 · 제목 이름) · `project-detection.html`(필터 타겟 · 앱 이름) · `primitive-substitution-gate.html`(앱 이름)을 다시 만든다 |
| `Phase 6` | Phase 6 | 대조할 기존 화면 수는 플러터 규약 「2 개 이상」 · 스스로 고치기 상한 「3 회」 그대로다 — 이 Phase 가 바꾸지 않았다. design-kit 쪽 숫자를 이것에 맞춘다 |

CI 에 넣을 줄은 없다 — 새 시험 파일이 없고, 바뀐 평가 사례는 CI 가 이미 돌리는 `run-evals.py` 안에 있다.
Final 이 더 할 것: 이 Phase 는 공유 파일(marketplace · plugin.json · 루트 README · 루트 CLAUDE.md · `docs/` HTML · 감사 로그 · 실패 횟수 파일 · 처리 배정표 ·
`.github/workflows/ci.yml` · `docs/kaizen/*.md`)과 `harness/` 를 건드리지 않았다.

## changelog 한 단락

flutter-toolkit 이 codegen 에 `--build-filter` 를 스스로 붙이지 않는다. feature 인자가 와도 전체를 돌리고, 사용자가 프로젝트 전용 필터 명령을 이름으로 부를 때만 그 명령을 쓴다.
킷이 codegen 을 직접 돌리는 다섯 자리(flutter-run · flutter-build · flutter-preflight · flutter-l10n · flutter-transition)는 세 스킬에 글자 그대로 들어간 전후 삭제 수 블록으로 돈다 —
git 이 삭제로 보는 추적 파일을 경로로 세고, 늘어나면 한 번 더 돌린 뒤 첫 기준과 비교하고, codegen 실패나 남은 삭제를 종료 코드로 드러낸다. 남으면 멈추되 맞는 삭제일 수 있어 되돌리지 않는다.
생성물을 git 에 올리지 않는 저장소에서는 이 세기가 늘 0 이라 통과로 쓰지 않는다. `--delete-conflicting-outputs` 를 필수로 두던 규칙은 build_runner 2.16 에서 제거된 호환 옵션이 된 사실로 바꿨다.
widget-inspector 에 관례 대조(감지 기준 7)가 생겼다 — 호출 스킬이 넘긴 관례 표의 화면과 줄 모양 · 칩·뱃지 모양 · 아이콘 뜻을 대조하고, flutter-widget · flutter-screen 이 그 표를 넘긴다.
flutter-test 에 위젯 시험 로캘 고정과 build 도중 provider 수정 금지 Gotcha 가, flutter-widget 카탈로그 등록에 타일 높이 문단이 들어갔다.
생성 측 `[미검증]` 아홉 자리는 설계 가이드 §3.7 의 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 요구한다(규약 1.2.0). 킷 파일에서 특정 앱 · 프로젝트 · 화면 조종 도구 이름을 뺐고,
Freezed 는 4.0.2, Flutter 는 3.47.5 로 고쳤다. 평가 사례 1 · 5 · 16 이 새 동작을 기대한다.

## 킷 로그 한 단락 (flutter-toolkit)

2026-09-24 Phase 5 — flutter-kaizen. 트리거 orchestrator-phase-5. 처리 배정표 열 행(`F02` · `F06` · `F22` · `F24` · `F25` · `flutter:P-F06-codegen-delete-count` ·
`flutter:P-INSPECTOR-convention` · `flutter:P-TEST-locale-buildmod` · `flutter:P-CATALOG-tile-height` · `user-setup:P1`)과 러닝북 과제 셋, 앞 Phase 넘김 셋, 근거 파일 §3 현행화를 일곱 갈래로 묶었다. 근거:
[build_runner CLI 옵션 소스](https://github.com/dart-lang/build/blob/master/build_runner/lib/src/build_runner_command_line.dart) ·
[build-filter 통합시험](https://github.com/dart-lang/build/blob/master/build_runner/test/integration_tests/build_command_build_filter_test.dart) (필터는 공식 옵션, 필터 밖 생성물 보존 보장은 없음),
[build_runner CHANGELOG](https://raw.githubusercontent.com/dart-lang/build/master/build_runner/CHANGELOG.md) (2.16 부터 생성물을 기본으로 고치고 `--delete-conflicting-outputs` 는 제거된 호환 옵션),
[git-status](https://git-scm.com/docs/git-status) (`--porcelain=v1` 고정 형식 · 두 자리 `D`),
[Flutter 국제화](https://docs.flutter.dev/ui/accessibility-and-internationalization/internationalization) · [WidgetsApp.locale](https://api.flutter.dev/flutter/widgets/WidgetsApp/locale.html) ·
[TestPlatformDispatcher.locale](https://api.flutter.dev/flutter/flutter_test/TestPlatformDispatcher/locale.html) (로캘 기본값과 시험 로캘),
[Riverpod DO/DON'T](https://riverpod.dev/docs/root/do_dont) · [useEffect](https://pub.dev/documentation/flutter_hooks/latest/flutter_hooks/useEffect.html) (위젯이 provider 를 초기화하지 않는다 · build 중 동기 호출),
[ListView](https://api.flutter.dev/flutter/widgets/ListView-class.html) · [NestedScrollView](https://api.flutter.dev/flutter/widgets/NestedScrollView-class.html) ·
[ScrollView.shrinkWrap](https://api.flutter.dev/flutter/widgets/ScrollView/shrinkWrap.html) (겹친 스크롤은 저절로 협조하지 않음 · shrinkWrap 비용),
[Flutter 배포 메타데이터](https://storage.googleapis.com/flutter_infra_release/releases/releases_macos.json) (stable 3.47.5, 2026-09-18) ·
[Freezed pub API](https://pub.dev/api/packages/freezed) · [Freezed CHANGELOG](https://raw.githubusercontent.com/rrousselGit/freezed/master/packages/freezed/CHANGELOG.md) (4.0.2 · 생성자 파라미터 `final` 미지원).
근거 파일이 밝힌 한계 — 필터가 필터 밖 생성물을 지운다는 공식 문장은 없다(267 개는 내부 실측), 「고정 높이가 낮으면 안쪽이 스크롤을 먹는다」 는 공식 설명과 내부 실측을 합친 추론이다,
관례 대조와 시안 개수에는 외부 표준 근거가 없다, 삭제 수만으로 삭제의 옳고 그름은 가를 수 없다.

## 다음 사이클 메모

- §0-b 의 `3ac429d0` 세션(기기 경합 · 스크롤 대상 재시도)은 인사이트 스프린트가 넣은 flutter-ui-verify 몫이라 이번에 손대지 않았다
- 규약 `visual-evidence-protocol.md` 판이 1.2.0 으로 올라 Final F2 의 문서 사이트 재생성 대상에 그대로 든다
- 계약 오라클 경고 훅(사용자 설정 `lint-contract-oracle.sh`)이 서술 절의 `오라클 해소:` 줄을 읽지 않아, 해소 기록이 있는 조건 다섯을 계약을 고칠 때마다 다시 경고했다
- `LC_ALL=C.UTF-8` 에서 `[:alnum:]` 이 한글을 포함한다 — 영문 옵션 뒤 값을 거르는 정규식이 한국어 조사에 걸린다(D3 재실측). 셸 이식성 규약 후보
- 봉인 판 계약에서 도우미 코드 블록을 떼는 일을 이번에도 스크래치 스크립트로 했다 — Phase 3 · 4 · 7 과 같다
- 계약 피드백 자기진단 `implementation_leakage` 가 true — 조건 줄에 측정 도우미 이름이 들어갔다. 산출물이 문서 문장이라 새 문장을 글자 그대로 세는 자리가 필요했다
