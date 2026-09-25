# 카이젠 2026-09-24 Phase 1 (설계 가이드) — notes

- 계약: `.harness/sprint-contract-kaizen-0924-p01-guides.md` (조건 25, 봉인 `sha256:176baf1603fe5981`)
- 개정: `.harness/sprint-amendments-kaizen-0924-p01-guides.md` (조건 변경 0 건, `end_sha` 만)
- 검토: `.harness/.meta/kaizen-0924/phase1-review.md` (1 차 · 2 차 모두 CHANGES, 전부 봉인 전에 반영)
- 시작 커밋 `7689fde6efdaa2401e90689dd15dd16baf8d59a0`

## 커밋

| 커밋 | 내용 | 파일 |
| --- | --- | --- |
| `51a22b4` | 봉인 커밋 | 계약 1 개 |
| `18b8ff0` | 구현 — 두 가이드 (`end_sha`) | `harness/docs/guides/skill-design-guide.md` · `harness/docs/guides/agent-design-guide.md` |
| `fc29b58` | 개정 파일에 `end_sha` | 개정 1 개 |
| 이 파일의 커밋 | notes · 개정 파일 `created` 시각 정정 | `.harness/` 두 개 |

모든 커밋 메시지 끝 문단에 `Kaizen-Phase: kaizen-0924-p01-guides` 줄이 있다. 계약의 `mine()` 과 AR-04 ① 이 이 줄로
이 Phase 커밋을 가린다. **FIX 가 커밋을 더할 때도 이 줄을 넣어야 한다** — 빠지면 AR-04 ① 이 떨어진다. 다른 Phase 는 커밋
메시지에 이 줄을 쓰지 않는다.

## 바꾼 파일

- `harness/docs/guides/skill-design-guide.md` 1.5.0 → 1.6.0
- `harness/docs/guides/agent-design-guide.md` 1.6.0 → 1.7.0

## 반영한 처리 배정표 키

| 키 | 반영 |
| --- | --- |
| `F10` | skill 가이드 §3.7 5 조항 3 항 — 작업 자체를 못 한다고 결론 내리기 전에도 네 칸을 먼저 적는다. 실측 두 건(배포 전 · 실기기 없음 불가 선언, 서버 목록 상한 과대 해석)을 앱 이름 없이 적었다. Bad 예시 한 줄 |
| `harness:P09` | skill 가이드 §3.7 3 항에 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령). agent 가이드 §10 정책 4 항을 평가자(`qa-evaluator.md` 규칙 2 · 11)와 같은 분류(`[미검증:ENV]` · `[미검증:INVALID]` · `env_gaps`)로 다시 썼다. 2 건 기준은 양쪽이 세는 대상이 다르다고 적었다 |
| `harness:P05` | §3.7 생성 측만 — 새 소절 「0 이 아닌 값을 내는 새 측정 — 알려진 답 대조」, 등급 원장 행, §11 parity 16 행. 계약 측 형식(`contract-schema.md` · sprint-contract 패턴 표)과 zsh 배열 규칙 문장은 Phase 2 몫으로 남겼다. 여기서는 zsh 를 사례로만 들었다 |

근거 파일 §3 현행화도 했다 — agent frontmatter 15 종 → 18 종(`omitClaudeMd` · `initialPrompt` · `experimental`, 앞 둘 중
`omitClaudeMd` · `experimental` 은 뜻 미확인으로 적음), 내장 Explore 모델 상속(v2.1.198 부터), 세션 전체 스폰 수 상한 없음,
「2026-04 최신」 → 조회일, 500 라인 「상한」 → 「권고」.

근거 파일 밖에서 찾은 파일 안 모순 둘도 고쳤다 — skill §3.7 이 인용하던 「§11 parity 표 15 번째 항목」이 빈 곳을 가리켰고,
「현재 등급: E2 (§3.7 등급 원장 참조)」가 원장에 없는 행을 가리켰다.

## 넘기는 것 — 이 Phase 범위 밖이라 못 고친 반대편 (명시적 미완)

이번 편집 뒤에도 옛 규칙을 들고 남는 곳이다. 각 Phase 가 고친다.

| 파일 | 남은 것 | 맡을 Phase |
| --- | --- | --- |
| `harness/skills/sprint/SKILL.md:77` | 「`[미검증]` + 사유 한 줄」 — 처리 배정표 `harness:P09` 비고 「sprint/SKILL.md 3 단계 부분은 Phase 4 와 맞춘다」 | Phase 4 |
| `harness/skills/create-agent/SKILL.md` (`:25` · `:33` · `:81` · `:106`) | 「15 종」 · 「4항: (2) 2건 이상 자동 REJECT」 | Phase 4 |
| `harness/skills/create-skill/SKILL.md:24` | 「1500-2000 words 타깃 — Anthropic 기준」 — 근거 파일은 이 수치를 확인하지 못했다(확인된 기준은 500 줄 미만 권고뿐) | Phase 4 |
| `react-kit/references/render-evidence-protocol.md:59` | 「`[미검증]` 마커와 사유 한 줄 … 부분 완료로 보고」 | Phase 10 |
| `flutter-toolkit/references/visual-evidence-protocol.md:136` | 「`[미검증]` 마커 + 사유 한 줄」 | Phase 5 |
| `onboarding-kit/skills/setup-guide/SKILL.md:30` | 「마커 + 사유 한 줄」 | Phase 14 |
| `infra-kit/skills/infra-test/SKILL.md:37` | 「`[미검증] TOOL_OR_ENV_MISSING` … 재검증」 — 시도한 우회 칸 없음 | Phase 8 |
| `rust-kit/agents/rust-reviewer.md:137` | 「agent-design-guide §10」 을 인용하며 접미 없는 `[미검증]` | Phase 9 |

