# 카이젠 2026-09-24 Phase 8 (infra-kit) — notes

- 계약: `.harness/sprint-contract-kaizen-0924-p08-infra-kit.md` (조건 28 · 기능 조건 18, 봉인 `sha256:7cc562b4e14e06a3` · `locked_at` 2026-09-25 07:40)
- 개정: `.harness/sprint-amendments-kaizen-0924-p08-infra-kit.md` (조건 변경 0 건, `end_sha` 만)
- 검토: `.harness/.meta/kaizen-0924/phase8-review.md` (1 회차 CHANGES 고칠 것 하나 · 권장 여섯은 초안이 반영, 2 회차 CHANGES 고칠 것 하나 · 권장 둘은 BUILD 가 봉인 전에 반영)
- 시작 커밋 `4a8ec55f4d874eaaed083af9621f9679693cbdb6`
- 계약 피드백: `~/.harness/feedback/contract/5a24cc99-2026-09-25T074456-de8c7935-5544.yaml` (`verify-feedback.sh` PASS). 초안은 `.harness/feedback-draft-p08.yaml` 로 갈라 썼다

## 커밋

| 커밋 | 내용 | 파일 |
| --- | --- | --- |
| `3227f51` | 봉인 커밋 | 계약 1 개 |
| `19d2a2f` | cicd 원칙 7 · research-log | `docs/infra/` 둘 |
| `d215fdd` | Gotcha 14 · 미검증 네 칸 · 알려진 답 대조 · kubeconform 버전 변수 · 1.7+ 정정 · 평가 사례 6 · README | `infra-kit/` 열하나 |
| `a18f6c3` | 개정 파일에 `end_sha` (`d215fdd`) | 개정 1 개 |
| 이 파일의 커밋 | notes · 검토 기록 | `.harness/` 두 개 |
| 그다음 커밋 | 개정 파일에 notes 커밋 sha 로 `end_sha` 한 줄 더 | 개정 1 개 |

모든 커밋 메시지 끝 문단에 `Kaizen-Phase: kaizen-0924-p08-infra-kit` 줄이 있다. 구현 커밋은 `git add -- <파일…> && git commit -o -- <파일…>` 로 내 경로만 실었다.
**FIX 가 커밋을 더할 때도 서명 줄을 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다.**

구현은 초안의 모의 편집(스크래치 `p8d/mock.py`, 치환 29)을 작업 폴더에 그대로 돌렸다 — `mock applied 29`, 더한 줄 159. 돌린 뒤 열세 파일이
예행 저장소 `p8b/rh` 의 같은 파일과 `cmp` 로 모두 같았다.
28 조건 측정은 봉인 커밋 판 계약에서 뗀 묶음으로 돌렸다 — 스크래치 `p8b/ks/`(`common.sh` · `m.sh` · `new-warnings.sh`, 초안의 `p8d/k/` 와 `cmp` 로 같다) ·
`p8b/run.sh`(공통 정의를 `.` 로 읽고 `TMPDIR` 를 스크래치로 둔 뒤 `type` 으로 도우미 넷을 확인하고 `m <조건 ID>`). QA 가 같은 묶음을 다시 돌릴 수 있다.

디스크 여유 공간이 250 MB 안팎이라 한 번은 DG-05 의 `git add` 가 `No space left on device` 로 멈췄다. 같은 디스크를 여러 Phase 가 같이 쓴 탓이고 오류 줄이 그대로 찍혔다.
DG-05 만 다시 돌려 요구값(`10 0` · `1 0` · `stale_rc=0 0`)이 나왔다. QA 도 측정 전에 `df -h /private/tmp` 를 한 번 보는 편이 낫다.

## 바꾼 파일

- `docs/infra/platform/cicd.md` 0.1.0 → 0.2.0 — 다루는 범위에 「빨간 검사의 원인 가르기」, 원칙 6 뒤 원칙 7(원인 다섯 갈래 · 분류는 이 킷의 규칙 · merge base 가 둘 이상일 수 있음 ·
  임시 워크트리의 준비 명령 · `/sprint` Step 3 코드 블록과 판정 세 줄 원문 · CI 에서만 보이는 두 경우 · 같은 핵심 오류일 때만 기준 실패 · 원인 증명이 아님 · `gh run list` 두 용법과 한계 · 출처 다섯)
