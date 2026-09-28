#!/usr/bin/env bash
# m-hs.sh <레포> <판> — <판> 의 sprint-contract SKILL.md Step 0.5 가 적은 superseded 확인 부르기를 세 환경에서 돌린다.
# 부르기 = Step 0.5 절(`### 0.5. ` ~ `### 1. `)에서 `check-superseded.sh` 를 담은 첫 ```bash 덩어리.
#          덩어리가 없으면 그 절의 백틱 인라인 명령 `bash …check-superseded.sh …` 한 줄.
# 환경 셋 (레포는 읽기만, 나머지는 임시 폴더):
#   repo   — cwd · CONTRACT_ROOT = <레포>, CLAUDE_PLUGIN_ROOT 빈 값
#   plugin — cwd · CONTRACT_ROOT = harness 없는 임시 프로젝트, CLAUDE_PLUGIN_ROOT = 스크립트를 담은 임시 플러그인 폴더
#   market — cwd · CONTRACT_ROOT = 같은 임시 프로젝트, CLAUDE_PLUGIN_ROOT 빈 값, HOME = 마켓 설치본만 둔 임시 폴더
# 셸 bash · zsh 각각. 출력: `hs <판> <셸> repo=<rc> plugin=<rc> market=<rc>` 두 줄,
# 끝 줄 `hs <판> feedback_repo_rel=<Step 9 · 10 에 남은 `bash harness/scripts/(save|verify)-feedback.sh` 수>`.
R=${1:?레포}; REV=${2:?판}
T=$(mktemp -d "${TMPDIR:-/tmp}/mhs.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT
git -C "$R" show "$REV:harness/skills/sprint-contract/SKILL.md" > "$T/skill.md" || exit 2
awk '/^### 0\.5\. /{on=1} /^### 1\. /{on=0} on' "$T/skill.md" > "$T/sec"
awk '/^[[:space:]]*```bash/{b=1; buf=""; next} b && /^[[:space:]]*```/{b=0; if (buf ~ /check-superseded\.sh/) { printf "%s", buf; exit } next} b{buf=buf $0 "\n"}' "$T/sec" > "$T/snip.sh"
if [ ! -s "$T/snip.sh" ]; then
  # shellcheck disable=SC2016  # 백틱은 찾을 글자다
  grep -oE '`bash [^`]*check-superseded\.sh[^`]*`' "$T/sec" | head -1 | tr -d '`' > "$T/snip.sh"
fi
[ -s "$T/snip.sh" ] || { echo "STOP $REV Step 0.5 에 check-superseded 부르기가 없다"; exit 2; }
mkdir -p "$T/proj/.harness" "$T/plug/scripts" "$T/plug/references" "$T/home/.claude/plugins/marketplaces/m/harness/scripts" "$T/home/.claude/plugins/marketplaces/m/harness/references"
cp "$R/harness/scripts/"*.sh "$T/plug/scripts/"
cp "$R/harness/scripts/"*.sh "$T/home/.claude/plugins/marketplaces/m/harness/scripts/"
# 설치본 모양 — 스크립트가 옆 폴더 references/contract-schema.md 를 읽는다
cp "$R/harness/references/contract-schema.md" "$T/plug/references/"
cp "$R/harness/references/contract-schema.md" "$T/home/.claude/plugins/marketplaces/m/harness/references/"
printf -- '---\nstatus: superseded\nsuperseded_by: b\n---\n' > "$T/proj/.harness/sprint-contract-a.md"
printf -- '---\nstatus: active\n---\n' > "$T/proj/.harness/sprint-contract-b.md"
for sh in bash zsh; do
  zf=""; [ "$sh" = zsh ] && zf=-f  # zsh 는 사용자 설정을 읽지 않게
  run() {  # run <cwd> <plugin root> <home>
    (cd "$1" && env HOME="$3" CLAUDE_PLUGIN_ROOT="$2" CONTRACT_ROOT="$1" "$sh" ${zf:+"$zf"} "$T/snip.sh" >/dev/null 2>&1); echo $?
  }
  echo "hs $REV $sh repo=$(run "$R" '' "$HOME") plugin=$(run "$T/proj" "$T/plug" "$T/nohome") market=$(run "$T/proj" '' "$T/home")"
done
echo "hs $REV feedback_repo_rel=$(grep -cE 'bash harness/scripts/(save|verify)-feedback\.sh' "$T/skill.md")"
