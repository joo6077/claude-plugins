---
version: 1.0.0
last_updated: 2026-04-11
---

# Flutter Kit Research Log

> Flutter 관련 리서치 로그. `docs/kaizen/flutter-research-log.md` 와 동일 내용을 per-kit view 로 보관한다.
> kaizen-orchestrator 의 per-kit research-log 정책 (Step 12) 에 따라 생성됨.
> 상세 소스/인사이트는 `docs/kaizen/flutter-research-log.md` 를 참조.

---

## 2026-04-11

**트리거:** kaizen-orchestrator Phase 5 (research-mode rerun)

### 조사한 소스 요약

| # | 제목 | URL | 유형 | 결과 |
| - | ---- | --- | ---- | ---- |
| 1 | Riverpod 3.0 migration | <https://riverpod.dev/docs/3.0_migration> | 공식 | 채택 |
| 2 | Freezed 3.0 changelog | <https://pub.dev/packages/freezed/changelog> | 공식 | 채택 (abstract/sealed) |
| 3 | go_router StatefulShellRoute | <https://pub.dev/documentation/go_router/latest/go_router/StatefulShellRoute-class.html> | 공식 | 채택 |
| 4 | Flutter 3.29 release notes | <https://docs.flutter.dev/release/release-notes/release-notes-3.29.0> | 공식 | 채택 |
| 5 | flutter_hooks | <https://pub.dev/packages/flutter_hooks> | 공식 | 채택 |
| 6 | fit-pal / apps sprint-feedback | (internal) | ground truth | 채택 |

### 주요 인사이트 (요약)

- **Riverpod 3.0 Notifier 라이프사이클**: 재생성 시 leak 방지를 위해 Notifier 내부 Timer/Controller 금지, `ref.onDispose` 로 분리
- **Freezed 3.0 sealed + Dart 3 switch expression**: `when`/`map` 제거 마이그레이션 대응
- **go_router StatefulShellRoute + preload: true**: 탭 네비게이션 공식 권장 패턴
- **context.mounted vs ref.mounted**: async gap 후 context 재사용 시 필수 가드 구분
- **Makefile monorepo 감지**: fit-pal/apps 에서 make 기반 표준 타겟 감지 → project-detection Step 2b
- **Props 번들링 (widget-inspector)**: HAS_FREEZED + HAS_HOOKS 프로젝트에서 위젯 파라미터 6+ 개 → `@freezed Props` 권장

### 전체 기록

- `docs/kaizen/flutter-research-log.md` (마스터 로그)
- `docs/kaizen/flutter-changelog.md` (변경 이력)

### PR

- <https://github.com/joo6077/claude-plugins/pull/6>
