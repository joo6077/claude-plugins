---
slug: howto-kit-implementation
created: "2026-09-08 12:20"
amends: sprint-contract-howto-kit-implementation.md
contract_digest_at_amendment: sha256:5de60ce9548db9c6
---

## A-01 · AR-07 diff-scope 베이스라인 정정

**대상 조건**: AR-07 (변경 범위 허용목록)
**개정 내용**: 측정 명령의 베이스라인을 `4fb1382` 에서 `54fb3b3` 으로 좁힌다.
허용목록과 제외 pathspec 은 **바꾸지 않는다**.

원 측정 명령:

```text
git diff --name-only 4fb1382..HEAD -- . ':(exclude).harness/handoff/*' ':(exclude)docs/bambu-calibration/*'
```

개정 측정 명령:

```text
git diff --name-only 54fb3b3..HEAD -- . ':(exclude).harness/handoff/*' ':(exclude)docs/bambu-calibration/*'
```

### direction — 자기신고가 아니라 집합 비교로 산출

```text
A = 4fb1382..HEAD  (원)      37 경로
B = 54fb3b3..HEAD  (개정)    35 경로

comm -23 A B   (측정에서 빠지는 경로)
  .harness/sprint-contract-howto-kit-design-brief.md
  .harness/sprint-feedback-howto-kit-design-brief.md

comm -13 A B   (새로 들어오는 경로)
  (없음)
```

| 축 | 값 |
| --- | --- |
| direction | **`relaxing`** — 제거만 2 건, 추가 0 건 |
| anchor | **`unanchored`** — 계약 서술 섹션이 이 변경을 앵커하지 않는다 |
| consent | **획득** — 사용자가 2026-09-08 "베이스라인 54fb3b3 로 좁힌다" 를 선택 |

`relaxing · unanchored` 는 그 자체로 정당화되지 않는다. 아래가 사유다.

### 사유

빠지는 2 경로는 커밋 `54fb3b3` 이 도입했고, 그 커밋은 **별개 스프린트**의 산출물이다.

```text
slug:              howto-kit-design-brief
status:            done            (qa-evaluator 가 APPROVE 시점에 전환)
conditions_digest: sha256:dee06e6878247d76
```

AR-07 의 `Given:` 절은 *"이번 스프린트의 커밋 변경 경로"* 를 측정 대상으로 지정한다.
`4fb1382` 를 베이스라인으로 쓰면 **직전 스프린트의 커밋까지 이번 스프린트의 범위로 세게 되므로**,
그 베이스라인 자체가 조건의 의도와 어긋난 오라클이었다. 실질적 범위 이탈은 없다 —
두 파일 모두 이미 별도 계약으로 평가·승인된 산출물이다.

`git show --stat 0e771e0` (이번 스프린트의 구현 커밋)에는 두 파일이 등장하지 않는다.

### 왜 허용목록에 추가하지 않았는가

허용목록에 두 경로를 넣으면 *"이 스프린트가 저 파일들을 건드려도 된다"* 는 서술이 되어
조건의 의미가 부정확해진다. 실제 사실은 *"저 파일들은 이 스프린트의 대상이 아니다"* 이므로
베이스라인을 좁히는 쪽이 의미에 맞다.

### 재측정 결과 (2026-09-08)

```text
$ git diff --name-only 54fb3b3..HEAD -- . ':(exclude).harness/handoff/*' ':(exclude)docs/bambu-calibration/*' | wc -l
35
$ 허용목록 밖 경로 건수
0
```

## 남기는 교훈

diff-scope 오라클의 베이스라인은 **직전 커밋이 아니라 "이번 스프린트의 첫 커밋 직전"** 이어야
한다. 이어작업 브랜치에서 `main..HEAD` 를 그대로 쓰면 앞 스프린트의 산출물이 섞인다.
계약 작성 시점에 베이스라인 커밋 해시를 명시적으로 고르고, 그 시점의 `git log --oneline -1` 을
서술 섹션에 남기면 이 결함이 재발하지 않는다.

