# G3 — Performance Layer Skills

```yaml
last_updated: 2026-04-10
group: G3
scope: react-kit 고성능 레이어 스킬 2종
skills: [/react-wasm, /react-tauri]
depends_on: [G0 wasm-catalog.md, G1 /react-init]
research_sources:
  - docs/react/wasm-catalog.md (G0 결정 카탈로그)
  - wasm-bindgen Guide (rustwasm.github.io/docs/wasm-bindgen)
  - GoogleChromeLabs/comlink README
  - vite-plugin-comlink (mathe42/vite-plugin-comlink)
  - Tauri 2 Calling Rust from the Frontend (v2.tauri.app)
  - Tauri 2 Capabilities & Permissions (v2.tauri.app/security)
  - Tauri 2 isTauri core API (v2.tauri.app/reference/javascript/api/namespacecore)
  - 2026-04 WebSearch 검증
```

## 문서 목적

react-kit **G3 그룹** 은 앱의 "느린 곳"을 풀어내는 두 개 스킬을 다룬다.

- **`/react-wasm`** — Rust 함수를 WebAssembly 로 컴파일하여 **웹 + Tauri 양쪽 모두** 에서 동작하는 고성능 모듈 생성. G0 `docs/react/wasm-catalog.md` 가 "이 카테고리는 WASM 이득 있음/없음" 을 이미 판정하므로 이 스킬은 카탈로그를 소비 (consume) 하는 자동화 레이어.
- **`/react-tauri`** — Tauri 2 의 Rust 백엔드 command/event 를 정의하고 React 에서 invoke 하는 브릿지 생성. 데스크탑 전용 기능 (파일시스템, 네이티브 메뉴, 쉘, 트레이 등) 을 React 코드에서 호출 가능하게 만든다.

**핵심 제약**: react-kit 의 R eact 코드는 **웹 배포 + Tauri 데스크탑 배포** 양쪽에서 동일하게 동작해야 한다. 따라서 두 스킬 모두 "데스크탑 전용" 코드를 만들지 않고, **feature detection 기반 분기** 로 웹/데스크탑 모두 지원하거나 그럴 수 없는 경우 명시적인 fallback 을 요구한다.

**의존**: G0 `wasm-catalog.md` + G1 `/react-init` 이 생성한 `crates/core/` (Rust workspace) + `src-tauri/` (Tauri Rust backend).

## 공통 설계 원칙

- **Result 경계 불변**: 모든 고성능 호출은 경계를 넘을 때 `neverthrow` 의 `Result<T, Failure>` 로 감싼다. Rust panic, JS throw, Tauri 에러, WASM 부재, 모두 타입 안전한 Failure 로 변환.
- **Clean Architecture 준수**: WASM 호출은 `data/datasources/wasm/` 레이어, Tauri 호출은 `infrastructure/tauri/` 레이어에만 배치. `domain/` 과 `presentation/` 는 하위 런타임을 모른다.
- **Feature detection 우선**: 환경 분기는 런타임 감지로만. 빌드 타임 define 플래그 (예: `if (import.meta.env.TAURI)`) 는 웹 빌드와 데스크탑 빌드가 같은 dist 를 공유하는 시나리오에서 혼란을 유발하므로 보조로만 사용.
- **Strict TypeScript**: WASM 바인딩의 자동 생성 `.d.ts` 를 신뢰하되, 경계 (데이터 진입 시점) 에서 Zod 재검증. Tauri invoke 의 반환값도 마찬가지.
- **G0 카탈로그 불변**: `/react-wasm` 이 Rust 이식 제안 시 반드시 `docs/react/wasm-catalog.md` 의 판정 로직을 1차 기준으로 사용. 카탈로그를 무시하고 사용자 요청만으로 이식 결정 금지.

## /react-wasm vs /react-tauri — 경계 결정 규칙

두 스킬이 기술적으로 유사한 문제 ("느린 부분 네이티브로 보내기") 를 풀지만 **서로 다른 레이어에 배치된다**. 결정 규칙:

