#!/usr/bin/env bash
# flutter-catalog 계약 측정 묶음. 사용: bash measure.sh <case>
# 원본 핏팰은 읽기만 한다. 모든 쓰기는 $M 아래 복사본에서 한다.
# 판정 사례는 끝 줄에 `VERDICT PASS` 또는 `VERDICT FAIL <사유>` 를 찍는다.
set -uo pipefail

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(cd "$HERE/../../.." && pwd)
KIT="$REPO/flutter-toolkit/skills/flutter-catalog"
SRC=/Users/jackson/Hub/10_Dev/fit-pal
SCR=/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/85aff6fc-39c9-4668-852b-7307fe63e954/scratchpad
M=${MEASURE_DIR:-$SCR/fc-measure}
APP="$M/app"
GEN_OUT="$APP/lib/catalog_kit/generated/catalog_entries.g.dart"
CSV="$APP/build/widget_fundamentals.csv"
GOOD_CSV="$M/fund.good.csv"
PW_DIR=${PW_DIR:-$SCR/shot}   # playwright-core 가 깔린 폴더 (환경변수로 바꿀 수 있다)
SHOTS="$HERE/shots"

fvmd() { (cd "$APP" && fvm dart "$@"); }
fvmf() { (cd "$APP" && fvm flutter "$@"); }
mtime() { stat -f '%m' "$1" 2>/dev/null || echo none; }
use_yaml() { cp "$HERE/fixtures/$1" "$APP/catalog/widgets.yaml"; }
# flutter test -r json 출력에서 숨김 아닌 testDone 사건 수. 줄 안 키 순서에 기대지 않는다
ran_count() { python3 -c 'import json,sys
n=0
for l in open(sys.argv[1]):
    try: e=json.loads(l)
    except ValueError: continue
    n+=e.get("type")=="testDone" and not e.get("hidden")
print(n)' "$1"; }
verdict() { if [ "$1" = 0 ]; then echo "VERDICT PASS"; else echo "VERDICT FAIL $2"; fi; }
gen() { use_yaml "$1"; fvmd run tool/catalog_gen.dart; }

# 결과 표 질의: csvq <widget> <variant> <check> → "result|measured" 줄들
csvq() {
  python3 - "${4:-$CSV}" "$1" "$2" "$3" <<'PY'
import csv, sys
p, w, v, c = sys.argv[1:5]
with open(p, newline='') as f:
    for r in csv.DictReader(f):
        if r['widget'] == w and (v == '*' or r['variant'] == v) and r['check'] == c:
            print(f"{r['result']}|{r['measured']}|{r['case']}")
PY
}

case "${1:-}" in
  setup)
    rm -rf "$M"; mkdir -p "$M"
    rsync -a --exclude build --exclude .dart_tool --exclude ios --exclude android \
      --exclude widgetbook --exclude '*.log' "$SRC/app/" "$APP/"
    cp -R "$SRC/fit_pal_lint" "$M/"
    bash "$KIT/scripts/install.sh" --add-deps "$APP" || { echo "SETUP_FAIL install"; exit 2; }
    mkdir -p "$M/tmpl-hosts"
    cp "$APP/test/catalog_kit/catalog_kit_host.dart" "$M/tmpl-hosts/catalog_kit_host.dart"
    cp "$APP/lib/catalog_kit/catalog_kit_app_host.dart" "$M/tmpl-hosts/catalog_kit_app_host.dart"
    mkdir -p "$APP/lib/catalog_probe"
    cp "$HERE/fixtures/probes.dart" "$APP/lib/catalog_probe/probes.dart"
    cp "$HERE/fixtures/catalog_kit_host.dart" "$APP/test/catalog_kit/catalog_kit_host.dart"
    cp "$HERE/fixtures/catalog_kit_app_host.dart" "$APP/lib/catalog_kit/catalog_kit_app_host.dart"
    use_yaml widgets.ok.yaml
    fvmf pub get >/dev/null 2>&1 || { echo "SETUP_FAIL pub get"; exit 2; }
    echo "SETUP_OK $APP"
    ;;

  gen-ok)   # 스크립트-01
    gen widgets.ok.yaml; rc=$?
    python3 - "$GEN_OUT" <<'PY'
