---
feature: "카이젠 2026-09-24 Phase 13 계약 — MakerWorld JSON 먼저 · 칸마다 읽기 · 시험 파일 전수 · 빈 옵션 목록 · G-code 길이 재기 · 형상 측정 알려진 답"
slug: kaizen-0924-p13-bambu-kit
created: "2026-09-25 09:05"
complexity: "복잡"
conditions: 29
status: active
owner_session: de8c7935-a5b6-4df5-9106-fafa73c288a0
conditions_digest: sha256:b172964574387cbb
locked_at: "2026-09-25 11:31"
---

## 배경

이 Phase 의 외부 근거는 `.harness/.meta/evidence/phase13.md` 하나다. 처리 배정표(`.claude/kaizen-input/insights-report.md`)에서 `배정` 칸이
`Phase 13` 인 행은 일곱이다(`F30` · `bambu:P1` ~ `bambu:P6`). 다른 Phase 행의 비고가 이 Phase 를 가리키는 것이 둘이다 — `F16`(「킷별 실제 결함은
bambu:P2~P4 …」)과 `F17`(「뱀부 쪽은 bambu:P5 · bambu:P6」). 앞 Phase notes 열둘(`phase1` ~ `phase12`, 2026-09-25 10:22 작업 폴더)에 Phase 13 줄은 `phase3-notes.md:46`(F16 과 같은 말) 하나뿐이고, 러닝북
`Phase 별 추가 과제` 에 Phase 13 줄은 없다. 오케스트레이터 `Phase 별 추가 지시` 에도 Phase 13 은 없다.

배정표 표는 한 줄 요약이다. 행마다 무엇을 고칠지는 배정표를 만든 빈틈 대조 원문에 있다 — 이 세션 스크래치
`/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/insights/gapmap.json` 의 `groups[1]`
(`scope` 첫 줄 「bambu-kit 전체를 봤다」, `findings_reviewed` 여섯 · `proposals` `P1` ~ `P6`). 원문은 bambu-kit 판 `c0e12a8` 에서 재현한 값이고, `c0e12a8..499cc12` 사이에
bambu-kit 을 건드린 커밋은 0 개라 원문의 줄 번호가 그대로 맞는다(2026-09-25 10:22 `git log c0e12a8..499cc12 --oneline -- bambu-kit/ | wc -l` → `0`).
근거 파일 §2 는 bambu:P2 ~ P5 제목을 P1 의 하위 항목으로 달리 붙였다 — 내용은 P1 의 근거로 쓰고, 키 이름은 배정표를 따른다.

이 계약은 앞선 DRAFT 가 `82b2493` 에서 쓰다 멈춘 초안을 이어 쓴 것이다. 워크플로가 이 Phase 를 `499cc12` 에서 다시 시작해 기준 커밋을 그 값으로 옮겼다.
`82b2493..499cc12` 의 커밋 열하나는 모두 Phase 11 · 12 서명이고 `bambu-kit/` · `harness/docs/guides/skill-design-guide.md` · `scripts/` 를 건드린 것은 0 개라
시작 커밋 판 값은 그대로다(같은 날 `git log 82b2493..499cc12 --oneline -- bambu-kit/ harness/docs/guides/skill-design-guide.md scripts/ | wc -l` → `0`).

| 키 | 내용 (배정표 요약 · 원문) | 이번 처리 |
| --- | --- | --- |
| `F30` · `bambu:P1` | 헤드리스 브라우저로 MakerWorld 를 긁다 `Just a moment...` · 403 으로 막혔다(§0-b `d204ea78`). 킷은 특정 브라우저 서버를 1 순위로 두고 「Cloudflare 우회」 라고 적었으며, 실제로 통한 JSON 주소는 킷 어디에도 없었다 | 반영 — 「MakerWorld 읽는 순서」 네 단계 · JSON 주소 셋 · 받는 법 블록, 댓글 두 수와 두 종류, 첨부 찾기 줄 수 먼저, comment-analysis §4.1 · §4.3 · §8 · §10 (SK-01 ~ SK-04) |
| `bambu:P2` | 값 박기(`value[0]` 을 모든 칸에)와 G-code 대조(`split(',')[0]`)가 첫 칸만 읽는다. 재현: 슬롯 2 가 다른 G-code 를 대조하면 `RESULT: PASS` · exit 0, `["25","30"]` 을 박으면 `["25","25"]` | 반영 — 칸마다 대조 · 칸마다 박기 · 두 스크립트 자기 검사 (SC-01 ~ SC-03) |
| `bambu:P3` | 폴더에만 있는 시험 파일 8 개(표에도 실행 줄에도 없음), 표에는 있는데 지운 사본 실행이 빠진 둘, 값 규칙 넷의 FAIL 시험 파일 0 개 | 반영 — 8 개 · 새 4 개를 표와 실행 줄에, 폴더 · 표 · 실행 줄 대조 검사, 빠진 지운 사본 둘 (SC-06). 원문 (e) `bambu-kaizen` 회귀 줄은 범위 밖 — 넘김 |
| `bambu:P4` | 옵션 목록 파일이 있기만 하고 비면 `if CANONICAL:` 이 키 검사를 통째로 건너뛰는데 `[미검증]` 도 없다. 생성기에 최소 개수 검사가 없다. 음성 대조 블록은 게이트를 못 뽑아도 모두 통과처럼 보인다 | 반영 — 게이트 `[미검증]` · 줄 수, 생성기 exit 1, 뽑기 줄 수 확인, 빈 목록 변이 (SC-04 · SC-05 · SC-06) |
| `bambu:P5` | 킷에 G-code 길이를 재는 도구가 없는데 길이 수치를 근거로 쓴다. 세션마다 짠 스크립트가 호(G2 · G3)를 빠뜨렸다(§0-b `d204ea78`) | 반영 — 「G-code 로 길이 재기」 블록(알려진 답 자기 검사 · 호 · E 모드 · 빈 결과 멈춤), 점검 목록 한 줄, surface-recipes 실측 세 곳에 잰 방법 (SK-06) |
| `bambu:P6` | 형상 측정에 빈 결과 assert 만 있고 값이 맞는지 보는 입력이 없다 | 반영 — 가짜 3mf 셋 자기 검사 (SK-05) |
| `F16` · `F17` 비고 | 킷별 실제 결함은 이 Phase 몫 | 위 P2 ~ P6 이 그 결함이다 |

카이젠 스킬 Step 3 의 「관심사 1~2 개」 와 맞춘다: 관심사는 둘이다 — **A 「MakerWorld 를 무엇으로 읽나」**(F30 · P1)와 **B 「검사 · 측정이 조용히 통과로 보이는 자리」**
(P2 ~ P6 — 첫 칸만 읽기 · 안 도는 시험 파일 · 빈 목록 · 호 빠짐 · 정답 모르는 측정). 파일이 여럿이어도 관심사 둘이다(Step 3 「unit 수 기준」). 같은 스킬 Step 3 단서
「오케스트레이터가 특정 결함 목록을 지정한 사이클은 그 범위를 우선한다」 에 따라 배정표 일곱 행을 모두 싣는다.

이번 사이클 Phase 1 가이드 변경과 이 킷(오케스트레이터 Gotcha 「Phase 1 에서 가이드를 변경했으면 전수 체크」):

| 변경 | 이 킷의 자리 | 처리 |
| --- | --- | --- |
| skill-design-guide §3.7 알려진 답 대조 | 이번에 새로 짜는 측정 셋 — G-code 길이 · 형상 측정 자기 검사 · 받은 댓글 세기 | 반영 — 앞 둘은 킷 안에 알려진 답을 싣고(SK-05 · SK-06), 셋째는 계약 측정이 알려진 답(근거 파일 §2 페이지 표)으로 잰다(SK-02) |
| §3.7 `[미검증]` 네 칸 | 생성 측 자리 다섯 — 시작 커밋 `SKILL.md:806` · `:1072` · `:1209` · `:1706` · `references/failure-recipes.md:150` | 미반영 — 관심사 셋째가 된다. Phase 1 넘김 목록에 bambu-kit 이 없었다. 다음 사이클 (ER-03 넘김) |
| §3.7 작업 자체를 못 한다고 하기 전 네 칸 | 「MakerWorld 읽는 순서」 4 번(사용자 입력) | 네 단계를 다 거친 뒤에만 사용자에게 묻게 했다 — 막는 것(상태 코드)과 시도한 우회(2 · 3 번)가 절차에 들어 있다 |
| agent 가이드 §10 | bambu-kit 에 에이전트가 없다 | 해당 없음 |

## 리서치 소스

외부 조회 0 회. 아래 URL 은 전부 근거 파일 `.harness/.meta/evidence/phase13.md` 에서 가져왔다. 러닝북대로 MakerWorld 주소를 새로 부르지 않았다.

