---
feature: "kaizen 2026-07-27 Final — 크로스 Phase 정합성 검증 (Phase 1~14 전수 CHANGED)"
created: "2026-07-27 21:40"
complexity: "복잡"
conditions: 18
---

## 배경

2026-07-27 카이젠 사이클에서 Phase 1~14 가 **전부 CHANGED** 되었고 11개 플러그인이 minor bump 되었다.
이번 사이클의 프레이밍은 "새 규칙 추가"가 아니라 **enforcement 등급 상향**(E1 문장 → E2 아티팩트 →
E3 결정론적 게이트)이며, Phase 1 이 정의한 어휘·규약이 하위 12개 Phase 에 일관되게 전파됐는지가
정합성의 핵심이다.

Final 단계는 **새 기능을 추가하지 않는다.** 이미 적용된 변경들 사이의 모순·누락·drift 만 검증한다.

## 리서치 소스

Final 단계는 자체 리서치를 수행하지 않는다. Phase 별 리서치 출처는
`docs/kaizen/research-log.md` 의 `[2026-07-27]` 엔트리에 전량 기록되어 있다.

## 범위 경계

- **측정 baseline**: `da6663c` (직전 사이클 머지 커밋). 모든 diff 조건은 `da6663c..HEAD` 기준.
- 검증 대상은 이 사이클이 만든 커밋 전체이며, 새 소스 변경은 하지 않는다.
- `docs/*.html` 재생성(Step 11.5)은 별도 서브에이전트 산출물이며 이 계약의 AR-04 로 검증한다.

## GAP 분석

Final 이 잡아야 할 drift 후보 (Phase 리포트에서 명시적으로 이관된 것):

1. Phase 1 의 E1/E2/E3 와 `[미검증]` 임계 2건이 **SSOT 한 곳에서만 정의**되고 나머지는 인용인가.
2. Phase 3 의 Canonical Unverified-Evidence Protocol 이 kit reviewer 들에 **문구 변형 없이** 복제됐는가.
3. Counterpart Conditions 의 **evaluator 측 대응 절이 만들어지지 않았는가** (parity item 12 의도된 부재).
4. 11킷 버전이 plugin.json ↔ marketplace.json ↔ orchestrator AUTO 블록 3곳에서 일치하는가.
5. Phase 번호 표기(13=bambu / 14=onboarding)가 전 문서에서 일관되는가.

## 회귀 게이트

`python3 scripts/validate-plugin.py` 가 11 plugins / 11 OK / Exit 0 이어야 한다. 하나라도 ERROR 면 REJECT.

## Architecture

- [ ] AR-01 [exact] `git diff --name-only da6663c..HEAD -- '.claude-plugin/marketplace.json'` 이 정확히 1행. marketplace.json 이 이번 사이클에 갱신되었다.
- [ ] AR-02 [exact] 11개 `*/.claude-plugin/plugin.json` 의 version 이 각각 `harness 0.5.0 · flutter-toolkit 0.6.0 · design-kit 0.3.0 · backend-kit 0.2.0 · infra-kit 0.2.0 · rust-kit 0.2.0 · react-kit 0.2.0 · planning-kit 0.4.0 · reflect-kit 0.5.0 · bambu-kit 0.5.0 · onboarding-kit 0.2.0` 이다.
- [ ] AR-03 [exact] Phase 번호 매핑이 13=bambu / 14=onboarding 으로 일관된다. 측정: 매핑을 **선언**하는 형태만 잡는다 — `grep -rniE "Phase 13 *(—|-|:) *onboarding" .claude/ --include='*.md'` 결과 0건, 그리고 `grep -rniE "Phase 14 *(—|-|:) *onboarding" .claude/skills/kaizen-orchestrator/SKILL.md` 결과 1건 이상. (주의: "Phase 13 bambu-kit 섹션 신설 + Phase 14 onboarding 번호 정정" 처럼 **정정 이력을 서술하는 문장**은 두 토큰을 한 줄에 포함하므로 위반이 아니다 — 매핑을 **선언**하는 문장만 대상.)
- [ ] AR-04 [exact] Step 11.5 대상 9개 HTML(`docs/harness/{skill-design-guide,agent-design-guide,contract-design-guide,qa-evaluation-guide,contract-schema}.html`, `docs/flutter-toolkit/{project-detection,visual-evidence-protocol}.html`, `docs/design-kit/visual-change-protocol.html`, `docs/react-kit/render-evidence-protocol.html`)이 모두 존재하고 각각 400 라인 이상이다.
- [ ] AR-05 [exact] `docs/` 하위에 `research-log.html` 이 0건이다 (사이트 규약상 research-log 는 게시하지 않는다 — detect-docs-drift 오탐을 따라가지 않았음을 확인).

## Skill

