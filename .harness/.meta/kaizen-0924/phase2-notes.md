# 카이젠 2026-09-24 Phase 2 (contract) — notes

- 계약: `.harness/sprint-contract-kaizen-0924-p02-contract.md` (조건 28 · 기능 조건 19, 봉인 `sha256:76b807f6d67fcf8a`)
- 개정: `.harness/sprint-amendments-kaizen-0924-p02-contract.md` (조건 변경 0 건, `end_sha` 만)
- 검토: `.harness/.meta/kaizen-0924/phase2-review.md` (1 회차 CHANGES 여섯 건 · 2 회차 CHANGES 한 건, 전부 봉인 전에 반영)
- 시작 커밋 `76cfb376e2293350e2583c50166286bd2ec95b82`
- 계약 피드백: `~/.harness/feedback/contract/5a24cc99-2026-09-24T222231-de8c7935-60429.yaml` (`verify-feedback.sh` PASS)

## 커밋

| 커밋 | 내용 | 파일 |
| --- | --- | --- |
| `211f00d` | 봉인 커밋 | 계약 1 개 |
| `3e3ff04` | 구현 — 네 파일 | `harness/references/contract-schema.md` · `harness/skills/sprint-contract/SKILL.md` · `harness/docs/guides/contract-design-guide.md` · `harness/skills/sprint-contract/references/red-flags.md` |
| `92d99e9` | 개정 파일에 `end_sha` (`3e3ff04`) | 개정 1 개 |
| 이 파일의 커밋 | notes | `.harness/` 한 개 |
| 그다음 커밋 | 개정 파일에 notes 커밋 sha 로 `end_sha` 한 줄 더 | 개정 1 개 |

모든 커밋 메시지 끝 문단에 `Kaizen-Phase: kaizen-0924-p02-contract` 줄이 있다. 계약의 `mine()` 과 AR-06 ① 이 이 줄로
이 Phase 커밋을 가린다. **FIX 가 커밋을 더할 때도 이 줄을 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다.**

## 바꾼 파일

- `harness/references/contract-schema.md` v5.4 → v5.5
- `harness/docs/guides/contract-design-guide.md` v5.0 → v5.1
- `harness/skills/sprint-contract/SKILL.md` (frontmatter 는 그대로 — harness README AUTO 구간 변화 없음)
- `harness/skills/sprint-contract/references/red-flags.md`

**`contract-schema.md` v5.4 → v5.5 — PR 본문에 적을 것** (contract-kaizen Gotcha 「contract-schema.md 를 바꾸면 PR 본문에 반드시
적는다」). Final 이 PR 본문으로 옮긴다.

## 반영한 처리 배정표 키

| 키 | 반영 |
| --- | --- |
| `harness:P03` · `F12` | 스키마 §미실측 오라클 봉인 금지 에 「면제는 기대값에만 걸린다」 — 재는 명령의 준비 단계(읽을 경로 · `command -v` 출력과 종료 코드 · 도구를 숨기는 전제 · 임시 사본)는 봉인 전에 돌린다. 스킬 Gotcha · Step 7 `measure_premise_unrun` · 가이드 체크리스트 행 |
| `harness:P05` · `F17` | 스키마 §알려진 답 대조 (조건 패턴), 스킬 조건 패턴 5 종 표 행, 가이드 새 절 `### 0 이 아닌 기대값` 과 parity 15 · 16 행, Step 7 `known_answer_missing`. 생성 측(`skill-design-guide.md` §3.7)은 Phase 1 이 넣었다 |
| `user-setup:P5` | 스키마 §셸 이식성 규약 에 zsh 배열 첨자 줄 (`harness:P05` 의 zsh 줄과 같은 줄이라 한 번만) |
| `harness:P06` · `F11` | 조건 수 가이드를 기능 조건만 세게(단순 1~3 · 중간 4~8 · 복잡 9~20), 스키마와 스킬 6.2 에 같은 계산식, 금지 패턴 `AP-00: N/A` 예외, 스킬 Step 5 끝 「사용자가 할 일」 한 줄. `/sprint` 쪽 두 자리는 Phase 4 |
| `harness:P08` · `F13` | 스키마 §메타데이터 · 스킬 Step 6 에 `created` 는 `date '+%Y-%m-%d %H:%M'` 출력을 옮긴다. `Evaluated` 는 Phase 3 |
| `F21` | 스킬 Step 0 — 셸이 없는 세션이면 멈추고, 파일 쓰기 도구만 없으면 셸로 쓴다. 멈출 때 네 칸 · 재검증 명령, 셸이 없으면 막는 것 칸에 쓸 수 있는 도구 목록 |
| `F27` | 준비 단계 실측(명령 · 종료 코드)과 기능 조건 계산 명령으로 반영. 계약 검사기 부분(`harness:P02`)은 Phase 4 |

