# Phase 13 (bambu-kit) 계약 초안 검토

- 대상: `.harness/sprint-contract-kaizen-0924-p13-bambu-kit.md` (757 줄, 봉인 전 초안) · 개정 파일은 아직 없다(BUILD 가 만든다)
- 검토: 2026-09-25, 독립 Claude 검토자 — 사용자 승인(5 단계) 대신. 파일은 이 검토 결과 하나만 썼다. 임시 사본은 스크래치 `p13r/` 에만 두었다
- 결론: 고칠 것 넷. 둘은 직접 돌려서 찾은 측정 구멍이다(SC-06 새 확인이 파일 하나를 놓친다 · SK-06 알려진 답이 호 방향 버그를 통과시킨다). 나머지 둘은 문구다(SK-06 줄 수 · DG-06 빈 출력). 모두 작게 고칠 수 있고 조건 수는 늘지 않는다

## 다시 돌려 본 것

- 기준 커밋: 작업 폴더 HEAD 가 아직 `499cc12` 이고 `499cc12..HEAD` 커밋 0 개, `git status --short -- bambu-kit` 0 줄. 배경의 두 주장(`c0e12a8..499cc12` · `82b2493..499cc12` 에서 bambu-kit 을 건드린 커밋 0)을 다시 세어 둘 다 `0`
- 측정 도우미: 계약 `## 회귀 게이트` 의 네 블록을 계약에서 직접 뽑아 초안 쪽 `p13d/k/` 와 비교 — 네 파일 모두 한 글자도 같다. `mock.py` sha256 앞 16 자리 `23dcab88971de152` 도 계약과 같다
- 조건 전부: 뽑은 도우미로 예행 저장소 `p13d/rh-none`(이 초안을 봉인한 판)에서 27 개 ID 를 다시 돌렸다. 출력이 초안의 `p13d/all-none.final.txt` 와 바이트까지 같다(`diff` 빈 출력). 계약의 요구값과도 줄마다 맞다 — SK-06 줄 수 표기 하나만 빼고(아래 3)
- 저장 검사: Step 6.2 두 명령이 `29` · `20`, 6.5 (1)~(3) 위반 0, `[미실측]` 0. 기능 조건 20 은 복잡 9~20 의 위 끝이다 — 아래 고칠 것은 조건을 늘리지 않는다
- 커버리지 검출기: `UNCOVERED` 여섯(SK-01 · ER-01 · ER-03 · AR-01 · AR-02 · RE-01) 모두 `## 범위 경계` 에 해소 줄이 있다
- 설치본: BambuStudio `02.08.02.61` · OrcaSlicer `2.4.2` — 계약에 적힌 값 그대로다

## 처리 배정표 · 범위 · 공유 파일 · 조건끼리

- 배정표에서 `배정` 칸이 `Phase 13` 인 행은 일곱(`F30` · `bambu:P1` ~ `bambu:P6`)이고 전부 배경 표와 조건에 실려 있다. 비고가 이 Phase 를 가리키는 `F16` · `F17` 도 다뤘고, 끝의 적용 힌트 줄(169 행)과도 맞다
- 빈틈 대조 원문(`gapmap.json` `groups[1]` P1 ~ P6)을 항목마다 대조했다. 빠진 것은 둘이고 둘 다 사유가 있다 — 답글 수 세기(배열 이름이 근거 파일에 없다 → 다음 사이클 메모) · P3 (e) `bambu-kaizen` 회귀 줄(`.claude/skills/` 는 이 Phase 범위 밖 → ER-03 넘김). 다만 P3 (c) 는 원문이 「블록 안 `TARGET_SLICER=` 줄」 이라고 적었는데 초안 구현은 파일 전체를 찾는다 — 이 차이가 아래 1 의 구멍이다
- 근거 파일 §3 현행화(`bambu-fields-baseline.md` · `materials.md` 옛 버전 값)를 `/bambu-research` 로 넘긴 것은 `bambu-kaizen` 스킬 설명(「references 갱신은 /bambu-research」)과 Gotcha 1 과 맞다. ER-03 이 notes 의 그 넘김 줄을 잰다
- Phase 1 가이드 변경 전수 점검 표가 있고, `[미검증]` 네 칸은 다섯 자리를 줄 번호로 적어 넘겼다(ER-03 이 `SKILL.md:1706` 과 같은 줄로 잰다)
- 범위: 고치는 여덟 파일이 모두 `bambu-kit/` 안이라 러닝북 표의 고쳐도 되는 범위(`bambu-kit/` · `docs/bambu/`) 안이다. 공유 파일 · `bambu-kit/README.md` · 다른 Phase 폴더는 건드리지 않고 ER-03 넷째 값 · AR-01 이 커밋 기록으로 잰다
- 조건끼리 부딪히는 곳은 찾지 못했다 — SK-07 점검 목록 49 줄과 SK-06 새 줄, AR-02 `len_refs=1/3` 과 SK-06 `next=3`, SC-06 시험 파일 23 개와 RE-01 새 넷(19 + 4), AR-01 `0 8` 과 범위 블록 여덟 줄이 서로 맞는다

## 고칠 것

### 1. SC-06 — 새 「실행 줄에 있나」 확인이 파일 하나를 놓친다 (실측)

