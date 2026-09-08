---
feature: "onboarding-kit 게이트 결함 3건 수정"
slug: onboarding-kit-gate-defects
created: "2026-09-08 16:05"
complexity: "복잡"
conditions: 21
status: done
owner_session: 0e3335f2-8d08-4e29-8a5d-01ec6b7ed620
conditions_digest: sha256:a0be77436880ad3e
locked_at: "2026-09-08 16:55"
---

## 배경

`docs/howto/design-brief.md` §2 가 지적한, `howto-kit` 신설과 **무관하게 지금 깨져 있는**
`onboarding-kit` 결함 3 건을 고친다. howto-kit 스프린트에서 의도적으로 분리했다.

| # | 결함 | 위치 |
| --- | --- | --- |
| (a) | evals 가 접미 없는 `[미검증]` 을 assert 하는데 SKILL.md 는 그 표기를 금지 | `evals.json:86-87` ↔ `SKILL.md:30` |
| (b) | Drift 스니펫의 `$STACK` 이 어디에도 정의되지 않아 G3 가 영구 no-op | `SKILL.md:213` · `SKILL.md:83-86` |
| (c) | G4 판정식이 영문 `[Dd]eprecat` 에 묶여 한국어 1 차 출처 근거를 인정 못 함 | `SKILL.md:92` |

**공통 전제 (헤더 1 회 선언)**

- CONTRACT_ROOT 는 워크트리 `.claude/worktrees/onboarding-gate-defects`, 브랜치 `fix/onboarding-kit-gate-defects` (main `4fb1382` 기준).
- 대상은 `onboarding-kit/skills/setup-guide/` 하위뿐이다. `howto-kit/` 과 `docs/` 는 건드리지 않는다.
- 게이트는 SKILL.md 코드 펜스에서 추출해 실행한다. 추출 명령(전 조건 공통):
  `awk '/^guide_gate\(\) \{/{p=1} p{print} p&&/^\}$/{exit}' onboarding-kit/skills/setup-guide/SKILL.md > /tmp/ob-gate.sh`
  이후 `<셸> -c ". /tmp/ob-gate.sh; guide_gate <파일> [스택]"` 으로 zsh·bash 양쪽 실행한다.
- "zsh·bash 양쪽" 조건은 두 출력이 `diff` 로 동일해야 PASS 다.
- 마커 임계 숫자는 `harness/docs/guides/qa-evaluation-guide.md` 가 정본이며 이 킷에서 재정의하지 않는다.

## 리서치 소스

- `docs/howto/design-brief.md` §2 "onboarding-kit 처리" — 결함 3 건의 원 지적
- `onboarding-kit/skills/setup-guide/SKILL.md:50-107` — `guide_gate()` 현행 구현
- `onboarding-kit/skills/setup-guide/references/format-checklist.md:49` — Deprecated 박스 근거 표기 규약
- `howto-kit/scripts/howto-gate.sh` — 같은 결함을 이미 고친 선례 (G3 미선언 = FAIL, G4 한국어 토큰)

## GAP 분석

베이스라인 (2026-09-08, 계약 작성 시점, 현행 게이트를 배포 예제에 실행):

```text
$ guide_gate docs/onboarding-kit/examples/fcm-ios-setup-guide.md flutter     (bash == zsh)
G1_LEDGER PASS steps=8 ledger=8
G2_MARKER PASS bare=0 invalid=0 env=0
G3_STACKMIX PASS stack=flutter swift_fence=0
G4_DEPRECATION PASS unsourced_boxes=0
GATE_PASS

$ guide_gate docs/onboarding-kit/examples/fcm-ios-setup-guide.md             (스택 미지정 · bash == zsh)
G1_LEDGER PASS steps=8 ledger=8
G2_MARKER PASS bare=0 invalid=0 env=0
G3_STACKMIX PASS stack=unset swift_fence=0
G4_DEPRECATION PASS unsourced_boxes=0
GATE_PASS
```

두 번째 블록이 결함 (b) 의 실물이다 — 스택을 안 줬는데 `G3_STACKMIX PASS stack=unset`. 판정 불가를
통과로 흘린다. `howto-kit` 의 G3 는 같은 상황에서 `FAIL no_target_declared` 를 낸다.

소비면 (Step 2.5):
- `evals/evals.json` — 마커 규칙의 소비자 (결함 a 의 반대편)
- `references/format-checklist.md:49` — G4 가 인정하는 근거 표기의 **산문 정본**. 코드만 고치면 산문이 옛 규칙으로 남는다
- `docs/onboarding-kit/examples/fcm-ios-setup-guide.md` — 게이트의 소비자. 변경 후에도 같은 판정이어야 한다
- `docs/onboarding-kit/fcm-ios-example.html` · `search-strategy.html` · `format-checklist.html` — 게이트를 이름으로 언급하는 HTML 미러. **이번 스프린트 비범위** (docs-site 재생성 사이클)

## 범위 경계

