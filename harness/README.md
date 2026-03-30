# Harness Engineering

Sprint Contract + QA Evaluator 기반 품질 보증 시스템.
프로젝트 스택에 관계없이 `project.yaml`과 `procedures/`만 설정하면 동작한다.

## 셋업

```
.harness/
├── project.yaml              ← 프로젝트 설정 (필수)
├── procedures/                ← 검증 절차 (스택별)
│   ├── ui-verification.md
│   ├── logic-verification.md
│   ├── error-verification.md
│   └── architecture-verification.md
├── sprint-contract.md         ← 현재 스프린트 계약 (자동 생성)
├── sprint-feedback.md         ← QA 피드백 (자동 생성)
└── history/                   ← 아카이브 (자동)
```

## project.yaml 스키마

### 필수 필드

| 필드 | 타입 | 설명 |
|------|------|------|
| `stack` | string | 프로젝트 스택. 자유 텍스트 (flutter, rust, react, python 등) |
| `commands.analyze` | string | 정적 분석 명령. DG-01 검증에 사용 |
| `commands.test` | string | 테스트 명령. DG-03 검증에 사용 |
| `contract_categories` | list | 계약 카테고리 목록 (최소 1개) |
| `anti_patterns` | list | 안티패턴 Grep 패턴 목록 (최소 2개 권장) |

### 선택 필드

| 필드 | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| `commands.lint` | string\|null | null | 린트 명령. null이면 건너뜀 |
| `commands.format` | string\|null | null | 포맷 명령 |
| `commands.codegen` | string\|null | null | 코드 생성 명령 |
| `reusability.shared_path` | string | "" | 공유 컴포넌트 경로 |
| `reusability.check_duplicate` | bool | true | 유사 컴포넌트 중복 검사 |
| `diagnostics.ide_exclude` | list[string] | [] | IDE 경고 제외 패턴 |
| `diagnostics.console_errors` | list[string] | [] | 콘솔 에러 패턴 (ripgrep regex) |
| `diagnostics.console_exclude` | list[string] | [] | 콘솔 제외 패턴 |
| `env` | object\|null | null | 환경 설정. null이면 환경 검증 건너뜀 |
| `runtime_inspection` | object\|null | null | MCP 런타임 검증. null이면 정적 검증만 |
| `trigger` | object | 내장 기본값 | 트리거/비트리거 조건 |
| `verification.procedures_dir` | string | ".harness/procedures/" | 검증 절차 파일 디렉토리 |
| `rationalization_overrides` | list | [] | 프로젝트별 변명 차단 |

### contract_categories 상세

```yaml
contract_categories:
  - id: UI              # 섹션 헤더로 사용. 영문, 공백 없음
    prefix: "UI"         # 조건 ID 접두사. 고유, 짧게 (2-3자)
    description: "..."   # 조건 작성 가이드
```

**제약:**
- `id`는 영문, 공백/특수문자 없음 (파싱에 사용)
- `prefix`는 고유, 하이픈 미포함 (ID 형식: `{prefix}-{번호}`)
- 최소 1개 카테고리 필수

### anti_patterns 상세

```yaml
anti_patterns:
  - id: AP-01            # 고유 ID
    pattern: "regex"      # ripgrep 호환 정규식
    message: "설명"       # FAIL 시 표시할 메시지
```

**패턴 규칙:**
- ripgrep regex 문법 사용
- 변경/생성 파일에서만 검색 (전체 프로젝트 아님)
- 패턴 테스트: `rg "{pattern}" --type-not binary` 로 사전 확인 권장

### env 상세

```yaml
env:
  sdk_cmd:                    # SDK 래퍼 명령 (fvm, nvm 등)
    name: "fvm"               # 원래 명령 이름
    windows: "fvm.bat"        # Windows용
    unix: "fvm"               # macOS/Linux용
    guard_message: "메시지"   # 차단 시 표시
  required_files:             # 필수 파일 목록
    - path: ".env"
      message: "설명"
      resolve: "생성 명령"    # 선택 — 없을 때 자동 실행
  required_commands:          # 필수 CLI 명령
    - "cargo"
    - "docker"
  external_tools:             # 선택적 외부 도구
    - name: "adb"
      windows_fallback: "경로"
      optional: true
```

### trigger 상세

```yaml
trigger:
  min_files: 2                # 이 수 이상 파일 변경 시 트리거
  always: ["키워드"]           # 이 키워드가 요청에 있으면 항상 트리거
  never: ["키워드"]            # 이 키워드가 있으면 트리거 안 함
```

