---
title: 정적 증거 뷰어 계약
version: 0.1.0
last_updated: 2026-09-04
---

# 정적 증거 뷰어 계약

검증 결과를 사람이 읽는 단일 HTML 리포트가 지켜야 할 제약. 외부 의존 0건, `file://` 직접 열람, 신뢰할 수 없는 응답 본문의 안전한 인라인, 비밀 마스킹을 다룬다. 확정 시안은 `.mockups/api-ui-v7.html` 이다.

---

## 원칙

### 1. Zero Runtime Dependency

뷰어는 외부 참조 0건의 단일 HTML 이어야 한다. 외부 JS/CSS/font/image 를 요구하면 `file://` opaque origin, CDN 장애, supply-chain 변조에 그대로 노출된다. `file://` 문서는 현대 브라우저에서 대체로 opaque origin 으로 취급되므로 같은 폴더의 파일조차 same-origin 으로 가정할 수 없다 — 모든 데이터를 인라인한다.

> **출처:** [MDN Same-origin policy — file origins](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Same-origin_policy#file_origins), [MDN Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Subresource_Integrity)

### 2. No Browser Network Calls

리포트를 열었을 때 `fetch`, XHR, WebSocket, EventSource, beacon, link ping 중 어느 것도 나가면 안 된다. CSP `connect-src 'none'` 으로 이 계층을 명시적으로 차단한다. 증거 리포트가 네트워크를 쓰는 순간, 열람 행위 자체가 관측 대상 시스템에 영향을 준다.

> **출처:** [MDN CSP connect-src](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/connect-src)

### 3. Data-as-Data Embedding

JSON 증거는 실행 스크립트가 아니라 데이터 블록으로 넣는다. `<script type="application/json">` 같은 non-JS MIME 은 브라우저가 실행하지 않고 author script 가 파싱한다. 증거를 JS 리터럴로 넣으면 응답 본문이 곧 실행 코드가 된다.

> **출처:** [HTML Standard — script element](https://html.spec.whatwg.org/multipage/scripting.html#the-script-element), [MDN — embedding data in HTML](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/script#embedding_data_in_html)

### 4. Script-block Escape 규칙

데이터 블록에 넣더라도 신뢰할 수 없는 본문은 그대로 쓰지 않는다. script 요소 내용에는 문법 제약이 있어 `</script` 문자열이 블록을 조기 종료시킬 수 있다. 인라인 전에 `<`, `</script`, `<!--` 세 패턴을 escape 한다.

> **출처:** [HTML Standard — restrictions for contents of script elements](https://html.spec.whatwg.org/multipage/scripting.html#restrictions-for-contents-of-script-elements)

### 5. XSS-safe Rendering

응답 본문은 신뢰할 수 없는 입력이다. raw body 를 `innerHTML` 에 넣지 말고 HTML entity encoding 또는 `textContent` 같은 safe sink 로만 렌더링한다. 대상 API 가 반환한 문자열이 리포트를 여는 사람의 브라우저에서 실행되면 안 된다.

> **출처:** [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)

### 6. Redacted-by-default Rendering

토큰, 쿠키, `Authorization`, API key 는 기본 비표시다. Hurl 이 secrets redaction 을 제공하더라도 raw stdout 과 저장된 응답에는 비밀이 남을 수 있다고 문서가 경고하므로, 뷰어는 자체 redaction 레이어를 따로 갖는다.

> **출처:** [Hurl Secrets](https://hurl.dev/docs/templates.html#secrets), [Hurl Redacting Secrets](https://hurl.dev/docs/capturing-response.html#redacting-secrets)

### 7. Raw / Normalized / Diff 분리

raw evidence, normalize 후 비교 입력, 최종 diff 를 각각 따로 보여준다. Hurl assertion 은 status/header/body/query/predicate 단위로 실패를 설명하므로, 중간 단계를 감추면 "왜 실패로 판정했는가" 를 재현할 수 없다.

> **출처:** [Hurl Asserting Response](https://hurl.dev/docs/asserting-response.html)

### 8. Operation Grouping + Severity Filtering

operation/testcase 단위 그룹핑과 `failure` / `error` / `skipped` 필터를 제공한다. JUnit XML 생태계의 testsuite/testcase 구조와 집계 필드를 그대로 따르면 같은 결과를 CI 대시보드와 뷰어가 동일하게 센다.

> **출처:** [JUnit XML 포맷 레퍼런스](https://github.com/testmoapp/junitxml)

### 9. Copy-safe Reproducer

재현 명령은 복사 가능해야 하지만 비밀은 제거되어야 한다. Hurl 은 `--curl` 로 curl 커맨드를 내보내므로, 뷰어는 마스킹된 curl/hurl 재현 커맨드를 artifact 에 포함한다. 붙여넣기만으로 토큰이 유출되는 경로를 남기지 않는다.

> **출처:** [Hurl Debug Tips — export curl commands](https://hurl.dev/docs/tutorial/debug-tips.html#export-curl-commands)

### 10. Offline Bundle Integrity

단일 HTML 안에 digest manifest 를 넣어 증거의 변조 여부를 확인할 수 있게 한다. SRI 자체는 fetch 된 리소스 검증용이지만, "기대 content 를 해시로 검증한다" 는 운영 원칙은 오프라인 번들에도 그대로 적용된다.

> **출처:** [W3C Subresource Integrity](https://www.w3.org/TR/SRI/), [MDN Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Subresource_Integrity)

---

## 수치 기준

| 항목 | 값 | 근거 |
|------|-----|------|
| CSP 최소 정책 | `default-src 'none'; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'` | [MDN default-src](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/default-src), [MDN connect-src](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/connect-src) |
| 외부 참조 개수 | `<script src` `0` / `<link rel=stylesheet` `0` / `fetch(` `0` / `XMLHttpRequest` `0` | 확정 시안 `.mockups/api-ui-v7.html` 실측 |
| 텍스트 대비 | 일반 `4.5:1` 이상, large text `3:1`, UI component·graphical object `3:1` | [WCAG 2.2](https://www.w3.org/TR/WCAG22/) |
| 텍스트 확대 | `200%` 까지 정보 손실 없음 | [WCAG 2.2](https://www.w3.org/TR/WCAG22/) |
| 클릭 타깃 최소 크기 | `44px` | 확정 시안 `.mockups/api-ui-v7.html` 실측 |
| 테마 | 라이트·다크 양립 (둘 다 대비 기준 충족) | 확정 시안 `.mockups/api-ui-v7.html` 실측 |
| Data URL 길이 한계 | Chromium·Firefox `512MB`, Safari·WebKit `2048MB` (data URL 기준이며 인라인 HTML 전체 한계는 아님) | [MDN data URL length limitations](https://developer.mozilla.org/en-US/docs/Web/URI/Reference/Schemes/data#length_limitations) |
| 해시 알고리즘 | `sha256` 최소, 가능하면 `sha384` 이상 (`sha256` / `sha384` / `sha512`) | [W3C SRI](https://www.w3.org/TR/SRI/) |
| 단일 HTML evidence payload | `10MiB` 초과 warning, `50MiB` 초과 시 split·excerpt 모드 | 추론 — 표준 한계가 아니라 브라우저 parse·메모리·UX 리스크를 줄이는 운영 임계값 |
| redaction 검증 통과 기준 | known secret pattern unredacted match `0건` | 추론 |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| CDN 의 JS/CSS 를 불러와야 열리는 리포트 | 오프라인·에어갭 환경에서 증거가 열리지 않고, CDN 변조가 리포트 내용을 바꾼다 |
| `file://report.html` 에서 sidecar JSON 을 `fetch('./data.json')` 로 로드 | opaque origin 때문에 CORS 로 막혀 리포트가 빈 화면이 된다 |
| raw response body 를 `innerHTML` 로 렌더링 | 대상 API 가 반환한 문자열이 열람자 브라우저에서 실행된다 |
| redacted view 만 있고 raw·normalized·diff 단계가 없음 | 판정 근거를 재현할 수 없어 리포트가 결론만 남은 종이가 된다 |
| "copy curl" 에 `Authorization` 헤더가 그대로 포함 | 리포트를 공유하는 행위가 곧 자격증명 유출이 된다 |

---

## Gotchas

- **`file://` origin 처리는 브라우저마다 다르다** — 한 브라우저에서 로컬 파일 읽기가 되더라도 다른 브라우저에서는 막힌다. "내 크롬에서 열리니까 괜찮다" 는 검증이 아니다. 인라인만이 이식 가능한 유일한 방법이다.
- **`<script type="application/json">` 도 안전하지 않다** — 실행되지 않을 뿐, 본문에 `</script` 가 있으면 블록이 조기 종료되어 이후 마크업이 파서에 노출된다. escape 를 건너뛰지 마라.
- **CSP `<meta>` 는 헤더의 완전한 대체가 아니다** — 정적 HTML 에서 유용하지만 일부 지시어는 `<meta>` 로 적용되지 않는다. `<meta>` CSP 를 넣었다는 사실만으로 네트워크 차단을 보증했다고 보고하지 마라.
- **Hurl secret redaction 은 저장된 raw 응답까지 보증하지 않는다** — 마스킹은 도구 출력 계층의 기능이고, 뷰어가 인라인하는 원본에는 비밀이 남을 수 있다. 마스킹은 리포트 생성 파이프라인에서 한 번 더 수행한다.
