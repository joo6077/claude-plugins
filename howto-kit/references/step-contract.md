# Step Contract — 스키마 정본

**이 파일이 Step Contract 필드 정의의 유일한 정본이다.** 다른 스킬·에이전트·evals 는 이 파일을
참조만 하고 필드 목록을 재서술하지 않는다. 재서술은 반드시 갈라진다 — 같은 규칙이 두 문서에
적히면 하나만 갱신되고 나머지가 조용히 옛 규칙으로 남는다.

대화 모드(`/howto`)와 문서 모드(`/howto-doc`)가 **같은 스키마**를 쓴다. 렌더링만 다르다.

## 스키마

```yaml
step:
  id: string                      # S1, S2, …
  condition: string | null        # 이 스텝을 실행하는 객관 조건. 항상이면 null (렌더링 생략)
  mode: READ_DO | DO_CONFIRM      # 실행 지시형 / 사후 검증형
  where:
    entry_url: string | null      # 딥링크. 있으면 이것이 1 순위
    path: [string]                # ["Settings","General","Cloud Messaging"] — 중간 단계 전부
    container: string | null      # left sidebar / top tab / dialog / upper-right / bottom of page
  what:
    verb: 이동|열기|선택|누르기|입력|체크|토글|저장|다운로드|업로드
    target_label: string          # 화면에 그대로 보이는 라벨
    target_label_i18n: string|null# 한국어 UI 라벨 (영문이 정본, 한국어는 괄호)
    target_type: 버튼|필드|탭|토글|드롭다운|체크박스|링크|메뉴|섹션
  value: string | null            # 입력값·선택지. 없으면 "입력 없음" 으로 명시 (빈칸 금지)
  constraints: string | null      # 형식·길이·범위·기본값
  verify: string                  # 이 스텝이 끝났음을 눈으로 확인하는 관측값 (필수)
  if_not_found:                   # 선제 분기. 최소 1 개
    - cause: 권한|요금제|버전|언어|A/B
      then: string
  killer: boolean                 # 누락 시 치명적인가
  source:
    url: string | null
    fetched_at: date | null
    tier: 관측 | 문서 | 추정 | 없음
```

## 필수·선택

| 필드 | 필수 | 비고 |
| --- | --- | --- |
| `id` · `mode` · `what.verb` · `what.target_label` · `what.target_type` | 필수 | |
| `where` | 필수 | `entry_url` 과 `path` 중 **최소 하나**. 둘 다 없으면 전역 검색어를 `path` 대신 적는다 |
| `value` | 필수 | 입력이 없어도 `"입력 없음"` 이라고 쓴다. `null` 로 비우면 렌더링에서 사라져 사용자가 무엇을 넣어야 하는지 모른다 |
| `verify` | **필수 (예외 없음)** | 아래 사유 참조 |
| `if_not_found` | 필수 · 최소 1 개 | |
| `source.tier` | **필수 (예외 없음)** | |
| `condition` · `constraints` · `killer` · `target_label_i18n` | 선택 | |

### `verify` 를 모든 스텝에 요구하는 이유

DITA 1.3 은 `<stepresult>` 를 *"should not be used for every step"* 이라고 한다
(docs.oasis-open.org/dita/dita/v1.3/os/part2-tech-content/langRef/technicalContent/stepresult.html).
이 킷은 그 권고를 **의도적으로 강화**한다. 표준을 모르고 어기는 것이 아니라,
이 도메인의 실패 데이터가 다르기 때문이다.

막으려는 실패는 **무증상 실패** — 절차를 다 따랐는데 아무 일도 일어나지 않고 에러도 안 나는 것이다.
같은 레포의 실측 사례: `docs/bambu-calibration/` 계열 문서가 기록한
*"silent skip 이 가장 위험한 실패 모드 — 에러 없이 0 건 import"*. 확인 지점이 없으면 사용자는
마지막 스텝까지 가서야 아무것도 안 됐다는 것을 알게 되고, 어느 스텝이 실패했는지 되짚을 수 없다.

## 절차 전체 골격 (DITA task 모델)

