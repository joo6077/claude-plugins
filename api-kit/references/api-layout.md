# `.api/` 산출물 레이아웃

api-kit 의 모든 스킬이 읽고 쓰는 디렉토리 구조 정본. 설계 문서
`docs/superpowers/specs/2026-09-02-api-kit-design.md` §6 · §8.3 · §10.2b 를 옮긴 것이다.

---

## 1. 트리

```text
.api/
├── project.yaml              환경 정의 · baseUrl · allowHosts · tier
├── auth.yaml                 auth 프로파일 (시크릿은 참조만)
├── credentials.local.json    id/비번 (gitignore 강제 · 권한 0600)
├── inventory.yaml            엔드포인트 인벤토리
├── cases/*.hurl              실행 케이스 — plain text, 코드리뷰 대상
├── contracts/*.yaml          계약 — 스키마 + assert 수준(partial · pin · exact)
├── snapshots/
│   ├── dev/*.json            baseline (커밋 O)
│   ├── stg/*.json            baseline (커밋 O)
│   └── prod/                 커밋 X — 실 고객 데이터
├── masks/*.yaml              비결정 필드 정규화 규칙
├── ui.html                   정적 뷰어 — 의존성 0 단일 파일
└── reports/                  실행 리포트 (gitignore)
```

**repo 밖**에 하나 더 있다.

```text
~/.cache/api-kit/             토큰 캐시 — 디렉토리 0700 / 파일 0600
```

토큰 캐시를 `.api/` 안에 두지 않는다. 캐시 키는
`환경 + 프로파일 + tokenUrl + clientId + scope + username 해시` 로 분리한다 — stg 토큰이 prod 로
새지 않게 하는 장치다.

---

## 2. 파일별 역할

| 파일 | 쓰는 스킬 | 읽는 스킬 | 내용 |
|------|-----------|-----------|------|
| `project.yaml` | `/api-init` | 전부 | 환경별 `tier` · `baseUrl` · `allowHosts` · `authProfile` · `readOnlyByDefault` · `requiresExplicitConfirm` |
| `auth.yaml` | `/api-init` | `/api-probe` · `/api-verify` | 프로파일 `type`(`oauth2_client_credentials` · `custom_login`) · `tokenUrl` · 시크릿 **참조** · `token.*Path` · `cache` · `inject` |
| `credentials.local.json` | 사용자 (`/api-init` 이 생성 유도) | auth 런타임 | 환경별 `{ id, password }`. **값이 들어가는 유일한 파일** |
| `inventory.yaml` | `/api-init` | 전부 | 그룹 · 엔드포인트 id · method · path · 파라미터 · 헤더 · `sideEffect` 수동 표시 |
| `cases/*.hurl` | `/api-contract` | `/api-verify` | Hurl 실행 케이스. `Authorization: Bearer {{access_token}}` 만 남고 값은 들어가지 않는다 |
| `contracts/*.yaml` | `/api-contract` | `/api-verify` · `api-reviewer` | 모드 · pin assertion · required/optional/미확정 · enum 확정 여부와 근거 표본 수 |
| `snapshots/<env>/*.json` | `/api-probe` | `/api-verify` · `/api-ui` | 시크릿 값만 마스킹한 raw + 정규화 JCS + manifest |
| `masks/*.yaml` | `/api-contract` | `/api-probe` · `/api-verify` | 비결정 필드 경로 registry (타임스탬프 · UUID · 커서 · request id) |
| `ui.html` | `/api-ui` | 사람 | 정적 뷰어. 기본 gitignore (커밋 여부는 미결) |
| `reports/` | `/api-verify` | `/api-ui` | PASS/FAIL · 위반 목록 · canonical diff |

### 시크릿이 값으로 들어가도 되는 파일

`credentials.local.json` **하나뿐이다.** 나머지 전부는 참조만 기록한다.

```yaml
clientIdRef: env:DEV_CLIENT_ID
clientSecretRef: keychain:api-kit/dev-client-secret
credentialsFile: .api/credentials.local.json
```

세 방식(`env:` · `keychain:` · `credentialsFile`)은 택일이다. CI 는 `env:`/`keychain:` 쪽이 맞다.

---

## 3. 스냅샷 — baseline 구조

baseline 은 캐시가 아니라 **리뷰를 거친 증거**다. 세 층을 분리해 보관한다.

| 층 | 내용 | 용도 |
|----|------|------|
| raw (마스킹) | 상태코드 · 원본 헤더 라인 · 본문 바이트. **시크릿 값만** 자리를 유지한 채 마스킹 | 회귀 조사 시 원본 복원 |
| normalized | mask registry 적용 후 RFC 8785 JCS canonical JSON | 계약 비교 입력 |
| manifest | raw digest · normalized JCS digest · redaction registry 버전 · media type · extraction mode · lineage(환경 · 브랜치 · API 버전) | 변조 확인 · 어느 환경의 진실인지 식별 |

주의:

- **마스킹 결과만 저장하고 raw digest 를 안 남기면** baseline 이 증거로 기능하지 못한다.
- **`Content-Encoding: gzip` 이면 digest 가 둘이다** — raw content bytes digest 와 decoded
  representation digest 를 구분해 기록한다.
- 승인본과 실행 산출물을 같은 파일에 섞지 않는다(ApprovalTests 의 `.approved` / `.received` 관례).
  무엇이 승인된 값인지 사라진다.
