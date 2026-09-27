---
feature: "2026-09-26 남은 일 vs 묶음 — 카이젠 오케스트레이터 · 킷 카이젠 스킬 문서 · 루트 README (감사 기록 제목 · Final 감시 거리 · 범위 줄 scripts/templates · 판 번호 원본 목록 · 강도 칸 앞머리 · 형제 표 새 행)"
slug: after-0926-orchestrator-docs
created: "2026-09-27 02:37"
complexity: "복잡"
conditions: 29
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:b58978bc9d7b1b4f
measurement_digest: sha256:e55ee0c47d0dedbc
locked_at: "2026-09-27 10:07"
---

## 배경

- 사용자 위임 — 이 계약의 합의(sprint-contract Step 5)는 아래 위임으로 받은 것으로 적는다. 사용자에게 따로 묻지 않았다.
  - user `2026-09-26T10:09:00.557Z` 「123다실행해 그러면끝나?다음카이젠에왜넘기는데?」 — 넘긴 것도 지금 처리하라는 뜻 (세션 `bda55d45-296c-491f-89ba-b52042d58e72`)
  - AskUserQuestion 답 `2026-09-26T10:30:16.222Z` — 결정 표(`decisions.md`)의 UD-3 등. 이 묶음 항목에 직접 걸린 결정은 없다
  - 그 전 위임 `2026-09-24T04:04:16.964Z` 「나한테 물어보지 말고 자동으로 끝까지」
  - 봉인된 조건을 느슨하게 하는 개정(허용 파일 늘리기 · 측정 대상 줄이기 · 문턱 낮추기)은 이 위임으로 동의 처리하지 않는다. 그런 개정은 개정 파일에 동의 칸을 비워 두고 부모가 사용자에게 묻는다
- 묶음: 남은 일 목록 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/leftovers.md` 「## vs」 절의 VS-3 · VS-7 · VS-8 · VS-11 · VS-16 · VS-17 · VS-18 · VS-19 · VS-20 · VS-22 · VS-23 · VS-25. 결정 파일은 같은 폴더 `decisions.md`, 바깥 문서 원문 대조는 같은 폴더 `ex/EX-<번호>.md`(이 묶음 항목을 가리키는 것은 없다).
- 작업 폴더 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-vsb`, 가지 `chore/ak2-vsb`, 시작 판 `6378948` (= origin/main, 목록의 줄 번호 기준 판). 시작할 때 `git status --short` 는 비어 있었고 앞 단계가 남긴 파일은 없었다(이 계약 파일은 Step 0.5 가 선점한 빈 파일로 시작). 이 가지는 한 주체만 커밋한다 — 범위는 시작 판에서 가지 끝까지의 누적 차이로 잰다.
- 같은 판에서 다른 묶음이 같은 파일을 고칠 수 있다 — 특히 vsa 묶음(`chore/ak2-vsa`)이 `scripts/sync-orchestrator.py:125-148` 과 `scripts/collect-kaizen-data.py:403-421` 을 고쳤다. 이 묶음은 `sync-orchestrator.py:39` 와 `collect-kaizen-data.py:1704` · `:1708` 만 고치고 이 묶음 항목에 없는 절은 건드리지 않는다. 기존 markdownlint 경고 정리(VS-26)와 로컬 CI 도구 단계(VS-24)는 부모 몫이다.

## 리서치 소스

- 바깥 문서는 새로 찾지 않았다. 열두 항목 모두 저장소 안 동작과 기록만 다룬다 — 바깥 근거 없음.
- 저장소 안 근거:
  - VS-3 — `.harness/.meta/after-kaizen-0926/c1a-notes.md:118` (V8 설명 옛 글), 현행 설명 `harness/docs/guides/plugin-validation-guide.md:391-424`
  - VS-7 · VS-8 — `c1a-notes.md:32` · `:114`, `kaizen-0924/final-notes.md:216-218` (계약 밖 결함 2 — 감시 목록이 실패 목록에서만 만들어진다)
  - VS-11 — `c1b-notes.md:41` · `:197` (N7)
  - VS-16 — `c3c-notes.md:110-111`, 정본 `api-kit/skills/api-verify/SKILL.md:133` (「`.hurl` 에도 적을 수는 있다 … 한쪽 경로가 없으면 Hurl 이 종료 코드 `3` … 판정 불가를 표현할 곳이 없다」)
  - VS-17 — `c4c-notes.md:145-151`
  - VS-18 — `d2-notes.md:34`, 현행 원칙 `.claude/skills/docs-site/SKILL.md:16` (공통 파일 `docs/assets/site.css` 링크 한 줄 + 인라인 `<style>`)
  - VS-19 — `kaizen-0924/phase6-notes.md:128` · `phase7-notes.md:80` · `phase9-notes.md:92`, F1H-44 (`f1-harness-followups-notes.md:117`)
  - VS-20 — `kaizen-0924/phase13-notes.md:51` · `:71-72` · `:99`, F1H-59 · F1H-60 (`f1-harness-followups-notes.md:122-123`), 현행 순서 `bambu-kit/skills/bambu-print-profile/SKILL.md:2446-2463` 「MakerWorld 읽는 순서」 · 음성 대조 절 `:1833`
  - VS-22 · VS-23 — `kaizen-0924/final-notes.md:221-225` (측정 구멍 2 · 3)
  - VS-25 — F2 Final 메모 (목록 비고), sync-docs 루트 처리 `scripts/sync-docs.py:330-338` · `:468-483`

## GAP 분석 · 개선안

### 복잡도 4 축

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 계층을 관통하나 | 스크립트 둘(감사 기록 · 오케스트레이터 동기화) · 데이터 풀 수집기 · 오케스트레이터 스킬과 참조 둘 · 개별 카이젠 스킬 일곱 · 루트 README — 다섯 |
| 공개 API·계약 변경 | 출력 모양이 바뀌나 | 예 — 감사 기록 제목 모양, 오케스트레이터 범위 줄, 데이터 풀 표 글 |
| 소비면 존재 | 받아 쓰는 쪽이 있나 | 예 — 다음 사이클 Step 0.5 가 감사 기록을 읽고, Phase 서브에이전트가 범위 줄 · 조사 지침을 읽는다. 문서 사이트 `docs/process/kaizen-flow.html` 이 오케스트레이터를 원본으로 삼는다 |
| 회귀 위험 | 기존 동작이 깨질 길 | 예 — 감사 기록은 덧붙이기만 해야 하고, 범위 줄 자동 생성이 어긋나면 CI 의 오케스트레이터 동기화 단계가 멈춘다 |

네 축 모두 예 → **복잡**. 기능 조건 수는 19 로 가이드(9~20) 안이다 (Step 6.2 둘째 명령 실측).

### 설정 리터럴 대조표

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | `bash -n scripts/release.sh` (DG-01 N/A 사유) |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | 같은 글자 (DG-03 N/A 사유) |
| `diagnostics.ide_exclude` | `[]` | 없음 — DG-02 는 markdownlint · 파이썬 컴파일로 잰다 |
| `contract_categories[].id` / `prefix` | `Skill`/`SK` · `Script`/`SC` · `Error`/`ER` · `Architecture`/`AR` | 같은 넷 |
| `anti_patterns[].id` / `message` | `AP-01` 버전 하드코딩 · `AP-02` force push · `AP-03` bare code fence (`python3 scripts/validate-plugin.py --check=code-fence`) · `AP-04` frontmatter name 누락 | 넷 모두 (AP-03 은 킷 밖 파일까지 재려고 같은 CommonMark 규칙의 도우미를 쓴다) |

### 편집 전 감사 — 시작 판 `6378948` 을 실제로 읽은 줄

| 대상 파일 | 읽은 증거 (`파일:줄`) | 발견한 갭 | 조건 |
| --------- | --------------------- | --------- | ---- |
| `.claude/skills/react-kaizen/SKILL.md` | `:97` `\| V8 hook-exec \| hooks.json 이 직접 실행하는 .sh 의 실행 비트(0755) \|` | 따옴표 검사가 빠진 옛 글. 전수 찾기(`grep -rn 'V8' .claude/skills harness/skills`)는 이 한 줄뿐, 킷 쪽 `flutter-toolkit/skills/flutter-kaizen/SKILL.md:248` 은 「hook-exec 회귀 가드」 라고만 해 틀린 글이 아니다 | SK-01 |
| `scripts/append-audit-log.py` | `:137-141` 소제목 꼬리 `{오늘} — {사이클}` · `:153` · `:164` · `:176` 하위 제목 셋이 같은 꼬리 · `:239-241` 기록 없음 종료 코드 2 · `:246-253` phase 인자 모자람 종료 코드 2 · `:282-288` 덧붙이기만 | 같은 날 같은 사이클로 두 번 부르면 제목 넷이 겹친다(사본 실측 `dup=4 md024=4`) | SC-01 · ER-01 |
| `.claude/skills/kaizen-orchestrator/SKILL.md` | `:33` 「Step 11 Final 종료 시」 · `:303` · `:307` `fit-pal` · `:362` 「Step 11 이후에 기록」 · `:581` `### Step F1` (구 Step 11) · `:583-603` F1 조건 목록(판 번호 목록을 뽑는 법 없음) · `:620` F2 「standalone」 · `:702-784` F4 (감사 기록 도구 호출 없음) | Final 이 감사 기록 도구를 `--watch` 로 부르는 걸음이 없다. 옛 단계 이름 둘 · 앱 이름 둘 · 옛 원칙 낱말 하나 | SK-02 · SK-05 · SK-06 · SK-10 |
| `scripts/sync-orchestrator.py` | `:37-39` `KIT_SCOPE_DIRS` 여섯(`references/` · `skills/*/references/` · `agents/` · `hooks/` · `docs/` · `evals/`) · `:99-110` 있는 폴더만 적음 | 킷 `scripts/` · `templates/` 없음. 있는 킷: scripts 여섯(flutter-toolkit · design-kit · react-kit · reflect-kit · bambu-kit · howto-kit), templates 다섯(flutter-toolkit · design-kit · rust-kit · react-kit · tone-kit) — `test -d` 실측 | SC-02 · ER-02 |
| `.claude/skills/kaizen-orchestrator/references/phase-dependencies.md` | `:23-86` Phase 5~17 블록 | 같은 열한 폴더가 없다 | SK-03 |
| `.claude/skills/kaizen-orchestrator/references/phase-research-templates.md` | `:78` `fit-pal/` · `:130` `fit-pal server` · `:261-262` 「경로 간 불변식은 Hurl 로 표현할 수 없다」 | 앱 이름 둘, 바로잡힌 단정 하나 | SK-04 · SK-05 |
| `scripts/collect-kaizen-data.py` | `:1704` · `:1708` 데이터 풀 §6 표의 Flutter · Rust 행에 `fit-pal` | 오케스트레이터 표와 같은 글의 사본 — 이것을 두면 데이터 풀로 앱 이름이 다시 들어간다 | SK-05 |
| `.claude/skills/design-kaizen/SKILL.md` · `backend-kaizen/SKILL.md` · `rust-kaizen/SKILL.md` | Gotcha 6 표 `design-kaizen:21-29` · `backend-kaizen:22-30` · `rust-kaizen:23-32` | 새 행 없음. 형제 쪽 실재: `design-kit/references/visual-change-protocol.md:19` · `:145` · `:161`, `flutter-toolkit/references/visual-evidence-protocol.md:106`, `react-kit/references/render-evidence-protocol.md:88` · `:110`, `backend-kit` 의 `시각 종류`(system · guide · audit-criteria), `rust-kit/skills/rust-preflight/SKILL.md:87` · `:169-176`, `rust-audit/SKILL.md:123` · `rust-reviewer` 의 `UNVERIFIED_INVALID_EVIDENCE` · `env_gaps` | SK-07 |
| `.claude/skills/bambu-kaizen/SKILL.md` · `.claude/skills/bambu-research/SKILL.md` | `bambu-kaizen:52` 「MakerWorld Cloudflare」 · `:67-75` Step 4 에 음성 대조 실행 줄 없음 · `bambu-research:17` · `:45-48` 브라우저 서버 이름 `mcp__playwright__` 셋 · 「Cloudflare bot challenge 우회」 | 킷의 현행 순서(JSON 주소 먼저 · 서버 이름 박지 않기 · 403 에서 기다리지 않기)와 어긋남 | SK-08 · SK-09 |
| `.claude/skills/tone-kaizen/SKILL.md` | `:38-52` Step 2 격차 표 (`:43` 「강도 정합」 행) 「강도 정합」 · 판정 방법 없음 | 강도 칸에 글이 덧붙은 줄(`tone-kit/references/adapter-dart-flutter.md:40` D-04)을 못 읽는 판정이 되풀이될 수 있다 | SK-11 |
| `README.md` | `:137-260` 킷 절 열(harness ~ bambu-kit), AUTO 스킬 블록 넷(`:148` · `:166` · `:206` · `:220`), `:254` 「references 4종」 | onboarding · tone · api · howto 절 없음, 블록 열 개 없음, bambu 참조 문서는 9 개(`find … -name '*.md'` 실측) | AR-03 |

