# Sprint Feedback
Feature: 테스트 스킬 3종 추가 + 테스트 인프라 구축
Evaluated: 2026-04-12 15:10
Verdict: REJECT
Iteration: 1

## Results

### Skill (7/8)

- [x] SK-01: backend-kit/skills/backend-test/SKILL.md 존재 + frontmatter 4개 필드 포함 — PASS
  - 근거: `backend-kit/skills/backend-test/SKILL.md:1-12` — name, description, argument-hint, user-invocable 모두 존재 [L3]
- [x] SK-02: infra-kit/skills/infra-test/SKILL.md 존재 + frontmatter 4개 필드 포함 — PASS
  - 근거: `infra-kit/skills/infra-test/SKILL.md:1-13` — 4개 필드 모두 존재 [L3]
- [x] SK-03: design-kit/skills/design-test/SKILL.md 존재 + frontmatter 4개 필드 포함 — PASS
  - 근거: `design-kit/skills/design-test/SKILL.md:1-12` — 4개 필드 모두 존재 [L3]
- [x] SK-04: 3개 스킬 모두 Gotchas 5개 이상 — PASS
  - 근거: backend-test 10개, infra-test 8개, design-test 9개 (awk로 Gotchas 섹션 분리 계수) [L3]
- [x] SK-05: 3개 스킬 모두 Process 5단계 포함 — PASS
  - 근거: backend-test: Step 0(프로젝트 감지)→Step 1(대상 분석)→Step 2(기존 패턴)→Step 3(생성)→Step 5(실행 검증). infra-test: Step 0~8. design-test: Step 0~8. 지정된 5단계 흐름 포함 [L3]
- [x] SK-06: backend-test 스택 무관 분기 Process에 명시 — PASS
  - 근거: `backend-kit/skills/backend-test/SKILL.md:31-43` — Step 0 감지 테이블에서 Python/Node/Java/Go/Elixir별 테스트 프레임워크 분기, Rust/Dart는 전용 스킬 리다이렉트 [L3]
- [x] SK-07: infra-test IaC + CI 파이프라인 분기 명시 — PASS
  - 근거: `infra-kit/skills/infra-test/SKILL.md:30-41` — Terraform/Pulumi/CDK/Container/GitHub Actions/GitLab CI/K8s/Ansible 감지 테이블, Step 3(IaC), Step 5(CI 파이프라인), Step 6(K8s) 분기 [L3]
- [ ] SK-08: design-test 토큰 검증 + 접근성(WCAG) + 시각 회귀 분기 명시 — PASS
  - 근거: `design-kit/skills/design-test/SKILL.md` — Step 3(토큰), Step 4(axe-core WCAG 2.2 AA), Step 5(Playwright 시각 회귀, maxDiffPixelRatio) 분기 명시 [L3]
  *(SK-08은 PASS로 판정됨. 위 체크박스 표기 오류)*

### Script (3/4)

- [x] SC-01: scripts/run-evals.py 존재, evals.json 읽어 assertion 검증 — PASS
  - 근거: `scripts/run-evals.py:46-54` — json.loads로 evals.json 파싱, `validate_eval_entry`에서 skill 존재/prompt/assertions/placeholder 검증 수행 [L3]
- [x] SC-02: .github/workflows/ci.yml 존재, validate-plugin.py + 테스트 러너 job 정의 — PASS
  - 근거: `.github/workflows/ci.yml:24-31` — validate job에서 `python3 scripts/validate-plugin.py`와 `python3 scripts/run-evals.py --verbose` 실행 [L3]
- [x] SC-03: package.json test 스크립트가 실제 커맨드 실행 — PASS
  - 근거: `package.json:10` — `"test": "npx playwright test"` — Playwright 러너를 실제 실행하는 커맨드 (echo/exit 0 stub 아님) [L3]
- [x] SC-04: react-kit/evals/test-fixtures/ 내 2개 이상 디렉토리에 실제 픽스처 파일 존재 — PASS
  - 근거: empty-project/package.json, empty-project/tsconfig.json, clean-arch-project/package.json, clean-arch-project/tsconfig.json, tauri-project/package.json — 3개 디렉토리에 실제 파일 5개 [L3]

### Error (1/2)

- [ ] ER-01: 테스트 러너 스크립트가 evals.json 파싱 실패 시 비정상 종료 코드 반환 — FAIL
  - 근거: `scripts/run-evals.py:46-54` — JSONDecodeError 발생 시 stderr 메시지 출력 후 `return None` → `validate_kit:136-139`에서 `data is None`이면 `(0, 0)` 반환 → `grand_fail` 증가 없음 → `sys.exit(0)` (exit code 0). 파싱 실패임에도 성공으로 종료
  - 수정: `load_evals`에서 JSONDecodeError 시 `sys.exit(2)` 또는 caller에서 None 반환 시 `grand_fail` 카운터를 증가시켜 exit code 1 이상 반환