import re, sys
s = open(sys.argv[1]).read()
blocks = re.split(r"\n  PlaygroundEntry\(", s)[1:]
b = next((b for b in blocks if "widget: 'IFButton'" in b and "variant: 'new'" in b), '')
for p in ['onTap', 'child', 'height', 'width', 'radius', 'refractionStrength', 'held']:
    print(('has ' if f"key: '{p}'" in b else 'MISSING ') + p)
PY
    miss=$(python3 - "$GEN_OUT" <<'PY'
import re, sys
s = open(sys.argv[1]).read()
blocks = re.split(r"\n  PlaygroundEntry\(", s)[1:]
b = next((b for b in blocks if "widget: 'IFButton'" in b and "variant: 'new'" in b), '')
print(sum(f"key: '{p}'" not in b for p in ['onTap','child','height','width','radius','refractionStrength','held']))
PY
)
    echo "exit=$rc"; [ "$rc" = 0 ] && [ "$miss" = 0 ]; verdict $? "exit=$rc missing=$miss"
    ;;

  gen-unsupported)   # 스크립트-02
    gen widgets.ok.yaml >/dev/null 2>&1; before=$(mtime "$GEN_OUT"); sleep 1
    out=$(gen widgets.unsupported.yaml 2>&1); rc=$?; after=$(mtime "$GEN_OUT")
    echo "$out" | tail -5
    a=$(echo "$out" | grep -c IFChipContainer); b=$(echo "$out" | grep -c padding)
    echo "exit=$rc before=$before after=$after IFChipContainer=$a padding=$b"
    [ "$before" != none ] && [ "$before" = "$after" ] && [ "$rc" = 1 ] && [ "$a" -ge 1 ] && [ "$b" -ge 1 ]
    verdict $? "조건 불충족"
    ;;

  gen-missing)   # 스크립트-03 (앞 절반)
    out=$(gen widgets.missing.yaml 2>&1); rc=$?; echo "$out" | tail -10; ok=0
    for n in GlassPressBox IFSpotButton IFStatusMark IconTapTarget Pressable SplitPill; do
      c=$(echo "$out" | grep -cw "$n"); echo "$n=$c"; [ "$c" -ge 1 ] || ok=1
    done
    pd=$(echo "$out" | grep -cw PressableData); echo "PressableData=$pd"; [ "$pd" = 0 ] || ok=1
    echo "exit=$rc"; [ "$rc" = 1 ] && [ "$ok" = 0 ]; verdict $? "exit=$rc 이름 누락 또는 InheritedWidget 포함"
    ;;

  gen-unknown)   # 스크립트-03 (뒤 절반)
    out=$(gen widgets.unknown.yaml 2>&1); rc=$?; c=$(echo "$out" | grep -c NoSuchWidget)
    echo "exit=$rc NoSuchWidget=$c"; [ "$rc" = 1 ] && [ "$c" -ge 1 ]; verdict $? "exit=$rc"
    ;;

  gen-unreadable)   # 스크립트-03 보강 (개정 A-03) — 공용 폴더의 파일을 못 읽거나 문법이 깨지면 경로를 알리고 1
    f="$APP/lib/shared/presentation/widgets/buttons/split_pill.dart"; cp "$f" "$M/split_pill.bak"
    chmod 000 "$f"; o1=$(gen widgets.missing.yaml 2>&1); r1=$?; chmod 644 "$f"
    echo 'class {{{' >> "$f"; o2=$(gen widgets.missing.yaml 2>&1); r2=$?; cp "$M/split_pill.bak" "$f"
    rs=$(diff "$M/split_pill.bak" "$f" | grep -cE '^[<>]')
    p1=$(echo "$o1" | grep -c '읽지 못한 파일: .*split_pill.dart'); p2=$(echo "$o2" | grep -c '문법이 깨진 파일: .*split_pill.dart')
    echo "unreadable_exit=$r1 unreadable_path=$p1 broken_exit=$r2 broken_path=$p2 restored_diff=$rs"
    [ "$r1" = 1 ] && [ "$p1" = 1 ] && [ "$r2" = 1 ] && [ "$p2" = 1 ] && [ "$rs" = 0 ]; verdict $? "조건 불충족"
    ;;

  analyze)   # 스크립트-08
    gen widgets.ok.yaml >/dev/null 2>&1
    T="lib/catalog_kit lib/main_catalog_kit.dart lib/catalog_probe test/catalog_kit tool"
    echo "대상: $T"
    out=$(cd "$APP" && fvm flutter analyze --no-fatal-infos $T 2>&1); rc=$?
    echo "$out" | tail -20
    ni=$(echo "$out" | grep -c 'No issues found')
    echo "exit=$rc no_issues=$ni"; [ "$rc" = 0 ] && [ "$ni" = 1 ]; verdict $? "exit=$rc"
    ;;
  analyze-pos)   # 스크립트-08 양성 대조
    echo "int x = 'a';" > "$APP/lib/catalog_kit/zz_neg.dart"
    out=$(cd "$APP" && fvm flutter analyze --no-fatal-infos lib/catalog_kit 2>&1); rc=$?
    rm -f "$APP/lib/catalog_kit/zz_neg.dart"
    n=$(echo "$out" | grep -cE '^ *error'); echo "exit=$rc errors=$n"
    [ "$rc" != 0 ] && [ "$n" -ge 1 ]; verdict $? "오류를 못 잡음"
    ;;

  fund-run)   # 판정 아님 — 결과 표를 만든다. IFButton 등 일부 시험은 실패하는 것이 정상이다
    gen widgets.ok.yaml >/dev/null 2>&1; rm -f "$CSV"
    fvmf test test/catalog_kit/widget_fundamentals_test.dart -r json > "$M/fund.json" 2>&1
    echo "exit=$? (0 이 아니어도 정상)"
    python3 - "$M/fund.json" <<'PY'
