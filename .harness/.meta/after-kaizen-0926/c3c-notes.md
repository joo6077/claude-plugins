# 묶음 c3c — 킷 후속 B (reflect-kit · bambu-kit · tone-kit · api-kit)

- 계약: `.harness/sprint-contract-after-0924-kits-b.md` (봉인 `sha256:c583ca357d027c78`, 27 조건)
- 작업 폴더: `.claude/worktrees/ak-c3c`, 가지 `chore/ak-c3c-kits`, 시작점 `88ddfe5`
- QA 판정: APPROVE 27/27 (Iteration 1). 계약 `status` 를 `done` 으로 바꿔 리포트와 함께 `931d26c` 에 실었다. 교차 진단 BLOCKING 0 — 아래 「QA 판정과 교차 진단」.

## 한 일

| 커밋 | 묶음 | 내용 |
| --- | --- | --- |
| `cb7006a` | harness | 계약 봉인 커밋 (계약 파일 하나) |
| `1b26074` | reflect | 코드 블록 없는 분석 출력 정규화 · 옛 엔트리 세기 · 멈춤 경고 문턱 · 대체 경로 `--safe-mode` · 시험 두 개에 경우 추가 |
| `86d2074` | bambu | 목록 `[미검증]` 문구가 안 돈 검사만 적게 · G-code 길이 재기 문단에 `G91` 실측 한 줄 |
| `b367184` | tone | 표 칸 정규식 규칙 · 번역투 grep 열이 §8 갈래를 가리킴 · 「8종」 셈 기준 |
| `22d5901` | api | 설계 기록 §9.2 날짜 붙은 정정 |
| `3306a32` | reflect | tone-guide 5 단계 대조에서 나온 이름 · 주석 손질 (동작 그대로) |
| `931d26c` | harness | QA 리포트 `.harness/sprint-feedback-after-0924-kits-b.md` 와 계약 `status: done` |

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

## QA 판정과 교차 진단

- qa-evaluator: APPROVE 27/27. 봉인 `SEAL_OK`, 27 조건 모두 평가자가 계약의 측정 도우미 `m <조건 ID>` 를 직접 돌려 얻은 값이다. 리포트는 `931d26c` 에 실었다
- 교차 진단(부모가 띄운 독립 검토): BLOCKING 0. 끝 판 `e830bc6` 에서 측정 11 개(SC-01~06 · ER-01 · ER-02 · AR-01 · SK-04 · SK-05 · SK-07)를 다시 돌려 구현자 값과 같았다.
  SC-05 는 로그인 안 된 설정 사본에서 실제 claude 2.1.268 로 `--safe-mode` 표식 0 · 시작 판 4 였다. CI 와 같은 리눅스(Debian bookworm, `mawk 1.3.4`)에서 reflect 시험 셋이 32 · 18 · 16 경우 모두 불일치 0 이었다.
  이 맥 실제 로그의 새 엔트리 셈은 옛 판보다 claude-plugins +3 · fit-pal +93 이고, 늘어난 줄은 모두 코드 블록 없이 적힌 진짜 옛 엔트리였다(두 번 센 것 0). 다른 C 가지들과 같은 파일을 고친 곳은 없다
- `status: done` 변경 뒤에도 조건 줄 요약값은 `c583ca357d027c78` 그대로다(조건 27 줄)
- 글로벌 피드백 `/Users/jackson/.harness/feedback/evaluator/1a3bcba6-2026-09-26T144028-bda55d45-22810.yaml` 의 `cross_diagnosis_by` 를 `sprint-contract` 로 바꾸고 결과를 `cross_diagnosis_notes` 에 적었다(`verify-feedback.sh` PASS).
  QA 리포트 안 「Cross-Diagnosis Handoff」 의 `pending-parent` 는 평가자가 쓴 그대로 두었다

## 다음 사이클 메모

독립 검토가 적은 것 가운데 판정을 바꾸지 않는 다섯 가지와 QA 개선 제안 하나. 줄 번호는 끝 판 `e830bc6` 기준이다.

