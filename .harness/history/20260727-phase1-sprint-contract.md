---
feature: "kaizen Phase 1 — 설계 가이드 (skill-design-guide · agent-design-guide) enforcement 전환 + 사실 정정"
created: "2026-07-27 19:20"
complexity: "complex"
conditions: 14
---

# Sprint Contract — Phase 1 설계 가이드 카이젠

## 배경 · 이번 사이클 프레이밍

`/insights` 2026-07-27 (51세션/187커밋/53일) 의 Friction #1·#3 은 직전 사이클에 이미 승격된 주제이고
세션당 비율이 줄지 않았다. 따라서 **새 soft 규칙을 추가하는 것은 정답이 아니다.**
이번 Phase 1 의 목표는 두 가지다:

1. **enforcement 전환** — 문장형 규칙(soft reminder) 을 증거 아티팩트 기반 게이트로 등급화한다.
2. **사실 정정** — 공식 문서와 어긋난 서술(서브에이전트 중첩 불가, frontmatter 스키마) 을 바로잡는다.

신규 흡수 대상은 Friction #2 (검증 불가 완료 주장) 과 Friction #4 (양면 변경 누락) 두 건으로 한정한다.

## 리서치 소스 (필수 3+ 건 · 실제 6 건 조회)

Context7 MCP 는 이 세션에서 OAuth 미인증이라 사용 불가 → `phase-research-templates.md` §Phase 1 의 fallback 인
WebFetch 로 1 차 출처를 직접 조회했다 (fallback 사유: Context7 non-interactive 세션 인증 불가).

| # | 소스 | 유형 | URL |
| - | ---- | ---- | --- |
| 1 | Skill Authoring Best Practices | 공식 | <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices> |
| 2 | Create custom subagents | 공식 | <https://code.claude.com/docs/en/sub-agents> |
| 3 | anthropics/skills — skill-creator SKILL.md | 공식 | <https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md> |
| 4 | From Confident Closing to Silent Failure (False Success) | 학술 | <https://arxiv.org/abs/2606.09863> |
| 5 | Reason Less, Verify More — Deterministic Gates | 학술 | <https://arxiv.org/html/2607.07405v1> |
| 6 | How Coding Agents Fail Their Users (20,574 세션) | 학술 | <https://arxiv.org/abs/2605.29442> |

## GAP 분석 (리서치·데이터 vs 현재 가이드)

| # | 신호 | 근거 | 현재 상태 | 판정 |
| - | ---- | ---- | --------- | ---- |
| G1 | 증거 없는 완료 주장 | 소스 4 (자기평가 코딩 에이전트 궤적 중 false success 75.8%), 소스 6 (부정확한 자기보고 비중 증가) | skill-design-guide §3.6 은 "검증 기준을 제공하라" 까지만. `[미검증]` 프로토콜은 agent-design-guide §10 전용이며 parity 표가 "에이전트 전용" 으로 못 박음 | 신규 §3.7 |
| G2 | enforcement 형태 미구분 | 소스 5 (결정론적 게이트는 per-run 보장, 프롬프트는 통계적 개선), 소스 4 (LLM judge AUROC 0.54~0.65) | 두 가이드 모두 "…하라" 문장형만. 원칙을 어떤 강도로 구현할지 판정 규칙 없음 | §3.7 내 등급 사다리 |
| G3 | 양면(two-sided) 변경 누락 | insights Friction #4, 소스 1 "Create verifiable intermediate outputs" | §5.5 Enumerate-before-Act 와 §3.6 Pre-Edit Batch Audit 는 **변경 대상 파일 내부**만 열거. 소비자/호출자 열거 규칙 없음 | §5.5 하위 신설 |
| G4 | 서브에이전트 중첩 | 소스 2 "Let subagents spawn their own subagents" — 기본 3 층 (v2.1.219+), `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` | agent-design-guide 4 곳(§4, §10 ×2, 요약표)에서 "중첩 불가" 를 사실로 단언 | **사실 오류 정정** |
| G5 | 서브에이전트 상한 | 소스 2: concurrent 20 / session 200 / depth 3 | §7 은 자체 권고 "5 개 이하"만, 플랫폼 하드 리밋 미기재 | §7 보강 |
| G6 | frontmatter drift | 소스 2: `model: fable`·풀 ID 예 `claude-opus-5`, `permissionMode: auto`/`manual`, `effort: xhigh`, background 기본값 변경, `prompt` 필드, `name` → hooks `agent_type` | §2 표가 구버전 | 표 갱신 |

**예방적 분석 — 리서치가 지목하는 anti-pattern 잔존 여부**

- 소스 1 "Avoid time-sensitive information": 두 가이드 모두 버전·날짜를 출처 표기에만 사용 → 위반 없음.
- 소스 1 "Avoid offering too many options": 신규 섹션에서 옵션 나열 대신 기본값 1 개 + 예외 형태 유지.
- 소스 1 "Use consistent terminology": `[미검증]` 을 신규 용어로 만들지 않고 기존 레포 용어를 그대로 재사용.

## Skill (스킬 설계 가이드)

