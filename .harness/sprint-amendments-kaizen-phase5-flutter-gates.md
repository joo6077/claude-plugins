# Sprint Amendments — kaizen-phase5-flutter-gates

계약 본문(`.harness/sprint-contract-kaizen-phase5-flutter-gates.md`)은 **무수정**이다.
봉인 재계산 결과 `recorded=5853e8a469993a57` · `actual=5853e8a469993a57` → **SEAL_OK**,
조건 수 23 그대로다. 아래 항목은 전부 "이 조건을 이렇게 읽어라" 가 **아니라** 관측·핸드오프
기록이며, 어떤 조건의 PASS 근거로도 쓰이지 않는다.

포맷은 `harness/references/contract-schema.md` §Amendment 사이드카 (v5.3 · direction × consent
2 축) 를 따른다.

**QA iteration 2 요약**: blocking 1 건(AP-03)을 **조문 재해석이 아니라 구현 수정으로** 해소했다.
AP-03 은 이제 원 측정문 문자 그대로 충족한다 — `python3 scripts/validate-plugin.py flutter-toolkit`
exit 0 (`V6 code-fence 0 bare — OK`) **+** 변경된 `docs/flutter` 5 개 md 의
`grep -cE '^```$'` 합계 **0** (zsh · bash 동일).

## AM-01 — 관측 기록 (direction 없음 · PASS 근거로 쓰지 않음)

- **대상 조건**: AP-03
- **관측**: AP-03 두 번째 측정절의 오라클 `grep -cE '^```$'` 은 **닫는 펜스를 위반으로 센다.**
  마크다운 규약상 닫는 펜스는 언어 힌트를 달 수 없으므로, 이 오라클은 코드 예시를 하나라도
  가진 파일에 대해 구조적으로 만족 불가다. QA 실측 6 건(`testing.md` 4 · `state-management.md` 1 ·
  `animation.md` 1)은 전부 정상 `dart` 블록의 닫는 펜스였고, 여는 펜스 기준 위반은 0 건이었다
  (`flutter-toolkit/skills` · `agents` · `references` · `docs/flutter` 40 개 md 전수 스캔:
  `bare_open=0` · `unclosed=0`).
- **이 오라클은 Phase 5 에서 **퇴행**한 것이다.** 같은 조건을 Phase 1~4 는 전부 길이 인식
  검출기로 썼고 나이브 grep 을 명시적으로 배제했다:
  - Phase 1 `AP-03` — *"펜스 길이 인식 검출기 `bare_open_total=0` · 나이브 `` ^```$ `` grep 은
    닫는 펜스 60 건을 오탐하므로 오라클로 쓰지 않는다"*
  - Phase 2 `AP-03` — *"펜스 길이 인식 검출기로 여는 펜스 중 힌트 없는 것 0 건"*
  - Phase 3 `AP-03` — *"나이브 `` ^```$ `` grep 은 닫는 펜스를 오탐하므로 오라클로 쓰지 않는다"*
  - Phase 4 `AP-03` — 동일 문구
  Phase 5 커밋(`a35e5cc`) 메시지도 *"나이브 오라클 2 종 교정 — 닫는 펜스를 세던 bare-fence
  grep(→ 여는 펜스만)"* 이라고 적었다. 즉 **검증 시점에는 교정한 오라클을 썼는데 계약 측정문에는
  퇴행판이 남았다.**
- **그럼에도 amendment 로 처리하지 않은 이유 (direction 계산)**: "여는 펜스만 센다" 로 고쳐 읽으면
  PASS 하는 구현 집합이 **늘어난다** (원 측정을 통과하는 파일은 자동으로 개정 측정도 통과하지만,
  역은 성립하지 않는다) → `relaxing`. 사용자 발언 앵커가 없으므로 `unanchored` 이고,
  `relaxing · unanchored` 는 PASS 근거가 될 수 없다 (§Amendment 사이드카 2 축 표).
  Phase 4 AM-01 이 같은 자리에서 철회된 전례가 있다. **따라서 사이드카로는 이 blocking 을 닫을 수
  없고, 구현을 고치는 것이 유일한 경로다.**
