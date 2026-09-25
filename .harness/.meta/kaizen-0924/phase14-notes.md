# 카이젠 2026-09-24 Phase 14 (onboarding-kit) — notes

- 계약: `.harness/sprint-contract-kaizen-0924-p14-onboarding-kit.md` (조건 28 · 기능 조건 18, 봉인 `sha256:e90190048db61bfa` · `locked_at` 2026-09-25 11:00)
- 개정: `.harness/sprint-amendments-kaizen-0924-p14-onboarding-kit.md` (조건 변경 0 건, `end_sha` 만)
- 검토: `.harness/.meta/kaizen-0924/phase14-review.md` — 1 회차 `VERDICT: CHANGES`(고칠 것 넷 · 권고 셋)는 DRAFT 가 고칠 것 넷과 권고 둘을 반영했고, 2 회차가 `VERDICT: APPROVE` 를 냈다.
  BUILD 는 봉인 전에 `## 범위 경계` 승인 대체 줄에 이 판정을 적은 것 말고는 계약을 고치지 않았다
- 시작 커밋 `da9fbae94c13a9a1fc657f29ce9fc380ba9d506b`
- 계약 피드백: `~/.harness/feedback/contract/5a24cc99-2026-09-25T110416-de8c7935-62800.yaml` (`verify-feedback.sh` PASS). 초안은 스크래치 `p14b/feedback-draft.yaml` 에 따로 쓰고
  `HARNESS_CONTRACT_ROOT` · `HARNESS_CONTRACT` 를 명시해 저장했다 — 작업 폴더의 `.harness/feedback-draft.yaml` 은 다른 Phase 와 겹칠 수 있어 쓰지 않았다

## 커밋

| 커밋 | 내용 | 파일 |
| --- | --- | --- |
| `fdf756d` | 봉인 커밋 | 계약 1 개 |
| `b2e661f` | 막는 요구 세 칸 · 게이트 시험 입력 러너 · 값이 든 .env 를 열지 않음 | `onboarding-kit/` 일곱 개 |
| `00e900f` | 개정 파일에 `end_sha` (`b2e661f`) | 개정 1 개 |
| 이 파일의 커밋 | notes · 검토 기록 | `.harness/` 두 개 |
| 그다음 커밋 | 개정 파일에 notes 커밋 sha 로 `end_sha` 한 줄 더 | 개정 1 개 |

모든 커밋 메시지 끝 문단에 `Kaizen-Phase: kaizen-0924-p14-onboarding-kit` 줄이 있다. 구현 커밋은 `git add -- <일곱> && git commit -o -- <일곱>` 로 내 경로만 실었고
러너는 `chmod +x` 뒤 커밋해 git 모드가 `100755` 다. **FIX 가 커밋을 더할 때도 서명 줄을 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다.**

구현은 초안의 모의본(스크래치 `p14d2/mock.py`, 지문 앞 16 자리 `48edf971dd8f8213` — 계약에 적힌 값)을 작업 폴더에 그대로 돌렸다. 돌리기 전에 `onboarding-kit/` 가
시작 커밋과 `HEAD` 사이에 바뀌지 않았고 미커밋 변경도 없는 것을 봤다. 커밋한 일곱 파일이 예행 저장소(`p14d2/rh-none`)의 같은 경로와 blob 이 같다.
28 조건 측정은 봉인 판 계약에서 뗀 묶음으로 돌렸다 — 스크래치 `p14b/k/`(`common.sh` · `m.sh` · `rule-delta.sh`, DRAFT 판 `p14d2/k/` 와 글자 그대로 같다) ·
`p14b/runall.sh`(`K` 와 `TMPDIR` 를 스크래치로 두고 공통 정의를 `.` 로 읽은 뒤 `m <조건 ID>`). QA 가 같은 묶음을 다시 돌릴 수 있다.

구현 커밋 `b2e661f` 를 상한으로 둔 첫 측정에서 notes 에 기대는 둘(ER-01 둘째 줄 `NOTES_MISSING` · ER-03)을 빼고 26 개 ID 가 조건 줄의 값과 같았다.
커밋 뒤 저장소 검사: `validate-plugin.py onboarding-kit` 종료 코드 0(V1 ~ V10 OK · V2 SKIP) · `sync-docs.py --check-only` 0 · `sync-evals.py --check-only` 0 ·
`run-evals.py` 0(114 passed) · `validate-post-kaizen.py --since da9fbae` 0(12 PASS · 0 FAIL · 3 SKIP, scope-isolation · doc-contracts PASS, docs-site-regen SKIP).

