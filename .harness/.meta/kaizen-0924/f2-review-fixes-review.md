# 카이젠 2026-09-24 Final — `kaizen-0924-f2-review-fixes` 계약 초안 검토

- 검토 대상: `.harness/sprint-contract-kaizen-0924-f2-review-fixes.md` (봉인 전 초안, 1040 줄 · 조건 30 줄 · 기능 조건 20, 검토 시점 sha256 앞 16 자 `9e185d8e3aa0dea4`)
- 개정 파일 `.harness/sprint-amendments-kaizen-0924-f2-review-fixes.md`: 아직 없다. BUILD 가 만들 파일이라 정상이다
- 검토자: REVIEW(독립 검토 역할) 에이전트. 사용자 승인 대신이다(공통 러닝북 「계약 규칙」 의 두 기록 시각). 쓴 파일은 이 검토 결과 하나다.
  측정과 사본은 전부 스크래치 `scratchpad/kaizen/f2rv/` 안에서 돌렸다. 작업 폴더 `HEAD` `6a8be19` 는 검토 전후 그대로이고, 미추적 파일은 계약 초안 하나 그대로다
- 읽은 입력: Final 러닝북 전문(§PR 직전 검토 수정 계약 포함) · 공통 러닝북(계약 규칙 · git 규칙 · 말투 · 검증 절) · `review-fixes.md` · 원본 JSON `tasks/w5ft0hgez.output`(confirmed 8 · low 23 · rejected 3) ·
  Codex `r4-final.md`(2 회차) · `r4-final-run1.md`(1 회차) · `harness/skills/sprint-contract/SKILL.md` Step 2 · 6.2 · 6.5 · 6.6
- 검토일: 2026-09-26

## 결론

**고칠 것 여섯(꼭 둘 · 권함 넷)이 있어 CHANGES 다.** 초안은 입력 항목을 43 줄 표로 빠짐없이 다뤘고, 조건마다 도우미 출력 줄과 시작 판 값이 붙어 있어
실패 상태를 한 문장으로 쓸 수 있다. 계약 안 측정 블록 여덟은 예행 도구(`f2d/k/`)와 글자까지 같았고, 다시 돌린 시작 판 값과 예행 판 값은 초안 표와 전부 같았다.

꼭 고칠 것은 둘이다.

1. **SK-01 이 옛 규칙 한 줄을 못 본다.** design-kaizen Step 5 의 「오케스트레이터가 Phase 로 호출한 경우 이 Step 을 실행하지 마라」(`:81`)는
   「커밋은 오케스트레이터가 한다」 와 같은 규칙인데 옛 문장 목록에 없다. 예행 끝 판에서 이 줄만 되살려도 `design_cmd=1 react_cmd=1 old=0` 로 통과한다(아래 실측)
2. **DG-06 이 빈 출력에 통과한다.** 「`FAIL` · `ERROR` 가 아니다」 라서 두 줄이 아예 안 나오거나 `SKIP` 이어도 통과로 읽힌다

권하는 넷은 측정이 계약 산문이나 러닝북이 말한 만큼을 다 재지 않는 자리다 — ER-08 (d) 감사 기록 더한 줄 수 · AR-02 (g) 낱말 비율 ·
ER-04 digest 입력 설명 줄 · 입력 표 39 행 사유 문장. 그 밖에 선택 셋(ER-02 개선안 문구 · SK-06 문장 · 양성 대조 넷)을 적었다.

## 직접 다시 돌린 것

계약 `## 회귀 게이트` 의 블록 여덟을 첫 주석 줄 이름대로 떼어 `f2rv/k/` 에 두고(`node_modules` 는 `p1build` 로 잇고 `MD013` 끔 설정),
`common.sh` · `m.sh` 를 읽는 bash 5.3 셸에서 `type m >/dev/null || exit 2; m <ID>` 로 돌렸다.

- 블록 여덟 = 예행 도구: `diff -q` 로 여덟 모두 같음
- 시작 판(작업 폴더, `END_OVERRIDE=6a8be19…`): SK-01 `design_cmd=0 react_cmd=0 old=2` · `i02 … rust-kaizen=0/3` / SK-02 `planning=10/12 reflect=3/4 tone_docs=8/11` · `uncovered=2 api_ref=1 docs_site_rows=7 same=0` · `phase_dep_line=0` /
  SK-05 empty 두 셸 `rc=1` / SK-06 `rc=2 (Is a directory)` / SK-08 `stale_title=1 fail_line=0 left=2` / ER-01 `inject=1 rc=0 scope=25/25 excluded_line=1 hit=0` / ER-03 missing `rc=0,stop=0,ok=0,broken=1` — 초안 표와 같다
