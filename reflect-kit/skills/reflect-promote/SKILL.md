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
3. **중복 승격 금지**. `promotions-ledger.md`에서 같은 `mistake_tag`가 `status: active`로 존재하면 신규 엔트리 append 하지 말고 "기존 규칙 강화" 제안만 한다 (본 ledger 엔트리의 initial_freq는 덮어쓰지 않는다).
4. **rollback은 ledger 엔트리 삭제가 아니다**. `status: removed` 또는 `demoted`로 업데이트하고 `demotion_reason` 기록. 실제 파일에서도 해당 규칙 블록을 제거해야 완결. ledger 자체는 이력 보존용.
5. **rule_id 발급은 UUID(`uuidgen`)로 한다**. 시간 정렬이 필요하면 ledger append 순서로 충분하다. ULID 라이브러리 의존성을 추가하지 마라.
6. **target_path는 절대경로로 기록**. 상대경로로 기록하면 세션 cwd 변경 시 rollback이 깨진다.
7. **skill 승격은 진정 새 절차가 필요한 경우만**. 기존 스킬에 Gotchas 한 항목 추가로 해결 가능하면 "기존 스킬 Gotchas 추가"로 분류하라 (별도 skill 신설은 보수적으로).

## 입력

- `action` (optional): `promote` (기본) / `rollback`
- `rule_id` (optional, rollback 시): 되돌릴 ledger 엔트리의 UUID
- `tag` (optional, rollback 시): rule_id 대신 mistake_tag로 가장 최근 active 엔트리를 지정

후보 리스트는 대화 맥락에서 최근 `/reflect-digest` 출력을 참조한다. 없으면 사용자에게 먼저 `/reflect-digest` 실행을 요청한다.

## Process

### A. Promote 경로

1. **전제 확인**
   - `/reflect-digest`의 최근 출력이 대화 내 존재하는가? 없으면 실행 요청하고 중단.
   - 현재 프로젝트 ID 확인: `${CLAUDE_PLUGIN_ROOT}/hooks/_lib-project-id.sh` 의 `compute_project_id`.
   - `promotions-ledger.md` 경로: `~/.claude/logs/<project_id>/promotions-ledger.md`. 없으면 생성.

2. **Precedence Table 재판정**
   - digest가 제안한 surface를 **그대로 믿지 말고** 다음 4축 + 빈도로 재판정:
     | # | 조건 | 승격 surface |
     |---|---|---|
     | 1 | `enforcement_need == hard_gate` | **hook 검토** |
     | 2 | `procedurality == multi_step_procedure` AND freq ≥ 2 | **skill** |
     | 3 | `scope == global` AND 복수 프로젝트 freq ≥ 3 | risk=high → **global CLAUDE.md** / 나머지 → **global memory** |

     **규칙 #3 판정 근거**: 단일 프로젝트 digest 결과로는 "복수 프로젝트" 조건을 검증할 수 없다. 반드시 `/reflect-digest project=all` 출력의 `global_freq` + `project_count` 두 값을 함께 확인해야 rule #3 로 올바르게 분류된다. single-project digest에서 올라온 후보는 rule #4/#5로 재할당하는 것이 일관된 처리.
     | 4 | `scope == project` AND freq ≥ 3 | **project CLAUDE.md** (200줄 초과 예상 시 path_scoped_rule) |
     | 5 | `scope == project` AND freq ≥ 2 | **project memory** |
     | 6 | `risk_class == low` AND freq == 1 | **관망 (skip)** |
     | 7 | 그 외 | **review 후보 (수동)** |
   - digest 제안과 다를 경우 사용자에게 차이를 보고하고 결정 받는다.

3. **중복 체크**
   - `promotions-ledger.md`를 grep하여 같은 `mistake_tag`가 `status: active`로 존재하는지 확인.
   - 존재 시 신규 엔트리 append 하지 않고 "기존 규칙 강화" 제안 (target_path의 해당 블록에 severity 근거 한 줄 추가 또는 초안만 제시).

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
   - 새 파일 `feedback_{tag}.md` 생성 (여기서 `{tag}`는 mistake_tag의 snake_case 변환). frontmatter: `name`, `description`, `type: feedback`.
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
   - 초안에는 이벤트 타입(PreToolUse / PostToolUseFailure 등), matcher, command 예시 포함.

5. **rule_id 발급 + ledger append**
   - `rule_id=$(uuidgen)` (macOS/Linux 모두 기본 제공)
   - `promotions-ledger.md`에 아래 YAML 블록 append:
     ```yaml
     - rule_id: <uuid>
       mistake_tag: <tag>
       promoted_to: <surface>
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
   - `post_freq: null` 로 둔다. `/reflect-kaizen`이 30일 뒤 숫자로 채운다.

6. **결과 리포트**
   - 승격된 rule_id 리스트 + 수정된 파일 경로 + skip된 후보 사유.

### B. Rollback 경로

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

## 예시 사용

- `/reflect-promote` — 직전 digest의 후보 리스트를 승인 플로우로 처리
- `/reflect-promote action=rollback rule_id=a1b2c3d4-...` — 특정 규칙 되돌리기
- `/reflect-promote action=rollback tag=wrong-path-inference` — 최근 active 엔트리 되돌리기

## 관련 문서

- `reflect-kit/docs/DESIGN.md` — Precedence Table 원본 정의
- `reflect-kit/docs/SCHEMA.md` — YAML + Ledger 스키마 정본
- `reflect-kit/skills/reflect-digest/SKILL.md` — 입력 후보를 생성하는 선행 스킬
- `reflect-kit/skills/reflect-kaizen/SKILL.md` — 승격 규칙의 30일 효과 측정 + calibration
