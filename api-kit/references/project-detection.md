# API 프로젝트 감지

api-kit 스킬이 공통으로 실행하는 환경 감지 절차. 스킬은 이 문서를 인용만 하고 자체 감지 표를
만들지 않는다.

---

## Step 0. 적용 범위 선언 (스택 경계)

api-kit 은 **블랙박스**다. 돌아가는 서버를 밖에서 때려 계약을 뽑는다. 평가·생성 대상은 `.api/`
산출물과 **실제 HTTP 응답**뿐이다.

| 대상 | api-kit 적용 | 대신 적용할 것 |
|------|--------------|----------------|
| `.api/**` (계약 · 스냅샷 · 케이스 · 마스크) | O | — |
| 실행 중인 HTTP(S) JSON API 의 응답 | O | — |
| 서버 소스 코드 (핸들러 · 서비스 · 리포지토리) | ✗ | backend-kit · rust-kit 의 audit |
| 소스를 읽고 만드는 테스트 코드 | ✗ | `/backend-test` (화이트박스) |
| gRPC · GraphQL · WebSocket | ✗ | 계약 모델이 다르다 — v0.1 범위 밖 |
| 부하·성능 | ✗ | k6 영역 |

**금지:** 소스 접근을 전제로 한 판정을 계약 감사에 섞지 마라. api-kit 의 존재 이유가 "소스도 문서도
못 믿을 때 실제 응답을 SSOT 로 삼는 것" 이므로, 소스를 근거로 계약을 확정하면 킷의 전제가 무너진다.

---

## Step 1. 리포지토리 루트 고정 (cwd 드리프트 차단)

명령을 실행하기 전에 루트를 **한 번 확정하고 이후 모든 경로에서 고정**한다.

```bash
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
API_ROOT="$REPO_ROOT/.api"
```

`$API_ROOT` 는 `project.yaml` · 스냅샷 · 케이스 · `.gitignore` 검사의 **유일한 기준**이다.
서브디렉토리마다 다른 `.api/` 를 소싱하지 마라.

## Step 2. `.api/` 존재 확인

| 조건 | 결과 |
|------|------|
| `$API_ROOT/project.yaml` 존재 | 계속 진행 |
| 디렉토리는 있으나 `project.yaml` 없음 | 초기화 중단 상태 — `/api-init` 재실행 안내 |
| 디렉토리 없음 | `/api-init` 안내 후 중단 |

`/api-init` 을 제외한 모든 스킬은 여기서 멈출 수 있어야 한다. 산출물을 자기가 만들어내며 진행하지 마라.

## Step 3. OpenAPI 스펙 탐색

```bash
ls openapi.json openapi.yaml openapi.yml swagger.json swagger.yaml 2>/dev/null
find "$REPO_ROOT" -maxdepth 3 -name 'openapi.*' -o -maxdepth 3 -name 'swagger.*' 2>/dev/null
```

런타임 노출 경로(`/v3/api-docs`, `/swagger.json`, `/openapi.json`)도 후보다.

| 조건 | 결과 |
|------|------|
| 스펙 발견 | `HAS_SPEC = true` — 보조 레일(`--spec-conformance` · `--spec-diff`) 사용 가능 |
| 없음 | `HAS_SPEC = false` — **정상 경로다.** 사람 문서 · curl 덤프 · 실측 스냅샷만으로 동작해야 한다 |

스펙이 없다고 실패로 처리하지 마라. 스펙 없는 프로젝트가 1급 지원 대상이다.

## Step 4. 실행 엔진 감지

```bash
hurl --version
```

| 조건 | 결과 |
|------|------|
| 설치됨 | `HAS_HURL = true` — 버전을 기록한다 |
| 없음 | 설치 안내 후 중단. **curl 로 대체 실행하지 마라** — 케이스·캡처·assert 가 전부 다른 산출물이 된다 |

## Step 5. 환경과 tier 확정

`project.yaml` 에서 읽고, `--env` 인자가 있으면 그것이 이긴다.

| 변수 | 값 |
|------|-----|
| `ENV` | 환경 id (`dev` · `stg` · `prod`) |
| `TIER` | `dev` / `stg` / `prod` |
| `BASE_URL` | 해당 환경 baseUrl |
| `ALLOW_HOSTS` | 화이트리스트 — 목록 밖 호스트 요청은 무조건 차단 |
| `READ_ONLY` | `tier: prod` 기본 true |

`TIER = prod` 면 아래가 자동으로 켜진다.

- 자동 실행 허용 메서드는 `GET` · `HEAD` · `OPTIONS` 3개
- 쓰기 메서드는 케이스에 `prodWrite: true` 명시 + 실행 전 대상 목록 확인
- `TRACE` 허용 0회 · non-idempotent 재시도 0회 · cross-host 리다이렉트 0회
- prod auth 프로파일과 토큰 캐시를 다른 환경과 분리
- **메서드만 보고 safe 로 판정하지 마라** — `GET /delete?id=...` 는 메서드가 safe 여도 mutation 이다.
  인벤토리의 `sideEffect: true` 수동 표시를 함께 본다.

## Step 6. 자격증명 소스 감지

세 방식 중 어느 것을 쓰는지 확정한다. 셋은 택일이다.

| 소스 | 감지 | 주의 |
|------|------|------|
| `credentialsFile` | `auth.yaml` 에 `credentialsFile:` 존재 → 파일 존재 + 권한 `0600` 확인 | 권한이 느슨하면 중단 |
| `env:` | 참조된 환경변수가 셸에 있는지 확인 | CI 는 이쪽이 맞다 |
| `keychain:` | macOS keychain / libsecret 접근 가능 여부 | **headless Linux 에는 없다** — `pass`/GPG 또는 환경변수 fallback 경로가 필요하다 |

