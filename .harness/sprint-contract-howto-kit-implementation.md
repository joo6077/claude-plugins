---
feature: "howto-kit 플러그인 구현"
slug: howto-kit-implementation
created: "2026-09-08 10:30"
complexity: "복잡"
conditions: 29
status: active
owner_session: 0e3335f2-8d08-4e29-8a5d-01ec6b7ed620
conditions_digest: sha256:5de60ce9548db9c6
locked_at: "2026-09-08 11:40"
---

## 배경

`docs/howto/design-brief.md` §10 의 C1~C14 를 계약으로 옮긴 것이다. 브리프가 설계 정본이며
이 계약은 그 조건표를 이 레포의 카테고리(Skill/Script/Error/Architecture)로 재배치한 것이다.

**공통 전제 (헤더 1 회 선언 — 개별 조건에서 반복하지 않는다)**

- 산출물은 `howto-kit/` 신규 플러그인이다. 기존 `onboarding-kit` 은 **건드리지 않는다**.
- 모든 문서는 한국어로 쓴다.
- 킷 검증 명령은 `python3 scripts/validate-plugin.py howto-kit` 이다.
- 게이트 셸 스니펫은 **zsh 와 bash 양쪽에서 실제 실행**한 출력으로만 판정한다. 서술 존재는 증거가 아니다.
- 조건에 등장하는 `게이트` 는 브리프 §6 의 G1~G6 을 가리킨다.
- 판정 임계(`[미검증]` 마커 등)는 `harness/docs/guides/qa-evaluation-guide.md` 가 정본이며
  이 킷에서 재정의하지 않는다.

## 리서치 소스

- `docs/howto/design-brief.md` — 설계 정본 416 줄 (원칙 P1~P8 · Step Contract · 출처 등급제 · G1~G6)
- `docs/howto/drafts/SKILL.md` — `/howto` 초안 255 줄
- `onboarding-kit/skills/setup-guide/SKILL.md:53-106` — `guide_gate()` G1~G4 원형
- `harness/docs/guides/skill-design-guide.md` · `agent-design-guide.md` — 아키타입·도구 스코핑
- `harness/docs/guides/plugin-validation-guide.md` — V1~V8 검증 카테고리

## GAP 분석

브리프 §11 이 남긴 미확인 8 건 중 이번 스프린트에서 **사실로 말하면 안 되는 것**은 4 건이다:
체크리스트 방법론 1 차 출처(§11-1) · Microsoft Learn 권한 인용 2 건(§11-5) · RSS 피드 실측(§11-6) ·
이름 충돌 검사(§11-7). ER-01 이 이것을 조건화한다.

브리프에 없던 소비면 2 건을 Pre-Edit Audit 에서 발견했다 — `scripts/sync-orchestrator.py` 의
`infer_research_docs_dir` 하드코딩 dict, `scripts/check-external-links.py` 의 `KIT_DIRS` 하드코딩.
둘 다 새 킷을 자동 발견하지 않으므로 SC-05 · SC-06 으로 별도 조건화한다.

## 범위 경계

- **비범위**: `onboarding-kit` 개명·삭제 · 기존 `docs/onboarding-kit/` 산출물 수정 ·
  실제 절차 문서(가이드) 생산 · onboarding-kit 의 기존 결함 3 건 수정(별건 처리).
- 브리프 C14(qa-evaluator APPROVE)는 조건으로 넣지 않는다 — 평가 행위 자체를 평가 대상으로
  삼으면 순환이다. 이 계약 전체의 판정 결과가 곧 C14 다.
- 동시 세션 충돌: 다른 세션이 이 브랜치에 `97cde49` (bambu 핸드오프)를 커밋했다. 이번 스프린트
  산출물이 아니므로 AR-07 의 diff-scope 오라클에서 제외 pathspec 으로 뺀다.
- 커버리지 해소: SC-01 — 산문의 "G1~G6" 과 측정의 `grep -c 'G[1-6]_'` 는 같은 6 개를 가리키며,
  측정 절이 각 게이트 ID 를 개별 문자열로 열거한다.

## 회귀 게이트

marketplace.json 등록 순간 `validate-plugin.py`(인자 없이) 와 `sync-docs.py`(인자 없이)의
전수 실행 대상에 `howto-kit` 이 편입된다. 두 명령의 **전체 실행**이 새 킷 때문에 새로 FAIL 하지
않아야 한다 (SC-03 · SC-04).

