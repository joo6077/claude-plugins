---
name: react-tauri
description: >
  Tauri 2 Rust command를 정의하고 TS invoke 래퍼 + capabilities 등록까지 3-tier로 자동 생성한다.
  "Tauri 커맨드", "tauri invoke", "네이티브 연동", "데스크탑 API", "tauri command", "tauri bridge",
  "파일시스템 접근", "react-tauri", "네이티브 기능 추가" 같은 요청 시 트리거.
  CPU 바운드 순수 계산이나 웹에서도 동작해야 하는 고성능 로직은 트리거하지 않는다 — /react-wasm 사용.
argument-hint: "<command_name> <feature> [--capabilities=<perm,...>] [--web-fallback=throw|noop|stub|prompt-user]"
user-invocable: true
---

# Gotchas

1. **isTauri() gating 필수** — `infrastructure/tauri/` 의 모든 함수는 첫 줄에 `if (!isTauri())` 가드를 선언해야 한다. 브라우저 환경에서 `window.__TAURI_INTERNALS__` 가 없으면 `invoke`가 throw한다. 가드 없이 브라우저에서 실행하면 crash.
2. **레이어 경계 엄수** — `@tauri-apps/api/*` import는 오직 `src/infrastructure/tauri/` 에서만 허용. `data/`, `domain/`, `presentation/` 에서 직접 import하면 레이어 경계 위반. `/react-audit` G6이 이 패턴을 grep으로 강제 검출한다.
3. **capabilities 등록 누락** — Rust command를 추가하고 Builder에 등록해도 `src-tauri/capabilities/*.json` 에 권한이 없으면 런타임에 "not allowed" 에러 발생. 이 스킬은 capabilities 파일을 자동 수정한다.
4. **`invoke<unknown>` + Zod parse 강제** — `invoke<T>` 제네릭의 `T`는 컴파일 시점에만 유추되고 런타임 타입은 검증되지 않는다. 반드시 `invoke<unknown>('...')` 후 Zod `safeParse`로 검증한다.
5. **빌드 타임 분기 금지** — `import.meta.env.TAURI` 같은 빌드 타임 define 플래그를 런타임 분기 조건으로 사용하지 않는다. 같은 `dist/`를 웹과 Tauri WebView 양쪽에서 로드하므로 `isTauri()` 런타임 감지가 단일 진실 공급원.
6. **권한 식별자 최소화** — `fs:default` 같은 광범위 권한 대신 `fs:allow-read-text-file` 처럼 구체적 권한만 부여한다. 광범위 권한은 `/react-audit`의 Security 카테고리에서 경고를 발행한다.
7. **이벤트 리스너 cleanup** — `listen('event-name', handler)` 사용 시 반드시 `useEffect` cleanup에서 반환된 unlisten 함수를 호출한다. cleanup 없으면 컴포넌트 재마운트마다 리스너가 누적된다.
8. **domain/presentation은 Tauri를 모른다** — `domain/usecases/`는 `infrastructure/tauri/`의 함수를 얇게 재노출(re-export)하는 수준으로만 사용한다. domain 레이어가 Tauri 특정 타입을 import하면 레이어 위반.
9. **Rust command `Result<T, String>` 관례** — Tauri 2에서 Rust command 반환값이 `Err(String)`이면 JS 측에서 throw로 전달된다. 복잡한 에러 구조체보다 `String`으로 단순화하고 TS 쪽에서 Failure kind로 재분류한다.
10. **stateless command가 기본** — 복수 command가 상태를 공유해야 하면 `app.manage(...)` + `State<'_, T>` 인자 패턴을 사용한다. 이 스킬 기본 생성물은 stateless command이고, stateful은 사용자 명시 요청 시에만 추가한다.
11. **src-tauri/ 사전 확인** — G1 `/react-init --with-tauri`로 초기화된 프로젝트에만 적용. `src-tauri/` 디렉토리가 없으면 에러로 안내하고 `/react-init --with-tauri`를 먼저 실행하도록 유도한다.
12. **mobile 대응 범위 외** — Tauri 2 iOS/Android는 별도 permission 스키마가 필요하다. 이 스킬은 desktop 타겟만 다루고, mobile 지원은 별도 확장 스킬에서 처리한다.
13. **IPC Raw Payloads 로 직렬화 오버헤드 제거** — v2 는 JSON 직렬화 외에 Raw Request/Response 를 지원한다. 대용량 바이너리 데이터(이미지, 파일 청크 등) 전송 시 Custom Protocol 기반 IPC 로 JSON 오버헤드를 제거할 수 있다. 일반 command 는 JSON 이 충분하므로, Raw Payload 는 성능 병목이 측정된 경우에만 적용한다.
14. **Stronghold 보안 저장소 기본값** — 민감 데이터(토큰, API 키, 자격 증명) 저장은 `@tauri-apps/plugin-stronghold` 를 기본으로 사용한다. `tauri add stronghold` 로 설치하고 JS guest binding (`@tauri-apps/plugin-stronghold`) + Argon2 helper 를 활용한다. `localStorage` 에 민감 데이터 저장 금지.
15. **Updater 플러그인 — 서명 아티팩트 자동 생성** — v2 updater plugin 은 `bundle.createUpdaterArtifacts` 설정 시 플랫폼별 서명 번들(AppImage/macOS archive/MSI/NSIS) 을 자동 생성한다. 배포 파이프라인에 서명/업데이트 아티팩트 단계를 포함시킨다.
16. **Deep Link + Single Instance 조합 필수** — deep-link plugin 의 `onOpenUrl` 은 Windows/Linux 에서 single-instance plugin 없이 동작이 제한된다. OAuth callback 등 deep-link 활용 시 반드시 `single-instance` + `deep-link` 두 플러그인을 함께 설정한다. macOS/Android/iOS 는 런타임 동적 등록 불가 — config 기반 등록이 필요하다.

