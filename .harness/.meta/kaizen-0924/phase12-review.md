# 카이젠 2026-09-24 Phase 12 (reflect-kit) — 계약 초안 독립 검토

- 대상: `.harness/sprint-contract-kaizen-0924-p12-reflect-kit.md` (봉인 전, 작업 폴더에 추적 안 된 파일, 29 조건 · 기능 조건 20)
- 개정 파일 `.harness/sprint-amendments-kaizen-0924-p12-reflect-kit.md` 은 아직 없다 — 봉인 전이라 맞다
- 검토자: REVIEW 에이전트 (사용자 승인 대신, 러닝북 「사용자 승인(5 단계) 대체」)
- 검토일: 2026-09-25

## 결론

고쳐야 봉인할 수 있다. 측정 정의와 예행 값은 다시 돌려도 계약에 적힌 그대로 나왔고, 처리 배정표 · 범위 · 공유 파일 · 조건끼리의 충돌에서는 문제를 못 찾았다.
걸리는 것은 두 가지다.

1. 시험 출력을 세는 방식이 실패를 통과로 읽는다. 시험은 실패한 경우를 `불일치 <이름>` 으로 찍는데, 이 줄 안에 `일치 <이름>` 글자가 그대로 들어 있다.
   `toks` 는 그 글자가 든 줄을 세므로 시험이 실패를 적어도 `1` 이 나온다. SC-02 · SC-03 · SC-04 · SC-07 은 이 셈만으로 판정한다 —
   구현을 망가뜨린 사본 셋에서 `m SC-02` · `m SC-04` · `m SC-07` 이 요구값을 그대로 냈다(아래 재현). SC-01 · SC-06 은 `결과:` 줄이 따로 잡아 줘서 판정은 안 틀리지만 같은 식으로 고친다.
2. SC-06 · SC-07 조건 문구가 손으로 센 답(`Stop 실패 시도 5회 …` · `facets 4개 · 마찰 있는 세션 3개 …`)을 적어 두었는데, 측정은 그 답을 읽지 않고 시험이 찍은 `일치` 한 낱말만 본다.
   시험 파일의 답을 바꿔도 측정은 그대로다.

두 곳 모두 `m.sh` 몇 줄과 조건 문구 몇 구절이다. 고친 `m.sh` 를 예행 판에 돌려 요구값이 안 바뀌는 것과 망가뜨린 사본에서 값이 떨어지는 것을 이미 확인했다(아래). 고치면 `APPROVE` 다.

## 다시 돌려 본 것

모두 스크래치 `p12r/` 아래에서만 돌렸다. 작업 폴더에는 이 파일 하나만 썼다.

1. 계약 `회귀 게이트` 절의 bash 블록 셋을 새로 뽑아(`p12r/extract.sh`) DRAFT 의 `p12d/k/` 와 비교했다 — `common.sh` · `m.sh` · `new-warnings.sh` 셋 다 글자 그대로 같다.
   `mock.py` 의 sha256 앞 16 자리는 `714450452fff4513` 로 계약과 같다. DRAFT 예행 저장소(`p12d/rh-none`)의 계약은 지금 초안과 조건 줄이 같고 서술 두 곳만 다르다.
2. `p12d/rh-none` 에서 SC-01 · SC-05 · SC-06 · SC-08 · AR-01 · ER-03 을 내 임시 폴더로 다시 쟀다 — 계약 `봉인 전 실측` 표의 예행 판 값과 같다
   (예: SC-01 `결과: 24 경우 중 불일치 0 rc=0` 두 줄 · `1 1 1 1 1` · `ro=1 fullauto=0` · `결과: 24 경우 중 불일치 17 rc=1`, SC-08 `E rc=0 args=10 first=` · `B rc=2 args=9 first=error: unexpected argument '--full-auto' found`).
3. 지워진 예행 변형 가운데 `cross-phase` 를 DRAFT 의 `rehearse.sh` 로 새로 만들어(지금 초안 그대로 봉인) AR-01 · ER-03 · DG-06 을 쟀다 —
   AR-01 둘째 줄 `2 12`, ER-03 넷째 값 `1`, DG-06 `scope-isolation: FAIL` · `violators=1 mine=1`. 계약 표와 같다. 잰 뒤 지웠다(디스크 여유가 1.4 GB 뿐이다).
4. sprint-contract Step 6.2 · 6.5 명령을 초안에 돌렸다 — 조건 29 · 기능 조건 20(복잡 9~20 안), `##` 제목은 허용 목록 안, 서술 절의 조건 체크박스 0, `[미실측]` 0.
5. 러닝북 검증 목록의 `scripts/sync-evals.py --check-only` 가 계약에 없어서 따로 돌렸다 — 예행 끝 판 · 시작 커밋 판 둘 다 종료 코드 0. `reflect-kit/evals/` 에 `evals.json` 이 없어도 걸리지 않는다.

