#!/usr/bin/env bash
# upgrade-playwright-toolkit.sh 시험 — 계약 flutter-toolkit-playwright-upgrade 스크립트-01~07 · 오류-01.
# 가짜 git · fvm · flutter 가 받은 인자를 기록 파일에 한 줄씩 적는다. 기록과 표준 출력으로 판정한다.
# 다른 훅 사본으로 돌리기: UPGRADE_PLAYWRIGHT_TOOLKIT_HOOK=<사본 경로> bash upgrade-playwright-toolkit-test.sh
# 변이 확인: bash upgrade-playwright-toolkit-test.sh --mutations — 망가뜨린 사본마다 해당 조건이 FAIL 해야 한다
# prep_* 함수는 case03 이 이름으로 넘겨받아 부른다 — shellcheck 은 간접 호출을 못 본다
# shellcheck disable=SC2329

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
HOOK=${UPGRADE_PLAYWRIGHT_TOOLKIT_HOOK:-$HERE/../../scripts/upgrade-playwright-toolkit.sh}
unset FLUTTER_TOOLKIT_PLAYWRIGHT_UPGRADE FLUTTER_TOOLKIT_PLAYWRIGHT_UPGRADE_TTL CLAUDE_PROJECT_DIR

[ -f "$HOOK" ] || { echo "FAIL: 훅이 없다 — $HOOK"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "FAIL: 시각 조작에 쓸 python3 가 없다"; exit 1; }

