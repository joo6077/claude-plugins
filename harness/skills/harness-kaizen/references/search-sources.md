# 검색 소스 및 신뢰도 기준

## 소스 분류

### 학술 논문
- **검색 대상:** arXiv, ACL Anthology, IEEE Xplore, Semantic Scholar
- **키워드:** LLM agent evaluation, prompt engineering, quality assurance, agentic workflow, tool use, multi-agent, code generation verification
- **범위:** 최근 6개월 우선, 핵심 논문은 기간 무관
- **후속:** 발견한 논문의 references 섹션에서 관련 논문 추적

### 공식 소스
- **Anthropic:** docs.anthropic.com changelog, anthropic.com/research, anthropic.com/engineering
- **OpenAI:** platform.openai.com/docs changelog, openai.com/research, cookbook
- **Google DeepMind:** deepmind.google/research, cloud.google.com/vertex-ai docs

### 커뮤니티/실무
- **GitHub:** trending repos — 키워드: agent, harness, prompt, evaluation, quality
- **블로그:** Simon Willison (simonwillison.net), Lilian Weng (lilianweng.github.io), Eugene Yan (eugeneyan.com)
- **컨퍼런스:** NeurIPS, ICLR, ACL, EMNLP — 최신 proceedings
- **Changelog 모니터링:** Anthropic, OpenAI, Google의 공식 블로그/docs 업데이트 추적

## 신뢰도 기준

| 유형 | 신뢰도 | 태그 | 비고 |
|------|--------|------|------|
| Peer-reviewed 논문 | 높음 | — | 가장 신뢰 |
| 공식 블로그/docs (Anthropic, OpenAI, Google) | 높음 | — | 최신성 높음 |
| arXiv preprint | 중간 | `[preprint]` | 미검증 논문 명시 필수 |
| 유명 엔지니어 블로그 | 중간 | `[blog]` | 실전 검증된 패턴 |
| GitHub trending | 중간 | `[community]` | 커뮤니티 검증 필요 |
| 일반 블로그/포럼 | 낮음 | `[unverified]` | 다른 소스로 교차 검증 필수 |

## 최신성 기준

- 6개월 이내: 최신으로 간주
- 6개월~1년: `[dated: YYYY-MM]` 태그 부착, 후속 연구 확인
- 1년 이상: 핵심 원칙이 아니면 폐기 검토

## 중복 방지

- 매 실행 시 `docs/kaizen/research-log.md`를 먼저 읽는다
- 이미 조사한 URL은 건너뛴다
- 단, 이전 소스의 업데이트(새 버전, 후속 논문, docs 변경)는 재조사한다
