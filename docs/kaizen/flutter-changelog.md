---
title: Flutter Kaizen Changelog
version: 1.4.0
last_updated: 2026-08-13
---

# Flutter Kaizen Changelog

## [2026-08-13] — Phase 5 kaizen

사실 정정 사이클이다. `.harness/.meta/evidence/phase5.md`(codex foreground 로 확보한 이 Phase 의
유일한 외부 근거) 기준으로 우리 문서가 틀렸던 세 곳을 고쳤다. **Freezed** — 6 스킬 표면 +
리서치 로그 4 줄이 "3 부터 `.when`/`.map` 제거" 를 절대 규칙으로 단정하고 있었는데, 제거는 3.0 의
breaking 이었고 **3.1.0 에서 다시 추가**됐다 (최신 stable 3.2.5). 10 줄 → 0 줄, 권장 문구를
"신규는 switch expression 우선, 기존이 generated `when`/`map` 이면 일관성 우선, `.when` 사용
자체는 결함 아님" 으로 교체했다. **Flutter stable** — 3.44.7 을 현재 stable 로 적은 3 줄을
3.47.0 으로 정정하고 3.47 Android 의존성 매트릭스(Java 17 · KGP 2.4.0 · AGP 9.1.0 · Gradle 9.3.1)를
반영, flutter-audit 의 "AGP 9 는 pre-stable" 서술을 철회했다. **Impeller** — "macOS 실험적 ·
Web/Windows/Linux 미지원" 5 줄을 macOS/Linux/Windows 는 3.47 부터 기본으로 정정하고
`--enable-impeller` opt-in 서술을 제거했다.

게이트는 4 종을 신설했다. G1 **Primitive Substitution Gate** 를
`flutter-toolkit/references/primitive-substitution-gate.md` SSOT 로 만들고
flutter-widget · flutter-screen · flutter-audit · widget-inspector 4 표면이 **인용만** 하게 했다
(목록 복제 0). 기존 E1 조항(§Enumerate-before-Act, "기존 위젯 수정이 기본값")이 있는데도 실측
REJECT `RE-02`(기본 `Divider` 사용, 기존 `IFDivider` 미재사용)가 났으므로 문장을 또 추가하지 않고
**E1 → E2 로 승급**해 대체 후보 표를 아티팩트로 남기게 했다. 게이트 대상은 의미 있는 UI 위젯
8 종(`Divider` · Button 계열 · `Chip` · `Card` · `ListTile` · `Switch` · `TextField` ·
Progress indicator)이고, layout primitive(`Text` · `Row` · `Column` · `Padding` · `SizedBox` 등)는
면제로 명시했다 — 여기까지 금지하면 게이트가 통째로 우회된다.

G2 **invalidate 경계** (flutter-provider + `docs/flutter/state/state-management.md`) —
watch / listen / invalidate / refresh 의 역할을 분리하고, 파생 provider 는 source 를
`ref.watch` + `select` 로 연결하며, mutation 후에는 영향 provider 를 열거해 `invalidate` 하도록
했다. family 전체 invalidate 는 금지다. `autoDispose` 실수명(listener 0 이 된 뒤 한 프레임 후
dispose · recompute 시 autoDispose 여부와 무관하게 기존 state 파괴)도 같이 적었고,
`Ref.onManualInvalidation()` 에는 `flutter_riverpod` 3.4.x 하한 가드를 붙였다. 실측 REJECT
`LG-02`(팔레트 변경 후 상세 화면이 캐시된 이전 색을 계속 표시) 대응이다.

