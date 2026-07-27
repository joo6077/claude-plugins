---
name: backend-test
description: >
  대상 파일/모듈을 분석하여 백엔드 테스트 코드를 자동 생성한다.
  스택 무관 — 프로젝트 감지 결과에 따라 pytest/jest/JUnit/go test/ExUnit 등
  적합한 프레임워크로 unit test, integration test, API test를 생성한다.
  "테스트 만들어줘", "unit test", "integration test", "API test",
  "테스트 추가", "backend test" 같은 백엔드 프로젝트 요청 시 트리거.
  테스트 실행만 할 때는 프로젝트의 test 명령을 직접 사용한다.
argument-hint: "<file-or-module> [unit|integration|api|e2e]"
user-invocable: true
---

## Gotchas

1. **스택 감지 없이 테스트 코드 생성 금지** — Step 1의 프로젝트 감지를 반드시 먼저 수행하라. Python 프로젝트에 Jest 테스트를 생성하거나 Node 프로젝트에 pytest를 생성하면 안 된다
2. **DB 의존 테스트에 실제 DB 사용 원칙** — 가능하면 Testcontainers/Docker Compose로 실제 DB를 띄워라. Mock DB는 스키마 드리프트를 놓친다. 출처: backend-kit system-principles "Pact v4 + Testcontainers"
3. **API 테스트에서 서버 기동 방식 확인** — 프레임워크의 test client를 우선 사용하라 (FastAPI: `TestClient`, Express: `supertest`, Spring: `MockMvc`/`WebTestClient`, Go: `httptest`). 실제 포트 바인딩은 integration/e2e에서만
4. **테스트 격리 필수** — 각 테스트는 독립 실행 가능해야 한다. 공유 상태(전역 변수, DB 레코드)에 의존하면 순서 의존성이 생긴다. 트랜잭션 롤백 또는 테스트별 시드 데이터를 사용하라
5. **에러 경로 테스트 누락 금지** — happy path만 테스트하면 프로덕션에서 깨진다. 최소한 400/401/404/500 응답 경로를 각각 테스트하라. RFC 9457 problem+json 응답 형식도 검증 대상
6. **Mock 남용 금지** — 외부 서비스(결제 API, 이메일 발송)만 mock하라. 내부 서비스/리포지토리를 mock하면 리팩토링 시 테스트가 깨지고 실제 동작과 괴리가 생긴다
7. **기존 테스트 패턴 무시 금지** — 프로젝트에 이미 테스트가 있으면 그 패턴(디렉토리 구조, 네이밍, fixture 방식, assert 라이브러리)을 먼저 파악하고 따르라. 새로운 패턴을 무단 도입하지 마라
8. **환경 변수 하드코딩 금지** — DB URL, API 키를 테스트 파일에 직접 넣지 마라. `.env.test` 또는 fixture/conftest에서 주입하라
9. **비동기 테스트에서 타임아웃 미설정 금지** — async 테스트는 적절한 타임아웃을 설정하라. 무한 대기는 CI를 멈춘다
10. **ORM 쿼리 테스트 시 N+1 검증 포함** — 리스트 조회 API 테스트에서 쿼리 수를 assert하라. Django: `assertNumQueries`, SQLAlchemy: `connection.execute` 카운트, JPA: Hibernate statistics
11. **Pact v4 + Testcontainers 계약 테스트 (Phase 7 리서치)** — 외부 서비스 연동 코드에는 consumer-driven contract 를 권장. Pact v4 는 REST 외 gRPC / async messaging(Kafka · RabbitMQ) / GraphQL 지원. Pact Broker 는 Testcontainer 로 CI 에서 격리 실행 가능. 출처: [Pact + Testcontainers](https://prgrmmng.com/contract-testing-with-testcontainers-and-pact).
12. **Sibling Consistency (Phase 8 infra-test parity)** — Step 0 스택 감지 독립 단계 + 기존 테스트 패턴 탐색 + 외부 실환경 강제 금지 세 항목은 backend-test / infra-test 공통으로 유지해야 한다. 한쪽만 변경하면 sibling drift 로 평가 불일치 발생.
13. **mock-only 테스트를 integration 으로 명명하거나 보고하지 마라** — MockDatabase·인메모리 대체물만 쓰는 테스트는 단위 테스트다. 파일 경로(`tests/integration/`), 테스트 이름, 완료 보고 세 곳 모두 실제 수준에 맞춰 표기하라. 실측: 글로벌 REJECT `API-01` — "user 통합 테스트(실제 PostgreSQL) 미존재 — MockDatabase 단위 테스트만 있음 `[미검증]`". 근거는 "인메모리 서비스는 프로덕션 서비스의 모든 기능을 갖지 못하고 동작이 조금씩 다르다" 는 Testcontainers 의 문제 정의다. 또한 **테스트 실행 출력 없이 "통과했다" 고 보고하지 마라** — 실행 명령과 출력을 증거로 인용하고, 실행 자체가 불가능하면 `[미검증]` + 사유를 명시한다 (SSOT: `harness/docs/guides/skill-design-guide.md` §3.7 Completion Evidence Gate). 출처: [Testcontainers](https://testcontainers.com/getting-started/).
14. **통합 테스트 실행 전 마이그레이션 적용을 확인하라** — 로컬/CI DB 에 마이그레이션이 안 걸린 상태로 통합 테스트를 돌리면 `column "..." of relation "..." does not exist` 로 깨진다. 실측: 글로벌 REJECT `DG-03` (마이그레이션 미적용으로 통합 테스트 2 건 실패). fixture/conftest 에서 컨테이너 기동 → 마이그레이션 실행 → 시드 순서를 보장하고, 컨테이너를 재사용하는 설정이면 스키마 최신화 경로를 별도로 둔다.
15. **계약 변경 테스트는 양면이다** — 응답 형태·상태코드·직렬화가 바뀌면 provider 테스트만 고치지 말고 consumer 계약 테스트(픽스처 포함)도 같은 스프린트에서 갱신하라. Pact 는 "consumer 와 provider 양쪽 개발을 통제할 때" 를 적용 조건으로 명시하며, provider 의 기능 테스트가 아니라 요청/응답의 **내용과 형식** 일치를 확인하는 도구다. 소비면 코드가 별도 저장소면 그 저장소명과 갱신 필요 파일을 보고에 남긴다 — 조용한 반쪽 완료 금지. 출처: [Pact — What is Pact good for](https://docs.pact.io/getting_started/what_is_pact_good_for), [PactFlow BDCT](https://pactflow.io/bi-directional-contract-testing/).

## Process

### Step 0: 프로젝트 감지

프로젝트 루트에서 아래 파일들을 탐색하여 스택을 감지한다:

| 감지 파일 | 스택 | 테스트 프레임워크 |
|-----------|------|-----------------|
| `requirements.txt` / `pyproject.toml` / `Pipfile` | Python | pytest (기본), unittest |
| `package.json` | Node.js | jest / vitest / mocha |
| `build.gradle` / `pom.xml` | Java/Kotlin | JUnit 5 / TestNG |
| `go.mod` | Go | testing + testify |
| `mix.exs` | Elixir | ExUnit |
| `Cargo.toml` | Rust | → rust-test 스킬로 리다이렉트 |
| `pubspec.yaml` | Dart | → flutter-test 스킬로 리다이렉트 |

**Rust/Dart 프로젝트는 전용 스킬이 있으므로 리다이렉트한다.**

추가 감지 항목:
- ORM: SQLAlchemy / TypeORM / Prisma / Django ORM / JPA / GORM / Ecto
- API 프레임워크: FastAPI / Express / NestJS / Spring Boot / Gin / Echo / Phoenix
- 기존 테스트 디렉토리: `tests/`, `test/`, `__tests__/`, `src/test/`
- 기존 테스트 설정: `pytest.ini`, `jest.config.*`, `vitest.config.*`

### Step 1: 대상 분석

`$ARGUMENTS`에서 대상 파일/모듈과 테스트 유형을 파싱한다.

**유형 미지정 시 자동 추론:**

| 대상 특성 | 테스트 유형 |
|-----------|-----------|
| 순수 함수, 유틸리티, 도메인 로직 | unit |
| DB 모델, 리포지토리, 쿼리 | integration (실제 DB) |
| API 핸들러, 라우터, 컨트롤러 | api (test client) |
| 외부 서비스 연동, 전체 플로우 | e2e |

대상 파일을 읽어 `public` 함수/메서드, 클래스, 의존성(import)을 추출한다.

### Step 2: 기존 패턴 탐색

프로젝트의 기존 테스트를 분석한다:
- 디렉토리 구조 (mirror vs flat)
- import 스타일 및 assert 라이브러리
- fixture/factory 패턴 (conftest, beforeAll, @BeforeEach)
- mock 방식 (unittest.mock, jest.fn, Mockito, gomock)
- 네이밍 규칙 (`test_`, `should_`, `describe/it`, `@Test`)

기존 테스트가 없으면 스택의 커뮤니티 표준 패턴을 사용한다.

### Step 3: 테스트 코드 생성

**공통 규칙:**
- Arrange-Act-Assert (AAA) 패턴 준수
- 각 public 함수/메서드당 최소 1개 테스트
- happy path + error path 모두 커버
- 테스트 이름은 행위를 서술 (what, not how)

**스택별 생성 가이드:**

#### Python (pytest)

```python
# tests/test_{module}.py
import pytest
from {module} import {target}

class TestTargetName:
    """대상 함수/클래스의 행위 테스트."""

    def test_happy_path(self):
        # Arrange
        # Act
        result = target(valid_input)
        # Assert
        assert result == expected

    def test_error_case(self):
        with pytest.raises(ExpectedException):
            target(invalid_input)

# DB 의존 시 — conftest.py에 fixture 정의
@pytest.fixture
async def db_session():
    # Testcontainers 또는 트랜잭션 롤백
    ...
```

#### Node.js (Jest/Vitest)

```typescript
// __tests__/{module}.test.ts
import { describe, it, expect, beforeEach } from 'vitest' // or jest
import { target } from '../{module}'

describe('TargetName', () => {
  it('should return expected result for valid input', () => {
    const result = target(validInput)
    expect(result).toEqual(expected)
  })

  it('should throw on invalid input', () => {
    expect(() => target(invalidInput)).toThrow(ExpectedError)
  })
})

// API 테스트 시 — supertest (Express) / inject (Fastify)
import request from 'supertest'
import { app } from '../app'

describe('GET /api/resource', () => {
  it('should return 200 with list', async () => {
    const res = await request(app).get('/api/resource')
    expect(res.status).toBe(200)
    expect(res.body).toHaveLength(expect.any(Number))
  })
})
```

#### Java (JUnit 5)

```java
// src/test/java/{package}/{Target}Test.java
import org.junit.jupiter.api.*;
import static org.assertj.core.api.Assertions.*;

class TargetTest {
    @Test
    @DisplayName("valid input returns expected result")
    void happyPath() {
        var result = target.method(validInput);
        assertThat(result).isEqualTo(expected);
    }

    @Test
    @DisplayName("invalid input throws exception")
    void errorCase() {
        assertThatThrownBy(() -> target.method(invalidInput))
            .isInstanceOf(ExpectedException.class);
    }
}

// Spring Boot API 테스트
@SpringBootTest
@AutoConfigureMockMvc
class ResourceControllerTest {
    @Autowired MockMvc mockMvc;

    @Test
    void getResource_returns200() throws Exception {
        mockMvc.perform(get("/api/resource"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$").isArray());
    }
}
```

#### Go (testing + testify)

```go
// {module}_test.go
package {pkg}

import (
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestTarget_HappyPath(t *testing.T) {
    result, err := Target(validInput)
    require.NoError(t, err)
    assert.Equal(t, expected, result)
}

func TestTarget_ErrorCase(t *testing.T) {
    _, err := Target(invalidInput)
    assert.ErrorIs(t, err, ErrExpected)
}

// API 테스트 — httptest
func TestGetResource(t *testing.T) {
    req := httptest.NewRequest(http.MethodGet, "/api/resource", nil)
    w := httptest.NewRecorder()
    handler.ServeHTTP(w, req)
    assert.Equal(t, http.StatusOK, w.Code)
}
```

### Step 4: Integration/API 테스트 보강

DB 의존 코드가 감지되면:
1. Testcontainers 설정 안내 (Python: `testcontainers`, Node: `testcontainers`, Java: `org.testcontainers`, Go: `testcontainers-go`)
2. 마이그레이션 자동 실행 포함
3. 트랜잭션 롤백 또는 테이블 truncate 격리

API 핸들러가 감지되면:
1. 프레임워크 test client 사용
2. 요청/응답 스키마 검증 (OpenAPI spec이 있으면 대조)
3. 인증 헤더 fixture 포함

### Step 5: 실행 검증

생성된 테스트를 실행하고 결과를 확인한다:

| 스택 | 실행 명령 |
|------|----------|
| Python | `pytest {test_file} -v` |
| Node.js | `npx vitest run {test_file}` 또는 `npx jest {test_file}` |
| Java | `./gradlew test --tests {TestClass}` 또는 `mvn test -Dtest={TestClass}` |
| Go | `go test -v -run {TestFunc} ./{pkg}/...` |
| Elixir | `mix test {test_file}` |

실패 시 원인 분석 후 수정한다. 의존성 미설치(testcontainers, supertest 등)는 설치 안내를 제시한다.

**증거 규칙 (Gotcha 13)**: 실행한 명령과 그 출력(통과/실패 건수 포함)을 보고에 인용한다. Docker 미설치·DB 접속 불가 등으로 실행이 불가능하면 조용히 넘기지 말고 `[미검증] <사유>` 를 해당 테스트 항목에 붙이고 **부분 완료**로 보고한다.

### Step 6: 결과 보고

생성된 파일 목록, 테스트 케이스 수, 실행 결과를 사용자에게 제시한다.
추가 테스트가 필요한 영역(edge case, 성능, 보안)이 있으면 제안한다.

## References

- `../backend-guide/references/principle-index.md` — 백엔드 원칙 인덱스 (testing 카테고리)
- `../backend-system/references/system-principles.md` — 테스트 전략 원칙 (Pact v4 + Testcontainers)
