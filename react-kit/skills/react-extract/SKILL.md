---
name: react-extract
description: >
  feature 내부에 사유화되거나 중복된 컴포넌트를 감지하여 presentation/shared/components/로 추출한다.
  import 경로를 absolute(@/)로 자동 업데이트하고 원본을 삭제한다.
  "위젯 추출", "공통으로 빼줘", "extract component", "재사용으로 빼기",
  "shared 이동", "컴포넌트 추출", "중복 위젯 정리" 같은 요청 시 트리거.
  widget-inspector-react 에이전트 리포트 승인 후에도 자동 트리거.
  단순 새 컴포넌트 생성은 /react-widget 사용.
argument-hint: "<source_path> [<destination>] [--dry-run]"
user-invocable: true
---

# Gotchas

1. **grep/regex import 치환 금지** — 단순 문자열 치환은 함수 내부 문자열이나 주석에도 패턴이 있으면 오염된다. import 경로 변환은 반드시 TypeScript AST 수준(ts-morph 또는 TypeScript Compiler API)에서 import 노드를 식별하여 처리한다.
2. **`export default` 컴포넌트 추출 금지** — `export default function ...`은 import 시 임의 이름을 붙일 수 있어 일관성이 깨진다. 먼저 named export로 리팩터한 후 추출한다. 원본을 변경하는 것이므로 사용자에게 먼저 알린다.
3. **상대 경로 → absolute 통일** — 기존 코드의 `import { X } from './x'`를 이동 후 경로 재계산하지 않는다. 항상 `@/presentation/shared/components/...` 형태로 업데이트한다.
4. **re-export 파일 남기기 금지** — 원본 위치에 `export { X } from '@/...'` 같은 re-export를 남기지 않는다. 간접 경로가 누적되면 import 그래프가 복잡해진다. 원본 파일 삭제 후 모든 참조를 새 경로로 직접 업데이트한다.
5. **feature 타입을 shared 컴포넌트 Props에 노출 금지** — 특정 feature의 domain 타입(`AuthUser`, `PostDetail`)을 import하는 컴포넌트는 "잘못 추출됨" 신호다. Props를 generic화하거나 콜백으로 느슨하게 분리 후 추출한다.
6. **이동 후 타입 에러 → 즉시 전체 롤백** — `tsc --noEmit` 실패 시 부분 적용 상태를 방치하지 않는다. 생성한 파일과 수정한 import를 모두 원래 상태로 되돌린다.
7. **동일 이름 충돌** — 다른 feature에도 같은 이름의 컴포넌트가 있으면 shared 이동 시 충돌한다. 더 구체적인 이름을 사용자에게 제안한다 (예: `LogoBanner` → `AuthLogoBanner`).
8. **테스트/스토리 파일 동반 이동** — 추출 대상에 `.test.tsx`, `.spec.tsx`, `.stories.tsx`가 있으면 함께 이동하고 import 경로도 업데이트한다.
9. **순환 참조 감지** — 이동으로 새로운 순환 의존이 생기는지 확인한다. 순환이 감지되면 경고 후 이동을 중단한다.
10. **widget-inspector 리포트 신뢰하되 사용자 승인 필수** — 에이전트 판단이 100% 정확하지 않을 수 있다. 추출 전 반드시 사용자가 계획을 확인하고 승인한다.

# Process

## 1. 프로젝트 환경 감지

`references/project-detection.md` 절차를 실행한다:
- `tsconfig.json`의 `paths` 설정에서 `@/` alias 확인
- `src/presentation/shared/components/` 디렉토리 존재 여부
- `src/presentation/shared/components/ui/` (shadcn 원본 디렉토리)

## 2. 추출 대상 확인

**widget-inspector-react 리포트가 있는 경우:**
- 리포트의 감지 결과를 사용자에게 보여준다
- 사용자가 선택한 항목을 추출 대상으로 확정한다
- `--dry-run` 모드에서는 실제 파일 이동 없이 변경 내역만 보고한다

**직접 지정한 경우:**
- `source_path` 파일을 읽는다
- 컴포넌트가 다음 조건에 해당하는지 확인한다:
  - feature 특화 domain 타입을 import하지 않는가 (shared 가능 여부)
  - `export default`인가 (먼저 named export로 변환 필요)
  - 다른 파일에서도 동일/유사 컴포넌트가 있는가

## 3. 추출 계획 제시

사용자에게 추출 계획을 보여주고 확인받는다:

```text
추출 계획:

1. LogoBanner (src/presentation/features/auth/components/logo-banner.tsx)
   → src/presentation/shared/components/logo-banner.tsx
   변경될 import: 3개 파일
     - src/presentation/features/auth/screens/login-screen.tsx
     - src/presentation/features/auth/screens/register-screen.tsx
     - src/presentation/features/onboarding/screens/welcome-screen.tsx

2. (--dry-run: 실제 이동은 수행하지 않음)

진행할까요? [y/N]
```

