---
name: design-component
description: >
  반복되는 UI 요소를 컴포넌트로 정의하고 카탈로그화한다.
  확정된 시안에서 추출하거나 사용자가 직접 지정한 요소를 대상으로,
  variant, 상태, 토큰 매핑을 포함한 디자인 스펙을 생성한다.
  컨셉, 토큰, 시안이 있으면 자동으로 로드하여 일관성을 유지한다.
  "컴포넌트 정의", "컴포넌트 리스트", "design component",
  "UI 컴포넌트 정리", "컴포넌트 만들어줘", "컴포넌트 카탈로그" 같은 요청 시 트리거.
  실제 코드 구현에는 트리거하지 않는다 — 해당 toolkit 플러그인 사용.
argument-hint: "[component-name or mockup-id]"
user-invocable: true
---

# Gotchas

1. **구현 코드 생성 금지** — 이 스킬은 디자인 스펙만 출력한다. Flutter/React/CSS 컴포넌트 코드를 직접 생성하지 마라. 해당 toolkit 플러그인에 위임하라.
2. **상태 누락 금지** — 모든 인터랙티브 컴포넌트에 default, hover, active, disabled 상태를 정의하라. loading 상태가 필요한 경우(버튼, 카드) 포함한다. 상태가 1-2개만 정의된 컴포넌트는 불완전하다.
3. **토큰 매핑 누락 금지** — 디자인 토큰이 존재하면 모든 컴포넌트의 컬러, 타이포, 간격, 라디우스를 토큰에 매핑하라. 하드코딩 값은 토큰 체계를 무력화한다.
4. **시안 ID 무시 금지** — 확정된 시안에서 컴포넌트를 추출할 때, 해당 컴포넌트의 시안 ID(`{컴포넌트명}-{해시}`)를 카탈로그에 기록하라. 출처 추적에 필요하다.
5. **커스터마이징 옵션 누락 금지** — 모든 컴포넌트에 개발자가 통계적으로 가장 많이 조정하는 옵션을 기본 고려하라. 해당 컴포넌트에 불필요한 옵션은 제외하되, 필요한 옵션을 빠뜨리면 실사용성이 떨어진다.
6. **API Doc 헤더 필수** — 모든 컴포넌트 산출물 상단에 프로그래밍 언어 API 문서 형식의 헤더를 포함하라. 컴포넌트 설명, 각 옵션의 이름/타입/허용값/기본값/의미를 명시한다. 헤더 없는 컴포넌트 스펙은 불완전하다.
7. **Anatomy 누락 금지** — 복합 컴포넌트(Dialog, Menu, Accordion 등)는 구성 요소(part) 계층을 명시하라. 어떤 part가 필수/선택인지, 어떤 part가 상태를 가지는지 표기한다.
8. **접근성 섹션 누락 금지** — 인터랙티브 컴포넌트에 WAI-ARIA 역할/속성, 키보드 인터랙션 테이블, 라벨링 요구사항을 포함하라. 접근성 없는 컴포넌트 스펙은 불완전하다.
9. **When to use / When not to use 누락 금지** — 모든 컴포넌트에 사용 시점과 비사용 시점을 명시하라. 유사 컴포넌트(예: Menu vs Select, Dialog vs Sheet)와의 구분 기준을 포함한다.

# Process

## Step 0: 자동 감지 및 로드

프로젝트에서 이전 단계 산출물을 탐색한다:

```
# 감지 대상
.design/concept.md              → 컨셉 로드 (컬러/타이포/UI 패턴 방향)
**/theme/** **/tokens/**        → 디자인 토큰 로드
.design/mockups/*.html          → 확정 시안 로드
```

- 시안 존재 → 시안에서 반복되는 UI 요소를 자동 식별하여 제안
- 토큰 존재 → 컴포넌트별 토큰 매핑 자동 생성
- 둘 다 없음 → 사용자가 직접 컴포넌트 목록을 지정

## Step 1: 대상 파악

컴포넌트 대상을 결정한다:
- **시안에서 추출**: 사용자가 시안 ID로 지정 (예: "card-product-a3f2를 컴포넌트화해줘")
- **자동 식별**: 시안에서 2회 이상 반복되는 UI 패턴을 제안
- **사용자 직접 지정**: "버튼, 카드, 입력 필드 정의해줘"

## Step 2: 컴포넌트 분류 및 정의

references/component-spec-template.md의 포맷으로 각 컴포넌트를 정의한다.

### 2-1. 산출물 섹션 구조 (필수)

모든 컴포넌트 스펙은 아래 순서로 섹션을 포함한다 (MD3, Ant Design, Radix, Chakra, shadcn/ui 공통 패턴 기반):

1. **Purpose** — 컴포넌트명 + 한줄 설명
2. **When to use / When not to use** — 사용 시점, 유사 컴포넌트와 구분 기준
3. **Anatomy** — 구성 요소(part) 계층. 복합 컴포넌트는 필수/선택 part 명시
4. **Live Preview** — 기본 상태 렌더링
5. **Variants** — 시각적 변형 나열
6. **States** — Default, Hover, Active, Focus, Disabled, Loading
7. **Sizes** — S/M/L 등 크기 비교
8. **Props/API Table** — 아래 형식
9. **Accessibility** — ARIA 역할/속성, 키보드 인터랙션, 라벨링 요구사항
10. **Design Tokens** — 사용된 토큰 매핑
11. **Do / Don't** — 3~5개 규칙 (선택/계층/라벨링/레이아웃/오용)
12. **Related** — 유사/대체 컴포넌트 링크

