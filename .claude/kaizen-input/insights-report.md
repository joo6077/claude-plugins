---
source: claude-code-insights
generated: 2026-07-27
window: "2026-06-04 ~ 2026-07-27 (53일, 56 세션 중 51 세션 분석, 1,092 메시지, 187 커밋)"
report_file: ~/.claude/usage-data/report-2026-07-27-182904.html
supersedes: 2026-06-04 (168 세션 / 40일)
companion: .claude/kaizen-input/reflect-digest-2026-07-27.md (760 reflection 엔트리, 30d)
---

# Claude Code Insights — 카이젠 주입용 (§0)

사용자의 실제 53일 Claude Code 세션 사용 데이터 분석 산출물이다. 카이젠 각 Phase는 아래
Friction Points / Recommended Patterns / Feature Suggestions를 **도메인에 맞게 일반화**하여
스킬/에이전트/가이드 개선 신호로 사용한다.

## 직전 사이클(2026-06-04 리포트)에서 이미 승격 완료 — 중복 금지

- 글로벌: `~/.claude/rules/architecture-guardrails.md` (상태관리/최소변경/리팩토링위치/스킬호출증거 4섹션)
- kit: flutter-extract Gotcha(추상화 레벨), flutter-provider Gotcha(최소 구현 우선),
  planning-kit 8스킬 scope-discipline 가드(phase11), react-kit 9스킬 Enumerate-before-Act(phase10),
  setup-guide 스코프 가드(phase13), user-stated-constraint fast-track(phase12)
- memory: feedback-skill-invocation-evidence, feedback-minimal-change-no-overeng

**중요**: 이번 리포트의 Friction #1·#3 은 직전 사이클 Friction #1·#3 과 주제가 겹친다. 그러나
**빈도가 줄지 않았다** (wrong_approach 53→21건이나 세션 수도 168→51로 줄어 세션당 비율은 오히려 상승).
즉 "이미 승격했으니 스킵" 이 아니라 **기존 승격분이 왜 작동하지 않았는지**를 개선 대상으로 삼아야 한다.
새 규칙 추가보다 **enforcement 방식(soft reminder → 구조적 게이트)** 전환이 이번 사이클의 핵심 신호다.

## Friction Points (마찰점)

### 1. 의도 확인 전 편집 착수 (wrong_approach 21건 / misunderstood_request 8건 — 최다)

Claude가 무엇을 원하는지 확정하기 전에 편집을 시작한다. 특히 **시각/애니메이션 작업**에서
말이 의도를 충분히 규정하지 못할 때 집중 발생.

- play 아이콘 자체가 회전하길 원했는데 Material `CircularProgressIndicator`를 새로 만듦 → 전면 재작업
- 렌즈 확대 작업에서 wrong picker / wrong scale / wrong scope를 여러 라운드 반복 → 결국 미커밋·미검증 종료
- 보더만 요청했는데 배경까지 어둡게 변경

→ **일반화**: 생성형·수정형 스킬은 편집 전에 (a) 대상 1줄 재진술 (b) 변경할 것 / 변경하지 않을 것
분리 명시 (c) 근본원인 가설을 먼저 요구해야 한다.

### 2. 시각·런타임 검증을 신뢰할 수 없음 (신규 최상위 신호)

작업의 큰 비중이 UI 폴리시인데 Claude가 결과를 **실제로 보지 못한 채** 성공을 주장한다.
사용자 불만족은 "Claude가 경험적으로 검증할 수 없는 작업"과 거의 완벽히 상관한다.

- 빈 카탈로그를 웹 MCP 스냅샷 근거로 "정상 렌더링" 이라 반복 주장 → 실제로는 unbounded-height
  ListView collapse 버그. 사용자 신뢰 손상 + 욕설로 종료된 세션 2건
- AOT 빌드 + multi-VM vmservice race 로 MCP 런타임 검증 자체가 실패 → 검증 부담이 사용자에게 전가
- 사용자가 **"MCP를 UI/e2e 검증에 쓰지 않는 재발 습관을 영구히 고쳐달라"** 는 전용 세션을 개설

