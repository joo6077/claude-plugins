---
feature: "카이젠 2026-09-24 Phase 16 계약 — 경로 간 조건에 양쪽 값과 판정 불가 · 뷰어를 브라우저로 여는 확인 · Hurl 기재 현행화"
slug: kaizen-0924-p16-api-kit
created: "2026-09-25 12:06"
complexity: "복잡"
conditions: 29
status: active
owner_session: de8c7935-a5b6-4df5-9106-fafa73c288a0
conditions_digest: sha256:3178ee00afdb7c67
locked_at: "2026-09-25 13:24"
---

## 배경

이 Phase 의 외부 근거는 `.harness/.meta/evidence/phase16.md` 하나다. 처리 배정표(`.claude/kaizen-input/insights-report.md`)에서 `배정` 칸이
`Phase 16` 인 행은 `other-kits:P7` 와 `other-kits:P8` 둘이다. 적용 힌트는 「경로 간 조건에 양쪽 값을 적고, 화면 확인 숫자를 보고에 인용한다」 다.
러닝북 `Phase 별 추가 과제` 에 Phase 16 줄은 없고, 앞 Phase notes 가 Phase 16 으로 넘긴 줄도 없다(`grep -n 'Phase 16\|api-kit' .harness/.meta/kaizen-0924/phase*-notes.md` 에 넘김 0 줄).
오케스트레이터 `Phase 별 추가 지시` 의 Phase 16 줄은 「문서 기재와 실측이 어긋나면 실측을 채택하고 `docs/api/research-log.md` 에 기록한다」 와 확정 결정
여섯(`pin` 정의 · `exact` 본문만 · enum 3 샘플 · prod GET/HEAD/OPTIONS · JCS 기준선 · 종료 코드로 계약 실패와 환경 실패 구분)을 완화하지 말라고 적는다.
api-kit 은 2026-09-04 에 만들어져 이번이 첫 카이젠이다.

| 키 · 출처 | 내용 | 이번 처리 |
| --- | --- | --- |
| `other-kits:P7` | api-verify 경로 간 조건에 양쪽 실제 값, 판정 불가를 따로 셈 | 반영 — `/api-verify` §6 · §9 · §11(SK-01), 실패 분류 §5 · §8 과 회귀 정책 문서(SK-02), 「Hurl 로 표현 불가」 기재 정정(SK-03), 새 pin 변이 확인과 검토 에이전트 3 행(SK-04) |
| `other-kits:P8` | api-ui 에 브라우저로 여는 화면 확인 한 단계 | 반영 — `/api-ui` §7 · §8(SK-05), 그 식을 확정 시안에 실제로 돌림(SK-06), 뷰어 스펙 · 뷰어 계약 문서의 누르는 자리 기준 · `data-ep`(SK-07) |
| 근거 파일 §3 현행화 | `HURL_VARIABLE_` · `--secret` 옛 기재 · I-JSON `-0` · 44px 근거 | 반영 — SK-08 · SK-09 · SK-10 · SK-07, 연구 기록 새 절(SK-11) |
| 오케스트레이터 Phase 16 줄 | 「경로 간 불변식은 Hurl assert 로 표현할 수 없다」 | 실측과 어긋난다. 결론(후처리)은 유지하고 이유만 고친다. 오케스트레이터 파일은 이 Phase 범위 밖이라 notes 넘김(ER-03) |

## 리서치 소스

근거 파일 `.harness/.meta/evidence/phase16.md` 에서만 가져왔다. 새로 찾은 자료는 없다. 이 Phase 가 새로 돌린 것은 로컬 도구 실측뿐이다(아래 `회귀 게이트` 절).

