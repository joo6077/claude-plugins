---
name: design-mockup
description: >
  특정 화면 요청 시 하이파이 HTML 시안을 계약된 개수만큼 생성하여 제시한다 (미지정 3 · 사용자 지정 N · 승인 상한 5).
  정의된 디자인 컨셉과 토큰이 있으면 자동으로 로드하여 반영한다.
  각 시안의 UI 요소에 유니크 ID를 부여하여 사용자가 특정 컴포넌트를
  지칭하거나 추출할 수 있다. 선택한 시안/컴포넌트를 Figma MCP로 전송 가능.
  "시안 만들어줘", "목업", "mockup", "화면 시안", "디자인 시안",
  "레이아웃 제안", "시안 보여줘" 같은 요청 시 트리거.
  기존 UI 코드 리뷰/가이드에는 트리거하지 않는다 — design-guide 사용.
argument-hint: "<page-name or description>"
user-invocable: true
---

# Gotchas

1. **컬러 변형만으로 시안 구분 금지 — 구별성은 선언이 아니라 계산이다** — 시안들은 서로 다른 레이아웃/구성 접근이어야 한다. 색상·토큰 값·카피 문구·아이콘 교체는 `axis_vector` 원소로 세지 않으므로, 그것만 다른 두 안은 Hamming distance 0 이며 FAIL 이다. 판정식과 실행 가능한 게이트: `../../references/visual-change-protocol.md` §5 Variant Contract Matrix. 실측 근거는 글로벌 REJECT `UI-04` — 계약이 4 축을 **이미 명시**했는데도 두 안이 전 축 동일값이었다.
2. **ID 중복 금지** — 생성한 전 시안에 걸쳐 모든 컴포넌트 ID는 전역 유니크여야 한다. `{컴포넌트명}-{짧은해시}` 포맷을 사용하라. 같은 해시가 나오면 재생성한다.
3. **접근성 원칙 무시 금지** — 하이파이 시안이라도 WCAG 2.2 AA 대비 비율(4.5:1)과 최소 터치 타겟을 준수하라. **WCAG 2.2 SC 2.5.8 AA = 24×24 CSS px** / SC 2.5.5 AAA = 44×44 CSS px / Apple HIG 44pt는 터치 디바이스 실용 권장치다. 시안에서 AAA/플랫폼 권장 44pt를 기본으로 잡아두면 Figma/HTML → 코드 단계에서 안전하다. 시각적으로 예뻐도 접근성 위반이면 안 된다. 출처: [W3C WCAG 2.2 SC 2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html).
4. **Figma MCP 미설정 시 에러 금지** — Figma 전송 요청 시 MCP가 미설정이면 에러가 아닌 안내로 처리하라. "Figma 전송을 원하면 Figma MCP 설정이 필요합니다"와 함께 HTML 파일 경로를 안내한다.
5. **Lorem ipsum 금지** — 플레이스홀더 텍스트는 실제 사용자가 마주칠 콘텐츠와 다르게 읽힌다. 실제 콘텐츠나 현실적인 예시 데이터를 사용하라. 제목, 버튼 레이블, 설명문이 lorem ipsum이면 레이아웃 의도를 제대로 평가할 수 없다.
6. **시안 레이블을 "A안/B안"으로만 붙이지 마라** — 각 시안은 서로 다른 전략적 우선순위를 반영해야 한다. 레이블도 그 의도를 담아라. 예: `전환 최적화형`, `탐색성 강화형`, `브랜드 임팩트형`. 이렇게 하면 취향 투표가 아닌 선택 기준 토론으로 유도된다.
7. **디바이스 프레임은 목적에 따라 선택적으로 사용하라** — 클라이언트 발표나 near-final 데모에는 디바이스 프레임이 완성 인상을 준다. 그러나 레이아웃 구조 비교나 콘텐츠 밀도 검토가 목적이면 프레임 없이 보여주는 편이 낫다. 프레임 chrome이 실제 논점인 레이아웃 판단을 방해할 수 있다.
8. **인터랙션이 쟁점이면 정적 비교에 의존하지 마라** — 드롭다운, 오버레이, 멀티스텝 플로우, 로딩 상태, 모달 전환은 나란히 놓인 정지 화면만으로 판단하기 어렵다. HTML 시안에 hover/focus/click 인터랙션을 포함하거나, 인터랙티브 프로토타입 링크를 함께 제공하라.
9. **반응형 시안은 breakpoint별 스냅샷만으로 끝내지 마라** — mobile/tablet/desktop 3단 구성을 보여줄 때, 각 화면에서 동일한 유저 시나리오 상태를 맞춰 두어야 비교가 의미 있다. 컬럼 수, 거터, max-width 등 레이아웃 규칙도 함께 명시하라.
10. **Container Queries 활용 권장** — 반응형 시안에서 페이지 레벨 분기는 media queries, 컴포넌트 레벨 분기는 `container-type: inline-size` + `@container` queries를 사용하라. 2026 Baseline 기준 모든 주요 브라우저 지원. cqw/cqi 유닛으로 컨테이너 상대 크기 지정이 가능하다. 콘텐츠가 깨지는 지점에 breakpoint를 설정하고 디바이스 타겟 기반은 피하라. 출처: research-log §J.
11. **Fluid Typography 적용** — 시안 내 텍스트에 `clamp(min, preferred, max)` 기반 fluid font-size를 적용하면 breakpoint 없이 모든 뷰포트에서 자연스러운 크기 전환을 보여줄 수 있다. 특히 히어로/디스플레이 텍스트에 효과적이다. 출처: research-log §E.
12. **mockup.html은 HTML 형식이 정상 산출물이다** — 이 스킬의 출력물(`.design/mockups/*.html`)은 의도적으로 HTML 형식을 사용한다. `design-tokens.md`, `audit-report.md` 같은 `.md` 계약 패턴과 구조가 다른 것은 설계상 의도된 차이이며 오류가 아니다. QA 평가 또는 검증 도구가 "HTML 형식이 .md 패턴과 다르다"고 지적할 경우 False positive로 처리하고 이 Gotcha를 근거로 무시한다.
13. **확정 = 승인 기록 파일 생성 (대화 로그로 끝내지 마라)** — 사용자가 시안을 확정하면 Step 6 에서 `.design/approvals/{YYYYMMDD}-{화면명}.md` 를 생성한다. 여기에 선택된 안, 산출물 경로, **확정된 시각 값(색상·타이포·간격)**, 원문 근거를 남긴다. 대화에서만 승인받고 파일을 남기지 않으면 이후 QA 에서 "goal 조건의 측정 근거(시안 승인 기록) 확인 불가" 로 REJECT 된다 — 2026-07-13 글로벌 REJECT `UI-06` 의 실제 사유다. **자율 모드로 승인을 대행한 경우에도 기록을 남기고 승인 주체를 "자율 모드" 로 명시**하라. 규격: `../../references/visual-change-protocol.md` §4.
14. **승인된 시안 값을 토큰으로 치환하지 마라 (Visual Source of Truth Precedence)** — 사용자가 브라우저로 확인하고 승인한 시안의 색상·간격은 프로젝트 팔레트 토큰보다 **우선한다**. 시안 수정 요청을 처리할 때 승인된 값을 "토큰 체계에 맞춰" 단일 tint 나 기존 accent 로 정규화하지 마라. 토큰화가 필요하면 값을 바꾸는 게 아니라 **그 값으로 토큰을 정의**하고 별도 제안하라. 프로젝트에 이미 색상 체계가 있으면 새 팔레트를 도입하기 전에 기존 값을 먼저 열거해 제시한다. 우선순위 표: `../../references/visual-change-protocol.md` §1.
15. **부분 수정 요청은 그 속성만 — Change Manifest 필수** — "이 카드 보더만 진하게", "색은 지금이 맞는데 그라디언트만 이전으로" 같은 요청에서 지목되지 않은 시각 속성(background, fill, radius, shadow, spacing, typography)을 함께 바꾸지 마라. 편집 전에 `변경 / 보존` 두 목록을 응답에 남기고, 수정 후 보존 목록의 값이 그대로인지 확인한다. 의도 외 영역이 변했으면 성공이 아니라 실패이므로 되돌리고 다시 적용한다. 부분 롤백 요청은 지목된 축만 되돌린다. 상세: `../../references/visual-change-protocol.md` §2.
16. **산출 전에 Variant Contract Matrix 를 합의하라 (개수 계약 + 구별성 게이트)** — 시안을 하나라도 만들기 전에 `../../references/visual-change-protocol.md` §5 Variant Contract Matrix 6 열을 채워 사용자와 합의한다. 개수는 **사용자가 말하면 정확히 그 수**, 미지정이면 3, 자체 판단으로 그 이상 늘리지 않으며 승인 시 최대 5 다. 개수 상한·primary axis 개수·부대 산출물(토큰 파일·디자인 시스템·서페이스 레인·카탈로그) 금지의 정본은 `harness/docs/guides/skill-design-guide.md` §5.6 Variant Budget 이며 여기서 재정의하지 않는다. "몇 개 목업" 요청에 수십 타일과 토큰 파일을 함께 만들면 사용자가 전부 지우게 된다 — 실제로 그랬다.
17. **시안 캡처는 `artifact_snapshot` 이다 — 앱 화면 정상을 주장하지 마라** — 목업 HTML 이 잘 열리는 것과 사용자가 실제 앱에서 그 화면을 보는 것은 다른 명제다. 증거를 인용할 때 채널 이름을 함께 적고, PASS 문장에 viewport · route/state · visible locator · count/height · screenshot id 5 요소를 넣어라. 채널 정의: `../../references/visual-change-protocol.md` §7 Evidence Channels. 사용자가 "아직 깨져 있다" 고 보고하면 반박하지 말고 재현하라 — 규약 정본은 `harness/docs/guides/skill-design-guide.md` §3.8 User-Reported Failure Gate 다.

