# Phase 5 계약 검토 — kaizen-0924-p05-flutter-toolkit

검토: 2026-09-25 · 독립 Claude 검토자(REVIEW, 사용자 승인 대신) · 대상 `.harness/sprint-contract-kaizen-0924-p05-flutter-toolkit.md`
(봉인 전 초안 · 조건 26 · 기능 조건 16). 개정 파일은 아직 없다. 작업 폴더의 파일은 고치지 않았고, 다시 돌린 것은 전부
`/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p5review/` 안에서 했다.

결론부터: 계약 표의 측정 값은 전부 같게 다시 나왔다. 그래도 봉인 전에 네 곳을 고쳐야 한다.

1. zsh 에서 SK-08 (b) 가 시작 커밋 판에서도 0 을 낸다 (C1)
2. ER-01 의 낱말 셋은 실제 notes 에서 떨어질 수 없다 (C2)
3. 킷이 codegen 을 직접 돌리는 다섯째 자리(`flutter-transition` §5)에 전후 삭제 수가 없다 (C3)
4. 생성물을 git 에 올리지 않는 프로젝트에서는 새 삭제 세기가 늘 0 이고 그대로 통과로 보고된다 (C4)

## 1. 다시 돌려 본 것

시작 커밋 `7925890` 을 `git archive` 로 풀어 B 를 만들고, 같은 트리에 `p5draft/mock.py` 를 적용해 M 을 만들었다(61 치환 · bad 0,
초안 폴더의 M 과 `diff -rq` 차이 0). 측정은 계약 본문에서 **글자 그대로 떼어 낸** 공통 정의 블록과 도우미 셋(`delgate.sh` ·
`new-warnings.sh` · `ar01.sh`)으로 돌렸다. 공통 정의에서 바꾼 곳은 `AM` 줄(가짜 개정 파일)과 `E=` 줄(`PRE_E`) 둘뿐이다.

| 측정 | B (bash) | M (bash) | 계약 표와 |
| --- | --- | --- | --- |
| SK-01 (a) · (b) | `2 1 1 1 1 1` · 여덟 값 0 | 여섯 값 0 · 여덟 값 1 | 같다 |
| SK-02 (a) | `EMPTY` | `15839f98ccc530a0` 한 종 | 같다 |
| SK-02 (b) 세 스킬 · `bash -e` · `zsh` | — | 스물다섯 줄 = `K1`~`K5` 답 다섯 번 | 같다 |
| SK-02 (c) · SK-04 · SK-06 · SK-07 | 전부 0 | 전부 1 | 같다 |
| SK-03 | `1 0` · `1 0 0 0` | `0 1` · `0 1 1 1` | 같다 |
| SK-05 | `0` · `0` · `same` | `1` · `1` · `same` | 같다 |
| SK-08 (a)(b)(c) | `9` · `4` · `0` | `0` · `0` · `1` | 같다 (bash 에서만 — C1) |
| SK-09 (a) · (b) · (c) · (d) | `9` · 새 0 옛 1 · 0 · `1 1 1 1 1` | `0` · 새 1 옛 0 · 1 · `1 1 1 1 1` | 같다 |
| SK-10 (a) · (b)(c) · (d) | `9` · 0 · `1` | `0` · 1 · `1` | 같다 |
| AR-01 | `22 0 0 0 0 0 0 6` | `22 1 1 1 1 1 1 7` | 같다 |
| RE-02 · AP-04 | `0 0` · `0` | `1 0` · `0` | 같다 |
| DG-02 스물두 파일 | — | 전부 `new_warnings=0` · `LINT_NOT_RUN` 0 | 같다 |

