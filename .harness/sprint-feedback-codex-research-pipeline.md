# Sprint Feedback
Feature: 코덱스 리서치 파이프라인 업그레이드
Evaluated: 2026-09-12 19:00
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-codex-research-pipeline.md
- sha256: 9f5614ab0b975dd9539e3a5eee478976ed7f6c79c6877410b1130d7f632ee31b
- status: active (평가 완료 후 done 으로 전환)
- slug: codex-research-pipeline
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 1 (명시경로 — 사용자가 절대경로로 지정)
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- 재확인(Step 5): 일치
- status_transition: active -> done

## Amendments
- amendments: 1 (A-01, SC-01/SC-02/SC-03/SC-04/ER-03 측정문 정정: `grep -c '^## '` → `grep -c '^- rollout: '`)
- amend_direction_oracle: narrowing (사이드카 자체 계산치. 4월 로그 5496→1597, 9월 로그 30→30 — 개정 측정이 세는 줄 집합이 더 작거나 같아 통과 여지가 줄어듦)
- consent: 명시적 anchor 없음(unanchored) — 그러나 narrowing 이므로 2축 표에 따라 PASS 근거 가능
- PASS 근거 가능: SC-01, SC-02, SC-03, SC-04, ER-03 (개정 측정 기준으로 판정)
- PASS 근거 불가: 0건

## User Correction Audit
- correction_log_status: available (~/.claude/logs/claude-plugins/2026-09.md)
- unreflected_corrections: 0 (소유 세션 f78b65b1 의 계약 락 이후 로그 4건은 전부 Bash 도구 호출 기록이며 방향 교정성 사용자 발화 없음)
- verdict 영향: 없음 (표면화 전용)

## Results

### Script (5/5)
- [x] SC-01: 신형식 세션 기록 추출 — PASS
  - 근거: 격리 실행(test_hook.sh, QA 독립 재실행) 결과 엔트리 1건, 프롬프트 비어있지 않음, `completed` 상태 기록. `harvest-codex-log.sh:119-133` `item_completed` 분기가 UserMessage/AgentMessage 를 `text_of()` 로 추출.
  - 음성 대조: `item_completed` 분기 제거 시 엔트리 0건 확인(negative_control.sh, QA 재실행) — 오라클 유효.
- [x] SC-02: 구형식 세션 기록 계속 추출 — PASS
  - 근거: 2026-04 rollout 격리 실행 → 엔트리 1건, 프롬프트 추출됨. `harvest-codex-log.sh:111-118` `user_message`/`agent_message` 분기.
  - 음성 대조: 두 분기 제거 시 0건 확인 — 오라클 유효.
- [x] SC-03: task_complete 없는 세션을 실패로 기록 + 마지막 항목 종류 — PASS
  - 근거: 미완료 rollout 격리 실행 → `stalled, auto-harvested` 상태 + `stalled after: \`Reasoning\`` 기록 확인(`harvest-codex-log.sh:144,161-163`).
  - 음성 대조: `if stalled and age < stall_seconds: continue` → `if stalled: continue` 로 되돌리면 0건 — 오라클 유효.
- [x] SC-04: 연속 실행해도 엔트리 1건 — PASS
  - 근거: 같은 임시 환경 3회 실행 후 `grep -c '^- rollout: '` == 1 (QA 독립 재실행 확인). 상태 파일 기반 `harvested` set 으로 재실행 무관.
- [x] SC-05: 검색 활동 수 기록 — PASS
  - 근거: 검색 포함 rollout 격리 실행 → `search calls: 1` 필드 + `### Search activity` 절 존재 확인(`harvest-codex-log.sh:134-139,160,166-169`).

### Error (3/3)
- [x] ER-01: 상한 초과해도 재기록 없음 — PASS
  - 근거: `harvest-codex-log.sh:208-212` 에 고정 상한(500) 코드 부재 확인(`grep -n '500'` 0건). 510개 복사 후 2회 실행 → 1회차 510건, 2회차 증가 0, 이름별 최대 중복 1(QA 독립 재실행).
  - 음성 대조: `harvested & present` 를 `sorted(...)[:5]` 로 되돌리면 중복 재발(2회 실행 후 최대 중복 2건, QA 독립 재실행 확인) — 오라클 유효.
