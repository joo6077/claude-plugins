# shellcheck shell=bash
# 계약 측정 공통 정의. bash · zsh 에서 `.` 로 읽는다: . harness/scripts/measure-common.sh
#
# 계약 규약의 함수 아홉(fm_get · sha256_16 · contract_digest · verify_seal · measurement_digest ·
# verify_measurement · sprint_head · mine · unsigned_on)은 사본을 두지 않고 규약 문서의 bash 블록을 읽어 정의한다.
# 사본을 두면 규약이 바뀐 뒤 측정만 옛 정의로 돈다.
# 규약 문서는 MEASURE_SCHEMA 로 바꿀 수 있다 (기본: 이 파일 옆 ../references/contract-schema.md).
#
# 규약 문서가 없거나 함수 하나라도 못 찾으면 `.` 가 2 를 돌려주고 stderr 에 그 이름을 적는다.

if [ -n "${BASH_SOURCE[0]:-}" ]; then _mc_self=${BASH_SOURCE[0]}; else _mc_self=$0; fi
_mc_schema=${MEASURE_SCHEMA:-$(cd "$(dirname "$_mc_self")/../references" 2>/dev/null && pwd)/contract-schema.md}
if [ ! -f "$_mc_schema" ]; then
  echo "measure-common: 계약 규약 문서가 없다: $_mc_schema" >&2
  unset _mc_self _mc_schema
  return 2
fi

eval "$(awk '/^```bash$/ { f = 1; buf = ""; next }
  f && /^```$/ { if (buf ~ /(fm_get|sha256_16|sprint_head|mine)\(\) \{/) printf "%s", buf; f = 0; next }
  f { buf = buf $0 "\n" }' "$_mc_schema")"

_mc_missing=""
for _mc_fn in fm_get sha256_16 contract_digest verify_seal measurement_digest verify_measurement sprint_head mine unsigned_on; do
  type "$_mc_fn" >/dev/null 2>&1 || _mc_missing="$_mc_missing $_mc_fn"
done
if [ -n "$_mc_missing" ]; then
  echo "measure-common: 계약 규약에서 함수를 못 찾았다:$_mc_missing ($_mc_schema)" >&2
  unset _mc_self _mc_schema _mc_missing _mc_fn
  return 2
fi
unset _mc_self _mc_schema _mc_missing _mc_fn

scratch_dir() {  # scratch_dir [접두] — 새 임시 폴더 경로를 낸다. 지우는 것은 부른 쪽 몫이다
  mktemp -d "${TMPDIR:-/tmp}/${1:-measure}.XXXXXX"
}

unpack_rev() {  # unpack_rev <판> <폴더> — 그 판의 파일을 폴더에 푼다. 작업 폴더의 미커밋 변경이 끼지 않는다
  # 파이프만 쓰면 tar 의 종료 코드가 남아 없는 판을 풀어도 0 이 된다 — 판부터 확인한다
  git rev-parse --verify -q "$1^{commit}" >/dev/null || { echo "unpack_rev: 판을 못 찾았다: $1" >&2; return 2; }
  mkdir -p "$2" || return 2
  git archive "$1" | tar -x -C "$2" || return 2
}

need_fn() {  # need_fn <함수…> — 하나라도 정의돼 있지 않으면 이름을 적고 2
  _mc_rc=0
  for _mc_fn in "$@"; do
    type "$_mc_fn" >/dev/null 2>&1 || { echo "need_fn: 정의되지 않았다: $_mc_fn" >&2; _mc_rc=2; }
  done
  unset _mc_fn
  return "$_mc_rc"
}

sect() {  # sect <파일> <제목 앞부분> — 그 제목부터 같은 깊이 이하 다음 제목 전까지. 코드 펜스 안 # 줄은 제목이 아니다
  awk -v h="$2" '
    /^[[:space:]]*(```|~~~)/ { fence = !fence }
    !f && !fence && index($0, h) == 1 { f = 1; lvl = match($0, /[^#]/) - 1; print; next }
    f && !fence && /^#+ / { l = match($0, /[^#]/) - 1; if (l <= lvl) exit }
    f' "$1"
}
