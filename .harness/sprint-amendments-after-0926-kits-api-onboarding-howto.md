---
slug: after-0926-kits-api-onboarding-howto
created: "2026-09-27 11:58"
---

# after-0926-kits-api-onboarding-howto 개정

## A-01 — RE-01 · RE-02 측정에서 `.harness/` 를 뺀다 (동의 대기)

- 대상 조건: `RE-01` 의 N/A 사유 측정 `git diff --diff-filter=A --name-only 6378948 chore/ak2-k4 -- scripts '*.sh' '*.py'` 0 줄, 그리고 `RE-02` 가 「RE-01 과 같은 명령 0 줄」 로 같은 측정을 쓴다
- 바꾸려는 측정: 같은 명령 끝에 `':(exclude).harness'` 를 붙인다
- 이유: 계약 `## 범위 경계` 가 측정 도구 네 파일(`m.sh` · `ob.py` · `ka5.sh` · `stub.py`)을 「봉인 커밋 뒤 `.harness/` 만 든 커밋으로 싣는다」 고 정했다. 그대로 실은 커밋 `ee1fac4` 의 `.sh` · `.py` 가 RE-01 측정에 잡혀 0 줄이 될 수 없다. 교차 진단 반영으로 더한 `ci-local.sh` 사본까지 다섯 줄이다. 조건끼리 부딪힌 것이고, 킷 구현에서 새로 더한 스크립트 · 러너 파일은 0 개다(아래 개정 측정 0 줄)
- 실측 (2026-09-27, 가지 끝 `c420af5`):
  - 원 측정 5 줄 — `.harness/.meta/after-0926-kits-api-onboarding-howto/` 의 `ci-local.sh` · `ka5.sh` · `m.sh` · `ob.py` · `stub.py`
  - 개정 측정 0 줄
- 방향 계산: `amend_direction_oracle`(측정 집합 헬퍼, `harness/references/contract-schema.md` §Amendment 사이드카) → `relaxing measured_removed=5 measured_added=0`
- amend_direction_oracle: relaxing
- consent:
- 동의 근거(사용자 발언 · 시각 · 세션):

조건을 느슨하게 하는 개정이라 2026-09-26 위임으로 동의 처리하지 않았다. 사용자 동의가 적히기 전까지 RE-01 · RE-02 는 원 측정으로 잰다(5 줄 → 사유 거짓).
