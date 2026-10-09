# Sprint Feedback
Feature: 리서치 진행을 채팅에 — Codex 가 그사이 한 말 · 검색 · 열람 · 명령을 30초마다
Evaluated: 2026-10-09 18:05
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-research-activity/.harness/sprint-contract-codex-research-activity.md
- sha256: 75d9f9fe9a1364c38a5b921f6bd8a9140ecc95098a3631ee929578c21f8746cd
- status: active
- slug: codex-research-activity
- 선택 근거: ladder 1 명시경로 (호출 인자)
- legacy_contract_used: false
- seal_status: unavailable (스키마 함수 추출 실패) — 대신 봉인 커밋 f3b8379a 와 현재 계약 파일의 차이가 0 줄임을 직접 확인
- 재확인: 일치 (평가 전 sha 와 저장 직전 sha 동일)
- codex_audit.mode: off → 직접 판정

## Amendments
- amendments: 0 (사이드카 없음)

## Deletions
- deletions_range: ae918dab..HEAD
- 커밋 구간 삭제: 0
- 선언 밖 삭제: 0

## Cross-Diagnosis Handoff
- 상태: done (부모가 새 평가자로 실행, 결과는 아래 Cross-Diagnosis 절)
- 부모가 넘길 것: 계약 절대경로 + 이 판정 전문
- 부모가 물을 두 가지: (1) 의도와 다르게 해석한 조건이 있는가 (2) 0 건 · 빈 출력으로 통과한 조건 중 문제가 있어도 0 을 냈을 측정이 있는가


## Cross-Diagnosis
- 판정을 뒤집는 결함 없음 · 높음 0
- 중간 — 진단-04 증거는 경과 표기를 「N분 S초」로 바꾸기 직전 판의 진짜 실행이다(실행 17:47~17:51, 수정 17:51:52). 최종 판은 가짜로만 잼. 진짜 실행에서 활동이 맨 끝 주기에만 나온 이유는 기록 시각으로 확인(첫 말 08:50:30, 시작 08:47:44)
- 중간 — 6 줄 상한이 앞쪽(오래된) 활동을 남기고 최신을 「그 밖에 N개」로 숨긴다. 실제 기록 하나를 처음부터 읽히면 55 개 중 6 개만 보임. 후속: 최신 쪽을 남길지 사용자 판단
- 중간 — 사용량 표기가 시작 「남은 한도 약 N%」· 머리 줄 「5시간 N% · 주간 N%」(쓴 양) · 끝 「남은 한도 100%」(다른 세션 기록을 짐작) 로 엇갈린다. 끝 줄은 원래 동작(`remaining_percent`)이지만 이제 채팅에 나란히 보인다. 후속
- 낮음 — 시도 3 회 최악 1800 초 + 시작 대기 > Monitor 30 분 상한, 끊기면 완료 · 실패 줄 없이 끝날 수 있다(정리 trap 은 있음) · `.activity` 상태 파일이 출력 파일 옆에 남는다 · 변수 약식 · 반복문 꼴 명령(약 94/2121)은 건너뜀(계약 의도) · 한 호출에서 같은 주소가 열람 · 찾기로 두 줄 · `sleep 1` 로 파이썬 호출이 두 배(CPU 1% 수준)
- 실제 기록 908 파일 대조: 검색어 1945 개 전부 읽힘(`\"` 포함 635), 열람 주소 381 · 내부 번호 999 걸러짐, 16MB 기록 한 번 읽기 0.85 초
## Results

