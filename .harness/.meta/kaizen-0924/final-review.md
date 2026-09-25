# 카이젠 2026-09-24 Final — `kaizen-0924-final` 계약 초안 검토

- 검토 대상: `.harness/sprint-contract-kaizen-0924-final.md` (봉인 전 초안, 1496 줄 · 조건 26 줄 · 기능 조건 18, 검토 시점 sha256 앞 16 자 `50a027d88f4a03d9`)
- 개정 파일 `.harness/sprint-amendments-kaizen-0924-final.md`: 아직 없다. BUILD 가 만들 파일이라 정상이다
- 검토자: REVIEW(독립 검토 역할) 에이전트. 사용자 승인 대신이다(공통 러닝북 「계약 규칙」 의 두 기록 시각). 쓴 파일은 이 검토 결과 하나다.
  측정과 사본은 전부 스크래치 `scratchpad/kaizen/final-rv3/` 안에서 돌렸다. 작업 폴더 `HEAD` `511f19b` · 원래 레포 `HEAD` `5136cc2` 는 검토 전후 그대로다
- 읽은 입력: Final 러닝북 전문 · 공통 러닝북(계약 규칙 · git 규칙 · 말투 · 검증 절) · 진행 스킬 `.claude/skills/kaizen-orchestrator/SKILL.md` Step F1 ~ F4(`:576-793`) ·
  `final-todo.md` · `xdiag-all.md`(P1 · P15 · P17 절은 전문) · 두 후속 계약 notes 의 넘기는 것 · 다음 사이클 메모 · 고치지 않은 항목 · Phase notes 열일곱의 미반영 절
- 검토일: 2026-09-25

## 결론

**고칠 것 여섯이 있어 CHANGES 다.** 초안은 입력 항목을 80 줄 표(입력 표 번호 FN-01 ~ FN-80)로 다뤘고, 조건마다 도우미 출력 줄과 시작 판 값이 붙어 있어
탈락 상태를 한 문장으로 쓸 수 있다. 다시 돌린 시작 판 값은 초안의 봉인 전 실측 표와 전부 같았다. 고칠 것은 세 갈래다.

1. **측정 도우미 버그 하나** — `mdcmp.sh` 가 편집기 경고의 열 번호를 줄 번호로 읽는다. 새 항목을 파일 위쪽에 깨끗이 끼우기만 해도 새 경고로 센다.
   changelog · 연구 기록은 새 항목이 위에 붙는 파일이라 구현이 깨끗해도 DG-02 가 떨어진다(1 번)
2. **조건이 옛 값을 묶어 둔다** — 첫 화면 파일 `docs/index.html` 을 「그대로」 로 잠갔는데, 거기 harness 다섯 항목 제목에 이번 사이클에 오른 판 번호가 들어 있다.
   페이지 판 번호도 어떤 글자 검사도 재지 않는다(2 번)
3. **측정이 뜻을 덜 잰다** — 릴리스 계획 근거 칸 꼴(3 번) · 메모리 후보 근거 경로가 세션 뒤 사라짐(4 번) · per-kit 연구 기록 여섯과 출처 URL 수(5 번) ·
   감사 기록과 notes 가 옮긴 항목을 찾아갈 자리(6 번)

여섯 모두 고칠 문구를 아래에 적었다. 새 측정 줄은 이 검토에서 시작 판과 나쁜 예 사본에 먼저 돌려 값을 적었다.

## 직접 다시 돌린 것

계약의 「도우미 준비」 떼는 명령을 그대로 돌려 `final-rv3/K/` 에 도우미 스물넷을 두었다. 공통 정의는 `END` 한 줄만 바꾼 사본으로 `END=511f19b` 에서 돌렸다.
원래 공통 정의는 개정 파일이 없어 `END_UNRESOLVED` · 종료 코드 2 로 멈춘다 — 설계대로다.

- SK-01: `f1.sh` 네 줄 `p1hand=0 0 0 0 0 0 4 1` · `parity=1 1` · `apikit=1 1 1 1 1 1 1` · `orch16=1 1 1 1 1`. `tonegrade.py` `raised=0` 종료 코드 0.
  `toneterms.py` `tone_terms=8 other_files=119 other_terms=652 intersect=0 substring=0`. design-guide 설명에 「"톤 위반"」 을 넣은 사본은 `intersect=1` 로 떨어진다.
  `synt.sh` `sh=16 sh_bad=0 py=8 py_bad=0 json=14 json_bad=0 yaml=2 yaml_bad=0 actionlint_rc=0` — 초안 값과 같다
- ER-01 · ER-02: 슬러그 열일곱의 평가자 · 계약 피드백을 스크래치에 떠서 `fbx.py` → `evaluator files=17 by=0 marker=0 tok=0 keep=17 other_diff=0` ·
  `contract files=17 by=17 marker=0 tok=0 keep=17 other_diff=0`. 서른넷 모두 `cross_diagnosis_by` · `cross_diagnosis_notes` 줄이 하나씩이라 `fbedit.py` 가 걸리지 않는다
- ER-03: `amend.sh` → `ends=1 2 … p1_last=0 kept=16 xfix=0 0 0 0 p1_remeasure=0 0 guides=2 after=18 after_other=1` · `OTHER 76cfb37 p01-guides`.
  P1 의 `after` 둘은 `fc29b58`(end_sha 기록) · `76cfb37`(notes) 이라 끝 판 `after=16` 이 맞다
- ER-04: `stale.sh` 시작 판 `clean rc=0 values=15 why_missing=0 unexcluded=1 3 seeded=[0 rc=0 ] [0 rc=0 ] [0 rc=0 ]`.
  개선안 5 번 글자대로 등록부를 고친 사본 → `clean rc=0 values=18 why_missing=0 unexcluded=0 0 seeded=[1 rc=1 ] [1 rc=1 ] [1 rc=1 ]` — 끝 판 기대값에 닿는다
- ER-05: 모의 폴더 열한 파일(`CAP=7`)로 `cleanup-do.py` → `moved=4`, 두 번째 호출 `STOP` 종료 코드 2. `cleanup.py` 바른 이동 `archived_is_oldest=1 leaked=0 missing=0 log=1`,
  한 파일을 되돌리고 다른 파일을 옮기고 하나를 지운 사본 `archived_is_oldest=0 leaked=1 missing=2`. 전역 피드백은 639 개다