- MakerWorld JSON 주소 셋 `[관측 2026-09-24]` — [design/1186414](https://makerworld.com/api/v1/design-service/design/1186414) ·
  [instances](https://api.bambulab.com/v1/design-service/design/1186414/instances) ·
  [commentandrating offset 0](https://api.bambulab.com/v1/comment-service/commentandrating?designId=1186414&offset=0&limit=100) ·
  [offset 100](https://api.bambulab.com/v1/comment-service/commentandrating?designId=1186414&offset=100&limit=100) — 세 주소 200,
  `commentCount` 190 · `total` 159, 페이지 표(offset 0 → hits 100 · comment 44 · ratingItem 56, offset 100 → 59 · 0 · 59, offset 159 → 0) (SK-01 ~ SK-04)
- [3MF Core 1.4.0](https://github.com/3MFConsortium/spec_core/blob/1.4.0/3MF%20Core%20Specification.md) — `<model>` 은 `<resources>` 와 `<build>`, 출력 대상은
  `<build><item objectid>`, 기본 단위 mm. 가짜 3mf 를 파이썬 몇 줄로 만드는 방식과 맞는다 (SK-05)
- 근거 파일 §2 bambu:P6 의 산술 — 10 mm 정육면체 둘레 40 · 2 mm 기둥 8 · 벽 1 mm 관 `WALL_LOOPS=2` 예산 `0.42×2 + 0.45×2×1 = 1.74` · 부족 비율 1.0 · 최소 살 1.0 (SK-05)

근거 파일이 스스로 밝힌 한계를 그대로 옮긴다: 세 주소의 공식 스키마 · 안정성 · 요청 횟수 제한 문서는 없다 — 킷에 `[관측 2026-09-24]` 로 적는다(SK-01).
`commentCount` 와 `total` 이 무엇을 세는지 근거가 없다 — 멈추지 말고 둘 다 적게 한다(SK-03 · SK-04). 403 에서 기다리지 말라는 MakerWorld 공식 지침은 없다 —
「이 킷의 운영 규칙」 이라고 적는다(SK-01). 3mf 받기의 로그인 요구는 확인하지 못했다 — 「로그인이 필요하다」 로 단정하지 않고 「실패하거나 로그인을 요구하면」 으로 쓴다(SK-01).
가짜 3mf 자기 검사는 근거 파일 수집 때 실행하지 못했다(§5) — 이 초안이 실행했다(SK-05 봉인 전 실측).

근거 파일 밖에서 쓴 사실: G-code 의 기능 표시가 `; FEATURE: <이름>` 이라는 것은 이 맥 설치본 실행 파일 문자열에서 확인했다(2026-09-25 `grep -a -o '[ -~]\{0,12\}FEATURE[ -~]\{0,20\}'` —
BambuStudio 02.08.02.61 · OrcaSlicer 2.4.2 둘 다 ` FEATURE: ` 2 건). 킷 문장은 이 표시가 없으면 멈추게만 하고, 표시의 공식 정의를 주장하지 않는다.

내부 입력: 데이터 풀 §0 처리 배정표 · §0-b (`d204ea78` · `be3037df` · `bcf7a121`) · §0.5 bambu 그룹(주입 3 건 — 출력 시간 · 건조 · 품질 베이스, 이번 변경과 무관해 배경만) ·
빈틈 대조 원문(gapmap `groups[1]`) · 앞 Phase notes 열둘. `validate-plugin.py bambu-kit` 는 시작 커밋에서 V1 ~ V10 전부 OK(V2 는 SKIP) 였다.

## GAP 분석 · 개선안 초안

### 1.1 복잡도 4 축

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 4 — 스킬 문서 · 참조 문서 둘 · 옵션 목록 생성 스크립트 · 시험 입력 |
| 공개 API·계약 변경 | 외부에 노출된 형태가 바뀌는가 | 예 — G-code 대조 출력(`MISMATCH <키> 슬롯 <i>`), 게이트 `OPTION LIST` 줄 · 새 `[미검증]` 줄, 생성기 종료 코드, 값 박기가 칸 수가 맞지 않으면 멈춤 |
| 소비면 존재 | 이 형태를 받아 쓰는 반대편이 있는가 | 예 — 아래 Counterpart 표 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 게이트는 모든 산출물이 지나가는 자리, 값 박기는 사용자 3mf 를 만든다, 음성 대조 블록은 23 개 시험 파일을 돈다 |

넷 가운데 셋이 「예」 이고 공개 형태 변경과 소비면이 둘 다 「예」 라 **복잡**이다. Step 2.5 Counterpart 조건을 넣는다(SC-01 · SC-04 · SC-05 · AR-02).
기능 조건은 20 개다 — 복잡 9~20 안이다(SKILL.md Step 6.2 둘째 명령으로 이 파일을 세면 20).

### 1.2 설정 리터럴 대조표

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A 사유에 그대로 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A 사유에 그대로 |
| `diagnostics.ide_exclude` | `[]` | DG-02 에 그대로 |
| `contract_categories[].id` / `prefix` | `Skill`/`SK` · `Script`/`SC` · `Error`/`ER` · `Architecture`/`AR` | 조건 섹션 제목과 접두 그대로 |
| `anti_patterns[].id` / `message` | AP-01 · AP-02 · AP-03 · AP-04 | AP-01 · AP-03 · AP-04 선별, message 원문 그대로. AP-02(force push)는 이 Phase 가 밀어 넣지 않아서 뺀다 |

### 1.4 편집 전 감사 (실제로 읽은 줄 — `82b2493` 판. bambu-kit 은 시작 커밋 `499cc12` 와 같다)

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 |
| --------- | ---------------------------- | ------------------- | ----------- |
| `bambu-kit/skills/bambu-print-profile/SKILL.md` | `:63` (Phase 1 입력 분기) | 특정 브라우저 서버 이름 1 순위 · 「Cloudflare 차단을 우회」 | SK-01 |
| 같은 파일 | `:377-405` (전체 크롤링 원칙 · 첨부 찾기) | 댓글 수를 스냅샷 헤딩에서만, 50+ 는 sampling, 링크 grep 이 `<snapshot-yml>` 에만 — 파일이 없어 나온 0 을 「첨부 0 개」 로 읽을 수 있다 | SK-03 |
| 같은 파일 | `:2097-2104` (MakerWorld URL fallback 체인) | 브라우저 → Codex 캐시 · 웹검색 → WebFetch → 사용자, JSON 주소 0 | SK-01 |
| 같은 파일 | `:118-137` · `:130-336` (형상 측정) · `:339-344` (래티스 실측) | 빈 결과 assert 만(`:299` · `:306` · `:330`), 값 대조 없음 | SK-05 |
| 같은 파일 | `:1456-1486` (옵션 목록 읽기) · `:1562` (`if CANONICAL:`) | 빈 목록이면 키 검사가 소리 없이 꺼짐 | SC-04 |
| 같은 파일 | `:1708-1831` (음성 대조 절 — 표 `:1722-1734` · 실행 블록 `:1748-1812`) | 표 11 행 · 실행 줄 11, 폴더 19 개 중 8 개 누락, `process-thin-unreadable-slot` 의 지운 사본 실행 없음, `filament-unreadable-slot` 알림 줄은 `drop()` 이 못 바꿈, `drop()` 은 f 없는 문자열과 `if` 한 줄 검사를 못 바꿈, 게이트를 못 뽑아도 exit 0 | SC-06 |
| 같은 파일 | `:1877-1921` (값 박기) · `:1927-1977` (G-code 대조) · `:1980-1983` (명령줄 자르기) | 첫 칸만 읽기 · 자기 검사 없음 · 길이 재는 블록 없음 | SC-01 · SC-02 · SC-03 · SK-06 |
| 같은 파일 | `:2052-2095` (Gotcha 체크리스트 48 줄) · `:1002` (`enable_arc_fitting` 기본값 유지) · `:2062` (`nozzle_temperature`) | 체크리스트는 추가만 허용(카이젠 Gotcha 5), 사용자 정책 줄 유지(Gotcha 3) | SK-06 · SK-07 |
| 같은 파일 | `:49` (2026-08-13 카이젠 변경 노트) · `:2172-2182` (출처) | 이번 변경 노트 · 출처 줄 없음 | ER-01 (URL) |
| `bambu-kit/skills/bambu-print-profile/references/comment-analysis.md` | `:3` · `:131-148` (§4.1) · `:164-176` (§4.3) · `:314-320` (§8) · `:333-338` (§10) | 브라우저 서버 도구 이름 셋, 50+ sampling, 옛 체인, API 미해결 | SK-04 |
| `bambu-kit/skills/bambu-print-profile/references/surface-recipes.md` | `:3` · `:188-206` (갭필 표) · `:270-288` (허공 위 표) · `:305-311` (다림질 문단) | G-code 에서 잰 길이에 잰 방법이 없다 | SK-06 |
| `bambu-kit/scripts/option-key-probe/generate-option-list.py` | 전체 98 줄 (`:94-98` 쓰기 뒤 세기) | 판정 프로그램이 빈 출력을 내도 파일을 쓴다 | SC-05 |
| `bambu-kit/scripts/option-key-probe/build-option-list.sh` (읽기만) | `:11` (`set -euo pipefail`) · `:96` (생성기 호출) | 생성기 exit 1 이면 이 스크립트가 멈춘다 — 소비면이 받는다 | SC-05 |
| `bambu-kit/evals/gate-fixtures/` (읽기만 · 새 파일 넷) | 19 개 전체 — 시작 판 게이트로 19 개를 돌린 출력 | 8 개가 표 · 실행 줄 밖. 그 8 개는 지금도 기대대로 돈다(6 FAIL 1 건 · 2 PASS) | SC-06 |
| `.claude/skills/bambu-kaizen/SKILL.md` (읽기만) | `:14-22` (Gotchas) · `:54-66` (Step 2 · 3) · `:68-78` (Step 4) | Step 2 「fallback 체인 · Cloudflare」 · Step 4 회귀 검증에 음성 대조 블록 없음 — 범위 밖 | ER-03 넘김 |
| `harness/docs/guides/skill-design-guide.md` (읽기만) | `§3.7` 알려진 답 대조 소절 · 5 조항 3 항 네 칸 | 킷이 인용할 원문 | AR-02 |

구현 후보가 둘 이상이었던 곳의 선택:

- **읽는 순서 1 순위.** 브라우저 대 JSON. **JSON.** 근거 §2 — 세 주소 200, 브라우저는 403. 브라우저는 JSON 에 없는 사진만 보는 2 번으로 내린다
- **WebFetch 단계.** 남길지 뺄지. **뺀다.** 모델 페이지 WebFetch 는 JSON 주소 `curl` 이 대신하고, 근거 파일은 WebFetch 로 JSON 주소를 부른 기록이 없다(셸 `curl` 만)
- **댓글 받기.** 절차 문장만 대 블록. **블록.** 끝까지 넘기기 · 멈춤 규칙을 사람이 매번 짜면 P5 와 같은 실수가 난다. 다만 답글 배열 이름은 근거 파일에 없어 블록이 세지 않고 문장으로 읽게 한다
- **첨부 찾기.** 스냅샷 grep 대 받은 JSON grep. **받은 JSON 의 문자열을 풀어서 grep.** JSON 이스케이프(`\"` · 줄바꿈)를 풀어야 링크가 맞게 잡힌다. 줄 수를 먼저 찍는다
- **자기 검사 자리.** 측정 코드 안에 넣기 대 SKILL.md 에서 뽑아 따로 돌리기. **뽑아 돌리기.** 근거 §4 6 · 7 번과 같다. 측정 코드를 건드리지 않아 회귀 위험이 없고, 음성 대조 절과 같은 뽑기 방식이다
- **값 박기 칸 수가 다를 때.** 첫 칸 복사 대 멈춤. **값이 한 가지면 채우고, 칸마다 다르면 멈춤.** 어느 칸이 어느 압출기인지 모르고 박으면 틀린 값이 조용히 들어간다
- **G-code 대조 칸 수가 다를 때.** FAIL 대 알림. **짧은 쪽까지 비교하고 남는 칸은 WARN.** 원문 제안과 같다 — 뱀부 3 칸 · 오르카 2 칸처럼 정상적으로 다를 수 있다
- **빈 옵션 목록.** FAIL 대 `[미검증]`. **`[미검증]`.** 목록이 없을 때와 같은 등급이다 — 「이 줄이 있으면 완료를 선언하지 않는다」 가 이미 있다
- **새 값 규칙 시험 파일.** 원문 넷(유량비 · scarf · 소재 부모값 · 공차 음수). **넷.** 금지 키 · compatible_printers · 메타필드 · 숫자 타입은 다음 차례로 적는다(킷 문장 · notes)
- **`drop()` 이 못 바꾸는 둘.** `drop()` 을 넓히기 대 전용 변이 줄. **`drop()` 은 `f?` 만 넓히고(f 없는 문자열), `if` 한 줄 검사와 `unverified` 알림은 전용 변이 줄.** 정규식을 더 넓히면 다른 줄까지 걸린다 — 전용 줄마다 바뀐 줄 1 을 찍는다
- **`[미검증]` 네 칸.** 이번에 할지. **다음 사이클.** 관심사 셋째가 된다 — 위 표

### Counterpart — 바뀌는 형태를 받아 쓰는 반대편

| 파일 | 인용 | 이번 처리 |
| --- | --- | --- |
| `SKILL.md` §4.2 notes 틀 `# 4. 임포트 + 출력 절차` 7 번 | 「보낸 G-code 를 생성 설정과 대조한다 — `MISMATCH` 가 있으면 멈춘다」 | `MISMATCH` 로 시작하는 줄이 그대로라 읽기만 — SC-01 |
| `SKILL.md` 음성 대조 절 「실측 2026-09-15」 블록 | 게이트 출력 모양(`FAIL` · `[미검증]` · `RESULT`) | 그 날짜의 기록이라 고치지 않는다. 새 `OPTION LIST` 줄 수는 SC-04 가 잰다 |
| `bambu-kit/scripts/option-key-probe/build-option-list.sh:96` | 생성기를 부른다 (`set -euo pipefail`) | 생성기 exit 1 이면 멈춘다 — 읽기만. SC-05 |
| `bambu-kit/skills/bambu-print-profile/references/bambu-fields-baseline.md:363` | 「목록이 없는 버전은 게이트가 `[미검증]` 으로 보고」 | 빈 목록도 같은 보고가 되어 문장과 맞는다 — 읽기만 |
| `.claude/skills/bambu-kaizen/SKILL.md` · `.claude/skills/bambu-research/SKILL.md` · `docs/bambu-kit/bambu-print-profile.html` | 옛 읽는 순서 · 「Cloudflare 우회」 | 이 Phase 범위 밖 — 명시적 미완으로 넘긴다 (ER-03) |
| 안 올라간 가지 `feat/bambu-kit-orca-h2s-feedback` (QA 승인) | 같은 SKILL.md 의 4.3 · 음성 대조 표 · 4.4 를 고친다 | 이 Phase 는 그 가지를 합치지 않는다(다른 기능 · 다른 계약). 다시 올릴 때 SKILL.md 충돌을 풀어야 한다고 넘긴다 (ER-03) |

### 개선안 초안

정확한 문구는 스크래치 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p13d/mock.py`
(sha256 앞 16 자리 `2ae88ae777c4f1d8`)가 시작 커밋 판에 적용하는 32 치환 · 새 파일 넷 그대로다(`python3 mock.py <트리>` — 옛 문자열이 정확히 한 번 있어야 적용하고,
아니면 `MOCK_FAIL` 로 멈춘다). BUILD 는 `mock.py` 를 작업 폴더에 그대로 돌린다(`mock applied 36` 이 나와야 한다 — 치환 32 와 새 파일 4 를 합친 수).
돌리기 전에 `git status --short -- bambu-kit` 가 빈 출력인지 본다 — 두 번째 실행은 첫 치환에서 `MOCK_FAIL` 로 멈추고, 중간에 멈추면 앞서 쓴 파일이 남는다. 요지:

- SKILL.md — Phase 1 입력 분기 한 줄, 전체 크롤링 원칙(댓글 두 수 · 두 종류 · 답글 · 브라우저는 JSON 을 못 받을 때만 · 페이지 넘기기), 첨부 찾기(받은 JSON 문자열 풀기 · 줄 수 먼저),
  끝 절을 `## MakerWorld 읽는 순서` 로 바꿈(네 단계 · 운영 규칙 · `### JSON 주소` 표 · 받는 법 블록), 형상 측정 자기 검사(표 · 블록), 4.3 게이트 옵션 목록 줄 수와 빈 목록 `[미검증]`,
  음성 대조 절(제목 날짜 · 일곱 모두 문장 · 표 12 행 · 뽑기 확인 · 폴더 · 표 · 실행 줄 대조 · 실행 줄 12 · `drop()` `f?` · 지운 사본 줄 · 전용 변이 둘 · 빈 목록 변이 · 끝 문장),
  값 박기 칸마다, G-code 대조 칸마다, 두 스크립트 자기 검사, `G-code 로 길이 재기` 블록, 체크리스트 한 줄, 머리 변경 노트, 출처 한 줄
- comment-analysis.md — 머리 날짜, §4.1 JSON 먼저 · 50+ 도 전수, §4.3 첫 줄(앞에 빈 줄 하나 — 목록 앞 빈 줄 경고), §8 첫 줄, §10 첫 줄
- surface-recipes.md — 머리 날짜, 잰 방법 두 줄짜리 인용을 세 곳에
- generate-option-list.py — 다섯 종류 중 0 줄이 있으면 쓰지 않고 exit 1 (세기를 쓰기 앞으로)
- 새 시험 파일 넷 — 목표 위반 하나씩, 나머지는 정상값

## 범위 경계

- 이 Phase 시작 HEAD: `499cc1289f0f5ae5649da601515725f49f4f1096`. 범위 상한은 개정 파일 `.harness/sprint-amendments-kaizen-0924-p13-bambu-kit.md` 의 `end_sha:`
  마지막 값이다. 여러 Phase 가 같은 가지 `kaizen/2026-09-24` 에 동시에 커밋하므로 `HEAD` 로 재지 않는다
- 고치는 파일은 여덟이다(새 시험 파일 넷 포함) — 아래 블록이 그 목록이다(`harness/README.md` §커밋 안전 훅 이 정한 범위 선언 자리). `.harness/` 쪽은 이 계약 · 개정 파일 ·
  QA 피드백 · `.harness/.meta/kaizen-0924/phase13-notes.md` · `.harness/.meta/kaizen-0924/phase13-review.md` 를 쓴다 — 슬러그를 나열하지 않고 AR-01 셋째 값 `verify_seal` 로 잰다.
  AR-01 다섯째 값이 이 블록과 측정 공통 정의의 `FILES` 가 같은지 잰다

```text
# sprint-scope
bambu-kit/skills/bambu-print-profile/SKILL.md
bambu-kit/skills/bambu-print-profile/references/comment-analysis.md
bambu-kit/skills/bambu-print-profile/references/surface-recipes.md
bambu-kit/scripts/option-key-probe/generate-option-list.py
bambu-kit/evals/gate-fixtures/process-flow-ratio-over.json
bambu-kit/evals/gate-fixtures/process-scarf-ratio-over.json
bambu-kit/evals/gate-fixtures/filament-retraction-over-parent.json
bambu-kit/evals/gate-fixtures/process-elefant-foot-negative.json
.harness/
```

- **이 Phase 의 커밋 메시지에는 전부 `Co-Authored-By` 줄 바로 위에 서명 줄 `Kaizen-Phase: kaizen-0924-p13-bambu-kit` 한 줄을 넣는다** (봉인 커밋 포함).
  AR-01 · ER-03 · DG-01 · DG-04 · DG-06 이 이 줄로 이 Phase 커밋을 가린다(`harness/references/contract-schema.md` §여러 주체가 한 가지에 커밋할 때 선택지 B).
  서명을 빠뜨린 커밋은 서명 줄 목록에 안 보이므로 AR-01 첫째 값과 ER-03 넷째 값은 경로로 직접 센다.
  FIX 가 커밋을 더할 때도 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다(옛 줄은 지우지 않는다). notes 커밋도 이 Phase 커밋이다 — notes 를 커밋한 뒤 그 sha 로
  `end_sha:` 줄을 하나 더 덧붙여 커밋한다
- 구현 커밋은 `git add -- <파일…> && git commit -o -- <파일…>` 로 여덟 파일만 싣는다. 새 시험 파일 넷은 `add` 가 먼저다. 한 커밋에 킷 하나(bambu-kit)다
- 측정이 기대는 제목 · 줄 머리는 이름을 바꾸지 않는다: `## MakerWorld 읽는 순서` · `### JSON 주소` · `### Phase 1 — 모델 컨텍스트 추출` · `#### Phase 1.0` · `**전체 크롤링 원칙` ·
  `### Phase 1.5` · `**측정 전에 알려진 답으로 한 번 돌린다` · `# bambu-kit geometry-class probe` · `실측 (2026-09-07 래티스 통` · `#### 음성 대조` · `**두 스크립트 자기 검사 (2026-09-25 신규)**` ·
  `보내기 전에 명령줄로 잘라` · `**G-code 로 길이 재기 (2026-09-25 신규)**` · `### Phase 5` · `# 제작자 3mf 의 프로젝트 설정에` · `# 슬라이서가 실제로 쓴 설정` · `# G-code 로 기능별 압출 길이를 잰다` ·
  `ID=<모델 번호>; OUT=<output_dir>/makerworld` · `python3 - "$OUT" > "$OUT/strings.txt"` · `T=$(mktemp -d -t probe)` · `T=$(mktemp -d -t slots)` · `GATE=$(mktemp -t gate)` (SKILL.md) ·
  `### 4.1 댓글 받기 — JSON 먼저, 50+ 도 전수` · `### 4.3` · `## 8. Fail-soft 정책` · `## 10. 미해결 / 검증 필요` (comment-analysis) · `## 3.7.` (skill-design-guide — 읽기만).
  이름이 바뀌면 `sect` · `ext` · `pyblock` 이 빈 글을 내 값이 0 이 되거나 `BLOCK_MISSING` 이 나온다 — FAIL 쪽으로 틀린다
- 공유 파일(`.claude-plugin/marketplace.json` · `bambu-kit/.claude-plugin/plugin.json` 버전 · 루트 `README.md` · 루트 `CLAUDE.md` · `docs/` 전체 · 처리 배정표 · 감사 로그 ·
  실패 횟수 파일 · `.github/workflows/ci.yml`)과 다른 Phase · 레포 전용 파일(`harness/` · `scripts/` · `.claude/skills/`)과 `bambu-kit/README.md` 는 건드리지 않는다 — ER-03 넷째 값.
  bambu-kit README 의 AUTO 구간은 스킬 frontmatter 를 읽는데 frontmatter 를 바꾸지 않는다(AP-04). 문서 사이트 재생성은 Final F2 몫이라 DG-06 에서 `docs-site-regen` 을 뺀다
- 안 올라간 가지 `feat/bambu-kit-orca-h2s-feedback`(워크트리 `bambu-orca-h2s-feedback`, QA 승인)은 합치지 않는다. 그 가지가 같은 SKILL.md 자리를 고치므로 다시 올릴 때 충돌을 푼다는 것을
  notes 넘김에 적는다(ER-03)
- QA(`harness:qa-evaluator`)는 설치본이다 — 이 Phase 가 고치는 파일에 harness 파일은 없다
- 사용자 승인(Step 5) 대체: 사용자가 「자동으로 끝까지 알아서 진행해 내 허락이 필요한건 코덱스로 리서치나 검토받고」라고 위임했다(세션
  `de8c7935-a5b6-4df5-9106-fafa73c288a0` 기록 queued_command `2026-09-24T04:04:16.964Z`). Codex 사용량 한도가 소진돼(오류 원문 「You've hit your usage limit … try
  again at 11:05 PM」, 2026-09-24) 독립 Claude 검토자(REVIEW 에이전트)가 대신한다. 이어 사용자가 「코덱스 대신에 그냥 너가 알아서 진행하라고」라고 명시했다(같은 세션
  기록 user `2026-09-24T11:54:58.940Z`). 검토 결과 파일: `.harness/.meta/kaizen-0924/phase13-review.md`
- 검토 VERDICT: 1 회차 `CHANGES`(고칠 것 넷 — SC-06 실행 줄 확인이 파일 하나를 놓침 · SK-06 알려진 답이 회전 방향 버그를 통과시킴 · SK-06 줄 수 표기 ·
  DG-06 빈 출력) → 초안 작성자가 넷 다 반영. 2 회차 `CHANGES`(1 회차 반영은 모두 확인, 새로 하나 — SK-06 알려진 답이 방향을 무시한 호 계산을 통과시킴) →
  BUILD 가 검토 문구 그대로 반영했다(SK-06 조건 줄 · `m.sh` `mutated_abs` · `mock.py` `KNOWN` · 회귀 게이트 표 SK-06 행 · `mock.py` sha256). 3 회차 검토는 돌리지 않았다 —
  워크플로 지시(남은 지적을 반영하거나 반영하지 않는 이유를 이 절에 적은 뒤 진행)대로, 반영 뒤 예행 저장소를 다시 만들어 조건 전부 · 문장 삭제 46 · 대조 21 · 변형 다섯을
  다시 돌려 요구값과 줄마다 맞는 것을 봤다(`회귀 게이트` 절 끝 문단)
- 검토 권고 가운데 반영한 것: 2 회차 DG-06 문구(`doc_checked` 1 이상을 상태와 상관없이 요구 — 요구값 줄과 맞춤). 반영하지 않은 것과 이유 —
  (1) SK-02 에 모델 주소 403 경우 더하기: 권고이고, 검토자가 가짜 `curl` 로 그 경우 블록이 요청 4 번 뒤 `FAIL` · 종료 코드 1 로 멈추는 것을 이미 봤다. 측정 경우로 넣는 것은
  notes 다음 사이클 메모로 넘긴다 (2) 킷 블록이 임시 파일을 안 지움: 이번에 안 고친 블록까지 같은 모양이라 새 블록 하나만 지우면 규칙이 갈린다 — 다음 사이클 메모
  (3) `wc -l` 앞 공백: 고치면 SC-06 요구값도 바꿔야 한다 — 검토자 판단대로 둔다 (4) ER-03 넷째 값 경로 목록에 다른 킷 폴더: 넣으면 동시에 도는 다른 Phase 의
  서명 누락이 이 조건을 떨어뜨린다 — 검토자 판단대로 둔다
- 오라클 한계: 실제 MakerWorld 주소는 부르지 않는다(러닝북 — curl 로 새 자료를 찾지 마라). SK-02 · SK-03 은 근거 파일 §2 의 관측 모양(페이지 표 · 필드 이름)을 흉내 낸
  가짜 `curl`(`fakecurl.sh`)로 받는 법 블록을 돌린다 — 응답 모양이 실제로 바뀌면 이 측정은 못 잡는다. 킷 문장이 `[관측 2026-09-24]` 로 그 한계를 적는다
- 오라클 한계: SC-04 · SC-06 은 이 맥의 설치본 BambuStudio `02.08.02.61` · OrcaSlicer `2.4.2`(준비 단계 실측 2026-09-25 `defaults read … CFBundleShortVersionString`)와
  그 옵션 목록 파일에 기댄다. 버전이 바뀌면 옵션 목록 파일이 없어 게이트가 `[미검증]` 을 내고 값이 달라진다 — QA 는 설치본 버전을 먼저 본다
- 오라클 해소: SK-01 · SK-03(앞 두 줄) · SK-04 · SK-05(첫 줄) · SK-06(첫 줄 · 점검 목록 · surface-recipes 줄) · SC-03(첫 줄) · SC-06(「일곱 모두」 줄) — 산출물이 문서 문장 자체라
  정해진 절 · 줄에 정해진 문장이 있는지가 판정이다. 시작 커밋 판에서 새 문장 0 · 옛 문장 1 이상을 봉인 전에 확인했고, 문장 하나만 지운 사본 46 개에서 그 조건의 출력이 바뀌었다(`회귀 게이트` 절)
- 오라클 해소: SK-02 · SK-03(뒤 세 줄) · SK-05 · SK-06 · SC-01 ~ SC-06 — 킷의 블록 · 스크립트를 끝 판 사본에서 실제로 돌린 출력이다. 조건마다 알려진 답 · 음성 대조가 m 안에 있다
- 오라클 해소: ER-01 · ER-02 · AP-01 — 편집 전 판과 파일마다 비교한 더한 줄 계산이다. DG-02 — 파일마다 편집 전 판과 규칙별 경고 수를 비교한 값이다. 각각 양성 대조가 붙어 있다
- 오라클 해소: ER-03 · AR-01 · DG-01 · DG-04 · DG-06 — 커밋 기록과 봉인 검증 함수를 실제로 돌린 출력이다. 예행 저장소 변형 다섯이 양성 대조다
- 커버리지 해소: SK-01 ~ SK-07 · SC-01 ~ SC-06 · AR-02 — 산문의 파일 이름은 측정 `m <조건 ID>` 가 공통 정의의 변수(`$SK` · `$CA` · `$SR` · `$GO` · `$SKD` · `$FXD` · `$NF1` ~ `$NF4`)로
  연다(파일과 변수의 대응은 `common.sh` 머리). 토큰은 `m.sh` 의 같은 ID 갈래에 글자 그대로 있다. 읽기만 하는 파일(`harness/docs/guides/skill-design-guide.md` ·
  `bambu-kit/evals/gate-fixtures/` 의 기존 열아홉 · `bambu-kit/.claude-plugin/plugin.json`)은 `m.sh` 갈래 안에 경로 그대로 있다. SK-01 의 `bambu-kit/` 는
  `grep -r` 의 인자(`"$E/bambu-kit"`)다
- 커버리지 해소: RE-01 — 네 파일 이름은 `m RE-01` 이 `comm -13` 으로 낸 새 파일 목록 자체다(측정 출력이 열거다). `bambu-kit/evals/gate-fixtures/` 는 그 파일들의 폴더,
  `x.json` 은 양성 대조 사본에 더한 이름이다
- 커버리지 해소: ER-01 · ER-03 — `.harness/.meta/kaizen-0924/phase13-notes.md` · `.harness/.meta/evidence/phase13.md` 는 공통 정의의 `$NOTES` · `$EVID` 다. ER-03 의 넘김 문자열과
  공유 경로는 `m.sh` `ER-03)` 갈래 `toks` · `not_other` 의 인자다
- 커버리지 해소: AR-01 — `bambu-kit/` 는 `unsigned_on` 의 인자, `.harness/` 는 `scope` 블록 줄과 `verify_seal` 이 도는 폴더다
- 커버리지 해소: AR-02 — `4.1` 은 파일이 아니라 comment-analysis 의 절 번호다. `m AR-02` 가 `^### 4\.1 ` 과 ``references/comment-analysis.md` §4\.1`` 로 센다(정규식이라 점 앞에 역슬래시가 있다)
- 검출기는 공백 든 코드 조각 안의 인자를 읽지 못한다 — 위 해소 줄이 전부 그 경우다
- 편집 전부터 있던 경고(markdownlint MD032 · MD060 · MD031 등)는 고치지 않는다 — DG-02 는 파일마다 규칙별 경고 수가 편집 전 판보다 늘지 않았는지 잰다.
  더한 줄의 경고만 세지 않는다 — 같은 제목 중복(MD024) · 제목 앞뒤 빈 줄(MD022) · 목록 앞뒤 빈 줄(MD032)은 더한 줄 옆의 손대지 않은 줄에 붙는다
  (러닝북 측정 구멍 목록, Phase 7 · 8 · 9 · 11 실측). 옛 측정(더한 줄만 세기)이 0 을 내는데 새 측정이 1 을 내는 사본 둘을 양성 대조로 돌렸다(`회귀 게이트` 절 표 DG-02 행)
- 오라클 한계: DG-02 는 규칙마다 수를 세므로 같은 규칙 안에서 고친 경고와 새 경고가 서로 지우면 못 잡는다. 모의본은 comment-analysis §4.3 목록 앞에 빈 줄을 더해
  그 파일 MD032 를 22 → 21 로 줄였다 — 그 파일에 새 MD032 가 하나 생겨도 수가 22 라 가려진다. 그래서 MD032 양성 대조는 수가 그대로인 surface-recipes 에서 돌렸다
- notes 에 함께 적는다(조건으로는 재지 않는다): 「다음 사이클 메모」 에 둘 — `bambu-kaizen` Step 4 에 음성 대조 블록 실행 줄, 댓글 답글 배열 이름을 다음 실측 때 적기
- 기능 조건 20 · 전체 조건 줄 29
- 사용자가 할 일: 없음

## 회귀 게이트 — 측정 공통 정의와 봉인 전 실측

모든 조건의 측정은 아래 `common.sh` 와 `m.sh` 를 차례로 `.` 으로 읽은 **bash** 셸에서 돈다 — `common.sh` 는 bash 가 아니면 `NOT_BASH` 를 찍고 종료 코드 2 로 끝난다
(Claude Code 의 zsh 는 따옴표 없는 변수를 쪼개지 않고, `path` 가 `PATH` 와 묶여 있다). `m` 은 도우미 함수 · 두 판 폴더 · `fakecurl.sh` · `rule-diff.sh` 가 없으면
`HELPER_MISSING` · `SNAPSHOT_MISSING` 을 내고 멈춘다 — 그래서 조건마다 `type m` 하나로 정의 확인을 대신한다. 킷 블록이 zsh 에서도 도는지는 m 이 `zsh` 를 따로 불러 잰다(SK-02 · SK-03 · SK-05 · SC-03 · SC-06).
예행 값은 bash 5.3.9 와 `/bin/bash` 3.2.57 두 해석기에서 한 글자도 다르지 않았다(`diff` 빈 출력). zsh 에서 `common.sh` 를 읽으면 `NOT_BASH` · 종료 코드 2 다.
네 블록을 각 블록 첫 `#` 주석 줄(셔뱅 다음)의 이름 그대로 한 폴더에 저장하고 그 폴더를 `K` 에 넣는다. `END_UNRESOLVED` 가 찍히면 셸이 종료 코드 2 로 끝난다.
`rule-diff.sh` 옆에는 `node_modules` 를 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p1build/node_modules` 로 잇고
`cfg.markdownlint-cli2.jsonc` = `{ "config": { "MD013": false } }` 를 둔다 — 준비 단계 실측(2026-09-25): 그 자리의 `.bin/markdownlint-cli2 --version` 첫 줄이
`markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)`. 없으면 그 폴더에서 `npm install --no-save markdownlint-cli2@0.23.2` 부터 돌린다.
그 밖의 준비 단계 실측(2026-09-25): `command -v zip unzip` → `/usr/bin/zip` · `/usr/bin/unzip` · `zsh --version` 5.9 · `python3 --version` 3.14.3 ·
설치본 `02.08.02.61` · `2.4.2` · 옵션 목록 두 파일(`references/option-keys/bambu-02.08.02.61.tsv` · `orca-2.4.2.tsv`) 있음.
`common.sh` 의 `R` 은 예행 저장소를 가리킬 때만 쓴다 — 비우면 작업 폴더다. 두 판을 `${TMPDIR:-/tmp}/p13m.XXXXXX` 에 푸니 `TMPDIR` 를 스크래치 폴더로 두고 읽는다
(이 맥 디스크 여유가 2 GB 안팎이라 m 한 번이 두 판 · DG-05 사본으로 약 60 MB 를 쓴다 — 끝나면 `rm -rf "$T"`).

```bash
# common.sh — 측정 공통 정의. bash 로 읽는다 (zsh 는 배열 첨자가 1 부터이고 path 가 PATH 와 묶여 있다)
[ -n "${BASH_VERSION:-}" ] || { echo "NOT_BASH — bash -c 안에서 다시 읽는다"; exit 2; }
export LC_ALL=C.UTF-8   # 번역투 정규식이 글자 단위로 돌아야 한다
cd "${R:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/kaizen-0924}" || exit 2
B=499cc1289f0f5ae5649da601515725f49f4f1096                  # 이 Phase 시작 HEAD
SIG='Kaizen-Phase: kaizen-0924-p13-bambu-kit'
CF=.harness/sprint-contract-kaizen-0924-p13-bambu-kit.md
AM=.harness/sprint-amendments-kaizen-0924-p13-bambu-kit.md
NOTES=.harness/.meta/kaizen-0924/phase13-notes.md
EVID=.harness/.meta/evidence/phase13.md
END=$( [ -f "$AM" ] && sed -n 's/^end_sha:[[:space:]]*//p' "$AM" | tail -1 )
if [ -z "$END" ] || ! git rev-parse -q --verify "$END^{commit}" >/dev/null; then
  echo "END_UNRESOLVED — 측정을 멈춘다. HEAD 로 바꿔 재지 않는다"; exit 2
fi
: "${K:?도우미 폴더를 K 에 넣는다}"
SKD=bambu-kit/skills/bambu-print-profile
SK=$SKD/SKILL.md
CA=$SKD/references/comment-analysis.md
SR=$SKD/references/surface-recipes.md
GO=bambu-kit/scripts/option-key-probe/generate-option-list.py
FXD=bambu-kit/evals/gate-fixtures
NF1=$FXD/process-flow-ratio-over.json
NF2=$FXD/process-scarf-ratio-over.json
NF3=$FXD/filament-retraction-over-parent.json
NF4=$FXD/process-elefant-foot-negative.json
FILES=("$SK" "$CA" "$SR" "$GO" "$NF1" "$NF2" "$NF3" "$NF4")
MDS=("$SK" "$CA" "$SR")
T=$(mktemp -d "${TMPDIR:-/tmp}/p13m.XXXXXX") || exit 2; mkdir -p "$T/B" "$T/E"
# 두 판을 풀어 둔 폴더에서 잰다 — 작업 폴더에 남은 다른 Phase 의 미커밋 변경이 끼지 않는다
git archive "$B" | tar -x -C "$T/B"; git archive "$END" | tar -x -C "$T/E"
# sect <파일> <제목 앞부분> — 그 제목부터 같은 깊이 이하의 다음 제목 전까지. 코드 펜스 안의 `#` 줄은 제목으로 보지 않는다
sect() { awk -v h="$2" '
  /^[[:space:]]*(```|~~~)/ { fence = !fence }
  !f && !fence && index($0, h) == 1 { f = 1; lvl = match($0, /[^#]/) - 1; print; next }
  f && !fence && /^#+ / { l = match($0, /[^#]/) - 1; if (l <= lvl) exit }
  f' "$1"; }
# toks <글> <토큰…> — 토큰마다 글 안에서 그 토큰이 든 줄 수 (빈칸으로 잇고 끝 빈칸은 없다)
toks() { local s="$1" o=""; shift; for t in "$@"; do o="$o $(printf '%s\n' "$s" | grep -cF -- "$t")"; done; echo "${o# }"; }
# ext <파일> <줄 앞부분> — 그 앞부분으로 시작하는 줄이 든 ```bash 블록 전체 (펜스 줄 빼고)
ext() { awk -v p="$2" '
  /^```bash$/ { inb = 1; n = 0; hit = 0; next }
  inb && /^```$/ { if (hit) { for (i = 1; i <= n; i++) print buf[i]; exit } inb = 0; next }
  inb { buf[++n] = $0; if (index($0, p) == 1) hit = 1 }' "$1"; }
# pyblock <파일> <첫 줄 앞부분> — heredoc 파이썬 블록을 그 줄부터 다음 PY 줄 앞까지
pyblock() { awk -v p="$2" 'index($0, p) == 1 {f = 1} f && $0 == "PY" {exit} f' "$1"; }
# gate <트리> — 그 트리 SKILL.md 의 완료 게이트를 뽑은 파일 경로를 낸다 (킷의 음성 대조 절과 같은 뽑기)
gate() { local g=$T/gate.$RANDOM a b
  a=$(grep -n '^TARGET_SLICER=.* python3 - ' "$1/$SK" | head -1 | cut -d: -f1)
  b=$(awk -v s="$a" 'NR>s && $0=="PY" {print NR; exit}' "$1/$SK")
  sed -n "$((a+1)),$((b-1))p" "$1/$SK" > "$g"; echo "$g"; }
# url — 주소 틀의 <번호> · <N> 을 살리려고 `>` 에서 끊지 않는다. 끝의 `>` 와 문장 부호는 뗀다 (<https://…> 자동 링크)
url()   { grep -oE 'https?://[^ )"`]+' | sed -E 's/[>.,;:]+$//' | sort -u; }
# 주소 틀 — <번호> · $ID 는 근거 파일의 관측 모델 번호로, <N> · $OFF 는 0 으로 바꿔 근거 파일 주소와 맞춘다
urlnorm() { sed -E 's/<번호>?/1186414/g; s/\$ID/1186414/g; s/<N>?/0/g; s/\$OFF/0/g'; }
# 편집 전 판에 없는 새 파일은 빈 파일과 비교한다. 끝 판은 m 의 E(대조용 사본이면 그 사본)를 따른다
added() { local e=${E:-$T/E}; for f in "${FILES[@]}"; do if [ -f "$T/B/$f" ]; then git diff --no-index -U0 "$T/B/$f" "$e/$f"; else git diff --no-index -U0 /dev/null "$e/$f"; fi; done | grep '^+' | grep -v '^+++'; }
mine() { git log --format= --name-only "${1}..${2}" --grep="^${3}\$" | grep . | LC_ALL=C sort -u; }
unsigned_on() { _b=${1}; _u=${2}; _s=${3}; shift 3
  git log --format=%H "${_b}..${_u}" -- "$@" | while read -r _c; do git log -1 --format=%B "$_c" | grep -qxF "$_s" || echo "$_c"; done; }
# not_other <base> <상한> <서명> <경로…> — 경로를 건드린 구간 안 커밋 가운데 다른 Phase 서명이 없는 커밋 (0 줄이어야 한다)
not_other() { _b=${1}; _u=${2}; _s=${3}; shift 3
  git log --format=%H "${_b}..${_u}" -- "$@" | while read -r _c; do
    _m=$(git log -1 --format=%B "$_c")
    if printf '%s\n' "$_m" | grep -qE '^Kaizen-Phase: ' && ! printf '%s\n' "$_m" | grep -qxF "$_s"; then continue; fi
    echo "$_c"; done; }
my() { mine "$B" "$END" "$SIG"; }
# scope <계약> — `## 범위 경계` 절 안, 첫 줄이 `# sprint-scope` 인 text 블록의 경로 줄
scope() { awk '/^## /{s=$0} s ~ /^## 범위 경계/ && /^```text$/{b=1; n=0; next} b && /^```$/{b=0; next} b{n++; if (n==1 && $0 != "# sprint-scope") b=0; else if (n>1) print}' "$1"; }
fm_get() { awk -v k="^$2:[[:space:]]*" 'NR==1 && /^---[[:space:]]*$/ { fm=1; next } fm && /^---[[:space:]]*$/ { exit } fm && $0 ~ k { sub(k, "", $0); print; exit }' "$1" | sed -e "s/[[:space:]]*$//" -e "s/^['\"]//" -e "s/['\"]\$//"; }
sha256_16() { if command -v sha256sum >/dev/null 2>&1; then sha256sum; elif command -v shasum >/dev/null 2>&1; then shasum -a 256; else python3 -c 'import hashlib,sys; print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())'; fi | cut -c1-16; }
contract_digest() { grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$1" | sed -E 's/^- \[[ x]\]/- [ ]/' | sha256_16; }
verify_seal() { rec=$(fm_get "$1" conditions_digest); rec=${rec#sha256:}; if [ -z "$rec" ]; then echo "SEAL_ABSENT $1"; return 0; fi
  act=$(contract_digest "$1"); if [ "$rec" = "$act" ]; then echo "SEAL_OK $1"; else echo "SEAL_BROKEN $1 recorded=$rec actual=$act"; fi; }
K02='(을|를) ?(처리|관리)(합니다|한다)|에 대해서?|하도록 (합니다|한다)|에 의(해|하여)|되어 있(는 경우|을 때)|(표시|적용|호출|생성|반환)(됩니다|된다)'
```

```bash
# m.sh — 조건마다 재는 값을 한 줄씩 낸다. common.sh 를 읽은 bash 에서 `m <조건 ID>` 로 부른다
m() {
  local E=${EOVR:-$T/E} S L f n g sh out rc
  # 도우미가 하나라도 없으면 grep -c 가 조용히 0 을 낸다 — 멈춘다
  for fn in sect toks ext pyblock gate url urlnorm added mine unsigned_on not_other my scope fm_get verify_seal; do
    type "$fn" >/dev/null 2>&1 || { echo "HELPER_MISSING $fn"; return 2; }; done
  [ -n "${T:-}" ] && [ -d "$T/B" ] && [ -d "$E" ] || { echo "SNAPSHOT_MISSING"; return 2; }
  for h in fakecurl.sh rule-diff.sh; do [ -f "$K/$h" ] || { echo "HELPER_MISSING $h"; return 2; }; done
  case "$1" in
  SK-01)  # MakerWorld 읽는 순서 — 네 단계 · 403 규칙 · 주소 셋 · Phase 1 입력 분기
    S=$(sect "$E/$SK" '## MakerWorld 읽는 순서')
    toks "$S" '1. **JSON 주소** — 아래 표의 셋을 셸 `curl` 로 부르고 상태 코드를 먼저 본다. 200 이 아니면 다시 부르지 말고 2 번으로 간다.' \
      '2. **브라우저 도구** — 이 세션의 도구 목록에 페이지를 여는 도구가 있을 때만 쓴다. 서버 이름은 환경마다 다르므로 이름을 박지 말고 목록에서 찾는다.' \
      '제목이 `Just a moment...` 이거나 HTTP 403 이면 기다렸다 다시 열지 말고 3 번으로 간다.' \
      '3. **Codex 위임** — 브라우저로 열라고 쓰지 말고, 1 번 주소 셋을 셸 `curl` 로 부르라고 주소를 그대로 적어 넘긴다.' \
      '4. **사용자 입력** — 위가 모두 실패하면' \
      '3mf 는 자동으로 내려받는다고 가정하지 않는다 — 받기가 실패하거나 로그인을 요구하면 다시 시도하지 말고 사용자가 내려받은 `.3mf` 를 달라고 한다.' \
      '403 · `Just a moment...` 에서 기다리지 않는 것은 MakerWorld 공식 지침이 아니라 이 킷의 운영 규칙이다' \
      '### JSON 주소 (`[관측 2026-09-24]`)' \
      '| `https://makerworld.com/api/v1/design-service/design/<번호>` |' \
      '| `https://api.bambulab.com/v1/design-service/design/<번호>/instances` |' \
      '| `https://api.bambulab.com/v1/comment-service/commentandrating?designId=<번호>&offset=<N>&limit=100` |' \
      '`hits` 가 비거나 받은 수가 `total` 에 닿으면 멈춘다'
    echo "heads=$(grep -c '^## MakerWorld 읽는 순서' "$E/$SK") old=$(grep -c '^## MakerWorld URL fallback 체인' "$E/$SK")"
    toks "$(sect "$E/$SK" '### Phase 1 — 모델 컨텍스트 추출')" \
      '1. **MakerWorld URL** → **JSON 주소를 먼저 부른다** (이 파일 끝 「MakerWorld 읽는 순서」).' '**Playwright MCP 1차**'
    # 킷 전체 — 특정 브라우저 서버 이름 · 「Cloudflare 우회」
    echo "names=$(grep -rniE 'playwright|mcp__' "$E/bambu-kit" | grep -c .) bypass=$(grep -rn '우회' "$E/bambu-kit" | grep -ci cloudflare)" ;;
  SK-02)  # 받는 법 블록을 가짜 curl 로 돌린다 — 끝까지 넘기기 · 멈춤 · 두 수 · 403 에서 다시 안 부름
    ext "$E/$SK" 'ID=<모델 번호>; OUT=<output_dir>/makerworld' > "$T/p1.sh"
    [ -s "$T/p1.sh" ] || { echo "BLOCK_MISSING"; return 0; }
    fetch() {  # fetch <블록> <모드> <셸>
      local D; D=$(mktemp -d "$T/f.XXXXXX"); : > "$D/requests.log"
      { cat "$K/fakecurl.sh"; sed -e "s#^ID=<모델 번호>; OUT=<output_dir>/makerworld;#ID=1186414; OUT=$D/mw;#" "${1}"; } > "$D/run.sh"
      FAKE_DIR=$D FAKE_MODE=${2} ${3} "$D/run.sh" > "$D/out" 2>&1; local rc=$?
      echo "${3}/${2:-200} rc=$rc req=$(grep -c . "$D/requests.log") offs=$(sed -nE 's/.*offset=([0-9]+).*/\1/p' "$D/requests.log" | paste -sd, -) [$(grep '^comments total' "$D/out")] note=$(grep -c '^NOTE' "$D/out") warn=$(grep -c '^WARN' "$D/out") fail=$(grep -c '^FAIL' "$D/out")"; }
    fetch "$T/p1.sh" "" bash; fetch "$T/p1.sh" "" zsh; fetch "$T/p1.sh" 403 bash
    # 음성 대조 — 멈춤 조건을 지운 사본은 빈 페이지를 한 번 더 부르고, 첫 페이지에서 멈춘 사본은 WARN 을 낸다
    grep -vxF '  [ "$OFF" -lt "$TOTAL" ] || break' "$T/p1.sh" > "$T/p1-nostop.sh"; fetch "$T/p1-nostop.sh" "" bash
    sed 's/^  OFF=\$((OFF + GOT))$/  break/' "$T/p1.sh" > "$T/p1-onepage.sh"; fetch "$T/p1-onepage.sh" "" bash ;;
  SK-03)  # 댓글 수 · 첨부 — 두 수와 두 종류, 줄 수 먼저, 받은 JSON 에서 링크 찾기
    S=$(awk '/^\*\*전체 크롤링 원칙/{f=1} /^### Phase 1\.5/{exit} f' "$E/$SK")
    toks "$S" '- **댓글 수 확인 (JSON)**: 모델 주소의 `commentCount` 와 댓글 주소의 `total` 을 **둘 다** 적고, 받은 `hits` 수가 `total` 과 같은지 본다.' \
      '두 값이 달라도 멈추지 말고 둘 다 notes 에 적는다' '- **`hits` 원소마다 `comment` 와 `ratingItem` 을 각각 읽는다**' \
      '각 항목 안의 답글 배열도 따로 읽는다' '- **JSON 을 못 받아 브라우저로 읽을 때만**:' \
      '**대상 파일이 비었거나 없으면 링크 0 건은 「첨부 0 개」 가 아니다**' 'wc -l < "$SRC"'
    toks "$S" '<snapshot-yml>' 'Playwright `browser_evaluate`로' '- **댓글 카운트 확인**: 스냅샷에서'
    ext "$E/$SK" 'ID=<모델 번호>; OUT=<output_dir>/makerworld' > "$T/p1.sh"; ext "$E/$SK" 'python3 - "$OUT" > "$OUT/strings.txt"' > "$T/p1a.sh"
    [ -s "$T/p1.sh" ] && [ -s "$T/p1a.sh" ] || { echo "BLOCK_MISSING"; return 0; }
    for sh in bash zsh; do
      D=$(mktemp -d "$T/a.XXXXXX"); : > "$D/requests.log"
      { cat "$K/fakecurl.sh"; sed -e "s#^ID=<모델 번호>; OUT=<output_dir>/makerworld;#ID=1186414; OUT=$D/mw;#" "$T/p1.sh"; cat "$T/p1a.sh"; } > "$D/run.sh"
      FAKE_DIR=$D $sh "$D/run.sh" > "$D/out" 2>&1
      # 받은 JSON 뒤 첫 숫자 줄이 줄 수다 — 링크 줄보다 먼저 나와야 한다
      echo "$sh lines=$(awk '/^ *[0-9]+$/{print $1; exit}' "$D/out") pdf=$(grep -cxF 'https://example.com/manual.pdf' "$D/out") github=$(grep -cxF 'https://github.com/o/r' "$D/out") order=$(awk '/^ *[0-9]+$/{a=NR} /^https:/{if(!b)b=NR} END{print (a && b && a<b) ? 1 : 0}' "$D/out")"
    done
    # 받기 전(빈 폴더) — 줄 수 0 을 먼저 낸다
    D=$(mktemp -d "$T/a.XXXXXX"); mkdir -p "$D/mw"; echo "empty lines=$(OUT=$D/mw bash "$T/p1a.sh" 2>/dev/null | awk '/^ *[0-9]+$/{print $1; exit}')" ;;
  SK-04)  # comment-analysis — §4.1 JSON 먼저 · §4.3 · §8 · §10 · 머리
    sed -n 3p "$E/$CA"
    toks "$(sect "$E/$CA" '### 4.1 댓글 받기 — JSON 먼저, 50+ 도 전수')" \
      'MakerWorld 댓글은 JSON 주소(SKILL.md 「MakerWorld 읽는 순서」)로 **전부** 받는다.' '50+ 여도 sampling 하지 않는다' \
      '1. **원소마다 두 종류를 본다**: `hits` 의 원소에 `comment` 와 `ratingItem` 이 따로 있다.' \
      '2. **수를 두 가지로 적는다**: 모델 주소의 `commentCount` 와 댓글 주소의 `total` 은 같은 값이 아니다' \
      '**JSON 을 못 받았을 때만 — 브라우저 스냅샷 경로.**'
    toks "$(sect "$E/$CA" '### 4.3')" '1. 브라우저 도구가 있으면 그 캡처 기능으로 댓글 영역을 찍는다'
    toks "$(sect "$E/$CA" '## 8. Fail-soft 정책')" \
      'SKILL.md 「MakerWorld 읽는 순서」 대로 다음 단계로 바로 넘어간다 (JSON 주소 → 브라우저 도구 → Codex 셸 `curl` → 사용자 직접 입력)' \
      '(Playwright → Codex → WebFetch → 사용자 직접 입력)'
    toks "$(sect "$E/$CA" '## 10. 미해결 / 검증 필요')" \
      '- MakerWorld JSON 주소 — 2026-09-24 관측으로 댓글 전체를 `offset` 으로 끝까지 받을 수 있음을 확인했다' 'MakerWorld API endpoint (있다면)'
    echo "old41=$(grep -c '^### 4\.1 댓글 50+ 페이지 처리' "$E/$CA")" ;;
  SK-05)  # 형상 측정 자기 검사 — 문장 · 표 · 자리, 실행, 음성 대조 둘
    S=$(sect "$E/$SK" '#### Phase 1.0')
    toks "$S" '**측정 전에 알려진 답으로 한 번 돌린다 (2026-09-25 신규' '`SELFTEST PASS` · `exit=0` 이' '이진 시험 파일을 레포에 두지 않는다' \
      '| 10 mm 정육면체 | 가장 긴 루프 `40.0` mm · `planar` |' '| 2 mm 사각 기둥 (높이 10 mm) | 가장 긴 루프 `8.0` mm · `thin` |' \
      '| 벽 1 mm 사각 관 (바깥 10 mm, `WALL_LOOPS=2`) | 예산 `1.74` mm · 부족 비율 `1.0` · 최소 살 `1.0` mm |'
    # 자리 — 형상 측정 블록 < 자기 검사 문단 < 래티스 실측 문단
    awk '/^# bambu-kit geometry-class probe/{a=NR} /^\*\*측정 전에 알려진 답으로 한 번 돌린다/{b=NR} /^실측 \(2026-09-07 래티스 통/{c=NR} END{print "order=" ((a && b && c && a<b && b<c) ? 1 : 0)}' "$E/$SK"
    ext "$E/$SK" 'T=$(mktemp -d -t probe)' > "$T/p6.sh"
    [ -s "$T/p6.sh" ] || { echo "BLOCK_MISSING"; return 0; }
    run6() { out=$(SKILL_DIR=${1} ${2} "$T/p6.sh" 2>&1); echo "${3}/${2} ok=$(printf '%s\n' "$out" | grep -c '^OK   ') fail=$(printf '%s\n' "$out" | grep -c '^FAIL') $(printf '%s\n' "$out" | grep -E '^SELFTEST|^exit=' | paste -sd' ' -)"; }
    run6 "$E/$SKD" bash end; run6 "$E/$SKD" zsh end
    # 음성 대조 — 측정 코드를 틀리게 만든 사본 둘
    mkdir -p "$T/m6a" "$T/m6b"
    sed 's/^THIN_LOOP_MM = 30\.0 /THIN_LOOP_MM = 5.0 /' "$E/$SK" > "$T/m6a/SKILL.md"
    sed 's/^    wall_budget = outer_width \* 2 + inner_width \* 2 \* (wall_loops - 1)$/    wall_budget = outer_width * 2 + inner_width * 2 * wall_loops/' "$E/$SK" > "$T/m6b/SKILL.md"
    echo "mutated=$(diff "$E/$SK" "$T/m6a/SKILL.md" | grep -c '^>'),$(diff "$E/$SK" "$T/m6b/SKILL.md" | grep -c '^>')"
    run6 "$T/m6a" bash thin5; run6 "$T/m6b" bash budget ;;
  SK-06)  # G-code 길이 재기 — 문장, 알려진 답 둘, 멈춤 셋, 음성 대조, 점검 목록 줄
    S=$(awk '/^\*\*G-code 로 길이 재기 \(2026-09-25 신규\)\*\*/{f=1} /^### Phase 5/{exit} f' "$E/$SK")
    toks "$S" '세션마다 새로 짠 스크립트가 호(`G2` · `G3`)를 빠뜨렸다' '맨 앞의 자기 검사가 알려진 답과 다르면 실제 G-code 는 재지 않고 멈춘다.'
    ext "$E/$SK" '# G-code 로 기능별 압출 길이를 잰다' | sed 's#"<G-code 경로>" <<#"$GC" <<#' > "$T/p5.sh"
    [ -s "$T/p5.sh" ] || { echo "BLOCK_MISSING"; return 0; }
    printf '%s\n' '; HEADER_BLOCK_START' 'G90' 'M82' 'G92 E0' '; FEATURE: Outer wall' 'G1 X0 Y0 F600' 'G1 X10 Y0 E1' 'G3 X10 Y0 I0 J5 E2' \
      'G1 X10 Y10 E2' '; FEATURE: Sparse infill' 'G91' 'G1 X5 Y0 E1' 'G1 X0 Y5 E1' 'G90' 'G92 E0' 'G1 X20 Y20 E0.5' 'G1 X30 Y20' > "$T/known2.gcode"
    printf '%s\n' 'G1 X0 Y0' 'G1 X10 Y0 E1' > "$T/nomark.gcode"
    printf '%s\n' '; FEATURE: Outer wall' 'G1 X0 Y0' 'G2 X10 Y0 R5 E1' > "$T/rarc.gcode"
    printf '%s\n' '; FEATURE: Outer wall' 'G1 X0 Y0' 'G1 E.8 F1800' 'G1 X5 Y0 E.1' > "$T/prime.gcode"
    run5() { out=$(GC=${2} bash ${1} 2>&1); rc=$?; printf '%s\n' "$out" | grep -vE '^(G-code:|SELFTEST)'; echo "rc=$rc selftest=$(printf '%s\n' "$out" | grep -c '^SELFTEST 직선 20.000 · 호 15.708 · 합 35.708')"; }
    run5 "$T/p5.sh" "$T/known2.gcode"; run5 "$T/p5.sh" "$T/nomark.gcode"; run5 "$T/p5.sh" "$T/rarc.gcode"; run5 "$T/p5.sh" "$T/prime.gcode"
    # 음성 대조 — 호를 건너뛰고 좌표도 안 옮기는 옛 방식
    awk '{print} /^        if code in \("G2", "G3"\):$/{print "            continue"}' "$T/p5.sh" > "$T/p5-noarc.sh"
    echo "mutated=$(diff "$T/p5.sh" "$T/p5-noarc.sh" | grep -c '^>')"; run5 "$T/p5-noarc.sh" "$T/known2.gcode"
    # 음성 대조 — G2 · G3 를 같은 방향(반시계)으로 세는 사본. 반원 · 한 바퀴만 든 알려진 답은 이 사본을 통과시킨다
    sed 's/^            sweep = (start - finish) % (2 \* math.pi) if code == "G2" else (finish - start) % (2 \* math.pi)$/            sweep = (finish - start) % (2 * math.pi)/' "$T/p5.sh" > "$T/p5-dir.sh"
    echo "mutated_dir=$(diff "$T/p5.sh" "$T/p5-dir.sh" | grep -c '^>')"; run5 "$T/p5-dir.sh" "$T/known2.gcode"
    # 음성 대조 — 방향을 무시하고 각도 차의 절댓값을 쓰는 사본. 반원보다 짧은 호만 든 알려진 답은 이 사본을 통과시킨다
    sed 's/^            sweep = (start - finish) % (2 \* math.pi) if code == "G2" else (finish - start) % (2 \* math.pi)$/            sweep = abs(finish - start)/' "$T/p5.sh" > "$T/p5-abs.sh"
    echo "mutated_abs=$(diff "$T/p5.sh" "$T/p5-abs.sh" | grep -c '^>')"; run5 "$T/p5-abs.sh" "$T/known2.gcode"
    toks "$(cat "$E/$SK")" '- ☐ **(2026-09-25 신규) G-code 로 길이를 쟀으면 자기 검사 줄(`SELFTEST`)과 기능별 호 비율을 같이 붙였는지**'
    # surface-recipes — 잰 방법 세 줄이 세 실측 바로 뒤에 · 머리
    sed -n 3p "$E/$SR"
    L='> 잰 방법 (2026-09-25 추가): 명령줄로 자른 G-code 에서 쟀고 호(`G2` · `G3`)를 넣었는지 기록이 없다 — 같은 수치를 다시 잴 때는'
    echo "notes=$(grep -cxF -- "$L" "$E/$SR") next=$(grep -cxF -- '> `SKILL.md` Phase 4.4 「G-code 로 길이 재기」 블록으로 재고 호 비율을 같이 적는다.' "$E/$SR")"
    # 각 잰 방법 줄 앞의 빈 줄이 아닌 줄이 세 실측의 끝 줄이다 — 차례대로 갭필 표 · 허공 위 표 · 다림질 문단
    awk -v l="$L" -v p1='| `arachne` | 0.4 m |' -v p2='| 80° 브래킷 A / B | 1.4 m |' -v p3='출력한 대조가 아직 없다.' \
      'NF{if ($0 == l) { n++; ok += (n == 1 && index(prev, p1) == 1) || (n == 2 && index(prev, p2) == 1) || (n == 3 && index(prev, p3) == 1) } prev = $0} END{print "after_ok=" ok+0 "/" n+0}' "$E/$SR" ;;
  SK-07)  # 카이젠 스킬 Gotcha 3 · 5 — 사용자 정책 줄과 체크리스트는 지우지 않는다
    echo "checklist=$(grep -c '^- ☐' "$T/B/$SK")→$(grep -c '^- ☐' "$E/$SK") dropped=$(comm -23 <(grep '^- ☐' "$T/B/$SK" | sort) <(grep '^- ☐' "$E/$SK" | sort) | grep -c .)"
    echo "nozzle_same=$(diff <(grep -rh 'nozzle_temperature' "$T/B/$SKD") <(grep -rh 'nozzle_temperature' "$E/$SKD") >/dev/null && echo 1 || echo 0)" ;;
  SC-01)  # G-code 대조 — 칸마다 · 한 칸 펼치기 · 칸 수 다름 · 따옴표 · 없음. 시작 판 스크립트는 음성 대조
    cmpc() {  # cmpc <트리> <이름> <설정 기록 줄> <설정 JSON>
      pyblock "${1}/$SK" '# 슬라이서가 실제로 쓴 설정' > "$T/compare.py"
      printf '; CONFIG_BLOCK_START\n%s\n; CONFIG_BLOCK_END\n' "${3}" > "$T/g.gcode"; printf '%s\n' "${4}" > "$T/p.json"
      out=$(python3 "$T/compare.py" "$T/g.gcode" "$T/p.json" 2>&1); rc=$?
      echo "${2} rc=$rc$(printf '%s\n' "$out" | grep -E '^(MISMATCH|WARN)' | tr '\n' '|' | sed 's/^/ /')"; }
    cmpc "$E" slot2 '; bridge_speed = 25,50,25' '{"type":"process","name":"t","bridge_speed":["25","25","25"]}'
    cmpc "$E" same3 '; bridge_speed = 25,25,25' '{"type":"process","name":"t","bridge_speed":["25","25","25"]}'
    cmpc "$E" one_vs_3 '; bridge_speed = 25,30,25' '{"type":"process","name":"t","bridge_speed":"25"}'
    cmpc "$E" len_diff '; bridge_speed = 25,25' '{"type":"process","name":"t","bridge_speed":["25","25","40"]}'
    cmpc "$E" quoted '; wall_sequence = "inner wall/outer wall"' '{"type":"process","name":"t","wall_sequence":"inner wall/outer wall"}'
    cmpc "$E" missing '; other = 1' '{"type":"process","name":"t","bridge_speed":["25"]}'
    cmpc "$T/B" start_slot2 '; bridge_speed = 25,50,25' '{"type":"process","name":"t","bridge_speed":["25","25","25"]}' ;;
  SC-02)  # 값 박기 — 칸마다 · 한 값 채우기 · 칸 수 다르고 값이 다르면 멈춤 · 스칼라. 시작 판 스크립트는 음성 대조
    bakec() {  # bakec <트리> <이름> <프로젝트 설정> <설정 JSON> <볼 키>
      pyblock "${1}/$SK" '# 제작자 3mf 의 프로젝트 설정에' > "$T/bake.py"
      rm -rf "$T/bk"; mkdir -p "$T/bk/Metadata"; printf '%s' "${3}" > "$T/bk/Metadata/project_settings.config"
      ( cd "$T/bk" && zip -q src.3mf Metadata/project_settings.config ); printf '%s\n' "${4}" > "$T/p.json"
      out=$(python3 "$T/bake.py" "$T/bk/src.3mf" "$T/bk/out.3mf" "$T/p.json" 2>&1); rc=$?
      val=$( [ -f "$T/bk/out.3mf" ] && unzip -p "$T/bk/out.3mf" Metadata/project_settings.config | python3 -c "import json,sys; print(json.load(sys.stdin).get('${5}'))" || echo none)
      echo "${2} rc=$rc value=$val fail=$(printf '%s\n' "$out" | grep -c '^FAIL')"; }
    P2='{"bridge_speed":["50","50"],"print_settings_id":"x","different_settings_to_system":["","",""]}'
    bakec "$E" two_two "$P2" '{"type":"process","name":"t","bridge_speed":["25","30"]}' bridge_speed
    bakec "$E" one_to_2 "$P2" '{"type":"process","name":"t","bridge_speed":["25"]}' bridge_speed
    bakec "$E" same3_to_2 "$P2" '{"type":"process","name":"t","bridge_speed":["25","25","25"]}' bridge_speed
    bakec "$E" diff3_to_2 "$P2" '{"type":"process","name":"t","bridge_speed":["25","30","25"]}' bridge_speed
    bakec "$E" scalar '{"wall_loops":"3","print_settings_id":"x","different_settings_to_system":["","",""]}' '{"type":"process","name":"t","wall_loops":"2"}' wall_loops
    bakec "$T/B" start_two_two "$P2" '{"type":"process","name":"t","bridge_speed":["25","30"]}' bridge_speed ;;
  SC-03)  # 두 스크립트 자기 검사 블록 — 끝 판에서 기대대로, 시작 판 스크립트를 넣으면 기대에서 떨어진다
    ext "$E/$SK" 'T=$(mktemp -d -t slots)' > "$T/p2.sh"
    [ -s "$T/p2.sh" ] || { echo "BLOCK_MISSING"; return 0; }
    toks "$(awk '/^\*\*두 스크립트 자기 검사 \(2026-09-25 신규\)\*\*/{f=1} /^보내기 전에 명령줄로 잘라/{exit} f' "$E/$SK")" '기대와 다르면 박은 3mf 와 대조 결과를 믿지 않는다.'
    for sh in bash zsh; do out=$(SKILL_DIR=$E/$SKD $sh "$T/p2.sh" 2>&1)
      echo "$sh $(printf '%s\n' "$out" | grep -E '^(MISMATCH|RESULT|exit=|\[)' | tr '\n' '|')"; done
    out=$(SKILL_DIR=$T/B/$SKD bash "$T/p2.sh" 2>&1); echo "start $(printf '%s\n' "$out" | grep -E '^(MISMATCH|RESULT|exit=|\[)' | tr '\n' '|')" ;;
  SC-04)  # 게이트 — 옵션 목록 줄 수 · 빈 목록 [미검증] · 정상 목록 판정 유지. 시작 판 게이트는 음성 대조
    g=$(gate "$E"); mkdir -p "$T/empty/references/option-keys"
    : > "$T/empty/references/option-keys/bambu-$(defaults read /Applications/BambuStudio.app/Contents/Info.plist CFBundleShortVersionString).tsv"
    out=$(SKILL_DIR=$E/$SKD TARGET_SLICER=bambu python3 "$g" "$E/$FXD/process-machine-scope-key.json" 2>&1); rc=$?
    echo "normal rc=$rc $(printf '%s\n' "$out" | grep '^OPTION LIST') fail=$(printf '%s\n' "$out" | grep -c '^FAIL .*키 스코프 불일치 retraction_minimum_travel')"
    out=$(SKILL_DIR=$E/$SKD TARGET_SLICER=orca python3 "$g" "$E/$FXD/process-bambu-only-key-in-orca.json" 2>&1); echo "orca $(printf '%s\n' "$out" | grep '^OPTION LIST')"
    out=$(SKILL_DIR=$T/empty TARGET_SLICER=bambu python3 "$g" "$E/$FXD/process-machine-scope-key.json" 2>&1); rc=$?
    echo "empty rc=$rc empty_unv=$(printf '%s\n' "$out" | grep -c '^\[미검증\] .*목록이 비었거나 깨졌다. 키 존재 · 종류 · enum 값 검사 미실행$') fail=$(printf '%s\n' "$out" | grep -c '^FAIL') $(printf '%s\n' "$out" | grep '^RESULT')"
    g=$(gate "$T/B"); out=$(SKILL_DIR=$T/empty TARGET_SLICER=bambu python3 "$g" "$T/B/$FXD/process-machine-scope-key.json" 2>&1); rc=$?
    echo "start_empty rc=$rc list_unv=$(printf '%s\n' "$out" | grep -c '^\[미검증\] .*tsv') $(printf '%s\n' "$out" | grep '^RESULT')" ;;
  SC-05)  # 옵션 목록 생성기 — 빈 판정 결과면 쓰지 않고 exit 1, 채워지면 쓴다. 시작 판 생성기는 음성 대조
    mkdir -p "$T/gen/src/src/libslic3r"
    printf '%s\n' 'void PrintConfigDef::handle_legacy(t_config_option_key &opt_key, std::string &value)' '{' '    if (opt_key == "old_key") { opt_key = "new_key"; }' '}' \
      'void PrintConfigDef::handle_legacy_composite(DynamicPrintConfig &config)' '{' '}' > "$T/gen/src/src/libslic3r/PrintConfig.cpp"
    printf '#define BBL_JSON_KEY_NAME "name"\n' > "$T/gen/src/src/libslic3r/Preset.hpp"
    printf '#!/bin/sh\ncat > /dev/null\n' > "$T/gen/probe-empty"
    printf '%s\n' '#!/bin/sh' 'cat > /dev/null' 'case "$1" in' "  dump) printf 'canonical\\tk1\\nenum\\tk1\\tv1\\n';;" "  presets) printf 'process\\tk1\\nfilament\\tk2\\nmachine\\tk3\\n';;" \
      "  classify) printf 'accepted\\tk1\\n';;" "  values) printf 'accepted\\tk1\\tv1\\t\\tv1\\n';;" 'esac' > "$T/gen/probe-full"
    chmod +x "$T/gen/probe-empty" "$T/gen/probe-full"
    for tree in "$E" "$T/B"; do for p in probe-empty probe-full; do rm -f "$T/gen/out.tsv"
      out=$(python3 "$tree/$GO" "$T/gen/$p" "$T/gen/src" "$T/gen/out.tsv" 2>&1); rc=$?
      echo "$( [ "$tree" = "$E" ] && echo end || echo start)/$p rc=$rc written=$( [ -f "$T/gen/out.tsv" ] && grep -c . "$T/gen/out.tsv" || echo none) refused=$(printf '%s\n' "$out" | grep -c '을 쓰지 않았다 — canonical, process, filament, machine, enum 줄이 0 개다')"
    done; done ;;
  SC-06)  # 음성 대조 실행 블록 전체 — bash · zsh 같은 출력, 종료 코드 순서, 변이 줄 수, (1) 검사의 양성 대조
    ext "$E/$SK" 'GATE=$(mktemp -t gate)' > "$T/neg.sh"
    [ -s "$T/neg.sh" ] || { echo "BLOCK_MISSING"; return 0; }
    ( cd "$E" && bash "$T/neg.sh" > "$T/neg.bash" 2>&1; echo "bash_rc=$?" ); ( cd "$E" && zsh "$T/neg.sh" > "$T/neg.zsh" 2>&1; echo "zsh_rc=$?" )
    echo "same=$(diff <(sed -E 's#/var/folders/[^ ]*#TMP#g' "$T/neg.bash") <(sed -E 's#/var/folders/[^ ]*#TMP#g' "$T/neg.zsh") >/dev/null && echo 1 || echo 0) stop=$(grep -c '^STOP' "$T/neg.bash") $(grep -E '^gate_lines=' "$T/neg.bash" | tr -s ' ')"
    echo "exits=$(grep '^exit=' "$T/neg.bash" | cut -d= -f2 | tr -d '\n')"
    # 소재 칸 알림 줄은 검사 유지 실행에서만 나와야 한다 — 알림 줄을 지운 사본에서도 나오면 2 가 된다
    echo "mutations=$(grep -xE '[0-9]+' "$T/neg.bash" | tr '\n' ' ')anchor=$(grep -c '^기준점 1 개$' "$T/neg.bash") empty_unv=$(grep -c '목록이 비었거나 깨졌다' "$T/neg.bash") slot_note=$(grep -c 'filament-unreadable-slot.json: filament_retraction_length 슬롯 1 을 못 읽었다' "$T/neg.bash")"
    # 시험 파일 전수 — 폴더 = 표 = 실행 줄, 새 넷의 목표 위반, 「일곱 모두」 문장
    comm -3 <(cd "$E/$FXD" && find . -maxdepth 1 -name '*.json' | sed 's#^\./##' | sort) \
      <(grep -oE '^\| `evals/gate-fixtures/[a-z0-9-]+\.json` \|' "$E/$SK" | sed -E 's#.*/([a-z0-9-]+\.json).*#\1#' | sort) | grep -c . | sed 's/^/table_diff=/'
    echo "fixtures=$(cd "$E/$FXD" && find . -maxdepth 1 -name '*.json' | grep -c .) rows=$(grep -cE '^\| `evals/gate-fixtures/[a-z0-9-]+\.json` \|' "$E/$SK")"
    g=$(gate "$E"); L=""
    for pair in "$NF1|유량비 7.1x (sparse_infill_speed 슬롯 1) — 5x 초과" "$NF2|scarf 길이 20.0mm 가 루프 둘레 100.0mm 의 20% — 상한 15% 초과" \
                "$NF3|filament_retraction_length 슬롯 1 이 0.8 로 소재 부모값 0.4 의 1.5 배 초과" "$NF4|elefant_foot_compensation='-0.1' 음수 불가 (min=0)"; do
      f=${pair%%|*}; out=$(SKILL_DIR=$E/$SKD TARGET_SLICER=bambu python3 "$g" "$E/$f" 2>&1); rc=$?
      L="$L $(basename "$f" .json):rc=$rc,fail=$(printf '%s\n' "$out" | grep -c '^FAIL'),target=$(printf '%s\n' "$out" | grep -cF -- "${pair#*|}"),unv=$(printf '%s\n' "$out" | grep -c '^\[미검증\]')"; done; echo "${L# }"
    toks "$(cat "$E/$SK")" '일곱 모두 아래 표에 FAIL 이 나야 하는 시험 파일이 하나 이상 있다 (2026-09-25).' \
      '금지 키 · `compatible_printers` · 메타필드 · 숫자 타입 검사는 아직 FAIL 시험 파일이 없다.'
    # (1) 검사의 양성 대조 — 실행 줄 하나 뺀 사본 둘 · 표 행 하나 뺀 사본 · 폴더에만 파일을 더한 사본 · 틀린 SKILL.md 경로
    # run2 는 빈 목록 변이 줄에도 이름이 나오는 파일이다 — 파일 전체에서 이름을 찾으면 빠진 실행 줄을 못 잡는다
    for v in run run2 table stray path; do rm -rf "$T/nv"; mkdir -p "$T/nv"; cp -R "$E/bambu-kit" "$T/nv/"
      case $v in
        run)   grep -vxF 'TARGET_SLICER=bambu python3 "$GATE" $FX/process-thin-baseline.json; echo "exit=$?"' "$E/$SK" > "$T/nv/$SK" ;;
        run2)  grep -vxF 'TARGET_SLICER=orca  python3 "$GATE" $FX/process-bambu-only-key-in-orca.json; echo "exit=$?"' "$E/$SK" > "$T/nv/$SK" ;;
        table) grep -vF '| `evals/gate-fixtures/process-flow-ratio-over.json` |' "$E/$SK" > "$T/nv/$SK" ;;
        stray) cp "$E/$FXD/process-thin-baseline.json" "$T/nv/$FXD/process-stray.json" ;;
      esac
      if [ $v = path ]; then sed 's#^S=bambu-kit/skills/bambu-print-profile/SKILL.md$#S=bambu-kit/skills/없는폴더/SKILL.md#' "$T/neg.sh" > "$T/neg-v.sh"; else cp "$T/neg.sh" "$T/neg-v.sh"; fi
      out=$(cd "$T/nv" && bash "$T/neg-v.sh" 2>&1); rc=$?
      echo "$v rc=$rc $(printf '%s\n' "$out" | grep -E '^(표에 없음|실행 줄에 없음|STOP)' | tr '\n' '|') exits=$(printf '%s\n' "$out" | grep -c '^exit=')"; done ;;
  ER-01)  # 새로 생긴 URL 이 근거 파일에 있다 — 여덟 파일은 파일마다 편집 전 판과 비교, 주소 틀은 관측 모델 번호로 맞춘다, notes 는 URL 전부
    for f in "${FILES[@]}"; do comm -13 <( [ -f "$T/B/$f" ] && url < "$T/B/$f" ) <(url < "$E/$f"); done | urlnorm | sort -u | comm -23 - <(url < "$E/$EVID") | grep -c .
    if [ -f "$E/$NOTES" ]; then url < "$E/$NOTES" | urlnorm | sort -u | comm -23 - <(url < "$E/$EVID") | grep -c .; else echo NOTES_MISSING; fi ;;
  ER-02)  # 더한 줄의 번역투 6 종 · 앱 이름 · 브라우저 서버 이름
    echo "added=$(added | grep -c .) k02=$(added | grep -cE "$K02") names=$(added | grep -ciE 'fit-?pal|fit_pal|flutter[-_]playwright|playwright|mcp__|chrome-devtools-mcp')" ;;
  ER-03)  # notes 문자열 · 공유 파일과 다른 Phase 파일을 건드린 커밋
    git cat-file -e "$END:$NOTES" 2>/dev/null && echo notes_committed=1 || echo notes_committed=0
    toks "$(cat "$E/$NOTES" 2>/dev/null)" '`F30`' 'bambu:P1' 'bambu:P2' 'bambu:P3' 'bambu:P4' 'bambu:P5' 'bambu:P6' \
      '.claude/skills/bambu-kaizen/SKILL.md' '.claude/skills/bambu-research/SKILL.md' 'docs/bambu-kit/bambu-print-profile.html' \
      'feat/bambu-kit-orca-h2s-feedback' 'bambu-fields-baseline.md' '네 칸' 'plugin.json' \
      '## 바꾼 파일' '## 반영한 처리 배정표 키' '## 미반영 키와 사유' '## 넘기는 것' '## changelog 한 단락' '## 킷 로그 한 단락' '## 다음 사이클 메모'
    # 넘김 줄은 사유와 같은 줄로 센다 — 낱말은 다른 절에도 나와 넘김 줄을 빠뜨려도 1 이 된다
    echo "$(grep -F 'feat/bambu-kit-orca-h2s-feedback' "$E/$NOTES" | grep -cF '충돌') $(grep -F '네 칸' "$E/$NOTES" | grep -cF 'SKILL.md:1706') $(grep -F 'bambu-fields-baseline.md' "$E/$NOTES" | grep -cF '/bambu-research')"
    not_other "$B" "$END" "$SIG" .claude-plugin/marketplace.json bambu-kit/.claude-plugin/plugin.json bambu-kit/README.md README.md CLAUDE.md \
      .harness/.meta/orchestrator-audit-log.md .harness/.meta/kaizen-failure-count.yaml .claude/kaizen-input/insights-report.md \
      .github/workflows/ci.yml .claude/skills harness scripts docs | grep -c . ;;
  AR-01)  # 허용 경로 · 서명 · 봉인 · 범위 선언 블록
    unsigned_on "$B" "$END" "$SIG" bambu-kit | grep -c .
    echo "$(my | grep -v '^\.harness/' | grep -vxF -f <(printf '%s\n' "${FILES[@]}") | grep -c .) $(my | grep -cxF -f <(printf '%s\n' "${FILES[@]}"))"
    find .harness -type f -name 'sprint-contract*.md' -print0 | while IFS= read -r -d '' f; do verify_seal "$f"; done \
      | awk '$1=="SEAL_BROKEN"{print $2}' | sed 's#^\./##' | sort -u | comm -12 - <( { my; echo "$CF"; } | sort -u) | grep -c .
    verify_seal "$E/$CF" | cut -d' ' -f1
    diff <(scope "$E/$CF" | grep -vxF '.harness/' | sort) <(printf '%s\n' "${FILES[@]}" | sort) >/dev/null && echo "scope_same=1" || echo "scope_same=0"
    scope "$E/$CF" | grep -cxF '.harness/' ;;
  AR-02)  # 새 문장이 가리키는 자리가 실제로 있다 — 읽는 순서 제목 · 길이 재기 표지 · §4.1 제목 · 설계 가이드 소절
    echo "order_head=$(grep -c '^## MakerWorld 읽는 순서' "$E/$SK") order_refs=$( { grep -c '「MakerWorld 읽는 순서」' "$E/$SK"; grep -c '「MakerWorld 읽는 순서」' "$E/$CA"; } | paste -sd/ -)"
    echo "len_head=$(grep -c '^\*\*G-code 로 길이 재기 (2026-09-25 신규)\*\*' "$E/$SK") len_refs=$( { grep -c '「G-code 로 길이 재기」' "$E/$SK"; grep -c '「G-code 로 길이 재기」' "$E/$SR"; } | paste -sd/ -)"
    echo "ca41=$(grep -c '^### 4\.1 ' "$E/$CA") sk_ref41=$(grep -c 'references/comment-analysis.md` §4\.1' "$E/$SK") guide=$(sect "$E/harness/docs/guides/skill-design-guide.md" '## 3.7.' | grep -c '^#### 0 이 아닌 값을 내는 새 측정 — 알려진 답 대조$')" ;;
  RE-01)  # 새 파일 목록 — 시험 입력 JSON 넷뿐이다
    comm -13 <(cd "$T/B" && find bambu-kit -type f | sort) <(cd "$E" && find bambu-kit -type f | sort) ;;
  RE-02)  # 자기 검사는 SKILL.md 의 원 코드를 뽑아 돌린다 — 측정 · 박기 · 대조 코드의 고유 줄이 한 번씩만 있다
    echo "$(grep -c '^def wall_budget_shortfall(loops, budget):$' "$E/$SK") $(grep -c '^DIFF_SLOT = {"process": 0, "filament": 1}' "$E/$SK") $(grep -c '^recorded, in_block = {}, False$' "$E/$SK") $(grep -c '^drop() {' "$E/$SK")" ;;
  DG-01)  # commands.analyze · commands.test 는 scripts/release.sh 만 잰다 — 이 Phase 가 그 파일을 건드렸는지
    my | grep -c '^scripts/release\.sh$' ;;
  DG-04)  # 구동할 앱 · 서버 — 바뀐 코드 파일은 옵션 목록 생성기 하나뿐인지 (그것은 SC-05 가 돌린다)
    my | grep -vxF "$GO" | grep -v '^\.harness/' | grep -cE '\.(dart|ts|tsx|js|rs|go|py|sh)$' ;;
  AP-01)  # 더한 줄에 이 킷 플러그인 버전 값 — 값은 plugin.json 에서 읽는다
    L=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$E/bambu-kit/.claude-plugin/plugin.json")
    echo "version=$L $(added | grep -cF -- "$L")" ;;
  AP-04)  # frontmatter — SKILL.md 첫 블록이 편집 전과 같고 name 줄이 폴더 이름이다
    echo "$(diff <(awk 'NR==1&&/^---/{fm=1;next} fm&&/^---/{exit} fm' "$T/B/$SK") <(awk 'NR==1&&/^---/{fm=1;next} fm&&/^---/{exit} fm' "$E/$SK") >/dev/null && echo 1 || echo 0)/$(awk 'NR==1&&/^---/{fm=1;next} fm&&/^---/{exit} fm' "$E/$SK" | grep -cxF 'name: bambu-print-profile')" ;;
  DG-02)  # markdownlint — 파일마다 규칙별 경고 수를 편집 전 판과 비교 · JSON 읽힘 · 파이썬 조각 문법
    for f in "${MDS[@]}"; do k=$(printf '%s' "$f" | tr '/' '_'); cp "$T/B/$f" "$T/$k.0.md"; cp "$E/$f" "$T/$k.md"; bash "$K/rule-diff.sh" "$T/$k.0.md" "$T/$k.md"; done
    python3 -c 'import json,sys; [json.load(open(p, encoding="utf-8")) for p in sys.argv[1:]]; print("json_ok", len(sys.argv) - 1)' "$E/$NF1" "$E/$NF2" "$E/$NF3" "$E/$NF4"
    n=0; for p in '# bambu-kit geometry-class probe' '# 가짜 3mf 셋으로 형상 측정을' '# 받은 JSON 을 세어 보고한다' '# 받은 JSON 의 문자열 값을 한 줄씩 푼다' \
      '# 제작자 3mf 의 프로젝트 설정에' '# 슬라이서가 실제로 쓴 설정' '# G-code 로 기능별 압출 길이를 잰다'; do
      pyblock "$E/$SK" "$p" > "$T/pc.py"; [ -s "$T/pc.py" ] && python3 -c 'import ast,sys; ast.parse(open(sys.argv[1], encoding="utf-8").read())' "$T/pc.py" 2>/dev/null && n=$((n+1)); done
    g=$(gate "$E"); python3 -c 'import ast,sys; ast.parse(open(sys.argv[1], encoding="utf-8").read())' "$g" && n=$((n+1))
    python3 -c 'import ast,sys; ast.parse(open(sys.argv[1], encoding="utf-8").read())' "$E/$GO" && n=$((n+1)); echo "python_parsed=$n" ;;
  DG-05)  # 저장소 검사 — $END 판을 git 저장소로 만든 사본에서 돈다 (작업 폴더의 다른 Phase 미커밋 변경이 끼지 않는다)
    local G=$T/G; rm -rf "$G"; cp -R "$E" "$G"
    git -C "$G" init -q && git -C "$G" add -A && git -C "$G" -c user.name=m -c user.email=m@m commit -qm snap || return 2
    # V 줄 머리에는 FAIL 이 안 찍힌다(아래 들여쓴 줄에 찍힌다) — `— OK` · `— SKIP (…)` 로 끝나지 않는 V 줄을 센다
    ( cd "$G" && python3 scripts/validate-plugin.py bambu-kit > "$T/vp.txt" 2>&1; echo $? > "$T/vp.rc" )
    echo "$(grep -cE '^  V([1-9]|10) ' "$T/vp.txt") $(grep -E '^  V([1-9]|10) ' "$T/vp.txt" | grep -cvE -- '— (OK|SKIP \(no templates/\))$') rc=$(cat "$T/vp.rc")"
    ( cd "$G" && python3 scripts/validate-plugin.py --check=table-integrity,code-fence > "$T/ti.txt" 2>&1 )
    echo "tf_mine=$(grep 'FAIL' "$T/ti.txt" | grep -cF -f <(printf '%s\n' "${FILES[@]}"))"
    ( cd "$G" && python3 scripts/sync-docs.py --check-only > "$T/sd.txt" 2>&1 ); echo "sync_docs_rc=$? $(grep -cxF '  bambu-kit/README.md: 동기화됨' "$T/sd.txt")" ;;
  DG-06)  # 사이클 검사 — 이 Phase 몫 줄만 본다. docs-site-regen 은 Final F2 몫
    python3 scripts/validate-post-kaizen.py --since "$B" --verbose > "$T/vpk.txt" 2>&1
    grep -E '\] . (scope-isolation|doc-contracts): ' "$T/vpk.txt" | awk '{print $5, $2}'
    python3 scripts/validate-doc-contracts.py -v 2>&1 | awk -F' → ' '/^ *검사: /{a=$1; sub(/^ *검사: /,"",a); sub(/:[0-9]+$/,"",a); print a; print $2}' | sort -u > "$T/dc.txt"
    echo "doc_checked=$(grep -c . "$T/dc.txt") doc_mine=$(comm -12 "$T/dc.txt" <(my) | grep -c .)"
    awk '/ scope-isolation: /{f=1;next} /^\[ /{f=0} f&&/^ +[0-9a-f]{7,40}$/{print $1}' "$T/vpk.txt" > "$T/viol.txt"
    echo "violators=$(grep -c . "$T/viol.txt") mine=$(while read -r c; do git log -1 --format=%B "$c" | grep -qxF "$SIG" && echo "$c"; done < "$T/viol.txt" | grep -c .)" ;;
  *) echo "UNKNOWN $1"; return 2 ;;
  esac
}
```

```bash
# fakecurl.sh — 네트워크 없이 받는 법 블록을 돌리는 가짜 curl. 근거 파일 §2 bambu:P5 표의 관측 모양을 흉내 낸다
# FAKE_DIR 에 요청 기록(requests.log)을 남긴다. FAKE_MODE=403 이면 댓글 첫 페이지가 403 이다. bash · zsh 양쪽에서 돈다
curl() {
  local out="" fmt="" url=""
  while [ $# -gt 0 ]; do
    case "$1" in -o) out=$2; shift 2;; -w) fmt=$2; shift 2;; -*) shift;; *) url=$1; shift;; esac
  done
  echo "$url" >> "$FAKE_DIR/requests.log"
  python3 - "$url" "$out" "${FAKE_MODE:-}" "$fmt" <<'PY'
