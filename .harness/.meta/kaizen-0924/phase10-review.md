# 카이젠 2026-09-24 Phase 10 (react-kit) 계약 검토

- 대상: `.harness/sprint-contract-kaizen-0924-p10-react-kit.md` (봉인 전 초안, 687 줄, 조건 29 · 기능 조건 19)
- 개정 파일: 아직 없다 (`.harness/sprint-amendments-kaizen-0924-p10-react-kit.md` 없음 — 봉인 전이라 정상)
- 검토 기준 커밋: `4a8ec55` (작업 폴더 HEAD(지금 가지의 끝 커밋)와 같다. `react-kit/` · `docs/react/` 에 미커밋 변경 없음)
- 검토자: 독립 Claude 검토자 (Codex 대신 — 러닝북 `사용자 승인(5 단계) 대체`)

## 결론

**꼭 고칠 곳은 두 군데다.**

1. **BUILD 에게 주는 확인 값이 틀렸다.** 계약 166 · 167 줄은 `mock.py` 가 「45 치환 · 새 파일 하나」 이고 돌리면 `mock applied 46` 이 나와야 한다고 적었다.
   HEAD 판 새 사본에 실제로 돌리면 `mock applied 45` 가 나온다 — 치환 44 · 새 파일 1 을 합친 수다(`mock applied 45 {'rep': 44, 'new_file': 1}`).
   예행 스크립트가 이 출력을 `/dev/null` 로 버려서 초안이 못 봤다. 이대로 두면 BUILD 가 제대로 적용해 놓고도 값이 다르다며 멈추거나 원인을 찾아 헤맨다.
2. **ER-04 셋째 값이 딱 `1 1` 을 요구한다.** 조건 문장은 「넘김 둘은 사유와 같은 줄에 있다」 뿐인데 기대값은 정확히 한 줄씩이다.
   진짜 notes 는 넘김 줄을 `## 미반영 키와 사유` 와 `## 다음 사이클 메모` 두 곳에 적기 쉽고, 그러면 `2 2` 가 나와 글자대로는 FAIL 이다 — 직접 넣어 봤다(아래 P1).
   Phase 8 검토가 잡은 것과 같은 모양이다. 같은 조건에서 함께 고칠 것: 조건이 「러닝북 여섯 절 제목」 이라며 든 목록에 러닝북이 요구하는 `## 바꾼 파일` 이 빠지고,
   러닝북 목록에 없는 `## 넘기는 것` 이 들어가 있다. 그래서 `## 바꾼 파일` 절이 없는 notes 도 지금 측정을 통과한다.

나머지는 계약대로 돌려 보니 전부 맞았다. 조건 스물다섯의 `m` 출력이 봉인 전 실측 표의 「예행 판」 · 「시작 커밋 판」 칸과 한 글자도 다르지 않았고,
초안이 안 해 본 바꿔치기 열둘도 전부 요구값에서 벗어났다. 처리 배정표 Phase 10 행 여섯과 비고 둘 · 앞 Phase 넘김 셋이 전부 조건이나 미반영 사유로 다뤄졌다.
고치는 파일 열아홉은 전부 `react-kit/` · `docs/react/` 안이고 공유 파일은 건드리지 않는다. 조건끼리 서로 막는 곳도 없다.

`other-kits:P2` 의 「지울지 고칠지」 는 초안의 **「고친다」 에 동의한다.** 지우면 설계 문서 `docs/react/kit-design/final-integration.md:243` · `:482` 가 킷 구성으로 적은 파일이
사라져 문서까지 고쳐야 한다(두 줄 모두 직접 확인). 고치는 쪽은 한 줄과 시험 하나라 되돌리기 쉽고, 근거 파일 §2 에도 반대 근거가 없다.
그 시험이 근거 파일의 최소 수정(`!= "null"`)만으로는 모자란다는 것(jq 경로가 늘 거짓)까지 찾아냈다 — 고치는 편이 맞다.

## 직접 돌려 본 것

전부 내 폴더 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p10r/` 에서 돌렸다.
작업 폴더 파일은 이 검토 파일 말고 건드리지 않았다.

1. **계약 본문과 초안이 돌린 도우미가 같은가.** `## 회귀 게이트` 절의 bash 블록 셋을 `p10r/extract.py` 로 뽑아 초안 폴더 `p10d/k/` 와 `cmp` —
   `same common.sh` · `same m.sh` · `same new-warnings.sh`. 초안 사본 `p10d/contract.draft.md` 와는 `created:` 한 줄만 다르고(07:08 → 07:21), `p10d/contract.saved.md` 와는 같다.
   `mock.py` 지문 앞 16 자리 `20ed60ddd9c76fa2` 는 계약에 적힌 값과 같다. `markdownlint-cli2 --version` 첫 줄 `markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)`.
