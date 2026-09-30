# cx 기록 — Codex 최종 점검이 찾은 조용한 통과 결함 10

계약 `.harness/sprint-contract-after-0929-codex-silent-pass.md` (봉인 `sha256:29a945b036808430` · 측정 `sha256:82260932be2d56a1`,
봉인 커밋 `1817e16c`, 측정 묶음 커밋 `9fb9618a`). 근거는 `codex-final.md` 의 결함 1 ~ 10.

봉인 전에 교차 진단 지적 둘과 notes 경로 하나를 계약에 반영했다.

- 스크립트-13 양성 대조의 「기존 두 명령 · 새 한 명령 `1 1 0`」 이 무엇인지 흐려 인자 셋을 적었다 (다시 재어 `1 1 0`)
- 스크립트-14 (b) 의 옛 로컬 CI 도구가 git 이 추적하지 않는 파일이라는 점(`remaining.md` D2)을 범위 경계에 적었다
- 계약 초안은 notes 를 `$M/cx-notes.md` 로 두었는데 작업 지시가 이 파일 경로를 정해 구조-03 을 이 경로로 맞췄다

## 항목별 결과

| 결함 | 커밋 | 한 것 |
| --- | --- | --- |
| 1 `detect-docs-drift.py` | `2dc309c2` | git 실패를 `GitError` 로 올려 종료 코드 2. 시험 경우 4 추가 |
| 2 `sync-evals.py` | `2dc309c2` | 깨진 `evals.json` 을 SKIP 하지 않고 2. 새 시험 `scripts/test-sync-evals.py` |
| 3 `ci-local.sh` | `2dc309c2` | 돌린 run 단계 0 개(못 다룬 단계도 0 개)면 실행 · `--list` 모두 2. 못 다룬 단계만 있으면 지금처럼 1. 시험 경우 셋 추가 |
| 4 `check-install-docs-guidance.py` | `2dc309c2` | 못 읽은 파일을 `UNREADABLE <경로> (<까닭>)` 로 적고 2. NUL 바이트가 든 바이너리만 건너뛴다. 새 시험 |
| 5 `check-superseded.sh` | `fa524386` | `fm_get` 실패를 따로 받아 `UNREADABLE` 줄 · 2. 못 읽은 파일마다 한 줄 (가리킨 새 판이면 `UNREADABLE <계약> -> <새 판>`). 시험 경우 둘 추가 |
| 6 `run-evals.py` | `2dc309c2` | eval 항목 0 개면 경로를 적고 2. 새 시험 |
| 7 `check-docs-a11y.js` | `2dc309c2` | 잴 HTML 0 개(또는 `docs/` 없음)면 브라우저를 띄우기 전에 2. 새 시험 |
| 8 `run-gate-fixtures.sh` | `3985e1c5` | 표 행 · 실행 줄 중복을 `불일치 <이름> — … 중복 <n> 줄` 로. 새 시험 |
| 9 lint 훅 (레포 밖) | 아래 고친 줄 | grep · rg 로 시작하는 백틱 명령은 따옴표 안 검색 글만 산문인지 잰다. 시험 `fa524386` · `4e0d7937` |
| 10 qa 훅 (레포 밖) | 아래 고친 줄 | 판정이 `APPROVE` 가 아니면(빈 파일 · 판정 줄 없음 포함) 안내에 넣는다. 시험 `fa524386` |
| 종료 코드 표 | `fa524386` | `harness/evals/gate-exit-codes.md` 의 `check-docs-a11y.js` 행 `0 · 1 · 2` |
| CI 등록 | `eecdd1be` | 새 시험 다섯을 단계로 더했다 (지운 줄 0) |

## 레포 밖 훅의 고친 줄

`~/.claude/hooks/lint-contract-oracle.sh` (고친 뒤 지문 `ebe26e2aa1e0ef6a`, 고치기 전 `f00b60e16f87135c`):

```diff
+  # grep · rg 명령을 한 백틱에 통째로 적으면 명령이라 건너뛰어 검색 글의 산문을 놓친다 (2026-09-29 Codex 점검).
+  # 따옴표 안 글만 잰다 — 경로에 든 한글은 검색 글이 아니다
+  function quoted_prose(t,   s, re) {
+    s = t
+    re = "\"[^\"]*\"|\047[^\047]*\047"
+    while (match(s, re)) {
+      if (is_prose(substr(s, RSTART + 1, RLENGTH - 2))) return 1
+      s = substr(s, RSTART + RLENGTH)
+    }
+    return 0
+  }
-      if (is_command(t)) continue
+      if (is_command(t)) {
+        if (t ~ /^(grep|rg) / && quoted_prose(t)) { prose = 1; break }
+        continue
+      }
```

