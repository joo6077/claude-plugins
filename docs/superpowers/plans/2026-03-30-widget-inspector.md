# Widget Inspector + Flutter Extract 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** flutter-toolkit에 재사용 가능 위젯 패턴 감지 에이전트(widget-inspector)와 추출 스킬(flutter-extract)을 추가한다.

**Architecture:** widget-inspector 에이전트는 읽기 전용으로 프로젝트를 스캔하여 추출 후보를 리포팅한다. flutter-extract 스킬은 사용자 승인 후 실제 추출을 수행한다. flutter-audit deep 모드에 4번째 에이전트로 통합되며, 구현 스킬들의 후속 단계로도 연동된다.

**Tech Stack:** Claude Code agents, SKILL.md, markdown

---

## 파일 구조

| 액션 | 파일 | 역할 |
|------|------|------|
| Create | `flutter-toolkit/agents/widget-inspector.md` | 에이전트 정의 |
| Create | `flutter-toolkit/skills/flutter-extract/SKILL.md` | 추출 스킬 정의 |
| Modify | `flutter-toolkit/skills/flutter-audit/SKILL.md` | deep 모드에 Agent 4 추가, quick 모드에 Reusability 체크리스트 추가 |
| Modify | `flutter-toolkit/README.md` | 에이전트 + 신규 스킬 문서화 |

---

### Task 1: widget-inspector 에이전트 생성

**Files:**
- Create: `flutter-toolkit/agents/widget-inspector.md`

- [ ] **Step 1: agents 디렉토리 생성 확인**

```bash
ls flutter-toolkit/agents/ 2>/dev/null || mkdir -p flutter-toolkit/agents
```

- [ ] **Step 2: widget-inspector.md 작성**

```markdown
---
name: widget-inspector
description: >
  프로젝트 코드에서 재사용 가능한 위젯 패턴을 감지하고 리포팅한다.
  구현 스킬(flutter-screen, flutter-feature, flutter-widget) 실행 후 자동으로 사용.
  flutter-audit 실행 시 딥 스캔 축으로 포함.
  프로젝트 코드를 수정할 때 프로액티브하게 사용.
  use proactively.
tools: Read, Grep, Glob
model: sonnet
---

# Widget Inspector

프로젝트 코드에서 재사용 가능한 위젯 패턴을 감지하고 리포팅하는 읽기 전용 에이전트.
코드를 수정하지 않는다. 감지 결과만 보고한다.

## 모드

호출 시 프롬프트에서 모드를 지정받는다:

| 모드 | 범위 | 설명 |
|------|------|------|
| `quick` | 변경 파일의 feature 디렉토리 + 관련 shared 디렉토리 | 구현 후/프로액티브 스캔. 빠르게 |
| `deep` | `lib/` 내 전체 presentation 레이어 | audit 연동/명시 요청. 철저하게 |

모드가 지정되지 않으면 `quick`으로 동작한다.

## 감지 기준

### 1. 구조적 중복 (Duplicates)

비슷한 위젯 트리가 2곳 이상에서 반복되는 경우.

**탐지 방법:**
- Grep으로 프로젝트 내 위젯 클래스 정의를 수집한다 (`class .* extends .*Widget`, `class .* extends .*State`)
- 같은 구조의 build 메서드를 가진 위젯을 비교한다
- Container/Card/Row/Column + 동일한 자식 패턴이 반복되면 중복으로 판단한다

**판단 기준:**
- 위젯 트리의 depth 3 이상이 구조적으로 동일하면 중복
- 차이가 텍스트/아이콘/색상 등 데이터값만이면 파라미터화 가능한 중복

### 2. 비대한 build 메서드 (Inline Extraction)

build 메서드 안에 논리적으로 분리 가능한 큰 덩어리가 인라인으로 박혀 있는 경우.

**탐지 방법:**
- 위젯 파일의 build 메서드를 Read로 읽는다
- build 메서드의 줄 수를 측정한다
- 중첩 깊이(nesting depth)가 깊은 서브트리를 식별한다

**판단 기준:**
- build 메서드가 50줄 이상이면 분리 후보
- 논리적으로 독립된 서브트리(예: 헤더, 바디, 푸터)가 20줄 이상이면 추출 후보
- 같은 build 내에서 조건부로 다른 위젯 트리를 반환하는 경우 각각 분리 후보

### 3. 범용성 높은 private 위젯 (Private → Shared)

`_WidgetName`으로 정의된 private 위젯이 특정 feature에 갇혀 있지만 범용적으로 사용 가능한 경우.

**탐지 방법:**
- Grep으로 `class _` 패턴의 private 위젯을 수집한다
- 해당 위젯의 build 메서드를 읽어 feature 특화 로직이 있는지 확인한다
- feature 특화 로직 없이 범용 UI 패턴(카드, 리스트 아이템, 버튼 등)이면 추출 후보

**판단 기준:**
- feature 특화 import(`../domain/`, `../data/`)가 없으면 범용 가능성 높음
- 생성자 파라미터가 기본 타입(String, int, VoidCallback, Widget)이면 범용 가능성 높음
- 이름이 feature 이름을 포함하지 않으면 범용 가능성 높음 (예: `_InfoCard` vs `_WorkoutCard`)

### 4. 패턴 반복 (Pattern Repetition)

같은 구조(Card + 아이콘 + 텍스트 + 액션 등)가 다른 이름으로 여기저기 반복되는 경우.

**탐지 방법:**
- deep 모드에서 전체 presentation 파일을 스캔한다
- 위젯 트리의 구조 패턴을 추출한다 (예: `Card > Padding > Row > [Icon, Column > [Text, Text]]`)
- 동일 패턴이 다른 파일에서 다른 이름으로 나타나면 반복으로 판단

**판단 기준:**
- 구조 패턴이 3곳 이상에서 반복되면 강력한 추출 후보
- 2곳이면 약한 후보 (리포트에 포함하되 우선순위 낮게)

## Process

### Step 1: 스캔 범위 결정

**quick 모드:**
- 호출 시 전달받은 파일 목록 또는 경로를 사용한다
- 해당 파일이 속한 feature 디렉토리 전체를 범위로 잡는다
- 프로젝트의 shared 위젯 디렉토리도 범위에 포함한다

**deep 모드:**
- `lib/` 내 전체를 Glob으로 스캔한다
- presentation 레이어 파일을 우선 대상으로 한다
- 파일 수가 많으면 feature 단위로 순차 스캔한다

### Step 2: 감지 실행

감지 기준 4가지를 순서대로 적용한다:

1. private 위젯 수집 (`class _.*Widget`, `class _.*State`)
2. build 메서드 크기 측정
3. 구조적 중복 비교 (quick: feature 내부만, deep: 전체)
4. 패턴 반복 탐지 (deep 모드에서만 전체 비교)

### Step 3: 리포트 생성

```
-- Widget Inspector Report ([quick|deep]) --

