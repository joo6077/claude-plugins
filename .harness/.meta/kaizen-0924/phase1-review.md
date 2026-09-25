# Phase 1 계약 초안 검토 — kaizen-0924-p01-guides

- 대상: `.harness/sprint-contract-kaizen-0924-p01-guides.md` (봉인 전 초안, 조건 25 줄)
- 역할: 카이젠 2026-09-24 Phase 1 REVIEW (사용자 승인 5 단계를 대신하는 독립 검토자)
- 검토일: 2026-09-24 · 작업 폴더 `HEAD` = `7689fde6efdaa2401e90689dd15dd16baf8d59a0` (계약의 시작 커밋과 같다)
- 레포 파일은 이 파일 하나만 썼다. 임시 사본과 시험 스크립트는
  `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p1review/` 에 있다

## 결론

고쳐서 다시 내야 한다(CHANGES). 뼈대는 좋다. 조건 25 개 모두 실패 상태를 한 문장으로 쓸 수 있고, 봉인 전 실측 값은
다시 돌려 전부 같게 나왔다. 초안의 개선안을 그대로 따른 모의 편집본을 만들어 25 조건을 한꺼번에 돌렸더니 전부 통과했다 —
조건끼리 서로 막는 곳은 없다.

막는 이유는 다섯이다.

1. 바뀌는 3 항 문구를 그대로 베껴 쓴 다른 킷 파일 5 곳이 반대편 목록에서 빠졌다 (ER-04)
2. 초안이 BUILD 에게 쓰라고 한 문장 두 개가 평가자 규칙(`harness/agents/qa-evaluator.md` 규칙 2 · 11)과 다른 말을 한다.
   이번 Phase 가 없애려는 어긋남을 새 글자로 다시 만든다 (AR-02 · ER-03)
3. 모의 편집본이 25 조건을 다 통과하고도 parity 표 위아래 문장에 옛 개수(14개 · 9개)가 남았다 (SK-04)
4. AR-04 ② 가 `.harness/` 경로를 슬러그로 나열한다 — 러닝북 계약 규칙 「`.harness/` 는 슬러그를 열거하지 말고
   `verify_seal` 로 잰다」와 어긋난다
5. 17 Phase 가 한 작업 폴더를 같이 쓰는데, AR-04 ③ 과 DG-06 의 `doc-contracts` 는 다른 Phase 가 만든 결함으로 이 Phase 를
   떨어뜨릴 수 있다

## 다시 돌려 본 것

공통 정의 블록을 계약 본문에서 그대로 잘라 bash 로 실행했다.

- 개정 파일이 아직 없는 지금 `END_UNRESOLVED` 를 찍고 종료 코드 2 로 멈춘다 — 설계대로다
- `END` 자리에 시작 커밋을 넣어 편집 전 파일로 모든 측정을 돌렸다. 계약의 `봉인 전 실측` 표와 전부 같다:
  SK-01 0 · SK-02 0 · SK-03 이름 차이 2 · SK-04 skill 1~14, 없는 인용 1, agent 1~9 · ER-02 5 · 1 · 1 · 1 · 4 ·
  ER-03 1 · 2 · 1 · 1 · 1 · (0, 1) · 1 · AR-01 3 · 0 · 0 · 1 · 4 · 0 · AR-03 (a) agent 1 1 1 1 2 1 / skill 1 2 2 ·
  RE-02 13 · 9 · DG-07 1.5.0 / 1.6.0
- 양성 대조를 다시 만들어 돌렸다: ER-01 1 · ER-05 bash 에서 UTF-8 2 / C 로케일 1 · AP-01 1 · AP-03 펜스 검출기 1,
  `bash` 펜스 1 (`textile` 같은 다른 힌트도 1 로 잡힌다) · DG-02 3 · DG-05 1 · AR-04 ③ `SEAL_ABSENT` 11 · `SEAL_OK` 50
- 주의 하나: 이 맥의 zsh 에서는 `grep` 이 ugrep 함수라 ER-05 의 C 로케일 대조가 2 로 나온다. bash 는 `/usr/bin/grep` 을
  써서 1 이 나온다. 계약이 bash 실행을 못박아 둔 것이 맞다
- DG-05 양성 대조는 머리줄 없는 표 행 두 줄을 붙여 넣었더니 1 이 나왔다(계약은 2). 끊긴 표 한 덩어리를 한 번 세는
  것으로 보인다. 측정이 살아 있다는 결론은 같다
