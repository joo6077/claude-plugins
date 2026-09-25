---
feature: "카이젠 2026-09-24 Phase 14 계약 — 막는 요구에 출처 · 막히는 것 · 우회 · `guide_gate` 시험 입력을 돌리는 러너 · 값이 든 .env 를 열지 않음"
slug: kaizen-0924-p14-onboarding-kit
created: "2026-09-25 09:55"
complexity: "복잡"
conditions: 28
status: active
owner_session: de8c7935-a5b6-4df5-9106-fafa73c288a0
conditions_digest: sha256:e90190048db61bfa
locked_at: "2026-09-25 11:00"
---

## 배경

이 Phase 의 외부 근거는 `.harness/.meta/evidence/phase14.md` 하나다. 처리 배정표(`.claude/kaizen-input/insights-report.md`)에서 `배정` 칸이
`Phase 14` 인 행은 `other-kits:P3` 와 `other-kits:P9` 둘이다. 적용 힌트는 「등록 안 된 시험 입력을 돌리는 자리에 넣고, 막는 요구에 출처와 우회를
함께 적는다」 다. `F10` 은 Phase 1 배정이지만 비고가 「셋업 가이드 쪽은 other-kits:P9(Phase 14)」 로 이 Phase 를 가리킨다. 러닝북 `Phase 별 추가 과제`
에 Phase 14 줄은 없다. 앞 Phase notes 가 Phase 14 로 넘긴 줄은 Phase 1 의 하나다. 오케스트레이터 Step 14 는 「Phase 1 에서 설계 가이드가 변경되었으면
onboarding-kit 전 스킬을 전수 감사한다」 고 적는다 — 그 감사 결과는 `GAP 분석` 절 둘째 표에 있다.

| 키 · 출처 | 내용 | 이번 처리 |
| --- | --- | --- |
| `other-kits:P3` | 자동 검사에 howto-kit 시험 단계, onboarding-kit 의 등록 안 된 시험 입력 3 개. 비고: howto-kit 단계는 Phase 17 과 함께 넣고, ci.yml 은 인사이트 스프린트가 고친 판 위에 더한다 | 반영 — 픽스처 셋을 `evals.json` `gate_cases` 에 등록(SK-04), 등록된 입력을 zsh · bash 로 돌리는 러너 새 파일(SK-06 · ER-04 · DG-04), G1 · G2 · G3 양성 대조 픽스처 하나(SK-05). CI 줄은 러닝북이 Final 몫으로 정했다 — notes 넘김 표에 넣을 줄을 적는다(ER-03). howto-kit 단계는 Phase 17 몫 |
| `other-kits:P9` | setup-guide 의 막는 요구에 출처 · 막히는 것 · 우회를 함께 | 반영 — format-checklist §2 세 칸 규칙과 FCM iOS 예(SK-01), SKILL.md Gotcha 9 · Phase 4 확인 항목(SK-02), 평가 사례(SK-03) |
| `F10` 비고 | 앱이 안 올라갔다 · 실기기가 없다로 불가능 선언. 셋업 가이드 쪽은 other-kits:P9 | `other-kits:P9` 와 한 번에 — Gotcha 9 셋째 줄이 스킬 자신이 「못 만든다」 고 결론 낼 때도 §3.7 조항 3 의 네 칸을 먼저 적게 한다(SK-02) |
| `phase1-notes.md` 넘김 표 | `onboarding-kit/skills/setup-guide/SKILL.md:30` 「마커 + 사유 한 줄」 | 반영 — SK-08 |

## 리서치 소스

근거 파일 `.harness/.meta/evidence/phase14.md` 에서만 가져왔다. 새로 찾은 자료는 없다.