- 예행 판(`f2d/rrepo`, 개정 파일의 `end_sha`): SK-01 ~ SK-08 · SC-00 · ER-01 ~ ER-08 · AR-01 · AR-02 · AP-01 · AP-03 · AP-04 · RE-02 · DG-02 를 돌렸고 모두 초안 표 값과 같다
  (예: ER-04 `before=1 after_noissues=0 after_new_fail=1` · `start_lib rc=1 start_hook rc=1` / SK-07 두 셸 `pid_is_server=1,dir_ok=1,released=1` / AR-01 `0` · `0 46` · `mixed=0 one_kit=13` · `0` · `SEAL_OK` · `scope_same=1 harness_line=1`)
- DG-06 은 `m` 대신 예행 저장소에서 직접: `scope-isolation` · `doc-contracts` 두 줄 `[ PASS  ]`
- 입력 표 40 행(N4) 재현 안 됨 확인: `760a75f` 판 「파일 389 개」 · `6a8be19` 판 「파일 391 개」 — 초안 말대로다
- 입력 표 34 행 확인: `qa-evaluation-guide.md:1231` 절의 항목 번호가 `1 · 2 · 3 · 3 · 4 · 5` 여섯이다 — 초안 말대로다

### 이 검토가 새로 돌린 대조

```text
SK-01 구멍   예행 끝 판 사본에서 design-kaizen Step 5 의 옛 줄 「오케스트레이터가 Phase 로 호출한 경우 이 Step 을 실행하지 마라」 만 되살림
             → design_cmd=1 react_cmd=1 old=0   (그대로 통과 — 커밋 주체가 다시 둘로 갈린 판)
             넓힌 정규식(아래 1 번)으로 세면 시작 판 old=3 · 예행 판 old=0
ER-04 태그   예행 끝 판 사본 SCHEMA.md 에서 ok:no-issues 줄을 지움 → schema_missing=1   (태그 문서 대조가 살아 있다)
DG-06        예행 판 · 변형 rv-mixed 모두 lines=2 pass=2 (validate-post-kaizen 의 scope-isolation 은 섞인 커밋을 못 잡는다 — 그건 AR-01 셋째가 잡는다)
ER-08 (d)    예행 판 감사 기록 더한 줄(빈 줄 제외) = 1
AR-02 (g)    예행 판 cov2 wr: 0.95→0.95 · 0.92→0.92 · 0.97→0.97 · 0.73→0.73 · 0.80→0.80 · 0.90→0.91 · 0.92→0.92 (일곱 모두 줄지 않음)
             api 쪽 둘째 원본 api-ui/SKILL.md → lost=0 wr 0.40→0.41
```

## 점검 항목별 판단

### 조건마다 실패 상태를 한 문장으로 쓸 수 있는가 — 예

서른 줄 모두 `m <ID>` 출력 값과 기대 값이 붙어 있다. N/A 넷(SC-00 · RE-01 · DG-01 · DG-03)도 측정 값을 달았다. 예외는 DG-06 하나다(아래 2 번).

### 측정이 뜻을 재는가 — 대부분 예, 둘은 아니다

- 돌리는 검사(SK-05 · SK-06 (b) · SK-07 · SK-08 · ER-01 ~ ER-06)는 모두 끝 판 블록 · 코드 · 훅을 떼어 사본에서 돌리고, 시작 판에서 같은 측정이 결함을 드러낸다. 음성 대조(ER-02 · ER-04 · ER-05 · SK-04 (c))도 봉인 전에 돌렸다
- 글자 조건은 삭제 대조가 붙어 있다. 다만 SK-01 의 「없어야 할 옛 문장」 목록이 같은 규칙을 담은 셋째 줄을 빠뜨렸다(1 번)
- 결정 전파 검사 입력 아홉은 A4 가 짚은 다섯 자리(맨 위 · decisions · 결정 하나 · excluded 항목 · required 항목)를 모두 친다

### 공통 러닝북 「봉인 전에 막는 측정 구멍」 목록 — 지킨다

