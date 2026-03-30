# Flutter 공식 AI Rules 요약

> 출처: [flutter/flutter/docs/rules/rules.md](https://raw.githubusercontent.com/flutter/flutter/refs/heads/main/docs/rules/rules.md)
> 최종 확인: 2026-03-30

Flutter 공식 AI rules는 LLM이 Flutter 코드를 생성할 때 따라야 할 패턴을 정의한다.
flutter-toolkit 스킬은 이 규칙과 정합성을 유지해야 한다.

## 위젯 패턴

- **Composition Over Inheritance** — 복잡한 위젯은 상속이 아닌 합성으로 구성
- **Private Widget Class** — 헬퍼 메서드(`_buildHeader()`)가 아닌 private Widget 클래스로 추출
- **Const Constructor** — 가능한 모든 곳에 `const` 사용하여 리빌드 최소화
- **Build 분리** — 큰 `build()` 메서드는 작은 private 위젯으로 분해

## State Management (서드파티 패키지 없을 때)

공식 우선순위:
1. `ValueNotifier` + `ValueListenableBuilder` — 단일 값
2. `Stream` + `StreamBuilder` — 비동기 이벤트 시퀀스
3. `Future` + `FutureBuilder` — 일회성 비동기
4. `ChangeNotifier` + `ListenableBuilder` — 복합/다중 위젯 상태
5. MVVM 패턴 — 복잡한 앱

> 프로젝트에 Riverpod/Bloc이 있으면 해당 패키지 패턴을 따른다.

## 아키텍처

- **레이어 분리:** Presentation → Domain → Data → Core
- **대규모 프로젝트:** Feature-first 구조 (feature 내 presentation/domain/data)
- **MVVM:** View ↔ ViewModel (1:1) ↔ Repository ↔ Service

## Do's

- `go_router` 네비게이션 (딥링크, 웹 지원)
- SOLID 원칙
- `dart:developer.log` 사용 (`print()` 금지)
- `compute()` 사용 (비용 큰 연산은 Isolate)
- 모든 public API에 `///` 문서화
- `dart_format`, `dart_fix` 도구 활용
- 다양한 화면 크기 테스트

## Don'ts

- `print()` 사용 금지 → `dart:developer.log`
- `build()` 내 네트워크 호출 금지
- 같은 Row/Column에 `Flexible` + `Expanded` 혼용 금지
- `!` 연산자 남용 금지 (non-null 보장된 경우만)
- 깊은 위젯 트리 중첩 금지 → 합성으로 분해

## 코드 생성

- JSON 직렬화: `json_serializable` + `json_annotation`
- `fieldRename: FieldRename.snake` 사용
- `build_runner`: `dart run build_runner build --delete-conflicting-outputs`

## 테스팅

- Arrange-Act-Assert 구조
- Mock보다 Fake/Stub 선호
- Unit → Widget → Integration 순서
- 높은 테스트 커버리지 목표

## 라인 길이

- 최대 80자
