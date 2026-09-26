---
feature: "V10 표 검사의 코드 블록 판정을 CommonMark 규칙에 맞추기"
slug: v10-fence-commonmark
created: "2026-09-26 04:49"
complexity: "중간"
conditions: 19
status: active
owner_session: f5b7f3a5-c03d-452b-b44b-fc3d15dcd1a0
conditions_digest: sha256:16ee2de44c5dc820
locked_at: "2026-09-26 10:05"
---

## 배경

`scripts/validate-plugin.py` 의 V10(표 끊김 검사)은 코드 블록 밖의 표 행만 본다. 그런데 코드 블록을
"줄을 벗겨 백틱 3 개로 시작하면 켜고 끄기를 뒤집는다" 로만 판정한다. 이 판정은 CommonMark 0.31.2
§4.5(코드 블록 규격)와 네 군데서 어긋나, 끊긴 표를 잘못 잡거나 놓친다. 두 번의 교차 진단이 합성
파일로 재현했다 (개정 `sprint-amendments-check-count-decouple-and-table-gate.md` A-06 · 다음 스프린트 2 · 5 번).

규격 (Context7 `/websites/spec_commonmark_0_31_2` 로 확인):

- 여는 줄은 같은 문자(백틱 또는 `~`) 3 개 이상. 두 문자를 섞지 않는다
- 닫는 줄은 **같은 문자이면서 여는 줄 이상 길이**, 뒤에는 공백만
- 백틱으로 여는 줄의 뒤쪽 글에 백틱이 있으면 코드 블록이 아니다 (줄 안 코드)
- 닫는 줄이 없으면 문서 끝까지가 코드 블록이다

## GAP 분석 (구현 전 점검 · 복잡도)

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 계층을 관통하나 | 2 (검사 스크립트 · 문서) |
| 공개 API·계약 변경 | 외부에 보이는 동작이 바뀌나 | 예 — V10 이 무엇을 표 행으로 보는지가 바뀐다 |
| 소비면 존재 | 반대편이 있나 | 예 — CI 가 `validate-plugin.py` 를 전 킷에 돌린다 · 기준 문서와 문서 페이지가 V10 판정을 설명한다 |
| 회귀 위험 | 기존 동작이 깨질 수 있나 | 예 — 코드 블록 판정이 틀리면 문서 끝까지 코드로 읽어 끊긴 표를 놓친다 |

4 축이 모두 "예" 라 **중간 이상**. 파일은 셋이라 "중간" 으로 둔다. 소비면 조건은 SC-02 · AR-03(전 킷 결과) ·
SK-02 · SK-03(문서 두 곳) 으로 따로 둔다.

| 대상 파일 | 실제로 읽은 자리 | 발견한 갭 | 조건 |
| --------- | ---------------- | --------- | ---- |
| `scripts/validate-plugin.py` | `check_v10_table_integrity` 의 코드 블록 판정 `line.strip().startswith("```")` 토글 · 표 행 판정 `lstrip().startswith("\|")` | 규격 네 군데 불일치 · `\|` 하나짜리 보통 문장도 표 행 | SC-01 · ER-01 · ER-02 |
| `harness/docs/guides/plugin-validation-guide.md` | §3 V10 "어떻게" · 변경 이력(순서가 `1.3.0, 1.4.0, 1.3.1` 로 뒤섞임) · frontmatter `version: 1.4.0` | 새 판정 서술 없음 · 이력 순서 | SK-01 · SK-02 |
| `docs/harness/plugin-validation.html` | §7 V10 "어떻게" 카드 · 제목 `v1.4.0` · 원본 주석 `(v1.4.0)` · 판 표시 · "이후 들어온 것" 안내 · 변경 이력(`<strong>1.4.0</strong>`) | 기준 문서를 따라가야 함 | SK-03 · SC-03 |
| `scripts/validate-doc-contracts.py:65` | `FENCE_RE` — yaml 블록만 찾는 다른 스크립트의 정규식 | 공유 대상 아님 (용도 · 파일이 다르다) | RE-02 |

