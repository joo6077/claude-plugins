---
feature: "조건 번호 정규식을 리눅스에서도 돌게"
slug: after-0930-id-regex-linux
created: "2026-09-30 16:25"
complexity: "복잡"
conditions: 19
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: "sha256:64997021d92aa203"
measurement_digest: "sha256:4dc48dd81154a963"
locked_at: "2026-09-30 16:44"
---

## 배경

- 묶음 rx. PR #123 CI 의 Harness Integration Tests 가 실패했다. 우분투 CI 의 GNU grep 은 C.UTF-8 로캘에서 한글 범위식 `[가-힣]` 을 「Invalid collation character」 로 거부해, 조건 번호 정규식 `([A-Z]{2,}|[가-힣]+)-[0-9]{2}` 가 0 건을 낸다. `harness/evals/measure/measure-helpers-test.sh` 의 `M-bash` · `M-zsh` · `K1` 둘 · `K2` 가 실패하고 봉인 지문이 빈 입력 값 `e3b0c44298fc1c14` 가 된다. 리눅스에서는 모든 계약의 봉인 확인이 깨진다.
- 고칠 것: 조건 번호를 읽는 식의 한국어 몫 `[가-힣]+` 를 로캘과 무관한 `[^ -~]+`(출력 가능한 ASCII 가 아닌 글자) 로, awk 모양 `([A-Z][A-Z]+|[가-힣]+)` 도 `([A-Z][A-Z]+|[^ -~]+)` 로 바꾼다. 규약 문서의 식 설명에 「한글 범위식은 로캘마다 뜻이 달라 쓰지 않는다」 까닭을 한 줄 적는다. 시험에 「C.UTF-8 에서 한국어 번호를 읽는다」 경우를 더한다.
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-rx`, 가지 `chore/ak3-rx`, 시작 판 `BASE` = `bbcb43d8` (가지 `chore/after-kaizen-0928` 끝). 사용자 위임: 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 · 2026-09-28 「약점과 일부만 한 거 다처리하지??」(세션 bda55d45-296c-491f-89ba-b52042d58e72). 남은 일 목록 · 결정 파일은 통합 폴더 `.harness/.meta/after-kaizen-0928/remaining.md` · `decisions.md` (읽기만).
- 사용자가 할 일: 없음.

공통 전제 G (조건마다 되풀이하지 않는다) — 구현 · 기록 커밋이 가지 `chore/ak3-rx` 에 모두 들어가고, W 의 HEAD 가 그 가지 끝이며, `git -C W status --porcelain -- . ':(exclude).harness' ':(exclude)node_modules'` 가 빈 출력이다. W 맨 위 폴더에서 잰다. 측정 도우미 `m <조건 번호>` 는 `python3 harness/scripts/extract-helpers.py --sealed .harness/sprint-contract-after-0930-id-regex-linux.md <scratch 폴더>` 로 뗀 `m.sh` 를 `TMPDIR=<scratch 아래 폴더> bash <scratch 폴더>/m.sh <조건 번호>` 로 부르는 것이다(종료 코드 0 성립 · 1 불성립 · 2 잴 수 없음). 리눅스 쪽은 `docker run --rm ubuntu:24.04` 에 `LC_ALL=C.UTF-8` 을 주고 `apt-get install -y zsh git python3` 뒤 돈다 — 이 이미지에는 zsh · git · python3 이 없고, CI 의 `ubuntu-latest` 는 zsh 만 따로 넣는다(`.github/workflows/ci.yml` 「Install zsh」 단계). 브라우저 측정은 본 레포 `node_modules` 의 playwright 를 쓴다. 진단-05 전에 W 에 `node_modules` 가 있어야 한다(본 레포 것을 가리키는 바로가기 또는 `npm ci`).

## GAP 분석 (Pre-Edit Audit)

| 대상 파일 | 실제 Read 증거 | 발견한 갭 | 조건 |
| --- | --- | --- | --- |
| `harness/references/contract-schema.md` | :300 식 설명 · :333 `contract_digest` · :346 `measurement_digest` awk · :543 · :926 · :1518 | 한글 범위식 7 곳. `measure-common.sh` 가 이 파일의 함수 블록을 그대로 읽어 쓰므로(사본 0 — 시험 `M3`), 여기를 고치면 측정 도우미도 같이 고쳐진다 | 스킬-01 · 스킬-02 · 스크립트-01 ~ 03 |
| `harness/skills/sprint-contract/SKILL.md` | :313 · :703 · :713 · :730 · :768 · :777 | 6 곳 (봉인 확인 · 조건 수 · 기능 조건 수 · 게이트 · 봉인) | 스킬-01 |
| `harness/agents/qa-evaluator.md` | :517 · :592 | 2 곳 | 스킬-01 |
| `harness/docs/guides/qa-evaluation-guide.md` | :766 | 1 곳 | 스킬-01 |
| `docs/harness/contract-schema.html` | :515 · :564 · :577 · :776 · :1103 · :1363 · :1600 (:577 한 줄에 둘) | 8 곳, 원본과 짝(`scripts/detect-docs-drift.py --since bbcb43d8` 이 원본 둘 → 쪽 둘 짝을 낸다) | 구조-01 |
| `docs/harness/qa-evaluation-guide.html` | :823 | 1 곳 | 구조-01 |
| `harness/evals/measure/measure-helpers-test.sh` | :123 ~ :138 `K1` · `K2` | 로캘을 못박은 경우가 없어 맥에서는 옛 식도 통과한다(맥 BSD grep 은 C · C.UTF-8 · en_US.UTF-8 · ko_KR.UTF-8 모두 4 건) | 스크립트-01 · 02 |
| `git grep -l '가-힣'` (`.harness/` 밖) | 12 파일 | 조건 번호용은 위 여섯. 나머지 여섯(react-kit · tone-kit 쪽 한국어 글자 찾기 식)은 다른 용도라 그대로 둔다. `.harness/` 안은 봉인된 계약 · 앞 묶음 도우미의 한국어 글자 세기 식이라 손대지 않는다 | 구조-02 |

- 양면 조건: 식을 정하는 쪽은 규약 문서(스킬-01 · 스킬-02), 받아 쓰는 쪽은 스킬 · 평가자 · 평가 가이드(스킬-01) · 측정 공용 파일과 그 시험(스크립트-01 · 02) · 문서 쪽(구조-01) · 이미 봉인된 계약 149 개(스크립트-03)다.
- 복잡도 4 축: 레이어 — 규약 · 스킬 · 에이전트 · 시험 · 문서 쪽(예) / 공개 규약 변경 — 조건 번호 식(예) / 받아 쓰는 쪽 — 스킬 · 평가자 · 측정 공용 파일 · 봉인된 계약(예) / 회귀 위험 — 봉인 지문이 바뀌면 149 계약이 `SEAL_BROKEN` (예). 네 축 모두 예 → 복잡.
- 설정 대조: `commands.analyze` = `bash -n scripts/release.sh` · `commands.test` = `bash scripts/release.sh 2>&1 || true` (둘 다 이번 변경 파일과 무관 → 진단-01 · 03 N/A) · `diagnostics.ide_exclude` = `[]` · 카테고리 `Skill`/`스킬` · `Script`/`스크립트` · `Error`/`오류` · `Architecture`/`구조` · 금지 패턴 `금지-01` ~ `금지-04` (`금지-01` 버전 하드코딩은 버전을 건드리지 않아 뺀다).

## Skill

- [ ] 스킬-01: 규약 문서 · 스킬 · 평가자 · 평가 가이드 네 파일의 조건 번호 식이 로캘과 무관한 모양으로 바뀐다 — 파일마다 `grep -oF '가-힣'` 수가 0 이고, 조건 번호 식 안의 새 조각 `|[^ -~]+)-[0-9]` 수가 `harness/references/contract-schema.md` 7 · `harness/skills/sprint-contract/SKILL.md` 6 · `harness/agents/qa-evaluator.md` 2 · `harness/docs/guides/qa-evaluation-guide.md` 1 이다. Given 공통 전제 G, When `m 스킬-01`, Then 네 줄 모두 `hangul_range=0 new_piece=<수> want=<같은 수>` · `counts_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스킬-01`. 시작 판(W) 실측 `hangul_range` 7 · 6 · 2 · 1, `new_piece` 0 · 0 · 0 · 0, 종료 코드 1
  음성 대조: 한 파일이라도 식을 안 바꾸면 그 줄이 `hangul_range` 1 이상 · `new_piece` 부족으로 종료 코드 1
- [ ] 스킬-02: 규약 문서의 식 설명에 까닭이 한 줄 있다 — `harness/references/contract-schema.md` 에 「한글 범위식은 로캘마다 뜻이 달라 쓰지 않는다」 가 정확히 한 줄이고, 그 줄이 「조건 열거 정규식은」 이 처음 나오는 줄 바로 아래 1 ~ 3 줄 안에 있다. Given 공통 전제 G, When `m 스킬-02`, Then `reason_lines=1 after_rule_line=+<1~3>` · 종료 코드 0 [exact]
  측정: `m 스킬-02`. 시작 판 실측 `reason_lines=0` · 종료 코드 1

## Script

- [ ] 스크립트-01: 맥에서 측정 시험이 실패 0 이고, 새 경우 「C.UTF-8 에서 한국어 번호를 읽는다」 가 옛 식을 잡는다 — `harness/evals/measure/measure-helpers-test.sh` 에 이름이 `K3-C.UTF-8한국어번호` 인 경우가 있어 로캘을 `LC_ALL=C.UTF-8` 로 못박고 한국어 번호 계약의 두 지문(`8b52386c713a6054 c51d48673b5caeee`) · 조건 수 7 을 재고, 규약의 두 식(`contract_digest` 의 grep 식 · `measurement_digest` 의 awk 식)에 ASCII 밖 바이트가 든 줄이 0 이어야 통과한다. 맥에서 시험이 종료 코드 0 · 끝 줄 `실패 0 건` · `PASS K3-C.UTF-8한국어번호` 한 줄이고, CI 의 Harness Integration Tests 가 이 시험을 부르는 단계(빈칸 8 개 들여쓴 `run: bash harness/evals/measure/measure-helpers-test.sh` 한 줄 전체)가 `.github/workflows/ci.yml` 에 정확히 1 개다. Given 공통 전제 G, When `m 스크립트-01`, Then `mac_rc=0 mac_fails= k3_pass=1 last=[실패 0 건] neg_rc=1 neg_fails=[K3-C.UTF-8한국어번호] ci_step=1` · 종료 코드 0 [exact]
  측정: `m 스크립트-01` — 도우미가 가지 끝을 `git clone --shared` 로 떠서 규약 문서만 시작 판(`bbcb43d8`)으로 되돌린 사본에서도 시험을 돌린다
  음성 대조: 옛 규약 문서 사본에서 맥 시험이 종료 코드 1 이고 실패는 `K3-C.UTF-8한국어번호` 하나다(봉인 전 사본 실측 `non_ascii_lines=2`). 시작 판 실측 `k3_pass=0 neg_rc=0` · 종료 코드 1
- [ ] 스크립트-02: 리눅스에서 측정 시험이 실패 0 이다 — `docker run --rm ubuntu:24.04`(`LC_ALL=C.UTF-8`, `apt-get install -y zsh git python3`)에서 `bash harness/evals/measure/measure-helpers-test.sh` 가 종료 코드 0 · 끝 줄 `실패 0 건` · `PASS K3-C.UTF-8한국어번호` 한 줄이다. Given 공통 전제 G · 도커 사용 가능, When `m 스크립트-02`, Then `linux_rc=0 linux_fails=[] k3_pass=1 last=[실패 0 건] neg_rc=1 neg_fails=[K1-한국어번호지문-bash,K1-한국어번호지문-zsh,K2-한국어번호조건수,K3-C.UTF-8한국어번호,M-bash,M-zsh]` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-02`. 시작 판(W) 실측 `linux_rc=1 linux_fails=[K1-한국어번호지문-bash,K1-한국어번호지문-zsh,K2-한국어번호조건수,M-bash,M-zsh]` · `실패 5 건` · 종료 코드 1 (PR #123 CI 와 같은 다섯)
  음성 대조: 규약 문서만 시작 판으로 되돌린 사본은 도커에서 종료 코드 1 · 실패 여섯(위 `neg_fails`) — 봉인 전 사본 실측 `실패 6 건`
- [ ] 스크립트-03: 이미 봉인된 계약 149 개의 두 지문이 그대로다 — 시작 판 `bbcb43d8` 이 추적하는 `.harness/sprint-contract-*.md` 149 개를 그 판 글로 꺼내, 맥에서 옛 규약 함수로 낸 조건 지문 · 측정 지문과 ① 맥에서 새 규약 함수로 낸 값 ② 리눅스 도커(`LC_ALL=C.UTF-8`, mawk)에서 새 규약 함수로 낸 값이 한 줄도 다르지 않고, ② 는 오류 출력 0 줄이다. 양성 대조로 리눅스에서 옛 규약 함수로 낸 값은 맥 옛 값과 1 줄 이상 다르다. Given 공통 전제 G · 도커 사용 가능, When `m 스크립트-03`, Then `contracts=149 rows=149 mac_old_vs_mac_new=0 mac_old_vs_linux_new=0 linux_new_err=0 control_mac_old_vs_linux_old=<1 이상>` · 종료 코드 0 [exact]
  측정: `m 스크립트-03`. 시작 판(W, 새 규약 = 옛 규약) 실측 `mac_old_vs_linux_new=294 linux_new_err=149 control_mac_old_vs_linux_old=294` · 종료 코드 1. 구현 뒤 모양 사본 실측 `0 0 0 294`
  양성 대조: `control_mac_old_vs_linux_old` — 같은 비교가 차이를 잡을 수 있음을 매번 보인다

## Error

- [ ] 오류-01: 조건 번호가 아닌 줄은 세지 않는다(알려진 답) — 줄 여섯 `- [ ] SK-01: a` · `- [x] 스킬-02: b` · `- [ ] 구조-11: c` · `- [ ] 2026-09 날짜` · `- [ ] foo-12 소문자` · `- [ ] ER-03: d` 에 규약 문서에서 꺼낸 grep 식 · awk 식을 돌리면 맥(`LC_ALL` = `C` · `C.UTF-8` · `en_US.UTF-8`, grep · awk)과 리눅스 도커(`C` · `C.UTF-8`, GNU grep · mawk) 열 경우 모두 4 다. Given 공통 전제 G · 도커 사용 가능, When `m 오류-01`, Then `mac=4,4,4,4,4,4 linux=4,4,4,4` · 종료 코드 0 [exact, enumerated]
  측정: `m 오류-01` — 식은 글자로 적지 않고 규약 문서 `contract_digest` · `measurement_digest` 정의에서 꺼낸다
  알려진 답: 조건 번호 줄 넷(SK-01 · 스킬-02 · 구조-11 · ER-03), 기대 4. 시작 판 실측 `linux=4,4,grep: Invalid collation character,4` · 종료 코드 1, 구현 뒤 모양 사본 실측 `mac=4,4,4,4,4,4 linux=4,4,4,4` · 종료 코드 0

## Architecture

- [ ] 구조-01: 문서 쪽 둘이 원본과 같이 바뀐다 — `docs/harness/contract-schema.html` 8 · `docs/harness/qa-evaluation-guide.html` 1 곳에서 `가-힣` 이 0 개 · `|[^ -~]+)-[0-9]` 조각이 그 수이고, `docs/harness/contract-schema.html` 에 「한글 범위식은 로캘마다 뜻이 달라 쓰지 않는다」 가 정확히 한 줄 · `<li>` 로 시작하며 「조건 열거 정규식은」 이 처음 나오는 줄 바로 다음 줄이다. 두 쪽이 320 · 375 · 1280 폭에서 가로 넘침 0(6 경우)이고 `python3 scripts/check-docs-common-css.py` 가 종료 코드 0 이다. Given 공통 전제 G, When `m 구조-01`, Then `counts_ok=1` · `reason_lines=1 reason_li=1 after_rule_line=+1 cases=6 overflow=0 css_rc=0` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-01`. 시작 판 실측 `counts_ok=0 reason_lines=0 cases=6 overflow=0 css_rc=0` · 종료 코드 1
  양성 대조: 넘침 측정은 `<div style="width:2000px">` 를 끼운 사본에서 `overflow=3` 을 냈다(봉인 전 실측)
- [ ] 구조-02: 다른 용도의 한국어 글자 찾기 식은 그대로다 — `git grep -l '가-힣' chore/ak3-rx -- . ':(exclude).harness'` 가 정확히 여섯 파일 `docs/react-kit/build-audit.html` · `docs/react/kit-design/g6-build-audit.md` · `docs/tone-kit/antipattern-catalog.html` · `docs/tone/antipattern-catalog.md` · `react-kit/agents/react-reviewer.md` · `react-kit/skills/react-audit/SKILL.md` 이고, `git diff --name-only bbcb43d8 chore/ak3-rx -- <그 여섯> react-kit tone-kit docs/react docs/react-kit docs/tone docs/tone-kit` 가 0 줄이다. Given 공통 전제 G, When `m 구조-02`, Then `left=[<여섯 파일, LC_ALL=C 정렬>] changed_kept=0` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-02`. 시작 판 실측 `left` 12 파일(위 여섯 + 조건 번호용 여섯) · 종료 코드 1
- [ ] 구조-03: 커밋 규칙 — `bbcb43d8..chore/ak3-rx` 에 합침 커밋이 0 이고, 커밋이 3 개 이상이며, 커밋마다 맨 위 폴더가 하나(`docs` 는 `docs/<폴더>` 로 센다)이고, 바뀐 파일이 모두 `## 범위 경계` 의 `# sprint-scope` 목록 또는 `.harness/` 안이며, 서명 줄(`git log -1 --format='%(trailers:key=Co-Authored-By,valueonly)'`)이 `Claude … <noreply@anthropic.com>` 모양이다. Given 공통 전제 G, When `m 구조-03`, Then 커밋마다 `OK` · `commits=<3 이상> merges=0 bad=0` · 종료 코드 0 [exact]
  측정: `m 구조-03`. 구현 뒤 모양 사본(봉인 · harness · docs/harness 세 커밋) 실측 `commits=3 merges=0 bad=0`

## Anti-patterns

- [ ] 금지-02: force push 금지 (측정: 이 스프린트는 push 하지 않는다 — `git reflog show chore/ak3-rx` 에 `forced-update` 0 줄)
- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (측정: `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0, 그리고 진단-02 의 markdownlint 경고 0 — MD040 포함)
- [ ] 금지-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL (측정: `python3 scripts/validate-plugin.py harness --check=frontmatter` 종료 코드 0. 시작 판 종료 코드 0)

## Reusability

- [ ] 재사용-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 (측정: 새 코드는 기존 시험 파일 안의 경우 하나뿐이고, 그 시험은 CI 에 등록돼 있다 — 스크립트-01 `ci_step=1`. 식은 규약 문서 한 곳에 있고 공용 측정 파일이 그것을 읽는다 — 시험 `M3-규약과같음` 이 스크립트-01 · 02 에서 PASS)
- [ ] 재사용-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 (측정: 새 파일을 만들지 않고 기존 `harness/evals/measure/measure-helpers-test.sh` 에 경우를 더한다 — `git diff --name-status bbcb43d8..chore/ak3-rx -- . ':(exclude).harness'` 에 `A` 로 시작하는 줄 0)

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: git diff --name-only bbcb43d8..chore/ak3-rx | grep -c '^scripts/release.sh$' 이 0)
- [ ] 진단-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — 바뀐 `.md` 네 파일(`harness/references/contract-schema.md` · `harness/skills/sprint-contract/SKILL.md` · `harness/agents/qa-evaluator.md` · `harness/docs/guides/qa-evaluation-guide.md`)은 markdownlint-cli2(MD013 끔)로 경고 합계 0, 바뀐 셸 시험 `harness/evals/measure/measure-helpers-test.sh` 은 `shellcheck` 지적 0 · `bash -n` 종료 코드 0. Given 공통 전제 G, When `m 진단-02`, Then `md_warnings=0 shellcheck=0 bash_n_rc=0` · 종료 코드 0 [exact, enumerated]
  측정: `m 진단-02`. 시작 판 · 구현 뒤 모양 사본 모두 경고 0 · 지적 0
  양성 대조: 같은 설정으로 빈 줄 없는 목록 · 언어 없는 울타리를 넣은 파일에 경고 3 건(MD031 · MD032 · MD040)이 나왔다(봉인 전 실측)
- [ ] 진단-03: N/A (commands.test 대상도 scripts/release.sh 라 이번 변경 파일에 없다. 측정: 진단-01 과 같은 명령)
- [ ] 진단-04: N/A (구동할 앱 · 서버가 없다 — 산출물은 규약 · 스킬 · 에이전트 · 가이드 문서 · 셸 시험 · 문서 쪽. 측정: git diff --name-only bbcb43d8..chore/ak3-rx -- . ':(exclude).harness' | grep -cvE '^(harness/(references|skills|agents|docs|evals)/|docs/harness/)' 이 0)
- [ ] 진단-05: 로컬 CI 와 CI 파일에만 있는 단계가 모두 통과한다 — `bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh <W>`(TMPDIR 은 scratch 아래)의 단계가 모두 `rc=0`(yq 없는 `feedback-agg-test SKIP` 만 예외) · 25 단계 이상 · `docs-a11y` 로그 끝 `206/206 PASS` 이고, `python3 scripts/check-api-kit-docs.py` · `python3 scripts/test-check-api-kit-docs.py` · `python3 scripts/detect-docs-drift.py --check-table` · `python3 scripts/test-detect-docs-drift.py` · `python3 scripts/check-docs-common-css.py` · `python3 scripts/check-cause-table-copies.py` · `python3 scripts/test-check-cause-table-copies.py` · `bash harness/evals/measure/measure-helpers-test.sh` · `bash bambu-kit/evals/run-gate-fixtures.sh` · `bash bambu-kit/evals/makerworld-fetch-test.sh` · `bash bambu-kit/evals/run-gate-fixtures-test.sh` · `npx playwright test api-kit/evals/` 의 종료 코드가 모두 0 이다. Given 공통 전제 G · W 에 `node_modules`, When `m 진단-05`, Then `local_rc0=<local_lines - skip> skip<=1 a11y=[206/206 PASS] ci_only_failed=[]` · 종료 코드 0 [exact, enumerated]
  측정: `m 진단-05`. 시작 판 사본 · 구현 뒤 모양 사본 모두 ci-local 25 단계 `rc=0` · SKIP 1 · `206/206 PASS` · CI 전용 명령 모두 종료 코드 0 (`npx playwright test` 는 ci-local 이 `design-kit/evals/visuals.spec.js` 162 passed, 여기서 `api-kit/evals/` 12 passed)

## 범위 경계

- 이 계약이 고칠 경로는 아래 블록뿐이다. `.harness/` 아래(이 계약 · QA 리포트)는 늘 허용된다.

```text
# sprint-scope
harness/references/contract-schema.md
harness/skills/sprint-contract/SKILL.md
harness/agents/qa-evaluator.md
harness/docs/guides/qa-evaluation-guide.md
harness/evals/measure/measure-helpers-test.sh
docs/harness/contract-schema.html
docs/harness/qa-evaluation-guide.html
```

- 하지 않는 것: react-kit · tone-kit 의 한국어 글자 찾기 식(구조-02 여섯 파일), `.harness/` 아래 봉인된 계약 · QA 리포트 · 개정 파일과 앞 묶음 측정 도우미(`.harness/.meta/…`)의 한국어 글자 세기 식, `harness/scripts/measure-common.sh`(규약 블록을 읽어 쓰므로 고칠 글자가 없다), `.github/workflows/ci.yml`(시험 단계 · zsh 설치 단계가 이미 있다), 킷 버전 올리기 · 릴리스 · 합치기 · push, 레포 밖 `ci-local.sh`.
- 커밋: `git add <경로>` 뒤 `git commit -o <경로>`. `git add -A` · `git stash` · push · 가지 바꾸기 금지. 메시지 한국어, 끝에 빈 줄 뒤 서명 줄 「Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>」. 한 커밋에 맨 위 폴더 하나 — `harness/` 다섯 파일 한 커밋, `docs/harness` 두 쪽 한 커밋, 봉인 커밋(계약 파일 하나)은 따로.
- 교차 대조(봉인 전): 바뀌는 글자(`가-힣` · 조건 번호 식) · 파일을 읽는 기존 검사를 `scripts/` · `.github/` · `harness/scripts/` · `harness/evals/` 에서 `grep` 으로 찾았다 — 식 글자를 직접 읽는 검사는 없다(`git grep -nE '가-힣|\[A-Z\]\{2,\}' -- scripts .github harness/scripts harness/evals` 0 줄). 파일을 읽는 것은 `harness/scripts/measure-common.sh`(규약 함수 블록 — 스크립트-01 · 02 가 잰다) · `scripts/detect-docs-drift.py`(원본 → 쪽 짝 둘 — 구조-01 이 두 쪽을 같이 고친다) · `scripts/check-reviewer-protocol-copies.py`(평가 가이드 두 덩어리 사본) · `scripts/check-install-docs-guidance.py` · `scripts/validate-plugin.py` 다. 구현 뒤 모양 사본(여섯 파일 식 바꿈 + 설명 두 줄 + `K3`)에서 ci-local 25 단계와 진단-05 의 CI 전용 명령이 모두 종료 코드 0 이었다. 「더하라」 조건(스킬-01 · 02 · 스크립트-01 · 구조-01)과 「그대로」 조건(스크립트-03 · 구조-02 · 진단-05)이 함께 겨누는 파일은 `harness/references/contract-schema.md`(식을 바꾸되 봉인 지문은 그대로)와 `harness/evals/measure/measure-helpers-test.sh`(경우를 더하되 기존 경우는 통과) 둘이고, 같은 사본에서 두 쪽이 모두 성립해 부딪히지 않는다. CI 전용 단계와 범위 목록을 맞대면 범위 밖 파일을 고쳐야 하는 경우는 없다.
- 커버리지 해소: 스킬-01 · 구조-01 — 파일 이름과 기대 수는 도우미 `MD_FILES` · `PAGE_FILES` 에 글자 그대로 있다. 구조-02 — 여섯 파일은 도우미 `KEEP_FILES` 에 있다. 진단-05 — 명령 열둘은 조건 줄과 도우미 `CMDS` 에 같은 글자로 있다. 진단-02 — `.md` 네 파일은 도우미 `MD_FILES`, 셸 시험은 `TEST` 에 글자 그대로 있다(`.md` 는 확장자 낱말이라 경로가 아니다).
- 오라클 해소: 스크립트-01 · 02 — 글자 찾기가 아니라 시험을 맥 · 리눅스에서 실제로 돌리고, 옛 규약 사본으로 음성 대조한다. 스크립트-03 — 149 계약에 규약 함수를 실제로 돌린 지문을 맞댄다. 오류-01 — 식을 규약 문서에서 꺼내 알려진 답 입력에 열 경우로 돌린다.

## 회귀 게이트 — 측정 도우미 · 봉인 전 실측

- 도우미 `m.sh` 는 아래 블록이다. `python3 harness/scripts/extract-helpers.py --sealed <이 계약> <폴더>` 가 바이트 그대로 뗀다.
- 봉인 전 실측(2026-09-30, W 시작 판 `bbcb43d8`): 스킬-01 · 스킬-02 · 스크립트-01 · 스크립트-02 · 스크립트-03 · 오류-01 · 구조-01 · 구조-02 종료 코드 1(결함 재현), 구조-03 은 범위 목록을 읽을 계약이 아직 없어 종료 코드 2. 값은 각 조건 측정 줄에 있다.
- 봉인 전 사본 대조(구현 뒤 모양 scratch 사본 — `git clone --shared` 뒤 여섯 파일 식 바꿈 · 설명 두 줄 · 시험 `K3` 를 폴더별 서명 커밋에 담음): 위 측정이 모두 종료 코드 0 이었다. 값은 아래 `사본 실측` 줄에 적는다.
- 사본 실측(2026-09-30, 구현 뒤 모양 사본 · 세 커밋): 스킬-01 `counts_ok=1` · 스킬-02 `reason_lines=1 after_rule_line=+2` · 스크립트-01 `mac_rc=0 k3_pass=1 last=[실패 0 건] neg_rc=1 neg_fails=[K3-C.UTF-8한국어번호] ci_step=1` · 스크립트-02 `linux_rc=0 linux_fails=[] k3_pass=1 neg_rc=1` 실패 여섯 · 스크립트-03 `contracts=149 rows=149 0 0 0 294` · 오류-01 `mac=4,4,4,4,4,4 linux=4,4,4,4` · 구조-01 `counts_ok=1 reason_li=1 after_rule_line=+1 cases=6 overflow=0 css_rc=0` · 구조-02 여섯 파일 · `changed_kept=0` · 구조-03 `commits=3 merges=0 bad=0` · 진단-02 `md_warnings=0 shellcheck=0 bash_n_rc=0` · 진단-05 `local_rc0=25 local_lines=26 skip=1 a11y=[206/206 PASS] ci_only_failed=[]` — 모두 종료 코드 0. 금지-03 · 금지-04 의 validate-plugin 은 같은 사본에서 종료 코드 0(ci-local `validate-plugin` 단계 포함).
- 교차 진단 반영(2026-09-30): 사본 실측 기록 파일 `scratchpad/rx-c/copy-run.txt` 는 스킬-01 · 진단-02 에서 네 파일 중 두 줄만 담겨 불완전했다. 교차 진단이 같은 사본에서 다시 재어 네 줄과 위 값을 확인했으므로, 사본 실측의 근거는 그 기록 파일이 아니라 이 줄에 적은 재측정이다. 진단-05 는 교차 진단이 다시 재지 못했다 — 구현 뒤 실제 가지에서 `m 진단-05` 를 반드시 돌려 값을 기록에 남긴다.
- 도우미가 쓰는 레포 밖 경로: 본 레포 `node_modules/playwright/index.mjs`(구조-01) · scratch `mdl/node_modules/.bin/markdownlint-cli2`(0.23.2 계열, 진단-02) · `.harness/handoff/2026-09-26-tools/ci-local.sh`(진단-05). 없으면 그 조건은 종료 코드 2(잴 수 없음)다.

```bash
#!/usr/bin/env bash
# m.sh <조건 번호> — 계약 after-0930-id-regex-linux 의 조건 하나를 잰다. 종료 코드 0 성립 · 1 불성립 · 2 잴 수 없음
# 레포 맨 위 폴더(W)에서 부른다. 도커 이미지 ubuntu:24.04 와 본 레포 node_modules 의 playwright 를 쓴다
set -u
BASE=bbcb43d8
BR=chore/ak3-rx
CONTRACT=.harness/sprint-contract-after-0930-id-regex-linux.md
SCHEMA=harness/references/contract-schema.md
TEST=harness/evals/measure/measure-helpers-test.sh
PW=/Users/jackson/Hub/10_Dev/claude-plugins/node_modules/playwright/index.mjs
IMG=ubuntu:24.04
ML=/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/mdl/node_modules/.bin/markdownlint-cli2
CI_LOCAL=/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh
REASON='한글 범위식은 로캘마다 뜻이 달라 쓰지 않는다'
MD_FILES="harness/references/contract-schema.md:7 harness/skills/sprint-contract/SKILL.md:6 harness/agents/qa-evaluator.md:2 harness/docs/guides/qa-evaluation-guide.md:1"
PAGE_FILES="docs/harness/contract-schema.html:8 docs/harness/qa-evaluation-guide.html:1"
KEEP_FILES="docs/react-kit/build-audit.html docs/react/kit-design/g6-build-audit.md docs/tone-kit/antipattern-catalog.html docs/tone/antipattern-catalog.md react-kit/agents/react-reviewer.md react-kit/skills/react-audit/SKILL.md"

root=$(git rev-parse --show-toplevel 2>/dev/null) || { echo "레포 밖이다" >&2; exit 2; }
cd "$root" || exit 2
t=$(mktemp -d "${TMPDIR:-/tmp}/rx-m.XXXXXX") || exit 2
trap 'rm -rf "$t"' EXIT

need_docker() { docker info >/dev/null 2>&1 || { echo "도커가 없어 리눅스 쪽을 못 잰다" >&2; exit 2; }; }
verdict() { if [ "$1" = 1 ]; then echo "ok=1"; exit 0; else echo "ok=0"; exit 1; fi; }

# 파일마다 한글 범위식 수와 새 식 조각 수. 새 식 조각은 조건 번호 식 안의 모양으로만 센다
counts() {  # counts "<파일:기대 수> ..."
  good=1
  for pair in $1; do
    f=${pair%%:*}; want=${pair##*:}
    [ -f "$f" ] || { echo "$f 없음"; good=0; continue; }
    old=$(grep -oF '가-힣' "$f" | wc -l | tr -d ' ')
    new=$(grep -oF '|[^ -~]+)-[0-9]' "$f" | wc -l | tr -d ' ')
    echo "$f hangul_range=$old new_piece=$new want=$want"
    [ "$old" = 0 ] && [ "$new" = "$want" ] || good=0
  done
  echo "counts_ok=$good"
}

# 사본 하나를 가지 끝에서 만들고 규약 문서만 시작 판으로 되돌린다 (음성 대조용)
neg_copy() {
  git clone -q --shared "$root" "$t/neg" && git -C "$t/neg" checkout -q "$BR" 2>/dev/null \
    && git -C "$t/neg" show "$BASE:$SCHEMA" >"$t/neg/$SCHEMA" || { echo "사본을 못 만들었다" >&2; exit 2; }
}
fail_names() { grep '^FAIL ' "$1" | awk '{print $2}' | LC_ALL=C sort | tr '\n' ',' | sed 's/,$//'; }

# 계약마다 조건 지문 · 측정 지문을 낸다. $1 규약 파일 · $2 계약 폴더
cat >"$t/dig.sh" <<'EOF'
awk '/^```bash$/ { f = 1; buf = ""; next } f && /^```$/ { if (buf ~ /(fm_get|sha256_16|sprint_head|mine)\(\) \{/) printf "%s", buf; f = 0; next } f { buf = buf $0 "\n" }' "$1" >"${TMPDIR:-/tmp}/fns.$$.sh"
. "${TMPDIR:-/tmp}/fns.$$.sh"
find "$2" -maxdepth 1 -type f -name 'sprint-contract-*.md' | LC_ALL=C sort | while read -r f; do
  printf '%s %s %s\n' "${f##*/}" "$(contract_digest "$f")" "$(measurement_digest "$f")"
done
rm -f "${TMPDIR:-/tmp}/fns.$$.sh"
EOF

# 손으로 답을 아는 입력 — 조건 번호 줄 넷(SK-01 · 스킬-02 · 구조-11 · ER-03), 번호가 아닌 줄 둘
printf '%s\n' '- [ ] SK-01: a' '- [x] 스킬-02: b' '- [ ] 구조-11: c' '- [ ] 2026-09 날짜' '- [ ] foo-12 소문자' '- [ ] ER-03: d' >"$t/t.md"
rx=$(awk '/^contract_digest\(\)/ { getline; print; exit }' "$SCHEMA" | sed -E "s/.*grep -E '([^']*)'.*/\1/")
arx=$(awk '/^measurement_digest\(\)/ { f = 1 } f && /match\(/ { print; exit }' "$SCHEMA" | sed -E 's#^[[:space:]]*/(.*)/ \{ inb=1.*#\1#')
printf '/%s/ { n++ } END { print n + 0 }\n' "$arx" >"$t/a.awk"
printf '%s\n' "$rx" >"$t/rx.txt"

case "${1:-}" in
스킬-01)
  counts "$MD_FILES" | tee "$t/o"
  verdict "$(sed -n 's/^counts_ok=//p' "$t/o")" ;;
스킬-02)
  n=$(grep -cF "$REASON" "$SCHEMA")
  at=$(awk -v r="$REASON" 'index($0, "조건 열거 정규식은") && !s { s = NR } index($0, r) { print NR - s; exit }' "$SCHEMA")
  echo "reason_lines=$n after_rule_line=+$at"
  [ "$n" = 1 ] && [ -n "$at" ] && [ "$at" -ge 1 ] && [ "$at" -le 3 ] && verdict 1; verdict 0 ;;
스크립트-01)
  TMPDIR=$t bash "$TEST" >"$t/pos" 2>&1; prc=$?
  neg_copy
  TMPDIR=$t bash "$t/neg/$TEST" >"$t/negout" 2>&1; nrc=$?
  k3=$(grep -c '^PASS K3-C.UTF-8한국어번호 ' "$t/pos")
  ci=$(grep -cxF '        run: bash harness/evals/measure/measure-helpers-test.sh' .github/workflows/ci.yml)
  echo "mac_rc=$prc mac_fails=$(fail_names "$t/pos") k3_pass=$k3 last=[$(tail -1 "$t/pos")] neg_rc=$nrc neg_fails=[$(fail_names "$t/negout")] ci_step=$ci"
  [ "$prc" = 0 ] && [ "$k3" = 1 ] && [ "$ci" = 1 ] && [ "$(tail -1 "$t/pos")" = "실패 0 건" ] && [ "$nrc" = 1 ] \
    && [ "$(fail_names "$t/negout")" = "K3-C.UTF-8한국어번호" ] && verdict 1; verdict 0 ;;
