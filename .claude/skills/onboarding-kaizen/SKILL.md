---
name: onboarding-kaizen
description: onboarding-kit 스킬(setup-guide) 품질을 외부 docs/help 페이지 변경, 사용자 피드백 메모리, marketplace 트렌드 기반으로 주기적으로 개선한다. 이 레포 개발용 스킬이며, onboarding-kit 플러그인에는 포함되지 않는다. bambu-kaizen / rust-kaizen / flutter-kaizen 패턴과 동일. "/onboarding-kaizen", "온보딩 카이젠", "onboarding-kit 개선", "셋업 가이드 스킬 개선" 같은 요청 시 트리거. 단순 버그 수정이나 기능 구현 요청에는 트리거하지 않는다.
argument-hint: ""
user-invocable: true
---

onboarding-kit의 `/setup-guide` SKILL.md, references/ 3종, evals/evals.json을 주기적으로 개선한다.

## 트리거

- 주 1회 cron 자동 실행 (kaizen-orchestrator Phase 14)
- 수동 호출: `/onboarding-kaizen`
- 이벤트: `feedback_setup_guide_*` 메모리가 3개 이상 누적되면 자동 트리거 후보
- 이벤트: setup-guide 호출 결과의 사용자 부정 피드백 누적

## Process

### Phase 1: 데이터 수집

1. **사용자 피드백 메모리 스캔** — `~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_setup_guide_*.md`
2. **외부 출처 변경 확인** — `references/research-sources.md`의 출처 목록을 WebFetch / Codex로 최신화 확인
3. **marketplace 트렌드** — claude-plugins 마켓플레이스에 새 onboarding/setup 관련 플러그인 등장 여부

### Phase 2: 개선 후보 도출

- SKILL.md Gotchas에 추가할 새 패턴 (메모리 기반)
- references/ 3종에 추가/수정할 항목
- evals/evals.json에 추가할 시나리오

### Phase 3: Sprint Contract 작성 + 구현

`harness/skills/sprint-contract`로 완료 조건 정의 후 구현. 단순 텍스트 수정에서 큰 구조 변경까지 모두 contract 기반.

### Phase 4: QA Evaluator + Plugin Validation

`harness/agents/qa-evaluator`로 APPROVE/REJECT 판정. REJECT 시 수정 후 재평가.

**validate-plugin.py 실행 없이 완료 선언 금지** — 카이젠 세션 시작/종료 시 `python3 scripts/validate-plugin.py onboarding-kit` 을 실행한다. **8 카테고리 (V1~V8: frontmatter / templates / refs / triggers / placeholders / code-fence / plugin-json / hook-exec)** 중 하나라도 FAIL 이면 수정 후 재검증한다. 실행 출력을 인용하지 않은 "검증 통과" 보고는 증거가 아니다.

실행 패턴, 우선순위 매핑, 통합 규칙은 `harness/docs/guides/plugin-validation-guide.md §7` 이 정의한다 (SSOT) — 해당 섹션을 그대로 따른다. 등급 근거는 `harness/docs/guides/skill-design-guide.md` §3.7 Completion Evidence Gate (E1/E2/E3 SSOT).

### Phase 5: 커밋 + 릴리스

개선이 의미 있으면 onboarding-kit 버전 bump + marketplace.json 갱신 (`/release onboarding-kit patch`).

## References

- `references/research-sources.md` — 외부 출처 목록 + 폴링 빈도
- `harness/docs/guides/plugin-validation-guide.md` — 플러그인 품질 8 카테고리 (V1~V8) 기준 (SSOT)
- `scripts/validate-plugin.py` — 플러그인 검증 자동화 도구
- `harness/docs/guides/skill-design-guide.md` — §3.7 Completion Evidence Gate · Enforcement 등급 E1/E2/E3 (SSOT)
- `harness/docs/guides/qa-evaluation-guide.md` — §Canonical Unverified-Evidence Protocol (`[미검증]` 마커 · 임계 2 정본)