러닝북 추가 과제 둘: 메타 이슈 1(`.harness/.meta/phase4-handoff-to-contract.md`) F1 은 2026-09-23 스키마 절이 이미 해결했고 스킬
Gotcha 에 그 절을 가리키는 안내를 더했다. F2(커밋 뒤 빈 출력이 되는 상태 전제) · F3(여러 주체 커밋 — 서명 줄 `mine` ·
`unsigned_on`) · F4(검사 스크립트 전체 통과 대신 이 스프린트 몫의 줄)를 스키마에 넣었다. F11 크기 규칙은 위 `harness:P06` 행.
카이젠 Step 2 피드백 분석에서 찾은 자기진단 true 뜻 섞임도 고쳤다 — 모든 항목이 「문제가 있다」 가 true.

## 미반영 키와 사유

- `harness:P02` (계약 검사기 · `save-feedback.sh` 필수 필드) — 처리 배정표가 Phase 4 에 배정. 아래 `## Phase 4 가 읽을 것`
- 데이터 풀 §1 개선 제안 「개정 번호를 이어 붙이는 규칙」(2026-09-24) — 처리 배정표 밖이고 크기에 비해 조건이 늘어난다. 다음 사이클 메모

## 넘기는 것 — Phase 3 (평가자 쪽 반대편, 명시적 미완)

이번 편집 뒤에도 옛 규칙을 들고 남는 곳이다. 줄 번호는 시작 커밋 `76cfb37` 판이다.

| 파일:줄 | 남은 것 |
| --- | --- |
| `harness/agents/qa-evaluator.md:590` | 한 줄에 두 문제 — 표준형 「4 요소」(스키마 v5.5 는 상한 ref 를 더한 5 요소), 상태 전제 선택지에 `Given: 이 스프린트의 커밋이 끝난 뒤` 가 없다 |
| `harness/agents/qa-evaluator.md:1217` | 「contract-design-guide.md — 계약 작성 가이드 v4」 → v5.1 |
| `harness/docs/guides/qa-evaluation-guide.md:12` | 참조 스키마 `(v5.3)` → v5.5 |
| `harness/docs/guides/qa-evaluation-guide.md:742-743` | 상태 전제 확인이 `커밋 직전 working tree` · `스테이징 완료 후` · 브랜치 비교만 나열 — 커밋 구간 전제가 없다 |
| `harness/docs/guides/qa-evaluation-guide.md:746` | 「contract-schema v4 §Diff-Scope Oracle 표준형」 · 「표준형 4 요소」 → 5 요소 |
| `harness/docs/guides/qa-evaluation-guide.md:1785` | 평가자가 계약 수정 제안을 쓰는 예시 「`Given: 스테이징 완료 후` 를 붙이고 `--cached` 를 쓸 것」 — 커밋 뒤에는 늘 빈 집합을 잰다. 스키마 v5.5 §Diff-Scope 표준형 「상태 전제는 평가 시점에 다시 잴 수 있는 것으로 고른다」 로 맞춘다 |
| `harness/docs/guides/qa-evaluation-guide.md:1862` | Parity Table 에 16 행(알려진 답 대조, 생성 측 skill 가이드 §3.7 · 계약 측 스키마 §알려진 답 대조) 없음 |
| `harness/docs/guides/qa-evaluation-guide.md:1915` | 「Parity with: skill-design-guide 1.5.0 · agent-design-guide 1.6.0 · contract-design-guide v5.0」 → 1.6.0 · 1.7.0 · v5.1 |
| 같은 두 파일 — `Evaluated` 시각 | `harness:P08` 비고 「qa-evaluator 쪽 Evaluated 는 Phase 3 과 맞춘다」 — 계약 쪽은 `date '+%Y-%m-%d %H:%M'` 출력을 옮긴다(스키마 §메타데이터 v5.5) |