G3 **위젯 테스트 하네스** (flutter-test + `docs/flutter/quality/testing.md`) — `ProviderScope`
루트 + `tester.container()` 를 기본형으로 두고, unit 은 `ProviderContainer.test()`(테스트 간 공유
금지, autoDispose 는 `container.listen` 으로 붙잡기)로 분리했다. 매핑·variant 전수 coverage
조항도 넣었다(REJECT `LG-01` "16종 매핑 중 2종만 검증" 인용). G4 **성능 환경 배제**
(flutter-audit + `docs/flutter/quality/performance.md`) — Environment Exclusion Checklist 8 항과
"simulator/emulator/debug 단독 결과는 `[미검증]`" 판정 규칙을 도입했다. 18 일 누수된 시뮬레이터
render host 가 호스트 swap 을 포화시킨 것을 앱 코드 최적화 **전에** 규명한 성공 사례(insights D5)를
절차로 승격한 것이다. 함께 flutter-audit 이 Phase 3 정본 §Canonical User-Reported Failure Protocol
을 인용만 하도록 소비면을 붙였다(임계값·상태어 재정의 0).

검증은 23 조건 전부 실행 증거를 남겼고 zsh · bash 출력 diff 0, 음성 대조 3 종(3.1.0 토큰 제거 시
6 건 · 3.4 가드 제거 시 2 건 · 정정 마커 1 개 제거 시 1 건 검출), validate-plugin flutter-toolkit
8/8 OK 다. QA 는 blocking 1 건으로 REJECT 됐다 — 계약 AP-03 의 오라클이 bare code fence 를 세면서
닫는 펜스까지 위반으로 집계하는 나이브판이었고 실측 6 건이 전부 정상 dart 블록의 닫는 펜스였다.
조문을 "여는 펜스만 센다" 로 고쳐 읽는 amendment 는 `relaxing · unanchored` 라 PASS 근거가 될 수
없으므로(Phase 4 AM-01 전례) 대신 구현을 고쳤다: 세 문서의 코드 블록 6 개를 백틱 4 개 펜스로
전환해 원 측정문을 문자 그대로 충족시키고 APPROVE 를 받았다. 계약 측정문 퇴행과 그 근본원인
(skill-design-guide 가 아직 나이브 grep 을 검증법으로 가르치는 것)은 Scope 밖이라
`.harness/sprint-amendments-kaizen-phase5-flutter-gates.md` AM-01 / AM-02 에 핸드오프로 남겼다.

## [2026-07-27] — Phase 5 kaizen

시각 증거 규약(E2)을 UI 생성 스킬 5종(widget/screen/skeleton/transition/responsive)에 전수 도입하고
`references/visual-evidence-protocol.md` 를 SSOT 로 신설했다. 인사이트 Friction #2(시각·런타임 검증
불신)가 이번 사이클 신규 최상위 신호이고 flutter 가 진앙이었다 — 빈 화면을 스냅샷 근거로 "정상
렌더링"이라 반복 주장한 사고. MCP 도구명은 하드코딩하지 않고 project-detection Step 8 의 감지
ladder 로 일반화했다. flutter-audit 에 canonical 5조항 + Evidence Validity Gate 복제,
widget-inspector 의 "Clean — 추출 후보 없음" vacuous pass 차단.

실측 버그 3건 수정: flutter-test 의 `$DART test` 는 widget test 를 실행할 수 없음 ·
무출처 Gotcha("출처: community 2025-12")를 실측 URL 로 교체 · flutter-provider 를 신규생성
전용으로 명시(digest `mismatched-provider-skill` 대응). flutter-run 은 codegen 산출물과 수기
변경을 분리 보고하도록 했다(글로벌 REJECT AR-01).

## [2026-06-05] — Phase 5 kaizen

