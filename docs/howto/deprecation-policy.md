# deprecation 정책 — 출처보다 강한 주장을 막는 단계 구분

`last_updated: 2026-09-10`

절차 문서가 "이 방식은 지원 종료됐다" 고 쓸 때, 그 주장이 1 차 출처보다 강하면 날조다.
`권장하지 않음` 을 `deprecated` 로, `deprecated` 를 `제거됨` 으로 올리는 것이 전형적인 형태다.

설계 브리프 §11-4 가 이 항목을 확인 실패로 남겨 뒀었다 — Google Cloud 와 Apple 의 동등한 정의를
확보하지 못했다는 것이다. 이번 사이클이 그중 **Google Cloud 를 해소**했고 **Apple 은 여전히
확인 실패**다.

---

## 1. 3 단계 — 각 단계에 1 차 출처가 있다

조회일 **2026-09-10**.

| 단계 | 정의 원문 | 출처 |
| --- | --- | --- |
| **deprecated** | *"Deprecated indicates that the resource is no longer in active development as of the deprecation date."* — **호출은 아직 된다** | Amazon SP-API — developer-docs.amazon.com/sp-api/docs/sp-api-deprecations |
| **sunset / shutdown** | *"Sunset services have a sunset time line (typically 12 months). The sunset date is the date AWS will end operations and support of the service."* | AWS — docs.aws.amazon.com/general/latest/gr/sunset_services.html |
| **removed** | *"Removed indicates that calls to the resources fail as of the removal date."* | Amazon SP-API — 같은 문서 |

Google Cloud 도 같은 전이를 문장으로 정의한다 — 이번에 확인했다.

> *"After a service, feature, or product is officially deprecated, it continues to be available for
> at least the period of time defined in the Terms of Service. **After this period of time, the
> service is scheduled for shutdown.**"*
> — docs.cloud.google.com/service-usage/docs/deprecations (조회 2026-09-10)

그리고 출시 단계 정의에서 removed 까지 잇는다.

> *"Deprecated — Deprecated features are scheduled to be shut down and removed."*
> — cloud.google.com/products (조회 2026-09-10)

**`권장하지 않음` ≠ `deprecated` ≠ `제거됨`.** 1 차 출처가 deprecated 라고 말하지 않은 것을
deprecated 로 쓰지 마라.

---

## 2. 통지 기간 — 약속과 관행은 다르다

두 벤더 모두 "12 개월" 이라는 숫자를 쓴다. 그런데 **강도가 다르다.**

| 벤더 | 문장 | 성격 |
| --- | --- | --- |
| Google Cloud | *"Google will notify Customer **at least 12 months** before: (i) discontinuing any Service (or associated material functionality) unless Google replaces such discontinued Service or functionality…"* | **약관상 약속** — 조건절이 붙어 있다 |
| AWS | *"Sunset services have a sunset time line (**typically 12 months**)."* | **관행 서술** — 약속이 아니다 |

절차 문서가 이 둘을 같은 강도로 쓰면 안 된다.

- Google Cloud → "최소 12 개월 전 통지가 약관에 명시돼 있습니다" 라고 쓸 수 있다.
  단, **대체 서비스를 제공하는 경우는 예외**라는 단서까지 함께 적어야 한다.
- AWS → "보통 12 개월" 이라고만 쓴다. "12 개월이 보장됩니다" 는 **출처보다 강한 주장**이다.

출처: cloud.google.com/terms · docs.aws.amazon.com/general/latest/gr/sunset_services.html
(둘 다 조회 2026-09-10)

---

## 3. 한국어 공식 용어 — 매핑이 직관과 다르다

Google Cloud 한국어 문서는 영문 용어를 이렇게 옮긴다.

| 영문 | 한국어 공식 표기 |
| --- | --- |
| Deprecated | **지원 중단됨** |
| shut down | **서비스 종료** |
| removed | **삭제** |

> *"지원 중단됨 — 지원 중단된 기능은 서비스 종료 및 삭제가 예정된 기능입니다."*
> — cloud.google.com/products?hl=ko (조회 2026-09-10)

국내 서비스도 `지원 종료` 를 쓴다.

> *"단축URL 지원 종료 안내 — 단축 URL 기능의 지원이 2024년 11월 28일(목) 부로 종료됩니다."*
> — developers.naver.com/products/service-api/shortenurl/shortenurl.md (조회 2026-09-10)