import json, sys
st = {}
for line in open(sys.argv[1]):
    try: e = json.loads(line)
    except ValueError: continue
    if e.get('type') == 'testDone' and not e.get('hidden'):
        st[e['result']] = st.get(e['result'], 0) + 1
print('testDone', st)
PY
    cp "$CSV" "$GOOD_CSV" 2>/dev/null; wc -l < "$CSV"
    ;;

  sizing)   # 스크립트-04 (fund-run 뒤)
    python3 - "$CSV" <<'PY'
import csv, re, sys
rows = list(csv.DictReader(open(sys.argv[1], newline='')))
def q(w, v, c): return [r for r in rows if r['widget']==w and r['variant']==v and r['check']==c]
def num(s, k):
    m = re.search(k + r'=([0-9.]+)', s); return float(m.group(1)) if m else None
def small(s):
    v = [x for x in (num(s, 'left'), num(s, 'right')) if x is not None]
    return min(v) if len(v) == 2 else None
ok = True
r = q('IFButton','new','크기 동작'); print('IFButton 크기 동작', [(x['result'],x['measured']) for x in r])
w = num(r[0]['measured'],'w') if len(r)==1 else None
ok &= len(r)==1 and r[0]['result']=='FAIL' and w is not None and w >= 389
r = q('IFButton','new','여백'); print('IFButton 여백', [(x['result'],x['measured']) for x in r])
sm = small(r[0]['measured']) if len(r)==1 else None
ok &= len(r)==1 and r[0]['result']=='FAIL' and sm is not None and sm < 16
r = q('IFToggle','new','크기 동작'); print('IFToggle 크기 동작', [(x['result'],x['measured']) for x in r])
ok &= len(r)==1 and r[0]['result']=='PASS'
r = q('IFToggle','new','상태 불변'); print('IFToggle 상태 불변', [(x['result'],x['measured']) for x in r])
ok &= len(r)==1 and r[0]['result']=='PASS' and '52.0x28.0' in r[0]['measured']
r = q('StateProbe','new','상태 불변'); print('StateProbe 상태 불변', [(x['result'],x['measured']) for x in r])
ok &= len(r)==1 and r[0]['result']=='FAIL'
print('VERDICT PASS' if ok else 'VERDICT FAIL 조건 불충족')
PY
    ;;

  overflow)   # 스크립트-05 (fund-run 뒤)
    python3 - "$GEN_OUT" "$CSV" <<'PY'
