---
feature: "카이젠 Phase 6 — design-kit Variant Distinctiveness Gate(E1) + Decision Propagation Manifest(E2) + 증거 채널 구분(E3) + WCAG 터치타겟 사실 정정"
created: "2026-08-13 16:05"
complexity: "복잡"
conditions: 25
slug: kaizen-phase6-variant-decision-gates
status: active
owner_session: df1b3e15-30b3-4825-a3c4-4ac44c686e94
conditions_digest: sha256:a2dc871865f09e39
locked_at: "2026-08-13 16:05"
---

## 배경

`.harness/.meta/evidence/phase6.md` 가 이번 Phase 의 **유일한 외부 근거**다. 외부 조회 0 회.

Phase 6 은 이번 사이클 `/insights` §0 **신규 델타의 주 무대**다 (D2 탐색 축 미고정 · D3 사용자 보고
반박 · Horizon #1 decisions manifest). 직전 사이클(2026-07-27)이 만든 `visual-change-protocol.md`
는 **확정된 결정을 어떻게 지키는가**를 다뤘다. 이번 신호는 그 앞뒤 두 구간이다 — 확정 **이전**의
탐색이 발산하는 문제와, 확정 **이후**의 전파가 일부 표면에서 누락되는 문제.

**E1 — 축 선언만으로는 부족하다 (실측).** 글로벌 REJECT `UI-04` (2026-08-12, fit-pal):
*"B3(단일 컬럼)과 B6(조밀 로그)이 계약 지정 4축(버블 컨테이너 유무/정렬 컬럼 수/메타 위치/묶음
단위) 전부에서 동일값 — 구조 구별 요구 위반."* 계약이 축을 **이미 명시**했는데도 구현이 무시했다.
따라서 이번 처리는 문장 추가가 아니라 **기계 판정 가능한 pairwise 오라클**이다.

**E2 — 골든만으로는 "보인다" 를 증명하지 못한다.** evidence E3 은 Playwright 공식 문서를 근거로
스냅샷 존재가 사용자 관측이 아님을 지적한다. 따라서 manifest 의 coverage rule 핵심은
**골든만 있고 visible/count/height assertion 이 없으면 FAIL** 이다.

**E3 — 증거 채널.** `artifact_snapshot` 만으로 "사용자가 보는 화면 정상" 이라고 말할 수 없다.
사용자 관측과 충돌할 때의 규약은 이번 사이클 Phase 1 이 `skill-design-guide` §3.8 에, Phase 1/3 이
`agent-design-guide` §10 에 이미 착지시켰다. **여기서 재정의하지 않는다 — 채널 어휘만 더하고
정본을 경로로 참조한다.**

**중복 승격 금지 확인.** `.claude/kaizen-input/insights-report.md` 의 "직전 사이클 흡수분" 7 행
(진단 전 편집 · 검증 없이 done · 일부 표면 적용 · 서버-클라 누락 · 의도 외 영역 변경 · 스테일
핸드오프 · MCP 스냅샷 오용) 은 이 계약의 대상이 아니다. `visual-change-protocol.md` §1~§4 는
**손대지 않는다** (§2 부분 변경 격리, §3 증거 유효성 4 검사, §4 승인 기록은 직전 사이클 산출물).

## 리서치 소스 (evidence 파일 한정 — 외부 조회 0 회)

- `.harness/.meta/evidence/phase6.md` §1~§4 — E1/E2/E3 관찰 사실 · 권장 조항 · `decisions.yaml`
  스키마 초안 · **넣지 말 것** 5 항목 · 트레이드오프 · 열린 질문 5 종. 인용 URL:
  `ifm.eng.cam.ac.uk/.../morphological-charts` · `open.clemson.edu/all_theses/274` ·
  `strathprints.strath.ac.uk/70009` · `playwright.dev/docs/test-snapshots` ·
  `playwright.dev/docs/actionability` · `playwright.dev/docs/test-assertions` ·
  `chromatic.com/docs/visual` · `percy.io/how-it-works` · `github.com/garris/BackstopJS` ·
  `w3.org/TR/act-rules-format` · `tailwindcss.com/blog/tailwindcss-v4` ·
  `w3.org/community/reports/design-tokens/CG-FINAL-format-20251028` · `w3.org/TR/WCAG22` ·
  `developer.mozilla.org/.../Container_queries` · `design.google/library/expressive-material-design-google-research`
  · `developer.apple.com/tutorials/data/documentation/technologyoverviews/adopting-liquid-glass.md`
