---
name: react-wasm
description: >
  Rust 함수를 WebAssembly로 컴파일하고 Comlink Worker + Clean Architecture 데이터 레이어 바인딩까지 자동 생성한다.
  "WASM 추가", "Rust WASM", "wasm-bindgen", "고성능 계산 이식", "wasm-pack 빌드", "Rust 바인딩", "react-wasm" 같은 요청 시 트리거.
  WASM 이식 전 G0 카탈로그 자동 판정을 실행하고, 비권장 카테고리는 거부 후 이유를 설명한다.
  UI/DOM 작업, 폼 검증, JSON 파싱 등 JS로 충분한 연산에는 트리거하지 않는다.
argument-hint: "<task_description> [function_name] [--force]"
user-invocable: true
---

# Gotchas

1. **G0 카탈로그 우선** — 사용자 요청만으로 이식 결정 금지. 반드시 `docs/react/wasm-catalog.md` §1/§2 카테고리 매칭을 1단계로 실행한다. 카탈로그가 비권장으로 판정하면 `--force` 없이 진행하지 않는다.
2. **경계 비용 수치 인식** — JS↔WASM 호출 오버헤드 약 50~100 ns/call, 문자열 마샬링 약 600~2,500 ns/call (unverified secondary source). 고빈도 콜백(>1만/sec)이나 tiny 함수(<100 μs)는 경계 비용이 본 작업 비용을 압도한다. 이 두 유형은 카탈로그 §2 비권장에 명시적으로 포함되어 있다.
3. **Rust panic → Result 변환 필수** — Rust 함수는 반드시 `Result<T, JsError>`를 반환해야 한다. `?` 연산자로 에러 전파, `JsError::new(&format!("..."))` 로 JS Error 객체 변환. panic이 JS 경계를 넘는 것을 허용하지 않는다. `console_error_panic_hook`으로 패닉 메시지를 콘솔에 표시하고, Worker 경계에서 Comlink가 throw를 Promise reject로 전달하면 `ResultAsync.fromPromise`로 포획한다.
4. **`init()` 싱글톤 필수** — WASM 모듈 초기화를 매 함수 호출마다 실행하면 매번 재로드 발생. `ensureInit()` 패턴으로 한 번만 초기화한다.
5. **Worker 싱글톤 필수** — `getClient()` 패턴으로 Worker 인스턴스를 재사용한다. 매 호출마다 `new Worker()`하면 Spawn 비용 누적 + 메모리 누수.
6. **렌더 경로 호출 금지** — `useMemo` 없이 렌더마다 WASM 함수를 호출하면 경계 비용 누적. `/react-audit` G6이 이 패턴을 검출한다.
7. **문자열 인자 최소화** — WASM 함수 인자/반환값이 `String`이면 UTF-16↔UTF-8 복사 비용 지속. 가능하면 `Uint8Array`/`ArrayBuffer`로 대체한다. 1 KB 이상 문자열을 빈번히 전달하면 `/react-audit`이 경고를 발행한다.
8. **wasm-pack 타겟 선택** — G1 기본은 `--target web` + `vite-plugin-wasm` 조합. Vite 번들러 전용이면 `--target bundler`도 가능하지만 Tauri와 혼용 시 `--target web`이 안전하다.
9. **SIMD feature detection 필수** — SIMD 의존 WASM은 구형 환경에서 런타임 에러 발생. `WebAssembly.validate`로 SIMD opcode 지원 확인 후 로드, 미지원 시 JS fallback 경로 또는 non-SIMD WASM으로 전환한다.
10. **번들 크기** — `wasm-opt -O3` 최적화 필수. gzip 500 KB 이상이면 `/react-audit`이 경고를 발행한다.
11. **Strict TS** — `wasm-pack`이 생성한 `.d.ts`를 신뢰하되, `serde-wasm-bindgen`으로 교환된 Struct 타입은 Zod 스키마로 추가 검증한다.
12. **crates/core 사전 확인** — G1 `/react-init --with-wasm`으로 초기화된 프로젝트에만 적용. `crates/core/` 디렉토리가 없으면 에러로 안내하고 `/react-init --with-wasm`을 먼저 실행하도록 유도한다.
13. **`Transferable` 활용** — `ArrayBuffer`를 Worker로 전달할 때 Transferable로 zero-copy 이동 가능. 원본 보존이 필요한 경우만 복사한다(복사 비용 ~1~3 ms / MB).
14. **rustwasm org 아카이빙 (2025-09)** — wasm-pack, gloo, twiggy, walrus 등 rustwasm GitHub org 프로젝트가 아카이빙됐다. **wasm-bindgen 만 독립 org (`github.com/wasm-bindgen/wasm-bindgen`) 로 이전**. wasm-pack 은 여전히 동작하지만 신규 메인테이너 활동이 제한적이다. 대안으로 `wasm-bindgen-cli` + `wasm-opt` + 빌드 스크립트 직접 조합이 커스텀 cargo profile, 병렬 빌드 등에서 유리하다. react-kit 기본은 wasm-pack 유지하되, 빌드 커스터마이징이 필요하면 대안 경로를 안내한다.
15. **WASM SIMD 128-bit 전 브라우저 지원** — 2025 초 기준 모든 주요 브라우저에서 128-bit SIMD 를 지원한다. SIMD 활용 시 특정 워크로드에서 JS 대비 10-15배 성능 향상이 가능하다. 단, Gotcha #9 의 feature detection 은 여전히 필수 — SIMD opcode 미지원 환경에서 런타임 에러가 발생한다.