- [ ] SK-01 [exact] `harness/docs/guides/skill-design-guide.md` 에 `E1`·`E2`·`E3` 등급 정의가 존재하고, 다른 파일들은 이를 **정의하지 않고 인용만** 한다 — `grep -rln "E3.*결정론적 게이트" harness/ */skills/ */agents/ .claude/skills/` 결과에서 정의문을 가진 파일이 skill-design-guide.md 하나다.
- [ ] SK-02 [exact] Canonical 조항 1 의 **정본 문장**이 정본(`harness/docs/guides/qa-evaluation-guide.md`)과 복제본 7곳(design/infra/rust/planning/react/backend reviewer + `flutter-toolkit/skills/flutter-audit/SKILL.md`)에서 문자 단위로 동일하고, 동의어가 백틱으로 표기되어 있다. 측정: 각 파일에서 `마커는 ... 만들지 않는다.` 까지를 잘라 비교했을 때 고유 문자열 1종. (`design-reviewer` 가 그 뒤에 붙인 `[정적]` 보조 태그 설명은 canonical 을 **대체하지 않고 보강**하는 추가 문장이므로 위반이 아니다.)
- [ ] SK-03 [exact] reviewer 6종(design/backend/infra/rust/react/planning)이 전부 `[미검증]` 임계를 자체 재정의하지 않는다 — 각 파일에 "2건 이상" 을 **자기 규칙으로 선언하는** 문장이 없고 canonical 앵커 인용만 존재한다.
- [ ] SK-04 [exact] **kit reviewer 6종**(`design-kit`/`backend-kit`/`infra-kit`/`rust-kit`/`react-kit`/`planning-kit` 의 `agents/*-reviewer.md`)에 Counterpart 전용 평가 절이 없다 — 해당 6파일 대상 `grep -l "Counterpart"` 결과 0건. (`harness/agents/qa-evaluator.md` 가 참조 목록에서 contract-design-guide 의 목차 항목으로 이 단어를 언급하는 것은 평가 절이 아니므로 대상 밖.)
- [ ] SK-05 [goal] `.claude/skills/*-kaizen/SKILL.md` 중 validate-plugin 카테고리 수를 언급하는 파일이 전부 8(V1~V8)로 기술한다. 측정: `grep -rn "7 카테고리" .claude/skills/` 결과 0건.
- [ ] SK-06 [goal] Phase 1 이 정정한 "서브에이전트 중첩 가능(기본 3층)" 이 `agent-design-guide.md` 에 반영되어 있고, 같은 레포 안에 "중첩 불가"로 단언하는 문장이 남아 있지 않다.

## Script

- [ ] SC-01 [exact] `python3 scripts/validate-plugin.py` 가 `11 plugins, 11 OK` 를 출력하고 Exit 0 이다.
- [ ] SC-02 [exact] `python3 scripts/sync-docs.py --check-only` 가 "모든 README가 동기화 상태입니다" 를 반환한다.
- [ ] SC-03 [exact] `python3 scripts/sync-orchestrator.py --check-only` 가 Exit 0 이다.
- [ ] SC-04 [exact] V5 백틱 인식 회귀 가드: 백틱 밖 `TODO` 는 여전히 검출된다(음성 테스트 PASS), 그리고 `--fix` 실행이 백틱 안 토큰을 변조하지 않는다(대상 파일 해시 불변).
- [ ] SC-05 [exact] `.harness/.meta/kaizen-failure-count.yaml` 이 `yaml.safe_load` 로 파싱되고, 최상위 키가 `last_updated` 와 `phases` 둘뿐이며(중복 키 없음), `phases` 하위에 `phase_1`~`phase_14` 가 존재한다.

## Error

- [ ] ER-01 [exact] `.harness/.meta/cleanup-log.yaml` 에 `2026-07-27` 엔트리가 존재한다 (Step 11.6 실행 증거, 삭제 0건이어도 기록).
- [ ] ER-02 [exact] `.harness/.meta/evals-audit-2026-07-27.md` 가 존재한다.

## Reusability

- [ ] RU-01 [goal] 이번 사이클에 신설된 SSOT 3종(`flutter-toolkit/references/visual-evidence-protocol.md`, `design-kit/references/visual-change-protocol.md`, `react-kit/references/render-evidence-protocol.md`)이 각각 상위 SSOT(skill-design-guide §3.7 / qa-evaluation-guide canonical)를 **인용**하고 임계·등급을 재정의하지 않는다.

## Anti-patterns

- [ ] AP-01 [exact] AP-03(bare code fence) 위반 0건 — validate-plugin V6 가 전 킷에서 `0 bare` 를 보고한다.

## Diagnostics

- [ ] DG-01 [exact] `bash -n scripts/release.sh` 가 Exit 0 이다.
- [ ] DG-02 [exact] 이번 사이클에 수정한 셸/파이썬 스크립트가 문법 검증을 통과한다 — `bash -n scripts/finalize-phase.sh` 와 `python3 -m py_compile scripts/validate-plugin.py scripts/append-audit-log.py scripts/detect-docs-drift.py` 가 각각 Exit 0.
