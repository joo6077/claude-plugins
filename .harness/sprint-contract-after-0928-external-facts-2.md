---
feature: "바깥 원문 대조 셋 더 반영 · routing 예시 (X1 · X2 · X3 · R)"
slug: after-0928-external-facts-2
created: "2026-09-28 12:46"
complexity: "복잡"
conditions: 26
status: active
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:30978e4d67ca2840
measurement_digest: sha256:8c1c9fcbc681c2ca
locked_at: "2026-09-28 12:58"
---

## 배경

- 사용자 지시 2026-09-28 「맞게 고쳐」 (세션 bda55d45-296c-491f-89ba-b52042d58e72). 위임: 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 · 2026-09-28 「약점과 일부만 한 거 다처리하지??」. 결정 기록 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/.harness/.meta/after-kaizen-0928/decisions.md`.
- 근거는 원문 대조 결과 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/.harness/.meta/after-kaizen-0928/ex/X1.md` · `X2.md` · `X3.md` (Codex gpt-5.6-sol, 2026-09-28 조회, 읽기 전용). 이 계약에서 「X 파일」 은 이 셋을 말한다. R 항목은 앞 묶음 기록 `ex-notes.md` 「남은 것」 둘째 줄과 `ex/A11.md` C 절(Dart 3.7 와일드카드 `_`)이 근거다.
- 처리 규칙: X 파일 판정이 「맞음」 이면 출처(주소 · 날짜)만 붙인다. 「틀림」 · 「원문에 없음」 이면 원문 표현으로 낮추거나 뺀다. X 파일에 인용이 없는 새 사실은 쓰지 않는다 (ER-01 이 주소로 잰다).
- 원본을 바꾸면 대응 문서 페이지도 같이 맞춘다 (레포 `.claude/skills/docs-site/SKILL.md`). 공통 CSS 링크 하나, 320 · 375 · 1280 넘침 0 (AR-03).
- 기준 판(이하 BASE): `e500a63` (가지 `chore/ak3-ex2` 를 만든 시점). 끝 판(이하 TIP): 모든 커밋이 끝난 뒤 `git rev-parse chore/ak3-ex2` 의 출력. `HEAD` 를 쓰지 않는다.
- 모든 측정은 작업 폴더 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-ex2` 를 현재 폴더로 두고 돌린다. 글로빙을 쓰지 않아 zsh · bash 결과가 같다. `S` 는 세션 scratch 아래 새 폴더다.

## GAP 분석

| 항목 | X 파일 판정 요지 | 저장소 자리 (BASE 에서 연 줄) | 결과 | 조건 |
| --- | --- | --- | --- | --- |
| X1 | 「Android 16 에 later this year 들어온다」 가 원문. `Android 16과 함께 발표` 원문에 없음 · `Android 16+ 기본 UI 에 적용` 틀림 · `앱 개발자가 채택하는 것은 선택사항` 원문에 없음 · 표의 `(Android 16)` · 페이지 `(2025, Android 16)` 은 맞지만 모호 · 출처가 블로그 첫 화면 | `design-kit/docs/design/systems/material-design.md:27,257,280,285` · `docs/design-kit/material-design.html:256` | 계약에 넣음 | SK-01 · SK-02 · SK-03 |
| X1 | 레포 전체에서 같은 주장 | `git grep 'Android 16'` — 위 두 파일 밖은 `docs/flutter/research-log.md:298` 의 `Android 16KB 메모리 페이지` 하나(다른 사실) | 이미 됨 (다른 주장) | SK-03 |
| X2 | Firebase 문서는 APNs authentication key 업로드만 지시하고 `.p8` 을 적지 않는다 · `.p8` 확장자는 Apple 토큰 방식 문서가 명시 · Apple 은 `.p12` 인증서 방식을 지금도 절차로 문서화 · 「권장」 · 「deprecated」 는 원문에 없음 | `onboarding-kit/skills/setup-guide/evals/evals.json:67~83` (`deprecation-claim-fidelity`) | 계약에 넣음 | SK-04 |
| X2 | Firebase 갱신일을 `2026-09-17` 이라 적었다 | 같은 파일 69 행 `Last updated 2026-09-24 UTC` | 이미 됨 — 2026-09-28 12:4x `curl -sL https://firebase.google.com/docs/cloud-messaging/ios/get-started \| grep -oE 'Last updated [0-9-]+ UTC'` 출력이 `Last updated 2026-09-24 UTC` 라 X2 의 값을 따르지 않는다 | SK-04 |
| X3 | etc_seq=663 첨부 PDF 가 뒷받침하는 것은 보도자료의 `-다` 종결 권고(55쪽) · 한글 우선과 어렵거나 불필요한 외래어 다듬기(63 · 64쪽)뿐. K-01 · K-02 · K-03 · K-06 ~ K-11 원문에 없음, K-04 · K-05 는 범위가 넓게 옮겨져 틀림 | `docs/tone/korean-technical-writing.md:52,132,134,189,219,325` · `docs/tone/overview.md:171` · `tone-kit/references/locale-korean.md:62,79,90,188` · `tone-kit/references/sources.md:84` · 페이지 넷 | 계약에 넣음 | SK-05 ~ SK-10 |
| R | `(_, __)` 는 Dart 3.7 부터 `(_, _)` 로 (A11 이 tone 예시에 적용한 방식) | `docs/flutter/architecture/routing.md:85,86,88,120` · 대응 페이지 `docs/flutter-toolkit/routing.html` 에는 이 코드가 없다 (`grep -cE '[(,] ?__[,)]'` 0) | 원본은 계약에 넣음 · 페이지는 이미 됨 | SK-11 |
| A11 C-06 | `ex/A11.md` A 절: C-06 의 MUST 는 Effective Dart 의 `PREFER writing doc comments for public APIs` 보다 세다. 앞 묶음이 `06c1b7d` · `47e07fa` 에서 SHOULD 로 내렸다 | 옛 값 전체 검색 `git grep -n -E '(원칙 ?6\|C-06).{0,40}MUST' -- ':!.harness' ':!docs/tone/research-log.md'` 이 BASE 에서 1 — `docs/tone-kit/comment-economy.html:923` 의 `<span class="tag">원칙 6은 MUST</span>` (원본 `docs/tone/comment-economy.md` 원칙 6 은 이미 `**강도:** SHOULD`) | 남은 한 자리를 계약에 넣음 · 나머지는 이미 됨 | SK-12 · AR-03 |

