---
name: bambu-kaizen
description: >
  bambu-kit 스킬(bambu-print-profile) 품질을 references/ 4종과 실측 dogfood 결과 기준으로
  주기적으로 개선한다. 이 레포 개발용 스킬이며, bambu-kit 플러그인에 포함되지 않는다.
  harness-kaizen, flutter-kaizen, rust-kaizen과 동일한 패턴 (단, 도구형 1스킬 킷이라 단순화).
  "/bambu-kaizen", "Bambu 카이젠", "bambu-kit 개선", "삼프 스킬 개선" 같은 요청 시 트리거.
  단순 버그 수정이나 references 갱신에는 트리거하지 않는다 (references는 /bambu-research 사용).
argument-hint: ""
user-invocable: true
---

# Gotchas

1. **references 먼저, SKILL.md 다음** — 외부 소스 변동을 SKILL.md에 반영하기 전에 references에 먼저 흡수해야 한다. references → SKILL.md 순서를 절대 뒤집지 마라. references 부족 상태면 `/bambu-research`를 먼저 호출.
2. **실측 dogfood가 1순위 입력** — Codex 이론보다 사용자가 실제 출력해본 결과가 우선. 예: "회전체에서 random > aligned"는 Codex 이론과 반대였지만 실측이 맞았다 (seam-recipes.md Real-world findings). 이런 환류는 references와 SKILL.md 양쪽에 반영.
3. **사용자 명시 정책 깨뜨리지 마라** — `nozzle_temperature` 안 건드리는 정책 (2026-05-16 사용자 명시), `compatible_printers`는 H2S 고정, `wipe_on_loops`는 Bambu 부재(Orca 전용) 같은 검증된 제약은 카이젠 중에 풀어주지 마라.
4. **트리거 description은 신중히** — bambu-print-profile은 사용자 약어 "삼프", "Bambu 프로파일" 같은 한국어 트리거에 의존한다. description 수정 시 기존 트리거 키워드를 빼지 마라.
5. **silent skip 회피 체크리스트는 변경 금지** — Phase 4 끝의 "Gotcha 체크리스트 (생성 직후 자기 검증)" 7개 항목은 검증된 silent skip 회피 규칙(Codex run `a2a01770a87626167`)이다. 추가는 OK, 삭제 금지.
6. **카이젠 스킬은 .claude/skills/에만** — bambu-research, bambu-kaizen 자체를 bambu-kit 플러그인 안으로 옮기지 마라. 외부 사용자에게 노출되면 안 되는 레포 개발용 스킬이다.

# Process

## Step 1: 현재 상태 읽기

대상 surface (단일 스킬 + references):
- `bambu-kit/skills/bambu-print-profile/SKILL.md`
- `bambu-kit/skills/bambu-print-profile/references/bambu-fields-baseline.md`
- `bambu-kit/skills/bambu-print-profile/references/materials.md`
- `bambu-kit/skills/bambu-print-profile/references/seam-recipes.md`
- `bambu-kit/skills/bambu-print-profile/references/kaizen-sources.md`
- `bambu-kit/skills/bambu-print-profile/BACKLOG.md` (v2 큐)

추가 입력:
- `~/Hub/60_3D Print/Settings/<modelname>/notes.md` — 실측 케이스별 detail
- 메모리: `bambu_print_profile_skill.md`, `bambu_studio_json_import.md`, `3d_printing_setup.md`
- 사용자 피드백 (~/.harness/feedback/ 글로벌 + 세션 내 직접 피드백)

## Step 2: 격차 분석

다음 축으로 SKILL vs references vs 실측 정합성 점검:

| 축 | 점검 항목 |
|----|----------|
| **JSON 필드 정확성** | bambu-fields-baseline 변경분이 SKILL Phase 3 표/체크리스트에 반영됐는지 |
| **소재 매칭** | materials.md 신규/단종 SKU가 SKILL Phase 2 매핑 표에 반영됐는지 |
| **seam 전략** | seam-recipes.md Real-world findings가 SKILL Phase 3 결정 트리에 반영됐는지 |
| **silent skip 회피** | bambu-fields-baseline의 필수 메타필드가 Phase 4 체크리스트에 누락 없이 모두 들어있는지 |
| **fallback 체인** | MakerWorld Cloudflare / 메모리 자동 로드 / coupon test 가이드가 SKILL에 살아있는지 |
| **사용자 정책 보존** | nozzle_temperature/retraction/cooling 안 건드림 정책이 명시 유지되는지 |
| **트리거 정합성** | description의 트리거 키워드가 사용자 실사용 어휘 ("삼프", "MakerWorld 출력")를 커버하는지 |

## Step 3: 개선 적용

격차 항목별로 SKILL.md 또는 references 패치:
- Gotchas 추가 (실측 회귀 case → 한 줄 규칙)
- Phase 표/결정 트리 갱신
- v2 TODO에 새 큐 추가 (구현은 별도 사이클)

**한 번에 1~2개 surface만 수정.** 단일 스킬이라 변경 폭이 작지만 references 4종까지 합치면 5 surface — 한 사이클에 3개 이상 건드리지 마라.

## Step 4: 검증

- description 트리거 조건 유지 확인 (Gotcha 4)
- silent skip 체크리스트 7항목 보존 (Gotcha 5)
- references ↔ SKILL 경로 정합성 (`bambu-kit/skills/bambu-print-profile/references/...`)
- 사용자 정책 (nozzle_temperature 등) 미수정 확인 (Gotcha 3)

## Step 5: 검증 출력

다음 형식으로 보고:

```text
## bambu-kaizen 사이클 N (YYYY-MM-DD)

### 입력
- references 변경분: ...
- 실측 dogfood: ...
- 사용자 피드백: ...

### 격차
- [ ] ... (해소됨)
- [ ] ... (이번 사이클에서 다룸 vs 다음으로 이연)

### 적용
- SKILL.md: ...
- references/<file>.md: ...

### 다음 사이클 큐
- ...
```

## Step 6: 커밋

```text
chore(bambu-kaizen-cycle<N>): [개선 내용 요약]
```

# References

- `bambu-kit/skills/bambu-print-profile/SKILL.md` — 개선 대상 단일 스킬
- `bambu-kit/skills/bambu-print-profile/references/` — references 4종 (SSOT)
- `bambu-kit/skills/bambu-print-profile/BACKLOG.md` — v2 큐
- `~/Hub/60_3D Print/Settings/` — 실측 dogfood 케이스
- `~/.claude/codex-research-log/2026-05.md` — 초기 8 runs 로그
- `harness/docs/guides/skill-design-guide.md` — 스킬 설계 원칙 (단일 스킬도 동일 적용)
- `.claude/skills/bambu-research/SKILL.md` — references 갱신은 여기로 분리되어 있음
