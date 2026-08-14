---
feature: "카이젠 ↔ 메모리 연동 — 데이터 풀 §0.5 읽기 + grounding 축 + 승격 후보 산출"
slug: kaizen-memory-integration
created: "2026-08-14 18:10"
complexity: "복잡"
conditions: 21
status: active
owner_session: 1e76aa0b-dd42-4693-b79a-c2e2e6dfb88f
---

## 배경

카이젠 오케스트레이션이 **메모리를 읽지도 쓰지도 않는다.** 데이터 풀은 §0(`/insights`) ·
§1(글로벌 evaluator 피드백) · §2(외부 프로젝트) · §3(followup) · §4(최근 계약) ·
§5(validate-plugin) · §6(참조 가이드)로 구성되고, `~/.claude/projects/*/memory/` 는 한 번도
참조되지 않는다 (`grep -c memory .claude/skills/kaizen-orchestrator/SKILL.md` → **0**).

**실측 근거.** `feedback-oracle-must-execute-not-grep` 이 2026-07-28 에 기록됐다 —
*"계약 조건의 측정 oracle 을 '문서에 서술이 존재하는가' 로 쓰면 문언상 전부 PASS 인데 기능이
깨진 상태를 통과시킨다"*. 그런데 2 주 반 뒤 kaizen-2026-08-13 사이클의 재평가 REJECT **3 건이
정확히 그 유형**이었다 (phase6 AR-03 · phase13 AP-03 · phase12a SC-04, 전부 계약 측정문 결함).
루프가 메모리를 안 먹어서 계약 작성 단계에 전달되지 않았다.

### 왜 저자가 아니라 근거로 가르는가

메모리의 `feedback_*.md` 는 **전부 Claude 가 쓴 것**이므로 저자(`origin: session | kaizen`)로
가르면 모두 같은 쪽에 떨어져 아무것도 끊기지 않는다. 가를 축은 **무엇이 그 교훈을
뒷받침하느냐** 다. 문헌이 지목한 오염 경로는 *"국소적으로 맞지만 이전 불가능한 경험을
과일반화"* — 즉 **외부 검증 없는 자기추론**이 영속 규칙으로 증류되는 것이다. QA 가 REJECT 를
냈다거나 명령 출력이 그렇다는 것은 자기주장이 아니라 기계적 뒷받침이다.
차단할 것은 "카이젠이 썼다" 가 아니라 **"아무도 확인하지 않았다"** 다.

### 사용자 결정 사항

- 수집 범위: **전 프로젝트 교차** (`~/.claude/projects/*/memory/`)
- 소급 태깅: **104 건 전부 자동 태깅 + 샘플 검수** (정확도 측정)
- 회수 선별: **관련성 · 중요도 2 축.** recency 제외 — `modified` 필드가 104 중 44 건에만 있어
  60 건이 임의 판정된다
- 훅 2 종(dir-wide autofixer 차단 · 계약 린터)은 **별도 스프린트로 분리**.
  메모리와 독립 검증되며 한 계약에 묶으면 훅 하나가 메모리 쪽 APPROVE 를 막는다

## 리서치 소스

`.harness/.meta/research-memory-integration-2026-08-14.md` — 외부 근거 수집 완료.
출처 유형은 **WebSearch fallback** (Codex 사용량 한도 · 리셋 8/20 · 실패 출력 확인 후 사용자 승인).

핵심 인용:

- 선별적 추가·삭제가 장기 성능을 10% 개선 (서베이 인용값 · 원 논문 미확인 → **[미확인]**)
- SSGM 은 승격 전 **Write Validation Gate**(모순 검사)를 두고, 충돌 해소는 **미해결 문제로 명시**
- Generative Agents 는 relevance + recency + importance 를 **동일 가중 수기 튜닝**, ablation 에서
  세 축 각각이 critical. 단 이 프로젝트는 recency 근거가 부족해 2 축으로 간다
