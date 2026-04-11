# Sprint Contract — Phase 5 Kaizen Research Mode (flutter-toolkit)

Feature: flutter-toolkit 18개 스킬 + widget-inspector + references 2026 최신 Flutter/Riverpod/Freezed/go_router 트렌드 반영 카이젠
Created: 2026-04-11
Branch: kaizen/2026-04-11-research
Iteration: 1

## Context

Phase 1~4 완료 (commit 4587154 → 7586200). Phase 5는 flutter-toolkit 플러그인의 18개 스킬, `agents/widget-inspector.md`, `references/project-detection.md` + `references/flutter-ai-rules.md`를 2026 최신 Flutter 생태계(Flutter 3.29+, Riverpod 3.0, Freezed 3.0, go_router StatefulShellRoute preload)에 맞춰 갱신한다.

데이터 풀 §2 Hub 외부 프로젝트 피드백(fit-pal, apps)에서 확인된 실사용 패턴:

- **apps**: `HookWidget + @freezed Props` 기본 패턴, `context.mounted` async gap 체크, `useState<T>`, `context.pop<T>()`, `AdmMessageBoxType.custom` 재사용, build() 100줄 이하, pre-existing warning 구분
- **fit-pal**: Makefile 기반 monorepo (`make app-run`, `make app-preflight`), `dart-define-from-file=.dart_defines.json`, `--observatory-port=8181`, fvm 강제

외부 리서치 (WebSearch, 2026-04-11):

- **Riverpod 3.0**: `Ref.mounted` 공식 패턴, Notifier 재생성 라이프사이클 (2.x pseudo-singleton 폐기 — Timer/Controller 내부 유지 금지, 별도 provider + `ref.onDispose`), `StateNotifierProvider`/`StateProvider`/`ChangeNotifierProvider` legacy 분류, Ref 타입 파라미터 제거, `==` 기반 알림 필터링
- **Freezed 3.0**: `@freezed abstract class` / `@freezed sealed class` 필수, `.when`/`.map` 제거 → Dart pattern matching 사용, List/Map/Set Unmodifiable 자동 변환
- **go_router**: `StatefulShellRoute` + `StatefulShellBranch.preload` 지원, `notifyRootObserver`, 바텀 네비 스테이트풀 네스티드 네비 표준 패턴
- **Flutter 3.29+**: HTML 렌더러 제거, 스크립트 기반 Gradle plugin 제거, DisplayP3 (3.27+), Impeller OpenGL ES 확장
- **flutter_hooks**: HookConsumerWidget 통합, useMemoized 데이터 페칭 중복 방지, useEffect cleanup 반환 함수 필수

## 리서치 소스 (URL 필수)

1. <https://riverpod.dev/docs/3.0_migration> — Riverpod 2.0 → 3.0 Migration Guide
2. <https://riverpod.dev/docs/whats_new> — What's new in Riverpod 3.0
3. <https://pub.dev/packages/riverpod/changelog> — riverpod changelog
4. <https://pub.dev/packages/flutter_riverpod/changelog> — flutter_riverpod changelog
5. <https://pub.dev/packages/freezed/changelog> — Freezed 3.0 changelog (abstract/sealed 필수, when/map 제거)
6. <https://pub.dev/documentation/go_router/latest/go_router/StatefulShellRoute-class.html> — StatefulShellRoute 공식 API
7. <https://pub.dev/packages/go_router/changelog> — go_router changelog (preload, notifyRootObserver)
8. <https://docs.flutter.dev/release/release-notes/release-notes-3.29.0> — Flutter 3.29 release notes
9. <https://docs.flutter.dev/release/breaking-changes> — Flutter breaking changes index
10. <https://pub.dev/packages/flutter_hooks> — flutter_hooks package
11. <https://riverpod.dev/docs/concepts/about_hooks> — Riverpod + flutter_hooks 통합
12. Context7 `/rrousselgit/riverpod/riverpod-v3.0.2` (quota 초과 — resolve만 성공, query-docs fallback → WebSearch)

Hub 외부 프로젝트 피드백:

- `/Users/jackson/Hub/10_Dev/apps/.harness/sprint-feedback.md` (AdmHtmlEditorMessageBoxWidget APPROVE iter 2, 22/22 PASS)
- `/Users/jackson/Hub/10_Dev/fit-pal/.harness/sprint-feedback.md` (Monorepo Makefile APPROVE iter 2, 33/33 PASS)
- `/Users/jackson/Hub/10_Dev/apps/.harness/history/20260411-2110-sprint-contract.md` (HookWidget + @freezed Props + fvm + setState 금지 + new 금지)

## 완료 조건 (Sprint Contract)

### Provider (Riverpod 3.0)

