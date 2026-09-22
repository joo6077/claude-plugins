---
slug: cross-diagnosis-to-parent
created: "2026-09-22 15:49"
---

## A-01 — AR-04 (iv) 허용 목록에 앞 스프린트 계약 파일 1개 추가

**앵커**: AR-04 측정 (iv) — "`.harness/` 로 시작하는 줄 중 이 스프린트 산출물 3개
(`sprint-contract-cross-diagnosis-to-parent.md` ·
`sprint-feedback-cross-diagnosis-to-parent.md` ·
`sprint-amendments-cross-diagnosis-to-parent.md`) 를 뺀 나머지 0행"

**무엇이 달라졌나**: 허용 집합에 `.harness/sprint-contract-validate-check-count-sync.md` 를
더한다. 그 파일은 앞 스프린트 계약이고, 이 구간에 들어온 변경은 `status: active → done`
**한 줄**이다.

**왜 이번 스프린트의 산출물이 아닌가**: 그 전환은 앞 스프린트의 qa-evaluator 가 APPROVE
시점에 수행하는 정상 동작이다 (`qa-evaluator.md` Step 5.5 · `contract-schema.md` §status 해석
규칙 — 계약을 `done` 으로 바꾸는 주체는 평가자다). 이번 스프린트가 만든 변경이 아니고,
봉인된 조건 줄도 건드리지 않았다(`SEAL_OK` 확인). AR-04 의 취지는 "과거 기록을 고치지
않았다" 인데 이 전환은 기록을 고치는 것이 아니라 기록이 스스로 완료를 표시하는 것이다.

**왜 하한을 바꾸는 대신 허용 목록을 넓혔나**: AR-04 의 하한 `ab396f2` 는 봉인된 값이다.
앞 스프린트 커밋이 이미 그 해시이고, status 전환은 그 뒤에 일어났으므로 어떤 구간을 잡아도
이 파일은 들어온다. 하한을 움직이면 AR-01 과 어긋나므로 허용 목록 쪽을 고쳤다.

**amend_direction**: `relaxing added=1 removed=0` — 집합 비교로 계산했다.
원 허용 집합 3개 → 개정 4개. 자기신고가 아니라 계산값이다.

**consent**: `anchored` — 세션 `f5b7f3a5-c03d-452b-b44b-fc3d15dcd1a0`.
사용자에게 세 선택지(개정으로 허용 / status 되돌리기 / AR-04 FAIL 받기)를 제시하고
"개정으로 한 개 허용" 을 받았다. 되돌리는 쪽은 APPROVE 된 스프린트를 `active` 로 남겨
기록을 거짓으로 만들기 때문에 택하지 않았다.

**앵커 (검증 가능한 형태)** — 세션 기록
`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/f5b7f3a5-c03d-452b-b44b-fc3d15dcd1a0.jsonl`
의 `AskUserQuestion` 호출·답변 쌍이다.

| 항목 | 값 |
| --- | --- |
| 질문 `header` | `AR-04` |
| 호출 시각 | `2026-09-22T06:48:58.556Z` (KST 15:48:58) |
| 답변 시각 | `2026-09-22T06:49:14.987Z` (KST 15:49:14) |
| 구현 커밋 | `cb39d89` — KST 15:49:57 |

동의가 커밋보다 **43 초 앞선다.** 순서는 올바르다.

재현 명령:

```bash
S=~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/f5b7f3a5-c03d-452b-b44b-fc3d15dcd1a0.jsonl
grep -o '"name":"AskUserQuestion".\{0,120\}' "$S" | grep -c 'AR-04'
git log --format='%h %ad' --date=format:'%H:%M:%S' -1 cb39d89
```

**앞선 판(2026-09-22 첫 작성)의 오류** — consent 시각을 `16:05` 로 적었다. `date` 를 돌리지
않고 짐작해서 쓴 값이고, 실제 동의 시각은 위 표의 15:49:14 다. 커밋(15:49:57)보다 뒤인 값을
적었으니 QA 가 "16:05 에 합의한 내용이 15:49:57 커밋에 굳었다 — 시간 역전" 으로 읽고 REJECT
했다. **판정은 정당했다** — 검증하면 반증되는 앵커를 적었으므로 `unanchored` 와 다를 바 없다.
고친 것은 시각 하나이고 동의 사실 자체는 처음부터 실재했다.

QA 가 든 두 번째 근거(reflect-kit 프롬프트 기록에 15:06 이후 대화 없음)는 성립하지 않는다.
그 기록은 `UserPromptSubmit` 훅이 쓰는 파일이라 `AskUserQuestion` 의 답은 애초에 남지 않는다.
이 세션의 `AskUserQuestion` **4 건** 전부가 그 기록에 없다 — 즉 "없음" 이 "안 일어났음" 을 뜻하지
않는 자리다. 0 을 근거로 쓰기 전에 양성 대조를 세워야 한다는 규칙이 평가자 쪽에도 적용된다.

