#!/usr/bin/env bash
# m-phase.sh <레포> — Phase 부트스트랩의 번호 상한을 두 임시 사본(그대로 · 마켓 목록에 foo-kit 을 더함)에서 잰다.
# 사본은 git 저장소로 만들어 태그 · 상태 파일 쓰기가 레포 밖에서 일어나게 한다.
# 줄마다 `<사본> n=<번호> rc=<종료 코드> slug=<뽑힌 슬러그>`, 끝에 `<사본> help_1_17=<도움말의 「1 ~ 17」 수>`.
R=${1:?레포 경로}
T=$(mktemp -d "${TMPDIR:-/tmp}/mphase.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT
mkcopy() {  # mkcopy <이름> <foo 를 더할지 0|1>
  d=$T/$1; mkdir -p "$d"
  (cd "$R" && tar -cf - scripts .claude-plugin .harness/.meta/kaizen-data-pool.md .harness/.meta/kaizen-state.yaml) | tar -xf - -C "$d"
  if [ "$2" = 1 ]; then
    python3 - "$d/.claude-plugin/marketplace.json" <<'PY'
import json, sys
p = sys.argv[1]; d = json.load(open(p, encoding="utf-8"))
d["plugins"].append({"name": "foo-kit", "source": "./foo-kit", "description": "x", "version": "0.1.0"})
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
PY
  fi
  (cd "$d" && git init -q && git add -A && git -c user.name=t -c user.email=t@e commit -qm i) || exit 2
}
mkcopy same 0; mkcopy foo 1
for c in same foo; do
  for n in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19; do
    out=$(bash "$T/$c/scripts/spawn-kaizen-phase.sh" "$n" 2>&1); rc=$?
    printf '%s n=%s rc=%s slug=%s\n' "$c" "$n" "$rc" "$(printf '%s\n' "$out" | grep -oE 'kaizen-phase[0-9]+-[a-z0-9-]+' | head -1)"
  done
  printf '%s help_1_17=%s\n' "$c" "$(bash "$T/$c/scripts/spawn-kaizen-phase.sh" --help 2>&1 | grep -c '1 ~ 17')"
done
