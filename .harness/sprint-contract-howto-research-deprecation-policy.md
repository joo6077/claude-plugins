---
feature: "howto-research 5 사이클 — deprecation-policy 확정 · G4 false negative 수정"
slug: howto-research-deprecation-policy
created: "2026-09-10 12:10"
complexity: "복잡"
conditions: 25
status: active
owner_session: 4d264694-eb0e-4e84-801f-52b2db804772
conditions_digest: sha256:bd8eb381501716ef
locked_at: "2026-09-10 11:43"
---

## 배경

`/howto-research` 다섯 번째 사이클. 카테고리는 `deprecation-policy` 하나만 다룬다 (Gotcha 4).

설계 브리프 §11-4 가 이 항목을 확인 실패로 남겨 뒀다 — *"Google Cloud 정책 문서 안에서
`not recommended`/`sunset`/`removed` 를 각각 별도 공식 용어로 정의한 문장과 Apple 의 동등한
정의를 확인하지 못했다. 3 단계 구분은 AWS·Amazon SP-API 근거로 세웠다."*

이번 사이클의 결과는 셋이다.

1. **기존 4 인용을 전부 재확인**했고, Google Cloud 가 실제로 `deprecated → shutdown` 전이를
   문장으로 정의한다는 것을 확인했다 — *"After this period of time, the service is scheduled
   for shutdown."*
2. **통지 기간의 성격이 벤더마다 다르다**는 것을 확인했다. Google Cloud 는 **약관상 최소 12 개월
   통지**를 약속하지만(*"Google will notify Customer at least 12 months before"*), AWS 는
   *"typically 12 months"* 로 **관행 서술**일 뿐이다. 절차 문서가 둘을 같은 강도로 쓰면 안 된다.
3. **G4 게이트의 false negative 를 발견해 고친다.** Google Cloud 한국어 문서는 removed 를
   **`삭제`** 로 옮기는데, 게이트 토큰 목록에 그 계열이 없어 **근거 없는 "삭제 예정" 주장이
   그대로 통과**했다. 실측 3 방향 대조로 확인했다.

Apple 은 개별 API 종료 공지만 있고 **동등한 일반 lifecycle 정책은 확인 실패**다.

## 리서치 소스

- Codex 위임 1 회 (MODE=research, read-only, foreground, 검색 하드캡 20). rollout
  `turn_aborted` 0 건.
- 인용 8 건은 전부 세션 로컬 조회로 **응답 본문에서 직접 대조**했다. 이때 직전 사이클이 남긴
  **HTML 엔티티 디코드** 절차가 실제로 값을 했다 — Google Cloud deprecations 인용이
  `raw=miss decoded=HIT` 였다.

## 범위 경계

- 카테고리는 `deprecation-policy` 하나. `procedure-standards` 는 이번 스프린트에서 만들지 않는다.
- **게이트 토큰은 좁은 형태(`삭제 예정|삭제가 예정`)만 추가한다.** `삭제` 단독 추가는 정상
  절차("계정을 삭제한다")를 오탐하는 것이 실측됐다 — `unsourced_claims=2`.
- `docs/howto/drafts/SKILL.md` 는 설계 시점 스냅샷이라 고치지 않는다.
- `.claude/worktrees/` 와 `result.json` 은 다른 세션 소유다. **`main` 이 그 워크트리에
  체크아웃되어 있으므로 이 저장소에서 `main` 을 체크아웃하지 않는다.** 기준은 `origin/main`.
- diff-scope baseline: 계약 작성 시점, 이 계약 파일 1 행 외 **0 행**.

## GAP 분석

| 대상 파일 | 현재 상태 (Read 증거) | 처리 |
| --- | --- | --- |
| `docs/howto/deprecation-policy.md` | 부재 | 신규 생성 (AR-01) |
| `howto-kit/scripts/howto-gate.sh` | `:21` `HOWTO_DEP` 에 `삭제` 계열 없음 | 좁은 토큰 추가 (SK-01) |
| `howto-kit/references/source-tiers.md` | `deprecation 3 단계` 절, 통지 기간 구분 없음 | 통지 강도 구분 + 한국어 매핑 (SK-02) |
| `docs/howto/design-brief.md` | `:391` 부근 §11-4 확인 실패 | 부분 해소 표기 + 정본 포인터 (AR-02) |
| `howto-kit/references/provenance-notes.md` | §1~7 | Apple 확인 실패 추가 (ER-03) |
| `docs/howto-kit/`, `docs/index.html` | 5 면 | 미러 신규 + 등록 (AR-03~05) |