- **비범위**: `howto-kit/` · `docs/` 전체 · SKILL.md 의 게이트 외 Gotchas·Phase 서술 개편 · 마커 임계 숫자.
- diff-scope 베이스라인은 `4fb1382` (이 브랜치의 유일한 조상, 계약 시점 `4fb1382..HEAD` 경로 0 건).
  워크트리는 이 세션 전용이라 동시 작성자 제외 pathspec 이 필요 없다.
- 허용목록에 **슬러그 산출물 3 종**(계약·피드백·사이드카)을 전부 넣는다 — 직전 스프린트에서
  사이드카 누락으로 REJECT 된 자기참조 결함의 재발 방지.
- 커버리지 해소: SC-01·SC-02 — 산문의 픽스처 파일명과 측정의 파일명이 같은 백틱 표기다.

## 회귀 게이트

`python3 scripts/validate-plugin.py`(전 킷) 와 `python3 scripts/sync-docs.py --check-only` 가
이 변경으로 새로 FAIL 하지 않아야 한다 (SC-04 · SC-05). evals 디렉토리에 fixtures 가 생기면
README `AUTO:evals` 블록이 바뀌므로 sync-docs 를 실행해야 한다.

## Skill

- [ ] SK-01: `onboarding-kit/skills/setup-guide/evals/evals.json` 의 `source-ledger-per-step` 케이스 assertion
      문자열 전체에 접미 없는 `[미검증]` 이 0 건이고, `[미검증:ENV]` 와 `[미검증:INVALID]` 가 각각 1 회 이상
      등장한다 [exact, enumerated]
      (측정: `python3 -c` 로 json 로드 → 해당 케이스 assertions 를 `\n` 으로 join → 정규식
      `\[미검증\](?!:)` 매치 0, `[미검증:ENV]` ≥1, `[미검증:INVALID]` ≥1)
- [ ] SK-02: 같은 evals 의 `deprecation-claim-fidelity` 케이스에서 `cited_source_contains_deprecation_keyword`
      assertion 이 허용 키워드 집합을 인라인 열거하고, 그 집합에 `지원 종료` 가 포함된다 [exact]
      (측정: 해당 assertion 문자열에 `지원 종료` 부분문자열 존재)
- [ ] SK-03: SKILL.md 의 Regeneration Drift 스니펫에서 `STACK=` 대입이 `guide_gate "$f" "$STACK"` 호출 줄보다
      **앞 줄**에 존재하고, 그 대입 줄 또는 직전 주석이 Phase 1 스택 확정값을 쓴다고 명시한다 [structural]
      (측정: `grep -n 'STACK=' SKILL.md` 의 첫 라인 번호 < `grep -n 'guide_gate "\$f" "\$STACK"' SKILL.md` 의 라인 번호,
      그리고 `STACK=` 라인 ±2 줄에 `Phase 1` 문자열)
- [ ] SK-04: SKILL.md 의 G3 산문 설명(코드 펜스 밖)이 "스택 미지정이면 FAIL" 방향을 서술한다 — 코드와 산문이
      같은 방향 [structural]
      (측정: `grep -n 'G3' SKILL.md` 로 산문 줄을 뽑아 그중 `미지정\|unset\|없으면` 과 `FAIL` 을 같은 줄 또는
      인접 2 줄 안에 함께 가진 줄 ≥1)

## Script

- [ ] SC-01: G3 — 스택 인자를 주지 않고 `guide_gate <파일>` 을 호출하면 `G3_STACKMIX FAIL` 줄과 최종 `GATE_FAIL`
      이 나오고, `guide_gate <파일> flutter` 로 swift 펜스가 없는 파일을 호출하면 `G3_STACKMIX PASS` 다.
      픽스처 `onboarding-kit/skills/setup-guide/evals/fixtures/gate-ok-flutter.md` 1 개로 두 호출을 zsh·bash
      양쪽에서 실행한다 [exact, enumerated]
      (측정: 4 벌 출력 전문 첨부 — `gate-ok-flutter.md` × {미지정, flutter} × {zsh, bash}. 미지정 2 벌은
      `G3_STACKMIX FAIL`, flutter 2 벌은 `G3_STACKMIX PASS`, 각 쌍의 zsh/bash diff 빈 출력)
      음성 대조: 게이트에서 "stack 이 비면 FAIL" 분기를 제거하면 미지정 호출이 베이스라인처럼
      `PASS stack=unset` 으로 되돌아가 이 측정이 FAIL 한다.
- [ ] SC-02: G4 — `❌ Deprecated` 박스를 쓴 Step 의 `**출처:**` 줄이 한국어 근거(`지원 종료`)를 담은 픽스처
      `onboarding-kit/skills/setup-guide/evals/fixtures/gate-g4-ko-sourced.md` 는 `G4_DEPRECATION PASS`,
      같은 박스에 근거 토큰이 전혀 없는 픽스처
      `onboarding-kit/skills/setup-guide/evals/fixtures/gate-g4-ko-unsourced.md` 는 `G4_DEPRECATION FAIL` 이다.
      두 픽스처 모두 `flutter` 스택으로 zsh·bash 양쪽 실행 [exact, enumerated]
      (측정: 4 벌 출력 전문 첨부 — `gate-g4-ko-sourced.md`·`gate-g4-ko-unsourced.md` × {zsh, bash}.
      sourced 는 `G4_DEPRECATION PASS unsourced_boxes=0`, unsourced 는 `G4_DEPRECATION FAIL`)
      음성 대조: G4 정규식에서 한국어 토큰을 제거하면 `gate-g4-ko-sourced.md` 가 FAIL 로 뒤집힌다 —
      계약 작성 시점의 현행 게이트(베이스라인)가 정확히 그 상태다.
