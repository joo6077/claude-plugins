#!/usr/bin/env bash
# after-0926-docs-regen-a 계약의 측정 묶음. 사용: bash measure.sh <조건 번호>
# 환경: REPO(기본 이 파일 기준 레포 뿌리) · U(기본 chore/ak2-dr1a 가지 끝 — 해석이 안 되면 멈춘다) · SCR(임시 폴더 뿌리, 기본 ${TMPDIR:-/tmp})
# 기준 판 BASE=38cccd1 은 이 묶음이 가지를 딴 판이다. 원본 담김의 옛 판도 이것이다.
# 도구 두 개는 레포 밖 부모 세션 자리에 있다 — TOOLS 아래 coverage.py · fence2.py · ci-local.sh. 그 폴더 안에서 python3 를 돌리지 않는다.
set -u
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=${REPO:-$(cd "$HERE/../../.." && pwd)}
BASE=38cccd1
BR=chore/ak2-dr1a
TOOLS=/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools
SCR=${SCR:-${TMPDIR:-/tmp}}
SIGN='Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>'

tip() {
  if [ -n "${U:-}" ]; then echo "$U"; return 0; fi
  git -C "$REPO" rev-parse --verify -q "$BR" || { echo "UNRESOLVED $BR" >&2; return 1; }
}

pages() { cut -d' ' -f2 "$HERE/pairs.txt" | LC_ALL=C sort -u; }

tree_at() {  # tree_at <판> → 그 판을 푼 임시 폴더 경로
  local d
  d=$(mktemp -d "$SCR/dr1a-tree.XXXXXX") || return 2
  git -C "$REPO" archive "$1" scripts docs | tar -x -C "$d" || { rm -rf "$d"; return 2; }
  echo "$d"
}

case "${1:-}" in
SK-01)  # 원본 코드 표시 · 낱말 비율이 옛 판(BASE) 페이지보다 떨어지지 않는다
  bad=0; n=0
  while IFS=$'\t' read -r src page b_codes b_wr _; do
    case "$src" in '#'*) continue ;; esac
    n=$((n+1))
    out=$(python3 "$TOOLS/coverage.py" "$REPO" "$src" "$page" "$BASE") || { echo "READ_FAIL $page"; bad=$((bad+1)); continue; }
    new=$(printf '%s\n' "$out" | sed -E 's/.*\tnew=([0-9]+).*/\1/')
    lost=$(printf '%s\n' "$out" | sed -E 's/.*\tlost=([0-9]+).*/\1/')
    wr=$(printf '%s\n' "$out" | sed -E 's/.*->([0-9.]+).*/\1/')
    ok=$(awk -v a="$new" -v b="$b_codes" -v l="$lost" -v w="$wr" -v bw="$b_wr" 'BEGIN{print (a+0>=b+0 && l+0==0 && w+0>=bw+0) ? 1 : 0}')
    [ "$ok" = 1 ] || bad=$((bad+1))
    printf '%s\t%s\tnew=%s/%s\tlost=%s\twr=%s/%s\t%s\n' "$page" "$src" "$new" "$b_codes" "$lost" "$wr" "$b_wr" "$([ "$ok" = 1 ] && echo ok || echo BAD)"
  done < "$HERE/baseline.tsv"
  echo "pairs=$n bad=$bad"; [ "$bad" = 0 ] ;;