## Skill

- [ ] SK-01: `howto-kit/skills/` 아래에 `howto/SKILL.md`, `howto-doc/SKILL.md`, `howto-audit/SKILL.md`
      3 개가 존재하고 각 frontmatter 에 `name`·`description`·`user-invocable` 이 빈 값 아닌 상태로
      있다 [exact, enumerated]
      (측정: `python3 scripts/validate-plugin.py howto-kit --check=frontmatter` 가 V1 OK 이고
      출력에 `3 skills` 가 포함된다)
- [ ] SK-02: `howto-kit/agents/howto-reviewer.md` 가 존재하고 frontmatter 에 `name`·`description`·
      `tools`·`model` 4 필드가 모두 있으며, `tools` 값에 `Write`·`Edit`·`NotebookEdit` 중 어느
      것도 없다 [exact, enumerated]
      (측정: `grep -n '^tools:' howto-kit/agents/howto-reviewer.md` 출력에 세 토큰 부재 확인 +
      V1 이 `1 agent` 를 OK 로 보고)
- [ ] SK-03: `howto/SKILL.md` 와 `howto-audit/SKILL.md` 의 `allowed-tools` 에 `Write`·`Edit` 가
      없고, `howto-doc/SKILL.md` 의 `allowed-tools` 에는 `Write` 가 있다 [exact, enumerated]
      (측정: 3 파일 각각 `grep -n '^allowed-tools:'` 출력 3 줄을 보고에 인용)
- [ ] SK-04: `howto-kit/evals/evals.json` 이 유효 JSON 이고 케이스 수가 6 건 이상이며, 그중
      **입도 케이스가 2 건 이상**이다. 입도 케이스란 assertion 이 (a) 종결 동사 미충족 탐지
      (b) `확인`/`verify` 필드 부재 탐지 (c) `안 보이면`/분기 부재 탐지 중 하나 이상을 요구하는
      케이스를 말한다 [structural, collective]
      (측정: `python3 -c` 로 `json.load` 후 `len(cases)` 출력, 입도 케이스는 케이스 id 를 열거해
      보고에 적는다)
- [ ] SK-05: `howto-kit` 내 3 스킬 + 1 에이전트 description 의 트리거 키워드가 (a) 상호
      set intersection 공집합이고 (b) 어느 키워드도 다른 키워드의 부분문자열이 아니다
      [exact, enumerated]
      (측정: `find howto-kit/skills -mindepth 2 -maxdepth 2 -type f -name 'SKILL.md' -exec grep -Hn '^description:' {} +`
      와 `find howto-kit/agents -maxdepth 1 -type f -name '*.md' -exec grep -Hn '^description:' {} +`
      실행 후 python 으로 set intersection + substring pair 0 건 확인)

## Script

- [ ] SC-01: G1·G2·G3·G4·G5·G6 6 개 게이트가 하나의 셸 함수로 구현되어 있고, **정상 입력 1 건**에
      대해 zsh 와 bash **양쪽에서 실행**했을 때 6 개 게이트 판정 줄(`G1_`·`G2_`·`G3_`·`G4_`·`G5_`·`G6_`
      로 시작)과 최종 판정 줄이 나오며 두 셸 출력이 동일하다 [exact, enumerated]
      (측정: `zsh -c '. <게이트파일>; howto_gate <정상샘플>'` 과 `bash -c '...'` 두 출력 전문을
      보고에 붙이고 `diff <(zsh…) <(bash…)` 가 빈 출력임을 확인)
      음성 대조: 게이트 함수 본문에서 G5 판정 블록을 삭제하면 `G5_` 줄이 사라져 이 측정이 FAIL 한다.
- [ ] SC-02: G5(말단 액션)와 G6(입도) 각각에 대해 **일부러 위반한 양성 케이스 입력 1 건씩**이
      준비되어 있고, 그 입력에서 해당 게이트가 `FAIL` 을 출력하며 최종 판정이 `GATE_FAIL` 이다.
      zsh·bash 양쪽에서 실행한다 [exact, enumerated]
      (측정: G5 양성 케이스 파일과 G6 양성 케이스 파일 2 개 경로를 보고에 적고, 각각 zsh·bash 로
      실행한 출력 4 벌 전문을 붙인다. `G5_TERMINAL FAIL` / `G6_GRANULARITY FAIL` 문자열이 실제로
      나와야 한다)
      음성 대조: 양성 케이스에서 위반 문장을 정상 문장으로 바꾸면 그 게이트가 PASS 로 뒤집힌다 —
      즉 이 측정은 게이트 로직을 직접 호출한다.
