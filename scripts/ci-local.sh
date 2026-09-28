#!/usr/bin/env bash
# ci-local.sh [--list] <레포 폴더> — CI 파일(.github/workflows/ci.yml)의 run 단계를 로컬에서 차례대로 돌린다.
# 단계 목록을 여기 적어 두지 않고 CI 파일을 그때그때 읽는다 — 옛 손 목록 도구는 CI 에 더한 다섯 단계를 몰랐다(2026-09-28).
#
# 단계마다 한 줄:
#   --list  RUN <job> <이름> · SKIP <job> <이름> (<사유>) · UNSUPPORTED <job> <이름> (<사유>)
#   실행    PASS <job> <이름> rc=0 · FAIL <job> <이름> rc=<n> (그 뒤에 로그 끝 20 줄) · SKIP · UNSUPPORTED 는 같다
# 끝 줄: steps=<run 단계 수> run=<돌린 수> skip=<건너뛴 수> unsupported=<못 다룬 수> [failed=<실패 수>]
#
# SKIP 은 준비 단계다 — 명령이 pip install · npm ci · playwright install · apt-get install 인 단계. 로컬에는 미리 해 둔다.
# UNSUPPORTED 는 name · run 밖의 열쇠(if · working-directory · env · shell 등)가 든 단계다. 뜻을 흉내 내지 않고 알린다.
# 종료 코드는 harness/evals/gate-exit-codes.md — 0 모두 통과 · 1 실패나 못 다룬 단계가 있음 · 2 CI 파일이 없거나 못 읽음

list_only=0
case ${1:-} in
  -h|--help) sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
  --list) list_only=1; shift ;;
esac
repo=${1:-}
[ -n "$repo" ] || { echo "사용법: ci-local.sh [--list] <레포 폴더>" >&2; exit 2; }
workflow=$repo/.github/workflows/ci.yml
[ -f "$workflow" ] || { echo "CI 파일이 없다: $workflow" >&2; exit 2; }

work=$(mktemp -d "${TMPDIR:-/tmp}/ci-local.XXXXXX") || exit 2
trap 'rm -rf "$work"' EXIT

# 단계마다 한 줄: <종류>\t<job>\t<이름>\t<명령 파일>\t<사유>. 명령은 파일로 넘겨 여러 줄 run 도 그대로 돈다
python3 - "$workflow" "$work" >"$work/steps.tsv" <<'PY' || { echo "CI 파일을 읽지 못했다: $workflow" >&2; exit 2; }
import re, sys
import yaml

SETUP = re.compile(r"\b(pip install|npm ci|playwright install|apt-get install)\b")
workflow, work = sys.argv[1], sys.argv[2]
with open(workflow, encoding="utf-8") as handle:
    jobs = yaml.safe_load(handle)["jobs"]
index = 0
for job, body in jobs.items():
    for step in body.get("steps", []):
        if "run" not in step:
            continue
        index += 1
        name = str(step.get("name") or step["run"].strip().splitlines()[0])
        command_file = f"{work}/step-{index}.sh"
        with open(command_file, "w", encoding="utf-8") as out:
            out.write(step["run"])
        extra = sorted(set(step) - {"name", "run"})
        if extra:
            kind, reason = "UNSUPPORTED", "다루지 않는 열쇠: " + ", ".join(extra)
        elif SETUP.search(step["run"]):
            kind, reason = "SKIP", "준비 단계 — 로컬에는 미리 해 둔다"
        else:
            kind, reason = "RUN", ""
        print("\t".join([kind, job, name, command_file, reason]))
PY

steps=0; ran=0; skipped=0; unsupported=0; failed=0
while IFS="$(printf '\t')" read -r kind job name command_file reason; do
  steps=$((steps + 1))
  case $kind in
    SKIP) skipped=$((skipped + 1)); echo "SKIP $job $name ($reason)"; continue ;;
    UNSUPPORTED) unsupported=$((unsupported + 1)); echo "UNSUPPORTED $job $name ($reason)"; continue ;;
  esac
  ran=$((ran + 1))
  if [ "$list_only" = 1 ]; then echo "RUN $job $name"; continue; fi
  # CI 러너의 기본 셸과 같게 부른다 (bash --noprofile --norc -eo pipefail)
  (cd "$repo" && bash --noprofile --norc -eo pipefail "$command_file") >"$work/log" 2>&1 </dev/null
  rc=$?
  if [ "$rc" = 0 ]; then echo "PASS $job $name rc=0"
  else
    failed=$((failed + 1)); echo "FAIL $job $name rc=$rc"
    tail -20 "$work/log" | sed 's/^/    /'
  fi
done <"$work/steps.tsv"

if [ "$list_only" = 1 ]; then
  echo "steps=$steps run=$ran skip=$skipped unsupported=$unsupported"
else
  echo "steps=$steps run=$ran skip=$skipped unsupported=$unsupported failed=$failed"
fi
[ "$failed" = 0 ] && [ "$unsupported" = 0 ]