- [Firebase — Add Firebase to your Apple project](https://firebase.google.com/docs/ios/setup) — 일반 실행은 실기기 · 시뮬레이터 둘 다 되지만 Cloud Messaging 을 쓰면 실제 Apple 기기를 준비하라고 따로 적는다 (SK-01 · SK-02 · SK-03)
- [Apple — Supported capabilities (iOS)](https://developer.apple.com/help/account/reference/supported-capabilities-ios) — Push notifications 가 유료 두 열에 있고 무료 `Apple Developer` 열에 없다 (SK-01)
- [Apple — Programs overview](https://developer.apple.com/help/account/membership/programs-overview) — 일반 앱 개발과 개인 기기 시험에는 멤버십이 필요 없다 (SK-01)
- [Apple Developer Program enrollment](https://developer.apple.com/programs/enroll/) — 비영리 · 공인 교육기관 · 정부 기관 가입 비용 면제 경로 (SK-01)
- [Apple — Testing notifications using the Push Notification Console](https://developer.apple.com/documentation/usernotifications/testing-notifications-using-the-push-notification-console) — 개발 환경에서 기기 토큰으로 시험 발송이 된다. 앱 출시가 선행 조건이라는 근거는 없다 (SK-01 · SK-03)
- [Firebase — Get started with FCM in Flutter apps](https://firebase.google.com/docs/cloud-messaging/flutter/get-started) — 새 픽스처의 출처 줄 (SK-05)
- [GitHub Actions runner-images](https://github.com/actions/runner-images) · [Ubuntu 24 이미지 20260920.314](https://github.com/actions/runner-images/releases/tag/ubuntu24/20260920.314) — `ubuntu-latest` 는 24.04 이고 zsh 는 제공 목록에 없다. 그래서 CI 줄은 `command -v zsh` 로 보고 없을 때만 설치한다 (ER-03 넘김)
- 내부: 데이터 풀 §0.5 탈락 목록의 `feedback-no-read-env` (grounding `user_correction`) — 값이 든 `.env` 를 열지 말고 키 이름은 예시 파일 · 코드에서 얻는다 (SK-09)
- 내부: `harness/docs/guides/skill-design-guide.md` §3.7 조항 3 네 칸 · 「0 이 기대값인 검증의 양성 대조」 · 「알려진 답 대조」 (Phase 1 결과) — SK-02 · SK-05 · SK-08 · AR-02
- 내부: `howto-kit/evals/run-evals.sh` — 두 셸 출력을 대조하는 러너 선례. 구조만 따르고 코드는 가져오지 않았다 — 킷은 따로 설치되므로 다른 킷 파일을 부르면 깨진다

## GAP 분석 · 개선안 초안

복잡도 4 축 (Step 1). 두 축 이상이 예이고 계약 변경과 소비면이 둘 다 예라 **복잡** 이다 — Step 2.5 양면 조건을 넣었다.

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 셋 — 스킬 문서(SKILL.md · references 둘 · README) · 평가 데이터(evals.json · 픽스처) · 실행 스크립트(러너) |
| 공개 API·계약 변경 | 밖에서 읽는 형식이 바뀌는가 | 예 — `evals.json` 에 `runner` · `gate_cases` 필드가 생기고, 생성하는 가이드의 사전 요구사항 형식(세 칸)이 바뀐다 |
| 소비면 존재 | 반대편이 있는가 | 예 — `gate_cases` 를 읽는 새 러너(이번에 만든다) · CI(범위 밖, 넘김) · 배포 예제 `docs/onboarding-kit/examples/fcm-ios-setup-guide.md`(범위 밖, 넘김) · 이 Phase 가 바꾸는 세 소스(SKILL.md · format-checklist · project-detection)에서 만든 문서 사이트 페이지 셋 `docs/onboarding-kit/setup-guide.html` · `docs/onboarding-kit/format-checklist.html` · `docs/onboarding-kit/project-detection.html`(범위 밖, Final F2 넘김 — `scripts/detect-docs-drift.py` 에 onboarding-kit 매핑이 없어 드리프트 목록에 안 나온다). 레포 스크립트 셋은 `<킷>/evals/` 만 읽어 이 파일을 안 읽는다 — `scripts/run-evals.py:54` · `scripts/sync-evals.py:36` · `scripts/sync-docs.py:171` |
| 회귀 위험 | 기존 동작이 깨질 경로 | 낮음 — `guide_gate` 함수는 고치지 않고(AR-03), 기존 평가 사례 다섯은 글자 그대로 둔다(SK-03) |

설정 리터럴 대조표 (Step 1.2, `.harness/project.yaml` 원문):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A 사유에 그대로 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A 사유에 그대로 |
| `diagnostics.ide_exclude` | `[]` | DG-02 에 그대로 |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 그대로 |
| `anti_patterns[].id` / `message` | AP-01 · AP-02 · AP-03 · AP-04 | AP-01 · AP-03 · AP-04 — 메시지 원문 그대로. AP-02(force push)는 이 Phase 가 푸시하지 않아 뺐다 |

편집 전 감사 (Step 1.4, 대상 파일을 실제로 읽은 줄):

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 여부 |
| --------- | ---------------------------- | ------------------- | ---------------- |
| `onboarding-kit/skills/setup-guide/SKILL.md` | `:30` 「마커 + 사유 한 줄」 · `:40` 네 요건 · `:116`~`:120` `### Guide Conformance Gate (E3)` 절 끝 목록 · `:165` `com.fitpal.app` · `:197` 탐색 목록의 `.env*` · `:201` 「기존 `.env` 에 다른 이름의 키가 있는데」 · `:210` Phase 1 둘째 항목 `.env*` · `:252`~`:259` Phase 4 목록 여섯 항목 | `:30` 이 같은 절 `:40` 네 요건 · §3.7 네 칸과 어긋난다. `### Guide Conformance Gate (E3)` 절에 시험을 돌리는 자리가 없다. 킷 파일에 앱 이름. 값이 든 `.env` 를 여는 것을 막는 줄이 없고 세 곳이 오히려 `.env*` 를 읽게 이끈다. 막는 요구 규칙 · 확인 항목이 없다 | SK-02 · SK-07 · SK-08 · SK-09 · ER-02 |
| `onboarding-kit/skills/setup-guide/references/format-checklist.md` | `:14`~`:22` §2 사전 요구사항 — 「필요한 계정/권한 (예: Apple Developer Program 가입)」 한 줄과 박스 둘 | 막는 요구를 출처 · 막히는 것 · 우회로 좁히는 규칙이 없다. 첫 목록의 계정/권한 줄이 새 규칙이 막는 「한 줄 요구」 모양 그대로다 | SK-01 |
| `onboarding-kit/skills/setup-guide/references/project-detection.md` | `:42` 「`.env*` — 환경변수에서 외부 서비스 키 흔적」 | `.env` 를 열어 키를 보게 이끈다 | SK-09 |
| `onboarding-kit/skills/setup-guide/evals/evals.json` | `:1`~`:126` 사례 여섯, `gate_cases` 없음 · `:104`~`:123` `no-invented-paths` 가 `.env` 만 두고 키 인용을 요구 | 픽스처를 부르는 자리가 없다. 사례가 `.env` 를 읽게 이끈다 | SK-03 · SK-04 · SK-09 |
| `onboarding-kit/skills/setup-guide/evals/fixtures/` 셋 | `gate-ok-flutter.md:1`~`:20` · `gate-g4-ko-sourced.md:1`~`:10` · `gate-g4-ko-unsourced.md:1`~`:9`. `grep -rln 'gate-ok-flutter\|gate-g4-ko' --exclude-dir=.harness --exclude-dir=.git .` 가 0 줄 | 폴더에만 있고 아무도 안 돌린다. 셋 다 G1 · G2 · G3(Swift 쪽)의 0 · 같은 수 기대값만 낸다 — 이 셋이 살아 있다는 양성 대조가 없다 | SK-04 · SK-05 · SK-06 |
| `onboarding-kit/README.md` | `:42` 「`/kaizen` (Phase 13으로 자동 실행)」 | 오케스트레이터 Step 14 · onboarding-kaizen 은 Phase 14 다 | SK-07 |
| `onboarding-kit/skills/setup-guide/references/search-strategy.md` | `:1`~`:109` | 이번에 바꿀 곳이 없다 | AR-03 (그대로 둔다) |
| `.github/workflows/ci.yml` · `scripts/run-evals.py` | `ci.yml:46`~`:47` `run-evals.py --verbose` 뿐 · `run-evals.py:32`~`:35` `ALL_KITS` 에 onboarding-kit 없음 | onboarding 픽스처를 도는 단계가 없다 | 범위 밖 — ER-03 넘김 |
| `docs/onboarding-kit/examples/fcm-ios-setup-guide.md` · `docs/onboarding-kit/fcm-ios-example.html` | MD `:5` · `:29` Xcode 16+ · iOS 14+ · `:31` · `:370` · `:392` 시뮬레이터 주장 · `:30` · `:46` · `:381` · `:384` · `:385` 앱 이름. HTML `:249` · `:251` · `:605` | 근거 파일과 어긋나고(Xcode 26.2+ · iOS 15 · Cloud Messaging 은 실기기) 새 세 칸 형식이 아니다. `guide_gate` 는 통과한다(`GATE_PASS`, G1 steps=8 ledger=8) | 범위 밖 — ER-03 넘김 |
| `.claude/skills/onboarding-kaizen/SKILL.md` | `:37`~`:41` Phase 4 — `validate-plugin.py onboarding-kit` 만 | 러너를 모른다 | 범위 밖 — ER-03 넘김 |
| `docs/onboarding-kit/setup-guide.html` · `docs/onboarding-kit/format-checklist.html` · `docs/onboarding-kit/project-detection.html` · `scripts/detect-docs-drift.py` | `docs/index.html:524`~`:526` 에 세 페이지 등록 · `detect-docs-drift.py:33` `SOURCE_TO_HTML` · `:66` `SOURCE_OVERRIDES` 에 onboarding 이 0 줄 | 이 Phase 가 바꾸는 세 소스에서 만든 페이지인데 드리프트 검출이 못 본다 — 예행 판에서 `python3 scripts/detect-docs-drift.py --since da9fbae` 가 `no docs drift since da9fbae` | 범위 밖 — ER-03 넘김 |

Phase 1 결과 대조 (오케스트레이터 Step 14 전수 감사 — `skill-design-guide.md` 1.6.0):

| Phase 1 변경 | onboarding-kit 에서 본 자리 | 처리 |
| --- | --- | --- |
| §3.7 조항 3 — 검증 불가 시 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령) | SKILL.md `:30` 「사유 한 줄」 이 옛 말. `:40` 네 요건은 네 칸과 같은 내용 | SK-08 — `:30` 을 네 요건으로, `:40` 끝에 네 칸과의 대응 한 문장 |
| 작업 자체를 못 한다고 결론 내리기 전에도 네 칸 | 스킬 자신의 불가 결론에 대한 줄이 없다 | SK-02 Gotcha 9 셋째 줄 |
| 0 이 기대값인 검증의 양성 대조 | `guide_gate` 의 G1 · G2 · G3(Swift) 쪽 0 · 같은 수 기대값에 알려진 나쁜 예가 없다 | SK-05 새 픽스처 |
| 알려진 답 대조 | 새 러너가 내는 값 — 픽스처마다 손으로 센 기대 출력 다섯 줄 | SK-04 `expect` · SK-05 |
| 에이전트 frontmatter 18 종 | onboarding-kit 에 `agents/` 가 없다 | 해당 없음 |
| 500 줄 「권고」 | SKILL.md 265 줄 → 편집 뒤 약 280 줄 | 해당 없음 |

개선안 초안 — 정확한 문장은 조건 줄과 `m.sh` 토큰이 기준이다. 예행 도구 `mock.py`(스크래치 `p14d2/`)가 시작 커밋 판에 그대로 적용해 본 판이다.

1. **막는 요구 세 칸** (`other-kits:P9`) — format-checklist §2 끝에 규칙 한 단락 · 칸 표 · FCM iOS 예 표(실기기 · 유료 개발자 계정 · 앱 출시), 같은 절 첫 목록의 계정/권한 줄 끝에 「— 막는 요구면 아래 세 칸으로 쓴다」. SKILL.md 에 Gotcha 9(규칙 · 출처가 요구하지 않는 요구 금지 · 지어낸 우회 금지 · 스킬 자신의 불가 결론에도 §3.7 네 칸), Phase 4 목록 5 번 확인 항목(뒤 번호 하나씩 밀림). evals.json 에 사례 `blocking-requirement-scope`
2. **등록 안 된 시험 입력** (`other-kits:P3`) — `evals.json` 을 0.3.0 으로 올리고 `runner` 와 `gate_cases` 여섯(정상 · 스택 인자 없음 · 빈 스택 · G4 한국어 근거 있음 · 없음 · G1 · G2 · G3 동시 FAIL). 새 픽스처 `gate-fail-ledger-marker-swift.md`. 새 러너 `evals/run-gate-evals.sh` — 부를 때마다 SKILL.md 에서 `guide_gate` 를 뽑아 입력마다 zsh · bash 출력을 기대 출력 전체와 대조하고, 폴더에만 있는 픽스처 · 돈 수와 적힌 수의 차이를 실패로 센다. 도구 · 함수 추출 · 입력 목록이 없으면 종료 코드 2. SKILL.md `### Guide Conformance Gate (E3)` 절과 README 에 부르는 줄
3. **Phase 1 넘김** — SKILL.md `:30` 을 「마커와 아래 네 요건」 으로, `:40` 끝에 §3.7 조항 3 네 칸과의 대응 한 문장
4. **값이 든 `.env` 를 열지 않는다** (§0.5) — Gotcha 8 에 한 단락, `:201` 나쁜 예를 예시 파일 · 코드 기준으로, Phase 1 둘째 항목과 project-detection 을 `.env.example` 류로. `no-invented-paths` 사례에 `.env.example` 과 읽지 않음 단언
5. **작은 정정** — Gotcha 4 의 앱 이름을 `com.<앱이름>.app` 으로, README Phase 13 → 14

하지 않기로 한 것:

- 막는 요구 세 칸을 `guide_gate` 검사로 넣지 않는다. 형식이 새로 생겨 배포 예제(범위 밖)가 아직 옛 형식이라, 넣으면 예제가 바로 `GATE_FAIL` 이 된다. 예제를 Final 이 고친 뒤 다음 사이클에 본다(notes 다음 사이클 메모)
- 러너를 howto-kit 러너와 합치지 않는다 — 킷은 따로 설치된다
- evals.json `source` 조회일(`Last updated 2026-07-20 UTC`)을 옮기지 않는다 — 근거 파일은 페이지 갱신일만 다시 봤고 본문 주장(.p12 를 deprecated 로 적지 않음 · Instance ID)을 다시 확인하지 않았다(ER-03 미반영)

## 범위 경계

- 이 Phase 시작 HEAD: `da9fbae94c13a9a1fc657f29ce9fc380ba9d506b`. 범위 상한은 개정 파일 `.harness/sprint-amendments-kaizen-0924-p14-onboarding-kit.md` 의
  `end_sha:` 마지막 값이다. 여러 Phase 가 같은 가지 `kaizen/2026-09-24` 에 동시에 커밋하므로 `HEAD` 로 재지 않는다
- 고치는 파일은 일곱이고 그 가운데 둘(러너 · 새 픽스처)이 새 파일이다 — 아래 블록이 그 목록이다(`harness/README.md` §커밋 안전 훅 이 정한 범위 선언 자리).
  `.harness/` 쪽은 이 계약 · 개정 파일 · QA 피드백 · `.harness/.meta/kaizen-0924/phase14-notes.md` · `.harness/.meta/kaizen-0924/phase14-review.md` 를 쓴다 —
  슬러그를 나열하지 않고 AR-01 셋째 값 `verify_seal` 로 잰다. AR-01 다섯째 값이 이 블록과 측정 공통 정의의 `FILES` 가 같은지 잰다

```text
# sprint-scope
onboarding-kit/skills/setup-guide/SKILL.md
onboarding-kit/skills/setup-guide/references/format-checklist.md
onboarding-kit/skills/setup-guide/references/project-detection.md
onboarding-kit/skills/setup-guide/evals/evals.json
onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh
onboarding-kit/skills/setup-guide/evals/fixtures/gate-fail-ledger-marker-swift.md
onboarding-kit/README.md
.harness/
```

- **이 Phase 의 커밋 메시지에는 전부 `Co-Authored-By` 줄 바로 위에 서명 줄 `Kaizen-Phase: kaizen-0924-p14-onboarding-kit` 한 줄을 넣는다** (봉인 커밋 포함).
  AR-01 · ER-03 · SC-00 · DG-01 · DG-03 · DG-06 이 이 줄로 이 Phase 커밋을 가린다(`harness/references/contract-schema.md` §여러 주체가 한 가지에 커밋할 때 선택지 B).
  서명을 빠뜨린 커밋은 서명 줄 목록에 안 보이므로 AR-01 첫째 값과 ER-03 마지막 값은 경로로 직접 센다.
  FIX 가 커밋을 더할 때도 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다(옛 줄은 지우지 않는다). notes 커밋도 이 Phase 커밋이다 — notes 를 커밋한 뒤 그 sha 로
  `end_sha:` 줄을 하나 더 덧붙여 커밋한다
- 구현 커밋은 `chmod +x onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh` 뒤 `git add -- <일곱> && git commit -o -- <일곱>` 한 번이다. 일곱이 전부
  onboarding-kit 이라 `validate-post-kaizen.py` scope-isolation 에 걸리지 않는다(예행에서 한 커밋으로 확인). 러너는 실행 비트가 있어야 한다(AR-02 셋째 칸 `100755`)
- 측정이 기대는 제목 · 줄 머리는 이름을 바꾸지 않는다: `### 출처 원장 (Source Ledger)` · `### Guide Conformance Gate (E3)` · `- **게이트를 우회하거나` · `### Gotcha 8: ` ·
  `## Process` · `### Phase 1: 스택 + 외부 서비스 탐지` · `### Phase 4: 검증 + 완료 안내` (SKILL.md) · `### 2. 사전 요구사항` (format-checklist) · `## 카이젠` (README) ·
  대조가 깨뜨리는 `guide_gate` 의 네 자리(`|지원 ?종료|폐지|중단|서비스 종료|단종/` · `if [ -z "$stack" ]; then` · `bare=$(grep -oF '[미검증]'` · `  g=${1}; stack=${2:-}`)와
  `guide_gate() {` 줄 · 픽스처 `gate-ok-flutter.md` 의 `## Step 2: 프로젝트 연결` · 읽기만 하는 `harness/docs/guides/skill-design-guide.md` §3.7 조항 3 의 다섯 줄
- 공유 파일(`.claude-plugin/marketplace.json` · `onboarding-kit/.claude-plugin/plugin.json` 버전 · 루트 `README.md` · 루트 `CLAUDE.md` · `docs/` HTML · 처리 배정표 · 감사 로그 ·
  실패 횟수 파일 · `.github/workflows/ci.yml` · `.harness/stale-values.yaml`)과 다른 Phase · 레포 전용 파일(`harness/` · `scripts/` · `.claude/skills/` · `docs/onboarding-kit/`)은
  건드리지 않는다 — ER-03 마지막 값. 러닝북 Phase 표가 이 Phase 에 `onboarding-kit/` 만 줬으므로 배포 예제 MD(`docs/onboarding-kit/examples/`)도 넘긴다.
  onboarding-kit README 는 킷 전용 문서라 고친다 — AUTO 구간은 스킬 frontmatter 만 읽는데 그 줄이 그대로다(AP-04). 문서 사이트 재생성은 Final F2 몫이라 DG-06 에서 `docs-site-regen` 을 뺀다
- QA(`harness:qa-evaluator`)는 설치본이다 — 이 Phase 가 고치는 파일에 qa-evaluator 는 없다
- 사용자 승인(Step 5) 대체: 사용자가 「자동으로 끝까지 알아서 진행해 내 허락이 필요한건 코덱스로 리서치나 검토받고」라고 위임했다(세션
  `de8c7935-a5b6-4df5-9106-fafa73c288a0` 기록 queued_command `2026-09-24T04:04:16.964Z`). Codex 사용량 한도가 소진돼(오류 원문 「You've hit your usage limit … try
  again at 11:05 PM」, 2026-09-24) 독립 Claude 검토자(REVIEW 에이전트)가 대신한다. 이어 사용자가 「코덱스 대신에 그냥 너가 알아서 진행하라고」라고 명시했다(같은 세션
  기록 user `2026-09-24T11:54:58.940Z`). 검토 결과 파일: `.harness/.meta/kaizen-0924/phase14-review.md` — 1 회차 `VERDICT: CHANGES`(고칠 것 넷 DG-02 · DG-05 (b) · DG-05 (c) ·
  ER-03 (b), 권고 셋)는 DRAFT 가 고칠 것 넷과 권고 둘을 반영했다(남은 권고 하나는 1 회차가 그대로 둬도 된다고 한 ER-03 (d) 경로 넓히기다). 2 회차가 반영을 확인하고
  `VERDICT: APPROVE` 를 냈다 — 이 계약은 그 판정 뒤에 봉인했다(BUILD, 2026-09-25)
- 판정 한계: 가이드를 만드는 LLM 이 Gotcha 9 · Gotcha 8 을 실제로 따르는지는 결정론 측정이 없다 — 조건은 지시 문장이 정해진 절에 글자 그대로 있는지(SK-01 · SK-02 · SK-09)와
  그 행동을 요구하는 평가 사례가 있는지(SK-03 · SK-09)를 잰다. 평가 사례의 `prompt` · `assertions` 는 LLM 실행용이라 이번에 돌리지 않는다. CI 는 Final 이 줄을 넣은 뒤에야 돈다 —
  러너는 이 기계의 dash · `/bin/sh` · bash · zsh 로 돌려 봤고(DG-04), Ubuntu 는 돌려 보지 못했다. 그래서 넘김 줄에 zsh 설치 확인을 넣는다
- 판정 근거: SK-01 · SK-02 · SK-07 · SK-08 · SK-09 — 산출물이 문서 문장 자체라 정해진 절 · 줄에 정해진 문장이 있는지가 판정이다. `sect` 가 코드 펜스를 건너뛰고 절을 자르고,
  `runp` 가 표 머리 · 구분선 · 행이 붙어 있는지 본다. 시작 커밋 판에서 새 문장 0 을 봉인 전에 확인했고, 문장 하나만 지운 사본에서 그 값이 떨어졌다(`회귀 게이트` 절)
- 판정 근거: SK-03 · SK-04 · SK-09 넷째 줄 — `evals.json` 을 JSON 으로 읽어 값이 기대 목록과 같은지 본다
- 판정 근거: SK-05 · SK-06 · ER-04 · RE-01 · DG-04 — 러너 · `guide_gate` 를 실제로 돌린 출력이다. SK-06 은 SKILL.md 사본의 함수를 한 군데씩 깨뜨린 넷, ER-04 는 멈춰야 할 여섯 경우를
  측정 안에서 직접 돌린다 — 러너가 저장해 둔 함수를 쓰면 SK-06 대조가 안 떨어진다. 사본 편집이 안 걸리면 `NEG_EDIT_FAIL` 이 찍혀 기대값과 달라진다
- 판정 근거: ER-01 · ER-02 · AP-01 · AP-03 — 편집 전 판과 파일마다 비교한 더한 줄 계산이다. 새 파일 둘은 편집 전 판을 빈 파일로 본다. 각각 양성 대조가 붙어 있다
- 판정 근거: DG-02 — 마크다운 다섯 파일마다 규칙별 경고 수를 편집 전 판(새 파일은 빈 판)과 비교한 출력이다. 더한 줄만 보지 않는다 — MD022 · MD032 · MD024 는 더한 줄 옆의 손대지 않은 줄에 붙는다(러닝북 측정 구멍 목록)
- 판정 근거: ER-03 · AR-01 · SC-00 · DG-01 · DG-03 · DG-06 — 커밋 기록과 봉인 검증 함수를 실제로 돌린 출력이다. 예행 저장소 변형 넷이 양성 대조다
- 판정 근거: AR-02 · AR-03 · RE-02 · AP-04 · DG-05 — 가리키는 자리 · 편집 전과 같아야 하는 곳 · 저장소 검사 도구를 실제로 돌린 출력이다. DG-05 의 옛 값은 등록부 값을 일곱 파일에서 직접 센 수다 —
  `scripts/check-stale-values.py` 는 `SOURCE_DIRS` 에 onboarding-kit 이 없어 이 킷을 훑지 않고, `scripts/sync-docs.py --check-only` 는 이 README 의 표지(`<!-- AUTO:skills:start -->`)를 못 읽어
  늘 `동기화됨` 을 낸다(검토가 찾았고 봉인 전 실측 표 DG-05 칸에서 다시 쟀다). 각각 한 군데를 깬 사본이 대조다
- 커버리지 해소: SK-01 ~ SK-09 · ER-04 · AR-02 · AR-03 · RE-02 · AP-04 · DG-04 — 산문의 파일 이름은 측정 `m <조건 ID>` 가 공통 정의의 변수(`$SK` · `$FC` · `$PD` · `$EV` · `$RUN` · `$FX` · `$RD` · `$SDG`)로
  연다(파일과 변수의 대응은 `common.sh` 머리). 토큰은 `m.sh` 의 같은 ID 갈래에 글자 그대로 있다. 기존 픽스처 셋 · `search-strategy.md` · `extra-unregistered.md` 는 `m.sh` 의 `SK-04)` · `SK-06)` · `ER-04)` · `AR-03)` 갈래가
  경로를 적어 연다. `/insights` · `/kaizen` · `pubspec.yaml` · `lib/main.dart` · `.env` 계열 이름은 문장 토큰이나 JSON 값의 일부로 잰다. `0.3.0` · `0.3.2` 는 머리 설정 값이라 JSON 으로 읽는다. `mock.py` · `rehearse.sh` · `common.sh` · `m.sh` · `rule-delta.sh` 는 측정 도구 자체의 이름이다
- 커버리지 해소: ER-01 · ER-03 — `.harness/.meta/kaizen-0924/phase14-notes.md` · `.harness/.meta/evidence/phase14.md` 는 공통 정의의 `$NOTES` · `$EVID` 다. ER-03 의 넘김 경로
  (`.github/workflows/ci.yml` · `docs/onboarding-kit/examples/fcm-ios-setup-guide.md` · `docs/onboarding-kit/fcm-ios-example.html` · `.claude/skills/onboarding-kaizen/SKILL.md` · `plugin.json` ·
  `docs/onboarding-kit/setup-guide.html` · `docs/onboarding-kit/format-checklist.html` · `docs/onboarding-kit/project-detection.html` · `scripts/detect-docs-drift.py`)는
  `m.sh` `ER-03)` 갈래 `toks` 의 인자이고, 공유 경로는 `not_other` 의 인자다
- 커버리지 해소: AR-01 — `onboarding-kit` 은 `unsigned_on` 의 인자, `.harness/` 는 `scope` 블록 줄과 `verify_seal` 이 도는 폴더다. `harness/references/contract-schema.md` 는 셋째 값 권장 형태의 출처다
- 검출기는 공백 든 코드 조각 안의 인자를 읽지 못한다 — 위 해소 줄이 전부 그 경우다
- 편집 전부터 있던 경고(SKILL.md `:8` MD041 · `:160` MD032, project-detection 표의 MD060, README 표의 MD060, 기존 픽스처의 맨 URL MD034)는 같은 수로 남으면 된다.
  DG-02 는 파일마다 규칙별 경고 수를 편집 전 판과 비교한다. 새 픽스처는 빈 판과 비교하므로 경고가 하나라도 있으면 늘어난 것이다 —
  그래서 새 픽스처의 출처 줄은 `<…>` URL 로 쓴다. `guide_gate` 의 G1 은 줄 머리 `**출처:**` 만 보므로 판정이 같다
- notes 에 함께 적는다(조건으로는 재지 않는다): `GAP 분석` 절의 Phase 1 대조 표, 하지 않기로 한 셋과 이유, 오케스트레이터 Step 14 범위 줄의 `onboarding-kit/references/`
  (이 폴더는 없다 — 스킬 폴더 아래 `references/` 다), 근거 파일 §3 의 `docs/onboarding-kit/plan-2026-05-18.md` 옛 Stripe 호스트(역사 문서라 두었다),
  `## 다음 사이클 메모` 에 onboarding-kit · planning-kit README 의 AUTO 표지(`<!-- AUTO:skills:start -->` · `<!-- AUTO:skills:end -->`)를 `scripts/sync-docs.py` 의 `MARKER_RE` 가 못 읽는다는 한 줄
  (표지를 바꾸면 표가 스킬 설명 전문으로 바뀌어 이번에는 고치지 않는다)
- 기능 조건 18 · 전체 조건 줄 28
- 사용자가 할 일: 없음

## 회귀 게이트 — 측정 공통 정의와 봉인 전 실측

모든 조건의 측정은 아래 `common.sh` 와 `m.sh` 를 차례로 `.` 으로 읽은 **bash** 셸에서 돈다 — `common.sh` 는 bash 가 아니면 `NOT_BASH` 를 찍고 종료 코드 2 로 끝난다
(zsh 는 따옴표 없는 변수를 쪼개지 않고 배열 첨자가 1 부터다). `m` 은 도우미 함수와 두 판 폴더가 없으면 `HELPER_MISSING` · `SNAPSHOT_MISSING` 을 내고 멈춘다 —
그래서 조건마다 `type m` 하나로 정의 확인을 대신한다. 두 판 풀기가 끊기거나 일곱 파일 가운데 하나라도 끝 판에서 비면(편집 전 판은 새 파일 둘을 뺀 다섯) `common.sh` 가
`SNAPSHOT_FAIL` 을 내고 종료 코드 2 로 끝난다. 셸이 끝나면 두 판 폴더를 지운다. `END_UNRESOLVED` 가 찍히면 셸이 종료 코드 2 로 끝난다.
`m` 의 종료 코드는 판정하지 않는다 — 판정은 출력 값으로 한다. 갈래 마지막 명령이 `grep -c` 이고 그 값이 0 이면 종료 코드가 1 이라, 0 을 기대하는 조건은 PASS 값에서 1 을 낸다
(예행 판에서 ER-01 · ER-03 이 PASS 값을 내고 종료 코드 1 로 끝났다). `m` 이 스스로 멈출 때(`HELPER_MISSING` · `SNAPSHOT_MISSING` · `UNKNOWN` · DG-05 사본 저장소를 못 만들 때)만 2 다.
러너 대조(SK-06 · ER-04)는 끝 판 `onboarding-kit/` 을 임시 폴더에 복사한 사본에서만 돈다 — 작업 폴더와 두 판 폴더는 바뀌지 않는다.
세 블록을 각 블록 첫 `#` 주석 줄(셔뱅 다음)의 이름 그대로 한 폴더에 저장하고 그 폴더를 `K` 에 넣는다. `rule-delta.sh` 옆에는 `node_modules` 를
`/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p1build/node_modules` 로 잇고
`cfg.markdownlint-cli2.jsonc` = `{ "config": { "MD013": false } }` 를 둔다 — 준비 단계 실측(2026-09-25): 그 자리의 `.bin/markdownlint-cli2 --version` 첫 줄이
`markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)`. 없으면 그 폴더에서 `npm install --no-save markdownlint-cli2@0.23.2` 부터 돌린다.
그 밖의 준비 단계 실측(2026-09-25): `command -v bash` → `/opt/homebrew/bin/bash` (5.3.9) · `/bin/bash --version` 3.2.57 · `command -v dash` → `/bin/dash` · `zsh --version` 5.9 ·
`shellcheck --version` 0.11.0 · `python3` · `shasum` 있음. ER-04 (e4) 가 만드는 PATH(`$T/nozsh`, 심볼릭 링크 열둘)에서 `command -v zsh` 가 실패하는 것도 측정이 함께 찍는다(`zsh_visible=0`).
`common.sh` 의 `R` 은 예행 저장소를 가리킬 때만 쓴다 — 비우면 작업 폴더다. 두 판을 `${TMPDIR:-/tmp}/p14m.XXXXXX` 에 푸니 `TMPDIR` 를 스크래치 폴더로 두고 읽는다.
예행 도구(스크래치 `p14d2/` — 검토 반영 판. 첫 판은 `p14d/`): `mock.py`(sha256 앞 16 자리 `48edf971dd8f8213` — 시작 커밋 판에 이 계약이 요구하는 편집을 적용한다. 새 파일 둘은 `p14d2/new/` 에서 복사) ·
`rehearse.sh`(시작 커밋에서 예행 저장소를 만들어 봉인 · 다른 Phase 커밋 · 구현 한 커밋 · `end_sha` · notes · `end_sha` 를 흉내 낸다. 변형 `base` · `unsigned-mine` · `unsigned-shared` ·
`signed-outside` · `cross-phase`) · `runall.sh` · `del.sh`(문장 삭제 대조) · `ctl.sh`(양성 · 음성 대조).

```bash
# common.sh — 측정 공통 정의. bash 로 읽는다 (zsh 는 배열 첨자가 1 부터이고 따옴표 없는 변수를 쪼개지 않는다)
[ -n "${BASH_VERSION:-}" ] || { echo "NOT_BASH — bash -c 안에서 다시 읽는다"; exit 2; }
export LC_ALL=C.UTF-8   # 번역투 정규식이 글자 단위로 돌아야 한다
cd "${R:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/kaizen-0924}" || exit 2
B=da9fbae94c13a9a1fc657f29ce9fc380ba9d506b                  # 이 Phase 시작 HEAD
SIG='Kaizen-Phase: kaizen-0924-p14-onboarding-kit'
CF=.harness/sprint-contract-kaizen-0924-p14-onboarding-kit.md
AM=.harness/sprint-amendments-kaizen-0924-p14-onboarding-kit.md
NOTES=.harness/.meta/kaizen-0924/phase14-notes.md
EVID=.harness/.meta/evidence/phase14.md
END=$( [ -f "$AM" ] && sed -n 's/^end_sha:[[:space:]]*//p' "$AM" | tail -1 )
if [ -z "$END" ] || ! git rev-parse -q --verify "$END^{commit}" >/dev/null; then
  echo "END_UNRESOLVED — 측정을 멈춘다. HEAD 로 바꿔 재지 않는다"; exit 2
fi
: "${K:?도우미 폴더를 K 에 넣는다}"
SK=onboarding-kit/skills/setup-guide/SKILL.md
FC=onboarding-kit/skills/setup-guide/references/format-checklist.md
PD=onboarding-kit/skills/setup-guide/references/project-detection.md
EV=onboarding-kit/skills/setup-guide/evals/evals.json
RUN=onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh
FX=onboarding-kit/skills/setup-guide/evals/fixtures/gate-fail-ledger-marker-swift.md
RD=onboarding-kit/README.md
FILES=("$SK" "$FC" "$PD" "$EV" "$RUN" "$FX" "$RD")
NEWF=("$RUN" "$FX")                     # 시작 커밋에 없는 파일 — 편집 전 판은 빈 파일로 본다
MDF=("$SK" "$FC" "$PD" "$RD" "$FX")     # 마크다운 검사 대상
SDG=harness/docs/guides/skill-design-guide.md
T=$(mktemp -d "${TMPDIR:-/tmp}/p14m.XXXXXX") || exit 2; mkdir -p "$T/B" "$T/E"
trap 'rm -rf "$T"' EXIT
# 두 판을 풀어 둔 폴더에서 잰다 — 작업 폴더에 남은 다른 Phase 의 미커밋 변경이 끼지 않는다
# 풀기가 도중에 끊기면 0 을 기대하는 값이 통과로 읽힌다 — 여기서 멈춘다
git archive "$B" | tar -x -C "$T/B" && git archive "$END" | tar -x -C "$T/E" || { echo "SNAPSHOT_FAIL — 측정을 멈춘다"; exit 2; }
for f in "${FILES[@]}"; do [ -s "$T/E/$f" ] || { echo "SNAPSHOT_FAIL $f"; exit 2; }; done
for f in "$SK" "$FC" "$PD" "$EV" "$RD"; do [ -s "$T/B/$f" ] || { echo "SNAPSHOT_FAIL base $f"; exit 2; }; done
# 편집 전 판 경로 — 새 파일은 /dev/null
bpath() { if [ -e "$T/B/$1" ]; then printf '%s' "$T/B/$1"; else printf '/dev/null'; fi; }
# sect <파일> <제목 앞부분> — 그 제목부터 같은 깊이 이하의 다음 제목 전까지. 코드 펜스 안의 `#` 줄은 제목으로 보지 않는다
sect() { awk -v h="$2" '
  /^[[:space:]]*(```|~~~)/ { fence = !fence }
  !f && !fence && index($0, h) == 1 { f = 1; lvl = match($0, /[^#]/) - 1; print; next }
  f && !fence && /^#+ / { l = match($0, /[^#]/) - 1; if (l <= lvl) exit }
  f' "$1"; }
# gline <파일> <줄 앞부분> — 그 앞부분으로 시작하는 줄
gline() { awk -v p="$2" 'index($0, p) == 1' "$1"; }
# toks <글> <토큰…> — 토큰마다 글 안에서 그 토큰이 든 줄 수
toks() { local s="$1"; shift; for t in "$@"; do printf '%s ' "$(printf '%s\n' "$s" | grep -cF -- "$t")"; done; echo; }
# runp <글> <앞부분…> — 이어진 줄들이 차례로 그 앞부분으로 시작하는 자리 수 (표 머리 · 구분선 · 행이 붙어 있는지)
runp() { local s="$1"; shift; printf '%s\n' "$s" | awk -v n="$#" -v a="$(printf '%s\037' "$@")" '
  BEGIN { split(a, p, "\037") } { l[NR] = $0 }
  END { c = 0; for (i = 1; i + n - 1 <= NR; i++) { ok = 1; for (j = 1; j <= n; j++) if (index(l[i + j - 1], p[j]) != 1) { ok = 0; break }; if (ok) c++ }; print c }'; }
# fmb <파일> — 첫 frontmatter 블록 본문
fmb() { awk 'NR==1&&/^---/{fm=1;next} fm&&/^---/{exit} fm' "$1"; }
# gblock <파일> — guide_gate 함수를 담은 bash 코드 블록 전체 (여는 펜스부터 닫는 펜스까지)
gblock() { awk '/^```bash$/{b=1; buf=""} b{buf=buf $0 "\n"} b&&/^```$/{b=0; if (buf ~ /\nguide_gate\(\) \{/) printf "%s", buf}' "$1"; }
# barefence <파일> — 언어 힌트 없는 여는 펜스 수 (여닫기를 번갈아 센다)
barefence() { awk '/^[[:space:]]*```/{ if (!o) { o = 1; if ($0 ~ /^[[:space:]]*```[[:space:]]*$/) n++ } else o = 0 } END{print n+0}' "$1"; }
url()   { grep -oE 'https?://[^ )>"`]+' | sed -E 's/[.,;:]+$//' | sort -u; }
added() { for f in "${FILES[@]}"; do git diff --no-index -U0 "$(bpath "$f")" "$T/E/$f"; done | grep '^+' | grep -v '^+++'; }
mine() { git log --format= --name-only "${1}..${2}" --grep="^${3}\$" | grep . | LC_ALL=C sort -u; }
unsigned_on() { _b=${1}; _u=${2}; _s=${3}; shift 3
  git log --format=%H "${_b}..${_u}" -- "$@" | while read -r _c; do git log -1 --format=%B "$_c" | grep -qxF "$_s" || echo "$_c"; done; }
# not_other <base> <상한> <서명> <경로…> — 경로를 건드린 구간 안 커밋 가운데 다른 Phase 서명이 없는 커밋 (0 줄이어야 한다)
not_other() { _b=${1}; _u=${2}; _s=${3}; shift 3
  git log --format=%H "${_b}..${_u}" -- "$@" | while read -r _c; do
    _m=$(git log -1 --format=%B "$_c")
    if printf '%s\n' "$_m" | grep -qE '^Kaizen-Phase: ' && ! printf '%s\n' "$_m" | grep -qxF "$_s"; then continue; fi
    echo "$_c"; done; }
my() { mine "$B" "$END" "$SIG"; }
# scope <계약> — `## 범위 경계` 절 안, 첫 줄이 `# sprint-scope` 인 text 블록의 경로 줄
scope() { awk '/^## /{s=$0} s ~ /^## 범위 경계/ && /^```text$/{b=1; n=0; next} b && /^```$/{b=0; next} b{n++; if (n==1 && $0 != "# sprint-scope") b=0; else if (n>1) print}' "$1"; }
fm_get() { awk -v k="^$2:[[:space:]]*" 'NR==1 && /^---[[:space:]]*$/ { fm=1; next } fm && /^---[[:space:]]*$/ { exit } fm && $0 ~ k { sub(k, "", $0); print; exit }' "$1" | sed -e "s/[[:space:]]*$//" -e "s/^['\"]//" -e "s/['\"]\$//"; }
sha256_16() { if command -v sha256sum >/dev/null 2>&1; then sha256sum; elif command -v shasum >/dev/null 2>&1; then shasum -a 256; else python3 -c 'import hashlib,sys; print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())'; fi | cut -c1-16; }
contract_digest() { grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$1" | sed -E 's/^- \[[ x]\]/- [ ]/' | sha256_16; }
verify_seal() { rec=$(fm_get "$1" conditions_digest); rec=${rec#sha256:}; if [ -z "$rec" ]; then echo "SEAL_ABSENT $1"; return 0; fi
  act=$(contract_digest "$1"); if [ "$rec" = "$act" ]; then echo "SEAL_OK $1"; else echo "SEAL_BROKEN $1 recorded=$rec actual=$act"; fi; }
# kit <이름> — 끝 판 onboarding-kit 을 $T/<이름> 에 복사하고 그 경로를 낸다 (러너 대조는 사본에서만 돈다)
kit() { rm -rf "$T/$1"; mkdir -p "$T/$1"; cp -R "$T/E/onboarding-kit" "$T/$1/" && printf '%s' "$T/$1/onboarding-kit"; }
# sub <파일> <옛 글> <새 글> — 한 번만 나오는 글을 바꾼다. 없거나 여럿이면 NEG_EDIT_FAIL (변이가 안 걸린 채 "통과" 로 읽히지 않게)
sub() { python3 - "$1" "$2" "$3" <<'PY' || { echo "NEG_EDIT_FAIL $1"; return 1; }
import sys
p, o, n = sys.argv[1:4]
s = open(p, encoding="utf-8").read()
if s.count(o) != 1: sys.exit(1)
open(p, "w", encoding="utf-8").write(s.replace(o, n))
PY
}
# runk <킷 사본> — 러너를 돌려 `종료코드 | FAIL 줄의 id(정렬) | shell_mismatch · fixture_missing 줄 수 | 요약 줄 | 마지막 줄 첫 낱말` 한 줄로 낸다
runk() { local o rc; o=$( /bin/sh "$1/skills/setup-guide/evals/run-gate-evals.sh" 2>&1 ); rc=$?
  printf 'rc=%s | %s | sm=%s fm=%s | %s | %s\n' "$rc" "$(printf '%s\n' "$o" | awk '/^FAIL  /{print $2}' | sort | paste -sd, -)" \
    "$(printf '%s\n' "$o" | grep -c 'shell_mismatch')" "$(printf '%s\n' "$o" | grep -c 'fixture_missing')" \
    "$(printf '%s\n' "$o" | grep -E '^EVALS declared=' )" "$(printf '%s\n' "$o" | tail -1 | cut -d' ' -f1)"; }
K02='(을|를) ?(처리|관리)(합니다|한다)|에 대해서?|하도록 (합니다|한다)|에 의(해|하여)|되어 있(는 경우|을 때)|(표시|적용|호출|생성|반환)(됩니다|된다)'
NAMES='fit-?pal|fit_pal|flutter[-_]playwright|playwright-mcp|chrome-devtools-mcp'
```

```bash
# m.sh — 조건마다 재는 값을 한 줄씩 낸다. common.sh 를 읽은 bash 에서 `m <조건 ID>` 로 부른다
m() {
  local E=$T/E S f fn o rc KC
  # 도우미가 하나라도 없으면 grep -c 가 조용히 0 을 낸다 — 멈춘다
  for fn in bpath sect gline toks runp fmb gblock barefence url added mine unsigned_on not_other my scope fm_get verify_seal kit sub runk; do
    type "$fn" >/dev/null 2>&1 || { echo "HELPER_MISSING $fn"; return 2; }; done
  [ -n "${T:-}" ] && [ -d "$T/B" ] && [ -d "$E" ] || { echo "SNAPSHOT_MISSING"; return 2; }
  case "$1" in
  SK-01)  # format-checklist §2 — 막는 요구 세 칸 규칙 · 칸 표 · FCM iOS 예 표
    S=$(sect "$E/$FC" '### 2. 사전 요구사항')
    toks "$S" '**막는 요구는 세 칸으로 쓴다** (SKILL.md Gotcha 9).' \
      '계정 등급 · 기기 · 권한 · 출시 상태처럼 없으면 어떤 작업이 멈추는 요구마다 아래 세 칸을 채운다.' \
      '「이게 없으면 진행할 수 없다」 한 줄로 끝내지 않는다 — 실제로 막히는 범위는 대개 셋업 전체가 아니라 그중 한 작업이다.' \
      '| 출처 | 그 요구를 적은 1차 출처 URL 과 조회일. 출처가 요구하지 않으면 막는 요구로 쓰지 않는다 |' \
      '| 막히는 것 | 없으면 멈추는 Step · 작업. 안 막히는 작업도 함께 적는다 |' \
      '| 우회 | 출처가 제시하는 우회 하나. 출처에 없으면 `우회 없음(출처 확인)` 으로 적고 우회를 지어내지 않는다 |' \
      '예 — FCM iOS (조회 2026-09-24):' \
      '| 실기기 | [Firebase Apple 셋업](https://firebase.google.com/docs/ios/setup) — Cloud Messaging 을 쓰면 실제 Apple 기기를 준비하라고 한다 |' \
      '| APNs · FCM 원격 메시지 수신 확인. 프로젝트 생성 · Firebase 구성 · 일반 앱 실행은 안 막힌다 |' \
      '`우회 없음(출처 확인)` — 시뮬레이터를 FCM 수신 우회로 쓰라는 문장은 이 출처에 없다 |' \
      '| 유료 개발자 계정 | [Apple 지원 기능 표](https://developer.apple.com/help/account/reference/supported-capabilities-ios) — Push notifications 가 무료 계정 열에 없다' \
      '[멤버십 개요](https://developer.apple.com/help/account/membership/programs-overview) — 일반 개발과 개인 기기 시험은 멤버십 없이 된다 |' \
      '| Push Notifications 기능 · APNs 키 구성 |' \
      '비영리 단체 · 공인 교육기관 · 정부 기관은 [가입 비용 면제](https://developer.apple.com/programs/enroll/) 경로가 있다. 그 밖의 우회는 확인하지 못했다 |' \
      '| 앱 출시 | 막는 요구가 아니다 — [Push Notification Console](https://developer.apple.com/documentation/usernotifications/testing-notifications-using-the-push-notification-console) 이 개발 환경에서 기기 토큰으로 시험 발송을 지원한다 | 없음 | 해당 없음 |' \
      '- 필요한 계정/권한 (예: Apple Developer Program 가입) — 막는 요구면 아래 세 칸으로 쓴다'
    echo "runs=$(runp "$S" '| 칸 | 쓰는 것 |' '| --- | --- |' '| 출처 |' '| 막히는 것 |' '| 우회 |') $(runp "$S" '| 요구 | 출처 | 막히는 것 | 우회 |' '| --- | --- | --- | --- |' '| 실기기 |' '| 유료 개발자 계정 |' '| 앱 출시 |') whole=$(grep -cF '**막는 요구는 세 칸으로 쓴다**' "$E/$FC")" ;;
  SK-02)  # SKILL.md Gotcha 9 · 자리 · Phase 4 확인 목록
    S=$(sect "$E/$SK" '### Gotcha 9: ')
    toks "$S" '### Gotcha 9: 막는 요구는 출처 · 막히는 것 · 우회 세 칸으로 — 셋업 전체가 막힌 것처럼 쓰지 마라' \
      '사전 요구사항에 「실기기가 필요하다」 · 「유료 계정이 필요하다」 · 「앱을 먼저 출시해야 한다」 를 한 줄로 쓰면 사용자는 셋업 전체가 막혔다고 읽는다.' \
      '요구마다 출처 · 막히는 것 · 우회 세 칸을 채운다 (`references/format-checklist.md` §2 — FCM iOS 예 포함).' \
      '- 출처가 요구하지 않는 것을 막는 요구로 쓰지 않는다. 예: FCM 시험 발송에 앱 출시는 필요 없다 — 개발 환경에서 시험 발송이 된다' \
      '- 출처에 없는 우회를 지어내지 않는다. 확인한 우회가 없으면 `우회 없음(출처 확인)` 으로 적는다' \
      '§3.7 조항 3 의 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 적는다' \
      '같은 모양의 실측(`/insights` 2026-09-24 F10)' '「앱 올리면 되잖아?」'
    awk '/^### Gotcha 8: /{a=NR} /^### Gotcha 9: /{b=NR} /^## Process$/{c=NR} END{print (a&&b&&c&&a<b&&b<c)?1:0}' "$E/$SK"
    S=$(sect "$E/$SK" '### Phase 4: 검증 + 완료 안내')
    printf '%s\n' "$S" | grep -oE '^[0-9]+\. ' | tr -dc '0-9\n' | paste -sd' ' -
    toks "$S" '5. **막는 요구 세 칸 확인** — 사전 요구사항의 막는 요구마다 출처 · 막히는 것 · 우회가 있는지 본다 (Gotcha 9). 출처가 요구하지 않는 요구는 지운다' \
      '6. **마커 집계 보고** — ' '7. 사용자에게 파일 경로 + ' ;;
  SK-03)  # evals.json 막는 요구 사례 · 손대지 않은 다섯 사례
    python3 - "$T/B/$EV" "$E/$EV" <<'PY'
import json, sys
b = json.load(open(sys.argv[1], encoding="utf-8")); e = json.load(open(sys.argv[2], encoding="utf-8"))
print(" ".join(c["id"] for c in e["cases"]))
c = [x for x in e["cases"] if x["id"] == "blocking-requirement-scope"]
A = ["every_blocking_requirement_has_fields(['출처', '막히는 것', '우회']) == true",
     "every_blocking_requirement_source_has_url_and_fetch_date == true",
     "guide_does_not_list_as_blocking('앱 출시') — 출처가 요구하지 않는다",
     "guide_does_not_claim_simulator_receives_fcm_remote_message() — 출처에 없는 우회를 쓰지 않는다",
     "if source_gives_no_workaround then guide_includes('우회 없음(출처 확인)') == true",
     "does_not_declare_whole_setup_impossible == true — 막히는 범위를 그 작업으로 좁힌다"]
U = ["https://firebase.google.com/docs/ios/setup", "https://developer.apple.com/help/account/reference/supported-capabilities-ios",
     "https://developer.apple.com/documentation/usernotifications/testing-notifications-using-the-push-notification-console"]
if c:
    c = c[0]
    print("n=1 prompt=%d assertions=%d source=%d stack_setup=%d" % (
        c["prompt"] == "FCM iOS 설정해줘. 유료 개발자 계정도 실기기도 아직 없고 앱도 출시 전이야", c["assertions"] == A,
        sum(u in c["source"] for u in U), "pubspec.yaml" in c["setup"]["project_files"]))
else:
    print("n=0")
bm = {x["id"]: x for x in b["cases"]}
print("same=%d" % sum(1 for x in e["cases"] if x["id"] in bm and x["id"] != "no-invented-paths" and x == bm[x["id"]]))
PY
    ;;
  SK-04)  # evals.json 러너 · gate_cases 여섯 · 폴더의 픽스처가 전부 등록
    python3 - "$E/$EV" "$E/onboarding-kit/skills/setup-guide/evals/fixtures" <<'PY'
import json, os, sys
e = json.load(open(sys.argv[1], encoding="utf-8"))
A = ["G1_LEDGER PASS steps=2 ledger=2", "G2_MARKER PASS bare=0 invalid=0 env=0"]; P4 = "G4_DEPRECATION PASS unsourced_boxes=0"
X = [("ok-flutter", "fixtures/gate-ok-flutter.md", "flutter", A + ["G3_STACKMIX PASS stack=flutter swift_fence=0", P4, "GATE_PASS"]),
     ("stack-unset", "fixtures/gate-ok-flutter.md", None, A + ["G3_STACKMIX FAIL stack=unset swift_fence=0", P4, "GATE_FAIL"]),
     ("stack-empty", "fixtures/gate-ok-flutter.md", "", A + ["G3_STACKMIX FAIL stack=unset swift_fence=0", P4, "GATE_FAIL"]),
     ("g4-ko-sourced", "fixtures/gate-g4-ko-sourced.md", "flutter", ["G1_LEDGER PASS steps=1 ledger=1", A[1], "G3_STACKMIX PASS stack=flutter swift_fence=0", P4, "GATE_PASS"]),
     ("g4-ko-unsourced", "fixtures/gate-g4-ko-unsourced.md", "flutter", ["G1_LEDGER PASS steps=1 ledger=1", A[1], "G3_STACKMIX PASS stack=flutter swift_fence=0", "G4_DEPRECATION FAIL unsourced_boxes=1", "GATE_FAIL"]),
     ("ledger-marker-swift", "fixtures/gate-fail-ledger-marker-swift.md", "flutter", ["G1_LEDGER FAIL steps=2 ledger=1", "G2_MARKER FAIL bare=1 invalid=2 env=1", "G3_STACKMIX FAIL swift_fence=1", P4, "GATE_FAIL"])]
g = e.get("gate_cases") or []
got = [(c.get("id"), c.get("fixture"), c.get("stack", "MISSING"), c.get("expect")) for c in g]
print("version=%s runner=%d" % (e.get("version"), e.get("runner") == "sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh"))
print("gate_cases=%d same=%d note=%d" % (len(g), got == X, sum(1 for c in g if c.get("note"))))
folder = sorted(n for n in os.listdir(sys.argv[2]) if n.endswith(".md")) if os.path.isdir(sys.argv[2]) else []
ref = sorted({os.path.basename(c.get("fixture", "")) for c in g})
print("folder=%d referenced=%d equal=%d" % (len(folder), len(ref), folder == ref))
PY
    ;;
  SK-05)  # 새 픽스처 — 손으로 센 답과 두 셸 출력
    awk '/^guide_gate\(\) \{/{p=1} p{print} p&&/^\}$/{exit}' "$E/$SK" > "$T/gate.sh"
    printf '%s\n' 'G1_LEDGER FAIL steps=2 ledger=1' 'G2_MARKER FAIL bare=1 invalid=2 env=1' 'G3_STACKMIX FAIL swift_fence=1' \
      'G4_DEPRECATION PASS unsourced_boxes=0' 'GATE_FAIL' > "$T/ka.txt"
    for f in bash zsh; do "$f" -c ". '$T/gate.sh'; guide_gate '$E/$FX' flutter" > "$T/ka.$f" 2>&1; done
    echo "bash=$(cmp -s "$T/ka.bash" "$T/ka.txt" && echo 1 || echo 0) zsh=$(cmp -s "$T/ka.zsh" "$T/ka.txt" && echo 1 || echo 0) lines=$(grep -c . "$T/ka.bash")" ;;
  SK-06)  # 러너 — 끝 판 통과와 대조 넷 (SKILL.md 사본의 guide_gate 를 한 군데씩 깨뜨린다)
    KC=$(kit k0); o=$(/bin/sh "$KC/skills/setup-guide/evals/run-gate-evals.sh" 2>&1); rc=$?
    echo "rc=$rc pass=$(printf '%s\n' "$o" | grep -c '^PASS  ') $(for f in gate-ok-flutter gate-g4-ko-sourced gate-g4-ko-unsourced gate-fail-ledger-marker-swift; do printf '%s ' "$(printf '%s\n' "$o" | grep '^PASS  ' | grep -cF "(fixtures/$f.md, ")"; done)| $(printf '%s\n' "$o" | tail -2 | paste -sd' ' -)"
    KC=$(kit n1); sub "$KC/skills/setup-guide/SKILL.md" '|지원 ?종료|폐지|중단|서비스 종료|단종/' '/' && runk "$KC"
    KC=$(kit n2); sub "$KC/skills/setup-guide/SKILL.md" 'if [ -z "$stack" ]; then' 'if [ -z "$stack" ] && false; then' && runk "$KC"
    KC=$(kit n3); sub "$KC/skills/setup-guide/SKILL.md" "bare=\$(grep -oF '[미검증]'" "bare=\$(grep -oF '[미검증X]'" && runk "$KC"
    KC=$(kit n4); sub "$KC/skills/setup-guide/SKILL.md" '  g=${1}; stack=${2:-}' '  g=${1}; stack=${2:-}; v="a b"; set -- $v; echo "ARGS $#"' && runk "$KC" ;;
  SK-07)  # 러너 안내 — SKILL.md 게이트 절 · README
    S=$(sect "$E/$SK" '### Guide Conformance Gate (E3)')
    toks "$S" '- **게이트 함수를 고쳤으면 `sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh` 가 `EVALS_PASS` 로 끝나야 한다.**' \
      '이 스크립트는 SKILL.md 에서 함수를 그대로 뽑아 `evals/evals.json` 의 `gate_cases` 입력마다 zsh · bash 두 셸의 출력을 기대 출력 전체와 대조한다.' \
      '판정이 바뀌는 수정이면 기대 출력도 같은 커밋에서 고친다.'
    printf '%s\n' "$S" | awk '/^- \*\*게이트를 우회하거나/{a=NR} /^- \*\*게이트 함수를 고쳤으면/{b=NR} END{print (a&&b&&b==a+1)?1:0}'
    toks "$(sect "$E/$RD" '## 카이젠')" '- 전체 카이젠: `/kaizen` (Phase 14로 자동 실행)' \
      '- `guide_gate` 시험: `sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh` — 등록된 입력마다 zsh · bash 두 셸 출력을 기대 출력과 대조한다.' \
      '폴더에만 있고 등록 안 된 픽스처도 실패로 센다' 'Phase 13으로' ;;
  SK-08)  # Phase 1 넘김 — 「사유 한 줄」 을 네 요건 · §3.7 네 칸으로
    S=$(sect "$E/$SK" '### 출처 원장 (Source Ledger)')
    echo "old=$(grep -cF '마커 + 사유 한 줄' "$E/$SK") $(toks "$S" 'fetch 가 끝까지 실패한 항목은 조용히 넘기지 말고 마커와 아래 네 요건을 붙인다.' \
      '네 요건은 `harness/docs/guides/skill-design-guide.md` §3.7 조항 3 의 네 칸과 같다 — ①③ 이 막는 것, ② 가 시도한 우회, ④ 가 통제 불가 사유와 재검증 명령이다.')" ;;
  SK-09)  # 값이 든 .env 를 열지 않는다 — Gotcha 8 · Process 1 단계 · project-detection · 평가 사례
    S=$(sect "$E/$SK" '### Gotcha 8: ')
    toks "$S" '**값이 든 `.env` 파일(`.env.local` · `.env.production` 등)은 열지 않는다.** 열면 비밀 값이 대화 기록에 남는다.' \
      '파일이 있는지는 1 번 탐색으로 보고, 키 이름은 `.env.example` 같은 예시 파일이나 그 키를 읽는 코드에서 얻는다.' \
      '둘 다 없으면 사용자에게 키 이름을 묻는다. 사용자가 그 값을 보여 달라고 직접 요청한 경우만 예외다.' \
      '실측(2026-05-28): 설정 방법을 묻는 질문에 `.env` 를 바로 열었다가 사용자에게 즉시 거부당했다.' \
      '- ❌ 프로젝트가 이미 다른 이름의 키를 쓰는데(`.env.example` · 코드에 있다) 확인 없이 관례적인 이름(`FIREBASE_SERVER_KEY` 등)으로 안내' \
      '- ❌ 기존 `.env` 에 다른 이름의 키가 있는데'
    toks "$(sect "$E/$SK" '### Phase 1: 스택 + 외부 서비스 탐지')" '설정 파일(`.env.example` 류, `docker-compose*.yml`, `terraform/`)' \
      '값이 든 `.env` 파일은 있는지만 보고 열지 않는다 (Gotcha 8).' '설정 파일(`.env*`,'
    toks "$(cat "$E/$PD")" '- `.env.example` 류 — 환경변수 키 이름에서 외부 서비스 흔적 (`FIREBASE_*`, `AWS_*`, `STRIPE_*`).' \
      '값이 든 `.env` 파일(`.env.local` · `.env.production` 등)은 있는지만 보고 열지 않는다 (SKILL.md Gotcha 8)' '- `.env*` — '
    python3 - "$E/$EV" <<'PY'
import json, sys
c = [x for x in json.load(open(sys.argv[1], encoding="utf-8"))["cases"] if x["id"] == "no-invented-paths"][0]
s = c["setup"]
print("files=%d example=%d assert=%d desc=%d" % (s.get("project_files") == [".env", ".env.example", "lib/main.dart"],
    s.get("env_example_contains") == ["FCM_CREDENTIALS_PATH="],
    c["assertions"][-1] == "does_not_read_file('.env') — 값이 든 파일은 열지 않는다. 키 이름은 .env.example 에서 얻는다 (Gotcha 8)",
    c["description"].endswith(". 값이 든 .env 는 열지 않고 키 이름은 .env.example 에서 얻는다 (Gotcha 8)")))
PY
    ;;
  ER-01)  # 새로 생긴 URL 이 근거 파일에 있다 — 파일마다 편집 전 판과 비교, notes 는 URL 전부
    for f in "${FILES[@]}"; do comm -13 <(url < "$(bpath "$f")") <(url < "$E/$f"); done | sort -u | comm -23 - <(url < "$E/$EVID") | grep -c .
    if [ -f "$E/$NOTES" ]; then url < "$E/$NOTES" | comm -23 - <(url < "$E/$EVID") | grep -c .; else echo NOTES_MISSING; fi ;;
  ER-02)  # 더한 줄의 번역투 6 종 · 앱 · 도구 서버 이름, 킷 전체의 앱 이름
    echo "added=$(added | grep -c .) k02=$(added | grep -cE "$K02") names=$(added | grep -ciE "$NAMES") kit_names=$(grep -rhiE "$NAMES" "$E/onboarding-kit" | grep -c .) generic=$(grep -cF '조직 식별자 없는 흔한 조합(`com.<앱이름>.app`)은 누가 선점했을 확률 높음.' "$E/$SK")" ;;
  ER-03)  # notes 문자열 · 넘김 · 미반영 사유 · 공유 파일과 다른 Phase 파일을 건드린 커밋
    git cat-file -e "$END:$NOTES" 2>/dev/null && echo notes_committed=1 || echo notes_committed=0
    toks "$(cat "$E/$NOTES" 2>/dev/null)" '`other-kits:P3`' '`other-kits:P9`' '## 바꾼 파일' '## 반영한 처리 배정표 키' '## 미반영 키와 사유' \
      '## 넘기는 것' '## changelog 한 단락' '## 킷 로그 한 단락' '## 다음 사이클 메모'
    # 넘김 · 미반영 사유는 그 절 안에서 센다 — 낱말은 다른 절에도 나와 넘김 줄을 빠뜨려도 1 이 된다
    toks "$(sect "$E/$NOTES" '## 넘기는 것' 2>/dev/null)" '.github/workflows/ci.yml' 'command -v zsh' 'sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh' \
      'docs/onboarding-kit/examples/fcm-ios-setup-guide.md' 'docs/onboarding-kit/fcm-ios-example.html' '.claude/skills/onboarding-kaizen/SKILL.md' 'plugin.json' \
      'docs/onboarding-kit/setup-guide.html' 'docs/onboarding-kit/format-checklist.html' 'docs/onboarding-kit/project-detection.html' 'scripts/detect-docs-drift.py'
    toks "$(sect "$E/$NOTES" '## 미반영 키와 사유' 2>/dev/null)" '2026-07-20' 'Workload Identity Federation' 'CocoaPods'
    not_other "$B" "$END" "$SIG" .claude-plugin/marketplace.json onboarding-kit/.claude-plugin/plugin.json README.md CLAUDE.md \
      .harness/.meta/orchestrator-audit-log.md .harness/.meta/kaizen-failure-count.yaml .claude/kaizen-input/insights-report.md \
      .github/workflows/ci.yml .harness/stale-values.yaml .claude/skills harness scripts docs/onboarding-kit docs/index.html | grep -c . ;;
  ER-04)  # 러너가 멈춰야 할 때 멈추고, 한 칸이 깨져도 나머지를 잰다 — 전부 끝 판 킷 사본에서
    KC=$(kit e1); cp "$KC/skills/setup-guide/evals/fixtures/gate-ok-flutter.md" "$KC/skills/setup-guide/evals/fixtures/extra-unregistered.md" && runk "$KC"
    KC=$(kit e2); rm "$KC/skills/setup-guide/evals/fixtures/gate-g4-ko-sourced.md" \
      && sub "$KC/skills/setup-guide/evals/fixtures/gate-ok-flutter.md" '## Step 2: 프로젝트 연결' $'```swift\nFirebaseApp.configure()\n```\n\n## Step 2: 프로젝트 연결' && runk "$KC"
    KC=$(kit e3); python3 -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p,encoding="utf-8")); d["gate_cases"]=[]; open(p,"w",encoding="utf-8").write(json.dumps(d,ensure_ascii=False))' "$KC/skills/setup-guide/evals/evals.json" && runk "$KC"
    KC=$(kit e4); mkdir -p "$T/nozsh"; for f in dirname mktemp awk head grep tail python3 sed cmp rm bash cat; do ln -sf "$(command -v "$f")" "$T/nozsh/$f"; done
    o=$(PATH=$T/nozsh /bin/sh "$KC/skills/setup-guide/evals/run-gate-evals.sh" 2>&1); rc=$?
    echo "rc=$rc zsh_visible=$(PATH=$T/nozsh /bin/sh -c 'command -v zsh >/dev/null && echo 1 || echo 0') | $(printf '%s\n' "$o" | tail -1)"
    KC=$(kit e5); sub "$KC/skills/setup-guide/SKILL.md" 'guide_gate() {' 'guide_gate_v2() {' && runk "$KC"
    KC=$(kit e6); python3 -c 'import sys; p=sys.argv[1]; s=open(p,encoding="utf-8").read(); open(p,"w",encoding="utf-8").write(s[:120])' "$KC/skills/setup-guide/evals/evals.json" && runk "$KC" ;;
  AR-01)  # 허용 경로 · 서명 · 봉인 · 범위 선언 블록
    unsigned_on "$B" "$END" "$SIG" onboarding-kit | grep -c .
    echo "$(my | grep -v '^\.harness/' | grep -vxF -f <(printf '%s\n' "${FILES[@]}") | grep -c .) $(my | grep -cxF -f <(printf '%s\n' "${FILES[@]}"))"
    find .harness -type f -name 'sprint-contract*.md' -print0 | while IFS= read -r -d '' f; do verify_seal "$f"; done \
      | awk '$1=="SEAL_BROKEN"{print $2}' | sed 's#^\./##' | sort -u | comm -12 - <( { my; echo "$CF"; } | sort -u) | grep -c .
    verify_seal "$E/$CF" | cut -d' ' -f1
    diff <(scope "$E/$CF" | grep -vxF '.harness/' | sort) <(printf '%s\n' "${FILES[@]}" | sort) >/dev/null && echo "scope_same=1" || echo "scope_same=0"
    scope "$E/$CF" | grep -cxF '.harness/' ;;
  AR-02)  # 새 문장이 가리키는 자리가 실제로 있다
    echo "$(grep -cF '(SKILL.md Gotcha 9)' "$E/$FC") $(grep -c '^### Gotcha 9: ' "$E/$SK") | $(grep -cF '(`references/format-checklist.md` §2' "$E/$SK") $(grep -cx '### 2. 사전 요구사항' "$E/$FC") | $(for f in "$SK" "$RD" "$EV"; do printf '%s ' "$(grep -cF 'sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh' "$E/$f")"; done)$(git ls-tree "$END" -- "$RUN" | awk '{print $1}') | $(grep -cF '(SKILL.md Gotcha 8)' "$E/$PD") $(grep -c '^### Gotcha 8: ' "$E/$SK") | $(grep -cF '§3.7 조항 3 의 네 칸' "$E/$SK") $(grep -cF '3. **검증 불가 시 `[미검증]` 에 네 칸을 붙인다.**' "$E/$SDG") $(for t in '- **막는 것** —' '- **시도한 우회** —' '- **통제 불가 사유** —' '- **재검증 명령** —'; do printf '%s ' "$(grep -cF -- "$t" "$E/$SDG")"; done)" ;;
  AR-03)  # 손대지 않을 곳 — guide_gate 코드 블록 · 기존 픽스처 셋 · search-strategy
    diff <(gblock "$T/B/$SK") <(gblock "$E/$SK") >/dev/null && [ -n "$(gblock "$E/$SK")" ] && printf '1 | ' || printf '0 | '
    for f in gate-ok-flutter gate-g4-ko-sourced gate-g4-ko-unsourced; do f=onboarding-kit/skills/setup-guide/evals/fixtures/$f.md; cmp -s "$T/B/$f" "$E/$f" && printf '1 ' || printf '0 '; done
    f=onboarding-kit/skills/setup-guide/references/search-strategy.md; cmp -s "$T/B/$f" "$E/$f" && echo '| 1' || echo '| 0' ;;
  RE-01)  # 러너가 자기 위치 기준으로 돈다 — 레포 밖 폴더에서 불러도 같은 결과
    o=$(cd / && /bin/sh "$E/$RUN" 2>&1); echo "rc=$? $(printf '%s\n' "$o" | tail -2 | paste -sd' ' -)" ;;
  RE-02)  # guide_gate 사본이 없다 — 정의는 SKILL.md 하나, 러너는 뽑아 쓴다
    echo "$(grep -rlE '^guide_gate\(\) \{' "$E/onboarding-kit" | sed "s#^$E/##" | paste -sd' ' -) | $(grep -cF "awk '/^guide_gate\\(\\) \\{/{p=1} p{print} p&&/^\\}\$/{exit}' \"\$SKILL\"" "$E/$RUN") $(grep -cE 'G[1-4]_[A-Z]+ (PASS|FAIL)' "$E/$RUN")" ;;
  AP-01)  # 더한 줄에 이 킷 플러그인 버전 값
    f=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$E/onboarding-kit/.claude-plugin/plugin.json")
    echo "version=$f $(added | grep -cF -- "$f")" ;;
  AP-03)  # 언어 힌트 없는 여는 펜스 — 마크다운 다섯 파일 (V6 가 안 읽는 format-checklist · 픽스처 포함)
    for f in "${MDF[@]}"; do printf '%s ' "$(barefence "$E/$f")"; done; echo ;;
  AP-04)  # SKILL.md frontmatter 가 편집 전과 같고 name 줄이 하나
    echo "$(diff <(fmb "$T/B/$SK") <(fmb "$E/$SK") >/dev/null && echo 1 || echo 0) $(fmb "$E/$SK" | grep -cx 'name: setup-guide')" ;;
  DG-02)  # markdownlint — 파일마다 규칙별 경고 수를 편집 전 판과 비교 (새 파일은 빈 판). 더한 줄만 보면 옆 줄에 붙는 MD022 · MD032 · MD024 를 놓친다
    for f in "${MDF[@]}"; do L=$(printf '%s' "$f" | tr '/' '_'); cp "$E/$f" "$T/$L.md"
      if [ -e "$T/B/$f" ]; then cp "$T/B/$f" "$T/$L.0.md"; else : > "$T/$L.0.md"; fi
      printf '%s ' "$f"; bash "$K/rule-delta.sh" "$T/$L.0.md" "$T/$L.md"; done ;;
  DG-04)  # 러너를 네 해석기로 — 종료 코드 · stderr · 출력이 같은지, shellcheck · 문법 검사
    for f in dash /bin/sh bash zsh; do "$f" "$E/$RUN" > "$T/out.$(basename "$f")" 2> "$T/err.$(basename "$f")"; printf '%s rc=%s err=%s same=%s | ' "$f" "$?" "$(grep -c . "$T/err.$(basename "$f")")" "$(cmp -s "$T/out.dash" "$T/out.$(basename "$f")" && echo 1 || echo 0)"; done; echo
    o=$(shellcheck -s sh "$E/$RUN" 2>&1); echo "shellcheck rc=$? lines=$(printf '%s' "$o" | grep -c .) $(for f in dash sh bash zsh; do "$f" -n "$E/$RUN" 2>/dev/null; printf 'n_%s=%s ' "$f" "$?"; done)" ;;
  DG-05)  # 저장소 검사 — $END 판을 git 저장소로 만든 사본에서. 옛 값은 이 킷을 안 훑는 check-stale-values.py 대신 일곱 파일에서 직접 센다
    local G=$T/G; rm -rf "$G"; cp -R "$E" "$G"
    git -C "$G" init -q && git -C "$G" add -A && git -C "$G" -c user.name=m -c user.email=m@m commit -qm snap || return 2
    ( cd "$G" && python3 scripts/validate-plugin.py onboarding-kit > "$T/vp.txt" 2>&1; echo $? > "$T/vp.rc" )
    echo "$(grep -cE '^  V([1-9]|10) ' "$T/vp.txt") $(grep -E '^  V([1-9]|10) ' "$T/vp.txt" | grep -cvE -- '— (OK|SKIP \(no templates/\))$') rc=$(cat "$T/vp.rc")"
    python3 - "$E/.harness/stale-values.yaml" "${FILES[@]/#/$E/}" <<'PY'
