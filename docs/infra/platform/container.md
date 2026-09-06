---
title: 컨테이너
version: 0.1.0
last_updated: 2026-04-04
---

# 컨테이너

Dockerfile 작성, 멀티스테이지 빌드, 레이어 캐싱, 이미지 보안, docker-compose 프로덕션 운영, 리소스 제한, 헬스체크, 로깅 전략을 다룬다.

---

## 원칙

### 1. 멀티스테이지 빌드를 기본으로 사용한다

빌드 도구(컴파일러, 패키지 매니저, 테스트 프레임워크)는 빌드 스테이지에만 존재해야 한다. 최종 이미지에는 런타임에 필요한 바이너리와 설정만 복사한다. 이미지 크기가 줄고, 공격 표면이 축소되며, 빌드 캐시 효율이 올라간다. `COPY --from=builder`로 필요한 산출물만 가져온다.

> **출처:** [Docker — Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)

### 2. .dockerignore로 빌드 컨텍스트를 최소화한다

`.git`, `node_modules`, `.env`, 테스트 디렉토리 등 빌드에 불필요한 파일을 제외한다. 빌드 컨텍스트가 크면 전송 시간이 늘고, 민감 정보가 이미지에 포함될 수 있으며, 관련 없는 파일 변경이 레이어 캐시를 무효화한다.

> **출처:** [Docker — Dockerfile best practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

### 3. non-root 사용자로 실행을 강제한다

`USER` 지시어로 비특권 사용자를 지정한다. 베이스 이미지는 distroless 또는 minimal(alpine, slim) 계열을 우선한다. distroless에는 셸이 없어 컨테이너 탈출 공격을 원천 차단한다. Trivy 등 스캐너로 알려진 CVE를 CI에서 정기 점검한다.

> **출처:** [Dockerfile reference — USER](https://docs.docker.com/reference/builder/)

### 4. 프로덕션 Compose는 개발용 설정과 분리한다

개발 환경의 바인드 마운트, 디버그 포트, 소스 코드 동기화를 프로덕션에 가져가지 않는다. `docker-compose.yml`(공통) + `docker-compose.prod.yml`(오버라이드) 구조로 환경별 설정을 분리하고, 프로덕션에서는 `restart: always`, 로그 드라이버, 리소스 제한을 명시한다.

> **출처:** [Docker — Use Compose in production](https://docs.docker.com/compose/how-tos/production/)

### 5. CPU/메모리/PIDs 제한을 명시한다

컨테이너에 리소스 상한을 두지 않으면 단일 워크로드가 호스트 전체를 점유하는 noisy-neighbor 문제가 발생한다. 메모리 초과 시 커널 OOM killer가 임의 프로세스를 종료하므로, 워크로드별 하드 리밋을 설정하여 예측 가능한 격리를 확보한다.

> **출처:** [Docker — Resource constraints](https://docs.docker.com/engine/containers/resource_constraints/)

### 6. 헬스체크는 트래픽 처리 가능성을 검증한다

프로세스가 살아 있어도 데드락, 커넥션 풀 고갈, 초기화 미완료 등으로 요청을 처리하지 못할 수 있다. `HEALTHCHECK` 지시어의 CMD는 실제 엔드포인트(`/healthz`, `/readyz`)를 호출하여 애플리케이션 수준의 준비 상태를 확인해야 한다.

> **출처:** [Dockerfile reference — HEALTHCHECK](https://docs.docker.com/reference/dockerfile/)

### 7. 로그는 stdout/stderr로 출력한다

컨테이너 내부 파일에 로그를 쓰면 수집이 어렵고 디스크가 차서 장애가 발생한다. stdout/stderr로 보내면 Docker 로깅 드라이버가 수집하고, 외부 시스템(ELK, Loki, CloudWatch)으로 라우팅할 수 있다. `json-file` 드라이버는 반드시 `max-size`/`max-file` 로테이션을 설정한다.

> **출처:** [Docker — Configure logging drivers](https://docs.docker.com/engine/logging/configure/)

---

## 수치/기준값

| 항목 | 값 | 비고 |
|------|-----|------|
| 메모리 하드 리밋 최소값 | 6m | Docker가 허용하는 최저값 |
| CPU CFS period | 100000us (100ms) | `--cpu-period` 기본값 |
| `--cpus="0.5"` | quota 50000 / period 100000 | 0.5 CPU 코어 상당 |
| Compose healthcheck interval | 30s | 기본값 |
| Compose healthcheck timeout | 30s | 기본값 |
| Compose healthcheck retries | 3 | 기본값 |
| Compose healthcheck start_period | 0s | 기본값 |
| local 로깅 드라이버 기본 용량 | 100MB | 20MB x 5 파일 |

---

## 안티패턴

- **빌더 포함 단일 스테이지**: 컴파일러, 소스, 테스트 도구가 프로덕션 이미지에 남아 크기 비대 + 공격 표면 확대
- **루트 실행**: `USER` 없이 PID 1이 root로 실행되면 컨테이너 탈출 시 호스트 권한 획득 가능
- **소스 전체 먼저 COPY**: 의존성 설치 전에 소스를 복사하면 코드 한 줄 변경에도 의존성 레이어 캐시가 무효화됨. 의존성 파일(package.json, go.sum 등)을 먼저 COPY → install → 소스 COPY 순서로
- **json-file 무제한**: `max-size`/`max-file` 없이 json-file 드라이버를 쓰면 디스크 포화로 호스트 장애
- **readiness 없는 depends_on**: `depends_on`은 컨테이너 시작만 보장하고 애플리케이션 준비 상태는 확인하지 않음. `condition: service_healthy` 필수

---

## Gotchas

- **docker compose의 depends_on은 running과 ready를 구분하지 않는다.** DB 컨테이너가 시작되었어도 커넥션을 받을 준비가 안 됐을 수 있다. `depends_on.condition: service_healthy`를 사용해야 실제 준비 상태를 기다린다.
- **메모리 제한 초과가 즉시 kill이 아닐 수 있다.** 커널 OOM killer는 메모리 압박 상황에서 점수 기반으로 프로세스를 선택하므로, 제한을 초과한 컨테이너가 즉시 종료되지 않는 경우가 있다. `--oom-kill-disable`은 더 위험하다.
- **`--memory-swap` 의미를 오해한다.** `--memory=300m --memory-swap=1g`은 swap이 1g가 아니라 메모리+swap 합계가 1g이라는 뜻이다. 즉 swap 사용량은 700m이다.
- **기존 컨테이너는 daemon 로깅 설정을 상속하지 않는다.** daemon.json의 로깅 드라이버를 변경해도 이미 실행 중인 컨테이너에는 적용되지 않는다. 컨테이너를 재생성해야 한다.
