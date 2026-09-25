# 카이젠 2026-09-24 Final — `kaizen-0924-f1-harness-followups` 계약 초안 검토

- 검토 대상: `.harness/sprint-contract-kaizen-0924-f1-harness-followups.md` (봉인 전 초안, 1033 줄 · 조건 30 줄, 검토 시점 sha256 앞 16 자 `8e0b9b48f58ceea8`)
- 개정 파일: 아직 없다 (봉인 전이라 정상)
- 검토자: `REVIEW` 에이전트 (사용자 승인 대신 — 러닝북 `계약 규칙` 의 두 기록 시각 · Final 러닝북 「Codex 독립 검토 지적」). 쓴 파일은 이 검토 결과 하나다.
  다시 돌린 측정은 전부 스크래치 `scratchpad/f1h-review/` 안에서 돌렸다. 작업 폴더 HEAD `5b4fd72` · 원래 레포 HEAD `9cd924b` 는 검토 전후 그대로다
- 읽은 입력: Final 러닝북 전문 · 공통 러닝북(계약 규칙 · git 규칙 · 말투 · 검증 절) · `final-todo.md` · `xdiag-all.md` P1 ~ P17 전문 · Codex `r1-harness.md` 7 건 · 계약 초안 전문
- 검토일: 2026-09-25

## 결론

**고칠 것 열이 있어 CHANGES 다.** 초안은 입력 항목을 89 줄 표로 빠짐없이 다뤘고, 측정 대부분은 알려진 답 · 시작 커밋 판 음성 대조가 붙어 있으며
다시 돌린 값이 초안의 봉인 전 실측 표와 전부 같았다. 고칠 것은 네 갈래다.

1. **받는 쪽을 하나 놓쳤다** — V 줄 글자를 바꾸는 ER-08 의 받는 쪽인 `harness/docs/guides/plugin-validation-guide.md` §출력 포맷 예시(C1).
   같은 매핑을 적은 오케스트레이터 F2 표도 AR-01 이 고치는 문서 낡음 검사(`detect-docs-drift.py`)와 따로 논다(C2). SK-02 파일 안에 같은 결함 두 자리가 남는다(C3)
2. **구현 방향이 새 결함을 만든다** — CI(자동 검사)에서 reflect-kit 시험의 zsh 경우가 조용히 건너뛰어진다(C4). 평가 시각 블록이 `.harness/` 에 `.bak` 파일을 남긴다(C5)
3. **러닝북 「봉인 전에 막는 측정 구멍」 두 줄을 다 지키지 않는다** — 공유 파일을 직접 세는 측정이 없다(C7). 0 을 기대하는 측정 여섯 곳에 함수 정의 확인이 없다(C8).
   ER-06 (b) 는 다른 계약이 동시에 쓰는 살아 있는 작업 폴더를 읽는다(C6)
4. **문구가 모호하다** — ER-07 예외(C9). 입력 표에 리뷰가 찾은 새 항목과 교차 진단 (2) 절 묶음이 없다(C10)

열 가지 모두 고칠 문구를 아래에 적었다. 새로 넣는 측정은 이 검토에서 시작 커밋 판에 먼저 돌려 값을 적었다.

## 직접 다시 돌린 것

초안에 적힌 떼는 명령으로 도우미 스물을 스크래치 `f1h-review/K/` 에 떼었다(`align.sh` 는 Phase 4 계약에서). 개정 파일이 아직 없어 `common.sh` 의
`END` 줄만 시작 커밋 `5b4fd72` 로 바꾼 사본으로 돌렸다(초안의 봉인 전 실측과 같은 방식).

| 무엇 | 결과 | 초안 값과 |
| --- | --- | --- |
| `toks.py` 접두 열둘 (`$T/B`) | SK01 `30 ng=30` · SK02 `13/13` · SK03 `8/8` · SK04 `6/6` · SK05 `34 ng=33` · ER01 `1/1` · ER03 `2/2` · ER04 `1/1` · ER05 `6/6` · ER06 `4/4` · ER07 `1/1` · AR03 `1/1` | 같다 |
| 새 글자 · 옛 글자 줄 수 | 새 69 · 옛 37 · 바뀌지 않을 줄 1 = 107 (표에서 직접 셈) | 같다 |
| `orch.sh B B` · `upref.sh B` · 배치 표 넷째 칸 | `diagram=0 depdoc=0 concur=0 signline=0 auto_removed=0 auto_added=0` · `upper=0/5` · `1(최고),2,3,4(최저),` | 같다 |
| `ren2.sh` (시작 판 훅) | N1 · N2 · N5 `hook_rc=2 git_dels=0 DISAGREE`, N3 · N4 `hook_rc=2 git_dels=60 agree` | 같다 |
| `ident.sh` · `renlist.sh` | `wt-x project_name=wt-x hash_is_main=0` · `diff old=[] new=[keep/data.txt]` · `status old=[] new=[keep/two.txt]` | 같다 |
| `logdir.sh` 여덟 번 · `logblk` 비교 | 작업 폴더 `kaizen-0924 kaizen-0924-d4e5f6 made=0` · 본 레포 `claude-plugins claude-plugins-a1b2c3 made=0` (두 파일 · 두 셸 같음) · 차이 0 | 같다 |
| `sealcnt.sh` bash · zsh, `$PWD` | `none rc=0` · `no_fm_get rc=0 absent=79` · `full rc=0 ok=67 absent=12` | 같다 |
| `sealcnt.sh` bash, `$T/B` (C6 대안) | `none rc=0` · `no_fm_get rc=0 absent=77` · `full rc=0 ok=67 absent=10` | 새로 잼 — 작업 폴더에는 커밋 안 된 Final 초안 둘이 더 있다 |
| `vline.sh` | `A vp_rc=2 v3569_fail_lines=0 bare_fence=PASS` · `B vp_rc=0 … PASS` | 같다 |
| 새 CI 시험 여섯 (`$T/B` 에서) | 넷 `결과: 6 · 24 · 16 · 10 경우 중 불일치 0` rc=0, 둘 `EVALS_PASS` rc=0 | 같다 |
| AP-04 이름 줄 열둘 | 열두 파일 모두 1 | 같다 |
| 근거 파일 · 입력 대조 | `phase1.md:90` ultracode 문장 · `phase4.md:148-149` `initialPrompt` 와 배치 순서 · `phase15.md:114` · `:131` 663 제목 · 감사 기록 529 두 사이클 · 새 URL(`etc_seq=663` · `sub-agents`) 이 근거 파일에 있음 | 초안 인용과 맞다 |
| AR-04 (b) ID 목록 | 입력 표에서 `고치지 않음` 이 든 행을 뽑으면 정확히 스물여섯 ID | 같다 |

