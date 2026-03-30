# Phase 1 검색 소스 — 스킬/에이전트 설계 패턴

> Phase 1(설계 가이드 업데이트)에서 사용하는 리서치 소스.
> Phase 2/3 소스는 각 카이젠(harness-kaizen, flutter-kaizen)의 search-sources.md를 참조.

## 소스 분류

### Anthropic 공식
- **Claude Code 공식 문서:** code.claude.com/docs — sub-agents, skills, hooks, MCP 서버
- **Anthropic Research:** anthropic.com/research — Building Effective Agents, tool use, multi-agent
- **Anthropic Engineering:** anthropic.com/engineering — Claude Code 업데이트, 새 기능
- **Claude Code Changelog:** code.claude.com/changelog — 버전별 변경사항

### 학술 논문
- **검색 대상:** arXiv, Semantic Scholar
- **키워드:** LLM agent design pattern, prompt engineering, multi-agent system, tool use orchestration, agentic workflow, code generation agent, quality assurance agent
- **범위:** 최근 6개월 우선, 핵심 논문은 기간 무관

### 경쟁/유사 도구
- **Cursor Rules:** cursor.directory — AI 코딩 도구의 rules/instructions 패턴
- **GitHub Copilot Instructions:** .github/copilot-instructions.md 패턴 분석
- **Gemini CLI Extensions:** gemini-cli-extensions — 스킬/플러그인 구조
- **Windsurf Rules:** windsurf 커뮤니티 rules 패턴

### 커뮤니티/실무
- **skills.sh:** skills.sh — Claude Code 스킬 마켓플레이스, 인기 스킬 패턴 분석
- **GitHub trending:** 키워드: claude-code, agent-skill, prompt-template, mcp-server
- **블로그:** Simon Willison (simonwillison.net), Lilian Weng (lilianweng.github.io)
- **Claude Code 커뮤니티:** GitHub Issues (anthropics/claude-code), Discord

## 리서치 목적

Phase 1 리서치는 **설계 원칙 수준**의 인사이트를 찾는다:

| 찾는 것 | 예시 |
|---------|------|
| 새 스킬 아키타입 | 기존 9가지 외에 새로운 유형 |
| Gotchas 패턴 | Claude가 반복 실패하는 새로운 패턴 |
| 에이전트 디자인 패턴 | 5가지 패턴 외 새로운 패턴 |
| 도구 스코핑 규칙 | 새 도구 추가/변경에 따른 스코핑 업데이트 |
| description 작성법 | 트리거 정확도 향상 기법 |
| 프롬프트 엔지니어링 | 스킬/에이전트 프롬프트 품질 향상 기법 |
| 검증 기준 | 스킬의 자가 검증 패턴 개선 |

**Phase 2/3와의 차이:**
- Phase 1: "스킬을 **어떻게 설계**해야 하는가" (메타 수준)
- Phase 2: "harness 스킬을 **어떻게 개선**하는가" (QA/계약 도메인)
- Phase 3: "flutter-toolkit 스킬을 **어떻게 개선**하는가" (Flutter 도메인)

## 신뢰도 기준

| 유형 | 신뢰도 | 태그 |
|------|--------|------|
| Anthropic 공식 docs/blog | 높음 | — |
| Peer-reviewed 논문 | 높음 | — |
| arXiv preprint | 중간 | `[preprint]` |
| 경쟁 도구 공식 docs | 중간 | `[competitor]` |
| skills.sh 인기 스킬 | 중간 | `[skills.sh]` |
| 커뮤니티 블로그 | 낮음 | `[unverified]` |

## 중복 방지

- 매 실행 시 `docs/kaizen/research-log.md`를 먼저 읽는다
- Phase 1 소스는 `[phase1]` 태그로 구분하여 기록
