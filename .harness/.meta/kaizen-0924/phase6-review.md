# Phase 6 계약 초안 검토 — kaizen-0924-p06-design-kit

- 대상: `.harness/sprint-contract-kaizen-0924-p06-design-kit.md` (봉인 전 초안, 조건 30 줄 · 기능 조건 20, 파일 sha256 앞 8 자리 `47cb75d4`, 수정 시각 05:27)
- 역할: 카이젠 2026-09-24 Phase 6 REVIEW (사용자 승인 5 단계를 대신하는 독립 검토자)
- 검토 시각: 2026-09-25 05:42 (`date '+%Y-%m-%d %H:%M'` 출력) · 작업 폴더 `HEAD`(지금 가지의 마지막 커밋) = `7925890` (계약의 시작 커밋과 같다)
- 레포 파일은 이 파일 하나만 썼다. 임시 사본과 시험 스크립트는
  `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p6r/` 에 있다.
  시험용 git 저장소(`p6r/rh` · `p6r/rhn` · `p6r/rh0`)는 전부 그 폴더 안에 `git clone --shared` 로 따로 만들었다.
  검토 중 작업 폴더에 새로 생긴 `phase7-review.md` 는 다른 검토자 몫이다

## 결론

고쳐서 다시 내야 한다(CHANGES). 뼈대는 튼튼하다. 계약에서 떼어 낸 도우미 다섯의 지문이 AR-01 ② 와 같고, 내가 따로 만든 예행
저장소에서 `run_all` · `DG05` · `DG06` 을 돌린 값이 계약의 요구값과 한 글자도 다르지 않았다. 처리 배정표 Phase 6 아홉 행은 전부
조건이나 미반영 사유로 다뤄졌고, 고치는 열세 파일은 러닝북 Phase 6 범위(`design-kit/`) 안이다.

막는 이유는 다섯이다. 앞의 셋은 측정 구멍, 뒤의 둘은 내용이다.

1. **공통 정의 없이 돌리거나 zsh 로 돌리면 0 을 기대하는 조건이 조용히 통과한다 (AP-01 · AP-03 · SK-12 · SK-09 · ER-03).**
   러닝북 계약 규칙(「셸 함수에 기대는 측정은 앞에 `type <함수> >/dev/null || exit 2`」)과 Phase 1~3 교차 진단의 「zsh 조용한 0」 그대로다.
   계약은 AR01 · DG01 · DG04 셋에만 막는 줄을 뒀다. 실측(아래 「다시 돌려 본 것」 6 · 7):
   - `common.sh` 없이 `conds.sh` 만 source 한 bash — `AP-03 bare_open_total=0 unclosed_total=0` 이 요구값과 똑같이 나온다(파일 0 개를 읽었다).
     `AP-01 | own=0` 과 `ER-01 … vmiss=0` 도 AP-01 이 읽는 두 값 그대로다
   - zsh 로 두 파일을 source 하면 따옴표 없는 `$RT` 가 한 낱말로 남아 grep 이 파일을 못 찾는다. 옛 표현이 살아 있는 시작 커밋 판에서
     bash `SK-12 old=[1 1 1 3 2 1 1 1 1 1 ]` · zsh `SK-12 old=[0 0 0 0 0 0 0 0 0 0 ]`. SK-09 `old` 도 3 → 2(`evals.json` 만 셌다)
   - 이 사용자의 기본 셸이 zsh 라 QA 가 `bash -c` 를 빠뜨리면 그대로 걸린다
2. **SK-08 이 붙여 쓴 숫자(「3개」 · 「5회」)를 못 본다.** 측정 꼴이 `[0-9]+ 개` · `[0-9]+ 회` 라 띄어쓰기가 없으면 잡히지 않는다.
   모의본에 audit-criteria 새 행을 「기존 화면 3개 이상」, design-mockup Step 5 를 「스스로 고치기 최대 5회」 로 바꾼 사본에서
   `SK-08 line=1 screens=[2 |2 ] retry=[3 |3 ]` — 요구값 그대로다. 이 킷의 옛 글이 바로 그렇게 붙여 쓴다(SK-09 가 잡는 「시안 5개」)
3. **DG-05 (c) 가 저장소 전체 검사의 종료 코드를 잰다.** 조건 제목은 「이 Phase 파일을 문제로 가리키지 않는다」 인데
   `sync-docs.py --check-only` · `sync-evals.py --check-only` · `validate-doc-contracts.py` 는 모든 킷을 본다. Phase 5 · 7 이 같은 가지에서
   동시에 움직이므로 남의 킷이 어긋나면 이 조건이 떨어진다. DG-06 처럼 남의 몫을 가르는 문장이 없다. `sync-docs.py` 는 킷 이름을 받고,
   나머지 둘은 출력에서 design-kit 을 가리키는 줄을 세면 된다(아래 「고칠 문구」 DG-05 — 실측 값 붙임)
4. **근거 파일과 다른 선택을 했는데 이유를 안 적었다 (ER-03 · design:P1 · design:P7).** 근거 파일 §2 P7 · §4-1 · §4-8 은 같은 역할
   기존 화면이 모자라거나 관례 표가 없으면 `[미검증]` 으로 두라고 했다. 계약은 design-reviewer 규칙 7 의 「대상 코드에 해당 요소 부재」
   를 쓴다. 이 선택 자체는 맞다고 본다 — 규칙 8.2 가 `[미검증]` 을 검증 도구·환경이 없을 때만 쓰게 하고 규칙 8.3 이 2 건이면 REJECT 로
   세므로, 화면이 적은 앱이 도구가 멀쩡한데도 이 항목 하나로 REJECT 에 다가간다. 그런데 계약은 `N/A` 를 피한 이유만 적고(ER-03 (c))
   근거 파일의 권고를 왜 따르지 않았는지는 적지 않았다. 이 Phase 의 외부 근거는 그 파일 하나뿐이라, QA 나 교차 진단이 근거와 어긋난다고
   잡을 자리다. 서술 절에 한 문단이면 된다
