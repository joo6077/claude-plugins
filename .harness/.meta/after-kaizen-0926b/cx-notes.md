# cx 묶음 기록 — Codex 지적 · 묶음 기록 「남은 것」 코드 고침

작업 폴더 `ak2-cx`, 가지 `chore/ak2-cx`, 시작점 `82ec540`. 계약 `.harness/sprint-contract-after-0926-codex-and-leftover-fixes.md`
(조건 29 · 기능 조건 21). 이 파일은 계약 작성 단계(Step 0 ~ 6.5)에서 만들었다 — 구현 · QA 뒤 커밋 목록과 tone-guide 5 단계
대조 결과를 이어 적는다.

## 항목별 처리

읽은 입력: Codex 1 차 점검 `codex-review-1.md` 의 결함 둘, 열두 notes(cs-notes · dca-notes · dcb-notes · gd-notes · hs-notes ·
k1-notes · k2-notes · pd-notes · pd2-notes · us-notes · vsa-notes · vsb-notes)의 「남은 것」 절, cs 「명시적 미완」 · k1 「넘긴 것」 ·
gd 「뒤따를 일」 · dcb 「다른 묶음과 부딪히는 곳」. 「처리됨」 은 시작점 `82ec540` 에서 근거를 다시 확인했다.

| 항목 | 처리 | 근거 · 조건 |
| --- | --- | --- |
| Codex 1 외부 CSS 판정 (codex-review-1 · vsa) | 계약에 넣음 | SC-01. `<LINK` · `<SCRIPT` 대문자도 같이 |
| Codex 2 preflight 판정 표 사본 (codex-review-1 · k1 UD-3) | 계약에 넣음 | SK-01 · SC-02 · SC-03 · ER-01 |
| flutter-audit 사본을 CI 가 안 지킴 (k1 KF-2) | 계약에 넣음 | SC-04 — 목록에 넣으면 지금 사본이 원문과 달라(둘째 「3.」) 사본도 고친다 |
| `dirty_except_status` 가 본문 `status:` 까지 뺌 (cs) | 계약에 넣음 | SC-05 |
| 판 번호 자리 여덟 (cs) | 계약에 넣음 — 다섯 | SK-03: qa 가이드 `:12` · `:1984` · `:2063`, 설계 가이드 `:1311`, `docs/index.html:239`. `:15` · `:22` · `:2054` 셋은 2026-09-24 갱신 기록이라 그날 값 v5.5 를 그대로 둔다 |
| 판 번호 문서 사이트 쪽 여섯 (cs) | 이 묶음 밖 | `docs/harness/*.html` 페이지 다시 만들기 — 부모가 다음 차례에 한다 |
| 조건 패턴 표 v5.5 다섯 종 (cs 명시적 미완) | 계약에 넣음 | SK-02 |
| 평가 가이드 「①~④ 의 짝은 다음 사이클로」 (cs · gd CS-3) | 계약에 넣음 | SK-03 `cs3` |
| harness README 추적 규칙 `kaizen:` (gd) | 계약에 넣음 | SK-04 |
| 옛 단계 이름 Step 11 · 11.5 두 곳 (vsb) | 계약에 넣음 | SK-04. `scripts/append-audit-log.py:44` 의 「Step 11.5 added」 는 지난 감사 기록 값이라 둔다 |
| 설치본 `docs/` 경로 raw 안내 — backend · rust · infra-guide (k2) | 계약에 넣음 | SK-05. 같은 뿌리가 다른 킷에도 있다(아래 줄) |
| 같은 raw 안내가 api · design · flutter · howto · onboarding · planning · react · reflect 에도 없음 (이번에 찾음) | 이 묶음 밖 | 파일 69 개이고 그 가운데 사용자 프로젝트의 `docs/` 를 뜻하는 경로가 섞여 있어 하나씩 가려야 한다. k2 notes 가 짚은 범위만 고친다 — notes 에 넘김 |
| OpenAPI 최소 지원선 문구 (k2 독립 검토 1) | 계약에 넣음 | SK-06. `docs/backend/research-log.md` 는 날짜 기록이라 두고, 문서 페이지는 부모 몫 |
| design-mockup Step 0 이 대상 전에 관례 표 (k2 독립 검토 2) | 계약에 넣음 | SK-07 — 관례 표 줄만 Step 1 뒤로 미룬다 |
| bambu references 4종 (vsb) · 루트 README 나무 그림 (vsb) | 계약에 넣음 | SK-08. `.claude/skills/bambu-research/SKILL.md:5` · `bambu-kit/README.md:39` 의 「4종」 은 research 가 고치는 대상 넷(`.claude/skills/bambu-research/SKILL.md:33-36` 표)이라 맞는 말 — 그대로 둔다 |
| AP-04 정규식이 닫는 `---` 에 걸림 (us) | 계약에 넣음 | SC-07 |
| 피드백 `project_hash` 재계산 경고 (k2) | 계약에 넣음 | SC-06 · SK-09 — 스크립트가 아니라 설명과 조각이 뒤처졌다 |
| 검사기 단추 id `theme-btn` 만 봄 (dca) | 이 묶음 밖 | 고치면 `docs/design-kit/visual-styles.html` 단추가 63x33 이라 CI 가 빨개진다(흉내 판 실측, `color-palette` 87x48 · `korean-technical-writing` 80x44 는 통과). 페이지 손질이 같이 있어야 해 문서 페이지 차례로 넘긴다 |
| `check-stale-values` 가 오케스트레이터 참고 폴더를 안 봄 (dcb) | 처리됨 | `scripts/check-stale-values.py:56` 에 `.claude/skills/kaizen-orchestrator/references` 가 있다(vsa VS-27) |
| 매핑 표 `process (공유)` 행 부딪힘 (dcb) | 처리됨 | `.claude/skills/docs-site/SKILL.md:68` 에 원본 둘, `detect-docs-drift.py --check-table` 어긋남 0 |
| docs-site 스킬 「line-height 1.2~1.6배」 (k2) · KD-2 · VS-18 (dca) | 처리됨 | `.claude/skills/docs-site/SKILL.md:110` 이 「행간 1.7 은 공통 파일」, `design-audit/references/audit-criteria.md:10` 이 문자 체계별 범위, 오케스트레이터에 `standalone` 0 줄 |
| KD-3 다섯 자리가 화면 규약 숫자 재정의 (gd · k2) | 처리됨 | design-kit 에 `2 개 이상` · `3 회` 0 줄, `§8.9` 인용 다섯 파일 |
| reflect-digest 드리프트 [NEW] (vsa) | 처리됨 | 페이지 `docs/reflect-kit/reflect-digest.html` 이 생겨 이제 다시 맞출 쪽으로 나온다 — 다시 만들기는 부모 몫 |
| DG-05 가 평가자 `status:` 편집으로 깨짐 (pd · dca DG-05) | 처리됨 | 규칙과 도우미 `dirty_except_status` 가 v5.7 에 들어갔다(`contract-schema.md:678-692`). 도우미 결함은 SC-05 가 고친다 |
| design-mockup Step 2 가 폐기 칸 경로를 따라 읽기 (pd) | 처리됨 | pd2 가 넣었다(`design-mockup/SKILL.md:57`) |
| AR-02 `exact` · `old_left` 칸 나누기 제안 (dca QA 3 회차) | 이 묶음 밖 | 한 계약의 도우미 짜임 제안이라 규칙 문장이 아니다 — 다음 계약을 쓸 때의 관례. contract-kaizen 몫 |
| 원래 있던 편집기 경고 (cs · VS-26) | 이 묶음 밖 | 기존 마크다운 경고 정리는 부모가 다음 차례에 한다 |
| 문서 사이트 페이지 다시 만들기 (cs · gd · hs · k1 · pd · pd2 · vsa · vsb · dcb 의 KT-1 · KRf-1) | 이 묶음 밖 | 부모가 다음 차례에 한다. 이 계약이 원본을 고친 쪽(가이드 둘 · design-mockup · api-design · 스키마)도 그때 다시 맞춘다 |
| SK-11 · SK-13 머리 모양 되돌릴지 (k1) · KD-4 design:P2 (k2) · 폐기 칸 이름 남길지 (pd · pd2) · 핸드오프 틀 모델 이름 (us) | 이 묶음 밖 | 사용자 판단 몫으로 남은 항목 |
| `docs/flutter/research-log.md:20` 2.16 문장 (k1 KF-4) | 이 묶음 밖 | 2026-09-24 조사 기록이라 그날 문장을 둔다. 규칙 본문은 이미 2.7.0 기준(`flutter-build/SKILL.md:20`) |
| `spawn-kaizen-phase.sh:71` 최댓값 17 (vsa) | 이 묶음 밖 | 아래 `case` 표가 Phase 마다 손으로 적혀 있어 상한만 뽑아도 새 킷 Phase 는 `case` 에 없다. 표 전체를 바꾸는 개편이라 최소 변경 밖 |
| `run-evals.py` `ALL_KITS` · `sync-evals.py` `TARGET_KITS` 손 목록 (vsa) | 이 묶음 밖 | 「evals 가 있는 킷」 목록이라 마켓 목록과 뜻이 다르다. 결함이 아니라 설계 개편 |
| 두 번째 검색 줄 머리 조건 넓히기 (pd2) · 다른 폐기 표기 (pd) | 이 묶음 밖 | 넓히면 규칙 인용 줄을 폐기 결정으로 잘못 잡는 쪽이 커진다(pd2 ER-01 과 같은 모양) — 판단이 먼저다 |
| DG-05 를 추적 안 된 도구 없이 재기 (pd · pd2) | 이 묶음 밖 | `ci-local.sh` 를 레포에 들일지는 도구 관리 결정이다 |
| 병렬 세션 훅 · `bash -c` 커밋 · `us-test.sh` 커밋 뒤 경우 (us) | 이 묶음 밖 | 레포 밖 `~/.claude` 훅 |
| 킷 판 올림 · 릴리스 (cs · gd · hs · pd2 · vsa) | 이 묶음 밖 | 릴리스 단계 몫 |
| hs 1 · 2 · 4 · 5, k2 근거 파일 위치, cs AR-06 · dca A-01 · vsa A-01 개정 동의 | 처리됨 | 각 notes 가 「남은 일 없음」 또는 정보로 적었다 |

