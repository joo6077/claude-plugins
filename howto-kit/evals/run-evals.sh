#!/bin/sh
# run-evals.sh — evals.json 의 케이스를 zsh · bash 양쪽에서 실행해 대조한다.
# 사용: sh howto-kit/evals/run-evals.sh   (bash · zsh 로 실행해도 같다)
#
# 오라클은 **실행 결과**다. 서술 존재로 통과시키지 않는다.
# 두 셸의 출력이 다르면 그 자체가 FAIL 이다 — 셸 이식성 결함은 한쪽에서만 조용히 통과한다.
# 실측 2026-09-08: `set -- $var` 가 zsh 에서 단어분할되지 않아 G5·G6 위반이 zsh 에서만
# GATE_PASS 로 샜다. 한쪽 셸만 돌렸으면 못 잡았을 결함이다.

KIT_DIR=$(cd "$(dirname "$0")/.." && pwd)
EVALS="$KIT_DIR/evals/evals.json"
GATE="$KIT_DIR/scripts/howto-gate.sh"

[ -f "$EVALS" ] || { echo "EVALS_MISSING $EVALS"; exit 2; }
[ -f "$GATE" ]  || { echo "GATE_MISSING $GATE"; exit 2; }
command -v zsh  >/dev/null 2>&1 || { echo "SHELL_MISSING zsh — 양쪽 셸 대조가 불가하다"; exit 2; }
command -v bash >/dev/null 2>&1 || { echo "SHELL_MISSING bash"; exit 2; }

TSV=$(mktemp); RESULT=$(mktemp)
trap 'rm -f "$TSV" "$RESULT"' EXIT INT TERM

python3 - "$EVALS" > "$TSV" <<'PY'
import json, sys
with open(sys.argv[1], encoding='utf-8') as f:
    data = json.load(f)
for c in data['cases']:
    print('\t'.join([c['id'], c['fixture'], c['expect_final'], '|'.join(c['assertions'])]))
PY

while IFS='	' read -r id fixture expect asserts; do
  [ -n "$id" ] || continue

  if [ "${fixture#__NONEXISTENT__}" != "$fixture" ]; then
    target="/__howto_kit_nonexistent__/x.md"
  else
    target="$KIT_DIR/evals/$fixture"
  fi

  out_zsh=$(zsh  -c ". '$GATE'; howto_gate '$target'" 2>&1)
  out_bash=$(bash -c ". '$GATE'; howto_gate '$target'" 2>&1)

  problems=""
  [ "$out_zsh" = "$out_bash" ] || problems="$problems shell_mismatch"
  printf '%s\n' "$out_bash" | grep -q "^$expect" || problems="$problems final_expected=$expect"

  missing=""
  # 파이프 구분 assertion 을 개행으로 바꿔 순회한다 (글로빙·배열 없이)
  for_each=$(printf '%s\n' "$asserts" | tr '|' '\n')
  OLD_IFS=$IFS; IFS='
'
  for a in $for_each; do
    [ -n "$a" ] || continue
    printf '%s\n' "$out_bash" | grep -qF "$a" || missing="$missing
    MISSING_ASSERT: $a"
  done
  IFS=$OLD_IFS

  [ -z "$missing" ] || problems="$problems missing_assert"

  if [ -z "$problems" ]; then
    echo "PASS  $id"
    echo 1 >> "$RESULT"
  else
    echo "FAIL  $id —$problems"
    [ -z "$missing" ] || printf '%s\n' "$missing"
    echo "  --- bash 출력 ---"; printf '%s\n' "$out_bash" | sed 's/^/  /'
    if [ "$out_zsh" != "$out_bash" ]; then
      echo "  --- zsh 출력 (다름) ---"; printf '%s\n' "$out_zsh" | sed 's/^/  /'
    fi
    echo 0 >> "$RESULT"
  fi
done < "$TSV"

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
