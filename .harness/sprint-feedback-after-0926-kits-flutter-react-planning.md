# Sprint Feedback
Feature: 킷 남은 것 — flutter-toolkit · react-kit · planning-kit (카이젠 뒤 이어질 것 2026-09-26 두 번째 묶음 k1)
Evaluated: 2026-09-26 22:07
Verdict: APPROVE
Iteration: 2

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-k1/.harness/sprint-contract-after-0926-kits-flutter-react-planning.md
- sha256(조건 줄 전용, contract_digest): sha256:534198c0775e068c — measurement_digest: sha256:e957eecfbfa776f5
- status: active (봉인 값 그대로, Step 5.5 에서 done 전환)
- slug: after-0926-kits-flutter-react-planning
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-k1
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (HARNESS_CONTRACT 로 지정, test -f 확인 후 사용)
- legacy_contract_used: false
- seal_status: SEAL_OK — MEASURE_OK (evaluator 독립 재계산, contract-schema 0.15.2 sha256_16/contract_digest/verify_seal/measurement_digest 함수 그대로 적용)
- 봉인 커밋: 6d073dd (계약 파일 단독 1개, `git show --name-only` 확인). 봉인 커밋 대조(1-e-3): 산문 차이 없음(frontmatter status 전환만 필터됨), conditions_digest 차이 없음 → 재봉인 없음
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (아래 수행 직전 재확인 예정)
- status_transition: active -> done (본 리포트 저장 직후 수행)

## 참고 — 왜 Iteration 2인가
가지 `chore/ak2-k1` 는 두 차례 평가를 거쳤다. 1 차(끝점 `e4f63d8`)에서 별도 검토가 여섯 건(그중 1 건은 판정을 바꿀 만한 결함 — `project-detection.md` 의 「시험이 11 키를 지킨다」 는 허위 서술)을 찾아 REJECT 로 처리됐고(`.harness/.meta/after-kaizen-0926b/k1-notes.md` §「QA 1 차 REJECT 뒤 고친 것」), 구현자가 다섯 건을 고쳐 커밋 `729c110`·`899d2ab`·`7c51d87`·`1ea990c` 로 가지 끝을 옮겼다. 이 세션에 남아있던 `.harness/sprint-feedback-*.md`(iteration 1, verdict APPROVE)는 그 REJECT 이전 시점(끝점 `e4f63d8`)의 산출물로 — 이번 평가는 그 파일을 근거로 쓰지 않고 끝점 `1ea990c` 에서 29 조건을 처음부터 다시 정적·실행 검증했다.

## Amendments
- amendments: 0 (사이드카 `.harness/sprint-amendments-after-0926-kits-flutter-react-planning.md` 부재 확인)

## User Correction Audit
- correction_log_status: available 가능성 높음(전 iteration 확인) — 이번 재평가는 계약·구현 diff 재검증에 집중했으며 correction log 재대조는 전 iteration 결과(unreflected_corrections: 0)를 유지. verdict 영향 없음(표면화 전용)

## Deletions
- deletions_range: 6378948..1ea990c (계약 시작점 → 가지 끝, evaluator 재계산)
- 커밋 구간 삭제: 0 (`git diff --no-renames --name-status --diff-filter=D` 빈 출력)
- 커밋하지 않은 삭제: 0 (`git status --porcelain --no-renames | grep -E '^(D.|.D) '` 없음)
- 선언 밖 삭제: 0

## Cross-Diagnosis Handoff
- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-k1/.harness/sprint-contract-after-0926-kits-flutter-react-planning.md` · 이 판정 결과 전문
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가? — 특히 SK-11/SK-13: react-animation·plan-sync-github 의 머리를 `# Gotchas`→`## Gotchas` 로 낮춘 처리를 PASS 근거로 삼았다. 조건 문장이 문자 그대로 「`## Gotchas` 절에」 를 요구하므로 리터럴 해석상 PASS 이나, planning-kit 12 스킬 중 plan-sync-github 만 머리 모양이 달라지는 부수효과가 있다(계약 조건이 직접 재지 않는 스타일 일관성 문제). 이 처리를 최종 승인할지 재확인 요청
  2. 0 건·빈 출력을 근거로 PASS 한 조건 중, 문제가 있어도 0 을 냈을 측정(공허한 통과)이 있는가? — SC-00/RE-01/DG-01/DG-03 의 0 값은 evaluator 가 측정 명령을 직접 재실행해 확인(대상 파일이 diff 범위에 없음을 재확인). DG-05 는 evaluator 가 working tree 를 커밋 상태로 복원(아래 설명) 후 ci-local.sh 를 처음부터 끝까지 직접 실행해 25 rc=0 + SKIP 1 을 재현했다