새로 돌린 측정(아래 고칠 것의 근거):

| 무엇 | 시작 커밋 판 값 |
| --- | --- |
| C1 — 출력 포맷 예시에서 판정 글자로 끝나지 않는 V 줄 | `2` (`V3 refs 89 links, 2 BROKEN` · `V4 triggers 58 keywords, 1 duplicate`) · `— FAIL` 로 끝나는 줄 0 |
| C1 — `vline.sh` 에 `unjudged=` 를 더한 판 | `A … unjudged=4 …` · `B … unjudged=0 …` |
| C2 — 오케스트레이터 F2 매핑 표 | `reflect-kit=0 bambu-kit=0 onboarding-kit=0 howto-kit=0 api-kit=1 planning_refs=1` |
| C3 — phase-dependencies 옛 글자 | `planning-kit/references/` 1 줄 (`:56`) · `tone\|api}/` 1 줄 (`:124`) |
| C4 — reflect-kit 시험의 zsh 가지 | `project-id-test.sh:65-68` · `collect-status-test.sh:125-129` 가 zsh 없으면 `건너뜀 zsh 없음` 만 찍고 넘어간다 |
| C5 — `evald.sh` 에 `extra=` 를 더한 판, 모의 블록 둘 | `sed -i.bak` 만 쓴 블록: bash · zsh 모두 `rc=0 lines=1 now=1 other_changed=0 extra=1` · 끝에 `rm -f "$OUT.bak"` 를 붙인 블록: `extra=0` |
| C7 — 공유 파일 직접 세기 | `5b4fd72..5b4fd72` 0 · 양성 대조(마지막으로 `marketplace.json` 을 고친 커밋 `c~1..c`) 2 |

## 검토 항목별 판정

- **조건마다 FAIL 을 한 문장으로 쓸 수 있는가** — 30 줄 모두 쓸 수 있다. 예외 둘은 모호하다: ER-07 예외 문구(C9), AR-04 (a) 는 재는 명령이 적혀 있지 않다(권장 R4)
- **측정이 의도를 재는가** — 대부분 그렇다. 알려진 답을 git · 손으로 아는 이름 · 실제 페이지 이름에서 받고, 시작 커밋 판에서 떨어지는 것을 봤다.
  못 재는 곳: ER-08 이 V 줄 넷만 보고 V4 경고 줄과 문서 예시를 안 본다(C1). ER-04 가 블록이 남기는 부산물을 안 본다(C5). ER-06 (b) 가 끝 판이 아니라 작업 폴더를 읽는다(C6)
- **러닝북 측정 구멍 목록** — 상한 변수 받기(`END_UNRESOLVED` 로 멈춤) · 파일마다 비교(`newurls` · `mdcmp.sh` · `shcmp.sh`) · 규칙 · 줄 글자 묶음으로 새 편집기 경고 세기 · validate-plugin 종료 코드 · 옛 값 검사 범위는 지켰다.
  **못 지킨 둘**: 건드리면 안 되는 공유 파일을 `git log <기준>..<상한> -- <파일들>` 로 직접 세지 않는다(C7). 셸 함수 정의 확인 줄이 SC-00 · DG-01 · DG-03 · DG-04 에만 있고, 0 을 기대하는 SK-06 · AR-05 · ER-03 (b) 에는 없다(C8)
- **입력 항목** — final-todo · xdiag 계약 밖 · notes 넘김 · Codex 7 건은 빠짐없이 조건이나 이유로 다뤘다. Codex r1 2(중간)를 안 고치는 이유(새 실행기 = 새 기능)도 근거 줄(`SKILL.md:47`)을 확인했다.
  빠진 것: xdiag 각 절 (2) 의 Phase 계약 측정 구멍 묶음(P5 ~ P16) · V6 · V10 읽는 범위(P10 (2) · P13 (2)), 그리고 리뷰가 찾은 새 항목 넷(C10)
- **범위** — 서른 파일 모두 Final 러닝북 표의 이 계약 범위 안이다. 고칠 것이 더하는 파일(`harness/docs/guides/plugin-validation-guide.md`)과 자리(오케스트레이터 F2 표 · phase-dependencies `:56` · `:124`)도 범위 안이다
- **조건끼리 부딪힘** — 하나 있다. 개선안 ER-07 이 제외 이유로 backend-kit 세 줄이 인용한 명세 링크와 그 버전 숫자(`x.y.z` 꼴)를 적는데, 그 글자를 출력 문구에 옮기면 AP-01(더한 줄 버전꼴 0)과 SK-06 (b)(근거 밖 URL 0)에 걸린다(C9).
  kit-followups 와는 AR-02 (c) 가 그 계약이 고치는 `howto-kit/evals/run-evals.sh` 를 같은 끝 판에서 돌린다 — 권장 R2

