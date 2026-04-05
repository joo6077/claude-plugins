---
name: create-kit
description: >
  새 플러그인 킷을 처음부터 끝까지 생성하는 오케스트레이션 스킬.
  리서치 → 문서 → 플러그인 구조 → 스킬/에이전트 → 카이젠 → 레지스트리 → QA → docs-site
  전체 파이프라인을 자동화한다.
  "킷 만들어줘", "새 플러그인", "create kit", "kit 생성",
  "새 플러그인 만들어줘", "플러그인 추가" 같은 요청 시 트리거.
  기존 킷 수정, 단일 스킬 추가에는 트리거하지 않는다 — /create-skill 사용.
argument-hint: "<kit-name> <domain-description>"
user-invocable: true
---

# Gotchas

1. **리서치 없이 스킬부터 만들지 마라** — 리서치 문서(SSOT)가 먼저 존재해야 스킬이 참조할 수 있다. design-kit이 22개 문서 위에 3개 스킬을 올린 것처럼, 문서 → 스킬 순서는 절대 뒤집히면 안 된다.
2. **기존 킷 패턴 3종을 벗어나지 마라** — 모든 킷은 동일한 3스킬 패턴을 따른다: guide(가벼운 리뷰) + audit(체계적 감사) + system/init(초기 세팅). 4번째 스킬이 필요하면 기존 3개에 흡수할 수 없는지 먼저 검토하라.
3. **Codex 리서치와 문서 작성을 분리하라** — Codex는 원시 리서치만, 문서 포맷팅은 별도 서브에이전트가 담당. Codex에게 마크다운 포맷팅까지 시키면 출처 누락이 생긴다.
4. **카이젠 스킬은 플러그인이 아닌 .claude/skills/에** — research/kaizen 스킬은 이 레포 개발용이므로 플러그인 안에 넣지 않는다. 외부 사용자에게 노출되면 안 된다.
5. **accent 컬러 충돌 확인** — docs-site 페이지 생성 시 css-tokens.md의 기존 accent와 겹치지 않는 컬러를 선택해야 한다.
6. **병렬화 가능한 단계를 직렬로 실행하지 마라** — P1/P2 문서 작성, 스킬/에이전트 생성은 서브에이전트로 병렬 처리한다. 직렬 실행하면 시간이 3-4배 늘어난다.

# Process

## Phase 0: 요구사항 확인

사용자에게 확인:

| 항목 | 질문 | 예시 |
|------|------|------|
| 킷 이름 | `{name}-kit` | backend-kit, infra-kit |
| 도메인 | 어떤 영역을 다루는가 | 백엔드 개발, 인프라/DevOps |
| 스택 무관 여부 | 특정 프레임워크에 종속되는가 | 스택 무관 (design-kit 패턴) |
| 3번째 스킬 성격 | system(아키텍처 세팅) vs init(초기 세팅) | backend=system, infra=init |

## Phase 1: 리서치 (Codex)

### Step 1.1: 영역 분석

Codex에 위임:
- 해당 도메인에서 자동화 효과가 큰 작업 Top 10
- skills.sh 마켓플레이스 기존 스킬 분석
- 커뮤니티 니즈 (GitHub issues, Reddit)
- skill-design-guide 9가지 아키타입 중 적합한 유형

### Step 1.2: 리서치 문서 주제 선정

영역 분석 결과를 기반으로:
- P1 (필수): 8개 주제
- P2 (확장): 4개 주제

각 주제에 포함할 내용: 원칙 5-10개(출처 필수), 수치/기준값, 안티패턴 3-5개, Gotchas

### Step 1.3: 심화 리서치

P1/P2 각각 Codex에 위임 (병렬):
- 공식 문서, RFC, 학술 논문, 신뢰할 수 있는 엔지니어링 블로그
- 일반 블로그는 교차 검증 필수

## Phase 2: 리서치 문서 생성

### Step 2.1: 디렉토리 구조

```
docs/{kit-name}/
├── {category-1}/
│   ├── topic-a.md
│   └── topic-b.md
├── {category-2}/
│   └── topic-c.md
└── ...
```

### Step 2.2: 문서 작성

references/doc-template.md 포맷을 따라 서브에이전트로 병렬 생성.

