# 정적 뷰어 스펙 — `.api/ui.html`

`/api-ui` 가 생성하는 단일 HTML 의 구조 정본. 확정 시안 `.mockups/api-ui-v7.html` 의 실측을 옮긴
것이며, 시안과 이 문서가 어긋나면 **시안이 정본**이다.

---

## 1. 하드 제약

| 항목 | 값 | 위반 시 |
|------|-----|---------|
| 외부 스크립트 `<script src` | 0 | `file://` · 에어갭에서 열리지 않음 |
| 외부 스타일시트 `<link rel="stylesheet"` | 0 | 〃 |
| `fetch(` · `XMLHttpRequest` · `WebSocket` · `EventSource` · `sendBeacon` | 0 | 리포트 열람이 관측 대상 시스템에 영향을 준다 |
| 외부 폰트 · 이미지 · 미디어 URL | 0 | 오프라인에서 레이아웃이 무너진다 |
| 시크릿 원문 | 0건 | 리포트 공유가 곧 자격증명 유출 |
| 단일 스냅샷 본문 | ≤ 256KB | 인라인 파싱·메모리 부담 |
| HTML 전체 | 10MiB 초과 warning · 50MiB 초과 split | 〃 |
| 클릭 타깃 | ≥ 44px | 확정 시안 실측 기준 |
| 텍스트 대비 | 일반 4.5:1 · large 3:1 · UI component 3:1 | WCAG 2.2 |
| 테마 | 라이트·다크 양립 | 〃 |

**웹폰트를 링크하지 않는다.** `--font-ui` 는 `"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI",
"Pretendard", "Noto Sans KR", sans-serif` 처럼 **설치돼 있으면 쓰고 없으면 시스템 폰트로 떨어지는**
스택으로만 선언한다. `@font-face` 도 `fonts.googleapis.com` 링크도 넣지 않는다.

### CSP `<meta>`

```html
<meta http-equiv="Content-Security-Policy"
      content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'">
```

`script-src`/`style-src` 는 `default-src` 로 폴백하므로 인라인 `<style>`·`<script>`·`style=` 속성을
쓰는 이 뷰어에서는 `'unsafe-inline'` 이 필수다. `default-src 'none'` 만 넣으면 페이지가 통째로 죽는다.
`frame-ancestors` · `sandbox` · `report-uri` 는 `<meta>` 로 적용되지 않으므로 여기에 적지 않는다.

---

## 2. 문서 골격

```text
<!DOCTYPE html>
<html lang="ko" data-theme="light">
  <head>
    meta charset · viewport · CSP
    <title>api-kit · 계약 뷰어 — {프로젝트명}</title>
    <style> TOKENS → RESET → COMPONENTS → RESPONSIVE </style>
  </head>
  <body>
    #app-shell    ├ header  (환경 · 토큰 미터 · 요약 칩 · 테마)
                  ├ #main   ├ aside  (팔레트 런처 · 트리)
                  │         └ section (#ws-head · #panes ├ 요청 pane
                  │                                      ├ resizer
                  │                                      └ 응답 pane)
                  └ footer  (status bar)
    .pal          커맨드 팔레트 (hidden)
    #toast        role=status aria-live=polite
    <script> ICONS → DATA → STATE → RENDER → BIND </script>
  </body>
```

id 는 충돌 방지용 3~4자 접미사를 붙인다(`#topbar-3f2`, `#endpoint-tree-a91`). 접미사 값 자체는
의미가 없고 재생성 시 바뀌어도 된다 — 단, 같은 파일 안에서 JS 셀렉터와 반드시 일치해야 한다.

---

## 3. 영역별 스펙

### 3.1 상단바

| 요소 | 동작 |
|------|------|
| 사이드바 토글 | ≤880px 에서 드로어 열기. `aria-expanded` · `aria-controls` |
| 환경 선택기 | `role=menu` 팝오버. 각 항목에 env dot · id · baseUrl · 설명 · read-only 여부. `↑↓ Home End` 지원 |
| 토큰 만료 미터 | `role=progressbar` + `aria-valuenow`. 남은 시간 `mm:ss`. 프로파일 이름은 `title` 로. **토큰 값은 절대 표시하지 않는다** |
| 요약 칩 | PASS / FAIL / 미실행 3개. 클릭하면 트리를 그 상태로 필터. 활성 칩 재클릭 시 해제 |
| 테마 토글 | `data-theme` 속성 전환. 라벨은 전환 대상(다크 모드로 전환)으로 쓴다 |

