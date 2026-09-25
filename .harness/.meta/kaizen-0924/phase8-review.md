# 카이젠 2026-09-24 Phase 8 (infra-kit) 계약 검토

- 대상: `.harness/sprint-contract-kaizen-0924-p08-infra-kit.md` (봉인 전 초안, 641 줄, 조건 28 · 기능 조건 18)
- 개정 파일: 아직 없다 (`.harness/sprint-amendments-kaizen-0924-p08-infra-kit.md` 없음 — 봉인 전이라 정상)
- 검토 기준 커밋: `4a8ec55` (작업 폴더 HEAD 와 같다)
- 검토자: 독립 Claude 검토자 (Codex 대신 — 러닝북 `사용자 승인(5 단계) 대체`)

## 결론

**꼭 고칠 곳은 한 군데다 — ER-03 의 기대 출력.** 조건 문장은 notes 문자열을 「각각 1 회 이상」 요구하는데, 측정 절의 기대 출력은 「1 을 열일곱 번」으로 딱 1 을 요구한다.
진짜 notes 는 같은 키를 여러 절에 적기 마련이라 2 이상이 나온다. Phase 7 QA 가 바로 이 모양(`3 1 1 1 2 1 2 …`)을 만나 「예행 특유값」이라고 해석해서 넘겼다
(`.harness/sprint-feedback-kaizen-0924-p07-backend-kit.md:68`). 같은 해석 싸움을 이번에는 봉인 전에 없앤다.

나머지는 계약대로 돌려 보니 전부 맞았다. 측정 명령 · 봉인 전 실측 · 양성 대조 · 음성 대조가 촘촘하고, 범위와 공유 파일 처리도 러닝북과 맞다.
아래 「권하는 것」은 봉인 전에 하면 좋지만 안 해도 판정은 바뀌지 않는다.

## 직접 돌려 본 것

전부 내 폴더 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p8r/` 에서 돌렸다. 작업 폴더 파일은 이 검토 파일 말고 건드리지 않았다.

1. **계약 본문과 초안이 돌린 도우미가 같은가.** 계약 파일의 `## 회귀 게이트` 절 bash 블록 셋을 `p8d/extract.py` 로 뽑아 `p8r/k/` 에 저장하고 초안 폴더 `p8d/k/` 와 `cmp` —
   `same common.sh` · `same m.sh` · `same new-warnings.sh`. 초안 사본 `p8d/contract.draft.md` 도 계약 파일과 같다(`draft-same`).
2. **예행 저장소를 새로 만들어 조건 스물여덟을 전부 다시 쟀다.** `bash p8d/rehearse.sh <계약> p8r/rh none` → `rehearsal ready 324f16f var=none`.
   `p8r/run.sh` 로 `m` 을 조건마다 불렀다(`p8r/run-e.txt` · `p8r/run-e2.txt`). 스물여덟 조건 출력이 계약 `회귀 게이트` 표의 「예행 판」 칸과 한 글자도 다르지 않았다. 예:
   - SK-07 → `1 1 1 1 1 1 1` · `ka exit=1 refs=3 viol_lines=2 VIOLATION=1` · `ok exit=0 refs=3 viol_lines=0 VIOLATION=0`
   - SK-08 → `1 1 1` · `0` · `unset_rc=127 unset_msg=1 set_rc=0`
   - AR-01 → `0` · `0 13` · `0` · `SEAL_OK` · `scope_same=1` · `1`
   - DG-05 → `10 0` · `1 0` · `stale_rc=0 0`, DG-06 → `scope-isolation: PASS` · `doc-contracts: PASS` · `doc_checked=2 doc_mine=0` · `violators=0 mine=0`
