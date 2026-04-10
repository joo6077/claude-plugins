---
name: react-build
description: >
  전체 빌드 파이프라인을 실행한다. wasm-pack → tsc → vite build 순서.
  "전체 빌드", "프로덕션 빌드", "wasm + tsc + vite", "build 파이프라인",
  "빌드해줘", "배포 빌드", "dist 생성" 같은 요청 시 사용한다.
  각 단계가 순서대로 실행되며 한 단계라도 실패하면 즉시 중단한다.
argument-hint: "[--skip-wasm] [--skip-tsc] [--mode production|staging|development] [--analyze]"
user-invocable: true
---

## Gotchas

- **WASM 은 반드시 먼저**: `tsc` 와 `vite build` 가 `src/wasm/core/` 를 import 하므로 WASM 산출물이 먼저 존재해야 타입 에러가 발생하지 않음. 순서를 바꾸면 빌드 실패
- **Vite 는 tsc 를 하지 않음**: Vite 내장 ESBuild 는 타입 stripping 만 함. 타입 에러가 있어도 Vite 빌드가 성공할 수 있어 `tsc --noEmit` 별도 필수
- **`--skip-tsc` 는 비권장**: 타입 에러를 숨긴 채 배포하게 됨. CI 실패 디버깅 용도로만 사용
- **환경 변수 prefix**: `VITE_*` prefix 만 브라우저 번들에 포함. 다른 prefix 는 런타임에 `undefined`
- **base 설정**: `vite.config.ts` 의 `base` 옵션이 Tauri (기본 `/`) 와 웹 배포 서브패스에서 다를 수 있음. `--mode` 별 분기 확인 필요
- **wasm-pack 경로**: `crates/core/` 가 없으면 `--skip-wasm` 자동 활성화. 명시적으로 비활성화하지 않는 한 경고 출력

WASM 포함 React 프로젝트의 전체 프로덕션 빌드 파이프라인.

## 0. 프로젝트 감지

`references/project-detection.md` 의 절차를 실행하여 환경을 파악한다.

- `crates/core/` 없음 → WASM 단계 자동 스킵, 사용자에게 알림
- `lingui.config.ts` 없음 → codegen 단계에서 `tsr generate` 만 실행

## 빌드 순서

```
[1. WASM 빌드]
  pnpm wasm-pack build crates/core --target web --release --out-dir ../../src/wasm/core
        │ 실패 → Rust 컴파일 에러 출력 후 중단
        ▼
[2. TypeScript 검사]
  pnpm tsc --noEmit
        │ 실패 → 타입 에러 파일 리스트 + 첫 5개 에러 요약 후 중단
        ▼
[3. Vite 빌드]
  pnpm vite build --mode <mode>
        │ 실패 → 빌드 에러 출력 후 중단
        ▼
[4. 산출물 검증]
  dist/index.html 존재 확인
  dist/assets/*.js gzip 크기 리포트
  src/wasm/core/*.wasm 존재 + gzip 크기 리포트
  단일 chunk > 1MB gzip → 경고
        │
        ▼
완료 — 빌드 시간, dist/ 크기, wasm gzip 크기 리포트
```

각 단계에서 **실패 시 즉시 중단**. 후속 단계 실행하지 않음.

## 옵션

| 옵션 | 설명 |
|------|------|
| `--mode production` | 기본값. 프로덕션 최적화 번들 |
| `--mode staging` | 스테이징 환경 번들 |
| `--mode development` | 소스맵 포함 개발 빌드 |
| `--skip-wasm` | WASM 빌드 단계 건너뜀 (WASM 없는 프로젝트 또는 캐시 사용 시) |
| `--skip-tsc` | 타입 검사 단계 건너뜀 (비권장 — CI 디버깅 용도만) |
| `--analyze` | rollup-plugin-visualizer 번들 분석 HTML 생성 |

## 단계별 실패 처리

### WASM 빌드 실패
Rust 컴파일 에러를 그대로 출력. 다음 안내 제공:

```bash
# 빠른 진단 (링크 없이 타입 체크만)
cargo check --target wasm32-unknown-unknown -p core
```

### tsc 실패
타입 에러 파일 리스트 출력 + 첫 5개 에러 요약. 전체 출력은 `tsc-errors.log` 로 저장 안내.

### Vite 빌드 실패
의존성 resolve 실패 / ESBuild 에러 메시지를 그대로 출력. `vite.config.ts` `resolve.alias` 설정 확인 안내.

## 산출물 검증 기준

- `dist/index.html` 존재 확인 (Vite 빌드 성공 최소 지표)
- `dist/assets/*.js` gzip 크기 — 단일 chunk > 1MB gzip 이면 ⚠️ 경고
- `src/wasm/core/*.wasm` 존재 확인
- `src/wasm/core/*.wasm` gzip 크기 — 사용자 awareness 목적으로 출력

## Report Format

성공 시:

```
/react-build 완료 (XX.Xs)

산출물:
  dist/index.html — OK
  dist/assets/index-[hash].js — X.X MB (gzip: X.X KB)
  src/wasm/core/core_bg.wasm — X.X MB (gzip: X.X KB)

경고: <없음 | 크기 초과 chunk 목록>
```

실패 시:

```
/react-build 실패 — [단계명] 에서 중단

[에러 내용]
[복구 안내]
```

## Rules

- **MUST** 빌드 순서(WASM → tsc → vite)를 변경하지 않는다. 순서 변경 시 타입 에러 누락 또는 빌드 실패 발생
- **MUST** 모든 명령을 `pnpm` 으로 실행한다
- **MUST** 각 단계 실패 시 즉시 중단한다. 실패를 무시하고 다음 단계 진행 금지
- **MUST** `--skip-tsc` 사용 시 경고 메시지를 출력한다
- **MUST** 산출물 검증을 마지막에 반드시 실행한다. `dist/index.html` 없이 성공 보고 금지

## References

- `react-kit/references/project-detection.md` — 환경 감지 로직
- `docs/react/wasm-catalog.md` — WASM 빌드 정책
