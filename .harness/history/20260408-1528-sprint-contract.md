---
feature: "rust-kit Hexagonal Architecture 적용 + QA REJECT 해결"
created: "2026-04-07 01:30"
complexity: "complex"
conditions: 18
---

## Skill

- [ ] SK-01: 생성형 스킬(rust-api, rust-model, rust-service, rust-auth, rust-middleware, rust-grpc) 각각의 Process에 별도 Step으로 "trait(포트) 정의 생성" Step과 "impl(어댑터) 구현 생성" Step이 순서대로 존재한다
- [ ] SK-02: Given rust-init 스킬이 호출될 때, Then 생성되는 디렉토리 구조에 ports/와 adapters/ 레이어가 기본 포함된다
- [ ] SK-03: rust-service와 rust-api의 예시 코드에서 비즈니스 로직이 인프라를 직접 참조하는 코드가 없고, trait 파라미터/의존성 주입 패턴이 사용된다
- [ ] SK-04: project-detection.md에 ports/ + adapters/ 디렉토리 존재 시 ARCH 감지에 hexagonal 값이 추가되어 있다
- [ ] SK-05: 포트 목록(DB, Storage, Messaging, Auth, Email, Payment, Inference, Job) 8개가 docs/rust/fundamentals/hexagonal-architecture.md에 정의되어 있다

## Script

- [ ] SC-01: .claude/skills/create-kit/SKILL.md의 Gotcha에 "언어 전용 워크플로우 킷은 다종 스킬 패턴 허용" 예외가 추가되어 있다

## Error

- [ ] ER-01: ops/ 디렉토리가 3개 문서(docker.md, ci-cd.md, observability.md)로 스펙 디렉토리 구조와 매핑 테이블 모두에서 일치한다
- [ ] ER-02: Tokio 버전이 Codex 리서치로 확인된 값으로 스펙에 반영되어 있고, 해당 버전 옆에 확인 날짜가 주석으로 명시되어 있다

## Architecture

- [ ] AR-01: docs/rust/fundamentals/hexagonal-architecture.md 리서치 문서가 추가되어 있고, frontmatter(title, version, last_updated)를 포함한다
- [ ] AR-02: 리서치 문서 총 수가 docs/superpowers/specs/2026-04-06-rust-kit-design.md의 디렉토리 구조, 매핑 테이블, docs/superpowers/plans/2026-04-06-rust-kit.md의 Task 목록에서 모두 동일한 값이다
- [ ] AR-03: rust-init의 workspace_service 구조에 ports/ + adapters/ 디렉토리가 포함되어 있다
- [ ] AR-04: rust-init의 modular 구조에도 ports/ + adapters/ 모듈이 포함되어 있다

## Anti-patterns

- [ ] AP-01: rust-kit/의 SKILL.md 파일들에서 크레이트 버전 문자열을 하드코딩하지 않는다
- [ ] AP-02: 스펙(2026-04-06-rust-kit-design.md)과 계획(2026-04-06-rust-kit.md) 간 리서치 문서 수, 스킬 수가 일치한다

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 기존 references/ 문서(backend-kit, flutter-toolkit의 패턴)와 중복되는 내용을 새로 작성하지 않고 참조했다

## Diagnostics

- [ ] DG-01: bash -n scripts/release.sh 워닝 0개
- [ ] DG-02: IDE diagnostics 워닝/인포 0개
- [ ] DG-03: 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개
