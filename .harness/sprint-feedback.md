---
feature: "Simplify 잔여 findings 전부 적용 (plugin_utils + CheckContext + dispatch + 캐시 + kaizen fragment 링크)"
iteration: 3
evaluated: "2026-04-10 15:00"
verdict: APPROVE
---

# Sprint Feedback
Feature: Simplify 잔여 findings 전부 적용 (plugin_utils + CheckContext + dispatch + 캐시 + kaizen fragment 링크)
Evaluated: 2026-04-10 15:00
Verdict: APPROVE
Iteration: 3

## Results

### Plugin Utils — PU (5/5)

- [x] PU-01: scripts/plugin_utils.py 신규 파일 존재. Python 3.11+ 표준 라이브러리 + pyyaml만 의존 — PASS
  - 근거: `scripts/plugin_utils.py:1-13` — import json, re, pathlib (표준 라이브러리) + yaml (pyyaml). 외부 의존 없음. (L3)

- [x] PU-02: export 함수/상수 7종 — PASS
  - 근거: `scripts/plugin_utils.py:15` (REPO_ROOT), L19 (load_marketplace), L25 (list_kits), L34 (read_text), L42 (parse_frontmatter), L104 (iter_skills), L109 (iter_agents). 7종 모두 존재. (L2)

- [x] PU-03: sync-docs.py PLUGINS 하드코딩 제거, list_kits() 동적 로드 — PASS
  - 근거: `scripts/sync-docs.py:24` — list_kits import. L427, L451, L475, L295 — list_kits() 호출. PLUGINS 상수 없음. (L3)

- [x] PU-04: sync-docs.py가 plugin_utils의 frontmatter 파서(parse_frontmatter_raw)를 사용하여 내부 중복 파싱 구현을 제거. SSOT는 plugin_utils. 예외 조항 충족. — PASS (갱신된 PU-04 문구 기준)
  - 서브체크 1 — plugin_utils 파서 사용: `scripts/sync-docs.py:24` — `from plugin_utils import ..., parse_frontmatter_raw, ...`. `sync-docs.py:55` — `parse_frontmatter_raw(text)` 호출. PASS. (L3)
  - 서브체크 2 — SSOT 달성 (내부 중복 없음): `_parse_frontmatter_file`은 `parse_frontmatter_raw(text)` 단순 호출 wrapper (sync-docs.py:45-58). sync-docs.py 내부에 자체 `---` regex 파싱, yaml.safe_load, line-split 파싱 로직 없음 (Grep 확인). PASS. (L3)
  - 서브체크 3 — 예외 조항 기술적 타당성: pyyaml 실행 검증 — folded scalar(`>`) 결과: `'트리거 키워드 포함 설명. 두 번째 줄도 description의 일부다. 세 번째 줄까지.\n'` (전체 공백 합산). parse_frontmatter_raw 결과: `'트리거 키워드 포함 설명.'` (첫 indent 줄만). README 테이블 한 줄 요약 용도에 pyyaml 사용 시 회귀 발생 사실 확인. PASS. (L3 — 실행 검증)

- [x] PU-05: validate-plugin.py가 plugin_utils에서 4개 함수 import, 자체 중복 제거 — PASS
  - 근거: `scripts/validate-plugin.py:32` — `from plugin_utils import load_marketplace, list_kits, read_text, parse_frontmatter, REPO_ROOT`. (L3)

### CheckContext + Dispatch — CC (7/7)

- [x] CC-01: CheckContext dataclass, 5개 필드 — PASS
  - 근거: `scripts/validate-plugin.py:114-123` — kit_path, marketplace_data, fix, all_keywords, _file_cache. (L2)

- [x] CC-02: read() 메서드 — 캐시 hit 즉시 반환, miss 시 read_text() 호출 후 캐시 — PASS
  - 근거: `scripts/validate-plugin.py:124-128`. (L3)

- [x] CC-03: invalidate(path) 메서드 — PASS
  - 근거: `scripts/validate-plugin.py:130-132` — `self._file_cache.pop(path, None)`. (L3)