## 고칠 것 — 조건 ID 별 문구

### 재현 (1 번 문제)

예행 판 사본 한 군데를 망가뜨리고 되돌렸다(`p12r/neg.sh` · `neg2.sh` · `neg3.sh` · `neg4.sh`). 「지금 m」 은 초안의 `m.sh`, 「고친 m」 은 아래 수정을 넣은 `p12r/k2/m.sh` 다.

| 망가뜨린 것 | 시험이 찍은 줄 | 지금 m | 고친 m |
| --- | --- | --- | --- |
| codex `err=` 를 비어 있지 않은 첫 줄로만 고름 | `불일치 codex 실패 err= ERROR 줄` · `불일치 1` | SC-02 `1 1 1 1 1 1 1` · `1 1 0 0` — 요구값 그대로 | `0 1 1 1 1 1 1` · `1 1 0 0` |
| 가리기 전에 200 자로 자름 | `불일치 키 조각 없음` | (재지 않음) | `1 1 1 0 1 1 1` · `1 1 0 0` |
| 대체 경로 모델을 `haiku-4.5` 로 되돌림 | 불일치 일곱 | (재지 않음 — 둘째 줄 `0 1` 이 잡는다) | `0 1 0 1` · `0 1` |
| 분석 임시 폴더 `trap` 을 뺌 | `불일치 TMPDIR 비었음` | SC-04 `1 1 1 1 1 1 1` · `…:1:ok` 셋 — 요구값 그대로 | `1 1 1 1 1 1 0` · `…:1:ok` 셋 |
| `log-prompt.sh` 표식 검사를 뺌 | `불일치 표식 — log-prompt.sh 안 적음` | (둘째 줄 `log-prompt.sh:0:no` 가 잡는다) | `1 1 1 0 1 1 1` · `log-prompt.sh:0:no` |
| `facets_unmatched` 가 reflections 에 있는 세션도 냄 | 불일치 셋 | SC-07 `1 1 1 1` — 요구값 그대로 | `0 0 0 1` |

고친 `m.sh` 로 예행 판(`rh-none`)을 재면 SC-01 · SC-02 · SC-03 · SC-04 · SC-06 · SC-07 이 전부 계약 표의 요구값 그대로다. 초안의 음성 대조가 이 구멍을 못 본 까닭은
`회귀 게이트` 절 대조가 시험 출력(`T1`)이나 `m … | tail -1` 로만 읽었고 `m` 의 첫 줄을 망가뜨린 사본에서 읽지 않았기 때문이다.

### `m.sh` 수정

`SC-01` · `SC-02` · `SC-03` · `SC-04` 갈래의 `o=$(bash "$E/$TLR" 2>&1)` 네 줄과 `SC-06` · `SC-07` 갈래의 `o=$(bash "$E/$TCS" 2>&1)` 두 줄을 아래처럼 바꾼다.
SC-06 · SC-07 갈래 끝에는 한 줄씩 더한다.

```bash
    # 불일치 줄도 「일치 <이름>」 글자를 품는다 — 일치로 시작하는 줄만 남겨 센다
    o=$(bash "$E/$TLR" 2>&1 | grep '^일치 ')
```

```bash
  SC-06)  # collect_status — 알려진 답 시험 두 해석기 · 시험 줄 여섯 · 조건 문구의 답이 시험 check 줄에 있다
    lastline bash "$E/$TCS"
    lastline env PATH="$P32" /bin/bash "$E/$TCS"
    o=$(bash "$E/$TCS" 2>&1 | grep '^일치 ')
    toks "$o" '일치 7 일 · 두 폴더' '일치 all · 두 폴더' '일치 멈춤 — 엔트리 0 · 실패 1 이상' '일치 빈 폴더 — 경고 없음' '일치 일수 잘못 — 멈춤' '일치 zsh — 멈춤'
    toks "$(cat "$E/$TCS")" 'check "7 일 · 두 폴더" "수집 상태: Stop 실패 시도 5회 (codex 실패 4 · 대체 경로 실패 3 · 대체 경로 성공 1 · 분석 전 중단 2; 고유 세션 4) / 기록된 세션 1 / 엔트리 1 / 마지막 기록 $D1' \
      'check "all · 두 폴더" "수집 상태: Stop 실패 시도 6회 (codex 실패 5 · 대체 경로 실패 4 · 대체 경로 성공 1 · 분석 전 중단 2; 고유 세션 5) / 기록된 세션 2 / 엔트리 3 / 마지막 기록 $D1' ;;
  SC-07)  # facets_unmatched — 시험 줄 넷 · 조건 문구의 답이 시험 check 줄에 있다
    o=$(bash "$E/$TCS" 2>&1 | grep '^일치 ')
    toks "$o" '일치 facets 7 일 · alpha' '일치 facets 7 일 · all' '일치 facets all · alpha' '일치 facets 폴더 없음'
    toks "$(cat "$E/$TCS")" 'check "facets 7 일 · alpha" "facets 대조: facets 4개 · 마찰 있는 세션 3개 · 그중 reflections 없음 2개 (facets 읽기 실패 1 · session-meta 읽기 실패 1)' ;;
```