X3 규칙별 판정 (강도 규칙: `tone-kit/references/core-antipatterns.md:47` 「`MUST` (예외 없음) / `SHOULD` (명시 예외 존재) / `관측 컨벤션` (공개 근거 없음, 국지 실측만 존재)」 와 `docs/tone/korean-technical-writing.md` 규칙 강도 절 「SHOULD = 공개 1차 근거가 있는 규칙 · MUST = 킷 구조를 결정하는 규칙」):

| 규칙 | 663 을 근거로 든 자리 (BASE) | 원문 판정 | 조치 | 남는 근거 | 강도 전 → 후 |
| --- | --- | --- | --- | --- | --- |
| K-01 · K-09 (원칙 1) | 원칙 1 출처 줄 · 페이지 p1 | 원문에 없음 | 인용 뺌 | 킷 구조 결정 · 원본 프로젝트 전수 감사 | MUST → MUST (킷 구조 규칙이라 공개 근거와 무관) |
| K-02 (원칙 2 · overview 9) | 원칙 2 강도 괄호 · 출처 줄 · 페이지 p2 · overview 9 절 · overview 페이지 | 원문에 없음 | 인용 뺌, 강도 괄호에서 「국립국어원·」 뺌. 치환표는 이 킷이 정한 검사 규칙이라고 밝힘 | 한국어 번역투 연구(KCI) · Effective Dart (overview 9) | SHOULD → SHOULD (공개 근거가 남는다) |
| K-03 (원칙 3) | 없음 | 원문에 없음 | 할 일 없음 | LINE · Google Engineering Practices | SHOULD → SHOULD |
| K-04 (원칙 4) | 없음 | 틀림 (보도자료 권고를 코드 doc 규칙으로 넓힘) | 55쪽 `-다` 권고를 참고로만 적고 「근거로 세지 않는다」 고 밝힘 | 프로젝트 실측 | 관측 컨벤션 → 관측 컨벤션 |
| K-05 (원칙 5) | 원칙 5 출처 줄 · 페이지 p5 | 일부 (2번 원칙만) | 인용은 남기되 63 · 64쪽 · 2번 원칙으로 좁히고, 1번 · 3번은 이 킷의 컨벤션이라고 밝힘 | Effective Dart · 663 일부 | SHOULD → SHOULD |
| K-06 · K-07 · K-10 · K-11 | 없음 | 원문에 없음 | 할 일 없음 | 각자 출처 그대로 | 그대로 |
| K-08 (원칙 8) | 원칙 8 출처 줄 · 페이지 p8 | 원문에 없음 | 인용 뺌 | 프로젝트 실측 | 관측 컨벤션 → 관측 컨벤션 |

강도가 바뀌는 규칙은 없다. 인용을 뺀 뒤에도 각 규칙의 강도가 강도 규칙의 정의와 맞는다 (MUST 는 구조 규칙, SHOULD 는 공개 근거가 남음, 관측 컨벤션은 실측만).

## 범위 경계

