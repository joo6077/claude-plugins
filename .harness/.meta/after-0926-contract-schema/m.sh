#!/usr/bin/env bash
# 계약 after-0926-contract-schema 측정 묶음. 해석기는 bash 로 고정한다 (도우미 실행 칸만 zsh 를 따로 부른다).
# 사용: bash m.sh <조건 ID | all>
# 환경: R 저장소 (기본 이 파일 위치에서 셋 위) · B 기준 판 (기본 6378948) · U 상한 (기본 가지 chore/ak2-cs 끝)
# 출력: 조건마다 `PASS <ID> …` 또는 `FAIL <ID> …`. 종료 코드 0 모두 통과 · 1 하나라도 실패 · 2 준비 실패
set -u
HERE=$(cd "$(dirname "${0}")" && pwd)
R=${R:-$(cd "$HERE/../../.." && pwd)}
B=${B:-6378948}
if [ -z "${U:-}" ]; then U=$(git -C "$R" rev-parse --verify -q chore/ak2-cs) || { echo "STOP 상한 chore/ak2-cs 해석 실패" >&2; exit 2; }; fi
git -C "$R" rev-parse --verify -q "$B^{commit}" >/dev/null || { echo "STOP 기준 $B 없음" >&2; exit 2; }
git -C "$R" rev-parse --verify -q "$U^{commit}" >/dev/null || { echo "STOP 상한 $U 없음" >&2; exit 2; }
command -v zsh >/dev/null || { echo "STOP zsh 없음" >&2; exit 2; }
H="python3 $HERE/hunks.py"
S=harness/references/contract-schema.md
FB=harness/references/feedback-schema.yaml
SK=harness/skills/sprint-contract/SKILL.md
T=$(mktemp -d "${TMPDIR:-/tmp}/cs-m.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT
git -C "$R" show "$U:$S" > "$T/S.md" 2>/dev/null || : > "$T/S.md"
git -C "$R" show "$U:$SK" > "$T/SK.md" 2>/dev/null || : > "$T/SK.md"

H_TOP='# Sprint Contract 스키마'
H_SHELL='### 셸 이식성 규약 — 글로빙 대신 `find` (v5.1)'
H_HARN='##### `.harness/` 범위 조건 — 산출물 슬러그를 열거하지 마라 (2026-09-23 추가)'
H_MULTI='##### 여러 주체가 한 가지에 커밋할 때 — 서명 줄로 내 커밋을 가린다 (2026-09-24 추가)'
H_UNMEAS='#### 미실측 오라클 봉인 금지 (v5.4 추가)'
H_FACTOR='#### 인자 매트릭스 (Factor Matrix · v5.3 추가)'
H_KNOWN='#### 알려진 답 대조 (Known-Answer · 0 이 아닌 기대값 · v5.5 추가)'
H_CHECK='#### 산출물이 검사인 조건 — 사본 대조 ①~④ 의 계약 측 짝 (v5.7 추가)'
H_KEEP='#### 기존 동작 유지 조건 — 기준 판과 새 판을 여러 입력으로 맞댄다 (v5.7 추가)'
H_MEAS='#### 측정 관례 — 두 판 풀기 · 줄 번호 · 넘김 목록 (v5.7 추가)'
H_PAGE='#### 페이지 맞추기 계약 — 다섯 가지 (v5.7 추가)'
H_DIAG='### 4. Diagnostics (자동 포함)'
H_ENTRY='### 엔트리 포맷'
H_VER='## 스키마 버전'
H_S4='### 4. 자동 포함 섹션'

fails=0
pass() { echo "PASS $*"; }
fail() { echo "FAIL $*"; fails=$((fails + 1)); }

# need <ID> <더한 줄 파일> <낱말>... — 낱말마다 더한 줄에 1 번 이상 (글자 그대로)
need() {
  _id=${1}; _f=${2}; shift 2; _miss=""
  for _w in "$@"; do grep -qF -- "$_w" "$_f" || _miss="$_miss [$_w]"; done
  if [ -z "$_miss" ]; then pass "$_id n_added=$(grep -c . "$_f")"; else fail "$_id 빠진 낱말:$_miss n_added=$(grep -c . "$_f")"; fi
}
added_in() { $H added "$R" "$B" "$U" "$1" "$2" > "$3" || { echo "STOP hunks.py 실패" >&2; exit 2; }; }

fb_in() {  # 피드백 형식 파일 자기진단 절 안에 더한 줄 → $T/fb.in (표지 줄 못 찾으면 1)
  git -C "$R" diff -U0 --no-color "$B" "$U" -- "$FB" | awk '
    /^@@/ { match($0, /\+[0-9]+/); n = substr($0, RSTART + 1, RLENGTH - 1) + 0; next }
    /^\+\+\+/ { next } /^\+/ { print n "\t" substr($0, 2); n++ }' > "$T/fb.add"
  git -C "$R" show "$U:$FB" > "$T/fb.yaml"
  a=$(grep -n '^# --- 자기진단' "$T/fb.yaml" | cut -d: -f1); z=$(grep -n '^# --- 사용자 시그널' "$T/fb.yaml" | cut -d: -f1)
  [ -n "$a" ] && [ -n "$z" ] || return 1
  awk -F'\t' -v a="$a" -v z="$z" '$1 > a && $1 < z' "$T/fb.add" > "$T/fb.in"
}
c_SK01() {
  fb_in || { fail "SK-01 자기진단 · 사용자 시그널 표지 줄을 못 찾음"; return; }
  need SK-01 "$T/fb.in" 'measure_premise_unrun: bool' 'known_answer_missing: bool' '문제가 있다' 'sprint-contract/SKILL.md' 'Step 7'
}
c_SK02() { added_in "$S" "$H_ENTRY" "$T/a"; need SK-02 "$T/a" '같은 번호를 두 번 쓰지 않는다'; }
c_SK03() { added_in "$S" "$H_MEAS" "$T/a"; need SK-03 "$T/a" '`경로:13:8`' '`경로:줄`' '측정 묶음을 QA 에 같이 넘긴다' 'mktemp -d "${TMPDIR:-/tmp}/' '검사기가 돌았다는 줄' '더한 줄의 자리와 수' 'git diff -U0' 'validate-doc-contracts.py' 'git init' 'git add -A' 'NOT RUN' 'with_two' 'line_of'; }
c_SK04() { added_in "$S" "$H_MULTI" "$T/a"; need SK-04 "$T/a" 'unsigned_on' '같은 정의'; }
c_SK05() { added_in "$S" "$H_CHECK" "$T/a"; need SK-05 "$T/a" '①' '②' '③' '④' 'qa-evaluation-guide.md' '첫 칸' '실행 목록' '못 읽는 칸' 'zsh' 'bash'; }
c_SK06() { added_in "$S" "$H_SHELL" "$T/a"; need SK-06 "$T/a" 'comm' 'LC_ALL=C sort' 'sort -n'; }
c_SK07() { added_in "$S" "$H_KEEP" "$T/a"; need SK-07 "$T/a" '목표 문장' '하위 문장' '무작위' '시드' '3 개 이상' '조건 문장 안, 측정 밖' '계약 문언 밖'; }
c_SK08() { added_in "$S" "$H_HARN" "$T/a"; need SK-08 "$T/a" 'dirty_except_status' 'QA 가 바꾸는'; }
c_SK09() { added_in "$S" "$H_FACTOR" "$T/a"; need SK-09 "$T/a" '판정 규칙' 'FAIL 이 하나 이상인 칸'; }
c_SK10() { added_in "$S" "$H_DIAG" "$T/a"; need SK-10 "$T/a" '<!-- AUTO:' '블록 안' '블록 밖'; }
c_SK11() { added_in "$SK" "$H_S4" "$T/a"; need SK-11 "$T/a" '<!-- AUTO:' '블록 안' '블록 밖' 'contract-schema.md'; }
c_SK12() { added_in "$S" "$H_UNMEAS" "$T/a"; need SK-12 "$T/a" 'markdownlint-cli2@' '설치 명령'; }
c_SK13() { added_in "$S" "$H_PAGE" "$T/a"; need SK-13 "$T/a" 'plugins' '쉼표' '작은따옴표' '@import' '//' '종료 코드' '상세 줄' '양성 대조'; }
c_SK14() {  # 세 파일 더한 줄의 쉬운 말 목록 낱말
  : > "$T/all.add"
  for f in "$S" "$SK" "$FB"; do git -C "$R" diff -U0 --no-color "$B" "$U" -- "$f" | grep '^+' | grep -v '^+++' | cut -c2- >> "$T/all.add"; done
  python3 "$HERE/plain.py" "$HERE/plain-korean.snapshot.md" < "$T/all.add" > "$T/pk.out"; rc=$?
  [ "$rc" = 0 ] || { fail "SK-14 plain.py rc=$rc"; return; }
  h=$(tail -1 "$T/pk.out"); n=$(grep -c . "$T/all.add")
  case "$h" in "hits=0 "*) pass "SK-14 $h n_added=$n";; *) fail "SK-14 $h n_added=$n"; grep '^HIT' "$T/pk.out" | head -20;; esac
}

