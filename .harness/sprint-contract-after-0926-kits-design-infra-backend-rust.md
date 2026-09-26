---
feature: "카이젠 뒤 남은 것 — design · infra · backend · rust-kit (k2)"
slug: after-0926-kits-design-infra-backend-rust
created: "2026-09-26 21:20"
complexity: "복잡"
conditions: 28
status: active
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:ae16a8a46b2e9244
measurement_digest: sha256:b861d90d33e48c2b
locked_at: "2026-09-26 21:33"
---

## 배경

공통 전제 (모든 조건): Given 구현 커밋 · notes 커밋이 가지 `chore/ak2-k2` 에 다 올라갔고, 작업 폴더 `R=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-k2` 의 HEAD 가 그 가지 끝(`H`)이며
`git -C "$R" status --porcelain -- . ':(exclude).harness'` 가 빈 출력이다. 측정은 아래 `## 회귀 게이트` 의 도우미를 떼어 `TMPDIR=<빈 임시 폴더> bash m.sh <ID>` 로 돌리고, 출력이 조건에 적은 기대와 글자 그대로 같으면 PASS 다.
내용은 가지 끝 커밋에서 읽는다(`git show H:<경로>`). `UNRESOLVED` 가 나오면 판정하지 않고 멈춘다. 떼어 낸 도우미의 지문이 SK-01 아래 적은 값과 다르면 판정하지 않는다.

남은 일 목록 `leftovers.md`(통합 폴더 `.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/`, 기준 판 `6378948`)의
「## kit-design-kit」 KD-1 ~ KD-4, 「## kit-infra-kit」 KI-1 ~ KI-4, 「## kit-backend-kit」 KB-1, 「## kit-rust-kit」 KR-1 ~ KR-3 을 한 계약으로 묶는다.
작업 폴더는 `.claude/worktrees/ak2-k2`(가지 `chore/ak2-k2`, 시작 커밋 `63789486b72b8998be924fd54d56ae7465e76b21` = origin/main)다.

- 위임과 합의: 사용자 위임 2026-09-26T10:09:00.557Z 「123다실행해 그러면끝나?다음카이젠에왜넘기는데?」 · 결정 답 2026-09-26T10:30:16.222Z
  (세션 `bda55d45-296c-491f-89ba-b52042d58e72`, 원문은 같은 폴더 `decisions.md`). 그 전 위임 2026-09-24T04:04:16.964Z 「나한테 물어보지 말고 자동으로 끝까지」.
  이 계약의 합의는 이 위임으로 받은 것으로 적는다. 조건을 느슨하게 하는 개정은 이 위임으로 동의 처리하지 않는다 — 부모가 사용자에게 따로 묻는다
