---
name: react-l10n
description: >
  Lingui v5 매크로 기반으로 번역 문자열을 추가하고 codegen 흐름을 자동화한다.
  Trans 컴포넌트, t 매크로, Plural 컴포넌트 사용 패턴 안내 및 locale 전환 패턴 세팅.
  "번역 추가", "i18n 키", "다국어 지원", "Lingui", "l10n", "locale 전환" 같은 요청 시 트리거.
  하드코딩된 문자열을 매크로로 교체할 때도 트리거한다.
argument-hint: "<message> [--context=<번역자용 설명>] [--component=<파일경로>]"
user-invocable: true
---

## Gotchas

1. **하드코딩된 문자열 금지** — 모든 사용자 표시 문자열은 반드시 `t` 매크로 또는 `<Trans>` 컴포넌트를 경유해야 한다. 하드코딩된 한국어/영어 문자열은 `/react-audit` 이 검출한다.
2. **매크로 import 경로 혼동 주의** — Lingui v5 에서 `@lingui/macro` (구버전) 가 분리됨. JSX/React 는 `@lingui/react/macro`, core 함수는 `@lingui/core/macro`. 잘못 import 하면 컴파일 단계에서 매크로가 적용되지 않는다.
3. **Vite 플러그인 순서 고정** — `react({ plugins: [['@lingui/swc-plugin', {}]] })` 가 반드시 `lingui()` 플러그인 앞에 와야 한다. SWC 가 먼저 매크로를 transpile 한 뒤 lingui plugin 이 catalog 를 주입한다.
4. **`I18nProvider` 래핑 필수** — App 최상단에 `<I18nProvider i18n={i18n}>` 가 없으면 `<Trans>` / `t` 매크로가 동작하지 않는다.
5. **domain 레이어에 매크로 import 금지** — `src/domain/` 은 i18n 을 모른다. Failure 의 사용자 메시지 매핑은 presentation 레이어의 `display-failure.ts` 에서 처리한다.
6. **`extract` 후 빈 번역 키** — `lingui extract` 실행 후 `ko.po` 에 빈 `msgstr` 로 남은 키는 런타임에 원본(en) 으로 fallback 된다. 번역 추가 안내를 사용자에게 반드시 전달한다.
7. **동적 key 는 `msg` 매크로** — 컴포넌트 밖 상수 정의나 reducer message 에는 `msg` 매크로를 쓰고 `i18n._(msg)` 로 호출한다. 동적 key 에 `any` 사용 금지.
8. **서버 컴포넌트 미지원** — react-kit ��본 구성(Vite + TanStack Router)은 SSR 없음. Lingui RSC 지원은 해당 없다.
9. **`useLingui` 매크로 — 컴포넌트 내 비-JSX 메시지 간소화** — `@lingui/react/macro` 에서 import. `const { t } = useLingui()` 패턴으로 컴포넌트 함수 스코프 내에서 사용한다. **모듈 레벨에서 사용 불가** — 반드시 함수 스코프 안에서 호출한다. 모듈 레벨 상수는 기존 `msg` 매크로 + `i18n._(msg)` 패턴을 유지한다.

    나쁜 예 — 모듈 레벨:

    ```ts
    import { useLingui } from '@lingui/react/macro'
    const { t } = useLingui() // 에러: 함수 밖 호출
    ```

    좋은 예 — 컴포넌트 내부:

    ```tsx
    import { useLingui } from '@lingui/react/macro'
    function MyComponent() {
      const { t } = useLingui()
      return <p>{t`안녕하세요`}</p>
    }
    ```

10. **매크로 분리 codemod** — 기존 `@lingui/macro` 에서 v5 분리 import 로 일괄 전환: `npx @lingui/codemods split-macro-imports <path>`. 수동 import 경로 변경 실수를 방지한다.
11. **RTL 언어 지원 — shadcn CLI 자동 매핑 (2026-01)** — shadcn CLI 가 logical property (`start`/`end`) 를 자동 매핑하여 아랍어, 히브리어 등 RTL 언어를 즉시 대응한다. 새 컴포넌트 추가 시 `left`/`right` 대신 `start`/`end` logical property 를 사용하면 별도 RTL 스타일링 없이 양방향 레이아웃이 동작��다.

