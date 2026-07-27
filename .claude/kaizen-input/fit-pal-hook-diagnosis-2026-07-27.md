---
type: diagnosis
target_repo: /Users/jackson/Hub/10_Dev/fit-pal
generated: 2026-07-27
generated_by: kaizen-orchestrator 2026-07-27 사이클 (Step 0.6 사용자 선택 — "reflect-kit + fit-pal 진단 리포트")
source_signal: .claude/kaizen-input/reflect-digest-2026-07-27.md (760 엔트리 중 307건·40% 가 훅 실패)
status: 미수정 — fit-pal 레포는 이번 카이젠 범위 밖. 이 문서는 리포트만.
---

# fit-pal 훅 실패 진단 — 근본원인 2종

30일 reflection 로그 760 엔트리 중 **351건이 훅/가드 실패**다. 단일 원인이 아니라 **독립된
근본원인 2종**이며, 하나만 고치면 나머지가 계속 로그를 오염시킨다.

이 문서는 **진단만** 한다. fit-pal 레포는 이번 카이젠 범위 밖이므로 아무 파일도 수정하지 않았다.

## 측정 근거

| 항목 | 값 | 측정 방법 |
|---|---|---|
| 훅/가드 실패 엔트리 | 351건 (전체의 40%) | reflections 로그 30일 집계 |
| 파편화된 `mistake_tag` | 54종 | 전부 "가드 훅이 없다"는 동일 의미 |
| cwd = `fit-pal` (루트) | 206건 | 로그 헤더 `- cwd:` 필드 |
| cwd = `fit-pal/app` | 117건 | 동일 |
| cwd = `fit-pal/server` | 28건 | 동일 |
| 마지막 발생 | **2026-07-27 (오늘)** | 미해결 상태 |

## 근본원인 A — 참조되는 스크립트 3종이 존재하지 않음

`.claude/settings.json` 이 선언한 9개 훅 중 **3개가 없는 파일을 가리킨다.**

| 훅 이벤트 | 참조 경로 | 상태 |
|---|---|---|
| SessionStart | `.claude/scripts/env-check.sh` | ❌ **없음** |
| PreToolUse (Bash) | `.claude/scripts/fvm-guard.sh` | ❌ **없음** |
| PreToolUse (Bash) | `.claude/scripts/flutter-run-guard.sh` | ❌ **없음** |
| SessionStart | `.claude/scripts/ui-mcp-session-context.sh` | ✅ 존재 (tracked, 755) |
| PreToolUse (Bash) | `.claude/scripts/ui-mcp-bash-guard.sh` | ✅ 존재 (tracked, 755) |
| PreToolUse (Write\|Edit\|MultiEdit) | `.claude/hooks/enforce-plugin-skill.sh` | ✅ 존재 (tracked, 755) |
| PreToolUse (Write\|Edit\|MultiEdit) | `.claude/hooks/enforce-shared-widget.sh` | ✅ 존재 (tracked, 755) |
| PostToolUse (`mcp__fitpal-mobile__.*`) | `.claude/scripts/ui-mcp-autorecover.sh` | ✅ 존재 (tracked, 755) |
| PostToolUseFailure (`mcp__fitpal-mobile__.*`) | `.claude/scripts/ui-mcp-autorecover.sh` | ✅ 존재 (tracked, 755) |

**3종은 git 이력이 아예 없다** — 삭제된 게 아니라 **한 번도 커밋된 적이 없다.**

```bash
git log --diff-filter=AD --follow -- .claude/scripts/env-check.sh   # 출력 없음
git cat-file -e HEAD:.claude/scripts/env-check.sh                   # 실패
```

`.gitignore` 는 `.claude/settings.local.json` 과 `.claude/scheduled_tasks.lock` 만 제외하므로
ignore 때문도 아니다. 즉 **설정만 먼저 들어가고 스크립트를 만들지 않은 상태**다.

관측된 실제 에러:

```text
bash: .claude/scripts/env-check.sh: No such file or directory
```

## 근본원인 B — 상대경로 훅이 서브디렉토리 cwd 에서 해석 실패 (더 큰 원인)

**9개 훅 전부 맨 상대경로를 쓰고, `${CLAUDE_PROJECT_DIR}` 사용은 0건이다.**

```json
{ "type": "command", "command": "bash .claude/scripts/ui-mcp-bash-guard.sh" }
```

