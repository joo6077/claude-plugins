---
name: rust-build
description: >
  cargo build + clippy를 순서대로 실행한다.
  내부적으로 rust-run 스킬의 build + clippy를 호출하는 thin wrapper.
  "빌드", "build", "컴파일", "rust build" 같은 요청 시 사용한다.
  개별 프리미티브만 실행하려면 rust-run을 직접 사용한다.
argument-hint: ""
user-invocable: true
---

# Gotchas

1. **build 없이 clippy만 실행하지 않는다** — build가 선행되어야 clippy가 증분 분석을 제대로 수행한다.
2. **실패 시 즉시 중단** — build 실패 시 clippy를 실행하지 않는다.

# Process

## Gotchas

- **workspace 루트에서 단일 크레이트 명령을 실행하지 마라** — `cargo build`를 workspace 루트에서 실행하면 모든 멤버가 빌드된다. 특정 크레이트만 빌드하려면 `cargo build -p crate-name`을 사용하라.
- **clippy 경고를 무시하고 빌드 성공만 보고하지 마라** — `cargo clippy -- -D warnings`로 경고를 에러로 승격시켜야 CI와 동일한 기준이 된다. 빌드 성공 ≠ 품질 통과다.
- **증분 빌드 캐시가 깨졌을 때 재빌드를 시도하지 않으면 안 된다** — `cargo build`가 이상한 에러를 내면 `cargo clean` 후 재시도하라. proc-macro 변경, toolchain 업데이트, feature flag 변경 후 캐시 오염이 흔하다.
- **feature flag 조합을 확인하지 않으면 안 된다** — `cargo build --all-features`와 `cargo build --no-default-features`를 둘 다 실행하라. 특정 feature 조합에서만 컴파일 에러가 발생하는 경우가 많다.
- **cross-compilation 대상을 확인하지 않으면 안 된다** — `rust-toolchain.toml`에 targets가 명시되어 있으면 `cargo build --target`으로 해당 타겟도 빌드를 확인하라. x86에서 성공해도 aarch64에서 실패할 수 있다.
- **빌드 스크립트(build.rs)의 실패를 무시하지 마라** — `build.rs`에서 protobuf 컴파일, FFI 바인딩 생성 등이 실패하면 빌드는 성공처럼 보이지만 런타임에 크래시한다. stderr 출력을 반드시 확인하라.
- **RUSTFLAGS 환경변수를 임의로 설정하지 마라** — `-C target-cpu=native` 같은 플래그를 추가하면 캐시가 전부 무효화되고 전체 재빌드가 발생한다. 프로젝트의 `.cargo/config.toml`에 정의된 값만 사용하라.
- **cargo clippy를 cargo check 대용으로만 사용하지 마라** — clippy는 check보다 느리다. 빠른 컴파일 확인만 필요하면 `cargo check`를 먼저 실행하고, clippy는 품질 검증 단계에서 실행하라.
- **workspace의 resolver 버전을 무시하지 마라** — `resolver = "2"`가 아닌 workspace에서 feature unification 문제가 발생할 수 있다. Cargo.toml의 `[workspace]` 섹션에서 resolver를 확인하라.
- **빌드 결과를 파싱할 때 stderr와 stdout을 혼동하지 마라** — `cargo build`의 진단 메시지는 stderr로 출력된다. stdout만 캡처하면 에러 메시지를 놓친다. `--message-format=json`을 사용하면 구조화된 출력을 얻을 수 있다.

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$CARGO`, `IS_WORKSPACE`) 를 사용한다.

## 1. Build 실행

rust-run build를 실행한다. 실패 시 에러를 출력하고 중단.

## 2. Clippy 실행

rust-run clippy를 실행한다.

## 3. 결과 리포트

| Step | Status | Details |
|------|--------|---------|
| build | {PASS/FAIL} | {상세} |
| clippy | {PASS/FAIL} | {상세} |

# References

- references/project-detection.md
