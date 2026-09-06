# Sprint Feedback
Feature: anti_patterns 에 command 필드 추가 — 정규식으로 못 재는 검사 위임
Evaluated: 2026-09-06 15:30
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-antipattern-command-field.md
- sha256: 7db50a0832354ef5af2726d91552446fe90fddbbf9c9e6349dabf3f7f18bb7bd
- status: active (평가 시점) → done (전환 후)
- slug: antipattern-command-field
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 1 (명시 경로 — 사용자가 계약 경로 직접 지정)
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (평가 도중 다른 세션이 PR #32 를 merge 하여 HEAD 가 8f41a6d → f2fcef4 로 이동했으나,
  계약 파일 자체의 sha256/status는 불변. 4 target 파일 내용도 커밋 전후 byte-identical 확인)
- status_transition: active -> done

## Amendments
- amendments: 0 (사이드카 없음 — antipattern-command-field 슬러그 amendment 파일 부재 확인)

## User Correction Audit
- correction_log_status: available (/Users/jackson/.claude/logs/claude-plugins/2026-09.md)
- unreflected_corrections: 0 (세션 44c7700e 의 14:29~15:05 구간 프롬프트 2건 확인, 이 스프린트에 대한
  미반영 교정 없음)
- verdict 영향: 없음 (표면화 전용)

