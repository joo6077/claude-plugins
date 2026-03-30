# Phase 1 검색 소스 — 스킬/에이전트 설계 + AI 트렌드

> Phase 1(설계 가이드 업데이트)에서 사용하는 리서치 소스.
> Phase 2/3 소스는 각 카이젠(harness-kaizen, flutter-kaizen)의 search-sources.md를 참조.

## 소스 분류

### 1. Anthropic 공식
- **Claude Code 공식 문서:** code.claude.com/docs — sub-agents, skills, hooks, MCP 서버
- **Anthropic Research:** anthropic.com/research — Building Effective Agents, tool use, multi-agent
- **Anthropic Engineering:** anthropic.com/engineering — Claude Code 업데이트, 새 기능
- **Claude Code Changelog:** code.claude.com/changelog — 버전별 변경사항
- **Claude API Docs:** docs.anthropic.com — API 변경, tool use 업데이트

### 2. 경쟁사 공식 — AI 에이전트/스킬/하네스
- **OpenAI:**
  - platform.openai.com/docs — Assistants API, function calling, Code Interpreter
  - openai.com/research — agent 관련 연구
  - openai.com/index — 제품 업데이트, 새 기능 발표
  - Codex CLI — 오픈소스 에이전트 (github.com/openai/codex)
- **Google:**
  - cloud.google.com/vertex-ai/docs — Gemini agent, function calling
  - deepmind.google/research — AI agent 연구
  - Gemini CLI — gemini-cli-extensions, 스킬/플러그인 구조
  - Firebase Genkit — AI workflow orchestration
- **Microsoft:**
  - GitHub Copilot — .github/copilot-instructions.md 패턴
  - Semantic Kernel — AI orchestration framework
  - AutoGen — multi-agent 프레임워크
- **기타 AI 에이전트 프레임워크:**
  - LangChain / LangGraph — agent workflow, tool use 패턴
  - CrewAI — multi-agent 협업 패턴
  - Vercel AI SDK — tool calling, structured output 패턴

### 3. 경쟁 AI 코딩 도구
- **Cursor:** cursor.directory — rules/instructions 패턴, agent mode
- **Windsurf (Codeium):** rules 패턴, cascade agent
- **Devin (Cognition):** autonomous coding agent 접근법
- **Augment Code:** 코드베이스 이해 + agent 패턴
- **Aider:** agentic coding 오픈소스, convention 패턴

### 4. 학술 논문 / AI 트렌드
- **검색 대상:** arXiv, Semantic Scholar, ACL Anthology, NeurIPS/ICLR/ICML proceedings
- **키워드 — 에이전트 설계:**
  - LLM agent design pattern, multi-agent system, tool use orchestration
  - agentic workflow, code generation agent, agent evaluation
  - agent-computer interface, human-agent interaction
- **키워드 — 프롬프트/하네스:**
  - prompt engineering, instruction tuning, chain-of-thought
  - quality assurance LLM, automated code review
  - test generation LLM, harness engineering
- **키워드 — 최신 트렌드:**
  - reasoning model, thinking model (o1/o3 스타일)
  - model context protocol (MCP), tool augmented LLM
  - agentic RAG, memory-augmented agent
  - AI safety evaluation, red teaming agent
  - code agent benchmark (SWE-bench, HumanEval 등)
- **범위:** 최근 6개월 우선, 핵심 논문은 기간 무관
- **후속:** 발견한 논문의 references에서 관련 논문 추적

### 5. 커뮤니티/실무
- **skills.sh:** Claude Code 스킬 마켓플레이스, 인기 스킬 패턴 분석
- **GitHub trending:** 키워드: claude-code, agent-skill, prompt-template, mcp-server, ai-agent, coding-agent
- **블로그:**
  - Simon Willison (simonwillison.net) — AI 도구 실무 분석
  - Lilian Weng (lilianweng.github.io) — LLM agent 서베이
  - Eugene Yan (eugeneyan.com) — ML 시스템 설계
  - Chip Huyen (huyenchip.com) — AI 엔지니어링
- **Claude Code 커뮤니티:** GitHub Issues (anthropics/claude-code), Discord
- **AI 뉴스/컨퍼런스:** The Gradient, AI conference proceedings, AI Twitter/X 주요 토론

## 리서치 목적

Phase 1 리서치는 **설계 원칙 수준**의 인사이트를 찾는다:

| 찾는 것 | 예시 |
|---------|------|
| 새 스킬 아키타입 | 기존 9가지 외에 새로운 유형 |
| Gotchas 패턴 | Claude가 반복 실패하는 새로운 패턴 |
| 에이전트 디자인 패턴 | Anthropic 5가지 + 경쟁사에서 발견된 새 패턴 |
| 도구 스코핑 규칙 | MCP 서버, function calling 변화에 따른 업데이트 |
| description 작성법 | 트리거 정확도 향상 기법 |
| 프롬프트 엔지니어링 | 스킬/에이전트 프롬프트 품질 향상 기법 |
| 검증 기준 | 스킬의 자가 검증 패턴 개선 |
| 하네스 엔지니어링 | QA/계약 기반 품질 보증의 새로운 접근법 |
| AI 트렌드 반영 | reasoning model, MCP, agentic RAG 등 새 패러다임 |
| 경쟁사 패턴 차용 | OpenAI/Google/MS의 agent 접근법 중 우리에게 적용 가능한 것 |

**Phase 2/3와의 차이:**
- Phase 1: "스킬/에이전트를 **어떻게 설계**해야 하는가" + "AI 트렌드가 **설계 원칙에 어떤 영향**을 주는가" (메타 수준)
- Phase 2: "harness 스킬을 **어떻게 개선**하는가" (QA/계약 도메인)
- Phase 3: "flutter-toolkit 스킬을 **어떻게 개선**하는가" (Flutter 도메인)

## 신뢰도 기준

| 유형 | 신뢰도 | 태그 |
|------|--------|------|
| Anthropic 공식 docs/blog | 높음 | — |
| OpenAI/Google/MS 공식 docs | 높음 | `[competitor-official]` |
| Peer-reviewed 논문 | 높음 | — |
| arXiv preprint | 중간 | `[preprint]` |
| 경쟁 코딩 도구 공식 docs | 중간 | `[competitor]` |
| AI 프레임워크 공식 docs | 중간 | `[framework]` |
| skills.sh 인기 스킬 | 중간 | `[skills.sh]` |
| 유명 AI 블로거 | 중간 | `[blog]` |
| 커뮤니티 블로그/포럼 | 낮음 | `[unverified]` |

## 중복 방지

- 매 실행 시 `docs/kaizen/research-log.md`를 먼저 읽는다
- Phase 1 소스는 `[phase1]` 태그로 구분하여 기록
- 경쟁사 소스는 공식 문서 URL이 변경될 수 있으므로 매번 WebSearch로 최신 URL 확인
