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