구현 후보가 둘 이상인 곳과 고른 것:

- VS-7 제목 겹침 — (a) 항목 종류(시작 · 끝)를 제목에 / (b) 시각을 제목에 / (c) 같은 제목이 이미 있으면 차례 번호. (a) 만으로는 끝 항목을 두 번 부르면 또 겹치고, (b) 만으로는 같은 초에 두 번 부르면 겹친다. 조건은 결과(같은 날 같은 사이클 두 항목의 제목 겹침 0)만 정하고 방법은 구현이 고른다. 목록의 둘째 대상 `SKILL.md:362`(Step 0.5 가 사이클 시작에 빈 항목을 덧붙이는 줄)는 SC-01 의 두 번 부르기(첫째 = 시작 빈 항목 · 둘째 = Final 의 `--watch` 항목)와 SK-02(그 줄의 옛 이름 「Step 11」 을 Final 단계 이름으로)가 함께 잰다 — 구현은 `:362` 서술을 새 제목 모양 · Final 단계 이름과 맞게 고친다
- VS-8 Final 호출 자리 — 사이클 끝 기록이므로 F1 ~ F4 가운데 한 단계에 호출 줄을 둔다. 연동 스크립트 절(`:33`)은 그 단계 이름을 가리킨다. 감시 거리는 교차 진단 · 계약 밖 결함에서 온 것을 `--watch` 로 넘긴다
- VS-11 — `KIT_SCOPE_DIRS` 에 `scripts/` · `templates/` 를 더하고 스크립트로 오케스트레이터 자동 영역을 다시 만든다. 의존성 맵은 손으로 같은 열한 줄을 더한다. 없는 폴더는 적지 않는다(기존 `infer_scope_dirs` 규칙)
- VS-17 — 앱 이름을 「Hub 외부 프로젝트 (Flutter 앱)」 · 「(Rust 서버)」 처럼 종류로 바꾼다. **「킷 안 앱 이름 0 건」 검사는 두지 않는다** — 근거: (1) 이름이 다시 들어오는 길은 조사 입력 넷과 데이터 풀 표 둘인데 이 묶음이 여섯 자리를 모두 지운다, (2) 검사는 막을 앱 이름을 적은 금지 목록이 될 수밖에 없어 목록에 없는 다른 앱 이름은 통과시킨다(메모 `feedback_gate_blocklist_misses_unknown_keys`), (3) 저장소 전체로 걸면 harness 40 줄 · reflect-kit 4 줄이 실측 사례로 이미 이름을 쓰고 있어(`grep -rn -i fit-pal <킷>` 실측) 켜는 순간 실패하고, rust-kit 하나로 좁히면 이미 0 건인 곳을 지키는 공허한 통과에 가깝다. 이 판단은 notes `## 앱 이름 검사 판단` 절에 적는다
- VS-22 — 판 번호 원본 목록을 뽑는 bash 블록을 F1 절에 둔다. 첫 줄 주석은 `# 판 번호 원본 목록`, 입력은 셸 변수 `BASE` · `END`. 머리 설정(첫 `---` 블록)의 `version` 값이 두 판에서 다르고 끝 판에 값이 있는 `.md` 를 낸다. 스킬 본문이라 `$` + 숫자를 쓰지 않는다(인자 치환 — sprint-contract Gotcha)
- VS-23 — 강도 정합 판정을 bash 블록으로 Step 2 에 둔다. 첫 줄 주석은 `# 강도 칸 앞머리 판정`. 표 머리의 `강도` 칸 위치를 찾아 그 칸의 **앞머리**가 `MUST` · `SHOULD` · `관측 컨벤션` · `합성` 가운데 하나면 읽은 것으로 센다(`합성` 은 `tone-kit/references/core-naming.md:26` 이 선언한 강도). 출력 첫 줄 `rules=<N> read=<N> unread=<N>`, 못 읽은 줄마다 `UNREAD <파일>:<ID> <칸 글>`
- VS-25 — 네 킷 절을 marketplace 차례대로 더하고 열네 킷 모두에 `<!-- AUTO:skills-<킷> -->` 블록을 둔 뒤 `python3 scripts/sync-docs.py` 로 채운다. bambu 줄은 참조 문서 수를 실제 수로

### Counterpart — 바뀌는 모양을 받아 쓰는 반대편

| 바뀌는 것 (producer) | 받아 쓰는 쪽 (consumer) | 처리 |
| --- | --- | --- |
| 감사 기록 제목 모양 | 다음 사이클 Step 0.5 (`.claude/skills/kaizen-orchestrator/SKILL.md:350-354` — 파일을 읽어 이력 확인, 제목 모양에 기대지 않음) · 저장소의 기존 감사 기록 `.harness/.meta/orchestrator-audit-log.md` | 기존 기록은 고치지 않는다(덧붙이기만). SC-01 이 사본으로 잰다 |
| 오케스트레이터 범위 줄 | Phase 서브에이전트 · CI 동기화 단계(`sync-orchestrator.py --check-only`) · `docs/process/kaizen-flow.html` 카드 | 앞 둘은 SC-02 · DG-05. 페이지는 **미완 쪽** — 문서 묶음 · 부모가 드리프트 목록으로 다시 만든다. notes `## 문서 드리프트` 에 적는다 |
| 조사 입력 표의 앱 이름 | 데이터 풀 수집기 §6 표(`scripts/collect-kaizen-data.py:1704` · `:1708`) | 같은 커밋 범위에서 함께 바꾼다 — SK-05 |
| 루트 README 킷 절 | `scripts/sync-docs.py` 루트 처리 · CI 동기화 단계 | AR-03 · DG-05 |

### 조건 작성 자문

- 이진 판정 — 조건마다 도우미 출력 한 줄의 기대 글자를 적는다. 시작 판 출력도 같이 적어 고치기 전 판에서 FAIL 이 나는 것(양성 대조)을 보인다
- 새로 짠 측정(판 번호 목록 · 강도 칸 앞머리)은 손으로 셀 수 있는 답을 먼저 적는다(알려진 답)
- 구현 누수 — 조건은 파일 · 출력 글 · 종료 코드만 쓴다. SK-10 · SK-11 의 블록 첫 줄 주석과 출력 모양은 구현이 새로 만드는 이름이라 계약이 정한다

## 범위 경계

입력 항목마다 처리:

| 항목 | 처리 | 조건 |
| --- | --- | --- |
| VS-3 V8 설명 옛 글 | 계약에 넣음 — 전수 찾기 결과 대상은 `react-kaizen:97` 한 줄 | SK-01 |
| VS-7 감사 기록 제목 겹침 | 계약에 넣음 | SC-01 · ER-01 |
| VS-8 Final 의 `--watch` 호출 · 옛 단계 이름 | 계약에 넣음. 도구 쪽 `--watch` 는 `7f4559b` 로 이미 있다(처리됨) — 남은 것은 오케스트레이터 쪽 | SK-02 |
| VS-11 범위 줄 scripts · templates | 계약에 넣음 — 스크립트 · 자동 영역 · 의존성 맵. 문서 페이지는 미완 쪽 | SC-02 · SK-03 · ER-02 |
| VS-16 api 조사 지침 Hurl 단정 | 계약에 넣음 | SK-04 |
| VS-17 조사 입력 앱 이름 · 검사 여부 | 계약에 넣음 — 데이터 풀 수집기 표 두 줄도 함께. 검사는 두지 않는다(위 근거, notes 에 적음) | SK-05 · AR-02 |
| VS-18 F2 옛 원칙 | 계약에 넣음 | SK-06 |
| VS-19 형제 표 새 행 셋 | 계약에 넣음 | SK-07 |
| VS-20 bambu-kaizen · bambu-research | 계약에 넣음 | SK-08 · SK-09 |
| VS-22 판 번호 원본 목록 | 계약에 넣음 | SK-10 |
| VS-23 강도 칸 앞머리 | 계약에 넣음 | SK-11 |
| VS-25 루트 README 킷 절 | 계약에 넣음 | AR-03 |

범위 밖: 같은 절의 VS-1 · VS-2 · VS-4 ~ VS-6 · VS-9 · VS-10 · VS-12 ~ VS-15 · VS-21 · VS-27 (vsa 묶음), VS-24 · VS-26 (부모). 문서 페이지 `docs/process/kaizen-flow.html` · `docs/harness/plugin-validation.html` 다시 만들기(문서 묶음 · 부모), 루트 README `## 구조` 절 나무 그림(`:261-336` — 항목 줄 범위 `:137-260` 밖), `bambu-kit/README.md` 의 「references 4종」(킷 README — 킷 묶음 몫), 검증 가이드 V8 수동 수정 표(GD-1), `docs-site/SKILL.md` 의 standalone 글(DC-5), 킷 판 올림과 릴리스(부모), harness · reflect-kit 안의 실측 사례 앱 이름(이 묶음이 지우지 않는다 — 위 VS-17 근거).

커밋 규칙: `git add <경로>` 뒤 `git commit -o <경로>` · 킷 폴더는 건드리지 않는다(루트 README 는 킷 폴더가 아니다) · `git add -A` · `git stash` · 푸시 · 가지 바꾸기 금지 · main 을 합치지 않는다.

notes 경로: `.harness/.meta/after-kaizen-0926b/vsb-notes.md` — 구현이 쓴다. 적을 것: 항목 열둘의 처리와 커밋, `## 남은 것`(문서 페이지 · README 구조 절 · 킷 README · 판 올림 — 이유와 함께), `## tone-guide 결과`(1 단계 로드와 5 단계 전수 대조 표), `## 앱 이름 검사 판단`(VS-17 근거), `## 문서 드리프트`(`python3 scripts/detect-docs-drift.py --since 6378948` 출력).

