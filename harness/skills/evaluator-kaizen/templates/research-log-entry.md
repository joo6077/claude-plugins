# 연구 로그 엔트리 템플릿

> SKILL.md에서 research-log.md에 evaluator-kaizen 엔트리 추가 시 이 형식을 따른다.

## 형식

~~~markdown
## YYYY-MM-DD (evaluator-kaizen)

**트리거:** orchestrator-phase-3 / feedback-threshold (사유) / manual (영역)
**피드백 분석:** {분석된 피드백 건수}건, 주요 패턴: {패턴 요약}

### 조사한 소스

| # | 제목 | URL | 유형 | 신뢰도 | 결과 |
|---|------|-----|------|--------|------|
| 1 | Title | URL | peer-reviewed/공식/blog/community | 높음/중간/낮음 | 채택/폐기 |

### 채택한 인사이트

- **인사이트 1:** {Description} — 적용 영역: guide/skills

### 폐기 사유 (해당 시)

- **소스 N:** {Reason}

### 개선 적용

- 대상: {파일 경로}
- 변경: {요약}
- 버전: vX.Y.Z → vX.Y.Z

### PR

- PR URL 또는 "개선 포인트 없음"
~~~
