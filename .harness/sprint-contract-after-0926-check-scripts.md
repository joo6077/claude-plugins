---
feature: "2026-09-26 남은 일 vs 묶음 — 검사 스크립트 (회귀 패턴 실행기 · validate-plugin V2 V3 V6 V8 V10 · sync-docs 표 · Phase 부트스트랩 · 드리프트 짝 · api-kit 문서 검사 · evals 킷 목록 · 수집기 묶기 · 옛 값 검사 범위)"
slug: after-0926-check-scripts
created: "2026-09-26 20:13"
complexity: "복잡"
conditions: 32
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:ed9ff4a91d3ab1cd
measurement_digest: sha256:7321baf2bcf86697
locked_at: "2026-09-26 20:23"
---

## 배경

- 사용자 위임 — 이 계약의 합의(sprint-contract Step 5)는 아래 위임으로 받은 것으로 적는다. 사용자에게 따로 묻지 않았다.
  - user `2026-09-26T10:09:00.557Z` 「123다실행해 그러면끝나?다음카이젠에왜넘기는데?」 — 넘긴 것도 지금 처리하라는 뜻 (세션 `bda55d45-296c-491f-89ba-b52042d58e72`)
  - AskUserQuestion 답 `2026-09-26T10:30:16.222Z` — 결정 UD-8 「검증 도구 V2 줄의 SKIP 글자를 판정(OK)에 맞춘다」
  - 그 전 위임 `2026-09-24T04:04:16.964Z` 「나한테 물어보지 말고 자동으로 끝까지」
  - 봉인된 조건을 느슨하게 하는 개정(허용 파일 늘리기 · 측정 대상 줄이기 · 문턱 낮추기)은 이 위임으로 동의 처리하지 않는다. 그런 개정은 개정 파일에 동의 칸을 비워 두고 부모가 사용자에게 묻는다
- 묶음: 남은 일 목록 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/leftovers.md` 「## vs」 절의 VS-1 · VS-2 · VS-4 · VS-5 · VS-6 · VS-9 · VS-10 · VS-12 · VS-13 · VS-14 · VS-15 · VS-21 · VS-27. 결정 파일은 같은 폴더 `decisions.md`.
- 작업 폴더 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-vsa`, 가지 `chore/ak2-vsa`, 시작 판 `6378948` (= origin/main, 목록의 줄 번호 기준 판). 이 가지는 한 주체만 커밋한다 — 범위는 시작 판에서 가지 끝까지의 누적 차이로 잰다.
- 같은 판에서 다른 묶음(harness 스크립트 · 계약 형식 · PRD 없음 규칙 · 문서 사이트)이 같은 파일을 고칠 수 있다. 바꿀 줄은 최소로 하고 이 묶음 항목에 없는 절은 건드리지 않는다. 기존 markdownlint 경고 정리(VS-26)와 로컬 CI 도구 단계 추가(VS-24)는 부모 몫이다.

## 리서치 소스