5. **요소 하나를 지목한 요청의 Change Manifest 틀이 새 규칙을 따르지 않는다 (design:P3 · F01).** 모의본 규약 §2 새 문단은 「같은 줄·같은
   영역의 이웃 요소는 보존 목록에 올린다」 인데, 바로 아래 틀의 보존 줄은 여전히 「같은 요소/영역의 나머지 시각 속성 열거」 이고
   design-mockup Step 5 틀은 「같은 요소의 나머지 시각 속성」 이다. 모델이 실제로 채우는 것은 틀이다. F01 사고가 바로 칩 하나를 옮기라는
   말에 이웃 칩까지 옮긴 것이고, evals id 29 둘째 assertion 도 이웃 칩을 보존 목록에 올리기를 기대한다. 두 틀의 보존 줄에 한 구절씩이면
   된다(실측: 고친 사본에서 두 자리 각 1 · `## Change Manifest` 블록 수 2 그대로)

## 지시한 여섯 가지에 대한 답

| 볼 것 | 판단 |
| --- | --- |
| 조건마다 FAIL 상태를 한 문장으로 | 30 조건 모두 된다. 조건마다 측정 함수가 한 줄을 내고 조건 줄에 그 줄의 요구값이 글자 그대로 있다. 예: SK-06 「`SK06` 출력이 `SK-06 1 1 1 \| 1 \| 1 1 \| ka=2` 가 아니면 FAIL」 · AR-01 「① 이 `unsigned=0 … own=SEAL_OK` 가 아니거나 ② 지문 다섯 중 하나라도 다르면 FAIL — 단 `shared` 가 0 이 아니고 그 커밋이 모두 다른 Phase 서명이면 PASS」 · DG-06 「두 칸 중 하나가 `[ PASS` · `[ SKIP` 이 아니고, `scope-isolation` 위반 목록을 못 읽었거나 거기 이 Phase 서명 커밋이 있으면 FAIL」. 어긋난 곳은 ER-01 하나 — 산문 「열세 파일 각각에서 … URL 이 1 개 이상」 은 파일마다 1 개로 읽히는데 측정은 합계(`new_urls`)를 잰다. 문자 그대로 읽으면 모의본도 FAIL 이다(아래 고칠 문구) |
| 측정이 의도를 재는가 · 대조 · 봉인 전 실측 | 대체로 그렇다. 값을 잠그는 조건은 편집 전 값과 모의본 값, 0 기대 조건(ER-01 · ER-02 · ER-03 · AP-01 · AP-03 · RE-02 · DG-02)은 양성 대조, 커밋 기록 조건(AR-01 · ER-04)은 예행 저장소 음성 대조가 붙어 있다. SK-06 (d) 는 스킬이 가르치는 확인 명령을 틀 블록에 실제로 돌리는 알려진 답(편집 전 0 · 모의본 2)이고, SK-11 은 근거 파일 §3 이 짚은 위반 셋을 `dtcg.py` 가 3 으로 낸다. 문장 삭제 대조도 65 짝이다. 빈 곳은 막는 이유 1 · 2 · 3 |
| 처리 배정표 Phase 6 행 | 아홉 행(`F01` · `F04` · `design:P1` ~ `design:P7`) 전부 다뤘다. `design:P2` 는 부분 반영(방향은 그대로, 어긋난 두 자리만)이고 방향 질문은 notes 의 사용자 확인 목록으로 넘긴다 — 비고 「사용자 확인 필요」 와 맞다. 관련 행 `F02` · `F03` · `F20` · `F25` · `F26` 의 디자인 쪽 몫도 짚었다. 러닝북 Phase 6 추가 과제는 SK-08 과 결정 1 · 2 가 받는다. Phase 5 초안(`p05` 계약 205 줄)이 「대조할 기존 화면 수 2 개 이상 · 상한 3 회 그대로다 — 이 Phase 가 바꾸지 않았다」 고 Phase 6 에 넘긴 것과 숫자가 맞는다. Phase 1 ~ 4 notes 에 design-kit 로 넘긴 줄은 없다(다시 grep 해 0). 빈 곳은 막는 이유 4 · 5 |
| 범위가 러닝북 표 안인가 | 그렇다. 열세 파일이 모두 `design-kit/` 안이다. `docs/design/research-log.md` 는 저장소 맨 위 `docs/` 에 있어(`design-kit/docs/` 에는 없다) Phase 6 범위 밖이므로 notes 로 넘기는 것이 맞다 |
| 공유 파일을 건드리려 하는가 | 건드리려 하지 않는다. AR-01 이 서명 줄 목록(`outside`)과 경로 직접 세기(`unsigned` · `shared`) 두 방식으로 잰다. 예행 사본에 서명 없는 `design-kit/README.md` 커밋을 얹으면 `unsigned=1` 로 잡히는 것을 다시 확인했다 |
| 조건끼리 부딪히는가 | 안 부딪힌다. SK-08 (b) ↔ ER-03 (「같은 역할 기존 화면 N 개」 의 `N` 은 숫자가 아니라 안 잡힌다 — 아래 고친 꼴로도 모의본 값 `2` 하나), SK-09 (a) ↔ SK-10 (새 evals 에 「5개」 없음), RE-01 ↔ SK-07 (감사 행은 정의 줄 꼴이 아니다), AR-02 ↔ SK-12 (audit-criteria 제목 한 줄), AP-01 ↔ ER-04 (notes 의 ``버전: `0.1.0` `` 은 더한 줄에 안 들어간다), ER-02 ↔ SK-10 (새 evals 문장에 `합니다` 꼴 없음) 모두 확인했다. 아래 고칠 문구를 넣어도 새로 부딪히는 곳은 없다 — 틀 고침 뒤 RE-02 `manifest` 는 그대로 2 다 |

