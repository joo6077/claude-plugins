# Phase 4 계약 초안 검토 — kaizen-0924-p04-harness

- 대상: `.harness/sprint-contract-kaizen-0924-p04-harness.md` (봉인 전 초안, 조건 28 줄 · 기능 조건 18, 파일 내용 지문 sha256 `179afddf…`)
- 역할: 카이젠 2026-09-24 Phase 4 REVIEW (사용자 승인 5 단계를 대신하는 독립 검토자)
- 검토 시각: 2026-09-25 03:37 (`date '+%Y-%m-%d %H:%M'` 출력) · 작업 폴더 `HEAD`(지금 가지의 마지막 커밋) = `3a51b73` (계약의 시작 커밋과 같다)
- 레포 파일은 이 파일 하나만 썼다. 임시 사본과 시험 스크립트는
  `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p4r/` 에 있다.
  검토 전후로 작업 폴더 `git status --short` 가 같다 (시험용 git 저장소는 전부 임시 폴더에 따로 만들었다)

## 결론

고쳐서 다시 내야 한다(CHANGES). 뼈대는 튼튼하다. 계약에서 기계로 떼어 낸 도우미 열하나가 초안 작성자의 `p4d/k/` 와 글자까지
같았고, 그것으로 시작 커밋 판과 모의본(`p4d/mock.py` 를 시작 커밋 판에 새로 적용한 사본)에 다시 돌린 값이 계약의 봉인 전 실측 표와
전부 같았다. 처리 배정표 Phase 4 열 행은 전부 조건이나 미반영 사유로 다뤄졌고, 고치는 열네 파일은 러닝북 Phase 4 범위 안이다.

막는 이유는 넷이다.

1. **ER-01 — 새 훅이 희소 체크아웃에서 멀쩡한 커밋을 막는다.** 희소 체크아웃(작업 폴더에 일부 폴더만 꺼내 두는 git 기능)에서
   꺼내지 않은 파일은 작업 폴더에 없지만 git 은 경로 커밋에 그 파일을 삭제로 싣지 않는다(목록에 skip-worktree 표시가 있어 건너뛴다).
   새 `check_path_commit` 은 `HEAD` 를 새로 읽은 임시 목록에서 세므로 그 표시가 없어 전부 삭제로 센다. 실측(아래 「다시 돌려 본 것」 6):
   `git commit -o -m x -- .` 와 `-- d1 keep` 둘 다 `hook_rc=2 git_dels=0`. 조건 문장 「커밋이 실제로 실을 삭제를 세어」가 여기서
   거짓이고, `align.sh` 에 이 경우가 없어 통과한다. 훅의 설계 원칙(`commit-guard.sh:6-7` — 죽어서 정상 커밋을 막는 것이 없는 것보다
   나쁘다)과도 반대다. 고칠 수 있음은 확인했다 — 센 이름에서 공용 목록의 `S` 로 시작하는 줄을 빼는 세 줄을 더한 사본이 희소 두 경우 `hook_rc=0`,
   `align.sh` 열 줄 전부 `agree`, 시험 파일 bash · `/bin/bash` 둘 다 `실패 0 건`
2. **ER-05 · 배경 표 — 앞 Phase 가 「Phase 4 · 12 몫」 으로 넘긴 `project_name` 결함을 계약이 다루지 않는다.** 처리 배정표
   `harness:P02` 비고는 「reflect-collector:P5 가 같은 파일의 프로젝트 이름 계산을 바꾸므로 함께 시험한다」, `reflect-collector:P5`
   비고는 「harness/scripts/save-feedback.sh 도 같이 바뀐다」 다. phase1 · phase2 · phase3 notes 가 셋 다 저장본의 `project_name` 이
   워크트리 이름 `kaizen-0924` 로 적혔다고 적었다. Phase 12 범위는 `reflect-kit/` 뿐이라 이 하네스 파일을 고칠 수 있는 Phase 는 이번
   사이클에 Phase 4 하나다. 그런데 배경 표 · GAP · 넘김 열두 문자열 어디에도 없다. 같은 절에서 근거 파일 §3 이 짚은
   `create-agent/SKILL.md:25` (「`model` 을 생략하면 `inherit`」) · `create-skill/SKILL.md:27` (「다른 플랫폼에서는 무시된다」) 도
   이 Phase 파일인데 말이 없다 — 이 둘은 기준 원본이 Phase 1 가이드라 두는 것이 맞지만, 그 이유와 넘김을 적어야 한다