커버리지 해소 (Step 6.5 (4) 검출기 몫):

- 커버리지 해소: AR-01 — 파일 열넷은 `scope.sh` 의 `REQUIRED` 가 글자 그대로 담는다(허용 목록 = 필수 목록). `.harness/` 규칙은 같은 도우미의 `HX=` 정규식이 잰다
- 커버리지 해소: SC-02 — 폴더 열하나는 `kitdirs.sh` 가 marketplace 킷마다 `test -d` 로 펼친다(실측 펼친 결과는 편집 전 감사 표 `sync-orchestrator.py` 행 · SK-03 조건 산문). 낱말 `scripts/` · `templates/` 는 폴더 종류 이름이지 대상 경로가 아니다
- 커버리지 해소: SK-03 — 같은 `kitdirs.sh` 가 킷마다 의존성 맵 블록(`.claude/skills/kaizen-orchestrator/references/phase-dependencies.md` 의 `Phase N: … (<킷>-kaizen)` 아래)을 잘라 열한 폴더를 하나씩 찾는다. 파일 경로는 도우미의 `D=` 가 담는다
- 커버리지 해소: SK-05 — 세 파일은 `orch.sh` 의 `O=` · `P=` · `C=` 가 글자 그대로 담는다(`SKILL.md` 는 `.claude/skills/kaizen-orchestrator/SKILL.md`)
- 커버리지 해소: SK-07 — 파일 이름과 낱말은 `kz.sh` 의 `grep` 사슬이 글자 그대로 담는다
- 커버리지 해소: AR-03 — 킷 열넷은 `readme.sh` 가 `.claude-plugin/marketplace.json` 에서 읽는다
- 오라클 해소: SK-04 — 산출물이 조사 서브에이전트가 읽는 지침 문장 자체라 동작이 없다. 잴 것은 틀린 단정이 사라졌는지와 정본 · 종료 코드 · 판정 불가를 적었는지이며, 시작 판에서 `cannot=1 verify_ref=0` 으로 FAIL 한다(양성 대조)

## 회귀 게이트 — 측정 공통 정의 · 도우미 · 봉인 전 실측

모든 측정은 **bash** 에서 돈다(zsh 는 따옴표 없는 변수를 쪼개지 않는다). SK-10 만 블록을 bash 와 zsh 두 셸로 돌린다. 도우미는 잴 판(`REF`, 비면 가지 끝 `chore/ak2-vsb`)을 `git archive` 로 임시 폴더에 풀고 거기서 잰다 — 작업 폴더는 건드리지 않는다. `END_UNRESOLVED` · `REF_UNRESOLVED` · `END_HAS_MERGE` · `PREMISE_FAIL` 이 찍히면 종료 코드 2 로 멈춘다. `HEAD` 로 바꿔 재지 않는다. 양성 대조용 기준 바꾸기는 `B_OVERRIDE=<판>` 이다.

도우미 준비 — 이 절의 bash 코드 블록을 블록 첫 `#` 줄(셔뱅 다음)의 이름으로 한 폴더에 저장하고 그 폴더를 `K` 에 넣는다:

```bash
# 이 계약에서 도우미 블록을 떼어 $K 에 저장한다 — 블록 첫 주석 줄의 이름(셔뱅 다음 줄)이 파일 이름이다
K=${K:?도우미 폴더}; mkdir -p "$K"
python3 - /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-vsb/.harness/sprint-contract-after-0926-orchestrator-docs.md "$K" <<'PY'
import re, sys, pathlib
src = open(sys.argv[1], encoding="utf-8").read(); K = pathlib.Path(sys.argv[2])
for body in re.findall(r"^```bash\n(.*?)^```$", src, re.S | re.M):
    lines = body.splitlines(); i = 1 if lines and lines[0].startswith("#!") else 0
    m = re.match(r"# ([\w.-]+\.sh) ", lines[i]) if len(lines) > i else None
    if m:
        (K / m.group(1)).write_text(body, encoding="utf-8")
PY
```

돌리는 법: `K=<폴더> bash "$K/<도우미>"` (시작 판으로 재려면 앞에 `REF=6378948`). 도우미 열하나: `audit.sh` (SC-01 · ER-01) · `orch.sh` (SK-02 · SK-05 · SK-06) · `ver.sh` (SK-10) · `kitdirs.sh` (SC-02 · SK-03 · ER-02) · `kz.sh` (SK-01 · SK-04 · SK-07 · SK-08 · SK-09) · `tone.sh` (SK-11) · `readme.sh` (AR-03) · `scope.sh` (AR-01 · AR-02) · `dg.sh` (DG-02 · AP-03) · `misc.sh` (AP-01 · AP-02 · AP-04 · DG-01 · DG-03) · `ci.sh` (DG-05).

준비 단계 실측 (2026-09-27 02:0x ~ 02:3x): markdownlint-cli2 `0.23.2` (`…/scratchpad/mdlint/node_modules/markdownlint-cli2/package.json`, 설정 `{ "config": { "MD013": false } }`) · `command -v node` → fnm 경로 · `command -v zsh` 있음 · 이 맥 `sed -i ''` (BSD) 로 사본 변이 · `python3` 는 도구 폴더 밖에서만 돈다 · 로컬 CI 도구 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` 지문 `sha256` 앞 16 자 `59fe55125c0dbc77` (추적 안 된 파일 — 평가 때 지문이 다르면 `.github/workflows/ci.yml` 의 `run:` 줄을 하나씩 돌린다). markdownlint 폴더는 이 세션의 임시 폴더라 다른 세션에는 없다 — `common.sh` 가 없으면 `TMPDIR` 아래 `vsb-mdlint` 에 같은 판을 설치하고, 설치도 못 하면 `MDL_UNAVAILABLE` 을 찍고 종료 코드 2 로 멈춘다(재지 않은 0 을 통과로 내지 않는다). 2026-09-27 10:1x 실측: 기본 폴더 · 없는 폴더를 준 설치 길 · `PATH=/usr/bin:/bin` 로 npm 을 숨긴 길에서 `audit.sh` 가 각각 같은 네 줄(`dup=4 md024=4` 포함) · 같은 네 줄 · `MDL_UNAVAILABLE` 종료 코드 2

```bash
# common.sh — 측정 공통 정의. bash 로 읽는다 (`. "$K/common.sh"`)
export LC_ALL=C.UTF-8
W=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-vsb
B=${B_OVERRIDE:-6378948}
BR=chore/ak2-vsb
MDL=${MDL:-/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/mdlint}
# 위 폴더는 계약 작성 세션의 임시 폴더라 다른 세션에는 없다 — 없으면 TMPDIR 아래에 같은 판을 설치하고, 그래도 없으면 재지 않고 멈춘다
MDL_BIN="$MDL/node_modules/markdownlint-cli2/markdownlint-cli2-bin.mjs"
if [ ! -f "$MDL_BIN" ] || [ ! -f "$MDL/cfg.markdownlint-cli2.jsonc" ]; then
  MDL="${TMPDIR:-/tmp}/vsb-mdlint"; MDL_BIN="$MDL/node_modules/markdownlint-cli2/markdownlint-cli2-bin.mjs"
  if [ ! -f "$MDL_BIN" ]; then mkdir -p "$MDL" && (cd "$MDL" && npm install --silent --no-audit --no-fund markdownlint-cli2@0.23.2 >/dev/null 2>&1); fi
  printf '{ "config": { "MD013": false } }\n' > "$MDL/cfg.markdownlint-cli2.jsonc"