# Process

## Step 1: 화면 요구사항 파악

사용자의 요청에서 파악한다:
- 어떤 페이지/화면인지 (로그인, 대시보드, 설정 등)
- 주요 기능과 정보 요소
- 대상 사용자

불명확하면 사용자에게 확인한다.

## Step 2: 자동 감지 및 로드

프로젝트에서 이전 단계 산출물을 탐색한다:

```text
# 감지 대상
.design/concept.md          → 컨셉 로드
**/theme/** **/tokens/**    → 디자인 토큰 로드
**/design-tokens.*          → 디자인 토큰 로드
```

- 컨셉 존재 → 무드 키워드, 컬러/타이포 방향, UI 패턴을 시안에 반영
- 토큰 존재 → 구체적 컬러값, 타이포 스케일, 간격을 시안에 적용
- 둘 다 없음 → 사용자 요구사항만으로 시안 생성

## Step 3: 개수 계약 · Variant Contract Matrix 합의 후 하이파이 HTML 시안 생성

### Step 3-a: 개수와 축을 먼저 고정한다 (파일을 만들기 전에)

`../../references/visual-change-protocol.md` §5 Variant Contract Matrix 를 채워 사용자와 합의한다.
정본 규칙(상한·축 개수·부대 산출물 금지)은 `harness/docs/guides/skill-design-guide.md` §5.6 이다.