2. **예행 저장소를 새로 만들어 조건 스물다섯을 전부 다시 쟀다.** 초안의 `rehearse.sh` 를 내 폴더로 옮겨 이 계약 파일로 돌렸다 —
   `rehearsal ready b9a7420 var=none` · `rehearsal base ready (end_sha = 시작 커밋)`. 결과 `p10r/run-e.txt` · `p10r/run-b.txt`. 예:
   - SK-04 → `1` 여섯 · `1 0` · `1` 일곱 · `0` (시작 커밋 판 마지막 값 `8`)
   - SK-08 → `1` 여섯 · `1 1` · `1` 여덟 · `0` · `1` · `build_same=1 build_vitest=0`
   - ER-01 → `1 0 0` · `결과: 6 경우 중 불일치 0` `rc=0` 두 벌 · `결과: 6 경우 중 불일치 4` `rc=1` · `shellcheck=0 bash_n=0` · `mode=100755 fixtures_same=1`
   - AR-01 → `0` · `0 19` · `0` · `SEAL_OK` · `scope_same=1` · `1`
   - DG-05 → `10 0 rc=0` · `tf_mine=0` · `sync_docs_rc=0 1` · `1 0` · `stale_rc=0 0`, DG-06 → `scope-isolation: PASS` · `doc-contracts: PASS` · `doc_checked=2 doc_mine=0` · `violators=0 mine=0`
3. **커밋 기록 조건을 변형 둘에서 다시 쟀다**(`p10r/na.sh`). 변형 없음 · `cross-phase` · `unsigned-shared` 세 저장소:
   - 조건 없는 줄 넷(SC-00 · DG-01 · DG-04)은 셋 다 `SC-00=0 DG-01=0 DG-04=0`
   - `cross-phase` → ER-04 넷째 값 `1` · AR-01 둘째 줄 `1 19` · DG-06 `scope-isolation: FAIL` · `violators=1 mine=1`
   - `unsigned-shared` → ER-04 넷째 값 `1`
4. **`mock.py` 를 HEAD 판 새 사본에 돌렸다.** `git archive HEAD react-kit docs/react` 를 푼 폴더에 `python3 p10d/mock.py` → `mock applied 45`.
   세는 줄을 넣은 사본(`p10r/mock-count.py`)으로 → `mock applied 45 {'rep': 44, 'new_file': 1}`. 새 시험 파일은 `-rwxr-xr-x` 로 생긴다.
5. **초안이 안 해 본 바꿔치기 열둘**(`p10r/probe.sh` 외). 전부 요구값에서 벗어났다 — P1 만 빼고. P1 은 측정이 아니라 기대값이 틀린 경우다.

   | # | 바꾼 것 | 출력 |
   | --- | --- | --- |
   | P1 | notes 끝에 넘김 줄 둘을 다른 절로 한 번씩 더 적음 (진짜 notes 에 흔한 모양) | ER-04 셋째 줄 `2 2` — 요구값 `1 1` 과 달라 FAIL 로 읽힌다 |
   | P2 | 규약 `### 캡처 점검 목록` 을 `## 4.` 앞으로 옮김 | SK-02 둘째 줄 `0` (SK-03 은 `1` 그대로 — 순서는 SK-02 가 잡는다) |
   | P3 | react-skeleton 만 옛 「`[미검증]` 마커와 사유를 붙이고」 로 되돌림 | SK-04 셋째 줄 `1 1 0 1 1 1 1` · 넷째 줄 `1` |
   | P4 | 새 시험의 판정을 늘 일치로 | ER-01 음성 대조 줄 `불일치 0` `rc=0` — 요구 `불일치 4` `rc=1` 에서 벗어남 |
   | P5 | 조사 기록 `## [2026-08-13]` 절 한 줄 고침 | SK-10 `old_rounds_same=0` |
   | P6 | 규약 새 절에 띄어쓰기 없는 제목 한 줄(마크다운 경고 MD018) | DG-02 규약 줄 `new_warnings=1` |
   | P7 | 조사 기록 새 절에 근거 파일 밖 URL | ER-02 `1 0` |
   | P8 | 템플릿 `strictPort: true,` 를 주석으로 | SK-07 첫 줄 `1 0 1` |
   | P9 | react-preflight 옛 성공 줄 `✓ (N passed)` 를 새 줄 옆에 남김 | SK-08 넷째 줄 `1` |
   | P10 | react-screen Gotcha 15 를 16 으로 번호 건너뜀 | SK-06 `000/0-15 …` |
   | P11 | react-run 명령 표 가운데에 문장 한 줄 끼움 | DG-05 (b) `tf_mine=1` (초안 표에 이 값의 양성 대조가 없어 따로 넣어 봤다) |
   | P12 | `docs/react/kit-design/g4-quality.md` 끝에 등록된 옛 값 `shadcn-ui@latest` | DG-05 (e) `stale_rc=1 1` |

