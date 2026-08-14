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

> **[2026-08-13 18:50 · 철회] 이 항목의 조치는 AM-04 로 대체됐다.** QA 가 relaxing × unanchored
> 조합이라 PASS 근거로 쓸 수 없다고 판정했고, 그 판정이 옳다. 측정문을 좁히는 대신 **구현을
> 고쳐서 원 측정문을 그대로 충족**시켰다 — 지금 `grep -rlF 'mistake_tag:' reflect-kit/hooks` 는
> 1 행이다. 위 본문은 당시 판단 기록으로 남긴다.

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


## AM-04 — AM-01 철회 · SC-05 를 구현 수정으로 충족 (measurement 완화 없음)

**대상**: SC-05 · AM-01 의 조치 항목
**계기**: QA REJECT (blocking 1 건). 판정 요지 — AM-01 은 direction=relaxing × consent=unanchored
라 PASS 근거로 쓸 수 없고, 원 조건 문언대로 재면 SC-05 는 FAIL 이다.

**받아들인다.** 측정문을 좁히면 오라클만 조용해지고 리터럴은 두 곳에 그대로 남는다 — 이번
사이클이 F1·F2 에서 고친 바로 그 실수(오라클을 통과시키려고 판별력을 낮추는 것)의 재발이다.
그래서 **계약 문언은 그대로 두고 구현을 고쳤다.**

### 무엇이 진짜 결함이었나

AM-01 은 `log-reflection.sh:165` 를 "프롬프트 안 스키마 예시일 뿐 추출 로직이 아니다" 로 봤다.
그 관찰은 맞지만 **결론이 틀렸다.** 그 문자열은 훅이 분석기에게 "이 키로 출력하라" 고 지시하는
**수집면의 계약**이고, 추출기가 파싱하는 키와 **반드시 같아야 한다.** 즉 165 행은 무해한 산문이
아니라 SSOT 를 공유해야 하는 두 번째 표면이었다. 오라클이 옳았고 내 해석이 틀렸다.

전 표면 조사에서 `reflect-kit/hooks` 안 **세 번째** 표면도 나왔다 — 환경 dedup 게이트의 awk
패턴(`log-reflection.sh:324,326`). AM-03 이 "여기는 짝지어 읽어야 해서 통합 불가" 로 남겨둔
자리인데, **정규화(`norm()`)는 통합 불가여도 필드 패턴은 통합 가능**하다. 둘을 분리하지 않아
놓친 것이다.

### 조치 (3 표면 전부)

| 표면 | 전 | 후 |
| --- | --- | --- |
| `_lib-tag-canon.sh` 추출기 | 리터럴 2 곳(grep·sed) | `tag_canon_line_re` 참조 |
| `log-reflection.sh` 프롬프트 스키마 | 리터럴 | `${tag_field}` (= `tag_canon_field`) |
| `log-reflection.sh` dedup awk | 리터럴 2 곳 | `-v tagre="$(tag_canon_awk_re)"` |

필드 이름과 줄 패턴의 정본을 라이브러리 상수 `_REFLECT_TAG_FIELD` + 접근자 3 종으로 두고
호출부는 접근자로만 참조한다. 규약은 `references/tag-canonicalization.md` §1 · §6.1 **규칙 8**
에 박았다 — 요지는 *"N 곳에만 존재" 를 재는 오라클은 패턴을 좁히지 말고 **문자열을 코드에서
지워라**"* 다.

### 등가 증명 (행동 변경 0)

| 대상 | before (175ef87) | after | 판정 |
| --- | --- | --- | --- |
| `tag_canon_extract` 실로그 13 파일 4,757 행 | md5 `7e3ec362ac88eff908eefb84f38ef17b` | 동일 | IDENTICAL |
| `tag_canon_groups` 2,623 행 | md5 `7156755363e43d455a6429760c60d130` | 동일 | IDENTICAL |
| 렌더된 LLM 프롬프트 6,715 B | md5 `5279bafee7657566dc49f994d218790e` | 동일 | **BYTE-IDENTICAL** |
| dedup 게이트 (무들여쓰기·공백·탭·인용부호·주석·억제창 6 케이스 × seed 유무) | — | — | IDENTICAL |

원 측정문 실행 결과: `grep -rlF 'mistake_tag:' reflect-kit/hooks` → **1 행**
(`_lib-tag-canon.sh`). 좁힌 측정도 1 행이다.

### 덧붙인 것 — 상수화가 만든 새 실패 경로를 같이 막았다

리터럴을 상수로 바꾸면 **라이브러리 source 실패 시** `tag_field` 가 빈 문자열이 된다. 그대로
두면 (1) 프롬프트 스키마에서 키 이름이 사라지고, (2) dedup awk 의 `tagre` 가 빈 정규식이 되어
**모든 줄에 매치**한다 (실측: 3 행 입력 → 3 행 매치). 둘 다 에러 없이 로그만 오염시키는,
이 사이클이 없애려던 바로 그 무증상 실패다. 그래서 훅에 빈 값 가드를 넣고
`fail:tag-field-unresolved` 를 남기고 종료한다 (실측 확인).