- `.harness/.meta/kaizen-data-pool.md` §1 — 최근 REJECT 사유 Top 20 중 `UI-04` (2026-08-12)
- `.claude/kaizen-input/insights-report.md` — 신규 델타 D2 · D3 · Horizon #1 · 흡수분 표(재승격 금지)
- 이번 사이클 Phase 1 산출물 `harness/docs/guides/skill-design-guide.md` — §2 유형 11 탐색형 생성 ·
  §5.6 Variant Budget (상한 3 · primary axis 1(+1) · 부대 산출물 금지 · Variant Matrix 5 열) ·
  §3.7 등급 원장 · §3.8 User-Reported Failure Gate
- 이번 사이클 Phase 1/3 산출물 `harness/docs/guides/agent-design-guide.md` §10 — 평가자 측 짝 조항
- 이번 사이클 Phase 4 산출물 `harness/evals/gate-exit-codes.md` — exit code 4 값 SSOT
- `harness/references/contract-schema.md` v5.3 — 본 계약의 포맷 SSOT
- `docs/kaizen/changelog.md` `[2026-07-28]` Phase 6 항목 — 직전 사이클이 만든 `visual-change-protocol.md`

## GAP 분석 (전부 실측 · 사전 측정 출력 기준)

| # | 갭 | 실측 근거 (사전 측정) | 처리 |
| --- | --- | --- | --- |
| E1a | 구별성 판정 오라클 부재 | `grep -rcE 'variant_id\|axis_vector\|strategy_label\|Hamming' design-kit/{skills,agents,references}` → **전 파일 0 건** | `visual-change-protocol.md` §5 신설 + 실행 가능한 pairwise 게이트 |
| E1b | design-mockup 개수가 Phase 1 §5.6 과 충돌 | `grep -nF '시안 5개' design-kit/skills/design-mockup/SKILL.md` → 3 건(description 4행 · Gotcha 2 · Step 3 제목). Phase 1 §5.6 은 상한 3 · 4 개 이상 승인 필요이며 유형 11 예시로 design-mockup 을 **명시** | 개수 계약으로 교체 (미지정 3 · 지정 N 정확히 · 승인 상한 5) |
| E1c | design-concept 구별성 규칙이 서술뿐 | Gotcha 6 "최소 2개 이상이 달라야" — 축 목록도 판정식도 없음 | §5 게이트 참조로 교체 |
| E2a | 결정 전파 manifest 어휘 0 건 | `grep -rncE 'decision_id\|decisions\.yaml\|required_surfaces' design-kit/` → **0 건** | §6 신설 (스키마 + coverage rule 4 조 + 실행 가능한 체커) |
| E2b | design-test 시각 회귀가 결정 단위가 아님 | Step 5 는 페이지×뷰포트 순회. 어떤 결정이 어떤 surface 에 반영돼야 하는지 표현 수단 없음 | Step 5-b 신설 (manifest 기반 생성) |
| E2c | 감사 측 커버리지 판정 부재 | `design-audit` · `design-reviewer` 에 `decisions.yaml` 0 건 | 양쪽에 조항 1 개씩 (10 카테고리 구조는 건드리지 않는다) |
| E3a | 증거 채널 구분 0 건 | `grep -rncE 'artifact_snapshot\|dom_snapshot\|browser_user_visible\|device_user_visible' design-kit/` → **0 건** | §7 신설 (4 채널 + PASS 문장 5 요소) |
| E3b | Phase 1 §3.8 과의 연결 없음 | `grep -rncF 'skill-design-guide.md' design-kit/` → **0 건** | §7 에서 경로+절 번호로 참조 (재서술 금지) |
| F1 | WCAG 터치타겟 레벨 미표기 | 아래 AR-01 오라클 사전값 **6 줄** (`design-guide/SKILL.md:15` · `visual-hierarchy.md:267` · `apple-hig.md:67` · `navigation.md:221` · `navigation.md:267` · `accessibility.md:95`) | 전 줄에 레벨·출처 귀속 부여 |