- [ ] SK-01: `harness/docs/guides/skill-design-guide.md` 에 신규 최상위 섹션 "3.7"(제목에 `Completion Evidence Gate` 문자열 포함)이 존재한다 [exact] · 측정: `grep -n "^## 3.7" harness/docs/guides/skill-design-guide.md`
- [ ] SK-02: §3.7 에 enforcement 3 등급(문장 규칙 / 체크리스트 아티팩트 / 결정론적 게이트)이 각각 개별 항목으로 열거되고, 등급 승급 조건(재발 횟수 또는 비가역·신뢰 영향)이 1 문장 이상 기술된다 [structural, enumerated] · 측정: Read 로 §3.7 본문 확인
- [ ] SK-03: §3.7 이 `[미검증]` 마커를 스킬(생성) 측 규약으로 명시하고, 마커 없는 조용한 성공 주장 금지를 문장으로 포함한다 [exact] · 측정: `grep -c "\[미검증\]" harness/docs/guides/skill-design-guide.md` 결과 ≥ 1
- [ ] SK-04: §3.7 에 "렌더 가능한 산출물은 렌더 결과를 증거로 쓰되 **빈 결과는 PASS 증거가 아니라 검증 실패 신호**" 취지의 조항이 존재한다 [structural] · 측정: Read 로 확인 (Friction #2 fit-pal 빈 카탈로그 사고 직접 대응)
- [ ] SK-05: `skill-design-guide.md` §5.5 하위에 Counterpart Enumeration(변경의 반대편/소비자 열거) 서브섹션이 신설되고, 계약·직렬화·공유 모델 변경을 적용 대상으로 명시한다 [structural] · 측정: `grep -n "Counterpart Enumeration" harness/docs/guides/skill-design-guide.md`
- [ ] SK-06: skill-design-guide 요약 표에 §3.7 과 Counterpart Enumeration 두 원칙이 각각 1 행씩 추가된다 [exact, enumerated] · 측정: 요약 표 Read
- [ ] SK-07: skill-design-guide §11 parity 표의 Item 5 (Unverifiable / degraded-mode 정책) 가 "에이전트 전용" 에서 **양쪽 존재** 로 갱신되고, 표 아래 예외 서술 문장도 함께 정정된다 [exact] · 측정: §11 표 + 직후 문단 Read (표만 고치고 문장을 방치하면 FAIL)

## Architecture (에이전트 설계 가이드 · 사실 정합성)

- [ ] AR-01: `harness/docs/guides/agent-design-guide.md` 에서 "서브에이전트는 다른 서브에이전트를 생성/스폰할 수 없다" 취지의 서술이 **0 건** 남는다 [exact] · 측정: `grep -n "스폰할 수 없\|생성할 수 없\|중첩 불가" harness/docs/guides/agent-design-guide.md` 결과 0 행
- [ ] AR-02: 정정된 서술이 공식 사실(기본 3 층 중첩 · `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` 로 조정 · `Agent` 를 tools 에서 빼거나 `disallowedTools` 로 차단 가능)을 4 개 요소 모두 포함하여 기술한다 [exact, enumerated] · 측정: §4 Read
- [ ] AR-03: §10 "Self-Evaluator Rule-by-Rule Audit" 항목의 근거가 "중첩 불가의 우회법" 이 아닌 **독립 컨텍스트 편향 회피** 계열 근거로 재서술되고, 기법 자체(자기 규칙 전수 대조 + 외부 평가 대체 불가)는 보존된다 [structural] · 측정: §10 Read — 기존 arxiv 2604.08401 인용 유지 여부 확인
- [ ] AR-04: agent-design-guide §2 frontmatter 표가 `fable` 모델, `permissionMode` 의 `auto`/`manual`, `effort` 의 `xhigh`, background 기본 동작 변경 4 항목을 모두 반영한다 [exact, enumerated] · 측정: §2 표 Read
- [ ] AR-05: §7 Fan-out 섹션에 플랫폼 하드 리밋(동시 20 · 세션 200 · 깊이 3)이 명시되고, 기존 "기본 5 개 이하" 자체 권고와의 관계(자체 예산 ≤ 하드 리밋)가 1 문장 이상으로 구분 기술된다 [structural] · 측정: §7 Read
- [ ] AR-06: agent-design-guide §12 parity 표 Item 5 가 skill-design-guide §3.7 을 대응 위치로 가리키고, 표 아래 "skill-design-guide 에는 존재하지 않는 것이 정상" 문장이 정정된다 [exact] · 측정: §12 Read
- [ ] AR-07: 두 가이드의 frontmatter `version` 이 각각 bump 되고 `last_updated` 가 `2026-07-27` 로 갱신된다 [exact] · 측정: `head -5` 두 파일

## 안티패턴 (project.yaml)

- AP-03 `^```\s*$` — bare code fence 금지. 신규/수정 fence 전부 언어 태그 필수 (`text`, `bash`, `yaml`, `json`)
- AP-02 `git push --force` — 이번 Phase 는 커밋까지만. push/PR/브랜치 생성 전면 금지

## 범위 경계 (Scope-Bound)

**변경 허용**: `harness/docs/guides/skill-design-guide.md`, `harness/docs/guides/agent-design-guide.md`
**변경 금지**: 그 외 전부 — 다른 kit, `marketplace.json`, `plugin.json`, changelog, README, qa-evaluator.md,
qa-evaluation-guide.md, contract-design-guide.md. 하위 surface 전파는 Phase 2 이후 및 오케스트레이터 Step 12 소관.
`.harness/sprint-contract.md` 와 `.harness/history/` 이동은 프로세스 산출물로 허용.

## 회귀 게이트

- `python3 scripts/validate-plugin.py` → 11 plugins 전부 OK · Exit 0
- `git diff --stat` 대상 파일이 위 2 개 가이드로 한정 (계약/히스토리 파일 제외)
