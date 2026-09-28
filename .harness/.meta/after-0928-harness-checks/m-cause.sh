#!/usr/bin/env bash
# m-cause.sh <레포> — 판정 표 사본 검사를 다섯 경우의 임시 사본에 돌린다. 줄마다 `<경우> rc=<종료 코드> <요약 줄> mismatch=<MISMATCH 줄 수>`.
# 원문 = harness/skills/sprint/SKILL.md. 사본 둘은 그대로 둔다.
R=${1:?레포 경로}
T=$(mktemp -d "${TMPDIR:-/tmp}/mcause.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT
CANON=harness/skills/sprint/SKILL.md
case_run() {  # case_run <경우> <perl 치환식 또는 빈 값> <적용 확인용 grep 식> — applied 는 원문에서 그 식에 걸린 줄 수
  d=$T/$1; mkdir -p "$d"
  (cd "$R" && tar -cf - scripts harness/skills/sprint flutter-toolkit/skills/flutter-preflight react-kit/skills/react-preflight) | tar -xf - -C "$d"
  [ -n "$2" ] && perl -0pi -e "$2" "$d/$CANON"
  applied=$(grep -cE "$3" "$d/$CANON")
  out=$(python3 "$d/scripts/check-cause-table-copies.py" 2>&1); rc=$?
  printf '%s rc=%s %s mismatch=%s applied=%s\n' "$1" "$rc" "$(printf '%s\n' "$out" | tail -1)" "$(printf '%s\n' "$out" | grep -c '^MISMATCH ')" "$applied"
}
case_run a-unchanged '' '^판정 표와 두 경우는'
case_run b-bullet-after-last 's/(- \*\*미확정\*\*[^\n]*\n)/$1- **새 경우** — 원문에만 더한 줄\n/' '^- \*\*새 경우\*\*'
case_run c-para-before-note 's/(\n)(판정 표와 두 경우는)/$1**새 문단** — 원문에만 더한 문단\n\n$2/' '^\*\*새 문단\*\*'
case_run d-note-edited 's/판정 표와 두 경우는/판정 표와 두 경우는 (표지 문단 고침)/' '표지 문단 고침'
case_run e-note-removed 's/\n판정 표와 두 경우는[^\n]*\n/\n/' '^판정 표와 두 경우는'
