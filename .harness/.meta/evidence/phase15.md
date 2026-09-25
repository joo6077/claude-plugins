---
phase: 15
title: "Phase 15 tone-kit — 확보된 외부 근거"
collected: 2026-09-24
method: Claude 에이전트(WebFetch · WebSearch · curl) — Codex 사용 한도 소진, 사용자 지시 「코덱스 대신에 그냥 너가 알아서 진행하라고」(세션 기록 user 2026-09-24T11:54:58.940Z)
inputs: 처리 배정표(.claude/kaizen-input/insights-report.md)의 Phase 15 행 · phase-research-templates.md Phase 15 필수 출처 · 현행화 점검
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치를 지어내지 마라. 없으면 미반영으로 남긴다.
---

조회 수단: Claude(WebFetch·WebSearch·curl) — Codex 한도 소진으로 대체

# Phase 15 tone-kit 외부 근거 (2026-09-24 조회)

레포는 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/kaizen-0924` 를 읽기만 했다. 아래 파일:줄은 전부 이 워크트리 기준이다.
규칙 강도 이름은 킷 표기를 그대로 쓴다 — MUST(어기면 반려) · SHOULD(어기면 근거 요구) · 관측 컨벤션(프로젝트가 완화 가능).
Effective Dart 표기는 DO(반드시) · PREFER(되도록) · AVOID(피하라) · CONSIDER(검토하라) 로 읽는다.

## 1. 출처 목록

### 1-1. 본문을 실제로 읽은 것 (26건)

| # | 출처 | URL | 읽은 방법 |
|---|---|---|---|
| S1 | Droid (EMNLP 2025, 자연어처리 학회) 논문 페이지 | https://aclanthology.org/2025.emnlp-main.1593/ | WebFetch |
| S2 | SemEval-2026(국제 의미 평가 대회) Task 13 저장소 README | https://github.com/mbzuai-nlp/SemEval-2026-Task13 | WebFetch |
| S3 | Flutter 성능 모범 사례 | https://docs.flutter.dev/perf/best-practices | WebFetch |
| S4 | StatelessWidget 문서 | https://api.flutter.dev/flutter/widgets/StatelessWidget-class.html | WebFetch |
| S5 | Effective Dart: Style | https://dart.dev/effective-dart/style | WebFetch + curl |
| S6 | Effective Dart: Documentation | https://dart.dev/effective-dart/documentation | curl |
| S7 | Google Engineering Practices — What to look for | https://google.github.io/eng-practices/review/reviewer/looking-for.html | WebFetch |
| S8 | 국립국어원 자료 etc_seq=663 | https://korean.go.kr/front/etcData/etcDataView.do?etc_seq=663 | WebFetch + curl |
| S9 | LINE 기술 블로그 — 왜 개발자는 글을 못 쓸까? | https://engineering.linecorp.com/ko/blog/why-are-engineers-so-bad-at-writing/ | WebFetch |
| S10 | 한국어 어문 규범 — 한글 맞춤법 (제2항·제49항·제50항과 해설) | https://korean.go.kr/kornorms/regltn/regltnView.do?regltn_code=0001 | curl |
| S11 | 국립국어원 다듬은 말 목록 | https://www.korean.go.kr/front/imprv/refineList.do?mn_id=158 | curl |
| S12 | 국립국어원 온라인가나다 (보조 용언 띄어쓰기 답변) | https://m.korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&qna_seq=313449&pageIndex=1 | WebFetch |
| S13 | Microsoft Style Guide — Word choice 목차 | https://learn.microsoft.com/en-us/style-guide/word-choice/ | WebFetch |
| S14 | Microsoft Style Guide 공개 저장소 — Use technical terms carefully | https://github.com/MicrosoftDocs/microsoft-style-guide/blob/main/styleguide/word-choice/use-technical-terms-carefully.md | curl (raw) |
| S15 | Microsoft Style Guide 공개 저장소 — Don't use common words in new ways | https://github.com/MicrosoftDocs/microsoft-style-guide/blob/main/styleguide/word-choice/dont-use-common-words-in-new-ways.md | curl (raw, 해당 줄만) |
| S16 | Google 개발자 문서 스타일 가이드 — Jargon | https://developers.google.com/style/jargon | WebFetch |
| S17 | pub.dev 패키지 정보 (go_router · riverpod · flutter_riverpod · hooks_riverpod · flutter_hooks · freezed · flutter_lints · lints · material_ui · cupertino_ui) | https://pub.dev/api/packages/go_router (패키지 이름만 바꿔 10회) | curl |
| S18 | Flutter 릴리스 목록 | https://storage.googleapis.com/flutter_infra_release/releases/releases_macos.json | curl |
| S19 | Flutter 원본 `gesture_detector.dart` (3.38.4 · 3.47.5 태그) | https://raw.githubusercontent.com/flutter/flutter/3.47.5/packages/flutter/lib/src/widgets/gesture_detector.dart | curl |
| S20 | go_router CHANGELOG | https://raw.githubusercontent.com/flutter/packages/main/packages/go_router/CHANGELOG.md | curl |
| S21 | Dart 개발 도구 CHANGELOG | https://raw.githubusercontent.com/dart-lang/sdk/main/CHANGELOG.md | curl |
| S22 | Dart 언어 — Collections | https://dart.dev/language/collections | curl |
| S23 | 린트 규칙 `unnecessary_underscores` | https://dart.dev/tools/linter-rules/unnecessary_underscores | curl |
| S24 | 린트 규칙 `public_member_api_docs` | https://dart.dev/tools/linter-rules/public_member_api_docs | curl |
| S25 | pub.dev `material_ui` 패키지 페이지 | https://pub.dev/packages/material_ui | curl |
| S26 | Flutter 위키 스타일 가이드 (옮겨졌다는 안내) + 새 위치 | https://github.com/flutter/flutter/wiki/Style-guide-for-Flutter-repo · https://github.com/flutter/flutter/blob/main/docs/contributing/Style-guide-for-Flutter-repo.md | curl |

### 1-2. 접속만 확인한 것 (HTTP 200, 본문은 안 읽음)

- https://arxiv.org/abs/2507.10583 (Droid 논문 초고)
- https://semeval.github.io/SemEval2026/tasks.html
- https://aclanthology.org/2026.semeval-1.445/ (Task 13 개요 논문)
- https://www.kci.go.kr/kciportal/landing/article.kci?arti_id=ART002178732 (번역투 연구)
- https://microsoft.github.io/code-with-engineering-playbook/documentation/guidance/code/
- https://archive.eslint.org/docs/rules/no-nested-ternary · https://eslint.org/docs/latest/rules/no-nested-ternary
- https://riverpod.dev/ko/docs/concepts/about_code_generation · https://riverpod.dev/docs/whats_new
- https://pub.dev/packages/go_router/versions/16.3.0/example
- https://api.flutter.dev/flutter/material/Material/surfaceTintColor.html · https://api.flutter.dev/flutter/material/Divider/build.html · https://api.flutter.dev/flutter/cupertino/CupertinoActionSheet/CupertinoActionSheet.html
- https://github.com/flutter/flutter/blob/master/packages/flutter/lib/src/material/checkbox.dart (3.47.5 태그 경로도 200)

검색 결과 목록(WebSearch)은 찾는 용도로만 썼고 인용하지 않았다.

## 2. 항목별 관찰 사실

### 2-1. reflect-collector:P6 · F19 — K-11 "새 합성어를 만들지 않는다" (관측 컨벤션)

**영어권 문서 스타일 가이드는 "새 말을 만들지 마라"를 명시한다. 한국어 규범 쪽에는 그런 금지가 없고, 오히려 사전에 없는 전문 용어를 정당한 말로 다룬다.** 그래서 관측 컨벤션보다 높이 올릴 근거는 없고, "사전에 없는" 을 판정 기준으로 쓰는 문구는 반대 근거가 있다.

지지하는 근거

- Microsoft: "Don't create a new term if an existing one serves your purpose. If you must create a new term, verify that it isn't already being used to mean something else." / "When you must use technical terms for precise communication, define them in context." — S14. 같은 저장소의 다른 절에 "Don't create a new word from an existing word." — S15.
  - 주의: 공개 저장소 파일의 `ms.date` 는 01/19/2018 이다. 실제 Learn 페이지(S13, `updated_at` 2026-07-06)는 다른 비공개 저장소(`microsoft-style-guide-pr`)에서 만들어진다고 페이지 머리 정보에 적혀 있다. 하위 페이지 본문이 공개 저장소와 같은지는 확인하지 않았다. S13 목차에는 "Use technical terms carefully" · "Don't use common words in new ways" 가 지금도 있다.
- Google: 특정 집단만 아는 말(jargon)은 "Can you write around the term?" → "Can you replace the term with a different, more specific term?" 순서로 먼저 피하고, 꼭 써야 하면 처음 나올 때 괄호로 풀어 쓰거나 믿을 만한 정의에 연결하라고 한다. 페이지 갱신일 2025-06-25 — S16.
- Effective Dart 문서 주석 규칙 제목: "AVOID abbreviations and acronyms unless they are obvious" — S6. 추론: 독자가 모르는 줄임말을 피하라는 규칙이라, 독자가 모르는 새 합성어에도 같은 이유가 적용된다. 원문이 합성어를 직접 다루지는 않는다.
- 국립국어원 다듬은 말 목록(18,315건)의 최근 항목은 낯선 외국어를 풀어 쓴 구(句) 꼴이 많다 — "하이퍼 스케일러 → 대규모 데이터 센터 기업", "풀 스택 → 전 영역", "리밸런싱 → 자산 비중 재조정" — S11. 추론: K-11 문구의 "한국어 문장으로 풀어 쓴다" 방향과 맞는다.

반대하거나 조건을 다는 근거

- 한글 맞춤법 제50항: "전문 용어는 단어별로 띄어 씀을 원칙으로 하되, 붙여 쓸 수 있다." 해설: "국어사전에 모든 전문 용어를 실을 수는 없으므로, 국어사전에 실린 전문 용어와 유사한 전문 용어는 등재된 말에 준해 띄어쓰기를 할 수 있다." (예: 사전에 없는 '무릎 구부려 서기'도 '무릎구부려서기' 로 붙여 쓸 수 있다) — S10.
  - 즉 규범 기관은 **사전에 없다는 사실만으로 잘못된 말로 보지 않는다.** K-11 문구의 "사전에 없는 한국어 합성어" 를 판정 기준으로 읽으면, 정당한 전문 용어까지 걸리는 문제(문제가 없는데 잘못 잡는 것)가 생긴다.
- 같은 제50항 해설: 전문 용어는 "의미를 파악하기가 쉽지 않은 면이 있다. 이런 점을 고려하여 의미 파악이 쉽도록 띄어 쓰는 것을 원칙으로" 했다 — S10. 추론: 읽는 사람이 뜻을 쉽게 알아야 한다는 방향은 K-11 과 같다. 다만 규범은 "만들지 마라" 가 아니라 "띄어 써서 읽기 쉽게 하라" 를 택했다.
- 제2항 "문장의 각 단어는 띄어 씀을 원칙으로 한다." — S10. 추론: 사전에 없는 '표시훅' 은 규범대로라면 '표시 훅' 으로 띄어 쓴다. 합성어 문제의 일부는 띄어쓰기 문제이기도 하다.
- 국립국어원 스스로 새 표현을 만들어 보급한다(다듬은 말 목록 자체가 그 결과물) — S11. 추론: "새 말 만들기" 자체가 나쁜 것이 아니라, 글쓴이가 **정의 없이 혼자** 만든 이름이 문제다. Microsoft 도 "must create" 인 경우를 허용하고 확인 절차만 요구한다(S14).
- 온라인가나다에서 "사전에 없는 합성어는 띄어 쓴다" 를 직접 말한 답변은 찾지 못했다. 읽은 답변(S12)은 보조 용언 '심어 두다' 건이라 이 항목의 근거로 쓸 수 없다.

킷 안에서 겹치는 곳

- 예시 '표시훅' 의 '훅' 은 영어 hook 의 음역이다. 추론: 이미 `tone-kit/references/locale-korean.md:85` (§4-1 공식 이름은 영어 원문)과 `:87` (§4-3 음역 금지, K-05 SHOULD)에 걸릴 수 있다. K-11 과 K-05 가 같은 예시를 동시에 잡으면, 평가가 K-05(SHOULD)로 판정해도 틀린 것이 아니게 된다.
- "외래어 3원칙" 이라는 이름이 나오는 곳은 수집기가 적은 네 곳보다 많다: `locale-korean.md:34` · `:50` · `:83`, `docs/tone/korean-technical-writing.md:187` · `:313`, `docs/tone-kit/korean-technical-writing.html:306` · `:708` · `:710` · `:927` (grep 결과). 제목을 안 바꾸면 영향이 없지만, 거울 페이지 `html:306` 은 원칙과 강도를 나열한 표라서 K-11 을 넣으면 이 표도 같이 봐야 할 수 있다(추론).
- `tone-kit/evals/evals.json` 에는 지금 사례가 3건(id 1 tone-guide, 2 tone-scaffold, 3 tone-campaign)뿐이다. 새 사례는 id 4 가 된다.

### 2-2. 필수 출처 표 — 기존 규칙 강도가 출처 강도를 넘는지

| 킷 규칙 | 킷 강도 | 출처 원문 | 출처 강도 | 판정 |
|---|---|---|---|---|
| 위젯 분리 (추출 계열) | SHOULD (`docs/tone/research-log.md` 2026-08-31 행) | "Avoid overly large single widgets with a large `build()` function." / "To create reusable pieces of UIs, prefer using a `StatelessWidget` rather than a function." 갱신 2026-07-31 — S3 | Avoid · prefer | 넘지 않는다 |
| 헬퍼 대신 위젯 | SHOULD | "When trying to create a reusable piece of UI, prefer using a widget rather than a helper method." — S4 | prefer | 넘지 않는다 |
| C-01 why 만 남긴다 | SHOULD (`core-comment.md:14`) | "Usually comments are useful when they explain why some code exists, and should not be explaining what some code is doing." — S7 | Usually (단서 있음) | 넘지 않는다 |
| **C-06 공개 멤버는 doc 주석으로 계약을 쓴다** | **MUST** (`core-comment.md:19`, `docs/tone/comment-economy.md:235`) | 규칙 제목 "PREFER writing doc comments for public APIs" + 본문 "You don't have to document every single library, top-level variable, type, and member, but you should document most of them." — S6 | **PREFER** | **넘는다.** 아래 참조 |
| 네이밍 규약 | — | Effective Dart Style 제목 목록은 지난번과 같은 틀이다. 페이지 갱신 2026-08-12, Dart 3.13.3 기준. 새로 눈에 띄는 것은 "PREFER using wildcards for unused callback parameters" — S5 | PREFER | 킷 문서 예시가 이 규칙과 어긋난다(3절 표) |
| 탐지 문헌 (위치 설명용) | 규칙 근거로 쓰지 않음 (`sources.md:27`) | Droid: "most detectors are easily compromised by humanising the output distributions using superficial prompting and alignment approaches", "this problem can be easily amended by training on a small number of adversarial examples", EMNLP 2025 pp. 31263–31289 — S1. SemEval Task 13 Subtask C 네 번째 분류 "Adversarial — generated via adversarial prompts or RLHF(사람 피드백 강화학습) to mimic humans" — S2 | 연구 결과 | 지난번 기록과 같다. 스타일 규칙 근거로 쓰지 않는 현재 방침 유지 |

C-06 상세

- `docs/tone/comment-economy.md:232` 는 "공개 API에 문서 주석을 다는 것은 공식 강제 항목(`DO use /// for public APIs` 계열)이다" 라고 적었다. 실제 Effective Dart 에 있는 DO 규칙은 "DO use /// doc comments to document members and types" 이고, 연결된 린트는 `slash_for_doc_comments` 다 — S6. 이 규칙은 **주석 문법을 `///` 로 쓰라** 는 것이지 **공개 멤버마다 주석을 달라** 는 것이 아니다. 후자는 PREFER 다.
- 출처끼리 어긋나는 점: 린트 `public_member_api_docs` 설명은 "DO document all public members." 라고 쓴다 — S24. 가이드(PREFER)와 린트 설명(DO)이 다르다. 이 린트 페이지에는 'Stable' 표시만 보였고, `unnecessary_underscores` 페이지(S23)에 있던 'Recommended' 표시는 보이지 않았다. 추론: 기본 권장 린트 묶음에 들어 있지 않은 선택 린트다. 묶음 파일을 직접 열어 확인하지는 않았다.
- 추론: C-06 의 강도를 MUST 로 유지하려면 근거가 "프로젝트 방침" 이어야 하고, Effective Dart 를 강제 근거로 인용하면 출처 강도를 넘는다.

