---
feature: "kaizen Phase 3 — Evaluator (qa-evaluation-guide · qa-evaluator) 증거 유효성 게이트 + Phase 1·2 정합화"
created: "2026-07-27 19:30"
complexity: "복잡"
conditions: 17
---

# Sprint Contract — Phase 3 Evaluator 카이젠

## 배경 · 이번 사이클 프레이밍

`/insights` 2026-07-27 의 Friction #1·#3 은 직전 사이클 승격분인데 세션당 비율이 줄지 않았다.
Phase 1·2 와 동일하게 **새 soft 문장 추가가 아니라 enforcement 등급 상향**이 이번 Phase 의
기본 전략이다. 등급 어휘(E1/E2/E3)의 SSOT 는 `skill-design-guide.md §3.7` 이며 여기서
재정의하거나 동의어를 만들지 않는다.

흡수 대상은 네 갈래로 한정한다:

1. **Friction #2 (신규 최상위)** — 평가자는 이미 증거의 *존재*를 요구한다(§Execution-Grounded
   Evidence). 못 잡는 것은 **증거가 있는데 그 증거가 무의미한 경우**다 (빈 스냅샷, 0 매치 grep,
   0 개 테스트 실행). 이번 Phase 는 증거의 *유효성* 축을 신설한다.
