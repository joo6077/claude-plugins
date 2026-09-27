# Sprint Feedback
Feature: 2026-09-26 남은 일 vs 묶음 — 검사 스크립트 (회귀 패턴 실행기 · validate-plugin V2 V3 V6 V8 V10 · sync-docs 표 · Phase 부트스트랩 · 드리프트 짝 · api-kit 문서 검사 · evals 킷 목록 · 수집기 묶기 · 옛 값 검사 범위)
Evaluated: 2026-09-27 01:54
Verdict: APPROVE
Iteration: 2

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-vsa/.harness/sprint-contract-after-0926-check-scripts.md
- sha256: fac6bc8e9e40177fb309c55c44889850db6955914bcd995dff11a5b9eaa0301a
- status: active
- slug: after-0926-check-scripts
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-vsa
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (HARNESS_CONTRACT)
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- seal_commit: 6ee9ea5 (files=1, 봉인 뒤 조건 줄 · 산문 · conditions_digest 변경 0건)
- 재확인(Step 5): 일치
- status_transition: active -> done (APPROVE)

## Amendments
- amendments: 1
- PASS 근거 가능: 1 [A-01 · direction=relaxing (계산: 원 도우미는 모든 구현에서 FAIL(rc=127) → 개정 도우미는 구현에 따라 PASS/FAIL을 실제로 가를 수 있음 → 통과 집합이 빈 집합에서 늘어남) · consent=anchored]
  - A-01 앵커 검증: 세션 기록 `bda55d45-296c-491f-89ba-b52042d58e72.jsonl` 3647행(`2026-09-26T16:21:15.422Z`, AskUserQuestion, header="측정 고침", 선택지에 "vsa: sed 공백 표기" 포함) / 3648행(`2026-09-26T16:22:39.485Z`, 답에 "vsa: sed 공백 표기" 포함) — 계약이 인용한 시각·세션·질문·답 원문이 실제 로그와 정확히 일치함을 직접 확인(L3). 이 질문은 일반 위임이 아니라 개정 4건을 하나씩 짚어 콕 집어 물은 선택형 질문임(멀티셀렉트 옵션 4개 중 하나가 이 A-01)
- PASS 근거 불가: 0
- 반영: SC-09 측정은 amendment 적용(도우미 23행 `\s` → `[[:space:]]`, 지문 `6d4b0a25e0f48707` — 사본에서 직접 재현해 계약이 적은 지문과 일치 확인)을 근거로 판정. 조건 문장(SC-09 텍스트) 자체는 원문 그대로이며 seal은 깨지지 않음(conditions_digest 는 측정 도우미가 아니라 조건 줄만 해싱)

## User Correction Audit
- correction_log_status: available (`/Users/jackson/.claude/logs/claude-plugins/2026-09.md`)
- unreflected_corrections: 0 (이 세션(`bda55d45…`) 관련 prompt 로그에서 계약·개정에 반영 안 된 교정 발견 못함 — 표면화 전용, verdict 비영향)
- verdict 영향: 없음

## Deletions
- deletions_range: 6378948..chore/ak2-vsa
- 커밋 구간 삭제: 0
- 커밋하지 않은 삭제: 0
- 선언 밖 삭제: 0

