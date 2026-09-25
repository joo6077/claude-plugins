#!/bin/sh
# run-gate-evals.sh — evals.json 의 gate_cases 입력마다 guide_gate 를 zsh · bash 로 돌려 기대 출력 전체와 대조한다.
# 사용: sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh   (어느 폴더에서 불러도 된다)
# 종료 코드: 0 전부 통과 · 1 한 건 이상 실패 · 2 돌릴 수 없음 (도구 · 함수 추출 · 입력 목록)
#
# 함수는 부를 때마다 SKILL.md 에서 뽑는다 — 사본을 두면 SKILL.md 를 고쳐도 시험은 옛 함수를 잰다.
# 폴더에만 있고 gate_cases 에 없는 픽스처는 실패로 센다 — 입력 셋이 등록 없이 폴더에만 남아 한 번도 안 돌았다 (2026-09-24).

EVAL_DIR=$(cd "$(dirname "$0")" && pwd) || exit 2
SKILL=$EVAL_DIR/../SKILL.md
EVALS=$EVAL_DIR/evals.json

for t in zsh bash python3; do
  command -v "$t" >/dev/null 2>&1 || { echo "TOOL_MISSING $t — 두 셸 대조를 할 수 없다"; exit 2; }
done
[ -f "$SKILL" ] || { echo "SKILL_MISSING $SKILL"; exit 2; }
[ -f "$EVALS" ] || { echo "EVALS_MISSING $EVALS"; exit 2; }

W=$(mktemp -d "${TMPDIR:-/tmp}/ob-gate.XXXXXX") || exit 2
trap 'rm -rf "$W"' EXIT INT TERM

awk '/^guide_gate\(\) \{/{p=1} p{print} p&&/^\}$/{exit}' "$SKILL" > "$W/gate.sh"
if ! head -1 "$W/gate.sh" | grep -qx 'guide_gate() {' || ! tail -1 "$W/gate.sh" | grep -qx '}'; then
  echo "GATE_EXTRACT_FAIL — SKILL.md 에서 guide_gate 함수를 뽑지 못했다"; exit 2
fi

# 구분자를 탭이 아니라 | 로 둔다 — 탭은 IFS 공백이라 빈 칸이 붙어 사라진다 (빈 스택 케이스가 그렇다)
if ! python3 - "$EVALS" "$EVAL_DIR" "$W" > "$W/cases.txt" <<'PY'
import json, os, sys
evals, edir, w = sys.argv[1:4]
with open(evals, encoding="utf-8") as f:
    cases = json.load(f).get("gate_cases") or []
used = set()
for n, c in enumerate(cases, 1):
    st = c["stack"]
    mode = "none" if st is None else ("empty" if st == "" else "value")
    print("|".join(["CASE", str(n), c["id"], c["fixture"], mode, st or ""]))
    with open(os.path.join(w, f"{n}.expect"), "w", encoding="utf-8") as g:
        g.write("\n".join(c["expect"]) + "\n")
    used.add(os.path.normpath(c["fixture"]))
fx = os.path.join(edir, "fixtures")
for name in sorted(os.listdir(fx)) if os.path.isdir(fx) else []:
    rel = os.path.normpath(os.path.join("fixtures", name))
    if name.endswith(".md") and rel not in used:
        print("|".join(["ORPHAN", rel]))
print("|".join(["DECLARED", str(len(cases))]))
PY
then
  echo "EVALS_UNREADABLE $EVALS — gate_cases 를 읽지 못했다"; exit 2
fi

declared=$(sed -n 's/^DECLARED|//p' "$W/cases.txt")
[ "${declared:-0}" -gt 0 ] || { echo "NO_CASES — evals.json 에 gate_cases 가 없다"; exit 2; }

ran=0; failed=0
while IFS='|' read -r kind n id fixture mode stack; do
  case $kind in
    ORPHAN) echo "FAIL  orphan_fixture $n — gate_cases 에 없다"; failed=$((failed + 1)); continue ;;
    CASE) ;;
    *) continue ;;
  esac
  ran=$((ran + 1))
  target=$EVAL_DIR/$fixture
  case $mode in
    none)  call="guide_gate '$target'";             shown="(인자 없음)" ;;
    empty) call="guide_gate '$target' ''";          shown="(빈 문자열)" ;;
    *)     call="guide_gate '$target' '$stack'";    shown=$stack ;;
  esac
  label="$id ($fixture, stack=$shown)"
  if [ ! -f "$target" ]; then
    echo "FAIL  $label — fixture_missing"; failed=$((failed + 1)); continue
  fi
  zsh  -c ". '$W/gate.sh'; $call" > "$W/$n.zsh"  2>&1
  bash -c ". '$W/gate.sh'; $call" > "$W/$n.bash" 2>&1
  why=""
  cmp -s "$W/$n.zsh" "$W/$n.bash" || why="$why shell_mismatch"
  cmp -s "$W/$n.bash" "$W/$n.expect" || why="$why expect_mismatch"
  if [ -z "$why" ]; then
    echo "PASS  $label"
  else
    echo "FAIL  $label —$why"; failed=$((failed + 1))
    echo "  --- 기대 ---"; sed 's/^/  /' "$W/$n.expect"
    echo "  --- bash ---"; sed 's/^/  /' "$W/$n.bash"
    cmp -s "$W/$n.zsh" "$W/$n.bash" || { echo "  --- zsh ---"; sed 's/^/  /' "$W/$n.zsh"; }
  fi
done < "$W/cases.txt"

# 목록을 끝까지 못 읽고 멈추면 적게 돌고도 통과로 보인다 — 돈 수와 적힌 수를 맞춘다
[ "$ran" -eq "$declared" ] || { echo "FAIL  count_mismatch ran=$ran declared=$declared"; failed=$((failed + 1)); }

echo
echo "EVALS declared=$declared ran=$ran fail=$failed"
if [ "$failed" -eq 0 ]; then echo EVALS_PASS; exit 0; fi
echo EVALS_FAIL; exit 1
