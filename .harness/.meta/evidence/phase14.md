---
phase: 14
title: "Phase 14 onboarding-kit — 확보된 외부 근거"
collected: 2026-08-13
method: codex (foreground, 직접 호출)
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치·설정 키를 지어내지 마라.
---

출처 유형: WebSearch fallback (검색 1회, 직접 URL fetch 중심)

**1. 관찰 사실**
M1. 스택 혼용은 여전히 유효합니다. 현행 FlutterFire 기본 절차는 `flutterfire configure`와 `lib/main.dart`의 Dart 초기화 흐름이며, Flutter setup 문서에는 `AppDelegate.swift`의 `FirebaseApp.configure()` 단계가 나오지 않습니다.  Flutter FCM 문서도 iOS 쪽에서 요구하는 것은 Xcode Capability 설정, APNs 인증 키 업로드, `firebase_messaging` 추가, Dart API로 토큰 조회입니다. `Info.plist` 수정은 자동 초기화를 끄는 경우의 선택 단계입니다. ([firebase.google.com](https://firebase.google.com/docs/cloud-messaging/flutter/get-started))  
따라서 [fcm-ios-setup-guide.md](/Users/jackson/Hub/10_Dev/claude-plugins/docs/onboarding-kit/examples/fcm-ios-setup-guide.md:174)의 Flutter 예제에서 `AppDelegate.swift` + `FirebaseApp.configure()`를 최소 필수처럼 둔 것은 현행 FlutterFire 절차와 어긋납니다. 네이티브 iOS 문서의 Swift 절차를 Flutter 가이드에 섞은 상태입니다.

M1 보조. APNs 키는 여전히 `.p8` 형식입니다. Apple은 다운로드한 private key가 `.p8` 확장자로 저장된다고 설명하고, Firebase Flutter FCM 문서는 `.p8`, key ID, Apple team ID 입력 후 저장하는 흐름을 둡니다.  ([firebase.google.com](https://firebase.google.com/docs/cloud-messaging/flutter/get-started)) 다만 `.p12` APNs Certificate를 “deprecated”라고 단정하는 로컬 예제/HTML 문구는 근거가 약합니다. 현재 FCM 문서에서 명시적으로 deprecated로 부르는 것은 Instance ID API 쪽이고, APNs 인증 키를 안내한다고 해서 `.p12`를 deprecated로 승격하면 안 됩니다. 

M2. 콘솔 UI 라벨 이슈도 여전히 유효합니다. Firebase 공식 문서에서 확인 가능한 라벨은 `Settings > General`, `Cloud Messaging tab`, `APNs authentication key`, `iOS app configuration`, `Upload/Save`, 테스트 발송의 `DevOps & Engagement > Messaging`, `New campaign`, `Notifications`, `Send test message`, `Add an FCM registration token`, `Test`입니다. ([firebase.google.com](https://firebase.google.com/docs/cloud-messaging/flutter/get-started))  
미확인: Firebase Console / Apple Developer Portal의 로그인 뒤 실시간 UI는 fetch로 직접 확인 불가입니다. 이번 점검에서 인용 가능한 것은 public docs/help에 노출된 라벨뿐입니다.

M2 보조. Apple public Help의 현행 섹션명은 `Certificates`, `Keys`, `Identifiers`, `Capabilities`, `Provisioning Profiles` 등으로 확인됩니다. App ID 등록은 `Identifiers`, APNs 키는 `Keys`, 프로비저닝은 `Provisioning Profiles` 아래입니다.   

M3. Apple 사이트 구분은 여전히 유효하지만, “셋업의 99%가 Developer Portal” 표현은 과합니다.

| 작업 | 현행 사이트 | 확인된 섹션/흐름 |
|---|---|---|
| Bundle ID / App ID 등록 | Apple Developer Account | `Certificates, Identifiers & Profiles` → `Identifiers` → App IDs 등록.  |
| APNs 키 생성 | Apple Developer Account | `Certificates, Identifiers & Profiles` → `Keys`; APNs service 선택, `.p8` 다운로드.  |
| 인증서 | Apple Developer Account | `Certificates` 섹션. 수동 development provisioning에는 App ID, development certificate, registered device가 필요합니다.  |
| Provisioning Profile | Apple Developer Account | `Profiles` / `Provisioning Profiles`; development 및 App Store Connect distribution profile 생성.   |
| 앱 레코드 생성 | App Store Connect | `Apps` → `+` → `New App`.  |
| 빌드 업로드 | App Store Connect | 앱 추가 후 Xcode/Transporter/API 등으로 업로드; build는 bundle ID + version + build string으로 연결됩니다.  |
| TestFlight | App Store Connect | beta build 배포, 테스터 관리, 피드백 수집.  |

기타 출처 점검: Stripe 현행 문서 호스트는 `docs.stripe.com`이며, 개발환경 문서는 언어별 variant URL을 제공합니다.   GCP는 `cloud.google.com/docs`가 `docs.cloud.google.com/docs`로 리다이렉트되며, 서비스 계정/ADC 문서는 `docs.cloud.google.com` 최종 URL로 확인됩니다.   

**2. 권장안**
- Flutter FCM 예제에서 `AppDelegate.swift` / `FirebaseApp.configure()` 필수 단계를 제거하고, Xcode Capability + APNs key + FlutterFire CLI + Dart 초기화로 갱신.
- `.p12`를 deprecated로 단정한 예제/HTML 문구를 제거. “현행 가이드는 `.p8` APNs authentication key를 안내한다” 정도로 낮추기.
- Firebase 테스트 메시지 경로를 `DevOps & Engagement > Messaging` 기준으로 갱신.
- Apple 사전 요구사항 표를 작업별 사이트 표로 바꾸고, App Store Connect가 앱 레코드/TestFlight/빌드 업로드에는 필요하다는 점을 반영.
- 생성 HTML 문서에 남은 `stripe.com/docs`는 `docs.stripe.com`로 갱신. GCP 출처 원장은 최종 리다이렉트 URL인 `docs.cloud.google.com`도 허용/기록.

**3. 트레이드오프**
- public docs 라벨은 live console보다 안정적으로 인용 가능하지만, 로그인 뒤 실제 UI와 100% 동일하다고 보장할 수는 없습니다.
- “Flutter는 네이티브 코드 수정 없음”은 “Xcode 프로젝트 설정도 없음”이 아닙니다. Capability/Background mode 설정은 여전히 iOS 프로젝트 작업입니다.
- `.p12 deprecated` 표현을 빼면 경고 강도는 약해지지만, 출처보다 강한 주장을 하지 않는 쪽이 맞습니다.

**4. 열린 질문**
- `docs/onboarding-kit/*.html`을 배포 문서이자 템플릿처럼 관리하는지, 아니면 소스 MD만 정본인지 확인 필요.
- FCM Flutter 예제는 즉시 수정 대상인지, 과거 dogfood 산출물로 보존할지 결정 필요.
- 로그인 뒤 실제 Firebase/Apple UI 라벨 검증이 필요하면 계정 접근 가능한 별도 수동 검증이 필요합니다.

---

## 부록 — Step F1 시점 추가 등재 (2026-08-13)

**이 항목은 Phase 14 실행 이후 Step F1 Final QA 의 지적(ER-01)으로 추가됐다.** 원 근거 수집분이 아니다.
투명성을 위해 별도 절로 분리해 표기한다.

- <https://pub.dev/packages/firebase_core> — **실재 확인** (codex foreground, 2026-08-13).
  publisher `firebase.google.com`, 확인 시점 stable **4.13.0**.
  FlutterFire 의 Core API Flutter 플러그인으로 여러 Firebase app 연결을 담당한다.

**경위**: `docs/onboarding-kit/examples/fcm-ios-setup-guide.md:181` 이 `firebase_messaging` 과
`firebase_core` 를 sibling 으로 함께 인용하는데, 원 근거 수집 시 `firebase_messaging` 만 등재되어
`firebase_core` 가 "근거 파일에 없는 URL" 로 남았다. F1 QA 가 이를 미추적 URL 1 건으로 검출했다.
**등재 전에 실재를 확인했고, 확인 없이 채우지 않았다.**

**개선 제안 (다음 사이클)**: 근거 파일에 URL 을 등재할 때 같은 패턴의 sibling 리소스
(`firebase_core` ↔ `firebase_messaging` 류)를 함께 등재하는 체크리스트가 필요하다.
