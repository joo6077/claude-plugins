---
feature: "카이젠 2026-08-13 Final — Phase 1~14 크로스 정합성 검증"
created: "2026-08-13 (Step F1)"
rewritten: "2026-08-14 (v2 — ER-02 자기참조 측정 결함 · AR-04 아티팩트 재구축)"
complexity: "복잡"
conditions: 25
slug: kaizen-final-2026-08-13
status: active
owner_session: df1b3e15-30b3-4825-a3c4-4ac44c686e94
supersedes_digest: sha256:06c72d3b16851613
supersedes_commit: 107d98f
conditions_digest: sha256:2d5170ea874584bc
locked_at: "2026-08-14 (v2)"
---

## 폐기·재작성 (v2) — 앵커 있는 교체

원 계약(`107d98f`, digest `sha256:06c72d3b16851613`)은 폐기됐다. 원문은 git 이력에 보존된다.

### 폐기 사유 — ER-02 가 원문 그대로 만족 불가능

**ER-02 의 산문과 측정문이 서로 다른 것을 잰다.** 산문은 "**사이클 산출물**에 미해소 항목이 없다"
즉 Phase 피드백을 가리키는데, 측정 glob `.harness/sprint-feedback-kaizen-*.md` 가
**Final 자신의 피드백 파일까지** 잡는다. iteration 1 이 REJECT 를 그 파일에 쓰는 순간
iteration 2 이후로는 **구조적으로 통과가 불가능**해진다 (자기 REJECT 를 자기가 읽는다).

`DG-02` 에는 "Final 계약 파일 자신과 그 QA 피드백 파일은 예외" 라는 자기참조 카브아웃이 있는데
`ER-02` 에 그것을 대칭 적용하는 것을 빠뜨렸다. 이번 사이클 Phase 2 가 처리한
**산문↔측정문 커버리지 갭(F1)** 과 정확히 같은 유형의 결함이다.

### 함께 개정한 것 — AR-04

iteration 2 가 AR-04 를 문자 그대로는 PASS 시켰으나(15 계약 전부 `status: done`),
**전환의 정당성 근거**를 파고들어 blocking 했다: 글로벌 피드백 풀에 독립 qa-evaluator 아티팩트가
15 중 2 건(phase10 · phase11)뿐이었다.

근본원인이 규명됐다 — 오케스트레이터가 QA 서브에이전트에 **structured output schema 를 강제**해서
에이전트가 출력 계약을 만족시키고 종료했고, 그 결과 `qa-evaluator` 의 **피드백 저장 단계가
실행되지 않았다.** 판정 자체는 실재한다 (워크플로 저널 27 건 · 에이전트 트랜스크립트 63 개).
그러나 그것은 오케스트레이션 산물이고, **다음 사이클 데이터 풀 §1 이 먹는 것은 글로벌 풀**이다.
저장이 안 되면 다음 카이젠이 굶는다.

**처리**: 사용자가 3 선택지(저널을 아티팩트로 인정 / Phase QA 재실행 / 저널에서 백필) 중
**"Phase QA 재실행"** 을 택했다. schema 를 강제하지 않고 재평가하여 아티팩트를 정상 생성한다.
AR-04 의 측정문을 **아티팩트 실재 확인**으로 명시화한다.

### 앵커

- **승인 주체**: 사용자. 2026-08-14, 오케스트레이터가 근거와 함께 선택지를 제시하고 승인받았다.
- **재작성 주체**: 오케스트레이터. 구현 서브에이전트가 자기 산출물을 허용하려 고친 것이 아니다.
- 변경은 **ER-02 와 AR-04 두 조건의 측정문**뿐이며 나머지 23 조건은 문구 무수정이다.

## 배경

Phase 1~14 가 전부 CHANGED + QA APPROVE 로 끝났다. 각 Phase 는 **자기 scope 안에서만** 평가됐으므로,
Phase 간 정합성은 아직 아무도 보지 않았다. 이 계약은 그 공백을 메운다.

특히 이번 사이클은 **사실 정정 사이클**이었다. 14 종의 정정이 각 Phase 의 scope 안에서 이뤄졌는데,
같은 오류가 **다른 Phase 의 scope 에 남아 있을 수 있다.** 예: Phase 1 이 "서브에이전트 중첩 불가" 를
설계 가이드에서 정정했지만 kit 문서에 같은 단정이 남아 있으면 사이클 전체가 자기모순이다.
조건 SK-02~SK-07 이 그것을 전 레포 범위로 재검사한다.