import csv, re, sys
gen = open(sys.argv[1]).read()
rows = list(csv.DictReader(open(sys.argv[2], newline='')))
blocks = re.split(r"\n  PlaygroundEntry\(", gen)[1:]
ok = True; seen = set()
for b in blocks:
    w = re.search(r"widget: '([^']+)'", b).group(1); v = re.search(r"variant: '([^']+)'", b).group(1)
    seen.add((w, v))
    want = 3 * 4 * 2 * (3 if 'TextControl(' in b else 1)
    got = sum(1 for r in rows if r['widget']==w and r['variant']==v and r['check']=='넘침')
    print(('OK' if got==want else 'MISMATCH'), f"{w}.{v} want={want} got={got}"); ok &= got==want
need = [('IFButton','new'),('IFMiniButton','primary'),('IFToggle','new'),('AppErrorWidget','new'),('OverflowProbe','new')]
for n in need:
    if n not in seen: print('ABSENT', n); ok = False
if not any(w=='IFBadge' for w,_ in seen): print('ABSENT IFBadge'); ok = False
cnt = lambda w, v: sum(1 for r in rows if r['widget']==w and r['variant']==v and r['check']=='넘침')
kt, kb = cnt('IFToggle','new'), cnt('IFButton','new')
print(f"known IFToggle.new={kt}(24) IFButton.new={kb}(72)"); ok &= kt == 24 and kb == 72
of = [r for r in rows if r['widget']=='OverflowProbe' and r['check']=='넘침' and r['result']=='FAIL']
tg = [r for r in rows if r['widget']=='IFToggle' and r['check']=='넘침' and r['result']!='PASS']
print(f"entries={len(blocks)} OverflowProbe_FAIL={len(of)} IFToggle_notPASS={len(tg)}")
ok &= len(blocks) >= 15 and len(of) >= 1 and len(tg) == 0
print('VERDICT PASS' if ok else 'VERDICT FAIL 조건 불충족')
PY
    ;;

  icon-touch)   # 스크립트-09 (fund-run 뒤)
    python3 - "$CSV" <<'PY'
import csv, sys
rows = list(csv.DictReader(open(sys.argv[1], newline='')))
def res(w, c): return [r['result'] for r in rows if r['widget']==w and r['check']==c]
want = {('IconProbeBad','아이콘 정렬'):'FAIL', ('IconProbeGood','아이콘 정렬'):'PASS',
        ('TapSmallProbe','터치 크기'):'FAIL', ('TapBigProbe','터치 크기'):'PASS'}
ok = True
for (w, c), exp in want.items():
    got = res(w, c); print(w, c, got); ok &= got == [exp]
print('VERDICT PASS' if ok else 'VERDICT FAIL 조건 불충족')
PY
    ;;

  font)   # 스크립트-06
    gen widgets.ok.yaml >/dev/null 2>&1
    fvmf test test/catalog_kit/widget_fundamentals_test.dart --plain-name 'catalog_kit | 글꼴' -r json > "$M/font.base.log" 2>&1; base=$?
    ran=$(ran_count "$M/font.base.log")
    cp "$APP/pubspec.yaml" "$M/pubspec.bak"
    python3 - "$APP/pubspec.yaml" <<'PY'
import re, sys
p = sys.argv[1]; s = open(p).read()
s2 = re.sub(r"\n    - family: KIMM\n(?:      .*\n|        .*\n|          .*\n)*", "\n", s, count=1)
open(p, 'w').write(s2)
PY
    changed=$(diff "$M/pubspec.bak" "$APP/pubspec.yaml" | grep -cE '^[<>]')
    fvmf test test/catalog_kit/widget_fundamentals_test.dart --plain-name 'catalog_kit | 글꼴' > "$M/font.neg.log" 2>&1; neg=$?
    cp "$M/pubspec.bak" "$APP/pubspec.yaml"; restored=$(diff "$M/pubspec.bak" "$APP/pubspec.yaml" | grep -cE '^[<>]')
    hint=$(grep -c '글꼴' "$M/font.neg.log")
    echo "base_exit=$base base_tests=$ran changed_lines=$changed neg_exit=$neg hint=$hint restored_diff=$restored"
    [ "$base" = 0 ] && [ "$ran" -ge 1 ] && [ "$changed" -ge 1 ] && [ "$neg" != 0 ] && [ "$hint" -ge 1 ] && [ "$restored" = 0 ]
    verdict $? "조건 불충족"
    ;;

  wrapper)   # 오류-01 (fund-run 뒤 — 정상 감싸개 결과 $GOOD_CSV 를 쓴다)
    cp "$APP/test/catalog_kit/catalog_kit_host.dart" "$M/host.bak"
    cp "$HERE/fixtures/catalog_kit_host.bare.dart" "$APP/test/catalog_kit/catalog_kit_host.dart"
    rm -f "$CSV"
    fvmf test test/catalog_kit/widget_fundamentals_test.dart --name 'AppErrorWidget|IFToggle' > "$M/wrapper.log" 2>&1
    cp "$CSV" "$M/fund.bare.csv"
    cp "$M/host.bak" "$APP/test/catalog_kit/catalog_kit_host.dart"
    restored=$(diff "$M/host.bak" "$APP/test/catalog_kit/catalog_kit_host.dart" | grep -cE '^[<>]')
    python3 - "$GOOD_CSV" "$M/fund.bare.csv" "$restored" <<'PY'