스크립트-02)
  need_docker; neg_copy
  docker run --rm -v "$root:/w:ro" -v "$t/neg:/neg:ro" -v "$t:/o" -e LC_ALL=C.UTF-8 "$IMG" bash -c '
    apt-get update -qq >/dev/null 2>&1; DEBIAN_FRONTEND=noninteractive apt-get install -y -qq zsh git python3 >/dev/null 2>&1
    bash /w/'"$TEST"' >/o/lin 2>&1; echo $? >/o/lin.rc
    bash /neg/'"$TEST"' >/o/linneg 2>&1; echo $? >/o/linneg.rc' || exit 2
  k3=$(grep -c '^PASS K3-C.UTF-8한국어번호 ' "$t/lin")
  echo "linux_rc=$(cat "$t/lin.rc") linux_fails=[$(fail_names "$t/lin")] k3_pass=$k3 last=[$(tail -1 "$t/lin")] neg_rc=$(cat "$t/linneg.rc") neg_fails=[$(fail_names "$t/linneg")]"
  [ "$(cat "$t/lin.rc")" = 0 ] && [ "$k3" = 1 ] && [ "$(tail -1 "$t/lin")" = "실패 0 건" ] && [ "$(cat "$t/linneg.rc")" = 1 ] \
    && [ "$(fail_names "$t/linneg")" = "K1-한국어번호지문-bash,K1-한국어번호지문-zsh,K2-한국어번호조건수,K3-C.UTF-8한국어번호,M-bash,M-zsh" ] && verdict 1; verdict 0 ;;
