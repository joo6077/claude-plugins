# Style Guide

react-kit 이 생성하는 모든 코드가 준수해야 할 스타일 규칙. `/react-audit` 가 이 규칙을 검증한다.

## Strict TypeScript (`tsconfig.json`)

```jsonc
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitOverride": true,
    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "skipLibCheck": true,
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "jsx": "react-jsx",
    "paths": { "@/*": ["./src/*"] }
  }
}
```

## 금지 사항 (ESLint error 레벨)

- `any` 사용 금지 (`@typescript-eslint/no-explicit-any`)
- `as` 타입 단언 제한 (`as const` 만 허용)
- `!` non-null 단언 금지 (`@typescript-eslint/no-non-null-assertion`)
- `export default` 금지 (`no-default-export`)
- `React.FC` 사용 경고 — 대신 `(props: Props) => JSX.Element` 또는 `forwardRef`
- `console.log` production 경고 (`no-console`)
- `throw new` in `src/domain/` — Result 타입 사용
- 상대 경로 `'../../../'` — absolute `@/` 만 허용

## Naming

- **File**: kebab-case (`user-profile-card.tsx`, `use-drag.ts`)
- **Component**: PascalCase (`UserProfileCard`)
- **Hook**: `use` prefix (`useDrag`, `useUser`)
- **Type**: PascalCase (`User`, `UserFailure`)
- **Zod schema**: PascalCase + `Schema` suffix (`UserSchema`)
- **Store**: `use<Name>Store` 형태 (`useAuthStore`)

## Prettier 설정

```json
{
  "semi": false,
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2
}
```

## ESLint flat config 최소 구성

`docs/react/kit-design/g1-scaffolding.md` §1.6 Gotchas 의 "eslint-plugin-react-hooks flat config 수동 와이어링" 경고를 반드시 지킬 것.

## 관련 문서

- `docs/react/kit-design/g1-scaffolding.md` — `/react-init` 이 생성하는 초기 설정
- `docs/react/kit-design/g6-build-audit.md` §4.5 — `/react-audit` 의 Strict TS 카테고리 grep 패턴