**넣지 않는 것 (evidence §2 경계 준수)** — Playwright/Chromatic/Percy/BackstopJS 중 하나를
design-kit 표준으로 강제하지 않는다. OKLCH · M3 Expressive · Liquid Glass 를 기존 승인값보다 상위
규칙으로 두지 않는다. 모든 화면/상태에 골든을 무차별 생성하지 않는다. perceptual diff 만으로 시안
구별을 판정하지 않는다. 44px 를 WCAG AA 기준으로 쓰지 않는다. evidence §4 열린 질문 5 종(기본 시안
수 3 vs 5 · Hamming 전역 기본 · manifest 경로 고정 · 골든 커밋 위치 · surface registry 자동 생성)
중 **경로 고정 · 골든 위치 · registry 자동화 3 종은 근거 부족으로 이번 사이클 미반영**이며 문서에
열린 질문으로 남긴다.

## 범위 경계

수정 허용: `design-kit/skills/*/SKILL.md` · `design-kit/agents/*.md` · `design-kit/references/` ·
`design-kit/docs/design/` · 본 계약 파일.

수정 금지 (읽기만):

- `design-kit/README.md` — description 1 줄 변경으로 동기화가 필요해지나 **Final 소관**이다.
  DG-04 가 그 드리프트를 측정해 신고한다 (숨기지 않는다).
- `design-kit/skills/*/references/**` · `design-kit/templates/**` · `design-kit/evals/**` —
  스킬 로컬 참조/템플릿/평가 픽스처. `design-kit/skills/design-mockup/references/mockup-guidelines.md:67`
  에 레벨 미표기 44 가 **1 건 잔존**하고 `design-kit/evals/visuals.spec.js` 13 곳이 44 를 모바일
  기준으로 assert 하나 둘 다 범위 밖이므로 보고만 한다.
- `harness/**` (Phase 1~4 소관) · 다른 킷 전부.

## 회귀 게이트

- `python3 scripts/validate-plugin.py design-kit` 가 8 카테고리 OK 를 유지한다.
- `visual-change-protocol.md` §1~§4 의 기존 문장을 변경하지 않는다 (신설은 §5 이후에만).
- 임계값(`[미검증]` 1/2) · exit 숫자(0/1/2/3) · 개수 상한(3) 을 design-kit 이 **자체 정의하지
  않는다** — `qa-evaluation-guide` · `gate-exit-codes.md` · `skill-design-guide` §5.6 을 인용한다.
- design-audit / design-reviewer 의 **10 카테고리 구조와 `N/10` 커버리지 표기를 바꾸지 않는다.**

## Skill

- [ ] SK-01: `design-kit/references/visual-change-protocol.md` 에 §5 Variant Contract Matrix 가
      신설되고 variant 필수 4 필드가 각각 존재한다 [exact, enumerated]
      (측정: `variant_id`, `strategy_label`, `axis_vector`, `intended_user_scenario`
      4 토큰 각각 `grep -cF` >= 1)
- [ ] SK-02: 같은 §5 가 pairwise 임계를 축 개수로 분기하는 **실행 가능한 판정식**을 싣는다 [exact]
      (측정: `need = 2 if k >= 3 else 1` 문자열 `grep -cF` >= 1)