- [ ] SC-03: 소급 재측정 — 변경 후 게이트를 배포 예제 `docs/onboarding-kit/examples/fcm-ios-setup-guide.md` 에
      `flutter` 스택으로 실행하면 §GAP 분석 베이스라인 첫 블록과 **판정 5 줄이 동일**하다 (G1~G4 PASS + GATE_PASS).
      zsh·bash 양쪽 [exact]
      (측정: 변경 후 출력 5 줄 첨부 + 베이스라인 블록과 `diff` — G3 줄의 `stack=flutter swift_fence=0` 까지 동일.
      예제 파일 자체는 수정하지 않는다)
- [ ] SC-04: `python3 scripts/validate-plugin.py onboarding-kit` 의 V1~V8 에서 FAIL 0 건이고,
      인자 없는 전 킷 실행에서 `onboarding-kit` 이 원인인 새 FAIL 0 건 [goal]
      (측정: 두 명령 출력 전문 첨부. WARN 은 건별 사유와 함께 허용)
- [ ] SC-05: `python3 scripts/sync-docs.py onboarding-kit` 실행 후 `python3 scripts/sync-docs.py --check-only` 가
      exit 0 [goal]
      (측정: 두 명령 exit code 와 마지막 출력 줄)

## Error

- [ ] ER-01: 변경 후 게이트가 존재하지 않는 파일 경로에 대해 `GATE_BLOCKED no_such_file=` 을 출력하고 exit 상태 0 을
      유지한다 — 기존 동작 회귀 없음. zsh·bash 양쪽 [exact]
      (측정: `guide_gate /nonexistent/x.md flutter; echo rc=$?` 2 벌 출력)
- [ ] ER-02: 스택 인자를 **빈 문자열로 명시** 전달(`guide_gate <파일> ""`)해도 미지정과 동일하게 `G3_STACKMIX FAIL`
      이다 — `${2:-}` 경로와 빈 인자 경로가 갈리지 않는다. zsh·bash 양쪽 [exact]
      (측정: `gate-ok-flutter.md` 에 `""` 전달 2 벌 출력)

## Architecture

- [ ] AR-01: 이번 스프린트의 커밋 변경 경로가 아래 허용목록 접두 안에만 있다 [exact, enumerated]
      Given: 구현 커밋 완료 후 (커밋된 상태에서 측정)
      허용: `onboarding-kit/skills/setup-guide/` ·
      `.harness/sprint-contract-onboarding-kit-gate-defects.md` ·
      `.harness/sprint-feedback-onboarding-kit-gate-defects.md` ·
      `.harness/sprint-amendments-onboarding-kit-gate-defects.md`
      (측정: `git diff --name-only 4fb1382..HEAD` 의 각 줄이 위 4 접두 중 하나에 매치. 매치 안 되는 줄 0 건.
      제외 pathspec 없음 — 워크트리는 이 세션 전용. 계약 시점 베이스라인: 0 경로)
- [ ] AR-02: G4 근거 표기의 산문 정본 `onboarding-kit/skills/setup-guide/references/format-checklist.md` §Deprecated 박스
      규약이 "출처가 deprecated 라고 명시" 외에 **한국어 표기(`지원 종료` 등)도 근거로 인정**한다고 갱신된다.
      HTML 미러 3 파일(`docs/onboarding-kit/fcm-ios-example.html` · `docs/onboarding-kit/search-strategy.html` ·
      `docs/onboarding-kit/format-checklist.html`)은 이 스프린트에서 갱신하지 않는다 — docs-site 재생성 사이클의
      명시적 미완이며 그 사실을 완료 보고에 적는다 [exact, enumerated]
      (측정: `grep -n '지원 종료' onboarding-kit/skills/setup-guide/references/format-checklist.md` ≥1,
      그리고 `git diff --name-only 4fb1382..HEAD -- docs/` 가 빈 출력)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수
      (측정: `python3 scripts/validate-plugin.py onboarding-kit --check=code-fence` 가 V6 OK)
- [ ] AP-04: `SKILL.md` frontmatter 에서 `name` 필드 누락 없음
      (측정: `python3 scripts/validate-plugin.py onboarding-kit --check=frontmatter` 가 V1 OK)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (제외 목록 없음)
- [ ] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개 — N/A (이 킷은 실행 가능한 앱/서버가 아니라 스킬 정의 파일이다.
      게이트 함수 실행(SC-01·SC-02·SC-03·ER-01·ER-02)이 런타임 검증을 대신한다)
