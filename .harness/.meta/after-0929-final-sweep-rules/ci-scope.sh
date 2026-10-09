#!/usr/bin/env bash
# ci-scope.sh <ci-local.sh 경로> — 작업 전체 · 워크플로 전체에 걸린 if · env · defaults 를 ci-local.sh 가 어떻게 다루는지 잰다.
# 작은 CI 파일 넷을 임시 폴더에 만들어 실제로 돌리고(목록만이 아니라 실행), 사례마다 출력 전체와 종료 코드를 찍는다.
# 사례: job(작업 열쇠 defaults · env · if) · wf-env(워크플로 env) · wf-defaults(워크플로 defaults) · plain(runs-on · needs · timeout-minutes 만)
target=${1:?ci-local.sh 경로}
[ -f "$target" ] || { echo "대상이 없다: $target" >&2; exit 2; }
work=$(mktemp -d "${TMPDIR:-/tmp}/ci-scope.XXXXXX") || exit 2
trap 'rm -rf "$work"' EXIT
wf() { mkdir -p "$work/$1/.github/workflows" "$work/$1/sub" && cat >"$work/$1/.github/workflows/ci.yml"; }

wf job <<'YAML'
jobs:
  a:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: sub
    env:
      MUST: "yes"
    steps:
      - name: Where
        run: test "$(basename "$PWD")" = sub && test "$MUST" = yes
  b:
    runs-on: ubuntu-latest
    if: false
    steps:
      - name: Never
        run: exit 3
  c:
    runs-on: ubuntu-latest
    steps:
      - name: Plain
        run: echo ok
YAML
wf wf-env <<'YAML'
env:
  MUST: "yes"
jobs:
  a:
    runs-on: ubuntu-latest
    steps:
      - name: One
        run: test "$MUST" = yes
YAML
wf wf-defaults <<'YAML'
defaults:
  run:
    working-directory: sub
jobs:
  a:
    runs-on: ubuntu-latest
    steps:
      - name: One
        run: test "$(basename "$PWD")" = sub
YAML
wf plain <<'YAML'
jobs:
  a:
    name: First
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - name: One
        run: echo one
  b:
    runs-on: ubuntu-latest
    needs: a
    steps:
      - name: Two
        run: echo two
YAML
for c in job wf-env wf-defaults plain; do
  echo "== $c"
  bash "$target" "$work/$c" 2>&1
  echo "rc=$?"
done
