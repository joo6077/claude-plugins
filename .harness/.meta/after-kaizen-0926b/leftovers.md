# 남은 할 일 모음 (2026-09-26, 기준 origin/main `6378948`)

기준: 작업 폴더 HEAD = origin/main `6378948` 에서 파일을 직접 열어 확인했다. 줄 번호는 이 판 기준이다.
출처 약칭 — `FU` 부모 목록 followups.md(번호는 글머리 차례) · `c1a`~`d2` 는 `.harness/.meta/after-kaizen-0926/<묶음>-notes.md`
(`메모` = 다음 사이클 메모, `넘김` = 넘긴 것 절) · `c2` c2-carryover.md · `FN` final-notes · `F1H` f1-harness-followups · `F1K-<행>` f1-kit-followups 입력 행 ·
`F2` f2-review-fixes · `MEM` 메모리 project_after_kaizen_0924_pending.md · `PVS` `.harness/sprint-amendments-plugin-validation-page-sync.md` 끝 「다음 스프린트로 남기는 것」.

## hs — harness/scripts · evals · hooks

| ID | 요지 | 고칠 파일:줄 | 출처 | 비고 |
| --- | --- | --- | --- | --- |
| HS-1 | 피드백 저장이 계약 폴더를 셸 위치로 잡고(`contract_root`), `sprint_slug` · `contract_path` · `session_id` 를 초안 값 위에 또 붙여 한 파일에 두 번 든다. 초안 파일 이름 `.harness/feedback-draft.yaml` 도 고정이라 여러 세션이 덮는다 | `harness/scripts/save-feedback.sh:112-136`(`resolve_contract_root` 가 `HARNESS_CONTRACT` 를 안 봄) · `:295-321`(sed 는 project 두 칸만 이름 바꿈) · `harness/skills/sprint-contract/SKILL.md:838` · `:856` · `harness/skills/init/SKILL.md:61` | FU-1 · c2 F1H-39 남은 칸 · F1H-39 · phase3/4 notes | 계약 경로에서 계약 폴더를 뽑는다. Bash 호출 사이 `$CF` 가 비는 문제도 같은 자리(MEM 3번) |
| HS-2 | 피드백 저장 시험이 고정 `/tmp/test-*.yaml` 을 써서 다른 워크트리와 동시에 돌면 서로 지운다 | `harness/evals/kaizen/feedback-system/save-test.sh:45` · `:74` · `:106` · `:113` · `:123` · `:127-128` · `:164` · `:182` | FU-11 · c4d R6 | `mktemp -d` 한 폴더 아래로. `:150` 은 이미 mktemp |
| HS-3 | 커밋 안전 훅이 놓치는 두 모양 — (a) `git add <경로>` 가 싣는 그 경로의 삭제, (b) 하위 폴더에서 `commit -a` · `git add -A && git commit` 할 때 그 폴더 밖 삭제(60 개도 통과) | `harness/scripts/commit-guard.sh:234-245`(`:235` `ls-files --deleted` 가 지금 폴더 아래만 셈) | FU-8 · c1b N8 · c1b 메모 N8 | (a) 는 `add_all` 로 올리면 되돌림 검사가 꺼져 따로 설계 필요 |
| HS-4 | 평가자 카이젠 회귀 패턴 `silent-check` 셋 가운데 둘이 제목 글자만 봐서 본문이 비어도 통과 | `harness/evals/kaizen/evaluator-kaizen/assertions.json` `silent-check` 키 | c1a 넘김 (FN-18 뒷부분) | |
| HS-5 | 종료 코드 사용처 표에 새 검사 `check-reviewer-protocol-copies.py` 행이 없다 | `harness/evals/gate-exit-codes.md` 사용처 표 | c4b 넘김 | |
| HS-6 | 봉인 판 계약에서 측정 도우미 코드 블록을 떼는 스크립트 · 계약마다 되풀이되는 공통 정의를 harness 공용 파일로 | `harness/scripts/` (새 파일) + `harness/references/contract-schema.md` 측정 절 안내 한 줄 | c2 제안 둘째 · F1H 구현 중 넷째 · phase3/4/7 notes 메모 | 새 파일이라 계약 필요 |

## vs — scripts 검사 도구 · CI · 오케스트레이터 · *-kaizen 문서