- Step 6.2 두 명령 `26` · `16`, Step 6.5 헤더 목록 허용 안 · `OK conditions=26` · `OK 미실측 0`. 조건은 전부 조건 절 안에 있다
- 측정 커버리지 검출기: `UNCOVERED` 4 건(SK-01 · SK-09 · SK-10 · ER-01) — 네 건 모두 `## 범위 경계` 에 해소 기록이 있다
- 커밋을 재는 측정은 초안의 예행 복제본 `p5draft/rh` 에 계약 블록을 그대로 대어 다시 쟀다: AR-03 ① `0` · ② `0 23` · ③ `0 SEAL_OK` · ER-01 셋째 `0`. 같다
- 작업 폴더(시작 커밋 상태): `validate-plugin.py flutter-toolkit` `V1`~`V10` 전부 OK · `run-evals.py flutter-toolkit` `Total: 22 passed, 0 failed` 종료 0 ·
  `validate-post-kaizen.py --since 7925890…` `scope-isolation` PASS · `doc-contracts` PASS · `docs-site-regen` SKIP. 같다

초안 목록 밖에서 내가 넣어 본 변이:

- `comm -13` 두 곳을 `comm -23` 으로 뒤집음 → `K2` · `K3` · `K4` 가 답에서 떨어진다
- 두 번째 실행 뒤 비교 결과를 비움 → `K2` · `K4` 가 떨어진다
- `N4`(첫 codegen 줄의 `|| RC=$?` 제거)를 직접 돌림 → `K5` 가 `codegen_exit=0 … 종료=0` 으로 떨어진다. 계약 기록과 같다
- awk 의 `$(0)` 를 `$0` 으로 되돌림 → 알려진 답 다섯 줄은 그대로 통과하지만 `validate-plugin.py --check=arg-substitution`(V9)이
  `3 arg-substitution hazard(s)` 로 잡는다. DG-05 (a) 가 V9 를 포함하므로 막힌다

## 2. 처리 배정표 · 러닝북 · 앞 Phase 넘김

처리 배정표에서 `배정` 칸이 `Phase 5` 인 행은 열이다 — `F02` · `F06` · `F22` · `F24` · `F25` · `flutter:P-F06-codegen-delete-count` ·
`flutter:P-INSPECTOR-convention` · `flutter:P-TEST-locale-buildmod` · `flutter:P-CATALOG-tile-height` · `user-setup:P1`. 열 행 모두
배경 표에 반영이나 미반영 사유로 있고, ER-01 이 열 키를 notes 에서 센다. 러닝북 추가 과제 셋(필터 방향 · 다시 넣지 않기 · 특정 앱 이름)과
앞 Phase 넘김 셋(Phase 1 `visual-evidence-protocol.md:136` · Phase 3 `F31` · Phase 4 `flutter-preflight`)도 빠짐없다. Phase 4 넘김은
「필요하면」 이라 미반영 사유(이 Phase 근거 파일에 없음)를 받아들인다.

필터 방향(킷이 스스로 붙이지 않고, 사용자가 이름으로 부를 때만 쓴다)은 근거 파일 §2 · §4 1 번 문구와 같다. 새 URL 은 근거 파일 밖이 0 개다(AR-02).

## 3. 범위 · 공유 파일 · 조건끼리

- 고치는 스물셋은 전부 러닝북 표의 Phase 5 범위(`flutter-toolkit/` · `docs/flutter/`) 안이다. 새 파일은 없다
- 공유 파일과 `harness/` 를 고치려는 곳이 없다. ER-01 셋째 · 넷째와 AR-03 ① ② 가 커밋으로 잰다. `docs/kaizen/flutter-*.md` 를 Final 에 넘긴 것은
  오케스트레이터 Final 단계가 `docs/kaizen/flutter-changelog.md` 에 Phase 5 항목을 쓰므로 맞다
- Phase 6 초안은 `visual-evidence-protocol.md` 를 읽기만 하고 `:52` · `:91` 숫자를 제 시작 커밋 판으로 잰다. 이 계약은 그 두 줄을 건드리지 않고
  줄 번호도 밀지 않는다(바뀌는 줄은 `:3` 한 줄 교체 · `:136-137` · `:156` · `:164`). 부딪히지 않는다
