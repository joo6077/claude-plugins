---
name: flutter-skeleton
description: >
  Flutter 화면/페이지의 로딩 상태를 스켈레톤 shimmer로 구현한다.
  CircularProgressIndicator 대신 shimmer 패키지 shimmer 블록을 사용하여
  실제 Flutter 위젯 레이아웃과 동일한 구조의 스켈레톤을 만든다.
  '로딩 화면', '스켈레톤', 'shimmer', 'loading state', '로딩 UI',
  '스피너 교체', 'CircularProgressIndicator 대체', '로딩 스켈레톤 추가',
  '빈 화면 로딩', 'skeleton loading', 'placeholder UI' 같은 Flutter 프로젝트 요청 시 사용한다.
argument-hint: "<screen_or_page_name>"
user-invocable: true
---

## Gotchas

- 색상은 `context.colors.xxx` 시맨틱 토큰 사용 — shimmer 배경색에 `Colors.grey` 하드코딩하면 다크 모드에서 깨짐
- 수치값은 `AppRadii`, `AppPadding` 디자인 토큰 사용 — 실제 레이아웃과 동일한 구조여야 로딩→컨텐츠 전환이 자연스럽다

화면/페이지의 `loading` 상태를 스켈레톤 shimmer로 구현한다.

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$FLUTTER`, `$DART`, `$PACKAGE`, `ARCH`, `HAS_DS` 등)를 사용한다.

### Shimmer 패키지 감지

`pubspec.yaml`에서 shimmer 관련 패키지를 탐지한다:

| 패키지 | 감지 키 | Shimmer 위젯 |
|--------|---------|-------------|
| `shimmer` | `HAS_SHIMMER` | `Shimmer.fromColors(child:)` |
| `skeletonizer` | `HAS_SKELETONIZER` | `Skeletonizer(child:)` |
| `shimmer_animation` | `HAS_SHIMMER_ANIMATION` | `Shimmer(child:)` |
| 프로젝트 커스텀 shimmer 위젯 | `HAS_CUSTOM_SHIMMER` | `lib/`에서 `Shimmer` 클래스 탐색 |

**패키지가 없으면:**
> "shimmer 패키지가 pubspec.yaml에 없습니다. 스켈레톤을 구현하려면 먼저 설치해주세요:
> `$FLUTTER pub add shimmer`
> 또는 `$FLUTTER pub add skeletonizer`"

프로젝트에 커스텀 shimmer 위젯이 있으면 해당 위젯을 우선 사용한다.

## 핵심 원칙

스켈레톤의 목표는 **레이아웃 점프 제로**다. 로딩 중 스켈레톤과 로드 완료 후 실제 UI가 정확히 같은 위치, 같은 크기를 차지해야 한다.

### 고정 UI vs Shimmer 구분

이 구분이 스켈레톤 설계의 전부다. 서버 응답 없이 알 수 있는 것은 고정 렌더, 서버 데이터가 필요한 것만 shimmer.

| 고정 렌더 (즉시 표시) | Shimmer (서버 대기) |
|---|---|
| 헤더 타이틀 텍스트 | 사용자 이름, 핸들, 바이오 |
| 헤더 아이콘 버튼 (뒤로, 설정 등) | 팔로워/팔로잉 숫자 |
| 고정 라벨 (followers, following 등) | 프로필 사진, 아바타 |
| 탭바 텍스트 | 리스트 아이템 내용 |
| 뷰 토글, 필터 버튼 | 통계 수치, 퍼센트 |
| 구분선, 프레임 | 설정값 (토글 상태 등) |

**판단 기준:** "이 값이 서버 응답 전에 확정되는가?" -- Yes면 고정, No면 shimmer.

### Shimmer 크기 규칙

shimmer 블록은 실제 텍스트/위젯과 **동일한 크기**여야 한다.

```text
shimmer height = fontSize
shimmer borderRadius = max(fontSize * 0.3, 3)
```

| fontSize | shimmer height | borderRadius | 사용처 예 |
|---|---|---|---|
| 18px | 18 | 5 | 큰 숫자, 이름 |
| 15px | 15 | 4 | 상세 이름 |
| 14px | 14 | 4 | 리스트 제목, 설정 라벨 |
| 13px | 13 | 4 | 본문 (바이오, 설명) |
| 12px | 12 | 4 | 핸들, 서브텍스트 |
| 11px | 11 | 3 | 보조 텍스트, 멤버 수 |
| 10px | 10 | 3 | 칩 라벨, 캡션 |

아이콘/아바타는 실제 위젯과 동일한 size, borderRadius 적용:
- 원형 아바타: shimmer `height: size`, 원형 처리
- 아이콘 박스: `width: size, height: size`
- 배지/태그: pill 형태 그대로 유지

shimmer width는 예상 콘텐츠 길이에 맞춰 적당히 설정 (정확할 필요 없음, height가 중요).

## Shimmer 블록 구현

프로젝트에 감지된 shimmer 패키지에 따라 블록을 구성한다.

### shimmer 패키지 사용 시

```dart
// 텍스트 자리
Container(
  width: 80,
  height: 18,
  decoration: BoxDecoration(
    color: Colors.white,
    borderRadius: BorderRadius.circular(5),
  ),
)
// Shimmer.fromColors로 래핑
```

### skeletonizer 패키지 사용 시

실제 위젯을 그대로 `Skeletonizer(enabled: true, child: ...)` 로 래핑한다. 별도 shimmer 블록 불필요.

### 커스텀 shimmer 위젯 사용 시

프로젝트의 기존 shimmer 위젯 API를 분석하여 동일한 패턴으로 사용한다.

## 스켈레톤 위젯 구현 절차

### 1. 대상 화면의 실제 레이아웃 분석

대상 화면의 데이터 로드 완료 상태 코드를 읽고 레이아웃 구조를 파악한다:
- 어떤 Sliver/Column/Row 구조인가
- 어떤 위젯이 고정이고 어떤 값이 서버 데이터인가
- 각 텍스트의 fontSize는 몇인가 (Theme TextStyle 또는 직접 지정)

### 2. 스켈레톤 위젯 파일 생성

`ARCH`에 따라 파일 위치 결정:

| ARCH | 파일 경로 |
|------|----------|
| `clean` | `lib/features/<feature>/presentation/widgets/<feature>_<page>_skeleton.dart` |
| `feature_first` | `lib/features/<feature>/widgets/<feature>_<page>_skeleton.dart` |
| `flat` | `lib/widgets/<page>_skeleton.dart` |

### 3. 레이아웃 복제 + shimmer 배치

실제 위젯의 레이아웃 구조를 **그대로** 복제한다. 동일한:
- Padding, SizedBox 간격
- Row/Column 배치
- Sliver 구조 (CustomScrollView 사용 시)
- Expanded/Flexible 비율

서버 데이터 자리에만 shimmer 블록을 넣고, 고정 UI는 실제 위젯을 그대로 사용한다.

```dart
// -- 잘못된 예: 모든 것을 shimmer로 대체
Column(children: [
  ShimmerBlock(width: 200, height: 40),  // 헤더까지 shimmer
  ShimmerBlock(width: 100, height: 20),  // 탭바까지 shimmer
])

