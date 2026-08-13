#!/usr/bin/env bash
# reflect-kit — mistake_tag 결정론적 정규화 라이브러리 (LLM 앞단 pass)
#
# 왜 결정론적 pass 를 LLM 앞에 두는가:
#   분석기(LLM)는 세션마다 stateless 라 같은 근본원인에 매번 다른 표기를 붙인다.
#   ledger 의 post_freq 가 태그를 키로 재발을 세므로 이 파편화는 리포팅 문제가 아니라
#   **효과 측정 버그**다 (실패한 규칙이 "효과 있음" 으로 살아남는다).
#   LLM 에게 "잘 맞춰 써라" 라고 부탁하는 대신, 형태소·동의어·명시 alias 를 기계가 먼저
#   접어 버리고, LLM 에는 접힌 결과(canonical → aliases)만 되돌려준다.
#
# 설계 규약 (references/tag-canonicalization.md 가 정본):
#   - lemma key 는 **집계용 그룹 키**이지 표시용 태그가 아니다.
#   - canonical_tag 는 그룹 안에서 **가장 빈도가 높은 원시 표기**다 (동률이면 최근 것).
#     최빈이 아닌 표기를 canonical 로 강제하려면 수동 override 사유를 남긴다.
#   - 닫힌 라벨 집합을 강제하지 않는다. 새 태그는 허용하되 근거를 요구한다.
#
# 사용 (bash · zsh · sh 어디서든, cwd 무관 — **절대경로로 source 하라**):
#   . "${CLAUDE_PLUGIN_ROOT:-<repo>/reflect-kit}/hooks/_lib-tag-canon.sh"
#   tag_canon_groups <reflections 파일...>     # cluster_freq \t canonical \t aliases
#   tag_canon_fragmentation <파일...>          # 아래 7열 TSV 1줄
#   printf '%s\n' edited-before-read | tag_canon_keys   # 원시태그 → lemma key
#
# tag_canon_fragmentation 출력 열 (탭 구분, 헤더 없음):
#   1 raw_distinct  2 clusters  3 entries  4 singletons  5 fold_ratio  6 singleton_share  7 entries_per_cluster
#   fold_ratio(=1/2) 는 **정규화기 자체의 접힘 정도**만 잰다. 클러스터링이 아무것도 못 묶으면
#   1.00 이 나와 "정상" 으로 읽히므로, 어휘 파편화 판정에는 singleton_share(=4/2) 를 쓴다.
#
# 종료 코드: 0 정상 / 3 lemma map 없음(순수 kebab 정규화로 fail-open) / 1 입력 없음

# ── 자기 위치 해석 (source 시점에 1 회 확정) ───────────────────────────
# 왜 셸별로 갈라 쓰고, 왜 실패해도 cwd 를 쓰지 않는가:
#   `${BASH_SOURCE[0]}` 는 **bash 전용**이다. zsh 는 이 배열을 채우지 않으므로 빈 문자열이
#   되고, `dirname ""` → `.` → **호출 시점 cwd** 로 조용히 떨어진다. 그러면 cwd 가 hooks
#   디렉토리가 아닌 모든 호출(절대경로 source 등)에서 lemma map 을 "없음" 으로 오판해
#   순수 kebab 정규화로 전환되고, **에러 한 줄 없이 클러스터 수만 달라진다** — 무증상 실패다.
#   2026-08-13 재현 (동일 fixture · cwd=/):
#     bash `5 3 6 1 1.67 0.333 2.00` vs zsh `5 5 6 4 1.00 0.800 1.20`
#   그래서 세 가지를 지킨다:
#     (1) 셸별 관용구로 자기 경로를 확정한다.
#     (2) 확정에 실패해도 **cwd 로 추측하지 않는다** — 추측하는 순간 같은 입력이
#         셸·작업 디렉토리 조합마다 다른 답을 낸다.
#     (3) 그래도 못 정하면 조용히 넘어가지 않고 stderr 에 경고한다.
#   셸 고유 문법은 `eval` 로 감싼다 — 다른 셸의 파서에 노출하지 않기 위해서다.
_REFLECT_TAG_CANON_SELF=""
if [ -n "${BASH_VERSION:-}" ]; then
  # bash — macOS `/bin/sh`(sh-mode bash) 포함
  eval '_REFLECT_TAG_CANON_SELF=${BASH_SOURCE[0]}'
elif [ -n "${ZSH_VERSION:-}" ]; then
  # zsh — prompt 확장 `%x` = 지금 실행 중인 소스 파일 (BASH_SOURCE 를 제공하지 않는다)
  eval '_REFLECT_TAG_CANON_SELF=${(%):-%x}'
fi

