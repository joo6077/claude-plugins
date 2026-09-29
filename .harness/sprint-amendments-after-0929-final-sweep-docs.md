# after-0929-final-sweep-docs 개정

계약 `sprint-contract-after-0929-final-sweep-docs.md` (봉인 `sha256:34da4f58f14e406f` · 측정 `sha256:e2e8c0f8d4737f10`,
봉인 커밋 `87500fcc`) 의 조건 줄은 고치지 않았다. 바뀐 것은 여기에만 적는다.

## AM-01 — relaxing

- 대상 조건: 구조-03
- 변경: `docs/index.html` · `docs/bambu-kit/bambu-print-profile.html` 두 쪽에 한해 색 지문 비교를
  「새로 더한 요소를 뺀 나머지 요소의 색은 시작 판과 같다」로 좁혀 잰다. 나머지 200 쪽(어두운 테마)과 84 쪽(밝은
  테마)은 원 조건 그대로 지문이 같아야 한다(`changed=0`). 두 쪽은 모두 시작 판에서 어두운 테마만 있던 쪽이라 밝은
  테마 지문(84 쪽)에는 들지 않는다 — 좁혀 재는 것은 어두운 테마 두 번이다.
- 왜: 구조-07 이 요구하는 목차 항목 둘이 `docs/index.html` 에, 구조-08 이 요구하는 원본 내용이
  `docs/bambu-kit/bambu-print-profile.html` 에 새 요소를 더한다. 원 조건의 지문은 글자를 가진 요소마다 한 줄이라
  요소가 하나만 늘어도 색과 상관없이 바뀐다 — 세 조건을 원 문구대로 함께 만족하는 구현이 없었다.
- 근거 (redaction 거친 원문 — 세션 기록의 선택지 답): 질문 「…그래서 이 두 쪽에서만 '새로 더한 요소를 뺀 나머지
  요소의 색은 시작 때와 같다'로 검사를 바꿔도 될까요? 나머지 200 쪽은 지금처럼 '변화 0'을 그대로 유지합니다.」,
  고른 답 「두 쪽만 바꾼다 (Recommended)」
- 앵커: 2026-09-29T04:43:11.908Z · session=bda55d45-296c-491f-89ba-b52042d58e72 ·
  cwd=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928

### consent — anchored

세션 기록 `~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72.jsonl`
의 `AskUserQuestion` 쌍을 `tool_use_id` 로 짝지어 뽑았다. 결정 기록
`/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/.harness/.meta/after-kaizen-0928/decisions.md`
맨 끝 절이 같은 시각 · 줄을 적는다.

| 항목 | 값 |
| --- | --- |
| 질문 머리 | 색 검사 조건 |
| 질문 시각 | 2026-09-29T03:22:14.329Z (기록 6385 번째 줄) |
| 답 시각 | 2026-09-29T04:43:11.908Z (기록 6392 번째 줄) |
| `tool_use_id` | `toolu_015eZeoefQygP9LaDx5nYoUN` |
| 세션 | `bda55d45-296c-491f-89ba-b52042d58e72` |
| 작업폴더 | `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928` |
| 고른 답 | 두 쪽만 바꾼다 (Recommended) |

동의는 이 개정을 담은 커밋보다 앞선다 — 이 스프린트의 구현 첫 커밋 `42579355` 부터 모두 04:43:11Z 뒤다.

### amend_direction — 계산

스키마 `harness/references/contract-schema.md` 의 측정 집합 헬퍼 `amend_direction_oracle` 에 원 측정 집합(시작 판
어두운 테마 지문을 통째로 비교하는 쪽 202 개 — `git ls-tree -r --name-only cacd9da3 -- docs` 의 `.html`)과 개정 측정
집합(그중 두 쪽을 뺀 200 개)을 넣었다. zsh · bash 모두 같다.

```text
relaxing measured_removed=2 measured_added=0
```

두 쪽은 통째 지문 비교에서 빠지고 요소별 비교로 옮겨지므로 PASS 집합이 늘어난다 — 완화다.

