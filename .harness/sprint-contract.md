---
feature: "react-kit Final Integration Spec (harness + plugin structure + deliverables)"
created: "2026-04-10 19:35"
complexity: "중간"
conditions: 16
scope: "docs/react/kit-design/final-integration.md — react-kit 의 .harness/project.yaml 스키마, 플러그인 파일 구조, marketplace.json 엔트리, 에이전트 파일 경로, README 템플릿 등 최종 산출물 통합 명세"
---

## Harness
- [ ] HA-01: react-kit 전용 .harness/project.yaml 템플릿이 명시되고 stack, commands, contract_categories, anti_patterns, reusability, diagnostics 모든 섹션을 포함한다
- [ ] HA-02: contract_categories 가 react-kit 의 Clean Architecture 레이어 + G1~G6 그룹 특성을 반영한 4~6 카테고리로 정의된다
- [ ] HA-03: anti_patterns 가 G6 감사 체크리스트의 핵심 규칙을 harness trigger 가능한 grep 패턴으로 변환하여 수록된다
- [ ] HA-04: commands 섹션에 analyze/test/lint/format/codegen 각 필드가 pnpm 명령으로 채워진다

## Plugin Structure
- [ ] PS-01: react-kit/.claude-plugin/plugin.json 템플릿이 name, version, author, description 필드와 함께 명시된다
- [ ] PS-02: react-kit/ 폴더 구조 ASCII 트리 (skills/, agents/, references/, templates/, evals/, README.md, scripts/) 가 포함된다
- [ ] PS-03: 21개 스킬의 파일 경로 (skills/<name>/SKILL.md) 가 그룹별로 리스트업된다
- [ ] PS-04: 3개 에이전트 (react-reviewer, widget-inspector-react, animation-architect-react) 의 파일 경로 (agents/<name>.md) 가 명시된다
- [ ] PS-05: references/ 하위 공유 문서 (project-detection.md, clean-arch-layout.md, result-patterns.md, wasm-catalog.md 참조) 가 리스트된다

## Marketplace
- [ ] MA-01: 이 레포의 .claude-plugin/marketplace.json 에 react-kit 을 등록하는 엔트리 스니펫이 명시된다 (name, version, description, location)
- [ ] MA-02: scripts/release.sh 의 sed 갱신 대상 파일 (react-kit plugin.json, marketplace.json) 경로가 명시된다

## Docs
- [ ] DO-01: react-kit/README.md 의 섹션 구조 (overview, skills table, agents table, quickstart, architecture) 가 명시된다
- [ ] DO-02: docs/react/ 와 docs/react/kit-design/ 의 역할 구분 (리서치 vs 설계) 이 명시된다

## Anti-patterns
- [ ] AP-01: 특정 패치 버전 하드코딩 없음

## Reusability
- [ ] RE-01: 기존 flutter-toolkit, rust-kit, harness 플러그인과의 구조 일관성이 명시된다

## Diagnostics
- [ ] DG-01: N/A (마크다운)
- [ ] DG-02: N/A (IDE diagnostics 대상 아님)
- [ ] DG-03: 문서 내 placeholder (TODO, TBD, FIXME) 0건
- [ ] DG-04: 모든 외부 URL이 http(s):// 형식 (있다면)
