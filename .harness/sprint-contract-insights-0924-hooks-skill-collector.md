---
feature: "인사이트 2026-09-24 — 커밋 안전 훅 · dart 편집 파일 포맷 훅 · 화면 확인 스킬 · 카이젠 수집기 최신 인사이트 반영"
slug: insights-0924-hooks-skill-collector
created: "2026-09-24 13:45"
complexity: "복잡"
conditions: 36
status: done
owner_session: de8c7935-a5b6-4df5-9106-fafa73c288a0
conditions_digest: sha256:6c15402756476a09
locked_at: "2026-09-24 14:15"
---

## 배경

`/insights` 2026-09-24 산출물(`~/.claude/usage-data/report.html` · `facets/*.json` 18 세션 · `session-meta/`)이
제안한 훅 2 개 · 스킬 1 개 · 검토 에이전트 사용법을 킷에 들이고, 카이젠 수집기가 그 최신 산출물을 읽게 고친다.
킷별 나머지 제안은 이 스프린트 뒤의 전체 카이젠 입력(§0)으로 넘긴다. 넘긴 것은 처리 배정표(`.claude/kaizen-input/insights-report.md`)가 항목마다 추적한다(AR-06).

근거 세션(facets 앞 8 자리): 커밋 사고 9a0d4163(삭제 3217 개 기록) · d93c7e7a(남의 커밋 2 개 되돌림) ·
e19c3133(코드생성이 생성물 267 개 삭제) · 화면 의도 샘 00f4e982 · cfa1f76f · e163621c · ad969ac3 ·
hot restart 거짓 보고 e163621c · MCP 오진 a1412bc8 · 수집기 결함은 이번 세션에서 재현(아래 GAP 분석).

사용자 위임 기록: 세션 기록 `~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0.jsonl`
의 queued_command `2026-09-24T04:04:16.964Z` — 「자동으로 끝까지 알아서 진행해 내 허락이 필요한건 코덱스로 리서치나 검토받고」.
그래서 5 단계 사용자 승인은 Codex 검토로 대신한다. 검토 기록 경로는 이 문서 `## 범위 경계` 에 적는다.

## 리서치 소스