- `docs/infra/research-log.md` 1.3.0 → 1.4.0 — `## [2026-09-24] - Phase 8 kaizen` 항목(외부 근거 여덟 · 변경 내역 · 사실 정정 둘 · 규칙으로 올리지 않은 것 여섯 · 다음 사이클 후보 넷)
- `infra-kit/skills/infra-guide/SKILL.md` — Gotcha 14 (E1) 신설, Step 1 cicd 행 키워드 셋
- `infra-kit/references/principle-index.md` — cicd 행 키워드 셋(옛 사본 `skills/infra-guide/references/principle-index.md` 는 그대로)
- `infra-kit/skills/infra-test/SKILL.md` — Gotcha 12 · Step 8 4 항 · 보고 예시 두 건을 네 칸으로, Step 7 알려진 답 대조 문단, Step 6 kubeconform 스키마 버전을 `K8S_VERSION` 변수로
- `infra-kit/references/gate-result-taxonomy.md` — `## 재검증 명령 의무` 끝에 리포트는 네 칸으로 옮긴다는 문단
- `infra-kit/skills/infra-audit/SKILL.md` — Gotcha 11 본문과 예시 · Gotcha 12 · Step 4 1 항을 네 칸으로, Gotcha 12 의 번역투 한 곳을 「해당한다」 로(ER-02 첫 예행이 잡았다)
- `infra-kit/agents/infra-reviewer.md` — `## 출력 포맷` 미검증 규칙 줄과 예시 3 행을 네 칸 이름으로(§9 복제본은 그대로)
- `infra-kit/references/audit-criteria.md` · `infra-kit/references/init-checklist.md` · `infra-kit/skills/infra-init/SKILL.md` — 「OpenTofu 1.7+ native state encryption」 네 자리에서 버전을 뺐다
- `infra-kit/evals/evals.json` — 사례 6 (공용 가지의 빨간 CI, infra-guide)
- `infra-kit/README.md` — cicd 요약 · 검증 절 두 줄(「평가 사례 6 개의 구조 검증」 · 「등록된 검사 전부 …」) · 2026-04-24 이력 줄의 OTel 정정 표시

스킬 · 에이전트 머리 설정은 그대로다(AP-04). infra-kit README 에 자동 갱신 구간이 없다 — `sync-docs.py --check-only` 는 「모든 README가 동기화 상태입니다」.

## 반영한 처리 배정표 키

| 키 | 반영 |
| --- | --- |
| `backend-family:P3` | 공용 가지의 빨간 CI 를 이번 변경 탓으로 단정하기 전에 원인을 이번 커밋 · 남의 미커밋 변경 · 기준 커밋에서 이미 실패 · 환경 · 미확정으로 가른다. 원칙 본문은 cicd.md 원칙 7 한 곳(RE-02), infra-guide 는 그곳을 가리키는 Gotcha 14, 키워드 두 자리, 평가 사례 하나 (SK-01 ~ SK-04 · AR-02) |
| `F09` 비고 (Phase 4 행) | 기준 커밋 가르기 규칙 세 곳을 하나로 — Phase 4 가 정한 harness `/sprint` Step 3 을 기준 원본으로 두고 판정 세 줄 · 코드 블록을 글자 그대로 옮겼다(SK-01 이 원문과 같은지 잰다). CI 에서만 보이는 두 경우는 원문 표를 바꾸지 않고 표 밖 목록으로 붙였다 |

그 밖에 받은 것 — 앞 Phase 넘김 셋(Phase 1 `infra-kit/skills/infra-test/SKILL.md:37` 네 칸 · Phase 4 판정 세 줄 · Phase 7 README `:54` 「7 카테고리 구조 감사」),
근거 파일 §3 · §5 의 사실 정정(kubeconform 고정 `1.30.0` · README OTel 이력 줄 · 「OpenTofu 1.7+ native state encryption」).

Phase 1 가이드 변경 셋 (infra-kaizen Gotcha 8):