- sprint-contract 6.5 저장 검사 (1)(2)(3)(5): 제목은 허용 목록 안, 조건 체크박스는 조건 절에만, `conditions: 25` = 실제 25,
  `[미실측]` 0 건
- 모의 편집본(`mock_build.py`): 초안 개선안대로 두 가이드를 고친 사본에서 25 조건 전부 통과, 펜스 0/0, 새 경고 0/0,
  표 구분줄 13/9

## 항목별 판단

- 처리 배정표: `배정` 칸이 Phase 1 인 `F10` · `harness:P09` 와, Phase 2 배정이지만 §3.7 부분을 Phase 1 에 맞추라는
  `harness:P05` 셋 모두 배경 표와 개선안에 들어 있다. 빠진 행은 없다. `Phase 별 적용 힌트` 의 Phase 1 줄과도 맞는다.
  러닝북과 오케스트레이터에 Phase 1 추가 과제는 없다
- 범위: 고치는 파일은 두 가이드뿐이고 러닝북 Phase 표의 Phase 1 범위 안이다. 공유 파일은 건드리지 않는다(SC-00,
  `범위 경계`). harness `README` 의 `AUTO` 구간과 `sync-docs.py` 는 두 가이드를 읽지 않음을 확인했다 — 버전을 올려도
  범위 밖 파일을 고칠 일이 생기지 않는다
- 외부 근거: 새로 들어갈 URL 둘(zsh 매뉴얼, v2.1.281 릴리스)이 근거 파일에 있다. 근거 파일이 스스로 밝힌 한계 네 가지를
  계약이 그대로 옮겼다. `omitClaudeMd` · `experimental` 뜻을 지어내지 않게 `미확인` 을 요구한 것도 맞다
- 판정 가능성: 조건마다 실패 문장을 쓸 수 있다. 예: SK-03 「`#### 등급 원장` 표의 행 이름이 10 개와 다르거나, 빈 칸 행이 있거나, 새 두 행
  등급에 `E2` 가 없거나, `Completion Evidence Gate` 행에 `네 칸` 이 없다」. N/A 다섯 줄도 사유를 다시 재는 명령이 붙어 있다

## 고칠 것

### 1. ER-04 · Counterpart 표 — 반대편 5 곳이 빠졌다

초안은 조항 번호를 인용하는 곳만 찾았다. 3 항의 옛 문구 「`[미검증]` + 사유 한 줄」과 agent §10 을 **내용째 베낀** 곳은
찾지 않았다. 찾은 명령과 결과:

```text
grep -rnE "사유 한 줄|agent-design-guide §10|skill-design-guide §3\.7" --include="*.md" .
  (.harness/ 와 두 가이드 자신은 뺌)
react-kit/references/render-evidence-protocol.md:59   「`[미검증]` 마커와 사유 한 줄을 붙이고 부분 완료로 보고」
flutter-toolkit/references/visual-evidence-protocol.md:136   「`[미검증]` 마커 + 사유 한 줄」
onboarding-kit/skills/setup-guide/SKILL.md:30   「마커 + 사유 한 줄」
infra-kit/skills/infra-test/SKILL.md:37   「`[미검증] TOOL_OR_ENV_MISSING: … — 재검증: <명령>`」 (시도한 우회 칸 없음, skill §3.7 인용)
rust-kit/agents/rust-reviewer.md:137   「미검증 항목 마커 (agent-design-guide §10)」 접미 없는 `[미검증]` + 이유
```

다섯 곳 모두 이번 편집 뒤 옛 규칙을 들고 남는다. 각각 Phase 10 · 5 · 14 · 8 · 9 범위라 이 Phase 가 고칠 수는 없으니
sprint-contract 2.5 (6) 대로 명시적 미완으로 넘긴다.

`GAP 분석` 절 Counterpart 표에 다섯 행을 더한다:

```text
| `react-kit/references/render-evidence-protocol.md:59` | 「`[미검증]` 마커와 사유 한 줄 … 부분 완료로 보고」(3 항 옛 문구) | Phase 10 범위 — 넘김 (ER-04) |
| `flutter-toolkit/references/visual-evidence-protocol.md:136` | 「`[미검증]` 마커 + 사유 한 줄」 | Phase 5 범위 — 넘김 (ER-04) |
| `onboarding-kit/skills/setup-guide/SKILL.md:30` | 「마커 + 사유 한 줄」 | Phase 14 범위 — 넘김 (ER-04) |
| `infra-kit/skills/infra-test/SKILL.md:37` | 「`[미검증] TOOL_OR_ENV_MISSING` … 재검증」 — 시도한 우회 칸 없음 | Phase 8 범위 — 넘김 (ER-04) |
| `rust-kit/agents/rust-reviewer.md:137` | 「agent-design-guide §10」 접미 없는 `[미검증]` | Phase 9 범위 — 넘김 (ER-04) |
```