SK-02)  # 원본 코드 블록 줄이 페이지에 든 수가 옛 판 이상 · fence2 의 lost 0
  bad=0; n=0
  while IFS=$'\t' read -r src page _ _ b_fence; do
    case "$src" in '#'*) continue ;; esac
    n=$((n+1))
    out=$(python3 "$TOOLS/fence2.py" "$REPO" "$src" "$page") || { echo "READ_FAIL $page"; bad=$((bad+1)); continue; }
    inn=$(printf '%s\n' "$out" | sed -E 's/.*\tin_new=([0-9]+).*/\1/')
    lost=$(printf '%s\n' "$out" | sed -E 's/.*\tlost=([0-9]+).*/\1/')
    if [ "$inn" -ge "$b_fence" ] && [ "$lost" = 0 ]; then r=ok; else r=BAD; bad=$((bad+1)); fi
    printf '%s\t%s\tin_new=%s/%s\tlost=%s\t%s\n' "$page" "$src" "$inn" "$b_fence" "$lost" "$r"
  done < "$HERE/baseline.tsv"
  echo "pairs=$n bad=$bad"; [ "$bad" = 0 ] ;;
SK-03)  # 페이지 머리(본문 첫 700 글자)에 원본 머리의 판 번호 · 날짜
  python3 - "$REPO" "$HERE/heads.tsv" <<'PY'
import html, re, sys
repo, heads = sys.argv[1], sys.argv[2]
bad = n = 0
for line in open(heads, encoding='utf-8'):
    if line.startswith('#') or not line.strip():
        continue
    page, *toks = line.rstrip('\n').split('\t')
    n += 1
    h = open(f'{repo}/{page}', encoding='utf-8').read()
    body = h.split('<body', 1)[1]
    body = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', body)
    text = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', '<' + body)))[:700]
    miss = [t for t in toks if t not in text]
    bad += bool(miss)
    print(f'{page}\t{"ok" if not miss else "BAD missing=" + ",".join(miss)}')
print(f'pages={n} bad={bad}')
sys.exit(1 if bad else 0)
PY
  ;;
SK-04)  # 페이지가 마지막으로 고쳐진 뒤(BASE 기준) 원본에 새로 생긴 코드 표시가 모두 페이지에 든다
  python3 "$HERE/drift.py" "$REPO" "$HERE/pairs.txt" "$BASE" ;;
SK-05)  # notes 가 짚은 산문 어긋남 — 옛 글 0 · 새 글 1 이상
  bad=0
  chk() {  # chk <페이지> <기대 absent|present> <글>
    local c; c=$(grep -cF -- "$3" "$REPO/$1"); local r=ok
    if [ "$2" = absent ] && [ "$c" != 0 ]; then r=BAD; fi
    if [ "$2" = present ] && [ "$c" = 0 ]; then r=BAD; fi
    [ "$r" = ok ] || bad=$((bad+1))
    printf '%s\t%s\t[%s]\tcount=%s\t%s\n' "$1" "$2" "$3" "$c" "$r"
  }
  chk docs/harness/qa-evaluation-guide.html absent '50 개를 넘는 삭제만'
  chk docs/harness/qa-evaluation-guide.html present 'sprint-scope'
  chk docs/harness/contract-schema.html present '페이지 맞추기 계약'
  chk docs/bambu-kit/bambu-print-profile.html present '종류 줄만 빠진'
  chk docs/process/kaizen-flow.html present 'templates/'
  chk docs/harness/plugin-validation.html present 'no templates/ — OK'
  echo "items=6 bad=$bad"; [ "$bad" = 0 ] ;;
SK-06)  # 설계 가이드의 조건 패턴 수가 스킬 표의 실제 행 수(8)와 같고 페이지도 같다
  rows=$(awk '/^\*\*조건 패턴 8 종/{f=1;next} f&&/^\| \*\*/{n++} f&&/^$/&&n{exit} END{print n+0}' "$REPO/harness/skills/sprint-contract/SKILL.md")
  g5=$(grep -cF '조건 패턴 5 종' "$REPO/harness/docs/guides/contract-design-guide.md")
  g8=$(grep -cF '조건 패턴 8 종' "$REPO/harness/docs/guides/contract-design-guide.md")
  p5=$(grep -cF '조건 패턴 5 종' "$REPO/docs/harness/contract-design-guide.html")
  p8=$(grep -cF '조건 패턴 8 종' "$REPO/docs/harness/contract-design-guide.html")
  echo "skill_rows=$rows guide5=$g5 guide8=$g8 page5=$p5 page8=$p8"
  [ "$rows" = 8 ] && [ "$g5" = 0 ] && [ "$g8" = 1 ] && [ "$p5" = 0 ] && [ "$p8" -ge 1 ] ;;