# Process

## 1. 프로젝트 환경 감지

`references/project-detection.md` 절차를 실행한다. `crates/core/`, `wasm-pack` 설치, `vite-plugin-wasm` 패키지 존재 여부를 확인한다. `crates/core/` 가 없으면 안내 후 중단:

```text
crates/core/ 디렉토리를 찾을 수 없습니다.
/react-init --with-wasm 을 먼저 실행해 Rust WASM 워크스페이스를 세팅하세요.
```

## 2. 입력 수집

- `task_description` (필수): 이식 대상 작업의 자연어 설명 (예: "이미지 리사이즈", "CSV 파싱 10MB", "lz4 압축")
- `function_name` (선택): Rust 함수명 snake_case. 없으면 task_description 기반 자동 생성
- `--force` (기본 false): 카탈로그 비권장 판정이어도 강행 (경고 표시 후 진행)

## 3. G0 카탈로그 자동 판정 (필수 — 건너뛰기 금지)

### 3-1. 카테고리 키워드 매칭

`docs/react/wasm-catalog.md` §1 / §2 테이블과 `task_description`을 대조한다.

**§1 권장 카테고리 → WASM 진행:**

| 키워드 | 카테고리 | 추천 크레이트 |
|--------|----------|--------------|
| 이미지, 리사이즈, 썸네일, 필터, 코덱 | 이미지 처리 | `image`, `fast_image_resize` |
| 압축, 해제, gzip, brotli, lz4, zstd | 압축/해제 | `lz4_flex`, `brotli`, `zstd` |
| ML, 추론, ONNX, tensor, 뉴럴넷 | ML 추론 | `tract-onnx`, `ndarray` |
| SQL, DB, 쿼리, columnar, DuckDB | SQL/DB 엔진 | `duckdb-wasm`(JS), `sqlx`(네이티브) |
| markdown, protobuf, 바이너리 포맷, wasmparser | 복잡 파서 | `pulldown-cmark`, `prost` |
| FFT, 행렬, 수치 계산, 물리 | 수치 계산 | `nalgebra`, `rustfft`, `rapier` |
| 집계, 스캔, JOIN, 10만 row | 대용량 집계 | DuckDB-Wasm, DataFusion |
| blake3, argon2, AES-CTR, 스트림 해시 | 암호화 bulk | `hash-wasm`(JS), `argon2`, `blake3` |
| 비디오, 오디오, 인코딩, 디코딩, ffmpeg | 비디오/오디오 | ffmpeg.wasm 또는 커스텀 코덱 |

**§2 비권장 카테고리 → 거부 (--force 없이):**

| 키워드 | 카테고리 | 이유 |
|--------|----------|------|
| DOM, 컴포넌트, 렌더, React 상태 | UI/DOM | WebAssembly DOM 직접 접근 불가. 경계 비용이 본 작업 지배 |
| 폼 검증, form validation, Zod | 폼 검증 | V8 JIT이 hot small code path 최적화. 마샬링 비용 초과 |
| JSON 파싱, JSON.parse, JSON.stringify | JSON 처리 | V8 네이티브 SIMD급 최적화. WASM 이식 이득 없음 |
| 정규식, split, concat, 문자열 처리 | 문자열 처리 | UTF-16↔UTF-8 마샬링 비용 항상 발생 |
| 단발 AES-GCM, SHA-256 한 번 | Web Crypto 소규모 | 브라우저 SubtleCrypto API가 이미 네이티브 |
| 이벤트 버스, reducer, Zustand | 이벤트/state | hot small path. V8 JIT 영역 |
| 애니메이션, 스크롤, 드래그 | 애니메이션 | requestAnimationFrame + CSS/GPU 경로가 정답 |
| fetch, 네트워크, HTTP | 네트워크 | I/O 바운드. CPU 가속 의미 없음 |

