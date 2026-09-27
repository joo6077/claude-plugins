# hs 묶음 notes — harness 스크립트 · 시험 · 커밋 안전 훅

- 계약: `.harness/sprint-contract-after-0926-harness-scripts.md` (봉인 `conditions_digest: sha256:46d0b11f882527e0` · `measurement_digest: sha256:457007c4f27ccb5e` · 봉인 커밋 `93189f3`)
- 개정: `.harness/sprint-amendments-after-0926-harness-scripts.md` AM-01 — 사용자 동의 받음 (2026-09-26T16:22:39.485Z, `a415f0a`)
- 가지: `chore/ak2-hs` · 기준 판 `6378948` · 끝 판 `6b4c6d7` · QA 3 회차 APPROVE (리포트 커밋 `396943b`)

## 항목별 결과

| ID | 결과 | 커밋 |
| -- | ---- | ---- |
| HS-1 | 고침 — 피드백 저장이 `HARNESS_CONTRACT` 파일에서 위로 올라가 계약 폴더를 잡는다. 초안 식별 칸 다섯은 `draft_<칸>` 으로 보존하고 최종 칸은 한 번만 쓴다. sprint-contract Step 9 초안 이름을 `feedback-draft-<slug>.yaml` 로, init 은 `feedback-draft*.yaml` 를 무시하라고 안내 | `e38b7d9` |
| HS-2 | 고침 — 피드백 저장 시험이 실행마다 임시 폴더 하나만 쓰고 HOME 도 그 안으로 돌린다. 넷씩 세 번 동시 실행 12 회 중 실패 0 | `e38b7d9` |
| HS-3 | 고침 — 같은 명령의 `git add <경로>` 는 그 경로의 작업 폴더 삭제를 얹어 세고(되돌림 검사 유지), `commit -a` · `add -A` · `add -u` 는 하위 폴더에서도 저장소 전체를 센다 | `8a7880e` |
| HS-4 | 고침 — `silent-check` #2 · #3 패턴이 제목 다음 본문 줄까지 요구한다 | `ae4aeaf` |
| HS-5 | 고침 — 소비처 표에 빠진 다섯 행 + 새 스크립트 행 (인용 10 · 행 10 · 빠짐 0 · 남음 0) | `29c2eb4` |
| HS-6 | 고침 — `harness/scripts/extract-helpers.py` · `harness/scripts/measure-common.sh` · `harness/evals/measure/measure-helpers-test.sh`, CI harness 작업에 zsh 설치 뒤 시험 단계 | `29c2eb4` · `32d61cd` |
| CS-12 | 고침 — 커밋 안전 훅이 이 세션의 활성 계약 `# sprint-scope` 블록 밖 경로를 막는다. 규약 `contract-schema.md` §범위 목록 블록 신설, Step 6 이 가리킨다. 훅 설명 네 자리 갱신 | `8a7880e` |

「처리됨」 · 「바깥 근거 대기」 항목은 없다.

## 조건별 자기 측정 (끝 판 `32d61cd` 에서, 봉인 계약에서 뗀 도우미로)

측정 로그: `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/hs-impl/measure-all.log` (돌린 스크립트 `measure-all.sh` 같은 폴더)

