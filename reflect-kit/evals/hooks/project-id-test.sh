#!/usr/bin/env bash
# _lib-project-id.sh 시험 — 본 레포 root 와 로그 폴더 이름을 답을 아는 git 배치로 잰다.
# --show-toplevel 만 쓰면 링크된 워크트리가 워크트리 폴더 이름으로 갈린다 — 워크트리 경우가 잡는다.
# 공통 git 폴더의 부모를 조건 없이 쓰면 서브모듈이 상위 레포의 modules 로 묶인다 — 서브모듈 경우가 잡는다.
# 다른 사본으로 돌리기: PROJECT_ID_LIB=<사본 경로> bash project-id-test.sh
set -u
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
LIB=${PROJECT_ID_LIB:-$(cd "$HERE/../../hooks" && pwd)/_lib-project-id.sh}
[ -f "$LIB" ] || { echo "라이브러리가 없다 — $LIB"; exit 2; }
command -v git >/dev/null 2>&1 || { echo "git 이 없다"; exit 2; }

W=$(mktemp -d "${TMPDIR:-/tmp}/pit.XXXXXX") || exit 2
W=$(cd "$W" && pwd -P)
trap 'rm -rf "$W"' EXIT
g() { git -c user.name=t -c user.email=t@t -c init.defaultBranch=main -c protocol.file.allow=always "$@" > /dev/null 2>&1; }
mkrepo() { mkdir -p "$1" && g -C "$1" init && printf 'x\n' > "$1/f" && g -C "$1" add f && g -C "$1" commit -m init; }

# 배치 — 본 레포와 그 워크트리 · git 밖 폴더 · 서브모듈 · 다른 곳에 둔 git 폴더 · bare 레포의 워크트리 · 같은 이름의 다른 레포
mkrepo "$W/repos/alpha" || exit 2
mkdir -p "$W/repos/alpha/sub" "$W/wt" "$W/plain/gamma"
g -C "$W/repos/alpha" worktree add "$W/wt/alpha-wt" -b wt1 || exit 2
mkdir -p "$W/wt/alpha-wt/sub"
mkrepo "$W/src/libx" || exit 2
mkrepo "$W/repos/super" || exit 2
g -C "$W/repos/super" submodule add "$W/src/libx" libx || exit 2
mkdir -p "$W/gitdirs"
g init --separate-git-dir="$W/gitdirs/delta.git" "$W/repos/delta" || exit 2
g clone --bare "$W/repos/alpha" "$W/repos/eps.git" || exit 2
g -C "$W/repos/eps.git" worktree add "$W/wt/eps-main" main || exit 2
mkrepo "$W/other/alpha" || exit 2
g -C "$W/other/alpha" worktree add "$W/wt/alpha-other-wt" -b wt2 || exit 2
for d in "$W/wt/alpha-wt" "$W/repos/super/libx" "$W/repos/delta" "$W/wt/eps-main" "$W/wt/alpha-other-wt"; do
  [ -d "$d" ] || { echo "배치 실패 — $d"; exit 2; }
done

n=0; bad=0
check() {  # check <이름> <답> <값>
  n=$((n + 1))
  if [ "$2" = "$3" ]; then echo "일치 $1 = $3"
  else echo "불일치 $1 = $3 (답 $2)"; bad=$((bad + 1)); fi
}
root() { bash -c '. "$1" 2>/dev/null; project_root "$2"' _ "$LIB" "$1" 2>/dev/null; }
pid() { REFLECT_KIT_LOGS_ROOT="$W/logs" bash -c '. "$1" 2>/dev/null; compute_project_id "$2"' _ "$LIB" "$1" 2>/dev/null; }

check "root 본 레포" "$W/repos/alpha" "$(root "$W/repos/alpha")"
check "root 본 레포 하위" "$W/repos/alpha" "$(root "$W/repos/alpha/sub")"
check "root 워크트리" "$W/repos/alpha" "$(root "$W/wt/alpha-wt")"
check "root 워크트리 하위" "$W/repos/alpha" "$(root "$W/wt/alpha-wt/sub")"
check "root git 밖" "$W/plain/gamma" "$(root "$W/plain/gamma")"
check "root 서브모듈" "$W/repos/super/libx" "$(root "$W/repos/super/libx")"
check "root 다른 곳에 둔 git 폴더" "$W/repos/delta" "$(root "$W/repos/delta")"
check "root bare 레포의 워크트리" "$W/wt/eps-main" "$(root "$W/wt/eps-main")"
check "root 없는 경로" "$W/nope" "$(root "$W/nope")"

# 로그 폴더 이름 — 본 레포와 워크트리가 한 폴더, 같은 이름의 다른 레포와 그 워크트리가 다른 한 폴더
check "id 본 레포" alpha "$(pid "$W/repos/alpha")"
check "id 워크트리" alpha "$(pid "$W/wt/alpha-wt")"
check "마커는 본 레포 root" "$W/repos/alpha" "$(cat "$W/logs/alpha/.project-root" 2>/dev/null)"
h=$(bash -c '. "$1" 2>/dev/null; _rk_hash6 "$2"' _ "$LIB" "$W/other/alpha")
check "id 같은 이름 다른 레포" "alpha-$h" "$(pid "$W/other/alpha")"
check "id 그 레포의 워크트리" "alpha-$h" "$(pid "$W/wt/alpha-other-wt")"
check "id 서브모듈" libx "$(pid "$W/repos/super/libx")"

# zsh 로 source 해도 쓰기 id 가 같다 — 훅 밖의 스킬이 zsh 에서 부른다
if command -v zsh >/dev/null 2>&1; then
  check "zsh id 워크트리" alpha "$(REFLECT_KIT_LOGS_ROOT="$W/logs" zsh -c '. "$1" 2>/dev/null; compute_project_id "$2"' _ "$LIB" "$W/wt/alpha-wt" 2>/dev/null)"
else
  echo "건너뜀 zsh 없음"
fi

echo "결과: $n 경우 중 불일치 $bad"
[ "$bad" = 0 ]