## 바꾼 파일

- `onboarding-kit/skills/setup-guide/SKILL.md` — Gotcha 9(막는 요구 세 칸 · 스킬 자신의 불가 결론에도 §3.7 조항 3 네 칸) · Gotcha 8 값이 든 `.env` 문단과 나쁜 예 ·
  Gotcha 4 앱 이름을 `com.<앱이름>.app` 으로 · `### 출처 원장 (Source Ledger)` 의 「마커와 아래 네 요건」 과 §3.7 네 칸 대응 문장 ·
  `### Guide Conformance Gate (E3)` 러너 안내 줄 · Phase 1 둘째 항목 · Phase 4 목록 5 번(뒤 번호 하나씩 밀림)
- `onboarding-kit/skills/setup-guide/references/format-checklist.md` — §2 막는 요구 세 칸 규칙 · 칸 표 · FCM iOS 예 표, 첫 목록 계정/권한 줄 끝
- `onboarding-kit/skills/setup-guide/references/project-detection.md` — `.env.example` 류와 「있는지만 보고 열지 않는다」
- `onboarding-kit/skills/setup-guide/evals/evals.json` — `version` 0.3.0 · `runner` · `gate_cases` 여섯 · 사례 `blocking-requirement-scope` · `no-invented-paths` 에 `.env.example` 과 읽지 않음 단언
- `onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh` (새 파일) — SKILL.md 에서 `guide_gate` 를 뽑아 입력마다 zsh · bash 출력을 기대 출력과 대조한다.
  폴더에만 있는 픽스처 · 돈 수와 적힌 수 차이를 실패로 세고, 도구 · 함수 추출 · 입력 목록이 없으면 종료 코드 2
- `onboarding-kit/skills/setup-guide/evals/fixtures/gate-fail-ledger-marker-swift.md` (새 파일) — G1 · G2 · G3 가 함께 떨어지는 양성 대조
- `onboarding-kit/README.md` — `## 카이젠` 절 Phase 13 → 14, 러너 한 줄

## 반영한 처리 배정표 키

| 키 · 출처 | 반영 |
| --- | --- |
| `other-kits:P3` | 폴더에만 있던 픽스처 셋을 `gate_cases` 에 등록하고, 러너가 부를 때마다 SKILL.md 에서 함수를 뽑아 zsh · bash 로 돌린다. 양성 대조 픽스처 하나를 더했다. CI 줄은 러닝북이 Final 몫으로 정해 아래 `## 넘기는 것` 에 적었다. howto-kit 단계는 Phase 17 몫 |
| `other-kits:P9` | format-checklist §2 세 칸 규칙과 FCM iOS 예(실기기 · 유료 개발자 계정 · 앱 출시 — 앱 출시는 막는 요구가 아니다), SKILL.md Gotcha 9, Phase 4 확인 5 번, 평가 사례 `blocking-requirement-scope` |
| `F10` 비고 | `other-kits:P9` 와 한 번에 — Gotcha 9 셋째 줄이 스킬 자신이 「못 만든다」 고 결론 낼 때도 §3.7 조항 3 의 네 칸을 먼저 적게 한다 |
| `phase1-notes.md` 넘김 | `SKILL.md:30` 「마커 + 사유 한 줄」 을 「마커와 아래 네 요건」 으로, 네 요건 끝에 §3.7 조항 3 네 칸과의 대응 한 문장 |
| 데이터 풀 §0.5 `feedback-no-read-env` (grounding `user_correction`) | 값이 든 `.env` 를 열지 않는다 — Gotcha 8 · Phase 1 · project-detection · 평가 사례 |

### Phase 1 결과 대조 (오케스트레이터 Step 14 전수 감사, `skill-design-guide.md` 1.6.0)