### 2-2. API Doc 헤더 (필수)

모든 컴포넌트 스펙 상단에 아래 형식의 문서 헤더를 포함한다:

```
## Button

범용 액션 트리거 컴포넌트. 폼 제출, 네비게이션, 인라인 동작에 사용한다.

### When to use
- 사용자 액션을 트리거할 때 (제출, 확인, 취소)
- 인라인 동작 (삭제, 편집, 공유)

### When not to use
- 페이지 이동만 할 때 → Link 사용
- 토글 상태 전환 → Switch 또는 ToggleButton 사용

### Anatomy
- Root — 클릭 영역 전체
- LeadingIcon (선택) — 좌측 아이콘
- Label — 텍스트 라벨
- TrailingIcon (선택) — 우측 아이콘
- Spinner (조건부) — loading=true일 때 표시

### Props

| Prop      | Type            | Allowed Values                 | Default | Required | Description          |
|-----------|-----------------|--------------------------------|---------|----------|----------------------|
| variant   | string          | primary · secondary · outline · ghost · destructive | primary | N | 시각적 스타일 변형 |
| size      | string          | xs · sm · md · lg · xl         | md      | N | 크기 (높이/패딩/폰트 연동) |
| color     | string          | primary · success · warning · error · neutral | primary | N | 색상 테마 |
| radius    | string          | none · sm · md · lg · full     | md      | N | 모서리 둥글기 |
| disabled  | boolean         | true · false                   | false   | N | 비활성 상태 |
| loading   | boolean         | true · false                   | false   | N | 로딩 상태 |
| icon      | ReactNode       | —                              | —       | N | 아이콘 요소 |
| fullWidth | boolean         | true · false                   | false   | N | 부모 너비 맞춤 |
| onClick   | (event) => void | —                              | —       | N | 클릭 이벤트 핸들러 |

### Accessibility
- Role: `button`
- 키보드: Enter/Space로 활성화
- `aria-disabled`: disabled=true일 때
- `aria-busy`: loading=true일 때
- 아이콘 전용 버튼은 `aria-label` 필수
```

### 2-3. 커스터마이징 옵션 체크리스트

컴포넌트 정의 시 아래 옵션을 **기본 검토**한다. 해당 컴포넌트에 불필요하면 제외하되, 필요한 옵션을 빠뜨리지 마라:

| 카테고리 | 옵션 | 흔한 값 | 적용 대상 |
|----------|------|---------|-----------|
| 스타일 변형 | variant | primary, secondary, outline, ghost, link, destructive | 버튼, 배지, 알림 |
| 크기 | size | xs, sm, md, lg, xl | 거의 모든 컴포넌트 |
| 색상 | color | primary, secondary, success, warning, error, neutral | 버튼, 배지, 태그, 알림 |
| 모서리 | radius | 0, 4px, 6px, 8px, 12px, 16px, 9999px(pill) | 카드, 버튼, 입력, 이미지 |
| 굵기 | weight | 300, 400, 500, 600, 700 | 텍스트 포함 컴포넌트 |
| 테두리 | border | none, 1px, 2px, 3px | 카드, 입력, 구분선 |
| 그림자 | shadow | none, sm, md, lg, xl | 카드, 모달, 드롭다운 |
| 간격 | padding | 4/8/12/16/20/24/32px | 카드, 컨테이너, 버튼 |
| 높이 | height | 28/32/36/40/44/48px | 버튼, 입력, 탭 |
| 투명도 | opacity | 0.5, 0.7, 0.85, 1 | 오버레이, 비활성 상태 |
| 아이콘 | icon | leading, trailing, only | 버튼, 입력, 메뉴 아이템 |
| 방향 | orientation | horizontal, vertical | 탭, 라디오 그룹, 디바이더 |
| 위치 | placement | top, bottom, left, right, auto | 툴팁, 드롭다운, 팝오버 |
| 밀도 | density | compact, default, comfortable | 테이블, 리스트, 폼 |
| 제어 | controlled | value/defaultValue, open/defaultOpen | 입력, 드롭다운, 다이얼로그 |

### 2-4. 분류 카테고리

- **액션**: 버튼, 링크, FAB
- **입력**: 텍스트 필드, 체크박스, 라디오, 드롭다운, 스위치
- **표시**: 카드, 리스트 아이템, 배지, 칩, 태그
- **네비게이션**: 탭, 사이드바 아이템, 브레드크럼
- **피드백**: 토스트, 다이얼로그, 바텀시트
- **레이아웃**: 디바이더, 스페이서, 컨테이너

## Step 3: 사용자 피드백

- templates/catalog.md 포맷으로 컴포넌트 카탈로그를 생성하고 사용자에게 제시
- 피드백을 받아 수정 (variant 추가/제거, 상태 조정, 토큰 변경)
- 확정 시 `.design/components/catalog.md`에 저장

# References

- `references/component-spec-template.md` — 컴포넌트 정의 템플릿
- `templates/catalog.md` — 컴포넌트 카탈로그 출력 포맷
