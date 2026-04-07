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