import json, sys, re
url, out, mode, fmt = sys.argv[1:]
def hits(n_comment, n_rating):
    return [{"comment": {"content": "c"}} for _ in range(n_comment)] + [{"ratingItem": {"score": 5}} for _ in range(n_rating)]
code, body = 200, None
if "comment-service" in url:
    off = int(re.search(r"offset=(\d+)", url).group(1))
    if mode == "403" and off == 0:
        code, body = 403, "<html>Just a moment...</html>"
    else:
        body = json.dumps({"total": 159, "hits": hits(44, 56) if off == 0 else hits(0, 59) if off == 100 else []})
elif url.endswith("/instances"):
    body = json.dumps({"total": 4, "hits": [{}, {}, {}, {}]})
else:
    body = json.dumps({"title": "t", "summary": "<p><a href=\"https://example.com/manual.pdf\">m</a> <a href=\"https://github.com/o/r\">r</a></p>",
                       "designCreator": {}, "instances": [{}, {}, {}, {}], "commentCount": 190, "license": "x"})
open(out, "w").write(body)
sys.stdout.write(fmt.replace("%{http_code}", str(code)).replace("\\n", "\n"))
PY
}
```

```bash
#!/usr/bin/env bash
# rule-diff.sh <옛 파일> <새 파일> — 규칙마다 경고 수를 두 판에서 세어 늘어난 규칙만 적는다
# 더한 줄의 경고만 세면 같은 제목 중복(MD024) · 제목 앞뒤 빈 줄(MD022) · 목록 앞뒤 빈 줄(MD032)처럼 손대지 않은 옆 줄에 붙는 새 경고를 놓친다 (실측 2026-09-25: Phase 7 · 8 · 9 · 11)
# 린터가 안 돌면 경고 0 이 조용히 나온다 — 두 판 모두 돌았다는 줄(Linting: 1 file)이 없으면 멈춘다
set -u
DIR=$(cd "$(dirname "$0")" && pwd)
cnt() { local o
  o=$("$DIR/node_modules/.bin/markdownlint-cli2" --config "$DIR/cfg.markdownlint-cli2.jsonc" "$1" 2>&1)
  printf '%s\n' "$o" | grep -q '^Linting: 1 file' || { echo "LINT_NOT_RUN $1"; return 2; }
  printf '%s\n' "$o" | sed -nE 's/^[^ ]+:[0-9]+(:[0-9]+)? (error|warning) (MD[0-9]{3})\/.*/\3/p' | sort | uniq -c | awk '{print $2, $1}'; }