import sys, yaml
vals = [v["old"] for v in yaml.safe_load(open(sys.argv[1], encoding="utf-8"))["values"]]
hits = sum(open(p, encoding="utf-8").read().count(o) for p in sys.argv[2:] for o in vals)
print("stale_old=%d files=%d hits=%d" % (len(vals), len(sys.argv[2:]), hits))
PY
    ;;
  DG-06)  # 사이클 검사 — 이 Phase 몫 줄만 본다. docs-site-regen 은 Final F2 몫
    python3 scripts/validate-post-kaizen.py --since "$B" --verbose > "$T/vpk.txt" 2>&1
    grep -E '\] . (scope-isolation|doc-contracts): ' "$T/vpk.txt" | awk '{print $5, $2}'
    python3 scripts/validate-doc-contracts.py -v 2>&1 | awk -F' → ' '/^ *검사: /{a=$1; sub(/^ *검사: /,"",a); sub(/:[0-9]+$/,"",a); print a; print $2}' | sort -u > "$T/dc.txt"
    echo "doc_checked=$(grep -c . "$T/dc.txt") doc_mine=$(comm -12 "$T/dc.txt" <(my) | grep -c .)"
    awk '/ scope-isolation: /{f=1;next} /^\[ /{f=0} f&&/^ +[0-9a-f]{7,40}$/{print $1}' "$T/vpk.txt" > "$T/viol.txt"
    echo "violators=$(grep -c . "$T/viol.txt") mine=$(while read -r c; do git log -1 --format=%B "$c" | grep -qxF "$SIG" && echo "$c"; done < "$T/viol.txt" | grep -c .)" ;;
  NA)  # N/A 줄 넷(SC-00 · DG-01 · DG-03 · RE-01 이 아닌 것) 의 사유 측정 — 서명 커밋이 건드린 경로
    echo "SC-00=$(my | grep -cE '^(scripts/release\.sh|\.claude-plugin/marketplace\.json|[^/]+/\.claude-plugin/plugin\.json)$') DG-01=$(my | grep -c '^scripts/release.sh$')" ;;
  *) echo "UNKNOWN $1"; return 2 ;;
  esac
}
```

```bash
#!/usr/bin/env bash
# rule-delta.sh <옛 파일> <새 파일> — 규칙별 경고 수를 두 판에서 세어 늘어난 규칙만 낸다
# 더한 줄만 보면 손대지 않은 옆 줄에 붙는 경고(MD022 · MD032 · MD024)를 놓친다 (러닝북 — Phase 7 · 8 · 9 · 11 실측)
# 린터가 안 돌면 0 이 조용히 나온다 — 돌았다는 줄(Linting: 1 file)이 없으면 멈춘다
set -u
DIR=$(cd "$(dirname "$0")" && pwd)
cnt() { local out
  out=$("$DIR/node_modules/.bin/markdownlint-cli2" --config "$DIR/cfg.markdownlint-cli2.jsonc" "$1" 2>&1)
  printf '%s\n' "$out" | grep -q '^Linting: 1 file' || return 2
  printf '%s\n' "$out" | sed -nE 's/^[^ ]*:[0-9]+(:[0-9]+)? (error|warning) (MD[0-9]+)\/.*/\3/p' | sort | uniq -c | awk '{print $2, $1}'; }