`~/.claude/hooks/qa-pending-check.sh` (고친 뒤 지문 `07c427c14a16523e`, 고치기 전 `b18721b2ab224706`):

```diff
+    APPROVE) ;;
+    # 빈 파일이나 판정 줄이 없는 결과 파일을 완료로 치면 평가가 중간에 죽은 것을 놓친다 (2026-09-29 Codex 점검)
+    *)
+      pending="${pending}- ${name}: ${feedback} 에 Verdict: 판정 줄이 없음"$'\n'
+      continue ;;
```

QA 1 회차 뒤 독립 검토가 찾은 결함(`quoted_prose()` 안 `match()` 가 `RSTART` · `RLENGTH` 를 덮어 다음 조건 번호가 비고
그 조건이 검사에서 빠짐)을 고친 줄 (지금 지문 `182ed51390abd4ae`):

```diff
-    flush(); id = substr($0, RSTART + 6, RLENGTH - 6); buf = $0; next
+    # flush() 안의 match() 가 RSTART · RLENGTH 를 덮으므로 번호를 먼저 잘라 둔다.
+    nid = substr($0, RSTART + 6, RLENGTH - 6)
+    flush(); id = nid; buf = $0; next
```

## 훅 시험 출력 끝 줄

`bash harness/evals/hooks/lint-contract-oracle-test.sh` 와 `bash harness/evals/hooks/qa-pending-check-test.sh` 둘 다 끝 줄이 같다.

```text
실패 0 건
```

음성 대조: 고치기 전 사본으로 lint 시험은 `실패 6 건` · 종료 코드 1, qa 시험은 `실패 2 건` · 종료 코드 1. 없는 훅 경로는 2.
명령 백틱 건너뛰기를 통째로 지운 lint 사본은 `경로에만한글` 두 로캘에서 `스킬-05 (산문-grep)` 을 내 떨어진다.

## 자기 측정 (TIP `4e0d7937`)

- 스크립트-01 ~ 10: `repro.sh` 42 줄에서 조건이 적은 줄 전부 1 건씩. `d8 dup-row rc=1 dup=1` · `d8 dup-run rc=1 dup=1`
- 스크립트-11: TIP 여덟 모두 0 (`경우 4 개 중 통과 4` · ci-local `PASS` 9 · superseded `PASS` 5, `FAIL` 0). BASE 도구로 여덟 모두 1
- 스크립트-12: 두 시험 0, `LC_ALL=C` 1 · `en_US.UTF-8` 2 · `SK-` 4 · `스킬-` 8, 고치기 전 사본 1 · 1, 없는 훅 2
- 스크립트-13: `grep -cF` 여덟 모두 1, 단계 세기 `1 1 1 1 1 1 1 1`, 접근성 시험 작업 `['playwright']`, 지운 줄 0
- 스크립트-14: (a) `steps=50 run=45 skip=5 unsupported=0 failed=0` · 종료 코드 0 · `FAIL` 0, CI 전용 단계 모두 `PASS`
  (b) 옛 도구 `summary.txt` 26 줄 중 `rc=0` 아닌 줄은 `feedback-agg-test SKIP (yq 없음)` 하나
  (c) `here 결과: 28 경우 중 불일치 0 rc=0` · `noslicer 결과: 28 경우 중 불일치 0 · 건너뜀 20 rc=0 left_paths=0`
- 오류-01: `1 · 0 · 1 · 1 · 2 · 1 · 1`
- 구조-01: 병합 0 · BAD 0 · 커밋 8 (이 기록 커밋 포함). 구조-02: 범위 밖 0 · tail 파일과 `docs/` 0
- 재사용-01 `0` · `1`, 재사용-02 두 파일 `:0`
- 진단-02: shellcheck 0 · py_compile 0 · `node --check` 0 · markdownlint-cli2 0.23.2 `Linting: 1 file` · `Summary: 0 issues in 0 files`
- 금지-03 · 금지-04: `validate-plugin.py` 종료 코드 0

## tone-guide 1 · 5 단계

1 단계에서 `tone-kit:tone-guide` 를 불러 코어 규칙표(C · N · S · 안티패턴 A ~ J · 한국어 K)를 읽었다. 프로젝트 오버레이
`.claude/tone-project.md` 는 어댑터 없음 · 주석 한국어.

