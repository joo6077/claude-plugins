# cs 묶음 — 계약 형식 문서 · 피드백 형식 (after-kaizen-0926b)

- 작업 폴더 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-cs`, 가지 `chore/ak2-cs`, 기준 판 `6378948`
- 계약 `.harness/sprint-contract-after-0926-contract-schema.md` (32 조건, 봉인 `conditions_digest: sha256:fdaf977d37a36b86` ·
  `measurement_digest: sha256:b588e1b0e6a52014` · `locked_at: 2026-09-26 20:00`)
- 위임: 2026-09-26T10:09:00.557Z 「123다실행해 그러면끝나?다음카이젠에왜넘기는데?」, 결정 답 2026-09-26T10:30:16.222Z,
  세션 `bda55d45-296c-491f-89ba-b52042d58e72`. 조건을 느슨하게 하는 개정은 없다

## 커밋

| 해시 | 한 줄 |
| --- | --- |
| `83be9e4` | contract: after-0926-contract-schema 봉인 (32 조건) — 계약 파일 하나 |
| `0c3e690` | 측정 묶음 다섯 파일 (`m.sh` · `hunks.py` · `plain.py` · `plain-korean.snapshot.md` · `ci-local.sh`) |
| `d86d212` | harness: 계약 형식 문서 v5.7 · 피드백 형식 · sprint-contract SKILL.md Step 4 |
| 이 파일 커밋 | 넘김 기록 |

## 항목별 결과

| ID | 결과 | 자리 (`d86d212` 판) |
| --- | --- | --- |
| CS-1 | 넣음 — 자기진단 절에 `measure_premise_unrun` · `known_answer_missing` 과 「true 는 문제가 있다」 한 줄, 전체 목록은 SKILL.md Step 7 | `harness/references/feedback-schema.yaml` 자기진단 절 |
| CS-2 | 넣음 — 개정 번호(엔트리 포맷) · 측정 관례 새 절 · 서명 측정 한 정의(여러 주체 절). 「봉인 둘째 줄」 칸은 처리됨 — PR #114 `measurement_digest` (계약 형식 문서 §계약 봉인 > 측정 줄 봉인) | `harness/references/contract-schema.md` |
| CS-3 | 넣음 — 새 절 「산출물이 검사인 조건」 (①~④ 표) | 같은 파일 |
| CS-4 | 넣음 — 셸 이식성 절에 `comm` 앞 `LC_ALL=C sort` | 같은 파일 |
| CS-5 | 넣음 — 측정 관례 절 마지막 항목(`git init -q && git add -A` 사본) | 같은 파일 |
| CS-6 | 넣음 — 새 절 「기존 동작 유지 조건」 (목표 문장 나누기 · 무작위 입력 3 개 이상과 시드 · 「조건 문장 안, 측정 밖」) | 같은 파일 |
| CS-7 | 넣음 — `.harness/` 범위 조건 절에 규칙과 도우미 `dirty_except_status` | 같은 파일 |
| CS-8 | 넣음 — 인자 매트릭스 절에 FAIL 칸 규칙 | 같은 파일 |
| CS-9 | 넣음 — Diagnostics 절(규칙) · SKILL.md Step 4 (한 줄, 계약 형식 문서를 가리킴) | 두 파일 |
| CS-10 | 넣음 — 미실측 오라클 봉인 금지 절에 측정 도구 판과 설치 명령 | 계약 형식 문서 |
| CS-11 | 넣음 — 새 절 「페이지 맞추기 계약 — 다섯 가지」 | 계약 형식 문서 |
| CS-12 | 뺌 — hs 묶음 몫 (`# sprint-scope` 블록) | — |

「바깥 근거 대기」 항목은 없다.

## 명시적 미완 — 이번에 안 바꾼 소비면 (`경로:줄`)

계약 AR-04 가 요구하는 넘김이다. 부모가 받을 묶음을 정한다.

- `harness/docs/guides/qa-evaluation-guide.md:1210` — 「①~④ 의 짝은 다음 사이클 Phase 1 · 2 로 넘긴다」. 계약 측 짝이 이번에
  생겨 이 문장이 낡았다. 생성 측 짝(GD-7)과 함께 고친다
- `harness/skills/sprint-contract/SKILL.md:471` — 조건 패턴 표가 v5.5 다섯 종이다. 새 패턴 셋(산출물이 검사인 조건 · 기존 동작
  유지 조건 · 페이지 맞추기 계약)이 없다. Step 2 는 이 묶음 표에 없는 절이다
- `docs/harness/contract-schema.html` — 문서 사이트 페이지. 부모가 마지막에 다시 만든다

