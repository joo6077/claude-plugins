---
name: howto-audit
description: >
  이미 존재하는 절차 문서·안내문·런북을 입도·출처·네비게이션 기준으로 재측정해 PASS/FAIL
  리포트를 만든다. 결정론 게이트 G1~G6 을 돌린 뒤 howto-reviewer 에이전트로 독립 평가한다.
  문서를 수정하지 않는다.
  "절차 문서 검수", "가이드 감사", "안내문 재측정", "절차 품질 검사", "howto audit"
  같은 요청에 트리거한다.
  새 절차를 지금 알려 달라는 요청에는 트리거하지 않는다 — howto 를 쓴다.
  절차를 새 파일로 만들어 달라는 요청에도 트리거하지 않는다 — howto-doc 을 쓴다.
  코드 품질 감사에는 트리거하지 않는다 — 각 스택 킷의 audit 스킬이 우선한다.
argument-hint: "[문서 경로 또는 디렉토리] 예: 'docs/setup/' 또는 'docs/setup/fcm-ios.md'"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Agent
---

이미 나간 절차 문서를 **다시 잰다.** 고치지 않는다 — 판정과 근거만 낸다.

## 왜 필요한가

절차 문서는 영속 아티팩트다. 규칙이 바뀌면 어제 만든 문서가 **조용히 위반 상태가 된다.**
실측: 한 킷의 쇼케이스 예제가 자기 evals 6 중 3 을 3 개월간 위반한 채 배포돼 있었다.
규칙과 evals 는 고쳤는데 **이미 나간 산출물을 다시 재는 경로가 없었다.**

이 스킬이 그 경로다.

## Gotchas

### Gotcha 1: 대상 범위의 크기부터 출력한다

"위반 0 건"은 통과가 아니다. **빈 범위도 0 건으로 보인다.** 판정 전에 몇 개 파일을 검사하는지
숫자로 먼저 낸다.

```bash
find <대상> -type f -name '*.md' | wc -l
```

이 숫자가 0 이면 판정이 아니라 범위 오류다.

### Gotcha 2: 글로빙 대신 `find` 를 쓴다

zsh 는 `nomatch` 가 기본이라 매치 0 건인 글로브가 **명령을 통째로 죽인다.**
`2>/dev/null` 로는 못 막는다 — 글로빙 확장은 명령 실행 **전에** 일어난다.
bash 에서만 테스트하면 이 결함이 안 잡힌다.

### Gotcha 3: 게이트 출력을 요약하지 말고 그대로 붙인다

"대부분 통과" 같은 요약은 증거가 아니다. 파일별 7 줄 출력을 그대로 리포트에 싣는다.

### Gotcha 4: 게이트가 못 잡는 축을 에이전트에 넘긴다

게이트는 기계 판정 가능한 것만 잡는다 — 마커 존재, 개수 대조, 비율. 잡지 못하는 것은:

- 경로가 **실제로 그 화면에 있는가** (날조 탐지)
- 딥링크가 **살아 있는가**
- 분기 사유가 그 절차에 **말이 되는가**
- 요청 범위 밖의 절차가 섞여 있는가

이 축은 `howto-reviewer` 에이전트가 읽기 전용으로 판정한다.

### Gotcha 5: 고치지 마라

이 스킬은 `Write` 를 갖지 않는다. 수정이 필요하면 판정 리포트를 내고 `howto-doc` 으로
넘긴다. 감사자가 자기 감사 대상을 고치면 그 감사는 증거가 아니다.

### Gotcha 6: 게이트 함수는 자식 셸로 넘어가지 않는다

셸 함수는 그 함수를 읽은 셸 안에서만 보인다. 부모 셸에서 `howto-gate.sh` 를 읽고
`find -exec sh -c` 안에서 `howto_gate` 를 부르면 파일마다 `command not found` 만 나온다.
그래서 Phase 2 는 스크립트를 `sh -c` **안에서** 읽는다. `export -f` 로 넘기지 마라 — macOS 의
`sh` · bash 자식에게만 넘어가고 우분투의 `sh`(dash) · zsh 자식에게는 안 넘어간다.

스크립트 경로를 `howto-kit/scripts/` 로 시작하는 상대 경로로 쓰지 않는다. 킷을 플러그인으로 설치한
프로젝트에는 그 폴더가 없다. Phase 2 블록은 플러그인 설치 경로(`CLAUDE_PLUGIN_ROOT` 치환) → git 최상위
폴더의 `howto-kit/` → 마켓플레이스 설치본 순으로 `test -f` 해서 처음 있는 경로를 쓴다.