fi
[ -f "$MDL_BIN" ] && command -v node >/dev/null 2>&1 || { echo "MDL_UNAVAILABLE $MDL"; exit 2; }
# 잴 판 — REF 가 비면 가지 끝. HEAD 로 떨어지지 않는다
resolve_ref() {
  local r
  if [ -z "${REF:-}" ] || [ "$REF" = END ]; then
    r=$(git -C "$W" rev-parse --verify -q "refs/heads/$BR") || { echo END_UNRESOLVED; exit 2; }
  else
    r=$(git -C "$W" rev-parse --verify -q "$REF^{commit}") || { echo "REF_UNRESOLVED $REF"; exit 2; }
  fi
  printf '%s\n' "$r"
}
# unpack <commit> — 그 판을 임시 폴더에 풀고 경로를 찍는다. 작업 폴더는 건드리지 않는다
unpack() {
  local d
  d=$(mktemp -d "${TMPDIR:-/tmp}/vsb.XXXXXX") || exit 2
  git -C "$W" archive "$1" | tar -x -C "$d" || exit 2
  printf '%s\n' "$d"
}
# mdl <폴더> <파일...> — 편집기와 같은 설정(MD013 끔)의 markdownlint-cli2 0.23.2
mdl() { local d=${1}; shift; (cd "$d" && node "$MDL/node_modules/markdownlint-cli2/markdownlint-cli2-bin.mjs" --config "$MDL/cfg.markdownlint-cli2.jsonc" "$@" 2>&1); }
```

```bash
#!/usr/bin/env bash
# audit.sh — SC-01 · ER-01: 감사 기록 도구를 같은 날 같은 사이클로 두 번 부를 때 제목 겹침 · 덧붙이기만 · --watch · phase 모드
K=${K:?}; . "$K/common.sh"; R=$(resolve_ref); T=$(unpack "$R")
L="$T/.harness/.meta/orchestrator-audit-log.md"
run() { (cd "$T" && python3 scripts/append-audit-log.py "$@" >/dev/null 2>&1); echo $?; }
# (1) 실제 감사 기록 사본 — 두 번 덧붙여도 옛 내용이 한 글자도 안 바뀐다
cp "$L" "$T/orig.md"; n0=$(wc -c < "$T/orig.md" | tr -d ' ')
r1=$(run --cycle-id vsb-test --notes 시작); r2=$(run --cycle-id vsb-test --notes 끝 --watch 감시거리)
kept=$(head -c "$n0" "$L" | cmp -s - "$T/orig.md" && echo 1 || echo 0)
echo "real rc=$r1,$r2 kept=$kept grew=$([ "$(wc -c < "$L" | tr -d ' ')" -gt "$n0" ] && echo 1 || echo 0)"
# (2) 새 기록 — 같은 날 같은 사이클 두 항목의 제목이 겹치지 않는다
printf '# 감사 기록\n' > "$L"
r1=$(run --cycle-id vsb-test --notes 시작); r2=$(run --cycle-id vsb-test --notes 끝 --watch 감시거리)
dup=$(grep -E '^#{1,6} ' "$L" | sort | uniq -d | grep -c .)
m24=$(mdl "$T" .harness/.meta/orchestrator-audit-log.md | grep -c 'MD024')
echo "fresh rc=$r1,$r2 entries=$(grep -c '^## ' "$L") heads=$(grep -cE '^#{1,6} ' "$L") dup=$dup md024=$m24 watch=$(grep -cxF -- '- [ ] 감시거리' "$L")"
# (3) phase 모드 — 같은 사이클 두 줄은 머리 하나 아래에 모인다
printf '# 감사 기록\n' > "$L"
p1=$(run --cycle-id vsb-test --phase 3 --result pass --date 2026-09-27); p2=$(run --cycle-id vsb-test --phase 4 --result fail --date 2026-09-27)
echo "phase rc=$p1,$p2 head=$(grep -c '^### Phase log — vsb-test$' "$L") rows=$(grep -c '^- Phase [34] — ' "$L")"
# (4) 오류 길 — 감사 기록이 없거나 phase 모드 인자가 모자라면 종료 코드 2, 기록은 그대로
printf '# 감사 기록\n' > "$L"; e1=$(run --cycle-id vsb-test --phase 3); same=$(grep -c . "$L")
rm -f "$L"; e2=$(run --cycle-id vsb-test --notes x); made=$([ -e "$L" ] && echo 1 || echo 0)
echo "error phase_only_rc=$e1 lines_after=$same no_log_rc=$e2 log_created=$made"
rm -rf "$T"
```

```bash
#!/usr/bin/env bash
# orch.sh — SK-02 · SK-05 · SK-06: 오케스트레이터 옛 단계 이름 · Final 감사 기록 호출 · 앱 이름 · F2 원칙
K=${K:?}; . "$K/common.sh"; R=$(resolve_ref); T=$(unpack "$R")
O="$T/.claude/skills/kaizen-orchestrator/SKILL.md"
P="$T/.claude/skills/kaizen-orchestrator/references/phase-research-templates.md"
C="$T/scripts/collect-kaizen-data.py"
# SK-02 — 옛 이름 「Step 11」 이 Final 을 가리키는 줄(Phase 11 절 제목 · 「구 Step 11」 이력 표기는 뺀다)
old=$(grep -nE 'Step 11([^:.0-9]|$)' "$O" | grep -vE '### Step 11: Phase 11|구 Step 11' | grep -c .)
# 연동 스크립트 절의 감사 기록 도구 줄이 가리키는 Final 단계 이름
line=$(awk '/^## 연동 스크립트/{f=1;next} /^## /{f=0} f && /append-audit-log\.py/' "$O")
step=$(printf '%s\n' "$line" | grep -oE 'Step F[0-9.]+' | head -1)
# 그 단계 절(### <step>: … 부터 다음 ### 전)에 --watch 를 넘기는 감사 기록 도구 호출 줄
call=0; [ -n "$step" ] && call=$(awk -v s="### $step:" 'index($(0), s)==1{f=1;next} /^###? /{f=0} f' "$O" | grep 'append-audit-log\.py' | grep -c -- '--watch')
s05=$(awk '/^### Step 0\.5:/{f=1;next} /^###? /{f=0} f' "$O" | grep -c 'Step 11')
echo "SK02 old_step11=$old link_step=[${step:-없음}] watch_call=$call step05_step11=$s05"
# SK-05 — 조사 입력의 앱 이름 (오케스트레이터 · 조사 지침 · 데이터 풀 수집기의 같은 표)
echo "SK05 orch=$(grep -ci 'fit-pal' "$O") templates=$(grep -ci 'fit-pal' "$P") collector_table=$(grep -E '^ +"\| (5 Flutter|9 Rust) ' "$C" | grep -ci 'fit-pal')"
# SK-06 — F2 절의 옛 원칙 낱말과 공통 스타일 파일
f2=$(awk '/^### Step F2:/{f=1;next} /^###? /{f=0} f' "$O")
echo "SK06 standalone=$(printf '%s\n' "$f2" | grep -ci 'standalone') site_css=$(printf '%s\n' "$f2" | grep -cF 'docs/assets/site.css')"
rm -rf "$T"
```

```bash
#!/usr/bin/env bash
# ver.sh — SK-10: Final F1 절의 「판 번호 원본 목록」 블록을 떼어 2026-09-24 사이클(77ed5bb^1..77ed5bb)에 돌리고 기준 목록과 맞댄다
K=${K:?}; . "$K/common.sh"; R=$(resolve_ref); T=$(unpack "$R")
O="$T/.claude/skills/kaizen-orchestrator/SKILL.md"
# F1 절 안, 첫 줄이 「# 판 번호 원본 목록」 인 bash 블록 본문
awk '/^### Step F1:/{f=1;next} /^### /{f=0} f' "$O" \
  | awk 'm==0 && /^ *```bash *$/{b=1; buf=""; next} b && /^ *```/{if (hit) {printf "%s", buf; exit} b=0; next} b{ if (buf=="" && $(0) ~ /# 판 번호 원본 목록/) hit=1; buf=buf $(0) "\n"}' > "$T/blk.sh"
blk=$(grep -c . "$T/blk.sh"); argsub=$(grep -cE '\$[0-9]' "$T/blk.sh")
# 기준 목록 — 머리 설정(첫 --- 블록)의 version 값이 두 판에서 다르고 끝 판에 값이 있는 .md
fmv() { git -C "$W" show "${1}:${2}" 2>/dev/null | awk 'NR==1&&/^---/{f=1;next} f&&/^---/{exit} f&&/^version:/{sub(/^version:[ \t]*/,""); print; exit}'; }
git -C "$W" diff --name-only 77ed5bb^1 77ed5bb -- '*.md' | while read -r f; do
  n=$(fmv 77ed5bb "$f"); o=$(fmv 77ed5bb^1 "$f"); [ -n "$n" ] && [ "$o" != "$n" ] && echo "$f"; done | sort > "$T/ref.txt"
for sh in bash zsh; do
  (cd "$W" && BASE=77ed5bb^1 END=77ed5bb $sh "$T/blk.sh" 2>"$T/$sh.err") | grep -oE '[^ ]+\.md' | sort -u > "$T/$sh.txt"
  eq=$(cmp -s "$T/ref.txt" "$T/$sh.txt" && echo 1 || echo 0)
  seven=0; for p in api-design cicd data-modeling flows prd-patterns sqlx-patterns visual-evidence-protocol; do grep -q "/$p\.md$" "$T/$sh.txt" && seven=$((seven + 1)); done
  echo "SK10 $sh block_lines=$blk argsub=$argsub ref=$(grep -c . "$T/ref.txt") got=$(grep -c . "$T/$sh.txt") equal=$eq seven=$seven/7 err=$(grep -c . "$T/$sh.err")"
done
rm -rf "$T"
```

```bash
#!/usr/bin/env bash
# kitdirs.sh — SC-02 · SK-03 · ER-02: 오케스트레이터 범위 줄 · Phase 의존성 맵에 킷 scripts/ · templates/
K=${K:?}; . "$K/common.sh"; R=$(resolve_ref); T=$(unpack "$R")
O="$T/.claude/skills/kaizen-orchestrator/SKILL.md"; D="$T/.claude/skills/kaizen-orchestrator/references/phase-dependencies.md"
KITS=$(cd "$T" && python3 -c "import json;print(' '.join(p['name'] for p in json.load(open('.claude-plugin/marketplace.json'))['plugins'] if p['name']!='harness'))")
chk=$(cd "$T" && python3 scripts/sync-orchestrator.py --check-only >/dev/null 2>&1; echo $?)
want=0; hitO=0; hitD=0; extraO=0; extraD=0
for k in $KITS; do
  scope=$(awk -v h="— $k 카이젠" 'index($(0), h) && /^### Step /{f=1;next} /^### /{f=0} f && /^\*\*범위:\*\*/' "$O")
  blk=$(awk -v h="($(printf '%s' "$k" | sed -E 's/-toolkit$|-kit$//')-kaizen)" '/^Phase [0-9]+:/{f=index($(0), h)>0; next} f' "$D")
  for d in scripts templates; do
    if [ -d "$T/$k/$d" ]; then
      want=$((want + 1))
      printf '%s\n' "$scope" | grep -qF "\`$k/$d/\`" && hitO=$((hitO + 1)) || echo "  범위 줄 빠짐: $k/$d/"
      printf '%s\n' "$blk" | grep -qE "^ +$k/$d/" && hitD=$((hitD + 1)) || echo "  의존성 맵 빠짐: $k/$d/"
    else
      printf '%s\n' "$scope" | grep -qF "$k/$d/" && extraO=$((extraO + 1))
      printf '%s\n' "$blk" | grep -qE "^ +$k/$d/" && extraD=$((extraD + 1))
    fi
  done
done
echo "SC02 check_only_rc=$chk want=$want scope_line=$hitO/$want extra=$extraO"
echo "SK03 dep_map=$hitD/$want extra=$extraD"
# ER-02 — 범위 줄 하나에서 폴더 하나를 지운 사본은 --check-only 가 어긋남(종료 코드 1)으로 잡는다
sed -i '' -e 's#, `flutter-toolkit/evals/`##' "$O"; left=$(grep -cF '`flutter-toolkit/evals/`' "$O")
drift=$(cd "$T" && python3 scripts/sync-orchestrator.py --check-only >/dev/null 2>&1; echo $?)
echo "ER02 mutated_left=$left drift_rc=$drift"
rm -rf "$T"
```

```bash
#!/usr/bin/env bash
# kz.sh — SK-01 · SK-04 · SK-07 · SK-08 · SK-09: 개별 카이젠 스킬 문서와 조사 지침의 고친 자리
K=${K:?}; . "$K/common.sh"; R=$(resolve_ref); T=$(unpack "$R"); S="$T/.claude/skills"
# SK-01 — react-kaizen 검사 표의 V8 행이 실행 비트와 따옴표를 함께 적는다
v8=$(grep -E '^\| *V8 ' "$S/react-kaizen/SKILL.md")
echo "SK01 v8_rows=$(printf '%s' "$v8" | grep -c .) exec_bit=$(printf '%s' "$v8" | grep -c '실행 비트') quote=$(printf '%s' "$v8" | grep -c '따옴표')"
# SK-04 — api 조사 지침(Phase 16 절)의 바로잡힌 문장
P="$S/kaizen-orchestrator/references/phase-research-templates.md"
p16=$(awk '/^## Phase 16/{f=1;next} /^## /{f=0} f' "$P")
echo "SK04 cannot=$(grep -c 'Hurl 로 표현할 수 없다' "$P") verify_ref=$(printf '%s\n' "$p16" | grep -cF 'api-kit/skills/api-verify/SKILL.md') exit3=$(printf '%s\n' "$p16" | grep -c '종료 코드 `\{0,1\}3') unjudgeable=$(printf '%s\n' "$p16" | grep -c '판정 불가')"
# SK-07 — Gotcha 6 형제 표(6 번 항목부터 7 번 항목 전까지)의 새 행
g6() { awk '/^6\. \*\*Cross-Surface Parity/{f=1;next} /^[0-9]+\. \*\*/{f=0} f && /^ *\| /' "$S/${1}/SKILL.md"; }
d=$(g6 design-kaizen | grep '편집 전 확정' | grep '비교 반복 순서' | grep '캡처 점검 목록' | grep 'visual-change-protocol' | grep 'visual-evidence-protocol' | grep -c 'render-evidence-protocol')
b=$(g6 backend-kaizen | grep '시각 종류' | grep 'backend-system' | grep 'backend-guide' | grep -c 'backend-audit')
rf=$(g6 rust-kaizen | grep '실패 원인' | grep -c 'rust-preflight')
ru=$(g6 rust-kaizen | grep 'UNVERIFIED_INVALID_EVIDENCE' | grep 'env_gaps' | grep 'rust-audit' | grep -c 'rust-reviewer')
T0=$(unpack "$B"); lost=0
for k in design-kaizen backend-kaizen rust-kaizen; do
  S0="$T0/.claude/skills"; n=$(awk '/^6\. \*\*Cross-Surface Parity/{f=1;next} /^[0-9]+\. \*\*/{f=0} f && /^ *\| /' "$S0/$k/SKILL.md" | while IFS= read -r l; do g6 "$k" | grep -qxF -- "$l" || echo x; done | grep -c .)
  lost=$((lost + n))
