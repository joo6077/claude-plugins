---
feature: "anti_patterns 에 command 필드 추가 — 정규식으로 못 재는 검사 위임"
slug: antipattern-command-field
created: "2026-09-06 15:05"
complexity: "복잡"
conditions: 21
status: active
owner_session: 44c7700e-f565-4643-8410-e162aa7d93d5
conditions_digest: sha256:900a85a9dc5b74bd
locked_at: "2026-09-06 14:59"
---

## 배경

`.harness/project.yaml` 의 `AP-03` 패턴 `^\`\`\`\\s*$` 는 **오탐 100 %** 다.
실측: 이 레포 `harness/` + `bambu-kit/` 에서 **292 건 매치**, `validate-plugin --check=code-fence`
기준 **실제 위반 0 건**.

원인은 구조적이다. 마크다운의 여는 fence 와 닫는 fence 는 **텍스트가 동일**하므로
**줄 단위 정규식으로는 원리적으로 구분할 수 없다.** `scripts/validate-plugin.py` 의
`check_v6_code_fence` 는 `in_block` 플래그를 쓰는 **상태기계**로 판정한다.

그런데 `anti_patterns` 스키마는 `pattern`(ripgrep 정규식) 하나만 갖고
(`harness/README.md` §anti_patterns 상세), `qa-evaluator` 는 그것을 Grep 으로만 소비한다.
즉 **문맥이 필요한 검사를 표현할 방법이 스키마에 없다.** AP-03 은 그것을 정규식으로 억지로
표현하려다 오탐 292 건이 됐다.

발견 경위: 2026-09-06 `harness-attribution-followup` QA 에서 평가자가 지적
(*"정상적으로 닫히는 모든 코드펜스와 상시 매치되는 과매치 구조"*).

## 범위 경계

- 대상 4 파일: `harness/README.md` · `harness/agents/qa-evaluator.md` ·
  `harness/templates/project.yaml` · `.harness/project.yaml`
- `harness/scripts/validate.sh` 는 `id: AP-` 개수만 세고 필드 화이트리스트가 없다 —
  변경 불필요(실측 확인).
- eval fixture 의 `project.yaml` 4 종은 AP-03 이 다른 내용(`http.get|http.post`)이므로 **대상 아님.**
- `scripts/validate-plugin.py` 는 이미 올바르다 — **고치지 않는다.**
- 변경 범위 조건은 경로별 존재 확인으로 잰다 (동시 작성자 오염 내성 — 선행 스프린트 교훈).
- 커버리지 해소: SK-01 · AR-01 — 대상 4 파일을 측정 절에 개별 경로로 열거했다.

## Skill

- [ ] SK-01: `anti_patterns` 스키마에 선택 필드 `command` 가 문서화되고, `pattern` 과의 관계(둘 중 하나 이상 필수 · `command` 가 있으면 그것이 판정 권위)가 명시된다 [structural] (측정: `harness/README.md` §anti_patterns 상세 에 `command` 항목 1 건 이상 + 관계 규칙 문장 1 건 이상)
- [ ] SK-02: 문서가 **언제 `command` 를 써야 하는지**를 판단 기준으로 제시한다 — 줄 단위 정규식으로 판정 불가한 검사(문맥·상태 의존)일 때 [structural] (측정: 판단 기준 문단 1 건 이상, 코드펜스를 실례로 인용)
- [ ] SK-03: `harness/templates/project.yaml` 의 `anti_patterns` 주석 예시에 `command` 형태가 포함된다 [structural] (측정: 해당 파일에서 `command` 문자열 1 건 이상)
- [ ] SK-04: `qa-evaluator` 의 Anti-pattern 검증 절차가 `command` 를 가진 항목을 Grep 이 아니라 **그 명령 실행**으로 판정하도록 분기한다 [structural] (측정: `harness/agents/qa-evaluator.md` Anti-pattern 검증 절에 `command` 분기 문단 1 건 이상)

## Script

- [ ] SC-01: 수정된 `AP-03` 이 오탐을 내지 않는다. Given: baseline 커밋 `8f41a6d`. `.harness/project.yaml` 의 `AP-03` 이 `pattern` 대신 `command` 를 쓰고, 그 명령을 실행하면 실제 위반 건수만 보고한다 [goal] (측정: `AP-03` 의 `command` 값을 그대로 실행해 출력과 exit code 를 인용. 현재 레포 상태에서 위반 0 건이어야 한다) 음성 대조: 어떤 `.md` 에 언어 힌트 없는 여는 fence 를 1 개 넣으면 같은 명령이 그 파일을 지목하며 실패한다
- [ ] SC-02: 기존 `pattern` 전용 항목이 그대로 동작한다 (하위호환) [exact, enumerated] (측정: `.harness/project.yaml` 의 `AP-01` · `AP-02` · `AP-04` 3 종이 `pattern` 필드를 유지하고 `command` 없이 정의돼 있음을 확인)
- [ ] SC-03: `bash harness/scripts/validate.sh` 가 `AP-03` 변경 후에도 에러 0 건으로 통과한다 [goal] (측정: 명령 실행 후 출력과 `echo $?` 인용) 음성 대조: `anti_patterns` 항목을 1 개만 남기면 같은 스크립트가 "최소 2개 권장" 경고를 낸다
- [ ] SC-04: `python3 scripts/validate-plugin.py` 가 exit 0 으로 통과한다 [goal] (측정: `echo $?` == 0)

## Error

- [ ] ER-01: `command` 실행이 불가능한 환경(도구 부재)에서의 처리가 명시된다 — 조용히 PASS 로 넘기지 않고 `[미검증]` 으로 기록한다 [structural] (측정: 해당 분기 문장 1 건 이상)
- [ ] ER-02: `command` 와 `pattern` 이 둘 다 없는 항목은 설정 오류임이 명시된다 [structural] (측정: 해당 규칙 문장 1 건 이상)

## Architecture

- [ ] AR-01: 대상 4 파일이 baseline 이후 실제로 수정됐다 — `harness/README.md` · `harness/agents/qa-evaluator.md` · `harness/templates/project.yaml` · `.harness/project.yaml` [exact, enumerated] (측정: 4 경로 각각 `git diff --name-only 8f41a6d -- <path>` 또는 `git status --porcelain -- <path>` 가 비어 있지 않음)
- [ ] AR-02: `scripts/validate-plugin.py` 와 eval fixture 의 `project.yaml` 4 종이 변경되지 않았다 [exact, enumerated] (측정: `git status --porcelain -- scripts/validate-plugin.py harness/evals/` 가 빈 출력)
- [ ] AR-03: 권위가 한 곳이다 — 코드펜스 판정의 정본이 `scripts/validate-plugin.py` 이고 `project.yaml` 은 그것을 호출만 한다 (판정 로직을 복제하지 않는다) [structural] (측정: `.harness/project.yaml` 의 `AP-03` 에 정규식 기반 판정 로직이 0 건)

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0개 (변경/생성 파일 대상)
- [ ] DG-02: N/A (사유: IDE diagnostics 미적용 확장자 .md/.yaml 만 변경한다)
- [ ] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 수정된 `AP-03` 을 실제 1 회 실행해 오탐 292 건이 0 건으로 줄었음을 수치로 보인다