## 고칠 것 (필수)

### C1 — ER-08: V 줄 형식의 받는 쪽인 검증 가이드 출력 예시가 빠졌다

`harness/docs/guides/plugin-validation-guide.md:488-520` §출력 포맷은 실패 V 줄을 `V3 refs 89 links, 2 BROKEN` · `V4 triggers 58 keywords, 1 duplicate` 처럼 판정 글자 없이 보여 준다.
ER-08 뒤에는 실제 출력과 달라진다. Counterpart 표의 「validate-plugin V 줄 글자」 행이 이 문서를 받는 쪽으로 적지 않았다. 또 ER-08 (a) 는 V3 · V5 · V6 · V9 넷만 재서,
V4(경고) 같은 다른 줄이 판정 없이 남아도 통과한다.

- 공통 정의 `MDS` 배열 끝에 `harness/docs/guides/plugin-validation-guide.md` 를 더한다 → `FILES` 서른하나 · `MDS` 스물하나.
  계약 안의 파일 수 글자를 모두 고친다(`grep -n '서른\|스물\|스무' "$CF"` 로 찾는다 — 범위 경계 둘째 줄 · 조건 작성 자문 `범위-미명시` · SK-06 (a)(b) · AP-01 · AR-05 (a)(b) · DG-02 (a) · 봉인 전 실측 DG-02 행).
  범위 경계의 「편집 전부터 있던 경고 합계」 는 스물한 파일로 다시 잰다
- 편집 전 감사 표에 행을 더한다: `| harness/docs/guides/plugin-validation-guide.md | :488-520 §출력 포맷 · :506 · :508 | 실패 V 줄 예시가 판정 글자 없이 끝난다 — ER-08 뒤 실제 출력과 다르다 | ER-08 (c) |`
- Counterpart 표 「validate-plugin V 줄 글자」 행의 받는 쪽에 `` `plugin-validation-guide.md` §출력 포맷 예시 `` 를 더하고, 다루는 곳을 `ER-08 (a)(c)` 로
- `vline.sh` 의 `printf '%s vp_rc=…` 줄을 아래 두 줄로 바꾼다:

  ```bash
  uj=$(printf '%s\n' "$out" | grep -E '^  V[0-9]+ ' | grep -cvE '— (OK|WARN|FAIL|SKIP)$')
  printf '%s vp_rc=%s v3569_fail_lines=%s unjudged=%s bare_fence=%s\n' "$t" "$rc" "$vfail" "$uj" "$bf"
  ```

- ER-08 (a) 기대 줄을 `A vp_rc=2 v3569_fail_lines=4 unjudged=0 bare_fence=FAIL` · `B vp_rc=0 v3569_fail_lines=0 unjudged=0 bare_fence=PASS` 로 바꾸고, 시작 커밋 판 값에 `unjudged=4` 를 적는다(리뷰 실측)
- ER-08 에 (c) 를 더한다: 「(c) `type sect >/dev/null || exit 2;` 뒤 `sect "$T/E/harness/docs/guides/plugin-validation-guide.md" '### 출력 포맷' | grep -E '^  V[0-9]+ ' | grep -cvE '— (OK|WARN|FAIL|SKIP)$'` 이 0 이고,
  같은 출력에서 `— FAIL` 로 끝나는 줄이 1 이상 (시작 커밋 판 2 · 0 — 실패 예시를 지워서 맞추는 길을 막는다)」
- 「측정이 기대는 제목」 목록에 `### 출력 포맷` (검증 가이드)을 더한다. 측정 해소 줄에 ER-08 (c) 를 더한다

### C2 — AR-01: 오케스트레이터 F2 매핑 표가 드리프트 검사와 따로 논다

`.claude/skills/kaizen-orchestrator/SKILL.md` Step F2 「소스 → 출력 매핑」 표(`:602-614`)에 reflect-kit · bambu-kit · onboarding-kit · howto-kit 행이 없고, planning-kit 행은 없는 `planning-kit/references/` 를 적는다.
`detect-docs-drift.py` 의 `SOURCE_TO_HTML` 주석은 이 표를 기준으로 삼고(「kaizen-orchestrator SKILL.md 가 매핑 대상으로 명시하는데도 누락되어」), Final 러닝북은 `kaizen-0924-final` 이
문서 사이트를 다시 만들 때 이 표를 쓰라고 한다. AR-01 이 스크립트에만 onboarding · api · howto 를 넣으면 두 매핑이 더 벌어진다. howto-kit 행이 없는 것은 SK-01 이 말하는 「Phase 17 을 빠뜨린 자리」 이기도 하다.

- 개선안 AR-01 끝에 「오케스트레이터 F2 표에 reflect-kit · bambu-kit · onboarding-kit · howto-kit 행을 드리프트 매핑과 같은 소스로 더하고, planning-kit 행에서 없는 `planning-kit/references/` 를 뺀다」
- AR-01 지금 측정을 (a) 로 이름 붙이고 (b) 를 더한다. (b) 는 아래 명령의 출력이 정확히
  `reflect-kit=1 bambu-kit=1 onboarding-kit=1 howto-kit=1 api-kit=1 planning_refs=0` 이다
  (시작 커밋 판 `reflect-kit=0 bambu-kit=0 onboarding-kit=0 howto-kit=0 api-kit=1 planning_refs=1` — 리뷰 실측. `api-kit=1` 은 이미 있는 행이 셈에 걸리는지 보는 양성 대조):

  ```bash
  f="$T/E/.claude/skills/kaizen-orchestrator/SKILL.md"
  tb=$(sed -n '/^\*\*소스 → 출력 매핑/,/^\*\*절차:\*\*/p' "$f" | grep -E '^\| ')
  for k in reflect-kit bambu-kit onboarding-kit howto-kit api-kit; do
    printf '%s=%s ' "$k" "$(printf '%s\n' "$tb" | grep -cF "| \`docs/$k/\` |")"
  done
  printf 'planning_refs=%s\n' "$(printf '%s\n' "$tb" | grep -cF 'planning-kit/references/')"
  ```

