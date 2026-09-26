# 묶음 c3c — 킷 후속 B (reflect-kit · bambu-kit · tone-kit · api-kit)

- 계약: `.harness/sprint-contract-after-0924-kits-b.md` (봉인 `sha256:c583ca357d027c78`, 27 조건)
- 작업 폴더: `.claude/worktrees/ak-c3c`, 가지 `chore/ak-c3c-kits`, 시작점 `88ddfe5`
- QA 판정은 이 문서가 내리지 않는다. 다음 단계의 qa-evaluator 몫이다.

## 한 일

| 커밋 | 묶음 | 내용 |
| --- | --- | --- |
| `cb7006a` | harness | 계약 봉인 커밋 (계약 파일 하나) |
| `1b26074` | reflect | 코드 블록 없는 분석 출력 정규화 · 옛 엔트리 세기 · 멈춤 경고 문턱 · 대체 경로 `--safe-mode` · 시험 두 개에 경우 추가 |
| `86d2074` | bambu | 목록 `[미검증]` 문구가 안 돈 검사만 적게 · G-code 길이 재기 문단에 `G91` 실측 한 줄 |
| `b367184` | tone | 표 칸 정규식 규칙 · 번역투 grep 열이 §8 갈래를 가리킴 · 「8종」 셈 기준 |
| `22d5901` | api | 설계 기록 §9.2 날짜 붙은 정정 |
| `3306a32` | reflect | tone-guide 5 단계 대조에서 나온 이름 · 주석 손질 (동작 그대로) |

## 결정과 근거

- 대체 경로 인자는 `--safe-mode` 로 정했다. 봉인 전에 사본 설정(`CLAUDE_CONFIG_DIR` 사본 + 작업 폴더 `.claude/settings.json`)으로 재 보니 시작 판 인자는 SessionStart · UserPromptSubmit 표식 `marks=4`, `--safe-mode` 를 더하면 `marks=0` 이다. 구현 뒤에도 같은 값이다(SC-05). `--bare` 는 로그인 인증을 읽지 않아 대체 경로가 죽는다. `--setting-sources` 는 플러그인 훅까지 끄는지 따로 재야 해서 고르지 않았다.
- 멈춤 경고 문턱은 「실패 3 회 이상이고 첫 실패가 1 일 이상 지났을 때」 다. digest 는 `⚠` 한 줄에 `## 승격 후보` 를 통째로 비운다. 2026-09-26 11:15 ~ 12:16 실제 기록은 옛 판 세션 둘이 한 시간 안에 실패 여섯 줄을 남겨 횟수만 보면 켜지고 1 일 문턱이면 꺼진다. 새 판의 일시 실패 빈도는 `err=` 줄이 아직 0 이라 모른다 — 숫자는 근거가 생기면 다음 사이클에 고친다. 엔트리 0 경고는 그대로다.
- 코드 블록 정규화는 Stop 훅 한 곳에서 적기 전에 한다. 분석기 프롬프트를 더 세게 쓰는 것만으로는 같은 출력을 내는 분석기를 못 막는다. `primary_category:` 줄이 없는 산문과 다른 언어 fence 는 손대지 않는다(블록을 지어내지 않는다, ER-01).
- 엔트리 셈 규칙은 `collect_status` 한 곳에만 둔다(RE-01). yaml 코드 블록 밖의 `primary_category:` 줄 하나를 엔트리 하나로 센다. 이 맥 실제 기록으로 재면 `collect_status 7` 이 옛 판 `엔트리 4` → 새 판 `엔트리 7` 이다(`reflections-2026-09.md` 의 코드 블록 없는 세 절이 들어온다).
- bambu `G91` 은 코드를 바꾸지 않는다. 설치본 H2S 시작 G-code(뱀부 02.08.02.61 · 오르카 2.4.2)는 `G91` 구간 안 E 이동이 0 이고 E 모드는 `M83` 뿐(`M82` 0)이라 `G91` 을 E 에도 적용하든 말든 길이가 같다. 측정 블록은 글자 하나 안 바꿨다(SK-07 `block_same=1`).
- bambu 목록 문구: canonical 이 없으면 지금처럼 「키 존재 · 종류 · enum 값 검사 미실행」, canonical 이 있으면 빠진 것만 적는다 — enum 이 없으면 「enum 값 검사 미실행」, 종류가 없으면 「종류 줄이 없어 키 스코프 불일치 FAIL 은 믿지 마라」. 판정 동작은 그대로다.
- tone-kit 표 칸 형식: `\|` 가 든 정규식은 표 칸에 싣지 않고 실행 블록을 가리킨다. 규칙은 슬롯 형식 정본 `adapter-contract.md` 에 뒀다. `locale-korean.md` §2 grep 열은 지우지 않고 칸마다 `§8 G-1 갈래 N` 을 가리킨다 — 열을 없애면 옛 계약들의 「§2 grep 열」 인용이 끊긴다.
- 「리서치 문서 8종」 셈 기준은 tone-kaizen 이 이미 쓰는 것 — `docs/tone/*.md` 11 개에서 overview · research-log · templates 를 뺀 주제 문서 8 개. 같은 수가 적힌 다섯 줄에 기준을 붙였다.
- `docs/api` 12종은 같은 기준(research-log 제외)으로 세면 맞아서 고치지 않았다.
- api-kit 설계 기록은 옛 두 문장을 지우지 않고 정정 표시를 달았다(같은 문서 §10.1 선례). `kaizen-orchestrator` `:574` 는 이미 고쳐져 있어 건드리지 않았다.

