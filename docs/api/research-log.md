---
version: 0.1.0
last_updated: 2026-09-04
---

# api-kit Research Log

## [2026-09-04] — 최초 리서치 (킷 생성)

`/create-kit` Phase 1. 외부 조회는 Codex 5 런(read-only, foreground)으로 수행했고,
그 결과가 `docs/api/` 12 문서의 유일한 외부 근거다.

### 리서치 런

| 런 | 범위 | 소요 | 산출 |
| --- | --- | --- | --- |
| Step 1.1 | 영역 분석 + 12 주제 선정 | 4m 5s | P1 8 + P2 4 주제, Top 10 자동화 대상 |
| 배치 A | 인벤토리 정규화 · Probe/Hurl 의미론 · 상호운용 | 4m 40s | 190 줄 |
| 배치 B | 안전 게이트 · 인증/시크릿 · 오류 계약 | 3m 40s | 192 줄 |
| 배치 C | 스냅샷 봉인 · 계약 추출 모드 · 다중 샘플 | 4m 15s | 167 줄 |
| 배치 D | 회귀 diff · 정적 뷰어 · baseline 거버넌스 | 4m 55s | 237 줄 |

고유 출처 URL **108 개**. 1 차 출처(RFC · 공식 사양 · 공식 문서) 우선.

### 이 사이클에서 뒤집힌 결정

**`pin` 의 의미.** 설계문서 초안은 "지정 필드는 값까지 고정" 이라고 적었는데, 픽스처에서 pin 을
건 `$.meta.total`(주문 총건수)이 매 호출 변하는 값이라 자기모순이었다. 리서치 결과 `pin` 은
조사한 주류 도구 어디에서도 그 뜻으로 쓰이지 않는다 — 발견된 용례는 버전 pin 과 기준 snapshot pin 뿐이다.
필드별 검증 강도의 실제 어휘는 Hurl assert + predicate, Karate schema marker, Pact matcher,
JSON Schema `const`/`enum` 이다.

이름은 UI 전반에 아이콘이 깔려 있어 `pin` 으로 유지하되 **의미를 '경로별 명시 assertion' 으로
재정의**했다. 값 고정은 pin 이 표현할 수 있는 assertion 한 종류일 뿐이다. 상세는 설계문서 §9.2.

### 미검증 항목 — 구현 단계에서 실측 대조 필요

로컬에 `hurl` 바이너리가 없어 아래는 **공식 문서 기재를 옮긴 것이고 실행으로 확인하지 않았다.**
`/api-probe` 구현 시 실제 Hurl 8.0.1 로 대조하라.

| 항목 | 문서에 기재한 값 | 출처 |
| --- | --- | --- |
| 옵션 우선순위 | `env < CLI < [Options]` | hurl.dev/docs/manual.html#configuration |
| `--retry-interval` 기본 | `1000 ms` | hurl.dev/docs/manual.html#run-options |
| `--max-redirs` 기본 | `50` (`-1` 은 무제한) | hurl.dev/docs/manual.html#http-options |
| exit code | `0` 성공 / `1` CLI 파싱 / `2` 입력 파싱 / `3` 런타임 / `4` assert | hurl.dev/docs/manual.html#exit-codes |
| `--secret` 마스킹 범위 | stderr 로그·리포트만. **stdout 응답과 `--json` stdout 은 가리지 않음** | hurl.dev/docs/templates.html#secrets |

마지막 항목이 가장 중요하다 — api-kit 의 redaction 설계 전체가 여기 걸린다.
Hurl 에 맡기지 않고 킷이 자체 scrubber 를 거친 데이터만 저장·렌더한다는 결정(설계문서 §8.2)의
근거이므로, 실측에서 다르게 나오면 §8.2 를 다시 봐야 한다.

### 사용자 확정 (2026-09-04)

리서치가 남긴 열린 질문 4 건에 대한 결정이다. 상세는 설계문서 §12.

| 질문 | 결정 |
| --- | --- |
| `exact` 모드가 헤더까지 보는가 | **본문만.** 헤더는 `Date`·`X-Request-Id` 등이 매번 변해 상시 실패한다. 필요한 헤더는 pin 으로 개별 지정 |
| prod read-only 범위 | **미확정.** 기본 GET/HEAD/OPTIONS 로 두고 allowlist 여지만 남긴다 |
| enum 승격 최소 샘플 | **1 샘플은 후보 표시만(경고), 3 샘플 이상에서 승격.** 오탐 실패가 도구 신뢰를 가장 빨리 깎는다 |
| baseline 에 raw 보관 여부 | **보관.** 단 시크릿 값만 마스킹한 raw |

### 다음 사이클 후보

- Hurl 8.x 실측 대조 후 위 표의 미검증 항목 확정
- JSON Schema 역추론 도구(quicktype · GenSON · json-schema-inferrer) 최신 버전 pinning —
  설계문서 §13 이 이미 미해결로 표시한 항목
- `exact` 모드의 배열 순서 정책 — 순서 보장 없는 컬렉션에 exact 를 허용할지
