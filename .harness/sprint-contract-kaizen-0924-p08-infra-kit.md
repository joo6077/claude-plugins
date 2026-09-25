---
feature: "카이젠 2026-09-24 Phase 8 계약 — 빨간 CI 원인 가르기 · 미검증 네 칸 · 알려진 답 대조 · 사실 정정(kubeconform · OpenTofu 1.7+ · README)"
slug: kaizen-0924-p08-infra-kit
created: "2026-09-25 07:00"
complexity: "복잡"
conditions: 28
status: done
owner_session: de8c7935-a5b6-4df5-9106-fafa73c288a0
conditions_digest: sha256:7cc562b4e14e06a3
locked_at: "2026-09-25 07:40"
---

## 배경

이 Phase 의 외부 근거는 `.harness/.meta/evidence/phase8.md` 하나다. 처리 배정표(`.claude/kaizen-input/insights-report.md`)에서 `배정` 칸이
`Phase 8` 인 행은 `backend-family:P3` 하나다. 러닝북 `Phase 별 추가 과제` 에 Phase 8 줄은 없고, 앞 Phase notes 가 Phase 8 로 넘긴 줄이 셋이다.
오케스트레이터 Step 8 은 「Phase 1 에서 설계 가이드가 변경되었으면 infra-kit 전 스킬을 전수 감사한다」 고 적는다 — 그 감사에서 넘김 줄 밖의 자리를 더 찾았다.

| 키 · 출처 | 내용 | 이번 처리 |
| --- | --- | --- |
| `backend-family:P3` | infra-guide — 자동 검사가 빨갛다고 내 변경 탓으로 단정하지 않기. 비고: 기준 커밋 가르기 규칙 세 곳을 하나로 정한다 | 반영 — SK-01 ~ SK-04 · AR-02. 규칙은 Phase 4 가 `/sprint` Step 3 하나로 정했다(`phase4-notes.md`) — 판정 세 줄을 원문 그대로 옮긴다(SK-01 알려진 답) |
| `F09` (Phase 4 행) | 비고 「기준 커밋 가르기 규칙이 harness:P07 · backend-family:P3(Phase 8) · backend-family:P4(Phase 9) 세 곳」 | Phase 4 가 정한 정본을 따른다. CI 에서만 보이는 두 경우(환경 · 비결정성, 미확정)는 근거 파일 §4 로 더한다 — `/sprint` 가 이 둘을 받을지는 다음 사이클 Phase 4 로 넘긴다(ER-03) |
| `phase4-notes.md` 넘김 표 | 「`backend-family:P3` · `backend-family:P4` — Phase 8 · 9 — `/sprint` Step 3 의 판정 세 줄을 옮겨 적는다. 플러그인이 따로 설치돼 경로로 가리킬 수 없다」 | 반영 — SK-01 이 코드 블록과 판정 표가 원문과 글자 그대로 같은지 잰다 |
| `phase1-notes.md` 넘김 표 | `infra-kit/skills/infra-test/SKILL.md:37` 「`[미검증] TOOL_OR_ENV_MISSING` … 재검증」 — 시도한 우회 칸 없음 | 반영 — SK-05. 같은 꼴이 infra-test 안에 셋 더(Step 8 4 항 · 보고 예시 두 줄), infra-audit 에 셋 · infra-reviewer 에 둘 더 있고 상태어 정본에는 리포트 쪽 네 칸 안내가 없어 함께 고친다(SK-05 · SK-06) |
| `phase7-notes.md` 넘김 표 | `infra-kit/README.md` 검증 절 「7 카테고리 구조 감사」(`:54`) — 검사는 V1 ~ V10 열 가지 | 반영 — SK-04. 숫자를 박지 않고 개수는 `harness/docs/guides/plugin-validation-guide.md` 가 정한다고 적는다(Phase 7 과 같은 문구) |
| Phase 1 가이드 변경 셋 (`skill-design-guide.md` §3.7) | (1) `[미검증]` 네 칸 (2) 작업을 못 한다고 결론 내리기 전 네 칸 (3) 0 이 아닌 값을 내는 새 측정 — 알려진 답 대조 | (1) SK-05 · SK-06 (2) infra-audit Step 4 BLOCKED 의 「소스 부재」 가 이 꼴이라 SK-06 에 넣었다 (3) infra-test 가 만드는 검사 스크립트가 0 이 아닌 값을 낸다 — SK-07 |
| 근거 파일 §3 현행화 · §5 | `kubeconform -kubernetes-version 1.30.0` 고정 · README 이력 줄 「OpenTelemetry 3 signals stable」 · 「OpenTofu 1.7+ native state encryption」 은 v1.11 문서로 출처화 불가 | 반영 — SK-08 · SK-10 · SK-09. Flux v2.9 · Argo CD 3.5 · Kubernetes 1.37 · Terraform 1.16 · OpenTofu 1.12.6 · Crossplane 2.4 는 research-log 에 기록만 한다(SK-11) — 규칙으로 올리려면 `docs/infra/` 원칙이 먼저다(infra-kaizen Gotcha 2) |

글로벌 평가 피드백(`~/.harness/feedback/evaluator/`)에서 infra-kit Phase 계약을 평가한 최근 기록은 2026-08-14 `kaizen-phase8-infra-gate-taxonomy` 한 벌이다 — APPROVE ·
개선 제안 없음이고, 평가자가 infra-test Step 5 골격을 fixture 여덟으로 직접 돌려 확인했다. 이번 SK-07 도 같은 골격을 알려진 답 입력으로 실제로 돌린다. 데이터 풀 §1 의
2026-09-24 개선 메모(「N 카테고리」 낱말 측정이 backend · infra 감사의 10 카테고리와 겹친다)는 이 계약에서 겹치지 않는다 — SK-04 가 README 의 「7 카테고리 구조 감사」 를 낱말 하나가 아니라 문장 전체로 잰다.

관심사는 셋이다 — (1) 빨간 CI 원인 가르기(SK-01 ~ SK-04 · AR-02) (2) Phase 1 가이드 변경의 반대편 — 미검증 네 칸과
알려진 답 대조(SK-05 ~ SK-07) (3) 사실 정정과 현행화(SK-08 ~ SK-11). infra-kaizen Gotcha 4 는 관심사를 1~2 개로 제한하고 3 개를 넘으면 다음 사이클로 미루라고 한다.
셋째는 근거 파일 §3 · §5 가 낡았거나 출처로 뒷받침되지 않는다고 적은 문장을 고치는 일이라 함께 한다. 셋 다 파일 여러 개를 건드리지만 한 관심사 안의 형제 대칭이다(같은 Gotcha 4 가 이렇게 센다).

## 리서치 소스

외부 조회 0 회. 아래 URL 은 전부 근거 파일 `.harness/.meta/evidence/phase8.md` 에서 가져왔다.