- 부모가 교차 진단을 마친 뒤 `cross_diagnosis_by` 를 `sprint-contract` 로 갱신한다

## 평가 절차 특기사항 — working tree 복원
평가 시작 시 `.harness/sprint-contract-after-0926-kits-flutter-react-planning.md` 에 `status: active -> done` 미커밋 변경(이전 iteration 1 평가의 Step 5.5 잔여물로 추정)이 남아 있어 `git status --porcelain --untracked-files=no` 가 비어있지 않았다. DG-05 의 Given 전제(working tree clean)를 충족하려고 `git checkout -- <그 파일>` 로 커밋 상태(`status: active`)로 복원한 뒤 전 조건을 재검증했다. 구현자 작업물은 전혀 건드리지 않았다 — 되돌린 것은 평가자 자신의 이전 산출물뿐이다.

## Results

### Skill (16/16)
- [x] SK-01: flutter-audit 미검증 규칙 사본이 원문 v5.1 과 같다 — PASS
  - 근거: evaluator 독립 실행(계약 측정 도우미, `scripts/check-reviewer-protocol-copies.py` 의 `canonical_blocks`/`contains_block` 그대로 사용) `clauses=1 req=1 prov=1 old=0 md029=1/1`. `flutter-toolkit/skills/flutter-audit/SKILL.md:34-97` Read 로 react-reviewer.md:169-178 과 문자 대조(`diff` 로 일치 확인). L3.
- [x] SK-02: flutter-audit 자기 규칙·보고 틀이 v5.1 두 카운터를 쓴다 — PASS
  - 근거: evaluator 독립 실행 `env_gaps=6 invalid=7 rep_env=1 rep_inv=1 rule_old=0 rule_inv=1 l3_4req=1`. `SKILL.md:465,469,470,484` Read 로 `Total: N errors, N warnings | env_gaps N · invalid_evidence N`·결론 줄·Rules MUST 줄 확인. L3.
- [x] SK-03: 「관례 표 없는 호출」 평가 사례 추가 — PASS
  - 근거: evaluator 독립 실행 `cases=24 ids_ok=1 skip_case=1 case16_same=1`. `python3 scripts/run-evals.py flutter-toolkit` 을 evaluator 가 현재 작업 폴더(HEAD=1ea990c)에서 직접 실행 → `Total: 24 passed, 0 failed` 종료 코드 0. 사례 24 전문을 Read 로 확인(agent=widget-inspector, 프롬프트 「관례 표 없는 호출」, 단언 5개 중 「건너뜀 — 관례 표 없는 호출」 포함). L3.
- [x] SK-04: 루트 CLAUDE.md 평가 사례 수 두 문장 일치 — PASS
  - 근거: evaluator 독립 실행 `cases=24 commands=24개 conventions=24개`. `CLAUDE.md:52,373` Read 로 직접 확인. L3.
- [x] SK-05: flutter-kaizen Gotchas 에 Makefile 규칙 넷 교훈 — PASS
  - 근거: `flutter-toolkit/skills/flutter-kaizen/SKILL.md:36` Read — 4파일명(flutter-preflight·flutter-run·flutter-ai-rules·project-detection)·Step 2b·허용 경로 모두 포함. 측정값 1. L3.
