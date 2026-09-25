---
phase: 14
title: "Phase 14 onboarding-kit — 확보된 외부 근거"
collected: 2026-09-24
method: codex (foreground, 직접 호출 · gpt-5.6-sol · 조회는 curl/gh)
inputs: 처리 배정표(.claude/kaizen-input/insights-report.md)의 Phase 14 행 · phase-research-templates.md Phase 14 필수 출처 · 현행화 점검
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치를 지어내지 마라. 없으면 미반영으로 남긴다.
---

읽기 전용 조사만 수행했으며 작업 트리는 깨끗합니다. 아래 근거는 2026-09-24 실제 조회 결과입니다.

## 1. 출처 목록

실제로 가져온 1차·공식 출처:

1. [Firebase — Set up a Firebase Cloud Messaging client app on Apple platforms](https://firebase.google.com/docs/cloud-messaging/ios/client)
2. [Firebase — Add Firebase to your Flutter app](https://firebase.google.com/docs/flutter/setup)
3. [Firebase — Get started with Firebase Cloud Messaging in Flutter apps](https://firebase.google.com/docs/cloud-messaging/flutter/get-started)
4. [Firebase — Add Firebase to your Apple project](https://firebase.google.com/docs/ios/setup)
5. [Apple Developer Account Help](https://developer.apple.com/help/account/)
6. [Apple — Programs overview](https://developer.apple.com/help/account/membership/programs-overview)
7. [Apple — Supported capabilities (iOS)](https://developer.apple.com/help/account/reference/supported-capabilities-ios)
8. [Apple — Register an App ID](https://developer.apple.com/help/account/identifiers/register-an-app-id)
9. [Apple — Create a private key to access a service](https://developer.apple.com/help/account/keys/create-a-private-key)
10. [Apple — Create a development provisioning profile](https://developer.apple.com/help/account/provisioning-profiles/create-a-development-provisioning-profile)
11. [Apple — Testing notifications using the Push Notification Console](https://developer.apple.com/documentation/usernotifications/testing-notifications-using-the-push-notification-console)
12. [Apple Developer Program enrollment](https://developer.apple.com/programs/enroll/)
13. [pub.dev — firebase_messaging](https://pub.dev/packages/firebase_messaging)
14. [pub.dev — firebase_core](https://pub.dev/packages/firebase_core)
15. [pub.dev — flutterfire_cli](https://pub.dev/packages/flutterfire_cli)
16. [FlutterFire firebase_messaging changelog](https://github.com/firebase/flutterfire/blob/main/packages/firebase_messaging/firebase_messaging/CHANGELOG.md)
17. [FlutterFire firebase_core changelog](https://github.com/firebase/flutterfire/blob/main/packages/firebase_core/firebase_core/CHANGELOG.md)
18. [Firebase Apple SDK 12.19.2 release](https://github.com/firebase/firebase-ios-sdk/releases/tag/12.19.2)
19. [Google Cloud — Authentication overview](https://cloud.google.com/docs/authentication)
20. [Stripe documentation](https://docs.stripe.com/)
21. [GitHub Actions runner-images](https://github.com/actions/runner-images)
22. [Ubuntu 24 runner image release 20260920.314](https://github.com/actions/runner-images/releases/tag/ubuntu24/20260920.314)

## 2. 항목별 관찰 사실

### other-kits:P3 — 결정론적 eval을 CI에 등록

확인된 레포 사실:

- 현재 CI의 일반 eval 단계는 [`.github/workflows/ci.yml:46`](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/.github/workflows/ci.yml:46)의 `python3 scripts/run-evals.py --verbose`뿐입니다.
- 그런데 [scripts/run-evals.py:32](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/scripts/run-evals.py:32)의 대상 목록에는 `howto-kit`과 `onboarding-kit`이 없습니다.
- 이 Python runner는 [scripts/run-evals.py:65](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/scripts/run-evals.py:65)처럼 `evals`/`tests` 배열의 구조만 검사합니다. `cases`, `fixture`, `expect_final`을 실행하지 않습니다.
- `howto-kit/evals/evals.json`에는 실제로 16개 `cases`가 있고 전용 runner가 지정돼 있지만, CI에서 [howto-kit/evals/run-evals.sh](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/howto-kit/evals/run-evals.sh:1)를 호출하는 곳은 없습니다.
- onboarding의 세 픽스처는 [evals.json](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/onboarding-kit/skills/setup-guide/evals/evals.json:1)에 등록돼 있지 않습니다. 레포 전체 참조는 `.harness` 과거 기록뿐입니다.

`SKILL.md`의 함수 원문을 파일로 복사하지 않고 직접 뽑아 bash/zsh에서 실행한 실측:

| 입력 | stack | bash/zsh 공통 결과 |
|---|---|---|
| `gate-ok-flutter.md` | `flutter` | `GATE_PASS` |
| `gate-ok-flutter.md` | 빈 값 | `G3_STACKMIX FAIL stack=unset swift_fence=0`, `GATE_FAIL` |
| `gate-g4-ko-sourced.md` | `flutter` | `G4_DEPRECATION PASS unsourced_boxes=0`, `GATE_PASS` |
| `gate-g4-ko-unsourced.md` | `flutter` | `G4_DEPRECATION FAIL unsourced_boxes=1`, `GATE_FAIL` |

CI 셸 환경:

- GitHub 공식 runner-images 표에서 현재 `ubuntu-latest`는 Ubuntu 24.04를 가리킵니다. 공식 문서는 `-latest` 매핑이 점진적으로 바뀔 수 있으므로 고정 OS 라벨을 쓸 수 있다고 설명합니다. [runner-images README](https://github.com/actions/runner-images)
- Ubuntu 24.04 이미지 문서는 Bash를 명시하지만 zsh는 설치 도구 목록에서 확인되지 않았고, 2026-09-21 이미지 릴리스의 제공 manifest에서도 zsh 항목을 찾지 못했습니다. [Ubuntu 24 이미지 릴리스](https://github.com/actions/runner-images/releases/tag/ubuntu24/20260920.314)

반대 근거:

- zsh가 기반 이미지의 간접 패키지로 우연히 존재할 가능성까지 “없다”고 입증한 것은 아닙니다.
- 하지만 GitHub 공식 이미지 계약에서 zsh가 보장되지 않으므로 `command -v zsh` 검사 후 조건부 설치는 타당합니다.
- 추론: `ubuntu-latest`의 이동 가능성까지 고려하면, 현재 이미지에서 한 번 성공했다는 사실은 설치 확인 단계를 제거할 근거가 되지 않습니다.

### other-kits:P9 — 막는 요구에 출처·정확한 차단 범위·우회 병기

현재 [format-checklist.md:14](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/onboarding-kit/skills/setup-guide/references/format-checklist.md:14)의 사전 요구사항에는 제안된 3요소 규칙이 없습니다.

첫 대상은 실제로 다음 두 곳입니다.

- Markdown: [fcm-ios-setup-guide.md:27](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/onboarding-kit/examples/fcm-ios-setup-guide.md:27), [line 31](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/onboarding-kit/examples/fcm-ios-setup-guide.md:31)
- 생성 HTML: [fcm-ios-example.html:247](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/onboarding-kit/fcm-ios-example.html:247), [line 251](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/onboarding-kit/fcm-ios-example.html:251), [line 605](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/onboarding-kit/fcm-ios-example.html:605)

공식 출처가 구분하는 실제 경계:

- 실기기: Firebase Apple setup은 일반적인 앱 실행에는 “physical device or simulator”를 허용하지만, 앱이 Cloud Messaging을 사용한다면 physical Apple device를 준비하라고 별도로 요구합니다. 따라서 막히는 것은 Firebase 프로젝트 생성이나 Dart 코드 작성 전체가 아니라 실제 APNs/FCM 원격 수신 검증입니다. [Firebase Apple setup](https://firebase.google.com/docs/ios/setup)
- Flutter FCM 문서는 Xcode의 Push Notifications/Background Modes 활성화와 Firebase에 `.p8`, Key ID, Team ID를 올리는 절차를 요구하며 인증 키가 적어도 하나 필요하다고 명시합니다. 또한 iOS SDK 10.4.0 이상에서는 FCM API 전에 APNs token이 필요하다고 경고합니다. [Firebase Flutter FCM setup](https://firebase.google.com/docs/cloud-messaging/flutter/get-started)
- 유료 계정: Apple은 일반 앱 개발과 개인 기기 테스트 자체에는 멤버십이 필요 없다고 합니다. 반면 iOS capability 표에서는 Push notifications가 유료 ADP/ADEP에는 있고 무료 `Apple Developer` 열에는 없습니다. 따라서 “유료 계정 없으면 앱 개발 불가”가 아니라 “Push Notifications capability/APNs 자격증명 구성이 막힘”이 정확합니다. [Apple Programs overview](https://developer.apple.com/help/account/membership/programs-overview), [Supported capabilities](https://developer.apple.com/help/account/reference/supported-capabilities-ios)
- 비용은 현재 연 99 USD이며 지역별 가격이 다를 수 있습니다. 비영리·공인 교육기관·정부 기관에는 공식 fee-waiver 경로가 있습니다. [Apple enrollment](https://developer.apple.com/programs/enroll/)
- 앱 출시: Apple Push Notification Console은 development environment에서 device token으로 테스트 발송을 지원하며 non-admin 팀원도 development push를 보낼 수 있다고 설명합니다. 따라서 App Store 출시가 APNs/FCM 시험의 선행조건이라는 근거는 없습니다. [Apple Push Notification Console](https://developer.apple.com/documentation/usernotifications/testing-notifications-using-the-push-notification-console)

반대 근거와 한계:

- 예제의 “iOS 16+ 시뮬레이터도 FCM 푸시 일부 지원”, “시뮬레이터에서도 토큰은 받음”이라는 정확한 문구를 뒷받침하는 공식 출처는 이번 조회에서 찾지 못했습니다.
- Firebase 공식 setup은 오히려 Cloud Messaging에 physical device를 요구합니다. 따라서 해당 시뮬레이터 문구를 공식 우회로 계약에 넣으면 안 됩니다.
- Apple 문서는 무료 계정으로 일반 개발·개인 기기 테스트가 가능하다고 하지만, Push notifications capability는 무료 계정에 제공하지 않습니다. 두 출처는 충돌이 아니라 범위가 다릅니다.

## 3. 현행화 — 낡은 곳

| 파일:줄 | 현재 값 | 최신 확인값 | 판단·출처 |
|---|---|---|---|
| [fcm-ios-setup-guide.md:5](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/onboarding-kit/examples/fcm-ios-setup-guide.md:5), [line 29](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/onboarding-kit/examples/fcm-ios-setup-guide.md:29) | `Xcode 16+ · iOS 14+` | Firebase Apple SDK 공식 setup: `Xcode 26.2+`, 최소 `iOS 15` | 낡음. [Firebase Apple setup](https://firebase.google.com/docs/ios/setup) |
| [fcm-ios-example.html:249](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/onboarding-kit/fcm-ios-example.html:249) | `Xcode 16+` | `Xcode 26.2+` | 생성 HTML도 함께 낡음. MD를 고친 뒤 재생성해야 함. [Firebase Apple setup](https://firebase.google.com/docs/ios/setup) |
| [fcm-ios-setup-guide.md:31](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/onboarding-kit/examples/fcm-ios-setup-guide.md:31), [line 370](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/onboarding-kit/examples/fcm-ios-setup-guide.md:370), [line 392](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/onboarding-kit/examples/fcm-ios-setup-guide.md:392) | 시뮬레이터 토큰/FCM 일부 지원 | Cloud Messaging 사용 시 physical Apple device 요구 | 근거 미확보 및 공식 prerequisite와 어긋남. [Firebase Apple setup](https://firebase.google.com/docs/ios/setup) |
| [fcm-ios-example.html:251](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/onboarding-kit/fcm-ios-example.html:251), [line 605](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/onboarding-kit/fcm-ios-example.html:605) | 같은 시뮬레이터 주장 | physical device 요구 | 생성 HTML의 동일 drift. [Firebase Apple setup](https://firebase.google.com/docs/ios/setup) |
| [evals.json:9](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/onboarding-kit/skills/setup-guide/evals/evals.json:9), [line 68](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/onboarding-kit/skills/setup-guide/evals/evals.json:68) | `Last updated 2026-07-20 UTC` | 해당 Firebase 페이지들은 이번 조회에서 `Last updated 2026-09-24 UTC` | 출처 스냅샷 날짜가 낡음. [Flutter setup](https://firebase.google.com/docs/flutter/setup), [Apple FCM client](https://firebase.google.com/docs/cloud-messaging/ios/client) |
| [fcm-ios-setup-guide.md:4](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/onboarding-kit/examples/fcm-ios-setup-guide.md:4), [line 6](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/onboarding-kit/examples/fcm-ios-setup-guide.md:6), [line 210](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/onboarding-kit/examples/fcm-ios-setup-guide.md:210) | 2026-07-27/08-13 조회 | Firebase 문서 2026-09-24 갱신 | 재검증 날짜 갱신 필요. 절차가 전부 틀렸다는 뜻은 아님. |
| [fcm-ios-setup-guide.md:195](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/onboarding-kit/examples/fcm-ios-setup-guide.md:195) | Flutter iOS는 CocoaPods로 SDK 설치 | Firebase 공식 native 문서는 CocoaPods 생태계를 deprecated로 표시하고 Firebase 12가 CocoaPods에 배포되는 마지막 major라고 명시 | 위험 예고. 다만 FlutterFire의 현행 설치 구현과 native 신규 프로젝트 권고는 범위가 달라 즉시 SPM으로 바꾸면 안 됨. [Firebase Apple setup](https://firebase.google.com/docs/ios/setup) |
| [plan-2026-05-18.md:375](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/onboarding-kit/plan-2026-05-18.md:375), [line 836](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/onboarding-kit/plan-2026-05-18.md:836) | `stripe.com/docs/` | `docs.stripe.com/` | 역사 문서에 구 호스트 잔존. 런타임 [search-strategy.md:17](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/onboarding-kit/skills/setup-guide/references/search-strategy.md:17)은 이미 올바름. [Stripe docs](https://docs.stripe.com/) |

현재 안정 버전:

- `firebase_messaging` 16.7.0, 2026-09-14 공개; Flutter `>=3.27.0`, Dart `^3.6.0`, `firebase_core ^4.14.0`. [pub.dev](https://pub.dev/packages/firebase_messaging)
- `firebase_core` 4.15.0, 2026-09-14 공개; Flutter `>=3.27.0`, Dart `^3.6.0`. [pub.dev](https://pub.dev/packages/firebase_core)
- `flutterfire_cli` 1.4.1, 2026-08-03 공개; Dart `^3.6.0`. [pub.dev](https://pub.dev/packages/flutterfire_cli)
- FlutterFire `firebase_messaging` 16.0.0은 deprecated 함수 제거 및 Firebase iOS SDK 12.0.0 전환을 breaking change로 명시합니다. 16.7.0에는 Dart `Firebase.initializeApp()` 뒤 APNs 등록, UIScene launch callback 관련 iOS 수정이 들어갔습니다. [changelog](https://github.com/firebase/flutterfire/blob/main/packages/firebase_messaging/firebase_messaging/CHANGELOG.md)
- Firebase Apple SDK 최신 릴리스는 12.19.2이며 SPM-only 릴리스입니다. FlutterFire 4.15.0/16.7.0 changelog는 Firebase iOS SDK 12.19.0 사용을 기록합니다. [Apple SDK 12.19.2](https://github.com/firebase/firebase-ios-sdk/releases/tag/12.19.2), [firebase_core changelog](https://github.com/firebase/flutterfire/blob/main/packages/firebase_core/firebase_core/CHANGELOG.md)
- 예제는 패키지 버전을 고정하지 않고 레지스트리 조회를 요구하므로 [fcm-ios-setup-guide.md:181](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/onboarding-kit/examples/fcm-ios-setup-guide.md:181)의 정책 자체는 현행입니다.

추가 현행 보안 원칙:

- Google Cloud는 가능하면 실행 리소스에 service account를 연결하고, 외부 워크로드에는 Workload Identity Federation을 사용하며, service-account key 생성은 그 방법들을 쓸 수 없을 때의 분기로 둡니다. [Google Cloud authentication](https://cloud.google.com/docs/authentication)
- 현재 format checklist의 “JSON service account를 안전 저장”은 이미 키가 있을 때의 보관 지침이라 틀린 것은 아닙니다. 추론: 향후 GCP 가이드는 JSON 키 생성을 기본 경로처럼 쓰지 않는다는 계약을 추가할 가치가 있습니다.

## 4. 권장안

Phase 14 계약 조건으로 삼을 만한 항목:

1. CI의 validate job에 다음 순서를 계약합니다.

   - `command -v zsh`로 확인
   - 없을 때만 `sudo apt-get update && sudo apt-get install -y zsh`
   - `sh howto-kit/evals/run-evals.sh`
   - onboarding 전용 runner 실행

2. onboarding runner는 `SKILL.md`의 `guide_gate` 코드 블록을 실행 시 추출해야 합니다. 함수 사본을 별도 파일에 두지 않습니다.

3. onboarding `evals.json`에는 최소 다음 네 판정을 명시적으로 등록합니다.

   - 정상 Flutter + `flutter` → `GATE_PASS`
   - 정상 Flutter + 빈 stack → `G3_STACKMIX FAIL stack=unset swift_fence=0`
   - 한국어 출처 토큰 있음 → `G4_DEPRECATION PASS unsourced_boxes=0`
   - 한국어 출처 토큰 없음 → `G4_DEPRECATION FAIL unsourced_boxes=1`

4. 모든 경우를 bash와 zsh에서 실행하고 전체 출력을 비교합니다. 한 셸만 성공하거나 출력이 다르면 실패로 판정합니다.

5. `format-checklist.md` §2에는 막는 요구마다 다음 세 필드를 강제합니다.

   - 1차 출처 URL
   - 정확히 막히는 작업
   - 출처가 제시하는 우회 한 가지, 없으면 `우회 없음(출처 확인)`

6. FCM 예제에는 다음 수준으로 적는 것이 근거에 맞습니다.

   - `실기기 필요`
   - 출처: Firebase Apple setup
   - 차단 범위: APNs/FCM 원격 메시지 수신·발송 검증
   - 비차단 범위: 프로젝트 생성, Firebase 구성, 일반 앱 실행
   - 우회: `우회 없음(실제 FCM 원격 수신에 대해 출처 확인)`  
     시뮬레이터를 FCM 수신 우회로 단정하지 않음.

7. 유료 계정 요구는 다음처럼 범위를 좁힙니다.

   - 차단: Push Notifications capability, APNs 키/프로파일 구성
   - 비차단: 일반 앱 개발과 기본 개인 기기 테스트
   - 우회: 자격 있는 비영리·교육기관·정부 기관은 fee waiver; 그 밖에는 공식 우회 확인 못 함.

8. “앱 출시 필요”는 FCM 시험 요구사항으로 쓰지 않습니다. development environment에서 시험 발송이 가능하다는 Apple 근거가 있습니다.

9. Markdown 원본을 먼저 고치고 HTML을 재생성한 뒤 두 산출물에 옛 문구가 남지 않았는지 검사합니다.

10. 최신 버전 계약은 숫자를 예제 본문에 고정하기보다 레지스트리 실측값과 조회일을 기록하는 현재 정책을 유지합니다. 단, 최소 Xcode/iOS 요구처럼 설치 가능성을 결정하는 기준은 명시적으로 현행화합니다.

## 5. 못 가져온 것 / 열린 질문

- “iOS 16+ 시뮬레이터는 FCM 토큰을 받고 일부 원격 푸시도 지원한다”는 예제 문장을 직접 지지하는 공식 출처를 찾지 못했습니다. 없다는 뜻은 아니지만 이번 Phase 근거로는 사용할 수 없습니다.
- Firebase native Apple 문서는 CocoaPods를 deprecated로 선언했지만, FlutterFire가 CocoaPods 없이 모든 Flutter iOS 프로젝트를 지원한다는 공식 전환 지침은 찾지 못했습니다. 따라서 Phase 14에서 Flutter 예제를 곧바로 SPM 절차로 바꾸면 안 됩니다.
- GitHub Ubuntu 이미지에서 zsh가 절대 설치되지 않는다는 명시적 문장은 찾지 못했습니다. 공식 제공 목록·현행 이미지 manifest에서 보장되지 않는 것까지만 확인했습니다.
- Apple의 로그인 뒤 실제 콘솔 버튼·라벨은 공개 문서만으로 검증할 수 없습니다. 공개 Help에 나온 상위 섹션과 필드명까지만 계약해야 합니다.
- 사용자 피드백 메모리는 이번 Stop rule에 필요한 공식 근거와 레포 실측이 이미 확보돼 추가 조회하지 않았습니다.
