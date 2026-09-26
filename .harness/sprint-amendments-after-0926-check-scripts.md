---
slug: after-0926-check-scripts
created: "2026-09-26 20:37"
---

## A-01 — SC-09 측정 도우미 `drift.sh` 의 맥 sed 결함

**기준 조건**: SC-09 의 측정 줄 — `drift.sh` 의 `ci_lines=1` · `table-real rc=0` · `table-drop rc=<0 아님> named=<1 이상> changed=1` · `script-add rc=<0 아님> named=<1 이상> applied=1` (도우미 지문 `c6f46c258cf295c3`)

**무엇이 틀렸나**: 도우미 23 번째 줄이 CI 파일의 `run:` 줄에서 명령만 떼려고 `sed -E 's/^\s+run: //'` 를 쓴다.
이 맥의 `/usr/bin/sed`(BSD) 는 확장 정규식에서 `\s` 를 공백으로 읽지 않아 아무것도 떼지 못한다. 그래서 떼어 낸 명령이
앞 공백과 `run:` 이 붙은 채(`run: python3 scripts/detect-docs-drift.py --check-table`) `bash -c` 에 들어가 `run:` 이라는 명령을 못 찾고
종료 코드 127 이 난다. 구현과 무관하게 `table-real` · `table-drop` · `script-add` 세 줄이 늘 `rc=127 named=0` 이다 —
봉인 전 실측은 시작 판에서 `ci_lines=0` 이라 이 줄들이 돌지 않아 결함이 드러나지 않았다.

**고친 측정**: 23 번째 줄의 `\s` 를 `[[:space:]]` 로만 바꾼다. 나머지 줄 · 기대값 · 양성 대조는 그대로다.

```text
- CMD=$(grep -E '^\s+run: .*scripts/detect-docs-drift\.py' "$T/.github/workflows/ci.yml" | sed -E 's/^\s+run: //')
+ CMD=$(grep -E '^\s+run: .*scripts/detect-docs-drift\.py' "$T/.github/workflows/ci.yml" | sed -E 's/^[[:space:]]+run: //')
```

고친 도우미 지문: sha256 앞 16 자 `6d4b0a25e0f48707` (원 도우미 `c6f46c258cf295c3`)

**실측** (가지 끝 `157e8a2` 근처, 2026-09-26 20:37):

```text
원 도우미   ci_lines=1 · table-real rc=127 · table-drop rc=127 named=0 changed=1 · script-add rc=127 named=0 applied=1
고친 도우미 ci_lines=1 · table-real rc=0   · table-drop rc=1 named=1 changed=1   · script-add rc=1 named=1 applied=1
고친 도우미, 시작 판 6378948  ci_lines=0 (양성 대조 그대로)
```

**direction**: `relaxing` — 같은 구현에서 원 측정은 FAIL, 고친 측정은 PASS 다. 원 측정은 어떤 구현도 통과시키지 못하므로
통과 집합이 빈 집합에서 늘어난다 (계약 스키마 §Amendment 사이드카 — 원 오라클과 개정 오라클로 각각 판정해 FAIL→PASS 면 relaxing).
재는 대상(CI 파일에서 꺼낸 명령 한 줄)과 기대값은 바뀌지 않았다.

**consent**: (비어 있음 — 사용자 확인 필요. 조건을 느슨하게 하는 개정이라 위임으로 동의 처리하지 않는다)