OLD=$(cnt "$1") || { echo "$OLD"; exit 2; }
NEW=$(cnt "$2") || { echo "$NEW"; exit 2; }
UP=$(awk 'NR==FNR { if (NF) a[$1] = $2; next } NF { o = ($1 in a) ? a[$1] : 0; if ($2 > o) printf "%s:%d→%d\n", $1, o, $2 }' \
  <(printf '%s\n' "$OLD") <(printf '%s\n' "$NEW") | sort | paste -sd' ' -)
echo "rules_before=$(printf '%s\n' "$OLD" | grep -c .) rules_after=$(printf '%s\n' "$NEW" | grep -c .) rules_up=$(printf '%s' "$UP" | wc -w | tr -d ' ')${UP:+ $UP}"
```

**예행.** 시작 커밋에서 레포를 스크래치로 복제해(`p13d/rehearse.sh`) BUILD 가 할 커밋을 흉내 냈다 — 봉인 커밋(이 계약 초안에 digest 를 적은 판) → 다른 Phase 서명 커밋 하나
(`design-kit/README.md`, 걸러져야 한다) → `mock.py` 를 적용한 구현 커밋 하나(`bambu-kit/` 여덟) → `end_sha` → notes 모의본(`p13d/notes-mock.md`) → `end_sha` 한 줄 더.
변형 `base` 는 구현 없이 `end_sha` 를 시작 커밋으로 둬 시작 커밋 판을 잰다. 변형 다섯은 같은 흐름에 커밋 하나를 더한다: `unsigned-shared`(서명 없이 루트 `README.md`) ·
`unsigned-mine`(서명 없이 `bambu-kit/README.md`) · `unsigned-docsite`(서명 없이 `docs/bambu-kit/bambu-print-profile.html`) · `signed-outside`(서명하고 `bambu-kit/.claude-plugin/plugin.json`) ·
`cross-phase`(서명하고 `harness/skills/sprint/SKILL.md` 와 `bambu-kit/skills/bambu-print-profile/references/tolerance.md` 한 커밋). 변형 다섯의 저장소는 잰 뒤 지웠다(디스크).
다시 재려면 `bash p13d/rehearse.sh <이 계약 사본> p13d/rh-<변형> <변형>` 으로 만든다.

**봉인 전 실측 (2026-09-25, bash 5.3.9 · `/bin/bash` 3.2.57 같은 값).** 예행 판 = 이 계약 초안을 봉인한 예행 저장소(`p13d/rh-none`), 시작 커밋 판 = 변형 `base`(`p13d/rh-base`).
기준 커밋을 `499cc12` 로 옮긴 뒤(10:2x) 예행 저장소를 그 커밋에서 다시 만들어 조건 전부 · 문장 삭제 46 · 대조 21 · 변형 다섯을 다시 돌렸다 — 아래 값은 그 출력이고,
`82b2493` 기준으로 잰 앞 초안 값과 DG-02(측정을 바꿈) 밖에서는 한 글자도 다르지 않았다. 조건 전부를 한 셸에서 도는 스크립트는 `p13d/runall.sh <예행 폴더>` 다.
검토(`.harness/.meta/kaizen-0924/phase13-review.md`, 고칠 것 넷)를 반영한 뒤(11:0x) `mock.py` 두 자리(음성 대조 (1) 의 실행 줄 확인 · G-code 길이 알려진 답)와
`m.sh` 두 갈래(SK-06 · SC-06)를 고치고 예행 저장소를 다시 만들어 조건 전부 · 문장 삭제 · 대조 · 변형 다섯을 다시 돌렸다. 앞 판 출력과 달라진 줄은
SK-06 세 줄(`mutated_dir=1` 과 그 뒤 두 줄) · SC-06 두 줄(`slot_note=1` · `run2`) · ER-02 `added=545` 뿐이다(`p13d/all-none.final.txt` 와 `p13d/rv/all-none.rv.txt` 의 `diff`).
DG-06 은 측정을 바꾸지 않고 문구만 바꿨다 — 검사 이름 줄을 안 내는 사본은 `m DG-06` 이 두 줄, `검사:` 줄을 안 내는 사본은 `doc_checked=0` 이라 새 문구에서 FAIL 이다(`p13d/rv/dg6ctl.sh`).
2 회차 검토(같은 파일 `## 2 회차`, 새로 찾은 것 하나)를 BUILD 가 반영했다(11:2x) — `mock.py` 의 알려진 답을 `G2` 3/4 호(반지름 2) · `G3` 1/4 호(반지름 4)로, `m.sh` SK-06 갈래에
방향 무시 변이(`mutated_abs`)를 더했다. 예행 저장소를 다시 만들어 조건 전부 · 문장 삭제 46(`DROP 46 NODROP 0 MISSING 0`) · 대조 21 · 변형 다섯을 다시 돌렸고, 앞 판 출력과 달라진 줄은
SK-06 새 세 줄(`mutated_abs=1` 과 그 뒤 두 줄)뿐이다(`p13d/rv/all-none.rv2.txt` 와 `p13b/all-none.b1.txt` 의 `diff`). DG-06 문구는 2 회차 권고대로 `doc_checked` 1 이상을 상태와 상관없이
요구하게 맞췄다 — 요구값 줄은 전과 같고 예행 값 `doc_checked=2` 도 그대로다.
모의본은 `mock.py`(sha256 앞 16 자리 `2ae88ae777c4f1d8`)를 시작 커밋 판에 적용한 트리다. 측정 도우미는 이 절의 네 블록을 글자 그대로 뗀 것이다(`p13d/k/`).