## Process

### 1. 환경 감지

`references/project-detection.md` 절차를 실행하여 Lingui 설치 여부와 설정 파일을 확인한다.

| 감지 대상 | 경로/패턴 |
|----------|---------|
| Lingui 설치 | `package.json` 의 `@lingui/react`, `@lingui/core`, `@lingui/cli` |
| 설정 파일 | `lingui.config.ts` (프로젝트 루트) |
| locale catalog | `src/infrastructure/i18n/locales/<locale>.po` |
| i18n setup | `src/infrastructure/i18n/setup.ts` |
| Vite 플러그인 | `vite.config.ts` 의 `@lingui/vite-plugin` |

Lingui 가 미설치라면 `/react-init` 을 먼저 실행하도록 안내한다.

지원 locale 목록을 `lingui.config.ts` 의 `locales` 배열에서 읽는다.

### 2. 입력 파싱

`$ARGUMENTS` 에서 번역할 원본 문자열, 컨텍스트, 컴포넌트 경로를 파싱한다.

- `--context` : 번역자용 설명 (예: "로그인 버튼 레이블")
- `--component` : 문자열을 삽입할 컴포넌트 파일 경로

인자 없이 실행하면 interactive 모드: 번역할 문자열을 사용자에게 질문한다.

### 3. 번역 매크로 선택 및 삽입

대상 컴포넌트 파일을 읽어 맥락을 파악한 뒤 아래 규칙에 따라 매크로를 선택한다.

#### JSX 내부 — `<Trans>` 컴포넌트

```tsx
import { Trans } from '@lingui/react/macro'

export function Welcome({ name }: { name: string }) {
  return (
    <h1>
      <Trans>안녕하세요, {name}님!</Trans>
    </h1>
  )
}
```

컴파일 시 `id` 가 원본 문자열 해시로 자동 생성된다. 직접 id 를 지정하려면 `<Trans id="custom.id" message="안녕하세요, {name}님!" values={{ name }} />` 명시.

#### 속성값 / 동적 문자열 — `useLingui` 의 `t`

```tsx
import { useLingui } from '@lingui/react/macro'

export function SubmitButton({ disabled }: { disabled: boolean }) {
  const { t } = useLingui()
  return (
    <button disabled={disabled} aria-label={t`제출`}>
      {t`로그인`}
    </button>
  )
}
```

#### 복수형 — `<Plural>` 컴포넌트

```tsx
import { Plural } from '@lingui/react/macro'

export function ItemCount({ count }: { count: number }) {
  return (
    <span>
      <Plural value={count} one="항목 1개" other="항목 # 개" />
    </span>
  )
}
```

#### 컴포넌트 밖 상수 — `msg` 매크로

```ts
import { msg } from '@lingui/core/macro'
import { i18n } from '@lingui/core'

const BUTTON_LABEL = msg`저장`

export function getLabel(): string {
  return i18n._(BUTTON_LABEL)
}
```

**매크로 선택 요약:**

| 사용처 | 매크로 | import |
|--------|--------|--------|
| JSX 렌더 안 | `<Trans>` | `@lingui/react/macro` |
| 속성값, 동적 문자열 | `t` (via `useLingui`) | `@lingui/react/macro` |
| 복수형 | `<Plural>` | `@lingui/react/macro` |
| 컴포넌트 밖 상수 | `msg` | `@lingui/core/macro` |

### 4. codegen 흐름

매크로 삽입 후 아래 순서를 실행한다:

```bash
# 1. 소스 스캔 → .po 파일에 새 키 추가
pnpm lingui extract

# 2. 삭제된 키 정리 (선택)
pnpm lingui extract --clean

# 3. .po → runtime catalog 컴파일 (Vite 플러그인이 dev 모드에서 자동 수행)
pnpm lingui compile
```

`extract` 후 각 locale 의 `.po` 파일에 빈 `msgstr` 로 새 키가 추가된다. **번역 자체는 사람이 입력**해야 한다. 사용자에게 번역 추가 위치를 안내한다:

```text
src/infrastructure/i18n/locales/ko.po 에서 아래 항목에 번역을 입력하세요:

msgid "로그인"
msgstr ""      ← 여기에 한국어 번역 입력 (동일 언어면 그대로)
```

