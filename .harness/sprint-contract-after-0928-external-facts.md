---
feature: "바깥 원문 대조 반영 (A5 ~ A13)"
slug: after-0928-external-facts
created: "2026-09-28 10:51"
complexity: "복잡"
conditions: 29
status: active
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:72ee727e080b7190
measurement_digest: sha256:755b6e62692e0170
locked_at: "2026-09-28 10:59"
---

## 배경

- 남은 일 목록 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/.harness/.meta/after-kaizen-0928/remaining.md` 의 A5 ~ A13 아홉 건. 모두 「바깥 근거 없음」 으로 남았던 것이다.
- 원문 대조 결과는 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/.harness/.meta/after-kaizen-0928/ex/A5.md` ~ `A13.md` (Codex gpt-5.6-sol, 2026-09-28 조회, 읽기 전용). 이 계약에서 「ex 파일」 은 이 폴더를 말한다.
- 처리 규칙: ex 파일 판정이 「맞음」 이면 저장소 문장에 출처(주소 · 2026-09-28)만 붙인다. 「틀림」 이면 원문대로 고친다. 「원문에 없음」 이면 단정을 빼거나 「이 킷 규칙」 · 「확인 못 함」 으로 낮춘다. ex 파일에 인용이 없는 새 사실은 쓰지 않는다 (ER-01 이 주소로 잰다).
- 원본을 바꾸면 대응 문서 페이지도 같이 맞춘다 (레포 `.claude/skills/docs-site/SKILL.md`). 페이지 짝은 조건마다 적었다.
- 사용자 위임: 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 · 2026-09-28 「약점과 일부만 한 거 다처리하지??」 (세션 bda55d45-296c-491f-89ba-b52042d58e72). 결정 기록 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/.harness/.meta/after-kaizen-0928/decisions.md`.
- 기준 판(이하 BASE): `e78ea2f` (가지 `chore/ak3-ex` 를 만든 시점). 끝 판(이하 TIP): 모든 커밋이 끝난 뒤 `git rev-parse chore/ak3-ex` 의 출력. `HEAD` 를 쓰지 않는다.
- 모든 측정은 작업 폴더 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-ex` 를 현재 폴더로 두고 돌린다. 셸은 zsh 도 bash 도 같은 결과가 나오게 글로빙을 쓰지 않았다.

## GAP 분석

| 항목 | ex 판정 요지 | 저장소 자리 (BASE 에서 연 줄) | 조건 |
| --- | --- | --- | --- |
| A5 | 「Android 16」 원문에 없음 · 「tonal palette 정교화」 「컬러 토큰 세트」 「Roboto Flex 로 시스템화」 틀림 · 46 연구 / 18,000 명 이상 · spring 맞음 · primitive 매핑은 저장소 관례 | `design-kit/skills/design-system/SKILL.md:109` | SK-01 |
| A6 | go_router 최신 18.0.1 (Flutter 3.44 / Dart 3.12) · `notifyRootObserver: false` 복원 원문에 없음 · auto_route 최신 11.2.0 · `.named` 는 11.1.0 · `animatePageTransition` 폐기 예정 빠짐 · 「컴파일 에러」 원문에 없음 | `flutter-toolkit/skills/flutter-screen/SKILL.md:22` · `flutter-toolkit/skills/flutter-transition/SKILL.md:22` | SK-02 |
| A7 | OpenTofu mocking 1.8+ · write-only 1.11+ (1.7+ 틀림) · state encryption 1.7+ 맞음 · GitLab `sha` / Buildkite `commit` 로 커밋별 실행 조회 가능 · Argo CD 3.5 는 API 제거가 아니라 gRPC 응답 형식 변경 · K8s 1.37 `scheduling.k8s.io/v1alpha2` 제거 맞음 | `infra-kit/references/audit-criteria.md:106` · `infra-kit/references/init-checklist.md:134` · `infra-kit/skills/infra-test/SKILL.md:28,30` · `docs/infra/platform/cicd.md:95` · `docs/infra/research-log.md:18,68,70` | SK-03 · SK-04 · SK-05 |
| A8 | 오프셋 없는 벽시계 문자열은 RFC 3339 / OpenAPI `date-time` 이 아니다 · IANA 칸 FAIL 과 순간 하나 저장 FAIL 은 원문에 없음 (이 킷 규칙) | `backend-kit/skills/backend-audit/references/audit-criteria.md:28,40` · `docs/backend/fundamentals/database.md:140~` | SK-06 · SK-07 |
| A9 | Activity 는 React 19.2 정식 판에 들어 있다 — 「canary 에서 안정화 중」 틀림 | `react-kit/skills/react-screen/SKILL.md:24` | SK-08 |
| A10 | Mermaid 12.0.0 맞음 (npm latest 2026-09-28) · PRD 와 ADR 중 하나를 우선하라는 원문은 없다 | `docs/planning/flows.md:61` · 저장소 킷 문장에는 PRD · ADR 우열 단정이 없다 (단정은 `.harness/.meta` 기록뿐) | SK-09 · SK-10 |
| A11 | C-06 MUST 의 근거인 「공식 강제」 틀림 (Effective Dart 는 PREFER) · etc_seq=663 이름은 「유형별로 알아보는 보도자료 작성 길잡이」 · `__` 대신 `_` 맞음 | `tone-kit/references/core-comment.md:19` · `docs/tone/comment-economy.md:233,236` · `docs/tone/templates.md:121` · 이름표 8 파일 · `docs/tone/overview.md:155` · `docs/tone/dart-flutter-idioms.md:440` | SK-11 · SK-12 · SK-13 |
| A12 | 평가 사례 조회일 · 갱신일 낡음 · FCM Apple 문서는 `.p12` 를 아예 언급하지 않는다 · 앱 번들 금지 맞음 (서비스 계정 키는 피하라는 권고) | `onboarding-kit/skills/setup-guide/evals/evals.json:10,69,72,73` · `docs/onboarding-kit/examples/fcm-ios-setup-guide.md:358` | SK-14 · SK-15 |
| A13 | 필수 필드 `name` · `description` 맞음 · 중첩 3 층은 기본값이고 환경 변수로 바뀐다 (「하드 리밋」 틀림) · 「상한에 걸리면 Agent 도구가 실패」 틀림 · 깊이 오류 글자는 원문에 없음 | `harness/docs/guides/agent-design-guide.md:73,239,241,469,721` | SK-16 |

