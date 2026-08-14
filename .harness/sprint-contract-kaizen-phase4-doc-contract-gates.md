---
feature: "카이젠 Phase 4 — 문서-스크립트 계약(D1) + 게이트 exit taxonomy(D2) + 스펙 정합 + 계약 scope 구조 핸드오프"
created: "2026-08-13 12:50"
complexity: "복잡"
conditions: 23
slug: kaizen-phase4-doc-contract-gates
status: done
owner_session: df1b3e15-30b3-4825-a3c4-4ac44c686e94
conditions_digest: sha256:cd66d3b1ff6b051e
locked_at: "2026-08-13 12:50"
---

## 배경

`.harness/.meta/evidence/phase4.md` 가 이번 Phase 의 **유일한 외부 근거**다. 외부 조회 0 회.

evidence 가 우리 레포에서 **실제 버그 3 종**을 찾아냈고, 전부 재현했다.

- **D1 문서-스크립트 drift** — 오케스트레이터 Step 0 은 `<repo>/.claude/kaizen-input/insights-report.md`
  자동 탐색과 `--insights=PATH` 를 주장하는데 `scripts/collect-kaizen-data.py` 는 둘 다 없다.
  실행 확인: `python3 scripts/collect-kaizen-data.py --help` 출력 옵션은 `--output` · `--hub-dir` ·
  `--skip-validate` 3 종뿐. 그 결과 **사람이 정리한 §0 델타 분석본이 데이터 풀에 들어가지 못한다.**
- **D2 게이트 무력화** — `aggregation-test.sh` 는 `yq` 미설치 시 SKIP 후 `ALL TESTS PASSED` 를
  출력하고 exit 0 한다. 이 머신에 `yq` 가 실제로 없으므로 **지금 그 상태다**
  (`command -v yq` → exit 1). `save-test.sh` 네거티브 테스트 3 건은 stderr 를 버려 "무엇 때문에
  거부됐는지" 를 검증하지 않는다. `finalize-phase.sh --help` 는 `mktemp` 실패 환경에서 usage 를
  한 줄도 못 내고 exit 1 한다 (재현: PATH 에 실패하는 `mktemp` 스텁을 두고 실행 → exit 1, 출력 0 행).
- **C 마커 중복 (D1 과 같은 뿌리 · 신규 발견)** — `.claude/skills/kaizen-orchestrator/SKILL.md` 에
  `<!-- AUTO:plugin_phases:begin -->` / `:end` 가 **각각 2 회** 등장한다 (측정: python 문자열 count).
  `sync-orchestrator.py` 는 `content.find()` 로 **첫 번째** 쌍을 잡으므로, 자동 생성 블록이
  Gotchas 절의 산문 불릿 안(첫 쌍)에 계속 주입돼 왔다. 진짜 Process 위치(두 번째 쌍)는 갱신되지
  않아 **Phase 12(reflect-kit) 와 Phase 13(bambu-kit) 의 `### Step` 절이 Process 에서 통째로
  빠져 있다.** 그런데도 `sync-orchestrator.py --check-only` 는 exit 0 "이미 동기화됨" 을 보고한다 —
  게이트가 파손을 통과로 보고하는 D2 와 같은 실패 모드다.

## 리서치 소스 (evidence 파일 한정 — 외부 조회 0 회)

- `.harness/.meta/evidence/phase4.md` §1~§4 — D1/D2/D3 실측 · 확립된 대응(argparse SoT ·
  Google Shell Style Guide stderr · BashFAQ/105 · ShellCheck SC2310/SC2312 · SARIF
  `executionSuccessful` · Bats exit-status assert · Segment/Stripe identity) · 권장안 · 트레이드오프
- `.harness/.meta/kaizen-data-pool.md` §1 — legacy-identity 244 / deterministic 35 ·
  raw 이름 14 종 → canonical 5 종 · REJECT `AR-04` 계약 경로 열거 위반 3 회 ·
  Improvement `[AR-04] 계약-측정-불일치`
- `.claude/kaizen-input/insights-report.md` — 직전 사이클 흡수분 표(재승격 금지). §0 신규 델타
  D1~D5 는 전부 다른 Phase 소관(bambu/design/backend/flutter)이라 **Phase 4 직접 신호는 없다**
- Phase 1 산출물 — `harness/docs/guides/agent-design-guide.md` §frontmatter 전체 필드
  (공식 15 종 · 필수는 `name`/`description` 둘뿐 · 플러그인 에이전트는 `hooks`/`mcpServers`/
  `permissionMode` 무시), `skill-design-guide.md` (SKILL.md frontmatter 필수 2 종)
