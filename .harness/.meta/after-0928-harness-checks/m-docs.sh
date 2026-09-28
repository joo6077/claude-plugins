#!/usr/bin/env bash
# m-docs.sh <레포> — 글 조건을 절 단위로 잘라 센다. 줄마다 `<자리> <낱말>=<수>`.
# 절 자르기: 머리 줄부터 같은 단계의 다음 머리 줄 앞까지 (awk). 파일 전체 grep 이 아니다.
R=${1:?레포 경로}
S=$R/harness/references/contract-schema.md
K=$R/harness/skills/sprint-contract/SKILL.md
H=$R/docs/harness/contract-schema.html
T=$(mktemp -d "${TMPDIR:-/tmp}/mdocs.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT
awk 'index($0,"#### 측정 관례")==1{f=1;print;next} f && /^#### /{exit} f' "$S" > "$T/measure.txt"
awk '/^### 0\.5\. /{f=1} /^### 1\. /{f=0} f' "$K" > "$T/s05.txt"
awk '/^## Gotchas/{f=1;next} f && /^## /{exit} f' "$K" > "$T/gotchas.txt"
cnt() { printf '%s %s=%s\n' "$1" "$2" "$(grep -cF -- "$2" "$3")"; }
echo "measure_lines=$(grep -c . "$T/measure.txt") s05_lines=$(grep -c . "$T/s05.txt") gotcha_lines=$(grep -c . "$T/gotchas.txt")"
for w in 'disable-next-line' 'meaning.py' 'AR-02' 'SC-01' 'DG-02' '--format=%B' 'sort -u'; do cnt schema-측정관례 "$w" "$T/measure.txt"; done
for w in 'status: superseded' 'superseded_by' 'check-superseded.sh' 'SEAL_OK'; do cnt skill-0.5 "$w" "$T/s05.txt"; done
for w in '측정 관례' '--format=%B'; do cnt skill-gotchas "$w" "$T/gotchas.txt"; done
cnt schema-전체 'harness/scripts/check-superseded.sh' "$S"
for w in 'check-superseded.sh' 'disable-next-line' 'meaning.py' 'assets/site.css'; do cnt html "$w" "$H"; done
# 계약 형식 문서의 fm_get 과 페이지의 fm_get 이 글자까지 같은가 (페이지는 글자 참조를 푼 뒤)
awk '/^fm_get\(\) \{ # fm_get/{f=1} f{print} f && /^}/{exit}' "$S" > "$T/md.fm"
python3 - "$H" "$T/html.fm" <<'PY'
import html, re, sys
text = html.unescape(re.sub(r"<[^>]+>", "", open(sys.argv[1], encoding="utf-8").read()))
lines = text.split("\n"); out = []; on = False
for ln in lines:
    if ln.startswith("fm_get() { # fm_get"): on = True
    if on:
        out.append(ln)
        if ln == "}": break
open(sys.argv[2], "w", encoding="utf-8").write("\n".join(out) + ("\n" if out else ""))
PY
printf 'fm_same=%s md_lines=%s html_lines=%s\n' "$(cmp -s "$T/md.fm" "$T/html.fm" && echo 1 || echo 0)" "$(grep -c . "$T/md.fm")" "$(grep -c . "$T/html.fm")"