### 5. Locale 전환 패턴

#### i18n setup (`src/infrastructure/i18n/setup.ts`)

```ts
import { i18n } from '@lingui/core'

export async function activateLocale(locale: string): Promise<void> {
  // 번들 크기 최적화: 동적 import 로 lazy load
  const { messages } = await import(`./locales/${locale}.po`)
  i18n.load(locale, messages)
  i18n.activate(locale)
}

// 초기화 — 브라우저 언어 감지
const browserLocale = navigator.language.startsWith('ko') ? 'ko' : 'en'
activateLocale(browserLocale)
```

#### App 최상단 래핑 (`src/presentation/app.tsx`)

```tsx
import { I18nProvider } from '@lingui/react'
import { i18n } from '@lingui/core'

export function App() {
  return (
    <I18nProvider i18n={i18n}>
      {/* 라우터 또는 앱 트리 */}
    </I18nProvider>
  )
}
```

#### Locale 전환 컴포넌트

```tsx
import { useState } from 'react'
import { activateLocale } from '@/infrastructure/i18n/setup'

const SUPPORTED_LOCALES = ['en', 'ko', 'ja'] as const
type Locale = typeof SUPPORTED_LOCALES[number]

export function LocaleSwitcher() {
  const [locale, setLocale] = useState<Locale>('ko')

  async function handleChange(next: Locale) {
    await activateLocale(next)
    setLocale(next)
  }

  return (
    <select value={locale} onChange={(e) => handleChange(e.target.value as Locale)}>
      {SUPPORTED_LOCALES.map((l) => (
        <option key={l} value={l}>{l.toUpperCase()}</option>
      ))}
    </select>
  )
}
```

locale 선택 상태를 영속화하려면 `localStorage` 에 저장하고 `activateLocale` 호출 전에 읽는다:

```ts
// setup.ts 초기화 부분
const saved = localStorage.getItem('locale') as Locale | null
const initial = saved ?? (navigator.language.startsWith('ko') ? 'ko' : 'en')
activateLocale(initial)

// LocaleSwitcher 에서 변경 시
localStorage.setItem('locale', next)
await activateLocale(next)
```

### 6. Lingui 기본 구조 확인 (G1 생성)

G1 `/react-init` 이 이미 생성한 구조를 전제한다:

```text
src/
├── infrastructure/i18n/
│   ├── setup.ts
│   └── locales/
│       ├── en.po
│       ├── ko.po
│       └── ja.po          (선택)
lingui.config.ts            (프로젝트 루트)
vite.config.ts              (@lingui/vite-plugin 포함)
```

`lingui.config.ts` 확인:

```ts
import { defineConfig } from '@lingui/cli'

export default defineConfig({
  sourceLocale: 'en',
  locales: ['en', 'ko', 'ja'],
  catalogs: [
    {
      path: 'src/infrastructure/i18n/locales/{locale}',
      include: ['src'],
    },
  ],
})
```

`vite.config.ts` 플러그인 순서 확인:

```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import { lingui } from '@lingui/vite-plugin'

export default defineConfig({
  plugins: [
    // SWC 가 먼저 매크로 transpile
    react({ plugins: [['@lingui/swc-plugin', {}]] }),
    // 그 다음 lingui 가 catalog 주입
    lingui(),
  ],
})
```

### 7. 결과 보고

작업 완료 후 사용자에게 안내한다:

- 삽입된 매크로 위치와 코드 스니펫
- `lingui extract` 실행 결과 (새로 추가된 키 수)
- 번역이 필요한 `.po` 파일 경로와 빈 키 목록
- 사용 예시:

```tsx
// JSX 내부
<Trans>로그인</Trans>

// 속성값
const { t } = useLingui()
<button aria-label={t`로그인`}>

// 복수형
<Plural value={count} one="항목 1개" other="항목 # 개" />
```

## References

- `references/project-detection.md` — 환경 감지
- `references/clean-arch-layout.md` — 레이어별 경로 규칙
- 소스 문서: `docs/react/kit-design/g4-quality.md` §3
- Lingui 공식: https://lingui.dev/ref/macro, https://lingui.dev/tutorials/react