- AR-01: `done=0 status_only=0 seal_ok=19 fb_tracked=0 fb_new=0 dirty=38`. 작업 폴더의 열아홉 계약 차이는 모두 `-status: active` `+status: done` 한 줄이다
- AR-02: `rows=96 same_rows=1 phase_rows=74 phase_ok=0 miss_ok=0/8 other_note=0 non_phase_changed=0` · 검사기 `Phase 행 미완료 74` · `TRACKING_TABLE_FAIL`.
  초안에 없던 0 기대 값 둘의 양성 대조를 더 돌렸다 — 처리 배정표의 `이번 스프린트` 행 비고를 고친 사본 `non_phase_changed=1`, Phase 7 행 비고를 고친 사본 `other_note=2`. 둘 다 살아 있다
- AR-03: `pairs=44 exist=44 changed=0 short=7 accent=0 ext=0 hidden_up=0 tok_new=0/42 tok_old=9/9 html_added=0 html_removed=0`.
  `TOKENS` 51 개를 원본과 맞대 보니 새 글자는 모두 원본에 있고 옛 글자는 모두 원본에 없다. 44 페이지 모두 글자 하나 이상을 맡는다
- AR-03 페이지 목록: `detect-docs-drift.py --since 390dea8` 로 잇는 페이지 32 · 이름이 다른 페이지 1 · 같은 이름 페이지 10 · notes 넘김 1 을 다시 셌다.
  바뀐 킷 파일 이름으로 `docs/<킷>/<이름>.html` 을 찾는 방식으로 훑어도 목록 밖 페이지는 0 이다. `[NEW]` 스물 가운데 `docs/` HTML 에 이름이 나오는 것
  (`core-comment.md` 등)은 참고 링크일 뿐 그 원본을 옮긴 페이지가 아니다 — 초안 판단이 맞다
- AR-04 · AR-05 · AR-06 · AR-07: `files=5 bad=12 known_urls=350` · `state=0 phases=14 keys_ok=0 zero=0 last_updated=0 evals=[MISSING]` · `MISSING` ·
  `append_only=1 head=0 generated=0 manual_orch=0 f1h=0/29 f1k=0/33 new4=0/4 notes=0/17`. `audit.sh` 의 `F1H` 스물아홉은 harness 후속 notes 표와 글자 그대로 같다
- SC-01: `MISSING release-plan.md` 종료 코드 2. 모의 계획 파일 두 벌은 3 번에 적었다
- DG-04: 44 페이지 `44/44 PASS` 종료 코드 0, 모든 `OK` 줄 `err=0` (37 초)
- DG-05: `bash dg05.sh 511f19b 83cfb4f` → `rc=[000000000100000000000] vpk_rc=1 vpk_pass=12 vpk_bad=1 vpk_skip=[marketplace-sync plugin-json-bumps]` ·
  `NONZERO rc=1 python3 scripts/check-api-kit-docs.py` · `docs-site-regen` 실패 — 초안 값과 같다. 음성 대조로 복제본의 `cycle_id` 만 `kaizen-2026-09-24` 로 바꿔
  `validate-post-kaizen.py` 를 돌리니 `changelog-entry` · `research-log` · `docs-site-regen` · `cleanup-log` · `failure-count` · `evals-audit` 여섯이 실패한다 — AR-05 동기가 맞다
- 봉인: 시작 판 `.harness/sprint-contract*.md` 78 개 가운데 `SEAL_OK` 69 · `SEAL_ABSENT` 9 · `SEAL_BROKEN` 0 이라 AR-09 `broken=0` 을 끝 판에서 기대할 수 있다

## 반드시 고칠 것

### 1. DG-02 — `mdcmp.sh` 가 열 번호를 줄 번호로 읽는다

`mdcmp.sh` 의 sed 식 `s/^[^ ]*:([0-9]+)(:[0-9]+)? (error|warning) (MD[0-9]+)\/.*/\1 \4/p` 은 앞쪽 `[^ ]*` 가 욕심껏 먹어서,
`파일:309:1 error MD060/…` 처럼 열이 붙은 경고에서 줄 번호 `309` 대신 열 번호 `1` 을 잡는다.

```text
$ echo 'CLAUDE.md:309:1 error MD060/table-column-style …' | sed -nE '<계약의 식>'
1 MD060
$ echo 'CLAUDE.md:306 error MD036/no-emphasis …' | sed -nE '<계약의 식>'
306 MD036
```

그래서 열이 붙는 규칙(MD060 · MD034 · MD033 · MD004 · MD038 …)은 「그 줄 글자」 가 엉뚱한 줄 글자가 된다. 그 줄이 편집으로 밀리면 경고가 그대로여도 새 경고로 센다.

- 재현: `docs/kaizen/flutter-research-log.md` 사본 9 줄째에 경고 없는 새 항목 네 줄을 끼우고 `last_updated` 만 바꿨다. markdownlint 원래 출력은 옛 판 일곱 · 새 판 일곱으로
  같은 경고가 네 줄 밀렸을 뿐인데 `mdcmp.sh` 는 `new=4 MD033:1 MD060:3` 을 낸다
- 이 계약에서 반드시 터진다: `docs/kaizen/research-log.md` 에 열 53 경고(MD034)가 있고 53 번째 줄 글자로 묶인다. changelog · `research-log.md` · `flutter-research-log.md` 는
  새 항목이 위에 붙는 파일이다. 그 사본 첫 `##` 앞에 경고 없는 새 항목 네 줄을 끼우니 `new=1 MD034:1` 이 나왔다. DG-02 `new_total=3` 이 깨끗한 구현에서도 맞지 않는다
- 초안의 양성 대조(감사 기록 끝에 붙인 MD012 · MD022 · MD032 · MD034)는 줄이 밀리지 않는 파일 끝이라 이 버그를 못 봤다

고칠 문구 — `mdcmp.sh` 의 sed 줄을 아래로 바꾼다(경로에 콜론이 없다 — 두 판은 `TMPDIR` 아래에 푼다):

```bash
    | sed -nE 's/^[^:]*:([0-9]+)(:[0-9]+)? (error|warning) (MD[0-9]+)\/.*/\1 \4/p' \
```

두 재현 사본에서 바꾼 식은 모두 `new=0` 이고, flutter 사본 끝에 맨 URL 한 줄과 옛 제목 한 줄을 더하면 `new=2 MD024:1 MD034:1` 로 두 줄 글자가 바르게 찍힌다.
「봉인 전 실측」 표 `DG-02 · AP-03` 행의 양성 · 음성 대조 칸에 한 줄을 더한다:

```text
음성 대조: 새 항목을 파일 위쪽(flutter-research-log 9 줄째)에 경고 없이 끼운 사본 → new=0 (고치기 전 식은 new=4 로 잘못 셌다)
```

### 2. AR-03 — 첫 화면 제목의 판 번호가 묶이고, 페이지 판 번호를 재지 않는다