- 하지 않는 것: `.harness/` 아래 봉인된 계약 · QA 리포트 · 개정 파일, `.harness/.meta` 기록, `docs/tone/research-log.md:43` 의 「원칙 1 · 2 · 5 · 8 이 663 을 근거로 드는 문제는 다음 사이클」 줄 — 역사 기록이라 고치지 않는다.
- 하지 않는 것: `.claude/skills/kaizen-orchestrator/references/phase-research-templates.md:270` 과 `docs/process/phase-research-templates.html` 의 663 행 — 이미 「코드 주석 문체 근거로는 약하다」 고 적어 X3 판정과 어긋나지 않는다.
- 하지 않는 것: X 파일이 「추론」 으로 낸 문장 중 인용 없는 것(예: X1 의 「색상·형태·모션 등을 확장한」 표 칸 전체 교체) — 표 칸은 괄호 한 곳만 고친다. X2 의 `Last updated 2026-09-17 UTC` 는 위 GAP 표대로 따르지 않는다.
- 앞 묶음 계약 `sprint-contract-after-0928-external-facts.md` 는 `status: done` 이다. 그 계약의 SK-14 가 재던 `"apns_certificate_p12": "not_mentioned"` 키 이름이 이번에 바뀐다 — 끝난 계약이라 봉인과 판정에는 영향이 없다.
- 교차 진단 반영 (2026-09-28): remaining.md A11 은 세 가지(C-06 강도 · 663 이름표 · `__` 예시)다. C-06 과 이름표는 앞 묶음이 했고, 옛 값 전체 검색에서 남은 C-06 한 자리를 SK-12 로 넣었다. `docs/tone/research-log.md:44` 의 「C-06 은 MUST 인데」 는 그 사이클의 기록이라 고치지 않는다.
- 교차 진단 반영: AR-01 의 서명 줄은 이 묶음 공통 전제가 정한 줄이다. 구현도 같은 세션 모델(Opus 5.5)이 하므로 모델이 바뀌어 헛 FAIL 이 나는 일은 없다. 다른 모델이 이어 받으면 그 세션은 이 줄로 서명한다.
- 커버리지 해소: AR-02 — 검출기가 짚은 `.harness/` 는 제외 경로, `CF=…` 는 측정 변수 정의라 대상이 아니다.
- 커버리지 해소: SK-12 — 검출기가 짚은 `docs/tone/research-log.md` · `.harness` 는 측정이 일부러 빼는 경로(역사 기록 · 계약 폴더)라 대상이 아니다.
- 조건 수: 기능 조건 18 개 (가이드 「복잡」 9 ~ 20 안).
- 오라클 해소: SK-01 · SK-05 · SK-06 · SK-07 · SK-08 · SK-09 — 이 스프린트의 산출물이 문서 문장 자체라 글자 대조가 곧 결과 관찰이다. 조건마다 BASE 값(양성 대조)을 적어 구현을 빼면 FAIL 함을 보였다. SC-01 · ER-01 · AR-02 · AR-03 — 측정이 명령을 실제로 돌려 종료 코드와 출력으로 판정한다 (검출기 오탐).
- 범위 목록 (이 밖의 경로를 담은 커밋은 막힌다):

```text
# sprint-scope
design-kit/docs/design/systems/material-design.md
docs/design-kit/material-design.html
onboarding-kit/skills/setup-guide/evals/evals.json
tone-kit/references/locale-korean.md
tone-kit/references/sources.md
docs/tone/korean-technical-writing.md
docs/tone/overview.md
docs/tone-kit/korean-technical-writing.html
docs/tone-kit/locale-korean.html
docs/tone-kit/overview.html
docs/tone-kit/sources.html
docs/flutter/architecture/routing.md
docs/tone-kit/comment-economy.html
```

## 회귀 게이트

- BASE 실측(2026-09-28): `ci-local.sh` 25 단계 rc=0 · `feedback-agg-test SKIP (yq 없음)` 1 줄. CI 파일에만 있는 여섯 단계(`check-api-kit-docs` · `detect-docs-drift --check-table` · `check-cause-table-copies` · `measure-helpers-test` · `bambu-kit/evals/run-gate-fixtures.sh` · `bambu-kit/evals/makerworld-fetch-test.sh`) 전부 rc=0.
- BASE 실측: 범위 목록의 md 6 파일 markdownlint-cli2 0.23.2 (`{ "config": { "MD013": false } }`) 경고 전부 0. 양성 대조: `docs/flutter/architecture/routing.md` 사본 끝에 `#bad heading` · 빈 줄 셋 · 줄 끝 공백을 붙이면 4, 종료 코드 1.
- BASE 실측: 페이지 5 개 공통 CSS 링크 각 1, `node scripts/check-docs-a11y.js <5 파일>` → `5/5 PASS`, rc=0. 교차 진단 반영 뒤 `docs/tone-kit/comment-economy.html` 을 더한 6 개도 CSS 링크 각 1, `6/6 PASS` (2026-09-28 실측). 양성 대조: `docs/tone-kit/overview.html` 사본의 `<body>` 바로 뒤에 너비 2000px 요소를 넣으면 `FAIL … of=1680/1625/1232/720`, rc=1 (사본은 지웠다).

## Skill

- [ ] SK-01: (X1) `design-kit/docs/design/systems/material-design.md` 의 Android 16 문장이 원문 표현으로 낮춰지고 구체 출처가 붙었다 — 원문보다 센 세 말과 블로그 첫 화면 출처가 0 번, 원문 인용 `later this year` · 두 블로그 글 주소 · 조회일 `2026-09-28` 이 1 번 이상, 버전 표 M3 Expressive 행에 `후속 업데이트` 가 1 번 나온다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: `m=design-kit/docs/design/systems/material-design.md` 로 두고, 낱말마다 `grep -cF -- '<낱말>' $m`. 0 이어야 하는 것: `Android 16과 함께 발표` · `Android 16+ 기본 UI` · `앱 개발자가 채택하는 것은 선택사항` · `(https://android-developers.googleblog.com/)`. 1 이상이어야 하는 것: `later this year` · `https://android-developers.googleblog.com/2025/05/the-android-show-io-edition.html` · `https://android-developers.googleblog.com/2025/06/android-16-is-here.html` · `2026-09-28`. 표 행: `grep -F '| M3 Expressive | 2025 |' $m | grep -cF '후속 업데이트'` 이 1.
  양성 대조: BASE 에서 0 이어야 하는 네 낱말이 각 1, 1 이상이어야 하는 네 낱말이 각 0, 표 행 값 0 (2026-09-28 실측).
  측정 대상: `design-kit/docs/design/systems/material-design.md`
