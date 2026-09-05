---
name: api-research
description: >
  api-kit 의 리서치 문서(docs/api/ 12종)를 외부 1차 출처 폴링으로 갱신한다.
  이 레포 개발용 스킬이며 api-kit 플러그인에 포함되지 않는다.
  tone-research, rust-research 와 동일한 패턴.
  "/api-research", "API 계약 리서치", "api-kit 문서 갱신" 같은 요청 시 트리거.
  스킬 자체의 품질 개선에는 트리거하지 않는다 — /api-kaizen 을 사용한다.
argument-hint: "[category]"
user-invocable: true
---

# Gotchas

1. **할루시네이션 출처 금지** — 모든 원칙에 검증된 URL 출처 필수. 인용 전 URL 존재를 확인한다.
2. **기존 문서를 덮어쓰지 마라** — 먼저 읽고, 새 정보만 추가·갱신한다. 검증된 기존 내용을 지우지 않는다.
3. **블로그 단독 인용 금지** — 공식 문서·RFC 와 교차 검증한 뒤에만 인용한다.
4. **Hurl 은 실측이 문서를 이긴다** — `docs/api/research-log.md` 의 미검증 항목 표를 먼저 보라.
   로컬에 `hurl` 이 설치돼 있으면 `hurl --version` 과 `--help` 로 대조하고, 문서 기재와 다르면
   **실측을 채택하고 로그에 기록**한다. 특히 `--secret` 의 마스킹 범위는 킷의 redaction 설계
   전체가 걸려 있다.
5. **`pin` 의 의미를 되돌리지 마라** — 2026-09-04 리서치로 '값 고정' 에서 '경로별 명시 assertion'
   으로 재정의됐다. 외부 문서에 `pin` 이 다른 뜻으로 나와도 이 킷의 정의를 바꾸려면
   설계문서 §9.2 와 UI 전반을 함께 고쳐야 한다 — 문서만 조용히 바꾸지 마라.

# Process

## Step 1: 리서치 범위 결정

인자로 카테고리를 주면 그 문서만, 없으면 전체를 대상으로 한다.

```text
docs/api/
├── discovery/     api-inventory-normalization · artifact-interop-import-export
├── execution/     probe-synthesis-hurl-semantics · environment-safety-gates · auth-secret-lifecycle
├── contract/      snapshot-sealing-canonicalization · contract-extraction-modes
│                  multi-sample-pagination-variance · error-status-contracts
└── verification/  regression-diff-failure-policy · static-evidence-viewer-contract
                   baseline-governance-promotion
```

## Step 2: 현재 문서와 로그 읽기

대상 문서 + `docs/api/research-log.md` 를 읽는다. 로그의 **미검증 항목 표**와
**다음 사이클 후보**가 이번 폴링의 우선순위다.

## Step 3: 외부 폴링

Codex 에 `MODE=research` 로 위임한다 (read-only, foreground). 1 차 출처 우선순위:

| 순위 | 소스 |
|---|---|
| 1 | RFC / W3C / IETF 사양 |
| 2 | 공식 문서 (hurl.dev · spec.openapis.org · json-schema.org) |
| 3 | 릴리스 노트 · CHANGELOG |
| 4 | 이슈 트래커 |
| 5 | 엔지니어링 블로그 (교차 검증 후) |

버전이 걸린 주장(Hurl 옵션, OpenAPI 버전, JSON Schema draft)은 **버전과 확인 날짜를 함께** 기록한다.

## Step 4: 델타 판정

새 정보가 기존 원칙을 **바꾸는지** 확인한다. 표현만 다르면 갱신하지 않는다.

- 값이 바뀐 경우 → 문서 갱신 + 로그에 이전값/새값 기록
- 새 원칙 → 추가. 출처 없으면 추가하지 않는다
- 폐기된 정보 → 삭제하지 말고 `[deprecated: YYYY-MM]` 표기 후 대체 원칙 병기

## Step 5: 문서 갱신

`version` 을 올리고 `last_updated` 를 갱신한다. 원칙 수 = 출처 수 1:1 을 유지한다.

## Step 6: 로그 기록

`docs/api/research-log.md` 에 사이클을 추가한다. **판정(CHANGED / NO-CHANGE)과 외부 조회 횟수**를
명시하고, 미검증으로 남은 항목은 표에 남긴다.

# References

- `../../../docs/api/research-log.md` — 미검증 항목 · 이전 사이클 판정
- `../../../docs/superpowers/specs/2026-09-02-api-kit-design.md` — §9.2 계약 실패 기준, §12 확정 결정
- `~/.claude/codex-prompt-template.md` — Codex 위임 템플릿 (MODE=research)
