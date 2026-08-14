# Sprint Feedback
Feature: 카이젠 Phase 13 — bambu-kit 실측 실패 3종(L1 곡면 계단 / L2 스트링잉 / L3 바닥 박리) 인테이크 + 지원가능성 분기 + E3 금지 키 확장 (v2 계약 재평가)
Evaluated: 2026-08-14 13:10
Verdict: APPROVE
Iteration: 2 (v1 REJECT 15/16 AP-03 FAIL → 사용자 앵커로 계약 v2 재작성 → 본 재평가는 v2 를 처음부터 독립 재검증)

## 재평가 배경

이 계약은 두 차례 판정을 거쳤다: (1) 최초 판정(status: done 전환됨)이 있었으나 오케스트레이터의
structured output schema 강제로 글로벌 피드백 풀에 저장되지 않아 무효 취급, (2) 독립 재평가
(Iteration 1, 2026-08-14 11:21)가 v1 계약을 16개 조건 전부 재실행 검증하여 15/16 PASS ·
AP-03 FAIL(측정 clause 2 결함 — 닫는 fence 를 세는 패턴이 언어 힌트 정상 부착된 신규 코드블록만
추가해도 항상 위반으로 잡히는 구조적 결함)로 REJECT, 글로벌 저장(`1a3bcba6-2026-08-14T112435-df1b3e15-17562.yaml`)
까지 완료. 이후 사용자 앵커로 오케스트레이터가 AP-03 clause 2 측정문만 파일 상태 기반 방식으로
교체한 v2 계약(커밋 033a6ab)을 작성. 본 재평가는 **이전 판정을 승계하지 않고** v2 계약 16개 조건
전부를 처음부터 독립 재실행 검증했다.

## Contract Fingerprint
- path: `.harness/sprint-contract-kaizen-phase13-failure-modes.md`
- sha256(full): 2042b891e9bbe235edd7ef5eb77c305d54bbc35a77dbf5ddd9eb77a786dbf779
- seal(conditions_digest): sha256:27d4a8c7b52f668d
- seal_status: **SEAL_OK** (recorded=27d4a8c7b52f668d, actual=27d4a8c7b52f668d — v1→v2 는 조건 체크박스 줄을 건드리지 않았으므로 digest 불변이 정상. 독립 재계산으로 v1 파일(커밋 1c6216b)의 digest 도 동일 27d4a8c7b52f668d 임을 별도 확인)
- status: active (frontmatter — 오케스트레이터가 재평가를 위해 done→active 로 되돌림, `owner_session` 이 본 세션과 일치)
- slug: kaizen-phase13-failure-modes
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 1 (오케스트레이터가 절대경로로 지정) — session-owned(ladder 2)로도 동일 결과
- 재확인(Step 5): 일치 (TOCTOU 없음)
- status_transition: active -> done (verdict=APPROVE 이므로 전환)

⚠️ **계약 헤더 규약 위반 (contract-schema v4)**: `## 폐기·재작성 (v2) — 앵커 있는 교체` 섹션은
허용 서술 섹션 목록(배경/리서치 소스/GAP 분석/범위 경계/회귀 게이트)에 없는 헤더다. 단, 이 섹션은
조건 체크박스를 포함하지 않는 순수 메타 로그(v1→v2 재작성 근거 + 앵커 기록)이므로 조건 판정에는
영향이 없다. 계약 결함으로 기록만 한다 — 다음 사이클에서 이런 "재작성 로그" 를 위한 전용 서술
섹션(예: `변경 이력`)을 허용 목록에 추가하거나, 앵커 기록을 사이드카로 이관하는 것을 권장.

## 독립 검증 절차

1. `verify_seal` 실행 → `SEAL_OK` (조건 수 계산: `grep -cE '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}'` → `16`, frontmatter `conditions: 16` 과 일치)
2. 구현 범위 확정: `git log --oneline main..HEAD`로 구현 커밋 `04641f7` 단독 확인. 이후 `03669c7`은
   `bambu-kit/.claude-plugin/plugin.json` 버전 bump 1줄만(범위 경계가 명시적으로 제외한 파일) —
   `git diff --name-only 04641f7^ 04641f7 -- bambu-kit`가 정확히 4개 마크다운과 일치, 현재
   워킹트리 `git status --porcelain -- bambu-kit`는 clean (이미 커밋됨).