6. **멈춤 장치.** zsh 로 `common.sh` 를 읽으면 `NOT_BASH — bash -c 안에서 다시 읽는다` · 종료 코드 2. 개정 파일을 치운 예행 저장소에서는 `END_UNRESOLVED — 측정을 멈춘다. HEAD 로 바꿔 재지 않는다` · 종료 코드 2.
7. **계약 틀 검사.** sprint-contract Step 6.2 두 명령 → `29` · `19`(복잡 9~20 안). 둘째 단계 제목 열둘, 조건 줄은 전부 조건 절 일곱 안(SK 11 · SC 1 · ER 4 · AR 2 · AP 3 · RE 2 · DG 6). `[미실측]` 0 건.

## 꼭 고칠 곳 (조건 ID 별 문구)

### 개선안 초안 절 (조건 줄 밖이라 봉인 값에 안 걸린다)

- 166 줄: `시작 커밋 판에 적용하는 45 치환 · 새 파일 하나 그대로다` → `시작 커밋 판에 적용하는 44 치환 · 새 파일 하나 그대로다`
- 167 줄: ``BUILD 는 `mock.py` 를 작업 폴더에 그대로 돌린다(`mock applied 46` 이 나와야 한다).`` →
  ``BUILD 는 `mock.py` 를 작업 폴더에 그대로 돌린다(`mock applied 45` 가 나와야 한다 — 치환 44 와 새 파일 1 을 합친 수).``

### ER-04

1. `m.sh` 의 `ER-04)` 갈래 `toks` 목록 끝 줄에서 `'## 반영한 처리 배정표 키'` 앞에 `'## 바꾼 파일'` 을 넣는다:

   ```bash
         '## 바꾼 파일' '## 반영한 처리 배정표 키' '## 미반영 키와 사유' '## 넘기는 것' '## changelog 한 단락' '## 킷 로그 한 단락' '## 다음 사이클 메모'
   ```

   새 토큰은 열일곱째라 양성 대조가 가리키는 열한째 `UNVERIFIED_ENV` 자리는 그대로다. 도우미 폴더(`p10d/k/m.sh`)도 계약 블록에서 다시 떼어 낸다.
2. 조건 줄(652 줄) 세 군데:
   - `문자열 스물둘(` → `문자열 스물셋(`
   - ``러닝북 여섯 절 제목 `## 반영한 처리 배정표 키` · `## 미반영 키와 사유` · `## 넘기는 것` · `## changelog 한 단락` · `## 킷 로그 한 단락` · `## 다음 사이클 메모`)`` →
     ``러닝북 여섯 절 제목 `## 바꾼 파일` · `## 반영한 처리 배정표 키` · `## 미반영 키와 사유` · `## changelog 한 단락` · `## 킷 로그 한 단락` · `## 다음 사이클 메모` 와 넘김 절 제목 `## 넘기는 것`)``
   - `넘김 둘은 사유와 같은 줄에 있고(` → `넘김 둘은 사유와 같은 줄에 각각 1 줄 이상 있고(`
3. 측정 괄호(653 줄):
   - `` `m ER-04` 네 줄이 `notes_committed=1` · `1` 이상 스물둘 · `1 1` · `0`. `` → `` `m ER-04` 네 줄이 `notes_committed=1` · `1` 이상 스물셋 · 두 값 모두 `1` 이상 · `0`. ``
   - ``notes 모의본을 커밋한 예행 판 `notes_committed=1` · `1` 스물둘 · `1 1` · `0`.`` → ``… `1` 스물셋 · `1 1` · `0`.``
   - 양성 대조 끝에 덧붙인다: 「 · `## 바꾼 파일` 줄을 지운 사본 → 둘째 줄 열일곱째 값 `0` · 넘김 줄을 다른 절에 한 번씩 더 적은 사본 → 셋째 줄 `2 2`(요구값 안 — 진짜 notes 모양)」
4. 봉인 전 실측 표 ER-04 행(597 줄): 「예행 판」 칸 `` `1` 스물둘 `` → `` `1` 스물셋 ``, 「대조」 칸에 3 의 두 대조를 덧붙인다.

고친 도우미로 예행 판을 다시 재 봤다(`p10r/k2/` · `p10r/er04.sh`): 둘째 줄 `1` 스물셋 · 셋째 줄 `1 1` · 넷째 줄 `0`.
넘김 줄을 한 번씩 더 적은 사본 → 셋째 줄 `2 2`. `## 바꾼 파일` 을 지운 사본 → 둘째 줄 열일곱째 값 `0`. BUILD 는 봉인 전에 이 셋을 한 번 더 돌린다.

## 권하는 것 (안 해도 판정은 바뀌지 않는다)

- **시험 수 `[미검증]` 과 네 칸의 경계를 한 줄로.** SK-04 조건 문장은 「생성 측 `[미검증]` 이 … 네 칸을 요구한다」 인데, SK-08 이 react-run · react-preflight 에 새로 넣는
  `[미검증] 0 passed …` · `[미검증] N passed · M skipped` 는 네 칸 없이 두 수 · skipped 범위 · `.only` 수를 적는다. 규약 §3 (b)(c) 와 react-test 가 원래 쓰던
  「그 범위는 `[미검증]`」 모양이라 내용은 맞지만, 평가자가 SK-04 문장을 넓게 읽으면 어긋난다고 볼 수 있다. `구현 후보가 둘 이상이었던 곳의 선택` 목록에
  「시험 수 `[미검증]` 에 네 칸을 붙일지 — 안 붙인다. 규약 §3 (b)(c) 의 비어 있는 증거 범위 표시이고, 네 칸은 §2 의 환경상 불가(R1·R2)에 붙는다」 한 줄을 권한다(서술 절이라 봉인 값과 무관).
