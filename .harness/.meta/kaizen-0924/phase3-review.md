# Phase 3 계약 초안 검토 — kaizen-0924-p03-evaluator

- 대상: `.harness/sprint-contract-kaizen-0924-p03-evaluator.md` (봉인 전 초안, 조건 28 줄 · 기능 조건 18, 파일 내용 지문 sha256 `72ec9704…`)
- 역할: 카이젠 2026-09-24 Phase 3 REVIEW (사용자 승인 5 단계를 대신하는 독립 검토자)
- 검토 시각: 2026-09-24 23:28 (`date '+%Y-%m-%d %H:%M'` 출력) · 작업 폴더 `HEAD` = `165c8d5` (계약의 시작 커밋과 같다)
- 레포 파일은 이 파일 하나만 썼다. 임시 사본과 시험 스크립트는
  `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p3review/` 에 있다.
  검토 전후로 작업 폴더 `git status --short` 가 같다 (알려진 답 시험용 git 저장소는 임시 폴더에 따로 만들었다)

## 결론

고쳐서 다시 내야 한다(CHANGES). 뼈대는 튼튼하다. 조건 28 개 모두 실패 상태를 한 문장으로 쓸 수 있고, 계약에서 기계로 떼어 낸
공통 정의로 봉인 전 실측 값을 다시 돌려 편집 전 · 모의본 양쪽이 계약 표와 같게 나왔다. 처리 배정표 Phase 3 네 행과
Phase 2 넘김 아홉 행은 전부 조건이나 넘김으로 다뤄졌고, 고치는 파일 다섯은 러닝북 Phase 3 범위 안이다. 문장 삭제 대조도 했다.

막는 이유는 넷이다.

1. **SK-04** — 새 규칙이 가르치는 `git status --porcelain` 문구가 알려진 답과 어긋난다. 「`D` 가 든 줄」을 글자 그대로 읽으면
   경로에 대문자 `D` 가 든 줄(`README.md` · `CLAUDE.md`)까지 잡는다. 이번 Phase 가 넣는 ⑤ 「효과 증명」을 규칙 자신의 명령이 못 지난다
2. **AR-05** — `### 판정 엄격도` 의 기존 규칙(1 · 3 · 5 · 7 · 9 · 11 · 12 · 13 항)을 느슨하게 고쳐도 AR-05 가 통과한다.
   이 스프린트가 바로 그 구간에 문단을 더하므로, 「판정 임계는 건드리지 않는다」는 주장을 재는 측정이 그 구간을 덮어야 한다
3. **SK-01** — ④ 「셸 코드면 zsh · bash 양쪽」이 첫 줄 `#!` 나 호출부로 bash 에 고정된 스크립트까지 zsh 로 돌리게 하고, 판정
   문단이 「결함이 드러나면 FAIL」이라 옛 계약의 멀쩡한 bash 스크립트가 FAIL 을 받는다. 카이젠 스킬 Gotcha 「평가 루브릭 변경 시
   기존 계약과의 호환성 검증 필수」를 계약이 다루지 않았다
4. **ER-03** — `.harness/` 안 공유 파일(러닝북이 금지한 `.harness/.meta/orchestrator-audit-log.md` ·
   `.harness/.meta/kaizen-failure-count.yaml`, Phase 4 범위인 `.harness/project.yaml`)을 재는 조건이 없다. AR-06 ② 는 `.harness/`
   전체를 통과시킨다. 이 Phase 의 SK-05 가 그 감사 로그의 메타 이슈 3 을 인용하므로 「해결」 표시를 하러 들어갈 여지가 실제로 있다

## 지시한 여섯 가지에 대한 답

