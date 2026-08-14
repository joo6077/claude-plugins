---
feature: "카이젠 Phase 13 — bambu-kit 실측 실패 3종(L1 곡면 계단 / L2 스트링잉 / L3 바닥 박리) 인테이크 + 지원가능성 분기 + E3 금지 키 확장"
created: "2026-08-13 18:27"
rewritten: "2026-08-14 (v2 — AP-03 clause 2 측정문 결함: 닫는 fence 를 셌다)"
complexity: "복잡"
conditions: 16
slug: kaizen-phase13-failure-modes
status: active
owner_session: 1e76aa0b-dd42-4693-b79a-c2e2e6dfb88f
supersedes_digest: sha256:27d4a8c7b52f668d
supersedes_commit: 1c6216b
conditions_digest: sha256:27d4a8c7b52f668d
locked_at: "2026-08-14 (v2)"
---

## 폐기·재작성 (v2) — 앵커 있는 교체

원 계약(`1c6216b`, digest `sha256:27d4a8c7b52f668d`)은 폐기됐다. 원문은 git 이력에 보존된다.

### 폐기 사유 — AP-03 clause 2 가 원문 그대로 만족 불가능

clause 2 는 `git diff -U0 -- bambu-kit | grep -c '^+```$'` 가 `0` 일 것을 요구한다.
그런데 이 패턴 `^+```$` 는 **언어 힌트가 없는 줄**, 즉 마크다운 코드블록의 **닫는 fence** 를 센다.
여는 fence 는 정상적으로 언어 힌트를 달면 `+```bash` 형태가 되어 이 패턴에 걸리지 않지만,
그 블록의 **닫는 fence 는 언어 힌트를 가질 수 없다.** 따라서 코드블록을 하나라도 새로 추가하면
clause 2 는 **항상** 0 이 아니게 된다. 조건이 재는 대상(bare 여는 fence)과 측정문이 세는 대상
(닫는 fence)이 다르다.

실측 (구현 커밋 `04641f7`, bash·zsh 동일):

```text
git diff -U0 04641f7^ 04641f7 -- bambu-kit | grep -c '^+```$'   →  5
매치 5 건의 정체: 30:+```bash  37:+```  48:+```text  51:+```  68:+```text
                 75:+```  110:+```text  115:+```  385:+```text  401:+```
  → 여는 fence 5 개는 전부 언어 힌트(bash·text)를 가짐. 매치된 5 건은 전부 닫는 fence.