- [ ] SK-03: §5 가 개수 상한·부대 산출물 금지를 자체 정의하지 않고 정본을 경로로 인용한다 [exact]
      (측정: §5 블록 안에 `harness/docs/guides/skill-design-guide.md` 와 `§5.6` 이 각각
      `grep -cF` >= 1)
- [ ] SK-04: 같은 파일에 §6 Decision Propagation Manifest 가 신설되고 스키마 키 6 종이 존재한다
      [exact, enumerated]
      (측정: `decision_id`, `required_surfaces`, `excluded_surfaces`, `route_or_entry`,
      `viewport_or_container`, `assertions` 6 토큰 각각 `grep -cF` >= 1)
- [ ] SK-05: §6 coverage rule 이 4 조로 명문화되고 그중 "골든만 존재 = FAIL" 이 포함된다 [exact]
      (측정: `golden 만 있고` 문자열 `grep -cF` >= 1 이고 coverage rule 번호 목록 1~4 존재)
- [ ] SK-06: 같은 파일에 §7 Evidence Channels 가 신설되고 채널 4 종이 각각 정의된다
      [exact, enumerated]
      (측정: `artifact_snapshot`, `dom_snapshot`, `browser_user_visible`, `device_user_visible`
      4 토큰 각각 `grep -cF` >= 1)
- [ ] SK-07: §7 이 사용자 보고 규약을 재정의하지 않고 정본 2 곳을 경로+절 번호로 참조한다
      [exact, enumerated]
      (측정: `harness/docs/guides/skill-design-guide.md`, `§3.8`,
      `harness/docs/guides/agent-design-guide.md`, `§10` 4 토큰 각각 `grep -cF` >= 1)
- [ ] SK-08: `design-kit/skills/design-mockup/SKILL.md` 에서 고정 개수 리터럴이 사라지고 개수
      계약이 frontmatter description 과 Step 3 양쪽에 착지한다 [exact]
      (측정: `grep -cF '시안 5개'` == 0 이고, description 첫 줄과 `## Step 3` 블록 각각에
      `미지정` 또는 `상한` 낱말 포함 줄 >= 1)
- [ ] SK-09: 같은 파일이 §5 산출물을 이름으로 요구한다 [exact]
      (측정: `Variant Contract Matrix` `grep -cF` >= 1)
- [ ] SK-10: `design-kit/skills/design-test/SKILL.md` 에 manifest 기반 테스트 생성 단계가
      신설된다 [exact, enumerated]
      (측정: `decisions.yaml` `grep -cF` >= 1 이고 `^### Step 5-b` `grep -cE` == 1)
- [ ] SK-11: `design-kit/skills/design-audit/SKILL.md` 와 `design-kit/agents/design-reviewer.md`
      양쪽에 커버리지 판정 조항이 착지한다 [exact, enumerated]
      (측정: 두 파일 각각 `decisions.yaml` `grep -cF` >= 1)
- [ ] SK-12: `design-kit/skills/design-concept/SKILL.md` Gotcha 6 이 §5 게이트를 참조한다 [exact]
      (측정: `§5 Variant Contract Matrix` `grep -cF` >= 1)

## Error

- [ ] ER-01: §5 의 구별성 게이트가 실측 REJECT `UI-04` 를 FAIL 로 잡는다 [goal]
      (측정: §5 에 실린 스니펫을 그대로 파일로 추출해 4 축 · B3/B6 전축 동일 입력을 주면
      `hamming=0 < 2` 출력 + exit 1 ·
      음성 대조: 같은 입력에서 B6 의 축 값 2 개를 다르게 바꾸면 `violations=0` + exit 0)
- [ ] ER-02: §6 의 커버리지 게이트가 "골든만 존재" 를 FAIL 로 잡는다 [goal]
      (측정: golden 은 있고 `assertions: []` 인 fixture → `golden 만 존재` 출력 + exit 1 ·
      음성 대조: 같은 fixture 에 visible/count/height assertion 3 종을 채우면 exit 0)