실측(2026-09-24): 부모 셸에서 읽고 자식 셸에서 부르던 옛 Phase 2 블록을 시험 입력 15 개에 돌리면
`command not found` 가 15 줄, `GATE_PASS` · `GATE_FAIL` · `GATE_BLOCKED` 줄이 0 줄이었고 `find` 는
종료 코드 1 로 끝났다.

## Process

### Phase 1: 범위 확정 (Gotcha 1)

대상 파일 수를 먼저 출력한다. 사용자가 디렉토리를 줬으면 재귀 탐색하고, 절차 문서가 아닌
파일(README, 설계 문서)이 섞여 있으면 제외 사유와 함께 목록에서 뺀다.

### Phase 2: 게이트 전수 실행

```bash
GATE="${CLAUDE_PLUGIN_ROOT}/scripts/howto-gate.sh"
[ -f "$GATE" ] || GATE="$(git rev-parse --show-toplevel 2>/dev/null)/howto-kit/scripts/howto-gate.sh"
[ -f "$GATE" ] || GATE=$(find "$HOME/.claude/plugins/marketplaces" -maxdepth 4 -type f \
  -path '*/howto-kit/scripts/howto-gate.sh' 2>/dev/null | head -1)
if [ -n "$GATE" ] && [ -f "$GATE" ]; then
  echo "RESOLVED: $GATE"
  find <대상> -type f -name '*.md' -exec sh -c '
    . "${1}"; shift
    for f in "$@"; do echo "### $f"; howto_gate "$f"; done
  ' sh "$GATE" {} +
else
  echo "MISSING: howto-gate.sh tried=${CLAUDE_PLUGIN_ROOT}/scripts · $(git rev-parse --show-toplevel 2>/dev/null)/howto-kit/scripts · $HOME/.claude/plugins/marketplaces"
  false
fi
```

파일별 출력을 그대로 수집한다. 첫 줄이 `MISSING:` 이면 게이트를 돌리지 못한 것이다 — 판정을 내지 말고
그 줄을 그대로 보고하고 멈춘다. `### <경로>` 줄 수와 `GATE_PASS` · `GATE_FAIL` · `GATE_BLOCKED` 줄 수가
Phase 1 의 파일 수와 셋 다 같아야 한다. 다르면 판정이 아니라 실행 오류다 (Gotcha 6).
`find` 의 종료 코드로 판정하지 마라 — `howto_gate` 는 판정과 무관하게 0 을 돌려준다.
`MISSING:` 으로 멈출 때는 `[미검증:ENV]` 에 네 칸을 붙인다 — 막는 것(그 `MISSING:` 줄) · 시도한 우회(`tried=` 의 세 곳) ·
통제 불가 사유(한 문장) · 재검증 명령(킷을 설치하거나 킷이 든 저장소 안에서 이 블록을 다시 돌린다).

### Phase 3: 에이전트 독립 평가

`Agent` 도구로 `howto-reviewer` 를 호출한다. 전달 내용: 대상 파일 경로 목록 + Phase 2 의
게이트 출력. **판정 결론을 미리 알려주지 마라** — 편향된다.

### Phase 4: 리포트

```text
검사 범위:  <N> 파일
스크립트:   <Phase 2 첫 줄의 RESOLVED: 줄 그대로>
게이트:     GATE_PASS <a> / GATE_FAIL <b> / GATE_BLOCKED <c>
에이전트:   PASS <x> / FAIL <y>

파일별 판정
  <경로>  게이트=<판정>  에이전트=<판정>  주된 사유=<한 줄>

전문 출력
  (파일별 7 줄 게이트 출력 그대로)
```

FAIL 이 1 건이라도 있으면 리포트 결론은 FAIL 이다. "대체로 양호" 같은 중간 판정은 없다.

## 관련 스킬

- `howto` — 대화창 즉답으로 절차를 안내한다.
- `howto-doc` — 절차를 MD 문서로 만들고 게이트를 돌린다.

## References

- `../../references/step-contract.md` — Step Contract 스키마 정본
- `../../references/source-tiers.md` — 출처 등급 판정 기준
- `../../scripts/howto-gate.sh` — 게이트 G1~G6 구현