python3 scripts/validate-plugin.py bambu-kit  →  V6 code-fence 0 bare — OK
```

즉 **실제 코드 품질에는 결함이 없고**(clause 1 의 권위 있는 검사 V6 가 `0 bare`), 측정문만
구조적으로 충족 불가다. 같은 조건의 **clause 3 은 이미 올바른 방식**(여는 fence 수와 대조)을
쓰고 있어, clause 2 는 clause 3 과 중복이면서 서로 모순된다.

이번 사이클 Phase 2 가 처리한 **산문↔측정문 커버리지 갭(F1)**, Final v2 의 **ER-02 자기참조
측정 결함**과 정확히 같은 유형이다.

### 앵커

- **승인 주체**: 사용자. 2026-08-14, 오케스트레이터가 재평가 REJECT 근거(독립 QA 2 회 동일 결론)와
  함께 3 선택지(계약 v2 재작성 / amendment 무효화 / REJECT 유지)를 제시하고 **"계약 v2 재작성"** 을
  선택받았다.
- **재작성 주체**: 오케스트레이터. 구현 서브에이전트가 자기 산출물을 통과시키려 고친 것이 아니다.
- 변경은 **AP-03 한 조건의 측정문**뿐이며 나머지 15 조건은 문구 무수정이다. 조건 수는 16 으로 불변.

### 봉인 digest 가 v1 과 동일한 이유 — 봉인 커버리지 갭 (다음 사이클 신호)

`supersedes_digest` 와 `conditions_digest` 가 둘 다 `sha256:27d4a8c7b52f668d` 로 **같다.**
오기가 아니다. 봉인은 `^- \[[ x]\] [A-Z]{2,}-[0-9]{2}` 에 걸리는 **조건 체크박스 줄만** 해시하는데,
이번 재작성은 AP-03 의 **들여쓴 측정문**만 바꿨고 체크박스 줄은 글자 하나 바뀌지 않았다.

즉 이번 사이클 Phase 2 가 만든 봉인(E3)은 자기 규격의 목적 서술
*"조건 문구 변조와 조건 추가·삭제는 반드시 깨진다"* 를 **측정문에 대해서는 달성하지 못한다.**
조건의 판정력은 대부분 측정문에 있으므로, 측정문은 조용히 바뀌어도 `SEAL_OK` 가 유지된다.
이 계약의 v1→v2 가 바로 그 실례다 (61 줄 추가 · 7 줄 삭제 · `SEAL_OK` 불변).

**이것은 이 Phase 의 조건이 아니다** — 다음 사이클 Phase 2(contract-seal) 가 먹어야 할 신호로
여기 기록만 한다. 이 계약의 판정에 사용하지 마라.

### 재평가 규약

status 를 `active` 로 되돌렸다. v2 로 재평가하여 APPROVE 를 받은 뒤 `done` 으로 전환한다.
v1 에 대한 REJECT 아티팩트(`1a3bcba6-2026-08-14T112435-df1b3e15-17562.yaml`)는 삭제하지 않는다 —
측정문 결함의 발견 근거이므로 다음 사이클 데이터 풀이 먹어야 한다.


## 배경

`.harness/.meta/evidence/phase13.md` 가 이번 Phase 의 **유일한 외부 근거**다. 외부 조회 0 회.

`/insights` 2026-08-13 신규 델타 D1 이 이 Phase 를 직접 지목한다 (`insights-report.md:34-43`,
`kaizen-data-pool.md:182-187`): shower-box 부품 + holster 모델 **5 세션**에서 실물 출력이 계속 새
문제를 노출했고 결과는 "partially successful" 이었다 — **곡면 계단현상 · voronoi 스트링잉 · 바닥 박리**.
D1 은 직전 사이클 흡수분 표에 없는 **신규 신호**다 (직전 Phase 13 은 `xy_hole_compensation` 공차 SSOT
오류를 고쳤고, 이 3 종은 다른 실패 모드다).

**근본원인 — 왜 안 걸렸나.** 이 스킬에는 **사용자 자신의 직전 출력 실패가 다음 프로파일 생성으로
들어오는 경로가 아예 없다.** Phase 1.6 은 MakerWorld *댓글의 남의 실패*만 모으고, Phase 1.7/1.8 은
사전 형상·표면 의도만 본다. 그래서 v0.4.2 공차 정정도 2026-07-27 표면 의도 게이트도 전부 사용자가
불만을 말한 뒤의 손 수습이었다. **인테이크 부재**가 원인이므로 규칙 문장을 하나 더 써도 안 걸린다 —
Phase 1.9 라는 **경로**를 만들어야 한다.

**enforcement 등급 처리.** 이번 사이클 하드 프레이밍(같은 규칙 재추가 금지)에 따라, 이미 존재하는
결정론적 게이트(Phase 4.3 · E3)에 **금지 키 검사 4 종을 검사 항목으로 확장**했다. 새 산문 규칙을
추가하지 않았다. 사용자 실측 보고의 취급은 Phase 1 이 신설한
`skill-design-guide.md` §3.8 User-Reported Failure Gate 를 **인용만** 하고 재정의하지 않는다 —
이 킷이 갖는 것은 §3.8 재현 6 축의 **3D 프린팅 도메인 치환표** 하나뿐이다.

**evidence 기반 정정 3 건:**

1. **`layer_height` `0.08` 의 근거가 없다.** `surface-recipes.md:107` 이 `0.08` 을
   "0.12mm High Quality @BBL H2S.json" 을 근거로 제시하는데, 0.12 프로파일은 0.08 의 근거가 될 수 없다.
   evidence: `0.08` 은 `min_layer_height 0.07` 위이지만 **H2S 공식 0.08 process 근거는 미확인**.
   → `0.12` 를 1 차 권장으로 올리고 `0.08` 은 `[미확인]` 라벨 + 사용자 확인 후로 강등.
2. **`enable_arc_fitting` 은 품질 기능이 아니다.** `SKILL.md:614` 가 "✅ (원통 모델)" 로 튜닝 카드처럼
   제시한다. evidence: Orca 문서상 **G-code encoding 변경**이며 firmware arc segmentation 리스크가 있다.
3. **`resolution` 은 Z 계단 해결책이 아니다.** evidence: XY 곡선 faceting 완화용. 현재 문서는 이 축
   구분 없이 "외벽 표면 권장값" 에 넣어 두어 L1 대응 카드로 오독될 수 있다.

**Phase 1 서브에이전트 스펙 정정과의 교차 없음** — bambu-kit 전체에서 중첩 깊이·frontmatter 필드 수를
서술하는 곳이 **0 건**이다 (`grep -rni '서브에이전트\|subagent\|중첩\|frontmatter' bambu-kit` → 매치 없음).
bambu-kit 은 에이전트 0 개인 1 스킬 킷이다.

## 리서치 소스 (evidence 파일 한정 — 외부 조회 0 회)

- `.harness/.meta/evidence/phase13.md` — L1/L2/L3 각각 (a) 키 (b) 기본값 (c) 권장 (d) 부작용 + 권장안
  + 금지 4 항 + 트레이드오프 3 항 + 열린 질문 4 항. **인용 URL·수치는 이 파일에 실재하는 것만 쓴다**
  (AP-01 이 잰다).
- `.claude/kaizen-input/insights-report.md` §D1 + `:109` Phase 매핑 — 신규 델타 확인.
- `.harness/.meta/kaizen-data-pool.md:182-187` — `/insights` 원문 ("partially successful").
- `harness/docs/guides/skill-design-guide.md` §3.7 (Enforcement 3 등급 · 등급 원장) · §3.8
  (User-Reported Failure Gate · 현재 등급 E1) — Phase 1 산출물. **인용 앵커이며 재정의 대상 아님.**
- `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol — `[미검증]`
  마커 정본. 이 Phase 가 쓰는 `[미확인]` 은 **문서 근거 미확보** 라벨로 다른 축임을 문서에 명시한다
  (Phase 11 선례와 동일 용법).
