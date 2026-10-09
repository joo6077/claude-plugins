#!/usr/bin/env bash
# 도우미 떼는 스크립트(extract-helpers.py)와 공용 측정 파일(measure-common.sh)을 손으로 답을 아는 입력에 돌린다.
# 계약 after-0926-harness-scripts 의 SC-10 · SC-11 · ER-01 을 따른다.
# MEASURE_EXTRACT · MEASURE_COMMON 으로 대상 파일을 바꿀 수 있다 — 결함을 심은 사본으로 음성 대조를 돌릴 때 쓴다.
# zsh 가 없으면 절반을 못 재므로 2 로 끝낸다.

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
root=$(cd "$here/../../.." && pwd)
extract=${MEASURE_EXTRACT:-$root/harness/scripts/extract-helpers.py}
common=${MEASURE_COMMON:-$root/harness/scripts/measure-common.sh}
schema=$root/harness/references/contract-schema.md
command -v zsh >/dev/null 2>&1 || { echo "zsh 가 없어 zsh 쪽 확인을 못 한다" >&2; exit 2; }
[ -f "$extract" ] && [ -f "$common" ] && [ -f "$schema" ] || { echo "대상 파일이 없다: $extract · $common · $schema" >&2; exit 2; }
# 대상을 바꾼 사본은 제 위치에서 규약 문서를 못 찾으므로 규약 경로를 넘긴다. 바꾸지 않았으면 기본 경로 찾기를 그대로 잰다
schema_env=""
[ -n "${MEASURE_COMMON:-}" ] && schema_env=$schema

export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@example.com GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@example.com
work=$(mktemp -d "${TMPDIR:-/tmp}/measure-test.XXXXXX") || exit 2
work=$(cd "$work" && pwd -P)
trap 'rm -rf "$work"' EXIT
fails=0

check() {  # check <번호> <기대> <실제>
  if [ "$2" = "$3" ]; then echo "PASS $1 $3"; else echo "FAIL $1 기대 $2 / 실제 $3"; fails=$((fails + 1)); fi
}
fence() { printf '```%s\n' "$1"; }
names() { find "$1" -type f 2>/dev/null | sed 's#.*/##' | LC_ALL=C sort | tr '\n' ',' | sed 's/,$//'; }

# 봉인 판: 이름 붙은 bash · python 블록 둘, 이름 없는 bash 블록 하나, text 블록 안의 이름 하나(떼지 않는다).
# 봉인 뒤 커밋에 c.sh 블록, 작업 폴더에만 조건 한 줄을 더한다
repo=$work/repo
mkdir -p "$repo/.harness" && git -C "$repo" init -q -b main || exit 2
{ printf -- '---\nstatus: active\n---\n\n## Script\n\n- [ ] SC-01: x\n\n'
  fence bash; printf '#!/usr/bin/env bash\n# a.sh <x> — 첫째\necho a\n'; fence ''
  fence python; printf '# b.py — 둘째\nprint("b")\n'; fence ''
  fence bash; printf '# 이름 없는 설명 블록\necho none\n'; fence ''
  fence text; printf '# z.sh — text 블록은 떼지 않는다\n'; fence ''
} >"$repo/.harness/c.md"
# 봉인 값은 시험이 규약 블록을 따로 떼어 계산한다 — 대상 파일의 정의로 계산하면 대상이 틀려도 맞아 보인다
awk '/^```bash$/ { f = 1; buf = ""; next } f && /^```$/ { if (buf ~ /(fm_get|sha256_16|sprint_head|mine)\(\) \{/) printf "%s", buf; f = 0; next } f { buf = buf $0 "\n" }' "$schema" >"$work/schema.sh"
digest=$(bash -c '. "$1"; contract_digest "$2"' _ "$work/schema.sh" "$repo/.harness/c.md") || exit 2
awk -v d="$digest" '{ print } $0 == "status: active" && !done { print "conditions_digest: sha256:" d; done = 1 }' "$repo/.harness/c.md" >"$work/c.tmp" && mv "$work/c.tmp" "$repo/.harness/c.md"
git -C "$repo" add -A && git -C "$repo" commit -qm seal || exit 2
{ printf '\n'; fence bash; printf '# c.sh — 봉인 뒤에 붙은 블록\necho c\n'; fence ''; } >>"$repo/.harness/c.md"
git -C "$repo" commit -qam later || exit 2
printf '%s\n' "- [ ] SC-02: y" >>"$repo/.harness/c.md"
{ fence bash; printf '# d.sh — 하나\n'; fence ''; fence bash; printf '# d.sh — 같은 이름\n'; fence ''; } >"$work/dup.md"
{ printf '# 도우미 없음\n\n'; fence text; printf 'x\n'; fence ''; } >"$work/none.md"
echo untracked >"$repo/.harness/new.md"

