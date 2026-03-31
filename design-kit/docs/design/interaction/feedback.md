---
title: 피드백 패턴
version: 0.3.0
last_updated: 2026-03-30
---

# 피드백 패턴

피드백 수단 선택, 알림 피로(notification fatigue), 권한 요청 패턴, 온보딩 플로우 설계를 다룬다.

---

## 원칙

### 1. 정보 유형에 맞는 피드백 수단을 선택한다

NNGroup은 피드백 수단을 세 가지로 분류한다: **인디케이터**(UI 요소에 부착된 수동적 표시), **유효성 검사**(사용자 입력 오류에 대한 반응), **알림**(시스템 이벤트 공지). 잘못된 수단을 선택하면 효과가 사라진다 — 예를 들어 "토스트는 에러 메시지를 구현하는 나쁜 방법"이다.

> **출처:** [Indicators, Validations, and Notifications — NNGroup](https://www.nngroup.com/articles/indicators-validations-notifications/)

### 2. 긴급도에 비례하여 침투도를 조절한다

중요하지 않은 정보에 모달을 사용하면 사용자를 짜증나게 하고, 중요한 에러에 토스트를 사용하면 사용자가 놓친다. 심각도가 높을수록 침투도가 높은 수단(모달)을, 낮을수록 침투도가 낮은 수단(토스트/인디케이터)을 사용한다.

> **출처:** [Error-Message Guidelines — NNGroup](https://www.nngroup.com/articles/error-message-guidelines/)

### 3. 사용자 액션이 필요한 피드백과 정보 제공용 피드백을 구분한다

NNGroup은 알림을 두 가지로 나눈다: **액션 필요 알림**(모달 팝업 권장, 즉각적 주의와 확인 필요)과 **수동적 알림**(코너 배지, 팝오버 등 비침투적 방식, 놓칠 위험 있음). 혼용하면 사용자가 언제 행동해야 하는지 판단하기 어렵다.

> **출처:** [Indicators, Validations, and Notifications — NNGroup](https://www.nngroup.com/articles/indicators-validations-notifications/)

### 4. 피드백은 컨텍스트에 가깝게 배치한다

인디케이터는 "관련 UI 요소에 연결되어 근처에 표시"된다. 유효성 검사 메시지도 해당 필드 옆에 배치한다. 글로벌 알림(토스트/스낵바)만 예외적으로 화면 상단이나 하단에 고정 배치한다.

> **출처:** [Indicators, Validations, and Notifications — NNGroup](https://www.nngroup.com/articles/indicators-validations-notifications/)

---

## 토스트/스낵바

### 토스트와 스낵바의 차이

| 구분 | 토스트 (Toast) | 스낵바 (Snackbar) |
|------|---------------|------------------|
| 목적 | 순수 정보 전달 | 정보 전달 + 선택적 액션 |
| 사라짐 | 자동 사라짐 | 자동 또는 사용자가 닫음 |
| 액션 | 없음 | "실행취소", "다시 시도" 등 1개의 액션 버튼 가능 |
| 사용 예 | "메시지가 전송되었습니다" | "항목이 삭제되었습니다 [실행취소]" |

> **출처:** [Snackbar vs Toast: Decoding the Subtle Differences — Medium](https://medium.com/design-bootcamp/ux-blueprint-01-snackbar-vs-toast-decoding-the-subtle-differences-in-design-systems-8ad82ff61115)

### 표시 시간 (Duration)

Material Design 3의 스낵바 표시 시간 가이드라인:

| 유형 | 시간 | 사용 시기 |
|------|------|----------|
| **SHORT** | 2.0초 | 짧은 확인 메시지 ("저장됨") |
| **LONG** | 3.5초 | 약간 긴 메시지 또는 액션 포함 시 |
| **INDEFINITE** | 무기한 (사용자 닫기 또는 다음 스낵바까지) | 중요한 액션이 필요한 경우 |

> **출처:** [Snackbar — Material Design 3](https://m3.material.io/components/snackbar/guidelines)

### 배치 (Placement)

- **기본 위치:** 화면 하단 (Material Design 3 기본값)
- **FAB와의 관계:** FloatingActionButton 위에 표시하여 FAB를 가리지 않도록 한다
- **동시 표시 금지:** 한 번에 하나의 스낵바만 표시. 새 스낵바가 트리거되면 기존 스낵바가 먼저 사라진 후 새 것이 나타난다
- **입력 차단 없음:** 스낵바가 표시된 동안에도 사용자가 다른 작업을 계속할 수 있어야 한다. 스와이프로 닫기를 지원한다.

> **출처:** [Snackbar — Material Design 3](https://m3.material.io/components/snackbar/guidelines)

### 사용 금지 사례

NNGroup은 토스트/스낵바를 다음 상황에 사용하면 안 된다고 경고한다:

- **에러 메시지:** 자동으로 사라지므로 사용자가 에러 내용을 읽지 못하고 복구 방법을 파악할 수 없다
- **중요한 시스템 상태 변경:** 사용자의 주의가 다른 곳에 있을 수 있으므로 놓칠 위험이 크다
- **액션이 반드시 필요한 알림:** 토스트는 본질적으로 무시 가능하므로 필수 액션에 부적합하다

> **출처:** [Indicators, Validations, and Notifications — NNGroup](https://www.nngroup.com/articles/indicators-validations-notifications/)

---

## 다이얼로그/모달

### 모달을 사용해야 하는 경우

NNGroup은 모달 다이얼로그의 정당한 사용 사례를 다음과 같이 제한한다:

1. **치명적 에러 방지 및 확인:** 파일 덮어쓰기, 계정 삭제, 저장하지 않은 작업 등 되돌릴 수 없는 행동 전에 사용자를 일시 정지시키고 확인을 받는다.
2. **필수 정보 요청:** 누락된 정보가 태스크 완료를 차단하는 경우 (로그인 요구, 필수 입력 필드 등).
3. **워크플로우 분리:** 복잡한 프로세스를 소화 가능한 단계로 나누는 모달 위저드. 단, 다단계 모달은 사용자가 컨텍스트를 잊을 위험이 있다.

> **출처:** [Modal & Nonmodal Dialogs: When (& When Not) to Use Them — NNGroup](https://www.nngroup.com/articles/modal-nonmodal-dialog/)

### 모달을 사용하면 안 되는 경우

NNGroup 연구에서 참가자들은 모달 다이얼로그에 대해 **"본능적인 혐오감(visceral disdain)"**을 표현했다. 다음 상황에서 모달은 금물이다:

- **비필수 정보:** "사용자의 목표와 직접 관련이 없는 모달 다이얼로그는 짜증나는 것으로 인식된다." 뉴스레터 구독, 프로모션, 비중요 요청은 모달이 아닌 인라인 배너나 페이지 내 섹션으로 처리한다.
- **고위험 프로세스 중:** 결제 플로우에서 불필요한 모달은 신뢰를 훼손하고 구매 결정에 영향을 미칠 수 있다.
- **외부 정보가 필요한 의사결정:** 모달이 차단한 정보를 참조해야 하는 결정을 모달 안에서 요구하면 안 된다.

> **출처:** [Modal & Nonmodal Dialogs: When (& When Not) to Use Them — NNGroup](https://www.nngroup.com/articles/modal-nonmodal-dialog/)

### "양치기 소년" 효과

NNGroup은 비필수 콘텐츠에 모달을 남용하면 **"양치기 소년(Boy Who Cried Wolf)" 효과**가 발생한다고 경고한다. 사용자가 모든 모달을 반사적으로 닫게 되어, 정말 중요한 모달(데이터 손실 경고 등)도 무시하게 된다.

> **출처:** [Modal & Nonmodal Dialogs: When (& When Not) to Use Them — NNGroup](https://www.nngroup.com/articles/modal-nonmodal-dialog/)

### 확인 다이얼로그 설계 규칙

NNGroup은 확인 다이얼로그의 가장 중요한 유저빌리티 고려사항은 **"과도하게 사용하지 않는 것"**과 **"사용자가 무엇에 동의하는지 충분히 구체적으로 알려주는 것"**이라고 밝힌다.

- 확인 버튼에 구체적 동작을 라벨링한다 ("확인" 대신 "영구 삭제", "저장하지 않고 나가기" 등)
- 취소 버튼은 항상 제공한다
- 파괴적 액션의 확인 버튼은 빨간색 등으로 경고 시각 표시를 한다

> **출처:** [Confirmation Dialogs Can Prevent User Errors (If Not Overused) — NNGroup](https://www.nngroup.com/articles/confirmation-dialog/)

### 모달의 대안

| 대안 | 적합한 경우 |
|------|-----------|
| 인라인 UI (폼, 카드) | 추가 정보 입력, 편집 |
| 별도 페이지 | 복잡한 워크플로우, 많은 입력 |
| 사이드바/패널 | 상세 정보 조회, 비교 |
| 아코디언 | 점진적 공개(progressive disclosure) |
| 페이지 내 배너 | 프로모션, 비필수 공지 |
| 바텀 시트 | 모바일에서 옵션 선택, 필터 |

> **출처:** [Popups: 10 Problematic Trends and Alternatives — NNGroup](https://www.nngroup.com/articles/popups/)

---

## 에러 상태

### 에러 메시지 4대 원칙 (NNGroup)

#### 1. 가시성 (Visibility)

- 에러가 발생한 UI 요소 **바로 옆에** 메시지를 배치하여 인지 부하를 줄인다
- **굵은 글씨, 높은 대비, 빨간색** 텍스트에 아이콘을 조합한다
- 색상이나 애니메이션**만으로** 에러를 표시하면 안 된다 — 색각 이상 사용자를 위해 아이콘과 텍스트를 병용한다
- 심각도에 따라 수단을 차등 적용한다: 경미한 이슈는 토스트, 심각한 차단은 모달

> **출처:** [Error-Message Guidelines — NNGroup](https://www.nngroup.com/articles/error-message-guidelines/)

#### 2. 명확한 커뮤니케이션 (Communication)

- **평이한 언어:** 기술 전문용어와 모호한 에러 코드를 피한다
- **구체적으로:** "오류가 발생했습니다"를 "이메일 주소에 @ 기호가 필요합니다"로 교체한다
- **건설적 조언:** 문제만 지적하지 말고 해결책을 제시한다
- **정중한 어조:** "잘못된(invalid)", "불법(illegal)" 같은 비난조 용어 대신 긍정적이고 비판단적 언어를 사용한다. 유머도 피한다.

> **출처:** [Error-Message Guidelines — NNGroup](https://www.nngroup.com/articles/error-message-guidelines/)

#### 3. 효율성 (Efficiency)

- **사전 예방:** 흔한 실수를 미리 감지한다 (예: 이메일 첨부 누락 경고)
- **데이터 보존:** 사용자 입력을 유지하여 수정만 하면 되도록 한다. 처음부터 다시 입력하게 하면 안 된다
- **가이드된 복구:** 자유 입력 대신 제한된 선택지에서 수정안을 제시한다 (예: "이 주소를 찾으셨나요?")
- **추가 도움 링크:** 간결한 에러 메시지에서 상세 설명 페이지로 연결한다

> **출처:** [Error-Message Guidelines — NNGroup](https://www.nngroup.com/articles/error-message-guidelines/)

#### 4. 시기 (Timing)

- **조기 에러 표시 금지:** 탐색적 상호작용 중에 에러를 표시하지 않는다
- **인라인 실시간 검증은 신중하게:** 본질적으로 에러가 발생하기 쉬운 입력(비밀번호 강도 등)에만 타이핑 중 검증을 적용한다
- 대부분의 필드는 **사용자가 필드를 떠난 후(onBlur)**에 검증한다

> **출처:** [Error-Message Guidelines — NNGroup](https://www.nngroup.com/articles/error-message-guidelines/)

### 에러 심각도별 표시 전략

| 심각도 | 표시 수단 | 사용자 액션 | 예시 |
|--------|----------|-----------|------|
| **정보** | 인라인 텍스트, 인디케이터 | 불필요 | "비밀번호 강도: 보통" |
| **경고** | 인라인 배너, 토스트 | 선택적 | "저장 공간이 부족합니다" |
| **에러** | 인라인 메시지 + 아이콘 | 필요 (수정) | "이메일 형식이 올바르지 않습니다" |
| **치명적** | 모달 다이얼로그 | 필수 (즉각 대응) | "네트워크 연결이 끊어졌습니다" |

### 복구 패턴

사용자가 에러에서 복구하는 것을 돕는 구체적 패턴:

- **실행취소 (Undo):** 파괴적 액션 후 일정 시간 동안 되돌리기 옵션을 스낵바로 제공 ("삭제되었습니다 [실행취소]")
- **자동 저장:** 폼 진행 상황을 자동으로 저장하여 네트워크 오류 등에서 데이터 손실을 방지
- **재시도 (Retry):** 일시적 오류(네트워크 타임아웃 등)에 "다시 시도" 버튼을 명확히 제공
- **대안 경로:** 주요 경로가 실패할 때 대안을 제시한다 ("이메일로 로그인할 수 없으신가요? 전화번호로 로그인하기")
- **지원 연락:** 3회 이상 에러가 반복되면 고객 지원 채널로 연결한다

> **출처:** [Error-Message Guidelines — NNGroup](https://www.nngroup.com/articles/error-message-guidelines/)
> **출처:** [10 Design Guidelines for Reporting Errors in Forms — NNGroup](https://www.nngroup.com/articles/errors-forms-design-guidelines/)

---

## 알림 피로 (Notification Fatigue)

### 현상

알림을 과다하게 보내면 사용자가 모든 알림을 무시하게 되는 현상이다. "양치기 소년" 효과와 동일한 메커니즘.

**데이터:**
- Localytics 조사: 푸시 알림을 받은 사용자의 **52%**가 알림을 "성가시다"고 응답
- Accengage: 앱 설치 후 알림 옵트인 비율은 iOS에서 약 **46%**, Android에서 약 **91%** (Android는 기본 허용)
- 주 7회 이상 푸시를 보내는 앱의 사용자 유지율은 주 1~2회 앱 대비 **약 50% 낮다**

### 알림 등급 체계

| 등급 | 침투도 | 표시 수단 | 예시 |
|------|--------|----------|------|
| **Critical** | 최고 — 즉시 대응 필요 | 모달, 시스템 알럿, 푸시+소리 | 보안 침해, 결제 실패, 데이터 손실 위험 |
| **High** | 높음 — 가능한 빨리 확인 | 인앱 배너, 푸시(무음 가능) | 새 메시지, 배송 상태 변경 |
| **Medium** | 중간 — 편한 시점에 확인 | 뱃지, 인디케이터 | 새 기능 알림, 콘텐츠 추천 |
| **Low** | 낮음 — 무시해도 무방 | 알림 센터에만 누적 | 앱 업데이트 안내, 프로모션 |

**핵심 규칙:**
- 사용자에게 알림 카테고리별 on/off 제어권을 제공한다
- Critical이 아닌 알림에 소리/진동을 넣지 않는다
- 동일 유형 알림이 3개 이상 쌓이면 그룹핑한다 ("김철수 외 2명이 메시지를 보냈습니다")
- 마케팅 알림은 사용자 행동 기반 타이밍에만 발송한다 (예: 장바구니 이탈 24시간 후)

> **출처:** [NNGroup — Push Notifications: A Complete Guide](https://www.nngroup.com/articles/push-notification/)
> **출처:** [NNGroup — Indicators, Validations, and Notifications](https://www.nngroup.com/articles/indicators-validations-notifications/)

---

## 권한 요청 패턴 (Permission Requests)

### 시스템 권한 요청의 문제

iOS/Android 모두 카메라, 위치, 알림 등 시스템 권한은 OS 다이얼로그로 요청하며, 사용자가 거부하면 설정 앱에서만 복구 가능하다. 따라서 첫 요청의 수락률이 매우 중요하다.

### 프라이밍 패턴 (Pre-Permission Priming)

시스템 권한 요청 **전에** 앱 자체 UI로 이유를 설명하는 "프라이밍 스크린"을 삽입한다.

```
[앱 자체 화면]
"정확한 배송 추적을 위해 위치 접근이 필요합니다"
[허용할게요] [나중에]
        ↓ "허용할게요" 탭 시
[iOS 시스템 다이얼로그]
"이 앱이 사용자의 위치에 접근하도록 허용하시겠습니까?"
[앱 사용 중 허용] [한 번 허용] [허용 안 함]
```

**효과:**
- Cluster 앱 사례: 프라이밍 적용 후 iOS 사진 접근 수락률 **+12%**
- 이유를 설명하지 않고 바로 시스템 다이얼로그를 띄우면 수락률이 **40% 미만**으로 하락한다는 연구 결과

### 권한 요청 타이밍

| 타이밍 | 수락률 | 적합한 상황 |
|--------|--------|-----------|
| **즉시 (앱 첫 실행)** | 낮음 (30~50%) | 핵심 기능에 필수인 경우에만 (메신저의 알림) |
| **맥락 기반 (필요 시점)** | 높음 (60~80%) | 사진 업로드 탭 시 카메라 권한, 지도 탭 시 위치 권한 |
| **점진적 (사용 후)** | 가장 높음 (70~85%) | 앱을 2~3회 사용 후 알림 제안 |

Apple HIG는 "사람들이 기능을 이해하기도 전에 권한을 요청하지 마라"고 명시한다.

> **출처:** [Apple HIG — Requesting Permission](https://developer.apple.com/design/human-interface-guidelines/requesting-permission)
> **출처:** [NNGroup — Permission Patterns](https://www.nngroup.com/articles/permission-requests/)

---

## 온보딩 플로우 설계

### 온보딩 유형

| 유형 | 설명 | 적합한 앱 | 주의점 |
|------|------|----------|--------|
| **프로그레시브 (Progressive)** | 사용하면서 자연스럽게 기능을 발견 | 직관적 UI의 소비자 앱 | 가장 권장. NNGroup "학습을 한 번에 몰아서 시키지 마라" |
| **코치마크 (Coach Marks)** | 화면 위에 오버레이로 기능 설명 | 복잡한 전문 도구 | 3개 이하로 제한. 사용자의 85%가 스킵한다 (Appcues 데이터) |
| **온보딩 슬라이드** | 앱 첫 실행 시 3~5장 스와이프 | 브랜드/가치 전달 필요 시 | 기능 설명보다 가치 제안에 집중. "건너뛰기" 반드시 제공 |
| **빈 상태 (Empty State)** | 콘텐츠가 없을 때 가이드 표시 | CRUD 앱, 프로젝트 도구 | 첫 번째 행동(CTA)을 명확히 제시 |
| **인터랙티브 튜토리얼** | 실제 앱 내에서 지시를 따라 수행 | 게임, 복잡한 작업 도구 | 반드시 스킵/나중에 가능해야 함 |

### 핵심 규칙

- **스킵 가능하게 만든다**: NNGroup은 "강제 튜토리얼은 사용자를 짜증나게 한다"고 강조한다
- **한 번에 1가지만 가르친다**: 인지 부하 이론(Cognitive Load Theory) — 단기 기억의 용량은 4±1 청크
- **맥락 안에서 가르친다**: 설정 화면의 기능을 홈 화면에서 설명하지 않는다. 해당 화면에서 해당 기능을 만났을 때 설명한다
- **재접근 가능하게 한다**: 온보딩 팁을 한 번 닫으면 영원히 사라지는 것은 안티패턴. 도움말/설정에서 다시 볼 수 있게 한다
- **성과 지표를 추적한다**: 온보딩 완료율, 핵심 액션 도달 시간, 7일 유지율을 측정한다

> **출처:** [NNGroup — The Role of Empty States in UX](https://www.nngroup.com/articles/empty-state-interface-design/)
> **출처:** [NNGroup — Mobile App Onboarding](https://www.nngroup.com/articles/mobile-app-onboarding/)
