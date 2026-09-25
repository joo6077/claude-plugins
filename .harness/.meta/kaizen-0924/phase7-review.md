# 카이젠 2026-09-24 Phase 7 (backend-kit) — 계약 초안 검토

- 대상: `.harness/sprint-contract-kaizen-0924-p07-backend-kit.md` (봉인 전 초안, 조건 26 · 기능 조건 16)
- 개정 파일 `.harness/sprint-amendments-kaizen-0924-p07-backend-kit.md` 은 아직 없다 — BUILD 가 `end_sha:` 를 적을 때 만든다. 검토에 영향 없음
- 검토자: 독립 Claude 검토자(REVIEW 역할). 사용자 승인 대신이다. 파일은 이 검토 결과 하나만 썼다
- 다시 돌린 자리: `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p7review/`

## 결론

고칠 것 두 가지가 있어 **CHANGES** 다. 나머지는 봉인해도 된다.

1. **SK-09** — 이 Phase 가 이미 고치는 절 두 곳에 옛 `[미검증]` 표기가 남는다. backend-audit Gotcha 11 본문의 「근거에 이유를 기술하라」가
   바로 뒤 새 네 칸 예시와 어긋나고, backend-reviewer `## 출력 포맷` 예시 4 행의 「4 요건 충족(호출 로그·…)」가 바로 위 새 규칙 줄과 어긋난다.
   마지막 값(옛 표기 0 줄)은 작성자가 고른 문자열 넷만 찾으므로 둘 다 통과한다. 평가 에이전트는 규칙 줄보다 예시 행을 따라 쓴다.
2. **ER-01** — notes 의 URL 출처를 재지 않는다. 러닝북은 notes 「킷 로그 한 단락」의 출처 URL 을 근거 파일에서만 가져오라고 한다.
   notes 도 이 Phase 가 커밋하는 산출물인데, 지금 측정은 열한 파일만 본다.

두 가지 모두 아래 「고칠 문구」대로 바꾸면 된다. 바꾼 판을 예행 저장소에서 미리 재 두었다.

## 다시 돌려 본 것

계약 파일에서 `common.sh` · `m.sh` · `new-warnings.sh` 세 블록을 그대로 뽑았다. 초안 작성자의 도우미 폴더(`p7d/k/`)와 글자까지 같았다.
그 블록으로, 계약 파일 자체를 봉인한 예행 저장소(초안의 `rehearse.sh` · `mock.py` 를 내 폴더에서 다시 돌림)를 쟀다.

| 무엇 | 결과 |
| --- | --- |
| 예행 판 전 조건 (SK-01 ~ SK-09 · ER-01 ~ ER-03 · AR-01 · AR-02 · RE-02 · AP-01 · AP-03 · AP-04 · DG-02 · DG-05 · DG-06) | 계약 `회귀 게이트` 표의 요구값과 전부 같다 |
| 시작 커밋 판 (SK-01 ~ SK-09 · AR-02) | 표의 「시작 커밋 판」 값과 전부 같다. 예: SK-07 첫 값 3, SK-08 셋째 값 2, SK-09 마지막 값 8 |
| 변형 `cross-phase` | ER-03 셋째 값 1 · AR-01 ② `1 11` · DG-06 `scope-isolation: FAIL` · `violators=1 mine=1` |
| 변형 `unsigned-shared` | ER-03 셋째 값 1 |
| 내가 고른 망가뜨리기 다섯 | 원칙 10 의 「이 항목은 RFC 요구가 아니라 이 킷의 규칙이다」만 지움 → SK-01 열한째 값 0 · 사례 8 assertion 하나를 `check` 로 → `rc=1 Total: 7 passed, 1 failed` · reviewer 출력 포맷 줄을 옛 문구로 → SK-09 여섯째 줄 `0 0`, 마지막 값 1 · 조건 줄 한 글자 변조 → `SEAL_BROKEN` · §3 표 가운데 빈 줄 → SK-04 셋째 줄 `8 1` |
| 개정 파일 없이 `common.sh` 를 읽음 | `END_UNRESOLVED` 를 찍고 종료 코드 2 — 상한이 비면 멈춘다는 장치가 살아 있다 |

봉인 전 실측은 표에 적힌 대로 됐다. 값을 잠그는 조건, 0 을 기대하는 조건의 양성 대조, 시험 통과 조건의 음성 대조가 다 있다.

