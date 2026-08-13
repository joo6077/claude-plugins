---
name: sprint-contract
description: >
  기능 구현 전 완료 조건을 정의하고 사용자 합의를 받는다.
  QA Evaluator가 평가할 기준이 되는 Sprint Contract를 생성한다.
  "기능 만들어줘", "화면 추가", "구현해줘", "개발해줘" 같은
  구현 요청에서 /develop보다 먼저 트리거된다.
  단순 수정(색상 변경, 오타 수정, 1파일 변경)에는 트리거하지 않는다.
argument-hint: "<feature or description>"
user-invocable: true
---

# Sprint Contract

구현 전에 "무엇이 완료인가"를 정의한다.
QA Evaluator가 이 계약을 기준으로 구현을 APPROVE/REJECT한다.

## 이 스킬 폴더의 파일

필요할 때 읽어라:

- `references/red-flags.md` — Red Flags + Rationalization Table (계약 품질 검증용)

## References

- `../../docs/guides/contract-design-guide.md` — 계약 작성 원칙 가이드
- `harness/references/contract-schema.md` — 계약 포맷 공유 정의. **경로·슬러그·frontmatter 규약의
  단일 정의처(SSOT)** 다. 이 스킬은 그 규약을 인용해 적용만 하고 여기서 재정의하지 않는다.
  서술이 어긋나면 `contract-schema.md` 가 이긴다
- `harness/references/feedback-schema.yaml` — 피드백 YAML 스키마

## Gotchas