- `always`/`never`는 사용자 요청 텍스트에 대한 부분 문자열 매칭
- 사용자가 쓰는 언어로 작성 (한국어/영어 등)
- `never`가 `always`보다 우선

### runtime_inspection 상세

```yaml
runtime_inspection:
  mcp_server: "server-name"   # MCP 서버 이름. null이면 정적 검증만
  vm_port: 8181               # VM service 포트
  launch_script: "경로"       # 앱 실행 스크립트
```

## procedures 작성 가이드

### 파일 이름 규칙

`{category_id 소문자}-verification.md`

예: 카테고리 `id: API` → `api-verification.md`

### 필수 섹션

```markdown
# {Category} 조건 검증 절차 ({Stack})

## 검증 방법
1. {단계별 검증 절차 — 어떤 도구로 무엇을 확인}
2. ...

## 정적 검증 최소 증거
| 조건 유형 | PASS 가능한 최소 증거 |
|-----------|----------------------|
| "{패턴}" | {증거 설명} |
```

### 선택 섹션

```markdown
## 런타임 검증 (MCP 사용 가능 시)
1. {MCP 도구} — {확인 내용}

## 금지 패턴
- {패턴} — {이유}
```

### 절차 파일이 없으면?

해당 카테고리는 **범용 검증**으로 폴백:
- Glob으로 관련 파일 검색
- Read로 내용 확인
- 조건에 명시된 요소가 코드에 존재하는지 확인

## 스택별 예시

### Flutter

```yaml
stack: flutter
commands:
  analyze: "fvm.bat flutter analyze"
  test: "fvm.bat flutter test"
  format: "fvm.bat dart format"
  codegen: "fvm.bat dart run build_runner build --delete-conflicting-outputs"
anti_patterns:
  - id: AP-01
    pattern: "StatefulWidget|ConsumerStatefulWidget"
    message: "StatefulWidget 금지 → HookWidget"
  - id: AP-02
    pattern: "GestureDetector|InkWell"
    message: "GestureDetector/InkWell 금지 → Pressable"
```

### Rust Axum

```yaml
stack: rust
commands:
  analyze: "cargo clippy --workspace --all-targets -- -D warnings"
  test: "cargo test --workspace"
  lint: "cargo clippy --workspace"
  format: "cargo fmt --all -- --check"
contract_categories:
  - id: API
    prefix: "API"
    description: "엔드포인트, 요청/응답, 라우팅"
  - id: Database
    prefix: "DB"
    description: "스키마, 쿼리, 마이그레이션"
  - id: Error
    prefix: "ER"
    description: "에러 타입, 변환, HTTP 응답 매핑"
  - id: Architecture
    prefix: "AR"
    description: "모듈 구조, port/adapter, 의존 방향"
anti_patterns:
  - id: AP-01
    pattern: "unwrap\\(\\)"
    message: "unwrap() 금지 → ? 또는 expect() 사용"
  - id: AP-02
    pattern: "println!"
    message: "println! 금지 → tracing 매크로 사용"
env:
  required_commands:
    - "cargo"
    - "docker"
  required_files:
    - path: ".env"
      message: ".env 필요 (DB 연결 정보)"
```

### React / Next.js

```yaml
stack: react
commands:
  analyze: "npx eslint --max-warnings 0 ."
  test: "npx jest --passWithNoTests"
  lint: "npx eslint ."
  format: "npx prettier --check ."
contract_categories:
  - id: UI
    prefix: "UI"
    description: "컴포넌트 렌더링, 레이아웃, 스타일"
  - id: Logic
    prefix: "LG"
    description: "훅, 상태 관리, 데이터 페칭"
  - id: Error
    prefix: "ER"
    description: "에러 바운더리, 폴백 UI, 에러 핸들링"
  - id: Architecture
    prefix: "AR"
    description: "파일 구조, import 규칙, 서버/클라이언트 분리"
anti_patterns:
  - id: AP-01
    pattern: "any"
    message: "any 타입 금지 → 구체적 타입 명시"
  - id: AP-02
    pattern: "console\\.log"
    message: "console.log 금지 → logger 사용"
diagnostics:
  console_errors:
    - "Unhandled Runtime Error"
    - "Warning: Each child .* should have a unique"
    - "Hydration failed"
```

## 검증 체크리스트

