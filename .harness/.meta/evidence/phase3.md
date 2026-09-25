---
phase: 3
title: "Phase 3 evaluator — 확보된 외부 근거"
collected: 2026-09-24
method: codex (foreground, 직접 호출 · gpt-5.6-sol · 조회는 curl/gh)
inputs: 처리 배정표(.claude/kaizen-input/insights-report.md)의 Phase 3 행 · phase-research-templates.md Phase 3 필수 출처 · 현행화 점검
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치를 지어내지 마라. 없으면 미반영으로 남긴다.
---

요청 범위는 읽기 전용으로 조사했으며 파일 변경은 하지 않았다.

## 1. 출처 목록

실제로 조회한 출처만 적었다.

### 지정 학술 출처

1. [Judging the Judges: Position Bias — arXiv 2406.07791](https://arxiv.org/abs/2406.07791)
2. [Self-Preference Bias in LLM-as-a-Judge — arXiv 2410.21819](https://arxiv.org/abs/2410.21819)
3. [Evaluating Scoring Bias in LLM-as-a-Judge — arXiv 2506.22316](https://arxiv.org/html/2506.22316v1)
4. [A Survey on LLM-as-a-Judge — arXiv 2411.15594](https://arxiv.org/html/2411.15594v6)
5. [CheckEval — arXiv 2403.18771](https://arxiv.org/abs/2403.18771)
6. [Recursive Rubric Decomposition — arXiv 2602.05125](https://arxiv.org/html/2602.05125v1/)

### 공식 문서·1차 출처

7. [MITRE CWE-20: Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html)
8. [MITRE CWE-754: Improper Check for Exceptional Conditions](https://cwe.mitre.org/data/definitions/754.html)
9. [pytest Exit Codes](https://docs.pytest.org/en/stable/reference/exit-codes.html)
10. [zsh Parameter Expansion](https://zsh.sourceforge.io/Doc/Release/Expansion.html)
11. [zsh Array Parameters/Subscripts](https://zsh.sourceforge.io/Doc/Release/Parameters.html)
12. [GNU Bash Arrays](https://www.gnu.org/software/bash/manual/html_node/Arrays.html)
13. [Git diff 공식 문서](https://git-scm.com/docs/git-diff)
14. [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference)
15. [Claude Code Subagents](https://code.claude.com/docs/en/sub-agents)
16. [Claude Code v2.1.281 release](https://github.com/anthropics/claude-code/releases/tag/v2.1.281)
17. [zsh 5.9.2 tag](https://github.com/zsh-users/zsh/releases/tag/zsh-5.9.2)
18. [Git 2.55.0 tag](https://github.com/git/git/releases/tag/v2.55.0)
19. [GNU Bash 5.3 Reference Manual](https://www.gnu.org/software/bash/manual/html_node/Arrays.html)

## 2. 항목별 관찰 사실

### Phase 3 evaluator / harness:P04

#### ① 첫 칸만 읽는 검사

- CWE-20은 입력의 길이·형식·범위뿐 아니라 “missing or extra inputs”, 관련 필드 간 일관성 등 잠재적으로 관련 있는 모든 속성을 검증하라고 권고한다. 여러 입력을 받으면서 첫 항목만 검사하는 구현은 이 원칙에 맞지 않는다. [MITRE CWE-20](https://cwe.mitre.org/data/definitions/20.html)
- position-bias 논문은 후보 순서를 바꿔도 같은 내용을 선택하는지를 `Position Consistency`로 측정한다. pairwise에서는 `(A,B)`와 `(B,A)`, list-wise에서는 후보가 각 위치에 나타나도록 순열을 만든다. 따라서 “위반을 둘째 이후 칸으로 옮겨 재실행”은 순서에 종속된 검사를 드러내는 합리적인 변형이다. [arXiv 2406.07791](https://arxiv.org/abs/2406.07791)
- 반대 근거/한계: 해당 논문은 LLM 판정 후보의 위치 편향을 연구한 것이지 배열 순회 버그 시험 표준을 제안한 것은 아니다.
- 추론: 이 항목의 더 직접적인 근거는 position bias보다 CWE-20이다. 논문은 “순서를 바꾸어 일관성을 확인한다”는 시험 형태를 보조할 뿐이다.

#### ② 한 칸을 못 읽을 때 전체 검사가 꺼지는 문제

- CWE-754는 드문 예외 조건을 확인하지 않거나 잘못 확인해 crash, exit, restart 또는 unexpected state가 되는 것을 결함으로 분류한다. [MITRE CWE-754](https://cwe.mitre.org/data/definitions/754.html)
- CWE-20은 missing/extra input과 여러 출처에서 결합되는 입력을 함께 고려하라고 한다. 한 입력의 읽기 실패가 다른 입력의 실제 위반을 가리는 것은 이 취지와 맞지 않는다. [MITRE CWE-20](https://cwe.mitre.org/data/definitions/20.html)
- 추론: “읽기 실패 슬롯 번호는 별도 보고하되, 읽을 수 있는 다른 슬롯의 위반 검사는 계속한다”는 mixed-input fixture가 가장 판별력 높은 계약 조건이다.
- 반대 근거/한계: 보안상 모든 입력을 읽어야만 안전한 검사라면 부분 진행보다 fail-closed가 옳을 수 있다. 따라서 계약은 “부분 입력을 독립 검사할 수 있는 검사”에 한정해야 한다.

#### ③ 새 시험 파일이 표에만 있고 실행 목록에서 빠지는 문제

- pytest는 테스트를 하나도 수집하지 못하면 성공이 아니라 exit code 5를 낸다. 즉 “명령은 0으로 끝났다”만으로는 테스트가 실제 수집·실행됐다고 볼 수 없다. [pytest Exit Codes](https://docs.pytest.org/en/stable/reference/exit-codes.html)
- CheckEval은 고수준 판단을 추적 가능한 yes/no 항목으로 분해해야 평가자 간 합의와 해석 가능성이 좋아진다고 보고한다. 12개 evaluator 모델 실험에서 평균 agreement가 0.45 개선됐다. [arXiv 2403.18771](https://arxiv.org/abs/2403.18771)
- 추론: 계약에는 “파일이 표에 있다”와 “실행기가 그 파일을 수집했다”를 별도 boolean으로 두는 것이 타당하다.
- 반대 근거/한계: 모든 테스트 러너가 기본 실행 출력에 파일명을 인쇄하지는 않는다. 따라서 “원 명령 출력에 파일명이 반드시 있어야 한다”는 조건은 러너의 quiet reporter와 충돌할 수 있다. 계약이 해당 이름을 출력하는 verbose/collection 명령을 명시하거나, 원 명령의 수집 목록을 별도 출력하도록 해야 한다.

#### ④ zsh에서 조용히 0이 되는 문제

- zsh는 `SH_WORD_SPLIT`이 켜지지 않은 한 매개변수 확장을 공백으로 자동 분할하지 않는다. 문자열 변수에 파일 목록을 담아 unquoted로 넘기는 코드는 Bash와 다르게 동작할 수 있다. [zsh Parameter Expansion](https://zsh.sourceforge.io/Doc/Release/Expansion.html)
- zsh 배열은 기본적으로 1부터 번호를 매긴다. `KSH_ARRAYS`를 켠 경우에만 다른 의미가 적용된다. [zsh Array Subscripts](https://zsh.sourceforge.io/Doc/Release/Parameters.html)
- Bash indexed array는 0-based다. [GNU Bash Arrays](https://www.gnu.org/software/bash/manual/html_node/Arrays.html)
- 따라서 동일 코드가 `arr[0]` 또는 문자열 목록의 묵시적 word splitting에 의존하면 두 셸에서 읽은 대상 수가 달라질 수 있다.
- 추론: zsh·bash 양쪽 실행과 `read_count` 출력은 이 결함을 직접 검출한다. 단순 exit code 비교보다 대상 수 비교가 중요하다.
- 현재 레포의 셸 설명은 이 공식 동작과 일치한다: [contract-schema.md](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/references/contract-schema.md:74).

#### ⑤ 효과 증명 없이 성공을 말하는 문제

- CheckEval은 평가 기준을 추적 가능한 binary decision으로 분해한다. 이는 단일 총점보다 어느 속성이 결과를 바꿨는지 확인하기 쉽다는 근거다. [arXiv 2403.18771](https://arxiv.org/abs/2403.18771)
- RRD는 거친 rubric을 판별력 있는 세부 기준으로 재귀 분해하고, 잘못 정렬되거나 중복된 기준을 제거한다. 논문은 JudgeBench에서 최대 17.7점 향상을 보고한다. [arXiv 2602.05125](https://arxiv.org/html/2602.05125v1/)
- 추론: 판정 줄을 지운 임시 사본에서도 결과가 같다면 그 판정 줄을 실제로 검사했다는 증거가 없다. “검사가 도입된 파일 자신에게 먼저 실행됐다”는 조건과 함께 두면 self-exemption이나 dead path도 잡을 수 있다.
- 반대 근거/한계: 이번에 조회한 출처 중 “판정 줄을 삭제한 사본”이라는 정확한 mutation 절차를 직접 규정한 1차 출처는 찾지 못했다. 이는 CheckEval/RRD의 판별력 원칙을 구체화한 레포 수준의 추론이다.

#### LLM-as-judge 관련 보강·반대 근거

- position-bias 연구는 swap/permutation 검사를 지지한다. 다만 위치 편향의 방향은 judge·task별로 변동하며, 단순히 “항상 첫 항목 선호”라고 일반화할 수 없다. [arXiv 2406.07791](https://arxiv.org/abs/2406.07791)
- self-preference 연구는 GPT-4가 인간보다 low-perplexity, 즉 더 친숙한 출력에 높은 평가를 주었고 이것이 자기 생성 여부와 무관하게 나타났다고 보고한다. generator와 evaluator 분리 및 구현자 서술 배제에는 보조 근거가 된다. [arXiv 2410.21819](https://arxiv.org/abs/2410.21819)
- survey는 position, self-enhancement, length/verbosity 등 여러 bias와 prompt swap 완화법을 다룬다. 또한 swap 후 충돌을 tie로 처리하거나 점수를 평균하는 방식도 소개한다. [arXiv 2411.15594](https://arxiv.org/html/2411.15594v6)
- scoring-bias 논문이 정의한 것은 score-rubric order, score ID, reference-answer score perturbation이다. binary PASS/FAIL 강제를 주장하지 않는다. [arXiv 2506.22316](https://arxiv.org/html/2506.22316v1)
- 이 점은 현행 문서의 정정과 일치한다: [qa-evaluation-guide.md](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/qa-evaluation-guide.md:124), [qa-evaluation-guide.md](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/qa-evaluation-guide.md:1824).
- binary 분해의 직접 근거는 scoring-bias 논문이 아니라 CheckEval이다. 단, CheckEval도 “최종 verdict는 반드시 단 하나의 PASS/FAIL이어야 한다”고 말한 것은 아니며 세부 기준을 yes/no로 분해한 연구다. [arXiv 2403.18771](https://arxiv.org/abs/2403.18771)

### user-setup:P4

#### (a) 목록·슬롯 전수 확인

CWE-20의 all-relevant-properties 및 missing/extra-input 지침과 position swap 실험이 찬성 근거다. 둘째 이후 칸에만 위반을 둔 사본은 첫 항목 고정·조기 종료를 검출한다. [MITRE CWE-20](https://cwe.mitre.org/data/definitions/20.html), [arXiv 2406.07791](https://arxiv.org/abs/2406.07791)

#### (b) 새 시험 파일의 실제 실행 포함

pytest가 0개 수집을 별도 실패 코드로 취급하므로, 파일 존재와 수집·실행은 구분해야 한다. [pytest Exit Codes](https://docs.pytest.org/en/stable/reference/exit-codes.html)

추론: 실행 기록에 이름이 표시되지 않는 러너에서는 “이름 출력” 자체보다 canonical collection 명령 결과 또는 실행된 테스트 수가 더 이식성 높은 증거다.

#### (c) 읽기 실패와 실제 위반의 동시 입력

CWE-754는 예외 조건 하나가 검사 전체의 비정상 종료나 unexpected state로 이어지는 것을 결함으로 본다. mixed fixture에서 정상 슬롯의 위반과 unreadable 슬롯 번호를 모두 요구하는 조건이 타당하다. [MITRE CWE-754](https://cwe.mitre.org/data/definitions/754.html)

#### (d) 삭제 파일 열거

Git 공식 문서는 `--name-status`가 경로와 상태 문자를 출력하며 `D`가 Deleted를 뜻한다고 정의한다. 따라서 `git diff --name-status <기준>..<끝>`의 `D` 행을 계약 범위와 대조하는 방식은 직접적인 공식 근거가 있다. [Git diff](https://git-scm.com/docs/git-diff)

주의: `A..B`는 두 endpoint 사이 변경이며 working tree의 미커밋 삭제는 포함하지 않는다. 계약은 기준과 끝 커밋 또는 working-tree 포함 여부를 명시해야 한다.

### F16 / F31

레포 전체에서 `F16`, `F31` 키 정의를 찾지 못했다. 이번 요청문에 묶인 다섯 확인 항목 외에는 각 키의 독립 의미를 외부 근거와 1:1 매핑할 수 없다.

추론:

- F16이 “일부 입력만 검사” 계열이라면 CWE-20 및 position permutation이 근거다.
- F31이 “검사가 효과 없이 성공” 계열이라면 CheckEval/RRD와 counterfactual 사본 시험이 근거다.

정확한 매핑은 원 인사이트 원장의 키 설명이 필요하다.

## 3. 현행화 — 낡은 곳

### 외부 도구 최신 상태

| 대상 | 확인한 최신 안정 값 | 레포 현재 값/사용 | 판정 |
|---|---:|---|---|
| Claude Code | v2.1.281, 2026-09-23 | 버전 pin 없음. `model: sonnet`, `tools: Read, Grep, Glob, Bash` 사용 | 낡은 pin 없음. 현재 subagent 문서에도 `sonnet`과 해당 tools 형식이 유효하다. [공식 문서](https://code.claude.com/docs/en/sub-agents), [release](https://github.com/anthropics/claude-code/releases/tag/v2.1.281) |
| Bash | 5.3 | 버전 pin 없음 | 낡은 pin 없음. 배열 0-based 설명과 호환된다. [GNU Bash 5.3 manual](https://www.gnu.org/software/bash/manual/html_node/Arrays.html) |
| zsh | 5.9.2, 2026-07-12 tag | 버전 pin 없음 | 낡은 pin 없음. 1-based 배열 및 `SH_WORD_SPLIT` 차이에 대한 현재 문서 설명과 호환된다. [zsh tag](https://github.com/zsh-users/zsh/releases/tag/zsh-5.9.2) |
| Git | 2.55.0, 2026-06-29 tag | 버전 pin 없음 | 낡은 pin 없음. `--name-status`와 `D` 의미가 현재 문서에도 유지된다. [Git tag](https://github.com/git/git/releases/tag/v2.55.0), [git-diff](https://git-scm.com/docs/git-diff) |

### 2026-08-13 이후 Claude Code 변경 중 이 킷과 관련 가능한 것

- v2.1.233부터 plugin 기본 `agents/` 검증에 `claude plugin validate` 지원이 명시돼 있다. 현행 evaluator 계약에는 이 명령을 요구하지 않으므로 호환성 결함은 아니다. [Plugins Reference](https://code.claude.com/docs/en/plugins-reference)
- v2.1.277에서 deprecated `TaskOutput`이 제거됐다. evaluator는 이를 사용하지 않는다. [v2.1.277 release](https://github.com/anthropics/claude-code/releases/tag/v2.1.277)
- v2.1.281은 self-hosted runner wrapper가 `--system-prompt`를 덧붙이던 경우 file 기반 옵션으로 옮겨야 하는 breaking change를 포함한다. evaluator 파일에는 해당 wrapper나 옵션이 없다. [v2.1.281 release](https://github.com/anthropics/claude-code/releases/tag/v2.1.281)
- plugin agent에서는 `hooks`, `mcpServers`, `permissionMode` frontmatter가 보안상 무시된다. [Plugins Reference](https://code.claude.com/docs/en/plugins-reference) 현행 [qa-evaluator.md](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/agents/qa-evaluator.md:1)는 해당 필드를 쓰지 않으므로 문제없다.

### 실제로 낡거나 불일치한 레포 위치

외부 도구의 고정 버전이 낡은 곳은 찾지 못했다. 다만 내부 버전 메타데이터는 본문 날짜와 이미 어긋난다.

- [qa-evaluation-guide.md](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/qa-evaluation-guide.md:3): 현재 `version: v5.0`.
- [qa-evaluation-guide.md](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/qa-evaluation-guide.md:1912): 현재 “2026-08-13 · v5.0”.
- 같은 파일에는 이미 2026-09 추가 내용이 있다. 예: parity item 15는 [1874행](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/qa-evaluation-guide.md:1874)에 있다.
- [contract-design-guide.md](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/contract-design-guide.md:3) 및 [1292행](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/contract-design-guide.md:1292)도 `v5.0 · 2026-08-13`이지만, 본문에는 2026-09-23 추가 절이 있다([759행](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/contract-design-guide.md:759)).
- 추론: 이번 Phase가 실제 개정을 넣을 때 두 frontmatter와 두 버전 정보 절을 함께 올려야 한다. 다음 버전 번호는 레포 정책·병렬 브랜치 선점 여부에 따라 정해야 하므로 여기서 지어내지 않는다.

출처 정확성 점검:

- [qa-evaluation-guide.md:132](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/qa-evaluation-guide.md:132)의 “12개 이상의 편향”은 이번에 조회한 survey 본문에서 정확한 숫자를 확인하지 못했다. survey가 여러 bias를 분류한다는 사실은 확인했지만 “12개 이상”이라는 수치는 이번 조회만으로 재확인되지 않았다. [Survey](https://arxiv.org/html/2411.15594v6)

## 4. 권장안

이번 Phase 계약 조건으로 삼을 만한 형태는 다음과 같다.

1. `qa-evaluator` 규칙 10 아래에 “산출물 자체가 검사일 때” 특칙을 둔다. 다섯 항목은 질문만 두지 말고 각각 evaluator가 만든 임시 사본, 실행 명령, exit code, 읽은 대상 수, 관찰 출력을 요구한다.

2. 첫 항목 편향 시험은 다음처럼 판정 가능하게 쓴다.

   - 둘째 이후 슬롯에만 위반을 넣는다.
   - 기대값: 검사 FAIL, 해당 슬롯 번호/파일명 출력, `read_count == 전체 슬롯 수`.

3. mixed-input 시험은 하나의 고정 fixture로 둔다.

   - 슬롯 하나는 unreadable.
   - 다른 슬롯에는 실제 위반.
   - 기대값: 실제 위반 검출 + unreadable 슬롯 번호 별도 출력.
   - 전체 검사 success 또는 “위반 없음”이면 FAIL.
   - 안전상 부분 검사가 불가능한 검사에는 별도 fail-closed 계약을 작성한다.

4. 신규 시험 파일 조건은 존재와 실행을 분리한다.

   - 파일 존재.
   - canonical 실행/collection 명령에 포함.
   - 실제 수집된 테스트 수가 0보다 큼.
   - 파일명 출력이 가능한 reporter라면 이름도 증거로 남김.
   - quiet runner라면 “기본 출력에 파일명이 없다”를 곧바로 누락으로 판정하지 않도록 계약에 collection 명령을 명시한다.

5. 셸 조건은 zsh·bash 양쪽에서 다음 값을 출력하게 한다.

   - exit code
   - 후보 슬롯/파일 수
   - 실제 읽은 슬롯/파일 수
   - 위반 수
   - unreadable 수

   배열의 0/1-based 차이와 `SH_WORD_SPLIT` 차이는 공식 문서로 확인된다. [zsh arrays](https://zsh.sourceforge.io/Doc/Release/Parameters.html), [zsh expansion](https://zsh.sourceforge.io/Doc/Release/Expansion.html), [Bash arrays](https://www.gnu.org/software/bash/manual/html_node/Arrays.html)

6. 효과 증명은 “원본 성공”만으로 끝내지 않는다.

   - 판정에 핵심인 줄을 지운 임시 사본에서는 결과가 달라져야 한다.
   - 새 검사를 그 검사 정의 파일 자체에 먼저 실행한다.
   - 결과가 같으면 dead checker로 보고 조건 FAIL.
   - 이는 외부 표준의 직역이 아니라 CheckEval/RRD 판별력 원칙을 적용한 레포 계약임을 명시한다.

7. Step 3.5에는 현재 1~9 뒤에 명시적 10번으로 “산출물이 검사라면 다섯 시험의 실행 결과를 모두 남겼는가”를 추가한다. 현재 위치는 [qa-evaluator.md:786](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/agents/qa-evaluator.md:786)이다.

8. 교차 진단 요청은 현재 두 질문([qa-evaluator.md:1023](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/agents/qa-evaluator.md:1023)) 뒤에 “산출물이 검사일 때 다섯 가지 중 실행하지 않은 것이 있는가?”를 셋째 질문으로 추가한다.

9. `qa-evaluation-guide`에는 동일 목록을 독립 소절로 두되, parity 표에는 한 행만 추가한다. 현재 표는 [qa-evaluation-guide.md:1862](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/qa-evaluation-guide.md:1862)에 있다.

10. 계약 작성자 측 Gotcha는 다음 의미로 고정하는 것이 좋다.

   > 새 검사·새 시험 파일의 조건은 “표에 행이 있다”가 아니라 “canonical 명령을 돌렸을 때 어떤 대상 수·파일명·위반·exit code가 나온다”로 쓴다. unreadable 슬롯과 실제 위반 슬롯이 함께 있는 mixed-input fixture를 하나 둔다.

11. 삭제 범위 조건은 Git 공식 상태 문자를 직접 사용한다.

   ```text
   측정: git diff --name-status <기준>..<끝>
   판정: D 행을 전부 나열하고 계약 허용 삭제 집합과 비교한다.
   계약 범위 밖 D 행이 하나라도 있으면 FAIL.
   ```

   endpoint와 working-tree 포함 여부를 함께 명시해야 한다. [Git diff](https://git-scm.com/docs/git-diff)

12. scoring-bias 논문은 binary PASS/FAIL의 근거로 다시 연결하지 않는다. score prompt perturbation 근거로만 남기고, boolean 분해는 CheckEval에 연결한다. [Scoring Bias](https://arxiv.org/html/2506.22316v1), [CheckEval](https://arxiv.org/abs/2403.18771)

## 5. 못 가져온 것 / 열린 질문

- F16과 F31의 원 인사이트 정의를 레포에서 찾지 못했다. 요청문에 묶인 동작 이상으로 독립 해석하지 않았다.
- survey가 “12개 이상의 편향”을 분류한다는 정확한 숫자는 이번에 조회한 원문에서 확인하지 못했다. 여러 bias 분류와 완화 전략은 확인했다. 확인 실패가 “그 수치가 없다”는 뜻은 아니다.
- 판정 줄 삭제 사본 시험, 자기 검사 파일에 먼저 실행, unreadable+violation 혼합 fixture를 그대로 규정한 외부 1차 출처는 찾지 못했다. 이 세 가지는 CWE-20/CWE-754와 CheckEval/RRD를 적용한 추론이다.
- “원 실행 명령 출력에 새 테스트 파일명이 반드시 찍혀야 한다”는 요구는 quiet reporter와 충돌할 수 있다. 원 명령이 이름을 출력하도록 계약하거나 별도 canonical collection 명령을 정해야 한다.
- Claude Code v2.1.281 이후 릴리스는 조사하지 않았다. 기준일 2026-09-24에 직전 릴리스는 v2.1.281이었다.
