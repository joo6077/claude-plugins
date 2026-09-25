---
title: Render Evidence Protocol (렌더 산출물 완료 증거 규약)
version: 1.1.0
last_updated: 2026-09-25
source: /insights 2026-07-27 Friction #2 · /insights 2026-09-24 F01 · F03 · F05 · skill-design-guide §3.7 · qa-evaluation-guide §Evidence Validity Gate
enforcement: E2 (체크리스트 아티팩트)
---

# Render Evidence Protocol

렌더 결과가 산출물인 react-kit 스킬(`react-screen` · `react-widget` · `react-skeleton` ·
`react-responsive` · `react-animation`)이 따르는 증거 규약이다. 이 규약은 **편집 전과 완료 직전 두 번** 실행한다.
`react-test` 는 이 규약이 요구하는 measurement 를 **만드는** 쪽이므로 §4 를 따른다.

- 편집 전: §1 Step 0 과 §2 비교 반복 순서의 1 번(기준 캡처). 새로 만드는 화면·컴포넌트면 기준 캡처 칸에 `신규` 라고 적는다
- 완료 직전: §2 비교 반복 순서의 3 번(반영 확인)부터 §4 체크리스트까지

상위 정의는 아래를 따르며, 이 문서는 임계값·마커 의미·등급을 **재정의하지 않는다**.

