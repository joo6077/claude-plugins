---
feature: "카이젠 2026-09-24 Phase 3 계약 — 산출물이 검사일 때 평가자가 사본으로 돌리는 다섯 가지 · 0 기대 측정의 매치 줄 가르기 · 삭제 열거 · 스키마 v5.5 반대편 정합 · 회귀 확인 패턴 되살리기"
slug: kaizen-0924-p03-evaluator
created: "2026-09-24 23:06"
complexity: "복잡"
conditions: 28
status: done
owner_session: de8c7935-a5b6-4df5-9106-fafa73c288a0
conditions_digest: sha256:5d66862766e261e9
locked_at: "2026-09-24 23:59"
---

## 배경

이 Phase 의 외부 근거는 `.harness/.meta/evidence/phase3.md` 하나다. 처리 배정표(`.claude/kaizen-input/insights-report.md`)에서
`배정` 칸이 `Phase 3` 인 행은 넷이다. Phase 2 가 넘긴 반대편 목록(`.harness/.meta/kaizen-0924/phase2-notes.md` §넘기는 것 — Phase 3)과
러닝북 Phase 3 추가 과제가 있고, 카이젠 스킬 Step 2 · Step 7 에서 하나를 더 찾았다.

| 키 | 내용 | 이번 처리 |
| --- | --- | --- |
| `harness:P04` | qa-evaluator 규칙 10 아래, 산출물이 검사일 때 평가자가 직접 돌려 볼 다섯 가지 (계약 지정 배정) | 반영 — SK-01 · SK-02 |
| `user-setup:P4` | 규칙 10 뒤 네 줄 — 첫 칸만 · 안 돌아가는 시험 · 전체 꺼짐 · 삭제 열거. 앞 셋은 `harness:P04` 와 같다 — 한쪽만 남긴다 | 앞 셋은 SK-01 한 벌로 합침. 삭제 열거는 반영 — SK-04 |
| `F16` | 새 검사가 조용히 실패 — 첫 칸만 읽기 · 안 돌아가는 시험 파일 · 한 칸 못 읽으면 전체 꺼짐 | 평가자 확인 목록으로 반영 — SK-01. 킷별 실제 결함은 각 Phase (bambu:P2~P4 · other-kits:P2 · P3 · P5) |
| `F31` | 측정 스크립트 · UI 변경마다 독립 검토 에이전트 (계약 지정 배정) | 측정 스크립트 부분 반영 — SK-01 ⑤ 알려진 답 · SK-03 교차 진단 둘째 질문 · SK-04 삭제 목록. UI 관례 대조는 Phase 5 (`flutter:P-INSPECTOR-convention`) |
| `harness:P08` (Phase 2 행, 비고 「qa-evaluator 쪽 Evaluated 는 Phase 3 과 맞춘다」) | 평가 시각을 `date` 출력으로 | 반영 — SK-06 |
| Phase 2 넘김 (`phase2-notes.md` 표 9 행) | 스키마 v5.5 의 반대편 — 표준형 5 요소 · 커밋 구간 상태 전제 · 버전 표기 · Parity 16 행 · 평가자가 옛 `--cached` 권고를 가르치는 예시 | 반영 — AR-01 · AR-02 · AR-03 · SK-06 |
| Phase 2 넘김 — Phase 3 확인 목록 | 보조 스크립트 정규식이 `경로:13:8` 에서 열 번호 8 을 줄 번호로 읽었다 | SK-01 ⑤ 효과 증명의 예로 반영 |
| 러닝북 Phase 3 과제 — 지난 사이클 메타 이슈 3 | grep 이 「금지어를 나열한 조항」 과 「실제 위반 용법」 을 가르지 못한다 (`.harness/.meta/orchestrator-audit-log.md` 신규 메타 이슈 3) | 반영 — SK-05 |
| 카이젠 Step 7 회귀 확인 | `harness/evals/kaizen/evaluator-kaizen/assertions.json` 의 `vacuous-zero` 둘째 패턴이 2026-09-22 부터 0 건 — 표에만 있고 아무도 돌리지 않는 확인 | 반영 — AR-04 · DG-07 |

고칠 것은 여섯 갈래다.

1. **산출물이 검사일 때 (P04 · user-setup:P4 · F16 · F31).** 규칙 10 은 평가자 **자신의** 측정이 살아 있는지(0 기대 측정의 양성
   대조)를 보고, 규칙 12 는 9 항 대상의 **테스트**가 구현을 재는지를 본다. 스프린트 산출물 **자체가 검사**(검사 스크립트 · 막는 훅 ·
   검증기 · 새 시험 파일)일 때 그 검사가 살아 있는지를 평가자가 확인하는 절차는 없다. 실측(데이터 풀 §0-b `be3037df` 2026-09-23 ·
   글로벌 평가 피드백 `1a3bcba6-2026-09-23T113914`): 한 킷의 검사 강화 스프린트가 APPROVE 를 받았는데, 새 검사가 첫 칸만 읽었고 ·
   표에만 올린 시험 파일은 실행 목록에 없었고 · 한 칸을 못 읽으면 검사 전체가 꺼졌다. 셋 다 교차 검토가 잡았다. 다음 날
   (`1a3bcba6-2026-09-24T101420`)에는 평가자 자신의 측정이 frontmatter 를 못 읽은 계약 16 개를 봉인 없음으로 분류해 조용히 건너뛰었다.
2. **0 기대 측정의 매치 줄 (메타 이슈 3).** 규칙 10 은 **0 이 나왔을 때** 그 0 이 살아 있는지만 다룬다. 매치가 **나왔을 때** 그 줄이
   금지 조항 · 인용 · 다른 뜻인지 가르는 규칙이 없다. 실측(글로벌 평가 피드백 `1a3bcba6-2026-09-24T113221`, REJECT): 측정
   `grep '10 카테고리|V1~V10|V1-V10'` 이 다른 뜻의 「10 카테고리」 세 줄을 잡았고, 같은 측정을 좁히라는 제안이 그날 세 평가
   (`…T113221` · `…T124739` · `…T130805`)에 되풀이됐다. 평가자 스스로도 교차 진단에 「문자 그대로 FAIL 판정한 것이 맞는지 검토
   요청」 을 남겼다 — 규칙이 없어 판정이 흔들린다.
3. **삭제 열거 (user-setup:P4 · F31).** 평가자는 지운 파일을 따로 보지 않는다. 데이터 풀 §0-b `9a0d4163`: 잘못된 커밋 하나가 파일
   3217 개를 지운 것으로 기록했다. 커밋 훅(`harness/scripts/commit-guard.sh:11` `limit=50`)은 50 개를 넘는 삭제만 막는다.
4. **교차 진단 둘째 질문 (F31 독립 검토).** 부모가 띄우는 교차 진단의 둘째 질문은 「0 건 · 빈 출력 근거 PASS 가 공허한가」 뿐이라,
   산출물이 검사인 스프린트에서 위 다섯 가지를 빠뜨렸는지 묻지 않는다.
5. **스키마 v5.5 반대편 (Phase 2 넘김 · harness:P08).** Phase 2 가 스키마를 v5.5 로 올리며 넘긴 자리가 그대로다 — 평가자 Step 1.5
   · 가이드 Binary Decidability 6 항이 「표준형 4 요소」 와 커밋 전 상태 전제만 적는다. 가이드 `:1785` 는 커밋 뒤에 늘 빈 집합을
   재는 `--cached` 를 계약 수정 예시로 가르친다. 참조 스키마 `(v5.3)` · Parity with `1.5.0 · 1.6.0 · v5.0` · Schema link `v5.3` 이
   스테일하다 — 가이드 §버전 정보 의 추출 스니펫을 지금 돌리면 `1.6.0 · 1.7.0 · v5.1 · v5.5` 가 나온다. Parity Table 에 16 행
   (알려진 답 대조)이 없다. 리포트 틀의 `Evaluated:` 는 손으로 채운다.
6. **회귀 확인 패턴 (카이젠 Step 7).** `assertions.json:13` 의 패턴 `Agent\(general-purpose\)` 는 `cb39d89`(2026-09-22)가 교차 진단
   주체를 부모로 옮기며 `qa-evaluator.md` 에서 뺀 문자열이다. 그 뒤로 이 확인은 0 건인데 돌리는 실행기가 없어 아무도 몰랐다 —
   F16 의 「표에만 있고 안 돌아가는 시험」 이 이 킷 안에 있다. 바로잡고, 1 번 규칙을 지키는 fixture 를 더한다.

판정 임계는 건드리지 않는다. 카이젠 스킬 Gotcha 「severity 편향 방지」 — 최근 10 건 APPROVE 9 · REJECT 1(90 %, 피드백 파일 이름의
시각 순), 최근 30 건 26 · 4. 이번 변경은 확인을 더하는 쪽이고, 2 번은 판정을 계약 측정 그대로 두고 낱말 필터를 금지하는 쪽이라
완화가 아니다. AR-05 가 판정 규칙 · 미검증 임계 · 두 Canonical 절이 글자 그대로인지, 새 문단을 더하는 네 구간(판정 엄격도 ·
Red Flags · Evidence Validity Gate · Enforcement 등급)에서 기존 줄을 지우거나 바꾸지 않았는지 잰다.

## 리서치 소스

외부 조회 0 회. 아래 URL 은 전부 근거 파일 `.harness/.meta/evidence/phase3.md` 에서 가져왔다.