SK-07)  # 공통 링크 docs/assets/site.css 가 쪽마다 정확히 하나
  bad=0; n=0
  for p in $(pages); do
    n=$((n+1))
    l=$(grep -oE '<link[^>]*href="\.\./assets/site\.css"[^>]*>' "$REPO/$p" | grep -c .)
    a=$(grep -o 'assets/site\.css' "$REPO/$p" | grep -c .)
    if [ "$l" = 1 ] && [ "$a" = 1 ]; then r=ok; else r=BAD; bad=$((bad+1)); fi
    printf '%s\tlink=%s\tmentions=%s\t%s\n' "$p" "$l" "$a" "$r"
  done
  echo "pages=$n bad=$bad"; [ "$bad" = 0 ] ;;
SK-08)  # 세 폭 × 두 테마 넘침 · 글 잘림 · 콘솔 오류
  pages | (cd "$REPO" && xargs node "$HERE/layout.js" "$REPO") | grep -E 'BAD|cells=|OPEN_FAIL'
  st=("${PIPESTATUS[@]}"); [ "${st[1]}" = 0 ] ;;
SC-01)  # 외부 리소스 판정 — 사례 30 · 기준 판과 200 입력 맞대기 · 끝 판 트리 12 쪽 · 마지막 쪽과 첫 쪽 사본
  T=$(tip) || exit 2
  f=$(mktemp "$SCR/dr1a-chk.XXXXXX"); b=$(mktemp "$SCR/dr1a-base.XXXXXX")
  git -C "$REPO" show "$T:scripts/check-api-kit-docs.py" > "$f"; git -C "$REPO" show "$BASE:scripts/check-api-kit-docs.py" > "$b"
  c=$(python3 "$HERE/ext_cases.py" "$f"); cmp=$(python3 "$HERE/ext_cases.py" --compare "$b" "$f")
  d=$(tree_at "$T") || exit 2
  (cd "$d" && python3 scripts/check-api-kit-docs.py > out0.txt); rc0=$?
  last=$(cd "$d" && find docs/api -name '*.md' ! -name research-log.md | LC_ALL=C sort | tail -1 | sed -E 's#.*/##; s#\.md$##')
  first=$(cd "$d" && find docs/api -name '*.md' ! -name research-log.md | LC_ALL=C sort | head -1 | sed -E 's#.*/##; s#\.md$##')
  sed -i.bak 's#</body>#<img src="https://x.test/a.png" alt=""></body>#' "$d/docs/api-kit/$last.html"
  ap1=$(grep -c 'src="https://x.test/a.png"' "$d/docs/api-kit/$last.html")
  (cd "$d" && python3 scripts/check-api-kit-docs.py > out1.txt); rc1=$?
  mv "$d/docs/api-kit/$last.html.bak" "$d/docs/api-kit/$last.html"
  sed -i.bak 's#</style>#.x{background:url(//cdn.x.test/a.png)}</style>#' "$d/docs/api-kit/$first.html"
  ap2=$(grep -c 'url(//cdn.x.test/a.png)' "$d/docs/api-kit/$first.html")
  (cd "$d" && python3 scripts/check-api-kit-docs.py > out2.txt); rc2=$?
  echo "$c | $cmp | tree=[$(tail -1 "$d/out0.txt")] rc0=$rc0 | last=$last applied1=$ap1 rc1=$rc1 fail1=$(grep -c '^FAIL' "$d/out1.txt") fail1_last=$(grep -c "^FAIL docs/api-kit/$last.html" "$d/out1.txt") | first=$first applied2=$ap2 rc2=$rc2 fail2=$(grep -c '^FAIL' "$d/out2.txt") fail2_first=$(grep -c "^FAIL docs/api-kit/$first.html" "$d/out2.txt")"
  rm -rf "$d" "$f" "$b" ;;