- `harness/references/contract-schema.md` v5.3 (Phase 2 산출물) — 본 계약의 포맷 SSOT.

## GAP 분석 (전부 사전 실측 · 구현 착수 전 명령 출력 기준)

| # | 갭 | 사전 실측 | 처리 |
| --- | --- | --- | --- |
| F1 | L1 키 (`min_layer_height` · `max_layer_height` · `adaptive_layer_height`) 가 킷 전체에 부재 | 파일 수 **0 / 0 / 0** | AR-02 |
| F2 | L2 filament override 키 7 종이 킷 전체에 부재 | 7 키 전부 **0** | AR-02 |
| F3 | L3 키 13 종(brim/raft/initial_layer/plate temp/aux fan)이 킷 전체에 부재 | `brim_type` · `brim_object_gap` · plate temp 3 종 · aux fan 2 종 등 전부 **0** | AR-02 |
| F4 | 실패 모드 인테이크 경로 부재 | `grep -c 'Phase 1.9\|Failure-Mode\|Supportability' SKILL.md` → **0** | SK-01 · SK-02 |
| F5 | Phase 4.3 E3 게이트의 금지 키 검사 | `elephant_foot_compensation` **만** 존재 · 나머지 3 종 **0** | SK-03 |
| F6 | `surface-recipes.md:107` 의 `0.08` 근거 오귀속 | 옛 행 매치 **1** | ER-01 |
| F7 | `SKILL.md:614` `enable_arc_fitting` 을 튜닝 카드로 제시 | 옛 문자열 `- ✅ \`enable_arc_fitting\` (원통 모델)` **1** | ER-02 |
| F8 | L2 대응 시 온도/fan 자동 변경 금지 규약 | 기존 `❌ retraction/fan/cooling 안 건드림` 1 행 — **게이트 예외 경로 없음** (자동 과상향 위험은 막지만 정당한 wipe 경로도 없음) | SK-04 |