- main/release baseline 과 feature/WIP baseline 을 같은 파일에 섞지 않는다.
- 환경별로 파일을 나눈다. `staging`·`prod`·`local` 이 한 baseline 을 공유하면 환경 차이가 회귀로,
  회귀가 환경 차이로 오판된다.

**파일명 관례(추론):** `snapshots/<env>/<endpointId>.json`. 엔드포인트 id 가 인벤토리·계약·케이스·뷰어의
공통 키이므로 같은 키를 파일명에도 쓴다. 여러 표본을 보관할 때는 `<endpointId>.<n>.json` 로 늘린다 —
enum·required 승격 판정에 표본 수가 필요하기 때문이다.

---

## 4. 커밋 정책

| 대상 | 커밋 | 이유 |
|------|------|------|
| `project.yaml` · `auth.yaml` · `inventory.yaml` | O | 값이 아니라 구조와 참조만 들어 있다 |
| `cases/*.hurl` | O | plain text 라 git diff 가 읽히고 리뷰 대상이 된다 |
| `contracts/*.yaml` · `masks/*.yaml` | O | 계약과 정규화 규칙은 함께 버전 관리한다 |
| `snapshots/dev/` · `snapshots/stg/` | O | 회귀 diff 의 기준선 |
| `snapshots/prod/` | **X** | 실 고객 데이터. 한 번 history 에 들어가면 영구히 남는다 |
| `credentials.local.json` | **X** | 자격증명 |
| `reports/` | **X** | 실행 산출물 |
| `ui.html` | 기본 X | dev/stg 스냅샷이 인라인되어 diff 가 매우 시끄럽다. 커밋 여부는 미결 — 임의로 정하지 마라 |

prod 는 **계약 스키마만 커밋**한다. 값이 아니라 형태만 남긴다.

### `.gitignore` (`/api-init` 이 등록)

```gitignore
.api/reports/
.api/snapshots/prod/
.api/credentials.local.json
.api/ui.html
.env
```

**등록 실패 시 자격증명 파일을 만들지 않는다.** 그리고 매 실행 전에 파일이 git 추적 대상인지
검사하고, 추적 중이면 중단한다. gitignore 는 **이미 추적 중인 파일을 무시하지 않기** 때문에
`.gitignore` 한 줄로 안전하다고 보고하면 안 된다.

---

## 5. 명명 규칙

| 대상 | 규칙 | 예 |
|------|------|-----|
| 엔드포인트 id | `<그룹>.<동작>` | `orders.list` · `products.inventory` |
| 케이스 파일 | `cases/<endpointId>.hurl` | `cases/orders.list.hurl` |
| 계약 파일 | `contracts/<endpointId>.yaml` | `contracts/orders.list.yaml` |
| 스냅샷 | `snapshots/<env>/<endpointId>.json` | `snapshots/dev/orders.list.json` |
| 필드 경로 | JSONPath, 배열 인덱스 제거 | `$.data[].items[].sku` |

엔드포인트 id 는 **커맨드의 첫 인자**이기도 하다 (`/api-probe orders.list`). 이름을 바꾸면 계약·케이스·
스냅샷·뷰어가 한꺼번에 어긋나므로 `/api-init` 이후에는 바꾸지 않는다.

---

## Gotchas

- **`.gitignore` 등록과 "추적되지 않음" 은 다른 사실이다.** 이미 추적 중인 파일은 gitignore 로 무시되지
  않는다. `git ls-files --error-unmatch <path>` 로 실제 추적 여부를 확인한 결과만 근거가 된다.
- **토큰 캐시를 `.api/` 안에 두지 마라.** repo 안에 있으면 언젠가 커밋된다. `~/.cache/api-kit/` 에 두고
  디렉토리 0700 / 파일 0600 으로 잠근다.
- **환경별 캐시 키를 합치지 마라.** 프로파일 이름만으로 키를 만들면 stg 토큰이 prod 요청에 실린다.
- **baseline 을 실패했다고 자동 승격하지 마라.** 회귀가 새 truth 가 되어 다음 실행부터 green 이 된다.
  승격은 명시적 플래그가 있을 때만이고, CI 자동 갱신은 0회다.
- **비결정 필드를 baseline 에 영구화하기 쉽다.** timestamp·uuid·정렬 순서를 그대로 승격하면 이후 모든
  실행이 실패한다. 승격 전에 mask 규칙부터 확정하고 규칙을 baseline 과 함께 커밋한다.
- **`.hurl` 에 시크릿 값을 쓰지 마라.** wrapper 가 발급을 마친 뒤 임시 `--secrets-file` 로 넘기고,
  파일에는 `{{access_token}}` 템플릿만 남긴다.

---

## References

- `docs/superpowers/specs/2026-09-02-api-kit-design.md` §6 · §8 · §10 — 레이아웃·가드·인증 설계 근거
- `docs/api/contract/snapshot-sealing-canonicalization.md` — raw/normalized/manifest 분리 · JCS 기준
- `docs/api/verification/baseline-governance-promotion.md` — 승인본 분리 · 승격 규칙 · lineage
- `docs/api/execution/auth-secret-lifecycle.md` — 자격증명 파일 · 토큰 캐시 권한
- `project-detection.md` — 이 레이아웃을 감지하는 절차
