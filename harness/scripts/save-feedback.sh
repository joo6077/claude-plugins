#!/usr/bin/env bash
set -eo pipefail

# 피드백 YAML을 스키마 검증 후 글로벌 경로에 저장한다.
# LLM이 생성한 draft YAML을 받아서 검증 + identity 재계산 + 복사 + 정리한다.
#
# identity(project_name/project_hash)는 draft 값을 신뢰하지 않고 CONTRACT_ROOT
# 기준으로 **스스로 계산**한다. draft 원본은 draft_project_name /
# draft_project_hash 로 보존하고, 값이 달랐으면 stderr 에 경고를 낸다.
#
# contract_path 는 HARNESS_CONTRACT / draft 값이 없으면 추론한다. 추론했으면 stderr 경고 +
# `contract_path_inferred: true` 를 남긴다. 슬러그가 있는데 접미형 계약이 없으면 plain
# `sprint-contract.md` 로 내려가지 않고 필드를 생략한다 (stale 계약 오귀속 방지).
#
# Usage: bash save-feedback.sh <contract|evaluator> <draft-yaml-path>
# Output: 저장된 파일의 절대경로 (stdout)
# Exit: 0=성공, 1=검증실패, 2=인자오류
#
# 선택 환경변수:
#   HARNESS_CONTRACT_ROOT  — CONTRACT_ROOT 를 직접 지정 (미지정 시 자동 해석)
#   HARNESS_CONTRACT       — 계약 파일 경로 (contract_path / sprint_slug 도출)
#   HARNESS_SPRINT_SLUG    — 스프린트 슬러그 직접 지정
#   CLAUDE_CODE_SESSION_ID — session_id 필드 + 파일명 충돌 방지에 사용

SKILL_TYPE="${1:?Usage: save-feedback.sh <contract|evaluator> <draft-yaml-path>}"
DRAFT_PATH="${2:?Usage: save-feedback.sh <contract|evaluator> <draft-yaml-path>}"

if [[ "$SKILL_TYPE" != "contract" && "$SKILL_TYPE" != "evaluator" ]]; then
  echo "ERROR: skill type must be 'contract' or 'evaluator'" >&2
  exit 2
fi

# --- Python 명령 감지 (Windows Store 스텁 회피) ---
PYTHON_CMD=""
if command -v python3 &>/dev/null && python3 -c "pass" &>/dev/null; then
  PYTHON_CMD="python3"
elif command -v python &>/dev/null && python -c "pass" &>/dev/null; then
  PYTHON_CMD="python"
fi