- 바깥 문서는 새로 찾지 않았다. 필요한 바깥 사실 하나는 부모가 받아 둔 원문 대조를 쓴다:
  - VS-2 — `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/ex/EX-1.md` 가 [Hooks reference — Reference scripts by path](https://code.claude.com/docs/en/hooks#reference-scripts-by-path) 의 「In shell form, wrap each placeholder in double quotes.」 를 인용한다. 중괄호 없는 `$CLAUDE_PLUGIN_ROOT` 도 셸이 같은 변수로 펼치므로 같은 따옴표 규칙을 받는다 (이 추론은 셸 규칙이지 문서 인용이 아니다)
- 코드 블록 여닫는 규칙은 V10 이 이미 따르는 CommonMark 0.31.2 §4.5 (가이드 1.4.1 절, 2026-09-26 교차 진단이 markdown-it · micromark 와 대조) — 새 조사 없음
- 저장소 안 근거: 메모 `project_after_kaizen_0924_pending.md` 1 번(정해 둔 설계 — 헬퍼 네 역할 · V3 는 모든 코드 블록 안 링크 제외 · V6 는 백틱 여는 줄만), `.harness/.meta/after-kaizen-0926/c1a-notes.md:27`(VS-5 「설명 전체 첫 문장」) · `:35`, `c1b-notes.md:38-39`(N4 · N5), `d1-notes.md:73-77`(드리프트 도구가 못 낸 넷), `kaizen-0924/f1-harness-followups-notes.md:132` · `:137`(F1H-81 · F1H-94), `kaizen-0924/phase14-notes.md:112`(VS-27)
- 바깥 근거 없음: VS-1 · VS-4 · VS-5 · VS-6 · VS-9 · VS-10 · VS-12 · VS-13 · VS-14 · VS-15 · VS-21 · VS-27 은 저장소 안 동작만 다룬다. MD060 판정은 편집기와 같은 markdownlint-cli2 0.23.2 로 실제로 돌려 잰다

## GAP 분석 · 개선안

### 복잡도 4 축

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 계층을 관통하나 | 검사 스크립트 · CI 워크플로 · 킷 README(생성물) · 기준 문서 · reflect-kit 훅 라이브러리 — 다섯 |
| 공개 API·계약 변경 | 출력 모양이 바뀌나 | 예 — validate-plugin V2 줄 글자, sync-docs 표 구분 줄 · 설명 칸, 실행기 판정, Phase 부트스트랩 범위, 드리프트 도구 새 검사 |
| 소비면 존재 | 받아 쓰는 쪽이 있나 | 예 — CI 단계, 킷 README 15 개, 검증 가이드 · 문서 페이지, 옛 봉인 계약의 측정 꼴, 오케스트레이터 |
| 회귀 위험 | 기존 동작이 깨질 길 | 예 — 검사가 좁아지거나 넓어져 CI 가 멈추거나 조용해질 수 있다 |

네 축 모두 예 → **복잡**. 기능 조건 수는 22 로 가이드 상한 20 을 넘는다. 부모가 이 묶음을 한 계약으로 배정했고 항목 13 개가 서로 다른 스크립트라, 나누면 같은 README 재생성 · 같은 가이드 판 번호를 두 계약이 나눠 갖게 된다. 그래서 나누지 않는다.

### 설정 리터럴 대조표

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | `bash -n scripts/release.sh` (DG-01 N/A 사유) |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | 같은 글자 (DG-03 N/A 사유) |
| `diagnostics.ide_exclude` | `[]` | 없음 — DG-02 는 markdownlint · 파이썬 컴파일 · 셸 문법 · JSON · actionlint 로 잰다 |
| `contract_categories[].id` / `prefix` | `Skill`/`SK` · `Script`/`SC` · `Error`/`ER` · `Architecture`/`AR` | 같은 넷 |
| `anti_patterns[].id` / `message` | `AP-01` 버전 하드코딩 · `AP-02` force push · `AP-03` bare code fence (`python3 scripts/validate-plugin.py --check=code-fence`) · `AP-04` frontmatter name 누락 | 넷 모두 (AP-03 은 킷 밖 파일까지 재려고 같은 CommonMark 규칙의 도우미를 쓴다) |

### 편집 전 감사 — 시작 판 `6378948` 을 실제로 읽은 줄

| 대상 파일 | 읽은 증거 (`파일:줄`) | 발견한 갭 | 조건 |
| --------- | --------------------- | --------- | ---- |
| `scripts/run-kaizen-assertions.py` | `:58-62` 값이 목록인지만 봄 · `:65` 세 칸 존재만 봄 · `:73` `REPO_ROOT / assertion["file"]` · `:81` `len(re.findall(...))` | 빈 목록은 아무것도 안 재고 통과, 빈 문자열에 맞는 패턴은 늘 1 건 이상, 글자가 아닌 `file` · `pattern` 은 TypeError 로 죽어 종료 코드 1 (실측 `trace=1`) | SC-01 · ER-01 |
| `scripts/validate-plugin.py` | `:235-238` V2 「`0 files — SKIP (no templates/)`」 + 상태 OK · `:312-328` V3 옛 토글 · `:518-521` V6 범위(`skills/*/references` 없음) · `:533-542` V6 옛 토글 · `:635-637` V8 변수 글자가 중괄호 꼴 하나 · `:653-666` 따옴표 판정 · `:853-857` V10 범위(저장소 `docs/<원본>` 없음) · `:924-926` 판정 꼬리 설명 | V3 · V6 는 `~~~` 블록 · 백틱 4 개 블록 · 줄 안 코드 줄에서 오판(합성 실측), V6 `--fix` 가 닫는 줄을 고침, V8 은 `$CLAUDE_PLUGIN_ROOT` 를 못 봄 | SC-02 · SC-03 · SC-04 · RE-01 · RE-02 |
| `harness/docs/guides/plugin-validation-guide.md` | `:3` `version: 1.4.1` · `:126` V2 SKIP 글 · `:151-170` V3 · `:293-321` V6(옛 토글 의사 코드 `:310`) · `:391-426` V8 · `:476-485` V10 범위(「V6 는 같은 범위로 넓히지 않았다」 `:483-484`) · `:694-695` 이력 | 코드 바뀌면 설명이 옛 글이 된다 | SC-14 |
| `scripts/sync-docs.py` · `scripts/plugin_utils.py` | `sync-docs.py:41-46` 표지 정규식이 빈칸 든 꼴만 · `:67-71` `first_line` · `:110` · `:123` · `:236-273` 표 구분 줄 `\|------\|` · `:288` 루트 플러그인 표 · `plugin_utils.py:77-89` 설명은 첫 줄만 | 빈칸 없는 표지는 조용히 무시(실측 `rc=0`), 설명 33 칸이 첫 문장과 다름, AUTO 블록 안 MD060 107 건 | ER-02 · SC-05 · SC-06 |
| `scripts/spawn-kaizen-phase.sh` | `:30` 도움말 「1 ~ 10」 · `:64-67` 범위 막기 · `:73-84` 이름 표 1~10 · `:116-118` 공통 선언 「모든 Phase 는 §1 (feedback) + §5 (validate-plugin) 공통 참조」 · `:119-121` 5~10 에 §2 · §3 | 수집기 §6 표(`scripts/collect-kaizen-data.py:1700-1716`, 17 행)와 어긋남 — 17 개 중 4 개만 맞음 | SC-07 |
| `scripts/detect-docs-drift.py` · `.claude/skills/docs-site/SKILL.md` | `detect-docs-drift.py:32-70` `SOURCE_TO_HTML` · `:74-96` `SOURCE_OVERRIDES` · `docs-site/SKILL.md:45-64` 사람용 표(「표를 고치면 스크립트도 같은 커밋에서」) | 넷 짝 없음(d1 실측), 표 ↔ 스크립트를 재는 검사 없음 | SC-08 · SC-09 · SK-01 |
| `scripts/check-api-kit-docs.py` | `:33-34` `EXTERNAL` 이 `<link\s` 를 통째로 잡음 | 12 쪽 모두 `../assets/site.css` 한 줄로 실패(실측 `0/12 PASS`, 사유 12 건 모두 외부 리소스) | SC-10 |
| `scripts/run-evals.py` · `scripts/sync-evals.py` · `api-kit/evals/evals.json` · `.github/workflows/ci.yml` | `run-evals.py:32-35` · `:64-65` · `sync-evals.py:32` · `:65-71` · `evals.json` 은 `cases` 열쇠에 `api-ui` 한 사례 · `ci.yml:133` 「run-evals.py 킷 목록 밖」 | 두 목록에 api-kit 없음, 넣기만 하면 `cases` 를 못 읽어 0 건 통과, 스킬 넷은 사례 없음 | SC-11 |
| `scripts/collect-kaizen-data.py` · `reflect-kit/hooks/_lib-project-id.sh` · `reflect-kit/skills/reflect-digest/SKILL.md` | `collect-kaizen-data.py:403-421` · `_lib-project-id.sh:63-78` `project_root` · `:229-233` 설명 · `:261` 비교 · `reflect-digest/SKILL.md:58` | 여섯 경로 종류 중 둘이 다름 — 지운 워크트리(수집기 `repo` · reflect `gone`), bare 레포 워크트리(수집기가 bare 폴더의 부모 이름) | SC-12 · SK-02 |
| `scripts/check-stale-values.py` | `:47-54` `SOURCE_DIRS` | 문서 사이트 표의 원본 가운데 `docs/onboarding-kit/examples` · `docs/flutter` · `docs/howto` 를 안 읽음 — 심은 옛 값 셋 모두 못 잡음. 킷 폴더 `onboarding-kit/` 은 이미 읽는다(`:57-59` `kit_dirs`, 2026-09-25) | SC-13 |
| `scripts/sync-orchestrator.py` | `:125-148` `infer_research_docs_dir` — 킷 → 원본 폴더 짝 열 개 | V10 이 같은 짝을 써야 한다 — 사본을 또 만들지 않는다 | RE-02 |

구현 후보가 둘 이상인 곳과 고른 것:

- VS-1 빈 문자열에 맞는 패턴 — (a) 빈 글에 맞으면 못 읽은 입력으로 종료 코드 2 / (b) 빈 맞음을 빼고 센다. (b) 는 `(?=…)` 처럼 폭 0 이 정상인 패턴을 망가뜨린다 → (a). 빈 목록은 픽스처 짝 없음과 같은 급이라 FAIL (종료 코드 1)
- VS-4 빈칸 없는 표지 — (a) 표지로 읽어 갱신 / (b) 짝 없는 표지처럼 파일 · 줄 번호와 함께 종료 코드 2. 쓰는 쪽 꼴을 하나로 모으려고 (b)
- VS-5 설명 칸 — 설명 전체(접힌 여러 줄)의 **첫 문장**. 첫 문장 = 줄을 이어 붙이고 빈칸을 하나로 줄인 글에서 처음 나오는 「마침표 뒤 빈칸 또는 글 끝」까지. 실측 123 개 설명 모두 마침표 문장이 있고 `|` · 약어 마침표는 0 개
- VS-6 표 구분 줄 — `| --- | --- |` 꼴 (다른 칸 수도 같은 꼴). 세 README 사본에 적용해 MD060 0 건을 확인했다
- VS-10 V2 줄 — 결정 UD-8 대로 `no templates/ — OK`. 봉인된 옛 계약(P11 · P13 · P14 · P16 · P17 DG-05 등)의 `— SKIP (no templates/)` 측정 꼴과는 어긋난다 — 그 계약들은 끝났고 다시 재지 않는다(notes 에 적는다)
- VS-12 — §2 · §3 배정을 수집기 §6 표의 행에 맞추고, 표가 17 Phase 라 부트스트랩 범위도 1~17 로 넓힌다. 11~17 의 슬러그 꼬리는 기존 꼴(킷 이름에서 `-kit` · `-toolkit` 을 뗌)을 따른다
- VS-12 의 §1 · §5 — 표를 따르지 않고 부트스트랩의 기존 공통 선언(`scripts/spawn-kaizen-phase.sh:116-118`)을 그대로 둔다. 표의 열 이름이 「주요 참조 섹션」이라 표는 Phase 마다 **먼저 볼 것**을 적고, 부트스트랩은 그 위에 전 Phase 공통 둘(피드백 · 검증 도구 상태)을 늘 얹는 설계다. 표를 따라 §1 · §5 를 빼면 Flutter · Rust · Bambu Phase 가 검증 도구 상태를 못 받는다. 표의 §0 은 표 머리말(`scripts/collect-kaizen-data.py:1689-1690` 「§0 (/insights) 가 존재할 때는 모든 Phase 가 §0 을 최우선 참조」)이 따로 선언해 부트스트랩이 적지 않는다 — 이번 범위 밖 (2026-09-26 교차 진단 지적 반영)
- VS-13 — 짝 넷은 원본 → 페이지로: 오케스트레이터 → `docs/process/kaizen-flow.html`, design-mockup → `docs/design-kit/design-mockup.html`, infra-test → `docs/infra-kit/infra-test.html`, api-kit 설계 기록 → 그 기록을 출처로 단 두 쪽(`multi-sample-pagination-variance.html` · `contract-extraction-modes.html`, `grep -l api-kit-design docs/api-kit/*.html` 실측). 맞대기 검사는 드리프트 도구 안에 두고 CI 한 단계로 늘 돈다
- VS-15 — 두 스크립트가 `cases` 열쇠도 읽고, run-evals 는 글자 한 줄짜리 assertion 과 `expect` 도 받는다. sync-evals 가 스킬마다 사례를 요구하므로 `api-init` · `api-probe` · `api-contract` · `api-verify` 사례 넷을 실제 글로 더한다(자리표시 글 금지)
- VS-21 — 어느 쪽 규칙을 따를지: 지운 워크트리는 수집기 쪽(본 레포 이름 — `scripts/test-collect-kaizen-data.py:181` 이 기대), bare 레포 워크트리는 reflect-kit 쪽(워크트리 자신 — `reflect-kit/evals/hooks/project-id-test.sh:52` 가 기대). 두 쪽을 하나씩 고친다
- VS-27 — `docs/onboarding-kit/examples` 만 넣지 않고, 같은 결함인 `docs/flutter` · `docs/howto` 도 넣는다(문서 사이트 표에 있고 지금 등록 옛 값 0 건 — 실측)
- RE-02 — V10 이 읽을 킷 → 원본 폴더 짝을 `scripts/plugin_utils.py` 에 한 번 두고 validate-plugin 과 sync-orchestrator 가 함께 쓴다. sync-orchestrator 는 `:125-148` 함수만 고친다(같은 파일 `:39` 는 다른 묶음 VS-11 몫)

### Counterpart — 바뀌는 모양을 받아 쓰는 반대편

| 바뀌는 것 (producer) | 받아 쓰는 쪽 (consumer) | 처리 |
| --- | --- | --- |
| V2 없음 줄 글자 | `harness/docs/guides/plugin-validation-guide.md:126` · `docs/harness/plugin-validation.html:308` · 끝난 옛 계약 측정 꼴 | 가이드는 SC-14. 페이지는 부모가 드리프트 목록으로 모아 다시 만든다 — 이번 계약의 **미완 쪽**으로 notes 에 적는다(AR-03). 옛 계약은 고치지 않는다 |
| sync-docs 표 구분 줄 · 설명 칸 | 킷 README 14 개 · 루트 `README.md` 플러그인 표 | 같은 가지에서 다시 만든다 — SC-05 · SC-06 이 `--check-only` 종료 코드 0 과 표 칸을 잰다 |
| 드리프트 도구 새 검사 | `.github/workflows/ci.yml` 새 단계 · `.claude/skills/docs-site/SKILL.md` 표 | SC-09 · SK-01 |
| Phase 부트스트랩 범위 | 도움말 · `.claude/skills/kaizen-orchestrator/SKILL.md` (실측 grep: 범위 숫자가 있는 줄 `:25` · `:173` · `:583` 모두 이미 「1~17」 — 고칠 것 없음) | SC-07 이 도움말을 잰다 |
| run-evals · sync-evals 킷 목록 | `ci.yml:133` 설명 · `api-kit/evals/api-ui.spec.js:33` (`skill === 'api-ui'` 만 거름 — 사례를 더해도 안 깨짐) | SC-11 이 CI 설명 줄과 시험 통과(DG-05 `api-ui-viewer`)를 잰다 |
| reflect-kit `project_root` 의 git 밖 동작 | `compute_project_id` (`:85`) · `facets_unmatched` (`:261`) · `reflect-digest/SKILL.md:58` | SC-12 · SK-02, reflect-kit 시험 셋은 DG-05 |
| 옛 값 검사 범위 | 없음 — 결과만 CI 가 본다 | SC-13 |

### 조건 작성 자문

- 이진 판정 — 조건마다 도우미 출력 한 줄의 기대 글자를 적는다. 시작 판 출력도 같이 적어 **고치기 전 판에서 FAIL** 이 나는 것(양성 대조)을 보인다
- 검사를 바꾸는 조건은 합성 입력으로 잡아야 할 것(양성)과 잡지 말아야 할 것(음성)을 함께 잰다
- 구현 누수 — 조건은 스크립트 이름 · 출력 글 · 종료 코드만 쓴다. RE-01 · RE-02 는 재사용 여부를 재는 구조 조건이라 소스 글자를 센다

## 범위 경계

입력 항목마다 처리:

| 항목 | 처리 | 조건 |
| --- | --- | --- |
| VS-1 회귀 패턴 실행기 빈틈 셋 | 계약에 넣음 | SC-01 · ER-01 |
| VS-2 V8 중괄호 없는 변수 (+가이드 V8 절) | 계약에 넣음 | SC-02 · SC-14 |
| VS-4 빈칸 없는 AUTO 표지 | 계약에 넣음 | ER-02 |
| VS-5 README 설명 칸 첫 문장 | 계약에 넣음 — 전 킷 README 재생성 | SC-05 |
| VS-6 표 구분 줄 MD060 | 계약에 넣음 — VS-5 와 같은 재생성 | SC-06 |
| VS-9 V3 · V6 코드 블록 판정 · V6 범위 · V10 저장소 원본 | 계약에 넣음. 메모의 「언어 힌트 없는 펜스 8 개 먼저 고침」은 할 일이 없다 — 여덟은 킷 `pr-template.md` 의 `~~~markdown` 블록 **안** 줄이라 새 판정에서 코드다(실측: 새 규칙으로 `skills/*/references/` 의 언어 힌트 없는 여는 줄 0 개, 옛 토글로 8 개) | SC-03 · SC-04 · SC-14 · RE-01 · RE-02 |
| VS-10 V2 없음 줄 글자 | 계약에 넣음 (UD-8) | SC-04 · SC-14 |
| VS-12 Phase 별 데이터 풀 절 | 계약에 넣음 — 범위 1~17 포함 | SC-07 |
| VS-13 드리프트 짝 넷 · 맞대기 검사 | 계약에 넣음 | SC-08 · SC-09 · SK-01 |
| VS-14 api-kit 문서 검사 같은 사이트 CSS | 계약에 넣음 | SC-10 |
| VS-15 evals 킷 목록 api-kit | 계약에 넣음 — api-kit 사례 넷 추가 | SC-11 |
| VS-21 수집기 ↔ reflect-kit 묶기 규칙 | 계약에 넣음 — 지금 facets 18 개 경로가 모두 살아 있어 실데이터 영향 0 (실측) | SC-12 · SK-02 |
| VS-27 옛 값 검사 onboarding-kit | 일부 처리됨 — 킷 폴더는 `scripts/check-stale-values.py:57-59` `kit_dirs()` 가 2026-09-25 부터 읽는다(실측 범위 26/26 에 포함). 남은 문서 사이트 원본만 계약에 넣음 | SC-13 |

범위 밖: 같은 절의 VS-3 · VS-7 · VS-8 · VS-11 · VS-16 ~ VS-20 · VS-22 · VS-23 · VS-25 (다른 묶음), VS-24 · VS-26 (부모). 문서 페이지 `docs/harness/plugin-validation.html` 다시 만들기(부모 · 문서 묶음), 킷 판 올림과 릴리스(부모), `scripts/sync-orchestrator.py:39` `KIT_SCOPE_DIRS`(VS-11).

커밋 규칙: `git add <경로>` 뒤 `git commit -o <경로>` · 킷 폴더를 건드린 커밋은 그 킷 폴더만 담는다(README 재생성은 킷마다 한 커밋) · `git add -A` · `git stash` · 푸시 · 가지 바꾸기 금지 · main 을 합치지 않는다.

notes 경로: `.harness/.meta/after-kaizen-0926b/vsa-notes.md` (부모가 정한 경로) — 구현이 쓴다. 적을 것: 항목 13 개의 처리와 커밋, 남은 것(문서 페이지 재생성 · 옛 계약 측정 꼴 · 다른 스크립트의 킷 목록 사본 · 킷 판 올림 — 이유와 함께), tone-guide 1 단계와 5 단계 결과 표, 문서 드리프트 도구 출력, 킷별 판 올림 판단, 측정 도구 경로.

커버리지 해소 (Step 6.5 (4) 검출기 몫 — 검출기가 낸 다섯 건):

- 커버리지 해소: SC-08 — 원본 넷은 `drift.sh` 의 `SRCS=` 줄이, 페이지 다섯과 짝은 같은 도우미 파이썬 블록의 `want` 목록이 글자 그대로 담는다. 짝 없는 설계 기록은 `find docs/superpowers/specs` 로 고른 `NEG` 다
- 커버리지 해소: SC-13 — 폴더 셋은 `stale.sh` 의 `for F in docs/onboarding-kit/examples/fcm-ios-setup-guide.md $(… find docs/flutter docs/howto …) $(… find docs/flutter -mindepth 2 …)` 가 파일 넷으로 펼치고(실측 펼친 결과 `docs/flutter/research-log.md` · `docs/howto/branch-catalog.md` · 하위 폴더 파일 `docs/flutter/architecture/api-layer.md`), 검사 스크립트는 `st()` 가 돌린다. 하위 폴더는 `docs/flutter` 넷 · `docs/howto` 하나 · `docs/onboarding-kit/examples` 0 (실측 `find -mindepth 2`) — 넷째 줄이 폴더 아래까지 읽는지(재귀)를 직접 잰다
- 커버리지 해소: SC-14 — 가이드 경로는 `guide.sh` 의 `G=` 가, `skills/*/references/` 는 같은 도우미의 `grep -cF` 가 글자 그대로 잰다
- 커버리지 해소: SK-01 — 원본 넷은 `misc.sh` 의 `for s in …` 가, docs-site 파일은 `DS=` 가 글자 그대로 담는다
- 커버리지 해소: AR-01 — `.harness/` 경로 규칙은 `scope.sh` 의 `HX=` 정규식이 잰다 (이 슬러그 파일 셋 + `.meta/after-kaizen-0926b/vsa-notes.md`)
- 오라클 해소: RE-01 — 소스 글자 측정은 옛 토글이 남았는지만 본다. 판정이 하나로 모여 실제로 도는지는 SC-03 의 합성 입력 열 줄(`v3-*` · `v6-*`)이 validate-plugin 을 돌려 잰다

## 회귀 게이트 — 측정 공통 정의 · 도우미 · 봉인 전 실측

모든 측정은 **bash** 에서 돈다(zsh 는 따옴표 없는 변수를 쪼개지 않는다). 도우미는 잴 판(`REF`, 비면 가지 끝 `chore/ak2-vsa`)을 `git archive` 로 임시 폴더에 풀고 거기서 잰다 — 작업 폴더는 건드리지 않는다. `END_UNRESOLVED` · `REF_UNRESOLVED` · `END_HAS_MERGE` · `PREMISE_FAIL` 이 찍히면 종료 코드 2 로 멈춘다. `HEAD` 로 바꿔 재지 않는다.

도우미 준비 — 이 절의 bash 코드 블록을 블록 첫 `#` 줄(셔뱅 다음)의 이름으로 한 폴더에 저장하고 그 폴더를 `K` 에 넣는다:

```bash
# 이 계약에서 도우미 블록을 떼어 $K 에 저장한다 — 블록 첫 주석 줄의 이름(셔뱅 다음 줄)이 파일 이름이다
K=${K:?도우미 폴더}; mkdir -p "$K"
python3 - /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-vsa/.harness/sprint-contract-after-0926-check-scripts.md "$K" <<'PY'
import re, sys, pathlib
src = open(sys.argv[1], encoding="utf-8").read(); K = pathlib.Path(sys.argv[2])
for body in re.findall(r"^```bash\n(.*?)^```$", src, re.S | re.M):
    lines = body.splitlines(); i = 1 if lines and lines[0].startswith("#!") else 0
    m = re.match(r"# ([\w.-]+\.sh) ", lines[i]) if len(lines) > i else None
    if m:
        (K / m.group(1)).write_text(body, encoding="utf-8")
PY
```

돌리는 법: `K=<폴더> bash "$K/<도우미>"` (시작 판으로 재려면 앞에 `REF=6378948`). `group.sh` 는 맥 기본 TMPDIR(`/var/folders/…`)로 돌린다 — TMPDIR 이 `/tmp` · `/private/tmp` 아래면 수집기가 경로를 시험 세션으로 묶어 버려 `PREMISE_FAIL` 로 멈춘다. 도우미 열넷: `asr.sh` (SC-01 · ER-01) · `vp.sh` (SC-02 · SC-03 · SC-04) · `sdocs.sh` (ER-02 · SC-05 · SC-06) · `spawn.sh` (SC-07) · `drift.sh` (SC-08 · SC-09) · `apidocs.sh` (SC-10) · `evals.sh` (SC-11) · `group.sh` (SC-12 · SK-02) · `stale.sh` (SC-13) · `guide.sh` (SC-14) · `scope.sh` (AR-01 · AR-02) · `misc.sh` (SK-01 · AR-03 · AP-01 · AP-02 · AP-04 · RE-01 · RE-02 · DG-01 · DG-03) · `dg.sh` (DG-02 · AP-03) · `ci.sh` (DG-05).

준비 단계 실측 (2026-09-26 19:4x ~ 20:0x): `node .../mdlint/node_modules/markdownlint-cli2/markdownlint-cli2-bin.mjs --version` 첫 줄 `markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)` (설정 `{ "config": { "MD013": false } }`) · `command -v actionlint` → `/opt/homebrew/bin/actionlint` · `python3 --version` → 3.14.3 · `python3 -c 'import yaml'` 성공 · `command -v jq` 있음 · `command -v yq` 없음(로컬 CI 의 `feedback-agg-test` 는 SKIP) · 로컬 CI 도구 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` 지문 `sha256` 앞 16 자 `59fe55125c0dbc77` (추적 안 된 파일 — 평가 때 지문이 다르면 `.github/workflows/ci.yml` 의 `run:` 줄을 하나씩 돌린다).

```bash
# common.sh — 측정 공통 정의. bash 로 읽는다 (`. "$K/common.sh"`)
export LC_ALL=C.UTF-8
W=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-vsa
B=6378948
BR=chore/ak2-vsa
MDL=/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/mdlint
# 잴 판 — REF 가 비면 가지 끝(END). HEAD 로 떨어지지 않는다
resolve_ref() {
  local r
  if [ -z "${REF:-}" ] || [ "$REF" = END ]; then
    r=$(git -C "$W" rev-parse --verify -q "refs/heads/$BR") || { echo END_UNRESOLVED; exit 2; }
  else
    r=$(git -C "$W" rev-parse --verify -q "$REF^{commit}") || { echo "REF_UNRESOLVED $REF"; exit 2; }
  fi
  printf '%s\n' "$r"
}
# unpack <commit> — 그 판을 임시 폴더에 풀고 경로를 찍는다. 작업 폴더는 건드리지 않는다
unpack() {
  local d
  d=$(mktemp -d "${TMPDIR:-/tmp}/vsa.XXXXXX") || exit 2
  git -C "$W" archive "$1" | tar -x -C "$d" || exit 2
  printf '%s\n' "$d"
}
```

```bash
#!/usr/bin/env bash
# asr.sh — SC-01: 회귀 패턴 실행기의 빈틈 셋과 실제 저장소 실행
K=${K:?}; . "$K/common.sh"; R=$(resolve_ref); T=$(unpack "$R")
run() { (cd "$T" && python3 scripts/run-kaizen-assertions.py >"$T/out.txt" 2>&1); echo $? ; }
rc=$(run); echo "real rc=$rc total=[$(tail -1 "$T/out.txt")] trace=$(grep -c Traceback "$T/out.txt")"
A="$T/harness/evals/kaizen/contract-kaizen/assertions.json"; cp "$A" "$T/orig.json"
# 빈 문자열에 맞는 패턴 — 대상 파일에 없는 낱말을 괄호로 묶어 * 를 붙였다
python3 - "$A" <<'PY'
import json, sys; p = sys.argv[1]; d = json.load(open(p, encoding="utf-8"))
d["ambiguous-conditions"][0]["pattern"] = "(없는낱말qzx)*"
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False)
PY
rc=$(run); echo "empty-match rc=$rc named=$(grep -cE '^UNREADABLE contract-kaizen/ambiguous-conditions#1' "$T/out.txt") trace=$(grep -c Traceback "$T/out.txt")"
cp "$T/orig.json" "$A"
python3 - "$A" <<'PY'
import json, sys; p = sys.argv[1]; d = json.load(open(p, encoding="utf-8"))
d["category-bias"] = []
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False)
PY
rc=$(run); echo "empty-list rc=$rc named=$(grep -cE '^FAIL contract-kaizen/category-bias' "$T/out.txt") trace=$(grep -c Traceback "$T/out.txt")"
for field in pattern file; do
  cp "$T/orig.json" "$A"
  python3 - "$A" "$field" <<'PY'
