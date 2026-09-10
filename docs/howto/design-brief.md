---
title: howto-kit 설계 브리프
status: draft
created: 2026-09-07
purpose: 다른 세션이 이 문서만 읽고 킷을 만들 수 있게 하는 설계 정본
---

# howto-kit 설계 브리프

**한 줄**: 사람이 손으로 해야 하는 절차를 **어느 화면 → 어느 메뉴 → 어느 항목 → 무슨 값 → 어떻게 확인**까지 끊지 않고 알려주는 스택·도메인 무관 킷. 기본은 대화창 즉답, 요청 시 MD 문서화.

이 문서는 리서치 결과가 아니라 **결정문**이다. 근거는 각 결정에 인라인으로 붙였고, 확인 못 한 것은 §11에 따로 뺐다.

---

## 1. 무엇을 고치는가 — 결함 4종

사용자 원문: *"맨날 다르게 알려주고 자세히 안 알려줘서 내가 몇 번이나 요청해야 함. 최신 정보도 아니고, 어떤 페이지에 정확히 어떤 메뉴를 통해 들어가고 어떤 항목을 어떻게 설정 및 입력하고 이런 걸 안 알려줌. 걍 대략적으로 알려줌."*

| ID | 결함 | 로컬 실측 증거 |
| --- | --- | --- |
| **F1** | 같은 질문에 매번 다른 절차 | `qa-evaluation-guide.md:1009-1013` 킷별 임계 2/3/0 → 같은 상태가 다른 판정. fit-pal `docs/setup/` 4개 문서가 같은 Bundle ID 를 `com.fitpal.test`/`com.fitpal.app` 두 값으로 적음 |
| **F2** | 입도 부족 — "설정에서 활성화하세요" | `memory/feedback_console_ui_verify.md:13` 사용자 원문 **"대충 알려주면 누가 못해"** / `reflections-2026-05.md:18826` **"자세하게 말해 대충말하지말고"** |
| **F3** | 최신성 결여 | `reflections-2026-05.md:18733` "공식 docs에서 검증했다"고 주장했으나 `web_search_requests:0, web_fetch_requests:0` — **조회 없이 지어냄**. `:18780` 에서 교정 후 재발, `enforcement_need: hard_gate` 로 판정됨 |
| **F4** | 네비게이션 경로 부재 | `reflections-2026-05.md:18705` **"고급 설정 아래에도 없음"** / `feedback_setup_guide_site_distinction.md:18` FCM 하려고 App Store Connect 로 진입 → 옵션 자체가 없음 / `format-checklist.md:115` `General` 한 단계 누락으로 경로 무효 |

F2 와 F3 는 서로를 악화시킨다. `reflections-2026-05.md:18752-18753` 이 그 실물이다 — 사용자가 "자세하게"를 요구한 **직후에** 사이드바 메뉴 순서를 검증 없이 단정했다. **입도 요구를 날조로 메우는 것**이 이 킷이 막아야 할 최악의 실패다.

---

## 2. 왜 새 킷인가 — onboarding-kit 은 못 고친다

기존 `onboarding-kit/skills/setup-guide` 는 F2·F4 를 **부작용이 아니라 출력 규격으로 생산**한다. 두 규칙의 곱이다.

```text
SKILL.md:28   "fetch 하지 않은 Step 은 쓰지 않는다"          ← 아래를 막는다
SKILL.md:131  "문서에 있는 상위 섹션명까지만 확정하고,
               그 아래는 '이 섹션에서 …' 로 열어 둔다"        ← 위를 막는다
```

공식 문서는 버튼·필드·기본값을 대개 안 적는다고 전제했으므로, 두 선 사이에 남는 문장은 정확히 하나다 — **"`<섹션명>` → 이 섹션에서 찾으세요."** 그리고 게이트 G1 은 `Step 수 == 출처 줄 수` 만 세므로 그렇게 끝난 답변도 `GATE_PASS` 를 받는다. evals 6 케이스에도 **입도를 재는 assertion 이 0 개**다. 3 개월간 검출되지 않은 계측적 이유다.

**그 전제 자체가 틀렸다.** 2026-09-07 실측:

- Firebase 공식 문서에 콘솔 딥링크가 그대로 박혀 있다 — `console.firebase.google.com/project/_/settings/general/…` [firebase.google.com/docs/reference/admin/node/firebase-admin.auth.decodedidtoken.md]. **`_` 가 프로젝트 id 자리라는 설명 문장은 확보하지 못했다** — `[미확인]`, `howto-kit/references/provenance-notes.md` §5
- 필드명까지 적는다 — *"Enter your app's package name in the **Android package name** field."* [firebase.google.com/docs/android/setup]
- 안 보일 때의 분기까지 적는다 — *"If you don't see a Campaigns tab or add button…"* [developer.apple.com/help/app-store-connect-analytics/acquisition/campaign-links], *"Organizations that you are a member of will not appear if the organization has blocked…"* [docs.github.com/…/managing-your-personal-access-tokens]

즉 **핵심 오류는 "검증 불가"를 "생성 금지"로 번역한 것**이다. 정직성이 요구하는 것은 침묵이 아니라 **출처 등급 표시**다.