음성 대조 블록 (1) 의 확인은 `grep -qF "\"\$GATE\" \$FX/$name" "$S"` 로 SKILL.md **전체**에서 이름을 찾는다. 그런데 이번에 더한 빈 목록 변이 줄
`SKILL_DIR="$EMPTY" TARGET_SLICER=orca python3 "$GATE" $FX/process-bambu-only-key-in-orca.json; echo "exit=$?"` 에도 같은 글자가 들어 있다.
그래서 (2) 의 `process-bambu-only-key-in-orca.json` 실행 줄을 지워도 확인이 통과한다.

- 실측: 예행 끝 판 사본에서 그 (2) 줄만 지우고 초안 블록을 돌리면 `rc=0` · 빠진 이름 출력 없음 · `exit=` 46 줄 — 시험이 하나 빠졌는데 모두 통과로 보인다.
  파일마다 세 보면 이 파일만 `"$GATE" $FX/<이름>` 이 2 번이고 나머지 스물둘은 1 번이다. 계약의 양성 대조(`run`)는 `process-thin-baseline.json` 만 지워 봐서 이 경우를 못 봤다
- 고친 형태 실측: 확인 줄을 `grep -F "\"\$GATE\" \$FX/$name;" "$S" | grep -q '^TARGET_SLICER='` 로 바꾸면 같은 사본에서 bash · zsh 모두
  `실행 줄에 없음 process-bambu-only-key-in-orca.json` · `STOP 표와 실행 줄을 먼저 채운다` · `rc=1` · `exit=` 0 줄. 손대지 않은 판에서는 bash · zsh 모두 `rc=0` 에
  `exits=1111111111011111111110000000000000000000000000` — 초안 값과 같다

같은 조건의 작은 틈 하나: 새로 더한 「소재 칸 알림 줄을 지운 사본」(`$GATE.slotnote`)은 지우기 전에도 종료 코드가 0 이라, 종료 코드 줄만 보면 변이가 효과를 냈는지 알 수 없다.
`mutations` 의 `1` 은 sed 가 한 줄을 바꿨다는 것까지만 보여 준다(다른 칸 알림 줄을 바꿔도 1 이다). 실행 출력에서
`filament-unreadable-slot.json: filament_retraction_length 슬롯 1 을 못 읽었다` 줄을 세면 지금 bash · zsh 모두 `1`(검사 유지 실행에서만 나온다)이고, 변이가 엉뚱한 줄을 바꾸면 `2` 가 된다.

### 2. SK-06 — 알려진 답이 호 방향 버그를 통과시킨다 (실측)

블록 맨 앞 자기 검사의 호는 반원(`G2 X20 Y0 I5 J0`)이고, 둘째 알려진 답(`known2`)의 호는 한 바퀴(`G3 … I0 J5`)다. 둘 다 시계 · 반시계를 바꿔도 길이가 같다.
호 길이 스크립트에서 흔한 실수가 바로 회전 방향이다(F17 「측정 스크립트 자체 버그」 와 같은 종류).

- 실측: 블록의 `sweep = …` 줄을 세 가지로 망가뜨린 사본(둘 다 반시계 · 둘 다 시계 · 서로 바꿈) 모두 `SELFTEST 직선 20.000 · 호 15.708 · 합 35.708` 로 자기 검사를 통과하고,
  `known2` 출력도 원본과 한 글자도 같다. 지금 코드 자체는 맞다 — 1/4 호로 재면 `G3` 15.7 mm · `G2` 47.1 mm 로 방향을 제대로 가린다. 모자란 것은 이를 증명하는 알려진 답이다
- 고친 형태 실측: `KNOWN` 의 반원을 `G2` 1/4 호와 `G3` 1/4 호로 바꾸면(아래 문구) 기대값이 그대로 `직선 20 · 호 15.708 · 합 35.708` 이라 조건의 다른 요구값은 안 바뀐다.
  이 판에서 세 방향 변이는 모두 `FAIL: 알려진 답과 다르다 …` · 종료 코드 1(호 31.416 · 31.416 · 47.124), 기존 호 건너뛰기 변이도 여전히 `FAIL` · `rc=1 selftest=0`,
  원본은 bash · zsh 모두 `known2` 에서 초안과 같은 두 줄(`Outer wall … 76%` · `Sparse infill … 0%`)과 `rc=0 selftest=1`

### 3. SK-06 — 줄 수 표기가 틀렸다

조건과 `회귀 게이트` 표가 「`m SK-06` 열여섯 줄」 이라고 적었지만 나열한 값도 실제 출력도 열일곱 줄이다(`p13d/all-none.final.txt` 의 SK-06 절 17 줄, 이번 재실행도 17 줄).
QA 가 글자 그대로 대조하면 첫 줄부터 어긋난다. 위 2 를 반영하면 스무 줄이 된다.

### 4. DG-06 — 출력이 비어도 통과로 읽힐 수 있다

지금 문구는 「줄이 `FAIL` · `ERROR` 가 아니다」 여서, `validate-post-kaizen.py` 출력 모양이 바뀌어 두 줄이 아예 안 나오면 「아니다」 가 성립한다.
`doc-contracts` 가 실패했을 때의 대체 판정도 `검사:` 줄을 하나도 못 읽으면(`doc_checked=0`) `doc_mine=0` 으로 저절로 통과한다. 요구값이 한 줄도 적혀 있지 않은 유일한 `[exact]` 조건이기도 하다.