- **AR-02 문장과 측정 개수.** 조건 문장은 가리키는 자리 일곱(react-run Gotcha 머리 · 비교 반복 순서 · Step 0 · (b) · (c) · **Gotcha 12** · 4-1)을 「각각 1」 이라 하는데
  첫 줄 측정은 여섯이다. Gotcha 12 는 SK-09 가 잰다 — 문장에 「(Gotcha 12 는 SK-09 가 잰다)」 를 붙이거나 뺀다.
- **배경 표 30 줄** 「킷 파일에 canary 라고 적은 곳이 없고」 는 글자대로는 틀리다 — `react-screen/SKILL.md:24` 가 `<Activity />` 를 canary 로 적는다.
  「킷 파일에 `<ViewTransition>` 을 canary 라고 적은 곳이 없고」 로.
- **ER-04 양성 대조 목록.** 조건 괄호는 변형 셋(`unsigned-shared` · `signed-outside` · `cross-phase`), 봉인 전 실측 표는 넷(`unsigned-mine` 포함)이다. 표에 맞춘다.
- **DG-05 (e) 가 보는 범위.** `scripts/check-stale-values.py` 의 `SOURCE_DIRS` 에 `docs/react` 는 있지만 `react-kit/references` 는 없다 — 열아홉 파일 가운데 두 파일만 본다
  (P12 는 잡혔고, 같은 값을 규약 파일에 넣은 사본은 `stale_rc=0 0` 이었다). 문서 사이트 매핑표는 `react-kit/references/` 를 react-kit 소스로 적는다.
  `범위 경계` 에 이 한계를 한 줄로 적고, notes 「다음 사이클 메모」 에 Phase 4 몫(`scripts/`)으로 넘길 것을 권한다.
- **문서 사이트 넘김.** `docs/react-kit/render-evidence-protocol.html` 은 `v1.0.0 · 2026-07-27` 판으로 남는다. `scripts/detect-docs-drift.py --since 4a8ec55…` 가 예행 판에서 이 페이지를 잡으니
  Final F2 가 놓치지는 않는다. 그래도 Phase 5 · 7 notes 처럼 「넘기는 것」 에 한 줄 적어 두면 Final 이 찾기 쉽다.
- **react-l10n §4-1 둘째 명령의 설명.** `^-(msgstr "[^"]|")` 의 `-"` 는 여러 줄 `msgid` 의 이어진 줄도 잡는다. 「한 줄이라도 내면 번역이 채워져 있던 항목이 지워진 것이다」 는
  단정이 조금 세다 — 더 자주 멈추는 쪽으로만 틀리니 위험은 없다. 「지워졌을 수 있다 — 목록을 보고 가른다」 정도로 누그러뜨릴 만하다.
- **주석 톤.** `project-detect.sh` 새 주석 둘째 줄 끝 「고치기 전에는 두 결함이 서로를 가렸다」 와 새 시험 머리의 날짜 · 인사이트 키는 이유보다 경위에 가깝다(C-01).
  남길지 줄일지는 BUILD 가 tone-kit `core-comment.md` 로 판단한다. 바꾸면 ER-01 측정 문자열은 영향이 없다.
- **ER-04 공유 경로 목록.** `not_other` 에 `docs/react-kit` 은 있지만 `docs/index.html` 같은 다른 문서 사이트 페이지는 없다. 서명을 빠뜨린 커밋이 그 파일을 건드리면
  AR-01(`react-kit` · `docs/react` 만 봄)과 ER-04 둘 다 못 잡는다. 목록에 `docs/index.html` 을 더할 만하다.

## 러닝북 · 지시 대조