ER-04 조건 줄을 이렇게 바꾼다 (러닝북이 notes 에 적으라고 한 「반영한 처리 배정표 키」도 여기서 함께 잰다 —
Final 이 처리 배정표를 채울 때 이 파일을 읽는다):

```text
- [ ] ER-04: Counterpart 소비면 가운데 이 Phase 범위 밖이라 못 고치는 8 곳을 명시적 미완으로 넘기고, 이미 맞는 2 파일은 건드리지 않는다 — `.harness/.meta/kaizen-0924/phase1-notes.md` 에 `harness/skills/sprint/SKILL.md:77` · `harness/skills/create-agent/SKILL.md` · `harness/skills/create-skill/SKILL.md:24` · `react-kit/references/render-evidence-protocol.md:59` · `flutter-toolkit/references/visual-evidence-protocol.md:136` · `onboarding-kit/skills/setup-guide/SKILL.md:30` · `infra-kit/skills/infra-test/SKILL.md:37` · `rust-kit/agents/rust-reviewer.md:137` 과 처리 배정표 키 `F10` · `harness:P09` · `harness:P05` 가 각각 1 회 이상 있고, 이 Phase 커밋이 다섯 파일(`harness/skills/sprint/SKILL.md` · `harness/skills/create-agent/SKILL.md` · `harness/skills/create-skill/SKILL.md` · `harness/agents/qa-evaluator.md` · `harness/docs/guides/qa-evaluation-guide.md`)을 하나도 건드리지 않는다 [exact, enumerated]
      (Given: BUILD 가 notes 를 쓰고 커밋한 뒤 · 측정: `test -f .harness/.meta/kaizen-0924/phase1-notes.md` exit 0 · 위 11 문자열을 그 파일에서 각각 `grep -cF` 해 전부 1 이상 · `mine | grep -cE '^harness/(skills/(sprint|create-agent|create-skill)/SKILL\.md|agents/qa-evaluator\.md|docs/guides/qa-evaluation-guide\.md)$'` 0. 봉인 전 실측: notes 없음 — 구현이 만들 파일이라 면제)
```

`범위 경계` 의 「넘기는 것」 줄에도 다섯 곳을 더한다.

### 2. AR-02 · ER-03 · 개선안 초안 — 평가자 규칙과 다른 말

`harness/agents/qa-evaluator.md` 규칙 11 의 네 요건은 (1) 1 차 도구 시도와 실패 출력 인용 (2) fallback 시도, 또는 계약에
fallback 이 없음을 계약 결함으로 기록 (3) 실패 로그 출력 (4) 통제 불가 사유 한 문장 + 재검증 명령이다. 초안의 네 칸
(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)과 칸 경계가 1:1 이 아니다 — 규칙 11 은 실패 로그를 따로 세고, 사유와
명령을 한 요건으로 묶는다. 또 규칙 2 는 `INVALID` 만 2 건 임계로 세고 `ENV` 는 `env_gaps` 로 따로 센다. 그런데 초안은

- agent §10 (2) 에 「`qa-evaluator.md` 규칙 11 의 네 요건과 **같은 것**」
- agent §10 Cross-Surface Parity 에 「같은 네 칸 · **같은 2 건 임계**」
- skill 3 항에 「마커·임계값은 agent-design-guide §10 … 과 **동일 규약**을 쓴다」를 남김

이라고 쓰게 한다. 생성 측은 `[미검증]` 전체 2 건으로 부분 완료를 가르고, 평가 측은 `INVALID` 2 건으로 REJECT 를 가른다 —
숫자는 같아도 세는 대상이 다르다. 「같은 2 건 임계」는 ER-03 이 지우는 옛 주장 「2 건 임계값은 양쪽이 동일」을 다른 글자로
되살려 ER-03 을 그대로 통과한다.

개선안 초안 문구를 이렇게 바꾼다.

- agent §10 (2): 「네 칸은 `qa-evaluator.md` 규칙 11 의 네 요건을 생성 측 말로 옮긴 것이다 — 요건 (1)·(3) 의 실패 출력이
  `막는 것`, (2) 가 `시도한 우회`, (4) 가 `통제 불가 사유` 와 `재검증 명령` 이다. `INVALID` 2 건 이상이면 REJECT,
  `ENV` 는 `env_gaps` 로 따로 세어 검증 범위 판정에만 쓴다 (수치는 `qa-evaluation-guide.md` §카운팅 및 자동 REJECT 임계)」
