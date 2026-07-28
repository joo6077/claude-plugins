---
title: Render Evidence Protocol (렌더 산출물 완료 증거 규약)
version: 1.0.0
last_updated: 2026-07-27
source: /insights 2026-07-27 Friction #2 · skill-design-guide §3.7 · qa-evaluation-guide §Evidence Validity Gate
enforcement: E2 (체크리스트 아티팩트)
---

# Render Evidence Protocol

렌더 결과가 산출물인 react-kit 스킬(`react-screen` · `react-widget` · `react-skeleton` ·
`react-responsive` · `react-animation`)이 **완료를 선언하기 직전**에 실행하는 증거 규약이다.
`react-test` 는 이 규약이 요구하는 measurement 를 **만드는** 쪽이므로 §4 를 따른다.

상위 정의는 아래를 따르며, 이 문서는 임계값·마커 의미·등급을 **재정의하지 않는다**.

- 마커·임계값 SSOT: `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol
- 증거 유효성 SSOT: 같은 문서 §Evidence Validity Gate
- 등급(E1/E2/E3) SSOT: `harness/docs/guides/skill-design-guide.md` §3.7

## 왜 필요한가

`/insights` 2026-07-27 (53 일 · 51 세션) 에서 **Friction #2 "시각·런타임 검증을 신뢰할 수 없음"**
이 신규 최상위 마찰로 올라왔다. 사고의 형태는 "증거가 없다" 가 아니라 **"증거가 있는데 그 증거가
아무것도 입증하지 않는다"** 였다 — 빈 카탈로그 화면의 스냅샷을 근거로 "정상 렌더링" 을 반복
주장했고 실제 원인은 unbounded-height 리스트 collapse 였다. 사용자 신뢰가 손상되어 욕설로 끝난
세션이 2 건 발생했다.

react-kit 은 관측 사례가 없다. 그러나 **구조적으로 같은 사고가 가능한 도구 기본값을 갖고 있고**
(§3), UI 스킬 5 종의 검증 섹션이 `Strict TS 검증` 하나뿐이었다. 타입이 통과한 컴포넌트는 여전히
빈 화면을 렌더할 수 있다.

## 1. Step 0 — 무엇을 바꾸는지 먼저 확정한다 (Friction #1)

편집 전에 다음 3 줄을 응답에 남긴다. 시각 작업에서 말은 의도를 충분히 규정하지 못한다.

1. **대상**: 바꿀 컴포넌트를 `파일:라인` 으로 지목한다 (신규면 "신규" 라고 쓴다).
2. **바꿀 것 / 바꾸지 않을 것**: 색·간격·모션·레이아웃·breakpoint 중 **유지할 속성을 열거**한다.
3. **교체 여부**: 기존 컴포넌트를 shadcn 프리미티브나 다른 컴포넌트로 **교체**하려면 편집 전에
   승인을 받는다. 기본값은 **기존 컴포넌트 수정**이다.

```text
Bad:  "아이콘이 돌면 좋겠다" → 기존 아이콘 대신 새 스피너 컴포넌트를 만들어 교체 → 전면 재작업
Good: "아이콘이 돌면 좋겠다" → 대상: icon-button.tsx:24 / 바꿀 것: transform 회전만 /
      바꾸지 않을 것: 색·크기·aria-label / 교체 없음 → 편집
```

## 2. 증거 등급 — 무엇을 제출할 수 있는가

렌더 증거는 아래 순서로 시도한다. 상위 단계가 가능한데 하위로 내려가지 않는다.

| 등급 | 증거 | 획득 방법 |
| ---- | ---- | --------- |
| R1 | 실제 렌더 캡처 | Playwright `toHaveScreenshot()` 또는 브라우저 MCP 스냅샷 |
| R2 | 렌더된 DOM 단정 | Testing Library `getByRole` / `findByText` 통과 출력 |
| R3 | 정적 확인 | 클래스·토큰·props 를 `파일:라인` 으로 지목 — **보조 태그 `[정적]`** |

R3 만 확보된 항목은 완료가 아니다. `[정적]` 은 `[미검증]` 을 대체하지 않는다 (정본 조항 1).
R1·R2 가 환경상 불가하면 그 항목에 `[미검증]` 마커와 사유 한 줄을 붙이고 **부분 완료로 보고**한다.

## 3. 공허한 증거 4 유형 — react 도구 기본값이 만드는 자기충족 통과

아래 4 개는 "초록불" 을 만들지만 아무것도 입증하지 않는다. 증거 제출 전에 전부 배제한다.
각 항목은 조회한 공식 문서의 실제 동작에 근거한다.

### (a) 부재 단정이 렌더 실패를 가린다

Testing Library `queryBy*` 는 매치가 없으면 `null` 을, `queryAllBy*` 는 빈 배열 `[]` 을
반환하고 **throw 하지 않는다**. 공식 문서는 `queryBy` 를 "asserting an element that is not
present" 용도로 권장한다. 문제는 컴포넌트가 **아예 렌더되지 않았을 때도 동일하게 통과**한다는
점이다. 이것이 빈 화면을 "문제 없음" 으로 읽는 것과 같은 형태다.

```ts
// 나쁜 예 — 컴포넌트가 throw 해서 아무것도 안 붙어도 통과한다
render(<Skeleton loading={false} />)
expect(screen.queryByTestId('skeleton')).toBeNull()