| 시나리오 | 선택 | 이유 |
|----------|------|------|
| CPU 바운드 순수 계산 (이미지 처리, 압축, ML 추론) | **`/react-wasm`** | 웹 배포에서도 동작 필요. WASM 이 양쪽 타겟 지원 |
| 파일시스템 접근 (로컬 파일 읽기/쓰기) | **`/react-tauri`** | 브라우저는 File System Access API 로 제한적, Tauri 네이티브 호출로 완전 지원 |
| OS 기능 (네이티브 메뉴, 트레이, 알림, 다이얼로그) | **`/react-tauri`** | 브라우저 불가 |
| 시스템 쉘 / 서브프로세스 | **`/react-tauri`** | 브라우저 불가 |
| 암호화, 압축, 파서 (브라우저 지원 필요) | **`/react-wasm`** | 양 플랫폼 공통 고성능 코드 |
| 네트워크 요청 (특수 프로토콜, 커스텀 TLS) | **`/react-tauri`** | 브라우저 fetch 제약 우회 |
| 앱 내부 업데이터, 자동 실행 | **`/react-tauri`** | Tauri updater plugin 전용 |
| 대용량 데이터 분석 (SQL, columnar) | **`/react-wasm`** (DuckDB-Wasm 등) | 웹에서도 동작, 메모리 모델 통일 |
| 공통 Rust 로직을 네이티브 + WASM 양쪽에 재사용 | **`/react-wasm`** (Rust crate 공유) + **`/react-tauri`** (필요 시 네이티브 command) | `crates/core` 가 공통 crate, 호출 경로만 다름 |

**공존 시나리오**: 한 feature 가 WASM 계산 + Tauri 파일시스템 둘 다 필요하면 두 스킬을 **순차 호출**. `crates/core/` 의 같은 Rust 함수를 WASM 으로 빌드해 Worker 에서 쓰고, Tauri command 로 감싸 파일 I/O 와 묶을 수도 있다.

## 1. /react-wasm — Rust WASM 바인딩 생성

`crates/core/` 의 Rust 함수를 WebAssembly 로 빌드하고, Comlink 래핑된 Web Worker 와 Clean Arch 데이터 레이어 바인딩까지 자동 생성한다.

### 1.1 트리거

- 키워드: "WASM 만들어줘", "Rust 함수 WASM으로", "react-wasm", "고성능 계산 이식"
- 조건: G1 `/react-init --with-wasm` 으로 초기화된 프로젝트 (`crates/core/` 존재). 없으면 에러로 안내

### 1.2 입력

- `task_description` (필수): 이식 대상 작업의 자연어 설명 (예: "이미지 리사이즈", "CSV 파싱 10MB", "폼 검증 빠르게")
- `function_name` (선택): Rust 함수명. 없으면 task 기반 자동 생성
- `--force` (기본 false): 카탈로그가 JS 권장 판정 내려도 강행

### 1.3 자동 판정 로직 (G0 카탈로그 참조)

스킬의 1단계는 **`docs/react/wasm-catalog.md` 의 판정 플로우를 실행** 하는 것이다. 판정은 3단계로 진행:

**Step 1 — 카테고리 키워드 매칭**

카탈로그 §1 (WASM 권장) / §2 (비권장) 테이블과 task_description 을 매칭. 예시 규칙:

- "이미지", "리사이즈", "썸네일", "필터" → §1 이미지 처리 (WASM ✅)
- "압축", "해제", "gzip", "brotli", "lz4", "zstd" → §1 압축 (WASM ✅)
- "폼 검증", "form validation" → §2 폼 검증 (JS ❌)
- "JSON 파싱", "JSON parse" → §2 (JS ❌)
- "이벤트 버스", "state update" → §2 (JS ❌)

카탈로그에 정확히 일치하면 즉시 결정 (권장 또는 거부).

**Step 2 — 휴리스틱 fallback (카탈로그 미스 시)**

