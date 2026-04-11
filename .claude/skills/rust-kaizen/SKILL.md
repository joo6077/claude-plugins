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

## Step 6: Plugin Validation 결과 반영

이 카이젠 세션을 시작하기 전과 끝낼 때 모두 `scripts/validate-plugin.py` 를 실행하여 rust-kit 의 7가지 품질 카테고리 상태를 확인한다.

### 실행

```bash
# 세션 시작 시 현재 상태 파악
python3 scripts/validate-plugin.py rust-kit

# 자동 수정 가능한 항목 먼저 (V5 placeholders, V6 code-fence)
python3 scripts/validate-plugin.py rust-kit --fix --check=placeholders,code-fence

# 세션 종료 시 회귀 없음 확인
python3 scripts/validate-plugin.py rust-kit
```

### 우선순위 반영 규칙

- **ERROR** (V1~V7 중 실패): 카이젠 Step 3 (개선 우선순위) 의 "높음" 레벨에 자동 편입. 이 카이젠 세션에서 반드시 수정.
- **WARNING**: "중간" 레벨. V4 trigger 키워드 중복은 description 보강으로 처리.
- **PASS**: 해당 카테고리 skip.

### 통합 규칙

- `--fix` 자동 모드는 V5 placeholders 와 V6 code-fence 만 수정한다. 다른 체크는 수동 수정.
- V3 refs BROKEN 은 수동으로 링크 경로 확인 후 수정.
- V1 frontmatter 누락은 1줄 수정이라 즉시 처리.
- V7 plugin-json 불일치는 release.sh 흐름 문제라면 카이젠이 아닌 릴리스 스킬에서 다룬다.

# References

- docs/rust/ — 리서치 문서 (SSOT)
- rust-kit/skills/ — 개선 대상 스킬
- rust-kit/evals/evals.json — 테스트 케이스
- `harness/docs/guides/plugin-validation-guide.md` — 플러그인 품질 7 카테고리 기준 (SSOT)
- `scripts/validate-plugin.py` — 플러그인 검증 자동화 도구