- Phase 3 산출물 — `.harness/sprint-contract-kaizen-phase3-unverified-triage.md` §폐기·재작성
  (계약 scope 자기모순 3 회 실증 · AR-01 오라클 결함), 커밋 `b161d80`
- `harness/references/contract-schema.md` v5.3 — 본 계약의 포맷 SSOT

## GAP 분석 (전부 실측)

| # | 갭 | 실측 근거 | 처리 |
| --- | --- | --- | --- |
| G1 | 문서가 주장하는 스크립트 인터페이스가 없다 | `--help` 출력에 `--insights` 0 건 | 스크립트에 구현 + `docs-contract` 선언 |
| G2 | drift 를 기계적으로 잡는 검사가 없다 | 이 drift 가 최소 1 사이클 이상 방치됨 | `validate-doc-contracts.py` 신설 + post-kaizen 편입 |
| G3 | 도구 부재가 통과로 집계된다 | `yq` 부재인데 `ALL TESTS PASSED` exit 0 | exit taxonomy + python3 fallback |
| G4 | 네거티브 테스트가 실패 사유를 검증하지 않는다 | `save-test.sh:74,88,97` `2>/dev/null` | stderr 캡처 후 메시지 assert |
| G5 | help path 가 side-effect free 가 아니다 | `mktemp` 실패 시 usage 0 행 · exit 1 | 인자 처리 최상단 이동 |
| G6 | 인프라 오류가 위반 0 건으로 둔갑한다 | `git_diff_names()` 가 실패 시 `[]` 반환 · `check_scope_isolation` 이 git 실패를 SKIP | `ERROR` 상태 + exit 2 |
| G7 | scope 격리 검사가 신규 4 킷을 안 본다 | 하드코드 prefix 6 종 (planning/reflect/bambu/onboarding 누락) | marketplace.json 에서 유도 |
| G8 | 마커를 substring 으로 찾아 잘못된 위치를 덮어쓴다 | 마커 각 2 회 · Phase 12·13 Process 누락 | 행 앵커 + 유일성 강제 (0 또는 2+ 는 exit 2) |
| G9 | 스킬이 공식 스펙과 레포 정책을 뒤섞는다 | `create-agent:25` "tools/model 누락 → invisible 처리" — 공식 스펙상 둘 다 **선택** | 출처 분리 서술 |
| G10 | 계약 scope 열거가 다중 커밋 스프린트에서 3 회 연속 파손됐다 | Phase 3 §폐기·재작성 1~4 항 | Phase 2 소관 → 핸드오프 문서 + 본 계약이 구조 시연 |

## 범위 경계

**구현 변경 경로 11 개** (AR-01 의 기대 집합 한 곳에서만 열거한다 — §측정 커버리지 표기의
화이트리스트 규칙):

`.harness/` 하위는 **범주 규칙**으로 분리 정의한다 (AR-02). 파일 단위 exact enumeration 이
다중 커밋 오케스트레이션 스프린트에 구조적으로 취약하다는 것이 Phase 3 에서 3 회 실증됐고,
경로를 하나씩 추가하는 두더지잡기는 이번에 반복하지 않는다. 오케스트레이터가 Step 11 감사
로그를 언제 커밋하든 `.harness/.meta/**` 범주에 들어가므로 계약이 깨지지 않는다.

- **Phase 2 소관이라 건드리지 않는다**: `harness/references/contract-schema.md` ·
  `harness/skills/sprint-contract/`. 필요한 개정은 `.harness/.meta/phase4-handoff-to-contract.md`
  에 위치·문구 제안으로만 남긴다 (SK-03).
- **Phase 3 소관이라 건드리지 않는다**: `harness/agents/qa-evaluator.md` ·
  `harness/docs/guides/qa-evaluation-guide.md`.
- **D3 (피드백 identity 레거시) 는 이번 사이클 미반영**이다. evidence 의 canonical id + alias
  table + backfill index 제안을 검토한 결과, **집계 reader 가 현재 1 개뿐**이다 (측정:
  `grep -rn 'project_name' --include='*.py' --include='*.sh' scripts/ harness/ reflect-kit/` —
  reader 는 `scripts/collect-kaizen-data.py` 의 `canonical_project_name()` 하나, writer 는
  `harness/scripts/save-feedback.sh` 하나). evidence 가 경고한 "모든 reader 가 같은 alias 함수를
  호출해야만 맞는 구조" 의 위험은 reader 가 2 개 이상일 때 발생하는데 그 조건이 아직 성립하지
  않는다. 게다가 alias 테이블을 파일로 분리하면 `harness/references/` 로 가야 하는데 그곳은
  Phase 4 scope 밖이다. **재검토 트리거: 집계 reader 가 2 개 이상이 되는 시점.** 원본 YAML
  파괴적 rewrite 는 어느 경우에도 하지 않는다.
