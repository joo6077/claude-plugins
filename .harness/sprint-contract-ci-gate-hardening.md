---
feature: "CI 게이트 강화 — docs 오버플로 66건 근절 + 재생성 회귀 차단 + 액션 v7 + release PR 전환 + branch protection"
created: "2026-07-28 17:30"
complexity: "복잡"
conditions: 25
slug: ci-gate-hardening
status: done
owner_session: 8a9c2ebc-8d41-48fb-9586-496555a22b30
---

## 배경

PR #16 이 main 을 처음으로 green 으로 만들었다. 그러나 머지 전 독립 5 축 검증에서
**그 green 이 유지될 구조가 없다**는 것이 실측으로 드러났다.

1. **강제되지 않는다** — `branches/main/protection` 404, `rulesets` `[]`.
   main 계보 317 커밋 중 303(95.6%)이 직접 푸시이고, Playwright 잡은 51 런 중 44 회 failure ·
   green 2 회뿐이다. 강제 장치가 없어 32 회 red 인 채로 릴리스가 계속 나갔다.
2. **되돌아간다** — `docs/design-kit/*.html` 은 `.claude/skills/docs-site/` 생성물이고,
   카이젠 Step 11.5 재생성은 "건너뛰기 금지" 필수 단계다. 템플릿(`page-template.html` 94 줄)에
   PR #16 이 넣은 4 개 규칙이 **하나도 없다**.
3. **회귀 메커니즘이 특정됐다** — `scripts/detect-docs-drift.py` 의 design-kit 매핑이
   **26/26 전부 존재하지 않는 경로**를 가리킨다 (subdir 보존 vs 실제 flat 출력).
   그래서 design-kit 소스를 고칠 때마다 26 건이 `[NEW — 신규 생성 필요]` 로 오보되고,
   재생성 에이전트가 템플릿에서 새로 만들며 PR #16 수정을 날린다.
4. **결함은 레포 전역이다** — PR #16 은 design-kit 4 페이지만 고쳤으나, 375px 오버플로는
   146 페이지 중 **66 건**이다.

## 리서치 소스 (전부 1 차 실측 — 학습 데이터 사용 안 함)

- 오버플로 66 건 전수 스윕 (Playwright 1.58.2, 375×812, `scrollWidth - clientWidth > 2`)
- 액션 최신 버전: `gh api repos/actions/<x>/releases/latest` + `action.yml` input diff
- protection 설계: `gh api` GET 전수 (check-runs / commits status / PR 이력 / 권한)
- Node 20 deprecation 공지: <https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/>

## GAP 분석 (전부 실측)

### 오버플로 66 건의 원인 군집 — 페이지별 개별 진단이 아니라 규칙으로 수렴한다

| 군집 | 건수 | 원인 | 규칙 |
|---|---|---|---|
| G1 | 22 | `DIV`/`ARTICLE` in `display:grid` | grid item 기본 `min-width:auto`(= min-content) → `min-width:0` |
| G2 | 19 | 래퍼 없는 `TABLE` in block | 고정 컬럼 폭이 그대로 전파 → 스크롤 컨테이너 |
| G3 | 15 | `CODE`/`SPAN` `white-space:pre` | 내용폭 전파 → 컨테이너 `overflow-x:auto` |
| G4 | 4 | `CODE` in `display:flex` | flex item 기본 `min-width:auto` → `min-width:0` |
| G5 | 6 | `HTML` 자체 최광 / `nowrap` / 기타 | 개별 진단 |

킷별: rust-kit 14 · harness 11 · react-kit 10 · design-kit 9 · flutter-toolkit 7 ·
backend-kit 5 · bambu-kit 4 · infra-kit 4 · onboarding-kit 1 · process 1.
최악: `flutter-toolkit/project-detection.html` 915px, `react-kit/ui-patterns.html` 512px,
`harness/qa-evaluation-guide.html` 503px.

### 액션 버전 — 4 개 전부 node20, 최신 메이저는 v7

