---
feature: "howto-research 6 사이클 — procedure-standards 확정 · DITA 모델 명시"
slug: howto-research-procedure-standards
created: "2026-09-10 13:30"
complexity: "복잡"
conditions: 24
status: done
owner_session: 4d264694-eb0e-4e84-801f-52b2db804772
conditions_digest: sha256:4f61371a67736e33
locked_at: "2026-09-10 12:10"
---

## 배경

`/howto-research` 마지막 사이클. 카테고리는 `procedure-standards` 하나만 다룬다 (Gotcha 4).
이것으로 리서치 문서 6 종이 전부 선다.

킷은 DITA 1.3 을 근거로 스텝 규약을 세웠는데, 설계 브리프 §11-2 가 ISO/IEC/IEEE 26514·26515 는
**정의·개요만 확인**했다고 남겨 뒀다.

이번 사이클의 결과는 셋이다.

1. **DITA 인용 2 건 확정** — `<cmd>` 의 *"should not be more than one sentence"*,
   `<stepresult>` 의 *"should not be used for every step"*.
2. **킷의 `<taskbody>` 인용이 불완전했다.** DITA 1.2 부터 OASIS 배포본에는 **task 모델이 둘**이다 —
   *"the DTD and Schema packages distributed by OASIS contain two task models"*. 킷이 인용한
   고정 순서 모델은 **strict task model** 이고, general task model 은 요소를 더 허용하며 순서도
   자유롭다. 킷은 어느 모델인지 밝히지 않았다.
3. **무료로 인용 가능한 절차 규정 4 건을 확보**했다 — Google 2 · Microsoft 2. ISO 는 여전히
   확인 실패다 (유료이고, `iso.org` 는 이 환경에서 5.5KB 스텁만 응답한다).

## 리서치 소스

- Codex 위임 1 회 (MODE=research, read-only, foreground, 검색 하드캡 20). rollout
  `turn_aborted` 0 건. DITA `<taskbody>` 모델이 킷 인용과 다를 수 있다는 것을 지적해 왔고,
  직접 확인한 결과 **두 모델이 존재**한다는 것이 원인이었다.
- 인용 9 건은 전부 세션 로컬 조회로 대조했다. 이번 사이클은 직전 사이클들이 축적한 **검증 함정
  4 종**(엔티티 · 공백 정규화 · SPA · PDF)을 모두 적용한 정규화 대조기를 썼다. 그 덕에
  Google `"State the action first and the result second"` 인용이 `raw=miss norm=HIT` 로
  잡혔다 — raw 대조만 했으면 확인 실패로 잘못 기록했을 것이다.

## 범위 경계

- 카테고리는 `procedure-standards` 하나.
- **ISO 26514·26515 의 유료 전문을 추정으로 채우지 않는다.** 공개 범위에서 본 것만 쓰고
  나머지는 확인 실패로 남긴다.
- `verify` 를 모든 스텝에 요구하는 킷의 강화 규칙은 **바꾸지 않는다.** 이번 사이클은 그것이
  표준을 넘어선 선택이라는 사실의 근거를 더 단단히 할 뿐이다.
- `docs/howto/drafts/SKILL.md` 는 설계 시점 스냅샷이라 고치지 않는다.
- `.claude/worktrees/` 와 `result.json` 은 다른 세션 소유다. `main` 이 그 워크트리에
  체크아웃되어 있으므로 이 저장소에서 `main` 을 체크아웃하지 않는다. 기준은 `origin/main`.
- diff-scope baseline: 계약 작성 시점, 이 계약 파일 1 행 외 **0 행**.

## GAP 분석