- agent §10 Cross-Surface Parity: 「생성 측 짝은 skill-design-guide §3.7 3 항이다. 네 칸은 양쪽이 같은 말을 쓴다. 2 건 기준은
  세는 대상이 다르다 — 생성 측은 `[미검증]` 전체로 부분 완료를, 평가 측은 `INVALID` 만으로 REJECT 를 가른다」.
  agent §12 표 아래 문단(`:660`)도 같게
- skill 3 항: 「마커·임계값은 … 동일 규약을 쓴다」를 「마커와 네 칸은 agent-design-guide §10 과 같은 말을 쓴다 (용어 분기
  금지)」로. `시도한 우회` 칸에 한 문장: 「검증을 못 한 경우 우회가 정말 없으면 칸을 비우지 말고 `없음 — 이유` 를 적는다
  (규칙 11 (2) 가 계약 결함 기록으로 받는다). 작업 자체를 못 한다고 할 때는 하나 이상이어야 한다」 — 뒤 문장은 근거 파일 §4
  권장안 그대로다

AR-02 조건 줄을 이렇게 바꾼다 (토큰 8 → 10):

```text
- [ ] AR-02: `agent-design-guide.md` §10 「Unverifiable 조건 정책」 구간이 평가 측 분류와 같은 말을 쓴다 — 10 토큰 `[미검증:ENV]` · `[미검증:INVALID]` · `막는 것` · `시도한 우회` · `통제 불가 사유` · `재검증 명령` · `네 칸` · `2 건` · `규칙 11` · `env_gaps` 가 각각 1 건 이상이고, 요약 표 `| **Unverifiable 정책** |` 행에 `네 칸` 이 있다 [exact, enumerated]
      (측정: `for t in '[미검증:ENV]' '[미검증:INVALID]' '막는 것' '시도한 우회' '통제 불가 사유' '재검증 명령' '네 칸' '2 건' '규칙 11' env_gaps; do printf '%s=%s\n' "$t" "$(pol | grep -cF "$t")"; done` 10 값 전부 1 이상 · `grep -F '| **Unverifiable 정책** |' "$T/a.md" | grep -cF '네 칸'` 1. 봉인 전 실측: `2 건` 1 · 나머지 9 토큰 0 · 요약 행 0)
```

ER-03 은 옛 서술을 7 개에서 8 개로 늘린다. `회귀 게이트` 절 ER-03 블록에 한 줄을 더하고 조건 문구의 「7 개」를 「8 개」로,
열거에 「skill 3 항의 `마커·임계값은 agent-design-guide §10` (동일 규약 주장)」을 더한다:

```bash
grep -cF '마커·임계값은 agent-design-guide §10' "$T/s.md"
```

편집 전 값은 1 이다 (다시 재 봤다). 봉인 전 실측 줄도 「1 · 2 · 1 · 1 · 1 · (0, 1) · 1 · 1」로.

### 3. SK-04 — 표 위아래 문장의 옛 개수를 못 잡는다

모의 편집본은 SK-04 를 통과하고도 다음 세 문장이 옛 값 그대로였다 (모의본에서 1 · 1 · 1). 머리줄은 16개인데 바로 아래
문장이 「14개 항목」이라 하면 SK-04 가 없애려는 바로 그 어긋남이다.

- skill `:1087` 「아래 14개 항목을」
- skill `:1106` 「이 예외들(7, 8, 12, 13)을 제외한 나머지 (1~6, 9~11, 14)」 — 15 는 양면, 16 은 생성 측 전용이 된다
- agent `:644` 「아래 9개 항목을」

또 초안이 새 소절에 쓰라고 한 인용 「§11 16 번째 항목」은 (b) 의 정규식 `§11 parity 표 [0-9]+ 번째` 에 걸리지 않아 번호가
틀려도 못 잡는다. 개선안 초안의 그 문구를 「§11 parity 표 16 번째 항목」으로 바꾸고, SK-04 에 (d) 를 더한다:

```text
(d) 표 위아래 문장에 옛 개수가 남지 않고 새 소절이 같은 꼴로 인용한다 — `아래 14개 항목` · `(1~6, 9~11, 14)` (skill) · `아래 9개 항목` (agent) 이 0 건, `§11 parity 표 16 번째` 가 skill 에 1 건
측정: `grep -cF '아래 14개 항목' "$T/s.md"` 0 · `grep -cF '(1~6, 9~11, 14)' "$T/s.md"` 0 · `grep -cF '아래 9개 항목' "$T/a.md"` 0 · `grep -cF '§11 parity 표 16 번째' "$T/s.md"` 1.
봉인 전 실측: 1 · 1 · 1 · 0
```