if [ "${1:-}" = "--mutations" ]; then
  MUT=$(mktemp -d)
  trap 'rm -rf "$MUT"' EXIT
  NAMES=()
  # mutate <이름> <FAIL 해야 할 조건(쉼표)> <파이썬 치환식> — 사본마다 따로 돌려 결과를 파일에 남긴다
  mutate() {
    NAMES+=("$1")
    judge_mutant "$@" > "$MUT/$1.verdict" 2>&1 &
  }
  judge_mutant() {
    local name=$1 labels=$2 code=$3 copy=$MUT/$1.sh out label survived=0
    cp "$HOOK" "$copy"
    if ! python3 -I -c "import sys
path=sys.argv[1]; text=open(path,encoding='utf-8').read()
def rep(old,new):
    global text
    if old not in text: sys.exit(3)
    text=text.replace(old,new,1)
$code
open(path,'w',encoding='utf-8').write(text)" "$copy"; then
      echo "BROKEN $name — 치환할 글자를 훅에서 못 찾았다"; return
    fi
    out=$(UPGRADE_PLAYWRIGHT_TOOLKIT_HOOK=$copy bash "${BASH_SOURCE[0]}" 2>&1)
    IFS=, read -ra expected <<<"$labels"
    for label in "${expected[@]}"; do
      grep -qx "FAIL $label" <<<"$out" || survived=1
    done
    if [ "$survived" = 0 ]; then echo "KILLED $name"; else echo "SURVIVED $name ($labels)"; fi
  }
  # 치환할 글자는 훅 원문 그대로라 변수를 펼치면 안 된다
  # shellcheck disable=SC2016
  WORKER='  ( detach bash "$0" --worker "$dir" "$prefix" "$from" "$to" ) </dev/null >/dev/null 2>&1 &\n'
  # shellcheck disable=SC2016
  RESULT='  if [ -f "$prefix.result" ]; then\n    cat "$prefix.result"\n    rm -f "$prefix.result"\n  fi\n'
  mutate no-upgrade 스크립트-01-fvm "rep('$WORKER','  : &\n')"
  mutate double-upgrade 스크립트-01-fvm "rep('  (cd \"\$dir\" && \$cmd) </dev/null >\"\$prefix.log\" 2>&1\n','  (cd \"\$dir\" && \$cmd) </dev/null >\"\$prefix.log\" 2>&1\n  (cd \"\$dir\" && \$cmd) </dev/null >>\"\$prefix.log\" 2>&1\n')"
  mutate string-compare 스크립트-02a "rep('  local IFS=.\n  # shellcheck disable=SC2086\n  set -- \$1\n  printf \\'%05d%05d%05d\\' \"\$1\" \"\$2\" \"\$3\"\n','  printf \\'%s\\' \"\$1\"\n')"
  mutate keep-prerelease 스크립트-02c "rep('^[0-9]+\\\\.[0-9]+\\\\.[0-9]+\$ ]]','^[0-9]+\\\\.[0-9]+\\\\.[0-9]+ ]]')"
  mutate ignore-range 스크립트-02d "rep('  upper=\$(range_upper \"\$2\")\n','  upper=\"\"\n')"
  mutate always-behind 스크립트-02b "rep('  [[ \"\$(version_key \"\$to\")\" > \"\$(version_key \"\$from\")\" ]] || return 0\n','')"
  mutate no-tag-pattern-check 스크립트-03b,스크립트-03c "rep('[ \"\$git\" = 1 ] && [ \"\$tag\" = 1 ] && [ \"\$ref\" != 1 ] && [ -n \"\$url\" ] || return 0','true')"
  mutate no-off-switch 스크립트-03e "rep('[ \"\${FLUTTER_TOOLKIT_PLAYWRIGHT_UPGRADE:-on}\" = \"off\" ] && exit 0\n','')"
  mutate no-lock-check 스크립트-03f "rep('  [ -f \"\$dir/pubspec.lock\" ] || return 0\n',''); rep('  [ -n \"\$from\" ] || return 0\n','')"
  mutate no-depth-limit 스크립트-04 "rep('-maxdepth 3','-maxdepth 9')"
  mutate no-skip-dirs 스크립트-04 "rep('-name build -o -name .dart_tool -o','-name nosuch1 -o -name nosuch2 -o')"
  mutate no-ttl 스크립트-05a "rep('  if [ -f \"\$prefix.checked\" ] && [ \$(( \$(date +%s) - \$(modified_at \"\$prefix.checked\") )) -lt \"\$TTL\" ]; then','  if false; then')"
  mutate no-stamp-on-failure 스크립트-05c "rep('  : > \"\$prefix.checked\"\n',''); rep('  kill \"\$guard\" 2>/dev/null\n\n','  kill \"\$guard\" 2>/dev/null\n  : > \"\$prefix.checked\"\n\n')"
  mutate ignore-running 스크립트-06a "rep('    if [ -n \"\$pid\" ] && kill -0 \"\$pid\" 2>/dev/null; then return 0; fi\n','')"
  mutate trust-stale-running 스크립트-06b "rep('    if [ -n \"\$pid\" ] && kill -0 \"\$pid\" 2>/dev/null; then return 0; fi\n','    return 0\n')"
  mutate result-after-ttl 스크립트-06c "rep('$RESULT',''); rep('  : > \"\$prefix.checked\"\n','  : > \"\$prefix.checked\"\n$RESULT')"
  mutate keep-result 스크립트-06c "rep('    rm -f \"\$prefix.result\"\n','')"
  mutate foreground-upgrade 스크립트-07a "rep('$WORKER','  ( detach bash \"\$0\" --worker \"\$dir\" \"\$prefix\" \"\$from\" \"\$to\" ) </dev/null >/dev/null 2>&1\n')"
  mutate no-git-timeout 스크립트-07b "rep('GIT_LIMIT=10','GIT_LIMIT=100')"
  mutate failure-as-success 오류-01a "rep('  if [ \"\$rc\" -eq 0 ] && [ \"\$now\" = \"\$to\" ]; then','  if true; then')"
  wait
  ALL_KILLED=1
  for name in "${NAMES[@]}"; do
    cat "$MUT/$name.verdict"
    grep -q "^KILLED $name$" "$MUT/$name.verdict" || ALL_KILLED=0
  done
  if [ "$ALL_KILLED" = 1 ]; then echo "MUTATIONS PASS"; exit 0; fi
  echo "MUTATIONS FAIL"; exit 1
fi

WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
FAKE_BIN=$WORK/fake-bin
mkdir -p "$FAKE_BIN"
export FAKE_LOG=$WORK/calls.log

