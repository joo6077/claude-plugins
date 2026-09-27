#!/bin/bash
# m.sh <작업 폴더> <조건 ID> — 계약 after-0926-kits-api-onboarding-howto 의 측정. 읽기만 한다(임시 사본은 mktemp 아래).
# 종료 코드: 0 측정함(값은 출력으로 판정) · 2 측정 못 함
W="${1:?작업 폴더}"; ID="${2:?조건 ID}"
HERE=$(cd "$(dirname "${0}")" && pwd)
cd "$W" || exit 2
BASE=6378948
sec() {  # sec <파일> <시작 정규식> <끝 정규식> — 시작 줄부터 끝 줄 앞까지
  awk -v s="${2}" -v e="${3}" '$(0) ~ s {p=1; print; next} p && $(0) ~ e {exit} p' "${1}"
}
gate_of() {  # gate_of <SKILL.md> — guide_gate 함수만 뽑는다
  awk '/^guide_gate\(\) \{/{p=1} p{print} p&&/^\}$/{exit}' "${1}"
}
fm_get() {  # fm_get <파일> <키> — 첫 frontmatter 블록에서만
  awk -v k="^${2}:[[:space:]]*" 'NR==1 && /^---[[:space:]]*$/ {fm=1; next} fm && /^---[[:space:]]*$/ {exit} fm && $(0) ~ k {sub(k, "", $(0)); print; exit}' "${1}" \
    | sed -e 's/[[:space:]]*$//' -e "s/^['\"]//" -e "s/['\"]\$//"
}
sha256_16() { shasum -a 256 | cut -c1-16; }
T=$(mktemp -d "${TMPDIR:-/tmp}/k4m.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT

case $ID in
SK-01)
  S8=$(sec api-kit/skills/api-ui/SKILL.md '^## 8\.' '^# References')
  L=$(printf '%s\n' "$S8" | grep -F -- '- Step 7 브라우저 확인')
  echo "step7_lines=$(printf '%s\n' "$L" | grep -c .) chips=$(printf '%s\n' "$L" | grep -cF '`chips`') rows=$(printf '%s\n' "$L" | grep -cF '`rows`')" ;;
SK-02)
  S6=$(sec api-kit/skills/api-verify/SKILL.md '^## 6\.' '^## 7\.')
  S9=$(sec api-kit/skills/api-verify/SKILL.md '^## 9\.' '^## 10\.')
  echo "s6_prefixed_example=$(printf '%s\n' "$S6" | grep -cE '[a-z][a-z0-9_]*\.[a-z][a-z0-9_.]*: \$\.[A-Za-z]')" \
       "s6_id_word=$(printf '%s\n' "$S6" | grep -cF '엔드포인트 id')" \
       "s9_item7_id=$(printf '%s\n' "$S9" | grep -E '^7\. ' | grep -cF '엔드포인트 id')" ;;
SK-03)
  S2=$(sec api-kit/skills/api-ui/SKILL.md '^## 2\.' '^## 3\.')
  echo "s2_strip_rule=$(printf '%s\n' "$S2" | grep -F '엔드포인트 id' | grep -cF '앞머리')" ;;
SK-04)
  V=api-kit/skills/api-ui/references/viewer-spec.md
  echo "hold=$(grep -c '보류' "$V") flaky=$(grep -c 'flaky' "$V")" \
       "hold_fail=$(grep '보류' "$V" | grep -cF "'fail'") flaky_fail=$(grep 'flaky' "$V" | grep -cF "'fail'")" \
       "label=$(grep -E '보류|flaky' "$V" | grep -cF 'aria-label')" \
       "state_enum=$(grep -cF "'pass' | 'fail' | 'pending' | 'unjudged'" "$V") new_state=$(grep -cE "state: *'(hold|flaky|보류)'" "$V")" ;;
SK-05)
  for f in api-kit/skills/api-contract/SKILL.md api-kit/skills/api-verify/SKILL.md api-kit/skills/api-probe/SKILL.md; do
    echo "$f strict_note=$(grep -F 'RFC 7493' "$f" | grep -F 'SHOULD NOT' | grep -cF '엄격')"
  done ;;