- [ ] SC-03: `python3 scripts/sync-docs.py howto-kit` 실행이 exit 0 이고, 그 후
      `python3 scripts/sync-docs.py --check-only` 가 exit 0 (전 킷 동기화 상태)이다
      [goal]
      (측정: 두 명령의 exit code 와 마지막 출력 줄을 보고에 인용)
- [ ] SC-04: `python3 scripts/validate-plugin.py howto-kit` 의 8 카테고리(V1~V8) 중 FAIL 이 0 건이고,
      `python3 scripts/validate-plugin.py`(전 킷) 실행에서 `howto-kit` 이 원인인 새 FAIL 이 0 건이다
      [goal]
      (측정: 두 명령 출력 전문을 보고에 붙인다. WARN 은 허용하되 건별로 사유를 적는다)
- [ ] SC-05: `scripts/sync-orchestrator.py` 의 `infer_research_docs_dir` 매핑에 `"howto-kit"` 항목이
      추가되어 있고, `python3 scripts/sync-orchestrator.py` 실행 후
      `.claude/skills/kaizen-orchestrator/SKILL.md` 의 `AUTO:plugin_phases` 블록에 `howto-kaizen`
      Phase 가 나타난다 [exact, enumerated]
      (측정: `grep -n 'howto-kit' scripts/sync-orchestrator.py` 와
      `grep -n 'howto-kaizen' .claude/skills/kaizen-orchestrator/SKILL.md` 두 출력을 보고에 인용.
      마커 블록 바깥 수동 편집 금지)
- [ ] SC-06: `scripts/check-external-links.py` 의 `KIT_DIRS` 리스트에 `"howto-kit"` 이 포함되어 있다
      [exact, enumerated]
      (측정: `grep -n 'howto-kit' scripts/check-external-links.py`)

## Error

- [ ] ER-01: 브리프 §11 의 미확인 4 건(체크리스트 방법론 1 차 출처 · Microsoft Learn 권한 인용
      2 건 · RSS 피드 URL · 이름 충돌 검사)에 대해, 킷 산출물이 **확인 없이 사실로 단정하지 않는다**.
      각 건은 (a) 이번 스프린트에서 재조회하여 1 차 출처 URL 을 근거로 확정했거나, (b) 킷 파일 안에
      `[추정]` 또는 `[미확인]` 등급 표기와 함께 남아 있다 [exact, enumerated]
      (측정: 4 건 각각에 대해 처리 방식(a/b)과 근거 위치 `파일:라인` 을 표로 보고. b 인 건은
      해당 라인에 등급 마커가 실제로 있는지 `grep -n` 으로 확인)
- [ ] ER-02: 게이트 함수가 (a) 존재하지 않는 파일 경로를 받으면 `GATE_BLOCKED` 를 출력하고 exit
      상태를 0 으로 유지하며 (b) 빈 파일을 받아도 셸이 죽지 않고 6 개 게이트 줄을 출력한다.
      zsh·bash 양쪽에서 확인한다 [exact, enumerated]
      (측정: `howto_gate /nonexistent/x.md` 와 `howto_gate <빈파일>` 을 zsh·bash 로 각각 실행한
      출력 4 벌을 보고에 인용)
      음성 대조: `[ -f "$g" ]` 가드를 제거하면 (a) 가 빈 출력 또는 grep 에러로 바뀌어 FAIL 한다.
- [ ] ER-03: 게이트 G6 의 `추정` 비율 판정이 **0 으로 나누기 없이** 동작한다 — 액션 스텝이 0 건인
      입력에서도 셸 에러 없이 판정 줄을 출력한다 [structural, collective]
      (측정: 액션 스텝 0 건 샘플을 zsh·bash 로 실행한 출력 2 벌. `divide by zero` 류 문자열 0 건)

## Architecture

- [ ] AR-01: `howto-kit/.claude-plugin/plugin.json` 이 존재하고 `json.load` 로 파싱되며
      `name`·`version`·`description` 3 필드가 빈 값이 아니다. `name` 값은 `howto-kit` 이다
      [exact, enumerated]
      (측정: `python3 -c "import json;d=json.load(open('howto-kit/.claude-plugin/plugin.json'));print(d['name'],d['version'],len(d['description']))"`)
