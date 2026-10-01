#!/usr/bin/env bash
# harness 플러그인 훅 qa-pending-check.sh 가 QA 결과 파일이 비었거나 판정 줄이 없는 계약을 안내에 넣는지 본다.
# 계약 after-0929-codex-silent-pass 의 스크립트-10 · 스크립트-12 를 따른다. APPROVE 이고 봉인 뒤 시각일 때만 완료다.
# QA_PENDING_HOOK 으로 훅 경로를, CLAUDE_HOOK_LIB 로 훅 도우미 경로를 바꿀 수 있다 (기본: harness/scripts/ 의 qa-pending-check.sh · 그 옆 _lib-hook-payload.sh)
# — 고치기 전 사본으로 음성 대조를 돌릴 때 쓴다. CLAUDE_HOOK_LIB 를 안 주면 훅이 제 옆 도우미를 찾는다.
# 개인 설정이 같은 훅을 또 등록해 두 번 도는지는 scripts/check-user-hook-overlap.py 가 본다.
# 종료 코드: 0 통과 · 1 실패 · 2 준비 실패 (훅 · 훅 도우미 · jq 없음)

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
hook=${QA_PENDING_HOOK:-$here/../../scripts/qa-pending-check.sh}
lib=${CLAUDE_HOOK_LIB:-$(dirname "$hook")/_lib-hook-payload.sh}
[ -f "$hook" ] || { echo "훅이 없다: $hook" >&2; exit 2; }
[ -f "$lib" ] || { echo "훅 도우미가 없다: $lib" >&2; exit 2; }
command -v jq >/dev/null 2>&1 || { echo "jq 가 없다" >&2; exit 2; }

work=$(mktemp -d "${TMPDIR:-/tmp}/qa-pending-test.XXXXXX") || exit 2
trap 'rm -rf "$work"' EXIT
fails=0

pending() {  # pending <경우> <결과 파일 내용 | -none-> — 안내에 계약이 들어갔으면 1
  project=$work/$1; mkdir -p "$project/.harness"
  printf -- '---\nslug: x\nstatus: active\nowner_session: S1\nlocked_at: "2026-09-29 10:00"\n---\n\n## Skill\n- [ ] 스킬-01: x\n' \
    >"$project/.harness/sprint-contract-x.md"
  [ "$2" = -none- ] || printf '%s' "$2" >"$project/.harness/sprint-feedback-x.md"
  jq -nc --arg d "$project" '{session_id:"S1",cwd:$d,transcript_path:""}' \
    | bash "$hook" \
    | jq -r '.hookSpecificOutput.additionalContext // empty' \
    | grep -c 'sprint-contract-x.md'
}
check() {  # check <이름> <기대> <실제>
  if [ "$2" = "$3" ]; then echo "PASS $1"; else printf 'FAIL %s — 기대 %s 실제 %s\n' "$1" "$2" "$3"; fails=$((fails + 1)); fi
}

check 빈결과파일 1 "$(pending empty '')"
check 판정줄없음 1 "$(pending no-verdict $'# QA\n\nEvaluated: 2026-09-29 11:00\n')"
check 봉인뒤APPROVE 0 "$(pending approve $'Verdict: APPROVE\nEvaluated: 2026-09-29 11:00\n')"
check 봉인전APPROVE 1 "$(pending approve-old $'Verdict: APPROVE\nEvaluated: 2026-09-28 11:00\n')"
check REJECT 1 "$(pending reject $'Verdict: REJECT\nEvaluated: 2026-09-29 11:00\n')"
check 결과파일없음 1 "$(pending none -none-)"

echo "실패 $fails 건"
[ "$fails" = 0 ]