**신설하지 않는 것**: 새 스킬 · 새 에이전트 · 새 카이젠 스킬 · plugin.json 버전 bump ·
`skill-design-guide.md` §3.8 의 재정의 · references 대량 갱신(별도 `/bambu-research` 소관) ·
`kaizen-sources.md` 폴링 소스 확장 · `BACKLOG.md` 편집.

## 범위 경계

**변경 경로는 정확히 4 개** (신규 1 + 수정 3). 목록은 AR-01 의 기대 집합 한 곳에서만 열거한다
(§측정 커버리지 표기의 화이트리스트 규칙). 계약 파일 자신과 `.harness/**` 는 AR-01 pathspec 밖이다.

- **건드리지 않는다**: `bambu-kit/README.md` (Scope 밖 — "references 4종" 표기가 이미 stale 하지만
  이번 Phase 의 쓰기 범위가 아니다 · 후속 이관 대상) · `bambu-kit/.claude-plugin/plugin.json` ·
  `bambu-kit/skills/bambu-print-profile/BACKLOG.md` (Scope 밖) · `docs/bambu-kit/*.html` (Scope 밖) ·
  `CLAUDE.md` · 다른 킷 전부.
- **`kaizen-sources.md` · `comment-analysis.md` · `materials.md` · `seam-recipes.md` · `tolerance.md` 는
  무변경.** 이번 Phase 는 3 종 실패 모드 대응 + 스킬 프로세스 개선에 한정한다.
- **evidence 에 없는 수치를 지어내지 않는다.** `hot_plate_temp_initial_layer` 등 plate-specific 키의
  **구체 온도값**은 evidence 에 없으므로 키 이름·단위까지만 기재하고 권장 수치를 쓰지 않는다 —
  근거 부족으로 이번 사이클 미반영. `bed_temperature` 의 obsolete 여부도 evidence 가
  `bed_temperature_initial_layer` 만 명시하므로 `[미확인]` 라벨을 달고 게이트 금지 목록으로만 취급한다.
- **default 수치 SSOT 는 `bambu-fields-baseline.md` §10 한 곳.** 신규 `failure-recipes.md` 는 정책·게이트·
  부작용만 갖고 default 를 재기재하지 않는다 (RE-02 가 잰다).
- **복잡도 표기 근거**: 파일 수는 4 지만 신규 SSOT 파일 + 워크플로우 Phase 2 개 신설 + E3 게이트 확장 +
  사실 정정 3 건이 한 스프린트에 섞여 조건 수가 복잡 밴드다.

## 회귀 게이트

- 사실 정정 3 건은 "새 서술 추가" 가 아니라 **옛 서술 잔존 0 건 증명**으로 판정한다. 사전 출력
  (F6 = 1 · F7 = 1) 이 discriminating 근거다 — 변경 전에는 FAIL 이다.
- **E3 게이트는 서술 존재가 아니라 실행 결과로 잰다.** SK-03 은 게이트 스크립트를 SKILL.md 에서
  추출해 **금지 키를 심은 픽스처와 깨끗한 픽스처 양쪽에 실제로 돌리고** exit code 를 확인한다.
  "게이트 문구가 있다" 는 오라클이 아니다 (직전 사이클 25/25 PASS + 기능 파손 선례).
