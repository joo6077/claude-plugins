# FCM iOS (Apple) 푸시 알림 설정 가이드

> 작성일: 2026-05-18
> 기준: Firebase iOS SDK 11.x · Xcode 16+ · iOS 14+ · Apple Developer Program 가입 필요
> 공식 문서: https://firebase.google.com/docs/cloud-messaging/ios/client

## 사전 요구사항

> **⚠️ 사이트 혼동 주의:** FCM 셋업의 Apple 쪽 작업은 **Apple Developer Portal** (`developer.apple.com/account`)에서 합니다. **App Store Connect** (`appstoreconnect.apple.com`)는 앱 출시/심사용으로 완전히 다른 사이트입니다. 출시 단계에서만 그쪽으로 갑니다.

- [ ] **Apple Developer Program 가입** (연 $99) — Account Holder 또는 Admin 권한
- [ ] **Firebase 프로젝트** 존재 — Editor 이상 권한
- [ ] **Xcode 16+** 설치 — `xcodebuild -version`으로 확인
- [ ] **앱 Bundle ID 확정** — 예: `com.yourorg.fitpal`. **등록 후 변경 불가** (아래 "Bundle ID 변경 정책" 참고)
- [ ] **실기기** — FCM은 시뮬레이터에서도 토큰은 받지만 발송 테스트는 실기기 필요 (iOS 16+는 시뮬레이터도 일부 지원)

---

## Step 1 — Apple Developer에서 App ID에 Push 활성화

**어디서:** https://developer.apple.com/account → Certificates, Identifiers & Profiles → 좌측 사이드바 **Identifiers**

**무엇을:**

1. Identifiers 페이지 상단의 **`+`** 버튼 클릭
2. 식별자 유형 선택 화면에서 **App IDs** 선택 → **Continue**
3. "Register an identifier" 화면에서 **App ID Type: Explicit** 선택 → **Continue** (Wildcard는 Push Notifications에 사용 불가)
4. **Description** 입력 (예: "Fit Pal Production") + **Bundle ID** 입력 (예: `com.yourorg.fitpal`)
5. Capabilities 섹션에서 **Push Notifications** 체크박스 활성화
6. **Continue** → 검토 페이지 확인 → **Register**

> **⚠️ 주의:** Apple은 App Store Connect에 빌드를 한 번이라도 업로드한 뒤에는 해당 앱의 Bundle ID 변경을 허용하지 않습니다. 출시 후 변경이 필요하면 신규 Bundle ID로 새 App ID를 만들고 Firebase iOS 앱·Provisioning Profile도 새로 구성해야 함. (테스트 단계에서는 자유롭게 갈아치울 수 있음.)

**확인 방법:** Identifiers 목록에 방금 만든 App ID가 보이고, 상세 진입 시 Capabilities 섹션에서 Push Notifications가 활성화 표시.

---

## Step 2 — APNs Authentication Key (.p8) 발급

> **❌ Deprecated:** APNs Certificate (.p12) 방식 — 매년 갱신 필요, 환경별로 분리. 2020년 이후로 권장하지 않음.
> **✅ 현재 권장:** APNs Authentication Key (.p8) — 갱신 불필요, 하나로 dev/prod 모두 커버, Team 전체 앱 공유 가능.

**어디서:** https://developer.apple.com/account → Certificates, Identifiers & Profiles → 좌측 사이드바 **Keys**

**무엇을:**

1. Keys 페이지 상단의 **`+`** 버튼 클릭
2. **Key Name** 입력 (예: "FCM APNs Key")
3. 서비스 체크리스트에서 **Apple Push Notification service** 체크
4. 같은 행의 **Configure** 버튼 클릭
5. 구성 화면에서 **Environment** 선택 (Production / Development / Sandbox & Production — 하나로 dev/prod 모두 커버하려면 마지막 옵션)
6. **Key Restriction** 선택: **Team Scoped (All Topics)** 권장 (해당 Team의 모든 앱에 사용 가능) 또는 **Topic Specific** (특정 Bundle ID로 제한)
7. **Save** → 이전 화면으로 복귀 → **Continue**
8. 검토 페이지 확인 → **Register**
9. **Download** 버튼 클릭 — `.p8` 파일을 안전한 곳(1Password, GCP Secret Manager 등)에 저장
10. **Key ID** (10자리 영숫자) 메모 — 예: `ABCD123XYZ`
11. **Team ID** 확인 — Apple Developer 사이트 우측 상단 계정 메뉴 → **Membership Details**, 또는 `developer.apple.com/account` 메인 페이지 상단 (10자리)