## 범위 경계

- 하지 않는 것: A5 의 `design:P2` 규칙 방향(C3) — 사용자 결정이라 건드리지 않는다. `.harness/` 아래 봉인된 계약 · QA 리포트 · 개정 파일과 `.harness/.meta` 기록(`leftovers.md` · `phase*-notes.md`)은 고치지 않는다 — ex 파일도 「역사 기록이라 소급 수정할 필요 없다」 고 적었다.
- 하지 않는 것: `design-kit/docs/design/systems/material-design.md` 와 그 페이지의 「Android 16」 — 그 문서는 Android Developers Blog 를 따로 출처로 달았고, ex 파일(A5)은 m3.material.io 만 조회했다. 그 출처를 대조하지 않았으므로 이번에 판정하지 않는다.
- 하지 않는 것: `docs/flutter/architecture/routing.md:85-86` 의 `(_, __)` — A11 은 tone 예시만 물었다. 같은 Dart 사실이지만 flutter 문서 정리는 이 묶음 밖이다.
- 하지 않는 것: ex 파일이 「추론」 으로 제안한 새 규칙(벽시계 문자열 `YYYY-MM-DDTHH:mm:ss` 모양 고정 · PRD / ADR 경계 규칙 · setup-guide 의 조회일 · 갱신일 분리 규칙 · 서비스 계정 선택 나무 전체) — 인용 없는 새 사실이 되므로 넣지 않는다. 평가 날짜 규칙(A12)은 저장소가 바깥 근거를 주장한 적이 없어 「이미 됨」 으로 둔다.
- `docs/planning/research-log.md` 는 대응 페이지가 없는 것이 결정이다 (A2 매핑 결정 「페이지 없음이 맞음」). SK-10 은 원본만 고친다.
- 조건 수: 기능 조건 21 개로 가이드 상한 20 을 하나 넘는다. 오케스트레이터가 아홉 건을 한 묶음으로 배정했고 킷별 커밋(AR-01)으로 이미 나뉘어 있어 스프린트를 다시 쪼개지 않는다.
- 교차 진단 반영: SK-16 이 `하드 리밋` 을 통째로 0 으로 요구하면 동시 실행 20 개 쪽 표현도 바뀐다. ex 파일 A13 F 절이 원문을 「기본적으로 20 개가 실행 중일 때」 로 옮겼고, 3 절 제안 문장(721 행)이 「두 값은 각각 환경 변수로 변경할 수 있으며」 라 적었다. BASE 469 행도 이미 `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` 를 적었다. 그래서 동시 실행 20 개도 「기본값」 으로 부르는 것은 ex 파일 인용 안이다.
- 커버리지 해소: SK-12 — 검출기가 짚은 `.harness` 는 측정에서 뺄 경로(`:!.harness`)라 대상이 아니다. 여덟 파일은 측정 절에 같은 표기로 전부 적었다.
- 커버리지 해소: AR-02 — `.harness/` 는 제외 경로, `CF=…` 는 측정 변수 정의라 대상이 아니다.
- 오라클 해소: SK-01 · SK-02 · SK-05 · SK-06 · SK-07 · SK-09 · SK-10 · SK-11 · SK-12 · SK-15 · SK-16 — 이 스프린트의 산출물이 문서 문장 자체라 글자 대조가 곧 동작 관찰이다. 각 조건에 BASE 값(양성 대조)을 적어 구현을 빼면 FAIL 함을 보였다. SC-01 · ER-01 · AR-02 · AR-03 — 측정이 명령을 실제로 돌려 종료 코드와 출력으로 판정한다(검출기 오탐).
- 범위 목록 (이 밖의 경로를 담은 커밋은 막힌다):

```text
# sprint-scope
design-kit/skills/design-system/SKILL.md
flutter-toolkit/skills/flutter-screen/SKILL.md
flutter-toolkit/skills/flutter-transition/SKILL.md
infra-kit/references/audit-criteria.md
infra-kit/references/init-checklist.md
infra-kit/skills/infra-test/SKILL.md
docs/infra/platform/cicd.md
docs/infra/research-log.md
docs/infra-kit/infra-test.html
docs/infra-kit/cicd.html
docs/infra-kit/research-log.html
backend-kit/skills/backend-audit/references/audit-criteria.md
docs/backend/fundamentals/database.md
docs/backend-kit/database.html
react-kit/skills/react-screen/SKILL.md
docs/planning/flows.md
docs/planning/research-log.md
docs/planning-kit/flows.html
tone-kit/references/core-comment.md
tone-kit/references/sources.md
tone-kit/references/locale-korean.md
docs/tone/comment-economy.md
docs/tone/templates.md
docs/tone/korean-technical-writing.md
docs/tone/overview.md
docs/tone/dart-flutter-idioms.md
docs/tone-kit/comment-economy.html
docs/tone-kit/templates.html
docs/tone-kit/korean-technical-writing.html
docs/tone-kit/locale-korean.html
docs/tone-kit/overview.html
docs/tone-kit/sources.html
docs/tone-kit/dart-flutter-idioms.html
onboarding-kit/skills/setup-guide/evals/evals.json
docs/onboarding-kit/examples/fcm-ios-setup-guide.md
docs/onboarding-kit/fcm-ios-example.html
harness/docs/guides/agent-design-guide.md
docs/harness/agent-design-guide.html
```

