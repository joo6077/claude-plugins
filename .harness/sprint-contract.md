---
feature: "Phase 3: visual-styles 35종 퀄리티 리워크"
created: "2026-04-09 18:30"
complexity: "높음"
conditions: 12
---

## Skill
- [ ] SK-01: Given Neumorphism 카드를 확인할 때, Then 듀얼 방향 box-shadow(밝은쪽+어두운쪽)가 적용되어 있다
- [ ] SK-02: Given Neubrutalism 모달을 열었을 때, Then 모든 box-shadow가 blur:0이고 hard offset(4px+ 이상)이다
- [ ] SK-03: Given Neon Glow 모달을 열었을 때, Then box-shadow가 최소 3겹(다른 blur 값)으로 적용되어 있다
- [ ] SK-04: Given Dark Mode 카드를 확인할 때, Then 배경이 #000이 아닌 #121212 계열이고 텍스트가 #fff가 아닌 #e0e0e0 계열이다
- [ ] SK-05: Given Minimalism 카드를 확인할 때, Then padding이 30px 이상이고 font-weight가 300 이하이다
- [ ] SK-06: Given Metallic/Chrome 카드를 확인할 때, Then linear-gradient stop이 4개 이상이다

## Architecture
- [ ] AR-01: visual-styles.html이 브라우저에서 에러 없이 로드된다 (JS 런타임 에러 0개, CSP 제외)
- [ ] AR-02: 35종 카드 데모가 모두 렌더링된다 (style-card 요소 35개)
- [ ] AR-03: 다크/라이트 모드 토글이 정상 동작한다
- [ ] AR-04: 모바일(600px 이하)에서 1컬럼 그리드로 정상 표시된다

## Error
- [ ] ER-01: 라이트 모드에서 모달을 열어도 컴포넌트 스타일이 깨지지 않는다

## Anti-patterns
- [ ] AP-01: hardcoded version 없음