## 범위 경계

- 바꾸는 파일은 셋이다 (AR-01 기대 집합). `docs/index.html` 은 제목에 버전이 없어 건드리지 않는다
- **V10 만 바꾼다.** V6(언어 힌트 검사)도 같은 토글 판정을 쓰지만 V6 범위(`docs/` 제외)에는 백틱 4 개 · `~~~`
  블록이 0 개라 지금 영향이 없다. V6 은 다음 과제로 남긴다
- **4 칸 들여쓴 코드 블록은 판정하지 않는다.** 목록 안에 들여쓴 표와 구별하려면 목록 문맥을 따라가야 해서
  이번 규칙에 넣지 않았다. 앞선 교차 진단은 그런 블록 안 `|` 줄을 0 개로 셌고, 봉인 전 교차 진단은 4 칸 이상
  들여쓴 `|` 줄 22 개가 모두 번호 목록 안의 정상 표(design-audit · infra-test · reflect-promote)임을 확인했다 — 목록 문맥까지
  따라가는 확인은 못 했다
- V10 이 읽는 **파일 목록은 바꾸지 않는다** (AR-03 이 킷별 파일 수로 잰다)
- 기준 문서 버전은 1.4.1 로 올린다. 변경 이력 순서가 `1.3.0, 1.4.0, 1.3.1` 로 뒤섞여 있어 날짜 순으로 바로잡는다
- 배포: 병합 커밋으로 합치고 harness patch 릴리스. 열린 릴리스 PR #110(다른 세션 · 14 킷)이 먼저 합쳐진 뒤에 한다

### 설계 결정

- **`~~~` 코드 블록 안 표 24 행이 검사 밖으로 나간다.** 카이젠 스킬 넷의 `pr-template.md` 가 PR 본문 틀을
  `~~~markdown` 블록에 담는다. 규격상 코드 블록 안이라 표가 아니다. 옛 판은 `~~~` 를 몰라 안쪽 백틱 줄에서
  켜고 끄기가 뒤집히며 이 틀 안의 표를 재고 있었다 (그중 끊긴 표 0 개). 규격을 따르는 쪽을 택한다
- 표 행은 **(왼쪽 공백을 벗겨) 줄 앞이 `|` 이면서 `|` 가 둘 이상**인 줄로 본다. 두 조건이 모두 필요하다 — 줄 앞 조건을
  빼면 `argument-hint: "<a> | <b>"` 같은 frontmatter 줄이 표 행이 되어 레포에서 63 곳을 잘못 잡는다 (봉인 전 교차 진단 실측).
  목록 안의 "`|` 로 시작하는 보통 문장" 을 잘못 잡지 않게 하려는 규칙이다. 지금 표 행 6,981 줄 중 `|` 가 하나뿐인 줄은 0 개다.
  한계: 앞 `|` 하나만 쓰는 한 칸짜리 표(`| a`)는 이 규칙에서 표 행이 아니다 — 레포에 0 개
- 합성 시험 파일을 레포에 넣지 않는다 — CI 가 돌리지 않아 죽은 시험이 된다 (메모리 `feedback_new_fixture_must_join_run_list`).
  대신 이 계약의 픽스처 표가 측정이다

### 봉인 전 실측값 (2026-09-26, 기준 커밋 77ed5bb)

- 픽스처 12 개(SC-01 의 F1~F10 · E1 · E2)를 기준 판 `check_v10_table_integrity` 에 돌린 결과: **7 개 틀림**(F1 · F2 · F3 · F4 · F5 · F6 · F10),
  5 개 맞음(F7 · F8 · F9 · E1 · E2). 봉인 전 교차 진단 뒤 더한 F11 은 기준 판도 맞다 (줄 앞이 `|` 가 아니라 표 행이 아님)