3. **시작 커밋 판도 다시 쟀다**(`p8r/run-b.txt`). SK-01 ~ SK-11 · AR-02 · RE-02 · AP-01 · AP-03 이 표의 「시작 커밋 판」 칸과 같다 — 예: SK-05 여섯째 값 `4`, SK-06 다섯째 값 `4`, SK-09 첫 값 `4`, SK-08 둘째 값 `1`.
4. **초안이 안 해 본 바꿔치기 여덟 개를 따로 넣어 봤다**(`p8r/probe.sh`). 전부 요구값에서 벗어났다 — 측정이 실제로 잡는다.

   | 바꾼 것 | 출력 |
   | --- | --- |
   | infra-test 보고 예시 둘째 항목의 `통제 불가 사유` 줄 삭제 | SK-05 셋째 줄 `2 2 1 2` |
   | reviewer 예시 3 행을 옛 「1차 … fallback」 꼴로 되돌림 | SK-06 셋째 줄 `1 1 0` · 다섯째 값 `1` |
   | principle-index cicd 경로를 없는 파일로 | AR-02 첫 줄 `1 docs/infra/platform/cicdX.md 0` |
   | cicd.md 판정 표 한 칸 문구 변경 | SK-01 셋째 줄 `table_same=0` |
   | 변수 줄은 두고 kubeconform 명령만 `1.37.1` 고정 | SK-08 `1 0 1` · `1` |
   | research-log 새 항목 앞에 다른 항목 끼움 | SK-11 `first=0` |
   | README 스킬 표 한 줄 삭제 | SK-10 `3 1 3` |
   | 모의 notes 에 `backend-family:P3` · `plugin.json` 을 한 줄 더 | ER-03 둘째 줄 `2 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1` ← 아래 필수 수정의 근거 |

5. **ER-03 문자열이 빠지면 잡히는가**(`p8r/probe2.sh`). 모의 notes 에서 `` - `plugin.json` — Final `` 줄을 지운 사본 → 둘째 줄 `1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1`. 잡힌다.
6. **계약 저장 검사.** Step 6.2 두 명령 → `28` · `18`. 머리 제목 열둘이 전부 허용 목록 안(`회귀 게이트` · `GAP 분석` 은 앞부분 일치). `[미실측]` 0 건.
7. **러닝북 검증 목록 중 계약이 뺀 `sync-docs.py --check-only`.** 예행 저장소에서 시작 커밋 판과 끝 판 출력이 같고(`SAME`) 둘 다 종료 코드 0. 뺀 이유(infra-kit README 에 자동 갱신 구간이 없다 · 머리 설정은 AP-04 가 잰다)가 맞다.
8. **번역투 정규식** `K02` 가 `tone-kit/references/locale-korean.md` §2 치환표 grep 열 여섯과 같다.

## 볼 것별 판단

### 1. 조건마다 실패 상태를 한 문장으로 쓸 수 있는가 — 된다