더한 두 줄은 예행 판 시험 파일에서 `1 1` · `1` 이고, 답 한 글자를 바꾼 사본(`5회` → `9회`, `없음 2개` → `없음 3개`)에서 `0 1` · `0` 이다(`p12r/pin.sh`).
`$D1` 은 작은따옴표 안이라 글자 그대로 찾는다.

### 조건 문구

- **SC-01**: 「그 출력에 codex 경우 다섯 줄」 → 「그 출력 가운데 `grep '^일치 '` 가 남긴 줄에 codex 경우 다섯 줄」
- **SC-02**: 「같은 시험 출력에 `err=` 경우 일곱 줄」 → 「같은 시험 출력 가운데 `grep '^일치 '` 가 남긴 줄에 `err=` 경우 일곱 줄」.
  음성 대조 문장 「가리기 전에 200 자로 자르는 사본은 `불일치 키 조각 없음`, 비어 있지 않은 첫 줄만 고르는 사본은 `불일치 codex 실패 err= ERROR 줄` 을 낸다」 →
  「가리기 전에 200 자로 자르는 사본은 `m SC-02` 첫 줄이 `1 1 1 0 1 1 1`, 비어 있지 않은 첫 줄만 고르는 사본은 `0 1 1 1 1 1 1` 이다」
- **SC-03**: 「같은 시험 출력에 대체 경로 경우 넷」 → 「같은 시험 출력 가운데 `grep '^일치 '` 가 남긴 줄에 대체 경로 경우 넷」. 끝에 음성 대조 한 구절을 더한다 —
  「음성 대조: 모델 이름을 `haiku-4.5` 로 되돌린 사본은 `0 1 0 1` · `0 1`」
- **SC-04**: 「같은 시험 출력에 경우 일곱 줄」 → 「같은 시험 출력 가운데 `grep '^일치 '` 가 남긴 줄에 경우 일곱 줄」. 끝에 음성 대조 한 구절을 더한다 —
  「음성 대조: 분석 임시 폴더 `trap` 을 뺀 사본은 첫 줄 끝 값이 `0`, `log-prompt.sh` 표식 검사를 뺀 사본은 첫 줄 넷째 값이 `0` 이고 둘째 줄이 `log-prompt.sh:0:no`」
- **SC-06**: 「출력에 여섯 줄(…)이 각각 1 이다」 → 「출력 가운데 `grep '^일치 '` 가 남긴 줄에 여섯 줄(…)이 각각 1 이고, 시험 파일의 `check "7 일 · 두 폴더"` 줄과
  `check "all · 두 폴더"` 줄에 손으로 센 답(`Stop 실패 시도 5회 (codex 실패 4 · 대체 경로 실패 3 · 대체 경로 성공 1 · 분석 전 중단 2; 고유 세션 4) / 기록된 세션 1 / 엔트리 1` ·
  `Stop 실패 시도 6회 (codex 실패 5 · 대체 경로 실패 4 · 대체 경로 성공 1 · 분석 전 중단 2; 고유 세션 5) / 기록된 세션 2 / 엔트리 3`)이 글자 그대로 한 줄씩 있다」.
  괄호 안 all 설명 「all · 두 폴더 — 실패 6 · 기록 2 · 엔트리 3」 은 그대로 둬도 된다. 측정 끝: 「`m SC-06` 세 줄이 … `1` 여섯」 → 「`m SC-06` 네 줄이 `결과: 10 경우 중 불일치 0 rc=0` 두 줄 · `1` 여섯 · `1 1`」
- **SC-07**: 「같은 시험 출력에 넷(…)이 각각 1 이다」 → 「같은 시험 출력 가운데 `grep '^일치 '` 가 남긴 줄에 넷(…)이 각각 1 이고, 시험 파일의 `check "facets 7 일 · alpha"` 줄에
  손으로 센 답 `facets 대조: facets 4개 · 마찰 있는 세션 3개 · 그중 reflections 없음 2개 (facets 읽기 실패 1 · session-meta 읽기 실패 1)` 이 글자 그대로 한 줄 있다」.
  음성 대조 문장에 「reflections 에 있는 세션도 내는 사본은 `m SC-07` 첫 줄이 `0 0 0 1`」 을 더한다. 측정 끝: 「`m SC-07` 한 줄이 `1 1 1 1`」 → 「`m SC-07` 두 줄이 `1 1 1 1` · `1`」