### 2-3. 한국어 축 출처 자체의 상태

- `sources.md:84` · `locale-korean.md:174` 가 "국립국어원 공공언어 자료" 로 적은 etc_seq=663 은 실제로 **"유형별로 알아보는 보도자료 작성 길잡이"** (국립국어원 공공언어과, 등록 2021-03-03, 수정 2021-03-23)다. 목차는 보도자료의 구성·유형·형식·내용이고, 페이지 본문에서 신조어·외래어·전문 용어 지침은 찾지 못했다(첨부 PDF 는 안 읽음) — S8.
  - 추론: 코드 주석 문체의 근거로는 약하다. 이름표가 실제 내용보다 넓게 적혀 있다.
- LINE 글(수J, 2020-12-22)은 독자 수준을 알고 정보 설계를 우선하라는 내용이고, 용어 정의나 새 말 만들기에 관한 조언은 없었다 — S9. K-11 근거로 쓸 수 없다.

## 3. 현행화 — 낡은 곳

직전 카이젠 날짜: 지시문은 2026-08-13 이라고 했지만 레포 기록은 `docs/tone/research-log.md:4` last_updated 2026-08-31, `docs/tone/*.md` 다수가 2026-09-02 다. 이 표는 2026-08-31 이후 변경을 기준으로 봤다.

