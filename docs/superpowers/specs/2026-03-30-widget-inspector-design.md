# Widget Inspector 에이전트 + Flutter Extract 스킬 설계

> flutter-toolkit에 재사용 가능한 위젯 패턴 감지(에이전트) + 추출(스킬)을 추가한다.

## 배경

Flutter 프로젝트에서 흔한 문제:
- `_WidgetName`으로 분리했지만 여러 파일에서 중복
- build 메서드 안에 분리 가능한 덩어리가 인라인으로 박혀 있음
- private 위젯이 feature에 갇혀 있지만 실제로는 범용적
- 같은 구조(Card + 아이콘 + 텍스트 등)가 다른 이름으로 반복

이를 자동으로 감지하고 추출하는 에이전트/스킬 조합이 필요하다.

## 구성

| 구성 | 역할 | 타입 |
|------|------|------|
| `widget-inspector` | 읽기 전용 스캔 + 리포팅 | 에이전트 |
| `flutter-extract` | 사용자 승인 후 추출 수행 | 스킬 |

## 에이전트: widget-inspector

### 메타데이터

```yaml
name: widget-inspector
description: >
  프로젝트 코드에서 재사용 가능한 위젯 패턴을 감지하고 리포팅한다.
  구현 스킬(flutter-screen, flutter-feature, flutter-widget) 실행 후 자동으로 사용.
  flutter-audit 실행 시 딥 스캔 축으로 포함.
  프로젝트 코드를 수정할 때 프로액티브하게 사용.
  use proactively.
tools: Read, Grep, Glob
model: sonnet
```

### 두 가지 모드

| 모드 | 트리거 | 범위 |
|------|--------|------|
| `quick` | 구현 후 / 프로액티브 / 코드 수정 시 | 변경 파일의 feature 디렉토리 + 관련 shared 디렉토리 |
| `deep` | audit 연동 / 명시 요청 | `lib/` 내 전체 presentation 레이어 |

### 감지 기준

1. **구조적 중복** — 비슷한 위젯 트리가 2곳 이상 반복
2. **비대한 build 메서드** — build 내부에 논리적으로 분리 가능한 큰 덩어리가 인라인
3. **범용성 높은 private 위젯** — `_SomethingCard` 등이 특정 feature에 갇혀 있지만 범용적
4. **패턴 반복** — 같은 구조(Card + 아이콘 + 텍스트 + 액션 등)가 다른 이름으로 반복

### 리포트 포맷

```
-- Widget Inspector Report ([quick|deep]) --

Duplicates (구조적 중복)
  [파일A:라인 ↔ 파일B:라인 — 유사도/설명]

Inline Extraction (비대 build)
  [파일:라인 — 추출 가능 위젯 트리 설명]

Private → Shared (범용 private 위젯)
  [파일:_WidgetName — 사용 가능 범위 설명]

Pattern Repetition (패턴 반복)
  [패턴 설명 — 발견 위치 목록]

Total: N extraction candidates
```

### 행동 원칙

- 리포팅만 수행, 코드 수정 불가 (도구: Read, Grep, Glob만)
- quick 모드는 빠르게, deep 모드는 철저하게
- 발견된 후보마다 파일:라인 근거 필수
- 추출 시 예상되는 공용 위젯 이름과 배치 경로도 제안

## 스킬: flutter-extract

### 메타데이터

```yaml
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
```

### 프로세스

1. **프로젝트 감지** — `references/project-detection.md` 실행
2. **추출 대상 확인** — widget-inspector 리포트 참조 또는 사용자 지정 파일/위젯 분석
3. **추출 계획 제시** — 어떤 위젯을 어디로 빼는지 사용자에게 보여주고 확인
4. **공용 위젯 생성** — private → public 전환, 필요시 파라미터화
5. **사용처 교체** — 기존 코드에서 추출한 위젯으로 교체 + import 추가
6. **import 정리** — 불필요해진 import 제거, 순서 정리

### 배치 경로 결정

- 프로젝트 shared 위젯 디렉토리 감지 (기존 구조 우선)
- 카테고리 분류가 있으면 적절한 폴더에 배치
- 모호하면 사용자에게 확인
- 상황에 따라 유연하게 (flutter-widget의 shared 경로 로직 참고 가능)

### 추출 변환 규칙

- `_WidgetName` → `WidgetName` (private → public)
- 하드코딩된 값 → 생성자 파라미터로 추출
- feature 특화 로직 → 콜백/제네릭으로 일반화
- 기존 코드 패턴(base class, 디자인 토큰 등) 유지

## 기존 스킬 연동

### flutter-audit 연동

`flutter-audit`의 deep 모드에 widget-inspector를 4번째 에이전트로 추가:
- Agent 4: Widget Inspector (재사용성 감사)
- quick 모드에도 간단한 Reusability 체크리스트 항목 추가

### 구현 스킬 연동

`flutter-screen`, `flutter-feature`, `flutter-widget` 실행 후:
- widget-inspector를 quick 모드로 자동 실행
- 변경된 파일 주변만 스캔
- 후보가 있으면 리포팅, 없으면 조용히 넘어감

### 프로액티브 동작

description에 "use proactively" 포함:
- 프로젝트 코드를 수정할 때 Claude가 자동으로 widget-inspector를 실행할 수 있음
- quick 모드로 가볍게 스캔