| 조건 | 값 | 기대와 같음 |
| ---- | -- | ----------- |
| SK-01 | a=2 b=0 c=1 d=1 · 0 | 예 |
| SK-02 | 제목 1 · 아홉 글자 모두 ≥ 1 · Step 6 두 글자 1 · 1 | 예 |
| SK-03 | `^>` 1 · `^<` 0 · 두 경로 각 1 | 예 |
| SK-04 | (a) 0 · 2 (b) 1 (c) 0 · 1 (d) 0 · 1 | 예 |
| SC-01 · SC-02 | `A rc=0 root=proj hash=ok dup=none … session_id=sess-env renamed=5` · `B … session_id=sess-draft renamed=5` · `C rc=0 root=elsewhere warn=1` · `D rc=0 root=root2` · `E collect total=4 parse_failed=0 deterministic=4` | 예 |
| SC-03 | rc 0 · 마지막 줄 `=== ALL TESTS PASSED ===` · PASS 줄 contract_root 3 · draft_ 2 · HARNESS_CONTRACT 3 / 음성 대조 rc 1 · FAIL 1 | 예 |
| SC-04 | `race runs=12 fails=0 single_rc=0 home_left=0 fixed_tmp=0` | 예 |
| SC-05 | a1 · a2 · b1 · b2 · k0 `exit=2 삭제 60 개` · k1 0 · k2 `exit=2 되돌리는 파일 1 개` · k3 0 | 예 |
| SC-06 | 막음 여덟 exit 2 (`s13` names=[moved.txt]) · 통과 여덟 exit 0 | 예 |
| SC-07 | rc 0 · PASS 97 · FAIL 0 / 음성 대조(기준 판 훅) rc 1 · FAIL 12 | 예 |
| SC-08 | `orig rc=0` 셋 PASS · `empty rc=1 PASS #1 FAIL #2 FAIL #3` · `3 True True` | 예 |
| SC-09 | `cite=10 rows=10 missing=0 extra=0` · 여섯 행 각 1 | 예 |
| SC-10 | E1 · E2 · E3 기대대로 · 이 계약 자체 봉인 판 도우미 열하나 이름 같음 · cmp 차이 0 | 예 |
| SC-11 | M-bash · M-zsh 기대 줄 그대로 · `M3 same_as_schema=1 copies=0` | 예 |
| SC-12 | (a) rc 0 (b) zsh 줄 22 · 시험 줄 25 (c) actionlint 0 / 음성 대조 떼기 흉내 rc 1 · need_fn 뺀 사본 rc 1 | 예 |
| ER-01 | `E4 dup rc=1 files=0 named=1` · `E5 rc=3` · `E6 rc=2` · `E7 rc=2` · `M4 rc=2 names_fn=1` · `M5 rc=2` | 예 |
| ER-02 | s06 · s14 · s18 · s20 · s21 · s22 · s23 모두 exit 0 | 예 |
| AR-01 | 개정 커밋 뒤 끝 판 `3d3eeda` 에서 다시 잼: `block=17 changed=17 out_of_block=0 harness_other=0 commits=7 mixed_commits=0` · SEAL_OK · MEASURE_OK | 예 |
| AR-02 | 열둘 모두 rc 0 | 예 |
| AP-02 | **3** — 세 줄 모두 계약 자신의 글. 구현 경로만 재면 0 | **아니오 — 개정 AM-01 동의 대기** |
| AP-03 | `V6 code-fence 0 bare — OK` | 예 |
| AP-04 | `V1 frontmatter 9 skills + 1 agent — OK` | 예 |
| RE-01 | 공용 도우미 넷 `missing=[]` · 떼는 스크립트가 경로 인자만으로 이 계약에 돔 | 예 |
| RE-02 | `M3 same_as_schema=1 copies=0` · 기준 판 떼는 스크립트 0 개 | 예 |
| DG-01 · DG-03 | release.sh 교집합 0 | N/A 사유 참 |
| DG-02 | shellcheck 여섯 파일 끝 ≤ 기준(새 두 파일 0) · markdownlint 여덟 파일 끝 = 기준 · py_compile 0 · json 0 · actionlint 0 | 예 |
| DG-04 | 실행 진입점 0 | N/A 사유 참 |

## 로컬 CI

`ci-local.sh` (TMPDIR = 스크래치 `hs-impl/ci`) 요약 `…/hs-impl/ci/ci-local/summary.txt`: 스물여섯 단계 모두 rc 0, `feedback-agg-test` 는 yq 없음으로 건너뜀(원래 CI 와 같은 처리).
새 단계 `measure-helpers-test.sh` 는 ci-local 목록에 없어 따로 돌렸다 — rc 0.

## 킷별 버전 판단

- harness: **minor** (0.15.2 → 0.16.0) — 커밋 안전 훅이 새 조건(계약 범위 밖 경로)으로 막고, 새 스크립트 둘(`extract-helpers.py` · `measure-common.sh`)과 규약 새 절이 생겼다. 피드백 저장본 칸 모양도 바뀐다(`draft_*` 다섯 칸). 다른 묶음이 같은 킷을 올리면 부모가 합쳐 한 번만 올린다

## docs 드리프트

`python3 scripts/detect-docs-drift.py` 가 세 쌍을 냈다 — 원본이 바뀌어 페이지를 다시 만들어야 한다(이 묶음은 docs 묶음이 아니라 재생성하지 않았다):

- `harness/docs/guides/qa-evaluation-guide.md` → `docs/harness/qa-evaluation-guide.html`
- `harness/docs/guides/skill-design-guide.md` → `docs/harness/skill-design-guide.html`
- `harness/references/contract-schema.md` → `docs/harness/contract-schema.html`

## 톤 대조 (tone-kit:tone-guide 5 단계)

로드: core-comment · core-naming · core-structure · core-antipatterns · locale-korean (오버레이 `.claude/tone-project.md` — 어댑터 없음, 주석 한국어). 대상: 구간 `6378948..HEAD` 에서 `.harness/` 밖에 더한 606 줄.