- [Git — git merge-base](https://git-scm.com/docs/git-merge-base) — 기준 가지의 지금 끝이 아니라 공통 조상이고, 둘 이상일 수 있다 (SK-01)
- [GitHub CLI — gh run list](https://cli.github.com/manual/gh_run_list) — `--commit` · `--branch` · `--status` · `--workflow` · `--limit`, `headSha` 필드. `--workflow` 없는 성공 조회는 어느 workflow 의 성공인지 가리지 않는다 (SK-01 · SK-02)
- [GitHub — Re-running workflows and jobs](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs) — 재실행은 같은 `GITHUB_SHA` · `GITHUB_REF`, 실패 job 만 · 디버그 로그 (SK-01)
- [GitHub-hosted runners](https://docs.github.com/en/actions/reference/runners/github-hosted-runners) — job 마다 새 VM, `-latest` 의 뜻 (SK-01)
- [GitHub — About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) — 필수 검사는 성공 · skipped · neutral (SK-01)
- [Kubernetes v1.37.1](https://github.com/kubernetes/kubernetes/releases/tag/v1.37.1) — 최신 안정판. 고정 `1.30.0` 대신 대상 클러스터 버전을 따른다 (SK-08)
- [OpenTofu state encryption v1.11](https://opentofu.org/docs/v1.11/language/state/encryption/) — 1.7 도입 연혁을 적지 않는다 (SK-09)
- [OpenTelemetry spec status](https://opentelemetry.io/docs/specs/status/) — signal 별 상태가 다르다 (SK-10)
- research-log 기록만: [Kubernetes 1.37 changelog](https://github.com/kubernetes/kubernetes/blob/v1.37.1/CHANGELOG/CHANGELOG-1.37.md) · [Terraform v1.16.0](https://github.com/hashicorp/terraform/releases/tag/v1.16.0) ·
  [OpenTofu v1.12.6](https://github.com/opentofu/opentofu/releases/tag/v1.12.6) · [Flux v2.9.0](https://github.com/fluxcd/flux2/releases/tag/v2.9.0) ·
  [Argo CD 3.4→3.5](https://argo-cd.readthedocs.io/en/stable/operator-manual/upgrading/3.4-3.5/) · [Crossplane v2.4.0](https://github.com/crossplane/crossplane/releases/tag/v2.4.0) (SK-11)

근거 파일이 스스로 밝힌 한계를 그대로 옮긴다. 「내 변경 / 기준 실패 / 환경」 세 분류를 규범으로 정한 공식 문서는 없다 — 그래서 원칙 7 은 분류가 이 킷의 규칙이라고 적는다(SK-01 이 그 문장을 잰다).
HEAD 에서만 실패하고 기준 커밋에서 통과한 것은 상관 증거이지 인과 증명이 아니다 — 원칙 7 이 「원인 증명은 아니다」 로 적는다. 가를 수 없을 때는 억지로 셋에 넣지 않고 `미확정` 을 둔다(§4 권장안 4).
bare `gh run list --branch … --status success --limit 1` 은 필수 검사 전부의 통과를 보장하지 않는다 — 원칙 7 과 Gotcha 14 가 그 한계를 적는다. GitHub 밖 CI 의 같은 조회 명령은 근거 파일에 없어 넣지 않는다.
「Terraform 1.10+ ephemeral」 의 도입 버전은 근거 파일이 확인하지 못했고(§5), 「1.7+ mocking」(audit-criteria · init-checklist · infra-test Gotcha 8) · 「OpenTofu 1.7+ write-only 인수」(infra-test Gotcha 10) 는
근거 파일이 다루지 않았다 — 이번에 고치지 않고 research-log 다음 사이클 후보로 둔다.

내부 입력: 데이터 풀 §0 처리 배정표 · §0-b `e863512e`(2026-09-18 — 다른 세션들이 깬 공용 개발 가지의 빨간 CI 를 몇 시간 쫓았고 워크트리는 사용자가 먼저 제안) · §0.5 [infra]
세 건(참고만 — 공유 dev 트리 대신 워크트리 기억은 `미분류` 라 PASS 근거로 쓰지 않는다) · Phase 1 · 4 · 7 notes 의 넘김 표.

## GAP 분석 · 개선안 초안

### 1.1 복잡도 4 축

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 4 — 원칙 문서(`docs/infra/`) · 스킬 넷 · 상태어 정본과 감사 기준과 평가 에이전트 · 평가 사례 데이터 |
| 공개 API·계약 변경 | 외부에 노출된 형태가 바뀌는가 | 예 — `[미검증]` 보고 형태가 네 칸으로 바뀐다(infra-test 완료 보고 · infra-audit 과 infra-reviewer 의 근거 열). 원칙 색인의 cicd 키워드가 늘어 라우팅이 바뀐다 |
| 소비면 존재 | 이 형태를 받아 쓰는 반대편이 있는가 | 예 — 아래 Counterpart 표 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — Gotcha 를 가운데 끼우면 번호로 가리키는 자리(infra-guide Step 2 → Gotcha 9, infra-test Step 5 · 7 · 8 → Gotcha 11 ~ 15, infra-audit Step 3 · 4 → Gotcha 10 ~ 12)가 어긋난다. reviewer §9 는 정본 복제라 한 글자도 바뀌면 안 된다. 원칙 7 의 판정 세 줄이 `/sprint` 와 갈라지면 규칙이 두 벌이 된다 |

네 축 모두 「예」 이고 공개 형태 변경과 소비면이 둘 다 「예」 라 **복잡**이다. Step 2.5 Counterpart 조건을 넣는다(AR-02 · ER-03).
기능 조건은 18 개다 — 복잡 9~20 안이다 (SKILL.md Step 6.2 둘째 명령으로 이 파일을 세면 18).

### 1.2 설정 리터럴 대조표

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A 사유에 그대로 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A 사유에 그대로 |
| `diagnostics.ide_exclude` | `[]` | DG-02 에 그대로 |
| `contract_categories[].id` / `prefix` | `Skill`/`SK` · `Script`/`SC` · `Error`/`ER` · `Architecture`/`AR` | 조건 섹션 제목과 접두 그대로 |
| `anti_patterns[].id` / `message` | AP-01 · AP-02 · AP-03 · AP-04 | AP-01 · AP-03 · AP-04 선별, message 원문 그대로. AP-02(force push)는 이 Phase 가 밀어 넣지 않아 뺀다 |

### 1.4 편집 전 감사 (실제로 읽은 줄 — 시작 커밋 `4a8ec55` 판)

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 |
| --------- | ---------------------------- | ------------------- | ----------- |
| `docs/infra/platform/cicd.md` | `:3-4` (머리 설정 0.1.0 · 2026-04-04) · `:9` (다루는 범위) · `:45-49` (원칙 6 — 마지막) · `:53` (`## 수치/기준값`) | 빨간 검사 원인 가르기 원칙 0 건. infra-kaizen Gotcha 2 는 이 문서에 없는 원칙을 스킬에 넣지 못하게 한다 | SK-01 |
| `harness/skills/sprint/SKILL.md` | `:93-120` (Step 3 원인 셋 가르기 · 코드 블록 · 판정 표) | 없음 — 정본. 읽기만 | SK-01 알려진 답 (고치지 않는다) |
| `infra-kit/skills/infra-guide/SKILL.md` | `:29` (Gotcha 13 — 마지막) · `:31` (`# Process`) · `:40` (Step 1 cicd 행) · `:58` (Step 2 가 principle-index 를 읽는다) | 빨간 CI 규칙 없음 · cicd 키워드에 실패 · 재실행 낱말 없음 | SK-02 · SK-03 · AR-02 |
| `infra-kit/references/principle-index.md` | `:9` (cicd 행 → `docs/infra/platform/cicd.md`) · `:34` (경로는 레포 루트 기준) | 키워드가 Step 1 행과 같이 늘어야 한다(근거 파일 §2 P3.2) | SK-03 · AR-02 |
| `infra-kit/skills/infra-guide/references/principle-index.md` | `:10` (CI/CD 행 — 키워드 칸 없는 옛 사본) | 없음 — 근거 파일 §2 가 수정 대상에서 뺐다 | SK-03 (그대로인지 잰다) |
| `infra-kit/evals/evals.json` | `:56-66` (사례 5 — 마지막) · `:67` | 빨간 CI 사례 없음 | SK-04 |
| `infra-kit/README.md` | `:30` (cicd 요약) · `:53` (「4 스킬 assertion 전수 검증」) · `:54` (「7 카테고리 구조 감사」) · `:59` (2026-04-24 이력 「OpenTelemetry 3 signals stable」) | 평가 사례 수 · 구조 검사 개수(실제 V1 ~ V10) · OTel 이력 줄 | SK-04 · SK-10 |
| `infra-kit/skills/infra-test/SKILL.md` | `:37` (Gotcha 12 — 옛 `[미검증]` 꼴) · `:198-336` (Step 5 골격 — 알려진 답 입력으로 실제로 돌림) · `:382` (`-kubernetes-version 1.30.0`) · `:423` (Step 7 도구 확인 문단) · `:444` (Step 8 4 항) · `:458-459` (보고 예시) · `:467` (References) | 옛 미검증 꼴 넷 · 알려진 답 대조 없음 · 고정 스키마 버전 | SK-05 · SK-07 · SK-08 · AR-02 |
| `infra-kit/references/gate-result-taxonomy.md` | `:86-94` (§재검증 명령 의무 — 스크립트 줄 예시) · `:96-102` (§소비처 셋) | 리포트 쪽 네 칸 안내 없음. 스크립트 줄 형식 자체는 그대로 둔다 | SK-05 · AR-02 |
| `infra-kit/skills/infra-audit/SKILL.md` | `:25` (Gotcha 11 — 「근거에 이유를 기술하라」 · 「manifest 정적 리뷰만 수행」) · `:27` (Gotcha 12 — 규칙 소스 부재 줄, 번역투 「적용된다」) · `:103` (Step 4 1 항 「소스 부재 사유 명시」) · `:124` (References) | 옛 미검증 꼴 셋 · 번역투 하나 | SK-06 · ER-02 · AR-02 |
| `infra-kit/agents/infra-reviewer.md` | `:53-54` (평가 기준 참조 둘) · `:58` (「`[미검증]` 태그 + 이유」) · `:64` (예시 3 행 「1차 … fallback …」) · `:70-129` (§9 정본 복제) | 출력 포맷의 미검증 표기가 네 칸이 아니다. §9 는 정본의 2026-08-13 이후 판과 다르다 — 이번에 고치지 않는다(아래) | SK-06 · AR-02 |
| `infra-kit/references/audit-criteria.md` | `:103` (「OpenTofu 1.7+ native state encryption」) · `:104` (「1.7+ mocking」) · `:112` (v1.11 출처) | 출처로 뒷받침되지 않는 버전 | SK-09 (`:104` 는 근거 파일이 다루지 않아 그대로) |
| `infra-kit/references/init-checklist.md` | `:130` · `:133` (「1.7+」 native state encryption 두 자리) · `:132` (「1.7+ mocking」) | 같은 버전 단정 둘 | SK-09 (`:132` 그대로) |
| `infra-kit/skills/infra-init/SKILL.md` | `:26` (Gotcha 11 「OpenTofu 1.7+ native state encryption」) | 같은 버전 단정 | SK-09 · AP-04 |
| `docs/infra/research-log.md` | `:2-3` (1.3.0 · 2026-08-13) · `:8` (2026-08-13 항목) · `:82` (「OpenTofu 버전 단정」 제거 기록) · `:124` (2026-07-27 OTel 판정) | 2026-08-13 이 뺐다고 적은 「1.7+」 가 네 자리 남았다 | SK-11 |
| `harness/docs/guides/qa-evaluation-guide.md` | `:1223-1290` (§Canonical Unverified-Evidence Protocol — 조항 1 의 N/A 표 · 새 조항 2 · 번호 3 이 둘) | 정본을 복제하는 킷 reviewer 일곱(api · backend · design · planning · rust · react · infra) 모두 새 판의 조항 1 N/A 표와 조항 2 가 없다(`grep -c` 실측 0 씩). 조항 2 는 계약 DG 조건 처리라 킷 reviewer 에 맞는지 정본 쪽 결정이 먼저다 | ER-03 넘김 (고치지 않는다) |

후보 옵션은 하나로 정했다 — 빨간 CI 규칙 본문을 어디에 둘지 (가) `docs/infra/platform/cicd.md` 원칙 7 (나) `operations/incident-response.md` (다) infra-guide Gotcha 본문.
(가)를 고른다. principle-index 의 cicd 행이 이미 그 파일을 가리키고, infra-guide Gotcha 4 가 그 문서를 읽고 답하게 한다. (다)는 infra-kaizen Gotcha 2(원칙 문서 선행)에 어긋난다.
판정 세 줄은 Phase 4 가 정한 대로 `/sprint` Step 3 원문을 옮기고, 원문에 없는 CI 두 경우는 표 밖 목록으로 붙여 원문 표를 바꾸지 않는다. Gotcha 는 번호를 밀지 않도록 맨 끝(14)에 더한다.

### Counterpart — 바뀌는 형식을 받아 쓰는 반대편

| 면 | 파일 | 바뀌는 것 | 이번 처리 |
| --- | --- | --- | --- |
| producer | `docs/infra/platform/cicd.md` 원칙 7 | 새 원칙 | SK-01 |
| consumer | `infra-kit/references/principle-index.md` | cicd 행 → cicd.md, 키워드 | SK-03 · AR-02 (경로를 풀어 원칙 7 이 읽히는지) |
| consumer | `infra-kit/skills/infra-guide/SKILL.md` | Step 2 가 principle-index 를 읽는다 · Gotcha 14 가 원칙 7 을 가리킨다 | SK-02 · AR-02 (Step 2 줄이 그대로인지) |
| producer | `harness/skills/sprint/SKILL.md` Step 3 | 판정 세 줄 원문 | 고치지 않는다 — SK-01 이 원문과 같은지 잰다 |
| producer | `infra-kit/references/gate-result-taxonomy.md` §재검증 명령 의무 | 리포트는 네 칸 | SK-05 |
| consumer | `infra-kit/skills/infra-test/SKILL.md` · `infra-kit/skills/infra-audit/SKILL.md` · `infra-kit/agents/infra-reviewer.md` | 상태어 정본을 References · 평가 기준 참조로 읽는다 | 읽는 줄은 고치지 않는다 — AR-02 가 그대로인지 잰다. 각자의 미검증 표기는 SK-05 · SK-06 |
| consumer | `infra-kit/evals/evals.json` · `infra-kit/README.md` | 사례 수 · 검증 절 | SK-04 · SK-10 |
| consumer (Final) | `docs/infra-kit/cicd.html` · `docs/infra-kit/infra-test.html` · `docs/infra-kit/gate-result-taxonomy.html` | 원칙 7 과 네 칸이 없다 | 명시적 미완 — Final F2 재생성(ER-03) |
| consumer (다음 사이클) | `harness/skills/sprint/SKILL.md` Step 3 | CI 두 경우를 정본이 받을지 | 명시적 미완 — 다음 사이클 Phase 4(ER-03) |
| consumer (다음 사이클) | `infra-kit/agents/infra-reviewer.md` §9 ↔ `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol | 정본이 2026-08-13 뒤에 바뀌었다 | 명시적 미완 — 다음 사이클 Phase 3 가 정본 번호 3 중복과 조항 2 의 킷 적용 여부를 정한 뒤 킷 reviewer 일곱이 같이 옮긴다(ER-03) |

### 개선안 초안

치환 스물아홉 개를 글자 그대로 적은 모의 스크립트가
`/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p8d/mock.py` 에 있다.
옛 문자열이 정확히 한 번 있어야 치환하고 끝에 `mock applied 29` 를 낸다. BUILD 는 이 치환을 글자 그대로 옮긴다 — 조건이 문장을 글자 그대로 센다. 파일마다 요지:

1. `docs/infra/platform/cicd.md` — 머리 설정 0.2.0 · 2026-09-25, 다루는 범위에 「빨간 검사의 원인 가르기」, 원칙 6 뒤 원칙 7(원인 다섯 갈래 · 분류는 킷 규칙 · merge base 복수 ·
   준비 명령 · `/sprint` Step 3 코드 블록과 판정 세 줄 원문 · CI 두 경우 · 같은 핵심 오류 · 기준 실패도 따로 보고 · 원인 증명 아님 · `gh run list` 두 용법과 한계 · 출처 다섯)
2. `infra-kit/skills/infra-guide/SKILL.md` — Gotcha 14 (E1), Step 1 cicd 행 키워드 셋
3. `infra-kit/references/principle-index.md` — cicd 행 키워드 셋
4. `infra-kit/evals/evals.json` — 사례 6 (공용 가지의 빨간 CI, infra-guide)
5. `infra-kit/README.md` — cicd 요약 · 검증 절 두 줄 · 2026-04-24 이력 줄 정정 표시
6. `infra-kit/skills/infra-test/SKILL.md` — Gotcha 12 · Step 8 4 항 · 보고 예시를 네 칸으로, Step 7 알려진 답 대조 문단, Step 6 kubeconform 버전 변수
7. `infra-kit/references/gate-result-taxonomy.md` — §재검증 명령 의무 끝에 리포트 네 칸 문단
8. `infra-kit/skills/infra-audit/SKILL.md` — Gotcha 11 · 12 · Step 4 1 항 네 칸, Gotcha 12 번역투 「적용된다」 → 「해당한다」
9. `infra-kit/agents/infra-reviewer.md` — 출력 포맷 규칙 줄 · 예시 3 행 네 칸 이름
10. `infra-kit/references/audit-criteria.md` · 11. `infra-kit/references/init-checklist.md` · 12. `infra-kit/skills/infra-init/SKILL.md` — 「1.7+」 네 자리 제거
13. `docs/infra/research-log.md` — `## [2026-09-24] - Phase 8 kaizen` 항목(외부 근거 여덟 · 변경 내역 · 사실 정정 둘 · 규칙으로 올리지 않은 것 여섯 · 다음 사이클 넷), 머리 설정 1.4.0 · 2026-09-25

새 규칙의 강도: infra-guide Gotcha 14 는 E1(가이드 답변 속 지적이라 남길 산출물이 없다 — skill-design-guide §3.7 등급표). 네 칸은 가이드 §3.7 3 항을 옮긴 것이라 새 등급을 만들지 않는다.

## 범위 경계

- 이 Phase 시작 HEAD: `4a8ec55f4d874eaaed083af9621f9679693cbdb6`. 범위 상한은 개정 파일 `.harness/sprint-amendments-kaizen-0924-p08-infra-kit.md` 의
  `end_sha:` 마지막 값이다. 여러 Phase 가 같은 가지 `kaizen/2026-09-24` 에 동시에 커밋하므로 `HEAD` 로 재지 않는다
- 고치는 파일은 열셋이다 — 아래 블록이 그 목록이다(`harness/README.md` §커밋 안전 훅 이 정한 범위 선언 자리). 새 파일은 없다. `.harness/` 쪽은 이 계약 · 개정 파일 ·
  QA 피드백 · `.harness/.meta/kaizen-0924/phase8-notes.md` · `.harness/.meta/kaizen-0924/phase8-review.md` 를 쓴다 — 슬러그를 나열하지 않고 AR-01 셋째 값 `verify_seal` 로 잰다.
  AR-01 다섯째 값이 이 블록과 측정 공통 정의의 `FILES` 가 같은지 잰다

```text
# sprint-scope
docs/infra/platform/cicd.md
docs/infra/research-log.md
infra-kit/skills/infra-guide/SKILL.md
infra-kit/references/principle-index.md
infra-kit/evals/evals.json
infra-kit/README.md
infra-kit/skills/infra-test/SKILL.md
infra-kit/references/gate-result-taxonomy.md
infra-kit/skills/infra-audit/SKILL.md
infra-kit/agents/infra-reviewer.md
infra-kit/references/audit-criteria.md
infra-kit/references/init-checklist.md
infra-kit/skills/infra-init/SKILL.md
.harness/
```

- **이 Phase 의 커밋 메시지에는 전부 `Co-Authored-By` 줄 바로 위에 서명 줄 `Kaizen-Phase: kaizen-0924-p08-infra-kit` 한 줄을 넣는다** (봉인 커밋 포함).
  AR-01 · ER-03 · SC-00 · DG-01 · DG-03 · DG-04 · DG-06 이 이 줄로 이 Phase 커밋을 가린다(`harness/references/contract-schema.md` §여러 주체가 한 가지에 커밋할 때 선택지 B).
  서명을 빠뜨린 커밋은 서명 줄 목록에 안 보이므로 AR-01 첫째 값과 ER-03 셋째 값은 경로로 직접 센다.
  FIX 가 커밋을 더할 때도 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다(옛 줄은 지우지 않는다). notes 커밋도 이 Phase 커밋이다 — notes 를 커밋한 뒤 그 sha 로
  `end_sha:` 줄을 하나 더 덧붙여 커밋한다
- 구현 커밋은 `git add -- <파일…> && git commit -o -- <파일…>` 로 열세 파일만 싣는다. `docs/infra/` 둘과 `infra-kit/` 열하나를 두 커밋으로 나눠도 된다 —
  둘 다 이 킷 몫이라 `validate-post-kaizen.py` scope-isolation 에 걸리지 않는다(예행에서 두 커밋으로 확인)
- 측정이 기대는 제목 · 줄 머리는 이름을 바꾸지 않는다: `### 6. ` · `## 수치/기준값` (cicd.md) · `# Gotchas` · `## Step 1: 탐색` (infra-guide) · `| cicd |` (principle-index 둘) ·
  `### Step 6: K8s Manifest 테스트 생성` · `### Step 7: 실행 검증` · `### Step 8: 결과 보고` · `# tests/ci-validation.sh` (infra-test) · `## 재검증 명령 의무` · `## 소비처` (gate-result-taxonomy) ·
  `## Step 4: 최종 판정` (infra-audit) · `## 출력 포맷` · `## 9. Canonical Unverified-Evidence Protocol` (infra-reviewer) · `| State encryption |` (audit-criteria) · `## [2026-08-13] - Phase 8 kaizen` (research-log) ·
  `### Step 3: 빌드/분석 검증` (`/sprint` — 읽기만) · skill-design-guide §3.7 의 네 칸 줄(읽기만)
- 공유 파일(`.claude-plugin/marketplace.json` · `infra-kit/.claude-plugin/plugin.json` 버전 · 루트 `README.md` · 루트 `CLAUDE.md` · `docs/` HTML · 처리 배정표 · 감사 로그 ·
  실패 횟수 파일 · `.github/workflows/ci.yml` · `.harness/stale-values.yaml`)과 다른 Phase · 레포 전용 파일(`harness/` · `scripts/` · `.claude/skills/`)은
  건드리지 않는다 — ER-03 셋째 값. infra-kit README 에는 AUTO 구간이 없다. 문서 사이트 재생성은 Final F2 몫이라 DG-06 에서 `docs-site-regen` 을 뺀다
- QA(`harness:qa-evaluator`)는 설치본이다 — 이 Phase 가 고치는 파일에 qa-evaluator 는 없다
- 사용자 승인(Step 5) 대체: 사용자가 「자동으로 끝까지 알아서 진행해 내 허락이 필요한건 코덱스로 리서치나 검토받고」라고 위임했다(세션
  `de8c7935-a5b6-4df5-9106-fafa73c288a0` 기록 queued_command `2026-09-24T04:04:16.964Z`). Codex 사용량 한도가 소진돼(오류 원문 「You've hit your usage limit … try
  again at 11:05 PM」, 2026-09-24) 독립 Claude 검토자(REVIEW 에이전트)가 대신한다. 이어 사용자가 「코덱스 대신에 그냥 너가 알아서 진행하라고」라고 명시했다(같은 세션
  기록 user `2026-09-24T11:54:58.940Z`). 검토 결과 파일: `.harness/.meta/kaizen-0924/phase8-review.md`. 검토 VERDICT: 1 회차 `CHANGES` — 고칠 것 하나(ER-03 기대 출력 「1 을 열일곱 번」 이
  조건 문장 「각각 1 회 이상」 과 어긋남)와 막지 않는 권장 여섯을 초안이 전부 반영했다. 2 회차 `CHANGES` — 고칠 것 하나(ER-03 조건 줄이 Final 에 넘기는
  `.harness/stale-values.yaml` 등록 안내가 사실과 다르다 — 옛 값 검사는 docs-site 소스 폴더만 훑어 infra-kit 을 보지 못하고, 그대로 등록하면 이 Phase
  research-log 기록 줄이 걸린다)와 권장 둘. BUILD 가 `scripts/check-stale-values.py` 머리 설명과 `SOURCE_DIRS` 를 직접 읽어 지적이 맞는 것을 확인한 뒤,
  봉인 전에 2 회차 「고칠 문구」 를 그대로 ER-03 조건 줄에 넣고 권장 1(infra-kaizen Gotcha 6 형제 대조 표의 「미검증 3항」 넘김)도 같은 줄에 넣었다 — 조건 줄이
  검토자가 두 수정을 함께 넣어 본 사본 `p8r2/contract.fix2.md` 와 글자 그대로 같다. 권장 2(출력 파일)는 `회귀 게이트` 절 표 아래 문단을 BUILD 가 다시 잰 출력
  파일로 고쳤다. 측정 명령(`common.sh` · `m.sh` · `new-warnings.sh`)은 바꾸지 않았다. 3 회차 검토는 부르지 않았다 — 남은 지적은 조건 줄 글 한 곳이고
  측정이 그 자리의 토큰(`.harness/stale-values.yaml` · `.claude/skills/infra-kaizen/SKILL.md`)만 보므로 판정 값이 바뀌지 않는다
- 오라클 한계: SK-04 는 평가 사례의 **구조**만 잰다(`scripts/run-evals.py` 는 스킬을 실행하지 않는다). 사례 6 을 실제 스킬로 돌려 답이 네 assertion 을 채우는지는
  LLM 판정이라 결정론 측정이 없다 — 조건으로 걸지 않는다. 원칙 7 의 코드 블록은 문서 속 예시라 실제 저장소에서 돌리지 않는다 — 원문과 같은지(SK-01)만 잰다
- 오라클 해소: SK-01 ~ SK-06 · SK-09 ~ SK-11 — 산출물이 문서 문장 자체라 정해진 절 · 줄에 정해진 문장이 있는지가 판정이다. `sect` 가 코드 펜스를 건너뛰고 절을 자르고,
  `gline` 이 한 줄짜리 Gotcha · 표 행을 고른다. 시작 커밋 판에서 새 문장 0 · 옛 문장 1 이상을 봉인 전에 확인했고, 토큰 하나를 지운 사본 85 개 모두에서 출력이 요구값과 달라졌다(`회귀 게이트` 절)
- 오라클 해소: SK-07 · SK-08 — 문서가 적은 값을 실제로 돌린 결과와 대조한다(알려진 답 · 음성 대조). SK-04 · DG-05 — 검사 스크립트를 실제로 돌린 출력이다
- 오라클 해소: ER-01 · ER-02 · AP-01 · AP-03 · DG-02 — 편집 전 판과 파일마다 비교한 더한 줄 계산이다. 각각 양성 대조가 붙어 있다
- 오라클 해소: ER-03 · AR-01 · SC-00 · DG-01 · DG-03 · DG-04 · DG-06 — 커밋 기록과 봉인 검증 함수를 실제로 돌린 출력이다. 예행 저장소 변형 넷이 양성 대조다
- 커버리지 해소: SK-01 · SK-02 · SK-03 · SK-05 · SK-06 · SK-09 · AR-02 — 산문의 파일 이름은 측정 `m <조건 ID>` 가 공통 정의의 변수(`$CI` · `$GU` · `$PI` · `$OLDPI` · `$SP` ·
  `$TE` · `$GT` · `$AU` · `$RV` · `$AC` · `$IC` · `$IN`)로 연다(파일과 변수의 대응은 `common.sh` 머리). 토큰은 `m.sh` 의 같은 ID 갈래에 글자 그대로 있다.
  SK-01 의 `0.2.0` 은 머리 설정 값이라 `fm_get` 이 읽고, `/sprint` 는 `$SP` 의 스킬 이름, `m.sh` 는 측정 도우미 자체의 이름이다. SK-05 의 `gate-result-taxonomy.md` 는
  산문 속 짧은 이름(`$GT`), `infra-kit/skills/infra-test/SKILL.md:37` 은 넘김 출처 표기다. SK-05 · SK-06 · SK-09 의 `infra-kit/` 는 `grep -r` 의 인자다
- 커버리지 해소: ER-01 — `.harness/.meta/kaizen-0924/phase8-notes.md` · `.harness/.meta/evidence/phase8.md` 는 공통 정의의 `$NOTES` · `$EVID` 다. 측정 절은 `m ER-01` 한 줄이다
- 커버리지 해소: ER-03 — `.harness/.meta/kaizen-0924/phase8-notes.md` 는 공통 정의의 `$NOTES` 다. `docs/infra-kit/cicd.html` · `docs/infra-kit/infra-test.html` ·
  `docs/infra-kit/gate-result-taxonomy.html` · `.harness/stale-values.yaml` · `plugin.json` · `phase-research-templates.md` · `harness/skills/sprint/SKILL.md` · `.claude/skills/infra-kaizen/SKILL.md` 는
  `m.sh` `ER-03)` 갈래 `toks` 의 인자이고, `rust-kit/README.md` 는 예행 설명, `m.sh` 는 측정 도우미 자체의 이름이다
- 커버리지 해소: AR-01 — `infra-kit/` · `docs/infra/` 는 `unsigned_on` 의 인자, `.harness/` 는 `scope` 블록 줄과 `verify_seal` 이 도는 폴더, `harness/references/contract-schema.md` 는 권장 형태의 출처다
- 검출기는 공백 든 코드 조각 안의 인자를 읽지 못한다 — 위 해소 줄이 전부 그 경우다
- 편집 전부터 있던 경고(markdownlint MD060 · MD025 · MD032 등)는 범위 밖이다 — DG-02 는 더한 줄의 새 경고만 잰다
- notes 에 함께 적는다(조건으로는 재지 않는다): 「그대로 둔 곳」 에 `infra-kit/references/audit-criteria.md:104` · `init-checklist.md:132` · infra-test Gotcha 8(`:24`)의 「1.7+ mocking」,
  infra-test Gotcha 10(`:26`)의 「OpenTofu 1.7+ write-only 인수」, 「Terraform 1.10+ ephemeral」 — 도입 버전을 근거 파일이 확인하지 못했거나(§5) 다루지 않았지만 틀렸다는 근거도 없다.
  `gate-result-taxonomy.md` §재검증 명령 의무 의 스크립트 줄 예시와
  infra-test Step 5 골격 안 `[미검증]` 두 줄 — 스크립트가 찍는 한 줄 형식이라 그대로 두고 리포트가 네 칸으로 옮긴다. 네 칸 이름이 아닌 채 남는 두 자리와 이유 —
  infra-test Step 7 결과 분류 표의 `도구 미설치 · 클러스터/레지스트리 접근 불가` 행(스크립트 상태 표라 둔다) · infra-audit `## Unverifiable Summary` 블록의 `env_gaps` 줄
  (reviewer §9 정본 복제의 4 요건 이름을 따른다). Phase 1 가이드 변경 셋을 반영 · 해당 없음으로
  나눈 짧은 표(infra-kaizen Gotcha 8). ER-03 셋째 값이 0 이 아니면 QA 가 그 커밋 목록부터 보고 판정한다는 한 줄.
  다음 사이클 메모에는 README 가 평가 사례 수를 숫자로 박은 문구(이 Phase 「평가 사례 6 개」 · backend-kit 「평가 사례 8 개」)를 두 킷 함께 다룰지 적는다
- 기능 조건 18 · 전체 조건 줄 28
- 사용자가 할 일: 없음

## 회귀 게이트 — 측정 공통 정의와 봉인 전 실측

모든 조건의 측정은 아래 `common.sh` 와 `m.sh` 를 차례로 `.` 으로 읽은 **bash** 셸에서 돈다 — zsh 는 따옴표 없는 변수를 쪼개지 않고 배열 첨자가 1 부터라, 조립한 명령을
zsh 에서 돌리지 말고 `K=<도우미 폴더> bash -c '. "$K/common.sh" && . "$K/m.sh" && m <조건 ID>'` 꼴로 감싼다. `m` 은 도우미 함수와 두 판 폴더가 없으면
`HELPER_MISSING` · `SNAPSHOT_MISSING` 을 내고 멈춘다 — 그래서 조건마다 `type m` 하나로 정의 확인을 대신한다. 셋째 블록 `new-warnings.sh` 까지 각 블록 첫 `#` 주석 줄(셔뱅 다음)의
이름 그대로 한 폴더에 저장하고 그 폴더를 `K` 에 넣는다. `END_UNRESOLVED` 가 찍히면 셸이 종료 코드 2 로 끝난다. `new-warnings.sh` 옆에는 `node_modules` 를
`/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p1build/node_modules` 로 잇고
`cfg.markdownlint-cli2.jsonc` = `{ "config": { "MD013": false } }` 를 둔다 — 준비 단계 실측(2026-09-25): 그 자리의 `.bin/markdownlint-cli2 --version` 첫 줄이
`markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)`. 없으면 그 폴더에서 `npm install --no-save markdownlint-cli2@0.23.2` 부터 돌린다.
`common.sh` 의 `R` 은 예행 저장소를 가리킬 때만 쓴다 — 비우면 작업 폴더다. `common.sh` 는 두 판을 `${TMPDIR:-/tmp}/p8m.XXXXXX` 에 풀므로 `TMPDIR` 를 스크래치 폴더로 두고 읽는다.
SK-07 은 `python3` 와 PyYAML 이 있어야 돈다 — 준비 단계 실측(2026-09-25): `python3 -c 'import yaml; print(yaml.__version__)'` 가 `6.0.3`.

```bash
# common.sh — 측정 공통 정의. bash 로 읽는다 (zsh 는 배열 첨자가 1 부터이고 따옴표 없는 변수를 쪼개지 않는다)
export LC_ALL=C.UTF-8   # 번역투 정규식이 글자 단위로 돌아야 한다
cd "${R:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/kaizen-0924}" || exit 2
B=4a8ec55f4d874eaaed083af9621f9679693cbdb6                  # 이 Phase 시작 HEAD
SIG='Kaizen-Phase: kaizen-0924-p08-infra-kit'
CF=.harness/sprint-contract-kaizen-0924-p08-infra-kit.md
AM=.harness/sprint-amendments-kaizen-0924-p08-infra-kit.md
NOTES=.harness/.meta/kaizen-0924/phase8-notes.md
EVID=.harness/.meta/evidence/phase8.md
END=$( [ -f "$AM" ] && sed -n 's/^end_sha:[[:space:]]*//p' "$AM" | tail -1 )
if [ -z "$END" ] || ! git rev-parse -q --verify "$END^{commit}" >/dev/null; then
  echo "END_UNRESOLVED — 측정을 멈춘다. HEAD 로 바꿔 재지 않는다"; exit 2
fi
: "${K:?도우미 폴더를 K 에 넣는다}"
CI=docs/infra/platform/cicd.md
RL=docs/infra/research-log.md
GU=infra-kit/skills/infra-guide/SKILL.md
PI=infra-kit/references/principle-index.md
EV=infra-kit/evals/evals.json
RM=infra-kit/README.md
TE=infra-kit/skills/infra-test/SKILL.md
GT=infra-kit/references/gate-result-taxonomy.md
AU=infra-kit/skills/infra-audit/SKILL.md
RV=infra-kit/agents/infra-reviewer.md
AC=infra-kit/references/audit-criteria.md
IC=infra-kit/references/init-checklist.md
IN=infra-kit/skills/infra-init/SKILL.md
SP=harness/skills/sprint/SKILL.md                            # 읽기만 — 판정 세 줄의 원문
OLDPI=infra-kit/skills/infra-guide/references/principle-index.md   # 읽기만 — 옛 사본
FILES=("$CI" "$RL" "$GU" "$PI" "$EV" "$RM" "$TE" "$GT" "$AU" "$RV" "$AC" "$IC" "$IN")
MDS=("$CI" "$RL" "$GU" "$PI" "$RM" "$TE" "$GT" "$AU" "$RV" "$AC" "$IC" "$IN")
T=$(mktemp -d "${TMPDIR:-/tmp}/p8m.XXXXXX") || exit 2; mkdir -p "$T/B" "$T/E"
# 두 판을 풀어 둔 폴더에서 잰다 — 작업 폴더에 남은 다른 Phase 의 미커밋 변경이 끼지 않는다
git archive "$B" | tar -x -C "$T/B"; git archive "$END" | tar -x -C "$T/E"
# sect <파일> <제목 앞부분> — 그 제목부터 같은 깊이 이하의 다음 제목 전까지. 코드 펜스 안의 `#` 줄은 제목으로 보지 않는다
sect() { awk -v h="$2" '
  /^[[:space:]]*(```|~~~)/ { fence = !fence }
  !f && !fence && index($0, h) == 1 { f = 1; lvl = match($0, /[^#]/) - 1; print; next }
  f && !fence && /^#+ / { l = match($0, /[^#]/) - 1; if (l <= lvl) exit }
  f' "$1"; }
# gline <파일> <줄 앞부분> — 그 앞부분으로 시작하는 줄. Gotcha 와 표 행은 한 줄이다
gline() { awk -v p="$2" 'index($0, p) == 1' "$1"; }
# toks <글> <토큰…> — 토큰마다 글 안에서 그 토큰이 든 줄 수
toks() { local s="$1"; shift; for t in "$@"; do printf '%s ' "$(printf '%s\n' "$s" | grep -cF -- "$t")"; done; echo; }
# codeblk — 입력에서 첫 bash 코드 블록 본문만
codeblk() { awk '/^```bash$/{f=1; next} f && /^```$/{exit} f'; }
url()   { grep -oE 'https?://[^ )>"`]+' | sed -E 's/[.,;:]+$//' | sort -u; }
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
K02='(을|를) ?(처리|관리)(합니다|한다)|에 대해서?|하도록 (합니다|한다)|에 의(해|하여)|되어 있(는 경우|을 때)|(표시|적용|호출|생성|반환)(됩니다|된다)'
```

```bash
# m.sh — 조건마다 재는 값을 한 줄로 낸다. common.sh 를 읽은 bash 에서 `m <조건 ID>` 로 부른다
m() {
  local E=$T/E S L fn W
  # 도우미가 하나라도 없으면 grep -c 가 조용히 0 을 낸다 — 멈춘다
  for fn in sect gline toks codeblk url added mine unsigned_on not_other my scope fm_get verify_seal; do
    type "$fn" >/dev/null 2>&1 || { echo "HELPER_MISSING $fn"; return 2; }; done
  [ -n "${T:-}" ] && [ -d "$T/B" ] && [ -d "$E" ] || { echo "SNAPSHOT_MISSING"; return 2; }
  case "$1" in
  SK-01)  # cicd.md 원칙 7 · 자리 · /sprint Step 3 원문과 같은 코드 블록과 판정 표 · 머리 설정
    S=$(sect "$E/$CI" '### 7. 빨간 검사는 고치기 전에 원인부터 가른다')
    toks "$S" '### 7. 빨간 검사는' '이번 커밋 · 남의 미커밋 변경 · 기준 커밋에서 이미 실패 · 환경 · 미확정 가운데 하나로 적는다' '이 분류는 이 킷의 규칙이다' \
      'merge base 가 둘 이상일 수 있으니 어느 것을 골랐는지 적는다' '그 프로젝트의 준비 명령을 붙인다' '**환경 · 비결정성**' '원 실행과 같은 `GITHUB_SHA` · `GITHUB_REF` 를 쓰고' \
      '**미확정**' '「미확정 — 같은 커밋 재실행이 필요하다」' '같은 검사에서 같은 핵심 오류가 날 때만이다' '필수 검사를 건너뛰거나 통과로 적지 않는다' '원인 증명은 아니다' \
      '`gh run list --commit <sha>`' '`--workflow` 가 없어' '성공 · skipped · neutral' '`<고른 커밋>..origin/<기준 가지>` 로 빠지는 커밋 범위를 함께 보고한다' \
      'https://git-scm.com/docs/git-merge-base' 'https://cli.github.com/manual/gh_run_list' 'https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs' \
      'https://docs.github.com/en/actions/reference/runners/github-hosted-runners' 'https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches'
    # 원칙 7 이 원칙 6 뒤 · `## 수치/기준값` 앞에 있다 — 줄 번호 셋이 오름차순이면 1
    awk '/^### 6\. /{a=NR} /^### 7\. 빨간 검사는/{b=NR} /^## 수치\/기준값/{c=NR} END{print (a && b && c && a<b && b<c) ? 1 : 0}' "$E/$CI"
    # 알려진 답 — 코드 블록과 판정 표가 /sprint Step 3 원문과 글자 그대로 같다. 빈 블록끼리 같다고 나오지 않게 줄 수도 본다
    W=$(sect "$E/$SP" '### Step 3: 빌드/분석 검증')
    echo "code_same=$(diff <(printf '%s\n' "$S" | codeblk) <(printf '%s\n' "$W" | codeblk) >/dev/null && echo 1 || echo 0) code_lines=$(printf '%s\n' "$S" | codeblk | grep -c .)" \
      "table_same=$(diff <(printf '%s\n' "$S" | grep '^|') <(printf '%s\n' "$W" | grep '^|') >/dev/null && echo 1 || echo 0) table_lines=$(printf '%s\n' "$S" | grep -c '^|')"
    echo "$(fm_get "$E/$CI" version) $(fm_get "$E/$CI" last_updated) $(grep -cF '아티팩트 관리, 빨간 검사의 원인 가르기를 다룬다.' "$E/$CI")" ;;
  SK-02)  # infra-guide Gotcha 14 · 번호
    L=$(gline "$E/$GU" '14. **빨간 CI 를 이번 변경 탓으로 단정하기 전에 원인부터 가른다 (enforcement 등급 E1)**')
    toks "$L" '14. **빨간 CI' '`git merge-base HEAD origin/<기준 가지>`' '이번 커밋 · 남의 미커밋 변경 · 기준 커밋에서 이미 실패 · 환경 · 미확정 가운데 하나로 적는다' \
      '가를 근거가 없으면 미확정으로 두고 같은 커밋 재실행을 권한다' '기준 커밋에서 이미 실패하던 검사도 통과로 적거나 건너뛰라고 하지 않는다' \
      '`gh run list --branch <가지> --status success --limit 1` 결과를 필수 검사가 전부 통과한 커밋으로 읽지 않는다' '`docs/infra/platform/cicd.md` 원칙 7 이 SSOT 다' '실측(2026-09-18)'
    sect "$E/$GU" '# Gotchas' | grep -oE '^[0-9]+\. \*\*' | tr -dc '0-9\n' | paste -sd' ' - ;;
  SK-03)  # 키워드 두 자리 — infra-guide Step 1 cicd 행 · principle-index cicd 행 · 옛 사본은 그대로
    L=$(sect "$E/$GU" '## Step 1: 탐색' | awk 'index($0, "| cicd |") == 1')
    toks "$L" 'CI 실패, 빨간 검사, 재실행'
    L=$(gline "$E/$PI" '| cicd |')
    toks "$L" 'CI 실패, 빨간 검사, 재실행' '`docs/infra/platform/cicd.md`'
    echo "keywords_same=$( [ -n "$L" ] && [ "$(sect "$E/$GU" '## Step 1: 탐색' | awk -F'|' 'index($0, "| cicd |") == 1 {print $3}')" = "$(printf '%s\n' "$L" | awk -F'|' '{print $3}')" ] && echo 1 || echo 0)" \
      "oldcopy_same=$(diff "$T/B/$OLDPI" "$E/$OLDPI" >/dev/null && echo 1 || echo 0)" ;;
  SK-04)  # evals 사례 6 · run-evals · README 검증 절
    python3 - "$E/$EV" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8")); ev = d["evals"]
ids = [e.get("id") for e in ev]; e6 = [e for e in ev if e.get("id") == 6]
e = e6[0] if len(e6) == 1 else {}
a = [x.get("text", "") for x in e.get("assertions", [])]
ty = {x.get("type") for x in e.get("assertions", [])}
print(len(ev), ids == list(range(1, len(ev) + 1)), e.get("skill"), "빨간" in e.get("prompt", ""), "PR" in e.get("prompt", ""), len(a), ty <= {"behavior", "output"},
      sum("cicd.md 원칙 7" in t for t in a),
      sum("git merge-base" in t for t in a),
      sum("통과로 적거나 건너뛰라고 하지 않는다" in t for t in a),
      sum("미확정으로 두고 같은 커밋 재실행을 권한다" in t for t in a))
PY
    ( cd "$E" && python3 scripts/run-evals.py infra-kit > "$T/re.txt" 2>&1; echo "rc=$? $(grep -E '^Total: ' "$T/re.txt")" )
    echo "$(grep -cF '평가 사례 6 개의 구조 검증' "$E/$RM") $(grep -cF '4 스킬 assertion 전수 검증' "$E/$RM") $(grep -cF '등록된 검사 전부 (개수는 `harness/docs/guides/plugin-validation-guide.md` 가 정한다)' "$E/$RM") $(grep -cF '7 카테고리 구조 감사' "$E/$RM")" ;;
  SK-05)  # infra-test · gate-result-taxonomy 의 미검증 네 칸 · 가이드 칸 이름 · 옛 표기
    L=$(gline "$E/$TE" '12. **검사 도구 미설치는 PASS 가 아니라')
    toks "$L" '`[미검증] TOOL_OR_ENV_MISSING` 을 달고 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 채워 개별 표기한다' '막는 것은 `command -v <도구>` 와 그 출력이고' \
      '`없음 — 이유` 를 적는다' '(네 칸 정의: `harness/docs/guides/skill-design-guide.md` §3.7 Completion Evidence Gate 3 항)'
    S=$(sect "$E/$TE" '### Step 8: 결과 보고')
    toks "$S" '아래 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 채워 개별 나열' '네 칸 중 하나라도 비면 그 항목은 `UNVERIFIED_ENV` 로 인정되지 않는다' \
      '    시도한 우회: k8s/*.yaml 을 python3 YAML 파서로 읽기만 함' '    시도한 우회: 없음 — 이미지 안 파일 구조를 볼 다른 도구가 이 환경에 없다'
    # 보고 예시의 칸 줄 수 — 미검증 두 건이 네 칸씩
    echo "$(printf '%s\n' "$S" | grep -c '^    막는 것: \$ command -v ') $(printf '%s\n' "$S" | grep -c '^    시도한 우회: ') $(printf '%s\n' "$S" | grep -c '^    통제 불가 사유: ') $(printf '%s\n' "$S" | grep -c '^    재검증 명령: ')"
    S=$(sect "$E/$GT" '## 재검증 명령 의무')
    toks "$S" '**막는 것** 칸으로 옮기고 나머지 세 칸(시도한 우회 · 통제 불가 사유 · 재검증 명령)을 채운다' '§3.7 Completion Evidence Gate 3 항이 SSOT 다' '하나라도 비면 `UNVERIFIED_ENV` 로 인정되지 않는다'
    toks "$(cat "$E/harness/docs/guides/skill-design-guide.md")" '   - **막는 것** —' '   - **시도한 우회** —' '   - **통제 불가 사유** —' '   - **재검증 명령** —'
    grep -rF -e '<도구> 미설치 — 재검증: <명령>' -e '재검증 명령이 없으면 그 항목은' -e 'kubeconform 미설치 — 재검증: brew install kubeconform && kubeconform -strict k8s/' \
      -e 'container-structure-test 미설치 — 재검증:' "$E/infra-kit" | grep -c . ;;
  SK-06)  # infra-audit · infra-reviewer 의 미검증 네 칸 · reviewer §9 복제본은 그대로 · 옛 표기
    L=$(gline "$E/$AU" '11. **미검증 항목 마커 프로토콜**')
    toks "$L" '근거에 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 채워라' '막는 것: `kubectl get ns` 와 그 접근 거부 출력' '시도한 우회: manifest 정적 리뷰' \
      '통제 불가 사유: 감사자에게 production 클러스터 자격증명이 없다' '재검증 명령: 자격증명을 받은 뒤 같은 `kubectl get ns`' '네 칸 중 하나라도 비면 `[미검증:INVALID]` 다'
    toks "$(gline "$E/$AU" '12. **도구·규칙 소스 부재를')$(printf '\n')$(sect "$E/$AU" '## Step 4: 최종 판정')" '로 명시하고 네 칸(Gotcha 11)을 채워라' '소스를 못 읽었으면 Gotcha 11 의 네 칸'
    S=$(sect "$E/$RV" '## 출력 포맷')
    toks "$S" '와 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 근거 열에 적는다' '하나라도 비면 `INVALID` 다' \
      '막는 것: `terraform state pull` 과 그 접근 거부 출력 · 시도한 우회: `main.tf:15` `ephemeral` 블록 정적 확인 · 통제 불가 사유: 백엔드 자격증명이 없다 · 재검증 명령:'
    echo "s9_same=$(diff <(sect "$T/B/$RV" '## 9. Canonical Unverified-Evidence Protocol') <(sect "$E/$RV" '## 9. Canonical Unverified-Evidence Protocol') >/dev/null && echo 1 || echo 0) s9_lines=$(sect "$E/$RV" '## 9. Canonical Unverified-Evidence Protocol' | grep -c .)"
    grep -rF -e '근거에 이유를 기술하라' -e 'manifest 정적 리뷰만 수행' -e '`[미검증]` 태그 + 이유' -e '또는 소스 부재 사유 명시' -e '1차 `terraform state pull`' "$E/infra-kit" | grep -c . ;;
  SK-07)  # infra-test Step 7 알려진 답 대조 문단 · 그 문단이 적은 값을 $END 판 골격으로 실제로 돌린 결과
    S=$(sect "$E/$TE" '### Step 7: 실행 검증')
    toks "$S" '**생성한 검사 스크립트는 실제 대상보다 답을 아는 작은 입력에 먼저 돌린다 (알려진 답 대조 · skill-design-guide §3.7).**' '`WF_DIR=<임시 폴더> bash tests/ci-validation.sh`' \
      '`열거된 uses 참조 수: 3`' '참조 단위 `VIOLATION       :` 줄 2 개' '집계 `VIOLATION=1`(규칙 단위로 센다)' 'exit 1 이 나와야 한다' '다르면 실제 대상에 돌리지 말고 스크립트나 입력부터 고친다'
    python3 -c 'import yaml' 2>/dev/null || { echo "YAML_MISSING"; return 2; }
    awk '/^# tests\/ci-validation\.sh/{f=1} f && /^```$/{exit} f' "$E/$TE" | { echo '#!/usr/bin/env bash'; cat; } > "$T/gate.sh"
    mkdir -p "$T/ka" "$T/ok"
    printf '%s\n' 'name: ci' 'on: push' 'jobs:' '  build:' '    runs-on: ubuntu-latest' '    steps:' '      - uses: actions/checkout@v4' \
      '      - uses: actions/setup-node@0123456789abcdef0123456789abcdef01234567' '      - uses: aws-actions/configure-aws-credentials@v4' > "$T/ka/ci.yml"
    sed -E 's/@v4$/@0123456789abcdef0123456789abcdef01234567/' "$T/ka/ci.yml" > "$T/ok/ci.yml"
    for d in ka ok; do
      ( cd "$T" && WF_DIR="$T/$d" bash "$T/gate.sh" > "$T/$d.out" 2>&1; echo "$d exit=$? refs=$(sed -n 's/^열거된 uses 참조 수: \([0-9]*\).*/\1/p' "$T/$d.out") viol_lines=$(grep -c '^VIOLATION       : ' "$T/$d.out") $(grep -oE '^VIOLATION=[0-9]+' "$T/$d.out")" ); done ;;
  SK-08)  # kubeconform 스키마 버전 — 고정 값 대신 변수, 그 줄을 실제로 돌린 결과
    S=$(sect "$E/$TE" '### Step 6: K8s Manifest 테스트 생성')
    toks "$S" 'K8S_VERSION="${K8S_VERSION:?대상 클러스터의 Kubernetes 버전을 넣는다}"' 'kubeconform -strict -kubernetes-version "$K8S_VERSION" k8s/*.yaml' '# 고정 값을 박으면 클러스터를 올린 뒤에도 옛 스키마로 검증한다'
    grep -rF -e '-kubernetes-version 1.' "$E/infra-kit" | grep -c .
    L=$(printf '%s\n' "$S" | awk 'index($0, "K8S_VERSION=\"${K8S_VERSION:?") == 1')
    echo "unset_rc=$(env -u K8S_VERSION bash -c "$L" >/dev/null 2>&1; echo $?) unset_msg=$(env -u K8S_VERSION bash -c "$L" 2>&1 | grep -cF '대상 클러스터의 Kubernetes 버전을 넣는다') set_rc=$(K8S_VERSION=1.37.1 bash -c "$L" >/dev/null 2>&1; echo $?)" ;;
  SK-09)  # OpenTofu 「1.7+ native state encryption」 네 자리
    grep -rE '1\.7\+(는)? native state encryption' "$E/infra-kit" | grep -c .
    echo "$(gline "$E/$AC" '| State encryption |' | grep -cF '| State encryption | OpenTofu native state encryption 또는') $(grep -cF -- '- [ ] **State encryption** — OpenTofu는 native state encryption,' "$E/$IC") $(grep -cF -- '- [ ] **OpenTofu 대안 검토** — native state encryption, v1.9+' "$E/$IC") $(grep -cF 'OpenTofu native state encryption 을 권장 규격에 포함한다.' "$E/$IN")" ;;
  SK-10)  # README — cicd 요약 · 2026-04-24 이력 줄 정정 표시 · 표 구성 (infra-kaizen Gotcha 9)
    echo "$(grep -cF -- '- **cicd** — GitHub Actions/GitLab CI, OIDC, 최소 권한, 캐싱, self-hosted runner, 빨간 검사 원인 가르기' "$E/$RM") $(grep -cF 'OpenTelemetry 3 signals stable(2026-08-13 정정 — signal 별로 상태가 다르다, infra-guide Gotcha 13)' "$E/$RM")"
    echo "$(grep -c '^| `/infra-' "$E/$RM") $(grep -c '^| `infra-reviewer` |' "$E/$RM") $(grep -cE '^### (Platform|Operations|Security)$' "$E/$RM")" ;;
  SK-11)  # research-log 새 항목 · 자리 · 머리 설정 · 옛 항목은 그대로
    S=$(sect "$E/$RL" '## [2026-09-24] - Phase 8 kaizen')
    toks "$S" '## [2026-09-24] - Phase 8 kaizen' '`backend-family:P3`' '### 조회한 외부 소스 (근거 파일 `.harness/.meta/evidence/phase8.md`)' '### 변경 내역' '### 사실 정정' \
      '**OpenTofu 1.7+ 가 남아 있었다**' '### 조회만 하고 규칙으로 올리지 않은 것 (근거 파일 §3)' '### 다음 사이클 후보' '세 분류를 규범으로 정한 곳은 찾지 못했다'
    echo "first=$(awk '/^## \[/{print; exit}' "$E/$RL" | grep -cxF '## [2026-09-24] - Phase 8 kaizen') $(fm_get "$E/$RL" version) $(fm_get "$E/$RL" last_updated)"
    echo "history_same=$(diff <(awk '/^## \[2026-08-13\] - Phase 8 kaizen$/{f=1} f' "$T/B/$RL") <(awk '/^## \[2026-08-13\] - Phase 8 kaizen$/{f=1} f' "$E/$RL") >/dev/null && echo 1 || echo 0) history_lines=$(awk '/^## \[2026-08-13\] - Phase 8 kaizen$/{f=1} f' "$E/$RL" | grep -c .)" ;;
  ER-01)  # 새로 생긴 URL 이 근거 파일에 있다 — 열세 파일은 파일마다 편집 전 판과 비교, notes 는 URL 전부
    for f in "${FILES[@]}"; do comm -13 <(url < "$T/B/$f") <(url < "$E/$f"); done | sort -u | comm -23 - <(url < "$E/$EVID") | grep -c .
    # notes 가 없으면 입력이 비어 조용히 0 이 된다 — 없다고 찍는다
    if [ -f "$E/$NOTES" ]; then url < "$E/$NOTES" | comm -23 - <(url < "$E/$EVID") | grep -c .; else echo NOTES_MISSING; fi ;;
  ER-02)  # 더한 줄의 번역투 6 종
    added | grep -cE "$K02" ;;
  ER-03)  # notes 문자열 · 공유 파일과 다른 Phase 파일을 건드린 커밋
    git cat-file -e "$END:$NOTES" && echo notes_committed=1 || echo notes_committed=0
    toks "$(cat "$E/$NOTES")" 'backend-family:P3' 'docs/infra-kit/cicd.html' 'docs/infra-kit/infra-test.html' 'docs/infra-kit/gate-result-taxonomy.html' \
      '.harness/stale-values.yaml' 'plugin.json' '§Canonical Unverified-Evidence Protocol' 'phase-research-templates.md' 'harness/skills/sprint/SKILL.md' \
      'Flux v2.9' '.claude/skills/infra-kaizen/SKILL.md' \
      '## 반영한 처리 배정표 키' '## 미반영 키와 사유' '## 넘기는 것' '## changelog 한 단락' '## 킷 로그 한 단락' '## 다음 사이클 메모'
    not_other "$B" "$END" "$SIG" .claude-plugin/marketplace.json infra-kit/.claude-plugin/plugin.json README.md CLAUDE.md \
      .harness/.meta/orchestrator-audit-log.md .harness/.meta/kaizen-failure-count.yaml .claude/kaizen-input/insights-report.md \
      .github/workflows/ci.yml .harness/stale-values.yaml .claude/skills docs/infra-kit harness scripts | grep -c . ;;
  AR-01)  # 허용 경로 · 서명 · 봉인 · 범위 선언 블록
    unsigned_on "$B" "$END" "$SIG" infra-kit docs/infra | grep -c .
    echo "$(my | grep -v '^\.harness/' | grep -vxF -f <(printf '%s\n' "${FILES[@]}") | grep -c .) $(my | grep -cxF -f <(printf '%s\n' "${FILES[@]}"))"
    find .harness -type f -name 'sprint-contract*.md' -print0 | while IFS= read -r -d '' f; do verify_seal "$f"; done \
      | awk '$1=="SEAL_BROKEN"{print $2}' | sed 's#^\./##' | sort -u | comm -12 - <( { my; echo "$CF"; } | sort -u) | grep -c .
    verify_seal "$E/$CF" | cut -d' ' -f1
    diff <(scope "$E/$CF" | grep -vxF '.harness/' | sort) <(printf '%s\n' "${FILES[@]}" | sort) >/dev/null && echo "scope_same=1" || echo "scope_same=0"
    scope "$E/$CF" | grep -cxF '.harness/' ;;
  AR-02)  # 연결 — 원칙 색인이 가리키는 문서 · 색인을 읽는 쪽 · 상태어 정본과 감사 기준을 읽는 쪽
    python3 - "$E" <<'PY'