| 상황 | 산출 개수 |
|------|----------|
| 사용자가 개수를 말함 | **정확히 그 수** — 초과도 미달도 위반 |
| 미지정 | **3** |
| 자체 판단으로 늘리기 | 금지. 승인받으면 **최대 5**, 6 개 이상은 배치를 나눠 제안 |

매트릭스 6 열(`variant_id` · `strategy_label` · `axis_vector` · `constants` ·
`intended_user_scenario` · 생성 파일)을 채운 뒤 **구별성 자가 검사**를 통과시킨다 — 지정 축이
3 개 이상이면 모든 쌍의 Hamming distance ≥ 2, 2 개 이하면 ≥ 1. 실행 가능한 게이트가 §5 에 있다.
겹치는 쌍이 있으면 그 세트는 제출하지 말고 겹치는 쪽을 다시 설계한다 (글로벌 REJECT `UI-04`).

요청받지 않은 토큰 파일·디자인 시스템·서페이스 레인·컴포넌트 카탈로그는 **만들지 않는다.**
필요해 보이면 별도 제안으로 올리고 승인 후에 만든다.

### Step 3-b: 합의된 개수만큼 생성

references/mockup-guidelines.md를 참조하고 ../../templates/mockup.html 포맷으로 시안을 생성한다:

각 시안은 standalone HTML 파일로 생성:
- `.design/mockups/{페이지명}-{특징}.html` (예: `dashboard-sidebar.html`)
- 실제 컬러, 타이포, 간격이 반영된 하이파이 수준
- 모든 UI 요소에 `{컴포넌트명}-{4자리해시}` ID 부여
- 호버 시 ID를 표시하는 JavaScript 오버레이 포함
- lorem ipsum 금지 — 실제 콘텐츠 또는 현실적 예시 데이터 사용

`strategy_label` 후보 풀 (합의된 개수만큼 **골라 쓴다** — 다섯 개를 전부 내라는 목록이 아니다):

- **전환 최적화형** — 사이드바 네비게이션 + 메인 콘텐츠, 주요 CTA를 상단 고정
- **탐색성 강화형** — 탑바 + 카드 그리드, 필터/정렬 전면 배치
- **정보 밀도형** — 탭 기반 + 리스트 뷰, 스캔 가능한 텍스트 계층 강조
- **브랜드 임팩트형** — 풀스크린 히어로 + 스크롤 섹션, 비주얼 중심 진입
- **대시보드/제어형** — 위젯 패널 레이아웃, 상태 요약 + 빠른 액션 우선