`docs/index.html:234-238` 의 harness 다섯 항목 제목에 원본 판 번호가 있다. 사이클 시작(`83cfb4f`) 때는 넷이 원본과 같았는데 이번 사이클이 전부 올렸다.

- `skill-design` `v1.5.0` → 원본 `1.6.0` · `agent-design` `v1.6.0` → `1.7.0` · `contract-design` `v5.0` → `v5.1` · `qa-evaluation` `v5.0` → `v5.1` · `contract-schema` `v5.3` → `v5.5`
- 초안은 `git diff --quiet "$B" "$END" -- docs/index.html` 로 이 파일을 잠갔고 범위 경계도 「이번에 바꿀 것이 없다」 라고 적었다. 그대로면 페이지를 다시 만든 뒤에도
  첫 화면 목록이 옛 판 번호를 보인다 — 진행 스킬 F2 넷째 줄(「갱신 페이지 등록」) · F4 체크리스트 「대응 HTML 이 최신」 과 부딪힌다
- 페이지 쪽도 같다. 44 페이지 가운데 열넷이 원본 머리 설정 판 번호를 제목 · 뱃지에 보인다(예: `<title>스킬 설계 가이드 v1.5.0 — Harness</title>` · `v1.5.0 · 2026-08-13`).
  `TOKENS` 는 판 번호를 하나도 재지 않아, 옛 뱃지를 그대로 옮긴 페이지도 AR-03 을 통과한다. 아래 새 글자 열넷은 지금 페이지 본문에 모두 0 개다(`docs.py` 의 `text()` 로 셈)

고칠 문구:

- AR-03 조건 본문의 「`docs/` HTML 목록과 `docs/index.html` 은 시작 판 그대로이고, 이 계약 서명 커밋이 건드린 HTML 은 정확히 그 마흔넷이다」 를 아래로 바꾼다

```text
`docs/` HTML 목록은 시작 판 그대로이고, `docs/index.html` 은 harness 다섯 항목(`skill-design` · `agent-design` · `contract-design` · `qa-evaluation` · `contract-schema`)
제목의 판 번호 다섯 줄만 원본 판 번호로 바뀐다. 원본 판 번호가 사이클 동안 바뀐 페이지 열넷은 새 판 번호를 본문에 담는다.
이 계약 서명 커밋이 건드린 HTML 은 그 마흔넷과 `docs/index.html` 이다
```

- `docs.py` 의 `TOKENS` 끝에 열넷을 더한다(끝 판 기대 `tok_new=56/56 tok_old=0/9`, 시작 판 `tok_new=0/56 tok_old=9/9`):

```python
    ("new", "docs/harness/skill-design-guide.html", "1.6.0"),
    ("new", "docs/harness/agent-design-guide.html", "1.7.0"),
    ("new", "docs/harness/contract-design-guide.html", "v5.1"),
    ("new", "docs/harness/qa-evaluation-guide.html", "v5.1"),
    ("new", "docs/harness/contract-schema.html", "v5.5"),
    ("new", "docs/harness/plugin-validation.html", "1.4.0"),
    ("new", "docs/react-kit/render-evidence-protocol.html", "1.1.0"),
    ("new", "docs/backend-kit/database.html", "0.3.0"),
    ("new", "docs/api-kit/contract-extraction-modes.html", "0.1.1"),
    ("new", "docs/api-kit/snapshot-sealing-canonicalization.html", "0.1.1"),
    ("new", "docs/api-kit/auth-secret-lifecycle.html", "0.2.1"),
    ("new", "docs/api-kit/probe-synthesis-hurl-semantics.html", "0.2.1"),
    ("new", "docs/api-kit/regression-diff-failure-policy.html", "0.1.1"),
    ("new", "docs/api-kit/static-evidence-viewer-contract.html", "0.1.1"),
```

- AR-03 측정의 `git diff --quiet "$B" "$END" -- docs/index.html` 종료 코드 0 을 아래 둘로 바꾼다.
  `git diff --numstat "$B" "$END" -- docs/index.html | tr '\t' ' '` 가 `5 5 docs/index.html` 한 줄, 그리고 아래 블록이 `nav_ver=5/5`(시작 판 `nav_ver=0/5`, 다섯 줄을 고친 사본 `nav_ver=5/5` · numstat `5 5` — 이 검토에서 돌림)

```bash
python3 - "$T/E/docs/index.html" <<'PY'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
want = {"skill-design": "v1.6.0", "agent-design": "v1.7.0", "contract-design": "v5.1", "qa-evaluation": "v5.1", "contract-schema": "v5.5"}
ok = sum(1 for i, v in want.items() if re.search(r"\{ id: '%s',\s*title: '[^']*%s'" % (re.escape(i), re.escape(v)), t))
print(f"nav_ver={ok}/{len(want)}")
PY
```

- AR-03 측정의 `my | grep -cE '^docs/.+\.html$'` 44 를 `my | grep -E '^docs/.+\.html$' | grep -vxF docs/index.html | grep -c .` 44 로 바꾼다
- 범위 경계의 「`docs/index.html` 과 루트 `README.md` 는 러닝북 범위이지만 이번에 바꿀 것이 없다(새 페이지가 없고, …)」 를
  「`docs/index.html` 은 harness 다섯 항목 제목의 판 번호만 고친다(원본 판 번호가 이번 사이클에 올랐다). 루트 `README.md` 는 바꿀 것이 없다(README 판 번호 표는 릴리스 때 `release.sh` 가 고친다)」 로 바꾼다.
  개선안 6 번의 「새 페이지 · `docs/index.html` 편집은 없다」 도 「새 페이지는 없다. `docs/index.html` 은 위 다섯 제목의 판 번호만 고친다」 로 바꾼다

### 3. SC-01 — 근거 칸을 짧은 파일 이름으로 쓰면 `basis=0`

`plan.py` 의 `rows` 식은 근거 칸에서 `` `.harness/.meta/kaizen-0924/<파일>.md` `` 꼴의 전체 경로만 읽는다. 그런데 개선안 9 번이 옮기라는 GAP 분석 릴리스 표는
`` `phase3-notes.md` `` 처럼 짧은 이름이다. 모의 계획 파일로 쟀다 — 표 열넷 · `release.sh` 열네 줄에 근거를 짧은 이름으로 쓰면
`changed=14 cmds=14 lines_ok=1 level_ok=14/14 basis=0 bumped=0`, 전체 경로로 쓰면 `basis=14` 다. 표를 그대로 옮기면 SC-01 은 반드시 떨어진다.

