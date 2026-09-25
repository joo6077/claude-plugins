---
slug: kaizen-0924-p17-howto-kit
created: "2026-09-25 13:47"
---

# kaizen-0924-p17-howto-kit 개정

이 파일은 범위 상한 `end_sha` 를 적는 자리다. 봉인 뒤 조건은 바꾸지 않았다 — 개정 0 건. 봉인 뒤 계약의 산문도 고치지 않았다.

봉인 전에 BUILD 가 고친 곳: `## 범위 경계` 의 승인 대체 줄에 검토 2 회차 최종 판정(`.harness/.meta/kaizen-0924/phase17-review.md` `## 2 회차`, `VERDICT: APPROVE`)을 적고,
2 회차 권고 R3 대로 「notes 에 함께 적는다」 줄의 26514 · DITA 2.0 · `cache` 를 `## 미반영 키와 사유` 로 옮겼다. 둘 다 조건 줄이 아니라
봉인 값 `33e681f97ba3081e` 는 예행 저장소 `kaizen/p17/rh-final` 의 봉인 값과 같다. 이 편집은 모두 봉인 커밋에 들어 있다.

구현이 예행과 다른 곳 하나 — `amend_direction: unchanged`. 러너 `howto-kit/evals/run-evals.sh` 는 예행 도구 `new/run-evals.sh`(앞 16 자리 `47e5292a9e2b120c`)에서
새로 쓴 줄의 한 글자 변수 이름만 바꿨다(`tone-kit/references/core-naming.md` N-08 SHOULD — `a` → `assertion`, `tag a b c` → `tag rel declared found`,
블록 경우 `c` · `f` · `n` → `where` · `script` · `expect`, 파이썬 `b` · `n` · `i` · `m` → `body` · `expect` · `seq` · `hit` 등). 동작은 같다 —
조건 줄은 러너의 지문을 재지 않고 출력만 잰다(SK-07 · SK-08 · RE-01 · DG-04). 편집 전부터 있던 줄(`for c in data['cases']`)은 그대로 뒀다.

측정 공통 정의가 아래 `end_sha:` 줄의 마지막 값을 `END` 로 읽는다. 커밋을 더하면 새 값으로 한 줄을 **덧붙인다**
(옛 줄은 지우지 않는다). 그 커밋 메시지에도 서명 줄 `Kaizen-Phase: kaizen-0924-p17-howto-kit` 를 넣는다 — 빠지면
AR-01 첫째 값이 떨어진다.

- 봉인 커밋: `98f4d5ece091b5ef0464cee660e134a4e38df567` (계약 파일 1 개, `conditions_digest: sha256:33e681f97ba3081e`)
- 구현 커밋: `5a96f7c7a0f7aa301aceae1024e1b2e010be0bf2` — `howto-kit/` 일곱 파일 (계약 범위 선언 일곱)
- notes 커밋: `04a0e763ac2fedc4570c72fdefdfcea3608ff55b` — `.harness/.meta/kaizen-0924/phase17-notes.md` · `phase17-review.md`. 범위 상한을 이 커밋으로 옮긴다

end_sha: 5a96f7c7a0f7aa301aceae1024e1b2e010be0bf2
end_sha: 04a0e763ac2fedc4570c72fdefdfcea3608ff55b
