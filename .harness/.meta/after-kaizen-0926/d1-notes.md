# d1 원본이 바뀐 문서 페이지 다시 맞추기 — 작업 기록

- 가지 `chore/ak-docs` · 시작점 `39ddc12` · 원본 차이 구간 `f81568d..39ddc12`
- 계약 `.harness/sprint-contract-after-0924-docs-regen.md` (28 조건, 봉인 `sha256:5f2a4aa254cb4e0c`, 봉인 커밋 `e84dc35`)
- 계약 피드백 `/Users/jackson/.harness/feedback/contract/1a3bcba6-2026-09-26T155848-bda55d45-50511.yaml` (`verify-feedback.sh` PASS)
- QA 판정: APPROVE (Iteration 1, 28 조건 — 리포트 `.harness/sprint-feedback-after-0924-docs-regen.md`, 커밋 `9f78f0f`, 계약 `status` 는 `done`). 독립 검토는 BLOCKING 0 이고, 판정을 바꾸지 않는 네 건은 아래 「다음 사이클 메모」 로 옮겼다

## 봉인 전 교차 진단 반영

qa-evaluator 교차 진단이 계약의 측정 도우미를 떼어 시작 판에서 26 조건을 돌려 계약에 적은 시작 값과 모두 같게 냈다. 지적은 봉인 전에 계약 원문에 넣었다.

| 지적 | 반영 |
| --- | --- |
| 바뀐 줄 대조가 새 글의 자리를 안 본다 (SK 여덟 조건) | 의도한 느슨함이라고 범위 경계에 적고, 자리를 보는 조건 넷(SK-02 · SK-07 · SK-08 · SK-11)을 밝혔다 |
| SK-09 인용 형식이 실제 출력과 다르다 | `lines=21 in_old=19 in_new=21 lost=0` 꼴로 맞췄다 |
| SK-10 의 출처 이름표 · 함정 줄 재량에 기준이 없다 | 페이지 전체를 세는 옛 주장 셋 0 이 그 두 줄에도 걸린다고 적었다 |
| AR-02 가 낱말만 있으면 통과한다 | 토큰마다 한글 15 자 이상인 줄을 요구하게 도우미를 바꿨다 (설명 줄 notes 1 열, 토큰만 늘어놓은 notes 0 열) |
| AP-03 의 셈과 V6 가 같다는 증거가 없다 | 입력 열 가지로 나란히 재 열 가지 모두 같았다 |
| DG-02 설치 실패 · DG-05 도구 변경 때 판정이 없다 | `md=ENV_FAIL` · `tool_same=0` · `ci_summary=absent` 를 `[미검증:ENV]` 로 본다고 적었다 |
| 기능 조건 19 개의 근거 · 빠진 태그 11 개 | ID 목록을 배경에 적고 `[exact]` 를 채웠다 |

## 한 일

페이지마다 한 커밋이다. 원본 파일 · 킷 폴더 · 공통 스타일은 건드리지 않았다.

| 커밋 | 쪽 | 내용 |
| --- | --- | --- |
| `bac16b0` | `docs/design-kit/design-concept.html` | 나쁜 예 코드 앞 공백 세 칸을 뺐다 (c3b-notes 2 번) |
| `f7878c6` | `docs/flutter-toolkit/flutter-ai-rules.html` | Makefile 카드를 타겟별 확인 규칙으로 바꿨다 (원본 115 줄) |
| `b29f482` | `docs/flutter-toolkit/project-detection.html` | Step 2b 설명 · 감지 순서 4 번 · 묶음 타겟 문단 · 매핑 소제목 · 감지 결과 틀 줄 |
| `a0dad4b` | `docs/tone-kit/dart-flutter-idioms.html` | 슬롯 표 칸에서 정규식을 빼고 아래 `audit_greps` 코드 블록 넷째 줄을 가리키게 했다 |
| `45a47ab` | `docs/bambu-kit/bambu-print-profile.html` | 미검증 표의 enum 행 · 음성 대조 카드 문단 · G-code 길이 재기의 `G91` 줄 |
| `d213037` | `docs/design-kit/visual-change-protocol.html` | §6 규칙 두 줄 · 통과 못 하면 막는 검사 코드의 새 줄 아홉 · 종료 코드 표 1 · 2 행 |
| `796fba0` | `docs/design-kit/design-mockup.html` | 감지 대상 줄 · 비범위 표 규칙 · 새 폐기 칸 · `PRD 없음` 문단 (c4d-notes R4) |
| `4033bbe` · `bcb4b1b` | `docs/api-kit/multi-sample-pagination-variance.html` | 경로 간 불변식 절을 바로잡힌 설계 §9.2 로 맞추고 출처 이름표 · 함정 줄도 고쳤다. 둘째 커밋은 원본에 없는 도구 판 번호를 뺐다 |
| `92d2294` | `docs/infra-kit/infra-test.html` | 검사 스크립트 규칙 1 을 YAML 구조 읽기로, 「빼면 생기는 일」 표에 새 행 · 새 `CORE_TOOLS` 행 |
| `c593873` | `docs/harness/plugin-validation.html` | V8 따옴표 규칙 전부 · V8 요약 카드와 절 이름표 · 나쁜 예 둘 · V10 1.4.1 판정 카드 |
| `05fcdcd` | `docs/process/kaizen-flow.html` | 킷 카드 13 개 파일 표시를 원본 범위 줄에서 다시 만들고 공통 실행 패턴에 범위 줄 설명을 더했다 |

