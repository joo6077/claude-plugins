---
name: react-form
description: >
  React Hook Form + Zod를 통합한 폼 컴포넌트를 생성한다.
  "폼 만들어줘", "form validation", "Hook Form", "useForm", "Zod 폼", "입력 폼", "react-form" 같은 요청 시 트리거.
  API 계층(datasource, repository)만 필요할 때는 트리거하지 않는다 — /react-api 사용.
  서버 상태 훅만 필요할 때는 트리거하지 않는다 — /react-query 사용.
argument-hint: "<FormName> [--schema=<path>] [--submit=<hookPath>]"
user-invocable: true
---

# Gotchas

1. **Submit은 Result 반환, try/catch 금지** — 폼 제출 로직은 `Promise<Result<T, Failure>>`를 반환하는 mutation 훅을 props로 주입받는다. 컴포넌트 안에서 `try/catch`로 submit 에러를 잡지 않는다. 상위 useCase에서 이미 Result로 변환되어 있어야 한다.
2. **에러 표시는 `formState.errors`만** — 별도 state로 에러 메시지를 관리하지 않는다. 필드 에러는 `formState.errors.<field>?.message`, 제출 실패(서버/네트워크 에러)는 `setError('root.serverError', { message })` 후 `formState.errors.root?.serverError?.message` 로 표시.
3. **`defaultValues` 필수** — 초기값 없이 시작하면 uncontrolled → controlled 전환 경고가 발생한다. 빈 문자열이라도 모든 필드에 명시한다.
4. **controlled 컴포넌트는 `Controller` 필수** — `register()`는 uncontrolled input 전용이다. shadcn의 `Select`, `Checkbox`, `RadioGroup` 같은 controlled 컴포넌트에는 반드시 `Controller`로 래핑한다.
5. **`zodResolver`와 수동 `validate` 병용 주의** — `zodResolver`를 쓰면 resolver 검증이 우선 실행된다. 필드별 `validate` 옵션은 resolver를 통과한 뒤에만 동작한다. 중복 검증을 피한다.
6. **Zod v4 + React Hook Form TypeScript 이슈** — `z.infer`가 `unknown`으로 잡히는 제네릭 타입 이슈가 보고된 사례가 있다. 스키마는 `z.object(...)` 직접 정의, 타입은 `z.infer<typeof Schema>` 직접 파생 패턴만 사용한다. 제네릭 래퍼(`type FormValues<T extends z.ZodType> = z.infer<T>`)는 생성하지 않는다.
7. **폼 컴포넌트에서 직접 fetch 금지** — 컴포넌트 안에서 `fetch()`, repository, datasource를 직접 호출하지 않는다. 반드시 mutation 훅 또는 UseCase를 props로 주입한다.
8. **Strict TS** — `useForm<Values>()` 제네릭 명시 필수. `register('<field>')` 필드명은 Values 키로 타입 체크된다. `any`, `as` 단언, `!` non-null 단언 금지.
9. **상태 분리 원칙 (Hook Form vs Zustand vs TanStack Query 3-way)** — 3 도메인을 섞지 않는다. 섞으면 동기화 버그·불필요한 리렌더·무한 루프가 반복된다.
    - **폼 로컬 상태(입력값/dirty/touched/validation)** → React Hook Form 이 단독 소유. `useState` 로 별도 동기화 금지, `useEffect(() => setValue(...), [data])` 로 서버 응답을 폼에 강제 주입 금지 — `defaultValues` 또는 `form.reset(data)` 로 1회만 주입.
    - **서버 상태(폼 프리필 데이터, submit 결과)** → TanStack Query `useQuery` / `useMutation` 이 단일 진실 공급원. `mutateAsync` 의 반환값을 폼 local state 로 복사 금지. Optimistic update 는 queryClient 로만.
    - **폼 외부 클라이언트 UI 상태(draft 공유, multi-step wizard 진행도, 공통 banner)** → Zustand (`/react-store`). RHF 내부 값에 접근하려면 `useFormContext` 또는 `subscribe` 사용, store 에 폼 값 미러링 금지.
    - 서로 다른 상태 도메인 간 동기화가 필요한 유일한 접점: `form.reset(query.data)` (서버 → 폼 초기화 1회), `mutation.mutate(form.getValues())` (폼 → 서버 submit 1회). 그 외 자동 양방향 바인딩 금지.