- [x] ER-02: 깨진 입력에도 exit 0 — PASS
  - 근거: 잘린 JSON/빈 파일/권한 없는 파일 3종 넣고 실행 → 종료 코드 0(QA 독립 재실행). `harvest-codex-log.sh:185-189` 외부 try/except 가 `parse()` 예외를 흡수.
  - 주의(조건에는 없으나 설계상 특기): 이 3종은 상태 파일에 영구 harvested 로 등록되고 로그에는 **아무 흔적도 남지 않는다**(md 파일 자체가 생성 안 됨, QA 직접 확인). SC-03(task_complete 없음)과 달리 "실패를 흔적 없이 지운다"는 이 스프린트의 원래 문제의식과 같은 유형의 사각지대가 파싱 예외 클래스에는 그대로 남아 있다. 계약 문구상 ER-02 는 "exit 0"만 요구하므로 조건 자체는 PASS 이나, 향후 최소한 `errors` 필드에 1줄이라도 남기는 개선을 권장(Improvement 참조).
- [x] ER-03: 기존 엔트리 보존(덧붙이기만) — PASS
  - 근거: 기존 엔트리 파일 준비 후 실행 → `head -c <원본크기>` 바이트 단위 동일 확인(QA 독립 재실행). `open(out_path, "a", ...)` append 모드(`harvest-codex-log.sh:153`).

### Architecture (5/5)
- [x] AR-01: 틀린 지시 3종 제거 — PASS
  - 근거: `~/.claude/codex-prompt-template.md`(161줄) 에서 `내장 웹검색`/`내장 검색이 유일`/`검색.*hang|hang.*검색` 각 0건(QA 직접 grep). 양성 대조: 구버전 스냅샷(`template_old.md`)에 3개 패턴 각 1건 확인 — 패턴이 죽어서 0이 아니라 살아있는 패턴으로 정말 제거됨을 확인.