import csv, sys
good = list(csv.DictReader(open(sys.argv[1], newline='')))
bare = list(csv.DictReader(open(sys.argv[2], newline='')))
ga = [r for r in good if r['widget']=='AppErrorWidget']
ba = [r for r in bare if r['widget']=='AppErrorWidget']
g_hint = sum('감싸개' in r['measured'] for r in ga)
b_fail = sum(r['result']=='FAIL' and '감싸개' in r['measured'] for r in ba)
key = lambda r: (r['variant'], r['check'], r['case'])
gt = {key(r): r['result'] for r in good if r['widget']=='IFToggle'}
bt = {key(r): r['result'] for r in bare if r['widget']=='IFToggle'}
same = bool(gt) and gt == bt
print(f"good_AppError_rows={len(ga)} good_hint={g_hint} bare_AppError_rows={len(ba)} bare_fail_hint={b_fail} IFToggle_same={same} restored_diff={sys.argv[3]}")
ok = len(ga) > 0 and g_hint == 0 and b_fail >= 1 and same and sys.argv[3] == '0'
print('VERDICT PASS' if ok else 'VERDICT FAIL 조건 불충족')
PY
    ;;

  lint)   # 스크립트-07
    use_yaml widgets.lint.yaml
    out=$(fvmd run tool/catalog_lint.dart 2>&1); rc=$?
    fvmd run tool/catalog_lint.dart --report >/dev/null 2>&1; rrc=$?
    use_yaml widgets.ok.yaml
    a=$(echo "$out" | grep -cE 'if_chip\.dart:332:.*14\.5'); b=$(echo "$out" | grep -cE 'if_chip\.dart:333:.*5\.5')
    c=$(echo "$out" | grep -cE 'if_button\.dart:299:.*fontFamily'); d=$(echo "$out" | grep -c 'if_toggle\.dart')
    echo "exit=$rc report_exit=$rrc chip332=$a chip333=$b button299=$c toggle=$d"
    [ "$rc" = 1 ] && [ "$rrc" = 0 ] && [ "$a" -ge 1 ] && [ "$b" -ge 1 ] && [ "$c" -ge 1 ] && [ "$d" = 0 ]
    verdict $? "조건 불충족"
    ;;

  install)   # 구조-04 (setup 뒤)
    f="$APP/lib/catalog_kit/measured_box.dart"; echo "// 표식-$$" >> "$f"
    bash "$KIT/scripts/install.sh" "$APP" >/dev/null 2>&1; rc=$?
    kept=$(grep -c "표식-$$" "$f"); sed -i '' "/표식-$$/d" "$f"
    T="$M/partial"; rm -rf "$T"; mkdir -p "$T/lib/catalog_kit"; echo "name: t" > "$T/pubspec.yaml"; echo "// 있음" > "$T/lib/catalog_kit/measured_box.dart"
    bash "$KIT/scripts/install.sh" "$T" >/dev/null 2>&1; prc=$?
    pf=$(find "$T" -type f | wc -l | tr -d ' ')
    dd=$(awk '/^dev_dependencies:/{f=1;next} /^[a-z]/{f=0} f' "$APP/pubspec.yaml" | grep -cE '^  (analyzer|yaml):')
    echo "second_exit=$rc marker_kept=$kept partial_exit=$prc partial_files=$pf dev_deps_added=$dd"
    [ "$rc" = 1 ] && [ "$kept" = 1 ] && [ "$prc" = 1 ] && [ "$pf" = 2 ] && [ "$dd" = 2 ]; verdict $? "조건 불충족"
    ;;

  tmpl-hosts)   # 구조-06 (setup 뒤) — 틀 감싸개 두 개를 고치지 않은 채 넣고 분석 · 글꼴 시험 · 놀이터 빌드
    gen widgets.ok.yaml >/dev/null 2>&1
    cp "$APP/test/catalog_kit/catalog_kit_host.dart" "$M/fx-host.bak"; cp "$APP/lib/catalog_kit/catalog_kit_app_host.dart" "$M/fx-app.bak"
    cp "$M/tmpl-hosts/catalog_kit_host.dart" "$APP/test/catalog_kit/catalog_kit_host.dart"
    cp "$M/tmpl-hosts/catalog_kit_app_host.dart" "$APP/lib/catalog_kit/catalog_kit_app_host.dart"
    pk=$(grep -c 'package:app/' "$APP/test/catalog_kit/catalog_kit_host.dart" "$APP/lib/catalog_kit/catalog_kit_app_host.dart" | awk -F: '{s+=$NF} END{print s+0}')
    a=$(cd "$APP" && fvm flutter analyze --no-fatal-infos test/catalog_kit lib/catalog_kit lib/main_catalog_kit.dart 2>&1); arc=$?
    fvmf test test/catalog_kit/widget_fundamentals_test.dart --plain-name 'catalog_kit | 글꼴' -r json > "$M/tmpl-font.log" 2>&1; frc=$?
    ran=$(ran_count "$M/tmpl-font.log")
    fvmf build web -t lib/main_catalog_kit.dart --release --no-wasm-dry-run --pwa-strategy=none > "$M/tmpl-web.log" 2>&1; brc=$?
    cp "$M/fx-host.bak" "$APP/test/catalog_kit/catalog_kit_host.dart"; cp "$M/fx-app.bak" "$APP/lib/catalog_kit/catalog_kit_app_host.dart"
    rs=$(diff "$M/fx-host.bak" "$APP/test/catalog_kit/catalog_kit_host.dart" | grep -cE '^[<>]')
    echo "$a" | tail -3
    echo "app_imports=$pk analyze_exit=$arc font_exit=$frc font_tests=$ran build_exit=$brc restored_diff=$rs"
    [ "$pk" = 0 ] && [ "$arc" = 0 ] && [ "$frc" = 0 ] && [ "$ran" -ge 1 ] && [ "$brc" = 0 ] && [ "$rs" = 0 ]; verdict $? "조건 불충족"
    ;;

  web)   # 구조-05 · 진단-04
    gen widgets.ok.yaml >/dev/null 2>&1
    fvmf build web -t lib/main_catalog_kit.dart --release --no-wasm-dry-run --pwa-strategy=none > "$M/web.build.log" 2>&1 || { tail -5 "$M/web.build.log"; echo "VERDICT FAIL 빌드 실패"; exit 0; }
    mkdir -p "$SHOTS"; rm -f "$SHOTS"/*.png
    PORT=$(python3 -c 'import socket;s=socket.socket();s.bind(("127.0.0.1",0));print(s.getsockname()[1])')
    node "$HERE/serve.js" "$APP/build/web" "$PORT" > "$M/serve.log" 2>&1 & SP=$!
    sleep 1
    [ -d "$PW_DIR/node_modules/playwright-core" ] || { echo "VERDICT FAIL playwright-core 없음 ($PW_DIR)"; kill $SP; exit 0; }
    NODE_PATH="$PW_DIR/node_modules" node "$HERE/web_check.js" "http://127.0.0.1:$PORT/" "$SHOTS" | tee "$HERE/chrome.log"
    kill $SP 2>/dev/null
    ;;

  *)
    echo "cases: setup tmpl-hosts gen-ok gen-unsupported gen-missing gen-unknown gen-unreadable analyze analyze-pos fund-run sizing overflow icon-touch font wrapper lint install web"; exit 2;;
esac