값을 읽어 출력하지 마라. **존재 여부만** 확인한다.

## Step 7. git 추적 가드 (매 실행 전)

```bash
git ls-files --error-unmatch .api/credentials.local.json 2>/dev/null && echo TRACKED
git ls-files .api/snapshots/prod/ | head -1
```

추적 중인 파일이 하나라도 나오면 **중단**하고 사용자에게 보고한다. `.gitignore` 에 적혀 있다는 사실은
근거가 아니다 — gitignore 는 이미 추적 중인 파일을 무시하지 않는다.

## Step 8. 표본 수 집계

enum 승격 · required 교집합 · exact 자격 판정은 전부 표본 수가 입력이다. 판정 전에 먼저 센다.

```bash
ls "$API_ROOT/snapshots/$ENV"/*.json 2>/dev/null | wc -l
```

| 표본 수 | 가능한 판정 |
|---------|-------------|
| 1 | enum 은 **후보 표시 + 경고만**. required 확정 불가(미확정으로 남긴다). exact 자격 없음 |
| 2 | required 후보를 교집합/합집합 차분으로 제시 가능 |
| ≥3 | enum 승격 가능(distinct ≥2 · 최근 20 관측 신규 값 없음 · domain ≤12). exact 자격 판정 가능(JCS digest variance 0) |

## Step 9. 선택 도구 감지

없어도 기본 경로가 실패하면 안 된다. 전부 옵트인이다.

| 도구 | 감지 | 없을 때 |
|------|------|---------|
| prettier | `npx prettier --version` | `JSON.stringify(obj, null, 2)` 폴백 — 표시 품질만 떨어진다 |
| Schemathesis | `schemathesis --version` | `--spec-conformance` 비활성. `HAS_SPEC` 일 때만 의미 있다 |
| oasdiff | `oasdiff --version` | `--spec-diff` 비활성 |
| Redoc CE | `npx @redocly/cli --version` | `redoc-static.html` 보너스 산출물 생략 |

## Step 10. 감지 결과 요약

스킬은 아래 변수를 확정한 뒤 본 작업을 시작한다.

```text
REPO_ROOT · API_ROOT · ENV · TIER · BASE_URL · ALLOW_HOSTS · READ_ONLY
HAS_SPEC · HAS_HURL · CRED_SOURCE · SAMPLE_COUNT
HAS_PRETTIER · HAS_SCHEMATHESIS · HAS_OASDIFF · HAS_REDOCLY
```

---

## 버전 리터럴 SSOT

api-kit 문서에 적힌 도구 버전은 **2026-09-02 리서치 시점 스냅샷**이다. 아래 표가 이 킷에서 버전 값을
적는 유일한 자리이며, 다른 스킬·기준 문서는 이 절을 인용만 한다.

| 도구 | 버전 (2026-09) | 역할 |
|------|----------------|------|
| Hurl | 8.0.1 (2026-04-28), Apache-2.0 | 실행 엔진 — 단일 바이너리, 런타임 없음 |
| Schemathesis | 4.x | OpenAPI conformance / fuzz (옵트인) |
| oasdiff | — | OpenAPI breaking change 게이트 (옵트인) |
| microdiff | 1.6.0, MIT | 구조 diff — minified 1kB 미만, 의존성 0. 뷰어에 인라인 |
| Redoc CE | 2.5.3 (2026-05-29), MIT | `redoc-static.html` 보너스 산출물 (옵트인) |

버전이 오래됐다고 판단되면 추정하지 말고 리서치로 갱신한 뒤 이 표를 고친다.

---

## Gotchas

- **스펙 부재를 실패로 처리하지 마라.** OpenAPI 없는 프로젝트가 1급 지원 대상이다. 스펙이 없으면
  보조 레일만 끄고 본 경로는 그대로 간다.
- **`hurl` 이 없다고 curl 로 대체하지 마라.** 케이스 파일·캡처·assert 가 전부 다른 산출물이 되어
  회귀 기준선이 깨진다.
- **prod 판정을 메서드로만 하지 마라.** `GET` 인데 사이드이펙트가 있는 엔드포인트가 실무에 존재한다.
  인벤토리의 `sideEffect: true` 를 같이 본다.
- **`.gitignore` 확인과 추적 여부 확인은 다른 검사다.** 둘 다 해야 하고, 근거로 쓸 수 있는 것은
  `git ls-files` 출력이다.
- **표본 1개로 required·enum 을 확정하지 마라.** 오탐 실패 한 번이면 사용자는 도구를 끈다. 확정 대신
  `미확정` 으로 남기고 사용자에게 확정을 요청한다.
- **keychain 을 모든 환경에서 가정하지 마라.** headless Linux 에는 keychain/libsecret 이 없다.
  `pass`/GPG 또는 환경변수 fallback 을 감지 단계에서 확정한다.
- **환경을 바꾸면 토큰 캐시 키도 바뀐다.** 캐시 키는 `환경 + 프로파일 + tokenUrl + clientId + scope +
  username 해시` 조합이다. 프로파일 이름만으로 키를 만들면 stg 토큰이 prod 요청에 실린다.

---

## References

- `api-layout.md` — `.api/` 산출물 레이아웃 정본
- `docs/superpowers/specs/2026-09-02-api-kit-design.md` §3 · §5 · §8 · §10 — 범위 · 도구 선택 · 가드 · 인증
- `docs/api/execution/environment-safety-gates.md` — prod safe allowlist · 재시도 · 리다이렉트 수치 기준
- `docs/api/execution/auth-secret-lifecycle.md` — 자격증명 파일 · 토큰 캐시 권한 · 갱신 시점
- `docs/api/contract/contract-extraction-modes.md` — 표본 수와 승격 기준