### Script (10/10)
- [x] 스크립트-01 — PASS. `check.py activity` 종료 코드 0, FAIL 0줄. 말 · 검색 2 · 열람 · 명령 각 줄과 머리 줄 5개(기준 2 이상) 확인. L3: 래퍼 diff 의 activities() 가 message/commentary 와 custom_tool_call 입력을 읽음
- [x] 스크립트-02 — PASS. `forms` FAIL 0. 내부 번호 0 번, `  명령: ` 정확히 1 개. 래퍼에서 http/https 로 시작하는 ref_id 만 통과시킴
- [x] 스크립트-03 — PASS. `once` 여섯 글자 전부 정확히 1 번 (enumerated 6/6 개별 출력). 읽은 자리를 state 파일에 저장
- [x] 스크립트-04 — PASS. `answer` FAIL 0. 표준 오류 QQZ 0 번, 표준 출력 · 출력 파일엔 있음, 완료 줄 있음
- [x] 스크립트-05 — PASS. `length` FAIL 0. 200자 초과 줄 0, 긴 말 한 줄 + `…`
- [x] 스크립트-06 — PASS. `burst` 측정값: 들여쓴 줄 7 (기준 <= 7), `…그 밖에 6개` 있음
- [x] 스크립트-07 — PASS. `retry` 종료 코드 0, 네 항목 + 실패 줄 전부 (enumerated 4/4)
- [x] 스크립트-08 — PASS. `flush` 여섯 활동이 완료 줄보다 앞(60~174 < 217), 실패 시도 활동 79 < 105
- [x] 스크립트-09 — PASS. `partial` 검색어 정확히 1 번, Traceback 0. 래퍼는 마지막 줄바꿈까지만 읽음
- [x] 스크립트-10 — PASS. `monitor` 문서 명령 정확히 1 개를 원문 그대로 꺼내 실행, 진행 줄 · 완료 줄 있고 QQZ 0 번, 출력 파일엔 최종 답

### Error (1/1)
- [x] 오류-01 — PASS. `corrupt` 종료 코드 0, 깨진 줄 뒤 말 · 다음 묶음 열람 확인, Traceback/Error 0, 출력 파일 최종 답 있음

### Architecture (2/2)
- [x] 구조-01 — PASS. `docs` 10 항목 전부 PASS (CLAUDE.md · 템플릿 각각 호출 줄 정확히 1, Monitor · 명령 · 접두 네 개, 작업 카드+codex-research 줄 0). CLAUDE.md:42 직접 확인
- [x] 구조-02 — PASS. 두 메모 파일 `grep -c Monitor` 각 1, `grep -c '작업 카드로 본다'` 각 0. MEMORY.md:22 에 새 문구. 양성 대조(고치기 전 MEMORY.md 에서 1)는 계약이 16:39 실측으로 제시

### Anti-patterns (N/A 1)
- 금지-00 N/A — 바꾼 파일이 레포 밖 ~/.claude 와 .harness/.meta 뿐이라는 사유가 사실임 (레포 플러그인 파일 변경 0)

### Reusability (2/2)
- [x] 재사용-01 — PASS. `reuse` 진행 줄 함수가 이 차례 세션 기록을 읽음
- [x] 재사용-02 — PASS. `find "$SESS_DIR"` 2 곳 유지, `progress_every` 정하는 줄 1 줄 유지

### Diagnostics (1/1, N/A 3)
- 스킬-00 N/A — 측정값: 변경 파일 중 SKILL.md 0 개 (git diff ae918dab..HEAD)
- 진단-01 N/A — 측정값: release.sh 변경 0 (사유가 사실)
- 진단-03 N/A — 같은 명령 0
- [x] 진단-02 — PASS. `bash -n` 0, `shellcheck -S warning` 출력 0 줄 (양성 대조: SC2164 샘플이 10 줄 — 도구가 살아 있음), check.py · fake/codex ast.parse 0
- [x] 진단-04 — PASS. `evidence` FAIL 0. 증거 첫 줄이 문서 명령 꼴, 머리 줄 7, 활동 줄(말 1 · 검색 2 · 열람 3), `완료 (시도` 정확히 1, Traceback 0, 출력 파일 첫 줄이 진행 줄에 0 번

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: 21/21 (N/A 4 포함 조건 수 기준) → 임계 0.60 이상
- Verdict 영향: 통상