import json, sys; p, f = sys.argv[1], sys.argv[2]; d = json.load(open(p, encoding="utf-8"))
d["low-coverage"][0][f] = 7
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False)
PY
  rc=$(run); echo "nonstr-$field rc=$rc named=$(grep -cE '^UNREADABLE contract-kaizen/low-coverage#1' "$T/out.txt") trace=$(grep -c Traceback "$T/out.txt") others_measured=$(grep -cE '^PASS evaluator-kaizen/' "$T/out.txt")"
done
rm -rf "$T"
```

```bash
#!/usr/bin/env bash
# vp.sh — SC-02 · SC-03 · SC-04 · RE-02: validate-plugin V2 · V3 · V6 · V8 · V10 을 실제 저장소와 합성 입력으로 잰다
K=${K:?}; . "$K/common.sh"; R=$(resolve_ref); T=$(unpack "$R"); cp -R "$T" "$T.orig"
vp() { (cd "$T" && python3 scripts/validate-plugin.py "$@" >"$T/out.txt" 2>&1); echo $?; }
reset() { rm -rf "$T"; cp -R "$T.orig" "$T"; }
vline() { grep -E "^  $1 " "$T/out.txt" | head -1; }
rc=$(vp); echo "real rc=$rc vlines=$(grep -cE '^  V([1-9]|10) ' "$T/out.txt") not_ok=$(grep -E '^  V([1-9]|10) ' "$T/out.txt" | grep -cvE -- '— OK$')"
rc=$(vp api-kit --check=templates); echo "v2 rc=$rc line=[$(vline V2 | sed -E 's/ +/ /g')] skip=$(vline V2 | grep -c SKIP)"
# V3 — SKILL.md 끝에 합성 줄을 붙인다
S3=api-kit/skills/api-ui/SKILL.md
for c in tilde nested plain; do
  reset
  case $c in
    tilde)  printf '\n~~~text\n[a](없는-v3-tilde.md)\n~~~\n' >>"$T/$S3" ;;
    nested) printf '\n````markdown\n```text\n[b](없는-v3-nested.md)\n```\n````\n' >>"$T/$S3" ;;
    plain)  printf '\n[c](없는-v3-plain.md)\n' >>"$T/$S3" ;;
  esac
  rc=$(vp api-kit --check=refs); echo "v3-$c rc=$rc hit=$(grep -c "없는-v3-$c.md" "$T/out.txt")"
done
# V6 — 킷 README 끝 · 스킬 폴더 references 에 합성 블록을 붙인다
M6=api-kit/README.md; L6=$(wc -l <"$T/$M6" | tr -d ' ')
for c in tilde nested inline plain tildebare refs; do
  reset
  case $c in
    tilde)     printf '\n~~~text\n```\ncode\n```\n~~~\n' >>"$T/$M6" ;;
    nested)    printf '\n````markdown\n```\ncode\n```\n````\n' >>"$T/$M6" ;;
    inline)    printf '\n```x``` 는 줄 안 코드다\n\n```\nbare\n```\n' >>"$T/$M6" ;;
    plain)     printf '\n```\nbare\n```\n' >>"$T/$M6" ;;
    tildebare) printf '\n~~~\nbare\n~~~\n' >>"$T/$M6" ;;
    refs)      f=$(find "$T/api-kit/skills" -path '*/references/*.md' | sort | head -1); printf '\n```\nbare\n```\n' >>"$f" ;;
  esac
  rc=$(vp api-kit --check=code-fence)
  # inline 은 몇째 줄을 짚었는지도 본다 — 붙이기 전 줄 수 L 에서 여는 줄은 L+4, 옛 판은 닫는 줄 L+6 을 짚는다
  at=$(grep -oE "README.md:[0-9]+ — bare" "$T/out.txt" | grep -oE '[0-9]+' | head -1)
  echo "v6-$c rc=$rc fail=$(grep -cE '^ +FAIL .*bare' "$T/out.txt") at_offset=$(( ${at:-0} - L6 ))"
done
# V6 --fix — 줄 안 코드 뒤의 언어 힌트 없는 블록을 고치면 여는 줄(L+4)이 ```text 가 되고 다시 재면 0 이다
reset; printf '\n```x``` 는 줄 안 코드다\n\n```\nbare\n```\n' >>"$T/$M6"
vp api-kit --check=code-fence --fix >/dev/null; rc=$(vp api-kit --check=code-fence)
echo "v6-fix rc=$rc fail=$(grep -cE '^ +FAIL .*bare' "$T/out.txt") opener=[$(sed -n "$((L6 + 4))p" "$T/$M6")] closer=[$(sed -n "$((L6 + 6))p" "$T/$M6")]"
# V8 — design-kit hooks.json 명령 하나를 바꿔 본다
H=design-kit/hooks/hooks.json; SH=design-kit/scripts/env-check.sh
for c in unquoted quoted644 quoted755 otherVar interp644; do
  reset
  case $c in
    unquoted)  cmd='$CLAUDE_PLUGIN_ROOT/scripts/env-check.sh' ;;
    quoted644) cmd='"$CLAUDE_PLUGIN_ROOT/scripts/env-check.sh"'; chmod 644 "$T/$SH" ;;
    quoted755) cmd='"$CLAUDE_PLUGIN_ROOT/scripts/env-check.sh"'; chmod 755 "$T/$SH" ;;
    otherVar)  cmd='$CLAUDE_PLUGIN_ROOT_DIR/scripts/env-check.sh' ;;
    interp644) cmd='bash "$CLAUDE_PLUGIN_ROOT/scripts/env-check.sh"'; chmod 644 "$T/$SH" ;;
  esac
  python3 - "$T/$H" "$cmd" <<'PY'
import json, sys; p, c = sys.argv[1], sys.argv[2]; d = json.load(open(p, encoding="utf-8"))
d["hooks"]["SessionStart"][0]["hooks"][0]["command"] = c
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False)
PY
  rc=$(vp design-kit --check=hook-exec)
  echo "v8-$c rc=$rc quote=$(grep -c '큰따옴표 밖' "$T/out.txt") exec=$(grep -c '비실행' "$T/out.txt") checked=$(vline V8 | grep -oE '[0-9]+ hook 스크립트 실행 가능' | grep -oE '^[0-9]+')"
done
# V10 — 저장소 docs/<원본> 에 끊긴 표 행 하나
for c in research unmapped; do
  reset
  case $c in
    research) f=$(find "$T/docs/rust" -name '*.md' | sort | head -1); kit=rust-kit ;;
    unmapped) f=$(find "$T/docs/superpowers" -name '*.md' | sort | head -1); kit=rust-kit ;;
  esac
  printf '\n문단\n\n| 끊긴 | 표 |\n' >>"$f"
  rc=$(vp "$kit" --check=table-integrity); echo "v10-$c rc=$rc hit=$(grep -c "${f#$T/}" "$T/out.txt")"
done
# V10 결합 (RE-02) — 킷 → 원본 폴더 짝을 plugin_utils 에서 읽는가. 거기 rust 값만 없는 폴더로 바꾸면 V10 은 심은 표를 못 보고 없는 폴더를 이름으로 댄다
reset; f=$(find "$T/docs/rust" -name '*.md' | sort | head -1); printf '\n문단\n\n| 끊긴 | 표 |\n' >>"$f"
applied=$(grep -c '"docs/rust' "$T/scripts/plugin_utils.py"); sed -i '' 's#"docs/rust#"docs/rust-측정없음#' "$T/scripts/plugin_utils.py"
rc=$(vp rust-kit --check=table-integrity); echo "v10-coupled rc=$rc hit=$(grep -c "${f#$T/}" "$T/out.txt") gone=$(grep -c 'docs/rust-측정없음' "$T/out.txt") applied=$applied"
rm -rf "$T" "$T.orig"
```

```bash
#!/usr/bin/env bash
# sdocs.sh — ER-02 · SC-05 · SC-06: sync-docs 표지 · 표 설명 · 표 구분 줄
K=${K:?}; . "$K/common.sh"; R=$(resolve_ref); T=$(unpack "$R"); cp -R "$T" "$T.orig"
reset() { rm -rf "$T"; cp -R "$T.orig" "$T"; }
sd() { (cd "$T" && python3 scripts/sync-docs.py "$@" >"$T/out.txt" 2>&1); echo $?; }
rc=$(sd --check-only); echo "real rc=$rc need=$(grep -c '변경 필요' "$T/out.txt")"
# 빈칸 없는 표지 — api-kit README 의 skills 표지 한 쌍을 바꾼다
for c in nospace halfspace; do
  reset
  f="$T/api-kit/README.md"
  case $c in
    nospace)   sed -i '' -e 's/^<!-- AUTO:skills -->$/<!--AUTO:skills-->/' -e 's#^<!-- /AUTO:skills -->$#<!--/AUTO:skills-->#' "$f" ;;
    halfspace) sed -i '' -e 's/^<!-- AUTO:skills -->$/<!-- AUTO:skills-->/' -e 's#^<!-- /AUTO:skills -->$#<!--/AUTO:skills -->#' "$f" ;;
  esac
  o=$(grep -nE '^<!-- ?AUTO:skills ?-->$' "$f" | cut -d: -f1); e=$(grep -nE '^<!-- ?/AUTO:skills ?-->$' "$f" | cut -d: -f1)
  rc=$(sd --check-only)
  echo "marker-$c rc=$rc lines=$o,$e named=$(grep 'api-kit/README.md' "$T/out.txt" | grep -F "$o" | grep -cF "$e")"
done
reset
# 표 설명 — AUTO:skills · AUTO:agents 표의 설명 칸이 frontmatter 설명 전체의 첫 문장과 같은가
python3 - "$T" <<'PY'
import pathlib, re, sys, yaml
T = pathlib.Path(sys.argv[1])
def first_sentence(path):
    m = re.match(r"^---\n(.*?)\n---", path.read_text(encoding="utf-8"), re.S)
    d = " ".join(str(yaml.safe_load(m.group(1)).get("description", "")).split())
    s = re.search(r"\.(\s|$)", d)
    return d[: s.start() + 1] if s else d
rows = bad = 0; ex = []
for readme in sorted(T.glob("*/README.md")):
    kit = readme.parent
    text = readme.read_text(encoding="utf-8")
    for key, pat in (("skills", "skills/{}/SKILL.md"), ("agents", "agents/{}.md")):
        m = re.search(rf"<!-- AUTO:{key} -->\n(.*?)<!-- /AUTO:{key} -->", text, re.S)
        if not m:
            continue
        for line in m.group(1).splitlines():
            c = re.match(r"^\| `([^`]+)` \| (.*) \|$", line)
            if not c:
                continue
            src = kit / pat.format(c.group(1))
            if not src.exists():
                continue
            rows += 1
            if c.group(2) != first_sentence(src):
                bad += 1
                if len(ex) < 3:
                    ex.append(f"{readme.relative_to(T)} {c.group(1)}")