- 에이전트 자신의 산출물이 메모리로 write-back 되면 **자기검증 피드백 루프**가 된다
- **TTL 이 폭발 반경을 제한**한다 — 없으면 단 한 번의 주입이 무기한 영향

## GAP 분석

| 갭 | 실측 | 이번 스프린트 |
| --- | --- | --- |
| 데이터 풀에 메모리 없음 | `grep -c memory` → 0 | 해소 (§0.5 신설) |
| grounding 축 없음 | 104 건 중 보유 **0 건** | 해소 (자동 태깅 + 검수) |
| 쓰기 경로 없음 | 카이젠 교훈이 계약 본문·감사 로그에만 남음 | 후보 산출까지 (승격은 reflect-promote) |
| 모순 검사 없음 | Write Validation Gate 부재 | **이번 범위 밖** — 다음 사이클 |
| 무조건 TTL 없음 | demotion 이 조건부(재발 0 + low risk) | **이번 범위 밖** — 다음 사이클 |

## 범위 경계

- 이 스프린트는 **읽기(§0.5) + grounding 축 + 후보 산출**까지다. 실제 승격은
  `reflect-promote` 소관이며 이 스프린트가 재구현하지 않는다.
- 훅 2 종은 분리. 이미 착수·검증 완료된 1 종(`enforce-foreground-research.sh` 사용자 승인
  센티넬 게이트)은 이 계약의 대상이 아니다.
- 메모리 파일은 `~/.claude/projects/` 하위라 **레포 git diff 밖**이다. AR-01 의 diff scope 로는
  잡히지 않으므로 SK-03 이 별도로 측정한다.
- 스프린트 base = `main`. 레포 측 측정은 **구현 커밋 기준**이다 — `main..HEAD` 는 직전 카이젠
  사이클 변경분(`collect-kaizen-data.py` 포함 6 파일)을 이미 담고 있어 그대로 쓰면 오염된다.

### 측정 공통 전제 — 자기 산출물 제외 (모든 조건에 적용)

**레포 전체를 스캔하는 모든 조건은 이 스프린트 자신의 산출물을 검색 대상에서 제외한다:**

1. 이 계약 파일과 그 QA 피드백 · amendment 사이드카 — `.harness/sprint-*-kaizen-memory-integration.md`
2. 이 스프린트의 리서치·감사 기록 — `.harness/.meta/research-memory-integration-*.md` ·
   `.harness/.meta/memory-grounding-audit-*.md`
3. **생성물** — `.harness/.meta/kaizen-data-pool.md` (스크립트 산출물이며 소스가 아니다) ·
   `__pycache__/` 하위 `.pyc` (소스의 컴파일 사본이며 별도 정의가 아니다)

**근거.** 계약과 리서치 문서는 규약을 **설명하기 위해** 그 용어를 인용한다. 그 인용이 다시
"중복 정의" 로 잡히면, 규약을 문서화할수록 위반이 늘어난다. 직전 사이클 Final 계약이 같은 구조로
iteration 3→4 를 소모했다 (피드백 파일이 위반을 인용해 다음 라운드의 위반 근거가 됨).

이 선언은 **헤더 레벨 1 회**다. 개별 조건에 카브아웃을 반복하지 않는다 — 조건마다 붙이면
반드시 하나를 빠뜨린다 (Final v2 가 `ER-02`·`DG-02` 에만 넣고 `ER-01` 에 빠뜨린 사례).

## 회귀 게이트

`python3 scripts/validate-plugin.py` exit 0 · `python3 scripts/collect-kaizen-data.py` exit 0 ·
생성된 데이터 풀에서 기존 §0~§6 헤더가 전부 보존.

## Script

