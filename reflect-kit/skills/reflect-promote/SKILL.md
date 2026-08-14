---
name: reflect-promote
description: >
  /reflect-digest가 낸 승격 후보를 실제 Claude Code surface(project CLAUDE.md, project memory,
  global CLAUDE.md, global memory, skill, path-scoped rule, hook)에 반영하고,
  승격 이력을 ~/.claude/logs/<project_id>/promotions-ledger.md 에 append 한다.
  각 승격은 고유 rule_id(UUID)를 발급받아 30일 뒤 post_freq 측정·rollback이 가능하다.
  "승격해줘", "reflect 반영", "규칙 승격", "promote", "ledger에 기록", "rollback",
  "규칙 되돌려" 같은 요청 시 트리거. /reflect-digest 를 먼저 실행하지 않은 상태에서는
  트리거하지 않는다 — 반드시 후보 리스트가 선행되어야 한다.
argument-hint: "[action=promote|rollback] [rule_id=<id>] [tag=<mistake_tag>]"
user-invocable: true
---

# Reflect Promote

`/reflect-digest`의 출력을 실제 파일 수정으로 연결하는 실행기. digest가 아무리 정확해도 surface에 반영되지 않으면 Claude 행동은 바뀌지 않는다. 이 스킬은 그 루프를 닫는다.

**주의**: `/reflect-digest`가 먼저 실행되어 있어야 한다. digest 결과(승격 후보 리스트)가 입력이다. digest 없이 단독으로 "어떤 규칙을 승격할지"를 이 스킬이 판정하지 마라 — 증거가 없다.

## Gotchas

