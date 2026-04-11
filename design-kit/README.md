# design-kit

스택 무관 UI/UX 디자인 플러그인. 디자인 시스템 세팅, 실시간 가이드, 디자인 감사를 제공한다.

버전: `0.1.0`

## 스킬

<!-- AUTO:skills -->
| 스킬 | 설명 |
|------|------|
| `design-audit` | 완성된 UI를 디자인 원칙 기준으로 체계적으로 감사한다. |
| `design-component` | 반복되는 UI 요소를 컴포넌트로 정의하고 카탈로그화한다. |
| `design-concept` | 프로젝트의 디자인 방향성(무드, 컬러 방향, 타이포 방향, UI 패턴)을 정의하고 |
| `design-guide` | 개발 중 UI 코드/설명을 받아 관련 디자인 원칙을 참조하여 가이드한다. |
| `design-mockup` | 특정 화면 요청 시 하이파이 HTML 시안 5개를 생성하여 제시한다. |
| `design-reference` | 디자인 컨셉에 맞는 실제 프로덕트/서비스의 시각 디자인을 체계적으로 크롤링하고 |
| `design-system` | 프로젝트에 디자인 토큰 체계(컬러, 타이포, 스페이싱, 라디우스 등)를 세팅한다. |
<!-- /AUTO:skills -->

## 에이전트

<!-- AUTO:agents -->
| 에이전트 | 설명 |
|----------|------|
| `design-reviewer` | UI 코드를 디자인 원칙 기준으로 독립 평가한다. |
<!-- /AUTO:agents -->

## 훅

<!-- AUTO:hooks -->
| 이벤트 | 실행 | 설명 |
|--------|------|------|
| `SessionStart` | `env-check.sh` | SessionStart |
<!-- /AUTO:hooks -->

## 스크립트

<!-- AUTO:scripts -->
| 스크립트 | 설명 |
|----------|------|
| `env-check.sh` |  |
<!-- /AUTO:scripts -->

## Evals

<!-- AUTO:evals -->
| 파일 | 설명 |
|------|------|
| `evals.json` | 파일 |
| `visuals.spec.js` | 파일 |
<!-- /AUTO:evals -->

## 사용 흐름

```text
1. /design-system     → 프로젝트 디자인 토큰 세팅
2. (개발 중) /design-guide  → 실시간 디자인 조언
3. (개발 후) /design-audit  → 디자인 품질 감사
```

## 원칙

- **스택 무관** — 디자인 원칙만 다루고, 구체적 코드 생성은 각 toolkit에 위임
- **플러그인 간 의존성 없음** — 다른 플러그인과 독립적으로 동작
- **출처 기반** — 모든 가이드/판정에 출처 명시 (Apple HIG, Material Design, WCAG 등)

## 설치

```bash
claude plugin add github:joo6077/claude-plugins/design-kit
```
