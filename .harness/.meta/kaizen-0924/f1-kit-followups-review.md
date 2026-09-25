# 카이젠 2026-09-24 Final — `kaizen-0924-f1-kit-followups` 계약 초안 검토

- 검토 대상: `.harness/sprint-contract-kaizen-0924-f1-kit-followups.md` (봉인 전 초안, 1084 줄 · 조건 30 줄 · 기능 조건 20, 검토 시점 sha256 앞 16 자 `28c7f30213f2f118`)
- 개정 파일: 아직 없다 (봉인 전이라 정상)
- 검토자: REVIEW(독립 검토 역할) 에이전트 (사용자 승인 대신 — 공통 러닝북 「계약 규칙」 의 두 기록 시각 · Final 러닝북 「Codex 독립 검토 지적」). 쓴 파일은 이 검토 결과 하나다.
  다시 돌린 측정과 예행 저장소는 전부 스크래치 `scratchpad/f1kit-rv/` 안에서 돌렸다. 작업 폴더 `HEAD` `5b4fd72` · 원래 레포 `HEAD` `9cd924b` 는 검토 전후 그대로다
- 읽은 입력: Final 러닝북 전문 · 공통 러닝북(계약 규칙 · git 규칙 · 말투 · 검증 절) · `final-todo.md` · `xdiag-all.md` P5 ~ P17 전문 · Codex `r2-kits-a.md` 8 건 · `r3-kits-b.md` 6 건 ·
  Phase 5 ~ 17 notes 의 「Final」 넘김 줄 · 계약 초안 전문 · 짝 계약 `kaizen-0924-f1-harness-followups` 의 범위 선언 · AR-05 · ER-08
- 검토일: 2026-09-25

## 결론

**고칠 것 여덟이 있어 CHANGES 다.** 초안은 입력 항목을 80 줄 표로 다뤘고, 조건마다 기대 출력과 시작 커밋 판 값이 붙어 있어 FAIL(탈락) 상태를 한 문장으로 쓸 수 있다.
다시 돌린 값은 초안의 봉인 전 실측 표와 전부 같았다. 고칠 것은 네 갈래다.

1. **러닝북 「봉인 전에 막는 측정 구멍」 이 셋 남았다** — 예행 저장소에 나쁜 커밋을 하나씩 넣어 재현했다. 초안 측정은 셋 다 기대값 그대로 통과한다.
   서명 없는 커밋이 `planning-kit/` 을 고침(C1) · 서명 커밋이 Final 몫인 Phase 7 개정 파일을 고침(C2) · 서명 줄을 잘못 적은 커밋이 `docs/index.html` 을 고침(C3)
2. **정확한 수가 FIX(REJECT 뒤 고치는 역할)와 부딪힌다** — `one_kit=13` · `added=172` · `new_urls=6` · `Total: 115` 는 FIX 커밋 하나로 깨진다(C4)
3. **구현 방향이 새 결함을 만든다** — api-ui 여는 방법을 두 명령으로 나누면, 명령마다 새 셸이 뜨는 도구에서 `$D` 가 비어 `.api/credentials.local.json` 이 200 으로 열린다(C5)
4. **넘김이 빠졌다** — 다시 만들 페이지 둘(C6) · 다음 사이클 메모 둘 · Codex r2-7 을 「확인 불가」 로 둔 사유가 틀림(C7) · SK-06 (c) 경우 이름(C8)

여덟 가지 모두 고칠 문구를 아래에 적었다. 새 측정 줄은 이 검토에서 예행 판 · 시작 커밋 판 · 나쁜 예에 먼저 돌려 값을 적었다.

## 직접 다시 돌린 것

초안의 세 측정 블록을 여는 줄(`#!/usr/bin/env bash`)부터 닫는 펜스까지 떼어 `f1kit-rv/K/` 에 두었다 — 초안 도우미 폴더 `kaizen/f1kit/k/` 와 세 파일 모두 글자 그대로 같다.
`mock.py` sha256 앞 16 자 `c79e4b53b088bc35` 도 초안과 같다. 예행 저장소는 `kaizen/f1kit/rhv` 를 복제해 `rehearse.sh`(변형 넷을 더한 사본 `rehearse-rv.sh`)로 다시 만들었다.

| 무엇 | 결과 | 초안 값과 |
| --- | --- | --- |
| 시작 커밋 판(`END_OVERRIDE=5b4fd72`, 실제 작업 폴더) — SK-01 · SK-06 · SK-09 · SK-12 · AR-02 | SK-01 `0 0 0 0` … `backend=13/17 infra=13/15 rust=8/9 planning=1/2` · `UP` 네 줄 · `files=132 files_up=4` / SK-06 `schema_missing=2 design_missing=2` · `1 0` · `10 경우 중 불일치 0` · `2 0 1 0 0 0` / SK-09 `cells=3 dead=1 e_block=1 e_cell=0` / SK-12 `1 0 1 0 1 0` · `r1_lines=8 PASS PASS PASS violation=0` / AR-02 `1 1 1 0 1 0` | 같다 |
| 예행 판(변형 `base`) — SK-02 ~ SK-08 · SK-10 ~ SK-12 · NA · ER-01 · ER-02 · AR-02 · AR-03 · RE-02 · AP-01 · AP-03 · AP-04 | 열아홉 조건 값이 봉인 전 실측 표 왼쪽 칸과 글자까지 같다 (SK-07 일곱 줄 · SK-08 다섯 줄 · SK-10 `busy addr_in_use=1` 포함) | 같다 |
| 예행 판 AR-01 · ER-03 | `0` · `0 41` · `mixed=0 one_kit=13` · `0` · `SEAL_OK` · `scope_same=1 harness_line=1` / ER-03 일곱 줄 · `not_other=0` | 같다 |
| 새 나쁜 예 `unsigned-planningkit` (서명 없는 커밋이 `planning-kit/README.md` 를 고침) | AR-01 여섯 줄 · ER-03 일곱 줄이 `base` 와 똑같다 | 구멍 — C1 |
| 새 나쁜 예 `harness-other` (서명 커밋이 `.harness/sprint-amendments-kaizen-0924-p07-backend-kit.md` 를 고침) | AR-01 · ER-03 이 `base` 와 똑같다 | 구멍 — C2 |
| 새 나쁜 예 `typo-shared` (서명 줄을 `Kaizen-Phase: kaizen-0924-f1-kit-followup` 로 잘못 적은 커밋이 `docs/index.html` 을 고침) | ER-03 `not_other=0` | 구멍 — C3 |
| 고친 측정(`f1kit-rv/K2/`) — `base` · `unsigned-kit` · `unsigned-planningkit` · `harness-other` · `typo-shared` · `cross-phase` | AR-01 첫째 `0` · `1` · `1` · `0` · — · — / 둘째 `0 41` · `0 41` · `0 41` · `1 41` · — · — / ER-03 `not_other` `0` · — · — · — · `1` · `1` | 새로 잼 |
| `scripts/detect-docs-drift.py --since 5b4fd72` (예행 판) | 기존 페이지 가운데 `docs/bambu-kit/bambu-print-profile.html` 이 나온다 — ER-03 (c) 일곱에 없다 | C6 |
| api-ui 서버 명령을 `$D` 없이 (`env -u D`) 돌림 — 스크래치 폴더에 `.api/credentials.local.json` 을 두고 | 시작 커밋 판 한 줄 명령 `served=0` · 예행 판 둘째 명령 `served=200` · 고친 명령(C5) `served=0 guard_msg=1` | C5 |
| 고친 명령으로 초안 `api_serve` 그대로 | `run rc=0 blocked=0 http=200 \| busy addr_in_use=1 blocker_alive=1` | C5 를 넣어도 SK-10 기존 값 그대로 |
| 이 세션의 Bash 도구에서 `python3 -m http.server <빈 포트> … &` | 도구 호출이 바로 돌아오고, 다음 호출에서 그 서버가 200 으로 답했다 | 뒤에서 띄우는 방향 자체는 맞다 |
| `~/.pub-cache/hosted/pub.dev/build_runner-2.13.1/CHANGELOG.md` | `:142` `## 2.7.0` 아래 `:149` 「Remove interactive prompts for whether to delete files.」 · `:150` 「Ignore `-d` flag: always delete files as if `-d` was passed.」 | C7 |

