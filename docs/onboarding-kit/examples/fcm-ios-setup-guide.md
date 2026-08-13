# FCM 푸시 알림 설정 가이드 — Flutter (iOS / Apple)

> **대상 스택: Flutter (FlutterFire).** 네이티브 Swift / Objective-C iOS 앱은 초기화 절차가 완전히 다르다 — 그 경우 이 가이드를 쓰지 말고 네이티브용 가이드를 따로 만든다.
> 작성일: 2026-05-18 · 최종 갱신: 2026-08-13
> 기준: Xcode 16+ · iOS 14+ · Apple Developer Program 가입 필요
> 대표 1차 출처: [Firebase — Set up FCM on Flutter](https://firebase.google.com/docs/cloud-messaging/flutter/get-started) (조회 2026-08-13)
> 이 대표 URL 은 각 Step 의 `**출처:**` 줄을 **대체하지 않는다** — Step 마다 그 Step 의 근거를 따로 적었다.

## 사전 요구사항

> **⚠️ 사이트 혼동 주의 — 작업마다 사이트가 다릅니다.** "셋업은 전부 Developer Portal" 이 아닙니다. 키·식별자 발급은 Apple Developer Account, **앱이라는 레코드와 배포는 App Store Connect** 입니다.

| 작업 | 사이트 | 섹션 / 흐름 |
| --- | --- | --- |
| Bundle ID / App ID 등록 | [Apple Developer Account](https://developer.apple.com/account) | `Certificates, Identifiers & Profiles` → `Identifiers` → App IDs |
| APNs 키 생성 | Apple Developer Account | `Certificates, Identifiers & Profiles` → `Keys` (APNs service 선택 → `.p8` 다운로드) |
| 인증서 | Apple Developer Account | `Certificates` |
| Provisioning Profile | Apple Developer Account | `Profiles` / `Provisioning Profiles` |
| 앱 레코드 생성 | [App Store Connect](https://appstoreconnect.apple.com) | `Apps` → `+` → `New App` |
| 빌드 업로드 | App Store Connect | 앱 추가 후 Xcode / Transporter / API 로 업로드 (build 는 bundle ID + version + build string 으로 연결) |
| TestFlight | App Store Connect | beta build 배포 · 테스터 관리 · 피드백 수집 |

**이 가이드(FCM 셋업)는 위 표의 1~2 행만 씁니다.** 실기기 베타 배포로 넘어가면 App Store Connect 가 필요합니다.

> **ℹ️ 콘솔 라벨 경계:** 이 가이드의 섹션명·버튼 라벨은 **로그인 없이 볼 수 있는 공식 문서**에서 확인한 것입니다. 콘솔에 로그인한 뒤의 실제 화면은 공개 문서로 검증할 수 없어 표기가 다를 수 있습니다 (A/B 롤아웃·언어 설정). 화면에서 못 찾으면 **상위 섹션명**(`Identifiers`, `Keys`, `Cloud Messaging`, `Messaging`)으로 검색하세요.

- [ ] **Apple Developer Program 가입** (연 $99) — Account Holder 또는 Admin 권한
- [ ] **Firebase 프로젝트** 존재 — Editor 이상 권한
- [ ] **Xcode 16+** 설치 — `xcodebuild -version`으로 확인
- [ ] **앱 Bundle ID 확정** — 예: `com.yourorg.fitpal`. **등록 후 변경 불가** (아래 "Bundle ID 변경 정책" 참고)
- [ ] **실기기** — FCM은 시뮬레이터에서도 토큰은 받지만 발송 테스트는 실기기 필요 (iOS 16+는 시뮬레이터도 일부 지원)

---

## Step 1 — Apple Developer에서 App ID에 Push 활성화

**출처:** [Apple Developer Help — Account](https://developer.apple.com/help/account/) — 섹션 구조 조회 2026-07-27 (`references/search-strategy.md` 실측 기록) · 작업↔사이트 대응 재확인 2026-08-13. 로그인 뒤 버튼 단위 화면은 공개 문서 범위 밖이다 (위 ℹ️ 참조)

**어디서:** [developer.apple.com/account](https://developer.apple.com/account) → `Certificates, Identifiers & Profiles` → 좌측 사이드바 `Identifiers`

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

**출처:** [Apple Developer Help — Account](https://developer.apple.com/help/account/) (`Keys` 섹션 · 조회 2026-07-27) + [Firebase — Set up FCM on Flutter](https://firebase.google.com/docs/cloud-messaging/flutter/get-started) (조회 2026-08-13 — `.p8` 파일 · key ID · Apple team ID 입력 흐름)

> **✅ 현행 가이드가 안내하는 방식:** APNs Authentication Key (`.p8`) — 갱신 불필요, 하나로 dev/prod 모두 커버, Team 전체 앱 공유 가능. Firebase FCM 문서는 `.p8` + Key ID + Team ID 를 입력해 저장하는 흐름을 안내한다.
>
> APNs Certificate (`.p12`) 방식도 여전히 존재하지만, **이 가이드는 1차 출처가 안내하는 `.p8` 흐름만 다룹니다.** 1차 출처가 `.p12` 를 어떤 강도로 평가하는지 이 가이드가 대신 판단하지 않습니다 — 출처보다 강한 주장을 쓰지 않기 위해서입니다.

**어디서:** [developer.apple.com/account](https://developer.apple.com/account) → `Certificates, Identifiers & Profiles` → 좌측 사이드바 `Keys`

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
11. **Team ID** 확인 — Apple Developer 사이트 계정 메뉴의 Membership 정보에서 확인 (10자리)

> **🔒 보안 경고:** .p8 파일은 **단 한 번만** 다운로드 가능. 분실 시 Key를 revoke하고 새로 발급해야 함. **절대 git에 커밋하지 말 것**.

**확인 방법:** Keys 목록에 Key Name이 보이고, Key ID가 표시됨. .p8 파일이 다운로드 폴더에 존재.

---

## Step 3 — Xcode 프로젝트에 Capability 추가

**출처:** [Firebase — Set up FCM on Flutter](https://firebase.google.com/docs/cloud-messaging/flutter/get-started) (조회 2026-08-13) — Flutter 앱의 iOS 쪽 요구사항으로 Xcode Capability 설정과 APNs 인증 키 업로드를 명시한다

> **Flutter 라도 이 단계는 건너뛸 수 없다.** "Flutter 는 네이티브 코드를 수정하지 않는다" 는 말은 **Swift 소스를 안 건드린다**는 뜻이지, **Xcode 프로젝트 설정도 안 한다**는 뜻이 아니다. Capability 와 Background Modes 는 소스가 아니라 iOS 프로젝트 설정이며 Flutter 앱에서도 필요하다.

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

**출처:** [FlutterFire — Flutter 설치/구성](https://firebase.google.com/docs/flutter/setup) (조회 2026-07-27 · 킷 evals `flutter-fcm-ios` 케이스에 기록된 실측) + [Firebase — Set up FCM on Flutter](https://firebase.google.com/docs/cloud-messaging/flutter/get-started) (조회 2026-08-13). 현행 Flutter 절차는 `flutterfire configure` → Dart 초기화이며, **네이티브 초기화 호출은 이 절차에 등장하지 않는다**

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
   - **iOS Bundle ID** — Xcode `Signing & Capabilities` 탭의 Bundle Identifier와 정확히 일치해야 함

5. 명령 완료 시 자동 생성/배치:
   - `ios/Runner/GoogleService-Info.plist` (Xcode 프로젝트에 자동 추가)
   - `lib/firebase_options.dart` (`DefaultFirebaseOptions.currentPlatform` 제공)
   - Firebase 콘솔에 iOS 앱 자동 등록

> **⚠️ 주의:** 생성 경로는 프로젝트 구조(flavor·모듈 분리)에 따라 달라질 수 있습니다. 위 두 경로는 명령 출력에 찍히는 실제 경로로 대조하세요 — 이름을 가정하지 말 것.
>
> Bundle ID 오타로 잘못된 ID로 등록됐다면 Firebase 콘솔의 프로젝트 설정에서 해당 iOS 앱을 삭제한 뒤 `flutterfire configure` 를 재실행합니다.

**확인 방법:**

```bash
ls ios/Runner/GoogleService-Info.plist lib/firebase_options.dart
```

두 파일이 모두 출력되고, Firebase Console 프로젝트 개요에 iOS 앱이 표시됨.

---

## Step 5 — Firebase 콘솔에 APNs Key 업로드

**출처:** [Firebase — Set up FCM on Flutter](https://firebase.google.com/docs/cloud-messaging/flutter/get-started) (조회 2026-08-13) — 문서에서 확인되는 라벨: `Settings` · `General` · `Cloud Messaging` 탭 · `iOS app configuration` · `APNs authentication key` · `Upload` / `Save`

**어디서:** Firebase Console → `Settings` (설정 ⚙️) → `General` (일반) → `Cloud Messaging` (클라우드 메시징) 탭 → `iOS app configuration` (iOS 앱 구성) 섹션

**무엇을:**

1. iOS 앱 카드에서 `APNs authentication key` (APNs 인증 키) 항목의 `Upload` (업로드) 클릭
2. `.p8` 파일 선택 (Step 2에서 받은 파일)
3. **Key ID** 입력 (Step 2에서 메모한 10자리 값)
4. **Team ID** 입력 (Step 2에서 확인한 10자리 값)
5. `Upload` / `Save` 클릭

> **ℹ️ 라벨 경계:** 위 클릭 경로는 공개 문서에 적힌 영문 라벨을 정본으로 하고 한국어를 괄호에 넣었습니다. 콘솔 언어 설정에 따라 한국어 표기가 다를 수 있으니 **영문 라벨 기준으로 찾으세요**.

**확인 방법:** `APNs authentication key` 항목에 Key ID가 표시되고 등록 상태 표시가 보임.

---

## Step 6 — firebase_core + firebase_messaging 패키지 추가

**출처:** [pub.dev — firebase_messaging](https://pub.dev/packages/firebase_messaging) · [pub.dev — firebase_core](https://pub.dev/packages/firebase_core) — **버전은 설치 시점에 레지스트리에서 직접 조회한다.** 이 가이드는 버전을 고정하지 않는다 (`references/search-strategy.md` §버전 확인은 패키지 레지스트리 우선 · 2026-07-27 실측: GitHub Releases 는 최신 버전 확인에 쓸 수 없었다)

**어디서:** 프로젝트 루트 터미널

**무엇을:**

```bash
flutter pub add firebase_core firebase_messaging
```

이 명령이 그 시점 최신 호환 제약을 `pubspec.yaml` 에 직접 써 줍니다.

> **⚠️ 버전 번호를 가이드에 박지 마세요.** 문서에 고정한 버전은 몇 달 뒤 반드시 틀립니다 — 이 문서의 이전 판이 그랬습니다. 여러 `firebase_*` 패키지를 함께 쓸 때는 각 패키지의 pub.dev 페이지에서 `firebase_core` 제약을 확인해 메이저를 맞춥니다.

iOS 쪽 CocoaPods는 다음 `flutter run` 또는 `flutter build ios` 시 자동으로 `pod install`이 실행되어 firebase-ios-sdk가 설치됩니다.

**확인 방법:**

```bash
grep -n 'firebase_core\|firebase_messaging' pubspec.lock
grep -n 'Firebase/Messaging' ios/Podfile.lock
```

두 명령 모두 결과 행을 출력하면 성공.

---

## Step 7 — Dart 초기화 · 권한 요청 · 토큰 획득

**출처:** [Firebase — Set up FCM on Flutter](https://firebase.google.com/docs/cloud-messaging/flutter/get-started) (조회 2026-08-13) + [FlutterFire — Flutter 설치/구성](https://firebase.google.com/docs/flutter/setup) (조회 2026-07-27). Flutter 절차는 `Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform)` 로 끝나며, 문서에 **네이티브 초기화 단계가 없다**

> **네이티브 소스를 건드리지 않습니다.** Flutter 에서 FCM 초기화·권한·토큰·메시지 수신은 **전부 Dart** 에서 처리하고, 네이티브 쪽 초기화는 `firebase_core` 플러그인이 담당합니다. `flutterfire configure` 가 이미 구성을 심어 뒀으므로 iOS 네이티브 소스 파일을 열 일이 없습니다.
>
> (Xcode **프로젝트 설정**은 Step 3 에서 이미 했습니다 — 그건 소스 수정이 아닙니다.)

### 7-1. Dart 초기화 (main.dart)

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
  debugPrint('Background message: ${message.messageId}');
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

### 7-2. 권한 요청 + 토큰 획득 + 메시지 리스너

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
    debugPrint('FCM token: $token');
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
    debugPrint('Foreground: ${message.notification?.title}');
  });

  // 알림 탭하여 앱이 열렸을 때
  FirebaseMessaging.onMessageOpenedApp.listen((RemoteMessage message) {
    debugPrint('App opened from notification: ${message.data}');
  });
}
```

**확인 방법:** 실기기에서 앱 실행 → iOS 권한 다이얼로그 표시 → 허용 → Dart 콘솔(`flutter logs` 또는 IDE Debug Console)에 `FCM token: <긴 문자열>` 출력.

---

## Step 8 — 테스트 메시지 발송

**출처:** [Firebase — Set up FCM on Flutter](https://firebase.google.com/docs/cloud-messaging/flutter/get-started) (조회 2026-08-13) — 문서에서 확인되는 라벨: `DevOps & Engagement` → `Messaging` · `New campaign` · `Notifications` · `Send test message` · `Add an FCM registration token` · `Test`

**어디서:** Firebase Console → `DevOps & Engagement` → `Messaging`

**무엇을:**

1. `New campaign` (새 캠페인) → `Notifications` (알림) 선택
2. 알림 제목/본문 입력 → `Send test message` (테스트 메시지 보내기) 클릭
3. Step 7 콘솔에서 출력된 FCM 토큰을 `Add an FCM registration token` 필드에 붙여넣고 추가
4. `Test` 클릭 → 디바이스에 푸시 도착 확인

**확인 방법:** 실기기 잠금 화면 또는 배너에 알림 표시됨.

---

## 권한 / IAM

| 시스템 | 필요한 권한 | 누구에게 |
| --- | --- | --- |
| Apple Developer | Account Holder 또는 Admin | Step 1·2 수행자 |
| Firebase Console | Editor 이상 | Step 4·5 수행자 |
| 운영 단계 | Apple Developer는 Admin/Developer, Firebase는 Editor로 최소화 권장 | 일상 운영 |

## 비용

- **FCM**: 무료 (전송량 제한 없음, 2026년 5월 확인 — 과금 정책은 Firebase 요금 페이지에서 재확인)
- **Apple Developer Program**: 연 $99 (이미 가입했다면 추가 비용 없음)
- Firebase 다른 서비스(Analytics 등) 추가 사용 시 별도 한도 확인

## 환경 분기 (dev / staging / prod)

- **APNs Key**: 하나로 dev/prod 모두 처리 가능 (Sandbox & Production 환경으로 발급한 경우). 환경별로 따로 만들 필요 없음
- **Firebase 프로젝트**: **환경별로 분리 권장** — dev/staging/prod 각각 별도 프로젝트 + 별도 `GoogleService-Info.plist`
- Xcode에서 Build Configuration 별로 다른 .plist를 번들링: Build Phases → Run Script로 `cp GoogleService-Info-${CONFIGURATION}.plist ${BUILT_PRODUCTS_DIR}/${PRODUCT_NAME}.app/GoogleService-Info.plist`

## Rollback / 정리

- **APNs Key revoke**: Apple Developer → `Keys` → 해당 키 선택 → `Revoke`. 즉시 무효화되고 해당 키로 발송된 push가 모두 실패. **신중하게**
- **Firebase에서 APNs Key 제거**: Firebase Console → `Settings` → `Cloud Messaging` → `APNs authentication key` 항목에서 삭제. 새 키로 교체할 때만 사용
- **사용 중단**: Push Notifications capability를 Xcode에서 제거 + `firebase_messaging` 의존성 제거 + 앱 재배포

## 보안 체크리스트

- [ ] `.p8` 파일은 비밀 저장소(1Password / GCP Secret Manager / AWS Secrets Manager) 보관
- [ ] `.gitignore`에 `*.p8` 추가 (실수로 커밋 방지)
- [ ] `GoogleService-Info.plist`는 git에 커밋해도 무방 (공개 식별자만 포함) — 단, 환경별 분리 시 파일명 구분
- [ ] FCM 등록 토큰은 서버에 저장 시 사용자별로 격리 (다른 사용자에게 발송되지 않도록)
- [ ] Firebase Admin SDK의 서비스 계정 JSON은 **서버에만** 보관 (앱 번들에 절대 포함 금지)

## 검증 체크리스트

- [ ] 실기기에서 앱 실행 → Push 권한 허용 다이얼로그가 뜸
- [ ] Dart 콘솔(`flutter logs`)에 `FCM token: ...` 출력됨
- [ ] Firebase Console `Send test message` 성공 → 실기기에 알림 도착
- [ ] 앱을 백그라운드로 보낸 상태에서도 푸시 도착
- [ ] 앱이 죽은 상태(force quit)에서도 푸시 도착
- [ ] 다른 환경(staging/prod) Firebase 프로젝트로 전환했을 때도 동일 동작

## 트러블슈팅

**증상:** Dart 콘솔에 `FCM token: null`이 계속 출력됨
**원인:** APNs 토큰이 먼저 와야 FCM 토큰이 생성됨. APNs 등록 실패가 원인일 가능성
**해결:**

1. Provisioning Profile에 `aps-environment` entitlement 포함 확인 (Xcode → Signing & Capabilities → Push Notifications 추가됐는지)
2. Firebase Console 에 APNs 인증 키가 실제로 업로드돼 있는지 확인 (Step 5)
3. 실기기인지 확인 (iOS 16 이전 시뮬레이터는 APNs 불가)

**증상:** Firebase Console 테스트 발송은 성공인데 디바이스에 알림 안 옴
**원인:** APNs Key 업로드 시 Key ID/Team ID 불일치
**해결:** Firebase Console `Settings` → `Cloud Messaging` → `APNs authentication key` 행의 Key ID와 Apple Developer `Keys` 페이지의 ID 비교. 다르면 삭제 후 재업로드

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
**원인:** Apple Developer 의 App ID에 Push Notifications capability가 활성화 안 됨, 또는 Team을 무료 개인 계정으로 선택함 (개인 계정은 Push 사용 불가)
**해결:**

1. [Identifiers 페이지](https://developer.apple.com/account/resources/identifiers/list)에서 해당 App ID 클릭 → Capabilities 섹션 → Push Notifications 체크 확인. 미체크면 활성화 후 Save
2. Xcode `Signing & Capabilities` 탭에서 Team이 유료 Apple Developer Program 가입 계정인지 확인 (`Free` 표기가 있으면 Push 불가)
3. Xcode 재시작 후 자동 동기화 대기 (수 초~수 분)