3. **러닝북 계약 규칙 두 개를 안 지켰다 — 함수 정의 확인 · 건드리면 안 되는 파일의 직접 세기.** 공통 정의의 셸 함수(`my` ·
   `added` · `url` · `unsigned_on`)에 기대면서 0 을 기대하는 측정이 아홉 곳(SC-00 · DG-01 · DG-03 · DG-04 · ER-03 · ER-04 · AP-01 ·
   ER-05 셋째 · AR-05 ①)인데 `type <함수> >/dev/null || exit 2` 가 하나도 없다.
   공통 정의 없이 돌리면 `my | grep -c …` · `added | grep -cE …` 가 `command not found` 뒤 `0` 을 낸다(실측 7). 그리고 ER-05 셋째
   측정 · AR-05 ② 는 서명 줄 커밋 목록(`my`)으로만 잰다. 서명을 빠뜨린 이 Phase 커밋이 루트 `README.md` 나 `harness/hooks/hooks.json`
   을 건드려도 둘 다 0 이다(실측 8 — 예행 사본에 서명 없는 커밋 둘을 얹었다)
4. **ER-03 — 열네 파일을 합쳐서 옛판과 비교한다.** 러닝북 규칙 「여러 파일을 합쳐서 옛판과 비교하지 말고 파일마다 비교한다」 위반이다.
   실측 5: 합친 비교는 새 URL 넷만 보고 `create-skill/SKILL.md` 에 새로 생긴 `https://code.claude.com/docs/en/skills` 를 못 본다
   (다른 파일에 이미 있어서). 파일마다 비교해도 값은 0 이라 바꾸는 비용이 없다

## 지시한 여섯 가지에 대한 답

| 볼 것 | 판단 |
| --- | --- |
| 조건마다 FAIL 상태를 한 문장으로 | 28 조건 모두 된다. 예: SK-01 「`### Step 5: Commit` 구간에서 여덟 토큰 가운데 하나라도 1 건이 아니거나, `ka-commit.sh` 두 줄이 요구값과 다르면 FAIL」 · ER-01 「시험 끝 줄이 `실패 0 건` 이 아니거나 `align.sh` 에 `DISAGREE` 가 한 줄이라도 있으면 FAIL」 · AR-05 「서명 없는 커밋이 열네 파일을 건드렸거나 이 계약이 `SEAL_OK` 가 아니면 FAIL」. N/A 줄(해당 없음) 넷은 각각 재는 명령이 붙어 있다 |
| 측정이 의도를 재는가 · 대조 · 봉인 전 실측 | 대체로 그렇다. 값을 잠그는 조건은 편집 전 값, 0 기대 조건(ER-03 · ER-04 · AP-01 · AP-03 · DG-02)은 양성 대조, 시험 통과 조건(ER-01 · ER-02 · AR-02)은 음성 대조(시작 커밋 판 · 변이)와 git 이 낸 알려진 답이 붙어 있다. 문장 삭제 사본 45 개도 있다. 빈 곳은 막는 이유 1(알려진 답 대조에 희소 체크아웃이 없다) · 3(함수 정의 확인 · 직접 세기) · 4(합친 비교)와 SC-00 · DG-01 · DG-04 의 양성 대조 기록이 없는 것이다 |
| 처리 배정표 Phase 4 행 | 열 행 전부 — `harness:P02` · `F14`(ER-02) · `harness:P07` · `F08`(SK-01 ~ SK-03) · `user-setup:P2`(SK-01 · SK-02, 폐기 결정 줄은 `F20` 으로 넘김) · `F09`(SK-03, Phase 8 · 9 · 5 · 10 넘김) · `F28`(SK-02 · ER-01 · AR-03, 상태 스크립트 미반영) · `F18` · `other-kits:P10`(AR-01, YAML 검사는 안 더하는 선택과 근거) · `insights:scope-commit-block`(AR-03). 빈 곳 둘 — `harness:P02` 비고의 「reflect-collector:P5 와 함께 시험」(막는 이유 2)과 `F28` 비고의 「시뮬레이터 · 데이터베이스 나누기」 미반영 사유. 러닝북 추가 과제 (1) · (2) · 범위 선언 자리는 ER-01 · AR-04 · AR-02 · AR-03 이 받는다. Phase 1 넘김 셋 · Phase 2 넘김 넷 · Phase 3 넘김(`assertions.json 실행기` · 초안 고정 이름)은 조건이나 넘김으로 맞는다 |
| 범위가 러닝북 표 안인가 | 그렇다. 열네 파일이 전부 「`harness/` 나머지 · `scripts/` 의 카이젠 수집기 · 검사기」 안이다. harness-kaizen 이 고치지 말라는 목록(sprint-contract · qa-evaluator · 설계 가이드 넷 · `contract-schema.md` · `feedback-schema.yaml`)은 넘김으로 돌렸다. `commit-guard-test.sh` 는 러닝북 Phase 4 과제가 직접 지목했다 |
| 공유 파일을 건드리려 하는가 | 건드리려 하지 않는다. ER-05 셋째 측정 · SC-00 이 재지만 서명 줄 목록으로만 재서 서명 빠진 커밋을 못 본다(막는 이유 3) |
| 조건끼리 부딪히는가 | 안 부딪힌다. AP-01 ↔ AR-01 (d)(검증 가이드 버전 값만 빼기), ER-04 ↔ SK-05(`agents 에 대해` 0), AR-05 ② ↔ ER-05(notes 는 `.harness/` 안), RE-02 ↔ ER-01(더한 함수 하나), DG-05 Given ↔ AR-05(작업 트리가 `$END` 와 같을 때만) 모두 확인했다. 아래 고칠 문구를 넣어도 새로 부딪히는 곳은 없다 — 희소 체크아웃 고침은 함수를 더하지 않고 `block` · `top_dirs` 두 줄도 그대로라 RE-02 값이 그대로다 |

