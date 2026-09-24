#!/usr/bin/env bash
# format-edited-dart.sh 시험 — 계약 SC-04 ①~⑧ · ER-01 (a)(b)(c).
# 가짜 fvm·dart 가 받은 인자를 [인자] 로 감싸 기록 파일에 한 줄씩 적는다. 기록으로 판정한다.
# 다른 훅 사본으로 돌리기: FORMAT_EDITED_DART_HOOK=<사본 경로> bash format-edited-dart-test.sh

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
HOOK=${FORMAT_EDITED_DART_HOOK:-$HERE/../../scripts/format-edited-dart.sh}
unset FLUTTER_TOOLKIT_FORMAT_ON_EDIT

command -v jq >/dev/null 2>&1 || { echo "FAIL: 시험 입력을 만들 jq 가 없다"; exit 1; }
[ -x "$HOOK" ] || { echo "FAIL: 훅이 없거나 실행 비트가 없다 — $HOOK"; exit 1; }

WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
LOG=$WORK/calls.log
FAKE_BIN=$WORK/fake-bin
NOJQ_BIN=$WORK/nojq-bin
mkdir -p "$FAKE_BIN" "$NOJQ_BIN"

for tool in fvm dart; do
  cat > "$FAKE_BIN/$tool" <<EOF
#!/usr/bin/env bash
printf '%s' '$tool' >> '$LOG'
for a in "\$@"; do printf ' [%s]' "\$a" >> '$LOG'; done
printf ' @%s\n' "\$PWD" >> '$LOG'
EOF
  chmod 755 "$FAKE_BIN/$tool"
  cp -p "$FAKE_BIN/$tool" "$NOJQ_BIN/$tool"
done
# jq 만 빠진 PATH. /usr/bin 을 통째로 넣으면 그 안의 jq 가 보인다
for tool in bash cat; do
  ln -s "$(command -v "$tool")" "$NOJQ_BIN/$tool"
done
if PATH=$NOJQ_BIN command -v jq >/dev/null 2>&1; then
  echo "FAIL: 전제 깨짐 — jq 를 뺀 PATH 에서 jq 가 보인다"; exit 1
fi

APP=$WORK/app
FVM_APP=$WORK/fvm-app
LOOSE=$WORK/loose
mkdir -p "$APP/lib" "$FVM_APP/lib" "$LOOSE/lib"
printf 'name: app\n' > "$APP/pubspec.yaml"
printf 'name: fvm_app\n' > "$FVM_APP/pubspec.yaml"
printf '{"flutter": "stable"}\n' > "$FVM_APP/.fvmrc"
for f in "$APP/lib/a.dart" "$APP/lib/b.dart" "$APP/lib/my file.dart" "$APP/lib/a.g.dart" \
         "$APP/lib/a.freezed.dart" "$APP/README.md" "$FVM_APP/lib/a.dart" "$LOOSE/lib/x.dart"; do
  printf 'void main(){}\n' > "$f"
done
d=$LOOSE
while [ -n "$d" ]; do
  [ -f "$d/pubspec.yaml" ] && { echo "FAIL: 전제 깨짐 — ⑦ 폴더의 조상에 pubspec.yaml 이 있다: $d"; exit 1; }
  d=${d%/*}
done

edit_input() { # edit_input <tool_name> <file_path>
  jq -cn --arg t "$1" --arg p "$2" --arg c "$WORK" \
    '{hook_event_name: "PostToolUse", tool_name: $t, cwd: $c,
      tool_input: {file_path: $p, old_string: "a", new_string: "b", content: "void main() {}\n"}}'
}

TOTAL=0
BAD=0
# check <라벨> <입력> <기대 기록(없으면 빈 문자열)> [PATH 값] [VAR=값 ...]
check() {
  local label=$1 input=$2 want_log=$3 path=${4:-$FAKE_BIN:$PATH}
  shift $(($# < 4 ? $# : 4))
  : > "$LOG"
  local out rc got_log want got
  out=$(printf '%s' "$input" | env PATH="$path" "$@" "$HOOK" 2>/dev/null)
  rc=$?
  got_log=$(cat "$LOG")
  want="exit 0 · stdout 0 글자 · 기록 $([ -n "$want_log" ] && echo 1 || echo 0)줄${want_log:+ $want_log}"
  got="exit $rc · stdout ${#out} 글자 · 기록 $(grep -c '' "$LOG")줄${got_log:+ $got_log}"
  TOTAL=$((TOTAL + 1))
  if [ "$want" = "$got" ]; then
    echo "OK   $label"
  else
    BAD=$((BAD + 1))
    echo "FAIL $label"
  fi
  echo "       기대 / $want"
  echo "       실제 / $got"
}

check "① Edit lib/a.dart" "$(edit_input Edit "$APP/lib/a.dart")" \
  "dart [format] [--] [$APP/lib/a.dart] @$APP"
check "② Write lib/b.dart" "$(edit_input Write "$APP/lib/b.dart")" \
  "dart [format] [--] [$APP/lib/b.dart] @$APP"
check "③ 공백 경로 lib/my file.dart" "$(edit_input Edit "$APP/lib/my file.dart")" \
  "dart [format] [--] [$APP/lib/my file.dart] @$APP"
check "④ .fvmrc 프로젝트" "$(edit_input Edit "$FVM_APP/lib/a.dart")" \
  "fvm [dart] [format] [--] [$FVM_APP/lib/a.dart] @$FVM_APP"
check "⑤ 생성물 lib/a.g.dart" "$(edit_input Edit "$APP/lib/a.g.dart")" ""
check "⑤ 생성물 lib/a.freezed.dart" "$(edit_input Write "$APP/lib/a.freezed.dart")" ""
check "⑥ README.md" "$(edit_input Edit "$APP/README.md")" ""
check "⑦ pubspec.yaml 없는 폴더" "$(edit_input Edit "$LOOSE/lib/x.dart")" ""
check "⑧ FLUTTER_TOOLKIT_FORMAT_ON_EDIT=off" "$(edit_input Edit "$APP/lib/a.dart")" "" \
  "$FAKE_BIN:$PATH" FLUTTER_TOOLKIT_FORMAT_ON_EDIT=off
check "ER-01 (a) 빈 stdin" "" ""
check "ER-01 (b) 깨진 JSON" "{깨진" ""
check "ER-01 (c) jq 없는 PATH" "$(edit_input Edit "$APP/lib/a.dart")" "" "$NOJQ_BIN"

echo "결과: $TOTAL 경우 중 불일치 $BAD"
[ "$BAD" -eq 0 ]
