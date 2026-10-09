# Sprint Feedback
Feature: flutter-toolkit 공용 위젯 놀이터와 기본기 검사
Evaluated: 2026-10-09 17:27
Verdict: APPROVE
Iteration: 2

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/flutter-catalog/.harness/sprint-contract-flutter-catalog.md
- sha256: 98db0458caa39b0e369cc80250e05fdb00ab95bc8b5641c5a32ac178146a2f06 (1차와 같음)
- status: active
- slug: flutter-catalog
- 선택 근거: ladder 1 명시경로 (호출 인자)
- seal_status: SEAL_OK · measure_status: MEASURE_OK (1차 판정 때 확인. 계약 파일은 봉인 커밋 72d276b8 과 `git diff` 차이 0 줄이라 그대로)
- 재조사: 봉인 커밋 대조 차이 0, 재봉인 없음
- codex_audit.mode: off → 조건을 이 평가자가 직접 판정
- 재확인(Step 5): 일치 (저장 직전 sha256 같음)
- status_transition: active -> done
- 1차 앞 회차 리포트: 이 파일의 1차 판정서(REJECT)를 덮어썼다. 사본은 scratchpad/qa2/feedback.iter1.md

## Amendments
- amendments: 3 (A-01 · A-02 · A-03)
- PASS 근거 가능: 3 — A-01 · A-02 는 relaxing + anchored (2026-10-09 16:05 사용자 승인), A-03 은 narrowing (승인 없이 가능)
- A-03 대조: `git diff f89709ac..HEAD -- .harness/.meta` 의 `measure.sh` 차이는 사례 `gen-unreadable` 추가와 사례 목록 줄 한 곳뿐. 기존 사례의 판정식은 그대로(차이 없음). 통과해야 할 사례가 하나 늘었으므로 narrowing 이 맞다
- PASS 근거 불가: 0

## Deletions
- deletions_range: 72d276b8..HEAD
- 커밋 구간 삭제: 0 / 커밋하지 않은 삭제: 0 / 선언 밖 삭제: 0
- 추적 파일 중 커밋하지 않은 변경: 0

## Cross-Diagnosis Handoff
- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 위 path · 이 판정 전문
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가?
  2. 0 건 · 빈 출력을 근거로 PASS 한 조건 중 문제가 있어도 0 을 냈을 측정이 있는가? 검사 산출물(생성기 · 시험 파일) 조건에서 규칙 10 의 다섯 가지 가운데 돌리지 않은 것이 있는가?

## 이번 회차에서 다시 잰 범위
1차 이후 바뀐 파일은 3 개뿐이다 (`git diff f89709ac..HEAD --stat`): `catalog_gen.dart.tmpl`(생성기 틀), `measure.sh`, 개정 파일. 그 밖의 틀 · 스킬 문서 · 계약은 차이가 없다.
복사본은 평가자 전용 새 폴더(scratchpad/qa2)에 만들었다 (`MEASURE_DIR`). `fc-measure` 와 다른 파일은 건드리지 않았다.

## Results

### Skill (6/6) — 바뀐 파일 없음
- [x] 스킬-01 ~ 06 PASS — 1차 근거 유지. 스킬 문서 · 참조 문서 · README 차이 0 (`git diff f89709ac..HEAD -- '*.md' ':(exclude).harness/*'` 줄 수 0). 이번에도 `sync-docs.py flutter-toolkit --check-only` 「모든 README가 동기화 상태입니다」