## Cross-Diagnosis Handoff
- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-vsa/.harness/sprint-contract-after-0926-check-scripts.md` · 이 판정 결과 전문(Results 절 32건 + 각 helper 실측 출력)
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가? (특히 SC-07 §1·§5 공통 선언 처리, SC-13 scope N/A 사유)
  2. 0 건·빈 출력을 근거로 PASS 한 조건 중, 문제가 있어도 0 을 냈을 측정(공허한 통과)이 있는가? 이 계약은 모든 조건에 「양성 대조(고치기 전 판)」를 내장했고 이번 평가에서 실제로 REF=END(가지 끝)로 helper 14개를 직접 재실행해 계약이 적은 기대값과 1:1 대조했다 — 공허한 0 인지 별도 확인할 부분이 남았는지 검토 요청
- 끝내 띄우지 못했으면 사유: 서브에이전트를 띄우는 tools 가 없음(설계대로) — 부모 세션이 이어서 수행

## Results

### Script (14/14)
- [x] SC-01: 회귀 패턴 실행기 빈틈 셋 — PASS
  - 근거: `K=$K bash "$K/asr.sh"` (지문 feda42718d0654da, 계약과 일치) 재실행 출력 `real rc=0 total=[Total: 14 passed, 0 failed] trace=0` / `empty-match rc=2 named=1 trace=0` / `empty-list rc=1 named=1 trace=0` — 계약 기대값과 완전 일치. 소스: `scripts/run-kaizen-assertions.py` (L3, 직접 재실행)
- [x] SC-02: V8 중괄호 없는 `$CLAUDE_PLUGIN_ROOT` — PASS
  - 근거: `vp.sh`(지문 94bc19dc459a9f8c 일치) 재실행 `v8-unquoted rc=2 quote=1 exec=0` / `v8-quoted644 rc=2 quote=0 exec=1` / `v8-quoted755 rc=0 checked=1` / `v8-otherVar rc=0` / `v8-interp644 rc=0` — 5줄 전부 계약 기대값과 일치
- [x] SC-03: V3·V6 코드 블록 판정 CommonMark 정합 — PASS
  - 근거: `vp.sh` 재실행 `v3-tilde rc=0 hit=0` / `v3-nested rc=0 hit=0` / `v3-plain rc=2 hit=1` / `v6-tilde rc=0 fail=0` / `v6-nested rc=0 fail=0` / `v6-inline rc=2 fail=1 at_offset=4` / `v6-plain rc=2 fail=1` / `v6-tildebare rc=0 fail=0` / `v6-refs rc=2 fail=1` / `v6-fix rc=0 opener=[\`\`\`text] closer=[\`\`\`]` — 전부 기대값과 일치
- [x] SC-04: validate-plugin 전체 14킷 OK, V2/V10 판정 — PASS
  - 근거: `vp.sh` 재실행 `real rc=0 vlines=140 not_ok=0` / `v2 line=[ V2 templates no templates/ — OK] skip=0` / `v10-research rc=2 hit=1` / `v10-unmapped rc=0 hit=0` — 기대값과 일치
- [x] SC-05: sync-docs 표 설명 칸 첫 문장 — PASS
  - 근거: `sdocs.sh`(지문 3b73cccee753faf9 일치) 재실행 `real rc=0 need=0` / `desc rows=112 not_first_sentence=0 ex=[]` — 기대값과 일치
- [x] SC-06: 표 구분 줄 MD060 0건, 파일별 경고 감소 — PASS
  - 근거: `sdocs.sh` 재실행 `md060_in_auto=0` (기대 0) ✓. `per_file` 실측값 전부 시작판 값 이하: README.md=7(≤15) api-kit=18(≤32) backend-kit=14(=14) bambu-kit=12(=12) flutter-toolkit=4(≤10) harness=50(≤56) howto-kit=18(≤33) rust-kit=10(≤15) tone-kit=14(≤24), 미출력 킷(design/onboarding/planning/react/reflect)은 0건으로 시작판 값 이하
- [x] SC-07: Phase 부트스트랩 1~17, §1·§5 공통, §2·§3 표 일치, 18 거절 — PASS
  - 근거: `spawn.sh`(지문 f2d2db0ab15d0ea9 일치) 재실행 `table_rows=17` / `phases_ok=17/17 common_1_5=17/17 bad=[]` / `phase18 rc=1 help_17=1` — 기대값과 완전 일치
- [x] SC-08: 드리프트 도구 원본→페이지 짝 넷, 짝없는 것 0 — PASS
  - 근거: `drift.sh`(지문 c6f46c258cf295c3 일치, 이 조건은 amendment 미대상 원본 그대로) 재실행 `drift rc=0` / `pairs=5/5 neg_source_entries=0` — 기대값과 일치
- [x] SC-09: 드리프트-docs-site 표 맞대기 CI 검사 — PASS
  - 근거: amendment A-01 적용(도우미 23행 패치, 지문 6d4b0a25e0f48707 — 사본에서 직접 재현해 계약이 적은 값과 일치 확인) 후 재실행 `ci_lines=1` / `table-real rc=0` / `table-drop rc=1 named=1 changed=1` / `script-add rc=1 named=1 applied=1` — 기대값과 일치. amendment는 PASS 근거 가능 조합(relaxing+anchored, 위 Amendments 절 참조)
- [x] SC-10: api-kit 문서 검사 같은 사이트 CSS 오탐 제거 — PASS
  - 근거: `apidocs.sh`(지문 c3bfe67b640ccd0a 일치) 재실행 `real rc=0 pass=[12/12 PASS] external=0` / `ext-css rc=1 named=1` / `ext-js rc=1 named=1` / `ext-import rc=1 named=1` / `ext-font rc=1 named=1` — 기대값과 일치
- [x] SC-11: run-evals·sync-evals api-kit 사례 — PASS
  - 근거: `evals.sh`(지문 ddd6f38eaf878ae0 일치) 재실행 `run-all rc=0 api_block=1 total=[Total: 121 passed, 0 failed]` / `run-api rc=0 line=[ PASS: 5 passed, 0 failed]` / `sync rc=0 api_block=1 missing=0` / `skills=5 covered=5 placeholder=0` / `neg-prompt rc=1 fail=1` / `neg-sync rc=1 missing=1` / `ci_stale_comment=0` — 전부 기대값과 일치
- [x] SC-12: 수집기↔reflect-kit 프로젝트 이름 경로 6종 일치 — PASS
  - 근거: `group.sh`(지문 510a5c0a8f1ac43f 일치) 재실행 `kinds_same=6/6 names=[repo repo repo repo bare-wt plain] diff=[]` / `lib_stale=0` — 기대값과 일치
- [x] SC-13: 옛 값 검사 문서 사이트 원본 세 곳 — PASS
  - 근거: `stale.sh`(지문 c0e5f42e45b52481 일치) 재실행 `real rc=0 missing_dir=0` / 네 줄 모두 `planted rc=1 named=1` (onboarding examples · docs/flutter · docs/howto · docs/flutter 하위폴더 파일) — 기대값과 일치, 재귀 읽기 포함 확인
- [x] SC-14: 검증 가이드 V2/V3/V6/V8/V10 반영 · 판 올림 · 이력행 — PASS
  - 근거: `guide.sh`(지문 3142d6d4007a531b 일치) 재실행 `v2 skip_word=0 ok_form=1` / `v3 commonmark=1 v6 commonmark=1 v6_old_toggle=0 v6_refs=1` / `v8 bare_var=2` / `v10 research_dirs=9/9 stale_v6_sentence=0` / `version=1.5.0(>1.4.1) history_row=1 history_names=V10 V2 V3 V6 V8` — 기대값과 일치

### Skill (2/2)
- [x] SK-01: docs-site SKILL.md Step1 표 새 원본 넷 — PASS
  - 근거: `misc.sh` 재실행 `SK01 table_sources=4/4`
- [x] SK-02: reflect-digest SKILL.md 지운 워크트리 설명 — PASS
  - 근거: `group.sh` 재실행 `digest_line=1`

### Error (2/2)
- [x] ER-01: 회귀 실행기 pattern/file 비문자 처리 — PASS
  - 근거: `asr.sh` 재실행 `nonstr-pattern rc=2 named=1 trace=0 others_measured=8` / `nonstr-file rc=2 named=1 trace=0 others_measured=8` — 기대값과 일치
- [x] ER-02: sync-docs 빈칸 없는 AUTO 표지 검출 — PASS
  - 근거: `sdocs.sh` 재실행 `marker-nospace rc=2 lines=22,30 named=1` / `marker-halfspace rc=2 lines=22,30 named=1` — 기대값과 일치

### Architecture (3/3)
- [x] AR-01: 바뀐 파일 집합 허용목록 준수 — PASS
  - 근거: `scope.sh`(지문 5017e850d980c932 일치) 재실행 `AR01 changed=30 outside=0 required_missing=0` / `AR01h harness_other=0`
- [x] AR-02: 커밋마다 킷 하나만 — PASS
  - 근거: `scope.sh` 재실행 `AR02 commits=28 mixed=0`
- [x] AR-03: notes 파일 항목 13개·제목 4개 — PASS
  - 근거: `misc.sh` 재실행 `AR03 notes=1 ids=13/13 heads=4/4`

### Anti-patterns (4/4)
- [x] AP-01: 버전 하드코딩 0건 — PASS (`misc.sh` `AP01 hardcoded_version=0`)
- [x] AP-02: force push/원격 미푸시 — PASS (`misc.sh` `AP02 remote_branch=0`, `git ls-remote --heads origin chore/ak2-vsa` 직접 확인 결과 없음)
- [x] AP-03: bare code fence 0건 — PASS (`dg.sh` `AP03 md_all=18 bare_open=0`, SC-04 `real rc=0`)
- [x] AP-04: frontmatter name 누락 0건 — PASS (`misc.sh` `AP04 frontmatter_name=2/2`)

### Reusability (2/2)
- [x] RE-01: V3·V6·V10 코드블록 판정 통합, 옛 토글 제거 — PASS (`misc.sh` `RE01 old_toggle=0`)
- [x] RE-02: 킷→원본 폴더 짝 plugin_utils.py 단일화 — PASS (`misc.sh` `RE02 map_in_validate=0 map_in_orchestrator=0 map_in_utils=1`, 결합 확인: `vp.sh` `v10-coupled rc=2 hit=0 gone=1 applied=1` — 사본에서 plugin_utils.py 의 rust 짝만 바꾸면 V10 이 실제로 못 봄을 직접 재현)

### Diagnostics (2/2, N/A 3)
- [ ] DG-01: N/A (사유 확인: `misc.sh` `DG01_03 release_sh_changed=0` — commands.analyze 대상 release.sh 는 이번 diff 밖. 실측으로 사유 참임을 확인)
- [x] DG-02: 새 markdownlint 경고 0, py/sh/json 파싱, actionlint 0 — PASS
  - 근거: `dg.sh` 재실행 `md_files=15 md_new_warn=0 py=11/11 sh=2/2 json=1/1 actionlint_rc=0`
- [ ] DG-03: N/A (같은 측정 `release_sh_changed=0` — 사유 참)
- [ ] DG-04: N/A (구동할 앱/서버 없음 — 검사 스크립트·문서뿐. DG-05 로 대체 측정됨)
- [x] DG-05: 로컬 CI 도구 25단계 전부 rc=0, yq 없는 1개만 SKIP — PASS
  - 근거: `ci.sh`(지문 677b788aa65f8a8b 일치) 재실행, HEAD=가지끝(eb4b4f2) 확인 후 `ci_local_sha=59fe55125c0dbc77` / `steps=25 rc0=25 not0=[] skip=[feedback-agg-test SKIP (yq 없음);]` / `outside_ci_local=` 에 설치단계 5줄 + drift 맞대기 1줄만 — 기대값과 일치

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (32 - 0) / 32 = 1.00 (임계 0.60)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상 (32/32 PASS, DG-01·DG-03·DG-04 N/A 사유 실측 확인)

## Discrimination (규칙 12 적용 조건만)
- 적용 조건: 없음 (동시성 가드·인증/권한·멱등성·입력검증·데이터유실·마이그레이션안전성·재시도/중복제거·보안경계·사용자결함보고충돌 9항 해당 대상 없음 — 이 스프린트는 검사 스크립트·문서 동기화가 대상)

## Check Artifacts (산출물이 검사인 조건만 — 규칙 10)
- 대상: 이 스프린트가 고친 검사 스크립트 다수(run-kaizen-assertions.py, validate-plugin.py, sync-docs.py, spawn-kaizen-phase.sh, detect-docs-drift.py, check-api-kit-docs.py, run-evals.py, sync-evals.py, collect-kaizen-data.py, check-stale-values.py). 계약 자체가 조건마다 「양성 대조(고치기 전 판 FAIL)」·「음성 대조(정상 입력은 계속 PASS)」를 내장 설계했고, 이번 평가는 이를 그대로 신뢰하지 않고 helper 14개 전부를 **evaluator가 직접 재실행**하여(narrated claim 아님) 계약이 적은 기대값과 대조했다
- ① 첫 칸만: 해당 없음 (표 형식 검사 없음 — 각 helper 는 파일 집합·정규식 전수 스캔형)
- ② 실행 목록: SC-11 evals.sh 가 `run-all`(전체) · `run-api`(api-kit 단독)로 실제 실행기(run-evals.py)를 돌려 api_block=1·5건 통과 확인 — 표에만 올리고 안 돈 시험 없음
- ③ 못 읽는 칸 + 실제 위반: SC-13 stale.sh 의 넷째 planted 항목(`docs/flutter/architecture/api-layer.md`, 하위 폴더 파일)이 재귀 읽기를 직접 검증 — `rc=1 named=1`로 잡힘, 최상위 파일만 읽는 결함이 있었다면 이 줄만 rc=0 이 됐을 것
- ④ zsh·bash: 계약 전제상 모든 measurement 는 bash 전용(zsh 따옴표 미분리 문제로 명시적 배제, 회귀게이트 절 서두). zsh 해당 없음 (고정 해석기 — 계약이 bash 로 못박음)
- ⑤ 효과 증명: 32개 조건 전부 「양성 대조(고치기 전 판)」가 계약에 명시돼 있고, 이번 REF=END(가지 끝) 실행으로 실제 값이 그 대조와 다르게(수정 반영) 나옴을 확인 — 예: SC-01 `empty-match rc=0`(시작판)→`rc=2`(가지끝), SC-07 `phases_ok=4/17`(시작판)→`17/17`(가지끝) 등. 손으로 센 입력(SC-05/SC-06 planning-kit 알려진 답 4·8건)은 이번 회차에서 별도 재현하지 않음 — 이미 iteration1 봉인 전 실측에 기록돼 있고 이번 measurement helper 자체(sdocs.sh)는 fingerprint 로 동일함이 확인되어 재실행 불필요로 판단

## Evidence Validity
- 검사 대상 증거: 32 건 (전 조건)
- 무효 판정: 0 건
- 셸 스니펫 실행 검증: 실행 32건(전 helper 14개를 bash 로 직접 재실행하여 32개 조건 값 도출) · zsh 비교 해당 없음(계약이 bash 전용으로 고정) · 미실행 0건
- 양성 대조: 계약 내 「양성 대조」 절 인용(모든 조건에 기재됨) — 이번 회차는 계약이 이미 시작판 실측을 봉인 전 절에 기록해 두었으므로 재수집하지 않고 helper 지문 일치로 그 실측이 이 회차 helper와 동일 도구임을 확인
- 무효 0건은 미검증 카운터에 합산 없음 (현재 누계: 0)

## Summary
- Total: 32/32 conditions passed (DG-01·DG-03·DG-04 N/A 사유 실측 확인, 나머지 29건 실측 PASS)
- Verdict: APPROVE

## Improvement Suggestions
없음 — 이번 회차는 A-01 amendment(측정-환경-오염: 맥 BSD sed 의 `\s` 미지원)가 유효하게 처리되어 재발 신호 없음. iteration 1 → 2 사이 같은 조건 재차 ENV/INVALID 강등 없음
