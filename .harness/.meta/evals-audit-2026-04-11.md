# evals audit 2026-04-11

> Phase 1~10 research-mode rerun 후 자동 점검. `<plugin>/skills/` 디렉토리의 스킬과 `<plugin>/evals/evals.json` 의 `skill` 필드 대조.


## flutter-toolkit
- skills on disk: 18
- evals entries: 19
- unique skills covered by evals: 18
- ✅ coverage OK

## rust-kit
- skills on disk: 16
- evals entries: 17
- unique skills covered by evals: 17
- **eval entries referencing non-existent skills (orphans)**: ['rust-kaizen']

## react-kit
- skills on disk: 21
- evals entries: 0
- unique skills covered by evals: 0
- **skills without eval coverage**: ['react-animation', 'react-api', 'react-audit', 'react-build', 'react-error', 'react-extract', 'react-feature', 'react-form', 'react-init', 'react-l10n', 'react-preflight', 'react-query', 'react-responsive', 'react-run', 'react-screen', 'react-skeleton', 'react-store', 'react-tauri', 'react-test', 'react-wasm', 'react-widget']

## design-kit
- skills on disk: 7
- evals entries: 15
- unique skills covered by evals: 4
- **skills without eval coverage**: ['design-component', 'design-mockup', 'design-reference']