판 번호 `v5.5` 를 옮겨 적은 자리 여덟 — 지금도 v5.6 을 못 따라갔고, v5.7 로 올려 갭이 더 벌어졌다 (교차 진단이 찾았다):

- `harness/docs/guides/contract-design-guide.md:1311` — 「버전 정보」 표 `Schema version | v5.5`. 이 표는 `현재:` 줄에서 값을 옮겨
  적으라고 스스로 적어 두었다
- `docs/index.html:239` — 목차 제목 `'Sprint Contract 스키마 v5.5'`. `docs/harness/*.html` 밖이라 페이지 재생성에 안 딸려 온다
- `harness/docs/guides/qa-evaluation-guide.md:12` — 머리 「참조 스키마 … (v5.5)」
- `harness/docs/guides/qa-evaluation-guide.md:15` — 「Phase 2 가 넘긴 스키마 v5.5 의 반대편」
- `harness/docs/guides/qa-evaluation-guide.md:22` — 「정합 — 스키마 v5.5 의 …」
- `harness/docs/guides/qa-evaluation-guide.md:1968` — 참조 목록 「Sprint Contract v5.5 스키마」
- `harness/docs/guides/qa-evaluation-guide.md:2038` — Guide version 줄 안 「스키마 v5.5 정합」
- `harness/docs/guides/qa-evaluation-guide.md:2047` — 「Schema link: contract-schema.md v5.5」

## 원래 있던 편집기 경고

markdownlint-cli2 0.23.2 · MD013 끔 기준, 기준 판과 이번 판이 같다 — 이번에 더한 줄에 걸린 경고는 0 이다(DG-02).

- `harness/references/contract-schema.md` 8 건 (표 모양, 기준 판 `:519` · `:536` · `:537` 자리)
- `harness/skills/sprint-contract/SKILL.md` 9 건 (기준 판 `:104` · `:344` · `:406` · `:412` · `:425` · `:451` · `:628` · `:841` · `:850`)

둘 다 이 묶음 표에 없는 절이고 VS-26 목록에도 없다. 누구 몫인지 부모가 정한다.

## 킷 버전 판단

harness 하나. **minor** 를 권한다 — 계약 형식 문서 판이 v5.7 로 오르고 새 절 · 조건 패턴 셋 · 새 도우미 셋(`with_two` ·
`line_of` · `dirty_except_status`)과 피드백 체크리스트 키 둘이 더해졌다. 지운 규칙 · 바뀐 키는 없어 옛 계약과 피드백은 그대로
읽힌다. `plugin.json` 판 올림 · marketplace · README 는 부모 몫이라 손대지 않았다.

## 문서 사이트 페이지 갱신 필요

`python3 scripts/detect-docs-drift.py` (기본 기준):

```text
harness/references/contract-schema.md → docs/harness/contract-schema.html
harness/references/feedback-schema.yaml → docs/harness/feedback-schema.html  [NEW — 대응 HTML 없음, 신규 생성 + index.html 등록 필요]
```

`contract-schema.html` 은 다시 만들어야 한다. `feedback-schema.html` 은 원래 없는 페이지라 새로 만들지는 부모가 정한다.
`docs/index.html:239` 의 판 번호도 같이 본다. 이 묶음은 페이지를 만들지 않았다.

## 교차 진단 반영 (봉인 전)

qa-evaluator 교차 진단 지적 다섯 가운데 넷을 조건에 넣었다 — SK-01 측정에 `Step 7` · AR-02 제목 수 열여섯 → 열넷 · AR-04 에
판 번호 자리 여덟 · SK-13 에 교훈 다섯과 낱말 여덟의 관계. 넷 다 조건을 좁히는 쪽이다. `m.sh` 가 바뀌어 AR-05 의 `m.sh` 값을
`160e1a01e0b9abc3` 로 새로 쟀다. SC-01 ~ SC-03 의 `[goal]` 은 그대로 두었다 — 도우미 안쪽 구현은 자유이고 이름은 SK-03 `[exact]`
가 잠근다. 새 측정은 흉내 구현 사본에서 양성 · 음성 대조를 다시 돌렸다(`Step 7` 만 지운 변이 FAIL, 넘김 기록 `:12` → `:129` 변이
FAIL).

## 톤 5 단계 대조

규칙은 레포의 `tone-kit/references/` 판(core-comment · core-naming · core-structure · core-antipatterns · locale-korean)을
읽었다. 프로젝트 오버레이 `.claude/tone-project.md` — 어댑터 없음 · 주석 언어 ko. 대상은 `d86d212` 에서 세 파일에 더한 158 줄.

