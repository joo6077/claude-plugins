---
name: flutter-audit
description: >
  코드 품질 감사. quick 모드(단일 에이전트, 빠른 로컬 검토)와 deep 모드(최대 4에이전트 병렬 감사)를 지원한다.
  "리뷰해줘", "감사 돌려줘", "코드 검토", "품질 검사", "커밋 전에 확인",
  "PR 올리기 전에 검토", "코드 체크", "아키텍처 확인",
  "code review", "quality check", "audit", "lint check" 같은 요청 시 사용한다.
  변경 파일 수에 따라 자동으로 모드를 선택하지만 명시적으로 지정할 수도 있다.
  단순 탐색, 코드 읽기, 질문 응답만 할 때는 사용하지 않는다.
argument-hint: "[quick|deep] [path]"
user-invocable: true
---

## Gotchas

- quick 모드와 deep 모드의 차이: quick은 단일 에이전트 로컬 검토, deep은 최대 4에이전트 병렬 감사 — 변경 파일 5개 이하면 quick, 초과면 deep이 기본
- Provider watch 대신 select 사용 여부를 체크한다 — 성능 이슈의 주요 원인
- 커스텀 위젯에 const 생성자가 빠져 있으면 리빌드 최적화가 안 된다 — audit에서 지적 대상
- Flutter 3.41에서 테스트 매처 `containsSemantics`가 `isSemantics`로 변경됨 — 테스트 코드에 deprecated 매처가 남아 있으면 지적 대상. `matchesSemantics`(exact)와 구분 필요

