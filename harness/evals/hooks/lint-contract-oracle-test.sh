#!/usr/bin/env bash
# shellcheck disable=SC2016  # 측정 줄의 백틱 · 달러는 계약 글자 그대로다
# harness 플러그인 훅 lint-contract-oracle.sh 가 한 백틱 안 grep · rg 명령의 한글 검색 글을 산문-grep 으로 짚는지 본다.
# 계약 after-0929-codex-silent-pass 의 스크립트-09 · 스크립트-12 를 따른다. 조건이 이어질 때 다음 번호를 잃지 않는지도 본다. 로캘 C · en_US.UTF-8, 조건 번호 영어 · 한국어를 모두 돈다.
# LINT_ORACLE_HOOK 으로 훅 경로를, CLAUDE_HOOK_LIB 로 훅 도우미 경로를 바꿀 수 있다 (기본: harness/scripts/ 의 lint-contract-oracle.sh · 그 옆 _lib-hook-payload.sh)
# — 고치기 전 사본으로 음성 대조를 돌릴 때 쓴다. CLAUDE_HOOK_LIB 를 안 주면 훅이 제 옆 도우미를 찾는다.
# 개인 설정이 같은 훅을 또 등록해 두 번 도는지는 scripts/check-user-hook-overlap.py 가 본다.
# 종료 코드: 0 통과 · 1 실패 · 2 준비 실패 (훅 · 훅 도우미 · jq 없음)

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
hook=${LINT_ORACLE_HOOK:-$here/../../scripts/lint-contract-oracle.sh}
lib=${CLAUDE_HOOK_LIB:-$here/../../scripts/_lib-hook-payload.sh}
[ -f "$hook" ] || { echo "훅이 없다: $hook" >&2; exit 2; }
[ -f "$lib" ] || { echo "훅 도우미가 없다: $lib" >&2; exit 2; }
command -v jq >/dev/null 2>&1 || { echo "jq 가 없다" >&2; exit 2; }

work=$(mktemp -d "${TMPDIR:-/tmp}/lint-oracle-test.XXXXXX") || exit 2
trap 'rm -rf "$work"' EXIT
mkdir -p "$work/.harness"
contract=$work/.harness/sprint-contract-x.md
fails=0

found() {  # found <LC_ALL=로캘> <조건 줄> <측정 줄> [<조건 줄> <측정 줄> …] — 훅이 짚은 조건 번호와 까닭
  locale_arg=$1; shift
  { printf -- '---\nstatus: active\n---\n\n## Skill\n\n'; printf '%s\n  %s\n' "$@"; } >"$contract"
  jq -nc --arg f "$contract" '{tool_name:"Write",tool_input:{file_path:$f}}' \
    | env "$locale_arg" bash "$hook" \
    | jq -r '.hookSpecificOutput.additionalContext // empty' \
    | grep -oE '^  - [^ ]+ \([^)]*\)' | sed 's/^  - //' | tr '\n' ' ' | sed 's/ $//'
}
check() {  # check <이름> <기대> <실제>
  if [ "$2" = "$3" ]; then echo "PASS $1"; else printf 'FAIL %s — 기대 [%s] 실제 [%s]\n' "$1" "$2" "$3"; fails=$((fails + 1)); fi
}

for locale_setting in LC_ALL=C LC_ALL=en_US.UTF-8; do
  loc=${locale_setting#LC_ALL=}
  check "$loc 한백틱-영어번호" "SK-01 (산문-grep)" \
    "$(found "$locale_setting" '- [ ] SK-01: x' '측정: `grep -cF "표준으로 강제하지 않는다" file.md` >= 1')"
  check "$loc 한백틱-한국어번호" "스킬-01 (산문-grep)" \
    "$(found "$locale_setting" '- [ ] 스킬-01: x' '측정: `grep -cF "표준으로 강제하지 않는다" file.md` >= 1')"
  check "$loc 한백틱-rg" "스킬-02 (산문-grep)" \
    "$(found "$locale_setting" '- [ ] 스킬-02: x' "측정: \`rg -c '표준으로 강제하지 않는다' file.md\` 이 1 이상")"
  check "$loc 나뉜백틱-영어번호" "SK-03 (산문-grep)" \
    "$(found "$locale_setting" '- [ ] SK-03: x' '측정: `grep -cF` 로 `표준으로 강제하지 않는다` 를 센 값 >= 1')"
  check "$loc 나뉜백틱-한국어번호" "스킬-03 (산문-grep)" \
    "$(found "$locale_setting" '- [ ] 스킬-03: x' '측정: `grep -cF` 로 `표준으로 강제하지 않는다` 를 센 값 >= 1')"
  check "$loc ASCII검색글" "" \
    "$(found "$locale_setting" '- [ ] 스킬-04: x' "측정: \`grep -c 'yaml.safe_load' scripts/ci-local.sh\` 이 1")"
  check "$loc 경로에만한글" "" \
    "$(found "$locale_setting" '- [ ] 스킬-05: x' "측정: \`grep -c 'abc' 문서/스킬.md\` 이 1")"
  # 앞 조건의 따옴표 든 grep 을 읽은 뒤에도 다음 조건 번호가 비지 않아야 한다
  check "$loc 앞조건따옴표grep" "SC-02 (산문-grep)" \
    "$(found "$locale_setting" '- [ ] SC-01: x' '측정: `grep -c "abc" f.txt` 종료 코드 0' \
      '- [ ] SC-02: x' '측정: `표준으로 강제하지 않는다` 를 `grep -cF` 로 센다 >= 1')"
done

echo "실패 $fails 건"
[ "$fails" = 0 ]