## 회귀 게이트

- BASE 실측(2026-09-28): `ci-local.sh` 25 단계 rc=0 · `feedback-agg-test SKIP (yq 없음)` 1 줄. CI 파일에만 있는 여섯 단계(`check-api-kit-docs` · `detect-docs-drift --check-table` · `check-cause-table-copies` · `measure-helpers-test` · `bambu-kit/evals/run-gate-fixtures.sh` · `bambu-kit/evals/makerworld-fetch-test.sh`) 전부 rc=0.
- BASE 실측: 14 페이지 `node scripts/check-docs-a11y.js` → `14/14 PASS`, rc=0. 양성 대조: 너비 2000px 요소를 넣은 사본은 `FAIL … of=1680/1625/1232/720`, rc=1.
- BASE 실측: 바꿀 md 23 파일 markdownlint-cli2 0.23.2 (MD013 끔) 경고 전부 0. 양성 대조: `docs/tone/overview.md` 사본 끝에 `#bad heading` · 빈 줄 여럿 · 줄 끝 공백을 붙이면 4, rc=1.

## Skill

- [ ] SK-01: (A5) `design-kit/skills/design-system/SKILL.md` 의 `**참고 — Material 3 Expressive` 로 시작하는 문단이 원문대로 고쳐졌다 — 원문에 없거나 틀린 네 말(`Android 16` · `tonal palette 정교화` · `컬러 토큰 세트` · `variable font axes`)이 0 번 나오고, 공식 출처 네 주소와 조회일과 원문 표현 셋(`18,000명 넘는` · `type scale 에 포함되지 않는다` · primitive 매핑을 적은 `저장소 관례`)이 각각 1 번 이상 나온다 [exact, enumerated]
  Given: 모든 커밋 뒤, 작업 폴더에서.
  측정: `f=design-kit/skills/design-system/SKILL.md; grep -cF '**참고 — Material 3 Expressive' $f` 이 1. 이어서 `L=$(grep -F '**참고 — Material 3 Expressive' $f)` 로 그 줄을 잡고 낱말마다 `printf '%s\n' "$L" | grep -cF '<낱말>'`.
  0 이어야 하는 것: `Android 16` · `tonal palette 정교화` · `컬러 토큰 세트` · `variable font axes`.
  1 이상이어야 하는 것: `https://m3.material.io/blog/building-with-m3-expressive` · `https://m3.material.io/styles/color/system/overview` · `https://m3.material.io/styles/typography/overview` · `https://m3.material.io/styles/motion/overview` · `2026-09-28` · `18,000명 넘는` · `type scale 에 포함되지 않는다` · `저장소 관례`.
  양성 대조: BASE 에서 0 이어야 하는 네 낱말이 각각 1, 1 이상이어야 하는 여덟 낱말이 각각 0 이다 (2026-09-28 실측).
- [ ] SK-02: (A6) go_router · auto_route 줄이 최신 판과 원문에 맞게 고쳐졌다 — `flutter-toolkit/skills/flutter-screen/SKILL.md` 의 `- **go_router` 줄과 `flutter-toolkit/skills/flutter-transition/SKILL.md` 의 `- **auto_route` 줄이 아래 낱말 조건을 모두 만족한다 [exact, enumerated]
  Given: 모든 커밋 뒤, 작업 폴더에서.
  측정: 두 파일에서 각 머리 문자열을 가진 줄이 `grep -cF -- '- **go_router' flutter-toolkit/skills/flutter-screen/SKILL.md` · `grep -cF -- '- **auto_route' flutter-toolkit/skills/flutter-transition/SKILL.md` 로 각각 1. 낱말마다 `grep -F -- '<머리>' <파일> | grep -cF -- '<낱말>'`.
  go_router 줄 1 이상: `go_router 18.0.1` · `Flutter 3.44 / Dart 3.12` · `material_ui` · `cupertino_ui` · `ShellRoute` · `https://pub.dev/packages/go_router/changelog` · `2026-09-28`. go_router 줄 0: `notifyRootObserver: false` · `의도치 않은 동작` · `Flutter 3.32 / Dart 3.8`.
  auto_route 줄 1 이상: `auto_route 11.2.0` · `animatePageTransition` · `11.1.0` · `.named` · `redirectUntil` · `https://pub.dev/packages/auto_route/changelog` · `2026-09-28`. auto_route 줄 0: `컴파일 에러`.
  양성 대조: BASE 에서 go_router 줄의 0 기대 셋이 각 1, auto_route 줄의 `컴파일 에러` 가 1 이다.
  측정 대상: `flutter-toolkit/skills/flutter-screen/SKILL.md` · `flutter-toolkit/skills/flutter-transition/SKILL.md`
