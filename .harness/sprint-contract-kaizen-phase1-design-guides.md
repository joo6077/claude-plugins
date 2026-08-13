---
feature: "카이젠 Phase 1 — 설계 가이드 사실 정정(§A) + 신규 델타 3 조항(§C/§D/§E)"
created: "2026-08-13 10:20"
complexity: "complex"
conditions: 23
slug: kaizen-phase1-design-guides
status: done
owner_session: df1b3e15-30b3-4825-a3c4-4ac44c686e94
---

## 배경

`.harness/.meta/evidence/phase1.md` 가 이번 Phase 의 **유일한 외부 근거**다. 네 갈래 작업이다.

1. **§A 사실 정정 (최우선).** 공식 subagent 스펙과 어긋나는 서술을 두 가이드에서 전수 정정한다.
   직전 사이클(2026-07-27)이 "서브에이전트 중첩 불가" 4 곳을 고쳤으나, **frontmatter 필드 표는
   손대지 않았다.** 실측 결과 표가 16 행인데 공식은 15 종이고, 차이는 `initialPrompt` 다.
2. **§C 탐색형 발산 억제.** 글로벌 REJECT `UI-04`(2026-08-12) 가 실측 근거 — 계약이 4 축을
   지정했는데도 variant 2 개가 4 축 전부 동일값이었다. **축 선언만으로는 부족하고 축 값의
   상이성이 기계적으로 검사 가능해야 한다.**
3. **§D 사용자 관측 우선순위.** 자기 증거와 사용자 보고가 충돌할 때의 우선순위가 두 가이드
   어디에도 없다. §3.7 Completion Evidence Gate 는 *자기 증거의 유효성*만 다룬다.
4. **§E enforcement 승급 조건.** 현행 §3.7 은 **재발 시 승급 규칙**만 있고 **최초 등급을 무엇으로
   고를지**의 기준이 없다. 더 근본적으로, **가이드의 어떤 원칙이 지금 몇 등급인지 기록이 없어
   재발해도 "무엇에서 무엇으로 올릴지" 를 판정할 수 없다.** 이번 사이클 프레이밍(문장 추가 금지 ·
   등급 상향으로 처리)이 실제로 작동하려면 이 원장이 먼저 있어야 한다.

`/insights` 2026-08-13 Friction #1~#3 은 직전 사이클에 이미 구조적으로 승격됐고 리포트 관측 윈도가
수정 착지일 이전을 대부분 포함한다. **같은 취지의 규칙 문장을 다시 추가하지 않는다.**

## 리서치 소스 (evidence 파일 한정 — 외부 조회 0 회)

- `.harness/.meta/evidence/phase1.md` §A~§G (URL·인용문 전부 이 파일에서만 인용)
- `.harness/.meta/kaizen-data-pool.md` §1 — 최근 REJECT `UI-04` / `ER-02` / `AR-04`
- `.claude/kaizen-input/insights-report.md` — 직전 사이클 흡수분 표 + 신규 델타 D2/D3
- `docs/kaizen/changelog.md` `[2026-07-27]` / `[2026-07-28]`

## GAP 분석 (전부 실측)

| # | 갭 | 실측 근거 | 처리 |
| --- | --- | --- | --- |
| G1 | agent frontmatter 표가 공식 15 종과 불일치 (16 행) | 표 파싱 결과 `initialPrompt` 추가 존재 | §A 정정 |
| G2 | `prompt` 가 frontmatter 필드로 오인될 여지 | 가이드에 언급 0 건 · evidence 는 "`--agents` JSON 전용" 명시 | 각주 추가 |
| G3 | 탐색형 산출물의 개수 상한·축 고정 조항 없음 | `grep -c "Variant"` = 0 · REJECT UI-04 | §5.6 신설 |
| G4 | "Exploration Budget" 이 agent §7 에 이미 다른 뜻으로 존재 | agent-design-guide:426 | 이름 충돌 명시 구분 (§5.5 L1/L2/L3 선례) |
| G5 | 사용자 관측 vs 자기 증거 우선순위 조항 없음 | 두 가이드 grep 0 건 | §3.8 신설 |
| G6 | 최초 enforcement 등급 선택 기준 없음 | §3.7 은 승급 규칙만 보유 | 기존 표 보강 |
| G7 | 원칙별 현재 등급 원장 없음 → 재발해도 승급 대상 불명 | §3.7 전체 grep 0 건 | 원장 표 신설 |
| G8 | parity 표 헤더가 "(5개)" 인데 실제 12 / 7 행 | awk 계산 | 헤더 수치 정정 |