## A-02 · AR-07 허용목록에 amendment 사이드카 경로 추가

**대상 조건**: AR-07 (변경 범위 허용목록)
**개정 내용**: 허용목록에 `.harness/sprint-amendments-howto-kit-implementation.md` 1 항목을 추가한다.
베이스라인(A-01 로 `54fb3b3`)과 제외 pathspec 은 바꾸지 않는다.

### direction — 집합 비교로 산출

```text
A = 원 허용목록          14 항목
B = 개정 허용목록        15 항목

comm -13 A B   (추가)
  .harness/sprint-amendments-howto-kit-implementation.md

comm -23 A B   (제거)
  (없음)
```

| 축 | 값 |
| --- | --- |
| direction | **`relaxing`** — 추가 1, 제거 0 |
| anchor | **`unanchored`** — 계약 서술 섹션이 사이드카를 언급하지 않는다 |
| consent | **획득** — 사용자가 2026-09-08 "사이드카 경로 1 개 추가" 를 선택 |

### 사유

`harness/references/contract-schema.md` §산출물 3 종 (line 99~105) 은 슬러그당 산출물을
**계약 · QA 피드백 · amendment 사이드카 3 종**으로 정의한다. 원 계약의 AR-07 허용목록은
앞의 2 종만 열거하고 사이드카를 빠뜨렸다 — 계약 작성 시점의 누락이다.

그 결과 A-01 을 담은 사이드카 파일 자체가 커밋 `2b1cbcd` 에서 diff 에 새로 등장해
허용목록 밖 1 건으로 잡혔다. AR-07 을 고치려던 조치가 그 조치의 산출물 때문에 재발한
자기참조 결함이다.

A-02 는 **기존 사이드카 파일에 덧붙이므로** 새 경로가 생기지 않는다. 자기참조는 여기서 끝난다.

### 패턴화를 택하지 않은 이유

평가자는 `.harness/*-howto-kit-implementation.md` 패턴을 권고했다. 효과는 같지만
`[exact, enumerated]` 태그의 "개별 이름 열거" 관례에서 벗어나고, 이 슬러그의 산출물은
스키마상 정확히 3 종이라 패턴의 이득이 없다. 최소 변경(1 항목 추가)을 택한다.

### 재측정 — 이 개정을 담은 커밋이 랜딩된 **뒤** HEAD 기준

A-01 의 재측정은 사이드카 커밋 전 시점 값이라 stale 했다. 같은 실수를 반복하지 않도록
이번 재측정은 커밋 후 HEAD 에서 15 항목 허용목록 문언 그대로 돌린 결과를 아래에 적는다.
(값은 커밋 직후 채운다 — 자리표시자 없이, 실행 출력을 그대로.)

**HEAD 해시는 여기에 적지 않는다.** 이 파일을 담는 커밋의 해시를 이 파일 안에 적을 수는 없다 —
적는 순간 그 커밋이 아니게 된다 (2026-09-08 실측: `10a8a50` 을 적고 `--amend` 하자 HEAD 가
`b809c75` 로 바뀌어 인용이 stale 해졌다). 검증자는 **자기 시점의 HEAD** 에서 아래 명령을 돌린다.
이 사이드카를 갱신하는 커밋은 사이드카 경로만 건드리므로(A-02 로 허용목록에 있음) 경로 집합을
바꾸지 않는다.

```text
$ git diff --name-only 54fb3b3..HEAD -- . ':(exclude).harness/handoff/*' ':(exclude)docs/bambu-calibration/*' \
    | 15 항목 허용목록(계약 AR-07 14 항목 + A-02 의 1 항목) 문언 그대로 매치
총 37 경로 · 허용목록(15 항목) 밖 0 건        ← 2026-09-08, 구현 커밋 0e771e0 + 사이드카 커밋 포함 상태
```
