# c4d — 폐기 결정 기록 자리를 하나로

- 계약: `.harness/sprint-contract-after-0924-discard-decisions.md` (20 조건 · 기능 조건 12, 봉인 `sha256:881358107856d327`, `locked_at` 2026-09-26 13:31)
- 가지: `chore/ak-c4d` (시작 커밋 `f81568d`)
- 사용자 결정: 원문 자리는 기능 PRD 비범위 표 하나다 (user `2026-09-26T02:47:55.337Z` 「plan-prd 표로 확정」, 세션 기록 `bda55d45-296c-491f-89ba-b52042d58e72.jsonl` 1187 번째 줄)
- QA 판정: 아직 없음. 다음 단계에서 qa-evaluator 가 한다

## 한 일

| 커밋 | 내용 |
| --- | --- |
| `b728c69` | 계약 봉인. 계약 파일 하나만 실었다 (`git show --name-only` 1 개) |
| `4c079fa` | design-kit — design-mockup 승인 기록 폐기 칸이 PRD 비범위 표를 가리키게, PRD 가 없을 때 `PRD 없음` 한 줄, Step 2 가 PRD 비범위 표를 읽는다 |
| `ad9fe5c` | harness — `/sprint` Step 0.5 재검증에 폐기한 결정 명령 두 줄 · 보고 한 줄 · 원문 자리 한 문단, sprint-contract 포맷 규칙에 한 줄 (더한 줄 1 · 지운 줄 0) |
| `470579f` | `.claude/kaizen-input/insights-report.md` — F20 · design:P5 · backend-family:P1 · user-setup:P2 · user-setup:P6 다섯 행 비고 끝에 처리 결과 |
| 이 notes 커밋 | `.harness/.meta/after-kaizen-0926/c4d-notes.md` 하나 |

넣은 글은 계약 `## GAP 분석` 의 개선안([D1]~[I1])과 같다. 사본에 개선안을 넣어 둔 알려진 답 사본(`clone-good`)과 네 파일 모두 `cmp` 로 같음을 확인했다.

## 봉인 전 교차 진단 반영

- `m DG-03` 이 「모르는 조건」 으로 멈췄다 — 측정 도우미에 `DG-03) m DG-01` 분기를 더하고 DG-03 조건 문구를 `m DG-03` 으로 맞췄다. 시작 판에서 `release_sh=0` 을 다시 확인했다
- AR-02 의 배정 요약 `Phase 74 · 이번 스프린트 16 · 해당 없음 6` 은 처리 배정표 전체 행의 `배정` 칸 합계다. 이 묶음은 다섯 행의 `비고` 칸만 고쳐서 가지 끝에서는 그대로다. 같은 파일을 고치는 다른 묶음이 먼저 `main` 에 합쳐지면 합친 판에서 이 값이 달라질 수 있는데, 그것은 이 묶음의 회귀가 아니다 — 평가 기준은 이 가지 끝이다. PR 설명에도 한 줄 남긴다
- SK-03(design-mockup Step 2 가 PRD 비범위 표를 읽기)과 F20 행은 과제 문구 밖의 판단이라 봉인 전에 사용자 확인을 받으라는 권고가 있었다. 사용자 위임(`2026-09-26T01:04:21.505Z` 「다 실행하고 이어질 것도 실행해」 · `2026-09-24T04:04:16.964Z` 「물어보지 말고 끝까지」)에 따라 묻지 않았다. 근거는 아래 「이 계약의 판단」 이고, 둘 다 더하기만 하는 변경이라 되돌리기 쉽다

## 이 계약의 판단

- F20 행에도 처리 결과를 적었다 — 과제는 네 행(design:P5 · backend-family:P1 · user-setup:P2 · user-setup:P6)을 적었지만 F20 행 비고(`:77`)에 같은 「네 곳이다 — 카이젠에서 하나로 정한다」 문장이 있어, 남기면 처리 뒤에도 미정으로 읽힌다
- design-mockup Step 2 가 PRD 비범위 표를 읽게 두 줄을 더했다 — 폐기 칸만 고치면 기획 단계에서 버린 항목(승인 기록에 없는 것)을 시안이 모른다. F20 이 실제로 그렇게 났다. 기획 뒤 단계 셋(plan-stories · plan-flow · plan-data-model)은 이미 같은 표를 읽는다
- design-concept 폐기 칸은 그대로 두었다 — 컨셉 안(무드 · 색 방향)만 버리는 칸이고 기능·설정 항목이 아니다
- visual-change-protocol §4 는 그대로 두었다 — 이미 「제품 요구 수준의 폐기 결정은 그 결정이 적힌 파일 경로를 폐기 칸에 적는다」 로 경로만 적게 한다. 그 경로가 PRD 비범위 표라는 것은 design-mockup 쪽 글이 말한다. 같은 파일 §6 은 다른 워크트리(`ak-c3`)가 고치고 있어 건드리지 않았다
- 폐기 칸 이름 `폐기한 대안·이유` 는 그대로 두었다 — 확인 명령의 `→ 2` 와 `design-kit/evals/evals.json:539` 가 이 이름을 본다. 시각 대안(고르지 않은 시안 · 배치)만 버린 경우는 이유 한 줄을 이 칸에 그대로 남긴다
- user-setup:P6 — 핸드오프 틀의 폐기 절은 세션 인계용이라 따로 둔다. 결정 원문 자리가 아니다(원문은 기능 PRD 비범위 표). 틀 수정은 킷 밖 사용자 설정 몫이라 이 묶음에서 고치지 않았다