// -- 올바른 예: 고정 UI 유지, 서버 데이터만 shimmer
Column(children: [
  AppBar(title: Text('프로필')),  // 고정 헤더 그대로
  Row(children: [
    ShimmerBlock(width: 32, height: 18, borderRadius: 5),  // 숫자만 shimmer
    Text('팔로워', style: ...),  // 라벨은 고정
  ]),
])
```

### 4. loading 상태 교체

프로젝트의 상태 관리 패턴에 맞게 loading 상태를 교체한다:

```dart
// Before
loading: () => const Center(child: CircularProgressIndicator()),

// After
loading: () => const ProfileSkeleton(),
```

### 5. 체크리스트

- [ ] 모든 shimmer height가 실제 fontSize와 일치하는가
- [ ] 고정 UI(라벨, 탭바, 헤더)가 실제 위젯을 사용하는가
- [ ] Padding, 간격이 실제 레이아웃과 동일한가
- [ ] Sliver 구조가 실제 화면과 동일한가 (pinned header 등)
- [ ] `$FLUTTER analyze` 통과하는가

## Rules

- **MUST** 프로젝트에 존재하는 shimmer 패키지/위젯을 우선 사용한다 -- 통일된 shimmer 스타일이 시각적 일관성을 보장한다
- **MUST** 고정 UI와 shimmer 영역을 반드시 분리한다 -- 모든 것을 shimmer로 대체하면 레이아웃 점프가 발생하고 UX가 떨어진다
- **MUST** shimmer height는 실제 fontSize와 일치시킨다 -- 높이 불일치는 로딩 → 데이터 전환 시 레이아웃 점프를 유발한다
- **MUST** 실제 화면의 레이아웃 구조를 그대로 복제한다 -- 간격, 패딩, 비율이 다르면 스켈레톤의 목적(레이아웃 점프 제로)이 무의미하다
- **MUST** 디자인 시스템 토큰이 있으면(`HAS_DS = true`) spacing/radius에 프로젝트 토큰을 사용한다

### HAS_DS = true인 경우 토큰 적용

shimmer 블록의 borderRadius에 프로젝트의 radius 토큰을 사용한다:
- 프로젝트에 radius 토큰 클래스가 있으면 (예: `AppRadii.sm`, `BorderRadii.xs`) 해당 토큰 사용
- 없으면 `borderRadius = max(fontSize * 0.3, 3)` 공식 사용

아이콘/아바타 shimmer에도 프로젝트 토큰 적용:
- 아이콘 박스: 프로젝트의 radius 토큰으로 borderRadius 설정
- 원형 아바타: circle 파라미터 또는 `borderRadius: size/2`

기존 스켈레톤 구현이 있으면 먼저 참조한다 — 프로젝트에서 `*skeleton*`, `*shimmer*`, `*loading*` 키워드로 검색하여 기존 패턴을 확인한다
- **MUST NOT** `CircularProgressIndicator`를 전체 화면 로딩에 사용한다 -- 스켈레톤이 사용자에게 콘텐츠 구조를 예고하여 체감 로딩 시간을 줄인다