## 물어본 항목별 판정

**조건마다 FAIL(불합격) 상태를 한 문장으로 쓸 수 있는가** — 쓸 수 있다. 예: 「database.md 에 원칙 10 제목이 없거나 원칙 9 뒤 · 수치 기준 앞이 아니면 SK-01 FAIL」,
「구간 안에서 공유 파일 · 다른 Phase 파일을 건드린 커밋 가운데 다른 Phase 서명이 없는 커밋이 1 개 이상이면 ER-03 FAIL」. DG-06 은 예외 가르기가 길지만
「scope-isolation 이 FAIL 인데 위반 커밋 목록을 하나도 못 읽었거나 그 안에 이 Phase 서명 커밋이 있으면 FAIL」로 한 문장이 된다.

**측정이 의도를 재는가** — 대체로 그렇다. 새 문장은 절 · 줄 단위로 잘라 재고, 문장 하나만 지운 사본에서 값이 떨어진다(초안 67 개, 내가 다섯 개 더).
빈 곳은 위 결론의 둘이다. SK-09 의 「옛 표기 0 줄」은 옛 문자열을 먼저 전부 찾아 놓고 세야 하는데, 찾은 목록이 이 Phase 가 고치는 절 안의 두 자리를 놓쳤다.
검토 중 모의 편집 뒤 `backend-kit/` 에서 「사유 · 이유」와 미검증이 한 줄에 같이 나오는 곳을 grep 으로 찾고, 새 규칙 줄이 든 절은 통째로 읽었다. 남는 곳은 셋이다 —
backend-audit `:25` 본문 · backend-reviewer `:64` 예시 행 · backend-audit `:114`. 셋째(`:114` CONDITIONAL APPROVE 보고 문구 「미검증 1 건: [체크항목] — [이유]」)는
reviewer `:107` 원본 복제 조항의 「[조건/항목 ID, 사유, 시도한 fallback 단계]」와 같은 모양이라 그대로 두는 편이 맞다(backend-kaizen Gotcha 8 — 복제 조항은
문구를 바꾸지 않는다). notes 「그대로 둔 곳」에 한 줄 적기를 권한다.

**처리 배정표 Phase 7 행** — `배정` 이 `Phase 7` 인 행은 `backend-family:P2` 하나다(`grep` 로 확인). 계약이 SK-01 ~ SK-05 · AR-02 로 받고, rust-model 부분은
ER-03 이 notes 의 `rust-model` 넘김으로 잰다. F20(Phase 11 행)의 「시간대를 설정값으로」 부분만 맡고 폐기 결정 기록 자리는 Phase 11 로 넘긴 것도 맞다.
러닝북 `Phase 별 추가 과제` 에 Phase 7 줄은 없고, 앞 Phase notes 넷 가운데 Phase 7 로 넘긴 줄도 없다(Phase 4 notes 는 `backend-family:P3` · `P4` 를 Phase 8 · 9 로 넘겼다).
근거 파일 §4 권장안 여섯 항목도 모두 반영 또는 넘김으로 다뤄졌다.

**범위** — 열한 파일이 전부 `backend-kit/` · `docs/backend/` 안이고, 나머지는 `.harness/` 다. 러닝북 표의 Phase 7 범위 안이다.

**공유 파일** — 건드리지 않는다. ER-03 이 루트 README · CLAUDE.md · marketplace · plugin.json · 문서 사이트 HTML · 처리 배정표 등 열네 경로를 직접 세고,
AP-04 가 머리 설정 블록이 그대로인지 잰다. `backend-kit/README.md` 에 AUTO 구간은 0 개다(`grep -c AUTO` 0).

**조건끼리 부딪힘** — 찾지 못했다. SK-05(README 53 행)와 SK-06(README 59 행 이력 그대로)은 다른 줄, AR-02 (c)(reviewer 52 행 그대로)와 SK-09 (d)(57 행)도
다른 줄이다. AR-01 ②의 「열한 파일 전부」는 SK 조건들이 열한 파일을 모두 고치므로 맞물린다. 아래 고칠 문구를 넣은 판에서도 DG-02 · AR-01 · ER-02 · ER-03 ·
AP-01 · AP-03 · AP-04 · SK-08 · DG-05 값이 그대로다.

