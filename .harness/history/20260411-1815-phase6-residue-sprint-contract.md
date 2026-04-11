# Sprint Contract — Phase 6: Design-kit 카이젠

작성일: 2026-04-11
작성자: Kaizen Orchestrator Phase 6 서브에이전트

## 목표

design-kit validate-plugin V6 10건 해소 + data pool §1 design REJECT 3건 반영

## 완료 조건

### V6 — Code Fence (10건 → 0건 목표)
- [ ] CF-01: `python3 scripts/validate-plugin.py design-kit` 결과에서 V6 bare code-fence 0건
- [ ] CF-02: 수정된 파일: design-kit/README.md, design-reviewer.md, design-audit/SKILL.md, design-component/SKILL.md(×2), design-guide/SKILL.md, design-mockup/SKILL.md, design-system/SKILL.md(×2)

### B1 — design-concept Gotcha #3 강화 (concept.md hex 확정값 기재 REJECT 방지)
- [ ] GC-01: Gotcha #3에 "concept.md 컬러 방향 표 예시 행"이 방향 서술형임을 명시적으로 보여주는 Bad/Good 예시가 추가됨
- [ ] GC-02: "방향 서술형만 허용" 규칙이 Step 4 concept.md 템플릿 `## 컬러 방향` 섹션에 명시적 주의 코멘트로 반영됨

### B2 — design-mockup HTML 형식 예외 명시 (False positive 방지)
- [ ] GM-01: design-mockup SKILL.md Gotchas에 "mockup.html은 HTML 형식이 정상이며, .md 계약 패턴(design-tokens.md, audit-report.md)과 구조적으로 다른 HTML 형식은 의도된 산출물"을 명시한 항목 추가
- [ ] GM-02: 추가된 Gotcha는 False positive 패턴(HTML을 .md로 착각)을 방지하는 맥락을 포함함

### B3 — design-system :root CSS 변수 정합성 체크 강화
- [ ] GS-01: design-system SKILL.md Gotchas에 "스킬이 생성하는 HTML 예시의 :root CSS 변수 값이 design-kit 기존 HTML 파일 토큰 값과 일치해야 한다" 규칙 추가
- [ ] GS-02: Step 5 산출물 확인 절차에 ":root CSS 변수 정합성 체크" 항목 추가

## 검증 제약

- validate-plugin.py 실행 후 V6 count 0 확인 필수
- design-concept concept.md 템플릿 내 hex 예시가 없어야 함
- design-mockup Gotcha 번호는 기존 9개에 10번으로 추가 (순서 유지)
- design-system Gotcha 번호는 기존 9개에 10번으로 추가 (순서 유지)
