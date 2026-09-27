## 1. 확인된 결함

### 막아야 함 — 외부 CSS 검사가 유효한 URL 표기를 놓침

위치: [scripts/check-api-kit-docs.py:35](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/scripts/check-api-kit-docs.py:35)

상대경로 `<link>`를 허용하려고 정규식을 좁히면서 대소문자 구분과 속성값 앞 공백을 처리하지 않았다. 기존 구현은 `<link` 자체를 잡았기 때문에 아래 두 입력도 차단했지만, 변경 후에는 통과한다.

재현 명령(파일 생성 없는 메모리 입력):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -c \
'import runpy; m=runpy.run_path("scripts/check-api-kit-docs.py"); cases=["<link href=\"https://x.test/a.css\">","<link href=\"HTTPS://x.test/a.css\">","<link href=\" https://x.test/a.css\">"]; print([(s,bool(m["EXTERNAL"].search(s))) for s in cases])'
```

실제 출력:

```text
[('<link href="https://x.test/a.css">', True),
 ('<link href="HTTPS://x.test/a.css">', False),
 ('<link href=" https://x.test/a.css">', False)]
```

영향:

- `HTTPS://…`는 유효한 대소문자 변형이다.
- HTML URL 파서는 속성값의 선행 공백을 정리하므로 두 번째 변형도 실제 외부 리소스를 불러올 수 있다.
- 그런데 `check-api-kit-docs.py`와 CI는 이를 standalone 위반으로 잡지 않고 PASS 처리한다.
- 의도 문서 [vsa-notes.md](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/vsa-notes.md)에도 이 회귀가 독립 검토에서 재현됐다고 기록돼 있다.

`re.IGNORECASE`를 적용하고 따옴표 뒤 URL 앞 공백을 허용하되, 상대경로만 명시적으로 제외해야 한다.

### 고치면 좋음 — Flutter·React preflight가 정본과 반대인 귀속 규칙을 새로 복제함

위치:

- 정본: [harness/skills/sprint/SKILL.md:123](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/harness/skills/sprint/SKILL.md:123)
- Flutter 사본: [flutter-toolkit/skills/flutter-preflight/SKILL.md:149](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/flutter-toolkit/skills/flutter-preflight/SKILL.md:149), [동 파일:169](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/flutter-toolkit/skills/flutter-preflight/SKILL.md:169)
- React 사본: [react-kit/skills/react-preflight/SKILL.md:81](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/react-kit/skills/react-preflight/SKILL.md:81), [동 파일:101](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/react-kit/skills/react-preflight/SKILL.md:101)

두 preflight 문서는 “판정 표를 글자 그대로 옮긴 사본”이라고 선언했지만, 같은 가지에서 정본은 다음처럼 강화됐다.

- 시작 시점 목록에도 존재
- 내가 쓴 목록 밖
- 둘 중 하나라도 확인 못 하면 귀속 불명
- 결과도 “남의 변경” 확정이 아니라 “후보”

새 Flutter·React 사본은 옛 규칙인 “내가 쓴 목록 밖이면 남의 미커밋이다”를 그대로 넣었다. 정본에 추가된 CI 전용 실패의 `환경·비결정성`/`미확정` 분기도 복제하지 않았다.

재현 명령:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -c \
'from pathlib import Path; files=["harness/skills/sprint/SKILL.md","flutter-toolkit/skills/flutter-preflight/SKILL.md","react-kit/skills/react-preflight/SKILL.md"]; rows=[]; [rows.append(next(x for x in Path(f).read_text().splitlines() if x.startswith("| 실패 | 통과 | — |"))) for f in files]; print("flutter_exact_copy=",rows[0]==rows[1]); print("react_exact_copy=",rows[0]==rows[2]); print("canonical:",rows[0]); print("copied:",rows[1])'
```

실제 출력:

```text
flutter_exact_copy= False
react_exact_copy= False
canonical: | 실패 | 통과 | — | 미커밋 변경 탓 — `git status --short` 의 파일이 작업을 시작할 때 떠 둔 목록에도 있고 내가 쓴 목록 밖이면 남의 미커밋 후보다. 어느 하나라도 확인하지 못하면 귀속 불명이다 |
copied: | 실패 | 통과 | — | 미커밋 변경 탓 — `git status --short` 의 파일이 내가 쓴 목록 밖이면 남의 미커밋이다 |
```

영향:

- 작업 시작 전부터 있던 파일인지 확인하지 않고 다른 세션 변경으로 확정한다.
- 에이전트가 자기 변경이나 귀속 불명 변경을 동료 작업으로 잘못 보고할 수 있다.
- CI에서만 발생한 실패도 정본의 두 추가 분기를 무시하고 세 원인 중 하나로 억지 귀속할 수 있다.
- 이 가지가 두 preflight에 해당 절을 새로 추가했으므로 기존 결함이 아니라 이번 변경의 직접적인 모순이다.

## 2. 가설

추가 가설 없음. 확증하지 못한 의심은 결함 목록에 넣지 않았다.

## 3. 검토한 범위와 못 본 범위

검토한 범위:

- `origin/main...HEAD`의 요청 범위 103개 변경 파일 전체 인벤토리와 diff
- 의도 자료인 `leftovers.md`, `decisions.md`, 같은 폴더의 `*-notes.md`
- `commit-guard.sh`의 삭제 수 계산, `git add`/`commit -a`, 경로 지정 커밋, 개인 index, 계약 범위 블록 처리
- `save-feedback.sh`의 계약 루트·슬러그·identity 재작성·중복 키 제거·저장 경로
- `validate-plugin.py`, `sync-docs.py`, `run-kaizen-assertions.py`, `detect-docs-drift.py`, eval 동기화·실행기, CI
- 변경된 SKILL·agent·공유 규약의 정본/사본 관계
- Python AST, JSON, Bash 문법과 `git diff --check`

읽기 전용 실행 결과:

```text
validate-plugin.py                    rc=0
run-kaizen-assertions.py              14 passed, 0 failed · rc=0
sync-docs.py --check-only             rc=0
sync-evals.py --check-only            0 added, 0 orphans, 0 missing · rc=0
sync-orchestrator.py --check-only     rc=0
run-evals.py                          rc=0
run-evals.py api-kit --verbose        5 passed, 0 failed · rc=0
detect-docs-drift.py --check-table    어긋남 0 · rc=0
check-reviewer-protocol-copies.py     7 checked, violations 0 · rc=0
check-api-kit-docs.py                 12/12 PASS · rc=0
check-stale-values.py                 rc=0
git diff --check                      rc=0
```

못 본 범위:

- 실행 환경이 임시 폴더 생성도 차단해 `mktemp -d`가 `Operation not permitted`로 실패했다. 따라서 `commit-guard-test.sh`, `save-test.sh`, `decision-gate-test.sh`, 측정 도우미 시험의 새 임시 저장소 통합 재현은 직접 완료하지 못했다.
- 이 제한 때문에 `commit-guard.sh`와 `save-feedback.sh`에는 정적 대조 및 기존 notes의 측정 결과까지만 적용했으며, 확증되지 않은 문제는 보고하지 않았다.
- 사용자 지시대로 `docs/**`의 생성 HTML 자체와 `.harness/**` 변경은 코드 변경 검토 대상에서 제외했다. `.harness/.meta/...`는 변경 의도 파악 용도로만 읽었다.
- 외부 네트워크·공식 문서 최신성 검증은 수행하지 않았다.