import os, sys
e = sys.argv[1]
row = [l for l in open(os.path.join(e, "infra-kit/references/principle-index.md"), encoding="utf-8") if l.startswith("| cicd |")]
rel = row[0].split("|")[3].strip().strip("`") if len(row) == 1 else ""
p = os.path.join(e, rel) if rel else ""
ok = bool(p) and os.path.isfile(p) and any(l.startswith("### 7. 빨간 검사는") for l in open(p, encoding="utf-8"))
print(len(row), rel or "-", int(ok))
PY
    echo "$(grep -cF '`infra-kit/references/principle-index.md`에서 해당 카테고리의 원칙 문서 경로를 찾아 읽고' "$E/$GU")" \
      "$(grep -cxF -- '- infra-kit/references/gate-result-taxonomy.md — 결과 상태 5 종 · 머리말 4 카운터 · 핵심/선택 도구 분리' "$E/$RV")" \
      "$(grep -cxF -- '- infra-kit/references/audit-criteria.md — rule 정본 (카테고리 순서 SSOT)' "$E/$RV")" \
      "$(grep -cxF -- '- ../../references/gate-result-taxonomy.md — 결과 상태 5 종 · 머리말 4 카운터 (SSOT)' "$E/$AU")" \
      "$(grep -cF -- '- `../../references/gate-result-taxonomy.md` — 게이트 결과 상태 5 종' "$E/$TE")" \
      "$(sect "$E/$GT" '## 소비처' | grep -c '^| `infra-kit/')" ;;
  SC-00)  # N/A 사유 — 이 Phase 서명 커밋이 릴리스 스크립트 · marketplace · plugin.json 을 건드리지 않았다
    my | grep -cE '^(scripts/release\.sh|\.claude-plugin/marketplace\.json|[^/]+/\.claude-plugin/plugin\.json)$' ;;
  DG-01|DG-03)  # N/A 사유 — commands.analyze · commands.test 가 재는 파일과 이 Phase 커밋 파일의 교집합
    my | grep -c '^scripts/release.sh$' ;;
  DG-04)  # N/A 사유 — 구동할 진입점 확장자
    my | grep -cE '\.(dart|ts|tsx|js|rs|go|py|sh)$' ;;
  RE-01)  # N/A 사유 — 문서 · 데이터 밖 파일
    printf '%s\n' "${FILES[@]}" | grep -cvE '\.(md|json)$' ;;
  RE-02)  # 판정 표는 한 곳 — 머리 줄이 있는 파일
    grep -rlF '| 공용 작업 폴더 | `HEAD` 임시 | `FORK_BASE` 임시 | 판정 |' "$E/infra-kit" "$E/docs/infra" | sed "s#^$E/##" ;;
  AP-01)  # 더한 줄에 이 킷 플러그인 버전 값 — 값은 plugin.json 에서 읽는다
    L=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$E/infra-kit/.claude-plugin/plugin.json")
    echo "version=$L $(added | grep -cF -- "$L")" ;;
  AP-03)  # 더한 펜스 줄 수 · 마크다운 열두 파일의 언어 힌트 없는 여는 펜스
    echo "added_fence=$(added | grep -cE '^\+[[:space:]]*(```|~~~)') bare_open=$(for f in "${MDS[@]}"; do awk '/^[[:space:]]*(```|~~~)/{ if (!o) { o=1; t=$0; sub(/^[[:space:]]*(```|~~~)/, "", t); if (t ~ /^[[:space:]]*$/) n++ } else o=0 } END{print n+0}' "$E/$f"; done | awk '{s+=$1} END{print s+0}')" ;;
  AP-04)  # frontmatter — 첫 블록이 편집 전과 같은지 / name 줄 수. README AUTO 구간이 읽는 값이 안 바뀐다
    for f in "$GU" "$TE" "$AU" "$IN" "$RV"; do
      L=$(basename "$f" .md); [ "$L" = SKILL ] && L=$(basename "$(dirname "$f")")
      printf '%s/%s ' "$(diff <(awk 'NR==1&&/^---/{fm=1;next} fm&&/^---/{exit} fm' "$T/B/$f") <(awk 'NR==1&&/^---/{fm=1;next} fm&&/^---/{exit} fm' "$E/$f") >/dev/null && echo 1 || echo 0)" \
        "$(awk 'NR==1&&/^---/{fm=1;next} fm&&/^---/{exit} fm' "$E/$f" | grep -cxF "name: $L")"; done; echo ;;
  DG-02)  # markdownlint — 더한 줄의 새 경고 · evals.json 파싱
    for f in "${MDS[@]}"; do k=$(printf '%s' "$f" | tr '/' '_'); cp "$T/B/$f" "$T/$k.0.md"; cp "$E/$f" "$T/$k.md"; bash "$K/new-warnings.sh" "$T/$k.0.md" "$T/$k.md"; done
    python3 -c 'import json,sys; json.load(open(sys.argv[1], encoding="utf-8")); print("json_ok")' "$E/$EV" ;;
  DG-05)  # 저장소 검사 — $END 판을 git 저장소로 만든 사본에서 돈다 (작업 폴더의 다른 Phase 미커밋 변경이 끼지 않는다)
    local G=$T/G; rm -rf "$G"; cp -R "$E" "$G"
    git -C "$G" init -q && git -C "$G" add -A && git -C "$G" -c user.name=m -c user.email=m@m commit -qm snap || return 2
    ( cd "$G" && python3 scripts/validate-plugin.py infra-kit > "$T/vp.txt" 2>&1 )
    echo "$(grep -cE '^  V([1-9]|10) ' "$T/vp.txt") $(grep -E '^  V([1-9]|10) ' "$T/vp.txt" | grep -cE 'ERROR|FAIL')"
    # sync-evals 는 킷 이름 인자가 없다 — infra-kit 머리 줄을 읽었는지와 그 아래 어긋남 줄 수만 센다
    ( cd "$G" && python3 scripts/sync-evals.py --check-only > "$T/se.txt" 2>&1 )
    echo "$(grep -cxF '→ infra-kit' "$T/se.txt") $(awk '/^→ /{f=($2=="infra-kit"); next} f && NF' "$T/se.txt" | grep -c .)"
    ( cd "$G" && python3 scripts/check-stale-values.py > "$T/sv.txt" 2>&1 ); echo "stale_rc=$? $(grep -cF -f <(printf '%s\n' "${FILES[@]}") "$T/sv.txt")" ;;
  DG-06)  # 사이클 검사 — 이 Phase 몫 줄만 본다. docs-site-regen 은 Final F2 몫
    python3 scripts/validate-post-kaizen.py --since "$B" --verbose > "$T/vpk.txt" 2>&1
    grep -E '\] . (scope-isolation|doc-contracts): ' "$T/vpk.txt" | awk '{print $5, $2}'
    # doc-contracts 가 검사한 경로 수와 그 가운데 이 Phase 파일 수 — FAIL 이 나도 이 Phase 몫인지 가른다
    python3 scripts/validate-doc-contracts.py -v 2>&1 | awk -F' → ' '/^ *검사: /{a=$1; sub(/^ *검사: /,"",a); sub(/:[0-9]+$/,"",a); print a; print $2}' | sort -u > "$T/dc.txt"
    echo "doc_checked=$(grep -c . "$T/dc.txt") doc_mine=$(comm -12 "$T/dc.txt" <(my) | grep -c .)"
    # 위반 커밋 목록을 읽은 수와 그 가운데 이 Phase 서명 커밋 수. 목록을 못 읽으면 둘째 값이 조용히 0 이 되므로 첫 값을 함께 본다
    awk '/ scope-isolation: /{f=1;next} /^\[ /{f=0} f&&/^ +[0-9a-f]{7,40}$/{print $1}' "$T/vpk.txt" > "$T/viol.txt"
    echo "violators=$(grep -c . "$T/viol.txt") mine=$(while read -r c; do git log -1 --format=%B "$c" | grep -qxF "$SIG" && echo "$c"; done < "$T/viol.txt" | grep -c .)" ;;
  *) echo "UNKNOWN $1"; return 2 ;;
  esac
}
```

```bash
#!/usr/bin/env bash
# new-warnings.sh <옛 파일> <새 파일> — 새 파일에서 더한 줄에 걸린 경고만 센다. 줄이 밀리므로 전체 수 차이로 세지 않는다
# 줄 번호는 경로 뒤 첫 번째 숫자다. 탐욕 매치(^[^ ]*:)로 뽑으면 열 번호가 줄 번호로 둔갑한다 (실측 2026-09-24)
# 린터가 안 돌면 경고 0 이 조용히 나온다 — 돌았다는 줄(Linting: 1 file)이 없으면 멈춘다 (실측 2026-09-25: 옆에 node_modules 가 없어 0)
set -u
DIR=$(cd "$(dirname "$0")" && pwd)
ADDED=$(git diff --no-index -U0 -- "$1" "$2" | awk '/^@@/{split($3,a,","); s=substr(a[1],2)+0; n=(a[2]==""?1:a[2]+0); for(i=0;i<n;i++) print s+i}' | sort -u)
OUT=$("$DIR/node_modules/.bin/markdownlint-cli2" --config "$DIR/cfg.markdownlint-cli2.jsonc" "$2" 2>&1)
printf '%s\n' "$OUT" | grep -q '^Linting: 1 file' || { echo "LINT_NOT_RUN $2"; exit 2; }
LINES=$(printf '%s\n' "$OUT" | grep -E ':[0-9]+(:[0-9]+)? (error|warning) ' | sed -E 's#^([^:]*):([0-9]+).*#\2#' | sort -u)
NEWW=$(comm -12 <(printf '%s\n' "$ADDED" | grep . | sort) <(printf '%s\n' "$LINES" | grep . | sort) | wc -l | tr -d ' ')
echo "total_warning_lines=$(printf '%s\n' "$LINES" | grep -c .) added_lines=$(printf '%s\n' "$ADDED" | grep -c .) new_warnings=$NEWW"
```

**예행.** 시작 커밋에서 레포를 스크래치로 복제해(`p8d/rehearse.sh`) BUILD 가 할 커밋을 흉내 냈다 — 봉인 커밋(이 계약 초안에 digest 를 적은 판) → 다른 Phase 서명 커밋 하나
(`rust-kit/README.md`, 걸러져야 한다) → `mock.py` 를 적용한 구현 커밋 둘(`docs/infra/` 둘 · `infra-kit/` 열하나) → `end_sha` → notes 모의본 → `end_sha` 한 줄 더.
변형 넷은 같은 흐름에 커밋 하나를 더한다: `unsigned-shared`(서명 없이 루트 `README.md`) · `unsigned-mine`(서명 없이 `infra-kit/README.md`) ·
`signed-outside`(서명하고 `infra-kit/.claude-plugin/plugin.json`) · `cross-phase`(서명하고 `harness/skills/sprint/SKILL.md` 와 `infra-kit/skills/infra-test/SKILL.md` 한 커밋).
시작 커밋 판 값은 같은 측정을 `$T/E` 자리에 시작 커밋 판을 두고 돌린 것이다(`p8d/run0.sh`).

| 조건 | 예행 판 (요구값) | 시작 커밋 판 | 양성 · 음성 대조 |
| --- | --- | --- | --- |
| SK-01 | `1` 스물하나 · `1` · `code_same=1 code_lines=9 table_same=1 table_lines=5` · `0.2.0 2026-09-25 1` | `0` 스물하나 · `0` · `code_same=0 code_lines=0 table_same=0 table_lines=0` · `0.1.0 2026-04-04 0` | 문장 삭제 24 개 모두 출력이 바뀜(코드 블록 한 줄 · 판정 줄 하나를 지운 사본 포함 — `code_same=0` · `table_same=0`) |
| SK-02 | `1` 여덟 · `1 … 14` | `0` 여덟 · `1 … 13` | 문장 삭제 8 개 |
| SK-03 | `1 ` · `1 1 ` · `keywords_same=1 oldcopy_same=1` | `0 ` · `0 1 ` · `keywords_same=1 oldcopy_same=1` | principle-index 행에서 `빨간 검사, ` 를 뺀 사본 → `0 1 ` · `keywords_same=0` · 옛 사본 한 칸 변경 → `oldcopy_same=0` · 문장 삭제 2 개 |
| SK-04 | `6 True infra-guide True True 4 True 1 1 1 1` · `rc=0 Total: 6 passed, 0 failed` · `1 0 1 0` | `5 True None False False 0 True 0 0 0 0` · `rc=0 Total: 5 passed, 0 failed` · `0 1 0 1` | 음성: 사례 6 assertion 하나의 type 을 `check` 로 → `rc=1 Total: 5 passed, 1 failed` · 문장 삭제 4 개 |
| SK-05 | `1 1 1 1 ` · `1 1 1 1 ` · `2 2 2 2` · `1 1 1 ` · `1 1 1 1 ` · `0` | `0 0 0 0 ` · `0 0 0 0 ` · `0 0 0 0` · `0 0 0 ` · `1 1 1 1 ` · `4` | 여섯째 값이 양성 대조 · 문장 삭제 11 개 |
| SK-06 | `1 1 1 1 1 1 ` · `1 1 ` · `1 1 1 ` · `s9_same=1 s9_lines=60` · `0` | `0` 여섯 · `0 0 ` · `0 0 0 ` · `s9_same=1 s9_lines=60` · `4` | 음성: §9 한 글자 → `s9_same=0` · 다섯째 값이 양성 대조 · 문장 삭제 11 개 |
| SK-07 | `1` 일곱 · `ka exit=1 refs=3 viol_lines=2 VIOLATION=1` · `ok exit=0 refs=3 viol_lines=0 VIOLATION=0` | `0` 일곱 · 둘째 · 셋째 줄 같음 | 음성: `if SHA.search(ref):` → `if "@" in ref:` 사본에서 `ka exit=0 refs=3 viol_lines=0 VIOLATION=0` · 문장 삭제 7 개 |
| SK-08 | `1 1 1 ` · `0` · `unset_rc=127 unset_msg=1 set_rc=0` | `0 0 0 ` · `1` · `unset_rc=0 unset_msg=0 set_rc=0` | 둘째 값이 양성 대조 · 문장 삭제 3 개 |
| SK-09 | `0` · `1 1 1 1` | `4` · `0 0 0 0` | 첫 값이 양성 대조 · 문장 삭제 4 개 |
| SK-10 | `1 1` · `4 1 3` | `0 0` · `4 1 3` | 문장 삭제 2 개 |
| SK-11 | `1` 아홉 · `first=1 1.4.0 2026-09-25` · `history_same=1 history_lines=341` | `0` 아홉 · `first=0 1.3.0 2026-08-13` · `history_same=1 history_lines=341` | 음성: 2026-08-13 항목의 한 구절을 지운 사본 → `history_same=0` · 문장 삭제 9 개 |
| SC-00 | `0` | — | 변형 `signed-outside` → 1 |
| ER-01 | `0` · `0` (새 URL 열둘 전부 근거 파일에 있다 · notes 모의본의 URL 하나도 근거 파일에 있다) | — | cicd.md 끝에 `https://example.invalid/x` → `1` · `0` · notes 끝에 같은 URL → `0` · `1` · notes 를 지운 사본 → `0` · `NOTES_MISSING` |
| ER-02 | `0` (더한 줄 159) | — | 첫 예행 1(infra-audit Gotcha 12 원래 문구) → 고친 뒤 0 · infra-guide 끝에 「이 값이 적용된다」 → 1 |
| ER-03 | `notes_committed=1` · 열일곱 값 모두 1 이상(예행 모의 notes 는 모두 1) · `0` | — | 변형 `unsigned-shared` · `signed-outside` · `cross-phase` → 셋째 값 셋 다 1 · 변형 `unsigned-mine` → 0(`infra-kit/` 는 공유 경로 밖 — AR-01 ① 이 잡는다) · 모의 notes 에서 `plugin.json` 줄 삭제 → 둘째 줄 여섯째 값 0 · 두 키를 한 줄씩 더 → 첫째 · 여섯째 값 2 |
| AR-01 | `0` · `0 13` · `0` · `SEAL_OK` · `scope_same=1` · `1` | — | `unsigned-mine` ① 1 · `signed-outside` ② `1 13` · `cross-phase` ② `1 13` · 봉인 뒤 조건 줄 한 글자를 바꾼 커밋 → ③ 1 · ④ `SEAL_BROKEN` |
| AR-02 | `1 docs/infra/platform/cicd.md 1` · `1 1 1 1 1 3` | `1 docs/infra/platform/cicd.md 0` · `1 1 1 1 1 3` | 알려진 답 — 경로는 원래 맞고 제목만 새로 생긴다 |
| RE-01 · DG-01 · DG-03 · DG-04 | `0` · `0` · `0` · `0` | — | DG-04: `a/b.dart` · `c.sh` · `d.md` → 2 · RE-01: `x.sh` → 1 |
| RE-02 | `docs/infra/platform/cicd.md` 한 줄 | 0 줄 | — |
| AP-01 | `version=0.3.1 0` | `version=0.3.1 0` | README 끝에 「버전 0.3.1」 → 1 |
| AP-03 | `added_fence=2 bare_open=0` | `added_fence=0 bare_open=0` | README 끝에 언어 힌트 없는 펜스 한 벌 → `added_fence=4 bare_open=1` |
| AP-04 | `1/1` 다섯 | — | infra-guide description 한 글자 → `0/1 1/1 1/1 1/1 1/1` · 음성은 DG-05 |
| DG-02 | 열두 줄 `new_warnings=0` · `json_ok` | — | cicd.md 끝 `#bad heading` → 첫 줄 `new_warnings=1` |
| DG-05 | `10 0` · `1 0` · `stale_rc=0 0` | — | `name:` 을 깬 사본 → `10 1` · `zz-test` 스킬을 더한 사본 → `1 1` · 「OWASP 권장 12」 를 넣은 사본 → `stale_rc=1 1` |
| DG-06 | `scope-isolation: PASS` · `doc-contracts: PASS` · `doc_checked=2 doc_mine=0` · `violators=0 mine=0` | — | 변형 `cross-phase` → `scope-isolation: FAIL` · `violators=1 mine=1` |

