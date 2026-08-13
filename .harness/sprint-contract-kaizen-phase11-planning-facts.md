---
feature: "카이젠 Phase 11 — planning-kit 사실 정정 3건 (Projects v2 REST 존재 · one-When 과잉 인용 · HBR premortem 절차 미확인)"
created: "2026-08-13 14:55"
complexity: "복잡"
conditions: 15
slug: kaizen-phase11-planning-facts
status: active
owner_session: df1b3e15-30b3-4825-a3c4-4ac44c686e94
conditions_digest: sha256:700f616435f0075f
locked_at: "2026-08-13 14:55"
---

## 배경

`.harness/.meta/evidence/phase11.md` 가 이번 Phase 의 **유일한 외부 근거**다. 외부 조회 0 회.

Phase 11 은 low-signal Phase 다. `/insights` 2026-08-13 은 "Phase 11 Planning — 이번 리포트에
직접 신호 없음" 이라고 명시하고 (`insights-report.md:110`), 데이터풀 §1 의 REJECT Top 20 ·
Improvement Top 15 에도 planning 귀속 항목이 0 건이다 (`grep -n 'planning' kaizen-data-pool.md`
→ 2 행, 둘 다 self-audit 표와 Phase 매핑표). `validate-plugin.py planning-kit` 은 V1~V8 전부 OK 다.

따라서 **새 방법론·새 규칙·새 파일을 만들지 않는다.** evidence 가 잡은 **사실 오류 3 건 + 부수
2 건**만 정정한다. 정정은 **과잉 인용 제거**이지 규칙 폐기가 아니다 — 규칙 문장 자체는 보존되며
ER-01 이 그 보존을 잰다.

**정정 대상 (evidence §1 관찰 사실 · §2 권장안 기준):**

1. **"Projects v2 는 GraphQL" 은 틀렸다.** evidence: GitHub REST 공식 문서가
   `/orgs/{org}/projectsV2`, `/projectsV2/{project_number}/items`, `/fields` 를 제공한다.
   금지 대상은 **classic Projects** 다 — classic projects sunset 2024-08-23, classic REST API
   sunset 2025-04-01 을 이미 지났다. `gh project item-add --url` 패턴은 현행 CLI 문서와 일치하므로
   **기본 실행 경로는 `gh project` 로 유지**하고 GraphQL/REST 는 fallback 으로 병기한다
   (evidence §4 열린 질문 1 에 대한 이번 Phase 의 결정).
2. **"한 시나리오 = one When-Then pair" 는 Cucumber 원문 근거가 아니다.** evidence: 공식 문서에는
   오히려 "as many steps as you like" 와 successive `Then` 예시가 있다. 규칙은 **planning-kit 내부
   원자성 규칙**으로 라벨링하고, Cucumber 공식 근거로는 3-5 steps 권장과 observable `Then` 만 인용한다.
3. **HBR premortem 의 "개별 기록 → 공유" 절차는 접근 가능한 원문에서 미확인이다.** `[미확인]` 으로
   낮추고 비인용 내부 운영 팁으로 강등한다. HBR 로 인용 가능한 것은 기법 자체 (Gary Klein · 2007-09) 다.
4. **부수 — Betting Table 정본 URL.** evidence: `https://basecamp.com/shapeup/2.2-chapter-08`.
   현재 킷 안에 Betting Table 을 **URL 과 함께 인용하는 곳은 0 건**이므로 (`grep -rni betting`
   → `docs/planning/research-log.md:80` 1 행, URL 없음) 스킬 본문은 건드리지 않고 정본 URL 을
   research-log 신규 엔트리에 선제 기록만 한다.
5. **부수 — Mermaid 버전 고정 표기.** evidence: `v10` 같은 버전 고정은 원 문서에서 확인되지 않는다.
   근거 없는 버전 핀 2 건을 제거한다.

**Phase 1 서브에이전트 스펙 정정과의 교차 없음** — planning-kit 전체에서 중첩 깊이·frontmatter
필드 수를 서술하는 곳이 0 건이다 (`grep -rni '서브에이전트\|subagent\|중첩\|frontmatter' planning-kit`
→ 1 행, `plan-audit/SKILL.md:59` 의 "planning-reviewer 서브에이전트 spawn" 뿐이며 스펙 주장이 아니다).