## 이 묶음 밖으로 넘긴 것

- 문서 사이트 페이지 다시 만들기 · 원래 있던 마크다운 경고 정리 — 부모가 다음 차례에 한다
- 검사기 단추 id(`theme-btn` 만 봄) — 고치면 `docs/design-kit/visual-styles.html` 단추가 63x33 이라 문서 접근성 검사가 빨개진다.
  페이지 손질과 같이 문서 페이지 차례에 한다
- 설치본 `docs/` raw 안내가 없는 다른 킷 파일 69 개 — 사용자 프로젝트의 `docs/` 를 뜻하는 경로가 섞여 하나씩 가려야 한다
- 사용자 판단 몫: k1 SK-11 · SK-13 머리 모양, k2 KD-4, pd · pd2 폐기 칸 이름, us 핸드오프 틀 모델 이름

## 판단 기록

- `scripts/check-api-kit-docs.py` 를 CI 에 넣을지 — 이번에는 넣지 않는다. 끝 판에서 `12/12 PASS` 라 넣어도 지금은 초록이지만,
  api-kit 문서 페이지 다시 만들기가 부모 다음 차례로 남아 있어 그 작업과 함께 넣는 편이 덜 흔들린다. 계약 SC-01 도 등록을
  요구하지 않는다(산출물이 검사인 조건 ②). 다음 문서 페이지 차례에 `.github/workflows/ci.yml` 첫 작업에 한 단계로 넣기를 권한다
