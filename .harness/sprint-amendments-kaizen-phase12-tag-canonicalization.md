---
slug: kaizen-phase12-tag-canonicalization
contract: .harness/sprint-contract-kaizen-phase12-tag-canonicalization.md
created: "2026-08-13 15:35"
---

## AM-01 — clarification (측정문 결함 신고 · 조건 문구 변경 없음)

**대상**: SC-04 의 음성 대조 절
**원문**: "음성 대조: `alias`/`verb-synonym` 행을 제거한 맵으로 실행하면 두 값이 같아져야 한다"

**실행 결과 (2026-08-13, `~/.claude/logs/*/reflections-*.md` 전량)**

| 맵 상태 | `skipped-required-api-doc-check` 클러스터 | 원시 단독 |
| --- | --- | --- |
| 전체 맵 | **110** | 71 |
| `alias` + `verb-synonym` 제거 | **72** | 71 |
| 맵 없음 (순수 kebab) | **71** | 71 |

**판정**: 원 측정문의 등가 기대(`72 == 71`)는 **문자 그대로 충족되지 않는다.** 차이 1 건의 출처를
추적한 결과 `skipped-required-api-docs-check`(복수형 `docs`) 1 건이었고, 이는 제거하지 않은
**세 번째 행 종류 `synonym`(`docs → doc`)** 이 접은 것이다. 즉 측정문이 "정규화에 기여하는 행
종류" 를 2 종으로 가정했으나 실제로는 3 종이다 — **측정문 쪽의 결함**이다.

**증명하려던 명제는 유지된다**: `alias`/`verb-synonym` 행이 load-bearing 인가 → 110 → 72 로
**38 건이 사라진다.** 완전 제거(맵 없음) 시에는 `71 == 71` 로 정확히 등가가 성립한다.

**조치**: 계약 본문은 고치지 않는다 (write-once). SC-04 는 **주 측정(110 > 71) PASS · 음성 대조는
문자 그대로는 미충족이나 대체 실행 2 건으로 명제 성립 확인** 으로 보고한다. 다음 사이클에 이
조건을 재사용한다면 음성 대조를 "맵 전체를 제거하면 두 값이 같아져야 한다" 로 써야 한다.

**consent**: 사용자 앵커 없음 (백그라운드 서브에이전트 실행). direction 은 **narrowing 아님 ·
widening 아님** — 조건 집합·경로 집합 변화 0. 측정 해석 기록일 뿐이다.

## AM-02 — 환경 사고 기록 (계약 조건 무관 · 재현 정보 보존용)

스프린트 도중 다른 병렬 세션이 `git stash` + `git reset` 계열 명령을 실행해 이 Phase 의
미커밋 변경(추적 4 파일 + 미추적 3 파일)이 워킹트리에서 사라졌다. `stash@{0}` 에서 **본 Phase
경로만** 골라 복원했다 (`git show stash@{0}:<path>` / `git show stash@{0}^3:<path>`).

같은 stash 에는 본 Phase 소유가 아닌 파일 2 개가 함께 들어 있다 —
`.harness/sprint-contract-kaizen-phase10-react-currency.md`,
`.harness/sprint-feedback-kaizen-phase10-react-currency.md`. **복원하지 않았다** (Scope 밖).
Phase 10 담당이 `git show 'stash@{0}:<path>'` 로 회수할 수 있다.
