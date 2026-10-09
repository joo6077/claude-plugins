#!/usr/bin/env bash
# repro.sh <레포 폴더> <훅 폴더> — Codex 최종 점검 결함 1~10 을 가장 작은 입력으로 재현한다.
# 레포 폴더의 도구(BASE 를 푼 폴더 또는 작업 폴더)와 훅 폴더의 훅 둘(고치기 전 사본 또는 ~/.claude/hooks)을 돌린다.
# 경우마다 한 줄: <결함> <경우> rc=<종료 코드> [덧붙인 값]. 훅 경우는 훅이 늘 0 으로 끝나니 출력으로 판정한다.
# 임시 폴더는 TMPDIR 아래 만들고 끝나면 지운다. 레포 폴더 · 훅 폴더에는 쓰지 않는다.
set -u
R=$(cd "${1:?레포 폴더}" && pwd) || exit 2
H=$(cd "${2:?훅 폴더}" && pwd) || exit 2
NODE_MODULES=${NODE_MODULES:-$R/node_modules}
T=$(mktemp -d "${TMPDIR:-/tmp}/cx-repro.XXXXXX") || exit 2
trap 'chmod -R u+rwx "$T" 2>/dev/null; rm -rf "$T"' EXIT
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@example.com GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@example.com

# 결함 1 — detect-docs-drift: 없는 기준 판
d=$T/d1; mkdir -p "$d/scripts" "$d/docs/tone-kit" "$d/docs/tone"
cp "$R/scripts/detect-docs-drift.py" "$d/scripts/"
printf '<a href="tone-kit/overview.html">o</a>\n' >"$d/docs/index.html"
printf '<p>page</p>\n' >"$d/docs/tone-kit/overview.html"
printf '# 개요\n\n본문\n' >"$d/docs/tone/overview.md"
git -C "$d" init -q && git -C "$d" add -A && git -C "$d" commit -qm base
out=$(cd "$d" && python3 scripts/detect-docs-drift.py --since refs/heads/definitely-not-there 2>&1); rc=$?
echo "d1 bad-ref rc=$rc nodrift=$(printf '%s\n' "$out" | grep -c '^no docs drift') msg=$(printf '%s\n' "$out" | grep -c 'definitely-not-there')"
out=$(cd "$d" && python3 scripts/detect-docs-drift.py --since HEAD 2>&1); rc=$?
echo "d1 good rc=$rc nodrift=$(printf '%s\n' "$out" | grep -c '^no docs drift')"

# 결함 2 — sync-evals: 깨진 evals.json
mk_evals_tree() {  # mk_evals_tree <폴더> <evals.json 내용>
  mkdir -p "$1/scripts" "$1/.claude-plugin" "$1/k/evals" "$1/k/skills/s"
  cp "$R/scripts/sync-evals.py" "$R/scripts/run-evals.py" "$R/scripts/plugin_utils.py" "$1/scripts/"
  printf '{"plugins":[{"name":"k","source":"./k"}]}\n' >"$1/.claude-plugin/marketplace.json"
  printf -- '---\nname: s\ndescription: d\nuser-invocable: true\n---\n\n본문\n' >"$1/k/skills/s/SKILL.md"
  printf '%s\n' "$2" >"$1/k/evals/evals.json"
}
GOOD_EVALS='{"evals":[{"id":1,"skill":"s","prompt":"p","expected_output":"e","assertions":[{"text":"a","type":"output"}]}]}'
mk_evals_tree "$T/d2bad" '{ broken'
out=$(cd "$T/d2bad" && python3 scripts/sync-evals.py --check-only 2>&1); rc=$?
echo "d2 broken-json rc=$rc msg=$(printf '%s\n' "$out" | grep -c 'k/evals/evals.json')"
mk_evals_tree "$T/d2good" "$GOOD_EVALS"
(cd "$T/d2good" && python3 scripts/sync-evals.py --check-only >/dev/null 2>&1); echo "d2 good rc=$?"

# 결함 3 — ci-local: 돌릴 run 단계가 0 개
wf() { mkdir -p "$T/$1/.github/workflows" && cat >"$T/$1/.github/workflows/ci.yml"; }
printf 'jobs:\n  a:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n' | wf d3uses
printf 'jobs:\n  a:\n    runs-on: ubuntu-latest\n    steps:\n      - name: Install\n        run: pip install pyyaml\n' | wf d3skip
printf 'jobs:\n  a:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - name: Good\n        run: echo ok\n' | wf d3good
bash "$R/scripts/ci-local.sh" "$T/d3uses" >/dev/null 2>&1; echo "d3 uses-only rc=$?"
bash "$R/scripts/ci-local.sh" --list "$T/d3uses" >/dev/null 2>&1; echo "d3 uses-only-list rc=$?"
bash "$R/scripts/ci-local.sh" "$T/d3skip" >/dev/null 2>&1; echo "d3 all-skip rc=$?"
bash "$R/scripts/ci-local.sh" "$T/d3good" >/dev/null 2>&1; echo "d3 good rc=$?"