**그 밖에 확인한 것** — 조건 수 26 · 기능 조건 16 은 Step 6.2 두 명령 출력과 같다. `##` 제목은 모두 허용 목록 안이다. 리서치 소스 절과 모의 편집이 새로 넣는
URL 은 전부 근거 파일에 있다. 번역투 정규식은 `tone-kit/references/locale-korean.md` §2 grep 열과 글자까지 같다. 이번 사이클 Phase 3 이
`qa-evaluation-guide.md` 를 고쳤지만 `## Canonical Unverified-Evidence Protocol` 절은 사이클 시작 판과 같아서 reviewer 복제본을 다시 맞출 일은 없다.

## 고칠 문구

### SK-09

조건 줄(봉인 대상 첫 줄)에서 세 군데를 바꾼다. 화살표 왼쪽이 지금 문구, 오른쪽이 바꿀 문구다.

```text
(b) `backend-kit/skills/backend-audit/SKILL.md` Gotcha 11 예시 · Gotcha 12 · DB 엔진 문단
→ (b) `backend-kit/skills/backend-audit/SKILL.md` Gotcha 11 본문과 예시 · Gotcha 12 · DB 엔진 문단

(d) `backend-kit/agents/backend-reviewer.md` `## 출력 포맷`
→ (d) `backend-kit/agents/backend-reviewer.md` `## 출력 포맷` 의 규칙 줄과 예시 4 행

옛 표기 넷(`[미검증] <사유>` · `` `[미검증]` + 사유 `` · 「pool 설정 파일 정적 리뷰만 수행」 · `` `[미검증]` 태그 + 이유 ``)이 0 줄이다
→ 옛 표기 여섯(`[미검증] <사유>` · `` `[미검증]` + 사유 `` · 「pool 설정 파일 정적 리뷰만 수행」 · `` `[미검증]` 태그 + 이유 `` · 「근거에 이유를 기술하라」 · 「4 요건 충족(호출 로그」)이 0 줄이다
```

둘째 줄(Given/When/Then)의 요구값과 양성 대조 값은 이렇게 바꾼다 (값 끝의 공백은 `toks` 출력 그대로다).

```text
Then: 여덟 줄이 `1 1 ` · `1 1 1 1 1 ` · `1 1 1 1 1 1 ` · `1 1 ` · `1 1 ` · `1 1 1 ` · `1 1 1 1 ` · `0`.
여덟째 값은 시작 커밋 판에서 9(양성 대조 — Gotcha 11 은 옛 표기 둘이 한 줄에 있어 줄 수로는 9)
```

모의 편집(`mock.py` 끝, `print` 앞)에 두 치환을 더한다. 둘 다 시작 커밋 판에 옛 문자열이 한 번씩만 있다.

```python
rep(AU, "`[미검증]` 태그를 붙이고 근거에 이유를 기술하라 (예:",
    "`[미검증]` 태그를 붙이고 근거에 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 채워라 (예:")
rep(RV, "production Kafka broker 접근 불가 — 4 요건 충족(호출 로그·DDL 정적 fallback·실패 출력·재검증 명령 기재)",
    "막는 것: broker 접속 명령과 그 거부 출력 · 시도한 우회: outbox 테이블 DDL 정적 확인 · 통제 불가 사유: 감사자에게 운영 broker 접속 권한이 없다 · 재검증 명령: 권한을 받은 뒤 같은 접속 명령")
```

`m.sh` 의 `SK-09)` 갈래 세 곳:

```bash
# Gotcha 11 줄 — 앞에 토큰 하나를 더한다
    toks "$L" '근거에 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 채워라' '막는 것: 운영 DB 접속 명령과 그 거부 출력' …(뒤는 그대로)
# 출력 포맷 절 — 끝에 토큰 하나를 더한다
    toks "$S" '와 네 칸(…)을 근거 열에 적는다' '하나라도 비면 `INVALID` 다' '막는 것: broker 접속 명령과 그 거부 출력 · 시도한 우회: outbox 테이블 DDL 정적 확인'
# 옛 표기 0 줄 — 두 문자열을 더한다
    grep -rF -e '[미검증] <사유>' -e '`[미검증]` + 사유' -e 'pool 설정 파일 정적 리뷰만 수행' -e '`[미검증]` 태그 + 이유' -e '근거에 이유를 기술하라' -e '4 요건 충족(호출 로그' "$E/backend-kit" | grep -c . ;;