이미 맞아서 건드리지 않은 곳: `harness/agents/qa-evaluator.md:65` (네 요건 원본) · `harness/docs/guides/qa-evaluation-guide.md:1874`
(Parity Table 15 행). 조항 번호 · 항 수를 인용하는 곳(`react-kit/references/render-evidence-protocol.md:125` 「§3.7 5 조 3 항」 ·
`planning-kit/skills/plan-audit/SKILL.md:25` 「§3.7 조항 4」 · `flutter-toolkit/references/visual-evidence-protocol.md:169` 「5 조항」 ·
`qa-evaluation-guide.md:1868` 「§10 Unverifiable (4 항)」)은 번호 · 항 수를 그대로 두어 맞게 남았다.

## Final 에 넘기는 것

- 문서 사이트: `docs/harness/skill-design-guide.html` 에 「500 라인 상한」(`:665` · `:686` · `:998`)이 옛 판으로 남아 있다.
  `docs/harness/agent-design-guide.html` 도 옛 판이다. Final F2 재생성 대상 (`validate-post-kaizen.py` 의 `docs-site-regen` 이 이
  Phase 뒤 FAIL — 계약 DG-06 이 Final 몫으로 뺐다)
- 오케스트레이터 `.claude/skills/kaizen-orchestrator/references/phase-research-templates.md:28` 의 「500 라인 상한」 표기 — 어느
  Phase 범위에도 없다
- `harness` plugin.json 버전 · marketplace · 루트 README 는 건드리지 않았다

## changelog 한 단락

설계 가이드 두 편을 고쳤다. 스킬이 검증을 못 할 때 `[미검증]` 에 사유 한 줄만 붙이던 규칙을 네 칸(막는 것 · 시도한 우회 ·
통제 불가 사유 · 재검증 명령)으로 바꾸고, 작업 자체를 못 한다고 결론 내리기 전에도 같은 네 칸을 먼저 적게 했다. 에이전트 가이드의
미검증 정책은 평가자가 이미 쓰던 `ENV` / `INVALID` 분류와 같은 말로 다시 썼다. 새로 짠 측정 스크립트가 0 이 아닌 값을 낼 때 손으로
답을 셀 수 있는 작은 입력으로 먼저 맞추는 「알려진 답 대조」를 넣었다. 공식 문서를 다시 조회해 frontmatter 18 종, 내장 Explore 모델
상속, 세션 전체 스폰 수 상한 없음을 반영했고, 500 줄은 상한이 아니라 권고로 고쳤다.

## 킷 로그 한 단락 (harness)

2026-09-24 Phase 1 — skill-design-guide 1.6.0 · agent-design-guide 1.7.0. 근거:
[Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md) (검증기 실행 →
고침 → 재실행, 500 줄 미만은 최적 성능 권고),
[Create custom subagents](https://code.claude.com/docs/en/sub-agents.md) (2026-09-22 수정본 — frontmatter 18 종, `initialPrompt`
범위, 내장 Explore 모델 상속, 세션 전체 스폰 수 상한 없음),
[skill-creator SKILL.md](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) (`expected_output`, 500 줄은
ideal), [Claude Code v2.1.281](https://github.com/anthropics/claude-code/releases/tag/v2.1.281) (2026-09-23 게시),
[zsh 매뉴얼 — Array Subscripts](https://zsh.sourceforge.io/Doc/Release/Parameters.html#Array-Subscripts) (기본 zsh 배열은 1 부터,
`KSH_ARRAYS` 예외). 근거 파일이 밝힌 한계 — 「우회 1 개 이상 의무」의 공식 문구는 없다, 「2~3 줄」은 레포 관례, 세션 누적 상한이
없어진 릴리스는 특정 못 함.

## 다음 사이클 메모

- 근거 파일 `phase4.md` 에만 있고 이번 근거 파일에는 없어 미반영: agent 가이드 `:59`(배치 우선순위) · `:79`(model 생략 시 동작) ·
  skill 가이드 `:393`(`name` 필수 여부) · `:806`(다른 플랫폼 호환)
- agent 가이드 §7 의 오류 문구 두 개(`Concurrent subagent limit reached` · `Subagent spawn limit reached`)가 어느 상한 것인지
  근거가 없어 짝짓지 않았다. 다음 조회 때 확인
- `omitClaudeMd` · `experimental` 의 뜻 — 공식 표에서 이름만 확인했다
- `save-feedback.sh` 가 이번에도 `project_name` 을 워크트리 이름 `kaizen-0924` 로 적었다
  (`~/.harness/feedback/contract/5a24cc99-2026-09-24T204249-de8c7935-38902.yaml`). Phase 12 추가 과제와 같은 결함
- 검토에서 배운 것: 모의 편집본으로 「틀리게 남겨도 통과하는 문장」을 찾는 방법이 두 번 모두 막는 결함을 찾았다. 문서 산출물
  계약의 검토 절차로 올릴 만하다 (Phase 2 · 3 판단)
- 러닝북에 없는 서명 줄 `Kaizen-Phase:` 규약은 이 계약에만 있다. 다른 Phase 도 `mine()` 을 같은 꼴로 쓰려면 러닝북 계약 규칙에 올린다
