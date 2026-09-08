# Sprint Feedback
Feature: howto-kit 설계 브리프 + /howto SKILL.md 초안
Evaluated: 2026-09-07 18:00
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-howto-kit-design-brief.md
- sha256: f66668a75e9d5da6abae5fbce79c37eed160dd82f34f6676caff67d0dab99086
- status: active
- slug: howto-kit-design-brief
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (호출 인자로 절대경로 지정, test -f 확인 후 사용)
- legacy_contract_used: false
- seal_status: SEAL_OK (recorded=dee06e6878247d76, actual=dee06e6878247d76)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (sha256/status 저장 직전 재확인 OK)
- status_transition: active -> done (verdict APPROVE)

## Amendments
- amendments: 0 (사이드카 `sprint-amendments-howto-kit-design-brief.md` 부재 — 정상, 결함 아님)

## User Correction Audit
- correction_log_status: available (`~/.claude/logs/claude-plugins/2026-09.md`)
- unreflected_corrections: 0 — 스프린트 기간(2026-09-07 16:45 계약 생성 ~ 17:35 locked ~ 평가 시각) 동안
  세션 `129c9ed3-…` 의 유일한 prompt 는 17:31:59 "ㄱㄱ"(진행 승인)뿐이며 방향 교정 성격 아님
- verdict 영향: 없음 (표면화 전용)

## Results

### Skill (4/4)
- [x] SK-01: frontmatter 3필드(name/description/user-invocable) 존재 — PASS [exact, enumerated]
  - 측정값: 3 (기준: == 3)
  - 근거: `awk 'NR==1&&/^---$/{f=1;next} f&&/^---$/{exit} f' docs/howto-kit/drafts/SKILL.md | grep -cE '^(name|description|user-invocable):'` → `3`. docs/howto-kit/drafts/SKILL.md:2,3,13
- [x] SK-02: 비트리거 조건 3건 이상 — PASS [structural, collective]
  - 측정값: 3 (기준: >= 3)
  - 근거: `grep -c '트리거하지 않는다' docs/howto-kit/drafts/SKILL.md` → `3`. SKILL.md:9(문서화 요청)·10(검수 요청)·11(코드 작성 요청)
- [x] SK-03: 500줄 이하 — PASS [exact]
  - 측정값: 255 (기준: <= 500)
  - 근거: `wc -l < docs/howto-kit/drafts/SKILL.md` → `255`
- [x] SK-04: F1~F4 토큰 전부 등장 — PASS [exact, enumerated]
  - 측정값: 4/4 토큰 검출, 누락 0줄
  - 근거: `for t in F1 F2 F3 F4; do grep -qF "$t" docs/howto-kit/drafts/SKILL.md || echo "MISSING $t"; done` → 출력 0줄. SKILL.md:27-30 결함표에 F1~F4 전부 등장

### Script (0/0, N/A 1건)
- [~] SC-00: N/A — 이번 스프린트 산출물은 docs/ 문서 2종뿐이며 scripts/release.sh·plugin.json·marketplace.json 을 읽지도 쓰지도 않는다
  - 근거: AR-01 diff-scope 측정 결과(아래)가 이 files 무터치를 실측으로 뒷받침 — `git status --porcelain` 출력에 scripts/·plugin.json·marketplace.json 관련 라인 0건

### Error (3/3)
- [x] ER-01: "확인 못 한 것" 섹션 번호 항목 5건 이상 — PASS [structural, collective]
  - 측정값: 8 (기준: >= 5)
  - 근거: `sed -n '/^## 11\./,/^## 12\./p' docs/howto-kit/design-brief.md | grep -cE '^[0-9]+\. '` → `8`. §11 확인 (line 382-396, 헤더 위치 grep으로 경계 검증 완료)