## 고칠 것

### C1 — AR-01 첫째가 이 계약이 안 고치는 킷 자리를 보지 않는다 (러닝북 측정 구멍 첫 줄)

AR-01 첫째는 `GPATH` 열셋 묶음의 경로만 넘긴다. 그런데 `planning` 묶음은 `docs/planning/` 뿐이라 `planning-kit/` 이 빠지고, `docs/design/` · `docs/flutter/` · `docs/react/` · `docs/tone/` · `docs/howto/` 같은 킷 원본 문서 폴더도 빠진다.
교차 진단 P7 · P11 · P12 · P14 가 네 번 적은 「서명 없는 커밋이 다른 킷 폴더를 건드리면 못 잡는다」 와 같은 구멍이다. `unsigned-planningkit` 에서 AR-01 · ER-03 이 기대값 그대로 나왔다(DG-06 은 돌려 보지 않았다 — 한 킷만 건드린 커밋은 scope-isolation 이 섞임으로 보지 않는다).
이 경로들은 동시에 도는 harness 쪽 계약의 범위(`harness/` · `scripts/` · `.claude/skills/` · `ci.yml`)가 아니라 넓혀도 남의 정상 커밋이 걸리지 않는다.

- **m.sh `AR-01)` 갈래 둘째 · 셋째 줄**
  `for g in "${KITG[@]}"; do for p in ${GPATH[$g]}; do gp+=("$p"); done; done` 와 `echo "$(unsigned_on "$B" "$END" "$SIG" "${gp[@]}" | grep -c .)"` 를 아래 두 줄로 바꾼다 (`local` 의 `gp=()` 는 지운다)

  ```bash
      # 킷 묶음 열셋 경로만 넘기면 planning-kit/ · docs/design/ 처럼 이 계약이 안 고치는 킷 자리를 서명 없이 건드려도 0 이다
      echo "$(unsigned_on "$B" "$END" "$SIG" ':(glob)*-kit/**' flutter-toolkit ':(glob)docs/**' ':(exclude,glob)docs/**/*.html' ':(exclude)docs/kaizen' | grep -c .)"
  ```

- **AR-01 조건 본문 첫째** — 「시작 커밋부터 `$END` 사이에 킷 묶음 열셋의 경로를 건드린 커밋 가운데 서명 줄이 없는 커밋 수 0」 →
  「시작 커밋부터 `$END` 사이에 킷 폴더 전부(`*-kit/` · `flutter-toolkit/`, `harness/` 제외)와 `docs/` 원본(HTML · `docs/kaizen/` 제외)을 건드린 커밋 가운데 이 계약 서명 줄이 없는 커밋 수 0 — 이 자리는 동시에 도는 harness 쪽 계약의 범위가 아니다」
- **AR-01 양성 대조에 더한다** — 「`unsigned-planningkit`(서명 없는 커밋이 `planning-kit/README.md` 를 고침) → 첫째 `1`」. 예행 변형 표에도 같은 줄
- 검토 실측: 고친 줄로 `base` `0` · `unsigned-kit` `1` · `unsigned-planningkit` `1`

### C2 — `.harness/` 는 `verify_seal` 로 잴 수 없다 (교차 진단 P6 · P8 구멍 되풀이)

`## 범위 경계` 는 「`.harness/` 쪽은 이 계약 · 개정 파일 · QA 피드백 · notes · review 를 쓴다 — … AR-01 넷째 값 `verify_seal` 로 잰다」 고 적었다. 그러나 `verify_seal` 은 계약 조건 줄의 봉인만 보고,
AR-01 둘째는 `.harness/` 를 통째로 뺀다. 교차 진단 P8 이 같은 문장에 「이 함수로는 그걸 잴 수 없습니다」 라고 적은 것과 같은 모양이다.
이번에는 위험이 구체적이다 — Final 러닝북이 Phase 7 · 8 · 9 · 11 개정 파일에 「교차 진단 뒤 Final 에서 고침」 줄을 붙이는 일을 `kaizen-0924-final` 몫으로 정했는데,
이 계약 notes 가 바로 그 줄을 준비하므로 BUILD(봉인 · 구현 역할)가 개정 파일까지 고치기 쉽다. `harness-other` 에서 AR-01 · ER-03 이 모두 통과했다.

허용 목록을 **이 계약 서명 커밋에만** 거는 것이라 contract-schema §`.harness/` 범위 조건이 막으려던 경우(앞 스프린트 status 전환이 구간에 들어와 걸림)는 생기지 않는다.
짝 계약 AR-05 (a) 가 `MYHARNESS` 다섯으로 같은 방식을 쓴다.

