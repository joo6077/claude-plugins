---
feature: "howto-research 2 사이클 — deep-links 1차 출처 확정"
slug: howto-research-deep-links
created: "2026-09-09 16:05"
complexity: "복잡"
conditions: 24
status: done
owner_session: 4d264694-eb0e-4e84-801f-52b2db804772
conditions_digest: sha256:3ebb87958d77d396
locked_at: "2026-09-09 15:38"
---

## 배경

`/howto-research` 두 번째 사이클. 카테고리는 `deep-links` 하나만 다룬다 (SKILL.md Gotcha 4).

이 킷의 P3 는 "딥링크가 메뉴 경로보다 우선한다" 다. 그 원칙이 서 있으려면 **벤더 공식 문서가
실제로 콘솔 URL 을 본문에 박아 둔다**는 사실이 1 차 출처로 확정돼야 한다. `navigation-anchors.md`
§2 에 5 행짜리 표가 있었지만 2026-09-08 확인분이고, 인용 문장이 축약돼 있었다.

이번 사이클로 **7 벤더 · 8 인용**을 확정했다 (Firebase · Google Cloud · Apple · Stripe ×2 ·
GitHub · AWS · Azure). Azure 와 AWS 는 기존 표에 없던 신규다.

**이번 사이클이 얻은 검증 기법**: `developer.apple.com` 문서는 SPA 라서 HTML 을 받아도
17KB 껍데기만 온다. 검증 가능한 원문은 `https://developer.apple.com/tutorials/data/documentation/<경로>.json`
이다. 이 경로를 모르면 Apple 인용은 영원히 "확인 실패" 로 남는다 — 실제로 이번 Codex 위임이
그렇게 끝났다.

## 리서치 소스

- Codex 위임 1 회 (MODE=research, read-only, foreground, 검색 하드캡 20). rollout
  `~/.codex/sessions/2026/09/09/rollout-2026-09-09T15-31-40-01a084dd-7440-7392-86df-2e2507ba9741.jsonl`,
  `turn_aborted` 0 건. 5 건 확정 · Stripe · Azure 2 건 확인 실패로 반환.
- Codex 가 실패한 2 건과, Codex 인용문 3 건의 대조 실패는 세션 로컬 `curl` 로 해소했다.
  인용문은 전부 **응답 본문에서 추출**한 것이며 Codex 요약을 그대로 옮기지 않았다.

## 범위 경계

- 카테고리는 `deep-links` 하나. 나머지 4 종은 이번 스프린트에서 만들지 않는다.
- 콘솔 URL 자체를 열어 검증하지 않는다 — 로그인 리다이렉트라 의미가 없다. **근거는 그 URL 을
  담은 공식 문서 페이지**다.
- `.claude/worktrees/` 와 `result.json` 은 다른 세션 소유다. 건드리지 않는다.
- diff-scope baseline: 계약 작성 시점, 이 계약 파일 1 행 외 **0 행**.

## GAP 분석

| 대상 파일 | 현재 상태 (Read 증거) | 처리 |
| --- | --- | --- |
| `docs/howto/deep-links.md` | 부재 | 신규 생성 (AR-01) |
| `howto-kit/references/navigation-anchors.md` | `:16-27` §2 표 5 행, 인용 축약, AWS·Azure 없음 | 확정 인용으로 교체 + 2 행 추가 + 정본 포인터 (AR-02) |
| `howto-kit/references/provenance-notes.md` | §1~4 존재 | 확인 실패 2 건 추가 (ER-04) |
| `docs/howto-kit/`, `docs/index.html` | `changelog-feeds.html` 까지 2 면 | HTML 미러 신규 + 등록 (AR-03~05) |

## 회귀 게이트

이 킷의 실패 형태는 **확인 못 한 것을 확인한 척하는 것**이다. Codex 가 실패로 돌려준 2 건을
내가 curl 로 해소했다는 사실과, Codex 인용 3 건이 1 차 대조에서 MISS 났다는 사실을 모두
문서에 남긴다. "Codex 가 그렇게 말했다" 는 근거가 아니다.

## Skill

- [ ] SK-01: `docs/howto/deep-links.md` 의 확정 인용이 **전부 문서 URL 과 짝**으로 제시된다 [structural] (측정: 확정 표의 각 행에 `https://` 로 시작하는 출처 URL 이 1 개 이상. 출처 열이 빈 행이 0)
- [ ] SK-02: Apple 문서의 검증 경로(`tutorials/data/documentation/<경로>.json`)가 기법으로 명시된다 [exact] (측정: `grep -c 'tutorials/data/documentation' docs/howto/deep-links.md` 가 1 이상)
- [ ] SK-03: Stripe 의 `MODE` 가 URL 세그먼트라는 공식 문법이 원문 인용으로 실린다 [exact] (측정: `grep -c 'omit a value for live mode' docs/howto/deep-links.md` 가 1 이상)

## Script