고칠 문구 — SC-01 조건 본문의 「표의 근거 칸이 있는 notes 파일을 가리킨다」 를 아래로 바꾸고, 개선안 9 번 끝에 같은 뜻 한 줄을 더한다:

```text
표의 근거 칸이 notes 파일을 `.harness/.meta/kaizen-0924/<파일>.md` 전체 경로(백틱으로 감쌈)로 가리키고 그 파일이 있다
```

### 4. AR-06 — 메모리 후보의 근거 경로가 세션이 끝나면 사라질 수 있다

F3.5 후보 파일을 받는 쪽은 뒤 세션의 `/reflect-promote` 다(`reflect-promote/SKILL.md:44`). 그런데 이 계약의 후보 근거는 「교차 진단」 이고,
그 원문 `xdiag-all.md` 는 세션 스크래치(`/private/tmp/…`)에만 있다. `mem.py` 는 경로가 **재는 순간** 있는지만 보므로 스크래치 경로를 적어도 통과하고,
다음 세션에서는 그 근거를 열 수 없다.

고칠 문구 — AR-06 조건 본문의 「`source_evidence` 경로는 모두 있고」 를 아래로 바꾼다:

```text
`source_evidence` 경로는 모두 있고, 저장소 경로이거나 `~/.harness/` 아래다 — `/private/tmp` · `/tmp` 아래 경로는 0 개다(세션이 끝나면 사라진다)
```

측정 — `mem.py` 의 `ev_bad` 반복 안에 아래를 더하고 끝줄에 `tmp_bad=` 를 찍는다. 끝 판 기대 `tmp_bad=0`, 양성 대조는 모의 파일에 스크래치 경로 한 줄 → `tmp_bad=1`:

```python
        if p.startswith(("/private/tmp/", "/tmp/")):
            tmp_bad += 1; print("NG 세션 스크래치 경로", p)
```

(`tmp_bad = 0` 을 반복 앞에 두고, 마지막 `print` 끝에 빈칸 하나와 `tmp_bad={tmp_bad}` 를 붙인다.) 교차 진단 근거는 ER-01 · ER-02 가 적는 전역 피드백 파일이나
notes `## 교차 진단 기록` 절을 가리키면 된다.

### 5. AR-04 — per-kit 연구 기록 여섯과 출처 URL 수를 재지 않는다

진행 스킬 F4 3 번과 체크리스트 일곱째 줄은 per-kit 연구 기록 여섯(backend · infra · rust · react · flutter · planning)에 **이번 사이클 항목**이 있고,
연구 기록 항목마다 출처 URL 이 5 건 이상이라고 요구한다. 입력 표 FN-35 가 이것을 AR-04 로 보냈는데 AR-04 는 다섯 파일만 재고,
`url_out=0` 은 URL 을 하나도 안 적어도 통과한다. 사후 점검 `per-kit-research-logs` 는 파일이 있는지만 본다(`scripts/validate-post-kaizen.py:354-375`).

지금 여섯은 Phase 가 이미 항목을 썼다 — 이번 사이클 날짜가 든 `##` 머리가 파일마다 1 개, 사이클 기준 판(`83cfb4f`)에서는 0 개다.
Phase notes 킷 로그 단락의 URL 수는 P1 5 · P2 5 · P3 6 · P4 6 · P5 15 · P6 9 · P12 9 · P13 4 · P14 8 · P17 9 라 다섯 넘기기는 어렵지 않다.

고칠 문구 — AR-04 조건 본문 끝에 아래 두 문장을 더한다:

```text
연구 기록 셋(`docs/kaizen/research-log.md` · `flutter-research-log.md` · `docs/design/research-log.md`)은 더한 줄에 서로 다른 출처 URL 이 5 개 이상이다.
per-kit 연구 기록 여섯(`docs/{backend,infra,rust,react,flutter,planning}/research-log.md`)은 Phase 가 쓴 이번 사이클 `##` 머리를 하나씩 담는다(확인만 — 이 계약은 고치지 않는다)
```

측정 — `logs.py` 에 연구 기록 셋이면 `urls=len({clean(u) for u in URL.findall(body)})` 를 찍고 5 미만이면 `bad` 에 1 을 더한다(시작 판 셋 모두 `urls=0`).
그리고 아래 명령이 `1 1 1 1 1 1` 이다(사이클 기준 판 `83cfb4f` 에서 같은 명령은 `0 0 0 0 0 0` — 이 검토에서 돌림):

```bash
for k in backend infra rust react flutter planning; do grep -cE '^## .*2026-09-2[45]' "$T/E/docs/$k/research-log.md"; done | tr '\n' ' '
```

입력 표 FN-35 처리 칸도 「조건 AR-04 (다섯 파일 · 연구 기록 셋 URL 5 개 이상 · per-kit 여섯은 확인만)」 으로 바꾼다.

### 6. AR-07 · AR-08 — 옮긴 항목을 찾아갈 자리가 재지지 않는다

- AR-07: `audit.sh` 는 두 후속 계약 항목 번호(F1H · F1K)가 있는지만 센다. 그런데 kit 후속 notes 의 「고치지 않은 항목」 표는 `| 10 |` 같은 행 번호만 쓰고
  `F1K-10` 이라는 이름은 이 계약이 새로 붙인다. 두 notes 파일 이름이 감사 기록에 없으면 다음 사이클은 `F1K-10` 이 무엇인지 찾을 수 없다.
  이 계약이 적겠다고 한 이번 사이클 메타 이슈(개선안 11 번 · GAP 분석 「감사 기록에 적을 이번 사이클 메타 이슈」)도 재지 않는다
- AR-08: 입력 표 머리가 「`고치지 않음` 인 ID 는 notes `## 다음 사이클 메모` 와 감사 기록에 옮긴다(AR-07 · AR-08)」 라고 적었지만 `notes.sh` 는 그 소제목이 있는지만 본다

고칠 문구:

- AR-07 조건 본문 끝에 「두 후속 notes 파일 이름(`f1-harness-followups-notes.md` · `f1-kit-followups-notes.md`)과 이번 사이클 메타 이슈 넷의 파일 이름
  (`kaizen-state.yaml` · `check-insights-tracking.py` · `append-audit-log.py`) · `FN-79` · `FN-80` 이 붙은 부분에 있다」 를 더한다.
  `audit.sh` 파이썬의 `print` 앞에 아래 두 목록을 두고, 그 `print` 의 f 문자열 끝에 아래 두 값을 이어 붙여 한 줄로 찍는다. 끝 판 기대 줄 끝은 `fnotes=2/2 meta=5/5` 다(시작 판 `fnotes=0/2 meta=0/5`)

