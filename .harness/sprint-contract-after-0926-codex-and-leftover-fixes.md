---
feature: "Codex 1 차 점검 결함 둘 · 묶음 기록 「남은 것」 코드 · 규칙 문장 고침 (cx)"
slug: after-0926-codex-and-leftover-fixes
created: "2026-09-27 12:31"
complexity: "복잡"
conditions: 29
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:b825332e3932b0f2
measurement_digest: sha256:fc30d758abb4a9a8
locked_at: "2026-09-27 12:46"
---

## 배경

통합 가지 `chore/after-kaizen-0926b` 에 아홉 묶음을 합친 뒤 Codex 가 1 차 점검을 했다. 이 계약은 그 점검의 결함 둘과, 열두 묶음 기록(`*-notes.md`)의 「남은 것」 가운데
코드 · 규칙 문장으로 고칠 항목을 한 번에 고친다. 입력은 읽기만 한다 — 점검 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/codex-review-1.md`,
묶음 기록 같은 폴더 `cs` · `dca` · `dcb` · `gd` · `hs` · `k1` · `k2` · `pd` · `pd2` · `us` · `vsa` · `vsb` 의 `-notes.md`, 결정 `decisions.md`, 목록 `leftovers.md`, 바깥 원문 대조 `ex/EX-7.md`(OpenAPI 판 번호).

- Codex 결함 1 (막아야 함): `scripts/check-api-kit-docs.py:35` 의 외부 스타일 판정이 `HTTPS://` 대문자와 따옴표 뒤 빈칸을 놓친다. 대문자 `<LINK` · `<SCRIPT` 도 놓친다(vsa notes). 지금 12 쪽에는 그런 꼴이 없어 실제 피해는 0 이다.
- Codex 결함 2 (고치면 좋음): flutter-preflight · react-preflight 의 「실패 원인 가르기」 판정 표 사본이 원문(`harness/skills/sprint/SKILL.md` Step 3)의 강화된 첫 줄과 「CI 에서만 실패하면」 두 경우를 따라가지 못했다. 사본을 원문과 글자까지 같게 맞추고, 같은지 기계로 대조하는 검사를 새로 두어 CI 에 등록한다.
- 사용자 합의(Step 5): 위임으로 받은 것으로 적는다 — 세션 `bda55d45-296c-491f-89ba-b52042d58e72` 의 사용자 말 2026-09-26T10:09:00.557Z · 결정 답 2026-09-26T10:30:16.222Z · 추가 위임 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」. 조건을 느슨하게 하는 개정은 이 위임으로 동의 처리하지 않는다 — 봉인한 측정이 처음부터 틀렸으면 계약을 새 판(2 회차 계약)으로 다시 써서 다시 봉인한다(결정 파일 「추가 위임」 절).
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-cx`, 가지 `chore/ak2-cx`, 시작점 `82ec540`(통합 가지 끝, Codex 점검 기록 커밋). 시작 때 `git -C W status --short` 는 빈 출력이었다.
- 커밋 규칙: `git add <경로>` 뒤 `git commit -o <경로>` · 한 커밋에 맨 위 폴더 하나(레포 뿌리 파일 `CLAUDE.md` · `README.md` 는 둘을 묶어 한 커밋) · `git add -A` · `git stash` · push · 가지 바꾸기 금지. 커밋 메시지는 한국어, 끝에 빈 줄 뒤 `Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>`. 봉인 커밋(계약 한 파일)이 구현 커밋보다 먼저다.
- 구현 전에 `tone-kit:tone-guide` 1 단계(규칙 불러오기)를, 완료 선언 전에 5 단계(전수 대조)를 한다 — 대조 결과는 notes 에 남긴다(AR-02).
- 사용자가 할 일: 없음.

복잡도 4 축 — 넷 다 「예」 이고 공개 약속 변경과 소비자가 함께 있어 「복잡」 이다.

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 넷 — 검사 스크립트 · CI 설정(`scripts/` · `.github/`), 킷 스킬 · 참고 문서(여섯 킷), 계약 형식 문서 · 가이드(`harness/`), 레포 안내(`CLAUDE.md` · `README.md` · `.harness/project.yaml`) |
| 공개 API·계약 변경 | 밖에 드러난 약속이 바뀌는가 | 예 — 외부 리소스 판정 범위, 새 검사 스크립트의 출력 · 종료 코드, `dirty_except_status` 가 세는 값, 피드백 초안 `project_hash` 계산 규칙, 안티패턴 AP-04 의 판정 수단 |
| 소비면 존재 | 반대편이 있는가 | 예 — CI 두 단계, 사본 원문(`harness/skills/sprint/SKILL.md` Step 3)을 고치는 사람, `save-feedback.sh` 의 재계산 값, qa-evaluator 의 AP 판정, 설치본에서 원칙 문서를 여는 킷 사용자 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 12 쪽 api-kit 문서의 통과, reviewer 사본 검사 일곱 줄, `dirty_except_status` 의 기존 다섯 경우, 편집기 경고(표 줄 정렬) |

Step 2.5 짝 조건: 만드는 쪽은 SC-01(판정) · SC-02 · ER-01(새 검사) · SC-05(도우미) · SC-06(해시 조각) · SC-07(AP-04), 받는 쪽은 SC-03(CI 등록 · 종료 코드 표) · SK-01(사본과 원문 쪽 안내) · SK-09(qa-evaluator · sprint-contract 의 해시 설명) · SC-04(qa-evaluation-guide 의 사본 수 안내)다.

설정 값 대조 (`.harness/project.yaml` 을 글자 그대로 옮김):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A — 재는 파일이 바뀐 파일에 없다 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A — 같은 이유 |
| `diagnostics.ide_exclude` | `[]` | DG-02 의 `([] 제외)` |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 같은 넷 |
| `anti_patterns[].id` / `message` | AP-01 버전 하드코딩 · AP-02 force push · AP-03 bare code fence · AP-04 frontmatter name 누락 | AP-03 · AP-04 (바뀌는 파일에 코드 블록 있는 SKILL.md · 규약 문서가 있다). AP-01 은 `plugin.json` 판을 건드리지 않아서, AP-02 는 이 계약이 push 하지 않아서 뺐다. AP-04 는 이 계약이 판정 수단을 바꾸지만 message 는 글자 그대로 둔다(SC-07) |

## GAP 분석 (Pre-Edit Audit)

대상 파일을 읽기만 하고 줄을 적었다. 줄 번호는 시작점 `82ec540` 기준이다.

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 여부 |
| --------- | ---------------------------- | ------------------- | ---------------- |
| `scripts/check-api-kit-docs.py` | `:33-35` 외부 판정식 · `:70` 적용 · `:81-104` 전 쪽 순회 | 대소문자를 가린다. 따옴표 뒤 빈칸 · 탭 · 줄바꿈, `\\` 로 시작하는 주소를 넘기지 못한다. 18 사례 가운데 8 개를 틀린다(시작 판 실측 — `url(` 대문자 주소 U1 포함) | SC-01 |
| `harness/skills/sprint/SKILL.md` Step 3 | `:97` 절 머리 · `:121-125` 판정 표 · `:127-130` CI 에서만 실패할 때 두 경우 · `:132` `FORK_BASE` 문단 | 원문. 사본이 있다는 안내가 없다 — 원문만 고치면 사본이 뒤처진다(Codex 결함 2 의 뿌리) | SK-01 |
| `flutter-toolkit/skills/flutter-preflight/SKILL.md` | `:147` 절 머리 · `:149` 사본 출처 · `:167-171` 표(첫 줄이 옛 문장) | 첫 줄이 옛 규칙, 두 경우 없음. 원문 덩어리 8 줄과 끊김 없이 같지 않다(`flutter=0/8`) | SK-01 |
| `react-kit/skills/react-preflight/SKILL.md` | `:79` 절 머리 · `:81` 사본 출처 · `:99-103` 표 | 같은 결함(`react=0/8`) | SK-01 |
| `scripts/check-reviewer-protocol-copies.py` | `:2` 머리 설명 · `:35-43` `REVIEWERS` 일곱 · `:52` 정규화 · `:84` 덩어리 비교 함수 | flutter-audit 사본을 재지 않는다(k1 KF-2). 메모리 안에서 목록에 더해 재면 `MISMATCH … 조항` — 원문이 둘째 「3.」 을 3 항 안 문단으로 바꿨는데 사본은 옛 번호다 | SC-04 · RE-01 · RE-02 |
| `flutter-toolkit/skills/flutter-audit/SKILL.md` | `:36` 사본 출처(「3 이 둘이다」) · `:38` · `:93` MD029 끄고 켜기 · `:78` `3. **임계값 2 는` | 위 결함의 사본 쪽 | SC-04 |
| `harness/docs/guides/qa-evaluation-guide.md` | `:12` 참조 스키마 `(v5.5)` · `:15` · `:22` · `:2054`(2026-09-24 갱신 기록) · `:1210` 「다음 사이클 Phase 1 · 2 로 넘긴다」 · `:1257-1258` 사본 일곱 · `:1984` 참조 목록 · `:2063` Schema link | 스키마는 v5.7(`contract-schema.md:1465`). 넘긴다던 짝은 이미 생겼다(`skill-design-guide.md:392` · `contract-schema.md:1030`) | SK-03 · SC-04 |
| `harness/docs/guides/contract-design-guide.md` | `:1311` `\| Schema version \| v5.5 \|` | 같은 판 번호 뒤처짐 | SK-03 |
| `docs/index.html` | `:239` `'Sprint Contract 스키마 v5.5'` | 페이지 다시 만들기에 딸려 오지 않는 목차 제목(cs notes) | SK-03 |
| `harness/references/contract-schema.md` | `:678` 규칙 · `:686-692` `dirty_except_status` — `:689-690` awk 가 `status:` 로 시작하는 줄을 본문까지 뺀다 | 본문 `status:` 변경을 못 센다(알려진 답 k6=0 · k7=0, 맞는 값 1 · 2) | SC-05 |
| `harness/skills/sprint-contract/SKILL.md` | `:471-480` 조건 패턴 표 「5 종 (v5.5)」 · `:846-859` 피드백 초안 `project_hash` 글과 bash 조각 | 표에 v5.7 새 패턴 셋이 없다(cs notes). 조각이 `CONTRACT_ROOT` 를 그대로 해시해 워크트리에서 `save-feedback.sh` 재계산값과 늘 다르다(k2 notes — 이 W 에서 `70da29df` 대 `1a3bcba6`) | SK-02 · SC-06 · SK-09 |
| `harness/scripts/save-feedback.sh` | `:149-162` `identity_root_of` · `:200-` `hash8` · `:232` `PROJ_HASH` | 워크트리면 본 레포 폴더를 해시한다 — 기준(고치지 않는다) | SC-06 |
| `harness/agents/qa-evaluator.md` | `:1098-1100` 「`CONTRACT_ROOT` 기준으로 다시 계산」 | 워크트리 규칙이 없다 | SK-09 |
| `harness/README.md` | `:472` 추적 규칙 · `:474` 「`kaizen:` prefix」 | harness-kaizen 은 이미 「바꾼 종류 머리 + 서명 줄 `Kaizen-Phase:`」(`harness/skills/harness-kaizen/SKILL.md:206` · `:245`) — gd notes | SK-04 |
| `.claude/skills/meta-kaizen/SKILL.md` · `scripts/detect-docs-drift.py` | `:16` 「Step 11, Step 11.5, Step 11.6, Step 12」 · `:8` 「Step 11.5」 | 단계 이름이 F1 ~ F4 로 바뀌었다(`.claude/skills/kaizen-orchestrator/SKILL.md:581` · `:620` · `:643` · `:715`) — vsb notes | SK-04 |
| `backend-kit` 다섯 · `rust-kit` 셋 · `infra-kit/skills/infra-guide/SKILL.md` | backend `principle-index.md:1-8` 등 · rust `rust-init/SKILL.md:331` · infra-guide `:27` · `:31` · 짝 `infra-kit/skills/infra-guide/references/principle-index.md:5` | 설치본에 `docs/` 가 없어 경로를 못 여는데 raw 주소 안내가 없다(k2 notes). 시작 판 `backend=5/5 rust=3/3 infra=6/1` | SK-05 |
| `backend-kit/skills/backend-system/references/system-principles.md` · `docs/backend/fundamentals/api-design.md` | `:21` 「OpenAPI 3.1 JSON Schema 호환」 · `:80` 「OpenAPI 3.2.1 스펙을 단일 소스로」 · 바깥 대조 `ex/EX-7.md:61` | 최소 지원선 문구(`backend-audit/references/audit-criteria.md:22`)와 반대로 읽힌다(k2 독립 검토 1) | SK-06 |
| `design-kit/skills/design-mockup/SKILL.md` | `:37` Step 0 · `:57` 「앱 코드 존재 → §0 관례 표」 · `:60` Step 1 · `:68-70` 대상 · 되말하기 | 관례 표가 대상을 정하기 전에 「같은 역할」 화면을 고른다(k2 독립 검토 2) | SK-07 |
| `bambu-kit/README.md` · `CLAUDE.md` · `README.md` | bambu `:11` · `:23` 「4종」 · `:21` 절의 표 7 행 · `:39`(research 대상 4 — 맞다) · `CLAUDE.md:263` · `README.md:404` 나무 그림 · `:340-415` 구조 절 | references 는 9 개(`find … -name '*.md'`). `CLAUDE.md:263` 은 시작 판부터 MD060(표 정렬) 두 건이 걸린 줄이다 — 그 줄을 고치면 DG-02 에 걸리므로 같은 표의 구분 줄 `:262` 도 맞춘다. 나무 그림에 `onboarding-kit` · `tone-kit` · `api-kit` · `howto-kit` 이 없다 — vsb notes | SK-08 |
| `.harness/project.yaml` | `:39-41` AP-04 `pattern: "^---\\s*\\n(?![^-]*name:)"` | 앞머리를 닫는 `---` 에도 걸린다(us notes, 교차 진단 실측). 판정은 message 대로 validate-plugin V1 이 권위다 | SC-07 |
| `.github/workflows/ci.yml` · `harness/evals/gate-exit-codes.md` | ci `:77-78` reviewer 사본 단계(첫 작업 `validate`) · 종료 코드 표 `:62-73`(`:69` reviewer 사본 검사) | 새 검사를 들일 자리 | SC-03 |

개선안 — 구현이 넣을 모양. 조건은 동작과 낱말만 재므로 문장은 톤 대조에 맞춰 다듬어도 된다. 봉인 전 흉내 구현은 세션 스크래치 `cx/mock.py` 다(양성 · 음성 대조에 썼다).

```text
[A] check-api-kit-docs.py — 외부 판정식: 대소문자 무시, 따옴표 뒤 빈칸(공백 · 탭 · 줄바꿈) 허용, `<link href>` 값이
    상대 경로(`../` · `./` · `/한 글자` · 이름으로 시작)면 뺀다. 스킴(`https:` · `HTTPS:` · `data:` …) · `//` · `\\` 로 시작하면 외부.
    `url(` 쪽은 지금 뜻 그대로(대소문자만 무시)
[B] 새 검사 scripts/check-cause-table-copies.py — 원문 덩어리: sprint Step 3 의 `| 공용 작업 폴더 |` 줄부터 `- **미확정**` 줄까지.
    사본 둘에 끊김 없이 있으면 OK. 줄 앞 공백 · `>` · 끝 공백 · 빈 줄은 reviewer 사본 검사와 같은 규칙으로 무시(plugin_utils 로 옮긴 함수 재사용)
    출력: 파일마다 `OK <경로>` · `MISMATCH <경로>` · `UNREADABLE <경로> …`, 원문 덩어리가 없으면 `CANON_MISSING <경로>`, 끝에 요약 한 줄
    종료 코드: 0 둘 다 같다 · 1 다른 사본 · 2 원문이나 사본을 못 읽었다(1 과 함께면 2) — gate-exit-codes.md 에 한 줄
[C] 원문 쪽 안내 — sprint Step 3 의 두 경우 뒤에 「사본이 flutter-preflight · react-preflight 에 있고 CI 가 scripts/check-cause-table-copies.py 로 대조한다」
[D] dirty_except_status — 계약 안 차이는 첫 앞머리 블록의 `status:` 줄만 빼고 센다. 본문의 `status:` 줄은 센다. HEAD 에 없는 계약은 안 차이 0
[E] sprint-contract Step 9 해시 조각 — 워크트리면 공통 git 폴더의 부모(본 레포 폴더)를 해시한다. save-feedback.sh identity_root_of 와 같은 규칙
[F] project.yaml AP-04 — `pattern:` 대신 `command: "python3 scripts/validate-plugin.py --check=frontmatter"` (AP-03 과 같은 꼴), message 그대로
```

## 범위 경계

항목별 처리 — 입력은 Codex 결함 둘과 열두 notes 의 「남은 것」 절(cs 는 「명시적 미완」 · k1 은 「넘긴 것」 · gd 는 「뒤따를 일」 까지 따라 읽음)이다. 「처리됨」 은 끝 판 `82ec540` 에서 확인한 근거를 적었다.

| 항목 (출처) | 처리 | 근거 · 조건 |
| --- | --- | --- |
| Codex 1 외부 CSS 판정 (codex-review-1 · vsa) | 계약에 넣음 | SC-01. `<LINK` · `<SCRIPT` 대문자도 같이 |
| Codex 2 preflight 판정 표 사본 (codex-review-1 · k1 UD-3) | 계약에 넣음 | SK-01 · SC-02 · SC-03 · ER-01 |
| flutter-audit 사본을 CI 가 안 지킴 (k1 KF-2) | 계약에 넣음 | SC-04 — 목록에 넣으면 지금 사본이 원문과 달라(둘째 「3.」) 사본도 고친다 |
| `dirty_except_status` 가 본문 `status:` 까지 뺌 (cs) | 계약에 넣음 | SC-05 |
| 판 번호 자리 여덟 (cs) | 계약에 넣음 — 다섯 | SK-03: qa 가이드 `:12` · `:1984` · `:2063`, 설계 가이드 `:1311`, `docs/index.html:239`. `:15` · `:22` · `:2054` 셋은 2026-09-24 갱신 기록이라 그날 값 v5.5 를 그대로 둔다 |
| 판 번호 문서 사이트 쪽 여섯 (cs) | 이 묶음 밖 | `docs/harness/*.html` 페이지 다시 만들기 — 부모가 다음 차례에 한다 |
| 조건 패턴 표 v5.5 다섯 종 (cs 명시적 미완) | 계약에 넣음 | SK-02 |
| 평가 가이드 「①~④ 의 짝은 다음 사이클로」 (cs · gd CS-3) | 계약에 넣음 | SK-03 `cs3` |
| harness README 추적 규칙 `kaizen:` (gd) | 계약에 넣음 | SK-04 |
| 옛 단계 이름 Step 11 · 11.5 두 곳 (vsb) | 계약에 넣음 | SK-04. `scripts/append-audit-log.py:44` 의 「Step 11.5 added」 는 지난 감사 기록 값이라 둔다 |
| 설치본 `docs/` 경로 raw 안내 — backend · rust · infra-guide (k2) | 계약에 넣음 | SK-05. 같은 뿌리가 다른 킷에도 있다(아래 줄) |
| 같은 raw 안내가 api · design · flutter · howto · onboarding · planning · react · reflect 에도 없음 (이번에 찾음) | 이 묶음 밖 | 파일 69 개이고 그 가운데 사용자 프로젝트의 `docs/` 를 뜻하는 경로가 섞여 있어 하나씩 가려야 한다. k2 notes 가 짚은 범위만 고친다 — notes 에 넘김 |
| OpenAPI 최소 지원선 문구 (k2 독립 검토 1) | 계약에 넣음 | SK-06. `docs/backend/research-log.md` 는 날짜 기록이라 두고, 문서 페이지는 부모 몫 |
| design-mockup Step 0 이 대상 전에 관례 표 (k2 독립 검토 2) | 계약에 넣음 | SK-07 — 관례 표 줄만 Step 1 뒤로 미룬다 |
| bambu references 4종 (vsb) · 루트 README 나무 그림 (vsb) | 계약에 넣음 | SK-08. `.claude/skills/bambu-research/SKILL.md:5` · `bambu-kit/README.md:39` 의 「4종」 은 research 가 고치는 대상 넷(`.claude/skills/bambu-research/SKILL.md:33-36` 표)이라 맞는 말 — 그대로 둔다 |
| AP-04 정규식이 닫는 `---` 에 걸림 (us) | 계약에 넣음 | SC-07 |
| 피드백 `project_hash` 재계산 경고 (k2) | 계약에 넣음 | SC-06 · SK-09 — 스크립트가 아니라 설명과 조각이 뒤처졌다 |
| 검사기 단추 id `theme-btn` 만 봄 (dca) | 이 묶음 밖 | 고치면 `docs/design-kit/visual-styles.html` 단추가 63x33 이라 CI 가 빨개진다(흉내 판 실측, `color-palette` 87x48 · `korean-technical-writing` 80x44 는 통과). 페이지 손질이 같이 있어야 해 문서 페이지 차례로 넘긴다 |
| `check-stale-values` 가 오케스트레이터 참고 폴더를 안 봄 (dcb) | 처리됨 | `scripts/check-stale-values.py:56` 에 `.claude/skills/kaizen-orchestrator/references` 가 있다(vsa VS-27) |
| 매핑 표 `process (공유)` 행 부딪힘 (dcb) | 처리됨 | `.claude/skills/docs-site/SKILL.md:68` 에 원본 둘, `detect-docs-drift.py --check-table` 어긋남 0 |
| docs-site 스킬 「line-height 1.2~1.6배」 (k2) · KD-2 · VS-18 (dca) | 처리됨 | `.claude/skills/docs-site/SKILL.md:110` 이 「행간 1.7 은 공통 파일」, `design-audit/references/audit-criteria.md:10` 이 문자 체계별 범위, 오케스트레이터에 `standalone` 0 줄 |
| KD-3 다섯 자리가 화면 규약 숫자 재정의 (gd · k2) | 처리됨 | design-kit 에 `2 개 이상` · `3 회` 0 줄, `§8.9` 인용 다섯 파일 |
| reflect-digest 드리프트 [NEW] (vsa) | 처리됨 | 페이지 `docs/reflect-kit/reflect-digest.html` 이 생겨 이제 다시 맞출 쪽으로 나온다 — 다시 만들기는 부모 몫 |
| DG-05 가 평가자 `status:` 편집으로 깨짐 (pd · dca DG-05) | 처리됨 | 규칙과 도우미 `dirty_except_status` 가 v5.7 에 들어갔다(`contract-schema.md:678-692`). 도우미 결함은 SC-05 가 고친다 |
| design-mockup Step 2 가 폐기 칸 경로를 따라 읽기 (pd) | 처리됨 | pd2 가 넣었다(`design-mockup/SKILL.md:57`) |
| AR-02 `exact` · `old_left` 칸 나누기 제안 (dca QA 3 회차) | 이 묶음 밖 | 한 계약의 도우미 짜임 제안이라 규칙 문장이 아니다 — 다음 계약을 쓸 때의 관례. contract-kaizen 몫 |
| 원래 있던 편집기 경고 (cs · VS-26) | 이 묶음 밖 | 기존 마크다운 경고 정리는 부모가 다음 차례에 한다 |
| 문서 사이트 페이지 다시 만들기 (cs · gd · hs · k1 · pd · pd2 · vsa · vsb · dcb 의 KT-1 · KRf-1) | 이 묶음 밖 | 부모가 다음 차례에 한다. 이 계약이 원본을 고친 쪽(가이드 둘 · design-mockup · api-design · 스키마)도 그때 다시 맞춘다 |
| SK-11 · SK-13 머리 모양 되돌릴지 (k1) · KD-4 design:P2 (k2) · 폐기 칸 이름 남길지 (pd · pd2) · 핸드오프 틀 모델 이름 (us) | 이 묶음 밖 | 사용자 판단 몫으로 남은 항목 |
| `docs/flutter/research-log.md:20` 2.16 문장 (k1 KF-4) | 이 묶음 밖 | 2026-09-24 조사 기록이라 그날 문장을 둔다. 규칙 본문은 이미 2.7.0 기준(`flutter-build/SKILL.md:20`) |
| `spawn-kaizen-phase.sh:71` 최댓값 17 (vsa) | 이 묶음 밖 | 아래 `case` 표가 Phase 마다 손으로 적혀 있어 상한만 뽑아도 새 킷 Phase 는 `case` 에 없다. 표 전체를 바꾸는 개편이라 최소 변경 밖 |
| `run-evals.py` `ALL_KITS` · `sync-evals.py` `TARGET_KITS` 손 목록 (vsa) | 이 묶음 밖 | 「evals 가 있는 킷」 목록이라 마켓 목록과 뜻이 다르다. 결함이 아니라 설계 개편 |
| 두 번째 검색 줄 머리 조건 넓히기 (pd2) · 다른 폐기 표기 (pd) | 이 묶음 밖 | 넓히면 규칙 인용 줄을 폐기 결정으로 잘못 잡는 쪽이 커진다(pd2 ER-01 과 같은 모양) — 판단이 먼저다 |
| DG-05 를 추적 안 된 도구 없이 재기 (pd · pd2) | 이 묶음 밖 | `ci-local.sh` 를 레포에 들일지는 도구 관리 결정이다 |
| 병렬 세션 훅 · `bash -c` 커밋 · `us-test.sh` 커밋 뒤 경우 (us) | 이 묶음 밖 | 레포 밖 `~/.claude` 훅 |
| 킷 판 올림 · 릴리스 (cs · gd · hs · pd2 · vsa) | 이 묶음 밖 | 릴리스 단계 몫 |
| hs 1 · 2 · 4 · 5, k2 근거 파일 위치, cs AR-06 · dca A-01 · vsa A-01 개정 동의 | 처리됨 | 각 notes 가 「남은 일 없음」 또는 정보로 적었다 |

기능 조건 수는 21 이다(Step 6.2 둘째 명령). 복잡 기준 20 을 하나 넘지만 나누지 않았다 — 항목 대부분이 한두 줄 문장 고침이고, 나누면 `harness/docs/guides/qa-evaluation-guide.md` · `harness/skills/sprint-contract/SKILL.md` 를 두 계약이 같이 고쳐 범위 조건이 서로를 잡는다. 나누지 않는 판단은 사용자 위임(배경의 세 시각) 안에서 내렸다 — 조건을 느슨하게 하는 판단이 아니라 따로 묻지 않는다(교차 진단 1).

교차 진단 반영(봉인 전):

- 교차 진단 2 — DG-05 가 추적 안 된 도구 `ci-local.sh` 에 기대는 점은 notes 에 「도구를 QA 끝까지 그 자리에 두고 지문을 바꾸지 않는다, 관리 책임은 부모 세션」 한 줄로 남긴다
- 교차 진단 3 — SK-07 은 관례 표 줄 하나를 제자리에서 고쳐 쓰는 변경만 허용한다(`numstat=1/1`). 구현은 그 한 줄만 바꾼다
- 교차 진단 4 — SC-01 사례에 `url(` 쪽 둘(U1 대문자 외부 주소 1 · U2 상대 주소 0)을 더해 18 사례로 늘렸다. 시작 판은 U1 을 놓쳐 `wrong=8` 이다(봉인 전 실측)

다른 세션의 올리지 않은 가지와 부딪힘: `main` 에 없는 가지 다섯(`feat/bambu-kit-orca-h2s-feedback` · `feat/bambu-kit-wall-gen-shape` · `feat/scenario-*` 셋)의 바뀐 파일과 아래 범위 목록의 교집합은 0 이다(봉인 전 `git diff --name-only <갈림점> <가지>` 로 확인).

```text
# sprint-scope
scripts/check-api-kit-docs.py
scripts/check-cause-table-copies.py
scripts/check-reviewer-protocol-copies.py
scripts/plugin_utils.py
scripts/detect-docs-drift.py
.github/workflows/ci.yml
flutter-toolkit/skills/flutter-preflight/SKILL.md
flutter-toolkit/skills/flutter-audit/SKILL.md
react-kit/skills/react-preflight/SKILL.md
harness/skills/sprint/SKILL.md
harness/skills/sprint-contract/SKILL.md
harness/references/contract-schema.md
harness/agents/qa-evaluator.md
harness/docs/guides/qa-evaluation-guide.md
harness/docs/guides/contract-design-guide.md
harness/README.md
harness/evals/gate-exit-codes.md
backend-kit/skills/backend-audit/references/audit-criteria.md
backend-kit/skills/backend-guide/SKILL.md
backend-kit/skills/backend-guide/references/principle-index.md
backend-kit/skills/backend-system/SKILL.md
backend-kit/skills/backend-system/references/system-principles.md
rust-kit/skills/rust-audit/references/audit-criteria.md
rust-kit/skills/rust-init/SKILL.md
rust-kit/skills/rust-model/SKILL.md
infra-kit/skills/infra-guide/SKILL.md
design-kit/skills/design-mockup/SKILL.md
bambu-kit/README.md
docs/backend/fundamentals/api-design.md
docs/index.html
.claude/skills/meta-kaizen/SKILL.md
CLAUDE.md
README.md
```

`.harness/` 아래(이 계약 · 개정 · 피드백 · `project.yaml` · notes)는 범위 목록에 적지 않아도 늘 허용된다. `project.yaml` 은 SC-07 이 재고, notes 경로는 AR-02 가 잰다.

커버리지 해소 — Step 6.5 (4) 검출기가 낸 `UNCOVERED` 의 처리:

- 커버리지 해소: AR-01 — 기대 집합은 위 범위 목록 블록을 도우미 `scope` 가 그대로 읽는다(목록을 두 번 적지 않는다)
- 커버리지 해소: SK-01 · SK-03 · SK-04 · SK-08 · AR-02 — 측정 줄은 `m <조건 ID>` 한 줄이고, 산문의 경로는 도우미가 같은 글자로 담는다(`SPR` · `FPF` · `RPF` · `QAG` · `CDG` · `SCH` · `NOTES` 변수와 각 칸의 경로 글자 — `docs/index.html` · `harness/README.md` · `.claude/skills/meta-kaizen/SKILL.md` · `scripts/detect-docs-drift.py` · `bambu-kit/README.md` · `CLAUDE.md` · `README.md` · `.claude/skills/bambu-research/SKILL.md` · `.claude-plugin/marketplace.json`). `chore/ak2-cx` 는 경로가 아니라 가지 이름이다. AR-02 의 `visual-styles.html` · `check-api-kit-docs.py` 는 notes 에서 세는 낱말이다
- 커버리지 해소: SC-01 — 산문의 `href=…` · `url(…)` 조각은 경로가 아니라 사례 표이고, 도우미 `cases_py` 가 18 사례를 글자 그대로 담는다. `research-log.md` 는 마지막 쪽을 고를 때 빼는 이름이다(도우미 `find … ! -name research-log.md`)
- 오라클 해소: DG-05 — 검출기가 산문 확인으로 읽었지만 CI 단계를 실제로 돌려 종료 코드로 판정한다
- 커버리지 해소: SK-05 — 대상 아홉 파일은 도우미가 킷 폴더에서 `docs/<킷>/` 을 적은 파일로 다시 모은다(`README.md` · `evals/` 제외). 시작 판 모은 결과 backend 다섯 · rust 셋 · infra 여섯이 GAP 표와 같다

## 회귀 게이트 — 측정 도우미

평가 때 이 블록을 떼어 bash 에서 불러 쓴다: `python3 harness/scripts/extract-helpers.py --sealed <계약> <폴더>` 로 봉인 판 도우미를 뗀 뒤
`bash -c 'source <폴더>/cx-measure.sh || exit 2; m <조건 ID>'`. `TMPDIR` 은 평가자 임시 폴더로 준다. 도우미는 끝점을 `git archive` 로 풀어 재므로
작업 폴더의 미커밋 변경을 보지 않는다. 변이를 넣는 칸은 풀어 둔 트리 안에서만 고치고 git 판으로 되돌린다 — 작업 폴더와 작업 폴더 밖 입력은 지우지 마라.
시작점 `BASE` 는 `82ec540` 이다 — 통합 가지와의 갈림점을 쓰면 부모가 이 가지를 합친 뒤 갈림점이 끝점과 같아져 모든 차이가 사라진다.
`MDL` 이 가리키는 markdownlint 설치본이 없으면 `mdl_ready` 가 그 자리에 설치한다(npm).

```bash
# cx-measure.sh — 계약 after-0926-codex-and-leftover-fixes 측정 도우미. bash 에서 source 한 뒤 `m <조건 ID>`
# zsh 에서 source 하지 마라 — 도우미 안에서 zsh 를 따로 부르는 칸(SC-05)이 있다.
# 잴 트리 E — 기본은 가지 끝(TIP)을 git archive 로 푼 임시 폴더. 시작 판을 재려면 E_REF=BASE. 다른 사본을 재려면 W=<사본>.
# 변이를 넣는 칸은 E 안 파일을 고쳐 돌린 뒤 git 판으로 되돌린다(put_back). 작업 폴더 W 는 건드리지 않는다.
W=${W:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-cx}
BR=${BR:-chore/ak2-cx}
BASE=${BASE:-82ec540}
git -C "$W" merge-base --is-ancestor "$BASE" "$BR" 2>/dev/null || { echo "UNRESOLVED BASE $BASE 가 $BR 의 조상이 아니다"; return 2 2>/dev/null || exit 2; }
TIP=$(git -C "$W" rev-parse --verify -q "$BR") || { echo "UNRESOLVED TIP $BR"; return 2 2>/dev/null || exit 2; }
T=$(mktemp -d "${TMPDIR:-/tmp}/cx.XXXXXX") || { echo "STOP mktemp"; return 2 2>/dev/null || exit 2; }
snap() { mkdir -p "$2" && git -C "$W" archive "$1" | tar -x -C "$2"; }
case "${E_REF:-TIP}" in
  BASE) REF=$BASE; E=$T/base ;;
  *)    REF=$TIP;  E=$T/tip ;;
esac
snap "$REF" "$E" || { echo "STOP archive $REF"; return 2 2>/dev/null || exit 2; }
CF=.harness/sprint-contract-after-0926-codex-and-leftover-fixes.md
NOTES=.harness/.meta/after-kaizen-0926b/cx-notes.md
CHK=scripts/check-cause-table-copies.py
SPR=harness/skills/sprint/SKILL.md
FPF=flutter-toolkit/skills/flutter-preflight/SKILL.md
RPF=react-kit/skills/react-preflight/SKILL.md
FAU=flutter-toolkit/skills/flutter-audit/SKILL.md
SCH=harness/references/contract-schema.md
SCS=harness/skills/sprint-contract/SKILL.md
QAG=harness/docs/guides/qa-evaluation-guide.md
CDG=harness/docs/guides/contract-design-guide.md
QAE=harness/agents/qa-evaluator.md
PY() { PYTHONDONTWRITEBYTECODE=1 python3 "$@"; }
put_back() { for f in "$@"; do chmod u+rw "$E/$f" 2>/dev/null; git -C "$W" show "$REF:$f" > "$E/$f" 2>/dev/null || rm -f "$E/$f"; done; }
n() { grep -cF -- "$1" || true; }
sec() { awk -v s="$1" -v e="$2" 'index($0,s)==1{f=1;print;next} f&&index($0,e)==1{exit} f' "$3"; }
mdsec() { awk -v s="$1" 'index($0,s)==1{f=1;print;next} f&&/^## /{exit} f' "$2"; }
fmv() { awk -v k="^${1}:[[:space:]]*" 'NR==1&&/^---[[:space:]]*$/{f=1;next} f&&/^---[[:space:]]*$/{exit} f&&$0~k{sub(k,"");print;exit}' "$2" | sed -e 's/[[:space:]]*$//' -e "s/^['\"]//" -e "s/['\"]\$//"; }
h16() { shasum -a 256 | cut -c1-16; }
digest() { grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' | sed -E 's/^- \[[ x]\]/- [ ]/' | h16; }
mdigest() { awk '/^- \[[ x]\] [A-Z][A-Z]+-[0-9][0-9]/{inb=1;match($0,/[A-Z][A-Z]+-[0-9][0-9]/);print substr($0,RSTART,RLENGTH);next} inb&&/^[ \t]+[^ \t]/{l=$0;sub(/[ \t]+$/,"",l);print l;next} inb&&/^[ \t]*$/{next} {inb=0}' | h16; }
scope() { awk '/^## /{s=($0 ~ /^## 범위 경계/)} s&&prev=="```text"&&$0=="# sprint-scope"{b=1;prev=$0;next} b&&/^```$/{b=0} b{print} {prev=$0}' "$E/$CF" 2>/dev/null; }
inscope() {  # inscope <경로> — 범위 목록 블록 가운데 하나에 들면 1
  scope | awk -v p="$1" 'BEGIN{r=0} { s=$0; if (substr(s,length(s))=="/") { if (index(p,s)==1) r=1 } else if (p==s || index(p,s"/")==1) r=1 } END{print r}'
}
cases_py() { cat > "$T/cases.py" <<'PYEOF'
CASES = [
    ("P1", 1, '<link rel="stylesheet" href="https://x.test/a.css">'),
    ("P2", 1, '<link rel="stylesheet" href="HTTPS://x.test/a.css">'),
    ("P3", 1, '<link rel="stylesheet" href=" https://x.test/a.css">'),
    ("P4", 1, '<LINK REL="stylesheet" HREF="https://x.test/a.css">'),
    ("P5", 1, '<link rel="stylesheet" href="//x.test/a.css">'),
    ("P6", 1, '<link rel=stylesheet href=https://x.test/a.css>'),
    ("P7", 1, '<link rel="stylesheet" href="\thttps://x.test/a.css">'),
    ("P8", 1, "<link rel='stylesheet' href='\n https://x.test/a.css'>"),
    ("P9", 1, '<SCRIPT SRC="https://x.test/a.js"></SCRIPT>'),
    ("P10", 1, '<link rel="stylesheet" href="\\\\x.test/a.css">'),
    ("N1", 0, '<link rel="stylesheet" href="../assets/site.css">'),
    ("N2", 0, '<link rel="stylesheet" href=" ../assets/site.css">'),
    ("N3", 0, '<link rel="stylesheet" href="assets/site.css">'),
    ("N4", 0, '<link rel="stylesheet" href="/assets/site.css">'),
    ("N5", 0, '<a href="https://x.test/">x</a>'),
    ("N6", 0, '<script>const a = 1;</script>'),
    ("U1", 1, '<style>body { background: url(HTTPS://x.test/a.png); }</style>'),
    ("U2", 0, '<style>body { background: url(../assets/a.png); }</style>'),
]
PYEOF
cat > "$T/ext.py" <<'PYEOF'
import runpy, sys
m = runpy.run_path(sys.argv[1])
cases = runpy.run_path(sys.argv[2])["CASES"]
wrong = [name for name, want, text in cases if (1 if m["EXTERNAL"].search(text) else 0) != want]
print("cases=%d wrong=%d%s" % (len(cases), len(wrong), (" " + ",".join(wrong)) if wrong else ""))
PYEOF
}
canon_ok() {  # canon_ok <원문> <사본> — 원문 Step 3 판정 표 ~ CI 두 경우 덩어리가 사본 「실패 원인 가르기」 절에 끊김 없이 있으면 1
  PY - "$1" "$2" <<'PYEOF'
import sys
def lines(p):
    try: return open(p, encoding="utf-8").read().split("\n")
    except OSError: return None
src, cp = lines(sys.argv[1]), lines(sys.argv[2])
if src is None or cp is None: print(0); sys.exit()
blk, on = [], False
for l in src:
    if l.startswith("| 공용 작업 폴더 |"): on = True
    if on: blk.append(l.rstrip())
    if on and l.startswith("- **미확정**"): break
blk = [l for l in blk if l]
sec, on = [], False
for l in cp:
    if l.startswith("## 실패 원인 가르기"): on = True; continue
    if on and l.startswith("## "): break
    if on: sec.append(l.rstrip())
sec = [l for l in sec if l]
ok = bool(blk) and any(sec[i:i+len(blk)] == blk for i in range(len(sec) - len(blk) + 1))
print("%d/%d" % (1 if ok else 0, len(blk)))
PYEOF
}
MDL=${MDL:-/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/mdl}
mdl_ready() {  # markdownlint-cli2 0.23.2 · MD013 끔 — 편집기 확장과 같은 설정. 없으면 MDL 에 설치한다
  [ -x "$MDL/node_modules/.bin/markdownlint-cli2" ] || { mkdir -p "$MDL" && (cd "$MDL" && npm install --no-save --no-audit --no-fund markdownlint-cli2@0.23.2 >/dev/null 2>&1); }
  printf '{ "config": { "MD013": false } }\n' > "$T/cfg.markdownlint-cli2.jsonc"
  [ -x "$MDL/node_modules/.bin/markdownlint-cli2" ]
}
addn() { diff -U0 "$1" "$2" | awk '/^@@/{split($3,a,","); s=substr(a[1],2); c=(a[2]=="")?1:a[2]; for(i=0;i<c;i++) print s+i}'; }
newmd() {  # newmd <옛 파일|빈 파일> <새 파일> — 새 파일에서 더해진 줄에 걸린 경고 수
  ( cd "$(dirname "$2")" && "$MDL/node_modules/.bin/markdownlint-cli2" --config "$T/cfg.markdownlint-cli2.jsonc" "$(basename "$2")" 2>&1 ) \
    | awk -F: '/^[^ ]+:[0-9]+/{print $2+0}' | sort -n > "$T/w.txt"
  addn "$1" "$2" | sort -n > "$T/a.txt"
  comm -12 "$T/w.txt" "$T/a.txt" | grep -c . || true
}
m() {
  case "$1" in
  SC-01) cases_py
    c=$(PY "$T/ext.py" "$E/scripts/check-api-kit-docs.py" "$T/cases.py" 2>&1 | tail -1)
    p=$(cd "$E" && PY scripts/check-api-kit-docs.py | tail -1)
    last=$(cd "$E" && find docs/api -name '*.md' ! -name research-log.md | LC_ALL=C sort | tail -1); last=docs/api-kit/$(basename "$last" .md).html
    printf '<link rel="stylesheet" href="HTTPS://x.test/a.css">\n' >> "$E/$last"
    o=$(cd "$E" && PY scripts/check-api-kit-docs.py); rc=$?; put_back "$last"
    echo "$c pages=[$p] bad_rc=$rc bad_fail=$(printf '%s\n' "$o" | grep -c '^FAIL') bad_last=$(printf '%s\n' "$o" | n "FAIL $last")" ;;
  SC-02) [ -f "$E/$CHK" ] || { echo "script=0"; return; }
    run2() { (cd "$E" && PY "$CHK") > "$T/o.txt" 2>&1; echo $?; }
    s() { printf 'ok_f=%s ok_r=%s mis_f=%s mis_r=%s' "$(n "OK $FPF" <"$T/o.txt")" "$(n "OK $RPF" <"$T/o.txt")" "$(n "MISMATCH $FPF" <"$T/o.txt")" "$(n "MISMATCH $RPF" <"$T/o.txt")"; }
    r0=$(run2); s0=$(s)
    sed 's/\*\*미확정\*\*/**미정**/' "$E/$RPF" > "$T/x" && cat "$T/x" > "$E/$RPF"; r1=$(run2); s1=$(s); put_back "$RPF"
    sed 's/귀속 불명이다 |/귀속 불명 |/' "$E/$SPR" > "$T/x" && cat "$T/x" > "$E/$SPR"; r2=$(run2); s2=$(s); put_back "$SPR"
    echo "clean=rc$r0/$s0 | react_bad=rc$r1/$s1 | canon_bad=rc$r2/$s2" ;;
  SC-03) ci=$(awk '/^  [a-z][a-z-]*:$/{j=$1} /run: python3 scripts\/check-cause-table-copies.py[[:space:]]*$/{print j}' "$E/.github/workflows/ci.yml")
    first=$(awk '/^jobs:/{f=1;next} f&&/^  [a-z][a-z-]*:$/{print $1;exit}' "$E/.github/workflows/ci.yml")
    echo "ci_steps=$(printf '%s' "$ci" | grep -c .) job=[$ci] first_job=[$first] exitdoc=$(n '| `scripts/check-cause-table-copies.py` | 0 · 1 · 2 |' <"$E/harness/evals/gate-exit-codes.md")" ;;
  SC-04) o=$(cd "$E" && PY scripts/check-reviewer-protocol-copies.py 2>&1); rc=$?
    sed 's/\*\*임계값 2 는/3. **임계값 2 는/' "$E/$FAU" > "$T/x"; ap=$(diff "$E/$FAU" "$T/x" | grep -c '^>'); cat "$T/x" > "$E/$FAU"; ob=$(cd "$E" && PY scripts/check-reviewer-protocol-copies.py 2>&1); rcb=$?; put_back "$FAU"
    g=$(awk '/^> \*\*사본 검사:\*\*/{f=1} f{print} f&&!/^>/{exit}' "$E/$QAG")
    echo "rc=$rc fa_ok=$(printf '%s\n' "$o" | n "OK $FAU") sum=[$(printf '%s\n' "$o" | tail -1)] bad_applied=$ap bad_rc=$rcb bad_mis=$(printf '%s\n' "$ob" | n "MISMATCH $FAU") guide_fa=$(printf '%s\n' "$g" | n 'flutter-audit')" ;;
  SC-05) awk '/^dirty_except_status\(\) \{/{f=1} f{print} f&&/^}/{exit}' "$E/$SCH" > "$T/des.sh"
    cat > "$T/des-cases.sh" <<'SHEOF'