새 프로젝트에 하네스 셋업 후 확인:

- [ ] `project.yaml` 존재
- [ ] `commands.analyze`와 `commands.test`가 실제 실행 가능
- [ ] `contract_categories`에 최소 1개 카테고리
- [ ] 각 카테고리의 `id`가 영문, 공백 없음
- [ ] 각 카테고리의 `prefix`가 고유
- [ ] `anti_patterns`에 최소 2개 패턴
- [ ] 각 패턴이 `rg "{pattern}"` 으로 실행 가능
- [ ] `procedures/` 에 카테고리별 검증 절차 파일 존재 (없으면 범용 폴백)
- [ ] `trigger.always`와 `trigger.never`에 겹치는 키워드 없음

## Verdict 값

QA Evaluator 판정 결과는 **APPROVE** 또는 **REJECT** 두 가지만 사용한다.
(PASS는 개별 조건 수준, APPROVE/REJECT는 전체 판정 수준)

---

## Harness Kaizen — 지속적 개선

학술 논문·공식 문서·커뮤니티 리서치를 기반으로 하네스를 자동으로 개선하는 스킬.

### 사용법

```bash
# 전체 영역 리서치 + 개선 PR 생성
/harness-kaizen

# 특정 영역만 집중
/harness-kaizen config    # 설정 (project.yaml, procedures, anti-patterns)
/harness-kaizen skills    # 스킬 프롬프트, 에이전트, eval
/harness-kaizen guide     # docs/guides/skill-design-guide.md
```

### 자동 실행

| 트리거 | 조건 |
|--------|------|
| **주기적** | 매주 월요일 09:00 KST (cron, 클라우드 실행) |
| **REJECT 연속** | QA Evaluator REJECT 2회 연속 시 |
| **Anti-pattern 반복** | 같은 anti-pattern 3회 이상 감지 시 |
| **신규 스킬** | 스킬 추가 후 7일 이내 |

### 개선 대상

| 영역 | 대상 |
|------|------|
| 하네스 설정 | `project.yaml`, `procedures/`, anti-patterns |
| 스킬 프롬프트 | `skills/*/SKILL.md` |
| 에이전트 로직 | `agents/qa-evaluator.md` |
| Eval | `evals/` 테스트 픽스처·평가 기준 |
| 아키텍처 | 폴더 구조, 훅, 스크립트 |
| 설계 가이드 | `docs/guides/skill-design-guide.md` |

### 파이프라인

```
COLLECT → VERIFY → ANALYZE → PROPOSE + APPLY
(수집)    (3중검증)  (갭분석)   (브랜치→변경→PR)
```

1. **COLLECT** — 학술 논문(arXiv, ACL, IEEE), 공식 docs(Anthropic, OpenAI, DeepMind), 커뮤니티(GitHub trending, 블로그, 컨퍼런스) 검색
2. **VERIFY** — 3중 검증 게이트로 할루시네이션 차단 (출처 URL 필수 → WebFetch 접근 확인 → PR에 증거 첨부)
3. **ANALYZE** — 현재 하네스 상태와 연구 결과를 비교하여 갭 분석
4. **PROPOSE + APPLY** — 브랜치 생성, 변경 적용, 버전 bump, PR 생성

### 버전 관리

카이젠 PR은 영향도에 따라 semver bump:

| 변경 영역 | bump |
|-----------|------|
| docs, config 튜닝, Gotchas 추가 | **patch** |
| 스킬 프롬프트, eval 기준, procedure 추가 | **minor** |
| 아키텍처, 에이전트 로직 대폭 수정 | **major** |

### 추적 규칙

- 커밋: `kaizen:` prefix — `kaizen: sprint-contract few-shot 판단 로직 추가`
- 브랜치: `kaizen/{버전}-{날짜}` — `kaizen/0.4.0-2026-04-07`
- PR 제목: `[bump유형]` prefix — `[minor] sprint-contract 복잡도 판단 개선`

### 산출물

```
docs/kaizen/
├── research-log.md    # 누적 연구 기록 (소스별 채택/폐기)
└── changelog.md       # 카이젠 변경 이력 (버전, 근거, Before/After)
```

### 스케줄 관리

클라우드에서 실행되므로 로컬 컴퓨터가 꺼져 있어도 동작한다.
스케줄 확인·비활성화·삭제는 [claude.ai/code/scheduled](https://claude.ai/code/scheduled)에서 관리.