### 3-2. 판정 결과 출력

카탈로그 매칭 결과를 사용자에게 표시:

```text
# 카탈로그 §1 이미지 처리 ✅
프로덕션 사례: Figma (29s → 8s), Squoosh
권장 크레이트: image + fast_image_resize
진행합니다.
```

```text
# 카탈로그 §2 폼 검증 ❌
이유: V8 JIT이 hot small code path를 이미 공격적으로 최적화.
      WASM 마샬링 비용(약 600~2,500 ns/call)이 본 연산 비용을 초과합니다.
대안: Zod 스키마 유지. 정말 느리다면 React Profiler로 병목 먼저 측정.
--force 플래그 없이는 진행하지 않습니다.
```

### 3-3. 카탈로그 미스 시 5개 휴리스틱

카테고리 매칭이 실패하면 `docs/react/wasm-catalog.md` §5 휴리스틱으로 판정한다. 각 축을 정적 분석 또는 사용자 질문으로 채점:

| 축 | WASM 쪽 (YES=1점) | JS 쪽 |
|----|-------------------|-------|
| H1. 데이터 크기 | 바이너리 버퍼 (Uint8Array, Float32Array), KB~MB 단위 | 문자열, 일반 객체, <1 KB |
| H2. 호출 빈도 | 초당 <100 + 호출당 ms 단위 무거운 연산 | 초당 >1만 + 가벼운 연산 |
| H3. 내부 연산 | 반복 루프, 숫자/바이너리 위주, 분기 적음 | 문자열/객체 조작, 정규식, DOM |
| H4. 외부 접근 | 순수 함수 (fetch/DOM/timer 없음) | 외부 접근 있음 |
| H5. 알고리즘 | SIMD/threads 활용 가능 (픽셀, 해시, 행렬, 정렬) | 본질적으로 순차적 |

**3/5 이상** → WASM 제안. **미만** → JS 유지 또는 Web Worker(T1) 권고.

## 4. 사용자 최종 확인

판정 결과 요약 후 진행 여부 확인. `--force` 플래그가 있으면 비권장 판정도 경고 후 진행.

## 5. End-to-End 파이프라인 실행

5단계 자동 생성:

```text
[1. Rust 함수 추가]    crates/core/src/<module>.rs — wasm-bindgen 어노테이션
         ↓
[2. wasm-pack 빌드]    pnpm wasm:build — --target web --release
         ↓
[3. Worker 래퍼]       src/data/datasources/wasm/<module>-worker.ts — Comlink expose
         ↓
[4. Clean Arch 클라이언트]  src/data/datasources/wasm/<module>-client.ts — Worker 생성 + Comlink wrap
         ↓
[5. UseCase 바인딩]    src/domain/usecases/<feature>-usecases.ts — Result 반환 공개 API
```

### 5-1. Rust 함수 추가

`crates/core/src/<module>.rs`:

```rust
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn <function_name>(input: &[u8], /* 파라미터 */) -> Result<Vec<u8>, JsError> {
    // 실제 연산 로직
    let result = do_work(input)
        .map_err(|e| JsError::new(&format!("연산 실패: {e}")))?;
    Ok(result)
}
```

**핵심 규칙:**
- 반환 타입은 반드시 `Result<T, JsError>` — panic이 JS 경계를 넘지 못하게 한다
- `?` 연산자로 Rust 에러를 전파, `From` 구현으로 자동 변환
- `JsError::new(...)` 는 JS 측에서 `Error` 객체로 변환되어 catch 가능
- 문자열 인자 최소화 — 가능하면 `&[u8]` 또는 `Uint8Array` 사용

G1 기본 포함 항목 확인: `crates/core/Cargo.toml`에 `console_error_panic_hook` dev-dependency + `lib.rs`에 `#[wasm_bindgen(start)]`에서 `set_panic_hook()` 호출.