# Process

## 1. 프로젝트 환경 감지

`references/project-detection.md` 절차를 실행한다. `src-tauri/`, `@tauri-apps/api` 패키지, `src-tauri/capabilities/` 디렉토리 존재 여부를 확인한다. `src-tauri/` 가 없으면 안내 후 중단:

```text
src-tauri/ 디렉토리를 찾을 수 없습니다.
/react-init --with-tauri 를 먼저 실행해 Tauri 데스크탑 백엔드를 세팅하세요.
```

## 2. 입력 수집

- `command_name` (필수): snake_case (예: `read_config_file`, `open_save_dialog`, `get_system_info`)
- `feature` (필수): 어느 feature에 속하는지 (예: `config`, `file-manager`, `system`)
- `--capabilities` (선택): 필요한 Tauri permission 목록 (예: `fs:allow-read-text-file`, `dialog:allow-save`)
  - 생략 시 command_name 키워드로 자동 추론
- `--web-fallback` (기본 `throw`): 브라우저 런타임에서의 fallback 전략
  - `throw`: `Failure`로 반환. 호출부가 UI에 "데스크탑 앱에서만 지원" 표시
  - `noop`: 조용히 성공 (`ok(undefined)`). optional feature
  - `stub`: 미리 준비된 stub 값 반환. 개발 중 UI만 확인할 때
  - `prompt-user`: presentation 쪽에서 "데스크탑 앱 설치" 안내 처리 (Failure kind로 신호 전달)

## 3. 중복 확인

아래 경로가 이미 존재하는지 확인한다:

- `src-tauri/src/commands/<feature>.rs`
- `src/infrastructure/tauri/<feature>.ts`
- `src/domain/usecases/<feature>-usecases.ts` (기존 파일이면 append 모드)

존재하면 `--force` 없이 거부하고 사용자에게 알린다. usecases 파일은 기존 파일에 함수를 추가하는 append 모드로 처리한다.