- 조건끼리: SK-09 (a) 는 킷 전체에서 「`[미검증]` + 사유」 모양을 0 으로 요구하는데 SK-04 는 inspector 에 `[미검증] 관례 표 없음` 을 새로 넣는다.
  정규식에 걸리지 않아 값은 부딪히지 않고, 평가 측 `[미검증]` 모양은 다음 사이클로 넘긴다고 적혀 있다(ER-01 `flutter-audit/SKILL.md:50`). 받아들인다

## 4. 조건마다 FAIL 한 문장

전부 쓸 수 있다. 예를 들어 SK-02 는 「세 스킬의 블록 지문 값이 둘 이상이거나 비었고, 또는 알려진 답 스물다섯 줄 가운데 하나라도 다르고,
또는 아홉 문장 가운데 하나가 정해진 절에 없다」, AR-03 은 「`flutter-toolkit/` · `docs/flutter/` 를 건드린 서명 없는 커밋이 있거나,
서명 커밋이 스물셋 · `.harness/` 밖을 건드렸거나, 이 계약이 봉인되지 않았다」 다. 다만 ER-01 은 문장은 쓸 수 있어도 측정이 그 FAIL 을
볼 수 없는 칸이 셋 있다(C2).

## 5. 고칠 것

### C1 — 측정 공통 정의 · SK-08: bash 가 아니면 멈춘다

계약은 「bash 셸에서 돈다」 고 적었지만 막지는 않는다. 이 세션의 Bash 도구는 zsh 이고, 그 zsh 는 `grep` 을 셸 함수로 바꿔 다른 검색 프로그램을 부른다.
공통 정의 블록을 파일로 저장해 `. 파일` 로 잇는 방식(계약이 허용한 방식)을 zsh 에서 쓰면 SK-08 (b) 의 낱말 경계 정규식이 조용히 0 을 낸다.

검토 실측(2026-09-25): 같은 블록 · 같은 트리에서 SK-08 (b) 가 B 판 **bash 4 · zsh 0**. 나머지 텍스트 측정은 두 셸에서 같았다.
zsh 로 재면 양성 대조가 사라져 `apps` 가 남아도 PASS 가 된다.

고칠 문구 — 공통 정의 블록의 첫 주석 줄 바로 아래에 한 줄:

```bash
[ -n "${BASH_VERSION:-}" ] || { echo "NOT_BASH — 이 블록과 측정을 bash -c 안에서 다시 돌린다"; exit 2; }
```

그리고 측정 공통 정의 절 첫 문단 끝에 한 문장: 「Claude Code 의 zsh 는 `grep` 을 다른 검색 프로그램으로 바꿔 부른다 — SK-08 (b) 가 시작 커밋 판에서
bash 4 · zsh 0 으로 갈렸다(검토 실측 2026-09-25). 그래서 bash 가 아니면 멈춘다.」 봉인 전 실측 목록에 「zsh 에서 `. 파일` → `NOT_BASH` · 종료 코드 2」 한 줄.
(검토 실측: 이 줄은 zsh 부분 셸에서 `NOT_BASH` · 종료 2, `bash -c` 에서 통과.) `delgate.sh` 의 `RUNNER=zsh` 는 함수 없는 맨 zsh 를 띄우므로 SK-02 (b) 는 영향이 없다.

### C2 — ER-01: 낱말 셋은 같은 줄의 사유와 함께 센다

`flutter-preflight` 는 notes 의 「바꾼 파일」 목록(`flutter-toolkit/skills/flutter-preflight/SKILL.md`)에, `--delete-conflicting-outputs` 는
changelog 단락(SK-03 을 설명하면)에, `Phase 6` 은 다른 메모에 거의 반드시 나온다. 그러면 넘김 줄 자체를 빠뜨려도 값이 1 이다.
초안의 예행 notes 는 한 줄에 낱말 하나씩이라 이 경우를 보지 못했다.

