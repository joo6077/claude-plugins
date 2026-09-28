#!/usr/bin/env bash
# scripts/ci-local.sh 를 손으로 답을 아는 작은 CI 파일 넷과 CI 파일 없는 폴더에 돌려 출력 전체와 종료 코드를 맞댄다.
# 계약 after-0928-harness-checks 의 SC-11 · SC-12 · ER-02 를 따른다. CI_LOCAL 로 대상 스크립트를 바꿀 수 있다.

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
target=${CI_LOCAL:-$here/ci-local.sh}
[ -f "$target" ] || { echo "대상 스크립트가 없다: $target" >&2; exit 2; }
command -v python3 >/dev/null 2>&1 || { echo "python3 가 없다" >&2; exit 2; }

work=$(mktemp -d "${TMPDIR:-/tmp}/ci-local-test.XXXXXX") || exit 2
trap 'rm -rf "$work"' EXIT
fails=0

check() {  # check <이름> <기대> <실제>
  if [ "$2" = "$3" ]; then echo "PASS $1"; else printf 'FAIL %s\n기대:\n%s\n실제:\n%s\n' "$1" "$2" "$3"; fails=$((fails + 1)); fi
}
workflow() {  # workflow <폴더 이름> — stdin 을 그 폴더의 CI 파일로 쓴다
  mkdir -p "$work/$1/.github/workflows" && cat >"$work/$1/.github/workflows/ci.yml"
}

# 실제 실행 — 통과 하나 · 7 로 끝나는 단계 하나. uses 만 있는 단계는 run 단계가 아니라 세지 않는다
workflow two <<'YAML'
jobs:
  a:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - name: Good
        run: echo ok
      - name: Bad
        run: |
          echo 실패 전 줄
          exit 7
YAML
out=$(bash "$target" "$work/two" 2>&1); rc=$?
check 실행-통과하나실패하나 "$(printf '%s\n' "PASS a Good rc=0" "FAIL a Bad rc=7" "    실패 전 줄" \
  "steps=2 run=2 skip=0 unsupported=0 failed=1" "rc=1")" "$out
rc=$rc"

# 목록 — 준비 단계는 건너뛰고, job 이 둘이어도 차례대로 읽는다. 실행하지 않는다
workflow list <<'YAML'
jobs:
  first:
    runs-on: ubuntu-latest
    steps:
      - name: Install Python dependencies
        run: pip install pyyaml
      - name: Would fail
        run: exit 9
  second:
    runs-on: ubuntu-latest
    steps:
      - name: Install dependencies
        run: npm ci
      - name: Check
        run: echo check
YAML
out=$(bash "$target" --list "$work/list" 2>&1); rc=$?
check 목록-준비단계건너뜀 "$(printf '%s\n' \
  "SKIP first Install Python dependencies (준비 단계 — 로컬에는 미리 해 둔다)" \
  "RUN first Would fail" \
  "SKIP second Install dependencies (준비 단계 — 로컬에는 미리 해 둔다)" \
  "RUN second Check" \
  "steps=4 run=2 skip=2 unsupported=0" "rc=0")" "$out
rc=$rc"

# 실행 폴더를 바꾸는 단계 — 흉내 내지 않고 알린 뒤 1
workflow wd <<'YAML'
jobs:
  a:
    runs-on: ubuntu-latest
    steps:
      - name: Plain
        run: echo ok
      - name: Moved
        working-directory: sub
        run: echo moved
YAML
out=$(bash "$target" --list "$work/wd" 2>&1); rc=$?
check 못다루는열쇠 "$(printf '%s\n' "RUN a Plain" "UNSUPPORTED a Moved (다루지 않는 열쇠: working-directory)" \
  "steps=2 run=1 skip=0 unsupported=1" "rc=1")" "$out
rc=$rc"

# CI 파일이 없는 폴더 — 단계 0 으로 통과시키면 안 된다
mkdir -p "$work/none"
bash "$target" --list "$work/none" >/dev/null 2>&1; rc=$?
check CI파일없음 "rc=2" "rc=$rc"

echo "실패 $fails 건"
[ "$fails" = 0 ]