## 조건 ID 별 고칠 문구

### SK-06 — 조건 줄 전체를 아래로

```text
- [ ] SK-06: SKILL.md Phase 4.4 에 `**G-code 로 길이 재기 (2026-09-25 신규)**` 문단과 블록이 있어 — 알려진 답(직선 20 · 호 15.708. 호는 `G2` 1/4 호와 `G3` 1/4 호 하나씩이라 회전 방향을 틀리면 값이 바뀐다) 자기 검사를 먼저 하고, 두 기능 · 절대 E · `G92` · `G91` · 한 바퀴 호 · 이동 줄을 섞은 둘째 알려진 답에서 `Outer wall` 직선 0.010 m · 호 0.031 m · 합 0.041 m · 76 % 와 `Sparse infill` 0.007 m · 0 % 를 내고, 기능 표시 0 줄 · R 로 적은 호 · 압출로 센 이동 0 개에서는 각각 `FAIL` · 종료 코드 1 로 멈춘다. 음성 대조: 호를 건너뛰고 좌표도 안 옮기는 사본과 `G2` · `G3` 를 같은 방향으로 센 사본은 둘 다 자기 검사에서 멈춘다. 점검 목록에 G-code 길이 줄 하나가 더해지고, `bambu-kit/skills/bambu-print-profile/references/surface-recipes.md` 의 G-code 실측 세 곳(갭필 표 · 허공 위 표 · 다림질 문단) 바로 뒤에 잰 방법 두 줄 인용이 하나씩, 머리 줄이 바뀐다 (`bambu:P5`) — `m SK-06` 스무 줄이 `1 1` · `Outer wall: 직선 0.010 m · 호 0.031 m · 합 0.041 m · 호 비율 76%` · `Sparse infill: 직선 0.007 m · 호 0.000 m · 합 0.007 m · 호 비율 0%` · `rc=0 selftest=1` · ``FAIL: `; FEATURE: ` 줄이 0 개다 — 뱀부 · 오르카 G-code 가 아니거나 표시가 다르다. 빈 결과는 통과가 아니다`` · `rc=1 selftest=1` · `FAIL: R 로 적은 호는 재지 않는다 — I · J 호만 잰다: G2 X10 Y0 R5 E1` · `rc=1 selftest=1` · `FAIL: 기능 표시는 있는데 압출로 센 이동이 0 개다 — E 모드(M82 · M83)가 맞는지 본다` · `rc=1 selftest=1` · `mutated=1` · `FAIL: 알려진 답과 다르다 — 이 블록부터 고친다. 실제 G-code 는 재지 않았다` · `rc=1 selftest=0` · `mutated_dir=1` · `FAIL: 알려진 답과 다르다 — 이 블록부터 고친다. 실제 G-code 는 재지 않았다` · `rc=1 selftest=0` · `1` · `> Last updated: 2026-09-25 (G-code 실측 세 곳에 잰 방법 · 2026-09-08 §2.7 형상 클래스 축 신설 · 최초 2026-05-16)` · `notes=3 next=3` · `after_ok=3/3` [exact]
```

`m.sh` 의 `SK-06)` 갈래 — `echo "mutated=$(diff "$T/p5.sh" "$T/p5-noarc.sh" …` 줄 바로 뒤에 넣는다:

```bash
    # 음성 대조 — G2 · G3 를 같은 방향(반시계)으로 세는 사본. 반원 · 한 바퀴만 든 알려진 답은 이 사본을 통과시킨다
    sed 's/^            sweep = (start - finish) % (2 \* math.pi) if code == "G2" else (finish - start) % (2 \* math.pi)$/            sweep = (finish - start) % (2 * math.pi)/' "$T/p5.sh" > "$T/p5-dir.sh"
    echo "mutated_dir=$(diff "$T/p5.sh" "$T/p5-dir.sh" | grep -c '^>')"; run5 "$T/p5-dir.sh" "$T/known2.gcode"
```

`mock.py` 684 줄의 `KNOWN` 을 아래로(앞 줄의 까닭 주석은 넣어도 되고 빼도 된다):

```python
# 호는 G2 · G3 1/4 호 하나씩 — 반원이나 한 바퀴는 방향을 틀려도 길이가 같아 못 잡는다
KNOWN = ["M83", "; FEATURE: Outer wall", "G1 X0 Y0", "G1 X10 Y0 E1", "G2 X15 Y5 I5 J0 E1", "G3 X20 Y10 I0 J5 E1", "G1 X30 Y10 E1"]
```

`회귀 게이트` 표 SK-06 행 — 요구값 칸을 「조건 줄의 스무 줄」, 대조 칸 끝에 「· `G2` · `G3` 같은 방향 변이 → 자기 검사 FAIL (초안의 반원 알려진 답으로는 `rc=0 selftest=1` 로 통과했다 — 검토에서 찾은 구멍)」.

### SC-06 — 조건 줄 전체를 아래로