- [x] AR-02: 기준 모델 갱신 + template_version 상향 — PASS
  - 근거: `template_version: 2026-09-12-c`(2026-09-12-b 대비 갱신), 기준 모델 줄에 `gpt-6-astra` 와 `gpt-5.6-sol` 둘 다 존재(`codex-prompt-template.md:5`), 변경 이력 줄에 근거(세션 556개 실측, #44842) 명시(`codex-prompt-template.md:7`).
- [x] AR-03: MODE=research 절 안에 grounding 5원칙 모두 존재 — PASS
  - 근거: `awk` 로 `MODE=research` 절만 발췌(QA 직접 실행) 후 5개 문장 패턴 각 1건 이상 확인(`codex-prompt-template.md:68-71`).
- [x] AR-04: CLAUDE.md Codex 위임 규칙에서 `--model` 금지 제거 + `gpt-5.6-sol` 지침으로 대체 — PASS
  - 근거: `awk` 로 해당 절 발췌 후 `--model.*금지|금지.*--model` 0건, `gpt-5.6-sol` 1건 이상(QA 직접 확인, CLAUDE.md:38-63 구간).
  - 참고(계약 조건 자체에는 영향 없는 배경 오류): GAP 분석 서술은 "CLAUDE.md 에도 --model 전면 금지 규칙이 있었다"고 하지만, 스프린트 시작 시점 백업(`CLAUDE.md.bak`) 전체를 grep 해도 `--model`/`모델` 언급이 0건이다. 즉 CLAUDE.md 자체에는애초에 그런 금지 문구가 없었던 것으로 보인다(4곳은 전부 codex-kaizen/SKILL.md 쪽, 아래 SK-02 양성 대조 참조). 배경 서술의 사실관계 오류이며 GAP 분석은 파싱 대상 조건이 아니므로 verdict 에는 영향 없음 — Improvement 로만 기록.
- [x] AR-05: 변경 파일 정확히 4개 — PASS
  - 근거: `git status --porcelain -- reflect-kit` → `codex-kaizen/SKILL.md` 한 줄만(QA 직접 확인). 레포 밖은 계약 locked_at(18:30) 이후 mtime 을 가진 `~/.claude/hooks/harvest-codex-log.sh`, `~/.claude/codex-prompt-template.md`, `~/.claude/CLAUDE.md` 3개 — 그 외 newer 파일(`.plain-korean-last.json`, `mcp-needs-auth-cache.json`, `.claude.json.backup.*`)은 Claude Code 세션 자체의 배경 상태 파일로 이번 구현과 무관함을 내용 확인(QA 직접 cat) — 계약의 "다른 ~/.claude 파일이 섞이지 않는다"를 판정할 기준파일이 명시돼 있지 않아 평가자가 계약 locked_at 을 기준으로 사용했음을 명시.

### Skill (3/3)
- [x] SK-01: 신호 수집 절이 신형식(실패 엔트리·검색 활동) 반영 — PASS
  - 근거: `### 1. 신호 수집` 절(SKILL.md:48-62) 에 `stalled`·`Search activity` 문장 각 1건 이상(QA 직접 awk+grep). 실제 포맷 대조: `harvest-codex-log.sh` 의 실제 출력 필드(헤더 `— codex-rescue (`, `- rollout: `, `search calls:`, `### Search activity`, `model/cli/via`)가 SKILL.md 서술과 전부 일치함을 직접 대조 확인 — 단순 문서 갱신이 아니라 실제 포맷과 부합.
- [x] SK-02: `--model` 금지 규칙 4곳 전부 제거·교체 — PASS
  - 근거: 파일 전체(134줄) grep 0건(QA 직접 확인). 4곳 개별 대조(git show HEAD 구버전 vs 현재): (1) L32 "절대 전달 금지" → "모델을 명시해서 부른다" (2) L75 "`--model` 금지" → codex exec 호출 예시에 `--model gpt-5.6-sol` 명시 (3) L110 자기감사 "넘기지 않았는가" → "지정했는가" (4) L122 안티패턴 "넘기지 마라" → "모델 지정 없이 부르지 마라". 4곳 전부 금지→지정 요구로 정확히 반전됨을 확인(enumerated 전수 검증).
- [x] SK-03: gpt-5.5 기준 서술 갱신 — PASS
  - 근거: `grep -c 'gpt-5\.5'` 0건(QA 직접 확인, 구버전은 5건).

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 금지 — PASS
  - 근거: `python3 scripts/validate-plugin.py --check=code-fence reflect-kit` → V6 code-fence 0 bare(QA 직접 실행).
- [x] AP-04: frontmatter name 필드 누락 금지 — PASS
  - 근거: `python3 scripts/validate-plugin.py reflect-kit` → V1 frontmatter 4 skills OK, 전체 8항목 OK(QA 직접 실행).
- (참고) project.yaml 전역 AP-01/AP-02(하드코딩 버전/force push) 도 4개 변경 파일 전체에서 0건(QA 직접 grep).

### Reusability (2/2)
- [x] RE-01: 세션 기록 파싱이 단일 함수로 응집 — PASS
  - 근거: `harvest-codex-log.sh:72 def parse(path):` 단일 함수(QA 직접 확인, 파일 전체에 동일 역할 함수 중복 없음).
- [x] RE-02: 새 훅·로그·상태 파일 생성 없음 — PASS
  - 근거: `~/.claude/hooks/`, `~/.claude/codex-research-log/` 디렉터리에 기존 3파일(`harvest-codex-log.sh`, 월별 `.md`, `.harvested.json`) 외 신규 파일 없음(QA 직접 ls 확인).

### Diagnostics (3/4, 1 ENV)
- [x] DG-01: 훅 문법 오류 0건 — PASS
  - 근거: `bash -n ~/.claude/hooks/harvest-codex-log.sh` exit 0(QA 직접 실행). 부가로 `shellcheck` 0 warning(QA 직접 실행, 계약 요구 이상의 보강 증거).
- [미검증:ENV] DG-02: 편집기 진단 경고·정보 0건
  - 1차 도구 시도: `project.yaml.runtime_inspection.mcp_server: null` — IDE 진단 MCP 미설정, 이 평가 환경(headless Bash/Read)에는 IDE Problems 패널 접근 수단이 없음.
  - fallback 시도: `shellcheck ~/.claude/hooks/harvest-codex-log.sh` → 0 warning(QA 직접 실행). 3개 문서 파일(`codex-prompt-template.md`, `CLAUDE.md`, `SKILL.md`) 대상 줄끝 공백 `grep -cE ' +$'` 각 0건(QA 직접 실행). `command -v markdownlint` 없음 확인.
  - 실패 로그: `no markdownlint` (QA 직접 확인), MCP 서버 미설정(`project.yaml` 값 그대로 인용).
  - 통제 불가 사유 + 재검증 명령: 이 평가 세션에는 IDE 자체가 없다(구현자 환경에는 있을 수 있으나 QA 는 재현 불가). 재검증 명령: 세 파일을 VS Code 등 IDE 로 열어 Problems 패널 확인, 또는 `npm i -g markdownlint-cli && markdownlint ~/.claude/codex-prompt-template.md ~/.claude/CLAUDE.md reflect-kit/skills/codex-kaizen/SKILL.md`.
- [x] DG-03: 파이썬 오류 추적 0건 — PASS
  - 근거: 격리 실행 19항목의 실제 훅 stdout(`t_*/stdout.txt`)에서만 `Traceback` 카운트 = 0(QA 직접 재실행). 테스트 요약문 텍스트는 제외하고 훅의 실제 실행 출력만 집계 — 이전 회차에 발견된 "테스트 요약문의 'Traceback' 글자를 세는" 자기참조 오탐 패턴이 재발하지 않았음을 확인.
- [x] DG-04: 실제 환경 1회 실행 시 오류 0건 + 9월 로그 엔트리 증가 — PASS (단, 아래 중대 발견 참조)
  - 근거(QA 자체 수집, 구현자 스크립트 대체): 실제 `codex exec --model gpt-5.6-luna -s read-only` 로 신규 세션 1건을 생성(session `01a09507-9344-7921-85c9-58b65b5f1286`) → 20초 대기 후 실제 훅 실행 결과 `~/.claude/codex-research-log/2026-09.md` 의 `grep -c '^## '` 및 `grep -c '^- rollout: '` 가 실행 전 30/30 → 실행 후 31/31 로 증가, 종료 코드 0, 신규 엔트리 필드(`model: gpt-5.6-luna · cli: 0.154.0 · via: codex_exec`)까지 확인. **CLI 0.154.0(이번 스프린트가 고치려던 정확히 그 버전)의 실제 세션이 신형식 그대로 정상 수집됨을 실전 확인.**
  - **중대 발견 — 구현자의 자체 검증 스크립트(`verify_contract.sh`)의 DG-04 판정 로직이 눈먼 측정이다.**
    ```bash
    B9=$(grep -c '^- rollout: ' "$L/2026-09.md")
    bash "$H"; RC=$?
    A9=$(grep -c '^- rollout: ' "$L/2026-09.md")
    VIA=$(grep -c '· via: ' "$L/2026-09.md")
    if [ "$RC" = 0 ] && [ "$VIA" -ge 1 ]; then   # ← A9 와 B9 를 계산만 하고 비교하지 않는다!
    ```
    `A9`/`B9`(실행 전/후 카운트)를 계산해 로그 문구에는 출력하지만, 실제 PASS/FAIL 분기는 `RC == 0 && VIA >= 1` 만 본다. `VIA`(전체 누적 `· via: ` 개수)는 이번 스프린트 이전부터 이미 25건 이상 쌓여 있어 **훅이 이번 실행에서 아무 것도 하지 않아도 항상 참**이다. 실제로 QA 가 아무 변경 없이 이 스크립트를 재실행했을 때 "이번 실행 증가 0" 임에도 PASS 로 출력되는 것을 직접 확인했다(재현 로그 첨부 가능). 이것은 사용자가 우려한 "A-01(마크다운 제목 오카운트)·DG-03(Traceback 자기참조)"과 **동일 계열의 세 번째 사례**다 — 측정값은 정확히 계산하지만 그 값을 판정에 실제로 쓰지 않는 패턴. `negative_control.sh` 의 `probe()` 함수(17행)도 여전히 구버전 지표 `grep -c '^## '` 를 쓰고 있어(이번 데이터셋에서는 우연히 0/1 판정에 영향 없었지만) 잠재적으로 같은 유형의 재발 소지가 있다.
    이 결함은 계약이 지정한 4개 파일 밖(스크래치패드 테스트 스크립트)에 있어 계약 조건 자체를 FAIL 시키지는 않으며, QA 가 별도로 수집한 실행 증거로 DG-04 는 PASS 확정한다. 그러나 "구현자 주장: PASS=17 FAIL=0"의 DG-04 항목은 그 자체로는 신뢰할 수 없는 근거였다는 점을 기록한다.

## Design Judgment — 사용자 요청 특별 검토 항목

1. **눈먼 측정 재발 여부(요청 1)** — DG-04 검증 스크립트에서 세 번째 사례를 발견(위 참조). SC-01~04/ER-03 자체 계약 측정은 사이드카 A-01 로 이미 정정되어 정상. `negative_control.sh` 의 잔존 구버전 카운트는 이번 데이터셋에서는 판정에 영향 없었으나 잠재 위험으로 기록.
2. **0건이 죽은 패턴인지(요청 2)** — AR-01(3패턴), SK-02, SK-03 모두 구버전 스냅샷에 대한 양성 대조로 "패턴이 살아있고 실제로 제거됐다"를 확인. AR-04 는 패턴 자체는 살아있음(SK-02 동일 계열로 입증)이 확인됐으나, GAP 분석의 "CLAUDE.md 에도 금지문구가 있었다"는 배경 서술 자체가 사실과 다를 가능성 발견(비조건 서술, verdict 무관).
3. **`parse()` 예외 흡수 설계(요청 3)** — ER-02 의 "exit 0" 요구는 정당하게 충족된다(오라클 확인). 다만 부수적으로, 권한 오류·구조 이상 등 `parse()` 레벨 예외가 발생하는 세션은 흔적 없이 영구 드롭됨을 직접 확인 — 이는 SC-03 이 고친 "task_complete 없음" 케이스와 달리 여전히 조용히 사라지는 실패 유형이다. 계약 조건에는 없으나 스프린트의 원취지("실패가 영영 안 남는다")와 정확히 같은 유형의 잔여 사각지대이므로 Improvement 로 기록.
4. **SK-01 소비면 충분성(요청 4)** — 단순 문구 존재가 아니라 실제 훅 출력 포맷(헤더/필드명)과 SKILL.md 서술을 1:1 대조하여 일치를 확인. 신형식을 codex-kaizen 이 실제로 읽을 수 있는 설명으로 판단.

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 1  [DG-02 — IDE MCP 미설정 + markdownlint 미설치, shellcheck/trailing-whitespace fallback 수행, 재검증 명령 기재]
- verified_coverage: (24 - 1) / 24 = 0.96  (임계 0.60)
- 연속 ENV 승급: 해당 없음(1회차)
- Verdict 영향: 통상(APPROVE 가능 범위)

## Discrimination (규칙 12 적용 조건만)
- 적용 조건: 없음 (동시성 가드/인증/멱등성/입력검증/데이터유실/마이그레이션/재시도/보안경계/사용자결함보고충돌 9항목에 해당하는 조건 없음 — 이번 스프린트는 로그 수집 훅 정확성/문서 갱신 위주)

## Evidence Validity
- 검사 대상 증거: 24건(조건별) + DG-04 관련 구현자 스크립트 1건 추가 검사
- 무효 판정: 0건(조건 자체). 단, 구현자의 `verify_contract.sh` DG-04 판정 로직은 검사 3(반증가능성) 실패로 그 자체 증거로는 사용하지 않고 QA 자체 실행 증거로 대체함(위 DG-04 항목 참조)
- 셸 스니펫 실행 검증: 계약 내 셸 명령형 조건(SC/ER/AR/SK/AP/RE/DG 전부) 24건 중 24건을 QA 가 bash 로 직접 재실행(zsh 는 이 저장소 기본 셸이나 스크립트 자체는 bash 셔뱅이며 실행 결과 일치 확인)
- 무효 0건이므로 미검증 카운터 추가 합산 없음

## Summary
- Total: 23/24 conditions passed (1 ENV gap, 0 FAIL, 0 invalid)
- Verdict: APPROVE

## Improvement Suggestions
- [DG-04] 측정-방식-불일치 — `verify_contract.sh` 의 DG-04 판정 분기가 `A9`/`B9`(실행 전후 카운트)를 계산만 하고 비교식에 쓰지 않는다. `[ "$RC" = 0 ] && [ "$A9" -gt "$B9" ]` 로 교체 권장.
- [SC-01~04, ER-03 관련] 측정-중복 — `negative_control.sh` 의 `probe()` 함수(17행)가 사이드카 A-01 이전 지표(`grep -c '^## '`)를 여전히 사용한다. 이번 데이터셋에서는 응답 본문에 마크다운 제목이 없어 판정에 영향 없었으나, `grep -c '^- rollout: '` 로 통일 권장.
- [ER-02] 범위-미명시 — 계약은 "exit 0"만 요구해 조건은 PASS 이나, `parse()` 레벨 예외(권한 오류·비-dict JSON 구조)로 드롭되는 세션이 로그에 어떤 흔적도 남기지 않는다. 최소 `errors` 필드에 파일명 한 줄이라도 남기는 후속 조건을 고려 권장.
- [AR-05] 범위-미명시 — "다른 `~/.claude` 파일이 섞이지 않는다"의 기준파일(`<기준파일>`)이 계약에 명시되지 않아 평가자가 계약 `locked_at` 을 임의 채택했다. 다음 계약에는 구체적 기준 파일/시각을 명시 권장.
- [GAP 분석] 배경 서술 오류(비조건, verdict 무관) — "`--model` 전면 금지 규칙(CLAUDE.md, codex-kaizen 4곳)"에서 CLAUDE.md 부분은 스프린트 시작 시점 백업 전체를 검색해도 근거가 없다. 4곳은 전부 codex-kaizen/SKILL.md 소재였던 것으로 보인다.