Duplicates (구조적 중복)
  [파일A:라인 ↔ 파일B:라인 — 유사도/설명]
  → 추출 제안: WidgetName → shared/widgets/카테고리/

Inline Extraction (비대 build)
  [파일:라인 — 추출 가능 위젯 트리 설명]
  → 추출 제안: _WidgetName으로 분리

Private → Shared (범용 private 위젯)
  [파일:_WidgetName — 사용 가능 범위 설명]
  → 추출 제안: WidgetName → shared/widgets/카테고리/

Pattern Repetition (패턴 반복)
  [패턴 설명 — 발견 위치 목록]
  → 추출 제안: 공통 WidgetName으로 통합

Total: N extraction candidates
```

후보가 0건이면:
```
-- Widget Inspector Report ([quick|deep]) --
Clean — 추출 후보 없음
```

## Gotchas

- quick 모드에서 전체 프로젝트를 스캔하지 마라 — 변경 파일 주변만 봐야 빠르다
- 모든 private 위젯이 추출 대상은 아니다 — feature 특화 로직이 있으면 그대로 두는 게 맞다
- build 메서드 줄 수만으로 판단하지 마라 — switch expression이 길어도 논리적으로 하나면 분리 불필요
- 리포트에 파일:라인 근거 없이 "중복인 것 같다"는 금지 — 증거 없는 판단은 노이즈다

## Rules

- **MUST** 코드를 수정하지 않는다 — 리포팅만 수행
- **MUST** 모든 후보에 파일:라인 근거를 포함한다
- **MUST** 추출 시 예상 배치 경로를 제안한다
- **MUST** quick 모드는 전달받은 범위만 스캔한다
- **MUST NOT** feature 특화 로직이 있는 private 위젯을 추출 대상으로 잡지 않는다
```

- [ ] **Step 3: 커밋**

```bash
git add flutter-toolkit/agents/widget-inspector.md
git commit -m "feat: flutter-toolkit widget-inspector 에이전트 추가

재사용 가능한 위젯 패턴을 감지하고 리포팅하는 읽기 전용 에이전트.
quick/deep 두 가지 모드 지원."
```

---

### Task 2: flutter-extract 스킬 생성

**Files:**
- Create: `flutter-toolkit/skills/flutter-extract/SKILL.md`

- [ ] **Step 1: 디렉토리 생성 확인**

