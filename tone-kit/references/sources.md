# 출처 목록

축별 근거 출처. 규칙을 인용할 때는 그 규칙이 속한 축의 출처만 쓴다.

## 목차

- [검증 상태 표기](#검증-상태-표기)
- [포지셔닝 — AI 생성 코드 탐지](#포지셔닝--ai-생성-코드-탐지)
- [코어 — 주석과 가독성](#코어--주석과-가독성)
- [코어 — 리팩토링과 구조](#코어--리팩토링과-구조)
- [로케일 — 한국어 기술 문체](#로케일--한국어-기술-문체)
- [어댑터 — Dart / Flutter](#어댑터--dart--flutter)
- [제외된 출처](#제외된-출처)

## 검증 상태 표기

| 표기 | 뜻 |
|---|---|
| 확인됨 | 2026-08-28 에 접근성과 인용 문구를 확인 |
| 승계 | 원본 코퍼스의 인용을 그대로 옮김. 개별 재확인 미실시 |
| 주의 | 이동·리다이렉트 이력이 있어 인용 전 재확인 필요 |

승계 출처를 새 규칙의 근거로 처음 쓸 때는 접근 가능 여부를 먼저 확인한다.

## 포지셔닝 — AI 생성 코드 탐지

이 축의 출처는 **"무엇을 목표로 삼지 않는가"** 를 설명할 때만 쓴다. 스타일 규칙의 정당화 근거로 쓰지 않는다.

| 출처 | URL | 상태 |
|---|---|---|
| Droid: A Resource Suite for AI-Generated Code Detection (EMNLP 2025) | <https://aclanthology.org/2025.emnlp-main.1593/> | 확인됨 |
| Droid 프리프린트 | <https://arxiv.org/abs/2507.10583> | 확인됨 |
| SemEval-2026 Task 13 공식 task page | <https://github.com/mbzuai-nlp/SemEval-2026-Task13> | 확인됨 |
| SemEval-2026 task list | <https://semeval.github.io/SemEval2026/tasks.html> | 확인됨 |
| SemEval-2026 Task 13 overview paper | <https://aclanthology.org/2026.semeval-1.445/> | 확인됨 |
| Multilingual Code Stylometry (SANER 2025) | <https://arxiv.org/abs/2412.14611> | 확인됨 |
| 다중 LLM C 코드 저자 판별 | <https://huggingface.co/papers/2506.17323> | 승계 |

SANER 2025 논문의 OpenReview 항목(<https://openreview.net/forum?id=uO8ix6tnZl>)은 프리프린트 성격이다. **venue 로 표기하면 부정확하다** — SANER 2025 또는 arXiv 로 인용한다.

## 코어 — 주석과 가독성

| 출처 | URL | 상태 |
|---|---|---|
| Google Engineering Practices — 리뷰어 관점 | <https://google.github.io/eng-practices/review/reviewer/looking-for.html> | 승계 |
| Software Engineering at Google — 지식 공유 | <https://abseil.io/resources/swe-book/html/ch03.html> | 승계 |
| Microsoft Code with Engineering Playbook | <https://microsoft.github.io/code-with-engineering-playbook/documentation/guidance/code/> | 승계 |
| Robert C. Martin — Necessary Comments | <https://blog.cleancoder.com/uncle-bob/2017/02/23/NecessaryComments.html> | 승계 |
| Ousterhout — A Philosophy of Software Design 강의 | <https://web.stanford.edu/~ouster/cgi-bin/cs190-winter20/lecture.php?topic=bookReview> | 승계 |
| Ousterhout vs Clean Code 토론 기록 | <https://github.com/johnousterhout/aposd-vs-clean-code> | 승계 |
| SonarSource — Cognitive Complexity | <https://www.sonarsource.com/resources/cognitive-complexity/> | 승계 |
| Buse & Weimer — 가독성 모델 (TSE 2010) | <https://dblp.org/rec/journals/tse/BuseW10> | 승계 |
| Google — Tricorder 프로그램 분석 생태계 | <https://research.google/pubs/tricorder-building-a-program-analysis-ecosystem/> | 승계 |
| Meta — Getafix 자동 수정 | <https://engineering.fb.com/2018/11/06/developer-tools/getafix-how-facebook-tools-learn-to-fix-bugs-automatically/> | 승계 |
| 코드 품질 실증 연구 (EMSE) | <https://link.springer.com/article/10.1007/s10664-023-10390-z> | 승계 |
| 코드 이해도 연구 (IST) | <https://www.sciencedirect.com/science/article/pii/S095058492100046X> | 승계 |
| FSE 2025 연구 논문 | <https://conf.researchr.org/details/fse-2025/fse-2025-research-papers/76/> | 승계 |
| 중첩 삼항 금지 — ESLint | <https://archive.eslint.org/docs/rules/no-nested-ternary> | 주의 (아카이브 도메인) |
| 중첩 조건 연산자 회피 — clang-tidy | <https://clang.llvm.org/extra/clang-tidy/checks/readability/avoid-nested-conditional-operator.html> | 승계 |
| Code Complete 발췌 | <https://www.informit.com/articles/article.aspx?p=1235624&seqNum=6> | 승계 |

## 코어 — 리팩토링과 구조

| 출처 | URL | 상태 |
|---|---|---|
| Fowler — Extract Method | <https://refactoring.com/catalog/extractMethod.html> | 승계 |
| Fowler — Extract Class | <https://refactoring.com/catalog/extractClass.html> | 승계 |
| Fowler — Inline Function | <https://refactoring.com/catalog/inlineFunction.html> | 승계 |
| Fowler — Inline Class | <https://refactoring.com/catalog/inlineClass.html> | 승계 |
| Fowler — Introduce Parameter Object | <https://refactoring.com/catalog/introduceParameterObject.html> | 승계 |
| Fowler — Remove Dead Code | <https://refactoring.com/catalog/removeDeadCode.html> | 승계 |
| Fowler — Replace Conditional with Polymorphism | <https://refactoring.com/catalog/replaceConditionalWithPolymorphism.html> | 승계 |
| Fowler — Replace Nested Conditional with Guard Clauses | <https://refactoring.com/catalog/replaceNestedConditionalWithGuardClauses.html> | 승계 |
| Fowler — Function Length | <https://martinfowler.com/bliki/FunctionLength.html> | 승계 |
| Fowler — Code Smell | <https://martinfowler.com/bliki/CodeSmell.html> | 승계 |
| Fowler — YAGNI | <https://martinfowler.com/bliki/Yagni.html> | 승계 |
| Fowler — Is Design Dead? | <https://martinfowler.com/articles/designDead.html> | 승계 |
| Kent Beck — Tidy First | <https://www.oreilly.com/library/view/tidy-first/9781098151232/ch14.html> | 승계 |

## 로케일 — 한국어 기술 문체

| 출처 | URL | 상태 |
|---|---|---|
| 국립국어원 공공언어 자료 | <https://korean.go.kr/front/etcData/etcDataView.do?etc_seq=663> | 승계 |
| 한국어 번역투 연구 (KCI) | <https://www.kci.go.kr/kciportal/landing/article.kci?arti_id=ART002178732> | 승계 |
| LINE — 엔지니어의 글쓰기 | <https://engineering.linecorp.com/ko/blog/why-are-engineers-so-bad-at-writing/> | 승계 |
| LY 엔지니어링 블로그 | <https://techblog.lycorp.co.jp/ko/> | 승계 |
| 우아한형제들 기술 블로그 | <https://techblog.woowahan.com/> | 승계 |
| 카카오 기술 블로그 | <https://tech.kakao.com/> | 승계 |
| NAVER D2 | <https://developers.naver.com/d2/community/> | 승계 |

기업 기술 블로그는 개별 글이 아니라 **문서 구조 관행** 의 참고 사례다. 특정 규칙의 단독 근거로 쓰지 않는다.

## 어댑터 — Dart / Flutter

### 공식 문서 — 확인됨

| 출처 | URL |
|---|---|
| Flutter 성능 모범 사례 | <https://docs.flutter.dev/perf/best-practices> |
| Flutter 아키텍처 개요 | <https://docs.flutter.dev/resources/architectural-overview> |
| `StatelessWidget` | <https://api.flutter.dev/flutter/widgets/StatelessWidget-class.html> |
| `StatefulWidget` | <https://api.flutter.dev/flutter/widgets/StatefulWidget-class.html> |
| `Element.rebuild` | <https://api.flutter.dev/flutter/widgets/Element/rebuild.html> |
| `Widget.canUpdate` | <https://api.flutter.dev/flutter/widgets/Widget/canUpdate.html> |
| `State.setState` | <https://api.flutter.dev/flutter/widgets/State/setState.html> |
| `Builder` | <https://api.flutter.dev/flutter/widgets/Builder-class.html> |
| `RepaintBoundary` | <https://api.flutter.dev/flutter/widgets/RepaintBoundary-class.html> |

### 언어 · 스타일 — 승계

| 출처 | URL |
|---|---|
| Effective Dart — Style | <https://dart.dev/effective-dart/style> |
| Effective Dart — Documentation | <https://dart.dev/effective-dart/documentation> |
| Effective Dart — Design | <https://dart.dev/effective-dart/design> |
| Dart — 패턴 | <https://dart.dev/language/patterns> |
| Dart — 분기 | <https://dart.dev/language/branches> |
| Dart — 컬렉션 | <https://dart.dev/language/collections> |
| Dart — 생성자 | <https://dart.dev/language/constructors> |
| Dart — 클래스 수식자 | <https://dart.dev/language/class-modifiers> |
| Dart — 확장 메서드 | <https://dart.dev/language/extension-methods> |
| Dart — null 안전성 | <https://dart.dev/null-safety> |
| 린트 — `prefer_spread_collections` | <https://dart.dev/tools/linter-rules/prefer_spread_collections> |
| 린트 — `cascade_invocations` | <https://dart.dev/tools/linter-rules/cascade_invocations> |

### 프레임워크 API · 패키지 — 승계

| 출처 | URL |
|---|---|
| `Material.surfaceTintColor` | <https://api.flutter.dev/flutter/material/Material/surfaceTintColor.html> |
| `Border.all` | <https://api.flutter.dev/flutter/painting/Border/Border.all.html> |
| `Divider.build` | <https://api.flutter.dev/flutter/material/Divider/build.html> |
| `Positioned` | <https://api.flutter.dev/flutter/widgets/Positioned/Positioned.html> |
| `Tab` | <https://api.flutter.dev/flutter/material/Tab/Tab.html> |
| `CupertinoActionSheet` | <https://api.flutter.dev/flutter/cupertino/CupertinoActionSheet/CupertinoActionSheet.html> |
| freezed | <https://pub.dev/packages/freezed> |
| go_router 예제 | <https://pub.dev/packages/go_router/versions/16.3.0/example> |
| Riverpod — 코드 생성 | <https://riverpod.dev/ko/docs/concepts/about_code_generation> |
| Riverpod — 변경 이력 | <https://riverpod.dev/docs/whats_new> |

### 프레임워크 소스 — 실제 패턴 참조

| 출처 | URL |
|---|---|
| Flutter — checkbox | <https://github.com/flutter/flutter/blob/master/packages/flutter/lib/src/material/checkbox.dart> |
| Flutter — switch | <https://github.com/flutter/flutter/blob/master/packages/flutter/lib/src/material/switch.dart> |
| Flutter — radio | <https://github.com/flutter/flutter/blob/master/packages/flutter/lib/src/material/radio.dart> |
| Flutter — dropdown | <https://github.com/flutter/flutter/blob/master/packages/flutter/lib/src/material/dropdown.dart> |
| Flutter — tabs | <https://github.com/flutter/flutter/blob/master/packages/flutter/lib/src/material/tabs.dart> |
| Flutter 샘플 | <https://github.com/flutter/samples> |
| Flutter 레포 스타일 가이드 | <https://github.com/flutter/flutter/wiki/Style-guide-for-Flutter-repo> — 주의 (위키 이전 이력 있음) |

## 제외된 출처

원본 코퍼스에 있었으나 이 킷이 인용하지 않는 것들. **되살리지 마라.**

| 출처 | 제외 사유 |
|---|---|
| DetectGPT (ICML 2023) <https://proceedings.mlr.press/v202/mitchell23a.html> | 자연어 텍스트 탐지기. 코드 스타일 규칙의 근거로는 범위를 벗어난다 |
| Binoculars (ICML 2024) <https://icml.cc/virtual/2024/poster/33662> | 자연어 텍스트 탐지기. 위와 같음 |
| LLM 텍스트 스타일로메트리 <https://www.sciencedirect.com/science/article/pii/S0957417425026181> | 대상이 텍스트다. 코드 결론으로 옮길 수 없다 |
| 비공개 사내 코딩 가이드라인 PDF | 공개 URL 이 없다. 소비자가 검증할 수 없는 인용은 싣지 않는다. 해당 근거는 Flutter 공식 문서로 대체됐다 |
| 기본값 해소 접두사 통계 | 공개 1차 문헌에 존재하지 않는다 (2026-08 확인). 해당 규칙은 관측 컨벤션으로만 표기한다 |
