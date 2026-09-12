---
feature: "코덱스 리서치 파이프라인 업그레이드"
slug: codex-research-pipeline
created: "2026-09-12 18:30"
complexity: "복잡"
conditions: 24
status: done
owner_session: f78b65b1-72bb-4a83-b95b-830105b329d7
conditions_digest: sha256:ac123adad76df78c
locked_at: "2026-09-12 18:30"
---

## 배경

코덱스 리서치가 "개선이 필요한" 상태가 아니라 네 군데가 실제로 고장나 있다는 것을 실측으로 확인했다.

- 로그 수집 훅이 2026-09-02 이후 10일째 아무것도 담지 못했다. 세션 기록은 555개 쌓였는데 9월 로그 엔트리는 4건에서 멈춰 있다. codex CLI 0.154.0 이 세션 기록 형식을 `event_msg.item_completed.item` 구조로 바꿨는데 훅은 옛 `user_message`/`agent_message` 만 찾는다. 못 찾으면 "담을 게 없다"로 판정하고 조용히 버리면서 처리 완료로 표시한다. 오늘 세션 14개 중 11개가 그렇게 사라졌다.
- 처리 완료 목록 상한이 500인데 세션 파일은 555개다. 상한 밖으로 밀려난 파일이 다시 담긴다. 2026-04 로그는 서로 다른 세션 15개가 1302번 기록돼 25MB가 됐다.
- 훅은 `task_complete` 가 없으면 건너뛴다. 주 실패 모드인 멈춤이 바로 그런 경우라 개선의 근거가 되어야 할 실패가 영영 안 남는다.
- 템플릿이 멈춤 원인을 검색으로 오진하고 "내장 웹검색을 절대 쓰지 마라"를 박아뒀다. 전수 실측 결과 검색 횟수와 멈춤은 무관하다.

## 리서치 소스

측정 근거 — 세션 기록 556개 전수 스캔 (`~/.codex/sessions/**/rollout-*.jsonl`).

- 완료 481 / 미완료 75. 검색 0회도 미완료율 11.5%(16/139), 검색 6회 이상은 13.9%(54/389). 검색과 멈춤은 무관.
- 버전별 미완료율: 0.136.0 = 7.5%(n=200), 0.150.1 = 0%(n=9), 0.152.1 = 5.3%(n=19), 0.153.4 = 26.9%(n=78), 0.154.0 = 23.8%(n=21). 0.153.4 부터 3~4배 급등.
- 호출 경로별 미완료율: companion 경유(`Claude Code`) 14.0%(n=507) vs `codex exec` 직접 6.2%(n=32).
- 미완료 75건 전부 최종 답변 0개. 끊긴 지점은 Reasoning 8 · WebSearch 7 · CommandExecution 5 · UserMessage 4 로 흩어져 특정 도구 탓이 아니다.

1차 출처.

- openai/codex 이슈 #44842 — 중첩 `codex exec` 가 stdout 이벤트 없이 침묵하다 호출자 타임아웃. 영향 0.153.4, 미해결.
- openai/codex 이슈 #45009 — `--model` 미지정 시 모델 자동 전환(0.153.0~0.153.4).
- `~/.codex/skills/.system/openai-docs/references/latest-model.md` — `gpt-5.6-sol` 플래그십, `gpt-5.6-terra` mini급, `gpt-5.6-luna` nano급(고처리량·단순·저지연).
- `~/.codex/skills/.system/openai-docs/references/prompting-guide.md` — 가벼운 프롬프트가 평가 점수 10~15% 상승, 토큰 41~66% 감소. "GPT-5 계열은 프롬프트 계약을 엄격히 따르므로 모순된 규칙이 누락된 세부보다 큰 불안정을 만든다." grounding 5원칙과 권장 뼈대(Role/Personality/Goal/Success criteria/Constraints/Tools/Output/Stop rules).
- `sh ~/.codex/skills/.system/openai-docs/scripts/resolve-latest-model-info` 실행 결과 — 최신 모델 `gpt-6-astra`.
- codex 위임 1회 실행(`codex exec --model gpt-5.6-sol -s read-only`) — `gpt-6-astra` 는 `none` 추론 강도 미지원, 이전에 `none`/`minimal` 을 썼다면 `low` 부터.

## GAP 분석

`~/.codex/config.toml` 기본 모델이 `gpt-5.6-luna`, 즉 nano급이다. 리서치라는 최고난도 작업을 가장 작은 모델에 맡겨 왔다. `--model` 전면 금지 규칙(CLAUDE.md, codex-kaizen 4곳)이 그 상태를 고정시키고 동시에 #45009 자동 전환에도 노출시킨다.

템플릿은 기준 모델이 gpt-5.5 로 두 세대 낡았고, 멈춤 오진에서 나온 지시가 리서치 품질을 직접 깎는다. 내장 검색을 금지하고 셸 조회만 쓰게 하면 조회 품질이 떨어지는데, 정작 그 셸 우회는 2026-09-12 18:10 시도가 미완료로 끝나 검증된 적이 없다.