| 조건 | 예행 판 (요구값) | 시작 커밋 판 | 양성 · 음성 대조 |
| --- | --- | --- | --- |
| SK-01 | `1` 열둘 · `heads=1 old=0` · `1 0` · `names=0 bypass=0` | `0` 열둘 · `heads=0 old=1` · `0 1` · `names=7 bypass=2` | 문장 삭제 14 개 모두 출력이 바뀜 · 끝 판 사본 comment-analysis 끝에 「Playwright 로 연다」 → `names=1` · surface-recipes 끝에 「Cloudflare 를 우회한다」 → `bypass=1` |
| SK-02 | 조건 줄의 다섯 줄 | `BLOCK_MISSING` | 넷째 · 다섯째 줄이 음성 대조(멈춤 줄 삭제 → `req=5` · 첫 페이지 멈춤 → `warn=1`) · 셋째 줄이 403 경우 |
| SK-03 | `1` 일곱 · `0 0 0` · `bash lines=47 pdf=1 github=1 order=1` · `zsh …` 같은 값 · `empty lines=0` | `0` 일곱 · `4 1 1` · `BLOCK_MISSING` | 문장 삭제 7 개 · 둘째 줄의 시작 판 값이 옛 문장 양성 대조 |
| SK-04 | 머리 줄 · `1 1 1 1 1` · `1` · `1 0` · `1 0` · `old41=0` | `> Last updated: 2026-05-23` · `0 0 0 0 0` · `0` · `0 1` · `0 1` · `old41=1` | 문장 삭제 11 개 |
| SK-05 | `1` 여섯 · `order=1` · PASS 두 줄 · `mutated=1,1` · FAIL 두 줄 | `0` 여섯 · `order=0` · `BLOCK_MISSING` | 문장 삭제 6 개 · 변이 둘이 음성 대조 · 같은 블록에 시작 판 측정 코드를 넣으면 `SELFTEST PASS`(측정 코드 자체는 이번에 안 바뀐다) |
| SK-06 | 조건 줄의 스물세 줄 | `0 0` · `BLOCK_MISSING` | 문장 삭제 5 개(머리 두 문장 · 점검 목록 줄 · 잰 방법 두 줄) · 호 건너뛰기 변이 → 자기 검사 FAIL · `G2` · `G3` 같은 방향 변이 → 자기 검사 FAIL (초안의 반원 알려진 답으로는 `rc=0 selftest=1` 로 통과했다 — 검토에서 찾은 구멍) · 방향 무시(각도 차의 절댓값) 변이 → 자기 검사 FAIL (1/4 호 둘 알려진 답으로는 `rc=0 selftest=1` 로 통과했다 — 2 회차 검토에서 찾은 구멍). m 밖에서 둘 다 시계 · 서로 바꿈 · 짧은 호 · 중심을 끝점에서 잡는 변이도 돌려 `SELFTEST` 호 28.274 · 21.991 · 9.425 · 30.173 · `rc=1` 이었다. 방향 변이 셋(둘 다 반시계 · 둘 다 시계 · 서로 바꿈)은 반원 알려진 답에서, 방향 무시 · 짧은 호 두 변이는 1/4 호 둘 알려진 답에서 호 15.708 · `rc=0` 으로 통과했다(`p13d/rv/extra.sh`) |
| SK-07 | `checklist=48→49 dropped=0` · `nozzle_same=1` | `checklist=48→48 dropped=0` · `nozzle_same=1` | 체크리스트 `from` 줄을 뺀 사본 → `dropped=1` · `nozzle_temperature` 줄을 바꾼 사본 → `nozzle_same=0` |
| SC-01 | 조건 줄의 일곱 줄 | `slot2 rc=0` · `one_vs_3 rc=0` · `len_diff rc=0`(WARN 없음) · `missing rc=1 … 보낸 값 None` | 일곱째 줄(시작 판 스크립트)이 음성 대조 |
| SC-02 | 조건 줄의 여섯 줄 | `two_two` · `one_to_2` · `same3_to_2` · `diff3_to_2` 모두 `value=['25', '25']` · rc=0 | 여섯째 줄(시작 판 스크립트)이 음성 대조 |
| SC-03 | 조건 줄의 네 줄 | `BLOCK_MISSING` | 넷째 줄(시작 판 스크립트)이 음성 대조 · 문장 삭제 1 개 |
| SC-04 | 조건 줄의 네 줄 | `normal … OPTION LIST bambu-02.08.02.61.tsv fail=1`(줄 수 없음) · `empty … empty_unv=0` | 넷째 줄(시작 판 게이트)이 음성 대조 |
| SC-05 | 조건 줄의 네 줄 | `end/probe-empty rc=0 written=1 refused=0` | 셋째 줄(시작 판 생성기)이 음성 대조 |
| SC-06 | 조건 줄의 열네 줄 | `exits=111111111100000000000` · `mutations=1 1 1 1 1 1 anchor=1 empty_unv=0 slot_note=1` · `table_diff=8` · `fixtures=19 rows=11` · 다섯 변형 모두 `rc=0 … exits=21`(틀린 경로도 시험 21 개를 통과로 찍는다) | 문장 삭제 2 개 · 끝 판 사본에서 표 행 하나를 뺀 사본 → `table_diff=1` · `rows=22` · 뒤 다섯 줄이 (1) 검사의 양성 대조 — 초안 블록(파일 전체를 찾던 grep)은 `run2` 에서 `rc=0` · `exits=46` 이었다(검토에서 찾은 구멍). 고친 블록은 `run2` 에서 zsh 도 `rc=1` · `exits=0` · 알림 줄 변이가 다른 칸 알림 줄(`outer_wall_speed 슬롯`)을 바꾼 사본은 `mutations` 가 그대로 1 이고 `slot_note=2` 다(`p13d/rv/extra.sh`) |
| ER-01 | `0` · `0` | — | SKILL.md 끝 `https://example.invalid/x` → `1 0` · notes 끝 같은 URL → `0 1` · 주소 틀을 맞추지 않으면(`>` 에서 끊는 옛 추출) `3` — 실측으로 찾아 고친 측정 구멍 |
| ER-02 | `added=545 k02=0 names=0` | — | SKILL.md 끝 「이 값에 대해 적는다」 → `k02=1` · comment-analysis 끝 「fit-pal 화면」 → `names=1` |
| ER-03 | `notes_committed=1` · `1 5 1 2 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1 1 1` · `1 1 1` · `0` | — | 변형 `unsigned-shared` · `unsigned-mine` · `unsigned-docsite` · `signed-outside` · `cross-phase` → 넷째 값 모두 `1` |
| AR-01 | `0` · `0 8` · `0` · `SEAL_OK` · `scope_same=1` · `1` | — | `unsigned-mine` → 첫 값 `1` · `signed-outside` → `1 8` · `cross-phase` → `2 8` · 조건 줄 한 글자 변조 사본 → `SEAL_BROKEN` |
| AR-02 | `order_head=1 order_refs=3/3` · `len_head=1 len_refs=1/3` · `ca41=1 sk_ref41=1 guide=1` | `order_head=0 order_refs=0/0` · `len_head=0 len_refs=0/0` · `ca41=1 sk_ref41=1 guide=1` | 제목을 `## MakerWorld 읽기` 로 바꾼 사본 → `order_head=0` · 길이 재기 표지를 바꾼 사본 → `len_head=0` |
| RE-01 | 새 시험 파일 네 줄 | — | 끝 판 사본에 `x.json` → 다섯 줄 |
| RE-02 | `1 1 1 1` | `1 1 1 1` | 측정 함수 머리를 한 번 더 적은 사본 → `2 1 1 1` |
| AP-01 | `version=0.9.5 0` | — | SKILL.md 끝 「버전 0.9.5」 → `version=0.9.5 1` |
| AP-03 · DG-05 | `10 0 rc=0` · `tf_mine=0` · `sync_docs_rc=0 1` | `10 0 rc=0` · `tf_mine=0` · `sync_docs_rc=0 1` | 맨 펜스 한 쌍 → `10 1 rc=2` · `tf_mine=1` · `name:` 을 깬 사본 → `10 1 rc=2` |
| AP-04 | `1/1` | `1/1` | `name:` 을 바꾼 사본 → `0/0` |
| DG-01 · DG-03 · DG-04 | `0` · `0` | — | DG-04 거르개에 `bambu-kit/scripts/x.py` 를 넣으면 `1` |
| DG-02 | `rules_up=0` 셋(`rules_before=6 rules_after=6` · `3 3` · `4 4`) · `json_ok 4` · `python_parsed=9` | `rules_up=0` 셋(두 판이 같다) · JSON 줄 오류(새 파일 없음) · `python_parsed=5` | surface-recipes 끝 `#제목` → 셋째 줄 `MD018:0→1` · comment-analysis 앞쪽 첫 `##` 제목 앞에 `## 8. Fail-soft 정책` 을 넣은 사본 → 둘째 줄 `MD024:0→1` · surface-recipes 에서 빈 줄 뒤 첫 목록 바로 앞에 문장 한 줄을 넣은 사본 → 셋째 줄 `MD032:5→6` — 뒤 두 사본은 옛 측정(더한 줄만 세기)이 `new_warnings=0` 이었다 · 새 시험 파일 하나를 `{` 로 → JSON 줄이 오류 · 린터 자리를 없는 파일로 → `LINT_NOT_RUN` · 종료 코드 2 |
| DG-06 | `scope-isolation: PASS` · `doc-contracts: PASS` · `doc_checked=2 doc_mine=0` · `violators=0 mine=0` | — | 변형 `cross-phase` → `scope-isolation: FAIL` · `violators=1 mine=1` |