| Phase 1 변경 | onboarding-kit 에서 본 자리 | 처리 |
| --- | --- | --- |
| §3.7 조항 3 — 검증 불가 시 네 칸 | SKILL.md `:30` 「사유 한 줄」 이 옛 말, `:40` 네 요건은 같은 내용 | `:30` 을 네 요건으로, `:40` 끝에 대응 한 문장 |
| 작업 자체를 못 한다고 결론 내리기 전에도 네 칸 | 스킬 자신의 불가 결론에 대한 줄이 없었다 | Gotcha 9 셋째 줄 |
| 0 이 기대값인 검증의 양성 대조 | `guide_gate` 의 G1 · G2 · G3(Swift) 쪽에 알려진 나쁜 예가 없었다 | 새 픽스처 |
| 알려진 답 대조 | 새 러너가 내는 값 | 픽스처마다 손으로 센 기대 출력 다섯 줄 |
| 에이전트 frontmatter 18 종 | onboarding-kit 에 `agents/` 가 없다 | 해당 없음 |
| 500 줄 권고 | SKILL.md 265 줄 → 편집 뒤 280 줄 | 해당 없음 |

## 미반영 키와 사유

- evals.json `source` 의 `Last updated 2026-07-20 UTC` — 근거 파일은 페이지 갱신일만 다시 봤고 본문 주장(.p12 를 deprecated 로 적지 않음 · Instance ID)을 다시 확인하지 않았다.
  날짜만 옮기면 확인하지 않은 주장을 확인했다고 적게 된다
- GCP 서비스 계정 키를 기본 경로로 쓰지 않는 계약(Workload Identity Federation 우선) — 근거 파일이 스스로 추론이라 적었고, 이 킷의 GCP 가이드에서 생긴 사고 실측이 없다
- CocoaPods → SPM 전환 — 근거 파일 §5 가 Flutter 예제를 곧바로 SPM 절차로 바꾸지 말라고 적었다
- 패키지 최신 버전(`firebase_messaging` · `firebase_core` · `flutterfire_cli`) — 킷은 버전을 고정하지 않고 레지스트리 조회를 요구한다. 근거 파일도 그 정책을 현행으로 봤다
- 막는 요구 세 칸을 `guide_gate` 검사로 넣는 것 — 형식이 새로 생겨 배포 예제(범위 밖)가 아직 옛 형식이다. 넣으면 예제가 바로 `GATE_FAIL` 이 된다. 예제를 Final 이 고친 뒤 다음 사이클에 본다
- 러너를 howto-kit 러너와 합치는 것 — 킷은 따로 설치되므로 다른 킷 파일을 부르면 깨진다. 두 셸 대조 구조만 따랐다
- 근거 파일 §3 의 `docs/onboarding-kit/plan-2026-05-18.md` 옛 Stripe 호스트(`stripe.com/docs/`) — 역사 문서라 두었다. 런타임 `search-strategy.md` 는 이미 새 호스트다
- 오케스트레이터 Step 14 범위 줄의 `onboarding-kit/references/` — 이 폴더는 없다. references 는 스킬 폴더 아래 `onboarding-kit/skills/setup-guide/references/` 다. 오케스트레이터는 이 Phase 범위 밖이라 적어만 둔다

## 넘기는 것

| 파일 | 할 일 | 맡을 곳 |
| --- | --- | --- |
| `.github/workflows/ci.yml` | validate 작업에 두 단계 — `command -v zsh >/dev/null \|\| (sudo apt-get update && sudo apt-get install -y zsh)` 와 `sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh`. 러너는 zsh 가 없으면 `TOOL_MISSING zsh` · 종료 코드 2 로 멈춘다. Ubuntu 에서는 돌려 보지 못했다. howto-kit 단계는 Phase 17 과 함께 | Final |
| `docs/onboarding-kit/examples/fcm-ios-setup-guide.md` | `:5` · `:29` Xcode 26.2+ · iOS 15, `:31` · `:370` · `:392` 시뮬레이터 주장(Cloud Messaging 은 실기기), 사전 요구사항을 세 칸으로, `:30` · `:46` · `:381` · `:384` · `:385` 앱 이름을 일반형으로 | Final |
| `docs/onboarding-kit/fcm-ios-example.html` | `:249` · `:251` · `:605` 같은 옛 값 — MD 를 고친 뒤 다시 만든다 | Final F2 |
| `.claude/skills/onboarding-kaizen/SKILL.md` | Phase 4 검증에 `sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh` 한 줄 | Final |
| `onboarding-kit/.claude-plugin/plugin.json` | 버전 | Final |
| `docs/onboarding-kit/setup-guide.html` · `docs/onboarding-kit/format-checklist.html` · `docs/onboarding-kit/project-detection.html` | 이 Phase 가 바꾼 SKILL.md · format-checklist · project-detection 에서 만든 페이지라 다시 만든다. 소스가 바뀌었는데 드리프트 목록에 안 나온다 | Final F2 |
| `scripts/detect-docs-drift.py` | `SOURCE_TO_HTML` · `SOURCE_OVERRIDES` 에 onboarding-kit 소스와 `docs/onboarding-kit/` 페이지 매핑이 없다 — 예행 판에서 `no docs drift since da9fbae` 였다 | Final |