SC-02)  # CI 첫 작업에 한 단계 · 종료 코드 표 한 행
  T=$(tip) || exit 2
  ci=$(git -C "$REPO" show "$T:.github/workflows/ci.yml")
  steps=$(printf '%s\n' "$ci" | grep -cE '^[[:space:]]+run: python3 scripts/check-api-kit-docs\.py[[:space:]]*$')
  job=$(printf '%s\n' "$ci" | awk '/^jobs:/{j=1;next} j&&/^  [A-Za-z0-9_-]+:/{cur=$(1)} /run: python3 scripts\/check-api-kit-docs\.py/{print cur; exit}')
  first=$(printf '%s\n' "$ci" | awk '/^jobs:/{j=1;next} j&&/^  [A-Za-z0-9_-]+:/{print $(1); exit}')
  row=$(git -C "$REPO" show "$T:harness/evals/gate-exit-codes.md" | grep -cF '| `scripts/check-api-kit-docs.py` | 0 · 1 |')
  echo "ci_steps=$steps job=[$job] first_job=[$first] exitdoc=$row" ;;
SC-03)  # 문서 검사 다섯 — 종료 코드와 검사한 수를 함께
  cd "$REPO" || exit 2
  pages | xargs node scripts/check-docs-a11y.js > "$SCR/dr1a-a11y.txt" 2>&1; a=$?
  python3 scripts/check-docs-links.py > "$SCR/dr1a-links.txt" 2>&1; l=$?
  python3 scripts/check-contrast-claims.py > "$SCR/dr1a-contrast.txt" 2>&1; c=$?
  python3 scripts/check-api-kit-docs.py > "$SCR/dr1a-api.txt" 2>&1; k=$?
  python3 scripts/detect-docs-drift.py --check-table > "$SCR/dr1a-table.txt" 2>&1; t=$?
  echo "a11y=rc$a/[$(tail -1 "$SCR/dr1a-a11y.txt")] links=rc$l/[$(grep -c '고아 · 유령 · 아이콘 누락 없음' "$SCR/dr1a-links.txt")] contrast=rc$c/[$(grep -c '어긋난 것: 0' "$SCR/dr1a-contrast.txt")] api=rc$k/[$(tail -1 "$SCR/dr1a-api.txt")] table=rc$t/[$(grep -c '어긋남 0' "$SCR/dr1a-table.txt")]" ;;
SC-04)  # 로컬 CI 전체와 그 스크립트 밖의 CI 단계 셋
  cd "$REPO" || exit 2
  O=$(mktemp -d "$SCR/dr1a-ci.XXXXXX")
  echo "tool=$(shasum -a 256 "$TOOLS/ci-local.sh" | cut -c1-16)"
  TMPDIR=$O bash "$TOOLS/ci-local.sh" "$REPO" > "$O/run.txt" 2>&1
  ok=$(grep -c 'rc=0' "$O/ci-local/summary.txt"); other=$(grep -v 'rc=0' "$O/ci-local/summary.txt")
  python3 scripts/check-cause-table-copies.py > /dev/null 2>&1; cc=$?
  bash harness/evals/measure/measure-helpers-test.sh > /dev/null 2>&1; mh=$?
  echo "ci_local_ok=$ok other=[$other] cause_copies=rc$cc measure_helpers=rc$mh" ;;
