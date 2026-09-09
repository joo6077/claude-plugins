# Sprint Feedback
Feature: harness amend_direction — 오라클 변경 amendment 극성 규칙
Evaluated: 2026-09-08 17:20
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: .harness/sprint-contract-harness-amend-direction-baseline-case.md
- sha256: fa830beb6bd0d36481768d4d4d1bf1d31d376610058c6b86c403a25c39e9fede
- status: active (평가 시점) → done (전환 후)
- slug: harness-amend-direction-baseline-case
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/harness-amend-direction
- contract_root_unconfigured: false
- 선택 근거: ladder 1 (명시 경로)
- legacy_contract_used: false
- seal_status: SEAL_OK (recorded sha256:bef0472d446badb5 == actual)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (TOCTOU 없음)
- status_transition: active -> done

## Amendments
- amendments: 0 (사이드카 파일 `.harness/sprint-amendments-harness-amend-direction-baseline-case.md` 부재 확인)

## User Correction Audit
- correction_log_status: available (`/Users/jackson/.claude/logs/harness-amend-direction/2026-09.md`)
- unreflected_corrections: 0 (로그에 항목 1건뿐이며 reflect-kit Stop 훅의 자동 메타분석 프롬프트임 — 사용자 발화가 아니므로 교정 대조 대상 아님)
- verdict 영향: 없음

## Results

### Skill (3/3)
- [x] SK-01: `## Amendment 사이드카` 섹션에 허용 집합/측정 집합 극성 규칙 산문 — PASS
  - 측정: `awk '/^## Amendment 사이드카/{p=1;next} /^## /{p=0} p' harness/references/contract-schema.md` 결과 `허용 집합`=3, `측정 집합`=6, `amend_direction_oracle`=3 (전부 ≥1)
  - 근거: `harness/references/contract-schema.md:792-798` — "헬퍼의 입력은 허용 집합이다 — 측정 집합을 넣으면 극성이 뒤집힌다" 규칙 산문 확인 (L3: 의미 검증 — 두 극성이 대칭이라는 설명과 amend_direction_oracle로 유도하는 규칙까지 명시)
- [x] SK-02: A-01 worked example — PASS
  - 측정: 같은 섹션 출력에 `A-01`=2, `measured_removed=2`=1, `narrowing added=0 removed=2`=1 (전부 존재)
  - 근거: `harness/references/contract-schema.md:817-825` — 39→37 실측, 두 헬퍼 각각의 출력 대조 (relaxing vs narrowing 오라벨) 확인
- [x] SK-03: 소비면 2 파일 언급 + 미재정의 — PASS [enumerated 2/2]
  - `harness/agents/qa-evaluator.md`: `grep -c 'amend_direction_oracle'`=1, `grep -c 'amend_direction_oracle() {'`=0
  - `harness/skills/sprint-contract/SKILL.md`: `grep -c 'amend_direction_oracle'`=1, `grep -c 'amend_direction_oracle() {'`=0
  - 근거: qa-evaluator.md:649-653, SKILL.md:69 — 둘 다 "정의는 스키마가 SSOT" 로 명시하고 함수 본체 재정의 없음 (L3 확인)

### Script (3/3)
- [x] SC-01: `amend_direction_oracle` 실측 집합 판정 — PASS [enumerated: zsh+bash]
  - zsh: `relaxing measured_removed=2 measured_added=0` / bash: 동일 / diff 빈 출력
  - 음성 대조 1: 같은 파일을 `amend_direction`에 넣으면 `narrowing added=0 removed=2` — 확인 (극성 반전 재현)
  - 음성 대조 2 (mutation test, 자체 추가 검증): `amend_direction_oracle`의 relaxing 분기를 narrowing으로 바꾼 뮤턴트 실행 → `narrowing measured_removed=2 measured_added=0` (기대값과 불일치 → 이 측정은 구현에 결합되어 있고 극성 반전이 실제로 판정을 가른다는 것을 확인)
  - 픽스처 재현성: `git diff --name-only 4fb1382..37d50a7 -- . ':(exclude).harness/handoff/*' ':(exclude)docs/bambu-calibration/*' | LC_ALL=C sort -u` 재실행 결과가 `measured-orig.txt`(39줄)와 바이트 단위 diff 없음, `54fb3b3..37d50a7`도 `measured-amended.txt`(37줄)와 동일 — 픽스처가 실제 A-01 커밋 이력에서 재현됨을 확인
- [x] SC-02: `amend_direction` 회귀 + 함수 본체 불변 — PASS [enumerated: zsh+bash]
  - zsh: `relaxing added=2 removed=0` / bash: 동일
  - `git show 4fb1382:harness/references/contract-schema.md`에서 추출한 `amend_direction()` 본체와 HEAD에서 추출한 본체 `diff` 빈 출력 (바이트 단위 동일 확인)
