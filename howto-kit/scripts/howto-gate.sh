#!/bin/sh
# howto-gate.sh — 절차 문서 결정론 게이트 G1~G6. LLM 호출 없는 순수 판정.
#
# 사용:  . howto-kit/scripts/howto-gate.sh
#        howto_gate <절차문서.md>
#
# zsh · bash · sh 에서 동일 출력. 글로빙을 쓰지 않는다 (zsh 는 nomatch 가 기본이라
# 매치 0 건인 glob 이 명령을 통째로 죽인다).
#
# 판정 대상 마커는 howto-kit/references/step-contract.md §문서 모드 렌더링 이 정본이다.
# 마커를 바꾸려면 그 파일과 이 스크립트를 **짝으로** 고친다.

# 종결 동사 — step-contract.md 의 what.verb 열거값과 같아야 한다
HOWTO_VERBS='이동|열기|선택|누르기|입력|체크|토글|저장|다운로드|업로드'

# 말단 액션을 깨는 회피 표현 (G5)
HOWTO_HEDGE='이 섹션에서|해당 항목을|적절히|알아서|관련 메뉴에서|필요에 따라'

# deprecation 주장·근거 토큰 (G4) — 영문과 한국어를 **양쪽 다** 인식한다.
# 기존 킷의 G4 는 영문 [Dd]eprecat 에만 묶여 있어 한국어 1 차 출처를 근거로 인정하지 못했다.
# `삭제` 단독은 넣지 않는다 — "계정을 삭제한다" 같은 정상 액션을 오탐한다 (실측 unsourced_claims=2).
# Google Cloud 한국어 문서가 removed 를 `삭제` 로 옮기므로 좁은 형태만 추가한다 (2026-09-10).
HOWTO_DEP='[Dd]eprecat|[Ss]unset|[Rr]emoved|[Ee]nd of [Ll]ife|EOL|지원 종료|지원종료|폐지|중단|서비스 종료|단종|삭제 예정|삭제가 예정|종료 예정'

# G3 플랫폼 계열 — 선언과 다른 계열의 경로가 섞이면 실패
_howto_fam_declared() {   # _howto_fam_declared <family> <선언문자열>
  case "$1" in
    ios)     printf '%s' "$2" | grep -qiE 'ios|아이폰|iphone|ipad' ;;
    android) printf '%s' "$2" | grep -qiE 'android|안드로이드' ;;
    windows) printf '%s' "$2" | grep -qiE 'windows|윈도우' ;;
    macos)   printf '%s' "$2" | grep -qiE 'macos|mac os|맥' ;;
    *)       return 1 ;;
  esac
}

_howto_fam_pattern() {    # _howto_fam_pattern <family>
  case "$1" in
    ios)     printf '%s' 'appstoreconnect\.apple\.com|Info\.plist|APNs|Xcode|\.p8' ;;
    android) printf '%s' 'play\.google\.com/console|AndroidManifest|google-services\.json|build\.gradle' ;;
    windows) printf '%s' 'Start > Settings|Windows 설정|제어판|regedit' ;;
    macos)   printf '%s' 'System Settings > |시스템 설정 > |Keychain Access' ;;
  esac
}