// 좋은 예 — 부재 단정 앞에 "무언가 렌더됐다" 는 양성 대조(positive control)를 둔다
render(<Skeleton loading={false} />)
expect(screen.getByRole('list')).toBeInTheDocument()   // 양성 대조: 실제 콘텐츠 존재
expect(screen.queryByTestId('skeleton')).toBeNull()    // 그 위에서만 부재가 의미를 갖는다
```

### (b) 0 테스트 green run

Vitest `passWithNoTests` 는 Type `boolean` · Default `false` 이며 문서 설명은 "Vitest will not
fail, if no tests will be found." 다. 이 플래그가 npm script 에 박혀 있거나 파일 glob 이 어긋나면
**0 개 테스트 실행 = 성공** 출력이 나온다. 0 개 테스트는 "위반 없음" 이 아니라 "검사되지 않음"
이다 (유효성 검사 2 — 활성화).

증거에는 반드시 **실행된 테스트 수**를 함께 인용한다. `Tests 0 passed` 는 증거가 아니다.

### (c) `.only` 로 좁혀진 green run

Vitest `allowOnly` 의 기본값은 `!process.env.CI` 다 — 즉 **로컬에서는 `.only` 가 허용**된다.
디버깅 중 남은 `it.only` 하나만 돌고 나머지 전 스위트가 스킵된 상태에서 초록불이 뜬다.

증거 인용 시 `skipped` 카운트를 함께 남긴다. 스킵된 스위트가 있으면 그 범위는 `[미검증]` 이다.

### (d) 빈 화면이 baseline 으로 굳는다

Playwright `toHaveScreenshot()` 은 baseline 이 없을 때 실제 화면을 golden 파일로 기록한다.
그 뒤 `--update-snapshots` 로 갱신하면 **깨진 화면이 정답으로 고정**되고, 이후 모든 실행이
자기 자신과 비교해 통과한다.

- 새 baseline 을 기록·갱신했으면 그 이미지에서 **조건이 요구하는 구체 요소를 지목**해 근거에 쓴다
  (`baseline 에 목록 3 행 · 헤더 "내 그룹" 확인`). 지목할 수 없으면 무효 증거다.
- `maxDiffPixels` / `maxDiffPixelRatio` 를 통과 목적으로 키우지 않는다. 임계를 올린 diff 통과는
  유효성 검사 3(반증 가능성) 실패다 — 어떤 변경에도 같은 결과를 내는 측정은 oracle 이 아니다.
- 갱신 사유를 한 줄로 남긴다. 사유 없는 `--update-snapshots` 는 증거가 아니라 증거 삭제다.

## 4. 완료 전 체크리스트 (E2 — 응답에 복사해 채운다)

```text
## Render Evidence
- 대상: <파일:라인 또는 "신규">
- 유지할 속성: <열거>
- 증거 등급: R1 | R2 | R3
- 증거: <실행 명령 + 출력 인용 / 캡처에서 지목한 구체 요소>
- 실행/스킵 카운트: <passed N · skipped M · 0 이면 사유>
- 공허 증거 배제: (a) 양성대조 O/N.A · (b) 테스트 수 N · (c) skipped M · (d) baseline 지목 O/N.A
- [미검증]: <항목 + 사유 + 시도한 fallback> (없으면 "0 건")
```

- 미검증 **2 건 이상이면 완료가 아니라 부분 완료**로 보고한다 (정본 조항 3 · §3.7 5 조 3 항).
- 체크리스트를 채우지 못한 항목이 있으면 그 상태로 완료를 선언하지 않는다.

## 5. 하지 않는 것

- 임계값(2 건)·마커(`[미검증]`)·등급(E1/E2/E3) 을 이 문서에서 다시 정의하지 않는다. 상위 SSOT 인용만 한다.
- 증거 확보를 위해 **테스트 러너나 스냅샷 도구를 프로젝트에 새로 추가하지 않는다**. 미설치면
  `/react-init` 안내 후 해당 항목을 `[미검증]` 으로 남긴다 (요청 밖 의존성 추가 금지 — 가드레일 §2).
- 애니메이션 검증을 위해 금지 라이브러리를 도입하지 않는다. Library Policy 는 이 규약보다 상위다
  (`common-gotchas.md` G2 / G10).

## References

- `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol — 마커·임계값 SSOT
- `harness/docs/guides/qa-evaluation-guide.md` §Evidence Validity Gate — 유효성 4 검사 SSOT
- `harness/docs/guides/skill-design-guide.md` §3.7 Completion Evidence Gate — 등급·5 조항 SSOT
- `react-kit/agents/react-reviewer.md` §Evidence Validity Gate — 평가 측 짝
- `react-kit/references/common-gotchas.md` G11 — 킷 인덱스 포인터
- [Testing Library — About Queries](https://testing-library.com/docs/queries/about/) — `queryBy` `null` / `queryAllBy` `[]` 반환 (§3 a)
- [Vitest CLI](https://vitest.dev/guide/cli.html) — 플래그 목록 (§3 b, c)
- [Vitest — `passWithNoTests`](https://vitest.dev/config/passwithnotests) — Type `boolean` · Default `false` (§3 b)
- [Vitest — `allowOnly`](https://vitest.dev/config/allowonly) — Type `boolean` · Default `!process.env.CI` (§3 c)
- [Playwright — Visual comparisons](https://playwright.dev/docs/test-snapshots) — `toHaveScreenshot()` baseline 기록 · `--update-snapshots` · `maxDiffPixels` (§3 d)
- [Playwright — Assertions](https://playwright.dev/docs/test-assertions) — auto-retrying assertion 권장 · `expect.poll` / `expect.toPass` (§2 R1)