done; rm -rf "$T0"
echo "SK07 design_row=$d backend_row=$b rust_fail_row=$rf rust_counter_row=$ru rows=$(g6 design-kaizen | grep -c .),$(g6 backend-kaizen | grep -c .),$(g6 rust-kaizen | grep -c .) old_rows_lost=$lost"
# SK-08 — bambu-kaizen 격차 표 fallback 행 · 회귀 검증의 음성 대조 실행 줄
BK="$S/bambu-kaizen/SKILL.md"
fb=$(grep -E '^\| \*\*fallback 체인\*\*' "$BK")
s4=$(awk '/^## Step 4/{f=1;next} /^## /{f=0} f' "$BK")
echo "SK08 cloudflare=$(grep -ci 'cloudflare' "$BK") fallback_order=$(printf '%s' "$fb" | grep -c 'MakerWorld 읽는 순서') step4_neg=$(printf '%s\n' "$s4" | grep '음성 대조' | grep -cF 'bambu-kit/skills/bambu-print-profile/SKILL.md')"
# SK-09 — bambu-research 의 MakerWorld 받는 순서
BR="$S/bambu-research/SKILL.md"
echo "SK09 server_name=$(grep -o 'mcp__playwright__' "$BR" | grep -c .) bypass=$(grep -c '우회' "$BR") order_ref=$(grep -c 'MakerWorld 읽는 순서' "$BR") skill_ref=$(grep -cF 'bambu-kit/skills/bambu-print-profile/SKILL.md' "$BR")"
rm -rf "$T"
```

```bash
#!/usr/bin/env bash
# tone.sh — SK-11: tone-kaizen 「강도 칸 앞머리 판정」 블록을 떼어 지금 tone-kit 과 망가뜨린 사본에 돌린다
K=${K:?}; . "$K/common.sh"; R=$(resolve_ref); T=$(unpack "$R")
TK="$T/.claude/skills/tone-kaizen/SKILL.md"
# 첫 줄이 「# 강도 칸 앞머리 판정」 인 bash 블록 본문
awk 'b==0 && /^ *```bash *$/{b=1; buf=""; next} b && /^ *```/{if (hit) {printf "%s", buf; exit} b=0; next} b{ if (buf=="" && $(0) ~ /# 강도 칸 앞머리 판정/) hit=1; buf=buf $(0) "\n"}' "$TK" > "$T/blk.sh"
blk=$(grep -c . "$T/blk.sh"); s2=$(awk '/^## Step 2/{f=1;next} /^## /{f=0} f' "$TK" | grep -c '# 강도 칸 앞머리 판정')
run() { (cd "$T" && bash "$T/blk.sh" 2>&1); }
o=$(run); sum=$(printf '%s\n' "$o" | grep -E '^rules=' | head -1)
echo "SK11 block_lines=$blk in_step2=$s2 now=[$sum] unread_lines=$(printf '%s\n' "$o" | grep -c '^UNREAD ')"
# 양성 대조 — D-04 강도 칸을 앞머리가 네 값 밖인 글로 바꾼 사본
A="$T/tone-kit/references/adapter-dart-flutter.md"; cp "$A" "$T/a.bak"
sed -i '' -E 's/^(\| D-04 \|.*\| )관측 컨벤션 \(성능 근거는 SHOULD 수준\) \|$/\1기타 (메모) |/' "$A"
applied=$(grep -c '^| D-04 .*| 기타 (메모) |$' "$A")
o=$(run); echo "SK11 broken applied=$applied [$(printf '%s\n' "$o" | grep -E '^rules=' | head -1)] d04=$(printf '%s\n' "$o" | grep '^UNREAD ' | grep -c 'D-04')"
rm -rf "$T"
```

```bash
#!/usr/bin/env bash
# readme.sh — AR-03: 루트 README 킷 절 · 스킬 블록 · bambu references 수 · sync-docs 동기화
K=${K:?}; . "$K/common.sh"; R=$(resolve_ref); T=$(unpack "$R"); M="$T/README.md"
KITS=$(cd "$T" && python3 -c "import json;print(' '.join(p['name'] for p in json.load(open('.claude-plugin/marketplace.json'))['plugins']))")
sec() { awk -v h="### ${1}" '$(0)==h{f=1;next} /^##+ /{f=0} f' "$M"; }
DET=$(awk '/^## 플러그인 상세/{f=1;next} /^## /{f=0} f && /^### /{print substr($(0),5)}' "$M")
n=0; heads=0; blocks=0; links=0
for k in $KITS; do
  n=$((n + 1))
  printf '%s\n' "$DET" | grep -qxF "$k" && heads=$((heads + 1)) || echo "  절 없음: $k"
  s=$(sec "$k")
  printf '%s\n' "$s" | grep -qxF "<!-- AUTO:skills-$k -->" && printf '%s\n' "$s" | grep -qxF "<!-- /AUTO:skills-$k -->" && blocks=$((blocks + 1)) || echo "  블록 없음: $k"
  printf '%s\n' "$s" | grep -qF "(./$k/README.md)" && links=$((links + 1))
done
order=$([ "$(printf '%s\n' "$DET" | tr '\n' ' ' | sed 's/ $//')" = "$KITS" ] && echo 1 || echo 0)
chk=$(cd "$T" && python3 scripts/sync-docs.py --check-only > "$T/sd.txt" 2>&1; echo $?)
insync=$(grep -c '모든 README가 동기화 상태입니다' "$T/sd.txt")
refs=$(find "$T/bambu-kit/skills/bambu-print-profile/references" -maxdepth 1 -type f -name '*.md' | grep -c .)
bs=$(sec bambu-kit)
echo "AR03 kits=$n heads=$heads/$n order=$order blocks=$blocks/$n links=$links/$n sync_rc=$chk insync=$insync bambu_refs=$refs old4=$(printf '%s\n' "$bs" | grep -c 'references 4종') now=$(printf '%s\n' "$bs" | grep -c "references ${refs}종")"
# 양성 대조 — 사본의 rust-kit 스킬 블록에서 스킬 하나를 지우면 sync-docs 가 어긋남을 낸다
sed -i '' -e 's/`rust-api`, //' "$M"; applied=$(grep -c '`rust-api`, ' "$M")
chk2=$(cd "$T" && python3 scripts/sync-docs.py --check-only > "$T/sd2.txt" 2>&1; echo $?)
echo "AR03 broken applied_left=$applied sync_rc=$chk2 insync=$(grep -c '모든 README가 동기화 상태입니다' "$T/sd2.txt")"
rm -rf "$T"
```

```bash
#!/usr/bin/env bash
# scope.sh — AR-01 · AR-02: 바뀐 파일 집합 · .harness 경로 · notes 파일
K=${K:?}; . "$K/common.sh"; R=$(resolve_ref)
[ "$(git -C "$W" rev-list --merges "$B..$R" | grep -c .)" = 0 ] || { echo END_HAS_MERGE; exit 2; }
REQUIRED="scripts/append-audit-log.py scripts/sync-orchestrator.py scripts/collect-kaizen-data.py .claude/skills/kaizen-orchestrator/SKILL.md .claude/skills/kaizen-orchestrator/references/phase-dependencies.md .claude/skills/kaizen-orchestrator/references/phase-research-templates.md .claude/skills/react-kaizen/SKILL.md .claude/skills/design-kaizen/SKILL.md .claude/skills/backend-kaizen/SKILL.md .claude/skills/rust-kaizen/SKILL.md .claude/skills/bambu-kaizen/SKILL.md .claude/skills/bambu-research/SKILL.md .claude/skills/tone-kaizen/SKILL.md README.md"
CH=$(git -C "$W" diff --name-only "$B..$R" -- . ':(exclude).harness')
out=0; for f in $CH; do printf '%s\n' $REQUIRED | grep -qxF "$f" || { out=$((out + 1)); echo "  밖: $f"; }; done
miss=0; for f in $REQUIRED; do printf '%s\n' $CH | grep -qxF "$f" || { miss=$((miss + 1)); echo "  빠짐: $f"; }; done
echo "AR01 changed=$(printf '%s\n' $CH | grep -c .) outside=$out required_missing=$miss"
HX=$(git -C "$W" diff --name-only "$B..$R" -- .harness | grep -vE '^\.harness/(sprint-(contract|feedback|amendments)-after-0926-orchestrator-docs\.md|\.meta/after-kaizen-0926b/vsb-notes\.md)$')
echo "AR01h harness_other=$(printf '%s' "$HX" | grep -c .)"; [ -n "$HX" ] && printf '  %s\n' $HX
# AR-02 — notes 파일: 항목 열둘 · 제목 넷
N=$(git -C "$W" show "$R:.harness/.meta/after-kaizen-0926b/vsb-notes.md" 2>/dev/null)
ids=0; for i in 3 7 8 11 16 17 18 19 20 22 23 25; do printf '%s\n' "$N" | grep -qE "VS-$i([^0-9]|$)" && ids=$((ids + 1)); done
hd=0; for h in '## 남은 것' '## tone-guide 결과' '## 앱 이름 검사 판단' '## 문서 드리프트'; do printf '%s\n' "$N" | grep -qxF "$h" && hd=$((hd + 1)); done
echo "AR02 notes=$([ -n "$N" ] && echo 1 || echo 0) ids=$ids/12 heads=$hd/4"
exit 0
```

```bash
#!/usr/bin/env bash
# dg.sh — DG-02 · AP-03: 바뀐 파일의 편집기 진단 몫 — 마크다운 더한 줄의 새 경고 · 파이썬 컴파일 · 셸 문법 · JSON
K=${K:?}; . "$K/common.sh"; R=$(resolve_ref); T=$(unpack "$R")
CH=$(git -C "$W" diff --name-only --diff-filter=AM "$B..$R" -- . ':(exclude).harness')
MDS=$(printf '%s\n' $CH | grep -E '\.md$'); PYS=$(printf '%s\n' $CH | grep -E '\.py$'); SHS=$(printf '%s\n' $CH | grep -E '\.sh$'); JS=$(printf '%s\n' $CH | grep -E '\.json$')
new=0
for f in $MDS; do
  added=$(git -C "$W" diff -U0 "$B" "$R" -- "$f" | sed -nE 's/^@@ -[0-9,]+ \+([0-9]+)(,([0-9]+))? @@.*/\1 \3/p' | while read -r s c; do c=${c:-1}; [ "$c" = 0 ] && continue; seq "$s" $((s + c - 1)); done)
  hits=$(cd "$T" && node "$MDL/node_modules/markdownlint-cli2/markdownlint-cli2-bin.mjs" --config "$MDL/cfg.markdownlint-cli2.jsonc" "$f" 2>&1 | sed -nE "s#^$f:([0-9]+).*#\1#p")
  k=$(printf '%s\n' $hits | grep -cxF -f <(printf '%s\n' $added) || true)
  [ "${k:-0}" -gt 0 ] && echo "  새 경고 $f: $k"
  new=$((new + ${k:-0}))