| ID | 요지 | 고칠 파일:줄 | 출처 | 비고 |
| --- | --- | --- | --- | --- |
| VS-1 | 카이젠 회귀 패턴 실행기 빈틈 셋 — 빈 문자열에 맞는 패턴은 늘 통과, 키 값이 `[]` 면 통과, `pattern`/`file` 이 글자가 아니면 오류 종료 코드가 1(2 여야) | `scripts/run-kaizen-assertions.py:58-86`(`:81` `len(re.findall(...))`) | FU-10 · c1a 메모 2 | |
| VS-2 | V8 따옴표 검사가 중괄호 없는 `$CLAUDE_PLUGIN_ROOT` 를 못 본다(실행 비트 검사도) | `scripts/validate-plugin.py:635-637` | FU-10 · c1a 메모 3 | 가이드 V8 절 `:391-424` 도 같이 |
| VS-3 | V8 설명이 옛 글(실행 비트만) — 전수 찾기 뒤 고침 | `.claude/skills/react-kaizen/SKILL.md:103` (+ `grep -rn 'V8' .claude/skills harness/skills` 전수) | c1a 메모 5 | 가이드 수동 수정 표는 GD-1 |
| VS-4 | 빈칸 없는 `<!--AUTO:skills-->` 꼴 표지를 표지로도 경고로도 안 센다 | `scripts/sync-docs.py:41-46`(`MARKER_RE` · `MARKER_LINE_RE`) | FU-10 | |
| VS-5 | 킷 README 표 설명이 SKILL.md 설명 첫 줄만 옮겨 문장 중간에서 끊긴다 | `scripts/sync-docs.py`(설명 읽는 부분) → 다시 만들 곳 `planning-kit/README.md:21` · `:25` · `rust-kit/README.md:16` 외 전 킷 | c1a 메모 6 · c1a 판단 넷째 | 고치면 모든 킷 README 재생성 |
| VS-6 | sync-docs 가 그리는 표 구분 줄 `\|------\|` 이 MD060 경고를 낸다 | `scripts/sync-docs.py:251-256` 등 표 그리는 함수 전부 | c4a 넘김 · c4a R5 · R6 뿌리 | VS-5 와 한 번에(둘 다 전 킷 README 재생성) |
| VS-7 | 감사 기록 도구 소제목이 같은 날 같은 사이클이면 또 겹친다(MD024) | `scripts/append-audit-log.py:139-141` · `.claude/skills/kaizen-orchestrator/SKILL.md:362`(시작 때 빈 항목) | FU-10 · c1a 메모 1 · FN-78 남은 부분 | 소제목에 항목 종류(시작·끝)나 시각 |
| VS-8 | 오케스트레이터 Final 이 감사 기록 도구를 `--watch` 로 부르는 걸음이 없다. `:33` · `:362` 는 옛 이름 「Step 11」 을 가리킨다(Final 은 F1~F4) | `.claude/skills/kaizen-orchestrator/SKILL.md:33` · `:362` · F1 절 `:581~` | c1a 넘김 둘째 · FN 교차 진단 계약 밖 결함 2 | |
| VS-9 | V3 · V6 가 옛 코드 블록 토글을 쓴다 → `_lines_outside_code_blocks` 로. V6 범위에 `skills/*/references/` 넣기(언어 힌트 없는 펜스 8 개 먼저 고침). V10 이 저장소 `docs/<킷>/` 원본을 안 읽음 | `scripts/validate-plugin.py:312-328`(V3) · `:515-545`(V6) · `:850-857`(V10 범위) + 가이드 판 번호 · 이력 | MEM 1번 · F1H-40 V6 범위 · F1H-94 · c1a 넘김 V6·V10 · c2 F1H-40 | 설계는 MEM 에 정해 둠(네 역할 · V6 는 백틱만). 합성 예제로 양성 대조 필수 |
| VS-10 | V2 「없음」 줄 상태는 OK 인데 글자가 `— SKIP (no templates/)` | `scripts/validate-plugin.py:239` · `:924` | F1H 구현 중 둘째 | 바꾸면 봉인된 옛 계약 DG-05 꼴과 어긋남 — 바꿀지 판단 |
| VS-11 | 오케스트레이터 범위 줄에 킷 `scripts/` · `templates/` 가 없다 | `scripts/sync-orchestrator.py:39` `KIT_SCOPE_DIRS` · `.claude/skills/kaizen-orchestrator/SKILL.md` 범위 줄 · `.claude/skills/kaizen-orchestrator/references/phase-dependencies.md` | c1b 메모 N7 · c1b 넘김 N7 | kaizen-flow.html 카드도 다시(docs) |
| VS-12 | Phase 별 데이터 풀 절 배정이 5~10 만 §2 · §3 | `scripts/spawn-kaizen-phase.sh:120` | c1b 넘김 N5 | |
| VS-13 | 드리프트 도구 짝 표에 오케스트레이터 → `docs/process/kaizen-flow.html`, `design-kit/skills/design-mockup/SKILL.md`, `infra-kit/skills/infra-test/SKILL.md`, api-kit 설계 기록이 없다. 매핑 표 ↔ 스크립트를 늘 맞대는 검사도 없다 | `scripts/detect-docs-drift.py:34-98`(`SOURCE_TO_HTML` · `SOURCE_OVERRIDES`) · 새 검사 | d1 드리프트 절 · c1b 넘김 N4 | |
| VS-14 | `check-api-kit-docs` 가 같은 사이트 `assets/site.css` 링크까지 외부 리소스로 세어 api-kit 12 쪽이 실패 | `scripts/check-api-kit-docs.py:34` | d2 판단 · d2 넘김 | |
| VS-15 | run-evals · sync-evals 킷 목록에 api-kit 없음 | `scripts/run-evals.py:32-35` · `scripts/sync-evals.py:32` | c4a 넘김 | 지금은 CI 단계로 대신 |
| VS-16 | api 조사 지침에 바로잡힌 「경로 간 불변식은 Hurl 로 표현할 수 없다」 가 남음 | `.claude/skills/kaizen-orchestrator/references/phase-research-templates.md:303-304` | c3c 메모 2 | |
| VS-17 | Phase 5 · 9 조사 입력이 「fit-pal」 을 적어 rust-kit 에 앱 이름이 다시 들어올 길. 「킷 안 앱 이름 0 건」 검사를 둘지 | `.claude/skills/kaizen-orchestrator/SKILL.md:303` · `:307` · `references/phase-research-templates.md:90` · `:130` | c4c 메모 3 | |
| VS-18 | 오케스트레이터 F2 가 옛 원칙 「standalone」 을 적음 | `.claude/skills/kaizen-orchestrator/SKILL.md:620` | d2 넘김 | docs-site 쪽은 DC-5 |
| VS-19 | design · backend · rust-kaizen Gotcha 6 형제 표에 새 행(시각 종류 · 실패 원인 셋 · 미검증 두 카운터 · 편집 전 확정 등) | `.claude/skills/design-kaizen/SKILL.md` · `.claude/skills/backend-kaizen/SKILL.md` · `.claude/skills/rust-kaizen/SKILL.md:21` (Gotcha 6) | F1H-44 · phase6/7/9 notes | |
| VS-20 | bambu-kaizen 회귀 검증에 음성 대조 블록 실행 줄 · bambu-research 문구 | `.claude/skills/bambu-kaizen/SKILL.md:80` · `.claude/skills/bambu-research/SKILL.md` | F1H-59 · F1H-60 · phase13 notes 메모 | 문구 세부는 phase13-notes |
| VS-21 | 수집기 워크트리 묶기 규칙과 reflect-kit `facets_unmatched` 규칙이 다름 | `scripts/collect-kaizen-data.py:421` | F1H-81 | 지금 영향 0 |
| VS-22 | Final 에서 판 번호 목록을 손으로 적지 말고 원본 머리 설정에서 뽑는다 | `.claude/skills/kaizen-orchestrator/SKILL.md` F1 절 `:581~` | FN 교차 진단 측정 구멍 2 | |
| VS-23 | tone-kit 정합 검사가 강도 칸에 글이 덧붙은 줄을 못 읽음 — 앞머리만 보고 판정 | `.claude/skills/tone-kaizen/SKILL.md` (정합 검사 절) | FN 교차 진단 측정 구멍 3 | |
| VS-24 | 로컬 CI 도구에 `run-kaizen-assertions.py` 단계가 빠짐 | `.harness/handoff/2026-09-26-tools/ci-local.sh` (추적 안 된 파일) · 비교 `.github/workflows/ci.yml:52` | d1 R3 | 레포 밖 취급 파일 |
| VS-25 | 루트 README — 킷 절 스킬 목록 AUTO 블록이 넷(harness · flutter · rust · react)뿐, onboarding · tone · api · howto 절 없음, bambu 절 「references 4종」 옛 값 | `README.md:137-261`(`:148` · `:166` · `:206` · `:220` 블록) | F2 Final 메모 | sync-docs 가 세게 |
| VS-26 | 손대지 않은 기존 markdownlint 경고 — 루트 README 15 · rust-kit README 15 · planning-kit README 6 · onboarding README 2 · 검증 가이드 30 · docs-site SKILL 9 · phase-research-templates 12 | 각 파일 | c1a 넘김 끝 · c1b 넘김 끝 · c1b 메모 | 전역 규칙상 범위 밖 경고는 사용자 확인 대상이나 「전부 지금」 지시로 포함 |
| VS-27 | onboarding-kit 이 옛 값 검사 소스 목록에 없음 | `scripts/check-stale-values.py` `SOURCE_DIRS`(onboarding 0 건) | F1K-48 → phase14-notes 메모 | |

## cs — contract-schema.md · feedback-schema.yaml