## 4. 3-tier 흐름 생성 (Rust → capabilities → TS)

### 4-1. Rust command 정의

`src-tauri/src/commands/<feature>.rs`:

```rust
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
pub struct <ResponseType> {
    // 응답 필드
}

#[tauri::command]
pub fn <command_name>(/* 파라미터 */) -> Result<<ResponseType>, String> {
    // 연산 로직
    // 에러는 String으로 반환 — TS 쪽에서 Failure kind로 재분류
    do_work()
        .map_err(|e| format!("오류 설명: {e}"))
}
```

**규칙:**
- 반환 타입은 `Result<T, String>` 관례 사용
- `Serialize`, `Deserialize` derive 필수 — `serde_json` 직렬화 경로
- 에러 메시지는 `format!("context: {e}")` 패턴으로 맥락 포함

### 4-2. Builder 등록

`src-tauri/src/lib.rs` 의 `invoke_handler` 에 추가:

```rust
mod commands;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            commands::<feature>::<command_name>,
            // 기존 command 유지
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

기존 `invoke_handler` 목록에 append한다. 기존 command를 덮어쓰지 않는다.

### 4-3. capabilities 선언

`src-tauri/capabilities/default.json` 에 필요한 권한을 추가:

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "description": "Default app capability",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "<permission-identifier>",
    {
      "identifier": "<scoped-permission>",
      "allow": [{ "path": "$APPCONFIG/**" }]
    }
  ]
}
```

**권한 추론 규칙** (`command_name` 키워드 기반):

| 키워드 | 추론 권한 |
|--------|----------|
| read, load, open (파일) | `fs:allow-read-text-file` |
| write, save, create (파일) | `fs:allow-write-text-file` |
| dialog, 다이얼로그 | `dialog:allow-open`, `dialog:allow-save` |
| shell, 실행 | `shell:allow-execute` |
| clipboard | `clipboard-manager:allow-read-text`, `clipboard-manager:allow-write-text` |
| notification | `notification:allow-request-permission`, `notification:allow-send-notification` |

`--capabilities` 플래그가 있으면 사용자 지정 권한을 그대로 사용한다.

### 4-4. TS invoke 래퍼

`src/infrastructure/tauri/<feature>.ts`:

```ts
import { invoke, isTauri } from '@tauri-apps/api/core'
import { z } from 'zod'
import { ok, err, type Result } from 'neverthrow'

// 응답 스키마 — Rust 구조체와 1:1 대응
const <Response>Schema = z.object({
  // Rust 필드는 serde가 camelCase로 자동 변환하지 않음 — 명시적 매핑 또는 rename 필요
})
export type <Response> = z.infer<typeof <Response>Schema>

export type <Feature>Failure =
  | { kind: '<feature>/not-in-tauri' }
  | { kind: '<feature>/command-failed'; cause: string }
  | { kind: '<feature>/invalid-response'; issues: string[] }

export async function <commandCamel>(
  /* 파라미터 */
): Promise<Result<<Response>, <Feature>Failure>> {
  if (!isTauri()) {
    // --web-fallback 전략에 따라 분기
    // throw: return err({ kind: '<feature>/not-in-tauri' })
    // noop:  return ok(undefined as unknown as <Response>)
    // stub:  return ok(STUB_VALUE)
    return err({ kind: '<feature>/not-in-tauri' })
  }

  try {
    const raw = await invoke<unknown>('<command_name>', { /* 파라미터 매핑 */ })
    const parsed = <Response>Schema.safeParse(raw)
    if (!parsed.success) {
      return err({
        kind: '<feature>/invalid-response',
        issues: parsed.error.issues.map((i) => i.message),
      })
    }
    return ok(parsed.data)
  } catch (e) {
    return err({
      kind: '<feature>/command-failed',
      cause: e instanceof Error ? e.message : String(e),
    })
  }
}
```