- [x] SC-03: validate-plugin + sync-docs (워크트리 scripts/) — PASS [goal]
  - 스크립트 경로: `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/harness-amend-direction/scripts/{validate-plugin.py,sync-docs.py}` (워크트리 자체 경로. `plugin_utils.py:15` `REPO_ROOT = Path(__file__).parent.parent` 확인 — 실행한 cwd가 곧 워크트리이므로 메인 체크아웃 파일이 아니라 이 브랜치의 파일을 잰 것을 확인)
  - `python3 scripts/validate-plugin.py harness` → harness 전 항목 OK, Exit: 0
  - `python3 scripts/validate-plugin.py` (전 킷, 인자 없음) → 13 plugins, 13 OK, Exit: 0 (harness 원인 새 FAIL 0건)
  - `python3 scripts/sync-docs.py harness` → "변경 없음: harness/README.md", exit 0
  - `python3 scripts/sync-docs.py --check-only` → "모든 README가 동기화 상태입니다", exit 0

### Error (2/2)
- [x] ER-01: 빈 파일 2개 → `unknown measured_removed=0 measured_added=0`, stderr 0줄 — PASS [enumerated: zsh+bash]
  - zsh/bash 동일 출력, 양쪽 stderr 0줄 확인
- [x] ER-02: 결측 입력 → `unknown missing_input=/nonexistent/a`, stderr `No such file` 0건, rc=0 — PASS [enumerated: zsh+bash]
  - zsh/bash 동일. 대조: 베이스라인 `amend_direction`은 같은 입력에 `sort: No such file or directory` 4줄을 stderr에 낸 뒤 `unknown added=0 removed=0`으로 조용히 실패 (GAP 분석 서술과 실측 일치 확인) — `amend_direction_oracle`이 결측을 명시 표기로 바꾼 것을 확인

### Architecture (2/2)
- [x] AR-01: 변경 경로 8접두 허용목록 — PASS [enumerated]
  - `git diff --name-only 4fb1382..HEAD` = 10개 경로, 전부 8개 허용 접두(`harness/references/contract-schema.md` · `harness/agents/qa-evaluator.md` · `harness/skills/sprint-contract/SKILL.md` · `harness/evals/amend-direction/` · `harness/README.md` · 3종 슬러그 산출물) 중 하나에 매치. 매치 안 되는 줄 0건
- [x] AR-02: 헤더 갱신 이력 + 버전 미상향 + HTML 미러 미갱신 — PASS [enumerated 3/3]
  - `sed -n '1,20p' ... | grep -c '2026-09-08'` = 1 (≥1)
  - `git diff 4fb1382..HEAD -- harness/references/contract-schema.md | grep -cE '^\+.*v5\.[45]'` = 0
  - `git diff --name-only 4fb1382..HEAD -- docs/` = 빈 출력
  - 의심 지점 판단 (3f7d7be): 커밋 329e47c 시점엔 헤더에 리터럴 "v5.4"가 있어 같은 측정이 count=1로 FAIL했을 것을 확인. 3f7d7be는 그 리터럴을 브랜치명 언급으로 바꿨을 뿐 `## 스키마 버전` 섹션(880-882행, "현재: v5.3")은 건드리지 않았고, diff hunk도 헤더 블록 1곳과 함수 정의 블록 1곳뿐임을 확인 — 실제 버전 상향은 어디에도 없다. 조건의 명시 의도("다른 세션 브랜치와의 버전 번호 충돌 회피")도 문자 그대로의 측정도 동시에 충족하며, 오히려 리터럴 "v5.4" 문자열이 병합 후 다른 브랜치의 실제 v5.4 승격 항목과 텍스트 충돌할 여지를 없앤 것으로 판단 — 우회가 아니라 조건 의도에 더 부합하는 수정으로 판정. FAIL 사유 없음. (Improvement로 오라클 문구에 대한 관찰만 하단에 기록)

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 금지 — PASS
  - `python3 scripts/validate-plugin.py harness --check=code-fence` → V6 code-fence 0 bare — OK, Exit 0
- [x] AP-04: frontmatter name 필드 누락 없음 — PASS
  - `python3 scripts/validate-plugin.py harness --check=frontmatter` → V1 frontmatter 9 skills + 1 agent — OK, Exit 0
  - (참고, 비채점) AP-01/AP-02 sanity grep — 변경된 10개 파일 전체에서 `hardcoded.*version`, `git push.*--force` 매치 0건

### Reusability (2/2)
- [x] RE-01: 재사용 가능 컴포넌트를 private으로 만들지 않음 — PASS
  - `amend_direction_oracle`은 SSOT(`contract-schema.md`)에 1회만 정의되고 소비면 2곳은 참조만 함 — 의도적으로 공유 가능한 위치에 둠
- [x] RE-02: 기존 유사 컴포넌트 재사용 (신규 중복 없음) — PASS
  - `grep -rn "amend_direction" scripts/` 매치 0건, `grep -rln "comm -13\|comm -23" scripts/` 매치 0건 — `scripts/`(shared_path)에 중복 구현 없음

