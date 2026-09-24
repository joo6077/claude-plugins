---
feature: "카이젠 2026-09-24 Phase 2 계약 — 준비 단계 실측 · 알려진 답 대조 · 기능 조건 수 · 시각은 date 출력 · 도구 없는 세션 · 여러 주체 커밋 범위 · 자기진단 true 뜻 고정"
slug: kaizen-0924-p02-contract
created: "2026-09-24 21:20"
complexity: "복잡"
conditions: 28
status: active
owner_session: de8c7935-a5b6-4df5-9106-fafa73c288a0
conditions_digest: sha256:76b807f6d67fcf8a
locked_at: "2026-09-24 22:19"
---

## 배경

이 Phase 의 외부 근거는 `.harness/.meta/evidence/phase2.md` 하나다. 처리 배정표(`.claude/kaizen-input/insights-report.md`)에서
`배정` 칸이 `Phase 2` 인 행은 11 개다. 러닝북 Phase 2 추가 과제가 둘 있고, 카이젠 스킬 Step 2 의 피드백 분석에서 하나를 더 찾았다.

| 키 | 내용 | 이번 처리 |
| --- | --- | --- |
| `harness:P03` · `F12` | 면제는 값에만 — 재는 명령의 준비 단계는 봉인 전에 돌려 봄 · 돌려 보지 않은 명령으로 QA REJECT | 반영 — SK-01 |
| `harness:P05` · `F17` | 알려진 답 대조 소절 · 측정 스크립트 자체 버그 | 계약 측 반영 — SK-02 (생성 측 §3.7 은 Phase 1 이 넣었다) |
| `user-setup:P5` | contract-schema 셸 이식성 절에 zsh 배열 한 줄 | 반영 — AR-04 (`harness:P05` 의 zsh 줄과 같은 줄이라 한 번만) |
| `harness:P06` · `F11` | 조건 수를 작업 크기에 맞추고 끝에 사용자가 할 일 한 줄 · 한 줄 수정이 무거운 절차에 묻힘 | 반영 — SK-03 · SK-04. `/sprint` 쪽 두 자리는 Phase 4 로 넘김 |
| `harness:P08` · `F13` | `created` · `Evaluated` 시각을 date 출력으로 · 짐작한 시각 때문에 REJECT | 계약 측 반영 — SK-05. `Evaluated` 는 Phase 3 으로 넘김 |
| `F21` | 도구 없는 세션에서 0 단계 멈춤 (맡은 제안 0 개). 근거 파일 §4-7 · §5 는 대체 경로가 없는 필수 도구가 없을 때만 멈추고 대체 경로가 있으면 멈추지 말라고 가른다 | 반영 — SK-06 (셸이 없으면 멈추고, 파일 쓰기 도구만 없으면 셸로 쓴다) |
| `F27` | 스스로 검증하는 계약 — 조건마다 명령 · 출력 · 종료 코드, 계약 검사기, 크기 검사 | SK-01 (명령 · 종료 코드) · SK-03 (기능 조건 수 계산 명령) 으로 반영. 계약 검사기 부분(`harness:P02`)은 Phase 4 |
| 러닝북 추가 과제 1 — 메타 이슈 1 (`.harness/.meta/phase4-handoff-to-contract.md` F1~F4) | 계약 파일 단위 범위 열거가 여러 커밋 스프린트에서 반복해서 깨짐 | F1 은 2026-09-23 스키마 §`.harness/` 범위 조건 에 이미 있다 — `SKILL.md` 쪽 안내만 더한다. F2 · F3 · F4 반영 — AR-01 · AR-02 · AR-03 |
| 러닝북 추가 과제 2 — F11 크기 규칙 | 단순 「총 4-6 개」 대 자동 포함 최소 11 줄 | 반영 — SK-03 |
| 피드백 분석 (카이젠 Step 2) | 자기진단 체크리스트의 true 뜻이 섞였다 | 반영 — SK-07 |

고칠 것은 일곱 갈래다.

1. **준비 단계 실측 (P03 · F12 · F27).** 스키마 §미실측 오라클 봉인 금지 는 「구현이 만들 값」 을 면제한다
   (`contract-schema.md:655-657`). 이 면제를 명령 전체의 면제로 읽어 한 번도 돌려 보지 않은 명령이 봉인됐다. 실측
   (데이터 풀 §1, 2026-09-22 REJECT): 계약이 `PATH=/usr/bin:/bin` 으로 `jq` 를 숨긴다고 전제했는데 이 기계의 `jq` 는
   `/usr/bin/jq` 라 숨겨지지 않았다. 이 초안이 그 전제를 다시 돌려 확인했다 — 아래 `회귀 게이트` 절.
2. **알려진 답 대조 계약 측 (P05 · F17).** Phase 1 이 생성 측(`skill-design-guide.md` §3.7)을 넣으며 「평가자는 이 대조를
   계약 조건으로 받는다」(§11 parity 16 행)고 적었는데, 계약 스키마에는 받을 형식이 없다. zsh 배열 첨자 규칙 문장도
   「계약 측 문서가 맡는다」고 넘겨져 있다.
3. **조건 수 (P06 · F11).** 옛 가이드는 전체 조건 줄을 센다 — 단순 「총 4-6 개」(`SKILL.md:455` · `contract-schema.md:1120`).
   이 레포(카테고리 4 개)에서 가장 작은 계약은 카테고리마다 한 줄 · 금지 패턴 한 줄 · 자동 포함 여섯 줄로 11 줄이라 지킬 수
   없다. 금지 패턴 「최소 2 개」 규칙(`SKILL.md:38` · `contract-schema.md:866` · 가이드 `:1102` · `red-flags.md:7`)도 Step 3 의
   `AP-00: N/A` 와 어긋난다. DRAFT 끝의 「사용자가 할 일」 한 줄도 없다.
4. **시각 필드 (P08 · F13).** frontmatter 틀이 `created: "{YYYY-MM-DD HH:mm}"` 을 손으로 채우게 둔다(`SKILL.md:569` ·
   `contract-schema.md:191`). 이번 사이클에도 재발했다 — Phase 1 개정 파일에 `created: "2026-09-24 20:50"` 이 적혔는데 그 파일을
   처음 담은 커밋 `fc29b58` 은 `20:41:11` 이다 (`76cfb37` 에서 고쳤다).
5. **도구 없는 세션 (F21).** 데이터 풀 §0-b `858c246f`: 도구가 하나도 없는 세션에서 이 스킬이 0 단계에서 멈췄다. 멈춘 것은
   옳았다. 규칙이 없어 다음에도 그렇게 멈춘다는 보장이 없다. 멈출 조건은 셸 하나다 — 확인 단계가 전부 명령 출력이라 셸은
   대체 경로가 없고, 파일 쓰기는 셸로 대신할 수 있다 (근거 파일 §4-7).
6. **메타 이슈 1 남은 것 (F2 · F3 · F4).** 확인 결과:
   - F1(부기 경로를 구현 경로 열거에 넣지 마라) — 스키마 `:572-600` §`.harness/` 범위 조건 이 `verify_seal` 로 이미 해결했다.
     `SKILL.md` 에는 이 절을 가리키는 말이 없다
   - F2(커밋 뒤 빈 출력이 되는 상태 전제) — 반영 안 됨. 스키마 표준형 예시(`:563-568`)가 여전히
     `Given: 커밋 직전 working tree` · `git diff --name-only HEAD` 이고, 가이드 `:713` 은 「커밋 후 판정이 전제라면 … `--cached`
     를 사용한다」 고 적어 **커밋 뒤에 늘 빈 집합을 재게 한다**. 아래 `회귀 게이트` 절의 스크래치 저장소 실측이 이를 보인다
   - F3(구간에 남의 커밋이 섞임) — 반영 안 됨. v5.4 §커밋 구간 상한 은 `sprint/<slug>` 가지 관례만 다룬다. Phase 1 이 서명 줄
     `Kaizen-Phase:` 로 풀었지만 그 계약에만 있다(`phase1-notes.md` 다음 사이클 메모)
   - F4(검사 전체 통과를 조건으로 걸면 이 스프린트가 만들지 않는 줄까지 책임진다) — 반영 안 됨. 2026-09-24 에 재발했다 — 데이터
     풀 §1 REJECT `insights-0924-kaizen` DG-03 (「validate-post-kaizen.py 가 docs-site-regen · scope-isolation 2 건 FAIL」),
     개선 제안 태그는 `측정-환경-오염`
7. **자기진단 true 뜻 (피드백 분석).** `SKILL.md` Step 7 의 23 항목 가운데 12 개가 「했는가」(true = 좋음)로, 나머지는
   「있는가 · 빠졌는가」(true = 문제)로 묻는다. 최근 계약 피드백 40 건 가운데 그 항목이 있는 31 건 중 20 건이
   `nfr_coverage: true` 다 (2026-09-24 21:49 기준. 피드백이 늘면 바뀌는 값이라 잰 시각을 붙인다 — 초안을 쓴 21:0x 에는 19 건).
   문항이 「반영되었는가」라 대부분 「반영했다」 는 뜻이다. 카이젠 Step 2 는 「true 가 최근 10 건 중 3 회 이상」을 반복 실패로 세므로 이
   항목은 매 사이클 반복 실패로 잘못 잡힌다. 측정 명령은 `회귀 게이트` 절에 있다.

근거 파일 밖의 파일 안 모순 셋도 고친다 (외부 근거가 필요 없다): 스키마 현재 판 `v5.4` 인데 `v5.5 추가` 표기가 이미 있다
(`contract-schema.md:817` · `SKILL.md:459`), `SKILL.md:772` · 가이드 `:1121` · `:1147` 이 v5.4 가 5 요소로 늘린 표준형을
여전히 「4 요소」로 적는다, 가이드 버전 정보(`:1293-1294`)가 스키마 `v5.3` · skill 가이드 `1.5.0` · agent 가이드 `1.6.0` 을 적는다.

## 리서치 소스

외부 조회 0 회. 아래 URL 은 전부 근거 파일 `.harness/.meta/evidence/phase2.md` 에서 가져왔다.

