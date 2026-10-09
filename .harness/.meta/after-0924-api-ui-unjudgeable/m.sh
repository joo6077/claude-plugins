# 계약 after-0924-api-ui-unjudgeable 측정 도우미. bash · zsh 둘 다에서 `. m.sh` 뒤 `m <이름>` 으로 부른다.
# 상한 U 는 이 스프린트 가지(chore/ak-c4a)가 합쳐졌으면 origin/main 병합 커밋의 둘째 부모(합친 가지 끝), 아니면 가지 끝이다.
# 바뀐 파일은 BASE..U 의 첫째 부모 줄에 있는 병합 아닌 커밋만 모은다 — 가지에 main 을 합쳐 넣었거나 main 위로 다시 얹어도 남의 변경이 섞이지 않는다.
W=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c4a
R=/Users/jackson/Hub/10_Dev/claude-plugins
D=$W/.harness/.meta/after-0924-api-ui-unjudgeable
BASE=f81568d8fbf58382172281388ec5d7756f9f46b2
MAIN_NEW=88ddfe5f1bb39699d2c69a53df33901a6697c00b
MOCK=${MOCK:-$R/.mockups}
V7=$MOCK/api-ui-v7.html
V8=$MOCK/api-ui-v8.html
V7SHA=c4bd563ec8b71a95f804ae1f96a0eda2d17bda8256ca9fbc327a527c3a81ca7a
CREATED='2026-09-26 14:15'
SK=api-kit/skills/api-ui/SKILL.md
VS=api-kit/skills/api-ui/references/viewer-spec.md
AL=api-kit/references/api-layout.md
RM=api-kit/README.md

