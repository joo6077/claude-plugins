---
title: Flutter-Figma Parity 자가검증 루프 패턴
version: 0.1.0
last_updated: 2026-05-07
source: /insights 2026-05-07 fresh report (130 sessions, "5시간 이상을 태운 Flutter–Figma parity 작업")
---

# Flutter-Figma Parity 자가검증 루프 패턴

> **상위 규약:** `visual-evidence-protocol.md`. 본 문서는 그 규약의 **Figma 대조 특화 확장**이다.
> 역할 경계 — 상위 규약은 "시각 산출물의 완료를 증거 없이 선언하지 않는다"(모든 UI 스킬 공통,
> E2), 본 문서는 "Figma 시안과의 차이를 SSIM 수치로 수렴시킨다"(Figma 작업 한정). 상위 규약의
> Step 1(채널 감지) · Step 3(증거 유효성) · Step 4(degraded 모드) 를 먼저 통과한 뒤 아래 루프로
> 이어간다. **빈 캡처는 SSIM 을 계산할 대상이 아니라 검증 실패 신호**이며, 마커·임계값은 상위
> 규약이 인용하는 canonical 정의를 따른다 (여기서 재정의하지 않는다).

## 배경

`/insights` 2026-05-07 fresh report 에서 가장 큰 마찰 지점으로 명시된 항목:

> **시도해볼 기능 → 야심찬 워크플로우:** 5시간 이상을 태운 Flutter–Figma parity 작업이 최고 레버리지 타깃입니다. 스크린샷, Figma와 픽셀 diff, FigmaDecoration 파라미터를 SSIM 수렴까지 자동 조정하는 자가검증 루프는 가장 고통스러운 세션을 측정 가능한 최적화 문제로 바꿔줍니다.

130 세션 분석에서 figma-flutter-kit 작업이 5시간+ 단일 세션 burn rate 1위. 본 문서는 그 마찰을 측정 가능한 최적화 문제로 reframe 하는 패턴을 다룬다.

## 핵심 아이디어 — measurable optimization loop

기존 워크플로우 (사용자 눈 의존):

```text
Figma 시안 확인 → Flutter 구현 → 스크린샷 캡처 → 사용자가 눈으로 비교 → "여기가 다름" → 수정 → 반복 N회
```

자가검증 루프 (측정값 의존):

```text
Figma 시안 캡처 → Flutter 렌더 캡처 → SSIM 측정 → 임계값 미달이면 차이 분석 → 파라미터 조정 → 재측정 → 수렴까지 반복
```

핵심 차이: **사용자 개입 없이 Claude 가 자율적으로 수렴할 수 있다.** SSIM (Structural Similarity Index) 가 0.95+ 되면 자동 종료, 미달이면 어느 영역의 어느 파라미터를 조정해야 하는지 measurement-guided.

## 도구 스택

| 단계 | 도구 | 비고 |
|------|------|------|
| Figma 캡처 | Figma MCP `get_screenshot` | 노드 ID 지정, PNG 추출 |
| Flutter 캡처 | flutter-playwright MCP `take_screenshot` 또는 integration_test golden | 렌더 결과 PNG |
| SSIM 측정 | Python `scikit-image.metrics.structural_similarity` 또는 `pixelmatch` (Node) | 0.0~1.0 score |
| 픽셀 diff | `pixelmatch` antialiasing-aware diff PNG 산출 | 차이 영역 시각화 |
| 파라미터 매핑 | FigmaDecoration / TextStyle / 색상 토큰 | diff 영역 → 어느 위젯 파라미터인지 추론 |

## 5-step 자가검증 루프

### Step 1: 시안 + 구현 동시 캡처

```python
# 의사 코드
figma_png = figma_mcp.get_screenshot(node_id=NODE_ID)
flutter_png = flutter_playwright.take_screenshot(route=ROUTE, device=DEVICE)
```

같은 viewport / DPR / 폰트 시스템에서 캡처. 디바이스 차이로 false-positive 발생 가능 — 픽셀 단위가 아닌 **device-independent pixel** 기준으로 정규화.

### Step 2: SSIM 측정

```python
from skimage.metrics import structural_similarity as ssim
score = ssim(figma_array, flutter_array, channel_axis=-1)
# 0.0 (완전히 다름) ~ 1.0 (동일)
# 임계값: 0.95 (visually identical), 0.85 (acceptable), <0.85 (rework 필요)
```