### 오라클 유효성 사전 검증 (직전 사이클 최대 교훈)

계약 작성 시점에 오라클 후보 3 개를 실행해 **오탐을 먼저 확인**했다.

- 나이브 `grep -nE '^```[[:space:]]*$'` → **60 건**. 전부 닫는 펜스 오탐이다.
- 토글 인식 awk → **2 건**. 4-백틱 바깥 펜스 안의 예시 코드를 오탐한다 (skill-design-guide:737,751).
- 펜스 길이 인식 검출기 → **0 건**. 이것만 유효 오라클로 채택한다 (AP-03 · DG-01).
- 나이브 `grep -nE '중첩.*금지'` → **2 건**. 둘 다 "금지가 아니다" 라는 **정정 서술**이므로 오탐.
  AR-03 은 금지 단언 문구 7 종 집합으로 대체한다.

## 범위 경계

- 수정 허용: `harness/docs/guides/skill-design-guide.md`, `harness/docs/guides/agent-design-guide.md`,
  그리고 이 계약 파일. **그 외 0 파일.**
- `Script` 카테고리는 조건을 만들지 않는다 — 이 스프린트에 스크립트 변경이 없다.
- `Diagnostics` 는 문서 표면에 맞게 정의한다 (`project.yaml.commands.analyze` 는
  `bash -n scripts/release.sh` 라 이 변경과 무관하며 무조건 통과해 오라클 가치가 0 이다).
- 조건 수가 복잡도 밴드 상단인 이유: 파일은 2 개지만 손대는 **표면**이 많다 —
  섹션 신설 3 · 기존 표 보강 3 · parity 표 양면 2 · 요약 표 양면 2 · frontmatter 2.
- `## 2. 스킬 9가지 유형 체크리스트` **헤더 문자열은 바꾸지 않는다.** 레포 밖 6 개 surface 가
  이 문구를 리터럴로 참조한다 (`CLAUDE.md:325`, `harness/skills/create-skill/SKILL.md:5,45,107`,
  `harness/evals/evals.json:35`, `.claude/skills/create-kit/SKILL.md:44`,
  `flutter-toolkit/skills/flutter-kaizen/SKILL.md:158`, `.claude/skills/kaizen-orchestrator/references/search-sources.md:78`).
  표 아래 주석("1~9 는 공식, 10 은 레포 추가")만 갱신한다.

## 회귀 게이트

- 계약 작성 시점 baseline: `git status --porcelain` → **0 행**.
- 두 가이드의 기존 URL 37 개는 삭제하지 않는다 (`urls-before` 스냅샷 대조).
- 직전 사이클 승격물(Enforcement 3 등급 · Completion Evidence Gate · Counterpart Enumeration ·
  Pre-Edit Batch Audit · Scope-Bound Edits)의 **기존 문장을 삭제하거나 약화하지 않는다.**

## Architecture

- [ ] AR-01: `agent-design-guide.md` "frontmatter 전체 필드" 표의 필드명 집합이 공식 15 종
      (`name` `description` `tools` `disallowedTools` `model` `permissionMode` `maxTurns` `skills`
      `mcpServers` `hooks` `memory` `background` `effort` `isolation` `color`) 과 **양방향 차집합
      0** 으로 일치한다 [exact, enumerated]
      (측정: 표 구간 awk 추출 → `comm -3` 로 정본 목록과 대조, 양쪽 잔여 0 행)