| 볼 것 | 판단 | 근거 |
| --- | --- | --- |
| 조건마다 FAIL 을 한 문장으로 쓸 수 있는가 | 된다 | 스물아홉 전부. 까다로운 것만: DG-06 「이 Phase 서명 커밋이 위반 목록에 있다 · 목록을 못 읽었다 · doc-contracts 위반 경로에 이 Phase 파일이 있다」, RE-01 「새 파일이 시험 스크립트 말고 더 있다」 |
| 측정이 의도를 재는가 | 잰다 (ER-04 기대값만 틀림) | 두 판을 `git archive` 로 풀어 재서 다른 Phase 미커밋이 끼지 않는다. 문장 삭제 사본 126 개 `DROP` 126. 내 바꿔치기 열둘 |
| 0 기대 조건의 양성 대조 | 있다 | SK-04 넷째(시작 판 `8`) · SK-08 넷째(`1`) · SK-09 `flow_clean`(`1`) · SK-10 첫째(`6`) · ER-02 · ER-03 · ER-04 넷째 · AR-01 · RE-02 · AP-01 · AP-03 · DG-02 · DG-05 (b)(e) (P11 · P12 로 내가 더함) |
| 시험 통과 조건의 음성 대조 | 있다 | ER-01 옛 스크립트 → `불일치 4` `rc=1`, 비교만 고친 사본 → 불일치 1, 가짜 jq → 종료 코드 2. SK-11 단언 `type` → `check` → `rc=1` |
| 봉인 전 실측 | 됐다 | 내 예행 저장소에서 스물다섯 조건 · 조건 없는 줄 넷 · 변형 둘 모두 표와 같다. 단 BUILD 확인 값 `mock applied 46` 은 안 돌려 본 값이었다 |
| 처리 배정표 Phase 10 행 | 빠짐없다 | `F03` · `F05` · `other-kits:P1` · `P2` · `P5` · `P6` 반영, `F01` 리액트 쪽 반영, `F09` 비고는 미반영 사유(Phase 5 와 같은 판단), Phase 1 · 4 · 6 넘김 반영 또는 사유 |
| 근거 파일 권장안 §4 일곱 | 다뤘다 | 1~6 반영. 7 의 `<ViewTransition>` stable 은 조사 기록 표에만 — Tier 2 를 옮기는 것은 새 내용이라 다음 사이클. 받아들일 만하다 |
| 고쳐도 되는 범위 | 안이다 | 열아홉 전부 `react-kit/` · `docs/react/`. `# sprint-scope` 블록과 `FILES` 가 같다(`scope_same=1`) |
| 공유 파일 | 안 건드린다 | `plugin.json` · marketplace · 루트 README · CLAUDE.md · `docs/` HTML · `ci.yml` · `react-kit/README.md` 제외. CI(자동 검사)에 넣을 시험 줄은 notes 로 |
| 조건끼리 충돌 | 없다 | SK-04 문구와 RE-02 숫자 금지가 안 겹친다(`0`). AP-01 버전 `0.3.0` 과 조사 기록 `1.4.0` 은 다른 값. 시험 수 `[미검증]` 은 위 권하는 것 첫 줄 |
| 러닝북 측정 구멍 넷 | 막았다 | 금지 경로는 `not_other` 가 경로로 직접 센다 · 상한을 못 구하면 `END_UNRESOLVED` · 도우미 열넷을 `type` 으로 확인 · 파일마다 옛 판과 비교(`added` · ER-02) |
| 한 커밋에 킷 하나 · 서명 줄 · notes 뒤 상한 한 줄 더 | 적혀 있다 | `범위 경계` 절. 예행에서 두 커밋 분리 · `end_sha` 두 줄로 흉내 냈다 |

VERDICT: CHANGES

## 2 회차

- 대상: 같은 계약 초안(지금 698 줄, 조건 29 · 기능 조건 19). 초안 폴더의 `p10d/contract.saved2.md` 와 한 글자도 다르지 않다
- 개정 파일: 아직 없다 (봉인 전이라 정상)
- 작업 폴더 `HEAD`(지금 가지의 끝 커밋)는 `8c9a88c` 로 올라갔다 — 그사이 Phase 8 커밋 여섯이 들어왔다. `git diff --stat 4a8ec55 HEAD -- react-kit docs/react docs/react-kit` 는 빈 출력이고 두 폴더에 미커밋 변경도 없다. 그래서 시작 커밋 `4a8ec55` 는 그대로 맞다
- 직접 돌린 곳: `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p10r2/`. 작업 폴더는 이 검토 파일 말고 건드리지 않았다

### 2 회차 결론

**1 회차에 꼭 고치라고 한 두 곳은 둘 다 고쳐졌고, 권한 것 여덟도 전부 들어갔다.** 조건 스물다섯을 새 예행 저장소에서 다시 재 보니 봉인 전 실측 표와 한 글자도 다르지 않았다.

**새로 꼭 고칠 곳은 하나다 — DG-05 (c) · (e) 의 종료 코드 0 요구.** 조건 문장은 「저장소 검사가 이 킷을 문제로 가리키지 않는다」 인데,
측정은 `sync-docs.py --check-only` 와 `check-stale-values.py` 가 레포 전체에서 종료 코드 0 이기를 요구한다. 다른 Phase 가 자기 파일에 등록된 옛 값을 넣거나
다른 킷 `README.md` 가 어긋나 있으면 이 Phase 가 아무것도 틀리지 않았는데 글자대로 떨어진다. 사본으로 넣어 봤다(아래 3). 같은 사이클의 Phase 8 · 9 계약은
이 자리를 「킷 전체를 보는 검사는 이 킷 몫의 줄만 센다 — 같은 구간에 다른 Phase 가 올린 변경 때문에 떨어지지 않게 한다」 로 이미 막았다.
다만 그 두 계약처럼 「종료 코드 0 또는 1」 만 적으면 다른 구멍이 생긴다 — 검사기가 멈춰도 종료 코드가 1 이라 통과한다(`stale-values.yaml` 을 지운 사본에서 확인).
그래서 검사기가 실제로 돌았다는 줄을 함께 센다. 고칠 문구는 아래에 있다. 이것만 고치면 나머지는 봉인해도 된다.

