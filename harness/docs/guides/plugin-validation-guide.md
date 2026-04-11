---
title: Claude Code 플러그인 검증 가이드
version: 1.0.0
last_updated: 2026-04-11
scope: "harness/flutter-toolkit/design-kit/backend-kit/infra-kit/rust-kit/react-kit"
---

# Claude Code 플러그인 검증 가이드

> 릴리스 전 품질 게이트 + 카이젠 베이스라인을 제공하는 7-카테고리 검증 체계.

**이 문서의 용도:** `scripts/validate-plugin.py` 의 각 체크가 무엇을, 왜, 어떻게 검증하는지 정의한다.
새 킷을 추가하거나 기존 킷을 개선할 때 이 문서를 SSOT(Single Source of Truth)로 사용한다.

---

## 1. 목적

플러그인 모노레포는 7개 킷, 100여 개 스킬, 10여 개 에이전트로 구성된다. 킷 수가 늘어날수록 다음 문제가 발생한다.

- **숨은 깨진 링크**: SKILL.md가 references/xxx.md 를 참조하지만 파일이 존재하지 않는다.
- **Frontmatter 누락**: 신규 스킬에 `name` 또는 `description` 이 없어 Claude가 스킬을 인식하지 못한다.
- **트리거 중복**: 두 킷이 동일한 키워드를 트리거로 선언해 의도치 않은 스킬이 실행된다.
- **placeholder 노출**: `TODO`, `TBD`, `FIXME` 가 사용자에게 그대로 보여진다.
- **버전 불일치**: `plugin.json`의 버전과 `marketplace.json`의 description 태그가 달라 릴리스 추적이 깨진다.

이 가이드는 위 문제를 자동으로 탐지하는 7가지 검증 카테고리(V1~V7)를 정의하고, 각 카테고리의 기준·방법·예외·FAIL 예시를 명시한다. 카이젠 주기마다 이 가이드를 기준으로 전체 킷을 점검하여 품질 저하를 방지한다.

---

## 2. 적용 범위

`.claude-plugin/plugin.json` 을 가진 모든 디렉토리를 검증 대상으로 삼는다. 현재 7개 킷이 대상이다:

```
harness/          flutter-toolkit/    design-kit/
backend-kit/      infra-kit/          rust-kit/
react-kit/
```

킷 목록은 `.claude-plugin/marketplace.json` 의 `plugins` 배열에서 자동으로 읽는다. 새 킷을 추가할 때 marketplace.json 에 먼저 등록하면 검증 대상에 자동 포함된다.

### 실행 명령

```bash
# 전체 킷 검증
python3 scripts/validate-plugin.py

# 특정 킷만
python3 scripts/validate-plugin.py react-kit

# 특정 체크만
python3 scripts/validate-plugin.py --check=frontmatter,refs

# JSON 출력 (CI)
python3 scripts/validate-plugin.py --json

# 자동 수정 (V5 placeholders + V6 code-fence)
python3 scripts/validate-plugin.py --fix
```

---

## 3. 7가지 검증 카테고리

### V1 Frontmatter 무결성

**기준**

스킬 파일(`skills/*/SKILL.md`)은 `name`, `description`, `user-invocable` 세 필드를 모두 가져야 한다.
에이전트 파일(`agents/*.md`)은 `name`, `description`, `tools`, `model` 네 필드를 모두 가져야 한다.
두 경우 모두 YAML frontmatter(`---` 블록)가 정상 파싱되어야 한다.

**검증 방법**