| 조건 | 실패 상태 |
| --- | --- |
| SK-01 | cicd.md 원칙 7 이 없거나 원칙 6 뒤 · `## 수치/기준값` 앞이 아니거나, 스물한 문장 중 하나가 빠지거나, 코드 블록 · 판정 표가 `/sprint` Step 3 과 한 글자라도 다르거나, 머리 설정이 `0.2.0` · `2026-09-25` 가 아니면 실패 |
| SK-02 | infra-guide Gotcha 14 가 없거나 여덟 문장 중 하나가 빠지거나 Gotcha 번호가 1 ~ 14 로 이어지지 않으면 실패 |
| SK-03 | 두 cicd 행 중 하나에 새 키워드가 없거나, 두 행 키워드 칸이 다르거나, 옛 사본이 바뀌면 실패 |
| SK-04 | 사례 6 이 없거나 모양이 다르거나, `run-evals.py infra-kit` 이 6 통과 · 0 실패가 아니거나, README 옛 문구가 남거나 새 문구가 없으면 실패 |
| SK-05 | infra-test Gotcha 12 · Step 8 · 상태어 문서 중 한 곳이라도 네 칸 문장이 없거나, 보고 예시 두 건이 네 칸씩이 아니거나, 옛 표기가 한 줄이라도 남으면 실패 |
| SK-06 | infra-audit 세 자리 · reviewer 출력 포맷 중 하나라도 네 칸이 아니거나, reviewer §9 가 한 글자라도 바뀌거나, 옛 표기 다섯이 한 줄이라도 남으면 실패 |
| SK-07 | Step 7 알려진 답 문단이 없거나, `$END` 판 골격을 그 입력으로 돌린 결과가 문단 값(참조 3 · 줄 2 · 집계 1 · exit 1)과 다르면 실패 |
| SK-08 | infra-kit 에 고정 `-kubernetes-version 1.` 이 남거나, 변수 줄이 없거나, 변수 없이 돌려도 종료 코드 0 이면 실패 |
| SK-09 | infra-kit 에 「1.7+ native state encryption」 꼴이 한 줄이라도 남거나 네 자리 새 문구 중 하나가 없으면 실패 |
| SK-10 | README cicd 요약 · 이력 줄 정정 중 하나가 없거나 표 구성(`4 1 3`)이 바뀌면 실패 |
| SK-11 | research-log 첫 항목이 새 항목이 아니거나, 아홉 문장 중 하나가 빠지거나, 머리 설정이 `1.4.0` · `2026-09-25` 가 아니거나, 2026-08-13 항목부터 끝까지가 바뀌면 실패 |
| SC-00 | 이 Phase 서명 커밋이 `release.sh` · marketplace · 어떤 킷의 `plugin.json` 을 건드리면 실패 |
| ER-01 | 열세 파일의 새 URL 이나 notes 의 URL 가운데 근거 파일에 없는 것이 하나라도 있거나 notes 가 끝 판에 없으면 실패 |
| ER-02 | 더한 줄에 번역투 여섯 꼴이 한 건이라도 있으면 실패 |
| ER-03 | notes 가 커밋되지 않았거나, 열일곱 문자열 중 하나라도 0 이거나, 공유 경로를 건드린 커밋 가운데 다른 Phase 서명이 없는 것이 있으면 실패 |
| AR-01 | 서명 없는 커밋이 두 폴더를 건드렸거나, 서명 커밋이 열세 파일 밖을 건드렸거나 열세 파일 중 하나를 안 건드렸거나, 봉인이 깨졌거나 없거나, 범위 선언 블록이 열세 파일과 다르면 실패 |
| AR-02 | 색인 cicd 행이 원칙 7 이 있는 파일로 풀리지 않거나, 읽는 쪽 참조 줄 다섯 중 하나가 바뀌거나, 소비처 표가 세 파일이 아니면 실패 |
| RE-01 · DG-01 · DG-03 · DG-04 | 해당 없음(N/A) 사유가 거짓 — 각 측정이 0 이 아니면 실패 |
| RE-02 | 판정 표 머리 줄이 `docs/infra/platform/cicd.md` 한 곳에만 있지 않으면 실패 |
| AP-01 | 더한 줄에 infra-kit 버전 값이 있으면 실패 |
| AP-03 | 더한 펜스 줄이 둘이 아니거나 마크다운 열두 파일에 언어 힌트 없는 여는 펜스가 있으면 실패 |
| AP-04 | 다섯 파일 중 하나라도 첫 머리 설정 블록이 바뀌거나 `name:` 줄이 1 개가 아니면 실패 |
| DG-02 | 열두 파일 중 하나라도 더한 줄에 새 경고가 있거나, 린터가 안 돌았거나, `evals.json` 을 JSON 으로 못 읽으면 실패 |
| DG-05 | V1 ~ V10(검증 스크립트의 검사 열 가지) 중 하나라도 `ERROR` · `FAIL` 이거나, sync-evals 가 infra-kit 어긋남을 내거나, 옛 값 검사가 열세 파일을 가리키면 실패 |
| DG-06 | scope-isolation · doc-contracts 가 실패인데 그 원인에 이 Phase 서명 커밋이 있거나, 원인 목록을 못 읽었으면 실패 |

### 2. 측정이 의도를 실제로 재는가 — 재다. ER-03 기대 출력 하나만 틀렸다

- 문장 조건(SK-01 ~ SK-06 · SK-09 ~ SK-11)은 절 · 줄 단위로 잘라 문장 전체를 센다. 토큰 하나를 지운 사본 85 개 전부 출력이 바뀌었고(`p8d/del-out.txt` — `DROP` 85), 내 바꿔치기 여덟도 전부 잡혔다.
- 알려진 답이 필요한 곳에 있다. SK-01 은 `/sprint` Step 3 원문과 글자 비교, SK-07 은 골격을 실제로 돌린 값, SK-08 은 변수 줄을 실제로 돌린 종료 코드, AR-02 는 색인 경로를 실제로 풀어 제목을 찾는다.
- 0 을 기대하는 측정(SK-05 여섯째 · SK-06 다섯째 · SK-08 둘째 · SK-09 첫째 · ER-01 · ER-02 · ER-03 셋째 · AR-01 ①②③ · AP-01)은 시작 커밋 판이나 예행 변형에서 0 이 아닌 값이 나오는 것을 확인했다.
- 러닝북이 짚은 측정 구멍 넷이 다 막혀 있다 — 상한은 `END_UNRESOLVED` 로 멈추고, 도우미 함수가 없으면 `HELPER_MISSING` 으로 멈추고, 공유 파일은 경로로 직접 세고(`not_other`), 옛 판 비교는 파일마다 한다(`added` · ER-01).
- **ER-03 둘째 줄만 문제다.** 조건 문장(「각각 1 회 이상」)과 기대 출력(「1 을 열일곱 번」)이 서로 다르다. 모의 notes 는 키를 한 번씩만 적어 봉인 전 실측이 1 로 나왔을 뿐, 진짜 notes 는 `backend-family:P3` · `plugin.json` · `harness/skills/sprint/SKILL.md` 를 절마다 되풀이할 가능성이 크다(위 표 마지막 행). 아래 필수 수정 참고.