### 1 회차 지적 반영 확인

| 1 회차 지적 | 지금 계약 | 확인한 방법 · 결과 |
| --- | --- | --- |
| 꼭 1 — `mock applied 46` | 171 · 172 줄 「44 치환 · 새 파일 하나」 · `mock applied 45` | `git archive 4a8ec55 react-kit docs/react` 를 푼 새 사본에 `python3 p10d/mock.py` → `mock applied 45` · 종료 코드 0. 새 시험 파일 `-rwxr-xr-x`. `mock.py` 지문 앞 16 자리 `db181ec91592e78d` 는 계약에 적힌 값과 같다 |
| 꼭 2 — ER-04 토큰 · 기대값 | `m.sh` `ER-04)` 토큰 스물셋(열일곱째 `## 바꾼 파일`) · 663 줄 「스물셋」 · 「러닝북 여섯 절 제목 … 와 넘김 절 제목」 · 「각각 1 줄 이상」 · 664 줄 「두 값 모두 `1` 이상」 · 표 609 줄 | 예행 판 `1` 스물셋 · `1 1` · `0`. 사본 셋: `## 바꾼 파일` 줄을 지움 → 둘째 줄 열일곱째 `0` · 넘김 줄을 다른 절에 한 번씩 더 적음 → `2 2`(요구값 안) · 「기준 커밋」 을 전부 지움 → `0 1` |
| 권 — 시험 수 `[미검증]` 에 네 칸 | 148 ~ 150 줄 「안 붙인다」 | SK-04 · SK-08 이 재는 자리와 맞는다 |
| 권 — AR-02 문장과 측정 개수 | 670 줄 여섯 자리 + 「(§4-1 이 가리키는 Gotcha 12 는 SK-09 가 잰다)」 | 첫 줄 측정 여섯과 같다 |
| 권 — 배경 표 canary | 30 줄 「`<ViewTransition>` 을 canary 라고 적은 곳이 없고(canary 는 `react-screen` Gotcha 11 의 `<Activity />` 에만 있다)」 | `git grep -n -i canary 4a8ec55 -- react-kit` → `react-screen/SKILL.md:24` 한 줄뿐 |
| 권 — ER-04 변형 목록 | 244 · 584 ~ 586 · 609 · 664 줄 변형 다섯 | `unsigned-docsite` 를 새로 만들어 쟀다 → ER-04 넷째 값 `1` |
| 권 — DG-05 (e) 가 보는 범위 | 263 · 264 줄 · notes 「다음 사이클 메모」 넷째(260 줄) | 문장 있음 |
| 권 — 문서 사이트 넘김 | 261 · 262 줄 | 문장 있음 |
| 권 — react-l10n §4-1 설명 | 151 · 152 줄 · SK-09 토큰 「지워졌을 수 있다 — 출력 줄을 보고 가른다」 | 그 문장을 지운 사본 → SK-09 셋째 줄 여섯째 값 `0` |
| 권 — 주석 말투 | `mock.v1` 대 `mock.py` 차이 세 곳 | 「두 결함이 서로를 가렸다」 · 날짜 · 인사이트 키가 빠지고 이유만 남았다 |
| 권 — `docs/index.html` | `not_other` 목록 끝 | 위 `unsigned-docsite` → `1` |

### 2 회차에 직접 돌려 본 것

1. **계약 본문과 초안 도우미가 같은가.** 측정 공통 정의 절의 bash 블록 셋을 뗀 `p10r2/k/` 가 초안 `p10d/k/` 와 `cmp` 로 같다(`same common.sh` · `same m.sh` · `same new-warnings.sh`).
2. **새 예행 저장소 둘(`p10r2/rh-none` · `p10r2/rh-base`)을 이 계약으로 만들어 조건 스물다섯을 다시 쟀다**(`p10r2/run-e.txt` · `p10r2/run-b.txt`, bash 5.3.9). 전부 표와 같다. 예:
   - SK-09 → `flow_clean=0` · `1 1` · `1` 일곱 · `1` 여섯 · `1 12` · `1 0`
   - ER-01 → `1 0 0` · 불일치 0 `rc=0` 두 벌 · 불일치 4 `rc=1` · `shellcheck=0 bash_n=0` · `mode=100755 fixtures_same=1`
   - ER-03 → `added=256 k02=0 names=0`
   - ER-04 → `notes_committed=1` · `1` 스물셋 · `1 1` · `0`
   - DG-05 → `10 0 rc=0` · `tf_mine=0` · `sync_docs_rc=0 1` · `1 0` · `stale_rc=0 0`
   - DG-06 → `scope-isolation: PASS` · `doc-contracts: PASS` · `doc_checked=2 doc_mine=0` · `violators=0 mine=0`

   시작 커밋 판도 표와 같다(SK-04 마지막 값 `8` · SK-10 첫 값 `6` · ER-01 `0 1 1` 등). `/bin/bash` 3.2.57 로 SK-04 · SK-09 · ER-01 · ER-04 를 다시 재도 같았다.
