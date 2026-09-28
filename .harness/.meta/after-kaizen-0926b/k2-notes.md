# k2 — design · infra · backend · rust-kit 남은 것

- 계약: `.harness/sprint-contract-after-0926-kits-design-infra-backend-rust.md` (봉인 커밋 `279a7f8`,
  `conditions_digest: sha256:ae16a8a46b2e9244` · `measurement_digest: sha256:b861d90d33e48c2b`)
- 가지: `chore/ak2-k2`, 시작 커밋 `6378948`
- 위임: 2026-09-26T10:09:00.557Z · 결정 답 2026-09-26T10:30:16.222Z (세션 `bda55d45-296c-491f-89ba-b52042d58e72`)
- QA 1 회차 APPROVE(`.harness/sprint-feedback-after-0926-kits-design-infra-backend-rust.md`, 커밋 `cdc3fdc`). 독립 검토는 막을 결함 0 건, 막지 않는 어긋남 넷은 「남은 것」 에 옮겼다

## 항목별 결과

| ID | 결과 | 커밋 · 근거 |
| --- | --- | --- |
| KD-1 | 고침 | `0cfcb03` — 리뷰어 규칙 11 · 판정 틀 · 판정 규칙과 design-audit Step 5 가 L3 < 10/10 을 REJECT 로 낸다. 조건부 승인 갈래는 규칙 8 사본 한 줄에만 남는다(사본 검사 종료 코드 0) |
| KD-2 | 고침 | `0cfcb03` — 행간 기준이 `docs/design/foundations/typography.md` 의 라틴 1.4~1.6 · 한글 1.6~1.8 을 가리킨다. 옛 수치 세 자리(교차 진단이 찾은 `design-audit/SKILL.md` Step 2 표 포함)를 지웠다 |
| KD-3 | 고침 | `0cfcb03` · `87d08bc` — 다섯 자리가 숫자 대신 규약 §0 · §3 과 harness `skill-design-guide.md` §8.9 를 가리킨다. §8.9 는 gd 묶음(`.claude/worktrees/ak2-gd`)이 만드는 절이라 합친 뒤에야 실제로 열린다 |
| KD-4 OKLCH | 고침 | `0cfcb03` — design-system Gotcha 12 가 EX-13(`.harness/.meta/after-kaizen-0926b/ex/EX-13.md`, https://help.figma.com/hc/en-us/articles/360043042113-About-color-models) 원문대로 색 모델 다섯을 적고 「미지원」 단정을 뺐다 |
| KD-4 design-mockup Step 0 | 고침 | `0cfcb03` · `512ffae` — 자동 감지를 Step 0 으로 옮기고 Step 3 ~ 7 을 2 ~ 6 으로 당겼다. Gotcha 13 · 매트릭스 소절 · mockup-guidelines 참조도 새 번호다 |
| KD-4 §3.7 네 칸 | 고침 | `0cfcb03` — `visual-change-protocol.md` 「캡처 자체가 실패」 줄만 고쳤다. 리뷰어 출력 틀은 `09a0cde` 로 이미 처리됨(`design-reviewer.md:230`) |
| KD-4 `UNVERIFIED_ENV` | 처리됨 | `09a0cde` — `design-reviewer.md:65-75` 두 분류 · `env_gaps`, design-audit Gotcha 11 · Step 5, evals id 21 |
| KD-4 design:P2 | 넘김 | 규칙 방향을 바꾸는 일인데 `decisions.md` 에 사용자 결정이 없다 |
| KD-4 Material 3 | 바깥 근거 없음 | ex 폴더에 원문 대조가 없다 |
| KI-1 | 고침 | `a68db9d` — 사전 검사가 python3 · PyYAML 이 있으면 grep 을 요구하지 않는다. 네 환경 실측: E1 rc=0 · E2 rc=2 grep 부재 한 줄 · E3 rc=2 checkout 통과 · E4 rc=2 grep 부재 한 줄, 거짓 VIOLATION 0 |
| KI-2 | 고침 | `a68db9d` — 핀닝 규칙 오류 문구가 「YAML 읽기 실패」 이고 `docs/infra-kit/infra-test.html` 코드 사본도 원본과 글자 그대로 같다 |
| KI-3 | 고침 | `a68db9d` — 경로 표 다섯 파일에 raw 주소(`https://raw.githubusercontent.com/joo6077/claude-plugins/main/`)로 읽고 못 읽으면 못 읽었다고 적으라는 줄. 그 주소로 `docs/infra/platform/cicd.md` 가 200 |
| KI-4 판 번호 · `env_gaps` | 고침 | `a68db9d` — 연구 기록 `## [2026-09-26]` 절에 EX-8(`.harness/.meta/after-kaizen-0926b/ex/EX-8.md`, https://kubernetes.io/releases/) 대조, Kubernetes 최신판 1.37.1 → 1.37.0 정정. infra-audit 에 `env_gaps` 칸과 네 칸의 짝 한 줄 |
| KI-4 빠진 API · GitHub 밖 CI · 세 분류 규범 · 1.7+ | 바깥 근거 없음 | EX-8 은 판 번호와 날짜만 대조했다. 세 분류는 `docs/infra/platform/cicd.md` 원칙 7 이 이미 킷 규칙이라 적는다 |
| KB-1 OpenAPI 3.1 · AsyncAPI 3.1.0 | 고침 | `6d179cf` — 세 자리에 「3.1 이상 — 최소 지원선」. 연구 기록에 EX-7(`.harness/.meta/after-kaizen-0926b/ex/EX-7.md`, https://spec.openapis.org/oas/latest.html) 대조. 「AsyncAPI 3.0+」 은 참이라 두었다 |
| KB-1 시간대 저장 | 처리됨 | `backend-kit/skills/backend-system/SKILL.md:33` Gotcha 18 |
| KB-1 벽시계 문자열 | 바깥 근거 없음 | 근거 파일에도 ex 폴더에도 없다 |
| KR-1 | 고침 | `5a3277e` — 옛 실측 문장 세 자리가 크레이트 이름 없이 사건만 적는다. `rust-run` 예시 명령 두 줄은 그대로 |
| KR-2 | 고침 | `5a3277e` — `rust-init` 멤버 크레이트 이름이 `{project}-api` |
| KR-3 시각 종류 행 | 고침 | `5a3277e` — rust 감사 기준 `## 7. API Design` 에 「시각 종류별 저장」 행(sqlx-patterns 원칙 6), 카테고리 수 7 그대로 |
| KR-3 버전 값 · testcontainers | 고침 | `5a3277e` — utoipa 출처 · testcontainers 전제 칸 · rust-middleware Gotcha 2 · rust-init 4a · 4b · toml 템플릿이 Step 2c 표를 가리킨다 |
| KR-3 rust-model 타입 대응 | 처리됨 | `rust-kit/skills/rust-model/SKILL.md:39` · `:90` · `:240` (Phase 9) |

## 킷별 판 판단

| 킷 | 판 | 까닭 |
| --- | --- | --- |
| design-kit | minor | 감사 판정값에서 조건부 승인이 빠져 같은 입력의 판정이 바뀐다. design-mockup 단계 번호도 바뀐다 |
| infra-kit | patch | 골격이 grep 없이 멈추던 잘못을 고친 것이다. 규칙 · 판정값은 그대로다 |
| backend-kit | patch | 문구와 연구 기록뿐이다 |
| rust-kit | minor | 감사 기준에 FAIL 을 낼 수 있는 행이 하나 늘었다 |

판 올림 · 배포는 부모가 합친 뒤 한다.

## 다시 만들 문서 페이지

`python3 scripts/detect-docs-drift.py --since 6378948` 결과(스킬 파일은 이 도구가 대응시키지 않는다):

- `docs/design-kit/visual-change-protocol.html` — 「캡처 자체가 실패」 줄
- `docs/backend-kit/research-log.html` · `docs/infra-kit/research-log.html` · `docs/rust-kit/project-detection.html` — 도구가 「대응 HTML 없음, 신규」 로 적는다. 새로 만들지는 부모가 정한다

바뀐 낱말로 `docs/` 를 찾아 더한 것:

- `docs/design-kit/design-mockup.html` — Step 1 ~ 7 번호와 「Step 3-a」 (`:454` ~ `:597`). DC-15 와 함께 다시 만든다
- `docs/infra-kit/infra-test.html` — 이 계약이 코드 사본 · 표 한 줄을 직접 고쳤다(SC-02). 페이지 전체 재생성은 필요 없다

design-audit · design-system · design-reviewer · infra-audit · backend-audit · rust-audit 는 대응 페이지가 없다.

## 측정 도구

- 계약 측정 도우미: 계약 `## 회귀 게이트` 에서 뗀 `m.sh` (지문 `ed839ac28cacc62d`). 세션 사본 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/k2/m.sh`
- 로컬 CI: `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` (사본으로 돌림)
- markdownlint-cli2 0.23.2: 세션 스크래치 `k2/mdlint/`
- 교차 진단 반영: SK-02 에 `design-audit/SKILL.md` 를 넣고, AR-04 를 절 단위로 재게 바꿨다(봉인 전)

## 톤 대조

- tone-guide 1 단계: `Skill tone-kit:tone-guide` 호출 뒤 `.claude/tone-project.md`(어댑터 없음 · 주석 언어 ko)와 `core-comment.md` · `core-naming.md` · `core-structure.md` · `core-antipatterns.md` · `locale-korean.md` 를 Read 로 읽었다
- tone-guide 5 단계: 시작 커밋부터 가지 끝까지 `.harness` 밖에서 더한 줄 100 개를 대상으로 돌렸다

| 규칙 | 건수 | 판정 |
| --- | --- | --- |
| C-01 · C-02 (what 대신 why) | 0 | 통과 — 골격에 더한 주석 두 줄은 grep 을 언제 요구하는지(제약)를 적는다 |
| C-04 · F 구분선 | 0 | 통과 |
| C-13 자화자찬 | 0 | 통과 |
| C-15 주석 종결형 | 0 | 통과 |
| K-02 번역투 여섯 (G-1) | 0 | 통과 |
| K-04 · G-2 `합니다`체 | 0 | 통과 |
| K-11 새 이름 | 0 | 통과 — 「최소 지원선」 은 계약이 정한 문구이고 뜻이 바로 읽힌다 |
| N-07 fallback 접두사 | 0 | 통과 |
| N-08 한 글자 이름 | 2 | 위반 아님 — `infra-test/SKILL.md` 골격의 `for t in $CORE_TOOLS` 는 들여쓰기만 바뀐 기존 줄이고, 같은 골격의 도구 반복문(`:231`)이 같은 이름을 쓴다(S-12, 강도 SHOULD) |
| S-03 · S-04 추출 | 0 | 통과 — 새 함수를 만들지 않았다 |
| 쉬운 말 목록 | 1 | 고침 — 새로 쓴 「정본」 다섯 자리를 「기준 원본」 으로(`87d08bc`). 「클러스터」 · 「마이그레이션」 은 킷이 이미 쓰는 분야 낱말이라 두었다 |

## 남은 것

- backend-kit(`docs/backend/` 41 곳) · rust-kit(`docs/rust/` 4 곳)도 설치본에 `docs/` 가 없어 경로를 못 여는 같은 뿌리를 가진다. 이 계약은 infra-kit 만 고쳤다 — 같은 한 줄을 두 킷 경로 표에 넣을지 부모가 정한다
- `.claude/skills/docs-site/SKILL.md:112` 에 「line-height 1.2~1.6배」 가 남았다. 레포 전용 스킬이라 네 킷 묶음 밖이다
- KD-3 의 §8.9 인용은 gd 묶음의 새 절에 기대므로 두 가지를 합칠 때 절 번호가 바뀌었는지 확인한다. gd 도 `design-reviewer.md`(사본 3 항 번호 합침 `:70` · 규칙 12 `:116`)와 `design-audit/SKILL.md`(Gotcha 14 `:49`)를 고쳤다 — 이 계약이 고친 줄과 겹치지 않지만, 판정 문장에서 사본 조항 번호를 부르지 않게 적었다
- 이 계약의 근거 파일(`leftovers.md` · `decisions.md` · `ex/EX-7.md` · `EX-8.md` · `EX-13.md`)은 이 가지에는 없고 통합 가지 `chore/after-kaizen-0926b`(폴더 `after-0926b`)에서 추적된다(`ex/` 는 커밋 `77cfbd4`). 연구 기록이 적은 경로는 두 가지를 합친 뒤에 열린다. 형제 묶음이 다 끝나기 전에는 그 폴더를 지우지 않는다
- 독립 검토 1 — backend-kit 원칙 문서가 새 「최소 지원선」 문구와 반대로 읽힌다. `docs/backend/fundamentals/api-design.md:81` 이 「OpenAPI 3.2.1 스펙을 단일 소스로 유지한다」 고 적고, 그 문서를 원칙으로 삼는 `backend-kit/skills/backend-system/references/system-principles.md:21` 에는 조건 없는 「OpenAPI 3.1 JSON Schema 호환」 이 남았다. `docs/backend/research-log.md:14` 는 세 자리만 고쳤다고 적는다. 재현: `grep -rn "OpenAPI 3\.1\|3\.2\.1 스펙" backend-kit docs/backend/fundamentals`
- 독립 검토 2 — `design-kit/skills/design-mockup/SKILL.md:57` 새 Step 0 이 「같은 역할의 서로 다른 기존 화면」 으로 관례 표를 만들게 하는데, 대상 화면은 그 뒤 Step 1(`:66-68`)에서 정한다. 옮기기 전에는 대상을 먼저 정했다. Step 0 에 대상 확정을 앞당길지 부모가 정한다
- 독립 검토 3 — `infra-kit/skills/infra-guide/SKILL.md:27`(`docs/infra/operations/observability.md`) · `:31`(`docs/infra/platform/cicd.md`)이 `docs/infra` 경로를 직접 적는데 raw 주소 안내가 없어 설치본에서 못 연다. 재현: `grep -c raw.githubusercontent.com/joo6077 infra-kit/skills/infra-guide/SKILL.md` → 0. 위 첫 줄(backend · rust 경로 표)과 같은 뿌리라 함께 정한다
- KD-4 design:P2 는 사용자 결정 몫으로 넘긴다
- 계약 피드백 저장 때 `save-feedback.sh` 가 `project_hash` 를 `cf1be038` → `1a3bcba6` 으로 다시 계산했다(워크트리 대신 저장소 뿌리를 해시한 것으로 보인다). 저장 · 검증은 PASS

## 로컬 CI

`bash m.sh AR-03CI` (21:47 ~ 21:51, 가지 끝 `87d08bc` 판, 다른 `ci-local.sh` 가 끝난 뒤 사본으로 돌림) → `ci_ok=25 ci_other=0`. 시작 판 기준값과 같다(25 단계 rc=0, 나머지 한 줄은 `feedback-agg-test SKIP (yq 없음)`).

같은 판에서 `validate-plugin.py`(네 킷) · `check-reviewer-protocol-copies.py` · `sync-docs.py --check-only` · `sync-evals.py --check-only` · `check-stale-values.py` · `run-evals.py` · `run-kaizen-assertions.py` 가 모두 종료 코드 0 이다.