SK-06)
  bash "$HERE/ka5.sh" "$W" ;;
SK-07)
  S7=$(sec api-kit/skills/api-ui/SKILL.md '^## 7\.' '^## 8\.')
  S6=$(sec api-kit/skills/api-ui/SKILL.md '^## 6\.' '^## 7\.')
  echo "s7_cmd=$(printf '%s\n' "$S7" | grep -F "grep -c 'http-equiv=\"Content-Security-Policy\"' \"\$UI\"" | grep -cF '기대 1')" \
       "s7_row=$(printf '%s\n' "$S7" | grep '^|' | grep -c 'CSP')" \
       "s6_csp=$(printf '%s\n' "$S6" | grep -c 'CSP')"
  echo "example_csp=$(grep -c 'http-equiv="Content-Security-Policy"' api-kit/evals/fixtures/unjudged/.api/ui.html)" \
       "mockup_v8_csp=$(grep -c 'http-equiv="Content-Security-Policy"' /Users/jackson/Hub/10_Dev/claude-plugins/.mockups/api-ui-v8.html)" ;;
SK-08|SK-09|SK-10|ER-03)
  python3 "$HERE/ob.py" onboarding-kit/skills/setup-guide/evals/evals.json
  gate_of onboarding-kit/skills/setup-guide/SKILL.md > "$T/gate.sh"
  EX=docs/onboarding-kit/examples/fcm-ios-setup-guide.md
  zsh -c ". '$T/gate.sh'; guide_gate '$EX' flutter" > "$T/z" 2>&1
  bash -c ". '$T/gate.sh'; guide_gate '$EX' flutter" > "$T/b" 2>&1
  cmp -s "$T/z" "$T/b" && same=1 || same=0
  echo "example_same_shell=$same example_g5_pass=$(grep -c '^G5_BLOCKING PASS' "$T/b") example_gate_pass=$(grep -cx GATE_PASS "$T/b")"
  SK=onboarding-kit/skills/setup-guide/SKILL.md
  echo "five_lines=$(grep -c '5 줄' "$SK") six_lines=$(grep -c '6 줄' "$SK") run_line_g5=$(grep -F 'G1(출처 원장 완전성)' "$SK" | grep -c 'G5')"
  sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh > "$T/r" 2>&1; rc=$?
  echo "runner_rc=$rc $(grep '^EVALS declared' "$T/r")" ;;
NEG-KO)
  # 음성 대조: SKILL.md 사본의 G1 · G5 판정을 늘 PASS 로 바꾸면 러너가 떨어져야 한다
  cp -R onboarding-kit "$T/ob"
  SK="$T/ob/skills/setup-guide/SKILL.md"
  python3 - "$SK" <<'PY'
import re, sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
s2 = re.sub(r'echo "G5_BLOCKING FAIL', 'echo "G5_BLOCKING PASS', s)
open(p, "w", encoding="utf-8").write(s2)
print("g5_mutated=%d" % (s != s2))
PY
  sh "$T/ob/skills/setup-guide/evals/run-gate-evals.sh" > "$T/r1" 2>&1; echo "g5_neg_rc=$? $(grep '^EVALS declared' "$T/r1")"
  cp onboarding-kit/skills/setup-guide/SKILL.md "$SK"
  sed -i '' 's/if \[ "\$steps" -eq 0 \] || \[ "\$steps" -ne "\$ledger" \]; then/if false; then/' "$SK"
  echo "g1_mutated=$(grep -c 'if false; then' "$SK")"
  sh "$T/ob/skills/setup-guide/evals/run-gate-evals.sh" > "$T/r2" 2>&1; echo "g1_neg_rc=$? $(grep '^EVALS declared' "$T/r2")" ;;