3. v1→v2 diff를 직접 계산해 "나머지 15조건 문구 무수정" 주장을 독립 검증 — frontmatter 4줄 +
   `## 폐기·재작성 (v2)` 섹션(59줄) + AP-03 측정 clause만 변경, 나머지 조건 블록은 diff에 등장하지
   않음을 확인.
4. 16개 조건 전부 명령 직접 실행 (아래 Results). AP-03 clause 2(v2)는 특히 커밋 페어(`04641f7^`/`04641f7`)
   기준 파일 전문 상태추적 파서를 직접 작성해 실행 — 3개 변경 마크다운 파일 전부 "언어 힌트 없는
   여는 fence" 개수가 부모 대비 증가 0건.
5. SK-03 게이트, RE-02 스니펫에 대해 실제 음성 대조(negative control)를 직접 실행 —
   FORBIDDEN dict 제거 시 bad.json이 PASS로 반전, `zzz_fake_key` 추가 시 MISSING=1로 반전 (원본 복구 후
   `git status` clean 재확인).
6. 대표 오라클 셋(SK-01/02/04, AR-01, AP-03 clause1, DG-01, AR-02 스니펫, ER-01~02, AR-03, RE-01,
   DG-03, SK-03 게이트, RE-02 스니펫 — 16조건 전부의 오라클)을 bash·zsh 양쪽에서 실행해 출력 diff 0 확인.

## Amendments
- amendments: 2
- narrowing: 1 (AM-02 — 조건 수 15→16 정정. frontmatter `conditions: 16`에 이미 반영, 실측 재확인 일치)
- unknown: 1 (AM-01 — v1 AP-03 clause 2 측정문 결함 자기 공개, direction=unknown/unanchored → PASS 근거로 사용 불가. **단 이 amendment는 이제 무효화되지 않고 moot다** — v2 계약 자체가 AP-03 측정문을 사용자 앵커로 직접 교체했으므로, 본 재평가는 AM-01 을 참조하지 않고 v2 측정문을 독립 실행하여 PASS 에 도달)

## User Correction Audit
- correction_log_status: available (`~/.claude/logs/claude-plugins/2026-08.md`)
- 조사 범위: 계약 v1 생성(2026-08-13 18:27) ~ 평가 시각(2026-08-14 13:10)의 프롬프트 블록
- 실제 사람 프롬프트: `ㄱㄱ`(18:00:32, 20:05:47 — 오케스트레이터 계속 트리거), `다음 세션`(08-14 10:43:53),
  세션 이어받기 요약 1건(08-14 11:15:36, 방향 교정 아닌 상태 요약). 나머지는 전부 `<task-notification>`
  (서브에이전트 비동기 완료 알림). v2 재작성 결정("3 선택지" 제시·"계약 v2 재작성" 선택)에 대응하는
  별도 로그 항목은 이 윈도우에서 찾지 못함 — 오케스트레이터 판단으로 처리된 것으로 보이나, 이는
  본 재평가의 조건 판정 대상이 아니므로 verdict에 영향 없음.
- unreflected_corrections: 0
- verdict 영향: 없음 (표면화 전용)

## Results

### Skill (4/4)
- [x] SK-01: Phase 1.9 Failure-Mode Detector 신설 + Phase 2 게이트 — PASS
  - 근거: `SKILL.md:475` `### Phase 1.9 — Failure-Mode Detector` 1건. `SKILL.md:536` `#### Failure-Mode Gate (Phase 2 진입 조건)` 1건. `SKILL.md:543` `Phase 1.9 completed (Failure-Mode Gate)` 매치. `SKILL.md:513/517` `§3.8 User-Reported Failure Gate` 앵커가 Phase 1.9 절(475-540) 내부에서 "정본은 …다. 여기서 규칙을 다시 쓰지 말고 그대로 따른다"로 인용만 하고 재정의 안 함 (L3: 1.9.1~1.9.4 전체 Read 확인)
