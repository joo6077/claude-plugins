---
feature: "bambu-kit Surface-first 정책 풀 적용"
created: "2026-05-16 19:30"
revised: "2026-05-16 19:40 — qa-evaluator REJECT_WITH_REVISIONS 12건 반영 (v2)"
complexity: "중간"
conditions: 14
research_basis: "Codex run a25261e23b21252b2 (score 24/25)"
target_files:
  - "bambu-kit/skills/bambu-print-profile/SKILL.md"
  - "bambu-kit/skills/bambu-print-profile/references/seam-recipes.md"
  - "bambu-kit/skills/bambu-print-profile/references/bambu-fields-baseline.md"
  - "bambu-kit/skills/bambu-print-profile/references/surface-recipes.md (신규)"
  - "bambu-kit/skills/bambu-print-profile/BACKLOG.md"
language_policy: "조건 키워드는 한국어 우선. 영어 동의어 허용 시 측정식에 한·영 alternation 명시."
---

## Skill

- [ ] SK-01: `SKILL.md` Phase 3에 "Surface-first" 헤더가 존재하고, 회전체 default 결정 트리가 (1) spiral_mode 적용 가능성 체크 → (2) aligned/back + painted seam → (3) random fallback 의 3단계 순서로 명시. 결정 트리 포맷은 **번호 목록(1./2./3.), 표, 또는 코드 블록 다이어그램(예: `text` fenced) 중 하나**로 작성한다 [structural]
  - 측정:
    - `rg -n "Surface-first" bambu-kit/skills/bambu-print-profile/SKILL.md` ≥1건
    - `rg -n "spiral" SKILL.md` 동일 Phase 3 섹션 내 ≥1건
    - `rg -n "painted|aligned.*back|back.*aligned" SKILL.md` Phase 3 내 ≥1건
    - `rg -n "fallback|random" SKILL.md` Phase 3 내 ≥1건 (순서상 spiral 다음에 위치)
  - FAIL: "Surface-first" 헤더 없음, 또는 random이 회전체 1순위, 또는 결정 트리가 산문 한 문장으로만 기술

- [ ] SK-02: `SKILL.md` Phase 3에 형상별 결정 트리 6개가 모두 enumerate. 한국어 라벨 우선, 영어 동의어 허용 [exact, enumerated]
  - 6개 형상 (라벨 alternation):
    1. `회전체` (또는 `rotational|cylinder`)
    2. `박스|직육면체` (또는 `box|rectangular`)
    3. `유기적|곡면` (또는 `organic|curved`)
    4. `얇은 벽` (또는 `thin wall|thin-wall`)
    5. `평면.*top|top.*평면` (또는 `flat top`)
    6. `spiral vase|spiral mode` (영어 허용 — 슬라이서 용어)
  - 측정: 6개 패턴 각각 `rg -ni` SKILL.md 내 ≥1건
  - FAIL: 6개 중 하나라도 매칭 0건

- [ ] SK-03: `SKILL.md` Phase 3 또는 `surface-recipes.md`에 ironing 형상×소재 결정 트리 또는 표(table)가 존재하며, 8개 소재 각각이 동일한 표 또는 동일한 `###` 헤더 블록 내에서 ironing 적용/비적용 판정을 가진다 [structural, enumerated]
  - 8개 소재 (각 패턴):
    1. `PLA Basic`
    2. `PLA Matte`
    3. `PLA Silk`
    4. `PETG HF`
    5. `PA-?CF|PAHT-?CF` (PA-CF 또는 PAHT-CF)
    6. `\bPC\b` (workaround: word boundary)
    7. `ABS|ASA` (둘 다 또는 한 항목 묶음 허용)
    8. `\bTPU\b`
  - 측정: 8개 패턴 각각 `rg -ni` PASS + 같은 표 또는 같은 `### Ironing` (또는 동등) 블록 내에 모두 등장
  - FAIL: 8개 소재 중 하나의 ironing 판정 누락

## Reference

