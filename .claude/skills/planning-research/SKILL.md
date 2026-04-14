---
name: planning-research
description: >
  제품 기획 방법론 레퍼런스 소스를 크롤링/분석하여 docs/planning/ 문서를 갱신한다.
  이 레포 개발용 스킬이며, planning-kit 플러그인에 포함되지 않는다.
  "기획 리서치", "planning research", "기획 문서 갱신", "PM 리서치" 같은 요청 시 트리거.
argument-hint: "[category]"
user-invocable: true
---

# Gotchas

1. **할루시네이션 출처 금지** — 모든 원칙에 검증된 URL 출처 필수. URL 존재 확인 후 인용.
2. **기존 문서 덮어쓰기 금지** — 기존 docs/planning/ 문서를 읽고, 새 정보만 추가/갱신. 검증된 내용 삭제 금지.
3. **블로그 단독 인용 금지** — Lenny's/Reforge/FirstRound 블로그는 1차 출처(Basecamp, Amazon, Torres 원서 등)와 교차 검증 후 인용.
4. **6개월 이상 된 정보 태그** — `[dated: YYYY-MM]` 필수.
5. **frontmatter 갱신 누락 금지** — 수정 시 `last_updated` + `version` patch bump.
6. **Codex 결과 검증 금지 방지** — Codex 가 반환한 URL 은 반드시 WebFetch 로 접근 가능성 확인. 404 링크 저장 금지.
7. **방법론 유행 함정** — "최신이라서 좋다" 금지. Shape Up(2019) 은 여전히 유효하다. 연식이 아니라 프로덕션 사례 유무를 근거로.

# Process

## Step 1: 리서치 범위 결정

카테고리 지정 시 해당 문서만, 미지정 시 전체 docs/planning/ 갱신.

현재 문서 목록 (planning-kit SKILL 들이 참조):
- discovery.md — JTBD, Continuous Discovery, Cagan 4-risks
- prd-patterns.md — PR/FAQ, Shape Up, Linear 스펙
- stories.md — INVEST, Gherkin, Story Mapping
- prioritization.md — RICE, Kano, WSJF, MoSCoW, Opportunity Scoring
- flows.md — Mermaid 문법, Journey Map, Service Blueprint
- data-modeling.md — DDD, Event Storming, Mermaid erDiagram
- risks.md — Pre-mortem, Inversion, 4-risks
- cognitive-biases.md — PM 관점 편향 목록
- github-integration.md — Issues/Milestones/Projects v2, gh CLI

## Step 2: 기존 문서 읽기

대상 문서의 현재 원칙·출처·수치·`[dated:]` 태그 파악.

## Step 3: 외부 리서치 (Codex 위임)

codex:rescue 에이전트에 카테고리별 리서치 위임. 프롬프트 구조:
- 방법론 최신 상태 (deprecated 여부)
- 새 논문/공식 문서/컨퍼런스 세션
- 주요 PM 커뮤니티 신규 사례 (Lenny's, Reforge, FirstRound, SVPG, producttalk.org)
- Mermaid 는 공식 mermaid.js docs 기준으로 문법 확인

## Step 4: 문서 갱신

- 새 원칙 추가 (출처 URL + `[dated: YYYY-MM]`)
- 기존 수치 변경 시 이전 값 주석으로 보존
- deprecated 방법론은 표시 후 대체안 명시
- frontmatter version patch bump + last_updated

## Step 5: 커밋

```
research(planning): [카테고리] 문서 갱신 — 주요 변경 요약
```

# References

- docs/planning/ — 갱신 대상 SSOT
- codex:rescue — 외부 리서치 위임
- mermaid.js 공식 문서 — 다이어그램 문법 SSOT