```

함께 고칠 서술: `## 배경` 표 마지막 행 「옛 표기 여덟 자리」 → 「옛 표기 열 자리(아홉 줄)」. `### 1.4` 표의 backend-audit 행에 `:25` 본문, backend-reviewer 행에
`:64` 예시 행을 더한다. `### 개선안 초안` 의 「치환 서른일곱」 · `mock applied 37` → 서른아홉 · `39`, 5 항에 「Gotcha 11 본문」, 6 항에 「예시 4 행」.
모의 research-log 변경 요약 표도 backend-audit 행 「Gotcha 11 예시」 → 「Gotcha 11 본문 · 예시」, backend-reviewer 행 「출력 포맷의 미검증 표기와 예시 행을 네 칸으로」.
`회귀 게이트` 표 SK-09 행과 「문장 삭제 사본」 수(SK-09 18 → 20, 전체 67 → 69)도 BUILD 가 `del.sh` 를 다시 돌려 고친다. 새 토큰 둘은 내가 먼저 돌려 봤다 —
reviewer 예시 행을 옛 문구로 되돌리면 여섯째 줄 `1 1 0` · 마지막 값 1, Gotcha 11 본문을 옛 문구로 되돌리면 셋째 줄 첫 값 0 · 마지막 값 2.

notes 「그대로 둔 곳」에 권장: `backend-kit/skills/backend-audit/SKILL.md:114` 「미검증 1 건: [체크항목] — [이유]」 — reviewer 복제 조항 5 의 보고 모양과 같아 그대로 둔다.

### ER-01

조건 줄과 둘째 줄을 이렇게 바꾼다 (둘째 줄의 `…` 는 지금 문구 그대로).

```text
- [ ] ER-01: 열한 파일에 새로 생긴 URL 과 `.harness/.meta/kaizen-0924/phase7-notes.md` 의 URL 이 전부 이 Phase 의 외부 근거 파일 `.harness/.meta/evidence/phase7.md` 에 있다 — 열한 파일은 파일마다 편집 전 판과 비교한다 (러닝북 — notes 킷 로그 한 단락의 출처 URL 은 근거 파일에서만) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-01` 두 줄이 `0` · `0`. … 양성 대조: 예행 판 database.md 끝에 `https://example.invalid/x` 를 더하면 첫 줄 1, notes 끝에 같은 URL 을 더하면 둘째 줄 1)
```

`m.sh` 의 `ER-01)` 갈래 끝에 한 줄을 더한다:

```bash
    for f in "${FILES[@]}"; do comm -13 <(url < "$T/B/$f") <(url < "$E/$f"); done | sort -u | comm -23 - <(url < "$E/$EVID") | grep -c .
    url < "$E/$NOTES" | comm -23 - <(url < "$E/$EVID") | grep -c . ;;
```

### 고친 판을 미리 잰 값

`p7review/mock2.py`(치환 39) · `p7review/k2/m.sh`(위 두 갈래를 고친 판)로 예행 저장소 `p7review/rh2` 를 만들어 쟀다.

| 조건 | 값 |
| --- | --- |
| SK-09 | 위 「Then」 블록과 같다 (시작 커밋 판 마지막 값 9) |
| ER-01 | `0` · `0` (notes 에 근거 밖 URL 을 넣으면 둘째 줄 1) |
| DG-02 | 열 줄 모두 `new_warnings=0` (backend-reviewer 더한 줄 2 → 3) · `json_ok` |
| AR-01 | `0` · `0 11` · `0` · `SEAL_OK` · `scope_same=1` · `1` |
| ER-02 · ER-03 · AP-01 · AP-03 · AP-04 · SK-08 · DG-05 | 고치기 전과 같다 |

## 권장 (봉인을 막지 않음)

1. `## 범위 경계` 끝에 `사용자가 할 일: 없음` 한 줄 — sprint-contract Step 5 가 2026-09-24 에 넣은 끝맺음이다. 새 `##` 제목을 만들지 말고 불릿으로 둔다.
2. README 검증 절 둘째 줄 「7 카테고리 구조 감사」 — ER-03 이 다음 사이클로 넘기는데 이유가 없다. 이 Phase 가 바로 윗줄을 고치므로 지금 숫자를 빼고
   「등록된 검사 전부 (개수는 `harness/docs/guides/plugin-validation-guide.md` 가 정한다)」로 고치거나, 넘기는 이유를 notes 에 적는다. 지금 고치면 ER-03 토큰
   `7 카테고리` 도 함께 뺀다.
