# Harness Kaizen — 지속적 개선 스킬 설계 스펙

> 학술 논문, 공식 문서, 커뮤니티 리서치를 기반으로 하네스 엔지니어링을 주기적·자동으로 개선하는 스킬

---

## 1. 개요

### 목적

하네스 프레임워크(설정, 스킬, 에이전트, eval, 아키텍처, 설계 가이드)를 최신 연구와 실무 기법에 맞춰 점진적으로 개선한다. 연구 결과는 PR로 제출하여 사용자가 리뷰 후 머지한다.

### 핵심 제약

**할루시네이션 절대 불가.** 출처 없는 주장은 어떤 경우에도 반영하지 않는다.

### 스킬 유형

비즈니스 자동화(4번) + 코드 리뷰(6번) 혼합 — 주기적 연구 자동화 + 코드/설정 개선 제안

---

## 2. 개선 대상 범위

| 영역 | 대상 파일/디렉토리 | 예시 |
|------|---------------------|------|
| 하네스 설정 | `.harness/project.yaml`, `procedures/` | anti-pattern 추가, 카테고리 정교화 |
| 스킬 프롬프트 | `harness/skills/*/SKILL.md` | Gotchas 추가, 프롬프트 기법 개선 |
| 에이전트 로직 | `harness/agents/qa-evaluator.md` | 평가 로직 강화, 검증 패턴 추가 |
| Eval | `harness/evals/` | 테스트 픽스처 추가, 평가 기준 보완 |
| 아키텍처 | `harness/` 전체 구조 | 폴더 구조, 훅, 스크립트 |
| 설계 가이드 | `docs/skill-design-guide.md` | 새 원칙/패턴 발견 시 반영 |

---

## 3. 트리거 조건

### 3.1 주기적 실행 (cron)

- **매주 월요일 09:00 KST**
- Claude Code의 `schedule` (remote trigger) 기능 활용
- 전 영역 동시 스캔

### 3.2 이벤트 트리거

| 이벤트 | 감지 방법 | 카이젠 범위 |
|--------|-----------|-------------|
| QA Evaluator REJECT 2회 연속 | `sprint-feedback.md` REJECT 이력 확인 | REJECT 원인 영역 집중 개선 |
| 같은 anti-pattern 3회 이상 반복 | feedback 히스토리 분석 | 해당 anti-pattern 규칙 강화 또는 스킬 가이드 보완 |
| 새 스킬 추가 후 첫 주 | 스킬 폴더 변경 감지 | 신규 스킬이 설계 가이드 원칙을 따르는지 점검 |

### 3.3 수동 호출

- `/harness-kaizen` — 전체 영역 리서치
- `/harness-kaizen config` — 설정만 집중
- `/harness-kaizen skills` — 스킬만 집중
- `/harness-kaizen guide` — 설계 가이드만 집중

---

## 4. 실행 파이프라인

```
[트리거]
├─ cron: 매주 월요일 09:00 KST
├─ 이벤트: REJECT 2연속 / anti-pattern 3회 반복 / 신규 스킬 추가
└─ 수동: /harness-kaizen [영역]

    ↓

[COLLECT] 전 영역 동시 스캔
├─ 학술: arXiv, ACL, IEEE 논문 검색
├─ 공식: Anthropic, OpenAI, DeepMind docs & changelog
├─ 커뮤니티: GitHub trending, 엔지니어 블로그, 컨퍼런스
└─ 이전 research-log.md 참고하여 중복 방지

    ↓

[VERIFY] 3중 검증 게이트
├─ GATE 1: 모든 주장에 URL 존재 확인 (URL 없으면 즉시 폐기)
├─ GATE 2: WebFetch로 URL 실제 접근 + 내용 일치 확인
└─ GATE 3: 검증 실패 → 해당 정보 즉시 폐기

    ↓

[ANALYZE] 갭 분석
├─ 현재 하네스 상태 스캔
│  (project.yaml, skills, agents, evals, docs/skill-design-guide.md)
└─ 수집된 연구 vs 현재 상태 비교 → 개선 포인트 도출

    ↓

[PROPOSE + APPLY]
├─ 브랜치 생성: kaizen/YYYY-MM-DD
├─ 변경 적용
├─ research-log.md 업데이트
├─ docs/kaizen/changelog.md 업데이트
└─ PR 생성 (연구 정리본 + Before/After + 장단점 + 출처)
```

