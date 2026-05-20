# Project Detection — 스택 무관 탐지 패턴

`/setup-guide` 스킬이 프로젝트 스택을 자동 감지할 때 참조한다. 단일 스택부터 멀티 스택 모노레포까지 커버한다.

## 의존성 파일 → 스택 매핑

| 파일 (글로브 탐색) | 스택 | 비고 |
|------------------|------|------|
| `pubspec.yaml` | Flutter / Dart | `flutter:` 키 존재 시 Flutter 확정 |
| `Cargo.toml` | Rust | `[workspace]` 있으면 워크스페이스 |
| `package.json` | Node.js / JS | `dependencies` 안의 `react`/`next`/`vue` 등으로 세분 |
| `requirements.txt` / `pyproject.toml` | Python | poetry, pip, uv 등 |
| `go.mod` | Go | |
| `Gemfile` | Ruby | Rails 여부는 `rails` gem 포함 확인 |
| `composer.json` | PHP | Laravel 여부 별도 확인 |
| `build.gradle` / `build.gradle.kts` | JVM (Android/Kotlin/Java) | |
| `Podfile` | iOS 네이티브 (Swift/Obj-C) | Flutter도 ios/Podfile 보유 — 우선순위 낮음 |
| `*.xcodeproj` / `*.xcworkspace` | iOS 네이티브 | |
| `.csproj` / `.sln` | .NET | |

## 멀티스택 모노레포 탐지

- 루트에 위 파일 여러 개가 있으면 모노레포로 판단
- 하위 디렉토리(예: `app/`, `server/`, `web/`)별로 다시 스캔
- 사용자에게 명시적으로 어느 스택의 가이드를 만들지 확인

## 외부 서비스 의존성 grep 패턴

코드 안의 SDK 사용 흔적을 찾아 활성 서비스 목록 도출:

| 서비스 | grep 패턴 |
|--------|----------|
| Firebase | `firebase_core`, `firebase_messaging`, `FirebaseApp.configure`, `import { initializeApp } from "firebase/app"` |
| GCP | `google-cloud-`, `from google.cloud`, `GOOGLE_APPLICATION_CREDENTIALS` |
| AWS | `boto3`, `aws-sdk`, `@aws-sdk/`, `import software.amazon.awssdk` |
| Stripe | `stripe.api_key`, `import Stripe from "stripe"`, `stripe.Client(` |
| Sentry | `Sentry.init`, `sentry-sdk`, `sentry_dsn` |
| OAuth | `oauth2`, `passport-`, `next-auth`, `Sign in with` |

## 인프라/환경 파일

- `.env*` — 환경변수에서 외부 서비스 키 흔적 (`FIREBASE_*`, `AWS_*`, `STRIPE_*`)
- `docker-compose*.yml`, `Dockerfile` — 컨테이너 의존성
- `terraform/*.tf` — IaC 리소스
- `k8s/*.yaml`, `helm/` — Kubernetes 매니페스트

## 탐지 결과 0건일 때

사용자에게 명시적 질문: "프로젝트 스택이 자동 감지되지 않습니다. 어떤 환경에서 진행하시나요? (Flutter / 네이티브 iOS / React Native / Node 백엔드 / 기타)"
