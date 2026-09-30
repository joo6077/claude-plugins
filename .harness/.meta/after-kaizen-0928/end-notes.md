# 묶음 end 기록 — 깨진 바로가기 · 머리말 시험 · 평가 실행기 · 평가자 머리 읽기

계약 `.harness/sprint-contract-after-0930-end.md` (22 조건, 봉인 커밋 `6e87f54a`, 지문 `sha256:d2437ae0709e3d1a`,
측정 지문 `sha256:1775115ab58ed74e`). 가지 `chore/ak3-end`, 시작 판 `f0fcc534`. 측정 도우미 커밋 `1ff8164a`.
QA 판정은 아직이다(이 기록은 구현자 몫까지만 적는다).

## 항목별 결과

### (1) 깨진 바로가기 — 처리함

- `scripts/check-install-docs-guidance.py` (커밋 `cf0be233`): 파일을 열다 `FileNotFoundError` 가 나면
  `os.path.lexists` 로 경로 자체가 남았는지 본다. 바로가기가 남아 있고 가리키는 대상만 없으면
  `UNREADABLE <경로> (바로가기 대상 없음)` 으로 세어 종료 코드 2, 경로가 정말 없을 때만 전처럼 `SKIP`.
  맨 앞 설명에도 바로가기 경우를 적었다.
- `scripts/test-check-install-docs-guidance.py` (같은 커밋): 경우 4(대상 없는 바로가기 → 2)를 더해 네 경우.
  시작 판 검사를 넣으면 경우 4 만, `8dca3e73^` 판을 넣으면 경우 3 만 실패한다.

### (2) 머리말 시험 — 처리함

- `scripts/test-check-docs-mermaid.js` (커밋 `868708cf`): 이름표 없는 `<pre>` 에 머리말 + 정상 `flowchart LR`
  만 있는 경우 9 를 더해 아홉 경우. 검사의 머리말 건너뛰기 두 줄을 옛 모양으로 되돌린 사본은 경우 9 만 실패한다.
  검사 파일 `scripts/check-docs-mermaid.js` 는 고치지 않았다.
- `.github/workflows/ci.yml` (커밋 `09587206`): 시험 단계 이름을 「아홉 경우」 로.

### (3) 평가 실행기 — 처리함

- `scripts/run-evals.py` (커밋 `29466123`): 인자로 준 킷이 없거나 `evals/evals.json` 이 없으면
  `ERROR: 이름으로 준 킷 <킷> — <까닭>` 과 종료 코드 2. `SKIP_KITS` 에 적힌 킷은 전처럼 SKIP.
  `evals.json` 읽기의 `OSError`(권한 등)는 `UNREADABLE <경로> (<까닭>)` 과 종료 코드 2 로 끝낸다.
  목록에서 도는 킷은 이미 평가 파일이 있는 것만 고르므로 옛 「디렉토리 없음」 SKIP 줄은 뺐다.
- `scripts/sync-evals.py` (같은 커밋): `OSError` 를 같은 줄 모양과 종료 코드 2 로.
- `scripts/test-run-evals.py` · `scripts/test-sync-evals.py` (같은 커밋): 경우 4 · 5 · 6 과 경우 3 을 더했다.
  root 로 돌면 권한을 빼도 읽히므로 그때는 준비 실패 2 로 멈춘다. 시작 판 도구를 넣으면 새 경우만 실패한다.
- `.github/workflows/ci.yml` (커밋 `09587206`): 두 시험 단계 이름에 「없는 킷 이름 · 못 읽는 파일」 과 「못 읽는」 을 더했다.
- 킷 이름을 주고 부르는 소비처 셋(`tone-kit` · `backend-kit` · `infra-kit`)과 인자 없는 실행은 그대로 종료 코드 0.

### (4) 평가자 머리 읽기 — 이미 됨

- 레포 안 머리 읽개 사본 다섯(`harness/agents/qa-evaluator.md` · `harness/references/contract-schema.md` 의 `fm_get`,
  `docs/harness/contract-schema.html`, `harness/skills/sprint-contract/SKILL.md` 의 `read_fm`,
  `harness/scripts/commit-guard.sh` 의 `val()`)은 커밋 `e2ff8652` 에서 줄 끝 주석을 벗기게 됐다.
  이번에 고친 파일은 없고, 오류-01 이 다섯 사본이 `active|abc|x-y|a#b` 를 읽는 것을 잰다.
