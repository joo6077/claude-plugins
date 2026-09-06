---
feature: "harness 코어 결함 3건 — 태그 되먹임 · RE/DG 정본 정합 · markdown 킷 오라클"
slug: harness-core-defects
created: "2026-09-06 11:50"
complexity: "복잡"
conditions: 22
status: done
owner_session: 44c7700e-f565-4643-8410-e162aa7d93d5
conditions_digest: sha256:459a7c625948ffcb
locked_at: "2026-09-06 11:41"
---

## 배경

**결함 B (근본 원인)** — QA 가 붙이는 결함 태그와 계약 작성 preflight 태그가 **서로 다른 어휘**다.
평가자 집합 5 종(`qa-evaluator.md:812`): `측정-상태-모호` · `태그-산출물-불일치` · `측정-중복` ·
`범위-미명시` · `증거-경로-부재`. 작성 집합 6 종(`contract-schema.md:693-702`): `측정-수단-부재` ·
`측정-방식-불일치` · `측정-환경-오염` · `측정-산출물-부재` · `검증경로-미기재` · `측정-중복`.
**교집합이 `측정-중복` 하나뿐**이라, QA 가 3 회 붙인 `측정-상태-모호` 가 작성 단계로 되먹여질
자리가 없다. 되먹임 루프가 끊겨 같은 결함이 계속 재생산된다.

관련해서 "계약에 리터럴 환경값을 박지 마라" 규칙은 레포에 **0 건**이고(grep 확인),
`Given:` 은 diff-scope 와 상태의존 명령 두 경우에만 한정돼 있다
(`contract-design-guide.md:566-600`).

**결함 A** — `RE-01`/`RE-02` 문구가 정본(`sprint-contract/SKILL.md:502-503`)과
`contract-schema.md:720-721` 에서 다르다.

**결함 C** — `DG-01`~`DG-04` 문구가 정본(`sprint-contract/SKILL.md:505-508`)과
`contract-schema.md:729-733` 에서 다르다. 특히 `DG-02` 는 정본이 "IDE diagnostics" 인데
스키마는 "analyze 에러" 로 **의미가 다르다.** 또 `commands.lint` 는 어떤 DG 조건과도 연결돼
있지 않다(`README.md:94`). 그리고 "마커는 `[미검증]` 통일, N/A 금지"
(`qa-evaluation-guide.md:1015`)와 "빈 카테고리 `XX-00: N/A` 허용"
(`sprint-contract/SKILL.md:584`)이 충돌한다. 이식 가능한 선례는
`qa-evaluation-guide.md:1497-1509` 의 `N/A (사유)` 표기다.

## 범위 경계

- 대상 6 파일. `harness/templates/project.yaml` 과 `.harness/project.yaml` 은 **제외** —
  `commands.lint` 는 이미 선택 필드로 존재하며 스키마 변경 없이 문서 연결만으로 해소된다.
- 이탈 문구 전수 조사 결과 29 건 중 이탈 15 건이었으나, 문맥 확인 결과 **9 건은 정당**하다:
  `contract-schema.md:450-451` 은 aggregation mode 예시, `contract-design-guide.md:526,535` 는
  금지/허용 대비 예시, `fixture-a~e` 의 `DG-01` 5 건은 `{commands.analyze}` 가 실제 값으로
  치환된 정상 인스턴스다. **이 9 건을 고치면 안 된다.**
- 진짜 이탈은 `contract-schema.md` 의 자동 포함 블록 6 줄뿐이다.
- 기존에 저장된 계약·피드백의 옛 태그는 소급 수정하지 않는다 (write-once).
- 커버리지 해소: SK-01 — 통합 어휘 10 종을 조건 산문과 측정 절에 동일 백틱 표기로 열거했다.
- 커버리지 해소: AR-01 — 정당 예시 9 건의 경로·라인을 측정 절에 개별 열거했다.

## Skill

- [ ] SK-01: 통합 결함 태그 어휘가 단일 SSOT 에 정의되고, 평가자 5 종과 작성 6 종의 합집합 10 종 `측정-수단-부재` · `측정-방식-불일치` · `측정-환경-오염` · `측정-산출물-부재` · `검증경로-미기재` · `측정-중복` · `측정-상태-모호` · `태그-산출물-불일치` · `범위-미명시` · `증거-경로-부재` 이 모두 등재된다 [exact, enumerated] (측정: `harness/references/contract-schema.md` 의 통합 어휘 표에서 10 종 각각 `grep -c` >= 1)
- [ ] SK-02: 통합 어휘 표의 모든 행이 **평가자 측 판정 기준**과 **작성자 측 자문** 두 열을 모두 채운다 — 한쪽만 있는 행이 0 개다 [exact, enumerated] (측정: 표 파싱 후 10 행 각각 두 열이 비어 있지 않음을 확인, 빈 칸 수 == 0)
- [ ] SK-03: `sprint-contract/SKILL.md` 의 조건 작성 절차가 통합 어휘 SSOT 를 참조하며, 평가자 전용 4 종 `측정-상태-모호` · `태그-산출물-불일치` · `범위-미명시` · `증거-경로-부재` 에 대한 작성 단계 자문이 존재한다 [exact, enumerated] (측정: 4 종 각각이 SSOT 표에서 작성 측 열을 갖는지 + `sprint-contract/SKILL.md` 가 그 표를 경로로 참조하는지 `grep -c` >= 1)
- [ ] SK-04: 계약 조건에 리터럴 환경값(버전·절대경로·호스트명·계정 ID)을 박는 것을 금지하고 `Given:` 으로 환경 전제를 선언하도록 요구하는 규칙이 존재한다 [structural] (측정: `리터럴 환경값` 문자열이 `contract-design-guide.md` 에 1 건 이상, 현재 baseline 0 건)