- [ ] SK-03: (A7) OpenTofu 기능 하한이 원문대로 고쳐졌다 — 네 파일 `infra-kit/references/audit-criteria.md` · `infra-kit/references/init-checklist.md` · `infra-kit/skills/infra-test/SKILL.md` · `docs/infra-kit/infra-test.html` 에서 `1.7+` 가 0 줄이고, 네 파일 모두 mocking 하한 `1.8+` 와 v1.8.0 릴리스 주소를 담고, 뒤의 두 파일은 write-only 하한 `1.11+ write-only` 와 v1.11.0 릴리스 주소를 담는다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: 네 파일 각각 `grep -cF '1.7+' <파일>` 이 0, `grep -cF '1.8+' <파일>` 이 1 이상, `grep -cF 'https://github.com/opentofu/opentofu/releases/tag/v1.8.0' <파일>` 이 1 이상.
  `infra-kit/skills/infra-test/SKILL.md` · `docs/infra-kit/infra-test.html` 각각 `grep -cF '1.11+ write-only' <파일>` 이 1 이상, `grep -cF 'https://github.com/opentofu/opentofu/releases/tag/v1.11.0' <파일>` 이 1 이상.
  양성 대조: BASE 에서 `1.7+` 줄 수가 1 · 1 · 2 · 4 이고, 나머지 낱말은 네 파일 모두 0 이다.
  측정 대상: `infra-kit/references/audit-criteria.md` · `infra-kit/references/init-checklist.md` · `infra-kit/skills/infra-test/SKILL.md` · `docs/infra-kit/infra-test.html`
- [ ] SK-04: (A7) 「GitHub 밖 CI 의 조회 명령은 근거에 없다」 가 원문대로 고쳐졌다 — `docs/infra/platform/cicd.md` 와 대응 페이지 `docs/infra-kit/cicd.html` 둘 다 옛 문장이 0 줄이고, GitLab Pipelines 주소 · Buildkite Builds 주소 · `2026-09-28` · 한계를 적은 `필수 검사 전체` 를 1 번 이상 담는다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: 두 파일 각각 `grep -cF 'GitHub 밖 CI 의 같은 조회 명령은 이 문서의 근거에 없다' <파일>` 이 0. `grep -cF 'https://docs.gitlab.com/api/pipelines/' <파일>` · `grep -cF 'https://buildkite.com/docs/apis/rest-api/builds' <파일>` · `grep -cF '2026-09-28' <파일>` · `grep -cF '필수 검사 전체' <파일>` 이 각각 1 이상.
  양성 대조: BASE 에서 옛 문장이 두 파일 각 1, 나머지 넷은 각 0.
  측정 대상: `docs/infra/platform/cicd.md` · `docs/infra-kit/cicd.html`
- [ ] SK-05: (A7) 인프라 조사 기록에 2026-09-28 정정 절이 있다 — `docs/infra/research-log.md` 에 `## [2026-09-28]` 로 시작하는 절이 정확히 1 개이고, 그 절 안에 Flux v2.9.0 주소 · Argo CD 3.4→3.5 가이드 주소 · `gRPC 응답` · `scheduling.k8s.io/v1alpha2` · OpenTofu v1.7.0 주소 · `1.8+` · `1.11+` 가 각각 1 번 이상 나온다. 대응 페이지 `docs/infra-kit/research-log.html` 은 `2026-09-28` · `gRPC 응답` · `releases/tag/v1.7.0` 을 각각 1 번 이상 담는다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: `grep -c '^## \[2026-09-28\]' docs/infra/research-log.md` 이 1. 절 자르기: `awk '/^## /{p=($(0) ~ /^## \[2026-09-28\]/)} p' docs/infra/research-log.md` 의 출력에 낱말마다 `grep -cF`.
  절 안 1 이상: `https://github.com/fluxcd/flux2/releases/tag/v2.9.0` · `https://argo-cd.readthedocs.io/en/stable/operator-manual/upgrading/3.4-3.5/` · `gRPC 응답` · `scheduling.k8s.io/v1alpha2` · `https://github.com/opentofu/opentofu/releases/tag/v1.7.0` · `1.8+` · `1.11+`.
  페이지: `grep -cF '<낱말>' docs/infra-kit/research-log.html` 이 `2026-09-28` · `gRPC 응답` · `releases/tag/v1.7.0` 각각 1 이상.
  양성 대조: BASE 에서 절 머리 0, 페이지 세 낱말 각 0.
  측정 대상: `docs/infra/research-log.md` · `docs/infra-kit/research-log.html`
- [ ] SK-06: (A8) 백엔드 감사 기준의 두 행이 원문에 맞게 고쳐졌다 — `backend-kit/skills/backend-audit/references/audit-criteria.md` 의 `| Timestamp 직렬화 규칙 |` 행이 오프셋 없는 벽시계 문자열에 `date-time` 을 붙이면 안 된다는 판정을 원문 주소 · 조회일과 함께 담고, `| 시각 종류별 저장 |` 행이 IANA 칸 FAIL 이 표준 요구가 아니라 `이 킷 규칙` 이라고 IANA 주소와 함께 밝힌다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: `f=backend-kit/skills/backend-audit/references/audit-criteria.md`. 두 머리 줄 수 `grep -cF '| Timestamp 직렬화 규칙 |' $f` · `grep -cF '| 시각 종류별 저장 |' $f` 가 각 1.
  Timestamp 행 1 이상 (`grep -F '| Timestamp 직렬화 규칙 |' $f | grep -cF '<낱말>'`): `오프셋 없는 벽시계` · `https://spec.openapis.org/registry/format/date-time` · `2026-09-28`.
  시각 종류별 저장 행 1 이상: `이 킷 규칙` · `https://www.iana.org/time-zones/theory`.
  양성 대조: BASE 에서 다섯 낱말 모두 각 행에서 0.