print(f"desc rows={rows} not_first_sentence={bad} ex={ex}")
PY
# 표 구분 줄 — sync-docs 가 쓰는 파일(킷 README · 루트 README)의 AUTO 블록 안 MD060 경고 수와 파일 전체 경고 수
python3 - "$T" "$MDL" <<'PY'
import pathlib, re, subprocess, sys
T, MDL = pathlib.Path(sys.argv[1]), sys.argv[2]
files = sorted(T.glob("*/README.md")) + [T / "README.md"]
out = subprocess.run(["node", f"{MDL}/node_modules/markdownlint-cli2/markdownlint-cli2-bin.mjs",
                      "--config", f"{MDL}/cfg.markdownlint-cli2.jsonc", *(str(f.relative_to(T)) for f in files)],
                     capture_output=True, text=True, cwd=T)
text = out.stdout + out.stderr
ranges = {}
for f in files:
    lines = f.read_text(encoding="utf-8").splitlines(); r = []; start = None
    for i, l in enumerate(lines, 1):
        if re.fullmatch(r"<!-- AUTO:[\w-]+ -->", l): start = i
        elif re.fullmatch(r"<!-- /AUTO:[\w-]+ -->", l) and start: r.append((start, i)); start = None
    ranges[str(f.relative_to(T))] = r
md060 = 0; total = {}
for m in re.finditer(r"^(\S+?):(\d+)(?::\d+)? (?:error )?(MD\d+)", text, re.M):
    f, n, rule = m.group(1), int(m.group(2)), m.group(3)
    total[f] = total.get(f, 0) + 1
    if rule == "MD060" and any(a < n < b for a, b in ranges.get(f, [])):
        md060 += 1
print(f"md060_in_auto={md060} lint_rc={out.returncode} files={len(files)}")
print("per_file " + " ".join(f"{k}={v}" for k, v in sorted(total.items())))
PY
rm -rf "$T" "$T.orig"
```

```bash
#!/usr/bin/env bash
# spawn.sh — SC-07: Phase 1~17 마다 부트스트랩이 내는 참조 절(§2 · §3)이 수집기 §6 표의 그 Phase 행과 같은가. §1 · §5 는 부트스트랩의 공통 선언이라 표가 아니라 전 Phase 포함 여부로 잰다
K=${K:?}; . "$K/common.sh"; R=$(resolve_ref); T=$(unpack "$R")
( cd "$T" && git init -q && git add -A && git -c user.name=m -c user.email=m@m commit -qm base ) || exit 2
# 기대값 — 수집기 소스의 §6 표 행을 읽는다 (구현 스크립트가 아니라 표가 기준)
python3 - "$T/scripts/collect-kaizen-data.py" >"$T/want.txt" <<'PY'
import re, sys
for m in re.finditer(r'"\| (\d+) [^|]*\| [^|]*\| ([^"]*)\|",', open(sys.argv[1], encoding="utf-8").read()):
    print(m.group(1), " ".join(sorted(set(re.findall(r"§[23]\b", m.group(2))))) or "-")
PY
echo "table_rows=$(wc -l <"$T/want.txt" | tr -d ' ')"
ok=0; common=0; bad=""
for n in $(seq 1 17); do
  out=$(cd "$T" && bash scripts/spawn-kaizen-phase.sh "$n" 2>/dev/null); rc=$?
  got=$(printf '%s\n' "$out" | sed -n 's/^\*\*참조 섹션:\*\* //p' | grep -oE '§[23]\b' | sort -u | tr '\n' ' ' | sed 's/ $//')
  printf '%s\n' "$out" | grep '^\*\*참조 섹션:\*\*' | grep -q '§1' && printf '%s\n' "$out" | grep '^\*\*참조 섹션:\*\*' | grep -q '§5' && common=$((common + 1))
  want=$(awk -v n="$n" '$1==n { $1=""; sub(/^ /, ""); print }' "$T/want.txt")
  [ "$want" = "-" ] && want=""
  if [ "$rc" = 0 ] && [ "$got" = "$want" ]; then ok=$((ok + 1)); else bad="$bad $n(rc=$rc got=[$got] want=[$want])"; fi
  ( cd "$T" && git tag -d "kaizen-phase-$n-pre" >/dev/null 2>&1; git checkout -q -- .harness/.meta/kaizen-state.yaml )
done
echo "phases_ok=$ok/17 common_1_5=$common/17 bad=[${bad# }]"
out=$(cd "$T" && bash scripts/spawn-kaizen-phase.sh 18 2>&1); echo "phase18 rc=$? help_17=$(cd "$T" && bash scripts/spawn-kaizen-phase.sh --help | grep -cE '1 ?~ ?17')"
rm -rf "$T"
```

```bash
#!/usr/bin/env bash
# drift.sh — SC-08 · SC-09: 드리프트 도구 짝 넷과, 매핑 표 ↔ 스크립트 맞대기 검사
K=${K:?}; . "$K/common.sh"; R=$(resolve_ref); T=$(unpack "$R")
( cd "$T" && git init -q && git add -A && git -c user.name=m -c user.email=m@m commit -qm base ) || exit 2
SRCS=".claude/skills/kaizen-orchestrator/SKILL.md design-kit/skills/design-mockup/SKILL.md infra-kit/skills/infra-test/SKILL.md docs/superpowers/specs/2026-09-02-api-kit-design.md"
NEG=$(cd "$T" && find docs/superpowers/specs -name '*.md' ! -name '2026-09-02-api-kit-design.md' | sort | head -1)
for f in $SRCS $NEG; do printf '\n드리프트 측정용 한 줄\n' >>"$T/$f"; done
( cd "$T" && git -c user.name=m -c user.email=m@m commit -qam probe ) || exit 2
(cd "$T" && python3 scripts/detect-docs-drift.py --since HEAD~1 --json >"$T/drift.json" 2>"$T/drift.err"); echo "drift rc=$?"
python3 - "$T/drift.json" "$NEG" <<'PY'
import json, sys
got = {(e["source"], e["target"]): e["exists"] and e["registered"] for e in json.load(open(sys.argv[1], encoding="utf-8"))}
want = [(".claude/skills/kaizen-orchestrator/SKILL.md", "docs/process/kaizen-flow.html"),
        ("design-kit/skills/design-mockup/SKILL.md", "docs/design-kit/design-mockup.html"),
        ("infra-kit/skills/infra-test/SKILL.md", "docs/infra-kit/infra-test.html"),
        ("docs/superpowers/specs/2026-09-02-api-kit-design.md", "docs/api-kit/multi-sample-pagination-variance.html"),
        ("docs/superpowers/specs/2026-09-02-api-kit-design.md", "docs/api-kit/contract-extraction-modes.html")]
hit = sum(1 for w in want if got.get(w))
neg = sum(1 for s, _ in got if s == sys.argv[2])
print(f"pairs={hit}/{len(want)} neg_source_entries={neg} entries={len(got)}")
PY
# 맞대기 검사 — CI 파일의 run 줄에서 detect-docs-drift.py 를 부르는 명령을 그대로 꺼내 돌린다
CMD=$(grep -E '^\s+run: .*scripts/detect-docs-drift\.py' "$T/.github/workflows/ci.yml" | sed -E 's/^\s+run: //')
echo "ci_lines=$(printf '%s' "$CMD" | grep -c .)"
if [ -n "$CMD" ] && [ "$(printf '%s\n' "$CMD" | wc -l | tr -d ' ')" = 1 ]; then
  chk() { (cd "$T" && bash -c "$CMD" >"$T/chk.txt" 2>&1); echo $?; }
  git -C "$T" checkout -q -- . 
  echo "table-real rc=$(chk)"
  cp "$T/.claude/skills/docs-site/SKILL.md" "$T/ds.bak"
  sed -i '' 's#, `infra-kit/skills/infra-test/SKILL.md`##; s#`infra-kit/skills/infra-test/SKILL.md`, ##' "$T/.claude/skills/docs-site/SKILL.md"
  rc=$(chk); echo "table-drop rc=$rc named=$(grep -c 'infra-kit/skills/infra-test/SKILL.md' "$T/chk.txt") changed=$(cmp -s "$T/ds.bak" "$T/.claude/skills/docs-site/SKILL.md"; echo $?)"
  cp "$T/ds.bak" "$T/.claude/skills/docs-site/SKILL.md"
  python3 - "$T/scripts/detect-docs-drift.py" "$T/applied.txt" <<'PY'
import sys; p = sys.argv[1]; s = open(p, encoding="utf-8").read()
k = 'SOURCE_TO_HTML: list[tuple[str, str]] = ['
open(sys.argv[2], "w").write(str(s.count(k)))
s = s.replace(k, k + '\n    ("측정용-원본/", "docs/측정용/"),', 1)
open(p, "w", encoding="utf-8").write(s)
PY
  rc=$(chk); echo "script-add rc=$rc named=$(grep -c '측정용-원본/' "$T/chk.txt") applied=$(cat "$T/applied.txt")"
fi
rm -rf "$T"
```

```bash
#!/usr/bin/env bash
# apidocs.sh — SC-10: api-kit 문서 검사가 같은 사이트 스타일 파일은 외부로 세지 않고, 바깥 주소는 여전히 잡는가
K=${K:?}; . "$K/common.sh"; R=$(resolve_ref); T=$(unpack "$R"); cp -R "$T" "$T.orig"
reset() { rm -rf "$T"; cp -R "$T.orig" "$T"; }
ck() { (cd "$T" && python3 scripts/check-api-kit-docs.py >"$T/out.txt" 2>&1); echo $?; }
rc=$(ck); echo "real rc=$rc pass=[$(tail -1 "$T/out.txt")] external=$(grep -c '외부 리소스' "$T/out.txt")"
P=docs/api-kit/snapshot-sealing-canonicalization.html
for c in css js import font; do
  reset
  case $c in
    css)    tag='<link rel="stylesheet" href="https://cdn.example.com/x.css">' ;;
    js)     tag='<script src="https://cdn.example.com/x.js"></script>' ;;
    import) tag='<style>@import url("https://cdn.example.com/y.css");</style>' ;;
    font)   tag='<link rel="stylesheet" href="//fonts.example.com/css">' ;;
  esac
  python3 - "$T/$P" "$tag" <<'PY'
import sys; p, tag = sys.argv[1], sys.argv[2]; s = open(p, encoding="utf-8").read()
s = s.replace("</head>", tag + "\n</head>", 1); open(p, "w", encoding="utf-8").write(s)
PY
  rc=$(ck); echo "ext-$c rc=$rc named=$(awk -v p="$P" '/^(OK  |FAIL) /{ on = index($(0), p) > 0 } on' "$T/out.txt" | grep -c '외부 리소스')"
done
rm -rf "$T" "$T.orig"
```

```bash
#!/usr/bin/env bash
# evals.sh — SC-11: run-evals · sync-evals 가 api-kit 을 읽고, api-kit 사례를 실제로 재는가
K=${K:?}; . "$K/common.sh"; R=$(resolve_ref); T=$(unpack "$R"); cp -R "$T" "$T.orig"
reset() { rm -rf "$T"; cp -R "$T.orig" "$T"; }
re_() { (cd "$T" && python3 scripts/run-evals.py "$@" >"$T/re.txt" 2>&1); echo $?; }
se_() { (cd "$T" && python3 scripts/sync-evals.py --check-only >"$T/se.txt" 2>&1); echo $?; }
rc=$(re_); echo "run-all rc=$rc api_block=$(grep -c '^→ api-kit' "$T/re.txt") total=[$(grep '^Total' "$T/re.txt")]"
rc=$(re_ api-kit); echo "run-api rc=$rc line=[$(grep -E '^  (PASS|FAIL|WARN)' "$T/re.txt" | head -1)]"
rc=$(se_); echo "sync rc=$rc api_block=$(grep -c '^→ api-kit' "$T/se.txt") missing=$(grep -c 'MISSING' "$T/se.txt") total=[$(grep '^Total' "$T/se.txt")]"
# 스킬 다섯이 모두 사례를 가지는가 — evals.json 을 직접 센다
python3 - "$T/api-kit/evals/evals.json" "$T/api-kit/skills" <<'PY'
import json, pathlib, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
cases = d.get("cases") or d.get("evals") or d.get("tests") or []
skills = sorted(p.parent.name for p in pathlib.Path(sys.argv[2]).glob("*/SKILL.md"))
have = {c.get("skill") for c in cases}
print(f"skills={len(skills)} covered={sum(s in have for s in skills)} placeholder={json.dumps(d, ensure_ascii=False).count('(placeholder)') + json.dumps(d, ensure_ascii=False).count('(TODO')}")
PY
# 음성 대조 — api-kit 사례 하나의 prompt 를 비우면 run-evals 가 FAIL 을 낸다
python3 - "$T/api-kit/evals/evals.json" <<'PY'
import json, sys; p = sys.argv[1]; d = json.load(open(p, encoding="utf-8"))
key = "cases" if "cases" in d else ("evals" if "evals" in d else "tests")
d[key][0]["prompt"] = ""; json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
PY
rc=$(re_ api-kit); echo "neg-prompt rc=$rc fail=$(grep -c 'prompt 비어' "$T/re.txt")"
reset
# 음성 대조 — 스킬 폴더를 하나 더 만들면 sync-evals 가 빠진 사례로 잡는다
mkdir -p "$T/api-kit/skills/api-probe-extra"; printf -- '---\nname: api-probe-extra\ndescription: 측정용.\n---\n' >"$T/api-kit/skills/api-probe-extra/SKILL.md"
rc=$(se_); echo "neg-sync rc=$rc missing=$(grep -c 'MISSING: api-probe-extra' "$T/se.txt")"
echo "ci_stale_comment=$(grep -c 'run-evals.py 킷 목록 밖' "$T/.github/workflows/ci.yml")"
rm -rf "$T" "$T.orig"
```

```bash
#!/usr/bin/env bash
# group.sh — SC-12 · SK-02: 수집기 묶음 이름과 reflect-kit 이 고르는 프로젝트 이름이 경로 종류 여섯에서 같은가
K=${K:?}; . "$K/common.sh"; R=$(resolve_ref); T=$(unpack "$R")
X=$(mktemp -d "${TMPDIR:-/tmp}/vsa-grp.XXXXXX"); X=$(cd "$X" && pwd -P)
# 수집기는 /tmp · /private/tmp · /var/folders 로 시작하는 경로를 시험 세션으로 따로 묶는다 — 그 아래서 재면 여섯 모두 다르게 나와 아무것도 못 잰다.
# 맥 기본 TMPDIR(/var/folders/…)은 pwd -P 로 /private/var/folders 가 되어 이 전제를 지킨다
case $X in /tmp*|/private/tmp*|/var/folders*) echo "PREMISE_FAIL 임시 경로 접두 $X — 기본 TMPDIR 로 돌려라"; rm -rf "$X"; exit 2 ;; esac
g() { git -c user.name=m -c user.email=m@m -c init.defaultBranch=main "$@" >/dev/null 2>&1; }
g init "$X/repo" && touch "$X/repo/a" && g -C "$X/repo" add a && g -C "$X/repo" commit -m a
mkdir -p "$X/repo/sub" "$X/repo/.claude/worktrees" "$X/plain"
g -C "$X/repo" worktree add "$X/repo/.claude/worktrees/live" -b live
g -C "$X/repo" worktree add "$X/repo/.claude/worktrees/gone" -b gone && rm -rf "$X/repo/.claude/worktrees/gone"
g clone --bare "$X/repo" "$X/bare.git" && g -C "$X/bare.git" worktree add "$X/bare-wt" main
PATHS="$X/repo $X/repo/sub $X/repo/.claude/worktrees/live $X/repo/.claude/worktrees/gone $X/bare-wt $X/plain"
same=0; diff=""; names=""
for p in $PATHS; do
  col=$(cd "$T/scripts" && python3 -c 'import importlib.util,sys; s=importlib.util.spec_from_file_location("c","collect-kaizen-data.py"); m=importlib.util.module_from_spec(s); sys.modules["c"]=m; s.loader.exec_module(m); print(m.project_group(sys.argv[1]))' "$p" 2>/dev/null)
  ref=$(bash -c '. "$1/reflect-kit/hooks/_lib-project-id.sh" 2>/dev/null; basename "$(project_root "$2")"' _ "$T" "$p")
  names="$names ${ref:-?}"
  if [ -n "$col" ] && [ "$col" = "$ref" ]; then same=$((same + 1)); else diff="$diff ${p#$X/}(col=$col ref=$ref)"; fi
