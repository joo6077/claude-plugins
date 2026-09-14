# Sprint Feedback
Feature: bambu-kit 슬라이서 축 신설 · seam 정책 실측 반영
Evaluated: 2026-09-14 11:40
Verdict: APPROVE
Iteration: 2

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-bambu-kit-slicer-axis-and-seam-policy.md
- sha256: 0c0746b96cc8e6bce7f0ef1fb9eea605fa5e825fb6509573af31472c7af6ad3a
- status: active
- slug: bambu-kit-slicer-axis-and-seam-policy
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (호출자가 절대경로 지정 · `test -f` 확인함)
- legacy_contract_used: false
- seal_status: SEAL_OK (recorded=209ae5150c40cb31 · actual=209ae5150c40cb31)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (평가 전후 sha256·status·digest 동일)
- status_transition: active -> done

## 계약 파싱 범위 (Step 1.2)
- 조건 섹션 7 종 · 서술 섹션 5 종(배경·리서치 소스·GAP 분석·범위 경계·회귀 게이트)
- 파싱된 조건 23 · frontmatter `conditions: 23` — 일치

## Amendments
- amendments: 2 (AM-01 · AM-02) + 진행기록 2 절
- 계약 본문 변경: **0** (SEAL_OK 가 증명)
- PASS 근거 가능: 0 (어떤 조건도 amendment 를 근거로 PASS 하지 않았다)
- PASS 근거 불가: 1 — **사용자 확인 필요**
  - [relaxing · unanchored · anchor:none] AM-01 이 AR-03 의 enumerated 대상에서
    `bambu-print-profile.html` 을 빼고 `bambu-fields-baseline.html` 로 바꿔치웠다.
    오라클 축 계산: measured_removed=1(bambu-print-profile) · added=1 → **relaxing**
    (떨어진 파일을 측정 집합에서 제거하면 실패가 통과로 바뀐다).
    → 나는 이 대체표를 쓰지 않고 **원 조건의 3 파일 그대로** 판정했다. 결과는 PASS 다.
- AM-02 는 구현 기록이며 조건 문구를 바꾸지 않는다 (direction 판정 대상 아님).

## User Correction Audit
- correction_log_status: available (`~/.claude/logs/claude-plugins/2026-09.md`)
- unreflected_corrections: 0
  - 스프린트 구간(2026-09-13 11:20~) 사용자 발언은 진행 지시("순서대로 진행해",
    "다음 세션에서 고칠 목록으로 진행해")와 reflect-kit 분석 프롬프트뿐이다.
  - 이어작업 교정 2 건(슬라이서 «양쪽 다» 지정 · detect-docs-drift 승인)은 사이드카에 반영돼 있다.
- verdict 영향: 없음 (표면화 전용 · 미검증 카운터 비합산)

## Results

### Skill (6/6)
- [x] SK-01 — PASS
  - 근거 [L3]: 배제 문구 `grep -c` = **0 / 0**, `grep -c 'OrcaSlicer'` = **1 / 9**
    (`bambu-kit/.claude-plugin/plugin.json` / `SKILL.md`). enumerated 2 대상 전수.
    의미 확인: plugin.json:3 "슬라이서 판별(Bambu Studio / OrcaSlicer)",
    SKILL.md:3 "Bambu Studio 와 OrcaSlicer 를 모두 다루며", SKILL.md:9 "양쪽을 지원".
- [x] SK-02 — PASS
  - 근거 [L3]: `bambu-fields-baseline.md:350` §11 헤더 1 건. §11.2 오르카 전용 **7 행** ·
    §11.3 뱀부 전용 **6 행** (기준 각 >=3).
  - **독립 재측정(평가자 직접 · 사용자 방법론 지시 준수 — 바이너리·프로파일 둘 다)**:
    `strings -a` 뱀부 770,832 줄 / 오르카 753,573 줄. 24 키 전수 대조 —
    §11.2 6 키 전부 bambu=0/orca=2, §11.3 9 키 전부 bambu=2/orca=0, §11.2a 8 키 전부 2/2.
    프로파일 집계도 재현: `filament_scarf_*` 오르카 89·66·67·54, `wall_sequence` 0/303,
    `reduce_infill_retraction` 0/733, `scarf_joint_speed` 0/187 — 문서 수치와 전부 일치.
    대조군 2 종(`percise_outer_wall` 오타 · `jackson_totally_fake_key`) 양쪽 0/0
    → 이 측정이 아무 문자열이나 잡는 게 아님을 확인(공허한 0 아님).
