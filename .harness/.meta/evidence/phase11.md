---
phase: 11
title: "Phase 11 planning-kit — 확보된 외부 근거"
collected: 2026-09-24
method: codex (foreground, 직접 호출 · gpt-5.6-sol · 조회는 curl/gh)
inputs: 처리 배정표(.claude/kaizen-input/insights-report.md)의 Phase 11 행 · phase-research-templates.md Phase 11 필수 출처 · 현행화 점검
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치를 지어내지 마라. 없으면 미반영으로 남긴다.
---

읽기 전용으로 조사했으며 파일은 변경하지 않았다. 필수 표의 출처 중 5건 이상을 실제 조회했다.

## 1. 출처 목록

실제로 `curl` 또는 `gh`로 가져온 출처만 포함한다.

- Basecamp, Shape Up Chapter 6 — Write the Pitch  
  https://basecamp.com/shapeup/1.5-chapter-06
- Agile Alliance — INVEST  
  https://agilealliance.org/glossary/invest/
- Cucumber — Gherkin Reference  
  https://cucumber.io/docs/gherkin/reference
- Mermaid — Entity Relationship Diagram  
  https://mermaid.js.org/syntax/entityRelationshipDiagram.html
- Mermaid 12.0.0 release  
  https://github.com/mermaid-js/mermaid/releases/tag/mermaid%4012.0.0
- GitHub — Projects REST API  
  https://docs.github.com/en/rest/projects/items
- GitHub — REST API Versions  
  https://docs.github.com/en/rest/about-the-rest-api/api-versions
- GitHub — REST API Breaking Changes  
  https://docs.github.com/en/rest/about-the-rest-api/breaking-changes
- GitHub — Best practices for Projects  
  https://docs.github.com/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects
- GitHub CLI manual — `gh project`  
  https://cli.github.com/manual/gh_project
- GitHub CLI 2.101.0 release  
  https://github.com/cli/cli/releases/tag/v2.101.0

## 2. 항목별 관찰 사실

### Phase 11 planning-kit — F20: 폐기한 결정을 PRD의 한 자리에 기록

확인된 사실:

- Shape Up은 pitch의 필수 다섯 요소 중 하나로 `No-gos`를 둔다. 정의는 “appetite에 맞추거나 문제를 다루기 쉽게 하기 위해 의도적으로 제외한 기능 또는 사용 사례”다. 즉, “무엇을 하지 않기로 했는가”를 기획 문서에 명시하는 데 직접 근거가 있다.  
  https://basecamp.com/shapeup/1.5-chapter-06
- GitHub Projects 공식 지침은 정보 불일치를 막기 위해 정보를 여러 필드에 중복하지 말고 단일 source of truth에 두라고 한다. 공식 예시는 목표 출시일이지만, “기록 자리를 하나로 정한다”는 운영 원칙 자체는 명시돼 있다.  
  https://docs.github.com/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects
- 현행 내부 문서도 강한 PRD가 범위/비범위를 분리해야 한다고 정리한다. [docs/planning/prd-patterns.md:11](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/planning/prd-patterns.md:11)

추론:

- 폐기 결정을 PRD의 `Non-goals/No-gos` 한곳에 정규화하는 것은 Shape Up의 명시적 제외와 GitHub의 SSOT 원칙을 결합한 합리적인 로컬 계약이다.
- 다만 GitHub의 SSOT 문서는 제품 결정 기록을 직접 다룬 문서가 아니다. “폐기 결정에도 그대로 적용한다”는 부분은 추론이다.

반대·제한 근거:

- Shape Up은 `No-gos`를 “이 concept에서 하지 않는 것”으로 표현한다. 영구 금지나 전 제품 범위의 폐기 기록으로 정의하지 않는다.  
  https://basecamp.com/shapeup/1.5-chapter-06
- Agile Alliance는 INVEST의 `Negotiable`을 “특정 기능에 대한 구체적 계약이 아님”으로 정의한다. 따라서 No-go를 영구적이고 재논의 불가능한 금지로 취급하면 이 원칙과 긴장된다.  
  https://agilealliance.org/glossary/invest/
- 결론적으로 “자동으로 되살리지 말고 먼저 묻는다”는 동작은 양쪽을 잘 절충하지만, “절대 되살리지 않는다”까지 강화할 근거는 없다.