- [x] SK-02: Phase 3.0 Supportability Split — PASS
  - 근거: `SKILL.md:569` `#### Phase 3.0 — Supportability Split` 1건. 섹션(569-602) 내 `notes only` 2건(575,578), `adaptive_layer_height` 1건(575) 매치. Phase 3 튜닝 정책의 `adaptive_layer_height` 행 `SKILL.md:719` `- ❌ \`adaptive_layer_height\`` 로 시작 확인 (L3: 표 전체 Read로 L1/L2/L3 각 항목이 지원가능/불가능 명확히 분기됨을 확인)
- [x] SK-03: Phase 4.3 E3 게이트 금지 키 4종 실행 차단 — PASS
  - 근거: SKILL.md 마지막 python 히어독(4.3 게이트)을 추출해 실제 실행. clean.json → `RESULT: PASS` exit `0`. bad.json(금지 4키) → `RESULT: FAIL` exit `1`, FAIL 행 4건(adaptive_layer_height/bed_temperature/bed_temperature_initial_layer/elephant_foot_compensation). subonly.json(`bed_temperature_initial_layer`만) → 금지 키 FAIL 1건(substring 비충돌 확인). **음성 대조 직접 실행**: FORBIDDEN dict를 `{}`로 치환 후 재실행 → bad.json이 `RESULT: PASS` exit `0`으로 반전 확인
- [x] SK-04: L2 스트링잉 건조 우선 게이트 3단계 + 온도/fan 금지 유지 — PASS
  - 근거: `SKILL.md:730` `L2 스트링잉 게이트 예외` 1건. 표(732-736)에 `filament_wipe`(735)/`filament_retraction_length`(736)/`coupon`(736) 매치. `SKILL.md:726` `온도를 자동 하향하지 마라` 1건. `SKILL.md:726` `사용자 명시 요청 2026-05-16` 1건(기존 금지 보존, v1과 동일 카운트로 정정이 삭제하지 않았음을 확인) (L3: 표 전체 Read로 게이트 예외와 온도/fan 미변경 규칙이 상충 없이 공존함을 확인)

### Error (2/2)
- [x] ER-01: layer_height 0.08 근거 오귀속 정정 — PASS
  - 근거: `surface-recipes.md` `박스/도구` 0건, `1 차 권장` 1건, `미확인` 2건. `bambu-fields-baseline.md` `layer_height 0.08-0.12` 0건. `surface-recipes.md:107` 실제 행: "`0.12`: 0.12mm High Quality @BBL H2S.json (공식 체인 실재). **`0.08` 은 이 파일의 공식 근거가 아니다**...`[미확인]`" (L3 Read 확인)
- [x] ER-02: enable_arc_fitting / resolution 성격 오귀속 정정 — PASS
  - 근거: SKILL.md `(원통 모델)` 0건, `G-code encoding` 2건(`SKILL.md:718` "품질 개선 기능이 아니라 G-code encoding 변경"). `surface-recipes.md:116` `Z 계단의 주 해결책이 아니다` 1건 (`resolution` 행에 부착 — "⚠️ **XY 세그먼트 해상도 전용** — Z 계단의 주 해결책이 아니다") (L3 확인)

### Architecture (3/3)
- [x] AR-01: 변경이 정확히 4경로로 한정 — PASS
  - 근거: 계약 Given절("커밋 직전 working tree")을 구현 커밋 `04641f7`로 재구성(현재 워킹트리는 이미 커밋되어 `git status --porcelain -- bambu-kit`가 vacuous 공백). `git diff --name-only 04641f7^ 04641f7 -- bambu-kit | LC_ALL=C sort` → `SKILL.md`, `references/bambu-fields-baseline.md`, `references/failure-recipes.md`, `references/surface-recipes.md` 4행 정확히 일치. 이후 `03669c7`(plugin.json 버전 bump)은 Scope 밖이며 이 4경로에 미포함 확인
- [x] AR-02: bambu-fields-baseline.md §10 L1/L2/L3+금지 키 전수 백틱 존재 — PASS
  - 근거: §AR-02 스니펫 직접 실행 → `EXPECT=27 MISSING=0`. `## 10. 실측 실패 모드 관련 필드` 헤더 1건. 섹션 순서 `## 9. 미해결 / 검증 필요`(226) → `## 10. 실측 실패 모드 관련 필드`(232) 확인(tail -2)