판단이 갈린 곳과 근거:

- multi-sample-pagination-variance 의 출처 이름표 · 함정 줄은 계약상 재량이었지만 고쳤다 — 옛 이유가 남으면 같은 쪽 안에서 새 이유와 어긋나기 때문이다
- 첫 커밋에 `hurl` 판 번호를 적었다가 SK-13 이 원본 · 옛 페이지 어디에도 없는 판 번호라고 잡아 뺐다 — 실측 날짜와 기준 기록 이름만 남겼다
- plugin-validation 의 V10 카드에 규격 원문 주소를 달려다 뺐다 — 저장소 안에 없는 주소라 확인할 수 없어, 같은 절의 가이드 링크를 달았다
- kaizen-flow 의 공통 실행 패턴 새 줄은 줄 안 코드 표시 없이 적었다 — 그 목록은 한 줄 가로 배치라 코드 표시를 넣자 375 폭에서 220px 넘쳤다
- 쪽마다 기존 클래스(`plain-list` · `note` · `compare` · `card`)만 썼고 새 스타일 · 스크립트 · 파일은 더하지 않았다

## 넘긴 것과 사유

| 항목 | 사유 |
| --- | --- |
| `docs/api-kit/snapshot-sealing-canonicalization.html` | 원본이 바뀌었지만 페이지 머리가 이미 `v0.1.2 · 최종 갱신 2026-09-26` 이고 `-0` 검사 절도 새 글이라 손대지 않았다 |
| `docs/api/research-log.md` | 대응하는 문서 페이지(research-log)가 없어 새로 만들지 않았다 — 과제 지시 |
| `reflect-kit/skills/reflect-digest/SKILL.md` | 대응하는 문서 페이지(reflect-digest)가 없어 새로 만들지 않았다 |
| `tone-kit/references/adapter-contract.md` | 대응하는 문서 페이지(adapter-contract)가 없어 새로 만들지 않았다 |
| `tone-kit/references/adapter-dart-flutter.md` | 대응하는 문서 페이지(adapter-dart-flutter)가 없어 새로 만들지 않았다 |
| `tone-kit/references/locale-korean.md` | 대응하는 문서 페이지(locale-korean)가 없어 새로 만들지 않았다 |
| `rust-kit/references/project-detection.md` | rust-kit 쪽 대응 문서 페이지가 없어 새로 만들지 않았다 (flutter-toolkit 쪽 페이지와 다른 원본이다) |
| `.claude/skills/kaizen-orchestrator/references/phase-research-templates.md` | 대응하는 문서 페이지(phase-research-templates)가 없어 새로 만들지 않았다 |
| `docs/tone/dart-flutter-idioms.md` 머리 판 | 원본이 글을 바꾸고도 머리 판(`0.1.0` · `2026-09-02`)을 안 올렸다. 페이지 머리는 원본을 따라 그대로 두었고, 원본 판 올리기는 이 묶음 범위 밖이라 넘긴다 |
| bambu-print-profile 검사 코드 원본 1600 ~ 1612 줄 | 페이지가 검사 코드를 싣지 않고 미검증 표로 요약하므로 바뀐 줄 대조에서 뺐다. 같은 동작 변화는 표의 enum 행과 원본 2041 줄 문단으로 옮겼다 |
| kaizen-flow 원본의 197 줄 밖 바뀐 자리 | 참조 목록 · research-log 함정 · 데이터 풀 표 · F2 매핑 · F4 점검표는 페이지에 그 절이 없어 옮길 자리가 없다 — 대조는 197 줄만 본다 |
| 공통 스타일 · 움직임 줄이기 · 행간 · 320px 넘침 | 다음 묶음(핸드오프 §C4 5 번)에서 공통 틀을 정한 뒤 한다 |