- 마커·임계값 SSOT: `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol
- 증거 유효성 SSOT: 같은 문서 §Evidence Validity Gate
- 등급(E1/E2/E3) SSOT: `harness/docs/guides/skill-design-guide.md` §3.7

**형제 규약과 같은 숫자:** §1 의 「같은 역할 기존 화면 2 개 이상」 과 §2 의 「스스로 고치기 최대 3 회」 는
flutter-toolkit `references/visual-evidence-protocol.md` Step 0 · Step 2, design-kit `references/visual-change-protocol.md` §0 · §3 과 같은 값이다.
세 규약이 같이 쓰는 규칙의 정본은 harness `skill-design-guide.md` 한 절에 두기로 했고 그 절은 아직 없다 — 생기기 전까지는 한쪽 값을 바꾸면 다른 두 쪽도 같이 바꾼다.

## 왜 필요한가

`/insights` 2026-07-27 (53 일 · 51 세션) 에서 **Friction #2 "시각·런타임 검증을 신뢰할 수 없음"**
이 신규 최상위 마찰로 올라왔다. 사고의 형태는 "증거가 없다" 가 아니라 **"증거가 있는데 그 증거가
아무것도 입증하지 않는다"** 였다 — 빈 카탈로그 화면의 스냅샷을 근거로 "정상 렌더링" 을 반복
주장했고 실제 원인은 unbounded-height 리스트 collapse 였다. 사용자 신뢰가 손상되어 욕설로 끝난
세션이 2 건 발생했다.

react-kit 은 관측 사례가 없다. 그러나 **구조적으로 같은 사고가 가능한 도구 기본값을 갖고 있고**
(§3), UI 스킬 5 종의 검증 섹션이 `Strict TS 검증` 하나뿐이었다. 타입이 통과한 컴포넌트는 여전히
빈 화면을 렌더할 수 있다.

`/insights` 2026-09-24 (18 세션) 에도 react-kit 관측 사례는 없다. 같은 보고서의 플러터 세션 사고 셋은 개발 서버와
브라우저에서도 같은 모양으로 날 수 있다 — 평평한 줄 대신 카드를 만들고 화면을 보여 달라는 요청에 그 화면으로 가는 칩을
만들었고(F01), 재시작이 조용히 실패했는데 갱신했다고 보고했고(F03), 인자 이름을 틀리거나 남의 시뮬레이터에 붙어 놓고
도구가 고장났다고 세 번 오진했다(F05). Vite 는 지정 포트가 차 있으면 기본으로 다음 빈 포트로 옮긴다. 그러면 Tauri `devUrl` 과
harness 검사 포트(둘 다 5173)가 실제 서버와 조용히 어긋나고, 5173 주소에는 다른 서버의 화면이 떠 있을 수 있다.

## 1. Step 0 — 무엇을 바꾸는지 먼저 확정한다 (Friction #1)

편집 전에 다음 6 줄을 응답에 남긴다. 시각 작업에서 말은 의도를 충분히 규정하지 못한다.

1. **대상**: 바꿀 컴포넌트를 `파일:라인` 으로 지목한다 (신규면 "신규" 라고 쓴다).
2. **바꿀 것 / 바꾸지 않을 것**: 색·간격·모션·레이아웃·breakpoint 중 **유지할 속성을 열거**한다.
3. **교체 여부**: 기존 컴포넌트를 shadcn 프리미티브나 다른 컴포넌트로 **교체**하려면 편집 전에
   승인을 받는다. 기본값은 **기존 컴포넌트 수정**이다.
4. **되말하기**: 요청을 대상 요소 이름과 배치까지 넣어 한 문장으로 되말한다. 두 갈래로 읽히면 묻고 시작한다
   (예: 「추가 칩만 오른쪽 고정」 과 「줄 전체 오른쪽 고정」).
5. **화면 자체**: 화면을 가리키는 요청이면 대상은 그 화면의 라우트 파일(`src/presentation/routes/`)과 화면 컴포넌트
   (`src/presentation/features/<feature>/screens/`)다. 그 화면으로 들어가는 진입점(버튼·링크·칩)이나 화면을 흉내 낸
   그림이 아니다. 라우트 경로(주소)를 함께 적는다.
6. **관례 표**: 같은 역할의 서로 다른 기존 화면 **2 개 이상**을 Read 해서 경로와 함께 표로 남긴다. 칸은 줄 모양(카드인지
   평평한 줄인지) · 칩·뱃지 모양 · 아이콘 뜻(닫기·끝내기·접기) · 재사용할 컴포넌트(경로와 용도)다.

관례 표의 재사용 후보는 앱 코드가 실제로 import 하는지 grep 으로 확인하고, Storybook 이나 시안에서만 쓰이는 컴포넌트는
뺀다. **grep 에 나오지 않은 컴포넌트 이름은 쓰지 않는다.** 같은 역할 기존 화면이 2 개 미만이면 찾은 화면을 전부 적고
`관례 없음 — 같은 역할 기존 화면 N 개` 라고 쓴다. 앱 코드가 아직 없으면 `관례 없음 — 앱 코드 없음` 이다.

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
R1·R2 가 환경상 불가하면 아래 「도구가 고장이라 말하기 전에」 세 확인을 먼저 하고, 그 항목에 `[미검증]` 을 달고 네 칸을 채워
**부분 완료로 보고**한다 — **막는 것**(실행한 명령과 그 실패 출력) · **시도한 우회**(세 확인과 시도한 채널. 정말 없으면 `없음 — 이유`) ·
**통제 불가 사유**(한 문장) · **재검증 명령**(채널이 생기면 돌릴 명령). 칸의 뜻은 `harness/docs/guides/skill-design-guide.md`
§3.7 5 조항 3 항이 정한다. 네 칸 가운데 하나라도 비면 평가 측이 `[미검증:INVALID]` 로 센다.

### 비교 반복 순서 — 지금 보는 화면이 이번 코드인가

R1·R2 증거는 아래 순서로 얻는다. 1 은 편집 전에, 3 부터는 완료 직전에 한다. 새로 만드는 화면·컴포넌트면 1 의 기준 캡처 칸에
`신규` 라고 적는다.

1. **기준 캡처** — 캡처 파일 경로를 남기고 본 것을 요소 단위로 적는다 (「정상」 이 아니라 「목록 3 행 · 헤더 '내 그룹' ·
   하단 여백 있음」). 이번 변경으로 반드시 달라져야 할 눈에 보이는 표식 하나를 이때 정한다 (예: 버튼 색, 칩 순서, 제목 글자)
2. **한 번에 한 의도**만 고친다. 여러 변경을 묶으면 재캡처의 차이가 무엇 때문인지 가를 수 없다
3. **반영 확인** — 지금 보는 화면을 이번 코드가 그렸는지부터 본다
   - 개발 서버를 띄울 때 출력된 `Local:` 주소와 브라우저(브라우저 도구 포함)가 연 주소를 대조한다. 포트가 다르면 다른
     서버의 화면이다. 포트가 차서 서버가 멈췄을 때 다른 포트로 띄우는 법은 `/react-run` 의 `dev` 포트 Gotcha 를 따른다
   - 새로 찍은 캡처에서 1 의 표식이 바뀌었는지로 판정한다. 모듈 교체(HMR) 로그나 새로고침 성공만으로 판정하지 않는다.
     표식이 그대로면 「반영 안 됨」 이다
   - 반영 안 됨이면 같은 새로고침을 되풀이하지 말고 브라우저 새로고침 → 개발 서버를 멈추고 다시 띄우기 → Rust(`crates/core/`)를
     고쳤으면 `/react-run wasm-build` 뒤 서버 다시 띄우기 순서로 가고, 시도한 것을 적는다. 그래도 표식이 그대로면 그 항목은 `[미검증]` 이다
   - 반영이 확인되기 전에는 「갱신했다」 고 말하지 않는다
4. **재캡처** — 반영이 확인된 캡처를 재캡처로 쓰고 경로를 남긴다
5. **대조** — §1 의 유지할 속성이 그대로인지 본다. 의도 외 영역이 변했으면 self-reject 하고 되돌린 뒤 다시 한다.
   **스스로 고치기는 최대 3 회**다. 3 회째도 실패하면 기준 캡처 · 마지막 재캡처 · 달라진 속성을 붙여 사용자에게 넘긴다

주소 대조와 「새로고침 → 서버 다시 띄우기 → WASM 다시 빌드」 순서는 공식 문서가 정한 절차가 아니라 이 킷의 규칙이다.

### 캡처 점검 목록

기준 캡처와 재캡처마다 아래 넷을 본다. 하나라도 걸리면 그 캡처로 PASS 를 주지 않는다.

1. **글자 넘침** — 잘린 글자, 뜻밖의 말줄임, 컨테이너 밖으로 나간 글자, 문서 본체의 가로 스크롤
2. **깨진 글리프** — 네모나 빈칸으로 나온 글자와 이모지. 실제 서비스 글꼴로 그리지 않은 캡처로는 글자 모양을 판정하지 않는다
3. **칩·뱃지와 줄 모양** — 칩·뱃지 모양, 카드인지 평평한 줄인지를 §1 관례 표와 대조한다
4. **디버그 겹침** — 떠 있는 개발 도구 단추·패널·오류 겹침 화면이 판정할 자리를 가리는지 본다. 가렸으면 치우거나 옮긴 뒤
   같은 자리를 다시 찍는다

잘라낸 조각만 보고 결함이라 단정하기 전에 전체 화면을 한 장 더 찍는다. 넘침은 데이터를 고쳐 재현하지 말고 브라우저 글자
크기를 키운 상태로 한 장 더 찍는다.

### 도구가 고장이라 말하기 전에

캡처나 브라우저 도구 호출이 실패하면 고장이라 말하기 전에 셋을 확인하고 그 출력을 응답에 남긴다. 도구 이름은 이 문서에
적지 않는다 — 프로젝트 설정(`.mcp.json` 등)에서 읽는다.

1. 실패한 호출의 인자 이름을 도구 설명의 인자 목록과 대조한다. 틀린 키는 도구 고장이 아니다
2. 도구가 연 페이지가 내가 띄운 서버인지 확인한다 — 주소와 포트를 개발 서버 출력과 대조한다. 여러 세션이 같은 포트나 같은
   브라우저를 나눠 쓰면 남의 화면에 붙어 있을 수 있다
3. 대화상자·팝오버·시트처럼 따로 뜨는 층의 요소는 페이지 전체 스냅샷에서 한 번 더 찾는다. 첫 스냅샷에 없다고 없는 요소로
   단정하지 않는다

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
- 대상: <파일:라인 또는 "신규"> · 라우트: <화면이면 주소>
- 되말하기: <한 문장>
- 관례 표: <같은 역할 기존 화면 경로 2 개 이상 | 관례 없음 — 사유>
- 유지할 속성: <열거>
- 증거 등급: R1 | R2 | R3
- 서버 주소: <개발 서버 출력의 Local 주소> · 연 주소: <브라우저가 연 주소> (R1 이 아니면 N/A)
- 기준 캡처: <경로 + 본 것 | 신규> · 표식: <바뀌어야 할 것>
- 반영 확인: <표식이 바뀐 재캡처 경로 | 시도: 새로고침 → 서버 다시 띄우기 → wasm-build>
- 증거: <실행 명령 + 출력 인용 / 캡처에서 지목한 구체 요소>
- 캡처 점검: 넘침 · 글리프 · 칩·뱃지와 줄 모양 · 디버그 겹침 — 각각 없음 | 걸림
- 실행/스킵 카운트: <passed N · skipped M · 0 이면 사유>
- 공허 증거 배제: (a) 양성대조 O/N.A · (b) 테스트 수 N · (c) skipped M · (d) baseline 지목 O/N.A
- 대조: <의도한 변경만 | 의도 외 변경 → self-reject N 회 (최대 3)>
- 미검증: N 건 [항목 — 막는 것 — 시도한 우회 — 통제 불가 사유 — 재검증 명령]
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
- `react-kit/skills/react-run/SKILL.md` — `dev` 포트 Gotcha (포트가 찼을 때)
- flutter-toolkit `references/visual-evidence-protocol.md` · design-kit `references/visual-change-protocol.md` — 같은 숫자를 쓰는 형제 규약
- [Vite — `server.port` · `server.strictPort`](https://vite.dev/config/server-options.html#server-port) — 지정 포트가 차 있으면 다음 빈 포트로 옮기고, `strictPort` 면 멈춘다 (§2 반영 확인)
- [Tauri — Vite 설정](https://v2.tauri.app/start/frontend/vite/) — `devUrl` 과 `port` · `strictPort: true` 를 함께 두고 고정 포트를 기대한다
- [Testing Library — About Queries](https://testing-library.com/docs/queries/about/) — `queryBy` `null` / `queryAllBy` `[]` 반환 (§3 a)
- [Vitest CLI](https://vitest.dev/guide/cli.html) — 플래그 목록 (§3 b, c)
- [Vitest — `passWithNoTests`](https://vitest.dev/config/passwithnotests) — Type `boolean` · Default `false` (§3 b)
- [Vitest — `allowOnly`](https://vitest.dev/config/allowonly) — Type `boolean` · Default `!process.env.CI` (§3 c)
- [Playwright — Visual comparisons](https://playwright.dev/docs/test-snapshots) — `toHaveScreenshot()` baseline 기록 · `--update-snapshots` · `maxDiffPixels` (§3 d)
- [Playwright — Assertions](https://playwright.dev/docs/test-assertions) — auto-retrying assertion 권장 · `expect.poll` / `expect.toPass` (§2 R1)