## 다시 돌려 본 것

모두 임시 폴더에서 돌렸다. `B` = `git archive 3a51b73`, `E` = 같은 사본에 `p4d/mock.py` 를 새로 적용한 판(`mock applied` 출력 확인).
도우미는 계약 `회귀 게이트` 절(측정 공통 정의와 봉인 전 실측을 적은 절)의 코드 블록을 파이썬으로 떼어 저장했다 — 열둘 가운데 이름 붙은
열하나가 `p4d/k/` 와 `cmp` 로 전부 같았다.

1. **Step 6.2 · 6.5** — 조건 줄 28 · 기능 조건 18 · `OK conditions=28` · `OK 미실측 0 건`. 헤더 여덟은 허용 목록(서술 다섯은 접두 일치)
2. **ER-01** — `E` 에서 시험 bash · `/bin/bash` 둘 다 `rc=0` · 끝 줄 `실패 0 건` · 새 PASS 9. 시작 커밋 판 훅 `⑰ ⑰-확인 ⑱ ㉒ ㉓ ㉔` ·
   `mutants ok` · 공용 목록 변이 `⑳` · 개인 목록 변이 `⑳ ㉑` (셋 다 끝 공백 포함 — 계약 요구값과 같다). `align.sh` 새 판 열 줄 `agree` · `git_dels` `60 51 50 0 0 55 59 60 0 0` (끝 공백 포함),
   시작 커밋 판은 ⑰ ⑱ ㉒ ㉓ ㉔ 가 `DISAGREE`
3. **SK-01 (b) · SK-03 (b)** — `ka-commit.sh`: `committed=[M mine.txt A new.txt]` · `still_staged=[D other.txt M shared.txt]`.
   `ka-split.sh` bash · `RUNNER=zsh` 둘 다 네 줄 요구값 · `worktrees=1`. 시작 커밋 판 둘 다 `NO_BLOCK` · 종료 코드 2
4. **ER-02** — (a) `1 1 1` · 남은 파일 0 (b) `rc=1` · 1 (c) 여섯 줄 python · yq 쌍이 같은 문구, 뽑은 세 줄 요구값 · `saved_under_home=0`
   (d) `project_name 1 project_hash 1 rc=1 1 1 saved_under_home=0`. (d) 가 살아 있는지 따로 봤다 — `FINAL_FIELDS` 를 초안 여섯으로 줄인
   변이는 `rc=0 0 0 saved_under_home=1` 로 떨어진다
5. **ER-03** — 합친 비교 0 (계약 그대로). 파일마다 비교하면 새 (파일, URL) 쌍이 다섯 — `sprint/SKILL.md` 넷 ·
   `create-skill/SKILL.md` 의 `https://code.claude.com/docs/en/skills` — 이고 근거 파일에 없는 것 0
6. **ER-01 희소 체크아웃 (새로 짠 경우)** — 60 파일 `d1` · `keep/a.txt` 저장소에서 `git sparse-checkout set --cone keep`
   (작업 폴더 `d1` 파일 0 · `ls-files -t` 의 `S` 60), `keep/a.txt` 수정 뒤:

   ```text
   s1 git commit -o -m x -- .        hook_rc=2 git_dels=0  커밋 안전 훅: 삭제 60 개가 실린 커밋을 막았다 (… 지정한 경로 안에서 작업 폴더에 없는 추적 파일).
   s2 git commit -o -m x -- d1 keep  hook_rc=2 git_dels=0  (같은 문구)
   git 실제 커밋: [main …] x  1 file changed, 1 insertion(+)
   ```

   공용 목록의 `git ls-files --deleted` 는 같은 저장소에서 0 이다 — `-i` · `-a` 갈래는 이 문제가 없다. 고친 사본(`p4r/sparse-fix.py`,
   `rm -rf "$t"` 뒤에 아래 세 줄) — 희소 두 경우 `hook_rc=0 git_dels=0`, `align.sh` 열 줄 `agree`, 시험 bash · `/bin/bash` `실패 0 건`:

   ```bash
   # 희소 체크아웃의 skip-worktree 항목은 작업 폴더에 없어도 git 이 싣지 않는다
   names=$(comm -23 <(printf '%s\n' "$names" | grep . | sort) \
     <(g -c core.quotePath=false ls-files -t --full-name -- "${c_pathv[@]}" 2>/dev/null | sed -n 's/^S //p' | sort))
   ```

