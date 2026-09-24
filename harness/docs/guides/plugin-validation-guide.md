---
title: Claude Code 플러그인 검증 가이드
version: 1.4.0
last_updated: 2026-09-25
scope: "marketplace.json 에 등록된 킷 전부"
---

# Claude Code 플러그인 검증 가이드

> 릴리스 전 품질 게이트 + 카이젠 베이스라인을 제공하는 10-카테고리 검증 체계.

**이 문서의 용도:** `scripts/validate-plugin.py` 의 각 체크가 무엇을, 왜, 어떻게 검증하는지 정의한다.
새 킷을 추가하거나 기존 킷을 개선할 때 이 문서를 SSOT(Single Source of Truth)로 사용한다.

---

## 1. 목적

플러그인 모노레포는 여러 킷과 100여 개 스킬, 10여 개 에이전트로 구성된다. 킷 수가 늘어날수록 다음 문제가 발생한다.

- **숨은 깨진 링크**: SKILL.md가 references/xxx.md 를 참조하지만 파일이 존재하지 않는다.
- **Frontmatter 누락**: 신규 스킬에 `name` 또는 `description` 이 없어 Claude가 스킬을 인식하지 못한다.
- **트리거 중복**: 두 킷이 동일한 키워드를 트리거로 선언해 의도치 않은 스킬이 실행된다.
- **placeholder 노출**: `TODO`, `TBD`, `FIXME` 가 사용자에게 그대로 보여진다.
- **버전 불일치**: `plugin.json`의 버전과 `marketplace.json`의 description 태그가 달라 릴리스 추적이 깨진다.

이 가이드는 위 문제를 자동으로 탐지하는 10 가지 검증 카테고리(V1~V10)를 정의하고, 각 카테고리의 기준·방법·예외·FAIL 예시를 명시한다. 카이젠 주기마다 이 가이드를 기준으로 전체 킷을 점검하여 품질 저하를 방지한다.

---

## 2. 적용 범위

`.claude-plugin/plugin.json` 을 가진 모든 디렉토리를 검증 대상으로 삼는다. 지금 몇 개인지는 전체 실행의
마지막 `Total:` 줄이 알려준다.

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

## 3. 10 가지 검증 카테고리

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
| -------- | ------ |
| `.json` | `json.loads()` |
| `.yaml`, `.yml` | `yaml.safe_load()` |
| `.toml` | `tomllib.loads()` (Python 3.11 표준) |
| `.ts`, `.js`, `.tsx` | SKIP |
| 기타 | SKIP |

`templates/` 가 없으면 "SKIP (no templates/)" 로 출력하고 PASS 처리한다.

**예외**

- `templates/` 없는 킷: V2 체크 전체 SKIP (어느 킷인지는 §6 킷별 예외 카탈로그 참조)
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

SKILL.md 본문에 등장하는 마크다운 링크가 실제 파일로 해소되어야 한다.
검증 대상 패턴:

- Markdown 링크: `[text](path)`

절대 URL(`https://`, `http://`)과 앵커만 있는 링크(`#section`)는 제외한다. 코드 인라인 경로(예: 본문에 그대로 적힌 상대 경로 문자열)는 V3 범위 밖이다 — 독자가 눈으로 검증한다.

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
- **Cross-kit context disambiguation**: 두 kit 이 exact-match 키워드를 공유해도, 각 kit 의 description 전체가 **kit-specific 고유 단어** (예: flutter-toolkit → `flutter`, `dart`, `HookWidget`, `Riverpod`; react-kit → `react`, `vite`, `tauri`, `shadcn`; rust-kit → `rust`, `cargo`, `axum`) 를 포함하면 **disambiguation 성공으로 간주하여 WARN 제거**. 이는 "같은 개념 다른 프레임워크" 케이스 (예: Flutter "테스트 만들어줘" vs React "테스트 만들어줘") 가 false positive 로 처리되는 것을 방지한다. 구현: `scripts/validate-plugin.py` 의 `KIT_CONTEXT_TOKENS` 상수.

**FAIL 예시**

```yaml
# react-screen/SKILL.md
description: >
  "새 화면 추가", "페이지 추가" 요청 시 트리거.

# flutter-screen/SKILL.md
description: >
  "새 화면 추가" 요청 시 트리거.  # 동일 키워드 → WARNING
```