카테고리 매칭이 실패하면 G0 카탈로그 §5 의 5개 휴리스틱으로 판정. 스킬이 사용자에게 각 축에 대한 단순 질문 또는 코드 정적 분석으로 자동 채점:

1. **데이터 크기** — 입출력이 바이너리 버퍼 (Uint8Array, Float32Array, ArrayBuffer) + KB~MB 단위?
2. **호출 빈도** — 초당 <100 + 호출당 본 작업 무거움?
3. **내부 연산** — 반복 루프 중심 (for/while), 문자열/객체 조작 없음?
4. **외부 접근** — 순수 함수 (fetch/DOM/timer 없음)?
5. **알고리즘 특성** — SIMD/threads 활용 가능 (픽셀, 해시, 행렬, 정렬)?

각 축 YES = 1점. **3/5 이상 → WASM 제안**, 미만 → JS 유지 권고.

**Step 3 — 최종 사용자 확인**

판정 결과를 사용자에게 요약 제시. 거부 판정이어도 `--force` 플래그가 있으면 사용자 의지 우선으로 진행 (단, 경고 표시).

```
> /react-wasm "이미지 리사이즈"
카탈로그 매칭: §1 이미지 처리 ✅
프로덕션 사례: Figma (29s → 8s), Squoosh
권장 Rust crate: image + fast_image_resize
진행합니다.

> /react-wasm "폼 검증 빠르게"
카탈로그 매칭: §2 폼 검증 ❌
이유: V8 JIT 이 hot small code path 를 이미 공격적으로 최적화. WASM 마샬링 비용 초과.
대안: Zod 스키마 유지. 정말 느리다면 먼저 React Profiler 로 병목 측정.
--force 플래그 없이는 진행하지 않습니다.
```

### 1.4 End-to-End 파이프라인 (WASM 판정 통과 후)

5 단계 자동화:

```
[1. Rust 함수 추가]   crates/core/src/<module>.rs  에 wasm-bindgen 어노테이션 함수 삽입
         ↓
[2. wasm-pack 빌드]   pnpm wasm:build   (wasm-pack build --target web --release)
         ↓
[3. Worker 래퍼]      src/data/datasources/wasm/<module>-worker.ts   Comlink expose
         ↓
[4. Clean Arch 어댑터]   src/data/datasources/wasm/<module>-client.ts  Worker 생성 + Comlink wrap
         ↓
[5. UseCase 바인딩]    src/domain/usecases/<feature>-usecases.ts    Result 반환 추가
```

**[1] Rust 함수 추가** — `crates/core/src/<module>.rs`:

```rust
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn resize_thumbnail(input: &[u8], width: u32, height: u32) -> Result<Vec<u8>, JsError> {
    let img = image::load_from_memory(input)
        .map_err(|e| JsError::new(&format!("decode failed: {e}")))?;
    let resized = img.thumbnail(width, height);
    let mut out = Vec::new();
    resized
        .write_to(&mut std::io::Cursor::new(&mut out), image::ImageFormat::Png)
        .map_err(|e| JsError::new(&format!("encode failed: {e}")))?;
    Ok(out)
}
```

**핵심**: `Result<T, JsError>` 를 사용. `JsError::new(...)` 는 JS 측에서 `Error` 객체로 변환되어 catch 가능. `?` 연산자로 Rust 에러 전파 가능 (`From` 구현).

**[2] wasm-pack 빌드** — G1 이 세팅한 npm 스크립트:

```sh
pnpm wasm:build     # wasm-pack build crates/core --target web --release --out-dir ../../src/wasm/core
```

산출물은 `src/wasm/core/` 에 저장. `.gitignore` 대상 (G1 스캐폴딩 기본값).

**[3] Worker 래퍼** — `src/data/datasources/wasm/image-worker.ts`:

