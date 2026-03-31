---
feature: "docs-site Phase 1 — 스킬 + 구조 + index.html"
created: "2026-03-31 20:30"
complexity: "복잡"
conditions: 12
---

## Architecture
- [ ] AR-01: docs/index.html이 존재하고 Claude 컬러 토큰(--accent:#D97757, --bg:#0d0d14, --text:#F5F0E8)을 사용한다
- [ ] AR-02: docs/design-kit/ 디렉토리에 19개 HTML 파일이 존재한다
- [ ] AR-03: docs/process/kaizen-flow.html이 존재한다
- [ ] AR-04: docs/harness/ 및 docs/flutter-toolkit/ 디렉토리가 존재한다
- [ ] AR-05: docs/.nojekyll 파일이 존재한다
- [ ] AR-06: .claude/skills/docs-site/SKILL.md가 존재하고 유효한 frontmatter를 가진다

## Skill
- [ ] SK-01: docs/index.html의 categories 배열에 Design Kit 페이지 19개가 등록되어 있고 file 경로가 design-kit/ 접두어를 가진다
- [ ] SK-02: docs/index.html의 categories 배열에 Harness, Flutter Toolkit, Process 섹션이 존재한다

## Error
- [ ] ER-01: docs/design/visuals/ 디렉토리에 HTML 파일이 0개다 (이동 완료)

## Anti-patterns
- [ ] AP-01: 하드코딩된 버전 없음
- [ ] AP-02: force push 금지

## Reusability
- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics
- [ ] DG-01: bash -n scripts/release.sh 워닝 0개
- [ ] DG-02: IDE diagnostics 워닝/인포 0개
- [ ] DG-03: 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개
