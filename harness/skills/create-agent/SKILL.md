---
name: create-agent
description: >
  설계 가이드 기반으로 새 에이전트를 생성한다.
  ../../docs/guides/agent-design-guide.md의 6가지 디자인 패턴, 도구 스코핑,
  모델 선택, description 작성법을 따라 에이전트 .md 파일을 스캐폴딩한다.
  "에이전트 만들어줘", "새 에이전트", "create agent", "agent 생성",
  "서브에이전트 추가" 같은 요청 시 트리거.
  기존 에이전트 수정에는 트리거하지 않는다.
  스킬로 충분한 작업이면 트리거하지 않고 create-skill을 권장한다.
argument-hint: "<agent-name>"
user-invocable: true
---

# Create Agent

`../../docs/guides/agent-design-guide.md`를 기반으로 설계 원칙에 맞는 에이전트를 생성한다.

## Gotchas

- 스킬로 충분한 작업에 에이전트를 만들면 불필요한 복잡성 — "별도 컨텍스트 격리" 나 "도구 제한" 이 필요한지 먼저 판단해라
- description 을 사람용 요약으로 쓰면 위임 정확도가 떨어진다 — "언제 위임할지" + 트리거 키워드 + negative trigger (비트리거 조건) 명시
- 도구를 전체 상속(tools 생략) 하면 에이전트의 격리 의미가 없다 — 역할에 필요한 도구만 명시적으로 나열
- 플러그인 에이전트는 hooks, mcpServers, permissionMode 를 지원하지 않는다 — 필요하면 `.claude/agents/` 에 생성
- **frontmatter drift 방지**: `tools`, `model` 필드는 validate-plugin V1 검증 대상이다. 둘 중 하나라도 누락되면 에이전트가 Claude 에게 invisible 처리되거나 위임 실패한다 (리서치 근거: LLM Model Drift — byaiteam.com 2025-12-30, Anthropic Agent Skills 공식 frontmatter 요구사항). 생성 직후 `python3 scripts/validate-plugin.py <plugin-name>` 으로 검증해라.
- description 관점 일관성 (3 인칭 또는 명령형) — create-skill Gotchas 와 동일한 Anthropic best practice 규칙을 따른다
- `model: sonnet` 을 기본으로 쓰되, 판단/평가/합성이 필요한 에이전트는 `model: opus` 를 지정해라. 모델 선택 없이 기본 상속하면 호출 시점의 모델에 의존하여 품질이 불안정해진다
- 에이전트 파일명은 `kebab-case.md` 로 통일해라. camelCase, snake_case 를 쓰면 다른 에이전트/스킬의 네이밍 규칙과 불일치한다
- 에이전트가 코드를 수정하면 안 되는 경우(리뷰어, 감사) `Edit`, `Write` 를 tools 에서 제외해라. 읽기 전용 에이전트가 파일을 수정하면 독립 평가의 의미가 사라진다
- 에이전트 생성 후 반드시 해당 플러그인의 README에 등록 여부를 확인해라. `sync-docs.py --check-only` 가 drift 를 알려주지만, 에이전트 추가 자체는 자동 반영되지 않는다
- **Binary Decidability Pre-Check (리뷰어 계열 필수)** — 평가/감사 에이전트(`*-reviewer`, `qa-evaluator`)는 평가 시작 전에 계약 조건을 boolean 판정 가능한지 pre-check 하는 단계를 반드시 포함해야 한다 (agent-design-guide §3.5). "적절히", "필요 시", "보통" 같은 모호 표현을 감지하면 즉시 REJECT 또는 계약 수정 요청을 반환하도록 시스템 프롬프트에 명시해라. 없으면 PH-01 (design-kit 2026-04) 유형 REJECT 재발.
- **Unverifiable 조건 정책 3항** — 평가 에이전트는 검증 불가 상황(mcp_server:null, 런타임 미실행 등) 에서 `[미검증]` 마커를 달고, **2건 이상이면 자동 REJECT** 규칙을 시스템 프롬프트에 명시해야 한다 (agent-design-guide §10). 3항: (1) 미검증 마커 의무, (2) 2건 이상 자동 REJECT, (3) fit-pal/fit-pal-flutter 2026-04 패턴 재발 방지를 위한 "런타임 검증 불가 사유 명시". 없으면 LG-02/DG-04/UI-04 유형 REJECT 재발.
- **Cross-Surface Parity 체크 (agent-design-guide §12)** — 새 에이전트의 시스템 프롬프트 원칙을 추가할 때 parity item 4개(Binary Decidability / 트리거 배타성 / 검증 기준 / Unverifiable 정책) 중 하나인지 판정하고, 해당하면 skill-design-guide §11 · contract-design-guide · qa-evaluation-guide 와 동일 용어로 존재하는지 Grep 으로 확인해라.
- **Rule-by-Rule Audit Before Completion (평가 에이전트 필수)** — 평가/감사 에이전트는 판정 제출 전에 모든 계약 조건을 전수 대조하는 Step 을 포함해야 한다 (agent-design-guide §10 · qa-evaluation-guide §Rule-by-Rule). "샘플링으로 충분" 패턴은 L3 Coverage Honesty 위반이며 `[샘플링-N/전체-M]` 태그 없이 완료 선언 시 자동 REJECT.
- **Sibling Agent 트리거 키워드 배타성 (substring 포함)** — 동일 plugin 의 형제 에이전트 (예: design-reviewer, rust-reviewer, react-reviewer, widget-inspector, animation-architect, backend-reviewer 등) description 간 트리거 키워드 substring containment 까지 금지 (agent-design-guide §3). RE-02 (react-kit 2026-04) 재발 방지.