- [ ] SK-02: (X1) 대응 페이지 `docs/design-kit/material-design.html` 의 6 절 머리가 `Android 16 후속 업데이트` 로 바뀌고, 원문 인용과 두 블로그 글 주소 · 조회일을 담는다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: `h=docs/design-kit/material-design.html` 로 두고, `grep -cF '(2025, Android 16)' $h` 이 0. `grep -cF '6 · M3 Expressive (2025, Android 16 후속 업데이트)' $h` 이 1. `grep -cF -- '<낱말>' $h` 이 `later this year` · `https://android-developers.googleblog.com/2025/05/the-android-show-io-edition.html` · `https://android-developers.googleblog.com/2025/06/android-16-is-here.html` · `2026-09-28` 각 1 이상.
  양성 대조: BASE 에서 `(2025, Android 16)` 1, 나머지 다섯 값 모두 0.
  측정 대상: `docs/design-kit/material-design.html`
- [ ] SK-03: (X1) 레포 전체(`.harness` 제외)에 원문보다 센 Android 16 표현이 남지 않았다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: `git grep -n -E 'Android 16과 함께|Android 16\+|\(2025, Android 16\)' -- ':!.harness' | grep -c .` 이 0. 이어서 `git grep -l -E 'Android 16([^K]|$)' -- ':!.harness' | sort` 출력이 정확히 `design-kit/docs/design/systems/material-design.md` · `docs/design-kit/material-design.html` 두 줄.
  양성 대조: BASE 에서 첫 측정 3 (material-design.md 257 · 280, material-design.html 256). 두 번째 측정은 BASE 에서도 같은 두 줄이다 — `Android 16KB` 를 뺀 것이 맞게 걸러지는지 보는 확인이다.
- [ ] SK-04: (X2) `onboarding-kit/skills/setup-guide/evals/evals.json` 의 `deprecation-claim-fidelity` 사례에서 출처 · 출처 상태 · 판정 줄 · 설명이 서로 맞는다 — 출처 상태가 Firebase 와 Apple 로 나뉘고, 출처 칸이 세 주소와 조회일을 담고, `.p8` 판정 줄은 Apple 을 근거로 들고, 업로드 판정 줄은 Firebase 원문대로 `APNs 인증 키` 만 요구하고, `.p12` 판정 줄과 설명은 Apple 이 인증서 방식을 문서화한다는 사실과 맞는다. 파일은 JSON 으로 읽히고 평가 두 단계가 통과한다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: `e=onboarding-kit/skills/setup-guide/evals/evals.json` 로 두고, 아래 들여쓴 줄을 들여쓰기를 뺀 채 `$S/x2check.py` 로 저장하고 `python3 $S/x2check.py $e` 의 출력이 정확히 `OK` 한 줄이며 종료 코드 0. 이어서 `python3 -c "import json,sys; json.load(open(sys.argv[1]))" $e` · `sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh` · `python3 scripts/sync-evals.py --check-only` 종료 코드 각 0.
    import json, sys
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    c = [x for x in d["cases"] if x["id"] == "deprecation-claim-fidelity"]
    bad = []
    if len(c) != 1: print("BAD case count", len(c)); sys.exit(0)
    c = c[0]
    want = {"apns_auth_key": "documented", "apns_auth_key_p8_in_firebase_source": "not_mentioned", "apns_auth_key_p8_in_apple_source": "documented", "apns_certificate_p12_in_firebase_source": "not_mentioned", "apns_certificate_p12_in_apple_source": "documented", "instance_id_api": "deprecated"}
    if c["setup"]["fetched_source_states"] != want: bad.append("states")
    src = c["source"]
    for u in ["https://firebase.google.com/docs/cloud-messaging/ios/get-started (2026-09-28 조회 · Last updated 2026-09-24 UTC)", "https://developer.apple.com/documentation/usernotifications/establishing-a-token-based-connection-to-apns (2026-09-28 조회)", "https://developer.apple.com/help/account/capabilities/communicate-with-apns-using-a-tls-certificate (2026-09-28 조회)"]:
        if u not in src: bad.append("source:" + u.split(" ")[0])
    a = c["assertions"]
    if not (a[0].startswith("guide_includes('.p8')") and "Apple" in a[0]): bad.append("a0")
    if a[1] != "guide_instructs_upload('APNs 인증 키') == true": bad.append("a1")
    p12 = [x for x in a if x.startswith("guide_does_not_claim_deprecated('.p12')")]
    if len(p12) != 1 or "Apple" not in p12[0]: bad.append("a_p12")
    if "언급이 없는 .p12" in c["description"] or "Apple" not in c["description"]: bad.append("desc")
    for b in bad: print("BAD", b)
    if not bad: print("OK")
  알려진 답: 기대 모양만 담은 작은 JSON 에 돌리면 `OK` 한 줄, 그 JSON 에서 `apns_certificate_p12_in_apple_source` 값을 `not_mentioned` 로 바꾸면 `BAD states` 한 줄, 여는 괄호 하나뿐인 파일이면 출력 없이 종료 코드 1 (2026-09-28 실측 일치).
  양성 대조: BASE 에 돌리면 `BAD states` · `BAD source:https://developer.apple.com/documentation/usernotifications/establishing-a-token-based-connection-to-apns` · `BAD source:https://developer.apple.com/help/account/capabilities/communicate-with-apns-using-a-tls-certificate` · `BAD a0` · `BAD a1` · `BAD a_p12` · `BAD desc` 일곱 줄 (Firebase 출처 줄은 BASE 에서 이미 맞다).
  음성 대조: 구현 뒤 evals.json 끝의 `}` 하나를 지운 임시 사본에 JSON 명령을 돌리면 종료 코드 1 이다.
  측정 대상: `onboarding-kit/skills/setup-guide/evals/evals.json` · `.p8` · `.p12`