- DG-05 가 기대는 `ci-local.sh` 는 레포 밖(추적 안 됨) 도구다(교차 진단 2). QA 가 끝날 때까지 그 자리
  `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` 에 두고 지문 `59fe55125c0dbc77` 을
  바꾸지 않는다. 관리 책임은 부모 세션에 있다
- SK-07 은 관례 표 줄 하나만 제자리에서 고쳤다(교차 진단 3, `numstat=1/1`)
- SC-01 사례는 교차 진단 4 를 받아 `url(` 쪽 둘을 더해 18 사례로 봉인했다

## 커밋 목록

시작점 `82ec540` 뒤, 가지 `chore/ak2-cx`.

| 커밋 | 내용 |
| --- | --- |
| `28d063d` | 계약 봉인(파일 하나 · 조건 29 · `conditions_digest` `b825332e3932b0f2` · `measurement_digest` `fc30d758abb4a9a8`) |
| `7122605` | `scripts/` — 외부 리소스 판정 · 새 판정 표 사본 검사 · flutter-audit 사본 대조 · 공통 함수 두 개를 `plugin_utils.py` 로 · 단계 이름 |
| `45079b8` | `.github/` — CI 첫 작업에 판정 표 사본 검사 단계 |
| `f3083ed` | `harness/` — 원문 쪽 사본 안내 · 조건 패턴 8 종 · 워크트리 해시 조각 · `dirty_except_status` · 판 번호 v5.7 · 한계 문단 · README 추적 규칙 · 종료 코드 표 |
| `64d794c` | `flutter-toolkit/` — preflight 판정 표 사본 · flutter-audit 사본 번호 |
| `e6e7b27` | `react-kit/` — preflight 판정 표 사본 |
| `52d905c` | `backend-kit/` — raw 안내 다섯 파일 · OpenAPI 최소 지원선 |
| `10cc34e` | `rust-kit/` — raw 안내 세 파일 |
| `1ea26b2` | `infra-kit/` — infra-guide raw 안내 |
| `5018f7d` | `design-kit/` — design-mockup 관례 표 순서 |
| `e7f3caf` | `bambu-kit/` — README references 9종 · 표 두 행 |
| `2dbdf3f` | `docs/` — api-design OpenAPI 문구 · 목차 스키마 v5.7 |
| `a6af428` | `.claude/` — meta-kaizen 단계 이름 F1 ~ F4 |
| `ad55f4e` | 뿌리 `CLAUDE.md` · `README.md` — bambu 9종 · 나무 그림 네 킷 |
| `aec11b4` | `.harness/project.yaml` — AP-04 판정 수단 |
| `589c317` | `harness/` — `dirty_except_status` awk 한 글자 이름 정리(tone-guide 5 단계 대조에서 걸림) |
| (이 커밋) | `.harness/.meta/after-kaizen-0926b/cx-notes.md` — 이 기록 |