### 개명이 아니라 신설인 이유

1. **실행 모델이 다르다.** 기존 킷의 E3 게이트·Regeneration Drift·evals 픽스처가 전부 "MD 파일이 산출물"을 전제한다. 대화 즉답이 기본이면 G1 은 항상 FAIL(`## Step` 헤더 없음), G3 는 항상 PASS(`stack` 이 비어 no-op)다. 모드 추가가 아니라 판정 인프라 교체다.
2. **살아남는 자산이 파일 단위가 아니라 블록 단위다.** `project-detection.md` 48 줄은 전체 폐기, `search-strategy.md` 는 약 70% 생존, `format-checklist.md` 는 11 섹션 중 6 개만 코어. 이식이 개명보다 싸다.
3. **개명 비용이 이미 신설 비용과 비슷하다.** 참조 표면 12 곳(`marketplace.json`, 루트 `CLAUDE.md` 4 곳, `kaizen-orchestrator` Phase 14, `phase-dependencies.md`, `phase-research-templates.md`, `.claude/skills/onboarding-kaizen/` 전체, `docs/index.html` 5 엔트리, `docs/onboarding-kit/` 7 파일, `scripts/check-external-links.py:38` 하드코딩 등). 게다가 `~/.claude/plugins/installed_plugins.json` 이 플러그인 **이름 문자열을 키로** 추적하므로 개명 시 재설치가 필요하다.
4. **같은 이름 아래서 고치면 옛 규칙이 계속 정당화된다.** 배포된 쇼케이스와 docs 5 페이지가 Gotcha 2 기반 규칙의 정본 예시로 서 있다.

### onboarding-kit 처리

**폐기하지 않는다.** 개발 레포 안에서 외부 서비스를 붙일 때 스택 확정(Phase 1)과 레포 실측 근거(Gotcha 8)는 실제로 값을 한다. `howto-kit` 이 evals 로 안정화된 뒤 흡수 여부를 재판단한다.

단 **개명과 무관하게 지금 깨져 있는 결함 3 건**은 별도로 고쳐야 한다:

1. `evals.json:86-87` 이 접미 없는 `[미검증]` 을 assert 하는데 `SKILL.md:30` 이 그 표기를 금지 — evals 가 현행 규칙과 정면 충돌
2. `SKILL.md:213` 의 `$STACK` 이 어디에도 정의되지 않아 Drift 검사에서 G3 가 영구 no-op
3. G4 의 판정식이 영문 토큰 `[Dd]eprecat` 에 묶여 있어 한국어 1차 출처("지원 종료", "폐지")는 근거가 있어도 FAIL

---

## 3. 설계 원칙 8개

각 원칙은 근거에 묶여 있다. 근거 없는 원칙은 넣지 않았다.

### P1. 스텝은 말단 액션으로 끝난다

한 스텝 = 한 동작. 종결 동사(누르기/입력/선택/체크/토글/저장/다운로드)로 끝나야 하며, **"이 섹션에서 …", "해당 항목을 찾아", "적절히 설정"** 으로 끝나면 미완이다.

> *"In general, use one step for each action."* — Google developer documentation style guide, [developers.google.com/style/procedures]
> *"should not be more than one sentence"* — DITA 1.3 `<cmd>`, [docs.oasis-open.org/dita/dita/v1.3/os/part2-tech-content/langRef/technicalContent/cmd.html]

### P2. 위치를 먼저, 동작을 나중에

> *"Make sure that customers know where the action should take place before you describe the action."* — Microsoft Writing Style Guide, [learn.microsoft.com/en-us/style-guide/procedures-instructions/writing-step-by-step-instructions]
> *"Tell the reader where to complete an action—for example, in a particular tool or UI field—before you state the action."* — Google, [developers.google.com/style/procedures]

### P3. 딥링크가 메뉴 경로보다 우선한다 — 불변 앵커 순위

URL 은 버튼 라벨보다 훨씬 덜 바뀐다. 안내는 잘 안 바뀌는 앵커 위에 세운다.

```text
불변도 높음  URL 경로 · 설정 키/API 이름
            섹션명
            버튼/필드 라벨
불변도 낮음  아이콘 · 배치(좌/우/상단)
```

실측된 딥링크 관행 (**확정 정본은 `docs/howto/deep-links.md`** — 2026-09-09 사이클에서 7 벤더 8 인용으로 확정했고 AWS·Azure 가 추가됐다):

| 서비스 | 공식 문서에 등장하는 형태 | 출처 |
| --- | --- | --- |
| Firebase | `console.firebase.google.com/project/_/settings/general/…` (`_` 의 의미는 `[미확인]`) | firebase-admin.auth.decodedidtoken.md |
| Apple | *"replace `[Team ID]` in the following URL with your Team ID: `https://appstoreconnect.apple.com/teams/[Team ID]/access/ci/…`"* | developer.apple.com/documentation/xcode/understanding-infrastructure-validation-builds |
| Stripe | `dashboard.stripe.com/test/apikeys` — *"MODE: Use `test` for sandboxes … or omit a value for live mode"* | docs.stripe.com/keys, docs.stripe.com/stripe-apps/deep-links |
| GitHub | `github.com/settings/personal-access-tokens/new` | docs.github.com/…/managing-your-personal-access-tokens |