- Codex 사실 확인(2026-09-24, gpt-5.6-sol, 읽기 전용) — 세션 scratchpad `insights/codex-hooks-answer.md`:
  - PostToolUse 포매터 훅은 공식 hooks-guide 예시이며 연속 편집 거부 문제는 Claude Code v2.1.90 에서 고쳐졌다(#42317). 이 기계는 2.1.268
  - 편집 파일 경로는 stdin JSON 의 `tool_input.file_path` — `CLAUDE_FILE_PATHS` 는 공식 변수가 아니다(#23742 · #5489 상충)
  - PreToolUse 차단은 exit 2 + stderr 또는 `permissionDecision: deny`. PreToolUse 훅이 시간 초과로 끝나면 막지 않고 통과한다
  - 같은 명령 안의 `git add … && git commit` 은 PreToolUse 시점에 아직 스테이징 전이라 따로 계산해야 한다
- 빈틈 대조 워크플로(9 에이전트, 읽기 전용) — 세션 scratchpad `insights/gapmap.json`

## GAP 분석

- 커밋 사고 3 종을 막는 훅이 킷에도 사용자 전역에도 없다. 전역 `parallel-session-guard.sh` 는 올려 둔 목록만 보여 준다.
  `skill-design-guide.md` 등급 원장의 `Scope-Bound Edits` 행은 「Hard-stop 목록만 E3 (훅)」이라 적어 없는 훅을 있다고 말한다
- 인사이트 훅 예시 `dart format $CLAUDE_FILE_PATHS 2>/dev/null || true` 는 그대로 쓰면 변수가 비어 조용히 아무것도 안 한다.
  킷 `flutter-run` fix 단계와 `flutter-preflight` 1 단계는 `lib/` 통째 포맷을 권한다 — fit-pal 메모리
  `feedback_dart_format_shared_worktree` 가 금한 형태다
- `visual-evidence-protocol.md` 는 「완료를 선언하기 직전」에만 불린다(:11-13). 그래서 편집 전 기준 캡처가 구조적으로 불가능하다.
  flutter-widget 이 fit-pal 10 세션 중 8 세션에서 불렸는데 Visual Evidence Block 은 0 회 나왔다
- 수집기 재현(2026-09-24): `python3 scripts/collect-kaizen-data.py --skip-validate` stderr 가 `✓ 선택 .claude/kaizen-input/insights-report.md`
  (frontmatter `generated: 2026-08-13`) · `· 후순위 ~/.claude/usage-data/report.html`. 옛 요약본을 워크트리 생성 시각 때문에 `VERY FRESH (0.7h ago)` 로 표시했다.
  풀에 `2026-06-12 ~ 2026-08-12` 1 회, `2026-09-14 to 2026-09-23` 0 회, facets 0 건
- `contract-kaizen:37,105` · `evaluator-kaizen:38` · `harness-kaizen:51` 이 수집기를 거치지 않고 요약본을 직접 읽으라고 한다

## 범위 경계

- 계약 시각 출처: `created` 는 세션 기록에서 이 파일 본문을 처음 쓴 도구 결과 시각 `2026-09-24T04:45:17.820Z`(로컬 13:45), `locked_at` 은 봉인 명령의 `date` 출력이다. 경로 선점은 `04:40:46Z`
- 기준 커밋: `390dea8` (계약 작성 시점 origin/main). 가지: `feat/insights-0924-kaizen`
- 이 스프린트 상한 해석 (가지 관례가 `sprint/<slug>` 가 아니라서 이 프로젝트 형태로 적는다):

```bash
sprint_head() {  # 머지됐으면 머지 커밋, 아직이면 가지 tip. 실패하면 HEAD 로 떨어지지 않는다
  m=$(git log --merges --format=%H --grep="feat/insights-0924-kaizen" -1 origin/main 2>/dev/null)
  [ -n "$m" ] && { echo "$m"; return 0; }
  git rev-parse --verify -q feat/insights-0924-kaizen && return 0
  echo "UNRESOLVED feat/insights-0924-kaizen" >&2; return 1   # UNRESOLVED 는 AR-01 FAIL
}
```

- 화이트리스트(AR-01 이 참조하는 목록 — 이 목록을 바꾸면 개정 파일에 남긴다):
  `harness/scripts/commit-guard.sh` · `harness/hooks/hooks.json` · `harness/templates/settings-hooks.json` ·
  `harness/evals/hooks/commit-guard-test.sh` · `harness/docs/guides/skill-design-guide.md` · `harness/README.md` ·
  `harness/skills/contract-kaizen/SKILL.md` · `harness/skills/evaluator-kaizen/SKILL.md` · `harness/skills/harness-kaizen/SKILL.md` ·
  `flutter-toolkit/hooks/hooks.json` · `flutter-toolkit/scripts/format-edited-dart.sh` · `flutter-toolkit/evals/hooks/format-edited-dart-test.sh` ·
  `flutter-toolkit/skills/flutter-ui-verify/SKILL.md` · `flutter-toolkit/references/visual-evidence-protocol.md` ·
  `flutter-toolkit/references/project-detection.md` · `flutter-toolkit/skills/flutter-widget/SKILL.md` · `flutter-toolkit/skills/flutter-screen/SKILL.md` ·
  `flutter-toolkit/skills/flutter-skeleton/SKILL.md` · `flutter-toolkit/skills/flutter-transition/SKILL.md` · `flutter-toolkit/skills/flutter-responsive/SKILL.md` ·
  `flutter-toolkit/skills/flutter-kaizen/SKILL.md` · `flutter-toolkit/skills/flutter-run/SKILL.md` · `flutter-toolkit/skills/flutter-preflight/SKILL.md` ·
  `flutter-toolkit/evals/evals.json` · `flutter-toolkit/README.md` ·
  `scripts/collect-kaizen-data.py` · `scripts/validate-doc-contracts.py` · `scripts/test-collect-kaizen-data.py` ·
  `.claude/skills/kaizen-orchestrator/SKILL.md` · `.github/workflows/ci.yml` · `README.md` · `CLAUDE.md` ·
  `.claude/kaizen-input/insights-report.md` · `scripts/check-insights-tracking.py`
  (34 경로. `.harness/` 는 제외 — 계약·피드백·개정 파일은 SEAL 검사로 따로 잰다)
- 기준값 실측(390dea8, 계약 작성 시점): `validate-plugin.py` 14 OK exit 0 · `sync-evals.py --check-only` exit 0 ·
  `sync-docs.py --check-only` exit 0 · `sync-orchestrator.py --check-only` exit 0 · `run-evals.py` 106 passed exit 0 ·
  `validate-doc-contracts.py -v` 1 블록 violation 0 exit 0 · `check-stale-values.py` exit 0 · `check-docs-links.py` exit 0 ·
  `validate-post-kaizen.py` 12 PASS 0 FAIL
- 범위 밖: 킷별 나머지 인사이트 제안(qa-evaluator 조용한 실패 확인 목록 · design-kit · bambu-kit · planning/backend/rust/infra ·
  reflect-kit · tone-kit · react/api/onboarding/howto · flutter `--build-filter` 방향)은 전체 카이젠 §0 으로 넘긴다
- 오라클 해소: SK-03 — 산출물이 모델이 읽고 따르는 절차 문서라 구간 안 문장 존재가 산출물 자체다. 행동은 SK-06 평가 사례와 QA 단계의 실제 돌려보기로 따로 잰다
- 오라클 해소: SK-05 — 짝 맞춤 표 행 자체가 산출물이다(다음 카이젠이 읽는 대조 기준). 행동 효과는 이 스프린트에서 잴 수 없다
- 오라클 해소: AR-05 — 문서 속 권고 명령의 형태가 산출물이다. 양성 대조로 옛 판에서 측정이 1 이상임을 확인한다
- 오라클 해소: AP-01 · DG-03 — 안티패턴 grep 은 project.yaml 이 정한 검사 형태이고 DG-03 은 N/A 줄이다
- 측정 코드 5 종 — 조건이 `# oracle: <이름>` 으로 가리킨다. 평가자는 아래 블록을 원문 그대로 뽑아 실행한다 (`awk '/^# oracle: <이름>$/{f=1} f&&/^```$/{exit} f' <계약>` → 파일). 계약 작성 시 전부 실행해 확인했다 (trigger_overlap: 새 스킬 전 MISSING exit 1 · 겹치는 낱말 사본 substring=1 exit 1 · 안 겹치는 사본 exit 0 / facets_count: sessions=18 / report_period: newest report-2026-09-24-095238.html · 2026-09-14 2026-09-23 / skill_count_lines: 18=18 exit 0 / tracking_check: 390dea8 판 요약본 exit 1 · P10 만 있는 표에서 P1 미배정 검출 · trigger_overlap: 에이전트 폴더를 뺀 사본에서 OTHER_FILES_MISMATCH exit 1)

```python
# oracle: trigger_overlap
# 새 스킬 description 의 따옴표 구절이 flutter-toolkit 다른 스킬·에이전트 구절과 겹치는지 센다
import re, glob, sys, os
ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
NEW = 'flutter-ui-verify'
def phrases(path):
    text = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---', text, re.S)
    fm = m.group(1) if m else ''
    d = re.search(r'^description:(.*?)(?=^[A-Za-z_-]+:|\Z)', fm, re.S | re.M)
    desc = d.group(1) if d else ''
    return {p.strip().lower() for p in re.findall(r'"([^"]+)"', desc) if p.strip()}
files = sorted(glob.glob(os.path.join(ROOT, 'flutter-toolkit/skills/*/SKILL.md'))) + \
        sorted(glob.glob(os.path.join(ROOT, 'flutter-toolkit/agents/*.md')))
new = [f for f in files if f'/skills/{NEW}/' in f]
if not new:
    print('MISSING', NEW); sys.exit(1)
mine = phrases(new[0])
if not mine:
    print('NO_PHRASES', new[0]); sys.exit(1)
exact, sub = [], []
for f in files:
    if f == new[0]:
        continue
    for q in phrases(f):
        for p in mine:
            if p == q: exact.append((p, f))
            elif p in q or q in p: sub.append((p, q, f))
others = len(files) - 1
print(f'new_phrases={len(mine)} other_files={others} exact={len(exact)} substring={len(sub)}')
if others != 19:  # 다른 스킬 18 + 에이전트 1. 파일이 빠지면 비교가 조용히 줄어든다
    print('OTHER_FILES_MISMATCH', others); sys.exit(1)
for x in exact + sub: print('  ', x)
sys.exit(0 if not exact and not sub else 1)
```

```python
# oracle: facets_count
# 구현과 무관하게 facets 원본을 직접 세어 기대값을 낸다 (평가 시점 기준)
import json, glob, os, collections, sys
U = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else '~/.claude/usage-data')
groups, fr, n, bad = collections.Counter(), collections.Counter(), 0, 0
for f in sorted(glob.glob(os.path.join(U, 'facets', '*.json'))):
    try:
        d = json.load(open(f, encoding='utf-8'))
        m = json.load(open(os.path.join(U, 'session-meta', os.path.basename(f)), encoding='utf-8'))
    except Exception:
        bad += 1; continue
    n += 1
    p = m.get('project_path', '')
    g = 'temp' if p.startswith(('/private/tmp', '/tmp', '/var/folders')) else \
        'fit-pal' if '/fit-pal' in p else 'claude-plugins' if '/claude-plugins' in p else 'other'
    groups[g] += 1
    for k, v in (d.get('friction_counts') or {}).items(): fr[k] += v
print(f'sessions={n} unreadable={bad}')
print('groups', dict(sorted(groups.items())))
print('top3', fr.most_common(3))
```

```python
# oracle: report_period
# 가장 새 report-*.html 이름과 report.html 본문의 관측 기간을 낸다
import glob, os, re, sys
U = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else '~/.claude/usage-data')
reps = sorted(glob.glob(os.path.join(U, 'report-*.html')))
newest = os.path.basename(reps[-1]) if reps else ''
text = open(os.path.join(U, 'report.html'), encoding='utf-8').read()
m = re.search(r'(\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2})', text)
print('newest', newest)
print('period', m.group(1) if m else '', m.group(2) if m else '')
```

```python
# oracle: skill_count_lines
# README.md·CLAUDE.md 에서 flutter-toolkit 스킬 개수를 말하는 4 줄이 실제 스킬 폴더 수와 같은지 본다
import re, os, sys
n = len([d for d in os.listdir('flutter-toolkit/skills') if os.path.isdir(os.path.join('flutter-toolkit/skills', d))])
pats = [('CLAUDE.md', r'^- \*\*flutter-toolkit\*\* — Flutter 전용 개발 워크플로우 스킬 (\d+)종'),
        ('CLAUDE.md', r'^\*\*flutter-toolkit — Flutter 개발 워크플로우 \((\d+)종\)\*\*'),
        ('README.md', r'^Flutter 프로젝트 전용 개발 워크플로우 스킬 (\d+)종'),
        ('README.md', r'skills/ +# 개발 워크플로우 스킬 (\d+)종')]
ok = True
def lines_of(f, p):
    ls = open(f, encoding='utf-8').read().splitlines()
    if p.startswith('skills/'):  # 폴더 그림은 킷마다 같은 모양이라 flutter-toolkit 블록 다음 3 줄로 좁힌다
        i = next((k for k, l in enumerate(ls) if '── flutter-toolkit/' in l), None)
        ls = ls[i + 1:i + 4] if i is not None else []
    return ls
for f, p in pats:
    hits = [m.group(1) for m in (re.search(p, l) for l in lines_of(f, p)) if m]
    good = len(hits) == 1 and int(hits[0]) == n
    ok &= good
    print(f'{f} {p[:40]}… hits={hits} dirs={n} {"OK" if good else "FAIL"}')
sys.exit(0 if ok else 1)
```

```python
# oracle: tracking_check
# 카이젠 §0 입력 파일이 인사이트 항목 F01~F32 와 빈틈 대조 제안 전부에 처리 배정을 달았는지 본다
import re, sys
path, keys_path, newest = sys.argv[1], sys.argv[2], sys.argv[3]
text = open(path, encoding='utf-8').read()
m = re.match(r'^---\n(.*?)\n---', text, re.S)
fm = m.group(1) if m else ''
ok = True
if not re.search(r'^generated:\s*2026-09-24\s*$', fm, re.M): print('FM generated 불일치'); ok = False
if not re.search(r'^report_file:\s*\S*' + re.escape(newest) + r'\s*$', fm, re.M): print('FM report_file 불일치'); ok = False
rows = [l for l in text.splitlines() if l.startswith('|')]
if not any('대상 계약' in l and 'QA' in l for l in rows): print('표 머리에 대상 계약 · QA 열 없음'); ok = False
DISP = re.compile(r'이번 스프린트|Phase\s*\d+|기각|해당 없음')
def rows_for(key):  # 키가 다른 키의 앞부분으로 잡히지 않게 경계를 둔다 (P1 과 P10)
    pat = re.compile(r'(?<![\w:-])' + re.escape(key) + r'(?![\w-])')
    return [l for l in rows if pat.search(l)]
for i in range(1, 33):
    fid = f'F{i:02d}'
    if not any(DISP.search(l) for l in rows_for(fid)): print('F 배정 없음', fid); ok = False
keys = [x.strip() for x in open(keys_path, encoding='utf-8') if x.strip()]
if len(keys) != 64 or len(set(keys)) != len(keys):  # 키 파일이 줄거나 겹치면 검사가 조용히 줄어든다
    print('KEYS_MISMATCH', len(keys), len(set(keys))); ok = False
for k in keys:
    if not any(DISP.search(l) for l in rows_for(k)): print('제안 배정 없음', k); ok = False
FORCED = {'harness:P04': r'Phase\s*3\b', 'insights:scope-commit-block': r'Phase\s*4\b', 'F31': r'Phase\s*3\b'}
for k, want in FORCED.items():
    if not any(re.search(want, l) for l in rows_for(k)): print('지정 배정 어긋남', k, want); ok = False
print('TRACKING_OK' if ok else 'TRACKING_FAIL'); sys.exit(0 if ok else 1)
```

- 커밋 안전 훅 삭제 기준은 인사이트 원문(`deletes more than 50 files`)대로 50 초과다. SC-01 ① 51 개 · SC-02 ⑦ 50 개가 경계값이다
- Codex 검토 1 회차(`insights/codex-contract-review.md`, VERDICT: CHANGES)와 교차 진단 1 회차 지적을 반영해 조건을 다시 썼다. 반영: 처리 배정표(AR-06) · SK-02 파서 고정 · SK-03 측정 확장 · SK-04 위치 · SK-06 두 사례 · SC-04 Write·공백 경로 · SC-05 generated 분기 · SC-06/07 평가 시점 대조 · SC-08 인자·KNOWN_KEYS 짝 · ER-01 검사 못 함 알림 · AR-01 UNRESOLVED=FAIL · AR-04 네 줄 고정 · DG-04 미검증 판정. 반영 안 함: Task Agents(독립 검토 확인 목록)는 qa-evaluator 소관이라 카이젠 Phase 3 로 배정해 AR-06 이 추적한다 · 선언 범위 밖 파일 커밋 차단은 범위를 기계가 읽을 선언이 킷에 없어 카이젠 Phase 4 로 배정한다
- Codex 2 회차(`insights/codex-contract-review-2.md`, VERDICT: CHANGES) 반영: 처리 배정표 키 경계 비교 · 지정 배정 3 건 강제 · 표에 대상 계약·QA 열 · Final 이 배정표를 닫는 SK-09 · SK-03 21 낱말 · SK-04 편집 전 구간 · SC-04 Write 인자 · AR-01 `end_sha` 고정 · trigger_overlap 비교 대상 19 개 확인
- Codex 3 회차(`insights/codex-contract-review-3.md`, VERDICT: CHANGES) 반영: SK-03 낱말 수 정정과 `2 개 이상` 추가 · SK-09 를 실제 검사 스크립트(`scripts/check-insights-tracking.py --final`) 동작으로 바꿈 · AR-01 `end_sha` 필수
- Codex 검토(사용자 승인 대신): 세션 scratchpad `insights/codex-contract-review.md` · `-2.md` · `-3.md` · `-4.md` · `-5.md` · `-6.md` — 마지막 회차 VERDICT 를 봉인 전에 확인한다
- Codex 5 회차(VERDICT: CHANGES) 반영: SK-06 사례 B 의 한 assertion 에 경로 수 규칙과 경로 1 개 실패를 함께 못 박음
- Codex 4 회차(VERDICT: CHANGES) 반영: SK-03 에 `관례 표`·`2 개 이상` 같은 줄 요구 · SK-06 사례 B 에 `2 개 이상` 채점 · tracking_check 키 64 줄·중복 0 확인

## Skill

- [ ] SK-01: flutter-toolkit 에 사용자가 부를 수 있는 화면 확인 스킬 `flutter-ui-verify` 가 있고, 절차는 `references/visual-evidence-protocol.md` 의 단계를 번호로 전부 가리키며 규약 문장을 옮겨 적지 않는다 [exact] (측정: `python3 scripts/validate-plugin.py flutter-toolkit` exit 0 · `test -f flutter-toolkit/skills/flutter-ui-verify/SKILL.md` · 첫 frontmatter 블록에 `name: flutter-ui-verify` 와 `user-invocable: true` 각 1 회 · 본문에 `visual-evidence-protocol.md` · `Step 0` · `Step 1` · `Step 2` · `Step 3` · `Step 4` · `Visual Evidence Block` 각 1 회 이상 · 복제 검사 — 규약 파일에서 공백을 뺀 길이 25 자 이상인 줄 중 스킬 파일 본문에 글자 그대로 들어 있는 줄 수 = 0, python3 로 잰다)
- [ ] SK-02: 새 스킬 description 의 따옴표 구절이 flutter-toolkit 다른 스킬 18 개와 에이전트 1 개의 따옴표 구절과 완전 일치 0 쌍 · 부분 문자열 포함 0 쌍이다 [exact, enumerated] (측정: `## 범위 경계` 의 `# oracle: trigger_overlap` 블록을 원문 그대로 뽑아 레포 루트에서 `python3 <뽑은 파일> .` 실행 — exit 0 이고 출력 `other_files=19 exact=0 substring=0`(비교 대상이 19 개가 아니면 exit 1). 양성 대조: 계약 작성 시 임시 사본에 `"UI 컴포넌트 확인"` 을 넣으면 `substring=1` · exit 1 이었다)
- [ ] SK-03: `visual-evidence-protocol.md` 가 인사이트 다섯 가지를 담는다 [structural, enumerated] — (a) 머리말이 편집 전과 완료 직전 두 번 실행을 말한다 (b) Step 0 에 요청 되말하기 · 진입점이 아닌 화면 자체 · 기존 화면 2 개 이상 경로를 든 관례 표 (c) Step 2 에 재캡처 전 반영 확인 — 바뀌어야 할 표식으로 판정하고 재시작 성공 줄만으로 판정하지 않으며 확인 실패 시 앱을 다시 띄운다 (d) Step 3 에 캡처 점검 목록 — 글자 넘침 · 깨진 글리프 · 칩·뱃지와 카드·평평한 줄 관례 · 디버그 겹침, 넘침은 글자 크기를 키워 재현 (e) Step 4 에 고장이라 말하기 전 확인 — 인자 이름 대조 · 붙은 앱이 내가 띄운 앱인지 · 따로 뜨는 층의 위젯 (측정: awk `index($0,a)==1` 로 `## Step 0`~`## Step 1`, `## Step 2`~`## Step 3`, `## Step 3`~`## Step 4`, `## Step 4`~`## Visual Evidence Block` 구간만 잘라 구간 안 grep — (b) `되말` · `관례 표` · `진입점` · `기존 화면` · `2 개 이상` (c) `반영 확인` · `표식` · `성공 줄` · `다시 띄` (d) `넘침` · `글리프` · `칩` · `뱃지` · `카드` · `평평한 줄` · `디버그` · `글자 크기` (e) `인자` · `내가 띄운` · `따로 뜨는`, 머리말(첫 `## ` 줄 앞) `편집 전과 완료 직전` — 모두 21 낱말(b 5 · c 4 · d 8 · e 3 · 머리말 1) 각 1 회 이상, 그리고 Step 0 구간에 `관례 표` 와 `2 개 이상` 이 같은 줄에 있는 줄 1 개 이상 — 규약은 킷 문서라 실제 앱 경로를 담을 수 없으므로 경로 수 요구를 적은 문장을 잰다. 실제 경로 수는 SK-06 사례 B 가 채점한다. 음성 대조: 390dea8 판에서 같은 명령으로 21 낱말 모두 0 — 계약 작성 시 실측)
- [ ] SK-04: UI 를 고치는 flutter-toolkit 스킬 5 개가 규약을 편집 전에도 부른다 [exact, enumerated] (측정: awk `index($0,a)==1` 로 편집 전 구간만 잘라 그 안에 `기준 캡처는 편집 전에` 와 `Step 0` 이 같은 줄에 있는 줄이 1 개 이상 — `flutter-toolkit/skills/flutter-widget/SKILL.md` 는 `### 2. 기존 패턴 분석`~`### 3.` · `flutter-toolkit/skills/flutter-screen/SKILL.md` 는 `### 2. 기존 패턴 분석`~`### 3.` · `flutter-toolkit/skills/flutter-skeleton/SKILL.md` · `flutter-toolkit/skills/flutter-transition/SKILL.md` · `flutter-toolkit/skills/flutter-responsive/SKILL.md` 는 `## Gotchas`~`## 0.` — 5 개 모두. 구간 머리는 390dea8 판 기준 87 · 47 · 14 · 14 · 13 행. 음성 대조: 390dea8 판 5 파일에서 `기준 캡처는 편집 전에` 가 0 회 — 계약 작성 시 실측)
- [ ] SK-05: flutter-kaizen 의 짝 맞춤 표에서 visual-evidence 규약 행이 편집 전 호출까지 대조하게 바뀌었다 [exact] (측정: `grep -n 'visual-evidence' flutter-toolkit/skills/flutter-kaizen/SKILL.md` 가 내는 행 중 `편집 전` 을 포함하는 행 1 개 이상. 음성 대조: 390dea8 판 :45 행에는 `편집 전` 이 없다)
- [ ] SK-06: flutter-toolkit evals 에 서로 다른 새 사례 2 개가 있다 — 사례 A: skill 이 `flutter-ui-verify`. 사례 B: skill 이 `flutter-widget` 이고 assertions 가 편집 전 순서를 채점한다 [exact, enumerated] (측정: python3 로 `flutter-toolkit/evals/evals.json` 을 읽어 — skill `flutter-ui-verify` 사례 1 개 이상, skill `flutter-widget` 이면서 assertions 문자열 합에 `되말` · `관례 표` · `기준 캡처` · `반영 확인` · `점검 목록` · `재캡처` · `2 개 이상` 7 낱말이 모두 있는 사례 1 개 이상 — 그 사례에 `서로 다른 기존 화면 경로` · `2 개 이상` · `1 개면 FAIL` 을 한 assertion text 안에 모두 담은 항목이 1 개 이상(경로 수 판정 규칙과 경로 1 개일 때의 실패를 채점 기준에 못 박는다. `run-evals.py` 는 사례 구조만 검사하고(`scripts/run-evals.py:5-8`) 실행 결과가 없으므로 계약 단계에서 셀 수 있는 것은 채점 기준 문장이다), 두 사례의 id 가 다르다, 전체 id 중복 0 · `python3 scripts/sync-evals.py --check-only` exit 0 · `python3 scripts/run-evals.py` exit 0)
- [ ] SK-07: harness 카이젠 스킬 3 개가 요약본을 직접 읽지 않고 데이터 풀 §0 을 읽는다 [exact, enumerated] (측정: `harness/skills/contract-kaizen/SKILL.md` · `harness/skills/evaluator-kaizen/SKILL.md` · `harness/skills/harness-kaizen/SKILL.md` 각 파일 `grep -c 'kaizen-input/insights-report.md'` = 0 이고 `grep -c 'kaizen-data-pool'` ≥ 1. 양성 대조: 390dea8 판 3 파일의 첫 grep 이 2 · 1 · 1 — 계약 작성 시 실측)
- [ ] SK-08: 오케스트레이터 Step 0 이 새 선택 규칙과 facets 입력을 선언한다 [structural, enumerated] (측정: awk 로 `.claude/skills/kaizen-orchestrator/SKILL.md` 의 `### Step 0:` ~ `### Step 0.5:` 구간만 잘라 — `# docs-contract` 블록 안 `--usage-data` 1 회 · `usage_data_inputs` 1 회 · 구간 안 `우선순위대로` 0 회 · `report_file` 1 회 이상 · `0-b` 1 회 이상 · 그리고 SC-08 을 만족한 상태에서 `python3 scripts/validate-doc-contracts.py -v` exit 0. 양성 대조: 390dea8 판 구간 안 `우선순위대로` 1 회 — 계약 작성 시 실측)
- [ ] SK-09: 전체 카이젠이 처리 배정표를 닫는다 — 레포 검사 스크립트 `scripts/check-insights-tracking.py` 가 `--final` 일 때 `Phase N` 행의 `대상 계약` 칸(계약 슬러그)과 `QA` 칸(`APPROVE` 또는 `REJECT`)이 하나라도 비면 exit 1 이고, 오케스트레이터 Final 단계가 그 명령을 부른다 [goal] (측정: (a) `python3 scripts/check-insights-tracking.py --final .claude/kaizen-input/insights-report.md` 가 지금 판(Phase 행의 두 칸이 빈 상태)에서 exit 1 (b) 그 파일 사본에서 모든 `Phase N` 행의 두 칸을 채운 사본은 exit 0 (c) (b) 사본에서 한 행의 `QA` 칸만 비우면 exit 1 (d) `--final` 없이 지금 판은 exit 0 (e) awk 로 `.claude/skills/kaizen-orchestrator/SKILL.md` 의 `### Step F1:` ~ `### Step F2` 구간에 `python3 scripts/check-insights-tracking.py --final` 1 회 이상. 음성 대조: 390dea8 판에는 스크립트가 없고 같은 구간에 `insights-report.md` 0 회 — 계약 작성 시 실측)

## Script

- [ ] SC-01: 커밋 안전 훅이 임시 저장소에서 사고 형태를 막는다. Given: `bash harness/evals/hooks/commit-guard-test.sh` 가 임시 저장소를 만들고 `commit-guard.sh pre` 에 Claude Code PreToolUse 입력 JSON(`tool_input.command` · `cwd`)을 준다. When: ① 파일 51 개를 `git rm` 한 뒤 `git commit -m x` ② 파일 60 개를 작업 폴더에서만 지운 채 `git add -A && git commit -m x` ③ 다른 커밋이 HEAD 를 앞으로 옮겼는데 공용 목록은 옛 내용을 쥔 상태 — 예: `git update-index --cacheinfo 100644,<옛 blob>,f2` 로 공용 목록만 옛 내용으로 바꾸고 작업 폴더의 f2 는 HEAD 와 같게 둔 채 `git commit -m x` ④ `GIT_INDEX_FILE=<없는 경로> git add a.txt && GIT_INDEX_FILE=<같은 경로> git commit -m x`(같은 명령 안에 `git read-tree` 없음) ⑤ 저장소 경로에 공백이 든 폴더에서 ① 과 같은 커밋. Then: 다섯 경우 모두 exit 2 이고 stderr 에 막은 이유가 있다 [goal] (측정: 시험 스크립트가 경우마다 `기대 exit / 실제 exit` 한 줄을 찍고 전부 맞으면 exit 0. 음성 대조: `commit-guard.sh` 사본에서 삭제 수 판정 줄을 지우고 같은 시험을 돌리면 ①② 가 exit 0 으로 바뀌어 시험 스크립트 exit 1)
- [ ] SC-02: 커밋 안전 훅이 정상 커밋을 막지 않는다. Given: 같은 시험 스크립트. When: ⑥ 평범한 1 파일 커밋 ⑦ 삭제 정확히 50 개(경계값 — 기준은 인사이트 원문대로 50 초과) ⑧ `git mv` 60 개 ⑨ 60 개 삭제에 명령 앞 `HARNESS_COMMIT_GUARD=off` ⑩ 60 개 삭제에 `env HARNESS_COMMIT_GUARD=off git commit` ⑪ 커밋이 아닌 명령(`git status`) ⑫ heredoc 본문에만 `git commit` 글자가 있는 `cat <<EOF` 명령 ⑬ 60 개 삭제가 스테이징돼 있어도 `git commit -o a.txt` ⑭ 같은 상태에서 `git commit -m x -- a.txt`. Then: 모두 exit 0 이고 stdout 이 비어 있다 [goal] (측정: 시험 스크립트 출력의 ⑥~⑭ 줄 · 스크립트 exit 0)
- [ ] SC-03: 커밋 직후 훅이 방금 커밋의 삭제 50 개 초과를 알린다. Given: 임시 저장소에서 60 개를 지운 커밋을 막 만든 상태. When: `commit-guard.sh post` 에 그 커밋 명령의 PostToolUse 입력 JSON 을 준다. Then: stdout 이 `hookSpecificOutput.additionalContext` 를 가진 JSON 이고 그 문자열에 `60` 과 `git reset --soft HEAD~1` 이 있다. 삭제 1 개 커밋에서는 stdout 이 비어 있다 [goal] (측정: 시험 스크립트 ⑮ ⑯ 줄 — ⑮ 는 `jq -e '.hookSpecificOutput.additionalContext | test("60")'` exit 0)
- [ ] SC-04: 포맷 훅이 편집한 .dart 파일 하나에만 포맷을 부른다. Given: `bash flutter-toolkit/evals/hooks/format-edited-dart-test.sh` 가 받은 인자를 파일에 적는 가짜 `fvm`·`dart` 실행 파일을 PATH 앞에 두고 임시 플러터 프로젝트(`pubspec.yaml` 있음)를 만든다. When/Then: ① `tool_name: Edit` · `lib/a.dart` → 기록 1 줄 · 인자가 `dart format` 과 그 파일 절대경로 하나 ② `tool_name: Write` · `lib/b.dart` → 기록 1 줄 · 인자가 `dart format` 과 `lib/b.dart` 의 절대경로 하나 ③ 공백이 든 경로 `lib/my file.dart` → 기록 1 줄 · 경로가 쪼개지지 않고 한 인자 ④ 프로젝트에 `.fvmrc` 가 있으면 `fvm dart format <그 파일>` ⑤ `lib/a.g.dart` · `lib/a.freezed.dart` → 기록 0 ⑥ `README.md` → 기록 0 ⑦ `pubspec.yaml` 이 조상에 없는 폴더의 .dart → 기록 0 ⑧ `FLUTTER_TOOLKIT_FORMAT_ON_EDIT=off` → 기록 0 [goal] (측정: 시험 스크립트가 경우마다 `기대 / 실제` 를 찍고 전부 맞으면 exit 0. 음성 대조: 훅 사본에서 생성물 제외 줄을 지우면 ⑤ 가 기록 1 이 되어 시험 exit 1)
- [ ] SC-05: 수집기가 인사이트 입력을 '어느 보고서를 요약했는가' 로 고른다. Given: `python3 scripts/test-collect-kaizen-data.py` 가 임시 폴더에 가짜 `usage-data`(report-*.html 2 개 + report.html) 와 요약본을 만든다. When/Then: ① 요약본 frontmatter `report_file` 이 가장 새 `report-*.html` 이름과 같으면 요약본 선택 ② 옛 보고서 이름을 가리키면 원본 `report.html` 선택하고 진 이유를 stderr 한 줄로 찍는다 ③ `report_file` 없이 `generated` 가 가장 새 보고서 날짜와 같거나 늦으면 요약본 선택 ④ `generated` 가 더 이르면 원본 선택 ⑤ frontmatter 가 없으면 원본 선택 ⑥ `--insights <없는 경로>` 면 exit 2 ⑦ 요약본 나이는 파일 수정 시각이 아니라 `generated` 날짜로 잰다(파일 수정 시각을 지금으로 바꿔도 나이가 그대로) [goal] (측정: 시험 스크립트가 경우마다 결과 줄을 찍고 전부 맞으면 exit 0. 음성 대조: 선택 함수 사본을 옛 고정 순서로 되돌리면 ② ④ 가 실패해 exit 1)
- [ ] SC-06: 이 맥의 실제 수집 결과가 가장 새 인사이트를 싣는다 [exact] (Given: 이 워크트리. 측정: `O=$(mktemp -d)` 후 `python3 scripts/collect-kaizen-data.py --skip-validate --output "$O/pool.md" 2>"$O/err.txt"` · `## 범위 경계` 의 `# oracle: report_period` 블록을 뽑아 실행한 `newest` 와 `period` 두 날짜를 기대값으로 쓴다 — (a) `err.txt` 의 `✓ 선택` 줄이 `usage-data/report.html` 이거나, `.md` 이면 그 파일 frontmatter `report_file` 이 `newest` 와 같다 (b) `pool.md` 의 `## 0.` ~ `## 0.5` 구간에 period 두 날짜가 각각 1 회 이상 (c) `pool.md` 에 `2026-06-12 ~ 2026-08-12` 0 회. 양성 대조: 계약 작성 시 같은 명령의 결과 `insights/pool-before.md` 는 (c) 가 1 회였다)
- [ ] SC-07: 데이터 풀 §0 안에 세션별 분석 절 `### 0-b` 가 있고 원본을 따로 센 값과 맞는다 [exact] (측정: SC-06 의 `pool.md` 에서 제목 줄 번호가 `## 0.` < `### 0-b` < `## 0.5` · `## 범위 경계` 의 `# oracle: facets_count` 블록을 뽑아 평가 시점에 실행한 `sessions` · 프로젝트 묶음 수(`fit-pal` · `claude-plugins` · 임시 폴더) · 상위 마찰 3 종 합계가 `### 0-b` 절에 같은 숫자로 있다 — 고정값이 아니라 평가 시점 원본과 대조한다. 계약 작성 시 실측: sessions=18 · fit-pal 10 · claude-plugins 6 · temp 2 · buggy_code 28 · wrong_approach 20 · misunderstood_request 14)
- [ ] SC-08: 수집기와 문서 선언 검사기가 facets 입력을 짝으로 갖는다 [exact, enumerated] (측정: `python3 scripts/collect-kaizen-data.py --help` 출력에 `--usage-data` · `scripts/validate-doc-contracts.py` 의 `KNOWN_KEYS` 에 `usage_data_inputs` · 비교 반복문이 `usage_data_inputs` 값도 스크립트 선언과 대조 · 지금 판에서 `python3 scripts/validate-doc-contracts.py -v` exit 0. 음성 대조 ①: 오케스트레이터 SKILL.md 사본의 docs-contract 블록에서 `usage_data_inputs` 줄을 지우고 그 사본을 검사하면 exit 1 ②: 그 줄의 값 경로 하나를 틀리게 바꾼 사본도 exit 1 — 사본으로 재고 원본은 건드리지 않는다)
- [ ] SC-09: 새 셸·파이썬 파일이 문법 검사를 통과하고 새 시험 3 개가 CI 실행 목록에 들어 있다 [exact, enumerated] (측정: `bash -n harness/scripts/commit-guard.sh` · `bash -n harness/evals/hooks/commit-guard-test.sh` · `bash -n flutter-toolkit/scripts/format-edited-dart.sh` · `bash -n flutter-toolkit/evals/hooks/format-edited-dart-test.sh` 각 exit 0 · `shellcheck -S warning` 네 파일 경고 0 · `python3 -m py_compile scripts/collect-kaizen-data.py scripts/validate-doc-contracts.py scripts/test-collect-kaizen-data.py scripts/check-insights-tracking.py` exit 0 · `.github/workflows/ci.yml` 의 `run:` 줄에 `commit-guard-test.sh` · `format-edited-dart-test.sh` · `test-collect-kaizen-data.py` 각 1 회 이상 · 그 세 `run:` 명령을 원문 그대로 로컬에서 돌려 각 exit 0)

## Error

- [ ] ER-01: 두 훅이 깨진 입력에서 멈추지 않고, 커밋 안전 훅은 검사를 못 했을 때 그 사실을 알린다 [exact, enumerated] (측정: jq 가 없는 PATH 는 필요한 도구만 링크한 임시 bin 폴더로 만든다 — `PATH=/usr/bin:/bin` 은 이 맥에서 `/usr/bin/jq` 가 있어 가려지지 않는다, 계약 작성 시 실측: 링크 폴더 PATH 에서 `command -v jq` exit 1. 경우: `harness/scripts/commit-guard.sh pre` 에 (a) 빈 stdin → exit 0 · stdout 빈 값 (b) `{깨진` → exit 0 · stdout 빈 값 (c) jq 없는 PATH + `git commit` 이 든 입력 → exit 0 · stdout 이 `additionalContext` 를 가진 JSON 이고 그 안에 `jq` 와 `검사` (d) jq 없는 PATH + `git status` 입력 → exit 0 · stdout 빈 값. `harness/scripts/commit-guard.sh post` 와 `flutter-toolkit/scripts/format-edited-dart.sh` 에 (a)(b)(c) → 모두 exit 0 · stdout 빈 값. 총 10 경우, 두 시험 스크립트 안에서 잰다)
- [ ] ER-02: 커밋 안전 훅이 막을 때 사용자가 판단할 재료와 우회 방법을 준다 [exact] (측정: SC-01 ① 의 stderr 에 삭제 수 `51` · 상위 폴더 이름 1 개 이상 · `HARNESS_COMMIT_GUARD=off` · `승인` 이 모두 있고, 파일 이름 전체 목록을 뿌리지 않는다 — stderr 줄 수 ≤ 15)
- [ ] ER-03: 수집기가 facets 를 못 읽은 것을 조용히 넘기지 않는다 [goal] (측정: `scripts/test-collect-kaizen-data.py` 안에서 facets 3 개(본 레포 · 같은 레포 워크트리 · `/private/tmp` 경로) + 깨진 facets 1 개 + 평가 세션 session-meta 1 개 fixture 로 돌려 세션 3 · 프로젝트 묶음 1 · 임시 1 · 못 읽은 파일 1 이 stderr 와 풀 양쪽에 찍히고, facets 폴더가 없는 fixture 에서는 exit 0 과 `(없음)` 이 찍힌다)

## Architecture

- [ ] AR-01: 변경이 화이트리스트 34 경로 안에 있다 [exact, enumerated] (Given: 이 스프린트 커밋이 끝난 뒤 · 상한: 구현자가 구현 마지막 커밋 직후 `.harness/sprint-amendments-insights-0924-hooks-skill-collector.md` 에 적은 `end_sha:` 값(고정 SHA) — 그 줄이 없으면 이 조건은 FAIL 이다 · 측정: `git diff --name-only 390dea8..<상한> -- . ':(exclude).harness'` 의 각 줄이 화이트리스트 34 경로 중 하나 — 포함 관계. `end_sha` 가 `sprint_head` 가 가리키는 커밋의 조상(또는 같은 커밋)인지 `git merge-base --is-ancestor` 로 확인한다 — 아니거나 `UNRESOLVED` 면 FAIL. `.harness/` 는 `find .harness -type f -name 'sprint-contract*.md'` 에 `verify_seal` 을 돌려 `SEAL_BROKEN` 0 개로 잰다)
- [ ] AR-02: 두 훅이 킷 훅 파일에 등록되고 실행 비트가 있다 [exact, enumerated] (측정: `jq` 로 `harness/hooks/hooks.json` 의 `PreToolUse` 와 `PostToolUse` 에 `commit-guard.sh` 를 부르는 command 가 각 1 개 · `harness/templates/settings-hooks.json` 에도 같은 두 등록 · `flutter-toolkit/hooks/hooks.json` 의 `PostToolUse` 에 `format-edited-dart.sh` 1 개이고 그 matcher 가 `Edit` 와 `Write` 를 모두 잡는다 · 플러그인 훅 command 는 `CLAUDE_PLUGIN_ROOT` 를 쓴다 · `stat -f %Lp` 로 두 스크립트 `755` · `python3 scripts/validate-plugin.py harness` 와 `python3 scripts/validate-plugin.py flutter-toolkit` exit 0)
- [ ] AR-03: 새·고친 킷 파일에 특정 앱 이름이 없다 [exact, enumerated] (측정: `grep -ciE 'fitpal|fit-pal'` 이 `harness/scripts/commit-guard.sh` · `flutter-toolkit/scripts/format-edited-dart.sh` · `flutter-toolkit/skills/flutter-ui-verify/SKILL.md` · `flutter-toolkit/references/visual-evidence-protocol.md` 각 0. 양성 대조: 인사이트 원문 조각 `mcp__fitpal-mobile__screenshot_native_screen` 을 담은 임시 파일에 같은 명령이 1)
- [ ] AR-04: 킷 문서가 새 훅·스킬과 어긋나지 않는다 [exact, enumerated] (측정: `harness/docs/guides/skill-design-guide.md` 에 `commit-guard.sh` 1 회 이상 · `harness/README.md` 에 `commit-guard` 와 `HARNESS_COMMIT_GUARD=off` 각 1 회 이상 · `flutter-toolkit/README.md` 에 `flutter-ui-verify` 와 `format-edited-dart` 와 `FLUTTER_TOOLKIT_FORMAT_ON_EDIT` 각 1 회 이상 · `## 범위 경계` 의 `# oracle: skill_count_lines` 블록을 뽑아 레포 루트에서 실행해 exit 0 — `CLAUDE.md` 2 줄과 `README.md` 2 줄의 flutter-toolkit 스킬 개수가 실제 스킬 폴더 수와 같다 · `python3 scripts/sync-docs.py --check-only` exit 0)
- [ ] AR-05: flutter-toolkit 의 포맷 권고가 폴더 통째가 아니라 바뀐 .dart 파일만 대상으로 한다 [exact, enumerated] (측정: `flutter-toolkit/skills/flutter-run/SKILL.md` · `flutter-toolkit/skills/flutter-preflight/SKILL.md` · `flutter-toolkit/references/project-detection.md` 각 파일에서 `grep -cE 'format (lib|\.)(/|[[:space:]]|$)'` = 0 이고 `grep -c 'git diff --name-only'` ≥ 1. 양성 대조: 390dea8 판 세 파일의 첫 grep 이 1 · 1 · 1 — 계약 작성 시 실측)
- [ ] AR-06: 인사이트 항목과 빈틈 대조 제안 전부가 처리 배정을 받아 카이젠 §0 입력 파일에 있다 [exact, enumerated] (측정: `## 범위 경계` 의 `# oracle: tracking_check` 블록을 뽑아 `python3 <뽑은 파일> .claude/kaizen-input/insights-report.md <세션 scratchpad>/insights/proposal-keys.txt report-2026-09-24-095238.html` 실행 — exit 0 · 출력 `TRACKING_OK`. 검사 내용: frontmatter `generated: 2026-09-24` 와 `report_file` 이 가장 새 보고서 · 표 머리에 `대상 계약` 과 `QA` 열 · 키 파일이 정확히 64 줄 · 중복 0 · F01~F32 각각과 제안 64 건(빈틈 대조 63 + 선언 범위 밖 커밋 차단 `insights:scope-commit-block`) 각각이 앞뒤 경계가 맞는 키로 표 행에 `이번 스프린트` · `Phase N` · `기각` · `해당 없음` 중 하나와 함께 나온다 · 지정 배정 3 건: `harness:P04` 와 `F31`(독립 검토 확인 목록) 은 `Phase 3`, `insights:scope-commit-block` 은 `Phase 4`. 음성 대조: 390dea8 판 파일로 돌리면 exit 1 — 계약 작성 시 실측)

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다 (측정: 새 셸·파이썬 파일 6 개에서 `grep -nE '[0-9]+\.[0-9]+\.[0-9]+'` 히트가 플러그인 버전 문자열이 아니다 — 히트마다 무엇인지 적는다)
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (측정: `python3 scripts/validate-plugin.py --check=code-fence` exit 0)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 금지 (측정: `python3 scripts/validate-plugin.py flutter-toolkit` V1 통과 · 새 SKILL.md `grep -c '^name: flutter-ui-verify$'` = 1)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 — 두 훅은 킷 `scripts/` 에 독립 실행 파일로 두고 hooks.json 이 경로로 부른다 (측정: 두 스크립트가 다른 파일을 source 하지 않고 단독 실행된다 — `grep -cE '^[[:space:]]*(\.|source)[[:space:]]'` 각 0)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 새 스킬은 규약을 복제하지 않고 가리키고(SK-01 복제 검사), 커밋 안전 훅은 기존 두 킷 훅(`sdk-guard.sh` · `run-guard.sh`)과 같은 차단 방식(exit 2 + stderr)을 쓴다 (측정: `grep -c 'exit 2' harness/scripts/commit-guard.sh` ≥ 1)

## Diagnostics

- [ ] DG-01: N/A (commands.analyze 는 `bash -n scripts/release.sh` 로 release.sh 만 잰다 — 이번 화이트리스트에 없다. 측정: `git diff --name-only 390dea8..$(sprint_head) | grep -c '^scripts/release.sh$'` 이 0. 대신 SC-09 가 새 파일 문법을 잰다)
- [ ] DG-02: 편집기 마크다운 진단에서 이번에 더한 줄에 걸린 새 경고 0 개 (측정: 세션 scratchpad 에 `markdownlint-cli2@0.23.2` 를 `npm install --no-save` 로 받고 `{ "config": { "MD013": false } }` 설정으로 이번에 바뀐 `.md` 파일(`.harness/` 제외)만 잰 뒤, `git diff -U0 390dea8..$(sprint_head) -- <파일>` 이 더한 줄 번호에 걸린 경고만 센다. 양성 대조: MD013 을 켜서 새 줄 경고가 1 개 이상 잡히는지 확인)
- [ ] DG-03: N/A (commands.test 는 `bash scripts/release.sh 2>&1 || true` 로 릴리스 스크립트 실행이다 — release.sh 를 바꾸지 않았고 그 실행은 파일을 실제로 고친다(메모리 feedback_release_dryrun_mutates_files). 측정: DG-01 과 같은 grep 이 0. 대신 `python3 scripts/run-evals.py` · `python3 scripts/validate-post-kaizen.py` 가 FAIL 0 인지 본다)
- [ ] DG-04: 실제 Claude Code 세션에서 커밋 안전 훅이 대량 삭제 커밋을 막는다 (측정: 임시 저장소에 60 개 삭제를 스테이징하고 `claude -p --plugin-dir <워크트리>/harness` 로 커밋을 시키면 커밋이 생기지 않고(`git rev-list --count HEAD` 불변) 출력이나 세션 기록에 훅 차단 사유 문구가 있다. 1 차 시도가 플러그인 이름 충돌 등으로 실패하면 `--settings` 에 이 훅만 넣은 설정 파일로 다시 시도한다. 둘 다 안 되면 `[미검증]` 이며 이 조건은 PASS 가 아니다 — canonical 규약의 `[미검증]` 1 건으로 세고, 막은 것 · 시도한 우회 2 개 · 다시 돌릴 명령을 적는다)
</content>