셀프테스트에도 단정 **(4)** 를 추가했다 — `tag_canon_awk_re` 가 들여쓰기 없음·공백·탭 3 형태에
실제로 매치하는지 매 실행 확인한다. 판별력 음성 대조 2 종 실행:
`_REFLECT_TAG_FIELD` 를 바꾸면 단정 (1)(2)(3)(4) 가 **함께** 깨지고(= SSOT 배선이 실재한다는
증거), 접근자만 망가뜨리면 (4) 만 깨진다.

**consent**: 사용자 앵커 없음. **direction 은 relaxing 이 아니다** — 조건 문언·측정문·조건 집합
변경 0, 판정 기준을 낮추지 않았고 원 측정문을 그대로 충족시켰다. AM-01 의 relaxing 제안은
철회했다.

## AM-05 — 내가 하마터면 심을 뻔한 미검증 사실 (자진 신고)

`tag_canon_awk_re` 를 만들면서 주석에 *"`\t` 를 문자열로 넘기면 구현에 따라 이스케이프가 풀리지
않아 탭 들여쓰기 줄을 조용히 놓친다"* 라고 썼다. **측정하지 않고 쓴 문장이었다.**

실측하니 이 환경의 awk(BWK 20200816)는 `-v` 값의 이스케이프를 정상적으로 푼다
(`awk -v s='a\tb'` → `length(s)` = **3**). POSIX 도 `-v` 값의 이스케이프 처리를 규정한다. 즉
두 표기의 결과가 같고 **내가 고친 버그는 없었다.** 주석을 실측값과 함께 정정하고, 미리 풀어서
넘기는 이유를 "버그 회피" 가 아니라 "`-v` 이스케이프 처리에 대한 의존을 하나 지우는 것" 으로
다시 썼다.

이 사이클의 F1·F3 이 전부 **측정 안 하고 쓴 서술**이 원인이었는데 같은 실수를 반복할 뻔했다.

## AM-06 — 측정 해석 · 범위 기록 (조건 변경 없음)

1. **AR-01 의 `git status` 측정**: 이 재제출 커밋 직전 working tree 는 3 경로다
   (`_lib-tag-canon.sh` · `log-reflection.sh` · `tag-canonicalization.md`) — 계약이 적은 5 경로의
   **부분집합**이다. 스프린트 누적으로 재면 정확히 5 경로다:
   `git diff --name-only 409c780 -- reflect-kit/` → 5 행 (409c780 = 스프린트 직전 커밋).
   경로 집합이 늘지 않았음을 두 측정으로 함께 남긴다.
2. **`~/.claude/logs` 오염 및 복구**: SC-04 프로브를 처음에 **실 로그 버킷**(`fit-pal`)에 대고
   돌려 `.errors.log` 에 `session=probe` 4 행이 append 됐다. 계약 범위 경계가 이 경로를
   **읽기 전용**으로 규정하므로 위반이다. 해당 4 행만 제거해 1,044 → 1,040 행으로 되돌리고
   (백업 보관), 이후 측정은 **복제 버킷**에서 수행했다. ~~재검증 시점 `session=probe` 잔여 0 행.~~

   > **[2026-08-13 19:10 · 정정] 이 항목의 마지막 문장은 사실과 달랐다.** `fit-pal` 한 버킷만
   > 다시 보고 전역 결론("잔여 0 행")을 적었는데, 같은 프로브가 `coupon-stl/.errors.log` 에도
   > 2 행을 남긴 상태였다. 전수 감사·복구·재발 방지는 **AM-07** 에 있다. 위 본문은 당시
   > 기록으로 남긴다.