# run_both <이름> <도우미 블록 파일> <시험 본문 파일> — bash · zsh 에서 같은 시험을 돌려 출력 두 벌을 남긴다
run_both() {
  for sh in bash zsh; do
    ( cd "$T/repo" && TMPDIR="$T/tmp-$sh" "$sh" -c ". '$2'; . '$3'" ) > "$T/$1.$sh.out" 2>&1
    echo "rc=$?" >> "$T/$1.$sh.out"
  done
}
mkrepo() {
  rm -rf "$T/repo"; mkdir -p "$T/repo" && cd "$T/repo" || exit 2
  git init -q && git config user.email m@x && git config user.name m
  printf 'one\n' > f.txt; git add f.txt; git commit -qm c1; git tag c1
  printf 'two\n' > f.txt; git commit -qam c2; git tag c2
  cd - >/dev/null || exit 2
}
c_SC01() {  # with_two — 두 판 풀기, 명령 결과 그대로, 끝나면 지움, TMPDIR 아래
  $H block "$T/S.md" "$H_MEAS" with_two > "$T/with_two.sh" 2>"$T/blk.err" || { fail "SC-01 with_two 블록: $(cat "$T/blk.err")"; return; }
  mkrepo
  cat > "$T/t1.sh" <<'EOF'
mkdir -p "$TMPDIR"
show() { printf 'dir1=%s\n' "${1}"; cat "${1}/f.txt" "${2}/f.txt"; }
with_two . c1 c2 show; echo "cmd_rc=$?"
with_two . c1 c2 false; echo "false_rc=$?"
echo "left=$(find "$TMPDIR" -mindepth 1 | wc -l | tr -d ' ')"
EOF
  run_both sc01 "$T/with_two.sh" "$T/t1.sh"
  ok=1
  for sh in bash zsh; do
    o="$T/sc01.$sh.out"
    grep -q "^dir1=$T/tmp-$sh/" "$o" && [ "$(grep -xc 'one' "$o")" = 1 ] && [ "$(grep -xc 'two' "$o")" = 1 ] \
      && grep -qx 'cmd_rc=0' "$o" && grep -qx 'false_rc=1' "$o" && grep -qx 'left=0' "$o" || { ok=0; echo "  [$sh] $(tr '\n' ' ' < "$o")"; }
  done
  [ $ok = 1 ] && pass "SC-01 bash·zsh 같은 결과 (one/two · cmd_rc=0 · false_rc=1 · left=0 · TMPDIR 아래)" || fail "SC-01"
}
c_SC02() {  # line_of — 경고 줄에서 줄 번호
  $H block "$T/S.md" "$H_MEAS" line_of > "$T/line_of.sh" 2>"$T/blk.err" || { fail "SC-02 line_of 블록: $(cat "$T/blk.err")"; return; }
  mkrepo
  cat > "$T/t2.sh" <<'EOF'
printf '%s\n' 'a/b.md:13:8 error MD060 x' 'c.md:104 error MD032 y' 'd/e f.md:7:1 warn z' | line_of | tr '\n' ' '; echo
EOF
  run_both sc02 "$T/line_of.sh" "$T/t2.sh"
  ok=1
  for sh in bash zsh; do grep -qx '13 104 7 ' "$T/sc02.$sh.out" || { ok=0; echo "  [$sh] $(tr '\n' ' ' < "$T/sc02.$sh.out")"; }; done
  [ $ok = 1 ] && pass "SC-02 bash·zsh 모두 '13 104 7'" || fail "SC-02"
}
c_SC03() {  # dirty_except_status — 계약 status 줄만 빼고 센 미커밋 변경 수
  $H block "$T/S.md" "$H_HARN" dirty_except_status > "$T/des.sh" 2>"$T/blk.err" || { fail "SC-03 dirty_except_status 블록: $(cat "$T/blk.err")"; return; }
  mkrepo
  ( cd "$T/repo" && printf -- '---\nstatus: active\n---\n- [ ] AR-01: x\n' > c.md && printf 'o\n' > o.txt && git add c.md o.txt && git commit -qm c3 )
  cat > "$T/t3.sh" <<'EOF'
reset() { git checkout -q -- c.md o.txt; rm -f new.txt; }
reset; printf 'k1=%s\n' "$(dirty_except_status c.md)"
reset; sed 's/^status: active$/status: done/' c.md > c.tmp && mv c.tmp c.md; printf 'k2=%s\n' "$(dirty_except_status c.md)"
reset; sed -e 's/^status: active$/status: done/' -e 's/AR-01: x/AR-01: y/' c.md > c.tmp && mv c.tmp c.md; printf 'k3=%s\n' "$(dirty_except_status c.md)"
reset; printf 'p\n' >> o.txt; printf 'k4=%s\n' "$(dirty_except_status c.md)"
reset; printf 'n\n' > new.txt; printf 'k5=%s\n' "$(dirty_except_status c.md)"
reset
EOF
  run_both sc03 "$T/des.sh" "$T/t3.sh"
  ok=1
  for sh in bash zsh; do
    o="$T/sc03.$sh.out"
    for kv in k1=0 k2=0 k3=2 k4=1 k5=1; do grep -qx "$kv" "$o" || { ok=0; echo "  [$sh] $kv 아님: $(tr '\n' ' ' < "$o")"; break; }; done
  done
  [ $ok = 1 ] && pass "SC-03 bash·zsh 모두 k1=0 k2=0 k3=2 k4=1 k5=1" || fail "SC-03"
}
c_ER01() {  # 실패를 성공처럼 삼키지 않는다
  $H block "$T/S.md" "$H_MEAS" with_two > "$T/with_two.sh" 2>/dev/null || { fail "ER-01 with_two 블록 없음"; return; }
  $H block "$T/S.md" "$H_HARN" dirty_except_status > "$T/des.sh" 2>/dev/null || { fail "ER-01 dirty_except_status 블록 없음"; return; }
  mkrepo
  cat > "$T/t4.sh" <<'EOF'
mkdir -p "$TMPDIR"
mark() { : > ran.flag; }
with_two . c1 no-such-rev mark; echo "bad_rc=$?"
echo "ran=$([ -e ran.flag ] && echo yes || echo no)"
echo "left=$(find "$TMPDIR" -mindepth 1 | wc -l | tr -d ' ')"
out=$(dirty_except_status no-such-file.md); echo "des_rc=$?"; echo "des_out=[$out]"
EOF
  cat "$T/with_two.sh" "$T/des.sh" > "$T/both.sh"
  run_both er01 "$T/both.sh" "$T/t4.sh"
  ok=1
  for sh in bash zsh; do
    o="$T/er01.$sh.out"
    grep -qx 'bad_rc=0' "$o" && ok=0
    grep -qx 'ran=no' "$o" && grep -qx 'left=0' "$o" && grep -qx 'des_out=\[\]' "$o" && ! grep -qx 'des_rc=0' "$o" || ok=0
    [ $ok = 1 ] || echo "  [$sh] $(tr '\n' ' ' < "$o")"
  done
  [ $ok = 1 ] && pass "ER-01 bash·zsh 모두 bad_rc≠0 · ran=no · left=0 · des_rc≠0 · des_out 빈 값" || fail "ER-01"
}

