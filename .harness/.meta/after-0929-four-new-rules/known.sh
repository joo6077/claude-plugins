#!/bin/bash
# 알려진 답 대조 — 복제본에 좋은 구현을 넣고 커밋한 뒤 도우미를 돌린다. 인자: good | badquote | badorder | nohtml
set -u
S=/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/nr
W=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-nr
C=$S/clone-${1}
export TMPDIR=$S/tmp
rm -rf "$C"
git clone -q "$W" "$C" && git -C "$C" checkout -q 279085a3 -b t
ln -s "$W/node_modules" "$C/node_modules"
python3 "$S/apply_good.py" "$C" || exit 2
case "${1}" in
  badquote) sed -i '' 's/stated relationship (offset)/stated relation (offset)/' "$C/docs/backend/fundamentals/database.md" ;;
  badorder) python3 - "$C" <<'EOF'
import sys, pathlib
p = pathlib.Path(sys.argv[1]) / "onboarding-kit/skills/setup-guide/SKILL.md"
t = p.read_text(encoding="utf-8")
t = t.replace("② GKE", "②X").replace("③ 혼자", "② GKE").replace("②X", "③ 혼자", 1)
p.write_text(t, encoding="utf-8")
EOF
  ;;
esac
cd "$C" || exit 2
git config user.email t@t; git config user.name t
msg=$'시험\n\nCo-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>'
for d in backend-kit planning-kit onboarding-kit docs/backend docs/backend-kit docs/planning docs/planning-kit docs/onboarding-kit; do
  if [ "${1}" = nohtml ] && [ "$d" = docs/onboarding-kit ]; then git checkout -q -- docs/onboarding-kit/format-checklist.html; fi
  git add "$d" && git commit -q -m "$msg" -- "$d" 2>/dev/null
done
git log --oneline 279085a3..HEAD | wc -l
for c in 스킬-01 스킬-02 스킬-03 스킬-04 구조-01 구조-02 구조-03 구조-04 구조-05 구조-06 오류-01 오류-02; do
  out=$(NR_ROOT="$C" python3 "$W/.harness/.meta/after-0929-four-new-rules/measure.py" "$c"); rc=$?
  echo "== $c rc=$rc"; printf '%s\n' "$out" | grep -E 'MISSING|BAD|pairs=|pages_changed|quotes=|checks=|pages=' | head -6
done
