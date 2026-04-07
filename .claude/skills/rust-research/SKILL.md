---
name: rust-research
description: >
  Rust 레퍼런스 소스를 크롤링/분석하여 docs/rust/ 문서를 갱신한다.
  이 레포 개발용 스킬이며, rust-kit 플러그인에 포함되지 않는다.
  "Rust 리서치", "rust research", "Rust 문서 갱신" 같은 요청 시 트리거.
argument-hint: "[category]"
user-invocable: true
---

# Gotchas

1. **기존 문서 구조 유지** — frontmatter, 섹션 순서를 바꾸지 않는다. 내용만 갱신.
2. **출처 없는 내용 금지** — 모든 원칙과 수치에 출처(URL 포함)를 명시한다.
3. **한 번에 전체 갱신 금지** — category 인자로 특정 카테고리만 갱신한다. 미지정 시 사용자에게 확인.

# Process

## Step 1: 대상 카테고리 결정

| 인자 | 대상 |
|------|------|
| `fundamentals` | docs/rust/fundamentals/ (6개 문서) |
| `web` | docs/rust/web/ (4개 문서) |
| `data` | docs/rust/data/ (3개 문서) |
| `protocols` | docs/rust/protocols/ (3개 문서) |
| `ops` | docs/rust/ops/ (3개 문서) |
| 미지정 | 사용자에게 확인 |

## Step 2: 리서치 실행

Codex 에이전트에 해당 카테고리의 최신 정보를 리서치 위임한다:
- 공식 문서 (docs.rs, Rust Book)
- 크레이트 최신 버전 및 변경사항
- 커뮤니티 추천 사항 (Rust subreddit, This Week in Rust)

## Step 3: 문서 갱신

리서치 결과를 기존 문서에 반영한다:
- `last_updated` 날짜 갱신
- 새 원칙/안티패턴 추가
- deprecated 내용 제거 또는 대체
- 수치 기준 업데이트
- 출처 URL 갱신

## Step 4: 커밋

갱신된 문서를 커밋한다.

# References

- docs/rust/ — 갱신 대상 문서
