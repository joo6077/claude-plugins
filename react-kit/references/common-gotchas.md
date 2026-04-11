# react-kit 공통 Gotchas

react-kit 스킬/에이전트를 작성하거나 개선할 때 반복되는 실수 패턴.
이번 세션(2026-04-10) QA REJECT 사례에서 추출한 원칙이다.

---

## G1. description 트리거 키워드 유일성

**원칙**: 각 스킬의 `description` 트리거 키워드 집합은 다른 스킬 키워드 집합과 교집합이 공집합이어야 한다.

**사례 (SK-05/RE-02)**: `react-wasm` 과 `rust-kit` 의 "wasm-pack 빌드" 키워드 중복 → 어느 스킬이 트리거될지 모호.

**해결**: 키워드에 컨텍스트 단어를 추가해 도메인을 명확히 한다.
- 나쁜 예: `"wasm 추가"`, `"빌드"`
- 좋은 예: `"React 컴포넌트에서 WASM 호출"`, `"Vite 프로젝트 wasm-pack 연동"`

---

## G2. Library Policy 금지 목록 — 추가만, 삭제 금지

**원칙**: 카이젠/개선 시 Library Policy 금지 라이브러리 목록은 **추가만 허용**, 삭제 또는 완화는 빌드 게이트 위반이다.

**사례 (AP-03)**: `react-audit` 의 Library Policy 섹션에서 `react-transition-group` 이 누락된 채 배포 → QA REJECT.

**해결**: 새 스킬이나 에이전트를 작성할 때 Library Policy 문구를 복사하지 말고 아래 3 파일을 **정전 소스**로 참조한다.
- `react-kit/skills/react-animation/SKILL.md` — Gotcha #1
- `react-kit/agents/animation-architect-react.md` — § 금지 라이브러리 목록
- `react-kit/skills/react-audit/SKILL.md` — Library Policy 카테고리

금지 목록 (Phase 10 재확인: 2026-04-11): `motion` / `framer-motion` / `dnd-kit` / `react-spring` / `react-transition-group` / `react-dnd` / `react-beautiful-dnd` / `@formkit/auto-animate` / `gsap` / `lottie-react` / `animate.css`

**확장 사유**: 이 목록은 react-kit 의 라이브러리 0개 애니메이션 원칙에서 파생된다. 새 라이브러리 금지 추가는 자유롭지만, 기존 항목 삭제/완화는 빌드 게이트 성격이 훼손되므로 엄격히 금지된다. 예외 허용은 사용자 명시 요청 + sprint-contract 계약 문구로만 가능하다.

---

## G3. 코드 템플릿 내 placeholder 주석 — 미완성 단어 금지

**원칙**: 스킬 본문의 코드 예제에서 미완성 부분을 나타낼 때 `[미완성 마커]` (to-be-defined, hack, xxx 등) 를 쓰지 않는다. validate-plugin V5 는 이런 계열 단어를 탐지해 FAIL 처리하므로, 코드 템플릿 작성 시 descriptive 주석만 사용한다.

**사례 (DG-01)**: 코드 템플릿에 미완성 마커 주석이 남아 있어 사용자가 복사 후 그대로 사용할 위험.

**해결**: descriptive placeholder 표현을 사용한다.
- 나쁜 예: `// [미완성 마커]: 여기에 로직 추가`
- 좋은 예: `// 비즈니스 로직을 여기에 위치시킨다`, `/* fetch / transform 처리 */`

---

## G4. 원칙 카드 card-source URL 필수

**원칙**: 스킬 본문에 원칙 카드(📌 형식 등)를 작성할 때 `card-source` URL 또는 참조 문서 경로를 반드시 명시한다.

**사례 (CD-03)**: docs-site integration.html 의 원칙 카드에 card-source URL 이 없어 QA REJECT.

**해결**: 원칙 카드 말미에 출처를 명시한다.
```text
card-source: docs/react/kit-design/g1-scaffolding.md §2
```
내부 문서면 파일 경로, 외부 문서면 URL 을 사용한다.

---

## G5. References 섹션 — 그룹 경로가 아닌 개별 파일 명시

**원칙**: 스킬 말미 `## References` 섹션에서 "docs/react/kit-design/ 전체" 같은 그룹 경로 대신 실제 참조 파일을 개별 나열한다.

**사례 (KZ-04)**: References 그룹 경로만 명시 → 어떤 섹션을 봐야 하는지 불명확.

**해결**:
```markdown
## References
- `docs/react/kit-design/g2-state-data.md` §3 — TanStack Query 설계 상세
- `docs/react/wasm-catalog.md` §1 — 권장 WASM 카테고리
```

---

## G6. Gotchas / bad-good 예시 누락

**원칙**: 스킬 Gotchas 항목에는 반드시 bad(나쁜 예) → good(좋은 예) 대조가 있어야 한다. 설명만 있고 예시가 없으면 QA REJECT 대상이다.

**사례 (CD-02)**: integration.html Gotchas 섹션에 bad-good 예시 누락 → REJECT.

**해결**: 각 Gotcha 항목을 아래 구조로 작성한다. 설명 → 나쁜 예(코드 블록) → 좋은 예(코드 블록) 순서로 배치한다.

```text
N. **[제목]**: [설명]

나쁜 예 — [이유]:
<ts 코드 블록: 잘못된 패턴>

좋은 예 — [이유]:
<ts 코드 블록: 올바른 패턴>
```

---

## 사용 가이드

이 파일은 다음 시점에 참조한다:
- 새 react-kit 스킬 작성 시 (harness `create-skill` 전 필독)
- react-kit 카이젠 시 Gotchas 섹션 품질 검증 기준으로
- QA Evaluator 가 react-kit 스킬을 평가할 때 체크리스트로
