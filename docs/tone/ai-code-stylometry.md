---
title: AI 생성 코드 스타일로메트리와 킷의 포지셔닝
version: 0.1.0
last_updated: 2026-09-02
---

# AI 생성 코드 스타일로메트리와 킷의 포지셔닝

## 이 문서가 잡는 것

1. **목표 문장** — 규칙의 목적은 "읽고 고치기 쉬운 코드"다. "AI 티 지우기"가 아니다.
2. **근거** — 코드 대상 연구만 각주로 쓴다. 근거가 없으면 규칙을 지우지 말고 강도를 내린다.
3. **적용 범위** — 스택에 묶이지 않는 부분과 스택별로 갈리는 부분을 규칙 안에서 분리한다.

탐지 회피를 목표로 삼으면 코드는 더 인위적이 된다. 이름에서 의미가 가장 먼저 사라지기 때문이다.

```dart
// before — 목표가 "AI 티 지우기"일 때
final effectiveTextStyle = textStyle ?? {TokenClass}.bodyMedium; // AI 원본
final ts2 = textStyle ?? {TokenClass}.bodyMedium;                // 접두사는 지웠지만 의미도 같이 지워졌다
```

```dart
// after — 목표가 "읽기 쉬운 이름"일 때
final labelStyle = textStyle ?? {TokenClass}.bodyMedium;         // 이 값이 어디 쓰이는지 이름이 말한다
```

같은 한 줄인데 목표 문장이 달라지면 결과가 갈린다. 이 킷은 **maintainability / style gate** 이며 AI 탐지 회피 도구가 아니다. 코드 대상 탐지 연구는 오히려 표면적 humanizing 을 독립 위험군으로 분류한다.