3. **다른 Phase 커밋이 범위에 들어온 지금 상태.** `4a8ec55..HEAD` 여섯 커밋은 전부 `Kaizen-Phase: kaizen-0924-p08-infra-kit` 서명이 있고 `react-kit` · `docs/react` · `not_other` 경로를 건드리지 않는다.
   작업 폴더에서 `validate-post-kaizen.py --since 4a8ec55… --verbose` → `scope-isolation: PASS`(6 commits · 13 kits) · `doc-contracts: PASS`(1 블록 — 예행의 2 블록과 수가 다르지만 조건은 N 을 고정하지 않는다).
   `HEAD` 판 사본에서 `sync-docs.py --check-only` 종료 코드 0 · `check-stale-values.py` 종료 코드 0. 지금은 전부 통과다.
4. **DG-05 (c) · (e) 를 다른 Phase 몫 변경으로 흔들었다**(`p10r2/dg05var.sh` · `p10r2/dg05var2.sh`, 예행 판 사본). 셋째 칸은 아래 「고칠 곳」 대로 바꾼 측정의 출력이다.

   | 사본 | 지금 측정 | 바꾼 측정 | 지금 요구값으로 |
   | --- | --- | --- | --- |
   | 그대로 | `sync_docs_rc=0 1` · `stale_rc=0 0` | `stale_rc=0 ran=1 0` | 통과 |
   | `docs/rust/research-log.md` 끝에 등록된 옛 값 `shadcn-ui@latest` (다른 Phase 파일) | `stale_rc=1 0` | `stale_rc=1 ran=1 0` | **떨어진다** — 이 Phase 잘못이 아니다 |
   | 같은 값을 `docs/react/research-log.md` 끝에 (이 Phase 파일) | `stale_rc=1 1` | `stale_rc=1 ran=1 1` | 떨어진다 — 맞다 |
   | `.harness/stale-values.yaml` 을 지움 (검사기가 멈춤) | `stale_rc=1 0` | `stale_rc=1 ran=0 0` | 떨어진다 — 「0 또는 1」 만 적으면 통과해 버린다 |
   | `rust-kit/README.md` 를 어긋나게 함 (다른 킷) | `sync_docs_rc=1 1` | 같음 | **떨어진다** — 이 Phase 잘못이 아니다 |

   바꾼 측정을 예행 판에 bash 5 · `/bin/bash` 3.2 로 돌리면 둘 다 `10 0 rc=0` · `tf_mine=0` · `sync_docs_rc=0 1` · `1 0` · `stale_rc=0 ran=1 0`(`p10r2/k3/`).
5. **`mock.py` 를 두 번 돌리면** 첫 파일에서 `MOCK_FAIL react-kit/references/render-evidence-protocol.md: old 가 0 번 있다` · 종료 코드 1 로 멈춘다. `rep()` 가 치환마다 곧바로 파일을 쓰므로 중간에 멈추면 앞서 쓴 파일이 남는다.

### 꼭 고칠 곳 — DG-05 (c) · (e)

1. `m.sh` `DG-05)` 갈래 마지막 줄(계약 553 줄)을 아래로 바꾼다. `sync-docs` 줄(549 줄)은 그대로 둔다.

   ```bash
       ( cd "$G" && python3 scripts/check-stale-values.py > "$T/sv.txt" 2>&1 ); echo "stale_rc=$? ran=$(grep -c '^검사 범위: 소스 디렉토리 ' "$T/sv.txt") $(grep -cF -f <(printf '%s\n' "${FILES[@]}") "$T/sv.txt")" ;;
   ```

2. 조건 줄(695 줄) 두 군데:
   - `` (c) `scripts/sync-docs.py --check-only` 가 종료 코드 0 에 `` → `` (c) `scripts/sync-docs.py --check-only` 가 종료 코드 0 또는 1 에 ``
   - `` (e) `scripts/check-stale-values.py` 종료 코드 0 에 이 Phase 파일 0 건 [exact] `` →
     `` (e) `scripts/check-stale-values.py` 가 돌았고(`검사 범위: 소스 디렉토리 ` 로 시작하는 줄 1) 종료 코드 0 또는 1 에 이 Phase 파일 0 건. (c) · (e) 의 종료 코드 1 은 다른 킷 README 나 다른 Phase 파일 때문에도 나므로 허용하고 이 킷 몫의 줄로 가른다 — 검사기가 멈춰 난 종료 코드 1 은 (c) 는 `react-kit/README.md` 줄이, (e) 는 `검사 범위:` 줄이 0 이라 떨어진다 [exact] ``
