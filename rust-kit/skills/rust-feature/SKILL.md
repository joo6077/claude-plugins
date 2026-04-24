---
name: rust-feature
description: >
  feature 모듈을 프로젝트 아키텍처에 맞는 구조로 스캐폴딩한다.
  handler + service + model + test 디렉토리를 생성하고 mod.rs에 등록한다.
  "모듈 추가", "feature 생성", "새 기능 모듈", "rust feature" 같은 요청 시 트리거.
  프로젝트 자체를 새로 만들 때는 트리거하지 않는다 — rust-init 사용.
argument-hint: "<feature-name>"
user-invocable: true
---

# Gotchas

1. **`mod.rs` vs 파일 모듈 혼용 금지** — 프로젝트 기존 패턴을 따른다. 한 프로젝트에서 두 방식을 섞지 않는다.
2. **workspace 순환 의존 금지** — domain 크레이트가 api나 infra를 의존하면 안 된다. 의존 방향: `apps → modules ← shared` (또는 `api → domain ← infra`). modules/* 끼리도 직접 의존 금지 — Consumer-Owned Port 경유만 허용.
3. **`pub` 범위 최소화** — `pub(crate)` 기본, `pub`은 크레이트 경계에서만.
4. **빈 모듈 금지** — 생성하는 모든 파일에 최소한의 구조체 또는 함수를 포함한다.
5. **Consumer-Owned Port 원칙** — 새 feature 모듈이 다른 모듈의 기능을 필요로 하면 **자신의 crate 안에** outbound port trait을 정의하라. 예: `social` 모듈이 알림을 보내야 하면 `modules/social/src/port.rs`에 `SocialNotifier` trait을 정의하고, `modules/notification`은 그 trait을 구현하는 `NotificationAdapter`를 제공한다. `social`이 `notification::port`를 직접 import하는 순간 헥사고날이 깨진다. 출처: fit-pal `server/CLAUDE.md` §아키텍처 1번.
6. **Composition Root 단일화** — feature 모듈 자체는 DI 와이어링을 하지 않는다. 모든 `Arc<dyn Port>` 조립은 `apps/api/src/main.rs` 또는 `apps/worker/src/main.rs`에서만 이루어진다. 모듈이 다른 모듈의 구현체를 `new()`로 직접 생성하면 단일 Composition Root 원칙이 깨진다. 출처: fit-pal `server/CLAUDE.md` §아키텍처 3번.
7. **Domain event + outbox 패턴** — 새 feature가 다른 모듈에 알림/감사 로그/인덱스 동기화 같은 후처리를 필요로 하면 직접 호출 대신 **domain event** 발행 + **outbox 테이블** 기록으로 처리한다. feature 모듈의 `service.rs`는 트랜잭션 안에서 write + outbox insert를 원자적으로 실행하고, 외부 시스템 호출은 별도 워커가 outbox를 폴링하여 수행한다. 모듈 간 직접 호출 대신 이 패턴을 쓰면 Consumer-Owned Port 의존 방향이 깨지지 않는다. 출처: fit-pal `server/CLAUDE.md` §아키텍처 4번.
8. **Enumerate-before-Act (skill-design-guide §5.5)** — feature 모듈을 추가하기 전에 기존 `modules/*` (또는 `src/api/handlers/*`) 를 `Glob`/`Grep` 으로 전수 스캔하여 (a) 중복 이름, (b) 유사 네이밍 충돌, (c) 기존 shared port 존재 여부를 먼저 열거한다. 열거 결과를 체크리스트로 사용자에게 보이고 합의한 뒤에만 파일을 생성한다. 중복 모듈 생성은 Consumer-Owned Port 의존 그래프를 깨뜨린다.
9. **Sibling Consistency (skill-design-guide §8.8) — rust-init · rust-feature · rust-service · rust-api** — 4 스킬 모두 "Composition Root 단일화" + "Consumer-Owned Port" + "Domain event + outbox" + "포트에서 인프라 타입 제거" 4 원칙을 동일 문구·동일 출처(fit-pal `server/CLAUDE.md`) 로 유지한다. 한 스킬에서만 수정되면 드리프트가 발생하므로 카이젠 시 Grep 대조 필수.

# Process

## Gotchas

- **mod.rs 패턴과 파일명 패턴을 혼용하지 마라** — 프로젝트가 `feature/mod.rs` 스타일이면 일관되게 따르고, `feature.rs` + `feature/` 디렉토리 스타일이면 그것을 따르라. 혼용하면 `mod` 선언이 꼬인다.
- **상위 모듈에 `pub mod` 선언을 빠뜨리지 마라** — 파일을 생성만 하고 `lib.rs`나 부모 `mod.rs`에 `pub mod feature_name;`을 추가하지 않으면 컴파일러가 해당 모듈을 인식하지 못한다.
- **모듈 이름에 하이픈을 사용하지 마라** — Rust 모듈명은 snake_case만 허용한다. `user-auth`가 아니라 `user_auth`로 명명하라. 하이픈은 크레이트 이름에서만 사용 가능하다.
- **내부 타입을 무조건 `pub`으로 노출하지 마라** — hexagonal 아키텍처에서 domain 레이어의 내부 구현체는 `pub(crate)` 또는 `pub(super)`로 가시성을 제한하라. 모든 것을 `pub`으로 만들면 캡슐화가 무너진다.
- **순환 의존성을 만들지 마라** — `domain` → `infrastructure`로 의존하면 hexagonal 원칙이 깨진다. domain은 trait만 정의하고, infrastructure가 impl하는 구조를 유지하라. `use crate::infrastructure::*`가 domain에 있으면 잘못이다.
- **빈 모듈 파일을 생성하지 마라** — 최소한 모듈의 공개 인터페이스(trait, struct, enum)의 시그니처를 포함하라. 빈 파일은 빌드는 되지만 다음 단계에서 "뭘 구현해야 하지?" 상태가 된다.
- **feature 모듈 내부 구조를 프로젝트 컨벤션과 다르게 만들지 마라** — 기존 feature들이 `handler.rs`, `service.rs`, `repository.rs` 구조면 새 feature도 동일하게 따르라. 임의로 `controller.rs`, `logic.rs` 같은 이름을 쓰지 마라.
- **`#[cfg(feature = "...")]`와 Cargo feature를 혼동하지 마라** — 이 스킬의 "feature"는 도메인 기능 모듈이지, Cargo.toml의 `[features]` 섹션이 아니다. Cargo feature flag가 필요하면 별도로 명시하라.
- **에러 타입을 feature마다 독립 정의하지 마라** — 프로젝트에 공통 에러 타입(`AppError`, `DomainError`)이 있으면 그것을 확장하라. feature마다 별도 에러 enum을 만들면 핸들러에서 변환 보일러플레이트가 폭증한다.
- **테스트 모듈 위치를 잘못 잡지 마라** — 단위 테스트는 같은 파일 하단 `#[cfg(test)] mod tests`, 통합 테스트는 `tests/` 디렉토리에 배치하라. feature 모듈 안에 `tests/` 디렉토리를 만들면 cargo가 인식하지 못한다.

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`ARCH`, `IS_WORKSPACE`, `WORKSPACE_MEMBERS`)를 사용한다.

## 1. Feature 이름 확인

사용자에게 feature 이름을 확인한다 (snake_case).

## 2. 기존 패턴 분석

이미 존재하는 feature 모듈의 구조를 읽어 패턴을 파악한다:
- 디렉토리 구조
- mod.rs 등록 방식
- 네이밍 컨벤션

없으면 아키텍처 기본 패턴을 따른다.

## 3. 파일 생성

### ARCH = workspace_service

```text
crates/api/src/handlers/{feature}/
├── mod.rs          # pub mod 선언
├── handler.rs      # 핸들러 함수
└── dto.rs          # Request/Response 구조체

crates/domain/src/models/{feature}.rs    # 도메인 모델
crates/domain/src/services/{feature}.rs  # 서비스 로직
crates/domain/src/ports/{feature}.rs     # 서비스 trait 정의 (hexagonal)
crates/infra/src/adapters/{feature}.rs   # trait impl (hexagonal)
crates/infra/src/db/{feature}.rs         # DB 쿼리
```

### ARCH = modular

```text
src/api/handlers/{feature}/
├── mod.rs
├── handler.rs
└── dto.rs

src/domain/models/{feature}.rs
src/domain/services/{feature}.rs
src/domain/ports/{feature}.rs     # 서비스 trait 정의 (hexagonal)
src/infra/adapters/{feature}.rs   # trait impl (hexagonal)
src/infra/db/{feature}.rs
```

### ARCH = flat

```text
src/{feature}.rs    # 모든 로직을 한 파일에
```

## 4. mod.rs 등록

각 레이어의 mod.rs에 `pub mod {feature};`를 추가한다.

## 5. 라우터 연결 안내

> 라우터에 새 feature를 연결하세요:
> ```rust
> .nest("/{feature}", {feature}::router())
> ```

## After Creation

1. 생성/수정된 파일 목록 출력.
2. 다음 단계 안내:
   > - API 엔드포인트 추가: `/rust-api`
   > - DB 모델 추가: `/rust-model`
   > - 서비스 로직 추가: `/rust-service`

# References

- references/project-detection.md
- templates/rust-feature-mod.rs.template — feature 모듈 스캐폴딩 템플릿