- 「측정이 기대는 제목」 목록에 `**소스 → 출력 매핑` · `**절차:**` (오케스트레이터 F2)를 더한다. Counterpart 표 「드리프트 매핑 줄」 행에 「같은 매핑을 사람이 읽게 적은 오케스트레이터 F2 표 — AR-01 (b)」 를 더한다

### C3 — SK-02: 같은 파일 안에 같은 결함 두 자리가 남는다

`phase-dependencies.md:56` 은 onboarding(`:70`)과 같은 이유로 없는 `planning-kit/references/` 를 적는다. `:124` 의 리서치 전용 모드 목록 `docs/{backend|infra|rust|react|planning|tone|api}/` 에 howto 가 없다.
SK-02 가 `:124` 줄의 `Phase 7~16` 은 고치면서 같은 줄 괄호 목록은 두는 셈이다.

- `toks.py` `ROWS` 에 세 줄을 더한다:

  ```python
  ("SK02-O6", "PD", r"""planning-kit/references/""", 0),
  ("SK02-O7", "PD", r"""|planning|tone|api}/""", 0),
  ("SK02-N9", "PD", r"""|planning|tone|api|howto}/""", 1),
  ```

- SK-02 (a) 기대 끝줄을 `rows=16 ng=0` 으로, 봉인 전 실측 표 시작 커밋 판 값을 `16 ng=16` 으로. 편집 전 감사 표 phase-dependencies 행의 읽은 줄에 `:56` · `:124` 괄호 목록을 더한다
- 측정 해소 줄의 「`toks.py` 백일곱 줄 · 새 글자 예순아홉 · 옛 글자 서른일곱」 을 백열 · 일흔 · 서른아홉으로 다시 센다

### C4 — AR-02: zsh 설치 단계가 reflect-kit 시험보다 뒤면 CI 에서 zsh 경우가 조용히 빠진다

`reflect-kit/evals/hooks/project-id-test.sh:65-68` · `collect-status-test.sh:125-129` 는 zsh 가 없으면 `건너뜀 zsh 없음` 만 찍고 통과한다(phase12-notes 넘김 줄도 「zsh 가 없으면 zsh 경우를 건너뛴다」).
지금 AR-02 (a) 는 설치 단계가 `sh` 러너 둘보다 앞이기만 하면 되므로, 우분투에서는 reflect-kit 의 zsh 경우가 한 번도 안 돈다.

- AR-02 (a) 문구 「그 단계가 `sh` 러너 두 단계보다 앞에 있다」 → 「그 단계가 여섯 시험 단계 모두보다 앞에 있다 — reflect-kit 시험 둘은 zsh 가 없으면 zsh 경우를 건너뛴다」
- `ci.py` 의 `order = … for c in CMDS[4:]` 를 `for c in CMDS` 로, 출력 이름 `zsh_before_sh` 를 `zsh_first` 로. AR-02 (a) 기대 끝줄 `placed=7/7 zsh_first=1`
- 봉인 전 실측 표 AR-02 행의 모의 ci.yml 을 zsh 단계를 맨 앞에 둔 꼴로 다시 돌려 적는다

### C5 — ER-04: 평가 시각 블록이 리포트 옆에 `.bak` 을 남긴다

초안의 모의 블록(`sed -i.bak "s/^Evaluated: .*/…/" "$OUT"`)을 그대로 넣으면 평가마다 `.harness/sprint-feedback-<slug>.md.bak` 이 생긴다. 지금 `evald.sh` 는 리포트 한 파일만 봐서 이것을 못 잡는다.

- 개선안 ER-04 에 「블록은 리포트 옆에 새 파일을 남기지 않는다 — `sed -i.bak` 을 쓰면 `.bak` 을 지운다(또는 임시 파일에 쓰고 `mv`)」
- `evald.sh` 루프를 고친다: `cp "$w/r.md" "$w/orig.md"` 뒤에 `n0=$(ls -A "$w" | wc -l | tr -d ' ')`, `t1=…` 뒤에 `n1=$(ls -A "$w" | wc -l | tr -d ' ')`,
  마지막 `printf` 에 `extra=%s` 와 `"$((n1 - n0))"`, 루프 끝에 `rm -f "$w"/*.bak` (첫 바퀴가 남긴 `.bak` 이 둘째 바퀴 셈을 가리지 않게)
- ER-04 (a) 기대 줄을 `rc=0 lines=1 now=1 other_changed=0 extra=0` 으로. 봉인 전 실측 표 ER-04 행에 「`sed -i.bak` 만 쓴 모의 블록 `extra=1` · `.bak` 을 지우는 모의 블록 `extra=0` (bash · zsh, 리뷰 실측)」

### C6 — ER-06 (b): 살아 있는 작업 폴더 대신 끝 판을 읽는다