각 문서:
- frontmatter (title, version 0.1.0, last_updated)
- 1-2줄 요약
- 원칙 (### 번호. 제목 → 설명 → `> **출처:** [이름](URL)`)
- 수치/기준값
- 안티패턴
- Gotchas

### Step 2.3: 품질 확인

- 모든 문서에 frontmatter 존재
- 모든 원칙에 인라인 출처
- 수치가 구체적 (타임아웃, 임계값, 비율)

## Phase 3: 플러그인 스캐폴딩

### Step 3.1: 디렉토리 구조

```
{kit-name}/
├── .claude-plugin/plugin.json
├── skills/
│   ├── {kit-name}-guide/
│   │   ├── SKILL.md
│   │   └── references/principle-index.md
│   ├── {kit-name}-audit/
│   │   ├── SKILL.md
│   │   └── references/audit-criteria.md
│   └── {kit-name}-{system|init}/
│       ├── SKILL.md
│       └── references/{system-principles|init-checklist}.md
├── agents/
│   └── {kit-name}-reviewer.md
├── evals/
└── README.md
```

### Step 3.2: plugin.json

references/plugin-template.json 참조.

### Step 3.3: 스킬 3종 생성 (병렬)

**guide**: references/skill-patterns.md의 guide 패턴 참조
- 카테고리별 키워드 테이블
- principle-index.md로 문서 매핑
- 피드백 포맷: 원칙 → 근거 → 권장 → 출처

**audit**: references/skill-patterns.md의 audit 패턴 참조
- reviewer 에이전트 호출
- audit-criteria.md 체크리스트
- PASS/FAIL → APPROVE/REJECT

**system/init**: references/skill-patterns.md의 system 패턴 참조
- 프로젝트 감지
- 카테고리별 세팅/초기화
- 현재 상태 → 권장 → 개선

### Step 3.4: 에이전트 생성

references/skill-patterns.md의 reviewer 패턴 참조:
- tools: Read, Grep, Glob (읽기 전용)
- model: sonnet
- 핵심 규칙 5-6개
- 평가 카테고리 (audit-criteria 기반)
- 테이블 출력 포맷

### Step 3.5: README.md

references/readme-template.md 참조.

## Phase 4: 카이젠 연동

### Step 4.1: 카이젠 스킬 생성

`.claude/skills/`에 2개 생성:
- `{kit-name}-research/SKILL.md` — 외부 소스 크롤링 → docs 갱신
- `{kit-name}-kaizen/SKILL.md` — docs 기준 스킬 격차 분석 → 개선

references/kaizen-template.md 참조.

### Step 4.2: 카이젠 오케스트레이터 업데이트 검토

kaizen-orchestrator 스킬에 새 Phase 추가가 필요한지 사용자에게 확인.

## Phase 5: 레지스트리 & 문서

### Step 5.1: marketplace.json 업데이트

`.claude-plugin/marketplace.json`에 새 플러그인 추가.

### Step 5.2: CLAUDE.md 스킬 레퍼런스 업데이트 검토

필요하면 CLAUDE.md의 Skills Reference 테이블에 새 스킬 추가.

## Phase 6: QA

### Step 6.1: qa-evaluator 실행

harness:qa-evaluator 에이전트를 spawn하여 전체 결과물 평가.

평가 기준:
- 구조 일관성 (기존 플러그인과 동일 레이아웃)
- 리서치 문서 품질 (frontmatter, 출처, 수치)
- 스킬 품질 (Gotchas, Process, References)
- 에이전트 품질 (tools, model, 규칙, 카테고리)
- 경로 정합성 (principle-index 상대경로)

### Step 6.2: FAIL 수정

REJECT 시 FAIL 항목을 수정하고 재검증한다.
**최대 3회 반복.** 3회 후에도 REJECT가 지속되면 사용자에게 에스컬레이션하고 중단한다. 무한 루프 방지.

## Phase 7: docs-site 페이지

### Step 7.1: accent 컬러 선택

css-tokens.md의 기존 accent와 겹치지 않는 컬러 선택.

### Step 7.2: HTML 페이지 생성 (1 문서 = 1 페이지)

/docs-site 스킬을 실행하여 리서치 문서 개수만큼 HTML 페이지 생성.

**원칙:** 리서치 문서 N개 → HTML 페이지 N개. design-kit(22개 → 22개)이 기준이다. 여러 문서를 overview로 묶지 마라.

### Step 7.3: index.html 등록

categories 배열과 getIcon() 함수에 새 킷의 모든 페이지(N개) 추가.

## 검증 체크리스트

- [ ] docs/{kit-name}/ 리서치 문서 12개 이상 존재
- [ ] 모든 리서치 문서에 frontmatter + 인라인 출처
- [ ] {kit-name}/.claude-plugin/plugin.json 존재
- [ ] 스킬 3개 (guide, audit, system/init) SKILL.md 존재
- [ ] 에이전트 1개 (reviewer) .md 존재
- [ ] principle-index.md 상대경로가 실제 문서와 일치
- [ ] .claude/skills/{kit-name}-research + {kit-name}-kaizen 존재
- [ ] marketplace.json에 새 플러그인 등록
- [ ] qa-evaluator APPROVE
- [ ] docs/{kit-name}/ HTML 페이지 N개 존재 (리서치 문서 수와 동일) + index.html에 전체 등록

# References

- references/doc-template.md — 리서치 문서 포맷
- references/skill-patterns.md — 3종 스킬 + 에이전트 패턴
- references/kaizen-template.md — 카이젠 스킬 템플릿
- references/plugin-template.json — plugin.json 골격
- references/readme-template.md — README 골격