Phase 3 확인 목록에 넣을 것: Phase 1 계약 DG-02 의 보조 스크립트(`new-warnings.sh` 옛 판)가 `sed -E 's#^[^ ]*:([0-9]+).*#\1#'`
탐욕 매치라 `경로:13:8` 에서 열 번호 `8` 을 줄 번호로 읽었다. Phase 1 결과는 고친 판으로 다시 재도 같다(new_warnings 0 · 0).
평가자가 산출물이 검사 스크립트인 조건을 볼 때 「줄 번호를 뽑는 정규식이 열 번호를 잡지 않는가」 를 사본으로 확인하게 한다.

## Phase 4 가 읽을 것

러닝북의 Phase 4 입력 목록에 이 파일이 없다. **오케스트레이터가 Phase 4 를 부를 때 이 파일 경로를 함께 넘긴다.**

| 파일 | 할 일 |
| --- | --- |
| `harness/skills/sprint/SKILL.md` | `harness:P06` 의 `/sprint` 쪽 두 자리 — QA 결과 블록과 6 단계 보고 끝에 「사용자가 할 일」 한 줄. 문구는 sprint-contract Step 5 에 이번에 넣은 `사용자가 할 일: 없음` · `사용자가 할 일: <한 줄>` 과 맞춘다 |
| `harness/scripts/save-feedback.sh` · sprint-contract `SKILL.md` Step 9 | `harness:P02` — 스크립트를 먼저 바꾸고 Step 9 문구를 맞춘다. 문구를 먼저 바꾸면 틀린 안내가 된다. 이번 저장에서도 `project_name` 이 워크트리 이름 `kaizen-0924` 로 적혔다(Phase 12 추가 과제와 같은 결함) |
| `harness/references/feedback-schema.yaml` | 자기진단 checklist 의 true 뜻을 「문제가 있다」 로 적는다. 새 항목 `measure_premise_unrun` · `known_answer_missing` |
| `harness/skills/contract-kaizen/SKILL.md` Step 2 | 2026-09-24 이전 계약 피드백은 true 뜻이 섞였다 — 옛 문구가 「했는가」 였던 12 항목(`nfr_coverage` · `format_granularity_missing` · `diff_oracle_nonstandard` · `evidence_artifact_missing` · `section_header_unclassified` · `conditions_count_typed` · `contract_seal_missing` · `seal_commit_missing` · `measurement_coverage_gap` · `factor_matrix_missing` · `negative_control_missing` · `amendment_direction_uncomputed`)은 그 이전 값을 반복 실패로 세지 않게 한다. 실측: Phase 1 피드백(2026-09-24 20:42)도 `nfr_coverage: true` 로 적혔다 |

## Final 에 넘기는 것

- 문서 사이트: `validate-post-kaizen.py --since 76cfb37` 의 `docs-site-regen` 이 `harness/docs/guides/contract-design-guide.md` ·
  `harness/references/contract-schema.md` 를 들어 FAIL 이다. Final F2 재생성 대상
- 러닝북 · 오케스트레이터: Phase 계약의 서명 줄 규약(`Kaizen-Phase: <slug>`)은 이제 스키마 §여러 주체가 한 가지에 커밋할 때 가
  정의한다. 러닝북 계약 규칙에서 그 절을 가리키게 한다
- `harness` plugin.json 버전 · marketplace · 루트 README · `.github/workflows/ci.yml` 은 건드리지 않았다. 새 시험 파일도 없다

## changelog 한 단락