## Process

### 1. 설계 가이드 읽기

`../../docs/guides/agent-design-guide.md`를 읽어 최신 설계 원칙을 확인한다.
특히 아래 섹션을 참조:
- 섹션 1: 에이전트 vs 스킬 판단 기준
- 섹션 4: 도구 스코핑 (최소 권한)
- 섹션 5: 모델 선택 전략 + Model Routing (작업별 자동 모델 선택)
- 섹션 6: 6가지 디자인 패턴 (계획-실행 분리 포함)
- 섹션 9: 영속 메모리

### 2. 에이전트 필요성 판단

| 기준 | 스킬로 충분 | 에이전트 필요 |
|------|------------|-------------|
| 컨텍스트 격리 | 불필요 | 필요 (메인 보존) |
| 도구 제한 | 불필요 | 필요 (읽기 전용 등) |
| 출력량 | 적음~중간 | 대량 |
| 독립 실행 | 메인 대화 흐름 | 백그라운드/병렬 |

**스킬로 충분하다고 판단되면:** 사용자에게 알리고 `create-skill` 사용을 권장한다.

### 3. 요구사항 분석

- **에이전트 이름** (소문자, 하이픈)
- **역할** — 무엇을 하는 에이전트인가
- **디자인 패턴** — 6가지 중 어디에 속하는가
  1. 프롬프트 체이닝
  2. 라우팅
  3. 병렬화
  4. 오케스트레이터-워커
  5. 평가자-최적화자
  6. 계획-실행 분리
- **필요 도구** — 역할에 최소한으로 필요한 도구 목록
- **모델** — 작업 복잡도에 맞는 모델 (haiku/sonnet/opus/inherit)
- **대상 위치** — 플러그인 agents/ 또는 `.claude/agents/`
- **메모리** — 영속 메모리 필요 여부 (user/project/local)

### 4. 에이전트 파일 생성

`tools` 와 `model` 은 **필수 필드** 다. 누락 시 validate-plugin V1 FAIL + Claude invisible.

```markdown
---
name: {에이전트명}
description: >
  {역할 1줄}.
  {언제 위임하는지 트리거 조건}.
  {negative trigger — 어떤 경우에는 위임하지 않는지}.
tools: {도구 목록}           # 필수 — 쉼표 구분, 역할에 필요한 최소 set
model: {sonnet|opus|haiku|inherit}   # 필수 — 작업 복잡도 기반 선택
# memory: {user|project|local}  # 필요 시
---

{시스템 프롬프트}
```

**시스템 프롬프트 구성:**
1. 역할 정의 (1-2줄)
2. 핵심 제약 (하면 안 되는 것)
3. 실행 절차 (단계별)
4. 출력 형식 (있으면)

### 5. 검증

- [ ] frontmatter 필수 필드 존재 (name, description, tools, model — 4 개 모두)
- [ ] description 에 위임 트리거 + negative trigger (비트리거 조건) 포함
- [ ] description 관점 일관성 (3 인칭 또는 명령형 통일)
- [ ] tools 가 역할에 맞게 최소한으로 제한됨
- [ ] model 이 작업 복잡도에 맞게 선택됨
- [ ] 플러그인 에이전트면 hooks/mcpServers/permissionMode 미사용 확인
- [ ] **Cross-Surface Parity 4 개 item 확인** (agent-design-guide §12): Binary Decidability Pre-Check / 트리거 배타성 (substring 포함) / 검증 기준 / Unverifiable 정책 — 새 원칙이 parity item 에 해당하면 skill-design-guide §11 · contract-design-guide · qa-evaluation-guide 와의 정합성 Grep
- [ ] **리뷰어/평가자 계열인 경우 추가 체크**: (1) Binary Decidability Pre-Check 단계 포함, (2) `[미검증]` 마커 정책 3항 포함, (3) Rule-by-Rule Audit 전수 대조 Step 포함, (4) L3 Coverage Honesty `[샘플링-N/전체-M]` 태그 규칙 명시
- [ ] **Sibling Agent 트리거 배타성**: 동일 plugin 내 형제 에이전트 description 간 substring containment 금지 확인
- [ ] **validate-plugin 연동**: `python3 scripts/validate-plugin.py <plugin-name>` 실행하여 V1/V4/V5/V6 최소 4 개가 OK 인지 확인. 에이전트의 V1 필수 필드는 `name`, `description`, `tools`, `model` 4 개 (스킬과 달리 `user-invocable` 없음). 기준은 `harness/docs/guides/plugin-validation-guide.md §3.1` 참조.

### 6. 사용자에게 결과 제시

생성된 에이전트 파일을 보여주고 확인받는다.
수정 요청 시 반영 후 재제시.
