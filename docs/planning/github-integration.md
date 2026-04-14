---
name: github-integration
description: GitHub Projects v2, Issues, Milestones, gh CLI, Linear 비교를 제품 planning 관점에서 정리한 문서
last_updated: 2026-04-14
version: 0.1.0
---

# GitHub Integration

## 개요
2026년 기준 GitHub는 제품 planning 용도로도 꽤 강해졌다. Issues는 더 이상 버그 티켓만이 아니라 sub-issues, dependencies, issue types, Projects v2와 결합된 planning substrate 역할을 한다. 반면 GitHub의 강점은 code adjacency이고, Linear의 강점은 planning-first UX와 workflow opinionation이다.

planning 관점에서 핵심은 도구 선호보다 운영 모델 정렬이다. PRD에서 Epic, Story, Task로 어떻게 분해할지, Issues와 Projects를 어떤 단위로 쓸지, Milestone은 release에 쓸지 timebox에 쓸지, 그리고 `gh` CLI로 어떤 반복 작업을 자동화할지를 명확히 해야 한다.

## 원칙/방법론별 섹션

### GitHub Projects v2 + Issues + Milestones 베스트 프랙티스
**요약**: GitHub 공식 문서 기준으로 Projects는 planning과 tracking의 허브이고, Issues는 계층형 sub-issues와 dependencies, labels, issue types, milestones를 통해 work decomposition을 지원한다. Best practices 문서는 single source of truth, issue breakdown, views/fields/automation 활용을 강조한다.

실무적으로 좋은 기본 구조는 이렇다. Project는 팀/프로덕트 단위 운영판, Issue는 실행 단위, sub-issue는 더 작은 실행 항목, milestone은 release or 목표 시점, labels/issue types는 분류 메타데이터다. 중요한 점은 같은 날짜나 상태를 여러 곳에 중복 기록하지 않는 것이다.

**핵심 질문/포맷/체크리스트**:
- Project를 단일 planning 허브로 쓰고 있는가?
- 큰 issue를 sub-issue로 분해했는가?
- blocking/blocked dependency를 명시했는가?
- target date/status/owner를 중복 필드로 여러 군데 관리하지 않는가?
- views, fields, automation, insights를 역할별로 분리했는가?

**적용 시점**: GitHub-native planning, OSS+product 혼합 워크플로우, 엔지니어링 중심 조직.
**한계/주의사항**: 문서 협업 UX는 Notion/Linear보다 거칠 수 있다. 상태/필드 설계를 과하게 복잡하게 만들면 관리 비용이 급증한다.
**출처**:
- https://docs.github.com/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects
- https://docs.github.com/articles/about-issues
- https://docs.github.com/en/enterprise-cloud@latest/issues/using-labels-and-milestones-to-track-work/about-milestones

### gh CLI 패턴
**요약**: `gh` CLI는 GitHub planning 작업을 터미널에서 다루게 해준다. 공식 manual 기준으로 `gh issue`, `gh project`, `gh search issues` 계열이 planning 자동화의 핵심이다. 특히 project scope 권한과 JSON 출력이 중요하다.

기획/운영 관점의 대표 패턴은 다음과 같다. 이슈 생성과 milestone/project 연결, filtered list 조회, project item/field 조작, search 결과 스크립팅, 내 할 일 상태 확인이다.

**핵심 질문/포맷/체크리스트**:
- 이슈를 만들 때 label/milestone/project를 함께 넣는가?
- 프로젝트와 필드를 CLI로 재현 가능하게 관리하는가?
- 반복 리포팅은 `--json`/`--jq`로 자동화하는가?
- `project` scope가 필요한 명령을 구분했는가?

**적용 시점**: 개발자 친화적 planning, scriptable ops, repo-centric workflow.
**한계/주의사항**: Project field schema가 자주 바뀌면 스크립트 유지비가 든다. 비개발 직군에게는 CLI가 진입장벽이다.
**출처**:
- https://cli.github.com/manual/gh_issue
- https://cli.github.com/manual/gh_issue_create
- https://cli.github.com/manual/gh_project
- https://cli.github.com/manual/gh_project_list

### Linear 와의 비교
**요약**: Linear는 product development system으로 자신을 포지셔닝하며, GitHub integration을 통해 PR/commit/issue sync를 제공한다. 공식 문서 기준으로 branch, PR title, magic words, status automation, two-way issue sync가 핵심이다.

비교를 단순화하면 이렇다. GitHub는 code-adjacent planning이 강하고, Linear는 planning-adjacent code sync가 강하다. GitHub는 repo/issue가 중심이고, Linear는 team/project/workflow UX가 중심이다. 공개 오픈소스 협업과 코드 기준 추적은 GitHub가 자연스럽고, product org 내부 운영과 triage/templates/workflows는 Linear가 더 opinionated하다.

**핵심 질문/포맷/체크리스트**:
- 코드 리뷰와 planning을 하나의 surface에 둘 것인가?
- workflow/status/triage UX를 더 중요하게 보는가?
- 오픈소스 이슈와 사내 product planning을 같은 시스템에 둘 것인가?
- PR/commit 자동화와 issue sync가 필요한가?

**적용 시점**: 도구 선정, hybrid workflow 설계, migration 검토.
**한계/주의사항**: 둘을 완전히 대체 관계로 보면 오판한다. 많은 팀은 GitHub를 source of code, Linear를 source of workflow로 병행한다.
**출처**:
- https://linear.app/docs/github-integration
- https://linear.app/integrations/github
- https://linear.app/docs

### PRD → Epic → Story → Task 분해 패턴
**요약**: planning artifact를 GitHub에 연결할 때 가장 중요한 것은 계층을 tool primitive에 맞게 매핑하는 것이다. 권장 패턴은 PRD를 외부 문서 또는 project README/issue document로 두고, Epic을 parent issue, Story를 child issue 또는 issue type, Task를 sub-issue/checklist로 관리하는 방식이다.

Milestone은 보통 release 또는 timebox와 연결하고, dependency는 issue dependency로 표현한다. PR은 task나 story에 연결하되, PRD를 직접 닫는 단위로 쓰지 않는 편이 좋다.

**핵심 질문/포맷/체크리스트**:
- PRD는 narrative와 success metric을 담는 상위 artifact인가?
- Epic은 outcome/initiative 단위인가?
- Story는 사용자 가치 단위인가?
- Task/Sub-issue는 구현/운영 단위인가?
- close keyword가 어떤 레벨 이슈를 닫는지 규칙이 있는가?

**적용 시점**: 프로젝트 시작 시 작업 분해 규칙 설계, roadmap to repo 연결.
**한계/주의사항**: 레벨 수가 많을수록 운영비가 오른다. 팀 규모와 cadence에 맞게 3단계로 줄일 수도 있다.
**출처**:
- https://docs.github.com/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects
- https://docs.github.com/articles/about-issues
- https://linear.app/docs/project-templates

## 참고 링크 (전체)
- https://docs.github.com/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects
- https://docs.github.com/articles/about-issues
- https://docs.github.com/en/enterprise-cloud@latest/issues/using-labels-and-milestones-to-track-work/about-milestones
- https://cli.github.com/manual/gh_issue
- https://cli.github.com/manual/gh_issue_create
- https://cli.github.com/manual/gh_project
- https://cli.github.com/manual/gh_project_list
- https://linear.app/docs/github-integration
- https://linear.app/integrations/github
- https://linear.app/docs
- https://linear.app/docs/project-templates