계약 스키마를 v5.5 로 올렸다. 구현이 만들 값은 미리 잴 수 없어 면제지만, 그 값을 재는 명령의 준비 단계는 봉인 전에 돌리게 했다.
새로 짠 측정이 0 이 아닌 값을 내면 손으로 답을 셀 수 있는 작은 입력으로 먼저 맞추는 「알려진 답 대조」 를 조건 패턴에 넣었다.
조건 수 가이드는 자동 포함 줄 · 금지 패턴 줄 · 해당 없음 줄을 빼고 기능 조건만 세게 바꿔 단순 작업도 수를 지킬 수 있게 했다.
변경 범위 조건은 커밋하고 나면 빈 출력이 되는 상태 전제 대신 커밋 구간으로 재고, 여러 주체가 한 가지에 커밋하면 서명 줄로 내
커밋을 가린다. 셸이 없는 세션은 0 단계에서 멈추고, 계약 시각은 `date` 출력을 옮기고, 초안 끝에는 사용자가 할 일 한 줄을 적는다.
자기진단 체크리스트는 모든 항목이 「문제가 있다」 가 true 가 되게 문구를 맞췄다.

## 킷 로그 한 단락 (harness)

2026-09-24 Phase 2 — contract-schema v5.5 · contract-design-guide v5.1. 근거:
[POSIX.1-2024 `command`](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/command.html) (`command -v` 는 못 찾으면 출력
없이 0 보다 큰 종료 코드, 셸 내장 · 함수도 보고),
[zsh Array Parameters](https://zsh.sourceforge.io/Doc/Release/Parameters.html#Array-Parameters) ·
[GNU Bash Arrays](https://www.gnu.org/software/bash/manual/html_node/Arrays.html) (zsh 일반 배열은 기본 옵션에서 1 부터, bash 는 0 부터),
[Gherkin Best Practices](https://github.com/andredesousa/gherkin-best-practices) (조건을 짧게, 한 조건에 한 규칙 — 개수는 주지 않는다),
[GNU Coreutils `date`](https://www.gnu.org/software/coreutils/manual/html_node/date-invocation.html). 근거 파일이 밝힌 한계 — 기능
조건 1~3 · 4~8 · 9~20 은 레포 내부 정책, 「사용자가 할 일」 끝맺음과 도구 없는 세션의 멈춤은 직접 근거 없음, 알려진 답 입력
2~3 줄은 레포 관례.

## 다음 사이클 메모

- 데이터 풀 §1 개선 제안 「개정 번호를 이어 붙이는 규칙」(2026-09-24) — 이번에 넣지 않았다
- Phase 1 계약 DG-02 보조 스크립트의 열 번호 · 줄 번호 혼동(위 Phase 3 확인 목록) — 이 계약은 고친 판을 썼다. 같은 스크립트를
  다른 계약이 베꼈는지 찾아본다
- 근거 파일 `phase2.md` 에 있으나 이번에 쓰지 않은 자료: arxiv 두 편 · OWASP Logging Cheat Sheet · 요구사항 모호성 논문 ·
  Cucumber Gherkin reference · jq 1.8.2 릴리스 · Claude Code plugins-reference · skills 문서
- 사용자 전역 훅 `~/.claude/hooks/lint-contract-oracle.sh` 는 계약의 `오라클 해소:` 줄을 읽지 않아 해소한 조건도 계속 경고한다
  (이 계약에서 12 건). 레포 밖 파일이라 손대지 않았다
- 넘김 목록을 재는 조건은 경로를 `경로:줄` 로 쪼개 재야 한다 — 줄 번호 없는 경로 토큰은 같은 파일의 다른 줄 번호 토큰에 늘
  받쳐진다(2 회차 검토가 잡은 결함). 스키마 §측정 커버리지 표기 에 한 줄 올릴지 본다
- BUILD 가 계약 코드 블록을 기계로 떼어 28 조건을 한 번에 도는 묶음(스크래치 `p2build/meas.sh` · `extract.py`)을 썼다. 문서
  산출물 계약에서는 이 묶음을 QA 에 같이 넘기는 관례를 러닝북에 둘 만하다
