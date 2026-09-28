#!/usr/bin/env bash
# m-evals.sh <레포> — 평가 실행 · 평가 동기화의 킷 목록을 두 사본(그대로 · 마켓 목록에 foo-kit 을 더함)에서 잰다.
# foo-kit 은 스킬 둘(foo · bar) 가운데 foo 만 평가 사례가 있다.
# 줄마다 `<사본> <스크립트> rc=<종료 코드> kits=<→ 줄의 킷 이름, 글자 차례> skip=<SKIP 줄의 킷 이름, 글자 차례> bar_missing=<수> total=<Total 줄>`.
R=${1:?레포 경로}
T=$(mktemp -d "${TMPDIR:-/tmp}/mevals.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT
mkcopy() {
  d=$T/$1; mkdir -p "$d"
  git -C "$R" ls-files -z | (cd "$R" && xargs -0 tar -cf -) | tar -xf - -C "$d" 2>/dev/null
  # 추적 전 새 파일(구현 중)도 담는다
  (cd "$R" && git ls-files -z --others --exclude-standard -- scripts | xargs -0 tar -cf - 2>/dev/null) | tar -xf - -C "$d" 2>/dev/null
  if [ "$2" = 1 ]; then
    mkdir -p "$d/foo-kit/skills/foo" "$d/foo-kit/skills/bar" "$d/foo-kit/evals"
    printf -- '---\nname: foo\ndescription: x\n---\n' > "$d/foo-kit/skills/foo/SKILL.md"
    printf -- '---\nname: bar\ndescription: x\n---\n' > "$d/foo-kit/skills/bar/SKILL.md"
    printf '{"skill_name":"foo","evals":[{"id":1,"skill":"foo","prompt":"p","expected_output":"e","assertions":[{"text":"t","type":"output"}]}]}\n' > "$d/foo-kit/evals/evals.json"
    python3 - "$d/.claude-plugin/marketplace.json" <<'PY'
import json, sys
p = sys.argv[1]; d = json.load(open(p, encoding="utf-8"))
d["plugins"].append({"name": "foo-kit", "source": "./foo-kit", "description": "x", "version": "0.1.0"})
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
PY
  fi
}
mkcopy same 0; mkcopy foo 1
for c in same foo; do
  for s in run-evals sync-evals; do
    arg=""; [ "$s" = sync-evals ] && arg=--check-only
    out=$(python3 "$T/$c/scripts/$s.py" $arg 2>&1); rc=$?
    kits=$(printf '%s\n' "$out" | sed -n -E 's/^→ ([a-z0-9-]+).*/\1/p' | LC_ALL=C sort | tr '\n' ',' | sed 's/,$//')
    skip=$(printf '%s\n' "$out" | sed -n -E 's/^SKIP:? ([a-z0-9-]+) .*/\1/p' | LC_ALL=C sort | tr '\n' ',' | sed 's/,$//')
    printf '%s %s rc=%s kits=%s skip=%s bar_missing=%s total=[%s]\n' "$c" "$s" "$rc" "$kits" "$skip" \
      "$(printf '%s\n' "$out" | grep -c 'MISSING: bar')" "$(printf '%s\n' "$out" | grep '^Total' | tail -1)"
  done
done