Flutter 프로젝트의 코드 품질 감사. 프로젝트 환경을 자동 감지하여 적합한 규칙으로 검사한다.

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$FLUTTER`, `$DART`, `$PACKAGE`, `ARCH`, `HAS_DS`, `HAS_RIVERPOD`, `HAS_GO_ROUTER` 등)를 사용한다.

감지 결과에 따라 아래 체크리스트 항목의 활성화/비활성화를 결정한다:

| 감지 키 | 영향받는 검사 |
|---------|-------------|
| `ARCH = clean` | Architecture 전체 (레이어 분리, 의존 방향) |
| `ARCH = feature_first` / `flat` | Architecture를 구조에 맞게 적응 |
| `HAS_RIVERPOD` | State Management (codegen, mounted, Result) |
| `HAS_DS` | Design System (토큰, 컴포넌트 규칙) |
| i18n 라이브러리 감지 | i18n Audit (하드코딩 문자열, 키 동기화) |

## Input

`$ARGUMENTS` 파싱:

- `quick [path]` -- quick 모드 강제
- `deep [path]` -- deep 모드 강제
- `[path]` 또는 (인자 없음) -- auto 모드: 변경 파일 수로 자동 선택

## Auto 모드

인자에 `quick` / `deep` 키워드가 없으면 변경 파일 수를 기준으로 모드를 결정한다.

```bash
git diff --name-only HEAD
git diff --name-only --cached
```

- **5개 이하** -> quick 모드로 즉시 실행
- **6개 이상** -> 사용자에게 deep 모드 실행 여부를 확인한 뒤 실행

이렇게 나누는 이유: 소수 파일 변경은 빠른 체크리스트가 비용/시간 면에서 효율적이고, 대규모 변경은 관점을 분리한 병렬 감사로 빠짐없이 잡아야 하기 때문이다.

---

## Quick 모드

단일 에이전트, 비용 낮음, 지연 짧음. 변경된 파일(또는 지정된 경로)을 아래 체크리스트로 직접 검사한다.

### Architecture (ARCH에 따라 적응)

#### ARCH = clean

Clean Architecture 레이어 분리와 의존 방향을 지키지 않으면 도메인 로직이 인프라에 오염된다.

- [ ] 파일이 올바른 레이어에 위치 (data / domain / presentation)
- [ ] domain 레이어가 data / presentation을 import하지 않음
- [ ] data 레이어가 presentation을 import하지 않음
- [ ] Repository impl: 예외 -> Result/Either 변환 (raw exception 전파 금지)
- [ ] UseCase: 단일 책임, 단일 public 메서드

#### ARCH = feature_first

- [ ] feature 간 직접 import 최소화 (shared를 통해 공유)
- [ ] 각 feature 내부 구조가 일관적

#### ARCH = flat

- [ ] 관심사 분리가 최소한으로 유지되는지 (UI/로직 혼재 금지)

### Import Rules

잘못된 import 경로와 순서는 분석 도구 오류와 빌드 취약성을 유발한다.

- [ ] `lib/` 내 상대경로 import 금지 (`package:$PACKAGE/...` 전용) -- 프로젝트의 import 컨벤션이 상대경로면 이 규칙 스킵
- [ ] 순서: `dart:` -> `package:` (그룹 사이 빈 줄, 각 그룹 내 알파벳순)

### State Management (HAS_RIVERPOD일 때)

Riverpod codegen을 우회하거나 mounted 체크를 빠뜨리면 런타임 상태 오류가 발생한다.

- [ ] Provider: `@riverpod` / `@Riverpod(keepAlive: true)` codegen 사용 (프로젝트가 codegen 방식이면)
- [ ] keepAlive provider는 keepAlive provider만 참조
- [ ] async 작업 후 상태 변경 전 `ref.mounted` 확인
- [ ] 프로젝트에 Result 타입이 있으면 `Result.when(success:, failure:)` 분기 사용

### State Management (HAS_BLOC일 때)

- [ ] Bloc/Cubit이 단일 책임 원칙 준수
- [ ] State 클래스가 immutable (Equatable / Freezed 사용)

### State Management (기타)

- [ ] 상태와 UI의 분리가 유지되는지

### Error Handling

타입 없는 catch와 예외 미변환은 에러 추적을 불가능하게 만든다.

- [ ] bare `catch (e)` 금지 -- 타입 명시 우선
- [ ] 경계 계층(Repository/DataSource)에서 예외 -> Failure/Error 타입 변환
- [ ] catch 블록에서 에러를 조용히 무시하지 않음

### Naming

일관된 네이밍 규칙은 레이어와 역할을 파일 이름만으로 파악 가능하게 한다.

- [ ] 프로젝트의 네이밍 규칙 준수 (Screen/Page/View/Widget 또는 프로젝트 컨벤션)
- [ ] `_widget` 접미사 사용 금지
- [ ] 폴더 네이밍이 프로젝트 컨벤션과 일치

### Design System (HAS_DS = true일 때만)

디자인 시스템 토큰과 컴포넌트 규칙을 사용해야 테마 전환과 일관성이 보장된다.

- [ ] 색상: semantic token 패턴 사용 (하드코딩 Color 금지)
- [ ] 간격: spacing 토큰 사용 (반복 하드코딩 금지)
- [ ] 모서리: radius 토큰 사용 (반복 하드코딩 금지)
- [ ] 아이콘: 프로젝트 아이콘 패키지 사용 (다른 패키지 혼용 금지)
- [ ] 인터랙션: 프로젝트의 탭 피드백 위젯(Pressable 등) 사용, GestureDetector/InkWell 직접 사용 금지
- [ ] 애니메이션: 프로젝트에 애니메이션 상수(Duration/Curve 토큰)가 있으면 사용 (하드코딩 금지)
- [ ] opacity: `.withValues(alpha:)` 사용 (`.withOpacity()` deprecated)
- [ ] 서피스/데코레이션: 프로젝트에 서피스 토큰이 있으면 사용 (gradient/border 하드코딩 금지)
- [ ] disabled 상태: Pressable 자동 처리 확인 (별도 비활성 로직 중복 금지)
- [ ] variant 패턴: 프로젝트의 variant 패턴(enum+named constructor+switch expression) 준수

### Widget Rules

Flutter 위젯 모범 사례를 지키지 않으면 오버플로, 인터랙션 불일치가 발생한다.

- [ ] nullable 슬롯: `if (x != null) ...[x!, SizedBox()]` 패턴
- [ ] overflow 가능 레이아웃: 스크롤 컨테이너 사용
- [ ] const constructor 가능한 위젯에 const 사용
- [ ] 불필요한 StatefulWidget 사용 금지

### Reusability

재사용 가능한 위젯이 feature에 갇혀 있으면 코드 중복이 누적된다.

- [ ] private 위젯 중 feature 특화 로직 없이 범용 UI 패턴인 것이 shared로 추출되지 않음
- [ ] build 메서드가 50줄 이상이면서 논리적으로 분리 가능한 서브트리가 인라인
- [ ] 다른 feature에 구조적으로 유사한 위젯이 이미 존재하는데 중복 구현

---

## Deep 모드

최대 4개 전문 에이전트를 병렬로 실행한다 (haiku 모델로 실행, Widget Inspector만 sonnet). 인자가 없으면 변경된 파일 전체를 대상으로 하며, 경로가 지정되면 해당 경로만 감사한다.

인자 없을 때 파일 목록 수집:

```bash
git diff --name-only HEAD
git diff --name-only --cached
```

presentation 파일만 필터링하여 Design Review / i18n 에이전트에 전달한다.

Agent 도구를 사용하여 아래 에이전트를 **동시에** 실행한다 (조건부 에이전트 제외 시 최소 2개).

### Agent 1: Guard (아키텍처 감사)

아키텍처/임포트/네이밍/상태/에러 규칙은 서로 연관되므로 한 에이전트가 통합 검사한다.

```text
대상 파일의 규칙 준수 여부를 검사한다:

- Architecture: ARCH={감지된 아키텍처}에 맞는 레이어 분리 및 의존 방향
- Import 규칙: package:$PACKAGE/... only (프로젝트 컨벤션에 따라), dart: -> package: 순서
- State 관리: {감지된 상태관리} 패턴 준수
- 에러 처리: 타입 명시 catch, 경계 레이어 예외 변환
- 네이밍: 프로젝트 컨벤션 준수