7. **함수 정의 없는 셸** — `bash -c 'my | grep -cE "^(scripts/release\.sh)$"'` → `my: command not found` 뒤 `0`.
   `bash -c 'added | grep -cE "에 대해"'` → `added: command not found` 뒤 `0`. 둘 다 조건이 PASS 로 읽는 값이다
8. **서명 빠진 커밋 (예행 사본 `p4d/rh` 를 `p4r/rh3` 로 복제)** — 제안 측정 두 개가 예행 그대로에서 `AR-05① wide=0 · ER-05 direct=0`.
   서명 없이 `harness/hooks/hooks.json` 을 고친 커밋을 얹고 `end_sha` 를 옮기면 `wide=1`, 이어 서명 없이 루트 `README.md` 를 고친
   커밋을 얹으면 `direct=1`. 같은 상태에서 계약의 서명 줄 목록 측정은 `0` (둘 다 못 본다)
9. **AR-01 · AR-02 · 문서 문장 조건** — AR-01 (a) 시작 커밋 판 다른 킷 10 · 모의본 0 · references 킷 10 · FAIL 0 (b) 모의본
   `FAIL api-kit/skills/api-verify/references/zz-broken-table.md:9 …` · `rc=2`, 시작 커밋 판 `9 md files — OK` · `rc=0` (c) 0.
   AR-02 (a) `1 1 1` (b) `31 통과 · 0 실패` · 2 (c) 2 (d) `as_is rc=0` · `anchor 1` · `renamed rc=1 1`. SK-02 `1 1 1 1 1` ·
   SK-06 (a) `1 1 1` (b) `12 12 0` · AR-03 `1 1 1 1 1` · 블록 두 경로 · AR-04 `0 1 1 1` · `pfile rc=0`. 문장 삭제 한 개를 따로
   돌렸다 — SK-02 의 `git worktree add -b …` 줄을 지운 사본에서 그 토큰 1 → 0

## 고칠 문구 (조건 ID 별)

고친 뒤 새 측정과 바뀐 값은 봉인 전에 다시 잰다(러닝북 「봉인 전 실측」). 예행 값(`스물두 문자열` · `agree 10` · 새 PASS 9 등)도 다시 돌린 값으로 바꾼다.

### ER-01 (막는 이유 1)

- 산문 「경로 밖 삭제 · 목록에서만 뺀 파일 · 빈 개인 목록은 세지 않는다」 →
  「경로 밖 삭제 · 목록에서만 뺀 파일 · 빈 개인 목록 · 희소 체크아웃에서 꺼내지 않은 파일(skip-worktree)은 세지 않는다」
- (a) 새 경우를 열로 — `PASS` 와 공백으로 시작하는 새 경우 줄이 10 개(⑰ · ⑰-확인 · ⑱ · ⑲ · ⑳ · ㉑ · ㉒ · ㉓ · ㉔ · ㉕).
  측정 `grep -cE '^PASS (⑰|⑰-확인|⑱|⑲|⑳|㉑|㉒|㉓|㉔|㉕) ' "$T/cg5.txt"` 10.
  ㉕ = `d1` 60 파일 저장소에 `keep/` 을 더해 커밋하고 `git sparse-checkout set --cone keep` 뒤 `keep/` 파일 하나를 고쳐
  `git commit -o -m x -- .` 가 통과(0)
- (b) 음성 대조 넷째 — `mut.py` 가 희소 체크아웃 빼기 줄을 지운 셋째 변이(`mut-nosparse.sh`)를 더 만들고, 그 변이로 돌린 FAIL 번호가
  정확히 `㉕`. 시작 커밋 판 훅은 경로 커밋을 통째로 건너뛰어 ㉕ 를 통과하므로 FAIL 번호가 그대로 `⑰ ⑰-확인 ⑱ ㉒ ㉓ ㉔` 인지,
  공용 · 개인 목록 두 변이가 그대로 `⑳` · `⑳ ㉑` 인지 다시 잰다
- (c) `align.sh` 에 ㉕ 한 줄을 ㉔ 뒤에 더해 열한 줄 전부 `agree` 이고 `git_dels` 가 차례로 `60 51 50 0 0 55 59 60 0 0 0` (끝 공백 포함)
  (㉕ · ⑬ · ⑭ 가 모두 0 이라 ⑬ 앞에 두든 끝에 두든 값이 같다). 측정의 `grep -c ' agree$'` 기대값 10 → 11
- 개선안 초안 · `mock.py` 의 `check_path_commit` 에 위 「다시 돌려 본 것」 6 의 세 줄(또는 같은 일을 하는 줄)을 넣는다.
  README 경로 커밋 문단에 「희소 체크아웃에서 꺼내지 않은 파일은 세지 않는다」 한 문장을 더하면 좋다(조건으로 잠그지는 않아도 된다)

### ER-05 (막는 이유 2 · 3)