# ── 떼는 스크립트 ──
python3 "$extract" --sealed "$repo/.harness/c.md" "$work/o1" >"$work/o1.log" 2>&1; rc=$?
check E1-봉인판 "rc=0 names=a.sh,b.py" "rc=$rc names=$(names "$work/o1")"
python3 "$extract" "$repo/.harness/c.md" "$work/o2" >"$work/o2.log" 2>&1; rc=$?
check E2-작업판 "rc=0 names=a.sh,b.py,c.sh" "rc=$rc names=$(names "$work/o2")"
awk '/^```bash$/ { f = 1; b = ""; next } f && /^```$/ { if (b ~ /\n# a\.sh /) { printf "%s", b; exit } f = 0; next } f { b = b $0 "\n" }' "$repo/.harness/c.md" >"$work/a.want"
if cmp -s "$work/a.want" "$work/o1/a.sh"; then same=1; else same=0; fi
check E3-같은바이트 "same_bytes=1" "same_bytes=$same"
python3 "$extract" "$work/dup.md" "$work/o4" >"$work/o4.log" 2>&1; rc=$?
check E4-같은이름 "rc=1 files=0 named=1" "rc=$rc files=$(find "$work/o4" -type f 2>/dev/null | grep -c .) named=$(grep -c 'd.sh' "$work/o4.log")"
python3 "$extract" "$work/none.md" "$work/o5" >/dev/null 2>&1; rc=$?
check E5-블록없음 "rc=3" "rc=$rc"
python3 "$extract" "$work/missing.md" "$work/o6" >/dev/null 2>&1; rc=$?
check E6-파일없음 "rc=2" "rc=$rc"
python3 "$extract" --sealed "$repo/.harness/new.md" "$work/o7" >/dev/null 2>&1; rc=$?
check E7-추적안됨 "rc=2" "rc=$rc"

# ── 공용 측정 파일 (bash · zsh) ──
for sh in bash zsh; do
  # shellcheck disable=SC2016  # 안쪽 셸이 풀 변수다 — 바깥 셸이 풀면 안 된다
  out=$(cd "$repo" && MEASURE_SCHEMA=$schema_env MC=$common W=$work S=$sh $sh -c '
    [ -n "$MEASURE_SCHEMA" ] || unset MEASURE_SCHEMA
    . "$MC" || { echo "source_rc=$?"; exit 0; }
    miss=""
    for f in fm_get sha256_16 contract_digest verify_seal measurement_digest verify_measurement sprint_head mine unsigned_on unpack_rev scratch_dir sect need_fn; do
      type "$f" >/dev/null 2>&1 || miss="$miss$f,"
    done
    printf "source_rc=0 missing=[%s] seal_now=%s " "${miss%,}" "$(verify_seal .harness/c.md | cut -d" " -f1)"
    d=$(scratch_dir mt) && [ -d "$d" ] && case $d in "${TMPDIR:-/tmp}"/mt.*) printf "scratch=ok " ;; *) printf "scratch=bad " ;; esac
    rm -rf "$d"
    unpack_rev HEAD~1 "$W/u-$S" && [ -f "$W/u-$S/.harness/c.md" ] && printf "unpack=ok seal_sealed=%s " "$(verify_seal "$W/u-$S/.harness/c.md" | cut -d" " -f1)"
    unpack_rev no-such-rev "$W/v-$S" 2>/dev/null; printf "unpack_bad_rc=%s " "$?"
    need_fn verify_seal; printf "need_ok_rc=%s " "$?"
    need_fn no_such_fn 2>/dev/null; printf "need_bad_rc=%s " "$?"
    printf "# t\n\n## A\na\n\n## B\nb1\n\n\`\`\`bash\n## 펜스 안\n\`\`\`\nb2\n\n### B1\nb3\n\n## C\nc\n" >"$W/s-$S.md"
    printf "sect_lines=%s" "$(sect "$W/s-$S.md" "## B" | grep -c .)"
  ' 2>&1)
  check "M-$sh" "source_rc=0 missing=[] seal_now=SEAL_BROKEN scratch=ok unpack=ok seal_sealed=SEAL_OK unpack_bad_rc=2 need_ok_rc=0 need_bad_rc=2 sect_lines=8" "$out"
done

# 규약 함수는 사본이 아니라 규약 블록에서 읽는다 — 정의가 글자까지 같고 대상 파일에 정의 줄이 없다
fns="fm_get sha256_16 contract_digest verify_seal measurement_digest verify_measurement sprint_head mine unsigned_on"
got=$(MEASURE_SCHEMA=$schema bash -c '. "$1" >/dev/null 2>&1 || exit 2; for f in $2; do declare -f "$f"; done' _ "$common" "$fns" | shasum | cut -c1-12)
want=$(bash -c '. "$1"; for f in $2; do declare -f "$f"; done' _ "$work/schema.sh" "$fns" | shasum | cut -c1-12)
if [ "$got" = "$want" ]; then same=1; else same=0; fi
check M3-규약과같음 "same_as_schema=1 copies=0" "same_as_schema=$same copies=$(grep -cE '^[[:space:]]*(fm_get|sha256_16|contract_digest|verify_seal|measurement_digest|verify_measurement|sprint_head|mine|unsigned_on)\(\)' "$common")"

