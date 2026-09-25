---
feature: "카이젠 2026-09-24 Phase 1 설계 가이드 — 못 한다 전 네 칸(harness:P09 · F10) · 알려진 답 대조 생성 측(harness:P05 §3.7) · 현행화"
slug: kaizen-0924-p01-guides
created: "2026-09-24 19:45"
complexity: "복잡"
conditions: 25
status: done
owner_session: de8c7935-a5b6-4df5-9106-fafa73c288a0
conditions_digest: sha256:176baf1603fe5981
locked_at: "2026-09-24 20:35"
---

## 배경

이 Phase 의 외부 근거는 `.harness/.meta/evidence/phase1.md` 하나다. 처리 배정표(`.claude/kaizen-input/insights-report.md`)에서
`배정` 칸이 `Phase 1` 인 행은 둘이고, 한 행은 다른 Phase 배정이지만 이 Phase 가 맞출 부분을 갖는다.

| 키 | 내용 | 이번 처리 |
| --- | --- | --- |
| `F10` | 앱이 안 올라갔다 · 실기기가 없다로 불가능 선언, 서버 목록 상한을 막힘으로 과대 해석 | 반영 — skill 가이드 §3.7 5 조항 3 항 |
| `harness:P09` | 검증 불가 문장을 「막는 것 · 시도한 우회 · 다시 돌릴 명령」으로 | 반영 — skill 가이드 §3.7 3 항 + agent 가이드 §10 정책 |
| `harness:P05` (Phase 2 배정) | 알려진 답 대조 소절. 비고: skill-design-guide §3.7 부분은 Phase 1 과 맞춘다 | §3.7 생성 측만 반영. 계약 측 형식과 zsh 배열 한 줄은 Phase 2 몫 |

세 가지를 함께 고친다.

1. **못 한다고 말하기 전 네 칸.** 지금 생성 측 문구는 `[미검증]` 마커와 사유 한 줄뿐이다
   (`skill-design-guide.md:300`). 평가 측(`harness/agents/qa-evaluator.md:65`)은 이미 네 요건 — 1 차 도구 시도 ·
   대안 검증 시도 · 실패 로그 · 통제 불가 사유와 재검증 명령 — 을 요구하고 `[미검증:ENV]` · `[미검증:INVALID]` 로
   가른다. 그런데 agent 가이드 §10 정책 4 항(`agent-design-guide.md:569-575`)은 옛 구성(마커 · 2 건 REJECT ·
   조용한 PASS 금지 · 생성자 주장 배제)에 머물러 평가자와도 어긋난다. 작업 자체를 불가로 선언한 사고(F10)는
   검증 불가와 같은 모양이다 — 막는 것의 실제 출력도, 시도한 우회도 없이 결론부터 냈다.
2. **알려진 답 대조 생성 측.** §3.7 에는 0 이 기대값인 측정의 양성 대조만 있다. 새로 짠 측정 스크립트가 0 이 아닌
   값을 낼 때 그 값이 맞는지 보는 규칙이 없어서 2026-09-22 에 호 이동 길이를 빠뜨린 G-code 길이 측정과 zsh 배열
   첨자가 한 칸 밀린 측정이 그대로 믿어졌다(데이터 풀 §0-b `d204ea78`).
3. **근거 파일 §3 현행화.** agent 가이드 frontmatter(머리 설정) 필드 15 종 → 공식 18 종, 내장 Explore 모델, 세션 누적
   200 개 상한 주장, 두 가이드의 「2026-04 최신」 표기, skill 가이드 500 줄 「상한」 표기.

GAP 분석 중에 근거 파일 밖의 결함 둘을 더 찾았다 (둘 다 파일 안 모순이라 외부 근거가 필요 없다).

- skill 가이드 `:334` 가 「§11 parity 표 15 번째 항목」을 인용하는데 §11 표는 14 행이다. 15 행은
  `qa-evaluation-guide.md:1874` 에만 있다(`Zero-Result Positive Control`). agent 가이드 §12 표에도 없다.
- skill 가이드 `:315` 가 「현재 등급: E2 (§3.7 등급 원장 참조)」라고 적었는데 `#### 등급 원장` 표 8 행에 그 원칙 행이 없다.

## 리서치 소스

외부 조회 0 회. 아래 URL 은 전부 근거 파일에서 가져왔다.