| 가이드 변경 | 이 킷 | 자리 |
| --- | --- | --- |
| `[미검증]` 에 네 칸 (skill-design-guide §3.7 3 항) | 반영 | infra-test Gotcha 12 · Step 8 · 보고 예시, gate-result-taxonomy §재검증 명령 의무, infra-audit Gotcha 11 · 12 · Step 4, infra-reviewer 출력 포맷 (SK-05 · SK-06) |
| 작업 자체를 못 한다고 결론 내리기 전 네 칸 (§3.7) | 반영 | infra-audit Step 4 BLOCKED 의 「소스를 못 읽었으면」 이 이 꼴이라 네 칸을 가리키게 했다 (SK-06 (c)) |
| 0 이 아닌 값을 내는 새 측정 — 알려진 답 대조 (§3.7) | 반영 | infra-test 가 만드는 검사 스크립트가 0 이 아닌 값을 낸다 — Step 7 알려진 답 대조 문단. 문단이 적은 값은 Step 5 골격을 그 입력으로 실제로 돌린 값과 같다 (SK-07) |

## 미반영 키와 사유

- `Flux v2.9` · Argo CD 3.5 에서 빠진 API — 규칙으로 올리려면 `docs/infra/` 원칙 문서가 먼저다(infra-kaizen Gotcha 2). research-log 에 기록만 했다
- Kubernetes 1.37 · Terraform 1.16 · OpenTofu 1.12.6 · Crossplane 2.4 — 근거 파일 §3 「2026-08-13 이후 특히 반영할 변경」 의 네 항목이다. 규칙으로 올리려면 `docs/infra/` 원칙 문서가 먼저라(infra-kaizen Gotcha 2) research-log 에 기록만 했다
- GitHub 밖 CI 의 기준 커밋 조회 명령 — 근거 파일에 없다
- 「내 변경 / 기준 실패 / 환경」 세 분류를 규범으로 정한 공식 문서 — 근거 파일 §2 가 찾지 못했다. 그래서 원칙 7 은 분류가 이 킷의 규칙이라고 적는다

그대로 둔 곳과 이유:

- `infra-kit/references/audit-criteria.md:104` · `infra-kit/references/init-checklist.md:132` · infra-test Gotcha 8(`:24`)의 「1.7+ mocking」, infra-test Gotcha 10(`:26`)의
  「OpenTofu 1.7+ write-only 인수」, 「Terraform 1.10+ ephemeral」 — 도입 버전을 근거 파일이 확인하지 못했거나(§5, ephemeral) 다루지 않았다(mocking · write-only). 틀렸다는 근거도 없다
- `gate-result-taxonomy.md` §재검증 명령 의무 의 스크립트 줄 예시와 infra-test Step 5 골격 안 `[미검증]` 두 줄 — 스크립트가 찍는 한 줄 형식이라 그대로 두고 리포트가 네 칸으로 옮긴다
- 네 칸 이름이 아닌 채 남는 두 자리 — infra-test Step 7 결과 분류 표의 `도구 미설치 · 클러스터/레지스트리 접근 불가` 행(스크립트 상태 표라 둔다),
  infra-audit `## Unverifiable Summary` 블록의 `env_gaps` 줄(reviewer §9 가 복제한 조항 5 의 4 요건 이름을 따른다). 한 파일 안에서 두 가지 이름이 보이는 것은 다음 사이클에 정한다
- reviewer `## 9. Canonical Unverified-Evidence Protocol` — 복제본은 문구를 바꾸지 않는다(infra-kaizen Gotcha 8). 기준 원본이 바뀐 것은 아래 넘기는 것에 적었다

ER-03 셋째 값(공유 파일 · 다른 Phase 파일을 건드린 커밋 가운데 다른 Phase 서명이 없는 커밋 수)이 0 이 아니면 QA 가 그 커밋 목록부터 보고 판정한다 —
그 값은 다른 Phase 가 서명 줄을 단다는 전제에 기댄다.

## 넘기는 것 (명시적 미완)

