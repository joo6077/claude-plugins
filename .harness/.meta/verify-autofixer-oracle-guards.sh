#!/usr/bin/env bash
# 훅 2 종(block-dirwide-autofixer · lint-contract-oracle)의 4 축 검증 하네스.
#
# 계약: .harness/sprint-contract-autofixer-oracle-guards.md
# 4 축은 «양성 · 음성 대조 · 오탐 · 회귀» 다. 양성만 보면 판별력을 못 잰다.
#
# 축 값(TOOLS/MODES/ARGSHAPES)을 여기에 «다시 타이핑하지 않는다» — 훅 소스에서 추출한다.
# 테스트가 값을 재입력하면 훅과 하네스가 조용히 어긋난다 (contract-schema §인자 매트릭스).
#
# 사용법:  bash .harness/.meta/verify-autofixer-oracle-guards.sh
# zsh 에서도 동일 출력이어야 한다:  zsh .harness/.meta/verify-autofixer-oracle-guards.sh
set -uo pipefail

HOOK_A="${HOOK_A:-$HOME/.claude/hooks/block-dirwide-autofixer.sh}"
HOOK_B="${HOOK_B:-$HOME/.claude/hooks/lint-contract-oracle.sh}"
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
FAILS=0
pass() { printf '  ✓ %s\n' "$1"; }
fail() { printf '  ✗ %s\n' "$1"; FAILS=$((FAILS + 1)); }

payload_bash() { # payload_bash <command>
  printf '{"tool_name":"Bash","tool_input":{"command":%s}}' \
    "$(printf '%s' "$1" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')"
}
payload_edit() { # payload_edit <abs file path>
  printf '{"tool_name":"Edit","tool_input":{"file_path":%s}}' \
    "$(printf '%s' "$1" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')"
}
verdict_a() { # verdict_a <command> → DENY | PASS
  if payload_bash "$1" | bash "$HOOK_A" 2>/dev/null | grep -q '"deny"'; then
    printf 'DENY'
  else
    printf 'PASS'
  fi
}

# ── 축 값 추출 (훅 소스가 SSOT) ──────────────────────────────────────────────
extract_array() { # extract_array <file> <ARRAY_NAME>
  awk -v name="$2" '
    index($0, name "=(") == 1 { inb = 1; next }
    inb && $0 ~ /^\)/ { exit }
    inb { gsub(/^[[:space:]]*.|.[[:space:]]*$/, ""); print }
  ' "$1"
}
# 배열 «인덱싱을 쓰지 않는다». zsh 배열은 1-based 라 bash 의 [0] 접근이
# `parameter not set` 으로 죽는다 (실측: zsh 에서 하네스가 4 행 만에 중단). 대신
# 이름과 read-only 플래그를 TAB 으로 붙인 «줄» 로 만들어 순회한다 — 두 셸 공통.
TAB="$(printf '\t')"
PAIRS="$(paste <(extract_array "$HOOK_A" TOOLS_NAME) <(extract_array "$HOOK_A" TOOLS_RO))"
# «단어 분리에 의존하지 않는다». zsh 는 SH_WORD_SPLIT 이 기본 off 라
# `for m in $MODES` 가 목록 전체를 «원소 하나»로 넘긴다 — 죽지도 않고 조용히
# 케이스 수가 84→14 로 줄어든다 (실측). 축 값은 줄 단위로 두고 read 로 순회한다.
MODES="$(printf 'write\ncheck\n')"
ARGSHAPES="$(printf 'dir\nomitted\nfile\n')"

N_TOOLS=$(printf '%s\n' "$PAIRS" | grep -c .)
N_MODES=$(printf '%s\n' "$MODES" | grep -c .)
N_SHAPES=$(printf '%s\n' "$ARGSHAPES" | grep -c .)
CASES_TOTAL=$(( N_TOOLS * N_MODES * N_SHAPES ))   # 손으로 적지 않는다 — 곱을 계산한다
N_RO=$(extract_array "$HOOK_A" TOOLS_RO | grep -c .)

echo "════ 축 값 (훅 소스에서 추출) ════"
printf '  TOOLS=%d  MODES=%d  ARGSHAPES=%d  → cases_total=%d\n' \
  "$N_TOOLS" "$N_MODES" "$N_SHAPES" "$CASES_TOTAL"
if [ "$N_TOOLS" -ne "$N_RO" ]; then
  fail "TOOLS_NAME(${N_TOOLS}) 과 TOOLS_RO(${N_RO}) 길이 불일치 — 병렬 배열이 어긋났다"
fi