- [Hurl Manual](https://hurl.dev/docs/manual.html) — 종료 코드 0~4, 옵션 우선순위, `--variable` · `--secret` 의 환경변수 이름 (SK-02 · SK-08)
- [Hurl Asserting Response](https://hurl.dev/docs/asserting-response.html) — 판정식 값에 템플릿, 같은 요청의 capture 를 검사하는 예 (SK-01 · SK-03)
- [Hurl CHANGELOG](https://github.com/Orange-OpenSource/hurl/blob/master/CHANGELOG.md) — 8.0.0 깨지는 변경 `HURL_foo` → `HURL_VARIABLE_foo` (SK-08)
- [RFC 8785 정정 목록](https://www.rfc-editor.org/errata/rfc8785) — 정정 7920(기술, 2024-05-15 확인): `-0` 을 만나면 파서가 오류를 내야 한다 (SK-10)
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/) — 누르는 자리 2.5.8(AA) 24×24 · 2.5.5(AAA) 44×44 CSS px (SK-05 · SK-07)
- [PIT](https://pitest.org/) — 변이 시험의 뜻: 결함을 일부러 넣어 검사가 잡는지 본다 (SK-04)
- 근거 파일 로컬 실측 L1 ~ L7 — 경로 간 조건의 종료 코드, `HURL_VARIABLE_`, `--curl` · `--error-format long` 마스킹, 브라우저 조종 도구의 `file://` 차단
- 내부: `docs/api/research-log.md` 2026-09-05 절 — `--secret` 채널별 실측 (SK-09 가 스킬 Gotcha 를 이 실측과 근거 파일 L5 의 `--curl` 실측에 맞춘다)

## GAP 분석 · 개선안 초안

복잡도 4 축 (sprint-contract Step 1). 두 축 이상이 예이고 계약 변경과 소비면이 둘 다 예라 **복잡** 이다 — Step 2.5 양면 조건을 넣었다.

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 셋 — 스킬 본문(SKILL.md 넷 · README) · 스킬 참조 문서와 에이전트(references 넷 · api-reviewer) · 리서치 문서(`docs/api/` 일곱) |
| 공개 API·계약 변경 | 밖에서 읽는 형식이 바뀌는가 | 예 — `/api-verify` 리포트 집계에 `판정 불가` 칸, JUnit 매핑에 한 행, `/api-ui` 보고에 브라우저 숫자, 뷰어 마크업에 `data-ep` 규약 |
| 소비면 존재 | 반대편이 있는가 | 예 — 판정 불가를 낳는 쪽(`/api-contract` 가 만든 pin)과 그것을 보는 검토 에이전트(api-reviewer 3 행, SK-04) · 리포트 형식을 설명하는 실패 분류 문서(SK-02) · 뷰어를 만드는 스펙(`data-ep`, SK-07). 범위 밖 반대편은 설계문서 `docs/superpowers/specs/2026-09-02-api-kit-design.md:249` · 오케스트레이터 `:567` · 문서 사이트 페이지 여섯(ER-03 넘김) |
| 회귀 위험 | 기존 동작이 깨질 경로 | 중간 — 확정 결정 줄은 글자 그대로 둔다(AR-03). 누르는 자리 기준을 44 에서 24 로 낮추지만 44 는 확정 시안부터 39 개가 못 맞춘 값이었다(SK-06) |

설정 리터럴 대조표 (Step 1.2, `.harness/project.yaml` 원문):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A 사유에 그대로 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A 사유에 그대로 |
| `diagnostics.ide_exclude` | `[]` | DG-02 에 그대로 |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 그대로 |
| `anti_patterns[].id` / `message` | AP-01 · AP-02 · AP-03 · AP-04 | AP-01 · AP-03 · AP-04 — 메시지 원문 그대로. AP-02(force push)는 이 Phase 가 푸시하지 않아 뺐다 |

편집 전 감사 (Step 1.4, 대상 파일을 실제로 읽은 줄 — 줄 번호는 시작 커밋 판):

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 여부 |
| --------- | ---------------------------- | ------------------- | ---------------- |
| `api-kit/skills/api-verify/SKILL.md` | `:20` `--secret` Gotcha · `:117` I-JSON 게이트 · `:133` 「`.hurl` 로 표현되지 않은 경로 간 불변식」 · `:167` 실행 요약 · `:201` · `:203` 판정 요약 | 경로 간 불변식 판정에 값 · 판정 불가가 없다. 「표현되지 않은」 이 실측과 다르다. `--secret` 이 「stderr 로그와 리포트만」, `--very-verbose` 가 「그대로 뿌린다」 — 2026-09-05 실측과 다르다. I-JSON 목록에 `-0` 없음 | SK-01 · SK-09 · SK-10 |
| `api-kit/skills/api-verify/references/failure-taxonomy.md` | `:107` 「Hurl 로 표현 불가」 · `:151`~`:158` JUnit 표 | 판정 불가가 어디에도 없다 | SK-02 |
| `api-kit/skills/api-contract/SKILL.md` | `:20` I-JSON Gotcha · `:24` 「경로 하나에 predicate 하나이므로」 · `:64`~`:70` 게이트 목록 · `:263`~`:272` §11 보고 · `:225` `jsonpath "$.data[0].id" isString` | 표현 불가 기재 · `-0` 없음 · 새 pin 이 실패를 잡는지 확인하는 단계가 없다. `:225` 는 같은 파일 `:20` 의 index assertion 금지와 어긋난다 | SK-03 · SK-04 · SK-10. `:225` 는 미반영(ER-03) |
| `api-kit/skills/api-contract/references/strictness-modes.md` | `:81`~`:88` Hurl 표현 가능 여부 표 · 문장 | 「**불가**」 · 「경로 하나에 predicate 하나다」 | SK-03 |
| `api-kit/skills/api-ui/SKILL.md` | `:20` `--secret` Gotcha · `:132`~`:162` §7 자기 검증 · `:158` 「클릭 타깃 44px — 확정 시안 실측」 · `:164`~`:180` §8 | 브라우저로 여는 확인이 없다(글자 검사뿐). 44px 근거가 실측과 다르다(확정 시안 39 개가 44 미만) | SK-05 · SK-06 · SK-09 |
| `api-kit/skills/api-ui/references/viewer-spec.md` | `:19` 「클릭 타깃 ≥ 44px — 확정 시안 실측 기준」 · `:84` 엔드포인트 행 | 항목 수를 셀 표식(`data-ep`)이 스펙에 없고 시안에만 있다. 그룹 초기 펼침도 시안에만 있다 | SK-07 |
| `api-kit/skills/api-probe/SKILL.md` | `:15` `--secret` Gotcha · `:183` I-JSON 검문 | `--secret` 옛 기재 · `-0` 없음 | SK-09 · SK-10 |
| `api-kit/skills/api-probe/references/hurl-execution.md` | `:5` Hurl 8.0.1 · `:241`~`:258` §6 시크릿 표(2026-09-05 실측 반영됨) · `:312` 「`HURL_*` 는 변수에 안 붙는다」 | `:312` 가 8.0.0 변경(`HURL_VARIABLE_`)과 다르다. §6 표에 `--curl` 파일(근거 파일 L5 — 가려진다)이 없다 | SK-08 · SK-09 |
| `api-kit/README.md` · `api-kit/agents/api-reviewer.md` | README `:68` `--secret` · AUTO 표지 `:22` · `:30` · reviewer `:87` 3 행 | README 옛 기재. reviewer 3 행은 경로 간 불변식의 판정식 쪽 경로를 안 본다 | SK-09 · SK-04 |
| `docs/api/research-log.md` | `:1`~`:149`, 특히 `:86`~`:88` 「변수는 … 로만 들어온다」 | 2026-09-05 절이 `HURL_who` 만 쟀다 | SK-11 · SK-08 |
| `docs/api/execution/auth-secret-lifecycle.md` · `probe-synthesis-hurl-semantics.md` | `:131` · `:49` · `:51` · `:82` · auth-secret-lifecycle `:60` · `:99` · `:125` | `HURL_*` 옛 기재. auth-secret-lifecycle 세 자리가 `--secret` 이 가리는 곳을 「둘뿐」 으로 적는다(`--curl` 파일 빠짐 — 2 회차 검토 D1) | SK-08 · SK-09 |
| `docs/api/contract/snapshot-sealing-canonicalization.md` · `contract-extraction-modes.md` | `:35` · `:38` 게이트 문장과 출처 · `:131`~`:136` Gotchas | `-0` 없음 · 새 pin 변이 확인의 문서 근거가 없다 | SK-10 · SK-04 |
| `docs/api/verification/static-evidence-viewer-contract.md` · `regression-diff-failure-policy.md` | `:85` 44px · `:106`~`:111` Gotchas · `:110`~`:115` Gotchas | 44px 근거 · 브라우저 확인 함정 · 판정 불가의 문서 근거가 없다 | SK-07 · SK-02 |
| `docs/superpowers/specs/2026-09-02-api-kit-design.md` · `.claude/skills/kaizen-orchestrator/SKILL.md` | `:249` · `:567` | 같은 「표현할 수 없다」 기재 | 범위 밖 — ER-03 넘김 |
| `scripts/detect-docs-drift.py` · `docs/api-kit/*.html` | `:33`~`:62` `SOURCE_TO_HTML` 에 `docs/api/` 없음 · `docs/index.html:551`~`:562` 페이지 열둘 | 이 Phase 가 바꾸는 문서 여섯의 페이지가 드리프트 목록에 안 나온다 | 범위 밖 — ER-03 넘김 |
| 확정 시안 `/Users/jackson/Hub/10_Dev/claude-plugins/.mockups/api-ui-v7.html` | `:1534` `const EP` · `:1736` `openGroups` · `data-ep="${id}"` · `<link rel="icon">` 0 줄 | 킷이 정본이라 부르는데 `.gitignore` 에 있어 워크트리에 없다 | 읽기만 — SK-06 · AR-02 가 본 레포 경로로 읽는다 |

Phase 1 결과 대조 (오케스트레이터 Step 16 전수 감사 — `skill-design-guide.md` 1.6.0):

| Phase 1 변경 | api-kit 에서 본 자리 | 처리 |
| --- | --- | --- |
| §3.7 조항 3 — 검증 불가 시 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령) | 새로 넣는 브라우저 확인이 도구 없이 끝날 수 있다 | SK-05 — 네 칸을 적게 한다 |
| 0 이 기대값인 검증의 양성 대조 | `/api-ui` §7 은 이미 positive control 을 요구한다(`:138`~`:139`) | 새 식에도 대조 사본 넷과 CSP `<meta>` 를 넣은 사본을 붙였다(SK-06) |
| 알려진 답 대조 | 새로 짜는 측정(브라우저 식 · hurl 재실측) | SK-02 · SK-06 · SK-08 에 손으로 센 기대값 |
| agent 가이드 §10 — `[미검증:ENV]` · `[미검증:INVALID]` | api-reviewer 의 미검증 프로토콜이 정본 요약 복제다 | 처리 배정표 밖 — 미반영(ER-03, 다음 사이클) |

api-kaizen Step 1 사전 측정 — `.claude/skills/api-kaizen/SKILL.md` Step 1 명령을 시작 커밋 판에서 그대로 돌린 출력이다.
Step 5 사후 측정은 BUILD 가 `$END` 판에서 같은 명령을 다시 돌려 notes `## 사전 · 사후 측정` 절에 표로 적는다(ER-03 이 절 머리를 잰다).
예행 판 값은 api-verify 만 `gotchas=12` 이고 나머지는 같다 — 새 Gotcha 가 아니라 §6 에 더한 굵은 불릿 둘을 이 명령이 함께 센다.

```text
api-init       gotchas=10 steps=9
api-probe      gotchas=12 steps=9
api-contract   gotchas=10 steps=12
api-verify     gotchas=10 steps=12
api-ui         gotchas=20 steps=9
```

개선안 초안 — 정확한 문장은 조건 줄과 `m.sh` 토큰이 기준이다. 예행 도구 `mock.py`(스크래치 `p16d/`, sha256 앞 16 자리 `99aca4f2cab1bc42`)가 시작 커밋 판에 그대로 적용해 본 판이다.

1. **경로 간 조건** (`other-kits:P7`) — `/api-verify` §6 에 판정 줄 형식(`$.meta.total=47 · len($.data)=10 → PASS`)과 `판정 불가`(한쪽 경로 없음, PASS 도 FAIL 도 아니고 따로 셈, 그 자체로 게이트 미파괴 — 사라진 `required` 경로는 schema drift 가 잡는다). §9 실행 요약 · 7 번 항목, §11 판정 요약 · 게이트 안 깬 항목. 실패 분류 §5 행 · §8 JUnit 행(`skipped` + 사유). 회귀 정책 문서 Gotcha. 「Hurl 로 표현 불가」 넷을 「적을 수는 있지만 경로가 없으면 종료 코드 3 → 판정 불가를 가를 곳이 후처리뿐」 으로
2. **새 pin 변이 확인** (`other-kits:P7` 근거 파일 §4 4 번) — `/api-contract` §11 보고 4 번, 추출 모드 문서 Gotcha. api-reviewer 3 행에 판정식 쪽 경로
3. **브라우저 확인** (`other-kits:P8`) — `/api-ui` §7 에 여는 방법(`ui.html` 한 장만 든 빈 폴더를 띄운다 — `.api/` 를 통째로 띄우면 아이디 · 비밀번호 파일과 가리지 않은 원본 응답이 HTTP 로 열린다) · 콘솔 error · 페이지 안 식(`ep` · `shown` · `targets` · `under24` · `under44`) · 도구 없을 때 네 칸, 기대값 표 두 행, §8 보고 한 줄. 뷰어 스펙에 `data-ep` · 그룹 펼침, 누르는 자리 기준 24(44 권장)
4. **현행화** — `HURL_VARIABLE_` 넷, `--secret` 넷(2026-09-05 실측과 근거 파일 L5 `--curl` 에 맞춤)과 hurl-execution §6 표 `--curl` 행 · auth-secret-lifecycle 세 자리(§6 문장 · 수치 표 · Gotcha 머리), I-JSON `-0` 다섯과 문서 근거, 연구 기록 2026-09-24 절과 2026-09-05 절 정정 표시

하지 않기로 한 것:

- `판정 불가` 를 게이트에 넣지 않는다. 사라진 경로가 `required` 면 schema drift 가 이미 계약 실패로 잡고, `optional` 이면 계약상 없어도 되는 값이라 불변식을 판정할 수 없는 게 맞다. I-JSON 게이트 실패를 「비교 불가」 로 따로 두는 기존 규칙과 같은 모양이다. 근거 파일 §5 열린 질문 1 — notes 다음 사이클 메모에 사용자 확인 권장으로 적는다
- 경로 간 불변식을 `.hurl` 로 옮기지 않는다 — 확정 결정 유지. 경로가 없을 때 종료 코드 3 이 킷 분류로 환경 실패라 계약 판정이 보류된다(근거 파일 L1)
- OpenAPI 3.2 · Hurl 8 jsonpath 1 개 결과 벗기기 · 대비 · 테마 · Pact 브랜치 축 · Hurl 8.1.0 — ER-03 미반영 절과 연구 기록 이월 절

## 범위 경계

- 이 Phase 시작 HEAD: `3a348d601cedd49e0689ca194b57baf8f5029454`. 범위 상한은 개정 파일 `.harness/sprint-amendments-kaizen-0924-p16-api-kit.md` 의
  `end_sha:` 마지막 값이다. 여러 Phase 가 같은 가지 `kaizen/2026-09-24` 에 동시에 커밋하므로 `HEAD` 로 재지 않는다(DRAFT 도중에 Phase 13 커밋 셋이 이미 올라왔다)
- 고치는 파일은 열일곱이고 새 파일은 없다 — 아래 블록이 그 목록이다(`harness/README.md` §커밋 안전 훅 이 정한 범위 선언 자리).
  `.harness/` 쪽은 이 계약 · 개정 파일 · QA 피드백 · `.harness/.meta/kaizen-0924/phase16-notes.md` · `.harness/.meta/kaizen-0924/phase16-review.md` 를 쓴다 —
  슬러그를 나열하지 않고 AR-01 셋째 값 `verify_seal` 로 잰다. AR-01 다섯째 값이 이 블록과 측정 공통 정의의 `FILES` 가 같은지 잰다

```text
# sprint-scope
api-kit/skills/api-verify/SKILL.md
api-kit/skills/api-verify/references/failure-taxonomy.md
api-kit/skills/api-contract/SKILL.md
api-kit/skills/api-contract/references/strictness-modes.md
api-kit/skills/api-ui/SKILL.md
api-kit/skills/api-ui/references/viewer-spec.md
api-kit/skills/api-probe/SKILL.md
api-kit/skills/api-probe/references/hurl-execution.md
api-kit/README.md
api-kit/agents/api-reviewer.md
docs/api/research-log.md
docs/api/execution/auth-secret-lifecycle.md
docs/api/execution/probe-synthesis-hurl-semantics.md
docs/api/contract/snapshot-sealing-canonicalization.md
docs/api/contract/contract-extraction-modes.md
docs/api/verification/static-evidence-viewer-contract.md
docs/api/verification/regression-diff-failure-policy.md
.harness/
```

- **이 Phase 의 커밋 메시지에는 전부 `Co-Authored-By` 줄 바로 위에 서명 줄 `Kaizen-Phase: kaizen-0924-p16-api-kit` 한 줄을 넣는다** (봉인 커밋 포함).
  AR-01 · ER-03 · SC-00 · DG-01 · DG-03 · DG-06 이 이 줄로 이 Phase 커밋을 가린다(`harness/references/contract-schema.md` §여러 주체가 한 가지에 커밋할 때 선택지 B).
  서명을 빠뜨린 커밋은 서명 줄 목록에 안 보이므로 AR-01 첫째 값과 ER-03 마지막 값은 경로로 직접 센다.
  FIX 가 커밋을 더할 때도 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다(옛 줄은 지우지 않는다). notes 커밋도 이 Phase 커밋이다 — notes 를 커밋한 뒤 그 sha 로
  `end_sha:` 줄을 하나 더 덧붙여 커밋한다
- 구현 커밋은 `git add -- <열일곱> && git commit -o -- <열일곱>` 한 번이다. 열일곱이 `api-kit/` 과 `docs/api/` 뿐이라 `validate-post-kaizen.py` scope-isolation 에
  걸리지 않는다(예행에서 한 커밋으로 확인, DG-06). 예행 도구 `mock.py` 가 적용한 판이 조건의 기준이다 — BUILD 는 같은 편집을 쓰거나 `mock.py` 를 작업 폴더에 돌린다
- 측정이 기대는 제목 · 줄 머리는 이름을 바꾸지 않는다: `## Gotchas` · `## 5. 응답 정규화` · `## 6. drift 분류` · `## 9. 리포트 생성` · `## 11. 보고와 다음 단계` (api-verify) ·
  `## 4. schema drift 판정` · `## 5. value drift 판정` · `## 8. CI artifact 매핑` (실패 분류) · `## Gotchas` · `## 2. I-JSON 게이트` · `## 11. 보고` (api-contract) · `### Hurl 표현 가능 여부` (strictness-modes) ·
  `## Gotchas` · `## 7. 자기 검증 (건너뛰기 금지)` · `## 8. 열기와 보고` (api-ui) · `## 1. 하드 제약` · `### 3.2 사이드바 — 엔드포인트 트리` (viewer-spec) · `## Gotchas` · `## 7. 스크러빙 → 정규화 → 저장` (api-probe) ·
  `| 3 | Pin Assertion Fitness |` (api-reviewer) · `## Gotchas` (문서 넷) · `### 3. 정규화 전 I-JSON 게이트` · `## 수치 기준` · `## [2026-09-05] — Hurl 8.0.1 실측 대조` · `## [2026-09-24] — 첫 카이젠 (Phase 16)` ·
  AR-03 이 그대로인지 보는 확정 결정 줄 여덟(`m.sh` `AR-03)` 갈래)
- 공유 파일(`.claude-plugin/marketplace.json` · `api-kit/.claude-plugin/plugin.json` 버전 · 루트 `README.md` · 루트 `CLAUDE.md` · `docs/` HTML · 처리 배정표 · 감사 로그 ·
  실패 횟수 파일 · `.github/workflows/ci.yml` · `.harness/stale-values.yaml`)과 다른 Phase · 레포 전용 파일(`harness/` · `scripts/` · `.claude/skills/` · `docs/superpowers/`)은
  건드리지 않는다 — ER-03 마지막 값. 러닝북 Phase 표가 이 Phase 에 `api-kit/` · `docs/api/` 만 줬다. api-kit README 는 킷 전용 문서라 고친다 — AUTO 구간 밖 한 줄이고
  AUTO 가 읽는 스킬 · 에이전트 frontmatter 는 그대로다(AP-04). 문서 사이트 재생성은 Final F2 몫이라 DG-06 에서 `docs-site-regen` 을 뺀다
- QA(`harness:qa-evaluator`)는 설치본이다 — 이 Phase 가 고치는 파일에 qa-evaluator 는 없다
- 사용자 승인(Step 5) 대체: 사용자가 「자동으로 끝까지 알아서 진행해 내 허락이 필요한건 코덱스로 리서치나 검토받고」라고 위임했다(세션
  `de8c7935-a5b6-4df5-9106-fafa73c288a0` 기록 queued_command `2026-09-24T04:04:16.964Z`). Codex 사용량 한도가 소진돼(오류 원문 「You've hit your usage limit … try
  again at 11:05 PM」, 2026-09-24) 독립 Claude 검토자(REVIEW 에이전트)가 대신한다. 이어 사용자가 「코덱스 대신에 그냥 너가 알아서 진행하라고」라고 명시했다(같은 세션
  기록 user `2026-09-24T11:54:58.940Z`). 검토 결과 파일: `.harness/.meta/kaizen-0924/phase16-review.md` — 1 회차 판정 `VERDICT: CHANGES`. 꼭 고칠 것 넷(C1 ~ C4)과
  고치면 좋은 것 일곱 가운데 2 ~ 6 을 반영했고 1 은 SK-06 CSP 사본 줄과 notes 메모 둘만 넣었다(뷰어 계약 문서 Gotcha 끝 문장 · 연구 기록 표 행은 넣지 않았다).
  7(서명 없는 남의 커밋)은 QA 때 개정 파일로 가를 일이라 계약 글을 바꾸지 않았다. 같은 파일 `## 2 회차` 판정도 `VERDICT: CHANGES` 다 — 꼭 고칠 것 D1(auth-secret-lifecycle
  세 자리가 아직 「둘뿐」)을 BUILD 가 봉인 전에 반영했다: `mock.py` 에 편집 셋, SK-09 조건 줄 (e) · (f) 와 측정 값, `m.sh` SK-09 갈래(토큰 셋 · 옛 글 셋 · `curl_missing`), 대조 둘.
  2 회차 고치면 좋은 것 가운데 1(여는 방법 뒤 「확인이 끝나면 서버를 내리고 그 폴더를 지운다」)과 2(연구 기록 새 절의 `--curl` 문장 끝에 반영 자리)는 넣었다 —
  둘 다 조건 토큰이 든 줄 안에 문장을 더한 것이라 재는 값이 바뀌지 않는다. 3(`evid_same` 이 떨어지면 `git log 3a348d6..<end_sha> -- .harness/.meta/evidence/phase16.md` 로
  누가 고쳤는지부터 본다)은 QA 참고로 여기 적는다. 4(디스크)는 BUILD 가 봉인 전에 남은 자리를 봤다. D1 반영 뒤 예행 저장소를 새로 만들어 아래 표를 다시 쟀다
- 판정 한계: 스킬을 따르는 LLM 이 판정 줄 형식 · 브라우저 확인을 실제로 하는지는 결정론 측정이 없다 — 조건은 지시 문장이 정해진 절에 글자 그대로 있는지(SK-01 ~ SK-05 · SK-07 ~ SK-11)와
  스킬이 시키는 식이 확정 시안에서 실제로 맞는 값을 내는지(SK-06)를 잰다. 킷의 후처리는 스크립트가 아니라 스킬 본문 지시라 돌릴 것이 없다 — 대신 문서가 적은 Hurl 동작을 로컬 hurl 로 다시 잰다(SK-02 · SK-08 · SK-09).
  확정 시안은 `.gitignore` 에 있어 본 레포 경로에서 읽는다 — sha256 앞 16 자리가 다르면 `MOCKUP_CHANGED` 로 멈춘다.
  SK-02 · SK-08 · SK-09 의 hurl 기대값은 hurl 8.0.1 동작에 묶여 있다 — 판이 다르면 `HURL_VERSION_CHANGED` 로 멈춘다(판이 바뀐 것을 구현 결함으로 읽지 않게)
- 판정 근거: SK-01 ~ SK-05 · SK-07 ~ SK-11 — 산출물이 문서 문장 자체라 정해진 절 · 줄에 정해진 문장이 있는지가 판정이다. `sect` 가 코드 펜스를 건너뛰고 절을 자르고,
  `runp` 가 표 행이 붙어 있는지 본다. 시작 커밋 판에서 새 문장 0 을 봉인 전에 확인했고, 문장 하나만 지운 사본에서 그 값이 떨어졌다(`회귀 게이트` 절)
- 판정 근거: SK-02 · SK-06 · SK-08 · SK-09 의 hurl · 브라우저 줄과 SK-10 의 `js_minus_zero` — 로컬 hurl · 헤드리스 크로미엄 · node 를 실제로 돌린 출력이다. 대조 사본 · 시크릿 안 건 판 · 같은 값을 변수로 건 판이 측정 안에 있다
- 판정 근거: ER-01 · ER-02 · AP-01 · AP-03 — 편집 전 판과 파일마다 비교한 더한 줄 계산이다. 각각 양성 대조가 붙어 있다. ER-01 은 근거 파일을 시작 커밋 판에서 읽는다 — `.harness/` 안이라 이 Phase 가 고칠 수 있다
- 판정 근거: DG-02 — 열일곱 파일마다 규칙별 경고 수를 편집 전 판과 비교한 출력이다. 더한 줄만 보지 않는다 — MD022 · MD032 · MD024 는 더한 줄 옆의 손대지 않은 줄에 붙는다(러닝북 측정 구멍 목록)
- 판정 근거: ER-03 · AR-01 · SC-00 · DG-01 · DG-03 · DG-06 — 커밋 기록과 봉인 검증 함수를 실제로 돌린 출력이다. 예행 저장소 변형이 양성 대조다
- 판정 근거: AR-02 · AR-03 · AP-04 · DG-05 — 가리키는 자리 · 편집 전과 같아야 하는 곳 · 저장소 검사 도구를 실제로 돌린 출력이다. DG-05 의 옛 값은 등록부 값을 열일곱 파일에서 직접 센 수다 —
  `scripts/check-stale-values.py` 는 `SOURCE_DIRS` 에 `api-kit/` 이 없어 스킬 · 참조 문서를 훑지 않는다. api-kit README 의 AUTO 표지는 `sync-docs.py` 가 읽는 모양(`<!-- AUTO:skills -->`)이라 그 검사는 쓴다 — 대조는 봉인 전 실측 표 DG-05 칸
- 커버리지 해소: SK-01 ~ SK-11 · AR-02 · AR-03 · AP-04 — 산문의 파일 이름은 측정 `m <조건 ID>` 가 공통 정의의 변수(`$V` · `$FT` · `$C` · `$SM` · `$U` · `$VS` · `$P` · `$HE` · `$RD` · `$RV` · `$RL` · `$AS` · `$PS` · `$SS` · `$CM` · `$SV` · `$RG` · `$MOCKUP` · `$EVID`)로
  연다(파일과 변수의 대응은 `common.sh` 머리). 토큰은 `m.sh` 의 같은 ID 갈래에 글자 그대로 있다. `mock.py` · `rehearse.sh` · `common.sh` · `m.sh` · `rule-delta.sh` · `srv.py` · `probe.js` 는 측정 도구 자체의 이름이다
- 커버리지 해소: ER-01 · ER-03 — `.harness/.meta/kaizen-0924/phase16-notes.md` · `.harness/.meta/evidence/phase16.md` 는 공통 정의의 `$NOTES` · `$EVID` 다. ER-01 의 `.harness/` 는 근거 파일이 이 Phase 가 고칠 수 있는 자리라는 설명이다 — 셋째 값 `evid_same` 이 그 파일을 시작 커밋 판과 비교한다. ER-03 의 넘김 경로는 `m.sh` `ER-03)` 갈래 `toks` 의 인자이고, 공유 경로는 `not_other` 의 인자다
- 커버리지 해소: AR-01 — `api-kit` · `docs/api` 는 `unsigned_on` 의 인자, `.harness/` 는 `scope` 블록 줄과 `verify_seal` 이 도는 폴더다. `harness/references/contract-schema.md` 는 셋째 값 권장 형태의 출처다
- 커버리지 해소: SK-01 ~ SK-11 · ER-03 의 파일 아닌 토큰 — `.hurl` · `127.0.0.1` · `meta.total` · `favicon.ico` · `console.error` · `file://` · `.api/` · `ui.html` · `credentials.local.json` · `reports/` · `snapshots/prod/` · `fetch("./data.json")` · `report.json` · `store/*_response.json` · `contracts/*.yaml` · `/api-verify` · `/api-contract` · `SKILL.md` · `8.1.0` · `docs/api` 는 파일 경로가 아니라 문장 토큰이나 측정 출력의 일부다 — `m.sh` 같은 ID 갈래의 `toks` 인자 · hurl · 브라우저 출력에서 잰다. `api-kit/` · `docs/api/` 는 `oldn` · `unsigned_on` · AR-03 `find` 의 인자이고, `docs/api/research-log.md` 는 `oldn` 이 이름(`research-log.md`)으로 빼는 파일이다. `m.sh` 는 측정 도구 자체다
- 검출기는 공백 든 코드 조각 안의 인자를 읽지 못한다 — 위 해소 줄이 전부 그 경우다
- 편집 전부터 있던 경고(예: api-probe SKILL.md 의 MD038 두 개)는 같은 수로 남으면 된다. DG-02 는 파일마다 규칙별 경고 수를 편집 전 판과 비교한다
- notes 에 함께 적는다(조건으로는 재지 않는다): `GAP 분석` 절의 Phase 1 대조 표, 하지 않기로 한 셋과 이유, `## 사전 · 사후 측정` 절의 표 값(절 머리는 ER-03 이 잰다),
  `## 다음 사이클 메모` 에 「확정 시안이 `.gitignore` 에 있어 워크트리 · CI 에 없다」 · 「`판정 불가` 를 게이트에 넣지 않기로 한 결정은 사용자 확인 권장」 ·
  「확정 시안에 뷰어 스펙 §1 의 CSP `<meta>` 가 없다」 · 「§7 글자 검사가 CSP `<meta>` 가 있는지를 재지 않는다」 · 「1×1 px 로 숨긴 입력칸이 생기면 `under24` 가 1 이 된다」 다섯 줄
- 기능 조건 19 · 전체 조건 줄 29
- 사용자가 할 일: 없음

## 회귀 게이트 — 측정 공통 정의와 봉인 전 실측

모든 조건의 측정은 아래 `common.sh` 와 `m.sh` 를 차례로 `.` 으로 읽은 **bash** 셸에서 돈다 — `common.sh` 는 bash 가 아니면 `NOT_BASH` 를 찍고 종료 코드 2 로 끝난다
(zsh 는 따옴표 없는 변수를 쪼개지 않고 배열 첨자가 1 부터다). `m` 은 도우미 함수와 두 판 폴더가 없으면 `HELPER_MISSING` · `SNAPSHOT_MISSING` 을 내고 멈춘다 —
그래서 조건마다 `type m` 하나로 정의 확인을 대신한다. 두 판 풀기가 끊기거나 열일곱 파일 가운데 하나라도 어느 판에서 비면 `common.sh` 가
`SNAPSHOT_FAIL` 을 내고 종료 코드 2 로 끝난다. 셸이 끝나면 두 판 폴더를 지운다. `END_UNRESOLVED` 가 찍히면 셸이 종료 코드 2 로 끝난다.
`m` 의 종료 코드는 판정하지 않는다 — 판정은 출력 값으로 한다. 갈래 마지막 명령이 `grep -c` 이고 그 값이 0 이면 종료 코드가 1 이라, 0 을 기대하는 조건은 PASS 값에서 1 을 낸다.
`m` 이 스스로 멈출 때(`HELPER_MISSING` · `SNAPSHOT_MISSING` · `UNKNOWN` · `TOOL_MISSING` · `HURL_VERSION_CHANGED` · `SRV_FAIL` · `MOCKUP_MISSING` · `MOCKUP_CHANGED` · `EXPR_MISSING` · `NEG_EDIT_FAIL` · DG-05 사본 저장소를 못 만들 때)만 2 다.
hurl · 브라우저 대조(SK-02 · SK-06 · SK-08 · SK-09)는 `srv.py` 가 `127.0.0.1` 빈 포트에 띄운 서버에만 요청한다 — 외부 요청은 없다. 서버는 그 갈래 끝에서 내린다.
블록 다섯을 각 블록 첫 주석 줄(셔뱅 다음)의 이름 그대로 한 폴더에 저장하고 그 폴더를 `K` 에 넣는다. `rule-delta.sh` 옆에는 `node_modules` 를
`/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p1build/node_modules` 로 잇고
`cfg.markdownlint-cli2.jsonc` = `{ "config": { "MD013": false } }` 를 둔다 — 준비 단계 실측(2026-09-25): 그 자리의 `.bin/markdownlint-cli2 --version` 첫 줄이
`markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)`. 없으면 그 폴더에서 `npm install --no-save markdownlint-cli2@0.23.2` 부터 돌린다.
그 밖의 준비 단계 실측(2026-09-25): `command -v hurl` → `/opt/homebrew/bin/hurl` (`hurl 8.0.1 (x86_64-apple-darwin25.0) libcurl/8.7.1`) · `command -v node` 있음 ·
`/Users/jackson/Hub/10_Dev/claude-plugins/node_modules/playwright` 1.58.2 · 브라우저 `~/Library/Caches/ms-playwright/chromium-1208` ~ `chromium-1234` 와 `chromium_headless_shell-*` ·
확정 시안 sha256 앞 16 자리 `c4bd563ec8b71a95` · `python3` · `shasum` 있음.
`common.sh` 의 `R` 은 예행 저장소를 가리킬 때만 쓴다 — 비우면 작업 폴더다. 두 판을 `${TMPDIR:-/tmp}/p16m.XXXXXX` 에 푸니 `TMPDIR` 를 스크래치 폴더로 두고 읽는다.
예행 도구(스크래치 `p16d/`): `mock.py`(시작 커밋 판에 이 계약이 요구하는 편집을 적용한다. 연구 기록 새 절은 옆 `rl-append.md`) ·
`rehearse.sh`(시작 커밋에서 예행 저장소를 만들어 봉인 · 다른 Phase 커밋 · 구현 한 커밋 · `end_sha` · notes · `end_sha` 를 흉내 낸다. 변형 `base` · `unsigned-mine` · `unsigned-shared` ·
`signed-outside` · `cross-phase`) · `runall.sh` · `del.sh`(문장 삭제 대조) · `ctl.sh`(양성 · 음성 대조) · `notes-mock.md`(notes 모의본).

```bash
# common.sh — 측정 공통 정의. bash 로 읽는다 (zsh 는 배열 첨자가 1 부터이고 따옴표 없는 변수를 쪼개지 않는다)
[ -n "${BASH_VERSION:-}" ] || { echo "NOT_BASH — bash -c 안에서 다시 읽는다"; exit 2; }
export LC_ALL=C.UTF-8   # 번역투 정규식이 글자 단위로 돌아야 한다
cd "${R:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/kaizen-0924}" || exit 2
B=3a348d601cedd49e0689ca194b57baf8f5029454                  # 이 Phase 시작 HEAD
SIG='Kaizen-Phase: kaizen-0924-p16-api-kit'
CF=.harness/sprint-contract-kaizen-0924-p16-api-kit.md
AM=.harness/sprint-amendments-kaizen-0924-p16-api-kit.md
NOTES=.harness/.meta/kaizen-0924/phase16-notes.md
EVID=.harness/.meta/evidence/phase16.md
MOCKUP=/Users/jackson/Hub/10_Dev/claude-plugins/.mockups/api-ui-v7.html   # 킷이 정본으로 부르는 확정 시안 (레포 밖 · gitignore)
MOCKUP_SHA16=c4bd563ec8b71a95
PW=/Users/jackson/Hub/10_Dev/claude-plugins/node_modules/playwright
END=$( [ -f "$AM" ] && sed -n 's/^end_sha:[[:space:]]*//p' "$AM" | tail -1 )
if [ -z "$END" ] || ! git rev-parse -q --verify "$END^{commit}" >/dev/null; then
  echo "END_UNRESOLVED — 측정을 멈춘다. HEAD 로 바꿔 재지 않는다"; exit 2
fi
: "${K:?도우미 폴더를 K 에 넣는다}"
V=api-kit/skills/api-verify/SKILL.md
FT=api-kit/skills/api-verify/references/failure-taxonomy.md
C=api-kit/skills/api-contract/SKILL.md
SM=api-kit/skills/api-contract/references/strictness-modes.md
U=api-kit/skills/api-ui/SKILL.md
VS=api-kit/skills/api-ui/references/viewer-spec.md
P=api-kit/skills/api-probe/SKILL.md
HE=api-kit/skills/api-probe/references/hurl-execution.md
RD=api-kit/README.md
RV=api-kit/agents/api-reviewer.md
RL=docs/api/research-log.md
AS=docs/api/execution/auth-secret-lifecycle.md
PS=docs/api/execution/probe-synthesis-hurl-semantics.md
SS=docs/api/contract/snapshot-sealing-canonicalization.md
CM=docs/api/contract/contract-extraction-modes.md
SV=docs/api/verification/static-evidence-viewer-contract.md
RG=docs/api/verification/regression-diff-failure-policy.md
FILES=("$V" "$FT" "$C" "$SM" "$U" "$VS" "$P" "$HE" "$RD" "$RV" "$RL" "$AS" "$PS" "$SS" "$CM" "$SV" "$RG")
T=$(mktemp -d "${TMPDIR:-/tmp}/p16m.XXXXXX") || exit 2; mkdir -p "$T/B" "$T/E"
trap 'srv_stop 2>/dev/null; rm -rf "$T"' EXIT   # 갈래가 도중에 멈춰도 띄운 서버를 내린다
# 두 판을 풀어 둔 폴더에서 잰다 — 작업 폴더에 남은 다른 Phase 의 미커밋 변경이 끼지 않는다
# 풀기가 도중에 끊기면 0 을 기대하는 값이 통과로 읽힌다 — 여기서 멈춘다
git archive "$B" | tar -x -C "$T/B" && git archive "$END" | tar -x -C "$T/E" || { echo "SNAPSHOT_FAIL — 측정을 멈춘다"; exit 2; }
for f in "${FILES[@]}"; do [ -s "$T/B/$f" ] && [ -s "$T/E/$f" ] || { echo "SNAPSHOT_FAIL $f"; exit 2; }; done
# sect <파일> <제목 앞부분> — 그 제목부터 같은 깊이 이하의 다음 제목 전까지. 코드 펜스 안의 `#` 줄은 제목으로 보지 않는다
sect() { awk -v h="$2" '
  /^[[:space:]]*(```|~~~)/ { fence = !fence }
  !f && !fence && index($0, h) == 1 { f = 1; lvl = match($0, /[^#]/) - 1; print; next }
  f && !fence && /^#+ / { l = match($0, /[^#]/) - 1; if (l <= lvl) exit }
  f' "$1"; }
# gline <파일> <줄 앞부분> — 그 앞부분으로 시작하는 줄
gline() { awk -v p="$2" 'index($0, p) == 1' "$1"; }
# toks <글> <토큰…> — 토큰마다 글 안에서 그 토큰이 든 줄 수
toks() { local s="$1"; shift; for t in "$@"; do printf '%s ' "$(printf '%s\n' "$s" | grep -cF -- "$t")"; done; echo; }
# runp <글> <앞부분…> — 이어진 줄들이 차례로 그 앞부분으로 시작하는 자리 수 (표 행이 붙어 있는지)
runp() { local s="$1"; shift; printf '%s\n' "$s" | awk -v n="$#" -v a="$(printf '%s\037' "$@")" '
  BEGIN { split(a, p, "\037") } { l[NR] = $0 }
  END { c = 0; for (i = 1; i + n - 1 <= NR; i++) { ok = 1; for (j = 1; j <= n; j++) if (index(l[i + j - 1], p[j]) != 1) { ok = 0; break }; if (ok) c++ }; print c }'; }
# fmb <파일> — 첫 frontmatter 블록 본문
fmb() { awk 'NR==1&&/^---/{fm=1;next} fm&&/^---/{exit} fm' "$1"; }
# jsblock <SKILL.md> — §7 안 첫 js 코드 블록 본문 (브라우저 확인 식)
jsblock() { awk '/^## 7\. /{s=1} /^## 8\. /{s=0} s&&/^```js$/{b=1;next} s&&b&&/^```$/{exit} s&&b' "$1"; }
# oldn <판 폴더> <글…> — 글마다 api-kit · docs/api 에서 그 글이 든 줄 수. 연구 기록은 뺀다 — 옛 기재를 역사로 인용하는 파일이다(SK-11 이 따로 잰다)
oldn() { local r="$1"; shift; for t in "$@"; do printf '%s ' "$(find "$r/api-kit" "$r/docs/api" -type f ! -name research-log.md -exec grep -hF -- "$t" {} + | grep -c .)"; done; echo; }
# barefence <파일> — 언어 힌트 없는 여는 펜스 수 (여닫기를 번갈아 센다)
barefence() { awk '/^[[:space:]]*```/{ if (!o) { o = 1; if ($0 ~ /^[[:space:]]*```[[:space:]]*$/) n++ } else o = 0 } END{print n+0}' "$1"; }
# url — 문서 속 출처 URL. 로컬 주소(127.0.0.1 · localhost)는 출처가 아니라 명령 예시라 뺀다
url()   { grep -oE 'https?://[^ )>"`]+' | sed -E 's/[.,;:]+$//' | grep -vE '^https?://(127\.0\.0\.1|localhost)([:/]|$)' | sort -u; }
added() { for f in "${FILES[@]}"; do git diff --no-index -U0 "$T/B/$f" "$T/E/$f"; done | grep '^+' | grep -v '^+++'; }
mine() { git log --format= --name-only "${1}..${2}" --grep="^${3}\$" | grep . | LC_ALL=C sort -u; }
unsigned_on() { _b=${1}; _u=${2}; _s=${3}; shift 3
  git log --format=%H "${_b}..${_u}" -- "$@" | while read -r _c; do git log -1 --format=%B "$_c" | grep -qxF "$_s" || echo "$_c"; done; }
# not_other <base> <상한> <서명> <경로…> — 경로를 건드린 구간 안 커밋 가운데 다른 Phase 서명이 없는 커밋 (0 줄이어야 한다)
not_other() { _b=${1}; _u=${2}; _s=${3}; shift 3
  git log --format=%H "${_b}..${_u}" -- "$@" | while read -r _c; do
    _m=$(git log -1 --format=%B "$_c")
    if printf '%s\n' "$_m" | grep -qE '^Kaizen-Phase: ' && ! printf '%s\n' "$_m" | grep -qxF "$_s"; then continue; fi
    echo "$_c"; done; }
my() { mine "$B" "$END" "$SIG"; }
# scope <계약> — `## 범위 경계` 절 안, 첫 줄이 `# sprint-scope` 인 text 블록의 경로 줄
scope() { awk '/^## /{s=$0} s ~ /^## 범위 경계/ && /^```text$/{b=1; n=0; next} b && /^```$/{b=0; next} b{n++; if (n==1 && $0 != "# sprint-scope") b=0; else if (n>1) print}' "$1"; }
fm_get() { awk -v k="^$2:[[:space:]]*" 'NR==1 && /^---[[:space:]]*$/ { fm=1; next } fm && /^---[[:space:]]*$/ { exit } fm && $0 ~ k { sub(k, "", $0); print; exit }' "$1" | sed -e "s/[[:space:]]*$//" -e "s/^['\"]//" -e "s/['\"]\$//"; }
sha256_16() { if command -v sha256sum >/dev/null 2>&1; then sha256sum; elif command -v shasum >/dev/null 2>&1; then shasum -a 256; else python3 -c 'import hashlib,sys; print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())'; fi | cut -c1-16; }
contract_digest() { grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$1" | sed -E 's/^- \[[ x]\]/- [ ]/' | sha256_16; }
verify_seal() { rec=$(fm_get "$1" conditions_digest); rec=${rec#sha256:}; if [ -z "$rec" ]; then echo "SEAL_ABSENT $1"; return 0; fi
  act=$(contract_digest "$1"); if [ "$rec" = "$act" ]; then echo "SEAL_OK $1"; else echo "SEAL_BROKEN $1 recorded=$rec actual=$act"; fi; }
# srv_start <폴더> — 그 폴더를 127.0.0.1 빈 포트로 내보내고 포트를 낸다. 못 띄우면 SRV_FAIL (측정이 조용히 0 을 내지 않게)
srv_start() { python3 "$K/srv.py" "$1" > "$T/srv.port" 2>/dev/null & echo $! > "$T/srv.pid"
  for _i in 1 2 3 4 5 6 7 8 9 10; do [ -s "$T/srv.port" ] && break; sleep 0.3; done
  [ -s "$T/srv.port" ] || { echo "SRV_FAIL"; return 2; }; cat "$T/srv.port"; }
srv_stop() { [ -f "$T/srv.pid" ] && kill "$(cat "$T/srv.pid")" 2>/dev/null; rm -f "$T/srv.pid" "$T/srv.port"; }
K02='(을|를) ?(처리|관리)(합니다|한다)|에 대해서?|하도록 (합니다|한다)|에 의(해|하여)|되어 있(는 경우|을 때)|(표시|적용|호출|생성|반환)(됩니다|된다)'
NAMES='fit-?pal|fit_pal|flutter[-_]playwright|playwright[ _-]?mcp|chrome-devtools-mcp'
```

```bash
# m.sh — 조건마다 재는 값을 한 줄씩 낸다. common.sh 를 읽은 bash 에서 `m <조건 ID>` 로 부른다
m() {
  local E=$T/E S f fn o p q
  # 도우미가 하나라도 없으면 grep -c 가 조용히 0 을 낸다 — 멈춘다
  for fn in sect gline toks runp fmb jsblock oldn barefence url added mine unsigned_on not_other my scope fm_get verify_seal srv_start srv_stop; do
    type "$fn" >/dev/null 2>&1 || { echo "HELPER_MISSING $fn"; return 2; }; done
  [ -n "${T:-}" ] && [ -d "$T/B" ] && [ -d "$E" ] || { echo "SNAPSHOT_MISSING"; return 2; }
  case "$1" in
  SK-01)  # api-verify — §6 경로 간 불변식 양쪽 값 · 판정 불가, §9 · §11 집계
    S=$(sect "$E/$V" '## 6. drift 분류')
    toks "$S" 'pin 항목 중 **경로 간 불변식**(`$.meta.total >= len($.data)`)은 여기서 후처리로 검사한다.' \
      '`.hurl` 에도 적을 수는 있다 — 한쪽을 capture 해 판정식 값에 넣으면 된다(`jsonpath "$.data" count <= {{total}}`).' \
      '하지만 한쪽 경로가 없으면 Hurl 이 종료 코드 `3` 을 내 환경 실패로 잘못 분류되고, 아래 `판정 불가` 를 표현할 곳이 없다.' \
      '- **판정 줄마다 양쪽 실제 값을 적는다** — `$.meta.total=47 · len($.data)=10 → PASS`, `$.meta.total=-1 · len($.data)=10 → FAIL`.' \
      'Hurl 의 실패 출력도 값은 찍지만 판정식에 넣은 값이 어느 경로에서 왔는지는 찍지 않는다.' \
      '- **한쪽 경로라도 없으면 `판정 불가` 다** — `$.meta.total=(없음) · len($.data)=10 → 판정 불가`.' \
      'PASS 로도 FAIL 로도 세지 않고 따로 센다. 그 자체로는 게이트를 깨지 않는다' \
      '사라진 경로가 계약에 `required` 면 schema drift(필드 삭제 = 계약 실패)가 따로 잡는다.' \
      '`판정 불가` 를 PASS 에 합치면 경로가 사라진 회귀가 조용히 지나간다.'
    toks "$(sect "$E/$V" '## 9. 리포트 생성')" '1. 실행 요약 — 대상 수, PASS / FAIL / 보류 / flaky / 판정 불가, 실행 모드, 환경' \
      '7. 경로 간 불변식 판정 줄 — 양쪽 실제 값과 PASS · FAIL · 판정 불가 (§6)'
    toks "$(sect "$E/$V" '## 11. 보고와 다음 단계')" '1. 판정 요약 (PASS/FAIL/보류/flaky/판정 불가 카운트 + 종료 코드)' \
      '3. 게이트를 깨지 않은 항목 — pending baseline, 환경 실패, 데이터 부재, 판정 불가(없는 경로 이름과 함께)'
    echo "old=$(grep -cF '`.hurl` 로 표현되지 않은' "$E/$V") list_blank_after=$(printf '%s\n' "$S" | awk '/^- \*\*한쪽 경로라도 없으면/{getline n; print (n=="")?1:0}')" ;;
  SK-02)  # 실패 분류 참조 문서 · 회귀 정책 문서 — 판정 불가, 그리고 문서가 적은 Hurl 동작을 로컬 hurl 로 다시 잰다
    toks "$(sect "$E/$FT" '## 5. value drift 판정')" \
      '| 경로 간 불변식 (`$.meta.total >= len($.data)`) | 후처리에서 검사하고 판정 줄마다 양쪽 실제 값을 적는다(`$.meta.total=47 · len($.data)=10 → PASS`).' \
      '한쪽 경로라도 없으면 `판정 불가` — PASS 도 FAIL 도 아니라 따로 세고, 사라진 경로가 `required` 면 §4 필드 삭제가 잡는다.' \
      '`.hurl` 에 적으면 경로가 없을 때 종료 코드 `3` 이 나 환경 실패로 잘못 분류된다 |'
    echo "old=$(grep -cF 'Hurl 로 표현 불가' "$E/$FT") junit_row=$(runp "$(sect "$E/$FT" '## 8. CI artifact 매핑')" '| 계약 파일 오류 (exit `2`) | `error` |' '| 판정 불가 (경로 간 불변식의 한쪽 경로 없음) | `skipped` + 사유(없는 경로 이름) — 게이트 미파괴 |')"
    toks "$(sect "$E/$RG" '## Gotchas')" '- **경로 간 불변식은 판정 줄마다 양쪽 실제 값을 남기고, 한쪽 경로가 없으면 `판정 불가` 로 따로 센다**' \
      'Hurl 실패 출력은 `actual` · `expected` 값을 찍지만 판정식에 넣은 값이 어느 경로에서 왔는지는 찍지 않는다.' \
      '없는 경로를 바로 검사하면 `4`, capture 하면 `3` 이다(실측 2026-09-24, hurl 8.0.1).' \
      '그래서 `판정 불가` 는 `/api-verify` 후처리에서만 만들 수 있고'
    command -v hurl >/dev/null || { echo "TOOL_MISSING hurl"; return 2; }
    # 기대값이 hurl 8.0.1 동작에 묶여 있다 — 판이 바뀌면 구현 탓 FAIL 이 아니라 측정 멈춤으로 드러낸다
    hurl --version 2>/dev/null | head -1 | grep -q '^hurl 8\.0\.1 ' || { echo "HURL_VERSION_CHANGED $(hurl --version 2>/dev/null | head -1)"; return 2; }
    mkdir -p "$T/site"; p=$(srv_start "$T/site") || { echo "$p"; return 2; }
    q='GET http://127.0.0.1:{{port}}/fx/%s\nHTTP 200\n[Captures]\ntotal: jsonpath "$.meta.total"\n[Asserts]\njsonpath "$.data" count <= {{total}}\n'
    for f in ok bad nometa; do printf "$q" "$f" > "$T/h-$f.hurl"; done
    printf 'GET http://127.0.0.1:{{port}}/fx/nometa\nHTTP 200\n[Asserts]\njsonpath "$.meta.total" >= 10\n' > "$T/h-direct.hurl"
    o=""; for f in ok bad nometa direct; do hurl --test --variable port="$p" "$T/h-$f.hurl" > /dev/null 2> "$T/h-$f.err"; o="$o$f=$? "; done; srv_stop
    echo "hurl ${o}bad_actual=$(grep -cF 'actual:   integer <10>' "$T/h-bad.err") bad_names_path=$(grep -cF 'meta.total' "$T/h-bad.err") nometa_noquery=$(grep -cF 'No query result' "$T/h-nometa.err") direct_none=$(grep -cF 'actual:   none' "$T/h-direct.err")" ;;
  SK-03)  # 「Hurl 로 표현 불가」 기재 정정 — api-contract Gotcha · strictness-modes, 옛 글은 킷 · 문서 전체에서 0
    toks "$(sect "$E/$C" '## Gotchas')" \
      '같은 경로 간 불변식은 `.hurl` 이 아니라 `contracts/*.yaml` 의 `pin` 으로만 기록하고 `/api-verify` 후처리에서 검사한다.' \
      '`.hurl` 에도 한쪽을 capture 해 판정식 값에 넣으면 적을 수는 있지만(`jsonpath "$.data" count <= {{total}}`), 한쪽 경로가 없으면 종료 코드 `3` 이 나 환경 실패로 잘못 분류되고 `판정 불가` 를 따로 셀 수 없다(실측 2026-09-24).'
    toks "$(sect "$E/$SM" '### Hurl 표현 가능 여부')" \
      '| 경로 간 불변식 (`>= len($.data)`) | 제한적 — 한쪽을 capture 해 판정식 값에 넣으면 적을 수 있다. 경로가 없으면 종료 코드 `3` |' \
      '양쪽 값과 `판정 불가` 는 후처리에서만 적을 수 있다 |' \
      'Hurl assert 는 경로 하나에 predicate 하나지만, 판정식 값에 capture 한 변수를 넣을 수 있다(실측 2026-09-24).' \
      '그래도 경로 간 불변식은 후처리에 둔다 — 경로가 없을 때 `판정 불가` 를 환경 실패와 가를 수 있는 곳이 후처리뿐이다.'
    echo "old=$(oldn "$E" 'Hurl 로 표현 불가' '로 표현되지 않은' '| **불가** |' '경로 하나에 predicate 하나**이므로' '경로 하나에 predicate 하나다.')" ;;
  SK-04)  # pin 을 만드는 쪽 — 새 pin 변이 확인(스킬 · 문서) · 검토 에이전트 3 행의 양쪽 경로
    S=$(sect "$E/$C" '## 11. 보고')
    toks "$S" '4. **새로 만든 pin 의 변이 확인** — pin 마다 스냅샷 **사본**의 그 값을 타입은 두고 한 번 망가뜨려(`47` → `-1`, `"Bearer"` → `"bearer"`) 그 pin 판정이 FAIL 을 내는지 본 결과.' \
      '먼저 사본에 변이가 실제로 들어갔는지 값으로 확인한다 — 안 들어간 사본의 PASS 를 보고 pin 이 죽었다고 오진하지 않게.' \
      '`.hurl` pin 은 사본을 `127.0.0.1` 로컬 서버로 돌려주고 그 케이스를 돌리고, 경로 간 불변식은 `/api-verify` §6 후처리를 사본에 돌린다.' \
      '봉인된 baseline 과 원본 스냅샷은 건드리지 않는다'
    printf '%s\n' "$S" | grep -oE '^[0-9]+\. ' | tr -dc '0-9\n' | paste -sd' ' -
    toks "$(sect "$E/$CM" '## Gotchas')" '- **새 pin 은 한 번 망가뜨려 본다** — 결함을 일부러 넣고 검사를 돌려 실패하면 그 결함은 잡힌 것이고, 통과하면 검사 묶음에 문제가 있다는 신호다([PIT](https://pitest.org/)).' \
      'pin 을 새로 만들었으면 스냅샷 **사본**의 그 값을 타입은 그대로 두고 망가뜨려(`47` → `-1`) 그 pin 이 FAIL 을 내는지 본다.' \
      '사본에 변이가 실제로 들어갔는지 먼저 확인하고, 봉인된 baseline 은 건드리지 않는다.'
    echo "$(toks "$(gline "$E/$RV" '| 3 | Pin Assertion Fitness |')" '| 3 | Pin Assertion Fitness | pin 경로가 스냅샷에 실제로 존재한다 — 경로 간 불변식은 판정식 쪽 경로(`>= len($.data)` 의 `$.data`)까지 양쪽 모두 (부재 경로 pin 0 건) |' \
      '경로 간 불변식은 한쪽이 없으면 `/api-verify` 가 매번 `판정 불가` 를 낸다 |')rows=$(grep -cE '^\| [0-9]+ \| ' "$E/$RV")" ;;
  SK-05)  # api-ui §7 브라우저 확인 글 · 기대값 표 · §8 보고
    S=$(sect "$E/$U" '## 7. 자기 검증 (건너뛰기 금지)')
    toks "$S" '**브라우저로 열어 확인한다.** 글자 검사는 화면이 실제로 그려지는지 보지 못한다.' \
      '1. **여는 방법** — 브라우저 조종 도구 가운데 기본 설정에서 `file://` 주소를 막는 것이 있다(오류 예: `Access to "file:" protocol is blocked`).' \
      '`D=$(mktemp -d) && cp .api/ui.html "$D/" && python3 -m http.server 8765 --bind 127.0.0.1 --directory "$D"` 로 `ui.html` 한 장만 든 빈 폴더를 띄우고 `http://127.0.0.1:8765/ui.html` 을 열거나, 도구의 로컬 파일 허용 설정을 켜고 `file://` 로 연다. 어느 쪽으로 열었는지 보고에 적는다.' \
      '`.api/` 를 통째로 띄우지 마라 — `credentials.local.json`(아이디 · 비밀번호) · `reports/`(가리지 않은 원본 응답) · `snapshots/prod/` 가 HTTP 로 열리고, 출처가 `http://127.0.0.1` 로 바뀌어 옆 파일 `fetch` 가 성공해 버린다.' \
      '한 장만 든 폴더에서는 옆 파일 `fetch` 가 404 콘솔 오류로 드러난다(실측 2026-09-25). 그래도 외부 참조 0 건은 위 `grep` 검사로 잰다 — 브라우저 확인으로 대신하지 마라.' \
      '2. **콘솔 오류** — error 등급 메시지가 0 개다. 웹 서버로 열었을 때 `favicon.ico` 를 가리키는 404 한 건은 빼고 세되 뺀 건수를 따로 적는다' \
      '3. **항목 수 · 누르는 자리** — 필터와 검색을 건드리지 않은 첫 화면에서 아래 식을 페이지 안에서 돌린다. `ep` 와 `shown` 이 같고 `under24` 가 0 이어야 한다.' \
      '`under44` 는 권장값 44 에 못 미치는 수라 판정에 쓰지 않고 보고에만 적는다.' \
      '확정 시안 1280×720 실측(2026-09-25): `ep 14 · shown 14 · targets 56 · under24 0 · under44 39`.' \
      '브라우저 조종 도구가 없어 이 확인을 못 하면 조용히 건너뛰지 말고 `[미검증]` 에 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 붙여 보고한다.' \
      '| 누르는 자리 최소 크기 | 요소 상자 24×24 CSS px 미만 `0` 개 (아래 `under24`). 44 는 권장값 | WCAG 2.2 2.5.8 (AA, 24) · 2.5.5 (AAA, 44).'
    echo "rows=$(runp "$S" '| 테마 |' '| 인라인 항목 수 = 화면 항목 수 | `ep` = `shown` |' '| 콘솔 error 메시지 | `0` (`favicon.ico` 404 한 건은 뺀다) |') js=$(printf '%s\n' "$S" | grep -cx '```js') old=$(grep -cF '| 클릭 타깃 최소 크기 | `44px` |' "$E/$U") dir_api=$(grep -cF -- '--directory .api' "$E/$U")"
    toks "$(sect "$E/$U" '## 8. 열기와 보고')" '- Step 7 브라우저 확인 — 연 방법 · 콘솔 error 수와 뺀 `favicon.ico` 건수 · `ep` · `shown` · `under24` · `under44`. 못 했으면 `[미검증]` 과 네 칸' ;;
  SK-06)  # §7 의 식을 끝 판 SKILL.md 에서 뽑아 확정 시안 사본에 실제로 돌린다 — 대조 사본 넷과 CSP 사본 포함
    [ -f "$MOCKUP" ] || { echo "MOCKUP_MISSING"; return 2; }
    [ "$(shasum -a 256 "$MOCKUP" | cut -c1-16)" = "$MOCKUP_SHA16" ] || { echo "MOCKUP_CHANGED"; return 2; }
    command -v node >/dev/null && [ -d "$PW" ] || { echo "TOOL_MISSING node/playwright"; return 2; }
    jsblock "$E/$U" > "$T/expr.js"; [ -s "$T/expr.js" ] || { echo "EXPR_MISSING"; return 2; }
    mkdir -p "$T/site"; cp "$MOCKUP" "$T/site/ui.html"
    python3 - "$T/site" <<'PY' || { echo "NEG_EDIT_FAIL"; return 2; }
import os, sys
d = sys.argv[1]; s = open(os.path.join(d, "ui.html"), encoding="utf-8").read()
V = {"n1": ("</head>", '<style>[data-ep="auth.token"]{display:none!important}</style></head>'),
     "n2": ("</body>", '<button style="position:fixed;left:0;top:0;width:10px;height:10px">x</button></body>'),
     "n3": ("</body>", '<script>console.error("probe-neg")</script></body>'),
     # 옆 파일을 부르면 파일 하나만 내보내는 폴더에서 404 콘솔 오류로 드러난다 — SK-05 여는 방법 문장의 알려진 답
     "n4": ("</body>", '<script>fetch("./data.json")</script></body>'),
     # 실제로 만들 뷰어는 뷰어 스펙 §1 의 CSP <meta> 를 단다 — 확정 시안에는 없어 사본에 넣어 같은 식을 돌린다
     "csp": ("<head>", "<head><meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'\">")}
for k, (a, b) in V.items():
    if s.count(a) != 1: sys.exit(1)
    open(os.path.join(d, k + ".html"), "w", encoding="utf-8").write(s.replace(a, b))
PY
    p=$(srv_start "$T/site") || { echo "$p"; return 2; }
    for q in "ui chromium" "ui shell" "n1 chromium" "n2 chromium" "n3 chromium" "n4 chromium" "csp chromium"; do set -- $q
      node "$K/probe.js" "http://127.0.0.1:$p/$1.html" "$2" "$T/expr.js" | python3 -c '
import json, sys
t = sys.stdin.read().strip()
if not t.startswith("{"): print(sys.argv[1], sys.argv[2], t or "PROBE_EMPTY"); sys.exit()
d = json.loads(t); v = d["v"]; e = d["errors"]
fav = sum(1 for x in e if "favicon.ico" in x["url"] or "favicon.ico" in x["text"])
print(sys.argv[1], sys.argv[2], "ep=%s shown=%s targets=%s under24=%s under44=%s err_other=%d err_favicon=%d" % (v.get("ep"), v.get("shown"), v.get("targets"), v.get("under24"), v.get("under44"), len(e) - fav, fav))' "$1" "$2"
    done; srv_stop ;;
  SK-07)  # 뷰어 스펙 · 뷰어 계약 문서 — 누르는 자리 기준 · data-ep · 그룹 펼침, 옛 44px 는 킷 · 문서 전체에서 0
    toks "$(sect "$E/$VS" '## 1. 하드 제약')" '| 누르는 자리 | 요소 상자 ≥ 24×24 CSS px (44 는 권장) | 24 미만이면 간격 예외를 따지기 전에 고친다 — 요소 상자만 재므로 WCAG 2.2 2.5.8 (AA) 보다 엄하다. 확정 시안 실측은 44 미만 39/56 · 24 미만 0 — `SKILL.md` §7 `under24` 로 잰다 |'
    toks "$(sect "$E/$VS" '### 3.2 사이드바 — 엔드포인트 트리')" '행 버튼에는 `data-ep="<엔드포인트 id>"` 를 단다 — `SKILL.md` §7 브라우저 확인이 이 속성으로 화면에 보이는 항목을 센다.' \
      '- 첫 화면에서 그룹은 모두 펼친다(확정 시안 `openGroups` 초기값이 전부 `true`). 접힌 채 시작하면 `SKILL.md` §7 의 `shown` 이 `ep` 보다 작게 나와 항목이 빠진 것과 구별되지 않는다.'
    toks "$(sect "$E/$SV" '## 수치 기준')" '| 누르는 자리 최소 크기 | 요소 상자 `24×24` CSS px 미만 `0` 개. `44×44` 는 권장값 | [WCAG 2.2](https://www.w3.org/TR/WCAG22/) 2.5.8 (AA) · 2.5.5 (AAA). 확정 시안 1280×720 실측(2026-09-25): 보이는 누르는 요소 56 개 중 24 미만 0 · 44 미만 39 |'
    toks "$(sect "$E/$SV" '## Gotchas')" '- **브라우저로 여는 확인은 글자 검사를 대신하지 못한다** — 브라우저를 조종하는 도구 가운데 기본 설정에서 `file://` 주소를 막는 것이 있어' \
      '`.api/` 폴더를 통째로 띄우면 출처가 `http://127.0.0.1` 로 바뀌어 `file://` 에서 막히는 옆 파일 `fetch` 가 성공해 버리고 `credentials.local.json` · `reports/` 까지 HTTP 로 열린다 — `ui.html` 한 장만 든 빈 폴더를 띄운다.' \
      '웹 서버로 열면 `favicon.ico` 404 콘솔 오류가 한 건 생길 수 있다 — 아이콘 링크가 없어 브라우저가 기본 경로를 부른 것이지 뷰어 결함이 아니다.' \
      '헤드리스 셸은 아이콘을 아예 부르지 않아 이 한 건도 안 나온다(실측 2026-09-24).'
    echo "old=$(oldn "$E" '44px' '클릭 타깃')" ;;
  SK-08)  # 환경변수로 넣는 변수 — 네 자리 정정, 그리고 문서가 적은 동작을 로컬 hurl 로 다시 잰다
    toks "$(cat "$E/$HE")" '- **환경변수로 변수를 넣으려면 `HURL_VARIABLE_` 접두가 필요하다**' \
      'Hurl 8.0.0 부터 변수 접두는 `HURL_VARIABLE_` 이라 `HURL_VARIABLE_who` 가 `{{who}}` 를 채우고, `HURL_SECRET_<이름>` 은 `--secret` 처럼 값을 가린다.' \
      '둘이 겹치면 명령줄 `--variable` 이 이긴다 (실측 2026-09-24).' \
      'CI 환경에 남은 `HURL_VARIABLE_*` 가 `{{baseUrl}}` 같은 변수를 조용히 채울 수 있으니 필요한 변수는 명령줄로 준다.'
    toks "$(sect "$E/$AS" '## Gotchas')" '- **환경변수로 변수를 넣으려면 `HURL_VARIABLE_` 접두가 필요하다**' \
      'Hurl 8.0.0부터 `HURL_VARIABLE_who`가 `{{who}}`를 채우고 `HURL_SECRET_<이름>`은 `--secret`처럼 값을 가린다' \
      '겹치면 명령줄 `--variable`이 이긴다(실측 2026-09-24, hurl 8.0.1).'
    toks "$(cat "$E/$PS")" '변수는 접두가 다르다 — `HURL_who` 를 걸어도 `{{who}}` 는 채워지지 않고, Hurl 8.0.0 부터는 `HURL_VARIABLE_who` 가 채운다.' \
      '`HURL_SECRET_<이름>` 은 `--secret` 처럼 값을 가린다.' '변수도 같은 우선순위를 따라 명령줄 `--variable` 이 환경변수를 이긴다.' \
      '[Hurl CHANGELOG](https://github.com/Orange-OpenSource/hurl/blob/master/CHANGELOG.md) 8.0.0 · 실측 (hurl 8.0.1, 2026-09-05 · 2026-09-24)' \
      '| 환경변수로 들어가는 변수 | `HURL_VARIABLE_<이름>` 만 (`HURL_<이름>` 은 안 된다). 명령줄 `--variable` 이 이긴다 | 실측 |'
    echo "old=$(oldn "$E" '옵션에만 붙고 변수에는 안 붙는다' '이 규칙은 **옵션에만** 적용된다' '변수는 `HURL_*` 로 안 들어온다')"
    command -v hurl >/dev/null || { echo "TOOL_MISSING hurl"; return 2; }
    # 기대값이 hurl 8.0.1 동작에 묶여 있다 — 판이 바뀌면 구현 탓 FAIL 이 아니라 측정 멈춤으로 드러낸다
    hurl --version 2>/dev/null | head -1 | grep -q '^hurl 8\.0\.1 ' || { echo "HURL_VERSION_CHANGED $(hurl --version 2>/dev/null | head -1)"; return 2; }
    mkdir -p "$T/site"; p=$(srv_start "$T/site") || { echo "$p"; return 2; }
    printf 'GET http://127.0.0.1:{{port}}/fx/ok\nHTTP 200\n[Asserts]\nvariable "who" == "from-env"\n' > "$T/h-env.hurl"
    printf 'GET http://127.0.0.1:{{port}}/fx/sec\nHTTP 200\n[Asserts]\njsonpath "$.token" == "nope"\n' > "$T/h-sec.hurl"
    env -u HURL_VARIABLE_who HURL_who=from-env hurl --test --variable port="$p" "$T/h-env.hurl" >/dev/null 2>&1; o="plain=$?"
    HURL_VARIABLE_who=from-env hurl --test --variable port="$p" "$T/h-env.hurl" >/dev/null 2>&1; o="$o prefixed=$?"
    HURL_VARIABLE_who=from-env hurl --test --variable port="$p" --variable who=from-cli "$T/h-env.hurl" >/dev/null 2> "$T/h-cli.err"; o="$o cli=$? cli_actual=$(grep -cF 'actual:   string <from-cli>' "$T/h-cli.err")"
    # 본문이 이 채널에 실리는지 먼저 본다(marker) — 안 실리면 시크릿 0 은 마스킹이 아니라 미수록이다. 시크릿을 안 건 판이 양성 대조다
    HURL_SECRET_tok=sekret-p16 hurl --test --variable port="$p" --error-format long "$T/h-sec.hurl" >/dev/null 2> "$T/h-sec.err"
    env -u HURL_SECRET_tok hurl --test --variable port="$p" --error-format long "$T/h-sec.hurl" >/dev/null 2> "$T/h-nosec.err"
    o="$o | secret: plain=$(grep -cF 'sekret-p16' "$T/h-sec.err") masked=$(grep -cF '"token": "***"' "$T/h-sec.err") marker=$(grep -cF 'plain-marker' "$T/h-sec.err") no_secret_plain=$(grep -cF 'sekret-p16' "$T/h-nosec.err")"
    srv_stop; echo "hurl $o" ;;
  SK-09)  # --secret 이 가린다고 확인된 곳 — 스킬 셋 · README · hurl-execution §6 표, 그리고 --curl 파일 마스킹을 로컬 hurl 로 다시 잰다
    toks "$(sect "$E/$V" '## Gotchas')" 'Hurl `--secret` 이 exact match 로 가린다고 확인된 곳은 **stderr 로그 · JSON 리포트의 `report.json` · `--curl` 파일**이다' \
      '`--output <file>`, `--json` 출력(`curl_cmd` · 요청 헤더 · `captures`), JSON 리포트의 `store/*_response.json` 은 가리지 않는다(실측 2026-09-05).' \
      '`--very-verbose` 는 본문을 stderr 에 찍으면서 등록한 값만 `***` 로 바꾸고 등록하지 않은 변형은 그대로 남긴다.'
    toks "$(sect "$E/$U" '## Gotchas')" 'Hurl 의 `--secret` 이 exact match 로 가린다고 확인된 곳은 stderr 로그 · JSON 리포트의 `report.json` · `--curl` 파일이다(실측 2026-09-05 · 2026-09-24).' \
      '`--output <file>`, `--json` 출력, 리포트의 `store/*_response.json` 같은 저장된 raw body 는 **가리지 않는다**.'
    toks "$(sect "$E/$P" '## Gotchas')" '`--secret` 이 가린다고 확인된 곳은 stderr 로그 · JSON 리포트의 `report.json` · `--curl` 파일이다(실측 2026-09-05 · 2026-09-24).' \
      '`--output <file>`, `--json` stdout, JSON 리포트의 `store/*_response.json` 에는 토큰이 평문으로 남는다.' \
      '등록한 시크릿 값은 `***` 로 바뀌지만 등록하지 않은 변형(base64 · 대소문자 · `Bearer` 접두)과 시크릿으로 등록하지 않은 개인정보는 CI 로그에 그대로 남는다.'
    toks "$(cat "$E/$RD")" 'Hurl `--secret` 은 stderr · JSON 리포트의 `report.json` · `--curl` 파일을 가리지만 stdout · `--output` 파일 · 리포트의 원본 응답 파일(`store/`)은 가리지 않는다'
    toks "$(cat "$E/$HE" "$E/$AS")" '| `--curl <file>` 의 헤더 값 (실측 2026-09-24) | `--output <file>` |' \
      '가린다고 확인된 곳은 stderr 로그(`--verbose` / `--very-verbose`), JSON 리포트의 `report.json`(`curl_cmd`·요청 헤더), `--curl <file>`의 헤더 값이다(`--curl`은 실측 2026-09-24).' \
      '| `--secret` 마스킹되는 채널 | stderr 로그, JSON 리포트 `report.json`, `--curl <file>` | 실측 2026-09-05 · 2026-09-24 (hurl 8.0.1) |' \
      '- **`--secret`이 가린다고 확인된 채널은 stderr 로그 · `report.json` · `--curl <file>`이다**'
    # 여섯째 · 일곱째 글은 가리는 곳을 다 적은 것처럼 말하는 초안 첫 판 글, 뒤 셋은 auth-secret-lifecycle 의 옛 글이다
    # 목록에 없는 말투는 curl_missing 이 잡는다 — report.json 과 가림 낱말이 같이 든 줄에 --curl 이 없으면 센다
    echo "old=$(oldn "$E" 'stderr 로그와 리포트만' 'stderr 로그와 리포트뿐' 'stderr 와 리포트만' 'body 를 stderr 에 그대로 뿌린다' '뱉으므로 CI 로그에 그대로 남는다' '`report.json` 뿐' '`report.json` 만 가리' \
      '`report.json`(`curl_cmd`·요청 헤더)뿐이다' '`report.json` 둘뿐' '| `--secret` 마스킹되는 채널 | stderr 로그, JSON 리포트 `report.json` |')curl_missing=$(find "$E/api-kit" "$E/docs/api" -type f ! -name research-log.md -exec grep -hF -- 'report.json' {} + | grep -E -- '--secret|가려지는|가리는|가린다|마스킹되는' | grep -cvF -- '--curl')"
    command -v hurl >/dev/null || { echo "TOOL_MISSING hurl"; return 2; }
    hurl --version 2>/dev/null | head -1 | grep -q '^hurl 8\.0\.1 ' || { echo "HURL_VERSION_CHANGED $(hurl --version 2>/dev/null | head -1)"; return 2; }
    mkdir -p "$T/site"; p=$(srv_start "$T/site") || { echo "$p"; return 2; }
    printf 'GET http://127.0.0.1:{{port}}/fx/sec\nAuthorization: Bearer {{tok}}\nHTTP 200\n' > "$T/h-curl.hurl"; rm -f "$T/c-sec.curl" "$T/c-var.curl"
    # 같은 값을 변수로 건 판이 양성 대조다 — 거기서 평문이 안 나오면 그 파일에 헤더가 안 실린 것이라 시크릿 판의 0 은 마스킹 증거가 아니다
    hurl --test --variable port="$p" --secret tok=sekret-p16 --curl "$T/c-sec.curl" "$T/h-curl.hurl" >/dev/null 2>&1; o="secret=$?"
    hurl --test --variable port="$p" --variable tok=sekret-p16 --curl "$T/c-var.curl" "$T/h-curl.hurl" >/dev/null 2>&1; o="$o variable=$?"
    srv_stop; echo "hurl curl $o secret_plain=$(grep -c 'sekret-p16' "$T/c-sec.curl") secret_masked=$(grep -cF 'Bearer ***' "$T/c-sec.curl") variable_plain=$(grep -c 'sekret-p16' "$T/c-var.curl")" ;;
  SK-10)  # -0 — 게이트 목록 다섯 자리와 문서 근거
    toks "$(sect "$E/$C" '## Gotchas')" 'lone surrogate·`-0`·안전 정수 범위' '`-0` 은 JCS 가 `0` 으로 적어 부호가 사라진다(RFC 8785 정정 7920).'
    toks "$(sect "$E/$C" '## 2. I-JSON 게이트')" '-0 (음의 영)                        → 실패 — JCS 가 0 으로 적어 부호가 사라진다'
    toks "$(sect "$E/$P" '## 7. 스크러빙 → 정규화 → 저장')" '2. I-JSON 검문 중복 키 · lone surrogate · NaN/Infinity · binary64 표현 불가 숫자 · -0'
    toks "$(sect "$E/$V" '## 5. 응답 정규화')" '- I-JSON 게이트 실패(중복 키·NaN·lone surrogate·`-0`)는 계약 실패가 아니라 **비교 불가**로 분류한다.'
    toks "$(sect "$E/$SS" '### 3. 정규화 전 I-JSON 게이트')" 'lone surrogate, `-0` 은 정규화 대상이 아니라 **실패 또는 fallback 대상**이다.' \
      '`-0` 은 올바른 JSON 숫자지만 JCS 가 `0` 으로 적어 부호가 사라진다 — 그래서 파서는 `-0` 을 만나면 오류를 내고 멈춰야 한다(SHOULD, RFC 8785 정정 7920 · 2024-05-15 확인).' \
      '[RFC 8785 정정 목록](https://www.rfc-editor.org/errata/rfc8785)'
    echo "js_minus_zero=$(node -e 'process.stdout.write(JSON.stringify(-0))' 2>/dev/null || echo NODE_MISSING)" ;;
  SK-11)  # 연구 기록 — 새 절 · 옛 절 정정 표시 · 지운 줄은 머리 설정 둘뿐
    fmb "$E/$RL" | grep -cxE 'version: 0\.3\.0|last_updated: 2026-09-24' | tr -d '\n'; echo
    S=$(sect "$E/$RL" '## [2026-09-24] — 첫 카이젠 (Phase 16)')
    toks "$S" '### 경로 간 불변식을 Hurl 에 적어 본 결과 (2026-09-24)' '### 뷰어를 브라우저로 연 결과 (2026-09-24)' '### 문서와 실측이 어긋난 것 (2026-09-24)' \
      '### 이번에 정한 것 (2026-09-24)' '### 이월 — 다음 사이클 후보 (2026-09-24)' \
      '| `$.meta` 없음 | `3` | `No query result` — capture 에서 멈춘다 |' '| 요소 상자 가로나 세로가 24 CSS px 미만 | 0 |' '| 44 CSS px 미만 | 39 |' \
      '| 환경변수로 넣는 변수 | `HURL_*` 는 변수에 안 붙는다' '- `판정 불가` 는 PASS 로도 FAIL 로도 세지 않고 따로 세며, 그 자체로는 게이트를 깨지 않는다.' \
      '- 누르는 자리의 통과선은 요소 상자 24×24 CSS px 미만 0 개다. 44 는 권장값으로 보고에만 적는다' \
      '- OpenAPI 3.2(최신 3.2.1) 의 `query` 메서드' '`/api-contract` §9 예시 `jsonpath "$.data[0].id" isString` 이 같은 파일 Gotcha 의 index assertion 금지와 어긋나는데,'
    toks "$(sect "$E/$RL" '## [2026-09-05] — Hurl 8.0.1 실측 대조')" '> **[2026-09-24 정정]** 이 단서는 `HURL_who` 만 재서 나온 것이다.' \
      '`HURL_who=from-env` 를 걸어도 `{{who}}` 변수는 채워지지 않고 assert 가 `actual: none` 으로 실패한다.'
    echo "removed=$(git diff --no-index -U0 "$T/B/$RL" "$E/$RL" | grep '^-' | grep -vc '^---') last_h2=$(grep '^## ' "$E/$RL" | tail -1)" ;;
  ER-01)  # 새로 생긴 URL 이 근거 파일에 있다 — 파일마다 편집 전 판과 비교, notes 는 URL 전부
    # 근거 파일은 .harness 안이라 이 Phase 가 고칠 수 있다 — 시작 커밋 판에서 읽고, 끝 판이 같은지 따로 잰다
    for f in "${FILES[@]}"; do comm -13 <(url < "$T/B/$f") <(url < "$E/$f"); done | sort -u | comm -23 - <(url < "$T/B/$EVID") | grep -c .
    if [ -f "$E/$NOTES" ]; then url < "$E/$NOTES" | comm -23 - <(url < "$T/B/$EVID") | grep -c .; else echo NOTES_MISSING; fi
    cmp -s "$T/B/$EVID" "$E/$EVID" && echo evid_same=1 || echo evid_same=0 ;;
  ER-02)  # 더한 줄의 번역투 6 종 · 앱 · 도구 서버 이름, 킷 · 문서 전체의 같은 이름
    echo "added=$(added | grep -c .) k02=$(added | grep -cE "$K02") names=$(added | grep -ciE "$NAMES") kit_names=$(grep -rhiE "$NAMES" "$E/api-kit" "$E/docs/api" | grep -c .)" ;;
  ER-03)  # notes 문자열 · 넘김 · 미반영 사유 · 공유 파일과 다른 Phase 파일을 건드린 커밋
    git cat-file -e "$END:$NOTES" 2>/dev/null && echo notes_committed=1 || echo notes_committed=0
    toks "$(cat "$E/$NOTES" 2>/dev/null)" '`other-kits:P7`' '`other-kits:P8`' '## 바꾼 파일' '## 반영한 처리 배정표 키' '## 미반영 키와 사유' \
      '## 넘기는 것' '## changelog 한 단락' '## 킷 로그 한 단락' '## 다음 사이클 메모' '## 사전 · 사후 측정'
    # 넘김 · 미반영 사유는 그 절 안에서 센다 — 낱말은 다른 절에도 나와 넘김 줄을 빠뜨려도 1 이 된다
    toks "$(sect "$E/$NOTES" '## 넘기는 것' 2>/dev/null)" 'docs/superpowers/specs/2026-09-02-api-kit-design.md' '.claude/skills/kaizen-orchestrator/SKILL.md' \
      'docs/api-kit/probe-synthesis-hurl-semantics.html' 'docs/api-kit/auth-secret-lifecycle.html' 'docs/api-kit/snapshot-sealing-canonicalization.html' \
      'docs/api-kit/contract-extraction-modes.html' 'docs/api-kit/regression-diff-failure-policy.html' 'docs/api-kit/static-evidence-viewer-contract.html' \
      'scripts/detect-docs-drift.py' 'plugin.json'
    toks "$(sect "$E/$NOTES" '## 미반영 키와 사유' 2>/dev/null)" 'OpenAPI 3.2' 'jsonpath' '대비' 'Pact' '8.1.0' 'api-reviewer'
    not_other "$B" "$END" "$SIG" .claude-plugin/marketplace.json api-kit/.claude-plugin/plugin.json README.md CLAUDE.md \
      .harness/.meta/orchestrator-audit-log.md .harness/.meta/kaizen-failure-count.yaml .claude/kaizen-input/insights-report.md \
      .github/workflows/ci.yml .harness/stale-values.yaml .claude/skills harness scripts docs/api-kit docs/index.html docs/superpowers | grep -c . ;;
  AR-01)  # 허용 경로 · 서명 · 봉인 · 범위 선언 블록
    unsigned_on "$B" "$END" "$SIG" api-kit docs/api | grep -c .
    echo "$(my | grep -v '^\.harness/' | grep -vxF -f <(printf '%s\n' "${FILES[@]}") | grep -c .) $(my | grep -cxF -f <(printf '%s\n' "${FILES[@]}"))"
    find .harness -type f -name 'sprint-contract*.md' -print0 | while IFS= read -r -d '' f; do verify_seal "$f"; done \
      | awk '$1=="SEAL_BROKEN"{print $2}' | sed 's#^\./##' | sort -u | comm -12 - <( { my; echo "$CF"; } | sort -u) | grep -c .
    verify_seal "$E/$CF" | cut -d' ' -f1
    diff <(scope "$E/$CF" | grep -vxF '.harness/' | sort) <(printf '%s\n' "${FILES[@]}" | sort) >/dev/null && echo "scope_same=1" || echo "scope_same=0"
    scope "$E/$CF" | grep -cxF '.harness/' ;;
  AR-02)  # 새 글이 가리키는 자리가 실제로 있다
    # 중괄호 든 글은 변수로 먼저 받는다 — bash 3.2 는 큰따옴표 안 $( ) 의 작은따옴표 글을 중괄호 확장해 값이 네 벌로 불어난다(실측)
    q=$(grep -cF 'openGroups:{ auth:true, orders:true, products:true, users:true }' "$MOCKUP")
    echo "$(grep -c '^## 7\. 자기 검증' "$E/$U") $(jsblock "$E/$U" | grep -c 'under24') | $(grep -c '^## 6\. drift 분류' "$E/$V") $(sect "$E/$V" '## 6. drift 분류' | grep -cF '판정 불가') | $(grep -c '^## 4\. schema drift 판정' "$E/$FT") $(sect "$E/$FT" '## 4. schema drift 판정' | grep -cF '| 필드 삭제 |') | $(grep -cF '## [2026-09-05] — Hurl 8.0.1 실측 대조' "$E/$RL") $(grep -cF '| L7 |' "$T/B/$EVID") | $(grep -c 'data-ep="' "$MOCKUP") $q" ;;
  AR-03)  # 손대지 않을 곳 — 확정 결정 줄 · 목록 밖 킷 · 문서 파일
    for q in "- **\`pin\` 은 '값 고정' 이 아니다" '- **`exact` 는 본문만 본다.' '- **enum 은 1 샘플이면 확정하지 않는다' '순서를 지킨다. **redaction → 마스크 적용 → JCS 직렬화.**'; do
      a=$(gline "$T/B/$C" "$q"); b=$(gline "$E/$C" "$q"); [ -n "$a" ] && [ "$a" = "$b" ] && printf '1 ' || printf '0 '; done; printf '| '
    for q in '- **exit code 3 과 4 를 절대 합치지 마라.**' '- **prod 는 실행 전에 게이트를 통과해야 한다.**' '| `3` | 런타임 오류' '| `4` | assert 실패'; do
      a=$(gline "$T/B/$V" "$q"); b=$(gline "$E/$V" "$q"); [ -n "$a" ] && [ "$a" = "$b" ] && printf '1 ' || printf '0 '; done; printf '| '
    ( cd "$E" && find api-kit docs/api -type f | sort ) > "$T/all.txt"
    echo "outside_changed=$(grep -vxF -f <(printf '%s\n' "${FILES[@]}") "$T/all.txt" | while read -r f; do cmp -s "$T/B/$f" "$E/$f" || echo "$f"; done | grep -c .) outside_n=$(grep -cvxF -f <(printf '%s\n' "${FILES[@]}") "$T/all.txt")" ;;
  AP-01)  # 더한 줄에 이 킷 플러그인 버전 값
    f=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$E/api-kit/.claude-plugin/plugin.json")
    echo "version=$f $(added | grep -cF -- "$f")" ;;
  AP-03)  # 언어 힌트 없는 여는 펜스 — 열일곱 파일
    for f in "${FILES[@]}"; do printf '%s' "$(barefence "$E/$f")"; done; echo ;;
  AP-04)  # 스킬 넷 · 에이전트 하나의 frontmatter 가 편집 전과 같고 name 줄이 하나씩
    for f in "$V" "$C" "$U" "$P" "$RV"; do printf '%s%s ' "$(diff <(fmb "$T/B/$f") <(fmb "$E/$f") >/dev/null && echo 1 || echo 0)" "$(fmb "$E/$f" | grep -c '^name: ')"; done; echo ;;
  DG-02)  # markdownlint — 파일마다 규칙별 경고 수를 편집 전 판과 비교. 더한 줄만 보면 옆 줄에 붙는 MD022 · MD032 · MD024 를 놓친다
    for f in "${FILES[@]}"; do L=$(printf '%s' "$f" | tr '/' '_'); cp "$E/$f" "$T/$L.md"; cp "$T/B/$f" "$T/$L.0.md"
      printf '%s ' "$f"; bash "$K/rule-delta.sh" "$T/$L.0.md" "$T/$L.md"; done ;;
  DG-05)  # 저장소 검사 — $END 판을 git 저장소로 만든 사본에서. 옛 값은 api-kit 을 안 훑는 check-stale-values.py 대신 열일곱 파일에서 직접 센다
    local G=$T/G; rm -rf "$G"; cp -R "$E" "$G"
    git -C "$G" init -q && git -C "$G" add -A && git -C "$G" -c user.name=m -c user.email=m@m commit -qm snap || return 2
    ( cd "$G" && python3 scripts/validate-plugin.py api-kit > "$T/vp.txt" 2>&1; echo $? > "$T/vp.rc" )
    echo "$(grep -cE '^  V([1-9]|10) ' "$T/vp.txt") $(grep -E '^  V([1-9]|10) ' "$T/vp.txt" | grep -cvE -- '— (OK|SKIP \(no templates/\))$') rc=$(cat "$T/vp.rc")"
    python3 - "$E/.harness/stale-values.yaml" "${FILES[@]/#/$E/}" <<'PY'
