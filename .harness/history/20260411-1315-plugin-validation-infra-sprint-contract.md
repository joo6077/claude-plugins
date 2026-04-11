---
feature: "Plugin Validation Guide + Script + 7-kit Report"
created: "2026-04-11T00:00:00+09:00"
complexity: "복잡"
conditions: 15
scope: "harness/docs/guides/plugin-validation-guide.md (공용 검증 SSOT) + scripts/validate-plugin.py (자동화 구현) + 7개 킷 전체 리포트 생성. 가이드가 원칙/기준/예외를 정의하고, 스크립트가 가이드를 구현, 각 체크 함수는 가이드 섹션 번호를 주석으로 참조."
---

## Guide (SSOT 문서)
- [ ] GD-01: `harness/docs/guides/plugin-validation-guide.md` 존재. frontmatter (last_updated, scope) + 8개 최상위 섹션 (목적, 적용 범위, 7가지 검증 카테고리, 자동화 사용법, 발견 시 대응, 킷별 예외 카탈로그, 카이젠 연동, 변경 이력)
- [ ] GD-02: V1~V7 각 검증 카테고리가 4요소 모두 포함 — (a) 기준, (b) 검증 방법, (c) 예외, (d) FAIL 예시
- [ ] GD-03: 킷별 예외 카탈로그에 7개 킷 (harness, flutter-toolkit, design-kit, backend-kit, infra-kit, rust-kit, react-kit) 의 허용 예외 명시 (예: harness/backend-kit/infra-kit 은 templates/ 없음이 정상)

## Script (가이드 구현)
- [ ] SC-01: `scripts/validate-plugin.py` 존재. `python3 scripts/validate-plugin.py --help` 실행 시 사용법 출력
- [ ] SC-02: 7개 체크 구현 — V1 frontmatter / V2 templates / V3 refs / V4 triggers / V5 placeholders / V6 code-fence / V7 plugin-json
- [ ] SC-03: CLI 옵션 지원 — `<plugin>` (특정 킷) / `--check=<list>` (특정 체크) / `--json` (CI 출력) / `--fix` (자동 수정)
- [ ] SC-04: `--fix` 모드는 V5 placeholders 와 V6 code-fence 만 자동 수정 (V3 refs 같은 위험한 수정은 하지 않음)
- [ ] SC-05: exit code 규약 — 0=OK, 1=warning, 2=error
- [ ] SC-06: 의존성 — Python 표준 라이브러리 + pyyaml 만 (외부 CLI 도구 0개, tsc/cargo/node 불필요)
- [ ] SC-07: 각 체크 함수에 가이드 섹션 번호 주석 포함 (예: `# V1 — see harness/docs/guides/plugin-validation-guide.md §3.1`)

## Report (이 세션 산출물)
- [ ] RP-01: `python3 scripts/validate-plugin.py` 를 7개 킷 전체에 실행한 결과가 콘솔에 출력됨
- [ ] RP-02: 리포트가 각 킷별 PASS/WARNING/ERROR 분류 + 카테고리별 근거 (파일:라인) 포함
- [ ] RP-03: 발견된 문제가 있다면 `docs/superpowers/followup-2026-04-11-plugin-validation-findings.md` 에 숙제 목록으로 저장 (이 세션에서는 fix 하지 않음, 범위 분리)

## Documentation
- [ ] DC-01: `CLAUDE.md` 의 Key Conventions 또는 Commands 섹션에 plugin-validation-guide 경로 + validate-plugin.py 사용법 추가

## Diagnostics (자가 검증)
- [ ] DG-01: 가이드 문서와 스크립트 내 placeholder (TODO/TBD/FIXME) 0건
- [ ] DG-02: 스크립트가 **자기 자신** (validate-plugin.py) 을 포함한 레포 소스에 대해 V5 (placeholder), V6 (code-fence) 자체 통과 — self-hosting