| 파일:줄 | 현재 값 | 최신 값 | 출처 |
|---|---|---|---|
| `docs/tone/overview.md:154` · `docs/tone-kit/overview.html:540` | `separatorBuilder: (_, __) => divider` | `(_, _)`. Dart 3.7 부터 `_` 를 여러 번 쓸 수 있고, Effective Dart 가 "PREFER using wildcards for unused callback parameters" 로 `.onError((_, _) {...})` 를 좋은 예로 든다. 린트 `unnecessary_underscores` 는 Stable · Recommended · "Released in Dart 3.7", 설명 "AVOID using multiple underscores when a single wildcard will do." | S5 · S23 |
| `docs/tone/dart-flutter-idioms.md:435` · `docs/tone-kit/dart-flutter-idioms.html:851` | `builder: (_, value, __) =>` | `(_, value, _)` (같은 이유) | S5 · S23 |
| `docs/tone/comment-economy.md:232` (+ `core-comment.md:19` C-06 MUST) | "공식 강제 항목(`DO use /// for public APIs` 계열)" | 공식 문구는 "PREFER writing doc comments for public APIs". DO 는 `///` 문법 규칙 | S6 · S24 |
| `tone-kit/references/sources.md:138` | go_router 예제 16.3.0 링크 | 최신 18.0.1 (2026-09-02 게시). 17.0.0 에 "BREAKING CHANGE"(ShellRoute 이동이 관찰자에게 기본으로 알림), 18.0.0 에 "Migrates to material_ui and cupertino_ui" · "Updates minimum supported SDK version to Flutter 3.44/Dart 3.12". 버전 고정 링크라 접속은 된다(200) | S17 · S20 |
| `tone-kit/references/adapter-dart-flutter.md:180` · `:235`, `docs/tone/dart-flutter-idioms.md:618` · `:686`, `docs/tone/naming-taxonomy.md:103` · `:127` · `:401` | "Flutter 3.38.4 기준 58개" | Flutter 안정판 최신 3.47.5 (2026-09-18, Dart 3.13.4). 킷의 재현 명령을 3.47.5 원본에 그대로 돌리면 **58개, 목록도 3.38.4 와 똑같다.** 수치는 유효하고 기준 버전 표기만 오래됐다 | S18 · S19 |
| `tone-kit/references/sources.md:131`–`136` · `:146`–`150`, `core-antipatterns.md:192`, `docs/tone/overview.md:96` | `api.flutter.dev/flutter/material/...` 와 `flutter/flutter` 저장소의 `src/material/*.dart` 링크 | pub.dev `material_ui` 1.4.0 (2026-09-22) 페이지: "The standalone material_ui package was previously built directly into the core Flutter framework as package:flutter/material.dart. It has been decoupled from the flutter/flutter repository into its new home here in flutter/packages." `cupertino_ui` 1.1.1 (2026-09-21) 도 있다. **출처끼리 어긋남:** 그런데 `flutter/flutter` master 와 3.47.5 태그에는 `src/material/checkbox.dart` 가 아직 있고(200), `lib/material.dart` 에 옮김·폐기 안내 문구도 grep 으로 안 나왔다. 지금 링크는 안 깨졌다 | S25 · S17 · 1-2 |
| `tone-kit/references/sources.md:152` | 위키 스타일 가이드, "주의 (위키 이전 이력 있음)" | 위키 페이지에 "This page has migrated to docs/contributing/Style-guide-for-Flutter-repo.md" 가 떠 있고 새 경로 파일(1,867줄)이 있다. 주의 표기를 새 URL 로 바꿀 수 있다 | S26 |
| `tone-kit/references/sources.md:84` · `locale-korean.md:174` | "국립국어원 공공언어 자료" | 실제 제목 "유형별로 알아보는 보도자료 작성 길잡이" (2021) | S8 |
| `tone-kit/references/sources.md:58` | ESLint 아카이브 도메인, "주의" | `eslint.org/docs/latest/rules/no-nested-ternary` 도 200. 본문(폐기 여부)은 안 읽음 | 1-2 |

