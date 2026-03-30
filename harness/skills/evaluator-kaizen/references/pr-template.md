# Evaluator Kaizen PR 본문 템플릿

> SKILL.md에서 PR 생성 시 이 템플릿을 따른다.

## PR 본문 템플릿

~~~markdown
## Research Summary
> {One-line summary of contract design improvement}

### 조사한 소스
- [Title](URL) `[Type]` — {Brief summary}

### 핵심 발견
- Finding: {Specific description + citation}

---

## Changes

### 1. [Change Name]

**영역:** guide / skills
**버전 영향:** patch / minor / major

**Before:**
```
{현재 코드/설정}
```

**After:**
```
{변경된 코드/설정}
```

**왜 개선인가:**
- 장점: ...
- 단점/트레이드오프: ...
- 근거: [출처](URL)

---

## Impact Summary

| 항목 | 영향도 | 리스크 | 근거 |
|------|--------|--------|------|

---

## Version Bump

**유형:** patch / minor / major
**현재:** vX.Y.Z → **다음:** vX.Y.Z
**판단 근거:** ...

---

## Source Reliability

| 출처 | 유형 | 신뢰도 | 최신성 |
|------|------|--------|--------|
~~~

## changelog.md 엔트리 형식

~~~markdown
## [X.Y.Z] - YYYY-MM-DD

### 변경 유형: patch/minor/major (evaluator-kaizen)

### 연구 기반
- [제목](URL) — {Insight}

### 변경 내역
- **파일경로**: {Description}
  - Before: {Old}
  - After: {New}
  - 근거: [출처](URL)

### 버전 판단 근거
> {Why this bump type}
~~~