검토 실측: 「바꾼 파일 · changelog · 미반영」 세 부분을 갖춘 가짜 notes 에서 넘김 세 줄만 지운 사본 → 지금 측정 `1 1 1`(못 잡는다), 아래 측정 `0 0 0`.
세 줄이 있는 사본 → 아래 측정 `1 1 1`.

고칠 문구:

- ER-01 측정의 `for t in …` 열넷 목록에서 `'flutter-preflight'` · `'--delete-conflicting-outputs'` · `'Phase 6'` 을 빼고(열하나), 다음을 더한다 —
  ``N=$(git show "$END:$NOTES"); printf '%s %s %s\n' "$(printf '%s\n' "$N" | grep -F 'flutter-preflight' | grep -cF '기준 커밋')" "$(printf '%s\n' "$N" | grep -F -- '--delete-conflicting-outputs' | grep -cF '경고인지 오류인지')" "$(printf '%s\n' "$N" | grep -F 'Phase 6' | grep -cF '2 개 이상')"``
  세 값 1 이상
- ER-01 조건 줄 산문의 「각각 1 회 이상 있고」 뒤에 「— 그 가운데 `flutter-preflight` · `--delete-conflicting-outputs` · `Phase 6` 은 같은 줄에
  `기준 커밋` · `경고인지 오류인지` · `2 개 이상` 이 함께 있어야 한다」 를 넣는다
- `## 범위 경계` 「넘기는 것」 의 세 문자열 설명에 같은 요구를 적는다 — BUILD 가 세 낱말을 사유와 한 줄에 쓰도록
- 봉인 전 실측에 위 가짜 notes 두 사본의 값을 적는다

### C3 — 킷이 codegen 을 직접 돌리는 다섯째 자리

배경 표와 조사 기록 초안은 「전후 삭제 수는 필터와 상관없이 매번 센다」 고 쓰고 `flutter-run` Rules 에 MUST 를 둔다. 그런데
`flutter-transition/SKILL.md:303`(§5 「route codegen을 실행한다」 bash 블록)은 날 codegen 한 줄을 그대로 돌린다. `flutter-l10n` 은 블록을 가리키게
고쳤는데 transition 은 빠졌다. 이 파일은 이미 스물셋 안이라 범위가 늘지 않는다. 사용자에게 보여 주는 안내 셋(`flutter-api/SKILL.md:336` ·
`flutter-feature/SKILL.md:151` · `flutter-screen/SKILL.md:272`)도 블록을 가리키지 않는데 계약 어디에도 적혀 있지 않다.

고칠 문구:

- 개선안: `flutter-transition` `### 5. Codegen (필요 시)` 의 bash 블록을 한 문장으로 바꾼다 —
  「`HAS_GO_ROUTER_BUILDER`이면 route codegen 을 `flutter-run` codegen 절의 블록으로 돌린다 — 전후 삭제 수를 센다.」
- SK-01 (b) 에 값 둘을 더한다(여덟 → 열):
  ``toks "$(sect "$TRN" '### 5. Codegen')" '`flutter-run` codegen 절의 블록으로 돌린다'`` 1 ·
  ``sect "$TRN" '### 5. Codegen' | grep -c 'build_runner build'`` 0.
  검토 실측: 시작 커밋 판 `0` · `1`, 지금 모의본도 `0` · `1`(아직 안 고침). SK-01 산문의 「여덟 문장」 도 같이 고친다
- ER-01 넘김 문자열에 `flutter-feature/SKILL.md:151` 을 더한다(스물하나 → 스물둘). notes 에 쓸 줄: 「사용자에게 보여 주는 codegen 안내 셋
  (`flutter-api/SKILL.md:336` · `flutter-feature/SKILL.md:151` · `flutter-screen/SKILL.md:272`)은 전후 삭제 수 블록을 가리키지 않는다 — 다음 사이클」
- 배경 표 `F06` 행과 조사 기록 초안의 「매번 센다」 를 「킷이 codegen 을 직접 돌리는 다섯 자리(run · build · preflight · l10n · transition)는 매번 센다」 로 좁힌다

### C4 — 생성물을 git 에 올리지 않는 프로젝트에서 늘 0