# 결함 4 — check-install-docs-guidance: 못 읽는 추적 파일
mk_guidance_repo() {  # mk_guidance_repo <폴더> <k/a.md 내용>
  mkdir -p "$1/scripts" "$1/k/.claude-plugin" "$1/docs/foo"
  cp "$R/scripts/check-install-docs-guidance.py" "$1/scripts/"
  printf '{"name":"k"}\n' >"$1/k/.claude-plugin/plugin.json"
  printf 'x\n' >"$1/docs/foo/x.md"
  printf '%s\n' "$2" >"$1/k/a.md"
  git -C "$1" init -q && git -C "$1" add -A && git -C "$1" commit -qm base
}
RAW=https://raw.githubusercontent.com/joo6077/claude-plugins/main/
mk_guidance_repo "$T/d4bad" '참고: docs/foo/x.md'
chmod 000 "$T/d4bad/k/a.md"
out=$(cd "$T/d4bad" && python3 scripts/check-install-docs-guidance.py 2>&1); rc=$?
echo "d4 unreadable rc=$rc msg=$(printf '%s\n' "$out" | grep -c 'k/a.md')"
chmod 644 "$T/d4bad/k/a.md"
mk_guidance_repo "$T/d4good" "참고: docs/foo/x.md
설치본 플러그인에는 \`docs/foo/\` 가 없다 — $RAW 뒤에 붙여 읽는다."
(cd "$T/d4good" && python3 scripts/check-install-docs-guidance.py >/dev/null 2>&1); echo "d4 good rc=$?"

# 결함 5 — check-superseded: 못 읽는 계약
contract() {  # contract <폴더> <슬러그> <머리 줄…>
  folder=$1 slug=$2; shift 2
  { printf -- '---\nslug: %s\n' "$slug"; printf '%s\n' "$@"; printf -- '---\n\n## Skill\n- [ ] 스킬-01: x\n'; } >"$folder/sprint-contract-$slug.md"
}
sup() {  # sup <이름> <폴더> — 출력 줄 모양을 센다
  out=$(bash "$R/harness/scripts/check-superseded.sh" "$2" 2>&1); rc=$?
  echo "d5 $1 rc=$rc ok=$(printf '%s\n' "$out" | grep -c '^OK ') unreadable=$(printf '%s\n' "$out" | grep -c '^UNREADABLE ')"
}
s=$T/d5a/.harness; mkdir -p "$s"
contract "$s" a 'status: superseded' 'superseded_by: b'; contract "$s" b 'status: active'; chmod 000 "$s/sprint-contract-b.md"
sup target-unreadable "$s"
s=$T/d5b/.harness; mkdir -p "$s"
contract "$s" a 'status: superseded' 'superseded_by: b'; contract "$s" b 'status: active'; chmod 000 "$s/sprint-contract-a.md"
sup contract-unreadable "$s"
s=$T/d5c/.harness; mkdir -p "$s"
contract "$s" a 'status: superseded' 'superseded_by: b'; contract "$s" b 'status: active'
sup good "$s"

# 결함 6 — run-evals: 빈 eval 목록
mk_evals_tree "$T/d6list" '{"evals":[]}'
out=$(cd "$T/d6list" && python3 scripts/run-evals.py 2>&1); rc=$?
echo "d6 empty-list rc=$rc msg=$(printf '%s\n' "$out" | grep -c 'k/evals/evals.json')"
mk_evals_tree "$T/d6nokey" '{}'
out=$(cd "$T/d6nokey" && python3 scripts/run-evals.py 2>&1); rc=$?
echo "d6 no-key rc=$rc msg=$(printf '%s\n' "$out" | grep -c 'k/evals/evals.json')"
mk_evals_tree "$T/d6good" "$GOOD_EVALS"
(cd "$T/d6good" && python3 scripts/run-evals.py >/dev/null 2>&1); echo "d6 good rc=$?"

# 결함 7 — check-docs-a11y: HTML 0 개인 docs/
mkdir -p "$T/d7bad/docs" "$T/d7good/docs"
printf '# md 만 있다\n' >"$T/d7bad/docs/readme.md"
printf '<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>t</title></head><body style="background:#fff;color:#000"><p>본문</p></body></html>\n' >"$T/d7good/docs/a.html"
out=$(cd "$T/d7bad" && NODE_PATH=$NODE_MODULES node "$R/scripts/check-docs-a11y.js" 2>&1); rc=$?
echo "d7 no-html rc=$rc pass_line=$(printf '%s\n' "$out" | grep -c 'PASS$')"
out=$(cd "$T/d7good" && NODE_PATH=$NODE_MODULES node "$R/scripts/check-docs-a11y.js" 2>&1); rc=$?
echo "d7 good rc=$rc last=[$(printf '%s\n' "$out" | tail -1)]"

# 결함 8 — run-gate-fixtures: 같은 시험 파일의 표 행 · 실행 줄 중복
S=$R/bambu-kit/skills/bambu-print-profile/SKILL.md
N=process-bambu-only-key-in-orca.json
awk -v n="$N" '{ print } index($0, "| `evals/gate-fixtures/" n "` |") == 1 && !done { print "| `evals/gate-fixtures/" n "` | orca | **PASS** | x | y |"; done = 1 }' "$S" >"$T/dup-row.md"
awk -v n="$N" '{ print } index($0, "python3 \"$GATE\" $FX/" n ";") > 0 && !done { print; done = 1 }' "$S" >"$T/dup-run.md"
gate() {  # gate <이름> <SKILL 사본>
  out=$(BAMBU_GATE_SKILL=$2 bash "$R/bambu-kit/evals/run-gate-fixtures.sh" 2>&1); rc=$?
  echo "d8 $1 rc=$rc dup=$(printf '%s\n' "$out" | grep '^불일치 ' | grep -F "$N" | grep -c '중복') last=[$(printf '%s\n' "$out" | tail -1)]"
}
RUNLINE='^TARGET_SLICER=[a-z]+ +python3 "\$GATE" \$FX/process-bambu-only-key-in-orca\.json;'
echo "d8 inserted row=$(grep -cF "| \`evals/gate-fixtures/$N\` |" "$T/dup-row.md") run=$(grep -cE "$RUNLINE" "$T/dup-run.md")"
gate dup-row "$T/dup-row.md"
gate dup-run "$T/dup-run.md"
gate good "$S"

# 결함 9 — lint-contract-oracle 훅: 한 백틱 안의 grep 명령 전체
lint() {  # lint <로캘> <경우> <조건 줄> <측정 줄>
  mkdir -p "$T/d9/.harness"; c=$T/d9/.harness/sprint-contract-x.md
  printf -- '---\nstatus: active\n---\n\n## Skill\n\n%s\n  %s\n' "$3" "$4" >"$c"
  p=$(jq -nc --arg f "$c" '{tool_name:"Write",tool_input:{file_path:$f}}')
  out=$(printf '%s' "$p" | LC_ALL=$1 bash "$H/lint-contract-oracle.sh" 2>/dev/null)
  tag=$(printf '%s' "$out" | jq -r '.hookSpecificOutput.additionalContext // empty' 2>/dev/null | grep -oE '^  - [^ ]+ \([^)]*\)' | sed 's/^  - //' | tr '\n' ' ')
  echo "d9 $1 $2 found=[${tag% }]"
}
for loc in C en_US.UTF-8; do
  lint "$loc" in-span-en '- [ ] SK-01: x' '측정: `grep -cF "표준으로 강제하지 않는다" file.md` >= 1'
  lint "$loc" in-span-ko '- [ ] 스킬-01: x' '측정: `grep -cF "표준으로 강제하지 않는다" file.md` >= 1'
  lint "$loc" in-span-rg '- [ ] 스킬-02: x' "측정: \`rg -c '표준으로 강제하지 않는다' file.md\` 이 1 이상"
  lint "$loc" split-span-en '- [ ] SK-03: x' '측정: `grep -cF` 로 `표준으로 강제하지 않는다` 를 센 값 >= 1'
  lint "$loc" split-span-ko '- [ ] 스킬-03: x' '측정: `grep -cF` 로 `표준으로 강제하지 않는다` 를 센 값 >= 1'
  lint "$loc" ascii-pattern '- [ ] 스킬-04: x' "측정: \`grep -c 'yaml.safe_load' scripts/ci-local.sh\` 이 1"
  lint "$loc" korean-path '- [ ] 스킬-05: x' "측정: \`grep -c 'abc' 문서/스킬.md\` 이 1"
done

# 결함 10 — qa-pending-check 훅: 빈 QA 결과 파일
qa() {  # qa <경우> <결과 파일 내용 | -none-> — 결과 파일이 없으면 -none-
  p=$T/d10-$1; rm -rf "$p"; mkdir -p "$p/.harness"
  printf -- '---\nslug: x\nstatus: active\nowner_session: S1\nlocked_at: "2026-09-29 10:00"\n---\n\n## Skill\n- [ ] 스킬-01: x\n' >"$p/.harness/sprint-contract-x.md"
  if [ "$2" != -none- ]; then printf '%s' "$2" >"$p/.harness/sprint-feedback-x.md"; fi
  payload=$(jq -nc --arg d "$p" '{session_id:"S1",cwd:$d,transcript_path:""}')
  out=$(printf '%s' "$payload" | bash "$H/qa-pending-check.sh" 2>/dev/null); rc=$?
  echo "d10 $1 rc=$rc pending=$(printf '%s' "$out" | jq -r '.hookSpecificOutput.additionalContext // empty' 2>/dev/null | grep -c 'sprint-contract-x.md')"
}
qa empty ''
qa no-verdict $'# QA\n\nEvaluated: 2026-09-29 11:00\n'
qa approve $'Verdict: APPROVE\nEvaluated: 2026-09-29 11:00\n'
qa approve-old $'Verdict: APPROVE\nEvaluated: 2026-09-28 11:00\n'
qa reject $'Verdict: REJECT\nEvaluated: 2026-09-29 11:00\n'
qa none -none-