### backend-family:P1 (1) — plan-prd Gotcha 14

제안된 세 칸 중 외부 근거가 직접 지지하는 범위:

- `무엇`: Shape Up의 `No-gos`가 직접 지지한다.
- `왜 버렸나`: Shape Up은 appetite에 맞추거나 문제를 tractable하게 만들기 위한 제외라고 설명하므로, 이유를 남기는 것은 근거와 잘 맞는다.  
  https://basecamp.com/shapeup/1.5-chapter-06
- `코드에 남은 흔적`: 조회한 출처 중 이를 PRD Non-goal의 필수 필드로 규정한 근거는 찾지 못했다.
- “남은 흔적은 채울 빈틈이 아니라 치울 목록”이라는 분류 역시 조회한 방법론 문서에는 없다.

추론:

- 세 번째 칸과 “흔적을 보고 되살리지 말고 먼저 묻는다”는 이번 18세션에서 발견한 실패 양상을 막는 저장소 고유의 운영 규칙으로 계약해야 한다. 외부 표준의 요구사항이라고 표현하면 안 된다.
- `코드에 남은 흔적`은 정확한 파일/필드명을 적되, 존재 자체가 기능 요구를 의미하지 않는다는 문구가 필요하다.

### backend-family:P1 (2) — 세 PRD 템플릿과 Step 4

확인된 내부 불일치:

- Gotcha 5는 최소 3개 Non-goal을 요구한다. [plan-prd/SKILL.md:19](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/planning-kit/skills/plan-prd/SKILL.md:19)
- Step 4도 Non-goals 3개 이상을 검사한다. [plan-prd/SKILL.md:124](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/planning-kit/skills/plan-prd/SKILL.md:124)
- Shape Up 템플릿에는 `## No-gos`가 있다. [plan-prd/SKILL.md:87](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/planning-kit/skills/plan-prd/SKILL.md:87)
- PR/FAQ 템플릿에는 Non-goals 입력 자리가 없다. [plan-prd/SKILL.md:59](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/planning-kit/skills/plan-prd/SKILL.md:59)
- Linear-style 템플릿에도 없다. [plan-prd/SKILL.md:112](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/planning-kit/skills/plan-prd/SKILL.md:112)

외부 근거:

- Shape Up은 No-gos를 실제 pitch 구성요소로 요구한다.  
  https://basecamp.com/shapeup/1.5-chapter-06

추론:

- `## Non-goals (폐기한 결정 포함)`을 PR/FAQ와 Linear 템플릿에도 추가하는 것은 현행 Gotcha/체크리스트를 실제로 충족 가능하게 만드는 계약 정합성 수정이다.
- Shape Up 원문의 명칭은 `No-gos`이므로 Shape Up 템플릿의 제목은 유지해도 된다. 세 포맷 모두 동일한 의미와 세 칸 구조를 갖도록 정의하는 편이 낫다.
- Step 4에는 단순 개수뿐 아니라 `무엇·왜·코드 흔적` 필드의 완결성을 확인하는 항목이 필요하다.

### backend-family:P1 (3) — plan-data-model·plan-flow Step 0

확인된 사실:

- `plan-data-model` Step 0은 원칙 문서만 읽고 PRD를 자동 로드하지 않는다. [plan-data-model/SKILL.md:33](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/planning-kit/skills/plan-data-model/SKILL.md:33)
- `plan-flow` Step 0도 원칙 문서만 읽는다. [plan-flow/SKILL.md:29](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/planning-kit/skills/plan-flow/SKILL.md:29)
- Mermaid 공식 문서는 ERD가 추상적 논리 모델부터 물리 테이블 모델까지 쓰일 수 있으며, 논리 모델에서는 FK 속성을 생략하는 편이 나을 수도 있다고 명시한다. 즉 코드·DB 흔적을 개념 요구로 그대로 복제하는 것은 공식 문서가 요구하는 동작이 아니다.  
  https://mermaid.js.org/syntax/entityRelationshipDiagram.html

추론:

- 두 Step 0에서 PRD의 Non-goals/No-gos를 읽고 충돌 시 질문하게 하는 것은 폐기 결정이 하류 모델·플로우에서 부활하는 것을 막는 최소 가드다.
- “충돌하면 무조건 중단”보다 “그리기 전에 묻는다”가 적합하다. No-go는 concept/appetite 문맥의 결정이므로 새 증거에 따라 재논의될 가능성을 남겨야 한다.