- 배경 표에 행을 더한다:
  `| reflect-collector:P5 (harness:P02 비고 「함께 시험한다」) · phase1~3 notes | save-feedback.sh 의 프로젝트 이름 계산이 워크트리 폴더 이름을 적는다 (세 notes 실측: kaizen-0924) | 미반영 — 식별 규칙과 그 출처는 phase12.md 에만 있고 이 Phase 근거 파일 phase4.md 에는 없다. Phase 12 범위는 reflect-kit/ 라 이 하네스 파일을 고치지 못한다 — 다음 사이클 Phase 4 로 넘긴다 (ER-05) |`
  (BUILD 가 대신 이번에 고치기로 하면 조건 하나 · 음성 대조가 따로 있어야 하고 근거는 phase4.md 밖이라 러닝북 입력 규칙과 부딪힌다 — 넘김이 맞다)
- 배경 표 `F28` 행 「이번 처리」 에 덧붙인다: 「시뮬레이터 · 데이터베이스 나누기는 미반영 — 맡은 제안이 없고 근거 파일 §2 F28 도 다루지 않는다」
- GAP 분석 「구현 후보가 둘 이상이었던 곳의 선택」 에 불릿 하나: 「create-agent `:25` · `:33` 의 `model` 을 생략하면 `inherit` 와
  create-skill `:27` 의 「공식 필수는 `name` 과 `description`」 · 「다른 플랫폼에서는 무시된다」 는 근거 파일 §3 이 낡았다고 짚었지만
  고치지 않는다 — 두 스킬이 기준 원본으로 가리키는 `agent-design-guide.md:79` · `skill-design-guide.md` §frontmatter 규칙이 Phase 1 파일이고
  Phase 1 notes 가 다음 사이클로 넘겼다. 스킬 쪽만 고치면 스킬과 가이드가 갈린다」
- 넘김 문자열을 스물다섯으로 — 기존 스물둘에 `reflect-collector:P5` · `create-agent/SKILL.md:25` · `create-skill/SKILL.md:27` 셋을 더한다.
  조건 산문 「스물두 문자열」 → 「스물다섯 문자열」, 괄호 안 넘김 목록 「넘김 열둘」 → 「넘김 열다섯」 에 세 문자열을 더하고,
  측정 `for t in …` 목록 끝에 `'reflect-collector:P5' 'create-agent/SKILL.md:25' 'create-skill/SKILL.md:27'` 을 붙여 「25 값 전부 1 이상」.
  `## 범위 경계` 넘김 불릿의 「열두 문자열」 → 「열다섯 문자열」 과 세 문자열의 설명(각각 「다음 사이클 Phase 4 — 위 배경 행」 ·
  「다음 사이클 Phase 1 · 4 — `agent-design-guide.md:79` 와 함께」 · 「다음 사이클 Phase 1 · 4 — skill 가이드 frontmatter 규칙과 함께」)을 더한다
- 셋째 측정 앞에 `type my >/dev/null || exit 2;` 를 붙이고, 서명 줄 목록 측정 뒤에 직접 세기를 더한다 —
  `git log "$B..$END" --oneline -- harness/skills/sprint-contract harness/agents/qa-evaluator.md harness/docs/guides/skill-design-guide.md harness/docs/guides/agent-design-guide.md harness/docs/guides/contract-design-guide.md harness/docs/guides/qa-evaluation-guide.md harness/references .claude-plugin README.md CLAUDE.md .github .claude .harness/.meta/orchestrator-audit-log.md .harness/.meta/kaizen-failure-count.yaml | wc -l` 0.
  `docs/` 와 킷별 `plugin.json` 은 다른 Phase 가 제 킷 폴더를 고치므로 직접 세기에서 빼고 서명 줄 목록으로만 잰다는 말을 붙인다.
  봉인 전 실측: 예행 사본 0 · 서명 없이 루트 `README.md` 를 고친 커밋을 얹은 사본 1 (「다시 돌려 본 것」 8)

### AR-05 (막는 이유 3)

- ① 을 `type unsigned_on >/dev/null || exit 2;` 뒤 `unsigned_on "$B" "$END" "$SIG" harness scripts | grep -c .` 0 으로 바꾼다
  (열네 파일 → `harness/` · `scripts/` 전체). 산문 괄호 「열네 파일을 건드린 구간 안 커밋이 전부 서명했다」 →
  「`harness/` · `scripts/` 를 건드린 구간 안 커밋이 전부 서명했다 — 이 구간에 두 폴더를 고칠 수 있는 Phase 는 4 하나다」.
  봉인 전 실측: 예행 사본 0 · 서명 없이 `harness/hooks/hooks.json` 을 고친 커밋을 얹은 사본 1 — 지금 ①(열네 파일)과 ②(서명 줄 목록)는 그 사본에서 둘 다 0 이다

### ER-03 (막는 이유 4)

