#!/usr/bin/env bash
# m-cilocal.sh <레포> — 로컬 CI 도구의 목록 모드와 작은 CI 파일 네 벌을 잰다. 레포 CI 전체를 돌리지는 않는다.
# 줄마다 `<경우> rc=<종료 코드> last=[<끝 줄>] <세부>`.
R=${1:?레포 경로}
C=$R/scripts/ci-local.sh
T=$(mktemp -d "${TMPDIR:-/tmp}/mcil.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT
yml_steps() { python3 -c 'import sys,yaml; d=yaml.safe_load(open(sys.argv[1])); print(sum(1 for j in d["jobs"].values() for s in j["steps"] if "run" in s))' "$1"; }
wf() { mkdir -p "$T/$1/.github/workflows"; cat > "$T/$1/.github/workflows/ci.yml"; }
# 레포 CI 파일 그대로 — 목록만
out=$(bash "$C" --list "$R" 2>&1); rc=$?
printf 'repo-list rc=%s last=[%s] yaml_steps=%s skip_names=[%s]\n' "$rc" "$(printf '%s\n' "$out" | tail -1)" "$(yml_steps "$R/.github/workflows/ci.yml")" \
  "$(printf '%s\n' "$out" | sed -n -E 's/^SKIP [a-z]+ (.*) \(.*\)$/\1/p' | LC_ALL=C sort | tr '\n' '|' | sed 's/|$//')"
# 레포 CI 파일 + 단계 하나 더
mkdir -p "$T/extra/.github/workflows"
python3 - "$R/.github/workflows/ci.yml" "$T/extra/.github/workflows/ci.yml" <<'PY'
import sys, yaml
d = yaml.safe_load(open(sys.argv[1], encoding="utf-8"))
d["jobs"]["validate"]["steps"].append({"name": "Extra step", "run": "echo extra"})
yaml.safe_dump(d, open(sys.argv[2], "w", encoding="utf-8"), allow_unicode=True, sort_keys=False)
PY
out=$(bash "$C" --list "$T/extra" 2>&1); rc=$?
printf 'extra-list rc=%s last=[%s] extra_run=%s\n' "$rc" "$(printf '%s\n' "$out" | tail -1)" "$(printf '%s\n' "$out" | grep -c '^RUN validate Extra step$')"
# 실행 폴더를 바꾸는 단계 — 도구가 못 다루니 스스로 알려야 한다
wf wd <<'Y'
jobs:
  a:
    runs-on: ubuntu-latest
    steps:
      - name: Plain
        run: echo ok
      - name: Moved
        working-directory: sub
        run: echo moved
Y
out=$(bash "$C" --list "$T/wd" 2>&1); rc=$?
printf 'wd-list rc=%s last=[%s] unsupported_line=%s\n' "$rc" "$(printf '%s\n' "$out" | tail -1)" "$(printf '%s\n' "$out" | grep -c '^UNSUPPORTED a Moved ')"
# CI 파일 없음
mkdir -p "$T/none"
out=$(bash "$C" --list "$T/none" 2>&1); rc=$?
printf 'none-list rc=%s\n' "$rc"
# 실제 실행 — 하나는 통과, 하나는 7 로 끝남
wf two <<'Y'
jobs:
  a:
    runs-on: ubuntu-latest
    steps:
      - name: Good
        run: echo ok
      - name: Bad
        run: exit 7
Y
out=$(bash "$C" "$T/two" 2>&1); rc=$?
printf 'two-run rc=%s last=[%s] fail_line=%s pass_line=%s\n' "$rc" "$(printf '%s\n' "$out" | tail -1)" \
  "$(printf '%s\n' "$out" | grep -c '^FAIL a Bad rc=7$')" "$(printf '%s\n' "$out" | grep -c '^PASS a Good rc=0$')"
