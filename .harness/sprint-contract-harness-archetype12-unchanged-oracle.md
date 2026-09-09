---
feature: "harness 아키타입 12 신설 · 미변경 조건 오라클 규칙"
slug: harness-archetype12-unchanged-oracle
created: "2026-09-09 13:20"
complexity: "복잡"
conditions: 22
status: active
owner_session: 4d264694-eb0e-4e84-801f-52b2db804772
conditions_digest: sha256:c335ef27bcb4405e
locked_at: "2026-09-09 13:23"
---

## 배경

백로그 2 건을 한 스프린트로 묶는다. 둘 다 harness 설계 가이드의 결함이고, 둘 다 **직전
스프린트들이 평가자 Improvement 로 남겨 둔 것**이다.

**(1) 12 번째 아키타입 "절차 안내형".** `docs/howto/design-brief.md` §8 이 판단을 다음 세션으로
넘겼다. 근거는 실측으로 확보했다 — 사람이 외부 UI 를 조작하도록 안내하는 스킬이 **2 개 킷에
독립적으로 4 개** 존재한다 (`howto-kit/skills/howto`, `howto-audit`, `howto-doc`,
`onboarding-kit/skills/setup-guide`). 기존 11 유형 중 정의상 맞는 슬롯이 없다 — Type 1
(라이브러리 레퍼런스)은 코드 API 사용법이고, Type 8(런북)은 장애 트리거다.

이 유형의 **구별되는 실패 모드**가 새 슬롯을 정당화한다. Type 11 이 산출물 개수 때문에 별도
유형인 것처럼, 이 유형은 **입도 부족(F2)을 날조(F3)로 메우는 것**이 고유 실패다. 자세히 쓰라는
요구를 지어내기로 충족시키는 것은 다른 어떤 유형에도 없는 실패 경로다.

**(2) 미변경 조건의 오라클.** #37 평가자 Improvement: 측정식 `grep -cE '^\+.*v5\.[45]'` 는
"이 변경이 버전을 상향했는가" 와 "diff 텍스트 어딘가에 그 숫자가 나오는가" 를 구분하지 못해,
순수 서술("v5.4 는 다른 브랜치가 선점")이 1 회 FAIL 을 유발했다.

## 리서치 소스

외부 리서치 없음 — 두 항목 모두 **이 레포의 실측 실패 기록**이 근거다.