| 볼 것 | 판단 |
| --- | --- |
| 조건마다 FAIL 상태를 한 문장으로 | 28 조건 모두 된다. 예: SK-01 「토큰 아홉 개 가운데 하나라도 `### 판정 엄격도` 구간에서 1 건이 아니면 FAIL」 · DG-06 「`scope-isolation` · `doc-contracts` 줄이 FAIL 이고 뒤따르는 대조가 이 Phase 서명 커밋을 가리키면 FAIL」. N/A 다섯은 각각 재는 명령이 붙어 있다 |
| 측정이 의도를 재는가 · 대조 · 봉인 전 실측 | 대체로 그렇다. 0 기대 조건(ER-01 · ER-02 · AP-01 · AP-03 · RE-02 · DG-02 · DG-05)은 양성 대조가, 값을 잠그는 조건은 편집 전 값이 붙어 있다. 문장 삭제 사본 45 개도 있다. 다만 AR-05 는 음성 대조가 판정 규칙 1 항 변이 하나뿐이라 판정 엄격도 구간의 느슨화를 못 잡는다(막는 이유 2). SK-04 는 문구가 있다는 것만 재고 그 문구의 명령이 맞는지는 안 잰다(막는 이유 1) |
| 처리 배정표 Phase 3 행 | 넷 전부 — `harness:P04`(SK-01 · SK-02) · `user-setup:P4`(앞 셋은 SK-01 로 합침 · 삭제 열거는 SK-04) · `F16`(SK-01) · `F31`(측정 스크립트 부분 SK-01 ⑤ · SK-03 · SK-04, UI 관례 대조는 행 비고대로 Phase 5). `harness:P08` 의 평가자 쪽도 SK-06 이 받는다. Phase 2 넘김 아홉 행은 AR-01 (a)(b)(c) · AR-02 (b)(c)(d) · AR-03 (a) · SK-06 으로 하나씩 맞는다. 러닝북 Phase 3 추가 과제 다섯 항목과 메타 이슈 3 도 SK-01 ①~⑤ · SK-05 가 받는다 |
| 범위가 러닝북 표 안인가 | 그렇다. 평가자 · 평가 가이드 · `harness/evals/kaizen/evaluator-kaizen/` 의 회귀 확인 파일 셋(러닝북 「시험 픽스처」). 다른 Phase 소관(설계 가이드 · `contract-schema.md` · `harness/skills/` · `scripts/` · `.github/`)은 ER-03 넘김으로 돌렸다 |
| 공유 파일을 건드리려 하는가 | 건드리려 하지 않는다. 루트 README · CLAUDE.md · `marketplace.json` · 킷 `plugin.json` · `docs/` 는 AR-06 ② · SC-00 · ER-03 이 재고 있다. 빈 곳은 `.harness/` 안 공유 파일뿐이다(막는 이유 4) |
| 조건끼리 부딪히는가 | 조건끼리는 안 부딪힌다 — AP-01 ↔ AR-02 (c)(설계 가이드 버전 두 값을 빼는 처리), RE-02 ↔ AR-03(표 추가 없이 행만), AR-05 ↔ SK-01(새 FAIL · `[미검증:INVALID]` 는 기존 판정 규칙 3 · 4 항에 들어간다), SK-05 ↔ 규칙 10 (c)(대체 측정은 늘 엄격해지는 쪽이라는 설명이 모의본에 있다) 모두 확인했다. 규칙 쪽에서 ④ 범위가 호환성 Gotcha 와 부딪힌다(막는 이유 3) |

## 다시 돌려 본 것

계약 본문의 코드 블록 넷을 기계로 떼어 내고(`blk1.bash` 의 `AM=` 줄만 `end_sha: 165c8d5…` 를 담은 가짜 개정 파일로 바꿈),
편집 전은 `$END` = 시작 커밋, 모의본은 `p3draft/mock/` 다섯 파일을 `$T` 에 덮어 같은 측정을 돌렸다.

```text
                         편집 전                                      모의본
SK-03                    0 · 0 · 0 · 2                                1 · 1 · 1 · 2
SK-05 (a)                0 0 0 0 0                                    1 1 1 1 1
SK-06                    0                                            1
AR-02 (a) · (c)          0 · 0 0 0 0                                  2 · 1 1 1 1   (SV=1.6.0 AV=1.7.0 CV=v5.1 SCV=v5.5, SCV 한 줄)
AR-04 (a)                키 넷 · 1 · Agent\(general-purpose\)          키 다섯 · 0 · cross_diagnosis_by: pending-parent
AR-04 (b)                False · 0                                    True · 3
AR-05                    same:12 same:40 same:62 same:82 rule2-same   같음
AP-01 · AP-03 · RE-02    0 · bare 0 unclosed 0 · EV=8 QG=27           같음
ER-01                    0 (새 URL 없음)                              0 (새 URL 넷 전부 근거 파일에 있음)
ER-02                    0                                            0 · 양성 대조 C.UTF-8 2 · C 1 (계약과 같음)
DG-07                    … vacuous-zero#1:0 · min 0 n 5               … silent-check#2:1 · min 1 n 8
```