- [x] ER-02: `[미확인]` + "시도한 URL" 동시 등장 — PASS [exact, enumerated]
  - 측정값: `[미확인]`=3(기준 >=1), "시도한 URL"=2(기준 >=1)
  - 근거: `grep -c '\[미확인\]' docs/howto-kit/drafts/SKILL.md` → 3, `grep -c '시도한 URL' docs/howto-kit/drafts/SKILL.md` → 2. SKILL.md:57,68,206 / 68,206
- [x] ER-03: "학습 데이터로 채우지 않는다" 문구 등장 — PASS [exact]
  - 측정값: 1 (기준: >= 1)
  - 근거: `grep -c '학습 데이터로 채우지 않는다' docs/howto-kit/drafts/SKILL.md` → `1`. SKILL.md:206

### Architecture (4/4)
- [x] AR-01: diff-scope가 baseline 3건과 정확히 일치 — PASS [exact, enumerated]
  - Given: 커밋하지 않은 워킹트리 상태 (계약 §범위 경계에 명시된 상태 그대로 사용)
  - 측정값: `git status --porcelain -- . ':(exclude)docs/howto-kit' ':(exclude)docs/howto-kit/*'` →
    ```
    ?? .harness/sprint-contract-howto-kit-design-brief.md
    ?? docs/bambu-calibration/
    ?? result.json
    ```
    계약이 기대한 3줄과 순서·내용 정확히 일치 (뒤 2건은 §범위 경계에 기록된 사전 존재 미추적 파일, baseline)
- [x] AR-02: onboarding-kit/ 무수정 — PASS [exact]
  - 측정값: 0줄 (기준: 0)
  - 근거: `git status --porcelain -- onboarding-kit` → 출력 없음
- [x] AR-03: 산출물 2종 경로 확인 — PASS [exact, enumerated]
  - 근거: `test -f docs/howto-kit/design-brief.md && test -f docs/howto-kit/drafts/SKILL.md` → 성공. `find docs/howto-kit -type f` → 정확히 이 2 파일만 존재
- [x] AR-04: `| C<숫자>` 행 10건 이상 — PASS [structural, collective]
  - 측정값: 14 (기준: >= 10)
  - 근거: `grep -cE '^\| C[0-9]+' docs/howto-kit/design-brief.md` → `14`. design-brief.md:363-376 (C1~C14)

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 0건 (여는 fence 상태기계 직접 측정) — PASS [exact, enumerated]
  - 근거: `scripts/validate-plugin.py` V6 의 상태기계 로직(529-539행)을 그대로 재구현해 두 파일에 직접 실행 → `design-brief.md`: 0 bare, `SKILL.md`: 0 bare, TOTAL=0.
    계약의 주장(V6가 `docs/`를 스캔하지 않음)도 `python3 scripts/validate-plugin.py --check=code-fence` 실행으로 별도 확인 — 13개 킷 전부 OK, docs/howto-kit 자체는 스캔 대상에 없음(claim 정확)
- [x] AP-04: frontmatter `name` 필드 존재 — PASS [exact]
  - 측정값: 1 (기준: >= 1)
  - 근거: SK-01과 동일 awk로 추출한 frontmatter에 `^name:` → `1`. SKILL.md:2 `name: howto`

### Reusability (2/2)
- [x] RE-01: 재사용 가능 컴포넌트를 private으로 만들지 않음 — PASS [L3 의미 검증]
  - 근거: `find docs/howto-kit -type f` → design-brief.md, drafts/SKILL.md 2개뿐. 코드/컴포넌트 산출물이 전무한 문서 전용 스프린트이므로 "private 스코프된 재사용 컴포넌트"가 존재할 수 없다. 위반 대상 부재를 대상 파일 수(2, 둘 다 산문)로 확인
- [x] RE-02: onboarding-kit 재사용 자산 열거·승계 여부 명시 — PASS [structural, collective]
  - 측정값: 7 (기준: >= 3)
  - 근거: `grep -c 'search-strategy\|format-checklist\|출처 원장' docs/howto-kit/design-brief.md` → `7`. design-brief.md §2(승계 판단 근거), §9(feedback_*.md 인용)에서 onboarding-kit 자산을 구체적으로 열거·평가

