---
feature: "킷 후속 B — reflect-kit · bambu-kit · tone-kit · api-kit (2026-09-24 카이젠 다음 사이클 메모)"
slug: after-0924-kits-b
created: "2026-09-26 13:47"
complexity: "복잡"
conditions: 27
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:c583ca357d027c78
locked_at: "2026-09-26 14:03"
---

## 배경

2026-09-24 카이젠이 다음 사이클로 넘긴 킷 몫 가운데 네 킷(reflect-kit · bambu-kit · tone-kit · api-kit) 항목을 한 계약으로 묶는다(묶음 c3c).
근거 원문은 본 체크아웃의 `.harness/handoff/2026-09-26-0110.md` §C3(읽기만)과 이 가지의
`.harness/.meta/kaizen-0924/f1-kit-followups-notes.md` · `f2-review-fixes-notes.md` · `final-notes.md` 「다음 사이클 메모」 절, 그리고 이번 세션이 실측한 reflect-kit 결함이다.

- 사용자 합의(Step 5): 사용자 위임으로 받은 것으로 적는다 — user 2026-09-26T01:04:21.505Z 「다음 세션에서 직접할 일을 다 실행하고 이어질것도 실행해」
  (세션 기록 `/Users/jackson/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0.jsonl`),
  그 앞의 「나한테 물어보지 말고 자동으로 끝까지」(2026-09-24T04:04:16.964Z). 판단이 갈린 곳은 저장소 안 근거와 이 맥의 실측으로 정했고 `## 범위 경계` 에 적었다.
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c3c`, 가지 `chore/ak-c3c-kits`, 시작점 `88ddfe5`(origin/main, #112 harness 0.14.1).
- 커밋 규칙: `git add <경로>` 뒤 `git commit -o <경로>` · 한 커밋에 묶음 하나(AR-01 의 묶음 정의) · `.harness/` 파일은 킷과 다른 커밋 · `git add -A` · `git stash` · push · 가지 바꾸기 금지.
- 구현 순서: reflect-kit 을 가장 먼저 한다(수집기가 지금도 기록을 잘못 세고 있다). 이어 bambu-kit · tone-kit · api-kit.
- 구현 전에 `tone-kit:tone-guide` 1 단계(규칙 불러오기)를, 완료 선언 전에 5 단계(전수 대조)를 한다 — 대조 결과는 notes 에 남긴다(AR-02).
- 올리지 않은 가지 `feat/bambu-kit-orca-h2s-feedback` 은 다른 세션 것이다 — 건드리지 않고 충돌 가능 자리만 notes 에 적는다.
- 사용자가 할 일: 없음.

복잡도 4 축 — 넷 다 「예」 이고 공개 약속 변경과 소비자가 함께 있어 「복잡」 이다. Step 2.5 짝 조건: 기록 형식(생산 SC-01 · SC-02 ↔ 소비 SC-03 · SK-01) · 멈춤 문턱(생산 SC-04 ↔ 소비 SK-02) · 대체 경로 인자(생산 SC-05 ↔ 소비 SK-03) · 표 칸 형식(규칙 SK-04 ↔ 적용 SK-04 · SK-05).

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 넷 — 실행 훅과 공용 라이브러리, 킷 시험 스크립트, 스킬 · 참조 문서, 레포 안내 문서(루트 CLAUDE.md · `.claude/skills` · 설계 기록) |
| 공개 API·계약 변경 | 외부에 노출된 약속이 바뀌는가 | 예 — reflections 기록 형식 보장, `⚠ 수집 멈춤` 경고 조건, 대체 경로가 띄우는 훅, tone-kit 슬롯 값 표기 규칙, bambu `[미검증]` 출력 문구 |
| 소비면 존재 | 반대편이 있는가 | 예 — `collect_status` · `/reflect-digest` 4 단계 · reflect-kaizen, README, tone-guide · tone-scaffold 가 읽는 어댑터 표, 번역투 정규식을 옮겨 쓰는 계약들 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 이미 코드 블록인 출력 · 산문 출력 · no issues 경로, 환경 반복 억제, 기존 시험 셋(26 · 14 · 16 경우), bambu 빈 목록 문구 |

설정 값 대조 (`.harness/project.yaml` 을 글자 그대로 옮김):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A — 재는 파일이 바뀐 파일에 없다 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A — 같은 이유 |
| `diagnostics.ide_exclude` | `[]` | DG-02 의 `([] 제외)` |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 같은 넷 |
| `anti_patterns[].id` / `message` | AP-01 버전 하드코딩 · AP-02 force push · AP-03 bare code fence · AP-04 frontmatter name 누락 | AP-03 · AP-04 (바뀌는 파일이 SKILL.md · 코드 블록 있는 MD · frontmatter 가 있는 스킬 설명 줄이라 걸릴 수 있다). AP-01 은 plugin.json 버전을 안 건드려서, AP-02 는 이 계약이 push 하지 않아서 뺐다 |

## GAP 분석 (Pre-Edit Audit)

대상 파일을 읽기만 하고 줄을 적었다. 줄 번호는 시작점 `88ddfe5` 기준이다.

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 여부 |
| --------- | ---------------------------- | ------------------- | ---------------- |
| `reflect-kit/hooks/log-reflection.sh` | `:179-203` 프롬프트가 yaml 코드 블록을 요구 · `:316-321` no issues · `:368` 억제 awk 가 ```` ```yaml ```` 여는 줄만 블록으로 봄 · `:400` 블록 밖 줄은 빈 줄을 지우고 그대로 찍음 · `:429-440` 그대로 append | 분석기가 코드 블록을 빼면 블록 없이 적히고, 빈 줄이 지워져 여러 블록이 한 덩어리가 되며, 억제 awk 가 환경 블록을 못 본다 | SC-01 · SC-02 · ER-01 |
| 같은 파일 | `:250-254` 대체 경로 주석 · `:266` `claude -p --model haiku --no-session-persistence` · `:291-292` 분석기 표식은 reflect-kit 훅만 막는다 · `:318` 「실패 한 번만 보고 멈춤으로 판정」 주석 | 대체 경로가 사용자 · 프로젝트 설정 훅을 띄운다(봉인 전 사본 실측 `marks=4`) | SC-05 · SK-02 |
| `reflect-kit/hooks/_lib-project-id.sh` | `:182` 엔트리 = ```` ```yaml ```` 여는 줄 수 · `:199-207` 마지막 기록 · 정상 종료 뒤 실패 `a` · `:214-218` `a>0` 이면 바로 경고 | 코드 블록 없는 엔트리를 0 으로 센다. 실패 한 번에도 digest `## 승격 후보` 가 빈다 | SC-03 · SC-04 |
| `reflect-kit/evals/hooks/log-reflection-test.sh` | `:33-39` 가짜 codex 출력이 모두 코드 블록 · `:97-99` 대체 경로 인자 확인 | 코드 블록 없는 출력 경우가 0 | SC-06 |
| `reflect-kit/evals/hooks/collect-status-test.sh` | `:125-127` `b4` 한 번 실패 → 경고 기대 · `:130` `b6` 정상 종료 뒤 한 번 실패 → 경고 기대 | 새 문턱에서는 두 기대값이 바뀐다. 옛 엔트리 세기 경우 0 | SC-06 |
| `reflect-kit/skills/reflect-digest/SKILL.md` | `:35` Gotcha #13 「늦은 쪽 뒤에 Stop 실패 시도가 있으면」 · `:84` 블록 형식 · `:121` 4 단계 「`yaml` 코드블록 추출」 · `:254` · `:314` 「1 이상일 때」 | 코드 블록 없는 절을 읽는 법이 없다. 문턱 설명이 옛 조건 | SK-01 · SK-02 |
| `reflect-kit/README.md` | `:84` `.errors.log` 한 줄 설명 · `:99` 대체 경로 `claude -p --model haiku` | `ok:no-issues` 가 없다. 새 인자가 반영돼야 한다 | SK-03 |
| `reflect-kit/docs/SCHEMA.md` · `DESIGN.md` · `skills/reflect-kaizen/SKILL.md` | `SCHEMA.md:11` · `:148` · `DESIGN.md:24` · `:192` · `reflect-kaizen:63` · `:128` | 세는 법 설명(「마지막 기록 뒤」 실패로 센다)과 `⚠` 줄 쓰임새는 새 문턱과 어긋나지 않는다 — 바꾸지 않는다 | 범위 경계 |
| `~/.claude/logs/claude-plugins/reflections-2026-09.md` (이 맥 실제 기록, 읽기만) | 절 머리 `:2` 11:15:26 · `:30` 12:05:14 · `:155` 12:24:26 은 코드 블록 0 · `:58` 12:16:43 은 네 블록 · `reflections-2026-08.md` 는 ```` ```yaml ```` 61 개 | `collect_status 7` 이 `기록된 세션 2 / 엔트리 4` — 코드 블록 없는 세 엔트리를 뺀다 | SC-03 (참고값) |
| `~/.claude/logs/claude-plugins/.errors.log` (읽기만) | 2026-09-26 11:29 ~ 12:13 에 `err=` 없는 `fail:codex-exit-2` 여섯 줄(세션 `f5b7f3a5…` · `d204ea78…`, 재시작 전 옛 판) · 13:06:22 `ok:no-issues` · 전체에 `err=` 0 줄 | 11:15 기록 뒤 옛 판 세션 실패가 한 시간 안에 섞여 경고가 켜졌다 꺼진다. 새 판의 실패 빈도 자료는 아직 없다 | SC-04 (문턱 근거) |
| `~/.claude/settings.json` (읽기만) | SessionStart 둘(그중 `pkill -f 'flutter-playwright-mcp'`) · UserPromptSubmit 넷 · Stop 넷 | 대체 경로가 이 훅들을 띄우면 다른 세션의 화면 도구 서버를 죽이고 알림 · 기록을 남긴다 | SC-05 (근거) |
| `claude --help` (설치본 2.1.268) | `--safe-mode` 「hooks … disabled … Auth … work normally」 · `--bare` 「OAuth and keychain are never read」 | `--bare` 는 로그인 인증을 못 써 대체 경로가 죽는다 — `--safe-mode` 를 고른다 | SC-05 |
| `bambu-kit/skills/bambu-print-profile/SKILL.md` | `:1603-1605` 목록 `[미검증]` 문구 · `:1681-1701` 키 · 종류 · enum 검사 · `:2007-2011` enum 뺀 목록 음성 대조 · `:2034` enum 문단 | enum 줄만 빠져도 「키 존재 · 종류 · enum 값 검사 미실행」 — 같은 실행에서 종류 FAIL 이 나온다(봉인 전 실측) | ER-02 |
| 같은 파일 | `:2234-2239` G-code 길이 재기 문단 · `:2262-2265` M82 · M83 · G90 · G91 처리 | `G91` 이 E 를 상대로 바꾸는지 적힌 곳이 없다. 설치본 시작 G-code 실측으로 영향 0 | SK-07 |
| 설치본 `/Applications/BambuStudio.app` · `OrcaSlicer.app` 의 `profiles/BBL/machine/*H2S*.json` (읽기만) | 뱀부 `…template machine_start_gcode.json` · 오르카 `Bambu Lab H2S 0.4 nozzle.json` 의 `machine_start_gcode` | 뱀부 G91 6 · M82 0 · M83 6 · G91 구간 E 0, 오르카 G91 5 · M82 0 · M83 6 · G91 구간 E 0 | SK-07 (근거) |
| 가지 `feat/bambu-kit-orca-h2s-feedback` (읽기만) | `baa1a38` 기준 hunk `@@ -1401,4 +1441,6 @@` — `META =` 줄과 그 아래 두 줄 | 이 계약이 고칠 `:1603-1605` 과 그 가지가 고친 `META =` 줄 사이가 주석 한 줄뿐이다 | 넘김 (notes) |
| `tone-kit/references/adapter-dart-flutter.md` | `:26` `fallback_identifier_pattern` 칸 `\b(effective\|resolved)[A-Z]` · `:245` 실행 줄 · `:259` G-04 행 | 표 칸 정규식을 그대로 넣으면 0 건(봉인 전 실측 bash · zsh 둘 다) | SK-04 |
| `tone-kit/references/adapter-contract.md` | `:36` 슬롯 타입 「정규식」 · `:43-47` 슬롯 작성 규칙 | 표 칸의 `\|` 에 대한 규칙이 없다 | SK-04 |
| `docs/tone/dart-flutter-idioms.md` | `:633` 같은 칸 · `:646` 실행 줄 · `:662` 판정표 4 행 | 어댑터와 같은 결함 | SK-04 |
| `tone-kit/references/locale-korean.md` | `:58-69` §2 표(grep 열 여섯 칸 중 다섯에 `\|`) · `:155` §8 G-1 실행 줄 · `:174` §9 | grep 열을 붙여 넣으면 죽는다. 실행은 §8 이 한다(`phase15-notes.md:135` 권고 「§8 을 가리키게 한다」) | SK-05 |
| 루트 `CLAUDE.md` · `tone-kit/README.md` · `.claude/skills/tone-research/SKILL.md` · `.claude/skills/tone-kaizen/SKILL.md` | `CLAUDE.md:294` · `README.md:88` · `tone-research:4` · `:85` · `tone-kaizen:35` · `:100` | 「8종」 다섯 줄에 셈 기준이 없다. `tone-kaizen:35` 만 「11종 (리서치 문서 8종 + overview · research-log · templates)」. 실제 `.md` 11 · 셋 뺀 주제 문서 8 · 페이지 `docs/tone-kit/` 주제 8 | SK-06 |
| `docs/superpowers/specs/2026-09-02-api-kit-design.md` | `:249` · `:251` 「표현되지 않는다」 · 「쓸 수 없다」 · `:254` 결론 · `:280` `### 10.1 사실 정정` 선례 | 이유가 틀렸다. 근거 `docs/api/research-log.md:161-175` · `api-kit/skills/api-verify/SKILL.md:133` | SK-08 |
| `.claude/skills/kaizen-orchestrator/SKILL.md` | `:574` 이미 「적을 수 있지만 … 후처리뿐」 | 이미 고쳐져 있다 — 바꾸지 않는다 | 범위 경계 |

## Skill

- [ ] SK-01: reflect-digest 4 단계가 코드 블록 없는 옛 엔트리를 읽는 법을 적는다 — Given 정규화 전 0.8.0 훅이 남긴 절(`## <시각>` 아래 yaml 코드 블록이 하나도 없고 `primary_category:` 줄이 있는 절, 이 맥 실제 기록 `reflections-2026-09.md` 의 세 절), When digest 4 단계(엔트리 파싱)를 따르면, Then 그 절을 버리거나 파싱 실패로 세지 않고 `primary_category:` 줄마다 블록 하나로 읽는다. 4 단계 절(`4. **엔트리 파싱**` 로 시작하는 줄부터 `5. **actionability` 로 시작하는 줄 앞까지)에 `코드 블록` 과 `primary_category:` 를 함께 담은 줄이 1 이상이다 — `코드 블록` 은 띄어쓰기 유무를 가리지 않는다(같은 절 121 행이 쓰는 붙여쓰기 `코드블록` 도 받는다). 측정: `m SK-01` 이 `legacy_line=x` 이고 x≥1 (시작 판 `legacy_line=0` — 121 행은 `primary_category:` 가 없어 붙여쓰기를 받아도 0 이다) [exact, collective]
- [ ] SK-02: 수집 멈춤 문턱을 설명하는 자리가 SC-04 의 문턱과 같은 말을 한다 — digest Gotcha #13 · 요약 머리의 `⚠ 수집 멈춤` 줄 조건 · 필수 섹션 머리 문단 세 자리가 「3 회 이상」 과 「1 일 이상」 을 한 줄에 담고, 옛 문구 「늦은 쪽 뒤에 Stop 실패 시도가 있으면」 · 「마지막 기록 뒤 Stop 실패 시도가 1 이상일 때」 가 0 이며, 훅 정상 종료 주석의 옛 이유 「실패 한 번만 보고 멈춤으로 판정」 이 0 이다. 측정: `m SK-02` 가 `old13=0 old_rule=0 new=n hook_old=0` 이고 n≥3 (시작 판 `old13=1 old_rule=2 new=0 hook_old=1`) [exact, enumerated]
- [ ] SK-03: reflect-kit README 가 `.errors.log` 정상 종료 줄과 대체 경로 새 인자를 적는다 — `## 로그 경로` 블록의 `.errors.log` 줄(주석 `#` 이 있는 줄)에 `ok:no-issues` 가 있고, `## 의존성` 의 `claude -p` 줄에 `--safe-mode` 가 있다. 측정: `m SK-03` 이 `errors_ok=1 fallback_safe=1` (시작 판 `errors_ok=0 fallback_safe=0`) [exact, enumerated]
- [ ] SK-04: tone-kit 표 칸에 `|` 가 든 정규식을 싣지 않는 규칙을 정하고 두 칸에 적용한다 — 슬롯 형식 정본 `adapter-contract.md` 의 `### 슬롯 작성 규칙` 절에 글자 `\|` 와 `0 건` 을 함께 담은 규칙 줄(표 칸에 `\|` 로 적힌 정규식을 그대로 grep 에 넣으면 0 건이라 실행 블록 줄을 가리킨다는 뜻)이 1 이상이고, `fallback_identifier_pattern` 표 줄 두 곳(어댑터 §1 · 연구 문서 슬롯 표)에 `\|` 가 0 이며, 두 줄 모두 `effective` · `resolved` 를 담고 실행 줄을 가리킨다 — 어댑터 줄은 `G-04`, 연구 문서 줄은 `audit_greps`. 실행 줄 `grep -rnE '\b(effective|resolved)[A-Z]' --include='*.dart' <src>` 는 두 파일에 각 1 줄 그대로다. `codegen_cmd` 칸의 `<dart\|flutter>` 는 정규식이 아니라 명령 형태라 이 규칙 밖이다. 측정: `m SK-04` 가 `rule=r ad_pipe=0 ad_ptr=1 id_pipe=0 id_ptr=1 ad_run=1 id_run=1` 이고 r≥1 (시작 판 `rule=0 ad_pipe=1 ad_ptr=0 id_pipe=1 id_ptr=0 ad_run=1 id_run=1`). 양성 대조: `final effectiveColor = c;` 한 줄 `.dart` 파일에 시작 판 칸 글자 그대로의 정규식은 bash · zsh 모두 0 줄, 실행 줄 형태는 1 줄 (봉인 전 실측) [exact, enumerated]
- [ ] SK-05: locale-korean §2 치환표의 grep 열이 정규식 대신 §8 실행 줄의 갈래를 가리킨다 — §2 표 여섯 행의 셋째 칸이 행 순서대로 `§8 G-1 갈래 1` ~ `§8 G-1 갈래 6` 을 담고 `\|` 는 0 이며, §8 의 G-1 실행 줄은 글자 그대로 1 줄이고, 그 정규식의 맨 바깥 갈래 수가 6 이라 행과 짝이 맞는다(갈래 순서 = 행 순서, 봉인 전 실측). 측정: `m SK-05` 가 `rows=6 pointer_ok=6 pipe_rows=0 g1_line=1 g1_alts=6` (시작 판 `rows=6 pointer_ok=0 pipe_rows=5 g1_line=1 g1_alts=6`) [exact, enumerated]
- [ ] SK-06: `docs/tone/` 「8종」 표기가 셈 기준을 함께 적는다 — 셈 기준은 tone-kaizen 이 이미 쓰는 것(리서치 문서 = `docs/tone/*.md` 에서 overview · research-log · templates 를 뺀 주제 문서)이다. 네 파일(루트 CLAUDE.md · tone-kit README · tone-research 스킬 · tone-kaizen 스킬)에서 `8종` 이 든 줄 여섯이 모두 `overview` · `research-log` · `templates` 를 담고, tone-kaizen 의 「`docs/tone/*.md` 11종」 줄은 글자 그대로이며, 주제 문서 수가 실제로 8 이다. 측정: `m SK-06` 이 `lines_8=6 missing_basis=0 k35=1 research_docs=8` (시작 판 `lines_8=6 missing_basis=5 k35=1 research_docs=8`) [exact, enumerated]
- [ ] SK-07: bambu 「G-code 로 길이 재기」 문단이 `G91` 해석을 실측으로 적고 측정 코드는 그대로 둔다 — 그 문단(그 제목 줄부터 `### Phase 5` 앞까지)에 `G91` · `M83` · `M82` · 설치본 뱀부 판 `02.08.02.61` · 오르카 판 `2.4.2` 를 함께 담은 줄이 1 이상이고, 측정 블록(`python3 - "<G-code 경로>"` 줄부터 `PY` 까지)은 시작 판과 글자 하나 다르지 않다. 그 줄이 옮기는 값은 설치본 H2S 시작 G-code 실측과 같다 — 뱀부 `G91=6 M82=0 M83=6 G91_E=0` · 오르카 `G91=5 M82=0 M83=6 G91_E=0` (G91 구간 안 E 이동이 없고 E 모드가 M83 뿐이라 G91 이 E 까지 상대로 바꾸는지와 무관하게 길이가 같다). Given 설치본 판이 이 두 판 그대로. 측정: `m SK-07` 이 `note=x block_same=1 | bambu G91=6 M82=0 M83=6 G91_E=0 orca G91=5 M82=0 M83=6 G91_E=0` 이고 x≥1 (시작 판 `note=0 block_same=1 |` 같은 수치). 설치본 뱀부 · 오르카 가운데 하나라도 없으면 도우미가 `뱀부 · 오르카 설치본 없음` 만 내고 멈춘다 — 그때는 `[미검증]` 1 건으로 받는다(ER-02 와 같은 가드) [exact, enumerated]
- [ ] SK-08: api-kit 설계 기록의 「경로 간 불변식은 Hurl assert 로 표현되지 않는다」 를 날짜 붙은 정정으로 바로잡는다 — `### 9.2` 절 안에서 「표현되지 않는다」 · 「쓸 수 없다」 를 담은 줄은 모두 `정정` 을 함께 담고(옛 기록은 지우지 않고 정정 표시를 단다 — 같은 문서 `### 10.1 사실 정정` 이 선례), 절 안의 정정 문단이 `capture` · `종료 코드` · `판정 불가` · `research-log.md` 를 담는다(근거 `docs/api/research-log.md:161-175`, hurl 8.0.1 실측 2026-09-24). 결론 「**후처리 단계에서 검사**」 는 1 그대로이고, 이 파일에서 바뀐 줄은 모두 `### 9.2` 절 안이다. 측정: `m SK-08` 이 `unqualified=0 jeongjeong=j exit3=a undecided=b log=c capture=d post=1 out_of_92=0` 이고 j · a · b · c · d 모두 ≥1 (시작 판 `unqualified=2 jeongjeong=0 exit3=0 undecided=0 log=0 capture=0 post=1 out_of_92=0`). 양성 대조: 임시 복제본에서 문서 맨 앞에 한 줄을 넣으면 `out_of_92=1` (봉인 전 실측) [exact, enumerated]

## Script

- [ ] SC-01: Stop 훅이 코드 블록 없는 분석기 출력을 적기 전에 yaml 코드 블록으로 감싼다 — Given 가짜 codex 가 돌려준 네 모양(코드 블록 없는 한 블록 `nf1` · 빈 줄로 나뉜 코드 블록 없는 두 블록 `nf2` · 언어 없는 fence 로 싼 한 블록 `bare` · 이미 yaml 코드 블록인 한 블록 `fenced`), When 훅을 `--background` 로 한 번씩 돌리면, Then 적힌 기록의 「yaml 여는 줄 / 맨 fence 줄 / 코드 블록 안 `primary_category:` 줄 / `collect_status` 엔트리」 가 `nf1=1/1/1/1 nf2=2/2/2/2 bare=1/1/1/1 fenced=1/1/1/1` 이다. 기대값은 블록 수에서 손으로 정했다(구현이 낸 값을 옮긴 것이 아니다). 분석기에게 형식을 더 세게 요구하는 것만으로는 이 조건을 못 채운다 — 가짜 codex 는 지시와 무관하게 같은 출력을 낸다. 측정: `m SC-01` (시작 판 `nf1=0/0/0/0 nf2=0/0/0/0 bare=0/2/0/0 fenced=1/1/1/1`). 음성 대조: 정규화가 없는 시작 판 훅이 그 시작 판 값이다 — 앞 셋이 어긋나고 `fenced` 는 이미 맞는 출력을 건드리지 않는지 본다. 예행: 정규화 원형을 넣은 사본에서 기대값이 그대로 나왔다 [exact, enumerated]
- [ ] SC-02: 환경 반복 억제가 코드 블록 없는 블록도 본다 — Given 코드 블록 없는 `actionability: user_environment` 블록(태그 `fix-env-repeat-tag`)을 같은 로그 폴더에 두 세션(E1 · E2)이 차례로 남기면, Then 첫 세션만 기록되고 둘째는 `skip:env-dedup-all` 한 줄로 억제되며 `.env-issues.tsv` 의 그 태그 count 가 2 다. 측정: `m SC-02` 가 `e1=1 e2=0 dedup_all=1 tsv=2` (시작 판 `e1=1 e2=1 dedup_all=0 tsv=0` — 억제 awk 가 블록을 못 봐 둘 다 적었다) [exact, enumerated]
- [ ] SC-03: `collect_status` 가 코드 블록 없는 옛 엔트리를 센다 — Given 한 폴더에 코드 블록 없이 `primary_category:` 줄 둘이 빈 줄 없이 붙은 절(0.8.0 훅이 빈 줄까지 지워 남긴 모양) 하나와 yaml 코드 블록 하나짜리 절 하나, When `collect_status 7` 을 돌리면, Then `기록된 세션 2 / 엔트리 3` 이다(코드 블록 안의 `primary_category:` 는 두 번 세지 않는다). 측정: `m SC-03` (시작 판 `기록된 세션 2 / 엔트리 1`). 이 맥 실제 기록은 지금 `collect_status 7` 이 `기록된 세션 2 / 엔트리 4` 로 코드 블록 없는 세 절을 빼고 센다 — 실제 기록은 세션이 끝날 때마다 늘어 조건 값으로 잠그지 않는다 [exact, enumerated]
- [ ] SC-04: 수집 멈춤 경고에 문턱을 둔다 — 엔트리가 있는 기간의 `⚠ 수집 멈춤 — 마지막 기록 뒤 Stop 실패 시도 N회` 줄은 (1) 마지막 기록 · 마지막 정상 종료 가운데 늦은 쪽 뒤의 실패 시도가 3 회 이상이고 (2) 그 가운데 첫 실패가 지금보다 1 일(24 시간) 이상 앞설 때만 나온다. 엔트리 0 경고(`⚠ 수집 멈춤 — 엔트리 0은 문제 없음이 아니다`)의 규칙은 그대로다. Given 경우 여섯 — `old3`(기록 3 일 전 · 실패 3 번 2 일 전 → 경고) · `recent3`(기록 2 시간 전 · 실패 3 번 1 시간 전 → 없음) · `idle3`(기록 3 일 전 · 실패 3 번 1 시간 전 → 없음, 문턱 (2) 를 마지막 기록 나이가 아니라 첫 실패 나이로 재는지 가른다) · `old2`(기록 3 일 전 · 실패 2 번 2 일 전 → 없음) · `old1`(기록 2 일 전 · 실패 1 번 25 시간 전 → 없음) · `zero`(기록 없음 · 실패 1 번 1 시간 전 → 엔트리 0 경고), When `collect_status 7`, Then 경고 줄 수가 `old3=1 recent3=0 idle3=0 old2=0 old1=0 zero=1` 이다(`old3` 은 줄 글자 그대로 `⚠ 수집 멈춤 — 마지막 기록 뒤 Stop 실패 시도 3회`). 측정: `m SC-04` (시작 판 `old3=1 recent3=1 idle3=1 old2=1 old1=1 zero=1` — 가운데 넷이 양성 대조) [exact, enumerated]
- [ ] SC-05: 대체 경로 `claude -p` 가 사용자 · 프로젝트 설정의 훅을 띄우지 않는다 — Given 훅의 대체 경로 호출 줄, When 가짜 codex 가 실패해 가짜 claude 가 불리면, Then 인자에 `--safe-mode` · `--model haiku` · `--no-session-persistence` 가 각 1 이고(호출 줄은 지금처럼 `REFLECT_KIT_ANALYZER=1 claude -p` 로 시작한다 — 도우미가 이 줄에서 인자를 읽는다), 같은 인자를 실제 `claude` 로 표식 훅만 든 사본 설정(`CLAUDE_CONFIG_DIR` 사본 + 작업 폴더 `.claude/settings.json`)에서 띄우면 표식이 0 이다. 봉인 전 실측: 시작 판 인자로는 SessionStart · UserPromptSubmit 표식 넷이 적히고(로그인 안 된 사본이라 모델 호출 없이 끝난다), `--safe-mode` 를 더하면 0 이며, 실제 로그인 환경에서 `-p --safe-mode --setting-sources local --model haiku --no-session-persistence` 는 종료 코드 0 · 출력 `ok` 다(인증을 막지 않는다). 측정: `m SC-05` 가 `safe=1 model=1 nosess=1 | tip args=[…--safe-mode…] marks=0 | base args=[-p --model haiku --no-session-persistence] marks=4` (시작 판 `safe=0 model=1 nosess=1 | tip … marks=4 | base … marks=4`). `claude` 가 없으면 그 칸이 `claude-없음` 이고 `[미검증]` 1 건으로 받는다 [exact, enumerated]
- [ ] SC-06: reflect-kit 시험 둘이 새 경우를 담고, 시작 판 훅 · 라이브러리로 돌리면 어긋난다 — `log-reflection-test.sh` 에 다섯 경우(코드 블록 없는 한 블록 · 두 블록 · 언어 없는 fence · 코드 블록 없는 환경 블록 반복 억제 · 대체 경로 `--safe-mode` 인자), `collect-status-test.sh` 에 네 경우(코드 블록 없는 옛 엔트리 세기 · 문턱 넘는 멈춤 · 실패 수 모자람 · 1 일 안 됨)를 더하고, 기존 두 경우(`b4` 기록 뒤 한 번 실패 · `b6` 정상 종료 뒤 한 번 실패)의 기대값을 새 문턱에 맞춘다. 측정: `m SC-06` 이 세 시험 모두 `rc=0` · `불일치 0` 이고 경우 수가 log-reflection ≥31 · collect-status ≥18 · project-id 16 이며, `base_hooks` 줄의 불일치 ≥4 · `base_lib` 줄의 불일치 ≥3 이다 (시작 판 `26 · 14 · 16` 과 `base_hooks … 불일치 0` · `base_lib … 불일치 0`). 음성 대조: 그 두 base 줄 자체다 — 새 경우가 구현을 부르지 않으면 불일치가 0 으로 남는다. 예행: 새 경우 일부만 넣은 사본에서 `base_hooks 불일치 3` · `base_lib 불일치 3` [exact, enumerated]

## Error

- [ ] ER-01: 형식을 전혀 안 따른 분석기 출력은 버리지 않고 블록을 지어내지 않는다 — Given 코드 블록도 `primary_category:` 줄도 없는 산문 두 줄, When 훅이 적으면, Then 그 세션이 기록되고 산문 줄이 남으며 yaml 여는 줄은 0 이다(행동 신호를 잃지 않는다는 억제 게이트의 원칙 `log-reflection.sh:331-332` 와 같은 쪽). 측정: `m ER-01` 이 `recorded=1 prose=1 yaml=0` (시작 판 같은 값 — 바꾸면 안 되는 동작이다. yaml 여는 줄을 세는 식이 살아 있다는 양성 대조는 SC-01 의 `nf1` 이 1 을 내는 것) [exact, enumerated]
- [ ] ER-02: bambu 완료 검사의 목록 `[미검증]` 문구가 실제로 안 돈 검사만 적는다 — Given 설치본 뱀부 옵션 목록에서 enum 줄만 뺀 목록, When `process-seam-slope-type-invalid.json` 을 검사하면, Then 목록 `[미검증]` 줄이 `enum 값 검사 미실행` 을 담고 `키 존재` 는 담지 않으며 결과는 지금처럼 `RESULT: PASS` · 종료 코드 0 이다. 같은 목록으로 `process-machine-scope-key.json` 을 검사하면 종류 검사가 실제로 돌아 `키 스코프 불일치` FAIL 이 나오므로 그 `[미검증]` 줄도 `키 존재` 를 담지 않는다. 빈 목록 파일이면 지금처럼 `키 존재 · 종류 · enum 값 검사 미실행` 이다. 측정: `m ER-02` 가 `noenum=1/0/0/1 empty=1 scope=1/0` (시작 판 `noenum=1/1/0/1 empty=1 scope=1/1` — 종류 FAIL 과 「종류 검사 미실행」 이 한 출력에 같이 나온다) [exact, enumerated]

## Architecture

- [ ] AR-01: 바뀐 파일이 기대 집합 안이고 한 커밋에 묶음 하나다 — Given 구현 · notes · QA 리포트 커밋이 모두 가지 `chore/ak-c3c-kits` 에 들어간 뒤, 시작점 `BASE=$(git -C W merge-base origin/main chore/ak-c3c-kits)` 부터 끝점 `TIP=$(git -C W rev-parse --verify chore/ak-c3c-kits)` 까지(`HEAD` 를 쓰지 않는다. 해석이 안 되면 `UNRESOLVED` 로 멈춘다) `git diff --name-only` 로 모은 경로가 측정 도우미 `ALLOWED` 의 열아홉 경로와 notes 폴더 접두(`.harness/.meta/after-kaizen-0926/c3c-`) 안에만 있고(부분 집합, 생성물 제외 없음 — 이 묶음은 생성물을 만들지 않는다), 네 묶음(reflect · bambu · tone · api)이 각 1 경로 이상이며, 커밋마다 묶음이 하나뿐이다 — 묶음 정의는 도우미 `group()` 한 곳(tone 묶음 = tone-kit · docs/tone · 루트 CLAUDE.md · tone 쪽 `.claude/skills` 두 폴더, api 묶음 = 설계 기록 한 파일). 측정: `m AR-01` 이 extra=0 · 네 묶음 값 ≥1 · multi_group=0 (시작 판 `changed=0 extra=0` 네 묶음 0 `multi_group=0`). 양성 대조: 임시 복제본에서 두 묶음과 범위 밖 `scripts/stray.txt` 를 한 커밋에 넣으면 `extra=1` · `multi_group=1` 이고 남는 경로를 출력한다 (봉인 전 실측) [exact, collective]
- [ ] AR-02: 결정과 넘김을 notes 에 남긴다 — Given 끝점 `TIP`, notes 파일 `.harness/.meta/after-kaizen-0926/c3c-notes.md` 가 커밋돼 있고 열여섯 토큰(`--safe-mode` · `marks=` · `3 회` · `1 일` · `feat/bambu-kit-orca-h2s-feedback` · `G91` · `종류 줄` · `overview` · `docs/api` · `kaizen-orchestrator` · `noncharacter` · `reflections-2026-09.md` · `tone-guide` · `docs/tone-kit/dart-flutter-idioms.html` · `docs/bambu-kit/bambu-print-profile.html` · `넘김`)이 각 1 줄 이상이다. 담을 내용: 결정과 근거(대체 경로 `--safe-mode` 와 사본 실측 `marks=` 값 · 문턱 3 회 · 1 일 · G91 은 코드를 안 바꾼다 · 셈 기준 overview · research-log · templates 제외 · `docs/api` 12종도 같은 기준으로 맞아 안 고친다 · 표 칸 형식), 넘긴 것과 사유(bambu 종류 줄만 빠진 목록의 거짓 FAIL · 그 가지와 충돌 가능 자리 · api-verify `noncharacter` · `-0` 분류 이름 · `kaizen-orchestrator` `:574` 는 이미 고쳐짐 · 이 맥 `reflections-2026-09.md` 의 옛 세 절은 옮기지 않음), tone-guide 5 단계 대조 결과, 원본이 바뀌어 다시 만들 문서 페이지 둘(문서 사이트는 범위 밖). 측정: `m AR-02` 가 `committed=1` 과 1 이상 열여섯 (시작 판 `committed=0` 과 0 열여섯). 양성 대조: 임시 복제본에 열여섯 토큰을 담은 notes 를 커밋하면 `committed=1` 과 1 열여섯 (봉인 전 실측) [exact, enumerated]

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 측정: `m AP-03` 이 `v6_rc=0 bare_changed=0` — V6 은 킷 폴더의 SKILL.md · agents · references · README 만 보므로, 바뀐 `.md` 전부를 같은 상태기계를 옮긴 `v6_bare` 로 따로 센다(킷 밖 다섯 파일 — 연구 문서 · 설계 기록 · 루트 CLAUDE.md · tone 쪽 스킬 둘 — 이 여기서만 잡힌다. 시작 판 `v6_rc=0 bare_changed=0`). 양성 대조: 임시 사본의 tone-kit `locale-korean.md` 끝에 언어 없는 fence 를 붙이면 `v6_rc=2`, tone-research 스킬 끝에 붙이면 `v6_bare` 가 1 (봉인 전 실측)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL. 측정: `m AP-04` 가 `v1_rc=0 tone_names=1 1` — V1 은 킷 스킬만 보므로 설명 줄을 고치는 tone 쪽 `.claude/skills` 두 파일은 첫 frontmatter 블록의 `name:` 줄을 따로 센다 (시작 판 같은 값). 양성 대조: 임시 사본 reflect-digest 에서 `name:` 줄을 지우면 `누락 필드 ['name']` · `v1_rc=2`, tone-research 에서 지우면 그 칸이 0 (봉인 전 실측)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 — 엔트리 세는 규칙은 digest · kaizen 이 같이 부르는 공용 `collect_status` 한 곳에만 두고, 훅 · 시험 스크립트에 사본을 두지 않으며 새 파일을 만들지 않는다. 측정: `m RE-01` 이 `added=0 cs_defs=1 cs_file=reflect-kit/hooks/_lib-project-id.sh` (시작 판 같은 값)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 새 시험 파일 없이 기존 두 시험 스크립트에 경우를 더하고(reflect-kit/evals 파일 수가 시작 판과 같다), 억제 게이트는 태그 줄 패턴을 라이브러리 `tag_canon_awk_re` 에서 계속 받으며 태그 필드 이름 글자를 훅 코드(주석 밖)에 새로 박지 않는다(`log-reflection.sh:97-99` 「같은 상수에서 나와야 한다」). 측정: `m RE-02` 가 `tests=3/3 awk_re=a tag_literal=0` 이고 a≥1 (시작 판 `tests=3/3 awk_re=1 tag_literal=0`)

## Diagnostics

- [ ] DG-01: N/A (commands.analyze `bash -n scripts/release.sh` 가 재는 `scripts/release.sh` 는 이번 바뀐 파일에 없다. 측정: `git -C W diff --name-only BASE TIP | grep -cx 'scripts/release.sh'` 가 0)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — 편집기 진단을 명령줄로 같게 잰다: 바뀐 `.md`(계약 · QA 리포트 · 개정 파일 제외)의 더해진 줄에 걸린 markdownlint-cli2 0.23.2(MD013 끔, 편집기 확장과 같은 설정) 경고 0 · 바뀐 `.sh` 전체의 shellcheck 경고 0(시작 판 네 파일 모두 0). 측정: `m DG-02` 가 `md_new=0 sh_all=0` (도구가 없으면 도우미 `mdl_ready` 가 임시 폴더에 설치한다). 양성 대조: 임시 복제본에 `#bad heading` 줄 · 문서 맨 앞 제목 아닌 줄 · `echo $UNQUOTED_X` 줄을 넣으면 `md_new=2 sh_all=1` (봉인 전 실측 — 이 측정은 `comm` 앞 정렬을 글자 순으로 한다. 숫자 순이면 자릿수가 다른 줄 번호가 섞일 때 겹침이 0 으로 떨어진다)
- [ ] DG-03: N/A (commands.test `bash scripts/release.sh 2>&1 || true` 가 재는 `scripts/release.sh` 는 이번 바뀐 파일에 없다. 측정: DG-01 과 같은 명령이 0)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 바뀐 실행 파일은 Stop 훅과 그 라이브러리뿐이고 SC-01 ~ SC-06 · ER-01 이 가짜 분석기로 실제로 돌린다. 설치본 교체와 실제 세션 확인은 릴리스 단계 몫)
- [ ] DG-05: CI(자동 검사) 단계를 로컬에서 전부 돌려 통과한다 — Given 작업 폴더 W 가 끝점과 같다(`git -C W rev-parse HEAD` 가 `TIP` 이고 `git -C W status --porcelain --untracked-files=no` 가 빈 출력), When `TMPDIR=<임시 폴더> bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c3c` 를 돌리면, Then 요약(`$TMPDIR/ci-local/summary.txt`)에 `rc=0` 줄이 22 개이고 `rc=0` 이 아닌 줄은 `feedback-agg-test SKIP (yq 없음)` 하나뿐이다. 측정: `grep -c 'rc=0' "$TMPDIR/ci-local/summary.txt"` 가 22 · `grep -v 'rc=0' "$TMPDIR/ci-local/summary.txt"` 가 그 한 줄 (시작 판 봉인 전 실측: 22 · SKIP 한 줄). 이 도구는 본 체크아웃의 추적 안 된 파일이다(읽기만) — 돌리기 전에 `shasum -a 256` 이 봉인 전 실측값 `a415eaff98a46b86636e591e650950be12499307ff5720936076b85731119713` 과 같은지 보고, 파일이 없거나 값이 다르면 돌리지 말고 `[미검증]` 1 건으로 받는다(다른 세션이 고친 도구로 잰 값은 이 조건의 근거가 아니다). 음성 대조: 이 묶음이 기대는 `reflect-log-test` · `reflect-collect-test` 단계는 SC-06 의 base 두 줄이 보여 주듯 구현을 되돌리면 실패한다

## 범위 경계

항목별 처리 — 입력은 과제 목록의 네 킷 줄과 핸드오프 §C3 의 같은 줄이다.

| 킷 | 항목 | 처리 | 조건 · 사유 |
| --- | --- | --- | --- |
| reflect-kit | 코드 블록 없는 분석기 출력(이번 세션 실측 결함) | 계약에 넣음 | SC-01 · SC-02 · ER-01 · SC-06. 훅이 적기 전에 정규화한다. 프롬프트를 더 세게 쓰는 것은 막지 않지만 그것만으로는 SC-01 을 못 채운다 |
| reflect-kit | 옛 엔트리를 읽는 쪽 — `collect_status` · digest 4 단계 | 계약에 넣음 | SC-03 · SK-01. 이 맥 기록에 코드 블록 없는 세 절이 이미 있고, digest Gotcha #9 「파싱 실패를 조용히 넘기지 마라」 가 조용한 누락을 막으라 한다. 실제 기록 파일을 고쳐 옮기지는 않는다(사용자 데이터) |
| reflect-kit | 수집 멈춤 경고 문턱(몇 회 · 며칠) | 계약에 넣음 — 결정은 「3 회 이상 · 첫 실패 1 일 이상」 | SC-04 · SK-02. 근거: digest 는 `⚠` 한 줄이면 `## 승격 후보` 를 비운다(Gotcha #13). 2026-09-14~23 멈춤은 9 일 849 번으로 두 문턱을 첫날 넘는다. 2026-09-26 11:15 ~ 12:16 실제 기록은 새 판이 기록하는 동안 옛 판 세션 둘이 한 시간 안에 실패 여섯 줄을 남겼다 — 횟수만 보면 켜지고 1 일 문턱이면 꺼진다. 새 판의 일시 실패 빈도는 `err=` 줄이 아직 0 이라 모른다 — 숫자를 바꿀 근거가 생기면 다음 사이클에 고친다. 엔트리 0 경고는 그대로(엔트리가 없으면 비울 후보도 없다) |
| reflect-kit | `claude -p` 대체 경로가 사용자 훅을 띄우는지 사본 실측 | 계약에 넣음 — 결과 「띄운다」, 결정 `--safe-mode` | SC-05 · SK-03. `--bare` 는 로그인 인증을 안 읽어(`claude --help`) 대체 경로가 죽는다. `--setting-sources` 는 플러그인 훅까지 끄는지 따로 재야 해서 고르지 않았다 |
| reflect-kit | README `.errors.log` 설명에 `ok:no-issues` | 계약에 넣음 | SK-03 |
| bambu-kit | enum 줄만 빠진 목록의 `[미검증]` 문구 | 계약에 넣음 | ER-02. 종류 줄만 빠진 목록은 모든 키가 거짓 「키 스코프 불일치」 FAIL 을 낸다(봉인 전 실측) — 판정 동작을 바꾸는 일이라 넘김(notes) |
| bambu-kit | `G91` 뒤 E 상대값 | 계약에 넣음 — 결정은 「코드는 그대로, 실측을 문단에 적는다」 | SK-07. 설치본 시작 G-code 두 판 모두 G91 구간 E 이동 0 · E 모드 M83 뿐이다. 펌웨어가 G91 을 E 에도 적용하는지는 저장소 밖 원문이 있어야 정할 수 있어 코드 변경은 넘김 |
| bambu-kit | 가지 `feat/bambu-kit-orca-h2s-feedback` 충돌 | 넘김 — notes 에 자리만 | AR-02. 그 가지는 `baa1a38`(v0.9.2) 기준이라 그 뒤 main 변경 전부와 부딪힌다. 이 계약 몫은 목록 `[미검증]` 줄(`META =` 줄과 주석 한 줄 사이)과 G-code 문단(그 가지 기준 뒤에 생긴 문단) |
| tone-kit | `adapter-dart-flutter.md:26` · `docs/tone/dart-flutter-idioms.md:633` 표 칸 정규식 형식 | 계약에 넣음 — 결정은 「표 칸에는 `\|` 정규식을 싣지 않고 실행 줄을 가리킨다」 | SK-04. 근거: `adapter-contract.md:45` 「정규식은 실행 검증한 것만 싣는다」, P15 이 같은 결함을 `core-naming` 표에서 이 방식으로 고쳤다(`sprint-contract-kaizen-0924-p15-tone-kit.md:600`) |
| tone-kit | `locale-korean.md` §2 grep 열 | 계약에 넣음 — 열은 두고 §8 G-1 갈래를 가리킨다 | SK-05. 열을 없애면 옛 계약들의 「§2 grep 열」 인용이 끊긴다(`sprint-contract-kaizen-0924-f1-kit-followups.md:330`) |
| tone-kit | 「리서치 문서 N종」 셈 기준 | 계약에 넣음 — 기준은 tone-kaizen `:35` 가 쓰는 것 | SK-06. 과제가 적은 자리(루트 CLAUDE.md · tone-kaizen `:35` · `:100` · tone-research 설명 줄)에 같은 킷의 README `:88` 과 tone-research `:85` 를 더했다 — 같은 수가 적힌 자리를 전부 맞춘다. `:35` 는 이미 기준을 적고 있어 글자 그대로 둔다. `docs/api` 12종은 같은 기준(research-log 제외 13 − 1)으로 맞아 고치지 않는다 |
| api-kit | 설계 기록 `2026-09-02-api-kit-design.md:249` | 계약에 넣음 | SK-08. 오케스트레이터 `:574` 는 이미 고쳐져 있다 |
| api-kit | api-verify 목록 `noncharacter` · `-0` 분류 이름 | 넘김 | 외부 원문이 먼저라 부모가 따로 한다(과제 지시) |

범위 밖(이 계약이 고치지 않는다): api-kit 뷰어 「판정 불가」 칸 · reviewer 에이전트 미검증 규칙 · rust-kit · `docs/` HTML 페이지(다시 만들 둘은 notes 에 적어 문서 사이트 묶음으로 넘긴다 — `docs/reflect-kit/` 페이지는 원본 `SCHEMA.md` · `DESIGN.md` 가 안 바뀌어 대상 없음) · `scripts/` · `harness/` · `.claude/`(tone 쪽 두 스킬의 「8종」 줄만 예외) · 킷 `plugin.json` 버전(릴리스 단계 몫) · reflect-kit `docs/SCHEMA.md` · `DESIGN.md` · reflect-kaizen(세는 법 설명과 `⚠` 줄 쓰임새가 새 문턱과 어긋나지 않는다).

커버리지 해소 — Step 6.5 (4) 검출기가 낸 `UNCOVERED` 여섯 건과 AR-01 의 처리:

- 커버리지 해소: AR-01 — 경로 기대 집합은 측정 도우미 `ALLOWED` 한 곳에만 적는다(목록을 두 번 적지 않는다는 계약 형식 규칙)
- 커버리지 해소: SK-03 — `.errors.log` 는 `m SK-03` 이 README 에서 고르는 줄의 글자다(`grep -F '.errors.log'`)
- 커버리지 해소: SK-06 — `docs/tone/` · `docs/tone/*.md` 는 `m SK-06` 의 `find "$E/docs/tone"` 이 센다. 산문의 파일 넷은 `m SK-06` 의 `for f in` 목록과 같다
- 커버리지 해소: SK-08 — `research-log.md` 는 `m SK-08` 의 `log=` 가 세는 글자이고, `docs/api/research-log.md:161-175` 는 근거 인용이다
- 커버리지 해소: SC-06 — 두 시험 스크립트는 `m SC-06` 이 이름으로 부른다(`log-reflection-test` · `collect-status-test` · `project-id-test`)
- 커버리지 해소: ER-02 — 두 픽스처는 `m ER-02` 가 `$fx/…json` 으로 부르는 입력이다
- 커버리지 해소: AR-02 — 열여섯 토큰과 notes 경로는 `m AR-02` 의 토큰 목록과 `NOTES` 변수가 덮는다. `reflections-2026-09.md` 등 경로 모양 토큰은 notes 안에서 찾을 글자다
- 오라클 해소: SK-01 · SK-02 · SK-03 · SK-04 · SK-05 · SK-06 · SK-07 · SK-08 — 산출물이 문서 문장이라 부를 코드가 없다. 옛 문구 0 · 새 문구 줄 수 · 바꾸면 안 되는 줄의 글자 대조와 양성 대조로 잰다. 실행해서 재는 조건은 SC-01 ~ SC-06 · ER-01 · ER-02 · AR-01 · DG-02 · DG-05 다
- 오라클 해소: DG-05 — 검출기가 산문 grep 으로 읽었지만 `summary.txt` 는 CI 단계를 실제로 돌린 결과다. grep 은 실행 출력을 세는 자리일 뿐이다
- 교차 진단 반영(봉인 전): SK-01 측정을 띄어쓰기 무관(`코드 ?블록`)으로 넓혔다 — 시작 판 값은 그대로 0 이다. SK-07 에 ER-02 와 같은 설치본 가드를 더했다. DG-05 에 도구 해시 확인과 `[미검증]` 분기를 더했다
- 측정 도구 결함 발견(다른 묶음 몫): 킷 후속 A 계약(`ak-c3` 의 `sprint-contract-after-0924-kits-a.md`) 도우미 `newmd` 가 `sort -n` 뒤 `comm` 을 써 줄 번호 자릿수가 섞이면 겹침을 0 으로 센다 — 이 계약 DG-02 는 글자 순 정렬로 고쳐 썼고 양성 대조로 확인했다

## 회귀 게이트 — 측정 도우미

평가 때 이 블록을 떼어 bash 에서 불러 쓴다. `TMPDIR` 은 평가자 임시 폴더로 준다. 도우미는 끝점을 `git archive` 로 풀어 재므로 작업 폴더의 미커밋 변경을 보지 않는다.
`W` · `BR` 을 바꿀 때는 `export` 한 뒤 source 한다(앞에 붙인 일회성 대입은 source 가 끝나면 풀린다 — 봉인 전 예행에서 실측).
작업 폴더 밖 입력(이 맥 `~/.claude/logs` · 설치본 슬라이서)은 읽기만 하고 지우지 마라 — 도우미가 만든 `$T` 아래만 치워도 된다.
`SC-05` 는 실제 `claude` 를 로그인 안 된 사본 설정으로 두 번 띄운다(모델 호출 없음). `ER-02` · `SK-07` 은 이 맥 설치본 뱀부 · 오르카가 필요하다.

```bash
# 떼기: awk '/^# === 측정 도우미 시작/{f=1} f{print} /^# === 측정 도우미 끝/{exit}' <계약> > "$TMPDIR/kitsb-measure.sh"
# 부르기: bash -c 'source "$TMPDIR/kitsb-measure.sh" || exit 2; type m >/dev/null || exit 2; m SK-01'
# 시작 판: E_REF=BASE 를 export 하고 부른다
# === 측정 도우미 시작 (after-0924-kits-b) ===
# 쓰는 법: 이 블록을 파일로 떼어 bash 에서 source 한 뒤 `m <조건 ID>`. zsh 에서 부르지 마라.
# 잴 트리 E — 기본은 가지 끝(TIP)을 git archive 로 푼 임시 폴더. 시작 판은 E_REF=BASE, 봉인 전 예행은 E_DIR=<풀어 둔 폴더>.
# B 는 늘 시작 판이다 — 음성 대조(시작 판 훅 · 라이브러리로 새 시험을 돌리기)에 쓴다.
W=${W:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c3c}
BR=${BR:-chore/ak-c3c-kits}
BASE=$(git -C "$W" merge-base origin/main "$BR") || { echo "UNRESOLVED BASE"; return 2 2>/dev/null || exit 2; }
TIP=$(git -C "$W" rev-parse --verify "$BR") || { echo "UNRESOLVED TIP"; return 2 2>/dev/null || exit 2; }
T=$(mktemp -d "${TMPDIR:-/tmp}/kitsb.XXXXXX")
snap() { mkdir -p "$2" && git -C "$W" archive "$1" | tar -x -C "$2"; }
if [ -n "${E_DIR:-}" ]; then E=$E_DIR
else case "${E_REF:-TIP}" in
  BASE) E=$T/base; snap "$BASE" "$E" ;;
  *)    E=$T/tip;  snap "$TIP" "$E" ;;
esac; fi
B=$T/b0; snap "$BASE" "$B"
NOTES=.harness/.meta/after-kaizen-0926/c3c-notes.md
# s 로 시작하는 줄부터 e 로 시작하는 다음 줄 앞까지
sec() { awk -v s="$1" -v e="$2" 'index($0,s)==1{f=1;print;next} f&&index($0,e)==1{exit} f' "$3"; }
n()  { grep -cF -- "$1" || true; }   # 표준 입력에서 글자 그대로 든 줄 수
nr() { grep -cE -- "$1" || true; }   # 표준 입력에서 정규식에 맞는 줄 수
at() { local e=$(( $(date +%s) - $1 )); date -r "$e" "$2" 2>/dev/null || date -d "@$e" "$2"; }
F='+%Y-%m-%dT%H:%M:%S%z'
cs() {  # cs <트리> <일수|all> <폴더>... — 그 트리 라이브러리의 collect_status
  local tree=$1; shift
  bash -c '. "$1" 2>/dev/null; shift; collect_status "$@"' _ "$tree/reflect-kit/hooks/_lib-project-id.sh" "$@" 2>&1
}
rk_setup() {  # 가짜 codex(형식별 출력) · 가짜 claude(인자 기록 후 실패) · 12 줄 transcript
  mkdir -p "$T/bin" "$T/in"
  cat > "$T/bin/codex" <<'EOF'
#!/usr/bin/env bash
out=""; prev=""
for a in "$@"; do [ "$prev" = "--output-last-message" ] && out=$a; prev=$a; done
cat > /dev/null
case "${FAKE_CODEX:-}" in
  nf1) printf 'primary_category: misunderstanding\nalso_applies: []\nmistake_tag: nofence-one-tag\nseverity: low\nactionability: claude_behavior\n' > "$out" ;;
  nf2) printf 'primary_category: misunderstanding\nmistake_tag: nofence-two-a\nactionability: claude_behavior\n\nprimary_category: wrong_approach\nmistake_tag: nofence-two-b\nactionability: claude_behavior\n' > "$out" ;;
  bare) printf '```\nprimary_category: tool_failure\nmistake_tag: bare-fence-tag\nactionability: claude_behavior\n```\n' > "$out" ;;
  fenced) printf '```yaml\nprimary_category: misunderstanding\nmistake_tag: fenced-tag\nactionability: claude_behavior\n```\n' > "$out" ;;
  env) printf 'primary_category: tool_failure\nmistake_tag: fix-env-repeat-tag\nactionability: user_environment\n' > "$out" ;;
  prose) printf '요약하면 이번 세션에는 짚을 만한 일이 조금 있었다.\n다음 세션에서 다시 본다.\n' > "$out" ;;
  fail) exit 1 ;;
esac
exit 0
EOF
  cat > "$T/bin/claude" <<'EOF'
#!/usr/bin/env bash
{ printf 'claude'; for a in "$@"; do printf ' [%s]' "$a"; done; printf '\n'; } >> "$CALLS"
cat > /dev/null
exit 1
EOF
  chmod 755 "$T/bin/codex" "$T/bin/claude"
  for i in 1 2 3 4 5 6 7 8 9 10 11 12; do printf '{"type":"user","message":{"content":"line %s"}}\n' "$i"; done > "$T/in/t.jsonl"
}
rk_run() {  # rk_run <훅 폴더> <HOME> <session> <FAKE_CODEX>
  local in=$T/in/$3.json
  mkdir -p "$2/proj"
  jq -cn --arg s "$3" --arg t "$T/in/t.jsonl" --arg c "$2/proj" '{session_id:$s, transcript_path:$t, cwd:$c}' > "$in"
  env HOME="$2" TMPDIR="$T" PATH="$T/bin:$PATH" FAKE_CODEX="$4" CALLS="$T/calls.log" REFLECT_KIT_LOGS_ROOT= REFLECT_KIT_ANALYZER= \
    bash "$1/log-reflection.sh" --background "$in" >/dev/null 2>&1
}
rk_refl() { find "$1/.claude/logs" -type f -name 'reflections-*.md' 2>/dev/null | head -1; }
rk_count() {  # rk_count <HOME> — yaml 여는 줄 / 맨 fence 줄 / fence 안 primary_category 줄 / collect_status 엔트리
  local f e; f=$(rk_refl "$1")
  [ -n "$f" ] || { printf '0/0/0/0'; return; }
  e=$(cs "$E" all "$(dirname "$f")" | sed -n 's/.* \/ 엔트리 \([0-9]*\) \/.*/\1/p')
  printf '%s/%s/%s/%s' "$(nr '^[[:space:]]*```yaml[[:space:]]*$' <"$f")" "$(nr '^[[:space:]]*```[[:space:]]*$' <"$f")" \
    "$(awk '/^[ \t]*```yaml[ \t]*$/{f=1;next} /^[ \t]*```[ \t]*$/{f=0;next} f && /^[ \t]*primary_category:/{k++} END{print k+0}' "$f")" "${e:-?}"
}
real_hooks() {  # real_hooks <훅 파일> — 훅의 claude -p 인자 그대로, 표식 훅만 든 사본 설정(사용자 · 프로젝트)에서 띄워 표식 수를 센다
  command -v claude >/dev/null 2>&1 || { echo "claude-없음"; return; }
  local args d M; args=$(grep -m1 'REFLECT_KIT_ANALYZER=1 claude -p' "$1" | sed -E 's/.*REFLECT_KIT_ANALYZER=1 claude (-p[^\\>]*).*/\1/')
  case "$args" in -p*) ;; *) echo "args-없음(호출 줄을 못 찾음)"; return ;; esac   # 빈 인자로 claude 를 띄우면 대화형으로 멈춘다
  d=$(mktemp -d "$T/cp.XXXXXX"); mkdir -p "$d/cfg" "$d/cwd/.claude"; M=$d/marks.log; : > "$M"
  hk() { printf '{"type":"command","command":"printf \\"%s\\\\n\\" >> %s"}' "$1" "$M"; }
  for s in user project; do
    printf '{"hooks":{"SessionStart":[{"hooks":[%s]}],"UserPromptSubmit":[{"hooks":[%s]}],"Stop":[{"hooks":[%s]}]}}\n' \
      "$(hk "$s-SessionStart")" "$(hk "$s-UserPromptSubmit")" "$(hk "$s-Stop")" > "$d/$s.json"
  done
  mv "$d/user.json" "$d/cfg/settings.json"; mv "$d/project.json" "$d/cwd/.claude/settings.json"
  # shellcheck disable=SC2086  # 인자 목록을 낱말로 나눠 넘긴다
  ( cd "$d/cwd" && echo "say ok" | CLAUDE_CONFIG_DIR="$d/cfg" REFLECT_KIT_ANALYZER=1 claude $args >/dev/null 2>&1 )
  printf 'args=[%s] marks=%s' "$(printf '%s' "$args" | sed 's/ *$//')" "$(grep -c . "$M")"
}
stall() {  # stall <폴더> <기록 초 전|-> <실패 초 전> <실패 수> — 기록 하나 뒤 실패 시도 N 번
  mkdir -p "$1"; : > "$1/.errors.log"
  [ "$2" = - ] || printf '\n## %s\n\n- session: `R`\n\n```yaml\nprimary_category: tool_failure\n```\n' "$(at "$2" "$F")" > "$1/reflections-2026-09.md"
  local i; for i in $(seq 1 "$4"); do
    printf '%s [log-reflection] fail:codex-exit-1 session=X%s\n%s [log-reflection] fallback:claude-exit-1 session=X%s\n' "$(at "$3" "$F")" "$i" "$(at "$3" "$F")" "$i" >> "$1/.errors.log"
  done
}
gate() {  # bambu 완료 검사를 SKILL.md 에서 뗀다 (스킬 음성 대조 절과 같은 방법)
  local s=$E/bambu-kit/skills/bambu-print-profile/SKILL.md a b
  a=$(grep -n '^TARGET_SLICER=.* python3 - ' "$s" | head -1 | cut -d: -f1)
  b=$(awk -v s="$a" 'NR>s && $(0)=="PY" {print NR; exit}' "$s")
  sed -n "$((a+1)),$((b-1))p" "$s" > "$T/gate.py"
}
bv() { defaults read /Applications/BambuStudio.app/Contents/Info.plist CFBundleShortVersionString 2>/dev/null; }
optlist() {  # optlist <이름> <grep -v 로 뺄 줄 머리 정규식|-> — 원본 목록에서 줄을 뺀 기준 폴더
  local d src; d=$T/ol-$1; src=$E/bambu-kit/skills/bambu-print-profile/references/option-keys/bambu-$(bv).tsv
  mkdir -p "$d/references/option-keys"
  if [ "$2" = - ]; then : > "$d/references/option-keys/bambu-$(bv).tsv"
  else grep -vE "$2" "$src" > "$d/references/option-keys/bambu-$(bv).tsv"; fi
  printf '%s' "$d"
}
g91_scan() {  # 설치본 H2S 기계 프로파일의 G-code 템플릿 — G91 수 · M82 수 · M83 수 · G91 구간 안 E 이동 수
  python3 - <<'PY'
import json, pathlib
roots = {"bambu": "/Applications/BambuStudio.app/Contents/Resources/profiles/BBL/machine",
         "orca": "/Applications/OrcaSlicer.app/Contents/Resources/profiles/BBL/machine"}
for slicer, root in roots.items():
    for p in sorted(pathlib.Path(root).glob("*H2S*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        for key, val in d.items():
            if key != "machine_start_gcode" or not isinstance(val, str): continue
            rel = False; g91 = m82 = m83 = inside = 0
            for raw in val.splitlines():
                w = raw.split(";", 1)[0].split()
                if not w: continue
                c = w[0].upper()
                if c == "M82": m82 += 1
                elif c == "M83": m83 += 1
                elif c == "G91": g91 += 1; rel = True
                elif c == "G90": rel = False
                elif c in ("G0", "G1") and rel and any(x.upper().startswith("E") for x in w[1:]): inside += 1
            print(f"{slicer} G91={g91} M82={m82} M83={m83} G91_E={inside}")
PY
}
v6_bare() {  # 표준 입력의 .md 경로마다 validate-plugin V6 과 같은 상태기계로 언어 없는 여는 fence 를 센다 — V6 이 안 보는 킷 밖 파일용
  python3 -c '
import sys
k = 0
for p in sys.stdin.read().split():
    inb = False
    for line in open(p, encoding="utf-8").read().splitlines():
        st = line.strip()
        if st.startswith("```"):
            if not inb:
                k += not st[3:].strip(); inb = True
            else:
                inb = False
print(k)'
}
MDL=${MDL:-$T/mdl}
mdl_ready() {  # markdownlint-cli2 0.23.2 · MD013 끔 — 편집기 확장과 같은 설정
  [ -x "$MDL/node_modules/.bin/markdownlint-cli2" ] || { mkdir -p "$MDL" && (cd "$MDL" && npm install --no-save --no-audit --no-fund markdownlint-cli2@0.23.2 >/dev/null 2>&1); }
  printf '{ "config": { "MD013": false } }\n' > "$MDL/cfg.markdownlint-cli2.jsonc"
  [ -x "$MDL/node_modules/.bin/markdownlint-cli2" ]
}
added() { diff -U0 "$1" "$2" | awk '/^@@/{split($3,a,","); s=substr(a[1],2); c=(a[2]=="")?1:a[2]; for(i=0;i<c;i++) print s+i}'; }
newmd() {  # newmd <옛 파일|빈 파일> <새 파일> — 새 파일에서 더해진 줄에 걸린 경고 수
  ( cd "$(dirname "$2")" && "$MDL/node_modules/.bin/markdownlint-cli2" --config "$MDL/cfg.markdownlint-cli2.jsonc" "$(basename "$2")" 2>&1 ) \
    | awk -F: '/^[^ ]+:[0-9]+/{print $2+0}' | sort -u > "$T/w.txt"   # comm 은 글자 순 정렬을 요구한다 — sort -n 이면 54 · 191 이 어긋나 0 이 된다
  added "$1" "$2" | sort -u > "$T/a.txt"
  comm -12 "$T/w.txt" "$T/a.txt" | grep -c . || true
}
ALLOWED='reflect-kit/hooks/log-reflection.sh
reflect-kit/hooks/_lib-project-id.sh
reflect-kit/evals/hooks/log-reflection-test.sh
reflect-kit/evals/hooks/collect-status-test.sh
reflect-kit/skills/reflect-digest/SKILL.md
reflect-kit/README.md
bambu-kit/skills/bambu-print-profile/SKILL.md
tone-kit/references/adapter-dart-flutter.md
tone-kit/references/adapter-contract.md
tone-kit/references/locale-korean.md
tone-kit/README.md
docs/tone/dart-flutter-idioms.md
CLAUDE.md
.claude/skills/tone-kaizen/SKILL.md
.claude/skills/tone-research/SKILL.md
docs/superpowers/specs/2026-09-02-api-kit-design.md
.harness/sprint-contract-after-0924-kits-b.md
.harness/sprint-feedback-after-0924-kits-b.md
.harness/sprint-amendments-after-0924-kits-b.md'
group() {  # 경로 → 묶음 이름 (한 커밋에 묶음 하나)
  case "$1" in
    reflect-kit/*) echo reflect ;;
    bambu-kit/*) echo bambu ;;
    tone-kit/*|docs/tone/*|CLAUDE.md|.claude/skills/tone-kaizen/*|.claude/skills/tone-research/*) echo tone ;;
    docs/superpowers/specs/2026-09-02-api-kit-design.md) echo api ;;
    .harness/*) echo harness ;;
    *) echo "밖:$1" ;;
  esac
}
m() {
  case "$1" in
  SK-01) s=$(sec '4. **엔트리 파싱**' '5. **actionability' "$E/reflect-kit/skills/reflect-digest/SKILL.md")
    echo "legacy_line=$(printf '%s\n' "$s" | grep -F 'primary_category:' | nr '코드 ?블록')" ;;
  SK-02) f=$E/reflect-kit/skills/reflect-digest/SKILL.md
    echo "old13=$(n '늦은 쪽 뒤에 Stop 실패 시도가 있으면' <"$f") old_rule=$(n '마지막 기록 뒤 Stop 실패 시도가 1 이상일 때' <"$f") new=$(grep -F '3 회 이상' "$f" | n '1 일 이상') hook_old=$(n '실패 한 번만 보고 멈춤으로 판정' <"$E/reflect-kit/hooks/log-reflection.sh")" ;;
  SK-03) f=$E/reflect-kit/README.md
    echo "errors_ok=$(grep -F '.errors.log' "$f" | grep -F '#' | n 'ok:no-issues') fallback_safe=$(grep -F 'claude -p' "$f" | n '--safe-mode')" ;;
  SK-04) ad=$E/tone-kit/references/adapter-dart-flutter.md; id=$E/docs/tone/dart-flutter-idioms.md
    rule=$(sec '### 슬롯 작성 규칙' '## ' "$E/tone-kit/references/adapter-contract.md" | grep -F '\|' | n '0 건')
    ra=$(grep -F '| `fallback_identifier_pattern` |' "$ad"); ri=$(grep -F '| `fallback_identifier_pattern` |' "$id")
    run="grep -rnE '\\b(effective|resolved)[A-Z]' --include='*.dart' <src>"
    echo "rule=$rule ad_pipe=$(printf '%s\n' "$ra" | n '\|') ad_ptr=$(printf '%s\n' "$ra" | grep -F effective | grep -F resolved | n 'G-04') id_pipe=$(printf '%s\n' "$ri" | n '\|') id_ptr=$(printf '%s\n' "$ri" | grep -F effective | grep -F resolved | n 'audit_greps') ad_run=$(n "$run" <"$ad") id_run=$(n "$run" <"$id")" ;;
  SK-05) f=$E/tone-kit/references/locale-korean.md
    rows=$(sec '## 2. 번역투 킬러 패턴 치환표' '## 3.' "$f" | awk -F' \\| ' '/^\| /&&!/^\| 금지 /&&!/^\|---/{print $3}')
    ok=0; i=0; while IFS= read -r c; do [ -n "$c" ] || continue; i=$((i+1)); case "$c" in *"G-1 갈래 $i"*) case "$c" in *'\|'*) ;; *) ok=$((ok+1)) ;; esac ;; esac; done <<EOF
$rows
EOF
    g1="grep -nE '(을|를) ?(처리|관리)(합니다|한다)|에 대해서?|하도록 (합니다|한다)|에 의(해|하여)|되어 있(는 경우|을 때)|(표시|적용|호출|생성|반환)(됩니다|된다)' \"\${FILES[@]}\""
    alt=$(python3 - "$f" <<'PY'
import re, sys
s = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r"# G-1[^\n]*\ngrep -nE '([^']*)'", s)
d = 0; k = 1
for ch in (m.group(1) if m else ""):
    d += ch == "("; d -= ch == ")"; k += (ch == "|" and d == 0)
print(k if m else 0)
PY
)
    echo "rows=$i pointer_ok=$ok pipe_rows=$(printf '%s\n' "$rows" | n '\|') g1_line=$(n "$g1" <"$f") g1_alts=$alt" ;;
  SK-06) bad=0; tot=0
    for f in CLAUDE.md tone-kit/README.md .claude/skills/tone-research/SKILL.md .claude/skills/tone-kaizen/SKILL.md; do
      while IFS= read -r l; do tot=$((tot+1)); case "$l" in *overview*) case "$l" in *research-log*) case "$l" in *templates*) continue ;; esac ;; esac ;; esac; bad=$((bad+1)); done < <(grep -F '8종' "$E/$f")
    done
    echo "lines_8=$tot missing_basis=$bad k35=$(n '- `docs/tone/*.md` 11종 (리서치 문서 8종 + overview · research-log · templates)' <"$E/.claude/skills/tone-kaizen/SKILL.md") research_docs=$(find "$E/docs/tone" -maxdepth 1 -name '*.md' ! -name overview.md ! -name research-log.md ! -name templates.md | grep -c .)" ;;
  SK-07) command -v defaults >/dev/null 2>&1 && [ -n "$(bv)" ] && [ -d /Applications/OrcaSlicer.app/Contents/Resources/profiles/BBL/machine ] || { echo "뱀부 · 오르카 설치본 없음"; return; }
    f=$E/bambu-kit/skills/bambu-print-profile/SKILL.md; s=$(sec '**G-code 로 길이 재기' '### Phase 5' "$f")
    note=$(printf '%s\n' "$s" | grep -F 'G91' | grep -F 'M83' | grep -F 'M82' | grep -F "$(bv)" | n '2.4.2')
    blk_e=$(printf '%s\n' "$s" | awk '/^python3 - "<G-code 경로>"/{f=1} f{print} f&&/^PY$/{exit}')
    blk_b=$(sec '**G-code 로 길이 재기' '### Phase 5' "$B/bambu-kit/skills/bambu-print-profile/SKILL.md" | awk '/^python3 - "<G-code 경로>"/{f=1} f{print} f&&/^PY$/{exit}')
    echo "note=$note block_same=$([ "$blk_e" = "$blk_b" ] && [ -n "$blk_e" ] && echo 1 || echo 0) | $(g91_scan | tr '\n' ' ')" ;;
  SK-08) f=$E/docs/superpowers/specs/2026-09-02-api-kit-design.md; s=$(sec '### 9.2 ' '## 10.' "$f")
    st=$(grep -nF '### 9.2 ' "$f" | cut -d: -f1); en=$(grep -nF '## 10.' "$f" | head -1 | cut -d: -f1)
    out_hunk=$(diff -U0 "$B/docs/superpowers/specs/2026-09-02-api-kit-design.md" "$f" | awk -v a="$st" -v b="$en" '/^@@/{split($3,x,","); s=substr(x[1],2)+0; c=(x[2]=="")?1:x[2]+0; e=s+(c>0?c-1:0); if (s<a || e>=b) k++} END{print k+0}')
    echo "unqualified=$(printf '%s\n' "$s" | grep -E '표현되지 않는다|쓸 수 없다' | grep -vcF '정정' || true) jeongjeong=$(printf '%s\n' "$s" | n '정정') exit3=$(printf '%s\n' "$s" | n '종료 코드') undecided=$(printf '%s\n' "$s" | n '판정 불가') log=$(printf '%s\n' "$s" | n 'research-log.md') capture=$(printf '%s\n' "$s" | n 'capture') post=$(printf '%s\n' "$s" | n '**후처리 단계에서 검사**') out_of_92=$out_hunk" ;;
  SC-01) rk_setup; out=""
    for k in nf1 nf2 bare fenced; do h=$T/h-$k; rk_run "$E/reflect-kit/hooks" "$h" "S-$k" "$k"; out="$out $k=$(rk_count "$h")"; done
    echo "${out# }" ;;
  SC-02) rk_setup; h=$T/h-env; rk_run "$E/reflect-kit/hooks" "$h" E1 env; rk_run "$E/reflect-kit/hooks" "$h" E2 env
    f=$(rk_refl "$h"); d=$(dirname "$f"); tsv=$(awk -F'\t' '$1=="fix-env-repeat-tag"{print $4}' "$d/.env-issues.tsv" 2>/dev/null)
    echo "e1=$(n '- session: `E1`' <"$f") e2=$(n '- session: `E2`' <"$f") dedup_all=$(grep 'skip:env-dedup-all' "$d/.errors.log" 2>/dev/null | n ' session=E2') tsv=${tsv:-0}" ;;
  SC-03) d=$T/legacy; mkdir -p "$d"; t1=$(at 7200 "$F"); t2=$(at 3600 "$F")
    printf '\n## %s\n\n- session: `L1`\n- cwd: `/x`\n\nprimary_category: misunderstanding\nmistake_tag: legacy-a\nactionability: claude_behavior\nprimary_category: wrong_approach\nmistake_tag: legacy-b\nactionability: claude_behavior\n\n---\n\n## %s\n\n- session: `L2`\n- cwd: `/x`\n\n```yaml\nprimary_category: tool_failure\nmistake_tag: fenced-c\n```\n\n---\n' "$t1" "$t2" > "$d/reflections-2026-09.md"
    echo "$(cs "$E" 7 "$d" | head -1 | sed -n 's/.*\(기록된 세션 [0-9]* \/ 엔트리 [0-9]*\).*/\1/p')" ;;
  SC-04) stall "$T/s-old3" 259200 172800 3; stall "$T/s-recent3" 7200 3600 3; stall "$T/s-idle3" 259200 3600 3
    stall "$T/s-old2" 259200 172800 2; stall "$T/s-old1" 172800 90000 1; stall "$T/s-zero" - 3600 1
    out="old3=$(cs "$E" 7 "$T/s-old3" | n '⚠ 수집 멈춤 — 마지막 기록 뒤 Stop 실패 시도 3회')"
    for k in recent3 idle3 old2 old1; do out="$out $k=$(cs "$E" 7 "$T/s-$k" | n '⚠ 수집 멈춤')"; done
    echo "$out zero=$(cs "$E" 7 "$T/s-zero" | n '⚠ 수집 멈춤 — 엔트리 0은 문제 없음이 아니다')" ;;
  SC-05) rk_setup; : > "$T/calls.log"; rk_run "$E/reflect-kit/hooks" "$T/h-fb" F1 fail; c=$(grep '^claude' "$T/calls.log")
    echo "safe=$(printf '%s\n' "$c" | n '[--safe-mode]') model=$(printf '%s\n' "$c" | n '[--model] [haiku]') nosess=$(printf '%s\n' "$c" | n '[--no-session-persistence]') | tip $(real_hooks "$E/reflect-kit/hooks/log-reflection.sh") | base $(real_hooks "$B/reflect-kit/hooks/log-reflection.sh")" ;;
  SC-06) out=""; for t in log-reflection-test collect-status-test project-id-test; do o=$(bash "$E/reflect-kit/evals/hooks/$t.sh" 2>&1); out="$out $t rc=$? [$(printf '%s\n' "$o" | tail -1)]"; done
    nb=$(REFLECT_KIT_HOOKS="$B/reflect-kit/hooks" bash "$E/reflect-kit/evals/hooks/log-reflection-test.sh" 2>&1 | tail -1)
    nc=$(PROJECT_ID_LIB="$B/reflect-kit/hooks/_lib-project-id.sh" bash "$E/reflect-kit/evals/hooks/collect-status-test.sh" 2>&1 | tail -1)
    echo "${out# } | base_hooks [$nb] | base_lib [$nc]" ;;
  ER-01) rk_setup; h=$T/h-prose; rk_run "$E/reflect-kit/hooks" "$h" P1 prose; f=$(rk_refl "$h")
    if [ -n "$f" ]; then echo "recorded=$(n '- session: `P1`' <"$f") prose=$(n '짚을 만한 일이 조금 있었다' <"$f") yaml=$(nr '^[[:space:]]*```yaml' <"$f")"; else echo "recorded=0"; fi ;;
  ER-02) command -v defaults >/dev/null 2>&1 && [ -n "$(bv)" ] || { echo "뱀부 설치본 없음"; return; }
    gate; fx=$E/bambu-kit/evals/gate-fixtures; ne=$(optlist noenum "^enum$(printf '\t')"); em=$(optlist empty -)
    o1=$(SKILL_DIR="$ne" TARGET_SLICER=bambu python3 "$T/gate.py" "$fx/process-seam-slope-type-invalid.json" 2>&1); r1=$?
    l1=$(printf '%s\n' "$o1" | grep -F '[미검증]' | grep -F 'option-keys')
    o2=$(SKILL_DIR="$em" TARGET_SLICER=bambu python3 "$T/gate.py" "$fx/process-seam-slope-type-invalid.json" 2>&1)
    o3=$(SKILL_DIR="$ne" TARGET_SLICER=bambu python3 "$T/gate.py" "$fx/process-machine-scope-key.json" 2>&1)
    l3=$(printf '%s\n' "$o3" | grep -F '[미검증]' | grep -F 'option-keys')
    echo "noenum=$(printf '%s\n' "$l1" | n 'enum 값 검사 미실행')/$(printf '%s\n' "$l1" | n '키 존재')/$r1/$(printf '%s\n' "$o1" | n 'RESULT: PASS') empty=$(printf '%s\n' "$o2" | grep -F '[미검증]' | n '키 존재 · 종류 · enum 값 검사 미실행') scope=$(printf '%s\n' "$o3" | n 'FAIL process-machine-scope-key.json: 키 스코프 불일치')/$(printf '%s\n' "$l3" | n '키 존재')" ;;
  AR-01) ch=$(git -C "$W" diff --name-only "$BASE" "$TIP")
    extra=$(printf '%s\n' "$ch" | grep . | grep -vxF -f <(printf '%s\n' "$ALLOWED") | grep -v '^\.harness/\.meta/after-kaizen-0926/c3c-' | grep -c . || true)
    ks=""; for k in reflect bambu tone api; do ks="$ks $k=$(printf '%s\n' "$ch" | grep . | while IFS= read -r p; do group "$p"; done | grep -cx "$k" || true)"; done
    multi=0; for c in $(git -C "$W" rev-list "$BASE..$TIP"); do g=$(git -C "$W" show --name-only --format= "$c" | grep . | while IFS= read -r p; do group "$p"; done | sort -u | grep -c .); [ "$g" -gt 1 ] && multi=$((multi + 1)); done
    echo "base=${BASE:0:7} tip=${TIP:0:7} changed=$(printf '%s\n' "$ch" | grep -c . || true) extra=$extra$ks multi_group=$multi"
    [ "$extra" = 0 ] || printf '%s\n' "$ch" | grep . | grep -vxF -f <(printf '%s\n' "$ALLOWED") | grep -v '^\.harness/\.meta/after-kaizen-0926/c3c-' ;;
  AR-02) b=$(git -C "$W" show "$TIP:$NOTES" 2>/dev/null); c=$([ -n "$b" ] && echo 1 || echo 0); out="committed=$c"
    for k in '--safe-mode' 'marks=' '3 회' '1 일' 'feat/bambu-kit-orca-h2s-feedback' 'G91' '종류 줄' 'overview' 'docs/api' 'kaizen-orchestrator' 'noncharacter' 'reflections-2026-09.md' 'tone-guide' 'docs/tone-kit/dart-flutter-idioms.html' 'docs/bambu-kit/bambu-print-profile.html' '넘김'; do out="$out $(printf '%s\n' "$b" | n "$k")"; done
    echo "$out" ;;
  RE-01) echo "added=$(git -C "$W" diff --diff-filter=A --name-only "$BASE" "$TIP" -- reflect-kit bambu-kit tone-kit docs CLAUDE.md .claude | grep -c . || true) cs_defs=$(grep -rE '^collect_status\(\)' "$E/reflect-kit" | grep -c . || true) cs_file=$(grep -lE '^collect_status\(\)' -r "$E/reflect-kit" | sed "s#^$E/##")" ;;
  RE-02) echo "tests=$(find "$E/reflect-kit/evals" -type f | grep -c .)/$(find "$B/reflect-kit/evals" -type f | grep -c .) awk_re=$(grep -v '^[[:space:]]*#' "$E/reflect-kit/hooks/log-reflection.sh" | n 'tag_canon_awk_re') tag_literal=$(grep -v '^[[:space:]]*#' "$E/reflect-kit/hooks/log-reflection.sh" | n 'mistake_tag')" ;;
  AP-03) (cd "$E" && python3 scripts/validate-plugin.py --check=code-fence >/dev/null 2>&1); rc=$?
    bare=$(git -C "$W" diff --name-only "$BASE" "$TIP" -- '*.md' | while IFS= read -r f; do [ -f "$E/$f" ] && printf '%s\n' "$E/$f"; done | v6_bare)
    echo "v6_rc=$rc bare_changed=${bare:-0}" ;;
  AP-04) (cd "$E" && python3 scripts/validate-plugin.py --check=frontmatter >/dev/null 2>&1); rc=$?
    echo "v1_rc=$rc tone_names=$(for s in tone-kaizen tone-research; do awk -v want="name: $s" 'NR==1&&/^---$/{f=1;next} f&&/^---$/{exit} f&&$0==want{k++} END{print k+0}' "$E/.claude/skills/$s/SKILL.md"; done | tr '\n' ' ' | sed 's/ $//')" ;;
  DG-02) mdl_ready || { echo "MDL_NOT_READY"; return; }; tot=0; rows=""
    for f in $(git -C "$W" diff --name-only "$BASE" "$TIP" -- '*.md' ':(exclude).harness/sprint-*.md'); do
      o=$T/old.md; git -C "$W" show "$BASE:$f" > "$o" 2>/dev/null || : > "$o"
      c=$(newmd "$o" "$E/$f"); tot=$((tot + c)); rows="$rows $f=$c"; done
    sc=0; for f in $(git -C "$W" diff --name-only "$BASE" "$TIP" -- '*.sh'); do sc=$((sc + $(shellcheck -f gcc "$E/$f" 2>/dev/null | grep -c . || true))); done
    echo "md_new=$tot sh_all=$sc |$rows" ;;
  *) echo "모르는 조건 $1"; return 2 ;;
  esac
}
# === 측정 도우미 끝 ===
```

봉인 전 실측(2026-09-26, 시작점 `88ddfe5` 을 풀어 둔 판 `E_REF=BASE` · 정규화 원형을 넣은 예행 사본 `E_DIR`):

| 조건 | 시작 판 | 예행 사본 |
| --- | --- | --- |
| SK-01 · SK-02 · SK-03 | `legacy_line=0` · `old13=1 old_rule=2 new=0 hook_old=1` · `errors_ok=0 fallback_safe=0` | `legacy_line=1` · `old13=0 old_rule=0 new=3` · `errors_ok=1 fallback_safe=1` |
| SK-04 · SK-05 | `rule=0 ad_pipe=1 ad_ptr=0 id_pipe=1 id_ptr=0 ad_run=1 id_run=1` · `rows=6 pointer_ok=0 pipe_rows=5 g1_line=1 g1_alts=6` | `rule=1 ad_pipe=0 ad_ptr=1 id_pipe=0 id_ptr=1 ad_run=1 id_run=1` · `rows=6 pointer_ok=6 pipe_rows=0 g1_line=1 g1_alts=6` |
| SK-06 · SK-07 | `lines_8=6 missing_basis=5 k35=1 research_docs=8` · `note=0 block_same=1 \| bambu G91=6 M82=0 M83=6 G91_E=0 orca G91=5 M82=0 M83=6 G91_E=0` | `missing_basis=0` · `note=1 block_same=1` |
| SK-08 | `unqualified=2 jeongjeong=0 exit3=0 undecided=0 log=0 capture=0 post=1 out_of_92=0` | `unqualified=0 jeongjeong=3 exit3=1 undecided=1 log=1 capture=1 post=1 out_of_92=0` |
| SC-01 · SC-02 · SC-03 | `nf1=0/0/0/0 nf2=0/0/0/0 bare=0/2/0/0 fenced=1/1/1/1` · `e1=1 e2=1 dedup_all=0 tsv=0` · `기록된 세션 2 / 엔트리 1` | `nf1=1/1/1/1 nf2=2/2/2/2 bare=1/1/1/1 fenced=1/1/1/1` · `e1=1 e2=0 dedup_all=1 tsv=2` · `기록된 세션 2 / 엔트리 3` |
| SC-04 · SC-05 | `old3=1 recent3=1 idle3=1 old2=1 old1=1 zero=1` · `safe=0 model=1 nosess=1 \| tip … marks=4 \| base … marks=4` | `old3=1 recent3=0 idle3=0 old2=0 old1=0 zero=1` · `safe=1 … tip args=[-p --safe-mode --model haiku --no-session-persistence] marks=0 \| base … marks=4` |
| SC-06 | `26 · 14 · 16` 모두 `불일치 0` · `base_hooks 불일치 0` · `base_lib 불일치 0` | 새 경우 일부만 넣은 사본 `base_hooks 불일치 3` · `base_lib 불일치 3` |
| ER-01 · ER-02 | `recorded=1 prose=1 yaml=0` · `noenum=1/1/0/1 empty=1 scope=1/1` | `recorded=1 prose=1 yaml=0` · `noenum=1/0/0/1 empty=1 scope=1/0` |
| AR-01 · AR-02 · RE-01 · RE-02 | `changed=0 extra=0` 네 묶음 0 `multi_group=0` · `committed=0` 과 0 열여섯 · `added=0 cs_defs=1 cs_file=reflect-kit/hooks/_lib-project-id.sh` · `tests=3/3 awk_re=1 tag_literal=0` | — |
| AP-03 · AP-04 · DG-02 | `v6_rc=0 bare_changed=0` · `v1_rc=0 tone_names=1 1` · `md_new=0 sh_all=0` | — |
| 양성 대조(임시 복제본 · 사본) | AR-01 `extra=1 multi_group=1` · AR-02 `committed=1` 과 1 열여섯 · SK-08 `out_of_92=1` · DG-02 `md_new=2 sh_all=1` · AP-03 `v6_rc=2` · `v6_bare` 1 · AP-04 `v1_rc=2` · 이름 칸 0 · SK-04 칸 글자 그대로 bash · zsh 0 줄 / 실행 줄 1 줄 | — |
| DG-05 (시작 판 ci-local) | `rc=0` 22 · `feedback-agg-test SKIP (yq 없음)` 한 줄 | — |
| 실제 도구(사본 · 조건으로 잠그지 않는 참고) | `claude -p --model haiku --no-session-persistence` 를 사본 설정에서: 사용자 · 프로젝트 SessionStart · UserPromptSubmit 표식 넷, `--safe-mode` 를 더하면 0 · 실제 로그인 환경 `-p --safe-mode --setting-sources local --model haiku --no-session-persistence` → 종료 코드 0 · `ok` · 로그 폴더 수 42 그대로 | — |

## 리서치 소스

- 저장소 안: 핸드오프 `.harness/handoff/2026-09-26-0110.md` §C3(본 체크아웃) · `.harness/.meta/kaizen-0924/f1-kit-followups-notes.md` 입력 36 · 42 · 44 · 50 · 52 · 56 행과 「다음 사이클 메모」 · `f2-review-fixes-notes.md` 「고치지 않은 항목과 이유」 · 「다음 사이클 메모」 · `final-notes.md` FN-56 · `phase15-notes.md:48` · `:135` · `phase16-notes.md` 「넘기는 것」 · `.harness/sprint-contract-kaizen-0924-p12-reflect-kit.md` 봉인 전 실측 절 · `sprint-contract-kaizen-0924-p15-tone-kit.md:590-606` · `docs/api/research-log.md:161-175`
- 이 맥 실측(읽기만, 웹 조회 없음): `~/.claude/logs/claude-plugins/reflections-2026-09.md` · `reflections-2026-08.md` · `.errors.log` · `~/.claude/settings.json` 훅 목록 · `claude --help`(2.1.268) · 설치본 `/Applications/BambuStudio.app`(02.08.02.61) · `/Applications/OrcaSlicer.app`(2.4.2) 의 H2S 기계 프로파일