3. 측정 괄호(696 줄) 앞부분:
   - `` `m DG-05` 다섯 줄이 `10 0 rc=0` · `tf_mine=0` · `sync_docs_rc=0 1` · `1 0` · `stale_rc=0 0`. 봉인 전 실측: 예행 판이 요구값과 같다. `` →
     `` `m DG-05` 다섯 줄이 `10 0 rc=0` · `tf_mine=0` · `sync_docs_rc=0 1` 또는 `sync_docs_rc=1 1` · `1 0` · `stale_rc=0 ran=1 0` 또는 `stale_rc=1 ran=1 0`. 봉인 전 실측: 예행 판 `10 0 rc=0` · `tf_mine=0` · `sync_docs_rc=0 1` · `1 0` · `stale_rc=0 ran=1 0`. 양성 대조: 다른 킷 `rust-kit/README.md` 를 어긋나게 한 사본 → `sync_docs_rc=1 1`(요구값 안) · `docs/rust/research-log.md` 끝에 등록된 옛 값 `shadcn-ui@latest` → `stale_rc=1 ran=1 0`(요구값 안) · 같은 값을 `docs/react/research-log.md` 끝에 → `stale_rc=1 ran=1 1` · `.harness/stale-values.yaml` 을 지운 사본 → `stale_rc=1 ran=0 0`. ``
4. 봉인 전 실측 표 DG-05 행(619 줄): 「예행 판」 칸 `` `stale_rc=0 0` `` → `` `stale_rc=0 ran=1 0` ``, 「대조」 칸 끝에 「 · 다른 킷 README 어긋남 → `sync_docs_rc=1 1` · `docs/rust` 옛 값 → `stale_rc=1 ran=1 0` · `docs/react` 옛 값 → `stale_rc=1 ran=1 1` · 등록 파일 없음 → `stale_rc=1 ran=0 0`」 를 덧붙인다
5. `범위 경계` 264 줄: `` 등록된 옛 값을 규약 파일에 넣은 사본은 `stale_rc=0 0` 이다 `` → `` … `stale_rc=0 ran=1 0` 이다 ``

도우미 폴더도 계약 블록에서 다시 떼어 낸다. BUILD 는 봉인 전에 예행 판에서 `m DG-05` 를 한 번 더 돌려 다섯째 줄이 `stale_rc=0 ran=1 0` 인지 본다.
조건 줄이 바뀌니 봉인 값은 이 문구를 넣은 뒤에 구한다.

### 2 회차에 권하는 것 (안 해도 판정은 바뀌지 않는다)

- **`mock.py` 는 한 번만 돌린다.** 172 줄 「BUILD 는 `mock.py` 를 작업 폴더에 그대로 돌린다」 뒤에 「돌리기 전에 `git status --short -- react-kit docs/react` 가 빈 출력인지 본다 — 두 번째 실행은 첫 파일에서 `MOCK_FAIL` 로 멈추고, 중간에 멈추면 앞서 쓴 파일이 남는다」 를 권한다(서술 절이라 봉인 값과 무관)
- **다른 Phase 에 알릴 것.** Phase 8 계약 DG-05 의 「stale_rc 는 0 또는 1」 과 Phase 9 계약 DG-05 (c) 의 「종료 코드 0 또는 1 이고 출력에 열한 파일 경로가 0 건」 은 검사기가 멈춰도 통과한다(위 4 의 넷째 사본 모양). 이 계약 밖이라 여기서는 고치지 않는다. notes 「다음 사이클 메모」 에 한 줄 적어 두면 Final 이 찾기 쉽다

### 다시 본 것 — DG-05 말고는 새 결함 없음

| 볼 것 | 판단 | 근거 |
| --- | --- | --- |
| 조건마다 떨어지는 경우를 한 문장으로 쓸 수 있는가 | 된다 | 스물아홉 전부. DG-05 는 위 고칠 곳을 넣으면 「react-kit 줄이 어긋남 · 이 Phase 파일에 옛 값 · 검사기가 안 돎」 |
| 측정이 의도를 재는가 | 잰다 (DG-05 (c) · (e) 의 종료 코드만 레포 전체를 잰다) | 위 4 |
| 1 회차 뒤 바뀐 줄이 다른 조건을 건드리는가 | 안 건드린다 | 초안 설명(590 줄)대로 ER-04 둘째 줄만 바뀌었고 나머지 스물넷 출력은 그대로다 |
| 조건끼리 충돌 | 없다 | ER-04 「각각 1 줄 이상」 과 셋째 값 「두 값 모두 `1` 이상」 이 같은 뜻이다. SK-04 와 148 ~ 150 줄 선택이 맞는다 |
| 범위 | 안이다 | 고치는 파일 열아홉이 그대로고 `scope_same=1` |
| 다른 Phase 커밋이 범위에 들어옴 | 걸러진다 | 위 3. ER-04 · AR-01 · SC-00 · DG-01 · DG-03 · DG-04 는 서명 · 경로로 거르고, DG-06 은 떨어졌을 때 가르는 문장이 이미 있다 |

VERDICT: CHANGES