- [ ] SK-07: (A8) `docs/backend/fundamentals/database.md` 원칙 10 절과 대응 페이지 `docs/backend-kit/database.html` 이 벽시계 API 표기 사실과 규칙의 출처 성격을 담는다 — 절 안에 `format: date-time` · `time-offset` · RFC 3339 주소 · IANA 주소 · `이 킷 규칙` · `2026-09-28` 이 각각 1 번 이상, 페이지에 `format: date-time` · `time-offset` · `iana.org/time-zones/theory` · `2026-09-28` 이 각각 1 번 이상 나온다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: 절 자르기 `awk '/^#{2,3} /{p=($(0) ~ /^### 10\./)} p' docs/backend/fundamentals/database.md` (BASE 26 줄) 의 출력에 `grep -cF`.
  절 안 1 이상: `format: date-time` · `time-offset` · `https://www.rfc-editor.org/rfc/rfc3339` · `https://www.iana.org/time-zones/theory` · `이 킷 규칙` · `2026-09-28`.
  페이지 1 이상 (`grep -cF '<낱말>' docs/backend-kit/database.html`): `format: date-time` · `time-offset` · `iana.org/time-zones/theory` · `2026-09-28`.
  양성 대조: BASE 에서 절 여섯 낱말 · 페이지 네 낱말 모두 0.
  측정 대상: `docs/backend/fundamentals/database.md` · `docs/backend-kit/database.html`
- [ ] SK-08: (A9) `react-kit/skills/react-screen/SKILL.md` Gotcha 11 이 canary 단정을 버리고 React 19.2 발표 글을 출처로 단다 — 파일 전체 `canary` 0 줄(대소문자 무시), `11. **React 19.2` 로 시작하는 줄이 1 개이고 그 줄에 `https://react.dev/blog/2025/10/01/react-19-2` 와 `2026-09-28` 이 있다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: `grep -ci canary react-kit/skills/react-screen/SKILL.md` 이 0. `grep -cF '11. **React 19.2' react-kit/skills/react-screen/SKILL.md` 이 1. `grep -F '11. **React 19.2' react-kit/skills/react-screen/SKILL.md | grep -cF '<낱말>'` 이 두 낱말 각 1.
  양성 대조: BASE 에서 `canary` 1 줄, 두 낱말 각 0.
  측정 대상: `react-kit/skills/react-screen/SKILL.md` · `https://react.dev/blog/2025/10/01/react-19-2`
- [ ] SK-09: (A10) `docs/planning/flows.md` 의 `아래 예시는` 으로 시작하는 줄과 대응 페이지 `docs/planning-kit/flows.html` 이 Mermaid 12.0.0 재확인 날짜와 npm 주소를 담고, 「렌더해 보지는 않았다」 는 그대로 남긴다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: `grep -c '^아래 예시는' docs/planning/flows.md` 이 1. `grep '^아래 예시는' docs/planning/flows.md | grep -cF '<낱말>'` 이 `2026-09-28` · `https://registry.npmjs.org/mermaid/latest` · `렌더해 보지는 않았다` 각 1.
  페이지: `grep -cF '<낱말>' docs/planning-kit/flows.html` 이 `2026-09-28` · `registry.npmjs.org/mermaid/latest` 각 1 이상, `렌더해 보지는 않았다` 3 이상 (BASE 3).
  양성 대조: BASE 에서 원본 줄의 앞 두 낱말 0, 페이지 앞 두 낱말 0.
  측정 대상: `docs/planning/flows.md` · `docs/planning-kit/flows.html`
- [ ] SK-10: (A10) `docs/planning/research-log.md` 에 PRD · ADR 비교 결과를 적은 `## [2026-09-28]` 절이 정확히 1 개 있고, 그 절이 세 원문 주소와 결론 문장 `우선하라는 원문은 찾지 못했다` 를 담는다. 대응 페이지는 만들지 않는다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: `grep -c '^## \[2026-09-28\]' docs/planning/research-log.md` 이 1. `awk '/^## /{p=($(0) ~ /^## \[2026-09-28\]/)} p' docs/planning/research-log.md | grep -cF '<낱말>'` 이 `https://www.atlassian.com/agile/product-management/requirements` · `https://adr.github.io/` · `https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions` · `우선하라는 원문은 찾지 못했다` 각 1 이상. `test ! -e docs/planning-kit/research-log.html` 이 참.
  양성 대조: BASE 에서 절 머리 0.
- [ ] SK-11: (A11) C-06 강도가 원문 강도(Effective Dart 의 PREFER)에 맞춰 `SHOULD` 로 내려가고, 「공식 강제 항목」 문장이 원문대로 고쳐졌다 — 여섯 자리 `tone-kit/references/core-comment.md` · `docs/tone/comment-economy.md` · `docs/tone-kit/comment-economy.html` · `docs/tone/templates.md` · `docs/tone-kit/templates.html` 이 아래 값을 낸다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정 core-comment: `grep -F '| C-06 |' tone-kit/references/core-comment.md | grep -cF '| SHOULD |'` 이 1, `… | grep -cF '| MUST |'` 이 0.
  측정 comment-economy.md: `grep -cF '공식 강제 항목' docs/tone/comment-economy.md` 이 0. 절 자르기 `awk '/^### /{p=($(0) ~ /^### 6\./)} p' docs/tone/comment-economy.md` 에서 `**강도:** SHOULD` 1, `**강도:** MUST` 0, `PREFER` · `public_member_api_docs` · `2026-09-28` 각 1 이상.
  측정 comment-economy.html: `grep -cF '공식 강제 항목' docs/tone-kit/comment-economy.html` 이 0. 블록 자르기 `awk '/<!-- 원칙 6 -->/{p=1} /<!-- 원칙 7 -->/{p=0} p' docs/tone-kit/comment-economy.html` 에서 `s-must` 0, `s-should">SHOULD` 1 이상, `public_member_api_docs` 1 이상.
  측정 templates: `grep -cF 'C-06 `MUST`' docs/tone/templates.md` 0 · `grep -cF 'C-06 `SHOULD`' docs/tone/templates.md` 1 이상. `grep -cF 'C-06 <span class="strength s-must">MUST' docs/tone-kit/templates.html` 0 · `grep -cF 'C-06 <span class="strength s-should">SHOULD' docs/tone-kit/templates.html` 2.
  양성 대조: BASE 에서 core-comment `| MUST |` 1, `공식 강제 항목` md · html 각 1, 절의 `**강도:** MUST` 1, 블록 `s-must` 1, templates.md `C-06 `MUST`` 1, templates.html `s-must` 형 2.
  측정 대상: `tone-kit/references/core-comment.md` · `docs/tone/comment-economy.md` · `docs/tone-kit/comment-economy.html` · `docs/tone/templates.md` · `docs/tone-kit/templates.html`