## 리서치 소스 (evidence 파일 한정 — 외부 조회 0 회)

- `.harness/.meta/evidence/phase11.md` — 관찰 사실 9 항, 권장안 4 항, 트레이드오프 3 항,
  열린 질문 2 항. **인용 URL·수치는 이 파일에 실재하는 것만 쓴다** (AP-01 이 잰다).
- `.claude/kaizen-input/insights-report.md:110` — "Phase 11 Planning 직접 신호 없음" (Triage 근거).
- `.harness/.meta/kaizen-data-pool.md` §1 · §5 self-audit — planning 귀속 REJECT/Improvement 0 건,
  `planning-kit` V1~V8 OK.
- `docs/kaizen/changelog.md` `[2026-07-27]` / `[2026-07-28]` + `docs/planning/research-log.md`
  `[2026-07-27]` 엔트리 — 직전 사이클 흡수분 (canonical 미검증 규약 복제 · `## Surfaces` 양면 열거 ·
  INVEST 반증가능성). **재승격 금지 대상**이며 이번 변경은 그 목록과 교차하지 않는다.
- `harness/references/contract-schema.md` v5.3 (Phase 2 산출물) — 본 계약의 포맷 SSOT.
- Phase 1 `harness/docs/guides/skill-design-guide.md` §3.7 enforcement 등급 — 이번 Phase 는 신규
  조항 0 건이므로 등급 상향 대상도 0 건이다.

## GAP 분석 (전부 사전 실측 · 명령 출력 기준)

| # | 갭 | 사전 실측 | 처리 |
| --- | --- | --- | --- |
| F1 | `plan-sync-github` Gotcha 4 의 GraphQL-only 단정 | 옛 문자열 매치 **1** | SK-01 |
| F2 | 같은 스킬에서 REST 를 병기하지 않는 GraphQL 줄 | **2** (`:18`, `:90`) | SK-02 |
| F3 | `plan-stories` Gotcha 5 의 내부규칙 라벨 | `내부 원자성 규칙` **0** 건 | SK-03 |
| F4 | premortem "개별 기록 → 공유" 절차 중 `[미확인]` 미표기 | **3** (`plan-risks:22`, `plan-risks:40`, `risks.md:25`) | SK-04 |
| F5 | 근거 없는 Mermaid 버전 핀 | **2** (`reference.md:550`, `research-log.md:86`) | ER-02 |
| F6 | research-log 구 엔트리의 GraphQL-only 판단 (정정 포인터 없음) | **4** (`:24`, `:31`, `:57`, `:101`) | AR-03 |
| — | 감사 기준 표면 (`plan-audit` 카테고리 6·10 · `planning-reviewer`) | 정정 대상 아님 — 무변경 | ER-01 (보존 조건) |

**신설하지 않는 것**: 새 스킬 · 새 에이전트 · 새 references 파일 · 새 규칙 조항 · 새 섹션 헤더 ·
기존 규칙의 삭제 · plugin.json 버전 bump (이번 사이클 다른 Phase 도 bump 하지 않았다).

## 범위 경계

**변경 경로는 정확히 6 개.** 목록은 AR-01 의 기대 집합 한 곳에서만 열거한다
(§측정 커버리지 표기의 화이트리스트 규칙). 계약 파일 자신과 `.harness/**` 는 AR-01 pathspec 밖이다.

- **건드리지 않는다**: `planning-kit/skills/plan-audit/SKILL.md` · `planning-kit/agents/planning-reviewer.md`
  (감사 기준 — 정정 대상 서술이 없다) · `docs/planning/github-integration.md`
  (GraphQL-only 단정 **0 건** 확인 · `grep -n 'GraphQL' docs/planning/github-integration.md` → 매치 없음) ·
  `planning-kit/README.md` · `planning-kit/.claude-plugin/` · 다른 킷 전부.
- **`docs/planning/reference.md` 의 기존 bare code fence 5 건은 이번 Phase 범위 밖이다.** 문서 전역
  fence 정리는 별건(2026-07-28 커밋 `7ae0542` 계열)이며 여기서 섞지 않는다. AP-03 은 **증분**만 잰다.