done
pyok=0; for f in $PYS; do python3 -m py_compile "$T/$f" 2>/dev/null && pyok=$((pyok + 1)); done
shok=0; for f in $SHS; do bash -n "$T/$f" 2>/dev/null && shok=$((shok + 1)); done
jsok=0; for f in $JS; do python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$T/$f" 2>/dev/null && jsok=$((jsok + 1)); done
echo "md_files=$(printf '%s\n' $MDS | grep -c .) md_new_warn=$new py=$pyok/$(printf '%s\n' $PYS | grep -c .) sh=$shok/$(printf '%s\n' $SHS | grep -c .) json=$jsok/$(printf '%s\n' $JS | grep -c .)"
# AP-03 — 바뀐 마크다운 전부(.harness 포함)에서 백틱으로 여는 줄의 언어 힌트 없는 블록 수. 여닫는 규칙은 CommonMark 0.31.2 §4.5
ALLMD=$(git -C "$W" diff --name-only --diff-filter=AM "$B..$R" -- '*.md')
bare=$(cd "$T" && python3 - $ALLMD <<'PY2'
import re, sys
n = 0
for f in sys.argv[1:]:
    op = None
    for i, line in enumerate(open(f, encoding="utf-8").read().splitlines(), 1):
        m = re.match(r"^(`{3,}|~{3,})(.*)$", line.strip())
        if op is None:
            if m and not (m.group(1)[0] == "`" and "`" in m.group(2)):
                op = (m.group(1)[0], len(m.group(1)))
                if op[0] == "`" and not m.group(2).strip():
                    n += 1; print(f"  bare {f}:{i}", file=sys.stderr)
        elif m and m.group(1)[0] == op[0] and len(m.group(1)) >= op[1] and not m.group(2).strip():
            op = None
print(n)
PY2
)
echo "AP03 md_all=$(printf '%s\n' $ALLMD | grep -c .) bare_open=$bare"
rm -rf "$T"
```

```bash
#!/usr/bin/env bash
# misc.sh — AP-01 · AP-02 · AP-04 · DG-01 · DG-03: 더한 줄의 버전 하드코딩 · 원격 가지 · frontmatter name · release.sh 교집합
K=${K:?}; . "$K/common.sh"; R=$(resolve_ref)
echo "AP01 hardcoded_version=$(git -C "$W" diff -U0 "$B" "$R" -- . ':(exclude).harness' | grep -E '^\+[^+]' | grep -ciE 'hardcoded.*version')"
echo "AP02 remote_branch=$(git -C "$W" ls-remote --heads origin "$BR" | grep -c .)"
SK=$(git -C "$W" diff --name-only --diff-filter=AM "$B..$R" -- '*SKILL.md' '*/agents/*.md')
ok=0; for f in $SK; do git -C "$W" show "$R:$f" | awk 'NR==1&&/^---/{f=1;next} f&&/^---/{exit} f&&/^name:[ \t]*[^ \t]/{h=1} END{exit !h}' && ok=$((ok + 1)); done
echo "AP04 frontmatter_name=$ok/$(printf '%s\n' $SK | grep -c .)"
echo "DG01_03 release_sh_changed=$(git -C "$W" diff --name-only "$B..$R" -- scripts/release.sh | grep -c .)"
```

```bash
#!/usr/bin/env bash
# ci.sh — DG-05: 로컬 CI 도구를 가지 끝 작업 폴더에서 돌린다. 전제가 안 맞으면 재지 않고 멈춘다
K=${K:?}; . "$K/common.sh"; R=$(resolve_ref)
CIL=/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh
[ "$(git -C "$W" rev-parse HEAD)" = "$R" ] || { echo "PREMISE_FAIL HEAD 가 가지 끝이 아니다"; exit 2; }
[ -z "$(git -C "$W" status --porcelain --untracked-files=no)" ] || { echo "PREMISE_FAIL 추적 파일에 커밋 안 된 변경"; exit 2; }
echo "ci_local_sha=$(shasum -a 256 "$CIL" | cut -c1-16)"
O=$(mktemp -d "${TMPDIR:-/tmp}/vsb-ci.XXXXXX")
TMPDIR=$O bash "$CIL" "$W" >"$O/run.txt" 2>&1
S="$O/ci-local/summary.txt"
echo "steps=$(grep -c 'rc=' "$S") rc0=$(grep -c 'rc=0' "$S") not0=[$(grep 'rc=' "$S" | grep -v 'rc=0' | tr -s ' ' | tr '\n' ';')] skip=[$(grep SKIP "$S" | tr '\n' ';')]"
echo "outside_ci_local=[$(sed -n '/이 스크립트 밖의 것:/,/^[0-9]*$/p' "$O/run.txt" | sed '1d;$d' | tr '\n' ';')]"
```

### 봉인 전 실측 — 시작 판 `6378948`

시작 판 = 지금 가지 끝이라 아래 값이 곧 고치기 전 값(양성 대조)이다.

- `audit.sh` → `real rc=0,0 kept=1 grew=1` · `fresh rc=0,0 entries=2 heads=9 dup=4 md024=4 watch=1` · `phase rc=0,0 head=1 rows=2` · `error phase_only_rc=2 lines_after=1 no_log_rc=2 log_created=0`
- `orch.sh` → `SK02 old_step11=2 link_step=[없음] watch_call=0 step05_step11=1` · `SK05 orch=2 templates=2 collector_table=2` · `SK06 standalone=1 site_css=0`
- `ver.sh` → 두 줄 모두 `block_lines=0 argsub=0 ref=31 got=0 equal=0 seven=0/7 err=0`
- `kitdirs.sh` → `SC02 check_only_rc=0 want=11 scope_line=0/11 extra=0` · `SK03 dep_map=0/11 extra=0` · `ER02 mutated_left=0 drift_rc=1`
- `kz.sh` → `SK01 v8_rows=1 exec_bit=1 quote=0` · `SK04 cannot=1 verify_ref=0 exit3=0 unjudgeable=0` · `SK07 design_row=0 backend_row=0 rust_fail_row=0 rust_counter_row=0 rows=8,8,9 old_rows_lost=0` · `SK08 cloudflare=1 fallback_order=0 step4_neg=0` · `SK09 server_name=3 bypass=1 order_ref=0 skill_ref=0`
- `tone.sh` → `SK11 block_lines=0 in_step2=0 now=[] unread_lines=0` · `SK11 broken applied=1 [] d04=0`
- `readme.sh` → `AR03 kits=14 heads=10/14 order=0 blocks=4/14 links=10/14 sync_rc=0 insync=1 bambu_refs=9 old4=1 now=0` · `AR03 broken applied_left=0 sync_rc=1 insync=0`
- `scope.sh` → `AR01 changed=0 outside=0 required_missing=14` · `AR01h harness_other=0` · `AR02 notes=0 ids=0/12 heads=0/4`
- `dg.sh` → `md_files=0 md_new_warn=0 py=0/0 sh=0/0 json=0/0` · `AP03 md_all=0 bare_open=0`
- `misc.sh` → `AP01 hardcoded_version=0` · `AP02 remote_branch=0` · `AP04 frontmatter_name=0/0` · `DG01_03 release_sh_changed=0`
- `ci.sh` (작업 폴더 HEAD = 시작 판) → `ci_local_sha=59fe55125c0dbc77` · `steps=25 rc0=25 not0=[] skip=[feedback-agg-test SKIP (yq 없음);]` · `outside_ci_local=` 에 `pip install pyyaml` · `command -v zsh` · `npm ci` · `npx playwright install` · `run: |` 다섯

### 알려진 답 — 새로 짠 측정이 제대로 세는지

- SK-10 기준 목록 31 개 — 2026-09-24 사이클(`77ed5bb^1..77ed5bb`)에서 머리 설정 `version` 이 바뀐 `.md`. 교차 진단이 손으로 확인한 일곱(`api-design` · `cicd` · `data-modeling` · `flows` · `prd-patterns` · `sqlx-patterns` · `visual-evidence-protocol`)이 모두 든다(final-notes `:221-222`). 합성 F1 절(첫 줄 `# 판 번호 원본 목록`, `BASE` · `END` 를 쓰는 일곱 줄 블록)을 `ver.sh` 와 같은 추출식으로 떼어 bash · zsh 로 돌리면 둘 다 `31` 줄 — 추출식과 zsh 실행이 산다
- SK-11 규칙 69 개 — 파일마다 손으로 센 규칙 표 행: `adapter-dart-flutter.md` 15 · `core-comment.md` 17 · `core-naming.md` 12 · `core-structure.md` 14 · `locale-korean.md` 11 (합 69, `grep -cE '^\| [A-Z]+-[0-9]+ \|.*\| (MUST|SHOULD|관측 컨벤션|합성)'`). 위 `grep` 은 줄 어디든 네 값이 있으면 세므로 D-04 도 잡아 69 가 나온다 — 앞머리 판정이 따로 필요한 까닭은 칸 위치다: `adapter-dart-flutter.md` · `locale-korean.md` 는 `| ID | 규칙 | 강도 |` 세 칸, 나머지 셋은 `| ID | 규칙 | 강도 | 축 |` 네 칸이다(표 머리 실측). 강도 칸(셋째 칸)이 네 값과 **글자 그대로 같은** 줄만 세면 68(D-04 를 놓침), 세 값만 글자 그대로 세면 63(final-notes `:224-225` 의 「63 개만」 과 같음). 재현 명령(2026-09-27 02:4x 실측 `4 68` · `3 63`): `cd tone-kit/references && for V in 4 3; do cat adapter-dart-flutter.md core-comment.md core-naming.md core-structure.md locale-korean.md | awk -F'|' -v V=$V '/^\| [A-Z]+-[0-9]+ \|/{c=$(4); gsub(/^ +| +$/,"",c); if(c=="MUST"||c=="SHOULD"||c=="관측 컨벤션"||(V==4&&c=="합성")) n++} END{print V, n}'; done`. 합성 블록으로 돌리면 `rules=69 read=69 unread=0`, D-04 를 `기타 (메모)` 로 바꾼 사본은 `rules=69 read=68 unread=1` · `UNREAD adapter-dart-flutter.md:D-04 기타 (메모)`
- SK-07 옛 행 보존 — 디자인 표에서 한 행을 지운 사본을 같은 비교로 재면 `1`
- AR-01 — 기준 `7038841~1` · 끝 `7038841`(`B_OVERRIDE=7038841~1 REF=7038841`)로 재면 `outside=14`
- DG-02 — 기준 `f81568d` · 끝 `6378948` 로 재면 `md_new_warn=19` (vsa 계약의 같은 도우미 실측과 같음). 이 계약의 `dg.sh` 그대로(`B_OVERRIDE=f81568d REF=6378948`, 같은 `grep -cxF -f <(...)` 경로) 2026-09-27 02:4x 에 다시 돌려 `md_files=79 md_new_warn=19 py=10/10 sh=7/7 json=27/27` 를 확인했다 — 새 경고를 잡는 길이 산다

## Skill

- [ ] SK-01: react-kaizen 검사 표의 V8 행이 V8 의 두 검사 — 직접 실행 스크립트의 실행 비트와 `${CLAUDE_PLUGIN_ROOT}` 큰따옴표 — 를 함께 적는다 [exact]
    Given: 가지 끝 판. 측정: `kz.sh` 의 `SK01 v8_rows=1 exec_bit=1 quote=1`
    양성 대조: 시작 판에서 `quote=0`
    도우미 지문: `kz.sh` sha256 앞 16 자 `257b8dca596ecbbf`