### backend-family:P1 (4) — plan-stories Step 0

확인된 사실:

- `plan-stories`는 이미 `.planning/prd-*.md`를 읽는다. [plan-stories/SKILL.md:31](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/planning-kit/skills/plan-stories/SKILL.md:31)
- 그러나 Step 1에는 Problem/User/Solution 식별만 있고 No-go 충돌 검사가 없다. [plan-stories/SKILL.md:41](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/planning-kit/skills/plan-stories/SKILL.md:41)
- INVEST의 `Negotiable`은 스토리를 특정 기능의 고정 계약으로 보지 않는다.  
  https://agilealliance.org/glossary/invest/

추론:

- 기존 로드 과정에 “No-gos와 겹치는 스토리는 생성하지 말고 질문한다” 한 줄을 넣는 것은 충분하다.
- 삭제 또는 영구 금지보다 질문이 적절하다. 이는 스토리의 협상 가능성을 유지하면서 묵시적 부활만 차단한다.

### 선택 사항 — plan-audit와 planning-reviewer 동시 수정

확인된 사실:

- `plan-audit`의 Non-goals PASS 조건은 현재 최소 3개 존재 여부만 본다. [plan-audit/SKILL.md:72](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/planning-kit/skills/plan-audit/SKILL.md:72)
- `planning-reviewer`도 Non-goals의 출처 매핑만 있고 하류 산출물의 부활 여부는 검사하지 않는다. [planning-reviewer.md:92](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/planning-kit/agents/planning-reviewer.md:92)

추론:

- Phase 목표가 단순 기록이 아니라 재등장 방지라면 두 곳을 함께 수정하는 편이 계약적으로 완결된다.
- 한쪽만 수정하면 skill 실행과 reviewer 판정 기준이 달라질 수 있으므로 동시 수정이 타당하다.

## 3. 현행화 — 낡은 곳

| 파일:줄 | 현재 값 | 최신 값·상태 | 판단 |
|---|---|---|---|
| [plan-sync-github/SKILL.md:18](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/planning-kit/skills/plan-sync-github/SKILL.md:18), [동일 파일:171](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/planning-kit/skills/plan-sync-github/SKILL.md:171) | Projects REST 링크가 `apiVersion=2022-11-28` | 최신 REST API 버전은 `2026-03-10`. `2022-11-28`도 2028-03-10까지 지원 예정 | 낡았지만 아직 깨지지는 않음. 최신 문서 URL 및 버전으로 옮기려면 breaking-change 검토와 테스트 필요. https://docs.github.com/en/rest/about-the-rest-api/api-versions |
| [docs/planning/flows.md:53](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/planning/flows.md:53) | “공식 문법 10.x+ / 11.x 계열” | 최신 안정판 `12.0.0`, 2026-09-10 공개 | 버전 설명이 한 major 뒤처짐. https://github.com/mermaid-js/mermaid/releases/tag/mermaid%4012.0.0 |
| [plan-data-model/SKILL.md:24](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/planning-kit/skills/plan-data-model/SKILL.md:24), [docs/planning/data-modeling.md:156](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/planning/data-modeling.md:156) | Mermaid 버전 미기재 | Mermaid 12.0.0부터 ERD 기본 theme/look가 바뀌고 레이아웃이 Dagre에서 ELK로 변경됨 | 문법 오류는 아니지만 렌더 결과가 달라질 수 있는 호환성 공백. 버전 또는 렌더 환경을 계약해야 함. https://mermaid.js.org/syntax/entityRelationshipDiagram.html |

추가 점검 결과:

- GitHub REST `2022-11-28`은 deprecated 또는 즉시 sunset 상태가 아니다. 최신판 출시 후 최소 24개월 지원 정책에 따라 2028-03-10까지 지원된다고 공식 문서가 명시한다.  
  https://docs.github.com/en/rest/about-the-rest-api/api-versions
- `2026-03-10`에는 breaking changes가 있으므로 날짜만 기계적으로 교체해서는 안 된다. 공식 지침도 changelog 검토와 통합 테스트를 요구한다.  
  https://docs.github.com/en/rest/about-the-rest-api/breaking-changes
