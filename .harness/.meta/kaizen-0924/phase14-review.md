# 카이젠 2026-09-24 Phase 14 (onboarding-kit) — 계약 초안 독립 검토

- 대상: `.harness/sprint-contract-kaizen-0924-p14-onboarding-kit.md` (봉인 전, 작업 폴더에 추적 안 된 파일, 28 조건 · 기능 조건 18)
- 개정 파일 `.harness/sprint-amendments-kaizen-0924-p14-onboarding-kit.md` 은 아직 없다 — 봉인 전이라 맞다
- 검토자: REVIEW 에이전트 (사용자 승인 대신, 러닝북 「사용자 승인(5 단계) 대체」)
- 검토일: 2026-09-25

## 결론

고쳐야 봉인할 수 있다. 측정 정의와 예행 값은 내가 새로 만든 예행 저장소에서 바이트 단위로 같게 나왔고, 처리 배정표 · 범위 · 공유 파일 · 조건끼리의 충돌에서는
막을 만한 문제를 못 찾았다. 걸리는 것은 넷이다. 앞의 셋은 「실패할 수 없는 측정」 이고, 넷째는 넘김 목록에서 빠진 반대편이다.

1. **DG-02** 가 더한 줄에 붙은 경고만 센다. 러닝북 `봉인 전에 막는 측정 구멍` 목록이 이 초안 뒤에 늘어나 「파일마다 규칙별 경고 수를 편집 전 판과 비교」 를 요구한다.
   실제로 Gotcha 9 끝과 `## Process` 사이 빈 줄을 지운 사본에서 새 경고 MD022(제목 앞뒤 빈 줄 규칙)가 손대지 않은 `## Process` 줄에 붙었는데 측정은 `new_warnings=0` 을 냈다.
2. **DG-05 (c)** 의 `scripts/check-stale-values.py` 는 onboarding-kit 을 아예 훑지 않는다(`SOURCE_DIRS` 열두 폴더에 없음). 등록부 옛 값 `7개 킷` 을 README 에 넣은 사본에서도
   `되살아난 옛 값 없음` · 종료 코드 0 이었다. 러닝북이 「옛 값 0 을 근거로 삼으려면 그 킷 파일에 직접 grep」 이라고 적은 바로 그 경우다.
3. **DG-05 (b)** 의 `scripts/sync-docs.py --check-only` 도 이 README 에는 늘 `동기화됨` 을 낸다. README 표지가 `<!-- AUTO:skills:start -->` · `<!-- AUTO:skills:end -->` 인데
   `sync-docs.py` 의 `MARKER_RE` 는 `<!-- AUTO:skills -->` · `<!-- /AUTO:skills -->` 만 읽는다. AUTO 표의 행을 `BROKEN` 으로 바꾼 사본에서도 `동기화됨` · 종료 코드 0 이었다.
4. **ER-03 (b)** 넘김 목록에 이 Phase 가 바꾸는 세 파일에서 만든 문서 사이트 페이지 셋(`docs/onboarding-kit/setup-guide.html` · `format-checklist.html` · `project-detection.html`)이 없다.
   `docs/index.html:524`~`:526` 에 등록된 페이지인데 `scripts/detect-docs-drift.py` 에 onboarding-kit 매핑이 없어서, 예행 판에서 `detect-docs-drift.py --since da9fbae` 가
   `No docs drift since da9fbae` 를 냈다. Final F2 가 이 목록으로 다시 만들면 셋은 옛 판으로 남는다.

넷 다 고칠 문구와 측정을 아래에 적었고, 고친 측정을 예행 판에서 돌려 요구값이 나오는 것과 대조 사본에서 값이 떨어지는 것을 확인했다. 고치면 `APPROVE` 다.

## 다시 돌려 본 것

모두 스크래치 `p14rv/` 아래에서만 돌렸다. 작업 폴더에는 이 파일 하나만 썼다.

1. 계약 `회귀 게이트` 절의 bash 블록 셋을 새로 뽑아 DRAFT 의 `p14d/k/` 와 비교했다 — `common.sh` · `m.sh` · `new-warnings.sh` 셋 다 글자 그대로 같다.
2. DRAFT 의 `rehearse.sh` 로 지금 초안을 봉인한 예행 저장소를 내 폴더에 새로 만들고(`p14rv/rh-none`) `runall.sh` 로 26 개 ID 를 다 쟀다 —
   출력이 DRAFT 의 `out-final.txt` 와 바이트 단위로 같다(`diff` 0 줄).
