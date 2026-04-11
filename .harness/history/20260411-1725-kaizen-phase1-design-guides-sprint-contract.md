# Sprint Contract — Phase 1: 설계 가이드 카이젠

**작성일:** 2026-04-11  
**범위:** `harness/docs/guides/skill-design-guide.md`, `harness/docs/guides/agent-design-guide.md`  
**복잡도:** 낮음 (문서 추가, 코드 변경 없음)

---

## 완료 조건

### SD-01: 트리거 키워드 set intersection 원칙 명시 (skill-design-guide)

**조건:** `skill-design-guide.md` §4 (디스크립션은 트리거 조건이다) 또는 별도 섹션에 아래 내용이 추가되어야 한다.
- "트리거 키워드는 다른 스킬과 set intersection이 공집합이어야 한다" 규칙 문구
- 중복 키워드가 허용될 경우의 예외 처리 방법 (컨텍스트로 구분 가능할 때)
- Bad/Good 예시 또는 명확한 설명

**판정 기준:** `skill-design-guide.md`에서 "set intersection" 또는 "키워드 중복" 관련 문구가 Grep으로 확인될 것.

---

### SD-02: 계약 모호성 방지 원칙 명시 (skill-design-guide)

**조건:** `skill-design-guide.md`에 "설계 문서의 필드/카테고리명은 QA 계약과 1:1 매칭되어야 한다"는 원칙이 추가되어야 한다.
- Gotchas 섹션 또는 별도 섹션 (§3 또는 §3.5 근방) 에 배치
- QA 계약에서 사용할 카테고리 ID/이름을 스킬 본문과 동일하게 유지해야 한다는 규칙

**판정 기준:** `skill-design-guide.md`에서 "계약" 또는 "QA 계약" 또는 "카테고리명" 관련 원칙 문구가 확인될 것.

---

### AD-01: L3 실행 기반 검증 요건 명시 (agent-design-guide)

**조건:** `agent-design-guide.md` §10 Gotchas 섹션 또는 §11 적용 사례에 아래 내용이 추가되어야 한다.
- reviewer/evaluator 에이전트는 "정적 grep 뿐 아니라 실행 결과 검증(Read로 내용 확인, Bash로 명령 실행)까지 포함하여 L3 커버리지를 확보해야 한다"는 요건
- 정적 파일 존재 확인만으로 PASS 처리하는 것이 anti-pattern임을 명시

**판정 기준:** `agent-design-guide.md`에서 "L3" 또는 "실행 결과 검증" 또는 "정적 grep만으로 PASS 금지" 관련 문구가 확인될 것.

---

## 비기능 조건

- **Regression 없음:** `python3 scripts/validate-plugin.py` 결과가 이전 실행과 같거나 개선되어야 함
- **기존 구조 유지:** 섹션 번호, 제목 등 기존 구조를 깨지 않고 추가만 수행
- **창작 금지:** 글로벌 feedback에서 실제로 드러난 이슈만 반영. 추측성 내용 추가 금지