## 다시 돌려 본 것

모두 임시 폴더에서 돌렸다.

1. **도우미 떼어 내기** — 계약 `회귀 게이트` 절의 awk 명령을 글자 그대로 돌렸다. 다섯 파일 지문
   `common.sh:1b24d2392e68e433 conds.sh:c357630c274bd5de dtcg.py:ab7473168fd8f9c7 fence.py:dae506ed24cc7822 new-warnings.sh:e485430011be3e1a` —
   AR-01 ② 와 같고, 초안 작성자의 `p6d/k` · `kx` · `kx2` 와도 `cmp` 로 같다. `p6d/mock.py` 의 sha256 앞 16 자리 `8e34f2eff74a478e` 도 계약과 같다
2. **내 예행 저장소 `p6r/rh`** — 작업 폴더를 `git clone --shared` 로 받아 `7925890` 에서 봉인(계약 사본에 `conditions_digest` 기록) → 구현(`mock.py`) →
   `end_sha` → notes(열아홉 문자열) → `end_sha` 덧붙임 다섯 커밋, 모두 서명 줄. `run_all` 스물일곱 줄이 계약 요구값과 전부 같았다
   (`AR-01 unsigned=0 outside=0 mine=13 added_files=0 shared=0 broken=0 own=SEAL_OK` · `ER-04 1111111111111111111` · `SK-10 ids_ok=1 new=28:design-mockup:4:1;29:design-mockup:4:1;30:design-audit:3:1 e25=1` ·
   `ER-01 new_urls=7 miss=0 … vmiss=0 … dmiss=0` · `ER-02 lines=206 k02=0 formal=0 names=0` · `DG-02 md=[0 0 0 0 0 0 0 0 0 0 0 0 ] json=0` 등).
   `DG05` → `DG-05 v=10 bad=0 kitfail=0 rc=[0 0 0 0 ] evals=[Total: 30 passed, 0 failed] stale_rc=0 stale_mine=0`, `DG06` → 두 칸 `[ PASS`
3. **Step 6.2 · 6.5** — 레포의 `sprint-contract/SKILL.md` 명령을 bash 로 돌렸다. `30` · 기능 조건 `20`(복잡 9~20 안) · 헤더 열둘(서술 다섯 접두 일치 ·
   조건 일곱) · 조건 줄은 조건 절에만 · `OK conditions=30` · `OK 미실측 0 건`
4. **측정 커버리지 검출기** — `contract-schema.md` 의 블록 그대로. `UNCOVERED` 셋(SK-10 · ER-04 · AR-02) 모두 195-198 줄에 해소 줄이 있다
5. **문장 삭제 대조 일곱 개(내가 고른 것)** — 그 줄 하나만 지운 사본에서 조건 출력이 전부 바뀌었다: SK-03 「넘침은 데이터를 고쳐…」 셋째 1 → 0 ·
   SK-07 design-reviewer 새 항목 `dr=0` · SK-12 design-mockup 크기 쿼리 문장 `mu=0` · SK-06 design-concept 폐기 칸 둘째 칸 0 · SK-05 design-guide
   「§0 관례 표 —」 끝 칸 0 · ER-03 「앱 코드가 아직 없으면」 둘째 0 · SK-04 제품 요구 수준 문장 넷째 0
6. **공통 정의 없이** — 예행 저장소에서 `bash -c '. conds.sh; …'` 로 스물일곱 함수를 돌렸다. `AR-01` · `DG-01` · `DG-04` 는 `DEFS_MISSING`,
   대부분은 요구값과 다른 줄이 나와 떨어지지만 `AP-03 bare_open_total=0 unclosed_total=0` 은 요구값 그대로, `AP-01 | own=0` · `ER-01 … vmiss=0` 은
   AP-01 이 읽는 두 값 그대로다
7. **zsh** — 같은 예행 저장소에서 `zsh -c '. common.sh; . conds.sh; run_all'` 은 종료 코드 0. bash 와 다른 줄은 SK-08 · ER-01 · RE-01 · RE-02 넷뿐이고,
   SK-12 · SK-09 · ER-03 은 bash 와 같은 줄이 나온다(모의본에는 옛 표현이 없어 차이가 안 보인다). 시작 커밋 판(`p6r/rh0`, `end_sha` 를 시작 커밋으로)에서는:

   ```text
   bash  SK-09 old=3 0 | e19=0 0 | keep=1 1 1
   bash  SK-12 old=[1 1 1 3 2 1 1 1 1 1 ] ds=0 0 0 0 …
   zsh   SK-09 old=2 0 | e19=0 0 | keep=1 1 1
   zsh   SK-12 old=[0 0 0 0 0 0 0 0 0 0 ] ds=0 0 0 0 …
   ```

8. **막는 줄 두 개를 넣은 도우미 사본(`p6r/k2`)** — 아래 고칠 문구의 두 줄을 넣고 bash 로 `run_all` 을 다시 돌리면 지문 줄 말고는 값이 모두 같다.
   zsh → `NOT_BASH …` 뒤 종료, `conds.sh` 만 → `DEFS_MISSING …` 뒤 `AP03: command not found` · `AP01: command not found`(PASS 줄이 안 나온다)