- DG-05 (b) 양성 대조(계약에 없던 것): 모의본 가이드 사본 끝에 등록된 옛 값 「다섯 가지 에이전트」를 넣고
  `check-stale-values.py` 를 사본 폴더에서 돌리면 종료 코드 1 · 이 Phase 경로 줄 1. 측정이 살아 있다
- DG-06: `validate-post-kaizen.py:581-588` 의 출력 형식으로 가짜 FAIL 출력을 만들어 계약의 `awk` 가 커밋 번호를 뽑는 것을
  확인했다. `validate-doc-contracts.py:250` 의 `검사:` 줄 형식도 계약의 `awk -F' → '` 와 맞는다
- 판정 분포(카이젠 Gotcha 「severity 편향 방지」): 피드백 파일 이름의 시각 순 최근 10 건 APPROVE 9 · REJECT 1, 최근 30 건 26 · 4 —
  계약에 적힌 값과 같다
- 모의본이 인용한 사실 셋을 원 기록과 대조했다: 3217 개 삭제(데이터 풀 `9a0d4163` · 2026-09-14), 계약 16 개를 봉인 없음으로 분류
  (`1a3bcba6-2026-09-24T101420` 피드백 42 행), `경로:13:8` 열 번호 혼동(`phase2-notes.md:71`, Phase 1 계약 보조 스크립트) — 모두 맞다.
  `contract-schema.md` §셸 이식성 규약 · §양성 대조 · §알려진 답 대조, `contract-design-guide.md` §0 이 아닌 기대값,
  `skill-design-guide.md` §3.7 · Parity 16 행도 실제로 있다

## 막는 이유별 실측과 고칠 문구

### SK-04 — `git status --porcelain` 문구가 알려진 답과 어긋난다

알려진 답 시험(`p3review/ka-del.sh`): 임시 git 저장소에 파일 셋을 커밋하고, 커밋 하나로 `gone.txt` 를 지우고, 커밋하지 않은 채
`gone2.txt` 를 지우고 `README.md` 를 고치고 `NewDoc.md` 를 새로 만든다. 답은 구간 삭제 `gone.txt` 하나, 미커밋 삭제 `gone2.txt` 하나다.

```text
                                                      bash               zsh
git diff --name-status --diff-filter=D base..top      gone.txt           gone.txt
git status --porcelain | grep -c D  (문구를 글자대로)  3                  3      ← README.md · NewDoc.md 까지 잡음
git status --porcelain | grep -E '^(D.|.D) '           gone2.txt          gone2.txt
```

이 레포에서는 고친 `README.md` · `CLAUDE.md` 를 알리는 줄(상태 칸 `M`)이 늘 걸린다. 그러면 「선언 밖 삭제 → 사용자 확인 필요」가 매 평가 쏟아진다.

고칠 문구:

- 모의본 두 파일(평가자 Step 2 삭제 열거 첫 불릿 · 가이드 §삭제 열거 첫 불릿)의
  「`git status --porcelain` 에서 `D` 가 든 줄도 함께 뽑는다」 →
  「`git status --porcelain` 줄의 앞 두 글자(상태 칸)에 `D` 가 있는 줄도 함께 뽑는다 (`grep -E '^(D.|.D) '` — 경로에 든 `D` 는 세지 않는다)」
- SK-04 (a) 셋째 토큰 `` `git status --porcelain` 에서 `D` 가 든 줄 `` → `` 앞 두 글자(상태 칸)에 `D` 가 있는 줄 ``
- SK-04 (c) 에 여섯째 토큰 `` 앞 두 글자(상태 칸)에 `D` 가 있는 줄 `` 을 더하고 「5 값」 → 「6 값」
- SK-04 에 (d) 를 더한다: 「(d) 두 파일의 해당 구간(평가자 `### Step 2` · 가이드 `## 삭제 열거`)에 `grep -E '^(D.|.D) '` 가 각각 1 건 이상이고,
  `회귀 게이트` 절의 `ka-del.sh` 를 `bash ka-del.sh` · `zsh ka-del.sh` 로 돌린 출력이 둘 다 `range=gone.txt worktree=gone2.txt naive=3` 이다」.
  `naive=3` 은 글자대로 읽은 문구가 틀린 답을 낸다는 대조다. 스크립트 본문은 검토자 사본 `p3review/ka-del.sh` 를 그대로 옮기면 된다
  (배열 없음 · 변수 전부 따옴표 · `$var:` 꼴 없음 — 두 셸에서 같은 출력을 실측했다)