## 회귀 게이트

게이트를 건드리는 스프린트이므로 **음성·양성 대조를 둘 다** 요구한다. 토큰을 넓히면 정상 절차가
깨지고, 안 넣으면 결함이 남는다. SC-02 가 그 둘을 동시에 잰다.

## Skill

- [ ] SK-01: `howto-gate.sh` 의 `HOWTO_DEP` 에 좁은 형태의 삭제 계열 토큰이 추가된다 — `삭제` 단독은 넣지 않는다 [exact] (측정: `grep -o "HOWTO_DEP='[^']*'" howto-kit/scripts/howto-gate.sh` 출력에 `삭제 예정` 이 포함되고, 파이프로 구분된 항목 중 정확히 `삭제` 인 것이 없다)
- [ ] SK-02: `source-tiers.md` 의 deprecation 절이 (a) 통지 기간의 **약속 vs 관행** 구분 (b) 한국어 공식 용어 매핑을 담는다 [exact, enumerated] (측정: `awk '/^## deprecation 3 단계/{f=1;print;next} f&&/^## /{exit} f' howto-kit/references/source-tiers.md` 로 절을 추출한 뒤 — `at least 12 months` 와 `typically 12 months` 가 각각 1 회 이상, 그리고 `지원 중단됨` 이 1 회 이상. **awk 범위형을 쓰지 않는다**)
- [ ] SK-03: 게이트와 `step-contract.md` 의 마커 정본 관계가 깨지지 않는다 — 토큰 변경이 마커 규약을 건드리지 않았다 [structural] (측정: `git diff --name-only origin/main...HEAD -- howto-kit/references/step-contract.md` 가 비어 있다)

## Script

- [ ] SC-01: CI validate job 의 python 검사 8 종이 전부 exit 0 [exact, enumerated] — `scripts/validate-plugin.py`, `scripts/sync-evals.py --check-only`, `scripts/sync-docs.py --check-only`, `scripts/sync-orchestrator.py --check-only`, `scripts/run-evals.py --verbose`, `scripts/check-contrast-claims.py`, `scripts/check-docs-links.py`, `scripts/check-stale-values.py` (측정: 8 개를 각각 실행해 exit code 를 표로 인용. 음성 대조: `docs/index.html` 등록을 빼면 `check-docs-links.py` 가 FAIL 한다)
- [ ] SC-02: 게이트 토큰 변경이 **3 방향 대조**를 모두 만족한다 [exact, enumerated] — (a) 근거 없는 `삭제 예정` 주장 → `G4_DEPRECATION FAIL` (b) 같은 주장 + 출처 뒷받침 → `PASS` (c) 정상 계정 삭제 절차 → `PASS` (측정: 세 픽스처를 만들어 `. howto-kit/scripts/howto-gate.sh` 후 `howto_gate <파일>` 을 각각 실행하고 G4 줄을 그대로 인용한다. 픽스처는 `howto-kit/evals/fixtures/` 에 커밋한다)
- [ ] SC-03: `bash howto-kit/evals/run-evals.sh` 가 exit 0 이고 기존 9 케이스가 전부 PASS 다 [exact] (측정: 해당 명령 실행 후 `pass=` 값 인용. 신규 픽스처를 evals 에 등록했다면 그 수만큼 늘어난 값이어야 한다)
- [ ] SC-04: `node scripts/check-docs-a11y.js docs/howto-kit/deprecation-policy.html` 이 exit 0 [exact] (측정: 해당 명령 실행. 음성 대조: `--text3` 를 `#7A6F64` 로 낮추면 대비 미달로 FAIL 한다)

## Error