- [ ] SK-05: (X3) `docs/tone/korean-technical-writing.md` 가 663 자료를 원문이 뒷받침하는 원칙에만 인용하고, 원칙별 강도는 그대로다 [exact, enumerated]
  Given: 모든 커밋 뒤. 원칙 N 절 자르기: `awk -v N=<N> '/^### /{p=(index($(0), "### " N ".")==1)} p' $k`.
  측정: `k=docs/tone/korean-technical-writing.md` 로 두고, 절마다 `| grep -cF 'etc_seq=663'` 이 원칙 1 → 0 · 원칙 2 → 0 · 원칙 4 → 1 · 원칙 5 → 1 · 원칙 8 → 0. 원칙 4 절 `| grep -cF '근거로 세지 않는다'` 1. 원칙 5 절 `| grep -cF '2번 원칙'` 1 이상. `grep -cF '국립국어원·번역투 연구 근거' $k` 0. 강도 목록 `grep -E '^\*\*강도: ' $k | sed -E 's/^\*\*강도: ([^*]+)\*\*.*/\1/' | tr '\n' ','` 이 정확히 `MUST,SHOULD,SHOULD,관측 컨벤션,SHOULD,SHOULD,관측 컨벤션,관측 컨벤션,관측 컨벤션,`.
  양성 대조: BASE 에서 절별 663 값이 1 · 1 · 0 · 1 · 1, `근거로 세지 않는다` 0, `2번 원칙` 0, `국립국어원·번역투 연구 근거` 1. 강도 목록은 BASE 와 같다 (2026-09-28 실측).
  측정 대상: `docs/tone/korean-technical-writing.md`
- [ ] SK-06: (X3) 대응 페이지 `docs/tone-kit/korean-technical-writing.html` 이 SK-05 와 같은 인용 배치와 강도를 가진다 [exact, enumerated]
  Given: 모든 커밋 뒤. 원칙 N 카드 자르기: `awk -v N=<N> '/<article class="card" id="p[0-9]+">/{p=(index($(0), "id=\"p" N "\"")>0)} p' $h`.
  측정: `h=docs/tone-kit/korean-technical-writing.html` 로 두고, 카드마다 `| grep -cF 'etc_seq=663'` 이 p1 → 0 · p2 → 0 · p4 → 1 · p5 → 1 · p8 → 0. p4 카드 `| grep -cF '근거로 세지 않는다'` 1. p5 카드 `| grep -cF '2번 원칙'` 1 이상. `grep -cF '국립국어원·번역투 연구 근거' $h` 0. 강도 목록 `grep -oE '<p class="caption"><strong>강도: [^<]+</strong>' $h | sed -E 's/.*강도: //; s/<.*//' | tr '\n' ','` 이 정확히 `MUST,SHOULD,SHOULD,관측 컨벤션,SHOULD,SHOULD,관측 컨벤션,관측 컨벤션,관측 컨벤션,`.
  양성 대조: BASE 에서 카드별 663 값이 1 · 1 · 0 · 1 · 1, `근거로 세지 않는다` 0, `2번 원칙` 0, `국립국어원·번역투 연구 근거` 1.
  측정 대상: `docs/tone-kit/korean-technical-writing.html`
- [ ] SK-07: (X3) `tone-kit/references/locale-korean.md` 가 663 자료의 범위를 밝힌다 — §2 에 치환표가 그 자료의 항목이 아니라는 문장, §3 에 보도자료 `-다` 권고와 이 킷의 컨벤션이라는 문장, §4 에 한글 우선 · 외래어 다듬기와 이 킷의 컨벤션이라는 문장, §10 의 663 줄에 적용 범위와 확인일이 있고, 규칙표 강도는 그대로다 [exact, enumerated]
  Given: 모든 커밋 뒤. 절 자르기: `awk -v N=<N> '/^## /{p=(index($(0), "## " N ".")==1)} p' $l`.
  측정: `l=tone-kit/references/locale-korean.md` 로 두고, §2 절 `| grep -cF '국립국어원 자료의 항목을 옮긴 것이 아니라'` 1. §3 절 `| grep -cF '보도자료 본문에'` 1 이상 · `| grep -cF '이 킷의 컨벤션'` 1 이상. §4 절 `| grep -cF '어렵거나 불필요한 외래어'` 1 이상 · `| grep -cF '이 킷의 컨벤션'` 1 이상. `grep -F 'etc_seq=663' $l | grep -cF 'K-05 2번 원칙'` 1 · `grep -F 'etc_seq=663' $l | grep -cF '2026-09-28'` 1. 규칙표 강도 `grep -E '^\| K-[0-9]{2} \|' $l | awk -F'|' '{print $(NF-1)}' | tr -d ' ' | tr '\n' ','` 이 정확히 `MUST,SHOULD,SHOULD,관측컨벤션,SHOULD,SHOULD,관측컨벤션,관측컨벤션,MUST,MUST,관측컨벤션,`.
  양성 대조: BASE 에서 §2 · §3 · §4 · §10 의 여섯 값이 모두 0 이고 규칙표 강도는 같은 목록이다.
  측정 대상: `tone-kit/references/locale-korean.md`