- 옛 모양은 설치본 캐시 harness 0.16.0 에만 남아 있다. 봉인 전 교차 진단 에이전트가 받은 지침이 바로 그 옛 모양이었다.

### 교차 진단 지적 반영

- 남은 일 목록의 B2 · B3 · B9 가 빠졌다는 지적은, 목록이 `main 01b1cac` 기준이고 시작 판이 그보다 앞선 가지 끝이라
  생긴 것이다. B2 · B3 는 `e2ff8652`, B9 는 `dd607550` 에서 이미 처리됐다. 계약 배경에 한 줄로 적고 조건은 바꾸지 않았다.

## tone-guide 결과

- 1 단계: 오버레이 `.claude/tone-project.md` (어댑터 없음 · 주석 한국어)와 레포 `tone-kit/references/` 의
  코어 네 파일 · `locale-korean.md` 규칙 ID 를 읽었다. 걸리는 규칙은 C-01 · C-07 · C-15 · N-08 · S-04 · S-07 · K-02 · K-04 · F.
- 5 단계: 추가된 111 줄에 번역투 여섯 패턴(G-1) 0 건, `합니다` 체 0 건(`아니다` 두 줄은 잘못 걸린 것), 구분선(F) 0 건,
  한 글자 이름(N-08) 0 건. 새 주석은 왜 2 로 끝내는지만 적는다(C-01). 넘기기만 하는 감싸개 없음(S-04). 위반 없음.

## 자기 측정 (W, 커밋 뒤)

- 스크립트-01 ~ 06 · 오류-01 ~ 03 · 구조-01 · 02 모두 종료 코드 0. 구조-03 은 이 기록 커밋 뒤에 잰다.
- CI 파일에만 있는 명령 스물하나 모두 종료 코드 0 (`경우 4 개 중 통과 4` · `경우 6 개 중 통과 6` ·
  `경우 3 개 중 통과 3` · `경우 9 개 중 통과 9` · `174 passed` · `TOTAL files=94 ok=73 need=0 exempt=21 unreadable=0`).
- 로컬 CI(`ci-local.sh`) 25 단계 `rc=0`, `feedback-agg-test SKIP (yq 없음)`, `docs-a11y` `206/206 PASS`.
  계약 목록 밖 CI 단계 `bash bambu-kit/evals/run-gate-fixtures-test.sh` · `bash scripts/test-check-docs-a11y.sh` 도 종료 코드 0.

## 킷 버전 판단

- 바뀐 파일이 모두 레포 맨 위 `scripts/` 와 `.github/` 라 어느 킷의 설치본에도 들어가지 않는다 — 킷 버전은 올리지 않는다.
- (4) 의 설치본 옛 사본은 다음 harness 릴리스(0.16.0 다음)로 풀린다. 레포 쪽 변경은 이미 `e2ff8652` 에 있다.

## 남긴 것

- QA 판정과 계약 `status: done` — 구현자 몫이 아니다.
- harness 릴리스 — 설치본 0.16.0 의 옛 머리 읽개를 바꾸려면 필요하다. 이 계약은 릴리스를 하지 않는다(범위 밖).
- `SKIP_KITS` 에 적힌 `howto-kit` 을 이름으로 줄 때의 SKIP · 0 — 사유가 적힌 뺀 킷이라 그대로 둔다.
- `evals.json` 의 UTF-8 이 아닌 바이트 · `marketplace.json` 읽기 실패 — 이미 추적 출력과 종료 코드 1 로 CI 를 멈춘다.
  조용한 통과가 아니라 이번에 손대지 않았다.
- `backend-kit/README.md` · `infra-kit/README.md` 의 「2 = 파싱 오류」 글 — 그 킷 이름으로는 새 2 까닭이 생기지 않아 두었다.
- 로컬 CI 도구 `ci-local.sh` 는 레포 밖이라 고치지 않았다.
