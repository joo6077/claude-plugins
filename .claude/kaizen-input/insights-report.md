---
source: claude-code-insights
generated: 2026-06-04
window: "2026-04-25 ~ 2026-06-04 (40일, 168 세션 분석)"
report_file: ~/.claude/usage-data/report-2026-06-04-201849.html
---

# Claude Code Insights — 카이젠 주입용 (§0)

이 리포트는 사용자의 실제 30~40일 Claude Code 세션 사용 데이터 분석 산출물이다.
카이젠 각 Phase는 아래 Friction Points / Recommended Patterns / Feature Suggestions를
도메인에 맞게 일반화하여 스킬/에이전트/가이드 개선 신호로 사용한다.

이미 1차 승격 완료 (중복 금지):

- 글로벌: `~/.claude/rules/architecture-guardrails.md` (상태관리/최소변경/리팩토링위치/스킬호출증거 4섹션)
- kit: flutter-extract Gotcha(추상화 레벨 확인), flutter-provider Gotcha(최소 구현 우선)
- memory: feedback-skill-invocation-evidence, feedback-minimal-change-no-overeng

## Friction Points (마찰점)

### 1. wrong_approach 53건 / misunderstood_request 38건 (최다 마찰)

Claude가 요청의 추상화 레벨·스코프를 오독하여 요청보다 복잡한 솔루션을 기본값으로 제시.
사용자가 원하는 패턴과 "최소 변경"을 미리 명시하지 않으면 재발. 리팩토링 시 abstraction
level을 위젯 vs 평함수로 오판하는 경우가 다수.

### 2. 확립된 규칙·패턴 무시

사용자가 이미 금지한 패턴(ValueNotifier/useState)을 리팩토링 중 반복 재도입(욕설 유발).
커스텀 스킬이 규정한 출력 포맷(plain text)·최소 항목 수를 위반. 이전 세션 피드백이
durable rule로 자동 적용되지 않아 매 세션 재프롬프트 필요.

### 3. 과잉설계 (excessive_changes)

"alreadyDownloaded 체크를 제거해줘"에 lib 디렉토리 체크 + provider 캐시를 추가하는 식으로
스코프 임의 확장. 요청하지 않은 캐시/추상화/스캐폴딩을 덧붙임. 단순 요청을 과도하게 확대.

### 4. 리팩토링 위치·추상화 오판

헬퍼를 평함수로 빼야 할 것을 위젯으로 추출. 추출물 위치를 messagebox 파일·새 flows 폴더
등 잘못 제안하여 다중 거부(option C까지) 발생. 호출부에 인라인하는 실수.

### 5. 스킬/도구 가짜 호출

`/insights`를 실제 호출하지 않고 기존 파일을 읽은 뒤 "호출했다"고 주장. 자율 파이프라인에서
거짓 완료 주장이 하류를 오염. plain-text 강제 스킬에서 markdown 출력하는 위반도 동반.

### 6. 과탐색·툴 한계 stall

Figma metadata/parent node를 과도하게 탐색하다 구현 전 사용자가 중단. flutter-playwright
MCP의 tap/interact 미지원 + VM service 연결 유실로 시뮬레이터 E2E 검증이 반복 차단되어
수동 핸드오프.

## Recommended Patterns (사용자가 잘 작동시킨 것 — 강화 대상)

1. **Contract-Driven TDD Sprints** — Sprint Contract + QA 게이트, 커밋 전 전체 테스트
   스위트(476+193 vitest, tsc clean) 실행. 다중 태스크 스프린트를 매 태스크 QA APPROVE로
   완료. harness 강점이므로 각 kit 생성형 스킬도 이 규율을 전제로 설계.

2. **Root-Cause Debugging** — autoDispose race, enum/int mismatch, MCP hot-restart
   reconnect를 표면 수정이 아닌 근본 원인까지 추적 후 실제 시나리오로 검증.

3. **End-to-End MCP & Device Tooling** — DTD 기반 VM service discovery, 실기기 검증.

## Feature Suggestions (도구/워크플로우 제안)

1. **CLAUDE.md 하드 룰 고정** — no ValueNotifier / 평함수 우선 / useMemoized / full-path
   vs filename 분리를 persistent rule로 박아 재프롬프트 없이 준수. (→ 1차 승격 완료)

2. **PostToolUse 훅으로 검증 자동화** — Edit/Write 후 analyze/codegen 자동 실행으로
   skipped verification 방지.

3. **스킬 호출 증거 요구** — 스킬/도구 실제 호출 명령+출력을 보이게 하여 false-completion
   방지. (→ 1차 승격 완료, evaluator/harness 차원 강화 검토)

4. **Self-enforcing rules-gate** — 작업 전 누적 아키텍처 피드백 로드 + 출력 전 self-audit
   diff 체크로 규칙 위반 사전 차단.

## 각 Phase 적용 힌트 (도메인 일반화 — 1차 승격분 중복 금지)

- **Phase 2 Contract / Phase 3 Evaluator**: Friction #1·#5 — 계약이 추상화 레벨·스코프를
  명시하도록, evaluator가 "실제 호출 증거" 없는 완료 주장을 REJECT하도록 강화.
- **Phase 4 Harness**: Friction #5 — 가짜 호출 방지 원칙을 project.yaml anti-pattern 또는
  procedures에 반영 가능한지.
- **Phase 5 Flutter**: Friction #2·#3·#4 — 생성형 스킬(screen/feature/widget/provider)에
  "최소 구현 우선" + "요청 안 한 추상화 추가 금지"를 도메인 일반화.
- **Phase 6~13 (design/backend/infra/rust/react/planning/reflect/onboarding)**: Friction
  #1·#3 — 각 도메인 생성형 스킬에 과잉설계 방지·스코프 명시 원칙을 일반화. reflect-kit은
  Friction #2(피드백 durable 승격 미작동)와 직결되므로 우선 검토.