O=$(cnt "$1") || { echo "LINT_NOT_RUN $1"; exit 2; }
N=$(cnt "$2") || { echo "LINT_NOT_RUN $2"; exit 2; }
UP=$(join -a 2 -e 0 -o 0,1.2,2.2 <(printf '%s\n' "$O" | grep . | sort) <(printf '%s\n' "$N" | grep . | sort) | awk '$3 > $2 {printf "%s%s:%s>%s", (n++ ? " " : ""), $1, $2, $3}')
echo "rules_up=$(printf '%s' "$UP" | wc -w | tr -d ' ')${UP:+ $UP}"
```

### 봉인 전 실측 — 예행 판 · 시작 커밋 판

예행 판은 이 계약 초안을 봉인해 커밋하고 `mock.py` 를 적용한 구현 커밋 · 다른 Phase 커밋 · notes 모의본까지 올린 예행 저장소(변형 없음)다. 시작 커밋 판은 `end_sha` 를 시작 커밋으로 둔
예행 저장소다 — 새 파일 둘이 없어 `common.sh` 의 끝 판 비지 않음 검사를 다섯 파일로 줄인 사본(`p14d2/kb/`)으로 쟀다(파일이 없다는 오류 줄은 빼고 적었다).
예행 판 전체 출력은 bash 5.3.9 와 `/bin/bash` 3.2.57 에서 바이트 단위로 같았다(`out-none.txt` · `out-none-bash32.txt`).

| 조건 | 예행 판 (`m` 출력) | 시작 커밋 판 | 대조 |
| --- | --- | --- | --- |
| SK-01 | `1` 열여섯 · `runs=1 1 whole=1` | `0` 열여섯 · `runs=0 0 whole=0` | 토큰 삭제 27 가운데 27 이 바뀜 · 칸 표 행 뒤 빈 줄 → `runs=0 1` · 첫 목록 줄을 옛 줄로 → 첫 줄 끝 `0` |
| SK-02 | `1` 여덟 · `1` · `1 2 3 4 5 6 7` · `1 1 1` | `0` 여덟 · `0` · `1 2 3 4 5 6` · `0 0 0` | 토큰 삭제 11 가운데 11 · Gotcha 9 를 `## Process` 뒤로 → 둘째 줄 `0` |
| SK-03 | 일곱 이름 · `n=1 prompt=1 assertions=1 source=3 stack_setup=1` · `same=5` | 여섯 이름 · `n=0` · `same=5` | 새 사례 assertion 하나 지움 → `assertions=0` · 기존 사례 한 글자 → `same=4` |
| SK-04 | `version=0.3.0 runner=1` · `gate_cases=6 same=1 note=6` · `folder=4 referenced=4 equal=1` | `version=0.2.0 runner=0` · `gate_cases=0 same=0 note=0` · `folder=3 referenced=0 equal=0` | `g4-ko-unsourced` 기대 넷째 줄 `unsourced_boxes=2` → `same=0` |
| SK-05 | `bash=1 zsh=1 lines=5` | `bash=0 zsh=0 lines=1` | `[미검증] 조회 실패` 줄 지움 → `bash=0 zsh=0 lines=5` |
| SK-06 | 조건 줄의 다섯 줄 그대로 | 러너 없음 | 대조 넷이 측정 안에 있다 |
| SK-07 | `1 1 1` · `1` · `1 1 1 0` | `0 0 0` · `0` · `0 0 0 1` | 토큰 삭제 7 가운데 7(0 기대 하나는 끝 판에 없음) · 새 줄을 절 끝으로 → 둘째 줄 `0` |
| SK-08 | `old=0 1 1` | `old=1 0 0` | 토큰 삭제 2 가운데 2(0 기대 하나는 끝 판에 없음) |
| SK-09 | `1 1 1 1 1 0` · `1 1 0` · `1 1 0` · `files=1 example=1 assert=1 desc=1` | `0 0 0 0 0 1` · `0 0 1` · `0 0 1` · `files=0 example=0 assert=0 desc=0` | 토큰 삭제 9 가운데 9(0 기대 셋은 끝 판에 없음) · 옛 나쁜 예 되살림 → 첫 줄 끝 `1` |
| ER-01 | `0` · `0` | 재지 않음(notes 없음) | format-checklist 에 가짜 URL → `1` · notes 에 가짜 URL → 둘째 `1` · notes 지움 → `NOTES_MISSING` |
| ER-02 | `added=266 k02=0 names=0 kit_names=0 generic=1` | `added=0 k02=0 names=0 kit_names=1 generic=0` | 「이 값이 적용된다」 → `k02=1` · 「fit-pal 에서 본 일」 → `names=1 kit_names=1` |
| ER-03 | `notes_committed=1` · `1` 아홉 · `1 1 1 1 1 1 1 1 1 1 2` · `1 1 1` · `0` | 재지 않음 | ci.yml 줄을 반영 절 문장으로만 → 셋째 줄 `0 0 0 1 1 1 1 1 1 1 2` · 새 넘김 두 줄을 뺀 notes(검토 전 모의본 모양) → 셋째 줄 `1 1 1 1 1 1 1 0 0 0 0` · CocoaPods 줄을 메모 절로 → 넷째 줄 `1 1 0` · 변형 `unsigned-shared` · `signed-outside` · `cross-phase` 다섯째 줄 `1`, `unsigned-mine` `0` |
| ER-04 | 조건 줄의 여섯 줄 그대로 | 러너 없음 | 여섯 경우가 측정 안에 있다 |
| AR-01 | `0` · `0 7` · `0` · `SEAL_OK` · `scope_same=1` · `1` | 재지 않음 | `unsigned-mine` ① `1` · `signed-outside` ② `1 7` · `cross-phase` ② `2 7` · 작업 폴더 계약 한 글자 ③ `1` · 끝 판 계약 한 글자 ④ `SEAL_BROKEN` |
| AR-02 | `1 1 \| 1 1 \| 1 1 1 100755 \| 1 1 \| 2 1 1 1 1 1` | `0 0 \| 0 1 \| 0 0 0  \| 0 1 \| 0 1 1 1 1 1` | format-checklist 제목 바꿈 → 둘째 칸 `1 0` · 기준 가이드 조항 3 줄 바꿈 → 마지막 칸 `2 0 1 1 1 1` · 변형 `noexec` → `100644` |
| AR-03 | `1 \| 1 1 1 \| 1` | `1 \| 1 1 1 \| 1` | 함수 주석 한 글자 → 첫 값 `0` · 픽스처 끝 빈 줄 → `0 1 1` · 변형 `cross-phase` → 셋째 칸 `0` |
| AP-01 | `version=0.3.2 0` | `version=0.3.2 0` | README 에 「버전 0.3.2」 → `1` |
| AP-03 | `0 0 0 0 0` | 새 픽스처 없음 | 새 픽스처 ```` ```swift ```` → ```` ``` ```` → 다섯째 `1` |
| AP-04 | `1 1` | `1 1` | description 한 글자 → `0 1` |
| RE-01 | `rc=0 EVALS declared=6 ran=6 fail=0 EVALS_PASS` | 러너 없음 | `EVAL_DIR=$(pwd)` → `rc=2 SKILL_MISSING //../SKILL.md` |
| RE-02 | `onboarding-kit/skills/setup-guide/SKILL.md \| 1 0` | 러너 없음 | 러너 끝에 함수를 붙임 → 첫 칸에 러너 · 셋째 값 `9` |
| DG-02 | 다섯 줄 모두 `rules_up=0` | 네 파일 `rules_up=0`(편집 전과 같은 판) · 새 픽스처는 없어 `LINT_NOT_RUN` | Gotcha 9 끝과 `## Process` 사이 빈 줄 삭제 → SKILL.md 줄 `rules_up=1 MD022:0>1`(같은 사본에서 옛 측정 `new-warnings.sh` 는 `new_warnings=0`) · 예 표 끝과 `### 3.` 사이 빈 줄 삭제 → `rules_up=2 MD022:0>1 MD058:0>1` · `#bad heading` → `rules_up=1 MD018:0>1` · 픽스처 URL 의 `<…>` 벗김 → `rules_up=1 MD034:0>1` · `node_modules` 없는 폴더 → `LINT_NOT_RUN` · 종료 코드 2 |
| DG-04 | 조건 줄의 두 줄 그대로 | 러너 없음 | `[[ -n x ]] \|\| true` → `shellcheck rc=1 lines=7` · dash `err=1` · `echo oops >&2` → 네 칸 `err=1` |
| DG-05 | `10 0 rc=0` · `stale_old=15 files=7 hits=0` | `10 0 rc=0` · 둘째 줄 없음(새 파일 둘이 없어 파이썬이 멈춘다) | `nam: setup-guide` → `10 1 rc=2` · README 에 `7개 킷` → `hits=1`(같은 사본에서 `check-stale-values.py` 는 `되살아난 옛 값 없음` · 종료 코드 0) · AUTO 표 `/setup-guide` 행을 `BROKEN` 으로 → `sync-docs.py --check-only onboarding-kit` 가 `동기화됨` · 종료 코드 0 |
| DG-06 | `scope-isolation: PASS` · `doc-contracts: PASS` · `doc_checked=2 doc_mine=0` · `violators=0 mine=0` | — | 변형 `cross-phase` → `scope-isolation: FAIL` · `violators=1 mine=1` |
| N/A 줄 | `SC-00=0 DG-01=0` (`m NA`) | — | 변형 `signed-outside` → `SC-00=1` |