3. backend-audit Gotcha 16 의 「행도 2026-09-24 사이클에 이 기준으로 고쳤다」는 한 일을 적은 문장이라 읽는 쪽이 할 행동이 없다. 「행도 같은 기준으로 판정한다」
   쪽을 권한다. 바꾸면 SK-08 둘째 줄 토큰도 같이 바꾼다. 이 킷 Gotcha 에 날짜 실측 문장이 흔해 막을 사유는 아니다.
4. backend-kaizen Gotcha 8 은 설계 가이드 새 원칙마다 반영 스킬을 보고서에 적으라고 한다. notes 에 Phase 1 변경 셋(네 칸 · 작업 불가 전 네 칸 · 알려진 답
   대조)을 반영 · 해당 없음으로 나눈 짧은 표를 권한다. 조건으로는 재지 않는다.
5. ER-03 셋째 값은 다른 Phase 가 서명 줄을 단다는 전제에 기댄다. 지금까지 서명 없는 커밋은 오케스트레이터의 근거 파일 커밋(`.harness/.meta/evidence/` 만)뿐이라
   위험은 낮다. 값이 0 이 아니면 QA 가 커밋 목록부터 보고 판정하게 notes 에 적어 둔다.
6. `common.sh` 는 `mktemp -d` 로 두 판을 풀므로 `TMPDIR` 를 스크래치 폴더로 두고 돌린다. 이 검토의 처음 몇 번은 그러지 않아 시스템 임시 폴더에 풀렸고,
   내 예행 저장소의 커밋 값이 든 것만 골라 지웠다(여덟 개, 시작 커밋 판을 재려고 덮어쓴 하나는 가려낼 수 없어 남았다).

참고: 봉인 값은 조건의 첫 줄만 덮는다. 둘째 줄의 요구값과 `m.sh` 는 봉인 뒤 바뀌어도 `SEAL_OK` 다. harness 쪽 과제라 이 Phase 가 고칠 일은 아니다.

VERDICT: CHANGES

## 2 회차

- 대상: 같은 계약 초안(2026-09-25 05:52 저장판 — `p7d/contract.draft.md` 와 글자까지 같다). 개정 파일은 아직 없다
- 검토자: 독립 Claude 검토자(REVIEW 2 회차). 이 파일 끝에 이 절을 더한 것 말고 파일은 고치지 않았다
- 다시 돌린 자리: `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p7r2/`

### 결론

1 회차의 고칠 것 둘(SK-09 · ER-01)과 권장 여섯이 모두 들어갔다. 조건 줄 26 개는 이대로 봉인해도 된다 — **APPROVE**.

새 결함이 하나 있다. 조건 줄 밖이라 봉인 값과 요구값은 바뀌지 않지만, BUILD 가 **봉인 전에** 아래 「고칠 문구」대로 고친다.
계약 218 ~ 219 행 「`TMPDIR` 를 스크래치 폴더로 두고 읽는다」 는 이 맥에서 효과가 없다. `/usr/bin/mktemp -d` 는 틀을 주지 않으면
`TMPDIR` 를 무시하고 시스템 임시 폴더(`/var/folders/…/T/`)에 푼다 — `TMPDIR` 를 스크래치로 두고 bash 5.3.9 · `/bin/bash` 3.2.57 둘 다에서 확인했다.
이 문장은 내 1 회차 권장 6 에서 왔고, 그때 효과를 확인하지 않고 적었다. 지금 그 폴더에 Phase 7 측정이 남긴 두 판 폴더가 약 40 개,
합 1.8 GB 있다. 내가 이번에 만든 일곱 개는 지웠고, 나머지(05:12 ~ 05:52)는 초안 작성 쪽 것이라 두었다.

1 회차 기록 정정: 「Gotcha 11 본문을 옛 문구로 되돌리면 … 마지막 값 2」 는 틀렸다. 다시 재면 셋째 줄 `0 1 1 1 1 1` · 마지막 값 `1` 이다 — 계약 489 행의 값이 맞다.