### 3. 처리 배정표 Phase 8 행이 빠짐없이 다뤄졌는가 — 다뤄졌다

- `.claude/kaizen-input/insights-report.md` 의 `배정` 칸이 `Phase 8` 인 행은 `backend-family:P3` 하나다(`awk -F'|' '{print $4}'` 로 세면 `Phase 8` 1 건). 계약 `## 배경` 표 첫 행이 SK-01 ~ SK-04 · AR-02 로 반영한다. 비고 「기준 커밋 가르기 규칙 세 곳을 하나로」는 Phase 4 가 정한 `/sprint` Step 3 을 기준 원본으로 두고 글자 그대로 옮기는 것으로(SK-01 · RE-02) 다룬다.
- `F09`(Phase 4 행)의 비고, `Phase 별 적용 힌트` 의 Phase 8 줄(내 변경 · 기준 커밋에서 이미 실패 · 환경)도 원칙 7 의 다섯 갈래 안에 들어간다.
- 앞 Phase 넘김 셋 — Phase 1 `infra-test/SKILL.md:37`(SK-05), Phase 4 판정 세 줄(SK-01), Phase 7 README `:54`(SK-04) — 이 전부 조건이 됐다. 러닝북 `Phase 별 추가 과제` 에 Phase 8 줄은 없다.
- 데이터 풀 §0.5 [infra] 세 건 가운데 `미분류` 기억은 통과 근거로 쓰지 않았다고 적었다. Gotcha 14 의 「실측(2026-09-18)」 은 §0-b `e863512e` 기록과 맞다.

### 4. 범위가 러닝북 표의 「고쳐도 되는 범위」 안인가 — 안이다

고치는 열세 파일이 전부 `infra-kit/` 또는 `docs/infra/` 아래다. 새 파일은 없다. AR-01 ② 가 서명 커밋이 이 열세 파일 밖을 건드리면 잡고, ① 이 서명 없는 커밋이 두 폴더를 건드리면 잡는다.

### 5. 공유 파일을 건드리려 하지 않는가 — 않는다

marketplace · `plugin.json` 버전 · 루트 README · 루트 CLAUDE.md · `docs/` HTML · 처리 배정표 · 감사 기록 · 실패 횟수 파일 · 자동 검사 설정(`.github/workflows/ci.yml`) · `.harness/stale-values.yaml` 을 전부 notes 로 넘기고(ER-03 문자열), `not_other` 로 그 경로를 건드린 커밋을 센다. 예행 변형 셋에서 1 이 나온다.

### 6. 조건끼리 부딪히는가 — 부딪히지 않는다

- AR-01 ② 의 「열세 파일 전부」와 SK 조건들이 요구하는 파일별 변경이 같은 집합이다.
- SK-06 의 reviewer §9 불변과 SK-06 (d) 의 `## 출력 포맷` 변경은 다른 절이다. AP-04 의 머리 설정 불변과 본문 변경도 겹치지 않는다.
- ER-03 이 notes 에 `.harness/stale-values.yaml` 을 적으라고 하면서 그 파일을 건드리지 말라는 것은 충돌이 아니다 — 적기만 한다.
- 부딪히는 곳은 ER-03 한 조건 안의 문장과 기대 출력뿐이다(위 2 번).

## 고칠 문구 (필수)

### ER-03

조건 줄 측정 괄호 안의 이 글을

```text
Then: 세 줄이 `notes_committed=1` · `1 ` 열일곱 개 · `0`.
```

이렇게 바꾼다.

```text
Then: 첫 줄 `notes_committed=1` · 둘째 줄 값 열일곱 개가 모두 1 이상(0 이 하나라도 있으면 실패. 같은 문자열을 여러 절에 적으면 2 이상이 정상이다 — 예행 판은 모의 notes 라 모두 1) · 셋째 줄 `0`.
```

같은 괄호의 양성 대조 문장 끝에 이 문장을 더한다.

```text
문자열 삭제 대조: 모의 notes 에서 `- `plugin.json` — Final` 줄을 지운 사본에서 둘째 줄 여섯째 값 0.
```

`회귀 게이트` 절 표의 ER-03 행도 맞춘다. 「예행 판 (요구값)」 칸의

