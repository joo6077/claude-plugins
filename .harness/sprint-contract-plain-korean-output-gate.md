---
feature: "출력 직전 용어 검사 Stop 훅"
slug: plain-korean-output-gate
created: "2026-09-11 11:35"
complexity: "복잡"
conditions: 22
status: done
owner_session: 13d78b94-efc9-4ba6-8586-d5d9009d3c98
conditions_digest: sha256:cb1ab12850f89880
locked_at: "2026-09-11 11:33"
---

## 배경

사용자가 한 세션에서 세 번 "못 알아듣겠다"고 지적했다. 지금까지의 대응은 `~/.claude/CLAUDE.md`
의 `## Communication` 구간에 "쓰지 마라 / 이렇게 써라" 표를 늘리는 것이었고, 오늘 하루에만
단어 짝 62개 · 138줄이 쌓였다. 그런데 표에 없는 낱말(RPC 등)이 계속 새어 나왔다.

외부 조사 결과 이 방식 자체가 역효과다.

- 규칙 수를 10개에서 160개까지 늘린 실험에서 80개 부근부터 전부 지킨 경우가 0이 됐다
  (arxiv.org/abs/2607.19257 — 정식 게재 전 논문이라 확정 근거는 아니다)
- 긴 대화에서는 처음 준 지시가 8턴 안에 흔들린다 (COLM 2024, openreview.net/pdf?id=60a1SAtH4e)
- 제약을 여러 개 주면 GPT-4 도 21%는 하나 이상 어긴다 (EMNLP 2024,
  aclanthology.org/2024.findings-emnlp.458/)

항공 기술문서 표준(ASD-STE100), 국립국어원 공공언어 지침, 미국 연방 지침은 전부 금지 목록이
아니라 "쓸 수 있는 말 + 판정 규칙" 구조다.

따라서 표를 없애는 게 아니라 **읽는 주체를 바꾼다.** 표는 별도 파일로 빼서 기계가 읽고,
규칙 문서에는 판정 기준만 짧게 남긴다. 표에 없는 새 낱말은 "설명 없는 대문자 약자는 막는다"는
판정 규칙이 잡는다.

## 리서치 소스

- Stop 훅이 답변 전문을 받는지 실측 확인. `~/.claude/hooks/_probe-stop-payload.sh` 로 표본 2개
  수집, 둘 다 `last_assistant_message` 에 답변 전문이 잘림 없이 들어왔다 (1475자 · 1793자).
  표본 2는 다른 프로젝트 세션(`flutter_playwright`)이 남긴 것이다 — 이 훅이 전역임을 확인.
- 기존 훅 3종의 설계를 따른다: `_lib-hook-payload.sh`(공용) · `block-dirwide-autofixer.sh`(막기 +
  끄는 표시 파일) · `lint-contract-oracle.sh`(막지 않고 알리기).

## 범위 경계

대상은 `~/.claude` 아래 5개 경로뿐이다. 이 레포(`claude-plugins`)의 파일은 손대지 않는다.
`~/.claude` 는 git 저장소가 아니므로 변경 범위는 해시 대조로 측정한다.

커버리지 해소: SC-03 — 6종 입력의 개별 이름을 측정 절에 열거했다.
커버리지 해소: ER-01 — 4개 상황의 개별 이름을 측정 절에 열거했다.
커버리지 해소: AR-03 — 기대 집합 5개 파일을 조건에 전부 열거했다.
커버리지 해소: SK-04 — 62개 개별 열거 대신 계약 시점에 생성한 기준 파일
`glossary-baseline.txt`(62줄, 실행 완료)를 오라클로 쓴다. 파일 내용이 열거를 대신한다.

## 회귀 게이트

이 훅은 전역이라 모든 프로젝트의 모든 세션이 소비한다. 오탐이 나면 정상 답변이 막히고,
훅이 죽으면 모든 세션이 영향을 받는다. 그래서 두 가지를 강제한다 —
한 턴에 한 번만 막기(SC-04), 그리고 어떤 실패에서도 통과시키기(ER-01).

## Skill

- [ ] SK-01: `~/.claude/CLAUDE.md` 의 `## Communication` 구간이 20줄 이하다 `[exact]`
      측정: `awk '/^## Communication$/{f=1} f&&/^## /&&!/^## Communication$/{exit} f' ~/.claude/CLAUDE.md | wc -l` 출력이 20 이하. 계약 시점 실측 138
- [ ] SK-02: 같은 구간에 마크다운 표가 0개다 `[exact]`
      측정: 같은 `awk` 출력에 `grep -cE '^\|'` 결과가 0
- [ ] SK-03: 같은 구간이 단어 목록 파일 경로를 글자 그대로 포함한다 `[exact]`
      측정: 같은 `awk` 출력에 `grep -c 'plain-korean'` 결과가 1 이상
- [ ] SK-04: 현재 표의 단어 짝 62개가 하나도 빠짐없이 `~/.claude/rules/plain-korean.md` 로 옮겨진다 `[exact, enumerated]`
      측정: 계약 시점 생성된 기준 파일(scratchpad `glossary-baseline.txt`, 62줄)의 각 줄을 `grep -F` 로 조회해 미발견 0건

## Script

