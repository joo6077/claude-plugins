# Sprint Contract 개정 — tone-kit 문서 가독성 + 템플릿 노출

```yaml
sprint: tone-kit-readability
base_contract: .harness/sprint-contract-tone-kit.md
created: 2026-09-02
branch: feat/tone-kit-readability
iteration: 1
```

기존 계약(조건 50개)은 그대로 유효하다. 이 개정은 **사용자 피드백 2건**에 대응하는 조건을 추가한다.

> "문서화한 거 너무 알아듣기 어렵게 작성되어 있음. 그리고 템플릿은 어딧고"

## 문제 실측 (개정 전)

| 문서 | 줄 | 코드 예시 | 등급·축 메타 언급 |
|---|---|---|---|
| extraction-thresholds | 154 | **1** | 28 |
| comment-economy (주석 문서) | 153 | **1** | 19 |
| naming-taxonomy (네이밍 문서) | 195 | **1** | 25 |
| ai-code-stylometry | 107 | **0** | 6 |

킷이 만든 말 `관측 컨벤션` 47회 등장, 용어집 0개, 입구 페이지 0개. 템플릿 6종은 플러그인 파일로만 존재하고 웹 페이지 0개.

## 추가 완료 조건

### RD — 가독성 (Readability)

| ID | 조건 | 판정 |
|---|---|---|
| RD-01 | 기존 근거 문서 8종이 각각 코드 예시 **10쌍 이상** 보유 | 코드펜스 수 |
| RD-02 | 각 원칙이 `한 줄 결론 → before/after → 왜 → 강도·출처` 순서로 재배치 | 문서 검토 |
| RD-03 | 각 문서 첫머리에 "이 문서가 잡는 것" 요약 + 대표 before/after 1쌍 | 문서 검토 |
| RD-04 | 킷 고유 용어(`관측 컨벤션`·`합성 규칙`·`축`·`어댑터 슬롯`)가 첫 등장 시 풀이됨 | grep |
| RD-05 | **보존**: 기존 출처 인용·URL 이 하나도 삭제되지 않음 | 개정 전후 대조 |
| RD-06 | **보존**: 기존 강도 라벨(MUST/SHOULD/관측 컨벤션)이 하나도 삭제되지 않음 | 개정 전후 대조 |

### EP — 입구·템플릿 (Entry Point)

| ID | 조건 | 판정 |
|---|---|---|
| EP-01 | `docs/tone/overview.md` 존재 — 대표 before/after 10쌍 + 스킬 3종 용도 표 + 용어 3개 풀이 + 완료 게이트 실물 | 문서 검토 |
| EP-02 | `docs/tone/templates.md` 존재 — 템플릿 6종 각각 골격 전문 + placeholder 표 + 실측 + 주의 | 문서 검토 |
| EP-03 | 두 문서가 등급 체계·검증 방법론을 앞부분에 길게 서술하지 않음 | 문서 검토 |
| EP-04 | 컴포넌트·상태 골격이 flutter-toolkit 으로 이관됐다는 사실이 templates 문서에 명시 | grep |

### RV — 규칙 정합 (Rule Consistency)

| ID | 조건 | 판정 |
|---|---|---|
| RV-01 | `S-09`(하위 단위 별도 파일) 규칙이 **개정 전 상태 유지** — thin wrapper 완화가 반영되지 않음 | `core-structure.md` |
| RV-02 | `docs/tone/extraction-thresholds.md` 가 운영 문서와 **같은 규칙**을 말함 — "완화"·"파일 오버헤드 25줄 판정" 서술 0건 | grep |
| RV-03 | 근거 문서와 운영 문서 사이 규칙 모순 0건 | 교차 검토 |

### DS2 — 문서 사이트 (개정)

| ID | 조건 | 판정 |
|---|---|---|
| DS2-01 | `docs/tone-kit/` HTML **10페이지** (기존 8 재생성 + 신규 2) | 파일 수 · mtime |
| DS2-02 | 재생성된 페이지가 개편된 소스 md 를 반영 (코드 예시가 페이지에 실림) | 대조 |
| DS2-03 | 각 페이지 400줄 이상 · accent `#D946EF` · 테마 키 `dk-theme` · CDN 0건 | grep |
| DS2-04 | 다른 킷 색(`20,184,166`·`14B8A6`·`5EEAD4`) 잔존 0건 | grep |
| DS2-05 | `docs/index.html` 에 10페이지 전부 등록 + `getIcon()` 10개 | grep |
| DS2-06 | 페이지 URL 이 전부 대응 소스 md 에 실재 (창작 0건) | 교차 대조 |

### ER2 — 게이트 (회귀)

| ID | 조건 | 판정 |
|---|---|---|
| ER2-01 | `validate-plugin.py` 12 plugins 12 OK · exit 0 | 실행 |
| ER2-02 | `run-evals.py` 전체 PASS | 실행 |
| ER2-03 | `sync-docs` · `sync-orchestrator` · `detect-docs-drift` drift 0 | 실행 |
| ER2-04 | 킷 전체 `TODO`/`TBD`/`FIXME` 0건 · 언어 없는 코드펜스 0건 | V5 · V6 |
| ER2-05 | 프로젝트 고유 식별자 0건 | grep |
| ER2-06 | 타 킷 디렉토리 수정 0건 (flutter-toolkit 포함) | git status |

## 범위 밖

- 기존 계약 50개 조건의 재평가 (이미 APPROVE)
- apps 레포 원본 정리 · 글로벌 메모리 정리 · flutter-toolkit 충돌 8건
- `references/` 9종의 가독성 재작업 — 기계가 런타임에 읽는 운영 문서라 판정표 중심이 맞다

## 판정

전 조건 PASS → APPROVE. FAIL 1건 이상 → REJECT + 수정 지시.