flutter-feature/flutter-screen 에 과잉설계 방지 Gotcha 추가(요청 범위 넘는 레이어/provider/state 임의 스캐폴딩 금지, Friction #3).


> flutter-kaizen에 의한 flutter-toolkit 변경 이력을 기록한다.

## [2026-05-07] — Phase 5 kaizen (Phase 1 v1.3.0 신규 원칙 흡수)

- flutter-toolkit/README.md 에 cross-kit-principles 매트릭스 cross-reference 섹션 신규
- plugin.json v0.5.2 → v0.5.3 patch bump
- 매핑: flutter-audit / flutter-extract ANALYZE ↔ Pre-Edit Batch Audit, widget-inspector self-check ↔ Self-Evaluator Audit, PostToolUse dart format/analyze ↔ Hook-Triggered Auto-Correction
- 단일 진실 원천(SSOT): `harness/references/cross-kit-principles.md` v1

## [2026-04-11] - Phase 5 research-mode kaizen

### 변경 유형: patch (2026 Flutter 생태계 최신 패턴 반영)

### 변경 범위 (flutter-toolkit v0.5.0 → v0.5.1)

- **flutter-provider**: Riverpod 3.0 Notifier 재생성 라이프사이클 Gotcha 4건 추가 — Notifier 내부 Timer/Controller 금지, legacy provider 분류, `==` 기반 알림 필터링 (StreamProvider/StreamNotifier 영향), Freezed sealed Result → switch expression 병행 권장
- **flutter-hooks**: `context.mounted` async gap 체크 필수 Gotcha 추가 — showDialog / Navigator.push / `Future<T>` 반환 후 context 재사용 시 필수 검사, `ref.mounted` vs `context.mounted` 구분 설명, build() 100줄 이하 권장 노트 (금지 아님)
- **flutter-screen**: go_router `StatefulShellRoute.indexedStack` + `StatefulShellBranch` + `preload: true` 패턴 섹션 신규 — 2026 기준 go_router 공식 권장 패턴, 완전한 코드 예시 포함
- **flutter-error**: Freezed 3.0 sealed Result → switch expression 패턴 C' 코드 예시 추가 — `when`/`map` 제거 마이그레이션 대응
- **flutter-audit**: State Management 체크리스트 3건 확장 — Notifier 내부 Timer/StreamSubscription/TextEditingController 금지, Freezed sealed Result switch expression 병기, freezed changelog 링크
- **widget-inspector** 에이전트: Props 번들링 위반 감지 기준 5번 신규 — HAS_FREEZED + HAS_HOOKS 동시 조건, Named constructor variant 면제
- **references/project-detection.md**: Step 2b Makefile 기반 monorepo 감지 섹션 신규 — 타겟 목록 (app-run / app-preflight 포함), `$MAKE` 변수, HAS_MAKEFILE 스킬 매핑 테이블, fit-pal monorepo 출처
- **references/flutter-ai-rules.md**: 2026 생태계 노트 섹션 신규 6 서브섹션 — Riverpod 3.0 / Freezed 3.0 / go_router / Flutter 3.29 / flutter_hooks / Makefile, 전 항목 공식 출처 URL 명시

### QA 결과

Phase 5 sprint-contract 16 조건 모두 L3 PASS, iter 1 APPROVE. 독립 qa-evaluator 서브에이전트 평가로 검증. validate-plugin 7 OK, bare fence 0 건.

### 주요 리서치 소스

- [Riverpod 3.0 migration](https://riverpod.dev/docs/3.0_migration) — Notifier 재생성 라이프사이클 변경
- [Freezed changelog](https://pub.dev/packages/freezed/changelog) — 3.0 abstract/sealed 필수, when/map 제거
- [go_router StatefulShellRoute](https://pub.dev/documentation/go_router/latest/go_router/StatefulShellRoute-class.html) — preload 파라미터
- [Flutter 3.29 release notes](https://docs.flutter.dev/release/release-notes/release-notes-3.29.0) — context.mounted / breaking changes
- [flutter_hooks](https://pub.dev/packages/flutter_hooks) — 2026 권장 패턴
- Hub apps (iter 2 22/22) + fit-pal (iter 2 33/33) sprint-feedback 실무 검증

### Before/After 요약

| 영역 | Before | After |
| ---- | ------ | ----- |
| Riverpod Gotchas | 기본 `@Riverpod` codegen 안내 | 3.0 Notifier 라이프사이클 + 4건 경고 추가 |
| Hooks | context.mounted 언급 없음 | async gap 후 필수 체크 + ref.mounted 구분 |
| Screen Router | 기본 go_router 예시 | StatefulShellRoute + preload 패턴 섹션 |
| Widget Inspector | 4 감지 기준 | 5 감지 기준 (Props 번들링 포함) |
| project-detection | Makefile 감지 없음 | Step 2b Makefile monorepo 감지 |

---

---

## [0.5.0] - 2026-03-30

### 변경 유형: minor (skill-prompt, new-skill, eval)

### 연구 기반

- [Flutter 3.41 Breaking Changes](https://docs.flutter.dev/release/breaking-changes) — semantics 매처 변경, variable font weight
- [AToMIC 논문](https://arxiv.org/abs/2510.18861) — LLM 기반 Flutter 테스트 자동 생성
- [Flutter AI Rules](https://raw.githubusercontent.com/flutter/flutter/main/docs/rules/README.md) — Arrange-Act-Assert, Fake/Stub 우선

### 변경 내역

- **flutter-audit Gotcha**: containsSemantics → isSemantics 테스트 매처 변경
- **flutter-widget Gotcha**: FontWeight가 variable font weight axis 제어
- **flutter-test 신규 생성**: unit/widget/integration 테스트 자동 생성 스킬 v0.1
- **evals.json**: flutter-test eval 케이스 추가 (id: 18)

### 버전 판단 근거
> 신규 스킬 초안 생성 + 스킬 프롬프트 변경 = minor

## [0.4.0] - 2026-03-30

### 변경 유형: minor (skill-prompt, reference, detection)

### 연구 기반

- [Flutter Official Architecture Guide](https://docs.flutter.dev/app-architecture/guide) — MVVM 패턴 공식 권장
- [Riverpod 3.0 Newsletter](https://codewithandrea.com/newsletter/september-2025/) — `.valueOrNull` → `.value`, offline persistence
- [Flutter 3.38 Release Notes](https://docs.flutter.dev/release/release-notes/release-notes-3.38.0) — WidgetState 마이그레이션, PredictiveBack 기본 전환
- [Flutter Official AI Rules](https://raw.githubusercontent.com/flutter/flutter/main/docs/rules/README.md) — LLM 코드 생성 공식 가이드라인

### 변경 내역

- **flutter-toolkit/references/flutter-ai-rules.md**: 신규 생성 — Flutter 공식 AI rules 핵심 요약
  - Before: 공식 AI rules 참조 없음
  - After: 위젯 패턴, 상태관리, 아키텍처, Do's/Don'ts 요약 문서
  - 근거: [Flutter AI Rules](https://raw.githubusercontent.com/flutter/flutter/main/docs/rules/README.md)

- **flutter-toolkit/skills/flutter-provider/SKILL.md**: Gotchas 2개 추가
  - Before: Riverpod 버전 변경 미언급
  - After: `.valueOrNull` → `.value` 마이그레이션, offline persistence experimental 경고
  - 근거: [Riverpod 3.0](https://codewithandrea.com/newsletter/september-2025/)

- **flutter-toolkit/skills/flutter-widget/SKILL.md**: Gotchas 2개 추가
  - Before: MaterialState → WidgetState 마이그레이션 미언급
  - After: WidgetState 마이그레이션 안내, private Widget 클래스 합성 패턴 강조
  - 근거: [Flutter 3.38](https://docs.flutter.dev/release/release-notes/release-notes-3.38.0), [AI Rules](https://raw.githubusercontent.com/flutter/flutter/main/docs/rules/README.md)

- **flutter-toolkit/skills/flutter-screen/SKILL.md**: Gotcha 1개 추가
  - Before: PredictiveBack 기본 전환 미언급
  - After: Android에서 PredictiveBack 기본 전환과 커스텀 전환 충돌 가능성 경고
  - 근거: [Flutter Breaking Changes](https://docs.flutter.dev/release/breaking-changes)

- **flutter-toolkit/references/project-detection.md**: MVVM 패턴 추가
  - Before: clean, feature_first, flat 3가지만
  - After: mvvm 패턴 추가 (View ↔ ViewModel 1:1, Repository, Service)
  - 근거: [Flutter Architecture Guide](https://docs.flutter.dev/app-architecture/guide)

### 버전 판단 근거
> 스킬 프롬프트 변경(Gotchas) + 새 reference + detection 로직 변경 = minor
