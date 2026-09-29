#!/bin/bash
# 피드백 파일 셋을 임시 폴더에 만들어 harness-kaizen trigger-check.sh 를 돌린다. 레포 뿌리에서 돌린다.
# 쓰는 법: bash tc.sh <번호1> <번호2> <번호3>   각 파일에 「- [ ] <번호>: 패턴 걸림 — FAIL」 한 줄
root=$(pwd); tmp=$(mktemp -d "${TMPDIR:-/tmp}/tc.XXXXXX"); mkdir -p "$tmp/h"; i=0
for id in "$@"; do i=$((i + 1)); printf -- '- [ ] %s: 패턴 걸림 — FAIL\n' "$id" > "$tmp/h/sprint-feedback-s$i.md"; done
out=$(bash "$root/harness/skills/harness-kaizen/scripts/trigger-check.sh" "$tmp/h" "$tmp/none" 2>&1); rc=$?
printf 'rc=%s out=[%s]\n' "$rc" "$out"; rm -rf "$tmp"