import sys, yaml
vals = [v["old"] for v in yaml.safe_load(open(sys.argv[1], encoding="utf-8"))["values"]]
hits = sum(open(p, encoding="utf-8").read().count(o) for p in sys.argv[2:] for o in vals)
print("stale_old=%d files=%d hits=%d" % (len(vals), len(sys.argv[2:]), hits))
PY
    ( cd "$G" && python3 scripts/sync-docs.py --check-only api-kit 2>&1 | grep -F 'api-kit/README.md:' ) ;;
  DG-06)  # 사이클 검사 — 이 Phase 몫 줄만 본다. docs-site-regen 은 Final F2 몫
    python3 scripts/validate-post-kaizen.py --since "$B" --verbose > "$T/vpk.txt" 2>&1
    grep -E '\] . (scope-isolation|doc-contracts): ' "$T/vpk.txt" | awk '{print $5, $2}'
    python3 scripts/validate-doc-contracts.py -v 2>&1 | awk -F' → ' '/^ *검사: /{a=$1; sub(/^ *검사: /,"",a); sub(/:[0-9]+$/,"",a); print a; print $2}' | sort -u > "$T/dc.txt"
    echo "doc_checked=$(grep -c . "$T/dc.txt") doc_mine=$(comm -12 "$T/dc.txt" <(my) | grep -c .)"
    awk '/ scope-isolation: /{f=1;next} /^\[ /{f=0} f&&/^ +[0-9a-f]{7,40}$/{print $1}' "$T/vpk.txt" > "$T/viol.txt"
    echo "violators=$(grep -c . "$T/viol.txt") mine=$(while read -r c; do git log -1 --format=%B "$c" | grep -qxF "$SIG" && echo "$c"; done < "$T/viol.txt" | grep -c .)" ;;
  NA)  # N/A 줄의 사유 측정 — 서명 커밋이 건드린 경로
    echo "SC-00=$(my | grep -cE '^(scripts/release\.sh|\.claude-plugin/marketplace\.json|[^/]+/\.claude-plugin/plugin\.json)$') DG-01=$(my | grep -c '^scripts/release.sh$') nonmd=$(my | grep -v '^\.harness/' | grep -cv '\.md$')" ;;
  *) echo "UNKNOWN $1"; return 2 ;;
  esac
}
```

```bash
#!/usr/bin/env bash
# rule-delta.sh <옛 파일> <새 파일> — 규칙별 경고 수를 두 판에서 세어 늘어난 규칙만 낸다
# 더한 줄만 보면 손대지 않은 옆 줄에 붙는 경고(MD022 · MD032 · MD024)를 놓친다 (러닝북 — Phase 7 · 8 · 9 · 11 실측)
# 린터가 안 돌면 0 이 조용히 나온다 — 돌았다는 줄(Linting: 1 file)이 없으면 멈춘다
set -u
DIR=$(cd "$(dirname "$0")" && pwd)
cnt() { local out
  out=$("$DIR/node_modules/.bin/markdownlint-cli2" --config "$DIR/cfg.markdownlint-cli2.jsonc" "$1" 2>&1)
  printf '%s\n' "$out" | grep -q '^Linting: 1 file' || return 2
  printf '%s\n' "$out" | sed -nE 's/^[^ ]*:[0-9]+(:[0-9]+)? (error|warning) (MD[0-9]+)\/.*/\3/p' | sort | uniq -c | awk '{print $2, $1}'; }