`sealcnt.sh … "$PWD"` 는 작업 폴더의 `.harness/` 를 센다. 거기에는 커밋 안 된 Final 초안 둘이 있고, kit-followups · final 계약이 이 계약과 같은 때에 계약 파일을 쓴다.
`full … broken=` 빈 값이 이 계약 밖의 상태로 떨어질 수 있다(조건 작성 자문 `측정-환경-오염` 과도 어긋난다). 블록이 정의 없이 멈추는지는 어느 판에서 돌려도 같으므로 끝 판이면 된다.

- ER-06 (b) 의 `"$PWD"` 를 `"$T/E"` 로 바꾼다
- 봉인 전 실측 표 ER-06 (b)(c) 행 시작 판 값을 `$T/B` 로 다시 적는다: `none rc=0` · `no_fm_get rc=0 absent=77` · `full rc=0 ok=67 absent=10` (리뷰 실측, bash)

### C7 — AR-05: 공유 파일을 직접 세지 않고, 서명 글자가 틀린 커밋을 못 본다

러닝북 첫 구멍은 「건드리면 안 되는 파일은 서명 줄 달린 커밋 목록으로만 재지 말고 `git log <기준>..<상한> -- <파일들>` 로 직접 센다」 이다. 초안은 공유 파일을 AR-05 (a)(c) 로 잰다고 적었는데,
(a) 는 이 계약 서명 커밋만, (c) 는 `Kaizen-Phase:` 줄이 아예 없는 커밋만 본다. 서명 글자를 잘못 적은 커밋(예: 슬러그 끝 `s` 빠짐)이 공유 파일이나 다른 킷 폴더를 고치면 세 측정 모두 0 이다.

- (c) 의 `grep -q '^Kaizen-Phase: '` 를 `grep -qxE 'Kaizen-Phase: kaizen-0924-f1-(harness|kit)-followups'` 로 바꾸고 문구를 「알려진 두 서명 어느 것과도 글자가 같지 않은 커밋이 `.harness/` 밖 파일을 건드린 수가 0」 으로
- (f) 를 더한다: 「(f) `git log --format=%H "$B..$END" -- .claude-plugin/marketplace.json ':(glob)*/.claude-plugin/plugin.json' README.md CLAUDE.md ':(glob)docs/**/*.html' ':(glob)docs/kaizen/**' .claude/kaizen-input/insights-report.md .harness/.meta/orchestrator-audit-log.md .harness/.meta/kaizen-failure-count.yaml .harness/stale-values.yaml ':(glob).claude/skills/docs-site/**' | while read -r c; do git log -1 --format=%B "$c" | grep -qxF 'Kaizen-Phase: kaizen-0924-f1-kit-followups' || echo "$c"; done | grep -c .` 이 0 — 공유 파일을 건드린 구간 안 커밋을 서명과 상관없이 직접 센다(kit-followups 서명 커밋은 그 계약 몫이라 뺀다).
  `docs/*/research-log.md` 는 kit-followups 가 고치는 파일이라 넣지 않는다. 양성 대조: `c=$(git log -1 --format=%H -- .claude-plugin/marketplace.json)` 로 `"$c~1..$c"` 구간에 같은 경로 목록을 주면 1 이상 (리뷰 실측 2)」
- 범위 경계의 「공유 파일 … 건드리지 않는다 — AR-05 (a)(c)」 를 「AR-05 (c)(f)」 로

### C8 — SK-06 · AR-05 · ER-03 (b): 0 을 기대하는 측정에 함수 정의 확인이 없다

`added` · `newurls` · `evurls` · `my` · `unsigned_on` · `verify_seal` · `logblk` 가 정의되지 않은 셸에서는 「command not found」 뒤 셈이 0 이 되어 조용히 통과한다.
초안 `:343` 의 일반 문장은 좋지만, 조건 줄에는 SC-00 · DG-01 · DG-03 · DG-04 만 확인 줄을 달았다. 같은 꼴로 맞춘다.

- SK-06 측정 앞에 `type added newurls evurls >/dev/null || exit 2;`
- AR-05 (a)(b)(d) 앞에 `type my unsigned_on verify_seal >/dev/null || exit 2;`
- ER-03 (b) 앞에 `type logblk >/dev/null || exit 2;`

### C9 — ER-07: 예외 문구가 모호하고, 제외 이유 글자가 다른 조건과 부딪힐 수 있다

「(a) 첫 줄이 `clean rc=1` 이면 … PASS 로 본다」 는 그때 `files` · `want` · `excluded_line` · 둘째 줄까지 면제되는지 읽을 수 없다.

- 예외 문구를 바꾼다: 「예외: (a) 첫 줄의 `rc` 가 1 이면 그 출력에 찍힌 파일이 `my` 에 하나도 없을 때만 그 `rc` 를 PASS 로 본다 — 다른 계약이 넣은 옛 값이다. 이때도 `files` 와 `want` 가 같고 `excluded_line=1` 이어야 하며, 둘째 줄은 그대로 요구한다」
- 개선안 ER-07 끝에 「제외 이유 글자에 버전꼴 숫자(`x.y.z`)와 근거 파일 밖 URL 을 쓰지 않는다 — AP-01 · SK-06 (b) 와 부딪힌다」

### C10 — 입력 표: 리뷰가 찾은 항목과 교차 진단 (2) 절 묶음을 더한다

입력 표 끝에 여섯 행을 더한다.