### 4. AR-04 ② ③ — `.harness/` 슬러그 나열과 다른 Phase 몫

②는 허용 7 경로 가운데 5 개가 `.harness/` 슬러그 경로다. 러닝북 `계약 규칙` 은 「`.harness/` 는 슬러그를 열거하지 말고
`verify_seal` 로 잰다」고 적었다. 실제로도 교차 진단이나 워크플로가 `.harness/.meta/kaizen-0924/` 에 파일을 하나 더 남기고
슬러그 커밋에 실으면 ②가 떨어진다. `.harness/` 는 ③ 에 맡기고 ② 는 그 밖만 잰다.

```text
② `mine` 에서 `.harness/` 로 시작하는 줄을 뺀 나머지가 두 가이드 경로뿐이고, 두 가이드 경로가 둘 다 있다 — `.harness/` 는 ③ 으로 잰다
   측정: `mine | grep -vE '^(\.harness/|harness/docs/guides/(skill|agent)-design-guide\.md$)' | grep -c .` 0 · `mine | grep -cxE 'harness/docs/guides/(skill|agent)-design-guide\.md'` 2
```

가짜 목록으로 돌려 봤다: 두 가이드 + `.harness/` 세 줄이면 0 · 2, `harness/skills/sprint/SKILL.md` 가 섞이면 1 · 1.
`범위 경계` 의 허용 파일 문장은 설명으로 남겨도 된다.

③은 작업 폴더 전체의 계약을 센다. 다른 Phase 의 FIX 가 봉인된 제 계약을 고치면 이 Phase 가 떨어진다. ③ 끝에 붙인다:

```text
`SEAL_BROKEN` 줄마다 그 파일이 `mine` 에 있으면 실패다. `mine` 에 없는 파일의 `SEAL_BROKEN` 은 다른 Phase 몫이다 — 파일 이름을 근거에 적고 이 조건에는 세지 않는다
```

### 5. DG-06 — `doc-contracts` 도 다른 Phase 몫을 가려야 한다

`python3 scripts/validate-doc-contracts.py -v` 는 지금 `.claude/skills/kaizen-orchestrator/SKILL.md:222 →
scripts/collect-kaizen-data.py` 한 블록을 잰다. 그런데 러닝북 Phase 4 추가 과제 (2)가 같은 사이클에
`scripts/collect-kaizen-data.py` 를 고친다. 그쪽이 어긋나면 이 Phase 가 떨어진다. `scope-isolation` 에 둔 예외를
`doc-contracts` 에도 둔다. DG-06 조건 줄 끝에 더한다:

```text
`doc-contracts` 가 `FAIL` · `ERROR` 이면 `python3 scripts/validate-doc-contracts.py -v` 의 `검사:` 줄에 나온 경로를 `mine` 과 대조한다. 그 경로가 `mine` 에 하나도 없으면 다른 Phase 몫으로 근거에 적고 이 조건은 통과다
```

## 권고 (막지 않음 — 반영하면 좋다)

- SK-02: 조건은 「§3.7 에」라 했지만 측정은 파일 어디든 `####` 알려진 답 제목 하나면 통과한다. 위치를 잰다:
  `awk '/^## 3\.7\./{f=1;next} f&&/^## /{exit} f&&/^#### .*알려진 답/{c++} END{print c+0}' "$T/s.md"` 1
  (편집 전 0, 모의본 1). 채택하면 `범위 경계` 의 「측정이 기대는 제목」에 `## 3.7.` 을 더한다
- AR-03 (b): `2026-09-24` 는 두 파일 머리 설정의 `last_updated` 만으로 채워진다(모의본 skill 4 · agent 6). 날짜 표기를 바꿨는지
  재려면 `2026-09-24 조회` 로 잰다 (편집 전 0 · 0, 모의본 3 · 5)
- DG-05: 양성 대조 값 「2」는 넣는 방식에 따라 1 이 나온다. 「1 이상」으로 적는다
- `mine` 은 커밋 메시지 어디든 슬러그가 있으면 잡는다. Phase 2 가 harness:P05 를 「Phase 1 과 맞춘다」며 메시지에 이 슬러그를
  인용하면 그 파일이 `mine` 에 섞인다. notes 에 「다른 Phase 커밋 메시지에 이 슬러그를 쓰지 않는다」를 적거나, 제목 줄 끝
  `(kaizen-0924-p01-guides)` 꼴로 못박고 `--grep='(kaizen-0924-p01-guides)$'` 로 좁힌다