- 봉인 전 실측 문구: 편집 전 (d) 첫 두 값 0 · 0, 고친 모의본 1 · 1, 두 셸 출력 위 값. 문장 삭제 대조에 새 토큰을 지운 사본 두 개(평가자 · 가이드)를 더한다

### AR-05 — 판정 엄격도 구간의 느슨화를 못 잡는다

음성 대조(`p3review/m2.sh`): 모의본 평가자 규칙 1 을 `1. **1 FAIL = REJECT (경미하면 예외)**` 로 바꾼 사본에서 AR-05 측정은
`same … rule2-same` 그대로다. 규칙 2 줄과 `## 판정 규칙` 만 재기 때문이다. 이번 스프린트는 `### 판정 엄격도` · `## Red Flags` ·
가이드 `## Evidence Validity Gate` · `## 원칙별 Enforcement 등급` 에 **더하기만** 하므로(모의본 실측: 네 구간 모두 지운 줄 0, 더한 줄
2 · 2 · 62 · 3), 「기존 줄을 바꾸거나 지우지 않았다」를 재면 느슨화가 곧바로 드러난다.

고칠 문구:

- AR-05 조건 끝에 한 문장을 더한다: 「그리고 평가자 `### 판정 엄격도` · `## Red Flags`, 가이드 `## Evidence Validity Gate` ·
  `## 원칙별 Enforcement 등급` 구간은 줄을 더하기만 하고 기존 줄을 바꾸거나 지우지 않는다」
- 측정 뒤에 잇는다: `for p in "EV|### 판정 엄격도" "EV|## Red Flags" "QG|## Evidence Validity Gate" "QG|## 원칙별 Enforcement 등급"; do k=${p%%|*}; h=${p#*|}; printf 'kept:%s ' "$(diff <(sect "$T/$k.0" "$h") <(sect "$T/$k" "$h") | grep -c '^<')"; done`
  → `kept:0 kept:0 kept:0 kept:0`
- 봉인 전 실측 문구: 편집 전 · 모의본 모두 `kept:0` 넷. 음성 대조: 규칙 1 굵은 글씨에 「 (경미하면 예외)」 를 더한 사본은 첫 값
  `kept:1` 이고 기존 측정은 `same:12 … rule2-same` 그대로 — 검토자 실측
- `회귀 게이트` 표 `[AR-05]` 줄의 「줄 수 12:62:82:40」 은 조건 기대값 순서(`same:12 same:40 same:62 same:82`)와 다르다. 표를 조건 순서로 고친다

### SK-01 — ④ 가 해석기가 정해진 스크립트에도 zsh 를 요구한다

모의본 ④ 는 「셸 코드면 zsh · bash 양쪽에서 돌려 읽은 대상 수가 같고 0 보다 크다」 이고, 판정 문단은 「돌려서 결함이 드러나면
그 검사를 대상으로 한 조건은 FAIL」 이다. 첫 줄 `#!/usr/bin/env bash` 이거나 부르는 쪽이 `bash x.sh` 로 고정한 스크립트(이 레포의
훅 · `harness/scripts/commit-guard.sh` — 파일 머리에 「macOS 기본 /bin/bash 3.2 에서도 돌아야 한다」)를 zsh 로 돌리면 대상 수가 달라질 수
있고, 그 차이는 실제로 쓰일 때 생기지 않는다. 옛 계약의 멀쩡한 검사 스크립트가 FAIL 을 받는다. 기존 규칙 10 (5) 의 두 셸 실행은
「문서에 적힌 스니펫」 — 사용자가 셸에 붙여 넣는 것 — 이 대상이라 이런 문제가 없었다. ①②③⑤ 는 검사 자신의 주장(「위반을 잡는다」 ·
「돈다」)의 반례라 옛 계약에 새 요구를 만드는 것이 아니지만, ④ 는 고정 해석기에서는 새 요구가 된다.

고칠 문구:

- 모의본 두 파일의 ④ 끝(평가자 규칙 10 문단의 ④ 괄호 뒤 · 가이드 ④ 불릿 끝)에 한 문장:
  「해석기가 정해진 스크립트(첫 줄 `#!` 이나 부르는 쪽이 `bash` 로 고정)는 그 해석기로만 돌리고 다른 셸 칸은 `해당 없음 (고정 해석기)` 로 적는다 — 두 셸에서 도는 것은 사용자 셸에 붙여 넣는 명령과 `source` 하는 파일이다」