문장 삭제 사본(`p13d/del.sh` · 목록 `p13d/dl.txt`): SK-01 14 · SK-03 7 · SK-04 11 · SK-05 6 · SK-06 5 · SC-03 1 · SC-06 2 — 토큰 하나를 그 파일에서 한 번 지운 사본 46 개 모두
그 조건의 `m` 출력이 바뀌었다(`DROP 46 · NODROP 0 · MISSING 0`). 목록은 `p13d/mkdellist.py` 가 `m.sh` 의 `toks` 인자에서 뽑았고 surface-recipes 잰 방법 두 줄을 더했다.
내용 조건의 양성 · 음성 대조 스크립트는 `p13d/ctl.sh`(끝 판 사본을 한 군데씩 망가뜨린 21 경우)다. 예행 변형의 커밋 기록 대조는 `p13d/rh-<변형>` 에서 `m ER-03` · `m AR-01` · `m DG-06` 을 돌렸다.

## Skill

- [ ] SK-01: `bambu-kit/skills/bambu-print-profile/SKILL.md` 끝 절이 `## MakerWorld 읽는 순서` 로 바뀌어 네 단계(JSON 주소 → 브라우저 도구 — 서버 이름을 박지 않고 도구 목록에서 찾음 → Codex 위임 — 셸 `curl` 로 부르라고 주소를 그대로 넘김 → 사용자 입력)와 403 · `Just a moment...` 에서 기다리지 않고 다음 단계로 가는 규칙, 3mf 는 자동으로 받는다고 가정하지 않고 사용자에게 받기, 그 규칙이 공식 지침이 아니라 킷 운영 규칙이라는 문장, ``### JSON 주소 (`[관측 2026-09-24]`)`` 와 주소 셋의 표 행, 멈춤 규칙을 담고, 옛 제목 `## MakerWorld URL fallback 체인` 은 0, Phase 1 입력 분기 1 번이 그 절을 가리키고 옛 「Playwright MCP 1차」 는 0, `bambu-kit/` 전체에서 특정 브라우저 서버 이름(`playwright` · `mcp__`)이 든 줄과 `Cloudflare` · `우회` 가 같은 줄이 0 이다 (`F30` · `bambu:P1` · 러닝북 서버 이름 금지) — `m SK-01` 네 줄이 `1` 열둘 · `heads=1 old=0` · `1 0` · `names=0 bypass=0` [exact, enumerated]