## 범위 경계

바꾸는 파일은 4개다. 레포 안은 `reflect-kit/skills/codex-kaizen/SKILL.md` 하나뿐이고 나머지 셋은 레포 밖(`~/.claude/`)이라 `git diff` 로 재지 않고 파일 내용으로 측정한다.

이번 범위에 넣지 않은 것 — 2026-04 로그 25MB 중복분 정리, `~/.codex/config.toml` 기본 모델 변경, codex 버전 회귀 자체의 수정(상류 미해결 버그).

기준선(계약 작성 시점 1회 실행): `HEAD=921bd2e`, 브랜치 `main`, 미추적 파일은 `00000.log` 와 이 계약 파일뿐.

## 회귀 게이트

훅은 `CODEX_SESS_DIR` / `CODEX_LOG_DIR` / `CODEX_STATE` 환경변수로 격리 실행이 가능하다(`harvest-codex-log.sh:12,15-17`). 훅 관련 조건은 전부 글자 찾기가 아니라 실제 실행으로 판정한다. 구형식 세션 기록도 계속 읽히는지를 별도 조건으로 두어 신형식 대응이 옛 동작을 깨지 않는지 확인한다.

## Script

- [ ] SC-01: 신형식 세션 기록(`event_msg.item_completed.item.type` 이 `UserMessage`/`AgentMessage`)에서 프롬프트와 최종 응답을 추출해 로그에 엔트리 1건을 만든다 [goal] (측정: 오늘자 rollout 1개를 빈 디렉터리에 복사 → `CODEX_SESS_DIR`/`CODEX_LOG_DIR`/`CODEX_STATE` 를 임시 경로로 지정해 훅 2회 실행(1회차는 목록 씨뿌리기) → 생성된 로그에 `grep -c '^## '` == 1 이고 프롬프트 본문이 빈 문자열이 아니다. 음성 대조: 신형식 분기를 지우면 프롬프트가 비어 엔트리 0건이 된다)
- [ ] SC-02: 구형식 세션 기록(`event_msg.type` 이 `user_message`/`agent_message`)도 계속 추출한다 [goal] (측정: 2026-08 rollout 1개로 SC-01 과 같은 절차 → 엔트리 1건. 음성 대조: 구형식 분기를 지우면 0건이 된다)
- [ ] SC-03: `task_complete` 가 없는 세션 기록을 실패로 기록하고, 마지막 항목 종류를 엔트리에 남긴다 [goal] (측정: 미완료 rollout 1개로 격리 실행 → 엔트리 1건이 생기고 그 안에 마지막 항목 종류 문자열이 있다. 음성 대조: 미완료 skip 로직이 남아 있으면 0건이 된다)
- [ ] SC-04: 같은 세션 기록에 훅을 연속 실행해도 엔트리는 1건만 남는다 [goal] (측정: 같은 임시 환경에서 훅 3회 실행 → `grep -c '^## '` == 1)
- [ ] SC-05: 그 실행의 검색 활동 수를 엔트리에 기록한다 [structural] (측정: 검색을 쓴 rollout으로 격리 실행 → 엔트리에 검색 횟수 필드가 있고 값이 1 이상)

## Error

- [ ] ER-01: 세션 파일 수가 처리목록 상한을 넘어도 이미 기록한 것을 다시 기록하지 않는다 [goal] (측정: 같은 rollout을 이름만 바꿔 상한+10 개 복사 → 훅 2회 실행 → 이름별 엔트리 개수를 전수 세어 최대값 == 1. 음성 대조: 상한을 세션 수보다 작은 고정값으로 되돌리면 2회차에서 중복이 생긴다)
- [ ] ER-02: 깨진 입력(잘린 JSON 줄, 빈 파일, 읽기 권한 없는 파일)이 있어도 훅은 `exit 0` 으로 끝난다 [goal] (측정: 세 가지 깨진 픽스처를 넣고 실행 → 종료 코드 == 0)
- [ ] ER-03: 기존 로그 파일의 기존 엔트리를 고치거나 지우지 않고 덧붙이기만 한다 [goal] (측정: 기존 엔트리가 든 로그 파일을 준비해 실행 → 실행 후 파일의 `head -c <원본크기>` 가 원본과 바이트 단위로 동일)

## Architecture