3. 시작 커밋 판(`rehearse.sh … base`)에서 SK-01 · SK-02 · SK-04 · SK-07 · SK-08 · SK-09 · ER-02 · AR-02 · AR-03 · AP-04 를 쟀다 — 계약 표의 「시작 커밋 판」 칸과 같다
   (예: SK-04 `version=0.2.0 runner=0` · `gate_cases=0 same=0 note=0` · `folder=3 referenced=0 equal=0`, ER-02 `kit_names=1 generic=0`).
4. 계약이 적은 대조 넷을 끝 판 사본에서 다시 돌렸다 — ER-01 format-checklist 에 가짜 주소 → `1 0`, SK-04 `g4-ko-unsourced` 기대 넷째 줄을 `unsourced_boxes=2` 로 → `same=0`
   (같은 사본에서 SK-06 첫 줄도 `rc=1 pass=5 3 1 0 1 | … EVALS_FAIL` 로 떨어졌다 — 러너가 기대 출력을 실제로 대조한다), AR-02 `### 2. 사전 준비` → 둘째 칸 `1 0`,
   같은 사본에서 SK-01 `0` 열다섯 · `runs=0 0`.
5. 러너 초안(`p14d/new/run-gate-evals.sh`)을 끝까지 읽었다. 함수를 부를 때마다 SKILL.md 에서 뽑고, 폴더에만 있는 픽스처 · 돈 수와 적힌 수의 차이 · 도구 없음 · 함수 추출 실패 ·
   입력 목록 못 읽음을 따로 멈춘다. 임시 파일은 `mktemp` 폴더에만 쓰므로 한 셸에서 조건을 이어 재도 끝 판 폴더가 바뀌지 않는다.
6. Gotcha 9 의 사용자 말 「앱 올리면 되잖아?」 는 데이터 풀 §0-b 229 줄(friction_detail)에 그대로 있다 — 지어낸 인용이 아니다.
   format-checklist §2 예 표의 세 행은 근거 파일 §2 `other-kits:P9` 와 §4 6 · 7 · 8 번 권장안과 내용이 맞는다.

## 고칠 것 (조건 ID 별)

### DG-02 — 파일마다 규칙별 경고 수 비교로 바꾼다

재현: 끝 판 SKILL.md 에서 「「앱 올리면 되잖아?」 로 되받았다.」 줄과 `## Process` 사이 빈 줄 하나를 지운 사본.
계약 판 측정 `m DG-02` 첫 줄 `total_warning_lines=3 added_lines=20 new_warnings=0` — 경고가 2 → 3 으로 늘었는데 0 이다.
규칙별로 세면 `MD022:0>1`. format-checklist 에서 예 표 끝과 `### 3.` 사이 빈 줄을 지운 사본도 계약 판은 `new_warnings=1`(표 끝 줄의 MD058 만)이고
`### 3.` 에 붙은 MD022 는 못 봤다.

(1) 세 번째 bash 블록 `new-warnings.sh` 를 아래 `rule-delta.sh` 로 바꾼다. 이름을 바꾸면 절 머리의 「`new-warnings.sh` 옆에는 `node_modules` 를 … 잇고」 도 `rule-delta.sh` 로 고친다.

```bash
#!/usr/bin/env bash
# rule-delta.sh <옛 파일> <새 파일> — 규칙별 경고 수를 두 판에서 세어 늘어난 규칙만 낸다
# 더한 줄만 보면 손대지 않은 옆 줄에 붙는 경고(MD022 · MD032 · MD024)를 놓친다 (러닝북 — Phase 7 · 8 · 9 · 11 실측)
# 린터가 안 돌면 0 이 조용히 나온다 — 돌았다는 줄(Linting: 1 file)이 없으면 멈춘다
set -u
DIR=$(cd "$(dirname "$0")" && pwd)
cnt() { local out
  out=$("$DIR/node_modules/.bin/markdownlint-cli2" --config "$DIR/cfg.markdownlint-cli2.jsonc" "$1" 2>&1)
  printf '%s\n' "$out" | grep -q '^Linting: 1 file' || return 2
  printf '%s\n' "$out" | sed -nE 's/^[^ ]*:[0-9]+(:[0-9]+)? (error|warning) (MD[0-9]+)\/.*/\3/p' | sort | uniq -c | awk '{print $2, $1}'; }
O=$(cnt "$1") || { echo "LINT_NOT_RUN $1"; exit 2; }
N=$(cnt "$2") || { echo "LINT_NOT_RUN $2"; exit 2; }
UP=$(join -a 2 -e 0 -o 0,1.2,2.2 <(printf '%s\n' "$O" | grep . | sort) <(printf '%s\n' "$N" | grep . | sort) | awk '$3 > $2 {printf "%s:%s>%s ", $1, $2, $3}')
echo "rules_up=$(printf '%s' "$UP" | wc -w | tr -d ' ') ${UP}"
```

