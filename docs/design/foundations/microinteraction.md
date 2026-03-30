---
title: 마이크로인터랙션
version: 0.2.0
last_updated: 2026-03-30
---

# 마이크로인터랙션

UI의 세부 인터랙션을 설계하는 원칙, 구조, 피드백 패턴, 제스처, 성능 고려사항을 정리한다.

---

## 원칙

### 1. 마이크로인터랙션은 4가지 부품으로 구성된다

Dan Saffer는 "Microinteractions: Designing with Details"에서 모든 마이크로인터랙션이 4가지 구성 요소로 이루어진다고 정의했다.

| 구성 요소 | 역할 | 예시 (좋아요 버튼) |
|-----------|------|-------------------|
| **Trigger (트리거)** | 인터랙션을 시작하는 이벤트 | 하트 아이콘 탭 |
| **Rules (규칙)** | 인터랙션의 동작 순서와 제약 | 이미 좋아요면 취소, 아니면 추가 |
| **Feedback (피드백)** | 규칙이 적용되고 있음을 알려주는 신호 | 하트가 빨갛게 채워지고 스케일 애니메이션 |
| **Loops & Modes (반복/모드)** | 인터랙션의 지속 시간과 변화 | 좋아요 카운트 증가, 상태 서버 동기화 |

> **출처:** [Dan Saffer — Microinteractions: Designing with Details (O'Reilly)](https://www.oreilly.com/library/view/microinteractions/9781449342760/)

### 2. 피드백 없는 인터랙션은 고장난 것처럼 느껴진다

사용자가 행동했는데 시스템이 아무 반응을 보이지 않으면, 사용자는 "동작하지 않았다"고 판단하고 반복 클릭한다. Jakob Nielsen의 시스템 가시성(Visibility of System Status) 휴리스틱은 시스템이 적절한 시간 내에 적절한 피드백을 제공해야 한다고 명시한다.

> **출처:** [NNGroup — 10 Usability Heuristics for User Interface Design](https://www.nngroup.com/articles/ten-usability-heuristics/)

### 3. 애니메이션은 기능이다

마이크로인터랙션의 애니메이션은 장식이 아니다. 상태 변화를 설명하고, 인과 관계를 전달하며, 사용자의 주의를 안내한다. Material Design은 "모션은 의미 있는 것이어야 한다(Motion should be meaningful)"라고 규정한다.

> **출처:** [Material Design 3 — Motion Overview](https://m3.material.io/styles/motion/overview)

### 4. 과잉 인터랙션은 피로를 유발한다

모든 요소에 애니메이션을 넣으면 화려해 보이지만, 반복 사용 시 피로감이 누적된다. 첫인상에 좋은 것과 100번째 사용에도 좋은 것은 다르다. 핵심 상태 전환에만 모션을 적용하고 나머지는 즉각 반응(instant feedback)으로 처리한다.

---

## 트리거 유형

### 사용자 발동 트리거 (User-Initiated)

사용자의 의도적 행위가 인터랙션을 시작하는 경우다.

| 트리거 | 설명 | 예시 |
|--------|------|------|
| **Tap/Click** | 가장 기본적인 트리거 | 버튼 클릭, 체크박스 토글 |
| **Long Press** | 일정 시간(300–500ms) 누르기 | 컨텍스트 메뉴, 드래그 모드 진입 |
| **Swipe** | 수평/수직 슬라이드 | 카드 삭제, 페이지 전환 |
| **Pull** | 끌어당기기 | Pull-to-refresh |
| **Pinch** | 두 손가락 벌리기/모으기 | 줌 인/아웃 |
| **Scroll** | 스크롤 위치 기반 | 앱바 축소, FAB 숨기기 |
| **Type** | 텍스트 입력 | 실시간 검색, 입력 유효성 검사 |
| **Voice** | 음성 입력 | 음성 검색 시작 |

### 시스템 발동 트리거 (System-Initiated)

사용자 행위 없이 시스템 상태 변화가 인터랙션을 시작하는 경우다.

| 트리거 | 조건 | 예시 |
|--------|------|------|
| **Data Change** | 서버 데이터 갱신 | 새 메시지 배지, 실시간 주가 |
| **Time** | 특정 시간 경과 | 세션 만료 경고, 자동 저장 |
| **Location** | 위치 변경 | 근처 매장 알림 |
| **Error** | 오류 발생 | 네트워크 끊김 배너, 입력 오류 |
| **Threshold** | 임계값 도달 | 배터리 20% 경고, 저장 공간 부족 |

---

## 피드백 패턴

### 시각적 피드백 (Visual)

가장 보편적이고 필수적인 피드백 유형이다.

| 패턴 | 지속 시간 | 용도 |
|------|-----------|------|
| **색상 변화** | 100–200ms | 버튼 프레스, 선택 상태 |
| **크기 변화** | 100–300ms | 좋아요 하트, 아이콘 탭 |
| **투명도 변화** | 100–200ms | 비활성/활성 전환 |
| **위치 이동** | 200–500ms | 스와이프 삭제, 드래그 |
| **회전** | 반복 | 로딩 스피너 |
| **체크마크 그리기** | 300–400ms | 작업 완료 확인 |
| **프로그레스 바** | 가변 | 업로드, 다운로드 진행 |
| **Ripple 효과** | 300–400ms | Material 터치 피드백 |
| **스켈레톤 shimmer** | 로딩 중 | 콘텐츠 로딩 상태 |

### 촉각 피드백 (Haptic)

모바일 디바이스에서 물리적 진동으로 피드백을 전달한다.

| 유형 | 강도 | 용도 |
|------|------|------|
| **Light Impact** | 약함 | 토글 전환, 선택 |
| **Medium Impact** | 중간 | 스냅 포인트 도달, 슬라이더 값 변경 |
| **Heavy Impact** | 강함 | 삭제 확인, 에러 |
| **Selection** | 미세 | 피커 스크롤, 리스트 선택 |
| **Success/Warning/Error** | 패턴별 | 결제 완료, 경고, 실패 |

Apple의 Taptic Engine은 이러한 촉각 피드백을 세밀하게 제어할 수 있다. Android도 HapticFeedbackConstants로 유사한 피드백을 제공한다.

> **출처:** [Apple HIG — Playing Haptics](https://developer.apple.com/design/human-interface-guidelines/playing-haptics)

### 청각 피드백 (Audio)

소리는 강력하지만 가장 신중하게 사용해야 하는 피드백이다. 공공장소에서 소리는 사회적 부담이 된다.

| 사용 적합 | 사용 부적합 |
|-----------|-------------|
| 결제 완료 (카드 터치음) | 모든 버튼 클릭 |
| 에러 알림 | 스크롤 |
| 메시지 수신 | 페이지 전환 |
| 타이머 완료 | 폼 입력 |

원칙: 소리는 **시각적 피드백의 보강**으로만 사용하고, 유일한 피드백 수단으로 사용하지 않는다. 항상 음소거 상태에서도 동작해야 한다.

---

## 상태 전환

### 버튼 상태

| 상태 | 시각 처리 | 전환 시간 |
|------|-----------|-----------|
| **Default** | 기본 색상, 기본 elevation | — |
| **Hover** | 배경 5% overlay | 100ms ease |
| **Pressed** | 배경 10% overlay + ripple | 즉시(ripple 300ms) |
| **Focused** | 포커스 링 (2px outline) | 즉시 |
| **Disabled** | opacity 0.38, 클릭 불가 | — |
| **Loading** | 텍스트 → 스피너 교체 | 200ms fade |

### 토글/스위치 애니메이션

```
[OFF 상태]                    [ON 상태]
┌─────────────────┐          ┌─────────────────┐
│ ○               │   →→→    │               ● │
│  gray track     │  200ms   │  brand track    │
└─────────────────┘  ease    └─────────────────┘

전환 요소:
- 썸(thumb) 위치: 좌 → 우 (200ms, ease-in-out)
- 트랙 색상: gray → brand color (200ms)
- 썸 크기: pressed 시 1.2x 확대 후 복귀
```

### 체크박스 애니메이션

```
[Unchecked]     [Checked]      [Indeterminate]
┌───┐           ┌───┐          ┌───┐
│   │    →      │ ✓ │    →     │ ─ │
└───┘  150ms    └───┘  150ms   └───┘

전환: 체크마크가 좌하→우상 방향으로 그려지는 path animation
```

### 확장/축소 전환

```
[Collapsed]                    [Expanded]
┌─────────────────────┐       ┌─────────────────────┐
│ Section Title    ▶  │  →    │ Section Title    ▼  │
└─────────────────────┘       ├─────────────────────┤
                              │ Content area        │
                     250ms    │ ...                  │
                     ease-out └─────────────────────┘

- 높이 변화: 0 → auto (CSS: max-height transition)
- 아이콘 회전: ▶ → ▼ (90도, 200ms)
- 콘텐츠 fade-in: opacity 0 → 1 (200ms, 50ms delay)
```

---

## 제스처 인터랙션

### Pull-to-Refresh

Loren Brichter가 Tweetie 앱에서 처음 도입한 패턴으로, 현재 iOS와 Android 모두 시스템 수준에서 지원한다.

| 단계 | 동작 | 피드백 |
|------|------|--------|
| Pull 시작 | 아래로 당기기 | 인디케이터 노출 시작 |
| 임계치 도달 | 특정 거리(60–80dp) 이상 당김 | 인디케이터 완전 노출 + haptic snap |
| 릴리즈 | 손 떼기 | 인디케이터 회전(로딩 시작) |
| 완료 | 데이터 갱신 완료 | 인디케이터 사라짐 (300ms fade) |

### Swipe-to-Dismiss / Swipe Actions

| 구현 요소 | 규격 |
|-----------|------|
| 최소 스와이프 거리 | 아이템 너비의 25–33% |
| 스와이프 속도 임계치 | 500dp/s 이상이면 짧은 거리도 동작 |
| 배경 색상 | 삭제: red, 보관: blue/green, 기타: gray |
| 되돌리기(Undo) | Snackbar로 5–10초간 Undo 제공 |
| 반대 방향 | 좌→우, 우→좌에 서로 다른 액션 할당 가능 |

### Long Press

| 요소 | 규격 |
|------|------|
| 인식 시간 | 300–500ms (iOS: 500ms, Android: 400ms) |
| 피드백 시작 | 200ms 경과 시 시각적 힌트(scale 0.95x) |
| 완료 피드백 | haptic + 컨텍스트 메뉴 표시 |
| 취소 | 손가락을 영역 밖으로 이동하면 취소 |

### Pinch-to-Zoom

| 요소 | 규격 |
|------|------|
| 최소 스케일 | 1.0x (원본 이하 축소 불가가 기본) |
| 최대 스케일 | 3.0–5.0x (콘텐츠에 따라) |
| 스냅 포인트 | 1.0x, 2.0x, fit-to-width |
| 더블탭 줌 | 1.0x ↔ 2.0x 토글 (300ms ease) |
| 관성(momentum) | 핀치 릴리즈 후 관성 스케일링 |

---

## 성능 고려사항

### 60fps 유지 원칙

인간의 눈은 약 16.67ms(1000ms / 60fps) 간격의 프레임 갱신을 부드럽게 인식한다. 프레임이 이 간격을 넘으면 버벅거림(jank)이 발생한다.

### GPU 가속 가능한 속성

브라우저 렌더링 파이프라인에서 **compositor thread**에서 처리되는 속성만 GPU 가속이 가능하다.

| 속성 | GPU 가속 | 리플로우 | 리페인트 |
|------|----------|----------|----------|
| `transform` | O | X | X |
| `opacity` | O | X | X |
| `filter` | O | X | O |
| `width/height` | X | O | O |
| `top/left` | X | O | O |
| `margin/padding` | X | O | O |
| `background-color` | X | X | O |
| `box-shadow` | X | X | O |

핵심 규칙: **transform과 opacity만 애니메이션한다.** 위치 이동은 `top/left` 대신 `transform: translate()`, 크기 변화는 `width/height` 대신 `transform: scale()`을 사용한다.

> **출처:** [Smashing Magazine — CSS GPU Animation: Doing It Right](https://www.smashingmagazine.com/2016/12/gpu-animation-doing-it-right/)

### will-change 사용법

```css
/* GOOD: 애니메이션 직전에 적용, 직후에 제거 */
.card:hover {
  will-change: transform;
}
.card.animating {
  transform: scale(1.05);
}

/* BAD: 모든 요소에 상시 적용 */
* {
  will-change: transform, opacity; /* GPU 메모리 폭발 */
}
```

- `will-change`는 브라우저에 "이 요소가 곧 변할 것"이라 알리는 힌트다
- 페이지당 1–2개 요소에만 적용한다
- 모바일에서 과다 사용하면 메모리 부족으로 브라우저가 크래시할 수 있다

### prefers-reduced-motion 대응

전정기관(vestibular) 장애가 있는 사용자는 모션에 의해 어지러움, 두통, 구역질을 경험할 수 있다. 전 세계적으로 7,000만 명 이상이 전정기관 장애를 겪는다.

```css
/* 기본: 애니메이션 적용 */
.element {
  transition: transform 300ms ease;
}

/* reduced-motion: 애니메이션 제거 또는 최소화 */
@media (prefers-reduced-motion: reduce) {
  .element {
    transition: none;
  }
}
```

> **출처:** [MDN — prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion)

### Flutter 성능 최적화

```dart
// GOOD: RepaintBoundary로 리페인트 범위 격리
RepaintBoundary(
  child: AnimatedContainer(
    duration: const Duration(milliseconds: 200),
    // ...
  ),
)

// BAD: 전체 위젯 트리가 매 프레임 리빌드
setState(() {
  // 애니메이션 상태 변경 → 전체 build() 재실행
});

// GOOD: AnimationController + AnimatedBuilder로 격리
AnimatedBuilder(
  animation: _controller,
  builder: (context, child) => Transform.scale(
    scale: _scaleAnimation.value,
    child: child, // child는 리빌드 안 됨
  ),
  child: const ExpensiveWidget(),
)
```

---

## 타이밍 가이드

### 지속 시간별 용도

| 시간 | 체감 | 용도 |
|------|------|------|
| 0–100ms | 즉각 반응 | 버튼 프레스 피드백, 토글 |
| 100–300ms | 빠른 전환 | 페이드, 색상 변화, 작은 이동 |
| 300–500ms | 표준 전환 | 화면 전환, 모달 열기/닫기, 확장/축소 |
| 500–1000ms | 의도적 지연 | 복잡한 레이아웃 변화, 오케스트레이션 |
| 1000ms+ | 느린 전환 | 주의 — 대부분의 경우 너무 느림 |

### 이징 커브

| 커브 | 용도 |
|------|------|
| **ease-out** (decelerate) | 화면 진입 — 빠르게 들어와서 감속 |
| **ease-in** (accelerate) | 화면 퇴장 — 천천히 시작해서 가속으로 사라짐 |
| **ease-in-out** | 화면 내 요소 이동 — 부드러운 시작과 끝 |
| **linear** | 반복 회전(스피너), 프로그레스 바 |
| **spring** | 바운스 효과 — 자연스러운 물리 시뮬레이션 |

> **출처:** [Material Design 3 — Easing and Duration](https://m3.material.io/styles/motion/easing-and-duration/tokens-specs)

---

## 안티패턴

| 안티패턴 | 문제 | 해결 |
|----------|------|------|
| 모든 요소에 애니메이션 | 100번째 사용에서 피로감 | 상태 전환에만 모션 적용 |
| 느린 애니메이션(>500ms) | 반복 작업에서 답답함 | 200–300ms로 단축 |
| 피드백 없는 클릭 | "동작했나?" 반복 클릭 | 즉각적 시각/촉각 피드백 |
| width/height 애니메이션 | 프레임 드롭, 버벅거림 | transform으로 대체 |
| reduced-motion 미대응 | 전정 장애 사용자 배제 | @media 쿼리로 대응 |
| 자동 재생 캐러셀 | 읽는 중 콘텐츠가 사라짐 | 사용자 제어 또는 정지 버튼 |

---

## 참고 문헌

- [Dan Saffer — Microinteractions: Designing with Details (O'Reilly)](https://www.oreilly.com/library/view/microinteractions/9781449342760/)
- [NNGroup — 10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)
- [Material Design 3 — Motion Overview](https://m3.material.io/styles/motion/overview)
- [Apple HIG — Playing Haptics](https://developer.apple.com/design/human-interface-guidelines/playing-haptics)
- [Smashing Magazine — CSS GPU Animation: Doing It Right](https://www.smashingmagazine.com/2016/12/gpu-animation-doing-it-right/)
- [MDN — prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion)
- [W3C — WCAG 2.3.3: Animation from Interactions](https://www.w3.org/WAI/WCAG21/Understanding/animation-from-interactions.html)