- 상한: `END` 를 개정 파일 마지막 `end_sha:` 에서 받고 못 구하면 `END_UNRESOLVED` · 종료 코드 2 ✓
- 함수 정의 확인: 조건마다 `type m`, `m` 이 도우미 여섯과 두 판 폴더를 다시 본다. 확인 목록 밖 도우미(`toks` · `alltok` · `cnt` 등)는 없으면 값이 비어 기대 값과 어긋나므로 조용히 통과하지 않는다 ✓
- 건드리면 안 되는 파일: AR-01 첫째 · ER-08 (e) · SC-00 이 서명 목록이 아니라 `git log <기준>..<상한> -- <경로>` 로 센다 ✓
- 파일마다 비교: DG-02(규칙별 편집기 경고 · shellcheck 줄 수) · AP-03 이 파일마다 시작 판과 비교 ✓
- `validate-plugin.py` 는 종료 코드로(DG-05) ✓. 옛 값 검사 범위 문제는 ER-01 자체가 다룬다 ✓
- bash 강제(`NOT_BASH`) · exit 코드를 잴 때 `| tail` 없음 ✓

### 입력 항목이 빠짐없이 다뤄졌는가 — 예

원본 JSON 의 confirmed 8 · low 23 · rejected 3 을 하나씩 대조했다. A 여덟 · B 열넷은 조건, C 아홉 · 반박 셋은 23 ~ 34 행에 이유와 함께 있다.
Codex 1 회차 21 건 + 새 발견 둘, 2 회차 21 건 표 + N1 ~ N4 도 1 · 22 · 26 · 34 ~ 41 행에 모두 걸린다. 다음 사이클 토큰 열여덟도 「고치지 않음」 행과 맞다.
39 행의 사유 문장 하나가 사실과 다르다(아래 6 번).

### 범위가 Final 러닝북 표 안인가 — 예

마흔여섯 파일은 A · B · Codex 확정 지적이 가리키는 파일, 그 파일을 재는 시험 · 예시, `ci.yml`, 루트 `README.md`, 원본이 바뀐 문서 사이트 쪽 일곱,
그리고 `sync-docs.py` 가 다시 쓰는 킷 README 둘(`design-kit` AUTO:evals · `flutter-toolkit` 스킬 설명)이다. 루트 `CLAUDE.md` 는 러닝북이 허용했지만 43 행 이유로 손대지 않는다 — 더 좁은 쪽이라 문제없다.
문서 사이트 쪽은 바뀌는 문구(`위반 0` · `NO_MANIFEST` · `type verify_seal fm_get` · `design.json` · `no issues` · `한 번의 셸 호출` · `find_widget` 등)를 `docs/**/*.html` 전체에서 찾아봤고 일곱 쪽 밖에서는 나오지 않았다.
api 쪽 페이지는 원본 `docs/api/verification/…md` 가 안 바뀌지만, 그 쪽이 `api-ui/SKILL.md §7` 의 명령과 문장을 그대로 옮겨 적고 있어 맞추는 게 맞다.

### 조건끼리 부딪히는가 — 아니다

- AP-04(설명 줄 하나만 바뀜) ↔ SK-04 (b)(`Flutter Playwright` 뺌): 그 낱말이 「  Flutter 앱을 」 줄에만 있다 ✓
- ER-07 · AP-01(더한 줄 금지 글자) ↔ SK-04 · 예시 보고서 재생성: 예행 `k02=0 names=0 hits=0` ✓
- AR-01 셋째(묶음과 `.harness/` 섞지 않음) ↔ FIX 커밋: 범위 경계가 따로 싣도록 적었다 ✓
- SK-02 편집 자리(`:583` · F2 표 · 새 줄)는 AUTO 구간(`:409` ~ `:528`) 밖이라 DG-05 `sync-orchestrator.py --check-only` 와 부딪히지 않는다 ✓
- DG-05 `sync-docs.py --check-only` ↔ 킷 README 둘이 FILES 안에 있다 ✓

## 고칠 것 — 조건 ID 별 문구

봉인 전에 아래를 반영하고, 바뀐 ID(SK-01 · DG-06 · ER-08 · AR-02 · ER-04)는 시작 판 · 예행 판을 다시 재 `### 봉인 전 실측` 표를 고친 뒤 Step 6.5 를 다시 돌린다.
조건 수(30)와 기능 조건 수(20)는 바뀌지 않는다.

### 1. SK-01 — 꼭