- [ ] AR-02: `initialPrompt` 가 위 표의 행에서 사라지고, 표 **바깥** 서술에 "공식 필드 표 미등재"
      취지로 1 회 이상 남는다 [exact]
      (측정: 표 구간 추출 결과에 `initialPrompt` 0 건 AND 표 종료 라인 이후 본문에 1 건 이상)
- [ ] AR-03: 두 가이드 전체에 중첩 금지 단언 문구 7 종
      (`중첩 불가` `중첩은 불가` `중첩할 수 없` `하위 위임 불가` `하위 위임이 금지`
      `서브에이전트를 스폰할 수 없` `자기 아래로 위임할 수 없`) 이 **0 건**이다 [exact, enumerated]
      (측정: `grep -nE` 문구 집합 · 나이브 `중첩.*금지` 는 정정 서술 2 건을 오탐하므로 쓰지 않는다)
- [ ] AR-04: 스프린트 변경이 정확히 3 경로로 한정된다 [exact, enumerated]
      (Given: 커밋 직전 working tree ·
       측정: `git status --porcelain` 출력이 정확히 3 행이고 경로 집합이
       `harness/docs/guides/skill-design-guide.md`,
       `harness/docs/guides/agent-design-guide.md`,
       `.harness/sprint-contract-kaizen-phase1-design-guides.md` 와 정확히 일치)

## Skill

- [ ] SK-01: `skill-design-guide.md` §2 유형 표에 11 번 행 "탐색형 생성" 이 추가되고, 표 아래
      주석의 레포 추가분 표기가 `10~11` 로 갱신된다 [exact]
      (측정: 표 구간에서 `^| 11 |` 1 행 존재 AND 주석에 `10~11` 1 건)
- [ ] SK-02: `skill-design-guide.md` 에 Variant Budget 조항 섹션이 신설되고 5 요소를 모두 담는다
      — (a) 기본 산출물 상한 3 (b) primary axis 1 · secondary 최대 1 (c) Variant Matrix 표
      (d) 요청받지 않은 부대 산출물 생성 금지 (e) 축 값 상이성의 기계 검사
      [structural, enumerated] (측정: 섹션 구간 안에서 5 요소 각각 1 건 이상 grep)
- [ ] SK-03: 그 섹션이 `agent-design-guide.md` §7 "Exploration Budget" 과 **다른 개념임을
      명시적으로 구분**한다 [exact]
      (측정: 섹션 구간에 `Exploration Budget` 과 `§7` 이 같은 문단에 함께 등장 1 건 이상)
- [ ] SK-04: `skill-design-guide.md` 에 User-Reported Failure Gate 섹션이 신설되고 4 요소를 모두
      담는다 — (a) `REOPENED` 상태어 (b) oracle validity 재현 축 6 종
      (URL/브랜치/viewport/디바이스/auth·cache/데이터 상태) (c) 사용자 관측 반박 금지
      (d) 완료 선언 해제 조건 3 택 [structural, enumerated]
      (측정: 섹션 구간 안에서 4 요소 각각 1 건 이상 grep · 재현 축은 6 개 전부)
- [ ] SK-05: §3.7 Enforcement 3 등급 표에 **초기 등급 선택 기준**이 E1 · E2 · E3 각각에 대해
      기술된다 [structural] (측정: 표 또는 인접 서술에서 세 등급별 선택 조건 3 건 확인)
- [ ] SK-06: §3.7 에 **본 가이드 원칙의 현재 enforcement 등급 원장** 표가 존재하고, 모든 행이
      (원칙 · 현재 등급 · 승급 트리거) 3 열을 채우며 행 수가 6 이상이다 [structural, enumerated]
      (측정: 원장 표 구간 행 수 계산 ≥ 6 AND 빈 셀 0)
- [ ] SK-07: §3.7 에 "E3 단일 게이트가 전체 성공을 보장하지 않으며 계층 방어가 필요하다" 취지의
      서술이 근거 URL 2 개(`arxiv.org/html/2607.07405`, `anthropic.com/research/trustworthy-agents`)
      와 함께 존재한다 [exact] (측정: 해당 문단에 두 URL 모두 등장)
