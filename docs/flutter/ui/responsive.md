---
title: 반응형 레이아웃
version: 0.1.0
last_updated: 2026-04-05
---

# 반응형 레이아웃

MediaQuery와 LayoutBuilder 선택, breakpoint, SafeArea, NavigationRail vs BottomNavigationBar를 다룬다.

## 원칙

1. **Responsive와 Adaptive는 다르다.** Responsive는 주어진 공간에 맞춰 레이아웃을 늘리고 줄이는 것, Adaptive는 그 공간에서 usable한 UI 패턴을 선택하는 것이다.
   - 출처: https://docs.flutter.dev/ui/adaptive-responsive
2. **창 전체 크기는 `MediaQuery.sizeOf(context)`, 지역 레이아웃은 `LayoutBuilder`를 쓴다.** LayoutBuilder는 부모 constraints 기준이라 중첩 컨테이너에 정확하다.
   - 출처: https://docs.flutter.dev/ui/adaptive-responsive/general
3. **디바이스 종류가 아니라 window size로 브랜치한다.** "폰이냐 태블릿이냐"가 아니라 "현재 width class가 무엇이냐"로 결정하라.
   - 출처: https://docs.flutter.dev/ui/adaptive-responsive/general
4. **작은 창에는 BottomNavigationBar, 넓은 창에는 NavigationRail을 쓴다.** 내비게이션 패턴 자체를 width class에 따라 교체하는 것이 adaptive의 핵심.
   - 출처: https://docs.flutter.dev/ui/adaptive-responsive/general
5. **SafeArea와 system UI inset을 항상 고려한다.** 노치·상태바·제스처 영역을 무시하면 기기마다 레이아웃이 어긋난다.
   - 출처: https://docs.flutter.dev/ui/adaptive-responsive

## 수치·경계값

- 600dp 미만: BottomNavigationBar, 600dp 이상: NavigationRail.
- Material width size class: Compact 0–599dp, Medium 600–839dp, Expanded 840dp+.
- breakpoint는 물리 inch가 아니라 logical pixel(dp)로 판단한다.

## 안티패턴

- `Platform.isAndroid`/`Platform.isIOS`로 레이아웃을 분기 — OS가 아니라 창 크기 문제다.
- 기기명(iPhone 15 Pro 등) 하드코딩 — foldable, desktop resize에서 즉시 깨진다.
- `MediaQuery.of(context)`를 전역 남발 — 필요 없는 속성 변화에도 전부 rebuild된다.
- portrait lock으로 responsive 이슈를 숨기기 — 태블릿/폴더블/데스크톱 사용자 경험이 망가진다.

## Gotchas

- "폰/태블릿만" 분기하는 코드는 foldable의 접힘 상태 변화와 desktop window resize에서 반드시 깨진다 — width class 기반으로 작성하라.
- `MediaQuery.of(context)` 전체 대신 `MediaQuery.sizeOf(context)`, `MediaQuery.paddingOf(context)` 등 필요한 속성만 읽으면 rebuild 범위가 크게 줄어든다 (Flutter 3.10+).