# --- 스키마 검증 ---
validate_yaml() {
  local file="$1"

  # yq 또는 python으로 YAML 파싱 + 필수 필드 검증
  # 검증 대상: feedback-schema.yaml의 공통 필수 필드 + diagnosis
  # ⚠ 두 백엔드(yq · python)는 **같은 문구**로 실패해야 한다. 백엔드에 따라 메시지가 달라지면
  #   소비자(evals 네거티브 테스트 등)가 한쪽 문구만 assert 하게 되어 다른 환경에서만 깨진다.
  #   실측 2026-08-14: 로컬(yq 없음)은 python 경로라 통과했는데 CI(yq 있음)는 셸 경로라
  #   `timestamp 필드 누락` 을 내서 `누락 필드` 를 기대한 테스트가 CI 에서만 FAIL 했다.
  #   그래서 yq 경로도 **전체 누락 목록**을 python 과 동일한 형태로 낸다.
  if command -v yq &>/dev/null; then
    local fields=("schema_version" "skill" "timestamp" "project_hash" "project_name" "skill_version" "outcome" "diagnosis")
    local missing=()
    for field in "${fields[@]}"; do
      local val
      val=$(yq ".$field" "$file" 2>/dev/null)
      if [[ "$val" == "null" || -z "$val" ]]; then
        missing+=("'$field'")
      fi
    done
    if (( ${#missing[@]} > 0 )); then
      # `${arr[*]}` 는 IFS 의 **첫 글자만** 구분자로 쓴다 — `IFS=', '` 로는 `, ` 가 안 나온다.
      # python 의 list repr 과 바이트 단위로 같게 하려고 printf 로 붙인 뒤 꼬리를 자른다.
      local joined
      joined=$(printf "%s, " "${missing[@]}"); joined="${joined%, }"
      echo "FAIL: 누락 필드: [${joined}]" >&2; return 1
    fi

  elif [[ -n "$PYTHON_CMD" ]]; then
    $PYTHON_CMD -c "
import yaml, sys
with open(sys.argv[1], encoding='utf-8') as f:
    d = yaml.safe_load(f)
required = ['schema_version', 'skill', 'timestamp', 'project_hash', 'project_name', 'skill_version', 'outcome', 'diagnosis']
missing = [k for k in required if k not in d or d[k] is None]
if missing:
    print(f'FAIL: 누락 필드: {missing}', file=sys.stderr)
    sys.exit(1)
" "$file" || return 1

  else
    echo "ERROR: yq 또는 python 필수 — 스키마 검증 불가" >&2
    return 1
  fi

  return 0
}

if ! validate_yaml "$DRAFT_PATH"; then
  echo "ERROR: 스키마 검증 실패" >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# identity 계산
# ---------------------------------------------------------------------------

# CONTRACT_ROOT: 조상 체인에서 **처음 만나는 `.harness/` 디렉토리**. 판정 기준은
# `project.yaml` 이 아니라 `.harness/` 자체다 (SSOT: harness/references/contract-schema.md
# §CONTRACT_ROOT 해석 v5.2). qa-evaluator Step 1-a · sprint-contract Step 0 과 동일 알고리즘 —
# 세 표면이 갈라지면 조용한 오귀속이 재발한다.
#
# v5.1 까지는 `project.yaml` 기준이라 그것이 없는 `.harness/` 를 지나쳐 상위로 올라갔고,
# 그 결과 자기 계약을 가진 디렉토리를 건너뛰고 **남의 프로젝트로 귀속**시켰다
# (실측: apps/apps/app_kiosk → 조상 apps 로 상승).
# 후보가 여러 개여도 실패시키지 않는다 — 중첩 배포본(fit-pal/app 등)이 정상 케이스다.
resolve_contract_root() {
  if [[ -n "$HARNESS_CONTRACT_ROOT" && -d "$HARNESS_CONTRACT_ROOT" ]]; then
    (cd "$HARNESS_CONTRACT_ROOT" && pwd)
    return 0
  fi

  local dir
  dir="$PWD"
  while :; do
    if [[ -d "$dir/.harness" ]]; then
      printf '%s' "$dir"; return 0
    fi
    if [[ -z "$dir" || "$dir" == "/" ]]; then
      break
    fi
    dir="$(dirname "$dir")"
  done

  # `.harness/` 자체가 조상 체인에 없으면 git root, 그것도 없으면 cwd
  local gr
  gr="$(git -C "$PWD" rev-parse --show-toplevel 2>/dev/null)" || gr=""
  if [[ -n "$gr" ]]; then printf '%s' "$gr"; return 0; fi
  printf '%s' "$PWD"
}

# reflect-kit 과 동일하게 git root 를 identity 기준 경로로 삼는다.
identity_root_of() {
  local root="$1" gr
  gr="$(git -C "$root" rev-parse --show-toplevel 2>/dev/null)" || gr=""
  if [[ -n "$gr" ]]; then printf '%s' "$gr"; return 0; fi
  printf '%s' "$root"
}

# reflect-kit hooks/_lib-project-id.sh 의 _rk_hash6 과 동일 로직
rk_hash6() {
  local h=""
  if command -v md5 >/dev/null 2>&1; then
    h="$(printf '%s' "$1" | md5 2>/dev/null)" || h=""
  elif command -v md5sum >/dev/null 2>&1; then
    h="$(printf '%s' "$1" | md5sum 2>/dev/null | awk '{print $1}')" || h=""
  else
    h="$(printf '%s' "$1" | cksum 2>/dev/null | awk '{print $1}')" || h=""
  fi
  h="${h:0:6}"
  if [[ -z "$h" ]]; then h="noid00"; fi
  printf '%s' "$h"
}

# reflect-kit 의 project-id canonicalization 과 **같은 값**을 만든다.
# basename 기본, 동일 basename 이 다른 repo 로 이미 점유됐으면 6자 hash suffix.
# 읽기 전용 — reflect-kit 로그 버킷이나 .project-root 마커를 새로 만들지 않는다.
canonical_project_name() {
  local repo_root="$1"
  local base
  base="$(basename "$repo_root")"

  local logs_root="${REFLECT_KIT_LOGS_ROOT:-$HOME/.claude/logs}"
  local marker="$logs_root/$base/.project-root"
  if [[ -f "$marker" ]]; then
    local stored
    stored="$(cat "$marker" 2>/dev/null)" || stored=""
    if [[ -n "$stored" && "$stored" != "$repo_root" ]]; then
      printf '%s-%s' "$base" "$(rk_hash6 "$repo_root")"
      return 0
    fi
  fi
  printf '%s' "$base"
}

# 경로 SHA-256 앞 8자 (feedback-schema.yaml 의 project_hash 정의)
hash8() {
  local input="$1" h=""
  if command -v sha256sum >/dev/null 2>&1; then
    h="$(printf '%s' "$input" | sha256sum | awk '{print $1}')" || h=""
  elif command -v shasum >/dev/null 2>&1; then
    h="$(printf '%s' "$input" | shasum -a 256 | awk '{print $1}')" || h=""
  elif [[ -n "$PYTHON_CMD" ]]; then
    h="$($PYTHON_CMD -c "import hashlib,sys; print(hashlib.sha256(sys.argv[1].encode('utf-8')).hexdigest())" "$input")" || h=""
  elif command -v openssl >/dev/null 2>&1; then
    h="$(printf '%s' "$input" | openssl dgst -sha256 | sed 's/.*= //')" || h=""
  fi
  if [[ -z "$h" ]]; then h="nohash00"; fi
  printf '%s' "${h:0:8}"
}

# draft 의 top-level 스칼라 값 추출 (따옴표/후행 공백 제거)
draft_scalar() {
  sed -n "s/^$1:[[:space:]]*//p" "$DRAFT_PATH" 2>/dev/null | head -1 \
    | sed -e 's/[[:space:]]*$//' -e 's/^["'"'"']//' -e 's/["'"'"']$//'
}

# YAML single-quoted 스칼라로 이스케이프
yaml_str() {
  local v="$1"
  v="${v//\'/\'\'}"
  printf "'%s'" "$v"
}

CONTRACT_ROOT="$(resolve_contract_root)"
IDENTITY_ROOT="$(identity_root_of "$CONTRACT_ROOT")"
PROJ_NAME="$(canonical_project_name "$IDENTITY_ROOT")"
PROJ_HASH="$(hash8 "$IDENTITY_ROOT")"

DRAFT_NAME="$(draft_scalar project_name)"
DRAFT_HASH="$(draft_scalar project_hash)"

if [[ -n "$DRAFT_NAME" && "$DRAFT_NAME" != "$PROJ_NAME" ]]; then
  echo "WARNING: draft 의 project_name '$DRAFT_NAME' → 재계산값 '$PROJ_NAME' 으로 덮어씀 (원본은 draft_project_name 으로 보존)" >&2
fi
if [[ -n "$DRAFT_HASH" && "$DRAFT_HASH" != "$PROJ_HASH" ]]; then
  echo "WARNING: draft 의 project_hash '$DRAFT_HASH' → 재계산값 '$PROJ_HASH' 으로 덮어씀 (원본은 draft_project_hash 로 보존)" >&2
fi

# --- 스프린트 슬러그 / 계약 경로 ---
SPRINT_SLUG="$HARNESS_SPRINT_SLUG"
CONTRACT_PATH="$HARNESS_CONTRACT"
if [[ -z "$SPRINT_SLUG" ]]; then SPRINT_SLUG="$(draft_scalar sprint_slug)"; fi
if [[ -z "$CONTRACT_PATH" ]]; then CONTRACT_PATH="$(draft_scalar contract_path)"; fi

if [[ -z "$SPRINT_SLUG" && -n "$CONTRACT_PATH" ]]; then
  _base="$(basename "$CONTRACT_PATH")"
  _base="${_base%.md}"
  case "$_base" in
    sprint-contract-*) SPRINT_SLUG="${_base#sprint-contract-}" ;;
  esac
fi

# contract_path 추론.
#
# 명시 소스(HARNESS_CONTRACT · draft 의 contract_path)가 없으면 그 뒤는 전부 **추측**이다.
# 배포본은 거의 전부 stale 한 plain `sprint-contract.md` 를 갖고 있어서, 접미형 스프린트의
# 피드백이 무관한 옛 plain 계약에 귀속되는 오귀속이 조용히 발생한다. 그래서:
#   1. 슬러그가 있으면 **접미형만** 본다. plain 으로 절대 내려가지 않는다.
#   2. 추론했으면 stderr 경고 + `contract_path_inferred: true` 를 남긴다
#      (project_name/project_hash 덮어쓰기와 동일한 관측 가능성 수준).
CONTRACT_PATH_INFERRED=false
if [[ -z "$CONTRACT_PATH" ]]; then
  if [[ -n "$SPRINT_SLUG" ]]; then
    SLUGGED_CONTRACT="$CONTRACT_ROOT/.harness/sprint-contract-$SPRINT_SLUG.md"
    if [[ -f "$SLUGGED_CONTRACT" ]]; then
      CONTRACT_PATH="$SLUGGED_CONTRACT"
      CONTRACT_PATH_INFERRED=true
      echo "WARNING: contract_path 미지정 — 슬러그 '$SPRINT_SLUG' 로 추론함: $CONTRACT_PATH (contract_path_inferred: true)" >&2
    else
      echo "WARNING: contract_path 미지정 + 슬러그 '$SPRINT_SLUG' 의 접미형 계약 부재 ($SLUGGED_CONTRACT) — contract_path 를 생략한다. plain sprint-contract.md 로 내려가지 않는다 (stale 계약 오귀속 방지)" >&2
    fi
  elif [[ -f "$CONTRACT_ROOT/.harness/sprint-contract.md" ]]; then
    CONTRACT_PATH="$CONTRACT_ROOT/.harness/sprint-contract.md"
    CONTRACT_PATH_INFERRED=true
    echo "WARNING: contract_path 도 슬러그도 미지정 — plain 계약으로 추론함: $CONTRACT_PATH (contract_path_inferred: true). 접미형 스프린트였다면 stale 계약에 오귀속된 것이니 HARNESS_CONTRACT 를 명시하라" >&2
  else
    echo "WARNING: contract_path 를 결정할 수 없다 (HARNESS_CONTRACT · draft contract_path · 슬러그 모두 없음) — 필드 생략" >&2
  fi
fi

# --- 글로벌 경로 결정 ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GLOBAL_DIR="$(bash "$SCRIPT_DIR/feedback-path.sh")/$SKILL_TYPE"

# --- 파일명 생성 (ISO8601 타임스탬프 + 세션/pid 접미) ---
# 같은 초에 병렬 저장돼도 덮어쓰지 않도록 세션 앞자리와 pid 를 붙인다.
TIMESTAMP=$(date +"%Y-%m-%dT%H%M%S")
SESS_SHORT=""
if [[ -n "$CLAUDE_CODE_SESSION_ID" ]]; then
  SESS_SHORT="$(printf '%s' "$CLAUDE_CODE_SESSION_ID" | tr -cd '[:alnum:]' | cut -c1-8)"
fi
if [[ -n "$SESS_SHORT" ]]; then
  UNIQ="${SESS_SHORT}-$$"
else
  UNIQ="p$$"
fi
FILE_BASE="${PROJ_HASH}-${TIMESTAMP}-${UNIQ}"

# --- 최종 본문 작성 (identity 재계산 반영) ---
FINAL_TMP="$(mktemp "${TMPDIR:-/tmp}/harness-feedback.XXXXXX")"

# draft 의 top-level identity 필드를 draft_* 로 보존 (본문 나머지는 원문 유지)
sed -e 's/^project_hash:/draft_project_hash:/' \
    -e 's/^project_name:/draft_project_name:/' \
    "$DRAFT_PATH" > "$FINAL_TMP"

# 파일 끝 개행 보장 (없으면 append 가 마지막 줄에 붙는다)
if [[ -n "$(tail -c1 "$FINAL_TMP")" ]]; then
  printf '\n' >> "$FINAL_TMP"
fi

{
  printf '\n# --- save-feedback.sh 재계산 identity (CONTRACT_ROOT 기준) ---\n'
  printf 'project_name: %s\n' "$(yaml_str "$PROJ_NAME")"
  printf 'project_hash: %s\n' "$(yaml_str "$PROJ_HASH")"
  printf 'contract_root: %s\n' "$(yaml_str "$CONTRACT_ROOT")"
  if [[ -n "$SPRINT_SLUG" ]]; then
    printf 'sprint_slug: %s\n' "$(yaml_str "$SPRINT_SLUG")"
  fi
  if [[ -n "$CONTRACT_PATH" ]]; then
    printf 'contract_path: %s\n' "$(yaml_str "$CONTRACT_PATH")"
    # 이 계약 경로가 명시된 것(false)인지 스크립트가 추측한 것(true)인지 기록한다.
    # 집계 쪽에서 추론 귀속 비율을 볼 수 있어야 오귀속이 조용히 누적되지 않는다.
    printf 'contract_path_inferred: %s\n' "$CONTRACT_PATH_INFERRED"
  fi
  if [[ -n "$CLAUDE_CODE_SESSION_ID" ]]; then
    printf 'session_id: %s\n' "$(yaml_str "$CLAUDE_CODE_SESSION_ID")"
  fi
} >> "$FINAL_TMP"

# 재작성 결과가 여전히 스키마를 만족하는지 확인 (draft 는 보존한 채 중단)
if ! validate_yaml "$FINAL_TMP"; then
  echo "ERROR: identity 재작성 후 스키마 검증 실패 — draft 보존: $DRAFT_PATH" >&2
  rm -f "$FINAL_TMP"
  exit 1
fi

# --- 저장 시도 (글로벌 → 로컬 fallback) ---
save_to() {
  local dir="$1"
  mkdir -p "$dir" 2>/dev/null || return 1
  local name="$FILE_BASE.yaml"
  local n=1
  while [[ -e "$dir/$name" ]]; do
    name="$FILE_BASE-$n.yaml"
    n=$((n + 1))
  done
  cp "$FINAL_TMP" "$dir/$name" 2>/dev/null || return 1
  printf '%s' "$dir/$name"
}

SAVED_PATH="$(save_to "$GLOBAL_DIR")" || SAVED_PATH=""

if [[ -z "$SAVED_PATH" ]]; then
  echo "WARNING: 글로벌 저장 실패 — 로컬 fallback" >&2
  SAVED_PATH="$(save_to "$CONTRACT_ROOT/.harness/feedback/$SKILL_TYPE")"
fi

# --- 정리 ---
rm -f "$FINAL_TMP" "$DRAFT_PATH"

# --- 결과 출력 ---
echo "$SAVED_PATH"