### Script (9/9)
- [x] 스크립트-01 PASS (L3) — 새 틀로 `gen-ok` 종료 0, 속성 일곱 개 모두 `has`, `VERDICT PASS`. 생성물이 1차 생성물과 `diff -q` 로 같다(`SAME_GEN`) → 정상 입력의 동작이 바뀌지 않았다
- [x] 스크립트-02 PASS — `gen-unsupported`: 종료 1 · before=after=1791533991 · `IFChipContainer=1` `padding=1`
- [x] 스크립트-03 PASS (L3) — 계약 측정: `gen-missing` · `gen-unknown` 둘 다 `VERDICT PASS` (`SplitPill=1` · `PressableData=0` · `NoSuchWidget=1`). 1차 FAIL 사유였던 읽지 못한 파일 처리를 평가자가 사본에서 직접 다시 시험했다 (Check Artifacts ③)
- [x] 스크립트-04 PASS — `fund-run`(testDone success 1121 · error 312, 1차와 같음) 뒤 `sizing` `VERDICT PASS`. IFToggle `52.0x28.0 → 52.0x28.0`, StateProbe `40.0x30.0 → 40.0x40.0` FAIL
- [x] 스크립트-05 PASS — `overflow`: `IFToggle.new=24(24)` `IFButton.new=72(72)`, entries=22, OverflowProbe_FAIL=48, IFToggle_notPASS=0, `VERDICT PASS`
- [x] 스크립트-06 PASS — `font`: base_exit 0 · base_tests 1 · changed_lines 6 · neg_exit 1 · hint 6 · restored_diff 0
- [x] 스크립트-07 PASS — `lint`: exit=1 report_exit=0 chip332=1 chip333=1 button299=1 toggle=0
- [x] 스크립트-08 PASS — `analyze`: 종료 0 · `No issues found!` (대상 5 곳에 새 생성기 `tool/` 포함). 1차 양성 대조 `analyze-pos`(오류 1)는 측정 파일 · 대상이 안 바뀌어 유지
- [x] 스크립트-09 PASS — `icon-touch`: TapSmallProbe FAIL · TapBigProbe PASS (IconProbe 두 줄은 sizing 과 같은 표에서 1차와 같이 확인)

### Error (1/1)
- [x] 오류-01 PASS — `wrapper`: good_AppError_rows=74 good_hint=0 bare_AppError_rows=75 bare_fail_hint=75 IFToggle_same=True restored_diff=0

### Architecture (7/7)
- [x] 구조-01 PASS — 틀 파일 11 개, `.dart` 0 (`find` 재측정)
- [x] 구조-02 PASS — 금지 낱말 0 (재측정). `flutter_hooks` 사용 틀은 1차 근거 유지
- [x] 구조-03 PASS — `package:app/` 틀 0 (재측정)
- [x] 구조-04 PASS — `install`: second_exit=1 · marker_kept=1 · partial_exit=1 · partial_files=2 · dev_deps_added=2
- [x] 구조-05 PASS — 생성물이 1차와 같고 놀이터 틀 · `web_check.js` · 캡처 5 장 모두 1차 이후 차이 0이라 1차 근거(`steps 6 failed 0` · `errors 0` · 캡처 5 장 직접 확인)를 유지한다. 이번 회차는 크롬 단계를 다시 돌리지 않았다
- [x] 구조-06 PASS — `tmpl-hosts`: app_imports=0 · analyze_exit=0 · font_exit=0 · font_tests=1 · build_exit=0 · restored_diff=0 (새 생성기가 깔린 상태에서 통과)
- [x] 구조-07 PASS — `validate-plugin.py flutter-toolkit` 종료 0

### Anti-patterns (2/2)
- [x] 금지-03 PASS — `--check=code-fence` 종료 0
- [x] 금지-04 PASS — `--check=frontmatter` 종료 0

### Reusability (2/2)
- [x] 재사용-01 PASS — 공개 클래스 2 · private 0 (재측정 private 0)
- [x] 재사용-02 PASS — 1차 근거 유지 (스킬 문서 차이 0)

### Diagnostics (2/2, N/A 2)
- 진단-01 · 진단-03 N/A — 이번 범위가 `scripts/release.sh` 를 안 건드린다(변경 파일 3 개 모두 범위 안). 1차 확인 유지
- [x] 진단-02 PASS — 1차 이후 바뀐 .md 0 개, 1차 측정(11 개 · `error MD` 0) 유지
- [x] 진단-04 PASS — 구조-05 근거 유지

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (31 - 0) / 31 = 1.00 (임계 0.60)
- 이번 회차 구조-05 · 스킬 · 진단-02 는 새로 재지 않고 「바뀐 파일 없음」 차이로 근거를 이어받았다. 이는 도구 부재가 아니라 호출 쪽이 허용한 범위이며 미검증 장부에 올리지 않는다