(2) `m.sh` 의 `DG-02)` 갈래를 이렇게 바꾼다 (파일 이름을 줄 앞에 찍어 어느 파일인지 보이게 한다):

```bash
  DG-02)  # markdownlint — 파일마다 규칙별 경고 수를 편집 전 판과 비교 (새 파일은 빈 판). 더한 줄만 보면 옆 줄에 붙는 MD022 · MD032 · MD024 를 놓친다
    for f in "${MDF[@]}"; do L=$(printf '%s' "$f" | tr '/' '_'); cp "$E/$f" "$T/$L.md"
      if [ -e "$T/B/$f" ]; then cp "$T/B/$f" "$T/$L.0.md"; else : > "$T/$L.0.md"; fi
      printf '%s ' "$f"; bash "$K/rule-delta.sh" "$T/$L.0.md" "$T/$L.md"; done ;;
```

(3) 조건 줄:

> - [ ] DG-02: IDE diagnostics 워닝/인포 0개 (`diagnostics.ide_exclude` 값 `[]`) — 이번 변경에 적용: 편집기 마크다운 확장과 같은 조건(markdownlint-cli2 0.23.2 · MD013 끔)으로 마크다운 다섯 파일 **각각**에서 규칙별 경고 수를 편집 전 판(새 파일은 빈 판)과 비교해 늘어난 규칙이 0 개다. 더한 줄만 보지 않는다 — MD022 · MD032 · MD024 는 더한 줄 옆의 손대지 않은 줄에 붙는다(러닝북 측정 구멍 목록). 편집 전부터 있던 경고는 같은 수로 남아도 된다 [exact]
>       (측정: `type m >/dev/null || exit 2;` 뒤 `m DG-02` 다섯 줄이 모두 `rules_up=0` 으로 끝나고 `LINT_NOT_RUN` 줄 0.
>        양성 대조: 끝 판 사본에서 SKILL.md Gotcha 9 마지막 줄과 `## Process` 사이 빈 줄을 지우면 SKILL.md 줄 `rules_up=1 MD022:0>1` — 더한 줄만 세던 옛 측정은 같은 사본에서 `new_warnings=0` 이었다.
>        format-checklist 끝에 `#bad heading` 을 더한 사본에서 그 줄 `rules_up=1 MD018:0>1`, 새 픽스처 출처 줄의 `<…>` 를 벗긴 사본에서 그 줄 `rules_up=1 MD034:0>1`. 린터를 못 찾으면 `LINT_NOT_RUN`)

(4) 같이 고칠 서술: `범위 경계` 의 「DG-02 는 더한 줄의 새 경고만 잰다」 → 「DG-02 는 파일마다 규칙별 경고 수를 편집 전 판과 비교한다 — 편집 전부터 있던 경고는 같은 수로 남으면 된다」.
「판정 근거: ER-01 · ER-02 · AP-01 · AP-03 · DG-02 — 편집 전 판과 파일마다 비교한 더한 줄 계산이다」 에서 DG-02 를 빼고 「DG-02 는 파일마다 규칙별 경고 수 비교다」 한 줄을 더한다.
`봉인 전 실측` 표의 DG-02 행은 예행 판 `rules_up=0` 다섯 · 시작 커밋 판 「다섯 파일 규칙별 수 그대로」 · 대조 칸은 위 셋으로 바꾼다.

실측(내 예행 판 `p14rv/rh-none`, 고친 `m.sh` = `p14rv/k2/`): 다섯 줄 모두 `rules_up=0`. 빈 줄 삭제 사본 `rules_up=1 MD022:0>1`, `#bad heading` → `MD018:0>1`,
`<…>` 벗김 → `MD034:0>1`, `node_modules` 를 치운 폴더에서 `LINT_NOT_RUN` · 종료 코드 2.

### DG-05 — (c) 는 직접 세고, (b) 는 뺀다

재현: (c) 예행 판 README 끝에 `7개 킷`(등록부 `.harness/stale-values.yaml` 의 옛 값)을 더하고 `python3 scripts/check-stale-values.py` → `검사 범위: 소스 디렉토리 12/12 · 파일 133 개 …` · `되살아난 옛 값 없음` · 종료 코드 0.
(b) README AUTO 표의 `/setup-guide` 행 설명 칸을 `BROKEN` 으로, 또는 머리 줄을 `BROKEN LINE` 으로 바꾸고 `python3 scripts/sync-docs.py --check-only` → 두 번 다
`onboarding-kit/README.md: 동기화됨` · 종료 코드 0. 표지를 `<!-- AUTO:skills -->` · `<!-- /AUTO:skills -->` 로 바꾸면 그제야 `변경 필요` 가 나온다(스킬 설명 전문으로 표를 다시 쓰려 한다).
planning-kit README 도 같은 `:start` · `:end` 표지다.

