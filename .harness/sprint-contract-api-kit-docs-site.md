---
feature: "api-kit 파이프라인 §14 잔여 4항목 — kaizen-orchestrator Phase 16 등록 + docs/api-kit 12 페이지 + index.html 등록"
slug: api-kit-docs-site
created: "2026-09-05 00:00"
complexity: "중간"
conditions: 38
status: done
---

## 배경

`/create-kit` 파이프라인 체크리스트(설계문서 §14) 12 항목 중 8 항목이 끝나 있고
`validate-plugin.py` 는 api-kit 에 대해 8/8 OK 다. 남은 것은 4 항목이다.

1. `kaizen-orchestrator` 에 api-kit 을 **Phase 16** 으로 등록 (SKILL.md · phase-research-templates.md · phase-dependencies.md)
2. `docs/api-kit/*.html` 12 페이지 생성
3. `docs/index.html` 의 `categories` 배열 + `getIcon()` 에 12 페이지 등록
4. QA 로 docs-site 7 카테고리 검증

## 공통 전제 (조건마다 반복하지 않는다)

- 모든 측정은 레포 루트 `/Users/jackson/Hub/10_Dev/claude-plugins` 에서 실행한다.
- **12 라는 수는 `docs/api/` 하위 `.md` 중 `research-log.md` 를 제외한 리서치 문서 수**다.
  하드코딩이 아니라 `find docs/api -name '*.md' ! -name research-log.md | wc -l` 로 확인된다.
- **122 라는 수는 그 12 문서의 `> **출처:**` 줄에서 뽑은 문서별 고유 URL 합계**다
  (`scripts/check-api-kit-docs.py` 가 같은 규칙으로 계산한다).
- HTML 페이지의 공통 골격·CSS 는 `tone-kit` 페이지 계열 규약을 따른다 — 테마 키 `dk-theme`,
  `.table-wrap`, `min-width:0`, `prefers-reduced-motion`.
- 이번 스프린트는 커밋·태그·푸시를 수행하지 않는다. 브랜치 생성과 커밋은 별도 단계다.

## 범위 경계

- `api-kit/` 플러그인 본체(스킬 5 종 · `api-reviewer` · references)는 이미 끝났고 **수정하지 않는다.**
- `docs/api/` 리서치 문서 12 종은 **읽기 전용**이다. 페이지 생성 과정에서 고치지 않는다.
- `.mockups/api-ui-v7.html` 은 `.gitignore` 대상이며 이번 범위 밖이다.
- Hurl 8.0.1 미검증 항목 5 건은 **해소 대상이 아니다.** 문서에 "미검증" 으로 보이게 하는 것까지가 범위다.
- `kaizen-orchestrator` 의 `AUTO:plugin_phases` 마커 영역은 손으로 고치지 않는다 —
  `scripts/sync-orchestrator.py` 가 `marketplace.json` 에서 생성한다.

## 회귀 게이트

기존 146+ 페이지와 15 개 킷이 깨지지 않아야 한다: `validate-plugin.py` 전체 통과,
`sync-docs.py --check-only` 클린, `sync-orchestrator.py --check-only` 클린,
index.html 의 기존 카테고리·아이콘 매핑 무결.

## Skill

