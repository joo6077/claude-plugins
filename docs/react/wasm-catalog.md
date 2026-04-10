# WASM Decision Catalog — react-kit

```yaml
last_updated: 2026-04-10
status: draft
scope: react-kit /react-wasm skill 판정 기준
research_sources:
  - Codex 백그라운드 리서치 (task-mnshueuy-tz63ae, 2026-04-10)
  - V8/Chromium engineering blogs (2019~2026)
  - MDN WebAssembly reference (2026-03 최신)
  - Production engineering posts: Figma, Squoosh, ffmpeg.wasm, DuckDB-Wasm
  - 학술: Jangda et al. "Not So Fast" (USENIX ATC 2019) + 후속 벤치마크
```

## 문서 목적

이 문서는 react-kit의 `/react-wasm` 스킬이 "어떤 코드를 Rust → WebAssembly로 이식할지, 어떤 코드를 JavaScript/TypeScript로 둘지" 판정할 때 사용하는 리서치 기반 카탈로그다. 사용자에게 매번 벤치마크를 요구하지 않고, 공개된 프로덕션 사례와 엔진 벤치마크로 **카테고리 단위 사전 판정**을 내린다.

원칙: **측정 없이 가정하지 말고, 가정 없이 이식하지 말라.** 카탈로그는 이미 누가 측정한 결과의 응축본이다.

## 1. WASM 권장 카테고리

아래 카테고리는 공개된 프로덕션 시스템 또는 엔진팀 벤치마크에서 WebAssembly가 JavaScript를 유의미하게 앞선 것이 확인된 영역이다. `/react-wasm`은 이 카테고리 매칭 시 자동으로 Rust 크레이트 + `wasm-pack` 바인딩을 제안한다.

| 카테고리 | 근거 (측정/프로덕션) | 프로덕션 사례 | 출처 URL |
|---|---|---|---|
| **이미지 처리** (resize, filter, codec) | Figma의 dense-file 로드 경로가 WebAssembly 최적화 후 29s → <8s (약 3.6x) 로 개선. Squoosh는 WASM 코덱·hot path를 출시 이후 전 브라우저에서 일관된 이득 확인 | Figma, Squoosh | https://www.figma.com/blog/figma-faster/ , https://developer.chrome.com/blog/hotpath-with-wasm?hl=en |
| **비디오/오디오 인코딩·디코딩** | 브라우저에서 ffmpeg.wasm이 SIMD/threads로 C/C++ 코덱 스택을 실용적 속도로 구동. JS 기준 baseline은 현실적으로 존재하지 않아 "JS 대비 N배" 수치는 unverified, 그러나 "실용성 자체가 WASM 덕"이라는 점은 확립 | ffmpeg.wasm | https://ffmpegwasm.netlify.app/docs/performance/ |
| **압축/해제** (lz4, brotli, zstd, gzip) | `lz4-wasm` README 벤치마크: 66k JSON에서 compression ~2.9x (292 vs 101 MB/s), decompression ~25x (687 vs 27 MB/s) 대비 `lz4 js` | lz4-wasm, fflate, brotli-wasm | https://github.com/PSeitz/lz4-wasm |
| **ML 추론** (ONNX, TFLite, tensor ops) | V8 SIMD 적용 시 hand-tracking 추론이 14~15 FPS → 38~40 FPS (약 2.6x). XNNPACK·MediaPipe가 WASM 백엔드로 이식됨 | MediaPipe, onnxruntime-web, transformers.js | https://v8.dev/features/simd , https://onnxruntime.ai/docs/tutorials/web/deploy.html |
| **SQL / DB 엔진** | DuckDB-Wasm이 TPC-H 다중 스케일에서 이전 웹 데이터 처리 라이브러리들을 앞섬. Worker 안에서 비동기 분석 SQL 실행 | DuckDB-Wasm, sql.js | https://duckdb.org/library/duckdb-wasm/ |
| **복잡 파서** (markdown, SQL, 바이너리 포맷, protobuf) | `markdown-wasm`이 JS 파서 대비 벤치마크 우위를 공식 문서화. 단, JS 콜백으로 빠져나갈수록 bridge overhead로 이득이 깎임을 명시 | markdown-wasm, wasmparser | https://github.com/rsms/markdown-wasm |
| **수치 계산 / 행렬 / FFT** | `pffft.wasm`이 pure JS FFT 베이스라인을 SIMD로 추월. 정확한 고정 배수는 머신 의존적으로 unverified, 방향성은 확립 | pffft.wasm, Rapier 물리 엔진 | https://0110.be/l/pffft_benchmark , https://github.com/JorenSix/pffft.wasm |
| **대용량 집계** (>10만 row 스캔·집계·JOIN) | DuckDB-Wasm이 브라우저에서 컬럼형 벡터 실행으로 분석 SQL을 Worker 안에서 구동 | DuckDB-Wasm, DataFusion WASM, Arquero | https://duckdb.org/library/duckdb-wasm/ |
| **암호화 bulk** (blake3, argon2, 스트림 AES-CTR) | 반복 라운드가 많은 해시/KDF는 WASM이 네이티브 레이아웃과 SIMD로 JS 대비 우위. 정확 배수는 알고리즘별 상이, 방향성 확립 | hash-wasm, argon2-browser | (catalog: hash-wasm 벤치마크 페이지, unverified specific numbers) https://github.com/Daninet/hash-wasm |

**공통 원인 (왜 WASM이 이기는가)**
- 타이트한 내부 루프 + 명시적 메모리 레이아웃 + 낮은 GC 압력
- SIMD 벡터화 가능한 산술 (pixel, float 배열)
- JS↔WASM 경계 진입은 드물고, 한 번 들어가면 오래 머무는 호출 패턴
- 캐시 친화적 데이터 구조 (columnar, struct-of-arrays)