```text
- [ ] SC-06: SKILL.md 음성 대조 절이 시험 파일을 전수로 돈다 — 실행 블록을 끝 판에서 bash · zsh 로 돌리면 같은 출력에 `STOP` 0, 게이트를 뽑은 뒤 줄 수 · `RESULT` 줄 수를 찍고, 종료 코드 순서가 검사 유지 23 줄(FAIL 기대 20 · PASS 기대 3)과 지운 사본 · 변이 23 줄(전부 0)이며, 바뀐 줄 수 열넷이 모두 1 이고 합집합 변이 기준점 1 · 빈 목록 `[미검증]` 1 · 소재 칸 알림 줄 1(검사 유지 실행에서만 나오고 알림 줄을 지운 사본에서는 안 나온다)이다. 폴더의 시험 파일 23 개가 표 23 행과 이름이 같고, 새 넷이 각각 목표 위반 FAIL 하나만 내며 `[미검증]` 0, 「일곱 모두」 문장과 「아직 FAIL 시험 파일이 없다」 문장이 있다. 실행 줄 확인은 `TARGET_SLICER=` 로 시작하는 (2) 줄만 센다. 양성 대조: 실행 줄 하나 뺀 사본 둘(그중 하나는 빈 목록 변이 줄에도 이름이 나오는 `process-bambu-only-key-in-orca.json`) · 표 행 하나 뺀 사본 · 폴더에만 파일을 더한 사본 · 틀린 SKILL.md 경로 사본은 각각 빠진 이름이나 `STOP` 을 찍고 종료 코드 1 로 시험을 하나도 돌리지 않는다 (`bambu:P3` · `bambu:P4`) — `m SC-06` 열네 줄이 `bash_rc=0` · `zsh_rc=0` · `same=1 stop=0 gate_lines= 283 result_lines=1` · `exits=1111111111011111111110000000000000000000000000` · `mutations=1 1 1 1 1 1 1 1 1 1 1 1 1 1 anchor=1 empty_unv=1 slot_note=1` · `table_diff=0` · `fixtures=23 rows=23` · `process-flow-ratio-over:rc=1,fail=1,target=1,unv=0 process-scarf-ratio-over:rc=1,fail=1,target=1,unv=0 filament-retraction-over-parent:rc=1,fail=1,target=1,unv=0 process-elefant-foot-negative:rc=1,fail=1,target=1,unv=0` · `1 1` · `run rc=1 실행 줄에 없음 process-thin-baseline.json|STOP 표와 실행 줄을 먼저 채운다| exits=0` · `run2 rc=1 실행 줄에 없음 process-bambu-only-key-in-orca.json|STOP 표와 실행 줄을 먼저 채운다| exits=0` · `table rc=1 표에 없음 process-flow-ratio-over.json|STOP 표와 실행 줄을 먼저 채운다| exits=0` · `stray rc=1 표에 없음 process-stray.json|실행 줄에 없음 process-stray.json|STOP 표와 실행 줄을 먼저 채운다| exits=0` · `path rc=1 STOP 게이트를 못 뽑았다 — S 경로부터 본다| exits=0` [exact, enumerated]
```

`m.sh` 의 `SC-06)` 갈래 두 곳:

```bash
    # mutations 줄 끝에 소재 칸 알림 줄 수를 붙인다
    echo "mutations=$(grep -xE '[0-9]+' "$T/neg.bash" | tr '\n' ' ')anchor=$(grep -c '^기준점 1 개$' "$T/neg.bash") empty_unv=$(grep -c '목록이 비었거나 깨졌다' "$T/neg.bash") slot_note=$(grep -c 'filament-unreadable-slot.json: filament_retraction_length 슬롯 1 을 못 읽었다' "$T/neg.bash")"
    # 양성 대조 변형에 run2 를 더한다
    for v in run run2 table stray path; do rm -rf "$T/nv"; mkdir -p "$T/nv"; cp -R "$E/bambu-kit" "$T/nv/"
      case $v in
        run)   grep -vxF 'TARGET_SLICER=bambu python3 "$GATE" $FX/process-thin-baseline.json; echo "exit=$?"' "$E/$SK" > "$T/nv/$SK" ;;
        run2)  grep -vxF 'TARGET_SLICER=orca  python3 "$GATE" $FX/process-bambu-only-key-in-orca.json; echo "exit=$?"' "$E/$SK" > "$T/nv/$SK" ;;
```

(`table` · `stray` 갈래와 그 뒤는 그대로.)

`mock.py` 418 줄(SKILL.md 음성 대조 (1) 의 둘째 grep)을 아래 두 줄로:

```bash
  # (2) 의 TARGET_SLICER= 줄만 센다 — 빈 목록 변이 줄에도 같은 이름이 나와 파일 전체를 찾으면 빠진 줄을 못 잡는다
  grep -F "\"\$GATE\" \$FX/$name;" "$S" | grep -q '^TARGET_SLICER=' || echo "실행 줄에 없음 $name"
```

`회귀 게이트` 표 SC-06 행 — 요구값 칸을 「조건 줄의 열네 줄」, 대조 칸의 「뒤 네 줄이 (1) 검사의 양성 대조」 를 「뒤 다섯 줄이 (1) 검사의 양성 대조 — 초안 블록(파일 전체를 찾던 grep)은 `run2` 에서 `rc=0` · `exits=46` 이었다(검토에서 찾은 구멍)」 로.

### DG-06 — 조건 줄 전체를 아래로