각 SKILL.md, agents/*.md 파일 상단의 `---` 블록을 `yaml.safe_load()` 로 파싱한다.
파싱 성공 후 필수 필드 존재 여부를 `dict.get()` 으로 확인한다. 값이 빈 문자열이어도 FAIL.

```python
# V1 — see harness/docs/guides/plugin-validation-guide.md §3.1
required_skill_fields = {"name", "description", "user-invocable"}
required_agent_fields = {"name", "description", "tools", "model"}
```

**예외**

없음. 모든 스킬과 에이전트는 예외 없이 frontmatter 를 가져야 한다.

**FAIL 예시**

```yaml
# 필드 누락
---
name: react-screen
description: >
  화면을 생성한다.
# user-invocable 없음 → FAIL
---
```

```yaml
# YAML parse 실패
---
name: react-screen
description: >
 들여쓰기 오류로 파싱 실패: [broken
---
```

---

### V2 Templates 구문

**기준**

`templates/` 디렉토리가 존재할 때, 그 안의 JSON/YAML/TOML 파일은 각각 표준 파서로 파싱되어야 한다.
`.ts`, `.js` 등 트랜스파일이 필요한 파일은 외부 도구(tsc, node) 없이 검증 불가능하므로 SKIP 한다.

**검증 방법**

확장자별 파서 매핑:

| 확장자 | 파서 |
|--------|------|
| `.json` | `json.loads()` |
| `.yaml`, `.yml` | `yaml.safe_load()` |
| `.toml` | `tomllib.loads()` (Python 3.11 표준) |
| `.ts`, `.js`, `.tsx` | SKIP |
| 기타 | SKIP |

`templates/` 가 없으면 "SKIP (no templates/)" 로 출력하고 PASS 처리한다.

**예외**

- `templates/` 없는 킷: V2 체크 전체 SKIP (harness, flutter-toolkit, design-kit, backend-kit, infra-kit — §6 킷별 예외 카탈로그 참조)
- `.ts`, `.js` 파일: 언제나 SKIP (parse 실패로 처리하지 않음)
- `.template` 확장자 파일: 내부 확장자(`.json.template`)로 판별. 예를 들어 `package.json.template` 는 `.json` 파서 적용

**FAIL 예시**

```json
// package.json.template — 후행 쉼표 → JSON parse 실패
{
  "name": "my-app",
  "version": "0.1.0",
}
```

```yaml
# lingui.config.ts.template 가 .yaml 로 잘못 저장된 경우
name: [broken yaml
```

---

### V3 Cross-reference 링크

**기준**

SKILL.md 본문에 등장하는 상대 경로 링크가 실제 파일로 해소되어야 한다.
검증 대상 패턴:
- Markdown 링크: `[text](path)`
- 코드 인라인 경로: 상대 경로 형태의 문자열 (`references/xxx.md`, `../other-kit/yyy`)

절대 URL(`https://`, `http://`)과 앵커만 있는 링크(`#section`)는 제외한다.

**검증 방법**

정규식으로 마크다운 링크와 경로 패턴을 추출하고, SKILL.md 위치를 기준으로 `os.path.exists()` 로 확인한다.

```python
# V3 — see harness/docs/guides/plugin-validation-guide.md §3.3
pattern = r'\[(?:[^\]]+)\]\(([^)#]+)\)'  # [text](path), 앵커 제외
```

**예외**

- 절대 URL: 검증 대상에서 제외
- 앵커 링크 (`#heading`): 제외
- `<!-- novalidate -->` 주석이 달린 링크: SKIP (의도적 미해소 링크)

**FAIL 예시**

```markdown
## References
- [shadcn 스켈레톤 가이드](references/shadcn-skeleton.md)
# → references/shadcn-skeleton.md 파일 없음 → FAIL
```

```markdown
# 킷 간 교차 참조
참조: [Rust 에러 가이드](../rust-kit/references/error-patterns.md)
# → 파일 없으면 FAIL
```

---

### V4 Trigger 키워드

**기준**

각 SKILL.md 의 `description` 에서 따옴표(`"..."` 또는 `'...'`)로 감싼 키워드를 추출하여,
동일 킷 내부 또는 다른 킷과 exact-match 중복이 있으면 WARNING 으로 보고한다.

키워드 중복은 두 스킬이 동일한 사용자 발화에 동시에 트리거될 수 있음을 의미한다.

**검증 방법**

```python
# V4 — see harness/docs/guides/plugin-validation-guide.md §3.4
pattern = r'["\']([^"\']{3,})["\']'  # 3자 이상 키워드만 추출
```

추출한 키워드를 소문자 정규화 후 `collections.Counter` 로 중복 검출. 2회 이상 등장하면 WARNING.

**예외**

- 2자 이하 키워드: 너무 일반적이므로 추출에서 제외
- `--fix`, `--json` 같은 CLI 플래그 패턴: 제외
- 공통 동사(`구현해줘`, `만들어줘`): 중복이 설계 의도일 수 있음. WARNING 으로 처리하되 ERROR 는 아님

**FAIL 예시**

```yaml
# react-screen/SKILL.md
description: >
  "새 화면 추가", "페이지 추가" 요청 시 트리거.

# flutter-screen/SKILL.md
description: >
  "새 화면 추가" 요청 시 트리거.  # 동일 키워드 → WARNING
```

---

### V5 Placeholders

**기준**

검증 대상 파일(`SKILL.md`, `agents/*.md`, `README.md`, `references/*.md`)의 본문에
`TODO`, `TBD`, `FIXME` 가 0건이어야 한다. 대소문자 무관, 단어 경계(`\b`) 기준 매칭.

코드 블록 안의 주석(`// TODO: ...`, `# TODO: ...`)도 포함한다.
단, `--fix` 모드는 이를 중립 주석으로 자동 교체한다.

**검증 방법**

```python
# V5 — see harness/docs/guides/plugin-validation-guide.md §3.5
pattern = r'\b(TODO|TBD|FIXME)\b'
```

`re.IGNORECASE` 플래그로 검색. 매치된 파일과 라인 번호를 모두 보고한다.

**예외**

- `validate-plugin.py` 스크립트 본문: 자기 참조 도구이므로 V5 체크 대상에서 제외 (self-hosting)
- 코드 템플릿 예시 안의 플레이스홀더: 제외 없음. 설명용이라도 사용자 문서에 노출되므로 FAIL

**FAIL 예시**

```markdown
## Process

1. 입력을 받는다
2. TODO: 검증 로직 추가 예정  ← FAIL
3. 결과를 출력한다
```

```typescript
// templates/vite.config.template.ts
export default {
  // FIXME: 이 옵션은 나중에 채워야 함  ← FAIL
}
```

---

### V6 Code fence 언어 힌트

**기준**

마크다운 파일의 코드 블록 여는 fence(` ``` `) 에는 언어 힌트가 있어야 한다.
빈 fence(언어 힌트 없음)는 Claude 가 구문 하이라이팅과 언어 분류를 못해 컨텍스트 품질이 떨어진다.

닫는 fence(` ``` ` 단독 라인)는 검증하지 않는다.

**검증 방법**

마크다운 상태 머신으로 구현한다. ` ``` ` 를 토글 기준으로 `in_block` 상태를 추적한다.
여는 fence 에서 ` ``` ` 뒤가 공백이면 FAIL.

```python
# V6 — see harness/docs/guides/plugin-validation-guide.md §3.6
# ``` 뒤가 비어있으면(strip 후 빈 문자열) FAIL
if line.startswith("```") and not in_block:
    hint = line[3:].strip()
    if not hint:
        violations.append(...)
```

**예외**

- 닫는 fence: ` ``` ` 단독 라인은 정상, 체크 대상 아님
- `~~~` 틸드 fence: 현재 검증 대상 아님 (모노레포 컨벤션은 backtick 사용)

**FAIL 예시**

````markdown
## 예시

```
// 언어 힌트 없음 → FAIL
const x = 1;
```
````

````markdown
## 올바른 예시

```typescript
// 언어 힌트 있음 → PASS
const x: number = 1;
```
````

---

### V7 plugin.json ↔ marketplace.json 정합성

**기준**

각 킷의 `.claude-plugin/plugin.json` 과 루트 `.claude-plugin/marketplace.json` 이 일치해야 한다.

- `name` 일치
- `version` 일치
- marketplace description 의 `[vX.Y.Z · YYYY-MM-DD]` 형식 존재 + 버전 태그 일치

**검증 방법**

```python
# V7 — see harness/docs/guides/plugin-validation-guide.md §3.7
version_pattern = r'\[v(\d+\.\d+\.\d+)\s*·\s*\d{4}-\d{2}-\d{2}\]'
```

1. marketplace.json 의 해당 킷 엔트리에서 description 추출
2. 정규식으로 버전 태그 파싱
3. plugin.json 의 `version` 과 비교

**예외**

- 새 킷 초기 단계: marketplace.json 에 등록 전이면 V7 체크 대상 아님 (marketplace 에 없으면 킷 자체가 검증 대상 목록에서 빠짐)

**FAIL 예시**

```json
// react-kit/.claude-plugin/plugin.json
{ "version": "0.2.0" }

// .claude-plugin/marketplace.json
{ "description": "[v0.1.0 · 2026-04-10] React + Vite ..." }
// → 0.2.0 ≠ 0.1.0 → FAIL
```

```json
// marketplace.json description 에 버전 태그 없음
{ "description": "React + Vite + Tauri 2 개발 플러그인" }
// → [vX.Y.Z · YYYY-MM-DD] 형식 없음 → FAIL
```

---

## 4. 자동화 사용법

### CLI 옵션

| 옵션 | 설명 | 예시 |
|------|------|------|
| `[plugin]` | 특정 킷만 검증 | `validate-plugin.py react-kit` |
| `--check=<list>` | 특정 체크만 (쉼표 구분) | `--check=frontmatter,refs` |
| `--json` | JSON 출력 (CI 파이프라인용) | `--json` |
| `--fix` | 자동 수정 (V5 + V6만) | `--fix` |
| `--help` | 사용법 출력 | `--help` |

`--check` 에 사용하는 체크 이름:
`frontmatter`, `templates`, `refs`, `triggers`, `placeholders`, `code-fence`, `plugin-json`

### 출력 포맷

```
=== harness ===
  V1 frontmatter    7 skills + 1 agent — OK
  V2 templates      0 files — SKIP (no templates/)
  V3 refs           12 links — OK
  V4 triggers       42 keywords — OK
  V5 placeholders   0 found — OK
  V6 code-fence     0 bare — OK
  V7 plugin-json    v0.3.5 matches marketplace — OK

=== react-kit ===
  V1 frontmatter    21 skills + 3 agents — OK
  V2 templates      5 parsed, 4 skipped (ts/js) — OK
  V3 refs           89 links, 2 BROKEN
    FAIL react-kit/skills/react-skeleton/SKILL.md:42 → references/shadcn-skeleton.md (not found)
    FAIL react-kit/skills/react-skeleton/SKILL.md:67 → ../design-kit/references/token-schema.md (not found)
  V4 triggers       58 keywords, 1 duplicate
    WARN "새 화면 추가" — react-screen, flutter-screen
  V5 placeholders   0 found — OK
  V6 code-fence     0 bare — OK
  V7 plugin-json    v0.1.0 matches marketplace — OK

Total: 7 plugins — 5 OK, 1 WARNING, 1 ERROR
Exit: 2
```

### Exit Code

| Code | 의미 |
|------|------|
| 0 | 모든 체크 PASS |
| 1 | WARNING 있음 (킷별 예외 카탈로그에 해당하는 특수 케이스 포함) |
| 2 | ERROR 있음 (진짜 FAIL) |

---

## 5. 발견 시 대응

### 자동 수정 (`--fix`)

`--fix` 모드로 안전하게 자동 수정 가능한 두 체크:

| 체크 | 수정 동작 |
|------|----------|
| V5 Placeholders | `TODO:` → `<설명 필요>`, `TBD` → `<내용 추가>`, `FIXME:` → `<수정 필요>` |
| V6 Code fence | 빈 ` ``` ` → ` ```text ` |

나머지 체크(V1~V4, V7)는 `--fix` 로 수정하지 않는다. 파일 삭제나 링크 재배선 같은 작업은 의미 분석이 필요하므로 위험하다.

### 수동 수정

| 체크 | 수동 수정 방법 |
|------|--------------|
| V1 | SKILL.md 또는 agents/*.md frontmatter 에 누락 필드 추가 |
| V2 | templates/ 의 JSON/YAML/TOML 구문 오류 수정 |
| V3 | 참조 파일 생성 또는 링크 경로 수정 |
| V4 | description 에서 중복 키워드 제거 또는 구체화 |
| V7 | plugin.json 또는 marketplace.json 버전 태그 일치 |

### 카이젠 위임 기준

다음 경우 해당 킷의 `*-kaizen` 스킬로 위임한다:

- V3 FAIL 이 3건 이상: 참조 구조를 재설계해야 할 수준
- V4 중복이 5건 이상: 킷 간 트리거 키워드 체계 재정의 필요
- V1 FAIL 이 3건 이상: 스킬 템플릿 자체가 잘못된 경우

---

## 6. 킷별 예외 카탈로그

| 킷 | V2 templates | 비고 |
|-------|-------------|------|
| harness | `templates/` 없음 — SKIP | QA 프레임워크. 코드 템플릿 대상 아님 |
| flutter-toolkit | `templates/` 없음 — SKIP | 스킬 지시문 기반. 별도 템플릿 파일 없음 |
| design-kit | `templates/` 없음 — SKIP | 디자인 가이드 중심. 코드 템플릿 없음 |
| backend-kit | `templates/` 없음 — SKIP | 스택 무관 가이드. 프레임워크별 스캐폴딩은 각 킷에서 |
| infra-kit | `templates/` 없음 — SKIP | 스택 무관 가이드. 인프라 코드 템플릿 없음 |
| rust-kit | `templates/` 없음 — SKIP | 스킬에서 인라인으로 생성. 향후 templates/ 추가 가능 |
| react-kit | `templates/` 9 파일 — TS 파일은 V2 SKIP | `.ts/.js` 4개 SKIP, 나머지 5개(`Cargo.toml.template` 등) 파싱 |

> TS/JS 파일 V2 SKIP 은 외부 도구(tsc) 의존 없이 검증 불가능하기 때문이다. 이 파일들의 구문 검증은 CI 빌드 단계에서 수행한다.

---

## 7. 카이젠 연동

각 킷의 카이젠 스킬(`*-kaizen`)이 이 가이드를 베이스라인으로 사용한다.

### 카이젠 진입 시 체크리스트

카이젠 스킬은 실행 초반에 다음을 수행한다:

```bash
# 카이젠 대상 킷의 현재 상태 파악
python3 scripts/validate-plugin.py <kit-name>
```

검증 결과를 카이젠 컨텍스트에 포함하여 "이미 FAIL 인 항목은 먼저 수정"하고 "PASS 인 항목은 변경으로 깨지지 않도록" 보장한다.

### 가이드 갱신 기준

이 가이드는 다음 상황에서 갱신한다:

- 새 킷 추가 시: §6 킷별 예외 카탈로그에 추가
- 새 검증 카테고리 도입 시: V8~ 형식으로 §3 에 추가
- 기존 체크 기준 변경 시: 해당 V-번호 섹션 수정 + `last_updated` 갱신

가이드 갱신은 `harness-kaizen` 스킬이 담당한다.

---

## 8. 변경 이력

| 날짜 | 버전 | 내용 |
|------|------|------|
| 2026-04-11 | 1.0.0 | 초기 작성 — V1~V7 카테고리, 7개 킷 예외 카탈로그, scripts/validate-plugin.py 구현 |

다음 갱신 예정:
- V8: 에이전트 파라미터 스키마 검증 (tools 목록이 실제 Claude 지원 도구인지)
- V9: README ↔ SKILL.md 스킬 목록 정합성 (README 에 언급된 스킬이 실제 존재하는지)
