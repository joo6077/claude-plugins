---
name: react-run
description: >
  React 빌드 프리미티브를 개별 실행한다.
  "dev 실행", "build만", "lint만", "vitest run", "wasm-build 서브커맨드", "codegen 실행",
  "테스트 실행", "format", "tsc 확인", "e2e 실행" 같은 요청 시 사용한다.
  상위 워크플로우 스킬(react-build, react-preflight 등)에서 내부적으로도 호출된다.
  코드를 직접 수정하거나 새 파일을 생성하는 작업에는 사용하지 않는다.
argument-hint: "<subcommand> [options]"
user-invocable: true
---

## Gotchas

- **`pnpm vitest` vs `pnpm vitest run`**: 전자는 watch 모드 기본, 후자는 1회 실행. CI/preflight 에서는 반드시 `run` 서브커맨드 사용
- **`--max-warnings=0`**: ESLint 기본은 경고 허용. 빌드 게이트 의도면 명시 필수 — 누락하면 경고가 있어도 0 exit code
- **wasm-build 실행 위치**: `pnpm wasm-pack build crates/core ...` 는 프로젝트 루트에서 실행. `crates/core/` 안에서 실행하면 `--out-dir` 상대 경로가 달라짐
- **`tsc --noEmit`**: 컴파일 없이 타입 검사만 수행. `--noEmit` 없이 실행하면 `dist/` 에 불필요한 산출물이 생성됨
- **codegen 순서**: `tsr generate` → `lingui extract` → `lingui compile` 순서 고정. Lingui catalog 가 라우트 생성 이후에야 완전히 수집됨
- **pnpm 필수**: npm / yarn 직접 호출 금지. react-kit 의 유일한 패키지 매니저
- **`dev` 포트는 5173 에 묶여 있다 (`strictPort: true`)**: Vite 는 지정 포트가 차 있으면 기본으로 다음 빈 포트로 옮긴다. 그러면 Tauri `devUrl` 과 harness `runtime_inspection.vm_port`(둘 다 5173)가 실제 서버와 조용히 어긋나고, 5173 주소에는 다른 서버의 화면이 떠 있을 수 있다. react-init 으로 만든 프로젝트는 단계 2 에서 `vite.config.ts` 에 `strictPort: true` 를 넣어(템플릿 `templates/vite.config.template.ts` 와 같다) 차 있으면 옮기지 않고 멈춘다. 그 설정이 없는 프로젝트면 `pnpm vite dev --strictPort` 로 띄운다. 멈추면 그 포트를 쓰는 서버가 이 작업의 것인지 먼저 확인하고 남의 서버를 끄지 않는다. 다른 포트가 필요하면 `pnpm vite dev --port <N>` 으로 띄우되 Tauri 를 쓰면 `devUrl` 을, harness 런타임 검증을 쓰면 `vm_port` 를 같은 번호로 맞춘다 ([Vite server options](https://vite.dev/config/server-options.html#server-port) · [Vite CLI](https://vite.dev/guide/cli) · [Tauri Vite 설정](https://v2.tauri.app/start/frontend/vite/))
- **test 결과는 passed · skipped 두 수로 읽는다**: `vitest run` 이 종료 코드 0 이어도 시험을 하나도 안 돌렸거나(`passWithNoTests`) 남은 `.only` 때문에 나머지가 전부 skipped 일 수 있다(`allowOnly` 기본값이 로컬에서 참). 근거는 `references/render-evidence-protocol.md` §3 (b)(c)

React 빌드 프리미티브. 첫 번째 인자로 서브커맨드를 지정한다.

## 0. 프로젝트 감지

`references/project-detection.md` 의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과를 사용한다:

| 감지 키 | 영향받는 서브커맨드 |
|---------|-------------------|
| `crates/core/` 존재 | `wasm-build` 활성화 |
| `src-tauri/` 존재 | `tauri-dev`, `tauri-build` 활성화 |
| `lingui.config.ts` 존재 | `codegen` 에서 Lingui extract/compile 포함 |
| Playwright 설치 | `e2e` 활성화 |

## 서브커맨드 목록

서브커맨드가 없으면 사용 가능한 목록을 출력한다.

| 서브커맨드 | 명령 | 용도 |
|----------|------|------|
| `dev` | `pnpm vite dev` | Vite dev 서버 시작 (포트 5173) |
| `build` | `pnpm vite build` | 프로덕션 빌드 → `dist/` |
| `preview` | `pnpm vite preview` | 프로덕션 빌드 결과 로컬 서빙 |
| `tsc` | `pnpm tsc --noEmit` | TypeScript 타입 검사만 (컴파일 없음) |
| `lint` | `pnpm eslint . --max-warnings=0` | ESLint 검사 (경고 = 실패) |
| `lint-fix` | `pnpm eslint . --fix` | 자동 수정 가능한 린트 이슈만 수정 |
| `format` | `pnpm prettier --write .` | Prettier 포매팅 적용 |
| `format-check` | `pnpm prettier --check .` | 포매팅 검사만 (수정 없음) |
| `test` | `pnpm vitest run` | Vitest 1회 실행 (watch 없음) |
| `test-watch` | `pnpm vitest` | Vitest watch 모드 |
| `test-coverage` | `pnpm vitest run --coverage` | 커버리지 수집 포함 실행 |
| `e2e` | `pnpm playwright test` | Playwright e2e 테스트 *(Playwright 설치 시)* |
| `wasm-build` | `pnpm wasm-pack build crates/core --target web --release --out-dir ../../src/wasm/core` | Rust → WASM 빌드 *(crates/core 존재 시)* |
| `codegen` | `pnpm tsr generate && pnpm lingui extract && pnpm lingui compile` | TanStack Router 라우트 트리 + Lingui catalog 생성 |
| `tauri-dev` | `pnpm tauri dev` | Tauri 데스크탑 dev *(src-tauri 존재 시)* |
| `tauri-build` | `pnpm tauri build` | Tauri 데스크탑 프로덕션 빌드 *(src-tauri 존재 시)* |

### codegen 조건부 동작

- `lingui.config.ts` 없음 → `tsr generate` 만 실행
- TanStack Router 미설치 → `codegen` 서브커맨드 자체를 비활성화하고 안내 메시지 출력

## Report Format

성공 시:

```text
/react-run <subcommand> 완료
  결과: <success / N issues / N failed>
  시험 수: <N passed · M skipped>   (test · test-coverage · e2e 만)
```

`test` · `test-coverage` · `e2e` 는 러너 요약의 passed · skipped 두 수를 그대로 옮긴다. `success` 는 passed 가 1 이상이고 skipped 가 0 일 때만 쓴다.

- passed 가 0 이면 결과를 `[미검증] 0 passed — 시험을 하나도 돌리지 않았다` 로 적는다
- skipped 가 1 이상이면 결과를 `[미검증] N passed · M skipped` 로 적고 skipped 범위(파일 · 이름)와 `.only` 가 남은 곳 수(`grep -rnE '(it|test|describe)\.only\(' src tests 2>/dev/null | wc -l`)를 함께 적는다. 의도한 `skip` · `skipIf` 도 있으니 실패로 바꾸지는 않는다

실패 시:

```text
/react-run <subcommand> 실패
  [에러 내용 요약]
  [수정 방법 안내]
```

## Rules

- **MUST** 모든 명령을 `pnpm` 으로 실행한다. npm / yarn 직접 호출 금지
- **MUST** 비활성화 서브커맨드 호출 시 이유를 출력하고 중단한다. 조용히 스킵 금지
- **MUST** 이 스킬은 실행만 담당한다. 코드 수정은 별도 스킬에서 수행
- **MUST** `wasm-build` 는 프로젝트 루트에서 실행한다. `crates/core/` 안으로 cd 금지
- **MUST** CI/preflight 에서 test 실행 시 `test` (vitest run) 서브커맨드를 사용한다. `test-watch` 금지
- **MUST** `test` · `test-coverage` · `e2e` 결과에 passed · skipped 두 수를 적는다. passed 0 이나 skipped 1 이상을 `success` 로 적지 않는다

## References

- `react-kit/references/project-detection.md` — 환경 감지 로직