```python
FN = ["f1-harness-followups-notes.md", "f1-kit-followups-notes.md"]
MT = ["kaizen-state.yaml", "check-insights-tracking.py", "append-audit-log.py", "FN-79", "FN-80"]
# 기존 print 의 f 문자열 끝에 이어 붙인다
f" fnotes={sum(has(x) for x in FN)}/{len(FN)} meta={sum(has(x) for x in MT)}/{len(MT)}"
```

- AR-08 조건 본문에 「`## 다음 사이클 메모` 절이 입력 표에서 처리 칸이 `고치지 않음` 인 열하나(`FN-18` · `FN-39` · `FN-43` · `FN-56` · `FN-58` · `FN-64` · `FN-76` · `FN-77` ·
  `FN-78` · `FN-79` · `FN-80`)와 두 후속 notes 파일 이름을 담는다」 를 더한다. `notes.sh` 끝 `echo` 앞에 아래를 두고 끝줄 끝에 `memo=$mm/13` 을 붙인다(끝 판 기대 `memo=13/13`)

```bash
MEMO=$(awk '/^## 다음 사이클 메모$/{p=1; next} /^## /{p=0} p' "$NF")
mm=0; for x in FN-18 FN-39 FN-43 FN-56 FN-58 FN-64 FN-76 FN-77 FN-78 FN-79 FN-80 f1-harness-followups-notes.md f1-kit-followups-notes.md; do
  printf '%s\n' "$MEMO" | grep -qE -- "${x}([^0-9]|\$)" && mm=$((mm+1)); done
```

## 권고 (봉인 전에 넣으면 좋다 — 판정은 바꾸지 않는다)

아래 번호는 「권고 N」 으로 가리킨다.

1. **SK-01 (f) 와 수동 편집 JSON** — 개선안 11 번의 `--manual-edits <json>` (과 `--failures`) 경로가 정해져 있지 않다. 저장소에 두고 커밋하면 `json=14` 가 15 가 되어
   SK-01 (f) 와 AR-08 `lines=8/8` 이 함께 떨어진다. 개선안 11 번에 「JSON 은 스크래치 `$SP/final-manual-edits.json` 에 두고 커밋하지 않는다」 를 더한다
2. **DG-02 범위 밖을 이유와 함께 적기** — 이 계약이 커밋하는 QA 리포트 열아홉은 편집기 경고가 모두 648 개다(MD022 332 · MD032 309 · MD038 7).
   계약 파일 자신은 MD041 하나다. 범위 경계에 「QA 리포트는 평가자가 쓴 기록이라 글자를 고치지 않는다 — 이미 추적되는 QA 리포트 57 개와 같은 관례로 DG-02 에서 뺀다.
   계약 파일의 MD041 은 머리 설정 뒤 첫 제목이 `##` 인 계약 공통 꼴이다」 를 적는다. 개정 파일 `$AM` 과 검토 기록 `$REVIEW` 는 이 흐름이 새로 쓰는 마크다운이라 `MDS` 에 더한다
   (이 검토 파일은 같은 조건 markdownlint 로 0 건을 확인했다)
3. **AR-09 허용 경로의 `README\.md$`** — 조건 본문과 범위 경계는 루트 `README.md` 를 바꾸지 않는다고 적는데 `range.sh` 의 `ALLOW` 는 허용한다. README 를 고쳐도 `outside=0` 이다.
   `ALLOW` 에서 `|README\.md$` 를 뺀다(반드시 고칠 것 2 번을 반영하면 `docs/index.html` 은 허용에 그대로 둔다)
4. **개선안 12 번 차례** — 공통 정의는 `$AM` 에 `end_sha:` 가 없으면 `END_UNRESOLVED` 로 멈추므로 「도우미를 돌려 notes 에 옮긴 뒤 `$AM` 에 end_sha 를 적는다」 차례로는
    도우미를 공통 정의로 돌릴 수 없다. 「`$AM` 에 마지막 구현 커밋으로 `end_sha:` 를 적어 커밋 → 도우미를 돌려 notes 에 옮김 → notes · 검토 기록 커밋 → 그 sha 로 `end_sha:` 덧붙임 커밋」
    으로 바꾼다. notes 에 옮길 여덟 줄은 개정 파일 커밋에 따라 바뀌지 않는다(`synt.sh` 는 셸 · 파이썬 · JSON · YAML 만 세고 `amend.sh` 는 Phase 개정 파일만 읽는다)
5. **SK-01 (f) 「전체 `bash -n`」** — 진행 스킬 F1 은 Diagnostics 로 「전체 `bash -n` 검증」 을 적는데 (f) 는 사이클에 바뀐 셸 열여섯만 잰다. 추적되는 `.sh` 43 개를
    첫 줄 해석기대로 돌려 보니 모두 통과했다(머리 줄 없는 `env.sh` 둘은 `bash -n`). `synt.sh` 에 `all_sh=43 all_sh_bad=0` 을 더하면 싸게 맞출 수 있다
6. **ER-01 의 `verify-feedback.sh`** — `cross_diagnosis_by` 값을 재지 않는다. 사본에 `cross_diagnosis_by: bogus` 를 넣어도 `PASS` 를 낸다. 값은 `fbx.py` 의 `by=17` 만이 잰다는 것을
    「측정 해소」 줄에 적어 QA 가 `verify-feedback.sh` 통과를 그 값의 증거로 읽지 않게 한다
7. **교차 진단 기록 표 P15 · P17 행** — 교차 진단은 「측정 구멍 없음」 이라 했지만 한계 메모를 따로 남겼다. P15 는 DG-02 가 규칙별 수만 비교한다는 점(교차 진단이 줄 글자로 다시 재어 0),
    P17 은 DG-04 에서 안쪽 셸이 dash 로 한 번도 돌지 않았다는 점(결함 아님)이다. 계약 피드백 글에 한 구절씩 덧붙이면 원문과 맞는다

## 검토 관점별 요약

- **탈락 상태를 한 문장으로 쓸 수 있는가** — 26 줄 모두 쓸 수 있다. 예: SK-02 「`CLAUDE.md` 에 `10 Phase` 가 남거나 numstat 이 `3 3` 이 아니다」,
  ER-05 「목록의 가장 오래된 (전체 − 500) 개와 보관 폴더가 다르거나 목록의 나머지 하나라도 사라졌다」
- **측정이 뜻을 재는가 · 대조** — 0 기대 값은 모두 사본에서 1 이상으로 떨어지는 대조가 있거나 이 검토에서 더 돌렸다(AR-02 두 값). 뜻을 덜 재는 곳은 2 · 4 · 5 · 6 번이고,
  깨끗한 구현을 떨어뜨리는 측정은 1 · 3 번이다
