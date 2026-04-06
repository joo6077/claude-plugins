# 컴포넌트 정의 템플릿

design-component 스킬이 출력하는 컴포넌트 카탈로그의 포맷.

## 컴포넌트 카탈로그 포맷

```markdown
# 컴포넌트 카탈로그

> 생성일: {{date}}
> 프로젝트: {{project-name}}
> 컴포넌트 수: {{count}}

## {{컴포넌트명}}

> 출처 시안 ID: {{mockup-id}} (있는 경우)

### 역할
{{이 컴포넌트의 목적과 사용 맥락}}

### Variants

| Variant | 설명 | 사용 맥락 |
|---------|------|-----------|
| primary | 주요 액션 | CTA, 핵심 동작 |
| secondary | 보조 액션 | 취소, 대안 동작 |
| ghost | 최소 강조 | 텍스트 링크 대체 |

### 상태

| 상태 | 시각적 변화 |
|------|-------------|
| default | 기본 표시 |
| hover | {{변화 설명}} |
| active/pressed | {{변화 설명}} |
| disabled | 투명도 0.38, 인터랙션 불가 |
| loading | {{변화 설명}} (해당 시) |
| focused | 포커스 링 표시 |

### 사이즈

| 사이즈 | 높이 | 패딩 | 폰트 |
|--------|------|------|------|
| sm | {{값}} | {{값}} | {{토큰}} |
| md | {{값}} | {{값}} | {{토큰}} |
| lg | {{값}} | {{값}} | {{토큰}} |

### 토큰 매핑

| 속성 | 토큰 |
|------|------|
| 배경색 (default) | {{토큰명}} |
| 배경색 (hover) | {{토큰명}} |
| 텍스트 컬러 | {{토큰명}} |
| 보더 라디우스 | {{토큰명}} |
| 패딩 | {{토큰명}} |
| 폰트 | {{토큰명}} |

### 사용 가이드라인

- **DO:** {{권장 사용법}}
- **DON'T:** {{금지 사용법}}
```

## 컴포넌트 카테고리별 필수 상태

| 카테고리 | 필수 상태 |
|----------|-----------|
| 버튼 | default, hover, active, disabled, loading, focused |
| 입력 필드 | default, hover, focused, error, disabled, filled |
| 카드 | default, hover (인터랙티브인 경우) |
| 네비게이션 | default, active/selected, hover |
| 토글/스위치 | off, on, disabled |
| 체크박스 | unchecked, checked, indeterminate, disabled |