9. **SK-08 붙여 쓴 변이** — 막는 이유 2 의 사본에서 지금 꼴은 `screens=[2 |2 ] retry=[3 |3 ]`, 띄어쓰기를 선택으로 바꾼 꼴은 설계 쪽 숫자 `2 3` · `3 5`.
   모의본에서는 두 꼴 모두 `2` · `3` 이고 걸리는 자리 수도 6 · 3 으로 같다
10. **DG-05 좁힌 꼴** — 예행 저장소에서 아래 고칠 문구의 측정이 `rc=[0 0 0:0 0:0 ]`. 양성 대조: `evals.json` 첫 항목의 `skill` 을 없는 이름으로 바꾼 사본에서
    `sync-evals` 칸 `1:1`, design-guide description 을 바꾼 사본에서 `sync-docs.py design-kit --check-only` 종료 코드 1 (두 사본 모두 되돌렸다)
11. **음성 대조 다시** — notes 없이 `end_sha` 가 구현 커밋인 예행 저장소(`p6r/rhn`) `ER-04 0000000000000000000`, 거기에 서명 없는 `design-kit/README.md`
    커밋을 얹고 `end_sha` 를 옮기면 `AR-01 unsigned=1 outside=0 …`
12. **사실 확인** — flutter 규약 시작 커밋 판 Step 0 「같은 역할의 서로 다른 기존 화면 2 개 이상」 · Step 2 「최대 3 회, 이후 사용자」. evals id 19 프롬프트는
    「대시보드 홈 화면 시안 만들어줘」 로 개수가 없어 3 이 맞다. `evals.json` 을 다시 쓴 결과 지운 줄은 id 19 두 줄뿐이다(들여쓰기 모양이 안 흔들렸다).
    token-principles 새 색 예시는 `components [0.16, 0.45, 0.84]` 와 `hex #2973d6` 이 맞는다. 킷(`skills` · `agents` · `references` · README)에 옛 표현을
    다시 훑었다 — 「Apple HIG 44pt」 는 킷 전체가 이미 AA · AAA 와 갈라 쓰는 말이라 남아도 된다. 배경 표 ① 의 「backend-reviewer 11 건」 은 틀렸다 —
    `grep -o UNVERIFIED_ENV` 이 `backend-reviewer.md` 7 · `backend-audit/SKILL.md` 3 이다

## 고칠 문구 (조건 ID 별)

고친 뒤 바뀐 측정은 봉인 전에 다시 잰다(러닝북 「봉인 전 실측」). 다시 적을 것: AR-01 ② 의 `common.sh` · `conds.sh` 지문, `mock.py` 지문(개선안 초안 절),
봉인 전 실측 표의 SK-01 · SK-05 · SK-08 · DG-05 행, 문장 삭제 대조 표의 SK-01 · SK-05 칸(짝 수), 예행 절의 `DG-05` 줄과 음성 대조 목록.

### 공통 정의 · 모든 조건 (막는 이유 1)

- `common.sh` 둘째 줄(이름 주석 바로 아래 — 떼어 내기 awk 는 첫 두 줄에서 이름을 찾으므로 이름 줄은 첫 줄에 둔다)에:

  ```bash
  [ -n "${BASH_VERSION:-}" ] || { echo "NOT_BASH — bash 로 돌린다 (zsh 는 따옴표 없는 변수를 쪼개지 않아 0 이 조용히 나온다)"; exit 2; }
  ```

- `conds.sh` 셋째 줄(두 주석 줄 아래)에:

  ```bash
  type sect toks added url my >/dev/null 2>&1 && [ -n "${END:-}" ] && [ -n "${T:-}" ] || { echo "DEFS_MISSING — common.sh 를 먼저 source 한다"; return 2; }
  ```

- `회귀 게이트` 절 설명 문단의 「셸 함수에 기대는 측정(`AR01` · `DG01` · `DG04`)은 …」 뒤에 한 문장:
  「`conds.sh` 는 공통 정의가 없으면 함수를 하나도 만들지 않고 `DEFS_MISSING` 을 낸다 — 공통 정의 없이 `AP-03` 이 `bare_open_total=0 unclosed_total=0` 을 그대로 냈다(검토 실측).
  `common.sh` 는 bash 가 아니면 `NOT_BASH` 로 멈춘다 — zsh 에서 SK-12 `old` 가 옛 표현 열 개를 0 으로 냈다(검토 실측)」
- 예행 절 음성 대조 목록에 두 줄: 「zsh 로 source — `NOT_BASH` · 종료 코드 2」, 「`conds.sh` 만 source 한 bash — `DEFS_MISSING` 뒤 `AP03` 이 `command not found`, PASS 줄 없음」

### SK-08 (막는 이유 2)

- `SK08` 의 두 줄을 바꾼다:

  ```bash
  ds=$(grep -rhoE '기존 화면 \**[0-9]+ ?개' $RT | grep -oE '[0-9]+' | sort -u | tr '\n' ' ')
  dr=$(grep -rhoE '스스로 고치기(는)? 최대 [0-9]+ ?회' $RT | grep -oE '[0-9]+' | sort -u | tr '\n' ' ')
  ```

- 산문 (b) 「「기존 화면 N 개」 숫자 집합」 → 「「기존 화면 N 개」(붙여 쓴 「N개」 포함) 숫자 집합」, (c) 「「스스로 고치기 최대 N 회」 숫자 집합」 →
  「「스스로 고치기 최대 N 회」(붙여 쓴 「N회」 포함) 숫자 집합」