SK-11)
  SK=onboarding-kit/skills/setup-guide/SKILL.md
  echo "cocoapods_line=$(grep -F 'Swift Package Manager' "$SK" | grep -F 'CocoaPods' | grep -F 'Firebase 12' | grep -cF 'https://firebase.google.com/docs/ios/setup')" \
       "flutter_keep=$(grep -F 'CocoaPods' "$SK" | grep -c 'Flutter')" \
       "evals_spm_assert=$(grep -cF "guide_does_not_include('Swift Package Manager 검색창에 firebase-ios-sdk')" onboarding-kit/skills/setup-guide/evals/evals.json)" ;;
SK-12|SC-01)
  python3 scripts/check-reviewer-protocol-copies.py > "$T/c" 2>&1; rc=$?
  R=howto-kit/agents/howto-reviewer.md
  echo "copies_rc=$rc ok_lines=$(grep -c '^OK ' "$T/c") howto_ok=$(grep -cx 'OK howto-kit/agents/howto-reviewer.md' "$T/c") $(tail -1 "$T/c")"
  echo "source_line=$(grep '^사본 출처:' "$R" | grep -cF 'qa-evaluation-guide.md') grade_line=$(grep -F '[미확인]' "$R" | grep -cF '출처 등급')" \
       "tools=[$(fm_get "$R" tools)] docstring_eight=$(sed -n 2p scripts/check-reviewer-protocol-copies.py | grep -c '여덟')" ;;
NEG-KH1)
  # 음성 대조: 끝 판 사본에서 howto-reviewer 의 조항 첫 줄을 지우면 MISMATCH · 종료 코드 1
  git archive "${3:-HEAD}" | tar -x -C "$T" || exit 2
  sed -i '' '/^1\. \*\*마커는/d' "$T/howto-kit/agents/howto-reviewer.md"
  (cd "$T" && python3 scripts/check-reviewer-protocol-copies.py > "$T/c" 2>&1; echo "neg_rc=$? $(grep -c '^MISMATCH howto-kit/agents/howto-reviewer.md' "$T/c")") ;;
SK-13)
  S4=$(sec howto-kit/skills/howto-audit/SKILL.md '^### Phase 4' '^## ')
  echo "unverified_line=$(printf '%s\n' "$S4" | grep -F '[미검증:ENV]' | grep -cF '[미검증:INVALID]')" \
       "not_pass=$(printf '%s\n' "$S4" | grep -F '미검증' | grep -c 'PASS 로 세지 않는다')" ;;
SK-14)
  S9=$(sec howto-kit/references/provenance-notes.md '^## 9\.' '^## 이 원장을 쓰는 법')
  L=$(printf '%s\n' "$S9" | grep -F 'DITA 2.0')
  echo "dita_lines=$(printf '%s\n' "$L" | grep -c .)" \
       "url=$(printf '%s\n' "$S9" | grep -cF 'https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=dita')" \
       "d13=$(printf '%s\n' "$S9" | grep -c '2015-12-17') checked=$(printf '%s\n' "$S9" | grep -c '2026-09-26')" ;;
SK-15)
  # 러너 자기 음성 대조: 두 판정을 무력화한 킷 사본에서 러너가 떨어지는지 · 원본 사본은 통과하는지
  R=howto-kit/evals/run-evals.sh
  echo "lit_assert=$(grep -cF 'grep -qF -- "$assertion"' "$R") lit_shell=$(grep -cF '[ "$out_zsh" = "$out_bash" ]' "$R")"
  for v in orig assert shell; do
    rm -rf "$T/hk"; mkdir -p "$T/hk"; cp -R howto-kit "$T/hk/"
    case $v in
      assert) sed -i '' 's/grep -qF -- "\$assertion"/true/' "$T/hk/howto-kit/evals/run-evals.sh" ;;
      shell)  sed -i '' 's/\[ "\$out_zsh" = "\$out_bash" \]/true/g' "$T/hk/howto-kit/evals/run-evals.sh" ;;
    esac
    left=$(cmp -s howto-kit/evals/run-evals.sh "$T/hk/howto-kit/evals/run-evals.sh" && echo 0 || echo 1)
    sh "$T/hk/howto-kit/evals/run-evals.sh" > "$T/o" 2>&1; rc=$?
    echo "$v mutated=$left rc=$rc last=$(tail -1 "$T/o") selfcheck_lines=$(grep -ciE '^(PASS|FAIL) +selfcheck' "$T/o")"
  done ;;