_REFLECT_TAG_CANON_DIR=""
if [ -n "$_REFLECT_TAG_CANON_SELF" ]; then
  # CDPATH 가 설정된 사용자 환경에서 `cd` 가 엉뚱한 디렉토리로 가는 것을 막는다.
  _REFLECT_TAG_CANON_DIR="$(CDPATH='' cd -- "$(dirname -- "$_REFLECT_TAG_CANON_SELF")" 2>/dev/null && pwd)"
fi

_REFLECT_TAG_CANON_WARNED=""
_tag_canon_warn_unresolved() {
  [ -n "$_REFLECT_TAG_CANON_WARNED" ] && return 0
  _REFLECT_TAG_CANON_WARNED=1
  printf '%s\n' "[reflect-kit] _lib-tag-canon.sh: 이 셸에서는 라이브러리 자기 위치를 알 수 없어 lemma map 경로를 정할 수 없다. 순수 kebab 정규화로 fail-open 하므로 클러스터링 결과가 달라진다 — REFLECT_TAG_LEMMA_MAP 또는 CLAUDE_PLUGIN_ROOT 를 지정하라." >&2
}

# ── lemma map 경로 해석 ────────────────────────────────────────────────
# 우선순위: 명시 override → 라이브러리 자기 위치 → 플러그인 루트.
# **cwd 는 어떤 단계에서도 쓰지 않는다.** 읽히는 후보가 없으면 진단용으로 1 순위 후보
# 경로를 그대로 출력하고 rc=1 을 낸다 (호출자는 `[ -r ]` 로 다시 판정한다).
#
# 외부 변수는 전부 `${VAR:-}` 로 받는다. `set -u` 를 쓰는 호출자에서 unbound 로 함수가
# 중도 이탈하면 호출자는 `mp=""` 를 받아 **에러 없이 순수 kebab 정규화로 떨어진다** —
# cwd 의존과 똑같은 무증상 실패다 (2026-08-13 재현: `set -u` 시 `5 3 6 1` → `5 5 6 4`).
tag_canon_map_path() {
  if [ -n "${REFLECT_TAG_LEMMA_MAP:-}" ]; then
    # 존재 여부를 따지지 않고 그대로 돌려준다 — fail-open 경로를 테스트할 수 있어야 한다.
    printf '%s' "$REFLECT_TAG_LEMMA_MAP"
    return 0
  fi
  local self_cand=""
  local root_cand=""
  [ -n "${_REFLECT_TAG_CANON_DIR:-}" ] && self_cand="$_REFLECT_TAG_CANON_DIR/../references/tag-lemma-map.tsv"
  [ -n "${CLAUDE_PLUGIN_ROOT:-}" ] && root_cand="$CLAUDE_PLUGIN_ROOT/references/tag-lemma-map.tsv"
  if [ -n "$self_cand" ] && [ -r "$self_cand" ]; then printf '%s' "$self_cand"; return 0; fi
  if [ -n "$root_cand" ] && [ -r "$root_cand" ]; then printf '%s' "$root_cand"; return 0; fi
  if [ -n "$self_cand" ]; then printf '%s' "$self_cand"; return 1; fi
  if [ -n "$root_cand" ]; then printf '%s' "$root_cand"; return 1; fi
  _tag_canon_warn_unresolved
  return 1
}

# ── reflections 파일들에서 원시 mistake_tag 를 시간순으로 추출 ─────────
# 파일 인자가 없으면 stdin 을 "이미 추출된 원시 태그 목록" 으로 간주한다.
tag_canon_extract() {
  if [ "$#" -eq 0 ]; then
    cat
    return 0
  fi
  local f
  for f in "$@"; do
    [ -f "$f" ] || continue
    grep -h '^[[:space:]]*mistake_tag:' "$f" 2>/dev/null
  done | sed -e 's/^[[:space:]]*mistake_tag:[[:space:]]*//' -e 's/[[:space:]]*#.*$//'
}