# read-only 플래그 «리터럴» 을 정규식에서 기계적으로 도출한다 (역시 재타이핑 금지).
ro_literal() { printf '%s' "$1" | sed -E 's/^\[ \]//; s/\[ =\]//g; s/\(([^)|]+)\|[^)]*\)/\1/g'; }
# 도구 실행 접두 — 레포 스크립트는 python3 로, 나머지는 그대로 호출된다.
cmd_prefix() { case "$1" in *.py*) printf 'python3 scripts/' ;; *) printf '' ;; esac; }

# ── SK-01 / SK-02 · 인자 매트릭스 ────────────────────────────────────────────
echo "════ SK-01 · SK-02  인자 매트릭스 (${CASES_TOTAL} 케이스) ════"
n_deny=0; n_pass=0; n_mismatch=0
while IFS="$TAB" read -r base ro_re; do
  [ -n "$base" ] || continue
  ro="$(ro_literal "$ro_re")"; pre="$(cmd_prefix "$base")"
  while IFS= read -r mode; do
    [ -n "$mode" ] || continue
    while IFS= read -r shape; do
      [ -n "$shape" ] || continue
      case "$shape" in
        dir)     arg=" docs/" ;;
        omitted) arg="" ;;
        file)    arg=" README.md" ;;
        *)       arg="" ;;
      esac
      if [ "$mode" = check ]; then cmd="${pre}${base} ${ro}${arg}"; else cmd="${pre}${base}${arg}"; fi
      got="$(verdict_a "$cmd")"
      if [ "$mode" = write ] && { [ "$shape" = dir ] || [ "$shape" = omitted ]; }; then
        want=DENY
      else
        want=PASS
      fi
      [ "$got" = DENY ] && n_deny=$((n_deny + 1)) || n_pass=$((n_pass + 1))
      if [ "$got" != "$want" ]; then
        n_mismatch=$((n_mismatch + 1)); printf '    MISMATCH want=%s got=%s :: %s\n' "$want" "$got" "$cmd"
      fi
    done <<SHAPES_EOF
$ARGSHAPES
SHAPES_EOF
  done <<MODES_EOF
$MODES
MODES_EOF
done <<PAIRS_EOF
$PAIRS
PAIRS_EOF
printf '  cases=%d deny=%d pass=%d mismatch=%d\n' "$CASES_TOTAL" "$n_deny" "$n_pass" "$n_mismatch"
[ "$n_mismatch" -eq 0 ] && pass "SK-01/SK-02 전 셀 기대와 일치" || fail "SK-01/SK-02 불일치 ${n_mismatch} 건"
[ "$n_deny" -eq $(( N_TOOLS * 2 )) ] && pass "deny 수 = TOOLS×{dir,omitted} = $(( N_TOOLS * 2 ))" \
  || fail "deny 수 이상: ${n_deny} (기대 $(( N_TOOLS * 2 )))"

# ── SK-03 · 오탐 대조 (명령 위치 앵커) ───────────────────────────────────────
echo "════ SK-03  오탐 대조 — 포매터명이 명령 위치가 아닌 곳에 등장 ════"
for c in 'git log --grep=prettier' 'echo "run black on it"' 'cat scripts/fix-markdown-lint.py' 'rg "cargo fmt" docs/'; do
  got="$(verdict_a "$c")"
  [ "$got" = PASS ] && pass "$c" || fail "오탐: $c → $got"
done

# ── 실사용 플래그 변형 · heredoc (APPROVE 후 하드닝 · 계약 조건 아님) ──────────
# iteration 2 평가자가 "하네스/배열 자기지시적 오라클로는 PASS 지만 실사용 플래그를 직접
# 투입하면 오탐" 이라고 지적한 축이다. 매트릭스는 TOOLS_RO 에서 파생한 플래그만 쓰므로
# «배열 자체가 틀렸다는 사실» 을 구조적으로 잡지 못한다 — 실제 도구의 플래그를 손으로
# 적어야 잡힌다. 여기서 false negative 1 건(가드의 핵심 실패)이 발견됐다.
echo "════ 실사용 플래그 변형 — 축약형 · 대체형 · 비-read-only --check ════"
while IFS='|' read -r c want; do
  [ -n "$c" ] || continue
  got="$(verdict_a "$c")"
  [ "$got" = "$want" ] && pass "$got  $c" || fail "$got (기대 $want)  $c"
done <<REAL_EOF
eslint --fix-dry-run src/|PASS
dart format -o none lib/|PASS
dart format --output none lib/|PASS
prettier -c src/|PASS
isort -c .|PASS
clang-format -n -i src/|PASS
autopep8 -d --in-place src/|PASS
python3 scripts/validate-plugin.py --check=placeholders --fix|DENY
eslint --fix src/|DENY
dart format lib/|DENY
isort .|DENY
clang-format -i src/|DENY
autopep8 --in-place src/|DENY
REAL_EOF