블록은 git 이 추적하는 파일의 삭제만 센다(블록 주석도 「추적 파일」). `.gitignore` 에 `*.g.dart` 를 둔 프로젝트에서는 생성물이 다 지워져도
`new=0` 이고 종료 코드가 0 이라, 스킬 문장 「`new` 가 0 이면 통과다」 에 따라 통과로 보고된다. 알려진 답 `K1`~`K5` 는 모두 생성물을
추적하는 저장소라 이 경우를 보지 못한다. 이 킷이 새로 가르치는 측정이 0 을 내는데 그 0 이 「셀 수 없음」 인 경우다.

검토 실측(2026-09-25, `p5review/k6`): `*.g.dart` 를 무시하는 저장소에서 codegen 자리에 `rm -f lib/a.g.dart lib/b.g.dart lib/c.g.dart` 를 넣고
M 판 `flutter-run` 블록을 돌림 → `삭제 before=0 after=0 new_first=0 new=0 codegen_exit=0` · 종료 0. 생성물 셋은 실제로 사라졌다.

고칠 문구:

- 세 스킬 codegen 절(블록 바로 아래 문단)에 같은 문장을 넣는다 — 「생성물을 git 에 올리지 않는 프로젝트에서는 이 세기가 생성물 삭제를 보지 못해
  늘 0 이다 — `git ls-files -- '*.g.dart' '*.freezed.dart'` 가 비면 `new=0` 을 통과로 쓰지 말고 보고 줄 뒤에 `추적된 생성물 0 개 — 삭제를 셀 수 없다` 를 붙인다.」
- SK-02 (c) 에 세 값을 더한다(아홉 → 열둘): ``toks "$(sect "$RUN" '### codegen [feature]')" '이 세기가 생성물 삭제를 보지 못해 늘 0 이다'`` ·
  같은 문장으로 `"$BLD"` 의 `'### 1. codegen [feature]'` · `"$PRF"` 의 `'### 2. codegen [feature]'` 각 1. 시작 커밋 판 0 을 확인하고 문장 삭제 대조 세 경우를 봉인 전에 돌린다
- 블록 자체는 바꾸지 않으므로 SK-02 (a) 지문 값과 (b) 알려진 답은 그대로다

C1~C4 를 반영한 뒤 BUILD 는 `mock.py` 를 고쳐 다시 적용하고, 바뀐 조건(SK-01 (b) · SK-02 (c) · ER-01)의 시작 커밋 판 · 모의본 값과
문장 삭제 대조, DG-02 를 다시 재서 봉인 전 실측 표에 적는다. 조건 줄 수(26)와 기능 조건 수(16)는 그대로다.

## 6. 막지 않는 제안

- **O1 SK-01 (a)** — 다섯 파일의 `--build-filter=` 대신 킷 전체를
  ``grep -rnE -- '--build-filter(=|[[:space:]]+["'"'"'])' "$E/$FT" | grep -c .`` 0 으로 재면 `=` 없이 띄어 쓴 필터와 다른 스킬에 새로 생긴 필터도 잡는다
  (검토 실측, bash: 시작 커밋 판 `6` · 모의본 `0`)
- **O2** — `## 범위 경계` 해소 기록에 「awk `$(0)` · `${1}` 을 `$0` · `$1` 로 되돌리면 알려진 답은 통과하지만 DG-05 (a) 의 V9 가 잡는다(검토 변이)」 한 줄
- **O3** — notes 다음 사이클 메모에 두 줄: §0-b `3ac429d0`(기기 경합 · 스크롤 대상 재시도)은 인사이트 스프린트가 넣은 flutter-ui-verify 몫이라
  이번에 손대지 않았다 · 규약 판이 1.2.0 으로 올라 Final F2 의 문서 사이트 재생성 대상에 그대로 든다

VERDICT: CHANGES

## 2 회차