| 액션 | 현재 | 런타임 | 목표 | breaking 영향 |
|---|---|---|---|---|
| `actions/checkout` | v4 | node20 | **v7** (v7.0.1) | input 21 개 v4↔v7 완전 동일. fork 차단은 `pull_request_target`/`workflow_run` 전용이고 이 워크플로는 `push`+`pull_request` |
| `actions/setup-python` | v5 | node20 | **v7** (v7.0.0) | 제거 input 0, `pip-version` 추가만. `cache:"pip"` 유지 |
| `actions/setup-node` | v4 | node20 | **v7** (v7.0.0) | 제거는 `always-auth` 하나(미사용). `packageManager` 자동캐싱은 해당 필드 부재로 미발동 |
| `actions/upload-artifact` | v4 | node20 | **v7** (v7.0.1) | 제거 input 0, `archive`(default true) 추가만. 불변성은 v4 부터의 성질로 신규 변경 아님 |

정정 2 건: (a) 경고가 checkout·setup-node 만 지목한다는 전제는 틀렸다 — Plugin Validation 잡은
`setup-python@v5` 를 지목한다. (b) `upload-artifact@v4` 도 node20 이며, 경고에 없는 건
`if: failure()` 로 skip 됐기 때문이다. 부분 업그레이드는 금물 — node20 해소 최소선이 액션마다
다르고 `upload-artifact@v5` 는 기본이 여전히 node20 이다.

### branch protection — 최대 리스크는 context 오타

main 의 check-run 은 **6 개**인데 PR head 는 **3 개**다. 차이 3 개(`build`, `deploy`,
`report-build-status`)는 GitHub 관리형 `pages-build-deployment` 소속으로 **PR 에 절대 안 뜬다.**
하나라도 required 에 넣으면 영구 pending → 머지 완전 차단. legacy commit status 는 0 건이라
오타 시 `/status` 가 `total_count: 0` 을 조용히 반환한다.

정확한 context 3 개: `Plugin Validation` · `Playwright Visual Tests` · `Harness Integration Tests`
(`app_id: 15368`). 머지 PR 15/15 가 셀프 머지이므로 `required_pull_request_reviews` 는 **null**
(켜면 자기 PR 을 머지할 수 없다). 기존 PR 13 건이 전부 merge commit 이므로
`required_linear_history` 는 **false**.

`enforce_admins: true` 를 택했으므로 `scripts/release.sh:110` 의
`git push origin HEAD --follow-tags` 가 **거부된다** — release 를 PR 경유로 전환하는 작업이
같은 스프린트에 반드시 들어간다.

## 실행 순서 (역순 금지 — 자물쇠 사고 방지)

```text
A 재발 방지(소스 인코딩) → B 66 건 해소 → C 액션 v7 → D release PR 전환
  → PR 생성·머지 → E protection 적용(마지막)
```

**E 를 D 머지보다 먼저 하면 release.sh 가 즉시 깨지고, 자신의 수정을 push 할 수 없게 된다.**

## 범위 경계

