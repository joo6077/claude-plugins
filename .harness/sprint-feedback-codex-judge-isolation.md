# Sprint Feedback
Feature: Codex 감독 판정 격리 · 용량 · 비용 · 속도 최적화
Evaluated: 2026-10-07 16:17
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-judge-isolation/.harness/sprint-contract-codex-judge-isolation.md
- sha256: 6d9005c50e9d335035cf5599812d6be924964192b7841387f7311647fe055745
- status: done (판정 전 active → 본 APPROVE 로 전환)
- slug: codex-judge-isolation
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-judge-isolation
- contract_root_unconfigured: false
- 선택 근거: 명시 경로(사용자가 절대경로로 지정)
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- measure_status: MEASURE_OK
- 재확인(Step 5): 일치
- status_transition: active -> done

## Codex 감독 모드
- `codex_audit.mode: off` (이 저장소). 사용자 지시에 따라 Codex 감독을 부르지 않고 평가자가 직접 25 조건을 판정했다.

## Amendments
- amendments: 4 (AM-01~AM-04, 사이드카 `.harness/sprint-amendments-codex-judge-isolation.md`)
- PASS 근거 가능: 4 — 전부 `direction=relaxing · consent=anchored`
  - AM-01: 판정 사본 경로를 `-C` 에서 읽기 (스크립트-02 · 스크립트-04 측정 바로잡기)
  - AM-02: 스크립트-02 샌드박스 확인을 판정과 같은 환경(TMPDIR · PATH)으로
  - AM-03: 진단-02 의 "더한 줄" 세기를 BASE 대비 바뀐 줄로 한정
  - AM-04: 계약 제목 줄 + 스크립트-01 줄 위 markdownlint 억제 주석 (서술 2줄, 봉인 그대로)
- PASS 근거 불가: 0
- 동의 앵커: prompt-log `35b5945f-...jsonl` 1643~1644행, 동의 시각 2026-10-07T06:59:22Z, cwd 일치. 직접 확인한 commit timeline(아래)과 상충 없음
- commit 선후 재확인(직접 git log 조회): 봉인 cd68799d(14:51:01) → 측정 수정 3a57447f(14:51:57)·33eb890c(14:57:45)·e091f39b(15:01:07, 모두 동의 전) → 동의 06:03:09Z=15:03:09 JST → 개정 문서 12ffced2(16:00:38)·a9783ffc(16:02:06, 모두 동의 후). 사이드카의 주장과 정확히 일치, 날짜 조작 없음

## User Correction Audit
- correction_log_status: available (부분 — `~/.claude/logs/claude-plugins/2026-10.md` 가 14:14:50 까지만 있고 계약 봉인(14:50)·동의(15:03) 이후 구간은 로그에 없음)
- 발견된 교정 1건: [2026-10-07T14:14:50 · session 35b5945f] "앙스트라는 빼 / 기본값을 꺼짐이 낫겟다 일단" — 계약·구현에 반영됨(모델 비교 6개에서 astra 제외, `mode: off` 기본값). 다만 `harness/templates/codex-audit/prices.json` 에는 `gpt-6-astra` 가격 항목이 여전히 남아 있어 "빼" 지시를 표 수준까지 반영했는지는 불명확 — Improvement 로 기록
- unreflected_corrections: 0 (verdict 영향 없음, 표면화만)

## Deletions
- deletions_range: fc9ab639..feat/codex-judge-isolation (git diff --diff-filter=D)
- 커밋 구간 삭제: 0
- 커밋하지 않은 삭제: 0
- 선언 밖 삭제: 0

## Results

### Script (12/12)
- [x] 스크립트-01 — PASS. `measure.sh 스크립트-01` 실행 결과 PASS, `--base` 로 돌리면 판정 차례에 `-s workspace-write` 가 남아 FAIL(exit 1) 직접 재현
- [x] 스크립트-02 — PASS. 실제 `codex sandbox -P codex-audit-judge --log-denials` 로 8칸 전부 기대값 일치, `--positive`(`:workspace` 만 둔 프로필)로 3칸 반전 확인, `--base` 로는 권한 프로필 자체가 없어 전부 FAIL(권한 프로필 부재로 모든 칸 `?`) 직접 재현
- [x] 스크립트-03 — PASS. `--base` 로 TMPDIR 미전달 FAIL 직접 재현
- [x] 스크립트-04 — PASS (4가지 경우: APPROVE·REJECT·시간초과·SIGTERM 전부 임시 폴더 0개, 판정 사본 소멸). `--positive`(도는 중 항목수≥1)·`--base`(keep=True 판 FAIL) 둘 다 직접 재현
- [x] 스크립트-05 — PASS. `--base` 로 재실행 금지 문장 부재 FAIL 직접 재현
- [x] 스크립트-06 — PASS. 0.49달러 계산(손으로 검증: (100,000×2.00+900,000×0.10+20,000×10.00)/1e6=0.49) 일치, 단가 모름 모델 처리 확인. `--base` FAIL 직접 재현
- [x] 스크립트-07 — PASS. 오늘/이번달/저장소별 합계 전부 일치
- [x] 스크립트-08 — PASS (상한 넘음·아래·미설정 3경우). `--base` FAIL 직접 재현
- [x] 스크립트-09 — PASS (시간초과 1회 호출·빈응답 2회 호출·기본 1500초). `--base` FAIL 직접 재현
- [x] 스크립트-10 — PASS (세션 기록 `.jsonl.gz` 압축, 풀면 turn_context 확인)
- [x] 스크립트-11 — PASS (`CODEX_AUDIT_MODEL` 전파, 미설정시 project.yaml model)
- [x] 스크립트-12 — PASS (칸 없음/모드 없음 6경우 전부 SKIPPED+exit 3, `mode: codex` 는 정상 호출). `--base` FAIL 직접 재현