- **m.sh `AR-01)` 갈래의 둘째 값 줄**
  `echo "$(grep -v '^\.harness/' "$T/mine.txt" | grep -cvxF -f <(printf '%s\n' "${FILES[@]}")) $(grep -cxF -f <(printf '%s\n' "${FILES[@]}") "$T/mine.txt")"` 를 아래로 바꾼다

  ```bash
      # .harness/ 는 이 계약 이름이 든 파일만 허용한다 — verify_seal 은 조건 줄만 봐서 다른 Phase 개정 파일 · project.yaml 을 고쳐도 0 이다
      echo "$(grep -vxF -f <(printf '%s\n' "${FILES[@]}") "$T/mine.txt" | grep -cvE '^\.harness/(sprint-(contract|amendments|feedback)-kaizen-0924-f1-kit-followups|\.meta/kaizen-0924/f1-kit-followups-[a-z0-9-]+)\.md$') $(grep -cxF -f <(printf '%s\n' "${FILES[@]}") "$T/mine.txt")"
  ```

- **AR-01 조건 본문 둘째** — 「서명 커밋이 건드린 경로 가운데 `.harness/` 밖이면서 `FILES` 마흔하나 밖인 경로 수 0」 →
  「서명 커밋이 건드린 경로 가운데 `FILES` 마흔하나 밖이면서 이 계약 `.harness/` 허용 갈래(계약 · 개정 · QA 피드백 · `.harness/.meta/kaizen-0924/f1-kit-followups-*.md`) 밖인 경로 수 0」.
  양성 대조에 「`harness-other`(서명 커밋이 `.harness/sprint-amendments-kaizen-0924-p07-backend-kit.md` 를 고침 — Final 몫) → 둘째 `1 41`」
- **`## 범위 경계` 셋째 줄** — 「슬러그를 나열하지 않고 AR-01 넷째 값 `verify_seal` 로 잰다」 →
  「AR-01 둘째 값이 이 계약 이름이 든 허용 갈래로 잰다(다른 계약 슬러그는 나열하지 않는다). 허용 목록은 이 계약 서명 커밋에만 걸어서, 앞 스프린트의 status 전환이 구간에 들어와도 걸리지 않는다.
  넷째 값 `verify_seal` 은 봉인이 깨졌는지만 잰다. Phase 7 · 8 · 9 · 11 개정 파일의 「교차 진단 뒤 Final 에서 고침」 줄은 `kaizen-0924-final` 이 붙인다 — 이 계약은 notes 에 sha 만 적는다」
- 검토 실측: 고친 줄로 `base` `0 41` · `harness-other` `1 41`

### C3 — ER-03 (e) 가 서명 줄을 잘못 적은 이 계약 커밋을 「다른 Phase」 로 뺀다

`not_other` 는 `Kaizen-Phase:` 로 시작하는 줄이 있고 이 계약 서명과 글자가 다르면 건너뛴다. 그래서 서명을 한 글자 틀린 이 계약 커밋이 공유 파일을 고쳐도 0 이다(`typo-shared` → `not_other=0`).
이 구간(`5b4fd72..$END`)에 함께 커밋하는 계약은 `kaizen-0924-f1-harness-followups` 하나다(Final 러닝북 — `kaizen-0924-final` 은 두 계약이 끝난 뒤 시작한다). 짝 계약 AR-05 (c) 도 알려진 서명을 글자 그대로 대조한다.

- **common.sh `not_other()`** — 머리 주석을 「`# not_other <base> <상한> <서명> <경로…> — 경로를 건드린 구간 안 커밋 가운데 harness 쪽 계약 서명 줄이 글자 그대로 있는 커밋을 뺀 나머지 (0 줄이어야 한다)`」 로,
  몸통의 `if printf '%s\n' "$_m" | grep -qE '^Kaizen-Phase: ' && ! printf '%s\n' "$_m" | grep -qxF "$_s"; then continue; fi` 를 아래 두 줄로 바꾼다

  ```bash
      # 서명 모양만 보고 빼면 이 계약 서명을 잘못 적은 커밋도 「다른 Phase」 로 빠진다 — 이 구간에 함께 커밋하는 계약은 하나다
      printf '%s\n' "$_m" | grep -qxF 'Kaizen-Phase: kaizen-0924-f1-harness-followups' && continue
  ```

- **ER-03 조건 본문 (e)** — 「…를 건드린 커밋 가운데 다른 Phase · 계약 서명이 없는 커밋이 0 개다」 →
  「…를 건드린 커밋 가운데 `Kaizen-Phase: kaizen-0924-f1-harness-followups` 줄이 글자 그대로 있는 커밋을 뺀 수가 0 이다 — 서명을 잘못 적은 이 계약 커밋도 센다」.
  양성 대조에 「`typo-shared`(서명 줄을 `…f1-kit-followup` 으로 잘못 적은 커밋이 `docs/index.html` 을 고침) → 마지막 값 `1`」
- 검토 실측: 고친 함수로 `base` `0` · `typo-shared` `1` · `cross-phase` `1`

### C4 — 정확한 수가 FIX 커밋 하나로 깨진다 (조건과 절차가 부딪힘)

러닝북의 FIX 는 「QA REJECT(반려) 이유만 고치고 다시 커밋」 한다. 킷 파일 결함으로 REJECT 되면 FIX 는 킷 커밋을 하나 더 한다. 그러면 올바르게 고쳐도 아래 값이 깨져 개정 파일이 강제된다.
네 값 모두 조건의 뜻(한 커밋에 킷 하나 · 번역투 0 · 근거 밖 URL 0 · 시험 실패 0)과 상관없는 수다.

- **AR-01 셋째** — 기대값 `mixed=0 one_kit=13` → `mixed=0 one_kit=<13 이상>`. 본문 「킷 묶음 하나만 건드린 커밋 13」 → 「킷 묶음 하나만 건드린 커밋 13 이상(묶음마다 커밋이 있는지는 ER-03 (b) 가 잰다)」
- **ER-02** — 기대값 `added=172 k02=0 names=0 tax_old=0` → `added=<1 이상> k02=0 names=0 tax_old=0` (예행 판 172)
- **ER-01** — 첫 줄 기대값 `new_urls=6 not_in_evidence=0` → `new_urls=<1 이상> not_in_evidence=0` (예행 판 6). 본문의 「예행 판 6 개」 는 기록으로 둔다
- **DG-05 셋째** — 기대값 `evals_rc=0 Total: 115 passed, 0 failed` → `evals_rc=0 Total: <N> passed, 0 failed` (예행 판 115). 조건 본문 (c) 「`0 failed`」 와 맞춘다

### C5 — SK-10 (a) 고친 여는 방법이 `.api/` 를 통째로 띄울 수 있다