- 조건 수 23 은 복잡도 가이드 상한(20)을 3 초과한다. 사유: 서로 독립적인 결함 클러스터가
  4 종(D1 · D2 · 스펙 정합 · 핸드오프)이고, 각 클러스터를 하나로 묶으면 복합 조건이 된다.

### Diff-Scope baseline (작성 시점 1 회 실행)

`git diff --name-only b161d80..HEAD` → 0 행 (스프린트 시작 시점, HEAD = `b161d80`).

## 회귀 게이트

- `collect-kaizen-data.py` 는 **하위호환을 유지한다.** 인자 없이 실행할 때 기존 3 옵션의 의미가
  바뀌지 않고, 후보가 하나도 없으면 종전대로 §0 에 "(없음)" 을 쓰고 진행한다. 이미 생성된
  `.harness/.meta/kaizen-data-pool.md` 는 이번 스프린트에서 **재생성하지 않는다** (그 파일은
  구현 변경 경로가 아니다). 다음 사이클 Step 0 이 새 우선순위로 재수집하는 것이 마이그레이션
  경로다.
- exit code 의 **0 = pass 의미는 바뀌지 않는다.** 새로 도입하는 값은 2(usage/infra) 와
  3(no_data/not_run) 이며, 기존 1(policy violation) 의 의미도 유지한다. 비-0 를 실패로 취급하던
  호출부는 그대로 동작한다.
- `sync-orchestrator.py` 의 정상 경로 출력 문구(`이미 동기화됨` · `DRIFT 감지`)와 exit 0/1 은
  유지한다. 새 exit 2 는 마커 개수 이상일 때만 난다.
- AUTO 생성 영역 안의 문구는 손으로 고치지 않는다 — 스크립트를 실행해 재생성한다.

## Architecture

- [ ] AR-01: 스프린트 누적 구현 변경이 정확히 11 경로로 한정된다 [exact, enumerated]
      (Given: 스프린트 base = `b161d80` (Phase 3 종료 커밋) ·
       측정: `git diff --name-only b161d80..HEAD -- . ':(exclude).harness'` 출력을 `LC_ALL=C sort`
       한 집합이 아래 11 경로와 `comm -3` 양방향 차집합 0 건 —
       `.claude/skills/kaizen-orchestrator/SKILL.md`,
       `harness/evals/gate-exit-codes.md`,
       `harness/evals/kaizen/feedback-system/aggregation-test.sh`,
       `harness/evals/kaizen/feedback-system/save-test.sh`,
       `harness/skills/create-agent/SKILL.md`,
       `harness/skills/create-skill/SKILL.md`,
       `scripts/collect-kaizen-data.py`,
       `scripts/finalize-phase.sh`,
       `scripts/sync-orchestrator.py`,
       `scripts/validate-doc-contracts.py`,
       `scripts/validate-post-kaizen.py` ·
       커밋 전후 무관하게 재현 가능하다 — `git status --porcelain` 은 오라클로 쓰지 않는다)
- [ ] AR-02: `.harness/` 하위 누적 변경이 전부 harness 부기 4 범주 안에 든다 [structural]
      (측정: `git diff --name-only b161d80..HEAD -- .harness` 의 각 행이 아래 4 정규식 중 하나에
       매치 — 미매치 0 행. `^\.harness/sprint-contract-kaizen-phase4-.*\.md$` ·
       `^\.harness/sprint-amendments-kaizen-phase4-.*\.md$` ·
       `^\.harness/sprint-feedback-kaizen-phase4-.*\.md$` · `^\.harness/\.meta/` ·
       범주 규칙이므로 오케스트레이터가 감사 로그를 추가 커밋해도 위반이 되지 않는다)
- [ ] AR-03: 오케스트레이터 Process 절이 Phase 5~14 각 킷을 `### Step` 헤딩 1 개씩만 담는다
      [exact, enumerated]
      (측정: `grep -c '^### Step .*Phase <N> — <kit> 카이젠'` 을 marketplace.json 의 harness 제외
       10 킷에 대해 계산해 전부 1 · 합계가 킷 수와 일치. 킷 목록과 개수는 타이핑하지 말고
       marketplace.json 에서 계산한다)

## Script