- [ ] RF-01: `references/bambu-fields-baseline.md`에 19개 surface 관련 필드가 추가되어 각 필드 라인 또는 표 행(table row) 또는 **3줄 이내 인접 라인**에 (a) 키 이름 (b) enum 또는 단위 (c) default 값 (d) 출처가 모두 명시. 출처는 **URL(`https://`로 시작) 또는 `file:line` 형식(`PrintConfig.cpp:N` / `*.json:N`) 또는 `source:` 접두 레이블 중 하나** [exact, enumerated]
  - 필드 19종: `ironing_type`, `ironing_flow`, `ironing_spacing`, `ironing_speed`, `ironing_inset`, `top_surface_pattern`, `top_surface_speed`, `top_surface_acceleration`, `top_solid_infill_flow_ratio`, `bridge_flow`, `bridge_speed`, `reduce_crossing_wall`, `avoid_crossing_wall_includes_support`, `resolution`, `spiral_mode`, `seam_placement_away_from_overhangs`, `seam_slope_steps`, `seam_slope_entire_loop`, `seam_slope_inner_walls`
  - 측정: 19개 키 각각 `rg -n "<키>" references/bambu-fields-baseline.md` PASS, 매칭 라인의 ±3줄 윈도우 내에 `mm|%|°C|true|false|0|1|"[a-z]"|배열` 단위/default 토큰 + URL/file:line/source 출처 토큰 동시 존재
  - FAIL: 19개 중 하나라도 4종 정보 (키/단위/default/출처) 불완비

- [ ] RF-02: `references/seam-recipes.md`의 회전체 default 정책이 **Auto-select 결정 트리 (spiral → painted → random fallback)** 로 전환되었고, 기존 Finding 1의 "random > aligned" 컨텍스트는 보존 (삭제 금지) [structural]
  - 측정 (4개 grep 모두 PASS):
    - `rg -n "Auto-select|결정 트리" seam-recipes.md` ≥1건
    - `rg -n "spiral" seam-recipes.md` 회전체 섹션 내 ≥1건
    - `rg -n "painted" seam-recipes.md` 회전체 섹션 내 ≥1건
    - `rg -n "fallback|분산" seam-recipes.md` ≥1건
    - `rg -n "Finding 1" seam-recipes.md` PASS (보존 확인)
  - FAIL: 기존 default 그대로, 또는 Finding 1 헤더 삭제

- [ ] RF-03: 신규 파일 `references/surface-recipes.md`가 존재하고, 6개 섹션 헤더가 각각 다음 키워드 패턴으로 매칭 [structural, enumerated]
  - 6개 섹션 (헤더 expected 키워드):
    1. `^## .*(Surface-first|개요|모드 소개)`
    2. `^## .*(형상별|결정 트리|Shape)`
    3. `^## .*(외벽|outer wall|매끈)`
    4. `^## .*(Top|Bottom|상·하)`
    5. `^## .*(Ironing|이로닝|아이러닝)`
    6. `^## .*(트레이드오프|Trade-?off|주의사항)`
  - 측정: 파일 존재 + 6개 패턴 각각 `rg -ni` PASS
  - FAIL: 파일은 존재하나 Ironing 또는 트레이드오프 섹션 누락

## Architecture

- [ ] AR-01: `SKILL.md`의 "작업 디렉토리 / 파일 구조" 섹션에 신규 `surface-recipes.md`가 등록되어 references는 4종 → 5종으로 갱신, 기존 4파일 모두 보존 [structural, enumerated]
  - 측정 (5개 grep 모두 PASS, SKILL.md 한 파일 내):
    - `rg -n "surface-recipes.md" SKILL.md` ≥1건 (신규)
    - `rg -n "bambu-fields-baseline.md" SKILL.md` ≥1건
    - `rg -n "materials.md" SKILL.md` ≥1건
    - `rg -n "seam-recipes.md" SKILL.md` ≥1건
    - `rg -n "kaizen-sources.md" SKILL.md` ≥1건
  - FAIL: 5파일 중 하나라도 SKILL.md 구조 트리에 미등록

- [ ] AR-02: Codex 리서치 run id `a25261e23b21252b2` 가 `surface-recipes.md` 또는 `seam-recipes.md` 새 섹션 헤더 또는 frontmatter에 명시 [exact]
  - 측정: `rg -n "a25261e23b21252b2" bambu-kit/skills/bambu-print-profile/references/surface-recipes.md bambu-kit/skills/bambu-print-profile/references/seam-recipes.md` ≥1건
  - FAIL: 두 파일 모두에서 매칭 0건

## Error