- [ ] SK-02: 「MakerWorld 읽는 순서」 의 받는 법 블록을 근거 파일 관측 모양의 가짜 `curl` 로 돌리면 — bash · zsh 둘 다 요청 4 번(모델 · 프로파일 목록 · 댓글 offset 0 · 100)에서 멈추고 `comments total 159 · 받은 hits 159 (페이지 2) · comment 44 · ratingItem 115` 와 `NOTE` 한 줄(두 수가 다름)을 내며 종료 코드 0, 댓글 첫 페이지가 403 이면 다시 부르지 않고(요청 3 번) `FAIL` 한 줄 · 종료 코드 1 이다. 음성 대조: 멈춤 줄(`[ "$OFF" -lt "$TOTAL" ] || break`)을 지운 사본은 요청이 5 번이 되고, 첫 페이지에서 멈춘 사본은 `WARN` 을 낸다 (`bambu:P1` · 근거 §2 bambu:P5 페이지 표 · 알려진 답) — `m SK-02` 다섯 줄이 `bash/200 rc=0 req=4 offs=0,100 [comments total 159 · 받은 hits 159 (페이지 2) · comment 44 · ratingItem 115] note=1 warn=0 fail=0` · `zsh/200 rc=0 req=4 offs=0,100 [comments total 159 · 받은 hits 159 (페이지 2) · comment 44 · ratingItem 115] note=1 warn=0 fail=0` · `bash/403 rc=1 req=3 offs=0 [comments total None · 받은 hits 0 (페이지 0) · comment 0 · ratingItem 0] note=0 warn=0 fail=1` · `bash/200 rc=0 req=5 offs=0,100,159 [comments total 159 · 받은 hits 159 (페이지 3) · comment 44 · ratingItem 115] note=1 warn=0 fail=0` · `bash/200 rc=0 req=3 offs=0 [comments total 159 · 받은 hits 100 (페이지 1) · comment 44 · ratingItem 56] note=1 warn=1 fail=0` [exact]

- [ ] SK-03: SKILL.md 전체 크롤링 원칙이 댓글 수를 두 값(`commentCount` · `total`)으로 적고 받은 `hits` 수를 `total` 과 대조하며 두 값이 달라도 멈추지 않고, `hits` 원소마다 `comment` 와 `ratingItem` 을 각각 읽고 답글 배열도 따로 읽으며, 브라우저 스냅샷 경로는 JSON 을 못 받았을 때만 쓰고, 첨부 찾기는 대상 파일이 비었거나 없으면 0 건을 「첨부 0 개」 로 읽지 않도록 줄 수를 먼저 찍고 받은 JSON 의 문자열을 풀어 grep 한다 — 옛 `<snapshot-yml>` · 「Playwright `browser_evaluate`로」 · 「댓글 카운트 확인: 스냅샷에서」 는 0. 받은 뒤 첨부 블록을 bash · zsh 로 돌리면 줄 수 47 이 링크보다 먼저 나오고 PDF · GitHub 링크를 하나씩 찾으며, 빈 폴더에서는 줄 수 0 을 낸다 (`bambu:P1`) — `m SK-03` 다섯 줄이 `1` 일곱 · `0 0 0` · `bash lines=47 pdf=1 github=1 order=1` · `zsh lines=47 pdf=1 github=1 order=1` · `empty lines=0` [exact, enumerated]

- [ ] SK-04: `bambu-kit/skills/bambu-print-profile/references/comment-analysis.md` 머리 줄이 `> Last updated: 2026-09-25 (§4.1 JSON 먼저 · §8 읽는 순서 · 최초 2026-05-23)` 이고, `### 4.1 댓글 받기 — JSON 먼저, 50+ 도 전수` 가 JSON 주소로 전부 받기 · 50+ 도 sampling 안 함 · 원소마다 두 종류 · 두 수 · 브라우저 스냅샷은 JSON 을 못 받았을 때만을 담으며 옛 제목 `### 4.1 댓글 50+ 페이지 처리` 는 0, §4.3 첫 단계가 브라우저 도구 일반형, §8 이 새 순서를 가리키고 옛 체인(`Playwright → Codex → WebFetch`)은 0, §10 의 API 미해결 줄이 관측으로 풀렸다는 줄로 바뀐다 (`bambu:P1` · 근거 §3 `comment-analysis.md:335`) — `m SK-04` 여섯 줄이 그 머리 줄 · `1 1 1 1 1` · `1` · `1 0` · `1 0` · `old41=0` [exact, enumerated]

- [ ] SK-05: SKILL.md Phase 1.0 형상 측정 블록 뒤, 래티스 실측 문단 앞에 「측정 전에 알려진 답으로 한 번 돌린다」 문단 · 기대값 표(10 mm 정육면체 40.0 · planar / 2 mm 기둥 8.0 · thin / 벽 1 mm 관 `WALL_LOOPS=2` 예산 1.74 · 부족 비율 1.0 · 최소 살 1.0) · 자기 검사 블록이 있고, 그 블록을 끝 판에서 bash · zsh 로 돌리면 `OK` 셋 · `SELFTEST PASS` · `exit=0` 이다. 음성 대조: 측정 코드의 `THIN_LOOP_MM` 을 5 로 바꾼 사본과 벽 예산 식을 바꾼 사본은 각각 `FAIL` 하나 · `SELFTEST FAIL` · `exit=1` 이다 (`bambu:P6` · 설계 가이드 §3.7 알려진 답 대조) — `m SK-05` 일곱 줄이 `1` 여섯 · `order=1` · `end/bash ok=3 fail=0 SELFTEST PASS exit=0` · `end/zsh ok=3 fail=0 SELFTEST PASS exit=0` · `mutated=1,1` · `thin5/bash ok=2 fail=1 SELFTEST FAIL 1 개 — 실제 모델을 재지 말고 측정부터 고친다 exit=1` · `budget/bash ok=2 fail=1 SELFTEST FAIL 1 개 — 실제 모델을 재지 말고 측정부터 고친다 exit=1` [exact]

- [ ] SK-06: SKILL.md Phase 4.4 에 `**G-code 로 길이 재기 (2026-09-25 신규)**` 문단과 블록이 있어 — 알려진 답(직선 20 · 호 15.708. 호는 `G2` 3/4 호(반지름 2)와 `G3` 1/4 호(반지름 4)라 회전 방향을 뒤집거나 무시하면 값이 바뀐다) 자기 검사를 먼저 하고, 두 기능 · 절대 E · `G92` · `G91` · 한 바퀴 호 · 이동 줄을 섞은 둘째 알려진 답에서 `Outer wall` 직선 0.010 m · 호 0.031 m · 합 0.041 m · 76 % 와 `Sparse infill` 0.007 m · 0 % 를 내고, 기능 표시 0 줄 · R 로 적은 호 · 압출로 센 이동 0 개에서는 각각 `FAIL` · 종료 코드 1 로 멈춘다. 음성 대조: 호를 건너뛰고 좌표도 안 옮기는 사본, `G2` · `G3` 를 같은 방향으로 센 사본, 방향을 무시하고 각도 차의 절댓값을 쓴 사본은 셋 다 자기 검사에서 멈춘다. 점검 목록에 G-code 길이 줄 하나가 더해지고, `bambu-kit/skills/bambu-print-profile/references/surface-recipes.md` 의 G-code 실측 세 곳(갭필 표 · 허공 위 표 · 다림질 문단) 바로 뒤에 잰 방법 두 줄 인용이 하나씩, 머리 줄이 바뀐다 (`bambu:P5`) — `m SK-06` 스물세 줄이 `1 1` · `Outer wall: 직선 0.010 m · 호 0.031 m · 합 0.041 m · 호 비율 76%` · `Sparse infill: 직선 0.007 m · 호 0.000 m · 합 0.007 m · 호 비율 0%` · `rc=0 selftest=1` · ``FAIL: `; FEATURE: ` 줄이 0 개다 — 뱀부 · 오르카 G-code 가 아니거나 표시가 다르다. 빈 결과는 통과가 아니다`` · `rc=1 selftest=1` · `FAIL: R 로 적은 호는 재지 않는다 — I · J 호만 잰다: G2 X10 Y0 R5 E1` · `rc=1 selftest=1` · `FAIL: 기능 표시는 있는데 압출로 센 이동이 0 개다 — E 모드(M82 · M83)가 맞는지 본다` · `rc=1 selftest=1` · `mutated=1` · `FAIL: 알려진 답과 다르다 — 이 블록부터 고친다. 실제 G-code 는 재지 않았다` · `rc=1 selftest=0` · `mutated_dir=1` · `FAIL: 알려진 답과 다르다 — 이 블록부터 고친다. 실제 G-code 는 재지 않았다` · `rc=1 selftest=0` · `mutated_abs=1` · `FAIL: 알려진 답과 다르다 — 이 블록부터 고친다. 실제 G-code 는 재지 않았다` · `rc=1 selftest=0` · `1` · `> Last updated: 2026-09-25 (G-code 실측 세 곳에 잰 방법 · 2026-09-08 §2.7 형상 클래스 축 신설 · 최초 2026-05-16)` · `notes=3 next=3` · `after_ok=3/3` [exact]

- [ ] SK-07: 카이젠 스킬 Gotcha 3 · 5 를 지킨다 — SKILL.md Gotcha 체크리스트(`- ☐` 줄)는 시작 판 48 줄이 하나도 빠지지 않고 49 줄이 되며, 사용자 정책 키 `nozzle_temperature` 가 든 줄은 스킬 폴더 전체에서 시작 판과 글자 그대로 같다 (`.claude/skills/bambu-kaizen/SKILL.md` Gotcha 3 · 5) — `m SK-07` 두 줄이 `checklist=48→49 dropped=0` · `nozzle_same=1` [exact]

## Script

- [ ] SC-01: SKILL.md Phase 4.4 G-code 대조 스크립트가 칸마다 대조한다 — 끝 판에서 슬롯 2 만 다른 기록은 `MISMATCH bridge_speed 슬롯 2` · 종료 코드 1, 세 칸이 같으면 통과, 한 칸 설정은 모든 칸으로 펼쳐 슬롯 2 를 잡고, 칸 수가 다르면 짧은 쪽까지 비교하고 남는 칸을 `WARN` 으로 알리며, 따옴표 칸을 풀고, 기록에 키가 없으면 `보낸 값 없음` 이다. 음성 대조: 시작 판 스크립트는 슬롯 2 만 다른 기록을 통과시킨다 (`bambu:P2`) — `m SC-01` 일곱 줄이 `slot2 rc=1 MISMATCH bridge_speed 슬롯 2: 설정 '25' · 보낸 값 '50'|` · `same3 rc=0` · `one_vs_3 rc=1 MISMATCH bridge_speed 슬롯 2: 설정 '25' · 보낸 값 '30'|` · `len_diff rc=0 WARN bridge_speed: 칸 수가 다르다 — 설정 3 · 보낸 값 2. 슬롯 3 은 비교하지 않았다|` · `quoted rc=0` · `missing rc=1 MISMATCH bridge_speed: 설정 ['25'] · 보낸 값 없음|` · `start_slot2 rc=0` [exact]

