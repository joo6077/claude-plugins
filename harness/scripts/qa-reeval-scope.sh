#!/bin/bash
# 재평가 범위 — 직전 회차 리포트 이후 무엇이 바뀌었고 무엇을 다시 재야 하는지 한 번에 낸다.
# 규칙은 harness/references/qa-evaluator/reeval.md 에 있다. 여기서는 그 전제와 범위를 계산만 한다.
#
# 쓰는 법: qa-reeval-scope.sh <직전 리포트> <구현 저장소> <계약> [개정 파일]
#   새 리포트가 같은 경로를 덮어쓰기 전에 돌린다 — 덮어쓴 뒤에는 직전 내용이 없다.
#
# 출력:
#   PREV_HEAD=<직전 Evaluated-Head | ?>
#   CHANGED=<수>  그리고 파일마다  CHANGED <저장소 기준 경로>
#     직전 평가 커밋 이후 추적 파일의 변경(커밋한 것 + 커밋 안 한 것)과 git 이 무시하지 않는 추적 안 된 새 파일
#   IGNORED <경로>   — 도구가 다시 만드는 생성물. 세지 않는다 (시험 실행만으로 GeneratedPluginRegistrant 가 바뀐다)
#   PREV_FAIL=<번호,…>  PREV_PASS=<번호,…>  PREV_NA=<번호,…>   — 직전 리포트 ## Results 절의 판정
#   REUSE=<yes|no> reason=<ok|not-reject|no-head|head-missing|contract-changed|amendments-changed>
# 종료 코드: 인자 오류면 2, 아니면 0 (재사용 불가도 0 — 사유는 REUSE 줄로 낸다).

set -u
[ $# -ge 3 ] || { echo "qa-reeval-scope: <직전 리포트> <구현 저장소> <계약> [개정 파일] 이 필요하다" >&2; exit 2; }
REPORT=$1; REPO=$2; CONTRACT=$3; AMEND=${4:-}
if ! { [ -f "$REPORT" ] && [ -f "$CONTRACT" ] && git -C "$REPO" rev-parse --git-dir >/dev/null 2>&1; }; then
  echo "qa-reeval-scope: 리포트 · 계약 파일이나 git 저장소를 못 찾았다" >&2; exit 2
fi

sha() { shasum -a 256 "$1" | cut -d' ' -f1; }
field() { LC_ALL=C grep -a -m1 "^$1:" "$REPORT" | sed -e "s/^$1:[[:space:]]*//" -e 's/[[:space:]]*$//'; }

VERDICTS=$(mktemp "${TMPDIR:-/tmp}/qa-reeval-scope.XXXXXX")
# 직전 판정 — ## Results 절 안의 `- ` 줄만 읽는다. 체크 칸이 아니라 줄의 첫 판정 글자를 따르고,
# 줄 머리의 조건 번호 묶음(`LG-01, LG-02`)을 모두 그 판정으로 읽는다. 번호가 판정 뒤(`- N/A 재사용-01`)여도 읽는다
LC_ALL=C awk '
  /^## / { inr = ($0 ~ /^## Results/); next }
  !inr || !/^- / { next }
  {
    line = $0; sub(/^- /, "", line); sub(/^\[[ x]\] /, "", line)
    if (!match($0, /(PASS|FAIL|N\/A)/)) next
    v = substr($0, RSTART, RLENGTH)
    sub(/^(PASS|FAIL|N\/A) /, "", line)
    while (match(line, /^([A-Z][A-Z]+|[^ -~]+)-[0-9][0-9]/)) {
      id = substr(line, 1, RLENGTH)
      if (!(id in seen)) { seen[id] = 1; if (v == "FAIL") f = f "," id; else if (v == "PASS") p = p "," id; else n = n "," id }
      line = substr(line, RLENGTH + 1)
      if (!sub(/^, /, "", line)) break
    }
  }
  END { print "PREV_FAIL=" substr(f, 2); print "PREV_PASS=" substr(p, 2); print "PREV_NA=" substr(n, 2) }
' "$REPORT" > "$VERDICTS"

VERDICT=$(field Verdict); PREV=$(field Evaluated-Head); PREV_AM=$(field Amendments-Sha256)
PREV_CONTRACT=$(LC_ALL=C awk '/^## Contract Fingerprint/{f=1;next} /^## /{f=0} f && /^- sha256:/{print $3; exit}' "$REPORT")
if [ -n "$AMEND" ] && [ -f "$AMEND" ]; then NOW_AM=$(sha "$AMEND"); else NOW_AM=none; fi

reason=ok
if [ "$VERDICT" != REJECT ]; then reason=not-reject
elif [ -z "$PREV" ]; then reason=no-head
elif ! git -C "$REPO" cat-file -e "$PREV^{commit}" 2>/dev/null; then reason=head-missing
elif [ "$(sha "$CONTRACT")" != "$PREV_CONTRACT" ]; then reason=contract-changed
elif [ "$NOW_AM" != "${PREV_AM:-none}" ]; then reason=amendments-changed
fi

echo "PREV_HEAD=${PREV:-?}"
if [ "$reason" = no-head ] || [ "$reason" = head-missing ]; then
  echo "CHANGED=?"
else
  changed=(); ignored=()
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    case "$(basename "$f")" in
      GeneratedPluginRegistrant.*|*.g.dart|*.freezed.dart) ignored+=("$f") ;;
      *) changed+=("$f") ;;
    esac
  done < <( { git -C "$REPO" diff --name-only "$PREV"; git -C "$REPO" ls-files --others --exclude-standard; } | LC_ALL=C sort -u)
  echo "CHANGED=${#changed[@]}"
  for f in ${changed[@]+"${changed[@]}"}; do echo "CHANGED $f"; done
  for f in ${ignored[@]+"${ignored[@]}"}; do echo "IGNORED $f"; done
fi
cat "$VERDICTS"; rm -f "$VERDICTS"
if [ "$reason" = ok ]; then echo "REUSE=yes reason=ok"; else echo "REUSE=no reason=$reason"; fi