## 조건별 자기 측정 (구현자 측정 — 판정 아님)

봉인 판 도우미를 `extract-helpers.py --sealed` 로 떼어 끝점 `aec11b4` 에서 돌렸고, SC-05 · AR-01 · AR-03 · DG-05X 는 `589c317` 에서 다시 쟀다(값 같음).

| 조건 | 측정 출력 |
| --- | --- |
| SK-01 | `flutter=1/8 react=1/8 src_note=11 canon_note=1` |
| SK-02 | `hdr=1 hdr_old=0 rows=8 new=111` |
| SK-03 | `cur=v5.7 ref=1 list=1 link=1 cdg=1 index=1 hist=111 old_cs3=0 cs3=1` |
| SK-04 | `readme_old=0 readme_new=1 meta_old=0 meta_new=1 drift_old=0 drift_new=1` |
| SK-05 | `backend=5/0 rust=3/0 infra=6/0` |
| SK-06 | `sp=11 sp_old=0 ad_old=0 ad=11 src=1` |
| SK-07 | `app=1 step1=1 numstat=1/1` |
| SK-08 | `refs=9 r11=1 r23=1 r39=1 table_same=1 claude=1 claude_old=0 tree_bambu=1 tree_missing=0 research=1` |
| SK-09 | `qa_wt=1 skill_wt=3 old=0` |
| SC-01 | `cases=18 wrong=0 pages=[12/12 PASS] bad_rc=1 bad_fail=1 bad_last=1` |
| SC-02 | `clean=rc0/ok_f=1 ok_r=1 mis_f=0 mis_r=0 \| react_bad=rc1/ok_f=1 ok_r=0 mis_f=0 mis_r=1 \| canon_bad=rc1/ok_f=0 ok_r=0 mis_f=1 mis_r=1` |
| SC-03 | `ci_steps=1 job=[validate:] first_job=[validate:] exitdoc=1` |
| SC-04 | `rc=0 fa_ok=1 sum=[checked=8 violations=0 infra_errors=0 excluded=1] bad_applied=1 bad_rc=1 bad_mis=1 guide_fa=1` |
| SC-05 | bash · zsh 모두 `k1=0 k2=0 k3=2 k4=1 k5=1 k6=1 k7=2 k8=rc2/[] k9=0` |
| SC-06 | `wt=1a3bcba6 wt_same=1 plain_same=1 lines=19` |
| SC-07 | `cmd=1 pattern=0 msg=1 rc=0 bad_rc=2` |
| ER-01 | `unread=rc2/unr_f=1/mis_r=1 canon_gone=rc2/canon_missing=1/ok_lines=0` |
| AR-01 | `scope=33 changed=35 extra=0 missing=0 multi_top=0` (notes 커밋 전) |
| AR-03 | `seal_commit_files=1 seal_before_impl=1 seal_same_as_tip=1 measure_same_as_tip=1 this=SEAL_OK MEASURE_OK` |
| AP-03 · AP-04 | `v6_rc=0 fail=0` · `v1_rc=0 fail=0` |
| RE-01 · RE-02 | `added=[scripts/check-cause-table-copies.py ]` · `normalized=scripts/plugin_utils.py contains=scripts/plugin_utils.py chk_import=1` |
| DG-01 · DG-03 · DG-04 | `release_sh=0` · `release_sh=0` · `entry=0` |
| DG-02 | `md_new=0` (바뀐 `.md` 스물여섯 모두 0), `py_compile` 다섯 파일 종료 코드 0 |
| DG-05 | 도구 지문 `59fe55125c0dbc77` 같음. `ci-local.sh` 요약 `rc=0` 25 줄 · 나머지 한 줄 `feedback-agg-test SKIP (yq 없음)`. `m DG-05X` 가 `0 0 0` |