```text
`notes_committed=1` · `1` 열일곱 · `0`
```

을

```text
`notes_committed=1` · 열일곱 값 모두 1 이상(예행 모의 notes 는 모두 1) · `0`
```

으로 바꾸고, 「양성 · 음성 대조」 칸 끝에 아래 글을 더한다.

```text
 · 모의 notes 에서 `plugin.json` 줄 삭제 → 둘째 줄 여섯째 값 0
```

측정 명령(`m.sh` 의 `ER-03)` 갈래)은 바꾸지 않는다. 조건 줄이 바뀌므로 봉인 값은 이 수정 뒤에 계산한다.

## 권하는 것 (선택 — 판정에 영향 없음)

1. **아직 남는 「1.7+」 자리를 다음 사이클 목록에 빠짐없이 적는다.** 계약 `## 범위 경계` 의 「그대로 둔 곳」 과 research-log 「다음 사이클 후보」 는 `audit-criteria.md:104` · `init-checklist.md:132` 의 「1.7+ mocking」 만 적는다.
   같은 주장이 `infra-kit/skills/infra-test/SKILL.md:24`(Gotcha 8 「OpenTofu 1.7+는 `tofu test`에서 mocking 지원」)에 있고, 근거 파일이 다루지 않은 다른 주장
   「OpenTofu 1.7+ write-only 인수」 가 `infra-test/SKILL.md:26`(Gotcha 10)에 있다. `mock.py` 의 research-log 치환에서
   `- 「Terraform 1.10+ ephemeral」 · 「1.7+ mocking」 의 도입 버전 — 근거 파일이 확인하지 못했다(§5)` 를
   `- 「Terraform 1.10+ ephemeral」 · 「1.7+ mocking」(audit-criteria · init-checklist · infra-test Gotcha 8) · 「OpenTofu 1.7+ write-only 인수」(infra-test Gotcha 10) 의 도입 버전 — 근거 파일이 확인하지 못했다(§5)` 로 바꾸고,
   `## 범위 경계` 의 notes 줄에도 같은 두 자리를 더한다. 이 줄은 SK-11 토큰 · SK-09(infra-kit 만 본다) · ER-01(URL 없음)에 걸리지 않는다. 바꾸면 DG-02 · ER-02 를 다시 돌린다.
2. **네 칸이 아닌 채 남는 두 자리를 notes 「그대로 둔 곳」 에 이유와 함께 적는다.** infra-test Step 7 결과 분류 표의 `도구 미설치 · 클러스터/레지스트리 접근 불가` 행(「`[미검증] TOOL_OR_ENV_MISSING` (+ 재검증 명령)」 — 스크립트 상태 표라 둔다)과
   infra-audit `## Unverifiable Summary` 블록의 `env_gaps` 줄(「1차 도구 시도, fallback 시도, 실패 로그, 통제 불가 사유 + 재검증 명령」 — 복제 조항 5 와 4 요건 이름을 따르므로 둔다). 둘 다 옛 표기 목록에 안 걸리지만, 읽는 사람이 한 파일 안에서 두 가지 이름을 보게 된다.
3. **SK-07 문단의 입력 설명을 한 번에 읽히게.** 「워크플로 하나(`actions/checkout` 스텝이 있고 원격 `uses:` 셋 중 둘이 `@v4` 같은 태그)」 는 checkout 이 셋 안에 드는지 한 번 더 생각해야 한다.
   예: 「워크플로 하나(원격 `uses:` 셋 — `actions/checkout@v4` · 40 자 커밋 번호(SHA)로 고정한 액션 하나 · `@v4` 태그 액션 하나)」. 측정 토큰은 이 괄호 밖이라 SK-07 출력은 그대로다.
4. **`## 배경` 의 Gotcha 4 문장.** infra-kaizen Gotcha 4 는 관심사를 「1~2 개로 제한」 하고 「3 개를 넘으면」 미루라고 한다. 「상한에 맞춰 셋으로」 보다는 「셋째(사실 정정)는 근거 파일 §3 · §5 가 틀렸다고 확인한 문장을 지우는 일이라 함께 한다」 처럼 이유를 적는 편이 정확하다.
5. **`## 배경` 의 「N 카테고리」 문장.** SK-04 는 「7 카테고리 구조 감사」 를 문장 전체로 재므로 겹칠 걱정은 없지만, 「그 낱말을 재지 않아」 는 사실과 조금 다르다. 「낱말 하나가 아니라 문장 전체로 재서 겹치지 않는다」 가 맞다.
6. **README 의 「평가 사례 6 개」.** 검사 개수는 숫자를 박지 않기로 한 조건 안에서 사례 수는 숫자를 박는다. backend-kit README(Phase 7 「평가 사례 8 개」)와 같은 모양이라 이번에는 두고, 두 킷을 함께 다음 사이클 메모에 올리는 것을 권한다.