| 대상 파일 | 현재 상태 (Read 증거) | 처리 |
| --- | --- | --- |
| `docs/howto/procedure-standards.md` | 부재 | 신규 생성 (AR-01) |
| `howto-kit/references/step-contract.md` | `:74` `<taskbody>` 모델을 인용하며 **어느 모델인지 미명시** | strict 명시 + 두 모델 존재 서술 (SK-01) |
| `howto-kit/skills/howto/SKILL.md` | `:81` `<cmd>` 인용 | 조회일 갱신 + 정본 포인터 (SK-02) |
| `docs/howto/design-brief.md` | `:401` §11-2 ISO 확인 실패 | 현행 유지 확인 + 정본 포인터 (AR-02) |
| `howto-kit/references/provenance-notes.md` | §1~8 | ISO · verification 규정 확인 실패 추가 (ER-03) |
| `docs/howto-kit/`, `docs/index.html` | 6 면 | 미러 신규 + 등록 (AR-03~05) |

## 회귀 게이트

이 스프린트의 위험은 **표준을 근거로 킷 규칙을 약화시키는 것**이다. DITA 가 `<stepresult>` 를
매 스텝에 쓰지 말라고 하지만 킷은 `verify` 를 필수로 둔다. ER-02 가 그 강화가 유지되는지 잰다.

## Skill

- [ ] SK-01: `step-contract.md` 의 `<taskbody>` 인용이 **strict task model** 임을 명시하고 두 모델이 존재한다는 사실을 담는다 [exact] (측정: `awk '/^## 절차 전체 골격/{f=1;print;next} f&&/^## /{exit} f' howto-kit/references/step-contract.md` 로 절을 추출한 뒤 — `strict` 와 `two task models` 가 각각 1 회 이상. **awk 범위형을 쓰지 않는다**)
- [ ] SK-02: `skills/howto/SKILL.md` 의 DITA 인용에 조회일과 정본 포인터가 붙는다 [exact] (측정: `grep -n 'should not be more than one sentence' -A 2 howto-kit/skills/howto/SKILL.md` 결과에 `2026-09-10` 과 `procedure-standards.md` 가 각각 등장)
- [ ] SK-03: `verify` 필수 규칙의 근거 서술이 **유지되고 강화 사실이 명시**된다 — 표준을 넘어선 선택임을 감추지 않는다 [structural] (측정: `step-contract.md` 의 `verify` 절에 `강화` 토큰과 `stepresult` 인용이 모두 남아 있다)

## Script

- [ ] SC-01: CI validate job 의 python 검사 8 종이 전부 exit 0 [exact, enumerated] — `scripts/validate-plugin.py`, `scripts/sync-evals.py --check-only`, `scripts/sync-docs.py --check-only`, `scripts/sync-orchestrator.py --check-only`, `scripts/run-evals.py --verbose`, `scripts/check-contrast-claims.py`, `scripts/check-docs-links.py`, `scripts/check-stale-values.py` (측정: 8 개를 각각 실행해 exit code 를 표로 인용. 음성 대조: `docs/index.html` 등록을 빼면 `check-docs-links.py` 가 FAIL 한다)
- [ ] SC-02: `bash howto-kit/evals/run-evals.sh` 가 exit 0 이고 `pass=12 fail=0` 이다 [exact] (측정: 해당 명령 실행 후 `pass=` 값 인용. 이 스프린트는 게이트·픽스처를 건드리지 않으므로 직전 값이 유지돼야 한다)
- [ ] SC-03: `node scripts/check-docs-a11y.js docs/howto-kit/procedure-standards.html` 이 exit 0 [exact] (측정: 해당 명령 실행. 음성 대조: `--text3` 를 `#7A6F64` 로 낮추면 대비 미달로 FAIL 한다)

## Error