- [ ] SK-08: 두 가이드의 `## 요약` 표에 이번 신규 원칙 행이 각각 2 행씩 추가된다
      [exact, enumerated] (측정: skill 요약 표에 `Variant Budget` 1 행 + `User-Reported` 1 행,
      agent 요약 표에 `사용자 보고` 1 행 + `Variant Budget` 1 행)

## Error

- [ ] ER-01: evidence §F 금지 5 항의 단언이 신규 서술에 **0 건**이다 [exact, enumerated]
      (측정: `MUST 라고 세게`, `self-review 가 deterministic`, `사용자 보고는 항상 사실`,
       `모든 창의 작업은 시작 전 반드시 질문`, `서브에이전트 중첩 불가` 5 패턴 grep 0 건)
- [ ] ER-02: 신규·보강 3 조항(Variant Budget · User-Reported Failure Gate · Enforcement 등급 보강)
      각각에 evidence §G 의 **트레이드오프 서술**이 1 개 이상 포함된다 [structural, enumerated]
      (측정: 세 섹션 구간 각각에서 `트레이드오프` 또는 `비용` 을 포함한 대가 서술 1 건 이상)
- [ ] ER-03: 편집 후 두 가이드의 URL 집합에서 (편집 전 URL 37 개 ∪ evidence URL 11 개) 를 뺀
      **차집합이 공집합**이다 [exact, enumerated]
      (측정: `grep -ohE 'https?://[^ )>"]+'` → sort -u → `comm -23` 결과 0 행)

## Anti-patterns

- [ ] AP-03: bare code fence 0 건 [exact]
      (측정: 펜스 길이 인식 검출기 `bare_open_total=0` · 나이브 `^```$` grep 은 닫는 펜스 60 건을
       오탐하므로 오라클로 쓰지 않는다)
- [ ] AP-01: 신규 서술에 도구·플러그인 **버전 문자열 하드코딩이 없다** [exact]
      (측정: 신규 추가 라인에서 `[0-9]+\.[0-9]+\.[0-9]+` 패턴이 frontmatter `version` 2 행을
       제외하고 0 건)

## Reusability

- [ ] RE-01: `skill-design-guide.md` 의 신규 섹션 **제목**에 `Exploration Budget` 을 재사용하지
      않는다 [exact] (측정: `^### ` / `^## ` 헤더 라인 중 `Exploration Budget` 포함 0 건)
- [ ] RE-02: 신규 원칙 2 종이 새 전파 메커니즘을 만들지 않고 **기존 parity 표에 행으로 등록**된다
      [structural, enumerated] (측정: skill §11 표와 agent §12 표 각각에서 신규 항목 2 건씩 존재)

## Diagnostics

- [ ] DG-01: 펜스 길이 인식 검출기가 두 파일 합계 `bare_open_total=0` 이고 미닫힘 펜스 0 건이다
      [exact] (측정: 검출기 출력)
- [ ] DG-02: 두 가이드 parity 표 헤더의 `(N개)` 가 **실제 행 수와 일치**한다 [exact]
      (측정: awk 로 표 행 수를 계산해 헤더 숫자와 비교 — 숫자를 타이핑하지 않고 계산)
- [ ] DG-03: 두 가이드 frontmatter 의 `version` 이 minor bump 되고 `last_updated` 가
      `2026-08-13` 이다 [exact] (측정: frontmatter 2 필드 대조 — skill 1.4.0→1.5.0,
      agent 1.5.0→1.6.0)
- [ ] DG-04: 신규·수정 서술이 인용한 섹션 번호(`§N` / `§N.N`)가 **대상 파일에 실제 헤더로
      존재**한다 [exact, enumerated] (측정: 신규 인용 § 목록을 추출해 각 파일 헤더 목록과 대조,
      부재 0 건)