## Discrimination
- 해당 없음(9 항 아님). 결합 확인: 새 시험 결과 표는 1차와 같은 방식(`entry.build(values)` 로 진짜 위젯)이다. 변이 실행은 하지 않음 (discrimination: static-only)

## Check Artifacts
- 대상: 스크립트-03 의 `tool/catalog_gen.dart.tmpl`(바뀐 검사), 측정 사례 `gen-unreadable`
- ① 첫 칸만 읽기: 평가자 사본 `scratchpad/qa2/app/lib/zz_shared` 에 파일 3 개(읽을 수 없는 `hid.dart` · 문법이 깨진 `bad.dart` · 정상이지만 목록에 없는 `ok.dart`)를 두었다. 출력에 세 파일의 문제가 모두 나왔다: `읽지 못한 파일: lib/zz_shared/hid.dart (Permission denied)` · `문법이 깨진 파일: lib/zz_shared/bad.dart (Expected to find '}'.)` · `목록에 없는 공용 위젯: ZzOk`. 첫 문제에서 멈추지 않는다. 종료 1
- ② 실행 목록: 이번 변경은 새 시험 파일이 없다. 새 측정 사례 `gen-unreadable` 은 `measure.sh` 의 `case` 문과 도움말 사례 목록 두 곳에 모두 있고 실제로 돌았다 (출력 `unreadable_exit=1 ...`)
- ③ 못 읽는 칸 + 실제 위반: 1차 재현 그대로 — 목록이 완전하지 않은 상태에서 못 읽는 파일이 있는 사본을 만들었다. 못 읽는 칸이 따로 나오고(경로와 이유) 같은 폴더의 다른 위반(`ZzOk`)도 잡힌다. 모두 종료 1. 1차에서는 종료 0 이었다
- 양성 대조(읽기 가능한 두 파일): 못 읽는 파일이 없는 상태 `ZzHid` · `ZzOk` 두 이름이 모두 출력되고 종료 1 (검사가 살아 있음). 처음 시도에서 목록 파일에 `shared_dir` 줄이 없어 종료 0 이 나왔으나, 이는 내 사본 설정 실수였고 줄을 넣은 뒤 위 결과를 얻었다
- 사본 원복: 사본 폴더 삭제 · 목록 파일 원복 후 생성기 종료 0
- ④ zsh · bash: 해당 없음 (Dart 틀 · 해석기 고정 `bash` 스크립트)
- ⑤ 효과 증명: 알려진 답 — `chmod 000` 한 파일 → 「읽지 못한 파일」 한 줄, 문법 깨진 파일 → 「문법이 깨진 파일」 한 줄. 부모가 보고한 음성 대조(옛 판 생성기로 `unreadable_path=0 broken_path=0`)는 평가자가 다시 돌리지 않았으나 1차 평가자 사본 시험(옛 판은 안내 없음, 종료 0)이 같은 결론이다

## Evidence Validity
- 검사 대상 증거: 이번 회차 직접 수집 · 0 이 기대값인 측정 전부 대상 수와 양성 대조 있음 (`gen-unknown` 은 이름 1, 금지 낱말 측정은 1차에서 대조 확인)
- 무효 판정: 0 건

## Summary
- Total: 31/31 (N/A 2 포함: 진단-01 · 진단-03)
- Verdict: APPROVE
- 1차 FAIL(스크립트-03) 해소. 나머지는 재측정 또는 「바뀐 파일 없음」 근거로 유지

## Improvement Suggestions
- [스크립트-03] 측정-방식-불일치 — 계약 조건 문구에 「읽을 수 없거나 문법이 깨진 파일은 경로를 출력하고 종료 1」 을 더하는 것은 계약 개정(A-03)이 이미 측정으로 담았으니 추가 제안 없음. 다음 계약에서는 조건 문구도 같이 적는 것을 권한다
- [구조-05] 측정-환경-오염 — 외부 망이 막힌 환경에서는 배포용 빌드에 `--no-web-resources-cdn` 을 더해야 같은 결과가 난다 (1차 제안 유지)