### 5-2. wasm-pack 빌드

```bash
pnpm wasm:build
# 내부: wasm-pack build crates/core --target web --release --out-dir ../../src/wasm/core
```

산출물 `src/wasm/core/` 는 `.gitignore` 대상 (G1 기본값).

SIMD 의존 모듈인 경우 런타임 feature detection 코드를 함께 생성한다:

```ts
const SIMD_PROBE = new Uint8Array([
  0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00,
  0x01, 0x05, 0x01, 0x60, 0x00, 0x01, 0x7b, 0x03,
  0x02, 0x01, 0x00, 0x0a, 0x0a, 0x01, 0x08, 0x00,
  0xfd, 0x0f, 0x00, 0x00, 0x00, 0x00, 0x0b,
])

export const simdSupported = WebAssembly.validate(SIMD_PROBE)
```

### 5-3. Comlink Worker 래퍼

`src/data/datasources/wasm/<module>-worker.ts`:

```ts
import { expose } from 'comlink'
import init, { <function_name> } from '@/wasm/core'

let ready: Promise<void> | null = null

function ensureInit(): Promise<void> {
  if (!ready) ready = init().then(() => undefined)
  return ready
}

export const <module>WorkerApi = {
  async <camelFunction>(
    input: Uint8Array,
    // 파라미터 추가
  ): Promise<Uint8Array> {
    await ensureInit()
    return <function_name>(input /* 파라미터 */)
  },
}

expose(<module>WorkerApi)
```

### 5-4. Clean Arch 클라이언트

`src/data/datasources/wasm/<module>-client.ts`:

```ts
import { wrap, type Remote } from 'comlink'
import type { <module>WorkerApi } from './<module>-worker'

let workerInstance: Remote<typeof <module>WorkerApi> | null = null

function getClient(): Remote<typeof <module>WorkerApi> {
  if (workerInstance) return workerInstance
  const worker = new Worker(new URL('./<module>-worker.ts', import.meta.url), {
    type: 'module',
  })
  workerInstance = wrap<typeof <module>WorkerApi>(worker)
  return workerInstance
}

export async function <camelFunction>ViaWasm(
  input: Uint8Array,
  // 파라미터
): Promise<Uint8Array> {
  const client = getClient()
  return client.<camelFunction>(input /* 파라미터 */)
}
```

### 5-5. Domain UseCase 바인딩

`src/domain/usecases/<feature>-usecases.ts`:

```ts
import { ResultAsync } from 'neverthrow'
import { <camelFunction>ViaWasm } from '@/data/datasources/wasm/<module>-client'

export type <Feature>Failure =
  | { kind: '<feature>/wasm-not-ready'; cause: string }
  | { kind: '<feature>/operation-failed'; cause: string }

export function <camelFeature>(
  input: Uint8Array,
  // 파라미터
): ResultAsync<Uint8Array, <Feature>Failure> {
  return ResultAsync.fromPromise(
    <camelFunction>ViaWasm(input /* 파라미터 */),
    (e) => ({
      kind: '<feature>/operation-failed' as const,
      cause: e instanceof Error ? e.message : String(e),
    }),
  )
}
```

**panic 포획 경로**: WASM panic → `console_error_panic_hook`이 콘솔에 표시 → Comlink가 throw를 Promise reject로 전달 → `ResultAsync.fromPromise`가 `Failure`로 변환 → 호출부는 항상 `Result<T, Failure>`를 받는다.

## 6. 완료 후 안내

생성 파일 목록 출력. 다음 단계:
- WASM 연산 결과를 UI에 연결: `/react-query` (TanStack Query mutation)
- 화면 추가: `/react-screen`
- 감사: `/react-audit` (WASM render-in-loop, SIMD guard, 번들 크기 검사)

# References

- `references/project-detection.md` — 프로젝트 환경 감지
- `references/clean-arch-layout.md` — 레이어 배치 규칙 (datasources/wasm/, domain/usecases/)
- `references/wasm-catalog.md` — G0 판정 카탈로그 포인터 (`docs/react/wasm-catalog.md` 경유)
- `docs/react/wasm-catalog.md` — §1 권장 9종 / §2 비권장 10종 / §3 경계 비용 / §4 SIMD+Threads / §5 휴리스틱
- `docs/react/kit-design/g3-performance.md` §1 — 이 스킬 상세 설계 (파이프라인, Gotchas, Clean Arch 배치)