- [ ] SK-01: `python3 scripts/sync-orchestrator.py --check-only` 가 exit 0 이고, 출력이 `12 plugins` 를 보고한다 [exact] (측정: 명령 실행 + 종료 코드)
- [ ] SK-02: `kaizen-orchestrator/SKILL.md` 의 AUTO 영역에 `### Step 16: Phase 16 — api-kit 카이젠` 헤딩이 **정확히 1 개** 존재하고 `/api-kaizen` 서브에이전트 호출과 `docs/api/` 리서치 경로를 함께 지시한다 [exact] (측정: `grep -c '^### Step 16: Phase 16 — api-kit'` == 1, 같은 절 안에 `/api-kaizen` · `docs/api/` 각 1 건 이상)
- [ ] SK-03: SKILL.md 의 **AUTO 영역 밖** 4 곳이 Phase 16 을 반영한다 — (a) Phase 흐름도에 `Phase 16: Api-kit 카이젠`, (b) 「Phase 순서 논리」 16 번 항목, (c) 수동 트리거 `phase16` 행, (d) `final` 전제가 `Phase 1~16` [exact, enumerated] (측정: 4 패턴 각각 `grep -c` >= 1)
- [ ] SK-04: SKILL.md 의 「Phase 별 추가 지시」에 api-kit 항목이 있고, 카이젠에서 완화하면 안 되는 확정 결정을 명시한다 — `pin` 재정의 · `exact` 본문 한정 · enum 3 샘플 · prod GET/HEAD/OPTIONS · RFC 8785 JCS · exit code 분리 [exact, enumerated] (측정: 해당 불릿 안에서 6 개 키워드 각각 1 건 이상)
- [ ] SK-05: `references/phase-research-templates.md` 에 `## Phase 16 — api-kit` 절이 있고 필수 소스가 **3 건 이상**이며, 그 절이 인용한 모든 `https://` URL 이 `docs/api/` 문서 또는 `research-log.md` 에 실재하는 URL 이다 [exact] (측정: 절 안의 URL 을 뽑아 `grep -rF` 로 `docs/api/` 에서 각각 조회. 음성 대조: 지어낸 URL 을 넣으면 조회 0 건이 되어 FAIL 한다)
- [ ] SK-06: `references/phase-dependencies.md` 3 곳이 갱신됐다 — 업데이트 순서 블록의 `Phase 16: Api-kit`, 의존성 상세 표의 `docs/api/` 행, 스킵 전파 규칙의 `Phase 15 스킵 → Phase 16` [exact, enumerated]
- [ ] SK-07: SKILL.md Step F2 의 소스→출력 매핑 표에 `api-kit` 행이 있고 출력이 `docs/api-kit/` 다 [structural]

## Script

- [ ] SC-01: `docs/api-kit/` 의 `.html` 파일 수가 `docs/api/` 리서치 문서 수와 같고, 파일명 stem 이 1:1 로 대응한다 [exact] (측정: 두 목록을 정렬해 diff — 계산값끼리 비교하므로 12 를 하드코딩하지 않는다)
- [ ] SC-02: 12 페이지 각각이 **450 줄 이상**이다 [exact, enumerated] (측정: `python3 scripts/check-api-kit-docs.py`)
- [ ] SC-03: 12 소스 문서의 출처 URL 이 **한 건도 빠짐없이** 대응 HTML 의 `href` 에 존재한다 [exact] (측정: `python3 scripts/check-api-kit-docs.py` exit 0. 음성 대조: 임의 페이지에서 `card-source` href 하나를 지우면 그 URL 이 누락으로 보고되고 exit 1 이 된다 — 이 대조를 실제로 1 회 실행해 확인한다)
- [ ] SC-04: `docs/index.html` 의 `API Kit` 카테고리에 12 개 항목이 있고, 각 `file` 경로가 `docs/` 기준으로 실재한다 [exact, enumerated] (측정: 파이썬으로 `categories` 배열을 파싱해 `os.path.exists` 전수)
- [ ] SC-05: `getIcon()` 에 12 개 id 가 모두 있고 고아 아이콘이 0 이다 [exact] (측정: id 집합과 아이콘 키 집합의 양방향 차집합이 공집합)
- [ ] SC-06: 카테고리 accent 가 `#A3E635` 이고 `docs-site/references/css-tokens.md` 의 API Kit 매핑과 일치한다 [exact]

## Error

- [ ] ER-01: 12 페이지 어디에도 외부 리소스 참조가 없다 — `<link `, `<script src=`, `@import`, `url(http` 각 0 건 [exact, enumerated] (측정: `check-api-kit-docs.py` 의 EXTERNAL 패턴)
- [ ] ER-02: 12 페이지를 `file://` 로 열었을 때 콘솔 에러가 0 건이다 [exact] (측정: Playwright `console` + `pageerror` 수집)
- [ ] ER-03: 가로 오버플로를 `overflow:hidden` / `overflow-x:hidden` 으로 억제한 페이지가 0 개다 [exact] (`overflow-x:auto` 는 허용 — 스크롤로 끝까지 도달 가능해야 한다)
- [ ] ER-04: 테마 토글이 `localStorage` 접근 실패(사생활 보호 모드 등)에서도 페이지를 깨뜨리지 않는다 [structural] (측정: 토글 스크립트의 `getItem`/`setItem` 이 `try/catch` 안에 있는지 확인)

## Architecture

