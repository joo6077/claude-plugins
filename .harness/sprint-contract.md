# Sprint Contract — Phase 1 Kaizen Research Mode

Feature: skill-design-guide / agent-design-guide 2026 최신 패턴 리서치 반영 카이젠
Created: 2026-04-11
Branch: kaizen/2026-04-11-research
Iteration: 1

## Context

2026년 Anthropic 공식 문서(Skill Authoring Best Practices, Sub-agents Docs, skill-creator SKILL.md)에서 확인한 2026 최신 설계 원칙을 `harness/docs/guides/skill-design-guide.md` 와 `harness/docs/guides/agent-design-guide.md` 에 반영한다.

최근 REJECT 패턴에서 도출된 아래 issue 도 동시 해결:
- PH-01: agent-design-guide 에 계약 모호성 방지 원칙이 누락되어 있음 (이미 §10 에 반영됨 — 추가 검증)
- SK-05 / RE-02: 트리거 키워드 set intersection 배타성 (이미 §4 에 반영됨 — 공식 "undertrigger" 개념으로 보강)
- DG-02: 코드 펜스 언어 힌트 필수 — 두 문서 내 코드 블록 전수 점검 대상
- 구체성 레벨 네이밍 충돌 (L1/L2/L3) — 공식 "degrees of freedom" 용어로 매핑 권고 추가

## 리서치 소스 (URL 필수)

1. https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices — Skill Authoring Best Practices (Anthropic 공식)
2. https://code.claude.com/docs/en/sub-agents — Claude Code Sub-agents 공식
3. https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md — skill-creator SKILL.md
4. https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills — Equipping Agents for Real World
5. https://github.com/anthropics/skills — 공식 skills repo

## 완료 조건 (Sprint Contract)

### SG (skill-design-guide.md)

- [ ] SG-01 [exact]: frontmatter 규칙 서브섹션 추가 — `name` 최대 64 자 / 소문자·숫자·하이픈·XML 태그 금지·예약어(anthropic, claude) 금지, `description` 최대 1024 자 / 비어 있지 않음 / XML 태그 금지 / 3인칭 작성 필수 4개 규칙 모두 문서에 명시됨
- [ ] SG-02 [exact]: "undertrigger" 개념 설명 — description 이 "pushy" 해야 하는 이유와 예시 1건 이상 수록
- [ ] SG-03 [structural]: "Degrees of Freedom" 섹션 추가 — high/medium/low freedom 각 사용 시점 + 예시 포함. 기존 L1/L2/L3 네이밍 충돌 감소를 위한 참조 노트 1줄 포함
- [ ] SG-04 [exact]: Reference 1-level deep 원칙 명시 — 나쁜 예(깊은 중첩) vs 좋은 예(평탄) 비교 블록 포함
- [ ] SG-05 [exact]: SKILL.md body 500 라인 상한 룰 명시 — 초과 시 `references/` 등으로 분리 권고
- [ ] SG-06 [exact]: Evaluation-Driven Development 섹션 추가 — 최소 3개 eval 먼저 작성, with-skill vs baseline 비교 접근 소개
- [ ] SG-07 [exact]: Naming convention — gerund form 권장 (`processing-pdfs`), 금지 예약어, 소문자+하이픈 규칙 명시
- [ ] SG-08 [exact]: MCP 도구 참조 시 fully-qualified name(`ServerName:tool_name`) 필수 규칙 추가
- [ ] SG-09 [structural]: 각 새 섹션·개정 섹션에 **출처 URL** 이 인용으로 최소 1개 달림
- [ ] SG-10 [exact]: 문서 내 코드 펜스 중 언어 힌트 누락된 블록 0 건 (DG-02 anti)
- [ ] SG-11 [exact]: last_updated 필드 `2026-04-11` 로 갱신, version `1.1.0` 으로 bump

### AG (agent-design-guide.md)

- [ ] AG-01 [exact]: "use proactively" 키워드의 공식 의미를 인용과 함께 설명 — 언더트리거 방지 메커니즘임을 명시
- [ ] AG-02 [exact]: frontmatter 필드 표에 `color`, `initialPrompt` 필드가 포함됨 (공식 문서 2026 필드 목록 기준)
- [ ] AG-03 [exact]: "Subagents cannot spawn subagents" 제약을 Gotchas 에 명시적으로 포함 (이미 §10 첫 항목에 있음 — 유지 확인)
- [ ] AG-04 [exact]: `Agent(agent_type)` 문법 설명 — 메인 스레드 에이전트가 스폰 가능한 서브 에이전트 화이트리스트 방식 포함
- [ ] AG-05 [structural]: 도구 스코핑 표에 역할 5종 이상 유지 + 각 행이 2026 공식 문서의 4종 역할 (read-only reviewer / research / code writer / docs)과 정합
- [ ] AG-06 [exact]: §10 "계약 모호성 방지" Gotcha 가 문서에 존재하고, `[exact]`/`[structural]`/`[goal]` 태그 언급 포함 (PH-01 fix 확정)
- [ ] AG-07 [structural]: 각 새 섹션·개정 섹션에 **출처 URL** 이 인용으로 최소 1개 달림
- [ ] AG-08 [exact]: 문서 내 코드 펜스 중 언어 힌트 누락된 블록 0 건 (DG-02 anti)
- [ ] AG-09 [exact]: last_updated 필드 `2026-04-11` 로 갱신, version `1.1.0` 으로 bump

### I (Integration / Hygiene)

- [ ] I-01 [exact]: `python3 scripts/validate-plugin.py` 실행 결과 Total 7 plugins, 7 OK, Exit 0
- [ ] I-02 [exact]: Working tree modified 예외 3항목 외 없음 — 예외: `.harness/sprint-contract.md`, `harness/docs/guides/skill-design-guide.md`, `harness/docs/guides/agent-design-guide.md`
- [ ] I-03 [exact]: git commit 1건 (`kaizen(phase1-research): ...`) 포함하며 commit message body 에 리서치 소스 URL 2건 이상 인용

## 검증 절차

1. Edit 로 두 가이드 파일 수정
2. Grep 으로 bare fence (` ``` ` 뒤 바로 개행) 0건 확인
3. `python3 scripts/validate-plugin.py` 실행 → 7 OK 확인
4. git add + commit
5. qa-evaluator 에이전트 spawn

## Anti-patterns (절대 하지 마라)

- 기존 §3.5, §4 (트리거 키워드 중복 방지), §10 (계약 모호성) 내용을 삭제하거나 약화시키기
- "~같은", "~정도", "~적절히" 같은 모호한 표현으로 완료 조건을 흐리기
- 스프린트 범위 밖 파일 수정 (validate-plugin 스크립트, 다른 스킬, 킷 등)
- 리서치 출처 없이 "2026 트렌드" 같은 근거 없는 주장 추가