---

## 5. 할루시네이션 방지 — 3중 검증 게이트

### GATE 1: 출처 존재 확인

- 모든 주장에 URL 필수
- URL 없는 인사이트 → 즉시 폐기 (예외 없음)
- "~라고 알려져 있다" 식의 vague 표현 금지

### GATE 2: 출처 접근 검증

- WebFetch로 URL 실제 접근 시도
- 접근 불가 → 해당 정보 폐기
- 접근 가능하더라도 내용이 주장과 불일치 → 폐기

### GATE 3: PR 본문에 증거 첨부

- 모든 개선안에 출처 URL + 인용 원문 포함
- "이 논문의 Section X에서..." 수준의 구체적 근거
- 사용자가 PR에서 원문 대조 가능

### 추가 안전장치

- arXiv preprint → `[preprint]` 태그 명시
- 블로그 포스트 → 작성자 신뢰도 표기 (공식 vs 개인)
- 6개월 이상 된 정보 → `[dated: YYYY-MM]` 태그로 최신성 경고

---

## 6. PR 본문 템플릿

```markdown
## Research Summary
> 이번 주 연구에서 발견한 핵심 인사이트 정리

### 조사한 소스
- [논문/블로그/docs 제목](URL) — 핵심 요약 1-2줄
- [논문/블로그/docs 제목](URL) — 핵심 요약 1-2줄

### 핵심 발견
- 발견 1: 구체적 설명 + 출처 인용
- 발견 2: 구체적 설명 + 출처 인용

---

## Changes (개선 항목별 반복)

### 1. [개선 항목명]

**영역:** config / skill-prompt / agent-logic / eval / architecture / design-guide

**Before:**
// 현재 코드 또는 설정 (실제 스니펫)

**After:**
// 변경된 코드 또는 설정 (실제 스니펫)

**왜 개선인가:**
- 장점: ...
- 단점/트레이드오프: ...
- 근거: [출처](URL)의 Section X에서 "인용문..."

---

## Impact Summary

| 항목 | 영향도 | 리스크 | 근거 |
|------|--------|--------|------|
| 변경1 | 높음/중간/낮음 | 높음/중간/낮음 | 출처 링크 |
| 변경2 | ... | ... | ... |

---

## Source Reliability

| 출처 | 유형 | 신뢰도 | 최신성 |
|------|------|--------|--------|
| 논문 A | peer-reviewed | 높음 | 2026-02 |
| Anthropic blog B | 공식 | 높음 | 2026-03 |
| 개인 블로그 C | 커뮤니티 | 중간 | 2025-11 [dated] |
```

---

## 7. 연구 소스 및 검색 전략

### 소스 분류

```
학술 논문
├─ 검색: arXiv "LLM agent" OR "prompt engineering" + 최근 6개월
├─ 키워드: evaluation, verification, quality assurance, agentic
└─ 후속: 발견한 논문의 references 추적

공식 소스
├─ Anthropic: docs changelog, engineering blog, research
├─ OpenAI: cookbook, blog
└─ Google DeepMind: publications

커뮤니티/실무
├─ GitHub: trending repos (agent, harness, prompt 관련)
├─ 블로그: Simon Willison, Lilian Weng 등
└─ 컨퍼런스: NeurIPS, ICLR, ACL 최신 proceedings
```

### 신뢰도 기준

| 유형 | 신뢰도 | 비고 |
|------|--------|------|
| Peer-reviewed 논문 | 높음 | 가장 신뢰 |
| 공식 블로그/docs (Anthropic, OpenAI, Google) | 높음 | 최신성 높음 |
| arXiv preprint | 중간 | `[preprint]` 태그 필수 |
| 유명 엔지니어 블로그 | 중간 | 실전 검증된 패턴 |
| GitHub trending | 중간 | 커뮤니티 검증 필요 |
| 일반 블로그/포럼 | 낮음 | 다른 소스로 교차 검증 필요 |

### 중복 방지

