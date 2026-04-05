---
title: 위젯 컴포지션
version: 0.1.0
last_updated: 2026-04-05
---

# 위젯 컴포지션

Stateless/Stateful/HookWidget 선택, 작은 위젯 분해, const, Key, rebuild 최소화를 다룬다.

## 원칙

1. **위젯 타입 선택 기준은 "상태 소유권과 lifecycle 필요성"이다.** 내부 상태가 없으면 Stateless, 위젯 lifecycle에 묶인 상태가 있으면 Stateful, hooks로 lifecycle을 분해 재사용하고 싶으면 HookWidget.
   - 출처: https://docs.flutter.dev/ui
2. **Flutter는 aggressive composition 최적화가 전제다.** 작은 위젯으로 분해하는 것이 기본적으로 성능에 유리하다 — 큰 build 메서드보다 쪼개진 서브 위젯이 rebuild 경계를 좁힌다.
   - 출처: https://docs.flutter.dev/resources/inside-flutter
3. **const 생성자를 적극 사용해 동일 위젯 인스턴스를 재사용한다.** const 위젯은 element tree에서 canonical하게 공유되어 rebuild 비용이 0에 수렴한다.
   - 출처: https://docs.flutter.dev/perf/best-practices
4. **Key는 같은 타입 반복 children의 semantic identity를 보존한다.** 리스트 재정렬·삽입·삭제 시 state 보존 여부를 결정한다.
   - 출처: https://api.flutter.dev/flutter/foundation/Key-class.html
5. **Rebuild 최소화는 setState 범위 축소 + child hoisting + select/selector 조합으로 달성한다.** const로 상수화할 수 없는 child는 부모 밖으로 끌어올려 참조 공유로 재사용한다.
   - 출처: https://docs.flutter.dev/perf/best-practices

## 수치·경계값

- 일반 child에는 명시적 key가 필요 없다 — 타입과 위치로 충분히 식별된다.
- Key는 sibling 범위에서만 유일하면 된다. 트리 전역 유일성은 요구되지 않는다.
- GlobalKey는 전역에서 유일해야 하며, 매 build마다 재생성하면 안 된다 (보통 State 필드로 보관).

## 안티패턴

- 500줄짜리 단일 build 메서드 — 분해하지 않으면 rebuild 경계가 전체가 된다.
- 리스트 아이템에 index 기반 key — reorder 시 identity가 무너져 state가 잘못 매핑된다.
- 모든 위젯에 GlobalKey를 다는 습관 — 메모리·lifecycle 비용이 커지고 hot reload 이슈가 늘어난다.
- rebuild 원인을 모르는 채 const만 붙이는 습관 — 부모가 rebuild되면 const child는 이미 재사용되므로 이득이 없다.

## Gotchas

- reorder 가능한 리스트에서 `findChildIndexCallback`을 지정하지 않으면 key가 있어도 상태가 손실될 수 있다 — `SliverChildBuilderDelegate`의 옵션을 확인하라.
- StatefulWidget을 HookWidget으로 바꿔도 상태의 본질적 복잡도는 줄지 않는다 — 단지 재사용 축이 lifecycle에서 hook으로 옮겨갈 뿐이다. 상태가 복잡하면 먼저 책임 분리부터 검토하라.
