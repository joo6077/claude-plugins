---
name: bambu-research
description: >
  Bambu Lab / Bambu Studio / MakerWorld / scarf seam 관련 외부 소스를 폴링하여
  bambu-kit/skills/bambu-print-profile/references/ 4종 문서를 갱신한다.
  이 레포 개발용 스킬이며, bambu-kit 플러그인에 포함되지 않는다.
  "Bambu 리서치", "bambu research", "삼프 문서 갱신", "필라멘트 카탈로그 업데이트",
  "scarf seam 갱신" 같은 요청 시 트리거.
  단순 SKILL.md 텍스트 수정에는 트리거하지 않는다 — 실제 외부 소스 폴링이 필요할 때만.
argument-hint: "[category]"
user-invocable: true
---

# Gotchas

1. **출처 없는 갱신 금지** — 추가/변경한 모든 사실에 출처(URL + 접근 일자)를 명시한다. references는 Codex run 출처를 그대로 보존하고 있으므로 동일 포맷 유지.
2. **MakerWorld는 Cloudflare 차단 빈번** — WebFetch 1차 시도 후 실패하면 즉시 `codex-rescue` 에이전트에 위임 (research mode). 무한 retry 금지.
3. **버전 명시 필수** — Bambu Studio 버전, 필라멘트 SKU, OrcaSlicer 버전을 언급할 때 검증한 버전을 `[product@version]` 형태로 적는다. 버전 없는 추천은 6개월 후 outdated 된다.
4. **Reddit/YouTube는 보조 신호** — 공식 GitHub release / Bambu Blog / Discourse forum이 1순위. Reddit/YouTube는 "반복 출현 + 공식 소스 교차확인" 조건 시에만 references에 반영.
5. **카테고리별 단일 갱신** — 한 번에 4개 references를 모두 갱신하지 마라. category 인자로 1개씩 처리해야 회귀 추적이 쉽다. 미지정 시 사용자에게 확인.
6. **kaizen-sources.md 자체 변경은 보수적으로** — Top 10 우선순위는 가성비 trade-off가 들어간 결정이므로 새 소스를 추가하기 전에 폴링 안정성 (RSS/JSON 응답 200 + 스키마 stable) 검증 필수.

# Process

## Step 1: 대상 카테고리 결정

| 인자 | 갱신 대상 references | 폴링 소스 (kaizen-sources.md 매핑) |
|------|---------------------|--------------------------------|
| `studio` | bambu-fields-baseline.md | A. Bambu Studio 새 버전 릴리스 (GitHub releases, forum, blog) |
| `materials` | materials.md | B. Bambu Lab 신소재 출시/단종 (Shopify collections, filament-guide PDF) |
| `seam` | seam-recipes.md | E. Scarf seam / 신규 slicer 기능 (GitHub issues, OrcaSlicer wiki) |
| `sources` | kaizen-sources.md | meta — Top 10 소스 자체의 응답성/스키마 점검 |
| 미지정 | 사용자에게 확인 | — |

## Step 2: 폴링 실행

`bambu-kit/skills/bambu-print-profile/references/kaizen-sources.md`의 해당 카테고리 소스 표를 로드한다.

각 소스에 대해:
1. WebFetch 1차 시도 (RSS/JSON/HTML)
2. 실패 시 → `codex-rescue` 에이전트 위임 (research mode, `--read-only`, `MODE=research`)
3. 응답 200 + 콘텐츠 변경 감지 (ETag 또는 last commit hash 비교)

GitHub API는 unauth 60/h 한도 내에서 ETag/`If-None-Match` 사용으로 변동분만 가져온다.

## Step 3: 변경분 추출

새 정보 vs 기존 references 비교:
- **추가 항목**: 신규 SKU, 신규 Studio 필드, scarf 관련 새 GitHub issue
- **변경 항목**: deprecated 필드, 단종 SKU, 이름 변경
- **검증 항목**: 기존 권장사항이 여전히 유효한가 (예: PETG entire_loop stringing이 새 Studio 버전에서 해소됐는가)

## Step 4: references 갱신

해당 .md 파일에 반영:
- frontmatter나 상단 코멘트에 `Last updated: YYYY-MM-DD` + `Source: <폴링 출처>` 추가
- 새 항목은 기존 표/섹션 스키마를 그대로 따른다
- deprecated는 즉시 삭제하지 말고 "deprecated since vX.X (출처: ...)"로 표시 후 다음 사이클에 정리

## Step 5: 품질 확인

- 모든 새 항목에 인라인 출처 (URL + 접근 일자)
- 수치는 구체적 (온도, 속도, 시간)
- 기존 Codex run ID는 유지 (`a5afcf864d05cf3b7` 등) — 새 검증은 새 run ID 추가
- 사용자 명시 정책 (예: `nozzle_temperature` 안 건드림) 깨뜨리지 않는지 cross-check

## Step 6: 커밋

```text
chore(bambu-research-<category>): [갱신 내용 요약 + 폴링 일자]
```

# References

- `bambu-kit/skills/bambu-print-profile/references/kaizen-sources.md` — 폴링 소스 Top 10 + 카테고리별 매핑 (SSOT)
- `bambu-kit/skills/bambu-print-profile/references/bambu-fields-baseline.md` — studio 카테고리 갱신 대상
- `bambu-kit/skills/bambu-print-profile/references/materials.md` — materials 카테고리 갱신 대상
- `bambu-kit/skills/bambu-print-profile/references/seam-recipes.md` — seam 카테고리 갱신 대상
- `~/.claude/codex-research-log/2026-05.md` — 초기 8 runs 로그 (run ID 추적용)
