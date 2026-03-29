---
name: flutter-extract
description: >
  재사용 가능한 위젯을 공용 위젯으로 추출한다.
  private 위젯을 shared로 이동, 인라인 위젯 트리를 분리, 중복 위젯을 통합.
  "위젯 빼줘", "공통으로 추출", "shared로 이동", "extract widget",
  "중복 위젯 정리", "위젯 분리해줘" 같은 요청 시 트리거.
  widget-inspector 리포트 승인 후에도 트리거.
  단순 위젯 생성은 flutter-widget 사용.
argument-hint: "[파일경로|위젯이름]"
user-invocable: true
---

## Gotchas

- 추출할 때 기존 사용처의 import를 빠뜨리면 컴파일 에러 — 추출 후 반드시 모든 사용처에서 import 추가/변경 확인
- private → public 전환 시 하드코딩된 값을 그대로 두면 재사용 불가 — 반드시 파라미터화 검토
- feature 특화 타입(entity, state 등)을 파라미터로 받으면 shared 위젯이 아니다 — 콜백/제네릭으로 일반화하거나 추출 대상에서 제외
- 추출 후 원본 파일에 빈 줄/미사용 import가 남는다 — 정리까지 해야 완료

재사용 가능한 위젯을 감지하여 공용 위젯으로 추출한다.

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$FLUTTER`, `$DART`, `$PACKAGE`, `ARCH`, `HAS_DS`, `HAS_RIVERPOD`, `HAS_HOOKS` 등)를 사용한다.

## Input

`$ARGUMENTS`: 추출 대상 파일 경로 또는 위젯 이름 (optional)

- 파일 경로 지정 시: 해당 파일을 분석하여 추출 후보를 찾는다
- 위젯 이름 지정 시: 프로젝트에서 해당 위젯을 찾아 추출한다
- 인자 없음: widget-inspector 리포트가 있으면 참조, 없으면 사용자에게 대상 확인

## Steps

### 1. 추출 대상 확인

**widget-inspector 리포트가 있는 경우:**
- 리포트의 추출 후보 목록을 사용자에게 보여준다
- 사용자가 선택한 항목을 추출 대상으로 확정한다

**리포트가 없거나 직접 지정한 경우:**
- 지정된 파일/위젯을 Read로 읽는다
- 추출 가능한 부분을 분석한다:
  - private 위젯 클래스 → shared로 이동 후보
  - build 내 인라인 서브트리 → private 또는 shared 위젯으로 분리 후보
  - 다른 파일의 유사 위젯 → 통합 후보

### 2. 추출 계획 제시

사용자에게 추출 계획을 보여주고 확인받는다:

```
추출 계획:

1. _InfoCard (home_screen.dart:45)
   → InfoCard → lib/shared/presentation/widgets/cards/info_card.dart
   파라미터화: title(String), subtitle(String), icon(IconData), onTap(VoidCallback?)

2. build 내 헤더 섹션 (settings_screen.dart:23-45)
   → _SettingsHeader → 같은 파일 내 private 위젯으로 분리

진행할까요?
```

### 3. 배치 경로 결정

**shared 위젯으로 추출하는 경우:**
- 프로젝트의 shared 위젯 디렉토리를 감지한다
  - `lib/shared/presentation/widgets/` (clean architecture)
  - `lib/core/widgets/` (feature-first)
  - `lib/widgets/` (flat)
  - 기존 프로젝트 구조에서 감지된 경로 우선
- 카테고리 분류가 있으면 (`buttons/`, `cards/`, `inputs/` 등) 적절한 폴더에 배치
- 분류가 모호하면 사용자에게 확인

**같은 파일 내 분리인 경우:**
- 같은 파일 하단에 private 위젯으로 추출

### 4. 공용 위젯 생성

추출 대상별 변환 규칙:

**Private → Public 전환:**
- `_WidgetName` → `WidgetName`
- 하드코딩된 값을 생성자 파라미터로 추출
- `const` 생성자 사용 가능하면 적용

**파라미터화:**
- 텍스트, 아이콘, 색상 등 데이터 값 → required/optional 파라미터
- 콜백 (onTap, onChanged 등) → `VoidCallback?`, `ValueChanged<T>?` 파라미터
- feature 특화 타입 → 제네릭 또는 콜백으로 일반화
- 기본값이 자연스러운 파라미터는 optional + default value

**기존 패턴 유지:**
- Widget base class는 프로젝트 패턴을 따른다 (HookWidget, ConsumerWidget 등)
- 디자인 토큰 사용 방식 유지 (HAS_DS면 semantic token)
- import 패턴 유지 (`package:$PACKAGE/...`)

### 5. 사용처 교체

- 원본 파일에서 인라인 코드/private 위젯을 새 공용 위젯으로 교체
- 새 위젯의 import 추가
- 중복 위젯이 있던 다른 파일에서도 교체 + import 추가

### 6. Import 정리

- 불필요해진 import 제거 (추출로 인해 더 이상 참조하지 않는 패키지)
- import 순서 정리: `dart:` → `package:` (그룹 사이 빈 줄, 알파벳순)
- 원본 파일에서 빈 줄 정리

### 7. 검증

- `$FLUTTER analyze` 또는 `$DART analyze` 실행하여 에러 0개 확인
- 추출된 위젯이 올바르게 참조되는지 확인

## Code Rules

- **MUST** `package:$PACKAGE/...` import만 사용 (상대경로 금지)
- **MUST** import 순서: `dart:` → `package:` (그룹 사이 빈 줄, 알파벳순)
- **MUST** 추출 후 모든 사용처의 import를 업데이트한다
- **MUST** const constructor 가능한 위젯에 const 적용
- **MUST** 기존 코드에서 관찰된 패턴과 일관성 유지
- **MUST NOT** 프로젝트에 없는 패키지를 import하는 코드를 생성하지 않는다
- **MUST NOT** feature 특화 타입을 shared 위젯의 파라미터로 노출하지 않는다

## Rules

- **MUST** 추출 전 사용자에게 계획을 보여주고 확인받는다
- **MUST** 추출 후 analyze 실행하여 에러 없음을 확인한다
- **MUST** 원본 파일의 빈 줄/미사용 import를 정리한다
- **MUST** 하드코딩된 값은 파라미터화한다
- **MUST NOT** feature 특화 로직이 있는 위젯을 shared로 강제 추출하지 않는다 — 콜백/제네릭으로 일반화 가능한 경우에만

## Related Skills

- 새 위젯 생성 → `flutter-widget`
- 코드 품질 감사 → `flutter-audit`
- codegen 실행 → `flutter-run codegen`