ER-01)  # 쪽 하나가 없어도 나머지를 다 재고 없는 쪽을 이름으로 댄다 (기존 동작 유지)
  T=$(tip) || exit 2
  d=$(tree_at "$T") || exit 2
  rm "$d/docs/api-kit/multi-sample-pagination-variance.html"
  (cd "$d" && python3 scripts/check-api-kit-docs.py > out.txt); rc=$?
  echo "rc=$rc rows=$(grep -cE '^(OK  |FAIL) docs/api-kit/' "$d/out.txt") missing_named=$(grep -A1 '^FAIL docs/api-kit/multi-sample-pagination-variance.html' "$d/out.txt" | grep -c 'HTML 없음') summary=[$(tail -1 "$d/out.txt")]"
  rm -rf "$d" ;;
AR-01)  # 바뀐 경로가 범위 목록 안 · 꼭 바뀌어야 할 넷이 있다
  T=$(tip) || exit 2
  scope=$(awk '/^## 범위 경계/{s=1} s&&/^# sprint-scope$/{b=1;next} b&&/^```/{exit} b&&NF{print}' "$REPO/.harness/sprint-contract-after-0926-docs-regen-a.md")
  changed=$(git -C "$REPO" diff --name-only "$BASE..$T" -- . ':(exclude).harness')
  extra=$(printf '%s\n' "$changed" | grep . | grep -vxF -f <(printf '%s\n' "$scope") | tr '\n' ' ')
  need=0
  for p in harness/docs/guides/contract-design-guide.md scripts/check-api-kit-docs.py .github/workflows/ci.yml harness/evals/gate-exit-codes.md; do
    printf '%s\n' "$changed" | grep -qxF "$p" && need=$((need+1))
  done
  echo "scope=$(printf '%s\n' "$scope" | grep -c .) changed=$(printf '%s\n' "$changed" | grep -c .) extra=[$extra] required=$need/4" ;;
AR-02)  # 커밋마다 맨 위 단위 하나 · 한국어 메시지 · 끝 줄 서명
  T=$(tip) || exit 2
  bad=0; n=0
  for c in $(git -C "$REPO" rev-list --no-merges "$BASE..$T"); do
    n=$((n+1))
    units=$(git -C "$REPO" show --name-only --format= "$c" | grep . | awk -F/ '{ if ($(1)=="docs" && NF>2) print $(1)"/"$(2); else if (NF>1) print $(1); else print "(root)" }' | LC_ALL=C sort -u | grep -c .)
    msg=$(git -C "$REPO" log -1 --format=%B "$c")
    last=$(printf '%s\n' "$msg" | grep . | tail -1)
    blank=$(printf '%s\n' "$msg" | awk -v s="$SIGN" '$(0)==s{print (prev=="") ? 1 : 0} {prev=$(0)}' | tail -1)
    ko=$(printf '%s\n' "$msg" | head -1 | grep -c '[가-힣]')
    if [ "$units" = 1 ] && [ "$last" = "$SIGN" ] && [ "$blank" = 1 ] && [ "$ko" = 1 ]; then :; else bad=$((bad+1)); echo "BAD $c units=$units sign=$([ "$last" = "$SIGN" ] && echo 1 || echo 0) blank=$blank ko=$ko"; fi
  done
  echo "commits=$n bad=$bad"; [ "$n" -ge 1 ] && [ "$bad" = 0 ] ;;