예행 판은 명령을 둘로 나눴다 — `D=$(mktemp -d) && cp .api/ui.html "$D/"` 와 `python3 -m http.server 8765 --bind 127.0.0.1 --directory "$D" &`.
이 세션의 Bash 도구 설명은 「셸 상태는 호출 사이에 이어지지 않는다」 이다. 두 명령을 따로 부르면 둘째에서 `$D` 가 비고, `--directory ""` 는 지금 폴더를 띄운다.
스크래치 폴더에 `.api/credentials.local.json` 을 두고 둘째 명령만 `env -u D` 로 돌리자 그 파일이 200 으로 열렸다. 같은 문단이 「`.api/` 를 통째로 띄우지 마라 — `credentials.local.json`(아이디 · 비밀번호) … 가 HTTP 로 열리고」 라고 막은 바로 그 상태다.
시작 커밋 판의 한 줄 명령은 `&&` 로 이어져 있어 이 일이 없었다(`served=0`) — 이번 고침이 새로 만드는 결함이다. `api_serve` 는 두 줄을 한 스크립트에서 돌려 이 경우를 보지 못한다.

- **api-ui `1. **여는 방법**` 줄 (예행 판 `mock.py` api 갈래)** — 서버 명령을
  `` `python3 -m http.server 8765 --bind 127.0.0.1 --directory "${D:?폴더 변수가 비었다 — 두 명령을 한 셸에서 잇는다}" &` `` 로 바꾸고,
  그 뒤에 「두 명령은 한 번의 셸 호출에서 잇는다 — 명령마다 새 셸이 뜨는 도구에서는 `$D` 가 비어 지금 폴더(`.api/` 포함)를 띄운다.」 한 문장을 둔다
- **SK-10 조건 본문 (a)** — 서버 명령 토큰을 위 글자로 바꾸고 끝에 더한다: 「Given 스크래치 폴더에 `.api/credentials.local.json` 을 둔 채 폴더 변수 없이(`env -u D`) 서버 명령만 돌리면, Then 그 파일이 열리지 않고(`served=0`) 비었다는 알림이 1 줄이다」.
  양성 대조에 「예행 판 초안 명령(`--directory "$D" &`) → `unset_d served=200 guard_msg=0`」
- **m.sh `SK-10)` 갈래** — 첫 `echo` 의 둘째 `grep -cF` 토큰을 새 서버 명령 글자로 바꾸고, `api_serve "$c1" "$c2"` 다음 줄에 `api_unset "$c2"` 를 넣는다. 도우미는 `api_serve` 뒤에 둔다

  ```bash
  # api_unset <서버 명령> — 폴더 변수가 빈 채(명령마다 새 셸이 뜨는 도구) 서버 명령만 돌려, 지금 폴더의 .api/ 가 열리는지 잰다
  api_unset() { local d=$T/apiun p code
    rm -rf "$d"; mkdir -p "$d/.api"; printf 'secret\n' > "$d/.api/credentials.local.json"; printf '<title>t</title>\n' > "$d/.api/ui.html"
    p=$(python3 -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1",0)); print(s.getsockname()[1]); s.close()')
    { (cd "$d" && exec perl -e 'alarm 4; exec @ARGV' env -u D bash -c "${1//8765/$p}" > "$d/out.txt" 2>&1); } 2>/dev/null
    code=$(python3 - "$p" <<'PY'
  import sys, time, urllib.request
  p = sys.argv[1]; code = 0
  for _ in range(15):
      try:
          code = urllib.request.urlopen("http://127.0.0.1:%s/.api/credentials.local.json" % p, timeout=1).status; break
      except Exception:
          time.sleep(0.1)
  print(code)
  PY
  )
    pkill -f "http.server $p" 2>/dev/null
    echo "unset_d served=$code guard_msg=$(grep -c 'D:' "$d/out.txt")"; }
  ```

- **SK-10 측정 기대값** — 네 줄 → 다섯 줄: `1 1 0 1` · `run rc=0 blocked=0 http=200 | busy addr_in_use=<1 이상> blocker_alive=1` · `unset_d served=0 guard_msg=1` · `1 1 1 1 1` · `1 1`.
  시작 커밋 판 셋째 줄 `unset_d served=0 guard_msg=0`
- 검토 실측: 새 명령으로 `unset_d served=0 guard_msg=1`, 같은 명령으로 초안 `api_serve` 는 `run rc=0 blocked=0 http=200 | busy addr_in_use=1 blocker_alive=1` 그대로

### C6 — ER-03 (c) 다시 만들 페이지에 둘이 빠졌다

- `docs/bambu-kit/bambu-print-profile.html` — `scripts/detect-docs-drift.py` 의 `SOURCE_OVERRIDES` 가 `bambu-kit/skills/bambu-print-profile/SKILL.md` 를 이 페이지로 잇고, 예행 판에 돌리면 목록에 나온다. 페이지 안에 `SKILL_DIR` 도 있다 — SK-07 이 고치는 블록의 사본이다
- `docs/reflect-kit/schema.html` — `reflect-kit/docs/SCHEMA.md` 로 가는 출처 줄(`:179`)이 있고, `skip:cli-missing` 등 사유 태그 목록을 싣는다. `:197` 은 이 페이지를 두 원본(`DESIGN.md` · `SCHEMA.md`)과 함께 고치라고 적었다. SK-06 (a) 가 그 목록에 두 태그를 더한다

고칠 곳:

- `## 범위 경계` notes 설명 (c) 「다시 만들 문서 사이트 페이지 일곱(…)」 → 「아홉(… · `bambu-print-profile.html` · `schema.html`)」. 초안 첫머리 GAP 표 「소비면 존재」 칸의 페이지 목록에도 둘을 더한다
- m.sh `ER-03)` 갈래 `for pg in …` 목록에 `bambu-print-profile.html schema.html` 을 더하고 `/7` → `/9`
- ER-03 본문 (c) 「다시 만들 페이지 일곱(`api-design.html` · `visual-change-protocol.html` 포함)」 → 「아홉(`api-design.html` · `visual-change-protocol.html` · `bambu-print-profile.html` · `schema.html` 포함)」, 기대값 `release_kits=12/12 pages=9/9`

### C7 — 다음 사이클 메모 셋 · 입력 항목 표 73 행 사유