## 앞 Phase 에서 넘어온 측정 구멍 대조 (러닝북 네 항목)

| 러닝북 항목 | 이 계약 |
| --- | --- |
| 건드리면 안 되는 파일은 경로로 직접 센다 | ER-03 셋째 값 `not_other` · AR-01 ① `unsigned_on` — 경로로 센다 |
| 상한을 못 구하면 멈춘다 | `common.sh` 가 `END_UNRESOLVED` 로 종료 코드 2 |
| 셸 함수 정의 확인 | `m` 이 도우미 열셋을 `type` 으로 확인하고 없으면 `HELPER_MISSING` |
| 파일마다 옛 판과 비교 | `added` · ER-01 이 파일마다 `git diff --no-index` · `comm` |

VERDICT: CHANGES

## 2 회차

- 대상: 같은 계약 초안(650 줄, 조건 28 · 기능 조건 18). 1 회차 뒤 2026-09-25 07:24 에 고쳐졌다
- 개정 파일: 아직 없다(봉인 전이라 정상)
- 기준 커밋: `4a8ec55` (작업 폴더의 지금 커밋과 같다)
- 무엇이 바뀌었나: 1 회차 예행 저장소(`p8r/rh`)의 봉인 커밋 `8b7188b` 에 들어 있던 계약 사본에서 봉인 두 줄을 뺀 판과 지금 계약을 `diff` 했다 — 바뀐 곳 아홉 군데, 640 → 650 줄(`p8r2/contract.diff`)
- 내 폴더: `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p8r2/`. 작업 폴더 파일은 이 검토 파일 말고 건드리지 않았다

### 결론

1 회차 필수 수정(ER-03 기대 출력)은 세 자리 모두 제안 문구 그대로 들어갔고, 선택 권고 여섯도 전부 반영됐다. 지금 계약으로 예행을 새로 만들어 조건 스물여덟을 다시 쟀더니 실측 표와 한 글자도 다르지 않았다.

**새로 고칠 곳이 하나 있다 — ER-03 조건 줄이 Final 단계에 넘기는 옛 값 등록 안내가 사실과 다르다.** 안내대로 하면 이 Phase 가 쓰는 research-log 기록 줄에 거짓 경보가 나고,
정작 옛 값이 있던 infra-kit 파일은 검사 범위 밖이라 지켜지지 않는다. 1 회차가 놓친 것이다. 봉인 전이라 조건 줄 글만 고치면 되고 측정은 바뀌지 않는다.

### 1 회차 지적 반영 확인

| 1 회차 지적 | 지금 계약 | 확인한 것 |
| --- | --- | --- |
| 필수 — ER-03 Then 문장 | `:601` | 제안 문구와 글자 그대로 같다 |
| 필수 — ER-03 대조 문장 | `:604` 문자열 삭제 대조 · `:605` 중복 대조 | 둘 다 직접 재서 적힌 값이 나왔다(아래 3) |
| 필수 — 실측 표 ER-03 행 | `:529` | 요구값 칸 · 대조 칸 모두 제안대로다 |
| 필수 — 측정 명령은 그대로 | `## 회귀 게이트` 절의 bash 블록 셋 | 지금 계약에서 뽑은 `common.sh` · `m.sh` · `new-warnings.sh` 가 1 회차 사본(`p8r/k`) · 초안 사본(`p8d/k`) · 재예행 사본(`p8x/k`) 과 `cmp` 로 모두 같다 |
| 선택 1 — 남는 「1.7+」 자리 | `:54-55` · `:208-209` · 모의 치환의 research-log 다음 사이클 줄 | 근거 파일에 `mock` 낱말이 한 번도 없다. 「1.7+ mocking」 을 「확인하지 못했다(§5)」 가 아니라 「다루지 않았다」 로 가른 초안 쪽이 1 회차 제안보다 정확하다. write-only 는 근거 파일 `:104` 에 Terraform 쪽만 있고 OpenTofu 버전은 없어 「다루지 않았다」 가 맞다 |
| 선택 2 — 네 칸 아닌 채 남는 두 자리 | `:211-213` | infra-audit `env_gaps` 줄(`:99` · `:115`)과 infra-test Step 7 표 행(`:432`)의 실제 문구와 맞다 |
| 선택 3 — SK-07 입력 설명 | 킷 문단(모의 치환) · 계약 `:574` | 도우미의 `ka` 입력(`actions/checkout@v4` · `setup-node@` 40 자 · `configure-aws-credentials@v4`)과 맞다. 골격 규칙 1 이 checkout 존재 검사라 새로 넣은 「checkout 규칙은 통과한다」 도 맞다 |
| 선택 4 — Gotcha 4 문장 | `:31-33` | infra-kaizen Gotcha 4 원문(「1~2 개로 제한」 · 「3 개를 넘으면 다음 사이클로」)과 맞고 셋째를 함께 하는 이유가 적혔다 |
| 선택 5 — 「N 카테고리」 문장 | `:29` | 제안대로다 |
| 선택 6 — README 사례 수 | `:215` | 다음 사이클 메모로 두 킷을 함께 적는다 |

