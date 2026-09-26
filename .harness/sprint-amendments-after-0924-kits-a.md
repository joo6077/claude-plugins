---
slug: after-0924-kits-a
created: "2026-09-26 12:57"
---

# after-0924-kits-a 개정

봉인된 조건 줄은 고치지 않았다. 교차 진단(BLOCKING 1)이 짚은 파일이 AR-01 기대 집합 밖이라 그 집합에 한 경로를 더하고(AM-01),
더한 경로와 함께 고친 곳이 제대로 바뀌었는지 재는 측정을 새로 둔다(AM-02).

교차 진단 요지: 이 묶음은 Makefile 에 그 단계의 타겟이 있을 때만 `make` 를 쓰게 바꿨다(`project-detection.md` Step 2b 4 번 · `flutter-ai-rules.md:115`).
두 문장 모두 flutter-preflight 를 이름으로 가리키는데, flutter-preflight Gotcha(`SKILL.md:18`)는 「`Makefile` 존재 확인 후 `make` 커맨드를 우선 사용하라」 를 그대로 적고 있었다.
`app-preflight` 묶음 타겟만 있는 Makefile 에서 이 문장을 따르면 `make app-test` 가 종료 코드 2 로 멈춘다. SK-07 이 소비자를 둘(flutter-run · flutter-ai-rules)만 세어 이 파일이 빠졌다.

## AM-01 — relaxing

- 대상 조건: AR-01
- 변경: 측정 도우미의 `ALLOWED` 에 `flutter-toolkit/skills/flutter-preflight/SKILL.md` 한 경로를 더해 읽는다(스무 경로 → 스물한 경로). 나머지(네 킷 각 1 이상 · `multi_top=0`)는 그대로다.
  재는 법: 도우미를 source 한 뒤 `ALLOWED="$ALLOWED"$'\n''flutter-toolkit/skills/flutter-preflight/SKILL.md'` 로 다시 정하고 `m AR-01`.
- direction 계산: 허용 집합 헬퍼 `amend_direction`(contract-schema §Amendment 사이드카 그대로)에 원 집합 스무 줄 · 개정 집합 스물한 줄을 넣은 출력 `relaxing added=1 removed=0`.
  원 오라클로 재면 끝점 `7799a5a` 에서 `extra=1`(남는 경로 `flutter-toolkit/skills/flutter-preflight/SKILL.md`), 개정 오라클로 재면 `extra=0` — FAIL→PASS 라 relaxing 이 맞다.
- consent: anchored
- 근거 (redaction 거친 원문): 「사용자 지시(2026-09-26T01:04:21Z)대로 A·B·C 를 묻지 말고 전부 실행한다」 · 「C: … 묶음마다 계약 → 구현 → QA → 교차 진단을 거치고」.
  교차 진단이 찾은 결함을 고치는 일까지 위임 범위로 읽었다. 위임은 일반 지시이지 이 경로를 콕 집은 동의가 아니다 — 판정은 평가자 몫이다.
- 앵커: reflect-kit prompt 로그 `~/.claude/logs/claude-plugins/2026-09.md` 86355 줄 `## [prompt] 2026-09-26T11:13:38+0900` · session=`bda55d45-296c-491f-89ba-b52042d58e72` · cwd=`/Users/jackson/Hub/10_Dev/claude-plugins`
  (인용 두 줄은 같은 파일 86371 · 86374 줄). 세션 기록 `bda55d45-….jsonl` 의 같은 입력은 `timestamp 2026-09-26T02:13:37.863Z` · `origin.kind=human`.
  이 개정을 담은 구현 커밋 `4dedb85`(2026-09-26T12:55:25+09:00)보다 앞선다.

## AM-02 — narrowing

- 대상 조건: SK-07(flutter-preflight · flutter-run) · SK-01(widget-inspector) · SC-03(infra-test) — 새 측정을 더한다. 원 조건의 측정은 그대로 둔다
- 변경: 아래 `am02` 가 끝점에서 다음 값을 내야 한다. 원 조건에 없던 요구를 더하므로 통과하는 구현이 줄어든다.
  - `pre_old=0 pre_run=0 pre_ptr≥1` — flutter-preflight `## Gotchas` 에서 옛 문장 · `make app-run` 이 0 이고, `Step 2b` · `app-test` · `기본 명령` 을 함께 담은 줄이 1 이상
  - `run_old=0 run_ptr≥1` — flutter-run Gotcha 의 `make app-run` 도 `app-run` 타겟이 있을 때만(`Step 2b` 를 가리킨다)
  - `wi_cell≥1 wi_tpl≥1` — widget-inspector §7 칸 값 문장이 표를 받은 경우로 한정되고, 리포트 틀이 표 없는 두 줄을 담는다
  - `it_parse=0 it_row_exit1=0 it_row_rc2≥1` — infra-test checkout rule 오류 문구에 「파싱」 이 없고, 「빼면 안 되는 것」 표의 `CORE_TOOLS` 줄이 exit 1 대신 종료 코드 2 를 적는다
  - `nocore_nopy=1/2 nocore_py=1/0 core_py_nogrep=1/2` (`py_yaml=있음` 일 때) — 그 표 줄이 말하는 동작을 실제로 돌린 값. 사전 검사를 뺀 사본은 grep · python3 가 없으면 `checkout 스텝 없음` 을 오보하고 종료 코드 2, python3 · PyYAML 만 있으면 PASS · 0. 원본은 grep 만 없어도 종료 코드 2 로 멈춘다
