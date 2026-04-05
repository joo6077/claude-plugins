---
title: CI/CD
version: 0.1.0
last_updated: 2026-04-04
---

# CI/CD

GitHub Actions/GitLab CI 파이프라인 설계, OIDC 인증, 최소 권한 원칙, 캐싱 전략, 매트릭스 빌드, self-hosted runner 보안, 아티팩트 관리를 다룬다.

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