# ── 공통 awk 프로그램 ───────────────────────────────────────────────────
# mode=keys    → 각 입력 줄마다 "raw \t lemma_key"
# mode=groups  → "cluster_freq \t canonical \t alias1(f1),alias2(f2),..."
# mode=frag    → "raw_distinct \t clusters \t ratio"
_tag_canon_awk() {
  awk -v mapfile="$1" -v mode="$2" -v maxalias="${3:-5}" '
  function norm(s,   t, n, i, seg, out, s1) {
    t = tolower(s)
    sq = sprintf("%c", 39)
    gsub(/["`]/, "", t); gsub(sq, "", t)
    gsub(/[ _.:\/]/, "-", t)
    gsub(/[^a-z0-9-]/, "", t)
    gsub(/-+/, "-", t)
    sub(/^-/, "", t); sub(/-$/, "", t)
    if (t == "") return ""
    n = split(t, seg, "-")
    s1 = seg[1]
    if (s1 in verb) s1 = verb[s1]
    if (s1 in vsyn) s1 = vsyn[s1]
    out = s1
    for (i = 2; i <= n; i++) {
      if (seg[i] in syn) out = out "-" syn[seg[i]]
      else out = out "-" seg[i]
    }
    if (out in alias) out = alias[out]
    return out
  }
  BEGIN {
    FS = "\t"
    map_ok = 0
    if (mapfile != "") {
      while ((getline line < mapfile) > 0) {
        if (line ~ /^[ \t]*#/ || line ~ /^[ \t]*$/) continue
        n = split(line, f, "\t")
        if (n < 3) continue
        kind = f[1]; from = tolower(f[2]); to = tolower(f[3])
        if (from == "" || to == "") continue
        if (kind == "verb") { verb[from] = to; map_ok = 1 }
        else if (kind == "verb-synonym") { vsyn[from] = to; map_ok = 1 }
        else if (kind == "synonym") { syn[from] = to; map_ok = 1 }
        else if (kind == "alias") { alias[from] = to; map_ok = 1 }
      }
      close(mapfile)
    }
    ord = 0
  }
  {
    raw = $0
    sq2 = sprintf("%c", 39)
    gsub(/["`]/, "", raw); gsub(sq2, "", raw)
    gsub(/^[ \t]+|[ \t]+$/, "", raw)
    if (raw == "") next
    key = norm(raw)
    if (key == "") next
    ord++
    total++
    cnt[key]++
    pair = key SUBSEP raw
    if (!(pair in pfreq)) { members[key] = members[key] (members[key] == "" ? "" : "|") raw }
    pfreq[pair]++
    plast[pair] = ord
    rawseen[raw] = 1
    if (mode == "keys") printf "%s\t%s\n", raw, key
  }
  END {
    if (mode == "keys") exit 0
    nclust = 0
    for (k in cnt) nclust++
    nraw = 0
    for (r in rawseen) nraw++
    if (mode == "frag") {
      nsing = 0
      for (k in cnt) if (cnt[k] == 1) nsing++
      fold = (nclust > 0) ? nraw / nclust : 0
      share = (nclust > 0) ? nsing / nclust : 0
      epc = (nclust > 0) ? total / nclust : 0
      printf "%d\t%d\t%d\t%d\t%.2f\t%.3f\t%.2f\n", nraw, nclust, total, nsing, fold, share, epc
      exit 0
    }
    for (k in cnt) {
      m = split(members[k], mm, "|")
      # freq desc, 동률이면 최근(ord 큰 것) 우선 — 선택 정렬
      for (i = 1; i <= m; i++) {
        best = i
        for (j = i + 1; j <= m; j++) {
          fj = pfreq[k SUBSEP mm[j]]; fb = pfreq[k SUBSEP mm[best]]
          if (fj > fb || (fj == fb && plast[k SUBSEP mm[j]] > plast[k SUBSEP mm[best]])) best = j
        }
        if (best != i) { tmp = mm[i]; mm[i] = mm[best]; mm[best] = tmp }
      }
      canonical = mm[1]
      astr = ""; shown = 0; hidden = 0
      for (i = 2; i <= m; i++) {
        if (shown < maxalias) {
          astr = astr (astr == "" ? "" : ",") mm[i] "(" pfreq[k SUBSEP mm[i]] ")"
          shown++
        } else hidden++
      }
      if (hidden > 0) astr = astr ",+" hidden "more"
      printf "%d\t%s\t%s\n", cnt[k], canonical, astr
    }
  }
  '
}

# ── 공개 API ────────────────────────────────────────────────────────────
tag_canon_keys() {
  local mp; mp="$(tag_canon_map_path)"
  [ -r "$mp" ] || mp=""
  tag_canon_extract "$@" | _tag_canon_awk "$mp" keys
  [ -n "$mp" ] || return 3
}

# cluster_freq \t canonical \t aliases  (빈도 desc, 동률이면 canonical 사전순)
tag_canon_groups() {
  local mp; mp="$(tag_canon_map_path)"
  local rc=0
  [ -r "$mp" ] || { mp=""; rc=3; }
  tag_canon_extract "$@" | _tag_canon_awk "$mp" groups "${REFLECT_TAG_MAX_ALIAS:-5}" \
    | sort -t "$(printf '\t')" -k1,1nr -k2,2
  return $rc
}

# raw_distinct \t clusters \t ratio  — 파편화 지표 (reflect-kaizen §0 오라클)
tag_canon_fragmentation() {
  local mp; mp="$(tag_canon_map_path)"
  local rc=0
  [ -r "$mp" ] || { mp=""; rc=3; }
  tag_canon_extract "$@" | _tag_canon_awk "$mp" frag
  return $rc
}