### 3.2 사이드바 — 엔드포인트 트리

- 마크업은 **accordion** 이다. `nav > ul > li > button`. `role=tree`/`treeitem` 을 쓰지 않는다.
- 그룹 헤더: 이름 · 엔드포인트 수 · 접힘 chevron. 그룹 단위 `aria-expanded`.
- 엔드포인트 행: 메서드 배지(`data-m="GET"`) · **경로 전문**(말줄임 금지, wrap 허용) · 상태 아이콘.
- 상태 아이콘 3종: `pass` · `fail` · `pending(미실행)`. 아이콘만으로 구분하지 말고 `aria-label`/텍스트를 함께 준다.
- 헤더에 `엔드포인트 N` 카운트와 `모두 접기` 버튼.
- 필터(요약 칩 · 팔레트 스코프)로 결과가 0이면 빈 상태 + `필터 초기화` 버튼을 낸다.

### 3.3 요청 pane

탭 3종 — `파라미터` · `헤더` · `인증`. `role=tablist` + roving tabindex + `←→ Home End`.

| 탭 | 내용 |
|----|------|
| 파라미터 | path 파라미터 → 쿼리 파라미터 순. 각 행에 이름 · 타입 · 값 입력 · 설명. `enum` 타입은 값 pill 로 빠른 선택 |
| 헤더 | 인벤토리 헤더 + 사용자가 더한 헤더 |
| 인증 | 프로파일 이름 · 방식 · 만료까지 남은 시간 · 주입 위치. **값은 마스킹된 채로만** |

**행 추가(§11.11 필수)**

| 추가 대상 | UI | 커맨드 반영 |
|-----------|-----|-------------|
| 쿼리 파라미터 | `파라미터` 탭 하단 `+ 파라미터 추가` | `--query name=value` |
| 헤더 | `헤더` 탭 하단 `+ 헤더 추가` | `--header 'Name: value'` |
| JSON 본문 | 본문 없는 엔드포인트에 `+ 본문 추가` | `--body '{...}'` (+ `Content-Type: application/json` 자동) |

추가분은 엔드포인트별로 따로 산다(`state.extra[epId]`). 빈 이름 행은 커맨드에서 제외한다.

### 3.4 커맨드 바

요청 pane 하단 고정. 구성은 `커맨드 코드 블록` + `복사` 버튼 + `aria-live` 상태 라인이다.

문법:

```text
/api-probe <endpointId> [--env <env>] [--path k=v]... [--query k=v]... [--header 'K: V']... [--body '<json>'] [--record]
```

규칙:

- 기본 환경(`dev`)이면 `--env` 를 붙이지 않는다.
- 값이 빈 문자열인 파라미터는 제외한다.
- `--body` 는 JSON 을 파싱해 compact 직렬화한다. 파싱 실패면 `--body <JSON 구문 오류>` 를 표시하고 복사를 막는다.
- 상태가 `미실행` 이면 `--record` 를 붙인다.
- **prod tier + 비-GET 이면 커맨드를 만들지 않는다.** 코드 블록에 차단 메시지, 복사 시도에 토스트.
- 복사 경로는 함수 하나만 둔다. 여러 경로를 만들면 차단 규칙이 새는 구멍이 생긴다.
- 커맨드가 잘리면 잘림을 시각 신호로 노출한다(`data-clipped`).
- `aria-live` 는 커맨드 전문을 매 타자마다 낭독하지 않는다 — 300ms 디바운스 후 "커맨드 갱신됨" 만 알린다.

### 3.5 응답 pane

탭 구성 (순서 고정):

```text
[실패 원인]  ← state === 'fail' 일 때만, 맨 앞
본문
헤더
타이밍
```

`구조 diff` 탭은 **만들지 않는다**. `미실행` 상태면 탭 대신 `상태` 단일 탭 + 빈 상태(무엇을 실행하면
채워지는지 안내 + 커맨드 복사 유도)를 보여준다.

상단 스트립: 상태 코드 pill(4xx/5xx 는 danger) · 소요 ms · 응답 크기 · 기대값(실패 시 `expected`).

#### 본문 탭 — 2블록 구조

