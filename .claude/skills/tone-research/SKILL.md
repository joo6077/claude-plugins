---
name: tone-research
description: >
  tone-kit 의 리서치 문서(docs/tone/ 8종)를 외부 1차 출처 폴링으로 갱신한다.
  이 레포 개발용 스킬이며 tone-kit 플러그인에 포함되지 않는다.
  design-research, rust-research 와 동일한 패턴.
  "/tone-research", "톤 리서치", "tone-kit 문서 갱신" 같은 요청 시 트리거.
  스킬 자체의 품질 개선에는 트리거하지 않는다 — /tone-kaizen 을 사용한다.
argument-hint: "[category]"
user-invocable: true
---

# Tone Research

`docs/tone/` 리서치 문서를 외부 출처 기준으로 갱신한다.

# Gotchas

1. **출처를 지어내지 마라** — 접근 실패한 URL 은 "확인 실패" 로 명시한다. 이 킷은 근거 등급 표기가 핵심 자산이라, 검증 안 된 인용 하나가 등급 체계 전체의 신뢰를 무너뜨린다.
2. **한 번에 한 카테고리만 갱신하라** — 8개 문서를 한 사이클에 전부 손대면 무엇이 왜 바뀌었는지 추적이 끊긴다.
3. **자연어 텍스트 탐지 문헌을 코드 근거로 되살리지 마라** — `sources.md` 의 제외 목록에 사유와 함께 적혀 있다. 새 논문을 넣기 전에 대상이 코드인지 텍스트인지 확인한다.
4. **규칙 강도를 출처 강도보다 올리지 마라** — 공식 문서가 권고 수준이면 킷도 권고다. 새 출처가 더 강한 문구를 쓸 때만 등급을 올리고, 그 문구를 인용에 남긴다.
5. **기존 문서를 통째로 덮어쓰지 마라** — 변경분만 반영하고 `last_updated` 를 갱신한다.
6. **리서치는 Codex 에 위임하고 foreground 로 실행하라** — 백그라운드로 던지면 hang 시 결과가 유기된다. 검색 횟수 하드캡을 프롬프트에 명시한다.

# Process

## Step 1. 대상 카테고리 결정

| 카테고리 | 문서 | 1차 출처 |
|---|---|---|
| `stylometry` | `ai-code-stylometry.md` | AI 생성 **코드** 탐지 논문 (EMNLP / SemEval / SANER). 텍스트 탐지 문헌 제외 |
| `comment` | `comment-economy.md` | Google eng-practices · abseil · Ousterhout · Kent Beck |
| `naming` | `naming-taxonomy.md` | Material 3 · Apple HIG · MUI · Fluent · Ant · Carbon · Effective Dart |
| `korean` | `korean-technical-writing.md` | 국립국어원 · 한국 기업 테크니컬 라이팅 |
| `extraction` | `extraction-thresholds.md` | Fowler 카탈로그 · Flutter 공식 성능 문서 |
| `antipattern` | `antipattern-catalog.md` | 코퍼스 재실측 중심 |
| `adapter` | `dart-flutter-idioms.md` | dart.dev · api.flutter.dev · docs.flutter.dev · riverpod.dev |
| `campaign` | `campaign-methodology.md` | 코퍼스 재실측 중심 |

인자가 없으면 `last_updated` 가 가장 오래된 문서를 고르고 사용자에게 확인한다.

## Step 2. 폴링

Codex 에 `MODE=research` 로 위임한다. read-only 를 명시하고 검색 횟수 하드캡을 준다.

프롬프트에 반드시 넣을 것:

- 확인 대상 URL 목록과 "접근 실패 시 확인 실패로 명시하라"
- "존재하지 않는 논문·URL 을 만들어내지 마라 — 확인 실패가 핵심 산출물이다"
- 기존 문서의 현재 주장과 수치. 무엇이 바뀌었는지만 알면 된다

## Step 3. 변경분 추출

| 변경 유형 | 처리 |
|---|---|
| URL 이동·404 | `sources.md` 의 상태를 `주의` 로 바꾸고 새 URL 병기 |
| 새 1차 출처 | 해당 문서에 원칙 추가 또는 기존 원칙의 강도 재평가 |
| 기존 주장 반증 | 원칙을 고치고 변경 사유를 문서에 남긴다 |
| 인용 문구 변경 | 원문 인용을 갱신 |

## Step 4. 문서 갱신

대상 문서의 `last_updated` 를 갱신한다. `sources.md` 에 새 출처를 상태 표기와 함께 추가한다.

references 에 영향이 가면(강도 변경, 새 규칙) 해당 `tone-kit/references/*.md` 도 같이 고친다. **문서만 고치고 references 를 두면 스킬이 옛 규칙으로 판정한다.**

## Step 5. 검증

```bash
python3 scripts/validate-plugin.py tone-kit
python3 scripts/detect-docs-drift.py
```

V1~V8 전부 OK 여야 한다. HTML 페이지가 있으면 drift 도 확인한다.

## Step 6. 커밋

```text
chore(tone-research-<category>): [갱신 요지]
```

# References

- ../../../docs/tone/ — 리서치 문서 8종
- ../../../tone-kit/references/sources.md — 출처 목록과 검증 상태
- ../../../tone-kit/references/adapter-contract.md — 어댑터 슬롯 계약