반응형이 요구사항에 포함된 경우, 각 시안에 mobile/tablet/desktop breakpoint 섹션을 추가하고 컬럼 수·거터·max-width 규칙을 명시한다.

## Step 4: 디자인 의도 설명

각 시안에 대해 설명한다:
- 시안이 반영한 전략적 우선순위 (전환, 탐색, 브랜드 등)
- 레이아웃 선택 이유와 정보 구조
- 시각적 강조 포인트 — 어디서 시선이 머무는가
- 어떤 사용자 시나리오/맥락에 가장 잘 맞는가
- 주요 결정의 간단한 근거 (왜 이 구성인가)

발표 순서는 "화면 나열"이 아니라 사용자 시나리오 흐름으로 구성한다. 각 시안을 독립적으로 설명하기보다, 어떤 문제를 어떻게 다르게 해결하는지 대비하여 설명하면 선택 기준 토론이 쉬워진다.

## Step 5: 사용자 선택 및 수정

- 사용자가 시안을 선택하거나 피드백을 준다
- ID를 사용한 소통: "card-product-a3f2를 더 크게 해줘"
- 시안 간 비교 요청 시 비교 기법 선택:
  - **구조가 크게 다른 안 비교** → side-by-side (나란히 배치)
  - **동일 화면 일부 요소 변경 비교** → 변경 전/후를 겹쳐서 설명
  - **결정 근거/핸드오프 포함 비교** → 주석(annotation) 추가
  - **인터랙션·상태 변화 비교** → hover/focus/click 동작 포함
- 수정 요청이 **특정 속성만 지목한 경우**(보더만·색만·간격만) 편집 전에 Change Manifest 를 남긴다 (Gotcha 15):

  ```text
  ## Change Manifest
  - 변경: [속성 — 대상 ID — 현재값 → 목표값]
  - 보존: [같은 요소의 나머지 시각 속성 — background / fill / radius / shadow / spacing / typography 중 해당분]
  ```

  수정 후 보존 목록의 값이 그대로인지 확인한다. 변했으면 되돌리고 지목된 속성만 다시 적용한다.
- 수정 후 HTML 파일 갱신
- 확정 시 `.design/mockups/` 에 최종본 유지

## Step 6: 승인 기록 생성 (확정 시 필수)

사용자가 시안을 확정하면 `.design/approvals/{YYYYMMDD}-{화면명}.md` 를 생성한다.
대화 로그만으로는 이후 QA 에서 승인 근거를 확인할 수 없어 REJECT 된다 (Gotcha 13 · 글로벌 `UI-06`).

```markdown
# 승인 기록 — {화면명}

- 승인일: {YYYY-MM-DD}
- 승인 주체: {사용자 직접 확정 | 자율 모드 (판단 근거 명시)}
- 대상 산출물: .design/mockups/{파일명}.html
- 선택된 안: {전략 레이블 + 시안 ID}
- 확정된 시각 값: {승인 시점에 고정된 색상·타이포·간격 — 이후 토큰과 충돌 시 이 값이 우선}
- 미확정/후속: {합의되지 않아 남긴 항목}
- 원문 근거: {사용자 발화 인용}
```

생성 직후 확인한다:

```bash
ls .design/approvals/                      # 파일 존재
grep -c '확정된 시각 값' .design/approvals/{파일명}.md   # → 1
```

승인 후 시안을 다시 수정하면 이 기록도 갱신한다. 스테일 승인 기록은 없는 것보다 나쁘다.

## Step 7: Figma 전송 (선택)

사용자가 Figma 전송을 요청하면:
- Figma MCP 설정 확인
- 설정됨 → 선택한 시안 또는 개별 컴포넌트(ID 기준)를 Figma로 전송
- 미설정 → "Figma 전송을 원하면 Figma MCP 설정이 필요합니다" 안내 + HTML 파일 경로 재안내
- 전송 실패 → 에러 메시지 + HTML 파일 경로 안내

# References

- `references/mockup-guidelines.md` — 시안 생성 기준 상세
- `../../templates/mockup.html` — 시안 HTML 출력 포맷 (공유 템플릿)
- `../../references/visual-change-protocol.md` — 시각 우선순위 · 부분 변경 격리 · 승인 기록 규격 · §5 Variant Contract Matrix · §7 Evidence Channels (SSOT)
- `harness/docs/guides/skill-design-guide.md` §5.6 Variant Budget · §3.8 User-Reported Failure Gate — 개수 상한·부대 산출물 금지·사용자 보고 규약의 정본