### Diagnostics (2/4 확정, 2건 [미검증:ENV])
- [x] DG-01: `bash -n scripts/release.sh` 워닝 0개 — PASS
  - 근거: `bash -n scripts/release.sh` → 종료코드 0, 출력 없음 (구문 오류 없음). 이번 스프린트는 이 스크립트를 변경하지 않았으므로 회귀 없음 확인용 조건이며 그대로 성립
- [~] DG-02: IDE diagnostics 워닝/인포 0개 (MD025 제외) — [미검증:ENV]
  - 1차 도구 시도: 실제 IDE Problems 패널/에디터 MCP 접근 도구가 이 QA 에이전트 tools(Read, Grep, Glob, Bash)에 없음 — 시도 불가 자체를 확인
  - fallback 시도: `npx --no-install markdownlint-cli2 docs/howto-kit/design-brief.md docs/howto-kit/drafts/SKILL.md` 실행 → 122건(대부분 MD013 line-length, 일부 MD041/MD058) 검출
  - 실패 로그(판별력 검증): 같은 도구·같은 기본설정을 이 레포의 기존 SSOT 파일(`harness/docs/guides/contract-design-guide.md` — 이미 배포·승인된 문서)에 실행한 결과도 MD013 대량 검출(1128-1202행 구간만 21건). 이는 이 레포가 markdownlint 기본 룰셋(80자 줄바꿈 등)을 실제 컨벤션으로 채택하지 않았다는 반증이다 — repo에 `.markdownlint.json`, package.json markdownlint 의존성, CI 워크플로우(`.github/workflows/ci.yml`) 어디에도 markdownlint 설정/스텝이 없음(직접 확인)
  - 통제 불가 사유: 이 프로젝트는 markdown IDE lint 도구를 구성하지 않았다(project.yaml diagnostics.ide_exclude가 `[]`인 것과 별개로, 애초에 markdown lint 자체가 툴체인에 없음). 기본 설정 markdownlint-cli2를 오라클로 쓰면 이미 승인된 SSOT 문서군 전체가 동반 FAIL하는 stack-inappropriate 판정이 되므로 이 조건에서 오라클로 채택하지 않는다
  - 재검증 명령: 프로젝트에 `.markdownlint.json`을 실제 컨벤션(줄바꿈 무제한, MD025 제외 등)에 맞게 신설한 뒤 `npx markdownlint-cli2 --config .markdownlint.json docs/howto-kit/*.md docs/howto-kit/drafts/*.md` 재실행
- [x] DG-03: 콘솔 로그 에러/예외 0개 (`</dev/null`로 무인자 실행) — PASS
  - 근거: `bash scripts/release.sh 2>&1 </dev/null || true` → "Usage: bash scripts/release.sh <plugin-name> <patch|minor|major>" + 사용 가능 플러그인 목록 출력, 종료코드 0. error/exception 패턴 없음(project.yaml diagnostics.console_errors가 `[]`라 매칭 대상 자체가 없음도 확인)