- **substring 오탐 사전 확인 2 건**: (a) `bed_temperature` 검사가 `bed_temperature_initial_layer` 를
  잡으면 안 된다 → dict 키 정확 일치이므로 오탐 없음을 픽스처로 증명한다 (SK-03).
  (b) 마크다운 인라인 코드 추출은 ` ``` ` 펜스 때문에 페어링이 밀린다 → RE-02 오라클은 펜스를 먼저
  제거한다 (제거 없이 돌리면 KEYS 가 28 → 5 로 붕괴하는 것을 실측했다).
- 모든 오라클을 zsh 와 bash 양쪽에서 실행하고 출력이 같아야 한다 (DG-02). 글로빙 대신 명시 경로/
  `find`/파이썬 `glob` 을 쓴다 (zsh `nomatch` 회피).
- 열거값(경로 수 · 키 수 · 잔존 건수 · 레이어 수 배수)은 타이핑하지 않고 명령으로 계산한다.

## Skill

- [ ] SK-01: Phase 1.9 Failure-Mode Detector 가 신설되고 L1/L2/L3 3 종을 각각 판정·보고하며
      Phase 2 진입 게이트로 걸린다 [exact]
      (측정: `grep -c '^### Phase 1.9 — Failure-Mode Detector' bambu-kit/skills/bambu-print-profile/SKILL.md`
       → `1` (사전 `0`) · 같은 파일에 `Failure-Mode Gate (Phase 2 진입 조건)` 1 건 이상 ·
       Phase 2 진입 조건 줄에 `Phase 1.9 completed` 매치 ·
       §3.8 을 재정의하지 않고 인용하는지: `skill-design-guide.md` **§3.8** 앵커가 Phase 1.9 절 안에 매치)
- [ ] SK-02: Phase 3.0 Supportability Split 이 신설되고 L1 adaptive layer height 를 **notes only**
      로 분기한다 [exact]
      (측정: `grep -c '^#### Phase 3.0 — Supportability Split' bambu-kit/skills/bambu-print-profile/SKILL.md`
       → `1` (사전 `0`) · 같은 절에 `notes only` 와 `adaptive_layer_height` 가 모두 매치 ·
       Phase 3 튜닝 정책의 `adaptive_layer_height` 행이 `❌` 로 시작)
- [ ] SK-03: Phase 4.3 E3 게이트가 금지 키 4 종을 **실행으로** 차단한다 [exact, enumerated]
      (측정: 아래 §SK-03 실행 절차대로 게이트를 SKILL.md 에서 추출해 픽스처 2 종에 실제 실행 ·
       clean 픽스처 → `RESULT: PASS` + exit `0` · 금지 4 키를 심은 픽스처 → `RESULT: FAIL` + exit `1`
       + 금지 키 FAIL 행 4 건 ·
       substring 비충돌: `bed_temperature_initial_layer` 만 있는 픽스처의 금지 키 FAIL 행 `1` 건 ·
       음성 대조: 게이트에서 `FORBIDDEN` dict 를 제거하면 두 번째 픽스처가 `RESULT: PASS` 로 바뀌어야 한다)
- [ ] SK-04: L2 스트링잉 대응이 **건조 우선 게이트 3 단계**로 명문화되고, 온도·fan 자동 변경 금지가
      유지된다 [exact]
      (측정: 대상 파일 `bambu-kit/skills/bambu-print-profile/SKILL.md` ·
       `grep -c 'L2 스트링잉 게이트 예외'` → `1` (사전 `0`) ·
       그 표에 `filament_wipe`, `filament_retraction_length`, `coupon` 3 토큰 매치 ·
       `grep -c '온도를 자동 하향하지 마라'` → `1` (사전 `0`) ·
       기존 금지 보존: `grep -c '사용자 명시 요청 2026-05-16'` → `1` (사전 `1` — 정정이 온도 금지
       규칙을 삭제하지 않았다) ·
       음성 대조: 게이트 표를 지우면 첫 측정이 FAIL 해야 한다)

## Error

- [ ] ER-01: `layer_height` 0.08 의 근거 오귀속이 정정되어 0.12 1 차 권장 + 0.08 미확인 라벨이 된다
      [exact]
      (측정 대상 `bambu-kit/skills/bambu-print-profile/references/surface-recipes.md` ·
       옛 표기 잔존 `grep -c '박스/도구'` → `0` (사전 `1`) ·
       `grep -c '1 차 권장'` → `1` 이상 (사전 `0`) · `grep -c '미확인'` → `1` 이상 (사전 `0`) ·
       측정 대상 `bambu-kit/skills/bambu-print-profile/references/bambu-fields-baseline.md` ·
       `grep -c 'layer_height 0.08-0.12'` → `0` (사전 `1`) ·
       음성 대조: 정정한 행을 옛 문구로 되돌리면 첫 측정이 `1` 로 FAIL 해야 한다)
- [ ] ER-02: `enable_arc_fitting` 과 `resolution` 의 성격 오귀속이 정정된다 [exact, enumerated]
      (측정 대상 `bambu-kit/skills/bambu-print-profile/SKILL.md` ·
       `grep -c '(원통 모델)'` → `0` (사전 `1`) · `grep -c 'G-code encoding'` → `1` 이상 (사전 `0`) ·
       측정 대상 `bambu-kit/skills/bambu-print-profile/references/surface-recipes.md` ·
       `grep -c 'Z 계단의 주 해결책이 아니다'` → `1` 이상 (사전 `0`) ·
       음성 대조: `resolution` 행에서 그 문구를 지우면 마지막 측정이 `0` 으로 FAIL 해야 한다)

## Architecture

- [ ] AR-01: 변경이 정확히 4 경로로 한정된다 [exact, enumerated]
      (Given: 커밋 직전 working tree (untracked 포함) ·
       측정: `git status --porcelain -- bambu-kit | awk '{print $NF}' | LC_ALL=C sort` 결과가
       `bambu-kit/skills/bambu-print-profile/SKILL.md`,
       `bambu-kit/skills/bambu-print-profile/references/bambu-fields-baseline.md`,
       `bambu-kit/skills/bambu-print-profile/references/failure-recipes.md`,
       `bambu-kit/skills/bambu-print-profile/references/surface-recipes.md` 4 행과 정확히 일치)
- [ ] AR-02: `bambu-fields-baseline.md` §10 에 L1/L2/L3 + 금지 키가 **전수** 백틱 키로 존재한다
      [exact, enumerated]
      (측정: 아래 §AR-02 스니펫이 `MISSING=0` · `EXPECT` 값은 스니펫이 계산한다 (사전 킷 전체 부재 확인:
       27 키 중 `layer_height`/`resolution` 을 뺀 나머지가 전부 0 파일) ·
       `grep -c '^## 10. 실측 실패 모드 관련 필드' bambu-kit/skills/bambu-print-profile/references/bambu-fields-baseline.md`
       → `1` · 섹션 순서가 `## 9.` → `## 10.` 인지 `grep -n '^## ' | tail -2` 로 확인)