done
echo "kinds_same=$same/6 names=[${names# }] diff=[${diff# }]"
echo "lib_stale=$(grep -c 'all 에서만 보인다' "$T/reflect-kit/hooks/_lib-project-id.sh") digest_line=$(grep -F 'project_root "$cwd"' "$T/reflect-kit/skills/reflect-digest/SKILL.md" | grep -cE '지운|지워진')"
rm -rf "$T" "$X"
```

```bash
#!/usr/bin/env bash
# stale.sh — SC-13: 옛 값 검사가 onboarding-kit 예제 원본을 읽고, 거기 넣은 옛 값을 잡는가
K=${K:?}; . "$K/common.sh"; R=$(resolve_ref); T=$(unpack "$R")
st() { (cd "$T" && python3 scripts/check-stale-values.py >"$T/out.txt" 2>&1); echo $?; }
rc=$(st); echo "real rc=$rc scope=[$(grep '^검사 범위' "$T/out.txt")] missing_dir=$(grep -c '없는 소스 디렉토리' "$T/out.txt")"
OLD=$(python3 -c 'import yaml,sys; print(yaml.safe_load(open(sys.argv[1]))["values"][1]["old"])' "$T/.harness/stale-values.yaml")
# 문서 사이트 매핑 표에 있는데 이 검사가 안 읽던 원본 셋 — 파일마다 따로 심어 본다
# 넷째는 하위 폴더 안 파일 — 폴더 아래를 다 읽는지(재귀) 직접 잰다
for F in docs/onboarding-kit/examples/fcm-ios-setup-guide.md $(cd "$T" && find docs/flutter docs/howto -maxdepth 1 -name '*.md' | sort | awk -F/ '!seen[$(2)]++') $(cd "$T" && find docs/flutter -mindepth 2 -name '*.md' | sort | head -1); do
  cp "$T/$F" "$T/bak.md"; printf '\n%s\n' "$OLD" >>"$T/$F"
  rc=$(st); echo "planted rc=$rc named=$(grep -c "$F" "$T/out.txt") file=$F"
  cp "$T/bak.md" "$T/$F"
done
rm -rf "$T"
```

```bash
#!/usr/bin/env bash
# guide.sh — SC-14: 검증 가이드의 V2 · V3 · V6 · V8 · V10 절과 머리 판 번호 · 변경 이력
K=${K:?}; . "$K/common.sh"; R=$(resolve_ref); T=$(unpack "$R"); G="$T/harness/docs/guides/plugin-validation-guide.md"
sec() { awk -v a="^### $1 " -v b="^### $2 " '$(0) ~ a { on = 1; next } $(0) ~ b { on = 0 } on' "$G"; }
v2=$(sec V2 V3); v3=$(sec V3 V4); v6=$(sec V6 V7); v8=$(sec V8 V9); v10=$(awk '/^### V10 /{on=1; next} /^## /{on=0} on' "$G")
echo "v2 skip_word=$(printf '%s\n' "$v2" | grep -cF 'SKIP (no templates/)') ok_form=$(printf '%s\n' "$v2" | grep -cF 'no templates/ — OK')"
echo "v3 commonmark=$(printf '%s\n' "$v3" | grep -c 'CommonMark') v6 commonmark=$(printf '%s\n' "$v6" | grep -c 'CommonMark') v6_old_toggle=$(printf '%s\n' "$v6" | grep -cF 'if line.startswith("```") and not in_block') v6_refs=$(printf '%s\n' "$v6" | grep -cF 'skills/*/references/')"
echo "v8 bare_var=$(printf '%s\n' "$v8" | grep -cE '\$CLAUDE_PLUGIN_ROOT([^_A-Za-z0-9}]|$)')"
n=0; for d in docs/backend docs/infra docs/rust docs/react docs/flutter docs/planning docs/tone docs/api docs/howto; do printf '%s\n' "$v10" | grep -qF "$d" && n=$((n + 1)); done
echo "v10 research_dirs=$n/9 stale_v6_sentence=$(printf '%s\n' "$v10" | grep -cF 'V6 는 같은') "
ver=$(awk -F': *' '/^version:/{print $(2); exit}' "$G")
echo "version=$ver history_row=$(grep -cE "^\| [0-9-]+ \| $ver \|" "$G") history_names=$(grep -E "^\| [0-9-]+ \| $ver \|" "$G" | grep -oE 'V(2|3|6|8|10)\b' | sort -u | tr '\n' ' ')"
rm -rf "$T"
```

```bash
#!/usr/bin/env bash
# scope.sh — AR-01 · AR-02: 바뀐 파일 집합 · 커밋마다 킷 하나 · .harness 경로
K=${K:?}; . "$K/common.sh"; R=$(resolve_ref)
[ "$(git -C "$W" rev-list --merges "$B..$R" | grep -c .)" = 0 ] || { echo END_HAS_MERGE; exit 2; }
KITS="api-kit backend-kit bambu-kit design-kit flutter-toolkit harness howto-kit infra-kit onboarding-kit planning-kit react-kit reflect-kit rust-kit tone-kit"
ALLOWED="scripts/run-kaizen-assertions.py scripts/validate-plugin.py scripts/plugin_utils.py scripts/sync-docs.py scripts/spawn-kaizen-phase.sh scripts/detect-docs-drift.py scripts/check-api-kit-docs.py scripts/run-evals.py scripts/sync-evals.py scripts/collect-kaizen-data.py scripts/test-collect-kaizen-data.py scripts/sync-orchestrator.py scripts/check-stale-values.py .github/workflows/ci.yml .claude/skills/docs-site/SKILL.md harness/docs/guides/plugin-validation-guide.md api-kit/evals/evals.json reflect-kit/hooks/_lib-project-id.sh reflect-kit/skills/reflect-digest/SKILL.md reflect-kit/evals/hooks/project-id-test.sh README.md"
for k in $KITS; do ALLOWED="$ALLOWED $k/README.md"; done
REQUIRED="scripts/sync-orchestrator.py scripts/plugin_utils.py reflect-kit/hooks/_lib-project-id.sh reflect-kit/skills/reflect-digest/SKILL.md scripts/run-kaizen-assertions.py scripts/validate-plugin.py scripts/sync-docs.py scripts/spawn-kaizen-phase.sh scripts/detect-docs-drift.py scripts/check-api-kit-docs.py scripts/run-evals.py scripts/sync-evals.py scripts/collect-kaizen-data.py scripts/check-stale-values.py .github/workflows/ci.yml .claude/skills/docs-site/SKILL.md harness/docs/guides/plugin-validation-guide.md api-kit/evals/evals.json"
CH=$(git -C "$W" diff --name-only "$B..$R" -- . ':(exclude).harness')
out=0; for f in $CH; do printf '%s\n' $ALLOWED | grep -qxF "$f" || { out=$((out + 1)); echo "  밖: $f"; }; done
miss=0; for f in $REQUIRED; do printf '%s\n' $CH | grep -qxF "$f" || { miss=$((miss + 1)); echo "  빠짐: $f"; }; done
echo "AR01 changed=$(printf '%s\n' $CH | grep -c .) outside=$out required_missing=$miss"
# 커밋마다 — 킷 폴더를 건드린 커밋은 그 킷 폴더만 담는다
mixed=0; n=0
for c in $(git -C "$W" rev-list "$B..$R"); do
  n=$((n + 1))
  fs=$(git -C "$W" show --name-only --format= "$c" | grep .)
  ks=$(printf '%s\n' "$fs" | cut -d/ -f1 | sort -u | while read -r top; do printf '%s\n' $KITS | grep -qxF "$top" && echo "$top"; done | grep -c .)
  if [ "$ks" -gt 1 ] || { [ "$ks" = 1 ] && [ "$(printf '%s\n' "$fs" | cut -d/ -f1 | sort -u | grep -c .)" -gt 1 ]; }; then
    mixed=$((mixed + 1)); echo "  섞임: $(git -C "$W" log -1 --format='%h %s' "$c")"
  fi
done
echo "AR02 commits=$n mixed=$mixed"
# .harness 아래 — 이 계약 슬러그 파일 셋과 notes 파일 하나만
HX=$(git -C "$W" diff --name-only "$B..$R" -- .harness | grep -vE '^\.harness/(sprint-(contract|feedback|amendments)-after-0926-check-scripts\.md|\.meta/after-kaizen-0926b/vsa-notes\.md)$')
echo "AR01h harness_other=$(printf '%s' "$HX" | grep -c .)"; [ -n "$HX" ] && printf '  %s\n' $HX
exit 0
```

```bash
#!/usr/bin/env bash
# misc.sh — SK-01 · AR-03 · AP-01 · AP-02 · AP-04 · RE-01 · RE-02 · DG-01 · DG-03 의 글자 · 집합 측정
K=${K:?}; . "$K/common.sh"; R=$(resolve_ref); T=$(unpack "$R")
DS="$T/.claude/skills/docs-site/SKILL.md"
st1=$(awk '/^## Step 1:/{on=1; next} /^## /{on=0} on' "$DS")
n=0; for s in .claude/skills/kaizen-orchestrator/SKILL.md design-kit/skills/design-mockup/SKILL.md infra-kit/skills/infra-test/SKILL.md docs/superpowers/specs/2026-09-02-api-kit-design.md; do printf '%s\n' "$st1" | grep -E '^\|' | grep -qF "\`$s\`" && n=$((n + 1)); done
echo "SK01 table_sources=$n/4"
NOTES="$T/.harness/.meta/after-kaizen-0926b/vsa-notes.md"
if [ -f "$NOTES" ]; then
  ids=0; for i in 1 2 4 5 6 9 10 12 13 14 15 21 27; do grep -qE "VS-$i([^0-9]|$)" "$NOTES" && ids=$((ids + 1)); done
  hs=0; for h in '## 남은 것' '## tone-guide 결과' '## 문서 드리프트' '## 킷별 판 올림 판단'; do grep -qxF "$h" "$NOTES" && hs=$((hs + 1)); done
  echo "AR03 notes=1 ids=$ids/13 heads=$hs/4"
else echo "AR03 notes=0"; fi
ADDED=$(git -C "$W" diff -U0 "$B" "$R" -- . ':(exclude).harness' | grep -E '^\+[^+]')
echo "AP01 hardcoded_version=$(printf '%s\n' "$ADDED" | grep -ciE 'hardcoded.*version')"
echo "AP02 remote_branch=$(git -C "$W" ls-remote --heads origin "$BR" | grep -c .)"
fm=0; SK=$(git -C "$W" diff --name-only "$B..$R" -- '*SKILL.md' '*/agents/*.md'); for f in $SK; do awk 'NR==1&&/^---/{on=1;next} on&&/^---/{exit} on&&/^name:/{f=1} END{exit !f}' "$T/$f" && fm=$((fm + 1)); done
echo "AP04 frontmatter_name=$fm/$(printf '%s\n' $SK | grep -c .)"
echo "RE01 old_toggle=$(grep -cF 'startswith("```")' "$T/scripts/validate-plugin.py")"
echo "RE02 map_in_validate=$(grep -c '"docs/backend' "$T/scripts/validate-plugin.py") map_in_orchestrator=$(grep -c '"docs/backend' "$T/scripts/sync-orchestrator.py") map_in_utils=$(grep -c '"docs/backend' "$T/scripts/plugin_utils.py")"
echo "DG01_03 release_sh_changed=$(git -C "$W" diff --name-only "$B..$R" | grep -c '^scripts/release.sh$')"
rm -rf "$T"
```

```bash
#!/usr/bin/env bash
# dg.sh — DG-02: 바뀐 파일의 편집기 진단 몫 — 마크다운 더한 줄의 새 경고 · 파이썬 컴파일 · 셸 문법 · JSON · 워크플로 검사
K=${K:?}; . "$K/common.sh"; R=$(resolve_ref); T=$(unpack "$R")
CH=$(git -C "$W" diff --name-only --diff-filter=AM "$B..$R" -- . ':(exclude).harness')
MDS=$(printf '%s\n' $CH | grep -E '\.md$'); PYS=$(printf '%s\n' $CH | grep -E '\.py$'); SHS=$(printf '%s\n' $CH | grep -E '\.sh$'); JS=$(printf '%s\n' $CH | grep -E '\.json$')
new=0
for f in $MDS; do
  added=$(git -C "$W" diff -U0 "$B" "$R" -- "$f" | sed -nE 's/^@@ -[0-9,]+ \+([0-9]+)(,([0-9]+))? @@.*/\1 \3/p' | while read -r s c; do c=${c:-1}; [ "$c" = 0 ] && continue; seq "$s" $((s + c - 1)); done)
  hits=$(cd "$T" && node "$MDL/node_modules/markdownlint-cli2/markdownlint-cli2-bin.mjs" --config "$MDL/cfg.markdownlint-cli2.jsonc" "$f" 2>&1 | sed -nE "s#^$f:([0-9]+).*#\1#p")
  k=$(printf '%s\n' $hits | grep -cxF -f <(printf '%s\n' $added) || true)
  [ "${k:-0}" -gt 0 ] && echo "  새 경고 $f: $k"
  new=$((new + ${k:-0}))