딥링크가 없으면 **전역 검색어**를 준다.
> *"The Search bar at the top in the Google Cloud console is an efficient way to search for various product services, documentation pages, tutorials and even Google Cloud Resources"* — [cloud.google.com/blog/topics/developers-practitioners/tips-get-most-out-google-cloud-documentation]

### P4. 중간 단계를 생략하지 않는다

경로 표기는 `A > B > C` 로 전 구간을 쓴다. 한 단계라도 빠지면 사용자가 화면에서 못 찾는다 — `format-checklist.md:115` 의 실측(`General` 누락으로 경로 무효)이 근거다.

> *"Don't use bold on the greater-than symbol. Include a space before and after the symbol."* — Microsoft, [learn.microsoft.com/en-us/style-guide/procedures-instructions/describing-interactions-with-ui]

내부 데이터는 `path: ["Settings","General","Cloud Messaging"]` 로 **구조화**해 보관하고 렌더링만 `>` 로 한다 (Microsoft 는 `>` 를 굵게 하지 말라 하고 Google 은 시퀀스 전체를 한 bold 로 감싸라 해서 표기가 갈리기 때문이다).

### P5. 방향어 대신 명명된 컨테이너로 화면을 지목한다

> *"Don't use directional language to orient the reader"* / *"Add context to help the user find the element."* — Google, [developers.google.com/style/ui-elements]

실제 지원 문서가 쓰는 지목 어휘(2026-09-07 실측):

| 위치 | 실제 문장 | 출처 |
| --- | --- | --- |
| 좌측 사이드바 | *"Click Components from the left sidebar."* | support.atlassian.com/statuspage |
| 사이드바+상세 | *"Click Network in the sidebar, then click the network service that you're using (such as Wi-Fi) on the right."* | support.apple.com/102022 |
| 탭 | *"Click the Third-party tab."* | support.atlassian.com/statuspage |
| 탭 아래 배너 | *"From the Commits tab, select Sync now in the info banner under the tabs."* | support.atlassian.com/bitbucket-cloud |
| 모달 | *"In the Sync branch dialog, select the Sync strategy dropdown…"* | 같음 |
| 우측 상단 | *"Select more actions () at the top-right, then select Export."* | support.atlassian.com/jira-service-management-cloud |
| 우측 상단 버튼 | *"Stripe displays a Refund button in the upper-right corner of the page."* | docs.stripe.com/connect/end-to-end-marketplace |
| 페이지 하단 | *"Click Save component at the bottom of the page to save your changes."* | support.atlassian.com/statuspage |

### P6. 분기를 되묻기 전에 선제 제공한다

"몇 번이나 요청해야 함" 불만의 직접 해법이다. 라벨이 다르거나 항목이 아예 없는 경우를 **미리** 붙인다. 이것은 변명이 아니라 1급 공식 문서 관행이다.

> *"If you don't see a Campaigns tab or add button…"* — Apple
> *"If you can't see the filter's sharing configuration, you'll need your Jira administrator to give you the Create Shared Object global permission."* — Atlassian
> *"Organizations that you are a member of will not appear if the organization has blocked…"* — GitHub

분기 사유는 5 가지로 유형화한다: **권한/역할 · 요금제 · 버전 · 언어 · A/B 롤아웃**.

### P7. 최신성은 문장이 아니라 스탬프와 등급으로 보장한다

- 각 스텝에 **출처 URL + 조회일**. 조회하지 않은 스텝은 `[추정]` 등급을 달거나 쓰지 않는다.
- **적용 범위 스탬프** — 버전/지역/언어. Microsoft Support 는 본문 상단에 `Applies To / Windows 11 Windows 10` 을 두고, 같은 문서 안에서 경로를 버전별로 갈라 쓴다:
  *"Select Start > Settings > Apps > Advanced app settings."* (Win 11) ↔ *"Select Start > Settings > Apps > Apps & features."* (Win 10) — [support.microsoft.com/…/change-your-app-recommendation-settings-in-windows]

- **문서 최종 수정일 확인** — GCP 문서는 `Last updated 2026-07-29 UTC`, Google 약관은 `Last modified June 1, 2021`, Amazon Developer Docs 는 `Updated 11 days ago` 로 표기한다.
- **deprecated 는 3 단계로 구분하고 출처보다 강한 주장을 하지 않는다.**

  | 단계 | 정의 | 출처 |
  | --- | --- | --- |
  | deprecated | *"no longer in active development as of the deprecation date"* — 호출은 아직 된다 | Amazon SP-API |
  | sunset / maintenance | *"should plan to migrate … typically 12 months"* | AWS service lifecycle |
  | removed / shutdown | *"calls to the resources fail as of the removal date"* / *"completely removed"* | Amazon SP-API, AWS |

  Google Cloud 는 *"After a service, feature, or product is officially deprecated, it continues to be available for at least the period of time defined in the Terms of Service."* 라고 명시한다 — **deprecated ≠ 사용 불가**. `"권장하지 않음"` 을 `deprecated` 로 승격시키는 것은 날조다.

