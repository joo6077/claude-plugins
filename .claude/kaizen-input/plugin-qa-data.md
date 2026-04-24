# Plugin QA Data (Aggregated from 5 projects + global ~/.harness/)

Generated: automated aggregation from 138 evaluator feedbacks + 34 contract feedbacks.

## Global stats

- Total evaluations: 138
- APPROVE / REJECT split: see per-plugin below
- Sources: ~/.harness/feedback/{evaluator,contract}/*.yaml, .harness/ in 5 projects (apps, claude-plugins, fit-pal, flutter_playwright, iyaki-zip-dev)

## Per-plugin breakdown

### harness

- APPROVE: 77
- REJECT: 61
- Reject rate: 44%

**Top reject reasons:**

- SK-02: Neubrutalism 모달 .ms-card-action box-shadow offset 3px (기준: 4px+), .ms-badge box-shadow offset 2px (기준: 4px+)
- H-01: rust-init/rust-feature Gotchas에 domain event + outbox 원칙 누락
- H-03: rust-api Gotchas에 Composition Root 단일화 원칙 누락
- 미검증 항목 3개 (LG-02, DG-03, DG-04) — 미검증 2개 이상 REJECT 규칙 적용
- LG-02: 시각적 Figma 대조 불가 (mcp_server: null)
- DG-04: 런타임 에러 확인 불가 (mcp_server: null)
- AR-03: backend-kit/infra-kit README.md 누락
- AR-04: backend-kit/infra-kit evals/ 디렉토리 누락
- SK-07: infra-kit/skills/infra-audit/SKILL.md Step 3 내용 비어있음
- SK-08: infra-kit/skills/infra-init/SKILL.md Step 3 내용 비어있음

**Top improvement suggestions:**

- SK-02 계약 조건을 '주요 interactive element(버튼, 카드, 입력)의 shadow'로 범위를 명시하거나, badge/decoration shadow는 예외로 명기할 것
- H-01/H-03 누락 패턴: 동일 개념이 rust-service에는 있고 rust-init/rust-api에는 없는 불일치. 카이젠 체크리스트에 '동일 원칙이 여러 스킬에 일관되게 적용되었는가' 크로스체크 추가 권장
- DG-01 조건을 '미완성 placeholder' 로 명확히 표현하면 해석 모호성 제거 가능
- mcp_server 설정 시 LG-02, DG-04 자동 검증 가능
- widget_test.dart MyApp 컴파일 에러 수정 필요 (기존 문제)
- FigmaDecoration unit test 추가 시 DG-03 확실한 PASS 가능
- markdownlint를 프로젝트 devDependency로 추가하면 I-05를 L3 검증 가능
- DG-04 런타임 검증을 위해 MCP 서버 설정 권장
- pubspec.yaml dependency 정렬 수정 권장
- 신규 feature 시작 전 sprint-contract를 갱신하면 QA 정확도가 높아진다

### design-kit

- APPROVE: 0
- REJECT: 5
- Reject rate: 100%

**Top reject reasons:**

- SK-05: design-concept 스킬에 이전 단계 산출물(concept.md) 자동 로드 프로세스 단계 없음. 계약은 3개 스킬 모두를 요구한다.
- SK-05: design-component 프로세스에 자동 로드 독립 Step 없음 — 자동 감지 섹션이 프로세스 Steps 외부에 위치하여 계약의 '프로세스 단계' 요건 미충족
- PH-01: agent-design-guide.md에 계약 모호성 방지 원칙 누락 (skill-design-guide.md §3.5 대응 항목 없음)
- I-02: Working tree modified 2건 (.harness/sprint-contract.md, .harness/.meta/kaizen-data-pool.md) — 계약 'modified 0건' 미충족
- AR-01: design-mockup/templates/mockup.html이 계약 기준인 .md 패턴(design-tokens.md, audit-report.md)과 구조적으로 다른 HTML 형식
- AR-06: 스펙 스켈레톤 :root CSS 변수가 기존 design-kit HTML 파일 값과 불일치 (--bg2, --surface, --surface2, --surface3, --text, --text2 6개 변수). 스펙 본문의 재사용 지시와 스켈레톤 값이 내부 모순.

**Top improvement suggestions:**

- 구현 전 스펙 리뷰 시 계약 조건 중 구현 후 판정 대상을 명확히 분류하는 프로세스를 sprint-contract에 추가할 것을 권장
- design-concept SK-05 FAIL: 프로세스에 기존 concept.md 존재 시 로드/수정 모드 분기를 추가해야 한다
- design-component 프로세스 Step 0 추가로 자동 감지 로직을 독립 단계로 분리 — 1줄 단위 수정
- 이전 REJECT 5건 반영 모두 확인됨. 잔여 FAIL 1건 수정 후 스펙 수준 APPROVE 가능
- I-02 계약을 'QA sprint-contract 생성 및 E-08 명령 실행 제외하여 modified 0건' 또는 '.harness/ 이외 modified 0건'으로 범위 명확화
- PH-01 완료 시 agent-design-guide.md §xx 계약 모호성 방지 원칙 추가
- PH-05 infra-kit/references 파일 내용(principle-index, audit-criteria, init-checklist)이 계약에서 요구하는 기준을 충족하는지 L3 검증 추가 권장
- 계약 AR-01에 HTML 템플릿 예외 조건 추가 권장
- HTML 산출물 스킬에 대한 템플릿 패턴 기준을 별도로 정의할 것
- SK-03, SK-04, AR-02, AR-03은 구현 완료 후 L3 재검증 필요

### react-kit

- APPROVE: 1
- REJECT: 4
- Reject rate: 80%

**Top reject reasons:**

- DG-01: react-feature/SKILL.md(5건)와 react-widget/SKILL.md(2건)에서 코드 템플릿 내 TODO 7건 발견 — 계약 0건 조건 불충족
- DG-02: react-init/SKILL.md line 178, 190 코드블록 언어 힌트 누락
- AP-01: react-form Gotchas에 Zustand/TanStack Query 상태 분리 원칙 미명시
- RE-02: react-api의 트리거 키워드 '"API 연동"'이 react-feature의 '"API 연동 화면"'과 부분 중복 — 배타성 위반
- DG-02: 5개 파일 모두에서 언어 힌트 없는 fenced code block 존재 (react-run 2개, react-build 3개, react-preflight 3개, react-audit 4개+, react-reviewer 6개+)
- SK-05: react-run/SKILL.md:5의 트리거 키워드 'wasm-pack 빌드'가 react-wasm/SKILL.md:5와 중복. 기존 17개 스킬과 상호 배타 불충족
- RE-02: 21개 스킬 트리거 키워드 상호 배타 불충족 (react-run vs react-wasm 'wasm-pack 빌드' 겹침)

**Top improvement suggestions:**

- DG-01: 계약에 생성 코드 템플릿 내 TODO 예외 추가, 또는 코드 템플릿 TODO를 일반 주석으로 교체
- DG-02: react-init/SKILL.md의 언어 힌트 없는 코드블록 2개를 ```text로 수정
- AP-01: 폼 관련 스킬에도 상태 분리 원칙 Gotcha를 명시하도록 계약 조건에 '폼 포함' 명시 권장
- RE-02: 트리거 키워드 배타성 계약 시 부분 문자열 포함 여부도 명시 권장
- DG-02 조건에 '모든 opening fence'라는 표현을 더 명확히 명시하면 구현자가 닫는 fence와 혼동하지 않을 것
- Iter 1에서 Grep 교차 중복 확인 시 동일 문자열 트리거 키워드까지 스캔하지 않아 SK-05/RE-02 겹침을 미탐지. 다음 평가에서 description 트리거 키워드를 정규식으로 추출 후 set intersection으로 정확 비교 필요
- react-test Gotcha에 cleanup() 자동 동작 항목 추가 검토 (소스 §1.8 기재 있음)

### infra-kit

- APPROVE: 0
- REJECT: 4
- Reject rate: 100%

**Top reject reasons:**

- AR-03: backend-kit/infra-kit README.md 누락
- AR-04: backend-kit/infra-kit evals/ 디렉토리 누락
- SK-07: infra-kit/skills/infra-audit/SKILL.md Step 3 내용 비어있음
- SK-08: infra-kit/skills/infra-init/SKILL.md Step 3 내용 비어있음
- SK-13: .claude/skills/backend-kaizen, infra-kaizen References 섹션 누락
- SKILL.md:218 체크리스트에서 overview.html을 요구하나, SKILL.md:201 Phase 7.2는 'overview로 묶지 마라'로 금지함 — 내부 모순. 실제 docs/backend-kit/, docs/infra-kit/에 overview.html 미존재 확인
- PH-01: agent-design-guide.md에 계약 모호성 방지 원칙 누락 (skill-design-guide.md §3.5 대응 항목 없음)
- I-02: Working tree modified 2건 (.harness/sprint-contract.md, .harness/.meta/kaizen-data-pool.md) — 계약 'modified 0건' 미충족
- ER-01: run-evals.py가 evals.json 파싱 실패 시 exit code 0으로 정상 종료 — 비정상 종료 코드 미반환
- AR-04: backend-kit/README.md, infra-kit/README.md 스킬 테이블에 backend-test, infra-test 미등록

**Top improvement suggestions:**

- 신규 feature 시작 전 sprint-contract를 갱신하면 QA 정확도가 높아진다
- l3_unreached: 리서치 문서 20개 중 2개만 L3 검증. 나머지 18개는 L1/L2 수준. 시간 제약으로 샘플링했으나 추후 전수 확인 권장
- SKILL.md:218의 'docs/{kit-name}/overview.html + index.html 등록' 항목을 'docs/{kit-name}/ HTML 페이지 N개 존재 (리서치 문서 수와 동일) + index.html 등록'으로 수정
- I-02 계약을 'QA sprint-contract 생성 및 E-08 명령 실행 제외하여 modified 0건' 또는 '.harness/ 이외 modified 0건'으로 범위 명확화
- PH-01 완료 시 agent-design-guide.md §xx 계약 모호성 방지 원칙 추가
- PH-05 infra-kit/references 파일 내용(principle-index, audit-criteria, init-checklist)이 계약에서 요구하는 기준을 충족하는지 L3 검증 추가 권장
- ER-01 수정: load_evals에서 JSONDecodeError 시 sys.exit(2) 추가
- AR-04 수정: sync-docs.py backend-kit infra-kit 실행

### rust-kit

- APPROVE: 0
- REJECT: 3
- Reject rate: 100%

**Top reject reasons:**

- H-01: rust-init/rust-feature Gotchas에 domain event + outbox 원칙 누락
- H-03: rust-api Gotchas에 Composition Root 단일화 원칙 누락
- SK-03: rust-api 핸들러 패턴 예시에서 PgPool 직접 사용 — trait 추상화 없이 인프라 직접 참조
- AR-02: 계획 파일 Goal/리서치 문서 섹션의 '17개' vs 스펙의 '20개' 불일치
- AP-02: 스펙 20개 vs 계획 17개 리서치 문서 수 불일치 (AR-02와 동일 원인)
- AR-03: docs/flutter/ 1498줄 (목표 >=1500, 2줄 부족)
- AR-05: rust-kit templates/ 5개 파일이 rust-kit/skills/ SKILL.md에서 미참조

**Top improvement suggestions:**

- H-01/H-03 누락 패턴: 동일 개념이 rust-service에는 있고 rust-init/rust-api에는 없는 불일치. 카이젠 체크리스트에 '동일 원칙이 여러 스킬에 일관되게 적용되었는가' 크로스체크 추가 권장
- 계획 파일의 숫자 불일치(17 vs 20)를 수정하면 AR-02와 AP-02 동시 해결
- SK-03 해결을 위해 rust-api 핸들러 예시를 trait 기반 DI 패턴으로 교체
- Gotchas 카운팅 시 H1/H2 형태를 모두 고려하는 범용 정규식 사용
- 경계값 조건(>= N)은 즉시 측정값 출력 후 비교

### backend-kit

- APPROVE: 0
- REJECT: 3
- Reject rate: 100%

**Top reject reasons:**

- AR-03: backend-kit/infra-kit README.md 누락
- AR-04: backend-kit/infra-kit evals/ 디렉토리 누락
- SK-07: infra-kit/skills/infra-audit/SKILL.md Step 3 내용 비어있음
- SK-08: infra-kit/skills/infra-init/SKILL.md Step 3 내용 비어있음
- SK-13: .claude/skills/backend-kaizen, infra-kaizen References 섹션 누락
- SKILL.md:218 체크리스트에서 overview.html을 요구하나, SKILL.md:201 Phase 7.2는 'overview로 묶지 마라'로 금지함 — 내부 모순. 실제 docs/backend-kit/, docs/infra-kit/에 overview.html 미존재 확인
- ER-01: run-evals.py가 evals.json 파싱 실패 시 exit code 0으로 정상 종료 — 비정상 종료 코드 미반환
- AR-04: backend-kit/README.md, infra-kit/README.md 스킬 테이블에 backend-test, infra-test 미등록

**Top improvement suggestions:**

- 신규 feature 시작 전 sprint-contract를 갱신하면 QA 정확도가 높아진다
- l3_unreached: 리서치 문서 20개 중 2개만 L3 검증. 나머지 18개는 L1/L2 수준. 시간 제약으로 샘플링했으나 추후 전수 확인 권장
- SKILL.md:218의 'docs/{kit-name}/overview.html + index.html 등록' 항목을 'docs/{kit-name}/ HTML 페이지 N개 존재 (리서치 문서 수와 동일) + index.html 등록'으로 수정
- ER-01 수정: load_evals에서 JSONDecodeError 시 sys.exit(2) 추가
- AR-04 수정: sync-docs.py backend-kit infra-kit 실행

### flutter-toolkit

- APPROVE: 0
- REJECT: 2
- Reject rate: 100%

**Top reject reasons:**

- I-01: Fix commit 5f2f894 push 미완료 — git log origin/main..main 1건
- I-02: 예외 3항목 외 modified 파일 존재 (sprint-feedback.md, flutter-toolkit/README.md, history 아카이브)
- create-kit Gotcha #2 위반 — 3종 스킬 패턴 대신 17종 워크플로우 패턴 선택 (P1-02)
- ops/ 리서치 문서 수 불일치 — ci-cd.md, observability.md 처리 미결 (S2-02)
- principle-index.md 누락 — guide 스킬 미설계로 인한 cascade 이슈 (P1-05)
- Tokio 1.50 버전 검증 필요 — 존재하지 않는 버전일 가능성 (T4-03)
- axum-tungstenite deprecation 미검증 — axum 0.8 내장 WebSocket 존재 (T4-05)
- 검증 스크립트 수치 미확정 — S2-02 불일치 반영 안 됨 (P3-06)
- references/principle-index.md 구조 불완전 (S2-05)

**Top improvement suggestions:**

- I-02 예외 목록에 sprint-feedback.md, sync-docs 갱신 파일, history 아카이브 디렉토리를 포함 명시하면 다음 iteration에서 해소 가능
- I-01 조건은 git push 실행만으로 해소 가능 — 계약 자체 이슈 아님
- create-kit Gotcha #2에 flutter-toolkit형 워크플로우 킷 허용 여부를 명시하면 향후 유사 설계에서 모호성 제거 가능
- 기술 버전 명시 시 Codex 리서치를 먼저 수행하여 실제 최신 버전을 사용할 것

### reflect-kit

- APPROVE: 0
- REJECT: 2
- Reject rate: 100%

**Top reject reasons:**

- SC-05: git tag reflect-kit/v0.2.0 로컬 미생성 (git tag -l 결과 없음)
- AP-01: README.md 라인 7 '버전: 0.1.0' 하드코딩 — plugin.json v0.2.0과 불일치
- ER-01: log-reflection.sh에 _lib-redact.sh source 및 redact_sensitive() 호출 누락 — 보안 위험
- SK-06: reflect-digest/SKILL.md에 Gotchas 섹션과 Process 섹션 미존재
- AP-03: reflect-kit/docs/DESIGN.md:5 bare code fence (언어 힌트 없음)
- SK-04: 계약 'ULID 기반 rule_id' vs 구현 'UUID(uuidgen)' 불일치
- RE-01: _lib-redact.sh가 log-reflection.sh에서 미source — 세 훅에서 공통 source 조건 미충족

**Top improvement suggestions:**

- SC-05 DEFERRED 조건 설명에 로컬 태그 생성 여부를 별도 체크포인트로 명시 — DEFERRED는 원격 push만 해당함을 계약에 명확히
- AP-01: README 버전을 plugin.json에서 동적으로 읽거나, sync-docs.py가 버전 동기화 체크 항목 추가 검토
- SK-04 조건의 ULID/UUID 표현을 구현 의도에 맞게 통일할 것을 계약 수정 권장