```text
- [ ] DG-06: `python3 scripts/validate-post-kaizen.py --since 499cc1289f0f5ae5649da601515725f49f4f1096` 출력에 `scope-isolation` 줄과 `doc-contracts` 줄이 각각 1 개 있고, 둘 다 `FAIL` · `ERROR` 가 아니다(`PASS` · `SKIP` 은 통과). 두 줄 가운데 하나라도 없으면 FAIL 이다. `docs-site-regen` 은 Final F2 몫이라 판정에서 뺀다. 다른 Phase 커밋 때문에 `scope-isolation` 이 `FAIL` 이면 `--verbose` 위반 커밋 목록이 1 개 이상 읽혔고(`violators` 1 이상) 그 안에 이 Phase 서명 커밋이 없을 때(`mine=0`)만 PASS 다. `doc-contracts` 가 `FAIL` · `ERROR` 이면 `python3 scripts/validate-doc-contracts.py -v` 의 `검사:` 줄 경로가 1 개 이상 읽혔고(`doc_checked` 1 이상) 그 가운데 이 Phase 파일이 0 개(`doc_mine=0`)일 때만 PASS 다 — `m DG-06` 네 줄이 `scope-isolation: <상태>` · `doc-contracts: <상태>` · `doc_checked=<1 이상> doc_mine=0` · `violators=<N> mine=0` [exact]
```

`m.sh` 는 바꾸지 않는다 — 지금도 네 줄을 이 모양으로 낸다(예행: `scope-isolation: PASS` · `doc-contracts: PASS` · `doc_checked=2 doc_mine=0` · `violators=0 mine=0`).

### 반영 뒤 BUILD 가 다시 돌릴 것

`mock.py` 가 바뀌므로 봉인 전에 예행 저장소를 다시 만들고 `runall.sh` · `del.sh`(문장 삭제 46) · `ctl.sh`(대조 21) · 예행 변형 다섯을 다시 돌려 표 값을 확인한다.
바꾼 두 줄은 삭제 목록(`dl.txt`)의 토큰이 아니고, SK-06 의 다른 요구값 · ER-02 의 `added=N`(N 은 1 이상이면 된다) · DG-02 `python_parsed=9` 는 이 변경으로 조건을 벗어나지 않는다(위 실측).

## 막지 않는 권고 (고치지 않아도 APPROVE 사유를 해치지 않는다)

- SK-02 는 댓글 첫 페이지 403 만 흉내 낸다. 실제로 막힌 쪽은 `makerworld.com` 도메인이다 — 가짜 `curl` 에 모델 주소 403 모드를 더해 보니 블록이 요청 4 번 뒤 `FAIL design.json 을 JSON 으로 못 읽었다 …` · 종료 코드 1 로 멈췄다. 경우 하나로 더하면 가장 흔한 실패 경로가 측정 안에 들어온다
- 킷 블록들이 임시 파일을 지우지 않는다 — 새 빈 목록 변이의 `$EMPTY` 폴더도 남는다. 이 맥 `/var/folders/…/T/` 에 `gate.*` · `emptylist.*` 등이 1355 개 쌓여 있었다(디스크 여유 1.6 GB). 블록 끝에 `rm -rf "$EMPTY"` 한 줄이면 새로 생기는 몫은 막는다
- `gate_lines=     283` 처럼 macOS `wc -l` 앞 공백이 출력에 그대로 나온다. 고치려면 SC-06 요구값(`gate_lines= 283`)도 함께 바꿔야 하니 이번에는 두는 편이 싸다
- ER-03 넷째 값의 경로 목록에 다른 킷 폴더는 없다. 이 Phase 가 서명 없이 다른 킷을 건드리면 못 잡지만, 넣으면 동시에 도는 다른 Phase 의 서명 누락이 이 조건을 떨어뜨린다 — 지금 선택을 그대로 둬도 된다

VERDICT: CHANGES

## 2 회차

- 대상: 같은 계약 초안(766 줄, 봉인 전) · 개정 파일은 아직 없다. 검토: 2026-09-25, 독립 Claude 검토자. 이 파일에 이 절만 덧붙였고 다른 파일은 고치지 않았다. 임시 사본은 스크래치 `p13r2/` 에만 두었다
- 결론: 1 회차 고칠 것 넷은 모두 반영됐고, 계약이 적은 값을 도우미를 계약에서 새로 뽑아 다시 돌려 한 글자도 같게 얻었다. 새로 하나를 찾았다 — 1 회차가 제안한 SK-06 알려진 답(1/4 호 둘)이 **방향을 아예 안 보는** 호 계산(각도 차의 절댓값)을 통과시킨다. 1 회차 제안에 있던 빈틈이다. 킷에서 한 줄만 바꾸면 되고 기대값(직선 20 · 호 15.708 · 합 35.708)은 그대로다

### 1 회차 고칠 것 반영 확인