- **공통 러닝북 「봉인 전에 막는 측정 구멍」** — 지킨다. 금지 경로는 `git log <기준>..<상한> -- <경로>` 로 직접 세고(AR-09 `forbidden` · SC-01 `bumped`),
  상한은 `END_UNRESOLVED` · `U=${1:?}` 로 멈추며, 셸 함수 앞에 `type … || exit 2` 가 있고, 파일마다 비교하며, 저장소 검사는 종료 코드로 잰다(`dg05.sh`).
  서명 없는 커밋은 AR-09 `unsigned` 가 따로 센다. 편집기 경고 비교는 뜻은 맞게 설계했지만 1 번 버그로 줄 글자가 틀린다
- **입력 항목** — Final 러닝북 절 · final-todo 전 항목 · 진행 스킬 F1 ~ F4 · Phase notes 넘기는 것 · 미반영 · 다음 사이클 메모 · 두 후속 notes 가 FN-01 ~ FN-80 에 있다.
  빠진 것은 F4 3 번의 per-kit 연구 기록 여섯과 URL 5 건(5 번), F2 넷째 줄의 첫 화면 갱신(2 번)이다. 미반영 여덟 행은 Phase notes 미반영 절과 맞고 처리 배정표에서 항목 이름이 겹치지 않는다
- **범위** — 쓰는 경로가 Final 러닝북 표(`.harness/` · 처리 배정표 · `docs/**/*.html` · `docs/index.html` · `docs/kaizen/` · `docs/*/research-log.md` 새 항목 · `CLAUDE.md`) 안이다.
  저장소 밖 쓰기(전역 피드백 두 칸 · 보관 폴더로 옮김)는 러닝북 「교차 진단 기록」 과 진행 스킬 F3 이 시키는 일이고, 지우지 않고 옮기는 쪽이 더 조심스럽다.
  `~/.harness` 뿌리를 통째로 훑는 저장소 코드는 없어(`collect-kaizen-data.py:55` 는 `feedback/evaluator` 만) 보관 폴더가 다시 읽히지 않는다
- **조건끼리 부딪힘** — AR-03 의 첫 화면 잠금이 F2 · F4 요구와 부딪힌다(2 번). SK-01 (f) 의 `json=14` 가 수동 편집 JSON 커밋과 부딪힐 수 있다(권고 1).
  그 밖에는 서로 맞는다 — SK-01 (f) `yaml=6` 은 이 계약이 고치는 YAML 넷과 맞고, AR-08 은 SK-01 · ER-03 도우미 출력을 그대로 담으며, ER-01 · ER-02 사본은 ER-05 이동보다 먼저 뜨고
  이동 대상(가장 오래된 139 개 안팎, 2026-04 판)에 이번 사이클 피드백 서른넷이 들지 않는다

VERDICT: CHANGES

## 2 회차

- 검토 대상: 고친 초안 `.harness/sprint-contract-kaizen-0924-final.md` (1590 줄 · 조건 26 줄 · 기능 조건 18 — Step 6.2 두 명령으로 다시 셈, 검토 시점 sha256 앞 16 자 `3e5a3fb5735ad9ab`).
  개정 파일은 아직 없다(BUILD 몫). 작업 폴더 `HEAD` `511f19b` 는 검토 전후 그대로이고, 쓴 파일은 이 검토 기록 하나다
- 측정은 스크래치 `scratchpad/kaizen/final-rv4/` 에서 돌렸다. 계약의 떼는 명령으로 도우미 스물다섯을 새로 떼고, 공통 정의는 `END` 한 줄만 바꾼 사본으로 `END=511f19b` 에서 돌렸다.
  원래 공통 정의는 개정 파일이 없어 `END_UNRESOLVED` · 종료 코드 2 로 멈춘다 — 설계대로다
- 1 회차와 달라진 도우미는 여덟(`mdcmp.sh` · `docs.py` · `logs.py` · `mem.py` · `audit.sh` · `notes.sh` · `range.sh` · `synt.sh`)과 새 `navver.py`, 공통 정의의 `MDS` 한 줄이다. 나머지 열여섯은 1 회차 사본과 바이트가 같다

### 2 회차 결론

**1 회차 고칠 것 여섯은 모두 반영됐고, 다시 돌려 확인했다.** 권고 일곱 가운데 여섯이 반영됐다. 빠진 하나(권고 2 의 「검토 기록을 `MDS` 에 넣기」)는
뺀 이유가 맞다 — 1 회차 검토 기록이 인용한 페이지 판 번호 `0.3.0` · `0.2.1` 이 react-kit · howto-kit `plugin.json` 판과 글자가 같아 AP-01 이 센다.

**새로 고칠 것 하나가 있어 CHANGES 다.** AR-06 의 `mem.py` 가 오케스트레이터 F3.5 틀 그대로 쓴 후보 파일을 떨어뜨리고, 조건 문장의 「저장소 경로이거나 `~/.harness/` 아래」 반쪽을 재지 않는다(아래 「2 회차 반드시 고칠 것」).
고칠 곳은 도우미 한 파일과 AR-06 문장 · 표 한 줄씩이라 작다.

### 1 회차 고칠 것 반영 확인

