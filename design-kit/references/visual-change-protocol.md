# Visual Change Protocol

> design-kit 내 **시각 산출물을 만들거나 바꾸는 스킬**(design-mockup · design-component · design-concept ·
> design-system · design-guide · design-audit · design-test)이 공유하는 SSOT 다. 각 스킬은 이 문서를 Gotcha 한 줄로 인용하며,
> 여기 정의된 임계값·용어를 자기 문서에서 다시 정의하지 않는다.
>
> **배경 (실측):** 2026-06~07 사용 데이터에서 시각 작업 관련 반복 마찰이 최상위 신호로 올라왔다.
> 승인된 시안 색상을 무시하고 프로젝트 토큰을 적용한 사례, 보더만 요청받고 배경까지 바꾼 사례,
> 빈 화면 캡처를 "정상 렌더링" 근거로 반복 주장해 사용자 신뢰가 손상된 사례가 각각 별개 세션에서
> 발생했다. 공통점은 **무엇을 진실로 삼을지**와 **무엇을 건드리지 않을지**가 규정되지 않았다는 것이다.
>
> **형제 규약과 같은 숫자:** §0 의 「같은 역할 기존 화면 2 개 이상」 과 §3 의 「스스로 고치기 최대 3 회」 는
> flutter-toolkit `references/visual-evidence-protocol.md` Step 0 · Step 2 와 같은 값이다.
> **세 규약(이 문서 · flutter-toolkit visual-evidence-protocol · react-kit render-evidence-protocol)이 같이 쓰는 규칙의 정본은 harness `skill-design-guide.md` 한 절에 두고, 세 규약에는 스택마다 다른 채널 · 도구 · 명령만 남긴다.**
> 그 절은 아직 없다 — 생기기 전까지는 한쪽 값을 바꾸면 다른 쪽도 같이 바꾼다.

---

## 0. 편집 전 확정 — 대상 · 되말하기 · 관례 표

화면이나 화면 요소를 만들거나 바꾸는 요청이면 파일을 만들거나 고치기 **전에** 아래 셋을 응답에 남긴다.
시각 요청은 말만으로 의도가 정해지지 않는다. 실측(`/insights` 2026-09-24 F01 · F02): 평평한 줄 대신 카드를
만들었고, 화면을 보여 달라는 요청에 그 화면으로 가는 칩을 만들었고, 칩 하나만 오른쪽에 고정하라는 말을 줄
전체 고정으로 뒤집었고, 앱에 없는 위젯을 지어냈다.

1. **대상** — 바꿀 화면의 파일 경로와 라우트(웹은 주소, 앱은 화면 파일)를 적는다. 새로 만드는 화면이면
   `신규` 라고 적는다. 화면을 가리키는 요청이면 대상은 그 화면 자체다 — 그 화면으로 들어가는 진입점(버튼·칩)이나
   화면을 흉내 낸 그림이 아니다
2. **되말하기** — 요청을 대상 요소 이름과 배치까지 넣어 한 문장으로 되말한다. 두 갈래로 읽히면 묻고 시작한다
   (예: 「추가 칩만 오른쪽 고정」 과 「줄 전체 오른쪽 고정」)
3. **관례 표** — 앱 코드가 있으면 같은 역할의 서로 다른 기존 화면 **2 개 이상**을 Read 해서 경로와 함께 표로
   남긴다. 칸은 줄 모양(카드인지 평평한 줄인지) · 칩·뱃지 모양 · 아이콘 뜻(닫기·끝내기·접기) · 재사용 부품(실제
   심볼 이름 · `파일:줄` · 한 줄 용도)이다

관례 표의 규칙:

- 재사용 부품은 앱 코드가 실제로 부르는지 grep 으로 확인한다. 시안·카탈로그에서만 쓰이는 부품은 뺀다.
  **코드 검색에서 나오지 않은 부품 이름은 시안·스펙에 쓰지 않는다**
