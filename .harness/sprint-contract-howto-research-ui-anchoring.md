---
feature: "howto-research 3 사이클 — ui-anchoring 규칙 강도 교정"
slug: howto-research-ui-anchoring
created: "2026-09-09 17:10"
complexity: "복잡"
conditions: 24
status: done
owner_session: 4d264694-eb0e-4e84-801f-52b2db804772
conditions_digest: sha256:ac14502f09311b6d
locked_at: "2026-09-09 16:01"
---

## 배경

`/howto-research` 세 번째 사이클. 카테고리는 `ui-anchoring` 하나만 다룬다 (SKILL.md Gotcha 4).

**이 사이클은 킷의 규칙이 근거보다 강했다는 것을 고친다.** 킷은 P5 를 "방향어 **대신** 명명된
컨테이너" 로 쓰고 Google 스타일 가이드를 근거로 달았다. 그런데 킷이 인용한 벤더 문장 8 건 중
**4 건이 방향어를 쓴다** (`on the right`, `at the top-right`, `in the upper-right corner`,
`at the bottom of the page`). 규칙과 근거가 서로 어긋나 있었다.

리서치 결과 **Microsoft 스타일 가이드가 이 모순을 명시적으로 푼다**:

> *"Don't use directional terms (left, right, up, down) as the only clue to location. … It's OK to
> use a directional term if another indication of location, such as in the Save As dialog box, on
> the Standard toolbar, or in the title bar, is also included."*

즉 올바른 규칙은 **금지가 아니라 단독 사용 금지**다. 인용된 벤더 문장 4 건은 전부 방향어에
**이름을 붙여** 쓰므로 위반이 아니다.

킷 내부는 이미 갈려 있었다 — 체크리스트와 reviewer R4 는 `~만으로`(단독)라고 옳게 썼는데,
제목·본문은 `~대신`(대체)이라고 썼다. 이번 스프린트가 그 불일치를 없앤다.

## 리서치 소스

- Codex 위임 1 회 (MODE=research, read-only, foreground, 검색 하드캡 20). rollout
  `turn_aborted` 0 건. Google · Microsoft 원문 확보, Apple 동등 조항은 확인 실패로 반환.
- Codex 가 본문 fetch 에 실패한 Stripe 인용 1 건은 세션 로컬 `curl` 로 해소했다.
- 인용 4 건(Google 1 · Microsoft 2 · Stripe 1)은 전부 **응답 본문에서 직접 추출**해 대조했다.

## 범위 경계

- 카테고리는 `ui-anchoring` 하나. 나머지 3 종은 이번 스프린트에서 만들지 않는다.
- **규칙을 약화하는 것이 아니다.** 단독 사용 금지는 그대로 강제한다. 바뀌는 것은 (a) 규칙 진술이
  "대체" 에서 "단독 금지" 로 정확해지는 것 (b) 완화 조건의 출처가 Google 이 아니라 Microsoft 로
  바로잡히는 것이다.
- `docs/howto/drafts/SKILL.md` 는 설계 시점 스냅샷이라 고치지 않는다.
- `.claude/worktrees/` 와 `result.json` 은 다른 세션 소유다.
- diff-scope baseline: 계약 작성 시점, 이 계약 파일 1 행 외 **0 행**.

## GAP 분석

| 대상 파일 | 현재 상태 (Read 증거) | 처리 |
| --- | --- | --- |
| `docs/howto/ui-anchoring.md` | 부재 | 신규 생성 (AR-01) |
| `howto-kit/references/navigation-anchors.md` | `:44` 제목이 "방향어 대신", Google 만 인용 | 규칙 진술 교정 + Microsoft 원문 (SK-01) |
| `howto-kit/skills/howto/SKILL.md` | `:114` Gotcha 5 제목 "대신", `:121` Google 만 인용 | 같음 (SK-02) |
| `howto-kit/agents/howto-reviewer.md` | `:43` R4 는 `만으로` 로 이미 옳음 | 허용 조건 2 종을 판정 기준에 명시 (SK-03) |
| `docs/howto/design-brief.md` | `:117` P5 제목 "대신" | 1 줄 교정 + 정본 포인터 (AR-02) |
| `howto-kit/references/provenance-notes.md` | §1~5 | Apple 확인 실패 추가 (ER-03) |
| `docs/howto-kit/`, `docs/index.html` | 3 면 | 미러 신규 + 등록 (AR-03~05) |