스크립트-03)
  need_docker
  mkdir -p "$t/c"
  git ls-tree --name-only "$BASE" .harness/ | grep '^\.harness/sprint-contract-.*\.md$' | while read -r p; do git show "$BASE:$p" >"$t/c/${p##*/}"; done
  git show "$BASE:$SCHEMA" >"$t/old-schema.md"; cp "$SCHEMA" "$t/new-schema.md"
  n=$(find "$t/c" -type f | grep -c .)
  TMPDIR=$t bash "$t/dig.sh" "$t/old-schema.md" "$t/c" >"$t/mac-old"
  TMPDIR=$t bash "$t/dig.sh" "$t/new-schema.md" "$t/c" >"$t/mac-new"
  docker run --rm -v "$t:/o" -e LC_ALL=C.UTF-8 "$IMG" bash -c 'mkdir -p /tmp/x; TMPDIR=/tmp/x bash /o/dig.sh /o/new-schema.md /o/c >/o/lin-new 2>/o/lin-new.err; TMPDIR=/tmp/x bash /o/dig.sh /o/old-schema.md /o/c >/o/lin-old 2>/dev/null' || exit 2
  d1=$(diff "$t/mac-old" "$t/mac-new" | grep -cE '^[<>]')
  d2=$(diff "$t/mac-old" "$t/lin-new" | grep -cE '^[<>]')
  d3=$(diff "$t/mac-old" "$t/lin-old" | grep -cE '^[<>]')
  rows=$(grep -c . "$t/lin-new"); err=$(grep -c . "$t/lin-new.err")
  echo "contracts=$n rows=$rows mac_old_vs_mac_new=$d1 mac_old_vs_linux_new=$d2 linux_new_err=$err control_mac_old_vs_linux_old=$d3"
  [ "$n" = 149 ] && [ "$rows" = 149 ] && [ "$d1" = 0 ] && [ "$d2" = 0 ] && [ "$err" = 0 ] && [ "$d3" -ge 1 ] && verdict 1; verdict 0 ;;
