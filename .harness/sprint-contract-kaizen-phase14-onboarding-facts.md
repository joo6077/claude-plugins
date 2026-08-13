---
feature: "카이젠 Phase 14 — onboarding-kit 사실 정정 4종 + Guide Conformance Gate(E3) + 미검증 카운터 canonical 전파"
created: "2026-08-13 16:05"
complexity: "복잡"
conditions: 23
slug: kaizen-phase14-onboarding-facts
status: active
owner_session: df1b3e15-30b3-4825-a3c4-4ac44c686e94
conditions_digest: sha256:6f3dd3d4fc963a30
locked_at: "2026-08-13 16:05"
---

## 배경

`.harness/.meta/evidence/phase14.md` 가 이번 Phase 의 **유일한 외부 근거**다. 외부 조회 0 회.

`/insights` 2026-08-13 은 "Phase 14 Onboarding — 이번 리포트에 직접 신호 없음" 이라고 명시한다
(`.claude/kaizen-input/insights-report.md:110`). 근거는 §0 이 아니라 **evidence 파일의 실측 결함**과
**킷 자신의 evals 대비 배포 산출물 실측**이다.

### 근본원인 — 왜 직전 사이클 수정이 이 결함을 못 잡았나

직전 사이클(2026-07-27, changelog `[2026-07-27]` Phase 14)은 이 킷에서 정확히 같은 주제를 고쳤다:

> **evals 가 사용자 피드백 메모리와 정면 모순**하던 상태 수정 (Flutter FCM 가이드 테스트가
> Flutter 에 존재하지 않는 네이티브 Swift 호출을 요구). 출처 원장(Step별 URL+조회일, E2) +
> 경로·파일명 날조 금지(E2) 신설.

**규칙과 evals 는 고쳤고, 그 규칙을 위반하는 배포 산출물은 재검사하지 않았다.**
`setup-guide` 는 가이드를 **영속 아티팩트**(`docs/setup/<서비스>/<기능>.md`)로 생산하는데,
스킬의 Phase 4 검증은 **지금 쓰는 가이드 하나**만 본다. 규칙이 바뀌어도 이미 생성된 가이드를
다시 재는 경로가 없다. 그 결과 킷의 자체 쇼케이스 예제가 **킷 자신의 evals 6 케이스 중 3 개를
3 개월간 위반한 채** 배포돼 있었다.

**실측 (2026-08-13, zsh · bash 동일 출력):**

```text
$ G=docs/onboarding-kit/examples/fcm-ios-setup-guide.md
steps=8 ledger=0 appdelegate=4 firebaseconfigure=1 deprecatedbox=1 p12=1
```

| evals 케이스 | assertion | 배포 예제 실측 | 판정 |
| --- | --- | --- | --- |
| `source-ledger-per-step` | `every_step_has_field('출처')` | Step 8 개 / `**출처:**` 0 개 | 위반 |
| `flutter-fcm-ios` | `guide_does_not_require_appdelegate_call('FirebaseApp.configure()')` | Step 7-1 이 Swift 초기화를 필수로 제시 | 위반 |
| `deprecation-claim-fidelity` | `guide_does_not_claim_deprecated('.p12')` | `❌ Deprecated: APNs Certificate (.p12)` 1 건 | 위반 |
| `apple-site-distinction` | 사이트 차이 표 | 표 없음 · "출시 단계에서만 그쪽으로" 로 축소 | 부분 위반 |

→ 재발이 아니라 **미측정**이다. 처방은 문장 추가가 아니라 **enforcement 등급 상향**:
E1 문장 / E2 자기보고 체크리스트 → **E3 결정론적 게이트**(LLM 호출 없는 순수 판정 + 배포된
가이드에도 사후 적용 가능). 근거: `harness/docs/guides/skill-design-guide.md` §3.7 Enforcement 3 등급
("재발했는데 같은 등급에서 문장만 다시 다듬는 것은 개선이 아니다") · 등급 원장의
`Completion Evidence Gate` 행("증거 없는 완료 주장 재발 → 검증 스크립트 통과 전 완료 차단 E3").

## 리서치 소스

