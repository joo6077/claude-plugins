---
phase: 8
title: "Phase 8 infra-kit — 확보된 외부 근거"
collected: 2026-09-24
method: codex (foreground, 직접 호출 · gpt-5.6-sol · 조회는 curl/gh)
inputs: 처리 배정표(.claude/kaizen-input/insights-report.md)의 Phase 8 행 · phase-research-templates.md Phase 8 필수 출처 · 현행화 점검
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치를 지어내지 마라. 없으면 미반영으로 남긴다.
---

조사 기준일은 2026-09-24이며, 저장소는 변경하지 않았다. `git status --short`와 `git diff --stat` 모두 비어 있었다.

## 1. 출처 목록

### 필수 소스 — 6건 모두 실제 조회

1. [Kubernetes Pod Security Admission](https://kubernetes.io/docs/concepts/security/pod-security-admission/)
2. [Terraform ephemeral block](https://developer.hashicorp.com/terraform/language/ephemeral)
3. [OpenTofu state/plan encryption v1.11](https://opentofu.org/docs/v1.11/language/state/encryption/)
4. [SLSA provenance](https://slsa.dev/provenance)
5. [Sigstore Cosign attestation verification](https://docs.sigstore.dev/cosign/verifying/attestation/)
6. [OpenTelemetry specification status](https://opentelemetry.io/docs/specs/status/)

### CI 실패 분류 근거

- [GitHub CLI — `gh run list`](https://cli.github.com/manual/gh_run_list)
- [GitHub — protected branches와 required status checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub — workflow/job 재실행](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs)
- [GitHub-hosted runners](https://docs.github.com/en/actions/reference/runners/github-hosted-runners)
- [Git — `git merge-base`](https://git-scm.com/docs/git-merge-base)

### 최신 버전·변경 확인에 사용한 공식 릴리스

- [Kubernetes v1.37.1](https://github.com/kubernetes/kubernetes/releases/tag/v1.37.1), [v1.37 changelog](https://github.com/kubernetes/kubernetes/blob/v1.37.1/CHANGELOG/CHANGELOG-1.37.md)
- [Terraform v1.16.4](https://github.com/hashicorp/terraform/releases/tag/v1.16.4), [v1.16.0 notes](https://github.com/hashicorp/terraform/releases/tag/v1.16.0)
- [OpenTofu v1.12.6](https://github.com/opentofu/opentofu/releases/tag/v1.12.6)
- [Cosign v3.1.3](https://github.com/sigstore/cosign/releases/tag/v3.1.3)
- [OpenTelemetry specification v1.61.0](https://github.com/open-telemetry/opentelemetry-specification/releases/tag/v1.61.0)
- [Argo CD v3.5.3](https://github.com/argoproj/argo-cd/releases/tag/v3.5.3), [3.4→3.5 upgrade guide](https://argo-cd.readthedocs.io/en/stable/operator-manual/upgrading/3.4-3.5/)
- [Flux v2.9.5](https://github.com/fluxcd/flux2/releases/tag/v2.9.5), [v2.9.0 notes](https://github.com/fluxcd/flux2/releases/tag/v2.9.0)
- [Gateway API v1.6.2](https://github.com/kubernetes-sigs/gateway-api/releases/tag/v1.6.2)
- [Karpenter v1.14.1](https://github.com/kubernetes-sigs/karpenter/releases/tag/v1.14.1)
- [Crossplane v2.4.2](https://github.com/crossplane/crossplane/releases/tag/v2.4.2), [v2.4.0 notes](https://github.com/crossplane/crossplane/releases/tag/v2.4.0)
- [Grafana Alloy v1.19.2](https://github.com/grafana/alloy/releases/tag/v1.19.2)
- [hadolint v2.15.1](https://github.com/hadolint/hadolint/releases/tag/v2.15.1)
- [actionlint v1.7.12](https://github.com/rhysd/actionlint/releases/tag/v1.7.12)
- [kubeconform v0.8.0](https://github.com/yannh/kubeconform/releases/tag/v0.8.0)

## 2. 항목별 관찰 사실

### backend-family:P3.1 — 실패를 내 변경·기준 실패·환경으로 구분

확인된 사실:

- `gh run list`는 `--commit <SHA>`, `--branch <branch>`, `--status`, `--workflow`, `--limit` 필터와 `headSha`, `workflowName`, `conclusion`, `createdAt` 등의 JSON 필드를 지원한다. 따라서 특정 기준 SHA에 실행 기록이 있는지 찾는 예시는 공식 CLI 계약과 맞는다. [출처](https://cli.github.com/manual/gh_run_list)
- Git의 “브랜치가 갈라져 나온 커밋”은 단순히 현재 base 브랜치 HEAD가 아니라 두 이력의 best common ancestor, 즉 merge base로 구하는 것이 정확하다. 다만 복잡한 이력에는 merge base가 둘 이상일 수도 있다. [출처](https://git-scm.com/docs/git-merge-base)
- GitHub 재실행은 원 실행과 같은 `GITHUB_SHA`와 `GITHUB_REF`를 사용하고, 실패한 job만 다시 실행하거나 debug logging을 켤 수 있다. 동일 SHA 재실행 결과가 달라지는지 확인하는 환경·비결정성 조사에 쓸 수 있다. [출처](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs)
- GitHub-hosted 표준 runner는 job마다 새 VM을 사용한다. 또한 `-latest`는 OS 공급자의 최신판이 아니라 GitHub가 제공하는 최신 안정 이미지라는 뜻이다. 따라서 코드 외 runner 이미지·도구 환경도 실패 원인 후보가 된다. [출처](https://docs.github.com/en/actions/reference/runners/github-hosted-runners)

추론:

- “HEAD에서 실패했고 merge base의 동일 검사·동일 조건에서는 성공했다”는 내 변경과의 상관 증거지만, 곧바로 단일 변경의 인과 증명은 아니다. 비결정적 테스트, 외부 서비스, 캐시, 시간 의존성 때문에 같은 SHA도 결과가 달라질 수 있다.
- 따라서 세 분류를 쓰더라도 `환경`을 확정하기 어려운 경우를 억지로 넣지 말고 `미확정—동일 SHA 재실행 필요` 상태를 허용해야 한다.
- “기준 커밋에서 이미 실패”도 그 실패가 현재 실패와 같은 검사·같은 failure signature일 때만 상속 실패로 보아야 한다. 이름만 같은 job의 다른 오류는 별개다.

반대·제한 근거:

- 조회한 공식 문서 중 “실패 원인을 반드시 이 세 가지로 분류하라”는 규범은 찾지 못했다. 공식 문서는 SHA 필터, 재실행, runner 특성 같은 조사 수단만 제공한다.
- merge base가 둘 이상일 수 있으므로 “기준 커밋”을 항상 단일 SHA라고 전제하면 틀릴 수 있다. [출처](https://git-scm.com/docs/git-merge-base)

### backend-family:P3.1 — 최근 성공 커밋에서 출시/작업 브랜치 생성

확인된 사실:

- `gh run list --branch <b> --status success --limit 1 --json headSha`는 성공한 최근 workflow run 하나의 SHA를 얻는 명령이다. `--workflow`가 없으므로 어떤 workflow의 성공인지 제한하지 않는다. [출처](https://cli.github.com/manual/gh_run_list)
- GitHub의 required status checks는 보호 브랜치에 설정된 모든 필수 check/status가 성공·skipped·neutral이어야 한다는 별도 개념이다. strict 모드라면 base 브랜치 최신 상태와 동기화되어야 하며, merge queue는 최신 target branch와 결합된 결과를 다시 검사한다. [출처](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)

반대 근거:

- 제안된 bare 명령은 “필수 검사가 모두 통과한 커밋”을 보장하지 않는다. 문서 빌드 같은 비필수 workflow 하나만 성공한 SHA도 반환할 수 있다.
- 오래된 green SHA에서 새 브랜치를 자르면 그 이후 base 브랜치 변경을 조용히 제외할 수 있다.

추론:

- 계약은 “최근 성공 workflow run”이 아니라 “동일 SHA에서 적용 대상 필수 검사 집합 전체가 허용 결론인 커밋”으로 써야 한다.
- 오래된 green SHA를 선택하면 `선택 SHA..현재 base HEAD`의 제외 커밋 범위를 보고해야 한다.

### backend-family:P3.2 — 키워드 두 표면 동시 수정

저장소 확인 결과:

- canonical 위치는 [infra-guide/SKILL.md:40](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/infra-kit/skills/infra-guide/SKILL.md:40)과 [principle-index.md:9](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/infra-kit/references/principle-index.md:9)이다.
- `skills/infra-guide/references/principle-index.md`는 별도 옛 사본으로 존재한다. 이번 요구대로 수정 대상에서 제외하는 것이 현재 참조 경로(`../../references/principle-index.md`)와 일치한다.
- 이 동기화 규칙은 저장소 내부 계약이다. 이를 직접 규정하는 외부 근거는 조회하지 않았고 필요하지 않다.

### backend-family:P3.3 — `cicd.md` 원칙 7과 출처

- [cicd.md:13](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/docs/infra/platform/cicd.md:13) 이하에는 현재 원칙 1~6만 있다.
- Gotcha 4는 principle-index로 찾은 리서치 문서를 읽고 답하도록 요구하므로, Gotcha 14만 추가하고 `cicd.md`를 갱신하지 않으면 내부 계약이 끊어진다.
- 원칙 7의 외부 근거로는 `gh run list`, GitHub required checks, workflow 재실행, Git merge-base 문서를 함께 쓰는 것이 적절하다. 어느 한 문서도 세 분류 전체를 단독 규정하지는 않는다.

### 필수 소스 관찰

- Kubernetes PSA는 Kubernetes v1.25부터 stable이다. namespace별로 `enforce`, `audit`, `warn` 모드와 `privileged`, `baseline`, `restricted` 수준을 조합한다. [출처](https://kubernetes.io/docs/concepts/security/pod-security-admission/)
- Terraform 최신 문서는 v1.16.x를 latest로 표시했다. `ephemeral` resource와 write-only 인수는 값을 state와 plan 파일에 저장하지 않는다. [출처](https://developer.hashicorp.com/terraform/language/ephemeral)
- OpenTofu v1.11 문서는 state와 plan 각각에 encryption을 설정하고 `enforced`와 migration용 `fallback`을 지원한다. 현재 지원되는 내장 암호화 method는 AES-GCM이라고 명시한다. [출처](https://opentofu.org/docs/v1.11/language/state/encryption/)
- SLSA provenance 페이지는 SLSA v1.2, status Approved이며 build provenance와 source provenance를 구분한다. [출처](https://slsa.dev/provenance)
- Cosign 문서는 `cosign attest`와 `cosign verify-attestation`, CUE/Rego `--policy` 검증을 보여 주며 정책은 attestation의 predicate 부분을 대상으로 작성하라고 한다. 이 페이지 자체에서는 “Cosign v3 bundle/trusted-root 사용 의무”를 확인하지 못했다. [출처](https://docs.sigstore.dev/cosign/verifying/attestation/)
- OpenTelemetry 상태는 signal/component별로 다르다. tracing API/SDK/protocol은 stable, metrics는 API·protocol stable이나 SDK mixed, logging bridge API/SDK/protocol은 stable, profiles protocol은 development다. “3 signals 모두 stable”은 부정확하다. [출처](https://opentelemetry.io/docs/specs/status/)

## 3. 현행화 — 낡은 곳

| 위치 | 현재 값 | 최신 확인값·판정 |
|---|---|---|
| [infra-test/SKILL.md:382](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/infra-kit/skills/infra-test/SKILL.md:382) | `kubeconform -kubernetes-version 1.30.0` | Kubernetes 최신 안정판은 [v1.37.1](https://github.com/kubernetes/kubernetes/releases/tag/v1.37.1). 고정 예제가 명백히 낡았다. 단, 무조건 1.37.1로 바꾸기보다 프로젝트 target cluster 버전을 탐지해야 한다. |
| [infra-kit/README.md:59](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/infra-kit/README.md:59) | `OpenTelemetry 3 signals stable` | metrics SDK는 mixed이고 profiles protocol은 development다. [현재 status](https://opentelemetry.io/docs/specs/status/)와 충돌한다. |
| [docs/infra/research-log.md:124](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/docs/infra/research-log.md:124) | status를 정확히 나열한 뒤 `"3 신호 stable" 서술 유지 가능` | 같은 행 내부에서 자기모순이다. metrics SDK mixed라는 원문상 해당 결론은 유지 불가다. |
| [docs/infra/research-log.md:120](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/docs/infra/research-log.md:120) | Terraform 문서 latest `v1.15.x` | 현재 latest는 [v1.16.4](https://github.com/hashicorp/terraform/releases/tag/v1.16.4). 다만 날짜가 있는 과거 조사 로그라면 역사 기록으로 남기고 “당시 조회값”임을 명확히 하는 편이 낫다. |
| [infra-guide/SKILL.md:46](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/infra-kit/skills/infra-guide/SKILL.md:46), [audit-criteria.md:158](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/infra-kit/references/audit-criteria.md:158), [audit-criteria.md:165](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/infra-kit/references/audit-criteria.md:165) | Flux `v2.8`/`v2.8+`와 v2.8 출처 | 최신 안정판은 [v2.9.5](https://github.com/fluxcd/flux2/releases/tag/v2.9.5). `v2.8+`라는 최소 조건 자체는 거짓이 아니지만, v2.9에서 `image.toolkit.fluxcd.io/v1beta2`와 `notification.toolkit.fluxcd.io/v1beta2`가 제거되었다. [v2.9.0 notes](https://github.com/fluxcd/flux2/releases/tag/v2.9.0) |
| [init-checklist.md:120](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/infra-kit/references/init-checklist.md:120), [audit-criteria.md:90](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/infra-kit/references/audit-criteria.md:90) | 출처 라벨 `Karpenter v1.11` | 최신 안정판은 [v1.14.1](https://github.com/kubernetes-sigs/karpenter/releases/tag/v1.14.1). `v1.11+` 최소 조건과 최신판 표기를 구분해야 한다. |
| [init-checklist.md:141](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/infra-kit/references/init-checklist.md:141), [audit-criteria.md:112](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/infra-kit/references/audit-criteria.md:112) | OpenTofu v1.11 문서 고정 URL | 최신 안정판은 [v1.12.6](https://github.com/opentofu/opentofu/releases/tag/v1.12.6). v1.11 기능 설명은 유효할 수 있으나 최신 문서 포인터는 아니다. |
| [audit-criteria.md:158](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/infra-kit/references/audit-criteria.md:158) | Argo CD `3.x`만 언급 | 최신 안정판은 [v3.5.3](https://github.com/argoproj/argo-cd/releases/tag/v3.5.3). 3.5에는 Helm 4 전환, HTTP OCI registry 대응, React 19 UI extension 재빌드, `--repo-server-strict-tls` 폐기 예정 같은 마이그레이션 사항이 있다. [업그레이드 가이드](https://argo-cd.readthedocs.io/en/stable/operator-manual/upgrading/3.4-3.5/) |

### 2026-08-13 이후 특히 반영할 변경

- Kubernetes v1.37.0은 2026-08-26 공개됐다. `SELinuxMount`가 기본 활성화되어 기존 workload를 깨뜨릴 수 있고, `scheduling.k8s.io/v1alpha2`가 제거됐으며, `eventRecordQPS=0` 의미가 unlimited로 정정됐다. [changelog](https://github.com/kubernetes/kubernetes/blob/v1.37.1/CHANGELOG/CHANGELOG-1.37.md)
- Terraform v1.16.0은 2026-08-26 공개됐다. upgrade note는 provisioner의 `bastion_host_key`가 이제 실제 적용되므로 기존 설정의 키를 확인하라고 요구한다. [릴리스](https://github.com/hashicorp/terraform/releases/tag/v1.16.0)
- OpenTofu v1.12.6은 2026-08-19 공개됐다. OCI registry redirect에 원 origin credential이 잘못 재전송될 수 있던 문제와 악성 backend/registry 응답에 의한 CPU·메모리 과다 사용 문제를 수정했다. [릴리스](https://github.com/opentofu/opentofu/releases/tag/v1.12.6)
- Crossplane v2.4.0은 2026-08-20 공개됐다. CLI 배포 위치가 `releases.crossplane.io`에서 `cli.crossplane.io`로 완전히 이동했고 바이너리명이 `crank`에서 `crossplane`으로 바뀌었다. package runtime의 server-side apply 및 safe-start scale-to-zero 동작도 기존 운영 가정에 영향을 줄 수 있다. [릴리스](https://github.com/crossplane/crossplane/releases/tag/v2.4.0)

## 4. 권장안

Phase 계약은 다음처럼 잡을 만하다.

1. 기준 SHA는 먼저 기록한다.

   - Git이면 `git merge-base HEAD <base-ref>`를 기본으로 한다.
   - merge base 복수, rebase, merge queue 사용 시 어떤 SHA를 기준으로 택했는지 명시한다.

2. 실패 단위를 workflow 전체가 아니라 `workflow/job/test 이름 + 핵심 failure signature`로 고정한다.

3. HEAD와 기준 SHA에 같은 명령·같은 도구 버전·가능한 한 같은 runner 조건을 적용한다.

4. 보고 상태는 다음 네 가지가 안전하다.

   - `내 변경`: 기준은 통과하고 변경 SHA에서 재현
   - `기준 커밋에서 이미 실패`: 기준에서도 동일 failure signature 재현
   - `환경/비결정성`: 동일 SHA의 반복 실행 결과가 달라지거나 runner·외부 의존 실패 증거 존재
   - `미확정`: 기록·재현 환경이 없어 인과 판정 불가

5. 기준에서 이미 실패한 항목은 현재 변경의 회귀로 세지 않되, 별도 baseline debt로 보고한다. “이미 실패했다”는 이유만으로 필수 검사를 무시하거나 성공으로 처리해서는 안 된다.

6. GitHub 예시는 다음 의미로 제한한다.

   - 기록 탐색: `gh run list --commit <sha>`
   - bare `gh run list --branch <b> --status success --limit 1 --json headSha`를 “필수 검사 통과 SHA” 판정에 사용하지 않는다.
   - branch 생성 SHA는 동일 커밋에 적용되는 필수 검사 집합 전체의 결론을 확인한다.
   - 과거 green SHA를 택하면 그 SHA부터 현재 base HEAD까지 제외되는 커밋 범위를 함께 보고한다.

7. Gotcha 14, 두 canonical 키워드 표면, `cicd.md` 원칙 7을 하나의 변경 단위로 묶는다. 제목은 제안대로 유지할 수 있지만 본문에는 `미확정`과 bare `gh run list`의 한계를 넣는 것이 필요하다.

8. 현행화에서는 최소 기능 버전과 최신 안정 버전을 구분한다. 예를 들어 “Terraform 1.10+에서 ephemeral 지원”은 기능 하한이고, 현재 최신 안정판이 1.16.4라는 사실과 모순되지 않는다.

## 5. 못 가져온 것 / 열린 질문

- GitHub 외 GitLab·Jenkins·Buildkite가 기준 SHA의 필수 검사 집합을 조회하는 동등 명령은 이번 조사에서 가져오지 않았다.
- 공식 문서에서 “내 변경 / 기준 실패 / 환경”이라는 정확한 3분류 표준은 찾지 못했다. 이번 권장 분류는 조회한 Git·GitHub 기능을 조합한 추론이다.
- OpenTofu v1.11 state-encryption 문서는 “state encryption이 최초로 1.7에서 도입됐다”는 연혁을 명시하지 않았다. 따라서 해당 URL만으로 `OpenTofu 1.7+ native state encryption`을 출처화할 수 없다.
- Terraform ephemeral 페이지는 현재 v1.16.x latest를 보여 주지만, 이 조회에서 기능 최초 도입 버전을 직접 확인하지 않았다.
- Cosign attestation 문서는 CUE/Rego predicate 검증은 확인해 주지만 v3 bundle/trusted-root 의무를 뒷받침하지 않는다. v3 전용 계약에는 별도 [Cosign v3 릴리스](https://blog.sigstore.dev/cosign-3-0-available/) 근거를 써야 한다.
- SLSA provenance 페이지는 v1.2 Approved를 확인하지만 모든 저장소에 즉시 특정 SLSA level을 강제하라는 근거는 제공하지 않는다. 릴리스 산출물이 실제로 있는 경우에만 게이트로 삼는 현재 조건부 정책이 더 안전하다.
