---
feature: "설정 페이지 테마 선택"
created: "2026-01-01 00:00"
complexity: "단순"
conditions: 5
slug: "qaa-b"
---

## UI
- [ ] UI-01: 설정 페이지에 테마 선택 행이 표시된다

## Logic
- [ ] LG-01: 테마 변경 시 Provider 상태가 업데이트된다

## Error
- [ ] ER-00: N/A

## Architecture
- [ ] AR-01: 설정 페이지는 shared/settings/presentation/에 위치한다

## Anti-patterns
- [ ] AP-01: StatefulWidget / ConsumerStatefulWidget 사용하지 않는다

## Reusability
- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics
- [ ] DG-01: flutter analyze 워닝 0개