## 2. WASM 비권장 카테고리 (JS/TS 유지)

아래 카테고리는 **WASM으로 이식해도 이득이 없거나 오히려 손해**인 영역이다. `/react-wasm`은 이 카테고리 매칭 시 제안을 거부하고 이유를 설명한다.

| 카테고리 | 이유 | 출처 |
|---|---|---|
| **UI 상태, DOM 인접 작업, 컴포넌트 렌더** | WebAssembly는 DOM 직접 접근 불가. 모든 DOM 업데이트가 JS 글루를 통과하므로 경계 비용이 본 작업 비용을 지배 | https://developer.mozilla.org/en-US/docs/WebAssembly , https://v8.dev/blog/v8-release-90 |
| **폼 검증, 작은 함수, 소규모 리스트 (<1만 아이템)** | V8 JIT (Sparkplug, Maglev, TurboFan) 이 hot small code path를 공격적으로 최적화. JS↔WASM 래퍼 비용이 남아 JS가 동률 또는 우위 | https://v8.dev/blog/maglev , https://v8.dev/blog/v8-release-90 |
| **JSON 파싱 / 직렬화** | V8가 Chrome 138에서 `JSON.stringify`를 "2x 이상" 향상. JSON 경로는 이미 네이티브 SIMD급 최적화. WASM 이식 이득 unverified | https://v8.dev/blog/json-stringify |
| **문자열 처리 (정규식, split, concat, template)** | JS 문자열은 엔진 네이티브. WASM은 UTF-16↔UTF-8 마샬링/복사 비용을 항상 지불. V8 Irregexp은 매우 빠름 | https://github.com/rsms/markdown-wasm (bridge overhead 경고), https://v8.dev/blog/v8-release-90 |
| **Web Crypto 소규모 호출** (단발 AES-GCM, SHA-256 한 번) | 브라우저가 이미 네이티브 crypto API를 노출. 소규모 호출의 WASM 우위는 unverified이며 경계 비용에 묻힐 가능성 큼 | https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto |
| **고빈도 콜백 (>1만/sec)** | 매 호출마다 JS↔WASM 경계를 넘으면 누적 비용이 compute 비용을 압도. 배치화하지 못하면 WASM 금기 | https://github.com/rsms/markdown-wasm (JS callback overhead 문서화) |
| **tiny 함수 (<100μs per call)** | 호출 오버헤드 (추정 50~100 ns 급, unverified) 가 상대적으로 크게 느껴짐. 호출당 compute가 작을수록 JS 우위 | https://v8.dev/blog/v8-release-90 |
| **애니메이션, 스크롤, 드래그** | `requestAnimationFrame` + CSS/GPU 경로가 정답. WASM은 프레임 예산 16ms를 깎아먹을 뿐 | https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame |
| **네트워크 호출, fetch 래퍼, 요청 파이프라인** | I/O 바운드. CPU 가속 의미 없음 | https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API |
| **이벤트 버스, 작은 reducer, Zustand store 업데이트** | hot small path. V8 JIT 영역 | https://v8.dev/blog/maglev |

## 3. Boundary Cost — 경계 넘기 비용 (2025~2026)

WASM 결정에서 가장 자주 오해되는 축. "WASM이 빠르니까 작은 것도 옮기자"는 이 수치 때문에 거의 항상 손해다.

| 비용 항목 | 수치 | 비고 |
|---|---|---|
| JS ↔ WASM 호출 오버헤드 (정수 인자) | **50~100 ns / call** (추정, unverified) | 2025 secondary source 기반. primary 검증 미완. 호출 빈도가 초당 수십만을 넘으면 누적 비용 체감 |
| 문자열 마샬링 (짧은 문자열) | **600~2,500 ns / call** (추정, unverified) | 동일 secondary source. 긴 문자열 per-KB 수치는 unverified. UTF-16↔UTF-8 변환 비용 포함 |
| ArrayBuffer 전송 (zero-copy) | **~0 (transfer)** | `Transferable` 이용 시 zero-copy 이동 가능 |
| ArrayBuffer 복사 (1 MB) | **~1~3 ms** (추정, unverified) | 2025 secondary source. 원본 보존이 필요할 때만 |
| Worker + WASM 스레드 결합 | 정량 수치 unverified | 운영 제약은 확립: cross-origin isolation 헤더 (COOP/COEP) 필요 |

**단위 해석**
- 50 ns는 "초당 2천만 회 이하 호출이면 누적 경계 비용이 CPU 1% 미만"이라는 뜻
- 2,500 ns (2.5 μs) 는 "초당 40만 회 문자열 호출이면 경계 비용이 CPU의 100%" 라는 뜻
- 따라서 **경계를 자주 넘는 코드일수록 WASM이 불리**하고, **경계를 드물게 넘고 안에서 오래 머무는 코드일수록 유리**하다

