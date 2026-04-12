# Kaizen Data Pool

Generated: 2026-04-12T16:38:13
Generator: `scripts/collect-kaizen-data.py`

카이젠 오케스트레이션의 Phase 별 서브에이전트가 참조할 통합 데이터 풀이다. 이 파일은 `scripts/collect-kaizen-data.py` 로 재생성된다 — 수동 수정 금지.

## 1. 글로벌 Evaluator Feedback

- 경로: `/Users/jackson/.harness/feedback/evaluator`
- 총 파일: **100**

### Verdict 분포

- **APPROVE**: 62
- **REJECT**: 38

### Skill 분포

- `qa-evaluator`: 100

### Project 분포

- `claude-plugins`: 99
- `claude-plugins / react-kit phase10-research kaizen`: 1

### 최근 REJECT 사유 (Top 20)

- [2026-04-12] **claude-plugins**: SC-04: finalize-phase.sh 5 pass 실행 시 SCRIPT_DIR: unbound variable로 exit 1
- [2026-04-12] **claude-plugins**: G8-03: finalize-phase.sh --revert 시 git reset --hard 출력 (계약: git revert kaizen-phase-N-pre..HEAD)
- [2026-04-12] **claude-plugins**: G3-03: spawn-kaizen-phase.sh 인자 없을 때 exit 0 (계약: exit 1)
- [2026-04-12] **claude-plugins**: ER-02: flutter 2차 섹션 소스 테이블에 [official]/[blog] 브라켓 태그 컬럼 누락
- [2026-04-12] **claude-plugins**: ER-02: finalize-phase.sh 5 fail --revert 실행 시 SCRIPT_DIR: unbound variable로 exit 1
- [2026-04-12] **claude-plugins**: ER-01: docs/design/research-log.md:402 — blog.weskill.org URL HTTP 404
- [2026-04-12] **claude-plugins**: DG-03: automation-maturity-2026-04-12.md 종합 점수 산술 오류 — 영역별 합계 2+5+5+5+5+5+5=32/35(91%)인데 33/35(94%)로 기재
- [2026-04-12] **claude-plugins**: AR-05: rust-kit templates/ 5개 파일이 rust-kit/skills/ SKILL.md에서 미참조
- [2026-04-12] **claude-plugins**: AR-03: docs/flutter/ 1498줄 (목표 >=1500, 2줄 부족)
- [2026-04-12] **claude-plugins**: AR-03: design/research-log.md 섹션형 구조 — 다른 5개 파일의 번호+테이블 포맷과 불일치
- [2026-04-12] **claude-plugins**: AR-03: 6개 파일 포맷 불일치 (flutter 태그 컬럼 없음, design 파일 완전히 다른 구조)
- [2026-04-12] **claude-plugins**: AP-03: .claude/skills/ 수정 파일 4개에 bare code fence 잔존 (backend-kaizen:55, backend-research:52, infra-kaizen:51, infra-research:52)
- [2026-04-11] **claude-plugins**: OR-08: SKILL.md:174, SKILL.md:239 — 언어 힌트 없는 bare opening fence 2건
- [2026-04-11] **claude-plugins**: H-03: rust-api Gotchas에 Composition Root 단일화 원칙 누락
- [2026-04-11] **claude-plugins**: H-01: rust-init/rust-feature Gotchas에 domain event + outbox 원칙 누락
- [2026-04-11] **claude-plugins**: AP-03: 동일 — bare code fence anti-pattern 위반
- [2026-04-10] **claude-plugins**: SK-06: concept.md Accent 행에 #E8965A 구체 hex 확정값 기재 — Gotcha #3 위반
- [2026-04-10] **claude-plugins**: SK-05: react-run/SKILL.md:5의 트리거 키워드 'wasm-pack 빌드'가 react-wasm/SKILL.md:5와 중복. 기존 17개 스킬과 상호 배타 불충족
- [2026-04-10] **claude-plugins**: SC-02: package.json.template 라이브러리 버전 4건이 ^X.0.0 형식 위반 (^0.4.0, ^0.400.0, ^0.7.0, ^5.5.0)
- [2026-04-10] **claude-plugins**: RE-02: react-api의 트리거 키워드 '"API 연동"'이 react-feature의 '"API 연동 화면"'과 부분 중복 — 배타성 위반

### 최근 Improvement Suggestions (Top 15)

