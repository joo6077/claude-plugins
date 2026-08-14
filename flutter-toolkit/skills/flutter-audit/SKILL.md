---
name: flutter-audit
description: >
  코드 품질 감사. quick 모드(단일 에이전트, 빠른 로컬 검토)와 deep 모드(최대 4에이전트 병렬 감사)를 지원한다.
  "리뷰해줘", "감사 돌려줘", "코드 검토", "품질 검사", "커밋 전에 확인",
  "PR 올리기 전에 검토", "코드 체크", "아키텍처 확인",
  "code review", "quality check", "audit", "lint check" 같은 요청 시 사용한다.
  변경 파일 수에 따라 자동으로 모드를 선택하지만 명시적으로 지정할 수도 있다.
  단순 탐색, 코드 읽기, 질문 응답만 할 때는 사용하지 않는다.
argument-hint: "[quick|deep] [path]"
user-invocable: true
---

## Gotchas

- quick 모드와 deep 모드의 차이: quick은 단일 에이전트 로컬 검토, deep은 최대 4에이전트 병렬 감사 — 변경 파일 5개 이하면 quick, 초과면 deep이 기본
- Provider watch 대신 select 사용 여부를 체크한다 — 성능 이슈의 주요 원인
- 커스텀 위젯에 const 생성자가 빠져 있으면 리빌드 최적화가 안 된다 — audit에서 지적 대상
- Flutter 3.41에서 테스트 매처 `containsSemantics`가 `isSemantics`로 변경됨 — 테스트 코드에 deprecated 매처가 남아 있으면 지적 대상. `matchesSemantics`(exact)와 구분 필요
- **Impeller 플랫폼별 상태 체크리스트 (2026-08 정정)** — iOS: 필수 (Skia 전환 불가). Android API 29+: 기본 활성. **macOS / Linux / Windows: Flutter 3.47 부터 Impeller 가 기본**. Web: Skia (canvaskit/skwasm). 감사 시 대상 플랫폼에 따라 Impeller 관련 성능 지적을 분기하라 — Web 앱에 Impeller 최적화를 요구하면 오탐이고, 반대로 **데스크톱을 "Impeller 미지원" 으로 단정하는 것도 이제 오탐**이다. 프로젝트의 Flutter 버전을 먼저 확인하고 판정하라 (출처: <https://docs.flutter.dev/perf/impeller>)
- **Android 의존성 매트릭스는 Flutter 3.47 기준으로 확인하라** — 3.47 발표가 제시하는 매트릭스는 **Java 17 · KGP 2.4.0 · AGP 9.1.0 · Gradle 9.3.1** 이다. AGP 9 는 더 이상 "전환이 본격화되는 pre-stable" 이 아니라 매트릭스에 명시된 값이므로, `build.gradle` 감사 시 이 버전들과 대조해 미달/초과를 지적하라. 플러그인 호환성 문제로 `android.newDsl=false` 같은 임시 플래그가 남아 있으면 제거 가능 여부를 함께 확인한다 (출처: <https://flutter.dev/blog/whats-new-in-flutter-3-47>, <https://docs.flutter.dev/release/breaking-changes/migrate-to-agp-9>)
- **Primitive Substitution Gate 감사 (E2 · `HAS_DS = true` 일 때만)** — `references/primitive-substitution-gate.md` 가 SSOT 다. deep 모드에서는 그 파일 §deep 검색 의 명령으로 게이트 대상 직접 사용을 **전수 열거**하고, 각 사용처에 DS 대체 후보가 실재하는지 확인해 위반으로 보고한다. quick 모드에서는 변경 파일 범위에서만 본다. **면제 목록(layout primitive)을 위반으로 올리지 마라** — 이 게이트를 "기본 위젯 전면 금지" 로 확대하면 리포트가 노이즈가 되어 무시된다. 실측 REJECT `RE-02` (2026-08-12) 대응
- **Binary Decidability Pre-Check (agent §3.5 대응)** — 감사 시작 **전** 체크리스트의 각 항목이 PASS/FAIL 중 하나로 귀결 가능한지 자체 검토. "적절한", "충분한", "최소한" 같은 정성적 수식어가 있으면 파일/라인/임계값을 먼저 구체화하고, 그래도 모호하면 해당 항목은 `[미검증]` 으로 표기하되 **조용한 PASS 금지**. 마커 의미와 임계값은 이 문서에서 정의하지 않는다 — 아래 §Unverified-Evidence Protocol 을 따른다
- **Rule-by-Rule Audit — 완료 선언 전 전수 대조 (skill-design-guide §3.6 대응)** — 감사 리포트 제출 직전, 본 Gotchas + Architecture/State/Widget/Design System/i18n 체크리스트를 다시 한 번 읽고 각 규칙에 대해 "확인했는가 / 근거는 파일:라인 으로 가능한가" 를 1:1 대조한 뒤 보고. "그 외에도 혹시 놓친 규칙이 있는가?" 메타 질문을 스스로 1 회 더 수행 (insights-report #1 Proactive quality gaps 대응). 사용자가 첫 피드백 루프가 되면 안 된다
- **L3 Honesty — 정적 Grep 만으로 PASS 금지 (qa-evaluation-guide 대응)** — 파일 존재·키워드 포함은 L1/L2. PASS 를 주려면 `Read` 로 실제 내용을 읽거나 `Bash` 로 analyze/test 명령을 실행해 결과를 확인(L3). L3 수행이 불가능한 항목은 `[미검증]` 마커를 리포트에 붙이고 사유(예: "dart test 환경 미구성") 를 기재
- **감사 범위 Scope Range 선언 (contract-design-guide 대응)** — 리포트 서두에 "감사 대상: <glob 패턴 or 파일 목록>" 을 명시하여 평가자·사용자가 범위를 재해석하지 않도록 한다. `quick` 모드는 `git diff --name-only` 결과, `deep` 모드는 `lib/` 전체 (또는 `$ARGUMENTS` 의 path) 가 기본 Scope Range

Flutter 프로젝트의 코드 품질 감사. 프로젝트 환경을 자동 감지하여 적합한 규칙으로 검사한다.

## Unverified-Evidence Protocol

> **정본(SSOT):** `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol.
> 아래 5 조항은 정본을 **문구 변형 없이** 복제한 것이다. 이 문서에서 임계값이나 마커 의미를 다시
> 정의하지 않는다.

1. **마커는 `[미검증]` 하나로 통일한다.** 동의어(`미확인`, `N/A`, `TBD`, `unverified`) 를 만들지 않는다.
   `[정적]` 은 "런타임 없이 정적으로만 확인" 을 뜻하는 보조 태그이며 `[미검증]` 을 대체하지 않는다.
2. **`[미검증]` 은 검증 도구·환경 부재 전용이다.** 대상이 없거나 미구현이면 그것은 미검증이
   아니라 **FAIL** 이다. 증거는 있으나 공허하면(빈 출력·0 활성화) 그것도 `[미검증]` 이다
   (3 분기: FAIL / 도구 부재 / 증거 무효).
3. **임계값은 2 다.** `[미검증]` 0 건은 통상 판정, **1 건은 PASS 허용 + 경고 명시, 2 건 이상은
   개별 FAIL 이 없어도 verdict 는 REJECT**. "CONDITIONAL APPROVE" 를 쓰는 킷은 그것이
   "1 건 + FAIL 0" 인 경우에만 유효하며, 2 건 이상에는 쓸 수 없다.
4. **생성자의 완료 주장은 증거가 아니다.** 구현자가 "동작 확인함 / 실행했음" 이라고 쓴 문장,
   코드 주석, 커밋 메시지의 자기 평가는 상태 검증이 아니다. 명시적 완료 주장을 포함한 자기평가
   에이전트 궤적에서 **실패의 75.8% 가 false success** 였고, LLM 판정자의 AUROC 는 0.54~0.65 에
   그쳤다 ([arxiv 2606.09863](https://arxiv.org/abs/2606.09863)). 근거는 **도구 출력과 상태
   변화**여야 한다.
5. **조용한 PASS 금지 + 집계 의무.** 검증을 건너뛰고 정적 정황만으로 PASS 를 주지 않는다.
   리포트에 `미검증 N 건` 을 반드시 집계하고, 건별로 `[조건/항목 ID, 사유, 시도한 fallback 단계]`
   를 남긴다.

## 사용자 보고와 자기 증거가 충돌할 때

> **정본(SSOT):** `harness/docs/guides/qa-evaluation-guide.md`
> §Canonical User-Reported Failure Protocol.
> 상태어 · 오라클 유효성 축 · 완료 해제 조건은 **그 절이 정의한다.** 이 문서에서 재정의하지 않는다.

아래 Evidence Validity Gate 는 **자기 증거의 유효성**을 본다. 그것과 별개로, 사용자가 "아직
깨져 있다" 고 보고했는데 감사자가 자기 grep·테스트·스냅샷을 근거로 **반박**하는 경로가 있다.
그 경우 정본 절차가 **먼저** 돈다 — 사용자 관측은 반증 대상이 아니라 재현 대상이고, 먼저
의심할 것은 자기 오라클이 사용자가 보는 것을 재고 있는지다.

## Evidence Validity Gate — 공허한 증거 차단

> **정본:** `harness/docs/guides/qa-evaluation-guide.md` §Evidence Validity Gate.
> Flutter 감사에서 이 게이트가 필요한 이유: 빈 카탈로그 스냅샷을 근거로 "정상 렌더링" 을 반복
> 주장한 사고(`/insights` 2026-07-27 Friction #2)가 정확히 "증거는 있는데 아무것도 입증하지
> 않는" 형태였다.

PASS 를 확정하기 **전에** 아래 4 검사를 통과해야 한다. 하나라도 실패하면 그 항목은 PASS 가 아니라 `[미검증]`.

| # | 검사 | Flutter 감사에서의 형태 |
| - | ---- | ---------------------- |
| 1 | **비공백** | `$FLUTTER analyze` 출력이 비었거나 에러 메시지만 있는가? 스냅샷이 빈 화면인가? |
| 2 | **활성화** | 그 측정이 대상을 한 번이라도 통과했는가? **테스트 0 개 실행 · 매치 0 건 grep 은 "위반 없음" 이 아니라 "검사되지 않음"** 이다 |
| 3 | **반증 가능성** | 규칙이 위반된 상태였다면 이 측정이 다른 결과를 냈을 것인가? 어떤 입력에도 같은 출력을 내는 측정은 oracle 이 아니다 |
| 4 | **출처** | 그 증거를 감사자가 직접 수집했는가? 구현자의 서술·주석·커밋 메시지를 인용한 것이 아닌가? |

**0 매치 판정 규칙** — `grep -r "GestureDetector" lib/` 가 0 건이라도 두 가지 의미가 있다.

- **의도된 0**: 대상 파일 목록을 먼저 세고(예: 42 개 `.dart`), 그 패턴이 알려진 위치에서 매치된다는
  것을 1 회 확인한 뒤의 0 → PASS. 근거에 "대상 42 파일 · 패턴 유효성 확인 · 매치 0" 을 적는다
- **공허한 0**: 경로가 틀렸거나 대상 파일이 0 개이거나 패턴이 절대 매치되지 않는 경우 → **측정 실패**,
  `[미검증]`

**렌더 산출물 특칙** — 감사 대상에 UI 변경이 포함되면 빈 화면·빈 목록 캡처는 PASS 증거가 아니라
검증 실패 신호다. 절차는 `references/visual-evidence-protocol.md`.

**보고 의무** — 리포트 하단에 아래 블록을 반드시 포함한다.

```text
## Evidence Validity
- 검사 대상 증거: N 건
- 무효 판정: K 건 [항목 — 실패한 검사 번호 — 사유]
- 무효 K 건은 미검증 카운터에 합산 (현재 누계: M)
```

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$FLUTTER`, `$DART`, `$PACKAGE`, `ARCH`, `HAS_DS`, `HAS_RIVERPOD`, `HAS_GO_ROUTER` 등)를 사용한다.

감지 결과에 따라 아래 체크리스트 항목의 활성화/비활성화를 결정한다:

| 감지 키 | 영향받는 검사 |
|---------|-------------|
| `ARCH = clean` | Architecture 전체 (레이어 분리, 의존 방향) |
| `ARCH = feature_first` / `flat` | Architecture를 구조에 맞게 적응 |
| `HAS_RIVERPOD` | State Management (codegen, mounted, Result) |
| `HAS_DS` | Design System (토큰, 컴포넌트 규칙) |
| i18n 라이브러리 감지 | i18n Audit (하드코딩 문자열, 키 동기화) |

## Input

`$ARGUMENTS` 파싱:

- `quick [path]` -- quick 모드 강제
- `deep [path]` -- deep 모드 강제
- `[path]` 또는 (인자 없음) -- auto 모드: 변경 파일 수로 자동 선택

## Auto 모드

인자에 `quick` / `deep` 키워드가 없으면 변경 파일 수를 기준으로 모드를 결정한다.

```bash
git diff --name-only HEAD
git diff --name-only --cached
```

- **5개 이하** -> quick 모드로 즉시 실행
- **6개 이상** -> 사용자에게 deep 모드 실행 여부를 확인한 뒤 실행

이렇게 나누는 이유: 소수 파일 변경은 빠른 체크리스트가 비용/시간 면에서 효율적이고, 대규모 변경은 관점을 분리한 병렬 감사로 빠짐없이 잡아야 하기 때문이다.

---

## Quick 모드

단일 에이전트, 비용 낮음, 지연 짧음. 변경된 파일(또는 지정된 경로)을 아래 체크리스트로 직접 검사한다.

### Architecture (ARCH에 따라 적응)

#### ARCH = clean

Clean Architecture 레이어 분리와 의존 방향을 지키지 않으면 도메인 로직이 인프라에 오염된다.

- [ ] 파일이 올바른 레이어에 위치 (data / domain / presentation)
- [ ] domain 레이어가 data / presentation을 import하지 않음
- [ ] data 레이어가 presentation을 import하지 않음
- [ ] Repository impl: 예외 -> Result/Either 변환 (raw exception 전파 금지)
- [ ] UseCase: 단일 책임, 단일 public 메서드

#### ARCH = feature_first

- [ ] feature 간 직접 import 최소화 (shared를 통해 공유)
- [ ] 각 feature 내부 구조가 일관적

#### ARCH = flat

- [ ] 관심사 분리가 최소한으로 유지되는지 (UI/로직 혼재 금지)

### Import Rules

잘못된 import 경로와 순서는 분석 도구 오류와 빌드 취약성을 유발한다.

- [ ] `lib/` 내 상대경로 import 금지 (`package:$PACKAGE/...` 전용) -- 프로젝트의 import 컨벤션이 상대경로면 이 규칙 스킵
- [ ] 순서: `dart:` -> `package:` (그룹 사이 빈 줄, 각 그룹 내 알파벳순)

### State Management (HAS_RIVERPOD일 때)

Riverpod codegen을 우회하거나 mounted 체크를 빠뜨리면 런타임 상태 오류가 발생한다.

- [ ] Provider: `@riverpod` / `@Riverpod(keepAlive: true)` codegen 사용 (프로젝트가 codegen 방식이면)
- [ ] keepAlive provider는 keepAlive provider만 참조
- [ ] async 작업 후 상태 변경 전 `ref.mounted` 확인 (Notifier 생명주기) 및 async gap 후 `context.mounted` 확인 (Widget 생명주기)
- [ ] **Riverpod 3.0**: Notifier 내부 필드로 `Timer` / `StreamSubscription` / `TextEditingController` 등 생명주기 객체를 **직접 유지하지 않음** — 2.x pseudo-singleton 동작이 폐기되어 provider rebuild 마다 Notifier 가 재생성되므로 리소스 누수 발생. 이런 객체는 별도 provider 로 분리 후 `ref.onDispose` 로 바인딩
- [ ] **Riverpod 3.0 legacy**: 신규 파일에 `StateNotifierProvider` / `StateProvider` / `ChangeNotifierProvider` 를 추가하지 않음 (legacy 분류). 기존 마이그레이션은 점진적으로 `@riverpod` / `Notifier` 기반으로 전환
- [ ] 프로젝트에 Result 타입이 있으면 양쪽 분기를 모두 처리. Result 가 Freezed sealed class 기반이면 **Dart pattern matching (switch expression) 을 권장**하되, `.when`/`.map` 사용 자체를 위반으로 보고하지 마라 — `.when`/`.map` 은 Freezed 3.0 에서 제거됐다가 **3.1.0 에서 다시 추가**됐고 최신 stable 은 3.2.5 다. 프로젝트가 이미 generated `when`/`map` 을 쓰고 있으면 **일관성 유지가 우선**이다. 지적 대상은 "한쪽 분기 미처리" 뿐 ([Freezed changelog](https://pub.dev/packages/freezed/changelog))

### State Management (HAS_BLOC일 때)

- [ ] Bloc/Cubit이 단일 책임 원칙 준수
- [ ] State 클래스가 immutable (Equatable / Freezed 사용)

### State Management (기타)

- [ ] 상태와 UI의 분리가 유지되는지

### Error Handling

타입 없는 catch와 예외 미변환은 에러 추적을 불가능하게 만든다.

- [ ] bare `catch (e)` 금지 -- 타입 명시 우선
- [ ] 경계 계층(Repository/DataSource)에서 예외 -> Failure/Error 타입 변환
- [ ] catch 블록에서 에러를 조용히 무시하지 않음

### Naming

일관된 네이밍 규칙은 레이어와 역할을 파일 이름만으로 파악 가능하게 한다.

- [ ] 프로젝트의 네이밍 규칙 준수 (Screen/Page/View/Widget 또는 프로젝트 컨벤션)
- [ ] `_widget` 접미사 사용 금지
- [ ] 폴더 네이밍이 프로젝트 컨벤션과 일치

### Design System (HAS_DS = true일 때만)

디자인 시스템 토큰과 컴포넌트 규칙을 사용해야 테마 전환과 일관성이 보장된다.

- [ ] 색상: semantic token 패턴 사용 (하드코딩 Color 금지)
- [ ] 간격: spacing 토큰 사용 (반복 하드코딩 금지)
- [ ] 모서리: radius 토큰 사용 (반복 하드코딩 금지)
- [ ] 아이콘: 프로젝트 아이콘 패키지 사용 (다른 패키지 혼용 금지)
- [ ] 인터랙션: 프로젝트의 탭 피드백 위젯(Pressable 등) 사용, GestureDetector/InkWell 직접 사용 금지
- [ ] 애니메이션: 프로젝트에 애니메이션 상수(Duration/Curve 토큰)가 있으면 사용 (하드코딩 금지)
- [ ] opacity: `.withValues(alpha:)` 사용 (`.withOpacity()` deprecated)
- [ ] 서피스/데코레이션: 프로젝트에 서피스 토큰이 있으면 사용 (gradient/border 하드코딩 금지)
- [ ] disabled 상태: Pressable 자동 처리 확인 (별도 비활성 로직 중복 금지)
- [ ] variant 패턴: 프로젝트의 variant 패턴(enum+named constructor+switch expression) 준수
- [ ] 기본 위젯 대체: `references/primitive-substitution-gate.md` §게이트 대상 의 Flutter 기본 UI 위젯을 직접 쓴 곳에 DS 대체 후보가 실재하는지 확인 (면제된 layout primitive 는 대상 아님)

### Widget Rules

Flutter 위젯 모범 사례를 지키지 않으면 오버플로, 인터랙션 불일치가 발생한다.

- [ ] nullable 슬롯: `if (x != null) ...[x!, SizedBox()]` 패턴
- [ ] overflow 가능 레이아웃: 스크롤 컨테이너 사용
- [ ] const constructor 가능한 위젯에 const 사용
- [ ] 불필요한 StatefulWidget 사용 금지

### Reusability

재사용 가능한 위젯이 feature에 갇혀 있으면 코드 중복이 누적된다.

- [ ] private 위젯 중 feature 특화 로직 없이 범용 UI 패턴인 것이 shared로 추출되지 않음
- [ ] build 메서드가 50줄 이상이면서 논리적으로 분리 가능한 서브트리가 인라인
- [ ] 다른 feature에 구조적으로 유사한 위젯이 이미 존재하는데 중복 구현
- [ ] 기본 위젯 대체 후보 미사용 (`HAS_DS`) — 위 Design System 항목과 같은 게이트. Reusability 관점에서는 "이미 있는 컴포넌트를 안 쓴 것" 이므로 여기서도 집계한다

### Performance — Environment Exclusion Checklist (성능 이슈가 감사 대상에 포함될 때만)

**앱 코드 최적화를 지적하기 전에 환경부터 배제한다.** 공식 문서는 거의 모든 성능 디버깅을
**물리 Android/iOS 기기 + profile mode** 에서 하라고 하고, debug mode 나 simulator/emulator 의
성능은 release 동작을 대표하지 않는다고 명시한다. profile mode 는 **emulator/simulator 에서
비활성**이다 (출처: <https://docs.flutter.dev/perf/ui-performance>,
<https://docs.flutter.dev/testing/build-modes>).

실측 성공 사례(`/insights` 2026-08-13 D5): 18 일간 누수된 **시뮬레이터 render host** 가 swap 을
포화시킨 것이 원인이었고, 앱 코드 최적화에 착수하기 **전에** 그것을 규명해 불필요한 리팩터를 막았다.

아래 8 항을 리포트에 기록한다 (값을 모르면 "미확인" 이라고 적는다 — 빈칸 금지):

- [ ] **profile mode** 로 측정했는가 (`--profile`). debug 수치는 성능 근거가 아니다
- [ ] **physical device** 인가 (기기 모델명 기재)
- [ ] **simulator/emulator** 사용 여부 — 사용했다면 그 사실을 리포트 서두에 명시
- [ ] 호스트의 OS uptime / **swap** / memory pressure (render host 누수·swap 포화 배제)
- [ ] **DevTools trace** export 를 확보했는가 (경로 기재)
- [ ] renderer 가 **Impeller** 인지 Skia 인지 (위 Impeller 플랫폼 체크리스트로 판정)
- [ ] target **refresh rate** (60Hz / 120Hz — frame budget 이 16ms 인지 8ms 인지 결정)
- [ ] **slowest target device** 기준인가, 개발자 최고 사양 기기 기준인가

**판정 규칙** — simulator/emulator 또는 debug mode 결과만 있으면 앱 코드 성능 병목으로
**확정하지 말고 `[미검증]`** 으로 표기하고 미검증 카운터에 합산한다. "iOS simulator 에서
jank 가 보이니 앱 버그" 는 공식 문서 기준으로 **대표성이 없는 추론**이므로 쓰지 마라.

실기기 확보가 불가능하면 simulator 결과를 "환경 의심" 등급으로만 쓰고, profile trace export 와
시스템 메모리 상태를 함께 보관한다.

---

## Deep 모드

최대 4개 전문 에이전트를 병렬로 실행한다 (haiku 모델로 실행, Widget Inspector만 sonnet). 인자가 없으면 변경된 파일 전체를 대상으로 하며, 경로가 지정되면 해당 경로만 감사한다.

인자 없을 때 파일 목록 수집:

```bash
git diff --name-only HEAD
git diff --name-only --cached
```

presentation 파일만 필터링하여 Design Review / i18n 에이전트에 전달한다.

Agent 도구를 사용하여 아래 에이전트를 **동시에** 실행한다 (조건부 에이전트 제외 시 최소 2개).

### Agent 1: Guard (아키텍처 감사)

아키텍처/임포트/네이밍/상태/에러 규칙은 서로 연관되므로 한 에이전트가 통합 검사한다.

```text
대상 파일의 규칙 준수 여부를 검사한다:

- Architecture: ARCH={감지된 아키텍처}에 맞는 레이어 분리 및 의존 방향
- Import 규칙: package:$PACKAGE/... only (프로젝트 컨벤션에 따라), dart: -> package: 순서
- State 관리: {감지된 상태관리} 패턴 준수
- 에러 처리: 타입 명시 catch, 경계 레이어 예외 변환
- 네이밍: 프로젝트 컨벤션 준수

대상 파일: [파일 목록]

각 위반 사항마다 파일:라인, 규칙, 심각도(error/warning), 수정 제안을 출력한다.
```

### Agent 2: Design Review (디자인 시스템 감사) -- HAS_DS = true일 때만

디자인 토큰과 컴포넌트 규칙은 시각적 일관성과 테마 안정성을 보장한다.

```text
대상 파일의 디자인 시스템 준수 여부를 검사한다:

- 색상: semantic token 사용 (하드코딩 Color 금지)
- 간격: spacing 토큰 사용 (반복 하드코딩 금지)
- 모서리: radius 토큰 사용 (반복 하드코딩 금지)
- 아이콘: 프로젝트 아이콘 패키지 사용
- 인터랙션: 프로젝트의 탭 피드백 패턴 준수

디자인 시스템 경로: {감지된 DS 경로}
대상 파일: [파일 목록]

각 위반 사항마다 파일:라인, 규칙, 심각도, 수정 제안을 출력한다.
```

`HAS_DS = false`이면 이 에이전트를 스킵하고 2개 에이전트만 실행한다.

### Agent 3: i18n Audit (국제화 감사) -- i18n 라이브러리 감지 시에만

하드코딩 문자열과 키 동기화 누락은 다국어 지원을 조용히 깨뜨린다.

```text
대상 파일의 국제화 규칙 준수 여부를 검사한다:

- 하드코딩된 사용자 표시 문자열 탐지 (Text('..'), hint, label 등)
- i18n 파일 간 키 동기화 누락
- 미사용 i18n 키 탐지
- 올바른 접근 패턴 ({감지된 i18n 라이브러리}의 패턴)

대상 파일: [파일 목록]
i18n 파일: {감지된 i18n 파일 경로들}

각 위반 사항마다 파일:라인, 규칙, 심각도, 수정 제안을 출력한다.
```

i18n 라이브러리가 감지되지 않으면 이 에이전트를 스킵한다.

### Agent 4: Widget Inspector (재사용성 감사) -- 항상 실행

재사용 가능한 위젯 패턴을 감지하여 추출 후보를 리포팅한다.

```text
대상 파일에서 재사용 가능한 위젯 패턴을 감지한다:

- 구조적 중복: 비슷한 위젯 트리가 2곳 이상 반복
- 비대한 build: build 메서드 50줄 이상, 분리 가능한 서브트리
- 범용 private 위젯: feature 특화 로직 없는 _WidgetName이 shared로 추출 가능
- 패턴 반복: 같은 위젯 트리 구조가 다른 이름으로 반복

대상 파일: [파일 목록]
프로젝트 shared 위젯 경로: {감지된 shared 경로}

각 추출 후보마다 파일:라인, 감지 기준, 추출 제안(위젯 이름 + 배치 경로)을 출력한다.
```

---

## Report Format

모드에 관계없이 아래 형식으로 결과를 보고한다. 이슈가 없는 항목은 "Clean" 표시.

```text
-- Audit Report ([quick|deep]) ---------------------

Architecture
  errors: N | warnings: N
  [주요 이슈 목록]

State Management
  errors: N | warnings: N
  [주요 이슈 목록]

Error Handling
  errors: N | warnings: N
  [주요 이슈 목록]

Design System                    <-- HAS_DS = true일 때만
  errors: N | warnings: N
  [주요 이슈 목록]

i18n                             <-- i18n 감지 시에만 (deep 모드)
  errors: N | warnings: N
  [주요 이슈 목록]

Reusability
  candidates: N
  [추출 후보 목록]

Performance Environment          <-- 성능 이슈가 감사 대상에 포함될 때만
  profile mode: yes|no | device: <모델명|simulator|emulator>
  swap/memory: <상태|미확인> | trace: <경로|미확보>
  renderer: Impeller|Skia | refresh rate: <Hz> | slowest target: <기기|미지정>
  [환경 배제 실패 시 해당 성능 지적은 [미검증]]

Evidence Validity
  검사 대상 증거: N | 무효: K
  [항목 — 실패한 검사 번호 — 사유]

Unverifiable
  미검증: N 건
  [항목 ID — 사유 — 시도한 fallback 단계]

----------------------------------------------------
Total: N errors, N warnings | 미검증 N 건
```

감사 결과만 보고한다. 코드를 직접 수정하지 않는다.

## Rules

- **MUST** 프로젝트 감지 결과에 따라 체크리스트를 적응시킨다 -- 모든 프로젝트에 Clean Architecture, Riverpod, 디자인 시스템이 있는 것은 아니다
- **MUST** `HAS_DS = false`이면 Design System 검사를 완전히 스킵한다 -- 디자인 시스템이 없는 프로젝트에 토큰 규칙을 강제하면 의미 없는 위반이 보고된다
- **MUST** i18n 라이브러리가 없으면 i18n Audit를 스킵한다 -- 다국어 미지원 프로젝트에 하드코딩 문자열 경고는 노이즈다
- **MUST** 감사 결과만 보고하고 코드를 직접 수정하지 않는다 -- 감사와 수정을 분리해야 사용자가 변경 사항을 통제할 수 있다
- **MUST** `$PACKAGE` 변수를 import 규칙에 사용한다 -- 패키지명을 하드코딩하면 다른 프로젝트에서 오탐이 발생한다
- **MUST** 위반 보고 시 파일:라인, 규칙, 심각도, 수정 제안을 모두 포함한다 -- 위치 없는 위반 보고는 수정 작업을 지연시킨다
- **MUST** PASS 확정 전에 Evidence Validity Gate 4 검사를 통과시킨다 -- 0 매치 grep, 0 개 테스트, 빈 캡처를 "위반 없음" 으로 읽으면 감사가 통과 도장 기계가 된다
- **MUST** 리포트에 `Evidence Validity` + `Unverifiable` 블록을 포함한다 -- 집계하지 않으면 미검증 누계 임계(2 건) 판정이 성립하지 않는다
- **MUST** 성능 지적을 하기 전에 Environment Exclusion Checklist 8 항을 기록한다 -- profile mode 가 아니거나 simulator/emulator 결과만 있으면 그 지적은 `[미검증]` 이다. 환경 배제 없이 앱 코드 최적화를 요구하면 존재하지 않는 병목을 고치게 만든다
- **MUST NOT** Primitive Substitution Gate 를 layout primitive 로 확대 적용하지 않는다 -- 면제 목록은 `references/primitive-substitution-gate.md` 가 정한다. 확대 적용된 게이트는 전건 경보가 되어 사용자가 리포트 전체를 무시하게 만든다