(1) `m.sh` 의 `DG-05)` 갈래 — `sync-docs.py` · `check-stale-values.py` 두 줄을 지우고 옛 값을 일곱 파일에서 직접 센다:

```bash
  DG-05)  # 저장소 검사 — $END 판을 git 저장소로 만든 사본에서. 옛 값은 이 킷을 안 훑는 check-stale-values.py 대신 일곱 파일에서 직접 센다
    local G=$T/G; rm -rf "$G"; cp -R "$E" "$G"
    git -C "$G" init -q && git -C "$G" add -A && git -C "$G" -c user.name=m -c user.email=m@m commit -qm snap || return 2
    ( cd "$G" && python3 scripts/validate-plugin.py onboarding-kit > "$T/vp.txt" 2>&1; echo $? > "$T/vp.rc" )
    echo "$(grep -cE '^  V([1-9]|10) ' "$T/vp.txt") $(grep -E '^  V([1-9]|10) ' "$T/vp.txt" | grep -cvE -- '— (OK|SKIP \(no templates/\))$') rc=$(cat "$T/vp.rc")"
    python3 - "$E/.harness/stale-values.yaml" "${FILES[@]/#/$E/}" <<'PY'
import sys, yaml
vals = [v["old"] for v in yaml.safe_load(open(sys.argv[1], encoding="utf-8"))["values"]]
hits = sum(open(p, encoding="utf-8").read().count(o) for p in sys.argv[2:] for o in vals)
print("stale_old=%d files=%d hits=%d" % (len(vals), len(sys.argv[2:]), hits))
PY
    ;;
```

(2) 조건 줄:

> - [ ] DG-05: 저장소 검사가 이 킷을 문제로 가리키지 않는다 — `$END` 판을 git 저장소로 만든 사본에서 (a) `scripts/validate-plugin.py onboarding-kit` 출력에 `V1` ~ `V10` 열 줄이 있고 `— OK` · `— SKIP (no templates/)` 로 끝나지 않는 줄이 0 이며 종료 코드 0 (b) `.harness/stale-values.yaml` 의 `old` 값 전부를 일곱 파일에서 직접 센 수가 0 이다. `scripts/check-stale-values.py` 는 `SOURCE_DIRS` 에 onboarding-kit 이 없어 이 킷을 훑지 않고, `scripts/sync-docs.py --check-only` 는 이 README 의 표지(`<!-- AUTO:skills:start -->`)를 못 읽어 늘 `동기화됨` 을 내므로 둘 다 근거로 쓰지 않는다 (러닝북 측정 구멍 목록) [exact]
>       (측정: `type m >/dev/null || exit 2;` 뒤 `m DG-05` 두 줄이 `10 0 rc=0` · `stale_old=N files=7 hits=0` 이고 N 이 1 이상.
>        음성 대조: SKILL.md 의 `name: setup-guide` 를 `nam:` 으로 깬 사본에서 첫 줄 `10 1 rc=2`. 양성 대조: README 끝에 등록부 옛 값 `7개 킷` 을 더한 사본에서 `hits=1` — 같은 사본에서 `check-stale-values.py` 는 `되살아난 옛 값 없음` · 종료 코드 0 이었다)

`N` 을 15 로 잠그지 않는 까닭: 등록부는 공유 파일이라 `$END` 전에 다른 주체가 값을 더할 수 있다.

(3) 같이 고칠 서술: `범위 경계` 의 「onboarding-kit README 는 … AUTO 구간은 스킬 frontmatter 만 읽는데 그 줄이 그대로다(AP-04 · DG-05)」 에서 `DG-05` 를 뺀다 — 그 근거는 AP-04 하나다.
`봉인 전 실측` 표 DG-05 행: 예행 판 `10 0 rc=0` · `stale_old=15 files=7 hits=0`, 대조 칸에 `7개 킷` → `hits=1` 을 더한다.
notes `## 다음 사이클 메모` 에 한 줄(조건으로는 재지 않는다): onboarding-kit · planning-kit README 의 AUTO 표지가 `:start` · `:end` 꼴이라 `sync-docs.py` `MARKER_RE` 가 못 읽는다 —
표지를 바꾸면 표 내용이 스킬 설명 전문으로 바뀌므로 이번에 고치지 않았다.

실측(`p14rv/k2/`): 예행 판 `10 0 rc=0` · `stale_old=15 files=7 hits=0`, README 에 `7개 킷` 을 더한 사본 `hits=1`.

### ER-03 — 넘김 목록에 파생 문서 페이지 셋과 드리프트 매핑을 더한다