AR-03)  # 계약 봉인 · 봉인 커밋 · 측정 묶음 지문
  T=$(tip) || exit 2
  CF=.harness/sprint-contract-after-0926-docs-regen-a.md
  sc=$(git -C "$REPO" log --reverse --format=%H "$BASE..$T" -- "$CF" | head -1)
  files=$(git -C "$REPO" show --name-only --format= "$sc" | grep -c .)
  impl=$(git -C "$REPO" rev-list --reverse "$BASE..$T" -- . ':(exclude).harness' | head -1)
  before=0; [ -n "$sc" ] && [ -n "$impl" ] && git -C "$REPO" merge-base --is-ancestor "$sc" "$impl" && before=1
  src=$(git -C "$REPO" show "$T:$CF")
  fm() { printf '%s\n' "$src" | awk -v k="^${1}:[[:space:]]*" 'NR==1&&/^---/{f=1;next} f&&/^---/{exit} f&&$(0)~k{sub(k,"");print;exit}'; }
  cd_rec=$(fm conditions_digest); cd_rec=${cd_rec#sha256:}
  cd_act=$(printf '%s\n' "$src" | grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' | sed -E 's/^- \[[ x]\]/- [ ]/' | shasum -a 256 | cut -c1-16)
  md_rec=$(fm measurement_digest); md_rec=${md_rec#sha256:}
  md_act=$(printf '%s\n' "$src" | awk '/^- \[[ x]\] [A-Z][A-Z]+-[0-9][0-9]/{inb=1; match($(0), /[A-Z][A-Z]+-[0-9][0-9]/); print substr($(0), RSTART, RLENGTH); next} inb&&/^[ \t]+[^ \t]/{l=$(0); sub(/[ \t]+$/,"",l); print l; next} inb&&/^[ \t]*$/{next} {inb=0}' | shasum -a 256 | cut -c1-16)
  sums=$(cd "$HERE" && for x in measure.sh pairs.txt baseline.tsv heads.tsv drift.py layout.js ext_cases.py; do printf '%s=%s ' "$x" "$(shasum -a 256 "$x" | cut -c1-16)"; done)
  echo "seal_commit_files=$files seal_before_impl=$before seal=$([ -n "$cd_rec" ] && [ "$cd_rec" = "$cd_act" ] && echo OK || echo BROKEN) measure=$([ -n "$md_rec" ] && [ "$md_rec" = "$md_act" ] && echo OK || echo BROKEN)"
  echo "bundle $sums" ;;
AR-04)  # 묶음 기록 — 커밋 목록 · tone-guide 5 단계 대조 · 조건별 자기 측정
  T=$(tip) || exit 2
  N=.harness/.meta/after-kaizen-0926b/dr1a-notes.md
  body=$(git -C "$REPO" show "$T:$N" 2>/dev/null) || { echo "notes=0"; exit 1; }
  echo "notes=1 commits_h=$(printf '%s\n' "$body" | grep -c '^## 커밋 목록') tone_h=$(printf '%s\n' "$body" | grep -c '^## tone-guide 5 단계 대조') self_h=$(printf '%s\n' "$body" | grep -c '^## 조건별 자기 측정') tone_rows=$(printf '%s\n' "$body" | awk '/^## tone-guide 5 단계 대조/{f=1;next} f&&/^## /{exit} f&&/^\| /{n++} END{print n+0}')" ;;
AP-02)  # 이 가지를 원격에 밀지 않았다
  echo "remote_heads=$(git -C "$REPO" ls-remote --heads origin "$BR" | grep -c .)" ;;
AP-03)  # 바뀐 md 의 코드 블록 여는 줄 — validate-plugin V6
  cd "$REPO" && python3 scripts/validate-plugin.py harness --check=code-fence > "$SCR/dr1a-v6.txt" 2>&1; r=$?
  echo "rc=$r v6=[$(grep -E 'V6 code-fence' "$SCR/dr1a-v6.txt" | sed -E 's/^ +//')]" ;;
DG-02)  # 바뀐 md 편집기 경고(MD013 끔) · 바뀐 py 컴파일
  cd "$REPO" || exit 2
  ML=${ML:-$SCR/mdlint}
  "$ML/node_modules/.bin/markdownlint-cli2" --config "$ML/cfg.markdownlint-cli2.jsonc" harness/docs/guides/contract-design-guide.md > "$SCR/dr1a-md.txt" 2>&1; m=$?
  python3 -m py_compile scripts/check-api-kit-docs.py; p=$?
  echo "md=rc$m/[$(grep -c '^Linting: 1 file' "$SCR/dr1a-md.txt")]/[$(grep -E '^Summary' "$SCR/dr1a-md.txt")] py=rc$p" ;;
*) echo "모르는 조건: ${1:-}" >&2; exit 2 ;;
esac