### Error (2/2)
- [x] 오류-01 — PASS (권한 프로필 미지원시 BLOCKED·설정-오류, judge 호출 0번)
- [x] 오류-02 — PASS (깨진 JSON·문자열 달러 줄 2개 무시, traceback 없음, "못 읽은 줄 2" 출력)

### Skill (1/1)
- [x] 스킬-01 — PASS. README/SKILL.md/qa-evaluator.md/project.yaml 틀 4파일 전부 지정 낱말 포함 확인

### Architecture (2/2)
- [x] 구조-01 — PASS. 실제 바뀐 경로 8개 전부 sprint-scope 부분집합, codex-audit.sh 포함 확인
- [x] 구조-02 — PASS. prices.json 6모델 단가가 배경 근거값과 정확히 일치, codex-audit.sh 더한 줄에 단가 숫자 리터럴 없음(load_prices() 로 외부 파일 참조)

### Anti-patterns (2/2)
- [x] 금지-03 — PASS (`validate-plugin.py harness --check=code-fence` exit 0)
- [x] 금지-04 — PASS (`validate-plugin.py harness --check=frontmatter` exit 0)

### Reusability (2/2)
- [x] 재사용-01 — PASS (`codex-audit-usage.jsonl`·`prices.json` 이름이 각 1곳)
- [x] 재사용-02 — PASS (`tempfile.mkdtemp` 호출 자리 수 BASE 이하로 유지, `cleanup()`·`ACTIVE` 그대로 재사용 — 직접 grep 대조: BASE 2곳·HEAD 2곳)

### Diagnostics (4/4, N/A 2건 포함)
- [x] 진단-01 — N/A 타당성 확인(진단-04 가 `bash -n codex-audit.sh`·`validate-plugin.py harness` 를 실제로 실행해 묶어서 쟀음을 확인)
- [x] 진단-02 — PASS (더한 줄 markdownlint 경고 0, `--positive` 로 MD013 켜면 35·130·218·50건 — 검사가 살아있음을 확인)
- [x] 진단-03 — N/A 타당성 확인(진단-04 가 측정 묶음 전체 실행의 Traceback 0 을 실제로 쟀음을 확인)
- [x] 진단-04 — PASS (`bash -n` 0, `validate-plugin.py harness` 0, 측정 묶음 전체 20/20 PASS, 로컬 CI 명령 34개 전부 실패 0 — 전부 직접 재실행하여 확인)

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: 25/25 = 1.00
- Verdict 영향: 통상 (전부 실측 통과)

## Discrimination (규칙 12 적용 조건)
- 적용 조건: 스크립트-02(보안 경계 — 권한 프로필 읽기/쓰기/네트워크 차단), 스크립트-04(동시성/중단 처리 — SIGTERM 중 정리)
- 결합 확인: 스크립트-02 — 측정이 실제 `codex sandbox -P` 바이너리로 실제 구현이 생성한 config.toml 을 검증(모의 재구현 아님). 스크립트-04 — 실제 `codex-audit.sh` 프로세스에 SIGTERM 을 보내 실제 cleanup()/TEMP_ROOT 경로를 검증
- 음성 대조: 스크립트-02 — 계약에 기재 없음(양성 대조만 있음) → 계약 결함으로 기록(Improvement). 단, 평가자가 직접 `--base` 로 돌려 권한 프로필 부재로 전부 FAIL 하는 것을 확인함(아래 Evidence Validity 참조). 스크립트-04 — 계약에 기재 있음, `--base` 로 직접 FAIL(남은 항목) 재현