- [ ] SC-01: 메모리 수집이 전 프로젝트를 순회하고 `feedback` 타입만 모은다 [exact]
      (측정: `python3 scripts/collect-kaizen-data.py` 실행 후 생성된
       `.harness/.meta/kaizen-data-pool.md` §0.5 의 집계 줄이 보고하는 **프로젝트 수**와
       **엔트리 수**가, 아래 독립 계산과 일치 —
       `find ~/.claude/projects -maxdepth 3 -path '*/memory/*.md' ! -name 'MEMORY.md'` 로
       열거해 `grep -q '^  type: feedback'` 인 파일만 센 값. 계약 작성 시점 실측 baseline 은
       **6 프로젝트 · 104 엔트리**이나 값은 변할 수 있으므로 **재실행 시점 계산값과 대조**한다.
       주의: `memory/` 디렉토리는 9 개지만 `feedback` 엔트리를 **가진** 프로젝트는 6 개다 —
       디렉토리 수를 프로젝트 수로 세지 마라)
- [ ] SC-02: §0.5 가 §0 과 §1 사이에 렌더된다 [exact]
      (측정: `grep -n '^## ' .harness/.meta/kaizen-data-pool.md` 출력에서 헤더 번호가
       `0` → `0.5` → `1` → `2` … 순서. §0.5 가 §1 뒤에 오면 FAIL)
- [ ] SC-03: 선별이 관련성·중요도 2 축이며 recency 를 쓰지 않는다 [exact]
      (측정: `scripts/collect-kaizen-data.py` 에서 메모리 선별·정렬 코드가
       `modified` · `mtime` · `st_mtime` · `getmtime` 중 어느 것도 참조하지 않는다 —
       `grep -nE 'modified|mtime|getmtime'` 결과 중 **메모리 선별 함수 안에 있는 것 0 건**.
       다른 섹션(§1 등)의 기존 사용은 대상이 아니다)
- [ ] SC-04: 선별 탈락분의 제목이 §0.5 말미에 남는다 [structural]
      (측정: §0.5 에 주입 N 건의 본문과, 탈락 M 건의 **제목 목록**이 함께 존재.
       `N + M` 이 SC-01 의 총 엔트리 수와 일치)

## Skill

- [ ] SK-01: 오케스트레이터가 §0.5 를 Phase 참조 대상으로 명시한다 [exact]
      (측정: `grep -c 'memory' .claude/skills/kaizen-orchestrator/SKILL.md` >= 1.
       계약 작성 시점 실측 **0**. 단순 등장이 아니라 Step 0 수집 소스 목록 또는
       Phase 참조 조문에 있어야 한다 — Read 로 맥락 확인)
- [ ] SK-02: grounding 4 값의 **의미 정의**가 정확히 1 파일에만 존재한다 [exact]
      (측정: `grep -rl 'user_correction' --exclude-dir=.git .` 로 후보를 열거한 뒤
       §범위 경계 「측정 공통 전제」의 제외 대상을 뺀다. 남은 각 파일을 Read 해
       **값의 의미를 서술하는지(정의)** / **값 목록을 참조만 하는지(인용)** 를 구분 — **정의 1 건**.
       인용은 재정의가 아니다 (직전 사이클 Final 계약 RE-01 과 같은 취급).
       `scripts/collect-kaizen-data.py` 는 ER-02 가 요구하는 4 값 검증을 하려면 목록을 알아야
       하므로, 의미 서술 없이 값만 참조하면 위반이 아니다)
- [ ] SK-03: `feedback` 타입 메모리 전건이 `grounding` 을 보유한다 [exact, enumerated]
      (측정: SC-01 과 같은 방식으로 feedback 파일을 열거하고
       `grep -L 'grounding:'` 로 미보유를 센다 — **0 건**.
       대상은 `~/.claude/projects/*/memory/` 전 프로젝트. 레포 diff 밖이므로 이 조건이 단독 측정한다)
- [ ] SK-04: 자동 태깅 정확도가 샘플 검수로 측정되고 수치로 기록된다 [structural]
      (측정: 산출물에 **검수 대상 건수 · 자동값과 사람 판정이 일치한 건수 · 불일치 건의
       사유**가 각각 숫자와 함께 존재. "대체로 정확" 같은 서술은 FAIL.
       기록 경로: `.harness/.meta/memory-grounding-audit-2026-08-14.md`)