**`deprecated` 를 한국어로 옮길 때 `지원 종료` 를 쓰면 한 단계 올려 말하는 것이다.** Google Cloud
기준으로 `지원 종료` 에 대응하는 영문은 shut down 이고, deprecated 는 `지원 중단됨` 이다.

---

## 4. G4 게이트의 false negative — 이번에 고쳤다

§3 의 매핑이 게이트 결함을 드러냈다. `howto-gate.sh` 의 deprecation 토큰 목록에 **`삭제` 계열이
없었다.** 그래서 한국어 1 차 출처를 그대로 옮긴 `삭제 예정` 주장은 **근거가 없어도 통과**했다.

3 방향 대조로 확인했다.

```text
수정 전
  근거 없는 "삭제 예정" 주장   G4_DEPRECATION PASS unsourced_claims=0   ← 놓친다

수정 후 (토큰 '삭제 예정|삭제가 예정' 추가)
  근거 없는 "삭제 예정" 주장   G4_DEPRECATION FAIL unsourced_claims=1   ← 잡는다
  같은 주장 + 출처 뒷받침      G4_DEPRECATION PASS unsourced_claims=0
  정상 "계정을 삭제한다" 절차   G4_DEPRECATION PASS unsourced_claims=0
```

**`삭제` 를 단독 토큰으로 넣지 않은 이유**가 세 번째 줄이다. 단독으로 넣으면 계정 삭제·파일
삭제 같은 **정상 액션이 deprecation 주장으로 오탐**된다 — 실측 `unsourced_claims=2`. 좁은
형태(`삭제 예정` · `삭제가 예정`)만 넣어야 양성만 잡고 정상 절차는 통과한다.

세 케이스는 `howto-kit/evals/fixtures/` 에 픽스처로 커밋했고 `evals.json` 에 등록했다
(`E10` · `E11` · `E12`).

---

## 5. 단계별로 절차 문서에 뭐라고 쓰나

같은 기능이라도 **지금 어느 단계인가**에 따라 사용자가 할 일이 다르다. 단계를 올려 말하면 아직
쓸 수 있는 것을 못 쓰게 만들고, 내려 말하면 곧 깨질 것을 계속 쓰게 만든다.

| 단계 | 지금 상태 | 절차 문서에 쓸 문장 | 사용자가 할 일 |
| --- | --- | --- | --- |
| deprecated | 호출은 **아직 된다**. 신규 개발만 멈춤 | "이 방식은 지원 중단됐습니다. 아직 동작하지만 신규 등록에는 쓰지 마세요." | 새로 만들 때만 피한다 |
| sunset / shutdown | 종료일이 **정해졌다** | "`<날짜>` 에 종료됩니다. 그전에 `<대체>` 로 옮기세요." | 기한 안에 마이그레이션 |
| removed | 호출이 **실패한다** | "이 방식은 제거됐습니다. `<대체>` 를 쓰세요." | 즉시 전환 (선택지 없음) |

**판정 규칙** — 출처 문장에 *날짜*가 있으면 최소 sunset 이다. *"fail" / "removed"* 가 있으면
removed 다. 둘 다 없고 *"no longer in active development"* 계열이면 deprecated 에서 멈춰라.
출처에 없는 단계로 올리지 마라.

---

## 6. Apple — `[미확인]`

Apple 은 **개별 API·기능 종료 공지**는 제공하지만, AWS · Amazon SP-API · Google Cloud 처럼
단계를 정의한 **일반 lifecycle 정책 문서**를 확보하지 못했다.

킷의 처리: Apple 을 단계 정의의 근거로 인용하지 않는다. Apple 절차에서 deprecation 을 말해야
하면 **그 기능의 개별 공지 페이지**를 출처로 달아라. 시도한 URL 은
`howto-kit/references/provenance-notes.md` §8 에 있다.

---

## 7. 검증 함정 4 번째 — 공백 정규화

인용 8 건을 세션 로컬 조회로 대조했다. 그중 **Google Cloud deprecations 인용이 raw 대조에서
MISS** 였다.

> **정정.** 이 사이클은 처음에 그 원인을 HTML 엔티티로 적었다. QA 가 재현되지 않는다고 지적해
> 다시 확인한 결과 **원인이 달랐다.** 엔티티가 아니라 **원문의 줄바꿈과 들여쓰기**였다.