- [ ] SK-12: (A11) etc_seq=663 자료의 이름표가 원문 제목으로 바뀌었다 — 레포(`.harness` 제외) 전체에서 `국립국어원 공공언어 자료` 가 0 번 나오고, 여덟 파일 `tone-kit/references/sources.md` · `tone-kit/references/locale-korean.md` · `docs/tone/korean-technical-writing.md` · `docs/tone/overview.md` · `docs/tone-kit/korean-technical-writing.html` · `docs/tone-kit/locale-korean.html` · `docs/tone-kit/overview.html` · `docs/tone-kit/sources.html` 은 `보도자료 작성 길잡이` 줄을 BASE 의 옛 이름표 줄 수 이상 담는다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: `git grep -c -F '국립국어원 공공언어 자료' -- ':!.harness' | grep -c .` 이 0 (git grep 은 매치가 없으면 종료 코드 1 이라 뒤의 `grep -c .` 로 센다).
  `grep -cF '보도자료 작성 길잡이' <파일>` 기대 하한: `tone-kit/references/sources.md` 1 · `tone-kit/references/locale-korean.md` 1 · `docs/tone/korean-technical-writing.md` 4 · `docs/tone/overview.md` 1 · `docs/tone-kit/korean-technical-writing.html` 4 · `docs/tone-kit/locale-korean.html` 1 · `docs/tone-kit/overview.html` 1 · `docs/tone-kit/sources.html` 1.
  양성 대조: BASE 에서 첫 측정은 8 (여덟 파일), 여덟 파일의 `보도자료 작성 길잡이` 는 모두 0.
- [ ] SK-13: (A11) tone 예시의 밑줄 두 개 매개변수가 와일드카드 `_` 로 바뀌었다 — 네 파일 `docs/tone/overview.md` · `docs/tone/dart-flutter-idioms.md` · `docs/tone-kit/overview.html` · `docs/tone-kit/dart-flutter-idioms.html` 에서 `, __)` 가 0 줄이고, overview 두 파일은 `(_, _)`, dart-flutter-idioms 두 파일은 `(_, value, _)` 를 1 번 이상 담는다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: 네 파일 각각 `grep -cE ', __\)' <파일>` 이 0. `grep -cF '(_, _)' docs/tone/overview.md` · `grep -cF '(_, _)' docs/tone-kit/overview.html` 각 1 이상. `grep -cF '(_, value, _)' docs/tone/dart-flutter-idioms.md` · `grep -cF '(_, value, _)' docs/tone-kit/dart-flutter-idioms.html` 각 1 이상.
  양성 대조: BASE 에서 `, __)` 네 파일 각 1.
  측정 대상: `docs/tone/overview.md` · `docs/tone/dart-flutter-idioms.md` · `docs/tone-kit/overview.html` · `docs/tone-kit/dart-flutter-idioms.html`
- [ ] SK-14: (A12) `onboarding-kit/skills/setup-guide/evals/evals.json` 의 두 평가 사례 출처가 2026-09-28 대조 결과로 바뀌었다 — 옛 조회 표기 0, 새 조회 표기 2, FCM Apple 주소가 새 주소로, 원문 상태 값이 `documented` · `not_mentioned` 로 바뀌고, 파일이 JSON 으로 읽히며 평가 두 단계가 통과한다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: `e=onboarding-kit/skills/setup-guide/evals/evals.json`. `grep -cF '2026-07-27 조회 · Last updated 2026-07-20 UTC' $e` 0 · `grep -cF '2026-09-28 조회 · Last updated 2026-09-24 UTC' $e` 2 · `grep -cF 'cloud-messaging/ios/client' $e` 0 · `grep -cF 'https://firebase.google.com/docs/cloud-messaging/ios/get-started' $e` 1 · `grep -cF '"apns_auth_key_p8": "documented"' $e` 1 · `grep -cF '"apns_certificate_p12": "not_mentioned"' $e` 1 · `grep -cF '언급하지 않는다' $e` 1 이상.
  `python3 -c "import json,sys; json.load(open(sys.argv[1]))" $e` 종료 코드 0. `sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh` 종료 코드 0. `python3 scripts/sync-evals.py --check-only` 종료 코드 0.
  양성 대조: BASE 에서 옛 조회 표기 2, 새 표기 0, `ios/client` 1.
  음성 대조: evals.json 끝의 `}` 하나를 지운 임시 사본에 같은 JSON 명령을 돌리면 종료 코드 1 이다 (구현 뒤 사본으로 확인).