- [ ] AR-01: 12 페이지 각각의 `:root` 가 `--accent:#A3E635` 와 `--accent2:#D9F99D` 를 선언한다 [exact, enumerated]
- [ ] AR-02: 12 페이지의 가로 오버플로가 **375px 와 768px 양쪽에서 2px 이하**다 [exact, enumerated] (측정: Playwright 로 `scrollWidth - clientWidth` 실측. 0px 를 목표로 하고 경계값 튜닝으로 맞추지 않는다)
- [ ] AR-03: 본문 텍스트와 accent 링크의 전경/배경 대비가 다크·라이트 각각 **4.5:1 이상**이다 [exact] (측정: Playwright 로 computed color 를 읽어 WCAG 상대휘도로 계산. 라이트 테마 accent 는 lime 이 흰 배경에서 대비가 안 나오므로 별도 값을 쓴다)
- [ ] AR-04: 테마 토글 버튼의 실측 클릭 타깃이 44×44 CSS px 이상이다 [exact] (측정: `getBoundingClientRect()`)
- [ ] AR-05: 이번 스프린트가 `docs/` 아래 새로 만든 파일은 `docs/api-kit/*.html` 12 개뿐이다 [exact] (측정: `git status --porcelain docs/` 의 신규 항목 열거)
- [ ] AR-06: `prefers-reduced-motion: reduce` 대응이 12 페이지 전부에 있다 [exact, enumerated]

## Design (docs-site 7 카테고리)

`design-kit/skills/design-audit/references/audit-criteria.md` 의 7 카테고리를 12 페이지 전체에 적용한다.

- [ ] DS-01 Typography: 타이포 스케일이 12 페이지에서 동일하고, 본문 계열(`.desc` `.subtitle` `td`)이 13px 이상이며 line-height 가 1.2~1.8 범위다 [structural]
- [ ] DS-02 Color: 시맨틱 토큰(`--text` `--text2` `--text3` `--accent` `--green` `--red` `--yellow`)만 쓰고, 페이지 전용 CSS 가 새 hex 리터럴을 도입하지 않는다 [exact] (측정: 각 페이지의 `</style>` 직전 페이지 전용 블록에서 `#[0-9a-fA-F]{3,8}` 0 건)
- [ ] DS-03 Spacing: `.section` 간격과 카드 padding 이 `clamp()` 기반 공통 스케일을 따르고 페이지마다 다시 정의되지 않는다 [structural]
- [ ] DS-04 Accessibility: AR-02~AR-04 의 실측 결과(오버플로 · 대비 · 44px)가 12 페이지 전부 통과다 [exact]
- [ ] DS-05 Interaction: 인터랙티브 요소(테마 토글 · 출처 링크)에 hover 와 `:focus-visible` 스타일이 모두 있다 [exact, enumerated] (측정: `.theme-toggle:focus-visible` · `.card-source:focus-visible` 각 12 페이지에 존재)
- [ ] DS-06 Motion: 트랜지션이 200~500ms 범위이고 `prefers-reduced-motion: reduce` 에서 전부 꺼진다 [exact] (측정: `--transition:0.25s` + reduce 블록의 `transition:none !important`)
- [ ] DS-07 Authenticity: 같은 구조의 섹션이 한 페이지에서 3 회 연속 반복되지 않는다 — 원칙 카드 · 표 · bad/good 쌍 · 체크리스트 · 흐름 카드가 섞여 배치된다 [structural]

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — 페이지의 `v0.1.0` 표기는 소스 `.md` frontmatter 를 옮긴 **표시용**이며 로직 분기에 쓰지 않는다
- [ ] AP-03: 이번에 변경한 `.md` 에 bare code fence 가 0 건이다 (언어 힌트 필수) [exact] (측정: `validate-plugin.py` V6)

## Reusability

- [ ] RE-01: 12 페이지가 공통 골격을 공유한다 — 같은 CSS 변수 이름, 같은 유틸리티 클래스(`.card` `.table-wrap` `.checklist` `.pair` `.flow`), 같은 테마 스크립트. 페이지마다 규약을 새로 발명하지 않는다 [structural]
- [ ] RE-02: 기존 `docs-site` 규약을 재사용한다 — 테마 키는 `dk-theme` 하나이며 새 키를 만들지 않는다 [exact]

## Diagnostics

- [ ] DG-01: `python3 -m py_compile scripts/sync-orchestrator.py scripts/check-api-kit-docs.py` 에러 0 건
- [ ] DG-02: `python3 scripts/validate-plugin.py` 전체 킷 통과 (api-kit 8/8 포함)
- [ ] DG-03: `python3 scripts/sync-docs.py --check-only` 가 동기화 상태를 보고한다
- [ ] DG-04: 실제 브라우저 구동 시 에러 0 개 (ER-02 와 같은 실행에서 수집)
