# 검색 소스 및 신뢰도 기준

> contract-kaizen 전용 리서치 소스. 계약 설계 11개 + 자기개선 6개 도메인.

## 소스 분류

### 학술 (계약 설계)

- **검색 대상:** arXiv, ACL Anthology, IEEE Xplore, Semantic Scholar
- **키워드:** behavior-driven development BDD, acceptance test driven development ATDD, specification by example, design by contract DbC, formal specification TLA+ Alloy, requirements engineering IEEE 29148, LLM formal specification, property-based testing QuickCheck, GQM goal question metric, checklist defect prevention Fagan, consumer-driven contract testing Pact, NASA requirements writing
- **우선순위:** BDD/Gherkin(1), Requirements Engineering(2), Design by Contract(3) — 피드백 0건 시 이 상위 3개만 리서치

### 학술 (자기개선)

- **검색 대상:** arXiv, NeurIPS/ICLR/ACL proceedings
- **키워드:** LLM self-refine reflection, meta-learning learning to learn, retrospective post-mortem analysis, PDCA continuous improvement, LLM self-correction limits, experience replay feedback reuse
- **범위:** 2024-현재

### 공식

- **검색 대상:** Anthropic (docs, blog, research), OpenAI (cookbook, blog), Google (research, Vertex docs)
- **키워드:** prompt engineering best practices, specification, acceptance criteria, quality gates, agentic workflow
- **후속:** 변경 로그 / 릴리스 노트 확인

### 커뮤니티

- **검색 대상:** GitHub trending, Simon Willison blog, Lilian Weng blog, Eugene Yan blog
- **키워드:** contract testing, specification driven development, BDD tooling, requirement quality
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