재현: 예행 판(`p14rv/rh-none`, 구현 커밋이 SKILL.md · format-checklist · project-detection 을 바꾼 판)에서 `python3 scripts/detect-docs-drift.py --since da9fbae --verbose` →
`No docs drift since da9fbae`. `scripts/detect-docs-drift.py` 의 `SOURCE_TO_HTML` · `SOURCE_OVERRIDES` 에 `onboarding-kit/` 줄이 없다.
세 페이지는 `docs/index.html:524`~`:526` 에 등록돼 있다(`onboarding-kit/setup-guide.html` · `project-detection.html` · `format-checklist.html`).

(1) 조건 (b) 넘김 목록에 넷을 더한다 — 「… `plugin.json` (Final — 버전) · `docs/onboarding-kit/setup-guide.html` · `docs/onboarding-kit/format-checklist.html` · `docs/onboarding-kit/project-detection.html` (Final F2 — 소스가 바뀌었는데 드리프트 목록에 안 나온다) · `scripts/detect-docs-drift.py` (onboarding-kit 소스 매핑이 없다 — 예행 판에서 `No docs drift since da9fbae`) 이 각각 1 줄 이상」.
Then 의 「일곱 값 모두 `1` 이상」 → 「열한 값 모두 `1` 이상」.

(2) `m.sh` `ER-03)` 갈래 둘째 `toks` 인자 끝에 넷을 더한다:

```bash
    toks "$(sect "$E/$NOTES" '## 넘기는 것' 2>/dev/null)" '.github/workflows/ci.yml' 'command -v zsh' 'sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh' \
      'docs/onboarding-kit/examples/fcm-ios-setup-guide.md' 'docs/onboarding-kit/fcm-ios-example.html' '.claude/skills/onboarding-kaizen/SKILL.md' 'plugin.json' \
      'docs/onboarding-kit/setup-guide.html' 'docs/onboarding-kit/format-checklist.html' 'docs/onboarding-kit/project-detection.html' 'scripts/detect-docs-drift.py'
```

(3) `GAP 분석` 복잡도 표 「소비면 존재」 칸과 편집 전 감사 표에 세 페이지를 반대편으로 적고, `커버리지 해소: ER-01 · ER-03` 줄의 넘김 경로 목록에도 넷을 더한다.
notes 모의본(`p14d/notes-mock.md`)의 `## 넘기는 것` 표에 줄을 더하고 봉인 전에 다시 잰다.

실측(`p14rv/k2/`): 지금 notes 모의본 그대로면 셋째 줄 `1 1 1 1 1 1 1 0 0 0 0` — 새 넷이 없어서 떨어진다. `## 넘기는 것` 표에
「`docs/onboarding-kit/setup-guide.html` · `docs/onboarding-kit/format-checklist.html` · `docs/onboarding-kit/project-detection.html` | Final F2 | 소스가 바뀌었는데 `scripts/detect-docs-drift.py` 에 onboarding-kit 매핑이 없어 드리프트 목록에 안 나온다」
한 줄을 더한 사본에서 `1` 열하나.

### 범위 경계 notes 목록 한 줄 — ER-03 (d) 와 어긋난다

「ER-03 마지막 값이 0 이 아니면 QA 가 그 커밋 목록부터 보고 판정한다는 한 줄」 은 조건 (d) 의 「0 개다」 를 풀어 주는 말로 읽힌다. 서명 없는 커밋이 공유 경로를 건드리면
그 커밋이 누구 것인지 가를 수 없다 — 이 Phase 가 서명을 빠뜨린 커밋이 바로 러닝북이 잡으라는 것이다. 이 줄을 「ER-03 마지막 값이 0 이 아니면 FAIL 이고, QA 는 그 커밋 목록을 근거에 적는다」 로 바꾸거나 지운다.

## 고치면 좋은 것 (막지 않는다)

- ER-04 괄호의 「(e1) 이 ②(폴더에만 있는 시험 파일)」 — `harness/agents/qa-evaluator.md` 규칙 10 의 사본 입력 다섯 가운데 ② 는 「표에만 올린 시험」(목록에는 있는데 안 도는 것)이다.
  (e1) 은 그 반대(폴더에는 있는데 목록에 없는 것)다. 「(e1) 은 폴더에만 있는 픽스처 — 규칙 10 ② 와 반대 방향」 처럼 고치면 QA 가 헷갈리지 않는다
- format-checklist §2 첫 목록 「필요한 계정/권한 (예: Apple Developer Program 가입)」 은 새 규칙이 막는 「한 줄 요구」 모양 그대로다. 끝에 「— 막는 요구면 아래 세 칸」 정도를 붙이면
  규칙과 어긋나 보이지 않는다. 붙이면 SK-01 토큰 · DG-02 · 봉인 전 실측도 같이 고친다