# 규약의 fm_get 은 따옴표와 줄 끝 주석을 벗긴다. 빈칸 없이 붙은 # 는 값이다 (계약 after-0928-harness-checks SC-03)
fm_case() {  # fm_case <번호> <머리 줄> <키> <기대 값>
  printf -- '---\n%s\n---\n\n본문\n' "$2" >"$work/fm-$1.md"
  out=""
  for sh in bash zsh; do
    # shellcheck disable=SC2016  # 안쪽 셸이 풀 변수다
    got=$(MEASURE_SCHEMA=$schema $sh -c '. "$1" >/dev/null 2>&1 || exit 2; fm_get "$2" "$3"' _ "$common" "$work/fm-$1.md" "$3")
    out="$out$sh=[$got] "
  done
  check "F$1-줄끝주석" "bash=[$4] zsh=[$4]" "${out% }"
}
fm_case 1 'status: superseded   # 새 판 있음' status superseded
fm_case 2 'status: "active" # 주석' status active
fm_case 3 'status: active' status active
fm_case 4 'owner_session: abc#def' owner_session 'abc#def'
fm_case 5 'feature: "a # b"' feature 'a # b'
fm_case 6 "$(printf "status: 'done'\t# 탭 앞 주석")" status 'done'
fm_case 7 'status: active #' status active

sed 's/^verify_seal() {/verify_sealx() {/' "$schema" >"$work/broken-schema.md"
MEASURE_SCHEMA="$work/broken-schema.md" bash -c '. "$1"' _ "$common" >"$work/m4.out" 2>&1; rc=$?
check M4-함수빠진규약 "rc=2 names_fn=1" "rc=$rc names_fn=$(grep -c 'verify_seal' "$work/m4.out")"
MEASURE_SCHEMA="$work/no-such-schema.md" bash -c '. "$1"' _ "$common" >/dev/null 2>&1; rc=$?
check M5-규약없음 "rc=2" "rc=$rc"

# 한국어 조건 번호도 규약 함수가 읽는다 (계약 after-0928-korean-condition-ids 스크립트-03).
# 기대 지문은 파이썬 hashlib 로 조건 줄 7 줄 · 번호와 들여쓴 줄 8 줄을 따로 해시한 값이다.
# 옛 규약 정규식은 한국어 번호를 못 읽어 두 지문이 빈 입력의 지문 e3b0c44298fc1c14 가 된다
printf -- '---\nstatus: active\n---\n\n## Skill\n\n- [ ] 스킬-01: a\n  측정: x\n- [ ] 스크립트-02: b\n- [ ] 오류-03: c\n- [ ] 구조-04: d\n- [ ] 재사용-01: e\n- [ ] 진단-01: f\n- [ ] 금지-00: N/A (g)\n' >"$work/korean.md"
for sh in bash zsh; do
  # shellcheck disable=SC2016  # 안쪽 셸이 풀 변수다
  got=$(MEASURE_SCHEMA=$schema_env MC=$common $sh -c '
    [ -n "$MEASURE_SCHEMA" ] || unset MEASURE_SCHEMA
    . "$MC" >/dev/null 2>&1 || exit 2
    printf "%s %s" "$(contract_digest "$1")" "$(measurement_digest "$1")"' _ "$work/korean.md" 2>&1)
  check "K1-한국어번호지문-$sh" "8b52386c713a6054 c51d48673b5caeee" "$got"
done
rx=$(awk '/^contract_digest\(\)/ { getline; print; exit }' "$schema" | sed -E "s/.*grep -E '([^']*)'.*/\1/")
check K2-한국어번호조건수 "conditions=7" "conditions=$(grep -cE "$rx" "$work/korean.md")"

# 우분투 CI 의 GNU grep 은 C.UTF-8 에서 한글 범위식을 오류로 거부한다. 맥 grep 은 받아 주므로 식에 ASCII 밖 글자가 없는지도 본다
# shellcheck disable=SC2016  # 안쪽 셸이 풀 변수다
got=$(LC_ALL=C.UTF-8 MEASURE_SCHEMA=$schema_env MC=$common bash -c '
  [ -n "$MEASURE_SCHEMA" ] || unset MEASURE_SCHEMA
  . "$MC" >/dev/null 2>&1 || exit 2
  printf "%s %s" "$(contract_digest "$1")" "$(measurement_digest "$1")"' _ "$work/korean.md" 2>&1)
n=$(LC_ALL=C.UTF-8 grep -cE "$rx" "$work/korean.md" 2>&1)
wide=$({ awk '/^contract_digest\(\)/ { getline; print; exit }' "$schema"; awk '/^measurement_digest\(\)/ { f = 1 } f && /match\(/ { print; exit }' "$schema"; } | LC_ALL=C grep -c '[^ -~]')
check K3-C.UTF-8한국어번호 "8b52386c713a6054 c51d48673b5caeee conditions=7 non_ascii_lines=0" "$got conditions=$n non_ascii_lines=$wide"

echo "실패 $fails 건"
[ "$fails" = 0 ]
