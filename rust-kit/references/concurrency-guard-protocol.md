# 동시성 가드 프로토콜 (SSOT)

read-check-then-write 경합을 **SQL 술어**로 해소하고, 그 가드가 실제로 동작함을 **판별력 있는
테스트**로 증명하는 절차. rust-kit 안에서 이 규칙의 본문은 **이 파일
(`rust-kit/references/concurrency-guard-protocol.md`) 하나**다 — 소비 표면
(`rust-model` · `rust-test` · `rust-audit` · `rust-reviewer`) 은 이 경로를 **인용만** 하고 규칙을
재열거하지 않는다.

> **왜 생겼나 (2026-08-12 실측 REJECT `ER-02`):** *"신규 통합 테스트가 실제 바이너리를 호출하지
> 않고 독립적으로 재작성한 SQL 로 낙관적 동시성의 일반 동작만 검증한다. **mutation test 로 확정 —
> 실제 코드에서 동시성 가드(`WHERE exercises = $3::jsonb`)를 완전히 삭제해도 이 테스트는 여전히
> 통과한다.**"* 가드는 구현돼 있었고 테스트도 통과했는데, 그 테스트는 가드를 재고 있지 않았다.

---

## 1. 경합은 앱 레벨이 아니라 SQL 술어로 막는다

`SELECT` 로 상태를 읽고 → Rust 코드에서 비교하고 → `UPDATE` 하는 흐름은 두 문장 사이에 다른
트랜잭션이 끼어들 수 있다 (read-check-then-write). 앱 레벨 `if` 는 이 창을 닫지 못한다.

기대 상태를 **`UPDATE` 의 `WHERE` 술어**로 내려 원자적으로 판정한다:

```sql
-- 기대값(읽어온 스냅샷)을 술어에 포함시켜 경합 시 0 행이 갱신되게 한다
UPDATE sessions
   SET exercises = $1, updated_at = now()
 WHERE id = $2
   AND exercises = $3;   -- $3 = 읽을 때 관찰한 값 (stale 이면 매치되지 않는다)
```

- 버전 컬럼(`version = $n`) · 타임스탬프 · 값 자체 스냅샷 중 무엇을 쓰든 원리는 같다.
- `INSERT` 경로의 중복 방지는 partial unique index + `ON CONFLICT` 로 같은 층에서 처리한다.
- 술어를 앱 코드의 사전 `SELECT` 검사로 대체하지 마라 — 그 검사는 창을 좁힐 뿐 닫지 못한다.

## 2. 호출부를 함수로 추출하고 0 행을 `Conflict` 로 올린다

