---
phase: 12
title: "Phase 12 reflect-kit — 확보된 외부 근거"
collected: 2026-09-24
method: codex (foreground, 직접 호출 · gpt-5.6-sol · 조회는 curl/gh)
inputs: 처리 배정표(.claude/kaizen-input/insights-report.md)의 Phase 12 행 · phase-research-templates.md Phase 12 필수 출처 · 현행화 점검
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치를 지어내지 마라. 없으면 미반영으로 남긴다.
---

## 1. 출처 목록

실제로 조회한 외부 출처:

1. [Claude Code Hooks reference](https://code.claude.com/docs/en/hooks)
2. [Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference)
3. [Claude Code model configuration](https://code.claude.com/docs/en/model-config)
4. [Claude Code headless mode](https://code.claude.com/docs/en/headless)
5. [Claude Code v2.1.281 release](https://github.com/anthropics/claude-code/releases/tag/v2.1.281)
6. [Codex non-interactive mode](https://developers.openai.com/codex/noninteractive)
7. [Codex CLI v0.156.1 release](https://github.com/openai/codex/releases/tag/rust-v0.156.1)
8. [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)
9. [MultiSoc-4D: Instruction-Induced Label Collapse](https://arxiv.org/abs/2605.06940)
10. [Improving Labeling Consistency with Detailed Constitutional Definitions](https://arxiv.org/abs/2605.24247)
11. [Sentry Fingerprint Rules](https://docs.sentry.io/concepts/data-management/event-grouping/fingerprint-rules/)
12. [Prometheus Alertmanager configuration](https://prometheus.io/docs/alerting/latest/configuration/)
13. [git-rev-parse 공식 문서](https://git-scm.com/docs/git-rev-parse)
14. [Git 공식 GitHub tags](https://github.com/git/git/tags)

읽은 내부 근거:

- `~/.claude/logs/*/reflections-*.md`
- `~/.claude/logs/*/.errors.log`
- `~/.claude/logs/*/.env-issues.tsv`
- `~/.claude/usage-data/facets/*.json`
- `~/.claude/usage-data/session-meta/*.json`

## 2. 항목별 관찰 사실

### reflect-collector:P3 — Stop 수집 복구

확인된 사실:

- 현재 소스와 설치본 모두 `codex exec --full-auto`를 사용한다. 로컬 `codex-cli 0.154.0`에서 `codex exec --full-auto --help`는 실제로 `error: unexpected argument '--full-auto' found`와 exit 2를 반환했다. 소스는 [log-reflection.sh:273](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/reflect-kit/hooks/log-reflection.sh:273), 설치본도 동일한 273행이다.
- 최신 Codex 문서는 `codex exec` 기본 sandbox가 read-only라고 명시하고, 자동화는 필요한 최소 권한을 명시적으로 선택하라고 권한다. `--full-auto`는 deprecated compatibility flag이며 새 스크립트에는 명시적인 `--sandbox workspace-write`를 쓰라고 한다. 따라서 읽기만 필요한 이 호출에서 `-s read-only`를 명시하는 것은 공식 권한 모델과 일치한다. 다만 기능상 기본값도 이미 read-only이므로 `-s read-only`는 주로 계약을 명시하고 사용자 설정 변화에 대한 의도를 고정하는 효과다. [Codex non-interactive 문서](https://developers.openai.com/codex/noninteractive)
- 최신 안정 Codex CLI는 2026-09-23 공개된 0.156.1이고, 로컬은 0.154.0이다. 최신 문서는 `--full-auto`를 “deprecated지만 남아 있는” 것으로 설명하는 반면 로컬 0.154.0은 아예 거부한다. 즉 문서와 실제 설치 버전의 동작이 어긋난다. 호환 플래그에 의존하지 않고 제거하는 것이 안전하다. [Codex 0.156.1](https://github.com/openai/codex/releases/tag/rust-v0.156.1)
- Codex와 Claude fallback 모두 stderr를 폐기한다. [log-reflection.sh:248](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/reflect-kit/hooks/log-reflection.sh:248), [log-reflection.sh:277](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/reflect-kit/hooks/log-reflection.sh:277)
- 2026-09-14~23 내부 로그에는 `fail:codex-exit-2` 849행, `fallback:claude-exit-1` 849행, `fallback:claude-used` 0행이 있다. 실패에 등장한 고유 session ID는 55개다. 같은 세션에서 Stop이 여러 번 발생하므로 849는 세션 수가 아니라 호출/시도 수다.
- 해당 기간 reflection 기록 세션은 0이고, 전체 reflection의 마지막 기록은 `2026-08-28T17:28:39+0900`이다.
- Claude Code 공식 문서는 hook command가 JSON을 stdin으로 받고, 공통 입력에 `session_id`, `transcript_path`, `cwd`가 있다고 명시한다. Stop에는 `stop_hook_active`와 `last_assistant_message`도 있다. [Hooks reference](https://code.claude.com/docs/en/hooks)
- 반대 근거: 공식 문서는 transcript 파일이 비동기로 쓰여 Stop 시점에 최신 턴이 아직 없을 수 있다고 경고하고, 방금 끝난 응답은 `last_assistant_message`를 쓰라고 한다. 따라서 “Stop transcript는 언제나 완전하다”는 계약은 성립하지 않는다. 다만 이 수집기는 세션 전체 최근 150행을 분석하므로 transcript 자체를 없앨 수는 없다. [Hooks reference](https://code.claude.com/docs/en/hooks)
- Claude fallback의 `haiku-4.5`는 공식 alias도 full model name도 아니다. 공식값은 `haiku` alias 또는 `claude-haiku-4-5` 형식이다. [Model configuration](https://code.claude.com/docs/en/model-config)
- `claude -p`는 성공 시 0, 실패 시 non-zero를 반환하고 invalid flag는 stderr로 보고한다. 또한 `--no-session-persistence`가 공식 제공되므로 fallback이 새 세션 기록을 만들 필요가 없다면 추가할 수 있다. [Headless mode](https://code.claude.com/docs/en/headless), [CLI reference](https://code.claude.com/docs/en/cli-reference)
- 최신 Claude Code는 command hook의 native `async`와 `asyncRewake`를 제공한다. 현재 수동 `nohup` 방식은 여전히 작동할 수 있지만, 공식 hook lifecycle 밖에서 stderr를 버리는 원인이 된다. [Hooks reference](https://code.claude.com/docs/en/hooks)

추론:

- 849쌍의 exit 2/exit 1과 로컬에서 재현된 `unexpected argument '--full-auto'`를 합치면, Codex 단계의 직접 원인은 `--full-auto`일 가능성이 매우 높다.
- Claude fallback의 직접 원인은 기록이 없어 단정할 수 없다. `haiku-4.5`가 공식 형식이 아닌 점은 강한 후보지만 stderr 복구 후 확인해야 한다.

### reflect-collector:P4 — 수집 상태와 facets 대조

확인된 사실:

- 현행 digest는 파싱 실패를 헤더에 노출하도록 이미 강제하지만, collector 자체가 0건을 생산하는 상태는 별도로 표시하지 않는다. [reflect-digest/SKILL.md:31](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/reflect-kit/skills/reflect-digest/SKILL.md:31), [reflect-digest/SKILL.md:296](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/reflect-kit/skills/reflect-digest/SKILL.md:296)
- 실측 기간에는 reflection 세션 0, Codex 실패 시도 849, fallback 실패 시도 849, 마지막 성공 2026-08-28이다. 따라서 `엔트리 0 = 문제 없음`으로 읽으면 실제 상태와 정반대다.
- facets 파일은 정확히 18개이고 대응하는 session-meta 18개도 모두 읽혔다. 18개 중 `friction_detail`이 비어 있지 않은 세션은 16개, 빈 세션은 2개다. reflections에는 이 18개 session ID가 모두 0건이다.
- facets JSON에는 `session_id`와 `friction_detail`은 있지만 `project_path`는 없다. `project_path`와 `start_time`은 대응하는 `session-meta/<session_id>.json`에 있다. 따라서 P4의 join 경로는 `facets.session_id → session-meta.session_id → project_path`여야 한다.
- facets와 session-meta의 공개 형식 문서는 찾지 못했다. 따라서 필수 입력 계약으로 승격할 외부 근거는 없다.
- Reflexion 원전은 언어적 피드백을 reflective text로 만들고 episodic memory buffer에 유지하여 후속 trial의 의사결정을 개선하는 구조를 제안한다. 이는 reflection 저장·재주입의 방법론적 근거이지만, facets를 동일 집계에 합산하거나 영구 규칙으로 곧장 승격하는 근거는 아니다. [Reflexion](https://arxiv.org/abs/2303.11366)
- 닫힌 라벨 연구는 LLM이 `Other/Neutral/No` 같은 fallback label로 몰려 높은 agreement처럼 보이면서 소수 범주를 놓칠 수 있다고 보고한다. 해당 연구에서는 hateful·sarcastic 사례의 79%·75%를 인간 보정 기준보다 놓쳤고 sarcasm Fleiss’ κ가 약 -0.001이었다. 이는 `mistake_tag`를 hard enum으로 닫지 않고 known canonical 우선 + 새 태그 허용 정책을 유지할 근거다. [MultiSoc-4D](https://arxiv.org/abs/2605.06940)
- 반대 근거: 위 연구는 Bengali social-media annotation이라는 제한된 도메인의 2026년 preprint다. coding transcript용 reflect taxonomy에 동일 수치를 일반화할 수 없다.
- 라벨 상세도 연구는 단순 정의만으로는 일관된 golden label을 만들기 어렵지만, 지나치게 상세한 문서는 인간 작업기억을 넘어서 직관 회귀와 drift를 일으킬 수 있다고 말한다. LLM이 상세 constitution을 매 사례에 해석하는 방식은 paragraph definition 대비 cross-model inconsistency를 최대 57배 줄였다고 보고한다. [Labeling Consistency](https://arxiv.org/abs/2605.24247)
- 이는 현재의 태그 작성 규칙과 `new_tag_reason`을 지지하지만, 규칙을 무한히 늘리는 것은 지지하지 않는다. 연구 자체도 3개 content-moderation 범주에 대한 preprint여서 reflect-kit에 대한 직접 검증은 아니다.
- Sentry fingerprint 규칙은 먼저 일치한 규칙을 적용해 기본 grouping을 대체하거나 세분화한다. 동시에 자주 변하는 `error.value`나 message를 fingerprint에 넣으면 “really bad groups” 또는 낮은 데이터 품질을 만들 수 있다고 경고한다. 즉 안정된 근본원인 key로 canonicalize하되 변동성 높은 원문을 grouping key로 쓰지 않는 정책과 맞는다. [Sentry Fingerprint Rules](https://docs.sentry.io/concepts/data-management/event-grouping/fingerprint-rules/)
- Alertmanager는 `group_by`로 같은 성격의 alert를 묶고 `group_interval`과 `repeat_interval`로 반복 알림을 제한한다. 기본 repeat interval은 4시간이다. [Alertmanager configuration](https://prometheus.io/docs/alerting/latest/configuration/)
- 반대 근거: Alertmanager는 현재 reflect-kit의 7일 억제 창을 뒷받침하지 않는다. 7일은 digest 주기에 맞춘 로컬 hypothesis이며, 현재 문서도 그렇게 표시하는 것이 맞다.

추론:

- facets는 “수집기가 놓친 세션을 찾는 독립 탐지기”로는 강한 보조 신호지만, taxonomy·분석기·입력 시점이 다르므로 reflection 빈도에 합산하면 double counting과 척도 혼합이 생긴다.
- 이번 18세션에서는 `friction_detail 존재 + reflection 0`이 16세션이므로, 대조 절이 collector outage를 즉시 드러내는 역할을 실제로 수행한다.

### reflect-collector:P5 — worktree project identity

확인된 사실:

- 현재 `compute_project_id`는 `git rev-parse --show-toplevel`을 사용한다. linked worktree에서 이는 현재 worktree 경로를 반환하므로 basename이 `release-0924`, `bambu-orca-h2s-feedback`처럼 갈린다. [_lib-project-id.sh:57](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/reflect-kit/hooks/_lib-project-id.sh:57)
- 현재 작업 경로에서 실제 결과는 다음과 같다.

  - `--show-toplevel`: `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924`
  - `--path-format=absolute --git-common-dir`: `/Users/jackson/Hub/10_Dev/claude-plugins/.git`
  - common-dir의 상위 경로: `/Users/jackson/Hub/10_Dev/claude-plugins`

- Git 공식 문서는 `--path-format=absolute`가 대상 경로를 absolute canonical path로 출력하고, `--git-common-dir`는 `$GIT_COMMON_DIR` 또는 `$GIT_DIR`을 반환한다고 명시한다. `--show-toplevel`은 현재 working tree의 최상위 경로다. [git-rev-parse](https://git-scm.com/docs/git-rev-parse)
- 따라서 일반 checkout과 linked worktree에서는 common dir의 basename이 `.git`일 때 그 parent를 identity root로 삼는 방식이 본 레포 이름을 안정적으로 돌려준다.
- 같은 `--show-toplevel` 규칙이 [save-feedback.sh:128](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/harness/scripts/save-feedback.sh:128), [save-feedback.sh:136](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/harness/scripts/save-feedback.sh:136)에 복제돼 있다.
- 현재 18개 facets 중 worktree 경로를 가진 세션도 있으며, session-meta의 `project_path`를 그대로 basename하면 별도 worktree project가 된다.
- 로컬 Git은 2.53.0이고 이 옵션 조합이 정상 동작했다. 최신 안정 tag는 2.55.0이며 2.56.0은 아직 RC다. [Git tags](https://github.com/git/git/tags)

반대 근거와 경계:

- `dirname(git-common-dir)`을 무조건 적용하면 submodule에서 common dir가 상위 레포의 `.git/modules/<submodule>`일 수 있고, bare repository에서도 기대하는 working-tree root가 없다. 단순 parent-basename만을 보편 규칙으로 만들면 `modules`나 상위 디렉터리 이름으로 잘못 묶일 수 있다.
- 추론: `basename(common_dir) == ".git"`인 일반/linked-worktree 경우에만 parent를 쓰고, 그 외에는 기존 `--show-toplevel` 또는 cwd fallback을 쓰는 방어 규칙이 필요하다.
- 기존 worktree 이름 bucket은 새 규칙으로 자동 합쳐지지 않는다. 새 기록은 바로잡히지만 과거 `release-*`, `wall-clock-release` 등의 bucket은 별도다. 마이그레이션 또는 read-union 여부가 별도 결정 사항이다.

## 3. 현행화 — 낡은 곳

| 파일:줄 | 현재 값 | 최신 값/상태 | 근거 |
|---|---|---|---|
| [log-reflection.sh:273](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/reflect-kit/hooks/log-reflection.sh:273) | `--full-auto` | 제거 후 `-s read-only`; 최신 문서에서 `--full-auto` deprecated, 로컬 0.154.0에서는 아예 거부 | [Codex non-interactive](https://developers.openai.com/codex/noninteractive) |
| [log-reflection.sh:248](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/reflect-kit/hooks/log-reflection.sh:248) | `--model haiku-4.5`, stderr 폐기 | 공식 alias `haiku` 또는 full name `claude-haiku-4-5`; stderr 보존. 필요하면 `--no-session-persistence` | [Model config](https://code.claude.com/docs/en/model-config), [CLI reference](https://code.claude.com/docs/en/cli-reference) |
| [log-reflection.sh:277](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/reflect-kit/hooks/log-reflection.sh:277) | stdout·stderr 모두 `/dev/null` | stderr 임시 파일 수집 후 첫 줄을 `.errors.log`에 기록 | [Claude hook stderr/exit 계약](https://code.claude.com/docs/en/hooks) |
| [hooks.json:30](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/reflect-kit/hooks/hooks.json:30) | shell form에서 `${CLAUDE_PLUGIN_ROOT}` 미인용 | exec form의 `command: bash`, `args: ["${CLAUDE_PLUGIN_ROOT}/..."]` 또는 placeholder를 이중 인용 | [Hooks reference](https://code.claude.com/docs/en/hooks), [Claude Code 2.1.281](https://github.com/anthropics/claude-code/releases/tag/v2.1.281) |
| [hooks.json:25](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/reflect-kit/hooks/hooks.json:25), [log-reflection.sh:35](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/reflect-kit/hooks/log-reflection.sh:35) | 수동 `nohup` background | 최신 hook 계약에는 native `async`/`asyncRewake`가 있음. 즉시 교체 필수는 아니지만 현행화 검토 대상 | [Hooks reference](https://code.claude.com/docs/en/hooks) |
| [_lib-project-id.sh:62](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/reflect-kit/hooks/_lib-project-id.sh:62) | `--show-toplevel` | guarded common-dir identity | [git-rev-parse](https://git-scm.com/docs/git-rev-parse) |
| [save-feedback.sh:128](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/harness/scripts/save-feedback.sh:128), [save-feedback.sh:136](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/harness/scripts/save-feedback.sh:136) | `--show-toplevel` | reflect-kit과 같은 guarded common-dir 규칙 | [git-rev-parse](https://git-scm.com/docs/git-rev-parse) |
| [reflect-digest/SKILL.md:110](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/reflect-kit/skills/reflect-digest/SKILL.md:110) | 현재 cwd의 worktree basename 가능 | collector와 같은 common-repo identity | [Git 문서](https://git-scm.com/docs/git-rev-parse), [Claude의 worktree `cwd` 계약](https://code.claude.com/docs/en/hooks) |
| [reflect-digest/SKILL.md:297](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/reflect-kit/skills/reflect-digest/SKILL.md:297) | 엔트리/세션/파싱 실패만 표시 | collector 실패, 마지막 성공, stopped 경고 추가 | 내부 실측 |
| [SCHEMA.md:191](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/reflect-kit/docs/SCHEMA.md:191) | 항상 `<basename>-<hash6>` | 이미 구현·README와 불일치. Hybrid + common-repo root 규칙으로 갱신 필요 | 내부 구현 |
| [plugin.json:4](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/reflect-kit/.claude-plugin/plugin.json:4) | `0.7.1` | P3/P5 반영 시 patch release 필요 | 내부 릴리스 계약 |

버전 대조:

- Codex CLI: 로컬 0.154.0 / 최신 안정 0.156.1. 레포에 최소 버전 pin은 없지만 사용 플래그가 로컬과 비호환이다. [0.156.1](https://github.com/openai/codex/releases/tag/rust-v0.156.1)
- Claude Code: 로컬 2.1.268 / 최신 안정 2.1.281. README의 `v2.1.59+`가 곧바로 깨졌다는 근거는 찾지 못했다. 다만 최신 validator는 미인용 plugin-root hook을 경고한다. [2.1.281](https://github.com/anthropics/claude-code/releases/tag/v2.1.281)
- Git: 로컬 2.53.0 / 최신 안정 2.55.0. P5에 필요한 옵션은 로컬에서 이미 정상 동작하므로 업그레이드가 선행 조건은 아니다. [Git tags](https://github.com/git/git/tags)

## 4. 권장안

### P3 계약

- Codex 호출은 `--full-auto`를 제거하고 `-s read-only`를 명시한다.
- Codex와 Claude 각각 stderr 전용 임시 파일을 사용한다.
- 실패 로그는 최소한 다음을 포함한다.

  `fail:codex-exit-2 session=<id> err=<stderr 첫 비어 있지 않은 줄>`

- stderr 첫 줄은 길이 제한과 기존 `redact_sensitive`를 통과시킨다. 원문 전체를 `.errors.log`에 넣으면 토큰·경로·인증 정보가 유출될 수 있다.
- fallback 모델은 `haiku` 또는 `claude-haiku-4-5`로 바꾸고 `--no-session-persistence`를 추가한다.
- 임시 파일은 성공·실패·signal 모두 정리하도록 trap 계약을 둔다.
- 설치본 캐시를 직접 고치는 방식이 아니라 `0.7.2` patch release 후 설치/업데이트된 artifact에서도 해당 행을 검증한다.
- 별도 후속으로 native `async` 전환을 검토한다. 이번 patch에서 수동 background를 유지한다면, fast path의 stderr 폐기와 실제 분석기 stderr 폐기를 구분해 문서화한다.

### P4 계약

- Process 4단계에서 reflection 파싱 전에 `.errors.log`의 기간 필터를 수행한다.
- 요약은 실패 “행 수”와 실패 “시도 수”를 혼동하지 않게 정의한다. 이번 데이터라면 다음 형식이 가장 정확하다.

  `수집 상태: Stop 실패 시도 849회 (codex 849 · 대체 경로 849; 고유 세션 55) / 기록된 세션 0 / 마지막 기록 2026-08-28T17:28:39+0900`

- `codex 849 + fallback 849`는 동일 849회의 2단계 실패이므로 총 1,698회라고 표시하지 않는다.
- `M=0 && failed_attempts>0`이면 정확히 다음 경고를 출력한다.

  `⚠ 수집 멈춤 — 엔트리 0은 문제 없음이 아니다`

- 이 상태에서는 reflection 기반 승격 후보를 전부 금지하고 collector 복구를 `## 환경 액션 아이템`으로 보낸다.
- facets는 폴더가 있을 때만 읽는다. join은 `facets.session_id → session-meta/<id>.json → project_path → compute_project_id`로 고정한다.
- unreadable count는 `facets 읽기 실패`와 `session-meta 읽기 실패`를 나눠 표시한다.
- `friction_detail != "" && reflection session_id 없음`인 세션만 `## 인사이트 세션 분석과 대조`에 원문과 함께 표시한다.
- facets 자료는 `cluster_freq`, `project_count`, category/severity/4축, precedence, 규칙 표에 절대 합산하지 않는다.
- facets 폴더가 없으면 `(없음)`으로 정상 종료한다.
- 현재 known canonical + 새 tag 허용 + `new_tag_reason` 정책은 유지한다. hard enum 전환은 label-collapse 근거와 충돌한다.

### P5 계약

- identity root는 우선 다음처럼 계산한다.

  1. `git rev-parse --path-format=absolute --git-common-dir`
  2. 결과 basename이 `.git`이면 그 parent를 canonical repository root로 사용
  3. 그렇지 않으면 `git rev-parse --show-toplevel`
  4. Git 밖이면 기존 cwd fallback

- common-dir 명령 성공 여부와 빈 출력을 모두 검사한다.
- collision marker와 hash 입력도 동일 canonical root를 사용한다.
- `_lib-project-id.sh`, harness의 두 함수, facets의 project grouping이 같은 구현/fixture를 공유해야 한다.
- 최소 fixture는 main checkout, linked worktree, Git 밖 디렉터리, basename 충돌, submodule 또는 비표준 git-dir이다.
- 기존 worktree-name bucket을 새 main-repo bucket과 읽기에서 합칠지 명시적으로 결정한다. 아무 조치가 없으면 과거 worktree 데이터는 계속 분리된다.

## 5. 못 가져온 것 / 열린 질문

- facets/session-meta 형식의 공개 공식 문서는 찾지 못했다. 현재 관찰한 JSON 형식만 근거로 optional·fail-open 입력으로 다뤄야 한다.
- Claude fallback exit 1의 실제 stderr는 과거 로그에 없어 원인을 확정하지 못했다. `haiku-4.5`가 비공식 이름이라는 사실까지만 확인했다.
- `수집 상태`의 N을 “실패 stage 행 수”, “Stop 시도 수”, “고유 세션 수” 중 무엇으로 정의할지 기존 계약에는 없다. 권장안은 시도 수 849를 N으로 하고 고유 세션 55를 별도 표시하는 것이다.
- Stop transcript가 마지막 응답을 포함한다는 보장은 없다. P3 복구 후 누락 정도를 확인하고 필요하면 `last_assistant_message`를 분석 입력에 덧붙여야 한다.
- 7일 환경 억제 창은 Alertmanager 선행 사례에서 직접 나오지 않는다. 계속 hypothesis로 표시해야 한다.
- common-dir parent 규칙의 submodule·bare repo 의미는 Phase fixture에서 확정해야 한다.
- 과거 worktree별 로그 bucket을 읽기 union 또는 마이그레이션할지는 P5 제안에 아직 정의돼 있지 않다.

파일은 수정하지 않았고 작업트리 상태도 변경되지 않았다.