SK-16)
  s=$(python3 -c 'import time; print(time.time())')
  sh howto-kit/evals/run-evals.sh > "$T/o" 2>&1; rc=$?
  e=$(python3 -c 'import time; print(time.time())')
  echo "rc=$rc $(grep '^EVALS total' "$T/o") seconds=$(python3 -c "print(round($e - $s, 1))")" ;;
SK-17)
  echo "c5_three=$(grep '^| C5 |' docs/howto/design-brief.md | grep -cF 'zsh·bash·sh')" ;;
ER-01)
  # 예시 입력 리포트의 판정 불가 줄에서 「<엔드포인트 id>: 」 를 떼면 예시 ui.html 의 그 항목 unjudged 에 글자 그대로 있다
  python3 - <<'PY'
import re
rep = open("api-kit/evals/fixtures/unjudged/.api/reports/2026-09-02T1422-dev/report.md", encoding="utf-8").read().split("\n")
ui = open("api-kit/evals/fixtures/unjudged/.api/ui.html", encoding="utf-8").read()
lines = [l for l in rep if l.startswith("- ") and l.endswith("→ 판정 불가")]
ok = 0
for l in lines:
    m = re.match(r"- ([a-z][a-z0-9_.]*): (.+)$", l)
    if not m:
        continue
    ep, rest = m.groups()
    # 같은 이름이 SCHEMA 에도 있다 — 이름이 나오는 자리마다 다음 항목 머리 전까지만 본다
    for seg in ui.split("'%s':{" % ep)[1:]:
        seg = re.split(r"\n  '[a-z]", seg, maxsplit=1)[0]
        if any(("'%s'" % rest) in u.split("]", 1)[0] for u in seg.split("unjudged:[")[1:]):
            ok += 1
            break
print("report_unjudged=%d matched=%d" % (len(lines), ok))
PY
  ;;
ER-02)
  echo "contract_gate=$(grep -cE '^IEEE 754 binary64 표현 불가 숫자 +→ 실패$' api-kit/skills/api-contract/SKILL.md)" \
       "verify_class=$(grep -F 'binary64' api-kit/skills/api-verify/SKILL.md | grep -cF '**비교 불가**로 분류한다')" \
       "probe_gate=$(grep -E '^2\. I-JSON 검문' api-kit/skills/api-probe/SKILL.md | grep -cF 'binary64 표현 불가 숫자')" ;;
AR-01)
  U=$(git rev-parse --verify -q chore/ak2-k4) || { echo "UNRESOLVED chore/ak2-k4"; exit 2; }
  git diff --name-status "$BASE" "$U" -- . ':(exclude).harness' > "$T/d"
  python3 - "$T/d" <<'PY'
import sys
req = """api-kit/skills/api-ui/SKILL.md
api-kit/skills/api-ui/references/viewer-spec.md
api-kit/skills/api-verify/SKILL.md
api-kit/skills/api-contract/SKILL.md
api-kit/skills/api-probe/SKILL.md
onboarding-kit/skills/setup-guide/SKILL.md
onboarding-kit/skills/setup-guide/evals/evals.json
howto-kit/agents/howto-reviewer.md
howto-kit/skills/howto-audit/SKILL.md
howto-kit/references/provenance-notes.md
howto-kit/evals/run-evals.sh
docs/howto/design-brief.md
scripts/check-reviewer-protocol-copies.py""".split("\n")
opt = {"onboarding-kit/skills/setup-guide/references/format-checklist.md", "howto-kit/evals/evals.json"}
new_dirs = ("onboarding-kit/skills/setup-guide/evals/fixtures/", "howto-kit/evals/fixtures/")
out, seen, new_fx = [], set(), 0
for row in open(sys.argv[1], encoding="utf-8"):
    st, path = row.rstrip("\n").split("\t")[0], row.rstrip("\n").split("\t")[-1]
    seen.add(path)
    if st == "M" and (path in req or path in opt):
        continue
    if st == "A" and path.startswith(new_dirs):
        new_fx += path.startswith(new_dirs[0])
        continue
    out.append(st + " " + path)
