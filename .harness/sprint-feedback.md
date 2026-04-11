# Sprint Feedback
Feature: skill-design-guide / agent-design-guide Phase 1 Kaizen Research Mode
Evaluated: 2026-04-11 19:30
Verdict: APPROVE
Iteration: 1

## Results

### SG (skill-design-guide.md) (11/11)

- [x] SG-01 [exact]: frontmatter 규칙 4가지 모두 명시 — PASS
  - 근거: `skill-design-guide.md:167-180` — `name` 최대 64자, 소문자+숫자+하이픈만 허용, XML 태그 금지, 예약어(anthropic, claude) 금지 명시. `description` 최대 1024자(line 177), 비어 있을 수 없음(line 178), XML 태그 금지(line 179), 3인칭 작성 필수(line 180) 명시.
  - L3 검증: §4 "frontmatter 필드 규칙 (공식 스키마)" 서브섹션으로 구조화되어 있으며, 각 규칙이 명시적 항목으로 나열됨.

- [x] SG-02 [exact]: "undertrigger" 개념 + "pushy" 이유 + 예시 1건 이상 — PASS
  - 근거: `skill-design-guide.md:199-219` — §4 "Undertrigger 경향과 'pushy' 디스크립션" 서브섹션. line 201-203에 undertrigger 정의와 "pushy" 이유 설명. line 206-219에 Bad/Good 예시 1쌍 수록.
  - L3 검증: 출처 URL `skill-creator SKILL.md`가 line 200-201에 명시됨.

- [x] SG-03 [structural]: "Degrees of Freedom" 섹션 — high/medium/low + 예시 + L1/L2/L3 충돌 참조 노트 — PASS
  - 근거: `skill-design-guide.md:371-396` — §5.5 "Degrees of Freedom — 자유도를 태스크에 맞춰라". line 377-381에 high/medium/low 표와 사용 시점. line 383-385에 예시(낭떠러지/들판 비유). line 387-394에 L1/L2/L3 네이밍 충돌 해결 참조 노트 1줄 이상.
  - L3 검증: 출처 URL이 line 373-374에 인용됨. L1/L2/L3 vs High/Medium/Low 구분을 명시적으로 설명.

- [x] SG-04 [exact]: Reference 1-level deep + 나쁜 예 vs 좋은 예 비교 블록 — PASS
  - 근거: `skill-design-guide.md:328-357` — §5 "Reference 파일은 1-level deep (필수)". line 334-345에 Bad 예시(3단계 중첩), line 347-355에 Good 예시(1-level flat). 출처 URL이 line 329-330에 인용됨.
  - L3 검증: Bad/Good 코드 블록 두 개가 markdown 언어 힌트와 함께 명시됨.

- [x] SG-05 [exact]: SKILL.md body 500 라인 상한 + 초과 시 분리 권고 — PASS
  - 근거: `skill-design-guide.md:316-326` — "SKILL.md 본문 500 라인 상한 (공식)" 서브섹션. line 320에 "500 라인 미만으로 유지한다" 명시. line 322-324에 `references/`, `templates/`, `scripts/`로 분리 권고.
  - L3 검증: 출처 URL이 line 317-318에 인용됨.

- [x] SG-06 [exact]: Evaluation-Driven Development — 최소 3개 eval 먼저 + with-skill vs baseline 비교 — PASS
  - 근거: `skill-design-guide.md:469-511` — §8.5 "Evaluation-Driven Development". line 478-481에 5단계 개발 루프 중 "최소 3개 시나리오 작성"(step 2)과 "baseline 측정"(step 3) 포함. with-skill vs baseline 비교 개념이 step 5 "baseline 대비"로 명시됨.
  - L3 검증: 출처 URL이 line 470-471에 인용됨. Eval 구조 예시(JSON)도 line 485-496에 포함.

- [x] SG-07 [exact]: Naming convention — gerund form 권장 + 금지 예약어 + 소문자+하이픈 규칙 — PASS
  - 근거: `skill-design-guide.md:167-174` — `name` 필드 규칙 항목. line 172에 gerund form(`processing-pdfs`, `analyzing-spreadsheets`, `testing-code`) 권장. line 173-174에 허용 대안과 금지 이름(`helper`, `utils`, `tools`) 명시. line 169에 소문자+숫자+하이픈만 허용. line 171에 예약어 금지(anthropic, claude).
  - L3 검증: 구체적인 예시가 각 규칙과 함께 인라인으로 제공됨.