- [ ] SK-02: 오케스트레이터가 Final 을 옛 이름 「Step 11」 로 가리키지 않고(Phase 11 절 제목 · 「구 Step 11」 이력 표기 제외), 연동 스크립트 절의 감사 기록 도구 줄이 Final 단계 하나(`Step F<번호>`)를 가리키며, 그 단계 절에 감사 기록 도구를 `--watch` 와 함께 부르는 줄이 있고, Step 0.5 절(사이클 시작에 감사 기록 빈 항목을 덧붙이는 서술)도 옛 이름 「Step 11」 을 쓰지 않는다 [exact]
    Given: 가지 끝 판. 측정: `orch.sh` 의 `SK02 old_step11=0 link_step=[Step F<번호>] watch_call=<1 이상> step05_step11=0` (`link_step` 이 `없음` 이 아니다)
    양성 대조: 시작 판에서 `old_step11=2 link_step=[없음] watch_call=0 step05_step11=1`
    도우미 지문: `orch.sh` sha256 앞 16 자 `68fe3e659bffab39`
- [ ] SK-03: Phase 의존성 맵(`.claude/skills/kaizen-orchestrator/references/phase-dependencies.md`)의 Phase 5~17 블록이 그 킷에 실제로 있는 `scripts/` · `templates/` 열한 개(`flutter-toolkit/scripts/` · `flutter-toolkit/templates/` · `design-kit/scripts/` · `design-kit/templates/` · `rust-kit/templates/` · `react-kit/scripts/` · `react-kit/templates/` · `reflect-kit/scripts/` · `bambu-kit/scripts/` · `tone-kit/templates/` · `howto-kit/scripts/`)를 모두 적고, 없는 폴더는 적지 않는다 [exact, enumerated]
    Given: 가지 끝 판. 측정: `kitdirs.sh` 의 `SK03 dep_map=11/11 extra=0`
    양성 대조: 시작 판에서 `dep_map=0/11`
    도우미 지문: `kitdirs.sh` sha256 앞 16 자 `b695be7021092e56`
- [ ] SK-04: api 조사 지침(`phase-research-templates.md`)에 「Hurl 로 표현할 수 없다」 가 0 번 나오고, Phase 16 절이 정본 `api-kit/skills/api-verify/SKILL.md` 를 가리키며 한쪽 경로가 없을 때의 종료 코드 3 과 판정 불가를 적는다 [exact]
    Given: 가지 끝 판. 측정: `kz.sh` 의 `SK04 cannot=0 verify_ref=<1 이상> exit3=<1 이상> unjudgeable=<1 이상>`
    양성 대조: 시작 판에서 `cannot=1 verify_ref=0 exit3=0 unjudgeable=0`
    알려진 답: 같은 세 grep 을 오케스트레이터 `:576-578`(이미 바로잡힌 글)에 돌리면 `1 1 1`. `종료 코드` 찾기만 따로 bash(`/usr/bin/grep`)로 합성 네 줄(`종료 코드 3 이다` · 백틱 한 겹 `3` · `종료 코드 4` · 백틱 두 겹)에 돌리면 `2` — 앞 두 줄만 잡는다 (2026-09-27 10:1x 실측)
    도우미 지문: `kz.sh` sha256 앞 16 자 `257b8dca596ecbbf`
- [ ] SK-05: 카이젠 조사 입력에 앱 이름 `fit-pal` 이 0 번 나온다 — 오케스트레이터 `SKILL.md` · `phase-research-templates.md` · 데이터 풀 수집기 `scripts/collect-kaizen-data.py` 의 Flutter · Rust 표 행 (대소문자 무시) [exact, enumerated]
    Given: 가지 끝 판. 측정: `orch.sh` 의 `SK05 orch=0 templates=0 collector_table=0`
    양성 대조: 시작 판에서 `orch=2 templates=2 collector_table=2`
    도우미 지문: `orch.sh` sha256 앞 16 자 `68fe3e659bffab39`
- [ ] SK-06: 오케스트레이터 F2 절이 옛 원칙 낱말 「standalone」 을 쓰지 않고 공통 스타일 파일 `docs/assets/site.css` 를 적는다 [exact]
    Given: 가지 끝 판. 측정: `orch.sh` 의 `SK06 standalone=0 site_css=<1 이상>`
    양성 대조: 시작 판에서 `standalone=1 site_css=0`
    도우미 지문: `orch.sh` sha256 앞 16 자 `68fe3e659bffab39`
- [ ] SK-07: design · backend · rust-kaizen 의 Gotcha 6 형제 표에 새 행이 들고 옛 행은 한 줄도 바뀌지 않는다 — design 은 「편집 전 확정」 · 「비교 반복 순서」 · 「캡처 점검 목록」 과 세 규약 파일(`visual-change-protocol` · `visual-evidence-protocol` · `render-evidence-protocol`)을 한 행에, backend 는 「시각 종류」 와 `backend-system` · `backend-guide` · `backend-audit` 를 한 행에, rust 는 「실패 원인」 과 `rust-preflight` 를 적은 행 하나와 `UNVERIFIED_INVALID_EVIDENCE` · `env_gaps` · `rust-audit` · `rust-reviewer` 를 적은 행 하나 [exact, enumerated]
    Given: 가지 끝 판. 측정: `kz.sh` 의 `SK07 design_row=<1 이상> backend_row=<1 이상> rust_fail_row=<1 이상> rust_counter_row=<1 이상> … old_rows_lost=0`
    양성 대조: 시작 판에서 네 행 수 모두 `0`. 옛 행 비교는 알려진 답 절(한 행 지운 사본 `1`)
    도우미 지문: `kz.sh` sha256 앞 16 자 `257b8dca596ecbbf`
- [ ] SK-08: bambu-kaizen 격차 표의 fallback 행이 「Cloudflare」 대신 킷의 「MakerWorld 읽는 순서」 를 가리키고(파일 전체 `Cloudflare` 0), Step 4 회귀 검증에 `bambu-kit/skills/bambu-print-profile/SKILL.md` 의 음성 대조 표를 실제로 주입해 보는 줄이 있다 [exact]
    Given: 가지 끝 판. 측정: `kz.sh` 의 `SK08 cloudflare=0 fallback_order=1 step4_neg=<1 이상>`
    양성 대조: 시작 판에서 `cloudflare=1 fallback_order=0 step4_neg=0`
    도우미 지문: `kz.sh` sha256 앞 16 자 `257b8dca596ecbbf`
- [ ] SK-09: bambu-research 가 브라우저 서버 이름(`mcp__playwright__`)을 박지 않고 「우회」 를 말하지 않으며, MakerWorld 는 킷의 「MakerWorld 읽는 순서」(`bambu-kit/skills/bambu-print-profile/SKILL.md`)를 따르라고 적는다 [exact]
    Given: 가지 끝 판. 측정: `kz.sh` 의 `SK09 server_name=0 bypass=0 order_ref=<1 이상> skill_ref=<1 이상>`
    양성 대조: 시작 판에서 `server_name=3 bypass=1 order_ref=0 skill_ref=0`
    도우미 지문: `kz.sh` sha256 앞 16 자 `257b8dca596ecbbf`
- [ ] SK-10: 오케스트레이터 F1 절에 첫 줄이 `# 판 번호 원본 목록` 인 bash 블록이 있고, 셸 변수 `BASE` · `END` 로 2026-09-24 사이클(`77ed5bb^1` · `77ed5bb`)을 주어 저장소 폴더에서 bash 와 zsh 로 돌리면 둘 다 기준 목록(머리 설정 `version` 이 바뀐 `.md` 31 개)과 같은 경로 집합을 내고 교차 진단의 일곱을 모두 담으며, 블록에 `$` + 숫자가 없다 [exact]
    Given: 가지 끝 판. 측정: `ver.sh` 의 두 줄이 `SK10 bash block_lines=<1 이상> argsub=0 ref=31 got=31 equal=1 seven=7/7 err=0` · `SK10 zsh …` 같은 값
    양성 대조: 시작 판에서 `block_lines=0 … got=0 equal=0 seven=0/7`
    알려진 답: 알려진 답 절 — 합성 블록이 두 셸 모두 `31`
    음성 대조: 블록이 머리 설정이 아닌 본문 `version:` 까지 읽거나 값이 안 바뀐 파일을 내면 `equal=0`
    도우미 지문: `ver.sh` sha256 앞 16 자 `8eeb443de00f0f42`
- [ ] SK-11: tone-kaizen Step 2 에 첫 줄이 `# 강도 칸 앞머리 판정` 인 bash 블록이 있고, 저장소 폴더에서 bash 로 돌리면 첫 줄이 `rules=69 read=69 unread=0` 이며, `adapter-dart-flutter.md` D-04 의 강도 칸을 `기타 (메모)` 로 바꾼 사본에서는 `rules=69 read=68 unread=1` 과 D-04 를 짚는 `UNREAD` 줄을 낸다 [exact]
    Given: 가지 끝 판. 측정: `tone.sh` 의 `SK11 block_lines=<1 이상> in_step2=1 now=[rules=69 read=69 unread=0] unread_lines=0` · `SK11 broken applied=1 [rules=69 read=68 unread=1] d04=1`
    양성 대조: 시작 판에서 `block_lines=0 … now=[]`
    알려진 답: 알려진 답 절 — 파일별 15 · 17 · 12 · 14 · 11 = 69, 글자 그대로 세면 68 · 63
    음성 대조: 앞머리 대신 칸 전체를 네 값과 맞대면 `now=[rules=69 read=68 unread=1]` (D-04 를 못 읽음)
    도우미 지문: `tone.sh` sha256 앞 16 자 `c6b5712616713339`

## Script

- [ ] SC-01: 감사 기록 도구(`scripts/append-audit-log.py`)를 같은 날 같은 사이클로 두 번 부르면(둘째에 `--watch`) 두 항목이 모두 덧붙고 제목(`#` ~ `######` 줄) 글이 하나도 겹치지 않으며 markdownlint MD024 가 0 이고, 실제 감사 기록 사본에 덧붙여도 옛 내용은 한 글자도 안 바뀌며, phase 모드는 같은 사이클 두 줄을 머리 하나 아래 모은다 [exact]
    Given: 가지 끝 판을 푼 임시 폴더. 측정: `audit.sh` 의 `real rc=0,0 kept=1 grew=1` · `fresh rc=0,0 entries=2 heads=<수> dup=0 md024=0 watch=1` · `phase rc=0,0 head=1 rows=2`
    양성 대조: 시작 판에서 `fresh … dup=4 md024=4` — 겹침을 잡는다
    음성 대조: 제목 꼬리를 날짜 · 사이클만으로 되돌리면 `dup=4` 로 돌아간다(시작 판이 그 상태)
    도우미 지문: `audit.sh` sha256 앞 16 자 `f5bb3b64bb7bc644` · `common.sh` sha256 앞 16 자 `ba06eb40d0da1b1c`
- [ ] SC-02: 오케스트레이터 동기화 스크립트가 킷의 `scripts/` · `templates/` 도 범위 줄에 넣어, 가지 끝 오케스트레이터 자동 영역의 Phase 5~17 범위 줄에 SK-03 과 같은 열한 폴더가 모두 있고 없는 폴더는 없으며, `python3 scripts/sync-orchestrator.py --check-only` 가 종료 코드 0 이다 [exact, enumerated]
    Given: 가지 끝 판. 측정: `kitdirs.sh` 의 `SC02 check_only_rc=0 want=11 scope_line=11/11 extra=0`
    양성 대조: 시작 판에서 `scope_line=0/11`
    도우미 지문: `kitdirs.sh` sha256 앞 16 자 `b695be7021092e56`

## Error

