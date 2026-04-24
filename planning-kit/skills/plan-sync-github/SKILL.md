---
name: plan-sync-github
description: >
  기획 산출물(PRD, Stories, Priorities)을 GitHub Issues · Milestones · Projects v2 에 동기화한다.
  PRD → Epic Issue, Stories → Child Issues, Priorities → Project v2 field, Risks → Issue label.
  "GitHub Issues 만들어줘", "이슈 동기화", "milestone", "프로젝트 보드",
  "sync github", "issue 분해", "gh project" 같은 요청 시 트리거.
  동기화 전 반드시 사용자 확인 — 실제 외부 리소스를 생성하므로 destructive 에 준한다.
argument-hint: "[stories 또는 prd 파일 경로] [--repo owner/name]"
user-invocable: true
---

# Gotchas

1. **확인 없이 생성 금지** — Issues/Milestones 는 외부에 보이는 리소스다. 생성 목록 미리 보여주고 사용자 승인 후 실행. dry-run 먼저.
2. **중복 생성 방지** — 같은 title 이 이미 있으면 새로 만들지 말고 update 하거나 skip. `gh issue list --search` 로 사전 확인.
3. **gh CLI 인증 확인 우선** — `gh auth status` 로 로그인 여부 확인. 미인증이면 사용자에게 `gh auth login` 안내하고 중단.
4. **Projects v2 는 GraphQL** — classic Projects 가 아니다. `gh project` 서브커맨드 또는 `gh api graphql` 사용. CLI 명령 버전은 실행 시점에 `gh --version` 확인하고 필요 시 Codex 로 최신 문법 재확인.
5. **라벨 난립 금지** — 스토리 규모, 리스크 레벨, 우선순위 라벨을 미리 정의하고 일관되게 사용. 매번 새 라벨 만들지 마라.
6. **Body 마크다운 링크 상대경로 금지** — `.planning/prd.md` 같은 상대 경로는 GitHub 에서 열리지 않는다. 저장소 blob URL 로 변환하거나 본문에 인라인 붙여넣기.
7. **Milestone due date 현실성 체크** — Appetite(Shape Up) 또는 Sprint 길이에서 벗어난 due date 면 경고.
8. **Destructive 금지** — 기존 Issue 삭제/닫기 자동 실행 금지. 변경/삭제는 사용자 개별 승인.
9. **Single source of truth 원칙** — target date / status / owner 를 여러 필드에 중복 기록하지 마라. views/fields/automation 은 역할별로 분리. 출처: [GitHub Projects Best Practices](https://docs.github.com/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects).
10. **sub-issue + dependency 활용 필수** — 큰 issue 는 sub-issue 로 분해하고 blocking/blocked 명시. 출처: [GitHub — About Issues](https://docs.github.com/articles/about-issues).
11. **계층 분해 3단계까지** — 레벨 수가 많을수록 운영비가 급증. PRD(문서) → Epic(parent issue) → Story(child issue) → Task(sub-issue/checklist) 가 한계. PR 은 task/story 에 연결하고 PRD 를 직접 닫는 단위로 쓰지 마라. 출처: [GitHub Projects Best Practices](https://docs.github.com/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects).
12. **Milestone 은 release 또는 timebox 중 하나로 일관** — 섞어 쓰면 의미가 흐려짐. 출처: [GitHub — About Milestones](https://docs.github.com/en/enterprise-cloud@latest/issues/using-labels-and-milestones-to-track-work/about-milestones).
13. **gh project 는 project scope 권한 필요** — 반복 리포팅은 `--json`/`--jq` 로 자동화. Project field schema 가 자주 바뀌면 스크립트 유지비 발생. 출처: [gh project manual](https://cli.github.com/manual/gh_project), [gh issue manual](https://cli.github.com/manual/gh_issue).
14. **생성 리소스 ≠ 로컬 산출물** — 이 스킬이 생성하는 GitHub Issues/Milestones/Projects 는 **외부에 보이는 reversible 리소스**다. 로컬 `.planning/*.md` 산출물 생성과 달리 사용자/팀원이 즉시 관측하므로 dry-run + 승인 없이 실행 금지 (Gotcha 1 강화). 실패 시 이미 생성된 리소스는 자동 롤백 금지 — 목록만 보고하고 사용자가 수동 cleanup 결정하도록 둔다 (Gotcha 8).
15. **sync-log 는 재실행 안전성 계약** — `.planning/sync-log-<date>.md` 에 생성된 모든 Issue URL + Milestone number + Project item id 를 기록. 다음 실행에서 이 로그를 먼저 읽어 중복 생성 방지 (Gotcha 2 강화). 로그 없이 재실행하면 같은 Epic 이 #100 / #200 / #300 으로 세 번 생성된다.

# Process

## Step 0: 사전 확인

```bash
gh auth status           # 로그인 여부
gh --version             # 버전 확인
git remote get-url origin # 레포 추론
```

인증 안 되어 있으면 `! gh auth login` 안내 후 중단.

## Step 1: 입력 파싱

- stories 파일 또는 PRD 파일 경로 받기
- `--repo owner/name` 명시 없으면 `gh repo view --json nameWithOwner` 로 추론
- 매핑 규칙 확인:

매핑 근거: [GitHub Projects Best Practices](https://docs.github.com/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects), [About Issues](https://docs.github.com/articles/about-issues).

| 기획 산출물 | GitHub 리소스 |
|------------|---------------|
| PRD | Epic Issue (label: `epic`) |
| Story | Child Issue (label: `story`, body 에 Epic reference) |
| Priority(RICE/Kano) | Project v2 custom field |
| Risk R≥15 | Issue label `risk:high` |
| Appetite/Sprint | Milestone (with due date) |
| Acceptance Criteria (Gherkin) | Issue body 내 task list `- [ ]` |

## Step 2: Dry-run 리포트

사용자에게 다음을 먼저 보여주고 승인 요청:

```text
생성 예정:
- Milestone: "Sprint 12 (2026-05-01 ~ 2026-05-14)" [new]
- Epic Issue: "Checkout redesign" [new]
- Child Issues: 7개 [new]
- Labels: epic, story, risk:high, priority:P0 [new]
- Project v2 field: RICE Score (number) [new]

업데이트:
- Issue #42 "Cart empty state" [AC 업데이트]

충돌/스킵:
- Issue #31 "Guest checkout" 이미 존재 [skip]
```

사용자가 "go" / "yes" / "생성" 응답하면 진행. 그 외 중단.

## Step 3: 생성 순서

순서 중요 — 의존성 있음:

1. **Labels** — 없는 라벨 먼저 생성 (`gh label create`)
2. **Milestone** — `gh api` 로 생성 후 number 확보
3. **Epic Issue** — `gh issue create --label epic --milestone ...`
4. **Child Issues** — body 에 `Part of #<epic-number>` 포함
5. **Project v2 추가** — `gh project item-add <project-number> --owner <owner> --url <issue-url>`
6. **Custom field 업데이트** — GraphQL 또는 `gh project item-edit`

각 단계 실패 시 즉시 중단하고 이미 생성된 리소스 목록 보고. 자동 롤백 금지 (destructive).

## Step 4: Issue Body 템플릿

### Epic
```markdown
<!-- planning-kit: epic -->

## Problem
(PRD 의 Problem 섹션)

## Success Metrics
(Leading / Lagging)

## Stories
- [ ] #<story-1>
- [ ] #<story-2>
...

## Risks (score ≥ 15)
- R1: ... [mitigation]

## Links
- PRD: <blob url>
- Data Model: <blob url>
- Flow: <blob url>
```

### Story
```markdown
<!-- planning-kit: story -->
Part of #<epic-number>

## User Story
As a <persona>,
I want to <goal>,
so that <benefit>.

## Acceptance Criteria
- [ ] Given ... When ... Then ...
- [ ] Given ... When ... Then ...
- [ ] (edge case)

## Priority
- RICE: <score>
- MoSCoW: Must

## Dependencies
- Blocked by: #<id>
```

## Step 5: 검증

생성 후 확인:
- `gh issue list --milestone <milestone>` 개수 일치
- 각 Issue 에 label / body / milestone 반영
- Project 에 추가됐는지 `gh project item-list`

## Step 6: 저장

`.planning/sync-log-<date>.md` 에 동기화 결과 기록 (Issue URL 목록, 실패 항목).

## Step 7: 다음 단계

- 개발 착수 → harness `/sprint-contract` (이슈 하나당 또는 Milestone 단위)
- 구현 후 qa-evaluator REJECT 시 → 자동으로 Issue 에 코멘트 추가하는 후속 자동화 고려

# References

- `docs/planning/github-integration.md` — Issues/Milestones/Projects v2 + gh CLI 패턴 + Linear 비교
- GitHub CLI: `gh help issue` / `gh help project` — 실행 시점 버전 참조

주요 1차 출처:
- [GitHub Docs — Projects Best Practices](https://docs.github.com/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects)
- [GitHub Docs — About Issues](https://docs.github.com/articles/about-issues)
- [GitHub Docs — About Milestones](https://docs.github.com/en/enterprise-cloud@latest/issues/using-labels-and-milestones-to-track-work/about-milestones)
- [gh CLI — gh issue](https://cli.github.com/manual/gh_issue)
- [gh CLI — gh project](https://cli.github.com/manual/gh_project)
- [Linear — GitHub Integration](https://linear.app/docs/github-integration)