### 1 회차 지적이 들어갔는지

| 1 회차 지적 | 계약 자리 | 확인 |
| --- | --- | --- |
| SK-09 조건 줄 (b) 「Gotcha 11 본문과 예시」 · (d) 「규칙 줄과 예시 4 행」 · 옛 표기 여섯 | 532 행 | 들어감 |
| SK-09 요구값 여덟 줄 · 시작 커밋 판 9 | 533 행 | 들어감. 다시 재어 같다 |
| `m.sh` SK-09 갈래 세 곳 | 375 ~ 387 행 | 1 회차 제안 `p7review/k2/m.sh` 와 줄 나눔만 다르다 |
| 모의 편집 두 치환 | `p7d/mock.py` | 들어감. 치환 수 40 — 39 에 권장 2 의 README 한 줄이 더해졌다 |
| 배경 · 1.4 · 개선안 · 대조 표 · 문장 삭제 수 | 23 · 88 · 89 · 117 · 128 · 130 · 489 · 505 행 | 들어감. 문장 삭제 70 = 67 + SK-09 둘 + SK-05 README 하나 |
| ER-01 조건 줄 · 둘째 줄 · `m.sh` | 542 ~ 545 · 388 ~ 391 행 | 들어감. 제안보다 하나 낫다 — notes 가 없으면 `NOTES_MISSING` 을 찍는다(제안대로면 조용히 0) |
| 권장 1 「사용자가 할 일: 없음」 | 207 행 | 들어감 |
| 권장 2 README 「7 카테고리 구조 감사」 | 24 행 · SK-05 셋째 줄 · ER-03 토큰 `infra-kit/README.md` | 이번에 고치는 쪽으로 들어감. 레포 전체에 같은 줄은 `backend-kit/README.md:54` 와 `infra-kit/README.md:54` 둘뿐이다(시작 커밋 판 `git grep`) |
| 권장 3 Gotcha 16 문장 | SK-08 둘째 토큰 | 「행도 같은 기준으로 판정한다」 로 들어감 |
| 권장 4 · 5 · 참고(봉인 값이 첫 줄만 덮음) | 201 ~ 205 행 notes 할 일 | 들어감 |
| 권장 6 `TMPDIR` | 218 ~ 219 행 | 들어갔지만 효과가 없다 — 위 결론 |

### 다시 돌려 본 것

계약에서 세 블록을 뽑았다 — `p7d/k/` 와 글자까지 같다. 초안의 `rehearse.sh` 를 내 폴더로 옮기고(모의 편집 · notes 모의본은 복사) 예행 저장소 다섯
(기본 + 변형 넷)을 새로 만들었다. 시작 커밋은 지금도 `HEAD` 다(`7925890..HEAD` 커밋 0 개).

