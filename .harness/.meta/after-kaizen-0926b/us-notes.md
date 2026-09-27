# 사용자 훅 · 핸드오프 스킬 (us) 결과

- 계약: `.harness/sprint-contract-after-0926-user-hooks.md` (21 조건, 봉인 `sha256:92961b02c19bb6a0`, 봉인 커밋 `2c81bc2`)
- 작업 폴더 시작 상태: 앞 단계가 남긴 것은 커밋 안 한 계약 파일 하나뿐이었다. 봉인 커밋으로 담았다.
- 고친 파일(레포 밖) 넷: `~/.claude/hooks/next-session-handoff.sh` · `~/.claude/hooks/parallel-session-guard.sh` · `~/.claude/hooks/enforce-codex-stdin.sh` · `~/.claude/skills/handoff/SKILL.md`. 고친 뒤 사본은 `us-after/` 에 두었다.
- 시험 결과: 고친 뒤 `us-result-after.txt` (61 줄), 실제 세션 `us-e2e-after.txt`.

## 교차 진단 반영 (봉인 전)

- `PATH=/bin` 이 이 맥에서 jq 와 grep 을 같이 숨겼다(`/bin/grep` 없음). 세션 마감 훅이 표준오류에 `grep: command not found` 를 흘리는데 표준출력만 재서 못 잡았다. `us-test.sh` 가 `/usr/bin` 의 jq 뺀 도구마다 exec 감싸개(새 일반 파일)를 둔 폴더를 쓰게 바꾸고, 조용히 지나가야 하는 경우에 `stderr_empty` 칸과 준비 줄 `NOJQ-env jq=0 grep=1` 을 더했다. 고치기 전 결과를 다시 떴다(커밋 `1ab55df`).
- 공동 작성자 줄 목표 문자열은 이 구현 세션의 첨부 안내 줄을 근거로 계약 「범위 경계」 에 적었다.

## 항목별 결과

| ID | 결과 | 근거 (자기 측정) |
| --- | --- | --- |
| US-1 | 고침 | `N1 noti_has_kw=1 empty=1` · `N2 detect=1` · `N3 empty=1` · `H2 empty=1`. 실제 세션 `prompt_kw=0 noti_kw=1 handoff_ctx=0` (고치기 전 `handoff_ctx=1`) |
| US-2 | 고침 | 따옴표 안: `Q1~Q3-pre empty=1`, `Q1·Q2-post landed=0`. 따옴표 밖 진짜 커밋: `Q4·Q5-pre shared=1`, `Q4-post landed=1`. 인덱스: `I1-pre shared=1 mine=0 private=0`, `I2·I3-pre mine=1 private=1`. 기존 18 줄 글자까지 같음. 실제 세션 `pre_ctx=0 post_ctx=0 head_subject=init` |
| US-3 | 고침 | `inhd=0` · 공용 함수 호출 1 줄 · 함수 정의 0. `C01~C12` 12 줄 고치기 전과 같음 |
| US-4 | 고침 | `SK5 … coauthor_now=1 coauthor_old=0` |
| US-5 | 고침 | 틀: 목록 줄 1 개, 순서 검사 1, `없음` 1, `<이유>`·`<날짜>` 0. 훅: `pline_count=1 pline_prd=1 pline_scope=1 pline_approval=1 pline_order=1 pline_none=1 pline_reason=0` |

조건별 측정값:

- SK-01: 제목 1 줄(104 행), 다음 절 `## Known Issues / Blockers`, 목록 줄 1, 순서 1 · 없음 1 · 금지 자리표시 0
- SK-02: `SK5 new_commits=1 subject=1 files=1 other_in_commit=0 other_still_staged=1 coauthor_now=1 coauthor_old=0`
- SK-03: 뺀 줄 2 · 더한 줄 2, 뺀 두 줄이 옛 폐기 칸 줄과 옛 공동 작성자 줄. markdownlint-cli2 0.23.2 (`MD013: false`) `Summary: 0 issues in 0 files`
- SC-01 ~ SC-05: 위 표의 값 그대로
- SC-06: 차이 없음, 18 줄
- SC-07: `inhd=0 call=1 def=0`, `C` 줄 차이 없음 · 12 줄
- ER-01: 13 줄, 어긋난 줄 0, `NOJQ-env jq=0 grep=1` 1 줄
- AR-01: 도우미 `cmp` 종료 코드 0, 대상 밖 12 개 지문 OK 12, 훅 폴더 15 개, 핸드오프 폴더 1 개, 설정 지문 같음, `bash -n` 넷 다 0
- AR-02 · AR-03: 결과 커밋 뒤 부모가 잰다 (이 notes 커밋까지 모두 `.harness/` 아래, `us-backup/` 을 건드린 커밋은 `bfeb84c` 하나)
- RE-01: 도우미에서 함수 선언 확인 종료 코드 0, 대상 훅 셋 모두 함수 정의 0
- RE-02: SC-07 과 같음
- DG-02: shellcheck 0.11.0 `-f gcc` 넷 다 0 줄
- DG-04: 두 실제 세션 모두 `hook_errors=0`
- DG-01 · DG-03 · AP-00: N/A (계약 사유 그대로)