- [POSIX.1-2024 `command`](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/command.html) — `command -v` 는 못 찾으면 출력 없이 0 보다 큰 종료 코드, 셸 내장 · 함수도 보고한다 (P03)
- [zsh Array Parameters](https://zsh.sourceforge.io/Doc/Release/Parameters.html#Array-Parameters) · [GNU Bash Arrays](https://www.gnu.org/software/bash/manual/html_node/Arrays.html) — zsh 일반 배열은 기본 옵션에서 1 부터(`KSH_ARRAYS` 예외), bash 는 0 부터 (P05 · user-setup:P5)
- [Gherkin Best Practices](https://github.com/andredesousa/gherkin-best-practices) — 조건을 짧게, 한 조건에 한 규칙. 개수는 주지 않는다 (P06)
- [GNU Coreutils `date`](https://www.gnu.org/software/coreutils/manual/html_node/date-invocation.html) — `date +format` (P08)

근거 파일이 스스로 밝힌 한계를 그대로 옮긴다: 기능 조건 1~3 · 4~8 · 9~20 이라는 수를 지지하는 외부 연구는 없다(레포 내부
정책으로 적는다). 「사용자가 할 일」 끝맺음과 「도구가 없으면 0 단계에서 멈춘다」의 직접 근거는 없다 — 도구가 이후 모든 단계의
필수 전제이고 대체 경로가 없을 때만 멈춘다는 추론을 따른다. 알려진 답 입력 2~3 줄은 레포 관례다.

내부 입력: 데이터 풀 §0 처리 배정표 · §0-b `8fa13c90` (F11 · F12) · `858c246f` (F21) · `d204ea78` · `be3037df` (F17) ·
`f5b7f3a5` (F13) · §1 최근 REJECT 사유 · Improvement (2026-09-22 ER-02 · AR-04, 2026-09-24 DG-03) · 글로벌 계약 피드백
`~/.harness/feedback/contract/` 최근 40 건의 checklist.

## GAP 분석 · 개선안 초안

### 1.1 복잡도 4 축

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 3 — 계약 형식 정의(스키마) · 스킬 절차 · 설계 가이드 (+ `red-flags.md`) |
| 공개 API·계약 변경 | 외부에 노출된 형태가 바뀌는가 | 예 — 스키마 v5.4 → v5.5 (조건 패턴 하나 추가, 조건 수 정의 변경, 자기진단 항목 둘 추가와 true 뜻 고정) |
| 소비면 존재 | 이 문구를 받아 쓰는 반대편이 있는가 | 예 — 아래 Counterpart 표 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — contract-kaizen 회귀 확인 패턴 6 개(`harness/evals/kaizen/contract-kaizen/assertions.json`), V6 · V9 · V10 검사, 다른 문서가 인용하는 절 이름 |

4 축 가운데 3 축이 「예」이고 공개 계약 변경과 소비면이 둘 다 「예」라 **복잡**이다. Step 2.5 Counterpart 조건을 넣는다 (ER-03).
기능 조건은 19 개다 — 이 계약이 새로 정하는 복잡 9~20 안이다 (SK-03 (d) 의 계산식으로 이 파일을 세면 19).

### 1.2 설정 리터럴 대조표

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A 사유에 그대로 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A 사유에 그대로 |
| `diagnostics.ide_exclude` | `[]` | DG-02 에 그대로 |
| `contract_categories[].id` / `prefix` | `Skill`/`SK` · `Script`/`SC` · `Error`/`ER` · `Architecture`/`AR` | 조건 섹션 제목과 접두 그대로 |
| `anti_patterns[].id` / `message` | AP-01 · AP-02 · AP-03 · AP-04 | AP-01 · AP-03 선별, message 원문 그대로. AP-02(force push)는 이 Phase 가 밀어 넣지 않아서, AP-04(SKILL.md · agents 의 `name`)는 frontmatter 를 바꾸지 않아서 뺀다 |

### 1.4 편집 전 감사 (실제로 읽은 줄 — 시작 커밋 `76cfb37` 판)

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 |
| --------- | ---------------------------- | ------------------- | ----------- |
| `harness/references/contract-schema.md` | `:636-659` (미실측 오라클 · 면제 `:655-657`) | 면제가 준비 단계까지 덮는 것으로 읽힌다 | SK-01 |
| 같은 파일 | `:817-827` (양성 대조) · `:829-857` (preflight 표 10 태그) | 0 이 아닌 기대값 형식 없음 | SK-02 · AR-03 |
| 같은 파일 | `:1116-1122` (조건 수 표) · `:859-867` (§2 최소 2개 `:866`) | 전체 줄 수 기준 · `AP-00` 예외 없음 | SK-03 |
| 같은 파일 | `:187-199` (frontmatter · `created` `:191`) | 시각을 손으로 채우는 틀 | SK-05 |
| 같은 파일 | `:555-570` (표준형 예시 `:563-568`) · `:572-600` · `:602-634` | 예시가 5 번째 요소를 빼고 커밋 뒤 빈 출력이 되는 전제를 쓴다. 여러 주체 커밋 규칙 없음 | AR-01 · AR-02 |
| 같은 파일 | `:74-99` (셸 이식성) | zsh 배열 첨자 없음 | AR-04 |
| 같은 파일 | `:5` (최근 갱신) · `:1124-1126` (현재 v5.4) | `v5.5 추가` 표기와 어긋남 | AR-05 |
| `harness/skills/sprint-contract/SKILL.md` | `:32-75` (Gotchas 42 개 · `:38` 최소 2개 · `:58` 미실측) | 준비 단계 · 기능 조건 · 여러 주체 커밋 안내 없음 | SK-01 · SK-03 · AR-06 (Gotchas 는 덧붙이기만) |
| 같은 파일 | `:130-160` (Step 0) | 도구 없는 세션 규칙 없음 | SK-06 |
| 같은 파일 | `:454-467` (조건 수 · 패턴 4 종 표) · `:545-548` (Step 5) · `:565-599` (frontmatter 틀) · `:621-632` (6.2) | 위 3 · 4 번 | SK-02 · SK-03 · SK-04 · SK-05 |
| 같은 파일 | `:758-784` (Step 7 23 항목 · `:767` · `:772` · `:775`) | true 뜻 섞임 · 4 요소 | SK-07 · AR-01 |
| `harness/docs/guides/contract-design-guide.md` | `:1-5` · `:678-723` (표준형 4 요소 · `:713` `--cached`) · `:749-757` (`:757` 패턴 4 종) | 4 요소 · 커밋 뒤 빈 집합 규칙 | AR-01 · SK-02 |
| 같은 파일 | `:1097-1126` (안티패턴 표 `:1102` · `:1121`) · `:1130-1153` (체크리스트 19 행) · `:1213-1246` (parity 7 행) · `:1285-1294` (버전 정보) | 최소 2개 · true 뜻 섞임 · 15 · 16 행 없음 · 옛 버전 | SK-02 · SK-03 · SK-07 · AR-05 |
| `harness/skills/sprint-contract/references/red-flags.md` | `:7-8` | 최소 2개 · 전체 조건 수 | SK-03 |
| `harness/agents/qa-evaluator.md` | `:590` (표준형 4 요소) · `:1217` (가이드 `v4`) | Phase 3 범위 — 넘김 | ER-03 |
| `harness/docs/guides/qa-evaluation-guide.md` | `:12` (스키마 v5.3) · `:746` (4 요소) · `:1915` (Parity with 가이드 v5.0) | Phase 3 범위 — 넘김 | ER-03 |

구현 후보 옵션은 하나씩만 두었다. 둘 이상이었던 두 곳의 선택:

- 메타 이슈 F4 를 새 결함 태그 `측정-소유권-초과` 로 넣을지 — **넣지 않는다.** 태그 표는 평가자와 같이 쓰는 공통 어휘라
  (`contract-schema.md:831-836`) Phase 3 파일까지 같이 바꿔야 한다. 2026-09-24 REJECT 의 개선 제안도 기존 태그
  `측정-환경-오염` 을 붙였다 — 그 태그의 한 형태로 적는다 (AR-03 이 태그 행 10 개 유지를 잰다)
- `SKILL.md:38` 「안티패턴 최소 2개」 Gotcha 를 고칠지 — **고치지 않는다.** contract-kaizen Gotcha 가 기존 Gotcha 를 덧붙이기만
  허용한다. 예외는 새 Gotcha 로 덧붙인다 (SK-03 (e) · AR-06 이 옛 Gotcha 42 줄이 그대로인지 잰다)

### Counterpart — 바뀌는 규약을 받아 쓰는 반대편

| 파일 | 인용 | 이번 처리 |
| --- | --- | --- |
| `harness/agents/qa-evaluator.md:590` | 「Diff-Scope Oracle 표준형 4 요소 … 중 빠진 것을 REJECT 사유에 열거」 | Phase 3 — 넘김 (ER-03) |
| `harness/agents/qa-evaluator.md:1217` | 「contract-design-guide.md — 계약 작성 가이드 v4」 | Phase 3 — 넘김 (ER-03) |
| `harness/docs/guides/qa-evaluation-guide.md` (`:12` · `:746` · `:1915`) | 스키마 v5.3 · 표준형 4 요소 · Parity with 가이드 v5.0 (가이드 `:1292` 가 「둘을 같이 올린다」) | Phase 3 — 넘김 (ER-03) |
| `harness/agents/qa-evaluator.md:590` · `harness/docs/guides/qa-evaluation-guide.md:742-743` | 상태 전제 확인이 `커밋 직전 working tree` · `스테이징 완료 후` · 브랜치 비교만 나열 — AR-01 이 첫 선택지로 올리는 `이 스프린트의 커밋이 끝난 뒤` 가 없다 | Phase 3 — 넘김 (ER-03) |
| `harness/docs/guides/qa-evaluation-guide.md:1785` | 평가자가 계약 수정 제안을 쓰는 예시 「`Given: 스테이징 완료 후` 를 붙이고 `--cached` 를 쓸 것」 — AR-01 이 커밋 뒤에 늘 빈 집합을 잰다고 고치는 옛 규칙을 평가자에게 가르친다 | Phase 3 — 넘김 (ER-03) |
| `harness/docs/guides/qa-evaluation-guide.md:1862` | Parity Table 머리 「9 개」 · 15 행까지만 있고 16 행(알려진 답 대조)이 없다 — contract-kaizen Gotcha 「Cross-Surface Parity 전파 누락 금지」가 넘김으로 적게 하는 빈 곳 | Phase 3 — 넘김 (ER-03) |
| 같은 두 파일 — `Evaluated` 시각 | `harness:P08` 비고 「qa-evaluator 쪽 Evaluated 는 Phase 3 과 맞춘다」 | Phase 3 — 넘김 (ER-03) |
| `harness/skills/sprint/SKILL.md` | `harness:P06` 의 `/sprint` QA 결과 블록 · 6 단계 보고 끝 「사용자가 할 일」 | Phase 4 — 넘김 (ER-03) |
| `harness/scripts/save-feedback.sh` · `SKILL.md` Step 9 | `harness:P02` 비고 「sprint-contract 9 단계 문구는 Phase 2 와 맞춘다」 — 스크립트가 아직 안 바뀌어 문구를 먼저 바꾸면 틀린 안내가 된다 | Phase 4 가 스크립트를 바꾼 뒤 Step 9 문구를 맞춘다 — 넘김 (ER-03) |
| `harness/references/feedback-schema.yaml` · `harness/skills/contract-kaizen/SKILL.md` Step 2 | 자기진단 true 뜻 — 스키마 예시는 true = 문제로 읽히지만 적혀 있지 않다. 2026-09-24 이전 피드백은 뜻이 섞였다 | Phase 4 — 넘김 (ER-03) |
| 러닝북 · 오케스트레이터 | Phase 계약의 서명 줄 규약 | Final — notes 에 적는다 (ER-03) |

### 개선안 초안

정확한 문구는 스크래치 `mock.py`(아래 `회귀 게이트` 절 경로 — 검토 반영판 `p2draft2/mock.py`)가 네 파일 시작 커밋 판에
적용하는 치환 그대로다. BUILD 는 이것을 기준으로 적용한다. 요지:

스키마 (`contract-schema.md`, v5.5):

- §셸 이식성 규약 에 불릿 하나 — zsh 배열은 기본 옵션에서 1 부터(`${arr[0]}` 은 빈 값), `KSH_ARRAYS` 와 bash 는 0 부터, 두 셸에서
  도는 코드는 `for x in "${arr[@]}"`. 실측 2026-09-22, zsh · Bash 매뉴얼 링크
- §메타데이터 yaml 의 `created:` 줄에 주석 `# 저장하는 순간 date '+%Y-%m-%d %H:%M' 출력을 옮긴다`, 블록 뒤 문단 「시각 필드는
  `date` 출력을 옮긴다 — 짐작해 적지 마라 (v5.5)」 — 실측 `20:50` 대 `20:41:11`, 시간대 비교가 필요하면
  `date '+%Y-%m-%dT%H:%M:%S%z'` 원본, GNU date 링크
- §Diff-Scope 표준형 — `**(1) 상태 전제**` 정의 줄에 `Given: 이 스프린트의 커밋이 끝난 뒤` 를 첫 선택지로 더하고(평가 시점에
  다시 잴 수 있는 것), 예시를 같은 전제 · `<base>..$(sprint_head <slug>)` 로 바꾸고, 문단 「상태 전제는 평가 시점에 다시 잴 수
  있는 것으로 고른다 (v5.5)」 — `git diff HEAD` · `--cached` · `git status --porcelain` 은 커밋하고 나면 빈 출력이다
- §커밋 구간 상한 뒤에 `##### 여러 주체가 한 가지에 커밋할 때 — 서명 줄로 내 커밋을 가린다 (2026-09-24 추가)` — 실측은 「범위
  조건이 세 번 깨졌고 그중 두 번은 오케스트레이터가 감사 기록 커밋을 그 구간에 넣어서였다」(핸드오프 F1 · F3 절 — 첫 번은 자기
  개정 파일 경로가 열거에 없어서였다) · 선택지 A(누적 차이 · 한 주체 가지의 기본값 · 소리 나게 실패) · 선택지 B(끝 문단 서명 줄 ·
  `mine` · 반대 방향 확인 `unsigned_on` · 남는 사각은 `git commit -o` 커밋 규칙) · 상한은 `end_sha:` · `bash` 블록 하나(`mine` ·
  `unsigned_on`, 두 셸 확인)
- §미실측 오라클 봉인 금지 에 불릿 「면제는 기대값에만 걸린다 (v5.5)」 — 준비 단계 넷(경로 · `command -v` 출력과 종료 코드 · 도구를
  숨기는 전제 · 임시 사본), POSIX 링크, 실측 2026-09-22 (`jq` · `find`)
- §양성 대조 뒤에 `#### 알려진 답 대조 (Known-Answer · 0 이 아닌 기대값 · v5.5 추가)` — 무엇을 적나 · 언제 재나 · 판정 · 양성
  대조와의 차이 · 생성 측 짝, 실측 2026-09-22, `markdown` 예시 한 블록(10 mm 직선 두 줄 + 반지름 5 mm 반원 → 35.71)
- §조건 작성 preflight 표 뒤에 `##### 검사 스크립트 전체 통과를 조건으로 걸지 마라 — 이 스프린트 몫의 줄로 한정한다 (2026-09-24 추가)`
  — 새 태그 없이 `측정-환경-오염` 의 한 형태, 소유한 줄 이름 · 뺀 줄과 이유 · 서명 줄 `mine` 대조 · 전체 통과는 마지막 단계 계약 몫,
  실측 두 번
- §2. Anti-patterns 「최소 2개 선별」 뒤에 `AP-00: N/A (사유)` 예외
- §복잡도별 조건 수 가이드 — 기능 조건 정의(자동 포함 여섯 줄 · `## Anti-patterns` 절 · `N/A` 줄 제외), 표 `| 복잡도 | 기능 조건 수 |`
  1~3 · 4~8 · 9~20 (파일 영향 열은 뺀다 — Gotcha `:35` 「파일 수는 판정 근거가 아니다」와 어긋나서), 레포 내부 정책 · Gherkin 링크,
  계산식 `bash` 블록(`SKILL.md` 6.2 와 글자 그대로 같은 한 줄)
- 머리 「최근 갱신: 2026-09-24 (Phase 2 kaizen · v5.5)」, §스키마 버전 `현재: **v5.5** (2026-09-24)` 와 변경 이력 첫 항목

스킬 (`SKILL.md`):

- Gotchas 끝에 셋 덧붙임(기존 42 줄은 한 글자도 안 바꾼다) — 준비 단계 · 기능 조건과 `AP-00` · 여러 주체 커밋과 `verify_seal` ·
  `unsigned_on` (「세 번 깨졌고 그중 두 번이 남의 커밋 때문이었다」)
- Step 0 에 문단 「셸 실행 도구가 없는 세션이면 파일 쓰기 도구가 있어도 여기서 멈춘다 (2026-09-24 추가)」 — 확인 단계가 전부 명령
  출력이라 대체 경로가 없다. 파일 쓰기 도구만 없으면 멈추지 말고 셸로 파일을 쓴다. 멈출 때는 첫 줄에 없는 도구 이름,
  `skill-design-guide.md` §3.7 네 칸, 재검증 명령. 셸이 없으면 네 칸의 「막는 것」 칸에 실행한 명령 대신 이 세션에서 쓸 수
  있는 도구 목록을 적는다 (2 회차 검토 제안 — `mock.py` 에는 없고 BUILD 가 더한다)
- Step 2 조건 수 가이드를 기능 조건 1~3 · 4~8 · 9~20 으로, 조건 패턴 표 제목 `5 종` 과 `| **알려진 답 대조** |` 행
- Step 5 끝 문단 — `사용자가 할 일: 없음` 또는 `사용자가 할 일: <한 줄>`
- Step 6 필드 목록에 `` - `created` `` 불릿 (`date '+%Y-%m-%d %H:%M'`), Step 6.2 에 기능 조건 수 계산식(`$(0)` 꼴 — V9)
- Step 7 머리에 「모든 항목은 「문제가 있다」 가 true 다」 (실측은 잰 시각 `2026-09-24 21:49 기준` 을 붙인다) · 옛 문구 12 개를
  「빠졌는가 · 않았는가」 꼴로 · 표준형 5 요소 · 새 항목 `measure_premise_unrun` · `known_answer_missing`. 항목 이름은 그대로 둔다
  (피드백 키 호환) — 이름이 「덮었다」로 읽히는 `nfr_coverage` 문항 끝에만 「(이름과 달리 true = 빠졌다)」

가이드 (`contract-design-guide.md`, v5.1): 표준형 5 요소(표 5 행 · 상태 전제 선택지 · Good 예시 · `--cached` 규칙 정정) ·
`조건 패턴 5 종` · 새 절 `### 0 이 아닌 기대값 — 새 측정은 알려진 답으로 먼저 맞춘다 (2026-09-24 추가)` · 안티패턴 표 두 행 ·
체크리스트 true 뜻과 행 정정 · 새 두 행 · parity 표 `(9 개)` 와 15 · 16 행 · 버전 정보 세 행.

`red-flags.md`: `:7` 에 `AP-00` 예외, `:8` 을 기능 조건 기준으로.

## 범위 경계

- 이 Phase 시작 HEAD: `76cfb376e2293350e2583c50166286bd2ec95b82`. 범위 상한은 개정 파일 `.harness/sprint-amendments-kaizen-0924-p02-contract.md` 의 `end_sha:` 마지막 값이다. 여러 Phase 가 같은 가지 `kaizen/2026-09-24` 에 동시에 커밋하므로 `HEAD` 로 재지 않는다 (이 초안을 쓰는 동안에도 Phase 15 · 16 · 17 근거 커밋 둘이 들어왔다)
- 고치는 파일은 넷이다 — `harness/references/contract-schema.md` · `harness/skills/sprint-contract/SKILL.md` · `harness/docs/guides/contract-design-guide.md` · `harness/skills/sprint-contract/references/red-flags.md`. `.harness/` 쪽은 이 계약 · 개정 파일 · QA 피드백 · `.harness/.meta/kaizen-0924/phase2-notes.md` · `.harness/.meta/kaizen-0924/phase2-review.md` 를 쓴다 — 슬러그를 나열하지 않고 AR-06 ③ `verify_seal` 로 잰다
- **이 Phase 의 커밋 메시지에는 전부 `Co-Authored-By` 줄 바로 위에 서명 줄 `Kaizen-Phase: kaizen-0924-p02-contract` 한 줄을 넣는다** (봉인 커밋 포함 — 6.7 의 `-m` 뒤에 `-m` 을 하나 더 준다). AR-06 ① · ② 와 DG-06 이 이 줄로 이 Phase 커밋을 가린다. FIX 가 커밋을 더할 때도 넣는다
- 측정이 기대는 제목은 이름을 바꾸지 않는다: `#### 미실측 오라클 봉인 금지` · `## 필수 섹션` · `## 복잡도별 조건 수 가이드` · `### 2. Anti-patterns` · `## 메타데이터` · `#### Diff-Scope Oracle 표준형` · `#### 조건 작성 preflight` · `### 셸 이식성 규약` (스키마), `## Gotchas` · `### 0. CONTRACT_ROOT` · `### 2. 완료 조건 생성` · `### 5. 사용자 승인` · `### 6. 계약 저장` · `### 6.2. 조건 수 계산` · `### 7. 자기진단` (스킬), `##### Diff-Scope Oracle 표준형` · `### 구조화 진단 체크리스트` · `### 계약 설계에 전수된 parity items` · `### 버전 정보` (가이드)
- 공유 파일(`marketplace.json` · `plugin.json` 버전 · 루트 README · 루트 CLAUDE.md · `docs/` HTML · 처리 배정표 · 감사 로그)은 건드리지 않는다. harness README 의 AUTO 구간은 SKILL.md frontmatter 만 읽는데 frontmatter 를 바꾸지 않는다. 문서 사이트 재생성은 Final F2 몫이라 DG-06 에서 `docs-site-regen` 을 뺀다
- 넘기는 것 (notes 에 적는다): 위 Counterpart 표의 Phase 3 · Phase 4 · Final 몫. Phase 4 로 넘기는 네 자리(`/sprint` 두 곳 · Step 9 문구 · `feedback-schema.yaml` · contract-kaizen Step 2)는 러닝북의 Phase 4 입력 목록에 phase2-notes 가 없으므로 notes 에 `## Phase 4 가 읽을 것` 소제목으로 모으고, 오케스트레이터가 Phase 4 를 부를 때 이 파일을 넘기게 적는다. contract-kaizen Gotcha 「`contract-schema.md` 를 바꾸면 PR 본문에 반드시 적는다」에 따라 notes 에 「`contract-schema.md` v5.4 → v5.5 — PR 본문에 적을 것」 한 줄을 남겨 Final 이 옮기게 한다. Phase 1 계약의 DG-02 보조 스크립트 결함(아래 `회귀 게이트` 절 — 열 번호를 줄 번호로 읽음. Phase 1 결과는 다시 재도 같다)은 Phase 3 확인 목록과 다음 사이클 메모로. 데이터 풀 §1 개선 제안 「개정 번호를 이어 붙이는 규칙」(2026-09-24)은 이번에 넣지 않는다 — 처리 배정표 밖이고 크기에 비해 조건이 늘어난다. 다음 사이클 메모로
- 새 셸 코드 블록은 셋이다 — 스키마의 서명 줄 블록 · 기능 조건 계산식, `SKILL.md` 6.2 의 같은 계산식. 셋 다 bash · zsh 로 돌린 값이 조건에 있다 (AR-02 (b) · SK-03 (d)). 그 밖에는 새 셸 블록을 넣지 않는다 — 조건으로 재지는 않는다(AP-03 은 언어 힌트만 잰다). 검토 반영 모의본 실측: 네 파일에 더한 줄 가운데 bash 펜스를 여는 줄 3 개 (`회귀 게이트` 절 `[bash-blocks]`)
- 사용자 승인(Step 5) 대체: 사용자가 「자동으로 끝까지 알아서 진행해 내 허락이 필요한건 코덱스로 리서치나 검토받고」라고 위임했다(세션 `de8c7935-a5b6-4df5-9106-fafa73c288a0` 기록 queued_command `2026-09-24T04:04:16.964Z`). Codex 사용량 한도가 소진돼(오류 원문 「You've hit your usage limit … try again at 11:05 PM」, 2026-09-24) 독립 Claude 검토자가 대신한다. 이어 사용자가 「코덱스 대신에 그냥 너가 알아서 진행하라고」라고 명시했다(같은 세션 기록 user `2026-09-24T11:54:58.940Z`). 검토 결과 파일: `.harness/.meta/kaizen-0924/phase2-review.md`. 검토 VERDICT: 1 회차 `CHANGES`(막는 이유 여섯) · 2 회차 `CHANGES`(막는 이유 하나 — ER-03 의 줄 번호 없는 가이드 경로 토큰이 다른 줄에 받쳐 늘 1 이상). 3 회차 검토는 없다. 2 회차 지적은 BUILD 가 봉인 전에 검토가 적은 문구 그대로 반영했다 — ER-03 경로 9 개 → 12 개(`qa-evaluation-guide.md` 를 `:12` · `:742` · `:746` · `:1915` 넷으로), 측정 20 값 → 23 값, 이 절의 커버리지 해소 줄과 `회귀 게이트` 표 `[ER-03]`, 봉인 전 실측(아래 `검토 반영 기록` 2 회차 줄). 조건 줄 수는 그대로다(28 · 기능 조건 19). 2 회차의 막지 않는 제안 둘: SK-06 문단에 「셸이 없으면 네 칸의 막는 것 칸에 실행한 명령 대신 이 세션에서 쓸 수 있는 도구 목록을 적는다」 한 마디를 구현에 더한다(SK-06 토큰 다섯의 값은 그대로 — 새 문장에 그 토큰이 없다). `harness/agents/qa-evaluator.md:590` 은 notes 의 한 줄에 표준형 4 요소 · 상태 전제 선택지 두 내용을 함께 적는다
- 오라클 해소: SK-01 · SK-02 · SK-03 (a)(b)(e) · SK-04 · SK-05 · SK-06 · SK-07 · AR-01 · AR-02 (a)(c) · AR-03 · AR-04 · AR-05 — 산출물이 계약 형식 문서의 문장 · 표 자체라 정해진 절 구간에 정해진 문구 · 행이 있는지가 곧 산출물 판정이다. 각 측정은 코드 펜스를 건너뛰는 `sect` 로 절을 잘라 재므로 파일 다른 곳의 같은 낱말로 통과하지 않고, 편집 전 파일에서 새 문구가 전부 0 · 옛 문구가 전부 1 이상인 것을 봉인 전에 확인했다. 모의본에서 핵심 문장 하나만 지운 사본 30 개에서도 해당 값이 0 으로 떨어지는 것을 돌려 확인했다 (`회귀 게이트` 절 문장 삭제 대조 표). 실행할 동작이 있는 두 곳(SK-03 (d) 계산식 · AR-02 (b) 서명 줄 스니펫)은 알려진 답으로 돌린다
- 오라클 해소: ER-03 — 넘김 기록(notes)의 경로 문자열이 곧 산출물이고, 편집 금지는 커밋 파일 목록(`my`)으로 잰다
- 오라클 해소: AP-01 — 더한 줄의 버전꼴 문자열을 세는 측정이고, 옮겨 적은 두 값이 원본과 같은지는 AR-05 (c) 가 `$END` 판 머리 설정을 직접 읽어 잰다. 양성 대조가 붙어 있다
- 오라클 해소: RE-01 — `N/A (사유)` 줄이다. 사유는 커밋 파일 목록 명령의 출력(0)으로 다시 잰다
- 오라클 해소: DG-05 · DG-06 — 판정은 검사 스크립트를 실제로 돌린 출력이다. 뒤따르는 대조는 그 출력의 파일 경로를 이 Phase 네 파일 · `my` 와 맞출 뿐이다
- 커버리지 해소: SK-01 · SK-02 · SK-03 · SK-05 · SK-06 · SK-07 · AR-01 · AR-02 · AR-04 · AR-05 — 산문의 파일 이름(`contract-schema.md` · `SKILL.md` · `skill-design-guide.md` 를 인용한 문구 · `red-flags.md`)은 측정의 `"$T/SC"` · `"$T/SK"` · `"$T/GD"` · `"$T/RF"` 다. 공통 정의가 네 파일의 `$END` 판을 그 이름으로 꺼낸다. 산문의 토큰(`PATH=/usr/bin:/bin` · `pubs.opengroup.org` · `date-invocation.html` · `zsh.sourceforge.io` · `gnu.org/software/bash` · `v5.0` · `v5.1` 등)은 측정의 `tok` · `grep -cF` 가 인자로 하나씩 센다 — 검출기는 공백 든 코드 조각 안의 인자를 읽지 못해 `UNCOVERED` 로 냈다 (2026-09-24 21:3x 실측: SK-01 · SK-02 · SK-03 · SK-05 · SK-06 · ER-03 · AR-04 · AR-05 여덟 건, 전부 이 두 이유. 검토 반영 뒤 22:0x 실측: AR-02 가 더해져 아홉 건 — (c) 가 산문에 `SKILL.md` 를 더해 경로형 토큰이 둘이 됐다. `SKILL.md` 는 측정의 `"$T/SK"`, `f3test.sh` 는 측정이 `bash f3test.sh "$T/f3.sh"` 로 돌리는 `회귀 게이트` 절 블록이다. 같은 두 이유)
- 커버리지 해소: ER-03 — 산문의 넘김 경로 12 개와 키 11 개는 측정의 `for t in …` 한 줄이 같은 23 문자열을 하나씩 notes 에서 `grep -cF` 한다. notes 경로 `.harness/.meta/kaizen-0924/phase2-notes.md` 는 `test -f` 와 루프가 읽는 파일이다. 편집 금지 여섯 파일은 `my | grep -cE …` 정규식이 덮는다 — 펼치면 `harness/agents/qa-evaluator.md` · `harness/docs/guides/qa-evaluation-guide.md` · `harness/skills/sprint/SKILL.md` · `harness/scripts/save-feedback.sh` · `harness/references/feedback-schema.yaml` · `harness/skills/contract-kaizen/SKILL.md`
- 커버리지 해소: AR-06 — 허용 네 파일은 ② 의 `grep -cxE` 정규식 하나가 덮는다 (펼친 이름은 위 둘째 줄)
- 편집 전부터 있던 markdownlint 경고(고친 보조 스크립트 기준 스키마 4 · 스킬 10 · 가이드 5 · red-flags 1 줄)는 범위 밖이다 — DG-02 는 더한 줄만 잰다
- 기능 조건 19 · 전체 조건 줄 28 (N/A 5 · 금지 패턴 2 · 자동 포함 중 N/A 아닌 2)

## 회귀 게이트 — 측정 공통 정의와 봉인 전 실측

모든 조건의 측정은 아래 블록을 먼저 실행한 **bash** 셸에서 돈다 — 블록과 측정을 한 `bash -c` 안에 넣거나 블록을 파일로 저장해
`. 파일` 뒤에 잇는다. `END_UNRESOLVED` 가 찍히면 셸이 종료 코드 2 로 끝난다. `fm_get` · `sha256_16` · `contract_digest` ·
`verify_seal` 은 `harness/references/contract-schema.md` §계약 봉인 정의 그대로 더한다.

```bash
# 측정 공통 정의 — bash 로 실행한다 (zsh 에서 source 하지 마라)
export LC_ALL=C.UTF-8   # 번역투 정규식이 글자 단위로 돌아야 한다 — C 로케일이면 덜 잡힌다 (실측 UTF-8 2 · C 1)
cd /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/kaizen-0924 || exit 2
B=76cfb376e2293350e2583c50166286bd2ec95b82                  # 이 Phase 시작 HEAD
SIG='Kaizen-Phase: kaizen-0924-p02-contract'
AM=.harness/sprint-amendments-kaizen-0924-p02-contract.md
END=$( [ -f "$AM" ] && sed -n 's/^end_sha:[[:space:]]*//p' "$AM" | tail -1 )
if [ -z "$END" ] || ! git rev-parse -q --verify "$END^{commit}" >/dev/null; then
  echo "END_UNRESOLVED — 측정을 멈추고 BUILD 에 묻는다. HEAD 로 바꿔 재지 않는다"; exit 2   # return 을 쓰면 source 한 쪽이 계속 돈다
fi
SC=harness/references/contract-schema.md; SK=harness/skills/sprint-contract/SKILL.md
GD=harness/docs/guides/contract-design-guide.md; RF=harness/skills/sprint-contract/references/red-flags.md
T=$(mktemp -d)
for k in SC SK GD RF; do p=${!k}; git show "$B:$p" > "$T/$k.0"; git show "$END:$p" > "$T/$k"; done
# sect <파일> <제목 앞부분> — 그 제목부터 같은 깊이 이하의 다음 제목 전까지. 코드 펜스 안의 `#` 줄은 제목으로 보지 않는다
sect() { awk -v h="$2" '
  /^[[:space:]]*(```|~~~)/ { fence = !fence }
  !f && !fence && index($0, h) == 1 { f = 1; lvl = match($0, /[^#]/) - 1; print; next }
  f && !fence && /^#+ / { l = match($0, /[^#]/) - 1; if (l <= lvl) exit }
  f' "$1"; }
tok()   { local s="$1"; shift; for t in "$@"; do printf '%s=%s ' "$t" "$(printf '%s\n' "$s" | grep -cF -- "$t")"; done; echo; }
url()   { grep -oE 'https?://[^ )>"`]+' | sed -E 's/[.,;:]+$//' | sort -u; }
added() { for k in SC SK GD RF; do git diff --no-index -U0 "$T/$k.0" "$T/$k"; done | grep '^+' | grep -v '^+++'; }
# 스키마에 넣을 서명 줄 스니펫과 같은 두 함수 (AR-02 가 스키마 쪽 사본을 따로 돌린다)
mine() { git log --format= --name-only "${1}..${2}" --grep="^${3}\$" | grep . | LC_ALL=C sort -u; }
unsigned_on() { _b=${1}; _u=${2}; _s=${3}; shift 3
  git log --format=%H "${_b}..${_u}" -- "$@" | while read -r _c; do git log -1 --format=%B "$_c" | grep -qxF "$_s" || echo "$_c"; done; }
my() { mine "$B" "$END" "$SIG"; }
K02='(을|를) ?(처리|관리)(합니다|한다)|에 대해서?|하도록 (합니다|한다)|에 의(해|하여)|되어 있(는 경우|을 때)|(표시|적용|호출|생성|반환)(됩니다|된다)'
```

AR-02 (b) 가 쓰는 알려진 답 시험 (`f3test.sh <스니펫 파일>` — 스크래치 저장소를 만들어 네 커밋을 쌓는다: 서명 · 남의 커밋(본문에
서명 글자를 인용만) · 서명 · 서명 빠짐):

```bash
# f3test.sh <snippet> — 알려진 답: mine 은 a.md · b.md 두 줄, unsigned_on 은 넷째 커밋 한 줄
set -u
R=$(mktemp -d); cd "$R" || exit 2
git init -q . && git config user.email t@t && git config user.name t
echo 0 > a.md && git add a.md && git commit -qm base; BASE=$(git rev-parse HEAD)
S='Kaizen-Phase: demo-slug'
echo 1 >> a.md && git add a.md && git commit -qm "c1" -m "$S"
echo x > other.md && git add other.md && git commit -qm "c2 남의 커밋" -m "본문에 Kaizen-Phase: demo-slug 를 인용만 한다"
echo 1 > b.md && git add b.md && git commit -qm "c3" -m "$S"
echo 2 >> a.md && git add a.md && git commit -qm "c4 서명 빠짐"; C4=$(git rev-parse HEAD)
UP=$(git rev-parse HEAD)
. "$1"
M=$(mine "$BASE" "$UP" "$S" | tr '\n' ' ')
U=$(unsigned_on "$BASE" "$UP" "$S" a.md b.md)
[ "$M" = "a.md b.md " ] && echo "mine OK [$M]" || echo "mine NG [$M]"
[ "$U" = "$C4" ] && echo "unsigned_on OK (c4)" || echo "unsigned_on NG [$U] want [$C4]"
```

AP-03 이 쓰는 펜스 검출기 (`python3 fence.py <파일>...` — Phase 1 계약과 같은 것):

```python
import re, sys
# 여는 펜스에 언어 힌트가 없으면 bare. 4-백틱 바깥 펜스 안의 ``` 는 내용으로 본다
tot_bare = tot_unclosed = 0
for path in sys.argv[1:]:
    open_len = 0; open_ch = ''; bare = []
    for n, line in enumerate(open(path, encoding='utf-8'), 1):
        m = re.match(r'^\s*(`{3,}|~{3,})(.*)$', line.rstrip('\n'))
        if not m:
            continue
        run, rest = m.group(1), m.group(2).strip()
        if open_len == 0:
            open_len, open_ch = len(run), run[0]
            if not rest:
                bare.append(n)
        elif run[0] == open_ch and len(run) >= open_len and not rest:
            open_len = 0
    tot_bare += len(bare); tot_unclosed += 1 if open_len else 0
    print(f"{path}: bare_open={len(bare)} {bare} unclosed={1 if open_len else 0}")
print(f"bare_open_total={tot_bare} unclosed_total={tot_unclosed}")
```

DG-07 이 쓰는 회귀 확인 계산기 (`python3 dg07.py <스킬 사본> <가이드 사본>` — 작업 폴더에서 돈다):

```python
import json, re, sys
# assertions.json 의 file 을 $END 판 사본으로 바꿔 패턴 개수를 센다
a = json.load(open('harness/evals/kaizen/contract-kaizen/assertions.json', encoding='utf-8'))
m = {'harness/skills/sprint-contract/SKILL.md': sys.argv[1], 'harness/docs/guides/contract-design-guide.md': sys.argv[2]}
print(' '.join(f"{k}:{len(re.findall(x['pattern'], open(m[x['file']], encoding='utf-8').read()))}" for k, v in a.items() for x in v))
```

DG-02 가 쓰는 새 경고 계산기. 스크래치 폴더에 `npm install --no-save markdownlint-cli2@0.23.2`, 같은 폴더에
`cfg.markdownlint-cli2.jsonc` = `{ "config": { "MD013": false } }` (편집기 확장이 MD013 을 끈 것과 같은 조건). 준비 단계 실측:
이미 설치된 자리 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p1build/node_modules`
를 계산기 옆 `node_modules` 로 이어 쓰면 된다 — 그 자리의 `.bin/markdownlint-cli2 --version` 첫 줄이
`markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)` (2026-09-24 21:4x 실측). 없으면 위 설치 명령부터 돌린다. **Phase 1 계약의
판에서 한 줄을 고쳤다** — 옛 판은 `sed -E 's#^[^ ]*:([0-9]+).*#\1#'` 가 탐욕 매치라 `경로:13:8` 에서 열 번호 `8` 을 줄 번호로
읽었다:

```bash
#!/usr/bin/env bash
# new-warnings.sh <옛 파일> <새 파일> — 새 파일에서 더한 줄에 걸린 경고만 센다. 줄이 밀리므로 전체 수 차이로 세지 않는다
# 줄 번호는 경로 뒤 첫 번째 숫자다. 탐욕 매치(^[^ ]*:)로 뽑으면 열 번호가 줄 번호로 둔갑한다 (실측 2026-09-24)
set -u
DIR=$(cd "$(dirname "$0")" && pwd)
ADDED=$(git diff --no-index -U0 -- "$1" "$2" | awk '/^@@/{split($3,a,","); s=substr(a[1],2)+0; n=(a[2]==""?1:a[2]+0); for(i=0;i<n;i++) print s+i}' | sort -u)
OUT=$("$DIR/node_modules/.bin/markdownlint-cli2" --config "$DIR/cfg.markdownlint-cli2.jsonc" "$2" 2>&1)
LINES=$(printf '%s\n' "$OUT" | grep -E ':[0-9]+(:[0-9]+)? (error|warning) ' | sed -E 's#^([^:]*):([0-9]+).*#\2#' | sort -u)
NEWW=$(comm -12 <(printf '%s\n' "$ADDED" | grep . | sort) <(printf '%s\n' "$LINES" | grep . | sort) | wc -l | tr -d ' ')
echo "total_warning_lines=$(printf '%s\n' "$LINES" | grep -c .) added_lines=$(printf '%s\n' "$ADDED" | grep -c .) new_warnings=$NEWW"
```

봉인 전 실측 (초안 2026-09-24 21:0x ~ 21:2x, 검토 반영 21:4x ~ 22:0x). 편집 전 값은 공통 정의에서 `END` 자리에 `$B` 를 넣어
돌렸다. 「모의본」 값은 스크래치
`/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p2draft2/mock.py`
(검토 반영판 — 초안판 `p2draft/mock.py` 에 치환 하나 `SC-f2-def` 를 더하고 문구 다섯 곳을 고쳤다)가 시작 커밋 판 네 파일에
개선안을 적용한 사본에서 같은 측정을 돌린 값이다 (측정 묶음 `m3.sh`, 결과 `pre-values.txt` · `mock-values.txt` 같은 폴더):

```text
            편집 전                                   모의본
[SK-01]     5 토큰 0 · gotcha 0 · s7 0 · g7 0          1 · 2 · 3 · 1 · 1 · gotcha 1 · s7 1 · g7 1
[SK-02]     제목 0 · 구간 안 0 · 8 토큰 0               제목 1 · 구간 안 1 · 8 토큰 전부 1 이상 (다르면 봉인하지 않는다 1)
            5 종 0 · 4 종 1 · 행 0 · s7 0 · g7 0        5 종 1 · 4 종 0 · 행 1 · s7 1 · g7 1
            가이드 4 종 1 · 5 종 0 · 제목 0             가이드 4 종 0 · 5 종 1 · 제목 1
            (9 개) 0 · 15 행 0 · 16 행 0 · 번호 [1 2 3 11 12 13 14]    (9 개) 1 · 1 · 1 · [1 2 3 11 12 13 14 15 16]
[SK-03]     기능 조건 0 · 새 행 셋 0 · 옛 행 1 · 정책 0 · 링크 0 · 정의 0    2 · 1 · 1 · 1 · 옛 행 0 · 1 · 1 · 정의 1
            총 4-6개 1 · 기능 조건 세 줄 0 · 정의 0     0 · 1 · 1 · 1 · 정의 1
            계산식 줄 0,0 (같음 0)                      1,1 (같음 1) · 알려진 답 bash 16 · zsh 16
            AP-00 스키마 0 · RF 0 · RF 기능 조건 0 · 가이드 0 · Gotcha 0    전부 1
[SK-04]     0 · 0                                      1 · 1
[SK-05]     0 · 0 · 20:41:11 0 · date-invocation 0 · 짐작 0     1 · 1 · 1 · 1 · 1
[SK-06]     0 · 0 · 0 · 0 · 0                          1 · 1 · 1 · 1 · 1
[SK-07]     true 문장 0 · 옛 12 문구 합 12 · 이름 23 · 잃은 이름 0      1 · 0 · 25 · 0
            가이드 true 문장 0 · 옛 9 문구 합 9 · 행 19                  1 · 0 · 21
[ER-01]     0                                          0 · 양성 대조(example.invalid + 근거 안 URL 더한 사본) 1
[ER-02]     0                                          0 · 양성 대조(「훅에 의해 적용된다」 · 「그것에 대해 말한다」) UTF-8 2 · C 1
[ER-03]     notes 없음 (면제)                          가짜 notes 23 값 전부 1 · :746 · :742-743 · :12 · :1915 줄을 하나씩 지우면 그 값 0
[AR-01]     스키마 빈 출력 0 · porcelain 0 · 옛 예시 1 · 정의 줄 0       1 · 2 · 0 · 1 (초안판 모의본은 정의 줄 0)
            가이드 4 요소 1 · 5 요소 0 · 옛 규칙 1 · 빈 출력 0 · 옛 예시 1 · 5 행 0     0 · 1 · 0 · 1 · 0 · 1
            SKILL 4 요소 1 · 가이드 표준형 4 요소 2                      0 · 0
[AR-02]     제목 0 · 7 토큰 0 · 스니펫 0 줄 · Gotcha 0                   1 · 전부 1 이상 · 10 줄 · bash/zsh 둘 다 mine OK · unsigned_on OK · Gotcha 1
[AR-03]     제목 0 · 4 토큰 0 · 태그 행 10                               1 · 1 · 1 · 1 · 1 · 10
[AR-04]     5 토큰 0                                                     전부 1
[AR-05]     v5.5 0 · v5.4 1 · 이력 0 · 머리 0 · 가이드 머리 0 · 스키마 행 0 · v5.0 남음 1 · Parity 0     1 · 0 · 1 · 1 · 2 · 1 · 0 · 1
[AP-01]     0                                          0 · 양성 대조(9.9.9 · 1.6.0 더한 사본) 1
[AP-03]     bare 0 · unclosed 0                        0 · 0 · 양성 대조(언어 힌트 없는 펜스) 1
[RE-02]     표 구분줄 SC 15 · SK 6 · GD 18 · RF 1      15 · 6 · 18 · 1
[DG-02]     더한 줄 0                                  new_warnings SC 0 · SK 0 · GD 0 · RF 0
            양성 대조: 표 구분줄을 |--------|--------| 로 둔 모의본 SC 1 (1228 행 MD060), 빈 줄 없이 목록을 붙인 모의본 SK 1 (460 행 MD032)
[DG-05]     validate-plugin harness 10 검사 OK · FAIL 0 · check-stale-values 「되살아난 옛 값 없음」 exit 0
            검토 반영 모의본을 스크래치 사본(harness/ · scripts/validate-plugin.py · plugin_utils.py · marketplace.json)에 얹어 돌림: V1~V10 OK
            양성 대조: 같은 사본 SKILL.md 끝에 `awk x $1` 줄 → V9 1 hazard (FAIL harness/skills/sprint-contract/SKILL.md:856)
[DG-06]     15 checks — 12 PASS / 0 FAIL / 0 ERROR / 3 SKIP (scope-isolation PASS · doc-contracts PASS · docs-site-regen SKIP) · 위반 목록 읽은 수 0
            예외 분기 양성 대조(가짜 출력 51a22b4 · 43fc9ee): Phase 1 서명 줄 → 읽은 수 2 · 서명 1, 이 Phase 서명 줄 → 2 · 0 (C.UTF-8 · C 같음)
[DG-07]     assertions 6 패턴 3 · 19 · 2 · 2 · 1 · 2   3 · 19 · 2 · 2 · 2 · 2
[AR-06]     ① 0 줄 ② my 빈 목록 0 · 0 ③ SEAL_OK 51 · SEAL_ABSENT 11 (이 계약 선점 빈 파일 포함) · SEAL_BROKEN 0 ④ Gotcha 42 줄 → 45 줄 · 잃은 줄 0
[bash-blocks] 더한 줄 가운데 bash 펜스를 여는 줄 0                     3
```

문장 삭제 대조 (러닝북 계약 규칙 — 특정 문장이 있어야 한다는 조건은 그 문장만 지운 사본에서 FAIL 이 나야 한다). 검토 반영
모의본에서 아래 문자열 하나만 지운 사본 30 개(`p2draft2/del.py` · `del/<태그>/`)에 같은 측정을 돌렸다. 모의본 값은 전부 1 이상이다:

```text
태그       지운 곳 (SC = contract-schema.md · SK = SKILL.md · GD = 가이드)            떨어진 값
SK-01a     SC 「그 값을 재는 명령의 준비 단계는 면제가 아니다」                        준비 단계 0
SK-01b     SK Gotcha 「값이 면제여도 재는 명령의 준비 단계는 봉인 전에 돌려라」        gotcha 0
SK-01c     SK Step 7 `measure_premise_unrun` 항목                                      s7 0
SK-02a     SC 「판정」 불릿 (기대값과 실제값이 다르면 봉인하지 않는다)                 다르면 봉인하지 않는다 0
SK-02b     SK 조건 패턴 표 `| **알려진 답 대조** |` 행                                 행 0
SK-03a     SC 기능 조건 정의 문장                                                      `N/A (사유)` 줄을 뺀 0
SK-03b     SK 기능 조건 정의 문장                                                      `N/A (사유)` 줄을 뺀 0
SK-03e     SC 「하나도 없으면 `AP-00: N/A (사유)` 한 줄로 쓴다」                       AP-00 스키마 0
SK-04      SK 「DRAFT 끝은 `사용자가 할 일: 없음` 또는 … 로 맺는다」                   0 · 0
SK-05a     SK `created` 불릿 첫 줄                                                     a 0
SK-05c     SC 「시각 필드는 `date` 출력을 옮긴다 — 짐작해 적지 마라」                  짐작해 적지 마라 0
SK-06-1    SK 「셸 실행 도구가 없는 세션이면 파일 쓰기 도구가 있어도 여기서 멈춘다」   셸 실행 도구가 없는 세션 0
SK-06-2    SK 「파일 쓰기 도구만 없으면 멈추지 말고 셸로 파일을 쓴다」                 파일 쓰기 도구만 없으면 0
SK-06-3    SK 「멈출 때는 … 네 칸(…)을 채운 뒤 멈춘다」                                네 칸 0
SK-07a     SK 「모든 항목은 「문제가 있다」 가 true 다」                               true 문장 0
SK-07b     GD 같은 문장                                                                true 문장 0
AR-01a-1   SC 「… `--cached` 는 커밋하고 나면 빈 출력이다」                            커밋하고 나면 빈 출력 0
AR-01a-2   SC `(1) 상태 전제` 정의 줄의 새 선택지                                      정의 줄 0
AR-01b     GD 「`--cached` 와 `git diff HEAD` 는 커밋하고 나면 빈 출력이다」           커밋하고 나면 빈 출력 0
AR-02a-1   SC 「서명 줄을 빠뜨린 커밋은 조용히 빠진다」                                조용히 빠진다 0
AR-02a-2   SC 「그래서 반대 방향 확인을 함께 건다」                                    반대 방향 0
AR-02a-3   SC 「이것은 커밋 규칙으로 막는다 — … git commit -o …」                      git commit -o 0
AR-02a-4   SC 「상한은 … end_sha: 줄 마지막 값으로 읽는다 …」                          end_sha: 0
AR-02c     SK Gotcha 「`verify_seal` 로, 구현 경로는 … `unsigned_on` 으로 잰다」       Gotcha 0
AR-03-1    SC 불릿 「이 스프린트가 소유한 줄의 이름을 적고 …」                         소유한 줄의 이름 0 (초안 토큰 `소유한 줄` 은 1 — 가르지 못했다)
AR-03-2    SC 불릿 「검사 전체 통과는 사이클 마지막 단계(카이젠이면 Final) …」         마지막 단계(카이젠이면 Final) 0 (초안 토큰 `마지막 단계` 는 1)
AR-03-3    SC 불릿 「… `mine` … 과 대조해 겹치는 것만 …」                              `mine` 0
AR-04-1    SC 「zsh 배열은 기본 옵션에서 1 부터 센다」                                 1 부터 0
AR-04-2    SC 「`KSH_ARRAYS` 옵션을 켜면 0 부터 세고 …」                               KSH_ARRAYS 0
AR-04-3    SC 「… `for x in "${arr[@]}"` 로 원소를 돈다」                              for x in 0
```

준비 단계 실측 (SK-01 이 적게 하는 것을 이 계약에 먼저 적용):

```text
bash -c 'PATH=/usr/bin:/bin command -v jq; echo "exit=$?"'      → /usr/bin/jq  exit=0   (2026-09-22 계약의 「jq 숨김」 전제가 이 기계에서 성립하지 않는다)
zsh  -c 'PATH=/usr/bin:/bin command -v jq; echo "exit=$?"'      → /usr/bin/jq  exit=0
bash -c 'PATH=/nonexistent command -v jq; echo "exit=$?"'       → (출력 없음)  exit=1
bash -c 'command -v cd; echo "exit=$?"'                          → cd  exit=0   (셸 내장도 보고한다 — 경로인지까지 봐야 하는 이유)
```

AR-01 이 고치는 주장 (커밋하고 나면 빈 출력) — 스크래치 저장소에서 기준 커밋 뒤 두 파일을 스테이징 · 커밋:

```text
커밋 전:  git diff --name-only HEAD 2 · git diff --cached --name-only 2 · git status --porcelain 2
커밋 뒤:  git diff --name-only HEAD 0 · git diff --cached --name-only 0 · git status --porcelain 0 · git diff --name-only <base>..HEAD 2
```

알려진 답과 음성 대조 (조건이 가리키는 실행 두 곳):

```text
SK-03 (d) 계산식 × Phase 1 봉인 계약(51a22b4 판, 조건 25 줄) — 손으로 센 값 16 (SK 4 · ER 5 · AR 4 · DG-05~07 3) · bash 16 · zsh 16
AR-02 (b) 스니펫 — bash · zsh 둘 다 mine OK [a.md b.md ] · unsigned_on OK (c4)
  음성 대조 1: --grep 에서 ^ $ 를 뺀 변이 → mine NG [a.md b.md other.md ] (본문 인용 커밋이 섞인다)
  음성 대조 2: grep -qxF "$_s" || echo 를 true 로 바꾼 변이 → unsigned_on NG [] (서명 빠진 커밋을 못 찾는다)
DG-02 계산기 — 고친 판과 옛 판을 같은 모의본에 돌림: red-flags 옛 판 1 (줄 13 의 열 번호 8 이 더한 줄 8 과 우연히 겹침) · 고친 판 0
  (13 행은 더한 줄이 아니다 — 맞는 값). 스키마 표 구분줄 경고는 고친 판이 1228 행으로 읽고, 옛 판은 열 번호 1 · 10 · 19 로 읽는다
  Phase 1 두 가이드(7689fde → 18b8ff0)를 고친 판으로 다시 재도 new_warnings 0 · 0 — Phase 1 판정은 바뀌지 않는다
```

전체 예행 (계약 본문 그대로, 검토 반영판으로 다시 돌림): 작업 폴더를 스크래치에 복제(`…/scratchpad/p2draft2/rh2`)해 BUILD 를
흉내 냈다 — 이 계약 커밋 · 모의본 네 파일 커밋 · 서명 없는 다른 Phase 커밋(`.harness/` 한 파일, 본문에 서명 글자 인용) ·
notes 커밋(20 문자열 · `## Phase 4 가 읽을 것`) · 그 sha 를 적은 `end_sha` 커밋. 서명 줄 커밋에는 `Co-Authored-By` 줄 바로 위에
서명 줄을 넣었다. 위 코드 블록 다섯 개를 이 계약에서 기계로 떼어 내고(`cd` 줄만 복제본으로 바꿈, 측정 묶음 `p2draft2/r2.sh`)
28 조건의 측정을 조건 문구 그대로 돌렸다 — 28 조건 전부 요구값 (`r2-values.txt`). `my` 는 네 파일 · 계약 · notes 여섯 줄,
AR-06 ② 0 · 4, ③ `SEAL_OK 51 · SEAL_ABSENT 11` · 이 Phase 몫 0, ER-03 20 값 전부 1 이상 · 금지 여섯 파일 0. DG-06 은
`scope-isolation` PASS (7 commits) · `doc-contracts` PASS · `docs-site-regen` FAIL(Final 몫 — 판정에서 뺀 줄), 위반 목록 읽은 수 0.
AR-06 ① 음성 대조: 서명 없는 커밋이 `red-flags.md` 를 건드리게 하고 `end_sha` 를 그 커밋으로 옮기면 1.

자기진단 true 뜻 측정 (배경 7 번, 2026-09-24 21:59 다시 잼 — 초안 때보다 피드백이 늘어 몇 값이 1 씩 올랐다):

```text
~/.harness/feedback/contract/ 최근 40 건(수정 시각 순)의 diagnosis.checklist 에서 true 인 건수 / 그 항목이 있는 건수:
nfr_coverage 20/31 · ambiguous_conditions 12/39 · untestable_conditions 11/39 · implementation_leakage 7/34 ·
conditions_count_typed 6/25 · preamble_condition_conflict 4/23 · diff_oracle_nonstandard 4/24 · negative_control_missing 3/22 ·
evidence_artifact_missing 3/20 · 나머지 0~1
(초안 21:0x: nfr_coverage 19/31 · conditions_count_typed 6/24 · preamble_condition_conflict 4/22 · diff_oracle_nonstandard 4/23 ·
evidence_artifact_missing 3/19 · negative_control_missing 3/21)
```

검토 반영 기록 (2026-09-24 21:4x ~ 22:0x, 검토 결과 `.harness/.meta/kaizen-0924/phase2-review.md` 의 `CHANGES` 여섯 건):
1 문장 삭제 대조 — SK-02 · SK-03 · SK-05 에 토큰을 더하고 AR-03 토큰 둘을 바꿨다(검토가 짚은 `소유한 줄` 에 더해 `마지막 단계` 도
같은 결함이라 이 초안이 찾아 고쳤다). 위 표 30 건. 2 AR-01 (a) 에 정의 줄 값 · `mock.py` 치환 `SC-f2-def`. 3 AR-02 (c) · 「세 번
깨졌다」 문구 정정. 4 SK-06 토큰과 문단 · 배경 표 `F21` 행. 5 ER-03 경로 9 개 · 20 값 · Counterpart 표 세 행. 6 DG-06 예외 분기 명령.
막지 않는 제안 여섯 가운데 넷(범위 경계 셸 블록 문구 · 피드백 수 잰 시각 · `nfr_coverage` 문항 끝 · DG-02 설치 자리와 판)은 반영,
둘(PR 본문 한 줄 · Phase 4 소제목)은 notes 에 적을 일이라 `범위 경계` 넘김 줄에 BUILD 할 일로 적었다.
검토 밖에서 이 초안이 고친 것: 옛 Gotcha 줄 수 44 → 42 (1.4 표 · 개선안 · AR-06 ④ — 줄 범위를 센 값이었다).
2 회차 검토 반영 (BUILD, 2026-09-24 22:1x, 봉인 전): ER-03 의 가이드 경로 토큰 하나를 `경로:줄` 넷으로 바꾸고 20 값 → 23 값.
스크래치 `p2build/er03.sh` 로 가짜 notes 에 돌려 23 값 전부 1, 네 줄을 하나씩 지운 사본에서 각각 0, 몰아 쓴 꼴에서 가이드 토큰
여섯 전부 0 을 확인했다. 위 `전체 예행` 의 「ER-03 20 값」 · 「notes 커밋(20 문자열 …)」 은 2 회차 반영 전 판의 값이다.

## Skill

- [ ] SK-01: 값이 면제여도 재는 명령의 준비 단계는 봉인 전에 돌린다는 규칙이 세 자리에 들어간다 (harness:P03 · F12) — (a) `contract-schema.md` §미실측 오라클 봉인 금지 구간에 5 토큰 `준비 단계` · `command -v` · `종료 코드` · `PATH=/usr/bin:/bin` · `pubs.opengroup.org` 가 각각 1 건 이상 (b) `SKILL.md` Gotchas 구간에 `준비 단계` 와 `command -v` 를 함께 담은 줄이 1 개 이상 (c) `SKILL.md` Step 7 에 `` `measure_premise_unrun`: `` 줄이 1 개, 가이드 §구조화 진단 체크리스트 에 `| measure_premise_unrun |` 행이 1 개 [exact, enumerated]
      (측정: `tok "$(sect "$T/SC" '#### 미실측 오라클 봉인 금지')" '준비 단계' 'command -v' '종료 코드' 'PATH=/usr/bin:/bin' 'pubs.opengroup.org'` 5 값 전부 1 이상 ·
       `sect "$T/SK" '## Gotchas' | grep -F '준비 단계' | grep -cF 'command -v'` 1 이상 ·
       ``sect "$T/SK" '### 7. 자기진단' | grep -cF '`measure_premise_unrun`:'`` 1 · `sect "$T/GD" '### 구조화 진단 체크리스트' | grep -cF '| measure_premise_unrun |'` 1.
       봉인 전 실측: 편집 전 전부 0 · 모의본 1 · 2 · 3 · 1 · 1 · 1 · 1 · 1)
- [ ] SK-02: 알려진 답 대조가 계약 측 조건 패턴으로 들어가고 설계 가이드 parity 표에 짝이 생긴다 (harness:P05 · F17 · Cross-Surface Parity) — (a) `contract-schema.md` 에 `#### 알려진 답 대조` 로 시작하는 제목이 정확히 1 개이고 `## 필수 섹션` 구간 안에 있으며, 그 소절에 8 토큰 `알려진 답:` · `기대값` · `실제값` · `종료 코드` · `skill-design-guide.md` · `0 이 아닌` · `미실측 오라클 봉인 금지` · `다르면 봉인하지 않는다` 가 각각 1 건 이상 (b) `SKILL.md` Step 2 구간에 `조건 패턴 5 종` 1 · `조건 패턴 4 종` 0 · `| **알려진 답 대조** |` 행 1, Step 7 에 `` `known_answer_missing`: `` 줄 1, 가이드 체크리스트에 `| known_answer_missing |` 행 1 (c) 가이드 전체에 `조건 패턴 4 종` 0 · `조건 패턴 5 종` 1 이상 · `### 0 이 아닌 기대값` 으로 시작하는 제목 1 (d) 가이드 §계약 설계에 전수된 parity items 제목 줄에 `(9 개)`, 표 행 번호가 정확히 `1 2 3 11 12 13 14 15 16`, 15 행에 `Zero-Result Positive Control`, 16 행에 `알려진 답 대조` [exact, enumerated]
      (측정: (a) `grep -cE '^#### 알려진 답 대조' "$T/SC"` 1 · `sect "$T/SC" '## 필수 섹션' | grep -cE '^#### 알려진 답 대조'` 1 · `tok "$(sect "$T/SC" '#### 알려진 답 대조')" '알려진 답:' '기대값' '실제값' '종료 코드' 'skill-design-guide.md' '0 이 아닌' '미실측 오라클 봉인 금지' '다르면 봉인하지 않는다'` 8 값 전부 1 이상
       (b) `tok "$(sect "$T/SK" '### 2. 완료 조건 생성')" '조건 패턴 5 종' '조건 패턴 4 종' '| **알려진 답 대조** |'` 1 · 0 · 1 · ``sect "$T/SK" '### 7. 자기진단' | grep -cF '`known_answer_missing`:'`` 1 · `sect "$T/GD" '### 구조화 진단 체크리스트' | grep -cF '| known_answer_missing |'` 1
       (c) `grep -cF '조건 패턴 4 종' "$T/GD"` 0 · `grep -cF '조건 패턴 5 종' "$T/GD"` 1 이상 · `grep -cE '^### 0 이 아닌 기대값' "$T/GD"` 1
       (d) `P2=$(sect "$T/GD" '### 계약 설계에 전수된 parity items')` 뒤 `printf '%s\n' "$P2" | head -1 | grep -cF '(9 개)'` 1 · `printf '%s\n' "$P2" | grep -oE '^\| [0-9]+ \|' | tr -dc '0-9\n' | tr '\n' ' '` 이 `1 2 3 11 12 13 14 15 16 ` · `printf '%s\n' "$P2" | grep -E '^\| 15 \|' | grep -cF 'Zero-Result Positive Control'` 1 · 같은 꼴로 16 행 `알려진 답 대조` 1.
       봉인 전 실측: 편집 전 (a) 0 · 0 · 전부 0 (b) 0 · 1 · 0 · 0 · 0 (c) 1 · 0 · 0 (d) 0 · `1 2 3 11 12 13 14 ` · 0 · 0 — 모의본은 전부 요구값. 문장 삭제 대조: 모의본에서 「판정」 불릿만 지운 사본은 (a) `다르면 봉인하지 않는다` 0, `| **알려진 답 대조** |` 행만 지운 사본은 (b) 그 값 0)
- [ ] SK-03: 조건 수 가이드가 기능 조건만 세고 두 문서의 수와 계산식이 같으며, 금지 패턴 「최소 2개」 규칙에 `AP-00` 예외가 붙는다 (harness:P06 · F11 · F27 크기 검사) — (a) 스키마 §복잡도별 조건 수 가이드 구간에 `기능 조건` 1 이상 · 행 `| 단순 | 1~3 |` · `| 중간 | 4~8 |` · `| 복잡 | 9~20 |` 각 1 · 옛 행 `| 단순 | 1-3 | 4-6 |` 0 · `레포 내부 정책` 1 이상 · `gherkin-best-practices` 1 이상 · 기능 조건 정의 문장의 `` `N/A (사유)` 줄을 뺀 `` 1 이상 (b) `SKILL.md` Step 2 구간에 `총 4-6개` 0 · `기능 조건 1~3` · `기능 조건 4~8` · `기능 조건 9~20` 각 1 · 같은 정의 문장의 `` `N/A (사유)` 줄을 뺀 `` 1 (c) 스키마 §복잡도 구간과 `SKILL.md` §6.2 구간에서 `"## Anti-patterns") next` 를 담은 줄이 각각 정확히 1 줄이고 두 줄이 글자 그대로 같다 (d) 알려진 답: 그 줄을 파일로 떼어 `CF` 에 Phase 1 봉인 계약(`51a22b4` 판)을 주고 돌리면 bash · zsh 둘 다 `16` (e) `AP-00` 예외 — 스키마 §2. Anti-patterns 구간에 `AP-00: N/A` 1 이상, `red-flags.md` 에 `AP-00` 1 이상 · `기능 조건` 1 이상, 가이드 `| 과소 안티패턴 |` 행에 `AP-00` 1, `SKILL.md` Gotchas 에 `기능 조건만 센다` 와 `AP-00` 을 함께 담은 줄 1 이상 [exact, enumerated]
      (측정: (a) ``tok "$(sect "$T/SC" '## 복잡도별 조건 수 가이드')" '기능 조건' '| 단순 | 1~3 |' '| 중간 | 4~8 |' '| 복잡 | 9~20 |' '| 단순 | 1-3 | 4-6 |' '레포 내부 정책' 'gherkin-best-practices' '`N/A (사유)` 줄을 뺀'`` 8 값이 순서대로 1 이상 · 1 · 1 · 1 · 0 · 1 이상 · 1 이상 · 1 이상
       (b) ``tok "$(sect "$T/SK" '### 2. 완료 조건 생성')" '총 4-6개' '기능 조건 1~3' '기능 조건 4~8' '기능 조건 9~20' '`N/A (사유)` 줄을 뺀'`` 0 · 1 · 1 · 1 · 1
       (c) `A1=$(sect "$T/SC" '## 복잡도별 조건 수 가이드' | grep -F '"## Anti-patterns") next')` · `A2=$(sect "$T/SK" '### 6.2. 조건 수 계산' | grep -F '"## Anti-patterns") next')` 가 각각 1 줄이고 `[ -n "$A1" ] && [ "$A1" = "$A2" ]` 참
       (d) `printf '%s\n' "$A2" > "$T/fc.sh"; git show 51a22b4:.harness/sprint-contract-kaizen-0924-p01-guides.md > "$T/p1.md"` 뒤 `CF="$T/p1.md" bash "$T/fc.sh"` 과 `CF="$T/p1.md" zsh "$T/fc.sh"` 가 둘 다 `16` — 손으로 센 값: SK 4 · ER 5 · AR 4 · DG-05~07 3. SC-00 · RE-01 · DG-01 · DG-03 · DG-04 는 N/A 줄, RE-02 · DG-02 는 자동 포함, AP-01 · AP-03 은 금지 패턴 절이라 뺀다
       (e) `sect "$T/SC" '### 2. Anti-patterns' | grep -cF 'AP-00: N/A'` · `grep -cF 'AP-00' "$T/RF"` · `grep -cF '기능 조건' "$T/RF"` 각 1 이상 · `grep -F '| 과소 안티패턴 |' "$T/GD" | grep -cF 'AP-00'` 1 · `sect "$T/SK" '## Gotchas' | grep -F '기능 조건만 센다' | grep -cF 'AP-00'` 1 이상.
       봉인 전 실측: 편집 전 (a) 0 · 0 · 0 · 0 · 1 · 0 · 0 · 0 (b) 1 · 0 · 0 · 0 · 0 (c) 0 줄 · 0 줄 (d) 계산식 없음 (e) 전부 0. 모의본 (a) 2 · 1 · 1 · 1 · 0 · 1 · 1 · 1 (b) 0 · 1 · 1 · 1 · 1 (c) 1 줄 · 1 줄 · 같음 (d) bash 16 · zsh 16 (e) 전부 1.
       문장 삭제 대조: 스키마의 기능 조건 정의 문장만 지운 사본 (a) 끝 값 0, `SKILL.md` 정의 문장만 지운 사본 (b) 끝 값 0, 스키마 `AP-00: N/A (사유)` 절만 지운 사본 (e) 첫 값 0. `자동 포함 여섯 줄` 은 스키마의 다른 문장(옛 표가 11 줄이던 이유)에도 있어 정의 문장을 가르지 못하므로 쓰지 않는다)
- [ ] SK-04: DRAFT 끝을 사용자가 할 일 한 줄로 맺게 한다 (harness:P06) — `SKILL.md` Step 5 구간에 `사용자가 할 일: 없음` 과 `사용자가 할 일: <한 줄>` 이 각각 1 건 이상 [exact, enumerated]
      (측정: `tok "$(sect "$T/SK" '### 5. 사용자 승인')" '사용자가 할 일: 없음' '사용자가 할 일: <한 줄>'` 두 값 1 이상. 봉인 전 실측: 편집 전 0 · 0, 모의본 1 · 1)
- [ ] SK-05: 시각 필드를 `date` 출력으로 채우게 한다 (harness:P08 · F13) — (a) `SKILL.md` Step 6 구간에서 ``- `created` `` 로 시작하는 줄 가운데 `date '+%Y-%m-%d %H:%M'` 를 담은 줄이 1 개 (b) 스키마 §메타데이터 구간의 yaml `created:` 줄이 같은 명령을 담는다 (1 줄) (c) 스키마 §메타데이터 머리(첫 `###` 전)에 실측 시각 `20:41:11` · `date-invocation.html` · 규칙 문장의 `짐작해 적지 마라` 가 각각 1 건 이상 [exact, enumerated]
      (측정: (a) ``sect "$T/SK" '### 6. 계약 저장' | grep -E '^- `created`' | grep -cF "date '+%Y-%m-%d %H:%M'"`` 1 (b) `sect "$T/SC" '## 메타데이터' | grep -E '^created:' | grep -cF "date '+%Y-%m-%d %H:%M'"` 1 (c) `tok "$(sect "$T/SC" '## 메타데이터' | awk 'NR>1 && /^### /{exit} 1')" '20:41:11' 'date-invocation.html' '짐작해 적지 마라'` 세 값 1 이상.
       봉인 전 실측: 편집 전 0 · 0 · 0 · 0 · 0, 모의본 1 · 1 · 1 · 1 · 1. 문장 삭제 대조: 스키마 규칙 문장 「시각 필드는 `date` 출력을 옮긴다 — 짐작해 적지 마라」만 지운 사본 (c) 셋째 값 0, `SKILL.md` `created` 불릿 첫 줄만 지운 사본 (a) 0. `20:41:11` 은 git 이 찍은 값이다 — `git log -1 --format=%ci fc29b58` 이 `2026-09-24 20:41:11 +0900`, 그 커밋의 개정 파일 머리 `created: "2026-09-24 20:50"`)
- [ ] SK-06: 대체 경로가 없는 도구(셸)가 없는 세션에서만 0 단계에서 멈추고, 대체 경로가 있는 도구(파일 쓰기)만 없으면 멈추지 않는 규칙이 들어간다 (F21 · 근거 파일 §4-7) — `SKILL.md` Step 0 구간에 `셸 실행 도구가 없는 세션` 1 · `파일 쓰기 도구만 없으면` 1 · `네 칸` · `재검증 명령` · `skill-design-guide.md` 각 1 이상 [exact, enumerated]
      (측정: `tok "$(sect "$T/SK" '### 0. CONTRACT_ROOT')" '셸 실행 도구가 없는 세션' '파일 쓰기 도구만 없으면' '네 칸' '재검증 명령' 'skill-design-guide.md'` 1 · 1 · 1 이상 · 1 이상 · 1 이상. 봉인 전 실측: 편집 전 0 · 0 · 0 · 0 · 0, 모의본 1 · 1 · 1 · 1 · 1. 문장 삭제 대조: 멈춤 문장만 지운 사본 첫 값 0, 「파일 쓰기 도구만 없으면 멈추지 말고 셸로 파일을 쓴다」만 지운 사본 둘째 값 0, 네 칸 문장만 지운 사본 셋째 값 0)
- [ ] SK-07: 자기진단 체크리스트의 true 뜻을 「문제가 있다」 하나로 고정한다 (카이젠 Step 2 피드백 분석) — (a) `SKILL.md` Step 7 구간에 `**모든 항목은 「문제가 있다」 가 true 다` 가 1 건, 측정 절의 옛 문구 12 개 합계 0, 항목 이름 줄 집합이 편집 전 23 개를 하나도 잃지 않고 25 개 (b) 가이드 §구조화 진단 체크리스트 구간에 `**모든 항목은 「문제가 있다」 가 true 다**` 1 건, 측정 절의 옛 문구 9 개 합계 0, 표의 항목 행 21 개 [exact, enumerated]
      (측정: (a) `S7=$(sect "$T/SK" '### 7. 자기진단')` · `tok "$S7" '**모든 항목은 「문제가 있다」 가 true 다'` 1 · 옛 문구 12 개 `비기능 요구사항이 조건에 반영되었는가?` · `적용 수준(file/section/field)이 명시되었는가?` · `표준형 4 요소(상태 전제/경로 한정/생성물 제외/기대 집합)를 다 채웠는가?` · `증거 기록물의 경로가 조건에 명시되었는가?` · `Step 6.5 게이트가 위반 0 건으로 통과했는가?` · `손으로 세지 않고 Step 6.2 명령 출력으로 채웠는가?` · `출력을 인용했는가?` · `봉인 직후 계약만 단독 커밋했는가?` · `조건 수정 또는 해소 기록을 남겼는가?` · `산출 명령이 있는가?` · `절이 있는가?` · `자기신고하지 않고 집합 비교로 계산했는가?` 를 각각 `printf '%s\n' "$S7" | grep -cF` 해 합이 0 ·
       ``N0=$(sect "$T/SK.0" '### 7. 자기진단' | grep -oE '^   - `[a-z_]+`:' | sort -u)`` · ``N1=$(printf '%s\n' "$S7" | grep -oE '^   - `[a-z_]+`:' | sort -u)`` 에서 `printf '%s\n' "$N1" | grep -c .` 25 · `comm -23 <(printf '%s\n' "$N0") <(printf '%s\n' "$N1") | grep -c .` 0
       (b) `G7=$(sect "$T/GD" '### 구조화 진단 체크리스트')` · `tok "$G7" '**모든 항목은 「문제가 있다」 가 true 다**'` 1 · 옛 문구 9 개 `(성능/보안/접근성)이 조건에 반영되었는가?` · `적용 수준(file/section/field)이 명시되었는가?` · `4 요소(상태 전제/경로 한정/생성물 제외/기대 집합)를 다 채웠는가?` · `증거 기록물의 경로가 조건에 명시되었는가?` · `검증 출력을 인용했는가?` · `수정 또는 해소 기록을 남겼는가?` · `산출 명령이 있는가?` · `절이 있는가?` · `자기신고하지 않고 집합 비교로 계산했는가?` 합 0 · `printf '%s\n' "$G7" | grep -cE '^\| [a-z_]+ \|'` 21.
       봉인 전 실측: 편집 전 (a) 0 · 12 · 23 · 0 (b) 0 · 9 · 19 — 옛 문구 21 개가 전부 편집 전 파일에서 1 씩 잡히므로 측정이 살아 있다. 모의본 (a) 1 · 0 · 25 · 0 (b) 1 · 0 · 21)

## Script

- [ ] SC-00: N/A (Script 카테고리는 `release.sh` 연동 · 버전 올림 · `marketplace.json` 갱신이다. 이 Phase 는 그 파일을 건드리지 않는다 — 공유 파일은 Final 몫. 측정: `my | grep -cE '^(scripts/release\.sh|\.claude-plugin/marketplace\.json|[^/]+/\.claude-plugin/plugin\.json)$'` 이 0)

## Error

- [ ] ER-01: 네 파일에 새로 생긴 URL 이 전부 이 Phase 의 외부 근거 파일 `.harness/.meta/evidence/phase2.md` 에 있다 — 근거 밖 자료를 인용하지 않았다 [exact, enumerated]
      (측정: `comm -23 <(comm -13 <(cat "$T"/SC.0 "$T"/SK.0 "$T"/GD.0 "$T"/RF.0 | url) <(cat "$T"/SC "$T"/SK "$T"/GD "$T"/RF | url)) <(url < .harness/.meta/evidence/phase2.md) | grep -c .` 0.
       양성 대조: 모의본 가이드 끝에 `https://example.invalid/x` 와 근거 안 URL 하나를 더해 같은 비교를 돌리면 1 — 봉인 전 실측 1)
- [ ] ER-02: 네 파일에 더한 줄에 번역투 6 종(`tone-kit/references/locale-korean.md` §2 치환표의 grep 열)이 0 건이다 [exact]
      (측정: `added | grep -cE "$K02"` 0. 양성 대조: 모의본 가이드에 「이 값은 훅에 의해 적용된다.」 · 「그것에 대해 말한다.」 두 줄을 더하면 2 — 봉인 전 실측 UTF-8 2 · C 로케일 1. 1 이 나오면 로케일이 틀린 것이라 측정 무효)
- [ ] ER-03: 바뀌는 규약을 받아 쓰는 반대편 가운데 이 Phase 범위 밖인 것을 명시적 미완으로 넘기고 건드리지 않는다 — `.harness/.meta/kaizen-0924/phase2-notes.md` 에 경로 12 개 `harness/agents/qa-evaluator.md:1217` · `harness/agents/qa-evaluator.md:590` · `harness/docs/guides/qa-evaluation-guide.md:12` · `harness/docs/guides/qa-evaluation-guide.md:742` · `harness/docs/guides/qa-evaluation-guide.md:746` · `harness/docs/guides/qa-evaluation-guide.md:1915` · `harness/docs/guides/qa-evaluation-guide.md:1785` · `harness/docs/guides/qa-evaluation-guide.md:1862` · `harness/skills/sprint/SKILL.md` · `harness/scripts/save-feedback.sh` · `harness/references/feedback-schema.yaml` · `harness/skills/contract-kaizen/SKILL.md` 와 처리 배정표 키 11 개 `F11` · `F12` · `F13` · `F17` · `F21` · `F27` · `harness:P03` · `harness:P05` · `harness:P06` · `harness:P08` · `user-setup:P5` 가 각각 1 회 이상 있고, 이 Phase 커밋이 그 여섯 파일을 하나도 건드리지 않는다 [exact, enumerated]
      (Given: BUILD 가 notes 를 쓰고 커밋한 뒤 · 측정: `test -f .harness/.meta/kaizen-0924/phase2-notes.md` exit 0 ·
       `for t in harness/agents/qa-evaluator.md:1217 harness/agents/qa-evaluator.md:590 harness/docs/guides/qa-evaluation-guide.md:12 harness/docs/guides/qa-evaluation-guide.md:742 harness/docs/guides/qa-evaluation-guide.md:746 harness/docs/guides/qa-evaluation-guide.md:1915 harness/docs/guides/qa-evaluation-guide.md:1785 harness/docs/guides/qa-evaluation-guide.md:1862 harness/skills/sprint/SKILL.md harness/scripts/save-feedback.sh harness/references/feedback-schema.yaml harness/skills/contract-kaizen/SKILL.md F11 F12 F13 F17 F21 F27 harness:P03 harness:P05 harness:P06 harness:P08 user-setup:P5; do printf '%s=%s\n' "$t" "$(grep -cF "$t" .harness/.meta/kaizen-0924/phase2-notes.md)"; done` 23 값 전부 1 이상 ·
       `my | grep -cE '^harness/(agents/qa-evaluator\.md|docs/guides/qa-evaluation-guide\.md|skills/(sprint|contract-kaizen)/SKILL\.md|scripts/save-feedback\.sh|references/feedback-schema\.yaml)$'` 0.
       봉인 전 실측: notes 없음 — 구현이 만들 파일이라 면제. 23 문자열을 담은 가짜 notes(가이드 줄마다 `경로:줄` 을 붙여 씀, `:742` 는 `:742-743` 꼴)로 돌리면 23 값 전부 1, `:746` · `:742-743` · `:12` · `:1915` 가 든 줄을 하나씩 지우면 그 값이 각각 0. 같은 네 줄을 `` `harness/docs/guides/qa-evaluation-guide.md` (`:12` · `:746` · `:1915`) `` 처럼 몰아 쓰면 가이드 토큰 여섯이 전부 0 이다 — notes 는 줄마다 `경로:줄` 로 쓴다 (2026-09-24 22:1x 실측, 스크래치 `p2build/er03.sh`). `my` 가 빈 목록이라 둘째 측정 0 — 가짜 목록에 `harness/skills/sprint/SKILL.md` 를 넣으면 1)

## Architecture

- [ ] AR-01: Diff-Scope 표준형이 세 문서에서 5 요소로 맞고, 커밋하고 나면 빈 출력이 되는 상태 전제를 평가 시점 조건에 쓰지 말라고 적는다 (메타 이슈 1 F2) — (a) 스키마 `#### Diff-Scope Oracle 표준형` 머리(첫 `#####` 전)에 `커밋하고 나면 빈 출력` 1 · `porcelain` 1 이상 · 옛 예시 `git diff --name-only HEAD -- app/lib` 0 · `**(1) 상태 전제**` 정의 줄에 `Given: 이 스프린트의 커밋이 끝난 뒤` 1 (b) 가이드 `##### Diff-Scope Oracle 표준형` 구간에 `4 요소` 0 · `5 요소` 1 이상 · 옛 규칙 `` 커밋 후 판정이 전제라면 조건에 `Given: 스테이징 완료 후` 를 쓰고 `` 0 · `커밋하고 나면 빈 출력` 1 · `git diff --name-only HEAD -- app/lib` 0 · 표의 `| 5 |` 행 1 (c) `SKILL.md` 전체 `4 요소` 0 · 가이드 전체 `표준형 4 요소` 0 [exact, enumerated]
      (측정: (a) `tok "$(sect "$T/SC" '#### Diff-Scope Oracle 표준형' | awk 'NR>1 && /^##### /{exit} 1')" '커밋하고 나면 빈 출력' 'porcelain' 'git diff --name-only HEAD -- app/lib'` 1 · 1 이상 · 0 · `sect "$T/SC" '#### Diff-Scope Oracle 표준형' | grep -F '**(1) 상태 전제**' | grep -cF 'Given: 이 스프린트의 커밋이 끝난 뒤'` 1
       (b) `GDS=$(sect "$T/GD" '##### Diff-Scope Oracle 표준형')` · `tok "$GDS" '4 요소' '5 요소' '커밋 후 판정이 전제라면 조건에 `Given: 스테이징 완료 후` 를 쓰고' '커밋하고 나면 빈 출력' 'git diff --name-only HEAD -- app/lib'` 0 · 1 이상 · 0 · 1 · 0 · `printf '%s\n' "$GDS" | grep -cE '^\| 5 \|'` 1
       (c) `grep -cF '4 요소' "$T/SK"` 0 · `grep -cF '표준형 4 요소' "$T/GD"` 0.
       봉인 전 실측: 편집 전 (a) 0 · 0 · 1 · 0 (b) 1 · 0 · 1 · 0 · 1 · 0 (c) 1 · 2. 모의본 (a) 1 · 2 · 0 · 1 (b) 0 · 1 · 0 · 1 · 0 · 1 (c) 0 · 0. (a) 넷째 값은 정의 줄 치환 전 모의본(초안판)에서 0 이었다 — 예시와 새 문단만 고치고 정의 줄은 옛 두 선택지로 남던 결함을 이 값이 잡는다. 문장 삭제 대조: 스키마 「… `--cached` 는 커밋하고 나면 빈 출력이다」만 지운 사본 (a) 첫 값 0, 정의 줄의 새 선택지만 지운 사본 (a) 넷째 값 0, 가이드 같은 문장만 지운 사본 (b) 넷째 값 0. 주장 자체는 `회귀 게이트` 절 스크래치 저장소 실측이 받친다)
- [ ] AR-02: 여러 주체가 한 가지에 커밋할 때의 두 선택지와 서명 줄 스니펫이 스키마에 들어가고, 그 스니펫이 알려진 답을 두 셸에서 낸다 (메타 이슈 1 F3) — (a) 스키마에 `##### 여러 주체가 한 가지에 커밋할 때` 로 시작하는 제목이 정확히 1 개이고 `#### Diff-Scope Oracle 표준형` 구간 안에 있으며, 그 소절에 7 토큰 `서명 줄` · `선택지 A` · `선택지 B` · `반대 방향` · `end_sha:` · `git commit -o` · `조용히 빠진다` 가 각각 1 건 이상 (b) 그 소절의 첫 `bash` 블록을 떼어 `회귀 게이트` 절의 `f3test.sh` 에 넣으면 bash · zsh 둘 다 `mine OK [a.md b.md ]` 와 `unsigned_on OK (c4)` 두 줄을 낸다 (c) `SKILL.md` Gotchas 구간에 `verify_seal` 과 `unsigned_on` 을 함께 담은 줄이 1 개 이상 — 메타 이슈 F1 의 스킬 쪽 안내 [exact, enumerated]
      (측정: (a) `grep -cE '^##### 여러 주체가 한 가지에 커밋할 때' "$T/SC"` 1 · `sect "$T/SC" '#### Diff-Scope Oracle 표준형' | grep -cE '^##### 여러 주체가 한 가지에 커밋할 때'` 1 · `tok "$(sect "$T/SC" '##### 여러 주체가 한 가지에 커밋할 때')" '서명 줄' '선택지 A' '선택지 B' '반대 방향' 'end_sha:' 'git commit -o' '조용히 빠진다'` 7 값 전부 1 이상
       (b) ``sect "$T/SC" '##### 여러 주체가 한 가지에 커밋할 때' | awk '/^```bash$/{f=1;next} f&&/^```$/{exit} f' > "$T/f3.sh"`` 뒤 `bash f3test.sh "$T/f3.sh"` · `zsh f3test.sh "$T/f3.sh"` 의 출력이 둘 다 `mine OK [a.md b.md ]` · `unsigned_on OK (c4)`.
       (c) `sect "$T/SK" '## Gotchas' | grep -F 'verify_seal' | grep -cF 'unsigned_on'` 1 이상.
       음성 대조: `--grep` 에서 `^` · `$` 를 뺀 변이는 `mine NG [a.md b.md other.md ]`, `grep -qxF "$_s" || echo "$_c"` 를 `true` 로 바꾼 변이는 `unsigned_on NG` — 봉인 전 실측 둘 다 NG.
       봉인 전 실측: 편집 전 제목 0 · 토큰 0 · 스니펫 0 줄 · (c) 0. 모의본 1 · 1 · 7 값 전부 1 이상 · 스니펫 10 줄 · bash/zsh 둘 다 두 줄 OK · (c) 1.
       문장 삭제 대조: 「서명 줄을 빠뜨린 커밋은 조용히 빠진다」 · 「그래서 반대 방향 확인을 함께 건다」 · `git commit -o` 커밋 규칙 · `end_sha:` 상한 문장을 하나씩 지운 사본에서 (a) 해당 토큰이 각각 0, Gotcha 의 「`verify_seal` 로 … `unsigned_on` 으로 잰다」 문장만 지운 사본 (c) 0)
- [ ] AR-03: 검사 스크립트 전체 통과를 조건으로 걸지 말라는 규칙이 새 태그 없이 들어간다 (메타 이슈 1 F4) — 스키마 `#### 조건 작성 preflight` 구간 안에 `##### 검사 스크립트 전체 통과를 조건으로 걸지 마라` 로 시작하는 제목이 1 개, 그 소절에 4 토큰 `측정-환경-오염` · `소유한 줄의 이름` · `마지막 단계(카이젠이면 Final)` · `` `mine` `` 이 각각 1 건 이상이고, preflight 표의 태그 행이 편집 전과 같은 10 개다 [exact, enumerated]
      (측정: `sect "$T/SC" '#### 조건 작성 preflight' | grep -cE '^##### 검사 스크립트 전체 통과를 조건으로 걸지 마라'` 1 · ``tok "$(sect "$T/SC" '##### 검사 스크립트 전체 통과를 조건으로 걸지 마라')" '측정-환경-오염' '소유한 줄의 이름' '마지막 단계(카이젠이면 Final)' '`mine`'`` 4 값 전부 1 이상 · ``sect "$T/SC" '#### 조건 작성 preflight' | grep -cE '^\| `[^`]+` \|'`` 10.
       봉인 전 실측: 편집 전 0 · 전부 0 · 10, 모의본 1 · 1 · 1 · 1 · 1 · 10. 문장 삭제 대조: 세 규칙 불릿(소유한 줄의 이름 · `mine` 대조 · 마지막 단계)을 하나씩 지운 사본에서 해당 토큰이 각각 0. 초안의 `소유한 줄` · `마지막 단계` 는 둘째 불릿과 실측 문단에도 있어 불릿을 지워도 1 이상이었다)
- [ ] AR-04: 스키마 셸 이식성 규약에 zsh 배열 첨자 줄이 들어간다 (user-setup:P5 · harness:P05 의 zsh 줄) — §셸 이식성 규약 구간에 5 토큰 `KSH_ARRAYS` · `for x in "${arr[@]}"` · `zsh.sourceforge.io` · `gnu.org/software/bash` · `1 부터` 가 각각 1 건 이상 [exact, enumerated]
      (측정: `tok "$(sect "$T/SC" '### 셸 이식성 규약')" 'KSH_ARRAYS' 'for x in "${arr[@]}"' 'zsh.sourceforge.io' 'gnu.org/software/bash' '1 부터'` 5 값 전부 1 이상. 봉인 전 실측: 편집 전 전부 0 — `"${arr[@]}"` 만으로 재면 편집 전 규약(`:88`)에서 이미 1 이라 `for x in` 을 붙였다. 모의본 전부 1)
- [ ] AR-05: 버전 표기가 서로 맞는다 — (a) 스키마에 `현재: **v5.5** (2026-09-24)` 1 · `현재: **v5.4**` 0 · 변경 이력 줄 `- **v5.5 (2026-09-24)**` 1 · 머리 `최근 갱신: 2026-09-24` 1 (b) 가이드 머리 설정이 `version: v5.1` · `last_updated: 2026-09-24` (c) 가이드 §버전 정보 에 `| Schema version | v5.5 |` 1 · `v5.0` 0 · `v5.1` 1 이상, `| Parity with |` 행의 값이 `$END` 판 두 설계 가이드 머리 설정 `version` 과 같다 [exact, enumerated]
      (측정: (a) `tok "$(cat "$T/SC")" '현재: **v5.5** (2026-09-24)' '현재: **v5.4**' '- **v5.5 (2026-09-24)**' '최근 갱신: 2026-09-24'` 1 · 0 · 1 · 1
       (b) `head -5 "$T/GD" | grep -cE '^(version: v5\.1|last_updated: 2026-09-24)$'` 2
       (c) `VI=$(sect "$T/GD" '### 버전 정보')` · `printf '%s\n' "$VI" | grep -cF '| Schema version | v5.5 |'` 1 · `printf '%s\n' "$VI" | grep -cF 'v5.0'` 0 · `printf '%s\n' "$VI" | grep -cF 'v5.1'` 1 이상 · `SV=$(git show "$END:harness/docs/guides/skill-design-guide.md" | sed -n 's/^version: //p' | head -1)` · `AV=` 같은 꼴 agent 가이드 · `printf '%s\n' "$VI" | grep -F '| Parity with |' | grep -cF "skill-design-guide $SV · agent-design-guide $AV"` 1.
       봉인 전 실측: 편집 전 (a) 0 · 1 · 0 · 0 (b) 0 (c) 0 · 1 · 0 · 0 — `SV/AV` 는 `1.6.0/1.7.0`. 모의본 (a) 1 · 0 · 1 · 1 (b) 2 (c) 1 · 0 · 1 · 1)
- [ ] AR-06: 이 Phase 의 변경이 허용 경로 안에 머물고 기존 Gotcha 는 덧붙이기만 했다 [exact, enumerated]
      (Given: BUILD 가 개정 파일에 `end_sha:` 를 적은 뒤 · 이 Phase 커밋 메시지마다 서명 줄 `Kaizen-Phase: kaizen-0924-p02-contract` · 측정 넷 —
       ① `unsigned_on "$B" "$END" "$SIG" "$SC" "$SK" "$GD" "$RF" | grep -c .` 0 (네 파일을 건드린 구간 안 커밋이 전부 서명했다 — 다른 Phase 가 이 네 파일을 건드리지 않았다)
       ② `.harness/` 밖은 네 파일뿐이다 — `my | grep -vE '^(\.harness/|harness/references/contract-schema\.md$|harness/skills/sprint-contract/SKILL\.md$|harness/docs/guides/contract-design-guide\.md$|harness/skills/sprint-contract/references/red-flags\.md$)' | grep -c .` 0 · `my | grep -cxE 'harness/(references/contract-schema|skills/sprint-contract/SKILL|docs/guides/contract-design-guide|skills/sprint-contract/references/red-flags)\.md'` 4
       ③ `harness/references/contract-schema.md` §`.harness/` 범위 조건 의 권장 형태 — `find .harness -type f -name 'sprint-contract*.md' -print0 | while IFS= read -r -d '' f; do verify_seal "$f"; done | awk '{print $1}' | sort | uniq -c` 를 근거로 남기고, 그 가운데 이 Phase 몫인 `SEAL_BROKEN` 이 0 개 — `find .harness -type f -name 'sprint-contract*.md' -print0 | while IFS= read -r -d '' f; do verify_seal "$f"; done | awk '$1=="SEAL_BROKEN"{print $2}' | sort -u | comm -12 - <( { my; echo .harness/sprint-contract-kaizen-0924-p02-contract.md; } | sort -u) | grep -c .` 0. `SEAL_BROKEN` 줄의 파일이 `my` 에도 없고 이 계약도 아니면 다른 Phase 몫이다 — 파일 이름을 근거에 적고 이 조건에는 세지 않는다
       ④ Gotchas 덧붙이기만 — `comm -23 <(sect "$T/SK.0" '## Gotchas' | grep '^- ' | sort) <(sect "$T/SK" '## Gotchas' | grep '^- ' | sort) | grep -c .` 0.
       봉인 전 실측: ① 0 줄 ② 0 · 0 (`my` 가 빈 목록) — 가짜 목록으로 돌림: 네 파일 + `.harness/` 세 줄이면 0 · 4, `harness/skills/sprint/SKILL.md` 가 섞이고 한 파일이 빠지면 1 · 3 ③ SEAL_OK 51 · SEAL_ABSENT 11 · SEAL_BROKEN 0 · 이 Phase 몫 0 ④ 편집 전 42 줄 · 모의본 45 줄 · 잃은 줄 0 (Gotchas 구간에서 불릿으로 시작하는 줄 수. 초안의 44 · 47 은 `:32-75` 줄 범위를 센 값이라 고쳤다) — 모의본에서 옛 Gotcha 한 줄을 고친 변이는 1)

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다. 이번 변경에 적용: 네 파일에 더한 줄의 버전꼴 문자열(`x.y.z`)이 가이드 `| Parity with |` 행에 옮겨 적는 두 설계 가이드 버전(`$END` 판 머리 설정에서 읽은 값) 말고 0 건이다 — 그 두 값이 원본과 같은지는 AR-05 (c) 가 잰다 [exact]
      (측정: `SV` · `AV` 를 AR-05 (c) 처럼 읽은 뒤 `added | grep -oE 'v?[0-9]+\.[0-9]+\.[0-9]+' | sed 's/^v//' | sort -u | grep -vxF -e "$SV" -e "$AV" | grep -c .` 0. 양성 대조: 모의본 가이드에 `버전 9.9.9 와 1.6.0` 줄을 더하면 1 (`9.9.9` 만) — 봉인 전 실측 1)
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```` ```text, ```bash, ```yaml ```` 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 이번 변경에 적용: V6 는 `harness/references/` · `skills/*/SKILL.md` 만 읽고 가이드 · `red-flags.md` 는 읽지 않으므로 네 파일을 같은 판정에 펜스 길이를 더한 검출기로 잰다 [exact]
      (측정: `회귀 게이트` 절의 `fence.py` 를 `"$T/SC" "$T/SK" "$T/GD" "$T/RF"` 에 돌려 `bare_open_total=0 unclosed_total=0`. V6 쪽은 DG-05.
       양성 대조: 모의본 가이드 끝에 언어 힌트 없는 펜스를 더하면 `bare_open_total=1` — 봉인 전 실측 1)

## Reusability

- [ ] RE-01: N/A (산출물이 계약 형식 문서 넷뿐이라 재사용 단위 코드가 없다. 측정: `my | grep -vcE '\.md$'` 이 0)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다. 이번 변경에 적용: 새 규칙은 기존 절 · 표(조건 패턴 표 · 조건 수 표 · 체크리스트 표 · parity 표 · 버전 정보 표)에 행과 문단으로만 들어가고 새 표를 만들지 않는다 — 네 파일의 표 구분줄 수가 편집 전과 같다 [exact]
      (측정: `for k in SC SK GD RF; do printf '%s=%s ' "$k" "$(grep -cE '^[[:space:]]*\|[-: |]+\|[[:space:]]*$' "$T/$k")"; done` 이 `SC=15 SK=6 GD=18 RF=1`. 봉인 전 실측: 편집 전 · 모의본 모두 15 · 6 · 18 · 1)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `my | grep -c '^scripts/release.sh$'` 이 0)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (`diagnostics.ide_exclude` 값 `[]`) — 이번 변경에 적용: 편집기 마크다운 확장과 같은 조건(markdownlint-cli2 0.23.2 · MD013 끔)으로 네 파일의 **더한 줄**에 걸린 경고가 0 이다. 편집 전부터 있던 경고는 `범위 경계` 절에 적은 대로 범위 밖이다 [exact]
      (측정: `회귀 게이트` 절의 고친 `new-warnings.sh` 를 `for k in SC SK GD RF; do bash new-warnings.sh "$T/$k.0" "$T/$k"; done` 로 돌려 네 줄 모두 `new_warnings=0`.
       양성 대조: 표 구분줄을 `|--------|--------|` 로 둔 스키마 모의본 1 (1228 행 MD060), 굵은 글씨 줄 바로 뒤에 빈 줄 없이 목록을 붙인 스킬 모의본 1 (460 행 MD032) — 봉인 전 실측 1 · 1.
       알려진 답: 고친 판은 red-flags 모의본에서 0 (경고 13 행은 더한 줄 7 · 8 이 아니다), 옛 판은 열 번호 8 을 줄로 읽어 1)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: DG-01 과 같은 명령이 0)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 변경 파일이 문서뿐. 측정: RE-01 과 같은 명령이 0)
- [ ] DG-05: 저장소 검사 두 개가 이 Phase 파일에 대해 깨끗하다 — (a) `python3 scripts/validate-plugin.py harness` 출력에 `V6` · `V9` · `V10` 줄이 있고 셋 다 `ERROR` · `FAIL` 이 아니며, 이 Phase 네 파일을 가리키는 `FAIL` 줄이 0 (b) `python3 scripts/check-stale-values.py` 가 종료 코드 2(검사 범위 빔)가 아니고 출력에 이 Phase 네 파일 경로가 0 건 [exact]
      (Given: 작업 트리의 네 파일이 `$END` 와 같다 — `git diff --quiet "$END" -- "$SC" "$SK" "$GD" "$RF"` exit 0 · 측정: (a) `python3 scripts/validate-plugin.py harness > "$T/vp.txt" 2>&1` 뒤 `grep -cE '^  V(6|9|10) ' "$T/vp.txt"` 3 · `grep -E '^  V(6|9|10) ' "$T/vp.txt" | grep -cE 'ERROR|FAIL'` 0 · `grep -F 'FAIL' "$T/vp.txt" | grep -cE 'harness/(references/contract-schema|skills/sprint-contract/SKILL|docs/guides/contract-design-guide|skills/sprint-contract/references/red-flags)\.md'` 0
       (b) `python3 scripts/check-stale-values.py > "$T/sv.txt" 2>&1; echo $?` 가 0 또는 1 · 같은 네 경로 정규식으로 `grep -cE` 0. 1 이 나오면 되살아난 값의 파일이 이 Phase 네 파일이 아닐 때만 다른 Phase 몫으로 근거에 적는다.
       양성 대조: 스크래치 사본의 SKILL.md 끝에 `awk x $1` 한 줄 → V9 `1 arg-substitution hazard(s)` · `FAIL harness/skills/sprint-contract/SKILL.md:857` — 봉인 전 실측. 편집 전 · 모의본 모두 10 검사 OK, check-stale-values exit 0)
- [ ] DG-06: `python3 scripts/validate-post-kaizen.py --since 76cfb376e2293350e2583c50166286bd2ec95b82` 출력의 `scope-isolation` · `doc-contracts` 줄이 `FAIL` · `ERROR` 가 아니다. `docs-site-regen` 은 Final F2 몫이라 판정에서 뺀다. 다른 Phase 커밋 때문에 `scope-isolation` 이 FAIL 이면 `--verbose` 위반 커밋 목록에 서명 줄 커밋이 없을 때 이 조건은 PASS 다. `doc-contracts` 가 `FAIL` · `ERROR` 이면 `python3 scripts/validate-doc-contracts.py -v` 의 `검사:` 줄에 나온 경로를 `my` 와 대조해, 겹치는 경로가 0 개면 다른 Phase 몫으로 근거에 적고 이 조건은 PASS 다 [exact]
      (측정: 명령 출력의 두 줄. `doc-contracts` 가 `FAIL` · `ERROR` 일 때만 — `python3 scripts/validate-doc-contracts.py -v 2>&1 | awk -F' → ' '/^ *검사: /{a=$1; sub(/^ *검사: /,"",a); sub(/:[0-9]+$/,"",a); print a; print $2}' | sort -u | comm -12 - <(my) | grep -c .` 0.
       `scope-isolation` 이 `FAIL` 일 때만 — `python3 scripts/validate-post-kaizen.py --since "$B" --verbose > "$T/vpk.txt" 2>&1` 뒤
       `awk '/ scope-isolation: /{f=1;next} /^\[ /{f=0} f&&/^ +[0-9a-f]{7,40}$/{print $1}' "$T/vpk.txt" | grep -c .` 이 1 이상(위반 목록을 실제로 읽었다) ·
       `awk '/ scope-isolation: /{f=1;next} /^\[ /{f=0} f&&/^ +[0-9a-f]{7,40}$/{print $1}' "$T/vpk.txt" | while read -r c; do git log -1 --format=%B "$c" | grep -qxF "$SIG" && echo "$c"; done | grep -c .` 0.
       첫 값을 함께 거는 이유: 출력 형식이 바뀌어 목록을 하나도 못 읽으면 둘째 값이 조용히 0 이 된다. 검사 스크립트는 위반 커밋을 앞 8 자리로 찍는다(`check_scope_isolation` 의 `commit[:8]`) — 정규식은 7~40 자리를 받는다.
       봉인 전 실측: `15 checks — 12 PASS / 0 FAIL / 0 ERROR / 3 SKIP`, scope-isolation PASS · doc-contracts PASS · docs-site-regen SKIP — 지금 출력에서 위반 목록을 읽은 수 0 (예외 분기를 쓰지 않는 경우).
       예외 분기 양성 대조: 위반 목록에 `51a22b4` · `43fc9ee` 두 줄을 넣은 가짜 출력에서 `SIG` 를 Phase 1 서명 줄 `Kaizen-Phase: kaizen-0924-p01-guides` 로 두면 읽은 수 2 · 서명 커밋 1, `SIG` 를 이 Phase 서명 줄로 두면 2 · 0 — `C.UTF-8` · `C` 두 로케일에서 같다)
- [ ] DG-07: contract-kaizen 회귀 확인(카이젠 스킬 Step 7 Regression Smoke Test) — `harness/evals/kaizen/contract-kaizen/assertions.json` 의 패턴 6 개가 `$END` 판 대상 파일에서 각각 1 건 이상 잡힌다 [exact, enumerated]
      (측정: `회귀 게이트` 절의 `dg07.py` 를 `python3 dg07.py "$T/SK" "$T/GD"` 로 돌려 6 값 전부 1 이상 — assertions.json 의 `file` 이 스킬이면 `"$T/SK"`, 가이드면 `"$T/GD"` 에서 `pattern` 을 센다.
       봉인 전 실측: 편집 전 3 · 19 · 2 · 2 · 1 · 2, 모의본 3 · 19 · 2 · 2 · 2 · 2)