## changelog 한 단락

onboarding-kit — 셋업 가이드가 사전 요구사항을 한 줄로 막아 버리지 않게 했다. 실기기 · 유료 개발자 계정 · 앱 출시 같은 막는 요구마다 출처 · 막히는 것 · 우회 세 칸을 적고,
출처가 요구하지 않으면 막는 요구로 쓰지 않으며, 출처에 없는 우회를 지어내지 않는다(FCM iOS 예 포함). 스킬이 스스로 「못 만든다」 고 결론 낼 때도 막는 것 · 시도한 우회 ·
통제 불가 사유 · 재검증 명령을 먼저 적는다. 폴더에만 있고 한 번도 안 돌던 게이트 시험 입력 셋을 `evals.json` 에 등록하고, SKILL.md 에서 함수를 뽑아 zsh · bash 두 셸로
대조하는 러너 `evals/run-gate-evals.sh` 와 G1 · G2 · G3 양성 대조 픽스처를 더했다. 값이 든 `.env` 는 있는지만 보고 열지 않는다.

## 킷 로그 한 단락

2026-09-24 Phase 14 — 막는 요구 세 칸의 근거: Cloud Messaging 은 실제 Apple 기기를 요구한다(<https://firebase.google.com/docs/ios/setup>).
Push notifications 는 무료 계정 열에 없고(<https://developer.apple.com/help/account/reference/supported-capabilities-ios>), 일반 개발과 개인 기기 시험은 멤버십 없이 된다
(<https://developer.apple.com/help/account/membership/programs-overview>). 비영리 · 교육기관 · 정부 기관은 가입 비용 면제 경로가 있다(<https://developer.apple.com/programs/enroll/>).
개발 환경에서 기기 토큰으로 시험 발송이 된다(<https://developer.apple.com/documentation/usernotifications/testing-notifications-using-the-push-notification-console>).
새 픽스처 출처 줄은 <https://firebase.google.com/docs/cloud-messaging/flutter/get-started>. CI 넘김 줄의 zsh 확인은 `ubuntu-latest` 가 24.04 이고 zsh 가 제공 목록에 없다는 근거다
(<https://github.com/actions/runner-images> · <https://github.com/actions/runner-images/releases/tag/ubuntu24/20260920.314>).

## 다음 사이클 메모

- 막는 요구 세 칸은 아직 사람이 읽고 판정한다. Final 이 배포 예제를 세 칸으로 고친 뒤 `guide_gate` 에 검사를 더할지 본다
- onboarding-kit · planning-kit README 의 AUTO 표지가 `<!-- AUTO:skills:start -->` · `<!-- AUTO:skills:end -->` 꼴이라 `scripts/sync-docs.py` 의 `MARKER_RE` 가 못 읽는다.
  표지를 바꾸면 표가 스킬 설명 전문으로 바뀌어 이번에는 고치지 않았다
- `scripts/check-stale-values.py` 의 `SOURCE_DIRS` 에 onboarding-kit 이 없고 `scripts/run-evals.py` 의 `ALL_KITS` 에도 없다 — 두 저장소 검사가 이 킷을 훑지 않는다. Phase 4 몫
- 러너는 이 기계의 dash · `/bin/sh`(bash 3.2.57) · bash 5.3.9 · zsh 5.9 로만 돌려 봤다. CI 줄이 들어간 뒤 첫 Ubuntu 실행 출력을 확인한다
- 평가 사례의 `prompt` · `assertions`(`blocking-requirement-scope` · `no-invented-paths`)는 LLM 실행용이라 이번에 돌리지 않았다