- [MITRE CWE-20](https://cwe.mitre.org/data/definitions/20.html) — 빠진 입력 · 남는 입력까지 관련 속성 전부를 검사하라 (다섯 가지 ①)
- [MITRE CWE-754](https://cwe.mitre.org/data/definitions/754.html) — 예외 조건 하나를 잘못 다뤄 예상 밖 상태가 되는 결함 (③)
- [pytest Exit Codes](https://docs.pytest.org/en/stable/reference/exit-codes.html) — 수집 0 건은 종료 코드 5 (②. 가이드에 이미 있는 인용)
- [zsh Parameter Expansion](https://zsh.sourceforge.io/Doc/Release/Expansion.html) — `SH_WORD_SPLIT` 이 꺼진 기본값에서 매개변수 확장을 쪼개지 않는다 (④)
- [git diff](https://git-scm.com/docs/git-diff) — `--name-status` 의 상태 문자 `D` 는 삭제 (삭제 열거)
- [CheckEval — arXiv 2403.18771](https://arxiv.org/abs/2403.18771) — 판정을 추적 가능한 yes/no 로 쪼갠다 (다섯 가지의 한계 문단. 가이드에 이미 있는 인용)

근거 파일이 스스로 밝힌 한계를 그대로 옮긴다: 「둘째 칸에만 위반을 둔 사본 · 못 읽는 칸과 실제 위반을 섞은 사본 · 판정 줄을 지운
사본」 을 그대로 규정한 1 차 출처는 없다 — CWE-20 · CWE-754 · CheckEval 을 레포 규칙으로 옮긴 추론이다. 모든 칸을 읽어야만 안전한
검사에는 부분 진행보다 실패로 닫는 쪽이 옳을 수 있다(근거 파일 §2 ② 반대 근거) — ③ 에 그 분기를 넣었다. 이름을 찍지 않는 러너가
있어 「실행 출력에 파일 이름」 만 요구하면 거짓 실패가 난다(§2 ③ 한계) — ② 에 수집 명령 출력의 시험 수를 대안으로 넣었다.
`A..B` 구간은 커밋하지 않은 삭제를 담지 않는다(§2 user-setup:P4 (d) 주의) — 삭제 열거에 `git status --porcelain` 을 함께 넣었다.
근거 파일이 짚은 가이드 `:132` 「12 개 이상의 편향」 수치는 이번 조회로 재확인되지 않았다 — 이번에 고치지 않고 다음 사이클 메모로 넘긴다.

내부 입력: 데이터 풀 §0 처리 배정표 · §0-b `be3037df` (F16) · `9a0d4163` (3217 개 삭제) · `f5b7f3a5` · §1 최근 REJECT · Improvement
(2026-09-24 ER-02 · AR-02) · 글로벌 평가 피드백 `~/.harness/feedback/evaluator/` 최근 30 건과 `grep` 으로 찾은 네 건(위 배경).
인사이트 원문 보고서 `~/.claude/usage-data/report-2026-09-24-095238.html` 의 제안 「adversarial `qa-evaluator` … required checklist」 다섯 줄과
「Task Agents … (3) list any file deletions in the diff」.

## GAP 분석 · 개선안 초안

### 1.1 복잡도 4 축

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 3 — 평가자 에이전트 프롬프트 · 평가 방법론 가이드 · 카이젠 회귀 fixture |
| 공개 API·계약 변경 | 외부에 노출된 형태가 바뀌는가 | 예 — 평가 리포트 형식에 `Check Artifacts` · `Deletions` 블록, 교차 진단 둘째 질문, `Evaluated` 채우는 법 |
| 소비면 존재 | 이 형식을 받아 쓰는 반대편이 있는가 | 예 — 아래 Counterpart 표 (`/sprint` Step 4.5 가 넘김 절을 읽는다 · kit reviewer 6 종이 Canonical 두 절을 복제한다 · 설계 가이드 parity 표) |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 이후 모든 QA 판정이 이 파일을 읽는다. 회귀 확인 패턴(`assertions.json`) · V6 · V10 · 판정 임계 |

레이어가 셋이고 나머지 세 축이 전부 「예」이며, 공개 형식 변경과 소비면이 둘 다 「예」라 **복잡**이다. Step 2.5 Counterpart 조건을 넣는다 (SK-03 · AR-05 · ER-03).
기능 조건은 18 개다 — 복잡 9~20 안이다 (SKILL.md Step 6.2 둘째 명령으로 이 파일을 세면 18).

### 1.2 설정 리터럴 대조표

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A 사유에 그대로 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A 사유에 그대로 |
| `diagnostics.ide_exclude` | `[]` | DG-02 에 그대로 |
| `contract_categories[].id` / `prefix` | `Skill`/`SK` · `Script`/`SC` · `Error`/`ER` · `Architecture`/`AR` | 조건 섹션 제목과 접두 그대로 |
| `anti_patterns[].id` / `message` | AP-01 · AP-02 · AP-03 · AP-04 | AP-01 · AP-03 · AP-04 선별, message 원문 그대로. AP-02(force push)는 이 Phase 가 밀어 넣지 않아서 뺀다. AP-04 는 `harness/agents/qa-evaluator.md` 를 고치므로 넣는다 |

### 1.4 편집 전 감사 (실제로 읽은 줄 — 시작 커밋 `165c8d5` 판)

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 |
| --------- | ---------------------------- | ------------------- | ----------- |
| `harness/agents/qa-evaluator.md` | `:62-63` (규칙 10 · 0 기대 양성 대조) · `:67` (규칙 12 · 9 항 한정) | 산출물이 검사일 때의 확인 없음 · 매치가 나왔을 때의 줄 가르기 없음 | SK-01 · SK-05 |
| 같은 파일 | `:579-592` (Step 1.5 · 6 항 `:590`) | 표준형 4 요소 · 커밋 구간 전제 없음 | AR-01 |
| 같은 파일 | `:594-661` (Step 2 · N/A 블록 `:656-661`) | 삭제를 따로 보지 않는다 | SK-04 |
| 같은 파일 | `:786-802` (Step 3.5 · 9 항 `:800`) | 새 블록을 확인하는 self-check 없음 | SK-02 |
| 같은 파일 | `:804-904` (Step 4 틀 · `Evaluated` `:811` · Handoff `:842-853` · Discrimination `:880-883`) | 손으로 채우는 시각 · 검사 산출물 · 삭제 블록 없음 | SK-02 · SK-04 · SK-06 · SK-03 |
| 같은 파일 | `:1006-1032` (Step 7 · 질문 `:1023-1025`) | 둘째 질문이 0 건만 묻는다 | SK-03 |
| 같은 파일 | `:1094-1108` (판정 규칙) · `:54` (규칙 2 임계) | 이번에 바꾸지 않는다 | AR-05 |
| 같은 파일 | `:1110-1161` (Red Flags · `:1138-1139`) · `:1217` (가이드 `v4`) | 새 두 변명 없음 · 옛 버전 | SK-01 · SK-05 · AR-02 |
| `harness/docs/guides/qa-evaluation-guide.md` | `:1-4` · `:12` · `:14` (머리 · 스키마 v5.3 · 최근 갱신) · `:1910-1941` (버전 정보 · Parity with `:1915` · Schema link `:1920`) | 스테일한 버전 네 곳 | AR-02 |
| 같은 파일 | `:150-185` (Enforcement 표) · `:1848-1891` (Parity Table 9 행 · 15 행 `:1874`) | 새 원칙 등급 없음 · 16 행 없음 | AR-03 |
| 같은 파일 | `:722-747` (Binary Decidability 6 항 `:741-747`) · `:1767-1788` (예시 `:1785`) | 4 요소 · `contract-schema v4` · `--cached` 예시 | AR-01 |
| 같은 파일 | `:981-1112` (Evidence Validity Gate · 0 매치 `:1043-1081` · 렌더 `:1083-1091` · 보고 형식 `:1093`) | 산출물이 검사일 때 · 매치 줄 가르기 절 없음 | SK-01 · SK-05 |
| 같은 파일 | `:613-672` (User Correction Audit) · `:1739-1765` (교차 진단 · 핵심 질문 `:1759`) | 삭제 열거 절 없음 · 둘째 질문 좁음 | SK-04 · SK-03 |
| 같은 파일 | `:1115-1186` · `:1187-1286` (Canonical 두 절) · `:864-912` (카운팅 임계) | 이번에 바꾸지 않는다 — kit reviewer 6 종 전파가 필요 없게 | AR-05 |
| `harness/evals/kaizen/evaluator-kaizen/assertions.json` | `:1-15` (`:13` 죽은 패턴) | 2026-09-22 부터 0 건 | AR-04 · DG-07 |
| `harness/evals/kaizen/evaluator-kaizen/expected-improvements.md` | `:24-30` (`vacuous-zero`) | 새 fixture 절 없음 | AR-04 |
| `harness/evals/kaizen/evaluator-kaizen/fixture-feedback-data/` | `vacuous-zero.yaml` 전체 · `l3-miss.yaml` 전체 (형식) · 두 킷 fixture 의 `project_hash` 8 개 (`test0010` 은 contract-kaizen 이 이미 씀) | 새 fixture 는 `test0011` · `fixture-project-k` | AR-04 |
| `harness/skills/sprint/SKILL.md` | `:106-130` (Step 4.5 · `:118` 「물을 두 가지」) | 질문 수가 둘로 유지되면 그대로 맞다 — Phase 4 범위 | SK-03 (질문 수 2) · ER-03 |

구현 후보 옵션이 둘 이상이었던 다섯 곳의 선택 (넷째 · 다섯째는 검토에서 나왔다):

- 매치 줄이 전부 금지 조항이나 다른 뜻일 때 **평가자가 좁힌 측정으로 판정할지** — **하지 않는다.** 규칙 10 의 대체 측정은 늘 0 만
  내던 죽은 측정을 살아 있는 측정으로 바꾸는 것이라 판정이 엄격해지는 쪽이다. 매치를 걸러 PASS 로 바꾸는 것은 반대 방향이라, 평가자가
  계약을 코드에 맞춰 넓히는 것과 같다. 판정은 계약 측정 그대로 두고, 좁힌 측정을 두 값(지금 대상 0 · 알려진 위반 사본 1 이상)과 함께
  Improvement 로 남겨 다음 반복을 한 번에 끝내게 한다
- 교차 진단에 **셋째 질문**을 더할지 — **더하지 않는다.** `harness/skills/sprint/SKILL.md:118` 이 「물을 두 가지」 라고 적고 Phase 4
  범위다. 둘째 질문에 한 문장을 붙여 질문 수를 둘로 둔다 (SK-03 이 번호 질문 줄 수 2 를 잰다)
- 다섯 가지를 **새 parity item(17)** 으로 올릴지 — **올리지 않는다.** 생성 측 · 계약 측 짝은 ⑤ 만 있고(skill-design-guide §3.7 ·
  contract-schema §양성 대조 · §알려진 답 대조) ①~④ 는 없다. 번호를 먼저 만들면 다른 가이드의 표와 어긋난다 — 카이젠 스킬 Gotcha
  「Cross-Surface Parity 전파 확인」 대로 다음 사이클 Phase 1 · 2 로 넘긴다 (ER-03)
- 다섯 가지를 **옛 계약에도 그대로** 적용할지 (카이젠 Gotcha 「평가 루브릭 변경 시 기존 계약과의 호환성」) — **①②③⑤ 는 그대로, ④ 는
  좁힌다.** ①②③⑤ 의 FAIL 은 검사 자신의 주장(「위반을 잡는다」 · 「돈다」)의 반례라 옛 계약에 새 요구가 아니다. ④ 는 사용자 셸에 붙여
  넣는 명령과 `source` 하는 파일로 좁혀, 첫 줄 `#!` 이나 부르는 쪽이 해석기를 정한 옛 계약의 스크립트(이 레포의 훅 ·
  `harness/scripts/commit-guard.sh` 는 첫 줄이 `#!/usr/bin/env bash`)를 zsh 로 돌려 떨어뜨리지 않는다 (SK-01 열째 토큰). 돌리지 않은 것은 평가자 자신의
  증거 문제(`[미검증:INVALID]`)라 계약 쪽 부담이 아니다
- 선언 밖 삭제를 **평가자가 FAIL 로** 할지 — **하지 않는다.** 근거 파일 §4 권장안 11 은 범위 밖 `D` 행이 하나라도 있으면 FAIL 을 권했다.
  그것은 계약의 삭제 범위 조건 쪽 형태다 — 계약에 범위 조건이 있으면 평가자는 그 조건으로 FAIL 을 낸다. 조건이 없는데 평가자가 FAIL 을
  내면 계약에 없는 요구를 만드는 것이라 「사용자 확인 필요」 로 올린다 (SK-04)

### Counterpart — 바뀌는 형식을 받아 쓰는 반대편

| 파일 | 인용 | 이번 처리 |
| --- | --- | --- |
| `harness/skills/sprint/SKILL.md:118` | 「물을 두 가지가 거기 있다」 | 질문 수를 둘로 유지해 그대로 맞게 둔다 — SK-03. 파일은 Phase 4 범위라 건드리지 않는다 (ER-03) |
| `*-kit/agents/*-reviewer.md` 6 종 | 가이드 §Canonical Unverified-Evidence Protocol · §Canonical User-Reported Failure Protocol 을 복제 | 두 절을 글자 그대로 둔다 — AR-05. 전파할 것이 없다 |
| `harness/docs/guides/skill-design-guide.md` §3.7 · §11 · `harness/references/contract-schema.md` | 다섯 가지 ①~④ 의 생성 측 · 계약 측 짝 없음 | 다음 사이클 Phase 1 · 2 — 넘김 (ER-03) |
| `harness/evals/kaizen/contract-kaizen/assertions.json` · `harness/evals/kaizen/evaluator-kaizen/assertions.json` | 두 벌을 도는 실행기가 없다 (그래서 `:13` 이 2 일 동안 0 건이었다) | Phase 4(`scripts/`) · Final(`.github/workflows/ci.yml` 에 넣을 줄) — 넘김 (ER-03) |
| `docs/harness/qa-evaluation-guide.html` | 가이드의 HTML 판 | Final F2 — 넘김 (ER-03). `validate-post-kaizen.py` 의 `docs-site-regen` 은 이 Phase 뒤 FAIL 이 맞다 — DG-06 이 뺀다 |
| `harness/references/feedback-schema.yaml` | 피드백 YAML 필드 | 새 필드를 만들지 않는다 — 두 새 블록은 마크다운 리포트에만 있다 |

### 개선안 초안

정확한 문구는 스크래치 `mock.py`(`회귀 게이트` 절 경로)가 시작 커밋 판 네 파일에 적용하는 치환과 새 fixture 한 개 그대로다.
BUILD 는 이것을 기준으로 적용한다. 요지:

`harness/agents/qa-evaluator.md`:

- 규칙 10 의 0 기대 문단 뒤에 문단 둘 (4 칸 들여쓰기, 규칙 10 의 이어짐) — 「**산출물이 검사일 때 — 평가자가 사본 입력으로 직접 돌리는
  다섯 가지 (2026-09-24 추가).**」: 적용 대상(검사 스크립트 · 막는 훅 · 검증기 · 측정 스크립트 · 새 시험 파일), 사본 · 명령 · 종료 코드 ·
  읽은 대상 수 · 관찰 출력을 `Check Artifacts` 에, 실측 2026-09-23, ① 첫 칸만 읽기 ② 표에만 올린 시험(이름을 찍지 않는 러너면 수집
  명령의 시험 수) ③ 한 칸 못 읽으면 전체 꺼짐(모든 칸을 읽어야 안전한 검사면 칸 번호와 함께 실패) ④ 셸마다 다른 대상 수(해석기가
  정해진 스크립트는 그 해석기로만 · 다른 셸 칸은 `해당 없음 (고정 해석기)`) ⑤ 효과 증명(막는 검사는 알려진 위반에서 실패 · 수를 내는
  검사는 손으로 센 입력 · 계약의 `알려진 답:` 입력부터 · 예 `경로:13:8` · 임시 사본에서만 돌아 규칙 12 (3) 안전 조건과 무관), 판정(안 돌렸으면
  `[미검증:INVALID]`, 결함이 드러나면 FAIL). 「**0 이 기대값인데 매치가 나오면 줄마다 가른다 (2026-09-24 추가).**」: 줄마다 `파일:라인` 과
  분류, 낱말 필터 금지, 판정은 계약 측정 그대로, 관대해지는 쪽으로 측정을 바꾸지 않는다, 좁힌 측정은 두 값과 함께, 실측 2026-09-24
- Step 1.5 6 항 — 상태 전제 선택지 첫머리에 `Given: 이 스프린트의 커밋이 끝난 뒤`, 커밋하고 나면 빈 출력이 되는 세 명령 · 그 빈
  출력은 공허한 0, 표준형 5 요소(`· 상한 ref`)
- Step 2 끝 (Step 3 앞)에 「**삭제 열거 (구현 판정마다 · 2026-09-24 신규):**」 불릿 넷 — `--diff-filter=D` 구간 · `git status --porcelain`
  줄의 앞 두 글자(상태 칸)에 든 `D`(`grep -E '^(D.|.D) '` — 경로에 든 `D` 는 세지 않는다) · 기준 커밋 없으면 `deletions_range: unavailable` ·
  선언과 대조할 때 여러 세션이 같이 쓰는 작업 폴더면 다른 세션의 삭제일 수 있다고 함께 적기 · 재는 조건이 없으면 FAIL 이 아니라 사용자 확인
  필요 · 실측 3217 개와 훅 50 개
- Step 3.5 에 10 항 「검사 산출물 · 삭제 self-check」
- Step 4 틀 — `Evaluated:` 줄 끝에 `# 저장하는 순간 date '+%Y-%m-%d %H:%M' 출력을 옮긴다 — 짐작해 적지 않는다`, User Correction Audit 블록
  뒤에 `## Deletions` 블록 넷 줄, 둘째 질문 끝에 「산출물이 검사인 조건이면 규칙 10 의 다섯 가지 가운데 돌리지 않은 것이 있는가?」,
  Discrimination 블록 뒤에 `## Check Artifacts (산출물이 검사인 조건만 — 규칙 10)` 블록 여섯 줄
- Step 7 3 항 끝에 「산출물이 검사인 조건이면 둘째 질문에 「규칙 10 의 다섯 가지 가운데 돌리지 않은 것이 있는가?」 를 붙인다」
- Red Flags 에 두 줄 — 「새 검사가 원본 대상에서 위반 0 을 냈으니 동작한다」 · 「매치된 줄이 금지 조항이니 `grep -v` 로 빼고 0 으로 본다」
- References 의 `계약 작성 가이드 v4` → `계약 작성 가이드` (버전 값은 그 파일 머리 설정에만 둔다)

`harness/docs/guides/qa-evaluation-guide.md` (v5.0 → v5.1):

- 머리 설정 `version: v5.1` · `last_updated: 2026-09-24`, 참조 스키마 `(v5.5)`, 최근 갱신 블록 새 항목(네 불릿)과 옛 항목을
  「이전 (2026-08-13, v5.0):」 으로
- §원칙별 Enforcement 등급 표에 세 행 — 산출물이 검사일 때 다섯 가지 E2 · 0 기대 측정의 매치 줄 가르기 E2 · 삭제 열거 E1
- 새 절 `## 삭제 열거 — 변경 범위에서 지운 파일을 드러낸다 (2026-09-24 추가)` (§User Correction Audit 뒤, `### verdict 영향 — …` 소절 포함.
  상태 칸 문구 · 다른 세션 삭제 문구는 평가자와 같다)
- Binary Decidability 6 항 — AR-01 과 같은 세 고침 (`contract-schema v4 §` → `contract-schema §`)
- §Evidence Validity Gate 안 새 소절 둘 — `### 0 이 기대값인데 매치가 나올 때 — 줄마다 가른다 (2026-09-24 추가)` (§0 매치 판정 규칙
  뒤, 순서 네 단계와 실측. 감사 로그 원문대로 「두 번 관측한 메타 이슈」) · `### 산출물이 검사일 때 — 사본으로 돌리는 다섯 가지 (2026-09-24 추가)`
  (§렌더 산출물 특칙 뒤, 다섯 불릿 · **판정.** · **한계.** 문단, CWE-20 · pytest · CWE-754 · zsh 인용. ④ · ⑤ 끝 문장은 평가자와 같다)
- 교차 진단 핵심 질문 끝에 SK-03 문장, Recurring Improvement Escalation 4 항 예시를 커밋 구간으로
- References — 스키마 `v5.5` · `**알려진 답 대조**` 추가, 공식 문서에 CWE-20 · CWE-754 · zsh Parameter Expansion · git diff 네 줄
- Parity Table 제목 `(10 개 parity item` · 16 행(알려진 답 대조 — 평가자 쪽 착지는 §산출물이 검사일 때 ⑤)
- §버전 정보 — Guide version `2026-09-24 (Phase 3 kaizen · v5.1 — …)`, 옛 줄은 「이전:」, Parity with `1.6.0 · 1.7.0 · v5.1`, Schema link `v5.5`

회귀 fixture (`harness/evals/kaizen/evaluator-kaizen/`):

- `assertions.json` — `vacuous-zero` 둘째 패턴 `Agent\(general-purpose\)` → `cross_diagnosis_by: pending-parent`, 새 키 `silent-check`
  패턴 셋(`산출물이 검사일 때` · `## Check Artifacts` · 가이드 `### 산출물이 검사일 때`)
- `fixture-feedback-data/silent-check.yaml` 새 파일 — `be3037df` 모양의 APPROVE + 교차 검토가 찾은 결함 셋, `project_hash: "test0011"`
- `expected-improvements.md` — `vacuous-zero` 대체 메모에 패턴 교체 한 문장, `## fixture: silent-check` 절(기대 개선 셋)

## 범위 경계

- 이 Phase 시작 HEAD: `165c8d5dd9f81bd3485de04088494ebe62012fef`. 범위 상한은 개정 파일 `.harness/sprint-amendments-kaizen-0924-p03-evaluator.md` 의 `end_sha:` 마지막 값이다. 여러 Phase 가 같은 가지 `kaizen/2026-09-24` 에 동시에 커밋하므로 `HEAD` 로 재지 않는다
- 고치는 파일은 다섯이다 — `harness/agents/qa-evaluator.md` · `harness/docs/guides/qa-evaluation-guide.md` · `harness/evals/kaizen/evaluator-kaizen/assertions.json` · `harness/evals/kaizen/evaluator-kaizen/expected-improvements.md` · `harness/evals/kaizen/evaluator-kaizen/fixture-feedback-data/silent-check.yaml`(새 파일). `.harness/` 쪽은 이 계약 · 개정 파일 · QA 피드백 · `.harness/.meta/kaizen-0924/phase3-notes.md` · `.harness/.meta/kaizen-0924/phase3-review.md` 를 쓴다 — 슬러그를 나열하지 않고 AR-06 ③ `verify_seal` 로 잰다
- **이 Phase 의 커밋 메시지에는 전부 `Co-Authored-By` 줄 바로 위에 서명 줄 `Kaizen-Phase: kaizen-0924-p03-evaluator` 한 줄을 넣는다** (봉인 커밋 포함). AR-06 ① · ② · ER-03 · DG-06 이 이 줄로 이 Phase 커밋을 가린다(`harness/references/contract-schema.md` §여러 주체가 한 가지에 커밋할 때 선택지 B). FIX 가 커밋을 더할 때도 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다(옛 줄은 지우지 않는다). notes 커밋도 이 Phase 커밋이다 — notes 를 커밋한 뒤 그 sha 로 `end_sha:` 줄을 하나 더 덧붙여 커밋한다
- 측정이 기대는 제목은 이름을 바꾸지 않는다: `### 판정 엄격도` · `### Step 1.5` · `### Step 2` · `### Step 3.5` · `### Step 4: 판정` · `### Step 7` · `## 판정 규칙` · `## Red Flags` (평가자), `## 원칙별 Enforcement 등급` · `## 삭제 열거` · `## Binary Decidability Pre-Check` · `### 카운팅 및 자동 REJECT 임계` · `## Evidence Validity Gate` · `### 0 이 기대값인데 매치가 나올 때` · `### 산출물이 검사일 때` · `## Canonical Unverified-Evidence Protocol` · `## Canonical User-Reported Failure Protocol` · `### 교차 진단 프로토콜` · `### Recurring Improvement Escalation` · `### Parity Table` · `### 버전 정보` (가이드), `## fixture: silent-check` (expected-improvements)
- 공유 파일(`marketplace.json` · `plugin.json` 버전 · 루트 README · 루트 CLAUDE.md · `docs/` HTML · 처리 배정표 · 감사 로그 `.harness/.meta/orchestrator-audit-log.md` · 실패 횟수 `.harness/.meta/kaizen-failure-count.yaml` · `docs/kaizen/*.md`)과 Phase 4 범위인 `.harness/project.yaml` 은 건드리지 않는다. AR-06 ② 는 `.harness/` 전체를 통과시키므로 `.harness/` 안의 이 셋은 ER-03 셋째 측정이 잰다 (SK-05 가 감사 로그의 메타 이슈 3 을 인용하니 「해결」 표시를 하러 들어갈 여지가 있다). harness README 의 AUTO 구간은 에이전트 frontmatter 를 읽는데 frontmatter 를 바꾸지 않는다. 문서 사이트 재생성은 Final F2 몫이라 DG-06 에서 `docs-site-regen` 을 뺀다
- 넘기는 것 — BUILD 가 notes(`.harness/.meta/kaizen-0924/phase3-notes.md`)에 아래 여섯 문자열을 **각각 한 줄에 한 번씩** 적는다 (ER-03 이 글자 그대로 센다): `skill-design-guide.md §3.7 ①~④` (다음 사이클 Phase 1 — 다섯 가지 ①~④ 의 생성 측 짝) · `contract-schema.md ①~④` (다음 사이클 Phase 2 — 계약 측 짝) · `assertions.json 실행기` (Phase 4 — contract-kaizen · evaluator-kaizen 두 벌을 도는 실행기가 없다. `scripts/` 에 둘지 Phase 4 가 정한다) · `.github/workflows/ci.yml` (Final — 실행기가 생기면 넣을 줄) · `docs/harness/qa-evaluation-guide.html` (Final F2) · `harness/skills/sprint/SKILL.md:118` (확인만 — 질문 수가 둘이라 「물을 두 가지」 가 그대로 맞다). 처리 배정표 키 다섯(`harness:P04` · `user-setup:P4` · `F16` · `F31` · `harness:P08`)과 `메타 이슈 3` 도 notes 에 적는다. 러닝북이 적게 한 나머지(changelog 한 단락 · 킷 로그 한 단락 · 다음 사이클 메모)도 notes 에. 「미반영 키와 사유」 칸에는 `F31` 의 UI 관례 대조가 행 비고대로 Phase 5 `flutter:P-INSPECTOR-convention` 몫이라는 한 줄을 적는다. 다음 사이클 메모 후보: 가이드 `:132` 「12 개 이상의 편향」 재확인 · Phase 1 notes 가 제안한 「문장 삭제 사본으로 문서 조건의 판별력을 재는 검토 절차」(처리 배정표 밖이라 이번에 넣지 않음) · 카이젠 Gotcha 「L3 Coverage Honesty 회귀 체크」 실측 — 글로벌 평가 피드백 최근 10 건(파일 이름 시각 순, 2026-09-24T175139 ~ T223853) 가운데 `샘플링-` 태그가 든 것 0 건. 전수 검증을 주장했는데 일부만 본 태그 누락인지는 파일만으로 못 가른다
- QA(`harness:qa-evaluator`)는 설치본 — 이 Phase 가 고치기 **전** 판이다. 카이젠 스킬 Gotcha 「평가자 자기순환 방지」 대로 새 판으로 자기 자신을 평가하지 않는다
- 권고(판정 조건 아님 — 조건 줄이 없어 QA 는 이것으로 FAIL 을 내지 않는다): 새 셸 코드 블록은 넣지 않는다 — 두 파일에 더한 줄 가운데 셸 펜스를 여는 줄 0 개 (`회귀 게이트` 절 `[bash-blocks]`). 새 명령은 산문 안 인라인 코드뿐이다
- 사용자 승인(Step 5) 대체: 사용자가 「자동으로 끝까지 알아서 진행해 내 허락이 필요한건 코덱스로 리서치나 검토받고」라고 위임했다(세션 `de8c7935-a5b6-4df5-9106-fafa73c288a0` 기록 queued_command `2026-09-24T04:04:16.964Z`). Codex 사용량 한도가 소진돼(오류 원문 「You've hit your usage limit … try again at 11:05 PM」, 2026-09-24) 독립 Claude 검토자(REVIEW 에이전트)가 대신한다. 이어 사용자가 「코덱스 대신에 그냥 너가 알아서 진행하라고」라고 명시했다(같은 세션 기록 user `2026-09-24T11:54:58.940Z`). 검토 결과 파일: `.harness/.meta/kaizen-0924/phase3-review.md`. 검토 VERDICT: 1 회차(2026-09-24 23:28) `CHANGES` — 막는 이유 넷(SK-04 · AR-05 · SK-01 · ER-03)과 막지 않는 권고 아홉을 전부 이 판에 반영했다(`회귀 게이트` 절 끝 `검토 반영` 문단). 2 회차(2026-09-24 23:55) `APPROVE` — 새로 막을 결함 없음, 봉인 전에 고르면 좋은 권고 셋. BUILD 가 봉인 전에 셋 다 반영했다 — AR-05 에 더한 줄의 자리 · 수 잠금(`added:` · `evg-rest-`), SK-03 `awk` 가 제목 줄에서도 멈추게, 이 줄에 2 회차 판정. 반영 내역과 봉인 전 실측은 `회귀 게이트` 절 끝 `2 회차 검토 반영` 문단. 3 회차 검토는 없다
- 오라클 해소: SK-01 ~ SK-06 · AR-01 · AR-02 (b)~(e) · AR-03 — 산출물이 평가 규칙 문서의 문장 · 표 자체라 정해진 절 구간에 정해진 문구 · 행이 있는지가 곧 산출물 판정이다. 측정은 코드 펜스를 건너뛰는 `sect` 로 절을 잘라 재므로 파일 다른 곳의 같은 낱말로 통과하지 않고, 편집 전 파일에서 새 문구가 전부 0 · 옛 문구가 1 인 것을 봉인 전에 확인했다. 모의본에서 문장 하나만 지운 사본 48 개에서 해당 값이 0 으로 떨어지는 것을 돌려 확인했다 (`회귀 게이트` 절 문장 삭제 대조 표)
- 오라클 해소: AR-02 (c) · AR-04 · AR-05 · DG-07 — 값을 옮겨 적었는지(버전 값 · fixture 필드) · 바꾸지 않았는지(구간 `diff`) · 회귀 패턴이 잡히는지를 직접 계산한다. 각각 음성 대조가 붙어 있다
- 오라클 해소: ER-03 — 넘김 기록(notes)의 문자열이 곧 산출물이고, 편집 금지는 커밋 파일 목록(`my`)으로 잰다
- 오라클 해소: ER-01 — 새 URL 집합과 근거 파일 URL 집합을 `comm` 으로 비교하는 계산이다. 양성 대조가 붙어 있다
- 오라클 해소: AR-06 — 커밋 기록(`git log`)과 봉인 검증 함수(`verify_seal`)를 실제로 돌린 출력이다. 문서 서술을 읽지 않는다
- 오라클 해소: AP-01 · AP-04 · RE-01 · RE-02 — 더한 줄 · 머리 설정 · 커밋 파일 목록 · 표 구분줄을 센다. AP-01 · RE-02 는 양성 대조가 붙어 있다
- 오라클 해소: DG-05 · DG-06 — 판정은 검사 스크립트를 실제로 돌린 출력이다. 뒤따르는 대조는 그 출력의 파일 경로를 이 Phase 파일 · `my` 와 맞출 뿐이다
- 커버리지 해소: SK-01 ~ SK-06 · AR-01 ~ AR-05 — 산문의 파일 이름(`qa-evaluator.md` · `qa-evaluation-guide.md` · `assertions.json` · `expected-improvements.md` · `silent-check.yaml`)은 측정의 `"$T/EV"` · `"$T/QG"` · `"$T/AS"` · `"$T/EI"` · `"$T/FX"` 다. 공통 정의가 다섯 파일의 `$END` 판을 그 이름으로 꺼낸다. 산문의 토큰은 측정의 `toks` · `grep -cF` 가 인자로 하나씩 센다
- 커버리지 해소: ER-03 — 산문의 여섯 문자열 · 키 여섯은 측정의 `for t in …` 한 줄이 같은 열둘을 하나씩 notes 에서 `grep -cF` 한다. 편집 금지 파일은 `my | grep -cE …` 정규식이 덮는다 — 검토 반영으로 산문에 든 `project.yaml` 은 그 정규식의 `\.harness/project\.yaml$` 가, 감사 로그 · 실패 횟수 파일은 `\.harness/\.meta/(orchestrator-audit-log\.md|kaizen-failure-count\.yaml)$` 가 덮는다
- 커버리지 해소: AR-06 — 허용 다섯 파일은 ② 의 `grep -cxE` 정규식 하나가 덮는다 (펼친 이름은 위 둘째 줄)
- 커버리지 해소: SK-03 — 산문의 `harness/skills/sprint/SKILL.md:118` 은 재는 대상이 아니라 질문 수를 둘로 두는 이유(Counterpart)다. 그 파일은 Phase 4 범위라 이 조건은 평가자 쪽 번호 질문 줄 수 2 로 잰다
- 커버리지 해소: 검출기 실측(2026-09-24 23:1x, 검토 반영 뒤 23:4x 에 다시) `UNCOVERED` 다섯 건 — SK-03 · SK-04 · ER-03 · AR-02 · AR-04. 다시 잰 판에서 늘어난 것은 ER-03 의 `project.yaml` 하나(위 ER-03 줄). 전부 위 세 이유(파일 이름은 `"$T/…"` 사본 · 토큰은 공백 든 코드 조각 안의 `toks` · `for t in …` 인자 · SK-03 의 Counterpart 경로)다. 검출기는 공백 든 코드 조각 안의 인자를 읽지 못한다
- 편집 전부터 있던 markdownlint 경고(평가자 13 · 가이드 9 · expected-improvements 0 줄)는 범위 밖이다 — DG-02 는 더한 줄만 잰다
- 기능 조건 18 · 전체 조건 줄 28 (N/A 5 · 금지 패턴 3 · 자동 포함 중 N/A 아닌 2)

## 회귀 게이트 — 측정 공통 정의와 봉인 전 실측

모든 조건의 측정은 아래 블록을 먼저 실행한 **bash** 셸에서 돈다 — 블록과 측정을 한 `bash -c` 안에 넣거나 블록을 파일로 저장해
`. 파일` 뒤에 잇는다. `END_UNRESOLVED` 가 찍히면 셸이 종료 코드 2 로 끝난다. `fm_get` · `sha256_16` · `contract_digest` ·
`verify_seal` 은 `harness/references/contract-schema.md` §계약 봉인 정의 그대로 더한다.

```bash
# 측정 공통 정의 — bash 로 실행한다 (zsh 에서 source 하지 마라. zsh 는 "$B:harness/…" 의 :h 를 경로 수식어로 읽는다)
export LC_ALL=C.UTF-8   # 번역투 정규식이 글자 단위로 돌아야 한다 — C 로케일이면 덜 잡힌다 (실측 UTF-8 2 · C 1)
cd /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/kaizen-0924 || exit 2
B=165c8d5dd9f81bd3485de04088494ebe62012fef                  # 이 Phase 시작 HEAD
SIG='Kaizen-Phase: kaizen-0924-p03-evaluator'
AM=.harness/sprint-amendments-kaizen-0924-p03-evaluator.md
END=$( [ -f "$AM" ] && sed -n 's/^end_sha:[[:space:]]*//p' "$AM" | tail -1 )
if [ -z "$END" ] || ! git rev-parse -q --verify "$END^{commit}" >/dev/null; then
  echo "END_UNRESOLVED — 측정을 멈추고 BUILD 에 묻는다. HEAD 로 바꿔 재지 않는다"; exit 2
fi
EV=harness/agents/qa-evaluator.md; QG=harness/docs/guides/qa-evaluation-guide.md
KZ=harness/evals/kaizen/evaluator-kaizen
AS=$KZ/assertions.json; EI=$KZ/expected-improvements.md; FX=$KZ/fixture-feedback-data/silent-check.yaml
EVID=.harness/.meta/evidence/phase3.md
T=$(mktemp -d)
for k in EV QG AS EI; do p=${!k}; git show "$B:$p" > "$T/$k.0"; git show "$END:$p" > "$T/$k"; done
git show "$END:$FX" > "$T/FX" 2>/dev/null || : > "$T/FX"   # 새 파일 — 없으면 빈 파일로 두어 AR-04 (b) 가 떨어진다
fv() { git show "$END:$1" | awk '/^---$/{n++; next} n==1 && /^version:/{sub(/^version:[[:space:]]*/,""); print; exit}'; }
SV=$(fv harness/docs/guides/skill-design-guide.md); AV=$(fv harness/docs/guides/agent-design-guide.md)
CV=$(fv harness/docs/guides/contract-design-guide.md)
SCV=$(git show "$END:harness/references/contract-schema.md" | sed -n 's/^현재: \*\*\(v[0-9.]*\)\*\*.*/\1/p')
# sect <파일> <제목 앞부분> — 그 제목부터 같은 깊이 이하의 다음 제목 전까지. 코드 펜스 안의 `#` 줄은 제목으로 보지 않는다
sect() { awk -v h="$2" '
  /^[[:space:]]*(```|~~~)/ { fence = !fence }
  !f && !fence && index($0, h) == 1 { f = 1; lvl = match($0, /[^#]/) - 1; print; next }
  f && !fence && /^#+ / { l = match($0, /[^#]/) - 1; if (l <= lvl) exit }
  f' "$1"; }
toks()  { local s="$1"; shift; for t in "$@"; do printf '%s ' "$(printf '%s\n' "$s" | grep -cF -- "$t")"; done; echo; }
url()   { grep -oE 'https?://[^ )>"`]+' | sed -E 's/[.,;:]+$//' | sort -u; }
added_nofx() { for k in EV QG AS EI; do git diff --no-index -U0 "$T/$k.0" "$T/$k"; done | grep '^+' | grep -v '^+++'; }
added() { added_nofx; sed 's/^/+/' "$T/FX"; }
mine() { git log --format= --name-only "${1}..${2}" --grep="^${3}\$" | grep . | LC_ALL=C sort -u; }
unsigned_on() { _b=${1}; _u=${2}; _s=${3}; shift 3
  git log --format=%H "${_b}..${_u}" -- "$@" | while read -r _c; do git log -1 --format=%B "$_c" | grep -qxF "$_s" || echo "$_c"; done; }
my() { mine "$B" "$END" "$SIG"; }
K02='(을|를) ?(처리|관리)(합니다|한다)|에 대해서?|하도록 (합니다|한다)|에 의(해|하여)|되어 있(는 경우|을 때)|(표시|적용|호출|생성|반환)(됩니다|된다)'
S4=$(sect "$T/EV" '### Step 4: 판정')
```

DG-07 이 쓰는 회귀 확인 계산기 (`python3 dg07.py "$T"` — 카이젠 스킬 Step 7 Regression Smoke Test 를 `$END` 판 사본에 돌린다):

```python
import json, re, sys
# dg07.py <T 폴더> — T/AS 의 패턴을 T/EV · T/QG (각 file 의 사본)에서 센다
T = sys.argv[1]
m = {'harness/agents/qa-evaluator.md': f'{T}/EV', 'harness/docs/guides/qa-evaluation-guide.md': f'{T}/QG'}
a = json.load(open(f'{T}/AS', encoding='utf-8'))
out = []
for k, v in a.items():
    for i, x in enumerate(v):
        out.append(f"{k}#{i}:{len(re.findall(x['pattern'], open(m[x['file']], encoding='utf-8').read()))}")
print(' '.join(out))
print('min', min(int(s.rsplit(':', 1)[1]) for s in out), 'n', len(out))
```

AP-03 이 쓰는 펜스 검출기 (`python3 fence.py <파일>...` — Phase 1 · 2 계약과 같은 것):

```python
import re, sys
# 여는 펜스에 언어 힌트가 없으면 bare. 4-백틱 바깥 펜스 안의 ``` 는 내용으로 본다
tot_bare = tot_unclosed = 0
for path in sys.argv[1:]:
    open_len = 0; open_ch = ''; bare = []
    for n, line in enumerate(open(path, encoding='utf-8'), 1):
        m = re.match(r'^\s*(`{3,}|~{3,})(.*)$', line.rstrip('\n'))
        if not m:
            continue
        run, rest = m.group(1), m.group(2).strip()
        if open_len == 0:
            open_len, open_ch = len(run), run[0]
            if not rest:
                bare.append(n)
        elif run[0] == open_ch and len(run) >= open_len and not rest:
            open_len = 0
    tot_bare += len(bare); tot_unclosed += 1 if open_len else 0
    print(f"{path}: bare_open={len(bare)} {bare} unclosed={1 if open_len else 0}")
print(f"bare_open_total={tot_bare} unclosed_total={tot_unclosed}")
```

DG-02 가 쓰는 새 경고 계산기 — Phase 2 계약이 고친 판 그대로다(줄 번호는 경로 뒤 첫 번째 숫자). 스크래치 폴더에
`cfg.markdownlint-cli2.jsonc` = `{ "config": { "MD013": false } }` (편집기 확장이 MD013 을 끈 것과 같은 조건), 계산기 옆 `node_modules` 는
`/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p1build/node_modules`
를 이어 쓴다 — 준비 단계 실측: 그 자리의 `.bin/markdownlint-cli2 --version` 첫 줄이 `markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)`
(2026-09-24 23:0x). 없으면 스크래치 폴더에 `npm install --no-save markdownlint-cli2@0.23.2` 부터 돌린다. 마크다운 린터가 확장자를 보므로
두 사본을 `.md` 이름으로 넘긴다:

```bash
#!/usr/bin/env bash
# new-warnings.sh <옛 파일> <새 파일> — 새 파일에서 더한 줄에 걸린 경고만 센다. 줄이 밀리므로 전체 수 차이로 세지 않는다
# 줄 번호는 경로 뒤 첫 번째 숫자다. 탐욕 매치(^[^ ]*:)로 뽑으면 열 번호가 줄 번호로 둔갑한다 (실측 2026-09-24)
set -u
DIR=$(cd "$(dirname "$0")" && pwd)
ADDED=$(git diff --no-index -U0 -- "$1" "$2" | awk '/^@@/{split($3,a,","); s=substr(a[1],2)+0; n=(a[2]==""?1:a[2]+0); for(i=0;i<n;i++) print s+i}' | sort -u)
OUT=$("$DIR/node_modules/.bin/markdownlint-cli2" --config "$DIR/cfg.markdownlint-cli2.jsonc" "$2" 2>&1)
LINES=$(printf '%s\n' "$OUT" | grep -E ':[0-9]+(:[0-9]+)? (error|warning) ' | sed -E 's#^([^:]*):([0-9]+).*#\2#' | sort -u)
NEWW=$(comm -12 <(printf '%s\n' "$ADDED" | grep . | sort) <(printf '%s\n' "$LINES" | grep . | sort) | wc -l | tr -d ' ')
echo "total_warning_lines=$(printf '%s\n' "$LINES" | grep -c .) added_lines=$(printf '%s\n' "$ADDED" | grep -c .) new_warnings=$NEWW"
```

SK-04 (d) 가 쓰는 삭제 열거 알려진 답 (`bash ka-del.sh` · `zsh ka-del.sh` — 두 셸에서 같은 출력이어야 한다. 임시 git 저장소를 만들어
커밋 하나로 `gone.txt` 를 지우고, 커밋하지 않은 채 `gone2.txt` 를 지우고 `README.md` 를 고치고 `NewDoc.md` 를 새로 만든다. 답은 구간 삭제
`gone.txt` 하나, 커밋하지 않은 삭제 `gone2.txt` 하나다. `naive` 는 「`D` 가 든 줄」 을 글자대로 읽은 `grep -c D` 가 경로의 대문자 `D`
까지 잡아 틀린 답 3 을 낸다는 대조다):

```bash
# ka-del.sh — 삭제 열거 두 명령의 알려진 답. 답: range=gone.txt worktree=gone2.txt
d=$(mktemp -d) && cd "$d" || exit 2
git init -q . && git config user.email t@t && git config user.name t
printf 'a\n' > README.md; printf 'x\n' > gone.txt; printf 'y\n' > gone2.txt
git add . && git commit -qm base && base=$(git rev-parse HEAD)
git rm -q gone.txt && git commit -qm del && top=$(git rev-parse HEAD)
rm gone2.txt; printf 'b\n' >> README.md; printf 'n\n' > NewDoc.md
r=$(git diff --name-status --diff-filter=D "$base..$top" | cut -f2 | tr '\n' ' ')
w=$(git status --porcelain | grep -E '^(D.|.D) ' | cut -c4- | tr '\n' ' ')
n=$(git status --porcelain | grep -c D)
echo "range=${r% } worktree=${w% } naive=$n"
cd / && rm -rf "$d"
```

봉인 전 실측 (초안 2026-09-24 22:4x ~ 23:0x · 검토 반영 뒤 23:4x ~ 23:5x 에 다시 잼 — 아래 표는 반영 뒤 값). 「편집 전」 값은 공통 정의에서 `END` 자리에 `$B` 를 넣은 것과 같은 사본(`T/X` = `T/X.0`,
`FX` 빈 파일)으로, 「모의본」 값은 스크래치
`/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p3draft/mock.py`
가 시작 커밋 판 네 파일에 개선안을 적용하고 새 fixture 를 쓴 사본으로 같은 측정을 돌린 값이다 (측정 묶음 `meas.sh` · `run.sh` · `fns.sh`,
같은 폴더). 버전 값 넷은 시작 커밋 판에서 읽었다 — `SV=1.6.0 AV=1.7.0 CV=v5.1 SCV=v5.5`:

```text
            편집 전                                        모의본
[SK-01a]    10 토큰 전부 0                                 10 토큰 전부 1
[SK-01b]    EV 머리말 0 · QG 제목 0 · 증거 유효성 절 안 0     1 · 1 · 1
[SK-01c]    9 토큰 전부 0                                  9 토큰 전부 1
[SK-01d]    0                                              1
[SK-02a]    6 토큰 전부 0                                  6 토큰 전부 1
[SK-02b]    0 · 0                                          1 · 1
[SK-03]     s4 0 · s7 0 · qg 0 · 번호 질문 2                s4 1 · s7 1 · qg 1 · 번호 질문 2
            감긴 질문 대조(모의본 사본): 질문 1 을 두 줄로 감은 사본 2 (옛 awk 는 1) · 감긴 질문 2 뒤에 셋째 질문을 붙인 사본 3 (옛 awk 는 2)
            제목 줄 대조(2 회차 검토 반영, 합성 입력): 질문 둘 뒤 제목 줄 · 들여쓴 번호 줄 — 불릿에서만 멈추는 판 3 · 고친 판 2
[SK-04a]    5 토큰 전부 0                                  5 토큰 전부 1
[SK-04b]    0 · 0 · 0                                      1 · 1 · 1
[SK-04c]    제목 0 · 6 토큰 전부 0                          제목 1 · 6 토큰 전부 1
[SK-04d]    EV 0 · QG 0                                    EV 1 · QG 1
            ka-del.sh: bash(5.3.9 · /bin/bash 3.2.57) · zsh 5.9 모두 range=gone.txt worktree=gone2.txt naive=3 · 종료 코드 0
[SK-05a]    5 토큰 전부 0                                  5 토큰 전부 1
[SK-05b]    제목 0 · 증거 유효성 절 안 0 · 4 토큰 전부 0      1 · 1 · 4 토큰 전부 1
[SK-05c]    0                                              1
[SK-06]     0                                              1
[ER-01]     0                                              0 · 양성 대조(example.invalid + 근거 안 URL 더한 사본) 1
[ER-02]     0                                              0 · 양성 대조(「훅에 의해 적용된다」 · 「그것에 대해 말한다」) UTF-8 2 · C 1
[AR-01a]    5요소 0 · 4요소 1 · 새 전제 0 · 빈 출력 0 · 상한 ref 0 · 파일 전체 4 요소 1     1 · 0 · 1 · 1 · 1 · 0
[AR-01b]    5요소 0 · 4요소 1 · 새 전제 0 · 커밋하고 나면 0 · v4 § 1 · 상한 ref 0 · 전체 1   1 · 0 · 1 · 1 · 0 · 1 · 0
[AR-01c]    옛 예시 1 · 새 예시 0                            0 · 1
[AR-02a]    머리 설정 0                                    2
[AR-02b]    (v5.5) 0 · (v5.3) 1 · 새 갱신 0 · 이전 0 · v5.5 스키마 0 · v5.3 스키마 1        1 · 0 · 1 · 1 · 1 · 0
[AR-02c]    gv 0 · 이전 0 · Parity with 0 · Schema link 0   1 · 1 · 1 · 1
[AR-02d]    1                                              0
[AR-03a]    (10 개 0 · 행 [1 2 3 4 5 11 12 14 15] · 9 행 · 제목 수 9 · 16 행 0)
                                                           (10 개 1 · [1 2 3 4 5 11 12 14 15 16] · 10 행 · 10 · 1)
[AR-03b]    0 · 0 · 0                                      1 · 1 · 1
[AR-04a]    키 넷 · 죽은 패턴 1 · vz2 Agent\(general-purpose\)   키 다섯(silent-check) · 0 · cross_diagnosis_by: pending-parent
[AR-04b]    fields_ng · notes3 0                           fields_ok · notes3 3
[AR-04c]    제목 0 · 항목 0                                 1 · 3
[AR-05]     same:12 same:40 same:62 same:82 rule2-same     같음 · 음성 대조(판정 규칙 1 항 문구 변이) 첫 값 diff
            removed:0 removed:0 removed:0 removed:0        같음 (네 구간 모두 더한 줄만 있다)
            음성 대조(모의본 사본): 판정 엄격도 규칙 1 굵은 글씨에 「 (경미하면 예외)」 → removed:1 · 0 · 0 · 0, 옛 측정은 same … rule2-same 그대로
                                   Red Flags 기존 줄 「"테스트가 전부 통과했으니 PASS"」 삭제 → removed:0 · 1 · 0 · 0
            added:0 added:0 added:0 evg-rest-same           added:2 added:2 added:3 evg-rest-same (2 회차 검토 반영)
            음성 대조: 판정 엄격도 규칙 1 아래 느슨한 줄 → added:3 · EVG 머리 뒤 느슨한 줄 → evg-rest-diff · Enforcement 넷째 행 → added:4
[AP-01]     0                                              0 · 양성 대조(9.9.9 · 1.6.0 더한 사본) 1
[AP-03]     bare 0 · unclosed 0                            0 · 0 · 양성 대조(언어 힌트 없는 펜스) 1
[AP-04]     1                                              1
[RE-02]     EV 8 · QG 27                                   8 · 27 · 양성 대조(표 하나 더한 사본) QG 28
[DG-02]     더한 줄 0                                      EV 0 · QG 0 · EI 0 (새 경고 줄) · 양성 대조: 굵은 글씨 줄 뒤 빈 줄을 뺀 평가자 사본 1 (MD032), 펜스 · 표를 더한 가이드 사본 2
[DG-05]     validate-plugin harness V1~V10 OK · check-stale-values 「되살아난 옛 값 없음」 exit 0 · sync-docs --check-only 0 · sync-evals --check-only 0 · run-evals 0
            모의본을 시작 커밋 판 스크래치 사본(`git archive` → `p3draft/rh`)에 얹어 돌려도 같음
            양성 대조: 같은 사본 평가자 끝에 언어 힌트 없는 펜스 → V6 `1 bare` · `FAIL harness/agents/qa-evaluator.md:1251`,
            가이드 Enforcement 표 중간에 문단을 끼운 사본 → V10 `1 broken table row(s)` · `FAIL harness/docs/guides/qa-evaluation-guide.md:201`
[DG-06]     15 checks — 12 PASS / 0 FAIL / 0 ERROR / 3 SKIP (scope-isolation PASS · doc-contracts PASS · docs-site-regen SKIP)
[DG-07]     l3-miss 3 · false-approve 6 · reject-loop 5 · vacuous-zero 7 · 0 (min 0 · n 5 — 지금 회귀 확인은 떨어진다)
                                                           3 · 7 · 5 · 7 · 1 · silent-check 2 · 1 · 1 (min 1 · n 8)
[bash-blocks] 더한 줄 가운데 셸 펜스를 여는 줄 0                  0
```

문장 삭제 대조 (러닝북 계약 규칙 — 특정 문장이 있어야 한다는 조건은 그 문장만 지운 사본에서 FAIL 이 나야 한다). 모의본에서 아래
문자열 하나만 지운 사본 48 개(`p3draft/del3.py` → `del3/<태그>/` — `del.py` 의 39 개 · 따로 만든 6 개 · 검토 반영으로 늘린 3 개)에
같은 측정을 돌렸다. 모의본 값은 전부 1 이상이고, 사본마다 아래 값만 떨어지고 다른 값은 모의본과 같다:

```text
태그        지운 곳 (EV = qa-evaluator.md · QG = 가이드 · FX = 새 fixture)                         떨어진 값
SK01a-1~9   EV 다섯 가지 문단의 ① · ② 러너 문장 · ③ 실패로 닫는 분기 · ④ · ⑤ 막는 검사 · ⑤ 알려진 답 · INVALID 문장 · FAIL 문장 ·
            ④ 고정 해석기 문장                                                                       SK-01a 둘째~열째 값이 각각 0
SK01c-1~9   QG 소절의 같은 아홉 문장 (① 줄 · ② 러너 줄 · ③ 분기 · ④ 줄 · ⑤ 막는 검사 · 알려진 답 줄 · 판정 줄 · FAIL 문장 ·
            ④ 고정 해석기 문장)
                                                                                                     SK-01c 해당 값이 각각 0
SK01d       EV Red Flags 「새 검사가 원본 대상에서 위반 0 을 냈으니 동작한다」                        0
SK02a       EV 틀의 `- ③ 못 읽는 칸 + 실제 위반:` 줄                                                 SK-02a 넷째 값 0
SK02b       EV Step 3.5 10 항 머리                                                                    SK-02b 첫 값 0
SK03-s4/s7/qg  둘째 질문에 붙인 문장 (틀 · Step 7 · 가이드) 하나씩                                    s4 · s7 · qg 각각 0 (번호 질문 2 그대로)
SK04a-1/3/4/5  EV 삭제 열거 머리 · 상태 칸 `porcelain` 문장 · unavailable 불릿 · 「FAIL 로 만들지 말고」 문장
                                                                                                     SK-04a 해당 값이 각각 0 (3 은 SK-04d 첫 값도 0)
SK04c-4/5/6 QG 「**FAIL 로 만들지 않고**」 불릿 · 「두 미검증 카운터 어디에도 합산하지 않는다」 · 상태 칸 `porcelain` 문장
                                                                                                     SK-04c 넷째 · 다섯째 · 여섯째 값 0 (6 은 SK-04d 둘째 값도 0)
SK05a-2~5   EV 낱말 필터 문장 · 「판정은 계약 측정 그대로다.」 · 관대해지는 쪽 문장 · 두 값 문장       SK-05a 둘째~다섯째 값이 각각 0
SK05b-1/2/4 QG 순서 2 항 · 3 항 첫 줄 · 4 항 두 값 줄                                                 SK-05b 해당 값 0 (3 항 줄은 둘째 · 셋째 값 함께 0)
SK05c       EV Red Flags 「매치된 줄이 금지 조항이니」                                                0
SK06        EV `Evaluated:` 줄 끝 주석                                                               0
AR01a-3/4   EV Step 1.5 새 상태 전제 · 빈 출력 문장                                                   AR-01a 셋째 · 넷째 값 0
AR01b-3/4   QG 6 항 새 상태 전제 줄 · 빈 출력 줄                                                      AR-01b 셋째 · 넷째 값 0
AR01c       QG 새 예시                                                                                AR-01c 둘째 값 0
AR03a-16    QG Parity 16 행                                                                           16 행 0 · 행 수 9 ≠ 제목 수 10
AR03b-2     QG Enforcement 매치 줄 가르기 행                                                          AR-03b 둘째 값 0
AR04b       FX 교차 진단 메모의 「첫 칸만 읽는 검사, 」                                               notes3 2
```

ER-03 가짜 notes 대조 (`p3draft/fake-notes.md` — 열두 문자열을 한 줄에 하나씩): 열둘 전부 1, 한 줄씩 지운 사본 열한 개에서 그 값만 0.
ER-03 셋째 측정 정규식 대조 (검토 반영): 빈 목록 0, 한 줄 목록 `.harness/.meta/orchestrator-audit-log.md` · `.harness/.meta/kaizen-failure-count.yaml` ·
`.harness/project.yaml` · `harness/skills/sprint/SKILL.md` 각각 1, 이 Phase 파일 여덟 줄 목록 0.

검토 전 예행 (계약 본문 그대로, 2026-09-24 23:1x): 작업 폴더를 스크래치에 복제(`p3draft/rehearse.sh` → `rh2`)해 BUILD 를 흉내 냈다 —
이 계약을 봉인해 커밋(`SEAL_OK`) · 모의본 다섯 파일 커밋 · 서명 없는 다른 Phase 커밋(`.harness/` 한 파일, 본문에 서명 글자를 인용만) ·
`end_sha` 커밋 · 가짜 notes 커밋 · 그 sha 를 적은 `end_sha` 커밋. 서명 줄 커밋에는 `Co-Authored-By` 줄 바로 위에 서명 줄을 넣었다.
위 코드 블록 넷(그때는 `ka-del.sh` 가 없었다)을 이 계약에서 기계로 떼어 내고(`cd` 줄만 복제본으로 바꿈) 28 조건의 측정을 조건 문구 그대로 돌렸다
(`p3draft/r.sh`, 결과 `r-values.txt`) — 28 조건 전부 요구값. `my` 는 다섯 파일 · 계약 · 개정 · notes 여덟 줄(서명 없는 다른 Phase
커밋의 파일은 빠짐), AR-06 ① 0 · ② 0 · 5 · ③ `SEAL_OK 53 · SEAL_ABSENT 10` · 이 Phase 몫 0, ER-03 12 값 전부 1 · 넘김 대상 0,
DG-05 `V1` · `V6` · `V10` OK · check-stale-values exit 0 · sync-docs · run-evals 0, DG-06 `scope-isolation` PASS (6 commits) ·
`doc-contracts` PASS · `docs-site-regen` FAIL(Final 몫 — 판정에서 뺀 줄), DG-07 `min 1 n 8`. AR-06 ① 음성 대조: 서명 없는 커밋이
가이드를 건드리게 하고 `end_sha` 를 그 커밋 뒤로 옮기면 1. ER-03 둘째 값 음성 대조: 가짜 목록 `harness/skills/sprint/SKILL.md` 로 1.

검토 반영 뒤 예행 (2026-09-24 23:4x, 계약 본문 그대로): 같은 흉내(`p3draft/rehearse2.sh` → `rh3`)를 검토를 반영한 이 계약과 고친
모의본으로 다시 돌렸다. 코드 블록을 다섯(`ka-del.sh` 포함)으로 떼어 냈고, 28 조건의 측정을 고친 문구 그대로 돌렸다(`p3draft/r2.sh`,
결과 `r2-values.txt`) — 28 조건 전부 요구값. 바뀐 조건의 값: SK-01 (a) 10 값 · (c) 9 값 전부 1, SK-03 `1 1 1 2`, SK-04 (a) 5 · (b) 3 ·
(c) 제목 1 · 6 값 전부 1 · (d) `1 1` · `ka-del.sh` bash · zsh 둘 다 `range=gone.txt worktree=gone2.txt naive=3` 종료 코드 0, ER-03 셋째 0,
AR-05 `same:12 same:40 same:62 same:82 rule2-same` · `removed:0` 넷, AR-06 ① 0 · ② 0 · 5 · ③ `SEAL_OK 53 · SEAL_ABSENT 10` · 이 Phase
몫 0 · 이 계약 `SEAL_OK`. 나머지 조건 값은 첫 예행과 같다(DG-02 가이드 더한 줄 130 · 새 경고 0).

검토 반영 (`.harness/.meta/kaizen-0924/phase3-review.md` `VERDICT: CHANGES`):

- 막는 이유 1 SK-04 — 모의본 두 파일의 삭제 열거 문구를 「`git status --porcelain` 줄의 앞 두 글자(상태 칸)에 `D` 가 있는 줄」 과
  `grep -E '^(D.|.D) '` 로 고쳤다. SK-04 (a) 셋째 토큰 교체 · (c) 여섯째 토큰 · (d) 알려진 답(`ka-del.sh`) 을 더했다
- 막는 이유 2 AR-05 — 판정 엄격도 · Red Flags · Evidence Validity Gate · Enforcement 등급 구간의 `removed:0` 측정을 더했다. 이름은 검토
  제안의 `kept:` 대신 `removed:` 로 적었다 — 세는 것이 옛 구간에만 있는 줄이라 이름이 뜻과 맞게
- 막는 이유 3 SK-01 — ④ 끝에 고정 해석기 문장을 두 파일에 더하고 SK-01 열째 토큰으로 잰다. `GAP 분석` 에 호환성 선택을 넷째로 적었다
- 막는 이유 4 ER-03 — 셋째 측정 정규식에 `.harness/` 공유 파일 셋을 더하고 `범위 경계` 공유 파일 줄에 이름을 적었다
- 권고 — AR-06 ③ 에 이 계약 `SEAL_OK` 추가 · SK-03 awk 를 다음 불릿까지 세는 꼴로 교체 · `[bash-blocks]` 는 「권고」 로 표시 ·
  삭제 열거에 다른 세션 삭제 한 마디 · 근거 파일 §4 권장안 11 과 다른 선택을 `GAP 분석` 다섯째로 · 가이드 「두 사이클에 걸쳐」 →
  「두 번」(감사 로그 원문 「2 회째 관측」) · L3 Coverage Honesty 실측과 F31 UI 부분을 notes 지시에 · ⑤ 끝에 「임시 사본에서만 돌아
  규칙 12 (3) 안전 조건과 무관」 한 문장 (두 파일)

2 회차 검토 반영 (`.harness/.meta/kaizen-0924/phase3-review.md` `## 2 회차` · `VERDICT: APPROVE`, BUILD 가 봉인 전에):

- 권고 1 AR-05 — 줄을 더해서 느슨하게 만드는 편집을 잡게 조건 문장 끝에 더하는 줄의 자리 · 수를 적고, 측정 끝에 검토가 준 셋째
  측정(`added:` 셋 · `evg-rest-`)을 그대로 이었다. 모의본 판 개선안 문구는 바꾸지 않았다 — 모의본이 이미 그 수(2 · 2 · 3)다.
  봉인 전 실측은 AR-05 줄과 위 표 (`p3build/pre-ar05.sh` — 편집 전 · 모의본 · 음성 대조 셋)
- 권고 2 — `범위 경계` 사용자 승인 대체 줄에 2 회차 판정을 적었다
- 권고 3 SK-03 — `awk` 의 멈춤 조건을 `f&&/^(-|#)/{f=0}` 로 바꿨다. 편집 전 · 모의본 값은 그대로 2, 제목 줄 합성 입력에서 옛 판 3 · 새 판 2
- 조건 줄 수 · 기능 조건 수는 그대로다(28 · 18). 바뀐 조건 줄은 AR-05 하나 · 측정 문구가 바뀐 조건은 SK-03 · AR-05 둘

## Skill

- [ ] SK-01: 산출물이 검사일 때 평가자가 임시 사본으로 돌리는 확인 목록 한 벌(다섯 가지)이 평가자 규칙 10 과 평가 가이드에 들어간다 (harness:P04 · user-setup:P4 (a)~(c) · F16 · F31 측정 스크립트 부분 · 러닝북 Phase 3 과제) — (a) `qa-evaluator.md` §판정 엄격도 구간에 10 토큰 `평가자가 사본 입력으로 직접 돌리는 다섯 가지` · `위반을 둘째 이후 칸에만 둔 사본` · `이름을 찍지 않는 러너면 수집 명령 출력에서` · `모든 칸을 읽어야만 안전한 검사면` · `zsh · bash 양쪽에서 돌려 읽은 대상 수가 같고` · `막는 검사는 알려진 위반에서 실패를 내야` · `` 계약에 `알려진 답:` 절이 있으면 그 입력부터 다시 돌린다 `` · `다섯 가지를 돌리지 않았거나 기록이 없으면` · `결함이 드러나면 그 검사를 대상으로 한 조건은 **FAIL**` · `해석기가 정해진 스크립트` 가 각각 1 건 (b) 한 벌만 — 첫 토큰이 `qa-evaluator.md` 전체에서 1 건이고, 가이드에 `### 산출물이 검사일 때` 로 시작하는 제목이 정확히 1 개이며 `## Evidence Validity Gate` 구간 안에 있다 (c) 그 가이드 소절에 (a) 의 둘째~열째 토큰 9 개가 각각 1 건 이상 (d) `qa-evaluator.md` §Red Flags 에 `새 검사가 원본 대상에서 위반 0 을 냈으니 동작한다` 1 건 [exact, enumerated]
      (측정: (a) `toks "$(sect "$T/EV" '### 판정 엄격도')" '평가자가 사본 입력으로 직접 돌리는 다섯 가지' '위반을 둘째 이후 칸에만 둔 사본' '이름을 찍지 않는 러너면 수집 명령 출력에서' '모든 칸을 읽어야만 안전한 검사면' 'zsh · bash 양쪽에서 돌려 읽은 대상 수가 같고' '막는 검사는 알려진 위반에서 실패를 내야' '계약에 `알려진 답:` 절이 있으면 그 입력부터 다시 돌린다' '다섯 가지를 돌리지 않았거나 기록이 없으면' '결함이 드러나면 그 검사를 대상으로 한 조건은 **FAIL**' '해석기가 정해진 스크립트'` 10 값 전부 1
       (b) `grep -cF '평가자가 사본 입력으로 직접 돌리는 다섯 가지' "$T/EV"` 1 · `grep -cE '^### 산출물이 검사일 때' "$T/QG"` 1 · `sect "$T/QG" '## Evidence Validity Gate' | grep -cE '^### 산출물이 검사일 때'` 1
       (c) `toks "$(sect "$T/QG" '### 산출물이 검사일 때')" '위반을 둘째 이후 칸에만 둔 사본' '이름을 찍지 않는 러너면 수집 명령 출력에서' '모든 칸을 읽어야만 안전한 검사면' 'zsh · bash 양쪽에서 돌려 읽은 대상 수가 같고' '막는 검사는 알려진 위반에서 실패를 내야' '계약에 `알려진 답:` 절이 있으면 그 입력부터 다시 돌린다' '다섯 가지를 돌리지 않았거나 기록이 없으면' '결함이 드러나면 그 검사를 대상으로 한 조건은 **FAIL**' '해석기가 정해진 스크립트'` 9 값 전부 1 이상
       (d) `sect "$T/EV" '## Red Flags' | grep -cF '새 검사가 원본 대상에서 위반 0 을 냈으니 동작한다'` 1.
       봉인 전 실측: 편집 전 전부 0, 모의본 전부 1. 문장 삭제 대조: 평가자 문장 아홉 · 가이드 문장 아홉 · Red Flags 한 줄을 하나씩 지운 사본에서 해당 값이 각각 0 — `회귀 게이트` 절 표. 열째 토큰은 검토가 짚은 호환성 — 해석기가 정해진 옛 계약의 스크립트를 zsh 로 돌려 떨어뜨리지 않는다(`GAP 분석` 넷째 선택))
- [ ] SK-02: 리포트 형식에 `Check Artifacts` 블록이 들어가고 verdict 직전 self-check 가 그 블록과 삭제 블록을 확인한다 (harness:P04 · F16) — (a) `qa-evaluator.md` Step 4 구간에 `## Check Artifacts (산출물이 검사인 조건만 — 규칙 10)` · `- ① 첫 칸만:` · `- ② 실행 목록:` · `- ③ 못 읽는 칸 + 실제 위반:` · `- ④ zsh · bash:` · `- ⑤ 효과 증명:` 이 각각 1 건 (b) Step 3.5 구간에 `10. **검사 산출물 · 삭제 self-check**` 1 건 · `(a) 가 빈 조건의 PASS 는` 1 건 [exact, enumerated]
      (측정: (a) `toks "$S4" '## Check Artifacts (산출물이 검사인 조건만 — 규칙 10)' '- ① 첫 칸만:' '- ② 실행 목록:' '- ③ 못 읽는 칸 + 실제 위반:' '- ④ zsh · bash:' '- ⑤ 효과 증명:'` 6 값 전부 1 (b) `toks "$(sect "$T/EV" '### Step 3.5')" '10. **검사 산출물 · 삭제 self-check**' '(a) 가 빈 조건의 PASS 는'` 1 · 1.
       봉인 전 실측: 편집 전 전부 0, 모의본 전부 1. 문장 삭제 대조: `- ③` 줄만 지운 사본 (a) 넷째 값 0, 10 항 머리만 지운 사본 (b) 첫 값 0)
- [ ] SK-03: 교차 진단 둘째 질문이 세 자리에서 같은 문구로 넓어지고 질문 수는 둘 그대로다 (F31 독립 검토 · Counterpart `harness/skills/sprint/SKILL.md:118` 「물을 두 가지」) — `다섯 가지 가운데 돌리지 않은 것이 있는가` 가 `qa-evaluator.md` Step 4 구간 · Step 7 구간 · 가이드 `### 교차 진단 프로토콜` 구간에 각각 1 건이고, Step 4 구간 `부모가 물을 두 가지:` 아래(다음 불릿 전까지) 번호 질문 줄이 2 개다 [exact, enumerated]
      (측정: `printf '%s\n' "$S4" | grep -cF '다섯 가지 가운데 돌리지 않은 것이 있는가'` 1 · `sect "$T/EV" '### Step 7' | grep -cF '다섯 가지 가운데 돌리지 않은 것이 있는가'` 1 · `sect "$T/QG" '### 교차 진단 프로토콜' | grep -cF '다섯 가지 가운데 돌리지 않은 것이 있는가'` 1 · `printf '%s\n' "$S4" | awk '/부모가 물을 두 가지/{f=1;next} f&&/^(-|#)/{f=0} f&&/^ +[0-9]+\./{n++} END{print n+0}'` 2 (다음 불릿 줄이나 제목 줄에서 멈추고, 감긴 이어짐 줄은 세지도 멈추지도 않는다).
       봉인 전 실측: 편집 전 0 · 0 · 0 · 2, 모의본 1 · 1 · 1 · 2. 문장 삭제 대조: 세 자리의 붙인 문장을 하나씩 지운 사본에서 해당 값만 0, 번호 질문 2 그대로. 감긴 질문 대조: 질문 1 을 두 줄로 감은 사본 2 · 감긴 질문 2 뒤에 셋째 질문을 붙인 사본 3 — 첫 판 awk(번호 줄 아닌 줄에서 멈춤)는 1 · 2 를 내 두 경우를 거꾸로 판정했다. 제목 줄 대조(2 회차 검토 반영): 질문 둘 뒤에 `## Deletions` 제목 줄과 공백 셋으로 들여쓴 번호 줄 `3. 다른 목록` 이 오는 합성 입력에서 불릿에서만 멈추는 판은 3, 고친 판은 2 · 편집 전 · 모의본은 두 판 모두 2)
- [ ] SK-04: 변경 범위에서 지운 파일을 평가자가 뽑아 리포트에 올리고, 재는 조건이 없으면 FAIL 이 아니라 사용자 확인으로 올린다 (user-setup:P4 (d) · F31 삭제 목록) — (a) `qa-evaluator.md` Step 2 구간에 5 토큰 `**삭제 열거 (구현 판정마다 · 2026-09-24 신규):**` · `--diff-filter=D` · `` 앞 두 글자(상태 칸)에 `D` 가 있는 줄 `` · `deletions_range: unavailable (계약에 기준 커밋 없음)` · `재는 조건이 없는데 선언 밖 삭제가 있으면 FAIL 로 만들지 말고` 가 각각 1 건 (b) Step 4 구간에 `## Deletions` · `- deletions_range:` · `- 선언 밖 삭제:` 각 1 건 (c) 가이드에 `## 삭제 열거` 로 시작하는 제목이 정확히 1 개이고 그 절에 6 토큰 `--diff-filter=D` · `git-scm.com/docs/git-diff` · `deletions_range: unavailable` · `**FAIL 로 만들지 않고**` · `두 미검증 카운터 어디에도 합산하지 않는다` · `` 앞 두 글자(상태 칸)에 `D` 가 있는 줄 `` 가 각각 1 건 이상 (d) 두 파일의 해당 구간(평가자 `### Step 2` · 가이드 `## 삭제 열거`)에 `` grep -E '^(D.|.D) ' `` 가 각각 1 건 이상이고, `회귀 게이트` 절의 `ka-del.sh` 를 `bash ka-del.sh` · `zsh ka-del.sh` 로 돌린 출력이 둘 다 `range=gone.txt worktree=gone2.txt naive=3` 이다 — 규칙이 가르치는 명령이 답을 아는 입력에서 맞는 답을 낸다 [exact, enumerated]
      (측정: (a) ``toks "$(sect "$T/EV" '### Step 2')" '**삭제 열거 (구현 판정마다 · 2026-09-24 신규):**' '--diff-filter=D' '앞 두 글자(상태 칸)에 `D` 가 있는 줄' 'deletions_range: unavailable (계약에 기준 커밋 없음)' '재는 조건이 없는데 선언 밖 삭제가 있으면 FAIL 로 만들지 말고'`` 5 값 전부 1 (b) `toks "$S4" '## Deletions' '- deletions_range:' '- 선언 밖 삭제:'` 1 · 1 · 1 (c) `grep -cE '^## 삭제 열거' "$T/QG"` 1 · `toks "$(sect "$T/QG" '## 삭제 열거')" '--diff-filter=D' 'git-scm.com/docs/git-diff' 'deletions_range: unavailable' '**FAIL 로 만들지 않고**' '두 미검증 카운터 어디에도 합산하지 않는다' '앞 두 글자(상태 칸)에 `D` 가 있는 줄'` 6 값 전부 1 이상
       (d) ``sect "$T/EV" '### Step 2' | grep -cF "grep -E '^(D.|.D) '"`` 1 이상 · ``sect "$T/QG" '## 삭제 열거' | grep -cF "grep -E '^(D.|.D) '"`` 1 이상 · `회귀 게이트` 절 `ka-del.sh` 를 파일로 저장해 `bash ka-del.sh` 와 `zsh ka-del.sh` 가 둘 다 `range=gone.txt worktree=gone2.txt naive=3` · 종료 코드 0.
       봉인 전 실측: 편집 전 전부 0, 모의본 전부 1. ka-del.sh 는 bash 5.3.9 · /bin/bash 3.2.57 · zsh 5.9 셋 다 요구값 — `naive=3` 은 첫 판 문구 「`D` 가 든 줄」 을 글자대로 읽으면 `README.md` · `NewDoc.md` 까지 잡는다는 대조다(검토가 찾은 결함). 문장 삭제 대조: 평가자 머리 · 상태 칸 `porcelain` 문장 · unavailable 불릿 · 「FAIL 로 만들지 말고」 문장, 가이드 「FAIL 로 만들지 않고」 불릿 · 카운터 불릿 · 상태 칸 `porcelain` 문장을 하나씩 지운 사본에서 해당 값이 각각 0 — 두 `porcelain` 문장 사본은 (d) 의 그 파일 값도 0)
- [ ] SK-05: 0 이 기대값인 측정에 매치가 나오면 줄마다 가르고, 낱말 필터를 금지하고, 판정은 계약 측정 그대로 둔다 (러닝북 Phase 3 과제 — 지난 사이클 메타 이슈 3) — (a) `qa-evaluator.md` §판정 엄격도 구간에 5 토큰 `**0 이 기대값인데 매치가 나오면 줄마다 가른다` · `` `grep -v '금지'` `` · `판정은 계약 측정 그대로다` · `관대해지는 쪽으로 측정을 바꾸지 않는다` · `지금 대상에서 0, 알려진 위반을 넣은 임시 사본에서 1 이상` 이 각각 1 건 (b) 가이드에 `### 0 이 기대값인데 매치가 나올 때` 로 시작하는 제목이 정확히 1 개이고 `## Evidence Validity Gate` 구간 안에 있으며, 그 소절에 4 토큰 `**낱말로 거르는 필터로 매치를 빼지 마라**` · `**판정은 계약 측정 그대로다.**` · `판정이 관대해지는 쪽으로 측정을` · `지금 대상에서 0, 알려진 위반을 넣은 임시 사본에서 1 이상` 이 각각 1 건 이상 (c) `qa-evaluator.md` §Red Flags 에 `매치된 줄이 금지 조항이니` 1 건 [exact, enumerated]
      (측정: (a) ``toks "$(sect "$T/EV" '### 판정 엄격도')" '**0 이 기대값인데 매치가 나오면 줄마다 가른다' "\`grep -v '금지'\`" '판정은 계약 측정 그대로다' '관대해지는 쪽으로 측정을 바꾸지 않는다' '지금 대상에서 0, 알려진 위반을 넣은 임시 사본에서 1 이상'`` 5 값 전부 1 (b) `grep -cE '^### 0 이 기대값인데 매치가 나올 때' "$T/QG"` 1 · `sect "$T/QG" '## Evidence Validity Gate' | grep -cE '^### 0 이 기대값인데 매치가 나올 때'` 1 · `toks "$(sect "$T/QG" '### 0 이 기대값인데 매치가 나올 때')" '**낱말로 거르는 필터로 매치를 빼지 마라**' '**판정은 계약 측정 그대로다.**' '판정이 관대해지는 쪽으로 측정을' '지금 대상에서 0, 알려진 위반을 넣은 임시 사본에서 1 이상'` 4 값 전부 1 이상 (c) `sect "$T/EV" '## Red Flags' | grep -cF '매치된 줄이 금지 조항이니'` 1.
       봉인 전 실측: 편집 전 전부 0, 모의본 전부 1. 문장 삭제 대조: 평가자 넷 · 가이드 셋 · Red Flags 한 줄을 하나씩 지운 사본에서 해당 값이 각각 0. 판정 임계가 그대로인지는 AR-05)
- [ ] SK-06: 리포트의 `Evaluated` 시각을 `date` 출력으로 채우게 한다 (harness:P08 평가자 쪽 — Phase 2 넘김) — `qa-evaluator.md` Step 4 구간에서 `Evaluated:` 로 시작하는 줄이 `date '+%Y-%m-%d %H:%M'` 를 담는다 (1 줄) [exact]
      (측정: `printf '%s\n' "$S4" | grep -E '^Evaluated:' | grep -cF "date '+%Y-%m-%d %H:%M'"` 1. 봉인 전 실측: 편집 전 0 · 모의본 1. 문장 삭제 대조: 줄 끝 주석만 지운 사본 0)

## Script

- [ ] SC-00: N/A (Script 카테고리는 `release.sh` 연동 · 버전 올림 · `marketplace.json` 갱신이다. 이 Phase 는 그 파일을 건드리지 않는다 — 공유 파일은 Final 몫. 측정: `my | grep -cE '^(scripts/release\.sh|\.claude-plugin/marketplace\.json|[^/]+/\.claude-plugin/plugin\.json)$'` 이 0)

## Error

- [ ] ER-01: 다섯 파일에 새로 생긴 URL 이 전부 이 Phase 의 외부 근거 파일 `.harness/.meta/evidence/phase3.md` 에 있다 — 근거 밖 자료를 인용하지 않았다 [exact, enumerated]
      (측정: `comm -23 <(comm -13 <(cat "$T"/EV.0 "$T"/QG.0 "$T"/EI.0 "$T"/AS.0 | url) <(cat "$T"/EV "$T"/QG "$T"/EI "$T"/AS "$T"/FX | url)) <(url < "$EVID") | grep -c .` 0.
       봉인 전 실측: 편집 전 0 · 모의본 0 (새 URL 넷 `cwe.mitre.org/data/definitions/20.html` · `…/754.html` · `git-scm.com/docs/git-diff` · `zsh.sourceforge.io/Doc/Release/Expansion.html` 전부 근거 파일에 있음). 양성 대조: 모의본 가이드 끝에 `https://example.invalid/x` 와 근거 안 URL 하나를 더하면 1)
- [ ] ER-02: 다섯 파일에 더한 줄에 번역투 6 종(`tone-kit/references/locale-korean.md` §2 치환표의 grep 열)이 0 건이다 [exact]
      (측정: `added | grep -cE "$K02"` 0. 양성 대조: 모의본 가이드에 「이 값은 훅에 의해 적용된다.」 · 「그것에 대해 말한다.」 두 줄을 더하면 2 — 봉인 전 실측 UTF-8 2 · C 로케일 1. 1 이 나오면 로케일이 틀린 것이라 측정 무효)
- [ ] ER-03: 이 Phase 범위 밖 반대편을 명시적 미완으로 넘기고 건드리지 않는다 — `.harness/.meta/kaizen-0924/phase3-notes.md` 에 열두 문자열 `harness:P04` · `user-setup:P4` · `F16` · `F31` · `harness:P08` · `메타 이슈 3` · `skill-design-guide.md §3.7 ①~④` · `contract-schema.md ①~④` · `assertions.json 실행기` · `.github/workflows/ci.yml` · `docs/harness/qa-evaluation-guide.html` · `harness/skills/sprint/SKILL.md:118` 이 각각 1 회 이상 있고, 이 Phase 커밋이 넘김 대상 · 다른 Phase 소관 파일 · 러닝북이 금지한 `.harness/` 안 공유 파일(감사 로그 · 실패 횟수 파일 · `project.yaml`)을 하나도 건드리지 않는다 [exact, enumerated]
      (Given: BUILD 가 notes 를 쓰고 커밋한 뒤 · 측정: `test -f .harness/.meta/kaizen-0924/phase3-notes.md` exit 0 ·
       `for t in 'harness:P04' 'user-setup:P4' 'F16' 'F31' 'harness:P08' '메타 이슈 3' 'skill-design-guide.md §3.7 ①~④' 'contract-schema.md ①~④' 'assertions.json 실행기' '.github/workflows/ci.yml' 'docs/harness/qa-evaluation-guide.html' 'harness/skills/sprint/SKILL.md:118'; do printf '%s ' "$(git show "$END:.harness/.meta/kaizen-0924/phase3-notes.md" | grep -cF -- "$t")"; done` 12 값 전부 1 이상 ·
       `my | grep -cE '^(harness/docs/guides/(skill|agent|contract)-design-guide\.md|harness/references/|harness/skills/|harness/scripts/|harness/evals/kaizen/contract-kaizen/|\.github/|docs/|scripts/|\.harness/\.meta/(orchestrator-audit-log\.md|kaizen-failure-count\.yaml)$|\.harness/project\.yaml$)'` 0.
       봉인 전 실측: notes 없음 — 구현이 만들 파일이라 면제. 열두 문자열을 한 줄에 하나씩 담은 가짜 notes(`p3draft/fake-notes.md`)로 돌리면 12 값 전부 1, 한 줄씩 지운 사본에서 그 값만 0. `my` 가 빈 목록이라 셋째 측정 0 — 가짜 목록 한 줄씩 `harness/skills/sprint/SKILL.md` · `.harness/.meta/orchestrator-audit-log.md` · `.harness/.meta/kaizen-failure-count.yaml` · `.harness/project.yaml` 은 각각 1, 이 Phase 파일 여덟 줄(계약 · 개정 · notes · 검토 · QA 피드백 · 평가자 · 가이드 · `assertions.json`) 목록은 0 — `.harness/` 공유 파일 세 이름은 검토가 짚어 더했다)

## Architecture

- [ ] AR-01: Diff-Scope 표준형이 평가자 두 자리에서 5 요소로 맞고, 커밋하고 나면 빈 출력이 되는 상태 전제의 0 을 공허한 0 으로 보며, 옛 `--cached` 권고 예시가 사라진다 (Phase 2 넘김 — 스키마 v5.5 §Diff-Scope Oracle 표준형) — (a) `qa-evaluator.md` Step 1.5 구간에 `표준형 5 요소` 1 · `표준형 4 요소` 0 · `Given: 이 스프린트의 커밋이 끝난 뒤` 1 · `커밋하고 나면 빈 출력` 1 · `상한 ref` 1, 파일 전체 `4 요소` 0 (b) 가이드 `## Binary Decidability Pre-Check` 구간에 `표준형 5 요소` 1 · `표준형 4 요소` 0 · `Given: 이 스프린트의 커밋이 끝난 뒤` 1 · `커밋하고 나면` 1 · `contract-schema v4 §Diff-Scope` 0 · `상한 ref` 1, 가이드 전체 `표준형 4 요소` 0 (c) 가이드 `### Recurring Improvement Escalation` 구간에 옛 예시 `` `Given: 스테이징 완료 후` 를 붙이고 `--cached` 를 쓸 것 `` 0 · 새 예시 `` `Given: 이 스프린트의 커밋이 끝난 뒤` 를 붙이고 `<base>..<상한>` 구간으로 잴 것 `` 1 [exact, enumerated]
      (측정: (a) `toks "$(sect "$T/EV" '### Step 1.5')" '표준형 5 요소' '표준형 4 요소' 'Given: 이 스프린트의 커밋이 끝난 뒤' '커밋하고 나면 빈 출력' '상한 ref'` 1 · 0 · 1 · 1 · 1 · `grep -cF '4 요소' "$T/EV"` 0
       (b) `toks "$(sect "$T/QG" '## Binary Decidability Pre-Check')" '표준형 5 요소' '표준형 4 요소' 'Given: 이 스프린트의 커밋이 끝난 뒤' '커밋하고 나면' 'contract-schema v4 §Diff-Scope' '상한 ref'` 1 · 0 · 1 · 1 · 0 · 1 · `grep -cF '표준형 4 요소' "$T/QG"` 0
       (c) ``toks "$(sect "$T/QG" '### Recurring Improvement Escalation')" '`Given: 스테이징 완료 후` 를 붙이고 `--cached` 를 쓸 것' '`Given: 이 스프린트의 커밋이 끝난 뒤` 를 붙이고 `<base>..<상한>` 구간으로 잴 것'`` 0 · 1.
       봉인 전 실측: 편집 전 (a) 0 · 1 · 0 · 0 · 0 · 1 (b) 0 · 1 · 0 · 0 · 1 · 0 · 1 (c) 1 · 0 — 옛 문구가 편집 전 파일에서 1 이라 측정이 살아 있다. 모의본 (a) 1 · 0 · 1 · 1 · 1 · 0 (b) 1 · 0 · 1 · 1 · 0 · 1 · 0 (c) 0 · 1. 문장 삭제 대조: 두 자리의 새 상태 전제 · 빈 출력 문장, 새 예시를 하나씩 지운 사본에서 해당 값이 각각 0)
- [ ] AR-02: 버전 표기가 서로 맞는다 (Phase 2 넘김 · 근거 파일 §3 현행화) — (a) 가이드 머리 설정이 `version: v5.1` · `last_updated: 2026-09-24` (b) 가이드 전체에 `` `harness/references/contract-schema.md` (v5.5) `` 1 · 같은 꼴 `(v5.3)` 0 · `> **최근 갱신: 2026-09-24 (Phase 3 kaizen · v5.1)**` 1 · `> 이전 (2026-08-13, v5.0):` 1 · `— Sprint Contract v5.5 스키마 (` 1 · `v5.3 스키마` 0 (c) 가이드 §버전 정보 에 `- **Guide version**: 2026-09-24 (Phase 3 kaizen · v5.1 ` 로 시작하는 줄 1 · `- 이전: 2026-08-13 (Phase 3 kaizen · v5.0` 1, `- **Parity with**:` 줄이 `$END` 판 세 설계 가이드 머리 설정 `version` 을 `skill-design-guide {값} · agent-design-guide {값} · contract-design-guide {값}` 꼴로 담고, `- **Schema link**:` 줄이 `$END` 판 스키마 `현재:` 값을 `contract-schema.md {값} ` 꼴로 담는다 (d) `qa-evaluator.md` 에 `계약 작성 가이드 v4` 0 [exact, enumerated]
      (측정: (a) `head -5 "$T/QG" | grep -cE '^(version: v5\.1|last_updated: 2026-09-24)$'` 2
       (b) ``toks "$(cat "$T/QG")" '`harness/references/contract-schema.md` (v5.5)' '`harness/references/contract-schema.md` (v5.3)' '> **최근 갱신: 2026-09-24 (Phase 3 kaizen · v5.1)**' '> 이전 (2026-08-13, v5.0):' '— Sprint Contract v5.5 스키마 (' 'v5.3 스키마'`` 1 · 0 · 1 · 1 · 1 · 0
       (c) `VI=$(sect "$T/QG" '### 버전 정보')` 뒤 `printf '%s\n' "$VI" | grep -cE '^- \*\*Guide version\*\*: 2026-09-24 \(Phase 3 kaizen · v5\.1 '` 1 · `printf '%s\n' "$VI" | grep -cF -- '- 이전: 2026-08-13 (Phase 3 kaizen · v5.0'` 1 · `printf '%s\n' "$VI" | grep -F -- '- **Parity with**:' | grep -cF "skill-design-guide $SV · agent-design-guide $AV · contract-design-guide $CV"` 1 · `printf '%s\n' "$VI" | grep -F -- '- **Schema link**:' | grep -cF "contract-schema.md $SCV "` 1
       (d) `grep -cF '계약 작성 가이드 v4' "$T/EV"` 0.
       봉인 전 실측: 시작 커밋 판 값 `SV=1.6.0 AV=1.7.0 CV=v5.1 SCV=v5.5`. 편집 전 (a) 0 (b) 0 · 1 · 0 · 0 · 0 · 1 (c) 0 · 0 · 0 · 0 (d) 1. 모의본 (a) 2 (b) 1 · 0 · 1 · 1 · 1 · 0 (c) 1 · 1 · 1 · 1 (d) 0)
- [ ] AR-03: 새 원칙이 가이드의 두 표에 행으로 들어간다 — (a) `### Parity Table` 제목에 `(10 개 parity item`, 표 행 번호가 정확히 `1 2 3 4 5 11 12 14 15 16`, 행 수가 제목의 수와 같고, 16 행이 `알려진 답 대조` 와 `§산출물이 검사일 때` 를 담는다 (Phase 2 넘김 · Cross-Surface Parity) (b) `## 원칙별 Enforcement 등급` 표에 행 `| **산출물이 검사일 때 다섯 가지** | **E2 (신규)** |` · `| **0 기대 측정의 매치 줄 가르기** | **E2 (신규)** |` · `| **삭제 열거** | **E1 (신규)** |` 가 각각 1 건 (가이드 개정 체크리스트 「새 원칙에 Enforcement 등급을 부여했는가」) [exact, enumerated]
      (측정: (a) `PT=$(sect "$T/QG" '### Parity Table')` 뒤 `printf '%s\n' "$PT" | head -1 | grep -cF '(10 개 parity item'` 1 · `printf '%s\n' "$PT" | grep -oE '^\| [0-9]+ \|' | tr -dc '0-9\n' | tr '\n' ' '` 이 `1 2 3 4 5 11 12 14 15 16 ` · `printf '%s\n' "$PT" | grep -cE '^\| [0-9]+ \|'` 과 `printf '%s\n' "$PT" | head -1 | sed -nE 's/.*\(([0-9]+) 개 parity item.*/\1/p'` 이 둘 다 10 · `printf '%s\n' "$PT" | grep -E '^\| 16 \|' | grep -F '알려진 답 대조' | grep -cF '§산출물이 검사일 때'` 1
       (b) `toks "$(sect "$T/QG" '## 원칙별 Enforcement 등급')" '| **산출물이 검사일 때 다섯 가지** | **E2 (신규)** |' '| **0 기대 측정의 매치 줄 가르기** | **E2 (신규)** |' '| **삭제 열거** | **E1 (신규)** |'` 1 · 1 · 1.
       봉인 전 실측: 편집 전 (a) 0 · `1 2 3 4 5 11 12 14 15 ` · 9 · 9 · 0 (b) 0 · 0 · 0. 모의본 (a) 1 · `1 2 3 4 5 11 12 14 15 16 ` · 10 · 10 · 1 (b) 1 · 1 · 1. 문장 삭제 대조: 16 행만 지운 사본은 16 행 0 · 행 수 9 대 제목 10, 매치 줄 가르기 행만 지운 사본은 (b) 둘째 값 0)
- [ ] AR-04: 카이젠 회귀 fixture 가 지금 설계와 맞고 새 규칙을 재는 fixture 가 생긴다 (카이젠 Step 7 · F16 「표에만 있고 안 돌아가는 시험」) — (a) `assertions.json` 이 JSON 으로 읽히고 키가 정확히 `l3-miss false-approve reject-loop vacuous-zero silent-check` 순서이며, 패턴 `Agent\(general-purpose\)` 가 0 개이고 `vacuous-zero` 둘째 패턴이 `cross_diagnosis_by: pending-parent` 다 (b) `fixture-feedback-data/silent-check.yaml` 이 YAML 로 읽히고 `schema_version: 1` · `skill: qa-evaluator` · `evaluation.verdict: APPROVE` · 비지 않은 `diagnosis.cross_diagnosis_notes` · `project_hash: test0011` 을 갖고, 교차 진단 메모에 결함 셋(`첫 칸만 읽는 검사` · `표에만 올리고 실행 목록에 없는 시험 파일` · `한 칸을 못 읽으면 검사 전체가 꺼지는`)이 다 있으며, `test0011` 이 두 카이젠 fixture 폴더에서 이 파일 하나에만 있다 (c) `expected-improvements.md` 에 `## fixture: silent-check` 제목 1 개와 그 절의 `- [ ] ` 항목 3 개 [exact, enumerated]
      (측정: (a) `python3 -c 'import json,sys; a=json.load(open(sys.argv[1],encoding="utf-8")); print(" ".join(a), sum(x["pattern"]=="Agent\\(general-purpose\\)" for v in a.values() for x in v), a["vacuous-zero"][1]["pattern"])' "$T/AS"` 이 `l3-miss false-approve reject-loop vacuous-zero silent-check 0 cross_diagnosis_by: pending-parent`
       (b) `python3 -c 'import sys,yaml; d=yaml.safe_load(open(sys.argv[1],encoding="utf-8")) or {}; print(all([d.get("schema_version")==1, d.get("skill")=="qa-evaluator", d.get("evaluation",{}).get("verdict")=="APPROVE", bool(d.get("diagnosis",{}).get("cross_diagnosis_notes")), d.get("project_hash")=="test0011"]))' "$T/FX"` 이 `True` · `grep -oE '첫 칸만 읽는 검사|표에만 올리고 실행 목록에 없는 시험 파일|한 칸을 못 읽으면 검사 전체가 꺼지는' "$T/FX" | sort -u | grep -c .` 3 · `git grep -l 'test0011' "$END" -- harness/evals/kaizen | grep -c .` 1
       (c) `grep -cE '^## fixture: silent-check$' "$T/EI"` 1 · `sect "$T/EI" '## fixture: silent-check' | grep -cE '^- \[ \] '` 3.
       봉인 전 실측: 편집 전 (a) 키 넷 · 죽은 패턴 1 · 둘째 패턴 `Agent\(general-purpose\)` (b) 빈 파일 — `False` · 0 · `test0011` 0 파일 (`test0010` 은 contract-kaizen `vacuous-boilerplate.yaml` 이 이미 쓴다) (c) 0 · 0. 모의본 (a) 요구값 (b) `True` · 3 (c) 1 · 3. 음성 대조: 메모에서 「첫 칸만 읽는 검사, 」 만 지운 사본 (b) 둘째 값 2)
- [ ] AR-05: 판정 임계와 kit reviewer 가 복제하는 정본 절을 바꾸지 않는다 — 카이젠 Gotcha 「severity 편향 방지」 · 「평가 루브릭 변경 시 기존 계약과의 호환성」 · Counterpart kit reviewer 6 종 — `qa-evaluator.md` 의 `## 판정 규칙` 구간 · 규칙 2 줄(`2. **미검증 ≠ PASS`), 가이드의 `### 카운팅 및 자동 REJECT 임계` · `## Canonical Unverified-Evidence Protocol` · `## Canonical User-Reported Failure Protocol` 구간이 편집 전과 글자 그대로 같고 비어 있지 않다. 그리고 평가자 `### 판정 엄격도` · `## Red Flags`, 가이드 `## Evidence Validity Gate` · `## 원칙별 Enforcement 등급` 구간은 줄을 더하기만 하고 기존 줄을 바꾸거나 지우지 않는다. 더하는 줄도 정해져 있다 — 평가자 `### 판정 엄격도` 는 새 문단 두 줄 · `## Red Flags` 는 두 줄, 가이드 `## 원칙별 Enforcement 등급` 은 표 세 행만 더하고, 가이드 `## Evidence Validity Gate` 는 새 소절 둘(`### 0 이 기대값인데 매치가 나올 때` · `### 산출물이 검사일 때`) 밖에서 편집 전과 글자 그대로 같다 [exact, enumerated]
      (측정: `for p in "EV|## 판정 규칙" "QG|### 카운팅 및 자동 REJECT 임계" "QG|## Canonical Unverified-Evidence Protocol" "QG|## Canonical User-Reported Failure Protocol"; do k=${p%%|*}; h=${p#*|}; diff <(sect "$T/$k.0" "$h") <(sect "$T/$k" "$h") >/dev/null && printf 'same:%s ' "$(sect "$T/$k" "$h" | grep -c .)" || printf 'diff '; done; diff <(grep -F '2. **미검증 ≠ PASS' "$T/EV.0") <(grep -F '2. **미검증 ≠ PASS' "$T/EV") >/dev/null && echo rule2-same || echo rule2-diff` 이 `same:12 same:40 same:62 same:82 rule2-same` · 이어서 `for p in "EV|### 판정 엄격도" "EV|## Red Flags" "QG|## Evidence Validity Gate" "QG|## 원칙별 Enforcement 등급"; do k=${p%%|*}; h=${p#*|}; printf 'removed:%s ' "$(diff <(sect "$T/$k.0" "$h") <(sect "$T/$k" "$h") | grep -c '^<')"; done` 이 `removed:0 removed:0 removed:0 removed:0` (옛 구간에만 있는 줄 = 바뀌거나 지운 줄의 수) · 이어서 `for p in "EV|### 판정 엄격도" "EV|## Red Flags" "QG|## 원칙별 Enforcement 등급"; do k=${p%%|*}; h=${p#*|}; printf 'added:%s ' "$(diff <(sect "$T/$k.0" "$h") <(sect "$T/$k" "$h") | grep -c '^>')"; done; diff <(sect "$T/QG.0" '## Evidence Validity Gate') <(sect "$T/QG" '## Evidence Validity Gate' | awk '/^### (0 이 기대값인데 매치가 나올 때|산출물이 검사일 때)/{s=1;next} s&&/^#{2,3} /{s=0} !s') >/dev/null && echo evg-rest-same || echo evg-rest-diff` 이 `added:2 added:2 added:3 evg-rest-same` (새 구간에만 있는 줄의 수 · 새 소절 둘을 뺀 나머지가 편집 전과 같은지).
       봉인 전 실측: 편집 전 · 모의본 모두 `same:12 same:40 same:62 same:82 rule2-same` · `removed:0` 넷 (모의본은 네 구간에 줄을 더하기만 한다). 음성 대조: 모의본 판정 규칙 1 항 굵은 글씨에 「 · 변이」 를 더한 사본은 첫 값 `diff`. 판정 엄격도 규칙 1 굵은 글씨에 「 (경미하면 예외)」 를 더한 사본은 옛 측정이 `same … rule2-same` 그대로인데 새 측정 첫 값이 `removed:1` — 이것이 검토가 짚은 빈틈이다. Red Flags 기존 줄 하나를 지운 사본은 둘째 값 `removed:1`. 셋째 측정(2 회차 검토 반영): 편집 전 `added:0 added:0 added:0 evg-rest-same`, 모의본 `added:2 added:2 added:3 evg-rest-same`. 음성 대조: 판정 엄격도 규칙 1 줄 아래에 「단, 경미한 FAIL 하나는 Improvement 로 내리고 APPROVE 할 수 있다.」 를 더한 사본은 `added:3 …` (옛 두 측정은 그대로), 가이드 `## Evidence Validity Gate` 머리 바로 뒤(새 소절 바깥)에 「공허한 증거라도 경미하면 PASS 로 본다.」 를 더한 사본은 `evg-rest-diff`, Enforcement 표에 넷째 행을 더한 사본은 셋째 값 `added:4` — 봉인 전 실측 2026-09-24 (`p3build/pre-ar05.sh`))
- [ ] AR-06: 이 Phase 의 변경이 허용 경로 안에 머물고 이 계약이 봉인돼 있다 [exact, enumerated]
      (Given: BUILD 가 개정 파일에 `end_sha:` 를 적은 뒤 · 이 Phase 커밋 메시지마다 서명 줄 `Kaizen-Phase: kaizen-0924-p03-evaluator` · 측정 셋 —
       ① `unsigned_on "$B" "$END" "$SIG" "$EV" "$QG" "$AS" "$EI" "$FX" | grep -c .` 0 (다섯 파일을 건드린 구간 안 커밋이 전부 서명했다 — 다른 Phase 가 이 다섯 파일을 건드리지 않았다)
       ② `.harness/` 밖은 다섯 파일뿐이다 — `my | grep -vE '^(\.harness/|harness/agents/qa-evaluator\.md$|harness/docs/guides/qa-evaluation-guide\.md$|harness/evals/kaizen/evaluator-kaizen/(assertions\.json|expected-improvements\.md|fixture-feedback-data/silent-check\.yaml)$)' | grep -c .` 0 · `my | grep -cxE 'harness/(agents/qa-evaluator\.md|docs/guides/qa-evaluation-guide\.md|evals/kaizen/evaluator-kaizen/(assertions\.json|expected-improvements\.md|fixture-feedback-data/silent-check\.yaml))'` 5
       ③ `harness/references/contract-schema.md` §`.harness/` 범위 조건 의 권장 형태 — `find .harness -type f -name 'sprint-contract*.md' -print0 | while IFS= read -r -d '' f; do verify_seal "$f"; done | awk '{print $1}' | sort | uniq -c` 를 근거로 남기고, 그 가운데 이 Phase 몫인 `SEAL_BROKEN` 이 0 개 — `find .harness -type f -name 'sprint-contract*.md' -print0 | while IFS= read -r -d '' f; do verify_seal "$f"; done | awk '$1=="SEAL_BROKEN"{print $2}' | sed 's#^\./##' | sort -u | comm -12 - <( { my; echo .harness/sprint-contract-kaizen-0924-p03-evaluator.md; } | sort -u) | grep -c .` 0. `SEAL_BROKEN` 줄의 파일이 `my` 에도 없고 이 계약도 아니면 다른 Phase 몫이다 — 파일 이름을 근거에 적고 이 조건에는 세지 않는다. 그리고 이 계약 자신이 봉인돼 있다 — `verify_seal .harness/sprint-contract-kaizen-0924-p03-evaluator.md | cut -d' ' -f1` 이 `SEAL_OK` (`SEAL_ABSENT` 는 봉인을 건너뛴 것이라 FAIL — 평가자 1-e-2 는 이를 경고로만 두므로 이 조건이 막는다).
       봉인 전 실측: `회귀 게이트` 절 `검토 반영 뒤 예행` — ① 0 · ② 0 · 5 · ③ 이 Phase 몫 0 · 이 계약 `SEAL_OK`. 음성 대조: 서명 없는 커밋이 가이드를 건드리면 ① 1. 봉인 전인 지금 작업 폴더의 이 계약은 `SEAL_ABSENT` — 봉인을 빠뜨리면 ③ 이 떨어진다)

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다. 이번 변경에 적용: 네 파일(평가자 · 가이드 · `assertions.json` · `expected-improvements.md`)에 더한 줄의 버전꼴 문자열(`x.y.z`)이 가이드 `- **Parity with**:` 줄에 옮겨 적는 두 설계 가이드 버전(`$END` 판 머리 설정에서 읽은 `$SV` · `$AV`) 말고 0 건이다 — 그 값이 원본과 같은지는 AR-02 (c) 가 잰다. 새 fixture 의 `skill_version` 은 형제 fixture(`vacuous-zero.yaml` `"0.9.1"`)와 같은 시험 데이터라 뺀다 [exact]
      (측정: `added_nofx | grep -oE 'v?[0-9]+\.[0-9]+\.[0-9]+' | sed 's/^v//' | sort -u | grep -vxF -e "$SV" -e "$AV" | grep -c .` 0. 양성 대조: 모의본 가이드에 `버전 9.9.9 와 1.6.0` 줄을 더하면 1 (`9.9.9` 만) — 봉인 전 실측 1)
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```` ```text, ```bash, ```yaml ```` 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 이번 변경에 적용: V6 는 `agents/*.md` 를 읽고 가이드 · `expected-improvements.md` 는 읽지 않으므로 세 파일을 같은 판정에 펜스 길이를 더한 검출기로 잰다 [exact]
      (측정: `회귀 게이트` 절의 `fence.py` 를 `"$T/EV" "$T/QG" "$T/EI"` 에 돌려 `bare_open_total=0 unclosed_total=0`. V6 쪽은 DG-05. 양성 대조: 모의본 가이드 끝에 언어 힌트 없는 펜스를 더하면 `bare_open_total=1` — 봉인 전 실측 1)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL. 이번 변경에 적용: `qa-evaluator.md` 첫 frontmatter 블록에 `name: qa-evaluator` 줄이 1 개 그대로다 [exact]
      (측정: `awk 'NR==1&&/^---/{f=1;next} f&&/^---/{exit} f' "$T/EV" | grep -cxF 'name: qa-evaluator'` 1. V1 쪽은 DG-05. 봉인 전 실측: 편집 전 · 모의본 1)

## Reusability

- [ ] RE-01: N/A (산출물이 평가 규칙 문서 둘과 회귀 fixture 셋이라 재사용 단위 코드가 없다. 측정: `my | grep -vcE '\.(md|json|yaml)$'` 이 0)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다. 이번 변경에 적용: 새 규칙은 기존 절 · 표(Enforcement 표 · Parity Table)와 리포트 틀에 행 · 문단 · 블록으로만 들어가고 새 표를 만들지 않는다 — 두 파일의 표 구분줄 수가 편집 전과 같다 [exact]
      (측정: `for k in EV QG; do printf '%s=%s ' "$k" "$(grep -cE '^[[:space:]]*\|[-: |]+\|[[:space:]]*$' "$T/$k")"; done` 이 `EV=8 QG=27`. 봉인 전 실측: 편집 전 · 모의본 모두 8 · 27. 양성 대조: 표 하나를 더한 가이드 사본 QG=28)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `my | grep -c '^scripts/release.sh$'` 이 0)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (`diagnostics.ide_exclude` 값 `[]`) — 이번 변경에 적용: 편집기 마크다운 확장과 같은 조건(markdownlint-cli2 0.23.2 · MD013 끔)으로 마크다운 세 파일의 **더한 줄**에 걸린 경고가 0 이다. 편집 전부터 있던 경고는 `범위 경계` 절에 적은 대로 범위 밖이다 [exact]
      (측정: `회귀 게이트` 절의 `new-warnings.sh` 를 `for k in EV QG EI; do cp "$T/$k.0" "$T/$k.0.md"; cp "$T/$k" "$T/$k.md"; bash new-warnings.sh "$T/$k.0.md" "$T/$k.md"; done` 로 돌려 세 줄 모두 `new_warnings=0`.
       양성 대조: 삭제 열거 머리의 굵은 글씨 줄 뒤 빈 줄을 뺀 평가자 모의본 1 (MD032), 언어 힌트 없는 펜스와 표를 더한 가이드 모의본 2 — 봉인 전 실측. 모의본 세 파일 0 · 0 · 0)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: DG-01 과 같은 명령이 0)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 변경 파일이 문서와 fixture 뿐. 측정: RE-01 과 같은 명령이 0)
- [ ] DG-05: 저장소 검사가 이 Phase 파일에 대해 깨끗하다 — (a) `python3 scripts/validate-plugin.py harness` 출력에 `V1` · `V6` · `V10` 줄이 있고 셋 다 `ERROR` · `FAIL` 이 아니며, 평가자 · 가이드를 가리키는 `FAIL` 줄이 0 (b) `python3 scripts/check-stale-values.py` 가 종료 코드 2(검사 범위 빔)가 아니고 출력에 이 Phase 다섯 파일 경로가 0 건 (c) `python3 scripts/sync-docs.py --check-only` 와 `python3 scripts/run-evals.py` 가 종료 코드 0 [exact]
      (Given: 작업 트리의 다섯 파일이 `$END` 와 같다 — `git diff --quiet "$END" -- "$EV" "$QG" "$AS" "$EI" "$FX"` exit 0 · 측정: (a) `python3 scripts/validate-plugin.py harness > "$T/vp.txt" 2>&1` 뒤 `grep -cE '^  V(1|6|10) ' "$T/vp.txt"` 3 · `grep -E '^  V(1|6|10) ' "$T/vp.txt" | grep -cE 'ERROR|FAIL'` 0 · `grep -F 'FAIL' "$T/vp.txt" | grep -cE 'harness/(agents/qa-evaluator|docs/guides/qa-evaluation-guide)\.md'` 0
       (b) `python3 scripts/check-stale-values.py > "$T/sv.txt" 2>&1; echo $?` 가 0 또는 1 · `grep -cE 'harness/(agents/qa-evaluator\.md|docs/guides/qa-evaluation-guide\.md|evals/kaizen/evaluator-kaizen/)' "$T/sv.txt"` 0. 1 이 나오면 되살아난 값의 파일이 이 Phase 다섯 파일이 아닐 때만 다른 Phase 몫으로 근거에 적는다
       (c) `python3 scripts/sync-docs.py --check-only >/dev/null 2>&1; echo $?` 0 · `python3 scripts/run-evals.py >/dev/null 2>&1; echo $?` 0.
       양성 대조: 스크래치 사본 평가자 끝에 언어 힌트 없는 펜스 → V6 `1 bare` · `FAIL harness/agents/qa-evaluator.md:1251`, 가이드 Enforcement 표 가운데 문단을 끼운 사본 → V10 `1 broken table row(s)` · `FAIL harness/docs/guides/qa-evaluation-guide.md:201` — 봉인 전 실측. 편집 전 · 모의본 모두 V1~V10 OK, check-stale-values exit 0, sync-docs · run-evals 0)
- [ ] DG-06: `python3 scripts/validate-post-kaizen.py --since 165c8d5dd9f81bd3485de04088494ebe62012fef` 출력의 `scope-isolation` · `doc-contracts` 줄이 `FAIL` · `ERROR` 가 아니다. `docs-site-regen` 은 Final F2 몫이라 판정에서 뺀다. 다른 Phase 커밋 때문에 `scope-isolation` 이 FAIL 이면 `--verbose` 위반 커밋 목록에 서명 줄 커밋이 없을 때 이 조건은 PASS 다. `doc-contracts` 가 `FAIL` · `ERROR` 이면 `python3 scripts/validate-doc-contracts.py -v` 의 `검사:` 줄에 나온 경로를 `my` 와 대조해, 겹치는 경로가 0 개면 다른 Phase 몫으로 근거에 적고 이 조건은 PASS 다 [exact]
      (측정: 명령 출력의 두 줄. `doc-contracts` 가 `FAIL` · `ERROR` 일 때만 — `python3 scripts/validate-doc-contracts.py -v 2>&1 | awk -F' → ' '/^ *검사: /{a=$1; sub(/^ *검사: /,"",a); sub(/:[0-9]+$/,"",a); print a; print $2}' | sort -u | comm -12 - <(my) | grep -c .` 0.
       `scope-isolation` 이 `FAIL` 일 때만 — `python3 scripts/validate-post-kaizen.py --since "$B" --verbose > "$T/vpk.txt" 2>&1` 뒤
       `awk '/ scope-isolation: /{f=1;next} /^\[ /{f=0} f&&/^ +[0-9a-f]{7,40}$/{print $1}' "$T/vpk.txt" | grep -c .` 이 1 이상(위반 목록을 실제로 읽었다) ·
       `awk '/ scope-isolation: /{f=1;next} /^\[ /{f=0} f&&/^ +[0-9a-f]{7,40}$/{print $1}' "$T/vpk.txt" | while read -r c; do git log -1 --format=%B "$c" | grep -qxF "$SIG" && echo "$c"; done | grep -c .` 0.
       첫 값을 함께 거는 이유: 출력 형식이 바뀌어 목록을 하나도 못 읽으면 둘째 값이 조용히 0 이 된다 (이 계약 SK-01 ③ 과 같은 결함 꼴).
       봉인 전 실측: `15 checks — 12 PASS / 0 FAIL / 0 ERROR / 3 SKIP`, scope-isolation PASS · doc-contracts PASS · docs-site-regen SKIP)
- [ ] DG-07: evaluator-kaizen 회귀 확인(카이젠 스킬 Step 7 Regression Smoke Test) — `$END` 판 `assertions.json` 의 패턴 8 개가 `$END` 판 대상 파일에서 각각 1 건 이상 잡힌다 [exact, enumerated]
      (측정: `회귀 게이트` 절의 `dg07.py` 를 `python3 dg07.py "$T"` 로 돌려 둘째 줄이 `min 1 n 8` 이상 — `min` 이 1 이상이고 `n` 이 8.
       봉인 전 실측: 편집 전 `l3-miss#0:3 false-approve#0:6 reject-loop#0:5 vacuous-zero#0:7 vacuous-zero#1:0` · `min 0 n 5` — 지금 회귀 확인이 떨어진다(AR-04 가 고친다). 모의본 `… vacuous-zero#1:1 silent-check#0:2 silent-check#1:1 silent-check#2:1` · `min 1 n 8`)