- 조건 (a) 의 괄호를 이렇게 바꾼다:
  「옛 문장(「git add/commit/tag 를 직접 실행하지 마라」 · 「커밋은 오케스트레이터가」 · 「커밋은 오케스트레이터에」 · 「Phase 로 호출한 경우 이 Step 을 실행하지 마라」)이 든 줄 0」
- 양성 대조의 `old=2` → `old=3`
- `m.sh` SK-01 갈래의 정규식:

  ```bash
  old=$(cat "$E"/.claude/skills/*/SKILL.md | grep -cE 'git add/commit/tag 를 직접 실행하지 마라|커밋은 오케스트레이터(가|에)|Phase 로 호출한 경우 이 Step 을 실행하지 마라')
  ```

- 「예행 변형 · 삭제 대조」 표에 한 줄: `변형 step5-keep (design-kaizen :81 옛 줄만 되살림)  SK-01 → old=1` (지금 정규식이면 `old=0` 으로 통과한다 — 이 검토가 잰 값)

### 2. DG-06 — 꼭

- 조건 문구:
  「`python3 scripts/validate-post-kaizen.py --since 6a8be196d9c40a1686f51f9a6bd50039c2bd5b71` 출력에 `scope-isolation` 줄과 `doc-contracts` 줄이 각각 있고 둘 다 `[ PASS  ]` 로 시작한다 — 줄이 없거나 `SKIP` 이어도 실패다
  (측정: 작업 폴더에서 `type m >/dev/null || exit 2;` 뒤 `m DG-06` 끝 줄이 `dg06 lines=2 pass=2`)」
- `m.sh` DG-06 갈래:

  ```bash
  DG-06)
    python3 scripts/validate-post-kaizen.py --since "$B" 2>&1 | grep -E 'scope-isolation|doc-contracts' | awk '{print} /^\[ PASS/{p++} END{print "dg06 lines=" NR " pass=" p+0}' ;;
  ```

  (`docs-site-regen` 은 이 조건이 재지 않으므로 뺀다. 예행 판 · `rv-mixed` 에서 `dg06 lines=2 pass=2` — 이 검토가 잰 값)

### 3. ER-08 (d) — 권함

`## 범위 경계` 는 「이 줄 말고는 감사 기록을 고치지 않는다(ER-08 (d))」 라고 하는데, 측정은 지운 줄 0 과 포인터 줄 1 만 보고 더한 줄 전체 수를 안 잰다.

- 조건 (d): 「감사 기록 `.harness/.meta/orchestrator-audit-log.md` 는 시작 판에서 지운 줄 0 · 더한 줄(빈 줄 제외) 1 이고 그 줄이 `f2-review-fixes-notes.md` 를 담는다」
- `m.sh` ER-08 갈래 끝 두 줄:

  ```bash
  at=$(git diff "$B" "$END" -- "$AUD" | grep '^+' | grep -v '^+++' | grep -vc '^+[[:space:]]*$')
  ad=$(git diff "$B" "$END" -- "$AUD" | grep '^+' | grep -v '^+++' | grep -cF 'f2-review-fixes-notes.md'); dl=$(git diff "$B" "$END" -- "$AUD" | grep '^-' | grep -vc '^---')
  echo "audit added=$at added_ptr=$ad deleted=$dl shared_commits=$(…지금과 같음…)" ;;
  ```

- 기대 끝 줄 `audit added=1 added_ptr=1 deleted=0 shared_commits=0`. 양성 대조로 감사 기록에 줄 둘을 더한 변형 → `added=2` 를 예행 표에 넣는다

### 4. AR-02 (g) — 권함

Final 러닝북은 「담김 검사 `coverage.py` 로 옛 판 이상 유지」 라고 했는데 측정은 `lost` 만 본다. 부분 편집에서 원본 낱말이 페이지에서 빠지는 것은 못 잡는다.

- 조건 (g) 끝에 덧붙인다: 「… `lost` 0 이고, 원본 낱말이 페이지 글에 든 비율 `wr` 이 시작 판 페이지 이상이다」
- `m.sh` AR-02 갈래의 `awk '{print $2, $5}'` 를 바꾼다:

  ```bash
  python3 "$K/cov2.py" "$Bd" "$E" "$src" "$page" | awk '{w=$6; sub(/^wr=/,"",w); split(w,a,"->"); print $2, $5, (a[2]+0 >= a[1]+0 ? "wr_ok" : "wr_down")}'
  ```

