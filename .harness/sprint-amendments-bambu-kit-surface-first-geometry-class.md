# Amendments — bambu-kit-surface-first-geometry-class

계약 본문은 봉인돼 있다 (`conditions_digest: sha256:65d829d758d1fc9e`). 아래는 qa-evaluator 교차 진단(Step 8,
2026-09-08 · 구현 착수 전)이 지적한 **측정 범위 미한정**을 좁히는 amendment 다. 전부 PASS 집합을 줄이는
`narrowing` 이며 앵커는 없다 (`unanchored` — 에이전트 자체 판단, 사용자 발언 인용 없음). 스키마 §Amendment
사이드카에 따라 `narrowing · unanchored` 는 PASS 근거로 쓸 수 있다.

## AM-01 — narrowing
- 대상 조건: SK-01
- 변경: "그 섹션 본문" 을 `awk '/^### 2\.7\./{p=1} p && /^## /{exit} p' surface-recipes.md` 로 추출한 범위로 한정한다. `30` · `0.5` · `planar` · `thin` · `_geometry_class` 의 `grep -c` 는 이 추출 결과에만 적용한다 (파일 전역 grep 은 baseline 에 이미 `30` 10 회 · `0.5` 4 회가 있어 변별력이 없다)
- 근거 (redaction 거친 원문): 교차 진단 — "무한정 grep 이면 새 섹션을 안 써도 통과 가능. §추출 규약과 같은 awk 범위 지정 필요"
- 앵커: 없음 (unanchored · session=1778a3e2 · cwd=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/bambu-surface-first-geometry)

## AM-02 — narrowing
- 대상 조건: SK-02
- 변경: `SKILL.md` 의 (b) 블록은 `**형상 클래스 라우팅` 으로 시작하는 줄부터 `**Ironing 정책` 줄 직전까지, (c) 목록은 `**process JSON 튜닝 정책 (override 대상):**` 줄부터 `### 환경 검증` 줄 직전까지로 고정한다. `grep -nE 'thin.*outer_wall_speed|outer_wall_speed.*thin'` 매치 줄 번호가 두 범위에 각 1 건 이상 들어가야 PASS
- 근거 (redaction 거친 원문): 교차 진단 — "(b)블록/(c)목록 범위를 가리키는 grep/awk 앵커가 없어 매치가 어느 쪽에 속하는지 평가자가 임의 판단해야 함"
- 앵커: 없음 (unanchored · session=1778a3e2)

## AM-03 — narrowing
- 대상 조건: SK-05
- 변경: "Gotcha 체크리스트 섹션 안" 을 `awk '/^## Gotcha 체크리스트/{p=1} p && NR>1 && /^## / && !/Gotcha/{exit} p' SKILL.md` 추출 결과로 한정한다. `_geometry_class` · `스코프` 의 `grep -c` 는 이 범위에만 적용한다
- 근거 (redaction 거친 원문): 교차 진단 — "`_geometry_class` 는 SK-01/03/04 에 의해 문서 전역에 반드시 등장하므로 무한정 grep 은 Gotcha 에 안 써도 통과"
- 앵커: 없음 (unanchored · session=1778a3e2)

## AM-04 — narrowing
- 대상 조건: AR-03
- 변경: "그 표가 속한 섹션" 을 `awk '/^### 10\.5\./{p=1} p && /^출처 \(§10 전체\)/{exit} p' bambu-fields-baseline.md` 추출 결과로 한정한다. `filament` 와 `02.08.02.61`|`02.08.00.06` 의 `grep -c` 는 이 범위에만 적용한다 (파일 전역에는 `filament` 32 회 · 버전 문자열 4 회가 이미 있다)
- 근거 (redaction 거친 원문): 교차 진단 — "`filament`(기존 32회) · 버전문자열(기존 4회)이 파일 전역에 이미 존재해 스코프/버전 병기 요구는 무한정 grep 으로는 사실상 항상 통과"
- 앵커: 없음 (unanchored · session=1778a3e2)

## AM-05 — narrowing
- 대상 조건: SK-04
- 변경: 측정 토큰에 임계 리터럴 `THIN_LOOP_MM = 30.0` 과 `THIN_SHARE = 0.5` 각 1 건 이상을 추가한다. SC-04 의 음성 대조(`30` → `3`)가 이 상수의 존재를 전제하므로 SK-04 가 그것을 보장해야 한다
- 근거 (redaction 거친 원문): 교차 진단 — "분류 임계 리터럴 `30`(둘레mm)·`0.5`(median비율)는 검사 안 함 — SC-04 음성대조가 바로 이 `30` 상수 편집을 전제"
- 앵커: 없음 (unanchored · session=1778a3e2)

## 참고 — amendment 가 아닌 지적

- SC-02 · ER-02 "픽스처가 인접 4 키를 고정하지 않으면 유량비 게이트가 음성 대조를 오염" — 픽스처 `process-thin-speed-lowered.json` · `process-speed-without-class.json` 은 인접 4 키를 `80/85/80/60` (유량비 `2.86x`) 으로 고정해 이 오염을 막았다. 조건 변경 없음
- DG-01 · DG-03 은 `project.yaml` 의 `commands.analyze` · `commands.test` 리터럴이며 이 스프린트 산출물과 무관한 레포 공통 관례다. 조건 변경 없음
