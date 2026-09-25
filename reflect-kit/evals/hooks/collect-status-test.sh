#!/usr/bin/env bash
# collect_status · facets_unmatched 시험 — 답을 손으로 셀 수 있는 .errors.log · reflections · facets 묶음으로 잰다.
# codex 실패와 대체 경로 실패를 더하면 한 실행을 두 번 센다 — 「실패 시도」 값이 잡는다.
# 기간 밖 줄 · 다른 훅 줄 · 정상 skip 줄을 세면 실패 시도가 부푼다 — 7 일 값과 all 값이 잡는다.
# 다른 사본으로 돌리기: PROJECT_ID_LIB=<사본 경로> bash collect-status-test.sh
set -u
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
LIB=${PROJECT_ID_LIB:-$(cd "$HERE/../../hooks" && pwd)/_lib-project-id.sh}
[ -f "$LIB" ] || { echo "라이브러리가 없다 — $LIB"; exit 2; }
command -v jq >/dev/null 2>&1 || { echo "jq 가 없다 — facets 를 못 읽는다"; exit 2; }

W=$(mktemp -d "${TMPDIR:-/tmp}/cst.XXXXXX") || exit 2
W=$(cd "$W" && pwd -P)
trap 'rm -rf "$W"' EXIT
at() {  # at <초 전> <date 형식> [u] — BSD 는 -r, GNU 는 -d @. 셋째 인자가 u 면 UTC
  local e=$(( $(date +%s) - $1 ))
  if [ "${3:-}" = u ]; then
    date -u -r "$e" "$2" 2>/dev/null || date -u -d "@$e" "$2"
  else
    date -r "$e" "$2" 2>/dev/null || date -d "@$e" "$2"
  fi
}
D1=$(at 86400 '+%Y-%m-%dT%H:%M:%S%z'); D2=$(at 172800 '+%Y-%m-%dT%H:%M:%S%z')
D3=$(at 259200 '+%Y-%m-%dT%H:%M:%S%z'); D10=$(at 864000 '+%Y-%m-%dT%H:%M:%S%z')
mkdir -p "$W/logs/b1" "$W/logs/b2" "$W/logs/b3"
cat > "$W/logs/b1/.errors.log" <<EOF
$D2 [log-reflection] fail:codex-exit-2 session=A err=error: unexpected argument '--full-auto' found
$D2 [log-reflection] fallback:claude-exit-1 session=A err=There's an issue with the selected model (haiku-4.5).
$D2 [log-reflection] fail:codex-exit-2 session=A
$D2 [log-reflection] fallback:claude-exit-1 session=A
$D1 [log-reflection] fail:codex-exit-1 session=B err=ERROR: You've hit your usage limit.
$D1 [log-reflection] fallback:claude-used session=B
$D1 [log-reflection] fail:codex-empty-output session=C
$D1 [log-reflection] skip:fallback-unavailable session=C
$D1 [log-reflection] skip:cli-missing session=D
$D1 [log-reflection] skip:transcript-too-short lines=3
$D1 [log-reflection] vocab:raw_distinct/clusters/entries/singletons/fold/singleton_share/epc=1/1/1/1/1.00/1.000/1.00 session=A
$D1 [log-prompt] fail:codex-exit-9 session=Z
$D10 [log-reflection] fail:codex-exit-2 session=E
$D10 [log-reflection] fallback:claude-exit-1 session=E
EOF
printf '%s [log-reflection] fail:tag-field-unresolved session=F\n' "$D3" > "$W/logs/b2/.errors.log"
# 기록 하나 뒤에 실패만 이어진 폴더 — 엔트리가 있어도 기간 도중에 멈춘 수집기를 잡는지 본다
mkdir -p "$W/logs/b4"
printf '%s [log-reflection] skip:cli-missing session=H\n' "$D1" > "$W/logs/b4/.errors.log"
# shellcheck disable=SC2016  # 역따옴표는 reflections 머리의 마크다운 글자다
printf '\n## %s\n\n- session: `G2`\n\n```yaml\nprimary_category: tool_failure\n```\n' "$D2" > "$W/logs/b4/reflections-2026-09.md"
cat > "$W/logs/b1/reflections-2026-09.md" <<EOF

## $D10