| ID | 출처 | 항목 | 처리 |
| -- | ---- | ---- | ---- |
| F1H-90 | 리뷰 (입력 밖) | 오케스트레이터 F2 매핑 표에 reflect · bambu · onboarding · howto 행이 없고 planning 행이 없는 `planning-kit/references/` 를 적는다 — Final 러닝북이 문서 사이트 재생성에 이 표를 쓴다 | 조건 AR-01 (b) |
| F1H-91 | 리뷰 (입력 밖) | `.claude/skills/docs-site/SKILL.md:47-55` 매핑 표가 harness · flutter · design · backend · infra · tone · process 일곱 줄뿐이다 | 고치지 않음 — `.claude/skills/docs-site/` 는 세 Final 계약 어느 범위에도 없다. 다음 사이클 |
| F1H-92 | 리뷰 (입력 밖) | 오케스트레이터 F4 research-log 목록(`:731-738`)과 체크리스트 「per-kit research-log 6개 파일」(`:765`)에 design · tone · api 연구 기록이 없다 | 고치지 않음 — 목록을 「`docs/*/research-log.md` 가 있는 킷 전부」 같은 규칙으로 바꾸려면 「파일이 없으면 새로 만든다」 조문(`:56`)과 함께 정해야 하는 새 내용이다. 이번 Final 은 러닝북이 `docs/*/research-log.md` 로 대신 정했다. 다음 사이클 |
| F1H-93 | 리뷰 (받는 쪽 대조) | `harness/docs/guides/plugin-validation-guide.md` §출력 포맷 예시가 실패 V 줄을 판정 글자 없이 적는다 | 조건 ER-08 (c) |
| F1H-94 | xdiag P10 (2) DG-05 (b) · P13 (2) AP-03 | validate-plugin V10 이 `docs/<킷>/` 원본을, V6 가 `skills/*/references/` 를 읽지 않는다 | 고치지 않음 — F1H-40 의 `V6 범위` 결정(다음 사이클 Phase 4)과 함께 정한다 |
| F1H-95 | xdiag P5 · P6 (2) 2 · 3 · P7 · P8 (2) 1 · 2 · P9 · P10 · P11 · P12 · P13 · P14 · P16 의 (2) 절 | Phase 계약 측정의 구멍(서명 없는 커밋 · 더한 줄만 센 편집기 경고 · 좁은 정규식 · 구조상 늘 0 인 값 등) | 다른 계약 — `kaizen-0924-final` (계약 · 평가자 피드백 교차 진단 기록) |

- AR-04 (b) 목록에 `F1H-91` · `F1H-92` · `F1H-94` 를 더해 「스물여섯」 을 「스물아홉」 으로

## 권하는 것 (선택)

- **R1** 범위 경계 측정 해소 첫 줄 뒤에 한 문장: 「새 글자는 한 줄 안에 둔다 — `toks.py` 는 줄마다 세므로 긴 문장을 줄바꿈으로 가르면 NG 다」. 이 가이드들은 한 문장을 여러 줄로 감싸는 곳이 많아 구현 단계가 걸리기 쉽다
- **R2** AR-02 (c) 는 kit-followups 가 고치는 `howto-kit/evals/run-evals.sh` · onboarding 평가 파일을 같은 끝 판에서 돌린다. 종료 코드가 0 이 아닌 명령이 있으면
  「그 명령이 부르는 파일을 바꾼 구간 안 커밋이 전부 `Kaizen-Phase: kaizen-0924-f1-kit-followups` 서명이고 `$T/B` 판에서는 같은 명령이 0 일 때 이 계약 몫이 아니다」 예외를 두면 남의 중간 상태로 떨어지지 않는다
- **R3** AP-03 에 「`--check=code-fence` 종료 코드 0 과」 를 더한다 — 러닝북은 validate-plugin 결과를 V 줄 글자보다 종료 코드로 재라고 한다
- **R4** AR-04 (a) 에 재는 명령을 적는다: 제목마다 `grep -cx '## 커밋' "$T/E/$NOTES"` 꼴이 1
- **R5** ER-01 시험에 N4 꼴(옮긴 새 경로가 지정 경로 밖이라 삭제가 실리는 경로 지정 커밋 → 차단)을 ㉚ 으로 더한다. 지금은 계약 도우미(`ren2.sh`)만 재서 CI 에는 이 경우가 없다
- **R6** ER-06 (d) 새 설명에 「서명 줄을 끝 문단에 두는 관례는 그대로 둔다 — 도우미가 자리를 보지 않을 뿐이다」 를 함께 적는다. 옛 문장을 통째로 지우면 다음 작성자가 서명 줄을 아무 데나 둔다
- **R7** phase17-notes `:138`(러너 시간 3.4 초 → 8 ~ 9 초, CI 에 넣은 뒤 시간 상한을 조건으로 둘지)을 F1H-82 출처 칸에 더한다

VERDICT: CHANGES

## 2 회차

- 검토 대상: 같은 계약 초안 (1086 줄 · 조건 30 줄, 검토 시점 sha256 앞 16 자 `588d354719dbe5a2`). 개정 파일은 아직 없다 (봉인 전이라 정상)
- 계약에 적힌 떼는 명령을 그대로 돌려 도우미 스물하나(새 `f2map.sh` 포함)를 스크래치 `scratchpad/f1h-review2/K/` 에 떼었다. `common.sh` 의 `END` 줄만 시작 커밋 `5b4fd72` 로 바꾼 사본으로 돌렸다.
  작업 폴더 HEAD `5b4fd72` · 원래 레포 HEAD `9cd924b` · 계약 파일 sha256 은 검토 전후 그대로다. 쓴 파일은 이 절 하나다
- 검토일: 2026-09-25

### 2 회차 결론

**1 회차 고칠 것 열(C1 ~ C10)과 권하는 것 일곱(R1 ~ R7)은 모두 반영됐다.** 반영한 자리에서 다시 돌린 값이 계약의 봉인 전 실측 표와 전부 같다.
새로 고칠 것이 둘 있어 CHANGES 다. 둘 다 문구 한두 줄이고 새 실측은 필요 없다.

