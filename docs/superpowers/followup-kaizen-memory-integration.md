# Followup — 카이젠 ↔ 메모리 양방향 연동 + 훅 승격

작성: 2026-08-14 (kaizen-2026-08-13 사이클 중 사용자 지시)
상태: 미착수 — F4 이후 별도 스프린트로 처리하기로 합의

## 문제

카이젠 오케스트레이션이 **메모리를 읽지도 쓰지도 않는다.**

- 읽기 부재: `scripts/collect-kaizen-data.py` 의 데이터 풀은 §0(`/insights`) · §1(글로벌 evaluator
  피드백) · §2(외부 프로젝트) · §3(followup) · §4(최근 계약) · §5(validate-plugin) · §6(참조 가이드)
  로 구성된다. `~/.claude/projects/*/memory/` 는 **한 번도 참조되지 않는다**
  (`grep -c memory .claude/skills/kaizen-orchestrator/SKILL.md` → 0).
- 쓰기 부재: 사이클이 발견한 교훈이 계약 본문·감사 로그에만 남고 메모리로 승격되지 않는다.
  다음 사이클의 나는 같은 실수를 반복한다.

## 왜 지금 문제인가 — 실측 근거

`feedback_oracle_must_execute_not_grep` 는 **2026-07-28** 에 기록됐다. 내용은
*"계약 조건의 측정 oracle 을 '문서에 서술이 존재하는가' 로 쓰면 문언상 전부 PASS 인데 기능이
깨진 상태를 통과시킨다"* 이고, 25 조건 전부 PASS 인데 기능이 파손된 사례에서 나왔다.

**kaizen-2026-08-13 사이클의 재평가 REJECT 3 건이 정확히 그 유형이었다:**

| Phase | 결함 | 성격 |
| --- | --- | --- |
| 6 | AR-03 이 "같은 문단에 도구 4 종 열거"를 요구했으나 대상 문단은 역참조만 씀 | 측정문 |
| 13 | AP-03 clause 2 `grep -c '^+```$'` 가 **닫는** fence 를 셈 → 구조적 충족 불가 | 측정문 |
| 12a | SC-04 음성 대조가 맵 4 kind 중 2 종만 제거 → 등식 불성립 | 측정문 |

2 주 반 전에 이미 알고 있던 결함 유형이 계약 작성 단계에 전달되지 않았다.
메모리가 데이터 풀에 들어갔다면 Phase 2(contract) 가 이것을 먹었을 것이다.

## 범위 (사용자 결정)

- **읽기**: `~/.claude/projects/*/memory/` **전 프로젝트 교차** 수집.
  현재 레포 memory 를 최우선으로, 타 프로젝트는 교차 신호로. 스택 무관 `feedback` 타입만 필터링.
  데이터 풀 §0.5 (§0 다음, 모든 Phase 가 참조)로 삽입.
- **쓰기**: 사이클이 발견한 교훈을 메모리 엔트리로 승격하는 경로. 승격 기준·중복 판정·
  `MEMORY.md` 인덱스 갱신까지 포함. reflect-kit `/reflect-promote` 와 역할이 겹치는지 먼저 확인할 것.

## 훅 승격 후보 — 냉정하게 선별

메모리 `feedback` 12 건 중 기계화가 실제로 되는 것만:

| 메모리 | 적합 표면 | 비고 |
| --- | --- | --- |
| `no_dirwide_autofixer` | PreToolUse Bash 훅 | 포매터/린트픽서에 디렉토리 인자 감지 → 차단 |
| `oracle_must_execute_not_grep` | **훅 아님 — 계약 린터** | `.harness/sprint-contract-*.md` 저장 시 측정문이 서술확인 grep 만 쓰면 경고 |
| `codex_foreground_call_direct` | 훅 존재 (`enforce-foreground-research.sh`) | **오탐 개선 필요** — 아래 참조 |
| 나머지 9 건 | 규칙·가이드 | 훅 부적합 |

`feedback_codex_orthodox_hook_not_empire` 가 *"자동화는 훅이, 의식은 규칙 슬림화로. 카이젠 제국
금지"* 라고 못박고 있다. 후보를 늘리지 마라.

### `enforce-foreground-research.sh` 오탐 (실측)

`:51` 의 패턴이 `조사` 를 포함한다. 이 때문에 리서치와 무관한 프롬프트
(예: "커밋 origin **조사**", "research-log 갱신")까지 deny 된다.
kaizen-2026-08-13 세션에서 실제로 걸려 프롬프트 어휘를 우회해야 했다.
→ 어휘 기반 차단을 좁히거나, 도구·인자 기반 판정으로 교체할 것.

## 검증 방식 (이번 사이클에서 확립된 것을 그대로 적용)

훅·린터마다 **양성 · 음성 · 오탐** 3 축을 실행으로 확인한다. 서술 존재로 대체하지 마라.

이번 사이클 실례 — Phase 13 AP-03 새 측정문:

```text
양성  실제 커밋 04641f7          → 4 파일 전부 0, exit 0
음성  bare 여는 fence 도입 커밋   → INCREASED 검출, exit 1
오탐  fence 무관 텍스트만 수정    → 증가 0, exit 0
```

중간안(diff 기반 상태추적)은 **오탐 축에서 걸려** 파일 상태 기반으로 다시 고쳤다.
3 축 중 하나라도 빠지면 이 결함을 못 잡았다.

## 함께 처리할 것

- **봉인 커버리지 갭** — 봉인(`conditions_digest`)이 조건 체크박스 줄만 해시하고 들여쓴
  **측정문을 덮지 않는다.** Phase 13 계약을 61 줄 고쳤는데 `SEAL_OK` 가 유지됐다.
  조건의 판정력은 대부분 측정문에 있으므로 실질적 갭이다. 다음 사이클 Phase 2 소관.
- **harness 폐기 페이지 4 종 정리** — `docs/harness/{skill-design,agent-design,contract-design,
  qa-evaluation}.html` 은 2026-04-24 `7e3b69e` 가 nav 를 `-guide.html` 로 옮기며 대체한 폐기본이다.
  파일만 남아 도달 경로가 없는데 사이클마다 비용이 든다 (`4a71207` SK-02 수정 · 2026-08-14 재생성).
  삭제 검토.
