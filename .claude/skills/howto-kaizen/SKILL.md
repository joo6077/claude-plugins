---
name: howto-kaizen
description: >
  howto-kit 스킬 3종·에이전트 1종·references 5종·게이트 G1~G6 의 품질을 docs/howto/ 리서치
  문서와 실측 피드백 기준으로 주기 개선한다.
  이 레포 개발용 스킬이며 howto-kit 플러그인에 포함되지 않는다.
  tone-kaizen, api-kaizen 과 동일한 패턴.
  "/howto-kaizen", "절차 카이젠", "howto-kit 개선" 같은 요청 시 트리거.
  리서치 문서 갱신에는 트리거하지 않는다 — /howto-research 를 사용한다.
argument-hint: ""
user-invocable: true
---

# Howto Kaizen

`howto-kit` 스킬·에이전트·references·게이트를 리서치 문서 기준으로 개선한다.

# Gotchas

1. **게이트를 고쳤으면 양성 케이스로 실행해 증명하라.** 서술 존재는 증거가 아니다.
   `sh howto-kit/evals/run-evals.sh` 를 돌리고 `EVALS_PASS` 출력을 인용한다.
   준수 상태에서 0 건이 정상인 패턴은 **일부러 위반한 픽스처**로 살아 있음을 보인다 —
   오탐 통과만으로는 게이트 생존이 증명되지 않는다.
2. **게이트 수정은 zsh·bash 양쪽에서 돌려라.** 실측 2026-09-08: `set -- $var` 가 zsh 에서
   단어분할되지 않아 G5·G6 위반이 zsh 에서만 `GATE_PASS` 로 샜다. bash 만 돌렸으면
   못 잡았을 결함이다. eval runner 가 두 셸 출력 동일성까지 검사한다.
3. **게이트 마커를 바꾸면 `references/step-contract.md` 를 짝으로 고쳐라.** 한쪽만 고치면
   게이트가 조용히 0 건을 세고 그 0 건이 PASS 로 보인다.
4. **임계 숫자를 이 킷에서 재정의하지 마라.** `[미검증]` 마커 임계는
   `harness/docs/guides/qa-evaluation-guide.md` 가 정본이다. 킷별 재정의가 같은 상태를
   다른 판정으로 가르는 drift 를 낳았다 (실측 2/3/0 건).
5. **판정 불가를 PASS 로 흘리지 마라.** G3 가 대상 미선언에서 FAIL 하는 것은 버그가 아니라
   설계다. 기존 킷의 G3 는 stack 이 비면 항상 PASS 해서 3 개월간 아무것도 못 잡았다.
6. **`추정` 을 금지로 바꾸지 마라.** 이 킷의 핵심 전제는 "등급을 붙여 파는 것은 정직하다"이다.
   `추정` 을 금지하면 기존 킷이 만든 "이 섹션에서 찾으세요" 결함으로 되돌아간다.
7. **description 변경은 사용자 승인을 받아라.** 트리거 어휘를 바꾸면 배타성이 깨질 수 있다.
   변경 시 set intersection **과** substring containment 를 다시 계산한다 —
   `validate-plugin.py` V4 는 set intersection 만 본다.
8. **스킬 3 개 상한을 유지하라.** 별도 interview 스킬을 만들지 마라 — 선행 질문은 `/howto`
   내부의 한 단계이며, 분리하면 되묻기 왕복이 오히려 늘어난다.
9. **`references/provenance-notes.md` 를 비우지 마라.** 미확정 항목이 줄어드는 것은 좋지만,
   확인 실패를 조용히 삭제하는 것은 이 킷이 막으려는 결함 그 자체다. 확정으로 옮길 때만 지운다.
10. **온보딩 킷을 건드리지 마라.** `onboarding-kit` 은 별도 킷이고 별도 결함 목록을 갖는다.

# Process

## Step 0. 트리거 선별

직전 사이클과 같은 신호로 도는 것은 낭비다. 아래 중 하나 이상이 있을 때만 진행한다.

- `docs/howto/` 에 새 리서치 반영분이 있다
- `howto-kit/references/provenance-notes.md` 의 항목이 확정으로 바뀔 근거가 생겼다
- 게이트가 놓친 실패 사례가 실측으로 잡혔다
- 사용자 피드백에 절차 안내 관련 불만이 새로 들어왔다

없으면 그 사실을 보고하고 종료한다.

## Step 1. 현행 상태 측정

```bash
python3 scripts/validate-plugin.py howto-kit
sh howto-kit/evals/run-evals.sh
```

두 출력을 그대로 기록한다. 개선 전 baseline 이다.

## Step 2. 개선 대상 선정

한 사이클에 **1~2 개 surface** 만 수정한다. 판정은 파일 수가 아니라 관심사 수 기준이다.

## Step 3. 수정 + 증명

게이트를 손댔으면 Gotcha 1·2 를 그대로 수행한다. 새 검사를 추가했으면 **양성 케이스 픽스처를
같이 추가하고 evals 케이스로 등록한다.** 픽스처 없는 새 게이트는 죽은 가드다.

## Step 4. 회귀 확인

```bash
python3 scripts/validate-plugin.py howto-kit
sh howto-kit/evals/run-evals.sh
python3 scripts/sync-docs.py --check-only
```

세 명령이 모두 통과해야 완료다.

# References

- `howto-kit/references/step-contract.md` — Step Contract 스키마 정본
- `howto-kit/references/provenance-notes.md` — 미확정 근거 원장
- `howto-kit/scripts/howto-gate.sh` — 게이트 G1~G6 구현
- `harness/docs/guides/skill-design-guide.md` — 스킬 설계 아키타입
- `harness/docs/guides/qa-evaluation-guide.md` — 마커 임계 정본