- verify-feedback.sh가 PASS를 반환하지 않으면 절대 완료를 선언하지 마라. 이것은 선택이 아니다.
- 복잡도 판단에서 "단순"으로 과소평가하는 경향이 있다. **Process Step 1 의 4 축 표를 채우기 전에는 복잡도를 말하지 마라** — 파일 수는 판정 근거가 아니다 (E2 승급, `complexity-by-file-count` 재발)
- `project.yaml`의 값은 **리터럴 그대로** 쓴다. 카테고리를 하드코딩(UI/Logic/Error)하지 않는 것은 물론, `commands.analyze` 가 `fvm.bat flutter analyze` 면 계약에도 `fvm.bat flutter analyze` 라고 적어라. **Process Step 1.2 대조표를 출력하기 전에 DRAFT 를 제시하지 마라** (E2 승급, `config-command-mismatch` 재발)
- 조건을 "~가 잘 동작한다", "~를 적절히 처리한다"로 쓰면 QA Evaluator가 판정 불가능하다. 반드시 PASS/FAIL 이진 판정 가능한 문장으로 써라
- 안티패턴을 0개로 두면 안 된다. `project.yaml`에 정의된 패턴 중 해당 기능에서 위반 가능성이 높은 것을 최소 2개 선별해라
- 사용자가 "계약 필요없어"라고 해도 **생략할 수 없다**. 간소화된 계약(단순 복잡도, 최소 조건)을 제안해라
- 조건을 "구현 완료 후 1회 검증"만으로 작성하지 마라. 가능하면 **다단계 검증 시점**(코드 생성 중 → 커밋 전 → 최종 QA)을 조건에 반영해라. 단일 시점 검증은 중간 단계의 품질 저하를 놓친다
- 조건에 클래스명, 메서드명, DB 테이블명, API 경로 등 **구현 상세**를 쓰지 마라. 조건은 외부에서 관찰 가능한 행동만 기술한다. "UserService가 호출된다" ✗ → "사용자 등록이 완료된다" ✓. 이를 **구현 누수(implementation leakage)**라 하며, 구현이 바뀌면 조건도 깨진다
- 복잡도가 "중간" 이상이면 핵심 조건에 **Given-When-Then 구조를 필수** 적용해라. 반구조화된 조건이 자연어보다 해석 모호성을 줄인다
- 비기능 요구사항(성능, 보안, 접근성)을 무시하지 마라. 해당 기능에 관련된 NFR이 있으면 최소 1개 조건을 포함해라
- 조건 작성 시 **구체성 태그** 를 명시하라. 조건 끝에 `[exact]` (이름/값 일치), `[structural]` (섹션/필드 존재), `[goal]` (목표 달성, 수단 무관) 중 하나를 붙여라. 미명시 시 `[structural]` 로 간주되며, 구현이 목표를 달성했더라도 이름이 달라 REJECT 될 수 있다. **주의**: 숫자 레벨 (L-one, L-two, L-three) 은 QA 평가 깊이 전용 (skill-design-guide §5.5) 이므로 계약 태그에 재사용 금지 — 반드시 문자 태그만 사용
- 다수 대상 (파일/모듈/키워드) 조건 작성 시 **aggregation mode** 를 태그에 함께 명시하라. `[exact, enumerated]` 은 각 대상을 개별 이름으로 명시해야 PASS, `[structural, collective]` 은 포괄 경로/패턴 하나로도 PASS. 모드 미명시 시 기본값은 `collective`. (KZ-04 REJECT 패턴 방지)
- 특정 파일·타입에 조건이 적용되지 않는 경우 **예외 조항을 조건 내부에 인라인으로 명시하라**. `예외: (a) integration.html — Final 통합 페이지로 제외` 형태. 구두 합의나 별도 메모는 QA 시점에 반영되지 않는다
- 조건에 한국어 + 영어가 혼용되는 키워드 (예: "Layout shift" vs "레이아웃 shift") 가 있으면 **병기하거나 한쪽으로 통일 선언** 하라. 표현 변형은 키워드 매칭·의미 해석을 엇갈리게 만든다
- 경계값 조건 (`>= N`, `<= N`, `== N`) 작성 시 **측정 대상 + 측정 방법(명령어/도구)**을 인라인으로 명시하라. "1500줄 이상이다" 만으로는 wc -l / grep -c / 에디터 줄 수 중 무엇인지 불명확하여 근소한 차이에서 판정이 엇갈린다
- 포맷 일관성을 요구하는 조건은 **적용 수준(file-level / section-level / field-level)**을 명시하라. "일관된 포맷" 단독 사용 금지. 핵심 필드(컬럼명 등)까지 열거하면 가장 정확하다
- **범위어 (주요 / 모든 / 대부분 / 핵심) 가 등장하는 조건은 반드시 인라인 enumerate 하라.** "주요 interactive element" ✗ → "버튼·카드·입력 (badge/decoration 제외)" ✓. contract-design-guide §스코프 범위 인라인 명시 참조 (SK-02 재발 방지)
- **검증 수단이 없는 조건은 작성하지 마라.** 조건마다 "어떤 명령/도구/관찰로 PASS/FAIL 판정하는지" 를 인라인으로 적어라 (예: "측정: `wc -l`", "측정: MCP Figma read-back"). 외부 도구 의존 시 3 단계 fallback 을 명시 — 기본 / fallback / `[미검증]` 수용 임계 (1 건까지)
- **sibling 스킬 공통 원칙은 반드시 `[exact, enumerated]` 또는 `[structural, enumerated]` aggregation mode 로 작성하라.** 대상 스킬을 숫자로 명시 + 이름 전부 열거. "rust-api 에 적용" ✗ → "rust-init, rust-feature, rust-service, rust-api 4 스킬 모두에 적용" ✓ (rust-kit H-01/H-03 재발 방지)
- **조건의 FAIL 상태를 1 문장으로 기술 가능해야 한다.** FAIL 이미지가 떠오르지 않으면 그 조건은 모호하므로 재작성하라. 이는 Binary Decidability Pre-Check 사전 점검이다 (contract-design-guide §계약 작성자 의무 참조)
- **Pre-Edit Audit 은 Gotcha 가 아니라 Process Step 1.4 다.** `project.yaml` 만 읽고 "Pre-Edit 감사 결과" 를 제시하는 것은 감사가 아니다 — 대상 파일을 실제로 Read 하고 `파일:라인` 증거를 표에 남겨라. 증거 열이 빈 행은 감사되지 않은 것이다 (E2 승급, `skipped-pre-edit-audit` 재발)
- **측정 명령을 적은 뒤 그 명령이 조건 의도를 실제로 측정하는지 + 어떤 상태 전제에서 실행되는지 확인하라.** 측정 명령이 곧 test oracle 이므로, oracle 이 의도와 어긋나면 측정 방법을 명시하고도 false REJECT 가 난다. (a) **의미 일치**: `test ! -f` 는 물리적 부재를, gitignore 의도는 추적 여부를 측정 — 다르다. 추적 여부는 `git ls-files --error-unmatch` 로 측정하라. (b) **상태 전제**: `git diff main...HEAD` 는 커밋 전 변경을 못 본다 — 커밋 완료 같은 전제가 있으면 조건에 `Given:` 또는 "(... 완료 후)" 로 인라인 명시하라. contract-design-guide §검증 수단 명시 의무 > "측정 명령 타당성 · 상태 전제" 참조 (LG-07/AR-01 재발 방지)
- **변경 범위(scope) 조건에 `git diff` 를 자유 서술로 적지 마라 — 표준형 4 요소를 다 채워라.** (1) `Given:` 상태 전제 (2) 경로 한정 pathspec (3) 생성물 제외 pathspec (`':(exclude)*.g.dart'` 등) (4) "정확히 일치" 인지 "포함" 인지. 그리고 **계약 작성 시점에 그 명령을 1 회 실행해 baseline 을 서술 섹션에 남겨라.** 미커밋 codegen 산출물이 diff 에 섞여 scope 조건이 깨진 것이 AR-01 재발 3 회의 직접 원인이다 (E3 승급). contract-design-guide §Diff-Scope Oracle 표준형 참조
- **계약 서두의 설계 의도와 조건이 어긋나면 구현자는 조용히 한쪽만 따른다.** DRAFT 제시 전에 서술↔조건 방향을 대조하고, 조건이 기존 식별자(함수·클래스·파일명)를 literal 로 열거한다면 **그 이름이 지금 코드에 존재하는지 grep 으로 확인**하라. 의미(단방향/양방향 등)까지 설계 의도와 맞는지 본다 (RE-02 재발 방지)
- **`[exact]` 조건에 테스트·문서 같은 부산출물을 적으면 그것도 이번 스프린트 제출 대상이다.** 낼 생각이 없으면 `[goal]` 로 낮추거나 산출물 문구를 빼라. 그대로 두면 REJECT 가 예정된 것이다 (UI-07 재발 방지)
- **승인 기록·합의 로그처럼 사람이 남겨야 생기는 증거에 의존하는 조건은 그 기록물의 경로를 조건에 적어라.** 경로를 적을 수 없으면 그 조건을 만들지 마라 — 평가 시점에 읽을 대상이 없으면 판정 불가다 (UI-06 재발 방지)
- **계약·직렬화·공유 모델을 바꾸는 스프린트에서 producer 조건만 쓰면 절반짜리 계약이다.** consumer 면(클라이언트·호출자·생성 코드) 파일을 grep 으로 찾아 **별도 조건**으로 `[exact, enumerated]` 열거하라. 이 원칙은 qa-evaluator 쪽에 대응 규칙이 없어서 **계약에 안 넣으면 아무도 안 잡는다** (insights Friction #4 — "당연히 그러면 클라까지 바꿔야지"). Process Step 2.5 참조
- **계약을 고정 파일명에 바로 쓰지 마라 — 슬러그 경로를 선점한 뒤에 써라.** 같은 프로젝트에서 세션을 병렬로 돌리면 나중 세션이 앞 세션의 계약을 통째로 덮어쓰고, 앞 세션의 qa-evaluator 가 남의 계약을 평가한다 (2026-07-27 카이젠에서 실제 발생). Process Step 0.5 의 선점 절차를 통과하기 전에는 계약 본문을 어떤 파일에도 쓰지 않는다
- **파일을 글로빙으로 열거하지 마라 — `find` 를 써라. 계약 파일만이 아니라 이 스킬이 실행하는 모든 셸 스니펫에 적용된다.** 사용자 셸이 zsh 면 기본 `nomatch` 라 **매치가 0 건인 glob 이 명령을 통째로 죽인다.** 두 형태가 모두 죽는다 — (a) 루프: `for f in "$D"/sprint-contract-*.md` 는 파일이 없을 때 루프에 진입조차 못 하며 `[ -f "$f" ] || continue` 가드는 무력하다, (b) **명령 인자**: `grep -n '^description:' <plugin>/agents/*.md 2>/dev/null` 은 `agents/` 가 없거나 비어 있는 킷(reflect-kit · bambu-kit · onboarding-kit)에서 출력이 0 건이 된다. **글로빙 확장은 명령 실행 전에 일어나므로 `2>/dev/null` 로는 못 막는다.** 실측: zsh `no matches found` + 명령 미실행, bash 는 정상 통과 — **bash 에서만 테스트하면 안 잡힌다.** 선례: `harness/skills/harness-kaizen/scripts/trigger-check.sh`, Step 1.5
- **frontmatter 식별자 필드는 따옴표 없이 쓰고, 읽을 때는 따옴표를 벗겨라.** writer 가 `owner_session: "abc"` 로 쓰는데 reader 가 안 벗기면 `$CLAUDE_CODE_SESSION_ID` 와 **절대 일치하지 않아** 소유 세션 판정(계약 선택 ladder 2 단계)이 영구 불성립한다. `slug` · `status` · `owner_session` 은 따옴표 없이 쓰고, 공백·콜론이 들어가는 `feature` 만 따옴표를 유지한다. reader 는 레거시 호환을 위해 양쪽 다 벗긴다 (Step 0.5 (c) `read_fm`)
- **frontmatter 를 `sed -n '/^---$/,/^---$/p'` 로 잘라내지 마라 — 범위가 닫는 `---` 뒤에 재점화되어 본문까지 읽는다.** 계약 본문에 `---` 로 감싼 frontmatter 예시가 실리고 진짜 frontmatter 에 그 키가 없으면(레거시 계약, 또는 `CLAUDE_CODE_SESSION_ID` 가 비어 `owner_session` 을 생략한 계약) **본문 값이 frontmatter 값으로 읽힌다.** 본문 예시의 `owner_session` 이 현재 세션 ID 와 같으면 Step 0.5 (c) 가 "내 세션의 재작성" 으로 분기해 **남의 active 계약을 history 로 옮긴다.** reader 측 `fm_get`(`harness/agents/qa-evaluator.md` Step 1-b)은 닫는 `---` 에서 멈추므로 **writer 만 오판하는 비대칭 사고**가 된다. `read_fm` 은 `fm_get` 과 동일한 awk 구현을 쓴다 — 이 레포처럼 frontmatter 규약 자체를 다루는 메타 계약에서 실제로 터진다
- **슬러그를 정규식 통과만으로 자동 채택하지 마라.** 한국어 feature 명은 조사·기호가 전부 `-` 로 치환되어 `3.16.0 마이그레이션 if 분기 정리` → `3-16-0-if` 같은 ASCII 파편이 남는데, 이게 **정규식은 통과해서** "사용자에게 물어라" 가드가 발동하지 않는다. 그렇게 만든 새 슬러그는 기존 `sprint-feedback-<slug>.md` 짝을 고아로 만들어 접미형 정식화의 목적 자체를 무너뜨린다. Step 0.5 (a) 의 `LOST`/`WORDS` 게이트를 거치고, **기존 슬러그 재사용을 `find` 로 먼저 탐색**하라
- **`conditions:` 값을 손으로 세지 마라 — 명령으로 계산해서 채워라.** 사람이 세면 Anti-patterns / Reusability / Diagnostics 섹션을 빼먹는다. 실제로 한 세션에서 3 회 연속 틀렸다 (18→22, 19→27, 22→25). Step 6.2 의 `grep -cE` 출력을 그대로 전사하고 Step 6.5 게이트에서 재확인한다
- **계약 저장은 Step 6.5 게이트 통과 전까지 끝난 게 아니다.** 헤더 목록과 조건 배치를 grep/awk 로 실제 검사하고 출력을 인용하라. 허용되지 않은 `## Notes` 같은 헤더를 추가하면 평가자 파서가 오작동한다 (E3 승급, `parser-incompatible-contract-section` 재발)
- **계약은 write-once 다 — 봉인 이후 조건 줄을 고치지 마라.** Step 6.6 이 조건 체크박스 줄만 정규화 해시해 `conditions_digest` 에 기록한다. **자신이 만든 산출물을 사후에 허용하려고 조건 문구를 넓히는 것**이 실측된 위반 형태다 (2026-08-11 REJECT: "생성자가 … 계약 AR-04 조건 문구를 직접 편집(5→7 경로)"). 직전 사이클이 사이드카를 도입했는데도 재발했으므로 **E1 서술 → E3 결정론적 봉인으로 승급**했다. `SEAL_BROKEN` 을 만나면 조용히 재봉인하지 말고 `recorded`/`actual` 을 보고하라 — 재봉인은 위반을 지우는 행위다. 조건을 바꿔야 하면 `sprint-amendments-<slug>.md` 사이드카에 쓴다
- **사이드카 amendment 의 direction 을 자기신고하지 마라 — 집합형은 계산하라.** 경로 화이트리스트·파일 열거·대상 목록은 원 집합과 개정 집합을 `comm` 으로 비교해 direction 을 산출한다. 3 경로 → 5 경로는 계산상 `relaxing` 이라 "범위 조정" 이라 부를 여지가 없다. **앵커가 없다고 `unknown` 으로 적지 마라** — direction 과 consent 는 별개 축이고, `narrowing · unanchored` 는 정상적으로 PASS 근거다. 앵커 부재를 이유로 방향까지 무효화한 것이 사이드카를 무력화해 본문 직접 편집을 유발한 구조다 (contract-schema §Amendment 사이드카)
- **테스트 통과를 요구하는 조건에는 `음성 대조:` 절을 넣어라.** 구현을 지워도 통과하는 측정문은 oracle 이 아니다 — 실측: "mutation test 로 확정, 동시성 가드를 완전히 삭제해도 이 테스트는 여전히 통과한다" (ER-02). 측정이 구현을 **직접** 호출하는지 확인하고, 어느 지점을 무력화하면 FAIL 하는지 조건에 적어라. `[structural]` 존재 확인 조건에는 적용하지 않는다 (자명하게 실패하므로 무의미)
- **2 개 이상 축의 곱이 조건 의미를 결정하면 인자 매트릭스를 써라 — `cases_total` 을 타이핑하지 마라.** 축·축 값·값의 출처(공유 상수/enum)를 조건에 열거하고 곱은 명령으로 산출한다 (실측: "3 visibility x 6 relation = 18 중 15 만 재현", "16 종 중 2 종만 검증"). 탐색형 스프린트는 같은 매트릭스를 variant 쪽에 써서 **동일 축 값 조합 2 개 이상이면 FAIL** 로 만든다 (실측 UI-04 — 계약이 4 축을 지정했는데도 두 variant 가 4 축 전부 동일값이었다)

## 설정 로드

`.harness/project.yaml`을 읽어 프로젝트 설정을 로드한다.
파일이 없으면 기본값(범용)으로 동작한다.

**`CONTRACT_ROOT` 를 먼저 확정한다.** 규칙은 여기서 재정의하지 않는다 — 정의는
`harness/references/contract-schema.md` §CONTRACT_ROOT 해석 (v5.2) 이 SSOT 다. 요지만 옮기면:
cwd 에서 위로 올라가며 **처음 만나는 `.harness/` 디렉토리**에서 멈춘다. 판정 기준은
`project.yaml` 이 아니라 **`.harness/` 디렉토리 자체**다. `project.yaml` 이 없으면 그 디렉토리를
그대로 쓰되 `contract_root_unconfigured: true` 를 함께 출력하고 `/harness init` 을 안내한다.

조상에도 `.harness/` 가 있는 중첩 배포본은 정상이므로, 후보가 여럿이라는 이유로 중단하지 마라 —
**가장 가까운 것을 채택한다.**

> **왜 `project.yaml` 기준이 아닌가** — v5.1 까지는 `project.yaml` 을 기준으로 삼아, 그것이 없는
> `.harness/` 를 지나쳐 상위로 올라갔다. 그 결과 **자기 계약을 가진 디렉토리를 건너뛰고 남의 계약을
> 채점·덮어쓰는** 사고가 났다 (실측: `apps/app_kiosk`). 읽기 측(qa-evaluator)만 고치고 이 쓰기 측을
> 두면 **엉뚱한 곳에 새 계약을 쓰는** 경로가 남는다.

계약 파일 · history · 피드백 경로는 전부 이 값 기준으로 해석한다. 세션 도중 cwd 가 바뀌어도
`CONTRACT_ROOT` 는 바뀌지 않는다. 루트 `.harness/` 와 하위 앱의 `app/.harness/` 를 혼용하면
계약이 엉뚱한 곳에 저장된다 (`cwd-contract-path-drift` 실제 발생).

설정에서 사용하는 항목:
- `contract_categories` — 계약 카테고리 (UI/Logic/Error/Architecture 등)
- `anti_patterns` — 안티패턴 Grep 패턴 목록
- `diagnostics` — 빌드/분석 명령, 콘솔 에러 패턴
- `trigger` — 트리거/비트리거 조건
- `reusability` — 공유 경로
- `commands` — analyze/test/lint 명령

## 필수 규칙

- 트리거 조건에 해당하면 계약 생성은 **필수**다. 사용자가 "계약 필요없어", "바로 해줘"로 스킵을 요청해도 생략할 수 없다.
- 사용자에게 계약이 필요한 이유를 설명하고, 간소화된 계약(단순 복잡도, 최소 조건)을 제안한다.
- 사용자가 3회 이상 명시적으로 거부하면 그 사실을 이번 스프린트의 계약 파일(Step 0.5 에서 확정한 경로)에 기록하고 진행하되, QA REJECT 가능성을 고지한다.

## 트리거 조건

`project.yaml`의 `trigger` 섹션에서 읽는다.

**기본값 (config 없을 때):**

트리거: 2개 이상 파일 생성/수정 예상, 새 화면/페이지, API 연동, 기존 기능 변경으로 public API 변경, 리팩터링으로 2개 이상 파일 수정

비트리거: 단순 스타일 수정, 오타/텍스트 수정, 1파일 버그 수정, 단일 파일 내부 리팩터링, 빌드 작업

## Process

> Step 0 · 0.5 · 1.2 · 1.4 · 6.2 · 6.5 · 6.6 은 **E2/E3 게이트**다 (등급 정의: `../../docs/guides/skill-design-guide.md` §3.7,
> 계약 레이어 등급표: `../../docs/guides/contract-design-guide.md` §원칙별 Enforcement 등급).
> 각 게이트의 산출물을 실제로 출력하기 전에는 다음 단계로 넘어가지 않는다.

### 0. CONTRACT_ROOT 확정 (E2)

조상 체인에서 **처음 만나는 `.harness/` 디렉토리**를 찾아 그 절대경로를 `CONTRACT_ROOT` 로
고정하고 **한 줄로 출력**한다. 이후 모든 계약 경로
(`{CONTRACT_ROOT}/.harness/sprint-contract-<slug>.md`, `{CONTRACT_ROOT}/.harness/history/`)를
이 값 기준 절대경로로 쓴다. 상대경로 금지.

아래 스니펫은 `harness/agents/qa-evaluator.md` Step 1-a 와 **동일한 알고리즘**이다 (읽기·쓰기가
갈라지면 조용한 오귀속이 재발한다). 글로빙을 쓰지 않으므로 zsh·bash 양쪽에서 동작한다.

```bash
# 조상 체인을 올라가며 '처음 만나는 .harness' 에서 멈춘다. project.yaml 유무는 그 다음 문제다.
CONTRACT_ROOT=""; CONTRACT_ROOT_UNCONFIGURED=false
d=$PWD
while : ; do
  if [ -d "$d/.harness" ]; then
    CONTRACT_ROOT="$d"
    [ -f "$d/.harness/project.yaml" ] || CONTRACT_ROOT_UNCONFIGURED=true
    break
  fi
  [ "$d" = "/" ] && break
  d=$(dirname "$d")
done

printf 'CONTRACT_ROOT=%s contract_root_unconfigured=%s\n' \
  "${CONTRACT_ROOT:-<none>}" "$CONTRACT_ROOT_UNCONFIGURED"
```

`CONTRACT_ROOT` 가 비면(`<none>`) 계약을 쓸 위치를 정할 수 없다. 임의로 cwd 에 만들지 말고
**중단하고 `/harness init` 을 안내**하라. `contract_root_unconfigured=true` 면 계약은 그 디렉토리에
쓰되 출력에 그 사실과 `/harness init` 안내를 함께 남긴다.

### 0.5. 슬러그 확정 · 경로 선점 (E2)

병렬 세션이 서로의 계약을 덮어쓰지 않도록, **계약 본문을 쓰기 전에** 이 스프린트가 쓸 파일 경로를
확정하고 선점한다. 아래 (a)(b)(c) 를 순서대로 수행하고 결과를 출력한다.

**(a) 슬러그 확정** — 도출·정규화·**형식** 규약의 정의는
`harness/references/contract-schema.md` §계약 파일 — 산출물 경로 > 슬러그 규칙 에 있다.
**그 섹션이 SSOT 다** — 여기서 재정의하지 말고 규약을 **적용**하라. 아래는 원문 인용이며 서술이
어긋나면 스키마가 이긴다: 소문자화 → 공백·특수문자를 `-` 로 치환 → 연속 `-` 축약 → 앞뒤 `-` 제거,
최종 형식이 `^[a-z0-9][a-z0-9-]{0,47}$` 를 만족해야 한다.

아래 (a-0)~(a-3) 은 그 형식 규약을 **바꾸지 않는다.** 형식을 통과한 후보를 *자동 채택해도 되는가*
를 판정하는 추가 절차이며, 우선순위는 **사용자 지정 > 기존 슬러그 재사용 > 도출** 이다.

**(a-0) 사용자가 슬러그를 직접 준 경우** — 호출 인자나 대화에서 `slug=<값>` 을 명시했으면 도출을
건너뛰고 그 값을 쓴다. 형식 정규식만 검사하고, 통과하면 즉시 확정한다. **사용자가 준 슬러그를
"더 좋게" 다듬지 마라.**

**(a-1) 기존 슬러그 열거 (재사용 탐색)** — 이어서 하는 스프린트면 **기존 슬러그를 그대로 써야**
계약 ↔ 피드백 ↔ amendment 3 종의 짝이 유지된다. 새 슬러그를 만들면 앞 스프린트의
`sprint-feedback-<slug>.md` 가 고아가 되어 접미형을 정식화한 목적이 무너진다.

**글로빙(`sprint-contract-*.md`)으로 열거하지 마라 — `find` 를 써라.** zsh 는 기본 `nomatch` 라
매치가 0 건이면 `for` 루프에 진입조차 못 하고 명령 전체가 죽는다 (`[ -f "$f" ] || continue` 가드는
무력하다). 같은 레포 `harness/skills/harness-kaizen/scripts/trigger-check.sh` 가 이미 셸 무관
`find` 형태를 쓴다 — 그 선례를 따른다.

```bash
EXISTING=$(find "$CONTRACT_ROOT/.harness" -maxdepth 1 -type f \
  -name 'sprint-contract-*.md' 2>/dev/null \
  | sed -E 's#.*/sprint-contract-(.+)\.md$#\1#' | sort)
printf 'EXISTING_SLUGS: %s\n' "$(printf '%s' "$EXISTING" | tr '\n' ' ')"
```

출력된 목록을 사용자에게 보여주고, 이번 스프린트가 그중 하나의 연속이면 **그 슬러그를 채택**한다.

**(a-2)(a-3) 도출 + 채택 게이트** — 새 슬러그일 때만 도출한다. **정규식 통과 여부만으로 자동
채택하지 마라.** `3.16.0 마이그레이션 if 분기 정리` → `3-16-0-if` 는 정규식을 **통과하지만**
원문 정보를 거의 잃은 ASCII 파편이다. 게이트는 세 값을 본다: `FORM`(형식) · `LOST`(치환으로
사라진 비ASCII 바이트 수) · `WORDS`(3 자 이상 알파벳 조각 수).

```bash
SLUG=$(printf '%s' "$FEATURE" | tr '[:upper:]' '[:lower:]' \
  | sed -E 's/[^a-z0-9]+/-/g; s/-+/-/g; s/^-//; s/-$//' | cut -c1-48 | sed -E 's/-+$//')

REUSE=0
[ -n "$SLUG" ] && REUSE=$(printf '%s\n' "$EXISTING" | grep -Fxc "$SLUG" || true)
FORM=$(printf '%s\n' "$SLUG" | grep -cE '^[a-z0-9][a-z0-9-]{0,47}$' || true)
LOST=$(printf '%s' "$FEATURE" | LC_ALL=C tr -d '[:print:]' | wc -c | tr -d ' ')
WORDS=$(printf '%s\n' "$SLUG" | tr '-' '\n' | grep -cE '^[a-z]{3,}$' || true)

if [ "$FORM" = 1 ] && [ "$REUSE" -ge 1 ]; then
  echo "SLUG_REUSE=$SLUG"
elif [ "$FORM" = 1 ] && [ "$LOST" = 0 ] && [ "$WORDS" -ge 1 ]; then
  echo "SLUG_AUTO=$SLUG"
else
  echo "SLUG_CONFIRM cand=[$SLUG] form=$FORM lost=$LOST words=$WORDS"
fi
```

- `SLUG_REUSE` — 도출값이 (a-1) 목록에 이미 있다. **기존 슬러그 재사용**으로 확정하고 (c) 로 간다
  (같은 슬러그 계약이 이미 있으므로 (c) 의 3 분기를 반드시 거친다)
- `SLUG_AUTO` — 새 슬러그로 자동 채택 가능
- `SLUG_CONFIRM` — **자동 채택 금지.** 후보와 세 값을 그대로 보여주고 사용자에게
  "이 슬러그로 갈지 / 다른 슬러그를 줄지" 를 물어 확정한다. 한국어 feature 명은 대부분 여기로
  떨어진다 (`LOST > 0`) — 정상이며, 추측해서 진행하는 것이 오류다
- 사용자가 slug 를 원하지 않는다고 답하면 `SLUG=""` 로 두고 **plain 모드**로 간다

**(b) 경로 확정** — 확정된 경로 3 종을 한 번에 출력한다. 정의는 스키마 §산출물 3 종 에 있고,
이 스킬은 그중 **writer 측 경로**(계약)만 직접 쓴다.

```text
계약        {CONTRACT_ROOT}/.harness/sprint-contract-<slug>.md   ← 이 스킬이 쓴다
QA 산출물   {CONTRACT_ROOT}/.harness/sprint-feedback-<slug>.md   ← qa-evaluator 가 쓴다
amendment   {CONTRACT_ROOT}/.harness/sprint-amendments-<slug>.md ← 사이드카, 본문 수정 금지
```

슬러그가 없는 기존 프로젝트의 plain 파일명(`sprint-contract.md` / `sprint-feedback.md`)은
**계속 유효하다.** 이미 plain 계약만 쓰던 프로젝트에서 사용자가 슬러그를 원하지 않으면 plain 모드로
저장해도 되며, plain 모드에서는 frontmatter 의 `slug` 필드를 생략한다. plain 모드를 폐기하거나
기존 plain 계약을 슬러그 파일로 강제 이관하지 마라.

**(c) 선점 (덮어쓰기 없음 보장)** — 확정 경로를 **원자적으로** 예약한다. `set -C`(noclobber) 하의
`>` 는 `O_EXCL` 로 열리므로, 두 세션이 같은 순간에 같은 슬러그를 시도해도 **정확히 한 쪽만 성공**한다.

**plain 모드(`SLUG` 빈 값)에도 선점 절차가 그대로 적용된다.** 경로만 갈라진다 — `$SLUG` 를
파일명에 무조건 이어붙이면 `sprint-contract-.md` 쓰레기 파일이 생긴다 (실측 확인됨).

```bash
if [ -n "$SLUG" ]; then
  CF="$CONTRACT_ROOT/.harness/sprint-contract-$SLUG.md"
else
  CF="$CONTRACT_ROOT/.harness/sprint-contract.md"   # plain 모드
fi
mkdir -p "$CONTRACT_ROOT/.harness"
if ( set -C; : > "$CF" ) 2>/dev/null; then echo "RESERVED $CF"; else echo "TAKEN $CF"; fi
```

- `RESERVED` — 이 세션이 소유자다. 빈 파일이 예약되었으니 Step 6 에서 이 경로에 본문을 쓴다.
  Step 6 에 도달하지 못하고 중단하면 **남은 빈 파일을 지워** 다른 세션이 슬러그를 쓸 수 있게 한다.
- `TAKEN` — 이미 누가 쓰고 있다. **어떤 경우에도 그 파일을 덮어쓰지 마라.** frontmatter 를 읽어
  분기하되, **값의 따옴표를 반드시 벗기고 비교한다.** 레거시 계약은 `owner_session: "abc"` 처럼
  따옴표가 붙어 있어, 안 벗기면 `$CLAUDE_CODE_SESSION_ID` 와 **영원히 일치하지 않는다.**

**첫 frontmatter 블록만 읽는다 — sed 범위(`/^---$/,/^---$/`)를 쓰지 마라.** 범위는 닫는 `---` 뒤에
**재점화**되어 본문까지 훑는다. 계약 본문에 `---` 로 감싼 frontmatter 예시가 실려 있고 진짜
frontmatter 에 그 키가 없으면(레거시 계약, 또는 `CLAUDE_CODE_SESSION_ID` 가 비어 `owner_session` 을
생략한 계약) **본문 값을 frontmatter 값으로 읽는다.** 본문 예시의 `owner_session` 이 현재 세션 ID 와
같으면 아래 분기가 "내 세션의 재작성" 으로 빠져 **남의 active 계약을 history 로 옮긴다.**
reader 측 `fm_get`(`harness/agents/qa-evaluator.md` Step 1-b)은 닫는 `---` 에서 멈추므로,
**두 파서가 갈라지면 writer 만 오판한다.** 아래는 `fm_get` 과 동일 동작이며 인자 순서만 다르다.

```bash
read_fm() {   # read_fm <key> <file> — 첫 frontmatter 블록에서만 읽어 따옴표를 벗겨 출력
  awk -v k="^$1:[[:space:]]*" '
    NR==1 && /^---[[:space:]]*$/ { fm=1; next }
    fm && /^---[[:space:]]*$/    { exit }
    fm && $0 ~ k                 { sub(k, "", $0); print; exit }
  ' "$2" | sed -e "s/[[:space:]]*$//" -e "s/^['\"]//" -e "s/['\"]\$//"
}
echo "status=[$(read_fm status "$CF")] owner=[$(read_fm owner_session "$CF")]"
```

**분기 전에 봉인부터 검증한다 (v5.3).** 이어작업으로 기존 계약을 다시 여는 이 시점이, 지난
스프린트에서 조건 본문이 변조됐는지 확인할 수 있는 **작성 측의 유일한 검사 지점**이다. 검증
함수 정의는 `harness/references/contract-schema.md` §계약 봉인 이 SSOT 다 — 여기서 재정의하지
말고 그대로 쓴다 (`sha256_16` · `contract_digest` · `verify_seal`).

```bash
REC=$(read_fm conditions_digest "$CF"); REC=${REC#sha256:}
if [ -z "$REC" ]; then
  echo "SEAL_ABSENT $CF (레거시 — 경고이지 실패가 아니다. 소급 봉인 금지)"
else
  ACT=$(grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$CF" | sed -E 's/^- \[[ x]\]/- [ ]/' | sha256_16)
  [ "$REC" = "$ACT" ] && echo "SEAL_OK $CF" \
    || echo "SEAL_BROKEN $CF recorded=$REC actual=$ACT"
fi
```

- `SEAL_BROKEN` — **조용히 다시 봉인하지 마라.** 두 값을 그대로 사용자에게 보고하고, 아래 3 분기
  중 무엇을 택할지 함께 정한다. 변경이 정당했다면 그 내용을 사이드카 amendment 로 옮겨 적는다.
- `SEAL_ABSENT` — 레거시 계약이다. 경고만 남기고 정상 진행한다. **소급으로 봉인을 써 넣지 마라** —
  원문이 무엇이었는지 증명할 수 없는 봉인이 된다.

`read_fm` 출력으로 `TAKEN` 을 분기한다:

- `owner_session` 이 현재 `$CLAUDE_CODE_SESSION_ID` 와 같다 → 내 세션의 재작성이다.
  Step 6 의 아카이브 규칙에 따라 history 로 옮긴 뒤 다시 선점한다.
- `status: active` 이고 소유자가 다르다 → **같은 슬러그의 활성 계약**이다. 아래 3 분기 중
  하나를 사용자에게 선택받는다. **덮어쓰기는 어떤 경우에도 선택지가 아니다.**
  1. **재사용** — 기존 계약을 그대로 쓰고 이 스킬은 새 계약을 만들지 않는다 (조건 변경이
     필요하면 계약 본문이 아니라 `sprint-amendments-<slug>.md` 사이드카에 쓴다)
  2. **아카이브 후 신규** — 기존 계약을 Step 6 의 history 경로로 **옮긴 뒤** 다시 선점한다.
     옮기는 것이지 지우는 것이 아니다
  3. **BLOCKED** — 다른 세션이 진행 중이라 판단되면 중단하고 사용자에게 보고한다.
     사용자 동의가 있으면 `-2`, `-b` 같은 **구분 접미를 붙인 새 슬러그**로 (a) 부터 다시 한다
- `status` 필드가 없다(레거시) → 활성 여부를 알 수 없으므로 임의 판단하지 말고 위 3 분기를
  동일하게 사용자에게 선택받는다
- **0 바이트다** → 다른 세션이 방금 선점했거나, 앞선 실행이 본문을 쓰기 전에 중단된 흔적이다.
  둘을 구별할 방법이 없으므로 지우지 말고 사용자에게 확인받아라.

계약을 `done` 으로 전환하는 주체는 **qa-evaluator(APPROVE 시점)** 다. 이 스킬은 `status` 를
`done` 으로 바꾸지 않는다 — 여기서는 "같은 슬러그의 기존 active 계약을 어떻게 할지" 만 정한다.

**결과: 같은 슬러그를 두 세션이 동시에 생성해도 어느 쪽도 상대의 계약 파일을 덮어쓰지 않는다.**
선점에 실패한 세션은 BLOCKED 되거나 다른 접미의 새 경로로 이동할 뿐, 기존 파일을 건드리지 않는다.

`CLAUDE_CODE_SESSION_ID` 가 비어 있으면 소유자 비교를 건너뛰고 사용자에게 물어 분기한다.
식별자 부재 자체는 실패 사유가 아니다.

### 1. 요구사항 분석

`$ARGUMENTS`를 분석하여:
- 어떤 feature인지 (신규 vs 기존 확장)
- 영향 범위 (레이어, 파일 수)
- 복잡도 판단 (단순/중간/복잡)

**복잡도는 파일 수로 판정하지 않는다 (E2).** 아래 4 축을 표로 채운 뒤 판정하고, 그 표를 사용자에게
제시한다. 표 없이 "2 파일이라 단순" 으로 넘어가는 것이 `complexity-by-file-count` 실제 발생 형태다.

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 (UI / 상태 / 데이터 / 인프라) | |
| 공개 API·계약 변경 | 외부에 노출된 시그니처 · 응답 형태 · 스키마가 바뀌는가 | |
| 소비면 존재 | 이 변경을 소비하는 반대편(클라이언트 · 호출자 · 생성 코드)이 있는가 | |
| 회귀 위험 | 기존 동작이 깨질 수 있는 경로가 있는가 | |

4 축 중 **2 축 이상이 "예"** 면 파일 수와 무관하게 최소 "중간" 이다.
"공개 API·계약 변경 = 예" 이면서 "소비면 존재 = 예" 면 **"복잡"** 이고 Step 2.5 가 필수다.

### 1.2. 설정 리터럴 대조표 (E2)

`project.yaml` 에서 읽은 값은 **리터럴 그대로** 계약에 전사한다. 기억이나 관례로 바꿔 쓰지 마라 —
`fvm.bat flutter analyze` 를 `fvm flutter analyze` 로 적는 것이 `config-command-mismatch` 실제
발생 형태다. DRAFT 를 제시하기 **전에** 아래 표를 출력한다.

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | | |
| `commands.test` | | |
| `diagnostics.ide_exclude` | | |
| `contract_categories[].id` / `prefix` | | |
| `anti_patterns[].id` / `message` | | |

두 열이 다르면 계약을 고친다. 설정에 값이 없으면 `null` 이라고 적고, 없는 명령을 지어내지 않는다.

### 1.4. Pre-Edit Audit (E2)

계약 초안을 제시하기 전에 **대상 코드/파일을 read-only 로 실제 열어본다.** `project.yaml` 만 읽고
계약을 쓰는 것은 감사가 아니다 (`skipped-pre-edit-audit` 실제 발생 형태 — 대상 화면 파일을 한 번도
열지 않은 채 "Pre-Edit 감사 결과" 를 제시했다).

아래 표를 채워 출력한다. **증거 열이 비어 있으면 그 행은 감사되지 않은 것이다.**

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 여부 |
| --------- | ---------------------------- | ------------------- | ---------------- |
| | | | |

이어서 구현 **후보 옵션**이 2 개 이상이면 옵션 표(선택지 · 장단점 · 영향 파일)를 제시하고 사용자
합의를 받은 뒤 조건을 확정한다 (`skill-design-guide` §3.6 Pre-Edit Batch Audit 의 계약-시점 적용).

### 1.5. 트리거 키워드 중복 검사 (스킬/에이전트 생성 계약 시)

계약이 **새 스킬 / 새 에이전트 생성** 을 요구하거나 description 변경을 수반하면,
**sibling description 과의 트리거 키워드 중복** 을 조건으로 삽입하기 전 실제로
검사해야 한다. set intersection 뿐 아니라 **substring containment** 까지 둘 다
확인한다.

**검사 절차:**

1. 대상 플러그인의 description 을 추출한다. **글로빙으로 파일을 열거하지 마라 — `find` 를 써라**
   (Gotchas 의 하드 규칙). `agents/` 가 없거나 비어 있는 킷(reflect-kit · bambu-kit ·
   onboarding-kit)에서 `<plugin>/agents/*.md` 는 zsh `nomatch` 로 **명령을 통째로 죽여** 출력이
   0 건이 된다. `2>/dev/null` 은 글로빙 실패를 막지 못한다 — 확장은 명령 실행 **전에** 일어난다.
   `skills/` 와 `agents/` 는 깊이가 달라 `find` 를 두 번 돌린다:
   ```bash
   PLUGIN=reflect-kit   # 대상 플러그인 이름으로 바꿔라 (`<plugin>` 을 그대로 두면 리다이렉션으로 파싱된다)
   find "$PLUGIN/skills" -mindepth 2 -maxdepth 2 -type f -name 'SKILL.md' \
     -exec grep -Hn '^description:' {} + 2>/dev/null
   find "$PLUGIN/agents" -maxdepth 1 -type f -name '*.md' \
     -exec grep -Hn '^description:' {} + 2>/dev/null
   ```
   `-exec ... +` 는 매치가 0 건이면 `grep` 을 아예 실행하지 않는다. `xargs` 로 바꾸지 마라 —
   BSD `xargs` 는 입력이 비어도 유틸리티를 1 회 실행해 `grep` 이 stdin 을 기다린다.
2. 각 description 에서 트리거 키워드 (`"..."` 로 묶인 구문, 또는 콤마 분리 구문) 를
   정규식으로 파싱하여 `{skill_id: [keyword, ...]}` 맵을 만든다
3. **Set intersection 검사**: 모든 스킬 쌍 (i, j) 에 대해 `keywords[i] ∩ keywords[j]`
   가 공집합인지 확인 — 완전 일치 중복
4. **Substring containment 검사**: 모든 키워드 쌍 (k1, k2) 에 대해 `k1 != k2` 이면서
   `k1 ⊂ k2` (또는 k2 ⊂ k1) 인 경우가 없는지 확인 — 부분문자열 중복
5. 두 검사 모두 0 건 확인 후 계약 조건에 "substring containment 포함 배타성" 을
   요구하는 문구로 작성한다

**실패 사례 (RE-02 / SK-05, react-kit 2026-04)**:
- "API 연동" (react-api) ⊂ "API 연동 화면" (react-feature) — substring 중복, set
  intersection 만 검사하면 미탐지
- "wasm-pack 빌드" (react-run) == "wasm-pack 빌드" (react-wasm) — set intersection
  으로 탐지 가능하지만 이전 사이클에서 누락되어 REJECT

**계약 조건 예시:**

```text
- [ ] RE-05: <plugin> 내 모든 스킬/에이전트 description 의 트리거 키워드가
      (a) set intersection 공집합이고 (b) 어느 키워드도 다른 키워드의 부분문자열이
      아니다 [exact, enumerated]
      (측정: 위 1 번의 `find ... -exec grep -Hn '^description:' {} +` 2 회 실행 후
      Python/bash 로 set intersection + substring pair 0 건 확인)
```

### 2. 완료 조건 생성

`project.yaml`의 `contract_categories`에 정의된 카테고리별로 테스트 가능한 조건을 작성한다.

**각 조건의 규칙:**
- PASS/FAIL로 이진 판정 가능해야 한다
- "잘 동작한다", "적절히 처리한다" 같은 모호한 표현 금지
- 구체적 상태, 컴포넌트, 동작을 명시한다

**카테고리 포맷:**

```markdown
## {카테고리 ID}
- [ ] {PREFIX}-01: {설명}
- [ ] {PREFIX}-02: ...
```

**복잡도별 조건 수 가이드:**
- 단순 (1-3 파일): 카테고리당 1-2개, 총 4-6개
- 중간 (4-8 파일): 카테고리당 2-3개, 총 8-12개
- 복잡 (9+ 파일): 카테고리당 3-5개, 총 12-20개

**조건 패턴 3 종 (v5.3)** — 해당하는 조건에만 적용한다. 전 조건에 강요하면 과잉 절차다.
포맷 정의는 `harness/references/contract-schema.md` 가 SSOT 이며 여기서 재정의하지 않는다.

| 패턴 | 적용 조건 | 요구 |
| ---- | -------- | ---- |
| **측정 커버리지 표기** | `enumerated` 태그 조건 | 산문 측 대상과 측정 측 대상을 **같은 표기**(백틱 · 공백 없는 토큰)로 적는다. 상위 패턴으로 덮으면 **작성 시점에 1 회 실행해 확장 결과를 측정 절에 열거** |
| **인자 매트릭스** | 2 개 이상 축의 곱이 조건 의미를 결정할 때 | 축·축 값·값의 출처(공유 상수/enum)를 열거하고 `cases_total` 은 **명령으로 산출**. 탐색형이면 variant 별 축 값 조합을 열거하고 중복 조합 = FAIL |
| **음성 대조** | 조건이 **테스트 통과**로 판정될 때 | `음성 대조:` 절에 "어느 구현 지점을 무력화하면 이 측정이 FAIL 하는지" 를 적는다. `[structural]` 존재 조건에는 적용하지 않는다 |

**직전 사이클의 amendment 확정분을 원문에 반영한다 (v5.3).** 같은 슬러그를 이어받는
스프린트라면 사이드카를 먼저 읽고, 확정된 `narrowing` 을 **새 계약 조건의 원문에** 녹여
넣는다. 그러지 않으면 "write-once 계약 원문이 amendment 로 대체된 채 남아있다" 상태가 누적되어
다음 평가자가 두 문서를 겹쳐 읽어야 한다 (실측 improvement `[LG-02, LG-04]`).

```bash
# 이어작업 슬러그의 사이드카 확인 — 글로빙 금지 (§셸 이식성)
find "$CONTRACT_ROOT/.harness" -maxdepth 1 -type f \
  \( -name 'sprint-amendments.md' -o -name "sprint-amendments-$SLUG.md" \) 2>/dev/null
```

### 2.5. Counterpart 조건 삽입 (E2)

Step 1 의 "공개 API·계약 변경" 또는 "소비면 존재" 가 "예" 면 **Counterpart 조건을 반드시 넣는다.**
이 원칙은 평가자 가이드에 대응 규칙이 없다 — **계약에 조건으로 넣지 않으면 아무도 잡지 않는다.**

적용 대상: API 계약 · 엔드포인트 시그니처 · 상태 코드 · 직렬화 포맷(날짜/타임존/enum/null) ·
공유 모델 · 생성 코드 · 공개 함수 시그니처 · 이벤트 페이로드 · DB 스키마.

1. producer 면과 consumer 면 파일을 **grep 으로 실제 탐색**해 경로를 확보한다
2. **양면을 별도 조건 2 개**로 쓴다 (한 조건에 묶으면 복합 조건 — 부분 통과가 PASS 로 샌다)
3. 각 조건은 파일 경로를 `[exact, enumerated]` 로 열거한다 (`collective` 금지)
4. consumer 를 못 찾으면 "소비자 없음" 을 근거와 함께 조건에 적는다 — 추측으로 생략 금지
5. 소비면의 **내부 구현**은 조건화하지 않는다 (과잉 계약)
6. 이번 스프린트에 양면을 다 못 바꾸면 남는 쪽을 **명시적 미완 조건**으로 남긴다.
   `[미검증]` 을 쓰지 마라 — 그 마커는 검증 도구 부재 전용이다

상세 규칙과 예시: `../../docs/guides/contract-design-guide.md` §양면 조건 — Counterpart Conditions.

### 3. 안티패턴 체크리스트

`project.yaml`의 `anti_patterns`에서 읽어 해당 기능에서 위반 가능성이 높은 것만 선별한다.

```markdown
## Anti-patterns
- [ ] {id}: {message}
```

### 4. 자동 포함 섹션

아래 섹션은 **모든 계약에 자동 포함**되며 사용자 수정 불가:

```markdown
## Reusability
- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics
- [ ] DG-01: {commands.analyze} 워닝 0개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ({diagnostics.ide_exclude} 제외)
- [ ] DG-03: {commands.test} 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개
```

### 5. 사용자 승인

완료 조건과 안티패턴 체크리스트를 제시하고 사용자 확인을 기다린다.
**사용자가 수정 요청하면 반영 후 재제시한다.**

### 6. 계약 저장

사용자 승인 후 **Step 0.5 에서 선점한 경로**
`{CONTRACT_ROOT}/.harness/sprint-contract-<slug>.md` (`$CF`) 에 저장한다. plain 모드면
`{CONTRACT_ROOT}/.harness/sprint-contract.md` 에 저장한다. 선점하지 않은 경로에 쓰지 마라.

**frontmatter** — 필드 정의는 `harness/references/contract-schema.md` §메타데이터 > v5 신규 필드,
`status` 해석은 §status 해석 규칙 을 따른다. 아래는 그 규약을 적용한 형태다:

**따옴표 규약** — `slug` · `status` · `owner_session` 은 **따옴표 없이** 쓴다. 값에 공백·콜론이
없는 식별자이기 때문이며, 무엇보다 reader 가 따옴표를 안 벗기면 `owner_session` 비교가 영구
불성립한다. 공백·콜론이 들어가는 `feature` · `created` · `complexity` 만 따옴표를 유지한다.
(reader 측은 Step 0.5 (c) 의 `read_fm` 처럼 **양쪽 다 벗겨서** 읽는 것이 규약이다 — 레거시
따옴표 계약이 배포본에 남아 있다.)

```markdown
---
feature: "{이름}"
slug: {slug}
created: "{YYYY-MM-DD HH:mm}"
complexity: "{단순|중간|복잡}"
conditions: {Step 6.2 가 계산한 값}
status: active
owner_session: {$CLAUDE_CODE_SESSION_ID}
conditions_digest: sha256:{Step 6.6 이 계산한 값}
locked_at: "{YYYY-MM-DD HH:mm}"
---

## {카테고리별 조건}
...

## Anti-patterns
...

## Reusability
...

## Diagnostics
...
```

- `slug` — plain 모드면 **필드 자체를 생략**한다. 접미형이면 파일명 접미와 **동일**해야 한다
- `status` — 저장 시점에는 항상 `active`. **`done` 전환은 이 스킬이 하지 않는다** —
  qa-evaluator 가 APPROVE 시점에 수행한다.
  `status` 가 없는 레거시 계약은 active 로 세지 않는다는 것이 qa-evaluator 의 전제이므로,
  이 스킬이 새로 쓰는 계약에는 **반드시 `status` 를 적는다**
- `owner_session` — `$CLAUDE_CODE_SESSION_ID` 를 그대로 쓴다. 환경변수가 비어 있으면
  **필드 자체를 생략**한다. 빈 문자열이나 `unknown` 같은 자리표시자를 쓰지 마라
- `conditions_digest` · `locked_at` — **Step 6.6 에서 채운다.** 본문 저장 시점에는 값을 모르므로
  자리표시자를 넣지 말고, Step 6.6 이 계산한 값을 그때 써 넣는다

**아카이브** — Step 0.5 (c) 에서 **"아카이브 후 신규" 를 선택했을 때만** 수행한다.
같은 슬러그의 기존 계약을
`{CONTRACT_ROOT}/.harness/history/{YYYYMMDD-HHmm}-sprint-contract-<slug>.md` 로 옮기고,
옮긴 사본의 `status` 를 `done` 으로 바꾼다 (plain 모드는 `-<slug>` 없이 동일 규칙). 이것은
아카이브 사본에 대한 조치이며, 살아 있는 계약의 `done` 전환(qa-evaluator 소관)과는 별개다.
**다른 슬러그의 계약은 읽지도 옮기지도 마라** — 다른 세션이 쓰고 있는 파일이다.

**포맷 규칙 (QA Evaluator 파싱 호환):**
- YAML frontmatter로 메타데이터
- **섹션 헤더는 2 계층만 허용한다** (`harness/references/contract-schema.md` §허용 섹션 헤더):
  - **조건 섹션 (parsed)** — `project.yaml` 카테고리 ID + `Anti-patterns` + `Reusability` +
    `Diagnostics`. 정확히 일치해야 하며 괄호 부연 금지. `- [ ] {PREFIX}-{NN}:` 조건은 **여기에만**
  - **서술 섹션 (non-parsed)** — `배경` · `리서치 소스` · `GAP 분석` · `범위 경계` · `회귀 게이트`.
    접두 일치면 되고 뒤에 부연을 붙여도 된다. **조건 체크박스 금지** (일반 불릿만)
  - 두 목록 밖의 헤더(`Notes`, `Appendix`, `메모` 등)는 금지 — 평가자 파서가 오작동한다
- 모든 체크박스는 unchecked `- [ ]` 상태로 저장
- 모든 카테고리에 최소 1개 조건 필수. 해당 없으면 `- [ ] XX-00: N/A`

### 6.2. 조건 수 계산 (E3)

`conditions:` 값을 **세지 말고 계산한다.** 본문을 저장한 직후 아래를 실행하고, 출력된 숫자를
frontmatter 에 그대로 전사한다.

```bash
grep -cE '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$CF"
```

사람이 세면 Anti-patterns · Reusability · Diagnostics 를 빠뜨린다 — 한 세션에서 18→22, 19→27,
22→25 로 **3 회 연속 틀렸다.** 카테고리 섹션만 세는 습관이 원인이므로, 계산 명령은 섹션을 구분하지
않고 계약 전체의 조건 체크박스를 센다. 값을 고쳤으면 Step 6.5 를 다시 돌린다.

### 6.5. 저장 검사 게이트 (E3)

저장 직후 아래 세 명령을 **실행하고 출력을 인용**한다. LLM 판단이 아니라 명령 출력으로 판정한다.
(`$CF` 는 Step 0.5 에서 선점한 계약 경로다.)

```bash
# (1) 헤더 목록 — 허용 2 계층 밖 헤더가 있으면 위반
grep -n '^## ' "$CF"

# (2) 조건 체크박스가 어느 섹션에 있는지 — 서술 섹션에 있으면 위반
awk '/^## /{s=$0} /^- \[ \]/{print FNR": "s" -> "$0}' "$CF"

# (3) frontmatter conditions 값 == 실제 조건 수 (Step 6.2 재확인)
FM=$(awk -F'[: ]+' '/^conditions:/{print $2; exit}' "$CF")
N=$(grep -cE '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$CF")
[ "$FM" = "$N" ] && echo "OK conditions=$N" || echo "MISMATCH frontmatter=$FM actual=$N"
```

위반이 1 건이라도 있으면 계약을 수정하고 재실행한다. **통과 전에는 Step 6.6 으로 진행하지 않는다.**
(`parser-incompatible-contract-section` 실제 발생 — 허용되지 않은 `## Notes` 섹션 추가)

**(4) 측정 커버리지 검출기 — 이것만 blocking 이 아니다.** `enumerated` 조건에서 산문이 요구한
대상이 측정 절에 없으면 `UNCOVERED` 를 출력한다. 검출기 스니펫은
`harness/references/contract-schema.md` §측정 커버리지 표기 가 SSOT 다 — 그대로 실행한다.

`UNCOVERED` 는 **자동 FAIL 이 아니다.** 실측 오탐률 때문이다 (계약 109 개 · `enumerated` 조건
114 개 → 나이브 76 건 / 좁힌 형태 29 건, 상당수가 "상위 명령이 실제로 덮는" 정당 케이스).
출력된 1 건마다 아래 둘 중 하나를 한다:

1. 조건을 고친다 — 측정 절에 누락된 대상을 열거하거나, 상위 패턴을 1 회 실행해 **확장 결과**를 적는다
2. **해소 기록**을 남긴다 — 서술 섹션(`## 범위 경계` 등)에 `커버리지 해소: {조건 ID} — {사유}`
   한 줄. 사유 없이 넘기면 이 검출기를 도입한 의미가 없다

### 6.6. 계약 봉인 (E3)

Step 6.5 를 통과한 직후, 조건을 **봉인**한다. 계산·검증 함수 정의는
`harness/references/contract-schema.md` §계약 봉인 이 SSOT 다 (`sha256_16` · `contract_digest` ·
`verify_seal`) — 여기서 재정의하지 말고 그대로 쓴다.

```bash
# (a) digest 계산 — 조건 체크박스 줄만, 체크 상태를 정규화해서 해시
D=$(grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$CF" | sed -E 's/^- \[[ x]\]/- [ ]/' | sha256_16)

# (b) frontmatter 2 필드 기록 (없으면 추가, 있으면 치환)
#     본문의 `conditions_digest:` 예시 줄을 건드리지 않도록 첫 frontmatter 블록만 손댄다
printf 'conditions_digest=sha256:%s locked_at=%s\n' "$D" "$(date '+%Y-%m-%d %H:%M')"

# (c) 기록 직후 자기 검증 — 출력을 인용한다
REC=$(read_fm conditions_digest "$CF"); REC=${REC#sha256:}
ACT=$(grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$CF" | sed -E 's/^- \[[ x]\]/- [ ]/' | sha256_16)
[ "$REC" = "$ACT" ] && echo "SEAL_OK $CF" || echo "SEAL_BROKEN $CF recorded=$REC actual=$ACT"
```

**(d) 봉인 이후 조건 본문을 편집하지 마라.** 이 시점부터 계약은 write-once 다. 구현 중에
조건이 틀렸다는 것을 알게 돼도 `- [ ]` 줄을 고치지 않는다 — `sprint-amendments-<slug>.md`
사이드카에 쓴다. **자신이 만든 산출물을 사후에 허용하려고 조건 문구를 넓히는 것**이 실측된
위반 형태이며(2026-08-11 REJECT), 그것 때문에 이 규칙이 E1 서술에서 E3 봉인으로 승급했다.

- 체크박스 토글(`- [ ]` → `- [x]`)과 서술 섹션 보강은 봉인을 깨지 않는다 — 의도된 설계다.
- 조건 **문구 변조**와 **조건 추가·삭제**는 반드시 깬다.
- `SEAL_BROKEN` 이 뜨면 **다시 봉인하지 말고** `recorded` / `actual` 을 사용자에게 보고하라.

### 7. 자기진단

1. 구조화 체크리스트 실행:
   - `ambiguous_conditions`: 모호한 표현이 포함된 조건이 있는가? (어휘적/구문적/의미적 모호성 분류 적용)
   - `missing_error_paths`: 에러/예외 경로에 대한 조건이 누락되었는가?
   - `untestable_conditions`: 코드만으로 검증 불가능한 조건이 있는가?
   - `category_coverage_gap`: project.yaml 카테고리 중 커버하지 못한 것이 있는가?
   - `complexity_underestimate`: 복잡도를 과소평가하여 조건 수가 부족한가?
   - `implementation_leakage`: 조건에 내부 구현 용어(클래스명, 메서드명, DB명)가 포함되었는가?
   - `nfr_coverage`: 해당 기능의 비기능 요구사항이 조건에 반영되었는가?
   - `boundary_without_measurement`: 경계값(>=, <=, ==) 조건에 측정 방법이 누락되었는가?
   - `format_granularity_missing`: 포맷 일관성 조건에 적용 수준(file/section/field)이 명시되었는가?
   - `counterpart_missing`: 계약·직렬화·공유 모델 변경인데 consumer 면 조건이 누락되었는가?
   - `preamble_condition_conflict`: 서술 절의 설계 의도와 조건이 서로 다른 것을 요구하는가?
   - `diff_oracle_nonstandard`: 변경 범위 조건이 표준형 4 요소(상태 전제/경로 한정/생성물 제외/기대 집합)를 다 채웠는가?
   - `evidence_artifact_missing`: `[goal]` 조건이 참조하는 증거 기록물의 경로가 조건에 명시되었는가?
   - `section_header_unclassified`: Step 6.5 게이트가 위반 0 건으로 통과했는가?
   - `conditions_count_typed`: `conditions:` 값을 손으로 세지 않고 Step 6.2 명령 출력으로 채웠는가?
   - `slug_reservation_skipped`: Step 0.5 선점 없이 계약 파일을 썼는가? (선점 없이 쓰면 병렬 세션 덮어쓰기 위험)
   - `slug_adopted_without_confirm`: `SLUG_CONFIRM` 이 떴는데 사용자 확인 없이 채택했는가? 또는 (a-1) 기존 슬러그 재사용 탐색을 건너뛰었는가?
   - `contract_seal_missing`: Step 6.6 을 실행해 `conditions_digest` / `locked_at` 을 기록하고 `SEAL_OK` 출력을 인용했는가?
   - `measurement_coverage_gap`: Step 6.5 (4) 의 `UNCOVERED` 각 건에 조건 수정 또는 해소 기록을 남겼는가?
   - `factor_matrix_missing`: 2 개 이상 축의 곱이 의미를 결정하는 조건에 축·축 값·`cases_total` 산출 명령이 있는가? (탐색형이면 variant 축 조합 중복 검사까지)
   - `negative_control_missing`: 테스트 통과로 판정되는 조건에 `음성 대조:` 절이 있는가?
   - `amendment_direction_uncomputed`: 집합형 amendment 의 direction 을 자기신고하지 않고 집합 비교로 계산했는가? 앵커 부재를 이유로 `unknown` 으로 적지 않았는가?
2. 각 항목에 대해 true/false 판정

### 8. 교차 진단

1. Agent tool로 qa-evaluator 서브에이전트를 호출한다
2. 전달 내용: 생성된 계약 조건 전문 (`$CF` 파일 내용) + 그 절대경로.
   경로를 같이 넘겨야 평가자가 계약 선택 ladder 1 단계(명시 경로)로 바로 진입한다
3. 미전달: 사용자 대화 내용, 의사결정 과정
4. 핵심 질문: "이 조건들을 독립적으로 검증할 수 있는가? 모호하거나 해석이 갈리는 조건이 있는가?"
5. 서브에이전트 응답을 `cross_diagnosis_notes`로 기록

### 9. 피드백 저장

1. 자기진단 + 교차 진단 결과를 합쳐 피드백 YAML을 `.harness/feedback-draft.yaml`에 작성한다
   - `harness/references/feedback-schema.yaml`의 스키마를 따른다
   - `skill: sprint-contract`
   - `skill_version`: `harness/.claude-plugin/plugin.json`의 `version` 필드 값
   - `project_hash`: **`save-feedback.sh` 가 `CONTRACT_ROOT` 기준으로 재계산해 덮어쓴다.**
     draft 에 적은 값은 참고용이며, 다르면 스크립트가 stderr 로 경고하고 원본을
     `draft_project_hash` 로 보존한다. 경고가 나오면 draft 계산이 틀린 것이니 원인을 확인하라.
     draft 에 채워 넣을 때도 **`pwd` 가 아니라 `CONTRACT_ROOT` 를 해시한다** — cwd 를 해시하면
     같은 프로젝트인데도 세션마다 다른 해시가 나와 글로벌 피드백이 흩어진다 (실측: `claude-plugins`
     하나에 `project_hash` 43 종).
     ```bash
     # sha256sum → python3 → openssl 순서 fallback (입력은 항상 CONTRACT_ROOT)
     if command -v sha256sum &>/dev/null; then
       printf '%s' "$CONTRACT_ROOT" | sha256sum | cut -c1-8
     elif command -v python3 &>/dev/null; then
       CONTRACT_ROOT="$CONTRACT_ROOT" python3 -c "import hashlib,os; print(hashlib.sha256(os.environ['CONTRACT_ROOT'].encode()).hexdigest()[:8])"
     elif command -v openssl &>/dev/null; then
       printf '%s' "$CONTRACT_ROOT" | openssl dgst -sha256 | sed 's/.*= //' | cut -c1-8
     fi
     ```
   - `sprint_slug` · `contract_path` · `session_id` — `save-feedback.sh` 가 채운다.
     draft 에 손으로 적지 마라
   - `diagnosis.checklist`: Step 7의 결과
   - `diagnosis.cross_diagnosis_by: qa-evaluator`
   - `diagnosis.cross_diagnosis_notes`: Step 8의 결과
2. `bash harness/scripts/save-feedback.sh contract .harness/feedback-draft.yaml` 실행
3. 출력된 저장 경로를 기록한다

### 10. 피드백 검증

1. `bash harness/scripts/verify-feedback.sh {Step 9에서 출력된 경로}` 실행
2. PASS → 스킬 완료
3. FAIL → 피드백 YAML 수정 후 Step 9부터 재시도

## Red Flags + Rationalization Table

`references/red-flags.md`를 읽어라. 계약 작성 후 반드시 해당 체크리스트로 자가 검증한다.