- ER-03 (d) 의 경로는 `docs/onboarding-kit` · `docs/index.html` 만 본다. 서명 없는 커밋이 다른 `docs/` HTML 을 건드리면 아무 조건도 못 본다. `docs` 전체로 넓히면 다른 Phase 의
  서명 빠진 커밋 때문에 이 Phase 가 떨어질 수 있어서, 지금처럼 두는 것도 이해한다

## 봤고 문제없던 것

- 처리 배정표 `배정` 이 `Phase 14` 인 행은 `other-kits:P3` · `other-kits:P9` 둘이고(insights-report.md 144 · 152 줄) 둘 다 반영됐다. `F10` 비고 · Phase 1 notes 넘김 한 줄(`SKILL.md:30`) · 오케스트레이터 Step 14 전수 감사도 다뤘다.
  `other-kits:P3` 의 CI(자동 검사) 줄은 러닝북 규칙대로 notes 넘김이고 ER-03 이 잰다. howto-kit 단계는 Phase 17 몫이라는 비고와 맞다
- 이전 Phase notes 에서 Phase 14 로 넘긴 줄은 `phase1-notes.md:52` 하나뿐이다(전체 notes · review grep)
- 범위: 고치는 파일 일곱이 전부 `onboarding-kit/` 안이고 나머지는 `.harness/` 다 — 러닝북 Phase 표 14 행과 맞다. 공유 파일(`marketplace.json` · plugin.json 버전 · 루트 README · CLAUDE.md · `docs/` HTML · ci.yml · 등록부)은 건드리지 않고 ER-03 (d) 가 경로로 직접 센다
- 기준 커밋 `da9fbae` 는 계약 파일이 처음 생긴 09:43 에 `HEAD` 였다(그 뒤 Phase 12 커밋 다섯은 전부 Phase 12 서명이 있다)
- 러닝북 측정 구멍 목록 가운데 나머지: 경로로 직접 세기(AR-01 ① · ER-03 (d)) · 상한 못 구하면 멈춤(`END_UNRESOLVED`) · 셸 함수 확인(`m` 이 도우미 스물을 확인) · 파일마다 비교(ER-01 · `added`) ·
  `validate-plugin.py` 종료 코드(DG-05 `rc=0`) · 문장만 지운 사본(55/60 DROP, 없던 5 는 0 기대 옛 문장) — 다 지켰다. 연구 기록 소제목 날짜는 이 킷에 연구 기록 파일이 없어 해당 없음
- 조건끼리: AR-03 이 `guide_gate` 코드 블록을 그대로 두게 하고 SK-07 의 새 줄은 그 블록 밖이다(끝 판 AR-03 `1`). SK-03 이 `no-invented-paths` 를 빼고 비교하고 SK-09 (d) 가 그 사례를 고친다.
  AP-01 이 세는 `0.3.2` 와 SK-04 의 `evals.json` `0.3.0` 은 다르다. AR-02 (e) 의 `§3.7 조항 3 의 네 칸` 2 는 SK-02 · SK-08 문장에서 하나씩 나온다. 부딪히는 곳 없음
- 번역투 정규식은 `tone-kit/references/locale-korean.md` §2 치환표 grep 열 여섯과 같다

## 참고 — 고친 뒤 BUILD 가 할 일

- DG-02 · DG-05 · ER-03 세 줄의 `봉인 전 실측` 을 다시 재서 표를 고친다. 고친 `m.sh` · `rule-delta.sh` 는 `p14rv/k2/` 에 있고, 대조를 돈 스크립트는 `p14rv/dg/`(`dg02.sh` · `k2run.sh` · `ctl.sh`)다
- 예행 저장소는 디스크 여유(1.5 GB)가 적어 지웠다. 다시 만들 때 한 번에 하나씩 만들고 지운다

VERDICT: CHANGES

## 2 회차

- 대상: 같은 계약 초안 `.harness/sprint-contract-kaizen-0924-p14-onboarding-kit.md` (봉인 전, 686 줄, `conditions: 28`). 개정 파일은 아직 없다 — 봉인 전이라 맞다
- 검토자: REVIEW 에이전트 (2 회차) · 검토일 2026-09-25
- 스크래치: `p14rv2/` 아래에서만 돌렸다. 작업 폴더에는 이 절만 덧붙였다

### 결론 (2 회차)

1 회차가 고치라고 한 넷(DG-02 · DG-05 (b) · DG-05 (c) · ER-03 (b))과 범위 경계 notes 한 줄이 모두 반영됐다. 권고 셋 가운데 둘(ER-04 괄호 · format-checklist 첫 목록 줄)은 반영됐고,
나머지 하나(ER-03 (d) 경로를 `docs` 전체로 넓히기)는 1 회차가 「지금처럼 두는 것도 이해한다」 고 한 것이라 그대로 둔 것이 맞다. 새로 막을 결함은 찾지 못했다. 봉인해도 된다.