오류-01)
  need_docker
  mac=""
  for L in C C.UTF-8 en_US.UTF-8; do
    mac="$mac$(LC_ALL=$L grep -cE "$rx" "$t/t.md" 2>&1),$(LC_ALL=$L awk -f "$t/a.awk" "$t/t.md" 2>&1),"
  done
  docker run --rm -v "$t:/o" "$IMG" bash -c 'for L in C C.UTF-8; do printf "%s,%s," "$(LC_ALL=$L grep -cE "$(cat /o/rx.txt)" /o/t.md 2>&1)" "$(LC_ALL=$L awk -f /o/a.awk /o/t.md 2>&1)"; done >/o/lin.txt' || exit 2
  lin=$(cat "$t/lin.txt")
  echo "rx=[$rx] awk_rx=[$arx] mac=${mac%,} linux=${lin%,}"
  [ "${mac%,}" = "4,4,4,4,4,4" ] && [ "${lin%,}" = "4,4,4,4" ] && verdict 1; verdict 0 ;;
구조-01)
  counts "$PAGE_FILES" | tee "$t/o"
  page=docs/harness/contract-schema.html
  n=$(grep -cF "$REASON" "$page")
  at=$(awk -v r="$REASON" 'index($0, "조건 열거 정규식은") && !s { s = NR } index($0, r) { print NR - s; exit }' "$page")
  li=$(grep -F "$REASON" "$page" | grep -c '^[[:space:]]*<li>')
  [ -f "$PW" ] || { echo "플레이라이트가 없다: $PW" >&2; exit 2; }
  ov=$(REPO=$root PW=$PW node --input-type=module -e '
    const { chromium } = await import(process.env.PW);
    const b = await chromium.launch(); let n = 0, bad = 0;
    for (const p of ["docs/harness/contract-schema.html", "docs/harness/qa-evaluation-guide.html"]) for (const w of [320, 375, 1280]) {
      const pg = await b.newPage({ viewport: { width: w, height: 800 } });
      await pg.goto("file://" + process.env.REPO + "/" + p);
      const o = await pg.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      n++; if (o > 0) bad++; await pg.close();
    }
    await b.close(); console.log(`cases=${n} overflow=${bad}`);' 2>&1)
  python3 scripts/check-docs-common-css.py >/dev/null 2>&1; css=$?
  echo "reason_lines=$n reason_li=$li after_rule_line=+$at $ov css_rc=$css"
  [ "$(sed -n 's/^counts_ok=//p' "$t/o")" = 1 ] && [ "$n" = 1 ] && [ "$li" = 1 ] && [ "$at" = 1 ] \
    && [ "$ov" = "cases=6 overflow=0" ] && [ "$css" = 0 ] && verdict 1; verdict 0 ;;
구조-02)
  left=$(git grep -l '가-힣' "$BR" -- . ':(exclude).harness' | sed "s#^$BR:##" | LC_ALL=C sort | tr '\n' ' ')
  want=$(printf '%s\n' $KEEP_FILES | LC_ALL=C sort | tr '\n' ' ')
  # shellcheck disable=SC2086  # 목록을 낱말로 나눠 넘긴다
  ch=$(git diff --name-only "$BASE" "$BR" -- $KEEP_FILES react-kit tone-kit docs/react docs/react-kit docs/tone docs/tone-kit | grep -c .)
  echo "left=[${left% }] changed_kept=$ch"
  [ "$left" = "$want" ] && [ "$ch" = 0 ] && verdict 1; verdict 0 ;;