2. **Phase 1 이 넘긴 숙제** — agent-design-guide §10 Unverifiable 정책 4 항("생성자의 완료
   주장은 증거가 아니다")을 평가자 레이어에 착지시키고, 각 kit reviewer 6 종이 복제할
   **정본(canonical) 블록**을 한 곳에 고정한다.
3. **Phase 2 가 넘긴 정합화 6 지점** — 스키마 v4, 허용 섹션 헤더 2 계층 파싱, Counterpart 대응
   절 **비**신설, E 등급 SSOT, `[미검증]` 마커 의미 축소, feedback 스크립트 fallback.
4. **글로벌 evaluator 피드백 240 건의 반복 개선 제안** — 같은 제안이 반복된다는 것은 구조적
   미해결이라는 뜻이므로 "반복 제안 승급" 메커니즘으로 흡수한다.

## 리서치 소스 (필수 3+ 건 · 실제 4 건 조회)

Context7 MCP 는 이 세션에서 OAuth 미인증이라 사용 불가 → `phase-research-templates.md`
§Phase 3 의 fallback 인 WebFetch/WebSearch 로 1 차 출처를 직접 조회했다. 템플릿에 열거된 6 건은
이미 현행 가이드에 인용되어 있으므로, 이번 사이클 신규 신호(증거 유효성)에 맞는 소스를 조회했다.

- <https://arxiv.org/html/2606.22737v2> — GroundEval. 프런티어 LLM 판정자 2 종이 근거를 전혀
  가져오지 않은 답변에 0.90 / 0.85 를 부여("plausibility, not validity"). 결정론적 trace 대조
  시 answer score 0.000. 실패 분류: invalid absence / temporal leakage / permission leakage /
  invalid causality
- <https://arxiv.org/pdf/2603.03116> — Corrupt Success. 최종 상태만 보는 outcome-only 평가는
  절차 위반을 통과시켜 성능을 과대평가. 중간 상태·행위 시퀀스 대조 필요
- <https://arxiv.org/pdf/2606.21451> — LLM 생성 assertion 의 vacuity. trigger coverage /
  antecedent activation / mutation(negative control) 3 축으로 "통과했지만 아무것도 검사하지
  않은" assertion 을 걸러냄
- <https://code.claude.com/docs/en/plugins-reference> — `${CLAUDE_PLUGIN_ROOT}` 는 플러그인
  설치 디렉토리의 절대경로이며 **skill/agent 본문 어디에서나 치환**된다. 플러그인 업데이트 시
  경로가 바뀌므로 상태를 그 아래 쓰지 말 것

## GAP 분석

| # | 신호 (출처) | 현재 상태 | 갭 | 조치 |
| - | ---- | ---- | ---- | ---- |
| 1 | Friction #2 — 빈 스냅샷을 근거로 "정상 렌더링" 반복 주장 | §Execution-Grounded Evidence 는 산출물 **존재**만 요구 | 산출물이 있으나 **내용이 공허**한 경우 규칙 없음 | §Evidence Validity Gate 신설 (E2) |
| 2 | Phase 1 §10 4 항 | 평가자에 "주석은 증거가 아니다" 는 있으나 근거·명칭 없음 | 생성자 완료 주장 배제가 명시 정책으로 없음 | Evidence Validity Gate 4 번 항목 + canonical 블록 |
| 3 | Phase 1 drift 경고 — reviewer 6 종이 미검증 프로토콜 복제 중 | design 3 건 / backend·infra·rust 2 건 / planning 0 건 으로 임계 불일치 | 복제 원본이 없어 각자 변형 | canonical 블록을 고정 앵커로 신설 |
| 4 | Phase 2 #2 — 허용 섹션 헤더 2 계층 | 평가자는 계약 전체를 무구분 읽음 | 서술 섹션의 불릿을 조건으로 오파싱 가능 | Step 1.2 파싱 범위 확정 (E3 결정론적 명령) |
| 5 | Phase 2 #5 — `[미검증]` 의미 축소 | 미검증 = 모든 확인 불가 | **미완/부재를 미검증으로 세탁**하면 FAIL 이 1 건 허용 구간으로 샘 | 3-way triage 규칙 |
| 6 | digest — feedback-script-location-mismatch (3~4 건) | `bash harness/scripts/save-feedback.sh` 레포 상대경로 고정 | 타 프로젝트에서 항상 부재 → BLOCKED 또는 임의 경로 저장 | 경로 해석 ladder + degraded 저장 규약 |
| 7 | §1 Top 15 — 같은 개선 제안 반복 (측정 시점 / exact-goal / 중복 진단) | 매번 산문 권고로만 남김 | 반복이 축적돼도 승급 경로 없음 | Recurring Improvement Escalation |
| 8 | digest — stack-inappropriate-rust-antipatterns | anti_patterns 를 무조건 Grep | 스택 불일치 패턴을 그대로 판정 | 안티패턴 스택 정합성 규칙 |
| 9 | Phase 2 #1 — 스키마 v3 → v4 | 두 파일이 v3 를 참조 | 버전 drift | 참조 갱신 |
| 10 | Phase 2 #3 — Counterpart | 평가자 대응 절 없음(의도됨) | 후속 Phase 가 실수로 만들 위험 | parity 표에 "대응 절 없음" 명문화 |

## 범위 경계

- **변경 허용**: `harness/docs/guides/qa-evaluation-guide.md`, `harness/agents/qa-evaluator.md`
  두 파일 + 본 계약 파일 + `.harness/history/` 아카이브
- **변경 금지**: Phase 1·2 산출물 5 종(`skill-design-guide.md`, `agent-design-guide.md`,
  `contract-design-guide.md`, `sprint-contract/SKILL.md`, `contract-schema.md`) 및 각 kit
  reviewer 6 종 — 후속 Phase 소관
- 브랜치 생성·push·PR 금지. 커밋까지만

## 회귀 게이트

- `python3 scripts/validate-plugin.py` 전 kit OK · Exit 0
- Diff-Scope Oracle baseline (계약 작성 시점 실행):
  `git diff --name-only HEAD -- harness/ ':(exclude)*.json'` → 0 행

## Skill

- [ ] SK-01: `harness/docs/guides/qa-evaluation-guide.md` 에 증거 **유효성**(존재가 아니라 내용)
      을 판정하는 신규 절이 있고, 최소 4 개의 유효성 검사 항목을 표 또는 번호 목록으로 열거한다
      [structural] (측정: 해당 절 Read 후 검사 항목 수 >= 4)
- [ ] SK-02: 신규 리서치 URL 3 건이 같은 파일 References 절에 **각각** 명시된다
      [exact, enumerated] (측정: `arxiv.org/html/2606.22737`, `arxiv.org/pdf/2603.03116`,
      `arxiv.org/pdf/2606.21451` 3 개 문자열 각각 grep 1 건 이상)
- [ ] SK-03: `[미검증]` 마커 절에 **FAIL / `[미검증]` / 증거무효** 를 가르는 triage 규칙이
      있고, "`[미검증]` 은 검증 도구·환경 부재 전용" 이라는 취지의 문장이 존재한다
      [structural] (측정: 해당 절에 3 분기 표 또는 목록 + 도구 부재 전용 문장 Read 확인)
- [ ] SK-04: 계약 파싱 범위를 **조건 섹션 / 서술 섹션** 2 계층으로 구분하는 절이 있고,
      서술 섹션을 조건 파싱 대상에서 제외한다는 규칙과 결정론적 확인 명령이 포함된다
      [structural] (측정: 절 존재 + `awk` 또는 `grep` 명령 블록 1 개 이상)
- [ ] SK-05: 동일 개선 제안이 반복될 때 이를 승급 처리하는 절이 있다 [structural]
      (측정: 절 존재 + 승급 조건(반복 횟수 등) 1 개 이상 명시)
- [ ] SK-06: 각 kit reviewer 가 복제할 **정본 블록**이 고정된 제목의 독립 절로 존재하고,
      미검증 임계값이 `2` 로 명시된다 [exact] (측정: 절 제목 grep + 블록 내 "2 건" 문자열 확인)
- [ ] SK-07: 평가자 원칙의 Enforcement 등급 표가 있고, 등급 정의의 SSOT 가
      `skill-design-guide` §3.7 임을 명시하며 재정의 금지 취지 문장을 포함한다 [structural]
      (측정: 표 존재 + `skill-design-guide` 문자열 grep + 금지 문장 Read 확인)

## Script

- [ ] SC-01: `harness/agents/qa-evaluator.md` Process 에 계약 파싱 범위를 확정하는 단계가
      Step 1 과 Step 1.5 사이에 존재한다 [structural] (측정: Step 헤더 순서 Read 확인)
- [ ] SC-02: 같은 파일 피드백 저장 단계에 `${CLAUDE_PLUGIN_ROOT}/scripts/save-feedback.sh`
      literal 이 포함된다 [exact] (측정: 해당 문자열 grep 1 건 이상)
- [ ] SC-03: 스크립트 부재 시의 degraded 절차가 있고, (a) 임의 경로 저장 금지 (b) 저장 실패가
      verdict 를 무효화하지 않음 두 취지가 모두 서술된다 [structural]
      (측정: 두 취지 문장 각각 Read 확인)
- [ ] SC-04: 기본 엄격도 규칙에 (a) 증거 유효성/공허한 증거 (b) 미검증-FAIL 구분 두 규칙이
      각각 신규 번호 항목으로 추가된다 [structural] (측정: 규칙 번호 항목 2 개 Read 확인)

## Error

- [ ] ER-01: 안티패턴 검증에서 **대상 스택과 무관한 패턴**을 그대로 판정하지 않는 규칙이
      두 파일 중 최소 1 곳에 존재한다 [structural] (측정: 스택 불일치 처리 문장 grep)
- [ ] ER-02: `qa-evaluator.md` Binary Decidability Pre-Check 체크 항목에 **상태 전제**
      (working tree / staged / 브랜치 비교) 확인 항목이 추가된다 [structural]
      (측정: Step 1.5 항목 수 증가 + 상태 전제 문구 Read 확인)

## Architecture

- [ ] AR-01: 이번 스프린트의 `harness/` 하위 변경이 2 개 파일로 한정된다
      [exact, enumerated] (Given: 커밋 직전 working tree ·
      측정: `git diff --name-only HEAD -- harness/ ':(exclude)*.json'` 결과가
      `harness/agents/qa-evaluator.md`, `harness/docs/guides/qa-evaluation-guide.md`
      2 행과 정확히 일치 · 작성 시점 baseline = 0 행)
- [ ] AR-02: 두 파일의 스키마 참조가 v4 로 갱신된다 [exact, enumerated]
      (측정: `qa-evaluation-guide.md` 와 `qa-evaluator.md` 각각에서 `contract-schema` 를 포함한
      행에 `v3` 가 0 건이고 `v4` 가 1 건 이상)
- [ ] AR-03: Counterpart Conditions 의 평가자 대응 절을 **만들지 않았고**, parity 표에 그
      설계 결정이 기록된다 [structural] (측정: `qa-evaluation-guide.md` 에 Counterpart 제목의
      독립 절이 0 건 + parity 표 item 12 행에 대응 절 부재 취지 명시)
- [ ] AR-04: Phase 1·2 소관 5 파일이 변경되지 않는다 [exact, enumerated]
      (Given: 커밋 직전 working tree · 측정:
      `git diff --name-only HEAD -- harness/docs/guides/skill-design-guide.md harness/docs/guides/agent-design-guide.md harness/docs/guides/contract-design-guide.md harness/skills/sprint-contract/SKILL.md harness/references/contract-schema.md`
      결과가 0 행)

## Anti-patterns

- [ ] AP-01: 변경 파일에 bare code fence (` ``` ` 단독) 가 0 건이다 [exact]
      (측정: `grep -c '^```$'` 두 파일 각각 0)
- [ ] AP-02: 등급 어휘 E1/E2/E3 를 재정의하거나 동의어를 신설하지 않는다 [structural]
      (측정: 변경 파일에서 등급 정의 표가 SSOT 를 가리키는지 Read 확인)

## Reusability

- [ ] RU-01: reviewer 6 종이 복제할 내용이 canonical 블록 1 곳에 모여 있고, 같은 내용이 두 파일
      안에서 중복 정의되지 않는다 [structural] (측정: 정본 블록 1 개 + `qa-evaluator.md` 는
      해당 블록을 참조만)

## Diagnostics

- [ ] DG-01: `python3 scripts/validate-plugin.py` 가 전 kit OK 이고 Exit 0 이다 [exact]
      (측정: 명령 실행 출력 + `echo $?`)