- [ ] AR-01: 템플릿에서 틀린 지시 3종이 사라졌다 — 내장 웹검색 금지, 멈춤 원인이 검색이라는 서술, `-s read-only` 라서 내장 검색이 유일 통로라는 서술 [exact, enumerated] (측정: `~/.claude/codex-prompt-template.md` 전체에서 `내장 웹검색`·`내장 검색이 유일`·`검색.*hang\|hang.*검색` 각 패턴 `grep -c` 0건. 검사 전 `wc -l` 로 범위 출력)
- [ ] AR-02: 템플릿 상단 기준 모델이 현행(`gpt-6-astra` 및 `gpt-5.6-sol`)으로 적혀 있고 `template_version` 이 `2026-09-12-b` 에서 올라갔으며 변경 이력 한 줄에 근거 출처가 붙어 있다 [exact] (측정: `grep '^\*\*template_version'` 출력이 `2026-09-12-b` 와 다르고, 기준 모델 줄에 `gpt-6-astra` 와 `gpt-5.6-sol` 이 둘 다 있다)
- [ ] AR-03: 템플릿의 리서치 지침에 grounding 5원칙이 모두 있다 — 가져온 출처만 인용, 주장마다 뒷받침 출처, 추론과 확인된 사실 구분 표시, 출처 간 충돌 명시, 근거 없으면 추측 대신 못 찾았다고 보고 [structural, enumerated] (측정: `awk` 로 `MODE=research` 절만 잘라내어 다섯 항목에 대응하는 문장이 그 절 안에 각각 1건 이상. 절 밖 문구로 통과시키지 않는다)
- [ ] AR-04: `~/.claude/CLAUDE.md` 의 Codex 위임 규칙에서 `--model` 전면 금지가 사라지고 리서치·구현에 `gpt-5.6-sol` 이상을 지정하라는 지침으로 바뀌었다 [exact] (측정: `awk` 로 해당 절만 잘라내어 `--model.*금지\|금지.*--model` 0건이고 `gpt-5.6-sol` 1건 이상)
- [ ] AR-05: 이번 스프린트가 바꾼 파일은 정확히 4개다 — `harvest-codex-log.sh`, `codex-prompt-template.md`, `CLAUDE.md`, `codex-kaizen/SKILL.md` [exact, enumerated] (Given: 구현 완료 후 커밋 전. 측정: 레포 안은 `git status --porcelain -- reflect-kit` 가 `codex-kaizen/SKILL.md` 한 줄만 출력. 레포 밖 3개는 `find ~/.claude -maxdepth 2 -newer <기준파일> -type f` 목록이 정확히 그 3개이고 다른 `~/.claude` 파일이 섞이지 않는다)

## Skill

- [ ] SK-01: `codex-kaizen` 이 새 로그 형식을 읽도록 갱신됐고 실패 엔트리와 검색 활동 수를 신호로 쓰는 서술이 신호 수집 절에 있다 [structural] (측정: `reflect-kit/skills/codex-kaizen/SKILL.md` 의 `### 1. 신호 수집` 절만 `awk` 로 잘라내어, 실패 엔트리를 읽는다는 문장과 검색 활동을 읽는다는 문장이 각각 1건 이상)
- [ ] SK-02: `codex-kaizen` 에서 `--model` 금지 규칙이 4곳 모두 제거·교체됐다 [exact, enumerated] (측정: 파일 전체에서 `--model.*금지\|금지.*--model\|--model.*넘기지` 0건. 검사 전 `wc -l` 로 범위 출력)
- [ ] SK-03: `codex-kaizen` 의 gpt-5.5 기준 서술이 현행 기준으로 바뀌었다 [exact, enumerated] (측정: `grep -c 'gpt-5\.5'` 가 0건이거나, 남은 것이 과거 기준임을 밝히는 이력 문장뿐임을 해당 줄 출력으로 확인)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (측정: `python3 scripts/validate-plugin.py --check=code-fence reflect-kit`)
- [ ] AP-04: SKILL.md frontmatter 의 name 필드 누락 금지 (측정: `python3 scripts/validate-plugin.py reflect-kit`)

## Reusability

- [ ] RE-01: 훅에서 세션 기록을 읽어 구조로 바꾸는 부분이 하나의 함수로 모여 있어 다른 곳에서 같은 규칙을 참조할 수 있다 [goal]
- [ ] RE-02: 새 훅 파일·새 로그 디렉터리·새 상태 파일을 만들지 않고 기존 경로를 그대로 쓴다 [exact] (측정: `~/.claude/hooks/` 와 `~/.claude/codex-research-log/` 에 새 파일이 추가되지 않았다)

## Diagnostics

- [ ] DG-01: `bash -n ~/.claude/hooks/harvest-codex-log.sh` 문법 오류 0건
- [ ] DG-02: 편집기 진단 경고·정보 0건 (제외 목록 없음, 맞춤법 검사 제외)
- [ ] DG-03: 훅 격리 실행 출력에 파이썬 오류 추적 0건 (측정: 전체 격리 실행 로그에 `Traceback` 0건)
- [ ] DG-04: 실제 환경에서 훅을 1회 실행해 오류 0건이고 9월 로그에 새 엔트리가 쌓인다 (측정: 실행 후 `~/.claude/codex-research-log/2026-09.md` 의 `grep -c '^## '` 가 실행 전보다 크다)
