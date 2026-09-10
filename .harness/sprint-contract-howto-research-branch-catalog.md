---
feature: "howto-research 4 사이클 — branch-catalog 사유 유형 재정의"
slug: howto-research-branch-catalog
created: "2026-09-10 09:40"
complexity: "복잡"
conditions: 24
status: active
owner_session: 4d264694-eb0e-4e84-801f-52b2db804772
conditions_digest: sha256:de2726387b7bbb38
locked_at: "2026-09-10 11:11"
---

## 배경

`/howto-research` 네 번째 사이클. 카테고리는 `branch-catalog` 하나만 다룬다 (SKILL.md Gotcha 4).

**갭**: 킷은 분기 사유를 **5 종**(권한/역할 · 요금제 · 버전 · 언어 · A/B 롤아웃)으로 유형화해
놓고, 실제 인용을 확보한 것은 **권한 계열뿐**이었다. 나머지 4 종은 근거 없이 목록에만 있었다 —
그것 자체가 이 킷이 막으려는 F3 다.

이번 사이클의 결과는 셋이다.

1. **나머지 3 종의 1 차 출처를 확보했다** — 요금제(Dropbox) · 버전(Microsoft) ·
   A/B 롤아웃(Google DV360).
2. **6 번째 사유를 발견했다.** 기존 목록의 Apple 인용은 권한 분기가 아니라 **기능 선행조건**
   분기였다 — *"The Campaigns feature becomes available only after your app has received analytics
   data."* 권한도 요금제도 버전도 아니다. 유형 목록에 없던 사유다.
3. **언어/로케일은 다른 축이다.** 나머지 사유는 "항목이 없을 수 있다" 인데 언어는 "항목은 있는데
   이름이 다르다" 다. 실패 모드가 달라 같은 목록에 두면 안 된다. 게다가 언어 분기 문장의
   1 차 출처는 **확보하지 못했다**.

## 리서치 소스

- Codex 위임 1 회 (MODE=research, read-only, foreground, 검색 하드캡 20). rollout
  `turn_aborted` 0 건. A 3 건 재확인 · B 3 종 신규 확보 · 언어와 스타일 가이드 조항은
  확인 실패로 반환.
- 인용 6 건은 전부 세션 로컬 `curl` 로 **응답 본문에서 직접 대조**했다. 1 차 대조에서 Dropbox
  1 건이 MISS 였는데 원인이 **HTML 엔티티**(`&#39;`)였다 — 디코드 후 재대조로 확정.

## 범위 경계

- 카테고리는 `branch-catalog` 하나. `deprecation-policy` · `procedure-standards` 2 종은 이번
  스프린트에서 만들지 않는다.
- **`cause` enum 확장은 게이트에 영향이 없다** — `howto-gate.sh` 는 enum 을 검사하지 않는다
  (grep 0 건으로 확인). 게이트를 바꾸지 않는다.
- `docs/howto/drafts/SKILL.md` 는 설계 시점 스냅샷이라 고치지 않는다.
- `onboarding-kit` 파일은 다른 킷이므로 건드리지 않는다.
- `.claude/worktrees/` 와 `result.json` 은 다른 세션 소유다. **`main` 이 그 워크트리에
  체크아웃되어 있으므로 `main` 을 이 저장소에서 체크아웃하지 않는다.**
- diff-scope baseline: 계약 작성 시점, 이 계약 파일 1 행 외 **0 행**.

## GAP 분석

| 대상 파일 | 현재 상태 (Read 증거) | 처리 |
| --- | --- | --- |
| `docs/howto/branch-catalog.md` | 부재 | 신규 생성 (AR-01) |
| `howto-kit/references/navigation-anchors.md` | `:5장` 사유 표 5 행, 권한 외 인용 없음 | 6 종 + 인용 부착 (SK-01) |
| `howto-kit/references/step-contract.md` | `:29` `cause: 권한|요금제|버전|언어|A/B` | enum 확장 + 언어 축 분리 (SK-02) |
| `howto-kit/skills/howto/SKILL.md` | `:111` "분기 사유 5 종" | 6 종으로 교정 (SK-03) |
| `docs/howto/design-brief.md` | `:151` "5 가지", `:209` cause enum | 교정 + 정본 포인터 (AR-02) |
| `howto-kit/references/provenance-notes.md` | §1~6 | 확인 실패 2 건 추가 (ER-03) |
| `docs/howto-kit/`, `docs/index.html` | 4 면 | 미러 신규 + 등록 (AR-03~05) |