- [x] AR-03: failure-recipes.md 신설 + 3곳 참조 — PASS
  - 근거: `test -f` exit 0. 파일 트리 `SKILL.md:38` `├── failure-recipes.md`. frontmatter description에 `references/ 8종` 1건, `references/ 7종` 0건. Phase 3 도입부(`SKILL.md:564` 헤더 바로 다음 `SKILL.md:567`) `Phase 1.9 에서 실패 모드가 1 건 이상 감지됐으면 references/failure-recipes.md 도 로드한다` (L3 확인)

### Anti-patterns (2/2)
- [x] AP-01: 신규 URL 전부 evidence 파일 또는 변경 전 트리에 실재 — PASS
  - 근거: §AP-01 스니펫을 구현 커밋(`04641f7^..04641f7`) diff 기준으로 직접 실행 → `UNSOURCED_URL=0`. 신규 토큰 `0.07`(evidence 2건), `0.8`(3건), `auto_brim`(2건), `Spiral`(1건) 전부 evidence 파일에 매치. (상태 전제 미명시 조건 — AR-01과 동일하게 구현 커밋 기준으로 재구성해 기록)
- [x] AP-03: bare code fence 신규 미도입 — **PASS (v1→v2에서 뒤집힘)**
  - 근거 — 세 clause 전부 독립 실행:
    - clause 1: `python3 scripts/validate-plugin.py bambu-kit` → `V6 code-fence 0 bare — OK`, exit `0` (충족)
    - clause 2(v2 신규 방식): diff가 아닌 **파일 상태**로 측정. `git show 04641f7^:<파일>`과 `git show 04641f7:<파일>`의 파일 전문을 직접 작성한 Python 상태추적 파서(fence 발견마다 in/out 토글, 열림 시 언어 힌트 유무 판정)로 각각 파싱해 "언어 힌트 없는 여는 fence" 개수를 비교 — `SKILL.md`(parent=0,impl=0), `bambu-fields-baseline.md`(0,0), `surface-recipes.md`(0,0). **부모보다 증가한 파일 0건** (충족). 신규 파일 `failure-recipes.md`는 부모에 없으므로(→ `git cat-file -e 04641f7^:...` exit 128 확인) 별도 clause 3으로 처리
    - clause 3: `failure-recipes.md`에서 `grep -c '^```$'` → `1`(닫는 bare fence, 106행 `\`\`\`text` 여는+122행 `\`\`\`` 닫는 — 총 fence 2줄 중 bare는 닫는 1줄뿐). 여는 fence 총수(`grep -cE '^```'` → 2줄 중 여는 1개) `1` 과 일치 → 충족
  - v1 대비 변화: v1 clause 2는 `git diff -U0 -- bambu-kit | grep -c '^+\`\`\`$'` (닫는 fence까지 셈, 실측 `5`)로 구조적 결함이 있었으나, v2는 파일 상태 기반 여는-fence-전용 파서로 교체되어 결함 해소. 독립 재현으로 확인 — clause 2 설계 자체가 diff의 부분성(hunk 경계에서 여는/닫는 짝이 어긋나는) 오탐 요인을 제거함

### Reusability (2/2)
- [x] RE-01: 신규 파일 정확히 1개, 신규 디렉토리 0개 — PASS
  - 근거: (상태 전제 미명시 — AP-01과 동일하게 구현 커밋 기준 재구성) `git diff --name-status 04641f7^ 04641f7 -- bambu-kit`에서 `A`(added) 파일 정확히 1건 = `failure-recipes.md`. `find bambu-kit -type d -newer .harness/project.yaml`로 나온 5개 디렉토리는 전부 기존 디렉토리(`bambu-kit`, `.claude-plugin`, `skills`, `bambu-print-profile`, `references`)로 mtime 노이즈이며 신규 디렉토리 아님을 확인 — 신규 파일이 기존 `references/` 안에 생성됨
- [x] RE-02: failure-recipes.md가 새 설정 키를 발명하지 않음 — PASS
  - 근거: §RE-02 스니펫 직접 실행 → `SIBLINGS=7 KEYS=28 MISSING=0`. **음성 대조 직접 실행**: `zzz_fake_key`를 failure-recipes.md에 추가 후 재실행 → `MISSING=1  MISSING zzz_fake_key` 확인 후 원본 복구, `git status --porcelain -- bambu-kit` clean 재확인