예행 값은 bash 5.3.9 와 `/bin/bash` 3.2.57 두 해석기에서 조건 스물여덟 전부 같았다(`p8d/final-run.txt` · `p8d/final-run-bash32.txt`).
검토(`phase8-review.md`) 반영 뒤 예행을 `p8x/rh` 에 새로 만들어 다시 쟀다 — 조건 스물여덟 출력이 두 해석기 모두 위 표와 같았고(`p8x/final-run.txt` · `p8x/final-run-bash32.txt`),
변형 넷 · 대조 · 문장 삭제 85 도 같았다(`p8x/var-run.txt` · `p8x/controls-out.txt` · `p8x/del-list.txt.out`). 봉인 뒤 조건 한 글자 변경(`p8x/rh-tamper`)과
ER-03 의 새 대조 둘(`p8x/er03-probe.sh`)은 그때 출력을 파일로 남기지 않았다. 2 회차 검토 반영 뒤 BUILD 가 봉인 직전 판으로 예행을 `p8b/rh` 에 새로 만들어 셋을 다시
재고 출력을 남겼다 — 조건 스물여덟 `p8b/final-run.txt` · 봉인 뒤 조건 한 글자 변경 `p8b/tamper-run.txt` · ER-03 새 대조 둘 `p8b/er03-probe.txt`.

