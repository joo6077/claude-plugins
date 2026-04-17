---
feature: "reflect-kit v0.3.0 — Hybrid project_id (backward-compatible)"
created: "2026-04-17 17:17"
complexity: "중간"
conditions: 20
---

## Skill
- [ ] SK-01: `/reflect-digest project=<basename>` 와 `/reflect-digest project=<basename>-<hash6>` 가 동일한 스캔 대상 디렉토리 집합을 선택하고, 집계된 reflections 엔트리 수가 일치한다 [goal]
- [ ] SK-02: reflect-digest SKILL.md 에서 "레거시 버킷" 관련 분류 섹션이 제거되고, 정규화 쿼리 동작(basename → basename + basename-<hash6> glob union)이 명시된다 [structural]
- [ ] SK-03: `/reflect-digest project=all` cross-project 집계 로직이 신규 basename 디렉토리와 기존 `*-<hash6>` 디렉토리를 모두 포함하도록 glob 패턴이 확장된다 [structural]

## Script
- [ ] SC-01: 충돌 없는 경우 `compute_project_id` 는 `<basename>` 만 반환한다 (hash suffix 없음). "충돌 없는 경우" = `~/.claude/logs/<basename>/` 디렉토리가 없거나, 존재하면 해당 디렉토리의 `.project-root` 마커가 현재 git root와 일치할 때 [structural]
- [ ] SC-02: 충돌 감지 시 `<basename>-<hash6>` 로 fallback 하고 stderr 에 경고를 출력한다. "1회 보장" = 단일 스크립트 실행 프로세스 단위, `${TMPDIR:-/tmp}/.reflect-kit-warn-<basename>-<PID>` 마커 파일 기반 [structural]
- [ ] SC-03: `scripts/legacy-id-migrate.sh --scan` 결과에서 `_cron`, `.*`, `_*` 내부 디렉토리가 제외된다 [structural, enumerated]
- [ ] SC-04: reflect-digest 의 cross-project 스캔에서 SC-03 과 동일한 필터(`_cron`, dot-prefix, underscore-prefix)가 적용된다 [structural, enumerated]

## Error
- [ ] ER-01: git 미설치 또는 비-repo 환경에서 `compute_project_id` 는 cwd basename 을 반환하며 기존 fallback 경로(cwd → hash input)가 유지된다 [goal]
- [ ] ER-02: `hooks/log-*.sh` 의 쓰기 경로가 `compute_project_id` 결과를 그대로 사용하므로, SC-02 충돌 감지 충족 시 기존 `<basename>/` 디렉토리를 덮어쓰지 않고 자동으로 `<basename>-<hash6>` 로 분기한다 [structural]
- [ ] ER-03: `/reflect-digest project=<basename>` 호출에서 glob 매칭 디렉토리가 0개일 때 "no matching buckets" 취지의 명확한 메시지를 stderr 에 출력한다 [structural]

## Architecture
- [ ] AR-01: `/reflect-digest` 가 glob union 코드 경로(`<basename>` + `<basename>-*`)를 통해 기존 `*-<hash6>` 디렉토리를 그대로 읽는다 — 사용자 데이터 이동/마이그레이션 스크립트 추가 불필요 [goal]
- [ ] AR-02: `reflect-kit/.claude-plugin/plugin.json` version = `0.3.0`, `marketplace.json` 의 reflect-kit description 이 `[v0.3.0 · 2026-04-17]` 접두사로 시작한다 [exact]
- [ ] AR-03: `reflect-kit/docs/DESIGN.md` 에 "결정 #3 Hybrid 전환" 섹션이 추가되어 독립 리뷰 근거와 backward-compat 보증이 기록된다 [structural]
- [ ] AR-04: `reflect-kit/README.md` 에 v0.3.0 변경 요약(Hybrid 전환 + 정규화 쿼리 + 내부 디렉토리 제외)이 추가된다 [structural]

## Anti-patterns
- [ ] AP-01: 버전 문자열을 hook/스크립트에 하드코딩하지 않는다 — plugin.json 참조
- [ ] AP-03: SKILL.md / DESIGN.md / README.md 에 bare code fence 없음 — 언어 힌트 필수

## Reusability
- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics
- [ ] DG-01: `bash -n` 문법 검사 워닝 0개 (변경/생성 .sh 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개
- [ ] DG-03: `scripts/release.sh` 리허설 시 에러/예외 0개
- [ ] DG-04: 충돌 시뮬레이션 시 basename 반환 + hash fallback + 1회 경고 동작. 실 훅 발동 불가 환경에서는 `bash -x hooks/_lib-project-id.sh` 경로 추적으로 대체 검증 허용 [goal]