## 다시 낼 때

조건 수는 그대로 25 다 (새 ID 없음, 문구와 측정만 바뀐다). 바뀐 측정 넷(ER-03 여덟째 줄 · SK-04 (d) · AR-02 두 토큰 ·
AR-04 ② 새 꼴)은 편집 전 값을 봉인 전 실측 표에 적는다 — 위에 적은 값은 이 검토에서 실제로 돌린 값이다.

VERDICT: CHANGES

## 2 회차

- 대상: 1 회차를 반영해 다시 낸 계약 초안 (431 줄 · 조건 25 줄, 봉인 전)
- 검토일 2026-09-24 · 작업 폴더 `HEAD` = `7689fde6efdaa2401e90689dd15dd16baf8d59a0` (이 Phase 커밋은 아직 없다)
- 레포 파일은 이 파일 하나만 고쳤다(이 절을 끝에 붙였다). 임시 사본 · 모의본 · 스크립트는
  `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p1review2/` 에 있다

### 결론

한 번 더 고쳐야 한다(CHANGES). 1 회차의 막는 이유 다섯과 권고 넷은 전부 들어갔고, 바뀐 측정도 다시 재 보니 계약에
적힌 값과 같았다. 그런데 모의본을 두 벌 더 만들어 돌려 보니, 이번 Phase 가 고치려는 문장 두 곳을 틀리게 남겨도
25 조건이 전부 통과한다. 둘 다 조건 한 줄에 문자열 하나를 더하면 막힌다. 조건 수는 25 그대로다.

### 1 회차 지적이 들어갔는지

| 1 회차 | 계약에서 찾은 자리 | 판단 |
| --- | --- | --- |
| 1 · ER-04 반대편 5 곳 | Counterpart 표 `:110-114` · ER-04 `:373-377` (넘김 8 경로 + 처리 배정표 키 3) · `범위 경계` `:206` | 들어갔다 |
| 2 · 평가자 규칙과 다른 말 | 개선안 `:128-132` (skill 3 항) · `:167-176` (agent §10) · `:178-179` (§12 표 아래) · AR-02 10 토큰 `:387-388` · ER-03 8 개 `:251-262` · `:371-372` | 문구는 들어갔다. 측정이 덜 닫혔다 — 아래 고칠 것 1 |
| 3 · SK-04 옛 개수 | SK-04 (d) `:353-357` — 1 회차 제안보다 넓다 (새 개수 `아래 16개 항목` · `아래 10개 항목` 도 요구) | 들어갔다 |
| 4 · AR-04 ② ③ | ② `:395` (`.harness/` 밖만 잰다) · ③ `:396-398` (`mine` 이나 이 계약에 걸린 `SEAL_BROKEN` 만 센다) | 들어갔다 |
| 5 · DG-06 `doc-contracts` | `:426-427` (대조 명령까지 붙었다) | 들어갔다 |
| 권고 넷 | SK-02 위치 `:347` · `범위 경계` `:204` 에 `## 3.7.` · AR-03 (b) `2026-09-24 조회` `:389` · DG-05 「1 이상」 `:425` · `mine` 은 서명 줄 `Kaizen-Phase:` 로 좁힘 `:247` · `:203` | 들어갔다 |

### 다시 돌려 본 것

- 공통 정의 블록을 계약 본문에서 그대로 잘라 bash 로 돌렸다. 개정 파일이 없어 `END_UNRESOLVED` 를 찍고 종료 코드 2
- `END` 자리에 시작 커밋을 넣고 25 조건의 측정을 계약 문구 그대로 옮겨 편집 전 파일에 돌렸다. `봉인 전 실측` 표와
  전부 같다. 이번에 바뀐 것만 적으면 SK-02 §3.7 안 0 · SK-04 (d) 1 · 1 · 1 · 0 · 0 · 0 · ER-03 1 · 2 · 1 · 1 · 1 ·
  (0, 1) · 1 · 1 · AR-02 `2 건` 1 · 나머지 9 토큰 0 · 요약 행 0 · AR-03 (b) 전부 0 · AR-04 ③ `SEAL_ABSENT` 11 ·
  `SEAL_OK` 50 · `SEAL_BROKEN` 0 (이 계약 자신은 아직 `SEAL_ABSENT`)