## 킷별 판 올림 판단

없음. 바뀐 파일이 `docs/` 페이지 열한 쪽과 `.harness/` 기록뿐이라 어느 킷의 `plugin.json` 에도 속하지 않는다. `python3 scripts/validate-plugin.py` 는 `Total: 14 plugins, 14 OK` · 종료 코드 0 이다.

## 문서 드리프트

`python3 scripts/detect-docs-drift.py` (기준 `main`, 종료 코드 0) 결과다. 페이지 재생성은 하지 않았다 — 부모가 모아서 한다.

- 이번에 맞춘 쪽: bambu-print-profile · visual-change-protocol · dart-flutter-idioms · flutter-ai-rules · flutter-toolkit project-detection · plugin-validation
- 이미 맞는 쪽: snapshot-sealing-canonicalization
- 대응 페이지 없음(`NEW`) 여섯: research-log · reflect-digest · rust-kit project-detection · adapter-contract · adapter-dart-flutter · locale-korean
- 이 도구는 kaizen-flow · design-mockup · infra-test · multi-sample-pagination-variance 를 내지 않았다. 앞 셋은 원본(`.claude/skills/kaizen-orchestrator/SKILL.md` · `design-kit/skills/design-mockup/SKILL.md` · `infra-kit/skills/infra-test/SKILL.md`)이 `main` 과 다르지만 도구의 원본 → 페이지 짝 표(`SOURCE_TO_HTML` · `SOURCE_OVERRIDES`)에 없다. 마지막은 원본 md 가 바뀌지 않았고, 고친 근거인 설계 기록 `docs/superpowers/specs/2026-09-02-api-kit-design.md` 도 짝 표 밖이다. 짝 표를 채우는 일은 `scripts/` 라 이 묶음 범위 밖이어서 넘긴다

## tone-guide 결과

`tone-kit:tone-guide` 의 1 단계(규칙 불러오기)는 구현 전에, 5 단계(전수 대조)는 모든 페이지 커밋 뒤에 실제로 돌렸고 그 결과를 아래에 적는다.

1 단계 — 오버레이 `.claude/tone-project.md` 를 읽었다(어댑터 없음 · 주석 언어 ko). 레포 판 `tone-kit/references/` 의 규칙 파일 넷과 `locale-korean.md` 를 읽었다. 이번 작업에 걸리는 규칙은 C-01 · C-04 · C-13 · C-15, N-07, S-03 · S-12, 안티패턴 B · F · H, K-02 · K-03 · K-05 · K-10 · K-11 이다.

5 단계 — 바뀐 열한 쪽의 더해진 줄 174 줄에 대조했다.

| 패턴 / 규칙 | 건수 | 판정 |
| --- | --- | --- |
| K-02 G-1 번역투 킬러 패턴 6 종 | 0 | 통과 — 같은 식에 「배경색에 의해 적용됩니다」 한 줄을 넣으면 1 이 나와 식이 살아 있다 |
| K-04 G-2 · 합니다체 | 0 | 통과 |
| K-07 G-3 라벨 파손 | 0 | 해당 없음 — 문서 주석 라벨을 쓰지 않는다 |
| C-13 자화자찬 | 0 | 통과 |
| C-04 · F 구분선 블록 | 0 | 통과 — 새 주석 구분선 없음 |
| N-07 `effective` · `resolved` 접두 식별자 | 0 | 통과 — dart-flutter-idioms 칸의 두 낱말은 규칙 설명이지 식별자가 아니다 |
| C-01 · C-15 새 코드 주석 | 5 | 통과 — plugin-validation 좋은 예 둘 · multi-sample 코드 블록 셋은 왜를 적은 단문이다 |
| H 보존 대상 | 0 삭제 | 통과 — 원본에서 옮긴 함정 · 실패 모드 주석은 글자 그대로 옮겼다 |
| K-11 새 이름 | 0 | 통과 — 새 글은 원본 · 페이지에 있던 이름(토막 · 판정식 · 비범위 표)만 쓴다 |
| S-12 같은 꼴 | 0 | 통과 — 새 스타일 없이 쪽마다 있던 클래스를 썼다 |