- [ ] PR-01: `flutter-toolkit/skills/flutter-provider/SKILL.md` Gotchas 에 Riverpod 3.0 Notifier 재생성 라이프사이클 경고 추가 — Timer/Controller 를 Notifier 내부 필드로 유지 금지, 별도 provider + `ref.onDispose` 분리 요구
- [ ] PR-02: `flutter-provider/SKILL.md` Gotchas 에 Riverpod 3.0 `StateNotifierProvider` / `StateProvider` / `ChangeNotifierProvider` legacy 분류 명시 — 신규 코드는 `@riverpod` / Notifier 기반 권장
- [ ] PR-03: `flutter-provider/SKILL.md` Gotchas 에 Riverpod 3.0 `==` 기반 알림 필터링 + `StreamProvider`/`StreamNotifier` 영향 경고 추가
- [ ] PR-04: `flutter-provider/SKILL.md` Rules 또는 Gotchas 에 "프로젝트 Result 타입이 Freezed sealed 기반이면 `.when` 대신 Dart pattern matching (switch expression) 사용" 가이드 추가 — Freezed 3.0 when/map 제거 대응

### Hooks (flutter_hooks + context.mounted)

- [ ] HK-01: `flutter-hooks/SKILL.md` Gotchas 에 async gap 후 `context.mounted` 체크 필수 명시 추가 — apps 피드백 UI-06/AR-01 패턴 (showDialog/`Future<T>` 반환 후 context 재사용 시)
- [ ] HK-02: `flutter-hooks/SKILL.md` 어딘가에 build() 100줄 이하 권장 노트 추가 — apps CG-12 기반, 권장 표현 (금지 아님)

### Screen / Router (go_router 2026)

- [ ] SC-01: `flutter-screen/SKILL.md` 라우트 등록 섹션에 StatefulShellRoute + StatefulShellBranch 분기 추가 — 바텀 네비게이션 탭(Screen 타입) 스테이트풀 네스티드 네비 용도
- [ ] SC-02: `flutter-screen/SKILL.md` 에 `StatefulShellBranch.preload` 파라미터 언급 추가 (go_router 최신 preload 지원)

### Error handling (Freezed 3.0 대응)

- [ ] ER-01: `flutter-error/SKILL.md` Result.when 패턴 예시에 "프로젝트 Result 타입이 Freezed sealed 기반이면 Dart pattern matching (switch expression) 으로 작성" 주석 추가 — Freezed 3.0 when 제거 대응

### Audit (Riverpod 3.0 + Freezed 3.0)

- [ ] AU-01: `flutter-audit/SKILL.md` State Management 체크리스트에 Riverpod 3.0 Notifier 내부 Timer/Controller 금지 항목 추가
- [ ] AU-02: `flutter-audit/SKILL.md` Result.when 체크 항목에 "Freezed sealed 기반이면 switch expression 사용" 병기

### Widget Inspector

- [ ] WI-01: `agents/widget-inspector.md` 감지 기준에 "HookWidget 생성 시 @freezed Props 번들링 준수 여부" 추가 — HAS_FREEZED + HAS_HOOKS 프로젝트에서 개별 파라미터 나열을 리포트 항목으로 포함

### References (Project Detection + flutter-ai-rules)

- [ ] RD-01: `references/project-detection.md` 에 Makefile 기반 monorepo 감지 추가 — `Makefile` 존재 + `app-run` / `app-preflight` / `server-run` 타겟 감지 시 `HAS_MAKEFILE = true` + `$MAKE` 변수 제공 (fit-pal 피드백)
- [ ] RD-02: `references/project-detection.md` 에 `HAS_MAKEFILE` 을 의존성 감지 테이블 또는 별도 섹션으로 추가 + flutter-preflight/flutter-run 우선 사용 연동 명시
- [ ] RD-03: `references/flutter-ai-rules.md` 에 Riverpod 3.0 / Freezed 3.0 / go_router StatefulShellRoute 관련 2026 생태계 노트 추가 + "최종 확인" 날짜를 2026-04-11 로 갱신

## 규칙 / 안티패턴 (이 스프린트 전용)

- Phase 1~4 파일(`harness/**`) 수정 금지
- `.harness/sprint-contract.md` 외의 modified 파일은 본 카이젠 결과물만 허용
- flutter-toolkit `plugin.json` 수정 금지 (Final Phase 에서 일괄 bump)
- V6 bare code fence 0건 유지 (이전 Phase 5 residue 학습 — 언어 힌트 필수)
- markdownlint MD032 / MD060 / MD028 / MD034 준수
- 한국어 톤 유지, 반복 실수 방지 Gotcha 위주

## 검증 (Regression)

- [ ] VG-01: `python3 scripts/validate-plugin.py` 7 OK — baseline 유지
- [ ] VG-02: `python3 scripts/sync-docs.py --check-only` — 동기화 차이 없음 (또는 갱신 완료)
- [ ] VG-03: 변경된 markdown 파일에 bare code fence 0건

## Definition of Done

모든 13개 기능 조건 + 3개 검증 조건 = **16 조건 PASS**.

REJECT 재평가 최대 3회. 실패 시 iteration bump.