- 레포 전체: 대상 254 파일 · 표 행 6,981 줄 · 끊긴 표 0 · `|` 하나짜리 표 행 0. 새 규칙 시제품으로는 표 행 6,957 줄
  (빠진 24 줄은 전부 `pr-template.md` 4 개의 `~~~` 블록 안) · 끊긴 표 0 · 새로 생긴 표 행 0
- 백틱 4 개 이상 여닫는 줄 8 개(가이드 2 파일) · `~~~` 줄 16 개(`pr-template.md` 4 파일) · 백틱 여는 줄 뒤 글에 백틱 0 개
- `--json` 결과 비교 스크립트(아래 공통 정의)의 기준값: 같은 판끼리 `DIFF_OTHER=0 V10_FILES_DIFF=0` ·
  양성 대조 — 390dea8(V10 범위가 좁던 판)과 비교하면 `V10_FILES_DIFF=10` · V9 요약 글자만 바꾼 사본과 비교하면 `DIFF_OTHER=14`
- 기준 문서 마크다운 경고(markdownlint-cli2 0.23.2 · MD013 끔): MD025 1 · MD036 29 · 그 밖의 규칙 0
- 기준 문서 변경 이력 순서 `1.0.0,1.1.0,1.2.0,1.3.0,1.4.0,1.3.1` · 페이지 변경 이력 `1.0.0,1.1.0,1.2.0,1.3.0,1.3.1,1.4.0` · 페이지 굵은 판 `1.4.0`
- `node scripts/check-docs-a11y.js docs/harness/plugin-validation.html` → `1/1 PASS`
- `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0

### 공통 정의

- `S=scripts/validate-plugin.py` · `G=harness/docs/guides/plugin-validation-guide.md` · `P=docs/harness/plugin-validation.html`
- **픽스처 실행법**: 픽스처 내용을 임시 폴더의 `kit/docs/f.md` 로 쓰고, 재는 판의 `$S` 를 `importlib` 로 불러
  (레포 `scripts/` 를 `sys.path` 에 넣어 `plugin_utils` 를 찾게 한다) 모듈의 `REPO_ROOT` 를 임시 폴더로 바꾼 뒤
  `CheckContext(kit_path=<임시>/kit, marketplace_data={})` 로 `check_v10_table_integrity` 를 부른다. 결과 `details`
  중 `FAIL` 로 시작하는 줄의 `:줄번호` 를 모은다. 부모의 참고 구현: scratchpad `v10_fixtures.py` (평가자는 자기 방식으로 다시 재도 된다)
- **`--json` 비교법**: 기준 커밋의 `$S` 를 `git show` 로 임시 파일에 꺼내고, 두 판을 각각 `sys.argv=["x","--json"]` 로
  `main()` 을 불러 같은 레포 파일에 돌린다. 킷마다 V10 을 뺀 검사 결과 사전이 같은지(`DIFF_OTHER`), V10 요약의
  `N md files` 가 같은지(`V10_FILES_DIFF`) 센다. 부모의 참고 구현: scratchpad `v10_cmp_json.py`
- 구간 상한 (이 레포 관례):

```bash
sprint_head() {  # 머지됐으면 머지 커밋의 가지 쪽 부모, 아니면 가지 끝
  m=$(git log --merges --format=%H --grep="from joo6077/feat/${1}" -1)
  [ -n "$m" ] && { git rev-parse "$m^2"; return 0; }
  git rev-parse --verify -q "feat/${1}" && return 0
  echo "UNRESOLVED feat/${1}" >&2; return 1
}
```

- 오라클 해소: SK-01 — 재는 것이 문서의 판 번호와 변경 이력 순서 자체다
- 오라클 해소: SK-02 — 새 판정을 기준 문서가 적었는지가 취지다. 판정 동작 자체는 SC-01 이 실행으로 잰다
- 오라클 해소: SK-03 — 페이지가 기준 문서 판을 따라갔는지가 취지다. 페이지가 뜨는지는 SC-03 이 브라우저로 잰다
- 봉인 전 교차 진단(qa-evaluator 1 회)이 짚어 고친 것: 표 행 규칙의 "줄 앞" 조건이 문구에서 빠져 두 해석이 가능했다 → 문구 명시 + F11 · "늘 둘 이상" 단정 → 한계로 · 4 칸 코드 블록 0 개 주장의 확인 범위
- 오라클 해소: RE-02 — N/A 조건이다. 사유의 사실(같은 규칙의 판정 코드가 없음)은 `grep` 한 줄로 확인한다

## Skill

- [ ] SK-01: 기준 문서의 판이 1.4.1 이고, 변경 이력이 날짜 순으로 정확히 한 번씩 나온다 [exact, enumerated]
      (측정: `grep -m1 '^version:' $G` 출력이 `version: 1.4.1` ·
       `awk '/^## 8\. 변경 이력/,0' $G | grep -oE '^\| 20[0-9-]+ \| [0-9]+\.[0-9]+\.[0-9]+' | grep -oE '[0-9]+\.[0-9]+\.[0-9]+$' | paste -sd, -`
       출력이 `1.0.0,1.1.0,1.2.0,1.3.0,1.3.1,1.4.0,1.4.1` (정렬하지 않은 문서 순서) · 양성 대조: 봉인 전 `1.0.0,1.1.0,1.2.0,1.3.0,1.4.0,1.3.1`)
- [ ] SK-02: 기준 문서 V10 절이 새 판정 세 가지를 적는다 [exact, enumerated]
      (측정: `awk '/^### V10 /,/^## 4\. /' $G` 구간에서 아래 세 리터럴이 각각 `grep -cF` 1 이상 —
       `CommonMark 0.31.2 §4.5` · `` `|` 가 두 개 이상인 줄만 표 행으로 본다 `` · `4 칸 들여쓴 코드 블록은 판정하지 않는다` ·
       양성 대조: 봉인 전 셋 다 0)
- [ ] SK-03: 문서 페이지가 기준 문서 1.4.1 을 따른다 [exact, enumerated]
      (측정: `$P` 에서 — `<title>` 줄에 `v1.4.1` 1 · `kaizen-cycle` 주석 줄에 `(v1.4.1)` 1 · `class="ver"` 줄에 `v1.4.1` 1 ·
       변경 이력 `grep -oE '<tr><td>20[0-9-]+</td><td>(<strong>)?[0-9]+\.[0-9]+\.[0-9]+' $P | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | paste -sd, -`
       이 `1.0.0,1.1.0,1.2.0,1.3.0,1.3.1,1.4.0,1.4.1` · `grep -oE '<td><strong>[0-9.]+</strong></td>' $P` 가 `<td><strong>1.4.1</strong></td>` 한 줄뿐 ·
       `awk '/id="v10"/,/<!-- ── 8/' $P` 구간에 `CommonMark 0.31.2` 1 이상 · 양성 대조: 봉인 전 제목 `v1.4.0` · 굵은 판 `1.4.0` · `CommonMark` 0)

## Script

- [ ] SC-01: Given 아래 픽스처 13 개 · When 이번 판 `check_v10_table_integrity` 를 §공통 정의 실행법으로 부르면 · Then 각 픽스처의 FAIL 줄 번호가 기대값과 같다 [exact, enumerated]
      (측정: 13 개 전부 일치. 픽스처 내용은 `\n` 이 줄바꿈인 문자열 그대로다.
       음성 대조: 같은 픽스처를 기준 커밋 77ed5bb 의 `$S` 에 돌리면 F1 · F2 · F3 · F4 · F5 · F6 · F10 이 기대값과 다르다 — 봉인 전 실측)

  픽스처 (이름 · 기대 FAIL 줄 · 파이썬 문자열 그대로의 내용 — `\n` 이 줄바꿈):

  ```text
  F1  없음  "머리\n\n````markdown\n```text\n| 끊긴 | 모양 |\n```\n````\n"
  F2  없음  "머리\n\n~~~markdown\n| 끊긴 | 모양 |\n~~~\n"
  F3  없음  "- 항목\n\n  ~~~\n  | 끊긴 | 모양 |\n  ~~~\n"
  F4  4     "- 항목\n  ```bash``` 로 부른다\n\n| 끊긴 | 행 |\n"
  F5  없음  "- 항목\n  | 로 시작하는 문장이다\n"
  F6  6     "````\n```\n| 안 | 쪽 |\n````\n\n| 끊긴 | 행 |\n"
  F7  없음  "```\n| 끊긴 | 모양 |\n"
  F8  9     "1. 목록\n\n   | h | h |\n   | --- | --- |\n   | 1 | 1 |\n\n   산문\n\n   | 2 | 2 |\n"
  F9  없음  "머리\n\n| a | b |\n| --- | --- |\n| 1 | 2 |\n"
  F10 6     "~~~\n```\n| 안 | 쪽 |\n~~~\n\n| 끊긴 | 행 |\n"
  E1  없음  ""
  E2  없음  "```\n"
  F11 없음  "머리\n\nargument-hint: \"<a> | <b> [| <c>]\"\n"
  ```

  뜻: F1 백틱 4 개 블록 안의 백틱 3 개 블록 · F2 `~~~` 블록 · F3 목록 안 들여쓴 `~~~` · F4 목록 이어지는 줄 첫머리의 줄 안 코드 ·
  F5 `|` 하나짜리 보통 문장 · F6 짧은 닫는 줄은 닫지 못함 · F7 닫는 줄 없음 · F8 코드 블록 밖 들여쓴 끊긴 표 ·
  F9 정상 표 · F10 `~` 블록을 백틱 줄이 닫지 못함 · E1 빈 파일 · E2 여는 줄만 ·
  F11 줄 앞이 `|` 가 아니면서 `|` 가 둘 이상인 줄 (표 행 판정의 줄 앞 조건을 잠근다)

- [ ] SC-02: 검증 스크립트가 전 킷 통과한다 [exact]
      (측정: `python3 scripts/validate-plugin.py` 끝 두 줄이 `Total: 14 plugins, 14 OK` · `Exit: 0`)
- [ ] SC-03: 문서 검사 넷이 통과한다 [exact, enumerated]
      (측정: `node scripts/check-docs-a11y.js docs/harness/plugin-validation.html` 마지막 줄 `1/1 PASS` ·
       `scripts/check-docs-links.py` · `scripts/check-stale-values.py` · `scripts/check-contrast-claims.py` 를 각각 `python3` 으로 돌려 종료 코드 0)

## Error

- [ ] ER-01: 코드 블록이 끝나지 않은 파일 · 빈 파일 · 여는 줄만 있는 파일에서 예외 없이 FAIL 0 을 낸다 [exact]
      (측정: SC-01 의 F7 · E1 · E2 를 부를 때 예외가 0 건이고 FAIL 줄이 없다. 양성 대조: 이 셋은 기준 판도 맞다 — 멀쩡하던 동작이 깨지지 않았는지를 잰다)
- [ ] ER-02: FAIL 출력 줄의 모양이 바뀌지 않는다 [exact]
      (측정: SC-01 의 F8 을 기준 판과 이번 판에 각각 돌려 나온 `FAIL` 줄 문자열이 글자까지 같다)

## Architecture

- [ ] AR-01: Given 이 스프린트 커밋이 끝난 뒤 · 변경 파일이 정확히 3 개로 한정된다 [exact, enumerated]
      (측정: `git diff --name-only 77ed5bb..$(sprint_head v10-fence-commonmark) -- . ':(exclude).harness/**' | sort` 가 기대 집합
       `docs/harness/plugin-validation.html` · `harness/docs/guides/plugin-validation-guide.md` · `scripts/validate-plugin.py` 세 줄과 일치.
       `UNRESOLVED` 면 판정 보류)
- [ ] AR-02: 코드 블록 판정이 V10 함수 밖, 모듈 수준에 있어 다른 검사가 불러 쓸 수 있다 [structural]
      (측정: `$S` 를 불러 모듈 수준 함수 중 이름에 `code_block` 또는 `fence` 가 들어간 것이 1 개 이상이고, 그 함수에 F2 의 줄 목록을 넣으면
       표 모양 줄(4 번째 줄)이 코드 블록 밖으로 나오지 않는다)
- [ ] AR-03: V10 밖의 검사 결과와 V10 이 읽는 파일 수가 기준 판과 같다 [exact]
      (측정: §공통 정의 `--json` 비교법으로 기준 커밋 77ed5bb 과 비교해 `DIFF_OTHER=0 V10_FILES_DIFF=0` ·
       양성 대조: 봉인 전 390dea8 과 비교 → `V10_FILES_DIFF=10`, V9 요약 글자만 바꾼 사본과 비교 → `DIFF_OTHER=14`)

## Anti-patterns

- [ ] AP-02: force push 금지 — 이 세션이 봉인 뒤 실행한 명령에 강제 푸시가 0 건이다 [exact]
      (측정: 세션 기록 `~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/f5b7f3a5-c03d-452b-b44b-fc3d15dcd1a0.jsonl` 의
       `tool_use` 중 이름이 `Bash` 이고 `timestamp` 가 봉인 시각 이후인 것의 `command` 에서 `git push` 와 함께 `--force` 나 단독 `-f` 옵션이
       든 것을 세어 0. 명령 글자를 보므로 그 문구를 인자로 담은 명령을 봉인 뒤에 돌리지 않는다)
- [ ] AP-03: bare code fence 금지 — V6 가 통과하고, 기준 문서에 새로 넣은 코드 블록에도 언어 힌트가 있다 [exact]
      (측정: `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0 · V6 은 `docs/` 를 읽지 않으므로 기준 문서는
       markdownlint-cli2 0.23.2 의 `MD040` 이 0 건으로 잰다)

