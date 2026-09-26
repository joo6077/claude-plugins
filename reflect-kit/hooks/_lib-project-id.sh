#!/usr/bin/env bash
# reflect-kit: 프로젝트 ID 계산 (v0.3.0 Hybrid)
#
# 기본 출력: <basename>
# 충돌 감지 시: <basename>-<6자 hash> + stderr 1회 경고
#
# "충돌" 정의 — 동일 basename 디렉토리의 .project-root 마커가
# 현재 project_root 와 다른 경로를 가리킬 때. 마커는 compute 시점에
# 자동 ensure (basename 반환 경로). read 와 write 경로 모두 안전.
#
# 기존 <basename>-<hash> 디렉토리는 그대로 read 지원 (reflect-digest
# 의 glob union 으로 커버).
#
# 사용법:
#   source 후 project_id=$(compute_project_id "$cwd")
#   또는 query=$(normalize_project_query "<basename>")
#   digest · kaizen 머리 (bash 에서만): collect_status <일수|all> <bucket 폴더>...
#     facets_unmatched <일수|all> <프로젝트 이름|all> [usage-data 폴더] [logs 폴더]

LOGS_ROOT_DEFAULT="$HOME/.claude/logs"

_rk_hash6() {
  local input="$1"
  local h
  if command -v md5 >/dev/null 2>&1; then
    h=$(printf '%s' "$input" | md5 2>/dev/null)
  elif command -v md5sum >/dev/null 2>&1; then
    h=$(printf '%s' "$input" | md5sum 2>/dev/null | awk '{print $1}')
  else
    h=$(printf '%s' "$input" | cksum 2>/dev/null | awk '{print $1}')
  fi
  h=${h:0:6}
  [ -z "$h" ] && h="noid00"
  printf '%s' "$h"
}

# 내부 디렉토리 필터: "_", "." prefix 디렉토리는 project bucket 이 아님
# (예: _cron — install-scheduler.sh 가 만든 로그 디렉토리)
is_internal_logs_dir() {
  local name="$1"
  case "$name" in
    .*) return 0 ;;
    _*) return 0 ;;
    *) return 1 ;;
  esac
}

# 단일 프로세스 내에서 동일 basename 충돌 경고를 1회만 출력
# 마커 파일: ${TMPDIR:-/tmp}/.reflect-kit-warn-<basename>-<PID>
_rk_warn_once() {
  local basename="$1"
  local msg="$2"
  local marker="${TMPDIR:-/tmp}/.reflect-kit-warn-${basename}-$$"
  [ -e "$marker" ] && return 0
  : > "$marker" 2>/dev/null
  printf '%s\n' "$msg" >&2
}

# 워크트리 안에서도 본 레포 폴더를 돌려준다. --show-toplevel 만 쓰면 워크트리 폴더가 나와
# 같은 레포가 워크트리 이름마다 다른 로그 폴더로 갈렸다 (2026-09-25 실측: 폴더 31 개 중 12 개).
# 공통 git 폴더의 부모는 링크된 워크트리(git-dir 과 common-dir 이 다름)이고 그 폴더 이름이 .git 일
# 때만 쓴다 — 서브모듈의 공통 폴더는 상위 레포의 .git/modules/<이름> 이라 부모를 쓰면 엉뚱하게 묶인다.
project_root() {
  local dir="$1" top gdir common
  [ -z "$dir" ] && dir="$PWD"
  top=$(git -C "$dir" rev-parse --show-toplevel 2>/dev/null)
  if [ -z "$top" ]; then
    printf '%s\n' "$dir"
    return 0
  fi
  gdir=$(git -C "$dir" rev-parse --path-format=absolute --git-dir 2>/dev/null)
  common=$(git -C "$dir" rev-parse --path-format=absolute --git-common-dir 2>/dev/null)
  if [ -n "$common" ] && [ "$gdir" != "$common" ] && [ "$(basename "$common")" = ".git" ]; then
    dirname "$common"
    return 0
  fi
  printf '%s\n' "$top"
}

