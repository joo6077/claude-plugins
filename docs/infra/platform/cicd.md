---
title: CI/CD
version: 0.2.0
last_updated: 2026-09-25
---

# CI/CD

GitHub Actions/GitLab CI 파이프라인 설계, OIDC 인증, 최소 권한 원칙, 캐싱 전략, 매트릭스 빌드, self-hosted runner 보안, 아티팩트 관리, 빨간 검사의 원인 가르기를 다룬다.

---

## 원칙

### 1. DAG/needs 중심 설계로 임계경로를 최소화한다

모든 작업을 순차적으로 나열하면 불필요한 대기가 발생한다. `needs`(GitHub Actions) 또는 `needs`/`dependencies`(GitLab CI)로 작업 간 의존 관계를 명시하면, 독립적인 작업이 병렬로 실행되어 파이프라인 전체 시간이 줄어든다. 파이프라인을 DAG(Directed Acyclic Graph)로 설계한다.

> **출처:** [GitLab CI — needs](https://docs.gitlab.com/ci/yaml/needs/)

### 2. OIDC 단기 토큰을 기본으로 사용한다

클라우드 프로바이더(AWS, GCP, Azure) 접근에 장기 액세스 키를 CI secret에 저장하면 키 유출 시 무제한 접근이 가능해진다. OIDC federation으로 CI 작업 실행 시점에 단기 토큰을 발급받으면 토큰 수명이 제한되고, 키 로테이션이 불필요하며, 감사 추적이 용이하다.

> **출처:** [GitHub — Security hardening with OpenID Connect](https://docs.github.com/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect)

### 3. GITHUB_TOKEN/job token에 최소 권한을 부여한다

기본 토큰 권한을 `read-all`로 낮추고, 각 작업에서 필요한 권한만 `permissions` 블록으로 명시한다. 포크(fork)에서 오는 PR과 외부 기여자의 워크플로우는 별도 격리 전략을 적용한다. `pull_request_target` 사용 시 체크아웃 대상에 특히 주의한다.

> **출처:** [GitHub — GITHUB_TOKEN](https://docs.github.com/en/actions/concepts/security/github_token)

### 4. 캐시와 아티팩트를 구분하여 사용한다

캐시는 의존성(node_modules, pip 패키지, Go 모듈)을 재사용하여 설치 시간을 줄이는 용도다. 아티팩트는 빌드 산출물(바이너리, 테스트 리포트)을 후속 작업에 전달하거나 다운로드하는 용도다. 캐시는 hit/miss가 결과에 영향을 주면 안 되고, 아티팩트는 누락 시 파이프라인이 실패해야 한다.

> **출처:** [GitHub — Dependency caching](https://docs.github.com/actions/concepts/workflows-and-actions/dependency-caching)

### 5. Self-hosted runner는 ephemeral을 우선한다

장수(long-lived) runner는 이전 작업의 파일, 환경변수, 프로세스가 잔존하여 보안 위험과 재현 불가능한 빌드를 만든다. 매 작업마다 새 인스턴스를 생성하고 작업 후 폐기하는 ephemeral 패턴을 기본으로 한다. 비신뢰 코드(외부 PR)가 실행되는 인프라로 간주하고 네트워크를 격리한다.

> **출처:** [GitLab Runner — Security](https://docs.gitlab.com/runner/security/)

### 6. 매트릭스 빌드는 커버리지 확장용이다

OS, 언어 버전, 의존성 조합을 매트릭스로 구성하여 호환성 커버리지를 넓힌다. `max-parallel`로 동시 실행 수를 제어하고, `fail-fast`로 첫 실패 시 나머지를 취소할지 결정한다. 매트릭스가 과도하면 리소스 낭비와 큐 대기가 발생하므로 실제 배포 대상 조합으로 제한한다.

> **출처:** [GitHub — Using a matrix for your jobs](https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs)

### 7. 빨간 검사는 고치기 전에 원인부터 가른다

여럿이 같이 쓰는 가지에서는 빨간 검사가 이번 변경 탓이 아닌 경우가 많다. 원인을 가르지 않고 고치기 시작하면 남이 깬 것을 쫓느라 시간을 쓴다.
원인은 이번 커밋 · 남의 미커밋 변경 · 기준 커밋에서 이미 실패 · 환경 · 미확정 가운데 하나로 적는다. 이 분류는 이 킷의 규칙이다 — Git · GitHub
문서는 기준 커밋을 구하는 방법, 커밋별 실행 기록 조회, 같은 커밋 재실행 같은 수단만 준다.

기준 커밋 `FORK_BASE` 는 `git merge-base HEAD origin/<기준 가지>` 로 구한다. 기준 가지의 지금 끝이 아니라 두 이력의 공통 조상이다. 이력이 복잡하면
merge base 가 둘 이상일 수 있으니 어느 것을 골랐는지 적는다. 같은 명령을 깨끗한 임시 워크트리에서 다시 돌려 가른다. 임시 워크트리에는 추적하지 않는
파일(설치한 의존성 · 빌드 산출물)이 없으니 `<실패한 검사 명령>` 앞에 그 프로젝트의 준비 명령을 붙인다 — 안 붙이면 준비가 안 된 탓의 실패를 기준 커밋
탓으로 읽는다.

```bash
FORK_BASE=$(git merge-base HEAD origin/<기준 가지>)
for ref in HEAD "$FORK_BASE" origin/<기준 가지>; do
  t=$(mktemp -d)
  git worktree add -q --detach "$t" "$ref"
  ( cd "$t" && <실패한 검사 명령> ) >/dev/null 2>&1
  rc=$?
  echo "$ref $(git rev-parse --short "$ref") exit=$rc"
  git worktree remove --force "$t"
done
```

| 공용 작업 폴더 | `HEAD` 임시 | `FORK_BASE` 임시 | 판정 |
| --- | --- | --- | --- |
| 실패 | 통과 | — | 미커밋 변경 탓 — `git status --short` 의 파일이 내가 쓴 목록 밖이면 남의 미커밋이다 |
| 실패 | 실패 | 실패 | 기준 커밋에서 이미 실패 — 내 변경 전부터다 |
| 실패 | 실패 | 통과 | 이번 커밋 탓일 가능성이 크다 |

위 세 줄은 harness `/sprint` Step 3 의 판정과 같은 말이다. `origin/<기준 가지>` 줄은 분기 뒤 기준 가지가 깨졌는지를 본다. CI 에서만 보이는 두 경우를 더한다.

- **환경 · 비결정성** — 같은 커밋을 다시 돌렸는데 결과가 달라진다. GitHub 재실행은 원 실행과 같은 `GITHUB_SHA` · `GITHUB_REF` 를 쓰고, 실패한 job 만
  다시 돌리거나 디버그 로그를 켤 수 있다. GitHub 호스트 runner 는 job 마다 새 VM 이고 `-latest` 는 GitHub 가 정한 최신 안정 이미지라 runner 이미지 ·
  도구 버전도 원인 후보다
- **미확정** — 기록도 재현 환경도 없어 가를 수 없다. 억지로 셋 중 하나에 넣지 말고 「미확정 — 같은 커밋 재실행이 필요하다」 로 적는다

「기준 커밋에서 이미 실패」 는 같은 검사에서 같은 핵심 오류가 날 때만이다. 이름만 같은 검사의 다른 오류는 별개다. 이미 실패하던 검사는 이번 변경의
회귀로 세지 않되 따로 보고하고, 그 이유로 필수 검사를 건너뛰거나 통과로 적지 않는다. `HEAD` 에서만 실패하고 기준 커밋에서 통과해도 이번 변경과 함께
나타났다는 증거일 뿐 원인 증명은 아니다 — 비결정적 테스트 · 외부 서비스 · 캐시 · 시간 의존 때문에 같은 커밋도 결과가 달라질 수 있다.

GitHub Actions 라면 기준 커밋의 실행 기록은 `gh run list --commit <sha>` 로 찾는다. 최근 성공 커밋에서 가지를 자를 때
`gh run list --branch <가지> --status success --limit 1 --json headSha` 를 그대로 쓰지 마라 — `--workflow` 가 없어 문서 빌드처럼 필수가 아닌 workflow
하나만 성공한 커밋도 나온다. 그 커밋에서 보호 가지의 필수 검사가 전부 성공 · skipped · neutral 인지 확인하고, 옛 커밋에서 잘랐으면
`<고른 커밋>..origin/<기준 가지>` 로 빠지는 커밋 범위를 함께 보고한다. GitHub 밖 CI 의 같은 조회 명령은 이 문서의 근거에 없다.

> **출처:** [Git — git merge-base](https://git-scm.com/docs/git-merge-base) · [GitHub CLI — gh run list](https://cli.github.com/manual/gh_run_list) · [GitHub — Re-running workflows and jobs](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs) · [GitHub-hosted runners](https://docs.github.com/en/actions/reference/runners/github-hosted-runners) · [GitHub — About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)

---

## 수치/기준값

| 항목 | 값 | 비고 |
|------|-----|------|
| GitHub Actions 매트릭스 최대 jobs | 256 | 워크플로우 실행당 |
| 아티팩트 보존 기본 기간 | 90일 | 리포지토리 설정에서 변경 가능 |
| GITHUB_TOKEN 최대 수명 | 24시간 | 작업 종료 시 자동 만료 |
| Self-hosted runner 업데이트 기한 | 30일 | 이내 미업데이트 시 작업 거부 |
| GitLab needs 최대 의존 수 | 50개/job | 초과 시 파이프라인 생성 실패 |

---

## 안티패턴

- **장기 클라우드 키를 CI secret에 고정**: 키 로테이션을 잊으면 유출 시 무제한 접근. OIDC federation으로 대체
- **캐시와 아티팩트 혼용**: 캐시를 아티팩트처럼 쓰면 캐시 미스 시 빌드 실패. 아티팩트를 캐시처럼 쓰면 불필요한 저장 비용
- **모든 브랜치에서 풀 파이프라인 실행**: feature 브랜치에서 전체 배포 파이프라인을 돌리면 리소스 낭비. 브랜치별 필터로 실행 범위 제한
- **장수 공유 runner**: 상태가 축적되어 "내 로컬에서는 되는데" 문제 재현. ephemeral 패턴 필수
- **matrix 폭발**: OS 3종 x 언어 5버전 x 의존성 3버전 = 45 jobs. 실제 배포 대상만 포함하고 나머지는 nightly로 분리

---

## Gotchas

- **GitHub secret masking은 구조화된 값에서 실패한다.** JSON, multiline 문자열 등 구조화된 secret은 로그에서 마스킹이 불완전할 수 있다. `::add-mask::`로 개별 값을 명시적으로 마스킹하거나, 로그 출력 자체를 억제한다.
- **GitLab needs는 이전 stage의 아티팩트를 자동으로 전달하지 않는다.** `needs`를 사용하면 기존 stage 순서 기반 아티팩트 전달이 무시된다. `needs`에 명시한 job의 아티팩트만 전달되므로, 필요한 아티팩트를 생성하는 job을 `needs`에 포함해야 한다.
- **포크 PR의 권한 모델은 원본 리포와 다르다.** 포크에서 오는 `pull_request` 이벤트는 `GITHUB_TOKEN`이 read-only이고, secret에 접근할 수 없다. `pull_request_target`은 원본 리포 컨텍스트에서 실행되므로 포크 코드를 체크아웃하면 코드 인젝션 위험이 있다.
- **Self-hosted runner에 이전 작업의 파일이 남는다.** ephemeral이 아닌 runner에서 `$GITHUB_WORKSPACE` 외부에 생성된 파일, Docker 이미지, 환경변수가 다음 작업에 영향을 줄 수 있다. 작업 시작 시 정리 스크립트를 실행하거나 ephemeral runner를 사용한다.
