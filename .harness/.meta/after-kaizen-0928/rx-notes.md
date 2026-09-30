# 묶음 rx 기록 — 조건 번호 정규식을 리눅스에서도 돌게

계약 `.harness/sprint-contract-after-0930-id-regex-linux.md` (19 조건, 봉인 커밋 `f6b55082`, 지문 `sha256:64997021d92aa203`,
측정 지문 `sha256:4dc48dd81154a963`, 봉인 2026-09-30 16:44). 가지 `chore/ak3-rx`, 시작 판 `bbcb43d8`.
QA 판정 APPROVE 19/19 (Iteration 1, 커밋 `99edfe9b` 에 리포트와 계약 status done). 독립 검토 BLOCKING 0, 확인된 결함 없음.

## 항목별 결과

### (1) 조건 번호 식 바꿈 — 처리함

- 커밋 `7ea4c2c0` (harness): 규약 `harness/references/contract-schema.md` 7 곳 · 스킬 `harness/skills/sprint-contract/SKILL.md` 6 곳 ·
  평가자 `harness/agents/qa-evaluator.md` 2 곳 · 평가 가이드 `harness/docs/guides/qa-evaluation-guide.md` 1 곳에서
  한국어 몫 `[가-힣]+` 를 `[^ -~]+`(출력 가능한 ASCII 밖 글자)로 바꿨다. awk 모양도 같다.
  `harness/scripts/measure-common.sh` 는 규약 블록을 읽어 쓰므로 고칠 글자가 없었다.
- 커밋 `174890a2` (docs/harness): 문서 쪽 `contract-schema.html` 8 곳 · `qa-evaluation-guide.html` 1 곳을 원본과 맞췄다.

### (2) 까닭 한 줄 — 처리함

- 규약 문서 「조건 열거 정규식은」 줄 두 줄 아래, 문서 쪽은 바로 다음 `<li>` 로 「한글 범위식은 로캘마다 뜻이 달라 쓰지 않는다」 를 적었다.

### (3) 시험 경우 K3 — 처리함

- `harness/evals/measure/measure-helpers-test.sh` 에 `K3-C.UTF-8한국어번호` 를 더했다. `LC_ALL=C.UTF-8` 로 두 지문과 조건 수 7 을 재고,
  규약의 두 식에 ASCII 밖 글자가 든 줄이 0 인지 본다. 맥 grep 은 한글 범위식을 받아 주므로 마지막 검사가 맥에서도 옛 식을 잡는다.
  CI 단계는 이미 있어 `.github/workflows/ci.yml` 은 고치지 않았다.

## 자기 측정 (2026-09-30, 가지 끝 `174890a2`)

| 조건 | 값 | 판정 |
|---|---|---|
| 스킬-01 | 네 파일 `hangul_range=0`, `new_piece` 7 · 6 · 2 · 1, `counts_ok=1` | 성립 |
| 스킬-02 | `reason_lines=1 after_rule_line=+2` | 성립 |
| 스크립트-01 | `mac_rc=0 k3_pass=1 last=[실패 0 건] neg_rc=1 neg_fails=[K3-C.UTF-8한국어번호] ci_step=1` | 성립 |
| 스크립트-02 | `linux_rc=0 linux_fails=[] k3_pass=1 neg_rc=1` 실패 여섯(K1 둘 · K2 · K3 · M 둘) | 성립 |
| 스크립트-03 | `contracts=149 rows=149 0 0 0 294` | 성립 |
| 오류-01 | `mac=4,4,4,4,4,4 linux=4,4,4,4` | 성립 |
| 구조-01 | `counts_ok=1 reason_lines=1 reason_li=1 after_rule_line=+1 cases=6 overflow=0 css_rc=0` | 성립 |
| 구조-02 | 여섯 파일 그대로, `changed_kept=0` | 성립 |
| 구조-03 | `commits=3 merges=0 bad=0` (이 기록 커밋 뒤 4 개가 된다) | 성립 |
| 금지-02 · 03 · 04 | `forced-update` 0 · code-fence 종료 코드 0 · frontmatter 종료 코드 0 | 성립 |
| 재사용-01 · 02 | K3 는 CI 에 등록된 기존 시험 안 · 새 파일 `A` 0 줄 | 성립 |
| 진단-01 · 03 · 04 | N/A 측정 모두 0 | 성립 |
| 진단-02 | `md_warnings=0 shellcheck=0 bash_n_rc=0` | 성립 |
| 진단-05 | `local_rc0=25 local_lines=26 skip=1 a11y=[206/206 PASS] ci_only_failed=[]` | 성립 |