바뀌지 않은 것 (확인만)

- `adapter-dart-flutter.md:61` · `:271` "Dart 3.8 이상" null-aware element — Dart CHANGELOG 3.8.0 절에 "Dart 3.8 adds null-aware elements to the language." 가 있다 — S21. 유효.
- 킷이 버전을 적지 않은 패키지는 낡을 곳이 없다. 참고로 최신: riverpod · flutter_riverpod · hooks_riverpod 3.4.3 (2026-09-03), freezed 4.0.2 (2026-09-18), flutter_hooks 0.21.3+1 (2025-08-19, 그 뒤 새 판 없음), flutter_lints 6.0.0 (2025-05-27), lints 6.1.0 (2026-01-30) — S17.

## 4. 권장안 (계약 조건 후보)

1. **K-11 강도는 관측 컨벤션으로 둔다.** 영어권 가이드(S14 · S16)는 지지하지만 회사 문서용 규칙이고, 한국어 규범(S10)은 새 말 금지를 말하지 않는다. 그 이상 올릴 외부 근거가 없다.
2. **K-11 문구에서 "사전에 없는" 을 판정 기준으로 쓰지 않는다.** 한글 맞춤법 제50항 해설이 사전에 없는 전문 용어를 정당하게 본다(S10). 대신 "읽는 사람이 뜻을 짐작할 수 없는, 글쓴이가 새로 붙인 이름" 처럼 독자 기준으로 쓰고, 처방은 수집기 문구대로 "원래 이름을 그대로 쓰거나 문장으로 풀어 쓴다" 에 Google 식 "처음 나올 때 괄호로 뜻을 붙인다"(S16)를 선택지로 더하는 안을 검토한다(추론).
3. **K-11 근거 줄에는 S14 · S16 · S10 을 붙이고, S8(보도자료 길잡이)과 S9(LINE)는 붙이지 않는다.** 둘 다 이 규칙을 말하지 않는다.
4. **평가 사례의 예시는 K-05(음역 금지)와 겹치지 않는 것을 고르거나, 겹친다는 사실을 판정 기준에 적는다.** '표시훅' 은 '훅' 음역 때문에 K-05 SHOULD 에도 걸릴 수 있다(추론). 확인 조건 "K-11 을 관측 컨벤션으로 짚되 MUST 위반으로 단정하지 않는다" 는 그대로 쓸 수 있다.
5. **C-06 강도 근거 정리.** `docs/tone/comment-economy.md:232` 의 "공식 강제 항목" 문장을 원문(PREFER)에 맞춰 고치거나, MUST 를 유지한다면 근거를 "프로젝트 방침" 으로 바꾼다. 이 Phase 의 목적(강도가 출처를 넘지 않는지 재확인)에 정확히 해당한다.
6. **문서 예시의 `__` 를 `_` 로 바꾼다** (`docs/tone/overview.md:154`, `docs/tone/dart-flutter-idioms.md:435`, 거울 HTML 두 곳). 권장 린트 묶음이 잡는 모양을 톤 킷 문서가 좋은 예로 보여 주고 있다.
7. **버전 표기 갱신:** 제스처 콜백 58개의 기준 버전을 3.47.5 로 올리거나 "3.38.4 · 3.47.5 에서 같음" 으로 적는다. go_router 예제 링크(`sources.md:138`)와 위키 링크(`sources.md:152`)를 새 값으로 바꾼다.
8. **Material 분리는 기록만 한다.** `material_ui` 분리가 공지됐지만 SDK 저장소에는 파일이 아직 있다. 링크를 지금 바꿀 근거는 부족하다. `sources.md` 에 "주의" 표기와 날짜만 남기는 정도가 맞다(추론).