- [x] SG-08 [exact]: MCP 도구 fully-qualified name 필수 + `ServerName:tool_name` 형식 — PASS
  - 근거: `skill-design-guide.md:515-537` — §8.6 "MCP 도구 참조 — Fully-Qualified Name 필수". line 521에 `ServerName:tool_name` 형식 명시. line 523-528에 Good 예시, line 530-534에 Bad 예시.
  - L3 검증: 출처 URL이 line 516-517에 인용됨.

- [x] SG-09 [structural]: 각 새 섹션·개정 섹션에 출처 URL 최소 1개 — PASS
  - 근거: 검증 대상 섹션 전수 확인.
    - §4 (Undertrigger): `skill-design-guide.md:156-157` URL 인용
    - §5 (1-level deep): line 329-330 URL 인용
    - §5.5 (Degrees of Freedom): line 373-374 URL 인용
    - §8.5 (EDD): line 470-471 URL 인용
    - §8.6 (MCP): line 516-517 URL 인용
  - L3 검증: 모든 신규/개정 섹션에 `> **출처:**` 블록쿼트 형식으로 URL이 포함됨.

- [x] SG-10 [exact]: 코드 펜스 언어 힌트 누락 0건 — PASS
  - 근거: Grep `^```\s*$` 결과 모두 닫는 펜스였고, 여는 펜스(`^```[^`\n]`) 전수 검색에서 `text`, `markdown`, `yaml`, `json` 등 언어 힌트가 모두 존재.
  - L3 검증: `validate-plugin.py` 실행 결과 "V6 code-fence 0 bare — OK" (harness 포함 7 킷 전부).

- [x] SG-11 [exact]: last_updated `2026-04-11`, version `1.1.0` — PASS
  - 근거: `skill-design-guide.md:3-4` — `version: 1.1.0`, `last_updated: 2026-04-11`.
  - L3 검증: frontmatter 실제 필드 값 일치 확인.

---

### AG (agent-design-guide.md) (9/9)

- [x] AG-01 [exact]: "use proactively" 공식 의미 + undertrigger 방지 메커니즘 명시 — PASS
  - 근거: `agent-design-guide.md:113-136` — §3 "use proactively 키워드 — 공식 언더트리거 방지 메커니즘" 서브섹션. line 114-115에 undertrigger 정의와 Anthropic 공식 문서 인용. line 117-129에 Good 예시 2건. line 131-136에 적용 체크리스트.
  - L3 검증: 출처가 line 94에 Anthropic 공식 문서 직접 인용됨.

- [x] AG-02 [exact]: frontmatter 표에 `color`, `initialPrompt` 필드 포함 — PASS
  - 근거: `agent-design-guide.md:85-86` — 표의 두 개 행: `initialPrompt` (line 85)와 `color` (line 86).
  - L3 검증: 두 필드 모두 표에 설명과 함께 명시됨.

- [x] AG-03 [exact]: "Subagents cannot spawn subagents" Gotchas에 포함 — PASS
  - 근거: `agent-design-guide.md:391` — §10 Gotchas 첫 번째 항목: "서브에이전트는 다른 서브에이전트를 생성할 수 없다."
  - L3 검증: 이미 이전 버전에서 존재하던 항목이 유지됨.

- [x] AG-04 [exact]: `Agent(agent_type)` 문법 + 화이트리스트 방식 설명 — PASS
  - 근거: `agent-design-guide.md:183-204` — §4 "Agent(agent_type) — 스폰 가능 서브에이전트 제한" 서브섹션. line 189-195에 yaml 예시. line 198-203에 화이트리스트 규칙 4가지 명시.
  - L3 검증: 출처 URL이 line 184-185에 인용됨.

- [x] AG-05 [structural]: 도구 스코핑 표 역할 5종 이상 + 2026 공식 4종 역할 정합 — PASS
  - 근거: `agent-design-guide.md:151-158` — 표에 7개 역할: 읽기 전용 리뷰어(line 152), QA 평가자(line 153), 연구자(line 154), 구현자(line 155), 문서 작성자(line 156), 데이터 분석가(line 157), 아키텍트/PM(line 158).
  - L3 검증: 공식 4종(read-only reviewer, research, code writer, docs) 모두 표에 포함됨.

- [x] AG-06 [exact]: §10 "계약 모호성 방지" Gotcha + `[exact]`/`[structural]`/`[goal]` 태그 언급 — PASS
  - 근거: `agent-design-guide.md:411-415` — §10 "계약 모호성 방지" 항목. line 414에 `[exact]`, `[structural]`, `[goal]` 태그가 명시적으로 언급됨: "계약이 `contract-design-guide.md` §5 의 구체성 레벨 (`[exact]` / `[structural]` / `[goal]`) 태그를 사용하면..."
  - L3 검증: PH-01 fix 확정 조건 충족.

- [x] AG-07 [structural]: 각 새 섹션·개정 섹션에 출처 URL 최소 1개 — PASS
  - 근거:
    - §1 (에이전트 vs 스킬): `agent-design-guide.md:22` URL 인용
    - §2 (파일 구조): line 40 URL 인용
    - §3 (description/use proactively): line 92-95 URL 인용
    - §4 (도구 스코핑): line 147-148 URL 인용
    - §4 Agent(agent_type): line 184-185 URL 인용
  - L3 검증: 모든 신규/개정 섹션에 `> **출처:**` 인용 포함.

- [x] AG-08 [exact]: 코드 펜스 언어 힌트 누락 0건 — PASS
  - 근거: Grep `^```[^`\n]` 검색 결과 모든 여는 펜스에 `markdown`, `yaml`, `text` 언어 힌트 존재. `validate-plugin.py` "V6 code-fence 0 bare — OK" 확인.
  - L3 검증: 실제 Grep 결과 직접 확인.

- [x] AG-09 [exact]: last_updated `2026-04-11`, version `1.1.0` — PASS
  - 근거: `agent-design-guide.md:3-4` — `version: 1.1.0`, `last_updated: 2026-04-11`.
  - L3 검증: frontmatter 실제 필드 값 일치 확인.

---

### I (Integration / Hygiene) (3/3)

- [x] I-01 [exact]: `validate-plugin.py` 7 OK, Exit 0 — PASS
  - 근거: 직접 실행 결과 "Total: 7 plugins, 7 OK / Exit: 0" 확인.
  - L3 검증: 실제 명령 실행 결과.

- [x] I-02 [exact]: Working tree modified 예외 3항목 외 없음 — PASS
  - 근거: `git status` 결과 — tracked 파일 중 modified 없음. `scripts/__pycache__/`는 untracked 빌드 아티팩트이며 "modified"(추적 파일 변경) 범주가 아님. 예외 3항목(sprint-contract.md, skill-design-guide.md, agent-design-guide.md)은 이미 커밋된 상태.
  - L3 검증: `git status --short` 출력이 `?? scripts/__pycache__/` 한 줄뿐.

- [x] I-03 [exact]: 커밋 1건 (`kaizen(phase1-research):...`) + body에 리서치 소스 URL 2건 이상 — PASS
  - 근거: 커밋 `4587154` 메시지 확인. subject: `kaizen(phase1-research): skill/agent design guides 2026-04 최신 Anthropic 공식 패턴 반영`. body에 URL 5건: platform.claude.com, code.claude.com, github.com/anthropics/skills, anthropic.com/engineering, claudefa.st.
  - L3 검증: `git show 4587154 --format="%B"` 실제 메시지 직접 확인.

---

### Anti-patterns (2/2)

- [x] AP-01: `hardcoded.*version` 패턴 — PASS (변경 파일에 해당 패턴 없음)
- [x] AP-02: `git push.*--force` 패턴 — PASS (변경 파일에 해당 패턴 없음)

---

### Reusability (SKIP)
문서 파일(md) 변경이며 공유 컴포넌트 중복 해당 없음.

---

### Diagnostics

- validate-plugin.py: 7 OK, Exit 0 — PASS
- bare code fence: 0건 — PASS
- MCP 런타임 검증: 미수행 (mcp_server: null). 정적 검증만으로 판정.

---

## Summary

- Total: 23/23 conditions passed
- Anti-patterns: 2/2 OK
- Verdict: **APPROVE**

모든 SG-01~SG-11, AG-01~AG-09, I-01~I-03 조건이 L3 수준(파일:라인 근거)으로 검증 완료.