1. **C11** — ER-07 예외의 「그 출력에 찍힌 파일」 이 파일 이름을 찍지 않는 출력을 가리킨다. 이 계약 파일이 옛 값을 되살려도 예외로 통과할 수 있다. 1 회차 C9 에서 이 검토가 준 문구의 구멍이다
2. **C12** — AR-05 (d) 가 살아 있는 작업 폴더의 `.harness/` 를 읽는다. 계약이 스스로 적은 「작업 폴더를 읽는 예외는 둘」 과 어긋나고, 1 회차 C6 과 같은 결함이다

### 1 회차 지적 반영 확인

| 항목 | 반영한 자리 | 다시 잰 값 |
| ---- | ----------- | ---------- |
| C1 | `common.sh` `MDS` 스물하나 · `FILES` 서른하나, 편집 전 감사 행(`:486-522` · `:506` · `:509` — 1 회차에 적은 `:488-520` · `:508` 보다 실제 줄에 맞다), Counterpart 행, `vline.sh` `unjudged=`, ER-08 (a) 기대 줄 · (c), 제목 목록, 범위 경계 경고 합계 | `vline.sh` 시작 판 `A vp_rc=2 v3569_fail_lines=0 unjudged=4 bare_fence=PASS` · `B vp_rc=0 v3569_fail_lines=0 unjudged=0 bare_fence=PASS`. ER-08 (c) 명령: 시작 판 판정 없는 줄 2 · `— FAIL` 0, 예시 두 줄에 `— FAIL` · `— WARN` 을 붙인 모의본 0 · 1, V3 예시를 지운 모의본 0 · 0, `— ERROR` 로 적은 모의본 1 · 0. 스물한 파일 경고 합계 242 (Codex 로 든 셋 8 · 9 · 8, 검증 가이드 30, 나머지 열일곱 187) · shellcheck 2 줄 |
| C2 | 개선안 AR-01 끝 문장, AR-01 (b) 와 `f2map.sh`, Counterpart 행, 제목 목록 | 시작 판 `reflect-kit=0 bambu-kit=0 onboarding-kit=0 howto-kit=0 api-kit=1 planning_refs=1`. 표 머리 줄을 지운 사본 `NO_TABLE` 종료 코드 2, 없는 파일 `NO_FILE` 종료 코드 2. F2 표(`:601-617`)는 자동 생성 구간(`:402-521`) 밖이라 AR-03 재생성과 부딪히지 않는다. 표의 원본 칸 열두 폴더 가운데 없는 것은 `planning-kit/references/` 하나뿐이다(`git ls-tree`) |
| C3 | `toks.py` 세 줄, SK-02 (a) `rows=16`, 측정 해소 줄 | SK02 `rows=16 ng=16`. 전체 백열 줄 = 새 일흔하나(SK05-N8 포함) + 옛 서른아홉 — 계약 글자와 같다. `Phase 7~16` 은 `:124` · `:130` 두 줄이라 SK02-O1 기대 0 이 둘 다 고치게 한다 |
| C4 | AR-02 (a) 문구, `ci.py` `zsh_first`, 봉인 전 실측 행 | 시작 판 `placed=0/7 zsh_first=0`. 모의 ci.yml 둘: zsh 단계를 맨 앞에 둔 꼴 `placed=7/7 zsh_first=1`, reflect-kit 시험 뒤 · `sh` 러너 앞에 둔 꼴 `placed=7/7 zsh_first=0`. 둘 다 actionlint 종료 코드 0 · 되막음 글자 0 |
| C5 | 개선안 ER-04, `evald.sh` `extra=`, ER-04 (a) 기대 줄 | 시작 판 `NO_BLOCK` (bash · zsh). `sed -i.bak` 만 쓴 모의 블록 두 줄 `extra=1`, `rm -f "$OUT.bak"` 를 붙인 블록과 임시 파일 뒤 `mv` 하는 블록은 두 줄 `rc=0 lines=1 now=1 other_changed=0 extra=0` (bash · zsh) |
| C6 | ER-06 (b) `"$T/E"`, 봉인 전 실측 행 | `$T/B` 에서 `none rc=0` · `no_fm_get rc=0 absent=77` · `full rc=0 ok=67 absent=10` (bash · zsh). 셈 블록 머리에 정의 확인 한 줄을 넣은 모의본 `none rc=2` · `no_fm_get rc=2` · `full rc=0 ok=67 absent=10` |
| C7 | AR-05 (c) 새 정규식 · (f), 범위 경계 줄 | 시작 판 구간에서 (c) 0 · (f) 0. 양성 대조 `c=9cb0e02` (합치기 커밋, 부모 `f27a3d8` · `0716a8f`) 의 `c~1..c` 에서 (f) 2. 경로 열하나 모두 마지막으로 건드린 커밋이 있다 |
| C8 | SK-06 · AR-05 (a)(b)(d) · ER-03 (b) 앞 `type` 줄 | 글자로 확인 |
| C9 | ER-07 예외 문구, 개선안 ER-07 끝 문장 | 글자로 확인. 예외 문구에 새 구멍 — C11 |
| C10 | 입력 표 F1H-90 ~ 95, AR-04 (b) 스물아홉 | 입력 표 아흔다섯 행(번호 빠짐 · 겹침 0)에서 처리 칸에 `고치지 않음` 이 든 행을 뽑으면 AR-04 (b) 의 스물아홉 ID 와 정확히 같다 |