- [Anthropic Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md) — 순차 단계 · 검증기 실행 → 고침 → 재실행 · 검증 통과 전 다음 단계 금지 (P09 방향의 근거). 500 줄은 「최적 성능을 위해 미만」 권고
- [Claude Code — Create custom subagents](https://code.claude.com/docs/en/sub-agents.md) (2026-09-22 수정본) — frontmatter 18 종 · `initialPrompt` 범위 · 내장 Explore 모델 상속 · 세션 전체 스폰 수 상한 없음
- [anthropics/skills — skill-creator SKILL.md](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) — eval 의 `expected_output` · 500 줄은 ideal
- [Claude Code v2.1.281 릴리스](https://github.com/anthropics/claude-code/releases/tag/v2.1.281) — 2026-09-23 게시, 조회 시점 최신
- [zsh 매뉴얼 — Array Subscripts](https://zsh.sourceforge.io/Doc/Release/Parameters.html#Array-Subscripts) — 기본 zsh 배열은 1 부터, `KSH_ARRAYS` 예외

근거 파일이 스스로 밝힌 한계를 계약에 그대로 옮긴다: 「우회 1 개 이상 의무」의 공식 문구는 없다(공식 근거는
검증 실패 뒤 고쳐서 다시 돌리는 루프까지다). 「알려진 답 입력 2~3 줄」은 외부 근거가 없는 레포 관례다. 세션 누적
상한이 어느 릴리스에서 없어졌는지는 특정하지 못했다. 필수 소스 표의 arXiv 항목은 조회하지 않았다.

내부 입력: 데이터 풀 §0 처리 배정표 · §0-b 세션 `e863512e` · `d93c7e7a` (F10) · `d204ea78` (측정 스크립트 결함) ·
§1 Improvement Suggestions (Phase 1 해당 항목 없음 — 전부 계약·평가 측).

## GAP 분석 · 개선안 초안

### 1.1 복잡도 4 축

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 1 — 설계 가이드 문서 2 개 |
| 공개 API·계약 변경 | 외부에 노출된 형태가 바뀌는가 | 예 — `[미검증]` 보고 형식(네 칸)과 agent §10 정책 4 항의 내용이 바뀐다 |
| 소비면 존재 | 이 문구를 받아 쓰는 반대편이 있는가 | 예 — 아래 Counterpart 표 13 곳 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 다른 파일이 조항 번호 · 항 수 · parity 번호를 인용한다 |

3 축이 「예」이고 공개 계약 변경과 소비면이 둘 다 「예」라 **복잡**이다. Step 2.5 Counterpart 조건을 넣는다 (ER-02 · ER-04).

### 1.2 설정 리터럴 대조표

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A 사유에 그대로 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A 사유에 그대로 |
| `diagnostics.ide_exclude` | `[]` | DG-02 에 그대로 |
| `contract_categories[].id` / `prefix` | `Skill`/`SK` · `Script`/`SC` · `Error`/`ER` · `Architecture`/`AR` | 조건 섹션 헤더와 접두 그대로 |
| `anti_patterns[].id` / `message` | AP-01 · AP-02 · AP-03 · AP-04 | AP-01 · AP-03 선별, message 원문 그대로. AP-02(force push)는 이 Phase 가 밀어 넣지 않아서, AP-04(SKILL.md · agents 의 `name`)는 그 파일을 바꾸지 않아서 뺀다 |

### 1.4 편집 전 감사 (실제로 읽은 줄)

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 |
| --------- | ---------------------------- | ------------------- | ---------------- |
| `harness/docs/guides/skill-design-guide.md` | `:300` (5 조항 3 항) · `:308` (Good 예시) | `[미검증]` + 사유 한 줄뿐. 네 칸 · 불가 선언 규칙 없음 | SK-01 · ER-03 |
| 같은 파일 | `:313-337` (0 기대 양성 대조) · `:315` · `:275-288` (등급 원장 8 행) | 0 이 아닌 기대값 규칙 없음. `:315` 가 가리키는 원장 행 없음 | SK-02 · SK-03 |
| 같은 파일 | `:334` · `:1085-1106` (§11 parity 14 행) · `:1095` (5 행) · `:1087` · `:1106` (표 위아래 문장) | 15 번째 인용이 빈 곳을 가리킴. 5 행이 옛 「2 건 임계」. 표 위아래 문장이 「14개」 · 「(1~6, 9~11, 14)」 로 개수를 따로 적는다 | SK-04 · ER-03 |
| 같은 파일 | `:9` · `:15` · `:1159` (2026-04) · `:560` · `:1133` (500 라인 상한) | 「최신」 고정 표기. 권고를 상한으로 적음 | AR-03 |
| 같은 파일 | `:1139` (요약 Completion Evidence Gate) | 네 칸 없음 | SK-01 |
| `harness/docs/guides/agent-design-guide.md` | `:68-96` (frontmatter 15 행 · `initialPrompt` 불릿 `:95`) · `:98` | 공식 18 종과 3 개 차이 | AR-01 |
| 같은 파일 | `:214` (Explore haiku) · `:463` · `:701` (세션 200) · `:9` · `:15` · `:715-716` | 근거 파일 §3 의 낡은 값 | AR-03 |
| 같은 파일 | `:569-580` (Unverifiable 정책 4 항 · `:570` `[정적]` 또는 · `:575` · `:579` 특정 앱 이름) · `:706` (요약) | 평가 측 분류와 어긋남. 지침이 금지한 앱 이름 | AR-02 · ER-02 · ER-03 |
| 같은 파일 | `:642-660` (§12 parity 9 행 · `:644` 「아래 9개 항목」 · `:660` 「2 건 임계값은 양쪽이 동일」) | `Zero-Result Positive Control` 행 없음 | SK-04 · ER-03 |
| `harness/agents/qa-evaluator.md` | `:54` · `:64-66` | 이미 ENV/INVALID · 네 요건. 고칠 것 없음 | ER-04 (편집 금지 확인) |
| `harness/docs/guides/qa-evaluation-guide.md` | `:1862-1874` | Parity Table 15 행 있음. 고칠 것 없음 | ER-04 |

### Counterpart — 이 문구를 받아 쓰는 반대편 파일

| 파일 | 인용 | 이번 처리 |
| --- | --- | --- |
| `react-kit/references/render-evidence-protocol.md:125` | 「§3.7 5 조 3 항」 2 건 이상 부분 완료 | 번호 · 문구 유지 (ER-02) |
| `planning-kit/skills/plan-audit/SKILL.md:25` | 「§3.7 조항 4」 | 번호 · 문구 유지 (ER-02) |
| `flutter-toolkit/references/visual-evidence-protocol.md:169` | 「5 조항 SSOT」 | 조항 수 5 유지 (ER-02) |
| `harness/docs/guides/qa-evaluation-guide.md:1868` | 「§10 Unverifiable (4 항)」 | 항 수 4 유지 (ER-02) |
| `harness/agents/qa-evaluator.md:65` | 네 요건 원본 | 이미 맞다 — 편집 없음 (ER-04) |
| `harness/skills/create-agent/SKILL.md:25,33,81,106` | 「15 종」 · 「4항: (2) 2건 이상 자동 REJECT」 | Phase 4 범위 — 명시적 미완으로 넘김 (ER-04) |
| `harness/skills/sprint/SKILL.md:77` | 「`[미검증]` + 사유 한 줄」 | Phase 4 범위 (처리 배정표 비고 「sprint/SKILL.md 3 단계 부분은 Phase 4 와 맞춘다」) — 넘김 (ER-04) |
| `harness/skills/create-skill/SKILL.md:24` | 「1500-2000 words 타깃 — Anthropic 기준」 (근거 파일: 확인 못 함) | Phase 4 범위 — 넘김 (ER-04) |
| `react-kit/references/render-evidence-protocol.md:59` | 「`[미검증]` 마커와 사유 한 줄 … 부분 완료로 보고」(3 항 옛 문구) | Phase 10 범위 — 넘김 (ER-04) |
| `flutter-toolkit/references/visual-evidence-protocol.md:136` | 「`[미검증]` 마커 + 사유 한 줄」 | Phase 5 범위 — 넘김 (ER-04) |
| `onboarding-kit/skills/setup-guide/SKILL.md:30` | 「마커 + 사유 한 줄」 | Phase 14 범위 — 넘김 (ER-04) |
| `infra-kit/skills/infra-test/SKILL.md:37` | 「`[미검증] TOOL_OR_ENV_MISSING` … 재검증」 — 시도한 우회 칸 없음 | Phase 8 범위 — 넘김 (ER-04) |
| `rust-kit/agents/rust-reviewer.md:137` | 「agent-design-guide §10」 접미 없는 `[미검증]` | Phase 9 범위 — 넘김 (ER-04) |

위 다섯 줄은 1 차 검토가 찾았다. 조항 번호가 아니라 3 항 옛 문구와 agent §10 을 내용째 베낀 곳이다 — 찾은 명령:
`grep -rnE "(미검증|마커).{0,40}사유 한 줄" --include="*.md" .` · `grep -rnF "agent-design-guide §10" --include="*.md" .` ·
`grep -rnF "TOOL_OR_ENV_MISSING" --include="*.md" .` (`.harness/` 와 두 가이드 자신은 뺌, 2026-09-24 재실행해 같은 다섯 곳 확인).

### 개선안 초안 (BUILD 가 문장을 다듬어 넣는다)

skill 가이드:

- 머리 설정 `version: 1.6.0` · `last_updated: 2026-09-24`. `:9` 「(2026-04 최신)」 · `:15` · `:1159` 「(2026-04)」 → 「(2026-09-24 조회)」
- §3.7 5 조항 **3 항을 번호 그대로 두고** 다시 쓴다. 검증을 못 하면 `[미검증]` 에 네 칸을 붙인다 — **막는 것**(실행한 명령과
  그 실패 출력) · **시도한 우회**(하나 이상과 그 결과) · **통제 불가 사유**(한 문장) · **재검증 명령**(조건이 갖춰지면
  돌릴 명령). 네 칸이 다 있으면 평가에서 `[미검증:ENV]`, 하나라도 비면 `[미검증:INVALID]` 로 센다.
  「미검증 2 건 이상이면 완료가 아니라 부분 완료로 보고」 문장은 남긴다. 옛 문장 「마커·임계값은 agent-design-guide §10
  … 과 동일 규약을 쓴다」는 「마커와 네 칸은 agent-design-guide §10 과 같은 말을 쓴다 (용어 분기 금지)」로 바꾼다 — 2 건
  기준은 세는 대상이 달라 「동일」이 아니다(생성 측은 `[미검증]` 전체, 평가 측은 `INVALID` 만). `시도한 우회` 칸에 한 문장:
  검증을 못 한 경우 우회가 정말 없으면 칸을 비우지 말고 `없음 — 이유` 를 적는다(`qa-evaluator.md` 규칙 11 (2) 가 계약
  결함 기록으로 받는다). 작업 자체를 못 한다고 할 때는 하나 이상이어야 한다 — 이 문장은 근거 파일 §4 권장안 그대로다.
  이어서 한 문장: **작업 자체를 못 한다고 결론 내리기 전에도 같은 네 칸을 먼저 적는다** — 실측 예(2026-09-18 · 09-23):
  배포 전 · 실기기 없음을 이유로 두 작업을 불가로 선언했는데 사용자가 「올리면 되잖아」로 되받았고, 서버 목록 상한을
  막힘으로 읽었는데 그 작업은 서버 연동이 필요 없었다. 앱 이름은 쓰지 않는다
- 5 조항 아래 예시 블록: 옛 `Good: 검증 불가 → "[미검증] MCP 미설정 — 시각 대조 불가"` 줄을 네 칸 예시로 바꾸고,
  「실기기가 없다 → 불가 선언 (시도한 우회 없음)」 Bad 줄을 더한다
- `#### 0 이 기대값인 검증의 양성 대조` 뒤에 새 소절 `#### 0 이 아닌 값을 내는 새 측정 — 알려진 답 대조` (현재 등급: E2).
  적용: 이번에 새로 짠 측정 스크립트가 길이 · 개수 · 무게 · 비율처럼 0 이 아닌 값을 낼 때. 손으로 답을 셀 수 있는 작은
  입력(2~3 줄 — 레포 관례이며 외부 근거는 없다)을 먼저 돌려 기대값 · 실제값 · 명령을 나란히 적는다. 둘이 다르거나,
  0 이 아닌 기대값에 0 · 빈 출력이 나오면 통과가 아니다 — 스크립트나 입력 중 하나가 틀렸다. 양성 대조와 구별: 그쪽은
  나쁜 예에서 1 이상이 나오는지, 이쪽은 좋은 작은 입력에서 정확한 값이 나오는지 본다. 실측 형태 2026-09-22: 호 이동
  길이를 빠뜨린 G-code 길이 측정, 첨자가 한 칸 밀린 zsh 배열 — 기본 zsh 배열은 1 부터 센다(`KSH_ARRAYS` 예외,
  [zsh 매뉴얼](https://zsh.sourceforge.io/Doc/Release/Parameters.html#Array-Subscripts)). Cross-Surface Parity:
  「§11 parity 표 16 번째 항목」 — 이 꼴 그대로 적어야 SK-04 (b) 의 인용 검사에 걸린다. zsh 규칙 문장 자체는 계약 측
  문서가 맡는다 — 여기서는 사례로만 든다
- `#### 등급 원장` 표: `Completion Evidence Gate` 행 현재 등급 칸에 네 칸을 적고, 두 행을 더한다 —
  `0 기대 양성 대조 | §3.7 | E2 (명령 성공 · 대상 수 · 양성 대조 세 기록) | 대조 없이 0 을 통과로 읽은 일 2 회 재발 → …`,
  `알려진 답 대조 | §3.7 | E2 (기대값 · 실제값 · 명령 기록) | 대조 없이 새 측정 값을 믿은 일 2 회 재발 → …`. 셀 안에 `|` 금지
- §5 `:560` 헤더 → `### SKILL.md 본문 500 라인 미만 권고 (공식)`, 요약 `:1133` → `| 500 라인 권고 | … 강제 상한 아님 |`
- §11 표: 5 행 설명에 네 칸, 15 행 `Zero-Result Positive Control (0 기대 측정의 양성 대조)` (skill §3.7 · agent §4 한계 2),
  16 행 `알려진 답 대조 (0 이 아닌 기대값)` (skill §3.7 · agent 쪽 — 생성 측 전용, 평가자는 계약 조건으로 받는다),
  머리줄 `(16개)`. 표 위아래 문장의 개수도 같이 고친다 — `:1087` 「아래 14개 항목을」 → 「아래 16개 항목을」,
  `:1106` 예외 목록 「(7, 8, 12, 13)」 에 16(생성 측 전용)을 더하고 양면 목록 「(1~6, 9~11, 14)」 에 15 를 더한다
- 요약 표 `Completion Evidence Gate` 행에 네 칸

agent 가이드:

- 머리 설정 `version: 1.7.0` · `last_updated: 2026-09-24`. `:9` 「(2026-04 최신)」 → 「(2026-09-24 조회)」, `:15` 「(2026-04)」 → 「(2026-09-24 조회 · 2026-09-22 수정본)」, `:716` 「(2026-04 최신)」 → 「(2026-09-24 조회)」
- §2 frontmatter: `:68` 「(2026-08 재확인)」 → 조회일, `15 종` 네 곳 → `18 종`. 표에 세 행 추가 — `initialPrompt`(메인 세션 에이전트로
  뜰 때 첫 사용자 턴 · 파일 frontmatter 와 `--agents` JSON 양쪽 · 플러그인 서브에이전트에서는 무시된다 · 2026-08 판에서
  뺐다가 다시 확인), `omitClaudeMd` · `experimental`(공식 표에 이름만 확인 — 뜻 미확인, 쓰기 전에 공식 표를 읽는다).
  「표에 없는 이름들」에서 `initialPrompt` 불릿을 뺀다. `:98` 플러그인 제약에 `initialPrompt` 를 더한다
- §4 `:214` Explorer: 부모 모델을 상속한다(v2.1.198 부터, Anthropic API 에서는 Opus 가 상한), 전역으로 바꾸려면 `CLAUDE_CODE_SUBAGENT_MODEL`
- §7 `:463`: 세션 누적 상한 문장과 그 환경변수 · 오류 문구를 뺀다. 「세션 전체 스폰 수에는 상한이 없다」(공식 문서 기준, 없어진 릴리스는 특정 못 함).
  동시 20 · 깊이 3 은 그대로. 요약 `:701` 도 같게 — 숫자 `200` 을 「세션」 옆에 다시 쓰지 않는다.
  같은 문단의 「상한이 3 종 있다」 → 「2 종」. 뒤 문장 「각각 `Concurrent subagent limit reached` / `Subagent spawn limit reached`」도
  남는 상한 수에 맞춘다 — 어느 오류 문구가 어느 상한 것인지는 근거 파일에 없으니 새로 짝짓지 않는다 (2 차 검토 지적)
- §10 「Unverifiable 조건 정책」 **번호 4 개를 유지하며** 다시 쓴다: (1) 마커는 `[미검증]` 에 분류 접미 `:ENV` / `:INVALID`,
  `[정적]` 은 보조 태그 (2) `ENV` 는 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)이 있어야 성립, 하나라도
  없으면 `INVALID`. 네 칸은 `qa-evaluator.md` 규칙 11 의 네 요건을 생성 측 말로 옮긴 것이다 — 요건 (1)·(3) 의 실패 출력이
  `막는 것`, (2) 가 `시도한 우회`, (4) 가 `통제 불가 사유` 와 `재검증 명령` 이다. `INVALID` 2 건 이상이면 REJECT, `ENV` 는
  `env_gaps` 로 따로 세어 검증 범위 판정에만 쓴다(수치는 `qa-evaluation-guide.md` §카운팅 및 자동 REJECT 임계 가 정한다)
  (3) 조용한 PASS 금지 (4) 생성자 완료 주장은 증거가 아니다. Cross-Surface Parity 문장: 「생성 측 짝은 skill-design-guide
  §3.7 3 항이다. 네 칸은 양쪽이 같은 말을 쓴다. 2 건 기준은 세는 대상이 다르다 — 생성 측은 `[미검증]` 전체로 부분 완료를,
  평가 측은 `INVALID` 만으로 REJECT 를 가른다」. 「같은 네 칸 · 같은 2 건 임계」처럼 두 기준을 같다고 쓰지 않는다 — 규칙
  11 과 칸 경계가 1:1 이 아니고(규칙 11 은 실패 로그를 따로 세고 사유와 명령을 한 요건으로 묶는다), 규칙 2 는 `INVALID`
  만 2 건으로 센다. 실패 사례의 특정 앱 이름 → 「한 플러터 앱 프로젝트」
- §12 표: 10 행 `Zero-Result Positive Control (0 기대 측정의 양성 대조)` (agent §4 Agent(agent_type) 한계 2 · skill §3.7), 머리줄 `(10개)`.
  표 위 `:644` 「아래 9개 항목을」 → 「아래 10개 항목을」. 표 아래 `:660` 「마커 표기법과 2 건 임계값은 양쪽이 동일 규약을 쓴다」 →
  §10 Cross-Surface Parity 문장과 같은 말(네 칸은 같고 2 건 기준은 세는 대상이 다르다)
- 요약 `:706` `Unverifiable 정책` 행에 네 칸
- 출처 `:715`: 조회일 · 18 종 · 세션 전체 스폰 수 상한 없음. v2.1.281 릴리스 줄 추가

### 측정 설계에서 걸러 낸 것

- `validate-plugin.py --check=code-fence`(AP-03 설정 명령)는 `harness/docs/guides/` 를 읽지 않는다 — `scripts/validate-plugin.py:516-520`
  이 skills · agents · references · README 만 모은다. 그대로 쓰면 이 두 파일에서는 늘 0 인 측정이 된다. 같은 판정에 펜스
  길이를 더한 검출기(`fence.py`)로 대신 잰다
- parity 인용 번호를 `grep -oE '[0-9]+'` 로 뽑으면 「§11」의 11 까지 섞여 나온다(실측: `5 9 11 11 11 11 11 13 14 15`). `sed` 로 「표 N 번째」의 N 만 뽑는다
- 번역투 정규식 `에 대해서?` 는 C 로케일에서 글자가 아니라 바이트에 `?` 가 붙어 조용히 0 이 된다(실측: UTF-8 2 · C 1). 공통 정의가 `LC_ALL=C.UTF-8` 을 건다
- 표 끊김 검사 V10 은 `harness/docs/**/*.md` 를 읽는다 — 이 검사는 두 가이드를 실제로 잰다(양성 대조 1 이상)
- `mine` 이 커밋 메시지 어디든 슬러그가 있으면 잡으면, Phase 2 가 harness:P05 를 「Phase 1 과 맞춘다」며 메시지에 슬러그를
  인용하는 순간 그쪽 파일이 섞인다(1 차 검토 권고). 제목 줄 끝 `(슬러그)` 꼴은 sprint-contract 6.7 의 봉인 커밋 제목
  `contract: $SLUG 봉인 ($N 조건)` 과 부딪혀 쓰지 않고, 메시지 끝 서명 줄 모양 `Kaizen-Phase: kaizen-0924-p01-guides` 한 줄을
  `^…$` 로 잡는다. 스크래치 저장소 실측: 본문 가운데 같은 글자를 인용한 커밋은 옛 꼴에 잡히고 새 꼴에 안 잡혔다
  (옛 꼴 파일 3 · 새 꼴 2, 기본 · `--basic-regexp` · `-E` 모두 2)
- 17 Phase 가 한 작업 폴더를 같이 쓴다. `verify_seal` 전수와 `doc-contracts` 는 다른 Phase 가 만든 결함도 잡으므로, 그 줄에
  나온 파일이 `mine` 과 겹칠 때만 이 Phase 몫으로 센다 (AR-04 ③ · DG-06, 1 차 검토 지적)

## 범위 경계

- 이 Phase 시작 HEAD: `7689fde6efdaa2401e90689dd15dd16baf8d59a0`. 범위 상한은 개정 파일 `.harness/sprint-amendments-kaizen-0924-p01-guides.md` 의 `end_sha:` 다. 여러 Phase 가 같은 가지 `kaizen/2026-09-24` 에 동시에 커밋하므로 `HEAD` 로 재지 않는다
- 고치는 파일은 `harness/docs/guides/skill-design-guide.md` · `harness/docs/guides/agent-design-guide.md` 둘이다. `.harness/` 쪽은 이 계약 · 개정 파일 · QA 피드백 · `.harness/.meta/kaizen-0924/phase1-notes.md` · `.harness/.meta/kaizen-0924/phase1-review.md` 를 쓴다 — 측정은 슬러그를 나열하지 않고 AR-04 ③ `verify_seal` 로 잰다(러닝북 계약 규칙)
- **이 Phase 의 커밋 메시지에는 전부 `Co-Authored-By` 줄 바로 위에 `Kaizen-Phase: kaizen-0924-p01-guides` 한 줄을 넣는다** (봉인 커밋 포함 — 6.7 의 `-m` 뒤에 `-m` 을 하나 더 준다). AR-04 · `mine` 이 이 줄로 이 Phase 커밋을 가린다. 제목이나 본문에 슬러그를 적는 것은 가림에 쓰이지 않는다
- 측정이 기대는 제목은 이름을 바꾸지 않는다: `## 3.7.` · `### 스킬이 지켜야 할 5 조항` · `#### 0 이 기대값인 검증의 양성 대조` · `#### 등급 원장` · `### 전수 대상 parity items` · `### frontmatter 전체 필드` · `- **Unverifiable 조건 정책` · `- **사용자 실패 보고 우선`
- 공유 파일(`marketplace.json` · `plugin.json` 버전 · 루트 README · 루트 CLAUDE.md · `docs/` HTML · 처리 배정표 · 감사 로그)은 건드리지 않는다. 문서 사이트 재생성은 Final F2 몫이라 DG-06 에서 `docs-site-regen` 을 뺀다
- 넘기는 것 (notes 에 적는다): 위 Counterpart 표의 Phase 4 범위 3 파일과 옛 문구를 베낀 다른 킷 5 곳(`react-kit/references/render-evidence-protocol.md:59` Phase 10 · `flutter-toolkit/references/visual-evidence-protocol.md:136` Phase 5 · `onboarding-kit/skills/setup-guide/SKILL.md:30` Phase 14 · `infra-kit/skills/infra-test/SKILL.md:37` Phase 8 · `rust-kit/agents/rust-reviewer.md:137` Phase 9 — 이번 편집 뒤 옛 규칙을 들고 남는다). 근거 파일 `phase4.md` 에만 있고 이 Phase 근거 파일에는 없는 agent 가이드 `:59`(배치 우선순위) · `:79`(model 생략 시 동작) · skill 가이드 `:393`(`name` 필수 여부) · `:806`(다른 플랫폼 호환) — 다음 사이클. 오케스트레이터 `references/phase-research-templates.md` 의 「500 라인 상한」 표기 — 이 Phase 범위 밖
- 두 가이드에 새 셸 코드 블록을 넣지 않는다 (AP-03). 예시가 필요하면 `text` 블록이나 산문으로 쓴다
- 오라클 해소: SK-01 · SK-02 · SK-03 · SK-04 · ER-02 · AR-02 · AP-03 — 산출물이 설계 가이드의 문장 · 표 자체라 정해진 절 구간에 정해진 문구 · 행 · 번호가 있는지가 곧 산출물 판정이다. 실행할 동작이 없고, 새 셸 스니펫은 AP-03 이 막는다. 각 측정은 절 구간을 잘라 재므로 파일 다른 곳의 같은 낱말로 통과하지 않고, 편집 전 파일에서 전부 0 이 나오는 것을 봉인 전에 확인했다
- 오라클 해소: ER-04 — 넘김 기록(notes)의 경로 문자열이 곧 산출물이고, 편집 금지는 커밋 파일 목록(`mine`)으로 잰다
- 오라클 해소: RE-01 — `N/A (사유)` 줄이다. 사유는 커밋 파일 목록 명령의 출력(0)으로 다시 잰다
- 오라클 해소: DG-06 — 판정은 검사 스크립트 `validate-post-kaizen.py` · `validate-doc-contracts.py` 를 실제로 돌린 출력이다. 뒤따르는 대조 명령은 그 출력에서 경로를 뽑아 `mine` 과 겹침을 셀 뿐이다
- 커버리지 해소: SK-04 · ER-02 — 산문의 `skill-design-guide.md` · `agent-design-guide.md` 는 측정의 `"$T/s.md"` · `"$T/a.md"` 다. 공통 정의가 두 파일의 `$END` 판을 그 이름으로 꺼낸다
- 커버리지 해소: ER-04 — 산문의 넘김 경로 8 개와 키 3 개는 측정의 `for t in …` 한 줄이 같은 11 문자열을 하나씩 notes 에서 `grep -cF` 한다(검출기는 공백 든 코드 조각 안의 경로를 읽지 못한다). 편집 금지 다섯 파일은 `mine | grep -cE …` 정규식이 덮는다 — 펼치면 `harness/skills/sprint/SKILL.md` · `harness/skills/create-agent/SKILL.md` · `harness/skills/create-skill/SKILL.md` · `harness/agents/qa-evaluator.md` · `harness/docs/guides/qa-evaluation-guide.md`. notes 경로는 `test -f` 와 루프가 읽는 파일이다
- 커버리지 해소: AR-03 — (a) (b) 의 문자열 16 개(`2.1.198` · `2.1.281` · `2026-09-24 조회` 포함)는 측정 절의 「각 문자열을 `grep -cF` 로」가 하나씩 덮는다
- 편집 전부터 있던 markdownlint 경고 7 개는 범위 밖이다 — skill `:7` MD025 · `:470` MD024, agent `:7` MD025 · `:498` · `:504` · `:638` MD024 · `:512` MD032
- 조건 25 줄 중 5 줄이 `N/A (사유)` 라 기능 조건은 20 개다 — 파일은 2 개지만 고치는 자리가 15 곳이 넘고, 번호 인용이 다른 파일 5 곳에, 옛 문구 사본이 다른 킷 5 곳에 걸려 있다
- 사용자 승인(Step 5) 대체: 사용자가 「자동으로 끝까지 알아서 진행해 내 허락이 필요한건 코덱스로 리서치나 검토받고」라고 위임했다(세션 `de8c7935-a5b6-4df5-9106-fafa73c288a0` 기록 queued_command `2026-09-24T04:04:16.964Z`). Codex 사용량 한도가 소진돼(오류 원문 「You've hit your usage limit … try again at 11:05 PM」, 2026-09-24) 독립 Claude 검토자가 대신한다. 검토 결과 파일: `.harness/.meta/kaizen-0924/phase1-review.md` · 1 차 VERDICT: CHANGES (막는 이유 다섯 · 권고 넷) — 이 초안에 반영했다. 2 차(마지막) VERDICT: CHANGES (막는 이유 둘 · 권고 둘)
- 2 차 검토 반영 (BUILD, 봉인 전): 막는 이유 둘은 검토자가 적은 문구 그대로 넣었다 — AR-02 에 `세는 대상` 토큰과 §12 측정 · 음성 대조, AR-03 (a) 에 `상한이 3 종` (개선안 §7 줄 · 봉인 전 실측 표 · 커버리지 해소 16 개도 같이). 권고 둘도 넣었다 — SK-04 (d) 의 새 개수 세 측정을 「1 이상」으로, 서명 줄 `Kaizen-Phase:` 를 FIX 가 빠뜨리지 않게 notes 에 한 줄. 3 차 검토는 돌리지 않았다 — 2 차 검토가 「이 두 가지만 들어가면 나머지는 이대로 봉인해도 된다」고 적었고, 바뀐 측정의 편집 전 값은 BUILD 가 봉인 전에 다시 쟀다(`봉인 전 실측` 표)

## 회귀 게이트 — 측정 공통 정의와 봉인 전 실측

모든 조건의 측정은 아래 블록을 먼저 실행한 **bash** 셸에서 돈다 — 블록과 측정을 한 `bash -c` 안에 넣거나 블록을 파일로 저장해 `. 파일` 뒤에 잇는다. `END_UNRESOLVED` 가 찍히면 셸이 종료 코드 2 로 끝난다.

```bash
# 측정 공통 정의 — bash 로 실행한다 (zsh 에서 source 하지 마라)
export LC_ALL=C.UTF-8   # 번역투 정규식의 `서?` 가 글자 단위로 돌아야 한다 — C 로케일이면 조용히 0 이 된다
cd /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/kaizen-0924 || exit 2
B=7689fde6efdaa2401e90689dd15dd16baf8d59a0                  # 이 Phase 시작 HEAD
AM=.harness/sprint-amendments-kaizen-0924-p01-guides.md
END=$( [ -f "$AM" ] && sed -n 's/^end_sha:[[:space:]]*//p' "$AM" | tail -1 )
if [ -z "$END" ] || ! git rev-parse -q --verify "$END^{commit}" >/dev/null; then
  echo "END_UNRESOLVED — 측정을 멈추고 BUILD 에 묻는다. HEAD 로 바꿔 재지 않는다"; exit 2   # return 을 쓰면 source 한 쪽이 계속 돈다 (실측)
fi
S=harness/docs/guides/skill-design-guide.md; A=harness/docs/guides/agent-design-guide.md
T=$(mktemp -d)
git show "$B:$S" > "$T/s0.md"; git show "$B:$A" > "$T/a0.md"
git show "$END:$S" > "$T/s.md"; git show "$END:$A" > "$T/a.md"
sec5()   { awk '/^### 스킬이 지켜야 할 5 조항/{f=1;next} f&&/^#### /{exit} f' "$T/s.md"; }
cl()     { sec5 | awk -v n="$1" 'BEGIN{a="^" n "\\. \\*\\*"; b="^" (n+1) "\\. \\*\\*"} $0~a{f=1} $0~b{f=0} f'; }
ka()     { awk '/^#### .*알려진 답/{f=1;print;next} f&&/^##/{exit} f' "$T/s.md"; }
ledger() { awk '/^#### 등급 원장/{f=1;next} f&&/^#### /{exit} f' "$T/s.md" | grep -E '^\| ' | grep -vE '^\|[-: |]+\|$' | tail -n +2; }
par()    { awk '/^### 전수 대상 parity items/{f=1;print;next} f&&/^### /{exit} f' "$1"; }
rows()   { par "$1" | grep -oE '^\| [0-9]+ \|' | tr -dc '0-9\n'; }
pol()    { awk '/^- \*\*Unverifiable 조건 정책/{f=1} f&&/^- \*\*사용자 실패 보고 우선/{exit} f' "$T/a.md"; }
fmset()  { awk '/^### frontmatter 전체 필드/{f=1;next} f&&/^(###|##|---)/{exit} f' "$T/a.md" | grep -E '^\| `' | sed -E 's/^\| `([A-Za-z]+)`.*/\1/' | sort; }
url()    { grep -oE 'https?://[^ )>"`]+' | sed -E 's/[.,;:]+$//' | sort -u; }
added()  { git diff -U0 "$B" "$END" -- "$S" "$A" | grep '^+' | grep -v '^+++'; }
mine()   { git log --format= --name-only "$B..$END" --grep='^Kaizen-Phase: kaizen-0924-p01-guides$' | grep . | sort -u; }   # 서명 줄만 — 본문에 슬러그를 인용한 다른 Phase 커밋은 안 잡힌다 (실측)
K02='(을|를) ?(처리|관리)(합니다|한다)|에 대해서?|하도록 (합니다|한다)|에 의(해|하여)|되어 있(는 경우|을 때)|(표시|적용|호출|생성|반환)(됩니다|된다)'
```

ER-03 이 재는 옛 서술 8 개 (편집 전 값: 1 · 2 · 1 · 1 · 1 · skill 0 + agent 1 · 1 · 1):

```bash
grep -cF '`[정적]` 또는 `[미검증]` 마커' "$T/a.md"
grep -cF '2 건 임계값은 양쪽이 동일' "$T/a.md"
grep -cF '`[미검증]` 마커와 사유 한 줄' "$T/s.md"
grep -cF '`[미검증]` 마커 · 2 건 임계' "$T/s.md"
grep -cF '`[미검증]` 마커 · 2건 누적 REJECT' "$T/a.md"
grep -cF 'fit-pal' "$T/s.md" "$T/a.md"
grep -cF 'Good: 검증 불가 → "[미검증] MCP 미설정 — 시각 대조 불가" 명시 → 부분 완료로 보고' "$T/s.md"
grep -cF '마커·임계값은 agent-design-guide §10' "$T/s.md"
```

AP-03 이 쓰는 펜스 검출기 (`python3 fence.py "$T/s.md" "$T/a.md"`):

```python
import re, sys
# 여는 펜스에 언어 힌트가 없으면 bare. 4-백틱 바깥 펜스 안의 ``` 는 내용으로 본다
tot_bare = tot_unclosed = 0
for path in sys.argv[1:]:
    open_len = 0; open_ch = ''; bare = []
    for n, line in enumerate(open(path, encoding='utf-8'), 1):
        m = re.match(r'^\s*(`{3,}|~{3,})(.*)$', line.rstrip('\n'))
        if not m:
            continue
        run, rest = m.group(1), m.group(2).strip()
        if open_len == 0:
            open_len, open_ch = len(run), run[0]
            if not rest:
                bare.append(n)
        elif run[0] == open_ch and len(run) >= open_len and not rest:
            open_len = 0
    tot_bare += len(bare); tot_unclosed += 1 if open_len else 0
    print(f"{path}: bare_open={len(bare)} {bare} unclosed={1 if open_len else 0}")
print(f"bare_open_total={tot_bare} unclosed_total={tot_unclosed}")
```

DG-02 가 쓰는 새 경고 계산기. 스크래치 폴더에 `npm install --no-save markdownlint-cli2@0.23.2`, 같은 폴더에
`cfg.markdownlint-cli2.jsonc` = `{ "config": { "MD013": false } }` (편집기 확장이 MD013 을 끈 것과 같은 조건):

```bash
#!/usr/bin/env bash
# new-warnings.sh <옛 파일> <새 파일> — 새 파일에서 더한 줄에 걸린 경고만 센다. 줄이 밀리므로 전체 수 차이로 세지 않는다
set -u
DIR=$(cd "$(dirname "$0")" && pwd)
ADDED=$(git diff --no-index -U0 -- "$1" "$2" | awk '/^@@/{split($3,a,","); s=substr(a[1],2)+0; n=(a[2]==""?1:a[2]+0); for(i=0;i<n;i++) print s+i}' | sort -u)
OUT=$("$DIR/node_modules/.bin/markdownlint-cli2" --config "$DIR/cfg.markdownlint-cli2.jsonc" "$2" 2>&1)
LINES=$(printf '%s\n' "$OUT" | grep -E '^[^ ]*:[0-9]+' | sed -E 's#^[^ ]*:([0-9]+).*#\1#' | sort -u)
NEWW=$(comm -12 <(printf '%s\n' "$ADDED" | grep . | sort) <(printf '%s\n' "$LINES" | grep . | sort) | wc -l | tr -d ' ')
echo "total_warning_lines=$(printf '%s\n' "$LINES" | grep -c .) added_lines=$(printf '%s\n' "$ADDED" | grep -c .) new_warnings=$NEWW"
```

봉인 전 실측 (2026-09-24 19:4x 초안, 1 차 검토 반영 뒤 20:1x 에 다시 돌림 — 편집 전 파일 = `$B` 를 `END` 자리에 넣어 돌림.
공통 정의와 ER-03 블록 · `fence.py` · `new-warnings.sh` 는 이 계약 본문에서 잘라 그대로 실행했다):

```text
[SK-01] 9 토큰 전부 0 · Good 줄 0 · 요약 행 0
[SK-02] 알려진 답 헤더 0 · §3.7 구간 안 0
[SK-03] 원장 이름 차이 = 0 기대 양성 대조; 알려진 답 대조 · 빈 칸 행 0 · 새 행 E2 0 · CEG 네 칸 0
[SK-04] skill 행 1..14 · (16개) 0 · r15 0 · r16 0 · r5 네 칸 0 · 없는 인용 = 15 · agent 행 1..9 · (10개) 0 · r10 0
        (d) 아래 14개 항목 1 · (1~6, 9~11, 14) 1 · 아래 9개 항목 1 · 아래 16개 항목 0 · 아래 10개 항목 0 · §11 parity 표 16 번째 0
[ER-01] 근거 밖 새 URL 0 · 양성 대조(example.invalid 1 개 + 근거 안 URL 1 개 더한 사본) 1
[ER-02] 조항 5 · 3 항 「2 건 이상」 1 · 「부분 완료」 1 · 4 항 「검증 실패 신호」 1 · 정책 번호 항목 4
[ER-03] 1 · 2 · 1 · 1 · 1 · (0, 1) · 1 · 1
[ER-04] notes 파일 없음 (구현이 만들 파일 — 면제) · 가짜 notes 11 값 전부 1, 한 줄 지우면 그 값 0
        qa-evaluator.md:65 네 요건 토큰 4 · qa-evaluation-guide.md:1874 Zero-Result 1
[ER-05] 더한 줄 0 · 양성 대조(「훅에 의해 적용된다」 · 「그것에 대해 말한다」 두 줄) UTF-8 2 · C 로케일 1
[AR-01] 차집합 3 (experimental · initialPrompt · omitClaudeMd) · initialPrompt 행 0 · 미확인 0 · 불릿 1 · 15 종 4 · 18 종 0
[AR-02] 2 건 1, 나머지 10 토큰(규칙 11 · env_gaps · 세는 대상 포함) 0 · 요약 행 0 · §12 세는 대상 0
[AR-03] (a) agent 1 1 1 1 2 1 1 / skill 1 2 2 · (b) agent 0 0 0 0 0 / skill 0 (날짜 토큰은 `2026-09-24 조회`) · (c) 0 0
[AR-04] ① 0 커밋 · ② 0 · 0 (빈 `mine`) — 가짜 목록: 두 가이드 + .harness/ 세 줄 0 · 2, sprint 섞임 + 가이드 하나 빠짐 1 · 1
        서명 줄 가림: 스크래치 저장소에서 본문에 같은 글자를 인용한 커밋은 `grep -cxF` 0 · `mine` 에 안 잡힘, 서명 줄 커밋 1
        ③ SEAL_ABSENT 11 · SEAL_OK 50 · SEAL_BROKEN 0 · 이 Phase 몫 0
           양성 대조(사본 둘, 하나 조건 줄 변경) SEAL_BROKEN 1 · 이 Phase 몫: mine 에 없음 0 / 있음 1 / 이 계약 경로 1
[AP-01] 0 · 양성 대조(9.9.9 · v2.1.198 · version: 7.7.7 더한 사본) 1
[AP-03] bare_open_total=0 unclosed_total=0 · 양성 대조(언어 힌트 없는 펜스 더한 사본) bare_open_total=1
        text 아닌 여는 펜스(더한 줄) 0 · 양성 대조(text 블록 1 + bash 블록 1 더한 사본) 1
[RE-02] 표 구분줄 skill 13 · agent 9
[DG-02] 두 파일 new_warnings=0 (전체 경고 줄 skill 2 · agent 5) · 양성 대조(빈 줄 없는 헤더 · 목록 4 줄) new_warnings=3
[DG-05] 두 가이드 FAIL 0 · 양성 대조(스크래치 복사본에 헤더 없는 표 행 2 개) 2 — 1 차 검토 재실측 1, 기준은 1 이상
[DG-06] 15 checks — 12 PASS / 0 FAIL / 0 ERROR / 3 SKIP (scope-isolation PASS · doc-contracts PASS · docs-site-regen SKIP)
        doc-contracts 대조: 경로 2 개(.claude/skills/kaizen-orchestrator/SKILL.md · scripts/collect-kaizen-data.py) · 빈 mine 겹침 0 · 가짜 mine 1
[DG-07] skill 1.5.0 · 2026-08-13 / agent 1.6.0 · 2026-08-13
[SC-00 · RE-01 · DG-01] 0 · 0 · 0
```

모의 편집본(검토 반영 개선안을 그대로 따른 두 가이드 사본, 가짜 `mine` = 두 가이드 + `.harness/` 세 줄)에서 25 조건을 한꺼번에
돌렸다: 전부 통과 — SK-04 (d) 0 · 0 · 0 · 1 · 1 · 1, AR-02 10 토큰 전부 1 이상(`2 건` 2), AR-03 (b) agent 1 1 1 1 5 / skill 3,
ER-03 8 개 전부 0, ER-05 0, 펜스 0/0, 새 경고 0/0, 표 구분줄 13/9. 조건끼리 서로 막는 곳은 없다.
2 차 검토가 모의본 두 벌을 더 돌렸다 — `같은 2 건 임계` 를 되살린 본은 AR-02 의 `세는 대상` 이 0 · 0, 「상한이 3 종」을
되살린 본은 AR-03 (a) 의 `상한이 3 종` 이 1 로 떨어진다(좋은 모의본은 `세는 대상` 1 · 1, `상한이 3 종` 0). 이 두 측정은 2 차
검토 뒤에 더했다.

## Skill

- [ ] SK-01: `skill-design-guide.md` §3.7 「스킬이 지켜야 할 5 조항」 3 항이 검증 불가 보고를 네 칸으로 적게 하고, 작업 자체를 못 한다고 결론 내리기 전에도 같은 네 칸을 요구한다 — 3 항 구간에 9 토큰 `막는 것` · `시도한 우회` · `하나 이상` · `통제 불가 사유` · `재검증 명령` · `네 칸` · `작업 자체` · `[미검증:ENV]` · `[미검증:INVALID]` 가 각각 1 건 이상 있고, 5 조항 절의 `Good:` 줄 가운데 `시도한 우회` 를 담은 줄이 1 개 이상, 요약 표 `| **Completion Evidence Gate** |` 행에 `네 칸` 이 있다 [exact, enumerated]
      (측정: `for t in '막는 것' '시도한 우회' '하나 이상' '통제 불가 사유' '재검증 명령' '네 칸' '작업 자체' '[미검증:ENV]' '[미검증:INVALID]'; do printf '%s=%s\n' "$t" "$(cl 3 | grep -cF "$t")"; done` 9 값이 전부 1 이상 ·
       `sec5 | grep -F 'Good:' | grep -cF '시도한 우회'` 1 이상 · `grep -F '| **Completion Evidence Gate** |' "$T/s.md" | grep -cF '네 칸'` 1. 봉인 전 실측: 전부 0)
- [ ] SK-02: `skill-design-guide.md` §3.7 에 헤더에 `알려진 답` 을 담은 `####` 소절이 정확히 1 개 있고, 0 이 아닌 값을 내는 새 측정 스크립트에 손으로 답을 셀 수 있는 작은 입력을 먼저 돌려 기대값과 실제값을 나란히 적게 한다 — 소절 구간에 7 토큰 `기대값` · `실제값` · `0 이 아닌` · `레포 관례` · `KSH_ARRAYS` · `zsh.sourceforge.io` · `현재 등급: E2` 가 각각 1 건 이상 [exact, enumerated]
      (측정: `grep -cE '^#### .*알려진 답' "$T/s.md"` 1 · `awk '/^## 3\.7\./{f=1;next} f&&/^## /{exit} f&&/^#### .*알려진 답/{c++} END{print c+0}' "$T/s.md"` 1 (그 하나가 `## 3.7.` 구간 안에 있다) · `for t in 기대값 실제값 '0 이 아닌' '레포 관례' KSH_ARRAYS zsh.sourceforge.io '현재 등급: E2'; do printf '%s=%s\n' "$t" "$(ka | grep -cF "$t")"; done` 7 값 전부 1 이상. 봉인 전 실측: 헤더 0 · §3.7 구간 안 0)
- [ ] SK-03: `skill-design-guide.md` §3.7 `#### 등급 원장` 표의 행 이름 집합이 기존 8 개(`Enumerate-before-Act` · `Pre-Edit Batch Audit` · `Rule-by-Rule Audit` · `Scope-Bound Edits` · `Completion Evidence Gate` · `Counterpart Enumeration` · `Variant Budget` · `User-Reported Failure Gate`)에 `0 기대 양성 대조` · `알려진 답 대조` 를 더한 10 개와 정확히 같고, 모든 행이 4 칸을 다 채우며, 새 두 행의 현재 등급 칸에 `E2` 가 있고, `Completion Evidence Gate` 행에 `네 칸` 이 있다 [exact, enumerated]
      (측정: `comm -3 <(ledger | awk -F'|' '{g=$2; gsub(/^ +| +$/,"",g); print g}' | sort) <(printf '%s\n' 'Enumerate-before-Act' 'Pre-Edit Batch Audit' 'Rule-by-Rule Audit' 'Scope-Bound Edits' 'Completion Evidence Gate' 'Counterpart Enumeration' 'Variant Budget' 'User-Reported Failure Gate' '0 기대 양성 대조' '알려진 답 대조' | sort) | grep -c .` 0 ·
       `ledger | awk -F'|' '{e=0; for(i=2;i<=5;i++){g=$i; gsub(/ /,"",g); if(g=="") e++} if(NF!=6||e) print}' | grep -c .` 0 ·
       `ledger | grep -E '^\| (0 기대 양성 대조|알려진 답 대조) \|' | awk -F'|' '{print $4}' | grep -c E2` 2 · `ledger | grep -F 'Completion Evidence Gate' | grep -cF '네 칸'` 1.
       봉인 전 실측: 이름 차이 2 개(새 두 이름) · 빈 칸 행 0 · 새 행 E2 0 · 네 칸 0)
- [ ] SK-04: 두 가이드의 parity 표(같은 원칙을 두 가이드가 짝으로 갖는지 적은 표)가 번호 빈칸 없이 이어지고 머리줄 개수가 실제 행 수와 같다 — (a) `skill-design-guide.md` §11 표 행 번호가 정확히 1~16, 머리줄에 `(16개)`, 15 행에 `Zero-Result Positive Control`, 16 행에 `알려진 답 대조`, 5 행에 `네 칸` (b) 그 파일 안 「§11 parity 표 N 번째」 인용의 N 이 전부 표에 있다 (c) `agent-design-guide.md` §12 표 행 번호가 정확히 1~10, 머리줄에 `(10개)`, 10 행에 `Zero-Result Positive Control` (d) 표 위아래 문장에 옛 개수가 남지 않고 새 개수를 적는다 — skill `아래 14개 항목` · `(1~6, 9~11, 14)` 와 agent `아래 9개 항목` 이 0 건, skill `아래 16개 항목` · agent `아래 10개 항목` 이 1 건 이상, 새 소절이 같은 꼴로 인용해 skill 에 `§11 parity 표 16 번째` 가 1 건 이상 [exact, enumerated]
      (측정: `[ "$(rows "$T/s.md" | tr '\n' ' ')" = "$(seq 1 16 | tr '\n' ' ')" ]` 참 · `par "$T/s.md" | head -1 | grep -cF '(16개)'` 1 · `par "$T/s.md" | grep -E '^\| 15 \|' | grep -cF 'Zero-Result Positive Control'` 1 · 같은 형태로 16 행 `알려진 답 대조` 1 · 5 행 `네 칸` 1 ·
       `comm -23 <(grep -oE '§11 parity 표 [0-9]+ 번째' "$T/s.md" | sed -E 's/.*표 ([0-9]+) 번째/\1/' | sort -u) <(rows "$T/s.md" | sort -u) | grep -c .` 0 ·
       `[ "$(rows "$T/a.md" | tr '\n' ' ')" = "$(seq 1 10 | tr '\n' ' ')" ]` 참 · `par "$T/a.md" | head -1 | grep -cF '(10개)'` 1 · `par "$T/a.md" | grep -E '^\| 10 \|' | grep -cF 'Zero-Result Positive Control'` 1 ·
       (d) `grep -cF '아래 14개 항목' "$T/s.md"` 0 · `grep -cF '(1~6, 9~11, 14)' "$T/s.md"` 0 · `grep -cF '아래 9개 항목' "$T/a.md"` 0 · `grep -cF '아래 16개 항목' "$T/s.md"` 1 이상 · `grep -cF '아래 10개 항목' "$T/a.md"` 1 이상 · `grep -cF '§11 parity 표 16 번째' "$T/s.md"` 1 이상.
       봉인 전 실측: skill 1~14 · 없는 인용 15 (측정이 편집 전 결함을 1 로 잡는다) · agent 1~9 · (d) 1 · 1 · 1 · 0 · 0 · 0 · 나머지 0)

## Script

- [ ] SC-00: N/A (Script 카테고리는 `release.sh` 연동 · 버전 올림 · `marketplace.json` 갱신이다. 이 Phase 는 그 파일을 건드리지 않는다 — 공유 파일은 Final 몫. 측정: `mine | grep -cE '^(scripts/release\.sh|\.claude-plugin/marketplace\.json|[^/]+/\.claude-plugin/plugin\.json)$'` 이 0)

## Error

- [ ] ER-01: 두 가이드에 새로 생긴 URL 이 전부 이 Phase 의 외부 근거 파일 `.harness/.meta/evidence/phase1.md` 에 있다 — 근거 밖 자료를 인용하지 않았다 [exact, enumerated]
      (측정: `comm -23 <(comm -13 <(cat "$T/s0.md" "$T/a0.md" | url) <(cat "$T/s.md" "$T/a.md" | url)) <(url < .harness/.meta/evidence/phase1.md) | grep -c .` 0.
       양성 대조: 편집 전 agent 가이드 사본 끝에 `https://example.invalid/x` 와 근거 안 URL 하나를 더해 같은 비교를 돌리면 1 — 봉인 전 실측 1)
- [ ] ER-02: 다른 파일이 인용하는 번호가 편집 뒤에도 같은 내용을 가리킨다 (Counterpart 소비면 보존) — (a) `skill-design-guide.md` §3.7 5 조항의 번호 항목이 정확히 5 개 (b) 3 항에 `2 건 이상` 과 `부분 완료` 가 남아 있다 (c) 4 항에 `검증 실패 신호` 가 남아 있다 (d) `agent-design-guide.md` §10 「Unverifiable 조건 정책」 번호 항목이 정확히 4 개. 이 번호를 인용하는 5 곳은 `GAP 분석` 절 Counterpart 표에 있다 [exact, enumerated]
      (측정: `sec5 | grep -cE '^[0-9]+\. \*\*'` 5 · `cl 3 | grep -cF '2 건 이상'` 1 이상 · `cl 3 | grep -cF '부분 완료'` 1 이상 · `cl 4 | grep -cF '검증 실패 신호'` 1 이상 · `pol | grep -cE '^  [0-9]\. \*\*'` 4. 봉인 전 실측: 5 · 1 · 1 · 1 · 4)
- [ ] ER-03: `회귀 게이트` 절에 적은 옛 서술 8 개(`[정적]` 을 `[미검증]` 과 나란한 마커로 적은 문장 · 「2 건 임계값은 양쪽이 동일」 · 「마커와 사유 한 줄」 · §11 5 행 「2 건 임계」 · agent 요약 「2건 누적 REJECT」 · 특정 앱 이름 `fit-pal` · 옛 Good 예시 줄 · skill 3 항의 `마커·임계값은 agent-design-guide §10` (동일 규약 주장))가 두 가이드에 하나도 남지 않는다 [exact, enumerated]
      (측정: `회귀 게이트` 절 ER-03 코드 블록의 8 명령이 전부 0 — `fit-pal` 줄은 두 파일 모두 0. 봉인 전 실측: 1 · 2 · 1 · 1 · 1 · (0, 1) · 1 · 1 — 8 개 모두 편집 전 파일에서 잡히므로 측정이 살아 있다)
- [ ] ER-04: Counterpart 소비면 가운데 이 Phase 범위 밖이라 못 고치는 8 곳을 명시적 미완으로 넘기고, 이미 맞는 2 파일은 건드리지 않는다 — `.harness/.meta/kaizen-0924/phase1-notes.md` 에 `harness/skills/sprint/SKILL.md:77` · `harness/skills/create-agent/SKILL.md` · `harness/skills/create-skill/SKILL.md:24` · `react-kit/references/render-evidence-protocol.md:59` · `flutter-toolkit/references/visual-evidence-protocol.md:136` · `onboarding-kit/skills/setup-guide/SKILL.md:30` · `infra-kit/skills/infra-test/SKILL.md:37` · `rust-kit/agents/rust-reviewer.md:137` 과 처리 배정표 키 `F10` · `harness:P09` · `harness:P05` 가 각각 1 회 이상 있고, 이 Phase 커밋이 다섯 파일(`harness/skills/sprint/SKILL.md` · `harness/skills/create-agent/SKILL.md` · `harness/skills/create-skill/SKILL.md` · `harness/agents/qa-evaluator.md` · `harness/docs/guides/qa-evaluation-guide.md`)을 하나도 건드리지 않는다 [exact, enumerated]
      (Given: BUILD 가 notes 를 쓰고 커밋한 뒤 · 측정: `test -f .harness/.meta/kaizen-0924/phase1-notes.md` exit 0 ·
       `for t in harness/skills/sprint/SKILL.md:77 harness/skills/create-agent/SKILL.md harness/skills/create-skill/SKILL.md:24 react-kit/references/render-evidence-protocol.md:59 flutter-toolkit/references/visual-evidence-protocol.md:136 onboarding-kit/skills/setup-guide/SKILL.md:30 infra-kit/skills/infra-test/SKILL.md:37 rust-kit/agents/rust-reviewer.md:137 F10 harness:P09 harness:P05; do printf '%s=%s\n' "$t" "$(grep -cF "$t" .harness/.meta/kaizen-0924/phase1-notes.md)"; done` 11 값 전부 1 이상 ·
       `mine | grep -cE '^harness/(skills/(sprint|create-agent|create-skill)/SKILL\.md|agents/qa-evaluator\.md|docs/guides/qa-evaluation-guide\.md)$'` 0.
       봉인 전 실측: notes 없음 — 구현이 만들 파일이라 면제. 11 문자열을 담은 가짜 notes 로 돌리면 11 값 전부 1, 한 줄을 지우면 그 값이 0. 이미 맞다는 근거: `qa-evaluator.md:65` 에 `1 차 도구 시도` · `fallback 시도` · `실패 로그` · `재검증 명령` 각 1, `qa-evaluation-guide.md:1874` 에 `Zero-Result Positive Control` 1)
- [ ] ER-05: 두 가이드에 더한 줄에 번역투 6 종(`tone-kit/references/locale-korean.md` §2 치환표의 grep 열)이 0 건이다 [exact]
      (측정: `added | grep -cE "$K02"` 0. 양성 대조: 편집 전 skill 사본에 「이 값은 훅에 의해 적용된다.」 · 「그것에 대해 말한다.」 두 줄을 더하면 2 — 봉인 전 실측 UTF-8 2 · C 로케일 1. 1 이 나오면 로케일이 틀린 것이라 측정 무효)

## Architecture

- [ ] AR-01: `agent-design-guide.md` §2 「frontmatter 전체 필드」 표의 필드 이름 집합이 공식 18 종(`name` `description` `tools` `disallowedTools` `model` `permissionMode` `maxTurns` `skills` `mcpServers` `hooks` `memory` `background` `effort` `isolation` `color` `omitClaudeMd` `initialPrompt` `experimental`)과 양방향 차집합 0 이다. `initialPrompt` 행에 `플러그인` 이 있고, `omitClaudeMd` · `experimental` 두 행에 `미확인` 이 있다(근거 파일은 이름만 확인했다 — 뜻을 지어내지 않는다). 「표에 없는 이름들」에 `initialPrompt` 불릿이 없고, 파일 전체에 `15 종` 0 건 · `18 종` 2 건 이상 [exact, enumerated]
      (측정: `comm -3 <(fmset) <(printf '%s\n' name description tools disallowedTools model permissionMode maxTurns skills mcpServers hooks memory background effort isolation color omitClaudeMd initialPrompt experimental | sort) | grep -c .` 0 ·
       ``grep -E '^\| `initialPrompt`' "$T/a.md" | grep -cF 플러그인`` 1 · ``grep -E '^\| `(omitClaudeMd|experimental)`' "$T/a.md" | grep -cF 미확인`` 2 · ``grep -cE '^- \*\*`initialPrompt`\*\*' "$T/a.md"`` 0 · `grep -cF '15 종' "$T/a.md"` 0 · `grep -cF '18 종' "$T/a.md"` 2 이상.
       봉인 전 실측: 차집합 3 · 0 · 0 · 1 · 4 · 0)
- [ ] AR-02: `agent-design-guide.md` §10 「Unverifiable 조건 정책」 구간이 평가 측 분류와 같은 말을 쓴다 — 11 토큰 `[미검증:ENV]` · `[미검증:INVALID]` · `막는 것` · `시도한 우회` · `통제 불가 사유` · `재검증 명령` · `네 칸` · `2 건` · `규칙 11` · `env_gaps` · `세는 대상` 이 각각 1 건 이상이고, 요약 표 `| **Unverifiable 정책** |` 행에 `네 칸` 이 있으며, §12 parity 절에도 두 쪽의 2 건 기준은 `세는 대상` 이 다르다고 적혀 있다 [exact, enumerated]
      (측정: `for t in '[미검증:ENV]' '[미검증:INVALID]' '막는 것' '시도한 우회' '통제 불가 사유' '재검증 명령' '네 칸' '2 건' '규칙 11' env_gaps '세는 대상'; do printf '%s=%s\n' "$t" "$(pol | grep -cF "$t")"; done` 11 값 전부 1 이상 · `grep -F '| **Unverifiable 정책** |' "$T/a.md" | grep -cF '네 칸'` 1 · `par "$T/a.md" | grep -cF '세는 대상'` 1 이상. 봉인 전 실측: `2 건` 1 · 나머지 10 토큰 0 · 요약 행 0 · §12 0. 음성 대조: 두 자리를 「같은 네 칸 · 같은 2 건 임계」로 쓴 모의본은 `세는 대상` 0 · 0)
- [ ] AR-03: 근거 파일 §3 의 낡은 곳이 두 가이드에서 고쳐진다 — (a) 0 이어야 하는 10 문자열: agent `CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION` · `세션 200` · `세션 누적 200` · ``모델 `haiku` 로`` · `2026-04 최신` · `sub-agents) (2026-04)` · `상한이 3 종`, skill `2026-04 최신` · `best-practices) (2026-04)` · `500 라인 상한` (b) 1 이상이어야 하는 6 문자열: agent `CLAUDE_CODE_SUBAGENT_MODEL` · `2.1.198` · `2.1.281` · `세션 전체 스폰 수에는 상한이 없다` · `2026-09-24 조회`, skill `2026-09-24 조회` — 날짜는 머리 설정 `last_updated` 만으로 채워지지 않게 본문 표기 꼴로 잰다 (c) skill 의 500 라인 헤더와 요약 행에 `권고` [exact, enumerated]
      (측정: (a) (b) 는 각 문자열을 `grep -cF` 로 `"$T/a.md"` · `"$T/s.md"` 에서 잰다 · (c) `grep -E '^### SKILL.md 본문 500 라인' "$T/s.md" | grep -c 권고` 1 · `grep -E '^\| 500 라인' "$T/s.md" | grep -c 권고` 1.
       봉인 전 실측: (a) agent 1 · 1 · 1 · 1 · 2 · 1 · 1 / skill 1 · 2 · 2 (b) 전부 0 (c) 0 · 0)
- [ ] AR-04: 이 Phase 의 변경이 허용 경로 안에 머문다 [exact, enumerated]
      (Given: BUILD 가 개정 파일에 `end_sha:` 를 적은 뒤 · 이 Phase 커밋 메시지마다 서명 줄 `Kaizen-Phase: kaizen-0924-p01-guides` · 측정 셋 —
       ① `git log --format=%H "$B..$END" -- "$S" "$A"` 가 내는 커밋마다 `git log -1 --format=%B <커밋> | grep -cxF 'Kaizen-Phase: kaizen-0924-p01-guides'` 가 1 이상 (다른 Phase 가 두 가이드를 건드리지 않았고 구현 커밋이 서명 줄을 달았다)
       ② `.harness/` 밖은 두 가이드뿐이다 — `mine | grep -vE '^(\.harness/|harness/docs/guides/(skill|agent)-design-guide\.md$)' | grep -c .` 0 · `mine | grep -cxE 'harness/docs/guides/(skill|agent)-design-guide\.md'` 2. `.harness/` 는 슬러그를 나열하지 않고 ③ 으로 잰다
       ③ `harness/references/contract-schema.md` §`.harness/` 범위 조건 의 권장 형태 — `find .harness -type f -name 'sprint-contract*.md' -print0 | while IFS= read -r -d '' f; do verify_seal "$f"; done | awk '{print $1}' | sort | uniq -c` 를 근거로 남기고 (`fm_get` · `sha256_16` · `contract_digest` · `verify_seal` 은 그 문서 정의 그대로), 그 가운데 이 Phase 몫인 `SEAL_BROKEN` 이 0 개 —
          `find .harness -type f -name 'sprint-contract*.md' -print0 | while IFS= read -r -d '' f; do verify_seal "$f"; done | awk '$1=="SEAL_BROKEN"{print $2}' | sort -u | comm -12 - <( { mine; echo .harness/sprint-contract-kaizen-0924-p01-guides.md; } | sort -u) | grep -c .` 0.
          `SEAL_BROKEN` 줄의 파일이 `mine` 에도 없고 이 계약도 아니면 다른 Phase 몫이다 — 파일 이름을 근거에 적고 이 조건에는 세지 않는다.
       봉인 전 실측: ① 0 커밋 ② 0 · 0 (`mine` 이 빈 목록) — 가짜 목록으로 돌림: 두 가이드 + `.harness/` 세 줄이면 0 · 2, `harness/skills/sprint/SKILL.md` 가 섞이고 가이드 하나가 빠지면 1 · 1
          ③ SEAL_ABSENT 11 · SEAL_OK 50 · SEAL_BROKEN 0 · 이 Phase 몫 0 — 양성 대조(스크래치 폴더의 `.harness/` 에 봉인된 계약 사본 둘, 하나는 조건 줄 한 글자 변경): SEAL_BROKEN 1 · 이 Phase 몫은 그 사본이 `mine` 에 없으면 0, 있으면 1, 사본 이름을 이 계약 경로로 바꾸면 `mine` 이 비어도 1)

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다. 이번 변경에 적용: 두 가이드에 더한 줄의 버전꼴 문자열(`x.y.z`)이 머리 설정 `version:` 줄과 근거 파일에 있는 `2.1.198` · `2.1.281` 말고 0 건이다 [exact]
      (측정: `added | grep -v '^+version:' | grep -oE 'v?[0-9]+\.[0-9]+\.[0-9]+' | sed 's/^v//' | sort -u | grep -vxF -e 2.1.198 -e 2.1.281 | grep -c .` 0. 양성 대조: 편집 전 사본에 `9.9.9` · `v2.1.198` · `version: 7.7.7` 을 더하면 1 (`9.9.9` 만) — 봉인 전 실측 1)
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```` ```text, ```bash, ```yaml ```` 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 이번 변경에 적용: 설정 명령 `python3 scripts/validate-plugin.py --check=code-fence` 는 `harness/docs/guides/` 를 읽지 않으므로(`scripts/validate-plugin.py:516-520`) 같은 판정에 펜스 길이를 더한 검출기로 두 가이드를 잰다. 그리고 더한 줄에 `text` 말고 다른 언어의 여는 펜스가 0 건이다 — 새 셸 스니펫을 넣지 않는다 (넣으면 qa-evaluator 규칙 10 (5) 로 두 셸 실행 대상이 된다) [exact]
      (측정: `회귀 게이트` 절의 `fence.py` 를 `"$T/s.md" "$T/a.md"` 에 돌려 `bare_open_total=0 unclosed_total=0` · `added | grep -E '^\+[[:space:]]*(```|~~~)' | grep -vE '^\+[[:space:]]*(```|~~~)(text)?[[:space:]]*$' | grep -c .` 0.
       양성 대조: 편집 전 skill 사본 끝에 언어 힌트 없는 펜스를 더하면 `bare_open_total=1`, `bash` 펜스 한 줄을 더하면 둘째 측정이 1 — 봉인 전 실측 1 · 1)

## Reusability

- [ ] RE-01: N/A (산출물이 설계 가이드 문서 2 개뿐이라 재사용 단위 코드가 없다. 측정: `mine | grep -vcE '\.md$'` 이 0)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다. 이번 변경에 적용: 새 원칙 · 새 필드는 기존 표(`#### 등급 원장` · parity 표 · frontmatter 표 · 요약 표)에 행으로만 들어가고 새 표를 만들지 않는다 — 표 구분줄 수가 편집 전과 같다 [exact]
      (측정: `grep -cE '^[[:space:]]*\|[-: |]+\|[[:space:]]*$' "$T/s.md"` 13 · 같은 명령 `"$T/a.md"` 9. 봉인 전 실측 13 · 9)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `mine | grep -c '^scripts/release.sh$'` 이 0)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (`diagnostics.ide_exclude` 값 `[]`) — 이번 변경에 적용: 편집기 마크다운 확장과 같은 조건(markdownlint-cli2 0.23.2 · MD013 끔)으로 두 가이드의 **더한 줄**에 걸린 경고가 0 이다. 편집 전부터 있던 경고 7 개는 `범위 경계` 절에 적은 대로 범위 밖이다 [exact]
      (측정: `회귀 게이트` 절의 `new-warnings.sh "$T/s0.md" "$T/s.md"` · `new-warnings.sh "$T/a0.md" "$T/a.md"` 가 둘 다 `new_warnings=0`. 양성 대조: 편집 전 skill 사본에 빈 줄 없는 헤더 · 목록 4 줄을 더하면 `new_warnings=3` — 봉인 전 실측 3)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: DG-01 과 같은 명령이 0)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 변경 파일이 문서뿐. 측정: RE-01 과 같은 명령이 0)
- [ ] DG-05: `validate-plugin.py` 의 표 끊김 검사(V10 table-integrity — `harness/docs/**/*.md` 를 읽는다)가 두 가이드에 FAIL 을 0 줄 낸다 [exact]
      (Given: 작업 트리의 두 파일이 `$END` 와 같다 — `git diff --quiet "$END" -- "$S" "$A"` exit 0 · 측정: `python3 scripts/validate-plugin.py harness --check=table-integrity 2>&1 | grep -cE 'FAIL harness/docs/guides/(skill|agent)-design-guide\.md'` 0.
       양성 대조: 스크래치 폴더에 `harness/` · `scripts/validate-plugin.py` · `scripts/plugin_utils.py` · `.claude-plugin/marketplace.json` 을 복사하고 skill 가이드 사본에 헤더 없는 표 행을 넣으면 같은 명령이 1 이상 — 봉인 전 실측 2 (1 차 검토는 넣는 방식을 달리해 1. 끊긴 표 한 덩어리를 한 번 세는 것으로 보인다))
- [ ] DG-06: `python3 scripts/validate-post-kaizen.py --since 7689fde6efdaa2401e90689dd15dd16baf8d59a0` 출력의 `scope-isolation` · `doc-contracts` 줄이 `FAIL` · `ERROR` 가 아니다. `docs-site-regen` 은 Final F2 몫이라 판정에서 뺀다. 다른 Phase 커밋 때문에 `scope-isolation` 이 FAIL 이면 `--verbose` 위반 커밋 목록에 서명 줄 커밋이 없을 때 이 조건은 PASS 다. `doc-contracts` 가 `FAIL` · `ERROR` 이면 `python3 scripts/validate-doc-contracts.py -v` 의 `검사:` 줄에 나온 경로(문서 쪽 · 코드 쪽 둘 다)를 `mine` 과 대조해, 겹치는 경로가 0 개면 다른 Phase 몫으로 근거에 적고 이 조건은 PASS 다 [exact]
      (측정: 명령 출력의 두 줄. `doc-contracts` 가 `FAIL` · `ERROR` 일 때만 — `python3 scripts/validate-doc-contracts.py -v 2>&1 | awk -F' → ' '/^ *검사: /{a=$1; sub(/^ *검사: /,"",a); sub(/:[0-9]+$/,"",a); print a; print $2}' | sort -u | comm -12 - <(mine) | grep -c .` 0.
       봉인 전 실측: `15 checks — 12 PASS / 0 FAIL / 0 ERROR / 3 SKIP`, scope-isolation PASS · doc-contracts PASS · docs-site-regen SKIP. 대조 명령: 지금 `검사:` 줄에서 뽑히는 경로 `.claude/skills/kaizen-orchestrator/SKILL.md` · `scripts/collect-kaizen-data.py` 2 개 · 빈 `mine` 과 겹침 0 · `mine` 자리에 `scripts/collect-kaizen-data.py` 를 넣으면 1)
- [ ] DG-07: 두 가이드의 머리 설정이 올라간다 — skill `version: 1.6.0` · agent `version: 1.7.0` · 둘 다 `last_updated: 2026-09-24` [exact]
      (측정: `head -5 "$T/s.md"` · `head -5 "$T/a.md"` 의 두 필드. 봉인 전 실측: skill 1.5.0 · agent 1.6.0 · 둘 다 2026-08-13)
