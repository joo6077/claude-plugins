---
name: perf-kaizen
description: perf-kit 스킬(perf-compare) 품질을 스택 측정 문서의 출처 재대조, 통계 · 벤치마크 방법론 리서치, 실측 사용 기록 기반으로 주기적으로 개선한다. 이 레포 개발용 스킬이며, perf-kit 플러그인에는 포함되지 않는다. onboarding-kaizen / bambu-kaizen 패턴과 동일. "/perf-kaizen", "퍼프 카이젠", "perf-kit 개선", "성능 비교 스킬 개선" 같은 요청 시 트리거. 단순 버그 수정이나 기능 구현 요청에는 트리거하지 않는다.
argument-hint: "[stacks|stats|cost]"
user-invocable: true
---

<!-- markdownlint-disable MD041 -->

perf-kit 의 `/perf-compare` SKILL.md, `references/`(공용 3 종 + `stacks/` 5 종), `scripts/perf_compare.py`, `evals/` 를 주기적으로 개선한다.

<!-- markdownlint-enable MD041 -->

## Gotchas

- **스택 문서의 명령 · 키 이름은 도구 판이 바뀌면 틀린다** — `stacks/*.md` 의 출처 절 URL 을 다시 열어 같은 명령 · 키가 그대로인지 본다. 2026-11-08 첫 대조에서 criterion `estimates.json`(내부 구현) · k6 `dropped_iterations`(원문 없음) · `dumpsys thermalservice` 출력 형식(원문 없음)이 걸렸다. 새 출처를 찾기보다 적힌 출처가 지금도 같은 말을 하는지 보는 것이 먼저다
- **원문에서 확인 못 한 것은 문서에 사실로 남기지 않는다** — 스크립트로 본문을 그리는 페이지(Apple 문서)는 대조에 실패한다. 그 항목은 빼거나 "확인하지 못했다" 고 적는다. 기억으로 채우지 않는다
- **통계 판정을 바꾸면 알려진 답부터 고친다** — `perf_compare.py` 의 판정 · 분위수 · 비용 계산을 바꾸면 `perf-kit/evals/perf-compare/test_perf_compare.py` 의 알려진 답(SciPy 문서 예제 · 손으로 센 순열 수)과 틀린 사본 대조를 먼저 고친다. 손으로 센 값도 틀릴 수 있다 — 2026-11-08 동순위 순열 수를 2/20 으로 잘못 셌고 스크립트가 맞았다(6/20). 기대값은 스크립트와 다른 방법으로 한 번 더 센다
- **스택 문서는 같은 절 순서를 지킨다** — 감지 → 함정 → 지표별 경로 → 명령 → 출처. 새 스택을 더하면 `SKILL.md` 1 단계 감지 표에도 한 줄을 더한다. 스택 킷에 어댑터 스킬을 따로 만들지 않는다 — 원칙이 키트마다 복사되면 어긋난다

## 트리거

- kaizen-orchestrator Phase 18
- 수동 호출: `/perf-kaizen` (전체) · `/perf-kaizen stacks` · `/perf-kaizen stats` · `/perf-kaizen cost`
- 이벤트: perf-compare 사용 중 스택 문서 명령이 실제 출력과 달랐다는 보고

## Process

### Phase 1: 데이터 수집

1. **스택 문서 출처 재대조** — `perf-kit/skills/perf-compare/references/stacks/*.md` 의 출처 절 URL 을 WebFetch 로 다시 열어 명령 · 옵션 · 출력 키가 그대로인지 본다
2. **방법론 리서치** — `references/research-sources.md` 의 방법론 출처(RMIT · Duet · 정상 상태 · Mann-Whitney)와 같은 주제의 새 논문 · 공식 문서
3. **실측 사용 기록** — 각 프로젝트 `.mcp_screenshots/test-evidence/*/perf.json` · `perf-evidence/*/perf.json` 에서 `주의:` · `표본 부족` · `무효` 가 반복된 패턴
4. `python3 scripts/validate-plugin.py perf-kit` 현재 상태

### Phase 2: 개선 후보 도출

- 스택 문서의 틀린 명령 · 키 이름 정정 (사실 정정 — unit 계수에서 뺀다)
- 새 스택 문서 필요성 (반복 요청된 스택이 감지 표의 "해당 없음" 으로 빠졌는가)
- 스크립트 판정 규칙 · 주의 규칙 추가 (출처가 있는 방법론만)
- evals 추가

한 사이클의 새 개선은 3 unit 이하로 한다.

### Phase 3: Sprint Contract 작성 + 구현

`harness/skills/sprint-contract` 로 완료 조건을 정의한 뒤 구현한다.

### Phase 4: QA Evaluator + 검증

- `harness/agents/qa-evaluator` 로 APPROVE/REJECT 판정
- `python3 -m unittest discover -s perf-kit/evals/perf-compare -v` 통과, 바꾼 계산마다 틀린 사본 하나가 실패하는지 확인
- `python3 scripts/validate-plugin.py perf-kit` — 등록된 검사 전부. 실행 출력을 인용하지 않은 "검증 통과" 보고는 증거가 아니다

실행 패턴, 우선순위 매핑, 통합 규칙은 `harness/docs/guides/plugin-validation-guide.md §7` 이 정의한다 (SSOT). 등급 근거는 `harness/docs/guides/skill-design-guide.md` §3.7.

### Phase 5: 기록 + 릴리스

- `docs/kaizen/research-log.md` 에 조회한 출처 · 채택 · 폐기를 남긴다
- 개선이 의미 있으면 `bash scripts/release.sh perf-kit patch`

## References

- `references/research-sources.md` — 출처 목록과 조회 이유
- `harness/docs/guides/plugin-validation-guide.md` — 플러그인 품질 검사 정의 기준 (SSOT)
- `harness/docs/guides/skill-design-guide.md` — §3.7 Completion Evidence Gate · 알려진 답 대조 · 검사를 만드는 스킬
- `scripts/validate-plugin.py` — 플러그인 검증 자동화 도구