- **입력 항목 표 24 행(XD P8 결함 3 · `docs/infra` 판정 세 줄)과 31 행(XD P10 · `harness-project.yaml.template`)** 은 「고치지 않음」 인데 어느 Phase notes 의 다음 사이클 메모에도 없다
  (`phase10-notes.md` 에 `harness-project.yaml.template` 0 줄, `phase8-notes.md` 의 `cicd.md` 는 바꾼 파일 목록 `:33` 뿐). ER-03 (d) 토큰 열도 두 줄을 재지 않는다 — Final 러닝북 「조용히 빠뜨리지 마라」.
  ER-03 (d) 토큰에 `harness-project.yaml.template` · `docs/infra/platform/cicd.md` 를 더한다
- **입력 항목 표 73 행(Codex r2-7)** — 「확인 불가 … 2.7.0 부터 삭제가 기본이라는 주장은 근거 파일에 없는 바깥 문서다」 는 틀리다. 설치된 판 파일로 실측된다.
  73 행 처리 칸을 아래로 바꾼다:
  「고치지 않음 — 심각도 낮음. 2.7.0 동작은 설치된 `~/.pub-cache/hosted/pub.dev/build_runner-2.13.1/CHANGELOG.md` `:149` · `:150`(2.7.0 항목 「Ignore `-d` flag: always delete files as if `-d` was passed.」)으로 확인된다.
  킷 문장(2.16 에서 제거된 호환 옵션 목록으로 옮겨짐, `phase5.md:41`)과 어긋나지 않고, 명령의 플래그는 효과 없는 인자다. 명령에서 뺄지는 Phase 5 notes `:79` 가 다음 사이클로 보냈다 —
  그 notes 가 막힌 이유로 든 「경고인지 오류인지」 가운데 2.7.0 ~ 2.13.1 은 이 파일이 답한다(무시한다). 2.16 쪽은 설치본이 없어 모른다」.
  ER-03 (d) 토큰에 `build_runner-2.13.1` 을 더한다
- **ER-03 (d) 기대값** — 토큰 열여섯 → 열일곱: `claude -p` … `misplaced` · `harness-project.yaml.template` · `docs/infra/platform/cicd.md` · `build_runner-2.13.1`, 여섯째 줄 기대값은 `1` 열일곱.
  `## 범위 경계` notes 설명의 토큰 열과 m.sh `ER-03)` 갈래 `toks` 인자에도 같은 셋을 더한다

### C8 — SK-06 (c) 가 재는 경우 이름을 조건에 적는다

m.sh 는 `grep -c '^불일치 도중 멈춤'` 으로 그 경우를 찾는데, 조건 본문에는 경우 이름이 없다. `mock.py` 를 편집 명세로 쓰면 맞지만 조건만 읽으면 BUILD 가 다른 이름을 붙여도 알 수 없다.

- SK-06 본문 (c) 「열한째 경우는 기록 하나(`D2`) 뒤에 …」 → 「열한째 경우(`check` 이름 「도중 멈춤 — 마지막 기록 뒤 실패」)는 기록 하나(`D2`) 뒤에 …」,
  「그 불일치가 그 경우다」 → 「그 불일치가 그 경우다(`불일치 도중 멈춤` 으로 시작하는 줄 1)」

## 괜찮다고 본 것

- **FAIL 상태를 한 문장으로** — 조건 서른 줄 모두 `m <ID>` 기대 출력이 정해져 있고 시작 커밋 판 값이 옆에 있다. 해당 없음 넷(SC-00 · RE-01 · DG-01 · DG-03)도 `m NA` 값으로 잰다
- **측정이 뜻을 잰다** — 코드 줄을 도는 측정(SK-03 (d) · SK-05 넷째 · SK-06 (c) · SK-07 · SK-08 (d) · SK-11 · SK-12 (b))은 시작 커밋 판에서 결함이 드러나고 예행 판에서 사라진다. 문장 토큰은 `del.sh` 로 41 개 모두 값이 바뀐다고 적었고, 방식을 읽어 확인했다
- **러닝북 구멍 목록** — 상한은 `END_UNRESOLVED` 로 멈춘다 · 도우미는 `type m` 과 `m` 안의 `type` 으로 확인한다 · 연구 기록과 서른여섯 마크다운은 파일마다 규칙별로 비교한다 · validate-plugin 은 종료 코드로 잰다 ·
  옛 값은 `check-stale-values.py` 대신 마흔한 파일에 직접 센다 · `bash -c` 로 감싸고 zsh 를 막는다 · 종료 코드에 `| tail` 이 없다. 남은 구멍은 C1 ~ C3 셋이다
- **Codex 지적 처리** — r2-3 · r2-4 는 기준 원본이 여섯 항목(`qa-evaluation-guide.md:1236` · `:1250` · `:1267` · `:1274` · `:1280` · `:1285`, 「3.」 이 둘)임을 직접 확인했다.
  두 reviewer 파일은 이번 사이클에 바뀌었지만(`83cfb4f..5b4fd72` 에 3 · 6 줄), 옮기면 REJECT 문턱이 함께 바뀌는 별도 관심사라 다음 사이클로 미룬 이유가 성립한다. 짝 계약도 F1H-47 로 같은 판단을 했다.
  r3-6 은 근거 파일에 RFC(인터넷 표준 문서) 7493 본문이 없어 러닝북 규칙대로 조건으로 삼지 않은 것이 맞다
- **범위** — 마흔한 파일이 모두 Final 표의 킷 폴더 · 킷 원본 문서 폴더 안이다. `docs/onboarding-kit/examples/` 는 Phase 14 notes 가 Final 로 넘긴 자리다. 공유 파일 · 다른 계약 경로는 ER-03 (e) 가 잰다(C3 로 좁힌 뒤)
- **조건 수** — 기능 조건 20 으로 복잡 등급 상한 안이다. 이 검토의 고칠 것은 조건 줄을 더하지 않는다
- **SK-06 (c) 새 경고의 문턱** — 문턱 없이 「마지막 기록 뒤 실패」 로 가르는 판단과 그 대가(일시 실패 한 번에도 digest 의 `## 승격 후보` 절이 빈다)를 계약이 스스로 적고 다음 사이클 메모로 넘겼다. 세는 사유는 분석을 잃은 네 갈래뿐이라 짧은 대화 건너뛰기 같은 정상 사유로는 켜지지 않는다

## 조건끼리 부딪힘