- 문장 삭제 대조(`del.sh`, 목록은 `gen-del.py` 가 `m.sh` 에서 뽑는다): SK-01 · SK-02 · SK-07 · SK-08 · SK-09 갈래의 토큰 61 개(`printf` 형식 문자열 `%s\n` 둘은 뺐다)를 끝 판 사본에서 하나씩 한 번 지우고 그 조건을 다시 쟀다 — 56 개는 출력이
  바뀌었고(DROP), 5 개는 끝 판에 없었다(MISSING). 없던 다섯은 전부 0 을 기대하는 옛 문장이다(「Phase 13으로」 · 「마커 + 사유 한 줄」 · Gotcha 8 옛 나쁜 예 · Phase 1 옛 설정 파일 목록 · project-detection 옛 줄) — 시작 커밋 판 값이 1
- 양성 · 음성 대조(`ctl.sh` · 검토 반영분 `ctl2.sh`, 끝 판 사본 한 군데를 바꾸고 되돌림)와 예행 변형 다섯(`unsigned-mine` · `unsigned-shared` · `signed-outside` · `cross-phase` · `noexec`)이 위 표의 「대조」 칸이다.
  조건마다 기대값에서 벗어난 값이 나왔다 — 0 을 기대하는 조건은 1 이상이, 1 을 기대하는 조건은 0 이, 같아야 하는 두 판 비교는 `0` · `SEAL_BROKEN` 이 나왔다
