---
name: react-research
description: >
  React/Vite/Tauri/WASM 레퍼런스 소스를 크롤링/분석하여 docs/react/ 문서를 갱신한다.
  이 레포 개발용 스킬이며, react-kit 플러그인에 포함되지 않는다.
  "React 리서치", "react research", "React 문서 갱신" 같은 요청 시 트리거.
argument-hint: "[category]"
user-invocable: true
---

# Gotchas

1. **기존 문서 구조 유지** — `docs/react/kit-design/` 의 각 문서는 frontmatter + 표준 섹션 구조를 따른다. 섹션 순서를 바꾸지 말고 내용만 갱신한다.
2. **출처 없는 내용 금지** — 모든 원칙, API, 수치에 출처 URL 을 명시한다 (React 공식 문서, MDN, package npm 페이지 등).
3. **한 번에 전체 갱신 금지** — `category` 인자로 특정 그룹만 갱신한다. 미지정 시 사용자에게 확인.
4. **라이브러리 0개 원칙 보존** — 새 리서치에서 "이 라이브러리가 편리하다" 라는 제안을 받더라도, G5b 애니메이션의 금지 목록은 유지한다. React + Tailwind + 표준 Web API 만 사용한다는 원칙을 계속 반영한다.

# Process

## Step 1: 대상 카테고리 결정

| 인자 | 대상 문서 |
|------|----------|
| `g1` | docs/react/kit-design/g1-scaffolding.md |
| `g2` | docs/react/kit-design/g2-state-data.md |
| `g3` | docs/react/kit-design/g3-performance.md |
| `g4` | docs/react/kit-design/g4-quality.md |
| `g5` | docs/react/kit-design/g5-ui-patterns.md |
| `g5b` | docs/react/kit-design/g5b-animation.md |
| `g6` | docs/react/kit-design/g6-build-audit.md |
| `wasm-catalog` | docs/react/wasm-catalog.md |
| `final-integration` | docs/react/kit-design/final-integration.md |
| 미지정 | 사용자에게 확인 |

## Step 2: 리서치 실행

Context7 MCP (공식 API 문서 조회) 와 Codex 에이전트 (웹 리서치) 에 해당 카테고리의 최신 정보를 위임한다:

- **공식 문서**: react.dev, tanstack.com/router, tanstack.com/query, vitejs.dev, tauri.app, tailwindcss.com, shadcn, zustand docs, react-hook-form docs, lingui docs, neverthrow github
- **변경사항**: 최근 major 버전 release notes, migration guides, deprecated API
- **커뮤니티 트렌드**: React RFC, React Core team 발표, This Week in React, r/reactjs 공식 Q&A
- **수치 기준**: Web Vitals, WASM boundary cost, bundle size 데이터

## Step 3: 문서 갱신

리서치 결과를 기존 문서에 반영한다:
- `last_updated` 날짜 갱신
- 새 원칙/안티패턴 추가
- deprecated API 제거 또는 대체안 명시
- 수치 기준 업데이트
- 출처 URL 갱신

## Step 4: 커밋

갱신된 문서를 `docs(react-research): update <category> docs` 형식으로 커밋한다.

## Step 5: 후속 카이젠 권장

문서 갱신 후 `/react-kaizen` 스킬 호출을 권장하여, 갱신된 리서치 기준으로 react-kit 스킬들이 업데이트되도록 한다.

# References

- `docs/react/kit-design/` — 갱신 대상 설계 문서 7개 + final-integration
- `docs/react/wasm-catalog.md` — WASM 카탈로그
- Context7 MCP — 공식 API 문서 조회
- Codex 에이전트 — 웹 리서치 + 버전 확인