- [x] SK-06: codegen 안내 셋이 flutter-run 전후 삭제 수 블록을 가리킨다 — PASS
  - 근거: evaluator 독립 실행 `api=1 feature=1 screen=1`. `flutter-api/SKILL.md`·`flutter-feature/SKILL.md:7`(`### 4. codegen 안내` 절 「flutter-run 스킬 ### codegen [feature] 절처럼 전후 삭제 수를 세어」)·`flutter-screen/SKILL.md` Read 확인. L3.
- [x] SK-07: 평가 사례 18 실행 단언이 flutter-test Step 4 와 같다 — PASS
  - 근거: `flutter-toolkit/evals/evals.json` 사례 18 Read — `$FLUTTER test` 단언 존재, 옛 `$DART test로 검증한다` 단언 없음. 측정 `flutter_test=1 dart_verify=0 skill=flutter-test`. L3.
- [x] SK-08: build_runner Gotcha 가 EX-5 대로, 플래그는 명령에 그대로 — PASS
  - 근거: evaluator 독립 실행 `old216=0 joined=1 flags=[2/2 2/2 2/2]`(시작 판과 플래그 줄 수 동일). Gotcha Read — `2.16`·`2.7.0`·`빼지 않는다`·`build_runner_command_line.dart` 한 줄에 모두 포함, 옛 문구 없음. L3.
- [x] SK-09: flutter-preflight `## 실패 원인 가르기` 절 — PASS
  - 근거: evaluator 독립 실행 `sec=24 prov=1 rows=5/5 merge_base=2 wt=1 prep=2`. 절 전문 Read, `harness/skills/sprint/SKILL.md` Step 3 판정 표 5행과 문자 대조(정확히 일치, grep -E 로 재확인). L3.
- [x] SK-10: react-preflight 동일 절 — PASS
  - 근거: evaluator 독립 실행 `sec=24 prov=1 rows=5/5 merge_base=2 wt=1 prep=2`. `react-kit/skills/react-preflight/SKILL.md` 절 전문 Read 확인. L3.
- [x] SK-11: react-animation·animation-architect-react 가 React 19.3 `<ViewTransition>` 반영 — PASS
  - 근거: evaluator 독립 실행 `gotcha=1 wrapper=6/8 agent=1`(w=8≥6 요건 충족, wrapper 등장 수가 시작 판 6 이상으로 유지). Gotcha 15 전문 Read(안정 API·19.3·startTransition·원문 URL 모두 기재). Tier 표 T2 칸에 두 경로(`withViewTransition` 래퍼·`<ViewTransition>`) 명시 확인(SK-16 관련 §3.4·§5.1 추가분과 함께 L3 의미 추적 — §5.1 에 `<ViewTransition>` 경로가 래퍼 가드를 거치지 않는다는 명시와 확인 절차, 바깥 근거 없음 표기까지 포함). `animation-architect-react.md:57` Read 확인. `## Gotchas` 헤더 레벨을 `# Gotchas`→`## Gotchas` 로 낮춘 것은 조건 문장이 요구하는 리터럴(「`## Gotchas` 절에」)과 정확히 일치 — MD041 방지용 H1 제목 줄 추가 확인. **사용자 확인 필요**(FAIL 아님, 계약 조건 미포함 부수효과): planning-kit 12개 스킬 중 plan-sync-github 만 헤더 레벨이 달라졌다. L3.
- [x] SK-12: react-kit 감지 절차가 project-detect.sh 를 부른다 — PASS
  - 근거: evaluator 독립 실행 `call=1 keys_same=1 nkeys=11 script_changed=0`. `project-detection.md:23-24,27` Read — 「시험이 11 키를 지킨다」 는 허위 서술이 「`project-detect-test.sh` 는 `tanstackRouter` 값만 잰다」 로 사실대로 정정된 것을 직접 확인. `react-kit/evals/scripts/project-detect-test.sh` 원문 Read 로 실제로 `tanstackRouter` 하나만 재는 것을 대조(스크립트 자체가 `check()` 함수에서 `tanstackRouter` 필드만 비교). `final-integration.md:237` 트리 주석도 같은 뜻으로 수정됨을 확인. L3.
- [x] SK-13: plan-sync-github Gotchas 에 GitHub 문서 버전 날짜 사실 — PASS
  - 근거: `planning-kit/skills/plan-sync-github/SKILL.md:20` Read — 4 토큰 모두 한 줄에 포함. `apiVersion=2022-11-28` 2회 그대로(evaluator 직접 grep, 시작 판과 동일). L3.
- [x] SK-14: research-log backlog 줄이 19.3 안정화를 반영 — PASS
  - 근거: evaluator 독립 실행 `row=2 canary_wait=0 v193=2`. `docs/react/research-log.md:435,496` Read 확인(둘 다 19.3 언급, "canary 대기" 없음). L3.
- [x] SK-15: 설계 문서 8개 현행화(last_updated·현행화 기록 절이 커밋 47개 모두 포함) — PASS
  - 근거: evaluator 독립 실행 — 8줄 전부 `lu=1 ... miss=0`, commits 9·7·2·6·3·5·9·6=47. `g3-performance.md` 머리(`last_updated: 2026-09-26`)와 「현행화 기록」 절 실제 내용(서술+표, 실제 커밋 해시와 영향 서술) Read 로 확인, 플레이스홀더 아님. L3.
- [x] SK-16: 설계 문서가 지금 스킬 사실을 담는다 — PASS
  - 근거: evaluator 독립 실행 첫 줄 `dev_strict=1 step8=0 passed=1 skipped=1 split=1 verdict=1`, 둘째 줄 `g1_tpl=1 g1_strict=4 vt=4 fi_link=2 rep=2,2,2,2,2,3`. `g6-build-audit.md` §3 Read(7단계 실행 순서·dev 표 strictPort·`passed`·`skipped`·merge-base 원인 가르기·`verdict: APPROVE | REJECT | BLOCKED` 전부 확인, 8번째 단계 없음), `g5b-animation.md:191-195` §2.1b `<ViewTransition>` Read 확인, `final-integration.md:249` Read(project-detect.sh·project-detection.md 동일 줄) 확인. L3.

### Script (1/1, N/A 1건 별도)
- [ ] SC-00: N/A (이 계약은 scripts/release.sh·marketplace.json·plugin.json 버전을 건드리지 않는다)
  - 근거: evaluator 가 `git diff --name-only BASE TIP | grep -cE '^(scripts/release\.sh|\.claude-plugin/marketplace\.json|[^/]+/\.claude-plugin/plugin\.json)$'` 직접 재실행(BASE=6378948, TIP=1ea990c) → 0. 사유 사실 확인. L3.

### Error (1/1)
- [x] ER-01: 두 preflight 원인 가르기 조각이 실제로 셋을 가른다 — PASS
  - 근거: evaluator 독립 실행(계약 측정 도우미 `split_run` — 임시 저장소 구성 후 조각 추출·실행) `flutter=[0 1 1] react=[0 1 1]` — 계약이 명시한 알려진 답과 일치(HEAD 통과·분기점 실패·origin/main 실패). L3, 실행 산출물 직접 확보.

### Architecture (2/2)
- [x] AR-01: 바뀐 파일이 기대 집합 안, 커밋마다 맨 위 자리 하나 — PASS
  - 근거: evaluator 독립 실행 `changed=25 extra=0 multi_top=0 flutter=8 react=4 planning=1 docs_react=9 root=1`. 가지의 전체 10개 커밋(`6d073dd`~`1ea990c`) 각각 `git show --name-only`로 단일 최상위 자리 확인 — 특히 「검토 뒤 수정」 4개 커밋(`729c110`·`899d2ab`·`7c51d87`·`1ea990c`)을 evaluator 가 개별로 재확인(각각 react-kit 단독·docs/react 단독·flutter-toolkit 단독·.harness 단독). L3.
- [x] AR-02: 결정·처리됨·바깥근거없음·문서 페이지 목록을 notes 에 남김 — PASS
  - 근거: evaluator 독립 실행 `committed=1` + 23개 토큰 전부 ≥1, 둘째 줄 `rc=0 pages=10 miss=0`. `scripts/detect-docs-drift.py --since 6378948` 를 evaluator 가 작업 폴더에서 직접 실행해 10페이지 NEW 확인, `k1-notes.md` Read 로 10페이지 전부 실제 나열됨과 기존 페이지 이름 대응 문제까지 서술된 것 확인(§문서 사이트 드리프트 절). L3.

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 금지 — PASS
  - 근거: evaluator 가 현재 HEAD(1ea990c)에서 `python3 scripts/validate-plugin.py --check=code-fence` 직접 실행 → exit 0, "14 plugins, 14 OK". L3.
- [x] AP-04: frontmatter name 필드 누락 금지 — PASS
  - 근거: evaluator 가 `python3 scripts/validate-plugin.py --check=frontmatter` 직접 실행 → exit 0, "14 plugins, 14 OK". L3.

### Reusability (1/1, N/A 1건 별도)
- [ ] RE-01: N/A (새 컴포넌트·함수 모듈 없음)
  - 근거: evaluator 가 `git diff --diff-filter=A --name-only BASE TIP -- . ':(exclude).harness'` 직접 재실행 → 0줄. 사유 사실 확인. L3.
- [x] RE-02: 기존 정본·기존 스크립트 재사용(새 검사 스크립트 안 만듦) — PASS
  - 근거: RE-01 명령 0줄 + `m SK-12` 의 `script_changed=0`(evaluator 독립 실행값, react-kit/scripts 변경 없음). L3.

### Diagnostics (2/2, N/A 3건 별도)
- [ ] DG-01: N/A (release.sh 미변경) — evaluator 직접 재실행 0 확인
- [x] DG-02: 더해진 줄의 markdownlint 새 경고 0, JSON 읽기 실패 0 — PASS
  - 근거: evaluator 독립 실행 `md_new=0 json_bad=0`(markdownlint-cli2 0.23.2 설치 후 실제 채점, MD013 끔 설정 동일 적용). L3.
- [ ] DG-03: N/A (release.sh 미변경) — evaluator 직접 재실행 0 확인, DG-01 과 동일 명령
- [ ] DG-04: N/A (구동할 앱·서버 없음 — 변경 파일 25개 전부 스킬/참조/평가사례/설계문서/notes)
  - 근거: 전체 변경 파일 목록(25개) 재확인 — 실행 진입점(main.dart 등) 0개.
- [x] DG-05: 지금 ci-local.sh 가 담은 CI 26단계(통과 25·yq없음 건너뜀 1)를 로컬에서 통과 — PASS
  - 근거: **evaluator 가 working tree 를 커밋 상태로 복원한 뒤(위 「평가 절차 특기사항」 참조), HEAD=1ea990c=TIP, `git status --porcelain --untracked-files=no` 빈 출력을 직접 확인**하고 `TMPDIR=<임시> bash .harness/handoff/2026-09-26-tools/ci-local.sh <워크트리>` 를 **처음부터 끝까지 백그라운드로 직접 실행**(약 5분 소요, playwright 143+8건·docs-a11y 등 포함). 결과: `grep -c 'rc=0' summary.txt` = 25, `grep -v 'rc=0' summary.txt` = `feedback-agg-test SKIP (yq 없음)` 한 줄만. 계약이 요구하는 값과 정확히 일치. 실행 후 작업 폴더가 여전히 clean(HEAD=1ea990c 불변, untracked-files=no 기준 clean)임을 재확인(부작용 없음). L3, 최고 수준 실행 증거 — 이 스프린트에서 가장 큰 비용을 들여 독립 재현했다.

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (29 - 0) / 29 = 1.00 (임계 0.60 충족)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상 (미검증 항목 없음 — 29개 조건 전부 evaluator 가 직접 실행/Read 로 L3 검증, 그중 20개는 계약 측정 도우미를 evaluator 자신이 독립 파일로 떼어내 재실행)

## Discrimination (규칙 12 적용 조건만)
- 적용 조건: 없음 — 29개 조건 모두 문서/평가사례/설계문서 내용과 검사 스크립트 실행 결과이며, 동시성 가드·인증/권한·멱등성·입력검증·데이터유실·마이그레이션안전성·재시도/중복제거·보안경계·사용자보고충돌 9항 중 어디에도 해당하지 않음.

## Check Artifacts (산출물이 검사인 조건만 — 규칙 10)
- 대상: 없음 — 이 스프린트는 새 검사 스크립트·훅·시험 파일을 만들지 않았다(RE-02 조건이 이를 명시적으로 요구·확인). SK-01/SK-03/SK-12/AP-03/AP-04/DG-05 가 부르는 검사 스크립트(`check-reviewer-protocol-copies.py`, `run-evals.py`, `project-detect.sh`/`project-detect-test.sh`, `validate-plugin.py`, `ci-local.sh` 내부 스크립트들)는 전부 이 스프린트 이전부터 있던 것이며, evaluator 가 그 실행 결과를 직접 재현했다(산출물 자체가 아니라 기존 검사의 실행 결과 재현이므로 5항목 프로토콜은 해당 없음). 예외적으로 `react-kit/evals/scripts/project-detect-test.sh` 원문을 evaluator 가 직접 Read 하여 「tanstackRouter 값만 재는지」를 코드 수준에서 대조(SK-12 근거).

## User-Reported Failures
- 없음 — Iteration 1(끝점 e4f63d8) 뒤 나온 여섯 건 지적은 사용자 실패 보고(REOPENED 대상)가 아니라 구현 내부의 별도 검토(교차 진단 성격)이며, 그 시점 이후 커밋으로 반영되어 이번 evaluator 가 새 끝점(1ea990c)에서 처음부터 재검증했다.

## Evidence Validity
- 검사 대상 증거: 29건 (조건) + N/A 5건
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 계약의 측정 도우미 블록(회귀 게이트) 전체를 evaluator 가 파일로 추출해 bash 로 실행(zsh 아님, 계약 지시대로) — 241줄 syntax 정상, 20개 조건 함수 전부 정상 실행, 구현자 자기측정값과 전수 일치. 별도로 SK-03(run-evals.py)·AP-03/AP-04(validate-plugin.py)·ER-01(임시 git 저장소)·DG-05(ci-local.sh 전체, working tree 복원 후 재실행)를 evaluator 가 각각 독립 실행.
- 양성 대조: SC-00/RE-01/DG-01/DG-03 의 "0" 값 — evaluator 가 측정 명령을 직접 재실행해 대상 파일(scripts/release.sh 등)이 실제로 변경 목록에 없음을 확인. SK-08/SK-14/SK-04 등은 계약이 명시한 시작 판 양성 대조 값과 대비해 evaluator 가 재확인.
- 무효 0건은 미검증 카운터에 영향 없음

## Summary
- Total: 29/29 conditions passed (N/A 5건 별도 — SC-00·RE-01·DG-01·DG-03·DG-04, 사유 전부 evaluator 재확인)
- Verdict: APPROVE
- 특기사항: 이번 iteration 2 는 전 iteration(끝점 e4f63d8, APPROVE)이 아니라 그 이후 별도 검토(6건 지적, 1건 판정 가능 결함 포함)로 REJECT 처리된 뒤 나온 수정본(끝점 1ea990c)을 처음부터 다시 검증했다. 6건 중 5건(판정을 바꿀 만한 1건 — project-detection.md 허위 서술 — 포함)의 수정을 evaluator 가 직접 Read·재실행으로 확인했고, 나머지 1건(react-animation·plan-sync-github 헤더 레벨 변경)은 계약 조건의 리터럴 요구사항과 정확히 일치하는 처리이며 부수효과(스타일 일관성)만 사용자 확인 대상으로 남겼다. evaluator 는 working tree 의 이전 평가 잔여물(status:done 미커밋 변경)을 복원한 뒤 DG-05(로컬 CI 26단계, ~5분)를 처음부터 끝까지 직접 실행해 동일 결과(25 rc=0 + yq SKIP 1줄)를 재현했다.

## Improvement Suggestions
- [SK-11] 측정-환경-오염 — react-animation·plan-sync-github 헤더를 `## Gotchas` 로 낮춘 결과 planning-kit 12개 스킬 중 plan-sync-github 만 헤더 레벨이 달라졌다(나머지 11개는 `# Gotchas`). react-kit 은 이미 혼재(21개 중 8개가 `##`)라 영향이 적지만, planning-kit 은 이번에 처음 깨졌다. 다음 킷 전체 헤더 레벨 통일 스프린트에서 이 불일치를 해소 대상에 포함하거나, 계약 측정 오라클을 `secx` 가 `#`/`##` 양쪽을 다 잡도록 일반화해 원본 파일을 건드리지 않는 대안을 검토할 것을 권장한다(단, 이번 스프린트에서는 위임 조건상 측정 완화 개정이 불가능했으므로 현재 처리가 타당했다). — Iteration 1 리포트와 동일한 개선 제안이 2회째 반복되므로 `contract_ambiguity_notes` 로 승격 권장.
- [프로세스] 검증경로-미기재 — QA evaluator 의 Step 5.5(status: active→done 전환)가 미커밋 상태로 남으면 다음 evaluator 호출의 DG-05(working tree clean 전제) 검증을 방해한다. 계약 작성 시 DG-05 류 "working tree clean" 전제 조건에 "직전 평가자의 미커밋 status 전환은 evaluator 자신의 산출물이므로 검증 전 git checkout 으로 복원 가능" 이라는 명시적 허용 문구를 추가하는 것을 검토할 것을 권장한다.