- **무엇을 고쳤나** (`docs/flutter/quality/testing.md` · `state/state-management.md` ·
  `ui/animation.md`):
  1. 세 파일의 fenced code block 6 개를 **백틱 4 개 펜스**(` ````dart ` … ` ```` `)로 전환했다.
     CommonMark 는 여는 펜스와 같거나 더 긴 닫는 펜스를 허용하므로 렌더 결과는 동일하고,
     여는 펜스의 언어 힌트(`dart`)도 그대로 유지된다. 닫는 펜스 줄이 `` ``` `` 단독이 아니게 되어
     나이브 오라클의 오탐 표면 자체가 사라진다.
  2. 세 파일 상단에 **펜스 규약 주석**을 남겨 다음 편집자가 백틱 3 개로 되돌리지 않게 했다.
     주석은 HTML 주석이라 렌더 산출물에 나타나지 않는다.
  - `performance.md` · `research-log.md` 는 코드 블록이 0 개라 이미 0 건이었다 — 측정 대상 5 개
    파일 전부가 0 이다 (한 곳만 고친 것이 아니다).
  - 레포에 4 백틱 펜스 선례가 이미 있다 (`harness/docs/guides/plugin-validation-guide.md:328` ·
    `docs/superpowers/plans/*.md`), 틸드 펜스 선례도 flutter-toolkit 안에 있다
    (`flutter-toolkit/skills/flutter-kaizen/references/pr-template.md`). 4 백틱을 고른 이유는
    `startswith("```")` 로 펜스를 인식하는 레포 자체 도구
    (`scripts/validate-plugin.py` `_body_without_code_blocks` · `check_v6_code_fence`)가
    그대로 동작하기 때문이다. 틸드는 그 인식에서 빠진다.
- **범위 준수**: 변경 3 개 파일은 전부 AR-01 화이트리스트 17 경로 안이다. 새 경로를 추가하지
  않았고 계약 파일도 건드리지 않았다.
- **약화가 아님 (실행 증거)**:

  | 뮤테이션 | 입력 | 결과 |
  | ------ | ------ | ------ |
  | M0 수정 전 재현 | `a35e5cc` 상태 | 합계 **6** (`testing.md` 4 · `state-management.md` 1 · `animation.md` 1) — QA 실측과 일치 |
  | M1 음성 대조 | `animation.md` 닫는 펜스 1 개를 백틱 3 개로 되돌림 | 합계 **1** — 즉시 검출 (복원 후 다시 0) |
  | M2 여는 펜스 힌트 보존 | 6 블록 CommonMark 파싱 | `blocks=6` · `all_closed_and_hinted=True` — 힌트 유실 0 |
  | M3 여는 펜스 기준 위반 | 스코프 40 개 md 전수 | `bare_open=0` · `unclosed=0` |

- **사실 관계 하나 더**: 실측 6 건 중 **5 건은 `a35e5cc` 이전부터 있던 기존 펜스**였다
  (부모 커밋 카운트: `testing.md` 3 · `state-management.md` 1 · `animation.md` 1). 이번 커밋이
  새로 만든 것은 1 건뿐이다. 조건 문구가 "변경 **파일** 전체" 라 기존 줄까지 측정 대상에 들어온
  구조다 — 이 사실도 AM-02 의 근거에 포함된다.
- **다른 12 개 변경 파일(flutter-toolkit 쪽)은 왜 안 고쳤나**: AP-03 측정문은 두 절이 변경 집합을
  분할한다 — flutter-toolkit 12 개는 1 절(`validate-plugin.py flutter-toolkit`, V6 = 여는 펜스
  인식)이 담당하고 이미 `0 bare — OK` 로 통과한다. 2 절 grep 의 대상은 `docs/flutter` 뿐이다.
  QA 도 정확히 그렇게 계산해 6 을 보고했다. 통과 중인 절의 대상 파일 79 개 펜스를 함께 바꾸는 것은
  측정에 기여하지 않는 순수 churn 이라 하지 않았다.

## AM-02 — 핸드오프 (범위 밖 · direction 없음 · PASS 근거로 쓰지 않음)

- **대상 조건**: AP-03 (근본원인)
- **관측**: 계약 측정문이 퇴행한 근본원인은 **쓰기 측 가이드가 아직 나이브 오라클을 가르치기
  때문**이다. `harness/docs/guides/skill-design-guide.md:887` 은 지금도 이렇게 규정한다 —
  *"검증법: SKILL.md 저장 후 `` rg -n '^```\s*$' <file> `` 로 bare fence 탐지 … 0 건이어야 한다"*.
  `\s*` 가 붙었을 뿐 닫는 펜스를 세는 것은 동일하다. 계약을 쓰는 주체가 이 문장을 그대로 옮기면
  Phase 5 와 같은 퇴행이 반복된다.
- **왜 이번에 안 고쳤나**: `harness/` 는 Phase 5 Scope 밖이다. 계약 §범위 경계가
  *"건드리지 않는다: … 다른 킷 전부"* 라고 못박았고, Scope 는
  `flutter-toolkit/{skills,agents,references}` · `docs/flutter/` 4 개 디렉토리다. 여기서 harness
  가이드를 고치면 범위 위반이 새 blocking 이 된다.
- **권고 (Phase 1 · 설계 가이드 소관)**:
  1. `skill-design-guide.md:887` 의 검증법을 **펜스 길이 인식 검출기**로 교체한다 (여는 펜스만
     판정 · 미닫힘 펜스 별도 보고). 같은 문서 §8.7 의 "bare fence(``` 단독) 금지" 서술도 "여는
     펜스" 로 한정한다.
  2. 검출기를 계약마다 손으로 재서술하지 말고 **공유 스크립트 1 개**로 착지시킨다. 현재는 Phase
     1·2·3·4 가 각자 "펜스 길이 인식 검출기" 라는 **말**만 공유하고 구현은 매번 즉석에서 만든다 —
     SSOT 가 없어서 Phase 5 가 나이브판으로 되돌아갈 수 있었다. `scripts/validate-plugin.py` 의
     V6 로직(이미 여는 펜스 인식)을 임의 경로에도 적용 가능한 형태로 노출하는 것이 가장 싸다.
  3. `.claude/kaizen-input/per-project-feedback.md:187` 에도 같은 나이브 근거
     (`` grep -Pn '^```\s*$' ``)가 QA 증거로 박제돼 있다. 입력 데이터라 수정 대상은 아니지만,
     다음 사이클이 이걸 근거 템플릿으로 재사용하지 않게 표시해 둔다.
