# c4b — 킷 reviewer 일곱의 미검증 규칙을 평가 가이드 새 판으로

- 작업 폴더: `.claude/worktrees/ak-c4b` (가지 `chore/ak-c4b`, 시작 판 `f81568d`)
- 계약: `.harness/sprint-contract-after-0924-reviewer-unverified.md` — 23 조건, 봉인값 `sha256:3da851e5d1e58f0e` (2026-09-26 17:02)
- 계약 피드백: `~/.harness/feedback/contract/1a3bcba6-2026-09-26T170324-bda55d45-83561.yaml` (`verify-feedback.sh` PASS)
- QA 판정은 아직 없다. 다음 단계의 qa-evaluator 가 낸다. 계약 `status` 는 `active` 그대로다

## 한 일

| 커밋 | 내용 |
| ---- | ---- |
| `fa00350` | 계약 봉인 — 계약 파일 하나만 |
| `2b82945` | api-kit — api-reviewer 사본을 원문 v5.1 글자 그대로, 판정에 `BLOCKED` · 두 카운터 |
| `7b1af2c` | backend-kit — backend-reviewer 사본 교체(낱말 바꿔 옮긴 4 요건을 원문대로), 판정 순서 목록, backend-audit APPROVE 빈틈 |
| `09a0cde` | design-kit — design-reviewer 규칙 8 사본 교체 · 판정 규칙에 `BLOCKED`, design-audit Gotcha 11 · Step 5, 시험 파일 한 줄 |
| `9ef4614` | infra-kit — infra-reviewer §9 사본 교체(N/A 구분표 · DG 조항이 새로 들어감) |
| `a463cb8` | planning-kit — planning-reviewer 사본 교체, `reason:` 에 N/A 사유 칸, `[미검증]` 축에 보류, plan-audit 맞춤 |
| `446428a` | react-kit — react-reviewer 사본 교체, 판정값 `APPROVE` · `REJECT` · `BLOCKED`, react-audit 리포트 틀과 MUST 줄 |
| `ff22740` | rust-kit — rust-reviewer 사본 교체(「옮기지 않았다」 메모 삭제), rust-reviewer · rust-audit APPROVE 빈틈 |
| `8b27b36` | 킷 밖 — `scripts/check-reviewer-protocol-copies.py` 새 검사, CI `validate` 묶음 한 단계, infra-kaizen Gotcha 8 원문 행 |

사본마다 원문 두 덩어리(조항 47 줄 · 4 요건 7 줄)를 글자 그대로 넣고, 앞뒤를 MD029 끄기 · 켜기 주석으로 감쌌다.
출처 줄 하나에 원문 경로 · `v5.1` · 「계약」 풀이를 함께 적었다. 사본 밖의 「조항 2」 · 「조항 3」 · 「3 분기」 표기는
조항 첫머리 글(「`[미검증]` 은 검증 도구·환경 부재 전용이며」 조항 · 「임계값 2 는」 조항)로 바꿨다.

backend · rust 감사의 APPROVE 조건이 「전 row PASS」 라 `[미검증:ENV]` 가 하나라도 있으면 어느 판정에도 걸리지 않던 빈틈은,
네 판정 조건을 서로 겹치지 않게 다시 적어 메웠다(FAIL 0 + `invalid_evidence` 0 · 1 + 비율 0.60 이상 / 2 건 이상 / 비율 0.60 미만).

## 교차 진단 반영 (봉인 전)