- `.harness/.meta/evidence/phase14.md` — M1(스택 혼용) · M1 보조(`.p12` deprecated 근거 약함) ·
  M2(콘솔 라벨 · 로그인 뒤 UI 미확인) · M2 보조(Apple Help 섹션명) · M3(작업별 사이트 표) ·
  기타 출처 점검(`docs.stripe.com` · `docs.cloud.google.com`) · §3 트레이드오프
- `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol (Phase 3 개정,
  2026-08-13) — 마커 4 분기 · 접미 `:ENV` / `:INVALID` · 카운터 분리 · 임계 2 는 INVALID 에만
- `harness/docs/guides/skill-design-guide.md` §3.7 Enforcement 3 등급 + 등급 원장
- `harness/references/contract-schema.md` v5.3 — 계약 포맷
- `docs/kaizen/changelog.md` `[2026-07-27]` Phase 14 — 직전 사이클 흡수분(중복 금지 대상)
- 킷 자체 실측: `onboarding-kit/skills/setup-guide/evals/evals.json` 6 케이스 대비 배포 예제 대조

## GAP 분석

| # | GAP | 근거 | 처방 | 등급 |
| --- | --- | --- | --- | --- |
| G-A | Flutter 가이드에 네이티브 Swift 초기화가 최소 필수로 박혀 있다 | evidence M1 | Step 7-1 삭제 · Dart 단일 초기화 | 사실 정정 |
| G-B | `.p12` 를 deprecated 로 단정 (출처보다 강한 주장) | evidence M1 보조 | 박스 제거 · "현행 가이드는 `.p8` 을 안내" 로 강도 하향 | 사실 정정 |
| G-C | "셋업의 99% 가 Developer Portal" 과장 | evidence M3 | 작업별 사이트 표(7 행)로 교체 · App Store Connect 3 행 포함 | 사실 정정 |
| G-D | Firebase 콘솔 경로가 구 표기 · 한국어 우선 | evidence M2 | public docs 확인 라벨로 교체 (영문 정본 + 한국어 괄호) | 사실 정정 |
| G-E | GCP 문서 최종 호스트 미기록 | evidence 기타 출처 점검 | `docs.cloud.google.com` 기록 | 사실 정정 |
| G-F | 로그인 뒤 콘솔 UI 를 WebFetch 로 확인 가능한 것처럼 서술 | evidence M2 "미확인" | Gotcha 2 에 한계 명시 · public docs 라벨만 인용 | 사실 정정 |
| G-G | 킷 로컬 `[미검증]` 임계가 canonical 개정(4 분기 · 카운터 분리)과 어긋남 | qa-evaluation-guide §Canonical | 접미 분류 전파 · blanket 임계 제거 | 정합 |
| G-H | 배포된 가이드를 규칙 변경 후 다시 재는 경로가 없다 (근본원인) | 본 계약 §배경 실측 | Guide Conformance Gate (E3) + 재생성 전 드리프트 검사 | **E1/E2 → E3** |

## 범위 경계

- **수정 대상**: `onboarding-kit/skills/setup-guide/SKILL.md` ·
  `onboarding-kit/skills/setup-guide/references/` (이 킷은 다른 킷과 달리 top-level
  `onboarding-kit/references/` 가 없고 references 가 스킬 아래에 있다 — 선언 scope
  `onboarding-kit/references/` 의 실물) · `docs/onboarding-kit/examples/` (MD 만) · 본 계약 파일.
- **수정 금지**: `docs/onboarding-kit/*.html` (Step 11.5 docs-site 재생성 대상) ·
  `onboarding-kit/skills/setup-guide/evals/evals.json` (선언 scope 밖) · 다른 킷 · `harness/`.
- 외부 네트워크 도구 0 회. evidence 에 없는 URL·수치·버전 번호를 추가하지 않는다.

## 회귀 게이트

- AR-01 Diff-Scope baseline (계약 작성 시점 1 회 실행):
  `git status --porcelain -- onboarding-kit docs/onboarding-kit` → 빈 출력.
- 게이트 셸 이식성: 모든 측정 명령을 zsh · bash 양쪽에서 실행하고 동일 출력을 확인한다
  (`contract-schema.md` §셸 이식성 규약 — zsh `nomatch` 로 글로브가 명령을 죽인 전례).
- 열거값(Step 수 · 출처 수 · 파일 수)은 타이핑하지 않고 명령으로 계산한다.

## Skill

- [ ] SK-01: SKILL.md 의 미검증 마커 서술이 canonical 4 분기 접미 체계를 쓴다 [exact]
      (측정: `grep -c '미검증:ENV' onboarding-kit/skills/setup-guide/SKILL.md` >= 1 AND
       `grep -c '미검증:INVALID' onboarding-kit/skills/setup-guide/SKILL.md` >= 1 AND
       `grep -c 'Canonical Unverified-Evidence Protocol' onboarding-kit/skills/setup-guide/SKILL.md` >= 1)
- [ ] SK-02: 킷 로컬 blanket 임계 서술("2 건 이상이면 부분 완료")이 킷 3 파일에서 0 건이다
      [exact, enumerated]
      (측정: `grep -rn '2 건 이상이면' onboarding-kit/skills/setup-guide/SKILL.md onboarding-kit/skills/setup-guide/references/format-checklist.md onboarding-kit/skills/setup-guide/references/search-strategy.md`
       결과 0 행)
- [ ] SK-03: SKILL.md 에 `guide_gate` 셸 함수가 존재하고 G1~G4 4 검사 ID 를 모두 낸다 [exact]
      (측정: `grep -c 'guide_gate' SKILL.md` >= 1 AND `G1_LEDGER` `G2_MARKER` `G3_STACKMIX`
       `G4_DEPRECATION` 4 토큰이 각각 1 건 이상)
- [ ] SK-04: `guide_gate` 가 zsh 와 bash 에서 **동일 출력**을 낸다 [goal]
      (측정: 두 셸에서 배포 예제를 인자로 실행한 출력을 `diff` 하여 차이 0 행 ·
       음성 대조: 게이트 함수 본문을 제거하면 이 측정이 FAIL 해야 한다)
- [ ] SK-05: Process 에 **기존 가이드 재검사** 단계가 있고 게이트 실행을 요구한다 [structural]
      (측정: SKILL.md 에 `Regeneration Drift` 문자열 1 건 이상 AND 그 절이 `guide_gate` 를 호출)
- [ ] SK-06: Gotcha 2 가 "로그인 뒤 콘솔 화면은 공개 문서로 검증 불가" 사실을 기술한다 [structural]
      (측정: SKILL.md Gotcha 2 절에 `로그인` AND `공개 문서` 토큰 동시 출현)

## Error

- [ ] ER-01: SKILL.md 에서 `99%` 와 `거의 안 들어감` 표현이 0 건이다 [exact]
      (측정: `grep -c -e '99%' -e '거의 안 들어감' onboarding-kit/skills/setup-guide/SKILL.md` = 0)
- [ ] ER-02: SKILL.md Gotcha 3 이 작업별 사이트 표를 갖고 App Store Connect 가 필요한 작업 3 종을
      명시한다 [exact, enumerated]
      (측정: Gotcha 3 절에 `App Store Connect` 와 함께 `앱 레코드`, `빌드 업로드`, `TestFlight`
       3 토큰이 각각 1 건 이상)
- [ ] ER-03: 예제에서 `.p12` 를 deprecated 로 단정하는 문구가 0 건이다 [exact]
      (측정: `awk '/[Dd]eprecated/ && /\.p12/' docs/onboarding-kit/examples/fcm-ios-setup-guide.md`
       결과 0 행 AND `grep -c '❌ Deprecated' docs/onboarding-kit/examples/fcm-ios-setup-guide.md` = 0)
- [ ] ER-04: 예제에 Swift 코드펜스와 네이티브 Firebase 초기화 호출이 0 건이다 [exact]
      (측정: `grep -c '^```swift' docs/onboarding-kit/examples/fcm-ios-setup-guide.md` = 0 AND
       `grep -cF 'FirebaseApp.configure()' docs/onboarding-kit/examples/fcm-ios-setup-guide.md` = 0)
- [ ] ER-05: 예제가 "네이티브 코드 수정 없음 ≠ Xcode 프로젝트 설정 없음" 을 명시한다 [structural]
      (측정: 예제에 `Capability` AND `Background Modes` AND `Xcode 프로젝트` 토큰 동시 출현 ·
       evidence §3 트레이드오프 대응)
- [ ] ER-06: 예제 Firebase 콘솔 경로가 evidence M2 확인 라벨 6 종을 쓴다 [exact, enumerated]
      (측정: 예제에 `Cloud Messaging`, `iOS app configuration`, `APNs authentication key`,
       `DevOps & Engagement`, `New campaign`, `Send test message` 6 토큰이 각각 1 건 이상)
- [ ] ER-07: `search-strategy.md` 가 GCP 최종 리다이렉트 호스트를 기록한다 [exact]
      (측정: `grep -c 'docs.cloud.google.com' onboarding-kit/skills/setup-guide/references/search-strategy.md`
       >= 1)
- [ ] ER-08: 예제에 하드코딩된 패키지 버전 핀이 0 건이다 [exact]
      (측정: `grep -cE '\^[0-9]+\.[0-9]+\.[0-9]+' docs/onboarding-kit/examples/fcm-ios-setup-guide.md`
       = 0 — evidence 에 없는 수치를 유지하지 않는다)

## Architecture

- [ ] AR-01: 이번 스프린트의 변경이 정확히 4 경로로 한정된다 [exact, enumerated]
      (Given: 커밋 직전 working tree ·
       측정: `git status --porcelain -- onboarding-kit docs/onboarding-kit .harness/sprint-contract-kaizen-phase14-onboarding-facts.md`
       의 경로 집합이 `onboarding-kit/skills/setup-guide/SKILL.md`,
       `onboarding-kit/skills/setup-guide/references/search-strategy.md`,
       `onboarding-kit/skills/setup-guide/references/format-checklist.md`,
       `docs/onboarding-kit/examples/fcm-ios-setup-guide.md`,
       `.harness/sprint-contract-kaizen-phase14-onboarding-facts.md` 와 정확히 일치)
- [ ] AR-02: 예제의 `## Step` 수와 `**출처:**` 수가 같고 둘 다 0 보다 크다 [exact]
      (측정: 두 값을 각각 `grep -c` 로 **계산**해 비교 · 값을 타이핑하지 않는다 ·
       음성 대조: 출처 줄 하나를 지우면 이 측정이 FAIL 해야 한다)
- [ ] AR-03: 배포 예제가 `guide_gate` 를 통과한다 (`GATE_PASS`) [goal]
      (측정: SKILL.md 의 게이트 함수를 그대로 실행해 마지막 줄이 `GATE_PASS` ·
       음성 대조: 예제에서 `**출처:**` 줄 1 개를 제거하면 `GATE_FAIL G1_LEDGER` 가 나와야 한다)
- [ ] AR-04: `docs/onboarding-kit/*.html` 이 이번 커밋에서 0 건 변경된다 [exact]
      (측정: `git show --name-only --format= HEAD | grep -c '^docs/onboarding-kit/.*\.html$'` = 0)
- [ ] AR-05: 예제 제목이 스택을 명시한다 (Gotcha 1 stack-first) [exact]
      (측정: 예제 1 행에 `Flutter` 토큰 출현)

## Anti-patterns

- [ ] AP-03: 이번 변경이 bare **여는** code fence 를 새로 도입하지 않는다 [exact]
      (측정: `git diff -U0` 의 추가 행 중 여는 펜스(직전 상태가 코드블록 밖)인데 언어 힌트가
       없는 것 0 건 · 닫는 펜스는 대상 아님)
- [ ] AP-01: 예제·스킬에 하드코딩 버전이 남지 않는다 (ER-08 과 대상 분리 — 이쪽은 SKILL.md·references)
      (측정: `grep -cE '\^[0-9]+\.[0-9]+\.[0-9]+' onboarding-kit/skills/setup-guide/SKILL.md onboarding-kit/skills/setup-guide/references/*.md` 합계 0)

## Reusability

- [ ] RE-01: 미검증 프로토콜을 킷에서 재정의하지 않고 harness canonical 을 인용한다 [structural]
      (측정: 킷 3 파일이 `harness/docs/guides/qa-evaluation-guide.md` 앵커를 인용 ·
       킷 자체 임계 숫자 재정의 0 건 — SK-02 와 짝)

## Diagnostics

- [ ] DG-01: `python3 scripts/validate-plugin.py onboarding-kit` 가 Exit 0 이다
      (측정: 명령 실행 후 `echo $?` = 0 · 다른 킷은 병렬 Phase 진행 중이므로 전체 실행 금지)