문장 삭제 사본(`p8d/del.sh` · 목록 `p8d/del-list.txt`): SK-01 24 · SK-02 8 · SK-03 2 · SK-04 4 · SK-05 11 · SK-06 11 · SK-07 7 · SK-08 3 · SK-09 4 · SK-10 2 · SK-11 9 —
토큰 하나를 그 파일에서 한 번 지운 사본 85 개 모두 그 조건의 출력이 예행 판 출력과 달라졌다(`DROP` 85 · `NODROP` 0 · `MISSING` 0). 측정하지 않는 문장을 지운 대조 다섯
(cicd.md 원칙 6 제목 · infra-guide Gotcha 1 · infra-test Gotcha 4 · infra-audit Gotcha 1 · infra-test Gotcha 8)은 다섯 모두 출력이 같았다(`NODROP`) — 출력이 매번 바뀌는 측정이 아니다.

## Skill

- [ ] SK-01: `docs/infra/platform/cicd.md` 에 원칙 7 「빨간 검사는 고치기 전에 원인부터 가른다」 가 원칙 6 뒤 · `## 수치/기준값` 앞에 있고, 원인 다섯 갈래(이번 커밋 · 남의 미커밋 변경 · 기준 커밋에서 이미 실패 · 환경 · 미확정) · 이 분류가 킷 규칙이라는 문장 · merge base 가 둘 이상일 수 있다는 문장 · 임시 워크트리의 준비 명령 · CI 두 경우(환경 · 비결정성 과 미확정, 재실행은 같은 `GITHUB_SHA` · `GITHUB_REF`) · 같은 핵심 오류일 때만 기준 실패라는 문장 · 필수 검사를 건너뛰거나 통과로 적지 않는다는 문장 · 원인 증명이 아니라는 문장 · `gh run list --commit <sha>` · `--workflow` 없는 성공 조회의 한계 · 필수 검사 결론 셋 · 빠지는 커밋 범위 보고 · 근거 URL 다섯을 담으며, 코드 블록과 판정 표가 `harness/skills/sprint/SKILL.md` Step 3 원문과 글자 그대로 같고(Phase 4 넘김 — 판정 세 줄 원문 그대로), 머리 설정이 `0.2.0` · `2026-09-25` 이고 다루는 범위 문장이 「빨간 검사의 원인 가르기」 를 담는다 (backend-family:P3 — infra-kaizen Gotcha 2 가 요구하는 원칙 문서 선행) [exact, enumerated]
      (Given: 개정 파일 `end_sha:` 마지막 값이 정해진 뒤 · When: `type m >/dev/null || exit 2;` 뒤 `m SK-01` · Then: 네 줄이 `1 ` 스물한 개 · `1` · `code_same=1 code_lines=9 table_same=1 table_lines=5` · `0.2.0 2026-09-25 1`.
       토큰 스물하나는 `회귀 게이트` 절 `m.sh` 의 `SK-01)` 갈래에 글자 그대로 있다. 알려진 답: 코드 블록 아홉 줄 · 표 다섯 줄(머리 · 구분 · 판정 셋)은 `/sprint` Step 3 에서 손으로 센 수다.
       봉인 전 실측: `회귀 게이트` 절 표)