- 기대: 뒤 일곱 줄이 모두 `… lost=0 wr_ok`
- (선택) api 쪽은 `api-ui/SKILL.md §7` 을 옮겨 적은 쪽이라 여덟째 짝 `$AUI $PAV` 를 더하면 그 부분도 잰다(예행 `lost=0 wr 0.40→0.41`)

### 5. ER-04 — 권함

이번 고침으로 `.errors.log` 에서 가장 흔한 줄이 `ok:no-issues` 가 된다. 그런데 reflect-digest `## 입력` 의 `.errors.log` 설명 줄(`:78`, 「훅 자체 실패 로그 … + `env-dedup:` … + `vocab:` … + `warn:lemma-map-unreadable`」)은
그 파일에 무엇이 들었는지 하나하나 적는 목록인데 새 줄이 없다. 그대로 두면 digest 를 도는 모델이 모르는 줄을 「훅 실패 요약」 에 실패로 셀 수 있다. 같은 파일(`$RDG`)이 이미 FILES 안이라 범위가 늘지 않는다.

- 조건 ER-04 끝에 덧붙인다: 「… reflect-digest Gotcha 13 줄과 `## 입력` 의 `.errors.log` 설명 줄(`/.errors.log` — 훅 자체 실패 로그` 가 든 줄)이 각각 `ok:no-issues` 를 담는다」
- `m.sh` ER-04 갈래의 태그 줄 끝에 `digest_in=$(grep -F '/.errors.log` — 훅 자체 실패 로그' "$E/$RDG" | grep -cF 'ok:no-issues')` 를 더하고 기대 값에 `digest_in=1` (시작 판 0 — 이 검토가 잰 값)
- `reflect-kit/README.md:84` 의 한 줄 설명(「훅 실패 메타 로그 + 환경 오설정 억제 기록」)은 원래도 `vocab:` 을 안 적는 뭉뚱그린 말이라 FILES 를 늘리지 말고 notes 다음 사이클 메모에 한 줄로 남기면 된다

### 6. `## 범위 경계` 입력 항목 표 39 행(Codex N2) — 권함 (서술 절이라 봉인 값에 닿지 않는다)

사유의 「(`docs/howto/` 에는 출처 표가 든 연구 기록이 없다)」 는 사실과 다르다. `.claude/skills/howto-research/SKILL.md` Step 1 에 「카테고리 · 문서 · 1차 출처」 표가 있고,
`docs/howto/changelog-feeds.md` 에 주소 30 개 · `deep-links.md` 에 17 개가 있다. N2 는 Codex 가 중간으로 매긴 지적이라 러닝북 원칙상 고치는 쪽이 기본이다. 둘 가운데 하나를 고른다.

- (가) 고친다: 오케스트레이터 `:25` 괄호를 「(Phase 17 표는 아직 없다 — 표가 생길 때까지 Phase 17 은 `.claude/skills/howto-research/SKILL.md` Step 1 표의 1차 출처에서 3 건 이상을 조회한다)」 로 바꾼다.
  `$KOR` 는 이미 FILES 안이다. SK-02 에 그 줄을 재는 값 하나(예: `p17_src=$(grep -F 'Phase 17 표는 아직 없다' "$E/$KOR" | grep -cF 'howto-research/SKILL.md')` → 1, 시작 판 0)를 더하고 처리 표 39 행을 「조건으로 다룸 — SK-02 (f)」 로
- (나) 넘김을 유지한다: 사유를 「howto-research Step 1 표는 출처 종류만 적고 주소가 없다. 의무 3 건을 어느 주소로 할지 고르는 일이 새 내용이라 Final 에서 하지 않는다」 로 고친다

## 선택 — 고치면 좋지만 막지는 않는다

- **ER-02 · 개선안 10**: 개선안은 「`assertions` 의 형이 틀리면 `SCHEMA_ERROR`」 라고 하는데 입력 아홉에 그 경우가 없다. 입력 하나(`assertions: "main visible"` 문자열 → 2)를 더해 열로 하거나 개선안 문구에서 `assertions` 를 뺀다.
  참고: 시작 판 코드에 문자열 `assertions` 를 넣으면 멈추지는 않고 종료 코드 1(위반)로 잘못 분류된다
- **SK-06 (b)**: 새 명령 `grep -rF … src/ | awk 'END{print NR}'` 는 `src/` 가 없을 때 grep 오류(종료 코드 2)가 파이프에 가려져 `0` · 종료 코드 0 이 된다. 바로 아래 Gotcha 16 이 경고하는 모양이다.
  같은 문단의 「(a) 대상 `.rs` 파일 수를 먼저 세고」 가 이 경우를 막으므로 막는 사유는 아니다. 문장에 「`src/` 가 없으면 오류는 화면에만 나오고 0 이 찍힌다 — (a) 로 거른다」 를 덧붙이면 오해가 없다
- **양성 대조가 적히지 않은 0 기대 값 넷**: AP-03 `bare_up`(마크다운 하나에 힌트 없는 펜스) · DG-02 `sh_up`(`decision-gate-test.sh` 에 따옴표 없는 변수) · RE-02 `copied_gate_lines`(시험에 `viol =` 줄 복사) · AR-02 `lost`(쪽에서 백틱 표시 하나 지움).
  예행 저장소에 변형 하나씩이면 된다

VERDICT: CHANGES

## 2 회차

- 검토 대상: `.harness/sprint-contract-kaizen-0924-f2-review-fixes.md` (봉인 전 초안, 1074 줄 · 조건 30 · 기능 조건 20, sha256 앞 16 자 `e35ae81b777b14e0` — 1 회차는 `9e185d8e3aa0dea4`).
  초안 작성자의 예행 사본 `scratchpad/kaizen/f2d/draft.md` 와 바이트가 같다
- 개정 파일은 아직 없다. 구현 단계가 만들 파일이라 정상이다
- 검토자: 검토 역할(REVIEW) 에이전트, 2 회차. 쓴 파일은 이 절 하나다. 측정과 사본은 전부 스크래치 `scratchpad/kaizen/f2rv2/` 안에서 돌렸다.
  작업 폴더 `HEAD` `6a8be19` 는 검토 전후 그대로이고, 미추적 파일은 계약 초안과 이 검토 파일 둘 그대로다
- 읽은 입력: Final 지침 전문 · 공통 지침(계약 규칙 · git 규칙 · 말투 · 검증 절) · 1 회차 검토(이 파일 위) · 계약 초안 전문 · 예행 도구 `f2d/k/`(`rehearse.sh` · `vedit.py` · `del.sh` · `runfinal.sh`) ·
  `harness/skills/sprint-contract/SKILL.md` Step 6.2 · 6.5 · 6.6 · `harness/references/contract-schema.md` 허용 머리 표 · 커버리지 검출기 블록(`:758`)
- 검토일: 2026-09-26

### 2 회차 결론

**APPROVE 다.** 1 회차가 적은 고칠 것 여섯(꼭 둘 · 권함 넷)과 선택 셋이 모두 조건 문장 · 측정 블록 · 봉인 전 실측 표에 반영됐다.
계약에서 떼어 낸 측정 블록으로 조건 서른을 예행 판 · 시작 판 · 변형 스물에서 다시 돌렸고 값이 계약 표와 전부 같았다. 새로 막을 결함은 찾지 못했다.
봉인 전에 손보면 좋은 작은 것 셋은 끝에 적었다 — 막는 사유는 아니다.

### 1 회차 지적별 반영 확인

| 1 회차 | 계약에서 바뀐 자리 | 이번에 잰 값 |
| --- | --- | --- |
| 1 SK-01 (꼭) | 조건 (a) 옛 문장 넷째 「Phase 로 호출한 경우 이 Step 을 실행하지 마라」 · `m.sh` 정규식 · 양성 대조 `old=3` · 변형 `step5-keep` · Pre-Edit 표 `:81` 줄 | 시작 `old=3` · 예행 `old=0` · `step5-keep` → `old=1` |
| 2 DG-06 (꼭) | 조건 문구(줄이 없거나 `SKIP` 이면 실패) · `m.sh` 갈래가 `docs-site-regen` 을 빼고 `dg06 lines= pass=` 를 찍음 · 변형 `dg06-fail` · `dg06-skip` | 작업 폴더(시작) `dg06 lines=2 pass=2` · 예행 `lines=2 pass=2` · `dg06-fail` → `pass=1` (`[ FAIL  ]` scope-isolation) · `dg06-skip` → `pass=1` (`[ SKIP  ]` doc-contracts) |
| 3 ER-08 (d) | 조건 (d) 「더한 줄(빈 줄 제외) 1」 · `m.sh` 의 `at` · 범위 경계 「ER-08 (d) 가 … 1 로 잰다」 · 변형 `audit2` | 예행 `audit added=1 added_ptr=1 deleted=0 shared_commits=0` · `audit2` → `added=3` |
| 4 AR-02 (g) | 조건 (g) 에 `wr` · `m.sh` awk 가 `wr_ok` / `wr_down` 을 찍음 · 여덟째 짝 `$AUI $PAV` · 변형 `page-loss` · `page-prose` | 예행 여덟 줄 모두 `lost=0 wr_ok` · `page-loss` → `design.html lost=1 wr_ok` · `page-prose` → `design.html lost=0 wr_down` (원값 `wr=0.90->0.84`) · api-ui 짝 원값 `0.40->0.41` |
| 5 ER-04 | 조건 끝 digest `## 입력` 줄 · `m.sh` `digest_in` · 처리표 44 행 · ER-08 토큰 `reflect-kit/README.md` (열아홉째) · 이름 고정 목록에 그 줄 머리 | 시작 `digest_in=0` · 예행 `1` · `no-digest-in` → `0` |
| 6 처리표 39 행 | (가) 고침을 골랐다 — 개선안 2 · SK-02 (f) · `m.sh` `p17_src` · 이름 고정 목록에 「Phase 17 표는 아직 없다」 · 배경 · Pre-Edit 표 | 시작 `p17_src=0` · 예행 `1` · `no-p17` → `0` · 그 줄을 통째로 지운 사본 → `0` |
| 선택 ER-02 | 입력 열에 `assertions` 문자열(`assertstr:2`) · 개선안 10 · Pre-Edit 표 | 시작 `gate ok=5/10 traceback=4 wrong: … assertstr=1` · 예행 `gate ok=10/10 traceback=0` · 킷 시험 `결과: 10 경우 중 불일치 0` · 시작 판 문서로 `불일치 5` · `exec=100755` |
| 선택 SK-06 (b) | 조건 끝 「가 없으면」 · 「(a) 로 거른다」 · `no_src_note` · 변형 `no-src-note` | 예행 `no_src_note=1` · 변형 → `0` |
| 선택 양성 대조 넷 | 변형 `bare-fence` · `sh-unquoted` · `copied-gate` · `page-loss` | `bare_up=1 v6_rc=2` · `SC_UP … decision-gate-test.sh 0>1` · `copied_gate_lines=1` · `lost=1` |

조건 수(30)와 기능 조건 수(20), 고치는 파일 마흔여섯은 그대로다 — N2 · ER-04 고침이 이미 `FILES` 안 파일(`$KOR` · `$RDG`)이라 마크다운 27 · 셸 5 · SKILL.md · agents 18 셈도 바뀌지 않는다.

### 2 회차에 직접 다시 돌린 것

계약 `## 회귀 게이트` 절의 블록 여덟을 첫 주석 줄 이름대로 떼어 `f2rv2/k/` 에 두고(`node_modules` 는 `p1build` 로 잇고 `MD013` 끔 설정, `markdownlint-cli2 v0.23.2`),
`common.sh` · `m.sh` 를 읽는 bash 5.3 셸에서 `type m >/dev/null || exit 2` 뒤 `m <ID>` 로 돌렸다.

- 떼어 낸 블록 여덟 = 예행 도구 `f2d/k/`: `cmp` 로 여덟 모두 같음
- 예행 판(`f2d/rrepo`, 개정 파일의 `end_sha` `40e5fcf`, 봉인 계약은 지금 초안과 봉인 두 줄만 다름): 조건 서른 전부를 돌렸고 모두 계약 「조건별」 표와 조건 문장의 기대 값과 같다
  (예: AR-01 `0` · `0 46` · `mixed=0 one_kit=13` · `0` · `SEAL_OK` · `scope_same=1 harness_line=1` / DG-04 열하나 모두 `=0` / DG-05 `validate_fail: none` · 검사 일곱 `=0`)
- 시작 판(`END_OVERRIDE=6a8be19…`): SK-01 ~ SK-08 · ER-01 ~ ER-06 · AR-02 · AP-04 — 표와 같다
- 변형 스물: 「예행 변형」 표의 값과 모두 같다
- 삭제 대조: 표의 SCHEMA.md `ok:no-issues` 줄 → `schema_missing=1` 을 다시 쟀고, 새로 셋을 더 쟀다 —
  DESIGN.md `ok:no-issues` 줄 → `design_missing=1` · design-kaizen 서명 줄 → `design_cmd=0` · 오케스트레이터 「Phase 17 표는 아직 없다」 줄 → `p17_src=0`
- Step 6.2 · 6.5 를 레포 원본에서 떼어 돌림: 조건 `30` · 기능 조건 `20` · `##` 머리 열둘이 모두 허용 목록(서술 다섯은 접두 일치) · 체크박스 서른 줄 모두 조건 절 · `OK conditions=30` · `OK 미실측 0 건`.
  커버리지 검출기는 `UNCOVERED` 여섯(SK-01 · SK-02 · SK-04 · ER-08 · AR-02 · DG-05)을 냈고, 모두 `## 범위 경계` 「커버리지 해소」 줄이 같은 경로를 연다(SK-02 의 새 `howto-research/SKILL.md` 도 그 줄에 있다)

### 새 결함 찾기 — 없음

- 넓힌 옛 문장 정규식이 다른 스킬의 정상 문장에 걸리지 않는가: 예행 판 `.claude/skills/*/SKILL.md` 에서 「실행하지 마라」 가 든 줄은 create-kit `:21` 「직렬로 실행하지 마라」 하나이고 정규식 넷째 문장과 다르다 → `old=0`
- ER-08 (d): 감사 기록은 줄바꿈으로 끝나(`618` 줄) §Phase 다음 사이클 메모(`:595`) 끝에 한 줄을 더해도 `-` 줄이 생기지 않는다
- 새로 요구한 문장과 ER-07 · AP-01: 예행 `added=205 k02=0 names=0` · `versions=11 hits=0`
- SK-02 (f) 편집 자리 `:25` 는 AUTO 구간 밖이다 — 예행 DG-05 `sync-orchestrator.py=0`
- 39 행에서 계속 넘기는 `phase-research-templates.md` Phase 17 표는 감사 기록 `:542` (`F1H-76`)에 이미 다음 사이클로 적혀 있어, 토큰 열아홉에 없어도 빠지지 않는다
- 측정 블록 · 표 · 조건 문장 사이 수(변형 스물 · 삭제 대조 열일곱 · 음성 대조 넷 · 토큰 열아홉 · 짝 여덟)가 서로 맞다. `page-prose` 가 지운 문단 수 19 도 실제로 셌다

### 봉인 전에 손보면 좋은 것 — 막지 않는다

1. `m.sh` ER-02 갈래 주석 `# A4 — 입력 아홉의 종료 코드 …`(계약 556 행)가 옛 수다. 입력이 열이 됐다. 봉인은 조건 줄만 덮으므로 고쳐도 봉인과 무관하다
2. tone-kaizen 두 줄: SK-02 (b) 로 `:35` 가 11 이 되면 같은 파일 `:100` 「리서치 문서 8종」 과 나란히 남는다. 둘 다 맞는 수다(글로브 전체 11 · 리서치 문서 8 = 11 − overview · research-log · templates).
   다만 예행 편집(`mock.py`)의 괄호 「(overview · research-log 포함)」 은 templates 를 빼 8 + 2 로 읽힌다 — 구현 때 괄호에 셋을 모두 적으면 된다.
   그리고 f1 harness 계약이 같은 두 줄을 「셈 기준 불분명 — 다음 사이클」 로 넘겼다(`F1H-78`, 감사 기록 `:544`). notes `## 다룬 항목` 에 「`F1H-78` 의 `:35` 쪽은 B4 로 닫았고 `:100` 은 리서치 문서 셈이라 둔다」 한 줄을 남기면 감사 기록과 어긋나 보이지 않는다
3. SK-02 (f) 는 다른 문서 조건처럼 낱말 셋이 한 줄에 있는지만 잰다 — 반대 뜻 문장도 통과한다. `## 범위 경계` 「판정 근거」 줄이 SK-02 를 문장 자체가 산출물인 조건으로 이미 적었으므로 조건을 바꿀 일은 아니고, QA 가 그 줄 전문을 한 번 읽어 뜻을 확인하면 된다

참고: 이 맥에 `python3 -m http.server 60349`(번호 1220, 부모 1, 01:59 시작)가 떠 있다. 이 검토보다 먼저 시작된 것이라 끄지 않았다 — 시작 판 A8 재현(`&&` 이음이라 찍힌 번호가 하위 셸이었다) 때 남은 서버로 보인다. SK-07 측정은 빈 포트를 새로 골라 돌아 영향이 없다.

VERDICT: APPROVE