- [ ] SC-01: CI validate job 의 python 검사 8 종이 전부 exit 0 [exact, enumerated] — `scripts/validate-plugin.py`, `scripts/sync-evals.py --check-only`, `scripts/sync-docs.py --check-only`, `scripts/sync-orchestrator.py --check-only`, `scripts/run-evals.py --verbose`, `scripts/check-contrast-claims.py`, `scripts/check-docs-links.py`, `scripts/check-stale-values.py` (측정: 8 개를 각각 실행해 exit code 를 표로 인용. 음성 대조: `docs/index.html` 등록을 빼면 `check-docs-links.py` 가 FAIL 한다)
- [ ] SC-02: `node scripts/check-docs-a11y.js docs/howto-kit/deep-links.html` 이 exit 0 [exact] (측정: 해당 명령 실행. 음성 대조: `--text3` 를 `#7A6F64` 로 낮추면 대비 미달로 FAIL 한다)
- [ ] SC-03: `bash harness/evals/kaizen/feedback-system/save-test.sh` 가 exit 0 [exact] (측정: 해당 명령 실행. 음성 대조: `save-feedback.sh` 의 스키마 검증을 무력화하면 negative test 가 FAIL 한다)

## Error

- [ ] ER-01: 확정 7 벤더 각각에 조회일 `2026-09-09` 가 표기된다 [exact, enumerated] — `Firebase`, `Google Cloud`, `Apple`, `Stripe`, `GitHub`, `AWS`, `Azure` (측정: 7 개 벤더 각각의 행 또는 항목에 `2026-09-09` 가 있는지 개별 확인)
- [ ] ER-02: Codex 가 확인 실패로 돌려준 2 건(Stripe · Azure)을 로컬 조회로 해소했다는 사실이 문서에 남는다 [structural] (측정: `docs/howto/deep-links.md` 에 `Codex` 토큰과 `curl` 토큰이 모두 등장하고, 그 서술이 위임 결과와 로컬 조회 결과를 구분한다)
- [ ] ER-03: Codex 인용 3 건이 1 차 대조에서 불일치했다는 사실이 문서에 남는다 — 요약을 그대로 옮기지 않았다는 근거 [structural] (측정: 같은 문서에 `대조` 또는 `MISS` 토큰이 등장하고 그 서술이 인용 검증 절차를 가리킨다)
- [ ] ER-04: 확인 실패 2 건이 `[미확인]` 으로 남고 시도 URL 이 나열된다 [exact, enumerated] — Google 계정 슬롯 `/u/0/`, Firebase `_` 자리표시자 **설명 문장** (측정: `howto-kit/references/provenance-notes.md` 에 두 항목이 각각 `확인 실패` 또는 `[미확인]` 과 함께 등장하고, 각각 시도 URL 이 1 개 이상)

## Architecture

- [ ] AR-01: 신규 리서치 문서가 `docs/howto/deep-links.md` 경로에 존재한다 [exact] (측정: `test -f docs/howto/deep-links.md`)
- [ ] AR-02: `navigation-anchors.md` §2 표가 확정 인용으로 갱신되고 AWS · Azure 행이 추가되며 정본 포인터를 갖는다 [exact, enumerated] (측정: `awk '/^## 2\. 실측된 딥링크 관행/{f=1;print;next} f&&/^## /{exit} f' howto-kit/references/navigation-anchors.md` 로 §2 블록만 추출한 뒤 — `AWS` 와 `Azure` 토큰이 각각 1 회 이상, `deep-links.md` 포인터가 1 회 이상. **awk 범위형을 쓰지 않는다**)
- [ ] AR-03: HTML 미러 `docs/howto-kit/deep-links.html` 이 존재하고 `docs/index.html` 의 `pages` 배열과 `getIcon()` 양쪽에 **동일한 id** 로 등록된다 [exact, enumerated] (측정: 파일 존재 + `grep -c "howto-deep-links" docs/index.html` 가 2 이상이며 그중 하나는 `file:` 항목, 하나는 `getIcon` 매핑임을 각각 확인)
- [ ] AR-04: HTML 미러가 howto-kit accent 토큰과 공용 대비 토큰을 규약대로 쓴다 [exact, enumerated] — dark `--accent:#F59E0B` · light `--accent:#B45309` · dark `--text3:#948779` · light `--text3:#656C7A` · `localStorage` 키 `dk-theme` (측정: 5 개 리터럴을 각각 `grep -c` 로 확인, 전부 1 이상)
- [ ] AR-05: HTML 미러가 400 줄 이상이고 **외부 리소스 로드**가 0 건이다 [exact] (측정: `wc -l` 가 400 이상. 외부 로드는 `grep -cE '<link[^>]+rel="stylesheet"[^>]+https?://|<script[^>]+src="https?://|@import[^;]*https?://|url\(https?://'` 가 0. 본문 인용의 `<a href="https://...">` 출처 링크는 리소스 로드가 아니므로 제외한다)
- [ ] AR-06: 변경 범위가 선언한 경로에 정확히 일치한다 [exact, enumerated] (Given: 이번 스프린트의 커밋이 완료된 후. 측정: `git diff --name-only main...HEAD -- docs howto-kit .harness ':(exclude).claude/worktrees' ':(exclude)result.json'` 의 결과 집합이 `git diff --name-only main...HEAD` 전체 집합과 **정확히 일치**한다)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수. 판정 권위는 validate-plugin V6 상태기계다 (측정: `python3 scripts/validate-plugin.py --check=code-fence`)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 금지 (측정: `python3 scripts/validate-plugin.py`)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — HTML 미러는 `docs/howto-kit/changelog-feeds.html` 의 토큰 블록·테마 토글 구조를 재사용하고 새 패턴을 발명하지 않는다

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외 — project.yaml 의 ide_exclude 가 빈 목록)
- [ ] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개 — N/A (플러그인 모노레포. docs 사이트는 정적 HTML 이며 SC-02 의 a11y 게이트가 렌더 검증을 대신한다)