done
pyok=0; for f in $PYS; do python3 -m py_compile "$T/$f" 2>/dev/null && pyok=$((pyok + 1)); done
shok=0; for f in $SHS; do bash -n "$T/$f" 2>/dev/null && shok=$((shok + 1)); done
jsok=0; for f in $JS; do python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$T/$f" 2>/dev/null && jsok=$((jsok + 1)); done
al=$(cd "$T" && actionlint .github/workflows/ci.yml >/dev/null 2>&1; echo $?)
echo "md_files=$(printf '%s\n' $MDS | grep -c .) md_new_warn=$new py=$pyok/$(printf '%s\n' $PYS | grep -c .) sh=$shok/$(printf '%s\n' $SHS | grep -c .) json=$jsok/$(printf '%s\n' $JS | grep -c .) actionlint_rc=$al"
# AP-03 — 바뀐 마크다운 전부(.harness 포함)에서 백틱으로 여는 줄의 언어 힌트 없는 블록 수. 여닫는 규칙은 CommonMark 0.31.2 §4.5
ALLMD=$(git -C "$W" diff --name-only --diff-filter=AM "$B..$R" -- '*.md')
bare=$(cd "$T" && python3 - $ALLMD <<'PY2'
import re, sys
n = 0
for f in sys.argv[1:]:
    op = None
    for i, line in enumerate(open(f, encoding="utf-8").read().splitlines(), 1):
        m = re.match(r"^(`{3,}|~{3,})(.*)$", line.strip())
        if op is None:
            if m and not (m.group(1)[0] == "`" and "`" in m.group(2)):
                op = (m.group(1)[0], len(m.group(1)))
                if op[0] == "`" and not m.group(2).strip():
                    n += 1; print(f"  bare {f}:{i}", file=sys.stderr)
        elif m and m.group(1)[0] == op[0] and len(m.group(1)) >= op[1] and not m.group(2).strip():
            op = None
print(n)
PY2
)
echo "AP03 md_all=$(printf '%s\n' $ALLMD | grep -c .) bare_open=$bare"
rm -rf "$T"
```

```bash
#!/usr/bin/env bash
# ci.sh — DG-05: 로컬 CI 도구를 가지 끝 작업 폴더에서 돌린다. 전제가 안 맞으면 재지 않고 멈춘다
K=${K:?}; . "$K/common.sh"; R=$(resolve_ref)
CIL=/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh
[ "$(git -C "$W" rev-parse HEAD)" = "$R" ] || { echo "PREMISE_FAIL HEAD 가 가지 끝이 아니다"; exit 2; }
[ -z "$(git -C "$W" status --porcelain --untracked-files=no)" ] || { echo "PREMISE_FAIL 추적 파일에 커밋 안 된 변경"; exit 2; }
echo "ci_local_sha=$(shasum -a 256 "$CIL" | cut -c1-16)"
O=$(mktemp -d "${TMPDIR:-/tmp}/vsa-ci.XXXXXX")
TMPDIR=$O bash "$CIL" "$W" >"$O/run.txt" 2>&1
S="$O/ci-local/summary.txt"
echo "steps=$(grep -c 'rc=' "$S") rc0=$(grep -c 'rc=0' "$S") not0=[$(grep 'rc=' "$S" | grep -v 'rc=0' | tr -s ' ' | tr '\n' ';')] skip=[$(grep SKIP "$S" | tr '\n' ';')]"
echo "outside_ci_local=[$(sed -n '/이 스크립트 밖의 것:/,/^[0-9]*$/p' "$O/run.txt" | sed '1d;$d' | tr '\n' ';')]"
```

### 봉인 전 실측 — 시작 판 `6378948`

`REF=6378948` 으로 도우미 전부를 돌린 출력(2026-09-26 20:0x 첫 실측, 교차 진단 반영 뒤 다시 돌림 — `v10-coupled` · `stale` 넷째 줄이 새로 생겼고 나머지는 같다. `group.sh` 는 기본 TMPDIR 에서, 나머지는 TMPDIR 을 작업용 임시 폴더로 바꿔 돌렸다). 조건의 기대값과 다른 줄이 곧 고치기 전 판의 FAIL 이다.

```text
== asr
real rc=0 total=[Total: 14 passed, 0 failed] trace=0
empty-match rc=0 named=0 trace=0
empty-list rc=0 named=0 trace=0
nonstr-pattern rc=1 named=0 trace=1 others_measured=0
nonstr-file rc=1 named=0 trace=1 others_measured=0
== vp
real rc=0 vlines=140 not_ok=8
v2 rc=0 line=[ V2 templates 0 files — SKIP (no templates/)] skip=1
v3-tilde rc=2 hit=1
v3-nested rc=2 hit=1
v3-plain rc=2 hit=1
v6-tilde rc=2 fail=1 at_offset=3
v6-nested rc=2 fail=1 at_offset=5
v6-inline rc=2 fail=1 at_offset=6
v6-plain rc=2 fail=1 at_offset=2
v6-tildebare rc=0 fail=0 at_offset=-146
v6-refs rc=0 fail=0 at_offset=-146
v6-fix rc=0 fail=0 opener=[```] closer=[```text]
v8-unquoted rc=0 quote=0 exec=0 checked=
v8-quoted644 rc=0 quote=0 exec=0 checked=
v8-quoted755 rc=0 quote=0 exec=0 checked=
v8-otherVar rc=0 quote=0 exec=0 checked=
v8-interp644 rc=0 quote=0 exec=0 checked=
v10-research rc=0 hit=0
v10-unmapped rc=0 hit=0
v10-coupled rc=0 hit=0 gone=0 applied=0
== sdocs
real rc=0 need=0
marker-nospace rc=0 lines=22,30 named=0
marker-halfspace rc=0 lines=22,30 named=0
desc rows=112 not_first_sentence=33 ex=['api-kit/README.md api-contract', 'api-kit/README.md api-init', 'design-kit/README.md design-concept']
md060_in_auto=107 lint_rc=1 files=15
per_file README.md=15 api-kit/README.md=32 backend-kit/README.md=14 bambu-kit/README.md=12 design-kit/README.md=15 flutter-toolkit/README.md=10 harness/README.md=56 howto-kit/README.md=33 infra-kit/README.md=14 onboarding-kit/README.md=2 planning-kit/README.md=6 react-kit/README.md=8 reflect-kit/README.md=12 rust-kit/README.md=15 tone-kit/README.md=24
== spawn
table_rows=17
phases_ok=4/17 common_1_5=10/17 bad=[5(rc=0 got=[§2 §3] want=[§2]) 6(rc=0 got=[§2 §3] want=[]) 7(rc=0 got=[§2 §3] want=[]) 8(rc=0 got=[§2 §3] want=[]) 9(rc=0 got=[§2 §3] want=[§2]) 10(rc=0 got=[§2 §3] want=[§3]) 11(rc=1 got=[] want=[]) 12(rc=1 got=[] want=[]) 13(rc=1 got=[] want=[§2]) 14(rc=1 got=[] want=[]) 15(rc=1 got=[] want=[]) 16(rc=1 got=[] want=[]) 17(rc=1 got=[] want=[])]
phase18 rc=1 help_17=0
== drift
drift rc=0
pairs=0/5 neg_source_entries=0 entries=0
ci_lines=0
== apidocs
real rc=1 pass=[0/12 PASS] external=12
ext-css rc=1 named=1
ext-js rc=1 named=1
ext-import rc=1 named=1
ext-font rc=1 named=1
== evals
run-all rc=0 api_block=0 total=[Total: 116 passed, 0 failed]
run-api rc=0 line=[  WARN: evals.json에 eval 엔트리가 없음]
sync rc=0 api_block=0 missing=0 total=[Total: 0 added, 0 orphans, 0 missing (preview)]
skills=5 covered=1 placeholder=0
neg-prompt rc=0 fail=0
neg-sync rc=0 missing=0
ci_stale_comment=1
== group
kinds_same=4/6 names=[repo repo repo gone bare-wt plain] diff=[repo/.claude/worktrees/gone(col=repo ref=gone) bare-wt(col=vsa-grp.XXXXXX ref=bare-wt)]
lib_stale=1 digest_line=0
== stale
real rc=0 scope=[검사 범위: 소스 디렉토리 26/26 · 파일 403 개 · 등록값 18 개] missing_dir=0
planted rc=0 named=0 file=docs/onboarding-kit/examples/fcm-ios-setup-guide.md
planted rc=0 named=0 file=docs/flutter/research-log.md
planted rc=0 named=0 file=docs/howto/branch-catalog.md
planted rc=0 named=0 file=docs/flutter/architecture/api-layer.md
== guide
v2 skip_word=1 ok_form=0
v3 commonmark=0 v6 commonmark=0 v6_old_toggle=1 v6_refs=0
v8 bare_var=0
v10 research_dirs=0/9 stale_v6_sentence=1 
version=1.4.1 history_row=1 history_names=V10 
== scope
  빠짐: scripts/sync-orchestrator.py
  빠짐: scripts/plugin_utils.py
  빠짐: reflect-kit/hooks/_lib-project-id.sh
  빠짐: reflect-kit/skills/reflect-digest/SKILL.md
  빠짐: scripts/run-kaizen-assertions.py
  빠짐: scripts/validate-plugin.py
  빠짐: scripts/sync-docs.py
  빠짐: scripts/spawn-kaizen-phase.sh
  빠짐: scripts/detect-docs-drift.py
  빠짐: scripts/check-api-kit-docs.py
  빠짐: scripts/run-evals.py
  빠짐: scripts/sync-evals.py
  빠짐: scripts/collect-kaizen-data.py
  빠짐: scripts/check-stale-values.py
  빠짐: .github/workflows/ci.yml
  빠짐: .claude/skills/docs-site/SKILL.md
  빠짐: harness/docs/guides/plugin-validation-guide.md
  빠짐: api-kit/evals/evals.json