c_AR01() {  # 바뀐 경로 (.harness 제외) 정확히 세 개
  git -C "$R" diff --name-only "$B" "$U" -- . ':(exclude).harness' | LC_ALL=C sort > "$T/names"
  printf '%s\n' "$S" "$FB" "$SK" | LC_ALL=C sort > "$T/want"
  if cmp -s "$T/names" "$T/want"; then pass "AR-01 세 경로 정확히 일치"; else fail "AR-01 실제: $(tr '\n' ' ' < "$T/names")"; fi
}
c_AR02() {  # 편집 자리
  bad=""
  $H removed "$R" "$B" "$U" "$S" > "$T/s.rm"
  nrm=$(grep -c . "$T/s.rm"); n1=$(cut -f2- "$T/s.rm" | grep -cE '^> \*\*최근 갱신:'); n2=$(cut -f2- "$T/s.rm" | grep -cE '^현재: \*\*v5\.5\*\*')
  [ "$nrm" = 2 ] && [ "$n1" = 1 ] && [ "$n2" = 1 ] || bad="$bad [계약 형식 문서 지운 줄 $nrm 개: $(cut -f2 "$T/s.rm" | cut -c1-40 | tr '\n' '|')]"
  $H outside "$R" "$B" "$U" "$S" "$H_TOP" "$H_SHELL" "$H_HARN" "$H_MULTI" "$H_UNMEAS" "$H_FACTOR" "$H_KNOWN" \
     "$H_CHECK" "$H_KEEP" "$H_MEAS" "$H_PAGE" "$H_DIAG" "$H_ENTRY" "$H_VER" > "$T/s.out"
  [ "$(grep -c . "$T/s.out")" = 0 ] || bad="$bad [계약 형식 문서 허용 밖 더한 줄 $(grep -c . "$T/s.out") 개: $(cut -f2 "$T/s.out" | sort -u | tr '\n' '|')]"
  $H removed "$R" "$B" "$U" "$FB" > "$T/fb.rm"; [ "$(grep -c . "$T/fb.rm")" = 0 ] || bad="$bad [피드백 형식 지운 줄 $(grep -c . "$T/fb.rm")]"
  fb_in || { bad="$bad [자기진단 표지 줄 없음]"; }
  nfa=$(git -C "$R" diff -U0 --no-color "$B" "$U" -- "$FB" | grep '^+' | grep -vc '^+++'); nfi=$(grep -c . "$T/fb.in")
  [ "$nfa" = "$nfi" ] || bad="$bad [피드백 형식 더한 줄 $nfa 가운데 자기진단 절 안 $nfi]"
  $H removed "$R" "$B" "$U" "$SK" > "$T/sk.rm"; [ "$(grep -c . "$T/sk.rm")" = 0 ] || bad="$bad [SKILL.md 지운 줄 $(grep -c . "$T/sk.rm")]"
  $H outside "$R" "$B" "$U" "$SK" "$H_S4" > "$T/sk.out"
  [ "$(grep -c . "$T/sk.out")" = 0 ] || bad="$bad [SKILL.md 4 단계 밖 더한 줄 $(grep -c . "$T/sk.out")]"
  [ -z "$bad" ] && pass "AR-02 지운 줄 2 (판 줄) · 허용 밖 더한 줄 0 · 피드백 형식 절 안 $nfi/$nfa · SKILL.md 4 단계 밖 0" || fail "AR-02$bad"
}
c_AR03() {  # 판 번호
  bad=""
  head -10 "$T/S.md" | grep -qE '^> \*\*최근 갱신: 2026-[0-9]{2}-[0-9]{2} \(v5\.7\)\*\*' || bad="$bad [머리 v5.7]"
  head -12 "$T/S.md" | grep -qE '^> 이전: 2026-09-26 \(v5\.6\)' || bad="$bad [머리 이전 v5.6]"
  [ "$(grep -cE '^현재: \*\*v5\.7\*\* \(2026-[0-9]{2}-[0-9]{2}\)$' "$T/S.md")" = 1 ] && [ "$(grep -cE '^현재: ' "$T/S.md")" = 1 ] || bad="$bad [현재 v5.7]"
  first=$(awk '/^변경 이력:/{f=1; next} f && /^- \*\*/{print; exit}' "$T/S.md")
  case "$first" in '- **v5.7 (2026-'*) ;; *) bad="$bad [변경 이력 첫 항목: ${first:0:30}]";; esac
  [ "$(grep -cE '^- \*\*v5\.7 \(2026-' "$T/S.md")" = 1 ] || bad="$bad [v5.7 항목 수]"
  [ "$(grep -cE '^- \*\*v5\.6 \(2026-09-26\)\*\*' "$T/S.md")" = 1 ] || bad="$bad [v5.6 항목 수]"
  [ -z "$bad" ] && pass "AR-03 머리 v5.7 · 이전 v5.6 · 현재 v5.7 · 변경 이력 첫 항목 v5.7 · v5.6 항목 1" || fail "AR-03$bad"
}
c_AR04() {  # 넘김 기록
  N=.harness/.meta/after-kaizen-0926b/cs-notes.md
  git -C "$R" show "$U:$N" > "$T/notes" 2>/dev/null || { fail "AR-04 $N 가 상한 판에 없음"; return; }
  miss=""
  for w in 'harness/docs/guides/qa-evaluation-guide.md:1210' 'harness/skills/sprint-contract/SKILL.md:471' 'docs/harness/contract-schema.html' 'CS-12' \
           'harness/docs/guides/contract-design-guide.md:1311' 'docs/index.html:239' \
           'harness/docs/guides/qa-evaluation-guide.md:12' 'harness/docs/guides/qa-evaluation-guide.md:15' 'harness/docs/guides/qa-evaluation-guide.md:22' \
           'harness/docs/guides/qa-evaluation-guide.md:1968' 'harness/docs/guides/qa-evaluation-guide.md:2038' 'harness/docs/guides/qa-evaluation-guide.md:2047'; do
    grep -F -- "$w" "$T/notes" | grep -qE -- "$(printf '%s' "$w" | sed 's/[.]/[.]/g')([^0-9]|\$)" || miss="$miss [$w]"
  done
  for i in 1 2 3 4 5 6 7 8 9 10 11; do grep -qE "CS-${i}([^0-9]|\$)" "$T/notes" || miss="$miss [CS-$i]"; done
  [ -z "$miss" ] && pass "AR-04 넘김 경로:줄 열하나 · CS-12 · CS-1~CS-11 모두" || fail "AR-04 빠짐:$miss"
}
c_RE01() {  # 새 도우미 정의는 계약 형식 문서에만
  n=$(git -C "$R" diff -U0 --no-color "$B" "$U" -- "$SK" "$FB" | grep '^+' | grep -v '^+++' | grep -cE '^\+[[:space:]]*[A-Za-z_][A-Za-z0-9_]*\(\)[[:space:]]*\{')
  [ "$n" = 0 ] && pass "RE-01 SKILL.md · 피드백 형식 파일 더한 줄의 함수 정의 0" || fail "RE-01 함수 정의 $n 줄"
}
c_RE02() {  # 도우미 이름마다 정의 한 번
  bad=""
  for n in resolve_contract_root list_contracts fm_get sha256_16 contract_digest verify_seal measurement_digest verify_measurement sprint_head mine unsigned_on amend_direction amend_direction_oracle with_two line_of dirty_except_status; do
    c=$(grep -cE "^[[:space:]]*${n}\(\)[[:space:]]*\{" "$T/S.md"); [ "$c" = 1 ] || bad="$bad ${n}=$c"
  done
  [ -z "$bad" ] && pass "RE-02 16 이름 모두 정의 1 번" || fail "RE-02$bad"
}
c_AP03() {  # 더한 줄의 여는 울타리에 언어 표시
  bad=0
  for f in "$S" "$SK"; do
    git -C "$R" show "$U:$f" > "$T/f.md"
    $H added "$R" "$B" "$U" "$f" | cut -f1 > "$T/f.add"
    awk 'NR==FNR{a[$1]=1; next} /^[[:space:]]*(```|~~~)/{ if(!o){o=1; if((FNR in a) && $0 ~ /^[[:space:]]*(```|~~~)[[:space:]]*$/) print FILENAME":"FNR} else o=0 }' "$T/f.add" "$T/f.md" > "$T/bare"
    bad=$((bad + $(grep -c . "$T/bare")))
  done
  [ "$bad" = 0 ] && pass "AP-03 더한 여는 울타리의 언어 표시 빠짐 0" || fail "AP-03 $bad 곳"
}
c_AP04() {  # SKILL.md frontmatter name 과 검증 도구 V1
  git -C "$R" show "$U:$SK" | awk 'NR==1&&/^---$/{f=1;next} f&&/^---$/{exit} f&&/^name:/{n++} END{exit !(n==1)}' || { fail "AP-04 frontmatter name 줄 1 개 아님"; return; }
  pass "AP-04 frontmatter name 1 줄"
}
c_DG02() {  # 편집기 경고 — 더한 줄에 걸린 markdownlint 경고 0 · YAML 읽기
  ML=${ML:-}
  [ -x "$ML" ] || { fail "DG-02 ML(markdownlint-cli2 0.23.2 실행 파일) 경로 없음 — 준비: npm install --no-save markdownlint-cli2@0.23.2"; return; }
  "$ML" --help 2>&1 | head -1 | grep -q 'v0.23.2' || { fail "DG-02 markdownlint-cli2 판이 0.23.2 아님"; return; }
  printf '{ "config": { "MD013": false } }\n' > "$T/cfg.markdownlint-cli2.jsonc"
  tot=0; ran=0
  for f in "$S" "$SK"; do
    mkdir -p "$T/ml/$(dirname "$f")"; git -C "$R" show "$U:$f" > "$T/ml/$f"
    ( cd "$T/ml" && "$ML" --config "$T/cfg.markdownlint-cli2.jsonc" "$f" ) > "$T/ml.out" 2>&1; rc=$?
    grep -q '^Linting: 1 file' "$T/ml.out" && ran=$((ran + 1))
    [ "$rc" -le 1 ] || { fail "DG-02 markdownlint rc=$rc ($f)"; return; }
    $H added "$R" "$B" "$U" "$f" | cut -f1 > "$T/f.add"
    k=$(grep -oE "^$f:[0-9]+" "$T/ml.out" | cut -d: -f2 | grep -cxFf "$T/f.add"); tot=$((tot + k))
    [ "$k" = 0 ] || grep -E "^$f:($(tr '\n' '|' < "$T/f.add" | sed 's/|$//')):" "$T/ml.out" | head -5
  done
  git -C "$R" show "$U:$FB" | python3 -c 'import sys,yaml; d=yaml.safe_load(sys.stdin); assert d["example"]["schema_version"]==1' 2>"$T/y.err"; yrc=$?
  [ "$ran" = 2 ] && [ "$tot" = 0 ] && [ "$yrc" = 0 ] && pass "DG-02 검사 2 파일 · 더한 줄 경고 0 · YAML 읽기 OK" || fail "DG-02 ran=$ran new_warn=$tot yaml_rc=$yrc"
}
c_DG_NA() {  # DG-01 · DG-03 · DG-04 N/A 사유 측정
  n=$(git -C "$R" diff --name-only "$B" "$U" | grep -c '^scripts/release.sh$')
  x=$(git -C "$R" diff --name-only "$B" "$U" -- . ':(exclude).harness' | grep -vcE '\.(md|yaml)$')
  [ "$n" = 0 ] && [ "$x" = 0 ] && pass "DG-01·03·04 N/A 사유 성립 (release.sh 변경 0 · md/yaml 밖 변경 0)" || fail "DG-N/A release=$n non_doc=$x"
}

all="SK01 SK02 SK03 SK04 SK05 SK06 SK07 SK08 SK09 SK10 SK11 SK12 SK13 SK14 SC01 SC02 SC03 ER01 AR01 AR02 AR03 AR04 RE01 RE02 AP03 AP04 DG02 DG_NA"
sel=${1:-all}; [ "$sel" = all ] && sel=$all
echo "B=$B U=$U"
for id in $sel; do id=${id//-/}; "c_$id"; done
[ "$fails" = 0 ] && exit 0 || exit 1