- [ ] ER-03: 같은 게이트가 manifest 부재·결정 0 건을 통과로 접지 않는다 [goal]
      (측정: 없는 경로 → `NO_MANIFEST` + exit 3 · `decisions: []` → `NO_DECISION` + exit 3 ·
      두 경우 모두 exit 0 이 아니다)

## Architecture

- [ ] AR-01: 범위 안 문서에서 레벨 귀속 없이 `44` 를 터치 타겟 기준으로 제시한 줄이 0 건이다
      [exact]
      (측정: `grep -rnE '44' <범위 안 8 SKILL.md + agents + references + docs/design> |
      grep -E '터치|타겟' | grep -vE 'AAA|Apple|HIG|2\.5\.5|iOS|Enhanced|권장'` → 0 줄.
      사전값 6 줄 ·
      음성 대조: 정정한 줄 하나에서 귀속 낱말을 지우면 같은 명령이 1 줄을 낸다)
- [ ] AR-02: 소비 표면 5 파일이 해당 절을 **절 제목 토큰**으로 참조한다 [exact, enumerated]
      (측정: 9 쌍 각각 `grep -cF` >= 1 —
      design-mockup←`§5 Variant Contract Matrix`·`§7 Evidence Channels`,
      design-concept←`§5 Variant Contract Matrix`,
      design-test←`§6 Decision Propagation`·`§7 Evidence Channels`,
      design-audit←`§6 Decision Propagation`·`§7 Evidence Channels`,
      design-reviewer←`§6 Decision Propagation`·`§7 Evidence Channels`)
- [ ] AR-03: §6 이 특정 시각 회귀 도구를 design-kit 표준으로 강제하지 않음을 명시한다 [exact]
      (측정: `표준으로 강제하지 않는다` `grep -cF` >= 1 이고 도구 4 종
      `Playwright`·`Chromatic`·`Percy`·`BackstopJS` 가 같은 문단에 열거)

## Anti-patterns

- [ ] AP-03: 이번 스프린트가 추가·수정한 마크다운에 bare code fence 가 없다
      (측정: `python3 scripts/validate-plugin.py design-kit` V6 `0 bare`)
- [ ] AP-04: 수정한 SKILL.md 와 agents 파일의 frontmatter `name` 필드가 보존된다
      (측정: `python3 scripts/validate-plugin.py design-kit` V1 이 `8 skills + 1 agent — OK`)

## Reusability

- [ ] RE-01: §6 스키마 정의가 design-kit 안에서 1 파일에만 존재하고 소비 표면은 참조만 한다
      [exact, enumerated]
      (측정: `grep -rlF 'required_surfaces:' design-kit/ | wc -l` == 1 이고 그 파일이
      `design-kit/references/visual-change-protocol.md`)

## Diagnostics

- [ ] DG-01: `python3 scripts/validate-plugin.py design-kit` 가 exit 0 · `1 plugins, 1 OK`
- [ ] DG-02: §5 · §6 에 실린 스니펫 2 종이 zsh 와 bash 양쪽에서 동일한 출력·exit code 를 낸다
      (측정: 두 셸에서 ER-01·ER-02 측정 명령을 실행해 출력 `diff` 무출력)
- [ ] DG-03: 커밋에 scope 밖 경로가 0 건이다
      (측정: `git show --name-only --format= HEAD` 결과가 `design-kit/skills/` 의 SKILL.md ·
      `design-kit/agents/` · `design-kit/references/` · `design-kit/docs/design/` ·
      `.harness/sprint-contract-kaizen-phase6-` 접두로만 구성)
- [ ] DG-04: design-mockup description 변경으로 생긴 README 드리프트가 정확히 1 건이며 신고된다
      (측정: `python3 scripts/sync-docs.py design-kit --check-only` 출력에 변경 필요 파일이
      `design-kit/README.md` 1 건 · 사전 상태는 `동기화됨`)