- C4 넷(AR-01 셋째 · ER-02 · ER-01 · DG-05 셋째)이 FIX 절차와 부딪힌다
- C5 로 서버 명령 글자가 바뀌면 SK-10 첫 줄 토큰 · `mock.py` · `del.sh` 의 SK-10 줄이 함께 바뀌어야 한다. AR-02 (f) · RE-02 는 영향이 없다
- C6 · C7 로 ER-03 기대값 두 줄(`pages=9/9` · 토큰 열일곱)이 바뀐다. `rehearse.sh` 의 notes 모의본도 같은 페이지 · 토큰으로 맞춰 다시 잰다
- 그 밖에 서로 다른 값을 요구하는 조건 쌍은 찾지 못했다 — SK-01 (a) 와 AR-03 (a) 는 같은 여덟 소제목을 서로 다른 쪽에서 잰다. SK-08 (c) 와 RE-02 (a) 는 같은 세 행을 같은 방식으로 잰다

## BUILD 가 봉인 전에 다시 할 것

1. C1 ~ C8 을 초안 · `m.sh` · `common.sh` · `mock.py` · `rehearse.sh`(변형 `unsigned-planningkit` · `harness-other` · `typo-shared` 추가, 이 검토의 `f1kit-rv/rehearse-rv.sh` 에 세 변형이 있다)에 반영한다
2. 예행 판 · 시작 커밋 판 · 변형 전부를 다시 재서 봉인 전 실측 표와 예행 변형 표를 새 값으로 바꾼다
3. 계약 파일은 이 검토를 받은 뒤에 봉인한다

VERDICT: CHANGES

## 2 회차

- 검토 대상: 같은 계약 초안 (1118 줄 · 조건 30 줄, 검토 시점 sha256 앞 16 자 `83132998e7117f09` — 검토 시작과 끝이 같다). 개정 파일은 아직 없다 (봉인 전이라 정상)
- 검토자: REVIEW(독립 검토 역할) 에이전트. 쓴 파일은 이 절 하나다. 다시 돌린 측정 · 예행 저장소 · 시험용 서버는 전부 스크래치 `scratchpad/f1kit-rv2/` 안에서 돌렸고, 띄운 시험용 서버는 끝에 모두 내렸다(`pgrep -f http.server` 0)
- 검토 중에 짝 계약(harness 쪽)이 커밋을 이어 올려 작업 폴더 `HEAD`(가지 끝 커밋)가 `5cb9eb0` → `927434b` → `1a71606` 으로 움직였다. 시작 커밋 뒤 짝 계약 커밋 열(`5b4fd72..1a71606`)은 전부 `Kaizen-Phase: kaizen-0924-f1-harness-followups` 서명이 글자 그대로 있고 킷 폴더 · `docs/` 원본을 건드리지 않는다. 원래 레포 `HEAD` `9cd924b` 는 그대로다
- 검토일: 2026-09-25

### 결론 — 2 회차

**1 회차 고칠 것 여덟(C1 ~ C8)은 모두 반영됐다. 다만 C5 로 손본 api-ui 여는 방법에 새 결함이 하나 있어 CHANGES 다(R1).** 나머지는 문구 둘(R2)이다.

### C1 ~ C8 반영 확인

| 항목 | 반영 자리 | 다시 잰 값 |
| --- | --- | --- |
| C1 | m.sh `AR-01)` 첫째 줄이 `':(glob)*-kit/**' flutter-toolkit ':(glob)docs/**'` (HTML · `docs/kaizen` 제외) · AR-01 조건 본문 첫째 · 양성 대조 `unsigned-planningkit` | 아래 예행에서 `unsigned-planningkit` 첫째 `1` · `base` `0`. 사이클 구간(`7689fde..5b4fd72`)에 같은 경로 식을 주면 20 — 식이 실제로 커밋을 잡는다 |
| C2 | m.sh `AR-01)` 둘째 값 허용 갈래 정규식 · 조건 본문 둘째 · `## 범위 경계` 셋째 줄 | `harness-other` 둘째 `1 41` · `base` `0 41`. 설치된 평가자(0.13.0)가 쓰는 파일은 `.harness/sprint-feedback-<슬러그>.md` 라 허용 갈래 안이다 |
| C3 | common.sh `not_other()` 머리 주석과 몸통 · ER-03 (e) 본문 · 양성 대조 `typo-shared` | `typo-shared` `not_other=1`. 지금 구간의 짝 계약 커밋 여섯(공유 경로를 건드린 것)은 서명이 맞아 `not_other=0` |
| C4 | AR-01 셋째 `one_kit=<13 이상>` · ER-02 `added=<1 이상>` · ER-01 `new_urls=<1 이상>` · DG-05 셋째 `Total: <1 이상> passed, 0 failed` | 네 자리 모두 하한으로 바뀌었다 |
| C5 | mock.py api 갈래 · SK-10 (a) 본문 · m.sh `SK-10)` 첫 줄 토큰과 `api_unset` · 기대값 다섯 줄 | `unset_d served=0 guard_msg=1`. 그러나 아래 R1 |
| C6 | `## 범위 경계` (c) 아홉 · GAP 표 「소비면 존재」 칸 · m.sh `pages=…/9` · ER-03 (c) | `pages=9/9`. 두 페이지 파일이 실제로 있다 |
| C7 | 입력 항목 표 24 · 31 · 73 행 · (d) 토큰 열일곱 · m.sh `toks` | 토큰 열일곱 모두 `1` |
| C8 | SK-06 (c) 본문에 경우 이름과 `불일치 도중 멈춤` 줄 1 | `start_lib rc=1 … 불일치 1 1` |

직접 다시 돌린 것:

| 무엇 | 결과 |
| --- | --- |
| 측정 블록 셋을 계약에서 떼어 초안 도우미 폴더 `kaizen/f1kit/k/` 와 비교 | `common.sh` · `m.sh` · `sweep.sh` 모두 글자 그대로 같다. `mock.py` sha256 앞 16 자 `b2ed8130c26a6f02` 도 초안과 같다 (1 회차 판 `mock-v2.py` 와의 차이는 C5 두 줄뿐) |
| sprint-contract Step 6.2 · 6.5 검사(`kaizen/f1kit/gate65.sh`)를 지금 계약에 다시 | `OK conditions=30` · 검출기 `unresolved=0` · `OK 미실측 0 건` · 봉인 필드 0 줄 |
| **예행을 지금 가지 끝 위에 다시 쌓음** — 작업 폴더를 스크래치로 복제하고 `rehearse.sh` 의 시작 커밋만 `927434b`(짝 계약의 구현 · 새 검증 스크립트가 든 판)로 바꿔 봉인 · 킷 열셋 커밋 · `end_sha` · notes · `end_sha` 를 올림 | 스물일곱 측정(`SK-01` ~ `SK-12` · `NA` · `ER-01` ~ `ER-03` · `AR-01` ~ `AR-03` · `AP-01` · `AP-03` · `AP-04` · `RE-02` · `DG-02` · `DG-04` · `DG-05` · `DG-06`)이 봉인 전 실측 표 왼쪽 칸과 글자까지 같다 (`f1kit-rv2/out-rr-head.txt`). 짝 계약이 바꾼 `validate-plugin.py`(실패한 V 줄에 판정 글자) · `validate-post-kaizen.py` 로 돌려도 `kits=13 kitfail=0 bad_v=0` · `scope-isolation: PASS` 다 |
| 같은 예행에서 변형 넷 | `unsigned-kit` · `unsigned-planningkit` 첫째 `1` · `harness-other` 둘째 `1 41` · `typo-shared` `not_other=1`, 나머지 값은 `base` 와 같다 — 계약의 변형 표와 같다 |