- 러너 대조는 측정 자체에 들어 있다(SK-06 넷 · ER-04 여섯). 넷 다 변이가 실제로 걸렸는지 `sub` 가 먼저 확인한다 — 한 번만 나오는 글이 아니면 `NEG_EDIT_FAIL`
- 러너를 직접 dash · `/bin/sh` · bash · zsh 로 돌린 출력(DG-04)은 네 해석기에서 같았다. `shellcheck -s sh` 0 줄

## Skill

- [ ] SK-01: `onboarding-kit/skills/setup-guide/references/format-checklist.md` 의 `### 2. 사전 요구사항` 절(다음 `### 3.` 제목 전까지)에 막는 요구 세 칸 규칙이 있다 — (a) 규칙 머리 「**막는 요구는 세 칸으로 쓴다** (SKILL.md Gotcha 9).」 와 두 문장(「계정 등급 · 기기 · 권한 · 출시 상태처럼 …」 · 「「이게 없으면 진행할 수 없다」 한 줄로 끝내지 않는다 — …」) (b) 칸 표 머리 `| 칸 | 쓰는 것 |` · 구분선 · 행 셋(`| 출처 |` · `| 막히는 것 |` · `| 우회 |`)이 이어진 자리 1 개와 세 행의 글이 글자 그대로 — 우회 칸은 출처에 없으면 `우회 없음(출처 확인)` (c) 「예 — FCM iOS (조회 2026-09-24):」 와 예 표 머리 `| 요구 | 출처 | 막히는 것 | 우회 |` · 구분선 · 행 셋(`| 실기기 |` · `| 유료 개발자 계정 |` · `| 앱 출시 |`)이 이어진 자리 1 개, 칸 글 여덟 — 실기기는 Firebase Apple 셋업 출처 · 원격 메시지 수신 확인만 막힘 · `우회 없음(출처 확인)`, 유료 계정은 지원 기능 표 · 멤버십 개요 두 출처 · Push Notifications 기능과 APNs 키 구성만 막힘 · 가입 비용 면제, 앱 출시는 「막는 요구가 아니다」 와 Push Notification Console 출처 (d) 규칙 머리가 파일 전체에 1 번 (e) 같은 절 첫 목록의 계정/권한 줄이 「- 필요한 계정/권한 (예: Apple Developer Program 가입) — 막는 요구면 아래 세 칸으로 쓴다」 다 — 옛 한 줄 요구 모양을 새 규칙으로 잇는다 [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-01` 두 줄이 열여섯 값 모두 `1` · `runs=1 1 whole=1`. 알려진 답: 시작 커밋 판은 `0` 열여섯 · `runs=0 0 whole=0`.
       문장 삭제 대조: 이 갈래의 토큰 스물일곱(문장 열여섯 · 표 줄 머리 열 · 규칙 머리 하나)을 끝 판 사본에서 하나씩 지우면 전부 값이 떨어진다. 칸 표의 `| 막히는 것 |` 행 뒤에 빈 줄을 끼운 사본에서 `runs=0 1`,
       첫 목록 줄을 옛 줄 「- 필요한 계정/권한 (예: Apple Developer Program 가입)」 로 되돌린 사본에서 첫 줄 마지막 값 `0`)
- [ ] SK-02: `onboarding-kit/skills/setup-guide/SKILL.md` 에 (a) 제목 `### Gotcha 9: 막는 요구는 출처 · 막히는 것 · 우회 세 칸으로 — 셋업 전체가 막힌 것처럼 쓰지 마라` 절이 `### Gotcha 8: ` 뒤 · `## Process` 앞에 있고 (b) 그 절에 일곱 문장 조각 — 한 줄로 쓰면 셋업 전체가 막혔다고 읽는다는 문장 · format-checklist §2 를 가리키는 세 칸 문장 · 출처가 요구하지 않는 것을 막는 요구로 쓰지 않는다(앱 출시 예) · 출처에 없는 우회를 지어내지 않는다(`우회 없음(출처 확인)`) · 스킬 자신의 불가 결론에도 `§3.7 조항 3 의 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)` · 실측 머리 「같은 모양의 실측(`/insights` 2026-09-24 F10)」 · 사용자 말 「앱 올리면 되잖아?」 — 이 각각 1 줄 이상이며 (c) `### Phase 4: 검증 + 완료 안내` 목록 번호가 `1 2 3 4 5 6 7` 이고 5 번이 「**막는 요구 세 칸 확인** — … (Gotcha 9). 출처가 요구하지 않는 요구는 지운다」 · 6 번이 마커 집계 보고 · 7 번이 사용자 안내다 [exact, enumerated]
      (Given: `$END` 판 · When: `type m >/dev/null || exit 2;` 뒤 `m SK-02` · Then: 네 줄이 `1` 여덟 · `1` · `1 2 3 4 5 6 7` · `1 1 1`.
       알려진 답: 시작 커밋 판 `0` 여덟 · `0` · `1 2 3 4 5 6` · `0 0 0`. 문장 삭제 대조: 토큰 열하나를 하나씩 지운 사본에서 전부 값이 떨어진다. Gotcha 9 절을 `## Process` 뒤로 옮긴 사본에서 둘째 줄 `0`)
- [ ] SK-03: `onboarding-kit/skills/setup-guide/evals/evals.json` 의 `cases` 가 시작 커밋 판 여섯 뒤에 사례 `blocking-requirement-scope` 하나를 더한 일곱이고, 그 사례의 `prompt` 가 「FCM iOS 설정해줘. 유료 개발자 계정도 실기기도 아직 없고 앱도 출시 전이야」, `assertions` 가 `m.sh` `SK-03)` 갈래의 여섯 줄과 같은 순서 · 같은 글이며, `source` 에 근거 URL 셋(Firebase Apple 셋업 · Apple 지원 기능 표 · Push Notification Console)이 있고 `setup.project_files` 에 `pubspec.yaml` 이 있다. `no-invented-paths` 밖의 기존 사례 다섯은 시작 커밋 판과 JSON 값이 같다 [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-03` 세 줄이 `flutter-fcm-ios stack-not-detected apple-site-distinction deprecation-claim-fidelity source-ledger-per-step no-invented-paths blocking-requirement-scope` · `n=1 prompt=1 assertions=1 source=3 stack_setup=1` · `same=5`.
       알려진 답: 시작 커밋 판 여섯 이름 · `n=0` · `same=5`. 음성 대조: 끝 판 사본에서 새 사례의 assertion 한 줄을 지우면 둘째 줄 `assertions=0`, 기존 사례 `stack-not-detected` 의 assertion 한 글자를 바꾸면 셋째 줄 `same=4`)
- [ ] SK-04: 같은 `evals.json` 의 `version` 이 `0.3.0`, `runner` 가 `sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh` 이고, `gate_cases` 가 여섯 — `ok-flutter` · `stack-unset` · `stack-empty` · `g4-ko-sourced` · `g4-ko-unsourced` · `ledger-marker-swift` — 이며 각 사례의 `fixture` · `stack`(`"flutter"` · `null` · `""`) · `expect`(`guide_gate` 출력 다섯 줄)가 `m.sh` `SK-04)` 갈래의 목록과 같은 순서 · 같은 값이고 여섯 모두 `note` 를 갖는다. `evals/fixtures/` 의 `.md` 넷(`gate-ok-flutter.md` · `gate-g4-ko-sourced.md` · `gate-g4-ko-unsourced.md` · `gate-fail-ledger-marker-swift.md`)이 전부 어느 사례에 등록돼 있다 [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-04` 세 줄이 `version=0.3.0 runner=1` · `gate_cases=6 same=1 note=6` · `folder=4 referenced=4 equal=1`.
       알려진 답: 기대 출력 다섯 줄은 픽스처를 손으로 센 값이다 — `gate-ok-flutter.md` 는 `## Step ` 2 · `**출처:**` 2, 두 G4 픽스처는 1 · 1, 새 픽스처는 SK-05. 시작 커밋 판은 `version=0.2.0 runner=0` · `gate_cases=0 same=0 note=0` · `folder=3 referenced=0 equal=0` — 폴더에만 있는 셋이 이 결함의 실물이다.
       음성 대조: 끝 판 사본에서 `g4-ko-unsourced` 의 `expect` 넷째 줄을 `unsourced_boxes=2` 로 바꾸면 둘째 줄 `same=0`)