fm_get() { # fm_get <file> <key>
  awk -v k="${2}" -v q="\"'" '
    NR==1 && /^---[[:space:]]*$/ { fm=1; next }
    fm && /^---[[:space:]]*$/    { exit }
    fm && index($0, k ":") == 1 {
      v = substr($0, length(k) + 2)
      sub(/^[[:space:]]+/, "", v); sub(/[[:space:]]+$/, "", v)
      c = substr(v, 1, 1)
      if (length(v) > 1 && index(q, c) > 0 && substr(v, length(v), 1) == c)
        v = substr(v, 2, length(v) - 2)
      print v; exit
    }' "${1}"
}
sha256_16() { shasum -a 256 | cut -c1-16; }
contract_digest() { grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "${1}" | sed -E 's/^- \[[ x]\]/- [ ]/' | sha256_16; }
verify_seal() {
  rec=$(fm_get "${1}" conditions_digest); rec=${rec#sha256:}
  if [ -z "$rec" ]; then echo "SEAL_ABSENT ${1}"; return 0; fi
  act=$(contract_digest "${1}")
  if [ "$rec" = "$act" ]; then echo "SEAL_OK ${1}"; else echo "SEAL_BROKEN ${1} recorded=$rec actual=$act"; fi
}
c4a_head() {
  hm=$(git -C "$W" log origin/main --merges --format=%H --grep='from joo6077/chore/ak-c4a$' -1)
  [ -n "$hm" ] && { git -C "$W" rev-parse "${hm}^2"; return 0; }
  git -C "$W" rev-parse --verify -q chore/ak-c4a && return 0
  echo "UNRESOLVED chore/ak-c4a" >&2; return 1
}
mine_files() { # 이 스프린트 커밋이 건드린 파일 (첫째 부모 줄 · 병합 제외)
  git -C "$W" log --first-parent --no-merges --format= --name-only "$BASE..$U" | grep . | LC_ALL=C sort -u
}
# U 판의 트리를 임시 폴더에 풀고 node_modules 를 이어 붙인다 — 작업 폴더의 커밋 안 된 변경이 섞이지 않게
# 같은 커밋이면 풀어 둔 폴더를 다시 쓴다. fresh 를 주면 매번 새로 풀고, 쓴 쪽이 지운다
tree_at() { # tree_at <ref> [fresh] → 폴더 경로
  sha=$(git -C "$W" rev-parse --verify -q "${1}^{commit}") || { echo "STOP 없는 커밋 ${1}" >&2; return 2; }
  if [ "${2:-}" = fresh ]; then tt=$(mktemp -d "${TMPDIR:-/tmp}/c4a-fresh.XXXXXX")
  else tt="${TMPDIR:-/tmp}/c4a-tree-$sha"; [ -d "$tt/api-kit" ] && { echo "$tt"; return 0; }; mkdir -p "$tt"; fi
  git -C "$W" archive "$sha" | tar -x -C "$tt" && ln -s "$W/node_modules" "$tt/node_modules" && echo "$tt"
}

m() {
  if [ -n "${UOVR:-}" ]; then U=$UOVR; else U=$(c4a_head) || return 2; fi
  for need in "$V7"; do [ -f "$need" ] || { echo "STOP 없는 파일 $need" >&2; return 2; }; done
  case "${1}" in
  HEAD) echo "U=$U" ;;
  SEAL)
    ( cd "${SEALROOT:-$W}" && find .harness -type f -name 'sprint-contract*.md' -print0 \
      | while IFS= read -r -d '' f; do verify_seal "$f"; done | awk '{print $1}' | sort | uniq -c ) ;;
  SCOPE)
    mine_files | grep -v '^\.harness/' | awk -v sk="$SK" -v vs="$VS" -v al="$AL" -v rm="$RM" '
      { p=$0; ok = (p==sk || p==vs || p==al || p==rm || p==".github/workflows/ci.yml" || index(p, "api-kit/evals/")==1)
        print (ok ? "IN  " : "OUT ") p; if (!ok) out++; seen[p]=1; if (index(p,"api-kit/evals/")==1) ev++ }
      END { miss=0; n=split(sk" "vs" "al" "rm" .github/workflows/ci.yml", need, " ")
            for (i=1;i<=n;i++) if (!(need[i] in seen)) { miss++; print "MISSING " need[i] }
            if (ev+0 == 0) { miss++; print "MISSING api-kit/evals/*" }
            printf "scope_out=%d required_missing=%d\n", out+0, miss }'
    # api-kit/README.md 는 AUTO:evals 블록 안만 바뀌어야 한다 — 블록 안쪽을 지운 두 판을 맞댄다
    autob() { awk '/<!-- AUTO:evals -->/ {print; s=1; next} /<!-- \/AUTO:evals -->/ {s=0} !s'; }
    git -C "$W" show "${BASE}:${RM}" | autob > "${TMPDIR:-/tmp}/c4a-rm-b"
    git -C "$W" show "${U}:${RM}" | autob > "${TMPDIR:-/tmp}/c4a-rm-u"
    printf 'readme_outside_auto=%s\n' "$(diff "${TMPDIR:-/tmp}/c4a-rm-b" "${TMPDIR:-/tmp}/c4a-rm-u" | grep -c '^[<>]')" ;;
  COMMITS)
    git -C "$W" log --first-parent --no-merges --format=%H "$BASE..$U" | while read -r c; do
      a=$(git -C "$W" show --name-only --format= "$c" | grep . | grep -v '^\.harness/' | awk -F/ '{ if ($1==".github") print ".github"; else print $1 }' | sort -u | tr '\n' ' ')
      n=$(printf '%s' "$a" | wc -w | tr -d ' ')
      echo "$c areas=[$a] n=$n"
    done | awk '{print} / n=([2-9]|[1-9][0-9])$/ {mixed++} END {printf "mixed=%d\n", mixed+0}' ;;
  MOCKUPS)
    printf 'v7_sha_same=%s\n' "$([ "$(shasum -a 256 "$V7" | cut -d' ' -f1)" = "$V7SHA" ] && echo 1 || echo 0)"
    find "$MOCK" -maxdepth 1 -type f -newermt "$CREATED" | sed 's#.*/##' | sort | awk '{print "NEW " $0; n++} END {printf "new_files=%d\n", n+0}' ;;
  IDS)
    [ -f "$V8" ] || { echo "STOP v8 없음 $V8" >&2; return 2; }
    grep -oE ' id="[^"$]+"' "$V7" | sort -u > "${TMPDIR:-/tmp}/c4a-ids7"; grep -oE ' id="[^"$]+"' "$V8" | sort -u > "${TMPDIR:-/tmp}/c4a-ids8"
    printf 'v7_ids=%s missing_in_v8=%s\n' "$(wc -l < "${TMPDIR:-/tmp}/c4a-ids7" | tr -d ' ')" "$(comm -23 "${TMPDIR:-/tmp}/c4a-ids7" "${TMPDIR:-/tmp}/c4a-ids8" | wc -l | tr -d ' ')" ;;
  CLASSES)
    [ -f "$V8" ] || { echo "STOP v8 없음 $V8" >&2; return 2; }
    for f in "$V7" "$V8"; do grep -oE 'class="[^"]*"' "$f" | sed -E 's/class="//; s/"$//' | tr ' ' '\n' | grep -vE '[$}{]' | grep . | sort -u; echo '--'; done \
      | awk '/^--$/ {k++; next} k==0 {a[$0]=1; next} !($0 in a) {print "NEWCLASS " $0; n++} END {printf "new_classes=%d\n", n+0}' ;;
  MD)
    MDL=${MDL:-/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/c4a/mdlint}
    [ -x "$MDL/node_modules/.bin/markdownlint-cli2" ] || { echo "STOP markdownlint-cli2 0.23.2 없음 — npm install --no-save markdownlint-cli2@0.23.2 를 $MDL 에서" >&2; return 2; }
    tb=$(tree_at "$BASE") && tu=$(tree_at "$U") || return 2
    mine_files | grep -v '^\.harness/' | grep '\.md$' | while read -r f; do
      for side in "$tb" "$tu"; do
        if [ -f "$side/$f" ]; then (cd "$side" && "$MDL/node_modules/.bin/markdownlint-cli2" --config "$MDL/.markdownlint-cli2.jsonc" "$f" 2>&1 | grep -E "^${f}:[0-9]+" | grep -oE 'MD[0-9]{3}' | sort | uniq -c | awk '{print $2"="$1}' | tr '\n' ' ')
        else printf 'absent'; fi; echo
      done | awk -v f="$f" 'NR==1{b=$0} NR==2{u=$0} END{
        n=split(b,x," "); for(i=1;i<=n;i++){split(x[i],y,"="); B[y[1]]=y[2]}
        n=split(u,x," "); for(i=1;i<=n;i++){split(x[i],y,"="); if (y[2]+0 > B[y[1]]+0) {up++; r=r" "y[1]":"B[y[1]]+0"->"y[2]}}
        printf "%s rules_up=%d%s\n", f, up+0, r}'
    done ;;
  VALID)
    tu=$(tree_at "$U" fresh) || return 2
    ( cd "$tu" && python3 scripts/validate-plugin.py api-kit > vp-own.txt 2>&1; echo "own_rc=$?"; grep -E '^  V' vp-own.txt | grep -vcE '— OK$|— SKIP \(no templates/\)$' | sed 's/^/own_bad=/'
      git -C "$W" show "${MAIN_NEW}:scripts/validate-plugin.py" > scripts/validate-plugin.py && git -C "$W" show "${MAIN_NEW}:scripts/plugin_utils.py" > scripts/plugin_utils.py
      python3 scripts/validate-plugin.py api-kit > vp-main.txt 2>&1; echo "main_rc=$?"; grep -E '^  V' vp-main.txt | grep -vcE '— OK$|— SKIP \(no templates/\)$' | sed 's/^/main_bad=/'
      grep -cE '^  V([1-9]|10) ' vp-own.txt | sed 's/^/own_lines=/'; grep -cE '^  V([1-9]|10) ' vp-main.txt | sed 's/^/main_lines=/' )
    rm -rf "$tu" ;;
  CLEAN) find "${TMPDIR:-/tmp}" -maxdepth 1 \( -name 'c4a-tree-*' -o -name 'c4a-fresh.*' -o -name 'c4a-ids*' \) -exec rm -rf {} + ; echo cleaned ;;
  PROBE) # m PROBE <이름> <ui.html 또는 U:<U 판 안 경로>>
    tu=$(tree_at "$U") || return 2
    case "${3}" in U:*) tgt="$tu/${3#U:}" ;; *) tgt="${3}" ;; esac
    [ -f "$tgt" ] || { echo "STOP 없는 파일 $tgt" >&2; return 2; }
    node "$D/probe-ui.cjs" "$tgt" "$D/cap" "${2}" "$tu/$SK" ;;
  EVALS)
    tu=$(tree_at "$U") || return 2
    ( cd "$tu" && python3 - <<'PY'
import json, pathlib, re
ev = pathlib.Path('api-kit/evals/evals.json')
if not ev.exists():
    print('evals_json=0'); raise SystemExit(0)
d = json.loads(ev.read_text(encoding='utf-8'))
cases = [c for c in d.get('cases', []) if c.get('skill') == 'api-ui']
print(f'evals_json=1 api_ui_cases={len(cases)}')
L = ['PASS', 'FAIL', '미실행', '판정 불가']
for c in cases:
    base = ev.parent
    fx, ex = base / str(c.get('fixture', '')), base / str(c.get('example', ''))
    api = fx / '.api'
    need = ['project.yaml', 'inventory.yaml', 'contracts', 'snapshots', 'reports']
    have = [n for n in need if (api / n).exists()]
    lines = []
    if (api / 'reports').exists():
        for f in (api / 'reports').rglob('*'):
            if f.is_file():
                lines += [ln for ln in f.read_text(encoding='utf-8', errors='replace').split('\n')
                          if re.search(r'=\(없음\) · .*→ 판정 불가\s*$', ln) or re.search(r'· .*=\(없음\) → 판정 불가\s*$', ln)]
    exp = c.get('expect', {})
    print(f"case={c.get('id')} fixture_api={len(have)}/{len(need)} example={'U:' + str(ex) if ex.is_file() else 'MISSING'} "
          f"expect={'/'.join(str(exp.get(k, '-')) for k in L)} fail_with_unjudged={exp.get('fail_with_unjudged', '-')} "
          f"assertions={len(c.get('assertions', []))} unjudged_lines={len(lines)}")
PY
    ) ;;
  EX7) # m EX7 <U:<예시 경로>> — §7 bash 블록을 예시에 돌리고 비밀 형태 · CSP 를 센다
    tu=$(tree_at "$U") || return 2
    ex="$tu/${2#U:}"; [ -f "$ex" ] || { echo "STOP 없는 파일 $ex" >&2; return 2; }
    blk=$(awk '/^## 7\./{s=1} s && /^```bash$/{f=1; next} f && /^```$/{exit} f' "$tu/$SK" | sed "s#^UI=.*#UI='$ex'#")
    printf '%s\n' "$blk" > "$tu/sec7.sh"; echo "--- sec7 block"; bash "$tu/sec7.sh"; echo "sec7_rc=$?"
    printf 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIn0.x Bearer abcdefgh12345\n' | grep -cE 'eyJ[A-Za-z0-9_-]{10,}\.|Bearer [A-Za-z0-9._-]{8,}' | sed 's/^/secret_positive=/'
    grep -cE 'eyJ[A-Za-z0-9_-]{10,}\.|Bearer [A-Za-z0-9._-]{8,}' "$ex" | sed 's/^/secret_hits=/'
    grep -cF "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'" "$ex" | sed 's/^/csp_lines=/' ;;
  CI)
    tu=$(tree_at "$U") || return 2
    ( cd "$tu" && python3 - <<'PY'
import json, yaml, subprocess, pathlib
ev = pathlib.Path('api-kit/evals/evals.json')
if not ev.exists():
    print('evals_json=0'); raise SystemExit(0)
runner = json.loads(ev.read_text(encoding='utf-8')).get('runner', '')
steps = yaml.safe_load(open('.github/workflows/ci.yml', encoding='utf-8'))['jobs']['playwright']['steps']
runs = [str(st.get('run', '')).strip() for st in steps]
inst = next((i for i, r in enumerate(runs) if r.startswith('npx playwright install')), -1)
hit = [i for i, r in enumerate(runs) if r == runner.strip()]
print(f'evals_json=1 runner=[{runner}] ci_step={len(hit)} after_install={int(bool(hit) and hit[0] > inst >= 0)}')
if runner:
    rc = subprocess.run(runner, shell=True, capture_output=True, text=True)
    print(f'runner_rc={rc.returncode}')
    print(rc.stdout[-1500:])
PY
    ) ;;
  LIT)
    tu=$(tree_at "$U") || return 2
    python3 "$D/lit.py" "$tu" "$V8" ;;
  MUT) # m MUT <example|skill> '<sed 식>' — 새로 푼 U 판에서 예시 ui.html 또는 api-ui SKILL.md 에 변이를 넣고 측정기와 시험 실행기를 돌린다
    tu=$(tree_at "$U" fresh) || return 2
    ex=$(cd "$tu" && python3 -c 'import json,pathlib; e=pathlib.Path("api-kit/evals"); c=[c for c in json.loads((e/"evals.json").read_text(encoding="utf-8"))["cases"] if c.get("skill")=="api-ui"][0]; print(e/c["example"])') || return 2
    case "${2}" in example) tg=$ex ;; skill) tg=$SK ;; *) echo "STOP 변이 대상은 example · skill" >&2; return 2 ;; esac
    cp "$tu/$tg" "$tu/$tg.orig" && sed -i '' -e "${3}" "$tu/$tg"
    diff "$tu/$tg.orig" "$tu/$tg" | grep -c '^>' | sed 's/^/mutated_lines=/'; rm -f "$tu/$tg.orig"
    node "$D/probe-ui.cjs" "$tu/$ex" "$tu/cap-mut" mut "$tu/$SK" | grep -E "chip\[판정 불가\]|sec7-expr|VERDICT"
    run=$(cd "$tu" && python3 -c 'import json; print(json.load(open("api-kit/evals/evals.json", encoding="utf-8"))["runner"])')
    ( cd "$tu" && sh -c "$run" > runner.log 2>&1; echo "runner_rc=$?" ); rm -rf "$tu" ;;
  SYNTAX) # 바뀐 js · json · yaml 파일을 읽어 본다
    tu=$(tree_at "$U") || return 2
    mine_files | grep -v '^\.harness/' | grep -E '\.(js|cjs|mjs|json|ya?ml)$' | while read -r f; do
      [ -f "$tu/$f" ] || continue
      case "$f" in
        *.js|*.cjs|*.mjs) node --check "$tu/$f" >/dev/null 2>&1 && r=ok || r=BAD ;;
        *.json) python3 -c 'import json,sys; json.load(open(sys.argv[1], encoding="utf-8"))' "$tu/$f" >/dev/null 2>&1 && r=ok || r=BAD ;;
        *) python3 -c 'import yaml,sys; yaml.safe_load(open(sys.argv[1], encoding="utf-8"))' "$tu/$f" >/dev/null 2>&1 && r=ok || r=BAD ;;
      esac; echo "$r $f"
    done | awk '{print} $1=="BAD"{b++} END{printf "syntax_files=%d syntax_bad=%d\n", NR, b+0}' ;;
  FM) # api-ui SKILL.md 첫 머리 설정 블록이 시작 판과 같은가. CTL_SED 를 주면 U 쪽에 그 변이를 끼운다(양성 대조)
    fmb() { awk 'NR==1 && /^---$/ {f=1; print; next} f {print} f && /^---$/ {exit}'; }
    git -C "$W" show "${BASE}:${SK}" | fmb > "${TMPDIR:-/tmp}/c4a-fm-b"
    git -C "$W" show "${U}:${SK}" | sed -e "${CTL_SED:-s/^//}" | fmb > "${TMPDIR:-/tmp}/c4a-fm-u"
    printf 'fm_lines=%s fm_diff=%s\n' "$(wc -l < "${TMPDIR:-/tmp}/c4a-fm-b" | tr -d ' ')" "$(diff "${TMPDIR:-/tmp}/c4a-fm-b" "${TMPDIR:-/tmp}/c4a-fm-u" | grep -c '^[<>]')" ;;
  VER) # 더한 줄에 api-kit plugin.json 판 번호가 몇 번 나오나 (예시 입력 폴더는 뺀다)
    v=$(git -C "$W" show "${U}:api-kit/.claude-plugin/plugin.json" | python3 -c 'import json,sys; print(json.load(sys.stdin)["version"])')
    n=$(git -C "$W" log --first-parent --no-merges -p -U0 --format= "$BASE..$U" -- . ':(exclude).harness' ':(exclude)api-kit/evals/fixtures' | grep '^+' | grep -v '^+++' | grep -cF "$v")
    printf 'version=%s added_hits=%s positive=%s\n' "$v" "$n" "$(printf '+v%s\n' "$v" | grep -cF "$v")" ;;
  CILOCAL) # CI 단계 전부를 U 판 사본에서 돌린다. 사본 · 기록 폴더는 CLEAN 이 지우지 않는 이름으로 따로 만든다
    ct=$(mktemp -d "${TMPDIR:-/tmp}/c4a-ci.XXXXXX") && co=$(mktemp -d "${TMPDIR:-/tmp}/c4a-cio.XXXXXX") || return 2
    git -C "$W" archive "$U" | tar -x -C "$ct" && ln -s "$W/node_modules" "$ct/node_modules" || return 2
    TMPDIR=$co bash "$R/.harness/handoff/2026-09-26-tools/ci-local.sh" "$ct" > "$co/out.txt" 2>&1
    printf 'rc0=%s not_rc0=%s\n' "$(grep -c 'rc=0' "$co/ci-local/summary.txt")" "$(grep -vc 'rc=0' "$co/ci-local/summary.txt")"
    grep -v 'rc=0' "$co/ci-local/summary.txt"; rm -rf "$ct" "$co" ;;
  COUNT) # m COUNT <측정기 출력 파일> <FUNC|NFR|CONSOLE|SEC7> — 그 묶음 줄의 OK · NG 수
    case "${3}" in
      FUNC) re='(rows-one-label|chip\[[^]]+\]|sum|drawer-rows-visible|filter|unjudged-reason)' ;;
      NFR) re='(row-glyph-contrast\[판정 불가\]|chip-glyph-contrast\[판정 불가\]|row-glyph-distinct|chip-glyph-distinct|text-contrast)' ;;
      CONSOLE) re='console-errors' ;;
      SEC7) re='sec7-expr' ;;
      *) echo "STOP 묶음 이름은 FUNC · NFR · CONSOLE · SEC7" >&2; return 2 ;;
    esac
    [ -s "${2}" ] || { echo "STOP 빈 파일 ${2}" >&2; return 2; }
    grep -E "^(OK|NG) [^ ]+ [^ ]+ ${re} " "${2}" | awk '{c[$1]++} END {printf "ok=%d ng=%d\n", c["OK"]+0, c["NG"]+0}' ;;
  NA)
    mine_files | awk '
      $0=="scripts/release.sh" {r++} $0==".claude-plugin/marketplace.json" || $0 ~ /\/\.claude-plugin\/plugin\.json$/ {v++}
      END {printf "release_sh=%d version_files=%d\n", r+0, v+0}' ;;
  *) echo "모르는 측정: ${1}" >&2; return 2 ;;
  esac
}