- direction: narrowing (새 요구를 더한다. 측정 집합을 줄이지 않는다)
- consent: unanchored 로도 PASS 근거가 된다 — 앵커는 AM-01 과 같다
- 근거: 교차 진단 BLOCKING 1 과 「판정은 안 바꾸지만 확인된 작은 문제」 셋(widget-inspector 문구 · infra-test 표 줄 · 「파싱」), 같은 모양의 flutter-run `:22`
- 앵커: AM-01 과 같다
- 봉인 뒤 실측: 고치기 전 끝점 `224abe4` 에서 `pre_old=1 pre_run=1 pre_ptr=0 run_old=1 run_ptr=0 wi_cell=0 wi_tpl=0` ·
  `it_parse=1 it_row_exit1=1 it_row_rc2=0 py_yaml=있음 nocore_nopy=1/2 nocore_py=1/0 core_py_nogrep=1/2` (양성 대조 — 앞 열 값이 모두 살아 있다),
  고친 끝점 `7799a5a` 에서 `pre_old=0 pre_run=0 pre_ptr=1 run_old=0 run_ptr=1 wi_cell=1 wi_tpl=1` · `it_parse=0 it_row_exit1=0 it_row_rc2=1 py_yaml=있음 nocore_nopy=1/2 nocore_py=1/0 core_py_nogrep=1/2`.
  끝의 세 동작 값은 스크립트를 바꾸지 않았으니 두 판이 같고, 고친 것은 그 동작을 적는 표 줄이다

부르기: `bash -c 'source "$TMPDIR/kitsa-measure.sh" || exit 2; source "$TMPDIR/am02.sh" || exit 2; am02'` (`am02.sh` 는 아래 블록을 뗀 것)

```bash
# === AM-02 측정 시작 ===
# 쓰는 법: 계약의 측정 도우미를 source 한 뒤 이 블록을 source 하고 `am02`. bash 에서 부른다.
am02() {
  local p="$FT/skills/flutter-preflight/SKILL.md" r="$FT/skills/flutter-run/SKILL.md" wi="$FT/agents/widget-inspector.md"
  local g rg s7 tpl
  g=$(sec '## Gotchas' '# Preflight' "$p"); rg=$(sec '## Gotchas' '## 0.' "$r")
  s7=$(sec '### 7. 관례 대조' '## Process' "$wi"); tpl=$(sec '## Process' '## Gotchas' "$wi")
  echo "pre_old=$(printf '%s\n' "$g" | n '`Makefile` 존재 확인 후 `make` 커맨드를 우선 사용하라')" \
    "pre_run=$(printf '%s\n' "$g" | n 'make app-run')" \
    "pre_ptr=$(printf '%s\n' "$g" | grep -F 'Step 2b' | grep -F 'app-test' | n '기본 명령')" \
    "run_old=$(printf '%s\n' "$rg" | n 'Makefile 기반 monorepo 에서는 `fvm flutter run`')" \
    "run_ptr=$(printf '%s\n' "$rg" | grep -F 'make app-run' | grep -F 'Step 2b' | n '`app-run` 타겟이 있으면')" \
    "wi_cell=$(printf '%s\n' "$s7" | n '표를 넘겨받았으면 칸마다')" \
    "wi_tpl=$(printf '%s\n' "$tpl" | grep -F '건너뜀 — 관례 표 없는 호출' | n '[미검증] 관례 표 없음')"
  # infra-test — 파싱 낱말 · 표 줄 · 표가 말하는 동작을 실제로 돌려 본다
  local it="$E/infra-kit/skills/infra-test/SKILL.md" row py
  row=$(grep -F '| 핵심 도구 사전 검사 (`CORE_TOOLS`) |' "$it")
  infra_script
  awk '/^for t in \$CORE_TOOLS; do$/{skip=3} skip>0{skip--;next} {print}' "$T/ci-validation.sh" > "$T/ci-nocore.sh"
  mkdir -p "$T/am-wf"; printf 'on: push\njobs:\n  b:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@8f4b7f84864484a7bf31766abe9204da3cbe65b3\n' > "$T/am-wf/w.yml"
  py=$(command -v python3)
  mkdir -p "$T/am-bash" "$T/am-bashpy"; ln -sf "$(command -v bash)" "$T/am-bash/bash"; ln -sf "$(command -v bash)" "$T/am-bashpy/bash"; ln -sf "$py" "$T/am-bashpy/python3"
  local o1 rc1 o2 rc2 o3 rc3
  o1=$(PATH="$T/am-bash" WF_DIR="$T/am-wf" bash "$T/ci-nocore.sh" 2>&1); rc1=$?
  o2=$(PATH="$T/am-bashpy" WF_DIR="$T/am-wf" bash "$T/ci-nocore.sh" 2>&1); rc2=$?
  o3=$(PATH="$T/am-bashpy" WF_DIR="$T/am-wf" bash "$T/ci-validation.sh" 2>&1); rc3=$?
  echo "it_parse=$(n 'YAML 파싱 실패 (checkout rule)' <"$it")" \
    "it_row_exit1=$(printf '%s\n' "$row" | n 'exit 1 로 끝난다')" \
    "it_row_rc2=$(printf '%s\n' "$row" | grep -F 'python3 · PyYAML 이 없어' | n '종료 코드는')" \
    "py_yaml=$("$py" -c 'import yaml' >/dev/null 2>&1 && echo 있음 || echo 없음)" \
    "nocore_nopy=$(printf '%s\n' "$o1" | n 'checkout 스텝 없음')/$rc1" \
    "nocore_py=$(printf '%s\n' "$o2" | n 'checkout 존재')/$rc2" \
    "core_py_nogrep=$(printf '%s\n' "$o3" | n "핵심 도구 'grep' 미설치")/$rc3"
}
# === AM-02 측정 끝 ===
```