또 Phase 3 이 만든 canonical 프로토콜 2 종(Unverified-Evidence · User-Reported Failure)을
Phase 5~14 의 kit reviewer 들이 **인용해야 하고 재정의하면 안 된다.** RE-01 이 이것을 잰다.

## 리서치 소스

외부 조회 0 회. 이 계약은 레포 내부 정합성만 검사하므로 외부 근거가 필요 없다.
각 Phase 의 근거는 `.harness/.meta/evidence/phase1~14.md` 에 고정돼 있고 이미 소비됐다.

## GAP 분석

- 각 Phase QA 는 **자기 scope 격리**만 봤다 (해당 커밋의 파일이 계약 경로 안인지).
  Phase 간 **내용 모순**은 어느 QA 도 보지 않았다.
- `validate-post-kaizen.py` 는 구조 검사(버전 bump · 동기화 · scope 격리)를 하지만
  **사실 정정의 전 레포 잔존 여부**는 검사하지 않는다.
- 사이클 종료 산출물 5 종은 F4 소관이라 현재 유예 상태다. 이 계약은 그것을 판정하지 않는다.

## 범위 경계

- **이 계약은 읽기 전용 검증이다.** 구현 변경을 요구하지 않는다.
  조건이 FAIL 이면 해당 Phase 로 돌아가 수정한 뒤 Final 을 재실행한다.
- Step F2(docs-site) · F3(피드백 정리) · F4(PR) 산출물은 **이 계약의 대상이 아니다.**
  `validate-post-kaizen.py` 가 그것을 "종료 단계 미도래" 로 유예하는 것과 정합한다.
- 스프린트 base = `main`. 측정은 전부 `main..HEAD` 또는 현재 작업트리 기준이다.

## 회귀 게이트

`python3 scripts/validate-plugin.py` exit 0 · `python3 scripts/validate-post-kaizen.py` 의
FAIL 이 `docs-site-regen` 1 건 이하 (그 1 건은 F2 소관).

## Architecture

- [ ] AR-01: 11 킷의 `plugin.json` 버전이 `marketplace.json` description 의 `[vX.Y.Z ...]` 와 전부 일치한다 [exact, enumerated]
      (측정: 두 소스에서 킷별 버전을 추출해 문자열 비교 — 불일치 0 건.
       `python3 scripts/validate-plugin.py` 의 V7 가 11 킷 전부 OK 이고 exit 0)
- [ ] AR-02: 각 Phase 커밋이 다른 Phase 의 소스 파일을 수정하지 않았다 [exact]
      (측정: `python3 scripts/validate-post-kaizen.py` 의 `scope-isolation` 검사가 PASS)
- [ ] AR-03: 이번 사이클 변경이 계약이 열거하지 않은 킷을 건드리지 않았다 [structural]
      (측정: `git diff --name-only main..HEAD | awk -F/ '{print $1}' | sort -u` 결과가
       11 킷 + `docs` + `scripts` + `.harness` + `.claude` + `.claude-plugin` + `README.md` 안에 든다.
       그 밖의 최상위 경로 0 건)
- [ ] AR-04: Phase 계약이 전부 `status: done` 이고 **독립 QA 아티팩트로 뒷받침된다** [exact, enumerated]
      (측정 2 단계 —
       (a) `.harness/sprint-contract-kaizen-phase*.md` 를 `find` 로 열거해 개수를 **계산**하고
           각 frontmatter `status` 를 추출 — `active` 잔존 0 건. 본 Final 계약 자신은 제외.
       (b) 각 계약마다 `~/.harness/feedback/evaluator/*.yaml` 에서 그 계약을 `contract_path` 로
           참조하고 `verdict: APPROVE` 인 아티팩트가 **1 건 이상** 존재 — 미보유 계약 0 건.
           이 아티팩트는 qa-evaluator 가 직접 쓴 것이어야 하며, 오케스트레이터가 백필한 것은 무효다.
       (b) 가 AR-04 의 본체다. `status: done` 은 결과이고 아티팩트가 근거다)