```text
┌ 툴바 ─ 모두 펼치기 · 모두 접기 · [변경 표시] 스위치 · 본문 복사
├ ① JSON 본문
│    값 그대로 · 접기 · 구문 강조 · 타입 배지 · 필수 필드 빨간 *
│    pin 걸린 경로에 pin 아이콘 + assertion 툴팁
│    sentinel 값은 배경을 달리하고 "정규화됨" 힌트
│    인라인 diff: 좌측 거터 + − ~ · 행 배경 틴트 · 삭제 필드는 취소선 유령 행
└ ② 데이터 구조 표
     필드 · 타입 · 필수 · 설명 (4열)
     변경 표시가 켜져 있으면 같은 마크(+ − ~)와 틴트가 행에도 붙는다
     pin 이 있으면 경로 옆에 pin 아이콘 + assertion 문자열
     헤더에 `필드 N개 · 설명 M개`
```

**한 행에 값과 스키마를 같이 넣지 않는다.** 1280px 에서 값이 죽는다(폐기된 설계).

#### 헤더 탭

응답 헤더 key/value 목록. 매 호출 변하는 헤더(`x-request-id` · `date`)는 sentinel 로 치환된 채 표시하고
정규화 표시를 붙인다. 요청 헤더는 요청 pane 소관이라 여기 넣지 않는다.

#### 타이밍 탭

세그먼트 5구간 — DNS 조회 · TCP 연결 · TLS 핸드셰이크 · 서버 처리(TTFB) · 본문 다운로드. 색은 토큰에서
가져오고, 그린 계열끼리 붙지 않게 TLS 는 sage(`--seg-tls`)를 쓴다. 막대 + 숫자(ms)를 같이 준다.

#### 실패 원인 탭

위반 항목을 카드로 나열한다. 각 카드는 `제목` · `기대값 / 실제값` 또는 `경로` · `설명` 을 갖는다.
pin 이 깨졌으면 어떤 assertion 이 왜 실패했는지 문장으로 적는다. "실패했습니다" 만 적힌 카드는 만들지 마라.

### 3.6 분할 리사이저

`role=separator` · `aria-orientation` · `tabindex=0`. `←→↑↓` 로 2%씩, `Home` 으로 기본값 복귀.
가로 배치 기본 40%(요청) / 세로 배치 기본 45%. 응답이 데이터 구조 표까지 품으므로 응답 쪽을 넓게 준다.

### 3.7 커맨드 팔레트

- 열기: `⌘K` · `Ctrl+K` · `/` (입력 요소에 포커스가 있을 때는 `/` 를 가로채지 않는다)
- 이동 `↑↓` · 선택 `↵` · 닫기 `Esc` · 스코프 해제 `⌫`(입력이 비어 있을 때)
- 스코프 4종

  | id | 라벨 | 대상 |
  |----|------|------|
  | `fail` | 실패한 엔드포인트만 | `state === 'fail'` |
  | `recent` | 최근 실행 | `RECENT` 순서 유지 |
  | `pin` | 추가 검사가 걸린 엔드포인트 | `pins.length > 0` |
  | `help` | 단축키 도움말 | `HELP_KEYS` |

- 액션도 같은 목록에 섞는다 — 커맨드 복사 · 테마 전환 · 변경 표시 토글 · 환경 전환 · 그룹 모두 접기 · 필터 초기화
- fuzzy 매칭 결과는 매치 구간을 하이라이트한다
- `role=listbox` + `aria-activedescendant`, 닫을 때 이전 포커스로 복귀

### 3.8 status bar

base URL · read-only 배지(prod)만 둔다. 여기에 토큰·프로파일 값을 노출하지 않는다.

---

## 4. 데이터 모델

생성 시점에 아래 형태로 인라인한다. JSON 데이터 블록으로 넣을 때는 `<`, `</script`, `<!--` 를 escape 한다.