**출처 주의**: 수치는 [2025 secondary source PDF](https://isg-konf.com/wp-content/uploads/2025/10/DEVELOPMENT_OF_MODERN_SCIENTIFIC_TECHNOLOGIES_IN_THE_ERA_OF_GLOBALIZATION.pdf) 에서 인용. primary V8 벤치마크로 재검증 필요 (unverified).

## 4. SIMD + Threads 지원 현황 (2026-04 기준)

- **WebAssembly SIMD (fixed-width 128)** — 주요 브라우저에서 실사용 가능. MDN 호환성 테이블에 정식 지원으로 등재, SIMD 참조 문서 2026-03-23 최종 업데이트. https://developer.mozilla.org/en-US/docs/WebAssembly/Reference/SIMD , https://developer.mozilla.org/en-US/docs/WebAssembly
- **Threads (SharedArrayBuffer + Atomics)** — 사용 가능하나 **cross-origin isolation** 이 운영 요건. `Cross-Origin-Opener-Policy: same-origin` + `Cross-Origin-Embedder-Policy: require-corp` 헤더 없이는 `SharedArrayBuffer`가 차단됨. 정적 호스팅 시 호스트가 해당 헤더를 허용해야 함. https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer , https://onnxruntime.ai/docs/tutorials/web/deploy.html
- **Safari 특수사항** — 과거 SIMD/threads 지원이 지연된 이력 있음. 2026-04 시점의 정확한 Safari 최신 버전별 지원 테이블은 unverified (MDN 호환성 표가 JS 렌더 기반이라 정적 크롤로는 확인 제한)

react-kit의 결정 기준:
- **SIMD 의존 WASM**: 2+ 계열 (크롬/엣지/파이어폭스) 에서는 안전. Safari 대응은 런타임 feature detection (`WebAssembly.validate` + SIMD opcode probe) 로 가드
- **Threads 의존 WASM**: 데스크탑 Tauri 빌드는 항상 활성화 가능. 웹 빌드는 COOP/COEP 헤더 설정 여부를 `/react-init` 스캐폴딩 단계에서 사용자에게 고지

## 5. 카탈로그 미스 시 판정 — 5가지 휴리스틱

카탈로그 테이블에 정확히 해당하지 않는 요청이 오면 `/react-wasm`이 코드 정적 분석 + 아래 휴리스틱으로 판정한다. 5개 중 **3개 이상** 이 WASM 쪽이면 이식 제안, 아니면 JS 유지 또는 Worker (T1) 권고.

### H1. 데이터 크기

- WASM 쪽: 입출력이 **바이너리 버퍼** (`Uint8Array`, `Float32Array`, `ArrayBuffer`) 이고 KB~MB 단위
- JS 쪽: 입출력이 **문자열, 일반 객체, 작은 배열** (<1 KB 또는 수십 아이템)

### H2. 호출 빈도

- WASM 쪽: **낮은 빈도 (초당 <100) + 무거운 본 작업** (호출당 ms 단위)
- JS 쪽: **높은 빈도 (초당 >1만) + 가벼운 본 작업** — 경계 비용이 본 작업을 지배

### H3. 내부 연산 형태

- WASM 쪽: **반복 루프 중심** (`for`/`while`), 분기 적고, 숫자·바이너리 위주, 행렬·벡터 연산
- JS 쪽: **문자열/객체 조작 중심**, 정규식, `JSON.parse`, DOM 인접

### H4. 외부 리소스 접근

- WASM 쪽: 순수 함수. 외부 접근 없음 (fetch, DOM, timer, localStorage, Tauri API 불필요)
- JS 쪽: **외부 접근 있음** — WASM은 직접 할 수 없어 JS 브리지 거쳐야 함

### H5. 알고리즘 특성

- WASM 쪽: **SIMD / threads 활용 가능** — 픽셀 처리, 해시, 행렬, 정렬, 해제, 컨볼루션
- JS 쪽: **본질적으로 순차적** — 상태 기계, DOM 업데이트, UI 애니메이션, 소규모 트리 순회

### 판정 예시

- "10 MB CSV 파싱" → H1 ✓ (바이너리 가능), H2 ✓ (1회), H3 ✓ (루프), H4 ✓ (순수), H5 ~ (SIMD 일부) = **5/5 WASM**
- "폼 검증 (Zod 스키마)" → H1 ✗, H2 ✗ (매 타이핑), H3 ✗ (문자열), H4 ✗, H5 ✗ = **0/5 JS**
- "이미지 썸네일 생성 (512px resize)" → H1 ✓, H2 ✓, H3 ✓, H4 ✓, H5 ✓ = **5/5 WASM**
- "리스트 정렬 500 아이템" → H1 ✗, H2 ~, H3 ✓, H4 ✓, H5 ✗ = **2/5 JS (V8 sort가 충분)**
- "리스트 정렬 1M 아이템 멀티키" → H1 ✓, H2 ✓ (배치), H3 ✓, H4 ✓, H5 ✓ = **5/5 WASM (또는 DuckDB-Wasm 활용)**

## 6. 흔한 오해 — WASM이 이길 것 같지만 실제로는 지는 케이스

카탈로그에서 가장 가치 있는 섹션. 직관과 측정이 다른 사례를 모았다.

### 오해 1: "React 로직을 WASM으로 빼면 빠르다"

- **틀림.** React는 DOM 인접 작업이고, state 업데이트는 V8 JIT 대상이며, 렌더는 브라우저 페인트 파이프라인을 탄다. WASM으로 빼는 순간 매 렌더 경계를 넘게 되고, 경계 비용이 모든 이득을 먹는다.
- **예외**: 렌더와 완전히 분리된 **순수 계산 훅** (예: `useMemo` 안의 대용량 집계) 은 WASM 후보다. 하지만 이것도 "React 로직" 이 아니다.

### 오해 2: "JSON 파싱/문자열 처리를 WASM으로 빼면 빠르다"

- **틀림.** V8은 Chrome 138에서 `JSON.stringify` 를 2x 이상 개선 (https://v8.dev/blog/json-stringify). JSON parse는 이미 SIMD 경로 사용. 문자열은 JS 네이티브 타입이라 WASM 쪽에서 받으려면 UTF-16→UTF-8 복사가 필수.
- **예외**: **바이너리 포맷** (protobuf, MessagePack, Arrow IPC) 은 다르다. 이건 WASM 후보.

### 오해 3: "큰 데이터면 무조건 WASM이 이긴다"

- **틀림.** 2026년 리서치 합성에 따르면 "많은 WASM 구현이 중규모·대규모 입력에서도 진다"는 결과가 반복 관찰됨. https://unanswered.io/guide/webassembly-vs-javascript-performance (secondary, unverified at primary level)
- **진짜 규칙**: 크기가 아니라 **연산 밀도 (compute per byte)** 가 결정한다. 1 GB 데이터라도 "한 번 훑고 끝" 이면 V8 SIMD + 선형 스캔이 충분히 빠르다. 반대로 10 MB라도 "복잡한 순회 + 재계산" 이면 WASM 이득.

### 오해 4: "Threads를 켜면 자동으로 빨라진다"

- **틀림.** Threads는 **cross-origin isolation** (COOP/COEP) 없이는 `SharedArrayBuffer`가 차단되어 동작하지 않는다. 그리고 threads가 유효하려면 작업이 **worker 친화적** 이어야 한다 — 상호 의존성 없는 분할 가능한 compute. UI 렌더 코드에 threads를 붙여도 이득 없음.

### 오해 5: "Rust가 더 빠른 언어이므로 Rust로 쓴 WASM이 JS보다 빠르다"

- **조건부 틀림.** Rust 언어의 모델 속도와 WASM 타겟 속도는 다르다. Rust는 네이티브 타겟에서 LLVM 풀 최적화를 받지만, wasm32 타겟은 SIMD·스레드 활용도·메모리 모델이 제한된다. Jangda et al. (2019) 의 "Not So Fast" 가 이 점을 최초 체계화 — WASM은 네이티브의 완전한 대체가 아니다. https://www.usenix.org/conference/atc19/presentation/jangda
- **그래도 JS 대비**: 위에 나열한 WASM 권장 카테고리에선 여전히 확실히 빠름. 다만 "네이티브 Rust = WASM Rust" 는 아님.

## 7. react-kit 의사결정 알고리즘

`/react-wasm` 스킬이 사용자 요청을 받았을 때 실행하는 순서:

1. 요청을 **카테고리 키워드 매칭** — "이미지", "압축", "파서", "ML", "SQL" 등
2. 1번 결과가 §1 권장 테이블에 있으면 → **WASM 제안 + Rust crate 추천** (예: `image`, `lz4_flex`, `pulldown-cmark`)
3. 1번 결과가 §2 비권장 테이블에 있으면 → **거부 + JS 유지 권고 + 이유 설명**
4. 매칭 실패 시 → **코드 정적 분석 + §5 휴리스틱 5개** 평가 → 3/5 이상이면 WASM 제안
5. WASM 제안 후 **wasm-pack 빌드 파이프라인 + React 래퍼 + `domain/` Result 타입 바인딩** 생성
6. 생성된 바인딩은 기본적으로 **Web Worker 내부에서 호출** (Comlink 사용) — §2 고빈도 콜백 함정 방지
7. 결과를 `data/datasources/wasm/` 레이어에 배치, `domain/usecases/` 가 이를 호출

## 8. 감사 항목 (`/react-audit` 에서 강제)

- WASM 모듈이 React 렌더 경로에서 `useMemo` 없이 직접 호출되지 않는지 (렌더마다 경계 넘기 금지)
- WASM 함수가 main thread 에서 100 ms 이상 blocking 되지 않는지 (Worker 의무)
- 문자열 인자가 함수당 1 KB 이상 빈번히 전달되지 않는지 (마샬링 함정)
- WASM 모듈 크기가 gzip 기준 500 KB 미만인지 (번들 오버헤드)
- SIMD 의존 WASM에 runtime feature detection 가드가 있는지

## 9. 카이젠 루프

- `/react-research` (레포 전용 dev 스킬) 가 주 1회 Codex로 V8 블로그·MDN·프로덕션 사례를 크롤링해 이 문서를 갱신
- `/react-kaizen` 이 본 문서 기준으로 `/react-wasm` 스킬의 판정 로직을 개선
- 변경 이력은 `docs/react/wasm-catalog.md` 상단 frontmatter `last_updated` 로 추적

## 참고자료 (Primary sources)

1. Jangda, Powers, Berger, Guha — "Not So Fast: Analyzing the Performance of WebAssembly vs Native Code" (USENIX ATC 2019). WASM vs 네이티브 성능 차이의 기초 분석. https://www.usenix.org/conference/atc19/presentation/jangda
2. V8 팀 — "WebAssembly SIMD" feature note. 엔진 레벨 SIMD 지원 및 hand-tracking 벤치마크. https://v8.dev/features/simd
3. V8 팀 — "Speculative optimizations for WebAssembly" (2025-06-24). https://v8.dev/blog/wasm-speculative-optimizations
4. V8 팀 — "Making JSON.stringify more than 2x faster" (2025-08-04). JS JSON 경로 최적화. https://v8.dev/blog/json-stringify
5. V8 팀 — "Maglev — V8's Fastest Optimizing JIT" blog. JS JIT 성능 배경. https://v8.dev/blog/maglev
6. V8 팀 — V8 release 9.0 notes. WASM/JS 최적화 요약. https://v8.dev/blog/v8-release-90
7. Figma Engineering — "Figma is faster" 프로덕션 사례 (이미지/그래픽 경로 WASM 최적화). https://www.figma.com/blog/figma-faster/
8. DuckDB-Wasm 프로젝트 페이지. TPC-H 브라우저 벤치마크. https://duckdb.org/library/duckdb-wasm/
9. ffmpeg.wasm 성능 문서. https://ffmpegwasm.netlify.app/docs/performance/
10. MDN — WebAssembly reference + SIMD reference (2026-03 업데이트). https://developer.mozilla.org/en-US/docs/WebAssembly , https://developer.mozilla.org/en-US/docs/WebAssembly/Reference/SIMD
11. MDN — SharedArrayBuffer, Transferable objects 문서. https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer , https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Transferable_objects
12. Chrome Developers — "Hotpath with Wasm" (Squoosh 사례). https://developer.chrome.com/blog/hotpath-with-wasm?hl=en
13. markdown-wasm 프로젝트 README (JS 콜백 오버헤드 경고 포함). https://github.com/rsms/markdown-wasm
14. pffft.wasm 프로젝트 (SIMD FFT 벤치마크). https://github.com/JorenSix/pffft.wasm , https://0110.be/l/pffft_benchmark
15. lz4-wasm 프로젝트 (벤치마크). https://github.com/PSeitz/lz4-wasm
16. hash-wasm 프로젝트. https://github.com/Daninet/hash-wasm
17. ONNX Runtime Web 배포 가이드 (cross-origin isolation 운영 요건). https://onnxruntime.ai/docs/tutorials/web/deploy.html

**Secondary (수치 unverified — primary 재검증 필요)**
- "Development of Modern Scientific Technologies in the Era of Globalization" (2025-10). JS↔WASM 호출 오버헤드, 문자열 마샬링, ArrayBuffer 복사 수치 인용 출처. https://isg-konf.com/wp-content/uploads/2025/10/DEVELOPMENT_OF_MODERN_SCIENTIFIC_TECHNOLOGIES_IN_THE_ERA_OF_GLOBALIZATION.pdf
- "WebAssembly vs JavaScript performance" 2026 합성 가이드 (mid/large 입력에서 WASM이 지는 사례 인용). https://unanswered.io/guide/webassembly-vs-javascript-performance

---

## 10. 권장 Rust 크레이트 매핑

`/react-wasm` 스킬이 WASM 제안 시 기본 후보로 제시하는 Rust 크레이트. 모두 `wasm32-unknown-unknown` 타겟에서 동작 확인되었거나 공식 WASM 바인딩이 존재함.

| 카테고리 | 1순위 크레이트 | 비고 |
|---|---|---|
| 이미지 처리 (resize, format 변환) | `image` + `fast_image_resize` | SIMD 가속 resize. `image` 는 PNG/JPEG/WebP 디코딩 표준 |
| 이미지 필터/픽셀 조작 | `imageproc` | `image` 위에 쌓는 알고리즘 계층 |
| 비디오 (VP9/AV1 디코딩) | `dav1d-wasm`, `vp9` | 본격 인코딩은 ffmpeg.wasm 그대로 쓰는 편이 현실적 |
| 압축 | `lz4_flex`, `brotli`, `zstd`, `flate2` | 모두 `no_std` 가능, WASM 빌드 안정 |
| 해싱/암호화 bulk | `blake3`, `sha2`, `argon2`, `chacha20poly1305` | SIMD 경로 내장, bulk 데이터에 적합 |
| ML 추론 | `tract` | ONNX 모델 로드/실행 가능. 경량 대안은 `candle-wasm` |
| SQL / 컬럼형 실행 | `sqlparser`, `datafusion` (subset) | 본격 DB는 DuckDB-Wasm 재사용 권장 |
| Markdown 파싱 | `pulldown-cmark` | CommonMark 표준, WASM 빌드 빠름 |
| 바이너리 포맷 (protobuf, MessagePack, CBOR) | `prost`, `rmp-serde`, `ciborium` | serde 기반 공통 |
| 수치 연산 / 선형대수 | `nalgebra`, `ndarray` | SIMD 활성화 시 WASM 이득 |
| FFT / 신호처리 | `rustfft`, `realfft` | `num-complex` 기반, 벡터화 |
| 파서 프레임워크 (커스텀 DSL) | `nom`, `chumsky`, `pest` | parser combinator / PEG |
| 날짜·시간 고성능 계산 | `chrono` (기본) / `jiff` (최신) | 대량 파싱일 때만 WASM 고려 |
| Arrow / Parquet | `arrow`, `parquet` | Arrow IPC 로 JS 와 zero-copy 교환 가능 |

**주의사항**
- 크레이트의 기본 feature flag가 `std` 의존성을 끌어올 수 있음 — `default-features = false` + 필요한 feature만 선택해서 번들 최소화
- `wee_alloc` 은 deprecated — 기본 Rust 할당자가 더 빠른 경우 많음
- `wasm-bindgen` + `serde-wasm-bindgen` 조합이 JS 객체 왕복 시 표준
- 일부 crate (`reqwest`, `tokio`) 는 `wasm32-unknown-unknown` 에서 제한적 — `wasm32-wasi` 가 필요할 수 있음

## 11. 마이그레이션 체크리스트 — JS → Rust WASM

기존 JS 함수를 WASM으로 이식할 때 `/react-wasm` 스킬이 강제하는 단계별 체크리스트.

1. **카테고리 확인** — §1 권장 카테고리 또는 §5 휴리스틱 3/5 이상 통과
2. **함수 경계 식별** — 이식 대상 함수가 순수 함수에 가까운지 확인. 외부 상태/DOM/fetch 참조가 있으면 refactor 먼저
3. **데이터 타입 결정** — 입출력을 Uint8Array / Float32Array / JSON 중 무엇으로 할지. 바이너리 버퍼가 항상 우선
4. **Rust 구현** — `crates/core/` 에 함수 추가. `#[wasm_bindgen]` 어노테이션
5. **wasm-pack 빌드** — `wasm-pack build --target web --release` 또는 `--target bundler`
6. **TypeScript 바인딩 확인** — wasm-pack이 `.d.ts`를 자동 생성. 타입이 정확한지 검증
7. **Worker 배치** — 메인 스레드 호출이 100ms 넘으면 Comlink로 Worker 래핑 강제
8. **Zod 경계 검증** — WASM 결과를 `domain/entities/` 의 Zod 스키마로 parse
9. **Result 래핑** — WASM 함수가 panic할 수 있으면 `neverthrow` Result로 감싸 호출부에 전파
10. **번들 크기 확인** — `wasm-opt -O3` 적용 후 `.wasm` 파일이 gzip 500KB 이하인지 확인. 초과 시 feature flag 정리
11. **Feature detection** — SIMD 의존 코드는 `WebAssembly.validate` + SIMD opcode 프로브로 가드, fallback JS 경로 준비
12. **벤치마크 기록** — `docs/wasm-benchmarks.md` 에 이식 전후 수치 기록 (선택, 하지만 권장)

## 12. 성능 측정 레시피 (선택적)

카탈로그를 믿고 측정 없이 이식하는 게 기본이지만, 경계 사례에서 자체 검증이 필요할 때 사용하는 패턴. `/react-wasm` 이 "이식해도 되는데 애매함" 판정을 내릴 때 이 섹션을 참조.

### 레시피 A — 브라우저 기본

```ts
// 충분히 warm-up 후 측정
const iterations = 10_000
const start = performance.now()
for (let i = 0; i < iterations; i++) {
  subject(inputBuffer)
}
const elapsed = performance.now() - start
console.log(`${elapsed / iterations} ms/call`)
```

주의: `performance.now()` 해상도는 cross-origin isolation 없이는 0.1 ms 로 clamping 됨. 짧은 함수는 충분히 반복해야 함.

### 레시피 B — Vitest bench

```ts
import { bench, describe } from 'vitest'

describe('image resize', () => {
  bench('JS canvas', async () => { /* ... */ })
  bench('WASM image crate', async () => { /* ... */ })
})
```

Vitest bench는 자동으로 warm-up + 샘플링 + 표준편차 제공. 권장.

### 레시피 C — 프로덕션 샘플링

`performance.measure()` + User Timing API로 실제 사용자 환경에서 p50/p95 수집. 라이브러리: `web-vitals`, 자체 구현 가능.

**함정 목록**
- 첫 호출은 항상 느림 (wasm 모듈 컴파일). warm-up 필수
- Chrome DevTools Performance 탭은 WASM 프레임을 보여주지만 per-call 오버헤드는 averaging 됨
- `console.time`은 해상도 부족, 쓰지 말 것
- V8 Maglev/TurboFan 최적화 tier-up은 ~수십 호출 후 발동 → 최소 1000회 이상 돌려야 JS 비교가 공정

## 13. FAQ

**Q1. 내 앱은 내부 툴이라 성능이 덜 중요한데도 WASM이 가치 있나?**
A. 아니오. 이 카탈로그는 "성능이 병목일 때" 의사결정 돕는 도구. 병목 없으면 JS로 끝내라. WASM은 번들 크기, 빌드 파이프라인 복잡도, 디버깅 난이도를 모두 증가시킨다.

**Q2. 모든 걸 Web Worker에 넣으면 WASM 없이도 UI가 덜 끊기지 않나?**
A. 맞다. Worker만으로 해결되는 경우가 많다. WASM은 "Worker에 넣었는데도 CPU 바운드 시간이 허용치를 넘는" 경우에만 진짜 필요하다. §3 티어 T1 → T2 순서를 지켜라.

**Q3. Tauri 데스크탑 앱인데 WASM 말고 네이티브 Rust IPC로 하면 안 되나?**
A. 데스크탑 전용이면 그게 더 빠르다 (경계 비용이 동일하거나 더 낮고 SIMD 제한 없음). 하지만 **웹 배포도 한다** 면 같은 Rust 코드를 WASM + Tauri 양쪽에 공유해 중복 제거하는 편이 유지보수 이득이 크다. `crates/core/` 를 공용으로 두는 이유.

**Q4. React Server Components나 Next.js와 WASM은 어떤가?**
A. RSC는 서버에서 렌더되므로 브라우저 WASM 경로와 무관. Node.js 서버 측 WASM은 V8 동일 엔진이라 같은 카탈로그 적용. Vite + TanStack Router 중심 react-kit은 RSC 미사용.

**Q5. Emscripten으로 컴파일된 C++ WASM 라이브러리를 그냥 쓸 수 있나?**
A. 쓸 수 있다. ffmpeg.wasm, sql.js, DuckDB-Wasm이 그 예. Rust 대신 C++ 생태계 라이브러리를 가져올 때 선택. 단, Emscripten 런타임 오버헤드와 번들 크기 증가를 감안해야 함.

**Q6. WASM 모듈이 lazy-load 되면 첫 사용이 느린데?**
A. 맞다. 두 가지 완화책: (a) `wasm-pack build --target web` 후 `<link rel="preload">` 로 아이들 시간에 선로드, (b) Vite dynamic import + suspense로 UX 상 로딩 상태 노출. Tauri 빌드는 로컬 파일시스템에서 로드라 사실상 즉시.

**Q7. WASM이 보안상 더 안전한가?**
A. WebAssembly는 샌드박스 메모리 모델 덕에 **메모리 안전성**이 강하다 (out-of-bounds read/write 격리). 그러나 **비즈니스 로직 보안** (예: 라이선스 검증 코드) 은 WASM도 디컴파일 가능해 크게 강하지 않다. 클라이언트 코드는 공개되었다고 가정하라.

## 14. 용어집 (Glossary)

- **WASM / WebAssembly** — 브라우저와 기타 런타임에서 실행되는 포터블 바이너리 포맷. 32-bit 선형 메모리 모델
- **wasm-pack** — Rust 크레이트를 npm 패키지로 빌드하는 공식 도구. `wasm-bindgen` 을 래핑
- **wasm-bindgen** — Rust ↔ JS 타입 경계 자동 생성 라이브러리
- **wasm-opt** — Binaryen 프로젝트의 WASM 최적화 도구. 빌드 후 크기·속도 개선
- **SIMD** — Single Instruction Multiple Data. 한 명령으로 벡터 요소 여러 개 동시 처리. WASM v1.0 이후 `v128` fixed-width 지원
- **Threads** — `SharedArrayBuffer` + `Atomics` 기반 WASM 스레드. COOP/COEP 헤더 필수
- **COOP / COEP** — Cross-Origin Opener Policy / Embedder Policy. SharedArrayBuffer 활성화 요건
- **Boundary cost** — JS 와 WASM 사이를 오가는 함수 호출의 고정 비용. 작은 함수일수록 상대적 비중 큼
- **Marshaling** — JS 값과 WASM 선형 메모리 사이의 변환 (특히 문자열 UTF-16 ↔ UTF-8)
- **Transferable** — `postMessage` / Worker 통신에서 소유권 이전으로 zero-copy 전송하는 객체 (ArrayBuffer 등)
- **JIT tier-up** — V8이 함수를 인터프리터 → Sparkplug → Maglev → TurboFan 순으로 승격 최적화하는 과정
- **Hot path** — 앱 실행 시간 대부분을 차지하는 코드 경로. 최적화 대상 1순위
- **Cold code** — 드물게 실행되는 코드. WASM 이식해도 이득 없음

## 15. 코드 예시 — 대표 패턴

`/react-wasm` 스킬이 생성하는 코드의 원형. 스킬이 없어도 수동으로 참고 가능.

### 예시 A — Rust 함수 (`crates/core/src/image.rs`)

```rust
use wasm_bindgen::prelude::*;
use image::{ImageBuffer, Rgba};

#[wasm_bindgen]
pub fn resize_thumbnail(input: &[u8], width: u32, height: u32) -> Result<Vec<u8>, JsError> {
    let img = image::load_from_memory(input)
        .map_err(|e| JsError::new(&format!("decode failed: {e}")))?;
    let resized = img.thumbnail(width, height);
    let mut out = Vec::new();
    resized.write_to(&mut std::io::Cursor::new(&mut out), image::ImageFormat::Png)
        .map_err(|e| JsError::new(&format!("encode failed: {e}")))?;
    Ok(out)
}
```

### 예시 B — Worker 래퍼 (`src/data/datasources/wasm/image-worker.ts`)

```ts
import init, { resize_thumbnail } from '@/wasm/core'
import { expose } from 'comlink'

let ready: Promise<void> | null = null
function ensureInit() {
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

### 예시 C — UseCase 래핑 (`src/domain/usecases/resize-image.ts`)

```ts
import { ok, err, Result } from 'neverthrow'
import type { ImageResizeFailure } from '@/domain/failures'
import { wrap } from 'comlink'
import type { imageWorkerApi } from '@/data/datasources/wasm/image-worker'

const worker = new Worker(
  new URL('@/data/datasources/wasm/image-worker.ts', import.meta.url),
  { type: 'module' },
)
const api = wrap<typeof imageWorkerApi>(worker)

export async function resizeImage(
  input: Uint8Array,
  size: { width: number; height: number },
): Promise<Result<Uint8Array, ImageResizeFailure>> {
  try {
    const output = await api.resizeThumbnail(input, size.width, size.height)
    return ok(output)
  } catch (e) {
    return err({ kind: 'image/resize-failed', cause: String(e) })
  }
}
```

### 예시 D — React 훅 (`src/presentation/features/gallery/hooks/use-thumbnail.ts`)

```ts
import { useMutation } from '@tanstack/react-query'
import { resizeImage } from '@/domain/usecases/resize-image'

export function useGenerateThumbnail() {
  return useMutation({
    mutationFn: async (args: { file: File; size: { width: number; height: number } }) => {
      const input = new Uint8Array(await args.file.arrayBuffer())
      const result = await resizeImage(input, args.size)
      if (result.isErr()) throw result.error
      return result.value
    },
  })
}
```

### 안티패턴 — 피해야 할 코드

```ts
// ❌ 렌더마다 WASM 호출. useMemo 누락으로 경계 비용 누적
function ImageCard({ data }: { data: Uint8Array }) {
  const resized = resize_thumbnail(data, 256, 256)  // 매 렌더 호출
  return <img src={toObjectUrl(resized)} />
}

// ❌ 문자열 인자를 빈번히 전달. 마샬링 함정
for (const line of largeTextFile.split('\n')) {
  wasmValidator(line)  // 수십만 번 문자열 복사
}

// ❌ 작은 숫자 연산 루프를 WASM 경계 안으로 넣지 않고 밖에서 반복
for (let i = 0; i < 1_000_000; i++) {
  result += wasmAdd(a[i], b[i])  // 백만 번 경계 넘기 = 50~100 ms 고정 비용
}
```

## 16. 실제 프로덕션 케이스 스터디

카탈로그를 뒷받침하는 실제 사례. 각 사례의 공통점은 "경계를 드물게 넘고 안에서 오래 머문다".

### Case 1 — Figma (2D 벡터 렌더링)

- **문제**: 대용량 Figma 파일 로딩에서 JS 기반 파서/렌더러 성능 한계
- **해결**: C++ 핵심 로직을 WebAssembly 로 이식. 초기 로드 29s → 8s (약 3.6x)
- **교훈**: 단일 진입점 (파일 로드) 으로 들어가서 내부에서 오래 머무는 작업은 WASM 최적 후보
- **출처**: https://www.figma.com/blog/figma-faster/

### Case 2 — Squoosh (이미지 코덱 비교 도구)

- **문제**: 브라우저에서 MozJPEG, WebP, AVIF 같은 코덱을 실제로 돌려봐야 하는데 JS 구현이 현실적으로 없음
- **해결**: 각 코덱의 C 구현을 WASM으로 컴파일. 코덱마다 `.wasm` 파일 분리해서 lazy load
- **교훈**: "JS 대안이 없는" 영역에서는 WASM이 선택의 문제가 아니라 유일한 길
- **출처**: https://developer.chrome.com/blog/hotpath-with-wasm?hl=en

### Case 3 — DuckDB-Wasm (브라우저 SQL 엔진)

- **문제**: 브라우저에서 대용량 CSV/Parquet에 대한 분석 SQL 실행
- **해결**: DuckDB 컬럼 엔진을 WASM 으로 빌드. Worker 에서 실행, Arrow IPC로 zero-copy 교환
- **교훈**: 전문화된 실행 엔진을 통째로 WASM으로 가져오는 것이 "JS로 재구현" 보다 훨씬 현실적
- **출처**: https://duckdb.org/library/duckdb-wasm/

### Case 4 — MediaPipe Hand Tracking (온디바이스 ML)

- **문제**: 실시간 손 추적을 JS로는 frame rate 확보 불가
- **해결**: XNNPACK + WASM SIMD. 14~15 FPS → 38~40 FPS (약 2.6x)
- **교훈**: ML 추론은 텐서 연산이라 SIMD 효과가 강하게 나오는 전형적 WASM 승리 카테고리
- **출처**: https://v8.dev/features/simd

### Case 5 — Photopea (Photoshop 웹 클론)

- **문제**: PSD 파일 파싱, 레이어 블렌딩, 필터 적용 모두 JS로는 성능 한계
- **해결**: C++ 이미지 처리 코어를 WASM 으로 컴파일. 복잡한 필터/블렌딩은 대부분 WASM 내부에서 수행
- **교훈**: 이미지 편집기처럼 "사용자 인터랙션 → 대량 픽셀 처리 → 결과 표시" 사이클은 WASM 코어 + JS UI 조합의 이상적 분할
- **출처**: https://www.photopea.com/learn/about

## 17. Anti-example 케이스 — WASM 선택이 손해였던 사례

### Anti-case 1 — 작은 유틸 함수 이식

- **문제**: 팀이 "성능을 위해" 수학 유틸리티 (sin/cos/sqrt 래퍼) 를 Rust → WASM 이식
- **결과**: JS `Math.*` 대비 20배 느려짐. V8 TurboFan이 `Math.*` 를 네이티브 호출로 인라인하는데, WASM 경로는 매 호출 경계 비용 발생
- **교훈**: V8이 이미 네이티브 최적화한 경로는 WASM으로 이식하면 항상 진다. `Math.*`, `Array.sort`, `String.prototype.*`, `JSON.*` 등이 해당

### Anti-case 2 — React state reducer 이식

- **문제**: "성능 병목이 state 업데이트" 라는 오진으로 reducer 로직을 WASM으로 이식
- **결과**: 각 dispatch 마다 경계 비용. 실제 병목은 컴포넌트 리렌더 범위 문제였음. 리렌더 최적화만 하면 해결됐을 일
- **교훈**: 프로파일 없이 "어디가 느린지" 추측하면 WASM은 오히려 상황을 악화시킨다. React 쪽 병목은 99% React Profiler가 답을 준다

### Anti-case 3 — JSON 파싱 가속 시도

- **문제**: 대용량 JSON API 응답 파싱이 느린 것 같아서 Rust `serde_json` → WASM 경로 도입
- **결과**: `JSON.parse` 대비 오히려 느림. Chrome 138 이후 V8 JSON 경로가 2x+ 개선된 영향. 바이너리 경로 (MessagePack) 로 바꾸는 게 진짜 답이었음
- **교훈**: 문자열 기반 포맷 (JSON, XML, YAML) 의 파싱은 JS가 유리. 진짜 빠르게 하려면 포맷 자체를 바이너리 (Arrow, Protobuf, MessagePack) 로 바꿔야 함

### Anti-case 4 — 암호화 소규모 호출

- **문제**: 사용자 비밀번호 해싱 (SHA-256 단발) 을 WASM으로 이식
- **결과**: `crypto.subtle.digest('SHA-256', ...)` 가 네이티브 호출이라 WASM 대비 훨씬 빠름. 거기다 Web Crypto는 Promise 기반이라 블로킹도 없음
- **교훈**: Web Crypto API 커버리지 내 작업은 그쪽을 먼저 써라. WASM은 Web Crypto가 못 하는 알고리즘 (blake3, argon2, chacha20) 에서만 의미

### Anti-case 5 — 고빈도 이벤트 핸들러

- **문제**: 스크롤 이벤트에서 WASM 함수를 호출해 뷰포트 계산
- **결과**: 스크롤 초당 60회 × 내부 루프가 작음 → 경계 비용이 본 작업을 압도. 게다가 UI 스레드 블로킹
- **교훈**: 고빈도 이벤트는 JS + `requestAnimationFrame` 으로 배치. WASM은 무거운 개별 작업에만

## 18. 변경 이력

- **2026-04-10** — 초판 작성. Codex 리서치 (task-mnshueuy-tz63ae) 기반. §1 9개 카테고리, §2 10개 카테고리, §3 boundary cost, §4 SIMD/threads 상태, §5 휴리스틱 5개, §6 오해 5개, §10 Rust 크레이트 매핑, §11 마이그레이션 체크리스트, §15 코드 예시, §16 프로덕션 사례 스터디 5건, §17 anti-example 5건.

---

**문서 상태**: draft. react-kit 카이젠 루프 (`/react-kaizen`, `/react-research`) 로 주기적 갱신 대상. 특히 §3 boundary cost 의 secondary source 수치는 primary 재검증 필요.
