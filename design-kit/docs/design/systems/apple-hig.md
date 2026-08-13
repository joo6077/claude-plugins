---
title: Apple Human Interface Guidelines 분석
version: 0.3.0
last_updated: 2026-03-30
---

# Apple Human Interface Guidelines 분석

Apple HIG의 핵심 원칙, iOS/macOS/visionOS/watchOS/CarPlay 플랫폼별 차이, SF Symbols 심층, 주요 컴포넌트 패턴을 다룬다.

---

## 핵심 원칙

Apple HIG의 디자인 철학은 4가지 근본 기둥으로 구성된다.

### 1. 명확성 (Clarity)

인터페이스의 모든 요소는 읽기 쉽고 이해하기 쉬워야 한다.

- **텍스트 가독성**: 모든 크기에서 읽을 수 있는 명확한 텍스트, 선명한 아이콘
- **시각 위계**: 크기, 색상, 무게를 통해 중요도를 신호한다
- **간결한 레이블**: 전문 용어를 피하고, 기능을 명확히 전달하는 직관적인 언어를 사용한다
- **기능적 아이콘**: SF Symbols 체계를 통해 일관되고 의미 전달이 명확한 아이콘을 제공한다

### 2. 존중 (Deference)

UI는 콘텐츠를 돋보이게 하는 역할을 하며, 사용자의 주의를 빼앗지 않는다.

- 유체적 애니메이션과 반투명 UI 요소로 콘텐츠가 주인공이 되도록 한다
- 인터페이스는 콘텐츠를 프레이밍하되 콘텐츠와 경쟁하지 않는다
- 최소한의 장식적 요소 — 기능적 목적이 없는 시각 요소를 배제한다
- 전체 화면 활용을 통해 몰입감을 극대화한다

### 3. 깊이 (Depth)

시각적 레이어링과 자연스러운 전환으로 공간적 맥락을 제공한다.

- **레이어**: 계층적 레이어를 통해 사용자의 현재 위치를 시각적으로 전달한다
- **그림자와 투명도**: z축 깊이감으로 요소 간 관계를 표현한다
- **전환 애니메이션**: 사용자가 어디에서 왔고 어디로 가는지 이해하도록 돕는 물리적 움직임
- **제스처 연속성**: 드래그, 스와이프 등 직접 조작이 공간감을 강화한다

### 4. 일관성 (Consistency)

플랫폼 전체에서 예측 가능한 사용 경험을 제공한다.

- 시스템 제공 컨트롤과 표준 패턴을 우선 사용한다
- 기존 사용자 기대에 부합하는 인터랙션 패턴을 따른다
- 앱 내부에서도 용어, 아이콘, 동작의 일관성을 유지한다