Claude Code 공식 문서 (https://code.claude.com/docs/en/hooks):

> Handlers run in the current directory with Claude Code's environment.

> Use these placeholders to reference hook scripts relative to the project or plugin root,
> **regardless of the working directory when the hook runs**: `${CLAUDE_PROJECT_DIR}` — the project root.

fit-pal 은 모노레포라 세션이 `fit-pal/app` 이나 `fit-pal/server` 에서 시작되는 일이 흔하다.
그때 `.claude/scripts/...` 는 `fit-pal/app/.claude/scripts/...` 로 해석되어 **존재하는 스크립트조차
전부 실패**한다.

**전체 351건 중 145건 (41%) 이 서브디렉토리 cwd 에서 발생했다** (app 117 + server 28).
즉 근본원인 A(파일 3종 생성)만 고쳐도 **145건은 그대로 남는다.**

## 권고 조치 (fit-pal 세션에서 수행 — 이 카이젠은 손대지 않음)

우선순위 순.

1. **B 먼저 고쳐라 — 효과가 가장 크고 1파일 변경이다.**
   `.claude/settings.json` 의 9개 command 를 `${CLAUDE_PROJECT_DIR}` 기준으로 전환.
   공식 문서는 placeholder 사용 시 **exec form**(`command` + `args`)을 권고한다 — shell 토큰화가
   없어 공백/특수문자 경로에 안전하다. shell form 을 유지한다면 placeholder 를 **반드시 큰따옴표로
   감싸라.**

   ```json
   {
     "type": "command",
     "command": "${CLAUDE_PROJECT_DIR}/.claude/scripts/ui-mcp-bash-guard.sh",
     "args": []
   }
   ```

2. **A — 없는 스크립트 3종을 만들거나 훅 선언을 제거하라.** 둘 중 하나만 해도 로그 오염은 멈춘다.
   - 가드가 실제로 필요하면: `env-check.sh` / `fvm-guard.sh` / `flutter-run-guard.sh` 를 작성하고
     **`chmod +x` + git mode 100755 로 커밋**하라. (직전 카이젠 사이클이 mode 100644 로 인한
     permission-denied 957건을 잡은 이력이 있다 — 같은 함정 재발 주의.)
   - 필요 없으면: `.claude/settings.json` 에서 해당 3개 훅 엔트리를 삭제하라.
     **없는 스크립트를 가리키는 훅은 보호를 제공하지 않으면서 매 툴콜마다 실패한다.**

3. **검증** — 고친 뒤 `fit-pal`, `fit-pal/app`, `fit-pal/server` **세 디렉토리 각각에서** 세션을
   시작해 훅이 통과하는지 확인하라. 루트에서만 확인하면 근본원인 B 가 그대로 남는다.

## 남은 불확실성 (정직한 기록)

`ui-mcp-*` 스크립트는 2026-07-11 커밋 `aba11d4d` 로 추가·추적되고 있는데, 그 이후에도 cwd=루트에서
관련 태그가 13건 발생했다. 근본원인 B(서브디렉토리)로는 설명되지 않는 잔여분이다. 가능한 설명은
(a) 해당 커밋을 포함하지 않는 브랜치를 체크아웃한 세션 (b) reflection 분석기가 과거 컨텍스트를
반복 기술한 것 — 이번 조사로는 확정하지 못했다. 조치 1·2 를 적용한 뒤 재관측하면 구분된다.

## 이 신호가 카이젠에 남긴 것 (Phase 12 reflect-kit)

54종으로 파편화된 태그는 **reflect-kit Stop-hook 분석기의 결함**이기도 하다. 동일 사건(같은 파일
부재)이 `missing-claude-hook-scripts`(90) · `missing-bash-guard-hook`(23) ·
`missing-startup-env-check-script`(20) · `missing-hook-scripts`(15) … 로 쪼개져 **개별 빈도가
승격 임계치를 못 넘는다.** 진짜 행동 신호(API 문서 조회 스킵, 스코프 크립, 시각검증 우회)가
환경 오설정 반복 로깅에 묻힌다.

→ Phase 12 에서 (a) `mistake_tag` canonicalization (b) 환경 오설정의 반복 로깅 억제 (c) "없는 훅을
추가하라"는 meta-제안 억제를 다룬다.