```bash
ls flutter-toolkit/skills/flutter-extract/ 2>/dev/null || mkdir -p flutter-toolkit/skills/flutter-extract
```

- [ ] **Step 2: SKILL.md 작성**

```markdown
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
- 인자 없음: widget-inspector 리포트(`.harness/widget-inspector-report.md`)가 있으면 참조, 없으면 사용자에게 대상 확인

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
```

- [ ] **Step 3: 커밋**

```bash
git add flutter-toolkit/skills/flutter-extract/SKILL.md
git commit -m "feat: flutter-extract 위젯 추출 스킬 추가

private→shared 이동, 인라인 위젯 분리, 중복 위젯 통합을 수행하는 스킬.
widget-inspector 에이전트 리포트와 연동."
```

---

### Task 3: flutter-audit에 widget-inspector 연동

**Files:**
- Modify: `flutter-toolkit/skills/flutter-audit/SKILL.md`

- [ ] **Step 1: quick 모드에 Reusability 체크리스트 추가**

`flutter-audit/SKILL.md`의 quick 모드 섹션, `### Widget Rules` 뒤에 추가:

```markdown
### Reusability

재사용 가능한 위젯이 feature에 갇혀 있으면 코드 중복이 누적된다.

- [ ] private 위젯 중 feature 특화 로직 없이 범용 UI 패턴인 것이 shared로 추출되지 않음
- [ ] build 메서드가 50줄 이상이면서 논리적으로 분리 가능한 서브트리가 인라인
- [ ] 다른 feature에 구조적으로 유사한 위젯이 이미 존재하는데 중복 구현
```

- [ ] **Step 2: deep 모드에 Agent 4 추가**

`flutter-audit/SKILL.md`의 deep 모드 섹션, Agent 3 뒤에 추가:

```markdown
### Agent 4: Widget Inspector (재사용성 감사) -- 항상 실행

재사용 가능한 위젯 패턴을 감지하여 추출 후보를 리포팅한다.

```
대상 파일에서 재사용 가능한 위젯 패턴을 감지한다:

- 구조적 중복: 비슷한 위젯 트리가 2곳 이상 반복
- 비대한 build: build 메서드 50줄 이상, 분리 가능한 서브트리
- 범용 private 위젯: feature 특화 로직 없는 _WidgetName이 shared로 추출 가능
- 패턴 반복: 같은 위젯 트리 구조가 다른 이름으로 반복

대상 파일: [파일 목록]
프로젝트 shared 위젯 경로: {감지된 shared 경로}

각 추출 후보마다 파일:라인, 감지 기준, 추출 제안(위젯 이름 + 배치 경로)을 출력한다.
```
```

- [ ] **Step 3: Report Format에 Reusability 섹션 추가**

`flutter-audit/SKILL.md`의 Report Format 섹션에 추가:

```markdown
Reusability
  candidates: N
  [추출 후보 목록]
```

- [ ] **Step 4: deep 모드 설명 업데이트**

`3개 전문 에이전트를 병렬로 실행한다` → `최대 4개 전문 에이전트를 병렬로 실행한다` 로 변경. Widget Inspector는 항상 실행되므로 조건부 에이전트(Design Review, i18n)와 달리 기본 포함.

- [ ] **Step 5: 커밋**

```bash
git add flutter-toolkit/skills/flutter-audit/SKILL.md
git commit -m "feat: flutter-audit에 위젯 재사용성 감사 연동

quick 모드에 Reusability 체크리스트 추가.
deep 모드에 Agent 4: Widget Inspector 추가."
```

---

### Task 4: README 업데이트

**Files:**
- Modify: `flutter-toolkit/README.md`

- [ ] **Step 1: 스킬 목록에 flutter-extract 추가**

README의 스킬 목록 테이블에 행 추가:

```markdown
| `flutter-extract` | 재사용 가능한 위젯 추출 (private→shared, 인라인 분리, 중복 통합) |
```

- [ ] **Step 2: 에이전트 섹션 추가**

스킬 목록 테이블 뒤에 에이전트 섹션 추가:

```markdown
## 에이전트 목록 (1개)

| 에이전트 | 설명 |
|----------|------|
| `widget-inspector` | 재사용 가능한 위젯 패턴 감지 + 리포팅 (읽기 전용, quick/deep 모드) |
```

- [ ] **Step 3: 스킬 수 업데이트**

`## 스킬 목록 (15개)` → `## 스킬 목록 (16개)`

- [ ] **Step 4: 커밋**

```bash
git add flutter-toolkit/README.md
git commit -m "docs: README에 widget-inspector 에이전트, flutter-extract 스킬 추가"
```
