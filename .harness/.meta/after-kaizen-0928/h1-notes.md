# h1 — harness 계약 규칙 · 검사 도구 약점 (2026-09-28)

계약 `.harness/sprint-contract-after-0928-harness-checks.md` (36 조건, 봉인 `455c55aaa06642fa` · 측정 `d6e75fb37b35d6bd`).
가지 `chore/ak3-h1`, 시작 판 `95508d9`. QA 판정과 `status: done` 전환은 이 묶음에서 하지 않았다.

## 항목별 결과

| 항목 | 결과 | 근거 (명령 출력) |
| --- | --- | --- |
| B1 | 고침 — 머리 읽개 셋이 따옴표와 줄 끝 주석(빈칸 · 탭 뒤의 `#`)을 벗긴다. `abc#def` 는 값 그대로 | `m-fm.sh` → `ng=0 total=42` (전 `ng=24`). 공용 측정 시험에 `F1-` ~ `F7-` 을 더했다: 새 판 `pass_F=7`, 옛 `fm_get` 사본 `pass_F=3 fail_F=4` |
| B2 | 고침 — `harness/scripts/check-superseded.sh` 와 시험, CI 두 단계 | `m-superseded.sh` → A `rc=1 checked=4 violations=3` · B `rc=0` · 없는 폴더 `rc=2` · 레포 `checked=3 violations=0` |
| B3 | 고침 — sprint-contract Step 0.5 에 superseded 로 바꾸는 절차 · 확인 명령 | `m-docs.sh` 의 `skill-0.5` 세 값 1 이상 |
| B4 | 고침 — 원문 덩어리 끝을 `판정 표와 두 경우는` 표지 줄 앞으로. 표지가 없으면 `CANON_MISSING` · 2 | `m-cause.sh` → b · c 가 `rc=1 mismatch=2`, e 가 `rc=2`. 시험 `scripts/test-check-cause-table-copies.py` 다섯 경우 통과 |
| B7 | 고침 — 접근성 검사가 `themeToggle` 단추도 잰다. visual-styles 단추 63x33 → 63x48 (320 · 375 · 1280 모두 63x48) | `m-a11y.sh` → 네 쪽 `OK`, 임시 작은 단추 `FAIL btn=60x30`, `rc=1` |
| B8 | 고침 — Phase 상한 = 4 + (harness 를 뺀 킷 수), 5 번부터 마켓 목록 차례 | `m-phase.sh` → 킷을 더한 사본 `n=18 rc=0 slug=kaizen-phase18-foo`, 도움말 `1 ~ 17` 0 건 |
| B9 | 고침 — run-evals · sync-evals 대상을 마켓 목록에서 뽑고 빼는 킷은 `SKIP <킷> (<사유>)` | `m-evals.sh` → 새 킷이 둘 다에 잡히고 sync-evals 는 사례 없는 스킬로 `rc=1` |
| B22 | 고침 — 계약 형식 문서 §측정 관례 에 규칙 다섯, sprint-contract Gotchas 에 그 절 안내 | `m-docs.sh` 의 `schema-측정관례` 일곱 줄 · `skill-gotchas` 두 줄 모두 1 이상 |
| D2 | 고침 — `scripts/ci-local.sh` 가 CI 파일의 run 단계를 직접 읽는다. 준비 단계 다섯은 SKIP, 못 다루는 열쇠는 UNSUPPORTED · 1 | `m-cilocal.sh` → `steps=40 run=35 skip=5 unsupported=0`, 단계를 더한 사본에서 새 단계를 돈다. 옛 도구 파일은 손대지 않았다(지문 `59fe55125c0dbc77`) |
| D4 | 결정 — 변환 스크립트는 레포에 두지 않는다 | 아래 절 |

## D4 — 변환 스크립트는 레포에 두지 않는다

- D4 결정: 새 쪽 · 다시 쓴 쪽을 만든 변환 스크립트(세션 임시 폴더 `dcb/gen` · `dr2/gen`)는 레포에 두지 않는다.
- 근거 1 — 같은 결과를 못 낸다. `bash .harness/.meta/after-0928-harness-checks/m-d4.sh <W> 95508d9 <scratch>/dcb/gen <scratch>/dr2/gen` 로
  판 `95508d9` 원본에 다시 돌린 결과 `same=6 total=21` 이다. 나머지 15 쪽은 그 뒤 원본이 바뀌었거나(코드 울타리 언어 표기) 스크립트 결함 때문에 다르다.
- 근거 2 — 결함이 있다. 원본의 `<!-- markdownlint-disable … -->` 주석을 본문 글로 옮긴다 (`docs/tone-kit/locale-korean.html` 차이 2 줄).
  레포에 들이면 다음 사람이 이 결함째로 쪽을 다시 만든다.
- 다시 만드는 길: 원본이 바뀌면 레포 `.claude/skills/docs-site` 스킬로 쪽을 고치고, `python3 scripts/detect-docs-drift.py` 가 원본 → 쪽 짝의 어긋남을 알린다.

## 교차 진단 반영 (봉인 전)

- `m-scope.sh` 가 서명 줄을 모델 이름 한 벌과 글자로 맞대어, 모델이 바뀌면 AR-05 가 늘 FAIL 한다는 지적 — 서명 판정을
  `Claude <이름> <noreply@anthropic.com>` 모양 한 줄로 바꿨다. 같은 규칙을 §측정 관례 셋째 줄에도 적었다.
- 기능 조건 28 개로 가이드 상한 20 을 넘지만 한 묶음으로 갔다 — 나누면 CI 파일 · 종료 코드 표 · 계약 형식 문서를 두 가지에서 따로 고쳐 부딪힌다.

## 킷 버전 판단

- harness: 올린다 — patch (0.16.0 → 0.16.1). qa-evaluator · sprint-contract · 계약 형식 문서의 동작(머리 값 읽기)이 바뀌고 새 확인 스크립트가 들어간다. 기능 추가지만 규약 뜻은 그대로라 patch 로 본다.
- design-kit: 올리지 않는다 — `docs/` 쪽만 바뀌었다(킷 폴더 밖).
- 그 밖 킷: 바뀐 것 없음. `scripts/` · `.github/` 는 킷 밖이다.
- 릴리스는 통합 가지에서 한 번에 한다(이 가지에서 `release.sh` 를 돌리지 않았다).

## 남은 것

- QA 판정: qa-evaluator 로 이 계약을 평가해야 한다 — 이 묶음의 구현자는 판정을 하지 않는다는 지시를 따랐다.
- 옛 로컬 CI 도구 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` 는 그대로 있다 — 그 경로 · 지문을 적은 봉인 계약이 있어 지우거나 고칠 수 없다. 앞으로의 계약은 `scripts/ci-local.sh` 를 쓰면 된다.
- 카이젠 오케스트레이터 문서(`.claude/skills/kaizen-orchestrator/SKILL.md` · `docs/process/kaizen-flow.html` 등)는 여전히 「Phase 1~17」 이라 적는다. 지금 킷 수로는 맞지만 킷이 늘면 손으로 고쳐야 한다 — 이 계약 범위 밖이라 두었다.
- 로컬 CI 새 도구는 `npm ci` 같은 준비 단계를 돌리지 않는다. 새 작업 폴더에서는 `npm ci` 를 먼저 해야 playwright 단계가 돈다.