| 지적 | 반영 |
| ---- | ---- |
| AR-01 이 history 포함이라 적고 `sprint-contract*.md` 로 재 104 개를 빠뜨렸다 | `*sprint-contract*.md` 로 넓히고 잰 파일 수 `seals` 를 출력에 넣었다. 시작 판 186 · 끝 판 187, `SEAL_BROKEN` 0 |
| SK-03 이 「조항 3」 을 안 쟀다 | `scan.py` 에 `num3_ref` 를 더했다. reviewer 사본 밖은 0 을 요구, 시작 판 6 곳이 양성 대조. 감사 스킬 셋의 「정본 조항 3」 은 넘김이라 SK-06 은 거른다 |
| 범위 밖 다섯 파일 | 넷은 만드는 쪽 「부분 완료」 규칙이라 정본 `skill-design-guide.md:308` 과 맞다(고치지 않음). flutter-audit 옛 사본 하나는 넘김 |
| SK-01 출처 줄 한 줄 요구 | 세 낱말은 한 줄에 함께 두고 이어 쓴 줄에는 한꺼번에 넣지 않는다고 조건에 적었다 |
| SK-03 (a) 순우리말만 쓴 임계 줄 | 새 임계 줄에도 `invalid_evidence` · `INVALID` 이름을 같은 줄에 적게 했다 |
| SK-05 · SK-07 태그 | 양면 조건은 `[exact, enumerated]` 여야 한다는 규칙(contract-schema §Counterpart 조건)을 들어 그대로 두고 이유를 범위 경계에 적었다 |
| RE-02 음성 대조 없음 | 예행 `rh/badre` 에서 `plugin_utils=0 guide_path=0 canon_text=1` 을 실측했다 |

## 조건별 자기 측정 (끝 판 `8b27b36`, 계약 `m.sh`)

| 조건 | 잰 값 | 기대와 같은가 |
| ---- | ----- | ------------- |
| SK-01 | `files=7 a1=7 b1=7 prov1=7 base_a1=0 base_b1=0 guide=[a=1 b=1]` · `a_lines=47` · `b_lines=7` | 같다 |
| SK-02 | `rust-kit=0/1 backend-kit=0/1 infra-kit=0/1` | 같다 |
| SK-03 | `old_thr=0 num_ref=0 num3_ref=0 three_way=0 gate_ok=7 env_ok=7 invalid_ok=7 base_old_thr=20 base_num_ref=9 base_num3_ref=6 base_three_way=7 base_gate_ok=3`, `HIT` 0 | 같다 |
| SK-04 | `reason_lines=1 reason_na=1 base_reason_na=0` | 같다 |
| SK-05 | `files=7 scenarios=4 cases_total=28 labels_ok=7/7`, `LABEL_MISSING` 0 (칸 판정은 QA 몫) | 보조 측정 같다 |
| SK-06 | `old_thr=0 num_ref=0 three_way=0 skills_with_gate=6/6 infra_audit=same api_skills_citing_reviewer=0 base_old_thr=6 base_num_ref=1 base_three_way=1`, `HIT` 0 | 같다 |
| SK-07 | `files=6 scenarios=4 cases_total=24 labels_ok=6/6`, `LABEL_MISSING` 0 (칸 판정은 QA 몫) | 보조 측정 같다 |
| SK-08 | `rows=1 req4=1 script=1 base_req4=0 base_script=0` | 같다 |
| SK-09 | `added_lines=132 g1_hits=0 canon_g1=1` | 같다 |
| SC-00 | `release_paths=0` | 같다 |
| ER-01 | `end_rc=0 end_ok=7 end_excluded=1 end_stderr_bytes=0 base_rc=1 base_mismatch=7 mut_rc=1 mut_mismatch=1 mut_react=1 mut_ok=6` | 같다 |
| ER-02 | `guide_rc=2 del_mut_applied=1 del_rc=2 del_missing=1 del_mismatch=1 extra_rc=1 extra_unlisted=1 cwd_root_rc=0 cwd_root_ok=7` | 같다 |
| AR-01 | `impl_files=16 exact=1 mixed_commits=0 seal_commit_files=1 seal_before_impl=1 seals=187 seal_broken=0 this=SEAL_OK scope_block=1` | 같다 (이 notes 커밋 전 측정) |
| AR-02 | `in_validate=1 in_file=1 actionlint_end=0 base_in_file=0 actionlint_base=0` | 같다 |
| AP-03 | 킷 일곱 모두 `0` | 같다 |
| AP-04 | `files=12 name=12 fm_same=12` | 같다 |
| RE-01 | `added=1 script=1` | 같다 |
| RE-02 | `plugin_utils=1 guide_path=2 canon_text=0` | 같다 |
| DG-01 · DG-03 | `release_sh=0` | 같다 |
| DG-02 | `md=13 base_warn=204 end_warn=203 worse=0 py_compile=0 json=0` | 같다 |
| DG-04 | `rc=0 stderr_bytes=0 traceback=0` | 같다 |
| DG-05 | 시작 판 · 끝 판 모두 0, 시작 판 `copies=absent` · 끝 판 `copies=0` | 같다 |