### 봉인 전에 BUILD 가 할 것

- `회귀 게이트` 절 `m.sh` 블록을 위처럼 고치고 `p12d/k/m.sh` 도 같게 맞춘다(계약에서 다시 뽑는다)
- `봉인 전 실측` 표의 SC-02 · SC-03 · SC-04 · SC-06 · SC-07 행을 고친다 — 예행 판 칸에 SC-06 `1 1`, SC-07 `1` 을 더하고, 대조 칸에 위 재현 표의 「고친 m」 값을 적는다.
  시작 커밋 판 칸의 SC-06 · SC-07 은 시험 파일이 없어 `0 0` · `0` 이다
- 고친 `m.sh` 로 `ctl.sh` 의 해당 대조를 `m <조건 ID>` 전체 출력으로 다시 돌린다(이번엔 첫 줄까지 본다)
- Step 6.2 · 6.5 를 다시 돌린다. 조건 수는 29 · 기능 조건 20 그대로다

## 확인했고 문제 없는 것

1. **조건마다 실패를 한 문장으로 쓸 수 있는가.** 된다 — 예: SK-03 「digest `## 프로젝트 ID` 에 세 줄 가운데 하나가 없거나 `reflect-kit/` 에 `basename(git-root)` 가 한 줄이라도 남았다」,
   SC-08 「이 기계 codex 가 새 인자 묶음을 거부하거나 옛 묶음을 받아들인다」, ER-03 「notes 가 끝 커밋에 없거나, 스물네 문자열 가운데 하나가 없거나, 넘김 셋이 받을 Phase 와 다른 줄에 있거나,
   다른 Phase 서명 없는 커밋이 공유 파일 · 이 킷 나머지를 건드렸다」, DG-06 「`scope-isolation` 이 실패인데 위반 커밋을 못 읽었거나 그 안에 이 Phase 서명 커밋이 있다」.
   위 1 번 문제는 문장이 아니라 측정이 그 문장을 못 잰 것이다
2. **처리 배정표 Phase 12 행.** `reflect-collector:P3` · `P4` · `P5` 셋 다 조건으로 들어갔다(P3 → SC-01 ~ SC-04 · SC-08, P4 → SK-01 · SK-02 · SK-04 · SC-06 · SC-07, P5 → SK-03 · SK-05 · SC-05).
   `harness:P02` 비고 · 러닝북 Phase 12 추가 과제(`save-feedback.sh` 워크트리 이름) · `phase4-notes.md` 넘김은 `harness/` 가 범위 밖이라 「다음 사이클 Phase 4」 로 넘기고 ER-03 이 그 줄을 잰다.
   Phase 4 notes 가 같은 이유로 같은 곳에 넘겼으니 어긋나지 않는다. 근거 §3 의 `hooks.json` 따옴표 · `async` · `plugin.json` 도 표에 처리 방향이 있다.
   근거 §5 「7 일 억제 창은 가설로 표시」 는 `reflect-kit/docs/SCHEMA.md:155` 에 이미 있다
3. **범위.** 고치는 열두 파일이 전부 `reflect-kit/` 안이고 나머지는 `.harness/` 다 — Phase 표의 고쳐도 되는 범위 안이다. 범위 선언 블록 모양은 `harness/README.md` 가 정한 자리(`## 범위 경계` 안, 첫 줄 `# sprint-scope`)와 같다
4. **공유 파일.** 마켓플레이스 · `plugin.json` 버전 · 루트 문서 · `docs/` · `ci.yml` · 처리 배정표를 건드리지 않고 notes 로 넘긴다. ER-03 넷째 값과 AR-01 이 지키고, 예행 변형으로 잡히는 것을 다시 확인했다
5. **조건끼리 충돌.** SK-03 은 `basename(git-root)` 0 을 요구하는데 시작 커밋의 세 곳(`SCHEMA.md:191` · `README.md:94` · digest `SKILL.md:49`)이 전부 고치는 열두 파일 안이라 ER-03 의 건드리면 안 되는 파일과 부딪히지 않는다.
   SK-05 가 요구하는 README 문장의 `v0.3.0+` 는 킷 버전 `0.7.1` 이 아니라 AP-01 과 안 부딪힌다. ER-02 번역투 · DG-02 마크다운 경고는 SK 문장이 다 들어간 예행 판에서 0 이다