### Diagnostics (3/3)
- [x] DG-01: validate-plugin.py bambu-kit V1~V8 전부 OK, exit 0 — PASS
  - 근거: 직접 실행 `V1~V8` 전부 OK, `Total: 1 plugins, 1 OK`, `Exit: 0`
- [x] DG-02: 모든 grep/git/python 오라클 zsh·bash 동일 출력 — PASS
  - 근거: 16개 조건의 대표 오라클(SK-01/02/04, AR-01, AP-03 clause1, DG-01, ER-01 4항목, ER-02 3항목, AR-03 3항목, RE-01, DG-03 블록수, AR-02 스니펫, SK-03 게이트 fixture, RE-02 스니펫)을 bash·zsh 양쪽에서 각각 실행 — 전 항목 diff 0(IDENTICAL) 직접 확인
- [x] DG-03: SKILL.md 임베드 python 히어독 전부 ast.parse 통과 — PASS
  - 근거: 정규식 추출 → 히어독 3개 블록(19/15/48줄), `ast.parse` 전부 통과, SyntaxError 0건

## Unverifiable Summary
- 총 미검증 건수: 0
- 건 목록: 없음 (전 16조건 직접 실행/의미 추적으로 판정, 도구·환경 부재 없음)
- Verdict 영향: 해당 없음

## Evidence Validity
- 검사 대상 증거: 16건
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 16건 전부 실행, bash·zsh 양쪽 확인 16건 IDENTICAL, 미실행 0건
- 음성 대조(negative control) 직접 실행: SK-03(FORBIDDEN dict 제거 → bad.json PASS 반전), RE-02(zzz_fake_key 추가 → MISSING=1 반전) — 원본 복구 후 git status clean 재확인
- 상태 전제 미명시 조건(AP-01/RE-01)은 AR-01의 명시적 Given("커밋 직전 working tree")과 동일 컨벤션으로 구현 커밋(04641f7) 기준 재구성해 기록. AP-03 v2는 이 문제 자체를 diff 대신 특정 커밋 페어 비교로 설계 변경해 해소함(상태 비의존)

## Summary
- Total: 16/16 conditions passed
- Verdict: **APPROVE**
- v1(15/16, AP-03 FAIL) → v2(16/16, AP-03 PASS): AP-03 measurement clause 2가 파일 상태 기반 방식으로
  교체되어 실제 코드 품질(V6 0 bare)과 측정 결과가 정합하게 됨. 나머지 15조건은 v1에서도 이미
  PASS였고 문구 무수정이므로 본 재평가에서도 동일하게 PASS 재확인.

## Improvement Suggestions
- [계약 헤더] 구조위반 — `## 폐기·재작성 (v2)` 헤더가 contract-schema v4 허용 서술 섹션 목록 밖. "재작성 로그"류 메타 서술을 위한 전용 허용 헤더(예: `변경 이력`)를 v5 스키마에 추가하거나, 이런 기록은 사이드카(amendment)로 이관하는 패턴을 contract-design-guide에 권장 (2회 이상 반복 시 contract_ambiguity_notes 승격 후보)
- [계약 봉인] 커버리지 갭 — 계약 자신이 이미 기록했듯, `conditions_digest`가 조건 체크박스 줄만 해시하여 측정문(들여쓴 서술) 변조는 봉인을 깨지 않는다. 이번 v1→v2가 실례. 이 Phase의 조건은 아니지만(계약이 명시) 다음 사이클 contract-seal 개선 신호로 재확인
- [AR-02 서술] 정확도 — "27 키 중 layer_height/resolution 을 뺀 나머지가 전부 0 파일"이라는 사전 상태 서술에 오차 있음: 실측(구현 커밋 부모 상태) 결과 `brim_width`(1파일), `raft_layers`(2파일), `initial_layer_print_height`(1파일), `elephant_foot_compensation`(2파일)이 이미 0이 아니었음 (그리고 `resolution`은 애초에 27키 목록에 없음 — 서술 오류). 단 AR-02의 실제 그레이딩 명령(§AR-02 스니펫 MISSING=0)에는 영향 없어 조건 판정 자체는 영향받지 않음. 다음 계약 작성 시 이런 사전상태 서술도 실측 명령으로 재검증할 것을 권장