10. **RHF v8 beta — 아직 프로덕션 사용 금지** — React Hook Form v8.0.0-beta.1 (2026-01-11) 이 공개됐으나 breaking changes 포함. 2026-Q2 기준 **v7.71.x 안정 버전을 사용**한다. v8 stable 릴리스 전까지 마이그레이션하지 않는다.
11. **`@hookform/resolvers` Standard Schema 지원 + Zod 4 호환은 v5.1+ 에서 해소 (2026-08-13 정정)** — Standard Schema 기반 resolver 는 v5.2.2 에서 추가됐다. **Zod v4 타입 호환성 이슈는 `@hookform/resolvers@5.1.0` 에서 이미 해소됐다** (현행 stable 5.5.7). `import { z } from 'zod/v3'` workaround 를 기본 전제로 유지하지 마라 — 그 alias 는 **legacy resolver(v5.1.0 미만)** 에 묶인 프로젝트 전용이다. Standard Schema 로 전환 시 resolver import 경로가 변경되므로 점진적 마이그레이션을 권장한다.
12. **Enumerate-before-Act (skill-design-guide §5.5)** — 폼을 생성하기 전에 기존 Zod 스키마(`*-schema.ts`)와 폼 컴포넌트를 `Glob`/`Grep` 으로 전수 스캔하여 (a) 동일/유사 폼 명, (b) 재사용 가능한 기존 스키마, (c) 같은 필드 집합을 검증하는 기존 resolver 를 먼저 **모두 열거**한다. 열거 결과를 체크리스트로 사용자에게 보이고 합의한 뒤에만 파일을 생성한다. 중복 스키마는 `z.infer` 파생 타입 불일치를 유발한다 (insights-report #2 wrong_approach 대응). 출처: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#set-appropriate-degrees-of-freedom
13. **요청한 필드만 — 임의 필드·검증 확장 금지** — 사용자가 지정한 필드만 스키마와 폼에 포함한다. "이메일·비밀번호 폼" 요청에 약관 동의·전화번호·reCAPTCHA·다단계 스텝을 요청 없이 임의로 덧붙이지 마라. 표준으로 끼는 필드가 있으면 그 사실을 **먼저 알리고** 추가 여부를 확인한다 (insights-report #3 excessive_changes 대응).

# Process

## 1. 프로젝트 환경 감지

`references/project-detection.md` 절차를 실행한다. `react-hook-form`, `@hookform/resolvers`, `zod` 패키지 설치 여부를 확인한다. 미설치 시 `/react-init`을 먼저 실행하도록 안내한다.

## 2. 입력 수집

- `form_name` (필수): PascalCase (예: `LoginForm`, `UserEditForm`, `ProductCreateForm`)
- `--schema` (선택): 이미 있는 domain entity Zod 스키마 파일 경로. 없으면 인라인 스키마 정의
- `--submit` (선택): submit 시 호출할 mutation 훅 경로. 없으면 props 주입 방식으로 생성

kebab-case 변형: `LoginForm` → `login-form`.

## 3. 스키마 확인

`--schema` 경로가 주어지면 해당 파일에서 Zod 스키마를 import한다. 없으면 인라인으로 폼 전용 스키마를 정의한다. 도메인 엔티티 스키마가 있으면 import 후 `pick`/`omit`으로 폼 전용 shape를 파생한다.

## 4. 폼 컴포넌트 생성

`src/presentation/features/<feature>/components/<form-name>.tsx`:

```tsx
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import type { Result } from 'neverthrow'

// 폼 전용 스키마 — 도메인 엔티티 스키마가 있으면 import 후 파생
const <Form>Schema = z.object({
  // 폼 필드를 여기에 정의
  email: z.string().email('올바른 이메일을 입력하세요'),
  password: z.string().min(8, '비밀번호는 8자 이상이어야 합니다'),
})

type <Form>Values = z.infer<typeof <Form>Schema>

type <Form>Failure =
  | { kind: '<form>/invalid-credentials' }
  | { kind: '<form>/network-error'; cause: string }

type Props = {
  onSubmit: (values: <Form>Values) => Promise<Result<void, <Form>Failure>>
}

export function <Form>({ onSubmit }: Props) {
  const form = useForm<<Form>Values>({
    resolver: zodResolver(<Form>Schema),
    defaultValues: {
      email: '',
      password: '',
    },
  })

  const handleSubmit = form.handleSubmit(async (values) => {
    const result = await onSubmit(values)
    if (result.isErr()) {
      switch (result.error.kind) {
        case '<form>/invalid-credentials':
          form.setError('root.serverError', {
            message: '이메일 또는 비밀번호가 올바르지 않습니다',
          })
          break
        case '<form>/network-error':
          form.setError('root.serverError', {
            message: '네트워크 오류. 다시 시도해주세요',
          })
          break
      }
    }
  })

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* 서버/네트워크 에러 — root.serverError */}
      {form.formState.errors.root?.serverError && (
        <p className="text-sm text-destructive" role="alert">
          {form.formState.errors.root.serverError.message}
        </p>
      )}

      <div>
        <label htmlFor="email">이메일</label>
        <input
          id="email"
          type="email"
          aria-describedby={form.formState.errors.email ? 'email-error' : undefined}
          {...form.register('email')}
        />
        {form.formState.errors.email && (
          <p id="email-error" className="text-sm text-destructive">
            {form.formState.errors.email.message}
          </p>
        )}
      </div>

      <div>
        <label htmlFor="password">비밀번호</label>
        <input
          id="password"
          type="password"
          aria-describedby={form.formState.errors.password ? 'password-error' : undefined}
          {...form.register('password')}
        />
        {form.formState.errors.password && (
          <p id="password-error" className="text-sm text-destructive">
            {form.formState.errors.password.message}
          </p>
        )}
      </div>

      <button type="submit" disabled={form.formState.isSubmitting}>
        {form.formState.isSubmitting ? '처리 중…' : '제출'}
      </button>
    </form>
  )
}
```

## 5. Controlled 컴포넌트 패턴 (shadcn Select, Checkbox 등)

`register()`가 아닌 `Controller`를 사용한다:

```tsx
import { Controller } from 'react-hook-form'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'

// 폼 컴포넌트 내부
<Controller
  name="role"
  control={form.control}
  render={({ field, fieldState }) => (
    <div>
      <Select onValueChange={field.onChange} defaultValue={field.value}>
        <SelectTrigger>
          <SelectValue placeholder="역할 선택" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="admin">관리자</SelectItem>
          <SelectItem value="member">멤버</SelectItem>
        </SelectContent>
      </Select>
      {fieldState.error && (
        <p className="text-sm text-destructive">{fieldState.error.message}</p>
      )}
    </div>
  )}
/>
```

## 6. 성공 후 처리 (화면 연동)

폼 컴포넌트를 사용하는 screen/page에서 성공 분기를 처리한다:

```tsx
import { useNavigate } from '@tanstack/react-router'
import { useLogin } from '../hooks/use-login'
import { LoginForm } from '../components/login-form'

export function LoginScreen() {
  const navigate = useNavigate()
  const loginMutation = useLogin()

  const handleSubmit = async (values: LoginFormValues) => {
    const result = await loginMutation.mutateAsync(values)
    if (result.isOk()) {
      navigate({ to: '/dashboard' })
    }
    return result
  }

  return <LoginForm onSubmit={handleSubmit} />
}
```

## 7. Strict TS 검증

```bash
pnpm tsc --noEmit
pnpm eslint src/presentation/features/<feature>/components/<form-name>.tsx --max-warnings=0
```

## 8. 완료 후 안내

생성 파일 목록 출력. 다음 단계:
- mutation 훅 연동: `/react-query`
- 화면 배치: `/react-screen`
- 테스트 생성: `/react-test` (G4)

# References

- `references/project-detection.md` — 프로젝트 환경 감지
- `references/clean-arch-layout.md` — 레이어 배치 규칙 및 금지 import 방향
- `references/result-patterns.md` — neverthrow Result 패턴 (submit Result 체인, isOk/isErr)
- `docs/react/kit-design/g2-state-data.md` §4 — 이 스킬 상세 설계 (zodResolver 통합, Zod v4 이슈, Gotchas)
