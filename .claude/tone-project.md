# tone-kit 프로젝트 파라미터

- 감지 일시: 2026-09-15
- 어댑터: 없음 (플러그인 모노레포 — 마크다운 스킬 · 파이썬 · bash 스크립트. dart-flutter 어댑터 대상 아님)
- 주석 언어: ko

## 결정론적 감지값

| 키 | 값 | 감지 근거 |
|---|---|---|
| `scope_paths` | `scripts/` · `*/scripts/` · `*/skills/` · `*/references/` · `docs/` | 디렉토리 존재 |
| `token_class_names` | 해당 없음 | UI 코드 없음 |
| `state_lib` | 해당 없음 | 의존성 파일 없음 |
| `test_dir` | `*/evals/` | 디렉토리 존재 (harness · flutter-toolkit · bambu-kit 등) |
| `shared_component_dir` | 해당 없음 | UI 코드 없음 |
| `i18n_keys_class` | 해당 없음 | i18n 생성 파일 없음 |

## 확인이 필요한 값 (관례 선언)

위젯 조립 형식 키(`widget_prefix` · `widget_suffix` · `props_suffix` · `screen_split_path` · `divider_style`)는
UI 코드가 없어 해당 없음. `file_header_fields` 는 스크립트 첫 줄 docstring 관례만 관측되며 고정 필드 집합은 없다.

## 명령

| 키 | 값 | 출처 |
|---|---|---|
| `analyze_cmd` | `bash -n scripts/release.sh` | `.harness/project.yaml` `commands.analyze` |
| `codegen_cmd` | 없음 | `.harness/project.yaml` `commands.codegen` 이 null |