```js
const ENVS = [
  { id:'dev', base:'https://dev.api.example.com', label:'개발 · 프로브 실행 가능', ro:false },
  { id:'prod', base:'https://api.example.com',    label:'프로덕션 · 쓰기 메서드 차단', ro:true }
];

const GROUPS = [
  { id:'orders', name:'orders', eps:['orders.list','orders.get'] }
];

const EP = {
  'orders.list': {
    method:'GET', path:'/v1/orders',
    state:'pass',            // 'pass' | 'fail' | 'pending'
    contract:'partial',      // 'partial' | 'pin' | 'full'
    pins:[{ p:'$.meta.total', c:'≥ $.data 길이' }],
    resp:{ code:200, text:'OK', ms:340, size:'12.4KB', expected:'200 OK' },
    pathParams:[{ name:'orderId', type:'string', value:'ord_1', desc:'주문 식별자' }],
    params:[{ name:'status', type:'enum', enum:['active','shipped'], value:'active', desc:'상태 필터' }],
    reqBody:{ /* 요청 본문 (있을 때만) */ },
    body:{ /* 마스킹·정규화된 응답 본문. sentinel 은 S(token, hint) 형태 */ },
    timing:[['DNS 조회',12,'var(--info)'], /* ... */],
    violations:[{ title:'상태 코드 불일치', exp:'200 OK', act:'503 Service Unavailable', note:'...' }],
    diff:[
      { k:'add', path:'$.data[].items[].discountRate', note:'새 필드 · 타입 number' },
      { k:'rm',  path:'$.data[].items[].legacyCode',   note:'이전 스냅샷에 있던 string 필드가 사라졌습니다' },
      { k:'chg', path:'$.meta.total',                  note:'타입 변경 string → number' }
    ]
  }
};

const SCHEMA = {
  'orders.list': {
    '$.data[].status': { req:true,  t:'enum', d:'active · shipped · cancelled 중 하나' },
    '$.data[].items[].legacyCode': { req:false, t:'string', removed:true, d:'직전 스냅샷 이후 사라졌다' }
  }
};

const RECENT = ['orders.list','orders.get'];
```

### sentinel

정규화로 치환된 값은 `{ __s: '<TS>', hint: 'ISO 8601 · 정규화됨' }` 형태로 넣는다. 렌더러는 이 값을
일반 문자열과 다르게 칠하고 힌트를 툴팁으로 붙인다. **마스킹된 시크릿도 같은 형태**를 쓴다
(`<TOKEN>` · `<SECRET>` · `<REQID>`).

### SCHEMA 에 무엇을 적는가

타입은 실제 값에서 유도하므로 적지 않는다. 여기에는 **값만 봐서는 알 수 없는 것**만 적는다.

- `req` — `true`(필수) / `false`(옵션) / `null`(미확정)
- `t` — `enum`, `date-time` 처럼 값 모양으로 구분되지 않는 의미 타입만
- `removed` — 응답에는 없지만 계약에는 남아 있는 필드(유령 행으로 렌더)
- `d` — 사람이 읽는 설명

### state (런타임)

```js
const state = {
  env, selected, query, statusFilter,
  reqTab, respTab,                 // 'params'|'headers'|'auth' / 'fail'|'body'|'headers'|'timing'|'empty'
  openGroups, formValues, extra,   // extra: epId -> { params:[{n,v}], headers:[{n,v}], body:null|string }
  split, splitV, drawer, diffOn,
  palOpen, palScope, palIndex, palRows
};
```

---

## 5. 인라인 diff 규격

| 종류 | 거터 | 렌더 |
|------|------|------|
| 추가 (`add`) | `+` | 행 배경 틴트(성공 계열) |
| 삭제 (`rm`) | `−` | **취소선 유령 행** — 실제 응답에는 없지만 계약에 남은 필드 |
| 변경 (`chg`) | `~` | 행 배경 틴트(경고 계열) + 변경 요약(`string → number`) |

- `변경 표시` 스위치(`role=switch`)로 전체 on/off. 끄면 거터·틴트·유령 행이 모두 사라진다.
- 배열 경로는 `$.data[].items[].sku` 처럼 인덱스를 지우고 표기한다. `microdiff` 는 배열 원소 이동
  인식이 약하므로 index 기반 잡음이 보이면 그 사실을 뷰어에 적고 계약 쪽에서 정렬 정규화를 건다.
- 거터 기호만으로 구분하지 말고 `aria-label`(추가된 필드 / 제거된 필드 / 변경된 필드)을 함께 준다.
- **잘라낸 본문 구간에는 거터를 그리지 않는다** — 미측정 구간이지 무변경 구간이 아니다.

---

## 6. 디자인 토큰

확정 시안 실측값. 값이 아니라 **역할**로 참조한다 — 하드코딩 색을 컴포넌트에 직접 쓰지 마라.