- [~] DG-04: 실제 앱/서버 구동 시 에러 0개 — [미검증:ENV]
  - 1차 도구 시도: project.yaml `runtime_inspection.mcp_server: null` 확인 — Step 3 문서화된 기본 degrade 경로(MCP 미설정 시 정적 검증만)에 해당
  - fallback 시도: 이번 스프린트 산출물은 실행 가능한 앱/서버가 아니라 정적 마크다운 문서 2종(design-brief.md, SKILL.md 초안)이므로 "구동"할 대상 자체가 없음 — 정적 fallback도 원천적으로 적용 불가
  - 실패 로그: `grep -n 'mcp_server' .harness/project.yaml` → `mcp_server: null`
  - 통제 불가 사유: 이 프로젝트(claude-plugins 모노레포)는 runtime_inspection이 전역 미설정이며, 이번 스프린트는 §복잡도 판정에서 명시한 "문서만" 산출물이라 실행 가능한 런타임이 존재하지 않는다. 재검증 명령: howto-kit이 실제로 구현되는 다음 세션에서 해당 스킬을 실행하며 재평가 (`/howto` 실행 로그 확인)

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 2  [DG-02: markdown lint 미구성 + 기본설정 오탐 실증(SSOT 파일 동반 FAIL) / DG-04: mcp_server null + 실행 가능 런타임 부재(문서 전용 산출물)]
- verified_coverage: (19 - 2) / 19 = 0.89  (SC-00 N/A 1건 제외한 19건 분모, 임계 0.60)
- 연속 ENV 승급: 해당 없음 (Iteration 1, 직전 iteration 없음)
- Verdict 영향: 통상 (env_gaps는 자동 REJECT 카운터에 비합산, invalid_evidence 0건이므로 자동 REJECT 미해당)

## Discrimination
- 규칙 12(Discriminating Evidence Gate) 적용 대상 없음 — 이 스프린트에 동시성/인증/멱등성/입력검증/데이터유실/마이그레이션/재시도/보안경계/사용자보고-테스트충돌 유형 조건 없음 (문서 산출물 20조건 전부 구조·존재·문구 검증)

## User-Reported Failures
- 해당 없음 — 이번 평가에 선행 사용자 실패 보고 없음 (Iteration 1)

## Evidence Validity
- 검사 대상 증거: 20건 (조건 수 기준, N/A 1건 포함)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 20/20 조건의 인라인 측정 명령 전부 실제 실행(zsh 환경, bash 서브셸 아님 — 이 세션 자체가 zsh Bash 도구). AP-03만 계약 지정 명령(`validate-plugin.py --check=code-fence`)이 산출물 스캔 범위 밖이라는 계약의 자체 주장을 검증하기 위해 상태기계 로직을 직접 재구현해 추가 실행
- 무효 0건은 미검증 카운터에 영향 없음

## Summary
- Total: 17/19 conditions passed (2 conditions [미검증:ENV], 1 condition N/A)
- Verdict: APPROVE
- 봉인 검증: SEAL_OK — conditions_digest(dee06e6878247d76)가 현재 조건 체크박스 줄과 정확히 일치. 조건 문구 변조 없음
- DG-02·DG-04는 구현 결함이 아니라 이 프로젝트/스프린트의 구조적 환경 한계(markdown lint 미구성, 문서 전용 산출물이라 런타임 부재)이며 4요건(1차시도·fallback·실패로그·통제불가사유+재검증명령)을 모두 충족해 `env_gaps`로 처리했다. verified_coverage 0.89 >= 0.60 이므로 커버리지 게이트 통과

## Improvement Suggestions
- [DG-02] 검증경로-미기재 — "IDE diagnostics 워닝/인포 0개"에 인라인 측정 명령이 없다(다른 19개 조건은 전부 `측정: <command>`를 명시하는데 DG-02만 예외). 다음 계약에서는 이 프로젝트가 실제로 채택한 markdown lint 설정(`.markdownlint.json` 신설 후 그 설정 기준)을 측정 명령으로 명시하거나, 이 스택(shell-scripts/docs)에서는 markdown IDE lint 자체가 미구성임을 §범위 경계에 기록해 조건에서 제외할 것을 권장
- [DG-04] 검증경로-미기재 — "실제 앱/서버 구동" 조건이 문서 전용 산출물 스프린트에도 boilerplate로 포함되어 있다. project.yaml의 Diagnostics 카테고리가 모든 계약에 기계적으로 4개 조건을 복제하는 대신, 산출물 유형(문서 vs 코드)에 따라 DG-04를 조건부로 생략하거나 N/A 처리하는 규칙을 sprint-contract 스킬에 추가할 것을 권장