> **🔒 보안 경고:** .p8 파일은 **단 한 번만** 다운로드 가능. 분실 시 Key를 revoke하고 새로 발급해야 함. **절대 git에 커밋하지 말 것**.

**확인 방법:** Keys 목록에 Key Name이 보이고, Key ID가 표시됨. .p8 파일이 다운로드 폴더에 존재.

---

## Step 3 — Xcode에서 Capability 추가

**어디서:** Xcode → 프로젝트 네비게이터 → 앱 타겟 선택 → **Signing & Capabilities** 탭

**무엇을:**

1. 상단 `+ Capability` 클릭
2. **Push Notifications** 검색 → 더블클릭으로 추가
3. 다시 `+ Capability` → **Background Modes** 추가
4. Background Modes 항목에서 **Remote notifications** 체크

> **⚠️ 주의:** 백그라운드 silent push가 필요 없다면 Background Modes는 안 넣어도 되지만, FCM의 data-only 메시지를 백그라운드에서 처리하려면 필수.

**확인 방법:** Signing & Capabilities 탭에 Push Notifications + Background Modes 섹션이 모두 보임. 빌드 시 `Provisioning profile doesn't include the aps-environment entitlement` 에러가 없음.

---

## Step 4 — FlutterFire CLI로 Firebase 자동 구성

> **Flutter 프로젝트는 콘솔에서 수동 등록·.plist 드래그를 하지 않습니다.** `flutterfire configure` 명령어가 iOS 앱 콘솔 등록, `GoogleService-Info.plist` 배치, `lib/firebase_options.dart` 생성까지 한 번에 자동 처리합니다.

**어디서:** 프로젝트 루트 (`pubspec.yaml`이 있는 디렉토리) 터미널

**무엇을:**

1. FlutterFire CLI 전역 설치 (최초 1회):

   ```bash
   dart pub global activate flutterfire_cli
   ```

2. Firebase CLI 로그인 (안 한 경우):

   ```bash
   firebase login
   ```

3. 프로젝트 루트에서 구성 명령 실행:

   ```bash
   flutterfire configure
   ```

4. 대화형 프롬프트:
   - **Firebase 프로젝트 선택** — 이미 콘솔에 만들어둔 프로젝트 선택
   - **빌드할 플랫폼 선택** — 최소 `ios` 체크 (필요시 `android` 동시)
   - **iOS Bundle ID** — Xcode `Signing & Capabilities` 탭의 Bundle Identifier와 정확히 일치해야 함 (예: `com.fitpal.test`)

5. 명령 완료 시 자동 생성/배치:
   - `ios/Runner/GoogleService-Info.plist` (Xcode 프로젝트에 자동 추가)
   - `lib/firebase_options.dart` (`DefaultFirebaseOptions.currentPlatform` 제공)
   - Firebase 콘솔에 iOS 앱 자동 등록

> **⚠️ 주의:** Bundle ID 오타로 잘못된 ID로 등록됐다면 Firebase 콘솔 → 프로젝트 설정 → iOS 앱 카드에서 삭제 후 `flutterfire configure` 재실행.

**확인 방법:**
- `ls ios/Runner/GoogleService-Info.plist` → 파일 존재
- `ls lib/firebase_options.dart` → 파일 존재
- Firebase Console → 프로젝트 개요에 iOS 앱이 표시됨

---

## Step 5 — Firebase 콘솔에 APNs Key 업로드

**어디서:** Firebase Console → 프로젝트 설정 ⚙️ → **클라우드 메시징 (Cloud Messaging)** 탭 → **Apple 앱 구성 (Apple app configuration)** 섹션

**무엇을:**

1. iOS 앱 카드에서 **APNs 인증 키 (APNs authentication key)** 항목의 **업로드 (Upload)** 버튼 클릭
2. `.p8` 파일 선택 (Step 2에서 받은 파일) → **Open**
3. **Key ID** 입력 (Step 2에서 메모한 10자리 값)
4. **Team ID** 입력 — 공식 문서상 Key ID만 명시되어 있지만 실제 콘솔 폼에는 Team ID 필드도 표시되므로 함께 입력 (Step 2에서 확인한 10자리 값)
5. **업로드 (Upload)** 클릭

