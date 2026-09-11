---
feature: "howto-kaizen 1 사이클 — G4 주장 탐지 정밀화 · 미확정 원장 인덱스 동기화"
slug: howto-kaizen-g4-precision
created: "2026-09-10 14:20"
complexity: "복잡"
conditions: 24
status: done
owner_session: 4d264694-eb0e-4e84-801f-52b2db804772
conditions_digest: sha256:bcf7e7535ec1a339
locked_at: "2026-09-10 14:30"
---

## 배경

`/howto-kaizen` 첫 사이클. 리서치 6 종이 방금 섰으므로 카이젠이 읽을 입력이 처음으로 갖춰졌다.

**Step 0 트리거 3 종이 전부 성립**했다 — (a) `docs/howto/` 에 6 커밋의 새 반영분 (b) 원장이
4 절에서 9 절로 확장 (c) 게이트가 놓친 실패 사례가 실측으로 잡힘.

**Step 1 baseline**: `validate-plugin.py howto-kit` exit 0 · `run-evals.sh` `EVALS total=12 pass=12 fail=0`.

**Step 2 대상 2 surface** (관심사 기준):

### Surface A — G4 주장 탐지 정밀도

직전 스프린트의 QA 가 잔여 오탐을 지적했다. 실측 매트릭스로 원인을 좁힌 결과 **토큰 문제가
아니라 스캔 범위 문제**였다. 게이트가 `- 확인:` 줄까지 주장으로 센다. 그 줄은 **제품이 화면에
띄우는 문구를 관측해 적는 자리**이므로, 거기 있는 "삭제 예정" 은 저자의 주장이 아니라 근거다.

현재 상태 실측 (7 케이스):

```text
fp-retention  (데이터 보존 안내)  FAIL  ← 오탐
pos-종료예정  (근거 없는 주장)    PASS  ← 미탐
```

### Surface B — 미확정 원장 인덱스 동기화

원장이 **4 절 → 9 절**로 늘었는데 인덱스 두 곳이 옛 3 항목만 말한다.
`howto-kit/README.md` 와 `docs/howto-kit/overview.html` 다. 원장이 커질수록 인덱스가
축소 보고하면 "이 킷이 사실로 말하지 않는 것" 의 실제 크기를 감춘다.

## 리서치 소스

외부 리서치 없음 — 이번 사이클은 **직전 6 사이클이 남긴 실측**이 입력이다.

- QA 잔여 오탐 지적: `.harness/sprint-feedback-howto-research-deprecation-policy.md`
- 원인 규명: 이 세션에서 7 케이스 매트릭스를 3 개 후보안에 대해 실행

## 범위 경계

- 카이젠 surface 는 **2 개**다 (A · B). 그 밖의 킷 규칙은 건드리지 않는다.
- **게이트 출력 토큰(`G4_DEPRECATION`)을 바꾸지 않는다.** evals assertion 과 소비면이 그
  문자열에 묶여 있다. 라벨이 좁다는 지적은 유효하나 이번 범위 밖이다.
- `[추정]` 탐지는 `확인:` 줄에서도 유지한다 — G6 의 등급 비율 계산 대상이다. 이번 변경은
  **deprecation 주장 탐지에만** 적용한다.
- `.gitignore` 추가는 카이젠 surface 가 아니라 **레포 하우스키핑**이다. 별도 조건(AR-04)으로
  두고 surface 수에 세지 않는다.
