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
2. **workspace 순환 의존 금지** — domain 크레이트가 api나 infra를 의존하면 안 된다. 의존 방향: api → domain ← infra.
3. **`pub` 범위 최소화** — `pub(crate)` 기본, `pub`은 크레이트 경계에서만.
4. **빈 모듈 금지** — 생성하는 모든 파일에 최소한의 구조체 또는 함수를 포함한다.

# Process

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

```
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

```
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

```
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