- [ ] SK-08: (X3) 대응 페이지 `docs/tone-kit/locale-korean.html` 이 SK-07 의 네 문장을 같은 절에 담는다 [exact, enumerated]
  Given: 모든 커밋 뒤. 절 자르기: `awk -v I=<id> '/<section class="section[^"]*" id="/{p=(index($(0), "id=\"" I "\"")>0)} p' $h` — `s4` 는 §2, `s5` 는 §3, `s6` 은 §4, `s12` 는 §10 이다.
  측정: `h=docs/tone-kit/locale-korean.html` 로 두고, `s4` `| grep -cF '국립국어원 자료의 항목을 옮긴 것이 아니라'` 1. `s5` `| grep -cF '보도자료 본문에'` 1 이상 · `| grep -cF '이 킷의 컨벤션'` 1 이상. `s6` `| grep -cF '어렵거나 불필요한 외래어'` 1 이상 · `| grep -cF '이 킷의 컨벤션'` 1 이상. `s12` `| grep -F 'etc_seq=663' | grep -cF 'K-05 2번 원칙'` 1. `grep -cF '원본에 적힌 주소 9 개' $h` 1 (주소 모음 수가 그대로다).
  양성 대조: BASE 에서 앞의 여섯 값이 모두 0, 주소 모음 문구 1.
  측정 대상: `docs/tone-kit/locale-korean.html`
- [ ] SK-09: (X3) `tone-kit/references/sources.md` 와 대응 페이지 `docs/tone-kit/sources.html` 의 663 행 상태가 첨부 PDF 본문 확인 결과로 바뀌었다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: `grep -F 'etc_seq=663' tone-kit/references/sources.md | grep -cF '<낱말>'` 이 `본문 PDF 는 미확인` 0 · `첨부 PDF 본문 확인` 1 · `이 자료에 없고` 1. 페이지는 행 머리 다음 두 줄을 본다: `grep -A2 -F '국립국어원 「유형별로 알아보는 보도자료 작성 길잡이」</div></td>' docs/tone-kit/sources.html | grep -cF '<낱말>'` 이 같은 세 낱말에 0 · 1 · 1.
  양성 대조: BASE 에서 두 파일 모두 `본문 PDF 는 미확인` 1, 나머지 둘 0.
  측정 대상: `tone-kit/references/sources.md` · `docs/tone-kit/sources.html`
- [ ] SK-10: (X3) `docs/tone/overview.md` 9 절과 대응 페이지 `docs/tone-kit/overview.html` 이 663 인용을 빼고 Effective Dart 출처와 강도 SHOULD 는 남긴다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: `grep -cF 'etc_seq=663' docs/tone/overview.md` 0 · `grep -cF 'etc_seq=663' docs/tone-kit/overview.html` 0. `awk '/^### /{p=(index($(0), "### 9.")==1)} p' docs/tone/overview.md | grep -cF '**강도** SHOULD · **출처** [Effective Dart: Documentation](https://dart.dev/effective-dart/documentation)'` 1. `grep -F '<span class="sources-title">출처</span>' docs/tone-kit/overview.html | grep -cF 'https://dart.dev/effective-dart/documentation">Effective Dart: Documentation</a></div>'` 1 이상.
  양성 대조: BASE 에서 663 은 두 파일 각 1, 9 절 줄 측정 0 (앞에 663 링크가 끼어 있다).
  측정 대상: `docs/tone/overview.md` · `docs/tone-kit/overview.html`
- [ ] SK-11: (R) `docs/flutter/architecture/routing.md` 예시의 밑줄 두 개 매개변수 넷이 와일드카드 `_` 로 바뀌었고, 레포 문서(`.harness` 제외)에 같은 모양이 남지 않았다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: `r=docs/flutter/architecture/routing.md` 로 두고, `git grep -n -E '[(,] ?__[,)]' -- '*.md' '*.html' ':!.harness' | grep -c .` 이 0. `grep -cF -- '<줄>' $r` 이 `builder: (_, _) => const HomeScreen()` · `builder: (_, _) => const LoginPage()` · `builder: (_, _, child) => MainShell(child: child)` · `transitionsBuilder: (_, animation, _, child) =>` 각 1. 대응 페이지 `docs/flutter-toolkit/routing.html` 은 `grep -cE '[(,] ?__[,)]'` 0 이고 이 스프린트에서 바뀌지 않는다 (AR-02 범위 목록 밖).
  양성 대조: BASE 에서 첫 측정 4 (routing.md 85 · 86 · 88 · 120), 네 줄은 각 0.

  측정 대상: `docs/flutter/architecture/routing.md` · `.harness`