## 회귀 게이트

이 스프린트의 위험은 **규칙을 약화시키는 것**이다. "방향어를 써도 된다" 로 읽히면 F4(화면에서
항목을 못 찾음)가 되살아난다. ER-01 이 단독 사용 금지가 유지되는지를, ER-02 가 허용 조건이
**이름과 함께일 때로 한정**되는지를 각각 잰다.

## Skill

- [ ] SK-01: `navigation-anchors.md` §3 이 규칙을 **단독 사용 금지**로 진술하고 Microsoft 원문을 인용한다 [exact] (측정: `awk '/^## 3\. 화면 지목 어휘/{f=1;print;next} f&&/^## /{exit} f' howto-kit/references/navigation-anchors.md` 로 §3 블록을 추출한 뒤 — `only clue to location` 문자열이 1 회 이상, `learn.microsoft.com` 이 1 회 이상. **awk 범위형을 쓰지 않는다**)
- [ ] SK-02: `skills/howto/SKILL.md` Gotcha 5 가 같은 교정을 반영한다 [exact] (측정: `awk '/^### Gotcha 5:/{f=1;print;next} f&&/^### /{exit} f' howto-kit/skills/howto/SKILL.md` 블록에 `단독` 토큰과 `learn.microsoft.com` 이 각각 1 회 이상)
- [ ] SK-03: `howto-reviewer.md` R4 의 판정 기준이 허용 조건 2 종을 명시한다 [exact, enumerated] — (a) 다른 위치 단서가 함께 있을 때 (b) 동작 결과로 화면 변화가 보일 때 (측정: R4 행 또는 그 인접 서술에 두 조건이 각각 등장)

## Script

- [ ] SC-01: CI validate job 의 python 검사 8 종이 전부 exit 0 [exact, enumerated] — `scripts/validate-plugin.py`, `scripts/sync-evals.py --check-only`, `scripts/sync-docs.py --check-only`, `scripts/sync-orchestrator.py --check-only`, `scripts/run-evals.py --verbose`, `scripts/check-contrast-claims.py`, `scripts/check-docs-links.py`, `scripts/check-stale-values.py` (측정: 8 개를 각각 실행해 exit code 를 표로 인용. 음성 대조: `docs/index.html` 등록을 빼면 `check-docs-links.py` 가 FAIL 한다)
- [ ] SC-02: `bash howto-kit/evals/run-evals.sh` 가 exit 0 이고 `9/9 PASS` 다 [exact] (측정: 해당 명령 실행. 음성 대조: 픽스처의 `확인` 줄을 지우면 G6 이 FAIL 한다)
- [ ] SC-03: `node scripts/check-docs-a11y.js docs/howto-kit/ui-anchoring.html` 이 exit 0 [exact] (측정: 해당 명령 실행. 음성 대조: `--text3` 를 `#7A6F64` 로 낮추면 대비 미달로 FAIL 한다)

## Error