| 패턴 / 규칙 | 건수 | 판정 |
| --- | --- | --- |
| K-02 · K-10 번역투 여섯 (locale-korean §8 G-1) | 0 | 통과 |
| K-04 `합니다` · `습니다` 종결 | 0 | 통과 |
| C-13 자화자찬 (`자동 생성` · `AI 기반`) | 1 | 위반 아님 — `contract-schema.md` Diagnostics 절 「자동 생성 블록 안 · 밖」 은 생성기가 쓰는 블록의 이름이지 머리말 문구가 아니다 |
| C-01 · C-15 코드 블록 주석 | 5 | 통과 — 블록 머리 한 줄과 함수 옆 사용법 한 줄, 이웃 블록(`mine` · `unsigned_on`)과 같은 밀도 (C-08 · S-12) |
| C-04 · F 구분선 · 템플릿 마커 | 0 | 통과 |
| N-07 fallback 접두사 | 0 | 통과 |
| N-08 한 글자 이름 | 1 | 통과 — `dirty_except_status` 의 awk 안 셈 변수 `n` 은 같은 문서의 awk 관례(`n++`)를 따랐다. 셸 변수는 `_repo` · `_rev_a` · `_dir` · `_outside` · `_inside` 처럼 역할 이름 |
| S-03 · S-04 추출 | 3 | 통과 — 새 도우미 셋은 계약 SK-03 · SK-08 이 요구한 공용 정의이고, 여러 계약이 따로 쓰던 것을 모았다 (S-05 세 곳 기준 충족: Phase 7 · 8 · 9) |
| S-06 도우미 체인 | 0 | 통과 — 세 도우미 모두 다른 도우미를 부르지 않는다 |
| K-05 음역 · K-11 새 이름 | 0 | 통과 — 「두 판 풀기」 · 「넘김 목록」 · 「페이지 맞추기 계약」 은 남은 일 목록과 계약이 이미 쓰던 이름이다 |
| 쉬운 말 목록 (계약 SK-14) | 0 | 통과 — `hits=0 words=69` |

## 측정 도구

- 계약 측정 묶음: `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-cs/.harness/.meta/after-0926-contract-schema/`
  (`bash m.sh all` · DG-02 는 `ML=<markdownlint-cli2 0.23.2>` 필요)
- markdownlint-cli2 0.23.2: 세션 스크래치
  `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/cs/mdl/node_modules/.bin/markdownlint-cli2`
  — 빈 폴더에서 `npm install --no-save markdownlint-cli2@0.23.2` 로 다시 만든다
- 로컬 CI: `bash .harness/.meta/after-0926-contract-schema/ci-local.sh <작업 폴더>` (원본은
  `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh`)
- 흉내 구현 · 변이 사본: 세션 스크래치 `cs/mock` (가지 `try-real` 이 실제 편집을 옮긴 판, `m2-*` 가 음성 대조 변이)

## 남은 것

- AR-06 개정 AM-01 — 동의 받음(선택지 응답 2026-09-26T16:22:39.485Z, 커밋 `c29d286`). QA 2 회차 32/32 APPROVE,
  리포트 · 계약 `status: done` 은 `0491d68` 에 커밋. 더 할 일 없음
- 위 「명시적 미완」 열하나 — 소비면 셋과 판 번호 자리 여덟. 이 묶음 범위(세 파일) 밖이라 계약이 막았다
- 원래 있던 편집기 경고 8 · 9 건 — 배정 대기
- 문서 사이트 `docs/harness/contract-schema.html` 재생성 · `feedback-schema.html` 신규 여부 — 부모 몫
- harness `plugin.json` 판 올림(minor 권장) · marketplace · README — 부모 몫
- 독립 검토에서 나온 작은 흠 둘 (판정은 안 바뀜, 배정 대기):
  - `harness/references/contract-schema.md:686` `dirty_except_status` 의 awk 줄이 frontmatter 의 status 줄만이 아니라
    본문의 `status:` 로 시작하는 줄까지 모두 뺀다. 본문에 `status: sneaky` 를 더해도 세지 않는다(2 가 나와야 할 자리에 1)
  - 위 「판 번호 자리 여덟」 은 `.md` 원본만 적었다. 문서 사이트 쪽 여섯 자리가 빠졌다 —
    `docs/harness/contract-design-guide.html:219` · `:253` · `:1537`, `docs/harness/qa-evaluation-guide.html:206` · `:231` · `:1988`.
    원본 `.md` 가 안 바뀌어 `detect-docs-drift.py` 도 못 잡는다. 판 번호를 고칠 때 같이 봐야 한다
    (찾는 명령: `git grep -n "v5\.[4567]\b" -- ':!.harness' ':!harness/references/contract-schema.md'`)