1. **자동 write 금지 — 각 승격 건별로 사용자 승인 필수**. 특히 `CLAUDE.md`와 `hook` surface는 영향 범위가 커서 내용 초안을 보여주고 yes/no를 받아야 한다. 일괄 승인 옵션이 있더라도 hook 승격은 항상 개별 승인.
2. **CLAUDE.md 200줄 한도 체크**. 현재 라인 수 + 추가할 규칙 라인 수가 200을 넘으면 `path_scoped_rule`(`.claude/rules/<tag>.md`)로 자동 fallback 한다. 사용자에게 사유 보고 필수.
3. **중복 승격 금지 — 재발은 "강화"가 아니라 "등급 상향"이다**. `promotions-ledger.md`에서 같은 `canonical_tag`(또는 그 `aliases` 중 하나)가 `status: active`로 존재하면 신규 엔트리를 append 하지 마라. 대신 아래 §재발 — Enforcement 등급 상향 절차를 따른다. 같은 surface 에서 문구만 다시 다듬는 것은 이미 실패한 처방의 반복이다. (본 ledger 엔트리의 `initial_freq`는 덮어쓰지 않는다.)
4. **rollback은 ledger 엔트리 삭제가 아니다**. `status: removed` 또는 `demoted`로 업데이트하고 `demotion_reason` 기록. 실제 파일에서도 해당 규칙 블록을 제거해야 완결. ledger 자체는 이력 보존용.
5. **rule_id 발급은 UUID(`uuidgen`)로 한다**. 시간 정렬이 필요하면 ledger append 순서로 충분하다. ULID 라이브러리 의존성을 추가하지 마라.
6. **target_path는 절대경로로 기록**. 상대경로로 기록하면 세션 cwd 변경 시 rollback이 깨진다.
7. **skill 승격은 진정 새 절차가 필요한 경우만**. 기존 스킬에 Gotchas 한 항목 추가로 해결 가능하면 "기존 스킬 Gotchas 추가"로 분류하라 (별도 skill 신설은 보수적으로).
8. **`actionability: user_environment` 후보는 어떤 surface 로도 승격하지 마라.** 없는 훅 스크립트 참조, 실행 권한 없음, CLI 미설치 같은 사건은 사용자 환경 작업이지 Claude 행동 결함이 아니다. ledger 에 넣지 말고 결과 리포트의 "환경 액션 아이템" 으로만 사용자에게 전달한다. 이걸 CLAUDE.md 에 넣으면 고칠 수 없는 지시가 매 세션 컨텍스트를 먹고, 실제 환경은 고쳐지지 않는다.
9. **`aliases` 를 손으로 고르지 마라 — 결정론적 클러스터 멤버 전체다.** `tag_canon_groups`(`${CLAUDE_PLUGIN_ROOT}/hooks/_lib-tag-canon.sh`) 가 낸 `lemma_key` 클러스터의 멤버를 **그대로** 옮긴다. 사람이 고르면 빠지고, 빠지면 `post_freq` 가 과소집계되어 실패한 규칙이 "효과 있음" 으로 살아남는다. 2026-08-13 실측: `skipped-required-api-doc-check` 는 원시 단독 71 인데 클러스터 합산 110 이었다 — 39 건(55%)이 통째로 안 세지고 있었다. 규약: `${CLAUDE_PLUGIN_ROOT}/references/tag-canonicalization.md`.
10. **이미 승격했는데 재발이 "늘었으면" 문구 문제가 아니라 게이트가 안 걸린 것이다.** 같은 문구를 다시 승격하거나 등급만 올리기 전에 **§B-0 hook coverage audit** 을 먼저 돌려라. 2026-08 실측: `skipped-required-api-doc-check` 가 직전 사이클 9 건 → 이번 30 건 이상으로 **악화**됐는데 사용자는 이미 PreToolUse 훅을 등록해 둔 상태였다. 훅이 있는데 위반이 는다면 1 순위 가설은 "규칙 문장이 약하다" 가 아니라 "훅이 그 경로에서 안 fire 했다" 이다.
11. **`user_stated_constraint == true` 후보는 freq 2/3회를 기다리지 말고 매-세션 자동 로드 surface로 보낸다** (precedence rule #0). 사용자가 명시적으로 금지한 제약의 재위반은 memory(on-demand 로드)나 관망으로 강등하면 재주입이 약해 매 세션 재프롬프트가 반복된다 (insights-report #2 "이전 세션 피드백이 durable rule로 자동 적용 안 됨" 대응). 재주입 강도 순서: **hook(강제) > CLAUDE.md(매 세션 자동 로드) > path-scoped rule(해당 glob 편집 시 로드) > memory(on-demand)**. fast-track 대상은 memory 아래로 내리지 마라. 단 fast-track이어도 surface write 전 사용자 승인은 필수다 (Gotchas #1).
12. **메모리 엔트리는 `grounding` frontmatter 를 갖는다 — 승격 시 반드시 채우고, `self_inference` 는 승격 근거로 쓰지 마라.** `~/.claude/projects/*/memory/` 의 `type: feedback` 엔트리 frontmatter 에는 **`grounding` 필드**가 있다. 값의 정의·판정 절차는 `reflect-kit/references/memory-grounding.md` 가 **SSOT** 이며 여기서 재정의하거나 값을 나열하지 마라. 방향이 둘 다 걸린다 — **(a) 쓸 때**: `project_memory` / `global_memory` 로 승격해 새 엔트리를 만들 때 `grounding` 을 그 규칙의 근거 유형에 맞게 **반드시 기입한다.** 비우면 다음 주기 소비면이 근거 등급을 판정할 수 없고 미태깅으로 잡힌다. **(b) 읽을 때**: 근거가 `grounding: self_inference` 인 (또는 `grounding` 미보유인) 기존 메모리 엔트리**뿐**인 후보는 **승격하지 마라.** `source_evidence` 로도 쓰지 않는다. 외부 검증 없는 자기추론을 영속 규칙으로 올리면 그 규칙이 이후 자기 자신의 근거가 되는 **자기검증 피드백 루프**가 닫힌다.

## 입력

- `action` (optional): `promote` (기본) / `rollback`
- `rule_id` (optional, rollback 시): 되돌릴 ledger 엔트리의 UUID
- `tag` (optional, rollback 시): rule_id 대신 mistake_tag로 가장 최근 active 엔트리를 지정

후보 리스트는 대화 맥락에서 최근 `/reflect-digest` 출력을 참조한다. 없으면 사용자에게 먼저 `/reflect-digest` 실행을 요청한다.

**카이젠 사이클이 낸 후보 파일도 같은 자격의 입력이다** — `.harness/.meta/memory-promotion-candidates-{YYYY-MM-DD}.md` (kaizen-orchestrator Step F3.5 산출물). 이 파일은 관측 · 4축 · `source_evidence` 만 담고 surface 판정 필드는 담지 않으므로, digest 출력과 똑같이 §A-2 precedence 재판정을 처음부터 적용한다. 카이젠은 ledger 를 쓰지 않는다 — `rule_id` 발급 · 중복 판정 · 등급 상향은 전부 이 스킬이 수행한다.

## Process

### A. Promote 경로

1. **전제 확인**
   - `/reflect-digest`의 최근 출력이 대화 내 존재하는가? 없으면 실행 요청하고 중단.
   - 현재 프로젝트 ID 확인: `${CLAUDE_PLUGIN_ROOT}/hooks/_lib-project-id.sh` 의 `compute_project_id`.
   - `promotions-ledger.md` 경로: `~/.claude/logs/<project_id>/promotions-ledger.md`. 없으면 생성.

2. **Precedence Table 재판정**
   - **진입 전제**: `actionability == user_environment` 후보는 표를 적용하지 않고 즉시 제외한다 (Gotchas #8). `freq` 는 항상 digest 의 `cluster_freq`(canonical + aliases 합산)다 — 원시 태그 빈도로 임계를 판정하면 파편화된 최상위 이슈가 통째로 누락된다.
   - digest가 제안한 surface를 **그대로 믿지 말고** 다음 4축 + 빈도로 재판정:
     | # | 조건 | 승격 surface |
     |---|---|---|
     | 0 | `user_stated_constraint == true` (freq ≥ 1, 임계값 우회) | **매-세션 자동 로드 surface로 fast-track** — `scope==global`이면 global CLAUDE.md, 아니면 project CLAUDE.md (200줄 초과 시 path-scoped rule). hard_gate면 hook 후보 병기. memory/관망으로 강등 금지 |
     | 1 | `enforcement_need == hard_gate` | **hook 검토** |
     | 2 | `procedurality == multi_step_procedure` AND freq ≥ 2 | **skill** |
     | 3 | `scope == global` AND 복수 프로젝트 freq ≥ 3 | risk=high → **global CLAUDE.md** / 나머지 → **global memory** |

     **규칙 #3 판정 근거**: 단일 프로젝트 digest 결과로는 "복수 프로젝트" 조건을 검증할 수 없다. 반드시 `/reflect-digest project=all` 출력의 `global_freq` + `project_count` 두 값을 함께 확인해야 rule #3 로 올바르게 분류된다. single-project digest에서 올라온 후보는 rule #4/#5로 재할당하는 것이 일관된 처리.
     | 4 | `scope == project` AND freq ≥ 3 | **project CLAUDE.md** (200줄 초과 예상 시 path_scoped_rule) |
     | 5 | `scope == project` AND freq ≥ 2 | **project memory** |
     | 6 | `risk_class == low` AND freq == 1 | **관망 (skip)** |
     | 7 | 그 외 | **review 후보 (수동)** |
   - digest 제안과 다를 경우 사용자에게 차이를 보고하고 결정 받는다.

3. **중복 체크 → 재발이면 등급 상향 경로로 분기**
   - `promotions-ledger.md`를 grep하여 같은 `canonical_tag` **또는 그 `aliases` 중 하나**가 `status: active`로 존재하는지 확인. alias 를 빠뜨리면 같은 규칙이 다른 이름으로 이중 승격된다.
   - 존재하지 않으면 4단계(신규 승격)로.
   - 존재하면 신규 엔트리를 append 하지 말고 **아래 §재발 — Enforcement 등급 상향** 으로 간다.

4. **surface별 파일 수정 절차**

   **project_claude_md**
   - 프로젝트 `CLAUDE.md` 읽고 라인 수 계산. 180줄 이상이면 path_scoped_rule로 fallback (사용자에게 고지).
   - 적절한 섹션(Learning / Verification 등)을 찾아 불릿 한 줄 추가. 섹션 못 찾으면 "## Reflect Rules" 섹션 말미 생성.
   - 추가 라인 포맷: `- <초안 규칙> (rule_id: <uuid-앞8자>, <YYYY-MM-DD>)`
   - 사용자에게 diff 보여주고 승인.

   **global_claude_md**
   - `~/.claude/CLAUDE.md` 에 동일 규칙 적용. 전역 영향 크므로 **개별 승인 필수**.

   **project_memory**
   - 경로 감지: 현재 Claude Code 세션의 프로젝트 메모리 디렉토리 (예: `~/.claude/projects/<encoded>/memory/`).
   - 새 파일 `feedback_{tag}.md` 생성 (여기서 `{tag}`는 mistake_tag의 snake_case 변환). frontmatter: `name`, `description`, `type: feedback`, **`grounding`**. `grounding` 은 이 규칙을 뒷받침한 근거의 유형이며 판정 기준은 `reflect-kit/references/memory-grounding.md` 다 — 비운 채로 승격하지 마라 (Gotchas #12).
   - 본문: 규칙 + `**Why:**` + `**How to apply:**`.
   - `MEMORY.md`에 한 줄 포인터 append: `- [Title] → feedback_{tag}.md — one-line hook`.

   **global_memory**
   - 프로젝트 메모리와 동일하되 "current project" 이 아닌 **모든 세션에서 로드되는 글로벌 memory 영역**.
   - 구체 경로는 Claude Code 버전에 따라 다름 — 사용자 설정 확인 후 진행.

   **path_scoped_rule**
   - `.claude/rules/<tag>.md` 생성. 해당 파일은 특정 glob 편집 시만 로드됨.
   - frontmatter에 `path_glob` 또는 `file_glob` 지정 필요 (프로젝트 사양에 따라).
   - 사용자에게 어떤 파일 경로에 스코핑할지 확인.

   **skill**
   - 스킬 신설은 `harness:create-skill` 스킬을 호출하도록 **제안**만 한다. 이 스킬이 직접 `skills/<name>/SKILL.md`를 생성하지 마라 — 스킬 설계 품질 확보를 위해.
   - 기존 스킬 Gotchas 추가가 더 적합하면 해당 SKILL.md 경로를 보여주고 diff 제안.

   **hook**
   - 영향 범위 큼. **초안만 제시하고 실제 hooks.json 수정은 사용자가 직접** 하게 한다.
   - 초안에는 이벤트 타입, matcher, command, timeout 을 모두 포함한다. 아래 **이벤트 타입 사실**을 지키지 않은 초안은 예방 게이트가 아니다 (근거: https://code.claude.com/docs/en/hooks).

   | 사실 | 초안에 미치는 영향 |
   |---|---|
   | `PreToolUse` 는 tool call **직전**에만 실행된다 | 예방 게이트는 반드시 `PreToolUse` 다 |
   | `PreToolUse` 의 `exit 2` 가 그 tool call 을 **block** 한다 | 차단 의도면 exit code 2 를 명시하라. exit 0/1 은 막지 않는다 |
   | `PostToolUse` 는 **이미 성공한** tool 뒤에 실행된다. 거기서의 `exit 2` 는 stderr 를 Claude 에게 보여줄 뿐 실행을 되돌리지 못한다 | **`PostToolUse` 는 예방 surface 가 아니다.** E3 게이트를 여기에 걸지 마라 — 피드백용이다 |
   | `@` 파일 참조에는 `PreToolUse` 가 실행되지 않는다 | `@file` 경로로 우회되는 규칙은 훅으로 못 막는다. 조건에 명시하라 |
   | timeout 난 command/http/mcp `PreToolUse` 훅은 tool call 을 **막지 않는다** | timeout 값을 초안에 반드시 적고, 무거운 검사는 게이트로 쓰지 마라 |

   - **eligibility denominator 를 조건에 박아라.** "API 문서를 확인하라" 같은 서술은 게이트가 될 수 없다. "**Edit/Write/Bash 로 변경하기 직전, 이번 turn/session 에 공식 docs 조회 증거가 없으면 block**" 처럼 (a) 언제 재는지 (b) 무엇을 세는지 (c) 무엇이 통과인지가 있어야 한다.
   - 초안에는 **관측 카운터**(fired / blocked / bypassed / timeout)를 남기는 방법도 함께 적는다. 카운터가 없으면 다음 주기에 §B-0 를 돌릴 수 없다. hard gate 는 위반을 줄이지만 false positive 가 많으면 alert fatigue 로 무력화되며 (임상 알람 연구에서 false alarm 비율 72~99% 가 desensitization·missed alarm 으로 이어진다: https://pubmed.ncbi.nlm.nih.gov/24153215/), 우회된 게이트는 없는 게이트보다 나쁘다.

5. **rule_id 발급 + ledger append**
   - `rule_id=$(uuidgen)` (macOS/Linux 모두 기본 제공)
   - `promotions-ledger.md`에 아래 YAML 블록 append:
     ```yaml
     - rule_id: <uuid>
       mistake_tag: <canonical_tag>          # lemma_key 안 최빈 원시 표기
       lemma_key: <lemma_key>                # post_freq 집계의 실제 키
       aliases: [<lemma_key 클러스터의 나머지 멤버 전체 — tag_canon_groups 출력 그대로>]
       promoted_to: <surface>
       enforcement_level: E1 | E2 | E3
       target_path: <절대경로>
       promoted_at: <ISO8601+TZ>
       source_evidence:
         - path: ~/.claude/logs/<id>/reflections-YYYY-MM.md
           anchor: <digest가 집계한 타임스탬프 헤더>
       initial_freq: <int>
       calibration_window_days: 30
       post_freq: null
       status: active
     ```
   - `post_freq: null` 로 둔다. `/reflect-kaizen`이 30일 뒤 숫자로 채운다 (`aliases` 포함 합산).
   - `aliases` 는 `tag_canon_groups` 가 낸 `lemma_key` 클러스터의 멤버 **전체**를 그대로 옮긴다 (Gotchas #9). **비워두거나 손으로 추리면 `post_freq` 가 구조적으로 과소집계되어 효과 없는 규칙이 "효과 있음" 으로 오판정된다.**
   - `enforcement_level` 은 신규 승격이면 아래 매핑표에서 surface 에 대응하는 값을 적는다.

6. **결과 리포트**
   - 승격된 rule_id 리스트 + 수정된 파일 경로 + skip된 후보 사유.
   - 등급 상향한 rule_id 는 `E1 → E2` 형태로 before/after 를 명시.
   - **환경 액션 아이템** (`actionability: user_environment`) 은 승격하지 않았음을 명시하고 필요한 사용자 조치만 나열.

### B-0. 이미 승격했는데 `post_freq` 가 **증가**했다 → `hook_coverage_audit`

§B(등급 상향)로 가기 전에 이 분기를 먼저 통과해야 한다. **진입 조건**: ledger 엔트리가
`status: active` 이고 `promoted_to` 가 `hook` 또는 `*_claude_md` 인데, 최신 `post_freq` 가
`initial_freq` **이상**인 경우.

이 상태에서 같은 문구를 다시 쓰거나 등급만 한 칸 올리는 것은 오진이다. 실측 근거:
`skipped-required-api-doc-check` 는 직전 사이클 9 건 → 2026-08 30 건 이상으로 **늘었고**,
그 사이 사용자는 이미 PreToolUse 훅을 등록해 둔 상태였다. 규칙이 없어서 위반한 게 아니라
**게이트가 그 경로에서 작동하지 않은 것**이다.

**점검 9 항 — 전부 실행 결과로 답하라. "설정돼 있을 것이다" 는 답이 아니다.**

| # | 점검 | 확인 방법 | FAIL 이면 |
|---|---|---|---|
| 1 | hook installed | 해당 훅이 실제 settings/hooks 선언에 존재하는가 | 승격이 착지하지 않았다 — 재작성 아님, 설치 |
| 2 | event type | 예방 의도인데 `PostToolUse` 에 걸려 있지 않은가 | `PreToolUse` 로 이동 (§A step 4 hook 표) |
| 3 | matcher | 실제로 위반이 일어난 tool 이 matcher 에 잡히는가 | matcher 확장 |
| 4 | path normalization | 상대경로·심볼릭링크·서브디렉토리 cwd 에서도 같은 판정인가 | 경로 정규화 |
| 5 | exit code | 차단 의도인데 `exit 2` 를 쓰는가 | exit code 수정 |
| 6 | timeout | timeout 값이 검사 소요보다 큰가 (timeout 난 PreToolUse 는 **막지 않는다**) | 검사를 가볍게 하거나 timeout 상향 |
| 7 | executable | 스크립트 실행 권한·shebang·인터프리터가 있는가 | 권한/의존성 수정 |
| 8 | dependency | 훅이 쓰는 CLI/파일이 그 환경에 실재하는가 | 의존성 설치 또는 fail-open 명시 |
| 9 | fired/blocked 카운터 | fire 는 했는데 block 을 안 한 것인가, 아예 fire 를 안 한 것인가 | 두 경우의 처방이 다르다 |

**라우팅 규칙**

- 1~9 중 하나라도 FAIL → **`hook_coverage_audit` 결과로 보고하고 등급 상향을 하지 않는다.**
  ledger 엔트리는 그대로 두고 `## hook coverage` 절에 FAIL 항목과 조치를 적는다.
  같은 문구를 다시 승격하지 마라 — 그것은 이미 실패한 처방의 반복이다.
- 9 항 전부 PASS 인데도 재발이 늘었다 → 그때 비로소 §B 등급 상향 대상이다.
  이 경우 근본원인 재정의(태그가 잘못 묶였는지 — SSOT §4 family 확인)를 먼저 검토한다.
- **훅 자체가 사용자 환경(`~/.claude/settings.json`, `~/.claude/hooks/`)에 있으면 진단만 하고
  고치지 마라.** Gotchas #1 대로 초안·점검 결과만 제시하고 반영은 사용자가 한다.

### B. 재발 — Enforcement 등급 상향

> **SSOT**: `harness/docs/guides/skill-design-guide.md` §3.7 "Enforcement 3 등급".
> E1/E2/E3 의 정의·승급 임계는 그 문서가 정본이다. **여기서 재정의하거나 동의어를 만들지 마라.**
>
> **진입 전제**: §B-0 를 통과했을 것. hook / CLAUDE.md 로 이미 승격한 규칙의 `post_freq` 가
> 증가했다면 등급 상향이 아니라 `hook_coverage_audit` 이 먼저다.

승격했는데도 같은 규칙이 재발했다는 것은 문구가 부족한 게 아니라 **강제 수준이 부족한** 것이다.
`/insights` 2026-07-27 §0 은 직전 사이클 승격분(Friction #1·#3)의 세션당 발생 비율이 줄지 않았음을,
digest 는 PreToolUse 훅이 경고를 띄웠는데도 `skipped-required-api-doc-check` 가 9회 재발했음을 보여준다.

1. **재발량 확정** — ledger 엔트리의 `post_freq` 를 digest 최신값(`canonical_tag` + `aliases` 합산)으로 갱신한다. `promoted_at + calibration_window_days` 미도달이면 상향하지 말고 관망한다.
2. **승급 판정** — SSOT §3.7 의 승급 규칙을 그대로 적용한다: **재발 2회 이상 → E1 → E2**, **3회 이상이거나 비가역 변경·사용자 신뢰 손상이 걸리면 → E2 → E3**. `post_freq == 1` 이면 상향하지 않고 문구 명확화 + 다음 주기 재측정.
3. **surface 재배치** — 등급이 올라가면 그에 맞는 surface 로 옮긴다.

   | §3.7 등급 | reflect-kit surface | 형태 |
   |---|---|---|
   | E1 | project/global memory, CLAUDE.md 한 줄 | 서술문 (on-demand 또는 매 세션 로드) |
   | E2 | path_scoped_rule, skill 의 Process 체크리스트 | 편집 시 로드되는 규칙 / 채워야 하는 아티팩트 |
   | E3 | hook (PreToolUse 등), 검증 스크립트 | LLM 호출 없이 행위 직전 차단 |

   E3 는 여전히 Gotchas #1 대로 **초안만 제시하고 hooks.json 수정은 사용자가** 한다.
4. **ledger 갱신** — 기존 엔트리를 새 엔트리로 대체하지 마라. 기존 엔트리의 `status` 를 `demoted` + `demotion_reason: escalated-to-E<N> (rule_id: <새 uuid>)` 로 바꾸고, 새 등급의 엔트리를 append 한다. `source_evidence` 에 재발 근거 앵커를 추가하고 `initial_freq` 는 재발 시점의 `post_freq` 로 둔다. 이렇게 해야 "E1 에서 실패 → E2 로 올림" 이력이 남는다.
5. **사용자 승인** — 등급 상향도 surface write 이므로 Gotchas #1 이 그대로 적용된다. 특히 E3(hook) 은 개별 승인 필수.

### C. Rollback 경로

1. `rule_id` 또는 `tag` 로 ledger 엔트리 조회.
2. `target_path` 파일 읽기.
3. 해당 규칙 블록 위치 찾기:
   - project_claude_md / global_claude_md: `rule_id:` 수명이 포함된 라인 grep.
   - memory / path_scoped_rule: 파일 자체 삭제 + MEMORY.md 포인터 제거.
   - skill / hook: 사용자에게 경로만 안내, 자동 롤백 금지.
4. 해당 라인/파일 제거.
5. ledger 엔트리의 `status`를 `removed` 또는 `demoted`로 업데이트. `demotion_reason` 기록 (예: `post_freq=0 after 30d + low risk` 또는 `user_requested`).
6. 결과 리포트: 되돌린 rule_id + 수정된 파일.

## 안티패턴 (하지 말 것)

- digest 없이 "이런 규칙 필요할 것 같다"로 독자 판단해서 승격하지 마라. 증거가 ledger의 source_evidence에 없으면 규칙이 아니다.
- 여러 후보를 한꺼번에 자동 승인으로 처리하지 마라 (특히 CLAUDE.md / hook).
- rollback 시 ledger 엔트리를 `rm`이나 `sed -i` 로 삭제하지 마라 — 이력 유실. `status` 필드 업데이트로만.
- project_memory 후보를 global_memory로 자의 확대 마라. scope 축은 digest에서 결정된 값을 그대로 쓴다.
- CLAUDE.md 200줄 한도 초과를 무시하고 append 하지 마라. 공식 권고 위반 + context window 낭비.
- **재발한 규칙을 같은 surface·같은 등급에서 문구만 다듬지 마라.** 등급을 올리거나(§B), 왜 올리지 않는지 근거를 대라.
- **E1/E2/E3 를 이 문서에서 재정의하지 마라.** 정의·승급 임계는 `harness/docs/guides/skill-design-guide.md` §3.7 이 정본이다. 동의어(`레벨1`, `soft/hard` 등)를 만들지 마라.
- **`aliases` 를 비우거나 손으로 추린 채 ledger 에 append 하지 마라** — post_freq 과소집계로 효과 없는 규칙이 살아남는다. `tag_canon_groups` 출력을 그대로 옮겨라.
- **환경 오설정(`user_environment`)을 규칙으로 승격하지 마라** — 사용자 조치 안내로만.
- **예방 게이트를 `PostToolUse` 에 걸지 마라** — 이미 실행된 도구를 되돌리지 못한다. 예방은 `PreToolUse` + `exit 2` 다.
- **`post_freq` 가 늘었는데 §B-0 없이 등급만 올리지 마라** — 훅이 안 걸린 것을 문구 문제로 오진하면 다음 사이클에 같은 숫자가 또 올라온다.
- **사용자 환경(`~/.claude/settings.json`, `~/.claude/hooks/`)을 직접 고치지 마라** — 진단 결과와 초안만 제시한다.
- **`grounding: self_inference` 인 메모리 엔트리를 근거로 승격하지 마라** — 외부 검증이 없는 자기추론이다. 승격하면 자기 산출물이 자기 근거가 되는 루프가 닫힌다. `grounding` 미보유(미태깅)도 같다.
- **memory surface 로 승격하면서 `grounding` 을 비워두지 마라** — 미태깅 엔트리는 다음 주기 소비면이 근거 등급을 판정할 수 없다.
- **`grounding` 값을 이 문서에서 재정의하거나 나열하지 마라** — 정본은 `reflect-kit/references/memory-grounding.md` 하나다.

## 예시 사용

- `/reflect-promote` — 직전 digest의 후보 리스트를 승인 플로우로 처리
- `/reflect-promote action=rollback rule_id=a1b2c3d4-...` — 특정 규칙 되돌리기
- `/reflect-promote action=rollback tag=wrong-path-inference` — 최근 active 엔트리 되돌리기

## 관련 문서

- `reflect-kit/references/tag-canonicalization.md` — canonical / alias / family 규약 SSOT
- `reflect-kit/references/memory-grounding.md` — 메모리 엔트리 `grounding` 축 정의 SSOT (4 값 · 판정 절차 · 소비면 취급)
- `.claude/skills/kaizen-orchestrator/SKILL.md` Step F3.5 — 카이젠 사이클이 내는 승격 후보 파일의 산출 조문
- `reflect-kit/hooks/_lib-tag-canon.sh` — `tag_canon_groups` 실행 구현
- `reflect-kit/docs/DESIGN.md` — Precedence Table 원본 정의
- `reflect-kit/docs/SCHEMA.md` — YAML + Ledger 스키마 정본
- `reflect-kit/skills/reflect-digest/SKILL.md` — 입력 후보를 생성하는 선행 스킬
- `reflect-kit/skills/reflect-kaizen/SKILL.md` — 승격 규칙의 30일 효과 측정 + calibration