| 무엇 | 결과 |
| --- | --- |
| 시작 커밋 사본에 `mock.py` | `mock applied 40` |
| 예행 판 21 개 조건 + SC-00 · DG-01 · DG-04 · RE-01 측정 | 표 479 ~ 503 행 요구값과 전부 같다. 더한 줄 합 132, DG-02 더한 줄 29 · 5 · 59 · 4 · 3 · 6 · 6 · 3 · 2 · 2 |
| 시작 커밋 판 SK-01 ~ SK-09 · AR-02 · AP-01 · AP-03 · RE-02 | 표의 「시작 커밋 판」 값과 전부 같다. 예: SK-05 셋째 줄 `0 1 0 1`, SK-09 마지막 값 9 |
| 변형 넷 | `unsigned-shared` ER-03 1 · `unsigned-mine` AR-01 ① 1 · `signed-outside` ER-03 1 · AR-01 ② `1 11` · SC-00 1 · `cross-phase` ER-03 1 · DG-06 `scope-isolation: FAIL` · `violators=1 mine=1` |
| 새 대조 여섯 | reviewer 예시 행을 옛 문구로 → SK-09 여섯째 줄 `1 1 0` · 마지막 값 1. Gotcha 11 본문을 옛 문구로 → 셋째 줄 첫 값 0 · 마지막 값 1. database.md 끝에 `https://example.invalid/x` → ER-01 `1` · `0`. notes 끝에 → `0` · `1`. notes 를 지운 사본 → `0` · `NOTES_MISSING`. README 새 줄을 옛 문구로 → SK-05 셋째 줄 `1 0 0 1` |
| 문장 삭제 사본 `p7d/del.sh` | `DROP` 70, 그 밖 0 (SK-01 15 · SK-02 8 · SK-03 7 · SK-04 9 · SK-05 1 · SK-06 2 · SK-07 4 · SK-08 4 · SK-09 20) |
| ER-01 새 (파일, URL) 쌍 | 14 — database.md 2 · api-design.md 2 · research-log 5 · backend-system 2 · backend-guide 1 · audit-criteria 2 |
| `/bin/bash` 3.2.57 로 21 개 조건 | bash 5.3.9 출력과 한 글자도 다르지 않다(아래 고친 `common.sh` 로 잰 값이라 고친 판이 값을 바꾸지 않는다는 확인도 된다) |
| Step 6.2 · 6.5 (레포의 sprint-contract SKILL.md · contract-schema 검출기 그대로) | 조건 26 · 기능 조건 16 · `OK conditions=26` · `##` 제목 12 개 모두 허용 목록 안 · 체크박스는 조건 절에만 · `UNCOVERED` 9 건(SK-01 · SK-02 · SK-04 · SK-06 · SK-09 · ER-01 · ER-03 · AR-01 · AR-02) 모두 190 ~ 198 행에 해소 줄 · `[미실측]` 0 |
| 1.4 표 줄 번호 | 시작 커밋 판 backend-audit `:25 26 30 49 80 89 114` · reviewer `:33 52 57 62 64 110` · README `:53 54 59` · backend-test `:28 256` · evals `:50 81` 을 열어 표 설명과 맞는 것을 확인 |
| 모의 편집 뒤 남은 옛 표기 | `backend-kit/` 에서 `[미검증` 이 든 줄 가운데 네 칸이 없는 줄을 다 읽었다. 사유 한 줄 꼴은 1 회차에 그대로 두기로 한 두 자리(backend-audit `:114` · reviewer `:107` 복제 조항)뿐이다 |

새 문장 셋(Gotcha 11 본문 · reviewer 예시 4 행 · README 검증 절 둘째 줄)도 읽었다. 앞뒤 문장과 어긋나는 곳, 번역투, 특정 앱 이름은 없다.
reviewer 예시 행의 네 칸은 바로 아래 `UNVERIFIED_ENV` 남용 방지 4 요건(1 차 도구 시도 · 우회 시도 · 실패 출력 · 통제 불가 사유와 재검증 명령)에 대응한다.

### 고칠 문구 (봉인 전 BUILD)

`common.sh` 한 줄 — 화살표 왼쪽이 지금, 오른쪽이 바꿀 것.

```text
T=$(mktemp -d); mkdir -p "$T/B" "$T/E"
→ T=$(mktemp -d "${TMPDIR:-/tmp}/p7m.XXXXXX") || exit 2; mkdir -p "$T/B" "$T/E"
```

218 ~ 219 행 문장.

```text
`common.sh` 는 `mktemp -d` 로 두 판을 풀므로 `TMPDIR` 를 스크래치 폴더로 두고 읽는다
(검토 중 실측: 두지 않으면 시스템 임시 폴더에 풀린다).
→ `common.sh` 는 두 판을 `${TMPDIR:-/tmp}/p7m.XXXXXX` 에 풀므로 `TMPDIR` 를 스크래치 폴더로 두고 읽는다. 틀 없는 `mktemp -d` 는
이 맥에서 `TMPDIR` 를 무시하고 시스템 임시 폴더에 푼다(2 회차 검토 실측 2026-09-25 — 한 번 읽을 때마다 40 ~ 70 MB 가 남았다).
```

확인: 고친 판(`p7r2/k3/common.sh`)은 `TMPDIR` 를 두면 스크래치 폴더에, 비우면 `/tmp` 에 푼다. 21 개 조건 값은 고치기 전과 같다(bash 두 판 모두).
조건 줄을 건드리지 않으므로 봉인 값이 그대로다. 봉인 뒤에 고치게 되면 이 블록은 조건이 가리키는 산문이라 개정 파일에 「통과 집합이 안 바뀐다」 한 줄을 남긴다.

VERDICT: APPROVE