- **evidence 에 없는 URL·수치를 새로 쓰지 않는다.** `gh project item-edit` 의 REST 대응 엔드포인트
  정확한 경로는 evidence 에 `/fields` 수준까지만 있으므로 그 이상 구체화하지 않는다 —
  근거 부족으로 이번 사이클 미반영.
- **Betting Table 정본 URL 은 research-log 기록까지만.** 인용처가 0 건이라 스킬 본문에 새 인용을
  만드는 것은 근거 없는 확장이다.

## 회귀 게이트

- 정정 항목은 "새 서술 추가" 가 아니라 **잔존 0 건 증명**으로 판정한다. 사전 출력
  (1 · 2 · 0 · 3 · 2 · 4) 이 discriminating 근거다 — 변경 전에는 전부 FAIL 이다.
- 모든 오라클을 zsh 와 bash 양쪽에서 실행하고 출력이 같아야 한다 (DG-02). 글로빙 대신 명시 경로를
  쓴다 (zsh `nomatch` 회피).
- grep 오라클의 substring 오탐 사전 확인: `v10` 은 `v10.6+` 도 잡는다 — **제거 방향**의 검사라
  오탐이 판정을 느슨하게 만들지 않는다. `GraphQL` 은 `gh api graphql` 소문자형도 잡도록 대소문자
  양쪽 패턴을 명시한다.
- 열거값(경로 수 · 잔존 건수)은 타이핑하지 않고 명령으로 계산한다.

## Skill

- [ ] SK-01: `plan-sync-github` Gotcha 4 가 `gh project` · GraphQL · REST `/projectsV2` 3 경로
      병기 + classic Projects 금지로 정정된다 [exact]
      (측정: `grep -c '\*\*Projects v2 는 GraphQL\*\*' planning-kit/skills/plan-sync-github/SKILL.md`
       → `0` (사전 `1`) · 같은 파일의 Gotcha 4 줄에 `gh project`, `graphql`, `/projectsV2`,
       `classic` 4 토큰이 모두 매치)
- [ ] SK-02: 같은 스킬 안에서 GraphQL 을 언급하는 모든 줄이 REST 경로를 함께 명시한다 [exact]
      (측정: `grep -n 'GraphQL\|graphql' planning-kit/skills/plan-sync-github/SKILL.md | grep -vc 'REST'`
       → `0` · 사전 출력 `2`)
- [ ] SK-03: `plan-stories` Gotcha 5 의 "When 1 개" 규칙이 planning-kit 내부 규칙으로 라벨링되고
      Cucumber 공식 근거가 3-5 steps · 관찰 가능한 `Then` 으로 한정된다 [exact]
      (측정: Gotcha 5 줄에 `내부 원자성 규칙`, `Cucumber 공식 규칙이 아니다`,
       `as many steps as you like`, `3-5 steps` 4 토큰이 모두 매치)
- [ ] SK-04: premortem "개별 기록 → 공유" 절차 서술이 전부 `[미확인]` 표기를 갖는다 [exact]
      (측정: `grep -rn '먼저 쓰고\|개별 기록\|그 다음 공유' planning-kit/skills/plan-risks/SKILL.md docs/planning/risks.md | grep -vc '미확인'`
       → `0` · 사전 출력 `3`)

## Error

- [ ] ER-01: 정정이 규칙 자체를 삭제하지 않는다 — 라벨 강등 ≠ 규칙 폐기 [exact, enumerated]
      (측정: `grep -c '트리거 1개씩 분리' planning-kit/skills/plan-stories/SKILL.md` → `1` ·
       `grep -c '개인별로 먼저 쓰고' planning-kit/skills/plan-risks/SKILL.md` → `1` ·
       `git diff --name-only HEAD -- planning-kit/skills/plan-audit/SKILL.md planning-kit/agents/planning-reviewer.md | grep -c .`
       → `0` ·
       음성 대조: Gotcha 5 에서 `트리거 1개씩 분리` 를 지우면 첫 측정이 FAIL 해야 한다)
- [ ] ER-02: 근거 없는 Mermaid 버전 고정 표기가 제거된다 [exact]
      (측정: `grep -c 'v10' docs/planning/reference.md` → `0` (사전 `1`) ·
       `sed -n '/^## \[2026-07-27\]/,$p' docs/planning/research-log.md | grep 'v10' | grep -vc '정정 2026-08-13'`
       → `0` (사전 `1`))