O=$(cnt "$1") || { echo "LINT_NOT_RUN $1"; exit 2; }
N=$(cnt "$2") || { echo "LINT_NOT_RUN $2"; exit 2; }
UP=$(join -a 2 -e 0 -o 0,1.2,2.2 <(printf '%s\n' "$O" | grep . | sort) <(printf '%s\n' "$N" | grep . | sort) | awk '$3 > $2 {printf "%s%s:%s>%s", (n++ ? " " : ""), $1, $2, $3}')
echo "rules_up=$(printf '%s' "$UP" | wc -w | tr -d ' ')${UP:+ $UP}"
```

```python
#!/usr/bin/env python3
# srv.py <폴더> — 127.0.0.1 빈 포트에 뜬다. 첫 줄에 포트를 찍는다.
# /fx/<이름> 은 고정 JSON(Hurl 대조용), 그 밖은 <폴더> 의 파일(뷰어 사본용). 없는 파일은 404 — favicon 요청이 여기서 난다
import json, os, sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial

FX = {
    "/fx/ok": {"data": [{"id": i} for i in range(10)], "meta": {"total": 47}},
    "/fx/bad": {"data": [{"id": i} for i in range(10)], "meta": {"total": -1}},
    "/fx/nometa": {"data": [{"id": i} for i in range(10)]},
    "/fx/sec": {"token": "sekret-p16", "marker": "plain-marker"},
}