- [ ] SK-02: `infra-kit/skills/infra-guide/SKILL.md` 가 Gotcha 14 「빨간 CI 를 이번 변경 탓으로 단정하기 전에 원인부터 가른다 (enforcement 등급 E1)」 로 기준 커밋(`git merge-base HEAD origin/<기준 가지>`) 확인 · 원인 다섯 갈래 · 가를 근거가 없으면 미확정과 같은 커밋 재실행 · 기준 커밋에서 이미 실패하던 검사도 통과로 적거나 건너뛰라 하지 않음 · `gh run list --branch <가지> --status success --limit 1` 결과를 필수 검사 전부 통과로 읽지 않음 · `docs/infra/platform/cicd.md` 원칙 7 가리킴 · 실측 날짜를 담고, Gotcha 번호가 1 ~ 14 로 이어진다 (새 Gotcha 를 가운데 끼워 번호로 서로 가리키는 Gotcha 를 밀지 않는다) (backend-family:P3) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-02` 두 줄이 `1 1 1 1 1 1 1 1 ` · `1 2 3 4 5 6 7 8 9 10 11 12 13 14`. 시작 커밋 판: `0` 여덟 · `1 2 3 4 5 6 7 8 9 10 11 12 13`. 봉인 전 실측: `회귀 게이트` 절 표)
- [ ] SK-03: 키워드 두 자리가 같이 바뀐다 — `infra-kit/skills/infra-guide/SKILL.md` `## Step 1: 탐색` 의 `| cicd |` 행과 `infra-kit/references/principle-index.md` 의 `| cicd |` 행에 `CI 실패, 빨간 검사, 재실행` 이 붙고, 두 행의 키워드 칸이 글자 그대로 같으며, principle-index 행은 여전히 `docs/infra/platform/cicd.md` 를 가리키고, 옛 사본 `infra-kit/skills/infra-guide/references/principle-index.md` 는 편집 전과 같다 (근거 파일 §2 backend-family:P3.2 — 정본 두 자리 동시 수정 · 옛 사본은 대상 밖) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-03` 세 줄이 `1 ` · `1 1 ` · `keywords_same=1 oldcopy_same=1`. 시작 커밋 판: `0 ` · `0 1 ` · `keywords_same=1 oldcopy_same=1`.
       양성 대조: principle-index 행에서 `빨간 검사, ` 를 뺀 사본은 둘째 줄 `0 1 ` · `keywords_same=0`, 옛 사본 한 칸을 바꾼 사본은 `oldcopy_same=0`)
