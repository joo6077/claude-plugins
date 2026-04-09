# Responsive Web Design

design-kit HTML 산출물 템플릿에 적용할 반응형 패턴.

## 브레이크포인트

모바일 퍼스트, `min-width` 방향. 3단계로 충분.

| 이름 | 값 | 대상 |
|------|----|------|
| base | 0 ~ 639px | 모바일 (기본) |
| tablet | 640px | 태블릿 |
| desktop | 1024px | 데스크톱 |
| wide | 1536px | 와이드 모니터 |

```css
@media (min-width: 640px)  { /* tablet */ }
@media (min-width: 1024px) { /* desktop */ }
@media (min-width: 1536px) { /* wide */ }
```

Tailwind v4: 640/768/1024/1280/1536. Bootstrap 5: 576/768/992/1200/1400.

## CSS-only 반응형 패턴

### Grid auto-fill + minmax

브레이크포인트 없이 카드 그리드 자동 조절:

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: clamp(12px, 2vw, 24px);
}
```

- `auto-fill`: 빈 트랙 유지 (예측 가능)
- `auto-fit`: 빈 트랙 접음 (요소 적을 때 늘어남)

### clamp() 유체 타이포그래피/스페이싱

```css
:root {
  --text-base: clamp(14px, 1.5vw, 18px);
  --text-lg:   clamp(18px, 2.5vw, 28px);
  --text-xl:   clamp(24px, 4vw, 48px);
  --space-md:  clamp(16px, 3vw, 32px);
}
```

### 컨테이너 쿼리

뷰포트가 아닌 부모 컨테이너 기준. 2025 기준 전 주요 브라우저 지원 (Chrome 105+, Safari 16+, Firefox 110+).

```css
.card-wrapper { container-type: inline-size; }
@container (min-width: 400px) {
  .card { flex-direction: row; }
}
```

## 레이아웃 패턴

### 사이드바 + 콘텐츠

```css
.layout { display: grid; grid-template-columns: 1fr; }
@media (min-width: 1024px) {
  .layout { grid-template-columns: 260px 1fr; }
}
```

### 풀블리드 히어로

```css
.page { display: grid; grid-template-columns: 1fr min(65ch, 100%) 1fr; }
.full-bleed { grid-column: 1 / -1; }
.content { grid-column: 2; }
```

## base.html 적용 방향

1. 브레이크포인트: 640/1024/1536px CSS 변수 정의
2. 타이포/스페이싱: `clamp()` 유체 스케일
3. 카드/그리드: `auto-fill + minmax()` (미디어쿼리 불필요)
4. 레이아웃 전환: `min-width` 미디어쿼리
5. 접근법: 모바일 퍼스트

## Sources

- Tailwind CSS v4 Responsive Design
- Bootstrap 5 Breakpoints
- CSS Container Queries — MDN
- CSS-Tricks: auto-fill vs auto-fit
