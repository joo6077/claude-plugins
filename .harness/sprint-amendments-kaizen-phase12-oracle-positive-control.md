---
slug: kaizen-phase12-oracle-positive-control
contract: .harness/sprint-contract-kaizen-phase12-oracle-positive-control.md
created: "2026-08-13 18:40"
---

## AM-01 — clarification (측정문 결함 신고 · 조건 문구 변경 없음)

**대상**: SC-05 의 측정절
**원문**: "`grep -rlF 'mistake_tag:' reflect-kit/hooks` 결과가 `_lib-tag-canon.sh` 1 행"

**실행 결과 (2026-08-13)**

| 측정 | 결과 |
| --- | --- |
| 원 측정문 `grep -rlF 'mistake_tag:' reflect-kit/hooks` | **2 행** (`_lib-tag-canon.sh` · `log-reflection.sh`) |
| 추출 패턴으로 좁힌 측정 `grep -rlF '^[[:space:]]*mistake_tag:' reflect-kit/hooks` | **1 행** (`_lib-tag-canon.sh`) |

**판정**: 원 측정문은 **substring 오탐**이다. `log-reflection.sh:165` 의 `mistake_tag:` 는 추출
규칙이 아니라 **LLM 프롬프트 안의 YAML 스키마 예시**다 (분석기에게 이 필드를 출력하라고 지시하는
문장). 추출 규칙 자체는 좁힌 측정대로 라이브러리 1 곳에만 있다 — **증명하려던 명제는 성립한다.**

내가 세운 §6.1 규칙 7(`-F` 로 거짓 음성을 막아라)을 지켰는데도 **반대 방향인 거짓 양성**에
걸렸다. 교훈: `-F` 는 메타문자 오해석만 막고 **패턴이 너무 넓은 문제는 못 막는다.** "N 곳에만
존재" 를 재는 오라클은 대상 문자열을 **역할이 구별되는 형태**(여기서는 앵커를 포함한 실제 패턴)로
좁혀야 한다.

**조치**: 계약 본문은 고치지 않는다 (write-once). SC-05 는 **주 측정 미충족 · 좁힌 측정 + 등가
증명으로 명제 성립** 으로 보고한다. 다음 사이클에 이 조건을 재사용한다면 측정문을
`grep -rlF '^[[:space:]]*mistake_tag:' reflect-kit/hooks` 로 써야 한다.

**등가 증명 (SC-05 후단)**: 실로그 13 파일 전량에 대해 통합 전 인라인 추출과
`tag_canon_extract` 의 출력 md5 가 동일하다 — 양쪽 `0de336873d8c6758d2ecb6ffb01ebb9b`.

**consent**: 사용자 앵커 없음 (백그라운드 서브에이전트 실행). direction 은 **narrowing 아님 ·
widening 아님** — 조건 집합·경로 집합 변화 0. 측정 해석 기록일 뿐이다.

## AM-02 — 직전 계약(다른 슬러그)의 측정문 결함 신고 · 그 계약 본문 미수정

**대상**: `sprint-contract-kaizen-phase12-tag-canonicalization.md` 의 RE-02
**원문**: "(측정: `grep -c 'source \"$SCRIPT_DIR/_lib-' reflect-kit/hooks/log-reflection.sh` == 3)"

**실행 결과 (2026-08-13, 이 환경)**

| 측정 | 결과 |
| --- | --- |
| 원 측정문 그대로 (BRE) | **0** |
| `grep -cF` | **3** |
| `grep -c 'source "\$SCRIPT_DIR/_lib-'` (이스케이프) | **3** |
| 참값 (`source "$SCRIPT_DIR/_lib-…"` 실제 줄 수) | **3** |

**원인**: 이 환경의 `grep` 은 **ugrep 7.5.0** 이고 패턴 **중간의 `$` 를 앵커로 해석**한다
(`grep --version` → `ugrep 7.5.0 aarch64-apple-macosx`). POSIX BRE 는 `$` 를 패턴 끝에서만
앵커로 보지만 이 구현은 다르다. 따라서 원 측정문은 **참인 매치를 0 으로 보고**한다.

**왜 중요한가**: RE-02 는 `== 3` 이므로 거짓 음성이 곧 FAIL 로 드러난다 — 그래서 이번에 잡혔다.
그러나 **"0 건이면 PASS"** 형태의 조건(직전 계약 SK-06 · AR-03 · AR-04, 이 레포 다수 계약이
쓰는 형태)에서 같은 실수를 하면 **위반이 있어도 조용히 PASS** 한다. 방향이 반대라 훨씬 위험하다.

**조치**: 그 계약 본문은 건드리지 않았다 (봉인 · 이 스프린트 AR-03 로 diff 0 행 확인). 재발 방지
규약은 `reflect-kit/references/tag-canonicalization.md` **§6.1 규칙 7** 에 실측과 함께 박았다.
직전 계약의 RE-02 판정은 **참값 기준 충족**(3 == 3)이며, 그 계약의 "29/29 PASS" 주장 중 RE-02 는
**측정문대로 실행하면 0 이 나오는 상태에서 얻어진 것**임을 여기 기록한다.

**consent**: 사용자 앵커 없음. direction 변화 0 (다른 슬러그의 계약이며 조건 집합 불변).

## AM-03 — 발견했으나 이번 스프린트에서 해소하지 않은 결함 (기록 보존)

**대상**: 계약 조건 아님 (범위 밖 판단 기록)

`log-reflection.sh` 의 **환경 이슈 dedup 게이트**(`.env-issues.tsv`)는 그룹 키로 **원시 태그**를
쓴다. 같은 환경 문제가 다른 표기로 오면 다른 그룹으로 보여 억제되지 않는다 — K3 이 `post_freq`
에서 고친 파편화가 **이 경로에는 그대로 남아 있다.**

**이번에 고치지 않은 이유**: 그 awk 는 블록 안에서 `mistake_tag` 와 `actionability` 를 **짝지어**
읽어야 해서 `tag_canon_extract`(플랫 목록)로 대체할 수 없다. 여기에 `norm()` 을 복제하면
SSOT §1(정규화 구현은 라이브러리 1 곳) 이 깨진다. 올바른 해소는 **정규화 pass 를 스트림 필터로
노출하는 것**이고, 이는 dedup 동작 변경이므로 사용자 합의를 받는 별도 스프린트 대상이다.

**한 것**: 코드에 알려진 한계 주석을 남겨 다음 에이전트가 canonical 키로 오인하지 않게 했고,
"여기에 `norm()` 을 복제하지 마라" 를 명시했다. 행동 변경 0.