## 회귀 게이트

이 스프린트의 위험은 **유형을 늘리면서 근거 없는 항목을 또 만드는 것**이다. ER-01 이 6 종
각각에 인용이 붙었는지를, ER-02 가 언어 축이 사유 목록에서 분리됐는지를 잰다.

## Skill

- [ ] SK-01: `navigation-anchors.md` §5 의 사유 표가 **6 종**이 되고 각 행에 출처가 붙는다 [exact, enumerated] — 권한/역할 · 기능 선행조건 · 요금제 · 버전 · A/B 롤아웃 · (언어는 별도 축) (측정: `awk '/^## 5\./{f=1;print;next} f&&/^## /{exit} f' howto-kit/references/navigation-anchors.md` 로 §5 블록을 추출한 뒤 — `선행조건` 토큰이 1 회 이상, 그리고 `Dropbox`·`Windows`·`rolled out gradually` 3 토큰이 각각 1 회 이상. **awk 범위형을 쓰지 않는다**)
- [ ] SK-02: `step-contract.md` 의 `cause` enum 이 확장되고 언어가 사유 목록에서 분리된다 [exact] (측정: `grep -n 'cause:' howto-kit/references/step-contract.md` 결과 줄에 `선행조건` 이 포함되고 `언어` 가 같은 enum 파이프 목록 안에 남아 있지 않다)
- [ ] SK-03: `skills/howto/SKILL.md` 가 "5 종" 이 아니라 6 종으로 서술한다 [exact] (측정: `grep -c '분기 사유 5 종' howto-kit/skills/howto/SKILL.md` 가 0 이고, `분기 사유 6 종` 이 1 회 이상)

## Script

- [ ] SC-01: CI validate job 의 python 검사 8 종이 전부 exit 0 [exact, enumerated] — `scripts/validate-plugin.py`, `scripts/sync-evals.py --check-only`, `scripts/sync-docs.py --check-only`, `scripts/sync-orchestrator.py --check-only`, `scripts/run-evals.py --verbose`, `scripts/check-contrast-claims.py`, `scripts/check-docs-links.py`, `scripts/check-stale-values.py` (측정: 8 개를 각각 실행해 exit code 를 표로 인용. 음성 대조: `docs/index.html` 등록을 빼면 `check-docs-links.py` 가 FAIL 한다)
- [ ] SC-02: `bash howto-kit/evals/run-evals.sh` 가 exit 0 이고 `pass=9 fail=0` 이다 [exact] (측정: 해당 명령 실행. 음성 대조: 픽스처의 `안 보이면` 줄을 지우면 G6 이 FAIL 한다)
- [ ] SC-03: `node scripts/check-docs-a11y.js docs/howto-kit/branch-catalog.html` 이 exit 0 [exact] (측정: 해당 명령 실행. 음성 대조: `--text3` 를 `#7A6F64` 로 낮추면 대비 미달로 FAIL 한다)

## Error