AR-02 는 이 notes 커밋 뒤에 잰다.

## 검사 결과

- `python3 scripts/validate-plugin.py` — 14 킷 모두 OK, 종료 코드 0
- `python3 scripts/sync-docs.py --check-only` — 모든 README 동기화 상태
- `python3 scripts/sync-evals.py --check-only` — 0 added · 0 orphans · 0 missing
- `python3 scripts/detect-docs-drift.py --check-table` — 어긋남 0
- `python3 scripts/detect-docs-drift.py --since 82ec540` — 다시 만들 페이지 다섯: `docs/design-kit/design-mockup.html` ·
  `docs/backend-kit/api-design.html` · `docs/harness/contract-design-guide.html` · `docs/harness/qa-evaluation-guide.html` ·
  `docs/harness/contract-schema.html`. 이 묶음 밖(부모 다음 차례의 문서 페이지 다시 만들기)으로 넘긴다

## tone-guide 5 단계 대조

1 단계에서 `.claude/tone-project.md`(어댑터 없음 · 주석 언어 ko)를 읽고 코어 네 파일과 `locale-korean.md` 규칙표를 불러왔다.
대상은 끝점에서 시작점 대비 더한 줄 205 줄(`.harness` 제외)이다.

| 패턴 / 규칙 | 건수 | 판정 |
| --- | --- | --- |
| C-01 · C-02 (what 반복 주석) | 0 | 통과 — 새 주석은 까닭(구멍 · 실측)만 적었다 |
| C-06 (공개 함수 계약) | 0 | 통과 — `plugin_utils.normalized` · `contains_block` 에 한 줄 docstring |
| C-13 (자화자찬 헤더) | 1 | 위반 아님 — `.claude/skills/meta-kaizen/SKILL.md` 16 줄의 「자동 생성한다」 는 기존 문장이고 마커 영역 설명이다 |
| F (구분선 블록) | 0 | 통과 |
| N-08 (한 글자 이름) | 0 | 통과 — 첫 판의 `dirty_except_status` awk 가 `o` · `n` · `a` · `b` 를 썼다가 대조에서 걸려 `old_no` · `new_no` · `cnt` · `old_hd` · `new_hd` 로 고쳤다 |
| N-09 (무역할 파일명) | 0 | 통과 — 새 파일은 `check-cause-table-copies.py` 하나 |
| S-03 · S-04 · S-06 | 0 | 통과 — 옮긴 함수 둘은 두 검사가 함께 쓰고 서로 부르지 않는다 |
| K-02 G-1 (번역투) | 1 | 위반 아님 — `flutter-toolkit/skills/flutter-audit/SKILL.md` 의 「적용된다」 는 원문을 글자 그대로 옮긴 사본 줄이다(사본 검사가 같은지를 잰다) |
| K-04 G-2 (`합니다`체) | 0 | 통과 |
| K-11 (새로 붙인 이름) | 0 | 통과 |
| H (보존) | — | 판정 표 사본 · 미검증 규칙 사본의 까닭 문장은 지우지 않았다 |