- **비대상**: `design-kit/evals/visuals.spec.js` (PR #16 SC-01 정신 유지 — 기준 완화 금지),
  `.harness/history/**` (이력 기록물, 수정 금지), 터치타겟 부채 249/332 건,
  테마 키 파편화(`dk-theme` 12 / `theme` 3 / `vs-theme` 2 / `cp-theme` 2) 통일,
  dependabot 도입, 액션 SHA 핀닝, `allow_auto_merge`.
- 위 비대상은 전부 실측으로 확인된 실재 부채이며 후속 스프린트 후보로 audit-log 에 남긴다.

## 회귀 게이트

`python3 scripts/validate-plugin.py` = 11 plugins / 11 OK / Exit 0,
`bash -n scripts/release.sh` Exit 0,
`playwright test design-kit/evals/visuals.spec.js --project=chromium` = **0 failed**,
CI 3 잡 전부 pass.

## Architecture

- [x] AR-01: 375px 뷰포트에서 문서 오버플로가 **2px 이하**인 페이지가 146 개 중 **146 개**다. 측정: `docs/**/*.html` 전수를 375×812 에서 `document.documentElement.scrollWidth - clientWidth` 로 측정하여 `> 2` 인 페이지 수가 **0** (현재 66). 기준을 완화하거나 대상을 표본으로 줄이지 않는다. [exact, collective]
- [x] AR-02: 오버플로 해소가 **내용을 잘라내는 방식이 아니다.** 측정: 추가된 CSS 에 `overflow:hidden`/`overflow-x:hidden`/`display:none` 을 오버플로 억제 목적으로 쓴 건수 **0**. 코드블록·표는 `overflow-x:auto` 로 **끝까지 스크롤 도달 가능**해야 한다 (대표 3 페이지에서 `scrollLeft` 를 최대로 밀어 `scrollLeft + clientWidth >= scrollWidth - 1` 확인). [exact, enumerated]
- [x] AR-03: 768px 뷰포트 오버플로도 악화되지 않는다. 측정: 768×1024 에서 `> 2` 인 페이지 수가 작업 전(26 건) **이하**. [exact]
- [x] AR-04: 4 개 규칙이 `.claude/skills/docs-site/references/page-template.html` 에 존재한다: (a) grid/flex 자식 `min-width:0` (b) 인터랙티브 요소 최소 높이 (c) 좁은 뷰포트 단일 컬럼 스택 (d) 테마 토글 + `localStorage` 영속화 + 로드 시 복원. 측정: 각 규칙에 대응하는 셀렉터/코드가 파일에 존재 (현재 4 개 전부 0 매치). 테마 키는 레포 지배 패턴 `dk-theme` 를 쓰고 `prefers-color-scheme` 폴백을 포함한다. [structural, enumerated]
- [x] AR-05: `design-kit/templates/*.html` 8 개 전부에 grid/flex 자식 `min-width:0` 규칙이 있다. 측정: 8 개 파일 개별 확인 (현재 `component.html` 1 개만 보유). [structural, enumerated]

## Skill

- [x] SK-01: `.claude/skills/docs-site/SKILL.md` 가 페이지별 bespoke CSS 를 작성할 때도 4 개 규칙을 **하드 제약**으로 강제한다. 측정: Gotchas 에 4 개 규칙이 명시되고, 자가검증 단계에 "생성 후 375px 오버플로 ≤ 2px 확인" 이 **실행 가능한 명령과 함께** 포함된다 (E2 — 문장만이 아니라 검증 절차). [structural]
- [x] SK-02: `design-kit/skills/design-audit/references/audit-criteria.md` 에 오버플로·그리드 기준이 추가된다. 측정: `min-width` / 가로 오버플로 관련 기준 항목이 존재하고 근거 출처가 병기된다 (현재 `min-width` 0 매치 · `overflow` 0 매치). 기존 터치타겟 기준(WCAG 2.2 SC 2.5.8 AA 24px / SC 2.5.5 AAA 44px)의 **수치를 낮추지 않는다**. [structural]
- [x] SK-03: `.claude/commands/release.md` 가 `scripts/release.sh` 의 새 PR 경유 동작과 일치한다. 측정: 문서에 `git push origin HEAD --follow-tags` 직접 푸시 서술이 남아 있지 않고, PR 경유 절차가 기술된다. [exact]

## Script

- [x] SC-01: `scripts/detect-docs-drift.py` 의 design-kit 매핑이 실제 출력 경로를 가리킨다. 측정: 26 개 design-kit 소스를 전수 매핑하여 **존재하지 않는 경로가 0 건** (현재 26/26 MISS). [exact, enumerated]
- [x] SC-02: `detect-docs-drift.py` 의 `SOURCE_TO_HTML` 이 오케스트레이터가 매핑한다고 명시한 prefix 를 누락하지 않는다. 측정: `rust-kit/references/`, `react-kit/references/`, `planning-kit/references/`, `docs/planning/` 4 개 prefix 가 등록되고, 현재 미커버 20 개 `.md` 가 0 건이 된다. [exact, enumerated]
- [x] SC-03: `.github/workflows/ci.yml` 의 액션 6 건이 전부 `@v7` 이다. 측정: `grep -c 'actions/[a-z-]*@v7'` = 6 이고 `@v4`/`@v5` 잔여 0. `with:` 블록은 한 줄도 변경하지 않는다 (전 input 이 v7 에서 유효). [exact, enumerated]
- [x] SC-04: 배포되는 템플릿의 액션 버전도 갱신된다. 측정: `docs/rust/ops/ci-cd.md` 4 건 + `infra-kit/skills/infra-init/SKILL.md` 1 건 = 5 건이 최신 메이저를 가리킨다. **`.harness/history/` 의 1 건은 이력 기록물이므로 수정하지 않는다.** [exact, enumerated]
- [x] SC-05: `scripts/release.sh` 가 main 에 직접 push 하지 않는다. 측정: `git push origin HEAD` 계열 직접 푸시가 0 건이고, 브랜치 생성 → push → PR 생성 경로로 바뀐다. 태그는 branch protection 대상이 아니므로 태그 푸시 동작은 유지한다. [exact]
- [x] SC-06: `release.sh` 가 문법적으로 유효하고 파괴적 동작이 없다. 측정: `bash -n scripts/release.sh` Exit 0, 그리고 **dry-run 또는 임시 브랜치에서 실제 실행**하여 main 에 커밋·푸시가 발생하지 않음을 확인한다 (실행 증거 필수 — 서술 불가). [exact]

## Error

- [x] ER-01: 수정한 페이지의 브라우저 콘솔 에러가 0 건이다. 측정: 이번에 변경한 모든 HTML 을 로드하여 `console` error + `pageerror` 0 건 (변경 페이지 전수). [exact, collective]
- [x] ER-02: protection 적용 실패 시 되돌리는 경로가 문서화된다. 측정: 전체 해제 / 체크만 해제 / admin 강제 해제 3 개 명령이 계약 또는 레포 문서에 기재된다. [structural]

## Anti-patterns

- [x] AP-02: force push 를 사용하지 않는다. 측정: 셸 이력에 `git push --force` / `-f` 0 건. [exact]
- [x] AP-03: bare code fence 0 건. 측정: `validate-plugin.py` V6 가 전 킷에서 `0 bare` 보고. [exact]

## Reusability

- [x] RE-01: 오버플로 수정이 **페이지별 매직넘버 튜닝이 아니라 재사용 가능한 규칙**이다. 측정: 66 건 중 군집 G1(22)·G2(19)·G3(15)·G4(4) = 60 건이 **동일 규칙 패턴**으로 해소되고, 페이지별 고유 하드코딩 폭(`width: 340px` 류)을 새로 도입한 건수 0. G5(6 건)만 개별 진단을 허용한다. [structural, collective]
- [x] RE-02: 이미 존재하는 패턴을 재발명하지 않는다. 측정: 테마 토글은 `design-kit/templates/base.html` 의 기존 구현(`dk-theme` + `prefers-color-scheme` 폴백)을 따르고, 표 스크롤 래퍼는 레포에 이미 있는 패턴이 있으면 그것을 쓴다. [structural]

## Diagnostics

- [x] DG-01: 레포 게이트 통과. 측정: `python3 scripts/validate-plugin.py` = `11 plugins, 11 OK` + Exit 0, `bash -n scripts/release.sh` Exit 0. [exact]
- [x] DG-02: Playwright 스위트 0 failed. 측정: `playwright test design-kit/evals/visuals.spec.js --project=chromium` 의 failed 카운트 0. [exact]
- [x] DG-03: main branch protection 이 정확한 3 개 context 로 적용된다. 측정: `gh api .../branches/main/protection` 조회 결과 `checks` 가 정확히 `Plugin Validation`, `Playwright Visual Tests`, `Harness Integration Tests` 3 개이고 오타·잉여(`build`/`deploy`/`report-build-status`) 0 건, `enforce_admins.enabled = true`, `required_pull_request_reviews = null`, `required_linear_history.enabled = false`, `allow_force_pushes.enabled = false`. [exact, enumerated]
- [x] DG-04: protection 적용 **후** 실제로 PR 이 머지 가능한 상태가 된다. 측정: protection 적용 뒤 `gh pr view <PR> --json mergeStateStatus` 가 `BLOCKED` 로 영구 고착되지 않음을 확인한다 (context 오타 시 발생하는 증상). 확인 불가하면 즉시 되돌린다. [exact]
- [x] DG-05: CI 3 잡이 전부 pass 한다. 측정: PR 의 `gh pr checks` 3/3 pass 이고, Playwright 잡 로그에 `Running 143 tests` → `143 passed` 가 실제로 찍힌다 (수집 0 후 green 배제). [exact]