## 넘김 (이번에 하지 않은 것과 사유)

- 넘김: bambu 종류 줄만 빠진 옵션 목록에서 모든 키가 거짓 「키 스코프 불일치」 FAIL 을 내는 문제 — 판정 동작을 바꾸는 일이라 이번 범위 밖이다. 이번에는 `[미검증]` 줄에 「믿지 마라」 만 붙였다.
- 넘김: `G91` 이 E 까지 상대로 바꾸는지에 맞춘 코드 수정 — 펌웨어 원문이 저장소 밖이다.
- 넘김: 올리지 않은 가지 `feat/bambu-kit-orca-h2s-feedback`(다른 세션, 기준 `baa1a38` v0.9.2)과의 충돌. 그 가지는 이 SKILL.md 에 hunk 17 개를 갖고 있고 `if SYS is not None:` 블록(그 가지 기준 `@@ -1399,8 +1439,10 @@`, `META =` 줄 근처)을 고친다. 이 묶음이 고친 목록 `[미검증]` 줄은 그 블록 바로 안쪽이다. G-code 길이 재기 문단은 그 가지 기준 뒤에 생긴 문단이라 그 가지를 main 에 올리면 이 문단 앞뒤 전체가 부딪힌다.
- 넘김: api-verify 목록의 `noncharacter` · `-0` 분류 이름 — 외부 원문이 먼저라 부모가 따로 한다.
- 넘김: 이 맥 `~/.claude/logs/claude-plugins/reflections-2026-09.md` 의 코드 블록 없는 옛 세 절은 옮기거나 고쳐 쓰지 않았다(사용자 데이터). 새 셈 규칙이 그대로 읽는다.
- 넘김: 멈춤 문턱 숫자 재조정 — 새 판의 일시 실패 빈도 자료(`err=` 줄)가 쌓인 뒤.
- 넘김: `docs/` HTML 페이지 다시 만들기 — 문서 사이트 묶음(부모) 몫. 아래 드리프트 절 참고.

## 킷별 버전 판단

| 킷 | 지금 | 제안 | 이유 |
| --- | --- | --- | --- |
| reflect-kit | 0.8.0 | minor → 0.9.0 | 소비자가 있는 약속 둘이 바뀐다 — `⚠ 수집 멈춤` 경고 조건(digest · kaizen 머리)과 엔트리 셈(옛 엔트리를 센다). 훅이 적는 형식도 정규화된다 |
| bambu-kit | 0.10.0 | patch → 0.10.1 | 판정은 그대로, `[미검증]` 문구와 문서 한 줄만 바뀐다 |
| tone-kit | 0.2.0 | patch → 0.2.1 | 참조 문서의 표 칸 표기와 셈 기준 설명. 판정 규칙 · 게이트 명령은 그대로다 |
| api-kit | — | 릴리스 없음 | 킷 폴더 파일이 안 바뀌었다(설계 기록은 `docs/superpowers/specs/`) |

## 문서 페이지 드리프트

`python3 scripts/detect-docs-drift.py --since 88ddfe5 --verbose` 결과(페이지는 다시 만들지 않았다):

- 다시 만들 페이지 둘: `docs/bambu-kit/bambu-print-profile.html` (원본 `bambu-kit/skills/bambu-print-profile/SKILL.md`), `docs/tone-kit/dart-flutter-idioms.html` (원본 `docs/tone/dart-flutter-idioms.md`)
- 「NEW — 대응 HTML 없음」 넷(`reflect-digest` · `adapter-contract` · `adapter-dart-flutter` · `locale-korean`)은 원래 페이지가 없는 원본이라 만들 대상이 아니다. `docs/reflect-kit/` 페이지의 원본(`SCHEMA.md` · `DESIGN.md`)은 안 바뀌었다.

