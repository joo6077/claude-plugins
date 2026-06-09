# Codex Kaizen — 권위 소스 + 리서치 기준

이 스킬의 Step 2(방법론 리서치)에서 참조하는 1차 출처 목록과 신뢰도 기준이다.
추측 기반 템플릿 변경을 막기 위해, 개선안은 (a) 실제 codex 로그 패턴 또는 (b) 아래 소스 중 하나에 근거해야 한다.

> 출처 수집: 2026-06-08 codex-rescue read-only 리서치 3회 + WebFetch 검증(arXiv 4종 제목·저자 대조 통과). 6개월 경과 시 `[dated: YYYY-MM]` 태그 후 재확인.

## 목차
- (A) gpt-5.5 / OpenAI reasoning 모델 prompting
- (B) Codex CLI 위임 (sandbox · structured output)
- (C) 평가 방법론 — LLM-as-judge 편향 · self-score 신뢰성 · 리서치 실패 taxonomy
- (D) prompt kaizen / 로그 기반 개선 루프
- 미확인 (열린 질문)
- 리서치 운영 규칙

## (A) gpt-5.5 / OpenAI reasoning 모델 prompting

| URL | 무엇을 / 왜 신뢰 |
|-----|------------------|
| https://developers.openai.com/api/docs/guides/prompt-guidance?model=gpt-5.5 | **GPT-5.5 공식 prompting guide.** "outcome-first prompts > process-heavy stacks", define outcome/what-good-looks-like/constraints/evidence/final answer 명시. 1차 출처 |
| https://developers.openai.com/api/docs/guides/latest-model | Using GPT-5.5 — outcome-first 재확인 |
| https://developers.openai.com/api/docs/models/gpt-5.5 | reasoning effort 지원값(`none/low/medium(default)/high/xhigh`) |
| https://developers.openai.com/api/docs/guides/reasoning | reasoning effort, "done 정의 + 검증 방법" 권장 |
| https://developers.openai.com/api/docs/guides/structured-outputs | output contract를 JSON Schema로 강제 |
| https://developers.openai.com/api/docs/guides/citation-formatting | supporting source만 cite, source ID/URL 발명 금지 |
| https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_troubleshooting_guide | overthinking 원인(과한 effort·done 부재·충돌 지시) + stop condition |
| https://openai.com/index/introducing-gpt-5-5/ | GPT-5.5 vs 5.4 1차 릴리스 노트 |

## (B) Codex CLI 위임 (sandbox · structured output)

| URL | 무엇을 / 왜 신뢰 |
|-----|------------------|
| https://developers.openai.com/codex/noninteractive | `codex exec` non-interactive — `--output-schema`(JSON Schema 준수 최종 응답) + `-o`(JSON 파일 출력) |
| https://developers.openai.com/codex/concepts/sandboxing | `exec` 기본 read-only sandbox, edit 시 `--sandbox workspace-write` |
| https://developers.openai.com/codex/permissions | approval/permission 모델 |
| https://github.com/openai/codex/issues/19816 | `--json` 스트림에서 중간 `agent_message`도 schema-shaped 가능 — 외부 validator 유지 권장(주의점) |

## (C) 평가 방법론 — LLM-as-judge 편향 · self-score · 리서치 실패 taxonomy

WebFetch로 제목·저자 검증 완료(2026-06-08).

| URL | 무엇을 / 왜 신뢰 |
|-----|------------------|
| https://arxiv.org/abs/2306.05685 | "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" — judge가 인간선호 80%+ 일치 가능하나 position/verbosity/self-enhancement 편향 명시 |
| https://arxiv.org/abs/2305.17926 | "Large Language Models are not Fair Evaluators" — 응답 순서만 바꿔도 평가 왜곡. randomized/balanced order 보정 제안 |
| https://arxiv.org/abs/2303.16634 | "G-Eval" — CoT+form-filling 평가, LLM이 LLM 생성물을 선호할 가능성 지적 |
| https://arxiv.org/abs/2404.13076 | "LLM Evaluators Recognize and Favor Their Own Generations" — self-preference의 인과(자기 출력 인식↔편애). **self-score 신뢰성 낮음의 직접 근거** |
| https://arxiv.org/abs/2402.11436 | "Pride and Prejudice: LLM Amplifies Self-Bias in Self-Refinement" — 6개 LLM에서 self-refine가 bias 증폭 |
| https://arxiv.org/abs/2309.15217 | "Ragas" — RAG를 retrieval/generation으로 분리 평가 |
| https://arxiv.org/abs/2408.08067 | "RAGChecker" — retrieval·generation 세분 진단 지표 |
| https://arxiv.org/abs/2510.13975 | "Classifying and Addressing the Diversity of Errors in RAG Systems" — RAG 오류 taxonomy + 주석 데이터셋(EACL 2026) |

## (D) prompt kaizen / 로그 기반 개선 루프

| URL | 무엇을 / 왜 신뢰 |
|-----|------------------|
| https://developers.openai.com/api/docs/guides/model-optimization | baseline eval → 대표 test data → eval feedback 기반 수정 → 반복 |
| https://developers.openai.com/api/docs/guides/prompt-optimizer | grader 의존, 최적화 prompt가 특정 입력에서 원본보다 나쁠 수 있음(production 전 평가·수동 리뷰 게이트) |
| https://developers.openai.com/cookbook/examples/evaluation/building_resilient_prompts_using_an_evaluation_flywheel | failure taxonomy→grader→held-out test로 overfit 확인 |
| https://developers.openai.com/api/docs/guides/prompting | 프롬프트를 application code처럼 versioned·git·PR review로 관리 |
| https://platform.claude.com/docs/en/test-and-evaluate/develop-tests | 성공 기준 측정 가능 정의, edge case 반영 eval, rubric 신뢰성 먼저 확인 |

## 미확인 (열린 질문 — references 단정 금지)

- "bounded change size(주당 실패 1유형/작은 diff)"의 직접 규정 1차 출처 미확인 — 현재는 OpenAI/Anthropic eval 문서에서의 추론.
- 같은 모델 family를 "독립 judge"로 볼 수 있는 충분조건 미확인 — 서로 다른 frontier model 간 독립성은 별도 검증.
- `codex exec resume --output-schema` 최신 지원 상태는 문서/릴리스 어긋날 수 있음 — 일반 `codex exec` 기준으로만 단정.
- 주간 업데이트 빈도·최소 held-out size·pass/fail threshold의 보편값은 도메인·위험도 의존, 확정 불가.

## 리서치 운영 규칙 (Step 2)

1. Step 1 로그 분석의 약점 모드에 매핑되는 소스만 골라 읽는다(전체를 매번 읽지 마라).
2. Context7에 OpenAI/Codex 문서가 있으면 우선, 없으면 codex-rescue(read-only)로 위 URL 확인.
3. codex gpt-5.5 게이트 실패 시 1회 재시도 → WebSearch fallback(미검증 명시). `--model` 금지.
4. arXiv는 `arxiv.org/abs/` abstract 페이지 사용. **새 인용은 WebFetch로 제목·저자 1회 검증 후** references 추가(codex가 ID를 오매핑할 수 있다 — 실제 발생 사례 있었고 검증으로 걸러짐).
