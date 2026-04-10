---
name: react-preflight
description: >
  Pre-commit quality gate. 커밋 전 전체 검증을 순서대로 실행한다.
  "커밋 전 확인", "pre-commit", "quality gate", "전체 검증", "preflight",
  "프리플라이트", "커밋 전 검사", "올려도 돼?", "push 전에 확인" 같은 요청 시 사용한다.
  7단계 파이프라인: fix → codegen → lint → tsc → test → wasm-build → vite-build.
  실패 시 즉시 중단하며 복구 안내를 제공한다.
argument-hint: "[--files <glob>] [--skip-wasm] [--skip-e2e]"
user-invocable: true
---

## Gotchas

- **cached 파일과 working tree 불일치**: `git add` 된 파일과 수정 후 add 안 한 파일이 섞이면 결과가 부정확함. 실행 전 `git status` 확인 권장
- **husky + lint-staged 충돌**: lint-staged 가 이미 lint/format 을 돌리고 있으면 preflight 와 중복. react-kit 기본 설정은 lint-staged 미사용 — preflight 한 번에 처리
- **codegen 파일 git noise**: `routeTree.gen.ts` 가 매 codegen 마다 변경됨. gitignore 하거나 stable hash 사용하여 불필요한 diff 방지
- **1단계 fix 의도**: prettier/eslint 자동 수정 가능한 것을 **미리 처리** 후 파이프라인 진입. 3단계 lint 는 자동 수정 불가능한 위반을 잡는 별도 게이트
- **Tauri 빌드 미포함**: Tauri 빌드는 오래 걸려 preflight 에 포함 안 함. CI release 단계 또는 `/react-run tauri-build` 로 별도 실행
- **`--files` 와 tsc**: `--files` 옵션은 lint/test 에만 적용됨. `tsc --noEmit` 은 항상 프로젝트 전체를 검사함

React 프로젝트의 커밋 전 종합 품질 게이트.

## 0. 프로젝트 감지

`references/project-detection.md` 의 절차를 실행하여 환경을 파악한다.

- `crates/core/` 없음 → 6단계 wasm-build 자동 스킵
- `lingui.config.ts` 없음 → 2단계 codegen 에서 `tsr generate` 만 실행

## 실행 순서 (7단계)

각 단계에서 **실패 시 즉시 중단**. 후속 단계 실행하지 않음 — fail-fast.

```text
1. fix
   prettier --write . && eslint . --fix
        ↓ 자동 수정 적용 완료 (실패해도 계속 — fix 는 best-effort)

2. codegen
   pnpm tsr generate && pnpm lingui extract && pnpm lingui compile
        ↓ 실패 → routeTree.gen.ts 또는 .po 파일 손상 가능. 재생성 시도 안내 후 중단

3. lint
   pnpm eslint . --max-warnings=0
        ↓ 실패 → 위반 파일 + 규칙 리스트 출력 후 중단

4. tsc
   pnpm tsc --noEmit
        ↓ 실패 → 타입 에러 파일 리스트 + 첫 5개 에러 요약 후 중단

5. test
   pnpm vitest run
        ↓ 실패 → 실패 테스트 목록 + 스냅샷 변경 여부 출력 후 중단

6. wasm-build
   pnpm wasm-pack build crates/core --target web --release --out-dir ../../src/wasm/core
        ↓ (crates/core 없으면 스킵)
        ↓ 실패 → Rust 컴파일 에러 출력 후 중단

7. vite-build
   pnpm vite build
        ↓ 실패 → 빌드 에러 출력 후 중단

완료 — 전체 단계 통과
```

## 단계별 실패 복구 안내

| 단계 | 실패 원인 | 복구 방법 |
|------|-----------|-----------|
| codegen | routeTree.gen.ts 손상 | 삭제 후 `pnpm tsr generate` 재실행 |
| lint | 자동 수정 불가 위반 | 위반 파일:라인 확인 후 수동 수정 |
| tsc | 타입 에러 | 첫 5개 에러 파일 수정 후 재실행 |
| test | 테스트 실패 | 실패 테스트명 + `--update-snapshots` 필요 여부 안내 |
| wasm-build | Rust 컴파일 에러 | `cargo check --target wasm32-unknown-unknown -p core` 로 진단 |
| vite-build | resolve/ESBuild 에러 | `vite.config.ts` alias 설정 확인 |

## 부분 실행 (--files 플래그)

변경 파일만 대상으로 실행할 수 있다:

```bash
pnpm react-preflight --files "src/presentation/features/auth/**"
```

- **lint**: 지정 파일만 (`eslint <files>`)
- **test**: 관련 테스트만 (`vitest run --related <files>`)
- **tsc**: 항상 프로젝트 전체 검사 (`--files` 미적용)
- **wasm-build / vite-build**: 항상 전체 빌드

## 옵션

| 옵션 | 설명 |
|------|------|
| `--files <glob>` | 지정 파일만 lint/test 대상으로 실행 |
| `--skip-wasm` | 6단계 wasm-build 건너뜀 |
| `--skip-e2e` | Playwright e2e 테스트 건너뜀 (기본적으로 미포함) |

## Report Format

성공 시:

```text
/react-preflight 완료 ✓

  1. fix        ✓ (prettier + eslint --fix 적용)
  2. codegen    ✓ (routeTree.gen.ts 갱신)
  3. lint       ✓ (0 warnings)
  4. tsc        ✓ (0 errors)
  5. test       ✓ (N passed)
  6. wasm-build ✓ (core_bg.wasm X.X MB)
  7. vite-build ✓ (dist/ X.X MB)

커밋할 준비가 됐습니다.
```

실패 시:

```text
/react-preflight 실패 — [N단계: 단계명] 에서 중단

[에러 내용]
[복구 안내]

이후 단계(N+1~7)는 실행되지 않았습니다.
```

## Rules

- **MUST** 7단계 순서를 변경하지 않는다. fix → codegen → lint → tsc → test → wasm-build → vite-build
- **MUST** 각 단계 실패 시 즉시 중단한다. 실패를 무시하고 다음 단계 진행 금지
- **MUST** 모든 명령을 `pnpm` 으로 실행한다
- **MUST** test 단계에서 `vitest run` 을 사용한다. `vitest` (watch 모드) 금지
- **MUST** `--files` 옵션이 있어도 tsc 는 프로젝트 전체를 검사한다
- **MUST NOT** `--no-verify` 로 git hook 을 우회하는 안내를 제공하지 않는다

## References

- `react-kit/references/project-detection.md` — 환경 감지 로직
- `react-kit/skills/react-run/SKILL.md` — 각 빌드 프리미티브 상세