모든 규칙에는 `MUST` / `SHOULD` / `관측 컨벤션` 중 하나의 강도가 붙는다 — 판정 기준은 뒤쪽 [규칙 강도 등급](#규칙-강도-등급) 절에 있다.

---

## 원칙

### 1. 코드 규칙의 각주는 코드 대상 연구만 가리켜라

자연어 텍스트 탐지 연구를 코딩 표준의 근거로 인용하지 마라.

```text
# before — 규칙은 코드인데 근거는 자연어 문장 탐지 연구다
rule: identifier_length_max
근거: 문장 단위 perplexity 로 생성문을 가려내는 텍스트 탐지 연구
강도: MUST
```

```text
# after — 코드 대상 연구만 근거로, 강도는 그 근거가 버티는 만큼만
rule: identifier_length_max
근거: Droid (EMNLP 2025) — AI 생성 "코드" 탐지 suite. identifier length·naming convention 신호를 다룬다
강도: SHOULD
```

AI 생성물 탐지 문헌은 자연어 텍스트 대상과 소스 코드 대상이 갈라져 있고 신호도 방법론도 다르다. `Droid` 는 단일 탐지기가 아니라 `DroidCollection`(데이터)과 `DroidDetect`(탐지기) 로 구성된 코드 전용 리소스 suite 이며, 수집 대상에 완전 AI 생성물뿐 아니라 인간-AI 공동 작성 코드와 탐지 회피용으로 의도 제작된 adversarial 샘플이 포함된다. DetectGPT(ICML 2023) 와 Binoculars(ICML 2024) 는 **자연어 텍스트** 탐지기이므로 코드 스타일 규칙의 근거로 쓰면 범위를 벗어난 인용이 된다 — 이 킷은 두 논문을 인용하지 않는다.

**강도:** MUST

> **출처:** [Droid: A Resource Suite for AI-Generated Code Detection (EMNLP 2025)](https://aclanthology.org/2025.emnlp-main.1593/) · [arXiv:2507.10583](https://arxiv.org/abs/2507.10583)

### 2. 표면적 humanizing 을 하지 마라 — 개선이 아니라 별도 위험군이다

이름을 흐리거나 잡음을 넣어 "사람이 쓴 것처럼" 만들지 마라. 고칠 것은 의미다.

```dart
// before — 탐지 회피 목적으로 이름을 흐리고 상수를 도로 인라인했다
Widget build(BuildContext context) {
  var c1 = color ?? {TokenClass}.primary;   // 색 계산
  final pad = EdgeInsets.all(8);            // 토큰을 매직넘버로 되돌림
  return {widget_prefix}Badge(color: c1, padding: pad);
}
```

```dart
// after — 접두사만 걷어내고 의미는 남긴다. 토큰은 토큰으로 유지
Widget build(BuildContext context) {
  final badgeColor = color ?? {TokenClass}.primary;
  return {widget_prefix}Badge(
    color: badgeColor,
    padding: {TokenClass}.spacingSm,
  );
}
```

기계 생성 코드를 사람이 쓴 것처럼 표면만 고치는 행위는 문헌에서 독립 클래스로 다뤄진다. Droid 는 이를 `adversarial samples` · `adversarially humanised` · `machine-humanised code` 로 부르고 prompt 기반 공격과 preference-tuning 기반 공격으로 나눈다. SemEval-2026 Task 13 은 Subtask C 의 공식 4-way 분류에 `Adversarial` 을 별도 클래스로 둔다: `Human-written` / `Machine-generated` / `Hybrid` / `Adversarial`. 즉 "AI 티를 지운다"를 목표 문장으로 삼으면 그 목표는 학계가 위험 행위로 분류한 범주와 정확히 겹치고, 스타일 신호 약화는 목표가 아니라 가독성 개선의 부산물이어야 한다.

**강도:** MUST

> **출처:** [SemEval-2026 Task 13 공식 task page](https://github.com/mbzuai-nlp/SemEval-2026-Task13) · [SemEval-2026 task list](https://semeval.github.io/SemEval2026/tasks.html) · [overview paper](https://aclanthology.org/2026.semeval-1.445/)

### 3. 탐지 정확도 수치를 규칙의 근거로 쓰지 마라

규칙은 가독성·변경 용이성·리뷰 비용으로 정당화한다. "탐지기가 못 잡으니까"는 근거가 아니다.

```text
# before — 탐지기 성능을 규칙 정당화에 끌어다 썼다
rule: no_effective_prefix
근거: GPT-Zero adversarial recall 0.10 — 탐지기가 못 잡으므로 이 규칙이 옳다
강도: MUST
```

```text
# after — 근거를 읽는 사람 비용으로 되돌렸다
rule: no_effective_prefix
근거: 지역 변수 이름은 값의 정체를 말해야 한다. `effective` 는 정체가 아니라 유래를 말한다
강도: 관측 컨벤션 (실측 9건 / 4파일)
```

Droid 실측에서 기존 baseline 탐지기는 adversarial 샘플에 약했다. GPT-Zero 의 adversarial recall 은 0.10 이고, adversarial 샘플을 명시 학습한 `DroidDetectCLS-Base/Large` 는 0.92 를 보고한다. 이 수치가 말하는 것은 "탐지를 피할 수 있다"가 아니라 provenance 탐지 자체가 불안정한 기반이라는 것이다. 불안정한 기반 위에 코딩 표준을 세우지 말고, 탐지 문헌은 "왜 이 방향을 목표로 삼지 않는가"를 설명할 때만 써라.

**강도:** MUST

> **출처:** [Droid 논문 PDF (EMNLP 2025)](https://aclanthology.org/2025.emnlp-main.1593.pdf)

### 4. 규칙 본문은 스택 무관으로 쓰고, 스택 표현은 어댑터로 빼라

한 규칙 안에서 축(규칙을 쪼개는 기준선 — 코어는 스택 무관 본문, 어댑터는 스택별 표현)을 나눠라.

```text
# before — 규칙 본문이 Dart 문법에 묶여 다른 스택에 재사용 불가
rule: guard_clause_first
본문: Dart 에서 if (value == null) return; 을 함수 첫 줄에 둔다
```

```text
# after — 코어(스택 무관 본문) + 어댑터 슬롯(스택별 표현만 채우는 자리)
rule: guard_clause_first
본문: 예외 경로를 먼저 끝내고 정상 경로를 가장 바깥 들여쓰기에 남긴다
adapters:
  dart: if (value == null) return;
  rust: let Some(value) = value else { return; };
```

다국어 코드 스타일로메트리 연구는 단일 multilingual 모델로 10개 언어에서 accuracy `84.1% ± 3.8%`, F1 `84.0% ± 4.0%` 를 보고한다. 대상 언어는 C++, C, C#, Go, Java, JavaScript, Kotlin, Python, Ruby, Rust 다. 언어를 가로질러 신호가 잡힌다는 것은 스타일 규칙의 상당 부분이 특정 스택에 묶이지 않는다는 방증이고, 이 킷이 코어 / 어댑터 축을 나누는 근거가 여기 있다. 인용 시 주의: 이 논문의 OpenReview 항목([forum?id=uO8ix6tnZl](https://openreview.net/forum?id=uO8ix6tnZl))은 CoRR 프리프린트 성격이므로 **venue 로 표기하면 부정확하다** — 정식 표기는 SANER 2025 (2025-03, Montréal) 또는 arXiv 2412.14611 이다.

**강도:** SHOULD

> **출처:** [Is This You, LLM? Recognizing AI-written Programs with Multilingual Code Stylometry (SANER 2025)](https://arxiv.org/abs/2412.14611)

### 5. 근거가 없으면 규칙을 지우지 말고 관측 컨벤션으로 강등하라

관측 컨벤션(공개 출처 없이 프로젝트 실측만 있는 규칙 — 준수 강도가 낮다는 뜻이 아니라 근거의 출처가 국지적이라는 뜻이다) 라벨을 붙이고 실측 건수를 적어라.

```text
# before — 국지 실측에 논문 각주를 붙여 강도를 부풀렸다
rule: avoid_effective_prefix
근거: 코드 스타일로메트리 연구에서 LLM 이 `effective*` 접두사를 과대 사용
강도: MUST
```

```text
# after — 출처는 실측 그대로, 강도는 실측이 버티는 만큼만
rule: avoid_effective_prefix
근거: 프로젝트 코퍼스 57파일 스캔 — `effective*` / `resolved*` 9건 / 4파일
강도: 관측 컨벤션 (실측 9건)
```

`effective*` / `resolved*` 접두사가 LLM 생성 코드에 통계적으로 과대표집된다는 주장은 공개 1차 문헌에서 확인되지 않는다. 확인된 코드 탐지 문헌들은 identifier length, naming convention 같은 넓은 신호는 다루지만 특정 접두사 통계는 제시하지 않는다. 프로젝트 실측은 유효한 국지 근거이고 그것을 "관측된 관례"로 쓰는 것은 정직하지만, 같은 규칙에 논문 각주를 붙이는 순간 거짓이 된다.

**강도:** 관측 컨벤션 (실측 9건 / 4파일)

> **출처:** 확인 실패 — [Droid](https://aclanthology.org/2025.emnlp-main.1593/) · [SANER 2025](https://arxiv.org/abs/2412.14611) · [SemEval-2026 Task 13](https://github.com/mbzuai-nlp/SemEval-2026-Task13) 어디에도 해당 통계 없음 (2026-08 확인)

---

## 규칙 강도 등급

규칙 강도는 출처 강도를 넘지 못한다. 공식 문서가 `prefer` 라고 쓴 것을 킷이 `MUST` 로 승격하면 그 승격분은 킷의 창작이지 근거가 아니다.

```text
# before — prefer 를 MUST 로 조용히 승격했다
rule: prefer_const_constructor
근거: 공식 스타일 가이드 — "prefer const constructors"
강도: MUST
```

```text
# after — 출처 강도대로 두거나, 승격 사유를 프로젝트 컨텍스트로 명시한다
rule: prefer_const_constructor
근거: 공식 스타일 가이드 — "prefer const constructors" (권고)
강도: SHOULD
승격 시: 강도를 MUST 로 올리려면 "이 레포는 위젯 리빌드 비용이 지배적" 같은
        프로젝트 사유를 규칙 옆에 함께 적는다
```

이 킷의 모든 규칙은 세 등급 중 하나를 명시한다.

| 등급 | 조건 | 표기 |
|---|---|---|
| MUST | 공식 문서/표준이 금지 또는 강제 | 규칙 문장에 근거 URL 병기 |
| SHOULD | 공식 문서가 `prefer` 수준으로 권고 | 근거 URL + "권고" 명시 |
| 관측 컨벤션 | 공개 근거 없음, 프로젝트 실측만 존재 | "관측 컨벤션 (실측 N건)" 라벨 필수 |

**강도:** MUST

---

## 수치 기준

| 항목 | 값 | 출처 |
|------|-----|------|
| GPT-Zero adversarial recall | 0.10 | Droid (EMNLP 2025) |
| DroidDetectCLS-Base/Large adversarial recall | 0.92 | Droid (EMNLP 2025) |
| 다국어 코드 스타일로메트리 정확도 | 84.1% ± 3.8% (10개 언어) | SANER 2025 |
| 다국어 코드 스타일로메트리 F1 | 84.0% ± 4.0% | SANER 2025 |
| SemEval-2026 Task 13 Subtask C 클래스 수 | 4 (Human / Machine / Hybrid / Adversarial) | 공식 task page |
| `effective*`/`resolved*` 접두사 공개 통계 | 없음 (확인 실패) | 2026-08 조사 |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| DetectGPT·Binoculars 를 코드 스타일 규칙 근거로 인용 | 둘 다 자연어 텍스트 탐지기다. 대상 범위가 달라 근거가 성립하지 않는다 |
| "AI 탐지를 피하기 위해"를 규칙의 목적으로 서술 | 문헌이 adversarial humanizing 을 별도 위험군으로 분류한다. 목적 문장 자체가 위험군과 겹친다 |
| OpenReview forum 링크를 venue 로 표기 | SANER 2025 논문의 OpenReview 항목은 CoRR 프리프린트다. venue 는 SANER 2025 |
| 접두사·어휘 수준 규칙에 논문 각주 붙이기 | 해당 통계는 공개 문헌에 없다. 국지 실측을 논문 근거로 위장하는 것이 된다 |
| 공식 문서 `prefer` 를 킷에서 `MUST` 로 조용히 승격 | 승격분이 근거 없이 규칙 강도로 둔갑한다. 승격은 사유를 밝혀야 한다 |
| 탐지 정확도 수치를 "그러므로 이 규칙이 옳다"의 근거로 사용 | 탐지 가능성과 규칙 타당성은 다른 명제다. 규칙은 유지보수성으로 정당화한다 |

---

## Gotchas

- **"AI 티 제거"는 마케팅 문구로도 쓰지 마라** — 킷 description, README, 스킬 트리거 어휘 어디에도 탐지 회피를 목표로 읽히는 표현을 두지 않는다. Droid/SemEval 이 그 범주를 위험군으로 분류하기 때문에, 목적 문장 하나가 킷 전체의 정당성을 뒤집는다.
- **SemEval Task 13 언어 목록은 출처 간 불일치가 있다** — 공식 README(training: C++/Python/Java, unseen: Go/PHP/C#/C/JS)와 overview paper Table 1(C, C#, C++, Go, Java, JavaScript, Python)이 PHP/C 표기에서 어긋난다. 언어를 열거해야 하면 "multiple languages including …" 형태로 완화하거나 공식 dataset label 파일로 재확인하라.
- **Droid 는 탐지기 이름이 아니라 suite 이름이다** — `DroidCollection`(데이터) + `DroidDetect`(탐지기) 구성. "Droid 탐지기가 …"라고 쓰면 부정확하다.
- **"근거 없음"을 발견하면 규칙을 지우지 말고 등급을 내려라** — 실측이 있는 규칙은 관측 컨벤션으로 살아남는다. 지우면 프로젝트가 실제로 지키던 관례가 사라지고, 논문을 붙이면 거짓이 된다. 세 번째 선택지가 정답이다.
- **탐지 문헌은 "하지 않을 것"을 정의할 때만 인용된다** — 이 문서 외의 다른 리서치 문서에서 탐지 논문을 규칙 근거로 재인용하지 마라. 나머지 문서의 근거 축은 가독성·유지보수 문헌(Ousterhout, Fowler, Beck, 공식 스타일 가이드)이다.