### P8. 형식이 곧 결정성이다

같은 질문에 같은 답이 나오게 하는 유일한 수단은 **출력 템플릿 고정**이다.

> *"Provide templates for output format. Match the level of strictness to your needs."*
> *"ALWAYS use this exact template structure:"*
> — Anthropic Agent Skills best practices, [platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices]

같은 논리가 SRE 의 런북에도 있다.

> *"Each alert condition in your system should have a corresponding playbook entry that describes the steps to recovery."* — [sre.google/workbook/data-processing/]
> *"…an easy-to-follow and well-defined set of steps…"* — [sre.google/sre-book/being-on-call/]

체크리스트 방법론에서 가져올 것: **READ-DO(실행 지시형) vs DO-CONFIRM(사후 검증형) 구분**, 한 묶음 5~9 항목 상한, **killer item**(누락 시 치명적인 항목) 표시. *근거 등급 주의 — 1차 출처(Gawande 원저/항공 체크리스트 설계 문서)를 확보하지 못했고 공개 요약본을 인용했다. §11 참조.*

---

## 4. 고정 스텝 계약 (Step Contract)

**대화 모드와 문서 모드가 같은 스키마를 쓴다.** 렌더링만 다르다.

```yaml
step:
  id: string                      # S1, S2, …
  condition: string | null        # 이 스텝을 실행하는 객관 조건. 항상이면 null (생략 렌더링)
  mode: READ_DO | DO_CONFIRM      # 실행 지시형 / 사후 검증형
  where:
    entry_url: string | null      # 딥링크. 있으면 이것이 1순위
    path: [string]                # ["Settings","General","Cloud Messaging"] — 중간 단계 전부
    container: string | null      # left sidebar / top tab / dialog / upper-right / bottom of page
  what:
    verb: 이동|열기|선택|누르기|입력|체크|토글|저장|다운로드|업로드
    target_label: string          # 화면에 그대로 보이는 라벨
    target_label_i18n: string|null# 한국어 UI 라벨 (영문이 정본, 한국어는 괄호)
    target_type: 버튼|필드|탭|토글|드롭다운|체크박스|링크|메뉴|섹션
  value: string | null            # 입력값/선택지. 없으면 명시적으로 "입력 없음"
  constraints: string | null      # 형식/길이/범위/기본값
  verify: string                  # 이 스텝이 끝났음을 눈으로 확인하는 관측값 (필수)
  if_not_found:                   # P6 — 선제 분기. 최소 1개
    - cause: 권한|요금제|버전|언어|A/B
      then: string
  killer: boolean                 # 누락 시 치명적인가
  source:
    url: string | null
    fetched_at: date | null
    tier: 관측 | 문서 | 추정 | 없음
```

### 필수/선택

`verify` 와 `source.tier` 는 **모든 스텝에 필수**다. DITA 는 `<stepresult>` 를 *"should not be used for every step"* 이라고 하지만, 이 킷이 막으려는 실패가 **무증상 실패**(절차를 다 따랐는데 아무 일도 안 일어남 — `bambu_studio_json_import.md:24` *"silent skip이 가장 위험한 실패 모드 — 에러 없이 0건 import"*)이므로 예외를 두지 않는다. 이것은 표준을 어기는 것이 아니라 **이 도메인의 실패 데이터에 근거해 강화**한 것이다.

### 절차 전체 골격 (DITA task 모델)

```text
prereq   사전 요구사항 · 필요한 계정/권한/준비물 · 사이트 배정표
context  이 절차가 무엇을 달성하는가 (1~2문장)
steps    Step Contract 배열
result   전부 끝났을 때의 관측 가능한 최종 상태
postreq  뒤처리 · 되돌리기 · 파기해야 할 것
```

> *"before starting the current task"* — DITA `<prereq>` / 콘텐츠 모델은 `<prereq>?, <context>?, (<steps>|<steps-unordered>)?` 순서 — [docs.oasis-open.org/dita/dita/v1.3/os/part2-tech-content/contentmodels/cmtct.html]

---

## 5. 출처 등급제 (Provenance Tier) — "검증 불가 → 침묵"의 대체물

| 등급 | 의미 | 표기 | 허용되는 문장 |
| --- | --- | --- | --- |
| `관측` | 사용자가 지금 화면을 읽어줬거나 스크린샷을 줬다 | 표기 생략(최고 등급) | 무엇이든 단정 가능 |
| `문서` | 공개 1차 출처에 그 라벨이 실제로 적혀 있다 | `[문서 2026-09-07]` | 라벨·경로·필드명 단정 가능 |
| `추정` | 출처에 없고 모델 지식 기반 | `[추정]` **표기 필수** | 단정 금지, "대개 …에 있습니다" |
| `없음` | 확인 실패 | `[미확인]` + 시도한 URL | 이 경우에만 전역 검색어로 우회 |

**핵심 규칙**: `추정`은 금지 대상이 아니라 **라벨 대상**이다. 출처가 다른 정보를 같은 등급으로 섞어 파는 것이 부정직이지, 등급을 붙여 파는 것은 부정직이 아니다.