진단-05 는 교차 진단이 다시 재지 못했던 조건이라 실제 가지에서 돌렸다. W 에는 본 레포 `node_modules` 를 가리키는 바로가기를 두었다(추적 안 됨).

## 킷 버전 판단

harness 는 0.16.0 그대로 둔다. 버전 올리기는 계약 범위 밖이고, 묶음을 합친 뒤 릴리스 단계에서 한꺼번에 정한다.
바뀐 것은 식의 모양뿐이고 뜻(한국어 번호도 센다)은 같아 patch 급이다.

## 남은 것

- 교차 진단이 아직이다 — QA 가 `cross_diagnosis_by: pending-parent` 로 저장했다. 부모 세션이 리포트 「Cross-Diagnosis Handoff」 절의 두 질문
  (계약 해석 오판 여부, 스크립트-03 · 오류-01 에서 규칙 10 다섯 가지가 빠짐없이 됐는지)을 물은 뒤
  `~/.harness/feedback/evaluator/1a3bcba6-2026-09-30T171308-bda55d45-13141.yaml` 의 값을 갱신해야 한다. 이 묶음 작업 폴더 밖이라 여기서 하지 않았다.
- 독립 검토의 결함 아닌 관찰: 새 식 `[^ -~]+` 는 한글 말고도 ASCII 밖 글자를 모두 받는다. 계약 파일 4057 개에서 옛 식 · 새 식 조건 수 차이 0,
  한글 아닌 ASCII 밖 글자로 된 번호 줄 0 이라 지금 영향은 없다. 나중에 한자 · 기호로 시작하는 줄이 조건 번호로 세질 수 있으니 번호 규칙을 넓힐 때 다시 본다.
- 조건 줄을 읽는 스크립트 가운데 옛 식을 쓰는 것은 `.harness/.meta/` 안 지난 묶음 측정용뿐이다(독립 검토 확인). 지난 기록이라 고치지 않는다.
- W 의 `node_modules` 바로가기(본 레포 것을 가리킴)는 `.gitignore` 의 `node_modules/` 가 바로가기를 못 걸러 추적 안 된 파일로 보였다. 마무리 때 바로가기만 지웠다.
- 그 바로가기가 가리키는 본 레포 `node_modules` 에는 `mermaid` 가 없어, W 에서 `check-docs-mermaid.js` 는 rc=2, 그 시험은 1/9 로 떨어졌다.
  가지 탓이 아니다 — scratch 사본에서 `npm ci` 로 새로 깔고 돌리면 rc=0 (쪽 3 · 예시 9 · 안 그려진 예시 0), 시험 9/9.
  본 레포 쪽 `npm ci` 가 옛 판이라 생긴 일이다. 다음 묶음이 같은 바로가기를 쓰면 같은 오판이 나니, 본 레포에서 `npm ci` 를 다시 돌리거나 사본에서 잰다.
- 합치기 · push · 릴리스 — 계약 범위 밖.
- `ci-local.sh` 가 레포 밖이라 버전 관리가 안 된다 — 남은 일 목록 D2 와 같은 자리이고 이 묶음이 만든 문제가 아니다.
- `.harness/` 안 봉인된 계약 · 앞 묶음 도우미의 한국어 글자 세기 식은 봉인 때문에 손대지 않았다. 조건 번호 식이 아니라 리눅스 봉인 확인에는 영향이 없다(스크립트-03 에서 149 계약 지문이 리눅스에서도 같다).