- [ ] ER-01: 단독 사용 금지가 **유지**된다 — 어느 파일에서도 "방향어를 써도 된다" 로 읽히는 무조건 허용 진술이 없다 [goal] (측정: sweep 은 **검사 범위 크기를 먼저 출력**한다. `git ls-files | grep -v '^\.harness/' | wc -l` 로 대상 수를 출력한 뒤, 방향어 규칙을 다루는 파일들에서 `단독`·`만으로`·`only clue` 중 최소 1 개가 규칙 진술과 같은 블록에 있는지 확인. 범위가 0 이면 측정 무효이므로 FAIL)
- [ ] ER-02: 허용 조건이 **이름·위치 단서와 함께일 때로 한정**된다 — 무조건 허용이 아니다 [exact] (측정: `docs/howto/ui-anchoring.md` 에 `another indication of location` 원문이 1 회 이상 등장하고, 그 조건이 허용의 전제로 서술된다)
- [ ] ER-03: Apple 동등 조항 부재가 `[미확인]` 으로 원장에 남고 시도 URL 이 나열된다 [exact] (측정: `howto-kit/references/provenance-notes.md` 에 `Apple` 과 `확인 실패` 가 같은 항목에 등장하고 시도 URL 이 1 개 이상)
- [ ] ER-04: Google 과 Microsoft 의 **입장 차이**가 문서에 구분되어 적힌다 — Google 은 완화 조건을 명시하지 않았다 [structural] (측정: `docs/howto/ui-anchoring.md` 에서 Google 과 Microsoft 가 각각 별도 항목으로 인용되고, Google 쪽에 완화 조건 부재가 명시된다)

## Architecture

- [ ] AR-01: 신규 리서치 문서가 `docs/howto/ui-anchoring.md` 경로에 존재한다 [exact] (측정: `test -f docs/howto/ui-anchoring.md`)
- [ ] AR-02: `design-brief.md` §P5 가 교정되고 정본 포인터를 갖는다 [exact] (측정: `grep -c 'ui-anchoring.md' docs/howto/design-brief.md` 가 1 이상이고, §P5 제목에 `대신` 이 남아 있지 않다)
- [ ] AR-03: HTML 미러 `docs/howto-kit/ui-anchoring.html` 이 존재하고 `docs/index.html` 의 `pages` 배열과 `getIcon()` 양쪽에 **동일한 id** 로 등록된다 [exact, enumerated] (측정: 파일 존재 + `grep -c "howto-ui-anchoring" docs/index.html` 가 2 이상이며 그중 하나는 `file:` 항목, 하나는 `getIcon` 매핑임을 각각 확인)
- [ ] AR-04: HTML 미러가 howto-kit accent 토큰과 공용 대비 토큰을 규약대로 쓴다 [exact, enumerated] — dark `--accent:#F59E0B` · light `--accent:#B45309` · dark `--text3:#948779` · light `--text3:#656C7A` · `localStorage` 키 `dk-theme` (측정: 5 개 리터럴을 각각 `grep -c` 로 확인, 전부 1 이상)
- [ ] AR-05: HTML 미러가 400 줄 이상이고 **외부 리소스 로드**가 0 건이다 [exact] (측정: `wc -l` 가 400 이상. 외부 로드는 `grep -cE '<link[^>]+rel="stylesheet"[^>]+https?://|<script[^>]+src="https?://|@import[^;]*https?://|url\(https?://'` 가 0. 본문 인용의 `<a href="https://...">` 출처 링크는 제외한다)
- [ ] AR-06: 변경 범위가 선언한 경로에 정확히 일치한다 [exact, enumerated] (Given: 이번 스프린트의 커밋이 완료된 후. 측정: `git diff --name-only main...HEAD -- docs howto-kit .harness ':(exclude).claude/worktrees' ':(exclude)result.json'` 의 결과 집합이 `git diff --name-only main...HEAD` 전체 집합과 **정확히 일치**한다)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수. 판정 권위는 validate-plugin V6 상태기계다 (측정: `python3 scripts/validate-plugin.py --check=code-fence`)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 금지 (측정: `python3 scripts/validate-plugin.py`)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — HTML 미러는 `docs/howto-kit/deep-links.html` 의 토큰 블록·테마 토글 구조를 재사용한다

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외 — project.yaml 의 ide_exclude 가 빈 목록)
- [ ] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개 — N/A (플러그인 모노레포. SC-03 의 a11y 게이트가 렌더 검증을 대신한다)
