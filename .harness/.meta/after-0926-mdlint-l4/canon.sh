#!/bin/bash
# 사용: canon.sh <저장소> <판>
# 다른 킷 사본과 맞대는 정본 덩어리 셋을 그 판에서 뽑아 지문(sha256 앞 16 자리)과 줄 수를 낸다.
#   ① harness/docs/guides/qa-evaluation-guide.md 의 `## Canonical ` 로 시작하는 절 전부 (scripts/check-reviewer-protocol-copies.py 가 읽는 원문)
#   ② harness/skills/sprint/SKILL.md 의 `| 공용 작업 폴더 |` 줄부터 `- **미확정**` 줄까지 (scripts/check-cause-table-copies.py 의 CANON 덩어리)
#   ③ 같은 가이드의 `#### \`UNVERIFIED_ENV\` 남용 방지 4 요건` 덩어리 — `## Canonical` 절 밖에 있다. 따로 짜지 않고
#      scripts/check-reviewer-protocol-copies.py 의 canonical_blocks() 를 그대로 불러 뽑는다(두 추출이 어긋나지 않게)
# 끝 줄: CANON_LINES=<n> CANON_SHA=<16자리>. 판이나 파일을 못 읽으면 STOP 과 종료 코드 2.
set -o pipefail
R=${1:?저장소}; V=${2:?판}
out=$( { git -C "$R" show "${V}:harness/docs/guides/qa-evaluation-guide.md" | awk '/^## Canonical /{f=1;print;next} /^## /{f=0} f' ; } 2>&1 ) || { echo "STOP $out"; exit 2; }
out2=$( { git -C "$R" show "${V}:harness/skills/sprint/SKILL.md" | awk 'index($0,"| 공용 작업 폴더 |")==1{f=1} f{print} f && index($0,"- **미확정**")==1{exit}' ; } 2>&1 ) || { echo "STOP $out2"; exit 2; }
out3=$( { git -C "$R" show "${V}:harness/docs/guides/qa-evaluation-guide.md" | python3 -c '
import importlib.util, sys
root = sys.argv[1] + "/scripts"
sys.path.insert(0, root)
spec = importlib.util.spec_from_file_location("copies", root + "/check-reviewer-protocol-copies.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
_, req = mod.canonical_blocks(sys.stdin.read().split("\n"))
if not [x for x in req if x.strip()]:
    sys.exit("4 요건 덩어리를 못 찾았다")
print("\n".join(req))
' "$R" ; } 2>&1 ) || { echo "STOP $out3"; exit 2; }
all=$(printf '%s\n%s\n%s\n' "$out" "$out2" "$out3")
n=$(printf '%s\n' "$all" | grep -c .)
[ "$n" -gt 0 ] || { echo "STOP 덩어리를 못 찾았다"; exit 2; }
echo "CANON_LINES=$n CANON_SHA=$(printf '%s\n' "$all" | shasum -a 256 | cut -c1-16)"