| 1 회차 | 계약 초안의 반영 | 다시 돌린 결과 |
| --- | --- | --- |
| 1. SC-06 실행 줄 확인 | 조건 줄 · `m.sh` `run2` 갈래와 `slot_note` · `mock.py` 419 줄(`grep -F … \| grep -q '^TARGET_SLICER='`) · 회귀 게이트 표 SC-06 행 | `m SC-06` 열네 줄이 조건 줄과 같다. 시험 파일 23 개 모두 새 확인에 걸리는 실행 줄이 정확히 1 개다(옛 확인은 `process-bambu-only-key-in-orca.json` 만 2) — 다른 파일로 같은 구멍이 나지 않는다. `rv/extra.sh` 로 `run2` zsh `rc=1` · `exits=0`, 다른 칸 알림 줄을 바꾼 변이 `mutations` 그대로 · `slot_note=2` 를 다시 봤다 |
| 2. SK-06 회전 방향 | `mock.py` 685~686 줄 `KNOWN`(`G2` · `G3` 1/4 호) · `m.sh` `mutated_dir` · 표 SK-06 행 | 뒤집는 변이 셋(둘 다 반시계 · 둘 다 시계 · 서로 바꿈)이 모두 FAIL(호 31.416 · 31.416 · 47.124). 옛 반원 판에서는 셋 다 `rc=0` 이었다 |
| 3. SK-06 줄 수 | 「스무 줄」 | 실제 출력 20 줄 |
| 4. DG-06 빈 출력 | 조건 문구(두 줄이 각각 1 개 · 없으면 FAIL · `violators` 1 이상 · `doc_checked` 1 이상) | `rv/dg6ctl.sh` 두 사본 — 검사 이름 줄을 안 내면 `m DG-06` 이 두 줄, `검사:` 줄을 안 내면 `doc_checked=0` — 새 문구에서 둘 다 FAIL |

### 2 회차에 다시 돌려 본 것

- 기준 커밋: 작업 폴더 HEAD 가 `3a348d6` 으로 올라갔다(`499cc12..HEAD` 커밋 다섯, 모두 Phase 14). 그 다섯 가운데 `bambu-kit/` · `docs/bambu` · `harness/docs/guides/skill-design-guide.md` · `scripts/` 를 건드린 것 0, `git status --short -- bambu-kit` 0 줄 — 기준 `499cc12` 와 시작 판 값은 그대로다. `phase14-notes.md` 에 bambu-kit 로 넘긴 것은 없다
- `mock.py`: sha256 앞 16 자리 `1958e0065c4e3fc2` 가 계약과 같다. 초안 옛 판(`rv/orig/mock.py`)과 다른 곳은 두 자리(419 · 685~686)뿐이다. `499cc12` 의 `bambu-kit/` 를 풀어 새로 적용하니 `mock applied 36` 이고, 그 결과가 예행 저장소 `rh-none` 끝 판의 `bambu-kit/` 와 `diff -r` 빈 출력이다
- 측정 도우미: 계약 `## 회귀 게이트` 의 네 블록을 계약에서 직접 뽑아 `p13d/k/` 와 비교 — 넷 다 바이트 같다. `rh-none` 의 계약은 작업 폴더 계약에 봉인 두 줄(`conditions_digest` · `locked_at`)만 더한 판이다
- 조건 전부: 뽑은 도우미로 `rh-none` 에서 27 개 ID 를 돌렸다. 출력이 초안의 `rv/all-none.rv2.txt` 와 바이트 같고, 1 회차 출력(`all-none.final.txt`)과 다른 줄은 SK-06 세 줄 · SC-06 두 줄 · ER-02 `added=545` 뿐이다 — 계약 663~666 줄의 말 그대로다. 조건 줄 요구값과도 줄마다 맞다. 시작 판(`rh-base`)도 초안 출력과 임시 폴더 이름 밖에서는 같다
- 저장 검사: Step 6.2 두 명령 `29` · `20`, 6.5 (3) `OK conditions=29`, `[미실측]` 0. 커버리지 검출기 `UNCOVERED` 여섯은 1 회차와 같은 조건이고 모두 `## 범위 경계` 에 해소 줄이 있다. SC-06 에 새로 든 `process-bambu-only-key-in-orca.json` 은 측정 쪽에 있어 걸리지 않는다
- 예행 변형 다섯 · 문장 삭제 46 · 대조 21 은 초안 기록(`rv/verify-all.rv.out`)을 읽어 표와 맞췄다 — `DROP 46 NODROP 0`, 변형마다 ER-03 넷째 값 `1`, AR-01 · DG-06 값이 표와 같다
- 작업 폴더에서 `validate-post-kaizen.py --since 499cc12` 는 지금 `scope-isolation: PASS` · `doc-contracts: PASS`(1 블록). `validate-doc-contracts.py -v` 가 읽는 파일은 오케스트레이터 SKILL.md 와 `scripts/collect-kaizen-data.py` 뿐이라 `doc_mine` 은 이 Phase 에서 늘 0 이다

### 새로 찾은 것 — SK-06 알려진 답이 방향을 안 보는 호 계산을 통과시킨다 (실측)

1 회차는 회전 방향을 틀리는 실수를 막으려고 반원을 1/4 호 둘로 바꾸자고 했다. 두 방향을 뒤집거나 한쪽으로 모는 실수는 이제 잡는다.
그런데 **방향을 아예 보지 않고 두 각도 차의 절댓값을 쓰는** 계산(`sweep = abs(finish - start)`, 또는 둘 중 짧은 호를 고르는 계산)은 1/4 호 둘에서 맞는 값과 똑같이 15.708 을 낸다.
두 호가 모두 반원보다 짧아서 짧은 쪽 호가 곧 맞는 호이기 때문이다. 호 길이를 손으로 짤 때 흔한 실수가 이 모양이다(F17 「측정 스크립트 자체 버그」와 같은 종류).