## Architecture

- [ ] AR-01: 레포 변경 경로가 열거 집합과 정확히 일치한다 [exact, enumerated]
      (Given: 구현 커밋 완료 후. 측정:
       `git diff --name-only <impl>^ <impl> -- ':(exclude).harness/*'` 결과가
       {`scripts/collect-kaizen-data.py`, `.claude/skills/kaizen-orchestrator/SKILL.md`,
       `reflect-kit/skills/reflect-digest/SKILL.md`, `reflect-kit/skills/reflect-promote/SKILL.md`}
       와 **정확히 일치**. `.harness/` 산출물은 제외 — 계약·피드백·감사 기록이 들어간다.
       `main..HEAD` 를 쓰지 마라 — 직전 사이클 변경분 6 파일이 섞인다)
- [ ] AR-02: 카이젠이 승격 ledger 에 직접 쓰지 않는다 [exact]
      (Given: 이번 스프린트가 **추가한 줄**만 대상이다 — 파일 전체가 아니다.
       `reflect-promote` 는 ledger **소유자**라 자기 쓰기 조문을 원래 갖고 있고(main 기준 3 건),
       그것을 위반으로 세면 소유자를 고칠 때마다 FAIL 이 난다.
       측정: 이번 변경 4 파일 각각에 대해
       `git diff -U0 -- <file> | grep '^+' | grep -E "promotions-ledger.*(write_text|append|>>|open\(.*['\"]a)"`
       → 전부 **0 건**. 읽기·경로 언급·금지 조문은 위반이 아니다)
- [ ] AR-03: grounding 을 읽는 소비면이 조건화된다 [structural, enumerated]
      (측정: `reflect-kit/skills/reflect-digest/SKILL.md` 와
       `reflect-kit/skills/reflect-promote/SKILL.md` **2 파일 각각**이
       (a) `grounding` 필드의 존재와 (b) `self_inference` 를 승격/PASS 근거로 쓰지 않는다는
       취급을 명시. 두 파일 중 하나라도 빠지면 FAIL)

## Error

- [ ] ER-01: 메모리가 0 개이거나 디렉토리가 비어도 수집이 비정상 종료하지 않는다 [exact]
      (측정: 빈 임시 HOME 으로 `HOME=$(mktemp -d) python3 scripts/collect-kaizen-data.py` 실행 →
       exit 0 이고 §0.5 에 `(없음)` 표기. zsh·bash 양쪽에서 동일)
- [ ] ER-02: `grounding` 값이 4 값 밖이면 집계에서 제외하고 건수를 보고한다 [exact]
      (측정: 임시 HOME 에 `grounding: bogus` fixture 1 건을 넣고 실행 →
       §0.5 에 제외 건수 **1** 이 숫자로 표기. 조용히 삼키면 FAIL)

## Anti-patterns

- [ ] AP-03: 이번 변경이 bare code fence 를 새로 도입하지 않는다
      (측정: `python3 scripts/validate-plugin.py` 의 V6 가 `0 bare`)
- [ ] AP-04: 수정한 SKILL.md 의 frontmatter `name` 필드가 보존된다
      (측정: 같은 실행의 V1 이 OK)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private 으로 만들지 않았다
- [ ] RE-02: reflect-kit 의 승격·ledger 를 재구현하지 않고 재사용한다
      (측정: 이번 변경 파일에 승격 판정 로직(precedence table · rule_id 발급 · status 전환)의
       **복제 0 건**. reflect-promote 를 참조·호출하는 형태여야 한다)

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0 개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0 개 (제외 목록 없음)
- [ ] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 로그에 에러/예외 0 개
- [ ] DG-04: 실제 구동 — `python3 scripts/collect-kaizen-data.py` 실행 시 에러 0 개