- [ ] ER-01: 사유 6 종 각각에 **1 차 출처 인용**이 붙는다 — 목록에만 있고 근거 없는 항목이 0 개 [exact, enumerated] — `권한/역할`, `기능 선행조건`, `요금제`, `버전`, `A/B 롤아웃`, 그리고 언어(별도 축, `[미확인]` 표기) (측정: `docs/howto/branch-catalog.md` 의 사유 표에서 각 행의 출처 열이 비어 있지 않은지 **개별로** 확인해 표로 인용한다. 언어 행은 `[미확인]` 이면 통과)
- [ ] ER-02: 언어/로케일이 **사유 목록에서 분리**되고 그 이유가 명시된다 — "항목이 없다" 가 아니라 "이름이 다르다" [structural] (측정: `docs/howto/branch-catalog.md` 에 언어가 별도 축이라는 서술이 있고, 실패 모드 차이가 문장으로 설명된다)
- [ ] ER-03: 확인 실패 2 건이 원장에 남고 시도 URL 이 나열된다 [exact, enumerated] — (a) 언어/로케일 분기 문장 (b) 선제 분기를 규정한 **스타일 가이드 조항** (측정: `howto-kit/references/provenance-notes.md` 에 두 항목이 각각 리터럴 `확인 실패` 와 함께 등장하고, 각각 시도 URL 이 1 개 이상)
- [ ] ER-04: 검증 함정 — **HTML 엔티티 때문에 리터럴 대조가 실패한다**는 실측이 문서에 남는다 [exact] (측정: `docs/howto/branch-catalog.md` 에 `&#39;` 또는 `엔티티` 토큰이 등장하고, Dropbox 인용이 MISS→HIT 로 바뀐 경위가 서술된다)

## Architecture

- [ ] AR-01: 신규 리서치 문서가 `docs/howto/branch-catalog.md` 경로에 존재한다 [exact] (측정: `test -f docs/howto/branch-catalog.md`)
- [ ] AR-02: `design-brief.md` 의 5 가지 주장이 교정되고 정본 포인터를 갖는다 [exact] (측정: `grep -c 'branch-catalog.md' docs/howto/design-brief.md` 가 1 이상이고, `grep -c '분기 사유는 5 가지로 유형화한다' docs/howto/design-brief.md` 가 0)
- [ ] AR-03: HTML 미러 `docs/howto-kit/branch-catalog.html` 이 존재하고 `docs/index.html` 의 `pages` 배열과 `getIcon()` 양쪽에 **동일한 id** 로 등록된다 [exact, enumerated] (측정: 파일 존재 + `grep -c "howto-branch-catalog" docs/index.html` 가 2 이상이며 그중 하나는 `file:` 항목, 하나는 `getIcon` 매핑임을 각각 확인)
- [ ] AR-04: HTML 미러가 howto-kit accent 토큰과 공용 대비 토큰을 규약대로 쓴다 [exact, enumerated] — dark `--accent:#F59E0B` · light `--accent:#B45309` · dark `--text3:#948779` · light `--text3:#656C7A` · `localStorage` 키 `dk-theme` (측정: 5 개 리터럴을 각각 `grep -c` 로 확인, 전부 1 이상)
- [ ] AR-05: HTML 미러가 400 줄 이상이고 **외부 리소스 로드**가 0 건이다 [exact] (측정: `wc -l` 가 400 이상. 외부 로드는 `grep -cE '<link[^>]+rel="stylesheet"[^>]+https?://|<script[^>]+src="https?://|@import[^;]*https?://|url\(https?://'` 가 0. 본문 인용의 `<a href="https://...">` 출처 링크는 제외한다)
- [ ] AR-06: 변경 범위가 선언한 경로에 정확히 일치한다 [exact, enumerated] (Given: 이번 스프린트의 커밋이 완료된 후. 측정: `git diff --name-only origin/main...HEAD -- docs howto-kit .harness ':(exclude).claude/worktrees' ':(exclude)result.json'` 의 결과 집합이 `git diff --name-only origin/main...HEAD` 전체 집합과 **정확히 일치**한다. `main` 이 다른 워크트리에 체크아웃되어 있으므로 `origin/main` 을 기준으로 잰다)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수. 판정 권위는 validate-plugin V6 상태기계다 (측정: `python3 scripts/validate-plugin.py --check=code-fence`)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 금지 (측정: `python3 scripts/validate-plugin.py`)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — HTML 미러는 `docs/howto-kit/ui-anchoring.html` 의 토큰 블록·테마 토글 구조를 재사용한다

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외 — project.yaml 의 ide_exclude 가 빈 목록)
- [ ] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개 — N/A (플러그인 모노레포. SC-03 의 a11y 게이트가 렌더 검증을 대신한다)