→ **일반화**: "동작한다"는 주장은 **아티팩트(스크린샷·테스트 출력·쿼리 결과)** 없이는 금지.
검증 불가 시 조용히 넘어가지 말고 UNVERIFIED로 명시. 이는 harness의 `[미검증]` 프로토콜을
전 kit 생성형 스킬로 확장하라는 신호다.

### 3. 자율 스프린트의 스코프 드리프트 (50세션 중 fully achieved 10 / partial 18)

긴 "자율 진행" 세션이 처리량은 좋지만 과잉확장·날조·미완 핸드오프를 만든다.

- 이미 `UserModeScreen` enum이 동일 14개 화면을 정의하는데 `_SkinScreen` 중복 카탈로그 생성
- 헬퍼를 승인 없이 `lib_core`로 승격 → 사용자가 revert
- 존재하지 않는 FCM credentials 파일명을 **날조** (기존 config가 있었음)

→ **일반화**: 신규 enum/카탈로그/공용 헬퍼 생성 전 **기존 것 grep 필수**. 경로·파일명·env 키를
추측 금지 — 읽어서 확인하거나 모른다고 말할 것.

### 4. 풀스택 변경에서 클라이언트 누락 (반복)

API 계약·직렬화·공유 모델을 서버만 바꾸고 Flutter 클라이언트를 같은 스프린트에 반영하지 않음.
사용자가 "당연히 그러면 클라까지 바꿔야지" 로 명시 개입. UTC 직렬화 버그도 같은 계열.

→ **일반화**: 계약 변경은 **양면(two-sided) 작업**. 계약을 커밋된 아티팩트로 만들고 서버/클라
양쪽 파일을 착수 전에 열거해야 한다. Phase 2(contract) / 7(backend) / 9(rust) / 5(flutter) 공통.

### 5. 배치 커밋이 회귀를 은폐 · 스테일 핸드오프

- 배치 최적화 세션에서 중간 회귀가 뒤늦게 발견되어 되돌아감
- 재개 시 핸드오프 문서가 스테일(PL-2는 이미 완료, 실제 잔여는 S3 reclamation)이라 세션 시작 낭비
- 병렬 세션이 같은 파일을 건드려 빌드 파손

→ **일반화**: 재개 전 핸드오프 문서를 **git 기준으로 재검증**. 검증된 수정 단위로 커밋.

## Recommended Patterns (사용자가 잘 작동시킨 것 — 강화 대상)

1. **Sprint Contract + QA 게이트 + 핸드오프 문서** — 멀티세션 작업(routine schedule S3~S8)을
   재개 가능한 단위로 유지. 651 tests / 22-22 통과 후 커밋. harness의 핵심 강점.
2. **근본원인 우선 디버깅** — FCM 409 partial unique index, InheritedElement/GlobalKey reparent
   crash, 18일간 누수된 시뮬레이터 render host(swap 포화)를 표면 수정 없이 추적.
3. **증거 기반 검증** — 시뮬레이터 스크린샷 before/after, DB 레벨 확인, 실기기 확인.
   최고 성과 세션은 전부 하드 증거를 동반했다.
4. **릴리스 파이프라인 일괄 위임** — 버전 정합·whatsnew·CI·머지·배포·헬스체크·스토어 제출까지
   한 세션에서 완주. RUSTSEC 4건 패치와 Apple 계약 만료 블로커도 흡수.

## Feature Suggestions (도구/워크플로우 제안)

1. **Hooks로 검증 강제** — 아티팩트 없는 "done" 주장을 차단/플래그. Edit/Write 후 fmt/clippy/
   analyze 자동 실행. (사용자가 이미 PreToolUse 문서조회 훅을 운영 중이나 **무시되고 있음** —
   digest에서 `skipped-required-api-doc-check` freq 9로 재위반 확인)
