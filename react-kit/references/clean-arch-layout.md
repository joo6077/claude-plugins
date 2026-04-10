# Clean Architecture Layer Layout

react-kit 의 모든 스킬이 공유하는 레이어 배치 + 의존성 방향 규칙.

## 레이어 정의

| 레이어 | 경로 | 의존성 방향 |
|--------|------|------------|
| **domain** | `src/domain/` | 외부 의존성 **0개**. 오직 순수 TS + Zod |
| **data** | `src/data/` | `domain/` 만 알고, `presentation/`, `infrastructure/` 모름 |
| **presentation** | `src/presentation/` | `domain/`, `data/repositories/`, `shared/`, `infrastructure/` 알 수 있음 |
| **infrastructure** | `src/infrastructure/` | 브라우저/Tauri/OS API 래퍼. `domain/` 만 참조 가능 |

## 하위 디렉토리

### domain
- `entities/` — Zod 스키마 + `z.infer` 파생 타입
- `usecases/` — 함수 시그니처 (`Promise<Result<T, Failure>>`)
- `failures/` — `<Feature>Failure` discriminated union
- `types/` — 공유 타입 (WASM 경계 포함)

### data
- `datasources/remote/` — fetch + Zod parse (boundary 검증)
- `datasources/local/` — localStorage, IndexedDB
- `datasources/wasm/` — Comlink Worker 래퍼 + WASM 바인딩
- `models/` — DTO 스키마 + 도메인 변환 함수
- `repositories/` — UseCase 구현 (의존성 주입)

### presentation
- `features/<feature>/` — components/, hooks/, store.ts, screens/, index.ts
- `shared/components/ui/` — shadcn 원본 (수정 금지)
- `shared/components/` — 공용 위젯
- `shared/components/skeletons/` — 공용 skeleton
- `shared/hooks/` — useDrag, useDrop, useSortable, 기타 공용 훅
- `shared/stores/` — cross-feature Zustand 스토어 (drag-store 등)
- `shared/lib/` — cn 유틸, display-failure, view-transition 래퍼
- `routes/` — TanStack Router 파일 기반 라우트
- `styles/` — globals.css (@theme @keyframes)

### infrastructure
- `tauri/` — `@tauri-apps/*` 유일한 import 위치, `isTauri()` 가드 래퍼
- `storage/` — localStorage 어댑터
- `http/` — fetch 클라이언트 (Zod 검증 + Result 반환)
- `i18n/` — Lingui setup + locale catalog

## 금지 import 방향

- ❌ `domain/` 이 `data/`, `presentation/`, `infrastructure/` 중 아무거나 import
- ❌ `data/` 가 `presentation/` 또는 `infrastructure/tauri/` import
- ❌ `presentation/features/a` 가 `presentation/features/b` 직접 import
- ❌ `presentation/` 이나 `data/` 에서 `@tauri-apps/*` 직접 import (`infrastructure/tauri/` 경유 필수)
- ❌ 모든 상대 경로 (`'../../../'`) — absolute `@/` import 만 허용
- ❌ `export default` 컴포넌트 — named export 로 통일

## `/react-audit` 감사 규칙

이 레퍼런스의 금지 규칙은 G6 `/react-audit` 의 Architecture 카테고리 grep 패턴으로 번역되어 빌드 게이트급 실패로 강제된다. 상세 패턴은 `docs/react/kit-design/g6-build-audit.md` §4.5 Architecture 섹션 참조.

## 관련 문서

- `docs/react/kit-design/g1-scaffolding.md` — 스캐폴딩 시 디렉토리 생성
- `docs/react/kit-design/g2-state-data.md` — 데이터 레이어 패턴
- `docs/react/kit-design/g6-build-audit.md` — 경계 위반 감사