- [2026-04-12] **claude-plugins**: 성숙도 리포트 합계 검증 자동화 스크립트 추가 고려
- [2026-04-12] **claude-plugins**: 다음 research-log 작업 시 6개 파일 간 컬럼 구성을 통일하여 AR-03 해석 모호성 제거 권장
- [2026-04-12] **claude-plugins**: 경계값 조건(>= N)은 즉시 측정값 출력 후 비교
- [2026-04-12] **claude-plugins**: validate-plugin V6 스캔 범위를 .claude/skills/ 로 확장하면 향후 미탐지 방지
- [2026-04-12] **claude-plugins**: finalize-phase.sh에 SCRIPT_DIR 정의 추가 (REPO_ROOT 정의 직후)
- [2026-04-12] **claude-plugins**: append-audit-log.py 호출 인자를 실제 지원 인자(--cycle-id)로 교체
- [2026-04-12] **claude-plugins**: I-07 commit prefix 조건에 fix(scripts): 같은 bug-fix 커밋 prefix도 허용하는 표현 추가 권장
- [2026-04-12] **claude-plugins**: Gotchas 카운팅 시 H1/H2 형태를 모두 고려하는 범용 정규식 사용
- [2026-04-12] **claude-plugins**: G8-03: git revert 명령으로 교체
- [2026-04-12] **claude-plugins**: G3-03: 인자 없음 분기를 --help 분기와 분리하여 exit 1 처리
- [2026-04-12] **claude-plugins**: ER-02의 태그 요구사항을 테이블 컬럼 레벨인지 인사이트 본문 레벨인지 계약에서 명시 필요
- [2026-04-12] **claude-plugins**: ER-01 수정: design/research-log.md 섹션 10의 404 URL을 대체 URL로 교체
- [2026-04-12] **claude-plugins**: AR-03의 일관된 포맷 정의를 더 구체적으로 (열 이름까지) 명시 필요
- [2026-04-12] **claude-plugins**: AR-03 수정: design 파일을 번호+테이블 포맷으로 재구성하거나 계약 조건 재정의
- [2026-04-11] **claude-plugins / react-kit phase10-research kaizen**: Gotchas 헤더 요약(L15)을 Library Policy 정식 섹션과 동기화 유지하는 관례 추가 권장 (animate.css 누락됨)

## 2. 외부 프로젝트 (`Hub/10_Dev`) 피드백

- Hub 루트: `/Users/jackson/Hub/10_Dev`
- 발견된 프로젝트: **2**

### `apps`

- 경로: `/Users/jackson/Hub/10_Dev/apps`
- sprint-feedback.md: 507 lines
- history sprint-contracts: 24
- 최근 contracts:
  - 20260411-2321-sprint-contract.md
  - 20260411-2324-sprint-contract.md
  - 20260412-0010-sprint-contract.md
  - 20260412-1259-sprint-contract.md
  - 20260412-1430-sprint-contract.md

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: AdmPropertySectionWidget 공통 섹션 컨테이너
Evaluated: 2026-04-12 17:00
Verdict: REJECT
Iteration: 1

---

## Results

### UI (4/5)