## Discrimination · Check Artifacts (검사 산출물 = check.py, 임시 사본으로 직접 돌림)
- 사본 위치: scratchpad/mut (래퍼 5 종 변이 + WRAPPER 경로만 바꾼 check 사본)
- ⑤ 효과 증명: 변이 → 결과. 기록 끝 처리(flush) 제거 → `flush` FAIL 7. 6줄 상한 제거 → `burst` FAIL 2. 반 줄 처리(마지막 줄바꿈까지만 읽기) 제거 → `partial` FAIL 1. 최종 답 거르기 제거 → `answer` FAIL 2. 주소만 보이기 제거 → `forms` FAIL 3. 다섯 변이 전부 종료 코드 1로 잡힘
- 고치기 전 판(`--base`) 13 개 측정: `answer` 만 0, 나머지 12 개 1 — 계약에 적힌 값과 같음 (측정이 살아 있음)
- ① 첫 칸만 읽기 / ③ 못 읽는 칸: 해당 없음 (여러 칸을 읽는 검사가 아니라 개별 시나리오 검사). 단 corrupt 시나리오가 깨진 줄 6 종 뒤 이어지는 줄을 읽는지 확인(PASS)
- ② 실행 목록: 해당 없음 (레포 러너 수집 대상이 아님. 조건마다 측정 명령이 직접 실행함)
- ④ zsh/bash: 해당 없음 (고정 해석기 — 래퍼는 bash, check.py 는 python3). 단 이 평가 중 zsh 에서 `set -- $p` 가 낱말을 안 쪼개 내 변이 시험 첫 시도가 rc=2 로 실패한 일이 있어 bash 스크립트로 다시 돌렸다

## Evidence Validity
- 0 이 기대값인 측정(Traceback 0 · QQZ 0 · turn0search0 0): 같은 시나리오에서 관련 양성 항목(검색어 · 완료 줄)이 PASS 하고 `--base` 와 변이 사본에서는 FAIL 이라 측정이 죽지 않음
- 진짜 Codex 실행 증거: 부모가 Monitor 에서 옮긴 것. 내가 직접 수집한 것은 아니지만 실제 세션 기록(~/.codex/sessions rollout-…ed46)의 시각으로 교차 확인 — 말 08:50:30, 검색 08:50:31, 열람 08:50:43 · 08:50:49, 최종 답 08:50:56 이 증거의 순서 · 내용과 일치. 활동이 맨 끝에 몰려 나온 것은 Codex 가 첫 2분 넘게 활동 없이 생각했기 때문이라 래퍼 결함이 아님

## 계약 밖 변경 판단 (부모 요청)
- `sleep 3` → `sleep 1`, 진행 줄 앞에서 차례 식별자 · 기록 경로 먼저 찾기: 래퍼 diff 에서 확인. 이유가 타당하고 모든 측정이 새 판으로 통과. 반복 간격은 경과 시간 기준 판정이라 의미 변화가 없고 CPU 비용은 date 호출 정도. 문제 없음으로 판단 (조건 위반 아님)

## Summary
- Total: 17/17 판정 대상 조건 PASS, N/A 4
- Verdict: APPROVE

## Improvement Suggestions
- [진단-04] 증거-경로-부재 — 증거 속 머리 줄은 옛 표기(`N분`)이고 증거는 지금 래퍼 판이 아니다. 계약 문구상 통과지만, 현재 판으로 진짜 실행을 한 번 더 하면 가장 확실하다 (사용자 판단)
- [전체] 범위-미명시 — 래퍼가 `<출력파일>.activity` 상태 파일을 남긴다(실제 실행 폴더에 `out.md.activity` 144 바이트 잔존 확인). 지우는 코드가 없다. 해롭지는 않으나 정리 코드를 넣거나 계약에 허용 사항으로 적는 것이 좋다
