---
name: rust-preflight
description: >
  Pre-commit quality gate. fmt → clippy → test → audit 순서로 실행하고
  결과를 요약 보고한다.
  "preflight", "프리플라이트", "커밋 전 검사", "pre-commit",
  "품질 게이트", "커밋 전에 확인" 같은 요청 시 사용한다.
  개별 프리미티브만 실행하려면 rust-run을 직접 사용한다.
argument-hint: ""
user-invocable: true
---

# Gotchas

1. **순서 변경 금지** — fmt → clippy → test → audit 순서는 고정이다. clippy 전에 fmt를 해야 포맷 워닝이 없다.
2. **fmt 실패 시 자동 적용** — `cargo fmt -- --check` 실패 시 `cargo fmt`를 적용한 후 재검사한다. 자동 수정 후 unstaged changes가 생기므로 `git add` 안내를 출력한다.
3. **audit은 non-blocking** — 외부 크레이트 취약점은 즉시 수정 불가할 수 있으므로 WARN으로만 표시한다.
4. **clippy 또는 test 실패 시 즉시 중단** — 이후 단계를 실행하지 않는다.

# Process

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$CARGO`, `IS_WORKSPACE`, `HAS_NEXTEST`) 를 사용한다.

## 1. fmt 검사

rust-run `fmt --check`를 실행한다.
- PASS → Step 2로
- FAIL → rust-run `fmt`를 실행하여 자동 적용 후 재검사. 재검사도 FAIL이면 중단.
  - 자동 적용 시: "`cargo fmt`가 파일을 수정했습니다. `git add`로 변경사항을 스테이징하세요." 안내.

## 2. clippy 검사

rust-run clippy를 실행한다.
- PASS → Step 3로
- FAIL → 에러 출력 후 중단. 이후 단계 skip.

## 3. test 실행

rust-run test를 실행한다.
- PASS → Step 4로
- FAIL → 에러 출력 후 중단. 이후 단계 skip.

## 4. audit 검사

rust-run audit를 실행한다.
- PASS → 정상
- FAIL → WARN으로 표시 (non-blocking). 취약점 목록 출력.

## 5. 리포트

## Preflight Report

| Step | Status | Details |
|------|--------|---------|
| fmt | {PASS/FAIL/FIXED} | {상세} |
| clippy | {PASS/FAIL/SKIP} | {상세} |
| test | {PASS/FAIL/SKIP} | {N tests passed / failed} |
| audit | {PASS/WARN/SKIP} | {N advisories} |

**Result:** {PASS / PASS (with warnings) / FAIL}

# References

- references/project-detection.md