```ts
import { expose } from 'comlink'
import init, { resize_thumbnail } from '@/wasm/core'

let ready: Promise<void> | null = null
function ensureInit(): Promise<void> {
  if (!ready) ready = init().then(() => undefined)
  return ready
}

export const imageWorkerApi = {
  async resizeThumbnail(
    input: Uint8Array,
    width: number,
    height: number,
  ): Promise<Uint8Array> {
    await ensureInit()
    return resize_thumbnail(input, width, height)
  },
}

expose(imageWorkerApi)
```

**[4] Clean Arch 어댑터** — `src/data/datasources/wasm/image-client.ts`:

```ts
import { wrap, type Remote } from 'comlink'
import type { imageWorkerApi } from './image-worker'

let workerInstance: Remote<typeof imageWorkerApi> | null = null

function getClient(): Remote<typeof imageWorkerApi> {
  if (workerInstance) return workerInstance
  const worker = new Worker(new URL('./image-worker.ts', import.meta.url), {
    type: 'module',
  })
  workerInstance = wrap<typeof imageWorkerApi>(worker)
  return workerInstance
}

export async function resizeImageViaWasm(
  input: Uint8Array,
  size: { width: number; height: number },
): Promise<Uint8Array> {
  const client = getClient()
  return client.resizeThumbnail(input, size.width, size.height)
}
```

**[5] UseCase 바인딩** — `src/domain/usecases/image-usecases.ts`:

```ts
import { ok, err, ResultAsync } from 'neverthrow'
import { resizeImageViaWasm } from '@/data/datasources/wasm/image-client'

export type ImageFailure =
  | { kind: 'image/wasm-not-ready'; cause: string }
  | { kind: 'image/resize-failed'; cause: string }

export function resizeImage(
  input: Uint8Array,
  size: { width: number; height: number },
): ResultAsync<Uint8Array, ImageFailure> {
  return ResultAsync.fromPromise(
    resizeImageViaWasm(input, size),
    (e) => ({
      kind: 'image/resize-failed' as const,
      cause: e instanceof Error ? e.message : String(e),
    }),
  )
}
```

### 1.5 Rust panic → Result 변환 경로

Rust 코드가 **패닉**을 일으키면 기본적으로 WASM 런타임이 `RuntimeError` 를 throw 한다. 이건 `JsError` 가 아니라 런타임 에러라서 Result 로 자동 변환되지 않는다.

**처리 흐름**:

1. Rust 쪽: 가능하면 `Result<T, JsError>` 반환으로 **panic 대신 에러 값 반환** 을 우선. `?` 연산자 적극 활용
2. 어쩔 수 없는 panic (무한 재귀, 배열 OOB 등): `console_error_panic_hook` 크레이트 설정으로 panic 메시지를 JS 콘솔에 표시
3. Worker 경계: Comlink 는 throw 된 에러를 Promise reject 로 전달. `ResultAsync.fromPromise(..., (e) => Failure)` 로 모든 throw 를 Failure 로 포획
4. 최종: `resizeImage(...)` 는 panic 까지 포함해 항상 `Result<T, Failure>` 를 반환

**G1 `/react-init` 기본 포함**: `crates/core/Cargo.toml` 에 `console_error_panic_hook` 을 `dev-dependencies` 로 추가하고 `lib.rs` 에 `#[wasm_bindgen(start)]` 함수에서 `set_panic_hook()` 호출.

### 1.6 Gotchas