- [x] UI-01: 컨테이너 어두운 배경 + border-radius 10 + padding 20 — PASS [L3]
  - 근거: `property_section_widget.dart:53-55` bgColor = darkPanel, radius = AdmSizes.r10, pad = EdgeInsets.all(AdmSizes.w20)
  - 비고: Sprint Contract는 `#222`(= #222222) 명시, 구현은 `AdmColors.darkPanel = #212121`. 두 값이 다르나 darkPanel은 피그마 노드 14644:26557의 실제 패널 토큰이므로 계약 문구 "#222"는 근사값으로 해석. 피그마 노드가 계약에 명시되어 있어 토큰 기준으로 PASS 처리.

- [x] UI-02: title 있는 섹션 — 타이틀(Body M, white) + gap 10 + child pl 20 — PASS [L3]
  - 근거: `property_section_widget.dart:86-107` titleStyle=AdmTextStyles.bodyM.copyWith(color:textOnDark), titleGap=h10, contentPad=EdgeInsets.only(left:AdmSizes.w20)

- [x] UI-03: title 없는 섹션 — child만 직접 표시, 들여쓰기 없음 — PASS [L3]
```

</details>

### `fit-pal`

- 경로: `/Users/jackson/Hub/10_Dev/fit-pal`
- sprint-feedback.md: 109 lines
- history sprint-contracts: 0

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: Monorepo Makefile
Evaluated: 2026-03-30 16:00
Verdict: APPROVE
Iteration: 2

## Results

### Flutter App 커맨드 (15/15)
- [x] app-run (dev, dart-define + observatory-port 포함): PASS
  - 근거: `Makefile:24` — `--dart-define-from-file=.dart_defines.json --observatory-port=8181` 모두 포함. launch.json:13과 일치
- [x] app-run-staging: PASS
  - 근거: `Makefile:29-30`
- [x] app-run-prod: PASS
  - 근거: `Makefile:32-33`
- [x] app-run-profile: PASS
  - 근거: `Makefile:26-27` — launch.json:22(App: Dev Profile)에 observatory-port 없음, Makefile도 동일하게 없음. 일치
- [x] app-test: PASS
  - 근거: `Makefile:39-40`
- [x] app-analyze: PASS
```

</details>


## 3. Followup 문서

- `docs/superpowers/followup-2026-04-11-plugin-validation-findings.md`

## 4. 현재 레포 최근 Sprint Contracts

- `.harness/history/20260411-2226-phase7-sprint-contract.md`
- `.harness/history/20260411-2248-phase8-sprint-contract.md`
- `.harness/history/20260411-2318-phase9-sprint-contract.md`
- `.harness/history/20260411-2335-phase10-sprint-contract.md`
- `.harness/history/20260411-kaizen-phase6-design-kit-sprint-contract.md`
- `.harness/history/20260411-phase5-flutter-toolkit-sprint-contract.md`
- `.harness/history/20260412-0045-post-missing-items-sprint-contract.md`
- `.harness/history/20260412-0115-automation-gap-10-sprint-contract.md`
- `.harness/history/20260412-1255-sprint-contract.md`
- `.harness/history/20260412-1302-sprint-contract.md`

## 5. Validate-Plugin 최근 실행 스냅샷

```text
=== harness ===
  V1 frontmatter     7 skills + 1 agent — OK
  V2 templates       2 parsed, 1 skipped (ts/js) — OK
  V3 refs            0 links — OK
  V4 triggers        26 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.3.6 matches marketplace — OK

=== flutter-toolkit ===
  V1 frontmatter     18 skills + 1 agent — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        141 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.5.1 matches marketplace — OK

=== design-kit ===
  V1 frontmatter     7 skills + 1 agent — OK
  V2 templates       8 skipped (ts/js) — OK
  V3 refs            0 links — OK
  V4 triggers        39 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.2.1 matches marketplace — OK

=== backend-kit ===
  V1 frontmatter     3 skills + 1 agent — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        12 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.1.1 matches marketplace — OK

=== infra-kit ===
  V1 frontmatter     3 skills + 1 agent — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        12 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.1.1 matches marketplace — OK

=== rust-kit ===
  V1 frontmatter     16 skills + 1 agent — OK
  V2 templates       1 parsed, 4 skipped (ts/js) — OK
  V3 refs            0 links — OK
  V4 triggers        79 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.1.1 matches marketplace — OK

=== react-kit ===
  V1 frontmatter     21 skills + 3 agents — OK
  V2 templates       5 parsed, 4 skipped (ts/js) — OK
  V3 refs            0 links — OK
  V4 triggers        156 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.1.1 matches marketplace — OK

Total: 7 plugins, 7 OK
Exit: 0
```


## 6. Phase 별 참조 가이드

각 Phase subagent 는 아래 매핑을 참고하여 자신의 범위에 맞는 섹션을 우선 읽는다.

| Phase | 스킬 | 주요 참조 섹션 |
|-------|------|---------------|
| 1 설계 가이드 | skill-design-guide, agent-design-guide | §1 Improvement Suggestions |
| 2 Contract | contract-design-guide + sprint-contract | §1 Reject 사유 (계약 모호성) |
| 3 Evaluator | qa-evaluation-guide + qa-evaluator | §1 Improvement (L3, set intersection) |
| 4 Harness | harness/skills/* (sprint-contract, qa-evaluator 제외) | §5 validate-plugin 현재 상태 |
| 5 Flutter | flutter-toolkit/skills/* | §2 Hub 외부 프로젝트 (fit-pal, apps) |
| 6 Design | design-kit/skills/* | §5 validate-plugin 현재 상태 |
| 7 Backend | backend-kit/skills/* | §1 Backend 관련 feedback (있다면) |
| 8 Infra | infra-kit/skills/* | §5 validate-plugin 현재 상태 |
| 9 Rust | rust-kit/skills/* | §2 Hub 외부 프로젝트 (fit-pal server) |
| 10 React | react-kit/skills/* | §3 followup-2026-04-11, §5 |

