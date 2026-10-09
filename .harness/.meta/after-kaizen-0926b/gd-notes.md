# gd 묶음 기록 — harness 가이드 · 스킬 · 에이전트 (after-kaizen-0926b)

- 계약: `.harness/sprint-contract-after-0926-guides.md` — 봉인 커밋 `97d893b`,
  `conditions_digest: sha256:1774b0d356321753` · `measurement_digest: sha256:1292a5ca807199ca` (SEAL_OK · MEASURE_OK)
- 개정: `.harness/sprint-amendments-after-0926-guides.md` AM-01 — SK-19 측정 결함, `relaxing`, 동의 칸 채움(`a37fc21`, 사용자 선택지 답 2026-09-26T16:22:39Z). QA 2회차 APPROVE(33/33, N/A 4 제외) — 리포트 `29a7a1f`
- 가지 `chore/ak2-gd`, 시작점 `6378948`. QA 판정은 이 기록이 내리지 않는다 — 다음 단계 qa-evaluator 몫이다

## 항목별 결과

| ID | 결과 | 커밋 | 근거 |
| --- | --- | --- | --- |
| GD-1 | 계약에 넣음(SK-01 ~ SK-03) | `9ff9efe` | V8 FAIL 예시 2 를 reflect-kit 명령 둘과 실제 출력으로 바꿈 · 수동 수정 표 V8 행에 따옴표 · 변경 이력 1.4.2 · 출력 예시를 킷 하나 실행 모양(`Total: 1 plugins`)으로. `:400` 「큰따옴표로 감싸라」 문장은 처리됨 — `ex/EX-1.md` §2 판정 「맞음」(https://code.claude.com/docs/en/hooks#reference-scripts-by-path) |
| GD-2 | 계약에 넣음(SK-04 · SC-01) | `9ff9efe` · reviewer 일곱은 킷마다 `b9203db` `fe1a02e` `d8840e5` `98f86b3` `3209843` `383dab4` `85af2eb` | 둘째 `3.` 을 첫째 3 항의 이어지는 문단으로 합침(결정 1). 「현재 drift」 문단 대신 사본 검사 `scripts/check-reviewer-protocol-copies.py` 를 가리킴. 남은 일 목록의 「정본 절이 두 번(`:1236` · `:1308`)」 설명은 부정확했다 — `:1308` 은 다른 기준 절(사용자 보고 실패)이고 실제 결함은 한 절 안의 번호 `3.` 중복이었다(교차 진단 지적) |
| GD-3 | 계약에 넣음(SK-05 · SK-06) | `9ff9efe` · `1ad0754` | `model` 생략 순서(`ex/EX-2.md` §2.1, https://code.claude.com/docs/en/sub-agents) · 스킬 필수 필드와 다른 런타임 처리(`ex/EX-3.md` §A · §B · §D, https://code.claude.com/docs/en/skills · https://agentskills.io/specification). 서브에이전트 frontmatter 필수 필드(agent 가이드 `:70`)는 바깥 근거 없음 — EX-2 가 묻지 않았다. 고치지 않았다 |
| GD-4 | 계약에 넣음(SK-10) | `9ff9efe` | sprint-contract Step 6.7 · skill 가이드 §9 에 같은 작업 폴더 `checkout -b` 금지와 `git worktree add` |
| GD-5 | 계약에 넣음(SK-11 · SK-12) | `9ff9efe` · `d8840e5` · `1809bf1` | `/sprint` 판정 표 첫 줄을 시작 목록 · 귀속 불명으로 좁히고 CI 에서만 보이는 두 경우를 더함. 사본 셋(`docs/infra/platform/cicd.md` · rust-preflight · `docs/infra-kit/cicd.html`)을 글자 그대로 맞춤. rust-preflight 의 인용을 「남의 미커밋 후보」 로 |
| GD-6 | 계약에 넣음(SK-13 · SK-14) | `9ff9efe` · `b9203db` · `5389a59` · `fe1a02e` | skill 가이드 새 절 `## 8.9.` 에 두 숫자(2 개 이상 · 최대 3 회)와 한계. 세 규약이 §8.9 를 가리킨다 |
| GD-7 | 계약에 넣음(SK-15) | `9ff9efe` · `1ad0754` | §3.7 에 사본 네 가지(①~④)의 생성 측 짝과 「흔한 실수를 넣은 사본」 문단 |
| GD-8 | 계약에 넣음(SK-07 · SK-08 · SK-09) | `9ff9efe` | §7 오류 문구 · `omitClaudeMd` · `experimental`(`ex/EX-2.md` §2.3 · §2.4) · 편향 수(`ex/EX-4.md` §A, https://arxiv.org/html/2411.15594v6 · https://arxiv.org/html/2410.02736v1) · 평가 가이드 새 절 「문서 산출물일 때 — 문장 하나를 지운 사본으로 돌린다」. 처리됨 둘 — 평가 가이드 `:1944` 「12 개 편향 분류」(EX-4 「정확히 12」) · agent 가이드 배치 우선순위(EX-2 §2.2 와 같음). 중첩 깊이 상한 오류의 글자는 바깥 근거 없음(EX-2 「원문에 없음」) — 옛 문구 `Subagent spawn limit reached` 는 「찾지 못한 문구」 라고 적어 남겼다(계약 결정 4) |
| GD-9 | 계약에 넣음(SK-16) | `9ff9efe` | contract-kaizen · evaluator-kaizen Step 7 이 `python3 scripts/run-kaizen-assertions.py` 를 부르고 종료 코드 0 · 1 · 2 로 가른다 |
| GD-10 | 계약에 넣음(SK-17) | `9ff9efe` | sprint-contract Step 2.5 7 항 — 판정값을 바꾸는 계약은 `templates/` 리포트 틀까지 판정값 낱말로 찾는다 |
| GD-11 | 계약에 넣음(SK-18) | `9ff9efe` | `/sprint` Step 4 · qa-evaluator 에 「앞 회차 리포트를 커밋해 둔다」. 지우라고는 적지 않았다 — 지우면 Iteration 셈이 1 로 돌아간다 |
| GD-12 | 계약에 넣음(SK-19) | `9ff9efe` · `1ad0754` | harness-kaizen 커밋 규칙을 관행(바꾼 종류 머리 + 서명 줄 `Kaizen-Phase:`)에 맞춤. 표 예시는 실제 Phase 1 커밋 제목 |
| UD-5 | 계약에 넣음(SK-20 · SK-21 · SC-02 · SC-03 · ER-01) | `b9203db` · `1809bf1` | 결정 전파 `status: superseded` · `superseded_by`(같은 목록의 다른 `approved` 결정만, 사슬 금지). 검사 코드 · 시험 다섯 경우(21 경우) · design-test · design-audit · design-reviewer · 문서 사이트 한 쪽 |

## 교차 진단 반영 (봉인 전)

- SK-04 측정 대상에 design-reviewer · infra-reviewer · flutter 규약 · onboarding setup-guide 를 더했다. 뒤의 둘의 「조항 3」 은
  skill 가이드 §3.7 조항을 가리켜 도우미가 세지 않는다 — 진단이 예상한 분모 15 가 아니라 14 다
- 사용자 결정 UD-7(범위 밖 markdownlint 경고 전부 고친다)과 VS-26 — VS-26 은 같은 이어작업의 마지막 단계에서 부모가 모든 묶음 위에 한 번에 고친다.
  이 묶음은 자기가 더한 줄의 새 경고만 0 으로 맞췄다(DG-02 `md_new=0 sh_new=0`)
- AR-02 를 좁혀 넘길 것의 내용 짝을 요구하게 했다(아래 두 줄)

## 뒤따를 일

- KD-3 — design-kit 다섯 자리가 화면 규약 숫자(2 개 이상 · 3 회)를 다시 정의한다. 기준 원본은 이제 skill 가이드 §8.9 이니 다섯 자리는 §8.9 를 가리키게 고친다
- CS-3 — 평가 가이드 「한계」 문단의 「①~④ 의 짝은 다음 사이클 Phase 1 · 2 로 넘긴다」 문장. 생성 측 짝은 이 묶음이 skill 가이드 §3.7 에 넣었고, 계약 측 짝은 cs 묶음 몫이다. 두 묶음이 끝나면 부모가 그 문장을 ①~④ 의 짝 위치(§3.7 · contract-schema)로 한 번에 바꾼다

## tone-guide 대조 (5 단계)

1 단계에서 `.claude/tone-project.md`(어댑터 없음 · 주석 언어 ko)와 코어 네 파일 · `locale-korean.md` 규칙표를 읽었다. 대조 대상은 이 묶음이 더한 줄이다.

| 패턴 / 규칙 | 건수 | 판정 |
| --- | --- | --- |
| K-02 · G-1 번역투 6 종 | 8 | 통과 — 여덟 줄 모두 평가 가이드 원문과 reviewer 일곱이 글자 그대로 드는 「적용된다」 줄(번호 `3. ` 만 뗐다). 사본 검사가 글자 일치를 요구해 고치지 않는다. 한 건(create-skill 「skills 에 대해」)은 고쳤다 |
| K-04 · G-2 종결형 혼용 | 0 | 통과 — `합니다` · `습니다` 0 |
| K-11 새 이름 | 0 | 통과 — 「세 벌」 · 「앞 회차」 · 「사본 네 가지」 는 일상어이거나 원문 이름 |
| K-05 음역 | 0 | 관측 컨벤션 — 「런타임」 · 「러너」 는 레포에 이미 쓰던 말이라 새로 들이지 않았다 |
| C-01 · C-02 why 주석 | 3 | 통과 — 검사 코드 주석 둘(번호별 상태를 먼저 모으는 이유 · 대체된 결정이 건너뛰는 이유) · 시험 주석 하나, 모두 이유 |
| C-07 · C-15 | 0 | 통과 — 세 줄 넘는 해설 주석 없음 |
| N-08 한 글자 이름 | 0 | 통과 — 새 이름은 `status_by_id` · `superseded` · `by` · `NEXT`. `d` · `s` 는 원래 있던 이름 |
| S-01 ~ S-07 | 0 | 통과 — 새 함수 · 파일 없음. 기존 시험에 입력 열만 더했다 |
| 쉬운 말 목록(AR-03) | 0 | 통과 — `new_hits=0`. 처음 커밋에서 5 건(정본 · API · 스키마)이 나와 `1ad0754` 에서 풀어 썼다 |

## 킷별 버전 판단 (릴리스는 부모가 PR 을 합친 뒤)

| 킷 | 판단 | 이유 |
| --- | --- | --- |
| harness | minor | 평가 가이드에 새 절차(문장 하나를 지운 사본 · 판별 못 하면 `[미검증:INVALID]`)와 skill 가이드 새 절 §8.9, `/sprint` 판정 표가 받는 경우 둘이 늘었다 — 판정 결과가 바뀔 수 있다 |
| design-kit | minor | 결정 전파 검사가 새 상태 값 `superseded` 를 받는다(뒤로 호환 — 옛 목록은 그대로 통과) |
| flutter-toolkit · react-kit · rust-kit · api-kit · backend-kit · infra-kit · planning-kit | patch | 인용 · 사본 문장만 바뀌었다 |

## 다시 만들 문서 페이지

`python3 scripts/detect-docs-drift.py --since 6378948` 출력(원본 → 페이지):

- `design-kit/references/visual-change-protocol.md` → `docs/design-kit/visual-change-protocol.html` — 이 묶음이 직접 고쳤다(검사 코드 블록 · 상태 값 문단 · 종료 코드 2 행). 나머지 칸은 다시 만들 때 원본과 대조
- `design-kit/skills/design-test/SKILL.md` → `docs/design-kit/design-test.html`
- `docs/infra/platform/cicd.md` → `docs/infra-kit/cicd.html` — 판정 표 첫 줄은 이 묶음이 직접 고쳤다
- `flutter-toolkit/references/visual-evidence-protocol.md` → `docs/flutter-toolkit/visual-evidence-protocol.html`
- `harness/docs/guides/agent-design-guide.md` → `docs/harness/agent-design-guide.html`
- `harness/docs/guides/plugin-validation-guide.md` → `docs/harness/plugin-validation.html`
- `harness/docs/guides/qa-evaluation-guide.md` → `docs/harness/qa-evaluation-guide.html`
- `harness/docs/guides/skill-design-guide.md` → `docs/harness/skill-design-guide.html`
- `react-kit/references/render-evidence-protocol.md` → `docs/react-kit/render-evidence-protocol.html`

## 측정 도구

- 계약 안 측정 도우미를 뗀 파일: `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/gd/gd-measure.sh`
  (부르는 틀 `run.sh` · markdownlint 설치 `mdl/` 같은 폴더). 끝 판 값은 부모에게 돌려준 답에 있다
- 로컬 CI: `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh`

## 남은 것

- `harness/README.md:477` 「추적 규칙」 절이 아직 `kaizen:` 머리 커밋 규칙을 적고 있다. GD-12 가 harness-kaizen SKILL.md `:194` · `:233` 을
  「바꾼 종류 머리 + 서명 줄 `Kaizen-Phase:`」 로 바꿨으니 README 한 줄도 같은 규칙으로 맞춘다. AUTO 표지 밖이라 `sync-docs.py --check-only` 가 못 잡는다
  (독립 검토, 막지 않는 결함. 재현: `git ls-files | grep -v '^\.harness' | xargs /usr/bin/grep -n 'kaizen: sprint-contract few-shot'`)
- 문서 페이지 재생성 — 위 목록. 문서 사이트 묶음이 모아서 한다
- KD-3 · CS-3 — 위 「뒤따를 일」
- VS-26 — 부모가 마지막 단계에서 한다