### 새 측정

원 도우미 `measure.py` · `br.js` 는 그대로 둔다(지문 `1d53c015d309e924` · `01c706e939a85586`, 커밋 `94174ada` 판과 같음).
개정 측정은 새 이름의 두 파일이다.

| 파일 | sha256 앞 16 자리 |
| --- | --- |
| `.harness/.meta/after-0929-final-sweep-docs/keep-colors-narrow.py` | `dcdefbcc0888a7f6` |
| `.harness/.meta/after-0929-final-sweep-docs/br-rows.js` | `72dcf0ccbe2a8878` |

- 부르는 법: W 맨 위 폴더에서 `python3 .harness/.meta/after-0929-final-sweep-docs/keep-colors-narrow.py`
  (`TMPDIR` 은 scratch 아래 폴더). 기대 끝 줄 `dark_pages=200 light_pages=84 changed=0 narrowed_checks=2 narrowed_bad=0`
  · `br_rc=` 값이 모두 0 · 종료 코드 0.
- 200 · 84 쪽은 `measure.py` 의 `paint` 를 그대로 불러 구조-03 과 같은 지문을 비교한다.
- 두 쪽은 `br-rows.js` 가 구조-03 과 같은 고정 방법(색 설정 · `dk-theme` 저장값 · `data-theme` 셋 다 같은 값, 움직임
  줄이기 설정, 1280 폭, 0.3 초, 폭 320 · 375 · 1280 돌리기)으로 요소마다 [태그 · 글자색 · 배경색 · 글자] 를 낸다.
  시작 판 요소를 [태그 · 글자] 로 새 판과 짝짓고(`difflib`), 시작 판 요소가 모두 짝이 있고(`removed=0`) 짝지은 요소와
  body 의 색이 같아야(`color_diff=0`) 통과다. 짝 없는 새 판 요소가 새로 더한 요소(`added`)다.
- 같은 도구가 읽는지 대조: 시작 판 요소 목록으로 만든 지문이 `br.js paint` 지문과 같아야 한다(`fp_agree=1`).

### 봉인 전 판에서 잰 값 (2026-09-29, 작업 폴더)

```text
NARROW dark docs/index.html base_rows=245 head_rows=247 matched=245 edited=0 added=2 removed=0 color_diff=0 fp_agree=1
NARROW dark docs/bambu-kit/bambu-print-profile.html base_rows=2701 head_rows=2833 matched=2701 edited=0 added=132 removed=0 color_diff=0 fp_agree=1
dark_pages=200 light_pages=84 changed=0 narrowed_checks=2 narrowed_bad=0 br_rc=0,0,0,0,0,0,0
```

`index.html` 의 `added=2` 는 목차 항목 둘(`design-research-log` · react style-guide), bambu 쪽 `added=132` 는 원본이
`e500a63` 뒤 얻은 절(1.95.3 전송 경로 · Phase 3.1 · 프린터 설정 검사 발췌 · 시험 파일 실행 줄 · 오르카 확인 절차 ·
체크리스트 35 ~ 38 등)이다. 두 쪽 모두 기존 요소의 글은 바꾸지 않았다(`edited=0`).

### 대조

- 자기 대조: 시작 판을 새 판 자리에 둔 `--head-root <시작 판 사본> --only-narrowed` → 두 쪽 모두 `added=0 removed=0
  color_diff=0` · `narrowed_bad=0` · 종료 코드 0.
- 음성 대조: 작업 폴더 `docs` 사본에서 `docs/index.html` 의 `.sidebar-logo` 글자색을 `var(--text)` → `#ff0000` 으로
  하나 바꾸고, bambu 쪽 체크리스트 29 번 항목 하나를 지운 뒤 `--head-root <사본> --only-narrowed` →
  `index.html … color_diff=1` (`DIV rgb(245, 240, 232)` → `rgb(255, 0, 0)` `Claude Plugins`),
  `bambu-print-profile.html … removed=5` · `narrowed_bad=2` · 종료 코드 1.
