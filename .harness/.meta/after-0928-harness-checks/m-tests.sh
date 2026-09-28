#!/usr/bin/env bash
# m-tests.sh <레포> <옛 판> — 새 시험 셋을 그대로 한 번, 대상을 망가뜨린 사본에서 한 번 돌린다.
# 망가뜨리기: superseded 확인 스크립트 → 늘 0 으로 끝나는 가짜 · 판정 표 사본 검사 → 옛 판 것 · 로컬 CI 도구 → 아무것도 안 하는 가짜.
# 사본은 레포의 추적 파일 + 추적 전 새 파일(.harness 제외)을 담는다. 줄마다 `<시험> <그대로|망가뜨림> rc=<종료 코드> broken=<대상이 바뀌었는지 1|0>`
R=${1:?레포}; OLD=${2:?옛 판}
T=$(mktemp -d "${TMPDIR:-/tmp}/mtests.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT
copy() {
  mkdir -p "$1"
  (cd "$R" && { git ls-files; git ls-files --others --exclude-standard; } | grep -v '^\.harness/' | while IFS= read -r f; do [ -f "$f" ] && printf '%s\0' "$f"; done | xargs -0 tar -cf -) | tar -xf - -C "$1"
}
one() {  # one <이름> <시험 명령(사본 루트 기준)> <대상 경로> <망가뜨리는 방법: stub0|stubnoop|old>
  c=$T/$1-ok; copy "$c"
  (cd "$c" && TMPDIR=$T eval "$2") >/dev/null 2>&1; printf '%s 그대로 rc=%s broken=0\n' "$1" "$?"
  b=$T/$1-bad; copy "$b"
  before=$(shasum -a 256 "$b/$3" 2>/dev/null | cut -c1-16)
  case $4 in
    stub0) printf '#!/usr/bin/env bash\necho "checked=0 violations=0"\nexit 0\n' > "$b/$3" ;;
    stubnoop) printf '#!/usr/bin/env bash\nexit 0\n' > "$b/$3" ;;
    old) git -C "$R" show "$OLD:$3" > "$b/$3" ;;
  esac
  after=$(shasum -a 256 "$b/$3" | cut -c1-16)
  (cd "$b" && TMPDIR=$T eval "$2") >/dev/null 2>&1; rc=$?
  printf '%s 망가뜨림 rc=%s broken=%s\n' "$1" "$rc" "$([ "$before" != "$after" ] && echo 1 || echo 0)"
}
one superseded 'bash harness/evals/superseded/check-superseded-test.sh' harness/scripts/check-superseded.sh stub0
one cause 'python3 scripts/test-check-cause-table-copies.py' scripts/check-cause-table-copies.py old
one cilocal 'bash scripts/test-ci-local.sh' scripts/ci-local.sh stubnoop