- 실측(끝 판 블록을 뽑아 `sweep` 줄만 바꾼 사본, 스크래치 `p13r2/sk6/`): 절댓값 · 짧은 호 두 변이 모두 `SELFTEST 직선 20.000 · 호 15.708 · 합 35.708` · 종료 코드 0 이고, 둘째 알려진 답 출력도 원본과 글자 그대로 같다.
  이 변이를 `m` 에 넣어 돌리면 `mutated_abs=1` 다음에 `Outer wall …` · `Sparse infill …` · `rc=0 selftest=1` 이 나온다 — 측정이 틀렸는데 통과로 보인다
- 고친 형태 실측: 알려진 답의 호를 `G2` 3/4 호(반지름 2)와 `G3` 1/4 호(반지름 4)로 바꾸면 호 합이 3π + 2π = 5π 라 **기대값 · 킷의 비교 식(`abs(arc_mm - 5 * math.pi)`) · 출력 문구 · `m` 의 `selftest` 대조가 모두 그대로**다.
  반지름을 다르게 한 까닭: 반지름이 같으면 3/4 호와 1/4 호를 서로 바꾼 계산이 같은 합을 낸다. 이 판에서 변이 여섯이 모두 `FAIL` · 종료 코드 1 이다 —
  절댓값 · 짧은 호 9.425, 둘 다 반시계 9.425, 둘 다 시계 28.274, 서로 바꿈 21.991, 중심을 끝점에서 잡음 30.173. 원본은 `rc=0` · 15.708 · 35.708
- 같은 사본에서 `m SK-06` 은 새 세 줄(`mutated_abs=1` · `FAIL: 알려진 답과 다르다 …` · `rc=1 selftest=0`)만 늘고 나머지 스무 줄은 한 글자도 같다. 아래 고친 조건 줄의 요구값 스물셋을 뽑아 실제 출력과 `diff` 하면 빈 출력이다.
  ER-02 `added=545 k02=0 names=0` · DG-02(`rules_up=0` 셋 · `json_ok 4` · `python_parsed=9`) · RE-02 `1 1 1 1` · SK-07 도 바뀌지 않는다 — 한 줄을 한 줄로 바꾸기 때문이다

### 2 회차 고칠 문구

SK-06 조건 줄 전체를 아래로(바뀐 곳: 괄호 안 호 설명 · 음성 대조 문장 · 「스물세 줄」 · `mutated_dir` 세 값 뒤의 새 세 값):

```text
- [ ] SK-06: SKILL.md Phase 4.4 에 `**G-code 로 길이 재기 (2026-09-25 신규)**` 문단과 블록이 있어 — 알려진 답(직선 20 · 호 15.708. 호는 `G2` 3/4 호(반지름 2)와 `G3` 1/4 호(반지름 4)라 회전 방향을 뒤집거나 무시하면 값이 바뀐다) 자기 검사를 먼저 하고, 두 기능 · 절대 E · `G92` · `G91` · 한 바퀴 호 · 이동 줄을 섞은 둘째 알려진 답에서 `Outer wall` 직선 0.010 m · 호 0.031 m · 합 0.041 m · 76 % 와 `Sparse infill` 0.007 m · 0 % 를 내고, 기능 표시 0 줄 · R 로 적은 호 · 압출로 센 이동 0 개에서는 각각 `FAIL` · 종료 코드 1 로 멈춘다. 음성 대조: 호를 건너뛰고 좌표도 안 옮기는 사본, `G2` · `G3` 를 같은 방향으로 센 사본, 방향을 무시하고 각도 차의 절댓값을 쓴 사본은 셋 다 자기 검사에서 멈춘다. 점검 목록에 G-code 길이 줄 하나가 더해지고, `bambu-kit/skills/bambu-print-profile/references/surface-recipes.md` 의 G-code 실측 세 곳(갭필 표 · 허공 위 표 · 다림질 문단) 바로 뒤에 잰 방법 두 줄 인용이 하나씩, 머리 줄이 바뀐다 (`bambu:P5`) — `m SK-06` 스물세 줄이 `1 1` · `Outer wall: 직선 0.010 m · 호 0.031 m · 합 0.041 m · 호 비율 76%` · `Sparse infill: 직선 0.007 m · 호 0.000 m · 합 0.007 m · 호 비율 0%` · `rc=0 selftest=1` · ``FAIL: `; FEATURE: ` 줄이 0 개다 — 뱀부 · 오르카 G-code 가 아니거나 표시가 다르다. 빈 결과는 통과가 아니다`` · `rc=1 selftest=1` · `FAIL: R 로 적은 호는 재지 않는다 — I · J 호만 잰다: G2 X10 Y0 R5 E1` · `rc=1 selftest=1` · `FAIL: 기능 표시는 있는데 압출로 센 이동이 0 개다 — E 모드(M82 · M83)가 맞는지 본다` · `rc=1 selftest=1` · `mutated=1` · `FAIL: 알려진 답과 다르다 — 이 블록부터 고친다. 실제 G-code 는 재지 않았다` · `rc=1 selftest=0` · `mutated_dir=1` · `FAIL: 알려진 답과 다르다 — 이 블록부터 고친다. 실제 G-code 는 재지 않았다` · `rc=1 selftest=0` · `mutated_abs=1` · `FAIL: 알려진 답과 다르다 — 이 블록부터 고친다. 실제 G-code 는 재지 않았다` · `rc=1 selftest=0` · `1` · `> Last updated: 2026-09-25 (G-code 실측 세 곳에 잰 방법 · 2026-09-08 §2.7 형상 클래스 축 신설 · 최초 2026-05-16)` · `notes=3 next=3` · `after_ok=3/3` [exact]
```