- [ ] SK-04: `infra-kit/evals/evals.json` 에 사례 6(skill `infra-guide`, prompt 에 `빨간` 과 `PR`, assertion 넷 — type 은 `behavior` · `output` 만 — cicd.md 원칙 7 을 읽고 답하기 · 고치기 전에 `git merge-base` 기준 커밋에서 같은 검사를 확인해 가르기 · 기준 커밋에서 이미 실패하던 검사를 통과로 적거나 건너뛰라 하지 않기 · 가를 근거가 없으면 미확정과 같은 커밋 재실행)이 더해져 사례가 6 개 · id 1 ~ 6 이고, `$END` 판에서 `scripts/run-evals.py infra-kit` 이 종료 코드 0 · `Total: 6 passed, 0 failed` 이며, `infra-kit/README.md` 검증 절이 「평가 사례 6 개의 구조 검증」 · 「등록된 검사 전부 (개수는 `harness/docs/guides/plugin-validation-guide.md` 가 정한다)」 이고 옛 「4 스킬 assertion 전수 검증」 · 「7 카테고리 구조 감사」 는 0 이다 (backend-family:P3 평가 사례 · Phase 7 넘김 `infra-kit/README.md:54` — 검사는 V1 ~ V10 열 가지) [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-04` 세 줄이 `6 True infra-guide True True 4 True 1 1 1 1` · `rc=0 Total: 6 passed, 0 failed` · `1 0 1 0`.
       셋째 줄은 README 의 새 문구 둘과 옛 문구 둘의 줄 수다 — 시작 커밋 판에서 `0 1 0 1`(양성 대조).
       음성 대조: 사례 6 assertion 하나의 `type` 을 `check` 로 바꾼 사본에서 둘째 줄이 `rc=1 Total: 5 passed, 1 failed`. 봉인 전 실측: `회귀 게이트` 절 표)
- [ ] SK-05: infra-test 와 상태어 정본의 `[미검증]` 이 설계 가이드 §3.7 3 항의 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 쓴다 — (a) `infra-kit/skills/infra-test/SKILL.md` Gotcha 12 가 네 칸 · 막는 것은 `command -v <도구>` 와 그 출력 · 우회가 없으면 `없음 — 이유` · 네 칸 정의 위치를 적는다 (b) `### Step 8: 결과 보고` 4 항이 네 칸과 「네 칸 중 하나라도 비면 그 항목은 `UNVERIFIED_ENV` 로 인정되지 않는다」 를 적고, 보고 예시의 미검증 두 건이 네 칸씩이며 시도한 우회 두 줄 가운데 하나는 `없음 — 이유` 꼴이다 (c) `infra-kit/references/gate-result-taxonomy.md` `## 재검증 명령 의무` 가 스크립트 줄을 막는 것 칸으로 옮기고 나머지 세 칸을 채운다는 문장 · §3.7 3 항 SSOT 가리킴 · 하나라도 비면 인정되지 않는다는 문장을 담는다. 가이드의 네 칸 이름이 이 킷이 쓰는 이름과 같고(알려진 답), `infra-kit/` 전체에 옛 표기 넷(`<도구> 미설치 — 재검증: <명령>` · 「재검증 명령이 없으면 그 항목은」 · 보고 예시 두 줄의 「미설치 — 재검증:」 꼴)이 0 줄이다 (Phase 1 넘김 `infra-kit/skills/infra-test/SKILL.md:37` — 가이드 1.6.0 의 반대편) [exact, enumerated]
      (Given: SK-01 과 같다 · When: `type m >/dev/null || exit 2;` 뒤 `m SK-05` · Then: 여섯 줄이 `1 1 1 1 ` · `1 1 1 1 ` · `2 2 2 2` · `1 1 1 ` · `1 1 1 1 ` · `0`.
       셋째 줄은 보고 예시의 칸 줄(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령) 수, 다섯째 줄은 가이드 §3.7 의 네 칸 줄(`   - **막는 것** —` 등)이다.
       여섯째 값은 시작 커밋 판에서 4(양성 대조 — Gotcha 12 · Step 8 4 항 · 예시 두 줄). `gate-result-taxonomy.md` 의 스크립트 줄 예시와 Step 5 골격 안 `[미검증]` 두 줄은
       스크립트 출력 형식이라 그대로 두며 옛 표기 넷에 걸리지 않는다. 봉인 전 실측: `회귀 게이트` 절 표)
- [ ] SK-06: infra-audit 과 infra-reviewer 의 `[미검증]` 이 같은 네 칸을 쓴다 — (a) `infra-kit/skills/infra-audit/SKILL.md` Gotcha 11 본문이 네 칸을 요구하고 예시가 네 칸을 다 채운 `kubectl get ns` 예이며 「네 칸 중 하나라도 비면 `[미검증:INVALID]` 다」 를 적는다 (b) Gotcha 12 의 규칙 소스 부재 줄이 네 칸(Gotcha 11)을 가리킨다 (c) `## Step 4: 최종 판정` 1 항 BLOCKED 가 소스를 못 읽었으면 네 칸을 적게 한다 (d) `infra-kit/agents/infra-reviewer.md` `## 출력 포맷` 규칙 줄이 네 칸과 「하나라도 비면 `INVALID` 다」 를 적고 예시 3 행이 네 칸 이름을 쓴다. reviewer `## 9. Canonical Unverified-Evidence Protocol` 절은 편집 전과 글자 그대로 같고(infra-kaizen Gotcha 8 — 정본 복제는 문구를 바꾸지 않는다), `infra-kit/` 전체에 옛 표기 다섯(「근거에 이유를 기술하라」 · 「manifest 정적 리뷰만 수행」 · `` `[미검증]` 태그 + 이유 `` · 「또는 소스 부재 사유 명시」 · `` 1차 `terraform state pull` ``)이 0 줄이다 (Phase 1 가이드 변경의 반대편 — 오케스트레이터 Step 8 전수 감사 · backend-kit 형제와 같은 꼴) [exact, enumerated]
      (Given: SK-01 과 같다 · When: `type m >/dev/null || exit 2;` 뒤 `m SK-06` · Then: 다섯 줄이 `1 1 1 1 1 1 ` · `1 1 ` · `1 1 1 ` · `s9_same=1 s9_lines=60` · `0`.
       다섯째 값은 시작 커밋 판에서 4(양성 대조 — Gotcha 11 은 옛 표기 둘이 한 줄이라 줄 수로 4). 음성 대조: §9 한 글자를 바꾼 사본에서 넷째 줄 `s9_same=0 s9_lines=60`. 봉인 전 실측: `회귀 게이트` 절 표)
- [ ] SK-07: `infra-kit/skills/infra-test/SKILL.md` `### Step 7: 실행 검증` 에 알려진 답 대조 문단(생성한 검사 스크립트를 실제 대상보다 답을 아는 작은 입력에 먼저 돌린다 · `WF_DIR=<임시 폴더> bash tests/ci-validation.sh` · 기대값 `열거된 uses 참조 수: 3` · 참조 단위 VIOLATION 줄 2 개 · 집계 `VIOLATION=1` 은 규칙 단위 · exit 1 · 다르면 실제 대상에 돌리지 않고 스크립트나 입력부터 고친다)이 있고, 그 문단이 적은 값이 `$END` 판 Step 5 골격을 그 입력으로 실제로 돌린 결과와 같다 (Phase 1 가이드 §3.7 「0 이 아닌 값을 내는 새 측정 — 알려진 답 대조」 의 반대편) [exact]
      (Given: SK-01 과 같고 `python3 -c 'import yaml'` 이 종료 코드 0 — 없으면 `YAML_MISSING` 이라 FAIL · When: `type m >/dev/null || exit 2;` 뒤 `m SK-07` · Then: 세 줄이 `1 1 1 1 1 1 1 ` · `ka exit=1 refs=3 viol_lines=2 VIOLATION=1` · `ok exit=0 refs=3 viol_lines=0 VIOLATION=0`.
       `ka` 는 문단이 적은 입력(원격 uses 셋 — `actions/checkout@v4` · 40 자 SHA 로 고정한 액션 하나 · `@v4` 태그 액션 하나), `ok` 는 셋 다 40 자 SHA 인 같은 입력이다. 알려진 답: 손으로 센 기대값(참조 3 · 태그 2 · 규칙 단위 집계 1 · exit 1)이 둘째 줄과 같다.
       음성 대조: 골격의 `if SHA.search(ref):` 를 `if "@" in ref:` 로 바꾼 사본에서 둘째 줄이 `ka exit=0 refs=3 viol_lines=0 VIOLATION=0`. 시작 커밋 판: 첫 줄 `0` 일곱 · 둘째 · 셋째 줄은 같다(골격은 이번에 바뀌지 않는다))
- [ ] SK-08: `infra-kit/skills/infra-test/SKILL.md` `### Step 6: K8s Manifest 테스트 생성` 의 kubeconform 예시가 고정 버전 대신 `K8S_VERSION="${K8S_VERSION:?대상 클러스터의 Kubernetes 버전을 넣는다}"` 줄과 `-kubernetes-version "$K8S_VERSION"` 을 쓰고 고정 값의 위험을 주석 한 줄로 적으며, `infra-kit/` 전체에 `-kubernetes-version 1.` 이 0 줄이고, 그 변수 줄을 실제로 돌리면 변수가 없을 때 0 이 아닌 종료 코드와 안내 문장을 내고 있을 때 0 이다 (근거 파일 §3 — 고정 `1.30.0` 은 최신 안정판 v1.37.1 보다 낡았고 대상 클러스터 버전을 따라야 한다) [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-08` 세 줄이 `1 1 1 ` · `0` · `unset_rc=R unset_msg=1 set_rc=0` 이고 R 이 0 이 아니다 — 예행 bash 5.3.9 와 `/bin/bash` 3.2.57 모두 127.
       시작 커밋 판: `0 0 0 ` · `1`(양성 대조) · `unset_rc=0 unset_msg=0 set_rc=0`(줄이 없어 빈 명령))
- [ ] SK-09: 「OpenTofu 1.7+ native state encryption」 버전 단정 네 자리가 사라진다 — `infra-kit/references/audit-criteria.md` IaC 표 `| State encryption |` 행 · `infra-kit/references/init-checklist.md` 의 **State encryption** 줄과 **OpenTofu 대안 검토** 줄 · `infra-kit/skills/infra-init/SKILL.md` Gotcha 11 이 버전 없이 native state encryption 을 적고, `infra-kit/` 전체에서 `1.7+ native state encryption` · `1.7+는 native state encryption` 꼴이 0 줄이다 (근거 파일 §5 — 인용한 OpenTofu v1.11 문서가 1.7 도입 연혁을 적지 않는다. 2026-08-13 research-log 는 뺐다고 적었지만 네 자리가 남아 있었다) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-09` 두 줄이 `0` · `1 1 1 1`. 첫 값은 시작 커밋 판에서 4(양성 대조), 둘째 줄은 시작 커밋 판에서 `0 0 0 0`)
- [ ] SK-10: `infra-kit/README.md` 가 infra-kaizen Gotcha 9 구성(스킬 표 넷 · 에이전트 표 한 줄 · 리서치 문서 카테고리 요약 셋)을 유지한 채, cicd 요약 줄 끝에 「빨간 검사 원인 가르기」 가 붙고, 2026-04-24 이력 줄의 「OpenTelemetry 3 signals stable」 바로 뒤에 「(2026-08-13 정정 — signal 별로 상태가 다르다, infra-guide Gotcha 13)」 가 붙는다 (근거 파일 §3 — README 이력 줄이 OTel 현재 상태와 어긋난다) [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-10` 두 줄이 `1 1` · `4 1 3`. 시작 커밋 판: `0 0` · `4 1 3`)
- [ ] SK-11: `docs/infra/research-log.md` 의 첫 항목이 `## [2026-09-24] - Phase 8 kaizen` 이고, 처리 배정표 키 `backend-family:P3` · 조회한 외부 소스 절(근거 파일 경로) · 변경 내역 · 사실 정정(「OpenTofu 1.7+ 가 남아 있었다」) · 규칙으로 올리지 않은 것 절(근거 파일 §3) · 다음 사이클 후보 · 세 분류를 규범으로 정한 곳이 없다는 문장을 담으며, 머리 설정이 `1.4.0` · `2026-09-25` 이고, `## [2026-08-13] - Phase 8 kaizen` 부터 끝까지는 편집 전과 글자 그대로 같다 (오케스트레이터 Gotcha — per-kit research-log 갱신) [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-11` 세 줄이 `1 ` 아홉 개 · `first=1 1.4.0 2026-09-25` · `history_same=1 history_lines=341`.
       시작 커밋 판: `0` 아홉 · `first=0 1.3.0 2026-08-13` · `history_same=1 history_lines=341`. 음성 대조: 2026-08-13 항목의 한 구절을 지운 사본에서 셋째 줄 `history_same=0`)

## Script

- [ ] SC-00: N/A (Script 카테고리는 `release.sh` 연동 · 버전 올림 · `marketplace.json` 갱신이다. 이 Phase 는 그 파일을 건드리지 않는다 — 공유 파일은 Final 몫. 측정: `type m >/dev/null || exit 2;` 뒤 `m SC-00` 이 0. 양성 대조: 예행 변형 `signed-outside` 에서 1)

## Error

- [ ] ER-01: 열세 파일에 새로 생긴 URL 과 `.harness/.meta/kaizen-0924/phase8-notes.md` 의 URL 이 전부 이 Phase 의 외부 근거 파일 `.harness/.meta/evidence/phase8.md` 에 있다 — 열세 파일은 파일마다 편집 전 판과 비교한다 (러닝북 — notes 킷 로그 한 단락의 출처 URL 은 근거 파일에서만) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-01` 두 줄이 `0` · `0`. 첫 줄은 열세 파일을 파일마다 비교해 다른 파일에 이미 있던 URL 을 새로 더한 경우도 본다. 둘째 줄은 notes 의 URL 전부이고, notes 가 `$END` 판에 없으면 `NOTES_MISSING` 이라 FAIL 이다.
       봉인 전 실측: 예행 판의 새 URL 은 cicd.md 다섯 · research-log 열하나(겹치는 것을 빼면 열둘)이고 전부 근거 파일에 있어 첫 줄 0. notes 모의본의 URL 하나(git merge-base)도 근거 파일에 있어 둘째 줄 0.
       양성 대조: 예행 판 cicd.md 끝에 `https://example.invalid/x` 를 더하면 `1` · `0`, notes 끝에 더하면 `0` · `1`, notes 를 지운 사본에서 `0` · `NOTES_MISSING`)
- [ ] ER-02: 열세 파일에 더한 줄에 번역투 6 종(`tone-kit/references/locale-korean.md` §2 치환표의 grep 열)이 0 건이다 — 고친 줄에 원래 있던 번역투도 더한 줄로 세므로 함께 고친다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-02` 가 0. 봉인 전 실측: 첫 예행에서 infra-audit Gotcha 12 의 원래 문구 「같은 원칙이 규칙 소스에도 적용된다」 가 1 을 내 「해당한다」 로 고쳤고, 고친 뒤 0.
       양성 대조: infra-guide 끝에 「이 값이 적용된다」 를 더하면 1)
- [ ] ER-03: 이 Phase 범위 밖 반대편을 명시적 미완으로 넘기고 건드리지 않는다 — `.harness/.meta/kaizen-0924/phase8-notes.md` 가 `$END` 에 커밋돼 있고 열일곱 문자열(처리 배정표 키 `backend-family:P3` · 넘김 `docs/infra-kit/cicd.html` · `docs/infra-kit/infra-test.html` · `docs/infra-kit/gate-result-taxonomy.html` (Final F2) · `.harness/stale-values.yaml` (Final — 등록할지 판단한다. 옛 값 검사 check-stale-values.py 는 docs-site 소스 폴더만 훑어 infra-kit 안의 두 옛 값 「1.7+ native state encryption」 · `-kubernetes-version 1.30.0` 을 보지 못하고, 앞의 것을 그대로 등록하면 이 Phase research-log 항목의 변경 내역 줄이 걸리므로 그 파일을 allow 에 사유와 함께 둔다) · `plugin.json` (Final — 버전) · `§Canonical Unverified-Evidence Protocol` (다음 사이클 Phase 3 — reviewer §9 가 정본의 새 판과 다르다) · `phase-research-templates.md` (다음 사이클 — 「3 signals stable」 기대값) · `harness/skills/sprint/SKILL.md` (다음 사이클 Phase 4 — CI 두 경우를 정본이 받을지) · `Flux v2.9` (다음 사이클 — 원칙 문서 먼저) · `.claude/skills/infra-kaizen/SKILL.md` (다음 사이클 — Gotcha 8 복제 조항과 정본 판 차이 · Gotcha 6 형제 대조 표의 「미검증 3항」 을 네 칸으로) 과 러닝북이 적게 한 절 머리 `## 반영한 처리 배정표 키` · `## 미반영 키와 사유` · `## 넘기는 것` · `## changelog 한 단락` · `## 킷 로그 한 단락` · `## 다음 사이클 메모`)을 각각 1 회 이상 담고, 구간 안에서 공유 파일 · 다른 Phase 파일을 건드린 커밋 가운데 다른 Phase 서명이 없는 커밋이 0 개다 [exact, enumerated]
      (Given: BUILD 가 notes 를 커밋하고 개정 파일에 그 sha 로 `end_sha:` 를 덧붙인 뒤 · When: `type m >/dev/null || exit 2; type not_other >/dev/null || exit 2;` 뒤 `m ER-03` · Then: 첫 줄 `notes_committed=1` · 둘째 줄 값 열일곱 개가 모두 1 이상(0 이 하나라도 있으면 실패. 같은 문자열을 여러 절에 적으면 2 이상이 정상이다 — 예행 판은 모의 notes 라 모두 1) · 셋째 줄 `0`.
       셋째 값의 경로는 `m.sh` `ER-03)` 갈래의 `not_other` 인자 열넷이다 — 서명 줄 목록이 아니라 경로로 직접 세므로 서명을 빠뜨린 커밋도 보인다. 다른 Phase 서명이 달린 커밋은 그 Phase 몫이라 뺀다.
       봉인 전 실측: `회귀 게이트` 절 표. 양성 대조: 변형 `unsigned-shared` · `signed-outside` · `cross-phase` 에서 셋째 값 1. 예행의 다른 Phase 서명 커밋(`rust-kit/README.md`)은 인자 밖이라 0 에 영향이 없다.
       문자열 삭제 대조: 모의 notes 에서 `` - `plugin.json` — Final `` 줄을 지운 사본에서 둘째 줄 여섯째 값 0.
       중복 대조: 모의 notes 에 `backend-family:P3` · `plugin.json` 을 한 줄씩 더 적은 사본에서 둘째 줄 첫째 · 여섯째 값 2 — 모두 1 이상이라 PASS 다)

## Architecture

- [ ] AR-01: 이 Phase 의 변경이 허용 경로 안에 머물고, 범위 선언 블록이 그 경로와 같으며, 이 계약이 봉인돼 있다 [exact, enumerated]
      (Given: BUILD 가 개정 파일에 `end_sha:` 를 적은 뒤 · 이 Phase 커밋 메시지마다 서명 줄 `Kaizen-Phase: kaizen-0924-p08-infra-kit` · When: `type m >/dev/null || exit 2; type unsigned_on >/dev/null || exit 2; type verify_seal >/dev/null || exit 2;` 뒤 `m AR-01` · Then: 여섯 줄이 —
       ① `0` — `infra-kit/` · `docs/infra/` 를 건드린 구간 안 커밋이 전부 서명했다(이 구간에 두 폴더를 고칠 수 있는 Phase 는 8 하나다)
       ② `0 13` — 서명 커밋이 건드린 `.harness/` 밖 경로 가운데 열세 파일 밖이 0 개, 열세 파일이 전부 있다
       ③ `0` — `harness/references/contract-schema.md` §`.harness/` 범위 조건 의 권장 형태로 `.harness/` 의 계약 전부에 `verify_seal` 을 돌려 이 Phase 몫 `SEAL_BROKEN` 이 0 개
       ④ `SEAL_OK` — `$END` 판의 이 계약이 봉인돼 있다(`SEAL_ABSENT` 는 봉인을 건너뛴 것이라 FAIL)
       ⑤ `scope_same=1` — `## 범위 경계` 절 `# sprint-scope` 블록의 `.harness/` 밖 줄이 `FILES` 열세 줄과 같다 ⑥ `1` — 그 블록에 `.harness/` 줄이 하나 있다.
       봉인 전 실측: `회귀 게이트` 절 표. 양성 대조: 변형 `unsigned-mine` ① 1 · 변형 `signed-outside` ② `1 13` · 조건 줄 한 글자를 바꾼 사본 ④ `SEAL_BROKEN`)
- [ ] AR-02: 새 원칙과 바뀐 표기가 그것을 읽는 쪽에 닿는다 — (a) `infra-kit/references/principle-index.md` 의 `| cicd |` 행이 한 줄이고 그 경로(레포 루트 기준)를 풀면 `docs/infra/platform/cicd.md` 이며 그 파일에 `### 7. 빨간 검사는` 제목이 있다 (b) `infra-kit/skills/infra-guide/SKILL.md` Step 2 가 principle-index 를 읽는 줄이 그대로다 (c) `infra-kit/agents/infra-reviewer.md` 평가 기준 참조의 상태어 정본 줄과 감사 기준 줄, `infra-kit/skills/infra-audit/SKILL.md` · `infra-kit/skills/infra-test/SKILL.md` References 의 상태어 정본 줄이 그대로이고, `infra-kit/references/gate-result-taxonomy.md` `## 소비처` 표가 세 파일을 적는다 — 그래서 §재검증 명령 의무 에 더한 문단이 따로 옮겨 적지 않아도 세 소비처에 닿는다 (Counterpart — 소비면) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m AR-02` 두 줄이 `1 docs/infra/platform/cicd.md 1` · `1 1 1 1 1 3`. 알려진 답: 시작 커밋 판은 경로는 같고 제목이 없어 `1 docs/infra/platform/cicd.md 0` · `1 1 1 1 1 3`)

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다. 이번 변경에 적용: 열세 파일에 더한 줄에 infra-kit `plugin.json` 의 `version` 값(`$END` 판에서 읽는다)이 0 건이다 — 이 Phase 는 킷 버전을 적지 않고 Final 이 올린다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m AP-01` 이 `version=0.3.1 0` (버전 값은 `$END` 판 plugin.json 에서 읽은 것 — 이 Phase 가 plugin.json 을 건드리지 않으므로 0.3.1). 양성 대조: README 끝에 「버전 0.3.1」 을 더하면 `version=0.3.1 1`)
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```` ```text, ```bash, ```yaml ```` 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 이번 변경에 적용: 이 Phase 가 더하는 펜스는 cicd.md 원칙 7 의 `bash` 블록 하나(여는 줄 · 닫는 줄 둘)뿐이고, 마크다운 열두 파일 전체에 언어 힌트 없는 여는 펜스가 0 개다 — `docs/infra/` 는 V6 범위 밖이라 같은 상태기계를 이 측정이 돌린다. infra-kit 쪽은 DG-05 의 V6 가 함께 본다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m AP-03` 이 `added_fence=2 bare_open=0`. 양성 대조: README 끝에 언어 힌트 없는 펜스 한 벌을 더하면 `added_fence=4 bare_open=1`)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL. 이번 변경에 적용: 고친 SKILL.md 넷(infra-guide · infra-test · infra-audit · infra-init)과 infra-reviewer 의 첫 frontmatter 블록이 편집 전과 글자 그대로 같고 `name: <폴더 또는 파일 이름>` 줄이 1 개씩이다 — 그래서 README AUTO 구간과 트리거 설명이 읽는 값도 바뀌지 않는다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m AP-04` 가 `1/1 1/1 1/1 1/1 1/1 `. 양성 대조: 예행 판 infra-guide 의 description 한 글자를 바꾼 사본에서 `0/1 1/1 1/1 1/1 1/1 `. 음성 대조는 DG-05 — `name:` 을 깨면 V1 이 FAIL)

## Reusability

- [ ] RE-01: N/A (재사용 단위 코드 — 컴포넌트 · 함수 · 모듈 — 가 없다. 변경 파일이 문서 · 평가 사례 데이터뿐이고, 원칙 7 의 셸 조각은 문서 속 예시다. 측정: `type m >/dev/null || exit 2;` 뒤 `m RE-01` 이 0. 양성 대조: 같은 `grep -cvE` 에 `x.sh` 한 줄을 넣으면 1)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다. 이번 변경에 적용: 판정 세 줄은 새로 쓰지 않고 `harness/skills/sprint/SKILL.md` Step 3 원문을 옮기며(SK-01 알려진 답), 판정 표 머리 줄 「| 공용 작업 폴더 | `HEAD` 임시 | `FORK_BASE` 임시 | 판정 |」 은 `infra-kit/` · `docs/infra/` 에서 `docs/infra/platform/cicd.md` 하나에만 있다 — Gotcha 14 는 그곳을 가리킨다. 네 칸의 정의도 새로 쓰지 않고 skill-design-guide §3.7 3 항을 가리킨다(SK-05) [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m RE-02` 출력이 `docs/infra/platform/cicd.md` 한 줄)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `type m >/dev/null || exit 2;` 뒤 `m DG-01` 이 0. 실제 검사는 DG-02 · DG-05)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (`diagnostics.ide_exclude` 값 `[]`) — 이번 변경에 적용: 편집기 마크다운 확장과 같은 조건(markdownlint-cli2 0.23.2 · MD013 끔)으로 마크다운 열두 파일의 **더한 줄**에 걸린 경고가 0 이고, `infra-kit/evals/evals.json` 이 JSON 으로 읽힌다. 편집 전부터 있던 경고는 `범위 경계` 절에 적은 대로 범위 밖이다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m DG-02` 의 열두 줄이 모두 `new_warnings=0` 으로 끝나고 `LINT_NOT_RUN` 줄 0 · 마지막 줄 `json_ok`.
       봉인 전 실측: 예행 판 열두 줄 `new_warnings=0` (더한 줄 50 · 57 · 3 · 1 · 4 · 18 · 5 · 3 · 2 · 1 · 2 · 1) · `json_ok`.
       양성 대조: cicd.md 끝에 `#bad heading` 을 더하면 첫 줄 `new_warnings=1`)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: `type m >/dev/null || exit 2;` 뒤 `m DG-03` 이 0. 실제 시험은 SK-04 · SK-07 · DG-05)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 변경이 문서와 평가 사례 데이터뿐이다. 측정: `type m >/dev/null || exit 2;` 뒤 `m DG-04` 가 0. 양성 대조: 같은 `grep -cE` 에 `a/b.dart` · `c.sh` · `d.md` 세 줄을 넣으면 2)
