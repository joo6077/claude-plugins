---
feature: "Phase A — docs-site 2페이지 등록 + release.sh 크로스플랫폼 수정 + design-kit v0.2.0 릴리스"
created: "2026-04-10 12:37"
complexity: "단순"
conditions: 10
---

## Script
- [ ] SC-01: Given macOS(BSD sed) 환경에서, When `bash scripts/release.sh design-kit minor`를 실행했을 때, Then sed 에러 없이 plugin.json과 marketplace.json이 정상 치환된다
- [ ] SC-02: Given GNU sed 환경(Linux)에서도, When release.sh를 실행했을 때, Then 동일하게 정상 동작한다 (--version 감지 분기로 양쪽 호환)
- [ ] SC-03: Given release.sh 실행 후, Then design-kit/.claude-plugin/plugin.json의 version 필드가 0.2.0으로 변경되어 있다
- [ ] SC-04: Given release.sh 실행 후, Then .claude-plugin/marketplace.json의 design-kit description에 `[v0.2.0 · 2026-04-10]` 패턴이 반영되어 있다
- [ ] SC-05: Given release.sh 실행 후, Then git tag `design-kit/v0.2.0`이 생성되고 origin에 push 되어 있다

## Architecture
- [ ] AR-01: Given docs/index.html을 열었을 때, Then "Design Kit — 워크플로우" 섹션 pages 배열에 `design-template`와 `visual-styles` 두 항목이 등록되어 있다
- [ ] AR-02: Given 등록된 id와 file 경로가, Then 기존 pages 배열의 네이밍 컨벤션(kebab-case id, `design-kit/{id}.html` 파일 경로)과 일치한다
- [ ] AR-03: Given docs/design-kit/ 디렉토리에, Then design-template.html과 visual-styles.html 실제 파일이 존재한다

## Error
- [ ] ER-01: Given release.sh가 dirty working tree 상태에서 실행되었을 때, Then 사용자에게 확인 prompt를 띄우고 [y/N] 입력 대기한다 (기존 로직 유지, 수정으로 깨지지 않음)
- [ ] ER-02: Given sed가 in-place 치환에 실패했을 때, Then 스크립트가 `set -eo pipefail`로 즉시 종료하여 이어지는 git commit/tag/push가 실행되지 않는다

## Anti-patterns
- [ ] AP-01: 버전이 스크립트에 하드코딩되지 않았다 — `grep '"version"'`로 plugin.json에서 읽어 bump한다
- [ ] AP-02: `git push --force`를 사용하지 않았다 — 일반 `git push origin HEAD --follow-tags`만 사용한다

## Reusability
- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 (해당 작업은 공통 스크립트 수정이므로 N/A)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 (release.sh는 기존 스크립트 수정이며 중복 생성 없음)

## Diagnostics
- [ ] DG-01: `bash -n scripts/release.sh` 문법 에러 0개
- [ ] DG-02: IDE diagnostics 워닝/인포 0개
- [ ] DG-03: release.sh 실제 실행 시 콘솔 에러/예외 0개 (버그 수정 후 재실행 결과 기준)
- [ ] DG-04: design-kit v0.2.0 태그와 커밋이 origin에 정상 push 되어 있다 (`git ls-remote --tags origin | grep design-kit/v0.2.0`)