## Check Artifacts
- 해당 없음 — 이번 스프린트의 산출물은 "검사 대상 코드"(codex-audit.sh)이지 "검사 스크립트 자체"가 아니다. 다만 measure.py 자체도 산출물이므로 다섯 항목을 간단히 적용: ① 해당 없음(단일 대상 구조, 다중 칸 구조 아님) ② 실행 목록: `measure.sh all --skip 진단-04` 로 20개 함수 전부 TABLE 에 등록되어 실행됨을 출력으로 확인 ③ 해당 없음(한 조건 실패가 다른 조건 실행을 막지 않음, run_one 이 예외를 개별적으로 삼킴) ④ 셸: measure.sh 자체는 python3 호출이라 셸 무관, 해당 없음(고정 해석기) ⑤ 효과 증명: 8개 조건에서 `--base` 로 알려진 결함(옛 구현) 투입 시 전부 FAIL 재현, 2개 조건에서 `--positive` 로 느슨한 입력 투입 시 기대대로 반전 — 완료

## Evidence Validity
- 검사 대상 증거: 25건 (23건 measure.sh 실행 + 2건 validate-plugin.py 실행)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 해당 없음(이번 산출물에 사용자가 복붙할 셸 스니펫 문서는 없음 — codex-audit.sh 는 실행형 스크립트고 전부 실제로 실행해 확인함)
- 양성 대조: 스크립트-02(임시 사본, `:workspace` 만 둔 프로필로 3칸 반전 확인) · 진단-02(MD013 켜서 35·130·218·50건 확인)
- 추가 직접 확인(계약 기재 이상의 자발적 음성 대조): 스크립트-02 `--base` 직접 실행 → 전체 FAIL(권한 프로필 부재로 8칸 전부 `?`), 커밋 타임라인(git log) 으로 개정 사이드카의 선후 주장 전부 대조 확인

## Diff 전수 검토 (측정 조건 밖 — 코드 가독)
- `harness/scripts/codex-audit.sh` BASE..HEAD 전체(+247/-49 줄)를 직접 읽고 아래를 확인:
  - 하루 상한(`check_budget`)은 `run()` 에서 모든 Codex 유상 호출(draft/revise/impl) 전에 실행되고, `models` 서브명령(무상 HTTP 조회)만 우회 가능 — 의도된 설계, 우회 아님
  - 임시 폴더는 `TEMP_ROOT` 단일 루트로 통합되고 `finally: cleanup()` 이 정상/예외/신호 종료 모두에서 rmtree — 코드 추적으로 리크 경로 없음 확인(스크립트-04 실측과 일치)
  - 권한 프로필(`judge_profile`)의 읽기 허용 목록은 `PATH` 각 항목(존재하는 디렉터리만) + python3/node/git/bash 설치 경로 + 고정 4경로(`/opt/homebrew` 등, 배경에 문서화됨). 이 머신에서 실제로 계산해보니 전부 좁은 bin/설치 디렉터리이고 홈 전체나 공유 폴더 같은 과도하게 넓은 경로는 없음. `/opt/homebrew` 전체 읽기는 의도적으로 넓은 편이나 배경 섹션에 명시되어 있어 숨겨진 확장이 아님
- **발견 1 (경미, FAIL 아님)**: `harness/templates/codex-audit/prices.json` 에 비교 대상 6모델 외 `gpt-6-astra` 가격 항목이 남아 있다. 사용자가 14:14:50 에 "앙스트라는 빼" 라고 명시했고, 계약은 "모델 비교에서 제외"로 좁게 반영했지만 가격 표 자체에서는 안 뺐다. 어느 조건도 이를 FAIL 로 잡지 않음(구조-02 는 6모델 존재만 확인, 전체 키 집합은 안 봄) — Improvement 로 기록
- **발견 2 (경미, FAIL 아님)**: 같은 `codex_home`(공유 Codex 계정)을 여러 저장소가 동시에 쓸 때 `check_budget` 은 호출 시점 스냅샷 비교라 두 세션이 거의 동시에 상한 미만임을 확인하고 둘 다 호출을 진행하면 합산 지출이 상한을 넘을 수 있는 경쟁 상태가 이론상 있다. 계약 범위("동시 모델 판정은 다음 단계")가 명시적으로 동시성 보장을 요구하지 않고, 측정도 단일 호출 순차 시나리오만 다루므로 FAIL 대상 아님 — 향후 하드닝 메모로 기록

## Summary
- Total: 25/25 conditions passed
- Verdict: APPROVE

## Improvement Suggestions
- [구조-02] 측정-방식-불일치 — `prices.json` 에 사용자가 명시적으로 제외를 요구한 `gpt-6-astra` 가격 항목이 남아있다. 구조-02 조건에 "6모델 외 키가 없다" 는 전수 검사를 추가하거나, astra 항목을 표에서 제거할 것
- [스크립트-02] 측정-판별력-미기재 — 음성 대조 절이 없다. 이번 평가에서 `--base` 로 직접 돌려 권한 프로필 부재로 8칸 전부 FAIL 하는 것을 확인했으므로 그 결과를 조건에 음성 대조로 추가할 것