### 반영 확인 (조건 ID 별)

- **DG-02** — `rule-delta.sh` 블록(511~525 줄) · `m.sh` `DG-02)` 갈래(478~481 줄) · 조건 줄(669~673 줄) · 판정 근거 두 줄(151 · 152 줄, ER-01 줄에서 DG-02 가 빠지고 따로 한 줄) ·
  편집 전 경고 서술(166~168 줄) · 절 머리 「`rule-delta.sh` 옆에는 `node_modules`」(185 줄) · 봉인 전 실측 표 DG-02 행(557 줄). 1 회차 안과 다른 곳은 하나 — 끝 출력 줄에 뒤 공백이 없다
  (`rules_up=1 MD022:0>1`). 조건 줄의 기대값 · 대조값이 이 꼴로 적혀 있어 서로 맞는다
- **DG-05** — `m.sh` `DG-05)` 갈래(485~496 줄)에서 `sync-docs.py` · `check-stale-values.py` 줄이 빠지고 등록부 `old` 값을 일곱 파일에서 직접 센다. 조건 줄(678~682 줄)은 (a) · (b) 두 칸이고
  두 도구를 근거로 쓰지 않는 까닭과 그 실측을 적었다. `범위 경계` 의 README 줄은 `(AP-04)` 만 남았다(137 줄). 판정 근거(154~156 줄) · 봉인 전 실측 표(559 줄) · notes `## 다음 사이클 메모` 로 갈 AUTO 표지 한 줄(171 줄)
- **ER-03** — 조건 (b) 넘김이 열하나이고 Then 이 「열한 값 모두 `1` 이상」(618 · 619 줄). `m.sh` `toks` 인자 끝에 넷(436~438 줄). `GAP 분석` 소비면 칸(49 줄) · 편집 전 감사 표 새 행(76 줄) ·
  `커버리지 해소: ER-01 · ER-03` 줄(160~163 줄). notes 모의본(`p14d2/notes-mock.md`) `## 넘기는 것` 표에 페이지 셋 행 · 드리프트 스크립트 행 둘이 더해졌다
- **범위 경계 notes 줄** — 「커밋 목록부터」 가 계약에 0 줄. ER-03 Then 끝에 「다섯째 줄이 0 이 아니면 FAIL 이다.」 가 있다
- **권고 반영** — ER-04 괄호(631 줄)의 규칙 10 ② · ③ 풀이가 `harness/agents/qa-evaluator.md` 64 줄과 맞는다. format-checklist 첫 목록 줄은 SK-01 (e) 로 조건이 됐고 `m.sh` 토큰 열여섯째 ·
  문장 삭제 대조 수(61 개 가운데 56 DROP · 5 MISSING, `p14d2/del-out.txt`)가 함께 고쳐졌다

### 다시 돌려 본 것 (2 회차)

1. 계약 `회귀 게이트` 절의 bash 블록 셋을 새로 뽑아(`p14rv2/k/`) DRAFT 의 `p14d2/k/` 와 비교했다 — `common.sh` · `m.sh` · `rule-delta.sh` 셋 다 글자 그대로 같다. `cfg.markdownlint-cli2.jsonc` 도 같고,
   `node_modules` 자리의 `markdownlint-cli2 --version` 첫 줄이 `markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)` 다
2. DRAFT 의 예행 저장소 `p14d2/rh-none` 에 내 도우미 폴더로 `runall.sh` 26 개 ID 를 다 쟀다 — `p14d2/out-none.txt` 와 바이트 단위로 같다. 예행 저장소에 봉인된 계약의 조건 줄 지문
   (sha256 앞 16 자리)이 `e90190048db61bfa` 로 지금 초안의 조건 줄과 같다. 두 파일의 차이는 ER-03 설명 줄의 「인자 열다섯」 → 「열넷」 한 곳이고(조건 체크박스 줄이 아니다), `not_other` 인자를 세어 보면 열넷이 맞다
3. DG-02 대조를 직접 돌렸다(`p14rv2/dg02.sh`, 끝 판 = 예행 `end_sha` `5038f5f`): 편집 전 판 대 끝 판 SKILL.md · format-checklist · 새 픽스처(빈 판 대비) 모두 `rules_up=0`.
   Gotcha 9 끝과 `## Process` 사이 빈 줄 삭제 → `rules_up=1 MD022:0>1`, 예 표 끝과 `### 3.` 사이 빈 줄 삭제 → `rules_up=2 MD022:0>1 MD058:0>1`, `#bad heading` → `rules_up=1 MD018:0>1`,
   새 픽스처 `<…>` 벗김 → `rules_up=1 MD034:0>1`, 경고가 줄어든 방향(깬 판 → 끝 판) → `rules_up=0`, `node_modules` 없는 폴더 → `LINT_NOT_RUN` · 종료 코드 2. 계약 표와 같다