```text
prereq   사전 요구사항 · 필요한 계정/권한/준비물 · 사이트 배정표 · 수수료 · 처리기간 · 되돌리기 가능 여부
context  이 절차가 무엇을 달성하는가 (1~2 문장)
steps    Step Contract 배열
result   전부 끝났을 때의 관측 가능한 최종 상태
postreq  뒤처리 · 되돌리기 · 파기해야 할 것
```

DITA `<taskbody>` 콘텐츠 모델은 `<prereq>?, <context>?, (<steps>|<steps-unordered>)?, <result>?, <postreq>?`
순서다 — docs.oasis-open.org/dita/dita/v1.3/os/part2-tech-content/contentmodels/cmtct.html

## 대화 모드 렌더링

```text
S<n>. [조건이 있으면] <어디서> 에서 <무엇을> <타입> 을 <동작>
      값: <입력값 또는 "입력 없음">
      확인: <끝났음을 눈으로 확인하는 관측값>
      안 보이면: <분기>
      출처: <URL> (조회 YYYY-MM-DD) 또는 [추정] 또는 [미확인]
```

- `where.path` 는 `A > B > C` 로 렌더한다. `>` 앞뒤에 공백을 두고 `>` 자체는 굵게 하지 않는다
  (learn.microsoft.com/en-us/style-guide/procedures-instructions/describing-interactions-with-ui).
  **경로는 구조화해서 보관하고 렌더링에서만 `>` 로 합친다** — Microsoft 는 `>` 를 굵게 하지 말라 하고
  Google 은 시퀀스 전체를 한 bold 로 감싸라 해서 표기가 갈리기 때문이다.
- `where.entry_url` 이 있으면 그것을 첫 줄에 두고 `path` 는 보조로 붙인다.
- `source.tier` 가 `관측` 이면 출처 줄을 생략한다 (최고 등급이라 표기가 불필요하다).

## 문서 모드 렌더링

문서 모드는 게이트 G1(출처 원장 완전성)이 기계 판정할 수 있도록 **고정 마커**를 쓴다.
마커 문자열은 `../scripts/howto-gate.sh` 의 판정식과 짝이므로 임의로 바꾸지 않는다.

```text
## S<n>. <한 줄 요약>

- 어디서: <entry_url 또는 A > B > C>
- 무엇을: <target_label> (<target_type>)
- 동작: <verb>
- 값: <value>
- 확인: <verify>
- 안 보이면: <cause> — <then>
- 출처: <url> (조회 YYYY-MM-DD)
```

`## S<n>.` 헤더 1 개 = 액션 스텝 1 개다. `- 출처:` 줄이 그 스텝의 출처 원장 1 줄이다.

**문서 모드에는 `관측` 등급의 출처 줄 생략 규칙이 적용되지 않는다.** 게이트 G1 이 액션 스텝
수와 출처 줄 수를 대조하므로 생략하면 원장이 깨진다. `관측` 이면 `- 출처: 관측 (사용자 확인
YYYY-MM-DD)` 로 쓴다. 문서 헤더에는 `- 대상:` 을 반드시 두어야 G3 가 판정할 수 있다.

## `mode` — READ_DO 와 DO_CONFIRM

| 값 | 뜻 | 언제 |
| --- | --- | --- |
| `READ_DO` | 읽으면서 그때그때 실행한다 | 처음 하는 절차, 되돌리기 쉬운 조작 |
| `DO_CONFIRM` | 먼저 하고 나중에 한 번에 검증한다 | 익숙한 절차, 흐름을 끊으면 안 되는 구간 |

**근거 등급 `[미확인]`** — 이 두 값은 **이 킷의 운영 어휘**다. 외부 표준이나 특정 저작의
정의로 인용하지 마라. READ-DO / DO-CONFIRM 구분의 1 차 출처를 확보하지 못했다 (2026-09-08 조회,
시도 URL 은 `provenance-notes.md` §1). 같은 이유로 "한 묶음 5~9 항목" 과 "killer item" 은
이 스키마의 규칙으로 넣지 않았다 — 근거 없는 숫자를 규칙으로 만드는 것이 이 킷이 막으려는 F3 다.