구조-03)
  scope=$(awk '/^# sprint-scope$/ { f = 1; next } f && /^```$/ { exit } f && NF { print }' "$CONTRACT")
  [ -n "$scope" ] || { echo "범위 목록을 못 읽었다" >&2; exit 2; }
  merges=$(git rev-list --merges "$BASE..$BR" | grep -c .)
  bad=0; n=0
  for c in $(git rev-list --reverse --no-merges "$BASE..$BR"); do
    n=$((n + 1))
    files=$(git show --name-only --format= "$c")
    tops=$(printf '%s\n' "$files" | awk -F/ 'NF { print ($1 == "docs" ? $1 "/" $2 : $1) }' | LC_ALL=C sort -u | grep -c .)
    outside=$(printf '%s\n' "$files" | grep -v '^\.harness/' | grep -cvxF "$scope")
    tr_ok=$(git log -1 --format='%(trailers:key=Co-Authored-By,valueonly)' "$c" | grep -cE '^Claude .*<noreply@anthropic\.com>$')
    s="OK"; { [ "$tops" = 1 ] && [ "$outside" = 0 ] && [ "$tr_ok" = 1 ]; } || { s="BAD"; bad=$((bad + 1)); }
    echo "$s ${c:0:8} tops=$tops outside=$outside trailer=$tr_ok"
  done
  echo "commits=$n merges=$merges bad=$bad"
  [ "$n" -ge 3 ] && [ "$merges" = 0 ] && [ "$bad" = 0 ] && verdict 1; verdict 0 ;;