6. **러닝북 측정 규칙.** 상한을 변수로 받고 못 구하면 멈춘다(`END_UNRESOLVED`). 도우미 함수가 없으면 멈춘다(`HELPER_MISSING`). 파일마다 옛판과 비교한다(`added` · ER-01).
   서명 빠뜨린 커밋은 경로로 직접 센다(AR-01 첫 값 · ER-03 넷째 값). notes 커밋 뒤 `end_sha:` 한 줄 더하기가 범위 경계에 있다. 사용자 승인 대체 두 기록과 검토 파일 경로가 범위 경계에 있다

## 권하는 것 — 판정에 넣지 않는다

1. **SC-08 은 이 기계의 codex 판에 묶여 있다.** 근거 파일은 최신 0.156.1 문서가 `--full-auto` 를 「없어질 예정이지만 남아 있다」 고 적는다. QA 전에 codex 가 올라가면 둘째 줄(옛 묶음 `rc=2`)이 `rc=0` 으로 바뀌어 구현이 맞아도 실패한다.
   `m SC-08` 에 `codex --version` 첫 줄을 한 줄 더 찍어 두면 QA 가 환경이 바뀐 것인지 바로 가른다
2. **DG-05 에 `sync-evals.py --check-only` 가 없다.** 러닝북 검증 목록에 있는 명령이다. 지금은 종료 코드 0 이라 `sync_evals_rc=0` 한 칸을 더해도 요구값만 늘어난다
3. **notes 에 Final 이 볼 한 줄.** `harness/agents/qa-evaluator.md` Step 3.4(754~765 줄)는 워크트리 폴더 이름으로 prompt 로그 폴더를 찾는다. Final 이 reflect-kit 새 판을 배포하면
   워크트리 세션의 새 발언은 본 레포 폴더로 가므로, 다음 사이클 Phase 3 이 고치기 전까지 이 단계가 워크트리 계약에서 새 발언을 하나도 못 읽고 조용히 넘어간다.
   다음 사이클 Phase 3 넘김은 맞다 — 그 사이 틈이 있다는 것만 Final 이 알게 적어 두면 된다
4. **지워진 워크트리의 facets.** `facets_unmatched` 는 session-meta 의 `project_path` 가 지워진 워크트리를 가리키면 워크트리 폴더 이름으로 남긴다(라이브러리 217 줄 주석).
   `scripts/collect-kaizen-data.py:421` 은 `/.claude/worktrees/` 글자 앞에서 잘라 본 레포로 묶는다. 지금 facets 18 개는 경로가 전부 살아 있어 영향이 없다. notes `## 다음 사이클 메모` 에 한 줄이면 된다
5. **시험 셋 전체를 묶는 방법.** 2 번 고침보다 넓게, 새 시험 셋 세 파일의 sha256 앞 16 자리를 AR-02 에 걸 수도 있다(예행 판: `log-reflection-test.sh` `1260e58272c6b18f` ·
   `project-id-test.sh` `f84b7d5c17910c74` · `collect-status-test.sh` `8e9836d70c5d1a98`). 그러면 FIX 가 시험 답을 바꿀 때 개정 파일을 거쳐야 한다. 시험을 고칠 때마다 개정이 따라붙으니 고를 몫은 BUILD 다

## 기록

- 내 스크래치: `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p12r/`
  (`extract.sh` · `k/` 뽑은 블록 · `k2/` 고친 `m.sh` · `neg.sh` ~ `neg4.sh` 재현 · `pin.sh` 답 확인). `rh-cross` 예행 저장소와 풀어 둔 두 판은 잰 뒤 지웠다
- 이 파일의 SC-06 · SC-07 갈래 블록을 글자 그대로 뽑아 넣은 `m.sh`(`p12r/k3/`, `k3check.sh`)로 예행 판을 재면 `m SC-06` 이 `결과: 10 경우 중 불일치 0 rc=0` 두 줄 · `1 1 1 1 1 1` · `1 1`,
  `m SC-07` 이 `1 1 1 1` · `1` 이다
- DRAFT 스크래치 `p12d/` 는 읽기만 했다(`rehearse.sh` 를 내 폴더 대상으로 한 번 돌렸다)
- 작업 폴더에서 쓴 파일: 이 파일 하나

VERDICT: CHANGES

## 2 회차

- 대상: 같은 계약 초안(09:39 저장판, 봉인 전). 개정 파일은 아직 없다 — 봉인 전이라 맞다
- 검토일: 2026-09-25 · 검토자: REVIEW 에이전트
- 내 스크래치: `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p12r2/`
  (`k/` 계약에서 새로 뗀 세 블록 · `run.sh` 전체 재기 · `mut.sh` 변이 일곱 · `deadcheck.sh` · `deadcheck2.sh` 아래 1 번 · `rowpin.sh` 권하는 것 1 번 ·
  `log-reflection-test.fixed.sh` 고친 시험 사본). 작업 폴더에는 이 절만 덧붙였다

