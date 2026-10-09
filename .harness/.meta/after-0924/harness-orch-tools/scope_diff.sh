#!/usr/bin/env bash
# 이 스프린트 커밋 구간의 변경 범위를 잰다.
# (1) .harness 밖 변경 경로가 허용 13 개 안에만 있는지 · 필수 10 개가 모두 바뀌었는지
# (2) 커밋마다 건드린 킷 폴더(marketplace.json 의 플러그인 이름) 수가 1 이하인지
# (3) 커밋 제목마다 한글이 있는지
# 사용: scope_diff.sh <레포 또는 워크트리> <base> <upper>
repo=${1:?}; base=${2:?}; up=${3:?}
cd "$repo" || exit 2
git rev-parse -q --verify "$up^{commit}" >/dev/null || { echo "STOP 상한 해석 실패 $up"; exit 2; }
required="harness/scripts/commit-guard.sh
harness/evals/hooks/commit-guard-test.sh
scripts/detect-docs-drift.py
scripts/sync-orchestrator.py
scripts/collect-kaizen-data.py
scripts/validate-post-kaizen.py
.claude/skills/kaizen-orchestrator/SKILL.md
.claude/skills/kaizen-orchestrator/references/phase-research-templates.md
.claude/skills/docs-site/SKILL.md
.claude/skills/docs-site/references/css-tokens.md"
optional="harness/README.md
.claude/skills/kaizen-orchestrator/references/phase-dependencies.md
scripts/test-collect-kaizen-data.py"
changed=$(git diff --name-only "$base" "$up" -- . ':(exclude).harness' | LC_ALL=C sort)
outside=$(comm -23 <(printf '%s\n' "$changed" | grep .) <(printf '%s\n%s\n' "$required" "$optional" | LC_ALL=C sort))
missing=$(comm -13 <(printf '%s\n' "$changed" | grep .) <(printf '%s\n' "$required" | LC_ALL=C sort))
printf '%s\n' "$outside" | grep . | sed 's/^/  outside /'
printf '%s\n' "$missing" | grep . | sed 's/^/  missing /'
kits=$(python3 -c "import json;print('\n'.join(p['name'] for p in json.load(open('.claude-plugin/marketplace.json'))['plugins']))")
multi=0; nohangul=0; commits=0
for c in $(git rev-list "$base..$up"); do
  commits=$((commits + 1))
  n=$(git show --name-only --format= "$c" | grep . | cut -d/ -f1 | LC_ALL=C sort -u | grep -Fxc -f <(printf '%s\n' "$kits"))
  [ "$n" -le 1 ] || { multi=$((multi + 1)); echo "  multi-kit $c ($n)"; }
  git log -1 --format=%s "$c" | python3 -c 'import re,sys; sys.exit(0 if re.search("[가-힣]", sys.stdin.read()) else 1)' || { nohangul=$((nohangul + 1)); echo "  no-hangul $c"; }
done
printf 'changed=%s outside=%s missing=%s commits=%s multi_kit=%s no_hangul=%s\n' \
  "$(printf '%s\n' "$changed" | grep -c .)" "$(printf '%s\n' "$outside" | grep -c .)" "$(printf '%s\n' "$missing" | grep -c .)" "$commits" "$multi" "$nohangul"