검토: 2026-09-25 · 같은 독립 Claude 검토자 · 대상은 1 회차 지적을 반영한 초안(조건 26 · 기능 조건 16, 개정 파일은 아직 없다).
작업 폴더의 파일은 이 절을 덧붙인 것 말고는 고치지 않았다. 다시 돌린 것은 전부
`/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p5review2/` 안에서 했다.

결론부터: C1~C4 와 O1~O3 이 전부 반영됐고, 계약 본문에서 글자 그대로 떼어 다시 잰 값이 봉인 전 실측 표와 모두 같다.
봉인을 막을 새 결함은 없다. 봉인 전에 넣으면 좋은 것 넷(D1~D4)을 3 절에 적는다. 넷 다 맞는 결과를 FAIL 로 보는 쪽이거나,
`mock.py` 대로 적용하면 문제가 생기지 않는 자리라 막지 않는다.

### 1. 1 회차 지적 반영 확인

| 지적 | 계약에 들어간 자리 | 다시 잰 값 |
| --- | --- | --- |
| C1 bash 가 아니면 멈춤 | 공통 정의 둘째 줄 · 측정 공통 정의 절 첫 문단 끝 문장 · 봉인 전 실측 「bash 가드」 줄 | 블록을 이 세션 zsh 의 부분 셸에서 `. 파일` → `NOT_BASH …` 한 줄 · 종료 2. `bash -c` 에서는 가드를 지나 `END_UNRESOLVED`(개정 파일이 아직 없다) · 종료 2 |
| C2 세 낱말은 사유와 한 줄로 | ER-01 산문 · 측정 셋째 줄 · 범위 경계 「넘기는 것」 끝 · 봉인 전 실측 | 초안 가짜 notes 를 작은 저장소에 커밋하고 계약 측정 세 줄을 글자 그대로 돌림: 온전한 사본 `1 1 2 1 1 1 1` · 열둘 전부 1 · `1 1 1` / 넘김 세 줄 뺀 사본 같은 줄 `0 0 0` / `flutter-feature/SKILL.md:151` 줄 뺀 사본 열둘 가운데 열째 0 / `flutter-preflight` 줄에서 사유만 떼어 낸 사본 `0 1 1` |
| C3 transition §5 | 배경 · 편집 전 감사 · 개선안 초안 · SK-01 (b) · ER-01 스물둘 · 조사 기록 초안 | SK-01 (b) transition 값: 시작 커밋 판 `0` · 옛 줄 `1`, 모의본 `1` · `0`. 모의본에서 그 문장만 뺀 사본 `0`, 옛 bash 블록을 되살린 사본은 옛 줄 `1`. 모의본 조사 기록 31 줄이 「다섯 자리(run · build · preflight · l10n · transition)」 로 좁혀졌다 |
| C4 생성물을 추적하지 않는 저장소 | 세 스킬 codegen 절(블록 바로 아래 문단) · SK-02 (c) 열셋 | 시작 커밋 판 0 · 모의본 1. 세 문장을 하나씩 뺀 사본에서 그 값만 0 |
| O1 킷 전체 필터 세기 | SK-01 (a) | 시작 커밋 판 `6` · 모의본 `0`. 모의본에 `--build-filter "lib/**"` 한 줄을 더한 사본 `1` |
| O2 awk `$(0)` 변이 | 범위 경계 해소 기록 | 있다 |
| O3 다음 사이클 메모 두 줄 | 범위 경계 「넘기는 것」 끝 | 있다 |

### 2. 다시 돌려 본 것

- `p5draft/mock.py` 를 시작 커밋 `7925890` 판에 적용 → `edits=62 bad=0`. 초안의 `p5draft/M` 과 `diff -rq` 차이 0
- 계약 본문의 bash 블록 넷과, 조건마다 「측정:」 뒤의 두 겹 백틱 명령을 프로그램으로 떼어 그대로 돌렸다. 공통 정의에서 바꾼 곳은
  `END` 를 구하는 네 줄과 `git archive "$END"` 자리(모의본을 복사) 둘뿐이다