`m.sh` 의 `SK-06)` 갈래 — `echo "mutated_dir=$(diff "$T/p5.sh" "$T/p5-dir.sh" …` 줄 바로 뒤에 넣는다:

```bash
    # 음성 대조 — 방향을 무시하고 각도 차의 절댓값을 쓰는 사본. 반원보다 짧은 호만 든 알려진 답은 이 사본을 통과시킨다
    sed 's/^            sweep = (start - finish) % (2 \* math.pi) if code == "G2" else (finish - start) % (2 \* math.pi)$/            sweep = abs(finish - start)/' "$T/p5.sh" > "$T/p5-abs.sh"
    echo "mutated_abs=$(diff "$T/p5.sh" "$T/p5-abs.sh" | grep -c '^>')"; run5 "$T/p5-abs.sh" "$T/known2.gcode"
```

`mock.py` 685~686 줄(주석 한 줄과 `KNOWN`)을 아래로:

```python
# G2 3/4 호(반지름 2) · G3 1/4 호(반지름 4) — 짧은 호만 두면 방향을 무시한 계산이, 반지름이 같으면 두 방향을 바꾼 계산이 같은 합을 내 못 잡는다
KNOWN = ["M83", "; FEATURE: Outer wall", "G1 X0 Y0", "G1 X10 Y0 E1", "G2 X12 Y2 I0 J2 E1", "G3 X16 Y6 I0 J4 E1", "G1 X26 Y6 E1"]
```

`회귀 게이트` 표 SK-06 행 — 요구값 칸을 「조건 줄의 스물세 줄」 로. 대조 칸에 「· 방향 무시(각도 차의 절댓값) 변이 → 자기 검사 FAIL (1/4 호 둘 알려진 답으로는 `rc=0 selftest=1` 로 통과했다 — 2 회차 검토에서 찾은 구멍)」 을 더하고,
「m 밖에서 둘 다 시계 · 서로 바꿈 변이도 돌려 `SELFTEST` 호 31.416 · 47.124 · `rc=1` 이었고」 는 새 알려진 답 값으로 「m 밖에서 둘 다 시계 · 서로 바꿈 · 짧은 호 · 중심을 끝점에서 잡는 변이도 돌려 `SELFTEST` 호 28.274 · 21.991 · 9.425 · 30.173 · `rc=1` 이었고」 로 바꾼다.
계약 148 줄 · 667 줄의 `mock.py` sha256 앞 16 자리도 새 값으로 바꾼다.

### 2 회차 반영 뒤 BUILD 가 다시 돌릴 것

`mock.py` 가 바뀌므로 봉인 전에 예행 저장소를 다시 만들고 `runall.sh` 전부 · `del.sh`(문장 삭제 46, SK-06 다섯 포함) · `ctl.sh` · 변형 다섯을 다시 돌린다. `rv/extra.sh` 는 `KNOWN` 문자열을 확인하는 줄이 있어 새 판에 맞춰 고쳐야 돈다.
기대: 지금 출력과 다른 줄은 SK-06 새 세 줄뿐이다(위 실측). 바꾼 두 줄은 삭제 목록(`dl.txt`)의 토큰이 아니다.
디스크: 이 검토 중 여유가 211 MB 까지 내려간 순간이 있었다(다른 작업 때문이고 곧 1.3 GB 로 돌아왔다). 예행 저장소 하나(약 39 MB)와 `m` 한 번(약 60 MB)을 돌리기 전에 `df -h` 로 본다.

### 2 회차 막지 않는 권고

- DG-06 문구 한 곳: 산문은 `doc_checked` 1 이상을 「`doc-contracts` 가 `FAIL` · `ERROR` 이면」 일 때만 요구하는데, 요구값 줄 `doc_checked=<1 이상> doc_mine=0` 은 상태와 상관없이 요구한다.
  지금은 `doc_checked=2` 라 어느 쪽으로 읽어도 같다. 맞추려면 산문을 「`검사:` 줄 경로가 1 개 이상 읽혔고(`doc_checked` 1 이상) 그 가운데 이 Phase 파일이 0 개다(`doc_mine=0`) — `doc-contracts` 가 `FAIL` · `ERROR` 여도 이것이 맞으면 PASS」 로 적는다
- 1 회차 권고 넷(SK-02 모델 주소 403 · 임시 파일 · `wc -l` 앞 공백 · ER-03 경로 목록)은 반영되지 않았다. 권고라 그대로 둬도 된다. 참고로 이 맥 임시 폴더 `/var/folders/…/T/` 는 지금 항목 2892 개 · 8.3 GB 다

VERDICT: CHANGES