3. **범위 밖에 남은 동종 표면**: `reflect-kit/docs/SCHEMA.md` · `docs/DESIGN.md` 가 여전히
   `mistake_tag:` 리터럴을 갖는다. 계약이 `reflect-kit/docs/*` 를 수정 금지로 두었고, 이 둘은
   **기록된 로그의 wire format 을 설명하는 문서**라 실행 경로가 아니다. 다만 필드 이름을 바꾸는
   날에는 같이 고쳐야 하므로 라이브러리 상수 주석에 "이 이름은 wire format 이다" 를 남겼다.

   > **[2026-08-13 19:10 · 보완] 이 열거도 부분 감사였다.** 위 두 파일은 `reflect-kit/docs` 만
   > 훑어 얻은 목록이고, 킷 전체를 재면 6 개다:
   > `grep -rlF 'mistake_tag:' reflect-kit` → `docs/DESIGN.md`(2) · `docs/SCHEMA.md`(2) ·
   > `hooks/_lib-tag-canon.sh`(7 · 정본) · `references/tag-canonicalization.md`(3) ·
   > `skills/reflect-digest/SKILL.md`(2) · `skills/reflect-promote/SKILL.md`(1).
   > 빠졌던 3 개 중 `references`·`skills` 2 개는 **범위 안**이다. 다만 성격은 docs 와 같다 —
   > `references` 의 3 건은 전부 규칙 6·8 이 인용한 **전례 서술**(`- mistake_tag:` fixture,
   > `grep -rlF 'mistake_tag:'` 측정문)이고, `skills` 의 3 건은 로그 wire format 을 보여주는
   > **YAML 스키마 예시**다. 실행 경로는 하나도 없어 SC-05(`reflect-kit/hooks` 1 곳) 판정에
   > 영향이 없고, 지우면 오히려 전례 기록이 사라진다. **그래서 고치지 않는다** — 부분 열거를
   > 완전 열거로 정정할 뿐이다. 필드 이름을 바꾸는 날 함께 고쳐야 할 목록은 위 6 개 파일이다.

## AM-07 — 범위 경계 위반 전수 복구 (QA blocking 해소 · 조건 변경 없음)

**대상**: 계약 「범위 경계」의 `~/.claude/logs/**` (읽기 전용) · AM-06 §2 의 완료 주장
**계기**: QA REJECT — "coupon-stl/.errors.log 에 `session=probe` 2 행이 남아 있고, AM-06 §2 의
'잔여 0 행' 은 fit-pal 버킷에만 해당하는 사실인데 전역 결론으로 적혔다."

**받아들인다.** 두 가지가 다 사실이다. 오염이 남아 있었고, 그 상태에 대한 내 완료 선언이
부정확했다. 후자가 더 나쁘다 — 한 버킷을 보고 전역을 단정한 것은 이 사이클이 F1·F2 에서
고친 실수(범위를 좁힌 오라클을 전체의 증거로 쓰는 것)와 같은 형태다.

### 1. 무엇이 남아 있었나

`coupon-stl/.errors.log` — **파일 전체가 프로브 산출물**이었다. 4 행 append 였던 fit-pal 과
성격이 다르다.

| 측정 | 결과 |
| --- | --- |
| `stat -f '%SB' .../coupon-stl/.errors.log` (birth) | `2026-08-13T18:45:59` = 프로브 실행 시각 |
| 총 행 수 | 2 |
| 비-`session=probe` 행 수 | **0** |

즉 프로브 이전에 이 파일은 **존재하지 않았다.** fit-pal 만 보고 있어서 놓쳤다 — 프로브를 실
버킷 하나에 돌렸다고 기억했지만 실제로는 두 버킷에 돌렸고, 기억을 명령으로 확인하지 않았다.

### 2. 복구 (전 버킷)

파일이 프로브 생성물이므로 **비우지 않고 지웠다** — 빈 `.errors.log` 를 남기는 것은 원상복구가
아니라 새 잔여물이다. 지우기 전 원문을 백업했다
(`<scratch>/coupon-stl.errors.log.polluted.bak`, 2 행).

fit-pal 복구도 이번에 백업 대조로 재검증했다 — **원본 손상 없음**:

```
diff <(grep -vF 'session=probe' <scratch>/errors.log.bak) ~/.claude/logs/fit-pal/.errors.log
→ 차이 0 행 (bak 1,044 행 − probe 4 행 = 현재 1,040 행)
```

다만 복구 방식이 in-place 편집이 아니라 파일 재작성이어서 `fit-pal/.errors.log` 의 **birth 가
18:46:43 으로 바뀌었다** (내용은 위 대조대로 동일). 되돌릴 수 없는 메타데이터 변화라 여기 남긴다.

### 3. 전수 재감사 (범위를 명령으로 열거)

이번에는 "몇 개 버킷을 봤다" 를 타이핑하지 않고 산출했다.

| 측정 | 명령 | 결과 |
| --- | --- | --- |
| 감사 범위 · 버킷 수 | `find ~/.claude/logs -mindepth 1 -maxdepth 1 -type d \| wc -l` | **11** |
| 감사 범위 · 파일 수 | `find ~/.claude/logs -type f \| wc -l` | **49** |
| 프로브 세션 잔여 | `grep -rlF 'session=probe' ~/.claude/logs \| wc -l` | **0 파일** |
| 프로브 경유 마커 4 종 (`warn:lemma-map-unreadable path=/nonexistent` · `fail:tag-field-unresolved` · `PROBE_FAIL` · `SELFTEST_FAIL`) | 각각 `grep -rlF` | 전부 **0 파일** |
| 스프린트 창 이후 **생성**된 파일 | `find ~/.claude/logs -type f -newerBt '2026-08-13 18:20'` | 2 개 (아래 귀속) |
| 프로브가 만든 버킷 디렉토리 | 11 개 디렉토리 birth 전수 확인 | **0 개** (최신 birth 는 17:11 `bundle`, 스프린트 이전) |
| 프로브가 만든 `.project-root` 마커 | 11 개 마커 birth 전수 확인 | **0 개** (전부 스프린트 이전) |