- 측정을 파일마다 비교로 바꾼다:
  `type url >/dev/null || exit 2;` 뒤
  `for f in "${FILES[@]}"; do comm -13 <(url < "$T/B/$f") <(url < "$T/E/$f"); done | sort -u | comm -23 - <(url < "$EVID") | grep -c .` 0.
  봉인 전 실측 문장 「모의본 새 URL 넷 …」 → 「모의본 파일마다 새 URL 다섯 쌍(`sprint/SKILL.md` 넷 · `create-skill/SKILL.md` 의
  `code.claude.com/docs/en/skills`) 전부 근거 파일에 있어 0」. 양성 대조 문장은 그대로 둔다(파일마다 비교로 다시 잰다)

### SC-00 · DG-01 · DG-03 · DG-04 · ER-04 · AP-01 (막는 이유 3)

- SC-00 · DG-01 · DG-03 · DG-04 측정 앞에 `type my >/dev/null || exit 2;` 를 붙인다
- ER-04 · AP-01 측정 앞에 `type added >/dev/null || exit 2;` 를 붙인다
- SC-00 · DG-01 · DG-04 는 0 을 기대하는데 양성 대조 기록이 없다. 각각 한 줄을 적는다 — 예: SC-00
  「양성 대조: `printf 'scripts/release.sh\n' | grep -cE '^(scripts/release\.sh|…)$'` 1」, DG-04 「`printf 'x/y.dart\n' | grep -cE '\.(dart|…)$'` 1」

## 막지 않는 것 (넣으면 좋다)

1. SK-01 불릿 「`git add -A` · `git add .` · `git commit -a` 를 쓰지 않는다」 — 근거 파일 §4 둘째 항은 `git commit -i` 도 금지 목록에
   넣었다. `-i` 는 공용 목록 전체를 싣는다. 넣으면 SK-01 (a) 토큰과 문장 삭제 대조를 같이 고친다
2. `check_path_commit` 은 경로 커밋마다 `HEAD` 전체를 임시 목록으로 읽는다. 파일이 수십만 개인 저장소면 커밋마다 느려질 수 있다.
   지금 조건에는 영향이 없다 — 다음 사이클 메모로 충분하다
3. `save-test.sh` 의 새 경우 ⑧ ⑨ 가 `/tmp/test-…` 고정 이름을 쓴다(기존 경우도 같은 방식). 두 벌을 동시에 돌리면 서로 덮는다.
   ER-02 (a) · (b) 는 차례로 돌리니 지금은 문제없다

VERDICT: CHANGES

## 2 회차

- 대상: 같은 계약 초안 (봉인 전, 조건 28 줄 · 기능 조건 18, 파일 sha256 `a1c23aa6…`, 파일 수정 시각 04:01)
- 검토 시각: 2026-09-25 04:13 (`date '+%Y-%m-%d %H:%M'` 출력) · `HEAD`(지금 가지의 마지막 커밋) = `3a51b73` 그대로
- 레포 파일은 이 파일 하나만 썼다(끝에 이 절을 덧붙였다). 임시 사본과 시험 스크립트는
  `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p4r2/` 에 있다.
  시험용 git 저장소는 전부 그 폴더 안에 따로 만들었다

### 결론

통과(APPROVE). 1 회차가 막은 이유 넷과 조건별 고칠 문구 여섯 묶음이 전부 계약에 들어갔다. 1 회차 뒤 모의본에서 바뀐 파일은
넷(`commit-guard.sh` · `commit-guard-test.sh` · `sprint/SKILL.md` · `harness/README.md`)인데, 그 넷에 걸린 측정을 새로 푼 사본에서
계약 문구 그대로 다시 돌렸고 값이 계약의 봉인 전 실측과 전부 같았다. 새로 막을 결함은 찾지 못했다.

사본 만드는 법: `B` = `git archive 3a51b73`, `E` = 같은 사본에 `p4d/mock.py` 를 새로 적용한 판(`mock applied` 출력). 측정 공통 정의 블록은
계약에서 줄 단위로 떼어 `END` 해석과 `git archive` 두 줄만 이 두 사본을 쓰게 바꿨다(`p4r2/common.sh`, `bash -n` 통과).
도우미 열하나도 계약에서 다시 떼어 `p4d/k/` 와 `cmp` 로 비교했다 — 전부 같다.

### 1 회차 고칠 문구가 들어갔는지