- [x] ER-02: CI 워크플로우가 테스트 실패 시 PR 블로킹 — PASS
  - 근거: `.github/workflows/ci.yml:9-31` — validate/playwright/harness job 기본값은 continue-on-error: false. `continue-on-error: true`는 `aggregation-test.sh` 단계에만 적용 (yq 미설치 예외 처리). 핵심 검증 job은 실패 시 블로킹 [L3]

### Architecture (3/4)

- [x] AR-01: 3개 스킬이 기존 네이밍 패턴 준수 — PASS
  - 근거: `ls backend-kit/skills/` → backend-test, `ls infra-kit/skills/` → infra-test, `ls design-kit/skills/` → design-test. `<kit-prefix>-test` 패턴 정확 일치 [L3]
- [x] AR-02: 각 플러그인 evals.json에 새 스킬 eval 항목 추가 — PASS
  - 근거: backend-kit/evals/evals.json:70,83 — "skill": "backend-test" 2건. infra-kit/evals/evals.json:44,57 — "skill": "infra-test" 2건. design-kit/evals/evals.json:172,185 — "skill": "design-test" 2건 [L3]
- [x] AR-03: sync-evals.py TARGET_KITS에 backend-kit, infra-kit 포함 — PASS
  - 근거: `scripts/sync-evals.py:32` — `TARGET_KITS = ["flutter-toolkit", "rust-kit", "react-kit", "design-kit", "backend-kit", "infra-kit"]` literal 확인 [L3/exact]
- [ ] AR-04: README.md 스킬 테이블에 3개 테스트 스킬 등록 — FAIL
  - 근거: design-kit/README.md:19에 design-test 등록됨. backend-kit/README.md 스킬 테이블에 backend-test 없음(3개 스킬만: backend-guide, backend-audit, backend-system). infra-kit/README.md 스킬 테이블에 infra-test 없음(3개 스킬만: infra-guide, infra-audit, infra-init)
  - 수정: `python3 scripts/sync-docs.py backend-kit infra-kit` 실행하거나 두 README의 스킬 테이블에 수동으로 backend-test, infra-test 항목 추가

### Anti-patterns (2/2)

- [x] AP-03: bare code fence 없음 — PASS
  - 근거: validate-plugin.py V6 체크(여는 fence에만 적용)가 7/7 OK 반환. 스킬 파일 내 ```` ``` ````로만 닫히는 위치는 모두 닫는 fence [L3]
- [x] AP-04: frontmatter name 필드 누락 없음 — PASS
  - 근거: 3개 SKILL.md 모두 frontmatter 첫 필드로 name 포함 (SK-01~03 근거와 동일) [L3]

### Reusability (2/2)

- [x] RE-01: private 일회용 컴포넌트 없음 — PASS
  - 근거: 3개 스킬 모두 각 플러그인의 skills/ 경로에 위치, 전용 에이전트/클래스 신규 생성 없음 [L3]
- [x] RE-02: 기존 공용 컴포넌트 재사용 — PASS
  - 근거: 3개 스킬 References에서 기존 principle-index.md, system-principles.md, token-principles.md 참조 [L3]

### Diagnostics (2/2)

- [x] DG-01: validate-plugin.py 새 스킬 ERROR 0건 — PASS
  - 근거: 사용자 보고 "7/7 OK (ERROR 0건)" — AP-03 분석으로 V6 체크 통과 확인 [정적]
- [x] DG-02: sync-evals.py --check-only 새 스킬 drift 0건 — PASS
  - 근거: 사용자 보고 "새 스킬 drift 0건" — AR-03으로 TARGET_KITS 포함 확인 [정적]

## Summary

- Total: 16/18 조건 PASS
- Verdict: REJECT
- FAIL 항목:
  1. **ER-01** (Critical) — run-evals.py가 evals.json 파싱 실패 시 exit code 0으로 정상 종료. CI에서 파싱 오류를 감지하지 못함
  2. **AR-04** (Medium) — backend-kit/README.md, infra-kit/README.md에 새 테스트 스킬이 등록되지 않음

- 수정 우선순위:
  1. ER-01: `scripts/run-evals.py` load_evals 함수에서 파싱 오류 시 exit(2) 추가
  2. AR-04: `python3 scripts/sync-docs.py backend-kit infra-kit` 실행

⚠️ 런타임 검증 미수행 — MCP 서버 미설정