- **wasm-pack 타겟 선택**: `--target web` 은 ESM 브라우저 로딩용, `--target bundler` 는 번들러 (Vite, Webpack) 용. Vite 에서는 `vite-plugin-wasm` + `--target bundler` 가 가장 매끄럽지만 Tauri 와 섞을 땐 `--target web` 도 가능. G1 기본은 `--target web` + `vite-plugin-wasm` 조합
- **`init()` 중복 호출**: `init()` 을 매 함수 호출마다 부르면 매번 WASM 모듈을 재로드. `ensureInit()` 싱글톤 패턴 필수
- **Worker 싱글톤 누수**: Worker 인스턴스를 매 호출마다 생성하면 Spawn 비용 누적 + 메모리 누수. `getClient()` 싱글톤 + HMR 시 cleanup 고려
- **문자열 마샬링 함정**: G0 카탈로그 §6 오해 2 참조. WASM 함수 인자/반환값이 String 이면 UTF-16↔UTF-8 복사 비용 지속. `Uint8Array` 로 바꾸는 게 거의 항상 빠름
- **render 안에서 호출 금지**: `useMemo` 없이 렌더마다 WASM 호출하면 경계 비용 누적. G0 §8 감사 항목. `/react-audit` 이 검출
- **SIMD 의존 코드의 feature detection**: SIMD 를 쓰면 구형 환경에서 런타임 에러. `WebAssembly.validate` 로 SIMD opcode 지원 확인 후 로드, 미지원 시 fallback 경로 (JS 또는 non-SIMD WASM)
- **번들 크기**: `wasm-opt -O3` 로 최적화. gzip 500KB 이상이면 큼. `/react-audit` 이 경고
- **Strict TS**: `wasm-pack` 이 생성한 `.d.ts` 를 신뢰하지만, WASM 결과 값이 Struct 타입이면 Zod 스키마로 한 번 더 parse 하는 게 안전 (`serde-wasm-bindgen` 으로 교환된 객체는 런타임 타입이 정확히 매칭 안 될 수 있음)

### 1.7 Clean Architecture 배치

- **WASM Rust 함수**: `crates/core/src/<module>.rs`
- **Worker 래퍼**: `src/data/datasources/wasm/<module>-worker.ts` (Comlink `expose`)
- **Worker 클라이언트**: `src/data/datasources/wasm/<module>-client.ts` (Comlink `wrap`)
- **UseCase**: `src/domain/usecases/<feature>-usecases.ts` (Result 반환 공개 API)
- **절대 금지**: `domain/` 또는 `presentation/` 에 WASM 모듈 직접 import. domain 은 WASM 을 모른다.

## 2. /react-tauri — Tauri command/event 바인딩

Tauri 2 의 Rust 백엔드 command 를 정의하고 React 에서 invoke 하는 브릿지를 자동 생성한다. 데스크탑 전용 기능 + **브라우저 fallback** 까지 자동으로.

### 2.1 트리거

- 키워드: "Tauri command 추가", "네이티브 기능", "파일시스템 접근", "react-tauri"
- 조건: G1 `/react-init --with-tauri` 로 초기화된 프로젝트 (`src-tauri/` 존재)

### 2.2 입력

- `command_name` (필수): snake_case (예: `read_config_file`, `open_save_dialog`)
- `feature` (필수): 어느 feature 에 속하는지 (`presentation/features/<feature>/` + `infrastructure/tauri/`)
- `capabilities` (선택): 필요한 Tauri permission 목록 (예: `fs:read`, `dialog:allow-save`)
- `--web-fallback`: 브라우저 환경에서의 fallback 전략 (`throw` 기본, `noop`, `stub`, `prompt-user`)

### 2.3 생성 흐름 — Rust command + TS invoke + capabilities

**[1] Rust command 정의** — `src-tauri/src/commands/config.rs`:

```rust
use serde::{Deserialize, Serialize};
use std::fs;
use std::path::PathBuf;

#[derive(Serialize, Deserialize)]
pub struct AppConfig {
    pub theme: String,
    pub language: String,
}

#[tauri::command]
pub fn read_config_file(path: String) -> Result<AppConfig, String> {
    let buf = PathBuf::from(&path);
    let content = fs::read_to_string(&buf)
        .map_err(|e| format!("failed to read {}: {}", path, e))?;
    serde_json::from_str::<AppConfig>(&content)
        .map_err(|e| format!("invalid config format: {}", e))
}
```

**[2] Builder 등록** — `src-tauri/src/lib.rs`:

```rust
mod commands;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            commands::config::read_config_file,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

**[3] capabilities 선언** — `src-tauri/capabilities/default.json`:

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "description": "Default app capability",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "fs:allow-read-text-file",
    {
      "identifier": "fs:scope",
      "allow": [{ "path": "$APPCONFIG/*.json" }]
    }
  ]
}
```