- GitHub CLI 최신 안정 릴리스는 조사 시점 기준 `2.101.0`(2026-09-15)이다. 킷은 특정 버전을 고정하지 않고 실행 시 `gh --version`을 확인하므로, 이 부분은 낡은 고정값이 없다. [plan-sync-github/SKILL.md:33](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/planning-kit/skills/plan-sync-github/SKILL.md:33)  
  https://github.com/cli/cli/releases/tag/v2.101.0
- Cucumber 문서는 여전히 “시나리오당 3–5 steps 권장”, `Then`은 DB 내부가 아니라 시스템 밖의 관찰 가능한 출력이어야 한다고 명시한다. 현행 Gotcha 5/9의 정정 내용과 어긋나는 새 변경은 확인되지 않았다.  
  https://cucumber.io/docs/gherkin/reference

## 4. 권장안

Phase 11 계약 조건으로 삼을 만한 항목은 다음과 같다.

1. PRD의 폐기 결정 SSOT는 각 포맷의 `Non-goals` 또는 `No-gos` 한곳으로 제한한다.

2. 각 폐기 결정은 다음 세 칸을 갖는다.

   - 무엇을 버렸는가
   - 왜 버렸는가
   - 코드에 남은 흔적

3. `코드에 남은 흔적`은 요구사항 후보가 아니라 정리 후보로 정의한다. 흔적과 Non-goal이 충돌하면 자동 복원·자동 모델링·자동 스토리화를 금지하고 사용자에게 질문한다.

4. PR/FAQ와 Linear 템플릿에 `## Non-goals (폐기한 결정 포함)`을 추가한다. Shape Up은 공식 용어인 `## No-gos`를 유지하되 같은 필드 계약을 적용한다.

5. Step 4 검증은 “3개 이상” 외에 다음을 확인한다.

   - 세 칸이 모두 작성됐는가
   - 코드 흔적을 새 요구로 해석하지 않았는가
   - 뒤 단계 산출물이 No-go를 되살리지 않았는가

6. `plan-data-model`, `plan-flow`, `plan-stories`는 PRD의 Non-goals/No-gos를 읽고 충돌 시 생성 전에 질문한다.

7. 선택 사항인 audit/reviewer 보강은 포함하는 편을 권장한다. 두 파일을 반드시 함께 바꿔 판정 기준을 동일하게 유지한다.

8. No-go에는 범위를 함께 기록한다. 예: `이번 PRD`, `이번 appetite/cycle`, `제품 전체`. Shape Up 근거는 기본적으로 concept/appetite 범위이므로 모든 폐기 결정을 영구 금지로 확대하면 안 된다.

9. 현행화 계약에는 다음을 별도 포함한다.

   - GitHub REST 기준 버전은 `2026-03-10`으로 검토하되, breaking-change 테스트 후 전환
   - Mermaid 검증 환경은 `12.0.0`으로 명시하거나 렌더러 버전을 결과에 기록
   - Mermaid 12의 ERD 기본 레이아웃·외관 변경을 스냅샷/시각 검증 대상으로 취급

## 5. 못 가져온 것 / 열린 질문

- `무엇·왜·코드에 남은 흔적`이라는 정확한 세 칸을 요구하는 공식 제품 기획 방법론은 찾지 못했다.
- 서버 필드나 호출되지 않는 화면 파일을 “기능을 되살릴 근거가 아닌 정리 목록”으로 분류하는 직접적인 1차 출처는 찾지 못했다.
- “최소 3개 Non-goal”이라는 숫자는 Shape Up 공식 규칙에서 확인되지 않았다. Shape Up은 No-gos의 존재를 권하지만 최소 개수를 정하지 않는다. 따라서 `3개 이상`은 planning-kit 자체 품질 기준이다.
- 폐기 결정을 PRD에 둘지 별도 decision log/ADR에 둘지 비교하는 외부 자료는 이번 지정 소스 범위에서 조회하지 않았다.
- No-go의 유효기간과 재검토 조건은 열린 질문이다. 최소한 `영구`, `이번 사이클`, `현재 증거가 유지되는 동안`을 구분해야 한다.
- Mermaid 12에서 기존 모든 샘플이 실제 렌더되는지는 실행 검증하지 않았다. 공식 문서상 기본 렌더 방식 변경만 확인했다.