- SK-01 (a) 에 열째 토큰 `해석기가 정해진 스크립트`, (c) 에 아홉째 토큰으로 같은 문자열. 「9 값 전부 1」 → 「10 값 전부 1」, 「8 값」 → 「9 값」.
  검토자 실측: 편집 전 · 지금 모의본 모두 평가자 0 · 가이드 0 이라 새 토큰이다
- `GAP 분석` 의 「구현 후보 옵션」 목록에 넷째 줄: 카이젠 Gotcha 「평가 루브릭 변경 시 기존 계약과의 호환성」 — ①②③⑤ 의 FAIL 은 검사
  자신의 주장의 반례라 옛 계약에 새 요구가 아니고, ④ 는 사용자 셸에서 도는 코드로 좁혀 옛 계약의 고정 해석기 스크립트를 떨어뜨리지 않는다.
  미실행은 평가자 자신의 증거 문제(`[미검증:INVALID]`)라 계약 쪽 부담이 아니다
- `회귀 게이트` 표 `[SK-01a]` · `[SK-01c]` 값과 문장 삭제 대조 표에 새 문장 두 줄(평가자 · 가이드)을 더하고 봉인 전에 돌린다

### ER-03 — `.harness/` 안 공유 파일을 재는 조건이 없다

AR-06 ② 의 허용 정규식은 `^\.harness/` 전체를 통과시키고, ER-03 의 금지 정규식에는 `.harness/` 경로가 없다. 그래서
`.harness/.meta/orchestrator-audit-log.md` 나 `.harness/.meta/kaizen-failure-count.yaml`(러닝북 「Phase 에서 고치지 마라」 목록),
`.harness/project.yaml`(러닝북 표의 Phase 4 범위)을 서명 커밋이 고쳐도 28 조건이 전부 통과한다.

고칠 문구:

- ER-03 조건의 「넘김 대상과 다른 Phase 소관 파일을 하나도 건드리지 않는다」 → 「넘김 대상 · 다른 Phase 소관 파일 · 러닝북이 금지한
  `.harness/` 안 공유 파일을 하나도 건드리지 않는다」
- 셋째 측정 정규식 끝에 더한다: `…|scripts/|\.harness/\.meta/(orchestrator-audit-log\.md|kaizen-failure-count\.yaml)$|\.harness/project\.yaml$)` → 0
- 봉인 전 실측 문구: `my` 빈 목록 0. 가짜 목록(`.harness/.meta/orchestrator-audit-log.md` · 이 계약 · notes)으로 1 — 검토자가 늘린
  정규식 그대로 실측했다. 이 Phase 계약 · 개정 · notes · 검토 · QA 피드백 파일과 평가자 파일을 담은 목록은 0 이다
- `범위 경계` 의 공유 파일 줄에 두 `.harness/` 파일 이름을 더한다

고친 뒤 Step 6.2(조건 줄 28 · 기능 조건 18 그대로여야 한다 — 새 조건 ID 없이 하위 측정만 늘었다) · 6.5 · 측정 커버리지 검출기를 다시
돌린다. 새 `UNCOVERED` 는 `범위 경계` 의 해소 줄에 적는다.

## 고치면 좋지만 막지는 않는 것

- **AR-06 ③** 은 이 계약이 `SEAL_ABSENT` 여도 통과한다(`SEAL_BROKEN` 만 센다). 평가자 1-e-2 · 1-e-3 도 봉인 없음 · 봉인 커밋 없음을 경고로만
  둔다. BUILD 가 6.6 · 6.7 을 빠뜨리면 아무 조건도 떨어지지 않는다. ③ 에 `verify_seal .harness/sprint-contract-kaizen-0924-p03-evaluator.md | cut -d' ' -f1`
  이 `SEAL_OK` 를 더하면 막힌다
- **SK-03** 의 `awk` 는 질문 1 이 두 줄로 감기면 1 을 낸다(검토자 실측 — 질문 수는 여전히 둘인데 FAIL). 반대로 감긴 질문 2 뒤에 셋째 질문이
  붙으면 세지 않는다. `부모가 물을 두 가지` 다음 줄부터 다음 불릿(줄 머리 `-`) 전까지 번호 줄(정규식 `^ +[0-9]+\.`)을 세면 둘 다 없어진다
