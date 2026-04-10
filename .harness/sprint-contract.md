---
feature: "react-kit Phase 1 Foundation"
created: "2026-04-10T19:30:00+09:00"
complexity: "중간"
conditions: 14
scope: "react-kit/ 플러그인 디렉토리 스캐폴드 + marketplace.json 등록. 스킬 0개 (Phase 2~9 에서 추가)"
---

## Skill
- [ ] SK-01: react-kit/.claude-plugin/plugin.json 이 존재하고 유효한 JSON 이며 name=react-kit, version=0.1.0 을 포함한다
- [ ] SK-02: react-kit/README.md 가 존재하고 AUTO:skills, AUTO:agents 마커 4개를 포함한다
- [ ] SK-03: react-kit/references/ 에 project-detection.md, clean-arch-layout.md, result-patterns.md, wasm-catalog.md, style-guide.md 5개 파일이 존재한다
- [ ] SK-04: react-kit/templates/ 에 9개 템플릿 파일이 존재한다 (tsconfig, eslint, vite, tailwind, package.json, pnpm-workspace, Cargo, lingui, harness-project)
- [ ] SK-05: react-kit/evals/evals.json 이 존재하고 유효한 JSON 이며 test-fixtures/ 아래 5개 fixture 디렉토리가 존재한다
- [ ] SK-06: react-kit/scripts/project-detect.sh 가 존재하고 실행 권한이 있으며 bash 구문이 유효하다 (bash -n 통과)

## Script
- [ ] SC-01: 모든 템플릿의 JSON/YAML 파일이 parse 가능하다
- [ ] SC-02: 모든 템플릿의 라이브러리 버전이 caret range (`^` prefix) 로 표기되고 특정 패치 버전 하드코딩 없음. **예외 (semver 표준 준수)**: (a) 메이저 버전이 0 인 패키지 (`^0.X.Y` 허용 — semver 상 minor 가 breaking 과 동등 취급), (b) `packageManager` 필드 (Node.js corepack 규약이 정확한 버전 요구)
- [ ] SC-03: `python3 scripts/sync-docs.py --check-only react-kit` 이 성공한다

## Architecture
- [ ] AR-01: react-kit/ 의 폴더 구조가 기존 flutter-toolkit/, rust-kit/ 과 일관된다 (.claude-plugin/, skills/, agents/, references/, templates/, evals/)
- [ ] AR-02: .claude-plugin/marketplace.json 에 react-kit 엔트리가 rust-kit 뒤에 추가되어 있고 name/source/description 3개 필드를 포함한다

## Anti-patterns
- [ ] AP-01: 특정 패치 버전 하드코딩 없음. **예외**: (a) `plugin.json` 의 `version` 필드 (이 플러그인 자체 버전 선언), (b) `package.json.template` 의 `packageManager` 필드 (corepack 규약 요구), (c) 메이저 0 패키지의 `^0.X.Y` 형태 (semver 표준)

## Reusability
- [ ] RE-01: references/ 의 내용이 docs/react/kit-design/ 설계 문서들과 일관된다
- [ ] RE-02: 이 Phase 에서 SKILL.md 를 추가하지 않았다 (스킬은 Phase 2~9 에서 추가 예정)

## Diagnostics
- [ ] DG-01: 문서 내 placeholder (TODO, TBD, FIXME) 0건
- [ ] DG-02: 모든 외부 URL 이 http(s):// 형식