## 환경 사실 특기사항 (동시 편집 세션)
평가 도중 `chore/close-docs-quality-contract` 브랜치(별도 스프린트 `docs-quality-gates`, QA APPROVE 26/26)가
main 에 merge 됨 (PR #32, 커밋 f2fcef4). 이 브랜치는 이 스프린트가 손댄 동일 4 파일을 함께 포함하고 있었다
(사용자가 사전에 8ab6049 에서 4 파일만 골라 워킹트리를 복구해둔 상태). merge 전후로:
- `git status --porcelain` 이 9건 → 0건(clean)으로 바뀜 — working tree 내용이 그대로 커밋된 것 확인
- 계약 파일 sha256 불변, 4 target 파일 sha256(간접: git diff HEAD 빈 출력)으로 내용 불변 확인
- baseline 커밋 `8f41a6d` 은 여전히 히스토리 조상이라 `git diff --name-only 8f41a6d -- <path>` 측정 유효
- AR-02 재확인(`scripts/validate-plugin.py`, `harness/evals/`)도 병합 브랜치 기준으로 재검증 — 변경 0건
평가 결과에 영향 없음. 모든 명령은 최종 커밋 f2fcef4 기준으로 재실행하여 최종 근거로 사용.

## Results

### Skill (4/4)
- [x] SK-01: `command` 필드 문서화 + `pattern`/`command` 관계 명시 — PASS
  - 근거: `harness/README.md:133` (`command: "명령"  # 선택 — 정규식으로 판정 불가한 검사를 도구에 위임`),
    `harness/README.md:144-147` (관계 규칙: "둘 중 최소 하나는 있어야 한다... 둘 다 있으면 `command` 가 판정 권위다")
- [x] SK-02: 언제 `command` 를 쓰는지 판단 기준 + 코드펜스 실례 — PASS
  - 근거: `harness/README.md:149-159` ("줄 단위 정규식으로 판정할 수 없을 때" 문단, 코드펜스 예시 292건 실측 인용)
- [x] SK-03: `harness/templates/project.yaml` 주석 예시에 `command` 포함 — PASS
  - 근거: `harness/templates/project.yaml:39` (`#   command: "python3 scripts/validate-plugin.py --check=code-fence"`)
- [x] SK-04: qa-evaluator 가 `command` 항목을 명령 실행으로 분기 — PASS
  - 근거: `harness/agents/qa-evaluator.md:569-578` (`command` 유무 분기, "Grep 으로 대체하지 마라" 명시)

### Script (4/4)
- [x] SC-01: 수정된 AP-03 오탐 없음 + 음성 대조 — PASS
  - 근거: `python3 scripts/validate-plugin.py --check=code-fence` 실행 결과 "Total: 13 plugins, 13 OK / Exit: 0"
  - 음성 대조 실행: harness/README.md 말미에 언어 힌트 없는 fence 1개 임시 삽입 후 재실행 →
    `FAIL harness/README.md:470 — bare \`\`\` (no language hint)`, `Total: 13 plugins, 12 OK, 1 ERROR`, exit 2.
    이후 백업본으로 복원 후 `diff` 로 byte-identical 확인, 재실행 결과 exit 0 원복 확인 (Discrimination 검증 완료)
- [x] SC-02: 기존 `pattern` 전용 3종 하위호환 — PASS [exact, enumerated 3/3]
  - 근거: `.harness/project.yaml` AP-01(`pattern: "hardcoded.*version"`, command 없음),
    AP-02(`pattern: "git push.*--force"`, command 없음),
    AP-04(`pattern: "^---\\s*\\n(?![^-]*name:)"`, command 없음) — 3종 모두 개별 확인
- [x] SC-03: `bash harness/scripts/validate.sh` 에러 0건 + 음성 대조 — PASS
  - 근거: 실행 결과 "Score: 90/100 (errors: 0, warnings: 2)", exit 0
  - 음성 대조 실행: `.harness/project.yaml` 을 백업 후 anti_patterns 를 AP-01 1개만 남기도록 임시 편집,
    재실행 시 `⚠️ anti_patterns 1개 — 최소 2개 권장` 경고 확인. 이후 백업본 복원 → `diff` byte-identical 확인,
    재실행 결과 경고 사라짐 확인 (Discrimination 검증 완료)
- [x] SC-04: `python3 scripts/validate-plugin.py` exit 0 — PASS
  - 근거: 실행 결과 "Total: 13 plugins, 13 OK", `echo $?` == 0

### Error (2/2)
- [x] ER-01: `command` 실행 불가 환경 처리(도구 부재 시 `[미검증]`) 명시 — PASS
  - 근거: `harness/agents/qa-evaluator.md:574-575` ("명령을 실행할 수 없으면(도구 부재·권한) 조용히 PASS 로
    넘기지 말고 `[미검증]` 으로 기록하고 그 사유를 적는다")
- [x] ER-02: `command`/`pattern` 둘 다 없으면 설정 오류 명시 — PASS
  - 근거: `harness/README.md:145-146` ("둘 다 없으면 설정 오류이며 그 항목은 판정 불가다"),
    `harness/agents/qa-evaluator.md:578` ("둘 다 없으면 설정 오류다. PASS 로 넘기지 말고 계약/설정 결함으로 보고한다")

### Architecture (3/3)
- [x] AR-01: 대상 4파일 baseline 이후 수정 확인 — PASS [exact, enumerated 4/4]
  - 근거: `git diff --name-only 8f41a6d -- <path>` 4개 경로 각각 비어있지 않음 확인
    (harness/README.md, harness/agents/qa-evaluator.md, harness/templates/project.yaml, .harness/project.yaml)
    — 최종 커밋 f2fcef4 기준으로 재실행하여 동일 결과 재확인
- [x] AR-02: validate-plugin.py · evals/ 미변경 — PASS
  - 근거: `git status --porcelain -- scripts/validate-plugin.py harness/evals/` 빈 출력.
    병합된 동시 브랜치(becab71) 기준으로도 `git diff --name-only 8f41a6d becab71 -- ...` 빈 출력 재확인
- [x] AR-03: 권위 단일화 — PASS
  - 근거: `.harness/project.yaml` AP-03 항목에 `pattern` 필드 없음(0건), `command` 만 존재 — 정규식 기반
    판정 로직 복제 없음

### Anti-patterns (2/2)
- [x] AP-01: 버전 하드코딩 없음 — PASS
  - 근거: `grep -inE "hardcoded.*version" <4 files>` — 매치는 `.harness/project.yaml:31` 의 패턴 정의
    문자열 자체뿐(실제 위반 아님), 대상 4파일·패턴 유효성 확인
- [x] AP-04: frontmatter name 필드 누락 없음 — PASS
  - 근거: `harness/agents/qa-evaluator.md:2` (`name: qa-evaluator`) 존재 확인 (변경 대상 중 유일한 agents/*.md)

### Reusability (2/2)
- [x] RE-01: 재사용 가능 컴포넌트 private화 없음 — PASS
  - 근거: 이번 diff(`+50/-7`, 4파일)는 스키마 필드 추가 + 문서 갱신뿐, 신규 컴포넌트 생성 없음
    (`git diff --stat 8f41a6d -- <4 files>` 확인)
- [x] RE-02: 기존 컴포넌트 재사용 — PASS
  - 근거: AP-03 `command` 가 신규 로직을 만들지 않고 기존 `scripts/validate-plugin.py --check=code-fence`
    를 그대로 호출 (AR-03 근거와 동일 지점)

### Diagnostics (4/4)
- [x] DG-01: `bash -n scripts/release.sh` 워닝 0개 — PASS
  - 근거: 실행 결과 무출력, exit 0
- [x] DG-02: N/A (사유: IDE diagnostics 미적용 확장자 .md/.yaml 만 변경) — PASS(N/A 정당)
  - 근거: 변경 대상 4파일 전부 .md 2개/.yaml 2개, `commands.lint: null`(project.yaml)로 이 스택엔 별도
    린터 미설정. `qa-evaluation-guide.md:1036` 의 정본 예시(`N/A (IDE diagnostics 미적용 확장자: .md/.html)`)와
    동일 패턴 — "잴 수 있는데 회피"가 아니라 "잴 것이 없음". 추가로 두 yaml 파일의 문법 유효성을
    `python3 -c "import yaml; yaml.safe_load(...)"` 로 별도 확인(VALID) — 숨은 진단 누락 없음 재확인
- [x] DG-03: 콘솔 에러/예외 0개 — PASS
  - 근거: 실행 결과 usage 메시지만 출력(에러/예외 아님), `diagnostics.console_errors: []` 이라 매칭 대상도 없음
- [x] DG-04: 오탐 292→0 수치 입증 — PASS
  - 근거: 옛 패턴 `grep -rEn '^```\s*$' harness/ bambu-kit/` = 292건 (재확인),
    신규 `command` 실행 결과 = "0 bare — OK" (13/13 plugins) — 292 → 0 수치 확인

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (21 - 0) / 21 = 1.00 (임계 0.60 충족)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상 (미검증 항목 없음)

## Discrimination (규칙 12 — 참고 적용, 9항목 강제 대상은 아니나 계약이 명시적으로 음성 대조를 요구)
- 적용 조건: SC-01, SC-03 (계약 자체가 "음성 대조:" 절을 명시)
- 결합 확인: SC-01 — AP-03 의 `command` 값을 그대로(literal) 실행 → validate-plugin.py 의 V6 상태기계를
  직접 경유. SC-03 — validate.sh 의 `AP_COUNT` 로직을 직접 경유
- 음성 대조: SC-01 — 실행함(위 근거), 무력화 시 FAIL 확인(exit 2). SC-03 — 실행함(위 근거), 무력화 시
  경고 발생 확인. 안전 조건(백업 diff 원상복구) 충족 후 실행, 사후 byte-identical 복원 검증 완료

## User-Reported Failures
- 해당 없음 (사용자 실패 보고 없음)

## Evidence Validity
- 검사 대상 증거: 21건 (조건별 1건 이상)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 실행 8건 (SC-01/SC-03 각 2회 + DG-04/AP-01/AP-04 등) · zsh 환경에서 전부 실행
  (사용자 셸 zsh 확인됨, bash 별도 재검증은 미실시 — 스니펫이 문서 산출물이 아니라 실행 명령 자체이므로
  해당 없음)
- 무효 0건은 미검증 카운터에 영향 없음 (누계 0)

## Summary
- Total: 21/21 conditions passed
- Verdict: APPROVE

## Improvement Suggestions
- 없음 (계약 모호성·중복·범위 미명시 없음). 단, 이번 스프린트 중 관측된 동시 편집 세션의 merge 는
  계약 결함이 아니라 워크플로우 이슈이므로 별도 기록하지 않음 (사용자가 이미 알고 있는 상황)