**[4] TS 래퍼** — `src/infrastructure/tauri/config.ts`:

```ts
import { invoke, isTauri } from '@tauri-apps/api/core'
import { z } from 'zod'
import { ok, err, type Result } from 'neverthrow'

const AppConfigSchema = z.object({
  theme: z.string(),
  language: z.string(),
})
export type AppConfig = z.infer<typeof AppConfigSchema>

export type ReadConfigFailure =
  | { kind: 'config/not-in-tauri' }
  | { kind: 'config/read-failed'; cause: string }
  | { kind: 'config/invalid-format'; issues: string[] }

export async function readConfigFile(path: string): Promise<Result<AppConfig, ReadConfigFailure>> {
  if (!isTauri()) {
    return err({ kind: 'config/not-in-tauri' })
  }
  try {
    const raw = await invoke<unknown>('read_config_file', { path })
    const parsed = AppConfigSchema.safeParse(raw)
    if (!parsed.success) {
      return err({
        kind: 'config/invalid-format',
        issues: parsed.error.issues.map((i) => i.message),
      })
    }
    return ok(parsed.data)
  } catch (e) {
    return err({
      kind: 'config/read-failed',
      cause: e instanceof Error ? e.message : String(e),
    })
  }
}
```

**[5] UseCase 공개** — `src/domain/usecases/config-usecases.ts`:

```ts
import type { ResultAsync } from 'neverthrow'
import type { AppConfig, ReadConfigFailure } from '@/infrastructure/tauri/config'
import { readConfigFile } from '@/infrastructure/tauri/config'

export function loadAppConfig(path: string) {
  return readConfigFile(path)  // 이미 Promise<Result<...>> 반환
}
```

### 2.4 Feature detection gating

**공식 권장 API** (Tauri 2): `@tauri-apps/api/core` 의 `isTauri()` 함수 또는 `window.isTauri()` 전역.

```ts
import { isTauri } from '@tauri-apps/api/core'

if (isTauri()) {
  // 데스크탑 경로
} else {
  // 브라우저 경로 (fallback)
}
```

**사용 규칙**:

- **infrastructure 경계에서만 분기**: `infrastructure/tauri/*.ts` 함수 첫 줄에 `if (!isTauri())` 체크. 그 위 레이어 (domain, presentation) 는 환경을 모른다
- **fallback 전략 4가지** (`--web-fallback` 플래그):
  1. **throw** (기본): `Failure` 로 반환. 호출부가 UI 로 "데스크탑 앱에서만 지원" 표시
  2. **noop**: 조용히 성공 (`ok(undefined)`). 데스크탑 기능이 없어도 앱이 동작하는 optional feature
  3. **stub**: 미리 준비된 stub 값 반환. 개발 중 UI 만 확인하고 싶을 때
  4. **prompt-user**: 사용자에게 "데스크탑 앱 설치하시겠어요?" 안내 (presentation 쪽에서 처리)

**빌드 타임 분기는 보조**: Vite 환경 변수 `import.meta.env.TAURI` 를 직접 분기 조건으로 쓰지 말 것. 런타임 `isTauri()` 가 단일 진실 공급원. 이유: 같은 dist 를 웹과 데스크탑 모두에 배포할 수 있음 (Tauri 는 내부 WebView 에서 dist 를 그대로 로드).

### 2.5 Tauri API 실패 + 브라우저 미지원 처리

**실패 케이스 3가지**:

1. **Tauri 미탑재 (브라우저 환경)**: `isTauri()` 가 false → `kind: '<feature>/not-in-tauri'` Failure 즉시 반환
2. **invoke 실패 (command 에러)**: Rust command 가 `Err(String)` 반환 → JS 측에서 throw → catch 후 `kind: '<feature>/read-failed'` 로 변환
3. **invoke 성공했지만 타입 불일치**: Rust 가 예상과 다른 shape 반환 → Zod parse 실패 → `kind: '<feature>/invalid-format'`