**남는 구조적 문제**: 여러 스프린트를 한 브랜치에 쌓으면 앞 스프린트의 `status` 전환이 항상
뒤 스프린트의 범위 조건에 들어온다. 다음 계약에서 `.harness/` 범위 조건을 쓸 때는 산출물
슬러그를 열거하는 대신 **"이 구간에서 조건 줄이 바뀐 계약 파일 0개"** 로 재는 편이 낫다 —
`status` 토글과 조건 변조를 구별하는 것이 원래 의도였고, 봉인 검사가 이미 그것을 한다.


### A-01 정정 — 선택지 건수 5 → 4

처음 이 파일에 "5 건" 으로 적었다. `grep -c '"name":"AskUserQuestion"'` 의 값을 그대로 쓴 것이
원인이고, 그 계수에는 시스템 프롬프트에 붙은 도구 정의 문자열 1 건이 섞인다. `tool_use` 종류로
걸러 세면 **4 건**이다 (QA 와 교차 진단이 각각 독립으로 같은 값을 냈다).

```bash
S=~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/f5b7f3a5-c03d-452b-b44b-fc3d15dcd1a0.jsonl
grep -c '"name":"AskUserQuestion"' "$S"   # 5 — 도구 정의 문자열이 섞인다
python3 -c 'import json,io,sys; n=0
for ln in io.open(sys.argv[1],encoding="utf-8"):
    try: d=json.loads(ln)
    except Exception: continue
    c=(d.get("message") or {}).get("content")
    if isinstance(c,list):
        for it in c:
            if isinstance(it,dict) and it.get("type")=="tool_use" and it.get("name")=="AskUserQuestion": n+=1
print(n)' "$S"                             # 4 — 실제 호출
```

핵심 논증(동의가 커밋보다 43 초 앞선다)에는 영향이 없다.

## A-02 — 계약 조건 문구의 파일 수 "6개" 오류 기록

**앵커**: AR-01(`위 6개 경로`) · RE-01(`변경 6개 파일이 .md 5개 + .yaml 1개`) ·
DG-01(`AR-01 의 6행`) · DG-03 · DG-04(`변경 6개 파일`) — 조건 줄 5 곳.

**무엇이 틀렸나**: 실제 대상은 **7개**다 (`.md` 6 + `.yaml` 1). 계약을 쓴 뒤 교차 진단 지적을
받아 `harness/evals/kaizen/evaluator-kaizen/expected-improvements.md` 를 범위에 더했는데,
범위 경계의 산문 라벨만 7개로 고치고 **조건 줄 안의 숫자는 5 곳 모두 그대로 뒀다.**

**왜 조건 줄을 고치지 않았나**: 봉인 뒤라 조건 줄 편집은 봉인을 깬다. 통과 집합도 바뀌지
않는다 — AR-01 은 열거된 경로 목록으로 판정하고 그 목록은 7개이며, RE-01·DG-01·DG-03·DG-04 는
"실행 코드 0개" · "`scripts/release.sh` 와 교집합 0개" 를 재므로 파일 수가 6 이든 7 이든 결과가
같다. QA 와 교차 진단이 각각 같은 결론을 냈다.

**amend_direction**: `unchanged` — 통과 집합·측정 명령·판정 기준 전부 그대로다. 틀린 것은
서술 숫자이며 사용자 승인이 필요한 개정이 아니다.

**다음 계약에 반영할 것**: 파일 수를 조건 줄에 숫자로 박지 마라. 범위 경계의 열거 목록을
가리키고 개수는 그 목록을 세어 얻게 하면, 범위가 늘어도 조건 줄을 손댈 일이 없다.

## A-03 — DG-02 검사 범위가 대상 1개를 빠뜨렸다 (판정 영향 없음)

**앵커**: DG-02 의 "기준 39건 · (파일,규칙) 조합 11개, 대상은 `.md` 5개"

**무엇이 틀렸나**: 이번 스프린트가 바꾼 마크다운은 **6개**다. 계약이 `.md` 5개라 적고 대상을
열거하지 않아서, 나중에 범위에 더한 `expected-improvements.md` 가 검사에서 빠졌다. 그 파일에
경고가 생겨도 이 검사는 0 을 냈을 것이다 — 교차 진단이 짚었다.

**확인 결과**: 6개 전부 같은 설정으로 다시 돌리니 **39건 · 11조합**으로 5개 판과 같다.
빠진 파일의 경고가 0 이라 판정에 영향이 없다.

**amend_direction_oracle**: `unchanged` — 측정 집합을 늘려 다시 재봤고 값이 같았다. 기준값을
고치지 않았으므로 조건이 느슨해지지도 좁혀지지도 않았다.

**다음 계약에 반영할 것**: 0 이 기대값인 조건은 **대상 파일을 열거하라.** "`.md` 5개" 처럼
개수만 적으면 다음 평가자가 같은 집합을 만들 방법이 없다.
