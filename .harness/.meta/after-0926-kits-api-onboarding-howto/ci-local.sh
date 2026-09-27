#!/usr/bin/env bash
# CI(.github/workflows/ci.yml) 세 묶음의 실행 단계를 로컬에서 그대로 돌려 단계마다 종료 코드를 적는다.
K=${1:-$PWD}   # 레포 또는 워크트리 경로
O=${TMPDIR:-/tmp}/ci-local
mkdir -p $O; : > $O/summary.txt
cd "$K" || exit 2
[ -d node_modules/@playwright ] || npm ci >$O/npm.log 2>&1
run() { name=$1; shift; "$@" >"$O/$name.log" 2>&1; rc=$?; printf '%-28s rc=%s\n' "$name" "$rc" | tee -a $O/summary.txt; }
run validate-plugin        python3 scripts/validate-plugin.py
run sync-evals             python3 scripts/sync-evals.py --check-only
run sync-docs              python3 scripts/sync-docs.py --check-only
run sync-orchestrator      python3 scripts/sync-orchestrator.py --check-only
run run-evals              python3 scripts/run-evals.py --verbose
run contrast-claims        python3 scripts/check-contrast-claims.py
run docs-links             python3 scripts/check-docs-links.py
run stale-values           python3 scripts/check-stale-values.py
run collector-test         python3 scripts/test-collect-kaizen-data.py
run react-detect-test      bash react-kit/evals/scripts/project-detect-test.sh
run reflect-log-test       bash reflect-kit/evals/hooks/log-reflection-test.sh
run reflect-projid-test    bash reflect-kit/evals/hooks/project-id-test.sh
run reflect-collect-test   bash reflect-kit/evals/hooks/collect-status-test.sh
run onboarding-gate-evals  sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh
run howto-gate-evals       sh howto-kit/evals/run-evals.sh
run feedback-save-test     bash harness/evals/kaizen/feedback-system/save-test.sh
if command -v yq >/dev/null; then run feedback-agg-test bash harness/evals/kaizen/feedback-system/aggregation-test.sh; else echo "feedback-agg-test SKIP (yq 없음)" | tee -a $O/summary.txt; fi
run commit-guard-test      bash harness/evals/hooks/commit-guard-test.sh
run dart-format-hook-test  bash flutter-toolkit/evals/hooks/format-edited-dart-test.sh
run playwright-visuals     npx playwright test design-kit/evals/visuals.spec.js
run docs-a11y              node scripts/check-docs-a11y.js
run scenario-report-ut     python3 -m unittest discover -s flutter-toolkit/evals/scenario-report
run decision-gate-test     bash design-kit/evals/decision-gate-test.sh
run kaizen-assertions     python3 scripts/run-kaizen-assertions.py
run reviewer-copies      python3 scripts/check-reviewer-protocol-copies.py
run api-ui-viewer        npx playwright test api-kit/evals/
# CI 파일에 새로 들어온 단계가 있으면 이 스크립트에 없는 것으로 드러난다
grep -E '^\s+run: ' .github/workflows/ci.yml | sed 's/^\s*run: //' | grep -v '^|' > $O/ci-runs.txt
echo "ci.yml run 줄 $(wc -l < $O/ci-runs.txt) 개 — 이 스크립트 밖의 것:"; grep -vFf <(grep -oE '(python3|bash|sh|node|npx|npm) [^ ]+( [^ ]+)?' "$0" | sort -u) $O/ci-runs.txt || true
grep -c 'rc=0' $O/summary.txt; grep -v 'rc=0' $O/summary.txt