- 양성 대조에 하나 더: 「audit-criteria 새 행을 「기존 화면 3개 이상」, design-mockup Step 5 를 「스스로 고치기 최대 5회」 로 바꾼 사본 `screens=[2 3 |2 ]` · `retry=[3 5 |3 ]`
  (고치기 전 꼴은 이 사본에서 요구값 그대로였다)」. 요구값 `SK-08 line=1 screens=[2 |2 ] retry=[3 |3 ]` 은 그대로다

### DG-05 (막는 이유 3)

- 산문 (c) → 「`sync-docs.py design-kit --check-only` · `run-evals.py design-kit` 가 종료 코드 0 이고 `run-evals.py design-kit` 끝 줄이 `Total: 30 passed, 0 failed`,
  저장소 전체를 보는 `sync-evals.py --check-only` · `validate-doc-contracts.py` 는 종료 코드가 0 이거나, 0 이 아니면 출력에서 design-kit 을 가리키는 줄
  (`[design-kit]` 또는 `design-kit/`)이 0 — 다른 Phase 가 같은 가지에서 동시에 움직이므로 남의 킷 어긋남은 이 조건 몫이 아니다(그 출력을 근거에 붙인다)」
- `DG05` 의 `local` 에 `x r` 을 더하고, `for c in 'sync-docs.py --check-only' …` 한 줄을 두 줄로 바꾼다:

  ```bash
  for c in 'sync-docs.py design-kit --check-only' 'run-evals.py design-kit'; do python3 scripts/$c >/dev/null 2>&1; o="$o$? "; done
  for c in 'sync-evals.py --check-only' 'validate-doc-contracts.py'; do x=$(python3 scripts/$c 2>&1); r=$?; o="$o$r:$(printf '%s\n' "$x" | grep -cE '\[design-kit\]|design-kit/') "; done
  ```

- 요구값 `rc=[0 0 0 0 ]` → `rc=[0 0 0:0 0:0 ]` 이고 「셋째 · 넷째 칸은 `:` 뒤가 0 이면 앞 숫자와 무관하게 통과」 를 적는다.
  봉인 전 실측: 예행 `rc=[0 0 0:0 0:0 ]`, 양성 대조 — `evals.json` 한 항목의 `skill` 을 없는 이름으로 바꾼 사본 셋째 칸 `1:1`, design-guide description 을 바꾼 사본
  첫 칸 `1` (「다시 돌려 본 것」 10)

### ER-01 (FAIL 문장)

- 산문 「열세 파일 각각에서 시작 커밋 판에 없던 URL 이 1 개 이상이고(측정이 살아 있다)」 →
  「열세 파일을 파일마다 시작 커밋 판과 비교해 새로 생긴 URL 이 모두 합쳐 1 개 이상이고(측정이 살아 있다)」. 측정은 그대로

### ER-03 · 결정 셋 (막는 이유 4)

- 소제목 `### 결정 셋` 을 `### 결정 넷` 으로 바꾸고 넷째 항목을 더한다:
  「4. **같은 역할 기존 화면이 모자라거나 관례 표가 없을 때 — `[미검증]` 이 아니라 design-reviewer 규칙 7 의 「대상 코드에 해당 요소 부재」 로 적는다.**
  근거 파일 §2 P7 · §4-1 · §4-8 은 `[미검증]` 을 권했다. 그러나 이 킷의 design-reviewer 규칙 8.2 는 `[미검증]` 을 검증 도구·환경이 없을 때만 쓰고,
  규칙 8.3 은 2 건이면 FAIL 이 없어도 REJECT 다. 비교할 기존 화면이 모자란 것은 도구가 없는 것도, 감사 대상의 결함도 아니라 대조할 관례가 없는 것이다.
  `[미검증]` 으로 두면 화면이 적은 앱이 이 항목 하나로 REJECT 문턱에 다가간다(ER-03)」
- 배경 표 `design:P7` 행 「이번 처리」 끝에 「— 모자랄 때의 처리는 결정 4」 를 덧붙인다

### SK-01 · SK-05 (막는 이유 5)

- `mock.py` 에 두 치환을 더한다(각각 시작 커밋 판에 한 번만 있다 — 검토 grep):
  - 규약 `- 보존: [같은 요소/영역의 나머지 시각 속성 열거 — background, fill, radius, shadow, spacing, typography 중 해당분]` →
    `… typography 중 해당분 · 요소 하나를 지목했으면 같은 줄·같은 영역의 이웃 요소와 그 자리]`
  - design-mockup Step 5(앞 공백 두 칸) `- 보존: [같은 요소의 나머지 시각 속성 — background / fill / radius / shadow / spacing / typography 중 해당분]` →
    `… typography 중 해당분 · 요소 하나를 지목했으면 같은 줄·같은 영역의 이웃 요소와 그 자리]`
- SK-01 산문 끝 「요소 하나 지목 문장과 이웃 요소 보존 문장이 각 1 건이다」 → 「요소 하나 지목 문장과 이웃 요소 보존 문장, Change Manifest 틀 보존 줄의 이웃 요소 구절이 각 1 건이다」.
  `SK01` 의 `b=` toks 에 셋째 인자 `'요소 하나를 지목했으면 같은 줄·같은 영역의 이웃 요소와 그 자리'` 를 더하고 요구값 `b=1 1` → `b=1 1 1`
- SK-05 (c) 에 「틀 보존 줄의 이웃 요소 구절 1」 을 더하고, `SK05` 의 Step 5 toks 끝에 같은 인자를 더해 요구값 `| 1 1 0 |` → `| 1 1 0 1 |`
- 두 줄의 문장 삭제 대조를 다시 돌려 짝 수를 SK-01 12 · SK-05 10 으로 적는다. 검토 실측: 고친 사본에서 두 자리 각 1, 모의본 0, RE-02 `manifest` 2 그대로 (`p6r/tpl.sh`)