- [ ] SK-15: (A12) 예시 가이드의 서비스 계정 JSON 항목에 원문 출처가 붙었다 — `docs/onboarding-kit/examples/fcm-ios-setup-guide.md` 와 대응 페이지 `docs/onboarding-kit/fcm-ios-example.html` 에서 `앱 번들` 을 담은 줄이 각각 정확히 1 개이고, 그 줄이 키 관리 권장 주소 · Admin SDK 설정 주소 · `ADC` · `2026-09-28` 을 담는다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: 두 파일 각각 `grep -cF '앱 번들' <파일>` 이 1. `grep -F '앱 번들' <파일> | grep -cF '<낱말>'` 이 `https://docs.cloud.google.com/iam/docs/best-practices-for-managing-service-account-keys` · `https://firebase.google.com/docs/admin/setup` · `ADC` · `2026-09-28` 각 1.
  양성 대조: BASE 에서 `앱 번들` 줄은 두 파일 각 1 이고 네 낱말은 모두 0.
  측정 대상: `docs/onboarding-kit/examples/fcm-ios-setup-guide.md` · `docs/onboarding-kit/fcm-ios-example.html`
- [ ] SK-16: (A13) 서브에이전트 설계 가이드와 대응 페이지가 중첩 깊이를 기본값으로 바로 적었다 — `harness/docs/guides/agent-design-guide.md` · `docs/harness/agent-design-guide.html` 두 파일에서 `하드 리밋` 0 줄, 「상한에 걸리면 Agent 도구가 실패한다」 0 줄, `기본값` 1 줄 이상, `2026-09-28` 1 줄 이상이고, 원본의 frontmatter 출처 줄과 중첩 출처 줄이 `2026-09-28` 을 담는다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: 두 파일 각각 `grep -cF '하드 리밋' <파일>` 0 · `grep -cF '기본값' <파일>` 1 이상 · `grep -cF '2026-09-28' <파일>` 1 이상. `grep -cF '상한에 걸리면 `Agent` 도구가 실패한다' harness/docs/guides/agent-design-guide.md` 0 · `grep -cF '상한에 걸리면 <code>Agent</code> 도구가 실패한다' docs/harness/agent-design-guide.html` 0.
  출처 줄: `grep -F '> **출처:** [Create custom subagents' harness/docs/guides/agent-design-guide.md | grep -F 'frontmatter' | grep -cF '2026-09-28'` 1 · `grep -F '> **출처:** [Create custom subagents' harness/docs/guides/agent-design-guide.md | grep -F 'spawn their own' | grep -cF '2026-09-28'` 1.
  양성 대조: BASE 에서 `하드 리밋` 2 줄 · 6 줄, 실패 문장 1 · 1, `기본값` 0 · 0, `2026-09-28` 0 · 0.
  측정 대상: `harness/docs/guides/agent-design-guide.md` · `docs/harness/agent-design-guide.html`

## Script

- [ ] SC-01: 로컬 CI 와 CI 파일에만 있는 여섯 단계가 모두 통과한다 [exact, enumerated]
  Given: 모든 커밋 뒤, `TMPDIR` 을 세션 scratch 아래 새 폴더로 두고.
  측정: `TMPDIR=<scratch 폴더> bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-ex` 뒤 `<scratch 폴더>/ci-local/summary.txt` 에서 `grep -c 'rc=0'` 이 25, `grep -v 'rc=0'` 출력이 `feedback-agg-test SKIP (yq 없음)` 한 줄뿐.
  이어서 여섯 명령 각각 종료 코드 0: `python3 scripts/check-api-kit-docs.py` · `python3 scripts/detect-docs-drift.py --check-table` · `python3 scripts/check-cause-table-copies.py` · `bash harness/evals/measure/measure-helpers-test.sh` · `bash bambu-kit/evals/run-gate-fixtures.sh` · `bash bambu-kit/evals/makerworld-fetch-test.sh`.
  음성 대조: 이 조건의 판정 근거는 각 단계의 종료 코드다. SK-14 의 JSON 사본처럼 단계가 읽는 입력을 깨면 해당 단계가 rc≠0 을 낸다 — 구현자가 따로 증명할 필요는 없고, BASE 25 단계 rc=0 은 회귀 게이트 절에 적었다.

## Error

- [ ] ER-01: 이번 스프린트가 더한 줄의 주소는 모두 BASE 레포에 이미 있거나 ex 파일(A5~A13)에 인용된 것이다 — 인용 없는 새 출처가 0 개다 [exact, enumerated]
  Given: 모든 커밋 뒤. `TIP=$(git rev-parse chore/ak3-ex)`, `X=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/.harness/.meta/after-kaizen-0928/ex`.
  측정: 바로 아래 들여쓴 다섯 줄을 들여쓰기를 뺀 채 `newurls.sh` 로 저장하고 `bash newurls.sh "$PWD" e78ea2f "$TIP" "$X" | grep -c .` 이 0 이며 종료 코드 0.
    #!/bin/bash
    R="${1}"; B="${2}"; T="${3}"; X="${4}"
    url() { grep -oE 'https?://[^][ <>"`)(|]+' | sed -E "s/(&[a-z]+;)+\$//; s/[.,;:'」》]+\$//" | sort -u; }
    known=$( { git -C "$R" grep -h -I -E 'https?://' "$B" -- . | url; cat "$X"/A*.md | url; } | sort -u)
    git -C "$R" diff -U0 "$B" "$T" -- . ':(exclude).harness' | grep -E '^\+[^+]' | url | comm -23 - <(printf '%s\n' "$known")
  알려진 답: 새 임시 저장소에 기준 판(`https://a.example.com/x.`)과 끝 판(그 주소 · ex 사본의 `https://ex.example.com/y` · 새 `https://z.example.com/new` · `.harness/` 아래 `https://h.example.com/`)을 두면 출력은 `https://z.example.com/new` 한 줄, 종료 코드 0 (2026-09-28 실측 일치).
  음성 대조: 구현 뒤 문서 한 곳에 `https://z.example.com/new` 를 더한 임시 커밋에 돌리면 1 이 나온다.

## Architecture