`main()` · 핸들러 본문에 인라인된 `UPDATE` 는 단위 테스트가 불가능하다 (실측 improvement:
*"현재 main() 내부에 인라인되어 있어 단위 테스트가 불가능하므로, 이 UPDATE 호출부를 별도 함수로
추출하라"*). 다음 두 가지를 함께 만족시킨다:

1. 가드 쿼리 호출부를 **이름 있는 함수**로 추출한다 (테스트가 이 심볼을 직접 호출한다).
2. 드라이버가 돌려주는 **영향 행 수가 0 이면 성공으로 흘리지 말고** 도메인 `Conflict` 로 변환한다.
   `rows_affected == 0` 을 무시하면 "갱신되지 않았는데 성공" 이 되어 가드가 있으나 마나다.

```rust
pub async fn apply_exercises(
    pool: &PgPool,
    id: Uuid,
    expected: &Json<Vec<Exercise>>,
    next: &Json<Vec<Exercise>>,
) -> Result<(), DomainError> {
    let res = sqlx::query!(
        "UPDATE sessions SET exercises = $1 WHERE id = $2 AND exercises = $3",
        next, id, expected
    )
    .execute(pool)
    .await?;

    if res.rows_affected() == 0 {
        return Err(DomainError::Conflict);   // 경합으로 스킵됨 — 조용히 Ok 로 흘리지 않는다
    }
    Ok(())
}
```

- 스킵 건수를 카운터로 노출할 때도 **반환 타입에서 conflict 를 구분**한다. 로그만 남기고
  `Ok(())` 를 돌려주면 호출자가 재시도·보고를 결정할 수 없다.
- HTTP 매핑은 `Conflict → 409` (rust-error 3 계층 매핑 규칙).

## 3. 테스트 쌍 — positive 와 stale negative 를 **실 DB** 에서

가드 하나당 테스트 **두 개**를 만든다. 하나라도 없으면 판별력이 성립하지 않는다.

| # | 테스트 | 준비 | 기대 |
| - | ------ | ---- | ---- |
| P | positive | 기대값이 DB 현재 값과 일치 | 1 행 갱신 · `Ok` |
| N | **stale expected value** negative | 읽은 뒤 다른 경로로 행을 변형해 기대값을 낡게 만든다 | 0 행 갱신 · `Conflict` · 상태 미변경 |

- **실행 환경은 실 DB 엔진이다.** `#[sqlx::test]` (테스트 함수마다 새 테스트 DB · `migrations`
  자동 적용 · 성공 시 정리) 또는 `testcontainers` 를 쓴다. 두 경로 모두 `DATABASE_URL` 또는
  Docker 가 필요하다.
- **SeaORM `MockDatabase` 로 N 을 대체하지 마라.** mock 은 `rows_affected` 매핑과 repository
  control flow(0 행일 때 conflict 분기·후속 호출 0 회)까지는 검증하지만, **실제 SQL 술어가 행을
  걸러내는지는 검증하지 못한다.** 두 층은 상호 배타가 아니다 — mock 으로 control flow 를,
  실 DB 로 술어 의미를 각각 검증한다.
- 테스트가 SQL 을 **독립 재작성**하면 결합이 0 이라 가드를 지워도 통과한다 (`ER-02` 의 정확한
  실패 모드). 테스트는 §2 에서 추출한 **함수 심볼** 또는 실제 바이너리
  (`env!("CARGO_BIN_EXE_<name>")`) 를 호출해야 한다.
- 실행 증거는 명령 · **실행된 테스트 수**(`running N tests` 의 `N`) · 종료 코드를 함께 남긴다.
  타깃 필터를 붙였다면 `PKG_TARGETS` 확인이 선행돼야 한다
  (`references/project-detection.md` Step 3a · rust-run Gotcha 9).

## 4. 판정 절차는 정본을 인용한다 (재정의 금지)

이 프로토콜은 **생산 측**(가드를 어떻게 만들고 무엇을 테스트할지)만 정의한다. 판정 절차와
임계 규칙은 아래 정본을 따르며, 여기서 다시 정의하지 않는다.

| 축 | 정본 | 이 프로토콜의 역할 |
| -- | ---- | ------------------ |
| 평가자 판정 | `harness/docs/guides/qa-evaluation-guide.md` §Discriminating Evidence Gate (적용 범위 1 번 = 동시성 가드) | 그 게이트가 요구하는 **결합**과 **음성 대조 지점**을 코드 쪽에서 미리 만족시킨다 |
| 계약 문구 | `harness/references/contract-schema.md` §음성 대조 | 조건에 적을 `음성 대조:` 절의 대상 지점(= §1 의 술어)을 지정해 준다 |

- 계약 조건에는 "어느 구현 지점을 무력화하면 이 측정이 FAIL 하는지" 를 적는다. 이 프로토콜을
  따랐다면 그 지점은 **§1 의 `WHERE` 술어** 또는 **§2 의 0 행 → `Conflict` 분기**다.
- `cargo-mutants` ([mutants.rs](https://mutants.rs/)) 는 "가드를 지워도 살아남는 테스트" 를
  찾는 데 쓸 수 있다. 다만 **결정론적 negative test 를 대체하지 않는다** — 보조 확인 수단이다.
  범위는 이번 변경분 파일·패키지로 한정한다.

## 5. 안티패턴

- 가드 술어는 있는데 `rows_affected` 를 버리는 코드 (0 행이 성공으로 보고된다).
- negative test 없이 positive test 만 두고 "동시성 검증됨" 으로 보고.
- 테스트가 SQL 을 재작성해 "일반적인 낙관적 동시성 동작" 만 확인.
- mock 단위 테스트를 실 DB 통합 테스트로 계층 표기.
- 앱 레벨 `SELECT` → `if` → `UPDATE` 를 원자적 가드로 설명.