측정 파일은 계약에서 떼어 스크래치 `c4b-impl/k-final/` 에 두었고, 전체 출력은 `c4b-impl/measure.out` 이다
(스크래치 뿌리 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/`).

## 로컬 CI

`TMPDIR=<스크래치>/c4b-impl/citmp bash .harness/handoff/2026-09-26-tools/ci-local.sh <작업 폴더>` — 22 단계 `rc=0`,
`feedback-agg-test` 는 이 맥에 `yq` 가 없어 건너뜀(시작 판과 같은 조건). ci-local 이 모르는 새 단계
`python3 scripts/check-reviewer-protocol-copies.py` 는 따로 돌려 `checked=7 violations=0 infra_errors=0 excluded=1` · 종료 코드 0.
킷마다 `validate-plugin.py` 0 · `sync-docs.py --check-only` 0(바뀐 README 없음) · `sync-evals.py --check-only` 0 · `actionlint` 0.
ci-local 이 남긴 `__pycache__` 두 폴더는 지웠다.

## docs 드리프트

`python3 scripts/detect-docs-drift.py --since f81568d8fbf58382172281388ec5d7756f9f46b2 --verbose` → `No docs drift`.
바꾼 파일은 에이전트 · 스킬 · 시험 · 스크립트뿐이라 문서 사이트 원본(`harness/docs/guides` 등)에 닿지 않는다.

## 넘긴 것

- 원문 `qa-evaluation-guide.md` 의 조항 번호 겹침(3 이 둘) · 머리말 「5 조항」 · 「현재 drift」 문단 — 원문은 범위 밖, C2 · 다음 사이클 Phase 3.
  backend-audit · rust-audit · infra-audit 의 「정본 조항 3」 과 `react-kit/references/render-evidence-protocol.md:205` 의 「정본 조항 3」 도 그때 함께 본다
- `flutter-toolkit/skills/flutter-audit/SKILL.md:32-49` 의 옛 다섯 조항 사본 — reviewer 일곱 밖, 다음 사이클 Phase 5
- `howto-kit/agents/howto-reviewer.md` — 새 검사가 이유와 함께 `EXCLUDED` 로 출력한다. 다음 사이클 Phase 17
- design-reviewer 의 「미검증 0 건 · L3 10 개 미만 → CONDITIONAL APPROVE」 — design-kit 고유 L3 규칙이라 다음 사이클 Phase 6
- `docs/harness/*.html` 세 쪽의 옛 문턱 설명, `harness/evals/gate-exit-codes.md` 사용처 표에 새 검사 행 — 범위 밖
- `validate-plugin.py` 에 넣지 않고 따로 둔 까닭: 등록 검사 수가 문서 여러 곳에 적혀 있어 범위 밖 문서까지 고쳐야 한다

## 킷별 버전 판단 (릴리스는 부모가 PR 을 합친 뒤)

| 킷 | 지금 | 판단 | 이유 |
| -- | ---- | ---- | ---- |
| api-kit | 0.2.0 | minor | reviewer 판정에 `BLOCKED` 가 새로 생기고, 도구 부재(`[미검증:ENV]`)가 더는 불합격 셈에 들지 않는다 |
| design-kit | 0.5.0 | minor | 같은 이유 — reviewer · design-audit 판정에 `BLOCKED`, 불합격 문턱이 `invalid_evidence` 만 센다 |
| planning-kit | 0.6.0 | minor | 같은 이유 — `[미검증]` 축에 `BLOCKED`, N/A 사유 칸 |
| react-kit | 0.4.0 | minor | 판정값이 둘에서 셋(`BLOCKED`)으로, react-audit 리포트 틀도 바뀐다 |
| backend-kit | 0.4.0 | patch | 두 카운터 · `BLOCKED` 는 이미 있었다. 사본 글자 맞춤과 APPROVE 빈틈 메움이다 |
| rust-kit | 0.4.0 | patch | backend 와 같다 |
| infra-kit | 0.4.0 | patch | 판정 규칙은 그대로이고 사본 글자만 원문과 같아졌다 |

harness 는 고치지 않았다(`.claude/skills/infra-kaizen` · `scripts/` · `.github/` 는 킷 밖).

## 함께 도는 묶음과 부딪힐 자리

- `chore/ak-c4c` 가 `rust-kit/skills/rust-audit/SKILL.md` 의 다른 줄을 고친다. 이 묶음은 `## 5. 최종 판정` 안 네 줄만 바꿨다
- `chore/ak-c1-harness-scripts` 가 `.github/workflows/ci.yml` 에 다른 단계를 더한다. 이 묶음은 `Stale value check` 바로 뒤에 네 줄을 넣었다

## 톤 대조 (tone-kit:tone-guide 5 단계)

1 단계에서 `.claude/tone-project.md`(어댑터 없음 · 주석 언어 ko)와 코어 네 파일 · `locale-korean.md` 를 읽었다. 어댑터가 없어 스택 고유 대조 목록은 돌리지 않았다.

| 규칙 | 건수 | 판정 |
| ---- | ---- | ---- |
| C-01 · C-02 (what 대신 why, 이름 반복 금지) | 새 스크립트 주석 1 줄 · docstring 2 개 | 통과 — `EXCLUDED` 주석은 이유가 출력에 나간다는 제약, `canonical_blocks` docstring 은 못 찾으면 빈 목록이라는 약속 |
| C-04 · F (구분선) | 0 | 통과 — `#` 뒤 `-=_*~` 4 개 이상 grep. 같은 식이 `# ----------` 사본에서 1 을 냈다 |
| C-13 (자화자찬) | 0 | 통과 — 양성 대조 1 |
| C-14 (파일 헤더) | 1 | 통과 — 스크립트 첫 docstring 관례(오버레이), `check-stale-values.py` 와 같은 틀 |
| N-07 (`effective*` · `resolved*`) | 0 | 통과 |
| N-08 (한 글자 이름) | 0 | 통과 — 같은 식이 스크래치 `impl.py` 에서 22 를 냈다 |
| N-09 (무역할 파일명) | 0 | 통과 — `check-reviewer-protocol-copies.py` |
| S-03 · S-04 (의미 없는 추출 · 전달만 하는 함수) | 0 | 통과 — `normalized` · `canonical_blocks` · `contains_block` 모두 자기 일이 있다 |
| S-06 (헬퍼가 헬퍼를 부름, 관측 컨벤션) | 0 | 통과 — 세 함수 모두 `main` 만 부른다 |
| S-12 (같은 역할 같은 패턴, 관측 컨벤션) | — | 통과 — `scripts/check-*.py` 처럼 docstring · 상수 · `main` · `sys.exit(main())` |
| H (보존할 주석) | 2 | 이동 — backend · rust 의 「재동기화」 메모는 사본이 원문과 같아져 사실과 달라졌고, 그 실패 모드(사본이 원문을 못 따라감)는 새 검사 docstring 과 CI 주석이 들고 있다 |
| K-02 (번역투 여섯, locale-korean §8 G-1) | 0 | 통과 — 시작 판 → 끝 판에서 `.harness/` 밖에 더한 줄 636 줄 중 적중 4 줄은 모두 새로 사본을 넣은 네 파일(api · design · planning · react)의 원문 「임계값 2 는」 조항 첫 줄이다(글자 그대로 옮긴 줄). 사본 밖 0, `SK-09 g1_hits=0` |
| K-04 (한다체) · G-2 (`합니다` 체) | 0 | 통과 |
| K-11 (새로 만든 이름, 관측 컨벤션) | 0 | 통과 — `verified_coverage` · `invalid_evidence` · `env_gaps` 는 원문 이름, 「사본」 · 「덩어리」 는 일상어 |

meta-audit: 로드한 규칙 가운데 C-06(공개 API doc)은 새 스크립트에 공개 API 가 없어 해당 없음. 범위 밖 파일은 건드리지 않았다.