**모든 경로가 Result 로 수렴**: 호출부는 하나의 `isErr()` 체크와 `switch (error.kind)` 로 분기.

### 2.6 Gotchas

- **`window.isTauri` vs `isTauri()` import**: 둘 다 동작하지만 타입 안전한 import 방식 권장 (`@tauri-apps/api/core`). 전역 `window.isTauri` 는 `withGlobalTauri` 설정이 필요
- **capabilities 누락 에러**: 새 command 를 Rust 에 추가하고 Builder 에 등록해도 `capabilities/*.json` 에 권한이 없으면 런타임에 "not allowed" 에러. 이 스킬은 capabilities 자동 수정 포함
- **권한 식별자 최소화**: `fs:allow-read-text-file` 처럼 구체적 권한만 부여. `fs:default` 같은 광범위 권한은 감사에서 경고
- **`invoke<T>` 제네릭의 unknown 처리**: Tauri 2 의 `invoke` 반환 타입이 `T` 로 유추되지만, 실제 런타임 값은 검증 안 됨. `invoke<unknown>('...')` 후 Zod parse 로 강제. Strict TS 정책
- **데스크탑 전용 command 를 웹 빌드에서 참조**: TypeScript 컴파일은 통과하지만 런타임 분기 안 하면 브라우저에서 crash. 반드시 `isTauri()` 가드
- **이벤트 리스너 cleanup**: `listen('event', ...)` 사용 시 unmount 에서 unsubscribe 필수. React `useEffect` cleanup 에서 반환
- **Rust command 의 `tauri::State` 공유**: 복수 command 가 상태 공유하려면 `app.manage(...)` 로 등록 + `State<'_, T>` 인자. 이 스킬은 stateless command 가 기본, stateful 은 옵션
- **mobile 대응**: Tauri 2 의 iOS/Android 는 별도 permission 스키마가 필요할 수 있음. react-kit 기본은 desktop 만 다루고 mobile 은 별도 확장 스킬 여지
- **Strict TS**: Rust command 시그니처와 TS invoke 제네릭을 수동으로 맞추는 대신, `tauri-bindgen` 같은 codegen 도구를 고려. react-kit 기본은 수동 + Zod 검증 (추가 의존성 최소화)

### 2.7 Clean Architecture 배치

- **Rust command**: `src-tauri/src/commands/<module>.rs`
- **TS 래퍼**: `src/infrastructure/tauri/<module>.ts` — invoke + isTauri 가드 + Zod parse + Result 반환
- **UseCase**: `src/domain/usecases/<feature>-usecases.ts` — infrastructure/tauri 의 함수를 재노출 (얇은 래퍼)
- **presentation 훅**: `src/presentation/features/<feature>/hooks/use-<action>.ts` — UseCase 를 TanStack Query mutation 으로 감쌈
- **절대 금지**: `domain/`, `data/`, `presentation/` 에서 `@tauri-apps/api/*` 직접 import. 모든 Tauri 호출은 `infrastructure/tauri/` 경유

## 3. 웹/데스크탑 통합 배포 전략

react-kit 의 핵심 약속: **같은 React 소스가 양쪽 타겟 모두에서 동작한다**.

### 빌드 흐름

```
src/  ────────┬── pnpm build  ────► dist/        ────► 웹 호스팅 (S3, CDN, Vercel 등)
              │                                          (브라우저에서 실행, isTauri() = false)
              │
              └── pnpm tauri build ──► src-tauri/target/release/  ────► 데스크탑 바이너리
                                                                        (Tauri WebView 에서 dist/ 로드, isTauri() = true)
```

**동일한 `dist/`** 가 두 경로에 사용된다. 브라우저에서는 직접 hosting, Tauri 는 로컬 파일시스템에서 로드.

### 조건부 기능 활성화

- `isTauri()` 로 런타임 체크
- presentation 컴포넌트는 "데스크탑 전용 기능" 을 conditionally render
- fallback 전략 (throw / noop / stub / prompt-user) 이 명시적으로 선언되어야 UX 일관성 유지

