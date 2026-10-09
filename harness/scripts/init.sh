#!/usr/bin/env bash
# ── harness init ──
# 새 프로젝트에 .harness/ 디렉토리를 생성한다.
# Usage: bash harness/scripts/init.sh [target_dir] [stack]
#   target_dir: .harness/를 생성할 프로젝트 디렉토리 (기본: .)
#   stack:      프로젝트 스택 (flutter, rust, react 등. 기본: generic)
# 환경변수 HARNESS_STORE 에 하네스 저장소(깃) 폴더를 주면 기록을 그 저장소의
# <프로젝트 최상위 폴더 이름>/<최상위에서 대상까지 경로> 에 두고 .harness 는 그 폴더로 가는 바로가기로 만든다.

set -eo pipefail

HARNESS_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET_DIR="${1:-.}"
STACK="${2:-generic}"

TARGET_DIR="$(cd "$TARGET_DIR" 2>/dev/null && pwd -P)" || { echo "❌ 디렉토리 없음: $1"; exit 1; }
HARNESS_DIR="$TARGET_DIR/.harness"

# 깨진 바로가기는 -d 가 거짓이라 -L 도 본다
if [ -d "$HARNESS_DIR" ] || [ -L "$HARNESS_DIR" ]; then
  echo "⚠️ $HARNESS_DIR 이미 존재합니다. 덮어쓰려면 삭제 후 재실행하세요."
  exit 1
fi

STORE_DIR=""
if [ -n "${HARNESS_STORE:-}" ]; then
  # 무엇이든 만들기 전에 막는다 — 반쯤 만든 .harness 가 남으면 다음 init 이 "이미 존재" 로 멈춘다
  [ -d "$HARNESS_STORE" ] || { echo "❌ HARNESS_STORE 폴더가 없다: $HARNESS_STORE" >&2; exit 1; }
  # 바로가기가 상대 경로를 담으면 .harness 위치 기준으로 풀려 엉뚱한 곳을 가리킨다
  HARNESS_STORE=$(cd "$HARNESS_STORE" && pwd -P)
  git -C "$HARNESS_STORE" rev-parse --show-toplevel >/dev/null 2>&1 \
    || { echo "❌ HARNESS_STORE 가 깃 저장소가 아니다: $HARNESS_STORE" >&2; exit 1; }
  PROJECT_TOP=$(git -C "$TARGET_DIR" rev-parse --show-toplevel 2>/dev/null) \
    || { echo "❌ 대상이 깃 저장소 안에 있지 않아 하네스 저장소 폴더 이름을 정할 수 없다: $TARGET_DIR" >&2; exit 1; }
  STORE_DIR="$HARNESS_STORE/$(basename "$PROJECT_TOP")${TARGET_DIR#"$PROJECT_TOP"}"
fi

echo "=== Harness Init ==="
echo "Target: $TARGET_DIR"
echo "Stack:  $STACK"
echo ""

# 1. 디렉토리 생성 — 하네스 저장소 모양이면 그 폴더를 만들고 .harness 를 바로가기로 잇는다.
#    이미 기록이 있는 폴더(같은 프로젝트의 다른 작업 폴더)면 템플릿을 덮지 않고 잇기만 한다
REUSED=false
if [ -n "$STORE_DIR" ]; then
  [ -f "$STORE_DIR/project.yaml" ] && REUSED=true
  mkdir -p "$STORE_DIR"
  ln -s "$STORE_DIR" "$HARNESS_DIR"
  # 바로가기는 깃에게 파일이라 끝에 / 를 붙인 규칙(.harness/)에는 걸리지 않는다
  git -C "$PROJECT_TOP" check-ignore -q "$HARNESS_DIR" || printf '.harness\n' >> "$PROJECT_TOP/.gitignore"
fi
if [ "$REUSED" = true ]; then
  echo "↪ 기존 기록에 이었다: $HARNESS_DIR -> $STORE_DIR"
  exit 0
fi
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
