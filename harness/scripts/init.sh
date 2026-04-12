#!/usr/bin/env bash
# ── harness init ──
# 새 프로젝트에 .harness/ 디렉토리를 생성한다.
# Usage: bash harness/scripts/init.sh [target_dir] [stack]
#   target_dir: .harness/를 생성할 프로젝트 디렉토리 (기본: .)
#   stack:      프로젝트 스택 (flutter, rust, react 등. 기본: generic)

set -eo pipefail

HARNESS_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET_DIR="${1:-.}"
STACK="${2:-generic}"

TARGET_DIR="$(cd "$TARGET_DIR" 2>/dev/null && pwd)" || { echo "❌ 디렉토리 없음: $1"; exit 1; }
HARNESS_DIR="$TARGET_DIR/.harness"

if [ -d "$HARNESS_DIR" ]; then
  echo "⚠️ $HARNESS_DIR 이미 존재합니다. 덮어쓰려면 삭제 후 재실행하세요."
  exit 1
fi

echo "=== Harness Init ==="
echo "Target: $TARGET_DIR"
echo "Stack:  $STACK"
echo ""

# 1. 디렉토리 생성
mkdir -p "$HARNESS_DIR/procedures" "$HARNESS_DIR/history"

# 2. project.yaml 복사 + stack 치환
cp "$HARNESS_ROOT/templates/project.yaml" "$HARNESS_DIR/project.yaml"
# macOS sed -i requires '' suffix, Linux does not — use temp file for cross-platform
TMPFILE="$(mktemp)"
sed "s/^stack: \"\"/stack: \"$STACK\"/" "$HARNESS_DIR/project.yaml" > "$TMPFILE"
mv "$TMPFILE" "$HARNESS_DIR/project.yaml"

# 3. env.sh 복사
cp "$HARNESS_ROOT/templates/env.sh" "$HARNESS_DIR/env.sh"

# 4. procedures 템플릿 복사
cp "$HARNESS_ROOT/templates/procedures/_TEMPLATE.md" "$HARNESS_DIR/procedures/_TEMPLATE.md"

# 5. 기본 카테고리별 procedures 생성 (빈 템플릿)
for cat in ui logic error architecture; do
  PROC_FILE="$HARNESS_DIR/procedures/${cat}-verification.md"
  if [ ! -f "$PROC_FILE" ]; then
    CAT_UPPER=$(echo "$cat" | tr '[:lower:]' '[:upper:]')
    cat > "$PROC_FILE" << EOF
# ${CAT_UPPER} 조건 검증 절차 (${STACK})

## 검증 방법
1. Glob으로 관련 파일 검색
2. Read로 파일 내용 확인
3. 조건에 명시된 요소가 코드에 존재하는지 확인

## 정적 검증 최소 증거
| 조건 유형 | PASS 가능한 최소 증거 |
|-----------|----------------------|
| (프로젝트에 맞게 작성) | (증거 설명) |
EOF
  fi
done

# 6. 스킬/에이전트 디렉토리 생성 + 복사
CLAUDE_DIR="$TARGET_DIR/.claude"
mkdir -p "$CLAUDE_DIR/skills/sprint-contract" "$CLAUDE_DIR/agents"

if [ -f "$HARNESS_ROOT/skills/sprint-contract/SKILL.md" ]; then
  cp "$HARNESS_ROOT/skills/sprint-contract/SKILL.md" "$CLAUDE_DIR/skills/sprint-contract/SKILL.md"
fi
if [ -f "$HARNESS_ROOT/agents/qa-evaluator.md" ]; then
  cp "$HARNESS_ROOT/agents/qa-evaluator.md" "$CLAUDE_DIR/agents/qa-evaluator.md"
fi

echo "✅ 생성 완료:"
echo "  $HARNESS_DIR/project.yaml"
echo "  $HARNESS_DIR/env.sh"
echo "  $HARNESS_DIR/procedures/ (4개 카테고리)"
echo "  $CLAUDE_DIR/skills/sprint-contract/SKILL.md"
echo "  $CLAUDE_DIR/agents/qa-evaluator.md"
echo ""
echo "다음 단계:"
echo "  1. $HARNESS_DIR/project.yaml — commands, anti_patterns, trigger 설정"
echo "  2. $HARNESS_DIR/env.sh — SDK, 필수 파일, run 가드 설정"
echo "  3. $HARNESS_DIR/procedures/ — 카테고리별 검증 절차 작성"
echo ""
echo "검증: bash harness/scripts/validate.sh"
