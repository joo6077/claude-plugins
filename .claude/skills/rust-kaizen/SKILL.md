---
name: rust-kaizen
description: >
  rust-kit 스킬 품질을 docs/rust/ 리서치 문서 기준으로 주기적으로 개선한다.
  이 레포 개발용 스킬이며, rust-kit 플러그인에 포함되지 않는다.
  harness-kaizen, flutter-kaizen, design-kaizen과 동일한 패턴.
  "/rust-kaizen", "Rust 카이젠", "rust-kit 개선" 같은 요청 시 트리거.
  단순 버그 수정이나 기능 구현 요청에는 트리거하지 않는다.
argument-hint: ""
user-invocable: true
---

# Gotchas

1. **리서치 문서 없이 개선 금지** — docs/rust/ 문서를 먼저 읽고, 그 기준으로만 개선한다.
2. **스킬 삭제 금지** — 기존 스킬을 삭제하지 않는다. 개선만 한다.
3. **한 번에 1~2개 스킬만 개선** — 전체 스킬을 한 번에 수정하면 품질이 떨어진다.

# Process

## Step 1: 현황 분석

rust-kit/skills/ 디렉토리의 모든 SKILL.md를 읽고 현재 상태를 파악한다.

## Step 2: 리서치 문서 비교

docs/rust/ 리서치 문서와 스킬의 Gotchas, Process, 코드 예시를 비교한다.
차이가 있는 부분을 목록화한다.

## Step 3: 개선 우선순위

| 우선순위 | 기준 |
|----------|------|
| 높음 | 잘못된 정보, deprecated API 사용, 안티패턴 포함 |
| 중간 | 누락된 Gotchas, 불완전한 Process |
| 낮음 | 코드 예시 개선, 트리거 키워드 보완 |

## Step 4: 개선 실행

상위 1~2개 스킬을 개선한다. 각 개선마다:
1. 변경 전 내용
2. 변경 후 내용
3. 변경 근거 (리서치 문서 출처)

## Step 5: 검증

변경된 스킬의 evals를 확인하고, 필요하면 evals.json도 업데이트한다.

# References

- docs/rust/ — 리서치 문서 (SSOT)
- rust-kit/skills/ — 개선 대상 스킬
- rust-kit/evals/evals.json — 테스트 케이스
