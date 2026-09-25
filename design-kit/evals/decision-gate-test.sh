#!/usr/bin/env bash
# 결정 전파 검사 시험 — visual-change-protocol.md §6 의 검사 코드를 문서에서 떼어 입력 열로 돌리고 종료 코드를 대조한다.
# 부를 때마다 문서에서 뗀다 — 사본을 두면 문서를 고쳐도 시험은 옛 코드를 잰다.
# 모양이 틀린 입력이 Traceback 으로 멈추면 종료 코드 1(위반)로 읽힌다 — 종료 코드와 함께 Traceback 줄 수도 본다.
# 다른 판으로 돌리기: DECISION_GATE_DOC=<문서 경로> bash decision-gate-test.sh
set -u
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
DOC=${DECISION_GATE_DOC:-$HERE/../references/visual-change-protocol.md}
[ -f "$DOC" ] || { echo "문서가 없다 — $DOC"; exit 2; }
python3 -c 'import yaml' 2>/dev/null || { echo "PyYAML 이 없다 — 검사 코드가 yaml 을 읽는다"; exit 2; }

W=$(mktemp -d "${TMPDIR:-/tmp}/dgt.XXXXXX") || exit 2
trap 'rm -rf "$W"' EXIT
awk '/^```python/{b=1;n="";next} b&&/^```/{if(ok){exit} b=0;next} b{n=n $0 "\n"; if($0 ~ /Decision Propagation Coverage Gate/) ok=1} END{printf "%s", n}' "$DOC" > "$W/gate.py"
grep -q 'Decision Propagation Coverage Gate' "$W/gate.py" || { echo "검사 코드를 못 뗐다 — $DOC"; exit 2; }

DECISION='decision_id: DEC-20260813-001
    source: .design/approvals/DEC-20260813-001.md'
printf 'decisions:\n  - %s\n    required_surfaces:\n      - surface_id: a\n        golden: g.png\n        assertions: ["main visible"]\n' "$DECISION" > "$W/ok.yaml"
printf 'decisions:\n  - decision_id: DEC-2026-1\n    source: s\n    required_surfaces:\n      - surface_id: a\n        assertions: ["main visible"]\n' > "$W/badid.yaml"
printf 'decisions:\n  - %s\n    required_surfaces:\n      - surface_id: a\n        assertions: ["main visible"]\n    excluded_surfaces: [onboarding.mobile]\n' "$DECISION" > "$W/exstr.yaml"
printf 'decisions: [DEC-20260813-001]\n' > "$W/decstr.yaml"
printf -- '- a\n- b\n' > "$W/toplist.yaml"
printf 'decisions:\n  - %s\n    required_surfaces: [dashboard.desktop]\n' "$DECISION" > "$W/reqstr.yaml"
printf 'decisions:\n  - %s\n    required_surfaces:\n      - surface_id: a\n        golden: g.png\n        assertions: "main visible"\n' "$DECISION" > "$W/assertstr.yaml"
printf 'decisions:\n  - %s\n    required_surfaces:\n      - surface_id: a\n        golden: g.png\n' "$DECISION" > "$W/goldonly.yaml"
printf 'decisions: []\n' > "$W/empty.yaml"

n=0; bad=0
# 이름:답 — 0 통과 · 1 커버리지 위반 · 2 모양 오류 · 3 대상 0 건 (missing 은 파일을 만들지 않는다)
for c in ok:0 badid:2 exstr:2 decstr:2 toplist:2 reqstr:2 assertstr:2 goldonly:1 empty:3 missing:3; do
  name=${c%%:*}; want=${c##*:}; n=$((n + 1))
  out=$(python3 "$W/gate.py" "$W/$name.yaml" 2>&1); rc=$?
  tb=$(printf '%s\n' "$out" | grep -c '^Traceback')
  if [ "$rc" = "$want" ] && [ "$tb" = 0 ]; then
    echo "일치 $name rc=$rc"
  else
    echo "불일치 $name — rc=$rc (답 $want) Traceback=$tb"; bad=$((bad + 1))
  fi
done

echo "결과: $n 경우 중 불일치 $bad"
[ "$bad" = 0 ]