## 넘긴 것과 사유

- F1H-41 앞절반 — `/sprint` Step 3 원인 가르기 판정 표(CI 에서만 보이는 두 경우 `phase8-notes.md:94` · 첫 줄 문턱 `phase9-notes.md:94`). 폐기 결정과 다른 일이고, 표를 바꾸면 글자 그대로 옮긴 사본 둘(`docs/infra/platform/cicd.md:76` · `rust-kit/skills/rust-preflight/SKILL.md:112`)도 함께 바뀌어야 해 이 묶음 범위 밖이다. 다음 사이클 Phase 4 로 넘긴다. F1H-41 뒷절반(재검증 블록의 폐기 결정 자리)은 이 묶음이 했다
- PRD 가 나중에 생겼을 때 `PRD 없음` 줄을 PRD 비범위 표로 옮기는 절차 — plan-prd Step 0 이 읽을 대상을 늘리는 일이라 planning-kit 몫이다. 다음 사이클로 넘긴다
- `docs/design-kit/design-mockup.html` — 원본 Step 2 감지 블록이 바뀌어 이 페이지가 옛 글이 됐다(페이지 481 번째 줄 `.design/approvals/*.md` 다음에 `.planning/prd-*.md` 줄이 없다). Step 6 폐기 칸 자리표시자는 이 페이지에 글자 그대로 실려 있지 않다. 페이지 재생성은 부모가 모아서 한다
- 핸드오프 스킬(`~/.claude/skills/handoff`) · 다른 킷 — 범위 밖

## 킷별 버전 판단

| 킷 | 판단 | 이유 |
| --- | --- | --- |
| design-kit | patch | 새 스킬 · 새 인자 없이 design-mockup 승인 기록 칸의 글과 Step 2 감지 한 줄을 고쳤다. 기존 승인 기록 형식(칸 이름 · 확인 명령 `→ 2`)은 그대로다 |
| harness | patch | `/sprint` 재검증 보고에 한 줄 · 명령 두 줄, sprint-contract 포맷 규칙에 한 줄을 더했다. 지운 줄 · 바뀐 판정은 없다. `origin/main` 이 이미 v0.14.1 이라 그 위에서 올린다 |
| `.claude/` | 해당 없음 | 킷이 아니다 |

## docs 와 원본이 어긋났는지

`python3 scripts/detect-docs-drift.py --since f81568d --verbose` → 「no docs drift since f81568d」 (종료 코드 0). 이 스크립트는 `harness/docs/guides/` · `harness/references/` · `docs/<킷>/` 같은 리서치 원본만 보고 SKILL.md 는 보지 않는다. 손으로 찾은 어긋남은 위 `docs/design-kit/design-mockup.html` 하나다. `docs/harness/` 에는 sprint · sprint-contract 스킬 페이지가 없다.

## 저장소 검사

- `python3 scripts/validate-plugin.py design-kit` · `harness` → 둘 다 종료 코드 0 (V1 ~ V10 OK)
- `python3 scripts/sync-docs.py --check-only` → 0, 「모든 README가 동기화 상태」 — README 갱신 없음
- `python3 scripts/sync-evals.py --check-only` → 0 (added 0 · orphans 0 · missing 0)
- `python3 scripts/check-insights-tracking.py` 기본 · `--final` → 둘 다 0, 배정 요약 그대로
- 로컬 CI(`ci-local.sh`, 끝 판 `470579f`, `TMPDIR` 은 이 세션 스크래치 `c4d/ci1`): `rc=0` 22 줄, `feedback-agg-test SKIP (yq 없음)` 한 줄. CI 파일에만 있는 줄은 설치 단계(`pip install pyyaml` · zsh 설치 · `npm ci` · playwright 설치)뿐이다. 실행 뒤 작업 폴더 변경 0 줄

## 조건별 자기 측정 (끝 판 `470579f`, 가지 끝 계약에서 새로 떼어 낸 도우미)