**상한**: 한 절차에서 `추정` 이 액션 스텝의 40% 를 넘으면 그대로 내보내지 않는다 — 사용자에게 화면 확인을 요청하거나(§6 화면 폐루프) 미확인으로 강등한다.

### 화면 폐루프 (Screen-in-the-loop) — 대화 모드의 고유 강점

로그인 뒤 화면은 도구로 못 본다. **하지만 사용자는 지금 그 화면을 보고 있다.** MD 생성 전용이던 기존 킷에서는 못 쓰던 채널이다.

1. `문서` 등급으로 확정 가능한 지점까지 끊지 않고 안내한다.
2. 거기서 **한 번만** 묻는다 — "지금 그 화면에 보이는 항목을 그대로 읽어 주세요."
3. 사용자가 읽어준 라벨은 `관측` 등급으로 승격되고, **세션 내에서 재사용**한다 (같은 콘솔에서 다시 묻지 않는다).

되묻기를 늘리는 것처럼 보이지만 실제로는 줄인다 — 지금은 사용자가 못 찾아서 되묻는 왕복이 더 많다.

---

## 6. 결정론 게이트 (LLM 호출 없는 순수 판정)

기존 킷의 G1~G4 중 **G2 만 그대로 승계**하고, 나머지는 재작성한다. 신설 G5·G6 이 이 킷의 존재 이유다 — 기존 게이트 어디에도 **입도를 재는 검사가 없었다.**

| ID | 검사 | 실패 조건 | 승계 |
| --- | --- | --- | --- |
| **G1** | 출처 원장 완전성 | 액션 스텝 수 ≠ 출처 줄 수 | 재작성 (헤더 형식 비종속) |
| **G2** | 미검증 마커 분류 | 접미 없는 레거시 마커 ≥1, 또는 `INVALID` 가 정본 임계 이상 | **그대로** |
| **G3** | 도메인 혼용 | 요청 대상과 다른 플랫폼 경로 혼입 (iOS 안내에 Android 경로 등) | 재작성 (기존 G3 는 `stack≠flutter` 면 항상 PASS 하는 no-op) |
| **G4** | deprecation 근거 결합 | deprecated 주장을 한 스텝의 출처가 그것을 뒷받침하지 않음 | 재작성 — **영문 토큰 종속 제거** (한국어 "지원 종료/폐지/중단" 인식) |
| **G5** | **말단 액션 (신설)** | 종결 동사로 끝나지 않는 스텝 ≥1. `이 섹션에서`·`해당 항목을`·`적절히`·`알아서` 로 끝나는 스텝 0 건 요구 | 신설 |
| **G6** | **입도 완전성 (신설)** | `verify` 없는 스텝 ≥1 · `if_not_found` 없는 스텝 ≥1 · `추정` 비율 > 40% · `source.tier` 미표기 ≥1 | 신설 |

- 게이트 출력 전문을 보고에 붙인다. "게이트 통과함"은 증거가 아니다.
- 게이트를 우회하거나 조건을 느슨하게 고치지 않는다. 정당한 케이스를 막는다고 판단되면 사용자에게 보고하고 판단을 받는다.
- 게이트는 기계 판정 가능한 것만 잡는다. **사실 정확성·경로 날조는 여전히 Gotchas 와 검증 단계의 몫이다.**
- 임계 숫자는 `harness/docs/guides/qa-evaluation-guide.md` §카운팅 및 자동 REJECT 임계가 정본이다. **이 킷에서 재정의하지 않는다** (킷별 재정의가 같은 상태를 다른 판정으로 가르는 실측 drift 를 낳았다: 2/3/0 건).

### 소급 재측정 (Regeneration Drift)

절차 문서는 영속 아티팩트라 규칙이 바뀌면 이미 나간 산출물이 조용히 위반 상태가 된다 (`onboarding-kit/skills/setup-guide/SKILL.md:46` — 쇼케이스가 자기 evals 6 중 3 을 **3 개월간** 위반한 채 배포). 문서 모드 산출물에는 **기존 산출물 전수 재게이트**를 실행 초입에 둔다. `find` 를 쓴다 — zsh 는 `nomatch` 가 기본이라 매치 0 인 글로브가 명령을 통째로 죽인다.

---

## 7. 킷 구성

### 이름: `howto-kit`

근거: 사용자의 실제 발화가 "~하는 법", "어떻게 해?" 이고 슬래시 커맨드 `/howto` 가 가장 자연스럽다. 또한 이 킷의 산출물은 Diátaxis 의 **how-to guide** 정의(*"guide the reader through a problem or towards a result"*)와 정확히 일치하므로 문서이론상 앵커도 있다. 기존 킷 이름들과 충돌하지 않는다.

차점 `runbook-kit` — 정확하지만 SRE/운영 색이 강해 "등본 떼는 법"을 묻는 사용자와 결이 어긋난다. `guide-kit` 은 레포에 이미 `*-guide` 스킬이 8 개라 검색성과 트리거 정밀도가 떨어진다.

*킷이 아직 안 만들어졌으므로 이름 변경 비용은 0 이다. 다음 세션에서 바꿔도 된다.*

