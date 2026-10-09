# 시나리오 작성 규칙

2 단계에서 시나리오를 쓸 때 따른다. 근거는 Cucumber 공식 문서와 Flutter 테스트 도구 소스, 2025 년 산업 사례 연구다.
출처가 "권장" 이라고 한 것을 여기서 필수로 올리지 않았다 — 시나리오당 3~5 단계도 권장이다
([Gherkin Reference](https://github.com/cucumber/website/blob/aeb31cd2f1e05840e36a07b46402edfe5586a59f/docs/gherkin/reference.md) "we recommend 3-5 steps per example").

키워드는 공식 한국어 목록만 쓴다 — `먼저` · `조건` · `만일` · `만약` · `그러면` · `그리고` · `하지만` · `단`
([gherkin-languages.json](https://github.com/cucumber/gherkin/blob/907e36b3d91dfa2a0a9c2b5c102100b6707fa84d/gherkin-languages.json) `ko`).

## 1. 단계 문장은 의도를, 조작 순서는 do 에 따로

단계 문장(`text`)에는 사용자가 하려는 일을 쓰고, 실제로 누른 순서는 `do` 목록에 둔다. 조작을 문장에 섞으면 화면 배치가 바뀔 때마다 시나리오를 다시 써야 하고, 조작을 아예 안 남기면 다른 사람이 같은 실행을 재현하지 못한다.

출처: [Writing better Gherkin](https://github.com/cucumber/website/blob/aeb31cd2f1e05840e36a07b46402edfe5586a59f/docs/bdd/better-gherkin.md) — 행동의 what 을 쓰고 how 를 쓰지 않는다. 선언형이 "less brittle" 하다. 다만 명령형이 맞는 경우도 있다고 해서 금지하지는 않는다.

좋은 예:

```json
{"kw": "만일", "text": "그룹 메뉴에서 나가기를 고른다", "do": [
  {"act": "⋯ 버튼 탭", "shot": "03-menu.png"},
  {"act": "\"그룹 나가기\" 탭", "shot": "04-leave-confirm.png"},
  {"act": "\"확인\" 탭", "shot": "05-after-leave.png"}
]}
```

나쁜 예:

```json
{"kw": "만일", "text": "오른쪽 위 점 세 개를 누르고 두 번째 항목을 누른 뒤 확인을 누른다"}
```

한 단계의 조작이 5 개를 넘으면 상태를 만드는 앞부분을 `먼저` 로 옮기거나 단계를 나눈다. 화면 이동 · 메뉴 열기처럼 시험하려는 규칙과 상관없는 조작이 대개 앞부분이다. 조작이 길면 무엇을 시험하는지 흐려진다
([Keep your scenarios BRIEF](https://github.com/cucumber/website/blob/aeb31cd2f1e05840e36a07b46402edfe5586a59f/blog/2019-09-05-keep-your-scenarios-brief.md) — Essential · Brief, 대부분 5 줄 이하). 보고서는 조작이 3 개를 넘으면 나머지를 접고, 스크립트는 8 개를 넘으면 경고한다.

## 2. 먼저 · 조건 에는 상태를 적는다

`먼저` · `조건` 은 시험을 시작할 때의 상태다. 그 상태를 만드는 조작 과정은 적지 않는다. 다만 로그인 자체를 시험하면 로그인은 상태가 아니라 `만일` 이다.

출처: [Gherkin Reference](https://github.com/cucumber/website/blob/aeb31cd2f1e05840e36a07b46402edfe5586a59f/docs/gherkin/reference.md) — "put the system in a known state", Given 에서는 사용자 상호작용을 말하지 않는다.

좋은 예:

```text
조건 민지는 로그인되어 있다
그리고 내가 유일한 방장인 그룹 "주말 등산" 이 있다
```

나쁜 예:

```text
먼저 이메일 칸을 누른다
그리고 비밀번호를 입력한다
그리고 로그인 버튼을 누른다
```

## 3. 그러면 은 도구로 볼 수 있는 결과를 값으로

`그러면` 에는 대상 · 값 · 상태를 적는다. 사용자에게 보이는 결과를 쓰고, 데이터베이스 기록은 화면 결과를 뒷받침할 때만 `seen` 에 덧붙인다. 한 시나리오는 대부분 규칙 하나를 다룬다. 서로 다른 행동이 이어지면 시나리오를 나눈다.

출처: [Gherkin Reference](https://github.com/cucumber/website/blob/aeb31cd2f1e05840e36a07b46402edfe5586a59f/docs/gherkin/reference.md) — 결과는 "observable output" 이어야 하고 "changes to a database are usually not". [Keep your scenarios BRIEF](https://github.com/cucumber/website/blob/aeb31cd2f1e05840e36a07b46402edfe5586a59f/blog/2019-09-05-keep-your-scenarios-brief.md) — 구체적인 데이터, 대부분 규칙 하나.

좋은 예:

```text
그러면 "방장을 넘긴 뒤 나갈 수 있어요" 안내가 뜬다
그리고 그룹 목록에 "주말 등산" 이 1 개 있다
```

나쁜 예:

```text
그러면 나가기가 잘 막힌다
그리고 데이터베이스 group_members 에 행이 남아 있다
```

## 4. 보인다 · 숨김 · 비활성 · 탭 가능 을 다른 결과로

"없다" 는 네 가지로 갈린다 — 위젯 트리에 없다, 화면 밖에 있다, 보이지만 비활성이다, 다른 것에 가려 눌리지 않는다. 기대하는 것이 어느 쪽인지 문장에 적고, `seen` 에는 그것을 가른 도구 값을 적는다.

출처: [Flutter finders.dart](https://github.com/flutter/flutter/blob/master/packages/flutter_test/lib/src/finders.dart) — 기본 찾기는 화면 밖 위젯을 건너뛰고, `hitTestable` 은 눌리는지를 따로 본다. [Acceptance Test Generation with LLMs](https://arxiv.org/abs/2504.07244) — 비활성으로 기대한 버튼이 실제로는 숨김이었던 불일치가 나왔다.

좋은 예:

```text
그러면 저장 버튼이 보이지만 비활성이다
```

나쁜 예:

```text
그러면 저장 버튼을 쓸 수 없다
```

## 5. 사라짐은 두 번 확인한다

"사라졌다" 는 처음부터 없던 것도 통과시킨다. 행동 전에 있는 것을 확인하고, 화면 전환이 끝난 뒤 찾는 범위를 정해 0 개를 확인한다.

출처: [Flutter matchers.dart](https://github.com/flutter/flutter/blob/master/packages/flutter_test/lib/src/matchers.dart) — `findsNothing` 은 찾을 수 있는 후보 안에서 일치가 없다는 뜻일 뿐이다. [Flutter widget_tester.dart](https://github.com/flutter/flutter/blob/master/packages/flutter_test/lib/src/widget_tester.dart) — 전환이 끝났는지는 예약된 프레임이 없어질 때까지 기다려야 안다.

좋은 예:

```text
조건 현재 화면에 "삭제" 버튼이 1 개 보인다
만일 항목을 삭제한다
그러면 전환이 끝난 뒤 목록 화면에서 "삭제" 버튼과 일치하는 보이는 위젯은 0 개다
```

나쁜 예:

```text
만일 항목을 삭제한다
그러면 삭제 버튼이 사라졌다
```

## 6. 지어낸 실패 경우는 질문으로 돌린다

요구에 없던 실패 경우나 정책을 AI 가 떠올리면 시나리오로 확정하지 말고 사용자 확인 표 아래 질문으로 적는다. 결과를 모르는 채 판정 문장을 쓰면 없는 규칙을 시험하게 된다.

출처: [Acceptance Test Generation with LLMs](https://arxiv.org/abs/2504.07244) — 생성된 시나리오가 요구에 없던 오류 시나리오 두 개와 사용자에게 보이지 않는 결과("backend should be notified")를 더했다. [Example Mapping](https://github.com/cucumber/website/blob/aeb31cd2f1e05840e36a07b46402edfe5586a59f/docs/bdd/example-mapping.md) — 답을 모르는 것은 질문 카드로 남긴다.

좋은 예:

```text
질문: 네트워크가 끊긴 채 나가기를 누르면 어떤 안내가 떠야 하나요? — 답을 받기 전에는 시나리오로 넣지 않는다
```

나쁜 예:

```text
시나리오 4. 네트워크가 끊기면 "잠시 후 다시 시도해 주세요" 가 뜬다
```