- 아키타입: `docs/howto/design-brief.md` §8, 그리고 `find`/`grep` 으로 센 실제 스킬 4 개
- 오라클: `.harness/sprint-feedback-harness-amend-direction-baseline-case.md:120`
  (#37 평가자 Improvement 원문)
- awk 범위형: 이번 세션의 `sprint-amendments-howto-research-changelog-feeds.md` AM-01

## 범위 경계

- **이전 스프린트의 헤더 동결 결정을 뒤집는다.** `sprint-contract-kaizen-phase1-design-guides.md:70`
  은 `## 2. 스킬 9가지 유형 체크리스트` 헤더를 "레포 밖 6 개 surface 가 리터럴로 참조" 한다는
  이유로 동결했다. 그 스프린트의 평가자가 이미 재검색으로 **0 건**임을 지적했고
  (`sprint-feedback-kaizen-phase1-design-guides.md:145`), 이번에 직접 재확인해도 리터럴 참조는
  `skill-design-guide.md` 자신과 `.harness/` 이력 파일뿐이다. 소비면은 전부 산문 `9가지` 다.
- **`.harness/` 안의 과거 계약·피드백·data-pool 은 고치지 않는다.** 그 시점의 기록이며 봉인된
  이력이다. sweep 대상에서 제외한다.
- `.claude/projects/` (다른 프로젝트 메모리) 와 `.claude/kaizen-input/` (입력 산출물)도 제외한다.
- 아키타입 12 의 강제 조항을 `skill-design-guide` 안에 새로 만들지 않는다 — 입도·출처 등급 규칙은
  `howto-kit` 소관이고, harness 가이드가 특정 킷 규칙을 강제하면 레이어가 뒤집힌다. 참조 구현으로만
  가리킨다.
- diff-scope baseline: 계약 작성 시점 `git status --porcelain` 에서 이 계약 파일 1 행 외 **0 행**.

## GAP 분석

| 대상 파일 | 현재 상태 (Read 증거) | 처리 |
| --- | --- | --- |
| `harness/docs/guides/skill-design-guide.md` | `:46` 헤더 "9가지" 인데 표는 11 행 — 살아 있는 불일치 | 12 행 추가 + 개수 리터럴 제거 (SK-01~04) |
| `harness/docs/guides/contract-design-guide.md` | `:566` §측정 명령 타당성에 (1)(2)(3) 만 있음 | (4) 신설 (ER-01~04) |
| `CLAUDE.md` | `:368` "9가지 아키타입" | 개수 제거 (AR-03) |
| `harness/skills/create-skill/SKILL.md` | `:5, :28, :46, :108` 4 곳 | 개수 제거 (AR-03) |
| `harness/evals/evals.json` | `:35` assertion 문구 | 개수 제거 (AR-03) |
| `flutter-toolkit/skills/flutter-kaizen/SKILL.md` | `:158` | 개수 제거 (AR-03) |
| `.claude/skills/create-kit/SKILL.md` | `:44` | 개수 제거 (AR-03) |
| `.claude/skills/api-kaizen/SKILL.md` | `:85` | 개수 제거 (AR-03) |
| `.claude/skills/kaizen-orchestrator/references/search-sources.md` | `:78` "기존 9가지 외에" | 개수 제거 (AR-03) |

## 회귀 게이트

개수 리터럴이 드리프트의 원인이다 — 표가 9 → 11 로 늘 때 헤더와 소비면 7 곳이 따라오지 않아
지금 상태가 됐다. 12 로 올리기만 하면 **다음 추가에서 똑같이 깨진다.** 그래서 개수를 이름에서
빼고, 개수는 표 바로 아래 주석에서만 말한다. AR-01 이 리터럴 0 건을 sweep 으로 강제한다.

## Skill

- [ ] SK-01: `skill-design-guide.md` §2 표에 12 행 `절차 안내형` 이 추가된다 [exact] (측정: `awk '/^## 2\./{f=1;print;next} f&&/^## /{exit} f' harness/docs/guides/skill-design-guide.md` 로 §2 블록만 추출한 뒤 `grep -cE '^\| 12 \|.*절차 안내형'` 이 1. **awk 범위형(`/^## 2\./,/^## /`)을 쓰지 않는 이유는 시작 줄이 종료 패턴에도 매치되어 1 줄만 반환하기 때문이다** — 이번 스프린트가 규칙으로 승격하는 바로 그 결함이다)
- [ ] SK-02: 같은 §2 블록의 표 아래 주석이 (a) 출처 구분 `1~9` 공식 / `10~12` 레포 추가 (b) 12 번 신설의 실측 근거를 담는다 [structural] (측정: §2 블록에서 `1~9` 와 `10~12` 두 토큰이 각각 1 회 이상, 그리고 `howto-kit` 또는 `setup-guide` 토큰이 1 회 이상)
- [ ] SK-03: §2 헤더에서 개수 리터럴이 제거된다 [exact] (측정: `grep -cE '^## 2\..*[0-9]+ ?가지' harness/docs/guides/skill-design-guide.md` 가 0 이고, `grep -c '^## 2\. 스킬 유형 체크리스트'` 가 1)
- [ ] SK-04: 12 번 유형의 **구별되는 실패 모드**가 §2 블록에 명시된다 — 입도 부족을 날조로 메우는 것 [structural] (측정: §2 블록에 `날조` 또는 `지어내` 토큰이 1 회 이상 등장하고 그 문장이 12 번 유형을 가리킨다)

## Script

- [ ] SC-01: CI validate job 의 python 검사 8 종이 전부 exit 0 [exact, enumerated] — `scripts/validate-plugin.py`, `scripts/sync-evals.py --check-only`, `scripts/sync-docs.py --check-only`, `scripts/sync-orchestrator.py --check-only`, `scripts/run-evals.py --verbose`, `scripts/check-contrast-claims.py`, `scripts/check-docs-links.py`, `scripts/check-stale-values.py` (측정: 8 개를 각각 실행해 exit code 를 표로 인용. 음성 대조: `harness/evals/evals.json` 의 assertion `text` 를 빈 문자열로 만들면 `run-evals.py` 가 FAIL 한다 — 이 스프린트가 그 파일을 건드리므로 실효 있는 대조다)
- [ ] SC-02: `bash harness/evals/kaizen/feedback-system/save-test.sh` 가 exit 0 [exact] (측정: 해당 명령 실행. 음성 대조: `harness/scripts/save-feedback.sh` 의 스키마 검증을 무력화하면 negative test 3 건이 FAIL 한다)

## Error

- [ ] ER-01: `contract-design-guide.md` §측정 명령 타당성에 **(4) 항**이 신설되고, "변경하지 않았음/부재를 diff 텍스트 리터럴 매칭으로 재지 마라" 규칙을 담는다 [exact] (측정: `awk '/^#### 측정 명령 타당성/{f=1;print;next} f&&/^#{1,4} /{exit} f' harness/docs/guides/contract-design-guide.md` 로 절을 추출한 뒤 `grep -cE '^\*\*\(4\)'` 가 1)
- [ ] ER-02: 그 항이 #37 실측 근거를 인용한다 — 리터럴 매칭이 순수 서술에 FAIL 을 유발했다는 사실 [structural] (측정: 같은 절 블록에 `v5\.` 와 `329e47c` 또는 `#37` 중 하나가 등장)
- [ ] ER-03: 대체 oracle 이 **실행 가능한 명령 형태**로 제시된다 — 선언 라인 한정 [structural] (측정: 같은 절 블록에 `git diff` 를 포함한 코드펜스 또는 백틱 명령이 1 개 이상 있고 그것이 선언 라인 패턴(`현재: \*\*v5\.` 류)을 한정한다)
- [ ] ER-04: awk 범위형 퇴화 규칙이 같은 절에 실리고 실측 수치를 포함한다 [exact] (측정: 같은 절 블록에 `awk` 토큰이 있고, 범위형이 반환한 줄 수 `1` 과 플래그형이 반환한 줄 수 `9` 가 대조로 제시된다)

## Architecture

- [ ] AR-01: 아키타입 개수 리터럴이 레포 활성 표면에서 0 건이 된다 [goal] (측정: sweep 은 **검사 범위 크기를 먼저 출력**한다. `git ls-files | grep -v '^\.harness/' | grep -v '^\.claude/projects/' | grep -v '^\.claude/kaizen-input/' | wc -l` 로 대상 수를 출력한 뒤, 그 파일들에서 `grep -nE '[0-9]+ ?가지 (아키타입|스킬 유형|유형)'` 히트가 0. 범위가 0 이면 측정 무효이므로 FAIL)
- [ ] AR-02: producer — `skill-design-guide.md` §2 가 아키타입 카탈로그의 정본으로서 12 행을 갖는다 [exact] (측정: §2 블록에서 `grep -cE '^\| [0-9]+ \|'` 가 12)
- [ ] AR-03: consumer — 아키타입 카탈로그를 인용하는 7 개 파일이 전부 갱신된다 [exact, enumerated] — `CLAUDE.md`, `harness/skills/create-skill/SKILL.md`, `harness/evals/evals.json`, `flutter-toolkit/skills/flutter-kaizen/SKILL.md`, `.claude/skills/create-kit/SKILL.md`, `.claude/skills/api-kaizen/SKILL.md`, `.claude/skills/kaizen-orchestrator/references/search-sources.md` (측정: 7 개 각각에 대해 `grep -cE '[0-9]+ ?가지'` 가 0 임을 **개별로** 확인해 표로 인용한다. 상위 패턴 하나로 뭉뚱그리지 않는다)
- [ ] AR-04: 변경 범위가 선언한 경로에 정확히 일치한다 [exact, enumerated] (Given: 이번 스프린트의 커밋이 완료된 후. 측정: `git diff --name-only main...HEAD -- harness CLAUDE.md flutter-toolkit .claude/skills .harness ':(exclude).claude/worktrees' ':(exclude)result.json'` 의 결과 집합이 `git diff --name-only main...HEAD` 전체 집합과 **정확히 일치**한다)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수. 판정 권위는 validate-plugin V6 상태기계다 (측정: `python3 scripts/validate-plugin.py --check=code-fence`)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 금지 (측정: `python3 scripts/validate-plugin.py`)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — (4) 항은 기존 `#### 측정 명령 타당성` 절 **안에** 넣고 새 최상위 절을 만들지 않는다

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외 — project.yaml 의 ide_exclude 가 빈 목록)
- [ ] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개 — N/A (플러그인 모노레포이며 이 스프린트는 문서·JSON 만 바꾼다. SC-01 의 run-evals/validate-plugin 실행이 유일한 런타임을 대신 검증한다)