권하는 것 R1 ~ R7 도 모두 들어갔다 — 범위 경계 한 줄(R1), AR-02 (c) 예외(R2), AP-03 종료 코드(R3), AR-04 (a) 명령(R4), ER-01 ㉚ 과 (d) 번호 `㉖ ㉗ ㉘`(R5), 개선안 ER-06 문장(R6), F1H-82 출처 칸(R7).
R5 · R2 는 받는 쪽까지 확인했다. 훅 시험은 `COMMIT_GUARD_HOOK` 로 훅을 바꿀 수 있고(`commit-guard-test.sh:8`) 지금 경우 번호가 ㉕ 까지라 ㉖ ~ ㉚ 이 겹치지 않는다. 시작 판 시험은 종료 코드 0 · PASS 39 줄 · `실패 0 건`.
AR-02 (c) 예외는 여섯 시험이 모두 자기 킷 폴더 안 파일만 부르는 것(`../..` · `../../hooks` · `../SKILL.md` · 킷 안 `scripts/`)을 확인했다 — 이 계약 파일이 깨뜨린 실패를 예외가 덮을 길이 없다.
kit-followups 계약도 두 러너의 끝 줄 `EVALS_PASS` 와 `결과: <N> 경우 중 불일치 0` 꼴을 그대로 둔다(그 계약 `:53` · `:965` · `:993`).

그 밖에 다시 돌린 것: `toks.py` 접두 열둘 시작 판 값 · `orch.sh B B` 여섯 값 0 · `upref.sh` `upper=0/5` · 조건 줄 30 · 기능 조건 20 (자동 포함 여섯 · Anti-patterns 셋 · SC-00 을 뺀 수) — 모두 계약 글자와 같다.

### 2 회차 고칠 것 (필수)

#### C11 — ER-07 예외: 「그 출력에 찍힌 파일」 이 가리킬 출력이 없다

`stale.sh` 첫 줄은 `clean rc=… files=… want=… excluded_line=…` 뿐이고 파일 이름을 찍지 않는다. 글자대로 읽으면 이 계약 파일이 옛 값을 되살려 `rc=1` 이 나와도
「찍힌 파일 가운데 `my` 에 든 것 0」 이 되어 예외로 통과한다. ER-07 뒤에는 `harness/agents/qa-evaluator.md` · `harness/README.md` · 하네스 스킬 둘이
처음 검사 범위에 들어오므로(마켓 등록 폴더 `./harness` — 지금 `SOURCE_DIRS` 에는 `harness/docs/guides` · `harness/references` 뿐) 실제로 일어날 수 있는 경우다.

- ER-07 예외 첫 문장을 이렇게 바꾼다. 뒤 문장(「이때도 `files` 와 `want` 가 같고 …」)은 그대로 둔다:
  「예외: (a) 첫 줄의 `rc` 가 1 이면 `cd "$T/E" && python3 scripts/check-stale-values.py` 를 다시 돌려, `되살아난 옛 값 N 건:` 아래 두 칸 들여 쓴 `<파일>:<줄>` 꼴로 찍힌 파일이 `my` 에 하나도 없을 때만 그 `rc` 를 PASS 로 본다 — 다른 계약이 넣은 옛 값이다.」
- 출력 꼴의 근거: `scripts/check-stale-values.py:95-97` (`print(f"  {x['file']}:{x['line']}  …")`)

#### C12 — AR-05 (d): 살아 있는 작업 폴더 대신 끝 판을 읽는다

(d) 는 `verify_seal "$CF"` 와 `find .harness …` 를 공통 정의가 `cd` 한 작업 폴더에서 돈다. 조건 작성 자문(`측정-환경-오염`)은 작업 폴더를 읽는 예외를
ER-03 · DG-05 (d) 둘로 적었는데 (d) 가 셋째다. 작업 폴더에는 커밋 안 된 Final 초안 둘이 있고 kit-followups · final 계약이 같은 때 계약 파일을 쓴다.
이번에 두 곳을 같은 명령으로 세어 보면 작업 폴더 `SEAL_ABSENT 12 · SEAL_OK 67`, `$T/B` `SEAL_ABSENT 10 · SEAL_OK 67` 로 이미 다르다(둘 다 `SEAL_BROKEN` 0).

- AR-05 (d) 를 바꾼다: 「(d) `verify_seal "$T/E/$CF"` 가 `SEAL_OK` 이고 `find "$T/E/.harness" -type f -name 'sprint-contract*.md' -print0 | while IFS= read -r -d '' f; do verify_seal "$f"; done | grep -c '^SEAL_BROKEN'` 이 0 — 봉인 상태는 끝 판 커밋에 든 계약 파일로 잰다」
- 봉인 전 실측 표에 한 줄: 「AR-05 (d) — `$T/B/.harness` 에서 `SEAL_BROKEN` 0 · `SEAL_OK` 67 · `SEAL_ABSENT` 10. 이 계약 파일은 시작 판에 없어 `SEAL_ABSENT` (2 회차 검토 실측)」

### 2 회차 권하는 것 (선택)

- **R8** 개선안 ER-08 끝에 한 문장: 「검증 가이드의 머리 `version` 은 올리지 않고 변경 이력 표에 행을 더하지 않는다 — 그 표의 여섯 행이 모두 `x.y.z` 꼴(`plugin-validation-guide.md:655-660`, 머리 `version: 1.4.0`)이라 새 행이 AP-01 에 걸린다」.
  SK-05 개선안의 「가이드 머리의 `version` 은 올리지 않는다」 는 SK-05 가 고치는 가이드를 두고 한 말이라 1 회차 C1 로 새로 든 이 파일에는 닿지 않는다. 이 가이드는 고칠 때마다 이력 행을 더해 온 파일이라,
  관례대로 행을 더하면 QA 에서 AP-01 로 되돌아온다

VERDICT: CHANGES