| 1 회차 요구 | 계약 자리 | 다시 돌린 값 |
| --- | --- | --- |
| ER-01 산문에 희소 체크아웃 | 721 줄 「… 빈 개인 목록 · 희소 체크아웃에서 꺼내지 않은 파일(skip-worktree)은 세지 않는다」 | — |
| ER-01 (a) 새 경우 10 줄 | 722 줄 | bash · `/bin/bash` 둘 다 `rc=0` · 끝 줄 `실패 0 건` · 새 `PASS` 10 · 10 |
| ER-01 (b) 셋째 변이 | 723 줄 · `mut.py` 블록 | `mutants ok` · 시작 커밋 판 `⑰ ⑰-확인 ⑱ ㉒ ㉓ ㉔ ` · 공용 목록 `⑳ ` · 개인 목록 `⑳ ㉑ ` · 희소 빼기 줄 없앤 판 `㉕ ` (끝 공백 포함) |
| (1 회차에 없던 것) ㉕ 전제 대조 | 724 줄 | 시험에서 `sparse-checkout set` 한 곳만 지운 사본 — 차이 1 줄 · `FAIL ㉕ 기대 희소 체크아웃 전제 — 작업 폴더에 d1 없음 · S 60 개 / 실제 d1/f001 있음 · S 0 개` 1 줄. 희소 체크아웃이 안 걸리면 훅을 안 고쳐도 통과하는 구멍을 시험 스스로 막는다 |
| ER-01 (c) `align.sh` 열한 줄 | 725 줄 · `align.sh` 블록 ㉕ 줄 | `agree` 11 · `git_dels` `60 51 50 0 0 55 59 60 0 0 0 ` · 시작 커밋 판은 ⑰ ⑱ ㉒ ㉓ ㉔ 다섯 줄 `DISAGREE`(㉕ 는 agree) · 희소 빼기 줄 없앤 판은 `㉕ hook_rc=2 git_dels=0 DISAGREE` 한 줄 |
| 개선안 초안 · `mock.py` 세 줄 | 170 줄 · `mock.py` | 들어갔다. 1 회차 제안의 `-c core.quotePath=false` 는 빠졌지만 도우미 `g` 가 이미 붙인다(시작 커밋 판 `commit-guard.sh:95-100`) — 한글 이름도 두 목록이 같은 꼴로 나온다 |
| README 희소 체크아웃 문장 | AR-04 다섯째 토큰으로 잠갔다 | 모의본 1 · 그 문장만 지운 사본 0 |
| ER-05 배경 행 · `F28` 행 · GAP 불릿 | 31 줄 · 23 줄 · 146-149 줄 | 배경 행의 사실을 따로 확인 — 세 notes 가 모두 `kaizen-0924` 를 적었다(phase1 98 줄 · phase2 81 줄 · phase3 108 줄), `phase4.md` 에는 프로젝트 이름 규칙이 없고 `phase12.md` 83-102 줄에 있다 |
| ER-05 넘김 스물다섯 | 209-219 줄 · 739 줄 · 측정 25 인자 | 문자열끼리 서로 안에 들어가는 것이 없다(`F20` 은 다른 키에 없다) |
| ER-05 셋째 함수 확인 · 넷째 직접 세기 | 742-744 줄 | 아래 「git 기록 측정」 |
| AR-05 ① `harness` · `scripts` 전체 | 772 줄 | 아래 「git 기록 측정」 |
| ER-03 파일마다 비교 | 734 줄 | 0. 새 (파일, URL) 쌍 다섯이 계약에 적힌 것과 같다(`sprint/SKILL.md` 넷 · `create-skill/SKILL.md` 의 `code.claude.com/docs/en/skills`). 양성 대조 — 근거 파일에 없고 `sprint/SKILL.md` 에만 있던 `https://arxiv.org/abs/2606.27416` 을 create-agent 끝에 더한 사본에서 파일마다 비교 1 · 합친 비교 0 |
| 함수 확인 줄 · 양성 대조 | SC-00 · DG-01 · DG-03 · DG-04 · ER-03 · ER-04 · AP-01 · ER-05 셋째 · AR-05 ①②③ · DG-06 | 전부 `type <함수> >/dev/null \|\| exit 2` 가 있다. SC-00 · DG-01 · DG-04 양성 대조 줄도 있고 적힌 입력으로 세면 3 · 1 · 2 가 맞다 |
| (막지 않는 것 1) `git commit -i` | SK-01 넷째 토큰 · 177 줄 | 모의본 1 · 그 불릿만 지운 사본 0 · `ka-commit.sh` 두 줄 그대로 |
| (막지 않는 것 2) 속도 | 133 줄 | 다음 사이클 메모로 남긴다고 적었다 |

1 회차 표의 GAP 고칠 문구에 내가 create-agent `:25` · `:33` 이라고 적었는데 `:33` 은 틀렸다 — `:33` 은 Unverifiable 4 항 줄이고 「`model` 을 생략하면
`inherit`」 는 `:25` 와 `:80` 에 있다(시작 커밋 판 grep). 계약 146 줄의 `:25` · `:80` 이 맞다.

### git 기록 측정 (예행 저장소 `p4d/rh` 를 `p4r2/rh5` 로 복제)

계약 문구 그대로 돌린 값. 한 단계마다 서명 없는 커밋 하나를 얹고 `end_sha:` 를 그 뒤로 옮겼다.

```text
단계                                               ER-05 셋째  ER-05 넷째  AR-05 ①  AR-05 ②
예행 그대로                                          0           0           0        0 · 14
+ 서명 없이 harness/hooks/hooks.json 고친 커밋       0           0           1        0 · 14
+ 서명 없이 루트 README.md 고친 커밋                 0           1           1        0 · 14
+ p05 서명을 단 scripts/sync-docs.py 커밋            0           1           2        0 · 14
```