- **`범위 경계` 의 `[bash-blocks]`** 「더한 줄 가운데 셸 펜스를 여는 줄 0」 은 조건 줄이 없어 판정되지 않는다. 조건으로 올리거나 「권고」로 적는다
- **삭제 열거**: 이 레포처럼 작업 폴더를 여러 세션이 같이 쓰면 `git status --porcelain` 에 남의 미커밋 삭제가 섞인다. 판정에는 안 닿지만(사용자
  확인 목록으로만 간다) 「경로를 계약 선언과 대조해 남의 것은 그렇다고 적는다」 한 마디가 있으면 확인 목록이 덜 부푼다
- **근거 파일 §4-11** 은 범위 밖 삭제를 FAIL 로 권했다. 계약은 「사용자 확인」 을 골랐다(평가자는 계약에 없는 요구를 만들지 않는다 · 범위
  조건이 있으면 그 조건이 잡는다). 이 선택과 이유를 `GAP 분석` 선택 목록에 남기면 다음 사이클이 되묻지 않는다
- **가이드 SK-05 소절** 의 「두 사이클에 걸쳐 관측한 메타 이슈」 — 감사 로그 원문(`orchestrator-audit-log.md:494-495`)은 「2 회째 관측」 이다. 「두 번 관측한」 이 원문과 맞다
- **카이젠 Gotcha 「L3 Coverage Honesty 회귀 체크」** 측정 기록이 계약에 없다. 검토자 실측: 파일 이름 시각 순 최근 10 건 가운데 `[샘플링-` 태그가 든 것 0 건.
  이것이 「태그 누락」 인지(전수 검증을 주장했는데 실제로는 일부만 봤는지)는 파일만으로 못 가른다. notes 다음 사이클 메모에 값과 판단을 남긴다
- **F31 의 UI 부분**(행 비고대로 Phase 5 `flutter:P-INSPECTOR-convention`)을 notes 「미반영 키와 사유」 칸에 한 줄 적는다 — 러닝북이 notes 에 요구한 칸이다
- **⑤ 와 규칙 12 (3) 의 겹침** — 새 시험 파일이 9 항 대상이면 ⑤ 「알려진 위반 사본」 실행과 규칙 12 (3) 「실행 음성 대조는 선택 · 안전 조건 셋」 이 같은
  일을 가리킨다. ⑤ 는 임시 사본에서만 돌아 제자리 변형 안전 조건과 무관하다는 한 마디가 있으면 평가자가 둘 사이에서 망설이지 않는다

VERDICT: CHANGES

## 2 회차

- 대상: 같은 계약 파일의 고친 판 (599 줄 · 조건 28 · 기능 조건 18, 파일 내용 지문 sha256 `9ceadd77…`). 1 회차가 본 `72ec9704…` 는
  초안 폴더의 `p3draft/contract.v1.md` 와 같은 파일이다
- 검토 시각: 2026-09-24 23:55 (`date '+%Y-%m-%d %H:%M'` 출력) · 작업 폴더 `HEAD` = `165c8d5` (계약의 시작 커밋과 같다)
- 레포 파일은 이 파일 하나만 썼다(끝에 덧붙임). 임시 사본과 시험 스크립트는
  `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p3review2/` 에 있다.
  검토 전후 작업 폴더 `git status --short` 가 같다

### 결론

통과시켜도 된다(APPROVE). 1 회차 막는 이유 넷이 조건 문구 · 측정 · 모의본에 모두 들어갔고, 막지 않는 권고 아홉도 모두 들어갔다.
계약 본문에서 기계로 떼어 낸 코드 블록 일곱(bash 셋 · python 둘 · text 둘, `ka-del.sh` 포함)으로 편집 전 · 모의본을 다시 재면
측정 공통 정의 절의 표와 값이 모두 같다. 새로 막을 결함은 찾지 못했다. 봉인 전에 고르면 좋은 권고 셋을 아래에 적는다.
첫째 권고(AR-05 의 더하기만 하는 느슨화)는 1 회차 검토가 처방한 측정 자체에 남은 빈틈이라 초안 작성자의 잘못이 아니다.

### 1 회차 막는 이유 — 반영 확인

