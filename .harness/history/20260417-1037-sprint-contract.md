---
feature: "테스트 스킬 3종 추가 + 테스트 인프라 구축"
created: "2026-04-12 14:30"
complexity: "complex"
conditions: 18
---

## Skill
- [ ] SK-01: backend-kit/skills/backend-test/SKILL.md가 존재하며 frontmatter에 name, description, argument-hint, user-invocable 필드가 포함된다 [structural]
- [ ] SK-02: infra-kit/skills/infra-test/SKILL.md가 존재하며 frontmatter에 name, description, argument-hint, user-invocable 필드가 포함된다 [structural]
- [ ] SK-03: design-kit/skills/design-test/SKILL.md가 존재하며 frontmatter에 name, description, argument-hint, user-invocable 필드가 포함된다 [structural]
- [ ] SK-04: 3개 테스트 스킬 모두 Gotchas 섹션에 최소 5개 이상 항목이 있다 [structural]
- [ ] SK-05: 3개 테스트 스킬 모두 Process 섹션에 프로젝트 감지 → 대상 분석 → 기존 패턴 탐색 → 테스트 생성 → 실행 검증 단계가 포함된다 [structural]
- [ ] SK-06: backend-test는 스택 무관 — pytest/jest/JUnit/go test 등 프로젝트 감지 결과에 따라 분기하는 로직이 Process에 명시된다 [goal]
- [ ] SK-07: infra-test는 IaC 테스트(Terraform validate, Pulumi test, Ansible lint 등)와 CI 파이프라인 테스트를 커버하는 분기가 Process에 명시된다 [goal]
- [ ] SK-08: design-test는 디자인 토큰 검증, 접근성 테스트(WCAG), 시각 회귀 테스트를 커버하는 분기가 Process에 명시된다 [goal]

## Script
- [ ] SC-01: scripts/run-evals.py 또는 동등한 테스트 러너 스크립트가 존재하며 evals.json을 읽어 assertion을 검증할 수 있다 [goal]
- [ ] SC-02: .github/workflows/ 디렉토리에 CI 워크플로우 YAML이 존재하며 validate-plugin.py와 테스트 러너를 실행하는 job이 정의된다 [structural]
- [ ] SC-03: package.json의 test 스크립트가 stub이 아닌 실제 테스트 커맨드를 실행한다 [goal]
- [ ] SC-04: react-kit/evals/test-fixtures/ 내 5개 디렉토리 중 최소 2개에 .gitkeep이 아닌 실제 픽스처 파일이 존재한다 [structural]

## Error
- [ ] ER-01: 테스트 러너 스크립트가 evals.json 파싱 실패 시 명확한 에러 메시지와 비정상 종료 코드를 반환한다 [goal]
- [ ] ER-02: CI 워크플로우가 테스트 실패 시 PR을 블로킹한다 (fail-fast 또는 continue-on-error: false) [structural]

## Architecture
- [ ] AR-01: 3개 테스트 스킬이 각 플러그인의 기존 스킬 네이밍 패턴을 따른다 (backend-test, infra-test, design-test) [exact]
- [ ] AR-02: 각 플러그인의 evals.json에 새 테스트 스킬의 eval 항목이 추가된다 [structural]
- [ ] AR-03: sync-evals.py의 대상 킷 목록에 backend-kit, infra-kit가 포함된다 [exact]
- [ ] AR-04: README.md 스킬 테이블에 3개 테스트 스킬이 등록된다 (sync-docs.py 실행 또는 수동) [goal]

## Anti-patterns
- [ ] AP-03: bare code fence 금지 — 모든 코드 블록에 언어 힌트 필수
- [ ] AP-04: SKILL.md frontmatter에서 name 필드 누락 금지

## Reusability
- [ ] RE-01: private 일회용 컴포넌트가 없다
- [ ] RE-02: 기존 공용 컴포넌트를 재사용한다

## Diagnostics
- [ ] DG-01: python3 scripts/validate-plugin.py 실행 시 새로 추가된 3개 스킬에서 ERROR 0건
- [ ] DG-02: python3 scripts/sync-evals.py --check-only 실행 시 missing drift 0건