- [ ] SK-12: (A11 C-06) 레포(`.harness` · `docs/tone/research-log.md` 제외)에 C-06 · 원칙 6 을 MUST 로 적은 옛 값이 남지 않았고, `docs/tone-kit/comment-economy.html` 출처 목록의 원칙 6 표지가 원본 강도 SHOULD 와 같다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: `git grep -n -E '(원칙 ?6|C-06).{0,40}MUST' -- ':!.harness' ':!docs/tone/research-log.md' | grep -c .` 이 0. `grep -cF '<span class="tag">원칙 6은 SHOULD</span>' docs/tone-kit/comment-economy.html` 이 1. 원본 강도 확인: `awk '/^### /{p=(index($(0), "### 6.")==1)} p' docs/tone/comment-economy.md | grep -cF '**강도:** SHOULD'` 이 1.
  양성 대조: BASE 에서 첫 측정 1 (`docs/tone-kit/comment-economy.html:923`), 둘째 0, 셋째 1 (2026-09-28 실측).
  측정 대상: `docs/tone-kit/comment-economy.html` · `docs/tone/comment-economy.md`
## Script

- [ ] SC-01: 로컬 CI 와 CI 파일에만 있는 여섯 단계가 모두 통과한다 [exact, enumerated]
  Given: 모든 커밋 뒤, `TMPDIR` 을 세션 scratch 아래 새 폴더로 두고.
  측정: `TMPDIR=<scratch 폴더> bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-ex2` 뒤 `<scratch 폴더>/ci-local/summary.txt` 에서 `grep -c 'rc=0'` 이 25, `grep -v 'rc=0'` 출력이 `feedback-agg-test SKIP (yq 없음)` 한 줄뿐. 이어서 여섯 명령 각각 종료 코드 0: `python3 scripts/check-api-kit-docs.py` · `python3 scripts/detect-docs-drift.py --check-table` · `python3 scripts/check-cause-table-copies.py` · `bash harness/evals/measure/measure-helpers-test.sh` · `bash bambu-kit/evals/run-gate-fixtures.sh` · `bash bambu-kit/evals/makerworld-fetch-test.sh`.
  음성 대조: 판정 근거는 단계마다의 종료 코드다. SK-04 의 JSON 사본처럼 단계가 읽는 입력을 깨면 그 단계가 rc≠0 을 낸다. BASE 값은 회귀 게이트 절.

## Error

- [ ] ER-01: 이번 스프린트가 더한 줄의 주소는 모두 BASE 레포에 이미 있거나 X 파일에 인용된 것이다 — 인용 없는 새 출처가 0 개다 [exact, enumerated]
  Given: 모든 커밋 뒤. `TIP=$(git rev-parse chore/ak3-ex2)`, `X=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/.harness/.meta/after-kaizen-0928/ex`.
  측정: 바로 아래 들여쓴 다섯 줄을 들여쓰기를 뺀 채 `$S/newurls.sh` 로 저장하고 `bash $S/newurls.sh "$PWD" e500a63 "$TIP" "$X" | grep -c .` 이 0 이며 `bash $S/newurls.sh …` 종료 코드 0.
    #!/bin/bash
    R="${1}"; B="${2}"; T="${3}"; X="${4}"
    url() { grep -oE 'https?://[^][ <>"`)(|]+' | sed -E "s/(&[a-z]+;)+\$//; s/[.,;:'」》]+\$//" | sort -u; }
    known=$( { git -C "$R" grep -h -I -E 'https?://' "$B" -- . | url; cat "$X"/X*.md | url; } | sort -u)
    git -C "$R" diff -U0 "$B" "$T" -- . ':(exclude).harness' | grep -E '^\+[^+]' | url | comm -23 - <(printf '%s\n' "$known")
  알려진 답: 새 임시 저장소에 기준 판(`https://a.example.com/x.`)과 끝 판(그 주소 · X 사본의 `https://ex.example.com/y` · 새 `https://z.example.com/new` · `.harness/` 아래 `https://h.example.com/`)을 두면 출력은 `https://z.example.com/new` 한 줄, 종료 코드 0 (2026-09-28 실측 일치).
  음성 대조: 구현 뒤 문서 한 곳에 `https://z.example.com/new` 를 더한 떠 있는 커밋(가지는 안 옮김)에 돌리면 1 이 나온다.
- [ ] ER-02: 이번 스프린트가 더한 줄에 번역투 킬러 패턴(tone-kit `locale-korean.md` §8 G-1)이 0 건이다 [exact, enumerated]
  Given: 모든 커밋 뒤. `TIP=$(git rev-parse chore/ak3-ex2)`.
  측정: `git diff -U0 e500a63 $TIP -- . ':(exclude).harness' | grep -E '^\+[^+]' | grep -cE '(을|를) ?(처리|관리)(합니다|한다)|에 대해서?|하도록 (합니다|한다)|에 의(해|하여)|되어 있(는 경우|을 때)|(표시|적용|호출|생성|반환)(됩니다|된다)'` 이 0.
  양성 대조: 같은 정규식에 `printf '+값을 처리합니다\n+서버에 의해 적용됩니다\n'` 을 넣으면 2 (2026-09-28 실측).

## Architecture

