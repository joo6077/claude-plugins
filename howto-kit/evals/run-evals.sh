#!/bin/sh
# run-evals.sh — evals.json 의 케이스를 zsh · bash · sh 세 셸에서 실행해 대조하고,
# 스킬 본문 · README 에서 게이트를 부르는 bash 블록을 그대로 뽑아 실제로 돌린다.
# 사용: sh howto-kit/evals/run-evals.sh   (bash · zsh 로 실행해도 같다)
#
# 오라클은 **실행 결과**다. 서술 존재로 통과시키지 않는다.
# 셸 출력이 하나라도 다르면 그 자체가 FAIL 이다 — 셸 이식성 결함은 한쪽에서만 조용히 통과한다.
# 실측 2026-09-08: `set -- $var` 가 zsh 에서 단어분할되지 않아 G5·G6 위반이 zsh 에서만
# GATE_PASS 로 샜다. 한쪽 셸만 돌렸으면 못 잡았을 결함이다.
# 실측 2026-09-24: howto-audit 블록이 부모 셸에서 읽은 함수를 find -exec sh -c 자식에서 불러
# 파일마다 command not found 였다. 게이트 케이스만 돌리던 이 러너는 그것을 못 잡았다.

KIT_DIR=$(cd "$(dirname "$0")/.." && pwd)
EVALS="$KIT_DIR/evals/evals.json"
GATE="$KIT_DIR/scripts/howto-gate.sh"

[ -f "$EVALS" ] || { echo "EVALS_MISSING $EVALS"; exit 2; }
[ -f "$GATE" ]  || { echo "GATE_MISSING $GATE"; exit 2; }
command -v zsh  >/dev/null 2>&1 || { echo "SHELL_MISSING zsh — 양쪽 셸 대조가 불가하다"; exit 2; }
command -v bash >/dev/null 2>&1 || { echo "SHELL_MISSING bash"; exit 2; }
command -v git  >/dev/null 2>&1 || { echo "TOOL_MISSING git — 게이트를 부르는 블록을 git 저장소 안에서 돌려 볼 수 없다"; exit 2; }

if ! { TSV=$(mktemp) && RESULT=$(mktemp) && ASSERTS=$(mktemp) && BLK=$(mktemp -d); }; then
  echo "TMP_FAIL"; exit 2
fi
trap 'rm -rf "$TSV" "$RESULT" "$ASSERTS" "$BLK"' EXIT INT TERM
# git 은 실제 경로를 돌려준다 — 기대 경로도 실제 경로로 맞춘다
BLK=$(cd "$BLK" && pwd -P) || exit 2

python3 - "$EVALS" > "$TSV" <<'PY'
import json, sys
with open(sys.argv[1], encoding='utf-8') as f:
    data = json.load(f)
for entry in data['cases']:
    print('\t'.join([entry['id'], entry['fixture'], entry['expect_final'], '|'.join(entry['assertions'])]))
PY

record() {   # record <id> <problems> <상세> — PASS/FAIL 한 줄을 찍고 결과 파일에 1 · 0 한 줄
  if [ -z "$2" ]; then
    echo "PASS  $1"; echo 1 >> "$RESULT"
  else
    echo "FAIL  $1 —$2"
    [ -z "$3" ] || printf '%s\n' "$3"
    echo 0 >> "$RESULT"
  fi
}

while IFS='	' read -r id fixture expect asserts; do
  [ -n "$id" ] || continue

  if [ "${fixture#__NONEXISTENT__}" != "$fixture" ]; then
    target="/__howto_kit_nonexistent__/x.md"
  else
    target="$KIT_DIR/evals/$fixture"
  fi

  out_zsh=$(zsh  -c ". '$GATE'; howto_gate '$target'" 2>&1)
  out_bash=$(bash -c ". '$GATE'; howto_gate '$target'" 2>&1)
  out_sh=$(sh -c ". '$GATE'; howto_gate '$target'" 2>&1)

  problems=""
  [ "$out_zsh" = "$out_bash" ] || problems="$problems shell_mismatch"
  [ "$out_sh" = "$out_bash" ]  || problems="$problems shell_mismatch_sh"
  printf '%s\n' "$out_bash" | grep -q "^$expect" || problems="$problems final_expected=$expect"

  # assertion 을 한 줄씩 파일로 받아 돈다. 따옴표 없는 변수를 for 로 돌리면 zsh 가 쪼개지 않아
  # 여러 줄이 한 패턴으로 grep -F 에 들어가고, 그중 하나만 맞아도 통과한다 (2026-09-25 실측).
  missing=""
  printf '%s\n' "$asserts" | tr '|' '\n' > "$ASSERTS"
  while IFS= read -r assertion; do
    [ -n "$assertion" ] || continue
    printf '%s\n' "$out_bash" | grep -qF -- "$assertion" || missing="$missing
    MISSING_ASSERT: $assertion"
  done < "$ASSERTS"

  [ -z "$missing" ] || problems="$problems missing_assert"

  detail=""
  if [ -n "$problems" ]; then
    detail="$(printf '%s\n' "$missing" | grep .)
  --- bash 출력 ---