- [x] SK-03 — PASS
  - 근거 [L3]: `grep -c 'seam_slope_conditional'` = **4** (>=1). §6.5.4(`seam-recipes.md:277-287`)
    안에 `0%` **2 건** — 실측표 `1 → 0%` / `0 → 98.2%` + "기본값이 1 이므로 명시적으로 0 을 쓰지
    않으면 경사 설정 전체가 무효" 서술.
- [x] SK-04 — PASS
  - 근거 [L3]: 클램프 서술 `min(설정값, 루프 둘레)` 1 건(`seam-recipes.md:253`, GCode.cpp v2.4.2 출처 병기),
    규칙 문장 "**규칙: 경사 길이를 루프 둘레보다 작게 잡아라.**" 1 건(`:261`).
    실측 임계표(0.5/1.5/3/10 → 360% 비율) 동반.
- [x] SK-05 — PASS
  - 근거 [L3]: §6.5.2(`seam-recipes.md:237-249`) 근거 문단 1 건 + 출처 URL 1 건
    (OrcaSlicer PR 3839 코멘트 "random is a disaster, blobs and strings galore").
    수치(78%→11%)를 먼저 제시한 뒤 그럼에도 기본 처방으로 쓰지 않는 이유를 댔다.
- [x] SK-06 — PASS
  - 근거 [L3]: `surface-recipes.md:145` 계산식 한 줄에 `outer_wall_line_width` ·
    `inner_wall_line_width` · `wall_loops` 동시 사용(매치 1 건).
    `arachne` 전환 조건 `:158` ("< 벽 예산, >= 외벽 2겹(0.84 mm) → `wall_generator` 를 `arachne` 로").
    실측 대조표(classic 갭필 16,123 vs arachne 0) 동반.

### Script (4/4)
- [x] SC-01 — PASS
  - 근거 [L3]: `SKILL.md:1368` `KINDS = ("process","filament","machine")`,
    스코프 불일치 오류 경로 `SKILL.md:1462` `errs.append("키 스코프 불일치 …")`.
  - **계약의 `음성 대조:` 절을 평가자가 직접 실행** (SKILL.md:1581-1602 스니펫 원문 그대로,
    **bash 2 회 · zsh 2 회** — 총 4 회 전부 동일 출력):
    - 게이트 추출: SKILL.md 1331~1550 → 218 줄 (손으로 베끼지 않고 `sed` 로 추출 = 결합 1)
    - 검사 유지: `FAIL … 키 스코프 불일치 retraction_minimum_travel … machine 에만 실재`
      / `RESULT: FAIL` / `exit=1`
    - machine 분기 제거(변이 적용 확인 `grep -c` = 1): `OK … keys=17` +
      `[미검증] retraction_minimum_travel … 없는 키` / `RESULT: PASS` / `exit=0`
    - enum 제거: `RESULT: PASS` / `exit=0`
    → 계약이 적은 "machine 분기를 지우면 그 픽스처가 통과로 바뀐다" 가 **실행으로 확인됨.**
      FAIL 이 사라지고 `[미검증]` 으로 **강등**되는 것까지 재현.
- [x] SC-02 — PASS
  - 근거 [L3]: `SKILL.md:1622-1629`. enum 조용한 강등 설명(`seam_slope_type='hole'` →
    exit 0 · 경고 0 으로 스카프 소멸) + "가짜 키를 하나 넣어 슬라이스한 뒤 G-code 설정
    트레일러에서 그 키가 사라지는지 보면" 소멸 확인 절차 1 건. 픽스처 절차는 `:1564-1601`.
- [x] SC-03 — PASS
  - 근거 [L3]: `python3 scripts/validate-plugin.py bambu-kit` → V1~V8 전부 OK, `Exit: 0`,
    `echo $?` = **0**. 활성화 확인: V1 1 skill · V4 6 keywords · V6 0 bare(대상 0 아님).