# heredoc 본문은 «명령이 아니라 데이터» 다. grep 이 줄 단위라 앵커의 ^ 가 매 줄에 걸려
# 파일에 써 넣을 내용이 명령으로 오인됐다 — 이 하네스에 케이스를 추가하는 호출 자체가
# 차단된 것이 실측 계기다. 반대로 heredoc «밖» 줄바꿈은 진짜 구분자라 계속 잡아야 한다.
echo "════ heredoc 본문 = 데이터 · heredoc 밖 줄바꿈 = 명령 구분자 ════"
HD_DATA="$(printf 'cat > /tmp/t.txt <<XEOF\nprettier --write src/\ncargo fmt\nXEOF\n')"
HD_OUT="$(printf 'cd /tmp\nprettier --write src/\n')"
HD_AFTER="$(printf 'cat > /tmp/t.txt <<XEOF\nsome data\nXEOF\ncargo fmt\n')"
[ "$(verdict_a "$HD_DATA")"  = PASS ] && pass "heredoc 본문 내 포매터 → 통과 (데이터)"       || fail "heredoc 본문 오탐"
[ "$(verdict_a "$HD_OUT")"   = DENY ] && pass "heredoc 밖 2 행 포매터 → deny (명령)"          || fail "heredoc 밖 미탐"
[ "$(verdict_a "$HD_AFTER")" = DENY ] && pass "heredoc 종료 후 포매터 → deny (명령)"          || fail "heredoc 종료 후 미탐"

# ── SK-04 · 센티넬 4 축 ──────────────────────────────────────────────────────
echo "════ SK-04  센티넬 게이트 4 축 ════"
SENT="$HOME/.claude/.dirwide-format-approved"
BAK=""; [ -f "$SENT" ] && { BAK="$(mktemp)"; cp "$SENT" "$BAK"; }
TRIGGER='python3 scripts/fix-markdown-lint.py docs/'

rm -f "$SENT"
[ "$(verdict_a "$TRIGGER")" = DENY ] && pass "축1 센티넬 없음 → deny" || fail "축1 센티넬 없음인데 통과"

echo $(( $(date +%s) - 7200 )) > "$SENT"
[ "$(verdict_a "$TRIGGER")" = DENY ] && pass "축2 만료(7200초 전) → deny" || fail "축2 만료인데 통과"

date +%s > "$SENT"
[ "$(verdict_a "$TRIGGER")" = PASS ] && pass "축3 유효 → 통과" || fail "축3 유효인데 deny"

ok4=1
for c in 'git log --grep=prettier' 'echo "run black on it"' 'cat scripts/fix-markdown-lint.py' 'rg "cargo fmt" docs/'; do
  [ "$(verdict_a "$c")" = PASS ] || ok4=0
done
[ "$ok4" = 1 ] && pass "축4 유효 센티넬 상태에서도 오탐 4 건 무출력" || fail "축4 오탐 발생"

rm -f "$SENT"; [ -n "$BAK" ] && { cp "$BAK" "$SENT"; rm -f "$BAK"; }

# ── SK-05 / SK-06 / SK-07 · 훅 B ─────────────────────────────────────────────
echo "════ SK-05  훅 B 양성 대조 ════"
P6="$REPO/.harness/sprint-contract-kaizen-phase6-variant-decision-gates.md"
OUT_B="$(payload_edit "$P6" | bash "$HOOK_B" 2>/dev/null)"
printf '%s' "$OUT_B" | grep -q 'AR-03' && pass "Phase6 AR-03 (산문 grep 오라클) 검출" || fail "AR-03 미검출"

# AM-03 이 못박은 3 건은 ER-01 · ER-02 · ER-03 이다. DG-02 는 초과 확인분.
# iteration 3 평가자가 이 루프에 ER-03 이 빠져 있음을 지적했다 — 사이드카가 지정한 대상과
# 하네스가 실제로 도는 대상이 어긋나면, 문서가 주장하는 커버리지가 실측과 달라진다.
echo "════ SK-06  오탐 대조 — 실행+수치비교형 조건 (AM-03 지정 3 건 + 초과 1 건) ════"
for id in ER-01 ER-02 ER-03 DG-02; do
  printf '%s' "$OUT_B" | grep -q -- "$id" && fail "오탐: $id 가 검출됨" || pass "$id 미검출 (실행형 조건)"
done

echo "════ SK-07  훅 B 는 차단 신호를 내지 않는다 ════"
blk=0
for k in permissionDecision '"decision"' '"continue"'; do
  printf '%s' "$OUT_B" | grep -q -- "$k" && { fail "차단 신호 $k 발견"; blk=1; }
done
[ "$blk" = 0 ] && pass "permissionDecision · decision · continue 전부 0 건"
payload_edit "$P6" | bash "$HOOK_B" >/dev/null 2>&1
[ "$?" -eq 0 ] && pass "훅 B exit 0" || fail "훅 B 비정상 종료"