1. bambu — 종류 줄만 빠진 목록에서 `[미검증]` 줄이 「enum 값 검사 미실행」 을 빠뜨린다. `bambu-kit/skills/bambu-print-profile/SKILL.md:1608` 은 종류 줄이 없을 때 「종류 줄이 없어 키 스코프 불일치 FAIL 은 믿지 마라」 만 적는다.
   그런데 키마다 종류 판정(`:1701` `elif t not in TYPES…`)이 enum 값 판정보다 먼저 와서, 종류 줄이 없으면 모든 키가 거기서 FAIL 로 끝나 enum 값 검사에 닿지 않는다. 설명 문단 `:2041` 도 같은 전제로 적혀 있다.
   재현: 설치본 목록 `bambu-02.08.02.61.tsv` 에서 `process` · `filament` · `machine` 줄을 뺀 사본으로 `process-seam-slope-type-invalid.json` 을 돌리면 `종류 0 · enum 56`, 키 9 개 모두 「키 스코프 불일치」 FAIL,
   `seam_slope_type='hole'` 을 잡는 「받지 않는 값」 줄 0, 「enum 값 검사 미실행」 줄도 0 이다. 결과가 FAIL 로 남으므로 거짓 통과는 아니다.
   위 「넘김」 의 「종류 줄만 빠진 목록의 거짓 키 스코프 불일치」 와 같은 자리다 — 판정 동작을 고칠 때 `[미검증]` 문구에 「enum 값 검사 미실행」 을 함께 넣는다
2. api — 설계 기록 §9.2 에서 바로잡은 「Hurl 로 표현 불가」 가 두 곳에 남았다. `.claude/skills/kaizen-orchestrator/references/phase-research-templates.md:261` 「경로 간 불변식은 Hurl 로 표현할 수 없다.」 는 다음 api 카이젠이 읽는 조사 지침이다.
   `docs/api-kit/multi-sample-pagination-variance.html:425` · `:428` 에 「Hurl 로 표현되지 않는다」 · 「Hurl 문법으로 쓸 수 없다」 가 있고 `:470` 이 출처로 §9.2 를 가리킨다.
   HTML 쪽은 페이지 원본 md 에 이 문장이 없고 §9.2 에서 옮겨 온 내용이라 `detect-docs-drift.py` 가 못 찾았다 — 위 「문서 페이지 드리프트」 의 다시 만들 페이지 둘에도 빠져 있다.
   둘 다 origin/main 에 원래 있던 문장이고 이번 봉인 범위 밖이다. 다른 C 가지(c3b-docs-site · c3-kits · api0 · c4c · c4d · c1b)에서도 같은 grep 이 걸려 고치는 곳이 아직 없다.
   다음 api 카이젠에서 조사 지침을 고치고, 문서 사이트 쪽에서 이 페이지를 다시 만든다
3. tone — `tone-kit/references/adapter-dart-flutter.md:26` 가 가리키는 줄이 실제 정규식 줄과 다르다. 「§4 완료 게이트 G-04 줄」 이라고 적었지만 §4 에서 `G-04` 이름이 붙은 줄(`:259`)은 정규식 없는 표 행이고,
   실제 정규식은 이름 없는 코드 블록 넷째 줄(`:245`)이다. `docs/tone/dart-flutter-idioms.md:633` 은 「넷째 줄」 이라고 맞게 적었다. 다음 tone-kaizen 에서 `:26` 을 같은 말로 맞춘다
4. reflect — `reflect-kit/skills/reflect-digest/SKILL.md:255` · `:315` 의 「엔트리 0 이고 Stop 실패 시도가 1 이상일 때」 는 코드와 조건이 다르다.
   코드는 전체 실패 수 `n` 이 아니라 마지막 기록 · 마지막 정상 종료 뒤의 실패 수 `a` 로 판정한다. 시험 `collect-status-test.sh` 의 「엔트리 0 · 실패 뒤 정상 종료 — 경고 없음」 경우가 증거다(`Stop 실패 시도 1회 … 엔트리 0` 인데 경고 줄이 없다).
   main 에 원래 있던 구절을 이번에 문장을 다시 쓰며 그대로 옮겼다. 다음 reflect-kaizen 에서 「마지막 기록 · 정상 종료 뒤의 실패 시도」 로 고친다
5. reflect — `reflect-kit/hooks/log-reflection.sh:250` 주석이 아직 「`claude -p --model haiku`로 재시도」 다. 실제 호출(`:269`)은 `--safe-mode` 를 쓴다. 다음 reflect-kaizen 에서 주석을 맞춘다
6. QA 개선 제안(ER-02) — bambu 완료 검사가 SKILL.md 안에 박힌 스크립트라 따로 도는 실행 목록이 없다. 이번에는 계약 측정 도우미가 awk 로 떼어 돌렸을 뿐이다.
   evals 시험 파일을 돌리는 스크립트로 올려 CI 목록에 넣을지 다음 bambu-kaizen 에서 정한다
