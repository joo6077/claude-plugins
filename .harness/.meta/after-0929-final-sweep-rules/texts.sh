#!/usr/bin/env bash
# texts.sh <레포 폴더> — 문장 조건을 글자 그대로 세어 `이름=값` 한 줄에 하나씩 찍는다. 글로빙을 쓰지 않는다.
# 절 안 세기는 awk 로 절 머리부터 다음 절 머리 앞까지 자른 뒤 센다 (파일 전체를 세면 손대기 전부터 있던 글자로 통과한다).
# shellcheck disable=SC2016  # 역따옴표는 찾을 글자 그대로다
r=${1:?레포 폴더}
cd "$r" || exit 2
c() { grep -cF -- "$2" "$1"; }                        # c <파일> <글자> — 글자가 든 줄 수
sec() { awk -v a="$2" -v b="$3" 'index($0,a)==1{p=1} p&&index($0,b)==1&&!index($0,a){exit} p' "$1"; }  # sec <파일> <시작 머리> <끝 머리>
hsec() { awk -v a="$2" -v b="$3" 'index($0,a){p=1} p&&index($0,b)&&!index($0,a){exit} p' "$1"; }         # html 절 — 머리가 줄 가운데에 있다
both() { grep -F -- "$1" | grep -cF -- "$2"; }        # stdin 에서 두 글자가 한 줄에 함께 든 줄 수

SS=onboarding-kit/skills/setup-guide/references/search-strategy.md
SH=docs/onboarding-kit/search-strategy.html
EV=onboarding-kit/skills/setup-guide/evals/evals.json
echo "ss_old=$(c $SS '`.p8` 을 권장한다는 사실로부터')"
echo "ss_new=$(c $SS '`.p8` 을 안내한다는 사실로부터 `.p8` 권장이나 `.p12` 의 deprecation 을')"
echo "sh407_old=$(c $SH '<code>.p8</code>을 권장한다는 사실로부터')"
echo "sh407_new=$(c $SH '<code>.p8</code>을 안내한다는 사실로부터 <code>.p8</code> 권장이나 <code>.p12</code>의 deprecation을')"
echo "sh474_old=$(c $SH '<li><code>.p8</code> 권장 &rarr; <code>.p12</code> deprecated로 승격')"
echo "sh474_new=$(c $SH '<li><code>.p8</code> 안내를 <code>.p8</code> 권장 · <code>.p12</code> deprecated로 부풀림 (출처보다 강한 주장)</li>')"
echo "repo_p8_recommend=$(git grep -nE '\.p8.{0,20}(을|를) ?권장한다' -- . ':!.harness' ':!docs/kaizen/research-log.md' | grep -c .)"
echo "ev_old=$(c $EV 'Firebase 문서는 APNs 인증 키 업로드만 지시하고')"
echo "ev_new=$(c $EV 'Firebase iOS 설정 문서는 APNs 인증 키 업로드만 지시하고')"
echo "ev_json=$(python3 -c 'import json,sys; json.load(open(sys.argv[1],encoding="utf-8")); print("ok")' $EV 2>&1)"

DM=design-kit/skills/design-mockup/SKILL.md
DP=docs/design-kit/design-mockup.html
echo "dm201_old=$(c $DM '개수 상한·부대 산출물 금지·사용자 보고 규약의 정본')"
echo "dm201_new=$(c $DM '§5.6 Variant Budget · §3.8 User-Reported Failure Gate — 개수 규칙·부대 산출물 금지·사용자 보고 규약의 기준 원본')"
echo "dm_six_css=$(awk 'index($0,"틀은 시안 칸 A~E 다섯을 기본으로 둔다."){p=1} p&&/^$/{exit} p' $DM | grep -c 'CSS')"
echo "dp_six_css=$(grep -F '<strong>여섯째 시안부터:</strong>' $DP | grep -c 'CSS')"

SG=harness/docs/guides/skill-design-guide.md
SGH=docs/harness/skill-design-guide.html
echo "sg_old=$(c $SG '— 4 개 이상도, 3 축 변주도')"
echo "sg_new=$(c $SG '— 시안 밖 산출물의 4 개 이상도, 3 축 변주도')"
echo "sgh_old=$(c $SGH '— 4 개 이상도, 3 축 변주도')"
echo "sgh_new=$(c $SGH '— 시안 밖 산출물의 4 개 이상도, 3 축 변주도')"

BS=bambu-kit/skills/bambu-print-profile/SKILL.md
BH=docs/bambu-kit/bambu-print-profile.html
echo "bs_row=$(grep -F '| `evals/gate-fixtures/process-thin-unreadable-slot.json` | bambu |' $BS | grep -c .)"
echo "bs_row_unv1=$(grep -F '| `evals/gate-fixtures/process-thin-unreadable-slot.json` | bambu |' $BS | grep -cF '`[미검증]` 1 줄 (슬롯 1)')"
echo "bs_row_wall=$(grep -F '| `evals/gate-fixtures/process-thin-unreadable-slot.json` | bambu |' $BS | grep -cF '벽 예산 미기록')"
echo "bh_row_unv1=$(grep -F '<tr><td><code>process-thin-unreadable-slot.json</code></td>' $BH | grep -cF '<code>[미검증]</code> 1 줄 (슬롯 1)')"
echo "bh_row_wall=$(grep -F '<tr><td><code>process-thin-unreadable-slot.json</code></td>' $BH | grep -cF '벽 예산 미기록')"
echo "fx_key=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1],encoding="utf-8")).get("_wall_budget_short_share"))' bambu-kit/evals/gate-fixtures/process-thin-unreadable-slot.json 2>&1)"

CS=harness/references/contract-schema.md
CH=docs/harness/contract-schema.html
L1='원문 대조 계약은 항목마다 「레포 전체에서 같은 주장」 줄을 둔다.'
L2='설치본이 있어야 도는 검사는 설치본을 지운 사본으로도 잰다.'
L3='경로 목록을 따옴표 없는 변수로 넘기지 않는다.'
MS=$(sec $CS '#### 측정 관례' '#### ')
MH=$(hsec $CH 'id="measure-habits"' '<h3')
echo "cs_l1=$(printf '%s\n' "$MS" | both "**$L1**" 'git grep') cs_l2=$(printf '%s\n' "$MS" | both "**$L2**" '슬라이서') cs_l3=$(printf '%s\n' "$MS" | grep -F "**$L3**" | grep -F 'xargs' | grep -cF '배열')"
echo "cs_file_l1=$(c $CS "$L1") cs_file_l2=$(c $CS "$L2") cs_file_l3=$(c $CS "$L3")"
echo "ch_l1=$(printf '%s\n' "$MH" | both "<strong>$L1</strong>" 'git grep') ch_l2=$(printf '%s\n' "$MH" | both "<strong>$L2</strong>" '슬라이서') ch_l3=$(printf '%s\n' "$MH" | grep -F "<strong>$L3</strong>" | grep -F 'xargs' | grep -cF '배열')"
echo "ch_file_l1=$(c $CH "$L1") ch_file_l2=$(c $CH "$L2") ch_file_l3=$(c $CH "$L3")"
echo "sec_lines md=$(printf '%s\n' "$MS" | grep -c .) html=$(printf '%s\n' "$MH" | grep -c .)"