- 텍스트 측정은 전부 계약 표와 같다 — SK-01 (a) `6 1` → `0 0` · (b) 아홉 값 0 · 옛 줄 1 → 아홉 값 1 · 옛 줄 0 / SK-02 (a) `EMPTY` → `15839f98ccc530a0` 한 종 ·
  (b) 스물다섯 줄이 `K1`~`K5` 답 다섯 번 · (c) 열셋 0 → 1 / SK-03 `1 0` · `1 0 0 0` → `0 1` · `0 1 1 1` / SK-04 ~ SK-07 전부 0 → 1, SK-05 (c) 두 판 `same` /
  SK-08 `9 4 0` → `0 0 1` / SK-09 (a) 9 → 0 · (b) 새 0 옛 1 → 새 1 옛 0 · (c) 여덟 0 → 1 · (d) `1 1 1 1 1` / SK-10 (a) 9 → 0 · (b)(c) 0 → 1 · (d) 1 /
  AR-01 `22 0 0 0 0 0 0 6` → `22 1 1 1 1 1 1 7` / AR-02 `0 0 0` → `0 14 1` / AP-01 `V=0.8.0` 0 · AP-03 더한 줄 펜스 0 · AP-04 0 · RE-02 `1 0` / DG-02 스물두 줄 전부 `new_warnings=0` · `LINT_NOT_RUN` 0
- 커밋을 재는 측정: 초안 예행 복제본 `p5draft/rh` 에 `cd` 줄만 바꾼 공통 정의로 돌림 — AR-03 ① 0 · ② `0 23` · ③ `0 SEAL_OK` · ER-01 notes 있음 · 일곱 `1 1 2 1 1 1 1` · 열둘 1 ·
  같은 줄 `1 1 1` · 셋째 0 · 넷째 0 · SC-00 0 · DG-01 · DG-03 0 · DG-04 0 · RE-01 0. 계약 표와 같다
- 모의본 트리에서: `validate-plugin.py flutter-toolkit` `V1`~`V10` 전부 OK · `run-evals.py flutter-toolkit` `Total: 22 passed, 0 failed` 종료 0 ·
  `sync-docs.py --check-only` 0 · `sync-evals.py --check-only` 0 · `format-edited-dart-test.sh` `결과: 12 경우 중 불일치 0`
- Step 6.2 두 명령 `26` · `16`. Step 6.5 헤더 열둘 모두 허용 안(`회귀 게이트` 는 서술 절 이름) · 조건 26 줄 전부 조건 절 안 · `OK conditions=26` · `OK 미실측 0 건`.
  측정 커버리지 검출기 `UNCOVERED` 넷(SK-01 · SK-09 · SK-10 · ER-01) — 넷 다 범위 경계에 해소 기록이 있다
- 옛 수가 남은 곳을 찾았다(`여덟 문장` · `스물하나` · `열넷` · `61 치환` 등). `mock-v1.py`(61 치환) 한 줄뿐이고, 반영 전 판을 가리키는 설명이라 맞다

### 3. 봉인 전에 넣으면 좋은 것 (막지 않는다)

#### D1 — ER-01 짧은 키에 조사를 붙여 쓰면 0 이다

범위 경계 202 줄 「(ER-01 이 글자 그대로 센다)」 는 이제 반만 맞다. 짧은 키 일곱은 낱말 경계로, 세 낱말은 사유와 한 줄로 센다.
`LC_ALL=C.UTF-8` 에서는 한글이 `[:alnum:]` 에 들어가서, `F06은` 처럼 조사를 바로 붙이면 키가 있어도 0 이 나온다.

검토 실측(2026-09-25): 계약 정규식에 한 줄씩 대면 `F06은 반영` 0 · `` `F06` 은 반영`` 1 · `F06 · 반영` 1 · `(F06)` 1.
초안 가짜 notes 에서 `F06 ·` · `F25 —` 를 `F06은` · `F25는` 으로 바꾼 사본 → 일곱 값 `1 0 2 1 0 1 1`.
맞는 notes 를 FAIL 로 보는 쪽이고 `BUILD` 가 notes 커밋 뒤 ER-01 을 직접 재므로 막지 않는다.

