---
feature: "Simplify 잔여 findings 전부 적용 (plugin_utils + CheckContext + dispatch + 캐시 + kaizen fragment 링크)"
created: "2026-04-11T16:00:00+09:00"
complexity: "복잡"
conditions: 17
scope: "scripts/plugin_utils.py 신규 + sync-docs.py/validate-plugin.py 공통화 + CheckContext dataclass + CHECK_REGISTRY dispatch + 파일 캐시 + 9 kaizen 스킬 플러그인-검증 본문을 가이드 §5 로 링크 치환"
---

## Plugin Utils (PU)
- [ ] PU-01: `scripts/plugin_utils.py` 신규 파일 존재. Python 3.11+ 표준 라이브러리 + pyyaml 만 의존.
- [ ] PU-02: `plugin_utils.py` 가 아래 함수/상수를 export — `REPO_ROOT`, `load_marketplace(path?) -> dict`, `list_kits(marketplace_data) -> list[Path]`, `read_text(path) -> str`, `parse_frontmatter(text) -> tuple[dict|None, str]`, `iter_skills(kit_path) -> list[Path]`, `iter_agents(kit_path) -> list[Path]`
- [ ] PU-03: `scripts/sync-docs.py` 의 기존 `PLUGINS` 하드코딩 상수 제거, `plugin_utils.list_kits()` 로 marketplace.json 동적 로드
- [ ] PU-04: `scripts/sync-docs.py` 가 `plugin_utils` 의 frontmatter 파서 (`parse_frontmatter` pyyaml 기반 또는 `parse_frontmatter_raw` line-based 중 **적합한 것**) 를 사용하여 내부 중복 파싱 구현을 제거. SSOT 는 `plugin_utils`. **예외 조항**: sync-docs 는 description block scalar (`>`) 의 첫 indent 줄만 추출해야 하므로 pyyaml (folded scalar 를 공백 합산) 사용 시 회귀를 유발한다. 따라서 `parse_frontmatter_raw` 사용이 허용된다.
- [ ] PU-05: `scripts/validate-plugin.py` 가 `plugin_utils` 에서 `read_text`, `parse_frontmatter`, `load_marketplace`, `list_kits` 를 import 하여 사용. 자체 내부 정의 중복 제거

## CheckContext + Dispatch (CC)
- [ ] CC-01: `scripts/validate-plugin.py` 에 `CheckContext` dataclass 정의. 필드: `kit_path`, `marketplace_data`, `fix`, `all_keywords: dict[str, set[str]]`, 내부 `_file_cache: dict[Path, str]`.
- [ ] CC-02: `CheckContext.read(path) -> str` 메서드 — cache hit 시 즉시 반환, miss 시 `plugin_utils.read_text()` 호출 후 캐시
- [ ] CC-03: `CheckContext.invalidate(path)` 메서드 — `_file_cache` 에서 해당 path 제거 (V5/V6 fix 후 stale 방지)
- [ ] CC-04: 7 check 함수 시그니처 통일 — `check_vN(ctx: CheckContext) -> CheckResult` (단일 인자)
- [ ] CC-05: `CHECK_REGISTRY: dict[str, Callable[[CheckContext], CheckResult]]` 모듈 레벨 dict 정의. 7 키 (frontmatter, templates, refs, triggers, placeholders, code-fence, plugin-json)
- [ ] CC-06: `validate_kit(ctx, enabled_checks)` 가 if-chain 대신 `for name, fn in CHECK_REGISTRY.items(): if name in enabled_checks: ...` 루프 dispatch
- [ ] CC-07: V5 `check_v5_placeholders` 와 V6 `check_v6_code_fence` 가 `--fix` 적용 후 `ctx.invalidate(path)` 호출하여 cache stale 방지

## Kaizen Fragment (KZ)
- [ ] KZ-01: `harness/docs/guides/plugin-validation-guide.md` 에 "§5 카이젠 사이클 통합 규칙" (또는 §4 뒤 적절 위치) 신설. 포함 내용: 우선순위 매핑 (ERROR/WARNING/PASS), 통합 규칙 4개, 3단계 실행 패턴 (start → fix → end)
- [ ] KZ-02: 9 개 kaizen 스킬의 "Step N: Plugin Validation 결과 반영" 본문에서 공통 내용 (우선순위 매핑, 통합 규칙, 실행 명령 블록) 제거하고 `harness/docs/guides/plugin-validation-guide.md §5 참조` 링크로 치환. 9 스킬 = react-kaizen, rust-kaizen, backend-kaizen, infra-kaizen, design-kaizen (5 .claude/skills/), harness-kaizen, contract-kaizen, evaluator-kaizen (3 harness/skills/), flutter-kaizen (1 flutter-toolkit/skills/)
- [ ] KZ-03: 각 kaizen 스킬의 kit 특화 지침은 유지 — 예: react-kaizen 의 "Library Policy 카이젠 절대 불가 원칙" 문단은 그대로 보존

## Regression (RG)
- [ ] RG-01: `python3 scripts/validate-plugin.py` 실행 시 7 kit 결과가 refactor 전과 동일 (stdout 비교). 특히 backend-kit=OK, react-kit=ERROR, flutter-toolkit=ERROR 분류 유지
- [ ] RG-02: `python3 scripts/sync-docs.py --check-only` 실행 시 "모든 README가 동기화 상태입니다" 출력 유지
- [ ] RG-03: `python3 scripts/validate-plugin.py --check=frontmatter` 실행 시 flutter-hooks `user-invocable` 누락 FAIL 탐지 유지, exit code 2

## Diagnostics (DG)
- [ ] DG-01: `plugin_utils.py` + 수정 파일 (sync-docs.py, validate-plugin.py, 9 kaizen SKILL.md, plugin-validation-guide.md) placeholder (TODO/TBD/FIXME) 0건