서명 줄 목록(셋째 · ②)은 세 경우 모두 못 본다. 경로로 직접 세는 두 측정(넷째 · ①)이 각각 제 몫을 잡는다. 넷째는 1 회차 제안보다
하나를 더 뺀다 — 다른 Phase 서명 줄이 달린 커밋. 이 Phase 서명이 달렸거나 서명이 없는 커밋은 그대로 세므로 이 Phase 가 서명을 빠뜨려도 여전히 잡힌다.

### 그 밖에 다시 돌린 것

1. **Step 6.2 · 6.5** — 레포의 `sprint-contract/SKILL.md` 에서 명령을 옮겨 bash 로 돌렸다. `28` · 기능 조건 `18` · 헤더 열둘(서술 다섯 · 조건 일곱) ·
   조건 줄은 조건 절에만 · `OK conditions=28` · `OK 미실측 0 건`
2. **측정 커버리지 검출기** — `contract-schema.md` 732 줄 절의 블록 그대로. `UNCOVERED` 열한 조건(SK-01 · SK-03 · SK-04 · SK-05 · SK-06 · ER-01 · ER-02 · ER-05 · AR-01 · AR-02 · AR-03)
   모두 235-242 줄에 해소 줄이 있다. ER-05 해소 줄은 새 두 문자열까지 적었다
3. **바뀐 네 파일에 걸린 나머지 측정** — SK-01 (a) 8 값 1 (b) `committed=[M mine.txt A new.txt]` · `still_staged=[D other.txt M shared.txt]` ·
   SK-02 5 값 1 · SK-03 (a) 7 값 1 (b) bash · `RUNNER=zsh` 둘 다 네 줄 요구값 · `worktrees=1` · SK-04 (a) `1 1` · 0 (b) 1 · 1 · AR-03 5 값 1 · 한 줄 awk
   `harness/scripts/commit-guard.sh harness/evals/hooks/ ` · AR-04 `0 1 1 1 1` · `pfile rc=0` · RE-02 `check_path_commit() ` · 2 · 1 · AP-03
   `bare_open_total=0 unclosed_total=0` · AP-04 `1 1 1 1 1` · ER-04 0 · AP-01 0(머리 설정 값 `1.4.0`) · DG-02 (a) 일곱 줄 `new_warnings=0`(더한 줄
   71 · 4 · 3 · 1 · 1 · 11 · 7, 린터 `markdownlint-cli2 v0.23.2`) (b) `0 0 0 0 ` (c) `0 0 0 ` · DG-05 (d) `00 00 00 00 `.
   모의본을 git 저장소로 만든 사본에서 DG-05 (a) V 줄 10 · `ERROR`/`FAIL` 0 (b) 전체 킷 `FAIL` 0 (c) bash 로 `0 0 0 0 ` · `check-stale-values.py` 종료 코드 0 · 이 Phase 파일 0 건
4. **1 회차 뒤 바뀌지 않은 파일** — 나머지 열 파일은 1 회차 모의본(`p4r/E`)과 `cmp` 로 같다. 그래서 ER-02 · SK-05 · SK-06 · AR-01 · AR-02 · RE-01 은 1 회차 실측이 그대로 맞다
5. **예행 계약과 지금 계약** — 조건 줄이 한 글자도 다르지 않다. 예행 뒤 바뀐 것은 봉인 전 실측 글(표 값 · 대조 설명)과 ER-05 커버리지 해소 줄뿐이다

### 막지 않는 것 (넣으면 좋다)

1. AR-05 ① 은 다른 Phase 서명이 달린 커밋도 서명 없는 커밋으로 센다(위 표 넷째 단계에서 ① 이 1 → 2). ER-05 넷째는 같은 경우를 빼면서 ① 은
   빼지 않아 두 측정의 태도가 다르다. `phase-dependencies.md` 가 Phase 5 ~ 9 를 Phase 4 뒤에 두므로 지금 구간에 그런 커밋이 들어올 일은 드물고,
   들어와도 거짓 통과가 아니라 거짓 실패 쪽이다. QA 가 ① 에서 1 이상을 보면 그 커밋의 서명부터 보라는 한 줄을 AR-05 에 두면 헷갈림이 준다
2. ER-01 (b) 의 `mut.py` 는 모의본 문구를 글자 그대로 찾는다. BUILD 가 희소 체크아웃 세 줄을 다른 말로 쓰면 `NO_ANCHOR` 로 멈춘다 — 조용히
   통과하지는 않지만 그 조건이 실패로 떨어진다. 계약 166 줄대로 BUILD 가 `mock.py` 치환을 그대로 옮기면 된다
3. 197 줄의 「서명 줄로 이 Phase 커밋을 가리는 조건」 목록에 DG-03 이 빠졌다(DG-03 도 `my` 를 쓴다). 판정에는 영향이 없다

VERDICT: APPROVE