### 배경 표 ① (사실)

- 「`design-reviewer.md` 의 `UNVERIFIED_ENV` 0 건(backend-reviewer 11 건)」 → 「… 0 건(backend-reviewer 7 건 · backend-audit 3 건)」

## 막지 않는 것 (넣으면 좋다)

1. design-concept Step 7 에 폐기 칸을 더하면서 그 칸을 읽는 자리가 없다. 결정 3 이 말한 「기록만 두면 아무도 안 읽는다」 가 컨셉 쪽에 그대로 남는다.
   design-concept Step 0 감지 목록에 `.design/approvals/*-concept.md → 폐기한 컨셉 안 로드` 한 줄, Step 7 확인 명령에
   `grep -c '^- 폐기한 대안·이유:' … # → 1` 한 줄이면 design-mockup 과 짝이 맞는다
2. mockup-guidelines 「44×44 이상」 에서 단위가 빠졌다. 킷의 다른 자리는 「44×44 CSS px」(AAA) 와 「Apple HIG 44pt」 로 가른다
3. mockup-guidelines 개수 문장이 숫자(3 · N · 5)를 한 자리 더 적는다. 근거 파일 §2 P2 추론은 숫자는 한 곳에 두고 나머지는 가리키라는 것이다.
   「개수는 `SKILL.md` Step 3-a 를 따른다」 로 줄이면 숫자가 서로 어긋날 자리가 하나 준다(SK-09 (b) 인자도 함께)
4. 규약 머리의 결정 줄 뒤 「그 절이 생기기 전까지는 …」 앞에 「그 절은 아직 없다 — 다음 사이클 Phase 1 이 만든다」 를 적으면 읽는 사람이 헛걸음하지 않는다
5. 규약 머리는 「여기 정의된 임계값·용어를 자기 문서에서 다시 정의하지 않는다」 인데 「2 개 이상」 · 「3 회」 가 스킬 · 감사 다섯 자리에 다시 적힌다.
   SK-08 이 이번 한 번은 맞춰 보지만 다음 변경 때 막을 장치는 없다. notes 다음 사이클 메모에 적는다
6. 배경 표 「카이젠 Gotcha 8」 행: Phase 1 이 바꾼 agent 가이드 §10 의 `[미검증:ENV]` · `[미검증:INVALID]` 분류도 ① 과 같은 일이라 함께 넘긴다고 적고,
   §3.7 네 칸 넘김이 notes 에 반드시 남도록 ER-04 문자열에 하나(예: `§3.7 네 칸`)를 더하면 좋다
7. design-mockup Step 5 의 「§2」 · 「§3」 는 어느 문서의 절인지 그 줄에 없다(위 Gotcha 15 에만 규약 경로가 있다). 경로를 한 번 적으면 헷갈림이 준다

VERDICT: CHANGES

## 2 회차

- 대상: 같은 계약 초안(조건 30 줄 · 기능 조건 20, 파일 sha256 앞 8 자리 `77892a3e`, 수정 시각 05:59)과 개선안 `p6d/mock.py`(sha256 앞 16 자리 `0ec137c2ed0469bb`)
- 검토 시각: 2026-09-25 06:10 (`date '+%Y-%m-%d %H:%M'` 출력). 지금 가지 `HEAD` 는 `6a49ea5` 로 Phase 7 커밋 넷이 얹혔다 —
  그 가운데 `design-kit/` 을 건드린 커밋 0 · 공유 파일(AR-01 `shared` 목록)을 건드린 커밋 0, `validate-post-kaizen.py --since 7925890…` 두 칸 모두 `[ PASS`
- 레포 파일은 이 파일 끝에 이 절만 덧붙였다. 임시 사본 · 시험 저장소는
  `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p6r2/` 에 따로 만들었다(초안 작성자의 `p6d2/` 를 쓰지 않았다)

### 2 회차 결론

통과(APPROVE). 1 회차에 막은 다섯 가지와 고칠 문구 여섯 곳이 모두 들어갔고, 내가 따로 만든 예행 저장소에서 서른 줄이 조건 요구값과 같았다.
새로 찾은 것은 셋인데 모두 측정 값을 바꾸지 않고 봉인 전에 서술 · 모의본 한 줄씩으로 고칠 수 있어 막지 않는다(아래 「봉인 전에 넣을 것」).
BUILD(구현 역할)가 봉인 전에 셋을 넣기를 권한다.

### 1 회차 요구가 들어갔는지