| 규칙 | 건수 | 판정 |
| ---- | ---- | ---- |
| C-01 · C-02 (what 설명 · 이름 반복) | 0 | 통과 — 새 주석은 이유(되돌림 검사가 꺼짐 · 이름 바꾸기 뒤 숨음 · 고정 /tmp 충돌)를 적었다 |
| C-04 (템플릿 마커 · 구분선) | 0 | 통과 — 시험의 `# ── HS3 … ──` 는 같은 파일 기존 절 표시(`# ── SC-01 … ──`)를 따른 것 |
| C-07 (해설 3 줄 초과) | 0 | 통과 |
| C-10 · C-13 (툴 참조 · 자화자찬) | 0 | 통과 |
| C-15 (주석 종결형, 관측 컨벤션) | 0 | 통과 |
| N-07 (`effective*` · `resolved*`) | 0 | 통과 |
| N-08 (한 글자 이름, SHOULD) | 3 | 관례 유지 — `commit-guard-test.sh` 의 `r` · `n`, `commit-guard.sh` 의 `t`, 시험 안쪽 셸의 `d` 는 같은 파일 기존 이름을 그대로 따른 것(S-12). 새 이름을 들이지 않았다 |
| N-09 (무역할 파일명) | 0 | 통과 — `extract-helpers.py` · `measure-common.sh` 는 하는 일(떼기 · 측정)이 이름 앞에 있다 |
| S-03 · S-04 · S-06 (과분할 · 전달만 하는 래퍼 · 도우미 체인) | 0 | 통과 — `carried_paths` · `scope_blocks` · `check_scope` 는 각각 자기 일을 한다 |
| S-07 (발생하지 않는 방어 분기) | 0 | 통과 |
| K-02 (번역투 여섯 가지, G-1 grep) | 0 | 통과 |
| K-04 (`합니다`체) | 0 | 통과 |
| K-11 (새로 붙인 이름) | 0 | 통과 — 「범위 목록 블록」 은 계약이 정한 절 이름 |
| H (보존 주석) | — | 기존 주석 삭제 0 줄 (`save-feedback.sh` · `commit-guard.sh` 의 기존 이유 주석 그대로) |

## 측정 도구 경로

- 봉인 계약에서 뗀 도우미: `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/hs-impl/Ksealed/`
- 전체 측정 스크립트 · 로그: 같은 폴더 위 `hs-impl/measure-all.sh` · `hs-impl/measure-all.log`
- markdownlint: `…/scratchpad/hs/ml/node_modules/.bin/markdownlint-cli2` · 설정 `…/scratchpad/hs/ml/cfg.markdownlint-cli2.jsonc`
- 로컬 CI: `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh`

## 남은 것

1. AP-02 개정 AM-01 — 동의 받음(`a415f0a`), QA 3 회차가 세션 기록 3648 번째 줄 원문으로 다시 확인했다. 남은 일 없음
2. **이 notes 파일은 QA 뒤에 커밋했다** — AR-01 (b) 는 `.harness/` 안 변경을 계약 · 개정 · 피드백 셋으로 한정한다. 이 커밋 뒤 끝 판에서 AR-01 을 다시 재면 `harness_other=1` 이 나온다. 판정은 이 커밋 전 끝 판 `6b4c6d7` 기준이다
3. **docs 페이지 세 쌍 재생성 (독립 검토 결함 3, 막지 않음)** — `detect-docs-drift.py --since origin/main` 이 아직 세 쌍을 낸다. `docs/harness/qa-evaluation-guide.html:748` 은 「커밋 훅은 50 개를 넘는 삭제만 막는다」라고 적어 이제 틀렸다(원본 md 는 범위 목록 밖 경로도 막는다고 고쳤다). `docs/harness/*.html` 에 `sprint-scope` 0 건. 부모가 docs 묶음으로 모은다
4. 독립 검토 결함 1(막는 결함 — `-n` · `--dry-run` · `--ignore-removal` add 를 삭제 · 변경으로 셈)과 결함 2(HS-1 비고 `$CF` 빈 값)는 `6b4c6d7` 에서 고쳤다. 검토 재현 스크립트 `scratchpad/probe/p2.sh` 를 끝 판 훅으로 다시 돌려 세 경우 모두 rc=0 이다. 남은 일 없음
5. 다른 묶음과 겹칠 수 있는 파일: `harness/skills/sprint-contract/SKILL.md`(Step 6 한 줄 · Step 9 두 자리 다섯 줄) · `harness/references/contract-schema.md`(새 절 하나 · 한 줄) · `harness/docs/guides/qa-evaluation-guide.md` · `skill-design-guide.md` · `harness/agents/qa-evaluator.md`(각 한 줄) · `.github/workflows/ci.yml`(harness 작업 두 단계)