| 1 회차 번호 | 초안에 들어간 자리 | 이 검토에서 다시 돌린 결과 |
| ----------- | ------------------ | -------------------------- |
| 1 DG-02 `mdcmp.sh` | sed 식 `^[^:]*:` (`:1375`) · 경로 콜론 멈춤 (`:1371`) · 실측 표 음성 대조 | 다섯 기록 파일 첫 `##` 앞에 경고 없는 항목을 끼운 사본 → 다섯 모두 `new=0`, 같은 사본에 옛 식 → `new_total=18`. flutter 연구 기록 끝에 맨 URL · 옛 제목 → `new=2 MD024:1 MD034:1`. 콜론 든 경로 → `PATH_HAS_COLON` 종료 코드 2. 감사 기록 사본(빈 줄 하나 뒤 `render_entry` 출력 + 두 notes 이름 · 메타 절) → `new=3 MD024:3`, `NEW` 셋이 모두 도구 소제목 |
| 2 AR-03 첫 화면 · 판 번호 | 조건 본문 · `TOKENS` 끝 열넷 · `navver.py` · numstat · `my` 줄 · 범위 경계 · 개선안 6 | 시작 판 `tok_new=0/56 tok_old=9/9` · `nav_ver=0/5` · numstat 빈 출력. `docs/index.html` 안 판 번호는 `:234-238` 다섯 줄뿐이라 `5 5` 가 맞다. 원본 판 번호 다섯(`1.6.0` · `1.7.0` · `v5.1` · `v5.1` · `v5.5`)도 원본 머리 설정 · 「현재:」 줄과 같다 |
| 3 SC-01 근거 칸 | 조건 본문 · 개선안 9 | `plan.py` 는 1 회차 판 그대로(전체 경로만 읽음). 시작 판 `MISSING release-plan.md` |
| 4 AR-06 스크래치 경로 | 조건 본문 · `mem.py` `tmp_bad` · 개선안 9 | 모의 후보 파일: 근거가 저장소 notes 와 전역 피드백 절대경로 → `tmp_bad=0`, `~/.harness/…` 꼴 → `tmp_bad=0 evidence_bad=0`, 스크래치 `xdiag-all.md` → `tmp_bad=1`. 다만 새 결함이 같은 도우미에 있다(아래) |
| 5 AR-04 URL 수 · per-kit 여섯 | 조건 본문 · `logs.py` `urls` · per-kit 반복 · FN-35 | 시작 판 `files=5 bad=15` (연구 기록 셋 `urls=0`) · per-kit `1 1 1 1 1 1`, 사이클 기준 판 `0 0 0 0 0 0`. 참고로 per-kit 여섯의 이번 사이클 항목 URL 수는 7 · 14 · 10 · 16 · 8 · 9 라 F4 3 번 「최소 5 건」 도 이미 넘는다 |
| 6 AR-07 · AR-08 찾아갈 자리 | `audit.sh` `FN` · `MT` · `notes.sh` `memo` · 개선안 11 · 입력 표 머리 | 시작 판 `fnotes=0/2 meta=0/6`, 위 감사 기록 사본 → `fnotes=2/2 meta=6/6` · `head=1 generated=1 manual_orch=1`. 메타 글자를 `append-audit-log.py:148` 로 바꾼 이유가 맞다 — `render_entry` 가 `**Generated:**` 줄에 `scripts/append-audit-log.py` 를 늘 찍고, 그 스크립트 `:148` · `:159` · `:171` 이 세 고정 소제목 줄이다 |

권고 반영: 1 수동 편집 JSON 을 스크래치에(개선안 11) · 2 QA 리포트 · 계약 MD041 · 검토 기록을 범위 경계에 이유와 함께(`$AM` 은 `MDS` 에 들어가 열여덟) ·
3 `ALLOW` 에서 `README.md` 뺌 · 4 개선안 12 차례(가 ~ 라) · 5 `synt.sh` `all_sh` · 6 `verify-feedback.sh` 가 `cross_diagnosis_by` 값을 재지 않는다는 줄(`:305`) ·
7 P15 · P17 한계 메모(계약 쪽 글에 「없음」 이 그대로 들어가 `CON_TOK` 와 맞다). 개선안 12 의 「여덟 줄이 (가) · (다) · (라) 커밋으로 바뀌지 않는다」 도 다시 따져 맞다 —
`synt.sh` 는 셸 · 파이썬 · JSON · YAML 만 세고 `all_sh` 는 추적되는 셸 목록이며, `amend.sh` 의 `after` 는 Phase 서명 커밋만 센다.

### 다시 돌린 시작 판 값

모두 계약의 봉인 전 실측 표와 같다.

```text
p1hand=0 0 0 0 0 0 4 1 · parity=1 1 · apikit=1 1 1 1 1 1 1 · orch16=1 1 1 1 1
rules_old=62 rules_new=63 raised=0 added=[('K-11', ['관측 컨벤션'])]  (종료 코드 0)
tone_terms=8 other_files=119 other_terms=652 intersect=0 substring=0
sh=16 sh_bad=0 py=8 py_bad=0 json=14 json_bad=0 yaml=2 yaml_bad=0 all_sh=43 all_sh_bad=0 actionlint_rc=0
ends=1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 p1_last=0 kept=16 xfix=0 0 0 0 p1_remeasure=0 0 guides=2 after=18 after_other=1  (OTHER 76cfb37 p01-guides)
clean rc=0 values=15 why_missing=0 unexcluded=1 3 seeded=[0 rc=0 ] [0 rc=0 ] [0 rc=0 ]
evaluator files=17 by=0 marker=0 tok=0 keep=17 other_diff=0 · contract files=17 by=17 marker=0 tok=0 keep=17 other_diff=0  (전역 피드백 639 개)
done=0 status_only=0 seal_ok=19 fb_tracked=0 fb_new=0 dirty=38
rows=96 same_rows=1 phase_rows=74 phase_ok=0 miss_ok=0/8 other_note=0 non_phase_changed=0
pairs=44 exist=44 changed=0 short=7 accent=0 ext=0 hidden_up=0 tok_new=0/56 tok_old=9/9 html_added=0 html_removed=0 · nav_ver=0/5
files=5 bad=15 known_urls=350 · per-kit 1 1 1 1 1 1
state=0 phases=14 keys_ok=0 zero=0 last_updated=0 evals=[MISSING] · mem MISSING · MISSING release-plan.md
append_only=1 head=0 generated=0 manual_orch=0 f1h=0/29 f1k=0/33 new4=0/4 notes=0/17 fnotes=0/2 meta=0/6
new_total=0 · bare_open_total=0 unclosed_total=0
```

`yaml=6` 끝 판 기대도 맞다 — 사이클 동안 바뀐 YAML 둘은 `.github/workflows/ci.yml` · `silent-check.yaml` 이고, 이 계약이 고치는 넷(`cleanup-log.yaml` · `kaizen-failure-count.yaml` · `kaizen-state.yaml` · `stale-values.yaml`)은 그 둘에 없다.
기능 조건 18 · 조건 줄 26 · 절 헤더 배치도 Step 6.2 · 6.5 명령으로 다시 세어 같다.

### 2 회차 반드시 고칠 것 — AR-06 `mem.py`

두 곳이다. 한 도우미 안이라 한 번에 고친다.

(가) **따옴표 없는 시각을 떨어뜨린다.** 오케스트레이터 F3.5 틀은 `generated_at: <ISO8601+TZ>` 를 따옴표 없이 보인다. 그대로 `generated_at: 2026-09-25T20:00:00+09:00` 로 쓰면
PyYAML 이 `datetime` 으로 읽고, `str()` 이 `2026-09-25 20:00:00+09:00`(날짜와 시각 사이가 빈칸)을 내서, 그 자리에 `T` 를 요구하는 `mem.py` 정규식이 맞지 않는다. 나머지가 다 맞는 모의 파일에서 재 보니 `parse=0` 이다.
따옴표를 치면 `parse=1` 이다. 조건 문장은 「시간대 붙은 `generated_at`」 만 요구하므로 틀을 글자대로 따른 깨끗한 구현이 AR-06 에서 떨어진다 — 1 회차 3 번(SC-01 근거 칸)과 같은 종류다.