- [ ] AR-03: `failure-recipes.md` 가 신설되고 SKILL.md 파일 트리 · frontmatter description ·
      Phase 3 로드 지시 3 곳에서 참조된다 [exact, enumerated]
      (측정: `test -f bambu-kit/skills/bambu-print-profile/references/failure-recipes.md` → exit `0` ·
       측정 대상 `bambu-kit/skills/bambu-print-profile/SKILL.md` 에서 3 앵커가 각각 매치 —
       (a) 파일 트리 블록 줄 `├── failure-recipes.md`
       (b) frontmatter `description` 의 `references/ 8종` (사전 `references/ 7종` `1` 건 → 정정 후 `0` 건)
       (c) Phase 3 도입부의 `references/failure-recipes.md` 로드 지시)

## Anti-patterns

- [ ] AP-01: 이번 변경이 새로 도입한 URL 이 전부 evidence 파일 또는 변경 전 트리에 실재한다 (날조 0)
      [exact]
      (측정: 아래 §AP-01 스니펫 출력이 `UNSOURCED_URL=0` ·
       신규 수치 토큰 `0.07`, `0.8`, `auto_brim`, `Spiral` 이 각각
       `.harness/.meta/evidence/phase13.md` 에 매치)
- [ ] AP-03: 이번 변경이 bare code fence 를 새로 도입하지 않는다 [exact]
      (측정 — 세 clause 전부. **여는 fence 만 검사 대상이다.** 닫는 fence 는 언어 힌트를 가질 수
       없으므로 세지 않는다:
       (1) `python3 scripts/validate-plugin.py bambu-kit` 의 V6 가 `0 bare` (권위 있는 검사)
       (2) **도입 여부는 diff 가 아니라 파일 상태로 잰다.** diff 기반 fence 계수는 부분 변경 시
           여는/닫는 짝이 어긋나 오탐한다 (v1 결함의 원인). 구현 커밋이 건드린 `bambu-kit` 아래
           마크다운 파일 각각에 대해, `git show <impl>:<파일>` 과 `git show <impl>^:<파일>` 의
           **파일 전문**을 각각 처음부터 상태추적 파싱해 (fence 를 만날 때마다 in/out 토글)
           **언어 힌트 없는 여는 fence** 개수를 센다 — 그 개수가 부모보다 **증가한 파일이 0 건**.
           부모에 없던 신규 파일은 부모 개수를 0 으로 본다
       (3) 신규 파일 `bambu-kit/skills/bambu-print-profile/references/failure-recipes.md` 는
           tracked 가 아니므로 별도 검사 — `grep -c '^```$'` 가 여는 fence 수와 같다)

## Reusability

- [ ] RE-01: 신규 파일이 정확히 1 개이고 신규 디렉토리가 0 개다 [exact]
      (측정: `git status --porcelain -- bambu-kit | grep -c '^??'` → `1` ·
       그 1 건이 `bambu-kit/skills/bambu-print-profile/references/failure-recipes.md` ·
       `find bambu-kit -type d -newer .harness/project.yaml | grep -c .` 결과가 신규 디렉토리 0 임을 뒷받침)
- [ ] RE-02: `failure-recipes.md` 가 새 설정 키를 발명하지 않는다 — 인용한 모든 설정 키가 형제
      references 에 실재한다 [exact]
      (측정: 아래 §RE-02 스니펫이 `MISSING=0` + exit `0` · `KEYS` 값은 스니펫이 계산한다 ·
       스니펫은 ` ``` ` 펜스를 먼저 제거한다 (제거 없이 돌리면 KEYS 가 붕괴함을 실측) ·
       음성 대조: `failure-recipes.md` 에 존재하지 않는 키 `` `zzz_fake_key` `` 를 추가하면
       이 측정이 `MISSING=1` 로 FAIL 해야 한다)

## Diagnostics

- [ ] DG-01: `python3 scripts/validate-plugin.py bambu-kit` 이 V1~V8 전부 OK · exit `0` 이다 [exact]
- [ ] DG-02: 위 모든 grep / git / python 오라클을 zsh 와 bash 에서 실행한 출력이 동일하다 (diff 0)
      [exact]
- [ ] DG-03: SKILL.md 에 임베드된 python 히어독 블록 전부가 `ast.parse` 를 통과한다 [exact]
      (측정: 히어독 블록을 추출해 `ast.parse` — 블록 수는 명령이 계산 · SyntaxError 0 건)

### SK-03 실행 절차

```bash
SP=$(mktemp -d)
mkdir -p "$SP/process" "$SP/filament"
python3 - bambu-kit/skills/bambu-print-profile/SKILL.md "$SP/gate43.py" <<'PY'
import sys, pathlib, re
t = pathlib.Path(sys.argv[1]).read_text(encoding='utf-8')
b = re.findall(r"<<'PY'\n(.*?)\nPY\n", t, re.S)[-1]     # Phase 4.3 게이트 = 마지막 히어독
pathlib.Path(sys.argv[2]).write_text(b, encoding='utf-8')
PY
cat > "$SP/process/clean.json" <<'J'
{"type":"process","name":"X","version":"2.6.0.2","from":"User","inherits":"0.20mm Standard @BBL H2S",
 "print_settings_id":"X","compatible_printers":["Bambu Lab H2S 0.4 nozzle"],
 "layer_height":"0.12","brim_type":"outer_only","elefant_foot_compensation":"0.15","raft_layers":"0"}
J
cat > "$SP/process/bad.json" <<'J'
{"type":"process","name":"Y","version":"2.6.0.2","from":"User","inherits":"0.20mm Standard @BBL H2S",
 "print_settings_id":"Y","compatible_printers":["Bambu Lab H2S 0.4 nozzle"],
 "adaptive_layer_height":"1","bed_temperature":"60","bed_temperature_initial_layer":"65",
 "elephant_foot_compensation":"0.15"}
J
cat > "$SP/process/subonly.json" <<'J'
{"type":"process","name":"Z","version":"2.6.0.2","from":"User","inherits":"0.20mm Standard @BBL H2S",
 "print_settings_id":"Z","compatible_printers":["Bambu Lab H2S 0.4 nozzle"],
 "bed_temperature_initial_layer":"65"}
J
python3 "$SP/gate43.py" "$SP/process/clean.json";   echo "clean_exit=$?"
python3 "$SP/gate43.py" "$SP/process/bad.json";     echo "bad_exit=$?"
python3 "$SP/gate43.py" "$SP/process/subonly.json" | grep -c '금지 키'
```

### AR-02 스니펫

```bash
python3 - <<'PY'
import pathlib, sys
t = pathlib.Path('bambu-kit/skills/bambu-print-profile/references/bambu-fields-baseline.md').read_text(encoding='utf-8')
sec = t[t.index('## 10. 실측 실패 모드'):]
KEYS = """layer_height min_layer_height max_layer_height adaptive_layer_height
filament_retraction_length filament_retraction_speed filament_retraction_minimum_travel
filament_wipe filament_wipe_distance filament_z_hop filament_z_hop_types
brim_type brim_width brim_object_gap raft_layers raft_first_layer_expansion
initial_layer_print_height initial_layer_line_width initial_layer_speed
hot_plate_temp_initial_layer textured_plate_temp_initial_layer eng_plate_temp_initial_layer
additional_cooling_fan_speed close_additional_fan_first_x_layers
bed_temperature bed_temperature_initial_layer elephant_foot_compensation""".split()
miss = [k for k in KEYS if ('`%s`' % k) not in sec]
print("EXPECT=%d MISSING=%d" % (len(KEYS), len(miss)))
for m in miss: print("  MISSING", m)
sys.exit(1 if miss else 0)
PY
```

### RE-02 스니펫

```bash
python3 - <<'PY'
import re, pathlib, sys
d = pathlib.Path('bambu-kit/skills/bambu-print-profile/references')
strip = lambda t: re.sub(r'(?ms)^```.*?^```\s*$', '', t)   # 펜스 제거 — 인라인 페어링 오염 방지
fr = strip((d / 'failure-recipes.md').read_text(encoding='utf-8'))
sib = [p for p in sorted(d.glob('*.md')) if p.name != 'failure-recipes.md']
ssot = ''.join(p.read_text(encoding='utf-8') for p in sib)
keys = sorted({t for t in re.findall(r'`([^`\n]+)`', fr)
               if re.fullmatch(r'[a-z][a-z0-9]*(?:_[a-z0-9]+)+', t)})
missing = [k for k in keys if ('`%s`' % k) not in ssot]
print("SIBLINGS=%d KEYS=%d MISSING=%d" % (len(sib), len(keys), len(missing)))
for m in missing: print("  MISSING", m)
sys.exit(1 if missing else 0)
PY
```

### AP-01 스니펫

```bash
unsourced=0
TMPURLS=$(mktemp)
{ git diff -U0 -- bambu-kit | grep '^+' ;
  cat bambu-kit/skills/bambu-print-profile/references/failure-recipes.md ; } \
  | grep -oE 'https?://[^ )`<>]+' | sed 's/[.,]*$//' | LC_ALL=C sort -u > "$TMPURLS"
while IFS= read -r u; do
  [ -n "$u" ] || continue
  grep -qF -- "$u" .harness/.meta/evidence/phase13.md && continue
  git grep -qF -- "$u" HEAD -- bambu-kit && continue
  printf 'UNSOURCED %s\n' "$u"
  unsourced=$((unsourced + 1))
done < "$TMPURLS"
printf 'UNSOURCED_URL=%s\n' "$unsourced"
```
