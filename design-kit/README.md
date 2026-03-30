# design-kit

스택 무관 UI/UX 디자인 플러그인. 디자인 시스템 세팅, 실시간 가이드, 디자인 감사를 제공한다.

## 스킬

| 스킬 | 아키타입 | 설명 |
|------|----------|------|
| `/design-system` | Code Scaffolding | 프로젝트에 디자인 토큰 체계 세팅 |
| `/design-guide` | Library Reference | 개발 중 디자인 원칙 기반 실시간 가이드 |
| `/design-audit` | Product Verification | 완성된 UI를 디자인 원칙 기준으로 감사 |

## 에이전트

| 에이전트 | 모델 | 설명 |
|----------|------|------|
| `design-reviewer` | sonnet | design-audit이 호출하는 독립 디자인 평가 에이전트 |

## 사용 흐름

```
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
