# Sprint Feedback
Feature: Codex 진행 상황 VS Code 상태 표시줄 (세션마다 · 도는 동안만)
Evaluated: 2026-10-09 11:49
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: .harness/sprint-contract-codex-status-bar.md
- sha256: 325ed9d98b6eb4221fb59761752043af12977a1fb030de1a928cc8c7986235ab (status done 반영 뒤)
- slug: codex-status-bar
- seal_status: SEAL_OK · measure_status: MEASURE_OK (bash · zsh)
- 봉인 커밋 대조: seal_commit=92c262d3(계약 파일 1개), 차이 0
- status_transition: active -> done

## Amendments
- amendments: 1 (AM-01 relaxing · 스크립트-03 (f) · (j) 실패 문구의 % 서식 오류, consent anchored 2026-10-09T02:38:21.988Z)

## Deletions
- deletions_range: d72bd22c..6310b0e7, 삭제 0

## Results

판정 방식: Codex 를 부르지 않았다(감독 mode: off). 감독은 가짜 codex, 리서치 실행기는 가짜 codex 를 PATH 앞에, 확장은 가짜 vscode 모듈로 쟀다.

| 조건 | 판정 | 측정 |
|---|---|---|
| 스크립트-01 | PASS | 도는 동안 상태 파일 1 개 · 끝 · SIGTERM · 막힘 뒤 0 개 · usage.json 12/3 · --detach pid 일치 |
| 스크립트-02 | PASS | 리서치 도는 동안 1 개 · 끝 뒤 0 개 · usage.json 12/3(미끼 50/40 아님) · SIGTERM 뒤 0 개 · 가짜 codex 꺼짐 |
| 스크립트-03 | PASS | (a)~(k) 글자 · 폴더 · 죽은 pid · 오래 멈춤 · 풀린 창 · 기본 살아 있음 판단 |
| 스크립트-04 | PASS | 상태 폴더 없이 시작 · 반쯤 쓴 파일 · 작업마다 항목 · 죽은 pid · 폴더 밖 · 지우면 사라짐 · 쌓이지 않음 · 끈 뒤 새 항목 없음. (h) 정리 확인은 대체 측정(작업이 살아 있는 채 끄기)으로 PASS |
| 스크립트-05 | PASS | package.json 칸 · vsce 4.0.0 묶음 내용 |
| 스크립트-06 | PASS | 앞 묶음 usage-cap 01~04 |
| 스킬-01 · 구조-01 · 재사용-01 | PASS | README 문단 낱말, 바뀐 경로 8 개, extension.js 판단 없음 |
| 금지-03 · 금지-04 | PASS | validate-plugin 종료 0 |
| 재사용-02 · 진단-01 · 진단-03 | N/A | 계약 사유 |
| 진단-02 · 진단-04 | PASS | 더한 줄 경고 0(양성 대조 36 · 28) · 측정 전체 · 로컬 CI 34 개 실패 0 |

음성 대조: 스크립트-01 · 02 · 03 --base 종료 1.
변이 시험: --detach 부모만 씀 → 01(e), 가장 최근 세션 기록 → 02(b), 항목 하나로 합침 → 03(e) · 04(c), updated 안 봄 → 03(i), trap rm 빼기 → 02(b) 모두 FAIL 로 잡힘. 끌 때 정리 안 함 → 봉인 측정 통과(죽은 측정), 대체 측정으로 잡힘.

## 개선 제안 (판정 영향 없음)
1. [스크립트-04] 측정-방식-불일치 — 끄기 직전 작업 파일 하나를 살려 두고 all_disposed 를 재야 한다(지금은 끄기 전에 다 지워 (h) 가 늘 참).
2. [스크립트-01 · 02] 측정-판별력-미기재 — updated 주기 갱신(30 초 · 3 초)은 값을 재지 않는다. 코드 검토로 확인.
3. 실사용 — 리서치는 $PWD 를 그대로 써서 바로가기(심볼릭 링크) 폴더에서 부르면 확장의 실제 경로 작업 폴더와 안 맞을 수 있다(pwd -P 로 고칠 거리).

## Cross-Diagnosis
- 상태: done (부모가 새 에이전트로 실행)
- 1. 뜻과 다르게 읽힌 조건: 판정을 뒤집는 것은 없음. 중간 — 01 · 02 의 folder 비교가 양쪽을 실제 경로로 바꿔 확장보다 너그럽다. 리서치를 바로가기 폴더에서 부르면 jobsToItems 가 0 개(직접 재현). 중간 — 30 초 갱신 스레드를 지워도 모든 조건이 통과(측정 밖)
- 2. 0 건 통과: 04 (h) all_disposed 는 죽은 검사(끄기 전에 다 지움 · 구독 해제와 deactivate 를 둘 다 불러 서로 메움). 낮음 — 01 (d) 는 남지 않음만 잰다
- 3. 계약 밖: 중간 — write_json 실패 시 감독이 통째로 멈춤(리서치는 || true). 중간 — usage.json 하나라 다른 계정 값이 붙을 수 있음. 낮음 — 항목 ID 가 실행마다 새로 생겨 숨김 목록이 쌓임 · 순서 겹침 · 감시자 오류 처리 · 신호 사이 임시 파일 · 정상 종료 trap 의 kill_tree pid 재사용
- 후속 스프린트 후보: 리서치 pwd -P, 상태 쓰기 실패를 감독에서 삼키기, 갱신 주기 측정, 04 (h) 측정 고치기, 감시자 오류 처리