compute_project_id() {
  local cwd="$1"
  [ -z "$cwd" ] && cwd="$PWD"

  local repo_root
  repo_root=$(project_root "$cwd")

  local base
  base=$(basename "$repo_root")

  local logs_root="${REFLECT_KIT_LOGS_ROOT:-$LOGS_ROOT_DEFAULT}"
  local base_dir="$logs_root/$base"
  local marker="$base_dir/.project-root"

  # 충돌 감지: 기존 basename 디렉토리의 마커가 다른 git root 를 가리킴
  if [ -d "$base_dir" ] && [ -f "$marker" ]; then
    local stored
    stored=$(cat "$marker" 2>/dev/null)
    if [ -n "$stored" ] && [ "$stored" != "$repo_root" ]; then
      local h
      h=$(_rk_hash6 "$repo_root")
      _rk_warn_once "$base" \
        "[reflect-kit] basename collision for '$base' — using '${base}-${h}'. existing: $stored, current: $repo_root"
      printf '%s-%s' "$base" "$h"
      return 0
    fi
  fi

  # 충돌 없음 — basename bucket ensure + 마커 ensure
  # (read 경로에서도 자기 repo 의 bucket 만 생성하므로 안전)
  mkdir -p "$base_dir" 2>/dev/null
  [ ! -f "$marker" ] && printf '%s\n' "$repo_root" > "$marker" 2>/dev/null

  printf '%s' "$base"
}

# digest 용: project 쿼리를 glob pattern union 으로 확장
# 입력이 어느 쪽이든 같은 basename 의 "basename + basename-<hash6>" union 을 반환
# 하여 backward-compat 을 보장한다 (SK-01 동등성 계약).
#
#   basename        → "<basename> <basename>-[0-9a-f]{6}"
#   basename-<hash> → basename 추출 → "<basename> <basename>-[0-9a-f]{6}"
normalize_project_query() {
  local query="$1"
  local base
  case "$query" in
    *-[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f])
      base="${query%-??????}"
      ;;
    *)
      base="$query"
      ;;
  esac
  printf '%s %s-[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]' "$base" "$base"
}

# 에러 메타로깅: .errors.log 에 타임스탬프 + 이유 append
log_hook_error() {
  local log_dir="$1"
  local hook_name="$2"
  local reason="$3"
  [ -z "$log_dir" ] && return 0
  [ ! -d "$log_dir" ] && return 0
  local ts
  ts=$(date '+%Y-%m-%dT%H:%M:%S%z')
  printf '%s [%s] %s\n' "$ts" "$hook_name" "$reason" >> "$log_dir/.errors.log" 2>/dev/null
}

# ── 수집 상태 · facets 대조 (reflect-digest · reflect-kaizen 머리) ─────────
# 엔트리 0 은 실수가 없어도, 수집기가 멈춰도 나온다. 2026-09-14~23 은 Stop 실패 시도 849 번에
# 기록된 세션 0 이었다 — 요약에 0 만 있으면 정반대로 읽힌다.
# 두 함수는 bash 에서만 시험했다. 같은 입력에 셸마다 조용히 다른 답을 낸 전례가 있어
# (_lib-tag-canon.sh 2026-08-13) bash 가 아니면 멈춘다.

# <일수|all> → 기준 시각 (로컬 YYYY-MM-DDTHH:MM:SS, all 이면 빈 값).
# 로그 시각이 이 기계의 시간대로 적히므로 앞 19 자를 글자 순서로 비교한다.
_rk_since() {
  case "$1" in
    all) printf '' ;;
    ''|*[!0-9]*) return 2 ;;
    *) date -v-"$1"d '+%Y-%m-%dT%H:%M:%S' 2>/dev/null || date -d "-$1 days" '+%Y-%m-%dT%H:%M:%S' ;;
  esac
}

