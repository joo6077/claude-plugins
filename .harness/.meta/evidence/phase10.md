---
phase: 10
title: "Phase 10 react-kit — 확보된 외부 근거"
collected: 2026-09-24
method: codex (foreground, 직접 호출 · gpt-5.6-sol · 조회는 curl/gh)
inputs: 처리 배정표(.claude/kaizen-input/insights-report.md)의 Phase 10 행 · phase-research-templates.md Phase 10 필수 출처 · 현행화 점검
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치를 지어내지 마라. 없으면 미반영으로 남긴다.
---

읽기 전용으로 확인했으며 파일 변경은 하지 않았다. Context7 도구는 제공되지 않아 표의 공식 fallback과 GitHub 원문, npm registry를 `curl`/`gh`로 조회했다.

## 1. 출처 목록

실제로 조회한 출처만 열거한다.

- React
  - [React 19 발표](https://react.dev/blog/2024/12/05/react-19)
  - [React `forwardRef` 문서](https://react.dev/reference/react/forwardRef)
  - [React 19.3 발표](https://react.dev/blog/2026/09/09/react-19-3)
  - [React 19.3 GitHub release](https://github.com/facebook/react/releases/tag/v19.3.0)
- TanStack Query
  - [v5 migration guide](https://tanstack.com/query/v5/docs/framework/react/guides/migrating-to-v5)
- Tauri
  - [Vite frontend 설정](https://v2.tauri.app/start/frontend/vite/)
  - [Capabilities](https://v2.tauri.app/security/capabilities/)
- Vite
  - [`server.port`·`server.strictPort`](https://vite.dev/config/server-options.html#server-port)
  - [CLI `--port`·`--strictPort`](https://vite.dev/guide/cli)
  - [Vite 8 발표](https://vite.dev/blog/announcing-vite8)
- Vitest
  - [`passWithNoTests`](https://vitest.dev/config/passwithnotests)
  - [`allowOnly`](https://vitest.dev/config/allowonly)
  - [`test.skip`·`skipIf`](https://vitest.dev/api/)
- Tailwind CSS
  - [`@theme` 문서](https://tailwindcss.com/docs/theme)
  - [Tailwind CSS v4 발표](https://tailwindcss.com/blog/tailwindcss-v4)
- Zustand
  - [v5 migration 원문](https://raw.githubusercontent.com/pmndrs/zustand/main/docs/reference/migrations/migrating-to-v5.md)
- Lingui
  - [CLI `extract --clean`](https://lingui.dev/ref/cli)
  - [v6 migration](https://lingui.dev/releases/migration-6)
  - [Lingui v6.8.0 release](https://github.com/lingui/js-lingui/releases/tag/v6.8.0)
- React Hook Form·Zod
  - [`@hookform/resolvers` v5.1.0 release](https://github.com/react-hook-form/resolvers/releases/tag/v5.1.0)
  - [React Hook Form v7.88.0](https://github.com/react-hook-form/react-hook-form/releases/tag/v7.88.0)
  - [`@hookform/resolvers` v5.9.1](https://github.com/react-hook-form/resolvers/releases/tag/v5.9.1)
  - [Zod v4.6.5](https://github.com/colinhacks/zod/releases/tag/v4.6.5)
- 셸 조건식
  - [GNU Bash Conditional Expressions](https://www.gnu.org/software/bash/manual/html_node/Bash-Conditional-Expressions.html)
- 2026-09-24 `latest` dist-tag
  - [react](https://registry.npmjs.org/react/latest)
  - [@tanstack/react-query](https://registry.npmjs.org/%40tanstack%2freact-query/latest)
  - [@tauri-apps/cli](https://registry.npmjs.org/%40tauri-apps%2fcli/latest)
  - [tailwindcss](https://registry.npmjs.org/tailwindcss/latest)
  - [zustand](https://registry.npmjs.org/zustand/latest)
  - [@lingui/core](https://registry.npmjs.org/%40lingui%2fcore/latest)
  - [react-hook-form](https://registry.npmjs.org/react-hook-form/latest)
  - [@hookform/resolvers](https://registry.npmjs.org/%40hookform%2fresolvers/latest)
  - [zod](https://registry.npmjs.org/zod/latest)
  - [vite](https://registry.npmjs.org/vite/latest)

## 2. 항목별 관찰 사실

### other-kits:P1 · F03 · F05

확인된 사실:

- Vite는 지정 포트가 사용 중이면 기본적으로 다음 가용 포트를 시도한다. `server.strictPort: true`이면 다음 포트로 이동하지 않고 종료한다. [`vite.config.template.ts:24`](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/react-kit/templates/vite.config.template.ts:24)에는 현재 `port: 5173`만 있다. [Vite 공식 문서](https://vite.dev/config/server-options.html#server-port)
- Tauri의 공식 Vite 예시는 `devUrl: http://localhost:5173`, `port: 5173`, `strictPort: true`를 함께 두며 “Tauri expects a fixed port”라고 설명한다. 현재 [`react-init/SKILL.md:202`](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/react-kit/skills/react-init/SKILL.md:202)도 `devUrl`을 5173으로 고정한다. [Tauri 공식 Vite 설정](https://v2.tauri.app/start/frontend/vite/)
- [`harness-project.yaml.template:98`](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/react-kit/templates/harness-project.yaml.template:98) 역시 검사 포트를 5173으로 고정한다.
- Vite CLI에는 다른 포트를 지정하는 `--port`와 고정 실패를 요구하는 `--strictPort`가 모두 있다. [Vite CLI](https://vite.dev/guide/cli)

추론:

- `strictPort: true` 추가는 Tauri `devUrl` 및 harness 검사 포트와 실제 서버 포트가 조용히 어긋나는 경로를 차단한다.
- 브라우저 주소와 개발 서버의 `Local` 주소를 대조하고 변경 표식을 확인하는 규칙은 “현재 화면이 이번 코드인가”에 대한 좋은 양성 대조다. 다만 이 두 단계 자체를 정한 공식 표준은 찾지 못했다.
- `새로고침 → 서버 재시작 → Rust 변경이면 wasm-build`라는 정확한 순서도 공식 문서에서 찾지 못했다. 저장소 운영 규칙으로 채택할 수는 있으나 “추론”으로 계약해야 한다.

반대·제약 근거:

- “포트가 차면 `--port`로 다른 번호를 주라”는 안내는 브라우저 단독 확인에는 맞지만, Tauri 실행에서는 고정 `devUrl`, harness에서는 `vm_port`도 같은 번호로 맞추지 않으면 다시 불일치한다. [Tauri 설정](https://v2.tauri.app/start/frontend/vite/)과 [Vite CLI](https://vite.dev/guide/cli)
- 따라서 `g6-build-audit` 안내에는 “Tauri/harness를 함께 쓸 때는 소비자 설정도 같은 포트로 맞춘다”는 제한이 필요하다.

### other-kits:P2

확인된 사실:

- [`project-detect.sh:14`](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/react-kit/scripts/project-detect.sh:14)와 18·30·32행은 파일이나 값이 없을 때 문자열 `null`을 출력한다.
- [`project-detect.sh:52`](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/react-kit/scripts/project-detect.sh:52)는 `-n "$(read_json_field ...)"`을 사용한다. Bash의 `-n string`은 문자열 길이가 0이 아니면 참이므로 `"null"`도 참이다. [GNU Bash manual](https://www.gnu.org/software/bash/manual/html_node/Bash-Conditional-Expressions.html)
- 저장소 전체에서 이 스크립트를 실행하는 스킬·코드는 발견되지 않았다. 검색 결과는 스크립트 자체, 설계·계획 문서, 인사이트 보고서뿐이었다.

결론:

- 최소 수정은 제안대로 `!= "null"` 비교다.
- 그러나 호출자가 없으므로 삭제 여부는 사용자 결정 사항이다.
- 반대 근거는 찾지 못했다. 다만 단순 `!= "null"`은 향후 필드 값이 실제 JSON 문자열 `"null"`인 특수 상황까지 “없음”으로 취급한다. 현재 대상은 패키지 버전 필드라 실질 문제는 작다.

### other-kits:P5

확인된 사실:

- Vitest `passWithNoTests` 기본값은 `false`지만, 활성화하면 테스트를 하나도 찾지 못해도 실패하지 않는다. [Vitest `passWithNoTests`](https://vitest.dev/config/passwithnotests)
- `allowOnly` 기본값은 `!process.env.CI`다. 즉 로컬에서는 `.only`가 허용되고 선택된 테스트만 실행될 수 있다. [Vitest `allowOnly`](https://vitest.dev/config/allowonly)
- 현재 [`react-preflight/SKILL.md:111`](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/react-kit/skills/react-preflight/SKILL.md:111)은 `N passed`만 보고한다. [`react-run/SKILL.md:68`](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/react-kit/skills/react-run/SKILL.md:68)도 test 전용 passed/skipped 칸이 없다.

반대·제약 근거:

- `M>0`이 항상 `.only` 때문인 것은 아니다. Vitest는 의도적인 `test.skip`과 환경 조건부 `skipIf`도 공식 지원한다. [Vitest API](https://vitest.dev/api/)
- 따라서 “M>0이면 실행 자체가 실패”라고 정의하기보다는 “전체 범위 통과 ✓로 표시하지 않고 skipped 범위를 `[미검증]`으로 보고”가 더 정확하다.
- `N=0`을 통과 증거로 인정하지 않는 데 반대되는 근거는 찾지 못했다.

### other-kits:P6

확인된 사실:

- Lingui의 기본 `extract`는 새 메시지를 기존 catalog와 병합해 번역을 보존한다.
- `--clean`은 소스에서 더 이상 발견되지 않는 obsolete 메시지를 catalog에서 제거한다. [Lingui CLI](https://lingui.dev/ref/cli)
- 따라서 매크로가 적용되지 않아 extractor가 메시지를 발견하지 못하면 `--clean`이 번역된 항목까지 제거할 수 있다는 위험 모델은 공식 동작과 일치한다.
- Lingui v6 문서는 `@lingui/macro`가 v5에서 분리·deprecated 되었고 이제 더 이상 유지보수되지 않는다고 명시한다. 대체 경로는 `@lingui/core/macro`와 `@lingui/react/macro`다. [Lingui v6 migration](https://lingui.dev/releases/migration-6)
- 현재 [`react-l10n/SKILL.md:150`](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/react-kit/skills/react-l10n/SKILL.md:150)은 `extract --clean`을 기본 codegen 흐름 안의 선택 단계로 둔다.

추론:

- `--clean`을 기본 흐름에서 빼고 명시적 정리 작업으로 격리하는 것이 안전하다.
- 제안된 `grep '^-msgid'`는 삭제된 ID를 찾지만 해당 ID의 `msgstr`이 채워졌는지는 단독으로 판별하지 못한다. `git diff --stat`과 삭제 목록에 더해 해당 diff 묶음의 `msgstr`도 직접 확인해야 “번역이 채워져 있던 항목”을 판정할 수 있다.

반대 근거:

- 공식 문서는 `--clean`을 금지하지 않는다. obsolete catalog를 의도적으로 정리하는 정상 옵션이다. 위험은 옵션 자체보다 잘못된 extractor 설정·매크로 변환과 결합될 때 생긴다. [Lingui CLI](https://lingui.dev/ref/cli)

## 3. 현행화 — 낡은 곳

2026-09-24 npm `latest` 기준 주요 버전은 React 19.3.0, TanStack Query 5.103.2, Tauri CLI 2.11.5, Tailwind 4.3.3, Zustand 5.0.15, Lingui core 6.8.0, RHF 7.88.0, resolvers 5.9.1, Zod 4.6.5, Vite 8.3.0이다. 각 값은 위 npm registry 출처에서 확인했다.

| 위치 | 현재 값 | 최신 값·판정 |
|---|---|---|
| [`react-init/SKILL.md:18`](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/react-kit/skills/react-init/SKILL.md:18) | “2026-04 현재 React 19.2+” | React 19.3.0. ref-as-prop 방향은 여전히 유효하지만 시점·버전 문구가 낡았다. [React 19.3](https://github.com/facebook/react/releases/tag/v19.3.0) |
| [`react-widget/SKILL.md:17`](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/react-kit/skills/react-widget/SKILL.md:17) | “2026-04 현재 19.2+” | React 19.3.0. `forwardRef`를 새 코드에서 피하라는 방향은 공식 React 문서와 일치한다. [React `forwardRef`](https://react.dev/reference/react/forwardRef) |
| [`react-form/SKILL.md:28`](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/react-kit/skills/react-form/SKILL.md:28) | “현행 stable 5.5.7” | resolvers 5.9.1. 다만 “5.1부터 Zod 4 지원”이라는 호환성 하한은 여전히 맞다. [v5.1.0](https://github.com/react-hook-form/resolvers/releases/tag/v5.1.0), [v5.9.1](https://github.com/react-hook-form/resolvers/releases/tag/v5.9.1) |
| [`react-init/SKILL.md:19`](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/react-kit/skills/react-init/SKILL.md:19) | “현행 stable 5.5.7” | resolvers 5.9.1. `zod/v3`를 legacy 전용으로 둔 결론은 유지 가능하다. 같은 두 release 출처 |
| [`react-init/SKILL.md:173`](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/react-kit/skills/react-init/SKILL.md:173) | Lingui stable 6.6.0 | 6.8.0. 그러나 v5 pin은 Node floor를 올리지 않는다는 명시적 호환성 결정이므로 자동 상향 대상은 아니다. [Lingui v6.8.0](https://github.com/lingui/js-lingui/releases/tag/v6.8.0), [v6 migration](https://lingui.dev/releases/migration-6) |
| [`project-detection.md:28`](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/react-kit/references/project-detection.md:28) | 예시 `vite: 8.2.0` | 최신 8.3.0. 예시임을 명확히 하거나 갱신할 수 있다. [npm registry](https://registry.npmjs.org/vite/latest) |
| [`research-log.md:22`](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/react/research-log.md:22) | Vite 8.2.0 | 8.3.0. Vite 8/Rolldown 설명 자체는 유효하다. [Vite 8](https://vite.dev/blog/announcing-vite8) |
| [`research-log.md:23`](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/react/research-log.md:23) | resolvers 5.5.7 | 5.9.1. |
| [`research-log.md:25`](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/react/research-log.md:25) | Lingui 6.6.0 | 6.8.0. |
| [`research-log.md:27`](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/react/research-log.md:27) | React 19.2.8, Query 5.101.4, Tauri 2.11.4, Zustand 5.0.14 | 각각 19.3.0, 5.103.2, 2.11.5, 5.0.15. Tailwind 4.3.3은 그대로다. |
| [`research-log.md:303`](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/react/research-log.md:303) | `<ViewTransition>`을 canary/backlog로 분류 | React 19.3에서 stable. [React 19.3 발표](https://react.dev/blog/2026/09/09/react-19-3) |
| [`research-log.md:392`](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/docs/react/research-log.md:392) | React canary 통합, stable 대기 | React 19.3에서 `<ViewTransition>`과 Fragment Refs가 stable이므로 낡았다. [React 19.3 발표](https://react.dev/blog/2026/09/09/react-19-3) |

필수 소스 관련 구현 판단:

- Query v5 object-form은 여전히 정확하다. v5 migration guide는 단일 object 형식만 지원한다고 명시한다. [TanStack migration](https://tanstack.com/query/v5/docs/framework/react/guides/migrating-to-v5)
- Tauri capability 설계도 유효하다. capability는 window/webview별 permission을 정하고 `src-tauri/capabilities`에 JSON/TOML로 둔다. [Tauri capabilities](https://v2.tauri.app/security/capabilities/)
- Tailwind `@theme`와 OKLCH 예시는 현행 공식 문서와 일치한다. [Tailwind theme](https://tailwindcss.com/docs/theme)
- Zustand의 “새 객체·배열 selector에는 stable reference가 필요하고 `useShallow`로 고친다”는 설명은 유효하다. 다만 primitive selector까지 무조건 감쌀 필요는 없으므로 “모든 selector에 강제”로 확대하면 안 된다. [Zustand v5 migration](https://raw.githubusercontent.com/pmndrs/zustand/main/docs/reference/migrations/migrating-to-v5.md)
- Vite 8은 Rolldown 단일 번들러이고 Node 20.19+ 또는 22.12+가 필요하다. 현재 major 선택은 맞다. [Vite 8 발표](https://vite.dev/blog/announcing-vite8)

## 4. 권장안

Phase 10 계약 조건으로 삼을 만한 항목은 다음과 같다.

1. `vite.config.template.ts`에 `server.strictPort: true`를 넣는다. Tauri `devUrl`과 harness `vm_port`가 5173으로 고정된 현재 구조에서는 정확성 수정이다.

2. 렌더 증거에 아래를 필수화한다.

   - 개발 서버 시작 출력의 Local 주소와 브라우저 주소 일치
   - 이번 변경으로 달라져야 할 표식 하나를 화면에서 확인
   - 실패 시 시도한 새로고침·서버 재시작·필요한 WASM 재빌드를 기록
   - 그래도 확인되지 않으면 `[미검증]`

3. `--port` 우회 문구에는 “Tauri/harness 사용 시 `devUrl`·`vm_port`도 동일하게 맞춘다”를 붙인다.

4. `project-detect.sh`는 먼저 존치 여부를 사용자에게 묻는다. 존치한다면 52행을 `"null"` 명시 비교로 고치고, 결측 package.json과 결측 dependency 입력을 회귀 시험으로 둔다.

5. test 보고는 `N passed · M skipped`로 통일한다.

   - `N=0`: ✓ 금지
   - `M>0`: 전체 범위 ✓ 금지, skipped 범위를 `[미검증]`으로 보고
   - `.only` 존재 여부와 의도적 `skip`을 구분
   - 이유 설명은 기존 render-evidence §3(b)(c)를 참조

6. `lingui extract --clean`을 기본 codegen 흐름에서 제거한다. 명시 실행 시에는:

   - 즉시 `git diff --stat`
   - 번역 폴더의 삭제된 `msgid`
   - 해당 diff의 삭제된 `msgstr` 확인
   - 번역이 있던 항목이면 사용자 확인 전 정리 결과를 채택하지 않음

7. 현행화는 기능 계약과 숫자 갱신을 분리한다.

   - React 19.3의 `<ViewTransition>` stable 전환은 계약에 반영
   - resolver/Zod 호환성 하한 5.1+/v4는 유지
   - Query v5, Tauri 2, Tailwind v4, Zustand v5, Vite 8의 현행 규칙은 유지
   - Lingui v6 상향은 Node 22.19+ floor 결정 전에는 하지 않음

## 5. 못 가져온 것 / 열린 질문

- Context7은 사용 가능한 도구가 아니어서 직접 조회하지 못했다. 대신 필수 표의 공식 fallback 8종을 모두 조회했다.
- “주소+변경 표식 확인” 및 `새로고침 → 재시작 → wasm-build` 순서를 그대로 규정하는 공식 문서는 찾지 못했다. 이는 외부 표준이 아니라 로컬 증거 정책으로 계약해야 한다.
- `project-detect.sh`는 호출자가 없다. 삭제할지, 향후 사용을 위해 한 줄 수정과 시험을 추가할지는 사용자 결정이 필요하다.
- Lingui v5 compatibility pin을 언제 해제할지 결정되지 않았다. v6는 Node 22.19+와 ESM-only를 요구한다. [Lingui v6 migration](https://lingui.dev/releases/migration-6)
- `M>0이면 무조건 실패`는 공식 Vitest 의미보다 강하다. 의도적 skip도 존재하므로 “전체 검증 ✓ 금지 + skipped 범위 미검증”으로 계약하는 편이 근거에 더 정확하다.
