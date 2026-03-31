---
feature: "sync-docs 문서 자동 동기화"
created: "2026-03-31 14:00"
complexity: "중간"
conditions: 17
---

## Skill
- [ ] SK-01: `python scripts/sync-docs.py` 실행 시 3개 플러그인 README의 `<!-- AUTO:skills -->` 마커 내 스킬 테이블이 해당 플러그인의 `skills/*/SKILL.md` frontmatter와 일치한다
- [ ] SK-02: `python scripts/sync-docs.py` 실행 시 3개 플러그인 README의 `<!-- AUTO:agents -->` 마커 내 에이전트 테이블이 해당 플러그인의 `agents/*.md` frontmatter와 일치한다
- [ ] SK-03: `python scripts/sync-docs.py --check-only` 실행 시 stdout에 동기화 필요 여부 메시지가 출력되고, 파일 수정은 발생하지 않는다

## Script
- [ ] SC-01: `python scripts/sync-docs.py harness` 실행 시 harness/README.md만 갱신되고 다른 플러그인 README는 변경되지 않는다
- [ ] SC-02: `python scripts/sync-docs.py --dry-run` 실행 시 변경 예정 내용이 stdout에 출력되고, 파일 수정은 발생하지 않는다
- [ ] SC-03: 루트 README.md의 `<!-- AUTO:plugins -->` 마커 내 플러그인 테이블이 각 plugin.json의 version, marketplace.json의 설명과 일치한다

## Error
- [ ] ER-01: README에 마커가 없는 경우 경고 메시지를 출력하고 해당 파일을 스킵한다 (에러로 중단하지 않음)
- [ ] ER-02: SKILL.md에 frontmatter가 없는 경우 경고 메시지를 출력하고 해당 스킬을 스킵한다
- [ ] ER-03: 모든 파일 읽기에 `encoding='utf-8'`을 명시하여 Windows cp949 에러가 발생하지 않는다

## Architecture
- [ ] AR-01: 스크립트가 `scripts/sync-docs.py` 단일 파일로 구현된다
- [ ] AR-02: 경로 처리에 `pathlib.Path`를 사용하여 Windows/Unix 모두 동작한다
- [ ] AR-03: 마커 밖 README 내용(셋업 가이드, 사용 흐름, 원칙 등)이 동기화 실행 전후로 변경되지 않는다

## Anti-patterns
- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다
- [ ] AP-02: force push 금지

## Reusability
- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics
- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개
- [ ] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 `python scripts/sync-docs.py` 구동 시 에러 0개
