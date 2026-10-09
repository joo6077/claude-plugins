#!/usr/bin/env bash
# m-phase-sec.sh <레포> <판> — <판> 의 scripts/spawn-kaizen-phase.sh 가 Phase 마다 고르는 자료 절(§2 · §3)을 두 임시 사본에서 잰다.
# 사본 same = 마켓 목록 그대로, mid = 마켓 목록 harness 바로 뒤(flutter-toolkit 앞)에 aaa-kit 을 끼움.
# 스크립트는 `git show <판>:scripts/spawn-kaizen-phase.sh` 로 뜬다. 사본은 git 저장소라 태그 · 상태 파일 쓰기가 레포 밖에서 일어난다.
# 출력: 사본마다 `<사본> s2=<§2 를 받은 킷, 쉼표> s3=<§3 을 받은 킷> bad_rc=<Phase 5~끝 중 0 이 아닌 종료 코드 수>`.
R=${1:?레포}; REV=${2:?판}
T=$(mktemp -d "${TMPDIR:-/tmp}/mphsec.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT
mkcopy() {  # mkcopy <이름> <aaa 를 끼울지 0|1>
  d=$T/$1; mkdir -p "$d"
  (cd "$R" && tar -cf - scripts .claude-plugin .harness/.meta/kaizen-data-pool.md .harness/.meta/kaizen-state.yaml) | tar -xf - -C "$d"
  (cd "$R" && git show "$REV:scripts/spawn-kaizen-phase.sh") > "$d/scripts/spawn-kaizen-phase.sh" || exit 2
  if [ "$2" = 1 ]; then
    python3 - "$d/.claude-plugin/marketplace.json" <<'PY'
import json, sys
p = sys.argv[1]; d = json.load(open(p, encoding="utf-8"))
d["plugins"].insert(1, {"name": "aaa-kit", "source": "./aaa-kit", "description": "x", "version": "0.1.0"})
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
PY
  fi
  (cd "$d" && git init -q && git add -A && git -c user.name=t -c user.email=t@e commit -qm i) || exit 2
}
for c in same mid; do
  mkcopy "$c" "$([ "$c" = mid ] && echo 1 || echo 0)"
  kits=$(python3 -c 'import json,sys; [print(p["name"]) for p in json.load(open(sys.argv[1],encoding="utf-8"))["plugins"] if p["name"]!="harness"]' "$T/$c/.claude-plugin/marketplace.json")
  n=4; s2=""; s3=""; bad=0
  while IFS= read -r k; do
    n=$((n + 1))
    out=$(bash "$T/$c/scripts/spawn-kaizen-phase.sh" "$n" 2>/dev/null); rc=$?
    [ "$rc" = 0 ] || bad=$((bad + 1))
    sec=$(printf '%s\n' "$out" | sed -n -E 's/^\*\*참조 섹션:\*\* (.*)$/\1/p' | head -1)
    case "$sec" in *§2*) s2="$s2,$k" ;; esac
    case "$sec" in *§3*) s3="$s3,$k" ;; esac
  done <<< "$kits"
  echo "$c s2=${s2#,} s3=${s3#,} bad_rc=$bad"
done
