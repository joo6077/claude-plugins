#!/usr/bin/env bash
# CI 파일에만 있고 로컬 CI 도구(ci-local.sh)가 안 돌리는 단계 열다섯을 돌린다.
# 사용: bash ci-only.sh <레포 트리>   (TMPDIR 을 scratch 아래로 준다)
# 출력: 단계마다 `rc=<종료 코드> <명령>` 한 줄, 끝 줄 `ci_only=<rc 0 수>/<전체>`. 하나라도 0 이 아니면 종료 코드 1.
set -u
cd "${1}" || exit 2
ok=0; all=0
r() { all=$((all+1)); "$@" > /dev/null 2>&1; rc=$?; [ "$rc" = 0 ] && ok=$((ok+1)); echo "rc=$rc $*"; }
r python3 scripts/check-api-kit-docs.py
r python3 scripts/detect-docs-drift.py --check-table
r python3 scripts/test-detect-docs-drift.py
r python3 scripts/check-docs-common-css.py
r python3 scripts/test-check-docs-common-css.py
r python3 scripts/check-cause-table-copies.py
r python3 scripts/check-install-docs-guidance.py
r python3 scripts/test-check-cause-table-copies.py
r bash scripts/test-ci-local.sh
r bash harness/evals/measure/measure-helpers-test.sh
r bash harness/evals/superseded/check-superseded-test.sh
r bash harness/scripts/check-superseded.sh .harness
r bash bambu-kit/evals/run-gate-fixtures.sh
r bash bambu-kit/evals/makerworld-fetch-test.sh
r npx playwright test
echo "ci_only=$ok/$all"
[ "$ok" = "$all" ]