## 킷별 버전 판단

판 올림은 이 묶음에서 하지 않는다(릴리스 단계 몫). 다음 릴리스 때의 제안:

| 킷 | 제안 | 까닭 |
| --- | --- | --- |
| harness | patch | 규칙 문장 · 도우미 결함 고침 · 판 번호. 새 공개 약속 없음 |
| flutter-toolkit | patch | 사본 문장 맞춤 |
| react-kit | patch | 사본 문장 맞춤 |
| backend-kit | patch | 안내 문장 · 문구 |
| rust-kit | patch | 안내 문장 |
| infra-kit | patch | 안내 문장 |
| design-kit | patch | 순서 문장 한 줄 |
| bambu-kit | patch | README 수 정정 |

## 남은 것

- 문서 페이지 다시 만들기 다섯(위 검사 결과) — 부모 다음 차례
- `scripts/check-api-kit-docs.py` CI 등록 — 문서 페이지 차례에 같이
- 위 「이 묶음 밖으로 넘긴 것」 넷 그대로

### 끝 판 독립 검토가 찾은 것 (막지 않음 · QA APPROVE 뒤)

- `scripts/check-api-kit-docs.py:36-39` — `url(` 쪽 판정이 `https?://` 만 봐서 `url(//cdn.x/a.png)` 를 외부로 못 잡는다.
  `<link>` 쪽은 `//` 를 잡는다. `<img src="https://…">` · `@import"https://…"`(빈칸 없음)도 못 잡는데, 이 둘은 이번 변경 전부터 있던
  구멍이다. SC-01 의 18 사례에 이 모양이 없어 통과했다 — 다음에 이 검사를 CI 에 넣을 때 사례와 함께 고친다
- `scripts/check-cause-table-copies.py:26` — 원문 덩어리가 첫 `- **미확정**` 줄에서 끝나, 원문에서 그 줄 뒤에 더한 경우는 사본이
  안 따라가도 통과한다(scratch 사본에 한 줄 넣어 `checked=2 violations=0` 확인). SC-02 가 덩어리를 그렇게 정의했으므로 계약
  위반은 아니고 설계 한계다. 끝 표시를 덩어리 뒤 빈 줄이나 다음 절 머리로 옮길지 판단이 필요하다
- `harness/docs/guides/contract-design-guide.md:775` — 「작성 시점 패턴(조건 패턴 5 종)」 이 옛 수로 남았다. 같은 가지가
  `harness/skills/sprint-contract/SKILL.md:477` 을 「조건 패턴 8 종 (v5.7)」 로 올렸다. 옮겨 간 문장
  `docs/harness/contract-design-guide.html:1013` 에도 같은 말이 있어 문서 페이지 다시 만들 때 같이 맞춘다
- `docs/harness/contract-schema.html` 은 목차(`docs/index.html`)만 v5.7 이고 페이지는 아직 옛 판 — 위 문서 페이지 차례에 포함