## Architecture

- [ ] AR-01: 변경이 정확히 6 경로로 한정된다 [exact, enumerated]
      (Given: 커밋 직전 working tree ·
       측정: `git diff --name-only HEAD -- planning-kit docs/planning | LC_ALL=C sort` 결과가
       `docs/planning/reference.md`,
       `docs/planning/research-log.md`,
       `docs/planning/risks.md`,
       `planning-kit/skills/plan-risks/SKILL.md`,
       `planning-kit/skills/plan-stories/SKILL.md`,
       `planning-kit/skills/plan-sync-github/SKILL.md` 6 행과 정확히 일치)
- [ ] AR-02: `docs/planning/research-log.md` 최상단에 2026-08-13 Phase 11 엔트리가 추가되고
      frontmatter `last_updated` 가 갱신된다 [exact]
      (측정: `grep -n '^## \[20' docs/planning/research-log.md | head -1` 이 `[2026-08-13]` 행이고 ·
       그 엔트리 본문에 `projectsV2`, `2.2-chapter-08`, `미확인`, `v10` 4 토큰이 모두 매치 ·
       `grep -c '^last_updated: 2026-08-13' docs/planning/research-log.md` → `1`)
- [ ] AR-03: research-log 구 엔트리(`## [2026-07-27]` 이후 영역)의 GraphQL-only 판단이 전부 정정
      포인터를 갖는다 [exact]
      (측정: `sed -n '/^## \[2026-07-27\]/,$p' docs/planning/research-log.md | grep 'GraphQL' | grep -vc '정정 2026-08-13'`
       → `0` · 사전 출력 `4`)

## Anti-patterns

- [ ] AP-01: 이번 변경이 새로 도입한 URL·수치가 전부 evidence 파일 또는 변경 전 트리에 실재한다
      (날조 0) [exact]
      (측정: 아래 스니펫 출력이 `UNSOURCED_URL=0` · 신규 수치 토큰 `2024-08-23`, `2025-04-01`,
       `2022-11-28` 이 각각 `.harness/.meta/evidence/phase11.md` 에 매치)
- [ ] AP-03: 이번 변경이 bare code fence 를 새로 도입하지 않는다 [exact]
      (측정: `python3 scripts/validate-plugin.py planning-kit` 의 V6 가 `0 bare` ·
       `git diff -U0 -- planning-kit docs/planning | grep -c "^+$(printf '\140\140\140')$"` → `0` ·
       기존 `docs/planning/reference.md` 의 bare fence 5 건은 범위 밖이라 손대지 않는다)

```sh
# AP-01 URL 출처 대조 — zsh · bash 동일. 매치 0 이어도 죽지 않는다
unsourced=0
git diff -U0 -- planning-kit docs/planning \
  | grep '^+' \
  | grep -oE 'https?://[^ )`]+' \
  | sed 's/[.,]*$//' \
  | LC_ALL=C sort -u > /tmp/p11-urls.txt
while IFS= read -r u; do
  [ -n "$u" ] || continue
  grep -qF -- "$u" .harness/.meta/evidence/phase11.md && continue
  git grep -qF -- "$u" HEAD -- planning-kit docs/planning && continue
  printf 'UNSOURCED %s\n' "$u"
  unsourced=$((unsourced + 1))
done < /tmp/p11-urls.txt
printf 'UNSOURCED_URL=%s\n' "$unsourced"
```

## Reusability

- [ ] RE-01: 신규 파일·신규 디렉토리 생성이 0 건이다 [exact]
      (측정: `git status --porcelain -- planning-kit docs/planning | grep -c '^??'` → `0`)
- [ ] RE-02: 스킬 3 파일에 새 `#`/`##` 섹션이 추가되지 않는다 (기존 Gotchas / Process 구조 재사용)
      [exact]
      (측정: `git diff -U0 -- planning-kit/skills | grep -c '^+#'` → `0`)

## Diagnostics

- [ ] DG-01: `python3 scripts/validate-plugin.py planning-kit` 이 V1~V8 전부 OK · exit `0` 이다 [exact]
- [ ] DG-02: 위 모든 grep / sed / git 오라클을 zsh 와 bash 에서 실행한 출력이 동일하다 (diff 0) [exact]