### 2 회차 결론

1 회차가 고치라고 한 것은 전부 들어갔고 값도 다시 재 보니 계약 표 그대로다. 새 결함 하나 때문에 한 번 더 고쳐야 한다.

SC-01 이 증거로 드는 시험 줄 가운데 `일치 codex 인자 --full-auto 없음` 은 떨어질 수가 없다. 가짜 codex 가 `--full-auto` 를 보면 호출 기록(`$CALLS`)을
적기 **전에** 종료 코드 2 로 끝나므로(시험 `log-reflection-test.sh` 20~31 줄), `grep -c '\[--full-auto\]' "$CALLS"` 는 늘 0 이다.
`일치 codex 성공 기록` 도 codex 가 실패하면 대체 경로가 남긴 기록으로 1 이 된다. 훅 codex 인자를 `--full-auto` 로 되돌린 사본에서 두 줄 다 `1` 이었다
(DRAFT `ctl2-out.txt` 의 `0 1 0 1 0`, 내 변이 M5 에서 `-s read-only` 를 두고 `--full-auto` 를 더해도 같다).

조건 전체로는 거짓 통과가 없다 — 같은 사본에서 `ro=` · `fullauto=` 값과 다른 시험 줄이 떨어진다. 그래도 1 회차 2 번과 같은 종류다: 조건 문구가
「`--full-auto` 없음 줄이 1」 을 증거로 적었는데 그 줄은 그 성질을 재지 못하고, 이 시험은 뒤에 `ci.yml` 로 들어가 킷의 유일한 되풀이 방지 검사가 된다.
고치면 SC-01 의 편집 전 훅 대조 값이 `17` 에서 `18` 로 바뀐다. 조건 줄 값이라 **봉인 전에만** 고칠 수 있다 — 그래서 권하는 것이 아니라 고칠 것으로 둔다.

### 1 회차 반영 확인

1. `m.sh` — SC-01 · SC-02 · SC-03 · SC-04 · SC-06 · SC-07 여섯 갈래의 시험 출력이 `| grep '^일치 '` 를 거친다. SC-06 · SC-07 끝에 시험 파일의 `check` 줄을 세는 `toks` 가 한 줄씩 있다.
   계약에서 세 블록을 새로 떼어(`p12r2/k/`) DRAFT 의 `p12d/k/` 와 비교했다 — `common.sh` · `m.sh` · `new-warnings.sh` 셋 다 글자 그대로 같다
2. 조건 문구 — SC-01 ~ SC-04 · SC-06 · SC-07 모두 「`grep '^일치 '` 가 남긴 줄에」 로 바뀌었다. SC-02 · SC-03 · SC-04 · SC-07 음성 대조 문장, SC-06 · SC-07 의 손으로 센 답과
   측정 끝(`m SC-06` 네 줄 · `m SC-07` 두 줄)이 1 회차가 적은 글자 그대로 들어갔다. SC-06 음성 대조에는 줄 번호(셋째 · 넷째)까지 붙었다 — `m SC-06` 출력 줄 순서와 맞다
3. `봉인 전 실측` 표 — SC-01 ~ SC-08 행이 고쳐졌다. DRAFT 의 `ctl2.sh` 가 사본마다 `m <조건 ID>` 전체 출력을 읽었고, `ctl2-out.txt` 의 값이 표와 한 글자씩 같다
4. Step 6.2 · 6.5 를 레포 스킬 파일에서 떼어 다시 돌렸다 — 조건 `29` · 기능 조건 `20` · `OK conditions=29` · `OK 미실측 0 건`, `##` 제목 열둘이 허용 목록 안, 서술 절의 조건 체크박스 0.
   커버리지 검출기(`contract-schema.md` 판과 같은 글)는 열두 조건에 `UNCOVERED` 를 냈고, 모두 `범위 경계` 절 해소 줄(235 · 242 · 244 줄)이 받는다 — 이번에 새로 걸린 SC-03 `haiku-4.5` 는 240 줄이 받는다
5. 권한 것 — 1 번(`codex=` 셋째 줄)은 들어갔다. 2 번(`sync-evals.py`)은 조건으로 걸지 않고 notes 로 돌렸는데 사유가 맞다: `scripts/sync-evals.py:32` 의 `TARGET_KITS` 에 reflect-kit 이 없다.
   3 번 · 4 번은 notes 에 적을 목록에 들어갔다. 5 번(시험 파일 sha256 고정)은 안 골랐고 대신 SC-06 · SC-07 의 답 줄을 잰다 — BUILD 몫이라 했으니 문제 삼지 않는다

### 2 회차에 다시 돌려 본 것