class H(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in FX:
            b = json.dumps(FX[self.path]).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)
            return
        super().do_GET()

    def log_message(self, *a):
        pass


s = ThreadingHTTPServer(("127.0.0.1", 0), partial(H, directory=os.path.abspath(sys.argv[1])))
print(s.server_address[1], flush=True)
s.serve_forever()
```

```js
// probe.js <url> <mode: shell|chromium> <식 파일> — 뷰어를 1280×720 으로 열어 식의 값과 콘솔 error 를 한 줄 JSON 으로 낸다
// shell 은 아이콘을 부르지 않는 헤드리스 셸, chromium 은 아이콘을 부르는 새 헤드리스 — 두 판을 다 봐야 favicon 404 를 가를 수 있다
const { chromium } = require('/Users/jackson/Hub/10_Dev/claude-plugins/node_modules/playwright');
const fs = require('fs');
(async () => {
  const [url, mode, exprFile] = process.argv.slice(2);
  const b = await chromium.launch(mode === 'chromium' ? { channel: 'chromium' } : {});
  const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  const errs = [];
  p.on('console', m => { if (m.type() === 'error') errs.push({ text: m.text(), url: (m.location() || {}).url || '' }); });
  p.on('pageerror', e => errs.push({ text: 'pageerror ' + e.message, url: '' }));
  await p.goto(url, { waitUntil: 'load' });
  await p.waitForTimeout(800);
  const v = await p.evaluate(fs.readFileSync(exprFile, 'utf8'));
  console.log(JSON.stringify({ mode, v, errors: errs }));
  await b.close();
})().catch(e => { console.log('PROBE_FAIL ' + e.message.split('\n')[0]); process.exit(2); });
```

### 봉인 전 실측 — 예행 판 · 시작 커밋 판

예행 판은 이 계약 초안을 봉인해 커밋하고 다른 Phase 커밋 · `mock.py` 를 적용한 구현 커밋 · `end_sha` · notes 모의본(`notes-mock.md`) · `end_sha` 까지 올린 예행 저장소 `rh-base` 다.
시작 커밋 판은 시작 커밋에서 푼 저장소에 `end_sha` 를 시작 커밋으로 둔 개정 파일만 얹은 `rh-start` 다(편집이 없으니 새 문장 0 · 옛 글이 알려진 답이다).
예행 판 전체 출력은 bash 5.3.9 와 `/bin/bash` 3.2.57 에서 바이트 단위로 같았다(`out-base.txt` · `out-base-bash32.txt`). 측정이 끝난 뒤 스크래치 `tmp/` 에 남은 폴더 0 · 이 측정이 띄운 `srv.py` 0.
검토 반영(2026-09-25)으로 `mock.py` · `m.sh` · `notes-mock.md` 를 고친 뒤 예행 저장소 다섯(`rh-base` 와 변형 넷)을 새로 만들어 이 표 전체를 다시 쟀다.

| 조건 | 예행 판 (`m` 출력) | 시작 커밋 판 | 대조 |
| --- | --- | --- | --- |
| SK-01 | `1` 아홉 · `1 1` · `1 1` · `old=0 list_blank_after=1` | `0` 아홉 · `0 0` · `0 0` · `old=1 list_blank_after=` | 토큰 삭제 13 가운데 13 이 바뀜 · 판정 불가 불릿 뒤 빈 줄 삭제 → `list_blank_after=0` |
| SK-02 | `1 1 1` · `old=0 junit_row=1` · `1 1 1 1` · `hurl ok=0 bad=4 nometa=3 direct=4 bad_actual=1 bad_names_path=0 nometa_noquery=1 direct_none=1` | `0 0 0` · `old=1 junit_row=0` · `0 0 0 0` · 넷째 줄 같음 | 토큰 삭제 7 가운데 7 · JUnit 두 행 사이 빈 줄 → `junit_row=0` · 판 `8.1.0` 을 내는 가짜 `hurl` → 넷째 줄 `HURL_VERSION_CHANGED hurl 8.1.0 (fake)` |
| SK-03 | `1 1` · `1 1 1 1` · `old=0 0 0 0 0` | `0 0` · `0 0 0 0` · `old=1 1 1 1 1` | 토큰 삭제 6 가운데 6 · api-verify 끝에 「Hurl 로 표현 불가」 → `old=1 0 0 0 0` |
| SK-04 | `1 1 1 1` · `1 2 3 4 5` · `1 1 1` · `1 1 rows=24` | `0 0 0 0` · `1 2 3 4` · `0 0 0` · `0 0 rows=24` | 토큰 삭제 9 가운데 9 |
| SK-05 | `1` 열하나 · `rows=1 js=1 old=0 dir_api=0` · `1` | `0` 열하나 · `rows=0 js=0 old=1 dir_api=0` · `0` | 토큰 삭제 12 가운데 12 · 새 두 행 사이 빈 줄 → `rows=0` · 초안 첫 판 `--directory .api` 되살림 → `dir_api=1` |
| SK-06 | 조건 줄의 일곱 줄 그대로 | `EXPR_MISSING` | 대조 사본 넷이 측정 안에 있다(`n1` · `n2` · `n3` · 옆 파일 `fetch` 의 `n4`) · CSP `<meta>` 사본(`csp`)은 `favicon.ico` 도 0 · 식의 `[data-ep]` → `[data-id]` → 첫 줄 `shown=0` |
| SK-07 | `1` · `1 1` · `1` · `1 1 1 1` · `old=0 0` | `0` · `0 0` · `0` · `0 0 0 0` · `old=3 3` | 토큰 삭제 8 가운데 8 |
| SK-08 | `1 1 1 1` · `1 1 1` · `1 1 1 1 1` · `old=0 0 0` · `hurl plain=4 prefixed=0 cli=4 cli_actual=1 \| secret: plain=0 masked=1 marker=1 no_secret_plain=2` | `0 0 0 0` · `0 0 0` · `0 0 0 0 0` · `old=2 1 1` · 다섯째 줄 같음 | 토큰 삭제 12 가운데 12 · 시크릿 안 건 판이 측정 안의 양성 대조(`no_secret_plain=2`) · 가짜 `hurl` 8.1.0 → 다섯째 줄 `HURL_VERSION_CHANGED hurl 8.1.0 (fake)` |
| SK-09 | `1 1 1` · `1 1` · `1 1 1` · `1` · `1 1 1 1` · `old=0 0 0 0 0 0 0 0 0 0 curl_missing=0` · `hurl curl secret=0 variable=0 secret_plain=0 secret_masked=1 variable_plain=1` | `0 0 0` · `0 0` · `0 0 0` · `0` · `0 0 0 0` · `old=2 1 1 1 1 0 0 1 1 1 curl_missing=3` · 일곱째 줄 같음 | 토큰 삭제 13 가운데 13 · 초안 첫 판 글 넷 되살림 → `old=0 0 0 0 0 3 1 0 0 0 curl_missing=4` · hurl-execution 새 행을 옛 빈 칸 행으로 → 다섯째 줄 `0 1 1 1` · auth-secret-lifecycle Gotcha 머리를 옛 글로 → `1 1 1 0` · `old=0 0 0 0 0 0 0 0 1 0 curl_missing=1` · 그 파일 §6 문장을 목록 밖 말투로 → 옛 글 열 `0` · `curl_missing=1` · 변수로 건 판이 측정 안의 양성 대조(`variable_plain=1`) · 가짜 `hurl` 8.1.0 → 일곱째 줄 `HURL_VERSION_CHANGED hurl 8.1.0 (fake)` |
| SK-10 | `1 1` · `1` · `1` · `1` · `1 1 1` · `js_minus_zero=0` | `0 0` · `0` · `0` · `0` · `0 0 0` · `js_minus_zero=0` | 토큰 삭제 8 가운데 8 |
| SK-11 | `2` · `1` 열셋 · `1 1` · `removed=2 last_h2=## [2026-09-24] — 첫 카이젠 (Phase 16)` | `0` · `0` 열셋 · `0 1` · `removed=0 last_h2=## [2026-09-05] — Hurl 8.0.1 실측 대조` | 토큰 삭제 15 가운데 15 · 2026-09-04 절 표 머리 한 줄 고침 → `removed=3` |
| ER-01 | `0` · `0` · `evid_same=1` | `0` · `NOTES_MISSING` · `evid_same=1` | strictness-modes 에 가짜 URL → 첫 줄 `1` · notes 에 가짜 URL → 둘째 줄 `1` · probe-synthesis 에 있던 `https://hurl.dev/docs/entry.html` 을 api-ui 에 적음 → 첫 줄 `1` · strictness-modes 와 끝 판 근거 파일에 같은 가짜 URL → `1` · `0` · `evid_same=0` |
| ER-02 | `added=160 k02=0 names=0 kit_names=0` | `added=0 k02=0 names=0 kit_names=0` | 「이 값이 적용된다」 → `k02=1` · 「Playwright MCP 로 연다」 → `names=1 kit_names=1` |
| ER-03 | `notes_committed=1` · `1` 열 · `1` 열 · `1` 여섯 · `0` | 재지 않음 | 토큰 삭제 26 가운데 26 · 설계문서 넘김 줄을 반영 절 문장으로만 → 셋째 줄 첫 값 `0` · `Pact` 줄을 메모 절로 → 넷째 줄 넷째 값 `0` · `## 사전 · 사후 측정` 절 머리 지움 → 둘째 줄 열째 값 `0` · 변형 `unsigned-shared` · `signed-outside` · `cross-phase` 다섯째 줄 `1`, `unsigned-mine` `0` |
| AR-01 | `0` · `0 17` · `0` · `SEAL_OK` · `scope_same=1` · `1` | 재지 않음 | `unsigned-mine` ① `1` · `signed-outside` ② `1 17` · `cross-phase` ② `1 17` · 예행 작업 폴더 계약 한 글자 ③ `1` · 끝 판 계약 한 글자 ④ `SEAL_BROKEN` |
| AR-02 | `1 1 \| 1 2 \| 1 1 \| 1 1 \| 2 1` | `1 0 \| 1 0 \| 1 1 \| 1 1 \| 2 1` | api-ui `## 7. 자기 검증` → `## 7. 검증` → `0 1` 로 첫 값만 떨어짐(jsblock 은 `## 7. ` 머리로 자르므로 식은 그대로 잡힌다 — 둘째 값은 식이 있는지를 본다) |
| AR-03 | `1 1 1 1 \| 1 1 1 1 \| outside_changed=0 outside_n=11` | 같음 | enum Gotcha `>=3` → `>=2` → 첫 칸 셋째 `0` · api-init 끝에 빈 줄 → `outside_changed=1` |
| AP-01 | `version=0.1.0 0` | `version=0.1.0 0` | README 에 「버전 0.1.0」 → `1` |
| AP-03 | `00000000000000000` | 같음 | api-ui 의 ```` ```js ```` → ```` ``` ```` → 다섯째 자리 `1` |
| AP-04 | `11 11 11 11 11` | 같음 | api-ui description 한 글자 → 셋째 `01` |
| DG-02 | 열일곱 줄 모두 `rules_up=0` | — | 판정 줄 불릿 앞 빈 줄 삭제 → api-verify `rules_up=1 MD032:0>1` · 연구 기록 소제목 날짜 뗌 → `rules_up=1 MD024:0>1` · api-probe `` `Bearer ` `` → `rules_up=1 MD038:2>3` |
| DG-05 | `10 0 rc=0` · `stale_old=15 files=17 hits=0` · `  api-kit/README.md: 동기화됨` | — | `name: api-ui` → `nam:` → `10 1 rc=2` · api-verify 에 `3.1.1` → `hits=1` · README AUTO `api-ui` 행에 `BROKEN` → `  api-kit/README.md: 변경 필요` |
| DG-06 | `scope-isolation: PASS` · `doc-contracts: PASS` · `doc_checked=2 doc_mine=0` · `violators=0 mine=0` | — | 변형 `cross-phase`(구현 커밋이 `harness/skills/sprint/SKILL.md` 도 건드림) → `scope-isolation: FAIL` · `violators=1 mine=1` |
| N/A 줄 | `SC-00=0 DG-01=0 nonmd=0` (`m NA`) | — | 변형 `signed-outside` → `SC-00=1 … nonmd=1` |