$(printf '%s\n' "$out_bash" | sed 's/^/  /')"
    [ "$out_zsh" = "$out_bash" ] || detail="$detail
  --- zsh 출력 (다름) ---
$(printf '%s\n' "$out_zsh" | sed 's/^/  /')"
    [ "$out_sh" = "$out_bash" ] || detail="$detail
  --- sh 출력 (다름) ---
$(printf '%s\n' "$out_sh" | sed 's/^/  /')"
  fi
  record "$id" "$problems" "$detail"
done < "$TSV"

# 스킬 본문 · README 에서 게이트를 부르는 ```bash 블록을 뽑아 네 경우에서 zsh · bash 로 돌린다.
#   plugin  CLAUDE_PLUGIN_ROOT 자리를 킷 경로 글자로 바꾼다 (플러그인으로 불렀을 때 치환되는 모양)
#   repo    git 최상위 폴더에 howto-kit/ 이 있다
#   market  마켓플레이스 설치본에만 있다
#   none    어디에도 없다 — MISSING: 을 찍고 0 이 아닌 코드로 끝나야 한다
# find 뒤의 <…> 는 픽스처 사본 폴더로, howto_gate 뒤의 <…> 는 그 안의 파일 하나로 바꾼다.
# 사본은 이름순 앞 셋이다 — 파일마다 도는지는 셋으로 가려지고, 열다섯 전부면 러너 시간이 두 배를 넘는다
# (2026-09-25 실측 20 초 대 9 초).
unset CLAUDE_PLUGIN_ROOT
if ! { mkdir -p "$BLK/docs" "$BLK/work" "$BLK/home0" "$BLK/homem/.claude/plugins/marketplaces/mk" "$BLK/repo" \
  && find "$KIT_DIR/evals/fixtures" -type f -name '*.md' | sort | head -3 \
     | while IFS= read -r src; do cp "$src" "$BLK/docs/" || exit 1; done \
  && cp -R "$KIT_DIR" "$BLK/homem/.claude/plugins/marketplaces/mk/howto-kit" \
  && cp -R "$KIT_DIR" "$BLK/repo/howto-kit" \
  && git -C "$BLK/repo" init -q; }; then
  echo "BLOCK_SETUP_FAIL"; exit 2
fi

python3 - "$KIT_DIR" "$BLK" "$EVALS" > "$BLK/blocks.tsv" <<'PY' || { echo "BLOCK_EXTRACT_FAIL"; exit 2; }
import json, os, re, sys
kit, blk, evals = sys.argv[1:4]
declared = json.load(open(evals, encoding="utf-8")).get("gate_blocks") or {}
docs = os.path.join(blk, "docs")
names = sorted(name for name in os.listdir(docs) if name.endswith(".md"))
if not names:
    sys.exit(1)
one = os.path.join(docs, names[0])
scan = []
for root, dirs, files in os.walk(kit):
    dirs[:] = sorted(sub for sub in dirs if not (root == kit and sub == "evals"))
    scan += [os.path.relpath(os.path.join(root, name), kit) for name in sorted(files) if name.endswith(".md")]