2. **Custom Skills로 반복 워크플로우 고정** — 릴리스 파이프라인, sprint-contract→QA 루프.
3. **Task Agents** — 읽기 전용 서브에이전트가 독립적으로 근본원인을 규명한 뒤 편집. 두 번째
   에이전트가 실기기 MCP로 수정 결과를 독립 검증. 파일 소유권 경계를 명시해 병렬 충돌 방지.

## On the Horizon (사용자가 준비해야 할 상위 워크플로우)

1. **자율 시각 검증 루프** — baseline 캡처 → 변경 → 재캡처 → 픽셀 diff → 의도 외 영역이
   변했으면 self-reject 후 재시도(최대 N회). UI 작업을 왕복 교정에서 단일 승인/거절로 전환.
2. **풀스택 슬라이스 병렬 에이전트** — 계약 에이전트가 타입/OpenAPI를 먼저 확정 → 서버·클라
   에이전트가 별도 worktree에서 병렬 구현 → 계약 테스트 에이전트가 합치 검증.
3. **편집 전 근본원인 게이트** — falsifiable 가설 + 반증 실험 + blast radius를 기록한
   `.diagnosis/<slug>.md` 없이는 Edit/Write 차단(PreToolUse 훅).

## 각 Phase 적용 힌트 (도메인 일반화 — 1차 승격분 중복 금지)

- **Phase 1 설계 가이드**: Friction #1·#2 — 스킬/에이전트 설계 원칙에 "검증 아티팩트 없는 완료
  주장 금지"와 "편집 전 의도 재진술" 을 아키타입 레벨로 반영할지 검토.
- **Phase 2 Contract**: Friction #4 — 계약을 **two-sided(서버/클라 양면) 파일 열거**로 확장.
  digest 결함: `skipped-pre-edit-audit`, `config-command-mismatch`(project.yaml 명령 리터럴 사용),
  `parser-incompatible-contract-section`, `complexity-by-file-count`(파일 수 아닌 영향 범위),
  `cwd-contract-path-drift`.
- **Phase 3 Evaluator**: Friction #2 — `[미검증]` 자동 REJECT는 이미 있으나, digest 결함
  `feedback-script-location-mismatch` / `missing-feedback-scripts`(프로젝트에 save-feedback.sh
  부재 시 BLOCKED)의 fallback 경로가 필요. 글로벌 REJECT 사유에 unstaged working tree 측정
  모호성(`git diff --cached` 기준 권고)이 반복 등장.
- **Phase 4 Harness**: Friction #5 — 핸드오프 재검증(git 기준) + 검증 단위 커밋 원칙.
- **Phase 5 Flutter**: Friction #1·#2·#3 — 시각 검증 아티팩트 의무화가 가장 직접 매핑되는 kit.
  `mismatched-provider-skill`(기존 코어 컨트롤러 수정에 feature 스캐폴딩 스킬 오적용).
- **Phase 6 Design**: Friction #1·#2 — 시안 승인 기록 artifact(글로벌 REJECT UI-06)와
  before/after 증거 규약.
- **Phase 7 Backend / 9 Rust**: Friction #4 — 계약 변경 시 클라이언트 동시 반영.
  `stack-inappropriate-rust-antipatterns`(셸/compose 작업에 Rust 안티패턴 조건 오적용),
  `cargo-test-wrong-target`(binary crate에 `--lib`).
- **Phase 10 React / 11 Planning**: Friction #3 — 기존 것 grep 후 재사용, 날조 금지.
- **Phase 12 Reflect**: digest 최대 신호 — `missing-*-hook-script` 54태그/307엔트리(40%)
  파편화. Stop-hook 분석 프롬프트에 (a) mistake_tag canonicalization (b) 환경 오설정 반복
  로깅 억제 (c) "없는 훅 추가" meta-제안 억제가 필요. 또한 Friction #2 재발이 보여주듯
  **승격된 규칙이 왜 무시되는지**(soft reminder 한계)를 reflect-promote surface 판정에 반영.
- **Phase 13 Bambu / 14 Onboarding**: Friction #3 — 경로·파일명·콘솔 UI 날조 금지.