- [ ] AR-01: BASE 뒤 가지 `chore/ak3-ex2` 의 모든 커밋이 맨 위 폴더 하나만 건드리고, 메시지 마지막 줄이 서명 줄이다 [exact, enumerated]
  Given: 모든 커밋 뒤. `TIP=$(git rev-parse chore/ak3-ex2)`.
  측정: `for c in $(git rev-list e500a63..$TIP); do n=$(git show --name-only --format='' $c | cut -d/ -f1 | sort -u | grep -c .); s=$(git log -1 --format=%B $c | sed '/^[[:space:]]*$/d' | tail -1); [ "$n" = 1 ] && [ "$s" = 'Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>' ] || echo "BAD $c n=$n"; done | grep -c BAD` 이 0. `git rev-list e500a63..$TIP | grep -c .` 이 1 이상.
  양성 대조: 같은 폴더 세기를 `a5152c5` 에 돌리면 17 이다 (2026-09-28 실측).
- [ ] AR-02: BASE 에서 TIP 까지 바뀐 경로(`.harness/` 제외)가 전부 `## 범위 경계` 의 `# sprint-scope` 블록 안에 있다 [exact, enumerated]
  Given: 모든 커밋 뒤. `TIP=$(git rev-parse chore/ak3-ex2)`, `CF=.harness/sprint-contract-after-0928-external-facts-2.md`.
  측정: `comm -23 <(git diff --name-only e500a63 $TIP -- . ':(exclude).harness' | sort -u) <(awk '/^# sprint-scope$/{p=1;next} p&&/^```/{p=0} p' $CF | sort -u) | grep -c .` 이 0. 비교는 두 판의 직접 차이다 (`e500a63` 은 TIP 의 조상).
  양성 대조: 같은 `comm` 을 `git diff --name-only a5152c5~1 a5152c5` 에 돌리면 1 이상.
- [ ] AR-03: 바꾼 문서 페이지 6 개가 공통 CSS 링크를 하나씩 가지고 접근성 · 넘침 검사를 통과한다 — `docs/design-kit/material-design.html` · `docs/tone-kit/korean-technical-writing.html` · `docs/tone-kit/locale-korean.html` · `docs/tone-kit/overview.html` · `docs/tone-kit/sources.html` · `docs/tone-kit/comment-economy.html` [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: 6 파일 각각 `grep -c 'href="../assets/site.css"' <파일>` 이 1. `node scripts/check-docs-a11y.js docs/design-kit/material-design.html docs/tone-kit/korean-technical-writing.html docs/tone-kit/locale-korean.html docs/tone-kit/overview.html docs/tone-kit/sources.html docs/tone-kit/comment-economy.html` 이 종료 코드 0 이고 마지막 줄이 `6/6 PASS` (320 · 375 · 768 · 1280px 넘침 `> 2px` 이면 FAIL).
  양성 대조: 너비 2000px 요소를 넣은 사본은 `FAIL … of=1680/1625/1232/720`, 종료 코드 1 (2026-09-28 실측).

  측정 대상: `docs/design-kit/material-design.html` · `docs/tone-kit/korean-technical-writing.html` · `docs/tone-kit/locale-korean.html` · `docs/tone-kit/overview.html` · `docs/tone-kit/sources.html` · `docs/tone-kit/comment-economy.html`
## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가
  측정: `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0.
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL
  측정: `python3 scripts/validate-plugin.py --check=frontmatter` 종료 코드 0.

## Reusability

- [ ] RE-01: N/A (산출물이 문서 · 평가 데이터뿐 — 재사용 단위 코드가 없다. 측정: 범위 목록 12 경로의 확장자가 `.md` · `.html` · `.json` 뿐)
- [ ] RE-02: N/A (새 컴포넌트 · 함수를 만들지 않는다 — 기존 문장을 고칠 뿐이다. 측정: RE-01 과 같음)

## Diagnostics

- [ ] DG-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `git diff --name-only e500a63 $(git rev-parse chore/ak3-ex2) | grep -c '^scripts/release.sh$'` 이 0)
- [ ] DG-02: 바꾼 md 6 파일이 편집기와 같은 설정의 markdownlint 경고 0 개다 — 설정은 markdownlint-cli2 0.23.2 · `{ "config": { "MD013": false } }`
  Given: 모든 커밋 뒤. 도구가 없으면 scratch 새 폴더에서 `npm install --no-save markdownlint-cli2@0.23.2` 로 설치한다.
  측정: `design-kit/docs/design/systems/material-design.md` · `tone-kit/references/locale-korean.md` · `tone-kit/references/sources.md` · `docs/tone/korean-technical-writing.md` · `docs/tone/overview.md` · `docs/flutter/architecture/routing.md` 마다 `markdownlint-cli2 --config <설정 파일> <경로>` 출력에서 `^<경로>:[0-9]+` 줄 수가 0 이고 종료 코드 0.
  양성 대조: 회귀 게이트 절 — 나쁜 줄을 붙인 사본은 4, 종료 코드 1.
- [ ] DG-03: N/A (commands.test 는 scripts/release.sh 를 돌린다 — 이번 변경과 무관. 실제 시험은 SC-01 이 잰다)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 변경 파일이 문서 · 평가 데이터뿐. 페이지 실제 렌더는 AR-03 이 잰다)