### 직접 돌려 본 것

1. **새 예행.** `bash p8d/rehearse.sh <지금 계약 사본> p8r2/rh none` → `rehearsal ready 17f429d var=none`. 모의 치환은 지금 판(`p8d/mock.py`, 07:20)이 들어갔다 — 예행 research-log 에 「도입 버전 표기」 줄, infra-test 에 「checkout 이 있어 checkout 규칙은 통과한다」 가 각각 1 줄.
2. **조건 스물여덟.** 지금 계약에서 뽑은 도우미(`p8r2/k`)로 `p8r2/run.sh` 를 bash 5 와 `/bin/bash` 3.2 로 돌렸다. 두 출력이 서로 같고, 초안이 표를 만든 `p8d/final-run.txt` 와 `diff` 가 없다(`p8r2/run-e.txt` · `p8r2/run-e32.txt`). 예: ER-03 `notes_committed=1` · `1` 열일곱 · `0`, AR-01 `0` · `0 13` · `0` · `SEAL_OK` · `scope_same=1` · `1`, DG-05 `10 0` · `1 0` · `stale_rc=0 0`.
3. **ER-03 새 대조 둘**(`p8r2/er03-probe.sh`, 초안 스크립트에서 도우미 폴더만 바꿈). 모의 notes 에서 `` - `plugin.json` — Final `` 줄 삭제 → 둘째 줄 `1 1 1 1 1 0 1 …`. 두 키를 한 줄씩 더 → `2 1 1 1 1 2 1 …`, 셋째 줄 `0`. 계약 `:604-605` 와 같다.
4. **봉인 뒤 조건 한 글자 변경**(`p8x/rh-tamper`). AR-01 → `0` · `0 13` · `1` · `SEAL_BROKEN` · `scope_same=1` · `1`. 표와 같다.
5. **더한 줄 수** `added | grep -c .` → `159`. ER-02 표 값과 같다.
6. **저장 검사.** Step 6.2 두 명령 → `28` · `18`. `[미실측]` 0 건. `##` 제목 열둘은 1 회차와 같다. 커버리지 검출기를 `harness/references/contract-schema.md` 원문에서 뽑아 돌렸다(초안 사본 `p8x/coverage-detector.sh` 와 같다) — `UNCOVERED` 열 줄이 `p8x/gate65-final.txt` 와 같고, 전부 `## 범위 경계` 의 해소 줄에 있다.
7. **번역투 정규식**을 계약에서 바뀐 줄과 모의 치환에서 바뀐 줄에 돌렸다 → 둘 다 0.
8. **옛 값 등록 시험**(아래 새 결함의 근거). 예행 판을 복제한 `p8r2/stale` 에서 `python3 scripts/check-stale-values.py` → 종료 코드 0 · 「되살아난 옛 값 없음」. 등록부 끝에 두 값(`1.7+ native state encryption` · `-kubernetes-version 1.30.0`)을 더하고 다시 → 종료 코드 1, 걸린 것은 `docs/infra/research-log.md:37 '1.7+ native state encryption'` 한 건뿐이다.

### 새 결함 — ER-03 의 옛 값 등록 안내

ER-03 조건 줄(`:600`)은 notes 에 `.harness/stale-values.yaml` 을 「(Final — 「1.7+ native state encryption」 · `-kubernetes-version 1.30.0` 등록)」 으로 넘기게 한다. 이대로면 두 가지가 틀어진다.