- [ ] AR-02: Step Contract 스키마의 **필드 정의가 `howto-kit/references/step-contract.md` 한 곳에만**
      존재한다. 다른 킷 파일은 그 파일을 참조만 하고 필드 목록을 재서술하지 않는다
      [structural, collective]
      (측정: `grep -rn 'if_not_found\|target_label\|source.tier' howto-kit/` 실행 결과에서
      **필드 정의 형태**(YAML 키 나열 또는 필드 표)로 등장하는 파일이 `references/step-contract.md`
      1 개뿐임을 확인. 산문 인용·예시 렌더링은 재서술이 아니다)
- [ ] AR-03: `.claude-plugin/marketplace.json` 의 `plugins` 배열에 `name: "howto-kit"`,
      `source: "./howto-kit"` 엔트리가 있고 `description` 이 `[vX.Y.Z · YYYY-MM-DD]` 형식 태그로
      시작하며 그 버전이 `howto-kit/.claude-plugin/plugin.json` 의 `version` 과 같다
      [exact, enumerated]
      (측정: `python3 scripts/validate-plugin.py howto-kit --check=plugin-json` 이 V7 OK)
- [ ] AR-04: 루트 `CLAUDE.md` 의 (a) Repository Overview 목록과 (b) Skills Reference 표에
      `howto-kit` 항목이 있고, (b) 에 `/howto`·`/howto-doc`·`/howto-audit`·`howto-reviewer` 4 개가
      모두 열거된다 [exact, enumerated]
      (측정: `grep -n 'howto' CLAUDE.md` 출력에서 4 개 이름 각각의 등장 라인을 보고에 적는다)
- [ ] AR-05: `docs/howto-kit/` 아래 HTML 페이지가 1 개 이상 존재하고, `docs/index.html` 의 섹션
      배열에 그 파일이 `file: 'howto-kit/<name>.html'` 형태로 등록되어 있으며, 등록된 모든
      `howto-kit/*.html` 경로가 실재한다 [exact, enumerated]
      (측정: `grep -n "howto-kit/" docs/index.html` 로 등록 목록을 뽑고, 각 경로에 대해
      `test -f docs/<경로>` 를 돌려 부재 0 건 확인)
- [ ] AR-06: `.claude/skills/howto-kaizen/SKILL.md` 와 `.claude/skills/howto-research/SKILL.md` 가
      존재하고 각 frontmatter 에 `name`·`description` 이 있다 [exact, enumerated]
      (측정: 두 파일 각각 `head -6` 출력을 보고에 인용)
- [ ] AR-07: 이번 스프린트의 커밋 변경 경로가 아래 허용 목록 안에만 있다 [exact, enumerated]
      Given: 구현 커밋 완료 후 (`git add` 만 한 상태가 아니라 커밋된 상태)
      허용: `howto-kit/` · `.claude/skills/howto-kaizen/` · `.claude/skills/howto-research/` ·
      `.claude-plugin/marketplace.json` · `CLAUDE.md` · `README.md` · `docs/howto/` ·
      `docs/howto-kit/` · `docs/index.html` · `scripts/sync-orchestrator.py` ·
      `scripts/check-external-links.py` · `.claude/skills/kaizen-orchestrator/SKILL.md` ·
      `.harness/sprint-contract-howto-kit-implementation.md` ·
      `.harness/sprint-feedback-howto-kit-implementation.md`
      (측정: `git diff --name-only 4fb1382..HEAD -- . ':(exclude).harness/handoff/*' ':(exclude)docs/bambu-calibration/*'`
      의 각 줄이 허용 목록 접두 중 하나에 매치. 매치 안 되는 줄 0 건이면 PASS.
      제외 pathspec 은 동시 세션 커밋 `97cde49` 산출물이다)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수
      (측정: `python3 scripts/validate-plugin.py howto-kit --check=code-fence` 가 V6 OK)
- [ ] AP-04: `SKILL.md` / `agents/*.md` frontmatter 에서 `name` 필드 누락 없음
      (측정: `python3 scripts/validate-plugin.py howto-kit --check=frontmatter` 가 V1 OK)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (제외 목록 없음)
- [ ] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개 — N/A (이 킷은 실행 가능한 앱/서버가 아니라 스킬
      정의 파일 모음이다. 대신 게이트 함수 실행(SC-01·SC-02·ER-02)이 런타임 검증을 대신한다)