- 문장 삭제 대조(`del.sh`): `toks` 로 재는 열 갈래(SK-01 ~ SK-05 · SK-07 ~ SK-11)의 토큰 103 개와 ER-03 의 notes 토큰 26 개를 끝 판 사본(열일곱 파일과 notes)에서 하나씩 지우고 그 조건을 다시 쟀다 — 129 개 모두 출력이 바뀌었고(DROP), 같은 값(SAME) · 끝 판에 없음(MISSING)은 0 이다
- 양성 · 음성 대조(`ctl.sh`, 끝 판 사본 한 군데를 바꾸고 되돌림 — 백업은 판 폴더 밖 `$T/bak/` 에 둔다)와 예행 변형 넷(`unsigned-mine` · `unsigned-shared` · `signed-outside` · `cross-phase`)이 위 표의 「대조」 칸이다.
  조건마다 기대값에서 벗어난 값이 나왔다 — 0 을 기대하는 조건은 1 이상이, 1 을 기대하는 조건은 0 이, 같아야 하는 두 판 비교는 `0` · `SEAL_BROKEN` 이 나왔다
- DRAFT 가 이 측정으로 스스로 잡아 고친 것 셋: api-probe Gotcha 의 `` `Bearer ` ``(MD038 새 경고) · 옛 글 검사가 연구 기록의 역사 인용까지 세던 것(`oldn` 에서 연구 기록 제외) · ER-01 이 로컬 주소 `http://127.0.0.1:8765/ui.html` 을 출처로 세던 것(`url` 에서 제외)
- bash 3.2 에서 AR-02 의 중괄호 든 글이 네 벌로 불어났다 — 변수로 먼저 받게 고친 뒤 두 셸 출력이 같다
- 1 회차 검토가 찾은 구멍 넷을 이 표로 다시 쟀다: SK-05 여는 방법이 `.api/` 를 통째로 올리던 것(`dir_api`) · ER-01 이 근거 파일을 끝 판에서 읽던 것(`evid_same`) · SK-09 가 가리는 곳을 다 적은 것처럼 말하던 것(`--curl` 실측 줄 · 옛 글 둘) · notes 에 api-kaizen Step 1 · 5 절이 없던 것(ER-03 열째 값)
- 2 회차 검토가 찾은 구멍 D1(auth-secret-lifecycle 세 자리가 가리는 곳을 「둘뿐」 으로 적던 것)을 BUILD 가 반영하고 예행 저장소 다섯을 새로 만들어 이 표를 다시 쟀다 —
  바뀐 값은 SK-09 다섯째 · 여섯째 줄과 ER-02 `added` 뿐이고, 나머지 ID · 변형 넷 출력은 반영 전과 같다. `/bin/bash` 3.2.57 출력도 bash 5 와 바이트 단위로 같다

## Skill

- [ ] SK-01: `api-kit/skills/api-verify/SKILL.md` 가 경로 간 불변식 판정에 양쪽 실제 값과 `판정 불가` 를 둔다 — (a) `## 6. drift 분류` 절에 문장 아홉(후처리에서 검사한다 · `.hurl` 에도 적을 수는 있다는 capture 예 · 한쪽 경로가 없으면 종료 코드 `3` 이라 판정 불가를 표현할 곳이 없다 · 판정 줄 형식 `$.meta.total=47 · len($.data)=10 → PASS` 와 `FAIL` 예 · Hurl 실패 출력은 값이 어느 경로에서 왔는지 안 찍는다 · 판정 불가 예 `$.meta.total=(없음) · len($.data)=10 → 판정 불가` · PASS 도 FAIL 도 아니고 따로 세며 그 자체로 게이트를 깨지 않는다 · 사라진 `required` 경로는 schema drift 가 잡는다 · PASS 에 합치면 경로가 사라진 회귀가 지나간다)이 각각 1 줄 이상 (b) `## 9. 리포트 생성` 의 1 번이 `PASS / FAIL / 보류 / flaky / 판정 불가` 이고 7 번이 경로 간 불변식 판정 줄 (c) `## 11. 보고와 다음 단계` 의 1 번 판정 요약과 3 번 게이트 안 깬 항목에 `판정 불가` (d) 옛 문장 「`.hurl` 로 표현되지 않은」 이 0 줄이고, 두 불릿 뒤가 빈 줄이다 [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-01` 네 줄이 `1` 아홉 · `1 1` · `1 1` · `old=0 list_blank_after=1`. 알려진 답: 시작 커밋 판은 `0` 아홉 · `0 0` · `0 0` · `old=1 list_blank_after=`.
       문장 삭제 대조: 이 갈래의 토큰 열셋을 끝 판 사본에서 하나씩 지우면 전부 값이 떨어진다(`del.sh`). 판정 불가 불릿 뒤 빈 줄을 지운 사본에서 넷째 줄 `list_blank_after=0`)
- [ ] SK-02: 실패 분류 참조 문서와 회귀 정책 문서가 판정 불가를 적고, 그 문서가 기대는 Hurl 동작이 로컬 hurl 에서 그대로 나온다 — (a) `api-kit/skills/api-verify/references/failure-taxonomy.md` `## 5. value drift 판정` 의 경로 간 불변식 행에 양쪽 값 판정 줄 · 판정 불가(따로 셈, 사라진 `required` 경로는 §4 필드 삭제) · `.hurl` 이면 종료 코드 `3` 세 조각이 각각 1, 옛 「Hurl 로 표현 불가」 0 (b) `## 8. CI artifact 매핑` 의 JUnit 표에서 `| 계약 파일 오류 (exit `2`) | `error` |` 바로 다음 행이 `| 판정 불가 (경로 간 불변식의 한쪽 경로 없음) | `skipped` + 사유(없는 경로 이름) — 게이트 미파괴 |` (c) `docs/api/verification/regression-diff-failure-policy.md` `## Gotchas` 에 판정 불가 Gotcha 네 조각 (d) 로컬 hurl 8.0.1 과 `127.0.0.1` 픽스처로 capture 형 경로 간 조건을 돌리면 정상 `0` · 값 망가짐 `4` · 경로 없음 `3`, 없는 경로를 바로 검사하면 `4` · `actual: none` 이고, 값 망가짐의 실패 출력에 `meta.total` 이 0 번 나온다 [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-02` 네 줄이 `1 1 1` · `old=0 junit_row=1` · `1 1 1 1` · `hurl ok=0 bad=4 nometa=3 direct=4 bad_actual=1 bad_names_path=0 nometa_noquery=1 direct_none=1`.
       알려진 답: 시작 커밋 판은 `0 0 0` · `old=1 junit_row=0` · `0 0 0 0` 이고 넷째 줄은 판과 상관없이 같다(도구 동작).
       음성 대조: 새 JUnit 행과 앞 행 사이에 빈 줄을 끼운 사본에서 `junit_row=0`. 넷째 줄은 문서가 적은 종료 코드 · 출력의 알려진 답이다 — hurl 이 8.0.1 이 아니면 넷째 줄이
       `HURL_VERSION_CHANGED …` 로 멈추고, 그때는 문서도 다시 봐야 한다. 멈춤 대조: 판 `8.1.0` 을 내는 가짜 `hurl` 을 PATH 앞에 둔 셸에서 넷째 줄 `HURL_VERSION_CHANGED hurl 8.1.0 (fake)`)