## 톤 대조 (tone-kit:tone-guide 5 단계)

대상은 네 파일의 더한 줄 29 줄이다. 어댑터 없음(셸 · 마크다운) — 코어 규칙과 한국어 축만 적용했다.

| 규칙 | 건수 | 판정 |
| --- | --- | --- |
| C-01 what 대신 why | 0 | 통과 — 더한 주석 넷 모두 실측 실패 모드(작업 알림 헛안내, 따옴표 안 헛경고, `git add` 앞 대입 오판)나 공용 함수 사용 이유 |
| C-02 · A 이름 번역 주석 | 0 | 통과 |
| C-04 · F 구분선 | 0 | 통과 |
| C-07 해설 3 줄 초과 | 0 | 통과 — 가장 긴 주석이 2 줄 |
| C-13 자화자찬 | 0 | 통과 |
| C-15 문체 | 0 | 통과 — 기존 주석과 같은 한다체 |
| H 보존 | — | 기존 주석 삭제 0. codex 훅 주석 한 줄은 뜻을 바꿔 고침(인라인 awk → 공용 함수) |
| N-07 · E 접두 이름 | 0 | 통과 |
| N-08 한 글자 이름 | 0 | 처음에 awk 안 `n` · `q` · `c` 를 썼다가 `len` · `quote` · `ch` 로 고쳤다. 반복 변수 `i` 는 관용 |
| S-03 · S-04 · S-06 | 0 | 통과 — 새 함수 없음. 따옴표 덮기는 판별 한 곳에서만 쓰는 사본이라 인라인 |
| K-02 번역투 (G-1) | 0 | 통과 |
| K-04 · G-2 합니다체 | 0 | 통과 |
| K-11 새 이름 | 0 | 통과 — 「판별용 사본」 은 문장으로 뜻이 드러난다 |

## 킷별 버전 판단

- 레포 킷 파일을 하나도 고치지 않았다 (변경은 `.harness/` 아래뿐). 올릴 버전 없음.

## docs 드리프트

- 원본 문서를 바꾸지 않았다. `detect-docs-drift.py` 대상 없음.

## 로컬 검사

- `python3 scripts/validate-plugin.py`: 14 킷 14 OK
- `sync-docs.py --check-only`: 동기화 상태
- `sync-evals.py --check-only`: 0 added · 0 orphans · 0 missing
- `ci-local.sh` (TMPDIR = scratchpad `ci-us/tmp`): 성공 줄 25, 실패 0, `feedback-agg-test` 는 yq 가 없어 건너뜀

## 남은 것

- 핸드오프 틀은 여전히 모델 이름을 박아 둔다. 다음 모델 교체 때 같은 줄을 또 바꿔야 한다. 틀을 「세션 안내가 준 첨부 줄을 그대로 쓴다」 로 바꿀지 사용자 판단이 필요하다.
- `project.yaml` AP-04 정규식(`^---\s*\n(?![^-]*name:)`)이 앞머리 정보 블록의 닫는 `---` 에도 걸린다 (교차 진단이 `~/.claude/skills/handoff/SKILL.md` 11 행에서 실측). 이 계약 범위 밖.
- 병렬 세션 훅의 커밋 뒤 알림이 `git -C $W …` 처럼 변수로 폴더를 준 커밋에서 다른 작업 폴더의 HEAD(`2349002`)를 보여준다. 이번 세션에서도 두 번 다시 봤다. 이번 범위 밖.
- `bash -c '<명령>'` 처럼 따옴표 안에서 실제로 도는 커밋은 고치기 전에도 못 잡았고 이번에도 잡지 않는다 (계약 US-2 해석).
- QA 판정은 아직 없다.
