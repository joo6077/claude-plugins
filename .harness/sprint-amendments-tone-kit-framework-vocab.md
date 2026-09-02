# Sprint Contract 개정 — 프레임워크 어휘 우선 규칙

```yaml
sprint: tone-kit-framework-vocab
base_contract: .harness/sprint-contract-tone-kit.md
prior_amendment: .harness/sprint-amendments-tone-kit-readability.md
created: 2026-09-02
iteration: 1
```

기존 계약(50개) + 직전 개정(25개)은 그대로 유효하다. 이 개정은 **사용자 지적 1건**에 대응하는 조건을 추가한다.

> "startLongpress 이것도 좋은데 앱이나 그 프레임웍에서 사용하는거 따라가는게 맞다고 보는데. 예를 들면 pandown pressdown이나 이런걸로"

## 문제

킷의 콜백 이름 규칙이 `Changed` · `Tap` · `Blur` · `Submit` 이라는 **킷이 발명한 접미사 집합**이었다. 프레임워크가 이미 정의한 이벤트 어휘를 따르라는 규칙이 어디에도 없었다.

아이러니하게 킷은 로케일 축에 "공식 API 이름은 번역하지 않는다"(`locale-korean.md`)를 이미 갖고 있었다. 주석에서는 공식 이름을 지키라면서 코드에서는 자체 어휘를 쓰라고 한 셈이다.

**코퍼스 실측 위반**: `handlePressStart` 7건 · `handlePressEnd` 8건 · `…SelectTap` ↔ `…Selected` 혼재. `Press` 하나로는 tap 인지 long press 인지 이름에서 갈리지 않는다.

## 추가 완료 조건

### FV — 프레임워크 어휘 (Framework Vocabulary)

| ID | 조건 | 판정 |
|---|---|---|
| FV-01 | `core-naming.md` 에 코어 원칙 `N-12` 존재 — 강도 `SHOULD`, 축 `어휘` | 규칙표 |
| FV-02 | 우선순위가 `프레임워크 공식 어휘 > 프로젝트 관례 > 새로 만든 말` 로 명시 | 본문 |
| FV-03 | 이름 결정 절차에 "프레임워크가 이미 이름을 정했는가" 선행 단계 존재 | 절차 |
| FV-04 | `adapter-dart-flutter.md` 에 `D-15` + 슬롯 `event_vocabulary` + 제스처 어휘 절 존재 | 규칙표·슬롯표 |
| FV-05 | 제스처 콜백 표가 **SDK 실측 근거**(`gesture_detector.dart` 3.38.4 · 제스처 접두 고유 콜백 **58개** (주석 제외))와 함께 실림. 단계 축 `Down → Start → Update/MoveUpdate → End/Up → Cancel` 명시 | 본문 |
| FV-09 | 58 이라는 수의 **세는 기준과 재현 명령**이 문서에 실림. doc-comment(`///`) 제외 필수 사유(`onForcePress` 는 예시 코드)와 내부 recognizer 콜백 8종 제외 사실 명시 | 본문 · 명령 재실행 |
| FV-06 | `dart-typedef.md` 에서 킷 발명 접미사 집합(`Changed`·`Tap`·`Blur`·`Submit` 나열)이 프레임워크 어휘 우선으로 교체됨 | 템플릿 |
| FV-07 | **도메인 이벤트 예외** 명시 — 프레임워크에 대응이 없으면 프로젝트가 명명. 판정식이 "프레임워크가 이미 아는 이벤트인가" | 본문 |
| FV-08 | 강도가 `MUST` 로 승격되지 않음 — 공식 문서가 소비자 코드 명명을 지시하지 않으므로 `SHOULD` 가 상한 | 강도 라벨 |

### FC — 정합 (Consistency)

| ID | 조건 | 판정 |
|---|---|---|
| FC-01 | 운영 문서(`references/`)와 근거 문서(`docs/tone/`)가 같은 규칙을 말함 | 교차 대조 |
| FC-02 | 어댑터 슬롯 표가 `references` ↔ `docs/tone/dart-flutter-idioms.md` 양쪽에서 일치 (`event_vocabulary` 포함) | 대조 |
| FC-03 | `naming-taxonomy` 의 기존 "taxonomy 는 업계 표준이 아니다" 경고와 **모순 없음** — 컴포넌트 접미사(단일 권위 없음 → 합성)와 이벤트 어휘(프레임워크가 정함 → 준수)를 구분해 설명 | 본문 |
| FC-04 | HTML 2페이지가 갱신된 md 를 반영 (제스처 표 실림) | 대조 |

### ER3 — 게이트 (회귀)

| ID | 조건 | 판정 |
|---|---|---|
| ER3-01 | `validate-plugin.py` 12 plugins 12 OK · exit 0 | 실행 |
| ER3-02 | `run-evals.py` 전체 PASS | 실행 |
| ER3-03 | `sync-docs` · `sync-orchestrator` drift 0 | 실행 |
| ER3-04 | `TODO`/`TBD`/`FIXME` 0건 · 언어 없는 코드펜스 0건 | V5 · V6 |
| ER3-05 | 프로젝트 고유 식별자 0건 | grep |
| ER3-06 | 타 킷 디렉토리 수정 0건 | git status |
| ER3-07 | 기존 출처·강도 라벨 삭제 0건 | git diff 대조 |

## 범위 밖

- 기존 계약 50개 + 직전 개정 25개 재평가 (회귀만 관찰)
- 코퍼스의 실제 이름 수정 (규칙만 정의, 적용은 별개 작업)
- Flutter 외 스택의 이벤트 어휘 — 어댑터가 없으므로 대상 아님

## 판정

전 조건 PASS → APPROVE. FAIL 1건 이상 → REJECT + 수정 지시.