- 관례 일치는 **같은 역할**에만 적용한다. 역할이 다른 화면까지 같은 구조로 맞추지 않는다 — WCAG 2.2 SC 3.2.4 가
  요구하는 것은 같은 기능을 일관되게 식별하는 것이지 모든 화면의 구조를 같게 하는 것이 아니다
  ([WCAG 2.2](https://www.w3.org/TR/WCAG22/)). 그래서 감사 기준 Authenticity 의 레이아웃 변주 규칙(같은 구조 3 회 이상
  반복 금지)과 부딪히지 않는다
- 비교안을 만들면 관례를 §5 매트릭스의 `constants` 에 넣는다. 관례를 벗어나는 안은 사용자가 요청하거나
  승인했을 때만 만든다
- 같은 역할 기존 화면이 2 개 미만이면 찾은 화면을 전부 적고 `관례 없음 — 같은 역할 기존 화면 N 개` 라고 쓴다.
  앱 코드가 아직 없으면 `관례 없음 — 앱 코드 없음` 이다

---

## 1. Visual Source of Truth Precedence — 무엇이 진실인가

시각 값(색상·간격·타이포·형태)이 충돌할 때 아래 **우선순위 위에서 아래로** 따른다. 상위 근거가
존재하면 하위 근거로 덮어쓰지 않는다.

| 순위 | 근거 | 예 |
| ---- | ---- | -- |
| 1 | **사용자가 이번 대화에서 직접 지정한 값** | "이 헥스로 해줘", "지금 색이 맞다" |
| 2 | **사용자가 승인한 시각 결과물** | 브라우저로 띄워 확인한 시안, 확정된 mockup HTML, 승인 기록 아티팩트 |
| 3 | **프로젝트에 이미 존재하는 값** | 기존 앱의 색상 체계, 현재 테마 파일, 실제 사용 중인 토큰 |
| 4 | **프로젝트 디자인 토큰 명세** | `design-tokens.md`, `.design/concept.md` 방향 |
| 5 | **일반 원칙·기본 팔레트** | WCAG 권장, 프레임워크 기본값 |

### 규칙

- **승인된 시안이 있으면 그 시안의 실제 값을 그대로 쓴다.** 팔레트 토큰으로 "정규화" 하거나 단일
  tint 로 치환하지 마라. 토큰화가 필요하다고 판단되면 값을 바꾸지 말고 **토큰을 그 값으로 정의**하라.
- **기존 앱에 이미 색상 체계가 있으면 새 팔레트를 도입하지 마라.** 먼저 기존 값을 열거해 제시하고,
  교체가 필요하다면 이유와 함께 사용자 승인을 받는다.
- 순위 1~3 의 근거를 찾지 못했다고 **가정하지 마라** — 찾을 수 없으면 "찾지 못했다"고 말하고 확인한다.

```text
Bad:  승인된 시안의 #E8965A → 프로젝트 accent 토큰(단일 tint)으로 치환 → "토큰 체계에 맞췄습니다"
Bad:  기존 앱 배경색을 읽지 않고 새 뉴트럴 팔레트 생성 → "배경색이 아직도 이상함"
Good: 승인 시안 값을 그대로 적용 + "이 값을 `color.accent.brand` 토큰으로 등록할까요?" 별도 제안
```

---

## 2. Partial Visual Change Isolation — 무엇을 건드리지 않는가

"보더만", "색만", "간격만" 처럼 **속성 하나를 지목한 요청**은 그 속성만 바꾸라는 뜻이다.

**요소 하나를 지목한 요청**(「이 칩만」, 「추가 버튼만 오른쪽으로」)도 같은 규칙을 따른다. 변경 목록에는 지목된
요소만 올리고, 같은 줄·같은 영역의 이웃 요소는 보존 목록에 올린다. 요소가 두 갈래로 읽히면 §0 되말하기에서
먼저 묻는다.

### 편집 전 (Change Manifest)

편집을 시작하기 전에 두 목록을 명시한다. 문장 다짐이 아니라 **응답에 남는 목록**이어야 한다.

```text
## Change Manifest
- 변경: [속성 — 대상 — 현재값 → 목표값]
- 보존: [같은 요소/영역의 나머지 시각 속성 열거 — background, fill, radius, shadow, spacing, typography 중 해당분 · 요소 하나를 지목했으면 같은 줄·같은 영역의 이웃 요소와 그 자리]
```

보존 목록에 올린 속성은 편집 후에도 값이 같아야 한다. 리팩토링·정리·"김에 개선" 을 이유로 바꾸지 않는다.

### 편집 후 (판정)

- **의도 외 영역이 변했으면 그 변경은 실패로 간주한다.** 되돌린 뒤 요청 속성만 다시 적용한다.
  (예: 보더만 요청했는데 배경이 어두워짐 → 성공 아님, self-reject 후 재시도)
- 감사·평가 맥락에서는 이것이 **FAIL** 이다. "개선이니까 괜찮다" 는 근거가 되지 못한다.

### 부분 롤백 요청

"색은 지금이 맞는데 그라디언트는 이전이 낫다" 같은 **부분 롤백**은 두 축을 분리한 지시다.
지목된 축만 이전 상태로 되돌리고 나머지는 유지한다. 새 접근을 고수하거나 전체를 되돌리지 마라.

---

## 3. Before/After Evidence Block — 무엇을 증거로 삼는가

시각 산출물을 만들거나 바꾼 뒤에는 완료 보고를 **EVIDENCE 블록**으로 닫는다. 서술만으로 완료를
선언하지 않는다.

```text
## EVIDENCE
- before: [캡처 경로 / 명령+출력 / 파일:라인]
- after:  [캡처 경로 / 명령+출력 / 파일:라인]
- proof:  [이 변경이 의도대로 됐음을 보이는 테스트·쿼리·diff 결과]
- 의도 외 영역: [변화 없음 확인 근거 / 또는 변한 항목과 처리]
```

### 증거 유효성 4 검사

증거를 제출하기 전에 아래를 통과해야 한다. 하나라도 실패하면 그 증거는 무효이며 결과는 PASS 가
아니라 `[미검증]` 이다. (정본: `harness/docs/guides/qa-evaluation-guide.md` §Evidence Validity Gate)

| # | 검사 | 실패 예 |
| - | ---- | ------- |
| 1 | **비공백** — 출력·캡처가 실제 내용을 담았는가 | 0 바이트 파일, 에러 메시지만 담긴 로그 |
| 2 | **활성화** — 측정이 검사 대상을 실제로 한 번이라도 통과했는가 | 0 개 테스트 실행, 스킵된 스위트, 매치 0 건 grep |
| 3 | **반증 가능성** — 위반 상태였다면 이 측정이 다른 결과를 냈겠는가 | 어떤 입력에도 같은 출력을 내는 측정 |
| 4 | **출처** — 증거를 직접 수집했는가 | 구현자 서술·주석·커밋 메시지 인용 |

### 렌더 산출물 특칙

- **빈 화면·빈 목록·플레이스홀더만 있는 캡처는 PASS 증거가 아니라 검증 실패 신호다.**
  "요소가 안 보이니 문제도 없다" 는 잘못된 부재 추론이다.
- 캡처에서 **구체 요소를 지목**해 근거에 쓴다 (`헤더 "내 그룹" + 목록 3 행 확인`).
  지목할 수 없으면 그 캡처는 무효 증거다.
- 캡처 자체가 실패했거나 도구가 응답하지 않으면 그것은 `[미검증]` 이지 PASS 가 아니다.

### 비교 반복 순서 — 반영 확인과 스스로 고치기 상한

시각 산출물을 고칠 때는 아래 순서를 지킨다. 새로 만드는 산출물이면 1 의 기준 캡처 자리에 `신규` 라고 적는다.
실측(`/insights` 2026-09-24 F03 · F26): 재시작이 조용히 실패했는데 「갱신했다」 고 보고했고, 사용자는 기준 화면 ·
변경 · 재촬영 · 비교 · 스스로 고치기를 합의 조건으로 요구했다.

1. **기준 캡처** — 캡처 파일 경로를 남기고 본 것을 요소 단위로 적는다. 이번 변경으로 반드시 달라져야 할 눈에
   보이는 표식 하나를 이때 정한다 (예: 테두리 색, 칩 순서)
2. **한 번에 한 의도**만 고친다. 여러 변경을 묶으면 재캡처의 차이가 무엇 때문인지 가를 수 없다
3. **반영 확인** — 새로 찍은 캡처에서 1 의 표식이 바뀌었는지로 판정한다. 새로고침·재시작 명령의 성공 메시지만으로
   판정하지 않는다. 표식이 그대로면 「반영 안 됨」 이다 — 같은 새로고침을 되풀이하지 말고 처음부터 다시 띄운다.
   반영이 확인되기 전에는 「갱신했다」 고 말하지 않는다
4. **재캡처** — 반영이 확인된 캡처를 재캡처로 쓰고 경로를 남긴다
5. **대조** — §2 보존 목록의 속성이 그대로인지 본다. 의도 외 영역이 변했으면 self-reject 하고 되돌린 뒤 다시 한다.
   **스스로 고치기는 최대 3 회**다. 3 회째도 실패하면 기준 캡처 · 마지막 재캡처 · 달라진 속성을 붙여 사용자에게 넘긴다

### 캡처 점검 목록

기준 캡처와 재캡처마다 아래 넷을 본다. 하나라도 걸리면 그 캡처로 PASS 를 주지 않는다. 실측(`/insights`
2026-09-24 F04): 글자 넘침과 깨진 글리프를 사용자가 먼저 찾았고, 넘침을 데이터 수정으로 재현하려다 실패했다.

1. **글자 넘침** — 잘린 글자, 뜻밖의 말줄임, 컨테이너 밖으로 나간 글자, 문서 본체의 가로 스크롤
2. **깨진 글리프** — 네모나 빈칸으로 나온 글자와 이모지. 실제 서비스 글꼴로 그리지 않은 캡처로는 글자 모양을
   판정하지 않는다 — 글자 항목은 실제 글꼴로 그린 캡처로 본다
3. **칩·뱃지와 줄 모양** — 칩·뱃지 모양, 카드인지 평평한 줄인지를 §0 관례 표와 대조한다
4. **디버그 겹침** — 떠 있는 디버그 단추·띠·개발 도구 표시가 판정할 자리를 가리는지 본다. 가렸으면 치우거나
   옮긴 뒤 같은 자리를 다시 찍는다

넘침은 데이터를 고쳐 재현하지 말고 글자를 키운 상태로 한 장 더 찍는다.
웹은 텍스트 200% 확대(WCAG 2.2 SC 1.4.4), 앱은 기기 글자 크기 최대다.
320 CSS px 폭에서 내용·기능이 사라지거나 양방향 스크롤이 생기는지(SC 1.4.10 Reflow)는 따로 판정한다.
잘라낸 조각만 보고 결함이라 단정하기 전에 전체 화면을 한 장 더 찍는다.
출처: [WCAG 2.2](https://www.w3.org/TR/WCAG22/).

---

## 4. Design Approval Record — 승인을 어떻게 남기는가

사용자가 시안·컨셉을 확정하면 **파일 아티팩트로 기록**한다. 대화 로그만으로는 이후 평가에서
"승인 근거 확인 불가" 가 되어 REJECT 된다 (2026-07-13 글로벌 REJECT `UI-06` 의 직접 사유).

### 경로

```text
.design/approvals/{YYYYMMDD}-{대상}.md
```

프로젝트에 `.harness/` 가 있으면 같은 파일을 `.harness/` 기준 상대 경로로 참조 가능하게 남긴다 —
QA evaluator 가 증거로 읽는 위치다.

### 최소 필드

```markdown
# 승인 기록 — {대상}

- 승인일: {YYYY-MM-DD}
- 승인 주체: {사용자 직접 확정 | 자율 모드 (근거 명시)}
- 대상 산출물: {파일 경로 — 예 .design/mockups/dashboard-sidebar.html}
- 선택된 안: {시안 이름/ID}
- 확정된 시각 값: {승인 시점에 고정된 색상·타이포·간격 — 이후 §1 순위 2 의 근거가 된다}
- 확정 구성: {화면에 남는 요소와 배치 — 무엇이 어디에 있는가}
- 폐기한 대안·이유: {이번 결정에서 버린 안·요소와 이유 — 없으면 `없음`}
- 미확정/후속: {합의되지 않아 남긴 항목}
- 원문 근거: {사용자 발화 인용 또는 자율 모드 판단 근거}
```

### 규칙

- **자율 모드에서 승인을 대행한 경우에도 기록을 남긴다.** 이때 승인 주체를 "자율 모드" 로 명시하고
  판단 근거를 적는다. 기록 없이 진행하면 측정 근거 부재로 평가에서 REJECT 된다.
- 승인 기록의 "확정된 시각 값" 은 §1 우선순위 2 의 실체다. 이후 세션에서 토큰·팔레트와 충돌하면
  **승인 기록이 이긴다.**
- 승인 후 시안을 수정하면 기록을 갱신한다. 스테일 승인 기록은 없는 것보다 나쁘다.
- **폐기한 대안은 다시 넣지 않는다.** 다음 시안·수정 전에 같은 대상의 승인 기록을 읽고, 폐기 칸의 안·요소는
  사용자가 되살리라고 하지 않는 한 다시 만들지 않는다. 실측(`/insights` 2026-09-24 F20): 사용자가 폐기한
  시간대·국가 항목을 되살렸다.
- 제품 요구 수준의 폐기 결정(기능·설정 항목을 없앤다는 결정)은 이 기록에서 새로 정하지 않는다. 그 결정이 적힌
  파일 경로를 폐기 칸에 적는다 — 결정 원문이 두 곳에 있으면 한쪽만 고쳐진다.

---

## 5. Variant Contract Matrix + Distinctiveness Gate — 비교안이 실제로 서로 다른가

> **적용 대상:** 시안·컨셉 안·후보안처럼 **하나의 결정을 위해 비교용 변주안을 여러 개 만드는**
> design-kit 스킬 — `design-mockup` · `design-concept`.
>
> **현재 등급: E1** (문장 규약 + Variant Contract Matrix 아티팩트). 축 값이 겹치는 variant 가
> 다시 관측되면 문장을 다듬지 말고 아래 판정식을 CI 게이트로 승급한다.
>
> **개수 상한 · primary axis 개수 · 부대 산출물 금지의 정본은 이 절이 아니다.**
> `harness/docs/guides/skill-design-guide.md` §5.6 Variant Budget 이 정본이며 (유형 11 탐색형 생성),
> 여기서 그 숫자를 다시 정의하지 않는다. 이 절이 더하는 것은 **구별성을 기계 판정하는 오라클**이다.

### 왜 축 선언만으로는 부족한가 (실측)

글로벌 REJECT `UI-04` (2026-08-12): *"B3(단일 컬럼)과 B6(조밀 로그)이 계약 지정 4축(버블 컨테이너
유무 / 정렬 컬럼 수 / 메타 위치 / 묶음 단위) 전부에서 동일값 — 구조 구별 요구 위반."*

계약이 축을 **이미 명시**했는데도 산출물이 그것을 무시했다. 즉 "축을 정하라" 는 문장을 한 번 더
쓰는 것은 처방이 아니다. **축 값이 실제로 다른지를 계산**해야 한다. 이것은 morphological chart 가
기능/축별 수단을 나열해 design space 를 만들되 조합 폭발과 비실용 해를 제한하는 방식과 같다
([IfM Morphological Charts](https://www.ifm.eng.cam.ac.uk/research/dmg/tools-and-techniques/morphological-charts/) ·
[Clemson thesis 274](https://open.clemson.edu/all_theses/274/)). 생성 디자인 연구도 "서로 다르게
지각되는 대안" 을 거리 기반으로 다룬다 ([Strathclyde 70009](https://strathprints.strath.ac.uk/70009/)) —
다만 design-kit 은 **구조 feature vector 를 1 차 신호**로 두고 렌더 후 perceptual diff 는 보조로만
쓴다. 큰 pixel diff 는 구조 중복을 면제하지 않는다.

### 개수 계약 (§5.6 에 대한 design-kit 추가 2 조)

1. **사용자가 개수를 말하면 정확히 그 수를 낸다.** 초과도 미달도 위반이다. "3 개" 요청에 5 개를
   내면 사용자가 2 개를 지우는 비용을 떠안는다.
2. **자체 판단 상한은 §5.6 의 기본값(3)이고, 사용자 승인이 있을 때 최대 5 다.** 6 개 이상이
   필요해 보이면 한 번에 내지 말고 배치를 나눠 제안한다.

### variant 필수 4 필드

각 variant 는 산출 전에 아래 4 개를 갖는다. 하나라도 비면 그 variant 는 비교 대상이 아니다.

| 필드 | 의미 |
| ---- | ---- |
| `variant_id` | 전역 유니크 식별자 (`A1`, `B3` 처럼 짧게) |
| `strategy_label` | 이 안이 우선한 전략 (`전환 최적화형`, `정보 밀도형` — "A안/B안" 금지) |
| `axis_vector` | **지정 축 순서대로 나열한 값 벡터.** 구별성 판정의 유일한 입력이다 |
| `intended_user_scenario` | 이 안이 가장 잘 맞는 사용자 시나리오 (선택 기준 토론의 근거) |

### Variant Contract Matrix (산출 **전** 합의 · E1 아티팩트)

`skill-design-guide` §5.6 의 Variant Matrix 5 열(`id` · `axis` · `axis value` · `constants` ·
`생성·수정 파일`)에서 `axis` 와 `axis value` 를 `axis_vector` 한 열로 합치고,
`strategy_label` · `intended_user_scenario` 2 열을 더한 **6 열**이다. 열을 빼지 마라.

| variant_id | strategy_label | axis_vector (축1/축2/축3/축4) | constants | intended_user_scenario | 생성 파일 |
| ---- | ---- | ---- | ---- | ---- | ---- |
| A1 | 정보 밀도형 | 없음 / 1 / 하단 / 세션 | 컬러·타이포·카피 | 기록을 훑어보는 재방문 사용자 | `mock/a1.html` |
| A2 | 탐색성 강화형 | 카드 / 2 / 상단 / 세션 | 컬러·타이포·카피 | 특정 기록을 찾는 사용자 | `mock/a2.html` |
| A3 | 전환 최적화형 | 채움 / 1 / 상단 / 클러스터 | 컬러·타이포·카피 | 다음 액션을 유도받는 신규 사용자 | `mock/a3.html` |

### Distinctiveness Gate — 판정 규칙

- 지정 축 집합의 크기를 `k` 라 한다. 사용자가 축을 지정했으면 **그 축이 곧 계약**이며 임의로
  바꾸거나 늘리지 않는다. 지정이 없으면 매트릭스에 선언한 축이 `k` 다.
- 두 variant 의 `axis_vector` 를 원소별로 비교해 Hamming distance `d` 를 구한다.
- **`k <= 2` 이면 `d >= 1`, `k >= 3` 이면 `d >= 2`** 를 모든 쌍이 만족해야 한다.
- 예외는 하나다 — 사용자가 **"micro-variant 비교"** 를 명시한 경우. 이때만 `d >= 1` 로 완화하고
  그 선언을 매트릭스에 기록한다. 스스로 예외를 선언하지 마라.
- **구조 축이 아닌 것은 `axis_vector` 원소로 세지 않는다** — 색상·토큰 값·카피 문구·아이콘 교체.
  이것들만 다른 두 안은 `d = 0` 이며 FAIL 이다.
- 게이트 실패 세트는 **제출하지 않는다.** 겹치는 쪽을 다시 만든다.

```python
#!/usr/bin/env python3
"""Variant Distinctiveness Gate — 지정 축 axis_vector 의 pairwise Hamming 검사.
입력(stdin): 각 줄 `variant_id<TAB>축1값<TAB>축2값...` — 열 순서 = 지정 축 순서, 헤더 없음.
exit code 는 harness/evals/gate-exit-codes.md 를 따른다 (0 pass / 1 위반 / 2 입력 오류)."""
import sys

rows = [l.rstrip("\n").split("\t") for l in sys.stdin if l.strip()]
if len(rows) < 2:
    print("USAGE_ERROR: variant 2 개 이상 필요"); sys.exit(2)
k = len(rows[0]) - 1
if k < 1 or any(len(r) - 1 != k for r in rows):
    print("USAGE_ERROR: 모든 행의 축 개수가 같아야 한다"); sys.exit(2)
need = 2 if k >= 3 else 1
bad = 0
for i in range(len(rows)):
    for j in range(i + 1, len(rows)):
        d = sum(1 for a, b in zip(rows[i][1:], rows[j][1:]) if a != b)
        if d < need:
            print(f"FAIL {rows[i][0]} vs {rows[j][0]}: hamming={d} < {need}")
            bad += 1
print(f"axes={k} required_hamming>={need} pairs={len(rows)*(len(rows)-1)//2} violations={bad}")
sys.exit(1 if bad else 0)
```

`UI-04` 를 이 게이트에 넣으면 다음이 나온다 — 이것이 계약이 잡았어야 했던 출력이다.

```text
$ printf 'B3\tnone\t1\tbottom\tsession\nB5\tcard\t1\tbottom\tcluster\nB6\tnone\t1\tbottom\tsession\n' | python3 distinct_gate.py
FAIL B3 vs B6: hamming=0 < 2
axes=4 required_hamming>=2 pairs=3 violations=1
exit=1
```

**트레이드오프:** 이 게이트는 중복을 확실히 막지만 **체크박스식 변형**을 유도할 수 있다 — 축 값만
바꾸고 실제로는 좋지 않은 안을 만드는 것. 그래서 게이트는 "구별되는가" 만 판정하고, **"좋은가" 는
여전히 사용자 판단과 리뷰의 몫**이다. 게이트 통과를 품질 승인으로 읽지 마라.

---

## 6. Decision Propagation Manifest — 확정된 결정이 모든 표면에 갔는가

> **적용 대상:** `design-test` (생성) · `design-audit` · `design-reviewer` (판정).
>
> **현재 등급: E2** — `decisions.yaml` 이라는 아티팩트를 남긴다.

§4 승인 기록은 "무엇이 확정됐는가" 를 남긴다. 그러나 확정된 결정이 **어느 표면들에 반영돼야
하는가**는 어디에도 적히지 않았고, 그 결과 "A1 에는 적용, A3 에는 누락" 이 반복됐다. 이 절은 승인
기록의 downstream 이다 — `decision_id` 를 발급하고, 그 결정을 소비해야 할 surface 를 열거하고,
surface 마다 **사용자가 볼 수 있는 증거**를 요구한다.

이것은 시각 회귀 도구의 기본 기능이 아니다. Playwright · Chromatic · Percy · BackstopJS 는 baseline
snapshot 과 diff · threshold · ignore/selector/scenario 를 제공하지만, 확인한 공식 문서 범위에서
`decision_id → required surface → golden coverage` 를 native 로 강제하는 패턴은 없다
([Playwright](https://playwright.dev/docs/test-snapshots) · [Chromatic](https://www.chromatic.com/docs/visual/) ·
[Percy](https://percy.io/how-it-works) · [BackstopJS](https://github.com/garris/BackstopJS)).
따라서 manifest 는 도구 **위에 얹는 traceability gate** 이며, 그 구조는 W3C ACT Rules Format 이
테스트 규칙에 요구하는 requirement mapping / applicability / expectations / outcome 을 UI 결정
전파에 옮긴 것이다 ([ACT Rules Format](https://www.w3.org/TR/act-rules-format/)).

**도구 중립 — design-kit 은 Playwright · Chromatic · Percy · BackstopJS 중 어느 하나도 표준으로 강제하지 않는다.** 프로젝트가 이미 쓰는
도구에 manifest 를 얹어라. 도구를 바꾸라고 요구하지 마라.

### 위치

```text
.design/decisions.yaml
```

toolkit 별 manifest 를 쓰는 프로젝트는 경로만 바꾸고 **스키마는 같게 유지**한다. 단일 경로로
고정할지는 근거가 부족해 **열린 질문으로 남긴다** — 정하지 않은 것을 정해진 것처럼 쓰지 마라.

### 스키마

```yaml
decisions:
  - decision_id: DEC-20260813-001
    source: .design/approvals/20260813-dashboard.md
    status: approved
    summary: "SP-G spacing and grouping"
    required_surfaces:
      - surface_id: dashboard.desktop.main
        route_or_entry: /dashboard
        state: populated
        viewport_or_container: desktop-1440
        selectors: ["main", "[data-surface='group-list']"]
        golden: tests/design/goldens/DEC-20260813-001/dashboard.desktop.main.png
        assertions: ["main visible", "group rows >= 1", "container height > 0"]
    excluded_surfaces:
      - surface_id: onboarding.mobile
        reason: "decision does not apply to onboarding flow"
```

- `decision_id` 는 `DEC-{YYYYMMDD}-{NNN}` 이며 `source` 는 §4 승인 기록 파일이다. 승인 기록 없는
  결정은 manifest 에 올리지 않는다 — 그것은 결정이 아니라 제안이다.
- **`excluded_surfaces` 는 선택이 아니다.** 적용하지 않는 표면은 이유와 함께 명시한다. 침묵은
  "검토했다" 가 아니라 **커버리지 공백**이다.

### Coverage rule 4 조

1. `required_surfaces` 의 각 surface 에 **golden 또는 user-visible assertion 이 하나도 없으면
   FAIL** 이다.
2. **golden 만 있고 핵심 요소의 visible / count / height assertion 이 없으면 FAIL** 이다. 빈 화면도
   baseline 과 같으면 통과하므로 스냅샷 단독은 "사용자가 본다" 를 증명하지 못한다 (§3 렌더 산출물
   특칙과 같은 이유).
3. snapshot 갱신은 `decision_id` 와 대응 승인 아티팩트가 있을 때만 허용한다. 근거 없는
   `--update-snapshots` 는 회귀를 baseline 으로 굳힌다.
4. 변경 대상 locator snapshot 과 주변 영역 snapshot 을 **분리**해 "결정 반영" 과 "의도 외 변화 없음"
   을 따로 판정한다 (§2 Partial Visual Change Isolation 과 짝).

```python
#!/usr/bin/env python3
"""Decision Propagation Coverage Gate — surface 별 증거 충족 검사.
exit code 는 harness/evals/gate-exit-codes.md 를 따른다
(0 pass / 1 커버리지 위반 / 2 스키마 오류 / 3 대상 0 건 = 검사 미수행)."""
import re, sys, yaml

path = sys.argv[1] if len(sys.argv) > 1 else ".design/decisions.yaml"
try:
    doc = yaml.safe_load(open(path, encoding="utf-8")) or {}
except FileNotFoundError:
    print(f"NO_MANIFEST {path}"); sys.exit(3)
except yaml.YAMLError as e:
    print(f"SCHEMA_ERROR {e}"); sys.exit(2)

decisions = doc.get("decisions") or []
if not decisions:
    print("NO_DECISION 대상 0 건 — 검사 미수행"); sys.exit(3)

# user-visible assertion 으로 인정하는 3 종: visible / count / height
PATTERNS = {"visible": r"\bvisible\b", "count": r"(>=|<=|>|<|==)\s*\d+|\bcount\b",
            "height": r"\bheight\b"}
viol = surfaces = schema = 0
for d in decisions:
    did = d.get("decision_id", "<no-id>")
    # 아래 두 검사가 없으면 표면을 하나도 적지 않은 결정이 surface 0 개 · 위반 0 으로 통과한다 (2026-09-25 재현)
    if not re.fullmatch(r"DEC-\d{8}-\d{3}", str(d.get("decision_id", ""))) or not d.get("source"):
        print(f"SCHEMA_ERROR {did}: decision_id 형식(DEC-YYYYMMDD-NNN) 또는 source 가 없다"); schema += 1
    if not (d.get("required_surfaces") or d.get("excluded_surfaces")):
        print(f"FAIL {did}: required_surfaces · excluded_surfaces 가 둘 다 비었다 — 침묵은 커버리지 공백"); viol += 1
    for x in d.get("excluded_surfaces") or []:
        if not x.get("reason"):
            print(f"FAIL {did}/{x.get('surface_id', '<no-surface-id>')}: excluded_surfaces 에 reason 이 없다"); viol += 1
    for s in d.get("required_surfaces") or []:
        surfaces += 1
        sid = s.get("surface_id", "<no-surface-id>")
        asserts = " ; ".join(s.get("assertions") or [])
        hit = [k for k, p in PATTERNS.items() if re.search(p, asserts, re.I)]
        if not s.get("golden") and not hit:
            print(f"FAIL {did}/{sid}: golden 도 user-visible assertion 도 없음"); viol += 1
        elif not hit:
            print(f"FAIL {did}/{sid}: golden 만 존재 — visible/count/height assertion 부재"); viol += 1
print(f"decisions={len(decisions)} surfaces={surfaces} violations={viol} schema_errors={schema}")
if schema:
    sys.exit(2)
if viol:
    sys.exit(1)
if surfaces == 0:
    print("NO_SURFACE required_surfaces 0 개 — 검사 미수행"); sys.exit(3)
sys.exit(0)
```

**골든을 무차별로 만들지 마라.** 골든 회귀는 유지비가 크다 — 의도된 디자인 변경마다 baseline
리뷰가 필요하고, 브라우저·OS·폰트·anti-aliasing 차이로 잡음이 생기며, threshold 를 높이면 실제
회귀를 놓친다. 대응은 넷이다: (a) manifest 로 대상 surface 를 줄인다 (b) CI 렌더 환경·폰트·브라우저를
고정한다 (c) 동적 데이터·시간·애니메이션을 고정한다 (d) **high-risk 결정만** 골든으로 보호하고
나머지는 assertion 으로 간다.

골든을 repo 에 커밋할지 외부 baseline 서비스에 둘지, surface registry 를 수동 작성할지 라우트
목록에서 자동 생성할지는 **근거가 부족해 열린 질문으로 남긴다.**

---

## 7. Evidence Channels — 무엇을 재는 증거인가

> **적용 대상:** design-kit 전 스킬·에이전트. §3 Before/After Evidence Block 의 증거에 **채널
> 라벨**을 붙이는 규약이다.

§3 은 증거가 **유효한가**를 다뤘다. 이 절은 그 증거가 **무엇을 재는 증거인가**를 다룬다. 둘은 다르다 —
0 바이트가 아닌 멀쩡한 스크린샷도 "사용자가 그 화면에서 그것을 본다" 를 증명하지는 않는다.
Playwright 공식 문서도 visual comparison 은 첫 실행에서 reference 를 만들고 다음 실행부터 비교하며
렌더링이 OS·브라우저·폰트·하드웨어에 따라 달라질 수 있다고 경고한다
([test-snapshots](https://playwright.dev/docs/test-snapshots)). 실제 관측에는 locator visibility,
비어 있지 않은 bounding box, count/text/in-viewport 같은 assertion 이 필요하다
([actionability](https://playwright.dev/docs/actionability) ·
[test-assertions](https://playwright.dev/docs/test-assertions)).

| 채널 | 무엇을 재는가 | 무엇을 재지 못하는가 |
| ---- | ---- | ---- |
| `artifact_snapshot` | 산출물 파일(목업 HTML·스토리·골든 PNG) 자체의 상태 | 사용자가 실제 앱에서 그 화면에 도달하는지, 그 데이터로 그렇게 보이는지 |
| `dom_snapshot` | 렌더된 DOM·접근성 트리의 구조와 속성 | 시각적 겹침·클리핑·가려짐, 실제 픽셀 |
| `browser_user_visible` | 브라우저에서 지정 route·state·viewport 로 도달해 얻은 visible locator + count/height | 실기기 폰트·DPI·플랫폼 위젯 차이 |
| `device_user_visible` | 실기기/시뮬레이터에서 얻은 관측 | (가장 강한 채널 — 비용이 크다) |

### 규칙

- **증거를 인용할 때 채널 이름을 함께 적는다.** 채널 없는 증거는 강도를 알 수 없다.
- **`artifact_snapshot` 만으로 "사용자가 보는 화면이 정상" 이라고 말하지 못한다.** 목업 HTML 이
  잘 열리는 것과 앱 화면이 정상인 것은 다른 명제다.
- PASS 문장에는 최소 5 요소가 들어간다: **viewport · route/state · visible locator · count/height ·
  screenshot/golden id.** 하나라도 없으면 그 PASS 는 `[미검증]` 로 내린다.
- 채널 등급이 낮은 증거로 높은 주장을 하지 마라. 주장의 강도를 증거 채널에 맞춰 낮추는 것이 정답이다.

```text
Bad:  "목업 HTML 스냅샷 정상 → 대시보드 렌더링 문제 없음"  (artifact_snapshot 으로 앱 상태를 주장)
Good: "[browser_user_visible] /dashboard · desktop-1440 · populated — main visible ·
       group rows 3 · height 812 · golden DEC-20260813-001/dashboard.desktop.main.png"
```

### 사용자 관측과 충돌할 때

**이 규약을 여기서 재정의하지 않는다.** 정본은 두 곳이다:

- 생성 측 — `harness/docs/guides/skill-design-guide.md` §3.8 User-Reported Failure Gate
  (상태를 `REOPENED` 로 · 반박 금지 · 오라클 유효성 6 축 대조 · 완료 해제 3 택)
- 평가 측 — `harness/docs/guides/agent-design-guide.md` §10 (사용자 보고 우선)

design-kit 이 더하는 것은 재현 축의 **시각 도메인 구체화** 하나다: 6 축 대조 시 route/data/viewport
에 더해 **scroll 위치**와 **접근성 설정**(`prefers-reduced-motion` · `prefers-color-scheme` ·
텍스트 확대)을 같은 값으로 맞춘다. 이 둘이 다르면 같은 코드가 다르게 보인다.
