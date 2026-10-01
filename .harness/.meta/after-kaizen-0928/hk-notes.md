# hk 묶음 기록 — 레포 밖 훅 둘을 harness 플러그인 훅으로

- 계약: `.harness/sprint-contract-after-1001-hooks-into-harness.md` (봉인 커밋 `1c905f28`, 측정 도우미 `abe6c8b9` · 지문 `32eeb4f07489fd12`)
- 가지 `chore/ak3-hk`, 시작 판 `b33ed94a`. push · 합치기 · 릴리스는 하지 않았다.
- 근거: 2026-10-01T03:36:45.449Z 질문 도구 답에서 사용자가 「harness 플러그인 훅으로」 를 골랐다(세션 bda55d45 기록 8527 번째 줄). 부모가 03:38:37Z 에 모든 설치본에서 훅이 새로 돈다는 것과 0.18.0 계획을 알렸고, 04:32:13Z 「ㄱㄱ」 로 진행했다. `decisions.md` 에 같은 내용을 적었다(`51214b03`).

## 항목별 결과

| 항목 | 결과 | 커밋 |
| --- | --- | --- |
| 옮기기 · 등록 | 두 훅과 `_lib-hook-payload.sh` 를 `harness/scripts/` 로 옮기고 `harness/hooks/hooks.json` 에 PostToolUse(`Edit\|Write`) · Stop 두 등록을 더했다. 훅은 제 옆 도우미를 기본으로 찾는다. 훅 시험 둘은 새 자리를 보고, 플러그인 훅 시험을 새로 두었다. README 에 `## 플러그인 훅` 절 | `67ef1cdb` |
| 겹침 검사 | 설치본 맞대기를 지우고 `scripts/check-user-hook-overlap.py`(개인 설정이 같은 훅을 또 등록했는지)와 그 시험 일곱 경우로 바꿨다. 훅 표의 세로 막대가 표 칸을 가르지 않게 `sync-docs.py` 를 고쳤다 | `34daabd8` |
| CI | 옛 두 단계를 새 셋으로 바꿨다 | `9843ee06` |
| 다듬기 | 플러그인 훅 시험의 shellcheck 알림, 계약 오라클 훅 주석의 설치본에 없는 docs 경로, 훅 시험의 도우미 확인 자리 | `90ce2043` · `08372f7a` · `d38318d5` |

## 자기 측정 (W, TMPDIR 은 scratch 아래, `npm ci` 뒤)

- 스크립트-01 `new_found=2 base_kept=1 base_regs=5 regs=7 personal=same ok=1` · 스크립트-02 `runs=2 pass=2 base_rc=1 noquote_rc=1 homelib_rc=1 ok=1` · 스크립트-03 `runs=4 pass=4 stub_rcs=1,1 lib_exports=0 ok=1`
- 스크립트-04 (`--plugin-dir` 실제 claude) `plugin_ok=1 lint=1 stop=1 errors=0 base_lint=0 base_stop=0 ok=1` · 진단-04 `errors=0 ok=1`
- 스크립트-05 알려진 답 둘(`settings.json` 의 Stop · PostToolUse) · `home_rc=1` · `ok=1` · 스크립트-06 `tail=[경우 7 개 중 통과 7] stub_fails=3,4,5,6,7 ok=1` · 스크립트-07 `base_runs=56 runs=57 new_once=1 old_gone=1 kept=1 ok=1`
- 스크립트-08 도커 `ubuntu:24.04` `results=5 good=5 mawk=1 gnu_grep=1 ok=1` · 스크립트-09 `rows=7 rows_ok=1 prose_miss=[] mdl=0 pos_md056=1 ok=1`
- 오류-01 `cases=8 right=8 ok=1` · 오류-02 `same=1 commit_guard_rc=0 ok=1` · 구조-02 `files=17 extra=[] lack=[] ok=1` · 구조-03 `files=3 right=3 v8_rc=0 ok=1` · 구조-05 `version_files_changed=[] ok=1` · 재사용-02 `lib_users=2 new_dirs=[] ok=1`
- 로컬 CI `steps=57 run=52 skip=5 unsupported=0 failed=1` — `FAIL` 줄은 `User hook overlap check` 하나. 이 맥 개인 설정이 아직 두 훅을 등록해 두어 그 겹침을 알린 것이다(진단-05 의 F=1). CI 파일에만 있는 열 단계 모두 0 (`npx playwright test` 174 passed)
- `.py` 셋 `py_compile` 0, `.sh` 여섯 `bash -n` 0 · `shellcheck` 0 줄, `jq empty` 0, `validate-plugin.py --check=code-fence` 0

## tone-guide

