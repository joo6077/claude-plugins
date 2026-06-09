---
name: codex-kaizen
description: >
  Codex 위임 방법론과 전역 프롬프트 템플릿(~/.claude/codex-prompt-template.md)을
  실제 위임 로그 기반으로 주기적으로 강화하는 카이젠 루프.
  Stop 훅이 자동 수집한 codex rollout 로그(~/.claude/codex-research-log/*.md)를 읽어
  약한 응답·반복 fallback·output contract 미준수 패턴을 추출하고,
  gpt-5.5 기준 최신 prompting 가이드를 리서치하여 템플릿 개선 diff를 제안한다.
  반영은 사용자 승인 게이트로만. "codex 카이젠", "codex 템플릿 개선", "codex 위임 개선",
  "codex 프롬프트 강화", "/codex-kaizen" 요청 시, 또는 주 1회 스케줄로 트리거.
  실제 Codex 위임(codex-rescue)이나 reflect 파이프라인 개선(reflect-kaizen)과는 다르다 —
  대상은 오직 codex 위임 방법/템플릿이다.
argument-hint: "[window=<Nd>] [research-only]"
user-invocable: true
---

# Codex Kaizen

Codex 위임의 **방법론과 프롬프트 템플릿**을 점진 강화한다. 신호는 내가 손으로 매긴 점수가 아니라, Stop 훅(`~/.claude/hooks/harvest-codex-log.sh`)이 codex 세션 rollout에서 **verbatim으로 자동 수집한 로그**다. 평가는 위임 시점이 아니라 **리뷰 시점에 독립적으로** 한다.

**도메인 경계**: reflect-kaizen은 reflect 파이프라인(분류·승격 품질)을, 이 스킬은 **codex 위임 방법/템플릿**을 개선한다. 신호원(codex 로그 vs reflection 로그)도 대상 자산(codex-prompt-template vs CLAUDE.md/memory/skill/hook)도 다르다. 두 리포트를 섞지 마라.

## 이 스킬 폴더의 파일

- `references/search-sources.md` — Step 2에서 참조하는 1차 출처 목록(OpenAI 공식 docs 9종) + 신뢰도 기준 + 미확인 claim 격리. 추측 기반 변경을 막는 근거 소스다.

## Gotchas

- **자가채점 부활 금지.** 위임 시점에 5축 self-score를 매기는 ritual은 폐기됐다(신뢰도 0 — 내가 시킨 출력을 내가 후하게 매김). 평가는 리뷰 시점에 verbatim 로그를 독립적으로 읽고 한다. 점수표를 다시 만들지 마라.
- **거대화 금지.** 이 스킬을 위해 sprint-contract·QA 에이전트·별도 가설 누적파일·스핀오프 세션을 만들지 마라. 로그가 누적 신호, 템플릿 changelog가 기록이다. 한 번 호출에 한 번 개선.
- **승인 게이트 — 무인 편집 금지.** `~/.claude/codex-prompt-template.md`·`~/.claude/CLAUDE.md` 같은 전역 자산은 반드시 diff 제안 → 사용자 승인 → 적용. 무인 자가편집은 드리프트/자산 손상을 부른다. (auto-mode classifier도 CLAUDE.md 자가수정을 차단하므로 사용자 승인이 구조적으로 필수다.)
- **`--model` 절대 전달 금지.** codex gpt-5.5는 게이트/용량 제한으로 일부 호출이 404/400으로 간헐 실패한다. 사용자는 gpt-5.5 유지를 택했다. 실패 시 동일 프롬프트 1회 재시도 → 그래도 안 되면 WebSearch fallback으로 전환하되 출처 미검증임을 명시한다.
- **추측 기반 "강화" 금지.** 템플릿 수정은 (a) 실제 로그 패턴 또는 (b) `references/search-sources.md`의 1차 출처 근거가 있을 때만. "이러면 더 좋을 것 같다"는 변경 금지.
- **단일 실패 1건을 patch하지 마라 — overfit 위험.** 변경은 "반복 패턴을 줄이는 generalized instruction"이어야 한다(로그 1건 대응용 특수 지시 금지). 근거: OpenAI evaluation flywheel(held-out test로 overfit 확인), prompt-optimizer(production 전 평가 — 특정 입력에서 원본보다 나빠질 수 있음).
- **변경이 기존을 깨지 않는지 확인.** 템플릿 diff 제안 시, 그 변경이 과거 잘 동작한 위임 유형(로그상)을 망가뜨리지 않는지 1패스 점검한다. 큰 재작성보다 작은 diff를 선호(리뷰 가능성·회귀 추적).
- **과한 절차 지시 금지.** gpt-5.5는 과한 `ALWAYS`/`NEVER`/단계 나열에서 overthinking·latency가 늘 수 있다. outcome·constraints·done/verification만 선명하게(근거: gpt-5 troubleshooting guide).
- **스탬프 없이 템플릿 바꾸지 마라.** 템플릿을 수정하면 상단 `template_version`을 올리고(날짜+letter, 예 `2026-06-08-c`) 변경이력 한 줄을 출처와 함께 추가한다.
- **로그 0건이면 SKIP.** window 안에 새 codex 로그가 없으면 억지 개선을 만들지 마라. 방법론만 리서치하고 싶으면 `research-only` 인자로 명시 호출했을 때만 진행한다.
- **로그는 verbatim 보존 자산 — 편집/요약 금지.** 훅이 쓴 `~/.claude/codex-research-log/*.md`의 기존 엔트리를 고치거나 지우지 마라. 읽기 전용 신호다.

## 입력

- `window` (optional): 분석 대상 기간. 기본 `14d`. 주 1회 운영이면 `7d`도 가능.
- `research-only` (optional): 로그 분석을 건너뛰고 방법론 리서치 + 템플릿 GAP만 수행. 로그 0건일 때 또는 OpenAI 가이드 변경 반영 시 사용.

## Process

### 1. 신호 수집 (로그 분석)

1. `~/.claude/codex-research-log/*.md`에서 `window` 범위 내, `— codex-rescue (auto-harvested)` 마커가 있는 엔트리를 나열한다.
2. 0건이면: `research-only` 호출이 아닌 한 SKIP하고 종료(억지 개선 금지).
3. 각 엔트리에서 추출: 보낸 프롬프트, codex 응답(verbatim), `web_search calls` 수, model.
4. 리뷰 시점 독립 평가로 아래 약점 패턴을 집계한다(위임 시점 self-score 아님):
   - **Contract 미준수**: 요청한 출력 구조(관찰사실/권장안/트레이드오프/열린질문 등)를 응답이 빠뜨린 비율.
   - **Grounding 약함**: URL 없는 주장, 날조 의심, 추측을 추측으로 표시 안 함.
   - **Fallback 빈도**: WebSearch fallback / "출처 미검증" 표기 / 404·400 게이트 실패가 반복되는가.
   - **Scope 위반**: read-only 요청인데 `--write`로 편집했거나, unrelated 작업이 한 run에 섞임.
   - **반복 약점**: 여러 엔트리에 공통으로 나타나는 실패 모드(이게 개선 1순위).
5. 분류는 RAG/리서치 실패 taxonomy(references C)를 기준으로 태깅한다: `unsupported_claim · hallucinated_citation · retrieval_miss · low_precision_context · incomplete_coverage · outdated · contract_noncompliance · oververbose · reasoning_error · tool_error`. 각 약점 엔트리에 태그 + 로그 위치를 남긴다.
6. **평가는 독립적으로.** 이 평가를 codex(피평가 모델)에게 자가채점시키지 마라 — self-preference 편향이 실증됐다(references C: arxiv 2404.13076, 2402.11436). 평가는 메인 스레드(다른 모델 family)가 리뷰 시점에 rubric으로 수행한다.

### 2. 방법론 리서치 (research the research method)

식별된 약점 모드에 대해 **gpt-5.5 기준 현재 prompting 베스트 프랙티스**를 조사한다. 어느 출처를 볼지는 `references/search-sources.md`(OpenAI 공식 docs 9종 + 신뢰 기준)를 따른다 — 약점 모드에 매핑되는 소스만 골라 읽고, 전체를 매번 읽지 마라.

리서치로 검증된 핵심 패턴(소스는 search-sources.md):
- **Output contract**: codex CLI는 `codex exec --output-schema schema.json -o result.json`로 JSON Schema를 강제할 수 있다(프롬프트 contract만이 아님). 단 `--json` 스트림의 중간 `agent_message`도 schema-shaped일 수 있으니 최종 turn/`-o` 파일 기준 + 외부 validator 1회 유지.
- **reasoning effort**: gpt-5.5 기본 `medium`. 단순 리서치/분류는 `low`부터, `none`은 latency-critical일 때만, 복잡 구현은 eval로 품질 확인 후에만 `high`/`xhigh`.
- **Grounding**: supporting source만 cite, source ID/URL 발명 금지, 근거 없는 추론은 `추론:` 라벨, 미확인은 열린 질문으로.
- **Stop/retrieval**: 넓게 시작 → 충돌·공백 시만 재검색 → 충분하면 중단. `max_search_rounds`·`max_sources_per_claim`·early-stop 조건을 명시(overthinking·latency 방지).
- **read-only vs write 분기**: research는 `observed facts/recommendations/tradeoffs/open questions` + claim별 URL. implement는 `allowed files/forbidden actions/test command/definition of done/rollback` + citation보다 재현 가능한 verification log 우선.

1. **Context7** — OpenAI/모델 관련 공식 문서가 있으면 우선 조회.
2. **Codex (codex-rescue, read-only)** — 웹 리서치 위임. `MODE=research`, `--write` 금지, "research" 키워드 포함. 대상: OpenAI 공식 prompt-guidance, latest-model 가이드, output-contract/grounding 패턴.
3. codex 게이트 실패 시 1회 재시도 → WebSearch fallback(출처 미검증 명시). `--model` 금지.
4. arXiv 직접 PDF는 실패할 수 있으니 `arxiv.org/abs/` abstract 페이지 사용.

> circular 주의: codex는 개선 대상이자 리서치 도구다. 외부 베스트 프랙티스를 **read-only로** 가져오는 용도로만 쓰고, codex가 자기 템플릿을 자평하게 하지 마라.

### 3. GAP 분석

현재 `~/.claude/codex-prompt-template.md`를 (Step 1 약점 패턴 + Step 2 리서치 결과)와 대조하여 구체 갭을 enumerate한다:
- 로그에서 반복되지만 템플릿이 막지 못하는 실패 모드.
- 리서치가 권장하지만 템플릿에 없는 지시/블록.
- 더 이상 유효하지 않은(모델 세대가 바뀐) 기존 지시.

각 갭은 (a) 근거(로그 엔트리 또는 출처 URL) (b) 제안 수정 (c) 영향 범위(어느 MODE/블록) 3요소를 포함한다.

### 4. 개선 diff 제안 (승인 게이트)

1. 갭별로 `codex-prompt-template.md`(및 필요 시 `CLAUDE.md` 위임 규칙 / settings.json codex 리마인더)에 대한 **구체 diff**를 작성해 사용자에게 제시한다.
2. **파일에 적용하지 않는다** — 승인 대기.
3. 각 diff에 근거 한 줄(어느 로그 패턴 / 어느 출처가 이 변경을 정당화하는지) 첨부.
4. **변경 크기 제한**: 한 사이클은 주로 1개 실패유형 또는 작은 rubric 명확화만 다룬다(과적합 방지). 큰 재작성은 분할.
5. **회귀 1패스 점검(held-out)**: 제안 변경이 과거 잘 동작한 위임 유형(로그상)을 망가뜨리지 않는지 대조한다. 의심되면 그 위임 유형을 diff 근거에 명시하고 보수적으로 축소.

### 5. 적용 + 스탬프 (승인 후에만)

1. 승인된 diff를 파일에 적용.
2. `template_version`을 올리고(날짜+letter) 변경이력 한 줄 추가 — 출처 URL 또는 "로그 N건 패턴" 근거 명시.
3. CLAUDE.md/settings.json도 바꿨으면 함께 보고.

### 6. 기록

별도 ledger 없음. 템플릿 상단 changelog 라인이 곧 기록이다. 이번 사이클에서 무엇을 근거로 무엇을 바꿨는지(또는 "개선 없음")를 한 문단으로 사용자에게 요약한다.

### 7. 완료 전 규칙 전수 대조 (rule-by-rule audit)

완료 선언 전에 이 스킬의 Gotchas + 안티패턴을 한 항목씩 자기 대조한다:
- 위임 시점 self-score를 부활시키지 않았는가 / 전역 자산을 승인 없이 편집하지 않았는가 / `--model`을 넘기지 않았는가 / 단일 실패 1건 patch가 아니라 generalized instruction인가 / 모든 변경에 로그·1차 출처 근거가 있는가 / 템플릿 변경 시 `template_version` 스탬프를 올렸는가.
- 하나라도 위반이면 적용을 멈추고 수정한다. 이 대조 결과를 사이클 요약에 1줄로 명시한다.

## 주기 운영

주 1회 수동 호출 또는 `/schedule`로 등록한다. 스케줄 등록 시 프롬프트 예: `/codex-kaizen window=7d`. 로그가 비면 자동 SKIP되므로 빈 주에는 noise가 없다.

## 안티패턴 (하지 말 것)

- 위임 시점 self-score를 부활시키지 마라.
- 로그 0건인데 `research-only` 없이 억지 개선안을 만들지 마라.
- 전역 자산을 승인 없이 편집하지 마라.
- `--model`을 codex에 넘기지 마라.
- 추측만으로 템플릿을 "강화"하지 마라 — 로그 또는 1차 출처 근거 필수.
- reflect-kaizen의 reflection/ledger 이슈를 이 리포트에 섞지 마라.

## 관련 파일

- `~/.claude/hooks/harvest-codex-log.sh` — 신호를 자동 수집하는 Stop 훅(개선 대상 아님, 신호원).
- `~/.claude/codex-research-log/*.md` — verbatim 로그(읽기 전용 신호).
- `~/.claude/codex-prompt-template.md` — 개선 대상 템플릿(`template_version` 스탬프 보유).
- `~/.claude/CLAUDE.md` "Codex 위임 규칙" — 위임 프로토콜(승인 후에만 수정).