| 1 회차 요구 | 들어간 자리 | 확인 |
| --- | --- | --- |
| 막는 이유 1 — zsh · 공통 정의 없이 돌리면 0 이 조용히 나옴 | `common.sh` 둘째 줄 `NOT_BASH` · `conds.sh` 셋째 줄 `DEFS_MISSING` · 설명 두 문장(238-239 줄) · 음성 대조 두 줄(636-637 줄) | zsh 로 source → `NOT_BASH`, 종료 코드 2. `conds.sh` 만 source 한 bash → `DEFS_MISSING` · source 종료 코드 2 뒤 `AP03` · `AP01` · `ER01` · `run_all` 이 `command not found`, PASS 줄 없음 |
| 막는 이유 2 — SK-08 이 붙여 쓴 숫자를 못 봄 | `SK08` 두 정규식(`[0-9]+ ?개` · `[0-9]+ ?회`) · 조건 (b) · (c) 산문 · 양성 대조 | audit-criteria 새 행 「3개 이상」 · design-mockup Step 5 「최대 5회」 사본 `screens=[2 3 \|2 ] retry=[3 5 \|3 ]`, 규약 `**2 개 이상**` → `**3 개 이상**` 사본 `screens=[2 3 \|2 ]` |
| 막는 이유 3 — DG-05 가 저장소 전체 종료 코드를 잼 | `DG05` 두 반복문 · (c) 산문 · 요구값 `rc=[0 0 0:0 0:0 ]` | design-kit `evals.json` 첫 항목 `skill` 을 없는 이름으로 바꿔 서명 커밋하고 `end_sha` 를 옮긴 사본 `rc=[0 1 1:1 0:0 ]`, design-guide description 한 곳을 바꾼 사본 `rc=[1 0 0:0 0:0 ]`, backend-kit `evals.json` 을 같은 식으로 바꾼 사본 `rc=[0 0 1:0 0:0 ]` — 내 킷 어긋남은 떨어뜨리고 남의 킷 어긋남은 떨어뜨리지 않는다 |
| 막는 이유 4 — 근거 파일과 다른 선택의 이유 | `### 결정 넷` 넷째 항목(52-55 줄) · 배경 표 `design:P7` 행 끝 | 인용한 규칙 8.2(도구·환경 부재 전용) · 8.3(2 건이면 REJECT)이 시작 커밋 `design-reviewer.md` 20-45 줄과 같다 |
| 막는 이유 5 — Change Manifest 틀 보존 줄 | `mock.py` 두 치환(82 · 157 줄) · `SK01` `b=` 셋째 인자 · `SK05` Step 5 넷째 인자 · 요구값 `b=1 1 1` · `\| 1 1 0 1 \|` · 삭제 대조 SK-01 12 · SK-05 10 | 두 줄을 각각 지운 사본에서 `b=1 1 0` · `\| 1 1 0 0 \|` |
| ER-01 FAIL 문장 | 686 줄 「파일마다 … 모두 합쳐 1 개 이상」 | 측정(`new_urls` 합계)과 맞는다 |
| 배경 표 ① 사실 | 32 줄 「backend-reviewer 7 건 · backend-audit 3 건」 | 시작 커밋 판 `grep -o UNVERIFIED_ENV` 7 · 3, design-reviewer 0 |
| 다시 적을 값 | AR-01 ② 지문 · `mock.py` 지문 · 편집 전/모의본 표 · 삭제 대조 표 · 예행 절 | 아래 「2 회차에 다시 돌려 본 것」 1 · 2 · 5 와 한 글자도 다르지 않다. DG-02 더한 줄 수 `84 · 16 · 2 · 3 · 5 · 5 · 4 · 5 · 2 · 1 · 4 · 7` · ER-02 `lines=212` 도 같다 |
| 막지 않는 것 1 · 2 · 3 · 5 · 6 · 7 | design-concept Step 0 두 줄과 Step 7 확인 명령(SK-06 (b)) · 「44×44 CSS px」 와 「Apple HIG 44pt」 구분 · 개수 문장 → Step 3-a 참조(SK-09 (b)) · ER-04 `임계값 다시 정의` · Gotcha 8 행과 ER-04 `§3.7 네 칸` · Step 5 에 규약 경로 한 번 | 새로 잰 토큰 다섯(컨셉 Step 0 두 줄 · 컨셉 확인 명령 · 개수 참조 문장 · AA 24×24 문장)의 줄을 지운 사본에서 해당 조건 출력이 모두 바뀌었다 |
| 막지 않는 것 4 | 「그 절은 아직 없다」 만 넣고 카이젠 차례 이름은 뺐다 | 받아들인다 — 킷 파일은 다른 프로젝트에서 읽힌다 |

### 2 회차에 다시 돌려 본 것

1. **도우미 떼어 내기** — 도우미 정의 절의 awk 를 글자 그대로 돌렸다(`p6r2/extract.sh`). 지문
   `common.sh:64f32d049a33c4a8 conds.sh:5fe82e178530b978 dtcg.py:ab7473168fd8f9c7 fence.py:dae506ed24cc7822 new-warnings.sh:e485430011be3e1a` — AR-01 ② 와 같다
2. **내 예행 저장소 셋** — 작업 폴더를 `git clone --shared` 로 받아 `7925890` 에서 시작했다(`p6r2/reh.sh`). 초안과 겹치지 않게 봉인 지문은 python `hashlib` 으로
   따로 계산했고, notes 는 스물한 문자열을 한 줄에 하나씩 적는 다른 꼴로 썼다.
   `rh`(봉인 → 구현 → `end_sha` → notes → `end_sha` 덧붙임, 모두 서명 줄) 의 `run_all` · `DG05` · `DG06` 서른 줄이 조건 요구값과 같다(줄 끝 공백은 아래 2 번).
   `rh0`(시작 커밋) 의 SK-01 ~ SK-12 · ER-03 · RE-01 · RE-02 · AP-04 가 편집 전 열과 같고, `rhn`(notes 없음) 은 `ER-04 000000000000000000000` · AR-01 ① 요구값이다.
   ER-04 요구값 네 곳(622 · 694 · 695 · 634 줄)의 자리 수는 모두 21 이다
3. **`/bin/bash` 3.2.57** — 같은 `rh` 에서 `run_all` · `DG05` · `DG06` 출력 파일이 5.3.9 판과 `diff` 0 이다. QA 가 옛 bash 로 돌려도 값이 같다
4. **Step 6.2 · 6.5 와 측정 누락 검출기** — 레포 `sprint-contract/SKILL.md` 명령을 bash 로: `30` · 기능 조건 `20` · 둘째 단계 제목 열둘 · 조건 줄은 조건 절에만 ·
   `OK conditions=30` · `OK 미실측 0 건`. `contract-schema.md` 732 줄 절의 검출기 블록 그대로 → `UNCOVERED` 셋(SK-10 · ER-04 · AR-02), 205-207 줄에 해소 줄이 있다