## 측정 도구

- 계약에서 뗀 측정 도우미: `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/d1/extracted3.sh` (봉인 커밋의 계약과 `cmp` 종료 코드 0)
- 가지 끝 재기: 같은 폴더의 `run-tip.sh` · 커밋 전 작업 폴더 재기: `wt.sh` · 몇 쪽만 넘침 재기: `wt-pw.sh`
- 교차 진단 반영 대조: `ctl2.sh` (AR-02 · DG-02 · DG-05) · `v6eq/run.sh` (AP-03 과 V6)
- 로컬 CI: `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` — 도우미 `m DG-05` 가 이 기록을 커밋한 뒤 돌린다

## 다음 사이클 메모

독립 검토(2026-09-26, BLOCKING 0)가 찾은 네 건이다. 판정을 바꾸지 않아 이 묶음에서는 페이지를 다시 열지 않았다. 재현에 쓴 파일은 세션 스크래치 `rev/` 에 있다(`d1-measure.sh` · `runall.sh` · `run2.sh` · `blocks.py` · `clip.js` · `vcp_gate.py` · `infra_check.sh` · `clone/`).

| # | 항목 | 자리 | 받을 곳 · 할 일 |
| --- | --- | --- | --- |
| R1 | bambu-print-profile 의 미검증 표에 「종류 줄만 빠진 목록」 행이 없다 | `docs/bambu-kit/bambu-print-profile.html:1647` · 원본 `bambu-kit/skills/bambu-print-profile/SKILL.md:1603-1612` | 다음 문서 맞추기 묶음. 1647 행 「목록 파일이 비었거나 깨짐 → 같음」 은 키 존재 · 종류 · enum 세 검사가 모두 빠진다고 읽힌다. 지금 원본은 `CANONICAL` 이 비었을 때만 셋 다 미실행이라 적고, 그 밖에는 빠진 줄에 해당하는 검사만 적는다. 종류 줄만 없으면 키 검사는 그대로 돌고 「종류 줄이 없어 키 스코프 불일치 FAIL 은 믿지 마라」 를 낸다. 독립 검토가 원본 1603-1612 줄을 떼어 세 상태(종류 줄 없음 · enum 줄 없음 · 빈 목록)로 돌려 문구 셋을 확인했다. 표에 「종류 줄만 빠진 목록」 행을 더하고 「비었거나 깨짐」 행은 canonical 0 줄일 때로 좁힌다. 계약 쪽 교훈 — SK-01 이 원본 1600-1612 줄을 대조에서 빼서 측정이 이 자리를 못 봤다. 표로 줄여 옮긴 코드는 빼지 말고 표 행과 코드 분기를 짝지어 잰다 |
| R2 | dart-flutter-idioms 표 칸의 「(표 칸에 옮기면 대안 기호가 깨진다)」 는 HTML 페이지에서는 틀린 말이다 | `docs/tone-kit/dart-flutter-idioms.html:1286` (원본 `docs/tone/dart-flutter-idioms.md:633` 에서 옮긴 글) | 다음 문서 맞추기 묶음. 마크다운 표에서는 `\|` 가 칸 나눔으로 읽혀 맞는 말이지만 HTML 표 칸에서는 깨지지 않는다. 독립 검토가 Playwright 로 시작 판 페이지를 열어 옛 칸의 정규식이 온전히 보이는 것을 확인했다. 페이지에서 괄호 한 토막만 뺀다. 정규식을 칸에 되돌리지는 않는다 — 기준 자리를 한 곳에 두는 원본 뜻과 SK-03(페이지 안 정규식 1 건)에 맞춘다 |
| R3 | DG-05 는 「CI 단계를 전부 돌린다」 고 적었지만 한 단계가 빠진다 | `.github/workflows/ci.yml:52` `python3 scripts/run-kaizen-assertions.py` · 도구 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` | 다음 계약의 DG-05 틀. `ci-local.sh` 는 끝에 「이 스크립트 밖의 것」 아래 이 줄을 찍지만 계약 도우미는 요약의 `rc=0` 개수만 센다. 가지 끝 복제본에서 따로 돌리면 `Total: 14 passed, 0 failed` · 종료 코드 0 이라 숨은 실패는 없다. 도구는 본 체크아웃의 추적 안 된 파일이라 이 묶음에서 고치지 않았다. 도구에 이 단계를 더하거나, 도우미가 「이 스크립트 밖의 것」 줄이 설치 단계뿐인지도 재게 한다. 이번에 따로 돌린 결과는 아래 「QA 뒤 로컬 CI」 에 있다 |
| R4 | 쉬운 말 목록에 오른 낱말을 구현자가 새로 썼다 (원본에서 그대로 옮긴 글은 뺐다) | `docs/api-kit/multi-sample-pagination-variance.html:429` `정본은 …` · 이 notes 31 · 33 · 43 줄 · 커밋 메시지 `a0dad4b` 제목과 본문 · `d213037` 제목과 본문 · `bcb4b1b` 본문 | notes 세 줄은 이 커밋에서 고쳤다(「`audit_greps` 코드 블록 넷째 줄」 · 「통과 못 하면 막는 검사 코드」 · 「기준 기록」). 페이지 429 줄은 QA 가 승인한 판이라 다시 열지 않았다 — 다음 문서 맞추기 때 `정본은` 을 `기준 기록은` 으로 바꾼다(원본 설계 기록의 정정 문단에는 이 낱말이 없다). 커밋 메시지는 고치지 않는다 — 가지 기록을 다시 쓰면 커밋 번호를 적어 둔 이 notes 와 QA 리포트가 모두 어긋난다 |

QA 피드백 YAML(`~/.harness/feedback/evaluator/1a3bcba6-2026-09-26T163259-bda55d45-35139.yaml`)의 `cross_diagnosis_by: pending-parent` 는 부모가 교차 진단을 마치면 채운다. QA 가 넘긴 두 질문에 독립 검토가 답했다 — (1) 뜻을 잘못 읽어 판정이 틀린 조건은 없다. 봉인 커밋 `e84dc35` 의 도우미로 27 조건을 가지 끝에서 다시 재 모두 기대값과 같았다. (2) 0 건으로 통과한 조건 가운데 문제가 있어도 0 을 냈을 자리는 SK-01 이 대조에서 뺀 원본 1600-1612 줄(R1)이다. DG-05 는 가지 끝 복제본에서 `rc=0` 22 줄 · SKIP 한 줄로 다시 나왔고, 조건 문구만 측정보다 넓다(R3).

## QA 뒤 로컬 CI

`9f78f0f` 위에 이 notes 수정만 커밋 전으로 올린 상태에서 `ci-local.sh` 를 다시 돌렸다(2026-09-26 07:49 ~ 07:52 UTC, `TMPDIR` 은 세션 스크래치 `d1-final/ci`, 도구 sha256 앞자리 `a415eaff98a46b86` 로 봉인 전 값과 같다, 시작 전 다른 `save-test.sh` · `ci-local.sh` 실행 0 개). CI 단계는 `.harness/.meta/` 를 읽지 않는다.

- `rc=0` 22 줄, `feedback-agg-test SKIP (yq 없음)` 한 줄, 도구 종료 코드 0
- 도구 밖 단계 `python3 scripts/run-kaizen-assertions.py`(R3)를 따로 돌렸다 — `Total: 14 passed, 0 failed`, 종료 코드 0
- CI 파일에만 있는 나머지 줄은 설치 단계(`pip install pyyaml` · zsh 설치 · `npm ci` · playwright 설치)와 `yq` 가 있을 때만 도는 `aggregation-test.sh` 블록뿐이다
- 실행 뒤 작업 폴더에 새로 생긴 파일 0 개(이 notes 수정 한 줄만 남음)