missing = [p for p in req if p not in seen]
print("scope_out=%d required_missing=%d new_onboarding_fixtures=%d" % (len(out), len(missing), new_fx))
for o in out: print("  OUT " + o)
for m in missing: print("  MISSING " + m)
PY
  ;;
AR-02)
  U=$(git rev-parse --verify -q chore/ak2-k4) || { echo "UNRESOLVED chore/ak2-k4"; exit 2; }
  mixed=0; n=0
  for c in $(git rev-list --reverse "$BASE..$U"); do
    groups=$(git show --name-only --format= "$c" | grep . | grep -v '^\.harness/' \
      | sed -E 's#^docs/howto/.*#howto-kit#; s#^([a-z]+-kit)/.*#\1#; s#^scripts/.*#scripts#' | sort -u | tr '\n' ' ')
    [ -n "$groups" ] || continue
    n=$((n + 1)); k=$(printf '%s' "$groups" | wc -w | tr -d ' ')
    [ "$k" -le 1 ] || mixed=$((mixed + 1))
    echo "  $(git log -1 --format=%h "$c") [$groups]"
  done
  CT=.harness/sprint-contract-after-0926-kits-api-onboarding-howto.md
  seal=$(git log --diff-filter=A --format=%H "$BASE..$U" -- "$CT" | tail -1)
  [ -n "$seal" ] || { echo "impl_commits=$n mixed=$mixed seal_commit=none"; exit 0; }
  later=$(git rev-list --reverse "$seal..$U" | while read -r c; do git show --name-only --format= "$c" | grep -v '^\.harness/' | grep -q . && echo "$c"; done | head -1)
  echo "impl_commits=$n mixed=$mixed seal_commit_files=$(git show --name-only --format= "$seal" | grep -c .) impl_before_seal=$(git rev-list "$BASE..$seal" | while read -r c; do git show --name-only --format= "$c" | grep -v '^\.harness/' | grep -q . && echo x; done | grep -c .) first_impl_after_seal=${later:+1}" ;;
AR-03)
  find .harness -maxdepth 1 -type f -name 'sprint-contract*.md' | sort | while IFS= read -r f; do
    rec=$(fm_get "$f" conditions_digest); rec=${rec#sha256:}
    if [ -z "$rec" ]; then echo "SEAL_ABSENT"; continue; fi
    act=$(grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$f" | sed -E 's/^- \[[ x]\]/- [ ]/' | sha256_16)
    [ "$rec" = "$act" ] && echo "SEAL_OK" || echo "SEAL_BROKEN $f"
  done | awk '{print $1}' | sort | uniq -c | tr '\n' ' '; echo
  echo "tools_sha=$(cat "$HERE/m.sh" "$HERE/ob.py" "$HERE/ka5.sh" "$HERE/stub.py" | sha256_16)" ;;
DOCS)
  U=$(git rev-parse --verify -q chore/ak2-k4) || { echo "UNRESOLVED chore/ak2-k4"; exit 2; }
  echo "docs_changed=[$(git diff --name-only "$BASE" "$U" -- docs | tr '\n' ' ')]" ;;
DG-02)
  U=$(git rev-parse --verify -q chore/ak2-k4) || { echo "UNRESOLVED chore/ak2-k4"; exit 2; }
  bash .harness/.meta/after-0924/harness-orch-tools/lint_new.sh "$W" "$BASE" "$U" "${MDL:?MDL=markdownlint-cli2 경로}" "${PYF:?PYF=pyflakes 파이썬}"
  for j in $(git diff --name-only "$BASE" "$U" -- '*.json'); do
    python3 -c "import json,sys; json.load(open(sys.argv[1], encoding='utf-8'))" "$j" && echo "json_ok $j" || echo "json_bad $j"
  done ;;
*) echo "UNKNOWN $ID"; exit 2 ;;
esac
