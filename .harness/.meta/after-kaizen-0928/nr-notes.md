# nr — 새 규칙 넷 작업 기록 (2026-09-29)

계약 `.harness/sprint-contract-after-0929-four-new-rules.md` (25 조건, 봉인 `sha256:b809213f05ea2d04` · 측정 `sha256:a142377bc0fe31be`).
가지 `chore/ak3-nr`, 시작 판 `279085a3`. 봉인 커밋 `77d07bf3`, 측정 도우미 커밋 `b9ccbd96`.

## 봉인 전에 반영한 교차 진단 지적

- 남은 일 A10 의 둘째 몫(`docs/planning/flows.md:61` Mermaid 버전 문장)이 계약에 없었다. 범위 경계 「하지 않는 것」 에 이유와 함께 적었다 — 아래 `남긴 것` 첫 줄.
- 스킬-01 · 스킬-02 는 Gotcha 줄 하나만 잰다. 규칙 글을 그 줄 안에 이어 썼다.

## 규칙별 결과

| 규칙 | 남은 일 | 처리 커밋 | 한 일 |
| --- | --- | --- | --- |
| ① 시각 문자열 | A8 | `299a1c86` · `2e3956ea` · `d3913bc7` | backend-system Gotcha 15 와 감사 Timestamp 행에 `YYYY-MM-DDTHH:mm:ss[.fraction]` · `type: string` · `pattern` · `example` 과 「이 킷이 고른 형식」 표시. 원칙 10 과 그 쪽에 RFC 3339 · ISO 인용 둘과 ISO 출처 |
| ② PRD 와 ADR 경계 | A10 (첫째 몫) | `e42e518d` · `d6fe28e3` · `798d4981` | plan-prd Gotcha 15, `prd-patterns.md` 새 절 「PRD 와 설계 결정 기록(ADR)의 경계」, 쪽의 폐기한 결정 절 · 참고 링크(16 → 19). 경계는 「원문에 직접 근거가 없는 추론」 으로 표시 |
| ③ 조회일과 갱신일 | A12 194 줄 | `a751c1dd` · `0e31bf51` | setup-guide §출처 원장에 두 날짜 문단(「이 킷의 규칙」), 형식 목록 출처 줄 틀에 `Last updated YYYY-MM-DD UTC (원문에 표시가 있을 때만)`, 두 쪽을 같이 맞춤 |
| ④ 서비스 계정 선택 순서 | A12 166 · 180 줄 | `a751c1dd` · `0e31bf51` | setup-guide Gotcha 10(①~⑤, 인용 넷, `조회 2026-09-28 · Last updated 2026-09-24 UTC`), 쪽 Gotchas 10개 체크 · 끝 체크리스트 한 줄 |

## 자기 측정 (W, HEAD `0e31bf51` 기준)

- 스킬-01 `checks=9 missing=0` · 스킬-02 `checks=4 missing=0` · 스킬-03 `checks=7 missing=0` · 스킬-04 `checks=8 missing=0` — 모두 종료 코드 0
- 구조-01 `checks=14 missing=0` · 구조-02 `checks=9 missing=0` · 구조-03 `checks=4 missing=0` · 구조-04 `gotcha_items=1,2,3,4,5,6,7,8,9,10` `checks=7 missing=0`
- 구조-05 `pairs=4 drift_rc=0 new_marks=0`, 바뀐 쪽 네 개 · 구조-06 `pages=4 bad=0 br_rc=0,0 a11y_ok=4/4 a11y_rc=0`
- 오류-01 `quotes=9 bad=0 need_missing=0 ex_len=23040` · 오류-02 `gate_rc=0,0 gate_tail=[GATE_PASS] checks=6 missing=0`
- 구조-08 은 이 기록 커밋 뒤에 다시 잰다(커밋 11 개 예상). 구조-07 은 이 파일이 대상이다
- 스크립트-00 · 재사용-01 빈 출력, 진단-01 · 진단-04 `0`, 금지-02 `forced-update` 0 줄
- 진단-02: 바뀐 md 일곱 파일 markdownlint-cli2(MD013 끔) 모두 `warn=0 ran=1`
- 진단-05: ci-local 25 단계 `rc=0`(`feedback-agg-test SKIP (yq 없음)` 만 예외), `docs-a11y` `204/204 PASS`. CI 전용 단계 전부 0 — `12/12 PASS` · `어긋남 0` · `경우 3 개 중 통과 3` · `검사한 쪽 204 · 어긋난 쪽 0 · 못 읽은 쪽 0` · `경우 6 개 중 통과 6` · `checked=2 violations=0` · `need=0` · `실패 0 건` 넷 · `checked=6 violations=0` · `28 경우 중 불일치 0` · `5 경우 중 불일치 0` · `모든 README가 동기화 상태입니다.` · validate 세 킷 종료 코드 0. `npx playwright test` `172 passed`

