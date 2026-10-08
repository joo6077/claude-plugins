#!/usr/bin/env bash
# 판정 격리 안에서는 브라우저를 띄울 수 없어 구조-02 · 구조-03 을 격리 밖에서 미리 잰다. 나머지 조건은 판정자가 직접 잰다.
# 사용: bash .harness/.meta/scenario-report-op-roi/measure.sh <조건 번호>   (레포 뿌리에서)
case "${1}" in
  구조-02|구조-03) ;;
  *) echo "SKIP ${1} — 판정자가 직접 잰다"; exit 0 ;;
esac
HERE=$(cd "$(dirname "${0}")" && pwd)
WORK=$(mktemp -d "${TMPDIR:-/tmp}/op-roi-measure-XXXXXX")
T=flutter-toolkit/evals/scenario-report
K=flutter-toolkit/skills/flutter-scenario-report
cp -R "$T/example" "$WORK/example"
python3 "$K/scripts/build_report.py" "$WORK/example" >/dev/null || { echo "FAIL ${1} 예시 보고서를 못 만들었다"; exit 1; }
cmp -s "$WORK/example/TC-003-shot-strip/index.html" "$T/example/TC-003-shot-strip/index.html" || { echo "FAIL ${1} 커밋된 예시 보고서와 다시 만든 것이 다르다"; exit 1; }
python3 "$T/fold_fixture.py" "$T/example" "$WORK/fold" >/dev/null && python3 "$K/scripts/build_report.py" "$WORK/fold" >/dev/null \
  || { echo "FAIL ${1} 접힌 조작 임시 예시를 못 만들었다"; exit 1; }
PLAYWRIGHT="${PLAYWRIGHT_MODULE:-/Users/jackson/Hub/10_Dev/claude-plugins/node_modules/playwright}"
node "$HERE/measure.cjs" "${1}" "$WORK" "$PLAYWRIGHT"
