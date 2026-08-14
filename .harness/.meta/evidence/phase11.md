---
phase: 11
title: "Phase 11 planning-kit — 확보된 외부 근거"
collected: 2026-08-13
method: codex (foreground, 직접 호출)
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치를 지어내지 마라.
---

출처 유형: Codex  
웹 검색 사용: 2/8회. 파일 수정 없음.

**1. 관찰 사실**

- Teresa Torres / Product Talk URL은 유효. `Continuous Discovery`는 weekly customer touchpoints, small research activities, desired outcome 중심으로 현재 문서와 로컬 요약이 맞습니다. `Opportunity Solution Tree`도 Desired Outcome / Opportunity Space / Solution Space / Assumption Tests 4층 구조로 현재 문서와 일치합니다. 추론: 변경 필요 없음. ([]()) ([]())
- Marty Cagan / SVPG `Four Big Risks` URL은 유효. value, usability, feasibility, business viability 4축과 “big risks early” 취지는 현재 문서와 일치합니다. 추론: 변경 필요 없음. ([]())
- Basecamp Shape Up URL은 유효. Chapter 6은 Pitch의 5요소 Problem / Appetite / Solution / Rabbit Holes / No-gos를 유지하고, Appetite를 시간 제약으로 설명합니다. Betting Table은 Chapter 8 URL이 정본이며, cool-down 중 다음 cycle 결정을 하는 회의로 설명됩니다. 추론: Betting Table을 인용하는 곳에는 `https://basecamp.com/shapeup/2.2-chapter-08`가 더 정확합니다.  ([basecamp.com](https://basecamp.com/shapeup/2.2-chapter-08))
- Agile Alliance INVEST URL은 유효. INVEST 6항목과 Testable의 “in principle” 의미가 현재 문서에 있습니다. [plan-stories/SKILL.md](/Users/jackson/Hub/10_Dev/claude-plugins/planning-kit/skills/plan-stories/SKILL.md:88)의 반증가능성 강화는 현재 출처와 합치됩니다. 
- Cucumber Gherkin Reference URL은 유효하며 trailing slash로 리다이렉트됩니다. 현재 문서는 Example/Scenario가 3-5 steps 권장, Given/When/Then 패턴, Then의 observable output 원칙을 말합니다. 다만 “한 시나리오 = one When-Then pair”라는 원문은 확인되지 않았습니다. 오히려 “as many steps as you like”와 successive `Then` 예시가 있습니다. ([cucumber.io](https://cucumber.io/docs/gherkin/reference/))
- HBR `Performing a Project Premortem` URL은 유효. Gary Klein, September 2007, premortem 요약까지 확인됩니다. 단, [plan-risks/SKILL.md](/Users/jackson/Hub/10_Dev/claude-plugins/planning-kit/skills/plan-risks/SKILL.md:22)의 “개별 기록 → 공유” 절차 원문은 접근 가능한 HBR 본문에서 미확인입니다. ([hbr.org](https://hbr.org/2007/09/performing-a-project-premortem))
- Mermaid ER Diagram URL은 유효. Mermaid ER 문법, relationship statement 구성, FK 포함 여부는 모델 목적에 따른 선택이라는 내용이 현재 문서에 있습니다. 추론: 핵심 내용 변경 없음. 단 `v10` 같은 버전 고정 표현은 현재 문서 URL 자체에서는 확인되지 않습니다. 
- GitHub Projects v2 API 현황: `Projects v2 = GraphQL only`는 현재 기준으로 틀립니다. GitHub 공식 “Using the API to manage Projects”는 여전히 GraphQL 자동화를 문서화하고 `projectV2`, `addProjectV2ItemById`, `updateProjectV2ItemFieldValue`를 제공합니다. 동시에 REST 공식 문서가 `/orgs/{org}/projectsV2`, `/projectsV2/{project_number}/items`, `/fields` 등 Projects v2 REST endpoints를 제공합니다. ([basecamp.com](https://basecamp.com/shapeup/2.2-chapter-08)) ([docs.github.com](https://docs.github.com/en/rest/projects/items?apiVersion=2022-11-28)) ([docs.github.com](https://docs.github.com/en/rest/projects/items?apiVersion=2022-11-28)) ([docs.github.com](https://docs.github.com/en/rest/projects/items?apiVersion=2022-11-28))
- GitHub Issues/Milestones REST는 현재 지원됩니다. Issue 생성은 `POST /repos/{owner}/{repo}/issues`, milestone 생성은 `POST /repos/{owner}/{repo}/milestones`로 확인됩니다. ([docs.github.com](https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28)) ([docs.github.com](https://docs.github.com/en/rest/issues/milestones?apiVersion=2022-11-28))
- Projects classic은 폐지 흐름이 아니라 이미 sunset 기준을 지난 상태입니다. GitHub Changelog는 GitHub.com classic projects sunset을 2024-08-23, classic REST API sunset을 2025-04-01로 명시합니다. GraphQL classic reference도 classic 타입/뮤테이션 deprecated 및 removal date를 표시합니다.  ([docs.github.com](https://docs.github.com/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects))
- `gh project`는 현재 유효합니다. `gh project item-add`는 issue/PR URL 추가를 지원하고, `gh project item-edit`는 field name 또는 GraphQL node ID 방식 모두 지원합니다. [plan-sync-github/SKILL.md](/Users/jackson/Hub/10_Dev/claude-plugins/planning-kit/skills/plan-sync-github/SKILL.md:89)의 `item-add --url` 패턴은 현재 CLI 문서와 일치합니다. ([cli.github.com](https://cli.github.com/manual/gh_project_item-add)) ([cli.github.com](https://cli.github.com/manual/gh_project_item-edit))

**2. 권장안**

- [plan-sync-github/SKILL.md](/Users/jackson/Hub/10_Dev/claude-plugins/planning-kit/skills/plan-sync-github/SKILL.md:18)의 “Projects v2 는 GraphQL”을 “Projects v2는 `gh project`, GraphQL, REST `/projectsV2` 모두 지원. classic Projects API 금지”로 갱신.
- [docs/planning/research-log.md](/Users/jackson/Hub/10_Dev/claude-plugins/docs/planning/research-log.md:31)와 [docs/planning/research-log.md](/Users/jackson/Hub/10_Dev/claude-plugins/docs/planning/research-log.md:101)의 GraphQL-only/REST→GraphQL 전환 판단은 현재 REST v2 지원 사실로 정정.
- [plan-stories/SKILL.md](/Users/jackson/Hub/10_Dev/claude-plugins/planning-kit/skills/plan-stories/SKILL.md:19)의 “When 여러 개 섞지 마라”는 Cucumber 원문 근거가 아니라 planning-kit 내부 원자성 규칙으로 라벨링. Cucumber 공식 근거로는 3-5 steps, observable Then만 인용.
- [plan-risks/SKILL.md](/Users/jackson/Hub/10_Dev/claude-plugins/planning-kit/skills/plan-risks/SKILL.md:22)의 HBR 세부 절차 근거는 미확인 처리하거나 접근 가능한 정본 원문 확보 후 유지.

**3. 트레이드오프**

- GraphQL 중심 지침은 단순하지만 현재 REST `/projectsV2` 지원을 놓칩니다. REST+GraphQL 병기 방식은 정확하지만 스킬 지침이 약간 길어집니다.
- “one When” 규칙은 AC를 작게 유지하는 데 유용하지만, Cucumber 공식 문서라고 쓰면 과잉 인용입니다. 내부 품질 규칙으로 낮추면 정확성이 올라갑니다.
- HBR premortem은 URL 자체는 살아있지만 본문 일부만 확인됩니다. 절차 세부까지 강하게 주장하려면 접근 가능한 1차 원문이 필요합니다.

**4. 열린 질문**

- `plan-sync-github`의 기본 실행 경로를 `gh project` 유지로 둘지, REST `/projectsV2`를 명시적 fallback으로 둘지 결정 필요.
- HBR 원문/PDF 접근 권한이 있는지 확인 필요. 없으면 “개별 기록 → 공유” 문구는 `[미확인]` 또는 비인용 내부 운영 팁으로 내려야 합니다.
