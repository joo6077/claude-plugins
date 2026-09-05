---
feature: "bambu-kit 표면 품질 회귀 수정"
slug: bambu-kit
created: "2026-09-05 21:49"
complexity: "복잡"
conditions: 24
status: active
owner_session: 80e6651a-4542-4964-92cf-b2b72d8c3a42
conditions_digest: sha256:bf74c39c2c17cd90
locked_at: "2026-09-05 21:49"
---

## 배경

사용자 실측: 생성 프로파일 적용 시 표면이 거칠고("지글거림") 압출이 듬성듬성 결손된다.
시스템 프로파일 전수 대조로 확인된 사실 — 생성 번들 42 개 중 31 개 process 에서
`outer_wall_speed` 를 25~35 mm/s 로 낮추면서 `internal_solid_infill_speed`(180~250) ·
`sparse_infill_speed` · `gap_infill_speed`(230~250) 를 **한 번도 건드리지 않았다.**
outer 대비 최대 속도 배율 중앙값 5.1x, 최대 9.2x.

구조적 원인은 `SKILL.md:713` 이다. 튜닝 허용 키 목록에 `outer_wall_speed` 와
`inner_wall_speed` 만 있어 인접 유량 키를 **정책상 건드릴 수 없었다.**

부수 결함 3 종: (a) filament 키를 소재 부모값(`0.4`/`1`) 대신 제네릭 nil-fallback(`0.8`/`2`)으로
덮어씀 (b) `seam_slope_gap` 을 Bambu 기본 `0` 대신 `10%` 로 40 번들에 적용 — 이 키는 툴팁상
"the inner wall and outer wall are shortened by a specified amount" 로 벽을 물리적으로 줄인다
(c) 근거 철회된 처방(`resolution 0.006-0.010`)이 SKILL.md 에 잔존.

프로세스 결함 2 종: (d) `SKILL.md:734` 건조 하드게이트가 "JSON 변경 없이 종료" 로 진단을 조기
종료시킨다 — 실측 실패 6 건 중 4 건이 건조로 종결됐고, 사용자가 건조를 명시 확인한 1 건에서만
실제 원인 2 개가 즉시 발견됐다 (e) 품질 우선 의도를 매 실행마다 재선언해야 한다.

## 리서치 소스

- Codex research A (2026-09-05, foreground read-only) — 습기 감별진단. Prusa KB / Orca wiki /
  Bambu filament guide 기반. 습기 특이 신호 vs 위치·시점 패턴 분리
- Codex research B (2026-09-05, foreground read-only) — 유량/압력 일관성. Orca ERS 문서가
  200→40 mm/s(5x) 전이만으로 압력 추종 실패 사례를 명시. Klipper PA 문서
- 설치된 Bambu Studio 02.06.00.51 바이너리 문자열 — `seam_slope_gap` / `seam_gap` 툴팁 확정
- 슬라이스된 3mf 최종 해석값 — `seam_slope_gap` 기본 `0`, `seam_gap` 기본 `15%`,
  `seam_slope_steps` 기본 `10`
- Codex research C — **사용량 한도로 미완.** 효과 크기 순위 · 팬 정책 · 영속화 설계는 미검증

## GAP 분석

- `SKILL.md:713` 튜닝 허용 키에 유량 인접 속도·가속 키 부재 → 속도 불연속의 구조적 원인
- `SKILL.md:736` / `failure-recipes.md:120` 이 참조하는 "기준값(§10.2)" 은 제네릭 nil-fallback
- `seam-recipes.md:86` 이 "커뮤니티 기본 10%" 를 기본값으로 승격. 같은 파일 138 행은 이미
  "gap 과다" 를 언더익스트루전 원인으로 지목 — 자기모순
- `seam-recipes.md:117`(PETG outer 50-70) 과 `SKILL.md:804`(outer 20-40) 정면 충돌
- Phase 4.3 게이트(`SKILL.md:931-962`)에 속도비·부모값 이탈 검사 없음

## 범위 경계

수정 대상은 `bambu-kit/skills/bambu-print-profile/` 하위 5 파일로 한정한다.
기존 42 개 생성 번들(`~/Hub/60_3D Print/Settings/`)은 **재생성하지 않는다** — 단
`SC-04` 회귀 증거용으로 1 개만 재생성해 비교한다.
온도·팬 키는 이번 스프린트에서 건드리지 않는다 (Codex C 미완으로 근거 부족).

커버리지 해소: SC-03 — `validate-plugin.py` 는 킷 전체를 검사하는 상위 명령이므로 개별 파일
열거 대신 킷 이름 하나로 측정한다.

## 회귀 게이트

`SC-04` 가 회귀 증거의 정본이다. 기존 번들 1 개를 재생성해 유량비를 before/after 로 비교하고,
after 가 임계 이하임을 수치로 보인다. 스킬 실행 검증(`DG-04`)을 먼저 통과한 뒤 수행한다.

## Skill