- 1 회차 모의본에 개정 개선안 문장을 더한 `mock_build2.py` (3 항의 `없음 — 이유` · 용어 분기 금지 문장, §10 (2) 의
  `규칙 11` · `env_gaps`, 「2 건 기준은 세는 대상이 다르다」, 표 위아래 개수)에서 25 조건이 전부 통과했다 —
  SK-04 (d) 0 · 0 · 0 · 1 · 1 · 1, AR-02 10 토큰 전부 1 이상 · 요약 1, AR-03 (b) agent 1 1 1 1 5 / skill 3,
  새 경고 0 / 0, 펜스 0 / 0, 표 구분줄 13 / 9. 가짜 `mine`(두 가이드 + `.harness/` 두 줄)으로 ② 0 · 2,
  `harness/skills/sprint/SKILL.md` 가 섞인 목록으로 1 · 1
- 서명 줄 `mine`: 스크래치 저장소에서 봉인 커밋 꼴(`-m 제목 -m 서명 -m Co-Authored-By`)과 서명 · Co-Authored-By 를
  한 문단에 붙인 꼴은 잡혔고, 본문에 서명 글자를 인용한 커밋과 `kaizen-0924-p01-guides-extra` 는 안 잡혔다. ① 의
  `grep -cxF` 도 두 가이드 커밋 모두 1
- ER-04 문자열 루프: 11 문자열을 담은 가짜 notes 에서 11 값 전부 1, `harness:P05` 를 지우면 그 값 0
- `validate-post-kaizen.py --since 7689fde…`: 15 checks — 12 PASS / 0 FAIL / 0 ERROR / 3 SKIP. DG-06 대조 명령이 뽑는
  경로는 `.claude/skills/kaizen-orchestrator/SKILL.md` · `scripts/collect-kaizen-data.py` 둘. `scope-isolation` 은
  `harness/skills/` 와 다른 킷 `skills/` 가 한 커밋에 섞일 때만 떨어지는데 이 Phase 커밋은 ② 때문에 그럴 수 없다
- DG-05: `validate-plugin.py harness --check=table-integrity` 18 md files OK
- sprint-contract 6.5 (1)(2)(3)(5): 제목 12 개 모두 허용 목록 · 체크박스 25 줄 모두 조건 절 · `conditions: 25` = 25 ·
  `[미실측]` 0. (4) 커버리지 검출기는 `UNCOVERED` 를 SK-04 · ER-02 · ER-04 · AR-03 네 줄 낸다 — 넷 다 `범위 경계`
  `:212-214` 에 해소 기록이 있다
- 반대편을 한 번 더 훑었다. parity 번호 인용(`parity item 8/14` · `12` · `§11 parity 표 N 번째`)은 편집 뒤에도 같은
  행을 가리킨다. `15 종` 을 베낀 곳은 `harness/skills/create-agent/SKILL.md` 뿐(이미 넘김), `500 라인 상한` 은
  오케스트레이터 references(이미 넘김)와 지난 기록 파일뿐이다. 세션 200 · Explore haiku 를 베낀 킷 파일은 없고,
  에이전트 머리 설정 필드 목록을 읽는 코드도 없다

### 고칠 것

#### 1. AR-02 — 「같은 2 건 임계」를 다시 써도 통과한다

1 회차 2 번이 짚은 실패 모양이 측정에는 아직 열려 있다. 개선안 문구는 고쳐졌지만 조건은 그 문장을 재지 않는다.
`mock_bad.py` 는 좋은 모의본에서 두 문장만 바꿨다 — agent §10 의 `Cross-Surface Parity` 를 「양쪽이 같은 네 칸 ·
같은 2 건 임계를 쓴다」로, §12 표 아래를 「네 칸과 2 건 임계는 양쪽이 같다」로. 25 조건 측정 출력이 좋은 모의본과
한 글자도 다르지 않았다 (AR-02 10 토큰 전부 1 이상, ER-03 8 개 전부 0). `qa-evaluator.md` 규칙 2 와 어긋나는 바로
그 주장이 봉인 뒤 QA 를 통과한다는 뜻이다.

개선안이 두 자리(`:172-174` · `:178-179`)에 쓰라고 한 「2 건 기준은 세는 대상이 다르다」를 잰다. AR-02 줄을 이렇게 바꾼다:

