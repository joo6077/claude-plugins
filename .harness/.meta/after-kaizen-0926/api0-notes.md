# api-kit -0 분리 — 기록 (2026-09-26)

계약 `.harness/sprint-contract-after-0924-api-negzero.md` (봉인 `42659fdebb3e228a`, 커밋 `8c73f2c`). 가지 `chore/ak-api0`, 기준 `cdadb10`(V10 PR #111 뒤 origin/main).

- 한 일: `38b6076` 킷 스킬 셋(api-contract · api-verify · api-probe) — `-0` 을 I-JSON 게이트 목록에서 빼 게이트 다음 -0 검사로, noncharacter 를 세 목록에 맞춤 · `2ca8942` 원본 문서 0.1.2 · 문서 페이지 · 연구 기록 절 · `f20f3b0` 근거 파일(Codex 원문 대조).
- 근거: RFC 7493 §2.1 이 surrogate · noncharacter 를 MUST NOT 으로 막고, `-0` 규칙은 없다(RFC 8259 문법상 올바른 숫자). `-0` 을 막는 근거는 RFC 8785 정정 7920 의 SHOULD.
- QA 1 회차 APPROVE 18/18. 교차 진단(봉인 전) 지적 여섯 반영 — 가장 큰 것은 측정 표시가 백틱 표기를 못 알아보던 것과 기준 커밋이 V10 합침 전 값이던 것. 부모 교차 진단(QA 뒤): 0 기대 칸 모두 고치기 전 값이 1 이상이라 공허한 통과 아님.
- 버전 판단: api-kit patch (분류 · 동작 변화 없이 이름 · 근거 · 목록 정정). 같은 가지 묶음이 합쳐지면 한 번만 올린다(`ak-c3c` · `ak-c4a` 도 api-kit 을 고친다).
- 측정 도구: scratchpad `api0-measure.py`(지문 `9b4127b764ed5a62`) · `api0-apply.py` · `page-overflow.cjs` — 세션이 끝나면 사라진다. 백업 `../api0-backup/`.
- 다음에: binary64 밖 숫자는 RFC 7493 이 SHOULD NOT 인데 킷은 실패로 막는다 — 연구 기록에 「표준보다 엄격한 쪽」 으로 적었다. 킷 문서에도 그 강도 차를 밝힐지는 다음 api-kaizen 몫.