- [ ] SK-05: 새 픽스처 `onboarding-kit/skills/setup-guide/evals/fixtures/gate-fail-ledger-marker-swift.md` 에 `$END` 판 SKILL.md 의 `guide_gate` 를 `flutter` 스택으로 돌리면 bash · zsh 두 셸 출력이 모두 손으로 센 답 다섯 줄 `G1_LEDGER FAIL steps=2 ledger=1` · `G2_MARKER FAIL bare=1 invalid=2 env=1` · `G3_STACKMIX FAIL swift_fence=1` · `G4_DEPRECATION PASS unsourced_boxes=0` · `GATE_FAIL` 과 글자 그대로 같다 — G1 · G2 · G3 의 0 · 같은 수 기대값이 살아 있다는 양성 대조다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-05` 가 `bash=1 zsh=1 lines=5`. 알려진 답: 이 파일의 `## Step ` 줄 2 · `**출처:**` 줄 1 · 접미 없는 `[미검증]` 1 · `[미검증:INVALID]` 2 · `[미검증:ENV]` 1 · 여는 ```` ```swift ```` 1 · `❌ Deprecated` 0 — 봉인 전에 손으로 세고 `guide_gate` 출력과 맞췄다. 시작 커밋 판은 파일이 없어 `bash=0 zsh=0 lines=1`(`GATE_BLOCKED`).
       음성 대조: 끝 판 사본에서 접미 없는 `[미검증] 조회 실패` 줄을 지우면 `bash=0 zsh=0 lines=5`)
- [ ] SK-06: 러너 `onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh` 가 `$END` 판 킷 사본에서 종료 코드 0 으로 끝나고, `PASS  ` 줄 여섯이 각자 픽스처 이름을 적으며(`gate-ok-flutter.md` 셋 · 나머지 셋은 하나씩), 마지막 두 줄이 `EVALS declared=6 ran=6 fail=0` · `EVALS_PASS` 다. 그리고 SKILL.md 사본의 `guide_gate` 를 한 군데씩 깨뜨린 넷에서 종료 코드 1 과 그 자리를 잰 사례만 `FAIL` 로 나온다 — (n1) G4 한국어 근거 토큰을 지우면 `g4-ko-sourced` 하나 (n2) 스택이 비었을 때의 FAIL 분기를 끄면 `stack-empty` · `stack-unset` 둘 (n3) 접미 없는 마커를 세는 문자열을 바꾸면 `ledger-marker-swift` 하나 (n4) 따옴표 없는 변수 한 줄로 두 셸 출력을 갈라 놓으면 여섯 전부와 `shell_mismatch` 여섯 [exact, enumerated]
      (Given: `$END` 판 · When: `type m >/dev/null || exit 2; type runk >/dev/null || exit 2;` 뒤 `m SK-06` · Then: 다섯 줄이
       `rc=0 pass=6 3 1 1 1 | EVALS declared=6 ran=6 fail=0 EVALS_PASS` ·
       `rc=1 | g4-ko-sourced | sm=0 fm=0 | EVALS declared=6 ran=6 fail=1 | EVALS_FAIL` ·
       `rc=1 | stack-empty,stack-unset | sm=0 fm=0 | EVALS declared=6 ran=6 fail=2 | EVALS_FAIL` ·
       `rc=1 | ledger-marker-swift | sm=0 fm=0 | EVALS declared=6 ran=6 fail=1 | EVALS_FAIL` ·
       `rc=1 | g4-ko-sourced,g4-ko-unsourced,ledger-marker-swift,ok-flutter,stack-empty,stack-unset | sm=6 fm=0 | EVALS declared=6 ran=6 fail=6 | EVALS_FAIL`.
       음성 대조는 측정 안에 있다 — 넷 다 러너가 사본의 SKILL.md 에서 함수를 뽑기 때문에 떨어진다. 러너가 함수 사본을 따로 들고 있으면 넷이 첫 줄처럼 통과해 이 조건이 FAIL 한다. 사본 편집이 안 걸리면 `NEG_EDIT_FAIL` 이 찍혀 역시 FAIL 이다)
- [ ] SK-07: 러너를 부르는 자리가 둘이다 — (a) SKILL.md `### Guide Conformance Gate (E3)` 절의 「- **게이트를 우회하거나 …」 줄 바로 다음 줄이 「- **게이트 함수를 고쳤으면 `sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh` 가 `EVALS_PASS` 로 끝나야 한다.**」 로 시작하고 두 문장(함수를 SKILL.md 에서 뽑아 `gate_cases` 입력마다 두 셸 출력을 기대 출력 전체와 대조한다 · 판정이 바뀌는 수정이면 기대 출력도 같은 커밋에서 고친다)을 담는다 (b) `onboarding-kit/README.md` `## 카이젠` 절에 「- 전체 카이젠: `/kaizen` (Phase 14로 자동 실행)」 과 「- `guide_gate` 시험: `sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh` — …」 줄(폴더에만 있고 등록 안 된 픽스처도 실패로 센다는 말 포함)이 있고 「Phase 13으로」 가 0 줄이다 [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-07` 세 줄이 `1 1 1` · `1` · `1 1 1 0`. 알려진 답: 시작 커밋 판 `0 0 0` · `0` · `0 0 0 1`.
       문장 삭제 대조: 1 을 기대하는 토큰 일곱(절 제목 `## 카이젠` 포함)을 하나씩 지운 사본에서 전부 값이 떨어진다. 새 줄을 `### Guide Conformance Gate (E3)` 절 끝으로 옮긴 사본에서 둘째 줄 `0`)
- [ ] SK-08: Phase 1 넘김 — SKILL.md 에 「마커 + 사유 한 줄」 이 0 줄이고, `### 출처 원장 (Source Ledger)` 절에 「fetch 가 끝까지 실패한 항목은 조용히 넘기지 말고 마커와 아래 네 요건을 붙인다.」 와 「네 요건은 `harness/docs/guides/skill-design-guide.md` §3.7 조항 3 의 네 칸과 같다 — ①③ 이 막는 것, ② 가 시도한 우회, ④ 가 통제 불가 사유와 재검증 명령이다.」 가 각각 1 줄이다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-08` 이 `old=0 1 1`. 알려진 답: 시작 커밋 판 `old=1 0 0`. 문장 삭제 대조: 새 문장 둘을 하나씩 지운 사본에서 그 값 `0`)
- [ ] SK-09: 값이 든 `.env` 를 열지 않는다 — (a) SKILL.md `### Gotcha 8: ` 절에 「**값이 든 `.env` 파일(`.env.local` · `.env.production` 등)은 열지 않는다.**」 로 여는 한 단락(키 이름은 `.env.example` 같은 예시 파일이나 그 키를 읽는 코드에서 · 둘 다 없으면 사용자에게 묻는다 · 사용자가 직접 요청한 경우만 예외 · 실측 2026-05-28)의 네 조각과 새 나쁜 예 「- ❌ 프로젝트가 이미 다른 이름의 키를 쓰는데(`.env.example` · 코드에 있다) …」 가 각각 1 줄이고 옛 나쁜 예 「- ❌ 기존 `.env` 에 다른 이름의 키가 있는데」 가 0 (b) `### Phase 1: 스택 + 외부 서비스 탐지` 절의 설정 파일 목록이 `.env.example` 류이고 「값이 든 `.env` 파일은 있는지만 보고 열지 않는다 (Gotcha 8).」 가 있으며 옛 「설정 파일(`.env*`,」 가 0 (c) `onboarding-kit/skills/setup-guide/references/project-detection.md` 의 `.env` 줄이 `.env.example` 류와 「있는지만 보고 열지 않는다 (SKILL.md Gotcha 8)」 로 바뀌고 옛 「- `.env*` — 」 가 0 (d) `evals.json` `no-invented-paths` 사례의 `setup.project_files` 가 `.env` · `.env.example` · `lib/main.dart`, `setup.env_example_contains` 가 `FCM_CREDENTIALS_PATH=` 하나, 마지막 assertion 이 `does_not_read_file('.env')` 줄, `description` 끝이 「. 값이 든 .env 는 열지 않고 키 이름은 .env.example 에서 얻는다 (Gotcha 8)」 다 [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-09` 네 줄이 `1 1 1 1 1 0` · `1 1 0` · `1 1 0` · `files=1 example=1 assert=1 desc=1`. 알려진 답: 시작 커밋 판 `0 0 0 0 0 1` · `0 0 1` · `0 0 1` · `files=0 example=0 assert=0 desc=0`.
       문장 삭제 대조: 1 을 기대하는 토큰 아홉을 하나씩 지운 사본에서 전부 값이 떨어진다. 옛 나쁜 예 줄을 되살린 사본에서 첫 줄 끝 값 `1`)

## Script

- [ ] SC-00: N/A (Script 카테고리는 `release.sh` 연동 · 버전 올림 · `marketplace.json` 갱신이다. 이 Phase 는 그 파일을 건드리지 않는다 — 공유 파일은 Final 몫. 새 러너는 스킬 평가 도구라 Skill 카테고리에서 잰다(SK-06 · ER-04). 측정: `type m >/dev/null || exit 2;` 뒤 `m NA` 의 `SC-00=0`. 양성 대조: 예행 변형 `signed-outside` 에서 `SC-00=1`)

## Error

- [ ] ER-01: 일곱 파일에 새로 생긴 URL 과 `.harness/.meta/kaizen-0924/phase14-notes.md` 의 URL 이 전부 이 Phase 의 외부 근거 파일 `.harness/.meta/evidence/phase14.md` 에 있다 — 일곱 파일은 파일마다 편집 전 판과 비교하고 새 파일 둘은 빈 판과 비교한다 (러닝북 — 근거 파일에 없는 URL 을 지어내지 않는다 · notes 킷 로그의 출처 URL 은 근거 파일에서만) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-01` 두 줄이 `0` · `0`. notes 가 `$END` 판에 없으면 둘째 줄이 `NOTES_MISSING` 이라 FAIL 이다.
       양성 대조: 끝 판 format-checklist 끝에 `https://example.invalid/x` 를 더한 사본에서 첫 줄 `1`, notes 끝에 더한 사본에서 둘째 줄 `1`, notes 를 지운 사본에서 둘째 줄 `NOTES_MISSING`)