- [ ] SC-02: SKILL.md Phase 4.4 값 박기 스크립트가 칸마다 박는다 — 끝 판에서 두 칸 설정 `["25","30"]` 은 그대로, 한 값은 프로젝트 칸 수만큼 채우고, 세 칸이 같으면 두 칸으로 채우며, 칸 수가 다르고 값이 칸마다 다르면 `FAIL` · 종료 코드 1 로 파일을 쓰지 않고, 스칼라 키는 그대로 박는다. 음성 대조: 시작 판 스크립트는 `["25","30"]` 을 `['25', '25']` 로 박는다 (`bambu:P2`) — `m SC-02` 여섯 줄이 `two_two rc=0 value=['25', '30'] fail=0` · `one_to_2 rc=0 value=['25', '25'] fail=0` · `same3_to_2 rc=0 value=['25', '25'] fail=0` · `diff3_to_2 rc=1 value=none fail=1` · `scalar rc=0 value=2 fail=0` · `start_two_two rc=0 value=['25', '25'] fail=0` [exact]

- [ ] SC-03: SKILL.md 에 `**두 스크립트 자기 검사 (2026-09-25 신규)**` 문단과 블록이 있어, 끝 판에서 bash · zsh 로 돌리면 대조가 `MISMATCH bridge_speed 슬롯 2` · `exit=1`, 값 박기가 `['25', '30']` 을 내고, 같은 블록에 시작 판 스크립트를 넣으면 `RESULT: PASS` · `exit=0` · `['25', '25']` 로 기대에서 떨어진다 (`bambu:P2`) — `m SC-03` 네 줄이 `1` · `bash MISMATCH bridge_speed 슬롯 2: 설정 '25' · 보낸 값 '50'|RESULT: FAIL 1 개|exit=1|['25', '30']|` · `zsh MISMATCH bridge_speed 슬롯 2: 설정 '25' · 보낸 값 '50'|RESULT: FAIL 1 개|exit=1|['25', '30']|` · `start RESULT: PASS|exit=0|['25', '25']|` [exact]

- [ ] SC-04: SKILL.md Phase 4.3 게이트가 옵션 목록을 읽은 뒤 `OPTION LIST <파일> canonical N · 종류 N · enum N` 을 찍고, 목록 파일이 있기만 하고 비었으면 `[미검증] … 목록이 비었거나 깨졌다. 키 존재 · 종류 · enum 값 검사 미실행` 한 줄을 낸다 — 정상 목록의 판정(키 스코프 불일치 FAIL)은 그대로다. 음성 대조: 시작 판 게이트는 빈 목록에서 목록 알림 없이 `RESULT: PASS` 다 (`bambu:P4`) — `m SC-04` 네 줄이 `normal rc=1 OPTION LIST bambu-02.08.02.61.tsv canonical 679 · 종류 552 · enum 56 fail=1` · `orca OPTION LIST orca-2.4.2.tsv canonical 749 · 종류 640 · enum 58` · `empty rc=0 empty_unv=1 fail=0 RESULT: PASS` · `start_empty rc=0 list_unv=0 RESULT: PASS` [exact]

- [ ] SC-05: `bambu-kit/scripts/option-key-probe/generate-option-list.py` 가 canonical · process · filament · machine · enum 중 0 줄인 종류가 있으면 파일을 쓰지 않고 종료 코드 1 로 멈추고, 다섯이 다 있으면 전처럼 쓴다. 음성 대조: 시작 판 생성기는 아무것도 안 내는 판정 프로그램으로도 파일을 쓰고 종료 코드 0 이다 (`bambu:P4`) — `m SC-05` 네 줄이 `end/probe-empty rc=1 written=none refused=1` · `end/probe-full rc=0 written=6 refused=0` · `start/probe-empty rc=0 written=1 refused=0` · `start/probe-full rc=0 written=6 refused=0` [exact]

- [ ] SC-06: SKILL.md 음성 대조 절이 시험 파일을 전수로 돈다 — 실행 블록을 끝 판에서 bash · zsh 로 돌리면 같은 출력에 `STOP` 0, 게이트를 뽑은 뒤 줄 수 · `RESULT` 줄 수를 찍고, 종료 코드 순서가 검사 유지 23 줄(FAIL 기대 20 · PASS 기대 3)과 지운 사본 · 변이 23 줄(전부 0)이며, 바뀐 줄 수 열넷이 모두 1 이고 합집합 변이 기준점 1 · 빈 목록 `[미검증]` 1 · 소재 칸 알림 줄 1(검사 유지 실행에서만 나오고 알림 줄을 지운 사본에서는 안 나온다)이다. 폴더의 시험 파일 23 개가 표 23 행과 이름이 같고, 새 넷이 각각 목표 위반 FAIL 하나만 내며 `[미검증]` 0, 「일곱 모두」 문장과 「아직 FAIL 시험 파일이 없다」 문장이 있다. 실행 줄 확인은 `TARGET_SLICER=` 로 시작하는 (2) 줄만 센다. 양성 대조: 실행 줄 하나 뺀 사본 둘(그중 하나는 빈 목록 변이 줄에도 이름이 나오는 `process-bambu-only-key-in-orca.json`) · 표 행 하나 뺀 사본 · 폴더에만 파일을 더한 사본 · 틀린 SKILL.md 경로 사본은 각각 빠진 이름이나 `STOP` 을 찍고 종료 코드 1 로 시험을 하나도 돌리지 않는다 (`bambu:P3` · `bambu:P4`) — `m SC-06` 열네 줄이 `bash_rc=0` · `zsh_rc=0` · `same=1 stop=0 gate_lines= 283 result_lines=1` · `exits=1111111111011111111110000000000000000000000000` · `mutations=1 1 1 1 1 1 1 1 1 1 1 1 1 1 anchor=1 empty_unv=1 slot_note=1` · `table_diff=0` · `fixtures=23 rows=23` · `process-flow-ratio-over:rc=1,fail=1,target=1,unv=0 process-scarf-ratio-over:rc=1,fail=1,target=1,unv=0 filament-retraction-over-parent:rc=1,fail=1,target=1,unv=0 process-elefant-foot-negative:rc=1,fail=1,target=1,unv=0` · `1 1` · `run rc=1 실행 줄에 없음 process-thin-baseline.json|STOP 표와 실행 줄을 먼저 채운다| exits=0` · `run2 rc=1 실행 줄에 없음 process-bambu-only-key-in-orca.json|STOP 표와 실행 줄을 먼저 채운다| exits=0` · `table rc=1 표에 없음 process-flow-ratio-over.json|STOP 표와 실행 줄을 먼저 채운다| exits=0` · `stray rc=1 표에 없음 process-stray.json|실행 줄에 없음 process-stray.json|STOP 표와 실행 줄을 먼저 채운다| exits=0` · `path rc=1 STOP 게이트를 못 뽑았다 — S 경로부터 본다| exits=0` [exact, enumerated]

## Error

- [ ] ER-01: 여덟 파일에 새로 생긴 URL 과 `.harness/.meta/kaizen-0924/phase13-notes.md` 의 URL 이 전부 이 Phase 의 외부 근거 파일 `.harness/.meta/evidence/phase13.md` 에 있다 — 여덟 파일은 파일마다 편집 전 판과 비교하고, 주소 틀(`<번호>` · `$ID` · `<N>` · `$OFF`)은 근거 파일의 관측 모델 번호 `1186414` · offset `0` 으로 맞춰 대조한다 (러닝북 — 근거 파일에 없는 URL 을 지어내지 마라 · notes 킷 로그의 출처 URL 은 근거 파일에서만) — `m ER-01` 두 줄이 `0` · `0` [exact, enumerated]

- [ ] ER-02: 여덟 파일에 더한 줄에 번역투 6 종(`tone-kit/references/locale-korean.md` §2 치환표의 grep 열)과 특정 앱 · 브라우저 서버 이름(`fit-pal` · `fitpal` · `fit_pal` · `flutter-playwright` · `playwright` · `mcp__` · `chrome-devtools-mcp` 모양)이 0 건이다 (러닝북 말투 규칙 · 이름 금지) — `m ER-02` 가 `added=N k02=0 names=0` 이고 N 은 1 이상 [exact]

- [ ] ER-03: 이 Phase 범위 밖과 미반영을 명시적 미완으로 넘기고 공유 파일 · 다른 Phase 파일을 건드리지 않는다 — `.harness/.meta/kaizen-0924/phase13-notes.md` 가 `$END` 에 커밋돼 있고, 문자열 스물하나(처리 배정표 키 `` `F30` `` · `bambu:P1` ~ `bambu:P6`, 넘김 `.claude/skills/bambu-kaizen/SKILL.md` · `.claude/skills/bambu-research/SKILL.md` · `docs/bambu-kit/bambu-print-profile.html` · `feat/bambu-kit-orca-h2s-feedback` · `bambu-fields-baseline.md` · `네 칸` · `plugin.json`, 러닝북 여섯 절 제목 `## 바꾼 파일` · `## 반영한 처리 배정표 키` · `## 미반영 키와 사유` · `## changelog 한 단락` · `## 킷 로그 한 단락` · `## 다음 사이클 메모` 와 넘김 절 제목 `## 넘기는 것`)이 각각 1 줄 이상이며, 넘김 셋은 사유와 같은 줄에 각각 1 줄 이상 있고(`feat/bambu-kit-orca-h2s-feedback` 과 `충돌` · `네 칸` 과 `SKILL.md:1706` · `bambu-fields-baseline.md` 와 `/bambu-research`), 구간 안에서 공유 파일 · 다른 Phase 파일을 건드린 커밋 가운데 다른 Phase 서명이 없는 커밋이 0 이다 — `m ER-03` 네 줄이 `notes_committed=1` · 스물하나가 각각 1 이상 · 세 값이 각각 1 이상 · `0` [exact, enumerated]

## Architecture

- [ ] AR-01: 이 Phase 의 변경이 허용 경로 안에 머물고, 범위 선언 블록이 그 경로와 같으며, 이 계약이 봉인돼 있다 — `bambu-kit/` 를 건드린 구간 안 커밋이 전부 서명했고, 서명 커밋이 고친 `.harness/` 밖 경로가 여덟 파일뿐이며(여덟 전부 포함), 서명 커밋이 건드린 계약 가운데 봉인이 깨진 것이 0, 이 계약이 `SEAL_OK`, `## 범위 경계` 의 `# sprint-scope` 블록이 여덟 경로와 `.harness/` 한 줄이다 — `m AR-01` 여섯 줄이 `0` · `0 8` · `0` · `SEAL_OK` · `scope_same=1` · `1` [exact, enumerated]

- [ ] AR-02: 새 문장이 가리키는 자리가 실제로 있다 — `## MakerWorld 읽는 순서` 제목이 1 개이고 그 절 이름 인용이 SKILL.md 3 · comment-analysis 3, `**G-code 로 길이 재기 (2026-09-25 신규)**` 표지가 1 개이고 인용이 SKILL.md 1 · surface-recipes 3, SKILL.md 가 인용하는 comment-analysis §4.1 제목(`###` 다음 `4.1`)이 1 개이고 인용 1, 두 자기 검사가 인용하는 `harness/docs/guides/skill-design-guide.md` `## 3.7.` 안에 `#### 0 이 아닌 값을 내는 새 측정 — 알려진 답 대조` 가 1 개다 — `m AR-02` 세 줄이 `order_head=1 order_refs=3/3` · `len_head=1 len_refs=1/3` · `ca41=1 sk_ref41=1 guide=1` [exact, enumerated]

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다. 이번 변경에 적용: 여덟 파일에 더한 줄에 bambu-kit `plugin.json` 의 `version` 값(`$END` 판에서 읽는다)이 0 건이다 — 이 Phase 는 킷 버전을 적지 않고 Final 이 올린다. 설치본 · 옵션 목록 버전(`02.08.02.61` · `2.4.2`)과 3MF 규격 판(`1.4.0`)은 사실 문장이라 이 패턴의 대상이 아니다 — `m AP-01` 이 `version=<값> 0` [exact]

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```` ```text, ```bash, ```yaml ```` 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 이번 변경에 적용: 바뀐 마크다운 셋은 모두 `bambu-kit/` 안이라 V6 가 읽는다 — `m DG-05` 첫 두 줄이 `10 0 rc=0` · `tf_mine=0` 이다 [exact]

- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL. 이번 변경에 적용: `bambu-kit/skills/bambu-print-profile/SKILL.md` 첫 frontmatter 블록이 편집 전과 글자 그대로 같고 `name: bambu-print-profile` 줄이 1 개다 — 그래서 트리거 설명(카이젠 스킬 Gotcha 4)과 README AUTO 구간이 읽는 값도 바뀌지 않는다 — `m AP-04` 가 `1/1` [exact]

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다. 이번 변경에 적용: 새 재사용 단위 코드를 만들지 않는다 — 새 파일은 시험 입력 JSON 넷뿐이고 킷 공용 폴더 `bambu-kit/evals/gate-fixtures/` 에 둔다. 새 자기 검사 셋은 SKILL.md 안의 블록이다 — `m RE-01` 이 `filament-retraction-over-parent.json` · `process-elefant-foot-negative.json` · `process-flow-ratio-over.json` · `process-scarf-ratio-over.json` 네 경로(`bambu-kit/evals/gate-fixtures/` 아래)만 낸다. 양성 대조: 끝 판 사본에 `x.json` 을 더하면 다섯 줄 [exact, enumerated]
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다. 이번 변경에 적용: 자기 검사는 측정 · 값 박기 · G-code 대조 코드를 베끼지 않고 SKILL.md 에서 뽑아 돌리며, 새 시험 파일의 지운 사본은 기존 `drop()` 을 쓴다 — SKILL.md 에 `def wall_budget_shortfall(loops, budget):` · `DIFF_SLOT = {"process": 0, "filament": 1}` · `recorded, in_block = {}, False` · `drop() {` 가 각각 1 줄 — `m RE-02` 가 `1 1 1 1`. 양성 대조: 측정 함수 머리를 한 번 더 적은 사본은 첫 값 `2` [exact]

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `m DG-01` 이 `0`(서명 커밋이 고친 경로에 `scripts/release.sh` 가 0 줄). 이번 변경의 스크립트 조각은 SK-02 · SK-03 · SK-05 · SK-06 · SC-01 ~ SC-06 이 실제로 돌린다)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (`diagnostics.ide_exclude` 값 `[]`) — 이번 변경에 적용: 편집기 마크다운 확장과 같은 조건(markdownlint-cli2 0.23.2 · MD013 끔)으로 마크다운 셋을 파일마다 편집 전 판과 끝 판 두 번 돌려 **규칙마다 경고 수**를 비교하면 늘어난 규칙이 0 이고 린터가 여섯 번 다 돌았으며(`LINT_NOT_RUN` 0), 새 시험 파일 넷이 JSON 으로 읽히고, SKILL.md 의 파이썬 조각 일곱 · 게이트 · 생성기가 파이썬 문법으로 읽힌다(아홉) — `m DG-02` 다섯 줄이 `rules_up=0` 으로 끝나는 줄 셋 · `json_ok 4` · `python_parsed=9`. 더한 줄의 경고만 세지 않는다 — 손대지 않은 옆 줄에 붙는 새 MD024 · MD022 · MD032 도 센다. 양성 대조: comment-analysis 첫 `##` 제목 앞에 기존 `## 8. Fail-soft 정책` 과 같은 제목을 넣은 사본은 둘째 줄이 `rules_up=1 MD024:0→1`, surface-recipes 에서 빈 줄 뒤 첫 목록 바로 앞에 문장 한 줄을 넣은 사본은 셋째 줄이 `rules_up=1 MD032:5→6` 이다 (두 사본 모두 새 경고가 손대지 않은 줄에 붙어 더한 줄만 세는 측정은 0 을 낸다). 편집 전부터 있던 경고는 수가 늘지 않으면 고치지 않는다(`범위 경계` 절) [exact]
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: DG-01 과 같은 `m DG-01` 이 `0`. 실제 시험은 SK-02 · SK-05 · SK-06 · SC-01 ~ SC-06)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 바뀐 코드 파일은 옵션 목록 생성기 하나이고 SC-05 가 실제로 돌린다. 측정: `m DG-04` 가 `0`(서명 커밋이 고친 경로에서 생성기와 `.harness/` 를 뺀 코드 파일 수). 양성 대조: 같은 거르개에 `bambu-kit/scripts/x.py` 를 넣으면 1)
- [ ] DG-05: 저장소 검사가 이 킷을 문제로 가리키지 않는다 — `$END` 판을 git 저장소로 만든 사본에서 (a) `scripts/validate-plugin.py bambu-kit` 출력에 `V1` ~ `V10` 열 줄이 있고 전부 `— OK` 로(V2 는 `— SKIP (no templates/)`) 끝나며 종료 코드 0 이다 — V 줄 머리에는 FAIL 이 안 찍히고 들여쓴 다음 줄에 찍혀서, V 줄에서 FAIL 낱말을 세면 맨 펜스를 못 잡는다 (b) 전체 킷 `--check=table-integrity,code-fence` 의 `FAIL` 줄 가운데 이 Phase 파일을 가리키는 줄 0 (c) `scripts/sync-docs.py --check-only` 가 종료 코드 0 또는 1 에 앞 공백 둘이 붙은 `bambu-kit/README.md: 동기화됨` 줄 1 개 — 종료 코드 1 은 다른 킷 README 때문에도 나므로 이 킷 줄로 가른다 — `m DG-05` 세 줄이 `10 0 rc=0` · `tf_mine=0` · `sync_docs_rc=<0 또는 1> 1` [exact]
- [ ] DG-06: `python3 scripts/validate-post-kaizen.py --since 499cc1289f0f5ae5649da601515725f49f4f1096` 출력에 `scope-isolation` 줄과 `doc-contracts` 줄이 각각 1 개 있고, 둘 다 `FAIL` · `ERROR` 가 아니다(`PASS` · `SKIP` 은 통과). 두 줄 가운데 하나라도 없으면 FAIL 이다. `docs-site-regen` 은 Final F2 몫이라 판정에서 뺀다. 다른 Phase 커밋 때문에 `scope-isolation` 이 `FAIL` 이면 `--verbose` 위반 커밋 목록이 1 개 이상 읽혔고(`violators` 1 이상) 그 안에 이 Phase 서명 커밋이 없을 때(`mine=0`)만 PASS 다. 상태와 상관없이 `python3 scripts/validate-doc-contracts.py -v` 의 `검사:` 줄 경로가 1 개 이상 읽혔고(`doc_checked` 1 이상) 그 가운데 이 Phase 파일이 0 개다(`doc_mine=0`) — 다른 Phase 파일 때문에 `doc-contracts` 가 `FAIL` · `ERROR` 여도 이것이 맞으면 PASS 다 — `m DG-06` 네 줄이 `scope-isolation: <상태>` · `doc-contracts: <상태>` · `doc_checked=<1 이상> doc_mine=0` · `violators=<N> mine=0` [exact]