> **출처:** [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines)
> **출처:** [DEV Community — Navigating Apple's HIG: A Practical Guide](https://dev.to/matheussricardoo/navigating-apples-human-interface-guidelines-hig-a-practical-guide-26ka)

---

## 플랫폼별 가이드

Apple HIG는 각 플랫폼의 고유한 맥락과 입력 방식에 맞춘 차별화된 가이드를 제공한다.

### iOS (iPhone / iPad)

**핵심 특성**: 터치 중심, 휴대성, 한 손 조작 고려

| 항목 | 사양 |
|------|------|
| 최소 터치 타겟 | **44 x 44 pt** (Apple HIG 필수. WCAG 2.2 AA SC 2.5.8 하한은 24×24 CSS px, 44×44 는 AAA SC 2.5.5) |
| 탭 바 | 화면 하단, **최대 5개 탭** (iPhone) |
| 내비게이션 바 | 화면 상단, 뒤로가기/제목/액션 |
| Safe Area | 노치, Dynamic Island, 홈 인디케이터 고려 필수 |

**주요 설계 원칙:**

- **탭 바 중심 탐색**: 최상위 섹션은 탭 바로 전환, 계층 탐색은 내비게이션 스택으로 드릴다운
- **제스처 기반 인터랙션**: 스와이프 뒤로가기, 풀 투 리프레시, 길게 누르기 컨텍스트 메뉴
- **한 손 조작 배려**: 주요 액션 버튼을 화면 하단 또는 엄지 닿는 영역에 배치
- **적응형 레이아웃**: iPhone과 iPad에서 동일 앱이 크기에 맞게 레이아웃 조정 (Size Classes 활용)

> **출처:** [Apple — Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios)

### macOS

**핵심 특성**: 마우스/트랙패드 중심, 정밀한 포인팅, 다중 윈도우, 키보드 단축키

| 항목 | 사양 |
|------|------|
| 메뉴 바 높이 | **24 pt** (Big Sur 이후) |
| 최소 클릭 타겟 | 터치 타겟보다 작아도 됨 (정밀 포인팅) |
| 윈도우 컨트롤 | 닫기/최소화/전체화면 (좌측 상단 신호등) |
| 툴바 | 상단 배치, 커스터마이징 가능, 그룹화 지원 |

**iOS와 핵심 차이:**

- **사이드바 + 툴바**: macOS는 탭 바 대신 **사이드바**로 최상위 탐색, **툴바**로 액션 제공
- **메뉴 바**: macOS 고유 요소로, 앱의 모든 명령에 접근하는 전역 메뉴를 화면 최상단에 표시
- **커스터마이저블 툴바**: macOS/iPadOS 툴바는 사용자가 항목을 재배치할 수 있으며, iOS 툴바는 커스터마이징 불가
- **멀티 윈도우**: 동시에 여러 문서/윈도우를 열어 작업 가능
- **키보드 단축키**: Cmd+C/V 등 풍부한 단축키 체계, 메뉴 바에 단축키 표시

> **출처:** [Apple — Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars)
> **출처:** [Apple — The Menu Bar](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar)

### visionOS (Apple Vision Pro)

**핵심 특성**: 공간 컴퓨팅, 시선 추적 + 손 제스처 입력, 3D 환경

| 항목 | 특성 |
|------|------|
| 입력 방식 | 시선(eye tracking) + 핀치(hand gesture) |
| UI 표면 | 유리(glass) 질감, 반투명, 빛 투과 |
| 공간 개념 | 무한한 3D 공간에 윈도우 배치 |
| 그림자 | 실제 바닥에 투영되는 그림자 |

**iOS와 핵심 차이:**

- **윈도우 (Windows)**: SwiftUI 기반의 2D 인터페이스가 공간 내에 배치됨. 기존 뷰와 컨트롤을 포함하며, 3D 콘텐츠로 깊이를 추가할 수 있다
- **볼륨 (Volumes)**: RealityKit 또는 Unity로 구현된 3D 콘텐츠를 모든 각도에서 볼 수 있는 장면
- **몰입형 공간 (Immersive Spaces)**: 전체 몰입(Full Immersion)과 패스스루(Passthrough) 모드 사이에서 전환
- **네거티브 스페이스**: 2D 화면의 여백이 아닌, 실제 물리적 공간에서의 거리와 배치를 의미
- **인간 중심 설계**: 가상 환경에서도 동일한 인간 중심 디자인 원칙 유지. 시선 기반 인터랙션에는 높은 정밀도와 피드백이 필요

> **출처:** [Apple — Designing for visionOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos)
> **출처:** [Apple — Spatial Layout](https://developer.apple.com/design/human-interface-guidelines/spatial-layout)

---

## 주요 컴포넌트 패턴

### 내비게이션 바 (Navigation Bars)

화면 상단에 위치하며, 계층적 탐색의 현재 위치를 보여주고 뒤로가기 기능을 제공한다.

**구성 요소:**
- **뒤로가기 버튼**: 좌측, 이전 화면의 제목을 표시
- **현재 제목**: 중앙 정렬 (iOS), Large Title은 좌측 정렬로 스크롤 시 축소
- **트레일링 액션**: 우측에 편집, 공유 등 컨텍스트 액션 배치

**Large Title 패턴:**
- 정적 상태에서는 좌측 정렬된 큰 제목 (34pt)
- 스크롤 시 표준 크기(17pt)로 중앙 정렬되며 축소 전환
- 최상위 화면에서만 사용 권장, 하위 화면에서는 표준 크기 사용

> **출처:** [Apple — Navigation Bars](https://developer.apple.com/design/human-interface-guidelines/navigation-bars)

### 탭 바 (Tab Bars)

화면 하단에 위치하며, 앱의 최상위 섹션 간 즉각적인 전환을 제공한다.

**핵심 규칙:**
- iPhone에서는 **최대 5개 탭** (초과 시 "더보기" 탭 자동 생성)
- iPad에서는 상단 탭 바 또는 사이드바로 전환 가능
- 각 탭은 독립적인 탐색 상태를 유지한다 (탭 전환 후 돌아와도 이전 위치 유지)
- 아이콘 + 레이블 조합, SF Symbols 사용 권장
- 앱의 어떤 화면에서든 항상 접근 가능해야 한다

**iPadOS 18+ 변경사항:**
- 탭 바가 사이드바로 변형되는 적응형 탭 바 도입
- 컴팩트 모드(탭 바) ↔ 확장 모드(사이드바)를 사용자가 전환 가능

> **출처:** [Apple — Tab Bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars)

### 시트 (Sheets)

현재 맥락과 관련된 범위 한정 작업을 수행하기 위해 화면 하단에서 슬라이드업되는 모달 뷰.

**프레젠테이션 스타일:**

| 스타일 | 설명 |
|--------|------|
| **Page Sheet** | 이전 화면이 축소되어 뒤에 보임. 대형 디바이스에서 미가림 영역은 어두워짐 |
| **Form Sheet** | 화면 중앙에 표시. 정보 수집용 |
| **Full Screen** | 전체 화면 덮음. 복잡한 작업에 사용 |

**설계 원칙:**
- 모달 사용을 최소화한다 — 주의를 끌어야 하거나, 작업 완료/포기가 필요하거나, 중요 데이터 저장 시에만 사용
- 닫기/취소 동작을 항상 명확하게 제공한다 (스와이프 다운 또는 버튼)
- 시트 내부에서 추가 시트를 쌓지 않는 것을 권장한다

> **출처:** [Apple — Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets)

### 알럿 (Alerts)

사용자에게 즉시 필요한 중요 정보를 전달하는 모달 인터럽션.

**핵심 규칙:**
- **필수적이고 실행 가능한 정보에만** 사용한다 — 알럿은 경험을 중단시키므로 남용하지 않는다
- 제목은 간결하게, 본문은 선택사항이며 추가 설명이 필요할 때만 포함
- **버튼 배치**: 2개 버튼일 때 기본 액션은 우측(또는 상단), 취소는 좌측(또는 하단)
- **파괴적 액션**(삭제 등)은 빨간색으로 표시하고, 반드시 확인 단계를 거친다
- 알럿은 닫기 위해 반드시 탭이 필요하다 — 자동 사라짐 없음

**액션 시트 vs 알럿:**
- **알럿**: 시스템/앱이 주도적으로 알림 (예: 오류, 확인)
- **액션 시트**: 사용자 액션에 대한 선택지 제공 (예: 삭제 확인, 공유 옵션)

> **출처:** [Apple — Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts)
> **출처:** [Apple — Action Sheets](https://developer.apple.com/design/human-interface-guidelines/action-sheets)

---

## watchOS

Apple Watch는 가장 제한된 화면 크기와 짧은 인터랙션 시간을 가진 플랫폼이다.

### 핵심 특성

| 항목 | 사양 |
|------|------|
| 화면 크기 | 40mm: 162×197pt, 45mm: 176×215pt, Ultra: 185×223pt |
| 인터랙션 시간 | 평균 **2~5초** — "glance and go" 패턴 |
| 입력 방식 | 탭, 디지털 크라운 회전, 스와이프, Siri |
| 최소 터치 타겟 | **38pt** (iOS의 44pt보다 작지만, 시계 맥락에서 허용) |

### 설계 원칙

- **핵심 정보만 표시한다**: 1~2개 핵심 지표, 1~2개 액션. 리스트는 10개 이하 항목
- **네비게이션은 리스트 또는 페이지 기반**: 탭 바를 사용하지 않는다. 세로 스크롤 리스트 또는 수평 페이지 스와이프
- **컴플리케이션(Complication)**: 시계 화면에 앱 데이터를 표시하는 소형 위젯. 최대 3~4줄 텍스트, 게이지, 이미지 지원
- **알림 우선**: Watch 앱의 주 사용 패턴은 알림 확인 + 빠른 액션이다. 알림에 인라인 액션("승인", "거절")을 포함하면 앱을 열지 않아도 된다
- **Digital Crown 활용**: 스크롤, 줌, 값 조절에 사용. 정밀 입력이 필요한 곳(시간 설정, 볼륨)에서 터치보다 우수

> **출처:** [Apple — Designing for watchOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos)

---

## CarPlay

차량 내 사용을 위한 플랫폼으로, 운전 중 안전이 최우선이다.

### 핵심 특성

| 항목 | 사양 |
|------|------|
| 입력 방식 | 터치스크린, 노브/버튼(비터치 차량), Siri |
| 화면 비율 | 차량마다 다름 (가로형 다수) |
| 인터랙션 시간 | **최대 2초** — 운전 중 화면 주시 시간 제한 |
| 앱 유형 제한 | 오디오, 내비게이션, 메시지, 충전, 주차만 허용 |

### 설계 원칙

- **글랜스 가능한(glanceable) UI**: 큰 텍스트, 높은 대비, 단순한 레이아웃. 세부 정보는 Siri 또는 정차 시 표시
- **제한된 목록 길이**: Apple은 CarPlay 목록을 **최대 24개 항목**으로 제한한다. 실무적으로 한 화면에 4~6개가 적절
- **터치 타겟 확대**: 운전 중 정밀 터치가 어려우므로 터치 타겟을 iOS보다 크게 설정한다
- **Siri 통합 필수**: 음성으로 대부분의 기능에 접근 가능해야 한다
- **야간 모드**: 다크 배경 + 저밝기가 기본. 밝은 UI는 운전자 시야를 방해한다

> **출처:** [Apple — Designing for CarPlay](https://developer.apple.com/design/human-interface-guidelines/designing-for-carplay)
> **출처:** [Apple — CarPlay App Programming Guide](https://developer.apple.com/carplay/)

---

## SF Symbols 심층

SF Symbols는 Apple이 제공하는 6,000개 이상의 일관된 벡터 심볼 라이브러리다. San Francisco 시스템 폰트와 수직/무게 정렬이 보장된다.

### 렌더링 모드

| 모드 | 설명 | 적합한 용도 |
|------|------|-----------|
| **Monochrome** | 단색 렌더링. tintColor를 따름 | 대부분의 UI 아이콘 (기본값) |
| **Hierarchical** | 기본 색상에서 불투명도 레이어로 깊이 표현 | 복잡한 심볼에서 레이어 구분이 필요할 때 |
| **Palette** | 각 레이어에 개별 색상 할당 | 브랜드 색상 적용, 다색 아이콘 |
| **Multicolor** | Apple이 사전 정의한 고정 색상 | 날씨, 기기, 자연 관련 심볼 |

### 변수 값 (Variable Value)

SF Symbols 4+에서 도입된 기능으로, 0.0~1.0 범위의 값에 따라 심볼의 채움 수준이 변한다. 볼륨, 신호 강도, 배터리 잔량 같은 연속적 상태를 하나의 심볼로 표현한다.

```swift
// SwiftUI에서 변수 값 적용
Image(systemName: "wifi", variableValue: 0.67)
// 0.0: 빈 wifi, 0.33: 1칸, 0.67: 2칸, 1.0: 3칸 (풀)
```

### 자동 지역화

SF Symbols는 RTL(아랍어, 히브리어) 환경에서 방향이 의미를 가지는 심볼을 자동 미러링한다. 예: "chevron.right"는 RTL에서 자동으로 왼쪽을 가리킨다. "checkmark" 같은 방향 무관 심볼은 미러링하지 않는다.

### 커스텀 심볼 제작

Apple은 SF Symbols 앱에서 커스텀 심볼 템플릿(SVG)을 내보내기할 수 있다.

**규칙:**
- 9개 무게(Ultralight~Black) × 3개 스케일(Small/Medium/Large) = **27개 변형**을 모두 제작하는 것이 이상적이지만, 최소 Regular-Medium 1개만 제작하면 나머지는 자동 보간된다
- 레이어 구분을 올바르게 설정하면 Hierarchical/Palette/Multicolor 렌더링이 자동 적용된다
- 기본 심볼과 시각적 무게를 맞추기 위해 템플릿의 캡 높이(cap height) 가이드를 준수한다

> **출처:** [Apple — SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)
> **출처:** [Apple — Creating Custom Symbol Images](https://developer.apple.com/documentation/uikit/uiimage/creating_custom_symbol_images_for_your_app)