- [ ] SK-03: 「Hurl 로 표현 불가」 기재를 실측대로 고친다 — (a) `api-kit/skills/api-contract/SKILL.md` `## Gotchas` 에 「같은 경로 간 불변식은 `.hurl` 이 아니라 `contracts/*.yaml` 의 `pin` 으로만 기록하고 `/api-verify` 후처리에서 검사한다.」 와 capture 로 적을 수는 있지만 경로가 없으면 종료 코드 `3` 이라 판정 불가를 셀 수 없다는 문장 (b) `api-kit/skills/api-contract/references/strictness-modes.md` `### Hurl 표현 가능 여부` 의 행 「제한적 — …」 · 셋째 칸 「양쪽 값과 `판정 불가` 는 후처리에서만」 · 판정식 값에 capture 변수를 넣을 수 있다는 문장 · 그래도 후처리에 두는 이유 문장이 각각 1 (c) 옛 글 다섯(「Hurl 로 표현 불가」 · 「로 표현되지 않은」 · `| **불가** |` · 「경로 하나에 predicate 하나**이므로」 · 「경로 하나에 predicate 하나다.」)이 `api-kit/` · `docs/api/` 에서 각각 0 줄 — 연구 기록 `docs/api/research-log.md` 는 옛 기재를 역사로 인용하는 파일이라 빼고 SK-11 이 따로 잰다 [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-03` 세 줄이 `1 1` · `1 1 1 1` · `old=0 0 0 0 0`. 알려진 답: 시작 커밋 판 `0 0` · `0 0 0 0` · `old=1 1 1 1 1`.
       양성 대조: 끝 판 사본의 api-verify 끝에 「Hurl 로 표현 불가」 를 더하면 셋째 줄 첫 값 `1` — 옛 글 검사가 strictness-modes 밖 파일도 본다)
- [ ] SK-04: 새 pin 을 만드는 쪽이 판정 불가 · 죽은 pin 을 미리 막는다 — (a) `api-kit/skills/api-contract/SKILL.md` `## 11. 보고` 에 4 번 「**새로 만든 pin 의 변이 확인**」 문장 넷(사본의 값을 타입은 두고 망가뜨려 FAIL 을 보는 것 · 변이가 들어갔는지 먼저 값으로 확인 · `.hurl` pin 은 `127.0.0.1` 로컬 서버, 경로 간 불변식은 `/api-verify` §6 후처리를 사본에 · 봉인된 baseline 과 원본 스냅샷은 건드리지 않는다)이 각각 1 이고 번호가 `1 2 3 4 5` (b) `docs/api/contract/contract-extraction-modes.md` `## Gotchas` 에 「**새 pin 은 한 번 망가뜨려 본다**」 Gotcha 세 조각(PIT 출처 · 사본 변이 · 변이 확인과 baseline 불가침) (c) `api-kit/agents/api-reviewer.md` 표 3 행이 경로 간 불변식의 판정식 쪽 경로까지 양쪽을 보고, 그 까닭(한쪽이 없으면 `/api-verify` 가 매번 `판정 불가`)을 근거 칸에 적으며, 번호 붙은 표 행 수가 24(평가 표 20 · 증거 검사 표 4) 그대로다 [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-04` 네 줄이 `1 1 1 1` · `1 2 3 4 5` · `1 1 1` · `1 1 rows=24`. 알려진 답: 시작 커밋 판 `0 0 0 0` · `1 2 3 4` · `0 0 0` · `0 0 rows=24`.
       문장 삭제 대조: 토큰 아홉을 하나씩 지우면 전부 값이 떨어진다)
- [ ] SK-05: `api-kit/skills/api-ui/SKILL.md` 가 생성한 뷰어를 브라우저로 열어 확인하게 한다 — `## 7. 자기 검증 (건너뛰기 금지)` 절에 (a) 머리 「**브라우저로 열어 확인한다.**」 (b) 여는 방법 — `file://` 를 막는 조종 도구가 있다는 오류 예, `ui.html` 한 장만 든 빈 폴더를 `127.0.0.1` 웹 서버로 띄우거나 로컬 파일 허용 설정 · 어느 쪽으로 열었는지 보고, `.api/` 를 통째로 띄우지 말라는 문장(`credentials.local.json` · `reports/` · `snapshots/prod/` 가 열리고 옆 파일 `fetch` 가 성공한다), 한 장 폴더에서는 옆 파일 `fetch` 가 404 콘솔 오류로 드러나도 외부 참조는 `grep` 으로 잰다는 문장이 각각 1 줄 이상이고 `--directory .api` 는 0 줄 (c) 콘솔 error 0 · `favicon.ico` 404 한 건은 빼고 뺀 건수를 따로 (d) 첫 화면에서 식을 돌려 `ep` = `shown` · `under24` 0, `under44` 는 보고에만 (e) 확정 시안 실측 한 줄 `ep 14 · shown 14 · targets 56 · under24 0 · under44 39` (f) 도구가 없으면 `[미검증]` 에 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령) (g) 기대값 표의 누르는 자리 행이 WCAG 2.2 2.5.8 · 2.5.5 근거로 24 미만 0 개(44 권장)이고, `| 테마 |` 행 바로 다음에 항목 수 행 · 콘솔 error 행이 붙어 있고, 옛 `| 클릭 타깃 최소 크기 | `44px` |` 행 0, js 코드 블록 1 개 (h) `## 8. 열기와 보고` 에 브라우저 확인 숫자 · 못 했을 때 `[미검증]` 과 네 칸을 적는 줄 [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-05` 세 줄이 `1` 열하나 · `rows=1 js=1 old=0 dir_api=0` · `1`. 알려진 답: 시작 커밋 판 `0` 열하나 · `rows=0 js=0 old=1 dir_api=0` · `0`.
       문장 삭제 대조: 토큰 열둘을 하나씩 지우면 전부 값이 떨어진다. 새 두 행 사이에 빈 줄을 끼운 사본에서 `rows=0`. 양성 대조: 초안 첫 판 글(`--directory .api`)을 되살린 사본에서 `dir_api=1`)
- [ ] SK-06: SK-05 의 식이 확정 시안에서 실제로 맞는 값을 내고, 틀린 화면에서는 값이 떨어진다 — `$END` 판 SKILL.md §7 의 js 코드 블록을 그대로 뽑아 확정 시안 사본(sha256 앞 16 자리 `c4bd563ec8b71a95`)을 `127.0.0.1` 웹 서버로 1280×720 에서 열고 돌리면 (a) 아이콘을 부르는 크로미엄에서 `ep=14 shown=14 targets=56 under24=0 under44=39` · 콘솔 error 가운데 `favicon.ico` 밖 0 · `favicon.ico` 1 (b) 헤드리스 셸에서 같은 값 · 콘솔 error 0 · 0 (c) 트리 항목 하나를 숨긴 사본에서 `shown=13` (d) 10×10 버튼 하나를 더한 사본에서 `under24=1` (e) `console.error` 한 줄을 더한 사본에서 `favicon.ico` 밖 error 1 (f) 옆 파일 `fetch("./data.json")` 한 줄을 더한 사본에서 `favicon.ico` 밖 error 1 — SK-05 의 「한 장만 든 폴더에서는 옆 파일 `fetch` 가 404 콘솔 오류로 드러난다」 의 알려진 답 (g) 뷰어 스펙 §1 의 CSP `<meta>` 를 `<head>` 바로 뒤에 넣은 사본에서 (a) 와 같은 식 값 · 콘솔 error 0 · 0 이다 — 실제로 만들 뷰어는 그 `<meta>` 를 단다 [exact, enumerated]
      (측정: `type m >/dev/null || exit 2; type srv_start >/dev/null || exit 2;` 뒤 `m SK-06` 일곱 줄이
       `ui chromium ep=14 shown=14 targets=56 under24=0 under44=39 err_other=0 err_favicon=1` ·
       `ui shell ep=14 shown=14 targets=56 under24=0 under44=39 err_other=0 err_favicon=0` ·
       `n1 chromium ep=14 shown=13 targets=55 under24=0 under44=39 err_other=0 err_favicon=1` ·
       `n2 chromium ep=14 shown=14 targets=57 under24=1 under44=40 err_other=0 err_favicon=1` ·
       `n3 chromium ep=14 shown=14 targets=56 under24=0 under44=39 err_other=1 err_favicon=1` ·
       `n4 chromium ep=14 shown=14 targets=56 under24=0 under44=39 err_other=1 err_favicon=1` ·
       `csp chromium ep=14 shown=14 targets=56 under24=0 under44=39 err_other=0 err_favicon=0`.
       알려진 답: 시작 커밋 판 SKILL.md 에는 js 블록이 없어 `EXPR_MISSING`. 셋째 ~ 여섯째 줄이 식의 음성 대조다 — 사본 편집이 안 걸리면 `NEG_EDIT_FAIL` 로 멈춘다.
       식 음성 대조: 끝 판 사본 식의 `[data-ep]` 를 `[data-id]` 로 바꾸면 첫 줄 `shown=0`)
- [ ] SK-07: 뷰어 스펙과 뷰어 계약 문서가 누르는 자리 기준 · 항목 표식을 맞춘다 — (a) `api-kit/skills/api-ui/references/viewer-spec.md` `## 1. 하드 제약` 의 누르는 자리 행(24×24 CSS px, 44 권장, 위반 시 칸은 「24 미만이면 간격 예외를 따지기 전에 고친다 — 요소 상자만 재므로 WCAG 2.2 2.5.8 보다 엄하다」, 확정 시안 실측 44 미만 39/56 · 24 미만 0, `SKILL.md` §7 `under24` 로 잰다) (b) `### 3.2 사이드바 — 엔드포인트 트리` 에 `data-ep="<엔드포인트 id>"` 문장과 첫 화면 그룹 모두 펼침 문장 (c) `docs/api/verification/static-evidence-viewer-contract.md` `## 수치 기준` 의 누르는 자리 행(WCAG 2.2 2.5.8 · 2.5.5, 확정 시안 1280×720 실측) (d) 같은 문서 `## Gotchas` 에 브라우저 확인 Gotcha 네 조각(`file://` 차단 → 웹 서버 · `.api/` 를 통째로 띄우면 `fetch` 가 성공하고 아이디 · 비밀번호 파일이 열리니 한 장 폴더 · `favicon.ico` 404 · 헤드리스 셸은 아이콘을 안 부른다) (e) 옛 글 `44px` · 「클릭 타깃」 이 `api-kit/` · `docs/api/` 에서(연구 기록 제외 — SK-03 과 같은 까닭) 각각 0 줄 [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-07` 다섯 줄이 `1` · `1 1` · `1` · `1 1 1 1` · `old=0 0`. 알려진 답: 시작 커밋 판 `0` · `0 0` · `0` · `0 0 0 0` · `old=3 3`.
       문장 삭제 대조: 토큰 여덟을 하나씩 지우면 전부 값이 떨어진다)
- [ ] SK-08: 환경변수로 넣는 변수 기재 네 자리를 Hurl 8.0.0 동작으로 고치고, 그 동작이 로컬 hurl 에서 그대로 나온다 — (a) `api-kit/skills/api-probe/references/hurl-execution.md` 에 「**환경변수로 변수를 넣으려면 `HURL_VARIABLE_` 접두가 필요하다**」 Gotcha 네 조각 (b) `docs/api/execution/auth-secret-lifecycle.md` `## Gotchas` 에 같은 머리와 두 조각 (c) `docs/api/execution/probe-synthesis-hurl-semantics.md` 에 §6 문장 셋 · 출처 줄의 CHANGELOG · 수치 표 행 「환경변수로 들어가는 변수」 (d) 옛 글 셋(「옵션에만 붙고 변수에는 안 붙는다」 · 「이 규칙은 **옵션에만** 적용된다」 · 「변수는 `HURL_*` 로 안 들어온다」)이 `api-kit/` · `docs/api/` 에서(연구 기록 제외) 각각 0 줄 (e) 로컬 hurl 에서 `HURL_who` 는 변수를 못 채워 `4`, `HURL_VARIABLE_who` 는 `0`, 둘을 겹치고 `--variable who=from-cli` 를 주면 `4` 와 `actual: string <from-cli>`, `HURL_SECRET_tok` 은 본문이 실리는 `--error-format long` stderr 에서 값을 가리고(평문 0 · `"token": "***"` 1 · 표식 1) 시크릿을 안 건 판에서는 본문 줄과 실제값 줄 둘에 평문이 나온다 [exact, enumerated]
      (측정: `type m >/dev/null || exit 2; type srv_start >/dev/null || exit 2;` 뒤 `m SK-08` 다섯 줄이 `1 1 1 1` · `1 1 1` · `1 1 1 1 1` · `old=0 0 0` ·
       `hurl plain=4 prefixed=0 cli=4 cli_actual=1 | secret: plain=0 masked=1 marker=1 no_secret_plain=2`. 알려진 답: 시작 커밋 판 `0 0 0 0` · `0 0 0` · `0 0 0 0 0` · `old=2 1 1` 이고 다섯째 줄은 판과 상관없이 같다.
       다섯째 줄의 `no_secret_plain=2` 가 마스킹 측정의 양성 대조이고 `marker=1` 이 그 채널이 본문을 담는다는 확인이다. hurl 이 8.0.1 이 아니면 다섯째 줄이
       `HURL_VERSION_CHANGED …` 로 멈춘다. 멈춤 대조: 판 `8.1.0` 을 내는 가짜 `hurl` 을 PATH 앞에 둔 셸에서 다섯째 줄 `HURL_VERSION_CHANGED hurl 8.1.0 (fake)`)
- [ ] SK-09: `--secret` 이 가린다고 확인된 곳 기재를 2026-09-05 실측(`docs/api/research-log.md`)과 근거 파일 L5(`--curl` 파일)에 맞추고, `--curl` 파일 마스킹이 로컬 hurl 에서 그대로 나온다 — (a) `api-kit/skills/api-verify/SKILL.md` `## Gotchas` 세 조각(가린다고 확인된 곳은 stderr 로그 · `report.json` · `--curl` 파일 · `--output` · `--json` · `store/*_response.json` 은 안 가린다 · `--very-verbose` 는 등록한 값만 `***`) (b) `api-kit/skills/api-ui/SKILL.md` `## Gotchas` 두 조각 (c) `api-kit/skills/api-probe/SKILL.md` `## Gotchas` 세 조각(등록 안 한 변형 · 개인정보는 CI 로그에 남는다 포함) (d) `api-kit/README.md` 한 줄(`--curl` 파일 포함) (e) `api-kit/skills/api-probe/references/hurl-execution.md` §6 표에 `--curl <file>` 의 헤더 값이 가려지는 곳 칸에 있는 행, 그리고 `docs/api/execution/auth-secret-lifecycle.md` 의 §6 문장 · 수치 표 「`--secret` 마스킹되는 채널」 행 · Gotcha 머리 세 자리에 `--curl <file>` (f) 옛 글 열(「stderr 로그와 리포트만」 · 「stderr 로그와 리포트뿐」 · 「stderr 와 리포트만」 · 「body 를 stderr 에 그대로 뿌린다」 · 「뱉으므로 CI 로그에 그대로 남는다」, 가리는 곳을 다 적은 것처럼 말하는 두 글 「`report.json` 뿐」 · 「`report.json` 만 가리」, auth-secret-lifecycle 의 옛 글 셋 「`report.json`(`curl_cmd`·요청 헤더)뿐이다」 · 「`report.json` 둘뿐」 · 「`--secret` 마스킹되는 채널」 옛 행)이 `api-kit/` · `docs/api/` 에서(연구 기록 제외) 각각 0 줄이고, `report.json` 과 가림 낱말(`--secret` · 가려지는 · 가리는 · 가린다 · 마스킹되는)이 같이 든 줄 가운데 `--curl` 이 없는 줄이 0 이다 (g) 로컬 hurl 8.0.1 과 `127.0.0.1` 픽스처로 `Authorization: Bearer {{tok}}` 요청을 `--secret` 으로 걸면 `--curl` 파일에 평문 0 · `Bearer ***` 1 이고, 같은 값을 `--variable` 로 걸면 평문 1 이다 — 결론(킷 자체 scrubber 를 거친 것만 저장 · 렌더)은 그대로다 [exact, enumerated]
      (측정: `type m >/dev/null || exit 2; type srv_start >/dev/null || exit 2;` 뒤 `m SK-09` 일곱 줄이 `1 1 1` · `1 1` · `1 1 1` · `1` · `1 1 1 1` · `old=0 0 0 0 0 0 0 0 0 0 curl_missing=0` ·
       `hurl curl secret=0 variable=0 secret_plain=0 secret_masked=1 variable_plain=1`. 알려진 답: 시작 커밋 판 `0 0 0` · `0 0` · `0 0 0` · `0` · `0 0 0 0` · `old=2 1 1 1 1 0 0 1 1 1 curl_missing=3` 이고 일곱째 줄은 판과 상관없이 같다(도구 동작).
       문장 삭제 대조: 토큰 열셋을 하나씩 지우면 전부 값이 떨어진다. 양성 대조: 초안 첫 판 글 넷(「… `report.json` 뿐」 · 「… `report.json` 만 가리고」)을 되살린 사본에서 여섯째 줄 `old=0 0 0 0 0 3 1 0 0 0 curl_missing=4`,
       hurl-execution §6 새 행을 옛 빈 칸 행으로 되돌린 사본에서 다섯째 줄 `0 1 1 1`, auth-secret-lifecycle Gotcha 머리를 옛 글로 되돌린 사본에서 다섯째 줄 `1 1 1 0` · 여섯째 줄 `old=0 0 0 0 0 0 0 0 1 0 curl_missing=1`,
       그 파일 §6 문장을 목록에 없는 말투(「… `report.json`(…)에 한정된다.」)로 바꾼 사본에서 여섯째 줄의 옛 글 열 값은 모두 `0` 인데 `curl_missing=1`. 일곱째 줄의 `variable_plain=1` 이 마스킹 측정의 양성 대조다 — 그 파일에 헤더가 실린다는 확인이다.
       hurl 이 8.0.1 이 아니면 일곱째 줄이 `HURL_VERSION_CHANGED …` 로 멈춘다. 멈춤 대조: 판 `8.1.0` 을 내는 가짜 `hurl` 을 PATH 앞에 둔 셸에서 일곱째 줄 `HURL_VERSION_CHANGED hurl 8.1.0 (fake)`)
- [ ] SK-10: I-JSON 게이트 목록 다섯 자리에 `-0` 이 있고 문서 근거가 붙는다 — (a) `api-kit/skills/api-contract/SKILL.md` `## Gotchas` 에 `lone surrogate·`-0`·안전 정수 범위` 와 「`-0` 은 JCS 가 `0` 으로 적어 부호가 사라진다(RFC 8785 정정 7920).」 (b) 같은 파일 `## 2. I-JSON 게이트` 목록에 `-0 (음의 영)` 줄 (c) `api-kit/skills/api-probe/SKILL.md` `## 7. 스크러빙 → 정규화 → 저장` 2 번 줄 끝 `· -0` (d) `api-kit/skills/api-verify/SKILL.md` `## 5. 응답 정규화` 의 게이트 실패 목록 (e) `docs/api/contract/snapshot-sealing-canonicalization.md` `### 3. 정규화 전 I-JSON 게이트` 에 목록 · 정정 7920 문장 · 출처 줄의 정정 목록 URL (f) node 에서 `JSON.stringify(-0)` 이 `0` 이다 — JCS 가 쓰는 ECMAScript 직렬화에서 부호가 사라진다는 문장의 알려진 답 [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-10` 여섯 줄이 `1 1` · `1` · `1` · `1` · `1 1 1` · `js_minus_zero=0`. 알려진 답: 시작 커밋 판 `0 0` · `0` · `0` · `0` · `0 0 0` · `js_minus_zero=0`.
       문장 삭제 대조: 토큰 여덟을 하나씩 지우면 전부 값이 떨어진다)
- [ ] SK-11: `docs/api/research-log.md` 가 이번 실측을 남긴다 — (a) 머리 설정이 `version: 0.3.0` · `last_updated: 2026-09-24` (b) 마지막 `## ` 제목이 `## [2026-09-24] — 첫 카이젠 (Phase 16)` 이고 그 절에 날짜 붙은 소제목 다섯 · 경로 간 조건 표의 종료 코드 `3` 행 · 브라우저 표의 24 미만 `0` 과 44 미만 `39` 행 · 어긋난 것 표의 환경변수 행 · 정한 것 두 줄(판정 불가 · 누르는 자리 통과선) · 이월 두 줄(OpenAPI 3.2 · `/api-contract` §9 예시)이 각각 1 줄 이상 (c) `## [2026-09-05] — Hurl 8.0.1 실측 대조` 절에 「> **[2026-09-24 정정]** 이 단서는 `HURL_who` 만 재서 나온 것이다.」 가 있고 옛 문장 「`HURL_who=from-env` 를 걸어도 … 실패한다.」 도 그대로 있다 (d) 편집 전 판에서 지운 줄이 머리 설정 두 줄뿐이다 — 옛 절은 고치지 않고 표시만 더한다 [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-11` 네 줄이 `2` · `1` 열셋 · `1 1` · `removed=2 last_h2=## [2026-09-24] — 첫 카이젠 (Phase 16)`.
       알려진 답: 시작 커밋 판 `0` · `0` 열셋 · `0 1` · `removed=0 last_h2=## [2026-09-05] — Hurl 8.0.1 실측 대조`.
       음성 대조: 2026-09-04 절의 한 줄을 고친 사본에서 `removed=3`)