감사 대상 버킷(11): `.playwright-mcp` · `bundle` · `claude-plugins` · `coupon-stl` · `fit-pal` ·
`flutter_playwright` · `h2s-superlube-applicator` · `jackson` · `skadis-board-abs` ·
`social-feed-s1` · `social-feed-s2`. (QA 총평의 "13 개 버킷" 은 디렉토리가 아니라
`reflections-*.md` **파일 13 개**와 겹쳐 읽힌 수치로 보인다 — `find ~/.claude/logs -name
'reflections-*.md' | wc -l` → 13. AM-04 의 "실로그 13 파일" 은 후자를 가리키며 정확하다.)

스프린트 창 이후 생성된 2 파일의 귀속:

- `fit-pal/.errors.log` (birth 18:46:43) — **내 복구 작업**. 내용은 §2 대조로 원본 동일.
- `fit-pal/.env-issues.tsv` (birth 19:03:56) — **내 것이 아니다.** 내 프로브는 전부 18:42~18:49 에
  끝났고 상태 파일을 scratchpad(`$OUT.state.tsv`)에 쓴 뒤 지운다. 이 파일은 그 뒤 19:03 에 돌아간
  fit-pal 실세션 Stop 훅의 dedup 게이트가 tmp+mv 로 남긴 것이고, 내용도 실데이터다
  (`missing-pretool-hook-scripts` count=97, first_seen 1785409742 = 스프린트 훨씬 이전).

### 4. 계약이 이름 붙인 나머지 scope-out 경로도 같이 훑었다

blocking 은 로그 한 절이었지만, 같은 결함(=범위 경계 위반을 부분 감사로 넘김)이 다른 절에도
있는지 **계약이 열거한 모든 scope-out 경로**를 쟀다. 전부 0 이다.

| scope-out 경로 | 측정 | 결과 |
| --- | --- | --- |
| `reflect-kit/docs/*` · `README.md` · `hooks/hooks.json` · `scripts/*` · `.claude-plugin/*` | `git diff --name-only 409c780 -- <5 경로>` | **0 행** |
| 봉인 계약 `…-tag-canonicalization.md` | `git diff --name-only 409c780 -- <파일>` | **0 행** (AR-03 재확인) |
| `~/.claude/settings.json` | mtime | `16:00:18` — 스프린트 시작(18:20) 이전 |
| `~/.claude/hooks/` | `find … -newermt '2026-08-13 18:20' \| wc -l` | **0** |
| `~/.claude/logs/**` | 위 §3 | 잔여 **0** |

### 5. 재발 방지 (문서 한 줄이 아니라 절차로)

`references/tag-canonicalization.md` §6.1 에 **규칙 9** 를 넣었다. 요지 세 가지다.

1. `log_hook_error` 는 **디렉토리 존재만 확인하고 append** 한다 (`_lib-project-id.sh:119-123`).
   그래서 훅 조각 프로브에 실 버킷을 넘기면 사용자 로그가 조용히 오염된다 — 프로브는
   `mktemp -d` 복제 버킷에만 돌린다.
2. 정리 확인은 **전 버킷 전수**로 한다. 버킷 수를 명령으로 산출하고
   `grep -rlF 'session=<probe id>' ~/.claude/logs` 로 훑는다. 한 버킷 결과를 전역 결론으로 쓰지
   않는다 (이번 전례를 그대로 적었다).
3. 오염 파일이 프로브 **생성물**이면 비우지 말고 지운다 (birth 로 판별).
4. 사이드카에는 "잔여 0 행" 이 아니라 **감사 범위·명령·출력**을 적는다.

`~/.claude/logs` 는 계약상 읽기 전용이지만 이번 삭제 1 건은 **원상복구를 위한 되돌림**이다
(프로브가 만든 파일을 없애 프로브 이전 상태로 복원). 새 오염이 아님을 위 birth·행수 증거로
남긴다. 그 외 이 경로에 대한 쓰기는 0 이다.

**consent**: 사용자 앵커 없음 (백그라운드 서브에이전트). **direction 은 relaxing 이 아니다** —
조건 문언·측정문·조건 집합 변경 0. 계약 문구로 위반을 소거하지 않고 **상태를 되돌렸고**, 부정확했던
자기 주장(AM-06 §2)을 정정했다. 변경 경로 집합도 늘지 않았다
(`references/tag-canonicalization.md` 는 AR-01 의 5 경로에 이미 포함).