### 고칠 것 — 2 회차

#### R1 — api-ui 를 뒤에서 띄우면 포트 충돌 알림이 도구 출력에 안 보이고, 남은 서버가 옛 뷰어를 대신 보여 준다 (C5 로 손본 자리의 새 결함)

예행 판 문장은 「8765 를 이미 다른 서버가 쓰고 있으면 파이썬이 `Address already in use` 를 내고 바로 끝난다 — 그 서버는 끄지 말고 빈 포트로 바꿔 띄우고」 · 「확인이 끝나면 띄운 서버를 내리고(같은 셸이면 `kill $!`) 그 폴더를 지운다」 이다.
그런데 서버를 `&` 로 뒤에서 띄우면 그 오류는 셸이 돌아간 뒤에 찍혀 도구 출력에 실리지 않는다. 이 세션의 Bash 도구(zsh 5.9)에서 직접 재현했다.

1. 빈 포트에 옛 뷰어 역할 서버를 띄운다(`ui.html` 내용 `OLD-VIEWER`)
2. 다른 폴더에서 예행 판 두 명령(`D=$(mktemp -d) && cp .api/ui.html "$D/"` 줄 뒤에 `python3 -m http.server <그 포트> … --directory "${D:?…}" &`)을 한 번의 도구 호출로 돌린다 → 도구 출력 `(Bash completed with no output)`
3. 다음 호출에서 `http://127.0.0.1:<그 포트>/ui.html` → `OLD-VIEWER`. 새로 띄운 서버는 없다(그 포트의 서버 1 개)

옛 서버가 남는 까닭도 같은 문장 안에 있다. 브라우저 확인은 다른 도구 호출이라 정리는 늘 다른 셸에서 하게 되는데, 새 셸에서 `$!` 는 bash 에서 빈 값, zsh 에서 `0` 이다(`zsh -c 'echo "[$!]"'` → `[0]`). 그래서 `kill $!` 은 서버를 못 내리고 zsh 에서는 `kill 0`(자기 프로세스 묶음 전체에 신호)이 된다.
그러면 다음 api-ui 실행이 8765 에서 조용히 실패하고, 여는 주소에서 앞 실행의 뷰어를 재서 「콘솔 오류 0 · 항목 수 같음」 을 보고한다 — 이 스킬 확인 절차 셋이 옛 파일을 재는 셈이다.
시작 커밋 판은 앞에서 띄워 셸이 묶이는 결함이 있었지만 이 결함은 없었다 — 포트가 차 있으면 오류가 셸이 돌아오기 전에 찍혔다.

SK-10 측정도 이 차이를 못 본다. `api_serve` 의 `busy addr_in_use=1` 은 셸이 끝나고 1 초 기다린 뒤 파일에 쌓인 뒤늦은 출력을 센다. 셸이 끝난 바로 그때의 출력을 떠서 다시 쟀다(`f1kit-rv2/api_serve2.sh`).

| 판 | 셸이 끝난 때 출력 | 찍힌 번호로 내린 뒤 남은 서버 |
| --- | --- | --- |
| 시작 커밋 판 한 줄 명령(앞에서 띄움) | `run rc=142` · 충돌 때 `Address already in use` 2 줄 (셸이 돌아오기 전에 보인다) | 번호가 없어 1 |
| 예행 판(C5 반영) | 판정 줄 0 · 충돌 때 `Address already in use` 0 줄 | 번호가 없어 1 |
| 아래 고친 명령 | 띄움 `SERVING pid=… dir=…` 1 줄 · 충돌 때 `NOT_SERVING` 1 줄 | 0 |

고친 명령은 이 세션 도구에서도 확인했다 — 포트가 차 있으면 한 호출 안에 파이썬 오류와 `NOT_SERVING …` 줄이 보이고, 비어 있으면 `SERVING pid=<번호> dir=<폴더>` 가 찍힌다. 다음 호출에서 찍힌 번호로 `kill` · `rm -rf` 해 서버 0 개가 됐다. 폴더 변수 없이 돌린 경우도 `unset_d served=0 guard_msg=1` 그대로다.

고칠 곳:

- **api-ui `1. **여는 방법**` 줄 (mock.py api 갈래)**
  - 서버 명령 코드 조각을
    `` `python3 -m http.server 8765 --bind 127.0.0.1 --directory "${D:?폴더 변수가 비었다 — 두 명령을 한 셸에서 잇는다}" & sleep 1; kill -0 $! 2>/dev/null && echo "SERVING pid=$! dir=$D" || echo "NOT_SERVING 8765"` `` 로
  - 「8765 를 이미 다른 서버가 쓰고 있으면 파이썬이 `Address already in use` 를 내고 바로 끝난다 — 그 서버는 끄지 말고 빈 포트로 바꿔 띄우고 여는 주소의 포트도 같이 바꾼다.」 →
    「뒤에서 띄운 파이썬의 `Address already in use` 는 도구 출력에 안 실릴 수 있어 같은 호출 끝의 판정 줄로 가른다. `NOT_SERVING` 이면 8765 를 다른 서버(앞 실행이 남긴 서버일 수 있다)가 쥐고 있으니 그 주소를 열지 않는다 — 그 서버는 끄지 말고 빈 포트로 바꿔 다시 띄우고 여는 주소의 포트도 같이 바꾼다.」
  - 「확인이 끝나면 띄운 서버를 내리고(같은 셸이면 `kill $!`) 그 폴더를 지운다.」 →
    「확인이 끝나면 `SERVING` 줄에 찍힌 번호와 폴더로 `kill <번호>` · `rm -rf <폴더>` 를 돌린다 — 다른 셸 호출에서 `kill $!` 를 쓰지 마라(zsh 는 빈 `$!` 가 `0` 이라 `kill 0` 이 된다).」
