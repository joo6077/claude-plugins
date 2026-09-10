---
feature: "howto-research 첫 사이클 — changelog-feeds 1차 출처 확정 및 반영"
slug: howto-research-changelog-feeds
created: "2026-09-09 09:55"
complexity: "복잡"
conditions: 27
status: done
owner_session: 4d264694-eb0e-4e84-801f-52b2db804772
conditions_digest: sha256:ca745849209eb9d6
locked_at: "2026-09-09 10:01"
---

## 배경

`/howto-research` 의 첫 사이클이다. 카테고리는 `changelog-feeds` 하나만 다룬다
(SKILL.md Gotcha 4 — 한 번에 한 카테고리).

`howto-kit/references/provenance-notes.md` §3 은 2026-09-08 확인분으로 4 건 확정 · 3 건 미확인
상태였고, Google Cloud 피드는 "XML 인 것은 확인했으나 RSS/Atom 어느 서브타입인지는 확인하지
못했다" 로 남아 있었다.

이번 사이클의 실측(2026-09-09)으로 확정 **5 건**(Google Cloud · Apple Developer News ·
Apple Releases · GitHub Changelog · AWS What's New), 미확인 **3 건**(Firebase · Stripe ·
Azure updates)이 됐다. AWS 는 §3 에 없던 신규 확정이다.

**이번 사이클이 얻은 방법론적 반례**: AWS 는 `https://aws.amazon.com/new/` 에 피드
autodiscovery 링크가 없는데도 RSS 피드가 정상 동작한다. 따라서 "autodiscovery 링크 부재" 를
"피드 부재" 의 근거로 쓸 수 없다. Firebase · Stripe 를 "피드 없음" 으로 단정하지 않고 미확인으로
두는 근거가 이것이다.

## 리서치 소스

- Codex 위임 1 회 (MODE=research, read-only, foreground, 검색 하드캡 20).
  rollout `~/.codex/sessions/2026/09/09/rollout-2026-09-09T09-38-58-01a0839a-898e-7a53-adc4-6f9ba8845dc9.jsonl`,
  `turn_aborted` 0 건으로 정상 완주 확인. 단 Codex 샌드박스는 DNS 가 막혀 XML 원문을 열지 못해
  루트 엘리먼트·Content-Type 을 전부 확인 실패로 반환했다.
- 부족분은 세션 로컬 `curl` 로 피드 원문을 직접 조회해 보강했다. 루트 엘리먼트·Content-Type ·
  최신 항목은 **응답 본문 원문**에서 추출한 값이다.

## 범위 경계

- 카테고리는 `changelog-feeds` 하나. `deep-links` · `ui-anchoring` · `branch-catalog` ·
  `deprecation-policy` · `procedure-standards` 5 종은 이번 스프린트에서 만들지 않는다.
- `provenance-notes.md` §1(체크리스트 방법론) · §2(Microsoft Learn) · §4(이름 충돌)는 건드리지
  않는다. §1 은 이미 6 URL 시도 실패로 확정된 결론이 있고, 뒤집으려면 1 차 출처가 먼저다.
- `.claude/worktrees/` 와 `result.json` 은 다른 세션(bambu)의 미추적 산출물이다. 이번 스프린트에서
  추가·삭제·gitignore 처리를 하지 않는다.
- `docs/howto/design-brief.md` 는 설계 정본이므로 리서치 결과로 덮어쓰지 않는다. §11-6 한 줄만
  최소 수정한다 (사용자 승인 2026-09-09).
- diff-scope baseline: 계약 작성 시점에 `docs/howto` · `howto-kit` ·
  `.claude/skills/howto-research` 3 경로의 변경은 **0 건**이었다 (Step 실행 출력으로 확인).

## GAP 분석

| 대상 파일 | 현재 상태 (Read 증거) | 이번 스프린트 처리 |
| --- | --- | --- |
| `docs/howto/changelog-feeds.md` | 부재 — `docs/howto/` 에는 `design-brief.md` 와 `drafts/` 뿐 | 신규 생성 (AR-01) |
| `howto-kit/references/provenance-notes.md` | `:67-92` §3 에 확정분과 미확인분이 섞여 있음 | 확정 5 건 이관, 미확인 3 건 잔존 (AR-02) |
| `howto-kit/README.md` | `:129` "일부 RSS 피드 … **확인 실패**" | 3 건 기준으로 재서술 (AR-03) |
| `docs/howto/design-brief.md` | `:391` §11-6 "RSS/변경 로그 피드 URL 실측을 완료하지 못했다" | 1 줄 최소 수정 (AR-04) |
| `.claude/skills/howto-research/SKILL.md` | `:27` Gotcha 3 이 피드 URL 정본으로 원장을 가리킴 | 정본을 리서치 문서로 이전 (SK-01) |
| `docs/howto-kit/` | `overview.html` 하나뿐 | HTML 미러 신규 + index 등록 (AR-05~07) |

## 회귀 게이트