- [ ] SC-01: `collect-kaizen-data.py` 의 실제 인터페이스가 오케스트레이터 문서 주장과 일치한다
      [exact, enumerated]
      (측정: `python3 scripts/collect-kaizen-data.py --help` 출력에 `--insights` 가 등장하고,
       `--output` · `--hub-dir` · `--skip-validate` 3 종이 그대로 남아 있다 —
       4 종 모두 확인. 손으로 옵션 목록을 비교하지 말고 help 출력에서 추출한다)
- [ ] SC-02: `/insights` 입력 후보 우선순위가 4 단계로 구현되고 실행으로 확인된다 [exact, enumerated]
      (측정: `--insights <파일>` 로 임시 md 를 넘기면 그 파일이 §0 에 실리고,
       인자 없이 실행하면 `.claude/kaizen-input/insights-report.md` 가 선택되며,
       stderr 에 후보 전체와 선택된 후보가 출력된다. 임시 출력 경로(`--output`)로만 실행해
       `.harness/.meta/kaizen-data-pool.md` 는 건드리지 않는다 ·
       음성 대조: 후보 목록에서 선택된 항목을 제거하면 다음 순위 후보가 선택돼야 한다)
- [ ] SC-03: `validate-doc-contracts.py` 가 선언과 argparse 실체의 불일치를 실제로 잡는다 [goal]
      (측정: 현재 트리에서 실행하면 exit 0 · 선언 블록에서 옵션 하나를 임시로 지우면 exit 1 이고
       위반 항목이 출력된다 ·
       음성 대조: 대조 대상이 argparse `_actions` 이므로, 스크립트에서 그 옵션을 제거하면
       (문서를 고치지 않아도) 이 측정이 FAIL 해야 한다. 문서 자연어 regex 추론은 쓰지 않는다)
- [ ] SC-04: post-kaizen 게이트가 doc-contract 검사를 포함하고 전체 실행이 통과한다 [structural]
      (측정: `python3 scripts/validate-post-kaizen.py --since b161d80` 출력에 `doc-contracts` 행이
       있고 FAIL 0 · 종료 코드 0)
- [ ] SC-05: `sync-orchestrator.py` 가 마커 개수 이상을 조용히 넘기지 않는다 [exact]
      (측정: 마커가 2 쌍인 임시 사본에 대해 실행하면 exit 2 와 원인 메시지가 나오고,
       1 쌍인 실제 파일에 대해 `--check-only` 는 exit 0 ·
       음성 대조: 행 앵커·유일성 검사를 제거하면 2 쌍 입력이 exit 0 으로 통과해야 한다)
- [ ] SC-06: `finalize-phase.sh --help` 가 side-effect free 하다 [exact]
      (측정: PATH 에 항상 실패하는 `mktemp` 스텁을 얹고 `bash scripts/finalize-phase.sh --help`
       를 실행 — exit 0 이고 usage 본문이 출력된다. 인자 없는 호출도 동일 ·
       음성 대조: help 처리를 `mktemp` 아래로 되돌리면 이 측정이 FAIL 해야 한다)

## Error

- [ ] ER-01: `aggregation-test.sh` 가 `yq` 부재에도 실제 검증을 수행한다 [goal]
      (측정: `yq` 없는 현 환경에서 실행 — `SKIP` 이 아니라 python3 fallback 으로 3 건을 감지하고
       PASS 를 출력, exit 0 ·
       음성 대조: fixture 의 `ambiguous_conditions` 를 `false` 로 바꾼 사본으로 돌리면 FAIL 하고
       exit 1 이어야 한다)
- [ ] ER-02: 도구가 하나도 없으면 통과로 집계되지 않는다 [exact]
      (측정: PATH 를 좁혀 `yq` 와 `python3` 를 동시에 가린 상태로 실행 — exit 2 이고 출력에
       `ALL TESTS PASSED` 가 0 건이며 `NOT RUN` 사유가 출력된다)
- [ ] ER-03: `save-test.sh` 네거티브 3 건이 stderr 를 버리지 않고 사유를 검증한다 [exact, enumerated]
      (측정: 파일에 `2>/dev/null` 이 0 건이고, 3 건 각각이 캡처한 stderr 에 대해 에러 문자열을
       assert 한다. 실행 시 전체 통과 · exit 0 ·
       음성 대조: `save-feedback.sh` 의 필수 필드 검사를 무력화하면 해당 네거티브가 FAIL 해야 한다)
- [ ] ER-04: `validate-post-kaizen.py` 가 인프라 오류를 위반 0 건으로 둔갑시키지 않는다 [exact]
      (측정: 존재하지 않는 ref 로 `--since` 를 주면 해당 검사들이 `ERROR` 로 표시되고 종료 코드가
       2 다 — 0 이 아니다 ·
       음성 대조: `git_diff_names()` 를 실패 시 `[]` 반환으로 되돌리면 같은 입력이 exit 0 으로
       통과해야 한다)

