#!/usr/bin/env bash
# check-superseded.sh <.harness 폴더> — superseded 계약마다 superseded_by 가 살아 있는 새 판을 가리키는지 본다.
# 규칙 정의는 harness/references/contract-schema.md §v5 신규 필드 의 superseded_by 행이다.
#
# superseded 계약마다 한 줄: OK · MISSING_BY(가리킴 없음) · MISSING_TARGET(가리킨 계약 없음) · CHAIN(가리킨 계약도 superseded)
# 못 읽은 파일마다 한 줄: 가리킨 새 판을 못 읽으면 UNREADABLE <계약> -> <새 판>, 그 밖의 계약은 UNREADABLE <계약>.
# 못 읽은 것을 OK 로 치지 않는다
# 끝 줄: checked=<superseded 계약 수> violations=<위반 수> unreadable=<못 읽은 수>
# 종료 코드는 harness/evals/gate-exit-codes.md — 0 위반 없음 · 1 위반 있음 · 2 폴더 없음 · 공용 측정 파일을 못 읽음 · UNREADABLE 있음

case ${1:-} in
  -h|--help) sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
esac
contract_dir=${1:-}
[ -n "$contract_dir" ] || { echo "사용법: check-superseded.sh <.harness 폴더>" >&2; exit 2; }
[ -d "$contract_dir" ] || { echo "폴더가 없다: $contract_dir" >&2; exit 2; }

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)
# shellcheck source=/dev/null
. "$script_dir/measure-common.sh" || exit 2

checked=0; violations=0; unreadable=0
unread_contracts=""; reported_targets=""
contracts=$(find "$contract_dir" -maxdepth 1 -type f -name 'sprint-contract-*.md' | LC_ALL=C sort)
while IFS= read -r contract; do
  [ -n "$contract" ] || continue
  # 명령 치환은 fm_get 의 실패 코드를 버리므로 따로 받는다 — 못 읽은 계약이 빈 값으로 OK 가 되지 않게
  if ! status=$(fm_get "$contract" status); then
    unread_contracts="$unread_contracts$contract
"
    continue
  fi
  [ "$status" = superseded ] || continue
  checked=$((checked + 1))
  target_slug=$(fm_get "$contract" superseded_by)
  target=$contract_dir/sprint-contract-$target_slug.md
  if [ -z "$target_slug" ]; then state=MISSING_BY
  elif [ ! -f "$target" ]; then state=MISSING_TARGET
  elif ! target_status=$(fm_get "$target" status); then state=UNREADABLE
  elif [ "$target_status" = superseded ]; then state=CHAIN
  else state=OK
  fi
  case $state in
    OK) ;;
    UNREADABLE) unreadable=$((unreadable + 1)); reported_targets="$reported_targets$target
" ;;
    *) violations=$((violations + 1)) ;;
  esac
  echo "$state $contract${target_slug:+ -> $target_slug}"
done <<EOF
$contracts
EOF

# 새 판으로 이미 알린 파일은 다시 적지 않는다
while IFS= read -r contract; do
  [ -n "$contract" ] || continue
  printf '%s' "$reported_targets" | grep -qxF -- "$contract" && continue
  unreadable=$((unreadable + 1))
  echo "UNREADABLE $contract"
done <<EOF
$unread_contracts
EOF

echo "checked=$checked violations=$violations unreadable=$unreadable"
[ "$unreadable" = 0 ] || exit 2
[ "$violations" = 0 ]
