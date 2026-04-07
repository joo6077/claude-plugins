---
name: rust-audit
description: >
  Rust 코드를 원칙 기준으로 체계적으로 감사한다.
  카테고리별 PASS/FAIL 판정과 근거를 포함한 리포트를 생성한다.
  rust-reviewer 에이전트를 Agent 도구로 호출하여 독립 평가한다.
  "Rust 감사", "코드 검수", "rust audit", "코드 리뷰",
  "품질 검사" 같은 요청 시 트리거.
  빌드/테스트만 실행하려면 rust-run이나 rust-preflight를 사용한다.
argument-hint: "[quick|deep] [target-path]"
user-invocable: true
---

# Gotchas

1. **Rust 이외 도메인 평가 금지** — UI 디자인, 인프라 설정은 평가 대상이 아니다.
2. **추측성 FAIL 금지** — 실제 코드를 확인한 후 판정한다. "아마 문제가 있을 것"으로 FAIL하지 않는다.
3. **보안 카테고리 생략 금지** — 항상 Security 카테고리를 포함한다.
4. **deep 모드에서만 에이전트 호출** — quick 모드는 직접 검사한다.

# Process

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.

## 1. 대상 범위 결정

| 입력 | 범위 |
|------|------|
| 파일 경로 | 해당 파일만 |
| 디렉토리 경로 | 하위 전체 |
| 미지정 | `git diff --name-only` 기준 변경 파일 |

## 2. 모드 결정

| 모드 | 동작 |
|------|------|
| `quick` (기본) | 변경 파일만, 직접 검사, 경량 리포트 |
| `deep` | 전체 프로젝트, rust-reviewer 에이전트 위임, 상세 리포트 |

미지정 시: 변경 파일 5개 이하 → quick, 초과 → deep.

## 3-A. quick 모드 실행

references/audit-criteria.md를 읽고, 대상 파일을 직접 검사하여 카테고리별 PASS/FAIL 판정.

## 3-B. deep 모드 실행

rust-reviewer 에이전트를 Agent 도구로 호출:

```
subagent_type: "rust-kit:rust-reviewer"
prompt: |
  다음 파일을 Rust 원칙 기준으로 평가하라.
  감사 기준: rust-kit/skills/rust-audit/references/audit-criteria.md
  대상 파일: [목록]
```

## 4. 리포트 생성

| 카테고리 | 판정 | 근거 |
|----------|------|------|
| Ownership & Borrowing | {PASS/FAIL} | {파일:라인 + 설명} |
| Error Handling | {PASS/FAIL} | |
| Async | {PASS/FAIL} | |
| Security | {PASS/FAIL} | |
| Performance | {PASS/FAIL} | |
| Testing | {PASS/FAIL} | |
| API Design | {PASS/FAIL} | |

**최종 판정:** {APPROVE / REJECT}
**FAIL 수:** {N}개

# References

- references/audit-criteria.md — 카테고리별 PASS/FAIL 체크리스트