## Script

- [ ] SC-00: N/A (Script 카테고리는 `release.sh` 연동 · 버전 올림 · `marketplace.json` 갱신이다. 이 Phase 는 그 파일을 건드리지 않는다 — 공유 파일은 Final 몫. 측정: `type m >/dev/null || exit 2;` 뒤 `m NA` 의 `SC-00=0`. 양성 대조: 예행 변형 `signed-outside` 에서 `SC-00=1`)

## Error

- [ ] ER-01: 열일곱 파일에 새로 생긴 URL 과 `.harness/.meta/kaizen-0924/phase16-notes.md` 의 URL 이 전부 **시작 커밋 판**의 외부 근거 파일 `.harness/.meta/evidence/phase16.md` 에 있고, 끝 판 근거 파일이 시작 커밋 판과 같다 — 근거 파일은 `.harness/` 안이라 이 Phase 가 고칠 수 있으므로 끝 판에서 읽지 않는다. 파일마다 편집 전 판과 비교한다 (러닝북 — 근거 파일에 없는 URL 을 지어내지 않는다 · notes 킷 로그의 출처 URL 은 근거 파일에서만) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-01` 세 줄이 `0` · `0` · `evid_same=1`. notes 가 `$END` 판에 없으면 둘째 줄이 `NOTES_MISSING` 이라 FAIL 이다.
       양성 대조: 끝 판 strictness-modes 끝에 `https://example.invalid/x` 를 더한 사본에서 첫 줄 `1`, notes 끝에 더한 사본에서 둘째 줄 `1`, 다른 파일에 이미 있던 `https://hurl.dev/docs/entry.html` 을 api-ui SKILL.md 로 옮겨 적은 사본에서 첫 줄 `1` — 파일마다 비교해서 잡는다.
       strictness-modes 사본과 끝 판 근거 파일 사본에 같은 가짜 URL 을 넣은 사본에서 `1` · `0` · `evid_same=0` — 근거 파일을 같이 고쳐 통과시키는 길을 막는다)
- [ ] ER-02: 열일곱 파일에 더한 줄에 번역투 6 종(`tone-kit/references/locale-korean.md` §2 치환표의 grep 열)이 0 건, 특정 앱 이름 · 특정 화면 도구 서버 이름(`fit-?pal` · `fit_pal` · `flutter[-_]playwright` · `playwright[ _-]?mcp` · `chrome-devtools-mcp`, 대소문자 무시)이 0 건이고, `$END` 판 `api-kit/` · `docs/api/` 전체에서 같은 이름이 0 줄이다 (러닝북 말투 · 문서 규칙 — 킷 파일에 특정 앱 이름 · MCP 서버 이름을 넣지 마라) [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-02` 가 `added=N k02=0 names=0 kit_names=0` 이고 N 이 1 이상.
       양성 대조: api-ui SKILL.md 끝에 「이 값이 적용된다」 를 더한 사본에서 `k02=1`, 「Playwright MCP 로 연다」 를 더한 사본에서 `names=1 kit_names=1`)
- [ ] ER-03: 이 Phase 범위 밖 반대편을 명시적 미완으로 넘기고 건드리지 않는다 — `.harness/.meta/kaizen-0924/phase16-notes.md` 가 `$END` 에 커밋돼 있고 (a) 처리 배정표 키 `other-kits:P7` · `other-kits:P8` 과 러닝북이 적게 한 절 머리 일곱(`## 바꾼 파일` · `## 반영한 처리 배정표 키` · `## 미반영 키와 사유` · `## 넘기는 것` · `## changelog 한 단락` · `## 킷 로그 한 단락` · `## 다음 사이클 메모`), 그리고 api-kaizen Step 1 · 5 의 표를 담는 `## 사전 · 사후 측정` 이 각각 1 줄 이상 (b) `## 넘기는 것` 절 안에 넘김 열 — `docs/superpowers/specs/2026-09-02-api-kit-design.md` (`:249` 표현되지 않는다 — Final) · `.claude/skills/kaizen-orchestrator/SKILL.md` (`:567` 같은 말 — Final) · 문서 사이트 페이지 여섯 `docs/api-kit/probe-synthesis-hurl-semantics.html` · `docs/api-kit/auth-secret-lifecycle.html` · `docs/api-kit/snapshot-sealing-canonicalization.html` · `docs/api-kit/contract-extraction-modes.html` · `docs/api-kit/regression-diff-failure-policy.html` · `docs/api-kit/static-evidence-viewer-contract.html` (Final F2) · `scripts/detect-docs-drift.py` (`docs/api` 매핑 없음) · `plugin.json` (Final — 버전) 이 각각 1 줄 이상 (c) `## 미반영 키와 사유` 절 안에 `OpenAPI 3.2` · `jsonpath` · `대비` · `Pact` · `8.1.0` · `api-reviewer` 가 각각 1 줄 이상이고, (d) 구간 안에서 공유 파일 · 다른 Phase 파일을 건드린 커밋 가운데 다른 Phase 서명이 없는 커밋이 0 개다 [exact, enumerated]
      (Given: BUILD 가 notes 를 커밋하고 개정 파일에 그 sha 로 `end_sha:` 를 덧붙인 뒤 · When: `type m >/dev/null || exit 2; type not_other >/dev/null || exit 2;` 뒤 `m ER-03` · Then: 다섯 줄이 `notes_committed=1` · 열 값 모두 `1` 이상 · 열 값 모두 `1` 이상 · 여섯 값 모두 `1` 이상 · `0`. 다섯째 줄이 0 이 아니면 FAIL 이다.
       (d) 의 경로는 `m.sh` `ER-03)` 갈래의 `not_other` 인자 열여섯이다 — 서명 줄 목록이 아니라 경로로 직접 세므로 서명을 빠뜨린 커밋도 보인다. 다른 Phase 서명이 달린 커밋은 그 Phase 몫이라 뺀다.
       음성 대조: 넘김 표의 설계문서 줄을 지우고 같은 경로를 `## 반영한 처리 배정표 키` 절 문장에만 남긴 사본에서 셋째 줄 첫 값 `0` · 미반영 절의 `Pact` 줄을 `## 다음 사이클 메모` 절로만 옮긴 사본에서 넷째 줄 넷째 값 `0` · `## 사전 · 사후 측정` 절 머리를 지운 사본에서 둘째 줄 열째 값 `0`.
       양성 대조: 변형 `unsigned-shared`(서명 없이 루트 README) · `signed-outside`(서명하고 plugin.json) · `cross-phase`(서명하고 harness 파일) 에서 다섯째 줄 `1`. `unsigned-mine` 은 이 Phase 폴더라 `0` 이고 AR-01 ① 이 잡는다)

## Architecture

- [ ] AR-01: 이 Phase 의 변경이 허용 경로 안에 머물고, 범위 선언 블록이 그 경로와 같으며, 이 계약이 봉인돼 있다 [exact, enumerated]
      (Given: BUILD 가 개정 파일에 `end_sha:` 를 적은 뒤 · 이 Phase 커밋 메시지마다 서명 줄 `Kaizen-Phase: kaizen-0924-p16-api-kit` · When: `type m >/dev/null || exit 2; type unsigned_on >/dev/null || exit 2; type verify_seal >/dev/null || exit 2;` 뒤 `m AR-01` · Then: 여섯 줄이 —
       ① `0` — `api-kit/` · `docs/api/` 를 건드린 구간 안 커밋이 전부 서명했다(이 구간에 두 폴더를 고칠 수 있는 Phase 는 16 하나다)
       ② `0 17` — 서명 커밋이 건드린 `.harness/` 밖 경로 가운데 열일곱 파일 밖이 0 개, 열일곱 파일이 전부 있다
       ③ `0` — `harness/references/contract-schema.md` §`.harness/` 범위 조건 의 권장 형태로 `.harness/` 의 계약 전부에 `verify_seal` 을 돌려 이 Phase 몫 `SEAL_BROKEN` 이 0 개
       ④ `SEAL_OK` — `$END` 판의 이 계약이 봉인돼 있다(`SEAL_ABSENT` 는 봉인을 건너뛴 것이라 FAIL)
       ⑤ `scope_same=1` — `## 범위 경계` 절 `# sprint-scope` 블록의 `.harness/` 밖 줄이 `FILES` 열일곱 줄과 같다 ⑥ `1` — 그 블록에 `.harness/` 줄이 하나 있다.
       봉인 전 실측: 예행 판 `0` · `0 17` · `0` · `SEAL_OK` · `scope_same=1` · `1`. 양성 대조: 변형 `unsigned-mine` ① `1` · 변형 `signed-outside` ② `1 17` · 변형 `cross-phase` ② `1 17` ·
       예행 작업 폴더 계약의 조건 줄 한 글자를 바꾼 사본 ③ `1` · 끝 판 계약의 조건 줄 한 글자를 바꾼 사본 ④ `SEAL_BROKEN`)
- [ ] AR-02: 새 글이 가리키는 자리가 실제로 있다 — (a) 뷰어 스펙의 「`SKILL.md` §7 `under24`」 → api-ui `## 7. 자기 검증` 제목 1 과 §7 js 블록의 `under24` 1 (b) api-contract §11 과 실패 분류의 「`/api-verify` §6」 → api-verify `## 6. drift 분류` 1 과 그 절의 `판정 불가` 줄 1 이상 (c) 실패 분류 §5 의 「§4 필드 삭제」 → `## 4. schema drift 판정` 1 과 그 절의 `| 필드 삭제 |` 1 (d) api-verify Gotcha 의 「`docs/api/research-log.md` 2026-09-05」 → 그 절 제목 1, 연구 기록의 「근거 파일 L7」 → 시작 커밋 판 근거 파일 `| L7 |` 1 — 근거 파일은 이 Phase 가 고칠 수 있어 ER-01 처럼 시작 커밋 판에서 읽는다 (e) 뷰어 스펙의 `data-ep` · `openGroups` 문장 → 확정 시안에 `data-ep="` 줄 1 이상 · `openGroups:{ auth:true, orders:true, products:true, users:true }` 1 [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m AR-02` 가 `1 1 | 1 N | 1 1 | 1 1 | K 1` 이고 N · K 가 1 이상. 알려진 답: 시작 커밋 판 `1 0 | 1 0 | 1 1 | 1 1 | K 1`(js 블록 · 판정 불가가 아직 없다).
       양성 대조: 끝 판 사본에서 api-ui `## 7. 자기 검증` 을 `## 7. 검증` 으로 바꾸면 첫 값 `0` — 둘째 값은 식 안의 `under24` 를 보는 값이라 `1` 그대로다)
- [ ] AR-03: 손대지 않을 곳이 그대로다 — (a) 오케스트레이터가 완화하지 말라고 한 확정 결정 줄 여덟이 시작 커밋 판과 글자 그대로 같다: api-contract Gotcha 셋(`pin` 정의 · `exact` 본문만 · enum 1 샘플)과 §4 「순서를 지킨다. **redaction → 마스크 적용 → JCS 직렬화.**」, api-verify Gotcha 둘(종료 코드 3 과 4 · prod 게이트)과 §4 종료 코드 표 `3` · `4` 행 (b) `api-kit/` · `docs/api/` 에서 열일곱 파일 밖 파일이 시작 커밋 판과 전부 같다 [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m AR-03` 이 `1 1 1 1 | 1 1 1 1 | outside_changed=0 outside_n=N` 이고 N 이 1 이상.
       양성 대조: 끝 판 사본에서 api-contract enum Gotcha 의 `>=3` 을 `>=2` 로 바꾸면 첫 칸 셋째 값 `0` · `api-kit/skills/api-init/SKILL.md` 끝에 빈 줄을 더하면 `outside_changed=1`)

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다. 이번 변경에 적용: 열일곱 파일에 더한 줄에 api-kit `plugin.json` 의 `version` 값(`$END` 판에서 읽는다)이 0 건이다 — 이 Phase 는 킷 버전을 적지 않고 Final 이 올린다. 문서 머리 설정의 `0.1.1` · `0.2.1` · `0.3.0` 은 문서 자체의 판 번호라 이 값과 다르다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m AP-01` 이 `version=0.1.0 0`. 양성 대조: README 끝에 「버전 0.1.0」 을 더한 사본에서 둘째 값 `1`)
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```` ```text, ```bash, ```yaml ```` 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 이번 변경에 적용: V6 가 읽는 스킬 · README 는 DG-05 의 V6 줄이 보고, V6 가 안 읽는 참조 문서 · 에이전트 · `docs/api/` 까지 열일곱 파일 모두 같은 여닫기 방식으로 센 언어 힌트 없는 여는 펜스가 0 이다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m AP-03` 이 `0` 열일곱 자리(`00000000000000000`). 양성 대조: api-ui SKILL.md 새 ```` ```js ```` 를 ```` ``` ```` 로 바꾼 사본에서 다섯째 자리 `1`)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL. 이번 변경에 적용: 고치는 스킬 넷(api-verify · api-contract · api-ui · api-probe)과 api-reviewer 의 첫 frontmatter 블록이 편집 전과 글자 그대로 같고 `name: ` 줄이 하나씩이다 — 그래서 README AUTO 구간과 트리거 설명이 읽는 값도 바뀌지 않는다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m AP-04` 가 `11 11 11 11 11`. 음성 대조: api-ui SKILL.md `description` 한 글자를 바꾼 사본에서 셋째 값 `01`)

## Reusability

- [ ] RE-01: N/A (산출물에 재사용 단위 코드가 없다 — 열일곱 파일이 전부 마크다운 문서다. 스킬 안 js 식은 문서 속 예시로, 실행 검사는 SK-06 이 한다. 측정: `type m >/dev/null || exit 2;` 뒤 `m NA` 의 `nonmd=0`)
- [ ] RE-02: N/A (새로 만든 컴포넌트 · 함수 · 모듈이 없다 — RE-01 과 같은 측정 `nonmd=0`. 기존 채널 표를 새로 만들지 않고 2026-09-05 실측 표(`docs/api/research-log.md` · `hurl-execution.md` §6)에 문장을 맞췄고, §6 표에는 근거 파일 L5 의 `--curl` 행 하나만 채웠다 — SK-09)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `type m >/dev/null || exit 2;` 뒤 `m NA` 의 `DG-01=0`)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (`diagnostics.ide_exclude` 값 `[]`) — 이번 변경에 적용: 편집기 마크다운 확장과 같은 조건(markdownlint-cli2 0.23.2 · MD013 끔)으로 열일곱 파일 **각각**에서 규칙별 경고 수를 편집 전 판과 비교해 늘어난 규칙이 0 개다. 더한 줄만 보지 않는다 — MD022 · MD032 · MD024 는 더한 줄 옆의 손대지 않은 줄에 붙는다(러닝북 측정 구멍 목록). 편집 전부터 있던 경고는 같은 수로 남아도 된다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m DG-02` 열일곱 줄이 모두 `rules_up=0` 으로 끝나고 `LINT_NOT_RUN` 줄 0.
       양성 대조: api-verify §6 판정 줄 불릿 앞 빈 줄을 지운 사본에서 그 줄 `rules_up=1 MD032:0>1`(불릿 뒤 빈 줄을 지우면 다음 문단이 불릿에 이어 붙을 뿐 경고가 안 난다 — 그 자리는 SK-01 `list_blank_after` 가 잡는다),
       연구 기록 `### 이월 — 다음 사이클 후보 (2026-09-24)` 를 `### 다음 사이클 후보` 로 바꾼 사본에서 그 줄 `rules_up=1 MD024:0>1`,
       api-probe Gotcha 에 `` `Bearer ` `` 를 되살린 사본에서 `rules_up=1 MD038:2>3`(DRAFT 첫 판이 실제로 낸 경고). 린터를 못 찾으면 `LINT_NOT_RUN` · 종료 코드 2)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: DG-01 과 같은 `m NA` 의 `DG-01=0`. 실제 실행 검사는 SK-02 · SK-06 · SK-08 · SK-09)
- [ ] DG-04: N/A (산출물에 구동할 앱 · 서버가 없다 — 변경 파일이 전부 문서다(`m NA` 의 `nonmd=0`). 스킬이 시키는 브라우저 식과 문서가 적은 hurl 동작은 SK-06 · SK-02 · SK-08 · SK-09 가 실제로 돌린다)
- [ ] DG-05: 저장소 검사가 이 킷을 문제로 가리키지 않는다 — `$END` 판을 git 저장소로 만든 사본에서 (a) `scripts/validate-plugin.py api-kit` 출력에 `V1` ~ `V10` 열 줄이 있고 `— OK` · `— SKIP (no templates/)` 로 끝나지 않는 줄이 0 이며 종료 코드 0 (b) `.harness/stale-values.yaml` 의 `old` 값 전부를 열일곱 파일에서 직접 센 수가 0 이다 — `scripts/check-stale-values.py` 는 `SOURCE_DIRS` 에 `api-kit/` 이 없어 근거로 쓰지 않는다 (c) `scripts/sync-docs.py --check-only api-kit` 가 `api-kit/README.md: 동기화됨` 을 낸다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m DG-05` 세 줄이 `10 0 rc=0` · `stale_old=N files=17 hits=0` · `  api-kit/README.md: 동기화됨` 이고 N 이 1 이상. N 을 잠그지 않는 까닭: 등록부는 공유 파일이라 `$END` 전에 다른 주체가 값을 더할 수 있다.
       음성 대조: api-ui SKILL.md 의 `name: api-ui` 를 `nam:` 으로 깬 사본에서 첫 줄 `10 1 rc=2`. 양성 대조: api-verify 끝에 등록부 옛 값 `3.1.1` 을 더한 사본에서 `hits=1` ·
       README AUTO 표의 `api-ui` 행 설명 앞에 `BROKEN` 을 넣은 사본에서 셋째 줄이 `동기화됨` 이 아니다)
- [ ] DG-06: `python3 scripts/validate-post-kaizen.py --since 3a348d601cedd49e0689ca194b57baf8f5029454` 출력의 `scope-isolation` · `doc-contracts` 줄이 `FAIL` · `ERROR` 가 아니다. `docs-site-regen` 은 Final F2 몫이라 판정에서 뺀다. 다른 Phase 커밋 때문에 `scope-isolation` 이 FAIL 이면 `--verbose` 위반 커밋 목록을 1 개 이상 읽었고 그 가운데 서명 줄 커밋이 0 개일 때, `doc-contracts` 가 FAIL · ERROR 이면 `validate-doc-contracts.py -v` 가 검사한 경로를 1 개 이상 읽었고 그 가운데 이 Phase 서명 커밋이 건드린 경로가 0 개일 때 이 조건은 PASS 다 — 둘 다 근거에 다른 Phase 몫이라고 적는다 [exact]
      (Given: 작업 폴더에서 `$END` 이후 커밋이 있어도 된다 — 검사는 `HEAD` 까지 보지만 판정은 이 Phase 서명 커밋만 센다 · When: `type m >/dev/null || exit 2;` 뒤 `m DG-06` · Then: 네 줄이 `scope-isolation: PASS` · `doc-contracts: PASS` · `doc_checked=N doc_mine=0` · `violators=V mine=0` 이고 N 이 1 이상. 위 가르기로 PASS 를 줄 때만 첫 두 줄에 `FAIL` 이 있어도 되며, scope-isolation 이 `FAIL` 이면 V 가 1 이상이어야 한다(목록을 못 읽으면 mine 이 조용히 0 이 되므로).
       봉인 전 실측: 예행 판 `scope-isolation: PASS` · `doc-contracts: PASS` · `doc_checked=2 doc_mine=0` · `violators=0 mine=0`. 양성 대조: 변형 `cross-phase` 에서 `scope-isolation: FAIL` · `violators=1 mine=1`)