**핵심 규칙:**
- `isTauri()` 가드는 함수 첫 줄 — 브라우저 환경에서 invoke 호출 방지
- `invoke<unknown>` + Zod safeParse — 런타임 타입 안전 보장
- 3가지 실패 케이스를 모두 discriminated union으로 분류
- `@tauri-apps/api/*` import는 이 파일에서만

**Tauri 이벤트 리스너가 필요한 경우** (`command_name`이 이벤트 subscribe 패턴):

```ts
import { listen, type UnlistenFn } from '@tauri-apps/api/event'

export async function subscribe<EventName>(
  handler: (payload: <EventPayload>) => void,
): Promise<Result<UnlistenFn, <Feature>Failure>> {
  if (!isTauri()) {
    return err({ kind: '<feature>/not-in-tauri' })
  }
  try {
    const unlisten = await listen<unknown>('<event-name>', (event) => {
      const parsed = <EventPayload>Schema.safeParse(event.payload)
      if (parsed.success) handler(parsed.data)
    })
    return ok(unlisten)
  } catch (e) {
    return err({ kind: '<feature>/command-failed', cause: String(e) })
  }
}
```

React `useEffect` 에서 사용:

```ts
useEffect(() => {
  let unlisten: UnlistenFn | undefined
  subscribe<EventName>((payload) => { /* 처리 */ })
    .then((result) => {
      if (result.isOk()) unlisten = result.value
    })
  return () => { unlisten?.() }
}, [])
```

### 4-5. Domain UseCase 재노출

`src/domain/usecases/<feature>-usecases.ts` (기존 파일에 append):

```ts
import type { Result } from 'neverthrow'
import type { <Response>, <Feature>Failure } from '@/infrastructure/tauri/<feature>'
import { <commandCamel> } from '@/infrastructure/tauri/<feature>'

export type { <Feature>Failure }

export function <useCaseName>(
  /* 파라미터 */
): Promise<Result<<Response>, <Feature>Failure>> {
  return <commandCamel>(/* 파라미터 */)
}
```

UseCase는 infrastructure/tauri 함수를 얇게 재노출하는 수준. domain 레이어가 Tauri 특정 타입을 직접 import하지 않는다.

### 4-6. Presentation 훅 (선택)

`src/presentation/features/<feature>/hooks/use-<action>.ts`:

```ts
import { useMutation } from '@tanstack/react-query'
import { <useCaseName> } from '@/domain/usecases/<feature>-usecases'

export function use<Action>() {
  return useMutation({
    mutationFn: (params: { /* 파라미터 타입 */ }) =>
      <useCaseName>(/* params */),
  })
}
```

## 5. 생성 완료 검증

생성 후 아래 항목을 확인한다:

```bash
# Rust 컴파일 확인 (src-tauri 존재 시)
cargo check --manifest-path src-tauri/Cargo.toml

# TS 타입 확인
pnpm tsc --noEmit
```

타입 오류나 Rust 컴파일 에러가 있으면 자동 수정 후 재검증.

## 6. 완료 후 안내

생성 파일 목록 출력. 다음 단계:

- TanStack Query mutation 훅 연결: `/react-query`
- 화면에 Tauri 기능 추가: `/react-screen`
- 감사 (capabilities 누락, isTauri 가드 누락, @tauri-apps 레이어 위반): `/react-audit`

# References

- `references/project-detection.md` — 프로젝트 환경 감지
- `references/clean-arch-layout.md` — infrastructure/tauri/ 경계 규칙, 금지 import 방향
- `docs/react/kit-design/g3-performance.md` §2 — 이 스킬 상세 설계 (3-tier 흐름, Gotchas, fallback 전략)
- Tauri 2 Calling Rust from Frontend: https://v2.tauri.app/develop/calling-rust/
- Tauri 2 Capabilities: https://v2.tauri.app/security/capabilities/
- Tauri 2 isTauri API: https://v2.tauri.app/reference/javascript/api/namespacecore/