5. **문장 삭제 대조** — 초안의 `p6d2/dt3-out.txt` 76 행을 셌다. CHG 74 · SAME 2, 조건별 CHG 수가 표(12 · 5 · 6 · 4 · 10 · 8 · 5 · 1 · 1 · 5 · 12 · 5)와 같다.
   SAME 두 행은 `dt3.tsv` 에서 SK04 ↔ design-mockup 159 줄, SK06 ↔ 규약 206 줄 — 각 조건이 읽지 않는 파일의 줄이라 계약 설명(597-598 줄)과 맞는다.
   이번에 새로 잰 토큰은 내 사본으로 따로 지워 봤다(`p6r2/deltest.sh` — 위 표의 「막는 이유 5」 행과 「막지 않는 것 1 · 2 · 3 · 5 · 6 · 7」 행)

### 봉인 전에 넣을 것 (막지 않는다 — 측정 값이 안 바뀐다)

1. **evals id 28 프롬프트가 역할이 다른 화면을 비교 대상으로 준다.** 「그룹 설정 화면」 을 만들라며 「멤버 목록 화면」 · 「초대 화면」 이 있다고 한다.
   §0 새 규칙은 관례를 **같은 역할**에만 맞추라고 하고(근거 파일 §2 P7), 설정 화면과 목록 · 초대 화면은 역할이 다르게 읽힌다. 규칙을 따른 답은
   `관례 없음 — 같은 역할 기존 화면 N 개` 를 쓰게 되어 셋째 assertion(「같은 역할의 서로 다른 기존 화면 2 개 이상을 읽고 … 관례 표를 남긴다」)에 떨어진다.
   이 Phase 의 중심 규칙을 흐리는 사례라 고치는 것이 맞다. `mock.py` 314 줄
   `앱에 멤버 목록 화면이랑 초대 화면이 이미 있어` → `앱에 프로필 설정 화면이랑 알림 설정 화면이 이미 있어`.
   실측: 바꾼 사본(`p6r2/mock-alt.py`, sha256 앞 16 자리 `aed436d274a907a1`)을 적용한 저장소에서 SK-05 · SK-09 · SK-10 · ER-02 · DG-02 출력이 그대로다.
   계약은 132 줄의 `mock.py` 지문만 바꾸면 된다
2. **줄 끝 공백.** `toks` 가 값마다 뒤에 공백을 붙여 SK-04 · SK-05 · SK-07 · SK-11 · SK-12 출력 끝에 공백이 하나 남는데, 조건 줄 요구값에는 없다
   (AR-01 ② 만 끝 공백까지 적었다). QA 가 `[ "$(SK04)" = 'SK-04 1 1 1 1' ]` 처럼 글자 그대로 비교하면 잘못된 FAIL 이 나고, 봉인 뒤라 개정 파일로만 풀린다.
   도우미 블록 밖, 239 줄 뒤에 한 문장: 「출력 줄 끝의 공백은 비교하지 않는다 — `toks` 가 값마다 뒤에 공백을 붙인다(SK-01 `b=` · SK-04 · SK-05 · SK-07 ·
   SK-11 · SK-12). AR-01 ② 는 끝 공백까지 적었다」. 도우미 지문은 안 바뀐다
3. **결정 2 가 SK-08 이 재지 않는 줄을 SK-08 몫이라고 적는다.** 45-46 줄 「이 결정 한 줄과 「한쪽 값을 바꾸면 다른 쪽도 같이 바꾼다」 를 둔다(SK-08)」 인데
   SK-08 (a) 는 결정 줄만 잰다. 규약 머리의 `그 절은 아직 없다 — 생기기 전까지는 한쪽 값을 바꾸면 다른 쪽도 같이 바꾼다.` 줄을 지운 사본에서 `SK08` 출력이
   그대로였다(실측). 조건 줄을 늘리지 말고 「(SK-08)」 을 「(결정 줄은 SK-08 (a) 가 잰다. 같이 바꾼다는 줄은 재지 않는다 — `mock.py` 가 글자 그대로 넣는다)」
   로 바꾸면 서술과 측정이 맞는다

### notes 다음 사이클 메모로 넘길 것

1. `SK08` 정규식이 조사 붙은 꼴 「기존 화면이 N 개 미만」 을 세지 않는다. 새 글의 세 자리(규약 §0 · audit-criteria 새 행 · design-reviewer 새 항목)가 그 꼴이다.
   모의본에서는 모두 2 라 이번 판정은 맞다. 지금 고치면 `conds.sh` 지문과 AR-01 ② 를 다시 재야 하므로 notes 의 `임계값 다시 정의` 메모에 한 줄로 붙인다
   (다음 사이클 정규식 후보 `'기존 화면이? \**[0-9]+ ?개'` — 실측: 모의본에서 아홉 자리 모두 2)
2. token-principles 새 줄 「Figma 쪽 hex 병기 관행은 `SKILL.md` Gotcha 12 를 따른다」 가 가리키는 design-system Gotcha 12 에는
   「Figma Variables는 OKLCH 미지원」 이 그대로 남는다. 계약 리서치 소스 절은 Figma 의 OKLCH 지원을 확인하지 않아 강하게 쓰지 않는다고 적었다.
   token-principles 에서 지운 단정을 다른 파일을 가리키는 방식으로 남긴 꼴이라, 다음 사이클 근거 파일 조회 목록에 넣는다

VERDICT: APPROVE