## Script

- [ ] SC-01: `contract-schema.md` 의 자동 포함 `Reusability` 블록 2 줄이 정본 `sprint-contract/SKILL.md` 와 **문자 단위로 일치**한다 [exact, enumerated] (측정: 두 파일에서 `RE-01`/`RE-02` 자동 포함 블록 줄을 추출해 문자열 비교, 불일치 0 건) 음성 대조: 정본의 `RE-02` 문구를 한 글자 바꾸면 이 비교가 불일치 1 건을 낸다
- [ ] SC-02: `contract-schema.md` 의 자동 포함 `Diagnostics` 블록 4 줄이 정본과 **문자 단위로 일치**한다 [exact, enumerated] (측정: 두 파일에서 `DG-01`~`DG-04` 자동 포함 블록 줄을 추출해 문자열 비교, 불일치 0 건) 음성 대조: 정본의 `DG-02` 를 "analyze 에러 0건" 으로 되돌리면 불일치 1 건이 난다
- [ ] SC-03: 정당한 예시 9 건이 보존된다 — `contract-schema.md` 의 aggregation 예시 2 줄, `contract-design-guide.md` 의 금지/허용 대비 예시 2 줄, `fixture-a`~`fixture-e` 의 치환된 `DG-01` 5 줄이 변경 전과 동일하다 [exact, enumerated] (측정: `git diff -- harness/evals/test-fixtures/` 가 빈 출력이고, 두 가이드 파일에서 `RE-01: References 에 g1` · `DG-04: 런타임 에러가 없다` · `DG-04: 앱 구동 시 console` 각각 `grep -c` == 1)
- [ ] SC-04: `python3 scripts/validate-plugin.py harness` 가 exit 0 으로 통과한다 [goal] (측정: 명령 실행 후 `echo $?` == 0)

## Error

- [ ] ER-01: `N/A` 와 `[미검증]` 의 사용 경계가 명시되고 서로 충돌하지 않는다 — `[미검증]` 은 검증 도구·환경 부재, `N/A (사유)` 는 조건이 대상에 애초에 적용 불가인 경우로 갈린다 [structural] (측정: `qa-evaluation-guide.md` 에 두 마커의 구분 문단 1 건 이상 + `N/A` 를 `[미검증]` 동의어로 금지하는 기존 문장과 양립함을 같은 문단에서 명시)
- [ ] ER-02: markdown 전용 킷처럼 `commands.analyze` 가 적용되지 않는 프로젝트에서 `DG-01`/`DG-02` 를 어떻게 처리할지가 명시된다 [structural] (측정: 해당 분기를 다루는 문단 1 건 이상, `N/A (사유)` 표기 사용)

## Architecture

- [ ] AR-01: `commands.lint` 가 최소 1 개 DG 조건과 연결되어 문서화된다 [exact] (측정: `harness/README.md` 의 `commands.lint` 행에 `DG-` 로 시작하는 조건 ID 가 1 건 이상)
- [ ] AR-02: 통합 어휘가 단일 SSOT 에만 정의되고 나머지 파일은 그 경로를 참조한다 — 같은 표를 2 곳 이상에 복제하지 않는다 [exact, enumerated] (측정: 10 종 태그를 모두 담은 표가 존재하는 파일이 정확히 1 개, 나머지 파일은 그 파일 경로를 참조)
- [ ] AR-03: 변경 범위가 한정된다. Given: 계약 봉인 후 구현 완료 시점, 아직 커밋하지 않은 상태. `git diff --name-only -- harness/` 결과가 6 개 이내이고 `harness/evals/` 경로 0 건이다 [exact, enumerated] (측정: 해당 명령 출력 전체를 인용. baseline: 계약 작성 시점 이 명령 출력 0 파일)

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다
- [ ] AP-03: bare code fence 금지 — validate-plugin V6 FAIL (언어 힌트 필수: ```text, ```bash, ```yaml 등)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (제외 없음)
- [ ] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 변경한 문서 규약대로 계약을 1 건 작성해 Step 6.5 게이트가 위반 0 건으로 통과한다