## 5. 못 가져온 것 / 열린 질문

- 필수 출처 표 8번(디자인 시스템 6곳의 컴포넌트 목록)은 이번에 조회하지 않았다. 이번 항목(P6)이 접미사 체계를 건드리지 않아서다. 지난번 판정("단일 권위 없는 합성")을 다시 확인하지 않았다.
- 국립국어원 보도자료 길잡이(S8) 첨부 PDF 본문은 안 읽었다. PDF 안에 외래어·신조어 지침이 있을 수는 있다.
- "사전에 없는 합성어는 단어별로 띄어 쓴다" 를 직접 말한 온라인가나다 답변을 찾지 못했다(검색 요약에만 나왔고, 연 답변은 다른 주제였다). 없다는 뜻은 아니다.
- 국립국어원 '새말모임' 절차(새 표현을 위원회가 정하는 방식)는 검색 요약에만 나왔고 원문을 열지 않았다. 인용하지 않았다.
- Microsoft Learn 하위 페이지("Use technical terms carefully")의 현재 본문이 공개 저장소(2018년 날짜)와 같은지 확인하지 않았다.
- `public_member_api_docs` 가 `lints` · `flutter_lints` 권장 묶음에 없는지는 페이지 표시로만 짐작했다. 묶음 파일(`recommended.yaml`)을 직접 열지 않았다.
- `material_ui` 분리가 `package:flutter/material.dart` 폐기로 이어지는지, 일정이 있는지는 찾지 못했다. SDK 저장소와 pub.dev 설명이 어긋난다.
- KCI(한국학술지인용색인) 번역투 논문, SemEval 개요 논문, arXiv 초고, ESLint 새 주소, Riverpod 문서는 접속(200)만 확인했고 본문 문구는 다시 대조하지 않았다.
- 한국어 코드 주석에서 새 합성어가 실제로 독자 이해를 해친다는 실증 연구는 찾지 못했다. K-11 근거는 세션 1건 관찰과 영어권 스타일 가이드뿐이다.