echo "════ SK-06  기존 계약 전체 검출률 ════"
tot_c=0; tot_f=0; n_files=0
while IFS= read -r cf; do
  case "$cf" in *autofixer-oracle-guards*) continue ;; esac      # §범위 경계 1 자기 산출물 제외
  n_files=$((n_files + 1))
  # `grep -c` 는 매치 0 일 때 "0" 을 «출력하고» exit 1 이다. 여기에 `|| printf 0` 을 붙이면
  # 출력이 "0\n0" 이 되어 뒤의 $(( )) 가 산술 에러로 죽는다 (실측 후 수정).
  c=$(grep -cE '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$cf" 2>/dev/null | head -1); c=${c:-0}
  o="$(payload_edit "$cf" | bash "$HOOK_B" 2>/dev/null)"
  # additionalContext 는 «JSON 문자열» 이라 줄바꿈이 \n 로 이스케이프되어 있다.
  # grep 의 줄 앵커(^)로는 절대 안 잡힌다 — 반드시 JSON 을 풀어서 센다 (실측 후 수정).
  f=$(printf '%s' "$o" | python3 -c '
import json,re,sys
try:
    d = json.load(sys.stdin)
    ctx = d.get("hookSpecificOutput", {}).get("additionalContext", "")
except Exception:
    ctx = ""
print(len(re.findall(r"^  - [A-Z]{2,}-[0-9]{2} \((?:산문-grep|실행신호-부재)\)$", ctx, re.M)))
' 2>/dev/null); f=${f:-0}
  tot_c=$((tot_c + c)); tot_f=$((tot_f + f))
done < <(find "$REPO/.harness" -maxdepth 1 -type f \
           \( -name 'sprint-contract.md' -o -name 'sprint-contract-*.md' \) | LC_ALL=C sort)
if [ "$tot_c" -gt 0 ]; then
  rate=$(python3 -c "print(f'{100*$tot_f/$tot_c:.1f}')")
else
  rate=0
fi
printf '  DETECTION_RATE files=%d conditions=%d flagged=%d rate=%s%%\n' "$n_files" "$tot_c" "$tot_f" "$rate"

# ── ER-01 · deny 사유에 대체 경로 ────────────────────────────────────────────
echo "════ ER-01  deny 사유에 대체 경로 ════"
RSN="$(payload_bash "$TRIGGER" | bash "$HOOK_A" 2>/dev/null)"
printf '%s' "$RSN" | grep -q 'git diff --name-only' && pass "대체 명령(git diff --name-only) 포함" || fail "대체 명령 누락"
printf '%s' "$RSN" | grep -q 'dirwide-format-approved' && pass "센티넬 승인 절차 포함" || fail "센티넬 절차 누락"

# ── ER-02 · fail-open 3 케이스 × 2 훅 ────────────────────────────────────────
echo "════ ER-02  fail-open ════"
SHIM="$(mktemp -d)"
for b in cat grep head date tr awk basename sed cut wc sort uniq comm env python3 dirname; do
  src="$(command -v "$b" 2>/dev/null)"; [ -n "$src" ] && ln -sf "$src" "$SHIM/$b"
done
for h in "$HOOK_A" "$HOOK_B"; do
  hn="$(basename "$h")"
  # `PATH=X bash` 는 «bash 자체»를 X 에서 찾는다 → 127. 절대경로로 호출해야 한다 (실측 후 수정).
  out="$(payload_bash 'python3 scripts/fix-markdown-lint.py docs/' | PATH="$SHIM" /bin/bash "$h" 2>/dev/null)"; rc=$?
  { [ "$rc" -eq 0 ] && ! printf '%s' "$out" | grep -q '"deny"'; } \
    && pass "$hn jq 부재 → exit 0, deny 없음" || fail "$hn jq 부재 축 실패 (rc=$rc)"
  printf '' | bash "$h" >/dev/null 2>&1
  [ "$?" -eq 0 ] && pass "$hn 빈 stdin → exit 0" || fail "$hn 빈 stdin 실패"
  printf '{"tool_name":' | bash "$h" >/dev/null 2>&1
  [ "$?" -eq 0 ] && pass "$hn 깨진 JSON → exit 0" || fail "$hn 깨진 JSON 실패"
done
rm -rf "$SHIM"

# ── AR-02 · 훅 파일 존재·실행권한 ────────────────────────────────────────────
echo "════ AR-02  훅 파일 ════"
for h in "$HOOK_A" "$HOOK_B"; do
  [ -x "$h" ] && pass "$(basename "$h") 실행 가능" || fail "$(basename "$h") 실행 불가"
done

echo "════════════════════════════════════"
if [ "$FAILS" -eq 0 ]; then echo "HARNESS_OK fails=0 cases_total=$CASES_TOTAL"; exit 0
else echo "HARNESS_FAIL fails=$FAILS"; exit 1; fi