옛 등급 표기 잔존이 이 스프린트의 주된 회귀 형태다 (Gotcha 2 — "원장만 고치면 본문에 옛 등급
표기가 남는다"). AR-08 이 sweep 으로 이를 막고, sweep 은 **검사 범위 크기부터 출력**한다.
범위가 비어 0 건이 나오는 것과 실제로 0 건인 것을 구분하기 위해서다.

## Skill

- [ ] SK-01: `.claude/skills/howto-research/SKILL.md` 의 Gotcha 3 블록이 확정 피드 URL 의 정본 위치로 `docs/howto/changelog-feeds.md` 를 명시한다 [exact] (측정: `awk '/^3\. \*\*피드 URL 은 바뀐다/,/^4\. \*\*/' .claude/skills/howto-research/SKILL.md | grep -c 'changelog-feeds.md'` 가 1 이상. 섹션 앵커를 쓰는 이유는 파일 전체 grep 이 Step 1 표의 기존 토큰으로도 통과하기 때문이다)
- [ ] SK-02: 같은 Gotcha 3 블록이 "인용 전 재조회" 요구를 유지한다 — 확정됐다는 이유로 재조회 규칙을 완화하지 않았다 [structural] (측정: 위와 같은 awk 블록에서 `grep -cE '다시 조회|재조회'` 가 1 이상)
- [ ] SK-03: SKILL.md Step 1 표의 `변경 로그 폴링` 행이 가리키는 문서가 실재한다 [exact] (측정: `test -f docs/howto/changelog-feeds.md` 가 exit 0)

## Script

- [ ] SC-01: CI validate job 의 python 검사 8 종이 전부 exit 0 [exact, enumerated] — `scripts/validate-plugin.py`, `scripts/sync-evals.py --check-only`, `scripts/sync-docs.py --check-only`, `scripts/sync-orchestrator.py --check-only`, `scripts/run-evals.py --verbose`, `scripts/check-contrast-claims.py`, `scripts/check-docs-links.py`, `scripts/check-stale-values.py` (측정: 8 개를 각각 실행해 exit code 를 표로 인용. 음성 대조: `docs/index.html` 등록을 빼면 `check-docs-links.py` 가, HTML 미러의 대비 서술을 틀리게 적으면 `check-contrast-claims.py` 가 FAIL 한다)
- [ ] SC-02: `node scripts/check-docs-a11y.js docs/howto-kit/changelog-feeds.html` 이 exit 0 [exact] (측정: 해당 명령 실행. 음성 대조: `--text3` 를 `#7A6F64` 로 낮추면 이 게이트가 대비 미달로 FAIL 한다)
- [ ] SC-03: `bash harness/evals/kaizen/feedback-system/save-test.sh` 가 exit 0 [exact] (측정: 해당 명령 실행. 음성 대조: `harness/scripts/save-feedback.sh` 의 경로 계산을 깨면 FAIL 한다)

## Error

- [ ] ER-01: Firebase · Stripe · Azure updates 3 건이 "피드 없음" 으로 단정되지 않고 `[미확인]` 등급으로 표기되며, 각각에 대해 시도한 URL 이 문서에 나열된다 [exact, enumerated] (측정: `docs/howto/changelog-feeds.md` 에서 `Firebase` · `Stripe` · `Azure` 각 항목이 `[미확인]` 토큰과 같은 표 행 또는 같은 하위 섹션에 있고, 각 항목의 시도 URL 코드블록에 URL 이 1 개 이상)
- [ ] ER-02: "autodiscovery 링크 부재 ≠ 피드 부재" 라는 반례가 AWS 사례와 함께 문서에 명시된다 [structural] (측정: `grep -cE 'autodiscovery' docs/howto/changelog-feeds.md` 가 1 이상이고 그 서술이 AWS 를 반례로 지목한다)
- [ ] ER-03: 확정 5 건 각각에 조회일 `2026-09-09` 가 표기된다 [exact, enumerated] — `Google Cloud`, `Apple Developer News`, `Apple Releases`, `GitHub Changelog`, `AWS What's New` (측정: 5 개 벤더 각각의 표 행 또는 항목에 `2026-09-09` 가 있는지 개별 확인)
- [ ] ER-04: Azure 후보의 실패 사유가 "부재" 가 아니라 관측된 HTTP 결과로 기록된다 [exact] (측정: `docs/howto/changelog-feeds.md` 의 Azure 항목에 `403` 과 `301` 이 모두 등장하고, 후자가 HTML 로의 리다이렉트임이 적혀 있다)

## Architecture

- [ ] AR-01: 신규 리서치 문서가 `docs/howto/changelog-feeds.md` 경로에 존재한다 [exact] (측정: `test -f docs/howto/changelog-feeds.md`)
- [ ] AR-02: `provenance-notes.md` §3 에서 확정 5 건이 제거되고 미확인 3 건만 남는다 [exact, enumerated] (측정: `awk '/^## 3\./,/^## 4\./' howto-kit/references/provenance-notes.md` 로 §3 블록만 잘라낸 뒤 — `Google Cloud`·`Apple Developer news`·`Apple releases`·`GitHub changelog`·`AWS` 5 토큰이 확정 표 행으로 남아 있지 않고, `Firebase`·`Stripe`·`Azure` 3 토큰은 남아 있다. 파일 전체 grep 을 쓰지 않는 이유는 §3 밖의 서술이 같은 토큰을 갖기 때문이다)
- [ ] AR-03: `howto-kit/README.md` 의 "이 킷이 사실로 말하지 않는 것" 절이 피드 관련 확인 실패를 3 건 기준으로 서술한다 — 확정된 5 건을 여전히 확인 실패로 부르지 않는다 [exact] (측정: `awk '/^## 이 킷이 사실로 말하지 않는 것/,/^## /' howto-kit/README.md` 블록에 `Firebase`·`Stripe`·`Azure` 중 최소 1 개가 등장하고, `Google Cloud`·`GitHub`·`Apple` 은 확인 실패 대상으로 열거되지 않는다)
- [ ] AR-04: `docs/howto/design-brief.md` §11 의 6 번 항목이 (a) 확정분 해소 (b) 잔존 3 건 (c) `changelog-feeds.md` 포인터 3 요소를 담는다 [exact, enumerated] (측정: 해당 줄에 `changelog-feeds.md` 문자열과 `3` 또는 세 벤더명이 함께 등장. 그 줄 외 §11 의 나머지 7 항목은 변경하지 않는다)
- [ ] AR-05: HTML 미러 `docs/howto-kit/changelog-feeds.html` 이 존재하고, `docs/index.html` 의 `pages` 배열과 `getIcon()` 양쪽에 **동일한 id** 로 등록된다 [exact, enumerated] (측정: 파일 존재 + `grep -c "howto-changelog-feeds" docs/index.html` 가 2 이상이며 그중 하나는 `file:` 항목, 하나는 `getIcon` 매핑임을 각각 확인)
- [ ] AR-06: HTML 미러가 howto-kit accent 토큰과 공용 대비 토큰을 규약대로 쓴다 [exact, enumerated] — dark `--accent:#F59E0B` · light `--accent:#B45309` · dark `--text3:#948779` · light `--text3:#656C7A` · `localStorage` 키 `dk-theme` (측정: 5 개 리터럴을 각각 `grep -c` 로 확인, 전부 1 이상)
- [ ] AR-07: HTML 미러가 400 줄 이상이고 **외부 리소스 로드**가 0 건이다 [exact] (측정: `wc -l` 가 400 이상. 외부 로드는 `grep -cE '<link[^>]+rel="stylesheet"[^>]+https?://|<script[^>]+src="https?://|@import[^;]*https?://|url\(https?://'` 가 0. 본문 인용의 `<a href="https://...">` 출처 링크는 리소스 로드가 아니므로 이 측정에서 제외한다 — docs-site Gotcha 9 가 출처 링크를 오히려 요구한다)
- [ ] AR-08: 옛 등급 표기 잔존 0 건 — 확정된 5 벤더가 레포 어디에서도 피드 미확인/확인 실패 상태로 서술되지 않는다 [goal] (측정: sweep 은 **검사 범위 크기를 먼저 출력**한다. `git ls-files 'docs/howto*' 'howto-kit/*' '.claude/skills/howto-research/*' | wc -l` 로 대상 파일 수를 출력한 뒤, 그 파일들에서 확인 실패 맥락과 5 벤더명이 같은 줄에 있는 경우가 0 건임을 확인. 범위가 0 이면 측정 자체가 무효이므로 FAIL 로 본다)
- [ ] AR-09: 변경 범위가 선언한 경로에 정확히 일치한다 [exact, enumerated] (Given: 이번 스프린트의 커밋이 완료된 후. 측정: `git diff --name-only main...HEAD -- docs/howto docs/howto-kit docs/index.html howto-kit .claude/skills/howto-research ':(exclude).claude/worktrees' ':(exclude)result.json'` 의 결과 집합이 실제 변경 파일 전체 집합과 **정확히 일치**한다. 즉 `git diff --name-only main...HEAD` 전체와 위 pathspec 한정 결과가 같아야 한다)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 (측정: `python3 scripts/validate-plugin.py --check=code-fence`)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 금지 — validate-plugin V1 FAIL (측정: `python3 scripts/validate-plugin.py`)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — HTML 미러는 `docs/howto-kit/overview.html` 의 토큰 블록·테마 토글 IIFE 구조를 재사용하고 새 패턴을 발명하지 않는다

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외 — project.yaml 의 ide_exclude 가 빈 목록이므로 제외 대상 없음)
- [ ] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개 — N/A (이 레포는 구동 가능한 앱/서버가 없는 플러그인 모노레포다. docs 사이트는 정적 HTML 이며 SC-02 의 a11y 게이트가 렌더 검증을 대신한다)