- [ ] ER-01: `BACKLOG.md`에 "Surface-first 후속 검증" 섹션이 추가, 최소 4개 항목 enumerate [structural, enumerated]
  - 4개 항목 (각각 별도 grep):
    1. `rg -n "precise z-seam" BACKLOG.md` ≥1건
    2. `rg -n "seam_slope" BACKLOG.md` ≥1건 (entire_loop / steps / inner_walls 중 하나 이상)
    3. `rg -ni "PLA Matte|PLA Silk|ASA|PAHT-?CF|TPU" BACKLOG.md` ≥3건 (소재 3종 이상 enumerate)
    4. `rg -ni "PETG.*HF" BACKLOG.md` ≥1건 + `rg -ni "lot|습도|건조 의존" BACKLOG.md` ≥1건
  - 측정: 4개 패턴 모두 PASS + 동일 `## Surface-first` (또는 동등) 섹션 헤더 내 등장
  - FAIL: 4개 중 하나라도 누락

- [ ] ER-02: `SKILL.md` Phase 3 또는 Phase 5에 PETG HF 건조 경고가 명시. **"AMS HT", "건조", "PETG"** 3 키워드가 모두 같은 단락(paragraph) 또는 같은 callout/blockquote/경고 블록 내에 등장 [structural]
  - 측정:
    - 동일 5줄 윈도우 내 3 키워드 모두 매칭: `rg -nU --multiline-dotall '(?s)PETG.{0,500}AMS HT.{0,500}건조|건조.{0,500}AMS HT.{0,500}PETG|AMS HT.{0,500}PETG.{0,500}건조' SKILL.md` ≥1건 (정규식 순서 alternation)
    - 또는 단순 fallback: `rg -n -B2 -A2 "PETG" SKILL.md | rg "AMS HT"` + `rg -n -B2 -A2 "PETG" SKILL.md | rg "건조"` 둘 다 PASS
  - FAIL: 3 키워드 중 하나가 다른 단락에만 존재, 또는 다른 소재(PA-CF)로 잘못 매핑

## Script

- [ ] SC-00: N/A — release.sh / marketplace.json / plugin.json 변경 없음. 본 스프린트는 문서 정책 변경 한정.

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 신규 surface-recipes.md 및 변경 파일의 모든 code fence에 언어 힌트 명시 [exact]
  - 측정: `rg -n '^[[:space:]]*```[[:space:]]*$' bambu-kit/skills/bambu-print-profile/` → 0건
- [ ] AP-04: SKILL.md frontmatter `name: bambu-print-profile` 필드 보존 [exact]
  - 측정: `head -10 bambu-kit/skills/bambu-print-profile/SKILL.md | grep -c "^name: bambu-print-profile"` = 1

## Reusability

- [ ] RE-01: 신규 `surface-recipes.md`가 `bambu-kit/skills/bambu-print-profile/references/` 디렉토리에 위치하며, private/internal/_hidden 같은 격리 경로에 두지 않았다 [exact]
  - 측정: `test -f bambu-kit/skills/bambu-print-profile/references/surface-recipes.md` PASS + `find bambu-kit/skills/bambu-print-profile -path "*private*" -o -path "*_internal*" -o -path "*_hidden*" -name "surface-recipes.md"` = 0건
  - FAIL: 격리 경로 또는 references 외 위치에 생성

- [ ] RE-02: `SKILL.md`가 ironing 정책 본문을 인라인으로 박지 않고 `surface-recipes.md`를 참조하는 링크 또는 명시적 위임 문구를 포함 [structural]
  - 측정:
    - `rg -c "ironing" bambu-kit/skills/bambu-print-profile/SKILL.md` ≤ 10건 (인라인 본문 박지 않음)
    - `rg -n "surface-recipes" bambu-kit/skills/bambu-print-profile/SKILL.md` ≥1건 (위임/참조)
  - FAIL: SKILL.md 내 ironing 정책 표가 10줄 이상 인라인 박힘, 또는 surface-recipes.md 참조 0건

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` — N/A, 셸 스크립트 변경 없음
- [ ] DG-02: N/A — markdownlint 미적용 프로젝트, V6 코드펜스 검사는 DG-03(validate-plugin)로 흡수
- [ ] DG-03: `python3 scripts/validate-plugin.py bambu-kit` PASS (V1 frontmatter, V6 code-fence 포함)
- [ ] DG-04: 실제 앱 구동 검증 — N/A, 스킬 문서 변경