- [x] CC-04: 7 check 함수 시그니처 `(ctx: CheckContext) -> CheckResult` — PASS
  - 근거: L140 (V1), L200 (V2), L295 (V3), L347 (V4), L399 (V5), L447 (V6), L506 (V7). (L2)

- [x] CC-05: CHECK_REGISTRY 7 키 — PASS
  - 근거: `scripts/validate-plugin.py:565-573` — 7키 확인. (L2)

- [x] CC-06: validate_kit 루프 dispatch — PASS
  - 근거: `scripts/validate-plugin.py:576-582` — `for name, fn in CHECK_REGISTRY.items()`. (L3)

- [x] CC-07: V5/V6 fix 후 ctx.invalidate() 호출 — PASS
  - 근거: `scripts/validate-plugin.py:426` (V5), L484 (V6). (L3)

### Kaizen Fragment — KZ (3/3)

- [x] KZ-01: plugin-validation-guide.md §7 카이젠 연동 섹션 신설 — PASS
  - 근거: `harness/docs/guides/plugin-validation-guide.md:474-534` — §7.1~§7.5 확인. (L3)

- [x] KZ-02: 9 kaizen 스킬 공통 본문 제거 + §7 링크 치환 — PASS
  - 근거: 9개 파일 모두 "plugin-validation-guide.md §7 에서 정의한다 (SSOT)" 링크 존재. (L3)

- [x] KZ-03: react-kaizen의 kit 특화 지침 유지 — PASS
  - 근거: `.claude/skills/react-kaizen/SKILL.md:73-75` — Library Policy 원칙 보존. (L2)

### Regression — RG (3/3)

- [x] RG-01: validate-plugin.py — backend-kit=OK, react-kit=ERROR, flutter-toolkit=ERROR 분류 유지 — PASS
  - 근거: 실행 결과 확인. (L3 — 실행)

- [x] RG-02: sync-docs.py --check-only → "모든 README가 동기화 상태입니다" — PASS
  - 근거: 실행 결과 마지막 줄 "모든 README가 동기화 상태입니다." 확인. (L3 — 실행)

- [x] RG-03: validate-plugin.py --check=frontmatter → flutter-hooks FAIL, exit 2 — PASS
  - 근거: 실행: `FAIL flutter-toolkit/skills/flutter-hooks/SKILL.md: 누락 필드 ['user-invocable']`, exit 2. (L3 — 실행)

### Diagnostics — DG (1/1)

- [x] DG-01: 수정 파일 placeholder 0건 — PASS
  - 근거: Grep 및 validate-plugin.py V5 확인. 0건. (L3)

### Anti-patterns (2/2)

- [x] AP-01: hardcoded version 없음 — PASS
- [x] AP-02: force push 없음 — PASS

### Reusability (1/1)

- [x] plugin_utils.py 공유 사용 — PASS

## PU-04 계약 수정 정당성 판정

**계약 수정 정당성: 인정.**

Iter 2 QA가 제시한 "수정 옵션 B (plugin_utils에 두 파서 공존, 적합한 것 사용)"와 실질적으로 동등한 해결이다.

기술적 사실 (실행 검증):
- pyyaml folded scalar: 전체 줄을 공백으로 합산 → README 테이블 회귀 유발
- parse_frontmatter_raw: description 첫 indent 줄만 추출 → README 테이블 정상 동작

계약의 근본 의도 ("sync-docs와 validate-plugin 간 중복 파싱 제거, SSOT = plugin_utils")는 완전히 달성됐다.
새 PU-04 문구는 기술적 제약을 정확히 반영하며, 예외 조항은 회귀 없음(RG-02 PASS)으로 실증됐다.

## Summary
- Total: 17/17 conditions passed
- Verdict: APPROVE
- Iteration: 3

## Changes from Iteration 2

- PU-04: FAIL → PASS. 계약 PU-04 문구가 "parse_frontmatter_raw 사용 허용" 예외 조항을 포함하도록 갱신됨. 새 문구 기준 3개 서브체크 모두 통과.
- 나머지 16 조건: 변경 없음. Iteration 2 PASS 결과 그대로 유지.

## 런타임 검증
RG-01/02/03은 직접 스크립트 실행으로 검증 (MCP 서버 미설정).