1. 예행 판(`p12d/rh-none`, 09:40 — 계약 초안과 조건 줄이 같고 `conditions_digest` · `locked_at` 두 줄만 더 있다)에서 스물아홉 조건 전부를 내 폴더로 쟀다 —
   표의 예행 판 값과 전부 같다(SC-08 셋째 줄 `codex=codex-cli 0.154.0` 포함). 시작 커밋 판(`p12d/rh-base`)에서 SC-01 ~ SC-04 · SC-06 · SC-07 도 표의 시작 커밋 판 칸과 같다
2. `collect-status-test.sh` 의 답을 시험 입력으로 손으로 다시 셌다. 7 일: codex 실패 4(A 둘 · B · C 빈 응답) · 대체 경로 실패 3(A 둘 · C) · 성공 1(B) · 분석 전 중단 2(D · F) ·
   실패 시도 5 · 고유 세션 4(A · C · D · F). all 은 E 가 더해져 5 · 4 · 6 · 5. facets 7 일 · alpha 는 f1 · f2 · f3 · f8 넷, 마찰 셋, B 가 기록돼 있어 없음 둘, 읽기 실패 f4 · f5.
   계약 문구와 같다
3. DRAFT 가 안 해 본 변이 일곱(`mut.sh`) — 전부 해당 시험 줄과 `m` 값이 떨어졌다:
   `log-tool-failure.sh` 표식 검사 삭제 → `m SC-04` `1 1 1 1 0 1 1` · `log-tool-failure.sh:0:no` / `log-reflection.sh` 표식 검사 삭제 → `1 1 0 1 1 1 1` · `log-reflection.sh:0:no` /
   codex 호출의 표식 삭제 → `0 1 1 1 1 1 1` / `--no-session-persistence` 삭제 → `m SC-03` `1 0 1 1` · `0 0` / `-s read-only` 를 두고 `--full-auto` 추가 → 불일치 7 · `0 1 0 1 0` · `ro=1 fullauto=1` /
   `err_line` 의 200 자 자르기 삭제 → `m SC-02` `1 1 1 1 0 1 1` / `err_line` 의 가리기 삭제 → `1 1 1 0 1 1 1`
4. 가지 현재 상태: 시작 커밋 `82b2493` 뒤 커밋 여섯이 전부 `Kaizen-Phase: kaizen-0924-p11-planning-kit` 서명이다. `reflect-kit/` 를 건드린 커밋 0.
   ER-03 경로 목록을 건드린 것은 `bbdebaf`(`docs/planning/`) 하나이고 p11 서명이라 `not_other` 가 건너뛴다

### 고칠 것 — 봉인 전에

**(1) 시험 두 곳.** `mock.py` 가 쓰는 `reflect-kit/evals/hooks/log-reflection-test.sh` 를 아래처럼 바꾼다. 고친 사본이 `p12r2/log-reflection-test.fixed.sh` 다.

```diff
 cat > "$W/bin/codex" <<'EOF'
 #!/usr/bin/env bash
+{ printf 'codex'; for a in "$@"; do printf ' [%s]' "$a"; done; printf ' analyzer=[%s]\n' "${REFLECT_KIT_ANALYZER:-}"; } >> "$CALLS"
 out=""; prev=""
 for a in "$@"; do
   if [ "$a" = "--full-auto" ]; then
@@
 done
-{ printf 'codex'; for a in "$@"; do printf ' [%s]' "$a"; done; printf ' analyzer=[%s]\n' "${REFLECT_KIT_ANALYZER:-}"; } >> "$CALLS"
 printf 'OpenAI Codex v0.154.0\n--------\nsandbox: read-only\n--------\nuser\n%s\n' "$(cat)" >&2
@@
-check "codex 성공 기록" 1 "$(recorded S1)"
+check "codex 성공 기록" 1 "$(grep -h -c 'skip-test-tag' "$LOGD"/reflections-*.md 2>/dev/null | awk '{s += $1} END {print s + 0}')"
```

호출 기록을 거부보다 먼저 적어야 `--full-auto` 가 기록에 남는다. 성공 기록은 가짜 codex 만 내는 태그 `skip-test-tag` 로 센다 — `recorded S1` 은 대체 경로가 남긴 기록도 센다.
시험 줄 이름은 그대로라 `m.sh` 는 안 바뀐다. 고친 시험으로 예행 판을 재면(`deadcheck.sh` · `deadcheck2.sh`):