- `.claude/worktrees/` 의 bambu 워크트리는 **삭제하지 않는다.** 다른 세션 소유이며 작업 완료
  상태(PR #45 머지본, clean)일 뿐 제거 권한은 이 세션에 없다.
- diff-scope baseline: 계약 작성 시점, 이 계약 파일 1 행 외 **0 행**.

## GAP 분석

| 대상 파일 | 현재 상태 (실측 증거) | 처리 |
| --- | --- | --- |
| `howto-kit/scripts/howto-gate.sh` | `:83-86` 캐치올이 모든 줄에서 `dep_claim` 을 세움 → `확인:` 오탐 | 스캔 제외 + `종료 예정` 토큰 (SK-01·SK-02) |
| `howto-kit/evals/fixtures/` | 오탐 대조 2 종·미탐 양성 1 종 픽스처 없음 | 3 종 추가 (SC-02) |
| `howto-kit/evals/evals.json` | 12 케이스 | 3 케이스 추가 → 15 (SC-03) |
| `howto-kit/README.md` | 미확정 3 항목만 서술 (원장은 9 절) | 9 절 기준으로 갱신 (SK-03) |
| `docs/howto-kit/overview.html` | 표에 확인 실패 4 행 (원장은 9 절) | 소스와 짝으로 갱신 (AR-02) |
| `.gitignore` | `worktrees` 항목 없음 | 워크트리·CLI 산출물 추가 (AR-04) |

## 회귀 게이트

게이트를 손대는 사이클이다. **양성·음성 대조를 둘 다** 요구한다 (howto-kaizen Gotcha 1).
토큰을 좁히면 미탐이 남고 넓히면 오탐이 는다. SC-02 가 7 케이스로 그 균형을 잰다.
그리고 **zsh·bash 양쪽에서 돌린다** (Gotcha 2 — 실측 2026-09-08 에 zsh 에서만 새는 결함이 있었다).

## Skill

- [ ] SK-01: 게이트가 `- 확인:` 줄을 **deprecation 주장 탐지에서 제외**한다 [exact] (측정: `grep -n 'dep_claim = 1' howto-kit/scripts/howto-gate.sh` 결과 중 캐치올 블록의 줄에 `확인` 제외 조건이 포함된다. 그리고 그 이유가 주석으로 남아 있다)
- [ ] SK-02: `HOWTO_DEP` 에 `종료 예정` 이 추가되고 `삭제` · `종료` 단독은 없다 [exact] (측정: `grep -o "HOWTO_DEP='[^']*'" howto-kit/scripts/howto-gate.sh` 출력에 `종료 예정` 포함, 그리고 파이프 구분 항목 중 정확히 `삭제` 이거나 정확히 `종료` 인 것이 0)
- [ ] SK-03: `README.md` 의 "이 킷이 사실로 말하지 않는 것" 절이 **원장 절 수를 정확히** 말한다 [exact] (측정: `awk '/^## 이 킷이 사실로 말하지 않는 것/{f=1;print;next} f&&/^## /{exit} f' howto-kit/README.md` 로 절을 추출한 뒤 `9` 가 등장하고, 옛 서술인 "체크리스트 방법론의 1 차 출처, 변경 로그 피드 3 건(Firebase · Stripe · Azure updates), 이름 충돌 검사는" 문자열이 0 건. **awk 범위형을 쓰지 않는다**)

## Script

- [ ] SC-01: CI validate job 의 python 검사 8 종이 전부 exit 0 [exact, enumerated] — `scripts/validate-plugin.py`, `scripts/sync-evals.py --check-only`, `scripts/sync-docs.py --check-only`, `scripts/sync-orchestrator.py --check-only`, `scripts/run-evals.py --verbose`, `scripts/check-contrast-claims.py`, `scripts/check-docs-links.py`, `scripts/check-stale-values.py` (측정: 8 개를 각각 실행해 exit code 를 표로 인용. 음성 대조: `docs/index.html` 등록을 빼면 `check-docs-links.py` 가 FAIL 한다)
- [ ] SC-02: 게이트 변경이 **7 케이스 매트릭스**를 모두 만족한다 [exact, enumerated] — 오탐 대조 3 종(`데이터 보존 안내` · `설치 완료 서술` · `계정 삭제 액션`)은 `G4_DEPRECATION PASS`, 양성 3 종(`삭제 예정` · `종료 예정` · `폐지 예정` 근거 없음)은 `FAIL`, 출처 뒷받침 1 종은 `PASS` (측정: 7 픽스처를 `. howto-kit/scripts/howto-gate.sh` 후 `howto_gate` 로 각각 실행해 G4 줄을 그대로 인용. 신규 픽스처는 `howto-kit/evals/fixtures/` 에 커밋한다)
- [ ] SC-03: `sh howto-kit/evals/run-evals.sh` 가 `EVALS_PASS` 이고 케이스가 **15** 다 [exact] (측정: 해당 명령 실행 후 `EVALS total=` 줄 인용. 신규 3 케이스가 등록됐으므로 12 → 15)
- [ ] SC-04: 게이트가 **zsh 와 bash 양쪽에서 같은 출력**을 낸다 [exact] (측정: 대표 픽스처 1 종에 대해 `zsh -c` 와 `bash -c` 로 각각 `howto_gate` 를 실행해 G1~G6 전체 출력이 동일한지 `diff` 로 확인. 음성 대조: `set -- $var` 형태를 넣으면 zsh 에서만 결과가 갈린다 — 2026-09-08 실측 결함)

## Error

- [ ] ER-01: 오탐의 **원인이 토큰이 아니라 스캔 범위**였다는 실측이 문서에 남는다 [exact] (측정: `docs/howto/deprecation-policy.md` 의 잔여 오탐 절이 갱신되어 `확인:` 줄 제외가 해법이었음을 서술하고, 수정 전 `FAIL` / 수정 후 `PASS` 가 함께 인용된다)
- [ ] ER-02: `확인:` 줄을 제외해도 **양성 케이스가 여전히 잡힌다**는 근거가 명시된다 — 구멍을 만들지 않았다 [structural] (측정: 같은 절에 주장이 스텝 헤더에 오면 여전히 탐지된다는 서술이 있고, SC-02 의 양성 3 종이 그 증거로 인용된다)
- [ ] ER-03: 원장 9 절이 **줄어들지 않았다** — 확인 실패를 조용히 지우지 않았다 (howto-kaizen Gotcha 9) [exact] (측정: `grep -c '^## [0-9]\.' howto-kit/references/provenance-notes.md` 가 9 이상)
- [ ] ER-04: `overview.html` 의 미확정 표가 소스(`provenance-notes.md`)와 **어긋나지 않는다** [structural] (측정: 표가 9 절 전부를 열거하거나, 대표 항목 + "전체는 원장 참조" 포인터를 갖는다. 원장보다 적은 수를 전부인 것처럼 말하지 않는다)

## Architecture

- [ ] AR-01: 신규 픽스처 3 종이 `howto-kit/evals/fixtures/` 에 존재한다 [exact, enumerated] — 데이터 보존 오탐 대조 · 설치 완료 오탐 대조 · `종료 예정` 양성 (측정: 3 파일 각각에 `test -f` 를 실행해 표로 인용)
- [ ] AR-02: `docs/howto-kit/overview.html` 이 `README.md` 와 **짝으로** 갱신된다 — 생성물만 고치거나 소스만 고치지 않았다 [exact] (측정: `git diff --name-only origin/main...HEAD` 에 두 파일이 **모두** 있다)
- [ ] AR-03: 게이트 마커 규약이 안 바뀌었으므로 `step-contract.md` 는 변경되지 않는다 (howto-kaizen Gotcha 3) [exact] (측정: `git diff --name-only origin/main...HEAD -- howto-kit/references/step-contract.md` 가 비어 있다)
- [ ] AR-04: `.gitignore` 에 워크트리 디렉토리와 Bambu CLI 산출물이 추가되고, **추적 중이던 파일이 0** 이다 [exact, enumerated] — `.claude/worktrees/`, `result.json` (측정: 두 항목이 `.gitignore` 에 있고, `git ls-files .claude/worktrees result.json` 출력이 비어 있다. 추적 중인 파일을 ignore 로 숨기는 것이 아님을 이 명령이 보인다)
- [ ] AR-05: 변경 범위가 선언한 경로에 정확히 일치한다 [exact, enumerated] (Given: 이번 스프린트의 커밋이 완료된 후. 측정: `git diff --name-only origin/main...HEAD -- howto-kit docs .harness .gitignore ':(exclude).claude/worktrees' ':(exclude)result.json'` 의 결과 집합이 `git diff --name-only origin/main...HEAD` 전체 집합과 **정확히 일치**한다)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수. 판정 권위는 validate-plugin V6 상태기계다 (측정: `python3 scripts/validate-plugin.py --check=code-fence`)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 금지 (측정: `python3 scripts/validate-plugin.py`)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 신규 픽스처는 기존 `pass-g4-*` 형식(마커·필드 순서)을 그대로 따르고 새 포맷을 발명하지 않는다

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0개. 게이트도 함께 — `sh -n howto-kit/scripts/howto-gate.sh`
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 — N/A (이 세션·평가 환경에 IDE 진단 MCP 가 없고 `project.yaml` 의 `commands.lint` 가 `null` 이다. 대체 검증은 DG-01 의 `sh -n` 과 SC-04 의 이중 셸 실행이 수행한다)
- [ ] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개 — N/A (플러그인 모노레포. SC-02 의 게이트 실행이 런타임 검증을 대신한다)
