---
name: flutter-responsive
description: >
  화면에 반응형 레이아웃을 적용하거나 기존 화면을 반응형으로 전환한다.
  태블릿 대응, 2컬럼 레이아웃, 반응형 그리드, breakpoint 적용, 화면 크기별 UI 분기가 필요할 때 사용.
  '태블릿에서 2컬럼으로', '반응형으로 바꿔줘', '화면 크기별 레이아웃', 'responsive',
  'tablet layout', 'desktop layout', 'adaptive', 'breakpoint' 같은 요청 시 트리거.
  단순 패딩/간격 조정만 할 때는 사용하지 않는다.
argument-hint: "<대상 파일 또는 설명>"
user-invocable: true
---

## Gotchas

- breakpoint 값을 하드코딩하지 마라 — 프로젝트에 이미 정의된 breakpoint 상수가 있는지 먼저 확인
- LayoutBuilder 안에서 Provider를 watch하면 레이아웃 변경마다 불필요한 리빌드 발생 — Provider는 LayoutBuilder 밖에서 watch
- **Flutter Web WASM 빌드 시 반응형 폴백** — `flutter build web --wasm` 으로 빌드하면 WasmGC 미지원 브라우저(iOS WebKit 전면, Firefox/Safari 일부)에서 자동으로 JS 렌더러로 폴백한다. 반응형 breakpoint 테스트 시 WASM 과 JS 모드 양쪽에서 레이아웃이 동일한지 확인하라 — 렌더러 차이로 미세한 레이아웃 차이가 발생할 수 있다 (출처: <https://docs.flutter.dev/platform-integration/web/wasm>)
- **Web Stateful Hot Reload (Flutter 3.38+)** — Web 에서도 Stateful Hot Reload 가 기본 활성화됐다. 반응형 레이아웃 조정 시 브라우저 리사이즈 + hot reload 로 빠른 피드백 루프 가능. `web_dev_config.yaml` 로 CORS 프록시/로컬 SSL 설정도 가능 (출처: <https://blog.flutter.dev/whats-new-in-flutter-3-38-3f7b258f7228>)

반응형 레이아웃을 적용하거나 기존 화면을 반응형으로 전환한다.

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$FLUTTER`, `$DART`, `$PACKAGE`, `ARCH`, `HAS_DS` 등)를 사용한다.

### 반응형 유틸리티 감지

`pubspec.yaml` 및 `lib/` 디렉토리에서 반응형 관련 패키지/유틸리티를 탐지한다:

| 패키지/패턴 | 감지 키 | 설명 |
|------------|---------|------|
| `responsive_framework` | `HAS_RESPONSIVE_FW` | ResponsiveBreakpoints 위젯 제공 |
| `responsive_builder` | `HAS_RESPONSIVE_BUILDER` | ScreenTypeLayout 위젯 제공 |
| `lib/**/responsive/` 또는 `lib/**/breakpoint*` | `HAS_CUSTOM_RESPONSIVE` | 프로젝트 커스텀 breakpoint 상수 |

프로젝트에 커스텀 breakpoint 상수가 있으면 해당 값을 읽어 사용한다.

### 프로젝트 breakpoint 탐색

프로젝트에 커스텀 breakpoint가 있는지 확인한다:
1. `lib/` 내 `breakpoint`, `responsive`, `screen_size` 키워드 파일 검색
2. 일반적 위치: `lib/core/responsive/`, `lib/core/constants/`, `lib/utils/responsive/`
3. 파일 내 `static const` 또는 `static final` double 값으로 정의된 breakpoint 상수 확인

발견되면 해당 상수를 사용한다. 발견되지 않으면 아래 기본값을 사용한다.

### Spacing 시스템 감지

`HAS_DS = true`이면 디자인 시스템의 spacing 토큰을 읽어 breakpoint별 spacing에 적용한다.
없으면 기본 spacing 가이드를 사용한다.

## Input

`$ARGUMENTS`: 대상 파일 경로 또는 자연어 설명
- `lib/features/workout/presentation/workout_screen.dart`
- `홈 화면을 태블릿에서 2컬럼으로`

## Steps

### 1. 반응형 유틸리티 읽기

프로젝트에 반응형 유틸리티가 있으면 해당 파일을 읽는다:
- 커스텀 breakpoint 상수 파일
- ResponsiveLayout / ScreenTypeLayout 위젯

없으면 기본 breakpoint를 사용한다.

### 2. Breakpoint 기준

프로젝트에 커스텀 breakpoint가 없으면 아래 기본값을 사용한다:

| Breakpoint | Width | 페이지 패딩 | 카드 간격 | 카드 내부 패딩 |
|-----------|-------|-----------|---------|-------------|
| Mobile | < 600 | 16 | 16 | 16 |
| Tablet | 600~1024 | 24 | 20 | 24 |
| Desktop | > 1024 | 32 | 24 | 32 |

`HAS_DS = true`이면 디자인 시스템 spacing 토큰으로 위 값을 대체한다.

### 3. 대상 파일의 위젯 구조 분석

대상 파일을 읽고 현재 레이아웃 구조를 파악한다.

### 4. 반응형 적응 계획 수립

#### 일반 패턴

| 패턴 | Mobile | Tablet | Desktop |
|------|--------|--------|---------|
| 리스트 → 그리드 | 1열 | 2열 | 3열 |
| 스택 → 나란히 | 세로 배치 | 가로 배치 | 가로 배치 |
| 단일 → 마스터-디테일 | 페이지 전환 | split view | split view |
| 패딩/간격 | 기본 | 확대 | 확대 |

#### LayoutBuilder vs MediaQuery 선택

| 상황 | 권장 | 이유 |
|------|------|------|
| 위젯이 부모 공간에 따라 변해야 함 | `LayoutBuilder` | 부모의 실제 가용 공간 기준 |
| 전체 화면 크기에 따라 변해야 함 | `MediaQuery.sizeOf(context)` | 화면 전체 기준 |
| 위젯이 네비게이션/사이드바 안에 있음 | `LayoutBuilder` | 사이드바 축소 시 자동 대응 |

### 5. 구현

프로젝트의 반응형 유틸리티에 따라 구현한다:

#### 프로젝트 유틸리티가 있을 때

프로젝트의 `ResponsiveLayout`, `ScreenTypeLayout`, 또는 커스텀 breakpoint 위젯을 사용한다.

#### 유틸리티가 없을 때 (기본 LayoutBuilder 패턴)

```dart
LayoutBuilder(
  builder: (context, constraints) {
    if (constraints.maxWidth >= 1024) {
      return _buildDesktop(context);
    } else if (constraints.maxWidth >= 600) {
      return _buildTablet(context);
    }
    return _buildMobile(context);
  },
)
```

그리드 열 수 계산:

```dart
int crossAxisCount(double width) {
  if (width >= 1024) return 3;
  if (width >= 600) return 2;
  return 1;
}
```

### 6. Before/After 제시

변경 계획을 before/after 형태로 사용자에게 제시한다.

## Rules

- **MUST** 프로젝트의 breakpoint 상수가 있으면 사용한다 (하드코딩 금지) -- 하드코딩된 매직넘버는 breakpoint 기준 변경 시 모든 파일을 수동으로 수정해야 한다
- **MUST** mobile-first 접근을 따른다 (기본 레이아웃 = 모바일) -- 대부분의 사용자가 모바일이므로 모바일을 기본으로 하고 큰 화면에서 확장하는 것이 자연스럽다
- **MUST** 작은 화면에서 overflow가 발생하지 않는지 확인한다 -- 반응형 적용 시 큰 화면만 확인하고 작은 화면을 놓치면 기존 모바일 UX가 깨진다
- **MUST** breakpoint별 spacing은 디자인 시스템 토큰이 있으면 사용한다 -- 일관된 시각적 리듬이 깨지면 전문성 없는 UI로 보인다
- **MUST** 로컬 반응형에는 `MediaQuery`보다 `LayoutBuilder`를 우선 사용한다 -- `LayoutBuilder`는 부모 위젯의 실제 가용 공간을 기준으로 하므로, 전체 화면 크기가 아닌 해당 위젯의 공간에 맞게 반응한다
- **MUST** 600px 미만에서는 단일 컬럼을 유지한다 -- 좁은 화면에서 다중 컬럼을 강제하면 콘텐츠가 읽기 어려울 정도로 좁아진다
- **MUST** `$FLUTTER` / `$DART` 변수를 사용한다. 하드코딩된 명령 prefix 금지
