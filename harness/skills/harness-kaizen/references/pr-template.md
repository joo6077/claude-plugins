# Kaizen PR 본문 템플릿

> SKILL.md에서 PR 생성 시 이 템플릿을 따른다.

## PR 본문 템플릿

~~~markdown
## Research Summary
> 이번 주 연구에서 발견한 핵심 인사이트 정리

### 조사한 소스
- [제목](URL) `[유형]` — 핵심 요약 1-2줄
- [제목](URL) `[유형]` — 핵심 요약 1-2줄

### 핵심 발견
- 발견 1: 구체적 설명 + 출처 인용
- 발견 2: 구체적 설명 + 출처 인용

---

## Changes

### 1. [개선 항목명]

**영역:** config / skill-prompt / agent-logic / eval / architecture / design-guide
**버전 영향:** patch / minor / major

**Before:**
```
현재 코드 또는 설정 (실제 스니펫)
```

**After:**
```
변경된 코드 또는 설정 (실제 스니펫)
```

**왜 개선인가:**
- 장점: ...
- 단점/트레이드오프: ...
- 근거: [출처](URL)의 Section X에서 "인용문..."

---

## Impact Summary

| 항목 | 영향도 | 리스크 | 근거 |
|------|--------|--------|------|
| 변경1 | 높음/중간/낮음 | 높음/중간/낮음 | [출처](URL) |

---

## Version Bump

**유형:** patch / minor / major
**현재:** vX.Y.Z → **다음:** vX.Y.Z
**판단 근거:** (왜 이 bump 유형인지 1줄 설명)

---

## Source Reliability

| 출처 | 유형 | 신뢰도 | 최신성 |
|------|------|--------|--------|
| 논문 A | peer-reviewed | 높음 | 2026-02 |
| Blog B | 공식 | 높음 | 2026-03 |
| Blog C | 커뮤니티 | 중간 | 2025-11 `[dated]` |
~~~

## changelog.md 엔트리 형식

~~~markdown
## [X.Y.Z] - YYYY-MM-DD

### 변경 유형: patch/minor/major (영역)

### 연구 기반
- [제목](URL) — 핵심 인사이트 1줄

### 변경 내역
- **파일경로**: 변경 설명
  - Before: 이전 동작/값
  - After: 변경 후 동작/값
  - 근거: [출처](URL)

### 버전 판단 근거
> bump 유형 선택 이유 1줄
~~~