- [ ] DG-05: 저장소 검사가 이 킷을 문제로 가리키지 않는다 — `$END` 판을 git 저장소로 만든 사본에서 (a) `scripts/validate-plugin.py infra-kit` 출력에 `V1` ~ `V10` 열 줄이 있고 하나도 `ERROR` · `FAIL` 이 아니다 (b) `scripts/sync-evals.py --check-only` 출력에 `→ infra-kit` 머리 줄이 있고 그 아래 어긋남 줄이 0 이다 (c) `scripts/check-stale-values.py` 가 종료 코드 0 또는 1 이고 출력에 열세 파일 경로가 0 건이다. 킷 전체를 보는 검사는 이 킷 몫의 줄만 센다 — 같은 구간에 다른 Phase 가 올린 변경 때문에 떨어지지 않게 한다(`harness/references/contract-schema.md` §검사 스크립트 전체 통과를 조건으로 걸지 마라). `sync-docs.py` 는 넣지 않는다 — infra-kit README 에 AUTO 구간이 없어 이 킷에서는 떨어질 수 없는 검사다. README AUTO 구간이 읽는 frontmatter 가 그대로인지는 AP-04 가 잰다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m DG-05` 세 줄이 `10 0` · `1 0` · `stale_rc=0 0` (stale_rc 는 0 또는 1).
       봉인 전 실측: 예행 판 `10 0` · `1 0` · `stale_rc=0 0`. 음성 대조: infra-guide 의 `name: infra-guide` 를 `nam:` 으로 깬 사본에서 첫 줄 `10 1`.
       양성 대조: `infra-kit/skills/zz-test/SKILL.md` 를 더한 사본에서 둘째 줄 `1 1` · cicd.md 에 등록된 옛 값 「OWASP 권장 12」 를 넣은 사본에서 셋째 줄 `stale_rc=1 1`)
- [ ] DG-06: `python3 scripts/validate-post-kaizen.py --since 4a8ec55f4d874eaaed083af9621f9679693cbdb6` 출력의 `scope-isolation` · `doc-contracts` 줄이 `FAIL` · `ERROR` 가 아니다. `docs-site-regen` 은 Final F2 몫이라 판정에서 뺀다. 다른 Phase 커밋 때문에 `scope-isolation` 이 FAIL 이면 `--verbose` 위반 커밋 목록을 1 개 이상 읽었고 그 가운데 서명 줄 커밋이 0 개일 때, `doc-contracts` 가 FAIL · ERROR 이면 `validate-doc-contracts.py -v` 가 검사한 경로를 1 개 이상 읽었고 그 가운데 이 Phase 서명 커밋이 건드린 경로가 0 개일 때 이 조건은 PASS 다 — 둘 다 근거에 다른 Phase 몫이라고 적는다 [exact]
      (Given: 작업 폴더에서 `$END` 이후 커밋이 있어도 된다 — 검사는 `HEAD` 까지 보지만 판정은 이 Phase 서명 커밋만 센다 · When: `type m >/dev/null || exit 2;` 뒤 `m DG-06` · Then: 네 줄이 `scope-isolation: PASS` · `doc-contracts: PASS` · `doc_checked=N doc_mine=0` · `violators=V mine=0` 이고 N 이 1 이상. 위 가르기로 PASS 를 줄 때만 첫 두 줄에 `FAIL` 이 있어도 되며, scope-isolation 이 `FAIL` 이면 V 가 1 이상이어야 한다(목록을 못 읽으면 mine 이 조용히 0 이 되므로).
       봉인 전 실측: `회귀 게이트` 절 표. 양성 대조: 변형 `cross-phase` 에서 `scope-isolation: FAIL` · `violators=1 mine=1`)