| ID | 요지 | 고칠 파일:줄 | 출처 | 비고 |
| --- | --- | --- | --- | --- |
| CS-1 | 자기진단 체크리스트 true 뜻을 「문제가 있다」 로 적고 새 키 둘(`measure_premise_unrun` · `known_answer_missing`) | `harness/references/feedback-schema.yaml`(체크리스트 절, `:93` 근처) | c2 F1H-35 · F1H-35 · phase2/4 notes | harness-kaizen Gotcha 가 이 파일 수정을 막는다 — 그 조문도 확인 |
| CS-2 | 측정 관례 묶음(F1H-37 남은 것) — 개정 번호 이어 붙이기 · 열 번호 정규식(`경로:13:8`) · 넘김 목록은 `경로:줄` 로 쪼개 재기 · 측정 묶음을 QA 에 같이 넘기기 · `mktemp -d "${TMPDIR:-/tmp}/x.XXXXXX"` · 두 판 풀기 공통 정의(실패 멈춤·끝나면 지움) · 검사기가 돌았다는 줄 함께 세기 · 서명 없는 커밋 두 측정 태도 맞추기 · 「바꾸지 않는다」 구간은 더한 줄 자리·수까지 | `harness/references/contract-schema.md` 측정 절들 | c2 F1H-37 · F1H-37 · phase2/3/4/7/9/10 notes 메모 | 「봉인 둘째 줄」 은 처리됨(#114) |
| CS-3 | 검사 산출물 조건의 ①~④ 계약 측 짝 | `harness/references/contract-schema.md` | c2 F1H-38 · phase3 넘김 | 생성 측은 GD-7 |
| CS-4 | `comm` 앞 정렬은 `LC_ALL=C sort` (`sort -n` 금지) | `harness/references/contract-schema.md` §셸 이식성 규약 | FU-2 (C3a DG-02) | |
| CS-5 | 풀어 둔 판에서 `validate-doc-contracts.py` 는 `git init` 한 사본에서 돌린다 | `harness/references/contract-schema.md` 측정 예시 | c2 제안 첫째 · F1H 구현 중 셋째 | |
| CS-6 | 「기존 동작 유지」 조건은 기준 판과 새 판을 여러 입력 모양으로 맞대는 측정을 둔다(목표 문장 하위 문장 분리 · 무작위 입력 최소 요건) | `harness/references/contract-schema.md` 조건 패턴 | FU-7 · c1b 메모 QA-1 | 「계약 문언 밖」 → 「조건 문장 안, 측정 밖」 용어도 |
| CS-7 | 「미커밋 변경 0」 전제는 QA 가 바꾸는 계약 자신의 status 줄을 빼고 잰다 | `harness/references/contract-schema.md` | c3a 메모 5 | |
| CS-8 | 판정 규칙을 바꾸는 계약의 대응표에 FAIL ≥ 1 칸을 넣는다 | `harness/references/contract-schema.md` | c4b 메모 1 | |
| CS-9 | 편집기 경고 조건은 `<!-- AUTO:* -->` 블록 안 · 밖을 나눠 잰다 | `harness/references/contract-schema.md` · `harness/skills/sprint-contract/SKILL.md` | c4a R6 | |
| CS-10 | 측정 도구(markdownlint-cli2 등)의 판과 설치 명령을 준비 단계에 적는다 | `harness/references/contract-schema.md` | F2 메모 끝 | |
| CS-11 | 페이지 맞추기 계약 교훈 다섯 — `N plugins` 영어 꼴 · 쉼표 나열, 작은따옴표 `src` · `@import` · `//` 주소, 도구가 죽어도 0 줄 통과, 상세 줄 모양, 양성 대조를 조건에 | `harness/references/contract-schema.md` 조건 패턴 | MEM 5번 · PVS 1 · 2 · 3 · 4 · 6 | PVS 5 는 GD-1 |
| CS-12 | 계약 범위를 적는 `# sprint-scope` 블록 — 쓰는 절차(스키마 절 · sprint-contract Step 6)와 읽는 쪽(커밋 훅이 `owner_session` 으로 계약 찾기) | `harness/references/contract-schema.md` · `harness/skills/sprint-contract/SKILL.md` Step 6 · `harness/scripts/commit-guard.sh` · 지금 설명은 `harness/README.md:67-70` | c2 F1H-40 · F1H-40 · phase4 넘김 | hs · gd 에 걸침 |

## gd — 가이드 · harness 스킬 · 에이전트

| ID | 요지 | 고칠 파일:줄 | 출처 | 비고 |
| --- | --- | --- | --- | --- |
| GD-1 | 검증 가이드 — FAIL 예시 2 머리가 design-kit 인데 명령은 reflect-kit 것이고 출력이 한 줄, 수동 수정 표 V8 행에 따옴표 고치는 법 없음, 변경 이력에 V8 따옴표 줄 없음, 출력 예시 `Total: 2 plugins` 는 만들 수 없는 조합 | `harness/docs/guides/plugin-validation-guide.md:447-453` · `:590` · `:695` 뒤 · `:550` | c1a 메모 4 · c1a 넘김 여섯째 · MEM 5번 · PVS 5 | 고친 뒤 DC-4 |
| GD-2 | 평가 가이드 미검증 정본 절이 두 번(`:1236` · `:1308`) — 조항 번호 겹침 · 머리 「5 조항」 · 「현재 drift」 문단 정리, 그리고 킷 쪽 「정본 조항 3」 표기 | `harness/docs/guides/qa-evaluation-guide.md:1249-1257` · `:1308` · `backend-kit/skills/backend-audit/SKILL.md:116` · `rust-kit/skills/rust-audit/SKILL.md:131` · `react-kit/references/render-evidence-protocol.md:209` | c4b 넘김 첫째 · phase9 넘김 | 킷 셋을 함께 고침 |
| GD-3 | `model` 생략 동작(지금 「inherit 기본값」) · 스킬 공식 필수 필드 · 다른 플랫폼 무시 문장 — 공식 문서로 다시 확인 뒤 가이드와 스킬을 같이 | `harness/docs/guides/agent-design-guide.md:84` · `harness/skills/create-agent/SKILL.md:25` · `harness/skills/create-skill/SKILL.md:29` · `harness/docs/guides/skill-design-guide.md` §frontmatter(`:393` · `:806` 근처) | c2 F1H-40 · F1H-40 · phase1/4 notes | 외부 EX-2 · EX-3 |
| GD-4 | 같은 작업 폴더에서 `checkout -b` 하지 않는다는 문장을 Step 6.7 (a) 와 skill 가이드 §9 에 | `harness/skills/sprint-contract/SKILL.md:764` · `harness/docs/guides/skill-design-guide.md` §9 | c2 F1H-40 · F1H-40 · phase4 넘김 | |
| GD-5 | `/sprint` Step 3 원인 가르기 판정 표 — CI 에서만 보이는 두 경우 · 첫 줄 「내가 쓴 목록 밖이면 남의 미커밋」 이 느슨함. 글자 사본 둘도 같이 | `harness/skills/sprint/SKILL.md:116-120` · `docs/infra/platform/cicd.md:77` · `rust-kit/skills/rust-preflight/SKILL.md:123` | c4d 넘김 첫째(F1H-41 앞절반) · F1H-41 · phase8/9 notes | |
| GD-6 | 세 화면 규약(design · flutter · react)이 같이 쓰는 숫자(2 개 이상 · 3 회)의 원문 절을 skill 가이드에 두고 규약은 인용으로 | `harness/docs/guides/skill-design-guide.md` 새 절 → `design-kit/references/visual-change-protocol.md` · `flutter-toolkit/references/visual-evidence-protocol.md` · `react-kit/references/render-evidence-protocol.md` | c2 F1H-43 · F1H-43 · F1K-15 · phase6/10 notes | KD-3 가 뒤따름 |
| GD-7 | §3.7 ①~④ 생성 측 짝 · 알려진 답은 흔한 실수를 넣은 사본에서 값이 떨어지는지 봉인 전에 | `harness/docs/guides/skill-design-guide.md` §3.7 | c2 F1H-38 · phase3 넘김 · phase13 메모 | |
| GD-8 | 근거 다시 확인 뒤 고칠 것 — agent 가이드 §7 오류 문구 둘 짝 · `omitClaudeMd` · `experimental` 뜻 · 문장 삭제 사본 검토 절차 · 평가 가이드 「12 개 이상의 편향」 | `harness/docs/guides/agent-design-guide.md` §7 · `harness/docs/guides/qa-evaluation-guide.md:147` · `:1944` | c2 F1H-80 · F1H-80 · phase1/3 notes | 외부 EX-2 · EX-4 |
| GD-9 | contract-kaizen · evaluator-kaizen Step 7 회귀 검사가 새 실행기 `scripts/run-kaizen-assertions.py` 를 부르게 | `harness/skills/contract-kaizen/SKILL.md:112-120` · `harness/skills/evaluator-kaizen/SKILL.md:109~` | c1a 넘김 셋째 | |
| GD-10 | 판정값을 바꾸는 계약은 `templates/` 리포트 틀까지 판정값 낱말로 검색해 범위를 잡는다 | `harness/skills/sprint-contract/SKILL.md` 복잡도 · 범위 절 | c4b 메모 2 | |
| GD-11 | QA 를 다시 부르기 전 앞 회차 리포트를 커밋하거나 지운다 | `harness/skills/sprint/SKILL.md` QA 걸음 · `harness/agents/qa-evaluator.md` | c4b 메모 4 | |
| GD-12 | harness-kaizen 추적 규칙 표의 커밋 머리 `kaizen:` 이 실제 관행과 다름 — 표를 고칠지 따를지 | `harness/skills/harness-kaizen/SKILL.md` 추적 규칙 표 | F1H-37 끝 · phase4 메모 | |

## pd — PRD 없음 · 폐기 결정 규칙 (c4d R 표)

| ID | 요지 | 고칠 파일:줄 | 출처 | 비고 |
| --- | --- | --- | --- | --- |
| PD-1 | PRD 가 없을 때 결정 원문은 계약 `범위 경계` 한 곳에만, 승인 기록에는 경로만. 대체 조건을 프로젝트 단위(`prd-*.md` 0 개)에서 기능 단위(「그 기능 PRD 없음」)로 | `design-kit/skills/design-mockup/SKILL.md:169` · `harness/skills/sprint-contract/SKILL.md:641` · `harness/skills/sprint/SKILL.md:78` (`design-kit/references/visual-change-protocol.md:221-222` 와 맞춤) | FU-4 · c4d R3 | **부모 결정 (a)** 대로. 고친 뒤 `docs/design-kit/design-mockup.html` 재생성(DC-15) |
| PD-2 | 새 워크트리에서는 추적 안 된 `.planning` · `.harness` 가 없어 「기록 없음」 과 「못 봄」 이 같은 빈 출력 | `harness/skills/sprint/SKILL.md:64-65` (권고 `:42-51`) | c4d R1 | 본 작업 폴더(`git worktree list` 첫 줄)도 보거나 못 읽은 자리를 말하게 |
| PD-3 | `PRD 없음` 이 흔한 말이라 규칙 설명 문서 · QA 리포트까지 잡힌다 | `harness/skills/sprint/SKILL.md:65` + SC-01 시험 폴더(규칙 설명 문장이 든 파일 추가) | FU-12 · c4d R2 | 찾는 모양을 좁힌다 |
| PD-4 | PRD 가 나중에 생기면 `PRD 없음` 줄을 PRD 비범위 표로 옮기는 절차 | `planning-kit/skills/plan-prd/SKILL.md` Step 0 | c4d 넘김 둘째 | planning-kit 폴더지만 이 규칙 묶음 |

## kit-flutter-toolkit

| ID | 요지 | 고칠 파일:줄 | 출처 | 비고 |
| --- | --- | --- | --- | --- |
| KF-1 | widget-inspector 새 값 `건너뜀 — 관례 표 없는 호출` 을 재는 평가 사례가 없다. 루트 CLAUDE.md 평가 사례 수 두 문장이 서로 다름(23 · 20, 실제 23) | `flutter-toolkit/evals/evals.json` · `CLAUDE.md:52` · `:373` | c3a 메모 1 | CLAUDE.md 는 루트 파일 |
| KF-2 | flutter-audit 안 옛 다섯 조항 사본 → 평가 가이드 v5.1 | `flutter-toolkit/skills/flutter-audit/SKILL.md:34-54` | c4b 넘김 둘째 | |
| KF-3 | Makefile 규칙을 따르는 스킬 넷(flutter-preflight · flutter-run · flutter-ai-rules · project-detection)을 다음 계약 허용 경로에 처음부터 | `flutter-toolkit/skills/flutter-kaizen/SKILL.md` (계약 작성 주의) | c3a 메모 4 | 교훈 한 줄 |
| KF-4 | F1K-12 남은 것 — go_router · auto_route · flutter-audit `:50` · codegen 안내 셋 · 평가 사례 18 | phase5-notes 원문 확인 뒤 해당 스킬 | F1K-12 | 세부는 `.harness/.meta/kaizen-0924/phase5-notes.md` |

## kit-design-kit

| ID | 요지 | 고칠 파일:줄 | 출처 | 비고 |
| --- | --- | --- | --- | --- |
| KD-1 | 「미검증 0 건 · L3 10 개 미만 → CONDITIONAL APPROVE」 design-kit 고유 규칙을 v5.1 과 맞춤 | `design-kit/skills/design-audit/SKILL.md:118` · `:235` · `design-kit/agents/design-reviewer.md` | c4b 넘김 넷째 | |
| KD-2 | 감사 기준 행간 1.2~1.6 이 문서 사이트 1.7 과 어긋남 | `design-kit/skills/design-audit/references/audit-criteria.md:10` | d2 넘김 셋째 | DC-5 와 같이 |
| KD-3 | 규약 머리가 금한 임계값 재정의(2 개 이상 · 3 회)가 다섯 자리에 | design-kit 스킬 · 감사 다섯 자리 | F1K-15 · phase6 메모 | GD-6 뒤 |
| KD-4 | F1K-18 — design:P2 · `UNVERIFIED_ENV` · §3.7 네 칸 · design-mockup Step 0 · Material 3 · OKLCH(`Figma Variables는 OKLCH 미지원` 단정) | `design-kit/skills/design-system/SKILL.md:27` 외 · phase6-notes 「미반영 키」 | F1K-18 · phase6 메모 | OKLCH 는 외부 EX-13 |

## kit-infra-kit

| ID | 요지 | 고칠 파일:줄 | 출처 | 비고 |
| --- | --- | --- | --- | --- |
| KI-1 | 사전 검사 `CORE_TOOLS="grep"` 때문에 python3 · PyYAML 만 있는 환경도 종료 코드 2 — 도구 조합으로 가른다 | `infra-kit/skills/infra-test/SKILL.md:225` · 표 줄 `:389` | c3a 메모 2 | |
| KI-2 | 핀닝 규칙 오류 문구가 쉬운 말 목록 낱말(「파싱 실패」) — checkout 규칙처럼 「YAML 읽기 실패」 로 | `infra-kit/skills/infra-test/SKILL.md:332` · `docs/infra-kit/infra-test.html:615` | c3a 메모 3 | 페이지도 같이 |
| KI-3 | 판정 세 줄이 `docs/infra/platform/cicd.md` 에만 있는 구조 — 원칙 문서 열두 개 전부 같은 구조 | `docs/infra/platform/cicd.md` 등 `docs/infra/` 원칙 문서 | F1K-24 · c3a 넘김 둘째 · F2 Phase 8 | 설치본에 `docs/` 없음이 문제의 뿌리 |
| KI-4 | F1K-25 — Flux · Argo · Kubernetes 1.37 · GitHub 밖 CI · 세 분류 규범 · 1.7+ · `env_gaps` | phase8-notes 원문 확인 뒤 | F1K-25 | 외부 EX-8 |

## kit-backend-kit

| ID | 요지 | 고칠 파일:줄 | 출처 | 비고 |
| --- | --- | --- | --- | --- |
| KB-1 | F1K-21 — OpenAPI 3.1 표기(최소 지원선인지) · 벽시계 문자열 · 시간대 저장 · AsyncAPI 3.1.0 | `backend-kit/skills/backend-system/SKILL.md` Step 2 · `backend-audit` Step 3 · `audit-criteria` §2 | F1K-21 · phase7 넘김 | 외부 EX-7. 「정본 조항 3」 은 GD-2 |

## kit-rust-kit

| ID | 요지 | 고칠 파일:줄 | 출처 | 비고 |
| --- | --- | --- | --- | --- |
| KR-1 | 옛 실측 문장이 실제로 없던 크레이트 이름(`myapp-api` · `myapp-migration`)을 적음 → 이름 없이 사건만 | `rust-kit/references/project-detection.md:147-148` · `rust-kit/skills/rust-run/SKILL.md:26` · `rust-kit/skills/rust-preflight/SKILL.md:21` | c4c 메모 1 | |
| KR-2 | `name = "myapp-api"` 가 같은 파일 `{project}` 자리 표시와 방식이 다름 | `rust-kit/skills/rust-init/SKILL.md:245` (비교 `:91` · `:126` · `:159`) | c4c 메모 4 | |
| KR-3 | F1K-28 · phase9 — 감사 기준에 시각 종류 판정 행 · `:89` `utoipa 5.4 docs` 리터럴 · rust-init 등 버전 리터럴을 Step 2c 참조로 · testcontainers 전제 0.27 · rust-model 타입 대응 ORM 별로 | `rust-kit/skills/rust-audit/references/audit-criteria.md:89` · `rust-kit/references/project-detection.md:87` · `rust-kit/skills/rust-init/SKILL.md` · `rust-kit/skills/rust-model/SKILL.md:94` | F1K-28 · phase7/9 넘김 · phase9 메모 | 일부 외부(버전) |

## kit-react-kit

| ID | 요지 | 고칠 파일:줄 | 출처 | 비고 |
| --- | --- | --- | --- | --- |
| KRe-1 | F1K-32 — Activity canary · `<ViewTransition>` 로 Tier 2 옮길지 · react-reviewer §10 · `project-detect.sh` · 설계 문서 `g6-build-audit.md` dev 포트 · preflight 절 현행화 | `docs/react/kit-design/g6-build-audit.md:52` · `:144-206` · `react-kit/skills/react-animation/SKILL.md` | F1K-32 · phase10 넘김 · 메모 | 외부 EX-9. 설계 문서를 현행화할지 초판 기록으로 둘지 판단 |

## kit-planning-kit

| ID | 요지 | 고칠 파일:줄 | 출처 | 비고 |
| --- | --- | --- | --- | --- |
| KP-1 | F1K-34 — GitHub 문서 날짜 · Mermaid 12 · PRD 와 결정 기록 비교 | phase11-notes 원문 확인 뒤 planning-kit 스킬 | F1K-34 | 외부 EX-10. README 끊김은 VS-5 |

## kit-reflect-kit

| ID | 요지 | 고칠 파일:줄 | 출처 | 비고 |
| --- | --- | --- | --- | --- |
| KRf-1 | 「엔트리 0 이고 Stop 실패 시도가 1 이상일 때」 가 코드와 다름 — 「마지막 기록 · 정상 종료 뒤의 실패 시도」 로 | `reflect-kit/skills/reflect-digest/SKILL.md:259` · `:315` | c3c 메모 4 | |
| KRf-2 | 머리 주석이 아직 「`claude -p --model haiku`로 재시도」 — 실제는 `--safe-mode` | `reflect-kit/hooks/log-reflection.sh:250` | c3c 메모 5 | |
| KRf-3 | README 예시 `bash ${CLAUDE_PLUGIN_ROOT}/scripts/install-scheduler.sh` 따옴표 없음 | `reflect-kit/README.md:156` · `:159` · `:162` | c1a 넘김 일곱째 | |
| KRf-4 | F1K-39 남은 것 — hooks `async` · `last_assistant_message` · 지워진 워크트리 | `reflect-kit/hooks/` | F1K-39 · phase12 notes | 외부 EX-1(hooks 문서) |
| KRf-5 | (새로 봄) 오늘 19:09 `.errors.log` 에 `fail:codex-exit-2` 뒤 `fallback:claude-exit-1` — 대체 경로도 실패. 멈춤 문턱 재조정은 이런 `err=` 자료가 쌓인 뒤 | `reflect-kit/hooks/log-reflection.sh:269` 근처 · `~/.claude/logs/claude-plugins/.errors.log` | c3c 넘김 여섯째 + 이번 확인 | 원인 조사부터 |

## kit-bambu-kit

| ID | 요지 | 고칠 파일:줄 | 출처 | 비고 |
| --- | --- | --- | --- | --- |
| KBa-1 | 종류 줄만 빠진 목록에서 모든 키가 거짓 「키 스코프 불일치」 FAIL 로 끝나 enum 검사에 닿지 않는다 — 판정 동작을 고치고 `[미검증]` 줄에 「enum 값 검사 미실행」 도 넣는다 | `bambu-kit/skills/bambu-print-profile/SKILL.md:1604-1612` · `:1701` · `:2041` | c3c 메모 1 · c3c 넘김 첫째 | 고친 뒤 DC-6 |
| KBa-2 | 완료 검사가 SKILL.md 안에 박힌 스크립트라 따로 도는 실행 목록이 없다 — evals 실행 스크립트로 올려 CI 에 | `bambu-kit/evals/` (새 스크립트) · `.github/workflows/ci.yml` | c3c 메모 6 | |
| KBa-3 | 올리지 않은 가지 `feat/bambu-kit-orca-h2s-feedback`(다른 워크트리, main 에 안 합쳐짐)과 SKILL.md 충돌 | `bambu-kit/skills/bambu-print-profile/SKILL.md` | c3c 넘김 셋째 · F1K-44 | 그 가지 푸시 · PR 이 먼저(메모리 「bambu-kit 오르카 · H2S 피드백」) |
| KBa-4 | F1K-43 · phase13 — `[미검증]` 네 칸 다섯 자리 · 현행화 · 금지 키 FAIL 시험 파일 · 댓글 답글 배열 이름 · 받는 법 블록 403 경우 · 블록들이 `mktemp` 폴더를 남김 | `bambu-kit/skills/bambu-print-profile/SKILL.md` · `bambu-kit/evals/` | F1K-43 · phase13 메모 | |

## kit-tone-kit

| ID | 요지 | 고칠 파일:줄 | 출처 | 비고 |
| --- | --- | --- | --- | --- |
| KT-1 | 「정규식은 §4 완료 게이트 G-04 줄이 정본」 이 틀림 — 실제는 `audit_greps` 코드 블록 넷째 줄(`:245`) | `tone-kit/references/adapter-dart-flutter.md:26` | c3c 메모 3 · F1K-50 | |
| KT-2 | 원본이 글을 바꾸고도 머리 판(`0.1.0` · `2026-09-02`)을 안 올림 | `docs/tone/dart-flutter-idioms.md:3-4` | d1 넘김 | 페이지 머리도 따라 |
| KT-3 | F1K-52 — C-06 강도 · `etc_seq=663` · `__` 예시 · 3.38.4 · go_router 링크 · 위키 이전 · `material_ui` · `sources.md` | phase15-notes 원문 확인 뒤 tone-kit references | F1K-52 | 외부 EX-14 |

## kit-onboarding-kit

| ID | 요지 | 고칠 파일:줄 | 출처 | 비고 |
| --- | --- | --- | --- | --- |
| KO-1 | G1 음성 입력 「한 Step 에 출처 둘」 픽스처를 넣고 `gate_cases` 에 등록(`misplaced` 는 이미 있음) | `onboarding-kit/skills/setup-guide/evals/fixtures/` · `evals.json:157` | F1K 다음 사이클 Phase 14 | |
| KO-2 | F1K-48 — `guide_gate` 막는 요구 세 칸 검사 · CocoaPods → SPM · 서비스 계정 키 · 평가 날짜 | `onboarding-kit/skills/setup-guide/SKILL.md` · 예제 `docs/onboarding-kit/examples/` | F1K-48 · phase14 메모 | 외부 EX-11. AUTO 표지는 처리됨 |

## kit-api-kit

| ID | 요지 | 고칠 파일:줄 | 출처 | 비고 |
| --- | --- | --- | --- | --- |
| KA-1 | `/api-ui` 보고 목록 Step 7 줄에 칩 숫자 · 트리 줄 수(`chips` · `rows`)가 없다 | `api-kit/skills/api-ui/SKILL.md:241` (정한 곳 `:198`, 옮기라는 곳 `:186`) | c4a R1 | |
| KA-2 | 판정 줄이 어느 항목 것인지 적는 모양을 `/api-verify` 가 정하지 않음 → 정하고 `/api-ui` 는 앞머리를 떼고 옮긴다고 | `api-kit/skills/api-verify/SKILL.md:144` · `:177` · `api-kit/skills/api-ui/SKILL.md:90` · 예시 `api-kit/evals/fixtures/unjudged/.api/reports/2026-09-02T1422-dev/report.md:23` · `ui.html:1509` | c4a R4 | |
| KA-3 | 보류 · flaky 를 화면이 어떻게 보일지 규칙이 없다 | `api-kit/skills/api-ui/references/viewer-spec.md` | c4a 넘김 첫째 | |
| KA-4 | binary64 밖 숫자는 RFC 7493 이 SHOULD NOT 인데 킷은 실패로 막는다 — 표준보다 엄격하다는 걸 킷 문서에 밝힐지 | `api-kit/skills/api-contract/SKILL.md:72` · `api-verify/SKILL.md:125` · `api-probe/SKILL.md:191` | api0 「다음에」 | 근거 `.harness/.meta/evidence/rfc7493-ijson-2026-09-26.md` 있음 |
| KA-5 | F1K-57 남은 것 — `/api-contract` §9 예시 · CSP(v7 · v8 시안엔 없음, 예시 ui.html 에만) | `api-kit/skills/api-contract/SKILL.md` §9 | F1K-57 · c4a 넘김 셋째 | |

## kit-howto-kit

| ID | 요지 | 고칠 파일:줄 | 출처 | 비고 |
| --- | --- | --- | --- | --- |
| KH-1 | howto-reviewer 가 미검증 규칙 사본 검사에서 이유와 함께 빠져 있다 — v5.1 사본을 둘지 | `howto-kit/agents/howto-reviewer.md` · `scripts/check-reviewer-protocol-copies.py:47` | c4b 넘김 셋째 | |
| KH-2 | F1K-60 — howto-audit 리포트 미검증 칸 · DITA 2.0 · 러너 음성 대조를 킷 안에 · 러너 시간 · `design-brief.md:390` | `howto-kit/skills/howto-audit/SKILL.md` · `docs/howto/design-brief.md:390` | F1K-60 | 외부 EX-12 |

## docs — 문서 사이트

| ID | 요지 | 고칠 파일:줄 | 출처 | 비고 |
| --- | --- | --- | --- | --- |
| DC-1 | 대응 페이지 없는 원본 다섯의 새 페이지 + `docs/index.html` 등록 — api 연구 기록 · reflect-digest · tone adapter-contract · adapter-dart-flutter · locale-korean | 새 `docs/api-kit/research-log.html` · `docs/reflect-kit/reflect-digest.html` · `docs/tone-kit/adapter-contract.html` · `adapter-dart-flutter.html` · `locale-korean.html` · `docs/index.html` | FU-6 · c3c 드리프트 · d1 넘김 · d2 드리프트 | **부모 결정 (c)**. `detect-docs-drift.py --since 88ddfe5` 가 NEW 로 냄 |
| DC-2 | 좁은 화면 기준 폭에 320 — typography-scale 9px 넘침, theming 코드 줄 잘림 | `docs/design-kit/typography-scale.html` CSS `:179` · 마크업 `:577` · `docs/flutter-toolkit/theming.html`(`ColorScheme.fromSeed(seedColor` 줄) · 문서 사이트 시험 · `.claude/skills/docs-site/SKILL.md` 기준 폭 | FU-10(C3b) · c3b 메모 3 · d2 넘김 | **부모 결정 (b)** |
| DC-3 | 원본이 바뀌었는데 페이지가 옛 판 — contract-design-guide · qa-evaluation-guide 페이지는 v5.1 제목에 `measurement_digest` 0 건, static-evidence-viewer-contract 페이지는 「판정 불가」 0 건 | `docs/harness/contract-design-guide.html` · `docs/harness/qa-evaluation-guide.html` · `docs/api-kit/static-evidence-viewer-contract.html` | d2 N3 · 이번 확인 | 원본 `1922551` · `48618f6` 뒤 링크 한 줄 말고 안 바뀜 |
| DC-4 | 검증 가이드 고친 뒤 페이지 다시 맞춤 | `docs/harness/plugin-validation.html` | c1a 넘김 · GD-1 | |
| DC-5 | docs-site 스킬 안 어긋난 안내 — `:109` Motion 따로 대응 → 「공통 파일이 맡는다」, `:16` · `:5` standalone 과 공통 파일 링크, `:104` 행간 1.2~1.6 | `.claude/skills/docs-site/SKILL.md:5` · `:16` · `:104` · `:109` | d2 N2 · d2 넘김 셋째 · 넷째 | KD-2 · VS-18 과 같이 |
| DC-6 | bambu 미검증 표에 「종류 줄만 빠진 목록」 행, 「비었거나 깨짐」 행은 canonical 0 줄일 때로 | `docs/bambu-kit/bambu-print-profile.html:1647` | d1 R1 | KBa-1 뒤 |
| DC-7 | 「(표 칸에 옮기면 대안 기호가 깨진다)」 는 HTML 표에선 틀린 말 — 괄호 한 토막 빼기 | `docs/tone-kit/dart-flutter-idioms.html:1287` | d1 R2 | |
| DC-8 | 「정본은」 → 「기준 기록은」 | `docs/api-kit/multi-sample-pagination-variance.html:430` | d1 R4 | |
| DC-9 | 매핑 규칙 결정 — 짝 원본 없는 등록 페이지 21 쪽(`design-kit/references/visual-styles.md` 후보) · 없는 페이지를 가리키는 원본 43 개 이름 규칙 · howto `design-brief.md` ↔ `overview.html` 짝 · `process (공유)` 행 원본 칸을 오케스트레이터 SKILL.md 로 | `.claude/skills/docs-site/SKILL.md:68` 매핑 표 · `scripts/detect-docs-drift.py` | c1b 넘김 N1~N3 · c3b 넘김 넷째 | VS-13 과 같이 |
| DC-10 | 원본 md 쪽 옛 시안 v7 기재 | `docs/api/verification/static-evidence-viewer-contract.md:10` · `:82` · `:86` · `docs/superpowers/specs/2026-09-02-api-kit-design.md:483` · `:595` · `docs/api-kit/static-evidence-viewer-contract.html`(v7 5 곳) | c4a 넘김 둘째 | 원문 수정 대상 |
| DC-11 | 스크립트가 직접 주는 움직임(smooth 스크롤 다섯 쪽 · `.animate(` 한 쪽)은 공통 CSS 로 못 끈다 | `docs/design-kit/design-template.html` · `grid-alignment.html` · `ratio-proportion.html` · `visual-hierarchy.html` · `docs/process/kaizen-flow.html` · `docs/flutter-toolkit/animation.html` | d2 넘김 둘째 | 이번 확인에서 smooth 스크롤 쪽이 더 있음(backend-kit 셋 등) — 전수 다시 |
| DC-12 | 어두운 테마 전용 11 쪽의 밝은 테마 | c3b 가 손본 11 쪽 | c3b 넘김 셋째 | 공통 틀 변경 |
| DC-13 | 긴 쪽 `contract-schema.html` 이 같은 판 픽셀 비교에서도 1118px 흔들림 — 원인 조사 | `docs/harness/contract-schema.html` | d2 넘김 끝 | |
| DC-14 | 문서 사이트 계약은 옛 페이지 대비 원본 코드 표시 · 낱말 비율(담김)을 조건으로 | `.claude/skills/docs-site/SKILL.md` QA 절 | FN 교차 진단 측정 구멍 1 | |
| DC-15 | PD-1 뒤 design-mockup 페이지 다시 맞춤 · VS-11 뒤 kaizen-flow 카드 범위 칸 | `docs/design-kit/design-mockup.html` · `docs/process/kaizen-flow.html` | c4d R3 · c1b N7 | |

## user — 레포 밖 ~/.claude

| ID | 요지 | 고칠 파일:줄 | 출처 | 비고 |
| --- | --- | --- | --- | --- |
| US-1 | 세션 마감 훅이 작업 알림(task-notification) 글에 인용된 「다음 세션」 에도 반응 — 알림은 사용자 입력이 아니다 | `~/.claude/hooks/next-session-handoff.sh:6` | FU-3 | |
| US-2 | 병렬 세션 가드가 명령 인자 문자열 안 「git commit」(heredoc 아님)에도 알림. `GIT_INDEX_FILE=` 을 `git add` 에만 붙인 드문 꼴은 개인 인덱스 목록을 보임 | `~/.claude/hooks/parallel-session-guard.sh:29-57` | FU-9 · b-user 셋째 | |
| US-3 | heredoc 제거 awk 가 인라인으로 남음 → 공용 함수로 | `~/.claude/hooks/enforce-codex-stdin.sh:36` | b-user 첫째 | |
| US-4 | 핸드오프 커밋 예시의 공동 작성자 줄이 옛 모델 이름 | `~/.claude/skills/handoff/SKILL.md:138` | b-user 둘째 | |
| US-5 | 핸드오프 틀 「폐기한 결정」 칸이 결정 원문 자리(PRD 비범위 표 · 계약 범위 경계)를 가리키지 않음 | `~/.claude/hooks/next-session-handoff.sh:8` 틀 · `~/.claude/skills/handoff/SKILL.md` | c4d 판단 user-setup:P6 | c4d 는 「따로 둔다」 고 판단 — PD-1 과 맞출지 |

## 외부 — 저장소 밖 원문을 다시 받아야 판단되는 것

| ID | 요지 | 받을 곳 | 걸린 항목 | 근거 파일 |
| --- | --- | --- | --- | --- |
| EX-1 | 공식 hooks 문서가 `${CLAUDE_PLUGIN_ROOT}` 를 큰따옴표로 감싸라고 하는지 원문 대조 · Stop `last_assistant_message` · `async` | https://code.claude.com/docs/en/hooks | GD-1(`plugin-validation-guide.md:432` 문장) · KRf-4 | `.harness/.meta/evidence/phase12.md:14` · `:49` · `:113` |
| EX-2 | subagent `model` 생략 동작 · 배치 우선순위 · `omitClaudeMd` · `experimental` 뜻 · 두 오류 문구가 어느 상한 것인지 | https://code.claude.com/docs/en/sub-agents | GD-3 · GD-8 | `.harness/.meta/evidence/phase4.md:147-150` · `phase1.md:86` |
| EX-3 | 스킬 frontmatter 필수 필드(표준 vs Claude Code 런타임) · 비표준 필드 무시 보장 | https://code.claude.com/docs/en/skills · https://agentskills.io/specification | GD-3 | `.harness/.meta/evidence/phase4.md:151-153` |
| EX-4 | 「12 개 이상의 편향」 수치 | https://arxiv.org/html/2411.15594v6 · https://arxiv.org/html/2410.02736v1 | GD-8 | `.harness/.meta/evidence/phase3.md:154` · `qa-evaluation-guide.md:147` |
| EX-5 | build_runner 2.16 이후 `--delete-conflicting-outputs` 동작 | https://raw.githubusercontent.com/dart-lang/build/master/build_runner/CHANGELOG.md | c3a 넘김 셋째 · F1K-73 뒷부분 | `.harness/.meta/evidence/phase5.md:25` |
| EX-6 | H2S 펌웨어에서 `G91` 이 E 까지 상대로 바꾸는지 | 뱀부 펌웨어 원문(공개 문서 없음) — 참고 https://marlinfw.org/docs/gcode/G091.html , 실기 G-code 실측 | c3c 넘김 둘째 · F1K-42 | 지금은 `M83` 만 써서 영향 0 |
| EX-7 | OpenAPI 3.1 표기 뜻 · AsyncAPI 3.1.0 | https://spec.openapis.org/oas/latest.html · https://github.com/asyncapi/spec/releases/tag/v3.1.0 | KB-1 | `.harness/.meta/evidence/phase7.md:24` · `:135` |
| EX-8 | Flux · Argo · Kubernetes 1.37 | https://github.com/fluxcd/flux2/releases · https://kubernetes.io/releases/ | KI-4 | `.harness/.meta/evidence/phase8.md:39` |
| EX-9 | React 19.3 `<ViewTransition>` · Activity | https://react.dev/blog/2026/09/09/react-19-3 | KRe-1 | `.harness/.meta/evidence/phase10.md:147` |
| EX-10 | Mermaid 12 · GitHub 문서 날짜 | 근거 파일의 링크 | KP-1 | `.harness/.meta/evidence/phase11.md:22` · `:24` · `:106` · `:146` |
| EX-11 | Firebase iOS CocoaPods → SPM | https://firebase.google.com/docs/ios/setup | KO-2 | `.harness/.meta/evidence/phase14.md:104` |
| EX-12 | DITA 2.0 | https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=dita | KH-2 | `.harness/.meta/evidence/phase17.md:46` · `:48` |
| EX-13 | Figma Variables 의 OKLCH 지원 여부 | Figma 공식 도움말(변수 색 형식) — 근거 파일에 주소 없음 | KD-4 | phase6-notes 메모 둘째 |
| EX-14 | tone 3.38.4 · go_router 링크 · 위키 이전 등 | 근거 파일 `.harness/.meta/evidence/phase15.md` 의 링크 | KT-3 | phase15-notes |

## 처리됨

| ID | 근거 |
| --- | --- |
| F1H-14 · F1H-84 · FN-18 · FN-43 (회귀 패턴 실행기 · CI 줄) | `b9aea2c` · `.github/workflows/ci.yml:52` (남은 빈틈은 VS-1 · HS-4) |
| F1H-37 「봉인 둘째 줄」 · MEM 2번 | PR #114 `1922551` (`measurement_digest`) |
| F1H-39 Step 9 문구 · MEM 3 · 4번 | PR #116 `9146eb5` (고정 초안 이름은 HS-1 에 남김) |
| F1H-41 뒷절반 (재검증 블록 폐기 결정 자리) | `ad9fe5c` · `harness/skills/sprint/SKILL.md:64-78` |
| F1H-47 · F1H-48 · F1K-33 · F1K-69 · F1K-70 · F2 reviewer 넷 · F1K Phase 3 뒤 | c4b `2b82945` ~ `8b27b36` · `a463cb8` |
| F1H-56 · F1K-39 따옴표 부분 | `f705e1c` · `1861c65` · `372dc38` · `c1843a5` · `51f655c` |
| F1H-58 | 할 일 없음 — `reflect-kit/evals/` 에 `hooks/` 만 있고 `evals.json` 없음 |
| F1H-65 | 할 일 없음 — onboarding 평가는 CI 러너 단계로 대신(F1H 계약 AR-02) |
| F1H-66 · F1K-48 AUTO 표지 | `282f7c0` · `d9c2623` · `399b9a9` · `a579f82` |
| F1H-67 · FN-56 · F1K-56 | `22d5901` |
| F1H-76 | `9c24bbc` |
| F1H-77 | `a99a1ca` |
| F1H-78 · F2 tone 「N종」 셈 | `b367184` |
| F1H-79 · FN-64 | `72d6ddd` · `scripts/check-stale-values.py:45` · `.harness/stale-values.yaml:20-24` |
| F1H-82 · c4a 「CI 새 단계 한 번 통과」 | GitHub CI 우분투 실행 성공 — run `36233220180`(PR #118) · `36233420090`(main 합침) · 3 분 22 초 |
| F1H-91 · F2 드리프트 초안 폴더 제외 | `aea6e75` (`scripts/detect-docs-drift.py` `SOURCE_EXCLUDES`) |
| F1H-92 | `4bc33c8` |
| F1H 구현 중 첫째 (옮긴 폴더를 삭제로 셈) · F2 `-i` 설명 줄 | `7b0ba08` · `bb4b2b1` |
| F2 sync-orchestrator 범위 줄 | `afff36a` · `1dd2406` (scripts/templates 는 VS-11) |
| FN-39 (PR) | PR #109 · #110 합침(메모리 「9-24 전체 카이젠 끝」) |
| FN-76 | `18b05e6` |
| FN-77 | final-notes 표 「2026-09-26 에 끝냈다」 |
| FN-78 (소제목 날짜 · 빈 줄) · FN 계약 밖 결함 2 의 도구 쪽 | `7f4559b` (`--watch` 추가. 같은 날 겹침은 VS-7, 오케스트레이터 호출은 VS-8) |
| FN-79 · c3b 넘김 FN-79 | `a987ef3` · `.claude/skills/docs-site/references/css-tokens.md:41` |
| FN-80 · c3b 메모 1 (kaizen-flow 합친 뒤 맞춤) | `5994ee6` · `05fcdcd` · `6fd1505` (`docs/process/kaizen-flow.html` 에 `flutter-toolkit/evals` 1 건) |
| F2 infra-test checkout YAML | `19d93cd` · `92d2294` |
| F2 flutter 넷 · F1K-10 · F1K-73 · F1K Phase 5 `-d` | `1428484` · `4dedb85` (플래그는 유지로 결정 — c3a 판단) |
| F2 bambu enum 문구 | `86d2074` |
| F2 api `-0` · noncharacter · F1K-80 · F1K Phase 16 `-0` · c3c 넘김 api-verify 이름 | `38b6076` · `2ca8942` · `f20f3b0` |
| F2 design status · `excluded_surfaces` | `76debef` |
| F2 reflect README `ok:no-issues` | `reflect-kit/README.md:84` · `~/.claude/logs/claude-plugins/.errors.log` 에 `ok:no-issues` 2 줄 관측 |
| F1K Phase 12 멈춤 경고 문턱 · `claude -p` 훅 | `1b26074` (`--safe-mode`) |
| F1K-53 · F1K Phase 16 판정 불가 | `48618f6` · `5ceca27` |
| F1K-29 · F1K Phase 9 rust 앱 이름 66 곳 | `1b3e53d` (남은 옛 실측 문장은 KR-1) |
| F1K-31 · F1K Phase 10 템플릿 | `9a7c914` |
| F1K-26 README 평가 사례 수 | infra 6 · backend 8 이 `evals.json` 실제 수와 같음 (`infra-kit/README.md:56` · `backend-kit/README.md:56`) |
| c1a 넘김 첫째 (F1H-79) | `72d6ddd` |
| c1b 넘김 N6 (howto 연구 기록 안 만듦) | 결정으로 끝 — 오케스트레이터 Gotcha · Phase 17 틀에 기록 |
| c3a 문서 페이지 넷 | `f7878c6` · `b29f482` · `d213037` · `92d2294` |
| c3b 메모 2 (design-concept 공백) | `bac16b0` |
| c3b 메모 4 (`__pycache__`) | `39ddc12` |
| c3b 메모 5 · c4a R2 · d1 R4 커밋 메시지 낱말 | 할 일 없음 — 기록을 다시 쓰지 않기로 확정 |
| c3b c4d 겹침 · c4d R4 (design-mockup 페이지) | `796fba0` |
| c3b 공통 틀 움직임 · 행간 · MEM 6번 | `33fec27` · `c5aae49` · `6d36b2f` |
| c3c 드리프트 페이지 둘 · c3c 메모 2 HTML 쪽 | `45a47ab` · `a0dad4b` · `4033bbe` · `bcb4b1b` |
| c4a R5 (DG-02 개정 동의) | `5fe50bf` — AskUserQuestion 2026-09-26T09:03:30 사용자 동의 기록 |
| c4a 넘김 「가지를 origin/main 에 맞출지」 | 합쳐짐 `9a85d58` |
| c4c 메모 2 · c4d R5 (봉인된 계약 글) | 할 일 없음 — 봉인 계약은 안 고침. `커버리지 해소:` 규칙은 `harness/skills/sprint-contract/SKILL.md:697` 에 있음 |
| d2 N1 (contract-schema 페이지 충돌) | `docs/harness/contract-schema.html` 제목 v5.6 · `measurement_digest` 6 건 · 공통 파일 링크 1 건 |
| MEM 1번 V10 코드 블록 판정 | PR #111 (남은 V3 · V6 는 VS-9) |
| c2 F1H-41 · F1H-47 · F1H-48 | c4d · c4b 묶음(위 행) |

## 사용자 결정 필요

| ID | 무엇을 | 선택지 |
| --- | --- | --- |
| UD-1 | C3a 가 과제 목록을 뒤집은 두 결정(FU-5) — 알리고 유지할지 | 유지(build_runner `--delete-conflicting-outputs` 명령에 둠 · react-kit `harness-project.yaml.template` 을 react-init 13 단계가 씀) / 뒤집기(플래그 빼기 · 템플릿 지우기) |
| UD-2 | 증거 캡처 PNG 12 장(1.6 MB)이 main `.harness/.meta/after-0924-api-ui-unjudgeable/cap/` 에 들어감(c4a R3) | 그대로 둔다 / 새 커밋으로 지운다(기록엔 남음) |
| UD-3 | flutter-preflight · react-preflight 에 기준 커밋 비교(판정 세 줄)를 넣을지(KF · F1K-11 · c3a 넘김) | 넣는다(`/sprint` Step 3 표 사본 넷째) / 넣지 않는다(근거 없음으로 닫음) |
| UD-4 | 드리프트 도구가 NEW 로 내는 나머지 둘 — `rust-kit/references/project-detection.md` · `phase-research-templates.md` 도 페이지를 만들지(부모 결정 (c) 다섯 밖) | 같이 만든다 / 다섯만 |
| UD-5 | 결정 전파 상태 값에 `approved` 밖(예: 대체됨)을 둘지(c3a 넘김 넷째) | 둔다 / `approved` 하나로 닫는다 |
| UD-6 | 설계 문서 `docs/react/kit-design/` 현행화(KRe-1 일부) | 현행화 / 초판 기록으로 두고 머리에 표시 |
| UD-7 | 범위 밖 기존 markdownlint 경고 정리(VS-26) — 전역 규칙이 사용자 확인을 요구 | 이번에 전부 / 이번 변경 줄만 |
| UD-8 | V2 SKIP 줄 글자(VS-10) — 봉인된 옛 계약 꼴과 부딪힘 | 글자를 판정과 맞춘다 / 그대로 둔다 |

부모가 이미 정한 것(표에 반영): (a) PD-1 · (b) DC-2 · (c) DC-1.