# collect_status <일수|all> <bucket 폴더>... — 요약 머리에 그대로 싣는 한두 줄.
# Stop 실패 시도 = 기록 없이 끝난 실행. codex 실패와 대체 경로 실패는 한 실행의 두 단계라 더하지
# 않는다 — 대체 경로가 성공한 실행은 기록이 남으므로 실패 시도에 들지 않는다.
collect_status() {
  [ -n "${BASH_VERSION:-}" ] || { echo "collect_status: bash 로 부른다" >&2; return 2; }
  local since b rf errs refl
  since=$(_rk_since "$1") || { echo "collect_status: 일수는 숫자 또는 all" >&2; return 2; }
  shift
  refl=$(for b in "$@"; do find "$b" -maxdepth 1 -type f -name 'reflections-*.md' 2>/dev/null; done \
    | while IFS= read -r rf; do cat "$rf"; done | awk -v since="$since" '
    /^## [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T/ {
      ts = substr($0, 4); if (ts > last) last = ts
      inp = (since == "" || substr(ts, 1, 19) >= since); iny = 0; next
    }
    inp && /^- session: `/ {
      s = $0; sub(/^- session: `/, "", s); sub(/`.*$/, "", s)
      if (s != "" && !(s in seen)) { seen[s] = 1; k++ }
    }
    # 0.8.0 훅은 분석기가 코드 블록을 빼면 그대로 적었다 — yaml 코드 블록 밖의 primary_category 줄도 엔트리 하나다
    iny && /^[ \t]*```[ \t]*$/ { iny = 0; next }
    !iny && /^[ \t]*```yaml[ \t]*$/ { iny = 1; if (inp) e++; next }
    inp && !iny && /^[ \t]*primary_category:/ { e++ }
    END { printf "%d %d %s\n", k, e, (last == "" ? "없음" : last) }')
  local c f u p ns a stale k e last lastk n
  read -r k e last <<EOF
$refl
EOF
  # 마지막 기록 시각을 먼저 구한다 — 엔트리가 하나라도 있으면 엔트리 0 경고가 안 나와 기간 도중에 멈춘
  # 수집기를 놓친다. 마지막 기록 뒤의 실패 시도를 따로 센다
  lastk=${last:0:19}; [ "$last" = 없음 ] && lastk=
  errs=$(for b in "$@"; do [ -f "$b/.errors.log" ] && cat "$b/.errors.log"; done | awk -v since="$since" -v last="$lastk" -v day_ago="$(_rk_since 1)" '
    $2 != "[log-reflection]" { next }
    since != "" && substr($1, 1, 19) < since { next }
    { lost = 0 }
    $3 ~ /^fail:codex-(exit-[0-9]+|empty-output)$/ { c++ }
    $3 == "fallback:claude-used" { u++ }
    $3 ~ /^fallback:claude-(exit-[0-9]+|empty-output)$/ || $3 == "skip:fallback-unavailable" { f++; lost = 1 }
    $3 == "skip:cli-missing" || $3 == "fail:tag-field-unresolved" { p++; lost = 1 }
    $3 == "ok:no-issues" || $3 == "skip:env-dedup-all" { if (substr($1, 1, 19) > okl) okl = substr($1, 1, 19) }
    lost { lt[++nl] = substr($1, 1, 19) }
    lost && match($0, / session=[^ ]*/) {
      s = substr($0, RSTART + 9, RLENGTH - 9)
      if (s != "" && !(s in seen)) { seen[s] = 1; ns++ }
    }
    # 정상 종료(no issues · 전 블록 억제)는 기록을 안 남긴다 — 마지막 기록과 마지막 정상 종료 가운데 늦은 쪽 뒤의 실패만 센다
    END { cut = (okl > last) ? okl : last
          for (i = 1; i <= nl; i++) if (cut == "" || lt[i] > cut) { a++; if (first == "" || lt[i] < first) first = lt[i] }
          printf "%d %d %d %d %d %d %d\n", c, f, u, p, ns, a, (first != "" && first <= day_ago) }')
  read -r c f u p ns a stale <<EOF
$errs
EOF
  n=$((f + p))
  printf '수집 상태: Stop 실패 시도 %d회 (codex 실패 %d · 대체 경로 실패 %d · 대체 경로 성공 %d · 분석 전 중단 %d; 고유 세션 %d) / 기록된 세션 %d / 엔트리 %d / 마지막 기록 %s\n' \
    "$n" "$c" "$f" "$u" "$p" "$ns" "$k" "$e" "$last"
  # 엔트리가 있는 기간은 실패 3 회 이상이 첫 실패부터 1 일 넘게 이어질 때만 멈춤으로 본다. digest 는 이 줄
  # 하나에 승격 후보를 통째로 비우는데, 한도 초과 같은 일시 실패나 옛 판 세션의 실패 몇 줄로 켜지면 안 된다
  # (2026-09-26 실측: 새 판이 기록하는 동안 옛 판 세션 둘이 한 시간 안에 실패 여섯 줄을 남겼다)
  if [ "$e" -eq 0 ] && [ "$a" -gt 0 ]; then
    printf '%s\n' '⚠ 수집 멈춤 — 엔트리 0은 문제 없음이 아니다'
  elif [ "$a" -ge 3 ] && [ "$stale" = 1 ]; then
    printf '⚠ 수집 멈춤 — 마지막 기록 뒤 Stop 실패 시도 %d회\n' "$a"
  fi
  return 0
}

# facets_unmatched <일수|all> <프로젝트 이름|all> [usage-data 폴더] [logs 폴더]
# 마찰이 적혔는데 reflections 에 한 번도 안 나온 세션을 원문과 함께 낸다. 수집기가 놓친 세션을
# 찾는 데만 쓴다 — facets 는 다른 분석기 · 다른 분류라 빈도에 더하면 같은 세션을 두 번 센다.
# facets 에는 프로젝트 경로가 없어 session-meta/<session_id>.json 의 project_path 로 잇는다.
# 지워진 워크트리 경로는 git 이 본 레포를 못 구해 폴더 이름으로 남는다 — 그 세션은 all 에서만 보인다.
facets_unmatched() {
  [ -n "${BASH_VERSION:-}" ] || { echo "facets_unmatched: bash 로 부른다" >&2; return 2; }
  local days="$1" want="$2" usage="${3:-$HOME/.claude/usage-data}"
  local logs="${4:-${REFLECT_KIT_LOGS_ROOT:-$LOGS_ROOT_DEFAULT}}"
  local since=0 seen fj sid fd meta pp st ep total=0 fbad=0 mbad=0 fric=0 miss=0 rows=""
  case "$days" in
    all) ;;
    ''|*[!0-9]*) echo "facets_unmatched: 일수는 숫자 또는 all" >&2; return 2 ;;
    *) since=$(( $(date +%s) - days * 86400 )) ;;
  esac
  [ -n "$want" ] || { echo "facets_unmatched: 프로젝트 이름 또는 all" >&2; return 2; }
  if [ ! -d "$usage/facets" ]; then
    echo "facets 대조: (없음)"
    return 0
  fi
  command -v jq >/dev/null 2>&1 || { echo "facets 대조: jq 가 없어 대조하지 못했다"; return 2; }
  # shellcheck disable=SC2016  # 역따옴표는 reflections 머리의 마크다운 글자다
  seen=$(find "$logs" -mindepth 2 -maxdepth 2 -type f -name 'reflections-*.md' \
    -exec sed -n 's/^- session: `\([^`]*\)`.*/\1/p' {} + 2>/dev/null | sort -u)
  while IFS= read -r fj; do
    sid=$(jq -er '.session_id | strings' "$fj" 2>/dev/null) || { fbad=$((fbad + 1)); continue; }
    fd=$(jq -r '.friction_detail // "" | tostring' "$fj" 2>/dev/null | tr '\n' ' ' | sed 's/[[:space:]]*$//')
    meta="$usage/session-meta/$sid.json"
    pp=$(jq -er '.project_path | strings' "$meta" 2>/dev/null) || { mbad=$((mbad + 1)); continue; }
    st=$(jq -r '.start_time // ""' "$meta" 2>/dev/null)
    ep=$(jq -r '.start_time // "" | sub("\\.[0-9]+Z$"; "Z") | (fromdateiso8601? // 0) | floor' "$meta" 2>/dev/null)
    [ "${ep:-0}" -ge "$since" ] 2>/dev/null || continue
    [ "$want" = all ] || [ "$(basename "$(project_root "$pp")")" = "$want" ] || continue
    total=$((total + 1))
    [ -n "$(printf '%s' "$fd" | tr -d '[:space:]')" ] || continue
    fric=$((fric + 1))
    printf '%s\n' "$seen" | grep -qxF -- "$sid" && continue
    miss=$((miss + 1))
    rows="$rows- $sid · $st · $pp — $fd"$'\n'
  done < <(find "$usage/facets" -maxdepth 1 -type f -name '*.json' | sort)
  printf 'facets 대조: facets %d개 · 마찰 있는 세션 %d개 · 그중 reflections 없음 %d개 (facets 읽기 실패 %d · session-meta 읽기 실패 %d)\n' \
    "$total" "$fric" "$miss" "$fbad" "$mbad"
  printf '%s' "$rows"
}