- [ ] ER-01: 3 단계 각각에 **1 차 출처 인용**이 붙고 조회일이 표기된다 [exact, enumerated] — `deprecated`, `sunset/shutdown`, `removed` (측정: `docs/howto/deprecation-policy.md` 의 단계 표에서 각 행의 출처 열이 비어 있지 않고 `2026-09-10` 이 문서에 등장하는지 **개별로** 확인)
- [ ] ER-02: 통지 기간의 **약속과 관행이 구분**되어 서술된다 — 둘을 같은 강도로 쓰지 않는다 [exact] (측정: `docs/howto/deprecation-policy.md` 에 `at least 12 months` 와 `typically 12 months` 가 모두 등장하고, 전자가 약관상 약속·후자가 관행 서술로 구분되어 설명된다)
- [ ] ER-03: Apple 일반 lifecycle 정책 부재가 원장에 리터럴 `확인 실패` 로 남고 시도 URL 이 나열된다 [exact] (측정: `howto-kit/references/provenance-notes.md` 에 `Apple` 과 리터럴 `확인 실패` 가 같은 항목에 등장하고, 시도 URL 이 1 개 이상)
- [ ] ER-04: G4 의 **false negative 가 실측으로 문서화**된다 — 수정 전에는 근거 없는 주장이 통과했다는 사실 [exact] (측정: `docs/howto/deprecation-policy.md` 에 `unsourced_claims=0` 과 `unsourced_claims=1` 이 모두 등장하고, 전자가 수정 전 상태임이 서술된다)

## Architecture

- [ ] AR-01: 신규 리서치 문서가 `docs/howto/deprecation-policy.md` 경로에 존재한다 [exact] (측정: `test -f docs/howto/deprecation-policy.md`)
- [ ] AR-02: `design-brief.md` §11-4 가 부분 해소로 갱신되고 정본 포인터를 갖는다 [exact] (측정: `grep -c 'deprecation-policy.md' docs/howto/design-brief.md` 가 1 이상이고, §11 의 4 번 항목에 해소 표기가 있다)
- [ ] AR-03: HTML 미러 `docs/howto-kit/deprecation-policy.html` 이 존재하고 `docs/index.html` 의 `pages` 배열과 `getIcon()` 양쪽에 **동일한 id** 로 등록된다 [exact, enumerated] (측정: 파일 존재 + `grep -c "howto-deprecation-policy" docs/index.html` 가 2 이상이며 그중 하나는 `file:` 항목, 하나는 `getIcon` 매핑임을 각각 확인)
- [ ] AR-04: HTML 미러가 howto-kit accent 토큰과 공용 대비 토큰을 규약대로 쓴다 [exact, enumerated] — dark `--accent:#F59E0B` · light `--accent:#B45309` · dark `--text3:#948779` · light `--text3:#656C7A` · `localStorage` 키 `dk-theme` (측정: 5 개 리터럴을 각각 `grep -c` 로 확인, 전부 1 이상)
- [ ] AR-05: HTML 미러가 400 줄 이상이고 **외부 리소스 로드**가 0 건이다 [exact] (측정: `wc -l` 가 400 이상. 외부 로드는 `grep -cE '<link[^>]+rel="stylesheet"[^>]+https?://|<script[^>]+src="https?://|@import[^;]*https?://|url\(https?://'` 가 0. 본문 인용의 `<a href="https://...">` 출처 링크는 제외한다)
- [ ] AR-06: 변경 범위가 선언한 경로에 정확히 일치한다 [exact, enumerated] (Given: 이번 스프린트의 커밋이 완료된 후. 측정: `git diff --name-only origin/main...HEAD -- docs howto-kit .harness ':(exclude).claude/worktrees' ':(exclude)result.json'` 의 결과 집합이 `git diff --name-only origin/main...HEAD` 전체 집합과 **정확히 일치**한다)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수. 판정 권위는 validate-plugin V6 상태기계다 (측정: `python3 scripts/validate-plugin.py --check=code-fence`)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 금지 (측정: `python3 scripts/validate-plugin.py`)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — HTML 미러는 `docs/howto-kit/branch-catalog.html` 의 토큰 블록·테마 토글 구조를 재사용한다

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0개 (변경/생성 파일 대상). 게이트 스크립트도 함께 검사한다 — `sh -n howto-kit/scripts/howto-gate.sh`
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 — N/A (이 세션·평가 환경에 IDE 진단 MCP 가 없고 `project.yaml` 의 `commands.lint` 가 `null` 이다. 대체 검증은 DG-01 의 `sh -n` 과 AP-03/04 의 validate-plugin 이 수행한다)
- [ ] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개 — N/A (플러그인 모노레포. SC-02 의 게이트 실행과 SC-04 의 a11y 게이트가 런타임 검증을 대신한다)
