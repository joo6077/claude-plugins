# WASM Decision Catalog — Pointer

The authoritative WASM decision catalog lives at the repo-level development doc:

**`docs/react/wasm-catalog.md`** (521 lines)

Contents:
- §1 WASM 권장 카테고리 9 항목 (이미지, 압축, ML, SQL, 파서, 수치, 집계, 암호화)
- §2 WASM 비권장 카테고리 10 항목 (UI, 폼, JSON, 문자열, Web Crypto small, 고빈도 콜백, tiny 함수, 애니메이션, 네트워크, event bus)
- §3 Boundary cost 수치 (JS↔WASM call ~50-100ns, 문자열 마샬링 600-2500ns)
- §4 SIMD + Threads 브라우저 지원 현황
- §5 카탈로그 미스 시 5개 휴리스틱
- §6 5 가지 오해 교정
- §10 Rust 크레이트 매핑
- §11 마이그레이션 체크리스트

## 사용처

- `/react-wasm` 스킬 — 이식 판정의 1차 소스
- `/react-audit` Performance 카테고리 — 안티패턴 검출 기준
- `/react-kaizen` dev 스킬 — 카탈로그 주기 갱신

## 동기화 정책

`react-kit/` 은 배포 대상, `docs/react/` 는 레포 개발용. 두 위치의 sync 는 향후 `/react-kaizen` 스킬이 담당. 초판은 이 포인터 문서만 두고, 스킬 실행 시 런타임에 `docs/react/wasm-catalog.md` 경로를 읽어오는 방식으로 처리 (user repo 가 아니라 claude-plugins 레포 내부 참조).

**주의**: 이 파일은 플러그인 사용자가 아니라 스킬 내부 로직의 참조 포인터다. 플러그인이 설치된 사용자 프로젝트에서는 이 파일이 읽을 일이 없다.
