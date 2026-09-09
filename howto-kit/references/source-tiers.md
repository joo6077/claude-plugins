# 출처 등급제 (Provenance Tier)

**"검증 불가 → 침묵" 의 대체물이다.** 정직성이 요구하는 것은 침묵이 아니라 등급 표시다.

## 4 등급

| 등급 | 의미 | 표기 | 허용되는 문장 |
| --- | --- | --- | --- |
| `관측` | 사용자가 지금 화면을 읽어줬거나 스크린샷을 줬다 | 표기 생략 (최고 등급) | 무엇이든 단정 가능 |
| `문서` | 공개 1 차 출처에 그 라벨이 실제로 적혀 있다 | `출처: <URL> (조회 YYYY-MM-DD)` | 라벨·경로·필드명 단정 가능 |
| `추정` | 출처에 없고 모델 지식 기반 | `[추정]` **표기 필수** | 단정 금지. "대개 …에 있습니다" |
| `없음` | 확인 실패 | `[미확인]` + 시도한 URL | 이때만 전역 검색어로 우회 |

## 핵심 규칙

**`추정` 은 금지 대상이 아니라 라벨 대상이다.** 출처가 다른 정보를 같은 등급으로 섞어 파는 것이
부정직이지, 등급을 붙여 파는 것은 부정직이 아니다.

기존 킷(`onboarding-kit`)이 만든 결함이 정확히 이 지점이다 — "fetch 하지 않은 Step 은 쓰지 않는다"
와 "문서에 있는 상위 섹션명까지만 확정한다" 두 규칙의 곱으로, 남는 문장이
**"`<섹션명>` → 이 섹션에서 찾으세요"** 하나가 됐다. 검증 불가를 생성 금지로 번역한 결과다.

## 상한 — `추정` 40%

한 절차에서 `추정` 이 **액션 스텝의 40% 를 넘으면** 그대로 내보내지 않는다. 셋 중 하나를 한다:

1. 화면 폐루프로 사용자에게 지금 보이는 항목을 물어 `관측` 으로 승격 (§아래)
2. `미확인` 으로 강등하고 전역 검색어로 우회
3. 절차 범위를 확정 가능한 구간까지로 좁히고, 나머지는 사용자 확인 후 이어간다

게이트 G6 이 이 비율을 기계 판정한다 — `../scripts/howto-gate.sh`.

## 등급 승격 사다리

```text
없음(미확인)  ──조회 성공──▶  문서  ──사용자가 화면을 읽어줌──▶  관측
     ▲                          ▲
     │                          │
  추정 ────────────────────────┘   (추정은 조회로만 문서가 된다. 반복 서술로는 안 된다)
```

**모델 지식은 절대 `문서` 가 되지 않는다.** `문서` 등급은 도구 호출 기록이 있어야 성립한다.
실측 사고: `web_search_requests: 0, web_fetch_requests: 0` 인 상태에서 "공식 docs 에서 검증했다"고
주장한 건이 있다. 조회했다는 주장은 **호출과 그 출력**으로만 성립한다.

## 화면 폐루프 (Screen-in-the-loop)

로그인 뒤 화면은 도구로 못 본다. **하지만 사용자는 지금 그 화면을 보고 있다.**
MD 생성 전용이던 기존 킷에서는 쓸 수 없던 채널이다.

1. `문서` 등급으로 확정 가능한 지점까지 **끊지 않고** 안내한다.
2. 거기서 **한 번만** 묻는다 — "지금 그 화면에 보이는 항목을 그대로 읽어 주세요(또는 스크린샷)."
3. 사용자가 읽어준 라벨은 `관측` 등급으로 승격하고 **세션 내에서 재사용**한다.
   같은 콘솔에서 다시 묻지 않는다.

되묻기를 늘리는 것처럼 보이지만 실제로는 줄인다 — 지금은 사용자가 못 찾아서 되묻는 왕복이 더 많다.

## deprecation 3 단계 — 출처보다 강한 주장 금지

| 단계 | 정의 | 출처 |
| --- | --- | --- |
| deprecated | *"no longer in active development as of the deprecation date"* — **호출은 아직 된다** | Amazon SP-API |
| sunset / maintenance | *"should plan to migrate … typically 12 months"* | AWS service lifecycle |
| removed / shutdown | *"calls to the resources fail as of the removal date"* / *"completely removed"* | Amazon SP-API, AWS |

Google Cloud 는 *"After a service, feature, or product is officially deprecated, it continues to be
available for at least the period of time defined in the Terms of Service."* 라고 명시한다.

**`권장하지 않음` ≠ `deprecated` ≠ `제거됨`.** `권장하지 않음` 을 `deprecated` 로 승격시키는 것은
날조다. 1 차 출처가 deprecated 라고 말하지 않은 것을 deprecated 로 쓰지 마라.

한국어 1 차 출처는 `지원 종료` · `폐지` · `중단` · `서비스 종료` 로 쓴다. 게이트 G4 는 영문 토큰과
한국어 토큰을 **양쪽 다** 인식한다 (기존 킷의 G4 는 `[Dd]eprecat` 영문 토큰에만 묶여 있어 한국어
1 차 출처를 근거로 인정하지 못했다).

## 적용 범위 스탬프

절차 헤더에 **버전 · 지역 · 언어**를 적는다. 같은 문서 안에서 경로가 버전별로 갈리는 것이 정상이다.

> *"Select Start > Settings > Apps > Advanced app settings."* (Windows 11)
> *"Select Start > Settings > Apps > Apps & features."* (Windows 10)
> — support.microsoft.com, 같은 문서 안의 두 경로

문서의 **최종 수정일**을 확인한다. 표기 형태는 문서마다 다르다 —
`Last updated YYYY-MM-DD UTC` (Google Cloud) · `Last modified Month D, YYYY` (Google 약관) ·
`Updated N days ago` (Amazon Developer Docs).