진단-02)
  [ -x "$ML" ] || { echo "markdownlint-cli2 가 없다: $ML" >&2; exit 2; }
  printf '{ "config": { "MD013": false } }\n' >"$t/ml.jsonc"
  md=0
  for pair in $MD_FILES; do
    f=${pair%%:*}; w=$("$ML" --config "$t/ml.jsonc" "$f" 2>&1 | grep -cE '^[^ ]+:[0-9]+')
    echo "$f warnings=$w"; md=$((md + w))
  done
  sc=$(shellcheck "$TEST" | grep -c '^In '); bash -n "$TEST"; bn=$?
  echo "md_warnings=$md shellcheck=$sc bash_n_rc=$bn"
  [ "$md" = 0 ] && [ "$sc" = 0 ] && [ "$bn" = 0 ] && verdict 1; verdict 0 ;;
진단-05)
  [ -e node_modules ] || { echo "node_modules 가 없다 — npm ci 를 먼저 돌린다" >&2; exit 2; }
  mkdir -p "$t/ci" "$t/x"
  TMPDIR=$t/ci bash "$CI_LOCAL" "$root" >/dev/null 2>&1
  sum=$t/ci/ci-local/summary.txt
  rc0=$(grep -c 'rc=0' "$sum"); lines=$(grep -c . "$sum"); skip=$(grep -c 'SKIP' "$sum")
  a11y=$(tail -1 "$t/ci/ci-local/docs-a11y.log")
  bad=""
  while IFS= read -r cmd; do
    [ -n "$cmd" ] || continue
    TMPDIR=$t/x bash -c "$cmd" >"$t/x.log" 2>&1 </dev/null || bad="${bad}[${cmd}]"
  done <<'CMDS'
python3 scripts/check-api-kit-docs.py
python3 scripts/test-check-api-kit-docs.py
python3 scripts/detect-docs-drift.py --check-table
python3 scripts/test-detect-docs-drift.py
python3 scripts/check-docs-common-css.py
python3 scripts/check-cause-table-copies.py
python3 scripts/test-check-cause-table-copies.py
bash harness/evals/measure/measure-helpers-test.sh
bash bambu-kit/evals/run-gate-fixtures.sh
bash bambu-kit/evals/makerworld-fetch-test.sh
bash bambu-kit/evals/run-gate-fixtures-test.sh
npx playwright test api-kit/evals/
CMDS
  echo "local_rc0=$rc0 local_lines=$lines skip=$skip a11y=[$a11y] ci_only_failed=[$bad]"
  [ "$rc0" = $((lines - skip)) ] && [ "$skip" -le 1 ] && [ "$rc0" -ge 25 ] && [ "$a11y" = "206/206 PASS" ] && [ -z "$bad" ] && verdict 1; verdict 0 ;;
*) echo "모르는 조건 번호: ${1:-}" >&2; exit 2 ;;
esac
```