4. DG-05 · ER-03 대조를 끝 판 폴더를 한 군데씩 바꿔 돌렸다(`p14rv2/ctl.sh`): README 끝에 `7개 킷` → `hits=1`(등록부 53 줄의 `old`), 같은 사본에서 `check-stale-values.py` 는
   `되살아난 옛 값 없음` · 종료 코드 0. `nam: setup-guide` → `10 1 rc=2`. AUTO 표 `/setup-guide` 행 설명을 `BROKEN` 으로 바꾼 사본에서 `sync-docs.py --check-only onboarding-kit` →
   `onboarding-kit/README.md: 동기화됨` · 종료 코드 0. notes 모의본에서 새 두 행을 뺀 사본 → ER-03 셋째 줄 `1 1 1 1 1 1 1 0 0 0 0`. 전부 계약 표와 같다
5. `harness/skills/sprint-contract/SKILL.md` Step 6.5 의 저장 검사 (1)~(3) · (5) 를 돌렸다 — 제목 12 개가 허용 목록 안이고, 조건 줄은 전부 카테고리 절(Skill 9 · Script 1 · Error 4 · Architecture 3 ·
   Anti-patterns 3 · Reusability 2 · Diagnostics 6)에 있으며, `conditions: 28` = 실제 28, `[미실측]` 0. (4) 측정 커버리지 검출기(`harness/references/contract-schema.md` 스니펫 그대로)는
   `UNCOVERED` 11 건(SK-02 · SK-03 · SK-04 · SK-06 · SK-07 · SK-09 · ER-01 · ER-03 · ER-04 · AR-01 · AR-03)을 냈고, 전부 `범위 경계` 의 `커버리지 해소` 네 줄(157~164 줄)이 이름을 들어 덮는다.
   새 넘김 넷도 ER-03 해소 줄에 있다
6. 규칙별 수만 비교하면 편집 전 경고 하나가 없어지고 같은 규칙의 새 경고가 생길 때 수가 같아 못 본다. 그런 일이 예행 판에 있었는지 네 기존 파일의 경고 글을 줄 번호를 빼고 두 판에서 비교했다(`p14rv2/swap.sh`) —
   넷 다 같다. SKILL.md 의 MD032 가 160 → 161 줄로 밀렸을 뿐이다
7. `scripts/detect-docs-drift.py` 는 250 줄에서 소문자 `no docs drift since …` 를 찍는다(`p14d2/drift.txt` 도 같다). 계약 76 · 618 줄의 인용이 맞고, 1 회차 검토의 대문자 `No` 는 내가 옮겨 적다 틀린 것이다.
   `SOURCE_TO_HTML` 33 줄 · `SOURCE_OVERRIDES` 66 줄 · `docs/index.html` 524~526 줄의 세 페이지도 계약이 적은 자리 그대로다
8. `da9fbae..HEAD` 커밋 다섯(전부 Phase 12) 가운데 `onboarding-kit` · `docs/onboarding-kit` · `docs/index.html` · `scripts/detect-docs-drift.py` · `.harness/stale-values.yaml` 을 건드린 커밋은 0 이다

### 새 결함

막을 것은 없다.

### 참고 (막지 않는다)

- DG-02 는 러닝북이 적은 대로 규칙별 수를 비교한다. 위 6 의 「없어지고 새로 생겨 수가 같은」 경우는 예행 판에 없었지만, BUILD 의 실제 편집이 모의본과 달라지면 QA 가 줄 번호를 뺀 경고 글 비교를
  한 번 더 해 보면 확실하다. 조건으로 넣을 일은 아니다
- 디스크 여유가 1.6 GB 다. 예행 저장소는 20 MB 남짓이라 괜찮지만 BUILD 와 QA 가 여러 벌을 한꺼번에 만들지 않게 한다. `p1build/node_modules` 가 지워져 있으면 계약 185~188 줄대로 다시 설치한다
- 봉인 뒤에는 설명 줄(체크박스 아래 들여 쓴 줄)을 고쳐도 봉인 값이 안 바뀐다 — 위 2 의 「열다섯 → 열넷」 이 그 예다. 이번 초안은 둘이 맞으니 문제없고, BUILD 가 봉인 뒤 설명 줄을 고칠 일이 생기면 개정 파일에 적는다

VERDICT: APPROVE