**확인 방법:** APNs 인증 키 항목에 Key ID가 표시되고, 상태 표시(체크 또는 "등록됨")가 보임.

---

## Step 6 — firebase_core + firebase_messaging 패키지 추가

**어디서:** 프로젝트의 `pubspec.yaml`

**무엇을:**

`dependencies` 섹션에 아래 두 패키지를 추가:

```yaml
dependencies:
  firebase_core: ^3.6.0       # 최신 안정 버전 (pub.dev에서 확인)
  firebase_messaging: ^15.1.0
```

터미널에서:

```bash
flutter pub get
```

iOS 쪽 CocoaPods는 다음 `flutter run` 또는 `flutter build ios` 시 자동으로 `pod install`이 실행되어 firebase-ios-sdk가 설치됩니다.

> **⚠️ 주의:** 버전은 [pub.dev/packages/firebase_messaging](https://pub.dev/packages/firebase_messaging)에서 매번 최신 확인. `firebase_core`와 `firebase_messaging`의 메이저 버전은 [호환 매트릭스](https://firebase.flutter.dev/docs/overview/#compatibility-matrix)를 따라야 함 (다른 firebase_* 패키지도 같은 메이저로 맞출 것).

**확인 방법:**
- `pubspec.lock`에 `firebase_core`, `firebase_messaging` 항목 존재
- VSCode에서 `import 'package:firebase_messaging/firebase_messaging.dart';` 자동완성됨
- `ls ios/Podfile.lock` 후 grep으로 `Firebase/Messaging` 확인

---

## Step 7 — AppDelegate.swift (최소) + Dart 초기화/권한/토큰 코드

> Flutter에서는 FCM 토큰·권한·메시지 수신을 모두 **Dart에서** 처리합니다. `AppDelegate.swift`는 Firebase 초기화 한 줄만 담당.

### 7-1. iOS AppDelegate.swift

**파일:** `ios/Runner/AppDelegate.swift`

```swift
import UIKit
import Flutter
import FirebaseCore

@main
@objc class AppDelegate: FlutterAppDelegate {
  override func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
  ) -> Bool {
    FirebaseApp.configure()  // 이 한 줄만 추가
    GeneratedPluginRegistrant.register(with: self)
    return super.application(application, didFinishLaunchingWithOptions: launchOptions)
  }
}
```

### 7-2. Dart 초기화 (main.dart)

**파일:** `lib/main.dart`

```dart
import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'firebase_options.dart';

// 백그라운드 메시지 핸들러는 반드시 top-level + @pragma 어노테이션
@pragma('vm:entry-point')
Future<void> _firebaseMessagingBackgroundHandler(RemoteMessage message) async {
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  print('Background message: ${message.messageId}');
}

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );

  // 백그라운드 핸들러 등록 (앱이 죽거나 백그라운드일 때 메시지 수신)
  FirebaseMessaging.onBackgroundMessage(_firebaseMessagingBackgroundHandler);

  runApp(const MyApp());
}
```

### 7-3. 권한 요청 + 토큰 획득 + 메시지 리스너

앱 초기 진입(첫 화면 `initState` 또는 시작 액션) 시점에:

```dart
import 'package:firebase_messaging/firebase_messaging.dart';

Future<void> setupFcm() async {
  final messaging = FirebaseMessaging.instance;

  // iOS는 명시적 권한 요청 필수
  final settings = await messaging.requestPermission(
    alert: true,
    badge: true,
    sound: true,
  );

  if (settings.authorizationStatus == AuthorizationStatus.authorized ||
      settings.authorizationStatus == AuthorizationStatus.provisional) {
    // FCM 토큰 — 서버에 사용자별로 저장
    final token = await messaging.getToken();
    print('FCM token: $token');
    // TODO: 서버에 token 저장

    // 토큰 갱신 리스너
    messaging.onTokenRefresh.listen((newToken) {
      // TODO: 서버에 새 토큰 업데이트
    });
  }

  // iOS 포그라운드 알림 배너/사운드 표시
  await messaging.setForegroundNotificationPresentationOptions(
    alert: true,
    badge: true,
    sound: true,
  );

  // 포그라운드 메시지 수신
  FirebaseMessaging.onMessage.listen((RemoteMessage message) {
    print('Foreground: ${message.notification?.title} - ${message.notification?.body}');
  });

  // 알림 탭하여 앱이 열렸을 때
  FirebaseMessaging.onMessageOpenedApp.listen((RemoteMessage message) {
    print('App opened from notification: ${message.data}');
  });
}
```

**확인 방법:** 실기기/시뮬레이터에서 앱 실행 → iOS 권한 다이얼로그 표시 → 허용 → Dart 콘솔(`flutter logs` 또는 VSCode Debug Console)에 `FCM token: <긴 문자열>` 출력.

---

## Step 8 — 테스트 메시지 발송

**어디서:** Firebase Console → 좌측 메뉴 **Messaging** → **새 캠페인** → **알림**

**무엇을:**

1. 알림 제목/본문 입력 → **테스트 메시지 보내기** 버튼
2. Step 7 콘솔에서 출력된 FCM 토큰을 붙여넣기 → `+` → **테스트**
3. 디바이스에 푸시 도착 확인

**확인 방법:** 실기기 잠금 화면 또는 배너에 알림 표시됨.

---

## 권한 / IAM

| 시스템 | 필요한 권한 | 누구에게 |
|--------|------------|----------|
| Apple Developer | Account Holder 또는 Admin | Step 1·2 수행자 |
| Firebase Console | Editor 이상 | Step 4·5 수행자 |
| 운영 단계 | Apple Developer는 Admin/Developer, Firebase는 Editor로 최소화 권장 | 일상 운영 |

## 비용

- **FCM**: 무료 (전송량 제한 없음, 2026년 5월 기준)
- **Apple Developer Program**: 연 $99 (이미 가입했다면 추가 비용 없음)
- Firebase 다른 서비스(Analytics 등) 추가 사용 시 별도 한도 확인

## 환경 분기 (dev / staging / prod)

- **APNs Key**: 하나로 dev/prod 모두 처리 가능 (Apple 정책). 환경별로 따로 만들 필요 없음
- **Firebase 프로젝트**: **환경별로 분리 권장** — dev/staging/prod 각각 별도 프로젝트 + 별도 `GoogleService-Info.plist`
- Xcode에서 Build Configuration 별로 다른 .plist를 번들링: Build Phases → Run Script로 `cp GoogleService-Info-${CONFIGURATION}.plist ${BUILT_PRODUCTS_DIR}/${PRODUCT_NAME}.app/GoogleService-Info.plist`

## Rollback / 정리

- **APNs Key revoke**: Apple Developer → Keys → 해당 키 선택 → `Revoke`. 즉시 무효화되고 해당 키로 발송된 push가 모두 실패. **신중하게**
- **Firebase에서 APNs Key 제거**: Firebase Console → 프로젝트 설정 → 클라우드 메시징 → APNs 인증 키 → 휴지통 아이콘. 새 키로 교체할 때만 사용
- **사용 중단**: Push Notifications capability를 Xcode에서 제거 + Firebase Messaging SDK 의존성 제거 + 앱 재배포

## 보안 체크리스트

- [ ] `.p8` 파일은 비밀 저장소(1Password / GCP Secret Manager / AWS Secrets Manager) 보관
- [ ] `.gitignore`에 `*.p8` 추가 (실수로 커밋 방지)
- [ ] `GoogleService-Info.plist`는 git에 커밋해도 무방 (공개 식별자만 포함) — 단, 환경별 분리 시 파일명 구분
- [ ] FCM 등록 토큰은 서버에 저장 시 사용자별로 격리 (다른 사용자에게 발송되지 않도록)
- [ ] Firebase Admin SDK의 서비스 계정 JSON은 **서버에만** 보관 (앱 번들에 절대 포함 금지)

## 검증 체크리스트

- [ ] 실기기에서 앱 실행 → Push 권한 허용 다이얼로그가 뜸
- [ ] Xcode 콘솔에 `FCM token: ...` 출력됨
- [ ] Firebase Console **테스트 메시지 보내기** 성공 → 실기기에 알림 도착
- [ ] 앱을 백그라운드로 보낸 상태에서도 푸시 도착
- [ ] 앱이 죽은 상태(force quit)에서도 푸시 도착
- [ ] 다른 환경(staging/prod) Firebase 프로젝트로 전환했을 때도 동일 동작

## 트러블슈팅

**증상:** Xcode 콘솔에 `FCM token: nil`이 계속 출력됨
**원인:** APNs 토큰이 먼저 와야 FCM 토큰이 생성됨. APNs 등록 실패가 원인일 가능성
**해결:**

1. `didFailToRegisterForRemoteNotificationsWithError` 콜백 구현 후 에러 메시지 확인
2. Provisioning Profile에 `aps-environment` entitlement 포함 확인 (Xcode → Signing & Capabilities → Push Notifications 추가됐는지)
3. 실기기인지 확인 (iOS 16 이전 시뮬레이터는 APNs 불가)

**증상:** Firebase Console 테스트 발송은 성공인데 디바이스에 알림 안 옴
**원인:** APNs Key 업로드 시 Key ID/Team ID 불일치
**해결:** Firebase Console → 프로젝트 설정 → 클라우드 메시징 → APNs 인증 키 행의 Key ID와 Apple Developer Keys 페이지의 ID 비교. 다르면 삭제 후 재업로드

**증상:** 앱이 죽은 상태에서 푸시가 안 옴
**원인:** 사용자가 Settings에서 푸시 권한을 끔, 또는 silent push만 보내고 있음
**해결:** 알림 페이로드에 `notification` 객체(title/body) 포함했는지 확인. `data`만 있으면 silent push로 분류되어 죽은 앱은 깨우지 않음

**증상:** App ID 등록 시 `An App ID with Identifier 'com.example.app' is not available` 에러
**원인:** Apple은 Bundle ID를 전 세계 Apple Developer 계정에 걸쳐 유니크하게 관리. `com.fitpal.app` 같은 흔한 조합은 다른 개발자가 이미 선점했을 확률이 높음. 한 번 선점되면 그 계정이 풀어주기 전까지 다른 누구도 못 씀
**해결:**

1. 본인/조직 식별자를 prefix에 더 강하게 박기 — `com.<github핸들>.fitpal`, `com.<도메인>.fitpal`, `dev.<조직>.fitpal`
2. 환경별 분리도 충돌 회피에 유리 — `com.<핸들>.fitpal.dev`, `.staging`, `.prod`
3. **본인 Team에 이미 같은 ID가 등록돼 있다면** Identifiers 목록에서 검색해서 재사용 가능 (충돌이 아니라 본인 계정 중복)

**증상:** App ID는 등록했는데 Xcode `Signing & Capabilities`에서 `No profiles for '...' were found` + `Your team has no devices` 워닝이 그대로 뜸
**원인:** App ID 등록과 Provisioning Profile 생성은 별개 단계. Xcode 자동 signing이 provisioning profile을 만들려면 Team에 등록된 디바이스가 최소 1개 필요
**해결:**

- **시뮬레이터로 진행** — 시뮬레이터는 provisioning profile 불필요. Xcode 좌측 상단에서 시뮬레이터 선택하면 워닝 무시 가능. iOS 16+ 시뮬레이터는 FCM 푸시도 일부 지원
- **실기기 등록** — iPhone을 Mac에 USB 연결 → Xcode 좌측 상단에서 그 디바이스 선택하면 자동으로 Apple Developer Devices에 등록됨 → Signing 화면에서 **Try Again** 클릭

**증상:** Xcode `+ Capability`에서 Push Notifications가 안 보이거나 회색으로 비활성화
**원인:** Apple Developer Portal의 App ID에 Push Notifications capability가 활성화 안 됨, 또는 Team을 무료 개인 계정으로 선택함 (개인 계정은 Push 사용 불가)
**해결:**

1. [Identifiers 페이지](https://developer.apple.com/account/resources/identifiers/list)에서 해당 App ID 클릭 → Capabilities 섹션 → Push Notifications 체크 확인. 미체크면 활성화 후 Save
2. Xcode `Signing & Capabilities` 탭에서 Team이 유료 Apple Developer Program 가입 계정인지 확인 (`Free` 표기가 있으면 Push 불가)
3. Xcode 재시작 후 자동 동기화 대기 (수 초~수 분)