## 4. 대상 경로 결정

- `destination` 인자가 있으면 해당 경로 사용
- 없으면 기본: `src/presentation/shared/components/<kebab-name>.tsx`
- shadcn 컴포넌트 확장인 경우: `src/presentation/shared/components/ui/<kebab-name>.tsx`

**이름 충돌 감지:**
```bash
# 대상 경로에 이미 같은 이름 파일이 있으면 충돌 경고
```

## 5. 추출 전 Props 정리

이동 전에 컴포넌트를 shared에 적합하게 정리한다:

**Props 타입 export 확인:**
```tsx
// 없으면 추가
export type LogoBannerProps = {
  size?: 'sm' | 'md' | 'lg'
  className?: string
}
```

**named export 확인:**
```tsx
// export default → named export 변환 (사용자 승인 후)
// Before
export default function LogoBanner(props: LogoBannerProps) { ... }

// After
export function LogoBanner(props: LogoBannerProps) { ... }
```

**feature 타입 제거:**
```tsx
// Before (추출 불가)
import type { AuthUser } from '@/domain/entities/auth-user'
export function UserCard({ user }: { user: AuthUser }) { ... }

// After (generic화 후 추출 가능)
export type UserCardProps = {
  name: string
  email: string
  avatarUrl?: string
}
export function UserCard({ name, email, avatarUrl }: UserCardProps) { ... }
```

## 6. Import 참조 스캔

전체 프로젝트에서 대상 컴포넌트를 import하는 파일을 수집한다:

```bash
# AST 기반으로 import 노드 탐색 (grep은 보조 수단)
pnpm tsc --noEmit --listFiles 2>/dev/null | head -20
```

Grep으로 후보를 빠르게 찾고, AST로 정확히 검증한다:
- `import { LogoBanner }` 패턴
- `import type { LogoBannerProps }` 패턴
- 동적 import: `import('./logo-banner')` 패턴

## 7. 파일 이동

1. `source_path`의 컴포넌트 내용을 `destination`에 복사한다
2. Props 타입 export, named export 정리를 반영한다
3. 컴포넌트 내부의 상대 경로 import가 있으면 absolute로 변환한다

## 8. Import 경로 일괄 업데이트

참조하는 모든 파일의 import 구문을 새 경로로 업데이트한다:

```tsx
// Before
import { LogoBanner } from './logo-banner'
import { LogoBanner } from '../components/logo-banner'
import type { LogoBannerProps } from '@/presentation/features/auth/components/logo-banner'

// After (모든 케이스)
import { LogoBanner } from '@/presentation/shared/components/logo-banner'
import type { LogoBannerProps } from '@/presentation/shared/components/logo-banner'
```

**규칙:**
- 항상 absolute import(`@/...`)로 업데이트. 상대 경로 유지 금지
- `type`만 import하는 경우 `import type`으로 분리 (strict TS `verbatimModuleSyntax` 정책)

## 9. 원본 파일 처리

- 원본 `source_path` 파일 삭제
- 원본 파일에서 해당 컴포넌트를 import하던 구문 제거 후 불필요해진 import 정리
- 원본 파일에 다른 컴포넌트가 없으면 파일 전체 삭제

## 10. 검증

```bash
pnpm tsc --noEmit
pnpm eslint src/presentation --max-warnings=0
```

실패 시 즉시 전체 롤백:
- 생성한 `destination` 파일 삭제
- 수정한 모든 import를 원래 상태로 복원
- 삭제한 `source_path` 파일 복원
- 에러 내용과 함께 롤백 완료를 사용자에게 보고

## 11. 결과 리포트

```text
추출 완료:

이동: src/presentation/features/auth/components/logo-banner.tsx
  → src/presentation/shared/components/logo-banner.tsx

업데이트된 import: 3개 파일
  - src/presentation/features/auth/screens/login-screen.tsx
  - src/presentation/features/auth/screens/register-screen.tsx
  - src/presentation/features/onboarding/screens/welcome-screen.tsx

tsc --noEmit: 통과
eslint: 통과
```

## 12. 완료 후 안내

다음 단계:
- 추출된 컴포넌트에 반응형 적용: `/react-responsive`
- 테스트 재생성: `/react-test`
- 전체 재사용 패턴 재스캔: widget-inspector-react 에이전트 (deep 모드)

# References

- `references/project-detection.md` — 프로젝트 감지 (tsconfig paths alias)
- `references/clean-arch-layout.md` — 공용 컴포넌트 배치 (`presentation/shared/components/`)
- `docs/react/kit-design/g5-ui-patterns.md` §3 — 이 스킬의 상세 설계