```text
- [ ] AR-02: `agent-design-guide.md` §10 「Unverifiable 조건 정책」 구간이 평가 측 분류와 같은 말을 쓴다 — 11 토큰 `[미검증:ENV]` · `[미검증:INVALID]` · `막는 것` · `시도한 우회` · `통제 불가 사유` · `재검증 명령` · `네 칸` · `2 건` · `규칙 11` · `env_gaps` · `세는 대상` 이 각각 1 건 이상이고, 요약 표 `| **Unverifiable 정책** |` 행에 `네 칸` 이 있으며, §12 parity 절에도 두 쪽의 2 건 기준은 `세는 대상` 이 다르다고 적혀 있다 [exact, enumerated]
      (측정: `for t in '[미검증:ENV]' '[미검증:INVALID]' '막는 것' '시도한 우회' '통제 불가 사유' '재검증 명령' '네 칸' '2 건' '규칙 11' env_gaps '세는 대상'; do printf '%s=%s\n' "$t" "$(pol | grep -cF "$t")"; done` 11 값 전부 1 이상 · `grep -F '| **Unverifiable 정책** |' "$T/a.md" | grep -cF '네 칸'` 1 · `par "$T/a.md" | grep -cF '세는 대상'` 1 이상. 봉인 전 실측: `2 건` 1 · 나머지 10 토큰 0 · 요약 행 0 · §12 0. 음성 대조: 두 자리를 「같은 네 칸 · 같은 2 건 임계」로 쓴 모의본은 `세는 대상` 0 · 0)
```

이 검토에서 잰 값: `세는 대상` — 편집 전 `pol` 0 · §12 0, 좋은 모의본 1 · 1, `mock_bad.py` 0 · 0.
`봉인 전 실측` 표의 `[AR-02]` 줄도 「`2 건` 1, 나머지 10 토큰 0 · 요약 행 0 · §12 0」으로 고친다.

#### 2. AR-03 — 「상한이 3 종 있다」가 남아도 통과한다

agent `:463` 은 「Claude Code 자체가 강제하는 상한이 3 종 있다 — 동시 20 · 세션 누적 200 · 깊이 3」이다. 세션 상한을
빼면 2 종인데, 개선안 `:165` 는 개수를 고치라고 하지 않았고 AR-03 도 재지 않는다. `mock_stale3.py` (좋은 모의본에서
「2 종」만 「3 종」으로 되돌림)도 25 조건 출력이 좋은 모의본과 같았다. 1 회차 3 번(표 옆 문장의 옛 개수)과 같은 종류다.

- 개선안 `:165` 에 더한다: 「`상한이 3 종 있다` → `2 종`. 뒤 문장 「각각 `Concurrent subagent limit reached` /
  `Subagent spawn limit reached`」도 남는 상한 수에 맞춘다 — 어느 오류 문구가 어느 상한 것인지는 근거 파일에 없으니
  새로 짝짓지 않는다」
- AR-03 (a) 에 agent `상한이 3 종` 을 더해 「0 이어야 하는 10 문자열」로 (``sub-agents) (2026-04)`` 바로 뒤).
  봉인 전 실측은 「(a) agent 1 · 1 · 1 · 1 · 2 · 1 · 1 / skill 1 · 2 · 2」, `봉인 전 실측` 표의 `[AR-03]` 줄도 같게
- `범위 경계` `:214` 커버리지 해소 줄의 「문자열 15 개」 → 「16 개」

이 검토에서 잰 값: `grep -cF '상한이 3 종' "$T/a.md"` — 편집 전 1, 좋은 모의본 0, `mock_stale3.py` 1.

### 권고 (막지 않음)

- SK-04 (d) 의 `아래 16개 항목` · `아래 10개 항목` · `§11 parity 표 16 번째` 는 「정확히 1」이다. 같은 인용을 한 번 더
  쓰면(예: 새 소절 두 곳에서 16 번째를 인용) 뜻이 맞아도 떨어진다. 「1 이상」으로도 조건의 뜻은 다 선다
- 서명 줄 `Kaizen-Phase:` 는 러닝북에 없고 이 계약에만 있다. FIX 가 빠뜨리면 AR-04 ① 이 떨어진다(스스로 드러나서
  치명적이지는 않다). FIX 에게 넘기는 글이나 notes 에 한 줄 적어 두면 한 바퀴를 아낀다

### 다시 낼 때

조건 수는 25 그대로다. 바뀌는 곳은 AR-02 · AR-03 두 조건, `봉인 전 실측` 표 두 줄, `범위 경계` 커버리지 해소 한 줄,
개선안 `:165` 한 줄이다. 위 값은 이 검토에서 실제로 돌린 값이라 그대로 옮겨도 된다. 이 두 가지만 들어가면 나머지는
이대로 봉인해도 된다고 본다.

VERDICT: CHANGES