**PASS 예시 (context disambiguation 적용)**

```yaml
# flutter-toolkit/skills/flutter-test/SKILL.md
description: >
  Flutter 프로젝트에 WidgetTester 기반 unit/widget test 코드를 생성.
  "테스트 만들어줘", "unit test" 요청 시 트리거.
# → "Flutter", "WidgetTester" 가 KIT_CONTEXT_TOKENS["flutter-toolkit"] 과 매칭

# react-kit/skills/react-test/SKILL.md
description: >
  React + Vitest 기반 테스트 코드 생성.
  "테스트 만들어줘", "unit test" 요청 시 트리거.
# → "React", "Vitest" 가 KIT_CONTEXT_TOKENS["react-kit"] 과 매칭

# 결과: "테스트 만들어줘" exact-match 겹침이지만 양쪽 kit 모두 context_hit=True 이므로 WARN 제거
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

### V8 Hook 스크립트 실행 비트

```python
# V8 — see harness/docs/guides/plugin-validation-guide.md §3.8
```

**무엇을 검사하나**: `hooks/hooks.json` 이 **인터프리터 없이 직접 실행**하는 `.sh` 스크립트(`"command": "${CLAUDE_PLUGIN_ROOT}/scripts/x.sh"`)가 실행 비트(mode 0755)를 가지는지 검증한다. git 은 파일 모드를 추적하므로, 스크립트가 `100644`(비실행)로 커밋되면 marketplace clone·plugin cache 등 **모든 설치본**에서 해당 hook 이 `Permission denied` 로 실패한다.

**왜 중요한가**: 2026-06 reflect 로그 30일 집계에서 hook `permission-denied` 계열이 **24개 프로젝트 957건(전체 friction 의 38%)** 으로 단일 최대 마찰원이었다. 근본원인은 `harness/scripts/{env-check,run-guard,sdk-guard}.sh` 와 `design-kit/scripts/env-check.sh` 4종이 `100644` 로 커밋되어 있던 것. SessionStart·PreToolUse hook 은 매 세션·매 Bash 호출마다 발화하므로, 비실행 스크립트 하나가 전 프로젝트에 누적 실패를 만든다.

**직접 실행 vs 인터프리터 경유**: `${CLAUDE_PLUGIN_ROOT}/x.sh` 가 명령의 첫 토큰이면 직접 실행 → exec 비트 필수. `bash ${CLAUDE_PLUGIN_ROOT}/x.sh` 처럼 인터프리터(`bash`/`sh`/`source`)가 앞서면 읽기 권한만 있으면 되므로 V8 대상이 아니다 (예: reflect-kit 의 log-prompt.sh 는 `bash` 경유라 PASS).

**예외**: `hooks/hooks.json` 이 없는 킷은 SKIP 상당(OK, "no hooks.json"). 직접 실행 `.sh` 참조가 0건이면 OK.

**FAIL 예시** — `100644` 로 커밋된 직접 실행 스크립트:

```text
# harness/hooks/hooks.json
{ "command": "${CLAUDE_PLUGIN_ROOT}/scripts/run-guard.sh" }
# 그런데 git ls-files -s 결과 100644 (비실행)
# → FAIL: 직접 실행 hook 스크립트가 비실행 (mode 0o644 — chmod +x 필요)
```

**수정**: `chmod +x <script>` 후 커밋하면 git mode 가 `100755` 로 추적된다. 릴리스(release.sh)로 새 버전을 배포해야 기존 설치본의 cache 가 갱신된다.

---

### V9 스킬 본문의 인자 치환 위험

- **검사 이름**: `arg-substitution` (`--check=arg-substitution`)
- **대상**: 각 킷의 `skills/*/SKILL.md`
- **판정**: 이스케이프되지 않은 `$` + 숫자가 1 건이라도 있으면 FAIL. 파일:라인과 고치는 법을 함께 출력한다
- **왜**: Claude Code 는 스킬 본문의 `$N` 을 `$ARGUMENTS[N]` 으로 치환한다 ([Skills — Available string substitutions](https://code.claude.com/docs/en/skills)). 인자와 함께 호출하면 본문 코드의 `$0` · `$1` 이 그 순번(0 부터)에 들어온 인자 낱말로 바뀌어 awk·셸 스니펫이 깨진 채 로드된다. 2026-09 실측: `sprint-contract` 를 인자와 함께 부른 3 회 모두 frontmatter reader 와 저장 검사 게이트 스니펫이 깨졌고(`fm && 전역 ~ k`), 인자 없이 부른 회차만 멀쩡했다. 레포 전체 SKILL.md 6 개에 23 곳이 있었다
- **고치는 법** (자리마다 다르다)
  - awk 필드: `$(0)` · `$(2)` — awk 에서 괄호형은 같은 필드 참조다
  - bash 위치 인자·스크립트 이름: `${1}` · `${0}` — **`$(0)` 을 순수 bash 에 쓰면 명령 치환이라 `0: command not found` 로 깨진다**
  - SQL 자리표시자처럼 문법상 `$` + 숫자여야 하는 곳: 역슬래시 이스케이프. 로드 시 역슬래시가 제거되어 Claude 는 원래 형태를 본다
- **`--fix` 없음**: awk 인지 bash 인지 판단이 필요해 자동 치환이 위험하다
- **고친 뒤 실행으로 확인**: `$` + 숫자 0 건은 "형태만 바꾼 오류"(`$(1)` 을 bash 에 쓴 경우)를 못 잡는다. 고친 함수를 실제로 한 번 실행해 같은 결과가 나오는지 본다

### V10 마크다운 표 무결성

**무엇을** — 코드 블록 밖의 표행 중 헤더 없이 끊긴 행이 0 개인지 본다.

**왜** — 긴 문서에 절을 끼워 넣으면 표 중간에 들어가 뒷부분이 헤더 없이 남는다.
markdownlint 는 그것을 표로 인식하지 못해 경고 수가 전혀 움직이지 않는다. 실측(2026-09-23):
`contract-schema.md` 의 4 행 표 사이에 소제목이 들어가 마지막 행이 고립됐는데, 같은 파일의
경고 수는 **세 커밋 내리 14 건**이었다 — 167 줄을 넣고 표를 깨고 다시 고치는 동안 1 도
안 움직였다. 경고 수로는 이 붕괴를 볼 수 없다.

**어떻게** — 표행(`|` 로 시작) 중 바로 위가 표행이 **아니고** 바로 아래도 헤더 구분선
(`|` 로 시작하고 파이프 · 붙임표 · 콜론 · 공백만으로 이뤄진 줄)이 **아닌** 행을 고립으로 본다. 정상 표는 헤더 행
다음에 구분선이 오므로 걸리지 않는다.

**범위** — V6 보다 넓다. 킷 안의 `docs/**/*.md` 를 더해 기준 문서(`harness/docs/guides/`)가
검사 대상이 된다. 실제로 표가 끊겼던 자리는 `harness/references/contract-schema.md` 라 원래
V6 범위 안이었다 — 넓힌 이유는 "그 파일이 범위 밖이어서" 가 아니라 "같은 종류의 문서가
`docs/` 에도 있어서" 다 (교차 진단이 이 서술 오류를 짚었다).

스킬 폴더 안의 `skills/*/references/**/*.md` 도 더한다 (2026-09-25). 킷 최상위 `references/*.md` 만 보면 스킬마다
둔 참조 문서가 빠진다 — 실측 14 킷에 41 개(표가 있는 파일 40 개)가 검사 밖이었고 끊긴 표는 0 개였다. V6 는 같은
범위로 넓히지 않았다 — 넓히면 그 안의 언어 힌트 없는 펜스 8 개가 바로 걸린다.

**표행은 왼쪽 공백을 벗겨서 판정한다.** 표는 목록·인용 안에서 들여쓰여 쓰이고, 왼쪽 끝만
보면 그것이 전부 검사에서 빠진다. 실측(2026-09-24): 대상 210 파일에 들여쓴 표행이 84 줄(9 파일)
있었고 그 안에 실제로 끊긴 표가 숨어 있었다 —
`reflect-kit/skills/reflect-promote/SKILL.md` 의 8 행 표 한가운데에 산문 한 문단이 들어가
행 4~7 이 고립돼 있었다. 처음 판은 그것을 못 잡았다.

**`--fix` 없음** — 끊긴 표를 어디로 되돌려야 하는지는 의미 판단이다.

FAIL 출력은 이런 형태다.

```text
FAIL harness/references/contract-schema.md:1036 — 헤더 없이 끊긴 표 행
  (절을 표 중간에 끼워 넣었는지 보라): | `unknown` | PASS 근거 불가 — 표면화 | …
```

## 4. 자동화 사용법

### CLI 옵션

| 옵션 | 설명 | 예시 |
| ------ | ------ | ------ |
| `[plugin]` | 특정 킷만 검증 | `validate-plugin.py react-kit` |
| `--check=<list>` | 특정 체크만 (쉼표 구분) | `--check=frontmatter,refs` |
| `--json` | JSON 출력 (CI 파이프라인용) | `--json` |
| `--fix` | 자동 수정 (V5 + V6만) | `--fix` |
| `--help` | 사용법 출력 | `--help` |

`--check` 에 사용하는 체크 이름:
`frontmatter`, `templates`, `refs`, `triggers`, `placeholders`, `code-fence`, `plugin-json`, `hook-exec`, `arg-substitution`, `table-integrity`

`--help` 도 같은 목록을 보여준다. 그쪽은 등록 표에서 바로 뽑으므로, 이 목록과 다르면 `--help` 가 맞다.

### 출력 포맷

형식 예시다. 수치와 버전 번호는 예로 든 값이다.

```text
=== harness ===
  V1 frontmatter       9 skills + 1 agent — OK
  V2 templates         2 parsed, 1 skipped (ts/js) — OK
  V3 refs              12 links — OK
  V4 triggers          36 keywords — OK
  V5 placeholders      0 found — OK
  V6 code-fence        0 bare — OK
  V7 plugin-json       v0.3.5 matches marketplace — OK
  V8 hook-exec         3 hook 스크립트 실행 가능 — OK
  V9 arg-substitution  9 skills — OK
  V10 table-integrity   18 md files — OK

=== react-kit ===
  V1 frontmatter       21 skills + 3 agents — OK
  V2 templates         5 parsed, 4 skipped (ts/js) — OK
  V3 refs              89 links, 2 BROKEN
    FAIL react-kit/skills/react-skeleton/SKILL.md:42 → references/shadcn-skeleton.md (not found)
    FAIL react-kit/skills/react-skeleton/SKILL.md:67 → ../design-kit/references/token-schema.md (not found)
  V4 triggers          58 keywords, 1 duplicate
    WARN "새 화면 추가" — react-kit / planning-kit (cross-kit)
  V5 placeholders      0 found — OK
  V6 code-fence        0 bare — OK
  V7 plugin-json       v0.1.0 matches marketplace — OK
  V8 hook-exec         no hooks.json — OK
  V9 arg-substitution  21 skills — OK
  V10 table-integrity   32 md files — OK

Total: 2 plugins, 1 OK, 1 ERROR
Exit: 2
```

요약줄은 결과가 있는 상태만 적는다 — 전부 통과하면 `Total: N plugins, N OK` 처럼 짧아진다.

### Exit Code

| Code | 의미 |
| ------ | ------ |
| 0 | 모든 체크 PASS |
| 1 | WARNING 있음 (킷별 예외 카탈로그에 해당하는 특수 케이스 포함) |
| 2 | ERROR 있음 (진짜 FAIL) |

---

## 5. 발견 시 대응

### 자동 수정 (`--fix`)

`--fix` 모드로 안전하게 자동 수정 가능한 두 체크:

| 체크 | 수정 동작 |
| ------ | ---------- |
| V5 Placeholders | `TODO:` → `<설명 필요>`, `TBD` → `<내용 추가>`, `FIXME:` → `<수정 필요>` |
| V6 Code fence | 빈 ` ``` ` → ` ```text ` |

나머지 체크(V1~V4, V7~V10)는 `--fix` 로 수정하지 않는다. 파일 삭제나 링크 재배선 같은 작업은 의미 분석이 필요하므로 위험하다.

### 수동 수정

| 체크 | 수동 수정 방법 |
| ------ | -------------- |
| V1 | SKILL.md 또는 agents/*.md frontmatter 에 누락 필드 추가 |
| V2 | templates/ 의 JSON/YAML/TOML 구문 오류 수정 |
| V3 | 참조 파일 생성 또는 링크 경로 수정 |
| V4 | description 에서 중복 키워드 제거 또는 구체화 |
| V7 | plugin.json 또는 marketplace.json 버전 태그 일치 |
| V8 | `chmod +x <script>` 후 커밋해 git 이 `100755` 로 추적하게 한다 |
| V9 | 자리마다 다르다 — awk 필드는 `$(N)`, bash 위치 인자는 `${N}`, 문법상 `$` + 숫자여야 하는 곳은 역슬래시 이스케이프 (§3 V9) |
| V10 | 표 중간에 끼어든 절이나 문단을 표 뒤로 옮겨 헤더와 행을 다시 잇는다 |

### 카이젠 위임 기준

다음 경우 해당 킷의 `*-kaizen` 스킬로 위임한다:

- V3 FAIL 이 3건 이상: 참조 구조를 재설계해야 할 수준
- V4 중복이 5건 이상: 킷 간 트리거 키워드 체계 재정의 필요
- V1 FAIL 이 3건 이상: 스킬 템플릿 자체가 잘못된 경우

---

## 6. 킷별 예외 카탈로그

| 킷 | V2 templates | 비고 |
| ------- | ------------- | ------ |
| harness | `templates/` 4 항목 — 2 개 파싱, 1 개 SKIP | `project.yaml` · `settings-hooks.json` 파싱, `env.sh` SKIP (`procedures/` 는 디렉터리라 V2 대상 아님) |
| flutter-toolkit | `templates/` 2 파일 — 전부 SKIP | `.md` 는 V2 파서 대상 아님 |
| design-kit | `templates/` 8 파일 — 전부 SKIP | `.html` 은 V2 파서 대상 아님 |
| backend-kit | `templates/` 없음 — SKIP | 스택 무관 가이드. 프레임워크별 스캐폴딩은 각 킷에서 |
| infra-kit | `templates/` 없음 — SKIP | 스택 무관 가이드. 인프라 코드 템플릿 없음 |
| rust-kit | `templates/` 5 파일 — 1 개 파싱, 4 개 SKIP | `rust-init.toml.template` 파싱, `.rs.template` 4 개 SKIP |
| react-kit | `templates/` 9 파일 — TS 파일은 V2 SKIP | `.ts/.js` 4개 SKIP, 나머지 5개(`Cargo.toml.template` 등) 파싱 |
| tone-kit | `templates/` 6 파일 — 전부 SKIP | `.md` 는 V2 파서 대상 아님 |
| 그 밖의 킷 | `templates/` 없음 — SKIP | V2 전체 SKIP |

> TS/JS 파일 V2 SKIP 은 외부 도구(tsc) 의존 없이 검증 불가능하기 때문이다. 이 파일들의 구문 검증은 CI 빌드 단계에서 수행한다.

---

## 7. 카이젠 연동

각 킷의 카이젠 스킬(`*-kaizen`)이 이 가이드를 베이스라인으로 사용한다.
이 §7 이 각 카이젠 스킬(`*-kaizen`)의 "Plugin Validation 결과 반영" 단계의 SSOT(Single Source of Truth)다.
각 카이젠 스킬은 킷 특화 규칙만 로컬에 유지하고, 공통 규칙은 이 섹션을 따른다.

### §7.1 실행 패턴

카이젠 세션을 시작하기 전과 끝낼 때 모두 실행한다.

```bash
# 세션 시작 시 현재 상태 파악
python3 scripts/validate-plugin.py <kit-name>

# 자동 수정 가능한 항목 먼저 (V5 placeholders, V6 code-fence)
python3 scripts/validate-plugin.py <kit-name> --fix --check=placeholders,code-fence

# 세션 종료 시 회귀 없음 확인
python3 scripts/validate-plugin.py <kit-name>
```

### §7.2 우선순위 매핑

| 결과 | 의미 | 처리 |
| ------ | ------ | ------ |
| **ERROR** (FAIL) | V1~V10 중 하나 이상 실패 | 카이젠 개선 우선순위 "높음"에 자동 편입. 이 세션에서 반드시 수정 |
| **WARNING** | V4 trigger 키워드 중복 등 | 우선순위 "중간". description 보강으로 해소 권장 |
| **PASS** | 모든 체크 통과 | 해당 카테고리 skip. 변경으로 FAIL 이 생기지 않도록 주의 |

### §7.3 통합 규칙

- `--fix` 자동 모드는 **V5 placeholders 와 V6 code-fence 만** 수정한다. 다른 체크는 수동 수정.
- V3 refs BROKEN 은 링크 경로 또는 참조 파일을 수동으로 확인한 후 수정한다.
- V1 frontmatter 누락은 1줄 수정이므로 즉시 처리한다.
- V7 plugin-json 불일치가 릴리스 흐름 문제라면 카이젠이 아닌 `scripts/release.sh` (릴리스 스킬)에서 다룬다.

### §7.4 각 카이젠 스킬의 참조 방식

각 카이젠 스킬의 "Step N: Plugin Validation 결과 반영" 섹션은 다음 형식을 따른다:

```markdown
카이젠 세션 시작/종료 시 `scripts/validate-plugin.py <kit-name>` 을 실행하여
전 카테고리 상태를 확인하고 결과를 개선 우선순위에 반영한다.

**실행 패턴, 우선순위 매핑, 통합 규칙**은
`harness/docs/guides/plugin-validation-guide.md §7` 에서 정의한다 (SSOT).
```

킷별 특화 규칙(예외 동작, Library Policy 원칙 등)만 각 스킬 로컬에 유지한다.

### §7.5 가이드 갱신 기준

이 가이드는 다음 상황에서 갱신한다:

- 새 킷 추가 시: §6 킷별 예외 카탈로그에 추가
- 새 검증 카테고리 도입 시: V11~ 형식으로 §3 에 추가 (V10 까지는 이미 쓰였다)
- 기존 체크 기준 변경 시: 해당 V-번호 섹션 수정 + `last_updated` 갱신
- 통합 규칙 변경 시: §7.3 수정

가이드 갱신은 `harness-kaizen` 스킬이 담당한다.

---

## 8. 변경 이력

| 날짜 | 버전 | 내용 |
| ------ | ------ | ------ |
| 2026-04-11 | 1.0.0 | 초기 작성 — V1~V7 카테고리, 7개 킷 예외 카탈로그, scripts/validate-plugin.py 구현 |
| 2026-06-11 | 1.1.0 | V8 hook-exec 추가 — hooks.json 직접 실행 `.sh` 의 실행 비트(0755) 검증. reflect 30일 집계상 hook permission-denied 957건(전체 friction 38%)의 회귀 방지 가드 |
| 2026-09-21 | 1.2.0 | V9 arg-substitution 추가 — 스킬 본문 코드의 `$` + 숫자가 호출 인자로 치환되어 awk·bash 스니펫이 깨지는 것을 막는다. 공식 규칙은 `$N` = `[N]` 이며, sprint-contract 를 인자와 함께 부른 3 회 모두 `read_fm` 의 awk 와 저장 검사 스니펫이 깨져 로드됐다 |
| 2026-09-24 | 1.3.0 | V10 table-integrity 추가 — 헤더 없이 끊긴 표 행을 잡는다. markdownlint 는 고립 표 행을 표로 인식하지 못해 경고 수가 안 움직인다 (실측: 같은 파일 세 커밋 내리 14 건). 범위는 V6 + 킷 안 docs/**/*.md (210 파일, 오탐 0 확인) |
| 2026-09-25 | 1.4.0 | V10 범위에 스킬 폴더 안 `skills/*/references/**/*.md` 를 더했다 — 14 킷 41 개가 검사 밖이었다 (끊긴 표 0 개 확인). V6 는 같은 범위의 언어 힌트 없는 펜스 8 개 때문에 넓히지 않았다 |
| 2026-09-24 | 1.3.1 | 사실 정정 — `--check` 체크 이름 10 개 전부, 출력 예시에 V9 · V10 줄과 실제 요약줄 형식(`Total: N plugins, …`), 수동 수정 표에 V8 · V9 · V10, 킷별 예외 표의 `templates/` 항목 수를 실제 값으로(harness 4 · flutter-toolkit 2 · design-kit 8 · rust-kit 5 · tone-kit 6). 금방 낡는 킷 수 · 카이젠 스킬 수 표기와 부분 킷 목록은 뺐다 |

다음 갱신 예정:

- V11: 에이전트 파라미터 스키마 검증 (tools 목록이 실제 Claude 지원 도구인지)
- V12: README ↔ SKILL.md 스킬 목록 정합성 (README 에 언급된 스킬이 실제 존재하는지)
