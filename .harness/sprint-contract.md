---
feature: "6개 kit research-log 200줄+ 확충"
created: "2026-04-12 22:30"
complexity: "중간"
conditions: 16
---

# Sprint Contract — 리서치 로그 확충

## Context

자동화 성숙도 Gap 3번 해소: 6개 kit(Flutter, Design, Backend, Infra, Rust, React)의 research-log를 골격 수준(45~99줄)에서 200줄+ 수준으로 확충한다. Context7/Codex/WebSearch 기반 외부 소스 리서치를 포함하며, 모든 소스 URL은 검증된 것이어야 한다.

## 영향 범위

**수정:**
- `docs/flutter/research-log.md` (99줄 → 200+)
- `docs/backend/research-log.md` (61줄 → 200+)
- `docs/infra/research-log.md` (69줄 → 200+)
- `docs/rust/research-log.md` (59줄 → 200+)
- `docs/react/research-log.md` (70줄 → 200+)

**신규 생성:**
- `docs/design/research-log.md` (0줄 → 200+)

**수정 금지:**
- 기존 research-log 엔트리 삭제/수정 (append-only)
- 스킬 SKILL.md, plugin.json, marketplace.json

## Skill

- [ ] SK-01: 6개 research-log 파일 모두 200줄 이상
- [ ] SK-02: 각 research-log에 신규 추가된 소스 엔트리 최소 20개
- [ ] SK-03: 모든 소스 엔트리에 URL이 포함되어 있다 (URL 없는 엔트리 0개)

## Script

- [ ] SC-01: `python3 scripts/validate-plugin.py` exit 0 (7 OK) — 기존 구조 깨뜨리지 않음

## Error

- [ ] ER-01: 깨진 URL(404, 접근 불가)이 포함된 엔트리가 0개
- [ ] ER-02: 각 소스에 적절한 태그 부착 ([official], [blog], [spec], [paper], [dated: YYYY-MM] 중 최소 1개)

## Architecture

- [ ] AR-01: `docs/design/` 디렉토리가 존재하고 research-log.md가 생성됨
- [ ] AR-02: 각 research-log가 기존 엔트리를 보존하며 신규 섹션을 append
- [ ] AR-03: 6개 파일 모두 일관된 엔트리 포맷 (번호, 제목, URL, 태그, 요약 구조)

## Anti-patterns

- [ ] AP-03: 모든 research-log에 bare code fence 0개 (언어 힌트 필수)
- [ ] AP-05: 할루시네이션된 URL 0개 — 존재하지 않는 URL을 소스로 기재 금지

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics

- [ ] DG-01: `python3 scripts/validate-plugin.py` 워닝 0개
- [ ] DG-02: 기존 research-log 내용 미삭제 확인 (diff에서 삭제 라인 0)
