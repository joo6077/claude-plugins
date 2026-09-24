---
phase: 2
title: "Phase 2 contract — 확보된 외부 근거"
collected: 2026-09-24
method: codex (foreground, 직접 호출 · gpt-5.6-sol · 조회는 curl/gh)
inputs: 처리 배정표(.claude/kaizen-input/insights-report.md)의 Phase 2 행 · phase-research-templates.md Phase 2 필수 출처 · 현행화 점검
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치를 지어내지 마라. 없으면 미반영으로 남긴다.
---

읽기 전용으로 조사했으며 레포 파일은 만들거나 수정하지 않았다.

## 1. 출처 목록

실제로 조회한 자료만 적었다.

### 필수 소스

1. [Li et al., LLMs-as-Judges: A Comprehensive Survey, arXiv 2412.05579v2](https://arxiv.org/abs/2412.05579)
2. [Kim et al., An Empirical Study of LLM-as-a-Judge, arXiv 2506.13639v1](https://arxiv.org/html/2506.13639v1)
3. [Gherkin Best Practices](https://github.com/andredesousa/gherkin-best-practices)
4. [Tjong, Avoiding Ambiguity in Requirements Specifications](https://cs.uwaterloo.ca/~dberry/FTP_SITE/tech.reports/TjongThesis.pdf)

### 공식 문서·현행화 소스

5. [Cucumber Gherkin Reference](https://cucumber.io/docs/gherkin/reference/)
6. [POSIX.1-2024 `command`](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/command.html)
7. [POSIX.1-2024 `PATH`](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap08.html)
8. [zsh Array Parameters](https://zsh.sourceforge.io/Doc/Release/Parameters.html#Array-Parameters)
9. [GNU Bash Arrays](https://www.gnu.org/software/bash/manual/html_node/Arrays.html)
10. [GNU Coreutils `date`](https://www.gnu.org/software/coreutils/manual/html_node/date-invocation.html)
11. [Claude Code Skills](https://code.claude.com/docs/en/skills)
12. [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference)
13. [jq 1.8.2 릴리스](https://github.com/jqlang/jq/releases/tag/jq-1.8.2)
14. [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)

## 2. 항목별 관찰 사실

### harness:P03 — 면제는 값에만, 준비 단계는 봉인 전 실행

- POSIX에서 `PATH`는 실행 파일을 찾을 경로 접두 목록이며 앞에서부터 검색한다. `command -v`는 현재 셸 환경에서 사용할 경로나 명령을 출력하고, 찾지 못하면 출력하지 않으며 0보다 큰 종료 상태를 반환한다. 따라서 `PATH` 축소와 `command -v`는 “도구 부재 전제”를 구현 전에 직접 확인하는 정당한 방법이다. 다만 **빈 출력뿐 아니라 종료 코드도 같이 기록해야 한다**. [POSIX `PATH`](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap08.html), [POSIX `command -v`](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/command.html)

- 반대·한계: `command -v`는 외부 실행 파일만이 아니라 셸 내장·예약어·함수도 보고할 수 있다. 단순한 `PATH` 축소가 모든 명령 종류를 숨긴다는 일반화는 틀리다. `jq`처럼 외부 유틸리티임이 확실한 대상에는 적합하지만, 일반 도구에는 출력의 종류까지 확인해야 한다. [POSIX `command -v`](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/command.html)

- 레포 실측 근거도 방향이 같다. 2026-09-22에는 따옴표 없는 셸 변수가 파일을 못 찾은 오류를 `2>/dev/null`이 삼켜 0처럼 보이게 했다. 즉 기대 “값”과 별개로 입력 경로·대상 수·명령 성공 여부를 먼저 검증해야 했다. [skill-design-guide.md:325](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/skill-design-guide.md:325)

- 추론: 스키마 면제를 “구현이 만들 값”으로 한정하고, PATH·파일 경로·환경변수·빈 입력 구성 같은 준비 단계는 면제하지 않는 설계가 외부 명령 의미와 잘 맞는다.

### harness:P05 — 알려진 답 대조와 zsh 배열

- LLM-as-Judge 실험에서 평가 기준이나 참조 답을 제거하면 인간 판정과의 상관이 낮아졌다. GPT-4o에서는 기본 설정 0.666에서 기준 제거 시 0.591, 참조 답 제거 시 0.638로 낮아졌다. 작은 알려진 답을 측정 스크립트의 참조 오라클로 쓰는 방향과 일치한다. [arXiv 2506.13639](https://arxiv.org/html/2506.13639v1)

- 이 논문이 직접 입증한 것은 LLM 평가 설계다. “2~3줄 fixture가 모든 셸 측정 스크립트에 최적”이라는 수치까지 입증하지는 않는다.

- 반대·보정: 알려진 입력에서 0이 나왔다고 해서 반드시 “스크립트 결함”만 있는 것은 아니다. fixture가 비영점 결과를 실제로 유발하지 못했을 수도 있다. 문구는 “통과가 아니라 **스크립트 또는 fixture 결함**”이 더 정확하다.

- zsh 일반 배열은 기본적으로 1부터 번호를 매기고 `${arr[0]}`은 빈 문자열이다. 단, `KSH_ARRAYS` 옵션을 켜면 0부터 센다. [zsh 공식 문서](https://zsh.sourceforge.io/Doc/Release/Parameters.html#Array-Parameters)

- Bash indexed array는 0부터 센다. `"${name[@]}"`는 각 원소를 별도 단어로 확장한다. [GNU Bash Arrays](https://www.gnu.org/software/bash/manual/html_node/Arrays.html)

- 추론: 두 셸을 함께 지원하는 코드에서는 첨자 기반 순회를 피하고 `for x in "${arr[@]}"`를 사용하는 권고가 타당하다. 다만 문장은 “zsh 기본 옵션에서는 1부터”라고 써야 예외가 정확히 드러난다.

### harness:P06 — 작업 크기에 맞는 조건 수와 N/A

- Gherkin 커뮤니티 가이드는 시나리오를 가능한 짧게 하고, 한 시나리오에서 여러 규칙을 동시에 시험하지 말며, When–Then 쌍이 여러 개면 분리를 검토하라고 한다. 기능 파일이 커지면 하위 기능으로 나누라고도 권한다. [Gherkin Best Practices](https://github.com/andredesousa/gherkin-best-practices)

- 같은 가이드는 step 수에 절대 상한을 두지 않고 “reasonable value”, 예시로 Given/When/Then당 2~3개의 `And` 정도를 제시한다. conjunctive step 분리도 의무 규칙은 아니라고 명시한다. 따라서 “조건은 작업 크기에 비례하되 고정 총량을 기계적으로 강제하지 않는다”는 방향은 지지되지만, `1~3개`라는 정확한 기능 조건 수는 내부 정책이다. [Gherkin Best Practices](https://github.com/andredesousa/gherkin-best-practices)

- Cucumber 공식 문서는 Given을 초기 상태, When을 사건·행동, Then을 기대 결과로 정의하지만, 여러 Given·Then을 `And`/`But`로 연결하는 것도 정식 문법으로 허용한다. “one When–Then pair”는 공식 Gherkin 표준이 아니라 커뮤니티 설계 휴리스틱이다. [Cucumber Gherkin Reference](https://cucumber.io/docs/gherkin/reference/)

- LLM 평가 연구에서는 모든 중간 점수 설명보다 양끝 점수 설명만 둔 구성이 인간 평가와 가장 높은 상관을 보이면서 일관성을 유지했다. 더 많은 기준 설명이 항상 더 신뢰성 높다는 근거는 아니다. [arXiv 2506.13639](https://arxiv.org/html/2506.13639v1)

- 레포에는 실제 충돌이 있다. Gotcha는 안티패턴 최소 2개를 강제하지만, Step 3과 스키마는 `AP-00: N/A (사유)`를 허용한다. [sprint-contract/SKILL.md:38](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/skills/sprint-contract/SKILL.md:38), [sprint-contract/SKILL.md:498](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/skills/sprint-contract/SKILL.md:498)

- 추론: 자동 포함 RE 2개·DG 4개와 형식상 필요한 `N/A` 줄은 기능 크기 지표에서 빼고, 4축 복잡도 결과에 따라 기능 조건만 1~3개부터 확장하는 방식이 더 일관된다. 정확한 구간 자체에는 외부 정량 근거가 없다.

### harness:P08 — `created`·`Evaluated` 시각을 명령 출력에서 취득

- GNU `date`는 현재 날짜와 시간을 출력하며 `date [+format]` 형식을 지원한다. 따라서 `date '+%Y-%m-%d %H:%M'` 출력 전사는 손으로 짐작한 시각보다 재현 가능한 절차다. [GNU Coreutils `date`](https://www.gnu.org/software/coreutils/manual/html_node/date-invocation.html)

- OWASP는 로그 시각과 실제 사건 시각이 다를 수 있다고 구분하며, 서버·장치 간 시각 동기화 또는 시간 오프셋·신뢰도 기록을 권한다. 이는 AskUserQuestion의 **호출 시각이 아니라 답변 시각**을 동의 시각으로 쓰는 내부 제안과 부합한다. [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)

- 반대·한계: `date '+%Y-%m-%d %H:%M'`만으로는 시간대와 초가 사라진다. 현재 스키마와의 호환을 위해 그 형식을 유지할 수 있지만, 서로 다른 시간대의 기록을 비교한다면 오프셋을 가진 원본 타임스탬프도 보존해야 한다. [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)

- 현재 스키마는 이미 동의 앵커의 두 번째 출처로 세션 기록의 AskUserQuestion 쌍과 답변 시각을 규정하지만, 평가자 정의에는 prompt-log만 남아 있다. [contract-schema.md:989](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/references/contract-schema.md:989), [qa-evaluator.md:693](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/agents/qa-evaluator.md:693)

### user-setup:P5 — 셸 이식성 규약

- 권장 문장의 핵심은 공식 문서와 일치한다. zsh 기본 배열은 1-base, Bash indexed array는 0-base다. [zsh 배열](https://zsh.sourceforge.io/Doc/Release/Parameters.html#Array-Parameters), [Bash 배열](https://www.gnu.org/software/bash/manual/html_node/Arrays.html)

- 보정 권고: “zsh 배열은 1부터” 대신 “**zsh 일반 배열은 기본 옵션에서 1부터**”라고 적는다. `KSH_ARRAYS`에서는 0-base이기 때문이다.

### F11 — 한 줄 변경에 무거운 절차

- P06과 같은 근거다. 짧고 단일 규칙인 시나리오를 선호하고 큰 시나리오는 분리하라는 가이드는 규모 비례 절차를 지지한다. 다만 정확한 조건 수는 규정하지 않는다. [Gherkin Best Practices](https://github.com/andredesousa/gherkin-best-practices)

- “사용자가 할 일: 없음/한 줄” 끝맺음에 직접 대응하는 외부 근거는 이번 조회에서 찾지 못했다.

### F12 — 실행하지 않은 검증 명령을 계약에 기재

- P03과 동일하다. `command -v`와 종료 상태는 준비 전제를 직접 확인할 수 있는 표준 수단이다. [POSIX `command`](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/command.html)

- 명확한 평가 기준과 참조 답이 판단 신뢰성에 중요하다는 연구도 “명령 문자열 존재”보다 실행 결과를 기준으로 삼는 방향과 맞는다. [arXiv 2506.13639](https://arxiv.org/html/2506.13639v1)

### F13 — 짐작한 시각으로 REJECT

- P08과 동일하다. 시각은 사건 시각과 기록 시각을 구분해 수집해야 하며, 출력 또는 로그 기록에서 얻는 편이 낫다. [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)

### F17 — 측정 스크립트 자체 버그

- 알려진 답과 평가 기준을 함께 주는 것이 판정 신뢰성을 높였다는 실험은 known-answer 대조의 방향을 지지한다. [arXiv 2506.13639](https://arxiv.org/html/2506.13639v1)

- zsh와 Bash의 배열 시작 첨자가 실제로 다르므로, 첨자 반복을 피하라는 수정은 직접 근거가 있다. [zsh 배열](https://zsh.sourceforge.io/Doc/Release/Parameters.html#Array-Parameters), [Bash 배열](https://www.gnu.org/software/bash/manual/html_node/Arrays.html)

### F21 — 필요한 도구가 없을 때 Step 0에서 멈춤

- POSIX `command -v`는 도구 부재를 출력 없음과 비영 종료 상태로 판정할 수 있게 한다. [POSIX `command`](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/command.html)

- “첫 줄에 알리고 즉시 멈춘다”는 UX 정책 자체를 뒷받침하는 직접 근거는 이번 조회에서 찾지 못했다.

- 추론: 도구가 이후 전 단계의 필수 전제라면 fail-fast가 맞다. fallback이 가능한 도구라면 즉시 중단보다 가용 기능과 불가능 기능을 구분하는 편이 기존 3단계 fallback 정책과 더 일관된다.

### F27 — 스스로 검증하는 계약

- LLM-as-Judge 설문은 judge 시스템을 기능·방법론·적용·메타평가·한계의 다섯 관점으로 다뤄, 평가자 자체의 메타평가가 별도 문제임을 명시한다. [arXiv 2412.05579](https://arxiv.org/abs/2412.05579)

- 신뢰성 실험은 평가 기준과 참조 답을 빼면 인간 판정 정합성이 낮아지고, 명확한 기준이 있을 때 추가 CoT의 이득은 작다고 보고한다. 조건별 명령·기대 출력·종료 코드와 결정론적 검사기를 우선하는 방향을 지지한다. [arXiv 2506.13639](https://arxiv.org/html/2506.13639v1)

- 반대·한계: 이 연구는 계약 검사기의 특정 단계 수나 기능 조건 수를 검증한 것이 아니다. 그런 숫자는 내부 경험 정책으로 표시해야 한다.

## 3. 현행화 — 낡은 곳

### 외부 도구·표준

| 위치 | 현재 값 | 최신 확인 값 | 판정 |
|---|---|---|---|
| [skill-design-guide.md:10](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/skill-design-guide.md:10) | “Anthropic 공식 문서(2026-04 최신)” | 현재 Skills 문서는 최소 Claude Code v2.1.273까지의 동작을 기술하고, 새 `arguments`, `${CLAUDE_SKILL_DIR}`, `${CLAUDE_PROJECT_DIR}` 등의 규약을 포함한다. [Claude Code Skills](https://code.claude.com/docs/en/skills) | **낡음**. “2026-04 최신”이라는 최신성 표시는 제거하거나 조회일 2026-09-24로 갱신해야 한다. |
| [sprint-contract/SKILL.md:74](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/skills/sprint-contract/SKILL.md:74) | `$N = $ARGUMENTS[N]`, 누락된 indexed argument는 그대로 남고 `\\$1`로 literal escape | 현행 공식 문서도 동일 | 최신. [Claude Code Skills](https://code.claude.com/docs/en/skills) |
| [qa-evaluator.md:1223](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/agents/qa-evaluator.md:1223) | `${CLAUDE_PLUGIN_ROOT}`는 설치 디렉터리 절대경로 | 현행 공식 문서도 동일 | 최신. [Plugins Reference](https://code.claude.com/docs/en/plugins-reference) |
| [harness/README.md:63](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/README.md:63) | jq 버전 미지정 | 최신 확인 안정 릴리스 `jq-1.8.2`, 2026-06-20. 보안 수정 다수 포함 | 낡은 버전 표기는 없지만 최소 버전 정책도 없다. [jq 1.8.2](https://github.com/jqlang/jq/releases/tag/jq-1.8.2) |
| contract/schema 셸 스니펫 | zsh 기본 1-base 가능성을 아직 명시하지 않음 | zsh 기본 1-base, `KSH_ARRAYS`에서는 0-base; Bash는 0-base | **규약 누락**. [zsh](https://zsh.sourceforge.io/Doc/Release/Parameters.html#Array-Parameters), [Bash](https://www.gnu.org/software/bash/manual/html_node/Arrays.html) |

이번 범위에서 폐기된 POSIX `command -v`, `${arr[@]}`, `date +format`, `${CLAUDE_PLUGIN_ROOT}`, `$ARGUMENTS[N]` 사용은 발견하지 못했다.

### 같이 고쳐야 할 내부 버전 드리프트

외부 버전 문제는 아니지만 Phase 2 편집 시 그대로 두면 문서 정합성이 깨진다.

- [contract-design-guide.md:1293](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/contract-design-guide.md:1293): Schema version `v5.3` → 현재 스키마 선언은 [contract-schema.md:1126](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/references/contract-schema.md:1126)의 `v5.4`.
- [qa-evaluator.md:1217](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/agents/qa-evaluator.md:1217): contract-design-guide `v4` → 실제 frontmatter는 [contract-design-guide.md:3](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/contract-design-guide.md:3)의 `v5.0`.
- [contract-schema.md:817](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/references/contract-schema.md:817)에는 “v5.5 추가”가 있으나 같은 파일의 현재 버전은 `v5.4`다. 버전 bump 누락인지 미래 버전 라벨 오기인지 결정이 필요하다.

## 4. 권장안

Phase 2 계약 조건으로 삼을 만한 것은 다음과 같다.

1. **봉인 전 준비 단계 실행을 E2 증거로 요구한다.**

   - 면제 대상은 구현이 만들 결과값뿐이다.
   - PATH, 파일 경로, 환경변수, 설치 위치, 빈 입력 구성은 봉인 전 실행한다.
   - 출력과 종료 코드를 함께 기록한다.
   - 자기진단에 `measure_premise_unrun`을 추가한다.
   - 2026-09-22 사례는 “따옴표 없는 변수가 대상 파일을 못 찾았고 오류 억제가 이를 0으로 위장했다”로 쓰는 것이 확인된 레포 사실과 맞다.

2. **비영 측정 스크립트에 known-answer 대조를 요구한다.**

   - 손으로 셀 수 있는 2~3줄 입력, 기대값, 실제값, 종료 코드를 나란히 적는다.
   - 불일치나 0은 통과가 아니라 “스크립트 또는 fixture 결함”으로 둔다.
   - 조건 패턴 표와 skill-design-guide 생성 측 규칙에 같이 착지시킨다.

3. **zsh 문장은 예외를 포함해 쓴다.**

   > zsh 일반 배열은 기본 옵션에서 1부터 센다(`${arr[1]}`이 첫 원소). `KSH_ARRAYS`에서는 0부터 세며 Bash indexed array도 0부터 센다. 양쪽에서 도는 코드는 첨자 반복 대신 `for x in "${arr[@]}"`를 사용한다.

4. **복잡도와 조건 수를 분리한다.**

   - 복잡도는 기존 4축 표로 판정한다.
   - 조건 수는 자동 RE 2·DG 4와 형식상 `N/A`를 제외한 “기능 조건 수”로 정의한다.
   - 단순 작업의 기능 조건 1~3개는 내부 정책임을 명시한다.
   - 해당 없는 카테고리는 `N/A (사유)` 한 줄로 접는다.
   - Gotcha와 red-flags의 “안티패턴 최소 2개”는 `AP-00` 허용 규칙과 동기화한다.
   - 트리거 기준은 바꾸지 않는다.

5. **모든 사람이 전사하는 시각은 명령 출력으로 채운다.**

   - `created`와 `Evaluated`는 `date '+%Y-%m-%d %H:%M'` 출력에서 가져온다.
   - 동의 앵커는 AskUserQuestion의 호출 시각이 아니라 답변 시각을 사용한다.
   - 서로 다른 시간대 기록과 비교할 가능성이 있으면 원본 ISO 타임스탬프도 보존한다.

6. **조건 문장 하나에는 한 판정 단위만 둔다.**

   - one When–Then은 “공식 표준”이 아니라 복합 조건 탐지 휴리스틱이라고 정확히 표현한다.
   - 여러 `And` 자체를 금지하지 말고, 서로 독립적으로 FAIL할 수 있는 결과가 함께 있으면 조건을 분리한다.

7. **도구 부재 처리는 필수성과 fallback 여부로 나눈다.**

   - 필수 도구이고 대체 경로가 없으면 첫 줄에 도구명·실패 출력·재실행 명령을 알리고 중단한다.
   - fallback이 있으면 즉시 중단하지 말고 기존 3단계 fallback을 수행한다.

8. **종료 출력은 짧게 고정한다.**

   - sprint-contract 5단계 DRAFT 끝
   - `/sprint` QA 결과 블록 끝
   - `/sprint` 6단계 보고 끝

   각각 `사용자가 할 일: {없음 | 한 줄}`을 둔다. 이는 외부 표준이 아니라 이번 18세션 마찰을 줄이기 위한 로컬 UX 정책으로 표시한다.

## 5. 못 가져온 것 / 열린 질문

- “단순 작업 기능 조건 1~3개”라는 정확한 수치를 지지하는 외부 연구는 찾지 못했다. 외부 자료는 짧고 단일 목적의 조건을 권하지만 고정 개수는 주지 않는다.
- `N/A (사유)` 형식과 자동 RE/DG 제외 계수는 이 모노레포 고유 스키마이므로 외부 표준 근거가 없다.
- “사용자가 할 일” 끝맺음 문구의 직접적인 외부 근거는 찾지 못했다.
- F21의 “도구가 없으면 무조건 Step 0에서 중단”을 직접 지지하는 근거는 찾지 못했다. 필수 도구와 fallback 가능한 도구를 구분해야 한다.
- Acceptance criteria anti-patterns 2026 별도 최신 자료는 조회하지 않았다. 중지 조건인 필수 소스 3건 이상과 항목 1~3 근거가 확보된 시점에 조회를 멈췄다.
- `v5.5 추가`와 현재 스키마 `v5.4`의 불일치는 단순 오기인지 선점된 차기 버전인지 레포만으로 확정할 수 없다. Phase 2에서 버전 정책 결정을 내려야 한다.