AR01 changed=0 outside=0 required_missing=18
AR02 commits=0 mixed=0
AR01h harness_other=0
== misc
SK01 table_sources=0/4
AR03 notes=0
AP01 hardcoded_version=0
AP02 remote_branch=0
AP04 frontmatter_name=0/0
RE01 old_toggle=2
RE02 map_in_validate=0 map_in_orchestrator=1 map_in_utils=0
DG01_03 release_sh_changed=0
== dg
md_files=0 md_new_warn=0 py=0/0 sh=0/0 json=0/0 actionlint_rc=0
AP03 md_all=0 bare_open=0
== ci-local (시작 판 작업 폴더에서 도구를 직접 돌림 — ci.sh 의 전제는 가지 끝이라 이 줄들로 갈음)
steps=25 rc0=25 skip=[feedback-agg-test SKIP (yq 없음)]
run: pip install pyyaml
run: command -v zsh >/dev/null || { sudo apt-get update && sudo apt-get install -y zsh; }
run: npm ci
run: npx playwright install --with-deps chromium
run: |
```

알려진 답 (새로 짠 측정이 0 이 아닌 수를 낼 때):

- `sdocs.sh` 설명 칸 — `planning-kit/README.md` 한 파일만 넣으면 `rows=13 not_first_sentence=4`. 손으로 센 답 4: `plan-ideate`(「…수렴(convergent)하여」) · `plan-risks`(「…적용하여」) · `plan-stories`(「…검증과」) · `planning-reviewer`(첫 줄이 두 문장). 실제값 4, 종료 코드 0
- `sdocs.sh` MD060 — `planning-kit/README.md` · `onboarding-kit/README.md` 둘만 넣으면 `md060_in_auto=8`. 손으로 센 답: planning 스킬 표 구분 줄 `|------|------|` 한 줄에 파이프 빈칸 경고 4 · planning 에이전트 표 행 1 줄에 맞춤 경고 2 · onboarding 스킬 표 행 1 줄에 맞춤 경고 2 = 8. 실제값 8
- `dg.sh` 새 경고 — 기준을 `f81568d` 로 바꿔 `6378948` 을 재면 `md_new_warn=19` (죽은 측정이 아님)
- `dg.sh` AP-03 — 여는 백틱 줄 하나에 언어 힌트가 없고 `~~~text` 안에 백틱 줄이 든 합성 파일에서 `1` (`~~~` 안 줄은 세지 않음)
- `scope.sh` — 기준 `7038841~1` · 끝 `7038841`(릴리스 커밋)로 재면 `outside=15` · `mixed=1`, 병합이 든 구간은 `END_HAS_MERGE`
- `misc.sh` AP-02 — 같은 명령을 `main` 에 쓰면 `1`

## Script

- [ ] SC-01: 카이젠 회귀 패턴 실행기(`scripts/run-kaizen-assertions.py`)가 빈 문자열에 맞는 패턴을 「못 읽은 입력」(종료 코드 2)으로, 값이 빈 목록인 키를 FAIL(종료 코드 1)로 알리고, 실제 저장소 패턴 열넷은 그대로 통과한다 [exact]
    Given: 가지 끝 판. 측정: `K=<폴더> bash "$K/asr.sh"` 의 첫 세 줄이 `real rc=0 total=[Total: 14 passed, 0 failed] trace=0` · `empty-match rc=2 named=1 trace=0` · `empty-list rc=1 named=1 trace=0`
    양성 대조: 시작 판(`REF=6378948`)에서 `empty-match rc=0 named=0` · `empty-list rc=0 named=0` — 두 빈틈이 통과로 샌다
    음성 대조: 실제 패턴 열넷은 빈 글에 맞지 않는다(실측) — `real` 줄이 `14 passed` 에서 줄면 새 판정이 정상 패턴까지 막은 것이다
    도우미 지문: `asr.sh` sha256 앞 16 자 `feda42718d0654da` · `common.sh` sha256 앞 16 자 `c9670538dba5f035`
- [ ] SC-02: validate-plugin V8 이 중괄호 없는 `$CLAUDE_PLUGIN_ROOT` 도 따옴표 검사와 실행 비트 검사에 넣는다 — 따옴표 밖이면 FAIL, 직접 실행하는 스크립트가 비실행이면 FAIL, 이름이 더 긴 다른 변수와 인터프리터 경유는 건드리지 않는다 [exact]
    Given: 가지 끝 판, design-kit `hooks.json` 명령 하나를 바꾼 사본. 측정: `vp.sh` 의 `v8-` 다섯 줄이 `v8-unquoted rc=2 quote=1 exec=0 checked=` · `v8-quoted644 rc=2 quote=0 exec=1 checked=` · `v8-quoted755 rc=0 quote=0 exec=0 checked=1` · `v8-otherVar rc=0 quote=0 exec=0 checked=` · `v8-interp644 rc=0 quote=0 exec=0 checked=`
    양성 대조: 시작 판에서 다섯 줄 모두 `rc=0 quote=0 exec=0 checked=` — 앞 셋을 놓친다
    도우미 지문: `vp.sh` sha256 앞 16 자 `94bc19dc459a9f8c`
- [ ] SC-03: validate-plugin V3 · V6 이 V10 과 같은 코드 블록 규칙(CommonMark 0.31.2 §4.5)으로 판정한다 — `~~~` 블록과 백틱 4 개 블록 안의 링크 · 백틱 줄은 보지 않고, 줄 안 코드로 시작하는 줄 뒤의 언어 힌트 없는 블록은 그 여는 줄을 짚고, `--fix` 도 그 여는 줄을 고친다. V6 는 스킬 폴더 안 `skills/*/references/**/*.md` 도 읽고, `~~~` 여는 줄은 검사하지 않는다 [exact]
    Given: 가지 끝 판, api-kit 파일 끝에 합성 블록을 붙인 사본. 측정: `vp.sh` 의 줄들이 `v3-tilde rc=0 hit=0` · `v3-nested rc=0 hit=0` · `v3-plain rc=2 hit=1` · `v6-tilde rc=0 fail=0` · `v6-nested rc=0 fail=0` · `v6-inline rc=2 fail=1 at_offset=4` · `v6-plain rc=2 fail=1` · `v6-tildebare rc=0 fail=0` · `v6-refs rc=2 fail=1` · `v6-fix rc=0 fail=0 opener=[```text] closer=[```]` (fail 이 0 인 줄의 `at_offset` 은 보지 않는다)
    양성 대조: 시작 판에서 `v3-tilde` · `v3-nested` · `v6-tilde` · `v6-nested` 가 `rc=2`(잘못 잡음), `v6-inline` 이 `at_offset=6`(닫는 줄을 짚음), `v6-refs rc=0`(범위 밖), `v6-fix` 가 `opener=[```] closer=[```text]`
    음성 대조: `v3-plain` · `v6-plain` 은 두 판 모두 FAIL — 블록 밖 결함은 계속 잡는다
    도우미 지문: `vp.sh` sha256 앞 16 자 `94bc19dc459a9f8c`
- [ ] SC-04: validate-plugin 전체가 14 킷 모두 OK 이고, V2 는 `templates/` 없는 킷에서 `no templates/ — OK` 로 끝나며 SKIP 글자가 없고, V10 은 킷의 저장소 원본 폴더(`docs/backend` · `docs/infra` · `docs/rust` · `docs/react` · `docs/flutter` · `docs/planning` · `docs/tone` · `docs/api` · `docs/howto`)의 끊긴 표를 그 킷 결과로 잡고 짝 없는 폴더(`docs/superpowers`)는 보지 않는다 [exact]
    Given: 가지 끝 판. 측정: `vp.sh` 의 `real rc=0 vlines=140 not_ok=0` · `v2 rc=0 line=[ V2 templates no templates/ — OK] skip=0` · `v10-research rc=2 hit=1` · `v10-unmapped rc=0 hit=0`
    양성 대조: 시작 판에서 `real … not_ok=8`(V2 SKIP 여덟 줄) · `v2 … — SKIP (no templates/)] skip=1` · `v10-research rc=0 hit=0`
    도우미 지문: `vp.sh` sha256 앞 16 자 `94bc19dc459a9f8c`
- [ ] SC-05: sync-docs 가 킷 README 의 스킬 · 에이전트 표 설명 칸에 frontmatter 설명 전체의 첫 문장(줄을 이어 붙이고 빈칸을 하나로 줄인 글에서 처음 나오는 「마침표 뒤 빈칸 또는 글 끝」까지)을 쓰고, 가지 끝의 README 는 그 결과와 같다 [exact]
    Given: 가지 끝 판. 측정: `sdocs.sh` 의 `real rc=0 need=0` · `desc rows=112 not_first_sentence=0 ex=[]`
    양성 대조: 시작 판에서 `desc rows=112 not_first_sentence=33` (알려진 답: planning-kit 하나로 4)
    도우미 지문: `sdocs.sh` sha256 앞 16 자 `3b73cccee753faf9`
- [ ] SC-06: sync-docs 가 그리는 표(킷 README 의 skills · agents · hooks · scripts · evals · references, 루트 README 의 plugins)의 AUTO 블록 안에 MD060 경고가 0 건이고, 파일 열다섯 각각의 markdownlint 경고 수가 시작 판보다 많지 않다 [exact, enumerated]
    Given: 가지 끝 판, 편집기와 같은 설정(markdownlint-cli2 0.23.2, MD013 끔). 측정: `sdocs.sh` 의 `md060_in_auto=0` 과 `per_file` 줄의 각 값이 시작 판 값 이하 — 시작 판: `README.md=15 api-kit/README.md=32 backend-kit/README.md=14 bambu-kit/README.md=12 design-kit/README.md=15 flutter-toolkit/README.md=10 harness/README.md=56 howto-kit/README.md=33 infra-kit/README.md=14 onboarding-kit/README.md=2 planning-kit/README.md=6 react-kit/README.md=8 reflect-kit/README.md=12 rust-kit/README.md=15 tone-kit/README.md=24`
    양성 대조: 시작 판에서 `md060_in_auto=107` (알려진 답: planning · onboarding 둘로 8)
    도우미 지문: `sdocs.sh` sha256 앞 16 자 `3b73cccee753faf9`
- [ ] SC-07: Phase 부트스트랩(`scripts/spawn-kaizen-phase.sh`)이 Phase 1~17 을 모두 받고, 각 Phase 의 참조 절에 §1 · §5 를 늘 넣으며(표가 아니라 부트스트랩의 기존 공통 선언을 따른다 — GAP 절 VS-12 의 §1 · §5) §2 · §3 은 수집기 §6 표의 그 Phase 행에 적힌 것과 같게 내고, 18 은 거절하며, 도움말이 1 ~ 17 을 적는다 [exact]
    Given: 가지 끝 판을 git 저장소로 만든 사본. 측정: `spawn.sh` 가 `table_rows=17` · `phases_ok=17/17 common_1_5=17/17 bad=[]` · `phase18 rc=1 help_17=1`
    양성 대조: 시작 판에서 `phases_ok=4/17 common_1_5=10/17` (5~10 에 §2 §3 을 한꺼번에, 11~17 은 rc=1) · `help_17=0`
    도우미 지문: `spawn.sh` sha256 앞 16 자 `f2d2db0ab15d0ea9`
- [ ] SC-08: 문서 드리프트 도구가 원본 넷의 변경을 페이지 다섯으로 낸다 — `.claude/skills/kaizen-orchestrator/SKILL.md` → `docs/process/kaizen-flow.html`, `design-kit/skills/design-mockup/SKILL.md` → `docs/design-kit/design-mockup.html`, `infra-kit/skills/infra-test/SKILL.md` → `docs/infra-kit/infra-test.html`, `docs/superpowers/specs/2026-09-02-api-kit-design.md` → `docs/api-kit/multi-sample-pagination-variance.html` · `docs/api-kit/contract-extraction-modes.html` (모두 있는 · 등록된 페이지로), 짝 없는 다른 설계 기록은 내지 않는다 [exact, enumerated]
    Given: 가지 끝 판을 git 저장소로 만든 사본에서 다섯 원본과 짝 없는 `docs/superpowers/specs/` 파일 하나에 한 줄씩 더해 커밋. 측정: `drift.sh` 의 `drift rc=0` · `pairs=5/5 neg_source_entries=0`
    양성 대조: 시작 판에서 `pairs=0/5`
    도우미 지문: `drift.sh` sha256 앞 16 자 `c6f46c258cf295c3`
- [ ] SC-09: 드리프트 도구의 매핑과 `.claude/skills/docs-site/SKILL.md` Step 1 표를 맞대는 검사가 CI 한 단계로 돌고, 둘이 같을 때 종료 코드 0, 표에서 원본 하나를 빼거나 스크립트에만 짝 하나를 더하면 0 이 아닌 종료 코드와 함께 그 경로를 이름으로 낸다 [exact]
    Given: 가지 끝 판을 git 저장소로 만든 사본. `.github/workflows/ci.yml` 에서 `scripts/detect-docs-drift.py` 를 부르는 `run:` 줄 하나를 그대로 꺼내 돌린다. 측정: `drift.sh` 의 `ci_lines=1` · `table-real rc=0` · `table-drop rc=<0 아님> named=<1 이상> changed=1` · `script-add rc=<0 아님> named=<1 이상> applied=1`
    양성 대조: 시작 판에서 `ci_lines=0` — 검사가 없다. `changed=1` · `applied=1` 은 표 · 스크립트 변이가 실제로 적용됐다는 확인이다
    도우미 지문: `drift.sh` sha256 앞 16 자 `c6f46c258cf295c3`
- [ ] SC-10: api-kit 문서 검사(`scripts/check-api-kit-docs.py`)가 같은 사이트 상대 경로 스타일 파일은 외부로 세지 않아 12 쪽 모두 통과하고, 바깥 주소(`https://` · `//`)를 부르는 `<link>` · `<script src>` · `@import` 는 여전히 FAIL 로 잡는다 [exact]
    Given: 가지 끝 판. 측정: `apidocs.sh` 가 `real rc=0 pass=[12/12 PASS] external=0` · `ext-css rc=1 named=1` · `ext-js rc=1 named=1` · `ext-import rc=1 named=1` · `ext-font rc=1 named=1`
    양성 대조: 시작 판에서 `real rc=1 pass=[0/12 PASS] external=12`
    음성 대조: `ext-` 넷은 바깥 주소를 넣은 사본이다 — 외부 판정을 통째로 끄면 네 줄이 `rc=0` 이 된다
    도우미 지문: `apidocs.sh` sha256 앞 16 자 `c3bfe67b640ccd0a`
- [ ] SC-11: run-evals · sync-evals 가 api-kit 을 읽는다 — api-kit 스킬 다섯이 모두 사례를 갖고(자리표시 글 0), run-evals 가 api-kit 사례 다섯을 실제로 재며, 사례의 prompt 를 비우면 FAIL, 스킬 폴더를 하나 더 만들면 sync-evals 가 빠진 사례로 잡고, CI 파일의 「run-evals.py 킷 목록 밖」 설명은 사라진다 [exact]
    Given: 가지 끝 판. 측정: `evals.sh` 가 `run-all rc=0 api_block=1 total=[Total: 121 passed, 0 failed]` · `run-api rc=0 line=[  PASS: 5 passed, 0 failed]` · `sync rc=0 api_block=1 missing=0 total=[Total: 0 added, 0 orphans, 0 missing (preview)]` · `skills=5 covered=5 placeholder=0` · `neg-prompt rc=1 fail=1` · `neg-sync rc=1 missing=1` · `ci_stale_comment=0`
    양성 대조: 시작 판에서 `api_block=0`(두 스크립트) · `run-api … WARN: evals.json에 eval 엔트리가 없음` · `covered=1` · `neg-prompt rc=0 fail=0` · `neg-sync rc=0 missing=0` · `ci_stale_comment=1`
    음성 대조: `neg-prompt` · `neg-sync` 두 줄 — api-kit 을 목록에만 넣고 `cases` 를 읽지 않으면 둘 다 `rc=0` 이다
    도우미 지문: `evals.sh` sha256 앞 16 자 `ddd6f38eaf878ae0`
- [ ] SC-12: 수집기의 프로젝트 묶음 이름과 reflect-kit 이 고르는 프로젝트 이름이 경로 종류 여섯(레포 뿌리 · 하위 폴더 · 살아 있는 워크트리 · 지운 워크트리 · bare 레포의 워크트리 · git 밖 폴더)에서 같고, 그 이름은 차례로 `repo repo repo repo bare-wt plain` 이며, reflect-kit 훅 라이브러리의 「all 에서만 보인다」 설명은 사라진다 [exact, enumerated]
    Given: 가지 끝 판, 임시 폴더에 만든 git 레포 · 워크트리. 측정: `group.sh` 가 `kinds_same=6/6 names=[repo repo repo repo bare-wt plain] diff=[]` · `lib_stale=0`. 두 쪽 기존 시험(`python3 scripts/test-collect-kaizen-data.py` · `bash reflect-kit/evals/hooks/project-id-test.sh` · `bash reflect-kit/evals/hooks/collect-status-test.sh`)은 DG-05 가 잰다
    양성 대조: 시작 판에서 `kinds_same=4/6 names=[repo repo repo gone bare-wt plain]` (지운 워크트리 · bare 워크트리가 다름) · `lib_stale=1`
    도우미 지문: `group.sh` sha256 앞 16 자 `510a5c0a8f1ac43f`
- [ ] SC-13: 옛 값 검사(`scripts/check-stale-values.py`)가 문서 사이트 원본 `docs/onboarding-kit/examples` · `docs/flutter` · `docs/howto` 를 읽어, 세 곳 각각과 하위 폴더 안 파일 하나에 심은 등록 옛 값을 파일 이름과 함께 잡고, 실제 저장소는 옛 값 0 건에 없는 폴더 경고 0 이다 [exact, enumerated]
    Given: 가지 끝 판. 측정: `stale.sh` 가 `real rc=0 … missing_dir=0` 과 `planted rc=1 named=<1 이상> file=docs/onboarding-kit/examples/fcm-ios-setup-guide.md` · `… file=docs/flutter/research-log.md` · `… file=docs/howto/branch-catalog.md` · `… file=docs/flutter/architecture/api-layer.md` 네 줄
    양성 대조: 시작 판에서 네 줄 모두 `planted rc=0 named=0`
    음성 대조: 넷째 줄은 하위 폴더 파일이다 — 폴더 아래를 다 읽지 않고 맨 위 파일만 읽게 바꾸면 그 줄만 `rc=0 named=0` 이 된다
    도우미 지문: `stale.sh` sha256 앞 16 자 `c0e5f42e45b52481`
