---
title: 테마
version: 0.1.0
last_updated: 2026-04-05
---

# 테마

Material 3 ThemeData, ColorScheme.fromSeed, 라이트/다크 전환, ThemeExtension, 타이포 스케일을 다룬다.

## 원칙

1. **Flutter 3.16+는 Material 3이 기본이며, ThemeData의 중심은 colorScheme + textTheme이다.** 개별 컴포넌트 색상을 덮어쓰지 말고 ColorScheme role을 정의하라.
   - 출처: https://docs.flutter.dev/release/breaking-changes/material-3-default
2. **새 앱의 출발점은 `ColorScheme.fromSeed(seedColor: ...)`다.** 단일 seed에서 M3 토널 팔레트가 자동 생성되어 라이트/다크 일관성이 보장된다.
   - 출처: https://docs.flutter.dev/release/breaking-changes/material-3-migration
3. **라이트/다크는 `MaterialApp.theme` + `darkTheme` + `themeMode` 3종 조합으로 관리한다.** themeMode.system이 기본, 사용자 설정은 상태 관리 계층에서 주입한다.
   - 출처: https://api.flutter.dev/flutter/material/MaterialApp/theme.html
4. **커스텀 토큰은 `ThemeExtension<T>`로 정의하고 copyWith/lerp를 반드시 구현한다.** lerp가 있어야 theme 전환 애니메이션과 A/B 테마 보간이 부드럽게 동작한다.
   - 출처: https://api.flutter.dev/flutter/material/ThemeExtension-class.html
5. **M2의 accent 패턴을 버리고 M3 ColorScheme role 기반으로 마이그레이션한다.** primary/secondary/tertiary + container/onContainer 구조로 표현하라.
   - 출처: https://docs.flutter.dev/release/breaking-changes/theme-data-accent-properties

## 수치·경계값

- `useMaterial3`는 Flutter 3.16+에서 기본 true. 명시적으로 false로 내리지 마라.
- ColorScheme에 M3 기반의 새 surface/container role들이 추가되었다 (surface, surfaceContainer, surfaceContainerHighest 등).
- 일부 레거시 role(background, onBackground, surfaceVariant)은 deprecated — 마이그레이션 대상이다.

## 안티패턴

- 위젯마다 색/폰트를 하드코딩 — 테마 전환 시 일괄 변경 불가.
- light/dark 팔레트를 별도 상수 파일에 복붙해 유지 — 한쪽만 업데이트되는 drift가 발생한다.
- 커스텀 토큰을 static class로만 관리 — BuildContext와 무관해져 theme 스왑이 불가능.
- `accentColor` 시대의 패턴을 그대로 유지 — M3 컴포넌트에서 무시되거나 잘못 매핑된다.

## 실전 패턴

### ThemeExtension 정의

```dart
@immutable
class BrandTokens extends ThemeExtension<BrandTokens> {
  final Color cardGradientStart;
  final Color cardGradientEnd;
  final double cardElevation;

  const BrandTokens({required this.cardGradientStart, required this.cardGradientEnd, required this.cardElevation});

  @override
  BrandTokens copyWith({Color? cardGradientStart, Color? cardGradientEnd, double? cardElevation}) =>
      BrandTokens(
        cardGradientStart: cardGradientStart ?? this.cardGradientStart,
        cardGradientEnd: cardGradientEnd ?? this.cardGradientEnd,
        cardElevation: cardElevation ?? this.cardElevation,
      );

  @override
  BrandTokens lerp(BrandTokens? other, double t) {
    if (other is! BrandTokens) return this;
    return BrandTokens(
      cardGradientStart: Color.lerp(cardGradientStart, other.cardGradientStart, t)!,
      cardGradientEnd: Color.lerp(cardGradientEnd, other.cardGradientEnd, t)!,
      cardElevation: lerpDouble(cardElevation, other.cardElevation, t)!,
    );
  }
}
```

- 출처: https://api.flutter.dev/flutter/material/ThemeExtension-class.html

### Dynamic Color (Android 12+)

`dynamic_color` 패키지로 사용자 벽지 기반 시스템 팔레트를 가져올 수 있다. fallback으로 `ColorScheme.fromSeed`를 제공하면 비지원 기기에서도 일관된 경험을 보장한다.

- 출처: https://pub.dev/packages/dynamic_color

### 테마 전환 애니메이션

`AnimatedTheme`은 `ThemeData` 전체를 보간한다. 단, `ThemeExtension`의 `lerp`가 올바르게 구현되지 않으면 커스텀 토큰은 즉시 전환(jump)된다.

- 출처: https://api.flutter.dev/flutter/material/AnimatedTheme-class.html

## 테스트 전략

- `MaterialApp(theme: testTheme)`로 widget test에서 특정 테마 조건을 재현
- Golden test에서 light + dark 두 variant를 캡처하면 컬러 regression 방지
- ThemeExtension의 lerp 함수는 unit test로 t=0, t=0.5, t=1 경계값 검증

## Gotchas

- `ColorScheme.fromSeed`의 생성 결과는 underlying `material-color-utilities` 패키지 업데이트에 따라 미세하게 달라질 수 있다. 디자인 토큰을 픽셀 단위로 고정해야 하면 결과값을 캡처해 상수화하라.
- 타이포를 토큰화하지 않으면 feature별로 임의 fontSize가 폭발한다 — 처음부터 textTheme의 displayLarge~labelSmall 스케일을 고정하고 위젯에서는 `Theme.of(context).textTheme.xxx`만 사용하도록 강제하라.
- `Theme.of(context).extension<T>()`가 null을 반환할 수 있다 — ThemeExtension을 등록하지 않은 테스트 환경에서 NPE가 터진다. 반드시 null check 또는 테스트용 테마에 extension을 포함시켜라.
- `TextTheme` 인스턴스를 `.copyWith()`로 font family만 바꿀 때, `apply(fontFamily: ...)`가 더 간결하다. copyWith는 14개 text style 각각에 적용해야 한다.