| 막는 이유 | 계약에 들어간 것 | 검토자 실측 |
| --- | --- | --- |
| SK-04 | 모의본 두 파일 문구를 상태 칸 `grep -E '^(D.\|.D) '` 로 교체 · (a) 셋째 토큰 교체 · (c) 여섯째 토큰 · (d) 명령 문자열 + `ka-del.sh` · 문장 삭제 사본 둘 | 편집 전 (d) `0 0` → 모의본 `1 1`. `ka-del.sh` 를 bash 5.3.9 · `/bin/bash` · zsh 로 돌리면 셋 다 `range=gone.txt worktree=gone2.txt naive=3` · 종료 코드 0. 평가자 상태 칸 문장만 지운 사본은 (a) 셋째 0 · (d) 첫 값 0, 가이드 쪽은 (c) 여섯째 0 · (d) 둘째 0. 평가자 문장을 1 회차의 틀린 문구 「`D` 가 든 줄」 로 되돌린 사본도 (a) 셋째 0 · (d) 첫 값 0 |
| AR-05 | 조건 끝 문장 · `removed:` 측정 · 표를 조건 순서(`same:12 same:40 same:62 same:82`)로 고침 · 배경 문단 | 편집 전 · 모의본 `removed:0` 넷. 판정 엄격도 규칙 1 굵은 글씨에 「 (경미하면 예외)」 를 더한 사본은 `removed:1 0 0 0` 이고 옛 측정은 `same … rule2-same` 그대로. Red Flags 기존 줄 「"사소한 차이다" …」 를 지운 사본은 `removed:0 1 0 0` |
| SK-01 | 두 파일 ④ 끝 고정 해석기 문장 · (a) 열째 · (c) 아홉째 토큰 · `GAP 분석` 넷째 선택 · 문장 삭제 사본 둘 | 편집 전 0, 모의본 1. 평가자 문장만 지운 사본은 (a) 열째 0, 가이드 문장만 지운 사본은 (c) 아홉째 0. `GAP 분석` 이 인용한 `harness/scripts/commit-guard.sh` 첫 줄이 실제로 `#!/usr/bin/env bash` |
| ER-03 | 조건 문구 · 셋째 측정 정규식 · `범위 경계` 공유 파일 줄 | 정규식에 한 줄씩 넣으면 감사 로그 · 실패 횟수 파일 · `.harness/project.yaml` · `harness/skills/sprint/SKILL.md` 각 1, `orchestrator-audit-log.md.bak` · `project.yaml.x` · 이 계약 · notes · 평가자 각 0 (끝 고정 `$` 가 묶음 안에서도 먹는다) |

권고 아홉도 전부 들어갔다 — AR-06 ③ 에 이 계약 `SEAL_OK` · SK-03 을 다음 불릿까지 세는 `awk` · `[bash-blocks]` 를 「권고」 로 표시 ·
삭제 열거에 다른 세션 삭제 한 마디(모의본 평가자 `:669` · 가이드 `:702-703`) · 근거 파일 §4 권장안 11 과 다른 선택을 `GAP 분석`
다섯째로 · 가이드 「두 번 관측한 메타 이슈」(모의본 가이드 `:1130`, 감사 로그 `:494` 「2 회째 관측」 과 맞다) · L3 Coverage Honesty
실측과 F31 UI 부분을 notes 지시에 · ⑤ 끝 규칙 12 (3) 무관 문장(두 파일).

### 다시 돌린 것

- 계약 본문의 코드 블록 일곱을 떼어 내고 공통 정의의 `AM=` 줄만 `end_sha: 165c8d5…` 를 담은 가짜 개정 파일로 바꿨다. 편집 전
  (`$END` = 시작 커밋)과 모의본(`p3draft/mock/` 다섯 파일을 `$T` 에 덮음)에서 문서를 재는 조건 전부(SK-01~06 · ER-01 · ER-02 ·
  AR-01~05 · AP-01 · AP-03 · AP-04 · RE-02 · DG-02 · DG-07)를 조건 문구 그대로 돌렸다. 값이 모두 계약 표와 같다. 달라진 것은
  DG-02 의 가이드 더한 줄 130 과 DG-07 의 `false-approve#0:7` 인데 둘 다 계약에 적힌 값이다
- Step 6.2 · 6.5 (sprint-contract `SKILL.md` 명령 그대로): 조건 줄 28 · 기능 조건 18 · `OK conditions=28` · 허용 밖 제목 없음 ·
  서술 절 안 조건 줄 0 · `OK 미실측 0 건`. 커버리지 검출기(`contract-schema.md` §측정 커버리지 표기 원문과 같은 것)의 `UNCOVERED`
  는 다섯(SK-03 · SK-04 · ER-03 · AR-02 · AR-04)으로 `범위 경계` 해소 줄과 같다