. "${1}" || exit 2
R=$(mktemp -d "${TMPDIR:-/tmp}/des.XXXXXX") || exit 2
cd "$R" && git init -q && printf -- '---\nstatus: active\n---\n- [ ] AR-01: x\nstatus: body\n' > c.md && printf 'o\n' > o.txt && git add c.md o.txt && git -c user.name=t -c user.email=t@t commit -qm c
reset() { git checkout -q -- c.md o.txt; rm -f new.txt n.md; }
reset; echo "k1=$(dirty_except_status c.md)"
reset; sed 's/^status: active$/status: done/' c.md > c.tmp && mv c.tmp c.md; echo "k2=$(dirty_except_status c.md)"
reset; sed -e 's/^status: active$/status: done/' -e 's/AR-01: x/AR-01: y/' c.md > c.tmp && mv c.tmp c.md; echo "k3=$(dirty_except_status c.md)"
reset; printf 'p\n' >> o.txt; echo "k4=$(dirty_except_status c.md)"
reset; printf 'n\n' > new.txt; echo "k5=$(dirty_except_status c.md)"
reset; sed 's/^status: active$/status: done/' c.md > c.tmp && mv c.tmp c.md; printf 'status: sneaky\n' >> c.md; echo "k6=$(dirty_except_status c.md)"
reset; sed 's/^status: body$/status: other/' c.md > c.tmp && mv c.tmp c.md; echo "k7=$(dirty_except_status c.md)"
reset; out=$(dirty_except_status no-such.md); rc=$?; echo "k8=rc${rc}/[${out}]"
reset; printf -- '---\nstatus: active\n---\n' > n.md; echo "k9=$(dirty_except_status n.md)"
cd / && rm -rf "$R"
SHEOF
    for sh in bash zsh; do printf '%s: %s\n' "$sh" "$(TMPDIR=$T $sh "$T/des-cases.sh" "$T/des.sh" 2>/dev/null | tr '\n' ' ')"; done ;;
  SC-06) awk '/^### 9\./{s=1} s&&/`project_hash`/{p=1} p&&/```bash/{b=1;next} b&&/```/{exit} b{sub(/^     /,"");print}' "$E/$SCS" > "$T/hash.sh"
    F=$E/harness/scripts/save-feedback.sh
    { awk '/^identity_root_of\(\) \{/{f=1} f{print} f&&/^}/{exit}' "$F"; awk '/^hash8\(\) \{/{f=1} f{print} f&&/^}/{exit}' "$F"; echo 'hash8 "$(identity_root_of "${1}")"; echo'; } > "$T/ident.sh"
    mkdir -p "$T/plain"; P=$(cd "$T/plain" && pwd -P)
    wt=$(cd "$W" && CONTRACT_ROOT=$W bash "$T/hash.sh" 2>/dev/null | tail -1); wi=$(bash "$T/ident.sh" "$W")
    pl=$(cd "$P" && CONTRACT_ROOT=$P bash "$T/hash.sh" 2>/dev/null | tail -1); pi=$(bash "$T/ident.sh" "$P")
    echo "wt=$wt wt_same=$([ -n "$wt" ] && [ "$wt" = "$wi" ] && echo 1 || echo 0) plain_same=$([ -n "$pl" ] && [ "$pl" = "$pi" ] && echo 1 || echo 0) lines=$(grep -c . "$T/hash.sh")" ;;
  SC-07) blk=$(awk '/^  - id: AP-04$/{f=1;print;next} f&&(/^  - id:/||/^[^ ]/||/^$/){exit} f' "$E/.harness/project.yaml")
    cmd=$(printf '%s\n' "$blk" | n 'command: "python3 scripts/validate-plugin.py --check=frontmatter"')
    pat=$(printf '%s\n' "$blk" | n 'pattern:')
    msg=$(printf '%s\n' "$blk" | n 'message: "SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL"')
    (cd "$E" && PY scripts/validate-plugin.py --check=frontmatter >/dev/null 2>&1); rc=$?
    grep -v '^name:' "$E/$RPF" > "$T/x" && cat "$T/x" > "$E/$RPF"; (cd "$E" && PY scripts/validate-plugin.py --check=frontmatter >/dev/null 2>&1); rcb=$?; put_back "$RPF"
    echo "cmd=$cmd pattern=$pat msg=$msg rc=$rc bad_rc=$rcb" ;;
  SK-01) f=$(canon_ok "$E/$SPR" "$E/$FPF"); r=$(canon_ok "$E/$SPR" "$E/$RPF")
    sf=$(grep '^사본 출처:' "$E/$FPF" | grep -F "$CHK" | n 'CI 에서만'); sr=$(grep '^사본 출처:' "$E/$RPF" | grep -F "$CHK" | n 'CI 에서만')
    cn=$(sec '### Step 3:' '### Step 4:' "$E/$SPR" | grep -F "$CHK" | grep -F 'flutter-preflight' | n 'react-preflight')
    echo "flutter=$f react=$r src_note=$sf$sr canon_note=$cn" ;;
  SK-02) h=$(grep '^\*\*조건 패턴' "$E/$SCS")
    rows=$(awk '/^\*\*조건 패턴/{f=1;next} f&&/^\| \*\*/{n++} f&&/^$/&&n{exit} END{print n+0}' "$E/$SCS")
    t=$(awk '/^\*\*조건 패턴/{f=1;next} f&&/^$/&&c{exit} f&&/^\|/{c=1;print}' "$E/$SCS")
    echo "hdr=$(printf '%s' "$h" | grep -c .) hdr_old=$(printf '%s\n' "$h" | n '5 종 (v5.5)') rows=$rows new=$(printf '%s\n' "$t" | n '| **산출물이 검사인 조건** |')$(printf '%s\n' "$t" | n '| **기존 동작 유지 조건** |')$(printf '%s\n' "$t" | n '| **페이지 맞추기 계약** |')" ;;
  SK-03) cur=$(sed -n 's/^현재: \*\*\(v[0-9.]*\)\*\*.*/\1/p' "$E/$SCH")
    ref=$(grep '^> \*\*참조 스키마\*\*:' "$E/$QAG" | n "($cur)")
    lst=$(grep '^- `harness/references/contract-schema.md` — Sprint Contract' "$E/$QAG" | n "Sprint Contract $cur 스키마")
    lnk=$(grep '^- \*\*Schema link\*\*:' "$E/$QAG" | n "contract-schema.md $cur ")
    cdg=$(n "| Schema version | $cur |" <"$E/$CDG")
    idx=$(grep "id: 'contract-schema'" "$E/docs/index.html" | n "스키마 $cur'")
    hist=$(n 'Phase 2 가 넘긴 스키마 v5.5 의 반대편' <"$E/$QAG")$(n '정합 — 스키마 v5.5 의 Diff-Scope' <"$E/$QAG")$(grep '^- \*\*Guide version\*\*: 2026-09-24' "$E/$QAG" | n '스키마 v5.5 정합')
    lim=$(awk '/^\*\*한계\.\*\*/{f=1} f{print} f&&/^$/{exit}' "$E/$QAG")
    echo "cur=$cur ref=$ref list=$lst link=$lnk cdg=$cdg index=$idx hist=$hist old_cs3=$(n '①~④ 의 짝은 다음 사이클' <"$E/$QAG") cs3=$(printf '%s\n' "$lim" | n '§산출물이 검사인 조건')" ;;
  SK-04) tr_=$(awk '/^### 추적 규칙/{f=1;next} f&&/^### /{exit} f' "$E/harness/README.md")
    mk=$(sed -n '16p' "$E/.claude/skills/meta-kaizen/SKILL.md"); dd=$(sed -n '1,15p' "$E/scripts/detect-docs-drift.py")
    echo "readme_old=$(printf '%s\n' "$tr_" | n '`kaizen:` prefix') readme_new=$(printf '%s\n' "$tr_" | n 'Kaizen-Phase:') meta_old=$(printf '%s\n' "$mk" | grep -cE 'Step 11|Step 12' || true) meta_new=$(printf '%s\n' "$mk" | grep -F 'Step F1' | grep -F 'Step F2' | grep -F 'Step F3' | n 'Step F4') drift_old=$(printf '%s\n' "$dd" | n 'Step 11.5') drift_new=$(printf '%s\n' "$dd" | n 'Step F2')" ;;
  SK-05) out=""
    for k in backend rust infra; do tot=0; miss=0
      for f in $(cd "$E" && grep -rlF "docs/$k/" "$k-kit" | grep -v '/README\.md$' | grep -v '/evals/' | LC_ALL=C sort); do
        tot=$((tot+1)); grep -F 'raw.githubusercontent.com/joo6077/claude-plugins/main/' "$E/$f" | grep -qF '못 읽었다고' || miss=$((miss+1)); done
      out="$out $k=$tot/$miss"; done; echo "${out# }" ;;
  SK-06) sp=$(grep '^| API 규격 |' "$E/backend-kit/skills/backend-system/references/system-principles.md")
    ad=$(awk '/^### 5\. OpenAPI/{f=1;next} f&&/^### /{exit} f' "$E/docs/backend/fundamentals/api-design.md")
    b=$(printf '%s\n' "$ad" | grep -v '^>' | grep -v '^$' | head -1)
    echo "sp=$(printf '%s\n' "$sp" | n '3.1 이상')$(printf '%s\n' "$sp" | n '최소 지원선') sp_old=$(printf '%s\n' "$sp" | n 'OpenAPI 3.1 JSON Schema 호환') ad_old=$(printf '%s\n' "$ad" | n 'OpenAPI 3.2.1 스펙을 단일 소스로') ad=$(printf '%s\n' "$b" | n '3.1 이상')$(printf '%s\n' "$b" | n '3.2.1') src=$(printf '%s\n' "$ad" | n '> **출처:** [OpenAPI Specification 최신판 3.2.1](https://spec.openapis.org/oas/latest.html)')" ;;
  SK-07) f=design-kit/skills/design-mockup/SKILL.md; l=$(grep '^- 앱 코드 존재 →' "$E/$f")
    echo "app=$(printf '%s' "$l" | grep -c .) step1=$(printf '%s\n' "$l" | n 'Step 1') numstat=$(git -C "$W" diff --numstat "$BASE" "$REF" -- "$f" | awk '{print $1"/"$2}')" ;;
  SK-08) rb=$E/bambu-kit/README.md
    refs=$(cd "$E/bambu-kit/skills/bambu-print-profile/references" && find . -maxdepth 1 -name '*.md' | sed 's#^\./##' | LC_ALL=C sort)
    tab=$(awk '/^## 리서치 문서/{f=1;next} f&&/^## /{exit} f' "$rb" | grep -o '^| `[^`]*\.md`' | sed 's/^| `//; s/`$//' | LC_ALL=C sort)
    nr=$(printf '%s\n' "$refs" | grep -c .); same=$([ "$refs" = "$tab" ] && echo 1 || echo 0)
    tree=$(awk '/^## 구조/{f=1;next} f&&/^## /{exit} f' "$E/README.md")
    miss=0; for p in $(PY -c 'import json;print(" ".join(x["name"] for x in json.load(open("'"$E"'/.claude-plugin/marketplace.json"))["plugins"]))'); do printf '%s\n' "$tree" | grep -qF "── $p/" || miss=$((miss+1)); done
    echo "refs=$nr r11=$(grep -F '단일 스킬이 references' "$rb" | n "references ${nr}종") r23=$(grep -F '`skills/bambu-print-profile/references/`에' "$rb" | n "${nr}종") r39=$(grep -F '/bambu-research' "$rb" | n 'references 4종 갱신') table_same=$same claude=$(grep -F '/bambu-print-profile' "$E/CLAUDE.md" | n "references ${nr}종") claude_old=$(grep -F '/bambu-print-profile' "$E/CLAUDE.md" | n 'references 4종') tree_bambu=$(printf '%s\n' "$tree" | grep -F 'references/' | n "${nr}종") tree_missing=$miss research=$(n 'references/ 4종 문서를 갱신한다' <"$E/.claude/skills/bambu-research/SKILL.md")" ;;
  SK-09) q=$(awk '/`project_hash` \/ `project_name`: draft 에 적더라도/{f=1} f{print; c++} c==3{exit}' "$E/$QAE")
    s=$(awk '/^### 9\./{g=1} g&&/- `project_hash`:/{f=1} f&&/```bash/{exit} f' "$E/$SCS")
    echo "qa_wt=$(printf '%s\n' "$q" | n '워크트리') skill_wt=$(printf '%s\n' "$s" | n '워크트리') old=$(n '`pwd` 가 아니라 `CONTRACT_ROOT` 를 해시한다' <"$E/$SCS")" ;;
  ER-01) [ -f "$E/$CHK" ] || { echo "script=0"; return; }
    sed 's/\*\*미확정\*\*/**미정**/' "$E/$RPF" > "$T/x" && cat "$T/x" > "$E/$RPF"; chmod 000 "$E/$FPF"
    o=$(cd "$E" && PY "$CHK" 2>&1); rc=$?; put_back "$RPF" "$FPF"
    grep -v '^| 공용 작업 폴더 |' "$E/$SPR" > "$T/x" && cat "$T/x" > "$E/$SPR"
    o2=$(cd "$E" && PY "$CHK" 2>&1); rc2=$?; put_back "$SPR"
    echo "unread=rc$rc/unr_f=$(printf '%s\n' "$o" | n "UNREADABLE $FPF")/mis_r=$(printf '%s\n' "$o" | n "MISMATCH $RPF") canon_gone=rc$rc2/canon_missing=$(printf '%s\n' "$o2" | grep -c '^CANON_MISSING')/ok_lines=$(printf '%s\n' "$o2" | grep -c '^OK ')" ;;
  AR-01) chg=$(git -C "$W" diff --name-only "$BASE" "$REF")
    extra=0; for p in $chg; do case "$p" in .harness/*) continue ;; esac; [ "$(inscope "$p")" = 1 ] || { extra=$((extra+1)); echo "  밖: $p"; }; done
    miss=0; for s in $(scope); do printf '%s\n' "$chg" | grep -qxF "$s" || { miss=$((miss+1)); echo "  안 바뀜: $s"; }; done
    multi=0; for c in $(git -C "$W" rev-list --no-merges "$BASE..$REF"); do k=$(git -C "$W" show --name-only --format= "$c" | awk -F/ 'NF==1{print "(root)";next}{print $1}' | LC_ALL=C sort -u | grep -c .); [ "$k" -gt 1 ] && { multi=$((multi+1)); echo "  섞임: $(git -C "$W" log -1 --format='%h %s' "$c")"; }; done
    echo "scope=$(scope | grep -c .) changed=$(printf '%s' "$chg" | grep -c .) extra=$extra missing=$miss multi_top=$multi" ;;
  AR-02) c=$(git -C "$W" ls-tree -r --name-only "$REF" -- "$NOTES" | grep -c .)
    t=""; for k in '| 항목 |' '계약에 넣음' '처리됨' '이 묶음 밖' 'tone-guide' 'visual-styles.html' 'cs-notes' 'vsb-notes' 'us-notes' 'k2-notes'; do t="$t$( [ -f "$E/$NOTES" ] && n "$k" <"$E/$NOTES" || echo 0) "; done
    echo "committed=$c tokens=[$t]" ;;
  AR-03) s=$(git -C "$W" log --reverse --format=%H --diff-filter=A "$BASE..$REF" -- "$CF" | head -1)
    [ -n "$s" ] || { echo "seal_commit_files=0 seal_before_impl=0 seal_same_as_tip=0 measure_same_as_tip=0 this=SEAL_ABSENT MEASURE_ABSENT"; return; }
    fs=$(git -C "$W" show --name-only --format= "$s" | grep -c .)
    im=$(git -C "$W" rev-list --reverse "$BASE..$REF" -- . ':(exclude).harness' | head -1)
    before=0; [ -n "$im" ] && [ "$im" != "$s" ] && git -C "$W" merge-base --is-ancestor "$s" "$im" && before=1
    a=$(git -C "$W" show "$s:$CF" | digest); b=$(digest <"$E/$CF"); ma=$(git -C "$W" show "$s:$CF" | mdigest); mb=$(mdigest <"$E/$CF")
    rc=$(fmv conditions_digest "$E/$CF"); rm_=$(fmv measurement_digest "$E/$CF")
    st=SEAL_BROKEN; [ "sha256:$b" = "$rc" ] && st=SEAL_OK; mt=MEASURE_BROKEN; [ "sha256:$mb" = "$rm_" ] && mt=MEASURE_OK
    echo "seal_commit_files=$fs seal_before_impl=$before seal_same_as_tip=$([ "$a" = "$b" ] && echo 1 || echo 0) measure_same_as_tip=$([ "$ma" = "$mb" ] && echo 1 || echo 0) this=$st $mt" ;;
  AP-03) (cd "$E" && PY scripts/validate-plugin.py --check=code-fence >"$T/v6.txt" 2>&1); echo "v6_rc=$? fail=$(grep -c 'FAIL' "$T/v6.txt")" ;;
  AP-04) (cd "$E" && PY scripts/validate-plugin.py --check=frontmatter >"$T/v1.txt" 2>&1); echo "v1_rc=$? fail=$(grep -c 'FAIL' "$T/v1.txt")" ;;
  RE-02) echo "normalized=$(cd "$E" && grep -l '^def normalized' scripts/*.py | tr '\n' ' ')contains=$(cd "$E" && grep -l '^def contains_block' scripts/*.py | tr '\n' ' ')chk_import=$([ -f "$E/$CHK" ] && grep -cE '^from plugin_utils import .*normalized' "$E/$CHK" || echo 0)" ;;
  DG-01) echo "release_sh=$(git -C "$W" diff --name-only "$BASE" "$REF" -- scripts/release.sh | grep -c .)" ;;
  DG-03) m DG-01 ;;
  DG-04) echo "entry=$(git -C "$W" diff --name-only --diff-filter=A "$BASE" "$REF" -- . ':(exclude).harness' | grep -vE '^scripts/check-[a-z-]+\.py$' | grep -cE '\.(py|js|ts|sh|dart|rs)$')" ;;
  RE-01) echo "added=[$(git -C "$W" diff --diff-filter=A --name-only "$BASE" "$REF" -- . ':(exclude).harness' | tr '\n' ' ')]" ;;
  DG-02) mdl_ready || { echo "MDL_NOT_READY"; return; }; tot=0; rows=""
    for f in $(git -C "$W" diff --name-only "$BASE" "$REF" -- '*.md' ':(exclude).harness/sprint-*.md'); do
      o=$T/old.md; git -C "$W" show "$BASE:$f" > "$o" 2>/dev/null || : > "$o"
      c=$(newmd "$o" "$E/$f"); tot=$((tot + c)); rows="$rows $f=$c"; done
    echo "md_new=$tot |$rows" ;;
  DG-05X) r=""; for c in "scripts/detect-docs-drift.py --check-table" "$CHK"; do (cd "$E" && PY $c >/dev/null 2>&1); r="$r$? "; done
    (cd "$E" && bash harness/evals/measure/measure-helpers-test.sh >/dev/null 2>&1); echo "drift_table rc / cause_copies rc / measure_helpers rc = $r$?" ;;
  *) echo "모르는 조건 $1"; return 2 ;;
  esac
}
```

## Skill

- [ ] SK-01: flutter-preflight · react-preflight 의 판정 표 사본이 원문과 글자까지 같고(CI 에서만 실패할 때의 두 경우 포함), 원문 쪽에 사본이 있다는 안내가 있다(Codex 결함 2 · 짝 조건) — Given 구현 커밋이 가지 `chore/ak2-cx` 에 들어간 뒤, When `harness/skills/sprint/SKILL.md` 의 `| 공용 작업 폴더 |` 로 시작하는 줄부터 `- **미확정**` 으로 시작하는 줄까지(끝 공백 · 빈 줄을 뺀 원문 덩어리)를 `flutter-toolkit/skills/flutter-preflight/SKILL.md` · `react-kit/skills/react-preflight/SKILL.md` 의 `## 실패 원인 가르기` 절(끝 공백 · 빈 줄을 뺀 줄)과 맞대면, Then 두 사본 모두 그 덩어리가 끊김 없이 들어 있고, 두 사본의 `사본 출처:` 줄에 `scripts/check-cause-table-copies.py` 와 `CI 에서만` 이 있고, 원문 `### Step 3:` 절(다음 `### Step 4:` 앞까지)에 `scripts/check-cause-table-copies.py` · `flutter-preflight` · `react-preflight` 가 모두 든 줄이 1 줄이다 [exact, enumerated]
  측정: `m SK-01` 이 `flutter=1/8 react=1/8 src_note=11 canon_note=1` (시작 판 `flutter=0/8 react=0/8 src_note=00 canon_note=0`, 흉내 판 기대값 그대로). 이 측정은 새 검사 스크립트를 부르지 않고 도우미가 직접 맞댄다 — 너그러운 검사로 통과하지 못하게
  음성 대조: 흉내 판에서 원문 덩어리 끝을 `FORK_BASE` 문단 앞까지로 잡은 첫 흉내 구현(원문 쪽 안내 줄이 덩어리에 섞임)이 `flutter=0/9 react=0/9` 였다 (봉인 전 실측)
- [ ] SK-02: sprint-contract 조건 패턴 표가 v5.7 의 새 패턴 셋을 담는다(cs 명시적 미완) — Given 구현 커밋 뒤, When `harness/skills/sprint-contract/SKILL.md` 에서 `**조건 패턴` 으로 시작하는 줄과 그 뒤 첫 표를 읽으면, Then 그 줄이 1 줄이고 `5 종 (v5.5)` 가 없으며, 표의 `| **` 로 시작하는 행이 8 개이고 `| **산출물이 검사인 조건** |` · `| **기존 동작 유지 조건** |` · `| **페이지 맞추기 계약** |` 행이 각 1 개다 [exact, enumerated]
  측정: `m SK-02` 가 `hdr=1 hdr_old=0 rows=8 new=111` (시작 판 `hdr=1 hdr_old=1 rows=5 new=000`)
- [ ] SK-03: 판 번호 다섯 자리가 스키마 현재 판과 같고, 2026-09-24 갱신 기록 셋은 그날 값 그대로이며, 평가 가이드 「한계」 문단이 짝의 위치를 가리킨다(cs · gd CS-3) — Given 구현 커밋 뒤, When `harness/references/contract-schema.md` 의 `현재: **vX**` 값을 cur 로 두고 읽으면, Then (a) `harness/docs/guides/qa-evaluation-guide.md` 의 `> **참조 스키마**:` 줄에 `(cur)` · 참조 목록에서 `harness/references/contract-schema.md` 경로로 시작하는 `Sprint Contract` 줄에 `Sprint Contract cur 스키마` · `- **Schema link**:` 줄에 `contract-schema.md cur` 와 그 뒤 빈칸이 있다 (b) `harness/docs/guides/contract-design-guide.md` 에 `| Schema version | cur |` 가 1 줄이다 (c) `docs/index.html` 의 `id: 'contract-schema'` 줄에 `스키마 cur'` 가 있다 (d) `Phase 2 가 넘긴 스키마 v5.5 의 반대편` · `정합 — 스키마 v5.5 의 Diff-Scope` · `- **Guide version**: 2026-09-24` 줄의 `스키마 v5.5 정합` 이 각 1 개 그대로다 (e) `①~④ 의 짝은 다음 사이클` 이 0 이고 `**한계.**` 문단에 `§산출물이 검사인 조건` 이 있다 [exact, enumerated]
  측정: `m SK-03` 이 `cur=v5.7 ref=1 list=1 link=1 cdg=1 index=1 hist=111 old_cs3=0 cs3=1` (시작 판 `cur=v5.7 ref=0 list=0 link=0 cdg=0 index=0 hist=111 old_cs3=1 cs3=0`)
  양성 대조: 시작 판이 `ref=0 … old_cs3=1` — 뒤처진 값을 실제로 잡는다 (봉인 전 실측)
- [ ] SK-04: 옛 규칙 이름 세 자리를 지금 이름으로 바꾼다(gd · vsb) — Given 구현 커밋 뒤, When 읽으면, Then (a) `harness/README.md` 의 `### 추적 규칙` 절에 `kaizen:` 머리 규칙 글(도우미 낱말 「`kaizen:` prefix」)이 0 이고 `Kaizen-Phase:` 가 1 줄 이상이다 (b) `.claude/skills/meta-kaizen/SKILL.md` 16 번째 줄에 `Step 11` · `Step 12` 가 없고 `Step F1` · `Step F2` · `Step F3` · `Step F4` 가 모두 있다 (c) `scripts/detect-docs-drift.py` 첫 15 줄에 `Step 11.5` 가 없고 `Step F2` 가 1 줄이다 [exact, enumerated]
  측정: `m SK-04` 가 `readme_old=0 readme_new=1 meta_old=0 meta_new=1 drift_old=0 drift_new=1` (시작 판 `readme_old=1 readme_new=0 meta_old=1 meta_new=0 drift_old=1 drift_new=0`)
- [ ] SK-05: 설치본에서 `docs/` 경로를 못 열 때의 raw 주소 안내가 backend-kit · rust-kit · infra-kit 에서 `docs/<킷>/` 경로를 적은 파일 전부에 있다(k2) — Given 구현 커밋 뒤, When 세 킷 폴더에서 `docs/backend/` · `docs/rust/` · `docs/infra/` 를 적은 파일(`README.md` · `evals/` 아래 제외)을 모으면, Then 그 파일마다 `raw.githubusercontent.com/joo6077/claude-plugins/main/` 과 `못 읽었다고` 가 함께 든 줄이 있다 — 대상은 backend 다섯(`backend-kit/skills/backend-audit/references/audit-criteria.md` · `backend-kit/skills/backend-guide/SKILL.md` · `backend-kit/skills/backend-guide/references/principle-index.md` · `backend-kit/skills/backend-system/SKILL.md` · `backend-kit/skills/backend-system/references/system-principles.md`) · rust 셋(`rust-kit/skills/rust-audit/references/audit-criteria.md` · `rust-kit/skills/rust-init/SKILL.md` · `rust-kit/skills/rust-model/SKILL.md`) · infra 여섯(이미 있는 다섯 + `infra-kit/skills/infra-guide/SKILL.md`) [exact, enumerated]
  측정: `m SK-05` 가 `backend=5/0 rust=3/0 infra=6/0` (모은 파일 수 / 안내 없는 수. 시작 판 `backend=5/5 rust=3/3 infra=6/1`)
  양성 대조: 시작 판 안내 없는 수 9 — 측정이 빠진 파일을 실제로 센다 (봉인 전 실측)
- [ ] SK-06: OpenAPI 판 번호 글이 「3.1 이상 — 최소 지원선」 으로 읽힌다(k2 독립 검토 1 · `ex/EX-7.md`) — Given 구현 커밋 뒤, When 읽으면, Then (a) `backend-kit/skills/backend-system/references/system-principles.md` 의 `| API 규격 |` 행에 `3.1 이상` 과 `최소 지원선` 이 있고 `OpenAPI 3.1 JSON Schema 호환` 이 0 이다 (b) `docs/backend/fundamentals/api-design.md` 의 `### 5. OpenAPI` 절에 `OpenAPI 3.2.1 스펙을 단일 소스로` 가 0 이고, 인용(`>`) 밖 첫 글 줄에 `3.1 이상` 과 `3.2.1` 이 있으며, 출처 줄 `> **출처:** [OpenAPI Specification 최신판 3.2.1](https://spec.openapis.org/oas/latest.html)` 이 그대로다 [exact]
  측정: `m SK-06` 이 `sp=11 sp_old=0 ad_old=0 ad=11 src=1` (시작 판 `sp=00 sp_old=1 ad_old=1 ad=01 src=1`)
- [ ] SK-07: design-mockup 의 관례 표가 대상 화면을 정한 뒤에 만들어진다(k2 독립 검토 2) — Given 구현 커밋 뒤, When `design-kit/skills/design-mockup/SKILL.md` 를 읽으면, Then `- 앱 코드 존재 →` 로 시작하는 줄이 1 줄이고 그 줄에 `Step 1` 이 있으며, 이 파일의 시작점 대비 차이가 더한 줄 1 · 지운 줄 1 이다 [exact]
  측정: `m SK-07` 이 `app=1 step1=1 numstat=1/1` (시작 판 `app=1 step1=0 numstat=`)
- [ ] SK-08: bambu references 수와 루트 README 나무 그림이 실제와 같다(vsb) — Given 구현 커밋 뒤, When `bambu-kit/skills/bambu-print-profile/references/` 의 `.md` 수를 N 으로 두면(시작 판 9), Then (a) `bambu-kit/README.md` 의 `단일 스킬이 references` 줄에 `references N종` · `skills/bambu-print-profile/references/` 뒤에 「에」 가 붙은 줄에 `N종` 이 있고, `/bambu-research` 줄의 `references 4종 갱신` 은 그대로다(research 가 고치는 대상 넷) (b) 같은 파일 `## 리서치 문서` 절 표의 파일 이름 집합이 references 의 `.md` 집합과 같다 (c) `CLAUDE.md` 의 `/bambu-print-profile` 줄에 `references N종` 이 있고 `references 4종` 이 없다 (d) `README.md` 의 `## 구조` 절에서 `references/` 줄에 `N종` 이 있고, `.claude-plugin/marketplace.json` 의 플러그인 이름마다 `── <이름>/` 줄이 있다 (e) `.claude/skills/bambu-research/SKILL.md` 의 `references/ 4종 문서를 갱신한다` 는 그대로다 [exact, enumerated]
  측정: `m SK-08` 이 `refs=9 r11=1 r23=1 r39=1 table_same=1 claude=1 claude_old=0 tree_bambu=1 tree_missing=0 research=1` (시작 판 `refs=9 r11=0 r23=0 r39=1 table_same=0 claude=0 claude_old=1 tree_bambu=0 tree_missing=4 research=1`)
- [ ] SK-09: 피드백 초안 `project_hash` 설명이 워크트리 규칙을 적는다(SC-06 의 받는 쪽 · k2) — Given 구현 커밋 뒤, When 읽으면, Then `harness/agents/qa-evaluator.md` 의 `` `project_hash` / `project_name`: draft 에 적더라도 `` 줄부터 세 줄에 `워크트리` 가 있고, `harness/skills/sprint-contract/SKILL.md` `### 9.` 절의 `project_hash` 항목(다음 bash 블록 앞까지)에 `워크트리` 가 1 줄 이상이며, 옛 문장(`pwd` 가 아니라 `CONTRACT_ROOT` 를 해시한다 — 도우미 `old`)이 0 이다 [exact]
  측정: `m SK-09` 가 `qa_wt=1` · `skill_wt` 1 이상 · `old=0` (시작 판 `qa_wt=0 skill_wt=0 old=1`, 흉내 판 `qa_wt=1 skill_wt=2 old=0`)

## Script

- [ ] SC-01: api-kit 문서 검사가 외부 스타일 · 스크립트를 대소문자와 따옴표 뒤 빈칸에 상관없이 잡고, 상대 경로만 뺀다(Codex 결함 1) — Given 구현 커밋 뒤, When 끝 판 `scripts/check-api-kit-docs.py` 의 외부 판정식에 아래 18 사례를 넣으면, Then 틀린 사례가 0 이고, 끝 판 트리에서 검사를 돌리면 요약이 `12/12 PASS` 이며, 검사 순서의 마지막 쪽(`docs/api` 의 `research-log.md` 밖 `.md` 를 이름순으로 둔 마지막의 `.html`)에만 `<link rel="stylesheet" href="HTTPS://x.test/a.css">` 한 줄을 더한 사본에서는 종료 코드 1 · `FAIL` 줄 1 개 · 그 쪽 이름의 `FAIL` 줄 1 개다 [exact, enumerated]
  사례(1 = 외부로 잡아야 함, 0 = 잡으면 안 됨 — 도우미 `cases_py` 가 글자 그대로 담는다): P1 1 `href="https://…"` · P2 1 `href="HTTPS://…"` · P3 1 `href=" https://…"` · P4 1 `<LINK REL=… HREF="https://…">` · P5 1 `href="//x.test/…"` · P6 1 따옴표 없는 `href=https://…` · P7 1 `href="<탭>https://…"` · P8 1 `href='<줄바꿈> https://…'` · P9 1 `<SCRIPT SRC="https://…">` · P10 1 `href="\\x.test/…"` · N1 0 `href="../assets/site.css"` · N2 0 `href=" ../assets/site.css"` · N3 0 `href="assets/site.css"` · N4 0 `href="/assets/site.css"` · N5 0 `<a href="https://…">` · N6 0 `<script>` 안 글 · U1 1 `url(HTTPS://…)` · U2 0 `url(../assets/a.png)`
  측정: `m SC-01` 이 `cases=18 wrong=0 pages=[12/12 PASS] bad_rc=1 bad_fail=1 bad_last=1` (시작 판 `cases=18 wrong=8 P2,P3,P4,P7,P8,P9,P10,U1 pages=[12/12 PASS] bad_rc=0 bad_fail=0 bad_last=0`, 흉내 판 기대값 그대로 — 18 사례로 늘린 뒤 흉내 판정식에서 `cases=18 wrong=0` 을 다시 쟀다)
  음성 대조: 판정식을 시작 판으로 되돌리면 `wrong=8` · `bad_rc=0` — 사례와 마지막 쪽 사본이 둘 다 판별한다 (봉인 전 실측)
  산출물이 검사인 조건: ① 첫 칸만 읽기 — 위반을 마지막 쪽에만 둔 사본이 위 측정의 `bad_last=1` 이다 ② 해당 없음 (새 시험 파일 없음 — 이 검사는 CI 에 없고 이 계약도 등록하지 않는다. 등록 여부는 notes 에 적는다) ③ 해당 없음 (쪽 순회 코드는 바꾸지 않는다 — 판정식 한 줄 변경) ④ 해당 없음 (고정 해석기 python3)
- [ ] SC-02: 새 검사 `scripts/check-cause-table-copies.py` 가 판정 표 사본 둘을 원문과 대조한다(Codex 결함 2) — Given 구현 커밋 뒤 끝 판 트리, When 그 트리에서 `python3 scripts/check-cause-table-copies.py` 를 (가) 그대로 (나) react 사본의 `**미확정**` 을 `**미정**` 으로 바꾼 사본 (다) 원문 판정 표 첫 줄의 `귀속 불명이다 |` 를 `귀속 불명 |` 로 바꾼 사본에서 돌리면, Then (가) 종료 코드 0 · `OK flutter-toolkit/skills/flutter-preflight/SKILL.md` · `OK react-kit/skills/react-preflight/SKILL.md` 각 1 줄 (나) 종료 코드 1 · flutter `OK` 1 · react `MISMATCH` 1 (다) 종료 코드 1 · 두 사본 모두 `MISMATCH` 다. 대조 규칙은 원문 덩어리(SK-01 과 같은 시작 · 끝 줄)가 사본 안에 끊김 없이 있느냐이며, 줄 앞 공백 · 인용 표식 `>` · 끝 공백 · 빈 줄은 무시한다 [exact]
  측정: `m SC-02` 가 `clean=rc0/ok_f=1 ok_r=1 mis_f=0 mis_r=0 | react_bad=rc1/ok_f=1 ok_r=0 mis_f=0 mis_r=1 | canon_bad=rc1/ok_f=0 ok_r=0 mis_f=1 mis_r=1` (시작 판 `script=0`, 흉내 판 기대값 그대로)
  음성 대조: (나) · (다) 가 변이 사본이다 — 사본만 · 원문만 바꿔도 각각 실패해 검사가 두 쪽을 모두 읽는다 (봉인 전 실측)
  산출물이 검사인 조건: ① 첫 칸만 읽기 — (나) 가 위반을 둘째 사본(react)에만 둔 사본이고 기대 출력은 react `MISMATCH` 1 · 읽은 사본 수 2(요약 `checked=2`) ② CI 등록은 SC-03 ③ ER-01 ④ 해당 없음 (고정 해석기 python3)
- [ ] SC-03: 새 검사가 CI 첫 작업과 종료 코드 표에 등록된다(짝 조건 ②) — Given 구현 커밋 뒤, When `.github/workflows/ci.yml` 과 `harness/evals/gate-exit-codes.md` 를 읽으면, Then `run: python3 scripts/check-cause-table-copies.py` 줄이 1 개이고 그 줄이 든 작업이 `jobs:` 의 첫 작업이며, 종료 코드 표에 `` | `scripts/check-cause-table-copies.py` | 0 · 1 · 2 | `` 행이 1 개다 [exact]
  측정: `m SC-03` 이 `ci_steps=1 job=[validate:] first_job=[validate:] exitdoc=1` (시작 판 `ci_steps=0 job=[] first_job=[validate:] exitdoc=0`)
- [ ] SC-04: reviewer 사본 검사가 flutter-audit 사본까지 재고, 그 사본이 원문과 같으며, 평가 가이드의 사본 수 안내가 맞다(k1 KF-2) — Given 구현 커밋 뒤 끝 판 트리, When `python3 scripts/check-reviewer-protocol-copies.py` 를 그대로 · flutter-audit 사본의 `**임계값 2 는` 앞에 `3.` 과 빈칸 한 칸을 붙인 사본에서 돌리면, Then 그대로는 종료 코드 0 · `OK flutter-toolkit/skills/flutter-audit/SKILL.md` 1 줄 · 요약 `checked=8 violations=0 infra_errors=0 excluded=1`, 변이 사본은 변이가 1 줄 들어갔고 종료 코드 1 · `MISMATCH flutter-toolkit/skills/flutter-audit/SKILL.md` 1 줄이다. `harness/docs/guides/qa-evaluation-guide.md` 의 `> **사본 검사:**` 문단에 `flutter-audit` 이 있다 [exact]
  측정: `m SC-04` 가 `rc=0 fa_ok=1 sum=[checked=8 violations=0 infra_errors=0 excluded=1] bad_applied=1 bad_rc=1 bad_mis=1 guide_fa=1` (시작 판 `rc=0 fa_ok=0 sum=[checked=7 violations=0 infra_errors=0 excluded=1] bad_rc=0 bad_mis=0 guide_fa=0`)
  음성 대조: 변이 사본이 `bad_rc=1` — 목록에 넣은 것이 실제로 재진다 (봉인 전 실측)
- [ ] SC-05: `dirty_except_status` 가 계약 앞머리의 `status:` 줄만 빼고 본문의 `status:` 줄은 센다(cs 독립 검토) — Given 끝 판 `harness/references/contract-schema.md` 에서 `dirty_except_status() {` 줄부터 첫 `}` 줄까지 뗀 함수, When 알려진 답 저장소(커밋 하나: 계약 `c.md` = `---` · `status: active` · `---` · `- [ ] AR-01: x` · `status: body`, 다른 파일 `o.txt`)에서 아홉 경우를 bash 와 zsh 로 돌리면, Then 두 셸 모두 k1 깨끗함 0 · k2 앞머리 status 만 바꿈 0 · k3 앞머리 status + 조건 문구 2 · k4 다른 파일 고침 1 · k5 새 파일 1 · k6 앞머리 status + 본문 끝에 `status: sneaky` 더함 1 · k7 본문 `status: body` → `status: other` 2 · k8 없는 계약 파일은 종료 코드 2 에 표준 출력 빈 값 · k9 HEAD 에 없는 새 계약 0 이다 [exact]
  측정: `m SC-05` 가 `bash: k1=0 k2=0 k3=2 k4=1 k5=1 k6=1 k7=2 k8=rc2/[] k9=0` 과 zsh 같은 값 (시작 판 두 셸 모두 `k6=0 k7=0` 이고 나머지는 같다)
  알려진 답: 손으로 세면 k3 은 AR-01 줄의 지운 줄 1 · 더한 줄 1 = 2, k6 은 본문에 더한 줄 1, k7 은 본문 줄의 지운 줄 1 · 더한 줄 1 = 2 다. 흉내 판 실제값 같음 · 종료 코드 0
  음성 대조: 시작 판 함수가 `k6=0 k7=0` — 옛 구현을 두면 실패한다 (봉인 전 실측)
- [ ] SC-06: sprint-contract Step 9 의 초안 해시 조각이 `save-feedback.sh` 와 같은 값을 낸다(k2) — Given 끝 판 `harness/skills/sprint-contract/SKILL.md` `### 9.` 절의 `` `project_hash` `` 항목 아래 첫 bash 블록(앞 다섯 칸 들여쓰기를 뗌)과, 같은 판 `harness/scripts/save-feedback.sh` 의 `identity_root_of` · `hash8` 함수, When 조각을 `CONTRACT_ROOT` = 이 작업 폴더 W(워크트리) · 임시 폴더(git 밖)로 두고 bash 로 돌리면, Then 두 경우 모두 마지막 줄이 `hash8 "$(identity_root_of <그 폴더>)"` 와 같고, W 에서의 값은 `1a3bcba6` 이다 [exact]
  측정: `m SC-06` 이 `wt=1a3bcba6 wt_same=1 plain_same=1` 과 `lines=` 값 (시작 판 `wt=70da29df wt_same=0 plain_same=1 lines=8`, 흉내 판은 스크래치 복제본이라 `wt_same=1 plain_same=1`)
  알려진 답: 본 레포 폴더 `/Users/jackson/Hub/10_Dev/claude-plugins` 를 `printf '%s' <경로> | shasum -a 256 | cut -c1-8` 로 손으로 해시하면 `1a3bcba6`, W 경로는 `70da29df` — 워크트리에서 조각이 낼 값은 앞의 것이다. 봉인 전 `save-feedback.sh` 함수로 W 를 재 `1a3bcba6` · 종료 코드 0
- [ ] SC-07: 안티패턴 AP-04 가 정규식 대신 validate-plugin V1 명령으로 판정된다(us) — Given 구현 커밋 뒤, When `.harness/project.yaml` 의 `- id: AP-04` 항목(다음 항목 앞까지)을 읽고 그 명령을 끝 판 트리에서 그대로 · react-preflight 의 `name:` 줄을 지운 사본에서 돌리면, Then 항목에 `command: "python3 scripts/validate-plugin.py --check=frontmatter"` 가 1 줄 · `pattern:` 이 0 줄 · message 줄 `SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL` 이 그대로 1 줄이고, 그대로는 종료 코드 0, 변이 사본은 0 이 아니다 [exact]
  측정: `m SC-07` 이 `cmd=1 pattern=0 msg=1 rc=0 bad_rc=2` (시작 판 `cmd=0 pattern=1 msg=1 rc=0 bad_rc=2` — 명령 자체는 시작 판에도 있다)

## Error

- [ ] ER-01: 새 검사가 못 읽는 입력을 조용히 넘기지 않는다(산출물이 검사인 조건 ③) — Given 끝 판 트리, When (라) flutter 사본을 읽기 권한 없게(`chmod 000`) 하고 react 사본의 `**미확정**` 을 바꾼 사본 (마) 원문에서 `| 공용 작업 폴더 |` 줄을 지운 사본에서 `python3 scripts/check-cause-table-copies.py` 를 돌리면, Then (라) 종료 코드 2 · `UNREADABLE flutter-toolkit/skills/flutter-preflight/SKILL.md` 1 줄과 `MISMATCH react-kit/skills/react-preflight/SKILL.md` 1 줄이 함께 나오고 (마) 종료 코드 2 · `CANON_MISSING` 으로 시작하는 줄 1 개 · `OK` 로 시작하는 줄 0 개다 [exact]
  측정: `m ER-01` 이 `unread=rc2/unr_f=1/mis_r=1 canon_gone=rc2/canon_missing=1/ok_lines=0` (시작 판 `script=0`, 흉내 판 기대값 그대로)

## Architecture

- [ ] AR-01: 바뀐 파일이 범위 목록 안이고 범위 목록 파일이 모두 바뀌며 한 커밋에 맨 위 폴더 하나다 — Given 구현 · notes · QA 리포트 커밋이 모두 가지 `chore/ak2-cx` 에 들어간 뒤, 시작점 `82ec540` 부터 끝점 `TIP=$(git -C W rev-parse --verify chore/ak2-cx)` 까지(`HEAD` 를 쓰지 않는다. 해석이 안 되면 `UNRESOLVED` 로 멈춘다), When `git diff --name-only` 로 모은 경로를 이 계약 `## 범위 경계` 의 범위 목록 블록(33 경로)과 대조하면, Then `.harness/` 밖 경로가 모두 블록 안이고(생성물 없는 묶음이라 제외 경로 없음), 블록의 33 경로가 모두 바뀌었으며, 병합이 아닌 커밋마다 맨 위 폴더(뿌리 파일은 `(root)` 하나로 센다)가 하나다 [exact, enumerated]
  측정: `m AR-01` 이 `scope=33 changed=` 값 `extra=0 missing=0 multi_top=0` (시작 판 `scope=0 changed=0 extra=0 missing=0 multi_top=0` — 계약이 없어 목록이 빈다)
  양성 대조: 흉내 판에 범위 밖 `scripts/x.sh` 와 `.github` · `scripts` 를 한 커밋에 섞은 bad 에서 `extra=1 … multi_top=1` 과 밖 경로 줄 (봉인 전 실측)
- [ ] AR-02: 항목 표와 판단 · 넘김을 notes 에 남긴다 — Given 끝점 `TIP`, notes 파일 `.harness/.meta/after-kaizen-0926b/cx-notes.md` 가 커밋돼 있고 열 토큰 `| 항목 |` · `계약에 넣음` · `처리됨` · `이 묶음 밖` · `tone-guide` · `visual-styles.html` · `cs-notes` · `vsb-notes` · `us-notes` · `k2-notes` 가 각 1 줄 이상이다. 담을 내용: 위 `## 범위 경계` 표와 같은 항목별 처리(끝 판 기준으로 다시 확인), 커밋 목록, 이 묶음 밖으로 넘긴 것과 이유(문서 페이지 · 기존 경고는 부모 다음 차례, 단추 id 검사는 `visual-styles.html` 단추 크기 때문에 문서 페이지 차례, 다른 킷 raw 안내 69 파일), `check-api-kit-docs.py` 를 CI 에 넣을지 판단, tone-guide 5 단계 대조 결과 [exact, enumerated]
  측정: `m AR-02` 가 `committed=1` 과 1 이상 열 (시작 판 `committed=0` 과 0 열)
- [ ] AR-03: 봉인 커밋이 계약 한 파일이고 구현보다 먼저이며 봉인 뒤 조건 · 측정 줄이 그대로다 — Given 끝점 `TIP`, When 시작점..끝점 구간에서 이 계약 파일을 처음 담은 커밋을 찾으면, Then 그 커밋의 파일이 1 개이고, `.harness/` 밖을 처음 건드린 구현 커밋의 조상이며(같은 커밋이 아니다), 그 커밋 판 계약과 끝 판 계약의 조건 줄 지문 · 측정 줄 지문(체크 상태를 정규화한 sha256 앞 16 자리)이 각각 같고, 끝 판 계약의 `conditions_digest` · `measurement_digest` 가 그 지문과 같다(`SEAL_OK` · `MEASURE_OK`) [exact]
  측정: `m AR-03` 이 `seal_commit_files=1 seal_before_impl=1 seal_same_as_tip=1 measure_same_as_tip=1 this=SEAL_OK MEASURE_OK` (시작 판 `seal_commit_files=0 seal_before_impl=0 seal_same_as_tip=0 measure_same_as_tip=0 this=SEAL_ABSENT MEASURE_ABSENT`)
  양성 대조: bad(봉인 뒤 조건 문구 변조)에서 `seal_same_as_tip=0 this=SEAL_BROKEN` (봉인 전 실측)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가
  측정: 끝 판을 풀어 둔 `E` 에서 `m AP-03` 이 `v6_rc=0 fail=0` (시작 판 `v6_rc=0 fail=0`)
  양성 대조: bad(react-preflight 끝에 언어 없는 fence)에서 `v6_rc=2 fail=2` (봉인 전 실측)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL
  측정: `m AP-04` 가 `v1_rc=0 fail=0` (시작 판 `v1_rc=0 fail=0`)
  양성 대조: SC-07 의 변이 사본(react-preflight `name:` 삭제)에서 같은 명령이 종료 코드 2 (봉인 전 실측)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 — 사본 대조의 두 함수(줄 정규화 · 끊김 없는 덩어리 찾기)가 밑줄 없는 이름으로 `scripts/plugin_utils.py` 에 있고 두 사본 검사가 그것을 가져다 쓴다
  측정: `m RE-02` 가 `normalized=scripts/plugin_utils.py contains=scripts/plugin_utils.py chk_import=1` (시작 판 `normalized=scripts/check-reviewer-protocol-copies.py contains=scripts/check-reviewer-protocol-copies.py chk_import=0`)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 새 검사는 reviewer 사본 검사의 정규화 규칙을 다시 짜지 않는다: `scripts/` 아래 `def normalized` 와 `def contains_block` 이 각각 한 파일(`scripts/plugin_utils.py`)에만 있고, 새 파일은 `scripts/check-cause-table-copies.py` 하나다
  측정: `m RE-02` 가 위와 같고 `m RE-01` 이 `added=[scripts/check-cause-table-copies.py ]` (시작 판 `added=[]`)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 바뀐 파일과 교집합 0 개. 측정: `m DG-01` 이 `release_sh=0`. 실제 검사는 DG-02 · DG-05 · SC-*)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — IDE(편집기) 진단을 명령줄로 같게 잰다: 바뀐 `.md`(계약 · QA 리포트 · 개정 파일 `.harness/sprint-*.md` 제외)의 더해진 줄에 걸린 markdownlint-cli2 0.23.2(MD013 끔, 편집기 확장과 같은 설정) 경고가 0 이다. 파이썬 파일은 `python3 -m py_compile` 이 통과한다
  측정: `m DG-02` 가 `md_new=0` (시작 판 `md_new=0` — 바뀐 파일이 없다), 끝 판 트리에서 `python3 -m py_compile scripts/check-cause-table-copies.py scripts/check-reviewer-protocol-copies.py scripts/plugin_utils.py scripts/check-api-kit-docs.py scripts/detect-docs-drift.py` 종료 코드 0
  양성 대조: `CLAUDE.md:263` 은 시작 판부터 MD060 두 건이 걸린 줄이라, 그 줄만 고친 흉내 판에서 `md_new=1`(`CLAUDE.md=1`)이 나왔다. 구분 줄 `:262` 를 `| --- | --- |` 로 바꾼 흉내 판은 `md_new=0` (봉인 전 실측)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: `m DG-03` 이 `release_sh=0` — 도우미 안에서 `m DG-01` 을 그대로 부른다)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 새 실행 파일은 CI 검사 스크립트 하나이고 그 실행은 SC-02 · ER-01 · DG-05 가 잰다. 측정: `m DG-04` 가 `entry=0` — 구간에 새로 생긴 `.harness` 밖 실행 파일 가운데 `scripts/check-*.py` 가 아닌 것의 수)
- [ ] DG-05: CI(자동 검사) 단계를 로컬에서 전부 돌려 통과한다 — Given 작업 폴더 W 가 끝점과 같다(`git -C W rev-parse HEAD` 가 `TIP` 이고, `git -C W status --porcelain --untracked-files=no` 가 빈 출력이거나 이 계약 파일 한 줄뿐이며 그때 그 파일의 차이가 `status:` 한 줄뿐 — 평가자가 APPROVE 때 바꾸는 줄이다), When `PYTHONDONTWRITEBYTECODE=1 TMPDIR=<임시 폴더> bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-cx` 를 돌리고, 그 도구에 없는 CI 단계 셋을 도우미로 돌리면, Then 요약 `$TMPDIR/ci-local/summary.txt` 에 `rc=0` 줄이 25 개이고 `rc=0` 이 아닌 줄은 `feedback-agg-test SKIP (yq 없음)` 하나뿐이며, 도우미 셋(문서 매핑 표 대조 · 새 사본 검사 · 측정 도우미 시험)이 모두 0 이다
  측정: `grep -c 'rc=0' "$TMPDIR/ci-local/summary.txt"` 가 25 · `grep -v 'rc=0' "$TMPDIR/ci-local/summary.txt"` 가 그 한 줄 · `m DG-05X` 가 `… = 0 0 0`. 전제의 `status:` 한 줄 확인은 `git -C W diff -U0 -- .harness/sprint-contract-after-0926-codex-and-leftover-fixes.md | grep -E '^[-+][^-+]' | grep -vc '^[-+]status:'` 가 0 (시작 판 봉인 전 실측: 25 · SKIP 한 줄. 흉내 판 `m DG-05X` 는 첫 판 `0 1 0` — 사본 덩어리 끝을 잘못 잡은 흉내에서 새 검사가 실제로 빨갰다)
  도구 지문: 돌리기 전에 `shasum -a 256 <ci-local.sh> | cut -c1-16` 이 `59fe55125c0dbc77` 인지 본다 — 추적 안 된 도구라 다르거나 없으면 ci-local 쪽은 다시 잴 수 없다(대체 수단 없음, 평가자가 그 사실을 적는다). `m DG-05X` 는 도구와 무관하게 잰다
  음성 대조: 이 묶음이 깨뜨릴 수 있는 단계는 `validate-plugin` · `run-kaizen-assertions` · 새 사본 검사다 — AP-03 · AP-04 bad 와 SC-02 (나) 가 각각 0 이 아닌 종료 코드 (봉인 전 실측)

## 리서치 소스

- 저장소 안만 읽었다(웹 조회 · 외부 문서 가져오기 없음): Codex 점검 · 열두 notes · 결정 파일 · 남은 일 목록(위 배경의 경로, 읽기만), 앞 계약 `.harness/sprint-contract-after-0926-prd-none-followups.md`(형식 · 측정 도우미 틀), OpenAPI 판 번호는 `ex/EX-7.md` 의 2026-09-26 원문 대조를 그대로 쓴다
- 계약 형식 원본: 이 가지의 `harness/skills/sprint-contract/SKILL.md` · `harness/references/contract-schema.md` §계약 봉인 · §측정 줄 봉인 · §범위 목록 블록 · §산출물이 검사인 조건