대상 파일: [파일 목록]

각 위반 사항마다 파일:라인, 규칙, 심각도(error/warning), 수정 제안을 출력한다.
```

### Agent 2: Design Review (디자인 시스템 감사) -- HAS_DS = true일 때만

디자인 토큰과 컴포넌트 규칙은 시각적 일관성과 테마 안정성을 보장한다.

```text
대상 파일의 디자인 시스템 준수 여부를 검사한다:

- 색상: semantic token 사용 (하드코딩 Color 금지)
- 간격: spacing 토큰 사용 (반복 하드코딩 금지)
- 모서리: radius 토큰 사용 (반복 하드코딩 금지)
- 아이콘: 프로젝트 아이콘 패키지 사용
- 인터랙션: 프로젝트의 탭 피드백 패턴 준수

디자인 시스템 경로: {감지된 DS 경로}
대상 파일: [파일 목록]

각 위반 사항마다 파일:라인, 규칙, 심각도, 수정 제안을 출력한다.
```

`HAS_DS = false`이면 이 에이전트를 스킵하고 2개 에이전트만 실행한다.

### Agent 3: i18n Audit (국제화 감사) -- i18n 라이브러리 감지 시에만

하드코딩 문자열과 키 동기화 누락은 다국어 지원을 조용히 깨뜨린다.

```text
대상 파일의 국제화 규칙 준수 여부를 검사한다:

- 하드코딩된 사용자 표시 문자열 탐지 (Text('..'), hint, label 등)
- i18n 파일 간 키 동기화 누락
- 미사용 i18n 키 탐지
- 올바른 접근 패턴 ({감지된 i18n 라이브러리}의 패턴)

대상 파일: [파일 목록]
i18n 파일: {감지된 i18n 파일 경로들}

각 위반 사항마다 파일:라인, 규칙, 심각도, 수정 제안을 출력한다.
```

i18n 라이브러리가 감지되지 않으면 이 에이전트를 스킵한다.

### Agent 4: Widget Inspector (재사용성 감사) -- 항상 실행

재사용 가능한 위젯 패턴을 감지하여 추출 후보를 리포팅한다.

```text
대상 파일에서 재사용 가능한 위젯 패턴을 감지한다:

- 구조적 중복: 비슷한 위젯 트리가 2곳 이상 반복
- 비대한 build: build 메서드 50줄 이상, 분리 가능한 서브트리
- 범용 private 위젯: feature 특화 로직 없는 _WidgetName이 shared로 추출 가능
- 패턴 반복: 같은 위젯 트리 구조가 다른 이름으로 반복

대상 파일: [파일 목록]
프로젝트 shared 위젯 경로: {감지된 shared 경로}

각 추출 후보마다 파일:라인, 감지 기준, 추출 제안(위젯 이름 + 배치 경로)을 출력한다.
```

---

## Report Format

모드에 관계없이 아래 형식으로 결과를 보고한다. 이슈가 없는 항목은 "Clean" 표시.

```text
-- Audit Report ([quick|deep]) ---------------------

Architecture
  errors: N | warnings: N
  [주요 이슈 목록]

State Management
  errors: N | warnings: N
  [주요 이슈 목록]

Error Handling
  errors: N | warnings: N
  [주요 이슈 목록]

Design System                    <-- HAS_DS = true일 때만
  errors: N | warnings: N
  [주요 이슈 목록]

i18n                             <-- i18n 감지 시에만 (deep 모드)
  errors: N | warnings: N
  [주요 이슈 목록]

Reusability
  candidates: N
  [추출 후보 목록]

----------------------------------------------------
Total: N errors, N warnings
```

감사 결과만 보고한다. 코드를 직접 수정하지 않는다.

## Rules

- **MUST** 프로젝트 감지 결과에 따라 체크리스트를 적응시킨다 -- 모든 프로젝트에 Clean Architecture, Riverpod, 디자인 시스템이 있는 것은 아니다
- **MUST** `HAS_DS = false`이면 Design System 검사를 완전히 스킵한다 -- 디자인 시스템이 없는 프로젝트에 토큰 규칙을 강제하면 의미 없는 위반이 보고된다
- **MUST** i18n 라이브러리가 없으면 i18n Audit를 스킵한다 -- 다국어 미지원 프로젝트에 하드코딩 문자열 경고는 노이즈다
- **MUST** 감사 결과만 보고하고 코드를 직접 수정하지 않는다 -- 감사와 수정을 분리해야 사용자가 변경 사항을 통제할 수 있다
- **MUST** `$PACKAGE` 변수를 import 규칙에 사용한다 -- 패키지명을 하드코딩하면 다른 프로젝트에서 오탐이 발생한다
- **MUST** 위반 보고 시 파일:라인, 규칙, 심각도, 수정 제안을 모두 포함한다 -- 위치 없는 위반 보고는 수정 작업을 지연시킨다