- AR-06 ③ 을 지금 작업 폴더에 돌리면 `11 SEAL_ABSENT · 52 SEAL_OK`, 이 Phase 몫 `SEAL_BROKEN` 0, 이 계약 `SEAL_ABSENT` — 봉인 전이라
  맞는 값이고, BUILD 가 봉인을 빠뜨리면 ③ 이 떨어진다
- DG-05: 시작 커밋을 `git archive` 로 푼 사본에 모의본 다섯 파일을 얹고 돌리면 `validate-plugin.py harness` 의 V1 · V6 · V10 OK,
  `check-stale-values.py` 종료 코드 0 「되살아난 옛 값 없음」, `sync-docs.py --check-only` 0, `run-evals.py` 0
- 조건끼리 충돌: AR-05 의 새 측정 네 구간과 다른 조건이 고치는 자리(AR-01 의 `## Binary Decidability Pre-Check` ·
  `### Recurring Improvement Escalation`, AR-02 (d) 의 평가자 `## References`, AR-03 (b) 표 행, SK-01 · SK-05 가이드 소절)는 겹치지
  않는다 — 모의본에서 `removed:0` 넷이고, 가이드 `## Evidence Validity Gate` 에서 새 소절 둘을 뺀 나머지가 편집 전 구간과 글자
  그대로 같다

### 봉인 전에 고르면 좋은 것 (막지 않는다)

1. **AR-05 는 줄을 더해서 느슨하게 만드는 것을 못 잡는다.** 모의본 판정 엄격도 규칙 1 줄 아래에
   「단, 경미한 FAIL 하나는 Improvement 로 내리고 APPROVE 할 수 있다.」 한 줄을 더한 사본은 `removed:0` 넷 · `same … rule2-same` 이고,
   28 조건 가운데 이것을 잡는 조건이 없다. 가이드 `## Evidence Validity Gate` 의 새 소절 바깥에 「공허한 증거라도 경미하면 PASS 로
   본다.」 를 더한 사본도 같다. 더한 줄의 자리와 수를 잠그면 막힌다. AR-05 측정 끝에 잇는 문구:
   `for p in "EV|### 판정 엄격도" "EV|## Red Flags" "QG|## 원칙별 Enforcement 등급"; do k=${p%%|*}; h=${p#*|}; printf 'added:%s ' "$(diff <(sect "$T/$k.0" "$h") <(sect "$T/$k" "$h") | grep -c '^>')"; done; diff <(sect "$T/QG.0" '## Evidence Validity Gate') <(sect "$T/QG" '## Evidence Validity Gate' | awk '/^### (0 이 기대값인데 매치가 나올 때|산출물이 검사일 때)/{s=1;next} s&&/^#{2,3} /{s=0} !s') >/dev/null && echo evg-rest-same || echo evg-rest-diff`
   → `added:2 added:2 added:3 evg-rest-same`. 검토자 실측: 편집 전 `added:0 added:0 added:0 evg-rest-same`, 모의본
   `added:2 added:2 added:3 evg-rest-same`, 판정 엄격도에 한 줄 더한 사본 `added:3 …`, 가이드 새 소절 바깥에 한 줄 더한 사본
   `evg-rest-diff`. 조건 문장은 「평가자 두 구간은 새 문단 두 개 · Red Flags 두 줄만, Enforcement 표는 세 행만 더하고, 가이드
   `## Evidence Validity Gate` 는 새 소절 둘 밖에서 편집 전과 같다」 로 바꾸면 측정과 맞는다
2. **`범위 경계` 의 사용자 승인 대체 줄**은 검토 결과를 1 회차(23:28 · `VERDICT: CHANGES`)까지만 적는다. 봉인 전에 이 2 회차
   (23:55 · 판정)를 함께 적는다. 봉인은 조건 줄만 지문을 뜨므로 나중에 적어도 봉인은 안 깨지지만, 봉인 판에 남는 편이 낫다
3. **SK-03 의 `awk`** 는 줄 머리 `-` 에서만 멈춘다. 질문 목록 바로 뒤가 제목이나 빈 줄로 바뀌면 그 뒤의 들여쓴 번호 줄까지 센다
   (합성 입력 실측 3). 떨어지는 쪽으로만 틀리므로 거짓 PASS 는 없고, 모의본은 다음 줄이 `- 부모가 교차 진단을 마친 뒤` 라 지금 값
   2 가 맞다. `f&&/^-/{f=0}` 를 `f&&/^(-|#)/{f=0}` 로 바꾸면 없어진다

VERDICT: APPROVE
