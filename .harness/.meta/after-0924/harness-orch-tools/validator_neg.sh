#!/usr/bin/env bash
# 복제본에서 킷별 리서치 기록 파일을 하나씩 지우고 validate-post-kaizen 의 per-kit 줄이 FAIL 로 바뀌는지 본다.
# 사용: validator_neg.sh <레포 또는 워크트리> <ref>
src=${1:?}; ref=${2:?}
t=$(mktemp -d "${TMPDIR:-/tmp}/vneg.XXXXXX"); trap 'rm -rf "$t"' EXIT
git clone -q "$src" "$t/r" && git -C "$t/r" checkout -q "$ref" || { echo "STOP 복제 실패"; exit 2; }
cd "$t/r" || exit 2
line() { python3 scripts/validate-post-kaizen.py --since HEAD 2>&1 | grep 'per-kit-research-logs' | head -1; }
printf 'intact: %s\n' "$(line)"
caught=0
for x in backend infra rust react flutter planning design tone api; do
  f=docs/$x/research-log.md
  [ -f "$f" ] || { echo "STOP 없음 $f"; exit 2; }
  mv "$f" "$t/hold"; l=$(line); mv "$t/hold" "$f"
  case $l in *FAIL*) caught=$((caught + 1)); v=FAIL ;; *) v=PASS ;; esac
  printf '%s removed -> %s\n' "$x" "$v"
done
echo "caught=$caught/9"