| 축 | 값 |
|----|-----|
| spacing | 4 · 8 · 12 · 16 · 20 · 24 · 28 · 32 · 40 · 48 |
| radius | 6 · 8 · 10 · 14 · 999 |
| type | 12 / 13 / 14 / 15 / 17 / 21 (line-height 1.3 · 1.6) |
| accent | `#457335` (Forest Canopy primary-600) · hover `#375d2c` · lite `#74a85f` |
| semantic | ok `#047857` · danger `#b91c1c` · warn `#92400e` · info `#0f766e` (각 soft/line 쌍) |
| method | GET teal · POST green · PATCH amber · DELETE red (배경/전경 쌍) |
| json | key(진한 그린) · string(teal) · number(amber) · bool(sage) · null/punc(회색) · sentinel(중립 배경) · pin(앰버 배경) |

주의:

- 밝은 회색 텍스트(`#909399`)는 흰 배경에서 3.4:1 이라 본문에 쓸 수 없다. 3차 텍스트는 4.5:1 을 넘는 값으로 내린다.
- olive 계열(`#a4ac86`)은 흰 배경 2.1:1 이라 텍스트로 쓸 수 없다. bool 은 sage 계열로 간다.
- JSON 구문 강조에 보라·인디고를 섞지 않는다. 팔레트 안에서만 구분한다.
- 다크 테마는 `@media (prefers-color-scheme: dark)` + `:root:not([data-theme="light"])` 로 두고,
  명시 토글은 `:root[data-theme="dark"]` 로 덮는다. 양방향 모두 토글이 이겨야 한다.

---

## 7. 반응형

| 브레이크포인트 | 변화 |
|----------------|------|
| ≤ 1180px | 상단바 부가 정보 축약 |
| ≤ 1120px | 데이터 구조 표 열 폭 재배분 |
| ≤ 1024px | 요청/응답 분할 비율 조정 |
| ≤ 880px | 좌우 2패널 → **상하 스택**, 사이드바는 드로어 + scrim |
| ≤ 760px | 상단바 요약 칩 축약 |
| ≤ 880px & ≤ 600px 높이 | 세로 여백 축소 |

`prefers-reduced-motion: reduce` 에서 전환 애니메이션을 끈다.

---

## 8. 접근성 체크리스트

- 탭·메뉴·리스트박스에 `role` + roving tabindex + 방향키·Home·End
- 모든 상태 아이콘에 텍스트 대응물(`PASS` · `FAIL` · `미실행`)
- 복사·토글 결과는 `role=status` `aria-live=polite` 로 알린다. 긴 문자열 전문을 낭독시키지 않는다
- 포커스 링을 지우지 않는다. 커스텀 포커스 색은 대비 3:1 이상
- 드로어를 열면 scrim 을 깔고 `Esc` 로 닫는다
- 200% 확대에서 정보 손실 없음

---

## 9. 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| CDN 스크립트/스타일을 불러와야 열리는 리포트 | 오프라인·에어갭에서 안 열리고, CDN 변조가 리포트 내용을 바꾼다 |
| `fetch('./data.json')` 사이드카 | `file://` opaque origin 때문에 빈 화면이 된다 |
| raw body 를 `innerHTML` 로 렌더 | 대상 API 문자열이 열람자 브라우저에서 실행된다 |
| 경로에 `text-overflow: ellipsis` | 식별자가 잘려 무엇을 보는지 알 수 없다 |
| JSON 행 안에 스키마 열 | 1280px 에서 값이 통째로 사라진다 |
| `구조 diff` 탭 추가 | 같은 정보가 두 곳에 생겨 정본이 흐려진다 |
| 사이드바 검색창 + 팔레트 병존 | 입구가 둘이면 정본이 둘이다 |
| 복사 경로를 여러 개 만들기 | prod 쓰기 차단이 한쪽에서 샌다 |
| `Authorization` 이 그대로 들어간 curl 복사 | 리포트 공유가 곧 자격증명 유출이다 |
| redacted 뷰만 있고 raw·정규화·diff 단계가 없음 | 판정 근거를 재현할 수 없어 결론만 남은 종이가 된다 |

---

## References

- `.mockups/api-ui-v7.html` — 확정 시안(정본)
- `docs/api/verification/static-evidence-viewer-contract.md` — 뷰어 계약 원칙 10 · 수치 기준
- `docs/superpowers/specs/2026-09-02-api-kit-design.md` §11.1~§11.11 — 설계 근거
- `../../../references/api-layout.md` — 입력이 되는 `.api/` 레이아웃