### Step 3: 픽셀 diff 영역 추출

```python
# pixelmatch 결과: 차이 픽셀 위치 + 크기 + 영역 bounding box
diff_regions = pixelmatch(figma_png, flutter_png, output=diff_png, threshold=0.1)
```

`diff_regions` 의 bounding box 가 어느 위젯 영역인지 매핑.

### Step 4: 파라미터 추론 + 조정

| 차이 패턴 | 후보 파라미터 |
|----------|--------------|
| 영역 전체 hue 차이 | `Color`, `LinearGradient.colors` |
| 윤곽 부드러움 | `BorderRadius`, `BoxShadow.blurRadius` |
| 인접 그림자 | `BoxShadow.offset`, `BoxShadow.spreadRadius` |
| 텍스트 굵기/장평 | `TextStyle.fontWeight`, `letterSpacing`, `height` |
| 위치 어긋남 | padding/margin, alignment, layout 위젯 (Stack offset 등) |
| 배경 텍스처 | `BoxDecoration.gradient` (linear vs radial), `image: DecorationImage` |

조정은 **한 번에 한 파라미터씩**. 여러 파라미터를 동시에 변경하면 무엇이 SSIM 을 올렸는지 attribution 안 됨.

### Step 5: 재측정 + 수렴 판정

```text
loop:
  capture → ssim → if score >= 0.95 break
  diff regions → parameter candidate → adjust 1 param
  → goto loop (max iter = 10)
```

10 회 iteration 내 미수렴 → 사용자 에스컬레이션. 무한루프 방지.

## 위젯별 파라미터 chain (Flutter 특화)

### Container / DecoratedBox

```dart
BoxDecoration(
  color: ...,                    // hue/saturation 차이
  gradient: LinearGradient(...), // multi-stop hue 차이
  borderRadius: BorderRadius.circular(...), // 윤곽 부드러움
  border: Border.all(...),       // 외곽선
  boxShadow: [BoxShadow(...)],   // 인접 그림자 / inset
  image: DecorationImage(...),   // 배경 텍스처
)
```

### Text

```dart
TextStyle(
  fontFamily: ...,    // 폰트 자체 차이 (Pretendard vs SF Pro 등)
  fontSize: ...,      // 크기 차이
  fontWeight: ...,    // 굵기 차이
  letterSpacing: ..., // 장평 차이
  height: ...,        // line-height (Figma px → Flutter ratio 환산 필요)
  color: ...,
)
```

`height` 환산 함정: Figma `line-height: 24px` + `font-size: 16px` → Flutter `height: 1.5` (ratio).

### Custom shapes (CustomPaint)

CustomPainter 의 paint() 메서드 안에서 Path / 색상 직접 조정. SSIM diff 결과를 painter argument 로 전달.

## 한계 + 적용 범위

- **Anti-aliasing 차이는 SSIM 으로 잘 잡힘 (threshold 0.1).** 픽셀 완전 일치 (pixel-perfect) 는 plat 차이로 사실상 불가, 0.95 SSIM 으로 충분.
- **텍스트 hinting 차이는 이미지 비교 한계.** Figma 와 Flutter 의 hinting 알고리즘 차이로 텍스트 영역만 score 깎임 → 텍스트 영역 마스킹 후 SSIM 측정 권장.
- **디바이스 픽셀 비율 (DPR) 정규화 필수.** Figma 1x → Flutter 3x (iPhone) 비교 시 down-sample 후 비교.
- **MCP 미설정 환경에서는 적용 불가.** `mcp_server: null` 인 프로젝트는 Figma/Flutter 캡처 자체가 안 됨 → /insights 에서도 "MCP 디바이스 설정 마찰" 명시.

## 참조

- `/insights` 2026-05-07 fresh report ("5시간 이상을 태운 Flutter–Figma parity") — 본 패턴의 trigger
- `~/.claude/CLAUDE.md` "피그마 구현 워크플로우" — 본 패턴의 prerequisite (Figma MCP 사용 의무)
- `harness/docs/guides/skill-design-guide.md` §3.6 Pre-Edit Batch Audit — 본 패턴 적용 전 audit 단계
- 학술 참고: SSIM (Wang et al., 2004), pixelmatch (kss/pixelmatch GitHub), scikit-image structural_similarity
