# 개정 요구사항 — codex-audit-progress 개정 1 (스킬-02 증거 형태)

작성: Claude (2026-10-06, 세션 fb4aefa8-0ee1-4711-9b22-7baf9c6b989f). 개정 파일과 측정은 Codex 가 쓴다.

## 1. 무엇을 바꾸나

봉인된 스킬-02 는 「VS Code 확장의 부모 세션 · 작업 카드 화면 캡처」를 증거로 요구한다(`measure/ui-review.md`). 이 증거를 「명령줄로 띄운 새 부모 Claude 세션의 기록」으로 바꾼다. 기능 기대(시키지 않아도 부모가 follow 를 백그라운드로 띄움 · 큰 단계 · 오류 · 조용함 경고 · 최종 판정만 15 초 안에 채팅에 옮김 · 요약 줄과 사전 측정 중간 줄은 옮기지 않음 · 6 사례)는 그대로다. 빠지는 것은 화면 캡처와 「VS Code 확장」이라는 실행 장소뿐이다. 그래서 이 개정은 조건을 느슨하게 하는 쪽(relaxing)이다.

## 2. 이유

- Claude 는 사용자의 VS Code 창에서 새 대화를 열거나 화면을 캡처할 수 없다. 사용자가 직접 6 건을 돌려야 하는데, 사용자는 「이건 너가 알아서 진행해」 라고 했다.
- 1 차 실사용(사용자가 VS Code 에서 직접, 2026-10-06 16:30~17:27)은 실패였다: 부모가 6 건 모두 follow 를 시키지 않아도 백그라운드로 띄웠지만, 감독을 앞에서 기다리는 호출로 불러 감독 중 채팅 전달이 0 건이었다. 대화 기록: `/Users/jackson/.claude/projects/-Users-jackson/df0342df-0c76-4ba6-8def-713ae07a3bdf.jsonl`. 이 실패로 문서를 고쳤다(커밋 3f2cf216: 감독을 부모를 막지 않게 띄우고 Monitor 로 큰 단계만 받아 채팅에 옮긴다).
- 명령줄 `claude -p --output-format stream-json --verbose` 세션도 백그라운드 Bash 와 Monitor 알림을 받아 줄마다 답한다(2026-10-06 시험: `단계-1` → `단계-2` → `단계-3` → `끝`, 알림마다 따로 깨어남).

## 3. 사용자 동의

- 질문(AskUserQuestion, 이 세션): 「스킬-02 실사용 확인을 어떻게 끝낼까요?」 — 선택지 「제가 명령줄로 돌리기 (추천)」 설명에 「계약의 VS Code 카드 화면 캡처 요구를 대화 기록의 도구 호출 · 시각 증거로 바꾸는 개정이 필요하고, 이건 조건을 느슨하게 하는 개정이라 여기서 동의를 받습니다」 를 적었다.
- 답: 「제가 명령줄로 돌리기 (추천)」. 세션 기록 `/Users/jackson/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/fb4aefa8-0ee1-4711-9b22-7baf9c6b989f.jsonl` 3200 행, uuid `c7d2591f-afdb-4a7a-8a73-17bd1abab2f6`, `2026-10-06T08:41:34.255Z`.

## 4. 새 증거 (2 차 실사용, Claude 가 명령줄로 실행)

- 시험 프로젝트: `/Users/jackson/Hub/10_Dev/codex-audit-ui-trial` (조건 2 개짜리 인사 스크립트, CLAUDE.md 가 이 가지의 문서 · 스크립트를 정본으로 지정).
- 실행기: `claude -p <메시지> --output-format stream-json --verbose --permission-mode bypassPermissions`, 첫 메시지 뒤로는 `--resume <세션>` 으로 같은 부모 세션에 6 메시지를 차례로 보냈다. 메시지 원문과 순서는 증거 폴더 `drive-trial.py` 사본에 있다. 어느 메시지도 진행 표시를 요청하지 않는다.
- 증거 폴더: `.harness/.meta/codex-audit-progress/evidence/` — `stream-<n>-<verb>-<route>.jsonl`(명령줄 출력), `session.txt`(부모 세션 ID), 그리고 Claude 가 수집해 넣을 부모 대화 기록 사본 · 부모가 띄운 follow 백그라운드 작업의 출력 파일 사본 · Monitor 알림 기록.

## 5. 개정 조건이 재야 할 것

1. 6 사례(draft · revise · impl × direct · delegated)가 모두 있고 같은 부모 세션이다.
2. 사례마다 부모가 사용자 요청 없이 `codex-audit.sh follow` 를 Bash `run_in_background: true` 로 띄웠고, 첫 단계 줄보다 먼저 띄웠다. 평가자 경유 사례에서도 follow 를 띄운 주체는 부모(자식 기록이 아님)다.
3. 사례마다 감독을 부모를 막지 않게 띄웠다(직접: Bash `run_in_background: true`, 평가자 경유: Agent `run_in_background: true`).
4. follow 출력에서 큰 단계 · 오류 · 조용함 경고 · 최종 판정 줄(기존 measure.py 의 `relay_line` 과 같은 분류)마다, 부모가 채팅(assistant 텍스트)에 같은 종류 · 회차 · 결과를 담은 줄을 15 초 안에 남겼다. 활동 요약 · 사전 측정 중간 줄은 채팅에 옮기지 않았다.
5. 독립 검토자(구현자와 다른 새 평가자)가 원본을 직접 대조해 사례별 판정을 쓴 파일이 있고, 증거 파일 해시가 맞는다.

기존 `ui-review.json` 모양을 쓰되 `capture` 를 `stream`(명령줄 출력 파일)으로 바꾸고 `card_visible_during_run` 은 「follow 백그라운드 작업 출력 파일이 감독 중 자랐다」 로 재는 식으로 바꿔도 된다. 측정 묶음 안의 새 파일로 재고, `measure.sh` 는 스킬-02 만 새 측정으로 보낸다. 기존 측정 함수와 다른 조건의 측정은 바꾸지 않는다.

## 6. 제약

- 원 계약 본문 · 봉인 필드는 고치지 않는다. 개정 파일은 `.harness/sprint-amendments-codex-audit-progress.md`.
- 형식은 `harness/references/contract-schema.md` §Amendment 사이드카 와 앞선 본보기 `.harness/sprint-amendments-codex-supervisor.md` 를 따른다.
- 시각 · 식별자는 기계 기록에서 옮긴다. 세션 기록을 직접 읽어 확인한다.