- [ ] AR-01: BASE 뒤 가지 `chore/ak3-ex` 의 모든 커밋이 맨 위 폴더 하나만 건드리고, 메시지 마지막 줄이 서명 줄이다 [exact, enumerated]
  Given: 모든 커밋 뒤. `TIP=$(git rev-parse chore/ak3-ex)`.
  측정: `for c in $(git rev-list e78ea2f..$TIP); do n=$(git show --name-only --format='' $c | cut -d/ -f1 | sort -u | grep -c .); s=$(git log -1 --format=%B $c | sed '/^[[:space:]]*$/d' | tail -1); [ "$n" = 1 ] && [ "$s" = 'Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>' ] || echo "BAD $c n=$n"; done | grep -c BAD` 이 0. `git rev-list e78ea2f..$TIP | grep -c .` 이 1 이상.
  양성 대조: 같은 폴더 세기를 `a5152c5` 에 돌리면 17 이다 (2026-09-28 실측).
- [ ] AR-02: BASE 에서 TIP 까지 바뀐 경로(`.harness/` 제외)가 전부 `## 범위 경계` 의 `# sprint-scope` 블록 안에 있다 [exact, enumerated]
  Given: 모든 커밋 뒤. `TIP=$(git rev-parse chore/ak3-ex)`, `CF=.harness/sprint-contract-after-0928-external-facts.md`.
  측정: `comm -23 <(git diff --name-only e78ea2f $TIP -- . ':(exclude).harness' | sort -u) <(awk '/^# sprint-scope$/{p=1;next} p&&/^```/{p=0} p' $CF | sort -u) | grep -c .` 이 0. 비교 기준은 병합 커밋이 아니라 두 판의 직접 차이다 (`e78ea2f` 는 TIP 의 조상).
  양성 대조: 같은 `comm` 을 `git diff --name-only a5152c5~1 a5152c5` 에 돌리면 1 이상이 나온다.
- [ ] AR-03: 바꾼 문서 페이지 14 개가 공통 CSS 링크를 하나씩 가지고 접근성 · 넘침 검사를 통과한다 — `docs/infra-kit/infra-test.html` · `docs/infra-kit/cicd.html` · `docs/infra-kit/research-log.html` · `docs/backend-kit/database.html` · `docs/planning-kit/flows.html` · `docs/tone-kit/comment-economy.html` · `docs/tone-kit/templates.html` · `docs/tone-kit/korean-technical-writing.html` · `docs/tone-kit/locale-korean.html` · `docs/tone-kit/overview.html` · `docs/tone-kit/sources.html` · `docs/tone-kit/dart-flutter-idioms.html` · `docs/onboarding-kit/fcm-ios-example.html` · `docs/harness/agent-design-guide.html` [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: 14 파일 각각 `grep -c 'href="../assets/site.css"' <파일>` 이 1. `node scripts/check-docs-a11y.js <14 파일>` 이 종료 코드 0 이고 마지막 줄이 `14/14 PASS` (320 · 375 · 768 · 1280px 넘침 `> 2px` 이면 FAIL).
  양성 대조: 너비 2000px 요소를 넣은 사본은 `FAIL … of=1680/1625/1232/720`, 종료 코드 1 (2026-09-28 실측).
  측정 대상: `docs/infra-kit/infra-test.html` · `docs/infra-kit/cicd.html` · `docs/infra-kit/research-log.html` · `docs/backend-kit/database.html` · `docs/planning-kit/flows.html` · `docs/tone-kit/comment-economy.html` · `docs/tone-kit/templates.html` · `docs/tone-kit/korean-technical-writing.html` · `docs/tone-kit/locale-korean.html` · `docs/tone-kit/overview.html` · `docs/tone-kit/sources.html` · `docs/tone-kit/dart-flutter-idioms.html` · `docs/onboarding-kit/fcm-ios-example.html` · `docs/harness/agent-design-guide.html`

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가
  측정: `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0.
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL
  측정: `python3 scripts/validate-plugin.py --check=frontmatter` 종료 코드 0.

## Reusability

- [ ] RE-01: N/A (산출물이 문서 · 평가 데이터뿐 — 재사용 단위 코드가 없다. 측정: 범위 목록 38 경로의 확장자가 `.md` · `.html` · `.json` 뿐)
- [ ] RE-02: N/A (새 컴포넌트 · 함수를 만들지 않는다 — 기존 문장을 고칠 뿐이다. 측정: RE-01 과 같음)

## Diagnostics

- [ ] DG-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `git diff --name-only e78ea2f $(git rev-parse chore/ak3-ex) | grep -c '^scripts/release.sh$'` 이 0)
- [ ] DG-02: 바꾼 md 23 파일이 편집기와 같은 설정의 markdownlint 경고 0 개다 — 설정은 markdownlint-cli2 0.23.2 · `{ "config": { "MD013": false } }`
  Given: 모든 커밋 뒤. 도구가 없으면 scratch 새 폴더에서 `npm install --no-save markdownlint-cli2@0.23.2` 로 설치한다.
  측정: 범위 목록에서 `.md` 로 끝나는 23 경로마다 `markdownlint-cli2 --config <설정 파일> <경로>` 출력에서 `^<경로>:[0-9]+` 줄 수가 0 이고 종료 코드 0.
  양성 대조: 회귀 게이트 절 — 나쁜 줄을 붙인 사본은 4, 종료 코드 1.
- [ ] DG-03: N/A (commands.test 는 scripts/release.sh 를 돌린다 — 이번 변경과 무관. 실제 시험은 SC-01 이 잰다)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 변경 파일이 문서 · 평가 데이터뿐. 페이지 실제 렌더는 AR-03 이 잰다)