- [ ] ER-02: 일곱 파일에 더한 줄에 번역투 6 종(`tone-kit/references/locale-korean.md` §2 치환표의 grep 열)이 0 건, 특정 앱 이름 · 특정 화면 도구 서버 이름(`fit-?pal` · `fit_pal` · `flutter[-_]playwright` · `playwright-mcp` · `chrome-devtools-mcp`, 대소문자 무시)이 0 건이고, `$END` 판 `onboarding-kit/` 전체에서 같은 이름이 0 줄이며 Gotcha 4 가 「조직 식별자 없는 흔한 조합(`com.<앱이름>.app`)은 누가 선점했을 확률 높음.」 을 담는다 (러닝북 말투 · 문서 규칙 — 킷 파일에 특정 앱 이름을 넣지 마라) [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-02` 가 `added=N k02=0 names=0 kit_names=0 generic=1` 이고 N 이 1 이상. 알려진 답: 시작 커밋 판 `kit_names=1`(SKILL.md Gotcha 4 의 `com.fitpal.app`) · `generic=0`.
       양성 대조: SKILL.md 끝에 「이 값이 적용된다」 를 더한 사본에서 `k02=1`, 「fit-pal 에서 본 일」 을 더한 사본에서 `names=1 kit_names=1`)
- [ ] ER-03: 이 Phase 범위 밖 반대편을 명시적 미완으로 넘기고 건드리지 않는다 — `.harness/.meta/kaizen-0924/phase14-notes.md` 가 `$END` 에 커밋돼 있고 (a) 처리 배정표 키 `other-kits:P3` · `other-kits:P9` 와 러닝북이 적게 한 절 머리 일곱(`## 바꾼 파일` · `## 반영한 처리 배정표 키` · `## 미반영 키와 사유` · `## 넘기는 것` · `## changelog 한 단락` · `## 킷 로그 한 단락` · `## 다음 사이클 메모`)이 각각 1 줄 이상 (b) `## 넘기는 것` 절 안에 넘김 열하나 — `.github/workflows/ci.yml` (Final — validate 작업에 넣을 두 줄: `command -v zsh` 로 보고 없을 때만 설치 · `sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh`) · `docs/onboarding-kit/examples/fcm-ios-setup-guide.md` (Final — Xcode · iOS 최소 버전, 시뮬레이터 주장, 세 칸, 앱 이름) · `docs/onboarding-kit/fcm-ios-example.html` (Final F2) · `.claude/skills/onboarding-kaizen/SKILL.md` (Phase 4 검증에 러너) · `plugin.json` (Final — 버전) · `docs/onboarding-kit/setup-guide.html` · `docs/onboarding-kit/format-checklist.html` · `docs/onboarding-kit/project-detection.html` (Final F2 — 이 Phase 가 바꾼 세 소스에서 만든 페이지인데 드리프트 목록에 안 나온다) · `scripts/detect-docs-drift.py` (onboarding-kit 소스 매핑이 없다 — 예행 판에서 `no docs drift since da9fbae`) 이 각각 1 줄 이상 (c) `## 미반영 키와 사유` 절 안에 `2026-07-20` (evals `source` 조회일 — 본문 주장 재확인 없음) · `Workload Identity Federation` (근거 파일이 추론이라 적음) · `CocoaPods` (근거 파일이 바로 바꾸지 말라 적음) 이 각각 1 줄 이상이고, (d) 구간 안에서 공유 파일 · 다른 Phase 파일을 건드린 커밋 가운데 다른 Phase 서명이 없는 커밋이 0 개다 [exact, enumerated]
      (Given: BUILD 가 notes 를 커밋하고 개정 파일에 그 sha 로 `end_sha:` 를 덧붙인 뒤 · When: `type m >/dev/null || exit 2; type not_other >/dev/null || exit 2;` 뒤 `m ER-03` · Then: 다섯 줄이 `notes_committed=1` · 아홉 값 모두 `1` 이상 · 열한 값 모두 `1` 이상 · 세 값 모두 `1` 이상 · `0`. 다섯째 줄이 0 이 아니면 FAIL 이다.
       (d) 의 경로는 `m.sh` `ER-03)` 갈래의 `not_other` 인자 열넷이다 — 서명 줄 목록이 아니라 경로로 직접 세므로 서명을 빠뜨린 커밋도 보인다. 다른 Phase 서명이 달린 커밋은 그 Phase 몫이라 뺀다.
       봉인 전 실측: notes 모의본을 커밋한 예행 판 `notes_committed=1` · `1` 아홉 · `1 1 1 1 1 1 1 1 1 1 2` · `1 1 1` · `0`. 음성 대조: 넘김 표의 `.github/workflows/ci.yml` 줄을 지우고 같은 경로를 `## 반영한 처리 배정표 키` 절 문장에만 남긴 사본 → 셋째 줄 첫 세 값 `0 0 0`(그 줄에 두 명령이 함께 있다) ·
       새 넘김 두 줄(페이지 셋 · 드리프트 스크립트)을 뺀 사본 → 셋째 줄 `1 1 1 1 1 1 1 0 0 0 0` ·
       미반영 절의 `CocoaPods` 줄을 `## 다음 사이클 메모` 절로만 옮긴 사본 → 넷째 줄 `1 1 0`.
       양성 대조: 변형 `unsigned-shared`(서명 없이 루트 README) · `signed-outside`(서명하고 plugin.json) · `cross-phase`(서명하고 harness 파일) 에서 다섯째 줄 `1`. `unsigned-mine` 은 이 Phase 폴더라 `0` 이고 AR-01 ① 이 잡는다)
- [ ] ER-04: 러너가 멈춰야 할 때 멈추고, 한 칸이 깨져도 나머지를 잰다 — `$END` 판 킷 사본 여섯에서 (e1) 등록 안 된 픽스처 `extra-unregistered.md` 를 폴더에 더하면 종료 코드 1 · `FAIL  orphan_fixture` 한 줄 · `ran=6` (e2) 등록된 픽스처 하나를 지우고 다른 픽스처에 Swift 코드 블록을 더하면 종료 코드 1 · 지운 사례 `fixture_missing` 한 줄과 나머지 위반 셋이 함께 `FAIL` · `ran=6 declared=6` (e3) `gate_cases` 가 빈 목록이면 종료 코드 2 · `NO_CASES` (e4) PATH 에서 zsh 를 숨기면 종료 코드 2 · `TOOL_MISSING zsh` — 숨겨졌다는 확인(`zsh_visible=0`)과 함께 (e5) SKILL.md 의 함수 이름을 바꾸면 종료 코드 2 · `GATE_EXTRACT_FAIL` (e6) `evals.json` 이 깨지면 종료 코드 2 · `EVALS_UNREADABLE`. 어느 경우도 `EVALS_PASS` · 종료 코드 0 이 아니다 [exact, enumerated]
      (측정: `type m >/dev/null || exit 2; type runk >/dev/null || exit 2;` 뒤 `m ER-04` 여섯 줄이
       `rc=1 | orphan_fixture | sm=0 fm=0 | EVALS declared=6 ran=6 fail=1 | EVALS_FAIL` ·
       `rc=1 | g4-ko-sourced,ok-flutter,stack-empty,stack-unset | sm=0 fm=1 | EVALS declared=6 ran=6 fail=4 | EVALS_FAIL` ·
       `rc=2 |  | sm=0 fm=0 |  | NO_CASES` · `rc=2 zsh_visible=0 | TOOL_MISSING zsh — 두 셸 대조를 할 수 없다` ·
       `rc=2 |  | sm=0 fm=0 |  | GATE_EXTRACT_FAIL` · `rc=2 |  | sm=0 fm=0 |  | EVALS_UNREADABLE`.
       (e2) 가 qa-evaluator 규칙 10 ③(한 칸 못 읽으면 전체 꺼짐)의 사본 입력이다. (e1) 은 폴더에만 있고 실행 목록(`gate_cases`)에 없는 픽스처다 — 규칙 10 ②(표에만 올리고 안 도는 시험)와 방향은 반대이고, 안 도는 시험 파일을 러너가 스스로 잡는지 본다. 사본 편집이 안 걸리면 `NEG_EDIT_FAIL` 이 찍혀 기대 줄과 달라진다)

## Architecture

- [ ] AR-01: 이 Phase 의 변경이 허용 경로 안에 머물고, 범위 선언 블록이 그 경로와 같으며, 이 계약이 봉인돼 있다 [exact, enumerated]
      (Given: BUILD 가 개정 파일에 `end_sha:` 를 적은 뒤 · 이 Phase 커밋 메시지마다 서명 줄 `Kaizen-Phase: kaizen-0924-p14-onboarding-kit` · When: `type m >/dev/null || exit 2; type unsigned_on >/dev/null || exit 2; type verify_seal >/dev/null || exit 2;` 뒤 `m AR-01` · Then: 여섯 줄이 —
       ① `0` — `onboarding-kit/` 를 건드린 구간 안 커밋이 전부 서명했다(이 구간에 이 폴더를 고칠 수 있는 Phase 는 14 하나다)
       ② `0 7` — 서명 커밋이 건드린 `.harness/` 밖 경로 가운데 일곱 파일 밖이 0 개, 일곱 파일이 전부 있다
       ③ `0` — `harness/references/contract-schema.md` §`.harness/` 범위 조건 의 권장 형태로 `.harness/` 의 계약 전부에 `verify_seal` 을 돌려 이 Phase 몫 `SEAL_BROKEN` 이 0 개
       ④ `SEAL_OK` — `$END` 판의 이 계약이 봉인돼 있다(`SEAL_ABSENT` 는 봉인을 건너뛴 것이라 FAIL)
       ⑤ `scope_same=1` — `## 범위 경계` 절 `# sprint-scope` 블록의 `.harness/` 밖 줄이 `FILES` 일곱 줄과 같다 ⑥ `1` — 그 블록에 `.harness/` 줄이 하나 있다.
       봉인 전 실측: 예행 판 `0` · `0 7` · `0` · `SEAL_OK` · `scope_same=1` · `1`. 양성 대조: 변형 `unsigned-mine` ① `1` · 변형 `signed-outside` ② `1 7` · 변형 `cross-phase` ② `2 7` ·
       예행 작업 폴더 계약의 조건 줄 한 글자를 바꾼 사본 ③ `1` · 끝 판 계약의 조건 줄 한 글자를 바꾼 사본 ④ `SEAL_BROKEN`)
- [ ] AR-02: 새 문장이 가리키는 자리가 실제로 있다 — (a) format-checklist 의 `(SKILL.md Gotcha 9)` 1 과 SKILL.md `### Gotcha 9: ` 제목 1 (b) Gotcha 9 의 `(`references/format-checklist.md` §2` 1 과 format-checklist `### 2. 사전 요구사항` 제목 1 (c) 러너 경로 `sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh` 가 SKILL.md · README · evals.json 에 각각 1 이고, `$END` 판 git 에서 그 파일 모드가 `100755` (d) project-detection 의 `(SKILL.md Gotcha 8)` 1 과 SKILL.md `### Gotcha 8: ` 제목 1 (e) Counterpart — SKILL.md 의 `§3.7 조항 3 의 네 칸` 2(출처 원장 절 · Gotcha 9)와 `harness/docs/guides/skill-design-guide.md` 의 조항 3 줄 「3. **검증 불가 시 `[미검증]` 에 네 칸을 붙인다.**」 1 · 네 칸 줄(`- **막는 것** —` · `- **시도한 우회** —` · `- **통제 불가 사유** —` · `- **재검증 명령** —`) 각 1 [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m AR-02` 가 `1 1 | 1 1 | 1 1 1 100755 | 1 1 | 2 1 1 1 1 1`. 알려진 답: 시작 커밋 판은 새로 생기는 자리만 없어 `0 0 | 0 1 | 0 0 0  | 0 1 | 0 1 1 1 1 1`.
       양성 대조: 끝 판 사본에서 format-checklist 의 `### 2. 사전 요구사항` 을 `### 2. 사전 준비` 로 바꾸면 둘째 칸 `1 0` · skill-design-guide 조항 3 줄을 바꾸면 마지막 칸 둘째 값 `0` · 러너를 실행 비트 없이 커밋한 예행 판에서 셋째 칸 끝 `100644`)
- [ ] AR-03: 손대지 않을 곳이 그대로다 — (a) SKILL.md 의 `guide_gate` 를 담은 bash 코드 블록(여는 펜스부터 닫는 펜스까지)이 시작 커밋 판과 글자 그대로 같고 비지 않았다 — 기대 출력을 잰 함수가 이 함수다 (b) 기존 픽스처 셋(`gate-ok-flutter.md` · `gate-g4-ko-sourced.md` · `gate-g4-ko-unsourced.md`)이 시작 커밋 판과 같다 (c) `onboarding-kit/skills/setup-guide/references/search-strategy.md` 가 시작 커밋 판과 같다 [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m AR-03` 이 `1 | 1 1 1 | 1`. 양성 대조: 끝 판 사본에서 함수 주석 한 글자를 바꾸면 첫 값 `0`, `gate-ok-flutter.md` 끝에 빈 줄을 더하면 둘째 칸 첫 값 `0`, 예행 변형 `cross-phase`(search-strategy 에 빈 줄)에서 셋째 칸 `0`)

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다. 이번 변경에 적용: 일곱 파일에 더한 줄에 onboarding-kit `plugin.json` 의 `version` 값(`$END` 판에서 읽는다)이 0 건이다 — 이 Phase 는 킷 버전을 적지 않고 Final 이 올린다. `evals.json` 의 `0.3.0` 은 평가 파일 자체의 판 번호라 이 값과 다르다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m AP-01` 이 `version=0.3.2 0`. 양성 대조: README 끝에 「버전 0.3.2」 를 더한 사본에서 둘째 값 `1`)
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```` ```text, ```bash, ```yaml ```` 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 이번 변경에 적용: V6 가 읽는 SKILL.md · README 는 DG-05 의 V6 줄이 보고, V6 가 안 읽는 format-checklist · project-detection · 새 픽스처까지 마크다운 다섯 파일 모두 같은 여닫기 방식으로 센 언어 힌트 없는 여는 펜스가 0 이다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m AP-03` 이 `0 0 0 0 0`. 양성 대조: 새 픽스처의 ```` ```swift ```` 를 ```` ``` ```` 로 바꾼 사본에서 다섯째 값 `1`)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL. 이번 변경에 적용: SKILL.md 의 첫 frontmatter 블록이 편집 전과 글자 그대로 같고 `name: setup-guide` 줄이 1 개다 — 그래서 README AUTO 구간과 트리거 설명이 읽는 값도 바뀌지 않는다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m AP-04` 가 `1 1`. 음성 대조: SKILL.md `description` 한 글자를 바꾼 사본에서 `0 1`)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다. 이번 변경에 적용: 러너는 킷 안 실행 파일이고 자기 파일 위치로 경로를 잡아, 레포 밖 폴더(`/`)에서 절대 경로로 불러도 `$END` 판과 같은 결과를 낸다 — CI 든 사람이든 작업 폴더와 상관없이 부를 수 있다 [goal]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m RE-01` 이 `rc=0 EVALS declared=6 ran=6 fail=0 EVALS_PASS`. 음성 대조: 러너 사본의 `EVAL_DIR=$(cd "$(dirname "$0")" && pwd)` 를 `EVAL_DIR=$(pwd)` 로 바꾼 사본을 `/` 에서 부르면 `rc=2 SKILL_MISSING //../SKILL.md`)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다. 이번 변경에 적용: `guide_gate` 정의는 킷 안에서 SKILL.md 하나다 — (a) 줄 머리 `guide_gate() {` 를 담은 onboarding-kit 파일이 `onboarding-kit/skills/setup-guide/SKILL.md` 하나 (b) 러너가 함수를 SKILL.md 에서 뽑는 awk 줄 1 을 갖고 (c) 러너 안에 `guide_gate` 판정 줄(`G1_LEDGER PASS` 같은 `G[1-4]_… PASS|FAIL`)을 따로 적지 않는다(0). 기존 픽스처 셋은 새로 만들지 않고 그대로 등록했다(SK-04 · AR-03) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m RE-02` 가 `onboarding-kit/skills/setup-guide/SKILL.md | 1 0`. 양성 대조: 러너 사본 끝에 함수를 통째로 붙인 사본에서 첫 칸에 러너가 더해지고 셋째 값이 1 이상)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `type m >/dev/null || exit 2;` 뒤 `m NA` 의 `DG-01=0`. 새 셸 파일의 실제 검사는 DG-04)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (`diagnostics.ide_exclude` 값 `[]`) — 이번 변경에 적용: 편집기 마크다운 확장과 같은 조건(markdownlint-cli2 0.23.2 · MD013 끔)으로 마크다운 다섯 파일 **각각**에서 규칙별 경고 수를 편집 전 판(새 파일은 빈 판)과 비교해 늘어난 규칙이 0 개다. 더한 줄만 보지 않는다 — MD022 · MD032 · MD024 는 더한 줄 옆의 손대지 않은 줄에 붙는다(러닝북 측정 구멍 목록). 편집 전부터 있던 경고는 같은 수로 남아도 된다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m DG-02` 다섯 줄이 모두 `rules_up=0` 으로 끝나고 `LINT_NOT_RUN` 줄 0.
       양성 대조: 끝 판 사본에서 SKILL.md Gotcha 9 마지막 줄과 `## Process` 사이 빈 줄을 지우면 SKILL.md 줄 `rules_up=1 MD022:0>1` — 더한 줄만 세던 옛 측정은 같은 사본에서 `new_warnings=0` 이었다.
       format-checklist 예 표 끝과 `### 3.` 사이 빈 줄을 지운 사본에서 그 줄 `rules_up=2 MD022:0>1 MD058:0>1`, format-checklist 끝에 `#bad heading` 을 더한 사본에서 그 줄 `rules_up=1 MD018:0>1`,
       새 픽스처 출처 줄의 `<…>` 를 벗긴 사본에서 그 줄 `rules_up=1 MD034:0>1`. 린터를 못 찾으면 `LINT_NOT_RUN` · 종료 코드 2)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: DG-01 과 같은 `m NA` 의 `DG-01=0`. 실제 시험은 SK-06 · ER-04 · DG-04)
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개 — 이번 변경에 적용: 구동하는 것은 러너 하나다. `$END` 판 러너를 네 해석기(dash · `/bin/sh` · bash · zsh)로 돌리면 네 번 모두 종료 코드 0 · stderr 0 줄 · 표준 출력이 dash 판과 같고, `shellcheck -s sh` 가 종료 코드 0 · 출력 0 줄, 네 해석기의 `-n` 문법 검사가 모두 종료 코드 0 이다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m DG-04` 두 줄이 `dash rc=0 err=0 same=1 | /bin/sh rc=0 err=0 same=1 | bash rc=0 err=0 same=1 | zsh rc=0 err=0 same=1 |` · `shellcheck rc=0 lines=0 n_dash=0 n_sh=0 n_bash=0 n_zsh=0`.
       준비 단계 실측(2026-09-25): `command -v dash` → `/bin/dash` · `shellcheck --version` 0.11.0 · `/bin/sh` 은 bash 3.2.57. 양성 대조: 러너 사본에 `[[ -n x ]] || true` 한 줄을 넣으면 `shellcheck rc=1` · dash 칸 `err=1`, 마지막 판정 줄 앞에 `echo oops >&2` 를 넣으면 네 칸 모두 `err=1`)
- [ ] DG-05: 저장소 검사가 이 킷을 문제로 가리키지 않는다 — `$END` 판을 git 저장소로 만든 사본에서 (a) `scripts/validate-plugin.py onboarding-kit` 출력에 `V1` ~ `V10` 열 줄이 있고 `— OK` · `— SKIP (no templates/)` 로 끝나지 않는 줄이 0 이며 종료 코드 0 (b) `.harness/stale-values.yaml` 의 `old` 값 전부를 일곱 파일에서 직접 센 수가 0 이다. `scripts/check-stale-values.py` 는 `SOURCE_DIRS` 에 onboarding-kit 이 없어 이 킷을 훑지 않고, `scripts/sync-docs.py --check-only` 는 이 README 의 표지(`<!-- AUTO:skills:start -->`)를 못 읽어 늘 `동기화됨` 을 내므로 둘 다 근거로 쓰지 않는다 (러닝북 측정 구멍 목록) [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m DG-05` 두 줄이 `10 0 rc=0` · `stale_old=N files=7 hits=0` 이고 N 이 1 이상. N 을 잠그지 않는 까닭: 등록부는 공유 파일이라 `$END` 전에 다른 주체가 값을 더할 수 있다.
       봉인 전 실측: 예행 판 `10 0 rc=0` · `stale_old=15 files=7 hits=0`. 음성 대조: SKILL.md 의 `name: setup-guide` 를 `nam:` 으로 깬 사본에서 첫 줄 `10 1 rc=2`.
       양성 대조: README 끝에 등록부 옛 값 `7개 킷` 을 더한 사본에서 `hits=1` — 같은 사본에서 `check-stale-values.py` 는 `되살아난 옛 값 없음` · 종료 코드 0 이었다.
       README AUTO 표의 `/setup-guide` 행 설명을 `BROKEN` 으로 바꾼 사본에서 `sync-docs.py --check-only onboarding-kit` 는 `onboarding-kit/README.md: 동기화됨` · 종료 코드 0 이었다 — (b) 에서 뺀 까닭의 실측)
- [ ] DG-06: `python3 scripts/validate-post-kaizen.py --since da9fbae94c13a9a1fc657f29ce9fc380ba9d506b` 출력의 `scope-isolation` · `doc-contracts` 줄이 `FAIL` · `ERROR` 가 아니다. `docs-site-regen` 은 Final F2 몫이라 판정에서 뺀다. 다른 Phase 커밋 때문에 `scope-isolation` 이 FAIL 이면 `--verbose` 위반 커밋 목록을 1 개 이상 읽었고 그 가운데 서명 줄 커밋이 0 개일 때, `doc-contracts` 가 FAIL · ERROR 이면 `validate-doc-contracts.py -v` 가 검사한 경로를 1 개 이상 읽었고 그 가운데 이 Phase 서명 커밋이 건드린 경로가 0 개일 때 이 조건은 PASS 다 — 둘 다 근거에 다른 Phase 몫이라고 적는다 [exact]
      (Given: 작업 폴더에서 `$END` 이후 커밋이 있어도 된다 — 검사는 `HEAD` 까지 보지만 판정은 이 Phase 서명 커밋만 센다 · When: `type m >/dev/null || exit 2;` 뒤 `m DG-06` · Then: 네 줄이 `scope-isolation: PASS` · `doc-contracts: PASS` · `doc_checked=N doc_mine=0` · `violators=V mine=0` 이고 N 이 1 이상. 위 가르기로 PASS 를 줄 때만 첫 두 줄에 `FAIL` 이 있어도 되며, scope-isolation 이 `FAIL` 이면 V 가 1 이상이어야 한다(목록을 못 읽으면 mine 이 조용히 0 이 되므로).
       봉인 전 실측: 예행 판 `scope-isolation: PASS` · `doc-contracts: PASS` · `doc_checked=2 doc_mine=0` · `violators=0 mine=0`. 양성 대조: 변형 `cross-phase` 에서 `scope-isolation: FAIL` · `violators=1 mine=1`)
