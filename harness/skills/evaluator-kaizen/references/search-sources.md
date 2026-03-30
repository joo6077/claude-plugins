# 검색 소스 및 신뢰도 기준

> evaluator-kaizen 전용 리서치 소스. 평가 방법론 12개 + 자기개선 6개 도메인.

## 소스 분류

### 학술 (평가 방법론)

- **검색 대상:** arXiv, ACL Anthology, IEEE Xplore, ACM Digital Library, Semantic Scholar
- **키워드:** test oracle problem LLM, LLM-as-a-judge evaluation bias, rubric-based LLM evaluation CheckEval, multi-agent verification consensus, metamorphic testing oracle, mutation testing LLM, independent verification validation IV&V, Fagan inspection perspective-based reading, symbolic execution concolic testing LLM, N-version programming diverse redundancy, evidence-based software engineering, automated code review AI-assisted
- **우선순위:** LLM-as-a-Judge(1), Rubric-Based Evaluation(2), Test Oracle Problem(3) — 피드백 0건 시 이 상위 3개만 리서치

### 학술 (자기개선)

- **검색 대상:** arXiv, NeurIPS/ICLR/ACL proceedings
- **키워드:** LLM self-refine reflection, meta-learning learning to learn, retrospective post-mortem analysis, PDCA continuous improvement, LLM self-correction limits, experience replay feedback reuse
- **범위:** 2024-현재

### 공식

- **검색 대상:** Anthropic (docs, blog, research), OpenAI (cookbook, blog), Google (research, Vertex docs)
- **키워드:** LLM evaluation, judge model, automated review, code verification, quality assurance
- **후속:** 변경 로그 / 릴리스 노트 확인

### 커뮤니티

- **검색 대상:** GitHub trending, Simon Willison blog, Lilian Weng blog, Eugene Yan blog
- **키워드:** LLM judge, automated QA, code review tools, evaluation frameworks
- **후속:** star 수 + 최근 커밋으로 신뢰도 판단

## 신뢰도 기준

| 유형 | 신뢰도 | 태그 | 비고 |
|------|--------|------|------|
| 학회 논문 (peer-reviewed) | 높음 | — | NeurIPS, ICLR, ACL, EMNLP, ICSE, FSE |
| 공식 블로그/문서 | 높음 | — | Anthropic, OpenAI, Google |
| arXiv preprint | 중간 | `[preprint]` | 인용 수 확인 |
| 엔지니어 블로그 | 중간 | `[blog]` | 저자 신뢰도 확인 |
| GitHub trending | 중간 | `[community]` | star + 활동성 확인 |
| 일반 블로그/포럼 | 낮음 | `[unverified]` | 교차 검증 필수 |

## 최신성 기준

- 6개월 이내: 현행
- 6-12개월: `[dated: YYYY-MM]` 태그 부착
- 12개월 초과: 기본 원칙이 아니면 폐기

## 중복 방지

- `docs/kaizen/research-log.md`에서 이미 조사한 URL 확인
- 동일 URL은 재조사하지 않음 (6개월 이상 경과 시 예외)