- 매 실행 시 `docs/kaizen/research-log.md` 참조
- 이미 조사한 소스는 건너뜀
- 단, 이전 소스의 업데이트(새 버전, 후속 논문)는 재조사

---

## 8. 스킬 폴더 구조

```
harness/skills/harness-kaizen/
├── SKILL.md                     # 메인 지시문 + 파이프라인 정의
├── references/
│   ├── search-sources.md        # 검색 소스 목록 및 신뢰도 기준
│   └── pr-template.md           # PR 본문 템플릿
├── scripts/
│   └── trigger-check.sh         # 이벤트 트리거 조건 감지
└── templates/
    └── research-log-entry.md    # 연구 로그 엔트리 템플릿
```

### 산출물 디렉토리

```
docs/kaizen/
├── research-log.md              # 누적 연구 기록 (소스 + 채택/폐기)
└── changelog.md                 # 카이젠으로 인한 변경 이력
```

---

## 9. 이벤트 트리거 감지 로직

### REJECT 2회 연속 감지

```bash
# .harness/history/ 내 최근 2개 sprint-feedback.md 확인
# 둘 다 verdict: REJECT이면 트리거
```

### Anti-pattern 반복 감지

```bash
# .harness/history/ 내 sprint-feedback.md에서
# 같은 anti-pattern ID가 3회 이상 등장하면 트리거
```

### 신규 스킬 감지

```bash
# harness/skills/ 디렉토리의 git log 확인
# 최근 7일 내 새 스킬 폴더 추가 감지
```

---

## 10. 수동 호출 인터페이스

| 명령 | 동작 |
|------|------|
| `/harness-kaizen` | 전체 영역 리서치 + PR |
| `/harness-kaizen config` | `.harness/` 설정 영역만 집중 |
| `/harness-kaizen skills` | 스킬 프롬프트 영역만 집중 |
| `/harness-kaizen guide` | `docs/skill-design-guide.md`만 집중 |

---

## 11. 버전 관리 전략

### Semver 규칙 (영향도 기반)

| 변경 영역 | bump | 예시 |
|-----------|------|------|
| docs, config 튜닝, anti-pattern 추가, Gotchas 추가 | **patch** `0.3.1 → 0.3.2` | project.yaml에 anti-pattern 1개 추가 |
| 스킬 프롬프트 변경, eval 기준 변경, 새 procedure 추가 | **minor** `0.3.2 → 0.4.0` | sprint-contract 스킬의 프로세스 단계 수정 |
| 아키텍처 변경, 에이전트 로직 대폭 수정, breaking change | **major** `0.4.0 → 1.0.0` | qa-evaluator 평가 방식 전면 교체 |

### 업데이트 대상 파일

PR마다 아래 파일을 자동으로 업데이트한다:

1. `harness/.claude-plugin/plugin.json` → `version` 필드
2. `.claude-plugin/marketplace.json` → description의 `[vX.Y.Z · 날짜]`
3. `docs/kaizen/changelog.md` → 변경 엔트리 추가

### changelog.md 엔트리 형식

```markdown
## [0.4.0] - 2026-04-07

### 변경 유형: minor (스킬 프롬프트)

### 연구 기반
- [논문 제목](URL) — 핵심 인사이트 1줄

### 변경 내역
- **sprint-contract/SKILL.md**: complexity 판단 로직에 few-shot 예시 추가
  - Before: 키워드 기반 단순 판단
  - After: 논문 X의 rubric 기반 3단계 판단
  - 근거: [출처](URL)

### 버전 판단 근거
> 스킬 프롬프트의 동작 방식이 변경되어 minor bump.
> 기존 project.yaml 호환성 유지되므로 major 아님.
```

### 추적 규칙

| 항목 | 규칙 | 예시 |
|------|------|------|
| 커밋 메시지 | `kaizen:` prefix | `kaizen: sprint-contract few-shot 판단 로직 추가` |
| 브랜치명 | 버전 포함 | `kaizen/0.4.0-2026-04-07` |
| PR 제목 | bump 유형 명시 | `[minor] sprint-contract 복잡도 판단 개선` |
| git tag | 자동 생성 | `v0.4.0` |