| 대상 | 누가 | 할 일 |
| --- | --- | --- |
| `docs/infra-kit/cicd.html` · `docs/infra-kit/infra-test.html` · `docs/infra-kit/gate-result-taxonomy.html` | Final F2 | 원칙 7 · 네 칸 · 알려진 답 대조 문단 · kubeconform 버전 변수가 없다. 세 페이지를 다시 만든다 |
| `.harness/stale-values.yaml` | Final | 등록할지 판단한다. 옛 값 검사 `scripts/check-stale-values.py` 는 docs-site 소스 폴더(`SOURCE_DIRS`)만 훑어 infra-kit 안의 두 옛 값 「1.7+ native state encryption」 · `-kubernetes-version 1.30.0` 을 보지 못한다. 앞의 것을 그대로 등록하면 이 Phase research-log 항목의 변경 내역 줄이 걸리므로 `docs/infra/research-log.md` 를 allow 에 사유(이력 기록)와 함께 둔다. 뒤의 것은 검사 범위 안에서 0 건이다 |
| `plugin.json` | Final | infra-kit 버전(지금 0.3.1). Gotcha 하나 · 평가 사례 하나 · 보고 형태(네 칸)가 바뀌었다 |
| `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol | 다음 사이클 Phase 3 | 기준 원본이 2026-08-13 뒤에 바뀌었다(조항 1 의 N/A 표 · 새 조항 2 · 번호 3 이 둘). 킷 reviewer 일곱(api · backend · design · planning · rust · react · infra)의 §9 복제본에 둘 다 없다. 조항 2 가 킷 reviewer 에 맞는지와 번호 중복을 기준 원본 쪽이 먼저 정한 뒤 일곱이 같이 옮긴다 |
| `.claude/skills/kaizen-orchestrator/references/phase-research-templates.md` | 다음 사이클 | Phase 8 필수 출처 6 행의 기대값 「3 signals stable」 — OTel 상태는 signal 별로 다르다(infra-guide Gotcha 13). 레포 전용 파일이라 이 Phase 범위 밖이다 |
| `harness/skills/sprint/SKILL.md` | 다음 사이클 Phase 4 | Step 3 판정 표가 CI 에서만 보이는 두 경우(환경 · 비결정성, 미확정)를 받을지. 이 Phase 는 원문 표를 바꾸지 않고 cicd.md 원칙 7 에 표 밖 목록으로 붙였다 |
| `Flux v2.9` · Argo CD 3.5 | 다음 사이클 | 빠진 API 를 `operations/deployment-strategies.md` 원칙에 먼저 올린 뒤 감사 기준 GitOps 행에 붙일지 |
| `.claude/skills/infra-kaizen/SKILL.md` | 다음 사이클 | Gotcha 8 표의 「`infra-reviewer.md` §9 에 문구 변형 없이 복제」 가 기준 원본의 새 판과 어긋난다(위 Phase 3 행과 같이 푼다). Gotcha 6 형제 대조 표의 「미검증 3항」 은 이 Phase 뒤 infra-audit · infra-reviewer 가 네 칸을 쓰므로 네 칸으로 고친다. 레포 전용 파일이라 이 Phase 범위 밖이다 |

Final 이 더 할 것: 이 Phase 는 공유 파일(marketplace · plugin.json · 루트 README · 루트 CLAUDE.md · `docs/` HTML · 감사 기록 · 실패 횟수 파일 · 처리 배정표 ·
`.github/workflows/ci.yml` · `.harness/stale-values.yaml`)을 건드리지 않았다. CI 에 넣을 줄은 없다 — 새 평가 사례는 CI 가 이미 돌리는 `run-evals.py` 안에 있다.

## changelog 한 단락

infra-kit 이 빨간 CI 를 이번 변경 탓으로 단정하기 전에 원인부터 가르게 한다. 원칙은 `docs/infra/platform/cicd.md` 원칙 7 에 두고 — 원인을 이번 커밋 · 남의 미커밋 변경 ·
기준 커밋에서 이미 실패 · 환경 · 미확정 가운데 하나로 적고, 기준 커밋(`git merge-base`)을 깨끗한 임시 워크트리에서 다시 돌려 가르며, 판정 세 줄은 harness `/sprint`
Step 3 과 글자 그대로 같다 — infra-guide 가 Gotcha 14 로 그곳을 가리킨다. 기준 커밋에서 이미 실패하던 검사도 통과로 적거나 건너뛰지 않고, `gh run list --status success`
결과를 필수 검사 전부의 통과로 읽지 않는다. `[미검증]` 보고는 설계 가이드와 같은 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)으로 맞췄다(infra-test ·
infra-audit · infra-reviewer · 상태어 문서). infra-test 는 생성한 검사 스크립트를 답을 아는 작은 입력에 먼저 돌리게 하고, kubeconform 스키마 버전을 고정값 대신 대상
클러스터 버전 변수로 받는다. 근거로 뒷받침되지 않던 「OpenTofu 1.7+ native state encryption」 네 자리에서 버전을 뺐다. 평가 사례가 6 개가 됐다.

## 킷 로그 한 단락 (infra-kit)

2026-09-24 Phase 8 — infra-kaizen. 트리거 orchestrator-phase-8. 처리 배정표 `backend-family:P3` 하나와 앞 Phase 넘김 셋, 근거 파일 §3 · §5 의 사실 정정을 세 관심사로
묶었다(Gotcha 4 — 셋째는 낡았거나 출처가 없는 문장을 고치는 일이라 함께 했다). 근거:
[Git — git merge-base](https://git-scm.com/docs/git-merge-base) (기준 가지의 지금 끝이 아니라 공통 조상, 둘 이상일 수 있다 — 원칙 7 · Gotcha 14),
[GitHub CLI — gh run list](https://cli.github.com/manual/gh_run_list) (`--commit` · `--workflow` · `headSha` — `--workflow` 없는 성공 조회의 한계),
[GitHub — Re-running workflows and jobs](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs) (같은 `GITHUB_SHA` · `GITHUB_REF`),
[GitHub-hosted runners](https://docs.github.com/en/actions/reference/runners/github-hosted-runners) (job 마다 새 VM · `-latest`),
[GitHub — About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) (필수 검사는 성공 · skipped · neutral),
[Kubernetes v1.37.1](https://github.com/kubernetes/kubernetes/releases/tag/v1.37.1) (kubeconform 고정 `1.30.0` 을 변수로),
[OpenTofu state/plan encryption v1.11](https://opentofu.org/docs/v1.11/language/state/encryption/) (1.7 도입 연혁을 적지 않는다),
[OpenTelemetry specification status](https://opentelemetry.io/docs/specs/status/) (signal 별 상태 — README 이력 줄 정정 표시).
근거 파일이 밝힌 한계 — 세 분류를 규범으로 정한 공식 문서는 없다(그래서 분류는 킷 규칙이라고 적었다), HEAD 에서만 실패한 것은 상관 증거이지 원인 증명이 아니다,
GitHub 밖 CI 의 조회 명령은 없다.

## 다음 사이클 메모

- README 가 평가 사례 수를 숫자로 박은 문구 — 이 Phase 「평가 사례 6 개」 · backend-kit 「평가 사례 8 개」. 검사 개수는 숫자를 박지 않기로 한 것과 어긋난다. 두 킷을 함께 다룰지 정한다
- 네 칸 이름과 `env_gaps` 4 요건 이름이 infra-audit 한 파일 안에 같이 있다(위 그대로 둔 곳). reviewer §9 기준 원본을 새 판으로 옮길 때(Phase 3 넘김) 같이 정한다
- 넘김 안내에 「등록하라」 같은 행동 지시를 넣을 때는 그 도구의 실제 범위를 먼저 읽는다 — 2 회차 검토가 `check-stale-values.py` 를 돌려 보고서야 이 계약의 안내가 틀린 것을 찾았다. 측정은 토큰만 봐서 안내 글의 사실 여부를 못 잰다
- 계약 안 측정 도우미가 두 판을 풀고 DG-05 가 한 벌 더 복사해 한 번에 약 70 MB 를 쓴다. 여러 Phase 가 같은 디스크에서 동시에 돌 때 측정 준비 단계에 `df` 확인을 넣을 만하다
- 평가 사례 6 은 구조만 잰다 — 실제 스킬로 돌려 답이 assertion 넷을 채우는지는 결정론 측정이 없다(계약 `오라클 한계`)
- 계약 피드백 자기진단 `implementation_leakage` 가 true — 조건 줄에 측정 도우미 이름과 문서에 들어갈 문장이 글자 그대로 들어갔다. 산출물이 문서 문장이라 새 문장을 글자 그대로 세는 자리가 필요했다
