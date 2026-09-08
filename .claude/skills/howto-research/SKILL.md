---
name: howto-research
description: >
  howto-kit 의 리서치 문서(docs/howto/)를 외부 1차 출처 폴링으로 갱신한다.
  콘솔 딥링크 관행, UI 지목 어휘, 분기 문장, deprecation 정책, 변경 로그 피드가 대상이다.
  이 레포 개발용 스킬이며 howto-kit 플러그인에 포함되지 않는다.
  tone-research, api-research 와 동일한 패턴.
  "/howto-research", "절차 리서치", "howto-kit 문서 갱신" 같은 요청 시 트리거.
  스킬 자체의 품질 개선에는 트리거하지 않는다 — /howto-kaizen 을 사용한다.
argument-hint: "[category]"
user-invocable: true
---

# Howto Research

`docs/howto/` 리서치 문서를 외부 출처 기준으로 갱신한다.

# Gotchas

1. **출처를 지어내지 마라** — 접근 실패한 URL 은 "확인 실패"로 명시하고 시도 URL 을 남긴다.
   이 킷은 출처 등급 표기가 핵심 자산이라, 검증 안 된 인용 하나가 등급 체계 전체를 무너뜨린다.
   실측: 이 킷의 1 차 리서치에서 4 개 질문 중 2 개가 확인 실패로 끝났고, 그 사실이
   `howto-kit/references/provenance-notes.md` 에 그대로 남아 있다. 그것이 정상 결과다.
2. **확정된 항목은 `provenance-notes.md` 에서 옮기고 인용처도 같이 고쳐라** — 원장만 고치면
   본문에 옛 등급 표기가 남는다. 생성물만 고치면 되돌아간다.
3. **피드 URL 은 바뀐다.** `provenance-notes.md` §3 의 표에 적힌 URL 을 인용하기 전에 다시
   조회한다. "확인일 기준" 이라는 단서 없이 피드 URL 을 사실로 쓰지 마라.
4. **한 번에 한 카테고리만 갱신하라** — 여러 축을 한 사이클에 손대면 무엇이 왜 바뀌었는지
   추적이 끊긴다.
5. **UI 라벨을 수집할 때 로케일 변형 URL 을 같이 확보하라** — 한국어 라벨의 1 차 출처는
   같은 문서의 `ko-kr` 변형이다. 없으면 그 한국어 라벨은 `[추정]` 이다.
6. **리서치는 Codex 에 위임하고 foreground 로 실행하라.** 백그라운드로 던지면 hang 시 결과가
   유기된다. **한 번에 하나만** 띄운다 — 동시 실행하면 앞 작업이 1.4 초 안에 `turn_aborted` 되고
   마지막 것만 살아남는데, companion 이 그 abort 를 감지하지 못해 죽은 작업을 running 으로
   보고한다 (실측: 19 시간). 검색 횟수 하드캡을 프롬프트에 명시한다.
7. **작업 상태를 도구 요약으로 믿지 마라.** `status` 가 running 이라고 해도 rollout 로그
   (`~/.codex/sessions/**/rollout-*.jsonl`)에 `turn_aborted` 가 있으면 죽은 것이다.

# Process

## Step 1. 대상 카테고리 결정

| 카테고리 | 문서 | 1차 출처 |
| --- | --- | --- |
| 딥링크 관행 | `docs/howto/deep-links.md` | 각 벤더 공식 문서 본문에 박힌 콘솔 URL |
| UI 지목 어휘 | `docs/howto/ui-anchoring.md` | Google / Microsoft 스타일 가이드, 벤더 지원 문서 실문장 |
| 분기 문장 | `docs/howto/branch-catalog.md` | `"If you don't see …"` 계열 공식 문장 |
| deprecation 정책 | `docs/howto/deprecation-policy.md` | AWS · Amazon SP-API · Google Cloud 정책 문서 |
| 변경 로그 폴링 | `docs/howto/changelog-feeds.md` | 각 벤더 release notes / RSS |
| 절차 문서 표준 | `docs/howto/procedure-standards.md` | DITA 1.3, ISO/IEC/IEEE 26514·26515 |

`docs/howto/design-brief.md` 는 **설계 정본이지 리서치 문서가 아니다.** 이 스킬이 덮어쓰지 않는다.

## Step 2. Codex 위임 (한 번에 하나, foreground)

`~/.claude/codex-prompt-template.md` 의 `MODE=research` 템플릿을 채운다. read-only 명시.
프롬프트에 이 두 줄을 반드시 넣는다:

- *문서 표기 그대로 추출할 것 (의역 금지)*
- *확인 못 한 것은 "확인 실패" 로 답하고 시도 URL 을 나열할 것*

## Step 3. 반영

변경분만 반영하고 `last_updated` 를 갱신한다. 통째로 덮어쓰지 않는다.
확인 실패 항목은 `howto-kit/references/provenance-notes.md` 에 추가한다.

## Step 4. 하류 갱신

리서치 결과가 킷 규칙을 바꾸면 해당 references 파일도 **같은 커밋에서** 고친다.
`docs/howto/` 만 고치고 끝내면 킷은 옛 규칙으로 계속 동작한다.

# References

- `howto-kit/references/provenance-notes.md` — 미확정 근거 원장 (확정 시 여기서 옮긴다)
- `~/.claude/codex-prompt-template.md` — 위임 프롬프트 템플릿