cat > "$FAKE_BIN/git" <<'EOF'
#!/usr/bin/env bash
echo "git GTP=${GIT_TERMINAL_PROMPT:-unset} $*" >> "$FAKE_LOG"
[ -n "${FAKE_GIT_SLEEP:-}" ] && exec sleep "$FAKE_GIT_SLEEP"
for t in ${FAKE_TAGS:-}; do printf '%040d\trefs/tags/toolkit-v%s\n' 0 "$t"; done
exit "${FAKE_GIT_RC:-0}"
EOF
for tool in fvm flutter; do
  cat > "$FAKE_BIN/$tool" <<EOF
#!/usr/bin/env bash
echo "$tool \$* @\$PWD" >> "\$FAKE_LOG"
[ -n "\${FAKE_UPGRADE_SLEEP:-}" ] && sleep "\$FAKE_UPGRADE_SLEEP"
if [ "\${FAKE_UPGRADE_RC:-0}" = 0 ] && [ -n "\${FAKE_UPGRADE_TO:-}" ] && [ -f pubspec.lock ]; then
  python3 -I -c "import re,sys
path='pubspec.lock'; text=open(path).read()
text=re.sub(r'(  flutter_playwright_toolkit:\n(?:    .*\n|      .*\n)*?    version: )\"[^\"]*\"', r'\\\\g<1>\"'+sys.argv[1]+'\"', text)
open(path,'w').write(text)" "\$FAKE_UPGRADE_TO"
fi
exit "\${FAKE_UPGRADE_RC:-0}"
EOF
done
chmod 755 "$FAKE_BIN"/*

hash_path() {
  if command -v shasum >/dev/null 2>&1; then printf '%s' "$1" | shasum -a 256 | cut -c1-16
  else printf '%s' "$1" | sha256sum | cut -c1-16
  fi
}

# make_project <폴더> <tag|path|ref|none> <잠금 판, 빈 값이면 잠금 파일 없음> [범위] [fvm]
make_project() {
  local dir=$1 kind=$2 lock=$3 range=${4:-} fvm=${5:-}
  mkdir -p "$dir"
  {
    printf 'name: app\nenvironment:\n  sdk: ^3.9.0\ndependencies:\n  flutter:\n    sdk: flutter\n'
    case "$kind" in
      tag) printf '  flutter_playwright_toolkit:\n    git:\n      url: https://example.invalid/flutter_playwright.git\n      path: packages/flutter_playwright_toolkit\n      tag_pattern: toolkit-v{{version}}\n' ;;
      ref) printf '  flutter_playwright_toolkit:\n    git:\n      url: https://example.invalid/flutter_playwright.git\n      path: packages/flutter_playwright_toolkit\n      ref: toolkit-v0.17.0\n' ;;
      path) printf '  flutter_playwright_toolkit:\n    path: ../flutter_playwright_toolkit\n' ;;
      none) ;;
    esac
    [ -n "$range" ] && printf "    version: '%s'\n" "$range"
    printf 'dev_dependencies:\n  flutter_test:\n    sdk: flutter\n'
  } > "$dir/pubspec.yaml"
  if [ -n "$lock" ]; then
    cat > "$dir/pubspec.lock" <<EOF
# Generated by pub
# See https://dart.dev/tools/pub/glossary#lockfile
packages:
  async:
    dependency: transitive
    description:
      name: async
      sha256: "758e6d74e971c3e5aceb4110bfd6698efc7f501675bcfe0c775459a8140750eb"
      url: "https://pub.dev"
    source: hosted
    version: "2.13.0"
  flutter_playwright_toolkit:
    dependency: "direct main"
    description:
      path: "packages/flutter_playwright_toolkit"
      resolved-ref: "4856ee047efa59ff4f098a1ff2b9016d659cbbc2"
      tag-pattern: "toolkit-v{{version}}"
      url: "https://example.invalid/flutter_playwright.git"
    source: git
    version: "$lock"
sdks:
  dart: ">=3.9.0 <4.0.0"
  flutter: ">=3.18.0"
EOF
  fi
  [ -n "$fvm" ] && printf '{"flutter": "stable"}\n' > "$dir/.fvmrc"
  return 0
}

STATE=""
OUT=""
RC=0
ELAPSED=0
new_case() { # new_case <이름> — 새 세션 폴더 · 상태 폴더 · 기록
  ROOT=$WORK/$1/root
  STATE=$WORK/$1/state
  mkdir -p "$ROOT" "$STATE"
  : > "$FAKE_LOG"
}
run_hook() { # run_hook [VAR=값 ...]
  local start
  start=$(date +%s)
  OUT=$(cd "$ROOT" && printf '{"hook_event_name":"SessionStart","cwd":"%s"}' "$ROOT" \
    | env PATH="$FAKE_BIN:$PATH" FLUTTER_TOOLKIT_PLAYWRIGHT_UPGRADE_STATE="$STATE" "$@" bash "$HOOK" 2>/dev/null)
  RC=$?
  ELAPSED=$(( $(date +%s) - start ))
}
alive_running() {
  local marker pid
  while IFS= read -r marker; do
    pid=$(cat "$marker" 2>/dev/null)
    [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null && return 0
  done < <(find "$STATE" -name '*.running' 2>/dev/null)
  return 1
}
settle() { # 뒤쪽 프로세스가 끝날 때까지(최대 15 초). 시작하지 않았으면 2 초 더 본다
  for _ in $(seq 1 75); do
    alive_running || break
    sleep 0.2
  done
  [ -n "$(find "$STATE" -name '*.done' 2>/dev/null)" ] || sleep 2
}
upgrades() { grep -c 'pub upgrade flutter_playwright_toolkit' "$FAKE_LOG"; }
lookups() { grep -c '^git ' "$FAKE_LOG"; }
lines() { if [ -z "$OUT" ]; then echo 0; else grep -c '' <<<"$OUT"; fi; }
backdate() { python3 -I -c 'import os,sys,time; t=time.time()-int(sys.argv[2]); os.utime(sys.argv[1],(t,t))' "$1" "$2"; }

TOTAL=0
BAD=0
verdict() { # verdict <라벨> <조건식 결과 0/1> <설명>
  TOTAL=$((TOTAL + 1))
  if [ "$2" = 0 ]; then echo "OK   $1"; else BAD=$((BAD + 1)); echo "FAIL $1"; echo "     $3"; fi
}
expect() { # expect <라벨> <설명> <조건 명령...>
  local label=$1 why=$2; shift 2
  if "$@"; then verdict "$label" 0 ""; else verdict "$label" 1 "$why"; fi
}

# 01 — 뒤처진 프로젝트를 올린다 (fvm · 일반)
for flavor in fvm flutter; do
  new_case "01-$flavor"
  make_project "$ROOT" tag 0.17.0 "" "$([ $flavor = fvm ] && echo yes)"
  run_hook FAKE_TAGS="0.17.0 0.18.0" FAKE_UPGRADE_TO=0.18.0
  first_out=$OUT first_rc=$RC
  settle
  want="$flavor pub upgrade flutter_playwright_toolkit @$ROOT"
  [ "$flavor" = fvm ] && want="fvm flutter pub upgrade flutter_playwright_toolkit @$ROOT"
  expect "스크립트-01-$flavor" "rc=$first_rc 출력=[$first_out] 올리기=$(upgrades) 기록=$(cat "$FAKE_LOG")" \
    test "$first_rc" = 0 -a "$(OUT=$first_out lines)" = 1 \
      -a -n "$(grep -F 0.17.0 <<<"$first_out" | grep -F 0.18.0)" \
      -a "$(upgrades)" = 1 -a "$(grep -cxF "$want" "$FAKE_LOG")" = 1 \
      -a "$(grep -c '^git GTP=0 ' "$FAKE_LOG")" = 1
done

# 02 — 판 비교
case02() { # case02 <라벨> <잠금> <태그들> <범위> <올리기 기대> <출력에 들어갈 판, 빈 값이면 출력 0 글자>
  new_case "$1"
  make_project "$ROOT" tag "$2" "$4"
  run_hook FAKE_TAGS="$3"
  settle
  if [ -n "$6" ]; then
    expect "$1" "올리기=$(upgrades) 출력=[$OUT]" test "$(upgrades)" = "$5" -a -n "$(grep -F "$6" <<<"$OUT")" -a "$RC" = 0
  else
    expect "$1" "올리기=$(upgrades) 출력=[$OUT]" test "$(upgrades)" = "$5" -a -z "$OUT" -a "$RC" = 0
  fi
}
case02 스크립트-02a 0.9.0 "0.9.0 0.10.0" "" 1 0.10.0
case02 스크립트-02b 0.18.0 "0.18.0" "" 0 ""
case02 스크립트-02c 0.18.0 "0.18.0 0.19.0-dev" "" 0 ""
case02 스크립트-02d 0.18.0 "0.18.0 1.0.0" ">=0.11.0 <1.0.0" 0 ""

# 03 — 손대지 않는 여섯 경우. 각 경우와 한 가지만 다른 짝은 올린다
quiet() { test "$(lookups)" = 0 -a "$(upgrades)" = 0 -a -z "$OUT" -a "$RC" = 0; }
prep_none() { make_project "$ROOT" none 0.17.0; }
prep_path() { make_project "$ROOT" path 0.17.0; }
prep_ref() { make_project "$ROOT" ref 0.17.0; }
prep_tag() { make_project "$ROOT" tag 0.17.0; }
prep_deep() { make_project "$ROOT/a/b/c" tag 0.17.0; }
prep_shallow() { make_project "$ROOT/a" tag 0.17.0; }
prep_nolock() { make_project "$ROOT" tag ""; }
case03() { # case03 <라벨> <대상 준비 함수> <짝 준비 함수> [대상 환경]
  local label=$1 target=$2 partner=$3 env=${4:-}
  new_case "$label"
  "$target"
  # shellcheck disable=SC2086
  run_hook FAKE_TAGS="0.17.0 0.18.0" $env
  settle
  local target_ok=1 pair_ok=1
  quiet && target_ok=0
  new_case "$label-pair"
  "$partner"
  run_hook FAKE_TAGS="0.17.0 0.18.0"
  settle
  test "$(upgrades)" = 1 && pair_ok=0
  verdict "$label" $((target_ok | pair_ok)) "대상 조용함=$([ $target_ok = 0 ] && echo 예 || echo 아니오) 짝 올림=$([ $pair_ok = 0 ] && echo 예 || echo 아니오)"
}
case03 스크립트-03a prep_none prep_tag
case03 스크립트-03b prep_path prep_tag
case03 스크립트-03c prep_ref prep_tag
case03 스크립트-03d prep_deep prep_shallow
case03 스크립트-03e prep_tag prep_tag FLUTTER_TOOLKIT_PLAYWRIGHT_UPGRADE=off
case03 스크립트-03f prep_nolock prep_tag

# 04 — 찾는 범위
new_case 04
for d in app packages/x a/b/c build .dart_tool; do make_project "$ROOT/$d" tag 0.17.0; done
run_hook FAKE_TAGS="0.17.0 0.18.0"
settle
got=$(sed -n 's/.* @//p' "$FAKE_LOG" | sed "s#^$ROOT/##" | LC_ALL=C sort | tr '\n' ' ')
expect 스크립트-04 "올린 폴더=[$got]" test "$got" = "app packages/x "

# 05 — 확인 주기
new_case 05
make_project "$ROOT" tag 0.17.0
KEY=$STATE/$(hash_path "$ROOT")
run_hook FAKE_TAGS="0.17.0 0.18.0" FAKE_UPGRADE_TO=0.18.0
settle
: > "$FAKE_LOG"
run_hook FAKE_TAGS="0.17.0 0.18.0" FLUTTER_TOOLKIT_PLAYWRIGHT_UPGRADE_TTL=3600
settle
expect 스크립트-05a "조회=$(lookups)" test "$(lookups)" = 0
: > "$FAKE_LOG"
backdate "$KEY.checked" 7200
run_hook FAKE_TAGS="0.17.0 0.18.0" FLUTTER_TOOLKIT_PLAYWRIGHT_UPGRADE_TTL=3600
settle
expect 스크립트-05b "조회=$(lookups)" test "$(lookups)" = 1
new_case 05c
make_project "$ROOT" tag 0.17.0
KEY=$STATE/$(hash_path "$ROOT")
run_hook FAKE_GIT_RC=128
settle
first=$(lookups)
: > "$FAKE_LOG"
run_hook FAKE_TAGS="0.17.0 0.18.0"
settle
expect 스크립트-05c "첫 조회=$first 둘째 조회=$(lookups) 확인 기록=$([ -f "$KEY.checked" ] && echo 있음 || echo 없음)" \
  test "$first" = 1 -a "$(lookups)" = 0 -a -f "$KEY.checked"

# 06 — 진행 중 · 결과 알림
new_case 06a
make_project "$ROOT" tag 0.17.0
KEY=$STATE/$(hash_path "$ROOT")
sleep 30 &
LIVE=$!
echo "$LIVE" > "$KEY.running"
run_hook FAKE_TAGS="0.17.0 0.18.0"
sleep 2
expect 스크립트-06a "올리기=$(upgrades) 출력=[$OUT]" test "$(upgrades)" = 0 -a -z "$OUT"
kill "$LIVE" 2>/dev/null
wait "$LIVE" 2>/dev/null

new_case 06b
make_project "$ROOT" tag 0.17.0
KEY=$STATE/$(hash_path "$ROOT")
true &
DEAD=$!
wait "$DEAD"
echo "$DEAD" > "$KEY.running"
run_hook FAKE_TAGS="0.17.0 0.18.0" FAKE_UPGRADE_TO=0.18.0
settle
expect 스크립트-06b "올리기=$(upgrades)" test "$(upgrades)" = 1

new_case 06c
make_project "$ROOT" tag 0.18.0
KEY=$STATE/$(hash_path "$ROOT")
echo "flutter_playwright_toolkit 을 0.17.0 → 0.18.0 로 올렸다 ($ROOT)." > "$KEY.result"
: > "$KEY.checked"
run_hook FAKE_TAGS="0.18.0"
settle
first=$OUT
run_hook FAKE_TAGS="0.18.0"
settle
expect 스크립트-06c "첫 출력=[$first] 둘째 출력=[$OUT]" \
  test "$(OUT=$first lines)" = 1 -a -n "$(grep -F 0.18.0 <<<"$first")" -a -z "$OUT"

# 07 — 세션을 붙잡지 않는다
new_case 07a
make_project "$ROOT" tag 0.17.0
run_hook FAKE_TAGS="0.17.0 0.18.0" FAKE_UPGRADE_SLEEP=5
took=$ELAPSED
settle
expect 스크립트-07a "걸린 시간=${took}초" test "$took" -le 2
new_case 07b
make_project "$ROOT" tag 0.17.0
run_hook FAKE_GIT_SLEEP=60
took=$ELAPSED
settle
expect 스크립트-07b "걸린 시간=${took}초 올리기=$(upgrades) 출력=[$OUT]" \
  test "$took" -le 15 -a "$(upgrades)" = 0 -a -z "$OUT" -a "$RC" = 0

# 오류-01
new_case err-a
make_project "$ROOT" tag 0.17.0
run_hook FAKE_TAGS="0.17.0 0.18.0" FAKE_UPGRADE_RC=1
rc1=$RC
settle
run_hook FAKE_TAGS="0.17.0 0.18.0"
second=$OUT rc2=$RC
settle
run_hook FAKE_TAGS="0.17.0 0.18.0"
expect 오류-01a "둘째 출력=[$second] 셋째 출력=[$OUT] 종료 코드=$rc1,$rc2,$RC" \
  test "$(OUT=$second lines)" = 1 -a -n "$(grep -F 실패 <<<"$second" | grep -F 'flutter pub upgrade flutter_playwright_toolkit')" \
    -a -z "$OUT" -a "$rc1$rc2$RC" = 000
new_case err-b1
make_project "$ROOT" tag 0.17.0
run_hook FAKE_GIT_RC=128 FAKE_TAGS="0.18.0"
settle
expect 오류-01b1 "올리기=$(upgrades) 출력=[$OUT] 종료 코드=$RC" test "$(upgrades)" = 0 -a -z "$OUT" -a "$RC" = 0
new_case err-b2
make_project "$ROOT" tag 0.17.0
run_hook FAKE_TAGS=""
settle
expect 오류-01b2 "올리기=$(upgrades) 출력=[$OUT] 종료 코드=$RC" test "$(upgrades)" = 0 -a -z "$OUT" -a "$RC" = 0

echo "---"
echo "$((TOTAL - BAD))/$TOTAL"
if [ "$BAD" = 0 ]; then echo "PASS"; exit 0; fi
echo "FAIL"
exit 1