- session: \`G\`
- cwd: \`/x\`

\`\`\`yaml
primary_category: misunderstanding
\`\`\`

\`\`\`yaml
primary_category: wrong_approach
\`\`\`

---

## $D1

- session: \`B\`
- cwd: \`/x\`

\`\`\`yaml
primary_category: tool_failure
\`\`\`

---
EOF

# facets — 본 레포 alpha 와 그 워크트리 · 다른 레포 beta
g() { git -c user.name=t -c user.email=t@t -c init.defaultBranch=main "$@" > /dev/null 2>&1; }
mkdir -p "$W/repos/alpha" "$W/repos/beta" "$W/wt" "$W/usage/facets" "$W/usage/session-meta"
g -C "$W/repos/alpha" init && printf 'x\n' > "$W/repos/alpha/f" && g -C "$W/repos/alpha" add f && g -C "$W/repos/alpha" commit -m i || exit 2
g -C "$W/repos/alpha" worktree add "$W/wt/alpha-wt" -b wt1 || exit 2
fx() {  # fx <파일> <session> <friction> [<project_path> <초 전>] — 뒤 둘이 없으면 session-meta 를 안 만든다
  jq -cn --arg s "$2" --arg f "$3" '{session_id: $s, friction_detail: $f}' > "$W/usage/facets/$1.json"
  [ $# -ge 5 ] || return 0
  jq -cn --arg s "$2" --arg p "$4" --arg t "$(at "$5" '+%Y-%m-%dT%H:%M:%S.123Z' u)" \
    '{session_id: $s, project_path: $p, start_time: $t}' > "$W/usage/session-meta/$2.json"
}
fx f1 S-miss "missed friction" "$W/repos/alpha" 172800
fx f2 B "recorded friction" "$W/repos/alpha" 86400
fx f3 S-empty "" "$W/repos/alpha" 86400
printf '{"session_id": ' > "$W/usage/facets/f4.json"
fx f5 S-nometa "no meta"
fx f6 S-old "old friction" "$W/repos/alpha" 1728000
fx f7 S-other "other project" "$W/repos/beta" 86400
fx f8 S-wt "worktree friction" "$W/wt/alpha-wt" 86400

# 정상 종료(no issues) 뒤의 폴더 — 기록 뒤 실패가 있어도 그 뒤 정상 종료가 있으면 멈춤이 아니고, 정상 종료 뒤 다시 실패하면 멈춤이다
mkdir -p "$W/logs/b5" "$W/logs/b6" "$W/logs/b7"
# shellcheck disable=SC2016  # 역따옴표는 reflections 머리의 마크다운 글자다
printf '\n## %s\n\n- session: `K1`\n\n```yaml\nprimary_category: tool_failure\n```\n' "$D3" > "$W/logs/b5/reflections-2026-09.md"
cp "$W/logs/b5/reflections-2026-09.md" "$W/logs/b6/reflections-2026-09.md"
printf '%s [log-reflection] fail:codex-exit-1 session=K2\n%s [log-reflection] fallback:claude-exit-1 session=K2\n%s [log-reflection] ok:no-issues session=K3\n' "$D2" "$D2" "$D1" > "$W/logs/b5/.errors.log"
printf '%s [log-reflection] ok:no-issues session=K3\n%s [log-reflection] fail:codex-exit-1 session=K4\n%s [log-reflection] fallback:claude-exit-1 session=K4\n' "$D2" "$D1" "$D1" > "$W/logs/b6/.errors.log"
# 엔트리 0 이어도 실패 뒤에 정상 종료가 있으면 수집기는 돌고 있다
printf '%s [log-reflection] fail:codex-exit-1 session=K5\n%s [log-reflection] fallback:claude-exit-1 session=K5\n%s [log-reflection] ok:no-issues session=K6\n' "$D2" "$D2" "$D1" > "$W/logs/b7/.errors.log"

n=0; bad=0
check() {  # check <이름> <답> <값>
  n=$((n + 1))
  if [ "$2" = "$3" ]; then echo "일치 $1"
  else echo "불일치 $1 — 값 [$3] (답 [$2])"; bad=$((bad + 1)); fi
}
cs() { bash -c '. "$1" 2>/dev/null; shift; collect_status "$@"; echo "rc=$?"' _ "$LIB" "$@" 2>&1; }
fu() { bash -c '. "$1" 2>/dev/null; shift; facets_unmatched "$@"; echo "rc=$?"' _ "$LIB" "$@" 2>&1; }

check "7 일 · 두 폴더" "수집 상태: Stop 실패 시도 5회 (codex 실패 4 · 대체 경로 실패 3 · 대체 경로 성공 1 · 분석 전 중단 2; 고유 세션 4) / 기록된 세션 1 / 엔트리 1 / 마지막 기록 $D1
rc=0" "$(cs 7 "$W/logs/b1" "$W/logs/b2")"
check "all · 두 폴더" "수집 상태: Stop 실패 시도 6회 (codex 실패 5 · 대체 경로 실패 4 · 대체 경로 성공 1 · 분석 전 중단 2; 고유 세션 5) / 기록된 세션 2 / 엔트리 3 / 마지막 기록 $D1
rc=0" "$(cs all "$W/logs/b1" "$W/logs/b2")"
check "멈춤 — 엔트리 0 · 실패 1 이상" "수집 상태: Stop 실패 시도 1회 (codex 실패 0 · 대체 경로 실패 0 · 대체 경로 성공 0 · 분석 전 중단 1; 고유 세션 1) / 기록된 세션 0 / 엔트리 0 / 마지막 기록 없음
⚠ 수집 멈춤 — 엔트리 0은 문제 없음이 아니다
rc=0" "$(cs 7 "$W/logs/b2")"
check "빈 폴더 — 경고 없음" "수집 상태: Stop 실패 시도 0회 (codex 실패 0 · 대체 경로 실패 0 · 대체 경로 성공 0 · 분석 전 중단 0; 고유 세션 0) / 기록된 세션 0 / 엔트리 0 / 마지막 기록 없음
rc=0" "$(cs 7 "$W/logs/b3")"
check "도중 멈춤 — 마지막 기록 뒤 실패" "수집 상태: Stop 실패 시도 1회 (codex 실패 0 · 대체 경로 실패 0 · 대체 경로 성공 0 · 분석 전 중단 1; 고유 세션 1) / 기록된 세션 1 / 엔트리 1 / 마지막 기록 $D2
⚠ 수집 멈춤 — 마지막 기록 뒤 Stop 실패 시도 1회
rc=0" "$(cs 7 "$W/logs/b4")"
check "정상 종료 뒤 — 경고 없음" "수집 상태: Stop 실패 시도 1회 (codex 실패 1 · 대체 경로 실패 1 · 대체 경로 성공 0 · 분석 전 중단 0; 고유 세션 1) / 기록된 세션 1 / 엔트리 1 / 마지막 기록 $D3
rc=0" "$(cs 7 "$W/logs/b5")"
check "정상 종료 뒤 다시 실패 — 멈춤" 1 "$(cs 7 "$W/logs/b6" | grep -c '^⚠ 수집 멈춤 — 마지막 기록 뒤 Stop 실패 시도 1회$')"
check "엔트리 0 · 실패 뒤 정상 종료 — 경고 없음" "수집 상태: Stop 실패 시도 1회 (codex 실패 1 · 대체 경로 실패 1 · 대체 경로 성공 0 · 분석 전 중단 0; 고유 세션 1) / 기록된 세션 0 / 엔트리 0 / 마지막 기록 없음
rc=0" "$(cs 7 "$W/logs/b7")"
check "일수 잘못 — 멈춤" "collect_status: 일수는 숫자 또는 all
rc=2" "$(cs 7d "$W/logs/b1")"

check "facets 7 일 · alpha" "facets 대조: facets 4개 · 마찰 있는 세션 3개 · 그중 reflections 없음 2개 (facets 읽기 실패 1 · session-meta 읽기 실패 1)
- S-miss · $(jq -r .start_time "$W/usage/session-meta/S-miss.json") · $W/repos/alpha — missed friction
- S-wt · $(jq -r .start_time "$W/usage/session-meta/S-wt.json") · $W/wt/alpha-wt — worktree friction
rc=0" "$(fu 7 alpha "$W/usage" "$W/logs")"
check "facets 7 일 · all" "facets 대조: facets 5개 · 마찰 있는 세션 4개 · 그중 reflections 없음 3개 (facets 읽기 실패 1 · session-meta 읽기 실패 1)" \
  "$(fu 7 all "$W/usage" "$W/logs" | head -1)"
check "facets all · alpha" "facets 대조: facets 5개 · 마찰 있는 세션 4개 · 그중 reflections 없음 3개 (facets 읽기 실패 1 · session-meta 읽기 실패 1)" \
  "$(fu all alpha "$W/usage" "$W/logs" | head -1)"
check "facets 폴더 없음" "facets 대조: (없음)
rc=0" "$(fu 7 alpha "$W/nousage" "$W/logs")"

# zsh 로 부르면 셈을 하지 않고 멈춘다
if command -v zsh >/dev/null 2>&1; then
  check "zsh — 멈춤" "collect_status: bash 로 부른다
rc=2" "$(zsh -c '. "$1" 2>/dev/null; collect_status 7 "$2"; echo "rc=$?"' _ "$LIB" "$W/logs/b1" 2>&1)"
else
  echo "건너뜀 zsh 없음"
fi

echo "결과: $n 경우 중 불일치 $bad"
[ "$bad" = 0 ]