- [ ] SC-01: 단어 목록에 있는 낱말이 든 답변을 훅이 실제로 막는다 `[goal]`
      측정: Stop 페이로드 모양 JSON 을 `bash ~/.claude/hooks/check-plain-korean.sh` 의 stdin 으로 넣어 stdout 에 `"decision":"block"` 이 포함된다
      음성 대조: 단어 목록 파일을 빈 파일로 바꾸면 이 측정이 통과로 뒤집힌다
- [ ] SC-02: 단어 목록에 없는 대문자 약자도 설명 괄호가 없으면 막는다 `[goal]`
      측정: 본문 `RPC 로 붙인다` → 막힘, 본문 `RPC(다른 서버 기능을 불러 쓰는 방식) 로 붙인다` → 통과. 두 결과가 서로 달라야 PASS
      음성 대조: 설명 괄호 검사를 제거하면 두 결과가 같아져 FAIL 한다
- [ ] SC-03: 코드·경로·명령·주소만 든 답변을 위반으로 잡지 않는다 `[exact, enumerated]`
      측정: 6종 입력 — (a) 백틱 인라인 코드 (b) 세겹 백틱 묶음 (c) http 주소 (d) 파일 경로 (e) 명령줄 (f) 마크다운 링크 — 각각 넣어 전부 종료값 0 + stdout 비어 있음
- [ ] SC-04: 한 턴에 한 번만 막는다 `[exact]`
      측정: SC-01 과 동일한 위반 입력에서 `stop_hook_active` 만 `true` 로 바꾸면 stdout 이 비어 있다
      음성 대조: 그 검사를 제거하면 이 입력도 막혀 FAIL 한다
- [ ] SC-05: 막을 때 사유 문자열에 걸린 낱말과 바꿔 쓸 말(또는 해야 할 조치)이 둘 다 들어간다 `[structural]`
      측정: SC-01 의 stdout 을 `jq -r '.reason'` 으로 꺼내 걸린 낱말 문자열과 대체 문자열이 각각 1건 이상 등장

## Error

- [ ] ER-01: 네 가지 실패 상황에서 전부 종료값 0 + stdout 비어 있음 `[exact, enumerated]`
      측정: (a) `PATH` 에서 `jq` 를 뺀 상태 (b) stdin 이 빈 문자열 (c) 깨진 JSON 문자열 (d) 단어 목록 파일이 없는 상태 — 4회 실행
- [ ] ER-02: 끄는 방법이 있고 실제로 동작한다 `[goal]`
      측정: 끄기 표시 파일을 만들면 SC-01 의 위반 입력이 통과하고, 지우면 다시 막힌다
      음성 대조: 표시 파일 검사를 제거하면 두 결과가 같아져 FAIL 한다

## Architecture

- [ ] AR-01: 시험용 훅이 완전히 제거된다 `[exact, enumerated]`
      측정: `~/.claude/hooks/_probe-stop-payload.sh` 부재 + `~/.claude/_probe-stop-payload.json` 부재 + `grep -c '_probe-stop-payload' ~/.claude/settings.json` 결과 0
- [ ] AR-02: 새 훅이 `settings.json` 의 Stop 에 등록되고 JSON 이 유효하다 `[exact]`
      측정: `jq . ~/.claude/settings.json` 종료값 0 + `jq -r '.hooks.Stop[].hooks[].command' ~/.claude/settings.json | grep -c 'check-plain-korean'` 결과 1 이상
- [ ] AR-03: 변경 파일이 정확히 5개다 `[exact, enumerated]`
      Given: 계약 시점에 scratchpad `pk-baseline.txt` 로 20개 파일 해시 기록 완료
      범위: `~/.claude` 최상위 `*.md` `*.json` + `~/.claude/hooks/` + `~/.claude/rules/`. 제외: `~/.claude/.plain-korean-*` 런타임 기록 파일
      기대: 변경·신규 정확히 4개 (`CLAUDE.md` · `settings.json` · `hooks/check-plain-korean.sh` · `rules/plain-korean.md`) + 삭제 정확히 1개 (`hooks/_probe-stop-payload.sh`)

## Anti-patterns

- [ ] AP-02: force push 금지
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 새로 만드는 `rules/plain-korean.md` 대상

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
      적용: Stop 훅 막기 출력은 `_lib-hook-payload.sh` 에 공용 함수로 둔다 — 이 훅 안에만 두지 않는다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다
      적용: `hook_field` 재사용, 끄기 표시 파일 방식은 `block-dirwide-autofixer.sh` 선례를 따른다

## Diagnostics

- [ ] DG-01: `bash -n ~/.claude/hooks/check-plain-korean.sh` 통과 (project.yaml `commands.analyze` 의 `bash -n` 을 이번 변경 파일에 적용)
- [ ] DG-02: N/A (project.yaml `diagnostics.ide_exclude` 가 빈 목록이고 이번 변경에 IDE 진단 대상 언어 파일이 없다)
- [ ] DG-03: 위 측정 명령 실행 출력에 에러/예외 0건
- [ ] DG-04: 이 세션의 다음 턴이 끝난 뒤 `~/.claude/.plain-korean-last.json` 에 판정 기록이 남는다 — 훅이 실제 세션에서 돌았다는 증거