## tone-guide 5 단계 대조

1 단계에서 불러온 규칙: core-comment C-01~C-17 · core-naming N-01~N-12 · core-structure S-01~S-14 · core-antipatterns A~J · locale-korean K-01~K-11. 어댑터는 없음(`.claude/tone-project.md`) — 스택 게이트는 꺼져 있다. 대상은 이 묶음의 변경 줄 146 줄이다.

| 규칙 | 건수 | 판정 |
| --- | --- | --- |
| C-01 이유만 남긴다 | 0 | 통과 — 새 주석은 모두 이유 · 실패 모드다 (`--safe-mode` 3 줄, 정규화 3 줄, 옛 엔트리 1 줄, 문턱 3 줄, bambu 게이트 1 줄) |
| C-02 · A 이름 번역 주석 | 1 → 0 | 고침 — `stale = …` 한 줄을 지우고 이름을 `first` · `day_ago` 로 옮김 (`3306a32`) |
| C-04 · F 구분선 · 템플릿 마커 | 0 | 통과 — 새 절 머리 `# ── 코드 블록 정규화 ──` 는 같은 파일 기존 절 머리와 같은 형식이다 (C-04 는 관측 컨벤션, C-08 밀도 유지) |
| C-07 해설 3 줄 초과 | 1 → 0 | 고침 — 정규화 주석 4 → 3 줄 (코드가 이미 말하는 절을 뺌) |
| C-10 · C-12 · C-13 | 0 | 통과 — 디자인 툴 참조 · 계산 근거 · 자화자찬 grep 0 |
| C-15 주석 종결형 | 0 | 통과 — 같은 파일 기존 주석과 같은 문장형 (관측 컨벤션) |
| N-07 fallback 접두 식별자 | 0 | 통과 — 새 식별자 0 (표 칸의 글자는 규칙 설명이다) |
| N-08 한 글자 이름 | 2 → 0 | 고침 — 시험 awk 의 `y` · `b` → `yaml` · `bare`. 루프 `i` 는 관용이라 남김 |
| N-09 무역할 파일명 | 0 | 통과 — 새 파일 0 |
| S-03 · S-04 · S-06 추출 | 0 | 통과 — `wrap_loose` 는 세 곳에서 부르고 다른 함수를 안 부른다. `stall_dir` 세 곳, `fences_of` 네 곳 |
| S-05 재사용 승격 | 0 | 통과 — 정규화는 쓰는 곳이 훅 한 곳이라 라이브러리로 올리지 않았다 |
| S-12 같은 패턴 | 0 | 통과 — 새 시험 경우는 기존 `check` · `run_bg` 형식 그대로 |
| H 보존 | 0 삭제 | 통과 — 훅의 옛 이유 주석은 새 규칙으로 고쳐 썼고 지우지 않았다 |
| K-02 번역투 (§8 G-1) | 히트 6 · 위반 0 | 통과 — 히트는 전부 §2 치환표 행이다(규칙이 패턴을 담는 줄, §9 가 빼는 줄) |
| K-04 종결형 (§8 G-2 · G-3) | 0 | 통과 |
| K-09 한국어 규칙 정의처 | 0 | 통과 — 표 칸 규칙은 슬롯 형식이라 `adapter-contract.md` 소유, `locale-korean.md` 는 가리키기만 한다 |
| K-10 §8 · §9 실행 | 0 | 실행함 — §8 잔존 0, `자기모순 검사 잔존 0건` |
| K-11 새 이름 | 0 | 통과 — 「갈래」 · 「문턱」 은 일상어이고 「갈래」 는 표 아래 문장이 뜻을 풀어 준다 |

meta-audit: 불러오고 판정하지 않은 규칙은 어댑터 전용 규칙(I · J, dart 게이트 G-01~G-10)뿐이다 — 어댑터 없음. 범위 밖 파일은 건드리지 않았다.

## 측정 도구

- 계약 측정 도우미: 계약 `## 회귀 게이트` 블록을 떼어 bash 에서 `m <조건 ID>` (이번에 뗀 사본은 세션 임시 폴더의 `kitsb-measure.sh`)
- CI 로컬 실행: `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` (본 체크아웃의 추적 안 된 파일, 읽기만. sha256 `a415eaff98a46b86636e591e650950be12499307ff5720936076b85731119713` 이 봉인 전 값과 같음을 확인하고 돌렸다)
- 쓰지 않은 도구: `coverage.py` · `fence2.py` — 이 묶음은 문서 페이지를 다시 만들지 않았다
