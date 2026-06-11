# Final Sprint Contract — kaizen/2026-06-11 (인사이트 주도 부분 카이젠)

## 범위

reflect-digest 인사이트 주도 카이젠. 1 CHANGED Phase (Phase 4 harness — validate-plugin V8) + 13 NO_CHANGE Phase. 크로스 Phase 정합성 + 회귀 금지 검증.

평가 대상: `git diff main...HEAD` (커밋 0042225, 3abe8a8, ef83e11 / 15 파일).

## 완료 조건 (binary-decidable)

### V8 가드 정확성

- [ ] **VG-01** [exact]: `python3 scripts/validate-plugin.py --check=hook-exec` 가 11 plugins 전부 OK, Exit 0. (측정: 명령 실행 후 `Exit: 0`)
- [ ] **VG-02** [exact]: V8 음성 테스트 — `chmod -x harness/scripts/run-guard.sh && python3 scripts/validate-plugin.py harness --check=hook-exec` 가 `FAIL ... mode 0o644` + `Exit: 2` 출력. 검증 후 `chmod +x` 복원 시 다시 OK. (회귀 탐지 동작 증명)
- [ ] **VG-03** [structural]: V8 은 인터프리터 경유(`bash`/`sh`/`source`) 스크립트를 대상에서 제외한다 — reflect-kit(`bash` 경유)이 "직접 실행 hook 스크립트 없음 — OK" 로 PASS. (측정: `validate-plugin.py reflect-kit --check=hook-exec` → OK)
- [ ] **VG-04** [exact]: `scripts/validate-plugin.py` 가 `python3 -c "import ast; ast.parse(...)"` 구문 검사 통과 + `CHECK_REGISTRY` 에 `hook-exec` 키 존재.

### 카운트 정합성 (7→8)

- [ ] **CC-01** [exact, enumerated]: 권위 카운트 참조 4곳이 8/V1~V8 로 갱신 — `harness/docs/guides/plugin-validation-guide.md`(8가지·V1~V8), `scripts/validate-plugin.py`(8-카테고리·V1~V8), `CLAUDE.md`(8-카테고리), `README.md`(8-카테고리·V1~V8). (측정: 각 파일 grep)
- [ ] **CC-02** [structural]: 운영 참조(가이드 §7 SSOT 템플릿)는 number-agnostic("전 카테고리")로 전환되어 향후 카테고리 추가 시 drift 가 발생하지 않는다.
- [ ] **CC-03** [exact]: guide §3.8 V8 섹션 신규 + 변경이력 v1.1.0 엔트리 + 로드맵 renumber(V9/V10).

### docs-site / 정합성

- [ ] **DS-01** [exact]: `docs/harness/plugin-validation.html` 에 V8/hook-exec 가 포함되고("7-카테고리"·"7가지" 잔여 0), standalone(새 외부 `<script src=`/`<link rel=stylesheet>` 0) 유지.
- [ ] **DS-02** [exact]: `python3 scripts/validate-post-kaizen.py` → 14 PASS / 0 FAIL.
- [ ] **DS-03** [exact]: `python3 scripts/sync-docs.py --check-only` → "모든 README가 동기화 상태입니다". `python3 scripts/sync-orchestrator.py --check-only` → exit 0.

### 버전 / 회귀 금지

- [ ] **VR-01** [exact]: harness plugin.json v0.4.5 ↔ marketplace.json `[v0.4.5 · 2026-06-11]` 일치 (validate-plugin V7 OK).
- [ ] **VR-02** [structural]: Phase 5~14 per-kit 전 10 NO_CHANGE — `<plugin>/skills/` 디렉토리 및 SKILL.md 콘텐츠가 main 대비 무변경 (diff 에 per-kit skills 파일 0건).
- [ ] **VR-03** [exact]: 전체 `validate-plugin.py` 11 plugins OK Exit 0 (V1~V8 회귀 0).

### Scope 격리

- [ ] **SI-01** [structural]: 각 Phase commit 이 타 Phase 소스를 침범하지 않음. per-kit(flutter/design/backend/infra/rust/react/planning/reflect/bambu/onboarding) skills/ 파일 수정 0건. (측정: `git diff main...HEAD --name-only` 에 `*/skills/*/SKILL.md` 중 harness 외 0건)
- [ ] **SI-02** [structural]: react-kit Library Policy(라이브러리 0개 애니메이션) 완화 0건 — react-kit 파일 무변경으로 자명.

## 제외 (범위 밖)

- 가이드 전반의 기존 markdown lint(MD036/MD040 bold 의사-heading·언어 미지정 fence)는 이번 사이클 신규 추가분이 아니며 전수 수정은 범위 밖. 신규 추가분(§3.8)의 MD036은 해소 완료.
- main 에 이미 반영된 hook fix(520fa20) + harness v0.4.4/design-kit v0.2.5 릴리스는 본 PR 범위 밖(선행 조치).