(나) **조건 문장의 반쪽을 재지 않는다.** AR-06 문장은 「`source_evidence` 경로는 … 저장소 경로이거나 `~/.harness/` 아래다」 인데 `tmp_bad` 는 `/private/tmp` · `/tmp` 만 거른다.
`~/.claude/…` 같은 다른 절대경로를 적어도 끝줄이 기대 꼴 그대로다(모의 파일로 확인). 1 회차 4 번 문구를 그렇게 쓴 것은 이 검토였다 — 측정이 문장을 다 재게 맞춘다.

고칠 문구 — `mem.py` 를 아래처럼 바꾼다(스크래치 사본 `final-rv4/mem-fix2.py` 로 돌려 봄):

```python
# 머리 주석 끝에 한 줄
#  out_bad   — 절대경로인데 ~/.harness/ 아래가 아닌 수 (0 — 조건은 저장소 경로이거나 ~/.harness/ 아래만 허용한다)
# import 줄
import datetime, os, re, sys, yaml
# parse 계산 앞에 두 줄 — 따옴표 없는 시각은 yaml 이 datetime 으로 읽어 str() 이 가운데를 빈칸으로 바꾼다
ga = d.get("generated_at") if isinstance(d, dict) else None
ga = ga.isoformat() if isinstance(ga, datetime.datetime) else str(ga or "")
# parse 식의 끝 인자 str(d.get("generated_at", "")) 를 ga 로 바꾼다
parse = int(isinstance(d, dict) and body.startswith("# kaizen-memory-candidates") and d.get("cycle_id") == "kaizen-2026-09-24"
            and bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?[+-]\d{2}:\d{2}", ga)))
# 반복 앞
ev_bad = tmp_bad = out_bad = 0
# tmp_bad 두 줄 바로 뒤
        if os.path.isabs(p) and not p.startswith(os.path.expanduser("~/.harness/")):
            out_bad += 1; print("NG 저장소 · ~/.harness 밖 경로", p)
# 마지막 print 의 끝
      f"actionability_bad={a_bad} evidence_bad={ev_bad} need={need}/{len(NEED)} tmp_bad={tmp_bad} out_bad={out_bad}")
```

그리고

- AR-06 측정의 기대 줄 끝을 `need=2/2 tmp_bad=0 out_bad=0` 으로, 봉인 전 실측 표 AR-06 행의 끝 판 기대도 같게 바꾼다
- 같은 표 AR-06 행 양성 · 음성 대조 칸에 아래를 더한다(이 검토에서 고친 사본으로 돌린 값)

```text
generated_at 따옴표 없이 2026-09-25T20:00:00+09:00 → parse=1 (고치기 전 식은 parse=0) · 시간대 없는 2026-09-25T20:00:00 → parse=0 · 끝이 Z → parse=1
근거 경로 ~/.harness/feedback/evaluator/… 와 그 절대경로 → tmp_bad=0 out_bad=0 · $HOME/.claude/CLAUDE.md → out_bad=1 · 스크래치 xdiag-all.md → tmp_bad=1 out_bad=1
```

### 2 회차 권고 (판정은 바꾸지 않는다)

1. **AR-03 판 번호 넷은 원본 본문에도 있다.** `TOKENS` 판 번호 열넷 가운데 `contract-design-guide` `v5.1`(원본 본문 1 번) · `qa-evaluation-guide` `v5.1`(3 번) · `contract-schema` `v5.5`(9 번) ·
   `plugin-validation` `1.4.0`(1 번)은 원본 머리 설정 밖 본문에도 나온다. 그래서 페이지 `<title>` · 뱃지에 옛 판이 남아도 본문만 옮기면 `tok_new` 가 통과한다.
   조건 문장(「새 판 번호를 본문에 담는다」)과 측정은 서로 맞으니 결함은 아니다. 좁히려면 harness 다섯 페이지는 지금 `<title>` 에 판 번호가 있으므로 아래 줄을 AR-03 에 더한다.
   시작 판 `title_ver=0/5`, `skill-design-guide` 제목만 고친 사본 `1/5`, 거기에 `contract-design-guide` 본문에만 `v5.1` 을 더한 사본도 `1/5` (이 검토에서 돌림)

   ```python
   # titlever.py <판 폴더> — harness 다섯 페이지 <title> 이 원본 판 번호를 담는지 센다
   import re, sys
   W = {"skill-design-guide": "1.6.0", "agent-design-guide": "1.7.0", "contract-design-guide": "v5.1",
        "qa-evaluation-guide": "v5.1", "contract-schema": "v5.5"}
   def title(p):
       m = re.search(r"<title>([^<]*)</title>", open(p, encoding="utf-8").read())
       return m.group(1) if m else ""
   ok = sum(1 for p, v in W.items() if v in title(f"{sys.argv[1]}/docs/harness/{p}.html"))
   print(f"title_ver={ok}/{len(W)}")
   ```

2. **조건끼리 부딪힘을 더 찾았지만 없었다** — 적어 두면 QA 가 같은 확인을 되풀이하지 않는다.
   - AP-01 ↔ AR-04: Phase · followups notes 열아홉의 changelog · 킷 로그 · 넘기는 것 절 381 줄에 킷 `plugin.json` 판 열하나(`0.1.0` · `0.2.1` · `0.3.0` 등)가 0 번 나온다.
     다섯 기록 파일 머리 설정 판(`1.6.0` · `1.5.0` · `1.4.0` · `1.3.0` · `1.3.0`)을 올린 값도 킷 판과 겹치지 않는다
   - ER-04 ↔ AR-04: Phase 8 changelog 단락에 옛 값 `1.7+ native state encryption` 이 있지만, `check-stale-values.py` 의 `SOURCE_DIRS` 는 `docs/kaizen/` · `docs/design/` 를 훑지 않아 `clean rc=0` 과 부딪히지 않는다
   - DG-05 ↔ ER-05: 사후 점검 날짜 검사는 사이클 날짜와 **오늘**을 함께 인정한다(`validate-post-kaizen.py:197`). 정리 기록 `date` 가 2026-09-25 여도 `cycle: "kaizen-2026-09-24"` 로 통과한다
   - DG-02 ↔ AR-07: 감사 기록 사본에서 새 묶음은 도구 소제목 MD024 셋뿐이었다(위 표 1 번)

VERDICT: CHANGES