- 바깥 근거: Codex 원문 대조 결과 세 개만 쓴다. 저장소 경로는 합친 뒤 기준 `.harness/.meta/after-kaizen-0926b/ex/EX-<번호>.md` 다
  - EX-7 — OpenAPI 최신 3.2.1, 「3.1 지원 도구는 3.1.* 전부와 호환」(https://spec.openapis.org/oas/latest.html), AsyncAPI 3.1.0 은 2026-01-31 발표 · 기능 변경은 ROS 2 binding 추가(https://github.com/asyncapi/spec/releases/tag/v3.1.0)
  - EX-8 — Flux v2.9.5(2026-08-31, https://github.com/fluxcd/flux2/releases) · Argo CD v3.5.3(2026-09-14, https://github.com/argoproj/argo-cd/releases) ·
    Kubernetes 최신 1.37.0(2026-08-26) · 유지 판 1.37 · 1.36 · 1.35(https://kubernetes.io/releases/). 저장소 `docs/infra/research-log.md:23` 의 「v1.37.1 최신 안정판」 은 그 쪽에 없다고 판정됐다
  - EX-13 — Figma 도움말은 색 모델을 Hex · HSB · HSL · CSS · RGB 로 열거하고 OKLCH 를 넣지 않지만 「Variables 는 OKLCH 미지원」 이라 직접 단정하지는 않는다
    (https://help.figma.com/hc/en-us/articles/360043042113-About-color-models). Variables REST 의 원시 색은 0~1 범위 r · g · b · a 객체다
    (https://developers.figma.com/docs/rest-api/variables-types/)
- 이 계약이 정한 판단 넷(사용자 결정 파일에 없는 것 — 위임으로 계약 작성자가 정했다)
  - KD-1: 건너뛴 감사 카테고리(L3 < 10/10)는 v5.1 기준 원문 조항 3 의 「의도적으로 실행하지 않았으면 FAIL」 로 읽는다. design-kit 은 `CONDITIONAL APPROVE` 를 쓰지 않고 REJECT 로 판정한다.
    design-audit 리포트 틀(`templates/audit-report.md:6`)이 이미 `APPROVE|REJECT|BLOCKED` 셋뿐이라 두 쪽이 같아진다
  - KD-2: 행간 기준은 킷 원칙 문서 `design-kit/docs/design/foundations/typography.md` §줄 높이 · §한글 줄 높이 권장값 을 가리킨다. 문서 사이트 본문 1.7 은 한글 본문 1.6~1.8 안이다.
    출처 칸의 WCAG 1.4.12 를 뺀다 — 같은 원칙 문서(`:136`)가 1.4.12 를 간격을 늘려도 내용이 안 깨져야 한다는 규칙으로 설명하고, 범위 수치는 그 문서의 표에서 왔다
  - KI-3: `docs/infra/` 를 킷 안으로 옮기지 않는다(스크립트 · 레포 전용 스킬까지 바뀌어 이 묶음 밖). 설치본에는 `docs/` 가 없다는 사실(`~/.claude/plugins/cache/joo6077-plugins/infra-kit/0.5.0/` 에 `docs` 없음 — 실측)을
    경로 표 다섯 파일에 한 줄로 적고, 저장소 원본(공개 저장소 `joo6077/claude-plugins`, `gh repo view` 로 PUBLIC 확인)의 raw 주소에서 읽게 한다. 둘 다 못 읽으면 원칙을 지어내지 말고 못 읽었다고 적게 한다
  - KD-4 의 design-mockup Step 0: 「자동 감지 및 로드」(지금 Step 2) 를 Step 0 으로 옮기고, 그 뒤 Step 3 ~ 7 을 Step 2 ~ 6 으로 하나씩 당긴다(Step 1 「화면 요구사항 파악」 은 번호 그대로). design-kaizen Gotcha 6 의 형제 규칙(`## Step 0: 자동 감지 및 로드`)과
    design-component `:35` · design-concept `:92` 의 「design-mockup Step 0 동일 패턴」 이 지금은 사실과 다르다

항목별 처리 표:

| ID | 처리 | 조건 · 근거 |
| --- | --- | --- |
| KD-1 | 계약에 넣음 | SK-01 (자리: 목록은 `design-audit/SKILL.md:114 · :235` 라 적었지만 실제 자리는 `design-kit/agents/design-reviewer.md:114` · `:235` · `:248-249` · `:253` 과 design-audit Step 5) |
| KD-2 | 계약에 넣음 | SK-02 |
| KD-3 | 계약에 넣음 | SK-03 — 숫자를 다시 적지 않고 harness `skill-design-guide.md` 의 공통 규칙 절을 가리킨다. 그 절은 GD-6(다른 묶음)이 만든다 |
| KD-4 design:P2 | 넘김 — 사용자 결정 없음 | 규칙 방향(개수 계약 대 「여러 개 바로」)을 바꾸는 일이라 사용자 결정 몫인데 `decisions.md` 에 없다 |
| KD-4 `UNVERIFIED_ENV` | 처리됨 | `09a0cde` — `design-reviewer.md:65-75` 두 분류 · `env_gaps`, design-audit Gotcha 11 · Step 5, evals id 21 |
| KD-4 §3.7 네 칸 | 일부 처리됨 · 나머지 계약에 넣음 | reviewer 출력 틀 `design-reviewer.md:218` 은 `09a0cde` 로 처리됨. 규약 §3 「캡처 자체가 실패」 줄(`visual-change-protocol.md:143`)만 남아 SK-06 |
| KD-4 design-mockup Step 0 | 계약에 넣음 | SK-05 |
| KD-4 Material 3 | 바깥 근거 없음 | Material 3 Expressive · Apple HIG 2026 원문 대조가 ex 폴더에 없다 |
| KD-4 OKLCH | 계약에 넣음 | SK-04 (EX-13) |
| KI-1 | 계약에 넣음 | SC-01 · ER-01 · SC-02 |
| KI-2 | 계약에 넣음 | SK-07 · SC-02 |
| KI-3 | 계약에 넣음 | SK-08 |
| KI-4 Kubernetes 1.37 · Flux · Argo 판 | 계약에 넣음 | SK-09 연구 기록 정정 (EX-8) |
| KI-4 Flux v2.9 · Argo CD 3.5 에서 빠진 API | 바깥 근거 없음 | EX-8 은 판 번호와 날짜만 대조했다. 빠진 API 를 원칙으로 올릴 원문 대조가 없다 |
| KI-4 GitHub 밖 CI · 세 분류 규범 · 1.7+ | 바깥 근거 없음 | ex 폴더에 대조가 없다. 세 분류는 `docs/infra/platform/cicd.md` 원칙 7 이 이미 킷 규칙이라고 적는다 |
| KI-4 `env_gaps` | 계약에 넣음 | SK-09 — infra-audit 한 파일 안의 두 이름(네 칸 · 남용 방지 4 요건)을 짝짓는 한 줄 |
| KB-1 OpenAPI 3.1 · AsyncAPI 3.1.0 | 계약에 넣음 | SK-10 (EX-7) |
| KB-1 시간대 저장 | 처리됨 | `backend-kit/skills/backend-system/SKILL.md:33` Gotcha 18 — 「요청·기기·사용자 설정·레코드 칸 중 어디서 받는지와 저장 여부를 시간대 출처 칸에 적는다」 |
| KB-1 벽시계 문자열 | 바깥 근거 없음 | 벽시계 값을 보낼 문자열 형태는 phase7 근거 파일에도 ex 폴더에도 없다 |
| KR-1 · KR-2 | 계약에 넣음 | SK-11 |
| KR-3 시각 종류 판정 행 | 계약에 넣음 | SK-12 |
| KR-3 버전 리터럴 · testcontainers | 계약에 넣음 | SK-13 |
| KR-3 rust-model 타입 대응 | 처리됨 | `rust-kit/skills/rust-model/SKILL.md:35` Gotcha 「시각 컬럼은 종류부터 정하고, ORM 마다 다른 타입 대응을 따른다」 · `:90` · `:240` `DateTimeWithTimeZone` (Phase 9) |

## GAP 분석 — 복잡도 · 설정 대조 · 편집 전 감사

복잡도 네 축:

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 감사 판정 규칙 · 스킬 절차 · 검사 스크립트 골격 · 문서 페이지 · 연구 기록 | 예 (넷 이상) |
| 공개 판정 · 계약 변경 | design-reviewer 판정값에서 `CONDITIONAL APPROVE` 가 빠진다. infra-test 골격의 종료 코드가 바뀐다(python3 · PyYAML 있고 grep 없음 → 2 에서 0) | 예 |
| 소비면 존재 | design-audit Step 5 · 리포트 틀, `docs/infra-kit/infra-test.html` 코드 사본, 단계 번호를 가리키는 형제 스킬 두 줄 · 문서 페이지 | 예 |
| 회귀 위험 | 도구 조합 사전 검사를 잘못 바꾸면 grep 없는 환경에서 거짓 VIOLATION 이 난다 | 예 |

→ 네 축 모두 예 — **복잡**. 소비면 조건은 SK-01(리포트 틀) · SC-02(문서 페이지 코드 사본) · SK-05(단계 번호 참조)가 따로 잰다.

설정 리터럴 대조 (`.harness/project.yaml`):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | `bash -n scripts/release.sh` (DG-01 N/A 사유) |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | 같은 값 (DG-03 N/A 사유) |
| `diagnostics.ide_exclude` | `[]` | 없음 |
| `contract_categories` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 같은 넷 |
| `anti_patterns` | AP-01 · AP-02 · AP-03(`validate-plugin.py --check=code-fence`) · AP-04(frontmatter `name`) | AP-03 · AP-04 선별 — 스킬 · 참조 md 를 고친다. AP-01(버전 하드코딩) · AP-02(force push)는 이번 변경에 걸릴 자리가 없다(판 올림 · 푸시 안 함) |

편집 전 감사 (읽은 파일과 줄):

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭 | 조건화 |
| --------- | ---------------------------- | -------------- | ------ |
| `design-kit/agents/design-reviewer.md` | `:72` 사본 「CONDITIONAL APPROVE 를 쓰는 킷은 … 1 건 + FAIL 0」, `:114` 규칙 11, `:235` 판정 틀, `:248-249` L3 < 10/10 두 줄, `:253`, `:126` 행간 1.2~1.6배, `:177` 기존 화면 2 개 이상 · 2 개 미만, `:218` 네 칸 있음 | `:249`(미검증 0 · L3 부분)이 `:253` · 사본 `:72` 와 어긋남 | SK-01 · SK-02 · SK-03 |
| `design-kit/skills/design-audit/SKILL.md` | `:114-123` Step 5 (L3 줄 없음), `:31` Gotcha 10, `:80`, `:71` Step 2 표 Typography 「행간 1.2~1.6배」(교차 진단이 찾음) | 리뷰어와 판정 갈래가 다름, 옛 행간 수치 | SK-01 · SK-02 |
| `design-kit/skills/design-audit/templates/audit-report.md` | `:6` `{{APPROVE\|REJECT\|BLOCKED}}` | 없음 (소비면 확인) | SK-01 |
| `design-kit/skills/design-audit/references/audit-criteria.md` | `:10` 행간 1.2~1.6배 · WCAG 1.4.12, `:119` 기존 화면 2 개 이상 · 2 개 · 2 개 미만 | 사이트 1.7 과 어긋남, 규약 숫자 재정의 | SK-02 · SK-03 |
| `design-kit/docs/design/foundations/typography.md` | `:97-107` 라틴 본문 1.4~1.6, `:316-324` 한글 본문 1.6~1.8, `:136-139` WCAG 1.4.12 설명 | 없음 (근거 문서) | SK-02 |
| `docs/assets/site.css` | `:2` `body{line-height:1.7}` | 없음 | SK-02 배경 |
| `design-kit/references/visual-change-protocol.md` | `:3-15` 머리(「그 절은 아직 없다」 — GD-6 몫), `:31` · `:45` · `:159` 숫자(GD-6 몫), `:143` 캡처 실패 → `[미검증]` | `:143` 에 네 칸 없음 | SK-06 |
| `design-kit/skills/design-mockup/SKILL.md` | `:29` Gotcha 13 「Step 6 에서」, `:37` Step 1, `:50` Step 2 자동 감지, `:69-70` 기존 화면 2 개 이상 · Step 3-a, `:72-178` Step 3~7, `:143` 최대 3 회, `:166` (PD-1 묶음 자리) | Step 0 아님, 숫자 재정의 | SK-03 · SK-05 |
| `design-kit/skills/design-mockup/references/mockup-guidelines.md` | `:7` 「Step 3-a 를 따른다」 | 번호 옮기면 따라 바뀜 | SK-05 |
| `design-kit/skills/design-guide/SKILL.md` | `:54` 기존 화면 2 개 이상 | 숫자 재정의 | SK-03 |
| `design-kit/skills/design-system/SKILL.md` | `:27` Gotcha 12 「Figma Variables는 OKLCH 미지원」 | EX-13 보다 강한 단정 | SK-04 |
| `design-kit/skills/design-component/SKILL.md` · `design-concept/SKILL.md` | `:35` · `:92` 「design-mockup Step 0 동일 패턴」 | SK-05 뒤 사실이 된다 (고치지 않음) | SK-05 측정 밖 |
| `.claude/skills/design-kaizen/SKILL.md` | `:23` 형제 표 「Step 0 = 자동 감지 및 로드」 | 같음 | SK-05 근거 |
| `infra-kit/skills/infra-test/SKILL.md` | `:220` `CORE_TOOLS="grep"`, `:241-243` 사전 검사, `:253-296` checkout 규칙, `:327` 「YAML 파싱 실패」, `:389` 표 줄 | grep 만 없는 환경도 종료 2, 금지 낱말 | SC-01 · ER-01 · SK-07 |
| `docs/infra-kit/infra-test.html` | `:508` · `:530` · `:574` · `:615` · `:677` 코드 사본 | 원본과 글자 같음(실측 `same=1`) | SC-02 · SK-07 |
| `infra-kit/references/principle-index.md` 외 경로 표 넷 | `principle-index.md:4` · `:24-35`, `skills/infra-guide/references/principle-index.md:9-10`, `references/audit-criteria.md:4`, `references/init-checklist.md:18`, `skills/infra-init/references/init-checklist.md:9-10` | 설치본에 `docs/` 없음 | SK-08 |
| `infra-kit/skills/infra-guide/SKILL.md` | `:18` principle-index 경유, `:31` Gotcha 14 cicd.md 원칙 7 | 경로 표를 거쳐 읽는다 | SK-08 근거 |
| `docs/infra/platform/cicd.md` | `:60-89` 원칙 7 판정 표 · 세 줄 | 없음 | SK-08 근거 |
| `infra-kit/skills/infra-audit/SKILL.md` | `:25` Gotcha 11 네 칸, `:110-117` Unverifiable Summary `env_gaps` 4 요건 이름 | 두 이름 짝이 안 적힘 | SK-09 |
| `docs/infra/research-log.md` | `:1-4` 머리 판, `:23` Kubernetes v1.37.1 최신 안정판, `:47-56` 조회만 한 것 · 다음 후보 | EX-8 과 어긋남 | SK-09 |
| `backend-kit/skills/backend-system/SKILL.md` | `:51` API 규격 행 「OpenAPI 3.1 스펙 파일」, `:33` Gotcha 18 | 최소선인지 불분명 | SK-10 |
| `backend-kit/skills/backend-audit/SKILL.md` | `:77` 5 행 「OpenAPI 3.1 스펙 일치」 | 같음 | SK-10 |
| `backend-kit/skills/backend-audit/references/audit-criteria.md` | `:22` 「OpenAPI 3.1.x 이상」, `:94` AsyncAPI 3.0+ | 같음 | SK-10 |
| `docs/backend/research-log.md` | `:1-8` 머리 판 · 최근 절 | EX-7 기록 없음 | SK-10 |
| `rust-kit/references/project-detection.md` | `:77-99` Step 2c 표, `:87` testcontainers 전제 0.27, `:147-148` 실측 문장 `myapp-api` | 전제 0.27 이 킷 어디에도 없음(`grep -rn testcontainers rust-kit` 9 곳, 판 번호 0), 없던 이름 | SK-11 · SK-13 |
| `rust-kit/skills/rust-run/SKILL.md` | `:22` · `:24` 예시 명령, `:26` Gotcha 9 출처 `myapp-api` | 없던 이름 | SK-11 |
| `rust-kit/skills/rust-preflight/SKILL.md` | `:21` Gotcha 7 실측 `myapp-migration` | 없던 이름 | SK-11 |
| `rust-kit/skills/rust-init/SKILL.md` | `:91` · `:126` · `:159` `{project}/`, `:235` `name = "myapp-api"`, `:64-82` 의존성 목록과 Step 2c 안내, `:184-192` 4a 블록, `:252-257` 툴체인 | 자리 표시 방식 다름, 4a · 4b 에 Step 2c 안내 없음 | SK-11 · SK-13 |
| `rust-kit/skills/rust-audit/references/audit-criteria.md` | `:3` 머리(Step 2c 인용), `## 7. API Design` `:83-92`, `:89` `utoipa 5.4 docs` | 시각 종류 행 없음, 버전 리터럴 | SK-12 · SK-13 |
| `rust-kit/skills/rust-middleware/SKILL.md` | `:14` Gotcha 2 tower-http 0.6 | Step 2c 안내 없음 (Step 2c 표는 0.7.1 · 동작 변경 기재) | SK-13 |
| `rust-kit/templates/rust-init.toml.template` | `:11` · `:36-38` 판 번호 주석 | Step 2c 안내 없음 | SK-13 |
| `backend-kit/skills/backend-audit/references/audit-criteria.md` `:38` · `docs/rust/data/sqlx-patterns.md:180` | 시각 종류별 저장 행 원문 · 원칙 6 | 없음 (옮길 원문) | SK-12 |

구현 선택지가 둘 이상인 곳은 위 「이 계약이 정한 판단 넷」 에 고른 쪽과 까닭을 적었다.

봉인 전 기준값 (시작 커밋 판에서 `bash m.sh <ID>` — 2026-09-26 21:1x 실측):

```text
SK-01: a=6 b=0 l3_ok=1 l3_norej=2 verdict=0 audit_l3=0 copies=0
SK-02: old=3 row=0 reviewer=0 nowcag=0 audit=0
SK-03: global=5 | n=1 num=1 guide=0; (다섯 자리 모두 같음)
SK-04: old=1 url=0 models=0
SK-05: seq=1,2,3,4,5,6,7 first=0 old3a=3 new2a=0 g13=0
SK-06: cap=1 four=0 guide=0
SK-07: old_skill=1 old_html=1 new_skill=1 new_html=1
SK-08: files= 0 0 0 0 0 http=200
SK-09: sec=0 words=0 lu=0 map=0
SK-10: anchors=0 sec=0 words=0 lu=0
SK-11: pd=2 run=1 pre=1 kept=3 examples=2 / init_old=1 init_new=0
SK-12: row=0 words=0 cats=7
SK-13: utoipa=0 tc=0 mw=0 init_ok=0 tpl=0
SC-01: syntax=0 / E1 rc=2 grepmiss=1 falseviol=0 copass=0 / E2 rc=2 grepmiss=1 falseviol=0 copass=0 / E3 rc=2 grepmiss=0 falseviol=0 copass=1 / E4 rc=2 grepmiss=1 falseviol=0 copass=0
SC-02: skill_lines=168 html_lines=168 same=1
AP-03: check=code-fence fail_kits=0 · AP-04: check=frontmatter fail_kits=0
RE-02: added=0 · DG-02: TOTAL new=0
AR-01: allow=28 changed=0 outside=0 missing=28 harness_outside=0
AR-02: seal_first=0 mixed=0 multi_kit=0 kits=
AR-03: validate_fail=0 copies=0 sync=0 stale=0 evals=0 assertions=0 · AR-03CI: rc=0 25 줄, 나머지는 `feedback-agg-test SKIP (yq 없음)` 한 줄
AR-04: exists=0 ids=0 tone=0 pages=0 roots=0
```

대조 실측 (봉인 전):

- ER-01 음성 대조 — 골격에서 핵심 도구 사전 검사 세 줄(`for t in $CORE_TOOLS` 반복)을 지운 사본을 같은 네 환경에 돌리면 `E2 rc=2 grepmiss=0 falseviol=1` · `E4 rc=2 grepmiss=0 falseviol=1` 이 나온다. 사전 검사를 그냥 빼는 구현은 ER-01 에서 FAIL 한다
- SC-01 음성 대조 — 지금 판(사전 검사가 무조건 grep 을 요구)은 `E1 rc=2 grepmiss=1` 이다. 고치지 않으면 FAIL 한다
- SK-01 · AR-03 양성 대조 — `git archive` 사본에서 `design-reviewer.md` 사본 줄 한 낱말을 바꾸면 `check-reviewer-protocol-copies.py` 가 `violations=1` · 종료 코드 1 을 낸다
- AP-03 · AP-04 양성 대조 — 사본에서 design-guide 에 언어 표시 없는 펜스를 넣으면 `--check=code-fence` 종료 코드 2(`V6 … 1 bare — FAIL`), design-system 머리의 `name:` 을 지우면 `--check=frontmatter` 종료 코드 2. 손대지 않은 사본은 0
- DG-02 양성 대조 — 같은 측정을 `7b4618c^..7b4618c`(design-kit Phase 6 커밋)에 MD013 을 켜고 돌리면 `TOTAL new=28`, 끄면 0. 측정이 살아 있다
- AR-04 대조(교차 진단 반영 뒤) — 같은 판정 줄을 떼어 두 가짜 notes 에 돌렸다: 세 절(`## 톤 대조` · `## 다시 만들 문서 페이지` · `## 남은 것`)에 맞는 글이 든 쪽은 `tone=1 pages=1 roots=1`, 같은 낱말을 다른 절에 몰아 쓰고 톤 절에 「부르지 않음」 만 적은 쪽은 `tone=0 pages=0 roots=0`. SK-02 기준값 `old=3` 은 교차 진단이 찾은 세 줄(`design-reviewer.md:126` · `audit-criteria.md:10` · `design-audit/SKILL.md:71`)과 같다
- 알려진 답 — SK-03 `global=5` 는 손으로 센 다섯 자리(`design-reviewer.md:177` · `audit-criteria.md:119` · `design-guide/SKILL.md:54` · `design-mockup/SKILL.md:69` · `:143`)와 같다.
  SC-01 `E3 copass=1` 은 픽스처 워크플로 한 개에 checkout 한 줄이라 1 이다. SK-11 `examples=2` 는 `rust-run/SKILL.md:22` · `:24` 두 줄이다. AR-01 `allow=28` 은 아래 목록을 손으로 적은 수다
- 도구 준비 — `command -v bash` = `/opt/homebrew/bin/bash`(5.3.9), PyYAML 있는 python3 = `/Users/jackson/.pyenv/versions/3.14.3/bin/python3`(yaml 6.0.3), `/usr/bin/python3` 는 `import yaml` 실패,
  markdownlint-cli2 0.23.2 는 세션 스크래치 `k2/mdlint/`(c4c 묶음 것을 복사), 로컬 CI 도구 `ci-local.sh` 지문 `59fe55125c0dbc77`. SK-08 의 raw 주소는 `curl` 로 200

## 범위 경계

- 이 계약은 봉인 · 봉인 커밋 · 구현 전 단계까지를 만든다. 교차 진단을 먼저 받고 봉인한다
- 킷 판 올림(`plugin.json`) · marketplace · 릴리스 · 푸시는 하지 않는다 — 부모가 합친 뒤 한다
- 다른 묶음과 같은 파일: `design-kit/references/visual-change-protocol.md` 는 GD-6 이 머리 `:3-15` 와 숫자 줄(`:31` · `:45` · `:159`)을 고친다 — 이 계약은 `:143` 한 줄만 고친다.
  `design-kit/skills/design-mockup/SKILL.md:166` 은 PD-1 묶음 자리다 — 이 계약은 머리 줄 · `:29` · `:69-70` · `:143` 만 고친다. KD-3 은 GD-6 이 만들 절을 이름으로 가리키기만 하고 숫자를 다시 정하지 않는다
- 문서 페이지 다시 만들기는 부모 몫이다. 이 계약이 고치는 페이지는 `docs/infra-kit/infra-test.html` 하나(코드 사본 줄만). 원본이 바뀌어 다시 만들 후보 — `docs/design-kit/design-mockup.html`(DC-15 와 함께) ·
  `docs/design-kit/visual-change-protocol.html` · design-audit · design-system · infra-kit · backend-kit · rust-kit 페이지 중 바뀐 낱말이 든 쪽, `docs/infra-kit/research-log.html` · `docs/backend-kit/research-log.html`(드리프트 도구 대응, 지금 없음) — 구현자가 바뀐 낱말로 `docs/` 를 찾아 notes 에 목록을 남긴다(AR-04)
- 평가 사례(`design-kit/evals/evals.json` 의 「2 개 이상」 · 「최대 3 회」 기대 문장)는 고치지 않는다 — 규약이 정한 값을 행동으로 재는 문장이고 KD-3 대상(스킬 · 감사 다섯 자리)이 아니다
- `design-kit/skills/design-component/SKILL.md:35` · `design-concept/SKILL.md:92` 는 SK-05 뒤 사실이 되므로 고치지 않는다
- backend-kit(`docs/backend/` 41 곳) · rust-kit(`docs/rust/` 4 곳)도 설치본에 `docs/` 가 없는 같은 뿌리를 가진다. KI-3 은 infra-kit 만이다 — 두 킷은 notes 에 넘김으로 적는다
- 기존 markdownlint 경고 전체 정리(VS-26)는 부모 몫이다. DG-02 는 이 계약이 더한 줄의 새 경고만 잰다
- `.claude/skills/docs-site/SKILL.md:104` 에도 「line-height 1.2~1.6배」 가 있지만 레포 전용 스킬이라 이 묶음(네 킷) 밖이다 — notes 「남은 것」 에 넘긴다. `docs/superpowers/plans/2026-03-30-design-kit.md` 의 두 줄은 지난 계획 기록이라 둔다
- 이 계약의 근거 파일(`leftovers.md` · `decisions.md` · `ex/EX-7.md` · `EX-8.md` · `EX-13.md`)은 통합 폴더 `after-0926b` 에만 있고 git 에 없다(교차 진단 확인). 측정은 이 파일들을 읽지 않지만, 판단 근거가 사라지지 않도록 형제 묶음이 다 끝나기 전에 그 폴더를 지우지 말라고 notes 에 적는다
- KB-1 의 AsyncAPI 는 킷 문장 「AsyncAPI 3.0+」(최소선)가 EX-7 로도 참이라 킷 문장은 두고 연구 기록에만 남긴다
- 커버리지 해소: SK-03 (추가) — 측정의 `global` 은 design-kit 전체 md(규약 파일 · `docs/` 제외)를 돌므로 다섯 자리 밖에 새 숫자 재정의가 생겨도 잡는다. 다섯 자리는 줄 단위로 따로 잰다
- 커버리지 해소: SK-03 · SK-05 · SK-08 · SK-09 · SK-10 · SK-11 · SK-13 — 산문의 경로와 낱말(`skill-design-guide.md` · `rust-run/SKILL.md:22` · `5.4` · `0.27` · raw 주소 등)은 측정 줄의 `bash m.sh <ID>` 가 부르는 도우미 안에 같은 표기로 들어 있다(변수 `DR` · `DAC` · `DM` · `DMG` · `DG` · `IT` · `ITH` · `IA` · `ILOG` · `BS` · `BA` · `BAC` · `BLOG` · `RPD` · `RRUN` · `RPRE` · `RINIT` · `RAC` · `RMW` · `RTPL` 과 SK-08 의 다섯 경로). 측정 줄에 다시 적지 않은 것은 목록을 두 곳에 두지 않으려는 것이다
- 커버리지 해소: AR-01 · AR-02 · AR-03 · AR-04 — 허용 경로 28 개 · `.harness/` 허용 넷 · 킷 묶음 규칙 · 검사 스크립트 여섯 · notes 경로와 페이지 이름은 도우미의 `AR-01` · `AR-02` · `AR-03` · `AR-04` 한 곳에만 열거한다. 도우미는 SK-01 아래 지문으로 잠근다
- 느슨하게 하는 개정(허용 경로 늘리기 · 측정 대상 줄이기 · 문턱 낮추기)이 필요해지면 개정 파일에 동의 칸을 비워 적고 멈춘다

## Skill

- [ ] SK-01: KD-1 — Given 감사가 카테고리 일부를 건너뛰어 L3 < 10/10 인 경우, When design-reviewer 판정 규칙을 적용하면, Then 판정은 REJECT 이고 design-kit 어디에도 `CONDITIONAL APPROVE` 판정 갈래가 없다 — 리뷰어 규칙 11 · 판정 틀 · 판정 규칙과 design-audit Step 5 가 같은 판정을 낸다. 기준 원문을 옮긴 사본(규칙 8, `:72` 한 줄)은 글자를 바꾸지 않는다 [exact, enumerated]
    도우미 지문: `ed839ac28cacc62d` — 아래 `## 회귀 게이트` 에서 뗀 m.sh 의 `shasum -a 256 m.sh | cut -c1-16` 이 이 값과 다르면 어떤 조건도 판정하지 않는다
    측정: `bash m.sh SK-01` → `a=1 b=0 l3_ok=1 l3_norej=0 verdict=1 audit_l3=1 copies=0`
    뜻: a = `design-kit/agents/design-reviewer.md` 의 `CONDITIONAL` 줄 수(사본 한 줄만 남음), b = `design-kit/skills/design-audit/SKILL.md` + `design-kit/skills/design-audit/templates/audit-report.md` 의 `CONDITIONAL` 줄 수,
    l3_ok · l3_norej = 리뷰어의 `L3 < 10/10` 줄이 1 개 이상이고 그 줄이 모두 `REJECT` 를 담음, verdict = 판정 틀 줄이 `**판정: {{APPROVE | REJECT | BLOCKED}}**` 와 같은 줄 수,
    audit_l3 = design-audit `## Step 5` 절에 `L3` 와 `REJECT` 가 함께 든 줄이 있음, copies = `python3 scripts/check-reviewer-protocol-copies.py` 종료 코드
    FAIL 모양: `a` 가 2 이상(판정 갈래가 남음) 이거나 `copies` 가 0 이 아님(사본을 건드림)
- [ ] SK-02: KD-2 — design-kit 감사 기준 Typography 행간 행 · 리뷰어 Typography 행간 항목 · design-audit Step 2 카테고리 표의 Typography 행 세 자리가 「1.2~1.6배」 를 더 적지 않고, Step 2 표 행은 감사 기준 행간 행을 가리키며, 기준 행은 `typography.md` 의 문자 체계별 범위(한글 포함)를 가리키며 출처 칸에 WCAG 1.4.12 가 없다 [exact, enumerated]
    측정: `bash m.sh SK-02` → `old=0 row=1 reviewer=1 nowcag=1 audit=1`
    뜻: old = `design-kit/skills/design-audit/references/audit-criteria.md` + `design-kit/agents/design-reviewer.md` + `design-kit/skills/design-audit/SKILL.md` 의 `1.2~1.6` 줄 수, row = 기준 파일 `| 행간 비율` 행에 `typography.md` 와 `한글` 이 둘 다 있음,
    reviewer = 리뷰어 `- 행간 비율` 줄에 `audit-criteria` 가 있음, nowcag = 그 행에 `WCAG 1.4.12` 가 없음, audit = design-audit 의 `| **Typography** |` 행에 `행간` 과 `audit-criteria` 가 둘 다 있음
- [ ] SK-03: KD-3 — 규약 숫자(같은 역할 기존 화면 개수 · 스스로 고치기 횟수)를 다시 적은 다섯 자리 — `design-kit/agents/design-reviewer.md` 의 `- 같은 역할 관례 일치` 줄 · `design-kit/skills/design-audit/references/audit-criteria.md` 의 `| 같은 역할 관례 일치` 행 · `design-kit/skills/design-mockup/SKILL.md` 의 `- 앱 코드 존재` 줄 · 같은 파일의 `스스로 고치기` 줄 · `design-kit/skills/design-guide/SKILL.md` 의 `§0 관례 표` 줄 — 가 숫자를 적지 않고 harness `skill-design-guide.md` 의 공통 규칙 절을 가리킨다. design-kit 의 다른 md 에도 새 재정의가 없다 [exact, enumerated]
    측정: `bash m.sh SK-03` → `global=0 | n=1 num=0 guide=1; n=1 num=0 guide=1; n=1 num=0 guide=1; n=1 num=0 guide=1; n=1 num=0 guide=1;`
    뜻: global = design-kit 의 md 전부(`design-kit/references/visual-change-protocol.md` · `docs/` 아래 제외)에서 `(기존 화면이? \**[0-9]+ ?개|최대 [0-9]+ ?회)` 줄 수. 다섯 자리마다 n = 찾은 줄 수, num = `[0-9]+ ?(개|회)` 가 든 줄 수, guide = `skill-design-guide` 가 있음
- [ ] SK-04: KD-4 OKLCH — `design-kit/skills/design-system/SKILL.md` Gotcha 12 의 Figma 문장이 「미지원」 단정 대신 EX-13 원문대로 적힌다 — 도움말이 색 모델을 Hex · HSB · HSL · CSS · RGB 로 열거한다는 것과 그 주소 [exact, enumerated]
    측정: `bash m.sh SK-04` → `old=0 url=1 models=1`
    뜻: old = design-kit md(`docs/` 제외)의 `OKLCH 미지원` 줄 수, url = Gotcha 12 줄에 `help.figma.com/hc/en-us/articles/360043042113` 이 있음, models = 그 줄에 `Hex` `HSB` `HSL` `CSS` `RGB` 가 다 있음
- [ ] SK-05: KD-4 design-mockup Step 0 — `design-kit/skills/design-mockup/SKILL.md` 의 단계 머리가 `## Step 0: 자동 감지 및 로드` 로 시작해 0 부터 6 까지 빈 번호 없이 이어지고, 옮긴 번호를 가리키는 글(Gotcha 13 의 승인 기록 단계, 매트릭스 소절 `Step 2-a`, `design-kit/skills/design-mockup/references/mockup-guidelines.md` 의 소절 참조)이 새 번호를 쓴다 [exact, enumerated]
    측정: `bash m.sh SK-05` → `seq=0,1,2,3,4,5,6 first=1 old3a=0 new2a=1 g13=1`
    뜻: seq = `## Step N` 머리 번호 차례, first = 첫 단계 머리가 `## Step 0: 자동 감지 및 로드` 와 같음, old3a = 두 파일의 `Step 3-a` 줄 수, new2a = `### Step 2-a` 머리 수, g13 = Gotcha 13 줄에 `Step 5 에서` 가 있음
- [ ] SK-06: KD-4 §3.7 네 칸 — `design-kit/references/visual-change-protocol.md` 의 「캡처 자체가 실패」 줄이 `[미검증]` 보고에 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 쓰라고 하고 그 정의 자리 `skill-design-guide` §3.7 을 가리킨다. 이 파일에서 다른 줄은 이 조건 때문에 바꾸지 않는다 [exact]
    측정: `bash m.sh SK-06` → `cap=1 four=1 guide=1`
- [ ] SK-07: KI-2 — infra-test 핀닝 규칙의 오류 문구가 checkout 규칙과 같은 「YAML 읽기 실패」 이고, 문서 페이지 코드 사본도 같다 [exact, enumerated]
    측정: `bash m.sh SK-07` → `old_skill=0 old_html=0 new_skill=2 new_html=2`
    뜻: `infra-kit/skills/infra-test/SKILL.md` · `docs/infra-kit/infra-test.html` 각각의 `YAML 파싱 실패` 줄 수와 `YAML 읽기 실패` 줄 수
- [ ] SK-08: KI-3 — infra-kit 이 `docs/infra/` 경로를 싣는 경로 표 다섯 파일 — `infra-kit/references/principle-index.md` · `infra-kit/skills/infra-guide/references/principle-index.md` · `infra-kit/references/audit-criteria.md` · `infra-kit/references/init-checklist.md` · `infra-kit/skills/infra-init/references/init-checklist.md` — 이 각각 한 줄로, 설치본에 그 경로가 없으면 `https://raw.githubusercontent.com/joo6077/claude-plugins/main/` 뒤에 같은 경로를 붙여 읽고 그래도 못 읽으면 못 읽었다고 적으라고 한다 [exact, enumerated]
    측정: `bash m.sh SK-08` → `files= 1 1 1 1 1 http=200`
    뜻: 파일마다 그 주소 앞부분과 `못 읽` 이 함께 든 줄 수(다섯 칸, 위 순서), http = 그 주소로 `docs/infra/platform/cicd.md` 를 받은 HTTP 상태
    대체: 네트워크가 없어 http 가 `000` 이면 `[미검증:ENV]` 한 건까지 받는다 — 네 칸(막는 것 = curl 출력 · 시도한 우회 = `gh api repos/joo6077/claude-plugins/contents/docs/infra/platform/cicd.md` · 통제 불가 사유 · 재검증 명령 = 같은 curl)을 채워야 한다. files 다섯 칸은 대체 없이 재야 한다
- [ ] SK-09: KI-4 — `docs/infra/research-log.md` 에 `## [2026-09-26]` 절이 하나 생겨 EX-8 대조(Kubernetes 최신 1.37.0 · 2026-08-26 · 유지 판 1.37 · 1.36 · 1.35, Flux v2.9.5 · 2026-08-31, Argo CD v3.5.3 · 2026-09-14, 근거 파일 `ex/EX-8.md`)를 적고 머리 `last_updated` 가 2026-09-26 이다. `infra-kit/skills/infra-audit/SKILL.md` 에 `env_gaps` 칸 이름(1차 도구 시도 · fallback 시도 · 실패 로그)과 Gotcha 11 네 칸(시도한 우회 · 막는 것)을 짝짓는 줄이 하나 있다 [exact, enumerated]
    측정: `bash m.sh SK-09` → `sec=1 words=1 lu=1 map=1`
    뜻: sec = 그 머리 줄 수, words = 그 절에 `ex/EX-8.md` `kubernetes.io/releases` `1.37.0` `2026-08-26` `1.35` `v2.9.5` `2026-08-31` `v3.5.3` `2026-09-14` 가 다 있음, lu = `last_updated: 2026-09-26` 줄 수,
    map = infra-audit 에서 `fallback 시도` · `시도한 우회` · `실패 로그` · `막는 것` 이 한 줄에 다 든 줄 수
- [ ] SK-10: KB-1 — backend-kit 의 OpenAPI 3.1 표기 세 자리 — `backend-kit/skills/backend-system/SKILL.md` 의 `| API 규격 |` 행 · `backend-kit/skills/backend-audit/SKILL.md` 의 `| 5 | API Design |` 행 · `backend-kit/skills/backend-audit/references/audit-criteria.md` 의 `| OpenAPI 3.1 JSON Schema 호환` 행 — 이 「3.1 이상」 과 「최소 지원선」 을 함께 적어 최신판 뜻이 아님을 밝힌다. `docs/backend/research-log.md` 에 `## [2026-09-26]` 절이 생겨 EX-7 대조를 적고 머리 `last_updated` 가 2026-09-26 이다 [exact, enumerated]
    측정: `bash m.sh SK-10` → `anchors=3 sec=1 words=1 lu=1`
    뜻: anchors = 세 행 중 `3.1 이상` 과 `최소 지원선` 이 다 든 행 수, words = 그 절에 `ex/EX-7.md` `spec.openapis.org/oas/latest.html` `3.2.1` `asyncapi/spec/releases/tag/v3.1.0` `2026-01-31` 이 다 있음
- [ ] SK-11: KR-1 · KR-2 — 옛 실측 문장 세 자리(`rust-kit/references/project-detection.md` 의 `- 출처: 2026-07 실측` 두 줄 · `rust-kit/skills/rust-run/SKILL.md` Gotcha 9 · `rust-kit/skills/rust-preflight/SKILL.md` Gotcha 7)가 크레이트 이름 없이 사건만 적고, 사건 문장 자체는 남는다. 예시 명령 두 줄(`rust-run/SKILL.md:22` · `:24`)은 그대로다. `rust-kit/skills/rust-init/SKILL.md` 의 멤버 크레이트 이름이 `{project}` 자리 표시를 쓴다 [exact, enumerated]
    측정: `bash m.sh SK-11` → 두 줄 `pd=0 run=0 pre=0 kept=3 examples=2` · `init_old=0 init_new=1`
    뜻: pd · run · pre = 세 자리의 `myapp` 줄 수, kept = 세 자리에 `실측` 이 남은 수, examples = 예시 두 줄 수, init_old · init_new = `name = "myapp-api"` · `name = "{project}-api"` 줄 수
- [ ] SK-12: KR-3 — `rust-kit/skills/rust-audit/references/audit-criteria.md` 의 `## 7. API Design` 절에 `| 시각 종류별 저장 |` 행이 생겨, 벽시계 뜻의 필드를 순간 하나로만 저장하거나 특정 지역 벽시계에 IANA 시간대 이름 칸이 없으면 FAIL 이라고 하고 `sqlx-patterns.md` 원칙 6 을 가리킨다. 카테고리 수는 7 그대로다 [exact]
    측정: `bash m.sh SK-12` → `row=1 words=1 cats=7`
- [ ] SK-13: KR-3 — 버전 값이 Step 2c 표를 가리킨다: rust 감사 기준 `| OpenAPI 정합 |` 행의 출처가 `5.4` 없이 Step 2c 를 가리키고, Step 2c 표 `testcontainers` 행의 「전제」 칸이 `0.27` 이 아니며, `rust-kit/skills/rust-middleware/SKILL.md` Gotcha 2 줄 · `rust-kit/templates/rust-init.toml.template` 에 Step 2c 안내가 있고, `rust-kit/skills/rust-init/SKILL.md` 의 Step 2c 언급이 3 줄 이상이다(지금 1) [exact, enumerated]
    측정: `bash m.sh SK-13` → `utoipa=1 tc=1 mw=1 init_ok=1 tpl=1`
    뜻: init_ok = `grep -cE 'Step 2c'` 가 3 이상

## Script

- [ ] SC-01: KI-1 — Given infra-test 골격 스크립트(SKILL.md 의 `tests/ci-validation.sh` 코드 블록)와 checkout 을 SHA 로 고정한 워크플로 한 개, When PATH 를 도구 조합별 빈 폴더로 바꿔 돌리면, Then python3 · PyYAML 이 있고 grep 이 없는 환경(E1)은 종료 코드 0 으로 checkout 을 통과시키고, grep 만 있는 환경(E3)은 지금처럼 checkout 통과 · 종료 코드 2 다 [exact, enumerated]
    측정: `bash m.sh SC-01` 의 `syntax=0` 줄과 E1 · E3 줄 → `syntax=0` · `E1 rc=0 grepmiss=0 falseviol=0 copass=1` · `E3 rc=2 grepmiss=0 falseviol=0 copass=1`
    환경: E1 = PyYAML 있는 python3 하나, E2 = 없음, E3 = grep 하나, E4 = PyYAML 없는 `/usr/bin/python3` 하나. bash 는 절대 경로로 부른다
    음성 대조: 지금 판(사전 검사가 grep 을 무조건 요구)은 `E1 rc=2 grepmiss=1` — 고치지 않으면 FAIL
- [ ] SC-02: KI-1 · KI-2 소비면 — `docs/infra-kit/infra-test.html` 의 골격 코드 사본(HTML 엔티티를 푼 글)이 `infra-kit/skills/infra-test/SKILL.md` 의 같은 코드 블록과 글자 그대로 같다 [exact]
    측정: `bash m.sh SC-02` → 끝 칸 `same=1` (줄 수 두 칸은 같기만 하면 된다)
    음성 대조: 원본만 고치고 페이지를 두면 `same=0`

## Error

- [ ] ER-01: KI-1 — Given SC-01 과 같은 골격 · 픽스처, When grep 도 PyYAML 있는 python3 도 없는 두 환경(E2 = 도구 없음, E4 = PyYAML 없는 python3 만)에서 돌리면, Then 둘 다 grep 부재를 적은 `EXECUTION_ERROR` 줄 하나와 종료 코드 2 로 멈추고 거짓 `checkout 스텝 없음` VIOLATION 을 내지 않는다 [exact, enumerated]
    측정: `bash m.sh ER-01` 의 E2 · E4 줄 → `E2 rc=2 grepmiss=1 falseviol=0 copass=0` · `E4 rc=2 grepmiss=1 falseviol=0 copass=0`
    음성 대조: 사전 검사 세 줄을 그냥 지운 사본은 `E2 … grepmiss=0 falseviol=1` · `E4 … grepmiss=0 falseviol=1` (봉인 전 실측)

## Architecture

- [ ] AR-01: 바뀐 파일 범위 — Given 시작 커밋 `63789486b72b8998be924fd54d56ae7465e76b21` 부터 가지 `chore/ak2-k2` 끝(`git rev-parse --verify -q refs/heads/chore/ak2-k2`, 못 찾으면 UNRESOLVED)까지, `.harness/` 밖에서 바뀐 경로가 정확히 28 경로(열거는 아래 도우미 `AR-01` 의 허용 목록 한 곳에만 있다)와 같고, `.harness/` 안은 이 계약 · 같은 슬러그 개정 · 같은 슬러그 피드백 · notes 파일 밖을 건드리지 않는다 [exact, enumerated]
    측정: `bash m.sh AR-01` → `allow=28 changed=28 outside=0 missing=0 harness_outside=0` (생성물 없음 — 제외 경로는 `.harness` 하나)
- [ ] AR-02: 커밋 모양 — 같은 구간의 첫 커밋은 이 계약 파일 하나만 담은 봉인 커밋이고, 구현 커밋은 `.harness/` 를 섞지 않으며, 커밋마다 킷 하나(design = `design-kit/` · infra = `infra-kit/` `docs/infra/` `docs/infra-kit/` · backend = `backend-kit/` `docs/backend/` · rust = `rust-kit/`)만 담고, 네 킷이 모두 커밋을 가진다 [exact, enumerated]
    측정: `bash m.sh AR-02` → `seal_first=1 mixed=0 multi_kit=0 kits=backend,design,infra,rust`
- [ ] AR-03: 기존 검사 전부 통과 — 네 킷 `validate-plugin.py` · `check-reviewer-protocol-copies.py` · `sync-docs.py --check-only` · `check-stale-values.py` · `run-evals.py` · `run-kaizen-assertions.py` 가 모두 종료 코드 0 이고, 로컬 CI 도구가 시작 판과 같은 결과를 낸다 [exact, enumerated]
    측정 1: `bash m.sh AR-03` → `validate_fail=0 copies=0 sync=0 stale=0 evals=0 assertions=0`
    측정 2: `bash m.sh AR-03CI` → `ci_ok=25 ci_other=0` (도구 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` 지문 `59fe55125c0dbc77`, 사본으로 돌림. 같은 기계에서 다른 `ci-local.sh` · `save-test.sh` 가 도는 중이면 끝난 뒤 잰다)
    양성 대조: 사본 줄 한 낱말을 바꾼 `git archive` 사본에서 `check-reviewer-protocol-copies.py` 종료 코드 1 (봉인 전 실측)
- [ ] AR-04: notes — `.harness/.meta/after-kaizen-0926b/k2-notes.md` 가 가지 끝에 있고, 열두 항목 ID(KD-1 ~ KD-4 · KI-1 ~ KI-4 · KB-1 · KR-1 ~ KR-3) 처리 결과, `## 톤 대조` 절에 `tone-kit:tone-guide` 1 단계 · 5 단계를 실제로 부른 기록(두 단계 이름 각각), `## 다시 만들 문서 페이지` 절에 페이지 목록(`docs/design-kit/design-mockup.html` 포함), `## 남은 것` 절에 backend · rust 의 같은 뿌리(설치본 `docs/` 없음) 넘김을 담는다 [structural, enumerated]
    측정: `bash m.sh AR-04` → `exists=1 ids=12 tone=1 pages=1 roots=1`
    뜻: tone = `## 톤 대조` 절에 `tone-guide 1 단계` 와 `tone-guide 5 단계` 가 다 있음, pages = `## 다시 만들 문서 페이지` 절에 `docs/design-kit/design-mockup.html` 이 있음, roots = `## 남은 것` 절에 `backend-kit` · `rust-kit` · `docs/` 가 다 있음

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 네 킷에 `python3 scripts/validate-plugin.py <킷> --check=code-fence` 가 모두 종료 코드 0 [exact, enumerated]
    측정: `bash m.sh AP-03` → `check=code-fence fail_kits=0`
- [ ] AP-04: SKILL.md / agents/*.md frontmatter `name` 누락 금지 — 네 킷에 `--check=frontmatter` 가 모두 종료 코드 0 [exact, enumerated]
    측정: `bash m.sh AP-04` → `check=frontmatter fail_kits=0`

## Reusability

- [ ] RE-01: N/A (산출물이 스킬 · 참조 문서 · 연구 기록 · 문서 페이지 · 템플릿 주석뿐이라 재사용 단위 코드(컴포넌트 · 함수 · 모듈)가 없다. infra-test 골격은 문서 속 예시이고 SC-01 이 돌려 본다. 측정: AR-01 의 28 경로 확장자가 `.md` 26 · `.html` 1 · `.template` 1)
- [ ] RE-02: 새 파일을 만들지 않고 기존 원칙 문서 · 규약 · Step 2c 표 · 형제 킷 기준 행을 가리킨다 — `.harness/` 밖 새 파일 0 개 [exact]
    측정: `bash m.sh RE-02` → `added=0`

## Diagnostics

- [ ] DG-01: N/A (commands.analyze 는 `bash -n scripts/release.sh` — 이 계약의 바뀐 파일과 교집합 0 개. 측정: `git -C "$R" diff --name-only 63789486b72b8998be924fd54d56ae7465e76b21 H | grep -c '^scripts/release.sh$'` 이 0)
- [ ] DG-02: 편집기 진단 — 이 계약이 바꾼 md 파일에서 더한 줄에 걸린 markdownlint 경고 0 개 (markdownlint-cli2 0.23.2, MD013 끔 — 편집기 확장과 같은 설정. HTML · 템플릿은 편집기가 이 검사를 하지 않는다) [exact]
    측정: `bash m.sh DG-02` 의 끝 줄 → `TOTAL new=0`
    양성 대조: `BASE=7b4618c^ H=7b4618c bash m.sh DG-02P` → `TOTAL new=28` (MD013 을 켜면 같은 측정이 긴 새 줄을 잡는다, 봉인 전 실측)
- [ ] DG-03: N/A (commands.test 는 `bash scripts/release.sh` — 이 계약의 바뀐 파일과 교집합 0 개. 측정은 DG-01 과 같다)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 바뀐 파일에 실행 진입점 0 개. 문서 속 골격 스크립트는 SC-01 · ER-01 이 실제로 돌린다)

## 회귀 게이트 — 측정 도우미

떼는 법: `awk '/^<!-- m.sh:begin -->$/{f=1;next} /^<!-- m.sh:end -->$/{f=0} f' <계약> | sed '1d;$d' > m.sh`. 지문 `ed839ac28cacc62d` (`shasum -a 256 m.sh | cut -c1-16`).
도우미가 쓰는 도구 경로(markdownlint-cli2 · ci-local.sh)가 다른 기계에 없으면 `MDL=` 로 바꿔 넘긴다. 도우미는 파일을 고치지 않는다.

<!-- m.sh:begin -->
```bash
#!/usr/bin/env bash
# k2 계약 측정 도우미 — bash m.sh <조건 ID>. 읽기만 한다. 임시 파일은 mktemp 폴더에 두고 끝나면 지운다.
# R: 작업 폴더(기본 k2 워크트리) · BASE: 시작 커밋 · H: 끝 판(가지 끝을 해석, 못 찾으면 UNRESOLVED 로 멈춘다)
R=${R:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-k2}
BASE=${BASE:-63789486b72b8998be924fd54d56ae7465e76b21}
H=${H:-$(git -C "$R" rev-parse --verify -q refs/heads/chore/ak2-k2)}
[ -n "$H" ] || { echo "UNRESOLVED sprint_head"; exit 2; }
git -C "$R" cat-file -e "$BASE^{commit}" 2>/dev/null || { echo "UNRESOLVED base $BASE"; exit 2; }
MDL=${MDL:-/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/k2/mdlint/node_modules/.bin/markdownlint-cli2}
SLUG=after-0926-kits-design-infra-backend-rust
T=$(mktemp -d "${TMPDIR:-/tmp}/k2m.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT

f() { git -C "$R" show "$H:$1"; }                       # 끝 판의 파일 내용
cnt() { f "$1" | grep -cE -- "$2"; }                     # 끝 판 파일에서 정규식 줄 수
line() { f "$1" | grep -E -- "$2"; }                     # 기준 줄 뽑기
has() { printf '%s\n' "$1" | grep -qF -- "$2" && echo 1 || echo 0; }
sect() { f "$1" | awk -v h="$2" 'index($0,h)==1{p=1;print;next} p&&/^## /{exit} p'; }   # 머리 줄부터 다음 ## 앞까지

DR=design-kit/agents/design-reviewer.md
DA=design-kit/skills/design-audit/SKILL.md
DAC=design-kit/skills/design-audit/references/audit-criteria.md
DM=design-kit/skills/design-mockup/SKILL.md
DMG=design-kit/skills/design-mockup/references/mockup-guidelines.md
DG=design-kit/skills/design-guide/SKILL.md
DS=design-kit/skills/design-system/SKILL.md
VCP=design-kit/references/visual-change-protocol.md
IT=infra-kit/skills/infra-test/SKILL.md
ITH=docs/infra-kit/infra-test.html
IA=infra-kit/skills/infra-audit/SKILL.md
ILOG=docs/infra/research-log.md
BS=backend-kit/skills/backend-system/SKILL.md
BA=backend-kit/skills/backend-audit/SKILL.md
BAC=backend-kit/skills/backend-audit/references/audit-criteria.md
BLOG=docs/backend/research-log.md
RPD=rust-kit/references/project-detection.md
RRUN=rust-kit/skills/rust-run/SKILL.md
RPRE=rust-kit/skills/rust-preflight/SKILL.md
RINIT=rust-kit/skills/rust-init/SKILL.md
RAC=rust-kit/skills/rust-audit/references/audit-criteria.md
RMW=rust-kit/skills/rust-middleware/SKILL.md
RTPL=rust-kit/templates/rust-init.toml.template

# infra-test 골격 스크립트를 SKILL.md 코드 블록에서 뗀다
skill_script() {
  f "$IT" | awk '/^```bash$/{inb=1; buf=""; next}
    inb && /^```$/ { if (buf ~ /tests\/ci-validation\.sh/) { printf "%s", buf; exit } inb=0; next }
    inb { buf = buf $0 "\n" }'
}
html_script() {
  f "$ITH" | python3 -c '
import html, re, sys
s = sys.stdin.read()
m = re.search(r"<pre><code>(#!/usr/bin/env bash\n# tests/ci-validation\.sh.*?)</code></pre>", s, re.S)
sys.stdout.write(html.unescape(m.group(1)) + "\n" if m else "")'
}

# 도구 조합 네 환경에서 골격을 돌린다 — PATH 는 심볼릭 링크만 둔 빈 폴더
run_envs() {
  local sc="$1" bash_bin py_yaml py_noyaml grep_bin e d out rc
  bash_bin=$(command -v bash)
  py_yaml=$(python3 -c 'import sys, yaml; print(sys.executable)' 2>/dev/null)
  py_noyaml=/usr/bin/python3
  grep_bin=$(command -v grep)
  /usr/bin/python3 -c 'import yaml' 2>/dev/null && { echo "PREMISE_BROKEN /usr/bin/python3 에 PyYAML 이 있다"; return; }
  [ -n "$py_yaml" ] || { echo "PREMISE_BROKEN PyYAML 있는 python3 없음"; return; }
  mkdir -p "$T/fx/.github/workflows"
  printf '%s\n' 'name: ci' 'on: push' 'jobs:' '  build:' '    runs-on: ubuntu-latest' '    steps:' \
    '      - uses: actions/checkout@0123456789abcdef0123456789abcdef01234567' > "$T/fx/.github/workflows/ci.yml"
  for e in E1 E2 E3 E4; do
    d="$T/bin-$e"; mkdir -p "$d"
    case "$e" in
      E1) ln -s "$py_yaml" "$d/python3" ;;
      E2) : ;;
      E3) ln -s "$grep_bin" "$d/grep" ;;
      E4) ln -s "$py_noyaml" "$d/python3" ;;
    esac
    out=$(cd "$T/fx" && PATH="$d" "$bash_bin" "$sc" 2>&1); rc=$?
    printf '%s rc=%s grepmiss=%s falseviol=%s copass=%s\n' "$e" "$rc" \
      "$(printf '%s\n' "$out" | grep -cE '^EXECUTION_ERROR.*grep')" \
      "$(printf '%s\n' "$out" | grep -c 'checkout 스텝 없음')" \
      "$(printf '%s\n' "$out" | grep -c 'checkout 존재')"
  done
}

# 더한 줄에 걸린 markdownlint 경고 수 (MD013 끔 — 편집기와 같은 설정)
md_new_warn() {   # md_new_warn <cfg json> → 파일별 "path new=N" 와 합계
  local cfg="$1" total=0 p n
  printf '%s' "$cfg" > "$T/.markdownlint-cli2.jsonc"
  while IFS= read -r p; do
    mkdir -p "$T/md/$(dirname "$p")"; f "$p" > "$T/md/$p"
    git -C "$R" diff -U0 "$BASE" "$H" -- "$p" | awk '/^@@/{ split($3,a,","); s=substr(a[1],2)+0; c=(a[2]==""?1:a[2]+0); for(i=0;i<c;i++) print s+i }' > "$T/added"
    ( cd "$T/md" && "$MDL" --config "$T/.markdownlint-cli2.jsonc" "$p" 2>&1 ) | grep -oE "^$p:[0-9]+" | awk -F: '{print $NF}' | sort -u > "$T/warn"
    n=$(grep -cxFf "$T/added" "$T/warn")
    echo "$p new=$n"; total=$((total + n))
  done < <(git -C "$R" diff --name-only "$BASE" "$H" -- '*.md' ':(exclude).harness')
  echo "TOTAL new=$total"
}

case "$1" in
SK-01)
  a=$(cnt "$DR" 'CONDITIONAL'); b=$(( $(cnt "$DA" 'CONDITIONAL') + $(cnt design-kit/skills/design-audit/templates/audit-report.md 'CONDITIONAL') ))
  l3=$(cnt "$DR" 'L3 < 10/10'); l3n=$(line "$DR" 'L3 < 10/10' | grep -vc 'REJECT')
  v=$(f "$DR" | grep -cxF '**판정: {{APPROVE | REJECT | BLOCKED}}**')
  al3=$(sect "$DA" '## Step 5' | grep 'L3' | grep -c 'REJECT')
  ( cd "$R" && python3 scripts/check-reviewer-protocol-copies.py >/dev/null 2>&1 ); cp=$?
  echo "a=$a b=$b l3_ok=$([ "$l3" -ge 1 ] && echo 1 || echo 0) l3_norej=$l3n verdict=$v audit_l3=$([ "$al3" -ge 1 ] && echo 1 || echo 0) copies=$cp" ;;
SK-02)
  old=$(( $(cnt "$DAC" '1\.2~1\.6') + $(cnt "$DR" '1\.2~1\.6') + $(cnt "$DA" '1\.2~1\.6') ))
  row=$(line "$DAC" '^\| 행간 비율'); rv=$(line "$DR" '^- 행간 비율'); ty=$(line "$DA" '^\| \*\*Typography\*\* \|')
  echo "old=$old row=$( [ "$(has "$row" 'typography.md')$(has "$row" '한글')" = 11 ] && echo 1 || echo 0) reviewer=$(has "$rv" 'audit-criteria') nowcag=$( [ -n "$row" ] && [ "$(has "$row" 'WCAG 1.4.12')" = 0 ] && echo 1 || echo 0) audit=$( [ "$(has "$ty" '행간')$(has "$ty" 'audit-criteria')" = 11 ] && echo 1 || echo 0)" ;;
SK-03)
  g=0
  for p in $(git -C "$R" ls-tree -r --name-only "$H" -- design-kit | grep -E '\.md$' | grep -v '/docs/' | grep -vx "$VCP"); do
    g=$((g + $(cnt "$p" '(기존 화면이? \**[0-9]+ ?개|최대 [0-9]+ ?회)')))
  done
  out=""
  for spec in "$DR|^- 같은 역할 관례 일치" "$DAC|^\| 같은 역할 관례 일치" "$DM|^- 앱 코드 존재" "$DM|스스로 고치기" "$DG|§0 관례 표"; do
    p=${spec%%|*}; re=${spec#*|}
    L=$(line "$p" "$re")
    n=$(printf '%s' "$L" | grep -c .); d=$(printf '%s\n' "$L" | grep -cE '[0-9]+ ?(개|회)'); s=$(has "$L" 'skill-design-guide')
    out="$out n=$n num=$d guide=$s;"
  done
  echo "global=$g |$out" ;;
SK-04)
  old=0
  for p in $(git -C "$R" ls-tree -r --name-only "$H" -- design-kit | grep -E '\.md$' | grep -v '/docs/'); do old=$((old + $(cnt "$p" 'OKLCH 미지원'))); done
  L=$(line "$DS" '^12\. \*\*컬러 primitive')
  m=1; for w in Hex HSB HSL CSS RGB; do [ "$(has "$L" "$w")" = 1 ] || m=0; done
  echo "old=$old url=$(has "$L" 'help.figma.com/hc/en-us/articles/360043042113') models=$m" ;;
SK-05)
  seq=$(f "$DM" | grep -oE '^## Step [0-9]+' | awk '{print $3}' | paste -sd, -)
  first=$(f "$DM" | grep -E '^## Step ' | head -1)
  o3=$(( $(cnt "$DM" 'Step 3-a') + $(cnt "$DMG" 'Step 3-a') )); n2=$(cnt "$DM" '^### Step 2-a')
  g13=$(line "$DM" '^13\. ' | grep -c 'Step 5 에서')
  echo "seq=$seq first=$([ "$first" = '## Step 0: 자동 감지 및 로드' ] && echo 1 || echo 0) old3a=$o3 new2a=$n2 g13=$g13" ;;
SK-06)
  L=$(line "$VCP" '캡처 자체가 실패')
  echo "cap=$(printf '%s' "$L" | grep -c .) four=$(has "$L" '네 칸') guide=$(has "$L" 'skill-design-guide')" ;;
SK-07)
  echo "old_skill=$(cnt "$IT" 'YAML 파싱 실패') old_html=$(cnt "$ITH" 'YAML 파싱 실패') new_skill=$(cnt "$IT" 'YAML 읽기 실패') new_html=$(cnt "$ITH" 'YAML 읽기 실패')" ;;
SK-08)
  out=""
  for p in infra-kit/references/principle-index.md infra-kit/skills/infra-guide/references/principle-index.md \
           infra-kit/references/audit-criteria.md infra-kit/references/init-checklist.md \
           infra-kit/skills/infra-init/references/init-checklist.md; do
    out="$out $(f "$p" | grep -F 'raw.githubusercontent.com/joo6077/claude-plugins/main/' | grep -c '못 읽')"
  done
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 https://raw.githubusercontent.com/joo6077/claude-plugins/main/docs/infra/platform/cicd.md)
  echo "files=$out http=$code" ;;
SK-09)
  S9=$(sect "$ILOG" '## [2026-09-26]')
  ok=1; for w in 'ex/EX-8.md' 'kubernetes.io/releases' '1.37.0' '2026-08-26' '1.35' 'v2.9.5' '2026-08-31' 'v3.5.3' '2026-09-14'; do [ "$(has "$S9" "$w")" = 1 ] || ok=0; done
  M=$(f "$IA" | grep -F 'fallback 시도' | grep -F '시도한 우회' | grep -F '실패 로그' | grep -cF '막는 것')
  echo "sec=$(printf '%s' "$S9" | grep -c '^## \[2026-09-26\]') words=$ok lu=$(f "$ILOG" | grep -cx 'last_updated: 2026-09-26') map=$M" ;;
SK-10)
  a=0
  for spec in "$BS|^\| API 규격 \|" "$BA|^\| 5 \| API Design \|" "$BAC|^\| OpenAPI 3\.1 JSON Schema 호환"; do
    p=${spec%%|*}; re=${spec#*|}; L=$(line "$p" "$re")
    [ "$(has "$L" '3.1 이상')$(has "$L" '최소 지원선')" = 11 ] && a=$((a + 1))
  done
  S10=$(sect "$BLOG" '## [2026-09-26]')
  ok=1; for w in 'ex/EX-7.md' 'spec.openapis.org/oas/latest.html' '3.2.1' 'asyncapi/spec/releases/tag/v3.1.0' '2026-01-31'; do [ "$(has "$S10" "$w")" = 1 ] || ok=0; done
  echo "anchors=$a sec=$(printf '%s' "$S10" | grep -c '^## \[2026-09-26\]') words=$ok lu=$(f "$BLOG" | grep -cx 'last_updated: 2026-09-26')" ;;
SK-11)
  pd=$(f "$RPD" | grep -A1 -E '^- 출처: 2026-07 실측' | grep -c 'myapp')
  kp=$(f "$RPD" | grep -cE '^- 출처: 2026-07 실측')
  ru=$(line "$RRUN" '^9\. \*\*타깃 필터'); pr=$(line "$RPRE" '^7\. \*\*마이그레이션 미적용')
  ex=$(f "$RRUN" | grep -cE '^   - `.*cargo run -p myapp-(api|migration)`')
  echo "pd=$pd run=$(printf '%s' "$ru" | grep -c myapp) pre=$(printf '%s' "$pr" | grep -c myapp) kept=$((kp + $(has "$ru" '실측') + $(has "$pr" '실측'))) examples=$ex"
  echo "init_old=$(cnt "$RINIT" '^name = "myapp-api"$') init_new=$(cnt "$RINIT" '^name = "\{project\}-api"$')" ;;
SK-12)
  S13=$(sect "$RAC" '## 7. API Design'); L=$(printf '%s\n' "$S13" | grep -E '^\| 시각 종류별 저장 \|')
  ok=1; for w in '벽시계' 'IANA' 'FAIL' 'sqlx-patterns.md'; do [ "$(has "$L" "$w")" = 1 ] || ok=0; done
  echo "row=$(printf '%s' "$L" | grep -c .) words=$ok cats=$(cnt "$RAC" '^## ')" ;;
SK-13)
  U=$(line "$RAC" '^\| OpenAPI 정합 \|'); TC=$(line "$RPD" '^\| `testcontainers` \|')
  echo "utoipa=$([ "$(has "$U" 'Step 2c')$(has "$U" '5.4')" = 10 ] && echo 1 || echo 0) tc=$(printf '%s\n' "$TC" | grep -vc '| 0\.27 |$') mw=$(line "$RMW" '^2\. \*\*tower-http' | grep -c 'Step 2c') init_ok=$([ "$(cnt "$RINIT" 'Step 2c')" -ge 3 ] && echo 1 || echo 0) tpl=$(cnt "$RTPL" 'Step 2c')" ;;
SC-01|ER-01)
  sc="$T/ci-validation.sh"; skill_script > "$sc"
  bash -n "$sc" && echo "syntax=0" || echo "syntax=1"
  run_envs "$sc" ;;
SC-02)
  skill_script > "$T/a"; html_script > "$T/b"
  echo "skill_lines=$(grep -c '' "$T/a") html_lines=$(grep -c '' "$T/b") same=$(cmp -s "$T/a" "$T/b" && echo 1 || echo 0)" ;;
AP-03|AP-04)
  cd "$R" || exit 2
  chk=$([ "$1" = AP-03 ] && echo code-fence || echo frontmatter); bad=0
  for k in design-kit infra-kit backend-kit rust-kit; do python3 scripts/validate-plugin.py "$k" --check="$chk" >/dev/null 2>&1 || bad=$((bad + 1)); done
  echo "check=$chk fail_kits=$bad" ;;
RE-02)
  echo "added=$(git -C "$R" diff --diff-filter=A --name-only "$BASE" "$H" -- . ':(exclude).harness' | grep -c .)" ;;
DG-02)
  md_new_warn '{ "config": { "MD013": false } }' ;;
DG-02P)   # 양성 대조 — MD013 을 켜면 같은 측정이 새 줄의 긴 줄을 잡는다
  md_new_warn '{ "config": { "default": true } }' | tail -1 ;;
AR-01)
  git -C "$R" diff --name-only "$BASE" "$H" -- . ':(exclude).harness' | LC_ALL=C sort > "$T/got"
  printf '%s\n' \
    design-kit/agents/design-reviewer.md design-kit/references/visual-change-protocol.md \
    design-kit/skills/design-audit/SKILL.md design-kit/skills/design-audit/references/audit-criteria.md \
    design-kit/skills/design-guide/SKILL.md design-kit/skills/design-mockup/SKILL.md \
    design-kit/skills/design-mockup/references/mockup-guidelines.md design-kit/skills/design-system/SKILL.md \
    infra-kit/skills/infra-test/SKILL.md docs/infra-kit/infra-test.html \
    infra-kit/references/principle-index.md infra-kit/skills/infra-guide/references/principle-index.md \
    infra-kit/references/audit-criteria.md infra-kit/references/init-checklist.md \
    infra-kit/skills/infra-init/references/init-checklist.md infra-kit/skills/infra-audit/SKILL.md \
    docs/infra/research-log.md \
    backend-kit/skills/backend-system/SKILL.md backend-kit/skills/backend-audit/SKILL.md \
    backend-kit/skills/backend-audit/references/audit-criteria.md docs/backend/research-log.md \
    rust-kit/references/project-detection.md rust-kit/skills/rust-run/SKILL.md \
    rust-kit/skills/rust-preflight/SKILL.md rust-kit/skills/rust-init/SKILL.md \
    rust-kit/skills/rust-audit/references/audit-criteria.md rust-kit/skills/rust-middleware/SKILL.md \
    rust-kit/templates/rust-init.toml.template | LC_ALL=C sort > "$T/allow"
  git -C "$R" diff --name-only "$BASE" "$H" -- .harness | LC_ALL=C sort > "$T/hgot"
  printf '%s\n' ".harness/sprint-contract-$SLUG.md" ".harness/sprint-amendments-$SLUG.md" \
    ".harness/sprint-feedback-$SLUG.md" ".harness/.meta/after-kaizen-0926b/k2-notes.md" | LC_ALL=C sort > "$T/hallow"
  echo "allow=$(grep -c . "$T/allow") changed=$(grep -c . "$T/got") outside=$(comm -23 "$T/got" "$T/allow" | grep -c .) missing=$(comm -13 "$T/got" "$T/allow" | grep -c .) harness_outside=$(comm -23 "$T/hgot" "$T/hallow" | grep -c .)" ;;
AR-02)
  first=""; mixed=0; multi=0; groups=""
  for c in $(git -C "$R" rev-list --reverse "$BASE..$H"); do
    files=$(git -C "$R" show --name-only --format='' "$c")
    [ -z "$first" ] && first=$c
    impl=$(printf '%s\n' "$files" | grep -v '^\.harness/' | grep -c .)
    hz=$(printf '%s\n' "$files" | grep -c '^\.harness/')
    [ "$impl" -gt 0 ] && [ "$hz" -gt 0 ] && mixed=$((mixed + 1))
    gs=$(printf '%s\n' "$files" | grep -v '^\.harness/' | sed -E \
      -e 's#^(design-kit)/.*#design#' -e 's#^(infra-kit|docs/infra|docs/infra-kit)/.*#infra#' \
      -e 's#^(backend-kit|docs/backend)/.*#backend#' -e 's#^rust-kit/.*#rust#' | grep -v '^$' | sort -u)
    [ "$(printf '%s' "$gs" | grep -c .)" -gt 1 ] && multi=$((multi + 1))
    groups="$groups $gs"
  done
  sf=$(git -C "$R" show --name-only --format='' "$first" 2>/dev/null)
  seal=$([ "$sf" = ".harness/sprint-contract-$SLUG.md" ] && echo 1 || echo 0)
  echo "seal_first=$seal mixed=$mixed multi_kit=$multi kits=$(printf '%s\n' $groups | grep -v '^$' | sort -u | paste -sd, -)" ;;
AR-03)
  cd "$R" || exit 2
  v=0; for k in design-kit infra-kit backend-kit rust-kit; do python3 scripts/validate-plugin.py "$k" >/dev/null 2>&1 || v=$((v + 1)); done
  python3 scripts/check-reviewer-protocol-copies.py >/dev/null 2>&1; c=$?
  python3 scripts/sync-docs.py --check-only >/dev/null 2>&1; s=$?
  python3 scripts/check-stale-values.py >/dev/null 2>&1; st=$?
  python3 scripts/run-evals.py >/dev/null 2>&1; e=$?
  python3 scripts/run-kaizen-assertions.py >/dev/null 2>&1; k=$?
  echo "validate_fail=$v copies=$c sync=$s stale=$st evals=$e assertions=$k" ;;
AR-03CI)   # 로컬 CI — 몇 분 걸린다. 도구는 읽기만 하고 사본을 돌린다
  CI=/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh
  cp "$CI" "$T/ci-local.sh"; mkdir -p "$T/ci"
  TMPDIR="$T/ci" bash "$T/ci-local.sh" "$R" > "$T/ci/out.txt" 2>&1
  echo "ci_ok=$(grep -c 'rc=0' "$T/ci/ci-local/summary.txt") ci_other=$(grep -v 'rc=0' "$T/ci/ci-local/summary.txt" | grep -vc '^feedback-agg-test SKIP (yq 없음)$')" ;;
AR-04)
  N=$(f .harness/.meta/after-kaizen-0926b/k2-notes.md 2>/dev/null)
  ids=0; for i in KD-1 KD-2 KD-3 KD-4 KI-1 KI-2 KI-3 KI-4 KB-1 KR-1 KR-2 KR-3; do [ "$(has "$N" "$i")" = 1 ] && ids=$((ids + 1)); done
  NT=$(printf '%s\n' "$N" | awk 'index($0,"## 톤 대조")==1{p=1;next} p&&/^## /{exit} p')
  NP=$(printf '%s\n' "$N" | awk 'index($0,"## 다시 만들 문서 페이지")==1{p=1;next} p&&/^## /{exit} p')
  NL=$(printf '%s\n' "$N" | awk 'index($0,"## 남은 것")==1{p=1;next} p&&/^## /{exit} p')
  echo "exists=$([ -n "$N" ] && echo 1 || echo 0) ids=$ids tone=$( [ "$(has "$NT" 'tone-guide 1 단계')$(has "$NT" 'tone-guide 5 단계')" = 11 ] && echo 1 || echo 0) pages=$(has "$NP" 'docs/design-kit/design-mockup.html') roots=$( [ "$(has "$NL" 'backend-kit')$(has "$NL" 'rust-kit')$(has "$NL" 'docs/')" = 111 ] && echo 1 || echo 0)" ;;
*) echo "unknown $1"; exit 2 ;;
esac
```
<!-- m.sh:end -->
