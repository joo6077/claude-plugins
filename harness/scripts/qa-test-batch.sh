#!/bin/bash
# 시험 묶어 재기 — 시험 파일마다 한 번만 돌리고, 지목한 시험 이름마다 판정을 한 줄씩 낸다.
# 규칙은 harness/references/contract-schema.md §측정 관례 > 시험 묶어 재기 에 있다. 여기서는 그 규칙을 실행만 한다.
#
# 쓰는 법: qa-test-batch.sh --out <기록 폴더> [--cmd '<실행기>'] [--fail-mark '<실패 표시>'] [-n '<시험 이름>']... <시험 파일>...
#   --cmd        파일 하나를 붙여 돌릴 명령. 기본: pubspec.yaml 이 있고 fvm 이 있으면 `fvm flutter test --reporter expanded`,
#                fvm 이 없으면 `flutter test --reporter expanded`. 그 밖의 실행기는 이름별 결과를 찍는 형식으로 직접 준다
#   --fail-mark  실패한 시험 줄에 붙는 글자. 기본 `[E]` (Flutter expanded 형식)
#   -n           판정할 시험 이름 (글자 그대로 찾되, 바로 뒤가 글자 · 숫자 · _ 인 자리는 다른 이름으로 본다). 여러 번 준다
#
# 출력 (화면에는 이것만):
#   FILE <파일> rc=<종료 코드> last=<마지막 진행 줄> log=<기록 경로>
#   NAME <이름> PASS lines=<줄 수>          — 이름 줄이 있고 그 줄 중 실패 표시가 0 개
#   NAME <이름> FAIL lines=<줄 수> failed=<실패 줄 수>
#   NAME <이름> MISSING                     — 어느 기록에도 그 이름이 0 번 (파일 통째 실행이 통과해도 FAIL 로 읽는다)
#   SUMMARY files=<수> file_fail=<rc≠0 파일 수> names=<수> pass=<수> fail=<수> missing=<수>
# 종료 코드: 실패 파일 · FAIL · MISSING 이 하나라도 있으면 1, 인자 오류면 2, 아니면 0.

set -u
OUT=""; CMD=""; MARK='[E]'; NAMES=(); FILES=()
while [ $# -gt 0 ]; do
  case "$1" in
    --out) OUT=${2:-}; shift 2 ;;
    --cmd) CMD=${2:-}; shift 2 ;;
    --fail-mark) MARK=${2:-}; shift 2 ;;
    -n) NAMES+=("${2:-}"); shift 2 ;;
    -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
    *) FILES+=("$1"); shift ;;
  esac
done
[ -n "$OUT" ] && [ ${#FILES[@]} -gt 0 ] || { echo "qa-test-batch: --out 과 시험 파일 1 개 이상이 필요하다" >&2; exit 2; }
if [ -z "$CMD" ]; then
  if [ -f pubspec.yaml ] && command -v fvm >/dev/null 2>&1; then CMD='fvm flutter test --reporter expanded'
  elif [ -f pubspec.yaml ]; then CMD='flutter test --reporter expanded'
  else echo "qa-test-batch: 실행기를 정할 수 없다 — --cmd 를 준다" >&2; exit 2; fi
fi
mkdir -p "$OUT" || exit 2

file_fail=0; i=0
for f in "${FILES[@]}"; do
  i=$((i + 1))
  log="$OUT/$i-$(basename "$f").log"
  # shellcheck disable=SC2086  # CMD 는 낱말로 쪼개져야 하는 명령이다
  $CMD "$f" > "$log.raw" 2>&1
  rc=$?
  # 색 코드와 줄 되돌림을 지운다 — 남겨 두면 한글 이름이 든 기록을 grep 이 바이너리로 보고 0 을 낸다
  LC_ALL=C sed -e $'s/\x1b\\[[0-9;]*[A-Za-z]//g' -e $'s/\r/\\\n/g' "$log.raw" > "$log" && rm -f "$log.raw"
  [ "$rc" -eq 0 ] || file_fail=$((file_fail + 1))
  # 끝 줄은 진행 줄(`00:04 +9: …`) 가운데 마지막 것 — 실패 뒤에는 오류 위치가 기록 끝에 붙는다
  last=$(LC_ALL=C grep -a -E '^[0-9]+:[0-9]+ \+' "$log" | tail -1 | cut -c1-120)
  [ -n "$last" ] || last=$(LC_ALL=C grep -a -v '^[[:space:]]*$' "$log" | tail -1 | cut -c1-120)
  echo "FILE $f rc=$rc last=$last log=$log"
done

pass=0; fail=0; missing=0
for n in ${NAMES[@]+"${NAMES[@]}"}; do
  # 이름 바로 뒤가 글자 · 숫자 · _ 면 다른 이름이다 — UI-01 을 찾을 때 UI-010 줄을 세지 않는다
  hits=$(cat "$OUT"/*.log | LC_ALL=C grep -a -E '^[0-9]+:[0-9]+ \+[0-9]+' | LC_ALL=C awk -v n="$n" '
    { s = $0; while ((i = index(s, n)) > 0) { c = substr(s, i + length(n), 1); if (c !~ /[A-Za-z0-9_]/) { print; next } s = substr(s, i + 1) } }')
  lines=$(printf '%s' "$hits" | grep -c .)
  if [ "$lines" -eq 0 ]; then missing=$((missing + 1)); echo "NAME $n MISSING"; continue; fi
  bad=$(printf '%s\n' "$hits" | LC_ALL=C grep -a -c -F -- "$MARK")
  if [ "$bad" -eq 0 ]; then pass=$((pass + 1)); echo "NAME $n PASS lines=$lines"
  else fail=$((fail + 1)); echo "NAME $n FAIL lines=$lines failed=$bad"; fi
done

echo "SUMMARY files=${#FILES[@]} file_fail=$file_fail names=${#NAMES[@]} pass=$pass fail=$fail missing=$missing"
[ "$file_fail" -eq 0 ] && [ "$fail" -eq 0 ] && [ "$missing" -eq 0 ]