## tone-guide 1 단계 · 5 단계

1 단계: 레포 `tone-kit/skills/tone-guide/SKILL.md` 와 `.claude/tone-project.md`(어댑터 없음 · 주석 언어 ko)를 읽고, 이번 글에 걸리는 규칙으로 K-02(번역투 여섯 가지) · K-03(능동 · 직설) · K-04(`한다`체) · K-05(외래어 세 원칙) · K-11(새 이름 만들지 않기) · C-01(왜만 남기기) · S-12(같은 자리는 같은 모양)를 골랐다.

5 단계 대조 — 새로 더한 한국어 글(이번 구간 `+` 줄)이 대상:

| 규칙 | 건수 | 판정 |
| --- | --- | --- |
| K-02 G-1 번역투 여섯 가지 (`locale-korean.md` §8 정규식) | 0 | 통과 |
| K-04 `합니다` · `습니다` 종결 | 0 | 통과 |
| K-05 외래어 | 0 | 통과 — 공식 이름(`ADC` · `Workload Identity Federation` · GKE)은 원문대로, 처음 나올 때 괄호로 뜻을 붙였다(SKILL.md) |
| K-11 새 이름 | 0 | 통과 — 새로 붙인 이름 없이 「조회일」 · 「원문 갱신일」 · 「서비스 계정 가장」 처럼 원래 이름이나 문장으로 적었다 |
| S-12 같은 자리 같은 모양 | 0 | 통과 — Gotcha 는 기존 번호 · 머리 모양, `prd-patterns.md` 새 절은 요약 · 핵심 질문 · 적용 시점 · 한계 · 출처 다섯 칸 |

## 킷 버전 판단

backend-kit 0.5.1 · planning-kit 0.8.0 · onboarding-kit 0.4.2 는 그대로 뒀다. 세 킷 모두 사용자에게 새 규칙을 요구하므로 합친 뒤 릴리스할 때 minor 가 맞다고 본다. 버전 올리기 · 릴리스는 이 묶음 밖이다(계약 범위 경계).

## 남긴 것

- A10 둘째 몫 — `docs/planning/flows.md:61` 「최신 안정판」 문장에 Mermaid 버전 출처와 「렌더해 보지 않았다」 단서를 붙이는 일(`ex/A10.md` 교체안). 사용자 결정(규칙 넷)에 들지 않고, 그 파일을 고치면 드리프트 짝이 다섯이 되어 구조-05 와 부딪힌다. 다음 묶음에서 flows 쪽과 함께 한다.
- 옛 기록 `docs/backend/research-log.md:17,71` · `docs/planning/research-log.md:22` 의 「규칙으로 올리지 않았다 / 고칠 곳이 없다」 — 그때의 기록이라 고치지 않았다.
- 네 규칙을 기계로 막는 새 검사 — 글 규칙이라 만들지 않았다(스크립트-00). 글이 제자리에 있는지는 이 계약의 측정 도우미가 잰다.
- 킷 버전 올리기 · 릴리스 · 합치기 · push — 이 묶음 밖.
- QA 판정 — qa-evaluator 가 APPROVE(PASS 21 · N/A 4 · FAIL 0), 계약 `status: done`. 리포트와 함께 `d14ad55c` 로 커밋했다. 독립 검토는 막는 결함 0.

### 독립 검토가 짚은 작은 결함 셋 (막는 결함 아님)

봉인된 계약이 APPROVE 로 닫힌 뒤라 이 가지에서 고치지 않았다. 고치면 판정 뒤에 범위 파일이 바뀌어 리포트가 잰 판과 달라진다. 다음 묶음에서 새 계약으로 한다.

- `docs/planning/prd-patterns.md:4` 의 `last_updated: 2026-09-25` 와 짝 쪽 `docs/planning-kit/prd-patterns.html:311` 머리 날짜를 안 바꿨다. 이번에 새 절과 출처 셋(조회 2026-09-28)을 더했으니 올려야 한다. 이 묶음이 넣은 「조회일과 갱신일을 따로 적는다」 규칙과 같은 종류의 어긋남이라 먼저 고칠 것.
- `onboarding-kit/skills/setup-guide/SKILL.md:283-287` Gotcha 10 목록이 번호 목록과 ①~⑤ 표지를 같이 써서 「1. ①」 로 그려진다. 둘 중 하나만 남기면 된다. 측정에는 영향이 없다.
- `docs/onboarding-kit/setup-guide.html` 끝 체크리스트(`final-title` 절)에 두 항목(원문 Last updated 를 조회일과 따로 적었다 · 서비스 계정 키는 대안이 없을 때만)이 있는데, 원본 `SKILL.md` Phase 4(342-351 줄)에는 두 규칙을 확인하는 단계가 없다. 스킬만 따라 하면 완료 전에 확인되지 않는다. Phase 4 에 한 단계를 더하고 쪽과 맞춘다.