howto_gate() {
  g=$1
  [ -f "$g" ] || { echo "GATE_BLOCKED no_such_file=$g"; return 0; }
  fail=0

  # 스텝 단위 집계를 awk 한 번에 끝낸다. 헤더 레벨(## / ### / ####)에 종속되지 않는다.
  stats=$(awk -v verbs="$HOWTO_VERBS" -v hedge="$HOWTO_HEDGE" -v dep="$HOWTO_DEP" '
    function after_colon(s,   p) {
      p = index(s, ":"); if (p == 0) return ""
      s = substr(s, p + 1)
      gsub(/^[ \t]+/, "", s); gsub(/[ \t]+$/, "", s)
      return s
    }
    function flush() {
      if (!open) return
      steps++
      if (!f_value)  no_value++
      if (!f_verify) no_verify++
      if (!f_branch) no_branch++
      if (!f_source) no_source++
      if (guess)     n_guess++
      if (!verb_ok)  nonterminal++
      if (hedged)    n_hedge++
      if (dep_claim && !dep_src) dep_unsourced++
      open = 0
    }
    /^##+ S[0-9]+\./ {
      flush(); open = 1
      f_value = f_verify = f_branch = f_source = 0
      guess = verb_ok = hedged = dep_claim = dep_src = 0
      # 헤더 줄도 스캔한다. deprecation 주장은 스텝 요약문에 오는 것이 자연스러운데,
      # 헤더에서 next 로 빠지면 그 주장이 근거 없이 통과한다 (2026-09-08 실측 false negative).
      if ($0 ~ hedge) hedged = 1
      if ($0 ~ dep)   dep_claim = 1
      next
    }
    /^##+ / { flush(); next }
    !open { next }
    {
      if ($0 ~ /\[추정\]/) guess = 1
      # `- 확인:` 은 제품이 화면에 띄우는 문구를 관측해 적는 자리다. 거기 있는 "삭제 예정" 은
      # 저자의 주장이 아니라 근거이므로 주장 탐지에서 뺀다. 안 빼면 데이터 보존 안내
      # ("30일 지난 데이터를 삭제 예정입니다")가 deprecation 주장으로 오탐된다 (2026-09-10 실측).
      # `[추정]` 탐지는 그대로 둔다 — G6 의 등급 비율 계산 대상이다.
      if ($0 !~ /^- 확인:/ && $0 ~ dep) dep_claim = 1
    }
    /^- 값:/       { if (after_colon($0) != "") f_value = 1 }
    /^- 확인:/     { if (after_colon($0) != "") f_verify = 1 }
    /^- 안 보이면:/ { if (after_colon($0) != "") f_branch = 1 }
    /^- 출처:/     { if (after_colon($0) != "") f_source = 1; if ($0 ~ dep) dep_src = 1 }
    /^- 동작:/     { v = after_colon($0); if (v ~ verbs) verb_ok = 1; if (v ~ hedge) hedged = 1 }
    /^- 무엇을:/   { if (after_colon($0) ~ hedge) hedged = 1 }
    END {
      flush()
      # 한 줄에 하나씩 `key=value` 로 낸다. 공백 구분 한 줄로 내고 `set -- $var` 로 받으면
      # zsh 에서 단어분할이 일어나지 않아(SH_WORD_SPLIT 기본 off) 전체가 $1 에 들어가고,
      # 이후 산술 비교가 전부 조용히 실패해 **위반을 PASS 로 흘린다** (2026-09-08 실측).
      printf "steps=%d\nno_value=%d\nno_verify=%d\nno_branch=%d\nno_source=%d\n", \
             steps, no_value, no_verify, no_branch, no_source
      printf "n_guess=%d\nnonterm=%d\nn_hedge=%d\ndep_unsourced=%d\n", \
             n_guess, nonterminal, n_hedge, dep_unsourced
    }
  ' "$g")

  # 값은 전부 awk 의 %d 출력이므로 eval 이 안전하다 (숫자 외에는 들어올 수 없다).
  steps=0; no_value=0; no_verify=0; no_branch=0; no_source=0
  n_guess=0; nonterm=0; n_hedge=0; dep_unsourced=0
  eval "$stats"

  # G1 출처 원장 완전성 — 액션 스텝 수 == 출처 줄 수. 헤더 형식에 종속되지 않는다.
  ledger=$(grep -cE '^- 출처:[[:space:]]*[^[:space:]]' "$g" || true)
  if [ "$steps" -eq 0 ] || [ "$steps" -ne "$ledger" ]; then
    echo "G1_LEDGER FAIL steps=$steps ledger=$ledger"; fail=1
  else
    echo "G1_LEDGER PASS steps=$steps ledger=$ledger"
  fi

  # G2 미검증 마커 분류 — 접미 없는 레거시 0 건 · INVALID 는 정본 임계 미만 (ENV 는 별도 카운터).
  #    임계 상수는 harness/docs/guides/qa-evaluation-guide.md §카운팅 및 자동 REJECT 임계 를
  #    그대로 **구현**한 것이지 이 킷이 새로 정한 값이 아니다. 여기서 먼저 바꾸지 마라.
  bare=$(grep -oF '[미검증]' "$g" | grep -c . || true)
  inval=$(grep -oF '[미검증:INVALID]' "$g" | grep -c . || true)
  envg=$(grep -oF '[미검증:ENV]' "$g" | grep -c . || true)
  if [ "$bare" -ne 0 ] || [ "$inval" -ge 2 ]; then
    echo "G2_MARKER FAIL bare=$bare invalid=$inval env=$envg"; fail=1
  else
    echo "G2_MARKER PASS bare=$bare invalid=$inval env=$envg"
  fi

  # G3 도메인 혼용 — 선언한 플랫폼과 다른 계열의 경로가 섞이면 실패.
  #    선언이 없으면 **PASS 가 아니라 FAIL** 이다. 기존 킷의 G3 는 stack 이 비면 항상 PASS 하는
  #    no-op 이었고, 그래서 3 개월간 아무것도 잡지 못했다.
  decl=$(grep -m1 -E '^- 대상:' "$g" | sed 's/^- 대상:[[:space:]]*//')
  if [ -z "$decl" ]; then
    echo "G3_DOMAINMIX FAIL no_target_declared"; fail=1
  else
    foreign=""; fcount=0
    for fam in ios android windows macos; do
      if _howto_fam_declared "$fam" "$decl"; then continue; fi
      pat=$(_howto_fam_pattern "$fam")
      hit=$(grep -cE "$pat" "$g" || true)
      if [ "$hit" -ne 0 ]; then foreign="$foreign$fam:$hit,"; fcount=$((fcount + hit)); fi
    done
    if [ "$fcount" -ne 0 ]; then
      echo "G3_DOMAINMIX FAIL declared=$decl foreign=${foreign%,}"; fail=1
    else
      echo "G3_DOMAINMIX PASS declared=$decl foreign=0"
    fi
  fi

  # G4 deprecation 근거 결합 — deprecated 를 주장한 스텝의 출처 줄이 그것을 뒷받침해야 한다.
  #    출처보다 강한 주장은 날조다. 영문·한국어 토큰을 양쪽 다 인식한다.
  if [ "$dep_unsourced" -ne 0 ]; then
    echo "G4_DEPRECATION FAIL unsourced_claims=$dep_unsourced"; fail=1
  else
    echo "G4_DEPRECATION PASS unsourced_claims=0"
  fi

  # G5 말단 액션 (신설) — 종결 동사로 끝나지 않거나 회피 표현이 섞인 스텝이 0 건이어야 한다.
  #    이 킷의 존재 이유다. 기존 게이트 어디에도 입도를 재는 검사가 없었다.
  if [ "$nonterm" -ne 0 ] || [ "$n_hedge" -ne 0 ]; then
    echo "G5_TERMINAL FAIL nonterminal=$nonterm hedge=$n_hedge steps=$steps"; fail=1
  else
    echo "G5_TERMINAL PASS nonterminal=0 hedge=0 steps=$steps"
  fi

  # G6 입도 완전성 (신설) — 값·확인·안 보이면·출처가 빠진 스텝 0 건, 추정 비율 40% 이하.
  #    steps 가 0 이어도 0 으로 나누지 않는다.
  if [ "$steps" -gt 0 ]; then
    gpct=$(( n_guess * 100 / steps ))
  else
    gpct=0
  fi
  if [ "$no_value" -ne 0 ] || [ "$no_verify" -ne 0 ] || [ "$no_branch" -ne 0 ] \
     || [ "$no_source" -ne 0 ] || [ "$gpct" -gt 40 ]; then
    echo "G6_GRANULARITY FAIL steps=$steps no_value=$no_value no_verify=$no_verify no_branch=$no_branch no_tier=$no_source guess=$n_guess guess_pct=$gpct"
    fail=1
  else
    echo "G6_GRANULARITY PASS steps=$steps no_value=0 no_verify=0 no_branch=0 no_tier=0 guess=$n_guess guess_pct=$gpct"
  fi

  [ "$fail" -eq 0 ] && echo GATE_PASS || echo GATE_FAIL
  return 0
}