```text
찾은 문자열:  defined in the Terms of Service
응답 본문:    defined in the\n  Terms of Service.
```

HTML 은 줄바꿈과 들여쓰기를 렌더링에서 공백 하나로 접지만, `grep -F` 에는 그대로 남아 있다.
따라서 **문장이 두 줄에 걸치면 리터럴 대조가 실패한다.** 태그를 제거하고 `\s+` 를 공백 하나로
접은 뒤 대조해야 잡힌다.

이제 이 킷이 아는 검증 함정은 **네 가지**다.

| 함정 | 증상 | 대응 |
| --- | --- | --- |
| HTML 엔티티 | `you&#39;re` 가 `you're` 로 안 잡힘 | 엔티티 디코드 후 대조 (`branch-catalog.md` §6) |
| **공백 정규화** | 문장이 줄바꿈으로 갈려 안 잡힘 | 태그 제거 + `\s+` → 공백 하나로 접기 |
| SPA | HTML 이 껍데기뿐 | 문서 데이터 API (`deep-links.md` §3) |
| PDF | 폰트 서브셋으로 정규식 불가 | `pdftotext` 추출 (`provenance-notes.md` §6) |

**공통 규칙은 그대로다** — "문자열을 못 찾았다" 는 확인 실패이지 부재가 아니다. 다만 이번 사례가
하나를 더 가르쳐 준다: **실패 원인을 짚을 때도 그것을 재현해 보고 적어라.** 원인을 잘못 짚으면
다음 사람이 엉뚱한 도구를 쓴다.

## 7.1 잔여 오탐 — 원인은 토큰이 아니라 스캔 범위였다 (2026-09-10 해소)

QA 가 적대적 탐색으로 찾았다. **"30일 지난 데이터를 삭제 예정입니다"** 같은 데이터 보존 정책
문구가 `G4_DEPRECATION FAIL` 로 잡혔다.

**처음에는 토큰이 넓어서라고 봤다. 아니었다.** 카이젠 사이클에서 7 케이스 매트릭스를 돌려
원인을 좁힌 결과, 게이트가 **`- 확인:` 줄까지 주장으로 세고 있던 것**이 원인이었다.

`확인:` 은 **제품이 화면에 띄우는 문구를 관측해 적는 자리**다. 거기 있는 "삭제 예정" 은 저자의
주장이 아니라 **근거**다. 그 줄을 주장 탐지에서 빼자 오탐이 사라졌다.

```text
수정 전   데이터 보존 안내   G4_DEPRECATION FAIL unsourced_claims=1   ← 오탐
수정 후   데이터 보존 안내   G4_DEPRECATION PASS unsourced_claims=0
```

**구멍을 만들지 않았다.** 주장이 스텝 헤더나 다른 필드에 오면 여전히 잡힌다 — 양성 3 종
(`삭제 예정` · `종료 예정` · `지원 종료`, 전부 근거 없음)이 수정 후에도 `FAIL` 이다.

같은 사이클에서 미탐 하나도 메웠다. `종료 예정` 단독형이 토큰 목록에 없어 통과하고 있었다.
**`종료` 단독은 넣지 않았다** — "설치가 종료됩니다" 같은 완료 서술을 오탐한다.

7 케이스는 `howto-kit/evals/fixtures/` 에 전부 픽스처로 있고 `evals.json` 에 등록됐다 (15 케이스).

**교훈**: 오탐을 만나면 토큰부터 손대지 마라. **어느 줄을 세고 있는지** 먼저 보라. 토큰을 좁히면
미탐이 남고 넓히면 오탐이 는다 — 스캔 범위가 틀렸으면 그 균형점이 아예 존재하지 않는다.

---

## 8. 조회 기록

Codex 위임 1 회 (MODE=research · read-only · foreground · 검색 하드캡 20). rollout 로그의
`turn_aborted` 는 0 건으로 정상 완주했다. 기존 4 인용 재확인 · Google Cloud 용어 확보 ·
한국어 1 차 출처 2 건 확보 · Apple 은 확인 실패로 반환했다.

인용 8 건은 전부 응답 본문에서 직접 대조했다 (7 raw HIT · 1 decoded HIT).

미확정 근거의 원장은 `howto-kit/references/provenance-notes.md` 가 정본이다. 확정된 항목은
이 문서가 정본이다.