| 조건 | 출력 |
| --- | --- |
| SK-01 | `field=1 kind=1 norewrite=1 table=1 gotcha=1 old=0 check=1` |
| SK-02 | `all=1 prose=1 planning=1 cols=1 nocreate=1` |
| SK-03 | `load=1 rule=1 approvals=1 keep=1` |
| SK-04 | `tline=1 none=1 find=1 grep=1 src=1 keep_out=1 old=111111` |
| SK-05 | `numstat=1/0 in_fmt=1 scope=1 gotcha=1 tag=1 cols=1 argsub=0` |
| SC-01 | `lines=2 p1: bash=out2/prd1/tag1/err0 zsh=out2/prd1/tag1/err0` |
| ER-01 | `lines=2 p0: bash=out0/prd0/tag0/err0 zsh=out0/prd0/tag0/err0` |
| AR-01 | `changed=5 extra=0 req=1111 multi_top=0` (notes 커밋 전) |
| AR-02 | `rows=5 slug=5 prd=5 cells_same=5 p5=1 p2=1 p6=1 del=5 add=5 other=0 basic=0 final=0 counts=[Phase 74 · 이번 스프린트 16 · 해당 없음 6]` |
| AR-03 | notes 커밋 전이라 `committed=0` — 커밋 뒤 다시 잰다 |
| AR-04 | `seal_commit_files=1 seal_before_impl=1 seal_same_as_tip=1 this=SEAL_OK` |
| RE-01 · RE-02 | `added=0` · `prd_changed=0 hdr=3 cols=111 ptr=1` |
| DG-01 · DG-03 · DG-04 | `release_sh=0` · `release_sh=0` · `non_md=0` |
| DG-02 | `md_new=0` (바뀐 네 파일 각 0) |
| AP-03 · AP-04 | `v6_rc=0 ok=14 fail=0` · `v1_rc=0 ok=14 fail=0` |
| DG-05 | 위 로컬 CI — `rc=0` 22 · SKIP 한 줄 |

## tone-guide 5 단계 대조

규칙은 이 가지의 `tone-kit/references/` 와 오버레이 `.claude/tone-project.md`(어댑터 없음 · 주석 언어 ko)에서 읽었다. 어댑터가 없어 스택 고유 대조 목록은 돌리지 않았다. 대상은 `b728c69..470579f` 에서 더한 줄 14 줄이다(마크다운 스킬 글 · 명령 두 줄 · 표 비고).

| 패턴 / 규칙 | 건수 | 판정 |
| --- | --- | --- |
| K-02 번역투 6 종 (locale-korean §8 G-1 식) | 0 | 통과 — 식이 살아 있는지 `에 의해` 가 든 예문으로 1 건 나오는 것을 먼저 봤다 |
| K-04 종결형 (`합니다` · `습니다`) | 0 | 통과 — 산문은 모두 `한다` 체 |
| K-05 외래어 · 음역 | 0 | 통과 — `PRD` · `Gotcha` · `Non-goals` · `No-gos` · `Shape Up` 은 원래 이름 그대로 |
| K-11 새 이름 | 0 | 통과 — `비범위 표` 는 planning-kit 에 이미 있는 말이다(`planning-reviewer.md:103` · `docs/planning/prd-patterns.md:133`) |
| C-01 · C-15 명령 줄 주석 | 2 | 통과 — `# 폐기한 결정 원문이 든 PRD` · `# PRD 가 없을 때 적어 둔 폐기 결정` 은 그 줄 출력이 무엇인지 알린다. 같은 블록 형제 줄(`# 실제로 들어간 커밋` 등)과 같은 짧은 조각 모양이다(C-08) |
| C-04 구분선 · C-10 디자인 툴 참조 · C-13 자화자찬 | 0 | 통과 |
| N-07 `effective` · `resolved` 접두 | 0 | 통과 |
| S-12 같은 자리 같은 모양 | — | 통과 — 감지 블록 줄은 기존 줄과 같은 28 칸 정렬, 규칙 줄은 `- X 존재 → …` 모양, 표 비고는 기존 `· 미반영 — …` 처럼 `· 처리(…) — …` 로 이어 붙였다 |
| H 보존 | — | 지운 줄은 design-mockup 폐기 칸 자리표시자 한 줄과 표 다섯 행의 옛 판뿐이다. 표 행은 앞 글을 지우지 않고 끝에 덧붙였다 |

사용자 쉬운 말 목록(`~/.claude/rules/plain-korean.md`)에 걸리는 낱말도 더한 줄에서 0 건이었다.

## 측정 도구

- 측정 도우미 원본: 세션 스크래치 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/c4d/measure.sh` (계약 속 블록과 `cmp` 같음)
- 가지 끝 전부 재기: 같은 폴더 `measure-tip.sh` — 가지 끝 계약에서 도우미를 새로 떼어 `m` 을 조건마다 부른다
- 개선안 사본 적용: `mock.py`(알려진 답 · 양성 대조), 표 다섯 행만: `apply-rows.py`
- 톤 대조: `tone5.sh`, 봉인: `seal.sh`, Step 6.5 저장 검사: `gate65.sh`
- 로컬 CI: `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh`