### 스킬 3 + 에이전트 1

| 이름 | 역할 | 산출물 |
| --- | --- | --- |
| `/howto` | **기본 모드.** 대화창에서 Step Contract 로 즉답. 선행 질문은 한 번에 묶어서 1 회. 화면 폐루프 사용 | 대화 텍스트 (파일 없음) |
| `/howto-doc` | 사용자가 "문서로 남겨줘"라고 할 때만. 같은 Step Contract 를 MD 로 렌더 + 게이트 실행 | MD 파일 |
| `/howto-audit` | 이미 있는 절차 문서/가이드를 4 요소·출처 원장·G1~G6 기준으로 재측정 | 판정 리포트 |
| `howto-reviewer` (에이전트) | `/howto-audit` 에서 호출. 읽기 전용 독립 평가 | PASS/FAIL |

**별도 interview 스킬을 두지 않는다.** 선행 질문은 `/howto` 내부의 한 단계다 — 분리하면 되묻기 왕복이 오히려 늘어난다.

### 선행 질문 정책

한 번에 묶어 2~4 문항. 답을 이미 알 수 있으면 묻지 않고 가정을 명시한다.

**개발 절차 축**: 스택 · 플랫폼/OS · 환경(로컬/CI/프로덕션) · 기존 설정 유무
**일상 절차 축**: 기기/OS 버전 · 국가/언어 · 계정 등급/권한 · 웹 vs 앱 · 본인인증 수단

일상 절차에서 확인된 필수 축(2026-09-07 실측):

- **사이트 배정** — 주민등록등본=정부24 / 가족관계증명서=대법원 전자가족관계등록시스템 / 소득금액증명=홈택스. 서로 다른 사이트다. Apple 의 Developer Portal vs App Store Connect 와 같은 유형의 함정이고, 사전 요구사항 맨 위에 **작업별 배정표**로 박아야 한다.
- **본인인증 수단** — 정부24 는 *"간편인증 또는 인증서(공동, 금융)"* 로 열거한다. 어느 수단을 쓸지가 화면 흐름을 가른다.
- **온라인으로 안 끝나는 경우** — 정부24 는 `신청방법: 인터넷, 방문, 우편, 무인발급기` · `처리기간: 지체없이` · `수수료: 등본 1000원, 초본 500원` 을 개요 항목으로 구조화한다. 이 세 필드를 절차 헤더에 승계한다.
- **언어 라벨** — 영문이 정본, 한국어는 괄호. 실측 대조: `Settings > General > About` ↔ `설정 > 일반 > 정보` [support.apple.com/en-us/109065 ↔ /ko-kr/109065]

---

## 8. SKILL.md 규격 (2026-09 현행)

`platform.claude.com` 표준과 Claude Code 확장이 다르다. 이 킷은 **Claude Code 전용**을 택한다 (확장 필드를 쓰기 위해).