for rel in sorted(set(scan) | set(declared)):
    blocks = []
    if rel in scan:
        buf, inb = [], False
        for ln in open(os.path.join(kit, rel), encoding="utf-8").read().split("\n"):
            # sh · shell · zsh 펜스도 센다 — bash 만 보면 다른 펜스로 쓴 블록이 수 대조와 실행에서 함께 빠진다 (2026-09-25 교차 진단)
            if not inb and ln.strip() in ("```bash", "```sh", "```shell", "```zsh"):
                inb, buf = True, []
            elif inb and ln.strip() == "```":
                inb = False
                if re.search(r"\bhowto_gate\s", "\n".join(buf)):
                    blocks.append("\n".join(buf) + "\n")
            elif inb:
                buf.append(ln)
    print("DECL\t%s\t%d\t%d" % (rel, declared.get(rel, 0), len(blocks)))
    stem = rel.split("/")[-2] if rel.endswith("/SKILL.md") else re.sub(r"[^a-z0-9]+", "-", rel.lower()).strip("-")
    for seq, body in enumerate(blocks, 1):
        bid = "%s-%d" % (stem, seq)
        body, nd = re.subn(r"(find\s+)<[^<>\n]+>", lambda hit: hit.group(1) + '"' + docs + '"', body)
        body, nf = re.subn(r"(howto_gate\s+)<[^<>\n]+>", lambda hit: hit.group(1) + '"' + one + '"', body)
        if (nd, nf) == (1, 0) and "<" not in body:
            kind, expect = "dir", len(names)
        elif (nd, nf) == (0, 1) and "<" not in body:
            kind, expect = "file", 1
        else:
            kind, expect = "bad", 0
        open(os.path.join(blk, bid + ".sh"), "w", encoding="utf-8").write(body)
        open(os.path.join(blk, bid + ".plugin.sh"), "w", encoding="utf-8").write(body.replace("${CLAUDE_PLUGIN_ROOT}", kit))
        print("BLOCK\t%s\t%s\t%d" % (bid, kind, expect))
PY

decl_bad=""
while IFS='	' read -r tag rel declared found; do
  [ "$tag" = DECL ] && [ "$declared" != "$found" ] && decl_bad="$decl_bad $rel:declared=$declared,found=$found"
done < "$BLK/blocks.tsv"
record "blocks-declared" "$decl_bad" ""

while IFS='	' read -r tag bid kind expect; do
  [ "$tag" = BLOCK ] || continue
  for where in plugin repo market none; do
    script="$BLK/$bid.sh"; cwd="$BLK/work"; home="$BLK/home0"
    case $where in
      plugin) script="$BLK/$bid.plugin.sh"; want="RESOLVED: $KIT_DIR/scripts/howto-gate.sh" ;;
      repo)   cwd="$BLK/repo"; want="RESOLVED: $BLK/repo/howto-kit/scripts/howto-gate.sh" ;;
      market) home="$BLK/homem"; want="RESOLVED: $BLK/homem/.claude/plugins/marketplaces/mk/howto-kit/scripts/howto-gate.sh" ;;
      none)   want="" ;;
    esac
    oz=$(cd "$cwd" && HOME=$home GIT_CEILING_DIRECTORIES=$BLK zsh "$script" 2>&1); rz=$?
    ob=$(cd "$cwd" && HOME=$home GIT_CEILING_DIRECTORIES=$BLK bash "$script" 2>&1); rb=$?

    problems=""
    [ "$kind" != bad ] || problems="$problems placeholder"
    [ "$oz" = "$ob" ] && [ "$rz" = "$rb" ] || problems="$problems shell_mismatch"
    first=$(printf '%s\n' "$ob" | head -1)
    verdicts=$(printf '%s\n' "$ob" | grep -cE '^GATE_(PASS|FAIL|BLOCKED)')
    heads=$(printf '%s\n' "$ob" | grep -c '^### ')
    notfound=$(printf '%s\n' "$ob" | grep -ci 'not found')
    [ "$notfound" -eq 0 ] || problems="$problems not_found=$notfound"
    if [ "$where" = none ]; then
      case $first in "MISSING: "*) ;; *) problems="$problems first_line" ;; esac
      [ "$rb" -ne 0 ] || problems="$problems rc=0"
      [ "$verdicts" -eq 0 ] || problems="$problems verdicts=$verdicts"
    else
      [ "$first" = "$want" ] || problems="$problems first_line"
      [ "$rb" -eq 0 ] || problems="$problems rc=$rb"
      [ "$verdicts" -eq "$expect" ] || problems="$problems verdicts=$verdicts/$expect"
      [ "$kind" != dir ] || [ "$heads" -eq "$expect" ] || problems="$problems heads=$heads/$expect"
    fi

    detail=""
    [ -z "$problems" ] || detail="  --- bash 출력 (rc=$rb) ---
$(printf '%s\n' "$ob" | head -5 | sed 's/^/  /')"
    record "$bid:$where" "$problems" "$detail"
  done
done < "$BLK/blocks.tsv"

total=$(grep -c . "$RESULT" 2>/dev/null || echo 0)
passed=$(grep -c '^1$' "$RESULT" 2>/dev/null || echo 0)
failed=$((total - passed))

echo
echo "EVALS total=$total pass=$passed fail=$failed"
if [ "$failed" -eq 0 ] && [ "$total" -gt 0 ]; then
  echo EVALS_PASS; exit 0
else
  echo EVALS_FAIL; exit 1
fi