### 데스크탑 우위 활용

Tauri 빌드에서만 쓸 수 있는 것:
- WASM SIMD + threads (COOP/COEP 헤더 걱정 없음, 내부 WebView 설정 제어 가능)
- 네이티브 파일 I/O, OS 다이얼로그, 트레이
- 더 긴 CPU 작업 허용 (브라우저 탭처럼 백그라운드 throttling 없음)
- 원한다면 동일 Rust 코드를 WASM 이 아니라 **네이티브로 직접 호출** (Tauri command 경로) — 경계 비용 더 낮음

### 공유 Rust 코어

`crates/core/` 의 함수는:
- **웹 + Tauri 양쪽** 모두에서 WASM 으로 호출 가능 (`/react-wasm` 경로)
- **Tauri 에서만** 네이티브로 직접 호출 가능 (`src-tauri/` 가 `crates/core` 를 dependency 로 import → Tauri command 로 노출)

이 구조가 고성능 코드 중복을 완전히 제거. 이게 react-kit 이 Electron 이 아니라 Tauri 를 선택한 가장 큰 이유.

## 4. 공유 helpers 및 Cross-group 관계

- **G0 카탈로그**: `/react-wasm` 자동 판정의 1차 소스
- **G1 `/react-init`**: `crates/core/`, `src-tauri/`, `vite-plugin-wasm`, `vite-plugin-top-level-await`, `console_error_panic_hook` 전부 기본 세팅
- **G2 `/react-api`** 와 공존: Tauri command 도 Clean Arch 데이터 레이어의 한 datasource 로 취급 (infrastructure/tauri → data/repositories 에서 consume 가능)
- **G4 `/react-test`**: WASM 함수는 Vitest + jsdom 환경에서 테스트 (node 타겟이 아닌 browser), Tauri command 는 Playwright e2e 로 실행 가능 (Tauri webdriver)
- **G6 `/react-audit`**: WASM render-in-loop 검출, SIMD feature detection 가드 누락 검출, Tauri command 의 capabilities 누락 검출, `isTauri()` 가드 누락 검출

## 5. 출처 요약

1. wasm-bindgen Guide — Result 타입: https://rustwasm.github.io/docs/wasm-bindgen/reference/types/result.html
2. wasm-bindgen JsError 문서: https://docs.rs/wasm-bindgen/latest/wasm_bindgen/struct.JsError.html
3. wasm-bindgen 전체 가이드: https://rustwasm.github.io/docs/wasm-bindgen/
4. serde-wasm-bindgen: https://docs.rs/serde-wasm-bindgen
5. Comlink GitHub: https://github.com/GoogleChromeLabs/comlink
6. vite-plugin-comlink: https://github.com/mathe42/vite-plugin-comlink
7. Tauri 2 — Calling Rust from Frontend: https://v2.tauri.app/develop/calling-rust/
8. Tauri 2 — Capabilities: https://v2.tauri.app/security/capabilities/
9. Tauri 2 — Permissions: https://v2.tauri.app/security/permissions/
10. Tauri 2 — core namespace (isTauri): https://v2.tauri.app/reference/javascript/api/namespacecore/
11. Tauri 2 discussion — browser detection: https://github.com/tauri-apps/tauri/discussions/6119
12. Tauri 2 Stable Release: https://v2.tauri.app/blog/tauri-20/
13. Menci/vite-plugin-wasm: https://github.com/Menci/vite-plugin-wasm
14. docs/react/wasm-catalog.md (G0, 이 레포 내부 문서)

## 6. 변경 이력

- **2026-04-10** — 초판. G3 2개 스킬 (`/react-wasm`, `/react-tauri`) 상세 설계. WebSearch fallback 으로 wasm-bindgen Result, Comlink + Vite 통합, Tauri 2 invoke/capabilities/isTauri 공식 문서 검증. G0 wasm-catalog.md 의 판정 로직 참조 흐름 통합.