- [ ] SK-01: `SKILL.md` Phase 3 튜닝 허용 키 목록에 `internal_solid_infill_speed`, `sparse_infill_speed`, `gap_infill_speed`, `outer_wall_acceleration`, `default_acceleration` 5 키가 ✅ 허용 항목으로 존재한다 [exact, enumerated] (측정: 5 키 각각 `grep -c '<키명>' SKILL.md` >= 1 이고, 해당 줄이 ✅ 로 시작하는 허용 목록 블록 내부)
- [ ] SK-02: 유량비 게이트가 산식 `Q = line_width x layer_height x speed x flow_ratio` 와 3 단계 임계(<=3x 통과 / 3~5x 경고 / >5x FAIL)를 명시한다 [exact] (측정: `grep -c 'flow_ratio'` >= 1 및 임계 3 값 문자열 존재)
- [ ] SK-03: filament 키 override 전에 소재 부모 프로파일을 실제 조회하도록 요구하고, 제네릭 nil-fallback 값(`0.8` / `2`)을 소재값으로 쓰는 것을 금지한다고 명시한다 [structural] (측정: 부모 조회 절차 문단 + 금지 문구 각 1 건 이상)
- [ ] SK-04: 건조 하드게이트가 제거되어 `SKILL.md` 와 `references/failure-recipes.md` 양쪽에서 "JSON 변경 없이" 문구가 0 건이고, 관측 신호 기반 감별 분기로 대체되었다 [exact, enumerated] (측정: 두 파일 각각 `grep -c 'JSON 변경 없이'` == 0)
- [ ] SK-05: 품질 우선 선호 영속화 지점이 `bambu-kit/skills/bambu-print-profile/references/user-preferences.md` 경로로 명시되고, 저장 대상이 목표(품질 우선)이며 수단(저속)이 아님을 문서에 명시한다 [exact] (측정: 파일 존재 + SKILL.md 가 이 경로를 참조 + "저속" 을 목표로 저장하지 않는다는 문장 1 건 이상)

## Script

- [ ] SC-01: Phase 4.3 게이트가 생성 process JSON 을 파싱해 인접 feature 유량비를 계산하고 임계 초과 시 FAIL 을 출력한다 [goal] (측정: 게이트 명령을 9.2x 프로파일에 실행해 FAIL, 3x 이하 프로파일에 실행해 PASS) 음성 대조: 속도비 검사 블록을 삭제하면 9.2x 프로파일이 PASS 로 통과한다
- [ ] SC-02: Phase 4.3 게이트가 filament JSON 의 키가 소재 부모값에서 이탈했는지 검사하고 이탈 시 FAIL 을 출력한다 [goal] (측정: `filament_retraction_length: 0.8` + 부모 `0.4` 조합에 실행해 FAIL) 음성 대조: 이 검사를 삭제하면 부모 이탈 프로파일이 PASS 로 통과한다
- [ ] SC-03: `python3 scripts/validate-plugin.py bambu-kit` 가 exit 0 으로 통과한다 [goal] (측정: 명령 실행 후 `echo $?` == 0)
- [ ] SC-04: 기존 생성 번들 1 개를 수정된 스킬로 재생성했을 때, 인접 feature 최대 유량비가 재생성 전 값보다 낮고 3x 이하다 [goal] (측정: before/after 두 process JSON 을 부모 체인 해석 후 Q 비 계산, 두 수치를 응답에 인용) 음성 대조: SK-01 의 키 추가를 되돌리면 after 값이 before 와 동일해진다

## Error

- [ ] ER-01: 건조 미확인이 종료 사유가 아니라 confidence cap 으로 처리됨이 명시되어 있다 [structural] (측정: confidence cap 문구 1 건 이상 + 종료 분기 0 건)
- [ ] ER-02: 소재 부모 프로파일 조회에 실패했을 때의 폴백 동작이 정의되어 있고, 추측값 사용을 금지한다 [structural] (측정: 폴백 문단 1 건 이상)
- [ ] ER-03: 유량비 게이트가 FAIL 일 때 조용히 통과시키지 않고 사용자에게 제시하는 경로가 명시되어 있다 [structural] (측정: FAIL 시 사용자 제시 문구 1 건 이상)

## Architecture

- [ ] AR-01: `outer_wall_speed` 권장 범위의 문서 간 충돌이 해소되어, `references/surface-recipes.md` 와 `references/seam-recipes.md` 가 단일 SSOT 를 참조하거나 적용 조건이 명시되어 있다 [exact, enumerated] (측정: 두 파일에서 outer wall 속도 범위를 적은 줄을 모두 인용하고, 같은 소재에 서로 다른 범위를 제시하는 쌍이 0 건)
- [ ] AR-02: `seam_slope_gap` 기본값이 `0` 으로 환원되고, `seam_gap`(기본 `15%`)과 서로 다른 키임이 Bambu 툴팁 원문과 함께 명시되어 있다 [exact] (측정: `references/seam-recipes.md` 에서 gap 권장값 `10%` 를 기본으로 처방하는 행이 0 건, 두 키 구분 문단 1 건 이상)
- [ ] AR-03: 근거가 철회된 처방이 제거되어 `SKILL.md` 의 surface-first 공통값에서 `resolution 0.006-0.010` 및 `enable_arc_fitting` 끄기 권장이 0 건이다 [exact] (측정: 해당 문자열 `grep -c` == 0)
- [ ] AR-04: 변경 범위가 한정된다. Given: 계약 봉인 후 구현 완료 시점. `git diff --stat -- bambu-kit/` 결과 파일이 `SKILL.md`, `references/surface-recipes.md`, `references/seam-recipes.md`, `references/failure-recipes.md`, `references/bambu-fields-baseline.md`, `references/user-preferences.md` 6 개 이내이고 그 밖 경로 0 건이다 [exact, enumerated]

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 모든 코드 펜스에 언어 힌트가 있다 (```text, ```bash, ```yaml 등)
- [ ] AP-04: SKILL.md frontmatter 에 `name` 필드가 유지된다

## Reusability

- [ ] RE-01: 수치 정본을 `references/` 에 두고 `SKILL.md` 에 같은 수치를 중복 기재하지 않는다 (기존 SSOT 규약 준수)
- [ ] RE-02: 이미 존재하는 references 파일을 새로 만들지 않고 해당 섹션을 확장한다

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0 개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0 개 (제외 없음)
- [ ] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 로그에 에러/예외 0 개
- [ ] DG-04: 수정된 스킬을 실제 1 회 실행해 process + filament JSON 생성까지 에러 0 개