- [x] SC-04 — PASS
  - 근거 [L2/L3]: `git status --porcelain -- bambu-kit/evals/gate-fixtures` 신규(`??`) **2 건**
    (`process-machine-scope-key.json` · `process-seam-slope-type-invalid.json`). 기준 >=2.
    enumerated 2 대상 전수 내용 확인 — 각각 목표 위반 1 개만 담고(17 키 / 19 키) 나머지 정상값.
    SC-01 음성 대조 실행에서 FAIL 각 1 건만 낸 것으로 교차 확인.

### Error (2/2)
- [x] ER-01 — PASS
  - 근거 [L3]: `SKILL.md:696-730` Phase 1.95. 폴백 정의 `:721`("둘 다 미설치 → `[미검증]` 표시 +
    Bambu Studio 키셋으로 생성, Phase 4.3 이 판정 불가로 보고") 1 건,
    금지 문장 `:730`("**추측 금지.** 파일 확장자·모델 출처·과거 대화로 슬라이서를 유추하지 마라") 1 건.
    `:718` 에도 "추측으로 덮어쓰지 마라".
- [x] ER-02 — PASS
  - 근거 [L3]: `SKILL.md:1349`(미전달) · `:1352`(오타값) · `:1355`(설치본 경로 없음) ·
    `:1460`(스코프 미상 키) · `:1464`(시스템 프로파일 경로 없음) — `[미검증]` 분기 5 건.
  - 실행 확인: 내가 돌린 오르카 산출물 검사에서 `[미검증]` 8 건이 실제로 출력됐다
    (`brim_type` · `staggered_inner_seams` · `wipe_before_external_loop` · `scarf_joint_speed` ·
    `scarf_joint_flow_ratio`). 다른 슬라이서로 폴백하지 않는다.

### Architecture (3/3)
- [x] AR-01 — PASS
  - 근거 [L3]: 계약이 지정한 오라클 `git status --porcelain -- bambu-kit docs/bambu-kit`
    실행 결과 **12 건**, 전부 열거 목록 이내 —
    SKILL.md 1 · references 3 · plugin.json 1 · bambu-kit/README.md 1 ·
    gate-fixtures 하위 2 · docs/bambu-kit 하위 4. 목록 밖 **0 건**.
    측정 상태: HEAD 대비 working tree (계약 Given "구현 완료 시점" 그대로).
  - 평가 중 작업트리 무변형: 평가 전 26 항목 → 평가 후 26 항목. 내 변이본은 전부
    scratchpad·`/tmp` 에만 있고 레포 파일을 하나도 건드리지 않았다.
  - **계약 결함 기록(판정에는 영향 없음)**: 이 조건의 pathspec 이 열거 목록과 동일 범위라
    "그 밖 0 건" 절이 두 디렉토리 밖을 구조적으로 볼 수 없다. 아래 3 건이 오라클 사각에 있다 —
    `scripts/detect-docs-drift.py`(사용자 승인 · 구현자 자진 신고) ·
    `.claude/skills/kaizen-orchestrator/SKILL.md`(AR-02 변경이 sync-orchestrator 로 전파된 1 줄) ·
    `.noenum` · `.nomachine`(0 바이트 찌꺼기).
    다만 **pathspec 을 넓히면 AR-01 과 AR-02 가 정면 충돌한다** — AR-02 가 반드시 바꾸라고
    요구하는 `marketplace.json` · 루트 `README.md` · `CLAUDE.md` 3 파일이 AR-01 열거 목록에 없다.
    즉 pathspec 이 두 조건을 양립시키는 장치이므로, 문자 그대로 해석하는 것이 유일하게
    일관된 판정이다. 범위 확대는 사용자 권한이다.
- [x] AR-02 — PASS
  - 근거 [L3]: `grep -c 'Orca'` = marketplace.json **1** · 루트 README.md **1** · CLAUDE.md **1**
    (기준 >=1). enumerated 3 대상 전수.
    diff 확인 — 세 파일 모두 "슬라이서 판별(Bambu Studio / OrcaSlicer)" 이 **신규 추가된 줄**이다
    (기존 텍스트로 통과한 게 아니다).
- [x] AR-03 — PASS **(1 회차 FAIL → 이번 회차 조치 확인)**
  - 근거 [L3], enumerated 3 대상 전수:

    | 대상 | 계약 측정 `grep -c 'Orca'` | 소스 신설분 반영 (L3) |
    | --- | --- | --- |
    | `bambu-print-profile.html` | **3** (1 회차 2) | Phase 1.95 카드 **2** · `TARGET_SLICER` **2** · `음성 대조` **1** |
    | `seam-recipes.html` | **15** | `seam_slope_conditional` **2** |
    | `surface-recipes.html` | **7** | `outer_wall_line_width` **1** |

  - **1 회차 FAIL 사유가 해소됐다.** `:151` 의 배제 문장이 제거되고
    "슬라이서는 Bambu Studio 와 OrcaSlicer 양쪽을 다룬다 · 어느 쪽으로 생성할지는 Phase 1.95 가
    확정한다" 로 교체됐다. `:170` 은 "다른 프린터 언급(X1C, P1S, A1) 또는 PrusaSlicer —
    **OrcaSlicer 는 이제 트리거한다**" 로 뒤집혔다.
    `docs/bambu-kit/` 전체에서 배제 문장 잔존 **0 건** (`grep -rn` 확인).
  - diff 를 직접 읽어 소스 대조: Phase 1.95 카드의 4 갈래 판정표가 `SKILL.md:716-721` 과 행 단위로
    일치하고, 환경변수 전달 문단이 `:726-728` 과, 추측 금지가 `:730` 과, 음성 대조 콜아웃이
    `:1559-1620` 과 일치한다. 파생 페이지가 소스를 실제로 반영한다 (49 insertions / 5 deletions).
  - 측정 판별력 보완: 1 회차가 지적한 대로 `grep -c 'Orca'` 자체는 반증 불가능하므로,
    **소스 신설 토큰 4 종**(`Phase 1.95` · `TARGET_SLICER` · `음성 대조` · 배제 문장 0 건)으로
    재판정했다. 네 값 모두 1 회차 baseline 0 에서 올라왔으므로 이 측정은 판별력이 있다.

### Anti-patterns (2/2)
- [x] AP-03 — PASS
  - 근거 [L3]: `python3 scripts/validate-plugin.py --check=code-fence` **exit 0**.
    bambu-kit 개별 실행도 `V6 code-fence 0 bare — OK`. 대상 0 개가 아니라 실제 통과.
- [x] AP-04 — PASS
  - 근거 [L2/L3]: `SKILL.md:2` `name: bambu-print-profile` — frontmatter 안에 존재.
    validate-plugin `V1 frontmatter 1 skill — OK` 로 교차 확인.
- 참고(계약 미열거 · project.yaml 항목): 변경/신규 16 파일 대상
  AP-01 `hardcoded.*version` **0 건** · AP-02 `git push.*--force` **0 건**.
  공허한 0 아님 확인 — 같은 패턴이 레포 전체에서는 각각 13 · 19 파일에 매치한다. verdict 영향 없음.

### Reusability (2/2)
- [x] RE-01 — PASS
  - 근거 [L3]: 신규 산출물은 픽스처 2 개뿐이고 기존 7 개와 같은 공유 위치
    `bambu-kit/evals/gate-fixtures/` 에 놓였다. 게이트 스크립트는 종전대로 SKILL.md 안에 있어
    새로 private 화한 것이 없다. 이번 회차 신규 코드인 detect-docs-drift 매핑도
    공유 스크립트(`scripts/`)에 추가됐지 별도 사본을 만들지 않았다.
- [x] RE-02 — PASS
  - 근거 [L2/L3]: `git status --porcelain -- .../references/` 신규(`??`) **0 건**.
    세 파일 모두 `M` 이고 각각 기존 파일에 §11 / §6.5 / §2.8 을 **덧붙인** 형태다.

### Diagnostics (4/4)
- [x] DG-01 — PASS
  - 근거 [L3]: `bash -n scripts/release.sh` 출력 0 줄 · exit 0.
    범위 확인: 이번 스프린트에서 변경된 `.sh` 파일 0 개.
- [x] DG-02 — PASS `[정적]`
  - 1 차 도구(편집기 진단 패널)는 이 환경에서 조회 불가 (`project.yaml: runtime_inspection.mcp_server: null`).
  - 정적 대체를 수행했고 결과가 비공허하다: 변경/신규 파일 전수 파싱 —
    JSON 5/5 OK · Python 1/1 compile OK · HTML 4/4 parse OK.
    레포 게이트 10 종 전수 exit 0 — validate-plugin(14 플러그인) · sync-docs --check-only ·
    sync-evals · sync-orchestrator(13 plugins) · check-docs-links(176/176 등록) ·
    check-stale-values · check-contrast-claims · validate-doc-contracts ·
    run-evals(**106 passed, 0 failed**) · check-docs-a11y(docs/bambu-kit **7/7 PASS**).
  - 활성화 확인: 대상 수가 0 이 아니다(14 · 13 · 176 · 106 · 7).
- [x] DG-03 — PASS
  - 근거 [L3]: `bash scripts/release.sh 2>&1 || true` → usage 안내만 출력.
    `error|exception|traceback|fatal` 매치 **0 건**.
- [x] DG-04 — PASS **(1 회차 FAIL → 이번 회차 조치 확인)**
  - 조건: 수정된 스킬을 **실제 1 회 실행**해 process + filament JSON 생성까지 에러 0 개
  - **산출물 (평가자가 직접 수집)**: `/Users/jackson/Hub/60_3D Print/Settings/
    ams-2-pro-lattice-dry-pods/dogfood-2026-09-14/` — process **4** · filament **2** ·
    zip 2 · notes.md. 전부 2026-09-14 11:19~11:20 생성으로 **계약 봉인(09-13 11:44) 이후**다.
  - **게이트 재현 (평가자가 레포 SKILL.md 에서 sed 로 추출해 직접 실행)**:

    ```text
    TARGET_SLICER=bambu → OK×3  RESULT: PASS  exit=0   (WARN 1 · 유량비 3.8x gap_infill_speed)
    TARGET_SLICER=orca  → OK×3  RESULT: PASS  exit=0   ([미검증] 8 · BBL 트리에 없는 오르카 전용 키)
    ```

    `WARN` 은 `allok` 을 내리지 않으며 `[미검증]` 은 ER-02 가 요구한 정직 보고다. **에러 0 건.**
  - **"수정된 스킬" 판정 — 구현자 판단이 맞다.** 근거 3 가지:
    1. 설치본 캐시 `~/.claude/plugins/cache/joo6077-plugins/bambu-kit/0.9.0/…/SKILL.md` 는
       sha `639f5bac6794dbe1` · 1,690 줄 · `TARGET_SLICER` **0** · `Phase 1.95` **0** ·
       `음성 대조` **0** · `_target_slicer` **0`. 레포는 sha `137ddda83e032fa1` · 1,838 줄 ·
       15 / 4 / 1 / 1. **캐시본은 이번 스프린트 변경을 하나도 담고 있지 않다.**
       Skill 도구로 호출했다면 «수정된» 스킬이 아니라 **수정 전 스킬**을 돌린 것이 된다 —
       조건을 문자 그대로 읽으면 그쪽이 오히려 불충족이다.
    2. **역추적 증거**: 산출물 6/6 에 `_target_slicer` 가 기록돼 있고 값이 파일별로
       `bambu` / `orca` 로 갈린다. 이 키를 쓰라는 지시는 레포 SKILL.md:724 에만 있고
       캐시본에는 0 건이다 — 캐시본을 따라서는 나올 수 없는 산출물이다.
    3. **슬라이서 분기가 실제로 작동**: 오르카 산출물에만 오르카 전용 키가 들어 있다
       (CONTAINER `staggered_inner_seams` · `wipe_before_external_loop`,
       FUNNEL 은 거기에 `scarf_joint_speed` · `scarf_joint_flow_ratio` 추가).
       뱀부 전용 키 차집합은 0 이다. Phase 1.95 → Phase 3 라우팅이 장식이 아니다.
    - 따라서 **레포 SKILL.md 를 정본으로 실행한 것이 이 조건의 유일한 충족 경로**다.
  - **게이트 판별력 대조(공허한 PASS 아님)**: 직전 세션 산출물
    `…/orca/… ORCA-SEAM-V2.json`(09-13 10:10)을 같은 게이트에 넣으면
    `FAIL … _geometry_class 가 없다` + `FAIL … 유량비 11.5x` / `RESULT: FAIL` / `exit=1`.
    같은 오라클이 옛 산출물은 떨어뜨리고 새 산출물은 통과시킨다 → 반증 가능한 측정이다.
    (읽기 전용 실행 · 해당 파일 mtime 09-13 10:10 그대로 무변형 확인)
  - Phase 커버리지는 `notes.md` 에 측정값과 함께 기록돼 있고 게이트 출력과 교차 일치한다
    (Container thin 루프 최소 둘레 5.31mm → 스카프 off / Funnel planar 91.72mm → 스카프 on,
    최대 유량비 2.86x 주장 ↔ 게이트가 FUNNEL 에 WARN 을 안 냄 = 3.0x 이하).

## Unverifiable Summary
- invalid_evidence: **0**
- env_gaps: **0**
- verified_coverage: (23 - 0) / 23 = **1.00** (임계 0.60)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상

## Discrimination (규칙 12 적용 조건)
- 적용 조건: SC-01 (입력 검증 게이트) · DG-04 (실행 산출물로 판정)
- 결합 확인: 두 조건 모두 측정이 계약이 지목한 구현을 **직접 경유**한다 —
  게이트를 손으로 베끼지 않고 `sed -n "$((A+1)),$((B-1))p" SKILL.md` 로 추출해 실행했다.
  테스트가 로직을 독립 재작성한 부분은 없다 (결합 1).
- 음성 대조: 계약 SC-01 에 `음성 대조:` 절 **기재 있음**. 실행 변형 수행 —
  안전조건 3 개 충족(변형 대상이 `/tmp`·scratchpad 사본이라 레포 무변형 · 변형 지점 2 곳 ·
  평가 후 `git status` 26 항목으로 시작 시점과 동일).
  결과: `machine` 분기 제거 → FAIL 소멸·PASS 전환, `seam_slope_type` enum 제거 → 동일.
  **두 검사 모두 오라클로 살아 있음이 증명됨.**
- DG-04 음성 대조: 계약에 기재 없으나(조건 결함 아님 — 산출물 조건이다) 평가자가
  직전 세션 산출물로 대조 실행 → `RESULT: FAIL exit=1`. 게이트가 무엇이든 통과시키지 않는다.

## Evidence Validity
- 검사 대상 증거: 23 조건 + 보조 측정 18 건
- 무효 판정: **0 건**
  - 1 회차에 무효였던 AR-03 측정문(`grep -c 'Orca'`)은 이번 회차에 판별력 있는 대체 측정
    (소스 신설 토큰 4 종 · baseline 0 → 현재 2/2/1/0)으로 보강해 재판정했다.
  - `grep` 0 건을 근거로 쓴 곳(AP-01 · AP-02 · 배제 문장 잔존)은 전부 **패턴 유효성**을 함께 쟀다
    — AP 패턴은 레포 전체에서 13·19 파일에 매치하고, 배제 문장은 1 회차에 2 건이었다.
    즉 "검사되지 않은 0" 이 아니라 "의도된 0" 이다.
- 셸 스니펫 실행 검증: SKILL.md 음성 대조 스니펫 **총 4 회 실행 (bash 2 · zsh 2)** — 전부 동일 출력.
  1 회차가 지적한 `mktemp /tmp/gate-XXXX.py` 재실행 불가가 `mktemp -t gate` 로 고쳐졌고,
  **2 회 연속 실행이 두 셸 모두에서 성공**함을 확인했다 (1 회차에는 2 회차부터 죽었다).
  미실행 0 건.

## Summary
- Total: **23/23** conditions passed
- Verdict: **APPROVE**
- 1 회차 FAIL 2 건 모두 해소 — AR-03(파생 HTML 미반영) · DG-04(스킬 미실행).
- 사용자 확인 요청 3 건 처리 결과:
  1. AR-03 · DG-04 직접 재측정 완료. DG-04 는 산출물 6 개에 레포 게이트를 직접 돌려
     `RESULT: PASS` · exit 0 을 양쪽 슬라이서에서 재현했다.
  2. 1 회차 통과 21 건 전수 재측정 — 회귀 0 건. SC-01 음성 대조는 SKILL.md 가 이번 회차에
     바뀌었으므로 **변경 후 기준으로 다시 실행**해 확인했다. AR-01 도 재측정(12 건, 목록 밖 0).
  3. `scripts/detect-docs-drift.py` 는 **순수 추가**다 (10 insertions · 0 deletions).
     매핑 17 → 18, 제거 0, 추가 1(`bambu-kit/skills/bambu-print-profile/references/`).
     다른 킷 매핑 불변을 HEAD 대비 집합 비교로 확인했고, 양성 대조(`--since` 과거 ref)로
     새 매핑이 실제로 발동하는 것까지 봤다 — 공허한 추가가 아니다.

## 조건 밖 관찰 (verdict 영향 없음 · 정리 권장)
1. `.noenum` · `.nomachine` — 레포 루트에 0 바이트 찌꺼기 2 개(09-14 10:53).
   `mktemp` 버그로 `$GATE` 가 비었을 때 생긴 것이다. 지금은 고쳐져 재발하지 않지만
   파일은 남아 있다. `rm` 권장. (`00000.log` 는 09-13 09:49 로 봉인 이전이라 이번 스프린트 소산 아님)
2. 게이트 스코프 색인이 `profiles/BBL` 만 읽어, 이번 스프린트가 권장하기 시작한 오르카 전용 키가
   전부 `[미검증]` 으로 떨어진다 — `scarf_joint_speed` 는 오르카 전 벤더 프로파일에 **187 건**
   있는데 BBL 트리에는 **0 건**이다(평가자 직접 집계). 판정 불가는 통과로 취급되므로
   위반을 놓치는 쪽으로도 샌다. 사이드카 백로그 #1 과 같은 건이며 조건 범위 밖이다.
3. `SKILL.md:1582` 에 `gate-XXXX` 문자열이 1 건 남아 있으나 이는 고친 버그를 설명하는 주석이다.
   실행되는 명령은 `:1584` 의 `mktemp -t gate` 이며 정상이다.

## Improvement Suggestions
- [AR-01] 측정-방식-불일치 — pathspec 이 열거 목록과 같은 범위라 "그 밖 0 건" 이 두 디렉토리
  밖을 볼 수 없다. 다음 계약은 Diff-Scope Oracle 4 요소를 갖춰라:
  `Given: 봉인 후 구현 완료 시점 · 측정: git status --porcelain (pathspec 없음) ·
  생성물 제외: .harness/ · *.log · 기대 집합: {열거 8 경로} ∪ {AR-02 가 요구하는 3 파일}
  ∪ {sync-orchestrator 전파분}`. 지금 형태는 AR-02 와의 충돌을 pathspec 으로 숨기고 있어,
  범위 이탈이 생겨도 영원히 잡히지 않는다.
- [AR-03] 측정-방식-불일치 — `grep -c 'Orca' >= 1` 은 구현 전 baseline 이 이미 2/14/7 이라
  조건이 완전히 깨진 상태에서도 통과한다(1 회차에 실제로 그렇게 통과했다).
  측정 토큰은 **구현 전 baseline 을 1 회 실행해 0 건임을 확인한 뒤** 고르라.
  이번 건의 올바른 형태: `grep -c 'Phase 1.95' >= 1` + 배제 문장 `grep -c` == 0.
  (AM-01 이 같은 지적을 했으나 대상 파일을 바꿔치우는 방식이라 `relaxing` 이 됐다 —
  **측정 토큰만 바꾸고 대상 집합은 건드리지 마라.**)
- [DG-04] 측정-환경-오염 — "수정된 스킬을 실행" 은 Skill 도구가 **설치본 캐시**를 부르기 때문에
  레포에서 개발 중인 킷에는 그대로 적용할 수 없다. 다음 계약은 정본을 명시하라:
  `측정: 레포 SKILL.md 를 정본으로 실행하고 산출물에 <스프린트 고유 표식> 이 기록될 것`.
  이번엔 `_target_slicer` 가 그 표식 역할을 해서 판정이 가능했지만, 우연히 그랬을 뿐이다.