| 구분 | 필드 |
| --- | --- |
| 표준 필수 | `name` (≤64자, 소문자·숫자·하이픈, `anthropic`/`claude` 예약), `description` (≤1024자, 3인칭) |
| 이 레포 필수 | `user-invocable` — `scripts/validate-plugin.py` V1 이 `name`/`description`/`user-invocable` 3 종을 강제 |
| Claude Code 확장 | `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `allowed-tools`, `disallowed-tools`, `model`, `effort`, `context`, `agent`, `background`, `hooks`, `paths`, `shell`, `metadata`, `license`, `compatibility` |

- 본문 **500 줄 이하** 권고. 넘으면 `references/` 로 분리한다. *"Keep SKILL.md body under 500 lines"*
- Progressive disclosure — *"Files don't consume context until accessed"*. metadata 만 상시 로드, 본문은 트리거 시, references 는 필요 시.
- description 은 요약이 아니라 **트리거 판별문**. 3 인칭 필수 (*"Always write in third person."*), 비트리거 조건 최소 1 개 포함.
- `plugin.json` 은 `name` 만 필수. marketplace 엔트리는 `name` + `source` 필수.
- `allowed-tools` 는 스킬이 호출된 턴 동안만 유효하고 다음 사용자 메시지에서 해제된다. **`/howto` 와 `/howto-audit` 은 읽기 전용, `Write` 는 `/howto-doc` 에만 준다.**

### 아키타입 판정

`harness/docs/guides/skill-design-guide.md` 의 카탈로그(문서 제목은 "9가지"이나 표는 11 행 — 10~11 은 이 레포 운영 경험에서 추가)에 **"범용 절차 가이드" 전용 슬롯이 없다.** Type 1(라이브러리 레퍼런스: 사용법 + 함정)이 정의상 가장 가깝고, Type 8(런북)은 "장애 시 자동 조사"라 트리거가 다르다. 다음 세션에서 **12번째 아키타입 "절차 안내형(Procedural Guidance)" 신설을 제안**할지 판단할 것.

---

## 9. 흡수해야 할 기존 교훈

이미 로컬 메모리·규칙에 적혀 있고 신규 킷이 반드시 승계해야 하는 것들. 재발명 금지.

1. 절차를 쓰기 전에 **환경·버전을 먼저 확정**하라. 자동 감지 실패 시 선택지를 제시해 묻는다. — `feedback_setup_guide_stack_first.md`
2. **사용자가 이미 확인했다고 말한 사실은 재검증하지 마라.** — `feedback_user_confirmed_facts.md`
3. **로컬 설치본을 기준값으로 쓸 때는 버전 확인을 첫 단계에.** 읽은 값은 정확해도 그 시점의 값이다. — `feedback_local_install_baseline_staleness.md`
4. **조회했다는 주장은 도구 호출 기록으로만 성립한다.** — `feedback_skill_invocation_evidence.md`, `reflections-2026-05.md:18733`
5. **1차 출처가 deprecated 라고 말하지 않은 것을 deprecated 로 쓰지 마라.** 출처보다 강한 주장은 날조다. — `search-strategy.md:88`
6. **사이트가 갈리는 서비스는 사전 요구사항 맨 위에 작업별 표를 박아라.** — `feedback_setup_guide_site_distinction.md`
7. **한국어 라벨은 번역 추정이다. 영문을 정본으로, 한국어는 괄호.** — `format-checklist.md:117`
8. **각 단계에 관측 가능한 확인 지점을 붙여라.** 무증상 실패가 가장 위험하다. — `bambu_studio_json_import.md:23-24`, `bambu_ironing_type_enum.md:13`
9. **같은 규칙을 여러 문서에 재서술하지 마라.** 정본 한 곳을 인용하라. 재서술은 반드시 갈라진다. — `qa-evaluation-guide.md:1004-1013`
10. **추측 fallback 을 두지 마라.** 확정 실패 시 조용히 기본값으로 떨어지면 같은 입력이 환경마다 다른 답을 낸다. — `reflect-kit/hooks/_lib-tag-canon.sh:40-45`
11. **공통 전제는 헤더에서 1 회 선언**하고 개별 항목은 참조만. 항목마다 붙이면 하나를 빠뜨린다. — `feedback_shared_premise_to_header.md`
12. **값을 정정한 뒤에는 옛 값 전수 검색으로 검증하라.** `grep -rn "<옛 값>"` 이 0 인가. sweep 은 검사 범위 크기부터 출력한다. — `feedback_verify_absence_not_presence.md`
13. **지표가 주장과 같은 것을 재는지 먼저 확인하라.** "0 건"은 통과가 아니다 — 빈 범위·잘못된 대상도 0 으로 보인다. — `feedback_metric_must_match_claim.md`
14. **오라클은 서술 존재가 아니라 실행 결과다.** 셸 스니펫은 zsh·bash 양쪽에서 실제로 돌려라. — `feedback_oracle_must_execute_not_grep.md`
15. **요청한 그 범위만 다뤄라.** 섹션 목록은 포맷 표준이지 채우기 할당량이 아니다. — `onboarding-kit` Gotcha 7

---

## 10. 다음 세션용 Sprint Contract (초안)

**공통 전제 (헤더 1회 선언)**: 산출물은 `howto-kit/` 신규 플러그인. 기존 `onboarding-kit` 은 건드리지 않는다. 모든 문서는 한국어. 검증 명령은 `python3 scripts/validate-plugin.py howto-kit`.

| # | 완료 조건 | 측정 방법 |
| --- | --- | --- |
| C1 | `howto-kit/.claude-plugin/plugin.json` 존재, `name`/`version`/`description` 채워짐 | 파일 존재 + `python3 -c "import json;json.load(open(...))"` 성공 |
| C2 | 스킬 3 개(`howto`, `howto-doc`, `howto-audit`) SKILL.md 존재, 각 frontmatter 에 `name`/`description`/`user-invocable` | `validate-plugin.py` V1 통과 |
| C3 | 에이전트 `howto-reviewer.md` 존재, 도구가 읽기 전용으로 스코프됨 | frontmatter `tools` 에 Write/Edit 없음 |
| C4 | Step Contract 스키마가 `references/step-contract.md` 에 정본으로 1 곳만 존재 | `grep -rn "step_id\|target_label" howto-kit/` 결과가 references 1 파일에 집중 |
| C5 | G1~G6 게이트가 셸 함수로 구현되고 **zsh·bash 양쪽에서 실행**됨 | 두 셸에서 각각 실행한 출력 전문 첨부 |
| C6 | G5(말단 액션)·G6(입도) 각각에 대해 **양성 케이스 1 건**(일부러 위반한 입력)이 FAIL 을 내는 것을 실행으로 증명 | 실패 출력 첨부 — 오탐 통과만으로는 게이트 생존 증명 안 됨 |
| C7 | evals 에 **입도 assertion** 포함 — 종결 동사 검사, `verify` 필드 존재, 분기 존재 | `evals.json` 케이스 수 ≥ 6, 그중 입도 케이스 ≥ 2 |
| C8 | `.claude-plugin/marketplace.json` 에 등록 | 파일 diff |
| C9 | 루트 `CLAUDE.md` Repository Overview + Skills Reference 에 추가 | 파일 diff |
| C10 | `python3 scripts/sync-docs.py howto-kit` 실행 후 README AUTO 블록 갱신 | 명령 출력 |
| C11 | `docs/howto-kit/` HTML 페이지 + `docs/index.html` 등록 | `/docs-site` 실행 결과 |
| C12 | `.claude/skills/howto-kaizen` + `howto-research` 생성 | 파일 존재 |
| C13 | `kaizen-orchestrator` 에 Phase 추가 | 파일 diff |
| C14 | qa-evaluator APPROVE | 판정 리포트 |

**비범위**: `onboarding-kit` 개명·삭제 · 기존 `docs/onboarding-kit/` 산출물 수정 · 실제 절차 문서 생산.

---

## 11. 확인 못 한 것 (킷이 사실로 말하면 안 되는 것)

정직하게 남긴다. 다음 세션이 이 목록을 먼저 메워도 좋다.

1. **체크리스트 방법론의 1차 출처를 확보하지 못했다.** READ-DO/DO-CONFIRM, 5~9 항목, killer item 은 공개 요약본(shortform.com) 인용이다. Gawande 원저나 항공 체크리스트 설계 문서(FAA/Boeing)로 교체해야 한다.
2. **ISO/IEC/IEEE 26514·26515 의 절차 작성 세부 조항**은 공개 OBP 에서 정의·개요만 확인했다. 전문은 유료 접근이 필요할 수 있다.
3. **UI 필드의 placeholder 텍스트 문서화 규정**을 지정 출처 범위에서 확인하지 못했다. Google 의 placeholder 규정은 CLI command 쪽에서만 확인됐다.
4. **Google Cloud 정책 문서 안에서 `not recommended`/`sunset`/`removed` 를 각각 별도 공식 용어로 정의한 문장**과 Apple 의 동등한 정의를 확인하지 못했다. 3 단계 구분은 AWS·Amazon SP-API 근거로 세웠다.
5. **권한 관련 Microsoft Learn 인용 2 건은 이 브리프에서 제외했다.** 리서치가 돌려준 URL 에 `%20` 이 경로 안에 섞여 있어 링크가 깨졌을 가능성이 있다 (*"If you're missing permissions, the resource group is greyed out"*, *"If you don't see the option to grant permission, ask an admin…"*). 재확인 후 P6 근거로 추가할 것. 지금 P6 는 Apple·Atlassian·GitHub 3 건으로만 서 있다.
6. ~~**RSS/변경 로그 피드 URL 실측을 완료하지 못했다.**~~ **2026-09-09 해소 (부분).** 5 건을 루트 엘리먼트 실측으로 확정했고 3 건(Firebase · Stripe · Azure updates)이 확인 실패로 남았다. 정본은 `docs/howto/changelog-feeds.md`, 미확인 원장은 `howto-kit/references/provenance-notes.md` §3.
7. **후보 이름의 marketplace/GitHub/npm 충돌 검사**를 하지 않았다.
8. **로그인 뒤 화면을 Playwright MCP 로 스냅샷하는 경로**(사용자 동의 + 이미 로그인된 브라우저 프로필)는 아이디어 단계다. 실증하지 않았다. 등급 사다리의 최상단 후보로만 적어 둔다.

---

## 12. 부록 — 이 브리프를 만든 리서치의 실패 기록

솔직히 남긴다. 이 킷이 막으려는 실패를 리서치 과정에서 그대로 재현했기 때문이다.

Codex 리서치 7 회 중 5 회가 `turn_aborted / reason: "interrupted"` 로 죽었다. 레이트리밋이 아니었다(`primary 28~30%`, `rate_limit_reached=None`). 원인은 **동시 실행 충돌** — 새 codex 작업이 뜨면 돌고 있던 작업이 1.4 초 안에 죽고 마지막 것만 살아남는다.

```text
12:00:38.836 ABORT p2  →  12:00:40.281 START p3
12:08:27.336 ABORT p4  →  12:08:28.666 START p5
12:08:48.034 START p6  →  12:09:23.537 ABORT p5      (p6 만 생존)
```

더 나쁜 것은 **companion 이 abort 를 감지하지 못한다**는 것이다. 턴은 12:00 에 죽었는데 job 상태는 **19 시간 동안** `running / investigating` 이었다. 죽은 것을 산 것으로 보고했다.

교훈 2 개를 킷 설계에 반영했다:

- **작업 상태를 도구 요약으로 믿지 마라.** `status` 가 "running" 이라고 말해도 실제 이벤트 로그(`~/.codex/sessions/**/rollout-*.jsonl`)에 `turn_aborted` 가 있으면 그건 죽은 것이다. → §6 "게이트 출력 전문을 붙인다"와 같은 원리.
- **범위를 좁히는 것이 항상 답은 아니다.** 성공한 작업(19·22 회 검색)이 실패한 작업(7·8·14 회)보다 검색을 더 많이 했다. 실패 원인을 잘못 짚으면 축소가 아무 효과가 없다. → §1 F1~F4 를 증거로 특정한 이유.

**codex 운용 규약**: 한 번에 하나만, foreground, 도는 동안 다른 codex 를 띄우지 않는다. 이 규약을 지킨 재시도는 같은 프롬프트로 **1 분 만에** 완주했다.