- [ ] AR-05: 봉인이 기록된 계약은 전부 `SEAL_OK` 다 [exact]
      (측정: `contract-schema.md` §계약 봉인 의 `verify_seal` 을 그대로 구현해
       `.harness/sprint-contract-kaizen-*.md` 전체에 실행 — `SEAL_BROKEN` 0 건.
       `SEAL_ABSENT` 는 하위호환상 실패가 아니다. bash·zsh 양쪽 동일 결과)

## Skill

- [ ] SK-01: Phase 2 의 스키마 버전이 Phase 3 evaluator 가 인용하는 값과 일치한다 [exact]
      (측정: `harness/references/contract-schema.md` 의 현재 스키마 버전 문자열과
       `harness/docs/guides/qa-evaluation-guide.md` 가 인용한 스키마 버전을 각각 명령으로 추출해 비교 — 동일)
- [ ] SK-02: "서브에이전트 중첩 불가" 계열 단정이 레포 전체에 잔존하지 않는다 [exact]
      (측정: `grep -rn` 으로 `harness/` `*-kit/` `flutter-toolkit/` `docs/` 에서 중첩·하위 위임
       금지 단정을 찾고, 공식 문구 *up to three layers below the main conversation* 와 모순되는
       서술이 0 건. **정정 서술 자체는 오탐이므로 Read 로 맥락을 확인해 제외**한다 —
       naive `중첩.*금지` 패턴을 그대로 쓰지 마라)
- [ ] SK-03: WCAG 터치타겟 레벨 귀속이 정확하다 [exact]
      (측정: `grep -rn "44" design-kit/ docs/` 결과 중 44×44 를 **AA** 기준으로 제시한 줄 0 건.
       24×24 = AA (SC 2.5.8), 44×44 = AAA (SC 2.5.5) 귀속이 되어 있다)
- [ ] SK-04: Freezed `when`/`map` 영구 제거 단정이 잔존하지 않는다 [exact]
      (측정: `grep -rn` 으로 `flutter-toolkit/` `docs/flutter/` 에서 Freezed 3 의 when/map
       제거를 **영구·무조건**으로 단정한 줄 0 건. 3.1.0 재추가 사실이 병기돼 있다.
       historical 로그의 `[정정 2026-08-13]` 주석부는 잔존으로 세지 않는다)
- [ ] SK-05: `#[sqlx::test]` 의 격리 단위 오설명이 잔존하지 않는다 [exact]
      (측정: `grep -rn 'sqlx::test' rust-kit docs/rust | grep -E '트랜잭션|롤백' | grep -v '새 테스트 DB'`
       결과 0 행)
- [ ] SK-06: scoring bias 논문을 binary PASS/FAIL 근거로 오인용한 서술이 잔존하지 않는다 [exact]
      (측정: `grep -rn "2506.22316" harness/ docs/` 의 각 줄을 Read 로 확인 —
       binary 강제의 근거로 제시한 줄 0 건. 정정 disclaimer 는 잔존으로 세지 않는다)
- [ ] SK-07: "Projects v2 = GraphQL only" 서술이 잔존하지 않는다 [exact]
      (측정: `grep -rn -i "graphql" planning-kit/ docs/planning/` 의 각 줄을 확인 —
       REST 경로를 함께 명시하지 않은 채 GraphQL 전용이라 단정한 줄 0 건)

## Script

- [ ] SC-01: `python3 scripts/validate-plugin.py` 가 11 킷 전부 OK, exit 0 [exact]
      (측정: 명령을 실행해 마지막 두 줄이 `Total: 11 plugins, 11 OK` 와 `Exit: 0`)
- [ ] SC-02: `python3 scripts/sync-docs.py --check-only` 가 동기화 상태를 보고한다 [exact]
      (측정: 명령 실행 결과에 "모든 README가 동기화 상태입니다" 가 포함되고 exit 0)
- [ ] SC-03: `python3 scripts/sync-orchestrator.py --check-only` 가 drift 0 (exit 0) [exact]
      (측정: 명령 실행 후 `echo $?` 가 0)
- [ ] SC-04: `python3 scripts/validate-doc-contracts.py` 가 violation 0 · not-verifiable 0 [exact]
      (측정: `python3 scripts/validate-post-kaizen.py` 의 `doc-contracts` 항목이 PASS 이고
       violation 0 · not-verifiable 0 을 보고)