- 1 단계: 오버레이 `.claude/tone-project.md`(어댑터 없음 · 주석 한국어)와 코어 규칙 표(`core-comment.md` · `core-naming.md` · `core-structure.md` · `core-antipatterns.md` · `locale-korean.md`)를 레포 판으로 읽었다. 걸리는 규칙은 C-01 · C-04 · C-07 · C-15 · H(보존) · N-08 · N-09 · S-04 · S-07 · K-03.
- 5 단계: 더한 줄에서 구분선 · 템플릿 표시 · fallback 이름 · 새 한 글자 이름 · 무역할 파일 이름 0 건. 새 주석은 까닭을 적은 줄(다른 사람 기계에는 `~/.claude/hooks/` 가 없다 · 따옴표가 빠지면 경로가 쪼개진다 · 세로 막대가 표 칸을 가른다)이고, 옮긴 세 파일의 옛 까닭 주석은 지우지 않았다.

## 킷 버전 판단

harness 는 minor 로 올린다(0.17.1 → 0.18.0). harness 를 설치한 모든 사람에게 Stop · PostToolUse 훅 둘이 새로 돌기 시작하므로 동작이 늘어난 변경이다. 이 묶음은 `plugin.json` · `marketplace.json` 을 바꾸지 않았다(구조-05).

## 부모가 할 일 (이 계약 밖)

1. PR · CI · 합치기 뒤 harness 0.18.0 릴리스, 이 맥 설치본 갱신.
2. `~/.claude/settings.json` 의 두 등록과 `~/.claude/hooks/` 의 두 훅 파일을 백업한 뒤 지운다. 그 뒤 `python3 scripts/check-user-hook-overlap.py` 가 `겹침 없음` · 0 이 되는지 본다.
3. `~/.claude/hooks/_lib-hook-payload.sh` 는 지우지 않는다 — 개인 훅 `block-dirwide-autofixer.sh` · `parallel-session-guard.sh` 가 계속 그 사본을 불러 쓴다.
4. `~/.claude/CLAUDE.md` 의 `~/.claude/hooks/qa-pending-check.sh` 언급을 harness 플러그인 훅으로 고친다.

## 남긴 것

- push · PR · 릴리스와 위 개인 설정 정리는 부모 몫이다.
- 앞 fin 묶음 계약의 측정 가운데 옛 자리 세 파일 · 맞대기 검사 · 「hooks.json 에 세 이름 없음」 은 이번 결정으로 일부러 뒤집혔다. 그 계약은 이미 `done` 이라 다시 재지 않는다.
- 개인 설정을 지우기 전까지 로컬 CI 의 겹침 단계는 1 로 알린다. 지우면 0 이 된다.

## QA 와 독립 검토 (2026-10-01)

- qa-evaluator 2 회차 APPROVE — 26 조건 중 통과 23 · 해당 없음 3 · 실패 0. 보고서와 계약 `done` 표시는 `6beb342a`.
- 독립 검토 막는 결함 0, 막지 않는 지적 셋을 이렇게 처리했다.
  1. README 가 플러그인에 없는 `scripts/check-user-hook-overlap.py` 를 가리킴 — 고쳤다(`ee3a9ad4`). 도구가 레포 맨 위에 있다고 밝히고, 개인 설정에서 지울 줄을 직접 적었다. 스크립트-09 다시 재서 `ok=1`.
  2. 근거 결정이 `decisions.md` 에 없음 — 세션 기록에서 03:36:45Z 답을 찾아 적었다(`51214b03`). 위 「근거」 줄도 바로잡았다.
  3. 도우미 두 벌(`~/.claude/hooks/_lib-hook-payload.sh` · `harness/scripts/_lib-hook-payload.sh`)을 맞대는 검사가 없어짐 — 고치지 않고 남긴다. 아래 「남긴 것」 참고.

## 남긴 것 (QA 뒤)

- 도우미 두 벌 맞대기 검사를 다시 두지 않는다. 이제 레포 본은 플러그인 훅 둘만, 홈 사본은 개인 훅(`block-dirwide-autofixer.sh` · `parallel-session-guard.sh`)만 불러 쓴다. 서로 갈라져도 어느 훅도 깨지지 않고, 맞대기를 다시 두면 이 계약이 일부러 지운 검사(재사용-02 · 「도우미는 레포에 하나」)를 되살리는 일이 된다. 홈 사본을 레포 본과 같게 두고 싶으면 개인 훅 정리 때 손으로 맞춘다.
- harness 를 설치한 모든 사람에게 훅 둘이 새로 도는 것은 위 03:36:45Z 답으로 동의를 받았다. 릴리스 전에 다시 물을지는 부모가 정한다.