| 판 | 시험 끝 줄 | `m SC-01` 셋째 · 넷째 줄 |
| --- | --- | --- |
| 예행 판 훅 | bash 5 · `/bin/bash` 3.2 모두 `결과: 24 경우 중 불일치 0` | `1 1 1 1 1` · `ro=1 fullauto=0` — 다섯째 줄(편집 전 훅)은 `결과: 24 경우 중 불일치 18 rc=1` |
| codex 인자를 `--full-auto` 로 되돌린 사본 | 불일치 8 | `0 0 0 0 0` · `ro=0 fullauto=1` |
| `-s read-only` 를 두고 `--full-auto` 를 더한 사본 | 불일치 7 | `1 0 0 0 0` · `ro=1 fullauto=1` — 「`--full-auto` 없음」 줄이 살아 있다는 대조 |

같은 고친 사본에서 `m SC-02` `1 1 1 1 1 1 1` · `1 1 0 0`, `m SC-03` `1 1 1 1` · `1 0`, `m SC-04` 첫 줄 `1 1 1 1 1 1 1` — 안 바뀐다. 이 파일 하나에 shellcheck 0 줄 · `bash -n` 통과.

**(2) 조건 문구 — SC-01.**

- 「편집 전 판 훅 폴더를 넣으면(`REFLECT_KIT_HOOKS`) 끝 줄 `결과: 24 경우 중 불일치 17` 에 종료 코드 1」 → 「… `결과: 24 경우 중 불일치 18` 에 종료 코드 1」
- 측정 끝 「… · `결과: 24 경우 중 불일치 17 rc=1`」 → 「… · `결과: 24 경우 중 불일치 18 rc=1`」
- 「codex 경우 다섯 줄(`-s read-only` · `--full-auto` 없음 · codex 성공 시 대체 경로 안 부름 · 기록 남음 · 실패 줄 없음)」 →
  「codex 경우 다섯 줄(`-s read-only` · `--full-auto` 없음 · codex 성공 시 대체 경로 안 부름 · codex 가 낸 기록이 남음 · 실패 줄 없음)」
- 끝에 음성 대조 한 구절을 더한다 — 「음성 대조: `-s read-only` 를 두고 `--full-auto` 를 더한 사본은 `m SC-01` 셋째 줄이 `1 0 0 0 0`, 넷째 줄이 `ro=1 fullauto=1`」

**(3) 서술 절.**

- `개선안 초안` 절의 `mock.py` sha256 앞 16 자리(`714450452fff4513`)를 새 값으로 바꾸고, 시작 커밋 판 새 사본에서 `mock applied 12` · 두 번째 실행 `MOCK_FAIL` 을 다시 확인한다
- `봉인 전 실측` 표 SC-01 행: 예행 판 칸 끝 값 `불일치 17 rc=1` → `불일치 18 rc=1`. 대조 칸 「`-s read-only` 를 `--full-auto` 로 되돌린 사본 → 불일치 7 · 셋째 줄 `0 1 0 1 0`」 →
  「… → 불일치 8 · 셋째 줄 `0 0 0 0 0`」 에, 위 표 셋째 행을 더한다
- 새 `mock.py` 로 예행 저장소(`rh-none`)를 다시 만들고 스물아홉 조건을 한 번 다시 잰다 — SC-01 다섯째 줄 밖에는 값이 안 바뀌어야 한다. 시험 파일은 줄을 옮기고 한 줄을 바꾼 것이라 143 줄 그대로다 — ER-02 `added=626` 도 그대로여야 한다
- Step 6.2 · 6.5 다시 — 조건 29 · 기능 조건 20 그대로다

### 2 회차에 권하는 것 — 판정에 넣지 않는다

1. **SC-07 세션 줄 둘도 시험 파일에서 잰다.** 조건 문구는 「… 과 세션 줄 둘」 까지 답으로 적었는데 지금 측정은 머리 줄만 읽는다. FIX 가 구현과 시험 답에서 세션 줄을 같이 지우면
   `m SC-07` 은 그대로다. `m.sh` SC-07 둘째 `toks` 에 두 토큰
   `'- S-miss · $(jq -r .start_time "$W/usage/session-meta/S-miss.json") · $W/repos/alpha — missed friction'` ·
   `'- S-wt · $(jq -r .start_time "$W/usage/session-meta/S-wt.json") · $W/wt/alpha-wt — worktree friction'` 를 더하면 둘째 줄이 `1 1 1` 이 된다
   (예행 판 시험 파일 `1 1`, S-wt 줄을 지운 사본 `1 0` — `rowpin.sh`). 고르면 조건 문구 · 측정 끝(`1 1 1 1` · `1 1 1`) · 표를 같이 고쳐야 하니 봉인 전에만 된다.
   1 회차 5 번(시험 셋 sha256 고정)을 고르면 이것과 SC-06 의 `⚠ 수집 멈춤` 줄까지 한 번에 묶인다 — 여전히 BUILD 몫이다
2. 이 기계 디스크 여유가 1.4 GB 다. 예행 변형을 다시 만들 때 한 번에 하나씩 만들고 지운다

VERDICT: CHANGES