- **SK-10 조건 본문 (a)** — 서버 명령 토큰을 위 글자로 바꾸고, 문장 토큰에 「다른 셸 호출에서 `kill $!` 를 쓰지 마라」 1 · 옛 「(같은 셸이면 `kill $!`)」 0 을 더한다.
  동작 문장 「Then 스크립트가 4 초 안에 종료 코드 0 으로 돌아오고(묶이지 않음) 띄운 서버가 `ui.html` 에 200 으로 답한다. 같은 포트를 다른 서버가 먼저 쥐면 출력에 `Address already in use` 가 1 줄 이상이고」 →
  「Then 스크립트가 4 초 안에 종료 코드 0 으로 돌아오고 그때까지의 출력에 `SERVING pid=` 줄이 1 이며, 띄운 서버가 `ui.html` 에 200 으로 답하고 그 줄의 번호로 `kill` 하면 그 포트의 서버가 0 이다. 같은 포트를 다른 서버가 먼저 쥐면 셸이 돌아온 때까지의 출력에 `NOT_SERVING` 줄이 1 이고」.
  양성 대조에 「예행 판(C5 반영) 명령 → 판정 줄 0 · 남은 서버 1 · 충돌 때 `NOT_SERVING` 0 (셸이 돌아온 때 `Address already in use` 도 0 줄)」
- **m.sh `api_serve`** — 두 번의 `perl … bash run.sh` 바로 뒤에 그때의 출력을 떠 둔다(`cp "$d/out.txt" "$d/out-exit.txt"` · `cp "$d/out2.txt" "$d/out2-exit.txt"`). 첫째 경우는 200 확인 뒤
  `pid=$(sed -nE 's/^SERVING pid=([0-9]+) .*/\1/p' "$d/out-exit.txt")` 로 번호를 뽑아 `kill` 하고 0.5 초 뒤 `pgrep -f "http.server $p" | grep -c .` 를 센다. 출력 줄을
  `run rc=… blocked=… http=… serving_line=<out-exit 의 ^SERVING pid= 줄 수> left_after_kill=<남은 수> | busy not_serving_line=<out2-exit 의 ^NOT_SERVING 줄 수> blocker_alive=…` 로 바꾼다(`addr_in_use` 는 빼거나 참고 값으로만 둔다)
- **SK-10 측정 기대값 둘째 줄** — `run rc=0 blocked=0 http=200 serving_line=1 left_after_kill=0 | busy not_serving_line=1 blocker_alive=1`. 시작 커밋 판 `run rc=142 blocked=1 http=200 serving_line=0 left_after_kill=1 | busy not_serving_line=0 blocker_alive=1`
- **`del.sh` 문장 삭제 대조** — 새 문장 둘(판정 줄 문장 · `kill $!` 금지 문장)을 토큰 목록에 더해 `del_cases` 를 다시 잰다
- `api_unset` 은 고치지 않아도 된다 — 새 명령으로 `unset_d served=0 guard_msg=1` 그대로다(`NOT_SERVING` 줄의 글자에 `D:` 가 없다)

#### R2 — 옛 파일 수 두 자리

- 측정 공통 정의 소개 문단(359 줄) 「서른 파일 가운데 하나라도 시작 · 끝 판에서 비면」 → 「마흔한 파일 가운데 하나라도 시작 · 끝 판에서 비면」 (`common.sh` 는 `FILES` 마흔하나를 돈다)
- 입력 항목 표 64 행 「이 계약 DG-05 는 옛 값을 서른 파일에 직접 세고」 → 「마흔한 파일에 직접 세고」

### 괜찮다고 본 것 (2 회차에 새로 본 것)

- **짝 계약이 먼저 끝나도 측정이 흔들리지 않는다** — 구간(`5b4fd72..$END`)에 짝 계약 커밋이 끼는 것이 실제 순서다. 그 위에 쌓은 예행이 기대값 그대로라, C1 · C3 로 넓힌 경로 식이 짝 계약의 정상 커밋을 걸지 않는다는 것이 실측으로 확인됐다
- **DG-05 (a) 와 새 V 줄 꼴** — 짝 계약(`3e874e8`)이 V 줄 끝에 `— WARN` · `— FAIL` 판정을 적게 바꿨다. DG-05 (a) 는 `— OK` · `— SKIP` 이 아닌 줄을 모두 세므로 경고도 걸리는 쪽이지만, 새 스크립트로 킷 열셋을 돌려 0 이다
- **ER-03 (e) 가 기대는 순서** — `kaizen-0924-final` 커밋이 구간에 들어오면 (e) 와 AR-01 첫째가 걸린다. Final 지침이 「두 계약이 끝난 뒤 시작한다」 로 막고, 상한은 개정 파일 `end_sha:` 로 고정돼 뒤 커밋은 구간 밖이다
- **문서 사이트 목록 (c)** — 짝 계약이 고친 드리프트 매핑이 이제 `onboarding-kit/skills/setup-guide/SKILL.md` 를 `docs/onboarding-kit/setup-guide.html` 로 잇는다. 그 페이지 글에는 이 계약이 바꾸는 Gotcha 8 · G1 검사 내용이 없어(`.env*` 는 프로젝트 탐색 단계 요약에만 나온다) 아홉에 넣지 않아도 뜻이 어긋나지 않는다. Final 이 매핑대로 다시 만들면 된다
- **참고(고치지 않아도 된다)** — `m NA` 의 `RE-01` 은 서명과 상관없이 구간 안에서 더한 파일을 센다. 지금 `1a71606` 까지 0 이고 짝 계약도 새 파일 0 을 자기 조건으로 잠갔다. DG-06 은 작업 폴더의 스크립트로 돈다(끝 판 사본이 아니다) — 1 회차 판단 그대로 둔다

### 조건끼리 부딪힘 — 2 회차

- R1 로 SK-10 첫 줄 토큰 · 둘째 줄 기대값 · mock.py · del.sh 가 함께 바뀐다. AR-02 (f) · RE-02 는 영향이 없다
- 그 밖에 서로 다른 값을 요구하는 조건 쌍은 찾지 못했다

### BUILD 가 봉인 전에 다시 할 것 — 2 회차

1. R1 · R2 를 초안 · `m.sh` · `mock.py` · `del.sh` 에 반영한다
2. 예행 판 · 시작 커밋 판에서 SK-10 을 다시 재 봉인 전 실측 표 SK-10 두 칸을 새 값으로 바꾸고, 문장 삭제 대조를 다시 돈다
3. 이 검토를 받은 뒤에 봉인한다

VERDICT: CHANGES