- [ ] ER-01: 감사 기록 도구의 오류 길이 그대로다 — phase 모드에 `--result` 가 없으면 종료 코드 2 이고 기록이 안 바뀌며, 감사 기록 파일이 없으면 종료 코드 2 이고 새 파일을 만들지 않는다 [exact]
    Given: 가지 끝 판. 측정: `audit.sh` 의 `error phase_only_rc=2 lines_after=1 no_log_rc=2 log_created=0`
    양성 대조: 오류 길을 지우면(예: 기록 없음 검사를 빼면) `log_created=1` 또는 종료 코드 0 이 된다. 시작 판 값은 기대값과 같다 — 이 조건은 멀쩡하던 것이 망가지지 않았는지를 잰다
    도우미 지문: `audit.sh` sha256 앞 16 자 `f5bb3b64bb7bc644`
- [ ] ER-02: 오케스트레이터 동기화의 어긋남 감지가 산다 — 가지 끝 사본의 범위 줄 하나에서 폴더 하나(`flutter-toolkit/evals/`)를 지우면 `--check-only` 가 종료 코드 1 을 낸다 [exact]
    Given: 가지 끝 판. 측정: `kitdirs.sh` 의 `ER02 mutated_left=0 drift_rc=1`
    양성 대조: 변이를 안 넣은 같은 판은 `SC02 check_only_rc=0`
    도우미 지문: `kitdirs.sh` sha256 앞 16 자 `b695be7021092e56`

## Architecture

- [ ] AR-01: Given: 가지 끝이 해석되고(`git rev-parse --verify refs/heads/chore/ak2-vsb`) 시작 판 `6378948` 부터 병합 커밋이 없다. 시작 판..가지 끝 누적 차이(`git diff --name-only 6378948..<가지 끝> -- . ':(exclude).harness'`)가 정확히 14 파일로 한정되고 그 14 파일을 모두 담으며(기대 집합은 `scope.sh` 의 `REQUIRED` 한 곳에만 적는다 — 편집 전 감사 표의 대상 파일과 같다), `.harness/` 아래는 이 슬러그의 계약 · 피드백 · 개정 파일과 notes 파일 하나만 바뀐다 [exact, enumerated]
    측정: `scope.sh` 의 `AR01 changed=14 outside=0 required_missing=0` · `AR01h harness_other=0`
    양성 대조: 알려진 답 절 — 기준 `7038841~1` · 끝 `7038841` 로 재면 `outside=14`
    도우미 지문: `scope.sh` sha256 앞 16 자 `2efbd0676fde2ecd`
- [ ] AR-02: notes 파일 `.harness/.meta/after-kaizen-0926b/vsb-notes.md` 가 가지 끝에 있고, 항목 열둘(VS-3 · VS-7 · VS-8 · VS-11 · VS-16 · VS-17 · VS-18 · VS-19 · VS-20 · VS-22 · VS-23 · VS-25)을 모두 적으며, 줄 전체가 `## 남은 것` · `## tone-guide 결과` · `## 앱 이름 검사 판단` · `## 문서 드리프트` 인 제목 넷을 갖는다 [exact, enumerated]
    측정: `scope.sh` 의 `AR02 notes=1 ids=12/12 heads=4/4`
    양성 대조: 시작 판에서 `AR02 notes=0`
    도우미 지문: `scope.sh` sha256 앞 16 자 `2efbd0676fde2ecd`
- [ ] AR-03: 루트 README 의 `## 플러그인 상세` 가 marketplace 열네 킷을 같은 차례의 `### <킷>` 절로 두고, 절마다 `<!-- AUTO:skills-<킷> -->` 블록과 그 킷 README 링크가 있으며, `python3 scripts/sync-docs.py --check-only` 가 종료 코드 0 과 「모든 README가 동기화 상태입니다」 를 내고, bambu-kit 절이 「references 4종」 대신 실제 수 「references 9종」 을 적는다 [exact, enumerated]
    Given: 가지 끝 판. 측정: `readme.sh` 의 `AR03 kits=14 heads=14/14 order=1 blocks=14/14 links=14/14 sync_rc=0 insync=1 bambu_refs=9 old4=0 now=1` · `AR03 broken applied_left=0 sync_rc=1 insync=0`
    양성 대조: 시작 판에서 `heads=10/14 order=0 blocks=4/14 links=10/14 … old4=1 now=0`. 둘째 줄은 블록에서 스킬 하나를 지운 사본을 sync-docs 가 잡는지(감지가 사는지)를 본다
    도우미 지문: `readme.sh` sha256 앞 16 자 `637d6efad78f3c05`

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — 시작 판..가지 끝의 더한 줄(`.harness` 제외)에 `hardcoded.*version` (대소문자 무시) 0 건 [exact]
    측정: `misc.sh` 의 `AP01 hardcoded_version=0`
    양성 대조: 같은 거르기 사슬(`grep -E '^\+[^+]' | grep -ciE 'hardcoded.*version'`)에 합성 더한 줄 `+ hardcoded plugin version 1.2.3` 을 넣으면 `1` (2026-09-27 10:1x bash 실측). 머리 줄 `++ …` 은 세지 않는다
    도우미 지문: `misc.sh` sha256 앞 16 자 `94b098ee9e7f5d87`
- [ ] AP-02: force push 금지 — 이 가지는 원격에 아예 올리지 않는다 [exact]
    측정: `misc.sh` 의 `AP02 remote_branch=0` (`git ls-remote --heads origin chore/ak2-vsb` 줄 수). 양성 대조: 같은 명령을 `main` 에 쓰면 `1`
    도우미 지문: `misc.sh` sha256 앞 16 자 `94b098ee9e7f5d87`
- [ ] AP-03: bare code fence 금지 — 시작 판..가지 끝에 바뀐 마크다운 전부(`.harness` 포함)에서 백틱으로 여는 줄의 언어 힌트 없는 블록이 0 개다 (여닫는 규칙은 CommonMark 0.31.2 §4.5 — `python3 scripts/validate-plugin.py --check=code-fence` 는 킷 폴더만 재서 이 묶음 파일을 못 본다) [exact]
    측정: `dg.sh` 의 `AP03 md_all=<수> bare_open=0`. 양성 대조: 언어 힌트 없이 여는 블록 하나를 넣은 합성 파일에서 `1`
    도우미 지문: `dg.sh` sha256 앞 16 자 `dc4f76ae7b674a13`
- [ ] AP-04: frontmatter name 누락 금지 — 시작 판..가지 끝에 바뀐 `SKILL.md` 전부의 첫 frontmatter 에 `name:` 이 있다 [exact]
    측정: `misc.sh` 의 `AP04 frontmatter_name=<n>/<n>` (두 수가 같고 8 — 바뀌는 `SKILL.md` 여덟: kaizen-orchestrator · react · design · backend · rust · bambu-kaizen · bambu-research · tone)
    양성 대조: 같은 awk 판정을 `name:` 이 없는 합성 머리 설정(`---` · `description: x` · `---`)과 값이 빈 `name:` 에 돌리면 둘 다 종료 코드 1(세지 않음), `name: a` 는 0 (2026-09-27 10:1x bash 실측)
    도우미 지문: `misc.sh` sha256 앞 16 자 `94b098ee9e7f5d87`

## Reusability

- [ ] RE-01: N/A (산출물에 새 재사용 단위가 없다 — 기존 스크립트 둘 · 수집기 표 두 줄 · 스킬 문서 · README 를 고칠 뿐이다. 측정: `git diff --name-only --diff-filter=A 6378948..<가지 끝> -- . ':(exclude).harness'` 가 0 줄)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 범위 줄 폴더는 기존 `KIT_SCOPE_DIRS` 하나에 더하고(두 번째 폴더 목록 없음), 감사 기록 제목 겹침은 기존 도구 안에서 고치며, 새 파일(`.harness` 제외)을 만들지 않는다 [exact]
    측정: `git diff --name-only --diff-filter=A 6378948..<가지 끝> -- . ':(exclude).harness' | grep -c .` 이 `0` · `grep -c '"scripts/"' scripts/sync-orchestrator.py` (가지 끝 판) 이 `1` · `grep -c 'KIT_SCOPE_DIRS *=' scripts/sync-orchestrator.py` 이 `1`
    양성 대조: 시작 판에서 `"scripts/"` 는 `0` — 더하기 전이다

## Diagnostics

- [ ] DG-01: N/A (commands.analyze `bash -n scripts/release.sh` 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `misc.sh` 의 `DG01_03 release_sh_changed=0`. 대신 바뀐 파이썬 컴파일은 DG-02 가 잰다)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (diagnostics.ide_exclude `[]` 제외 없음) — 시작 판..가지 끝에 바뀐 마크다운의 더한 줄에 markdownlint 새 경고 0 건(편집기 설정 · 스펠체크 제외), 바뀐 파이썬 셋 전부 컴파일 [exact]
    측정: `dg.sh` 의 `md_files=<수> md_new_warn=0 py=3/3 sh=0/0 json=0/0`
    양성 대조: 알려진 답 절 — 기준 `f81568d` 로 재면 `md_new_warn=19`
    도우미 지문: `dg.sh` sha256 앞 16 자 `dc4f76ae7b674a13`
- [ ] DG-03: N/A (commands.test `bash scripts/release.sh 2>&1 || true` 는 release.sh 를 돌릴 뿐 이번 변경을 부르지 않는다 — 교집합 0 개, 같은 측정 `DG01_03 release_sh_changed=0`. 대신 저장소 시험 전부는 DG-05 가 잰다)
- [ ] DG-04: N/A (산출물에 구동할 앱 · 서버가 없다 — 스크립트 둘 · 스킬 문서 · README 뿐. 실행으로 재는 몫은 SC-01 · SK-10 · SK-11 과 DG-05 로컬 CI)
- [ ] DG-05: 로컬 CI 도구가 가지 끝 작업 폴더에서 모든 단계를 종료 코드 0 으로 끝내고(yq 없는 `feedback-agg-test` SKIP 하나만 예외), CI 파일에서 이 도구 밖 `run:` 줄은 설치 단계 다섯뿐이다 [exact]
    Given: 작업 폴더 HEAD = 가지 끝, 추적 파일에 커밋 안 된 변경 0 (아니면 `PREMISE_FAIL`). 측정: `ci.sh` 가 `ci_local_sha=59fe55125c0dbc77` · `steps=25 rc0=25 not0=[] skip=[feedback-agg-test SKIP (yq 없음);]` · `outside_ci_local=` 에 `pip install pyyaml` · `command -v zsh` · `npm ci` · `npx playwright install` · `run: |` 다섯
    양성 대조: 시작 판 작업 폴더에서 같은 값(2026-09-27 02:3x 실측) — 이 조건은 멀쩡하던 것이 망가지지 않았는지를 잰다. 동기화 어긋남을 넣으면 `sync-orchestrator` 단계가 `rc=1` 이 되는 것은 ER-02 가 같은 스크립트로 잰다
    대체 절차: 로컬 CI 도구가 없거나 지문이 `59fe55125c0dbc77` 와 다르면 `.github/workflows/ci.yml` 의 `run:` 줄(2026-09-27 10:1x 실측 30 줄)을 가지 끝 작업 폴더에서 하나씩 돌리고 설치 단계 다섯을 뺀 줄이 모두 종료 코드 0 인지 본다. 봉인 직전 다시 잰 지문은 `59fe55125c0dbc77` 로 같다
    도우미 지문: `ci.sh` sha256 앞 16 자 `5e39750babe892f8`