고칠 문구 — 202 줄 괄호를 이렇게 바꾼다:
「(ER-01 이 센다 — 짧은 키 일곱 `F02` · `F06` · `F22` · `F24` · `F25` · `F31` · `user-setup:P1` 은 낱말 경계로 세므로 백틱으로 감싸거나 뒤를 띄어 쓴다. `F06은` 처럼 조사를 바로 붙이면 0 이다)」

#### D2 — l10n 이 블록으로 돌리는지는 재지 않는다

배경 F06 행과 조사 기록 초안은 l10n 을 「킷이 codegen 을 직접 돌리며 전후 삭제 수를 매번 세는 다섯 자리」 에 넣는다. 그런데 SK-01 (b) 의 l10n 값은
「필터를 붙이지 않는다」 문장만 잰다. 모의본에는 두 문장(표 칸 「— `flutter-run` codegen 절의 블록으로 돌린다」 · 끝 문장 「전체를 돌리고 전후 삭제 수를 센다.」)이 있어
`mock.py` 대로 적용하면 문제가 없다. 다만 그 둘이 빠져도 지금 측정은 통과한다.

검토 실측: 모의본 l10n 에서 두 문장만 뺀 사본 → 지금 SK-01 (b) l10n 값 그대로 `1`. 아래 측정은 시작 커밋 판 `0 0` · 모의본 `1 1` · 뺀 사본 `0 0`.

고칠 문구 — SK-01 (b) 의 l10n 측정을
``toks "$(sect "$L10N" '### 6. Codegen 실행')" 'Slang 도 `--build-filter` 로 i18n 폴더만 돌리지 않는다' '`flutter-run` codegen 절의 블록으로 돌린다' '전체를 돌리고 전후 삭제 수를 센다'``
로 넓힌다(아홉 → 열한 값). SK-01 산문의 「아홉 문장」 과 「transition §5 도」 앞에 「l10n Slang 줄과」 를 같이 고친다.

#### D3 — SK-01 (a) 가 따옴표 없는 필터를 못 본다

검토 실측: 모의본 `flutter-widget/SKILL.md` 끝에 `$DART run build_runner build --build-filter lib/features/**` 한 줄을 더한 사본 → 지금 (a) 첫 값 `0`.
넓힌 정규식 ``grep -rnE -- '--build-filter(=|[[:space:]]+["'"'"'A-Za-z0-9_$/.*{])' "$E/$FT" | grep -c .`` → 시작 커밋 판 `6` · 모의본 `0` · 따옴표 없는 한 줄 더한 사본 `1`.
문자 목록을 영문으로 적는 까닭: `[:alnum:]` 로 쓰면 `C.UTF-8` 에서 한글이 들어가 evals 사례 1 단언의 「`--build-filter 를`」 이 걸린다(검토 실측: 모의본 `1`).

#### D4 — 측정이 기대는 제목 목록에 빠진 제목

범위 경계 「측정이 기대는 제목은 이름을 바꾸지 않는다」 목록에 이번에 새로 기대게 된 flutter-transition `### 5. Codegen` 이 없다.
1 회차부터 flutter-transition `## Gotchas` · `## Rules`, flutter-hooks `## Gotchas`, flutter-responsive `## Rules`, flutter-test `## Gotchas` 도 목록에 없었다(1 회차에서 못 봤다).
이름이 바뀌면 `sect` 가 빈 글을 내 값이 0 이 되므로 FAIL 쪽으로 틀린다. 목록에 더하기만 하면 된다.

D2 · D3 을 넣으면 `BUILD` 는 바뀐 값의 시작 커밋 판 · 모의본 값과 문장 삭제 대조를 다시 재서 봉인 전 실측 표에 적는다. 조건 줄 수(26)와 기능 조건 수(16)는 그대로다.

VERDICT: APPROVE