### Diagnostics (3/4, 1 env_gap)
- [x] DG-01: `bash -n scripts/release.sh` 워닝 0개 — PASS (exit 0, 출력 없음)
- [~] DG-02: IDE diagnostics 워닝/인포 0개 — `[미검증:ENV]`
  - 1차 시도: 이 evaluator 세션에 부여된 도구 목록(Read/Bash)에 `mcp__ide__getDiagnostics` 류의 IDE 진단 MCP 도구 자체가 없음 (project.yaml `runtime_inspection.mcp_server: null`과 일치)
  - fallback 시도: 변경된 5개 .md 파일 전체 코드펜스 균형 검사(```` ``` ```` 라인 수 전부 짝수 — 2/38/2/62/32) + 탭 문자 검사(0건) + validate-plugin V1(frontmatter)·V6(code-fence)는 이미 별도 조건(AP-03/04)에서 실측 OK
  - 실패 로그: 도구 호출 자체가 불가(도구 미부여) — 런타임 에러 로그 없음, 부재 자체가 로그
  - 통제 불가 사유 + 재검증 명령: `project.yaml commands.lint: null`이라 대체 린터도 미설정. 재검증 명령: Claude Code IDE에서 변경 파일을 열고 `mcp__ide__getDiagnostics` 호출, 또는 `commands.lint`에 markdownlint 등을 설정 후 재실행
- [x] DG-03: `bash scripts/release.sh 2>&1 || true` 에러/예외 0개 — PASS (인자 없이 실행 시 정상 Usage 안내만 출력, 에러/예외 문자열 없음)
- [x] DG-04: 실기 앱/서버 구동 — N/A (계약 명시) — PASS (N/A 사유 타당성 확인: harness는 실행형 앱/서버가 아니라 스킬·에이전트·references 문서이며, SC-01·SC-02·ER-01·ER-02의 헬퍼 실행이 이 스프린트의 유일한 "런타임"을 대신 검증함 — 실제로 이 4개 조건을 zsh·bash 양쪽에서 직접 실행해 대체 검증했으므로 N/A 사유가 형식적 회피가 아니라 실질적으로 충족됨)

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 1  [DG-02 — IDE 진단 MCP 도구 미부여 + lint 명령 미설정, fallback 정적 검사(fence 균형·탭·V1/V6) 완료, 재검증 명령 명시]
- verified_coverage: (18 - 1) / 18 = 0.94  (임계 0.60 이상 — 통과)
- 연속 ENV 승급: 없음 (iteration 1, 최초 발생)
- Verdict 영향: 통상 (env_gap 1건은 자동 REJECT 카운터에 미합산, coverage 게이트도 통과)

## Discrimination (규칙 12 — 참고, 필수 적용 조건 없음)
- 적용 조건: 없음 (9개 카테고리 — 동시성/인증/멱등성/입력검증/데이터유실/마이그레이션/재시도/보안경계/사용자보고충돌 — 중 해당하는 조건 없음. 이번 스프린트는 문서·셸 헬퍼 극성 규칙 정정)
- 자체 추가 검증: SC-01에 대해 계약이 요구한 음성 대조(허용 집합 헬퍼 오적용) 외에 뮤테이션 테스트(relaxing 분기→narrowing 치환)를 추가 실행 — 결합 확인: 측정이 실제 구현 분기에 의존함을 확인 (근거는 SC-01 결과 참조)

## Evidence Validity
- 검사 대상 증거: 18건 (조건별)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 실행 6건(SC-01/SC-02/ER-01/ER-02/README.md 스니펫/뮤테이션 테스트) · zsh+bash 양쪽 확인 5건 · 미실행 0건
- 무효 0건 → 미검증 카운터(`invalid_evidence`) 영향 없음

## Summary
- Total: 17/18 PASS, 1 env_gap (DG-02), 0 FAIL
- Verdict: APPROVE
- status_transition: active -> done (전환 완료)

## Improvement Suggestions
- [AR-02] 측정-방식-불일치 — 측정식 `grep -cE '^\+.*v5\.[45]'`는 "이 변경이 버전을 v5.4/v5.5로 상향했는가"와 "diff 텍스트 어딘가에 그 숫자가 언급되었는가"를 구분하지 못하는 과포괄 리터럴 매칭이다. 이번 스프린트에서 실제로 이 때문에 순수 서술("v5.4는 다른 브랜치가 선점")조차 1회 FAIL을 유발했다(commit 329e47c 시점 count=1). 대체 문구 제안: 측정을 `## 스키마 버전` 섹션의 `현재: **v5.X**` 라인이 diff에서 바뀌었는지로 한정 — 예: `git diff 4fb1382..HEAD -- harness/references/contract-schema.md | grep -E '^[+-]현재: \*\*v5\.'` 가 짝수(0 또는 대칭)인지 확인. 이러면 실제 버전 선언 변경만 잡고 본문 서술 속 버전 언급은 오탐하지 않는다.