- [ ] SC-14: 검증 가이드(`harness/docs/guides/plugin-validation-guide.md`)가 바뀐 동작을 적는다 — V2 절에 `SKIP (no templates/)` 0 · `no templates/ — OK` 1 이상, V3 · V6 절에 `CommonMark` 1 이상, V6 절의 옛 토글 의사 코드 0 · `skills/*/references/` 1 이상, V8 절에 중괄호 없는 `$CLAUDE_PLUGIN_ROOT` 1 이상, V10 절에 원본 폴더 아홉 모두와 「V6 는 같은」 문장 0, 머리 판 번호가 1.4.1 보다 높고 그 판의 변경 이력 행 하나가 V2 · V3 · V6 · V8 · V10 을 모두 적는다 [exact, enumerated]
    Given: 가지 끝 판. 측정: `guide.sh` 가 `v2 skip_word=0 ok_form=<1 이상>` · `v3 commonmark=<1 이상> v6 commonmark=<1 이상> v6_old_toggle=0 v6_refs=<1 이상>` · `v8 bare_var=<1 이상>` · `v10 research_dirs=9/9 stale_v6_sentence=0` · `version=<1.4.1 보다 높은 판> history_row=1 history_names=V10 V2 V3 V6 V8`
    양성 대조: 시작 판에서 `skip_word=1 ok_form=0` · `commonmark=0` 둘 · `v6_old_toggle=1` · `bare_var=0` · `research_dirs=0/9 stale_v6_sentence=1` · `version=1.4.1 … history_names=V10`
    도우미 지문: `guide.sh` sha256 앞 16 자 `3142d6d4007a531b`

## Skill

- [ ] SK-01: `.claude/skills/docs-site/SKILL.md` Step 1 매핑 표의 행이 새 원본 넷(`.claude/skills/kaizen-orchestrator/SKILL.md` · `design-kit/skills/design-mockup/SKILL.md` · `infra-kit/skills/infra-test/SKILL.md` · `docs/superpowers/specs/2026-09-02-api-kit-design.md`)을 백틱으로 적는다 [exact, enumerated]
    Given: 가지 끝 판. 측정: `misc.sh` 의 `SK01 table_sources=4/4` (표 일치 자체는 SC-09 `table-real rc=0`)
    양성 대조: 시작 판에서 `SK01 table_sources=0/4`
    도우미 지문: `misc.sh` sha256 앞 16 자 `ee71e88cbcac65d0`
- [ ] SK-02: `reflect-kit/skills/reflect-digest/SKILL.md` 의 `project_root "$cwd"` 설명 줄이 지운 워크트리 경로를 본 레포로 잇는다는 것을 적는다 (「지운」 또는 「지워진」 이 그 줄에 든다) [exact]
    Given: 가지 끝 판. 측정: `group.sh` 의 `digest_line=1`
    양성 대조: 시작 판에서 `digest_line=0` (지금 글은 「git 밖이면 cwd」)
    도우미 지문: `group.sh` sha256 앞 16 자 `510a5c0a8f1ac43f`

## Error

- [ ] ER-01: 카이젠 회귀 패턴 실행기에서 `pattern` 이나 `file` 이 글자가 아니면 그 항목만 「못 읽은 입력」으로 이름을 대고 나머지를 끝까지 잰 뒤 종료 코드 2 로 끝나며, 파이썬 Traceback 이 나오지 않는다 [exact]
    Given: 가지 끝 판, contract-kaizen `low-coverage` 첫 항목의 한 칸을 숫자 7 로 바꾼 사본. 측정: `asr.sh` 의 `nonstr-pattern rc=2 named=1 trace=0 others_measured=8` · `nonstr-file rc=2 named=1 trace=0 others_measured=8` (`others_measured` = evaluator-kaizen 의 PASS 줄 수)
    양성 대조: 시작 판에서 두 줄 모두 `rc=1 named=0 trace=1 others_measured=0`
    도우미 지문: `asr.sh` sha256 앞 16 자 `feda42718d0654da`
- [ ] ER-02: sync-docs 가 빈칸 없는 AUTO 표지(`<!--AUTO:skills-->` · `<!--/AUTO:skills-->`)와 한쪽만 빈칸인 표지를 조용히 넘기지 않고, 그 파일 이름과 두 표지의 줄 번호를 대며 종료 코드 2 로 끝난다 [exact]
    Given: 가지 끝 판, api-kit README 의 skills 표지 한 쌍을 바꾼 사본. 측정: `sdocs.sh` 의 `marker-nospace rc=2 lines=<여는 줄>,<닫는 줄> named=1` · `marker-halfspace rc=2 … named=1`
    양성 대조: 시작 판에서 두 줄 모두 `rc=0 … named=0`
    도우미 지문: `sdocs.sh` sha256 앞 16 자 `3b73cccee753faf9`

## Architecture

- [ ] AR-01: Given: 가지 끝이 해석되고(`git rev-parse --verify refs/heads/chore/ak2-vsa`) 시작 판 `6378948` 부터 병합 커밋이 없다. 시작 판..가지 끝 누적 차이(`git diff --name-only 6378948..<가지 끝> -- . ':(exclude).harness'`)가 허용 목록 안에만 있고 필수 목록을 모두 담으며, `.harness/` 아래는 이 슬러그의 계약 · 피드백 · 개정 파일과 `.harness/.meta/after-kaizen-0926b/vsa-notes.md` 만 바뀐다 (허용 · 필수 목록은 `scope.sh` 의 `ALLOWED` · `REQUIRED` 가 글자 그대로 담는다, 포함 판정) [exact, enumerated]
    측정: `scope.sh` 의 `AR01 changed=<수> outside=0 required_missing=0` · `AR01h harness_other=0`
    양성 대조: 기준 `7038841~1` · 끝 `7038841` 로 재면 `outside=15`
    도우미 지문: `scope.sh` sha256 앞 16 자 `5017e850d980c932`
- [ ] AR-02: 시작 판..가지 끝의 커밋 가운데 킷 폴더(14 킷)를 건드린 커밋은 그 킷 폴더 하나만 담는다 — README 재생성 · api-kit 사례 · reflect-kit 훅은 킷마다 따로 커밋된다 [exact]
    측정: `scope.sh` 의 `AR02 commits=<1 이상> mixed=0`
    양성 대조: 릴리스 커밋 `7038841` 하나를 재면 `mixed=1`
    도우미 지문: `scope.sh` sha256 앞 16 자 `5017e850d980c932`
- [ ] AR-03: notes 파일 `.harness/.meta/after-kaizen-0926b/vsa-notes.md` 가 가지 끝에 있고, 항목 열셋(VS-1 · VS-2 · VS-4 · VS-5 · VS-6 · VS-9 · VS-10 · VS-12 · VS-13 · VS-14 · VS-15 · VS-21 · VS-27)을 모두 적으며, 줄 전체가 `## 남은 것` · `## tone-guide 결과` · `## 문서 드리프트` · `## 킷별 판 올림 판단` 인 제목 넷을 갖는다 [exact, enumerated]
    측정: `misc.sh` 의 `AR03 notes=1 ids=13/13 heads=4/4`
    양성 대조: 시작 판에서 `AR03 notes=0`
    도우미 지문: `misc.sh` sha256 앞 16 자 `ee71e88cbcac65d0`

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — 시작 판..가지 끝의 더한 줄(`.harness` 제외)에 `hardcoded.*version` (대소문자 무시) 0 건 [exact]
    측정: `misc.sh` 의 `AP01 hardcoded_version=0`
    도우미 지문: `misc.sh` sha256 앞 16 자 `ee71e88cbcac65d0`
- [ ] AP-02: force push 금지 — 이 가지는 원격에 아예 올리지 않는다 [exact]
    측정: `misc.sh` 의 `AP02 remote_branch=0` (`git ls-remote --heads origin chore/ak2-vsa` 줄 수). 양성 대조: 같은 명령을 `main` 에 쓰면 `1`
    도우미 지문: `misc.sh` sha256 앞 16 자 `ee71e88cbcac65d0`
- [ ] AP-03: bare code fence 금지 — 킷 전체 `python3 scripts/validate-plugin.py --check=code-fence` 가 종료 코드 0 이고(SC-04 `real` 이 포함), 시작 판..가지 끝에 바뀐 마크다운 전부(`.harness` 포함)에서 백틱으로 여는 줄의 언어 힌트 없는 블록이 0 개다 [exact]
    측정: `dg.sh` 의 `AP03 md_all=<수> bare_open=0`. 양성 대조: 알려진 답 절의 합성 파일에서 `1`
    도우미 지문: `dg.sh` sha256 앞 16 자 `a3f7b3be8cbbaebd`
- [ ] AP-04: frontmatter name 누락 금지 — 시작 판..가지 끝에 바뀐 `SKILL.md` · `agents/*.md` 전부의 첫 frontmatter 에 `name:` 이 있다 [exact]
    측정: `misc.sh` 의 `AP04 frontmatter_name=<n>/<n>` (두 수가 같고 1 이상 — `docs-site` · `reflect-digest` 가 바뀌므로)
    도우미 지문: `misc.sh` sha256 앞 16 자 `ee71e88cbcac65d0`

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 — validate-plugin 의 V3 · V6 · V10 이 한 코드 블록 판정을 함께 쓰고, 백틱 3 개로 시작하는 줄마다 켜고 끄기만 뒤집는 옛 토글이 남지 않는다 [exact]
    측정: `misc.sh` 의 `RE01 old_toggle=0` (`grep -cF 'startswith("```")' scripts/validate-plugin.py`). 동작이 하나로 모였는지는 SC-03 의 합성 결과가 잰다
    양성 대조: 시작 판에서 `RE01 old_toggle=2`
    도우미 지문: `misc.sh` sha256 앞 16 자 `ee71e88cbcac65d0`
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 킷 → 저장소 원본 폴더 짝을 `scripts/plugin_utils.py` 에 한 번 두고 validate-plugin 과 sync-orchestrator 가 그것을 쓴다(두 스크립트 안에 `"docs/backend` 글자 0) — 그 한 곳의 짝을 바꾸면 V10 결과도 따라 바뀐다 [exact]
    측정: `misc.sh` 의 `RE02 map_in_validate=0 map_in_orchestrator=0 map_in_utils=1`, 그리고 결합은 `vp.sh` 의 `v10-coupled rc=2 hit=0 gone=<1 이상> applied=1` (사본의 `scripts/plugin_utils.py` 에서 rust 짝만 없는 폴더로 바꾸면 V10 이 심은 표를 못 보고 없는 폴더를 이름으로 대며 FAIL). sync-orchestrator 동작은 DG-05 의 `sync-orchestrator rc=0` 이 잰다
    양성 대조: 시작 판에서 `map_in_orchestrator=1 map_in_utils=0` · `v10-coupled rc=0 hit=0 gone=0 applied=0`
    음성 대조: validate-plugin 이 자기 목록을 따로 두면 `v10-coupled` 가 `rc=2 hit=1 gone=0` 이 된다
    도우미 지문: `misc.sh` sha256 앞 16 자 `ee71e88cbcac65d0` · `vp.sh` sha256 앞 16 자 `94bc19dc459a9f8c`

## Diagnostics

- [ ] DG-01: N/A (commands.analyze `bash -n scripts/release.sh` 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `misc.sh` 의 `DG01_03 release_sh_changed=0`. 대신 바뀐 스크립트 문법은 DG-02 가 잰다)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (diagnostics.ide_exclude `[]` 제외 없음) — 시작 판..가지 끝에 바뀐 마크다운의 더한 줄에 markdownlint 새 경고 0 건(편집기 설정 · 스펠체크 제외), 바뀐 파이썬 전부 컴파일, 바뀐 셸 전부 `bash -n` 통과, 바뀐 JSON 전부 읽힘, `actionlint .github/workflows/ci.yml` 종료 코드 0 [exact]
    측정: `dg.sh` 의 `md_files=<수> md_new_warn=0 py=<n>/<n> sh=<n>/<n> json=<n>/<n> actionlint_rc=0` (각 쌍의 두 수가 같다)
    양성 대조: 알려진 답 절 — 기준 `f81568d` 로 재면 `md_new_warn=19`
    도우미 지문: `dg.sh` sha256 앞 16 자 `a3f7b3be8cbbaebd`
- [ ] DG-03: N/A (commands.test `bash scripts/release.sh 2>&1 || true` 는 release.sh 를 돌릴 뿐 이번 변경을 부르지 않는다 — 교집합 0 개, 같은 측정 `DG01_03 release_sh_changed=0`. 대신 저장소 시험 전부는 DG-05 가 잰다)
- [ ] DG-04: N/A (산출물에 구동할 앱 · 서버가 없다 — 검사 스크립트 · 문서 · README 뿐. 실행으로 재는 몫은 DG-05 로컬 CI)
- [ ] DG-05: 로컬 CI 도구가 가지 끝 작업 폴더에서 모든 단계를 종료 코드 0 으로 끝내고(yq 없는 `feedback-agg-test` SKIP 하나만 예외), CI 파일에서 이 도구 밖 `run:` 줄은 설치 단계 다섯과 SC-09 의 맞대기 검사 한 줄뿐이다 [exact]
    Given: 작업 폴더 HEAD = 가지 끝, 추적 파일에 커밋 안 된 변경 0 (아니면 `PREMISE_FAIL`). 측정: `ci.sh` 가 `ci_local_sha=59fe55125c0dbc77` · `steps=25 rc0=25 not0=[] skip=[feedback-agg-test SKIP (yq 없음);]` · `outside_ci_local=` 에 `pip install pyyaml` · `command -v zsh` · `npm ci` · `npx playwright install` · `run: |` 다섯과 `detect-docs-drift.py` 한 줄
    양성 대조: 시작 판 작업 폴더에서 같은 도구가 `rc=0` 25 개 · SKIP 1 개 · 밖 다섯 줄(2026-09-26 20:0x 실측) — 기대값과 다른 점은 맞대기 검사 줄 하나다. 실행기 패턴 하나를 망가뜨리면 `kaizen-assertions` 단계가 `rc=1` 이 되는 것은 SC-01 이 같은 실행기로 잰다
    도우미 지문: `ci.sh` sha256 앞 16 자 `677b788aa65f8a8b`