## Skill

- [ ] SK-01: `create-agent` · `create-skill` 2 개 스킬이 공식 스펙 필수 필드와 이 레포
      validate-plugin 정책 필드를 구분해 서술한다 [exact, enumerated]
      (측정: 두 파일 각각에 "공식" 필수가 `name` · `description` 2 종임이 적혀 있고,
       레포 정책 필드(agents 4 종 / skills 3 종)가 `scripts/validate-plugin.py` 출처로 표기된다.
       두 파일에서 "invisible" 을 tools/model 누락의 결과로 서술한 곳 0 건)
- [ ] SK-02: 오케스트레이터 Step 0 이 스크립트 인터페이스를 `docs-contract` 블록으로 선언한다
      [structural]
      (측정: `.claude/skills/kaizen-orchestrator/SKILL.md` 에 ` ```yaml ` 펜스로 시작하고 첫 줄이
       `# docs-contract` 인 블록이 존재하며 `script` · `options` · `input_candidates` ·
       `exit_codes` 4 키를 갖는다. 자유 서술로 인터페이스를 주장한 문장은 이 블록으로 대체된다)
- [ ] SK-03: 계약 scope 구조 결함 3 종의 개정안이 Phase 2 핸드오프 문서로 남는다 [structural, enumerated]
      (측정: `.harness/.meta/phase4-handoff-to-contract.md` 가 존재하고 3 결함
       — 사이드카 경로 누락 · `git status --porcelain` 오라클 · 다중 커밋 exact enumeration —
       각각에 대해 대상 파일 경로 · 삽입 위치(절 이름) · 제안 문구를 담는다.
       Phase 4 가 직접 수정하지 않았음이 `git diff --name-only b161d80..HEAD` 에
       `harness/references/contract-schema.md` 와 `harness/skills/sprint-contract/` 0 건으로 확인된다)

## Anti-patterns

- [ ] AP-03: 변경·신설 파일의 여는 코드 펜스에 언어 힌트가 있다 — bare fence 0 건 [exact]
      (측정: 펜스 길이를 인식하는 검출기로 판정. 나이브 `^```$` grep 은 닫는 펜스를 오탐하므로
       오라클로 쓰지 않는다)
- [ ] AP-04: 변경한 SKILL.md 2 종의 frontmatter `name` 이 보존된다 [exact, enumerated]
      (측정: `create-agent` · `create-skill` frontmatter 에서 `name` 값을 추출해 HEAD 판과
       문자열 동일)

## Reusability

- [ ] RE-01: exit code taxonomy 가 한 곳에 정의되고 소비처가 재정의하지 않는다 [exact, enumerated]
      (측정: `harness/evals/gate-exit-codes.md` 에 4 값(0/1/2/3)의 정의가 있고,
       `aggregation-test.sh` · `save-test.sh` · `validate-post-kaizen.py` ·
       `validate-doc-contracts.py` 4 파일이 그 경로를 주석으로 인용한다. 4 파일에서 값의
       의미를 다시 정의한 표·목록 0 건)
- [ ] RE-02: AUTO 마커 해석 로직이 `sync-orchestrator.py` 한 곳에만 존재한다 [exact]
      (측정: 레포 추적 파일에서 `AUTO:plugin_phases` 마커를 **해석**하는 코드가
       `scripts/sync-orchestrator.py` 1 개 · 다른 스크립트에 복제 0 건)

## Diagnostics

- [ ] DG-01: `python3 scripts/validate-plugin.py` 전체 실행이 FAIL 0 건 [exact]
      (측정: 명령을 실행해 종료 코드와 FAIL 카운트를 출력)
- [ ] DG-02: 변경·신설한 셸 스크립트가 구문 검사와 정적 분석을 통과한다 [exact, enumerated]
      (IDE 진단 대체 — 이 레포에는 IDE lint 대상 소스가 없다 ·
       측정: 변경된 `.sh` 전부에 `bash -n` 과 `shellcheck -o all` 실행, 오류 0 건.
       조건 검증에 쓴 명령은 zsh 와 bash 양쪽에서 실행해 출력을 `diff` — 차이 0 건)
- [ ] DG-03: `python3 scripts/sync-docs.py --check-only` 가 이번 변경으로 인한 갱신을 요구하지
      않는다 [exact]
      (측정: 명령 실행 출력에 이번 스프린트의 구현 변경 경로가 갱신 대상으로 등장하지 않음)
