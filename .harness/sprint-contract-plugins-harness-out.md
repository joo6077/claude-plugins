---
feature: "claude-plugins 의 .harness 를 저장소에서 빼고 하네스 저장소로 — 원격 검사가 .harness 없이 돈다"
slug: plugins-harness-out
created: "2026-10-09 21:06"
complexity: "중간"
conditions: 16
status: active
owner_session: c0c0aae7-8201-45fd-b1e1-338ea412ed57
conditions_digest: sha256:f94bcfdbbc01cc3f
measurement_digest: sha256:8813c88157f8d3ac
locked_at: "2026-10-10 11:06"
---

## 배경

- 2026-10-09 사용자 결정: 모든 프로젝트의 하네스 기록은 하네스 저장소(`~/Hub/10_Dev/harness-store`)에 두고 프로젝트 저장소에는 넣지 않는다. 사용자 지시 「claude-plugins · flutter_playwright 옮기기 ㄱㄱ」.
- 이 저장소는 `.harness` 아래 1199 개를 추적 중이다. 원격 검사가 그 안을 읽어 그냥 빼면 깨진다.

## GAP 분석

봉인 전 실측(2026-10-09, `origin/main` 판 사본에서 `.harness` 를 지우고 원격 검사 명령을 돌림):

| 명령(`.github/workflows/ci.yml` 행) | `.harness` 있을 때 | 없을 때 | 원인 |
| --- | --- | --- | --- |
| `python3 scripts/check-stale-values.py` (85) | 0 | 1 | 설정 목록 `.harness/stale-values.yaml` 을 읽는다(`scripts/check-stale-values.py:41`) |
| `python3 scripts/test-collect-kaizen-data.py` (132) | 0 | 1 | `.harness` 와 무관 — 시험 사례 「없으면 Hub 만」 이 Hub 폴더 `b/c` 를 쓰는데, 사본 폴더 이름이 `c` 라 수집기의 「이 레포와 같은 이름 빼기」 에 걸렸다. 사본 폴더 이름에 따라 결과가 갈린다 |
| `bash harness/scripts/check-superseded.sh .harness` (273-274) | 0 | 2 | 잴 폴더가 없다 |
| `bash harness/evals/superseded/check-superseded-test.sh` (271) · `python3 scripts/validate-plugin.py` | 0 | 0 | — |

`stale-values.yaml` 은 하네스 기록이 아니라 문서 검사 설정이다 — 저장소 안 `scripts/` 로 옮긴다. 저장소 계약을 더는 저장소에 두지 않으니 274 행 단계는 잴 대상이 없어 뺀다(271 행의 검사기 자체 시험은 남는다).

## 범위 경계

- `.harness/.meta` 를 쓰는 로컬 도구(`scripts/append-audit-log.py` · `scripts/finalize-phase.sh` · 카이젠 데이터 풀 출력)는 고치지 않는다 — 로컬에서는 `.harness` 바로가기를 따라 하네스 저장소에 쓴다. 원격 검사는 이것들을 돌리지 않는다.
- 로컬 옮기기(본 작업 폴더 `~/Hub/10_Dev/claude-plugins` 의 `.harness` 를 하네스 저장소 `claude-plugins` 폴더로 복사 · 바로가기, 다른 작업 폴더 16 곳의 고유 기록 복사)는 이 저장소 밖 작업이라 조건이 아니다. 다른 세션이 쓰는 작업 폴더는 지우지 않는다.
- flutter_playwright 는 별도 계약이다.
- 다른 작업 폴더(`.claude/worktrees/` 16 곳)가 이 추적 해제를 받으면 그 폴더의 추적 `.harness` 파일이 지워진다. 그 전에 고유 기록을 하네스 저장소로 옮긴다(로컬 작업, 조건 아님).
- 이 가지를 원격에 올리고 PR 을 만드는 것까지 이 스프린트다(구조-02). 병합은 사용자 결정 뒤.
- 커밋 순서: (1) 봉인 커밋 (2) `scripts/` · `.github/` 수정 커밋 — 새 `scripts/stale-values.yaml` 추가 포함 (3) 추적 해제 커밋 — `.harness/` 삭제와 `.gitignore` 만.

```text
# sprint-scope
.harness/
.gitignore
.github/workflows/ci.yml
scripts/check-stale-values.py
scripts/stale-values.yaml
scripts/test-collect-kaizen-data.py
```

## Skill

- [ ] 스킬-00: N/A (스킬 파일을 바꾸지 않는다 — 원격 검사 설정 · 검사 스크립트 · 설정 목록 위치만 바뀐다)

## Script

- [ ] 스크립트-01: Given 이 가지의 판을 `.harness` 가 없는 사본으로 받았을 때, When `python3 scripts/check-stale-values.py` 를 돌리면, Then 종료 0 이고 설정 목록을 `scripts/stale-values.yaml` 에서 읽으며(내용은 옛 `.harness/stale-values.yaml` 과 같다), 그 스크립트 안 설명 · 안내 글에도 `.harness` 가 남지 않는다 [exact]
  측정: `git clone --shared` 사본 · `rm -rf .harness` 뒤 실행해 종료 코드; `git show befe2d0a:.harness/stale-values.yaml` 과 `scripts/stale-values.yaml` 을 `cmp`; `grep -c '\.harness' scripts/check-stale-values.py` 가 0 (기준값 3)
  음성 대조: `scripts/stale-values.yaml` 을 지운 사본에서 0 이 아닌 종료 코드