- [ ] ER-01: 확정 인용 각각에 **출처 URL 과 조회일**이 붙는다 [exact, enumerated] — DITA `<cmd>`, DITA `<stepresult>`, DITA 두 모델, Google 한 스텝 한 동작, Google 결과 순서, Microsoft 번호 목록, Microsoft 명령형 (측정: `docs/howto/procedure-standards.md` 의 인용 표에서 각 행의 출처 열이 비어 있지 않은지 **개별로** 확인하고, `2026-09-10` 이 문서에 등장)
- [ ] ER-02: 킷이 `verify` 를 **표준보다 강하게** 요구한다는 사실이 문서에 명시된다 — 표준 인용으로 규칙을 약화시키지 않았다 [exact] (측정: `docs/howto/procedure-standards.md` 에 `should not be used for every step` 인용과 `강화` 토큰이 모두 등장하고, 킷이 그 권고를 따르지 않는 이유가 서술된다)
- [ ] ER-03: ISO 세부 조항과 스타일 가이드의 verification 규정이 리터럴 `확인 실패` 로 원장에 남고 시도 URL 이 나열된다 [exact, enumerated] (측정: `howto-kit/references/provenance-notes.md` 에 `ISO` 항목과 `verification` 항목이 각각 리터럴 `확인 실패` 와 함께 등장하고, 시도 URL 이 각각 1 개 이상)
- [ ] ER-04: 검증 함정 4 종을 적용한 대조기가 이번 사이클에서 **실제로 값을 했다**는 실측이 남는다 [exact] (측정: `docs/howto/procedure-standards.md` 에 `raw=miss` 와 `norm=HIT` 가 모두 등장하고 어느 인용에서 그랬는지 명시된다)

## Architecture

- [ ] AR-01: 신규 리서치 문서가 `docs/howto/procedure-standards.md` 경로에 존재한다 [exact] (측정: `test -f docs/howto/procedure-standards.md`)
- [ ] AR-02: 리서치 문서 6 종이 `docs/howto/` 에 전부 존재한다 [exact, enumerated] — `deep-links.md`, `ui-anchoring.md`, `branch-catalog.md`, `deprecation-policy.md`, `changelog-feeds.md`, `procedure-standards.md` (측정: 6 개 파일 각각에 `test -f` 를 실행해 표로 인용한다. 상위 glob 하나로 뭉뚱그리지 않는다)
- [ ] AR-03: HTML 미러 `docs/howto-kit/procedure-standards.html` 이 존재하고 `docs/index.html` 의 `pages` 배열과 `getIcon()` 양쪽에 **동일한 id** 로 등록된다 [exact, enumerated] (측정: 파일 존재 + `grep -c "howto-procedure-standards" docs/index.html` 가 2 이상이며 그중 하나는 `file:` 항목, 하나는 `getIcon` 매핑임을 각각 확인)
- [ ] AR-04: HTML 미러가 howto-kit accent 토큰과 공용 대비 토큰을 규약대로 쓴다 [exact, enumerated] — dark `--accent:#F59E0B` · light `--accent:#B45309` · dark `--text3:#948779` · light `--text3:#656C7A` · `localStorage` 키 `dk-theme` (측정: 5 개 리터럴을 각각 `grep -c` 로 확인, 전부 1 이상)
- [ ] AR-05: HTML 미러가 400 줄 이상이고 **외부 리소스 로드**가 0 건이다 [exact] (측정: `wc -l` 가 400 이상. 외부 로드는 `grep -cE '<link[^>]+rel="stylesheet"[^>]+https?://|<script[^>]+src="https?://|@import[^;]*https?://|url\(https?://'` 가 0. 본문 인용의 `<a href="https://...">` 출처 링크는 제외한다)
- [ ] AR-06: 변경 범위가 선언한 경로에 정확히 일치한다 [exact, enumerated] (Given: 이번 스프린트의 커밋이 완료된 후. 측정: `git diff --name-only origin/main...HEAD -- docs howto-kit .harness ':(exclude).claude/worktrees' ':(exclude)result.json'` 의 결과 집합이 `git diff --name-only origin/main...HEAD` 전체 집합과 **정확히 일치**한다)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수. 판정 권위는 validate-plugin V6 상태기계다 (측정: `python3 scripts/validate-plugin.py --check=code-fence`)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 금지 (측정: `python3 scripts/validate-plugin.py`)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — HTML 미러는 `docs/howto-kit/deprecation-policy.html` 의 토큰 블록·테마 토글 구조를 재사용한다

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 — N/A (이 세션·평가 환경에 IDE 진단 MCP 가 없고 `project.yaml` 의 `commands.lint` 가 `null` 이다. 대체 검증은 AP-03/04 의 validate-plugin 이 수행한다)
- [ ] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개 — N/A (플러그인 모노레포. SC-03 의 a11y 게이트가 렌더 검증을 대신한다)