## Reusability

- [ ] RE-01: N/A (재사용 단위는 AR-02 가 잰다 — 코드 블록 판정을 모듈 수준 함수로 둔다. 이 줄은 자동 포함 조건의 자리 표시다)
- [ ] RE-02: N/A (레포에 같은 규칙의 판정 코드가 없다 — `scripts/validate-doc-contracts.py:65` 의 `FENCE_RE` 는 yaml 블록만 찾는 다른 스크립트용이라 공유 대상이 아니다. 측정: `grep -rn '~{3' scripts/*.py` 가 그 한 줄뿐)

## Diagnostics

- [ ] DG-01: N/A (commands.analyze 는 `bash -n scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 대신 DG-02 가 파이썬 문법을, SC-02 가 전 킷 실행을 잰다)
- [ ] DG-02: 바꾼 파이썬 파일이 문법 검사를 통과하고, 기준 문서의 마크다운 경고가 기준값보다 늘지 않는다 [exact]
      (측정: `python3 -m py_compile scripts/validate-plugin.py` 종료 코드 0 · markdownlint-cli2 0.23.2(MD013 끔)로 `$G` 를 돌려 MD025 1 이하 · MD036 29 이하 · 그 밖의 규칙 0.
       IDE 의 파이썬 진단은 명령으로 못 재므로 이 둘로 대신한다)
- [ ] DG-03: N/A (commands.test 는 `bash scripts/release.sh 2>&1 || true` — 릴리스 스크립트라 이번 변경을 재지 않는다. 측정: AR-01 목록에 `scripts/release.sh` 0 줄)
- [ ] DG-04: 검증 스크립트를 여러 실행 경로로 돌려도 예외 없이 끝난다 [exact, enumerated]
      (측정: `python3 scripts/validate-plugin.py --check=table-integrity` · `--json` · `harness` · `--help` 를 각각 돌려 종료 코드 0 이고
       출력에 `Traceback` 0)