- [ ] 스크립트-02: Given 같은 사본, When `python3 scripts/test-collect-kaizen-data.py` 를 사본 폴더 이름을 `c` 로 두고 돌리면, Then 종료 0 · 끝 줄 `0 실패` 다(시험 결과가 사본 폴더 이름에 따라 갈리지 않는다) [exact]
  측정: 사본을 `<임시>/c` 에 만들고 실행, 끝 줄과 종료 코드
  음성 대조: 시작점 `befe2d0a` 의 시험 파일로 바꾼 사본에서 같은 방법으로 돌리면 `FAIL 하네스 저장소 — 없으면 Hub 만` 이 나온다. 고치는 방법은 시험 사례의 Hub 폴더 이름을 레포 폴더 이름과 겹칠 수 없는 이름(`b/deep`)으로 바꾸는 것이다
- [ ] 스크립트-03: 원격 검사 설정에서 레포 `.harness` 를 재는 단계(`check-superseded.sh .harness`)가 없어지고, 검사기 자체 시험(`check-superseded-test.sh`) 단계는 남는다 [exact, enumerated]
  측정: `grep -c 'check-superseded.sh .harness' .github/workflows/ci.yml` 이 0 (기준값 1) · `grep -c 'check-superseded-test.sh' .github/workflows/ci.yml` 이 1 (기준값 1)

## Error

- [ ] 오류-00: N/A (새 오류 경로가 없다 — 설정 목록 위치만 바뀐다. 목록이 없을 때의 동작은 기존 그대로이며 스크립트-01 음성 대조가 잰다)

## Architecture

- [ ] 구조-01: Given 이 계약의 마지막 커밋 뒤, Then 저장소가 `.harness` 아래 파일을 하나도 추적하지 않고(`git ls-files -- .harness` 0 줄, 기준값 1199), 레포 루트 `.gitignore` 파일 안에 루트 폴더만 막는 `/.harness` 줄이 있으며 `git check-ignore -q --no-index .harness` 가 종료 0 이다 [exact]
  측정: `git ls-files -- .harness | wc -l` · `grep -qxF '/.harness' .gitignore` · `git check-ignore -q --no-index .harness` — 판은 이 가지 끝(`git rev-parse chore/plugins-harness-out`)
- [ ] 구조-02: Given 이 가지를 원격에 올려 만든 PR, Then 원격 검사 셋(`Plugin Validation` · `Harness Integration Tests` · `Playwright Visual Tests`)이 모두 통과한다 [exact, enumerated]
  측정: `gh pr checks <PR 번호>` 세 줄이 `pass`
- [ ] 구조-03: 추적 해제는 커밋 하나이고, 그 커밋에 `.harness/` 밖 경로는 `.gitignore` 하나뿐이며 그 커밋의 `.harness/` 변경은 전부 삭제다 [exact]
  측정: `git log --diff-filter=D --format=%h befe2d0a..chore/plugins-harness-out -- .harness` 가 정확히 한 줄(여러 줄이면 FAIL). 그 커밋의 `git show --name-status --format=` 에서 `.harness/` 로 시작하지 않는 줄이 `M	.gitignore` 하나, `.harness/` 줄은 전부 `D`

## Anti-patterns

- [ ] 금지-02: force push 금지 — 원격 가지 `chore/plugins-harness-out` 의 기록이 한 번도 되쓰이지 않는다
  측정: 올릴 때마다 직전 원격 끝 해시가 새 끝의 조상이다(`git merge-base --is-ancestor <직전> <새 끝>` 종료 0). 리포트에 올린 차례마다 두 해시를 적는다
- [ ] 금지-03: bare code fence 금지 — `python3 scripts/validate-plugin.py --check=code-fence` 종료 0

## Reusability

- [ ] 재사용-01: N/A (재사용 단위 코드를 새로 만들지 않는다 — 설정 파일 위치 · 원격 검사 단계 · 시험 이름만 바꾼다)
- [ ] 재사용-02: N/A (같은 이유)

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze 는 `bash -n scripts/release.sh` 만 잰다 — 이번 범위에 없다. 대신 `python3 -m py_compile scripts/check-stale-values.py scripts/test-collect-kaizen-data.py` 종료 0)
- [ ] 진단-02: N/A (편집기 진단을 읽을 수단이 없다 — 대신 진단-01 의 py_compile)
- [ ] 진단-03: N/A (commands.test 도 scripts/release.sh 만 돈다 — 대신 스크립트-01 · 02 와 구조-02)
- [ ] 진단-04: N/A (구동할 앱 · 서버 없음 — 원격 검사가 구조-02 에서 실제로 돈다)