| 규칙 | 판정 |
| --- | --- |
| C-01 · C-07 | 새 주석은 모두 까닭 한 줄 ~ 두 줄 (예: 명령 치환이 `fm_get` 실패 코드를 버리는 까닭) |
| A · B · F | 이름 번역 주석 · 틀 표지 · 구분선 0 |
| N-08 (SHOULD) | awk 함수 안 `s` · `re` 는 같은 파일의 `c` · `t` · `m` 관례를 따랐다 (C-08 · S-12 관측 컨벤션) |
| S-04 · S-05 | 넘기기만 하는 래퍼 0. 시험 파일은 기존 시험(`test-detect-docs-drift.py` · `test-ci-local.sh`)의 틀을 따랐다 |
| K-02 · K-03 | 번역투 없음, 주체와 결과를 적었다 |

## 킷 판 번호 판단

- harness: `scripts/check-superseded.sh` 는 설치본에도 실리는 스크립트라 종료 코드가 바뀐 것은 patch 한 단계가 맞다. 시험 · 표만 바뀐 것은 판 번호와 무관
- bambu-kit: `evals/` 만 바뀌어 설치본 동작은 같다 — 올리지 않아도 된다. 같이 릴리스한다면 patch
- `scripts/` · `.github/` 는 킷이 아니라 판 번호가 없다
- 계약 범위 경계대로 여기서는 올리지 않았다. 합친 뒤 main 에서 한다

## 남은 것

- QA 판정은 하지 않았다 (지시) — `harness:qa-evaluator` 가 이 계약으로 판정할 차례
- 범위 밖 같은 모양 결함 셋 (계약 범위 경계에 적은 것): `run-evals.py` 가 없는 킷 이름을 받아도 `SKIP` 으로 0,
  `evals.json` 이 없는 킷을 이름으로 받아도 0, `sync-evals.py` · `run-evals.py` 가 `OSError` 를 잡지 않는다. Codex 목록 밖이라 손대지 않았다
- 훅 시험 둘은 CI 에 없다 — 훅이 레포 밖(`~/.claude/hooks/`)이라 CI 러너에서 준비 실패 2 가 된다. 이 맥에서만 돈다
- 옛 로컬 CI 도구(`.harness/handoff/2026-09-26-tools/ci-local.sh`)는 여전히 git 밖이다 (`remaining.md` D2)
- `remaining.md` 의 B2 · B5 · B7 · B9 는 교차 진단이 코드로 확인한 결과 이미 고쳐진 낡은 항목이다
- `check-install-docs-guidance.py` 는 NUL 바이트가 없는데 UTF-8 이 아닌 킷 파일을 이제 못 읽음 2 로 본다 — 지금 레포에는 0 개(실측)

## QA 1 회차 뒤 독립 검토 결함 (2 차 수정)

| 결함 | 커밋 | 한 것 |
| --- | --- | --- |
| 막음 — lint 훅 번호 잃음 | `90e08acf` | 훅은 부모 세션이 고쳤다 (위 diff). `lint-contract-oracle-test.sh` 에 `앞조건따옴표grep` 경우를 두 로캘로 더했다. 지금 훅 `실패 0 건` · 0, 번호를 잃던 판 `실패 2 건` · 1, 고치기 전 판 `실패 6 건` · 1 |
| `check-superseded.sh` 중복 세기 | `90e08acf` | 폴더 인자 끝 빗금을 떼고, 같은 못 읽는 새 판은 한 번만 센다. 시험 경우 E(옛 판 둘 → 새 판 하나) · F(끝 빗금) 추가. 옛 판으로 돌리면 E · F 만 FAIL · 1 |
| `check-install-docs-guidance.py` 지운 파일 | `8dca3e73` | 정책: 추적 중인데 작업 폴더에서 지운 파일은 `SKIP <경로> (작업 폴더에서 지워짐)` 줄만 내고 실패로 치지 않는다. 커밋 전 삭제는 흔한 상태이고 다음 커밋에서 빠질 파일이라 잴 글이 없다. 권한 · 인코딩으로 못 읽는 파일은 그대로 `UNREADABLE` · 2. 시험 경우 3 추가, 옛 판은 경우 3 에서 2 로 FAIL |
| `sprint-contract/SKILL.md` 안내 | 안 함 | `harness/skills/sprint-contract/SKILL.md` 는 봉인된 범위 목록 밖이다. 고치면 구조-02 가 깨지고, 범위를 넓히는 개정은 조건을 느슨하게 한다 — 사용자 동의가 필요하다 |