- [ ] SC-05: 이번 사이클에 변경된 셸 스크립트가 bash·zsh 양쪽에서 문법 통과한다 [exact, enumerated]
      (측정: `git diff --name-only main..HEAD -- '*.sh'` 로 대상을 열거해 **개수를 계산**하고,
       각각 `bash -n` 과 `zsh -n` 실행 — 실패 0 건)

## Error

- [ ] ER-01: 이번 사이클이 도입한 외부 URL 이 근거 파일 또는 기존 원본에 실재한다 [structural]
      (측정: `git diff main..HEAD` 에서 추가된 줄의 `https?://` URL 을 추출해 중복 제거하고
       **개수를 계산**한 뒤, 각 URL 이 `.harness/.meta/evidence/phase*.md` 또는
       `git show main:<path>` 원본에 존재하는지 대조 — 미추적 URL 0 건.
       미추적이 있으면 그 목록을 근거로 제시하라)
- [ ] ER-02: **Phase** 산출물에 미해소 항목이 남아 있지 않다 [exact, enumerated]
      (측정: `.harness/sprint-feedback-kaizen-phase*.md` 를 `find` 로 열거해 **개수를 계산**하고
       각 파일의 최종 verdict 를 추출 — `APPROVE` 가 아닌 것 0 건, 미검증 카운트 합 0.
       **Final 자신의 피드백 파일(`sprint-feedback-kaizen-final-*.md`)은 제외한다** —
       평가 중인 계약이 자기 직전 라운드 verdict 를 읽으면 iteration 2 이후 구조적으로 통과 불가다.
       DG-02 의 자기참조 카브아웃과 대칭이다)

## Anti-patterns

- [ ] AP-01: 언어 태그 없는 bare code fence 가 0 건이다 [exact]
      (측정: `python3 scripts/validate-post-kaizen.py` 의 `bare-fence` 검사가 PASS,
       V6 가 0 bare 를 보고)
- [ ] AP-02: 계약 본문 사후 편집으로 위반을 소거한 흔적이 없다 [structural]
      (측정: Phase 3 계약의 재작성은 `supersedes_digest` + `supersedes_commit` + §폐기·재작성 절로
       앵커가 기록돼 있다. 그 외 계약 파일에서 `conditions_digest` 가 기록돼 있는데
       `SEAL_BROKEN` 인 것 0 건 — AR-05 와 동일 명령으로 확인)

## Reusability

- [ ] RE-01: Phase 3 canonical 프로토콜 2 종이 kit reviewer 에서 재정의되지 않는다 [exact, enumerated]
      (측정: `*-kit/agents/*-reviewer.md` 를 `find` 로 열거해 **개수를 계산**하고,
       각 파일이 canonical 절을 **인용**하는지 / 임계값·상태어를 **자체 정의**하는지 구분.
       자체 정의 0 건. 도메인 매핑 표를 덧붙이는 것은 재정의가 아니다)
- [ ] RE-02: 등급 원장이 단일 SSOT 로 유지된다 [exact]
      (측정: `skill-design-guide.md` §3.7 등급 원장의 원칙명을 추출하고,
       다른 파일이 같은 원칙명으로 **등급표를 복제**한 것이 0 건.
       참조·인용은 복제가 아니다)

## Diagnostics

- [ ] DG-01: changelog 와 누적 기록 문서에 이번 사이클 엔트리가 존재한다 [exact, enumerated]
      (측정: `docs/kaizen/changelog.md` · `docs/kaizen/flutter-changelog.md` ·
       `docs/kaizen/research-log.md` · `docs/kaizen/flutter-research-log.md` ·
       `docs/{backend,infra,rust,react,flutter,planning,design}/research-log.md`
       11 개 파일을 열거해 **개수를 계산**하고 각각 `2026-08-13` 문자열 포함 — 누락 0 건)
- [ ] DG-02: 작업트리가 clean 하고 미추적 산출물이 없다 [exact]
      (측정: `git status --porcelain` 출력 행 수 0.
       단 이 Final 계약 파일 자신과 그 QA 피드백 파일은 예외로 허용한다)