- `scripts/check-stale-values.py` 는 docs-site 소스 폴더 열둘만 훑는다(`SOURCE_DIRS` `:45-51`, 머리 설명 `:21-23` 「`infra-kit/references/*` … 같은 비 docs-site 문서는 훑지 않는다」). 두 옛 값이 있던 자리(`infra-kit/references/` · `infra-kit/skills/`)는 범위 밖이다. 등록해도 그 파일들에서 옛 값이 되살아나는 것을 못 잡는다 — `-kubernetes-version 1.30.0` 은 범위 안에서 0 건이다.
- 범위 안인 `docs/infra/` 에는 이 Phase 가 쓰는 research-log 변경 내역 줄이 그 옛 문자열을 그대로 담는다(「OpenTofu 1.7+ native state encryption」 네 자리에서 버전을 뺐다). 그래서 등록하는 순간 이 기록 줄 하나만 걸린다(위 8).

Final 이 안내대로 하면 자기 기록 줄에 거짓 경보를 보고 이유를 다시 캐야 하고, 등록한 값은 infra-kit 을 지켜 주지 않는다. 이 Phase 의 DG-05 (c)(검사 출력에 열세 파일 경로 0 건)가 지키려는 것과도 같은 파일에서 어긋난다.
안내 글만 사실대로 고치면 된다. 측정(`m.sh` `ER-03)` 갈래)은 토큰 `.harness/stale-values.yaml` 만 보므로 바뀌지 않는다.

### 고칠 문구 (필수)

ER-03 조건 줄(`:600`)의 이 글을

```text
`.harness/stale-values.yaml` (Final — 「1.7+ native state encryption」 · `-kubernetes-version 1.30.0` 등록)
```

이렇게 바꾼다.

```text
`.harness/stale-values.yaml` (Final — 등록할지 판단한다. 옛 값 검사 check-stale-values.py 는 docs-site 소스 폴더만 훑어 infra-kit 안의 두 옛 값 「1.7+ native state encryption」 · `-kubernetes-version 1.30.0` 을 보지 못하고, 앞의 것을 그대로 등록하면 이 Phase research-log 항목의 변경 내역 줄이 걸리므로 그 파일을 allow 에 사유와 함께 둔다)
```

사본에 적용해 봤다(`p8r2/contract.fix.md`). Step 6.2 두 명령 `28` · `18` 그대로, 커버리지 검출기 출력 그대로(새 경로를 백틱에 넣지 않았다), 계약에서 뽑은 도우미 셋 그대로, 이 줄의 번역투 0.
조건 줄이 바뀌므로 봉인 값은 이 수정 뒤에 계산한다. 실제 notes 의 넘김 줄에도 같은 내용을 적는다. 모의 notes 는 고치지 않아도 된다 — 측정이 토큰만 본다.

### 권하는 것 (선택 — 판정에 영향 없음)

1. **infra-kaizen 넘김 이유에 Gotcha 6 을 더한다.** `.claude/skills/infra-kaizen/SKILL.md:24`(Gotcha 6 형제 대조 표)가 infra-audit · infra-reviewer 에 「미검증 3항」 이 함께 있는지 보라고 적는데, 이 Phase 뒤 두 파일은 네 칸을 쓴다. 다음 사이클이 이 표로 대조하면 이름이 맞지 않는다.
   ER-03 줄의 `` `.claude/skills/infra-kaizen/SKILL.md` (다음 사이클 — Gotcha 8 복제 조항과 정본 판 차이) `` 괄호 끝에 ` · Gotcha 6 형제 대조 표의 「미검증 3항」 을 네 칸으로` 를 더한다.
   필수 수정과 같은 줄이라 한 번에 고치면 봉인 값 계산도 한 번이다. 두 수정을 함께 넣은 사본(`p8r2/contract.fix2.md`)에서도 조건 수 `28` · 커버리지 검출기 출력이 그대로다.
2. **계약 `:542-543` 이 가리키는 출력 파일을 채운다.** 「봉인 뒤 조건 한 글자 변경」 과 「ER-03 의 새 대조 둘」 의 출력이 그 줄이 든 `p8x/var-run.txt` · `p8x/controls-out.txt` · `p8x/del-list.txt.out` 어디에도 없다.
   내가 다시 돈 값(위 3 · 4)은 표와 같아 판정은 안 바뀌지만, 출력을 파일로 남기거나(예: `p8x/tamper-run.txt` · `p8x/er03-probe.txt`) 문장을 「스크립트로 쟀다」 로 좁히면 QA 가 따라가기 쉽다.

VERDICT: CHANGES
