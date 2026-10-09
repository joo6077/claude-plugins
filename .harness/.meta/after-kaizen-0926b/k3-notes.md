# k3 — reflect · bambu · tone-kit 남은 것 (2026-09-27)

계약 `.harness/sprint-contract-after-0926-kits-reflect-bambu-tone.md` (봉인 `sha256:94c9205998801dd1`, 봉인 커밋 `1db0437`).
가지 `chore/ak2-k3`, 시작점 `6378948`. 시작할 때 앞 단계가 남긴 것은 추적 밖 계약 파일 하나뿐이었다(QA 리포트 · status 줄 없음).

## 사용자에게 알릴 것

- **SC-05 개정 A-01 이 동의를 기다린다.** 측정 첫 줄의 `mut=4` 는 봉인 전에 잰 적이 없는 값이다. 시작 판에서도 가지 끝에서도 `mut=10` 이라 원래 조건은 구현과 무관하게 통과할 수 없다.
  `mut=10` 으로 바꾸는 개정은 계산상 완화라 위임으로 동의 처리하지 않았다(`.harness/sprint-amendments-after-0926-kits-reflect-bambu-tone.md`, 동의 칸 비움). 나머지 값은 `rc=0 fixtures=24 match=8 bad=0 skip=16 skip_named=16` · 음성 대조 `rc=1 bad_class=1` 로 조건대로다.
- **KBa-1 은 목록 원문과 다르게 처리했다.** 목록은 「`[미검증]` 에 `enum 값 검사 미실행` 도 넣는다」 였는데, 판정 동작을 고치면 enum 판정이 실제로 돌아 그 문구가 거짓이 된다. 그래서 종류 줄이 없으면 종류 판정만 건너뛰고 `종류 검사 미실행` 을 적었다. 봉인 전 교차 진단이 이 판단이 맞다고 확인했다.

## 항목별 결과

| ID | 결과 | 커밋 · 근거 |
| --- | --- | --- |
| KRf-1 | 고침 — reflect-digest 멈춤 조건 두 줄을 「엔트리 0 이고 마지막 정상 종료 뒤의 Stop 실패 시도가 1 이상일 때」 로 | `7e28a50` · SK-01 `old=0 new=2` |
| KRf-2 | 고침 — 대체 경로 주석을 실제 호출 `claude -p --safe-mode --model haiku` 로 | `7e28a50` · SK-02 |
| KRf-3 | 고침 — README `install-scheduler.sh` 예시 세 줄에 따옴표 (EX-1 `.../ex/EX-1.md`, <https://code.claude.com/docs/en/hooks>) | `7e28a50` · SK-03 `bare=0 quoted=3` |
| KRf-4 `async` | 주석만 고치고 `nohup` 유지 — EX-1 은 command 훅에 `async` 가 있다고만 하고 `timeout` 과의 관계는 원문에 없다 (EX-1 `.../ex/EX-1.md`, <https://code.claude.com/docs/en/hooks>) | `7e28a50` · SK-02 `async_doc=1 hooks_same=1` |
| KRf-4 `last_assistant_message` | 고침 — Stop 훅이 입력의 마지막 응답을 가려서 프롬프트 끝 `<last_assistant_message>` 블록에 싣는다. 필드가 없으면 프롬프트가 시작 판과 바이트까지 같다 (EX-1) | `7e28a50` · SC-01 |
| KRf-4 지워진 워크트리 | 고침 — facets 대조가 `/.claude/worktrees/` 앞에서 잘라 본 레포 이름으로 묶는다(`collect-kaizen-data.py` 와 같은 규칙) | `7e28a50` · SC-02 |
| KRf-5 | 원인 조사 · 문서 한 줄 — `err=` 가 없는 `fail:codex-exit-2` · `fallback:claude-exit-1` 은 0.8.0 전 판 훅을 쥔 세션 `d204ea78`(9 월 22 일 시작)이 적었다. 새 판 실패 줄(`err=` 붙은 줄) 0 이라 멈춤 문턱은 그대로 둔다 | `7e28a50` · SK-04 |
| KBa-1 | 고침 — 위 「사용자에게 알릴 것」 | `7b2e4ba` · SC-03 |
| KBa-2 | 고침 — `bambu-kit/evals/run-gate-fixtures.sh` 가 SKILL.md 표 · 실행 줄을 읽어 시험 파일 24 개를 판정. CI 한 단계 | `7b2e4ba` · `95457e4` · `1185415` · `5a33db9` · SC-04 · SC-05 · ER-01 · SK-05 |
| KBa-3 | notes 에만 적음 — 아래 「충돌 자리」 | 그 가지는 건드리지 않았다 |
| KBa-4 네 칸 | 고침 — `[미검증]` 을 적는 다섯 자리에 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령) | `7b2e4ba` · SK-06 `spots=5/5 def=1` |
| KBa-4 현행화 | 고침 — 뱀부 2.8.4 beta `v02.08.04.57`(2026-09-22) · 정식 `v02.08.02.61`(2026-08-21) · PLA Pure 설치본 번들 4 개 (이 맥 관측 2026-09-27) | `7b2e4ba` · SK-07 |
| KBa-4 금지 키 시험 파일 | 고침 — `process-forbidden-key.json` (`elephant_foot_compensation`) | `7b2e4ba` · SC-06 |
| KBa-4 답글 · 403 | 고침 — 받는 법 블록이 `commentReply` 배열 수와 `replyCount` 합을 한 줄로 낸다. `makerworld-fetch-test.sh` 가 답글 · 403 경우를 잰다 | `7b2e4ba` · `88b1f4b` · SC-07 · ER-02 |
| KBa-4 임시 파일 | 고침 — 음성 대조 블록 끝에 `trap` 으로 임시 파일 · 폴더를 지운다 (시작 판 18 개 → 0) | `7b2e4ba` · SC-08 `left=0 exits=50` |
| KBa-4 `G91` | 실물 확인 필요 — H2S 펌웨어가 `G91` 을 E 에도 적용하는지는 펌웨어 원문이 저장소 밖이다. 지금은 `M83` 만 써서 영향 0 | 고치지 않음 |
| KT-1 | 고침 — `fallback_identifier_pattern` 칸이 §4 첫 `text` 코드 블록 넷째 줄을 가리킨다 | `cb612c1` · SK-08 |
| KT-2 | 고침 — `docs/tone/dart-flutter-idioms.md` 머리 `0.2.0` · `2026-09-27`, 페이지 부제 · 끝 캡션도 같게. 0.1.0 뒤 원본 커밋 셋 가운데 `358f8e1` 이 규칙(N-12 / D-15)을 더해 부판을 올렸다 | `130a7aa` · `8216e19` · SK-09 |
| KT-3 판 · 링크 | 고침 — 제스처 콜백 기준 판에 3.47.5 병기(두 판 58 개, 목록 같음), go_router 최신 18.0.1 · 17.0.0 깨지는 변경 · 18.0.0 `material_ui` 이전, 스타일 가이드 새 주소, 「마지막 세 행」 → 행 이름 (EX-14 `.../ex/EX-14.md`, <https://storage.googleapis.com/flutter_infra_release/releases/releases_macos.json> · <https://pub.dev/api/packages/go_router> · <https://github.com/flutter/flutter/blob/main/docs/contributing/Style-guide-for-Flutter-repo.md>) | `cb612c1` · `130a7aa` · `8216e19` · SK-10 · SK-11 |
| KT-3 1,867 줄 | 처리됨 — 킷 · `docs/tone` 어디에도 그 수치가 없다 (`lines1867=0`) | — |
| KT-3 `locale-korean.md` §2 grep 열 | 처리됨 — `b367184` 가 이미 고쳤다 | — |
| KT-3 C-06 강도 · `etc_seq=663` 이름표 · `__` 예시 | 바깥 근거 없음 — EX-14 가 다루지 않았다. 새로 찾지 않았다 | 고치지 않음 |

## 충돌 자리 (KBa-3)

다른 세션 가지 `feat/bambu-kit-orca-h2s-feedback`(끝 `42209be`)과 겹치는 SKILL.md 자리는 시작 판 기준 다섯이다 —
`:1836-1846`(음성 대조 머리글) · `:1854-1872`(시험 파일 표) · `:1923-1941`(실행 줄) · `:1956-1985`(지운 사본 줄) · `:2443-2444`(점검 목록), 그리고 `docs/bambu-kit/bambu-print-profile.html`.

이 가지가 줄을 더하거나 바꾼 자리(시작 판 줄 번호): `:1608` · `:1701` 완료 검사 종류 판정, `:1846` 뒤 한 줄 · `:1870` 뒤 표 한 행, `:1889` 뒤 `trap` 두 줄, `:1939` 뒤 실행 줄 하나,
`:1980` 뒤 금지 키 변이 네 줄, `:2018` 뒤 종류 줄 빠진 목록 변이 네 줄, `:2041` 뒤 설명 한 줄, 받는 법 `:2469` 표 행 · `:2505` 뒤 세 줄, 릴리스 현황 `:2548`.
앞 넷은 위 충돌 자리와 바로 붙어 있어 그 가지를 합칠 때 충돌 줄이 는다.

## 킷별 버전 판단

- reflect-kit `0.9.0` → **0.10.0** 권장 — Stop 훅이 분석기에 넘기는 입력이 늘었다(마지막 응답 블록).
- bambu-kit `0.10.1` → **0.11.0** 권장 — 완료 검사 판정 동작이 바뀌고 시험 실행 스크립트 둘이 생겼다.
- tone-kit `0.2.1` → **0.2.2** 권장 — 참조 문서 표기 · 링크만 고쳤다.

`plugin.json` 은 건드리지 않았다(릴리스 단계 몫).

## 문서 사이트 드리프트

`python3 scripts/detect-docs-drift.py --since 6378948` 이 낸 페이지. `docs/tone-kit/dart-flutter-idioms.html` · `docs/tone-kit/naming-taxonomy.html` 은 SK-09 · SK-10 이 고친 줄만 원본과 맞췄다. 페이지 재생성은 부모 몫이다.

- `docs/bambu-kit/bambu-print-profile.html`
- `docs/bambu-kit/bambu-fields-baseline.html`
- `docs/bambu-kit/failure-recipes.html`
- `docs/bambu-kit/materials.html`
- `docs/tone-kit/dart-flutter-idioms.html` (고친 줄 말고 나머지 — 원칙 · 슬롯 수 등은 다시 보지 않았다)
- `docs/tone-kit/naming-taxonomy.html`
- `docs/reflect-kit/reflect-digest.html` — 대응 페이지 없음(새로 만들고 index 등록 필요)
- `docs/tone-kit/adapter-dart-flutter.html` — 대응 페이지 없음
- `docs/tone-kit/sources.html` — 대응 페이지 없음

## 톤 대조 (tone-kit:tone-guide 5 단계)

1 단계로 읽은 것: 오버레이 `.claude/tone-project.md`(어댑터 없음 · 주석 한국어), `core-comment.md` · `core-naming.md` · `core-structure.md` · `core-antipatterns.md` · `locale-korean.md`. 어댑터가 없어 스택 고유 대조는 돌리지 않았다.
대상은 시작 판 대비 더해진 줄 268 줄(`.harness` 제외).

| 규칙 | 건수 | 판정 |
| --- | --- | --- |
| C-01 what 대신 why | 0 | 통과 — 새 주석은 이유 · 실패 모드(마지막 응답이 transcript 에 아직 없을 수 있다, 빈 파일을 돌리면 종료 코드 0 등) |
| C-02 · A 이름 번역 주석 | 0 | 통과 |
| C-04 · F 구분선 · 템플릿 마커 | 0 | 통과 — 새 `#` 구분선 0 |
| C-07 해설 3 줄 초과 | 0 | 통과 — 스크립트 머리 설명(6 줄)은 파일 헤더라 대상 밖 |
| C-10 디자인 툴 참조 | 0 | 해당 없음 |
| C-12 계산 근거 | 0 | 통과 |
| C-13 자화자찬 | 0 | 통과 (grep 0) |
| C-15 주석 파편형 · 단문 | 0 | 통과 (관측 컨벤션) |
| H 보존 | — | 지운 주석 0 — 바꾼 주석(머리 `async` 줄, 대체 경로 줄, facets 머리)은 사실을 고친 것 |
| N-07 · E `effective*` · `resolved*` | 0 | 통과 (grep 0) |
| N-08 한 글자 이름 | 2 → 0 | 고침 — `local u` → `usage`, `local d` → `run_dir` (`1bdbad3` · `88b1f4b`). `n` · `bad` · `W` · `T` · `A` · `B` 는 같은 폴더 시험 · SKILL.md 블록의 기존 관례를 따랐다(S-12) |
| N-09 무역할 파일명 | 0 | 통과 — `run-gate-fixtures.sh` · `makerworld-fetch-test.sh` |
| S-03 · S-04 · S-06 추출 · 래퍼 · 체인 | 0 | 통과 — 새 함수 `miss` · `run_block` · `check` 뿐, 헬퍼가 헬퍼를 부르지 않는다 |
| S-12 같은 카테고리 같은 패턴 | 0 | 통과 — 새 시험은 `check` · `결과: N 경우 중 불일치 M` 형식을 따른다 |
| K-02 번역투 여섯 가지 (§8 G-1) | 0 | 통과 |
| K-04 종결형 | 0 | 통과 — 새 문서 문장은 `한다` 체 |
| K-05 음역 | 0 | 통과 |
| K-11 새 이름 | 0 | 통과 — 「건너뜀」 · 「네 칸」 은 기존 문서의 말 |
| K-10 대조 · 자기모순 검사 | 실행 | G-1 잔존 0 · G-2 · G-3 해당 없음(`///` doc 없음) |

## 자기 측정 (가지 끝 기준)

- SK-01 `old=0 new=2` · SK-02 `old_fb=0 new_fb=1 old_async=0 async_doc=1 hooks_same=1` · SK-03 `bare=0 quoted=3` · SK-04 `1`
- SK-05 `gate_steps=1 both=1 all_bambu_steps=1` · SK-06 `spots=5/5 def=1` · SK-07 `beta=1 stable=1 pure_old=0 pure_new=1 rel=1 rel_old=0`
- SK-08 `g04=0 fourth=1 line4_ok=1` · SK-09 `version=0.2.0 gt010=1 last_updated=2026-09-27 date_ok=1 sub=1 cap=1 old_sub=0 old_cap=0` · SK-10 `only_3384=0 short=[]`
- SK-11 `gor_rows=1 gor=1 gor_note=1 wiki_old=0 wiki_new=1 last3=0 k11=1 lines1867=0`
- SC-01 `mark=1 key=0 nofield_same=1` · `test_rc=0 결과: 35 경우 중 불일치 0 lam_cases=3` · SC-01N `mut=2 neg_lam_bad=1`
- SC-02 `facets 1개 · 마찰 있는 세션 1개 · 그중 reflections 없음 1개` · `test_rc=0 결과: 19 경우 중 불일치 0 wt_cases=1` · SC-02N `neg_wt_bad=1`
- SC-03 `notypes fail=1 scope=0 enum=1 unv=1 exit=1` · `full fail=1 enum=1 exit=1` · `old_text=0 para=1 neg_line=1`
- SC-04 `rc=0 fixtures=24 match=24 bad=0 skip=0 last=[결과: 24 경우 중 불일치 0]` · `linux_safe=0 fixture_literals=0` · SC-04N `mut=1 rc=1 bad_enum=1` · `norun mut=1 rc=1 missing=1`
- SC-05 `mut=10 rc=0 fixtures=24 match=8 bad=0 skip=16 skip_named=16` · `neg mut=1 rc=1 bad_class=1` — `mut=4` 가 아니라 개정 A-01 동의 대기
- SC-06 `fail=1 forbid=1 exit=1 | mut=1 1 exit=0` · `row=1 runline=1`
- SC-07 `reply_line=1 exit=0 | 403: fail_design=1 exit=1` · `table=1` · `test_rc=0 결과: 5 경우 중 불일치 0 c403=2 creply=1` · SC-07N `mut=1 rc=1 bad_reply=1`
- SC-08 `names=[emptylist gate noenum notypes] left=0 exits=50` · ER-01 `rc=2 stop=1 match=0`
- RE-01 `gate_env=2 fetch_env=2` · RE-02 `fetch_anchor=2 fetch_copy=0`
- AR-01 `extra=0 multi_top=0 reflect=6 bambu=7 tone=2 docs_tone=2 github=1` (notes 커밋 전)
- DG-02 `md_new=0 sc_new=0 json_bad=0` (셸 검사 경고 둘은 `1185415` 에서 이유와 함께 껐다)
- validate-plugin reflect-kit · bambu-kit · tone-kit 각 `Exit: 0` · sync-docs `--check-only` 동기화됨 · sync-evals `--check-only` `0 added, 0 orphans, 0 missing`
- 로컬 CI `ci-local.sh`(sha256 앞자리 `59fe55125c0dbc77`) — `rc=0` 25 줄, 나머지 한 줄 `feedback-agg-test SKIP (yq 없음)`

## 남은 것

- 개정 A-01(SC-05 `mut` 값)은 동의 없이 1 회차 개정 파일에 남는다. 2 회차 계약이 그 조건을 바로잡아 다시 봉인했으므로 동의가 없어도 막히는 것은 없다 — 아래 「2 회차 계약」.
- 문서 사이트 페이지 재생성 — 위 드리프트 목록 아홉(부모).
- SKILL.md 버전 교차 확인 표(시작 판 `:2541-2545` 「references 는 `02.06.00.51` 기준」)는 `/bambu-research` 몫이라 고치지 않았다.
- `compatible_printers` · 메타필드 · 숫자 타입 검사의 FAIL 시험 파일은 목록 밖이라 만들지 않았다.
- `G91` 실물 확인(H2S 펌웨어). KT-3 의 C-06 강도 · `etc_seq=663` · `__` 예시는 바깥 근거를 새로 찾아야 판단할 수 있다.
- 킷 버전 올리기(릴리스 단계).

## 2 회차 계약

1 회차 SC-05 측정 기대 `mut=4` 는 봉인 전에 잰 적 없는 값이었다(시작 판 · 가지 끝 모두 `mut=10`). 결정 파일 「추가 위임」 절대로 개정 대신 새 판 계약을 다시 봉인했다.

- 계약 `.harness/sprint-contract-after-0926-kits-reflect-bambu-tone-r2.md` — 조건 32(기능 24), 봉인 `sha256:9ee4c5cccc722588` · 측정 지문 `sha256:69bb247ef8d5b16a` · `locked_at` 2026-09-27 12:24, 봉인 커밋 `0ece417`(파일 1 개).
- 1 회차 처리: QA 리포트(REJECT) 커밋 `7f0a203`, 1 회차 계약 `status: superseded` 커밋 `e52318f`(조건 줄은 그대로, 봉인 `94c9205998801dd1` 유지).
- 1 회차와 달라진 조건 줄은 AR-01 하나(기대 경로 스물넷 → 스물일곱 — 2 회차 계약 · 피드백 · 개정 세 경로). 측정 줄은 SC-05 두 줄이 바뀌고 음성 대조 `SC-05N` 이 더해졌다.
- 교차 진단(qa-evaluator, 봉인 전): 도우미를 직접 돌려 SC-05 · SC-05N · AR-01 값을 글자 그대로 재현, 나머지 31 조건은 1 회차와 바이트가 같다고 확인. 지적 하나 — 1 회차의 `status: superseded` 가 스키마 값 밖이라는 것. 봉인 차단은 아니어서 배경에 까닭만 적었다(`supersedes_digest` · `supersedes_commit` 은 같은 파일을 다시 봉인할 때 쓰는 평가자 칸이라 새 파일인 이 계약엔 맞지 않는다). 배경의 굵은 글씨 가짜 제목 둘은 `###` 로 바꿨다.
- 6.5 재통과: `##` 헤더 12 개 모두 허용 · `OK conditions=32` · `UNCOVERED` 13 건 모두 「범위 경계」 해소 줄 · `OK 미실측 0 건`. 봉인 직후 `SEAL_OK` · `MEASURE_OK`.
- 피드백: `~/.harness/feedback/contract/1a3bcba6-2026-09-27T123130-bda55d45-47965.yaml` · `verify-feedback.sh` PASS.
- 새 코드는 쓰지 않았다. 2 회차 조건이 구현 빈틈을 드러낸 곳은 없다.

### 2 회차 자기 측정 (끝점 `0ece417`, 도우미는 봉인된 계약에서 뽑은 판 — 앞 사본과 바이트가 같다)

- SK-01 ~ SK-11 · SC-01 ~ SC-04 · SC-06 ~ SC-08 · ER-01 · RE-01 · RE-02 · DG-02 값은 위 「자기 측정」 과 같다.
- SC-05 `mut=10 rc=0 fixtures=24 match=8 bad=0 skip=16 skip_named=16` · `neg mut=1 rc=1 bad_class=1` · SC-05N `noskip mut=1 rc=1 bad=16 skip=0 match=8` — 2 회차 기대대로.
- ER-02 (`m SC-07`) `403: fail_design=1 exit=1` · `c403=2`.
- AR-01 `changed=25 extra=0 multi_top=0 reflect=6 bambu=7 tone=2 docs_tone=2 github=1` (notes 커밋 전) · AR-02 `committed=1` 서른 토큰 모두 1 이상 · `rc=0 pages=9 miss=0`.
- AP-03 `--check=code-fence` 종료 코드 0 · AP-04 `--check=frontmatter` 종료 코드 0 · DG-01 `scripts/release.sh` 0.
- validate-plugin 전체 `Total: 14 plugins, 14 OK` · sync-docs `--check-only` 동기화됨 · sync-evals `--check-only` `0 added, 0 orphans, 0 missing`.
- 킷 시험: reflect 35 · 19 경우, bambu 완료 검사 24 경우, 받는 법 5 경우 — 모두 불일치 0.
- 로컬 CI `ci-local.sh`(sha256 앞자리 `59fe55125c0dbc77`, 끝점 `0ece417`, 247 초) — `rc=0` 25 줄, 나머지 한 줄 `feedback-agg-test SKIP (yq 없음)`.
- 원본 문서는 이번 회차에 바꾸지 않아 문서 사이트 드리프트 목록은 위와 같다(아홉).

### 2 회차 톤 대조 (tone-kit:tone-guide 5 단계)

이번 회차에 바뀐 것은 `.harness` 의 계약 · QA 리포트 · 이 notes 뿐이고 코드 · 킷 문서는 0 줄이다. 그래서 주석 · 이름 · 구조 규칙은 대상이 없고, 한국어 문체 규칙만 새 글에 대조했다.

| 규칙 | 건수 | 판정 |
| --- | --- | --- |
| C · N · S (주석 · 이름 · 구조) | — | 대상 없음 — 코드 변경 0 줄 |
| K-02 번역투 | 0 | 통과 |
| K-04 종결형 | 0 | 통과 — 「한다」 체 |
| K-05 음역 | 0 | 통과 — 새로 음역한 낱말 없음 |
| K-11 새 이름 | 0 | 통과 — 「2 회차 계약」 · 「새 판」 은 결정 파일의 말 |

### 킷별 버전 판단 (2 회차)

바뀐 것이 없어 위 판단 그대로다 — reflect-kit 0.10.0 · bambu-kit 0.11.0 · tone-kit 0.2.2 권장, `plugin.json` 은 릴리스 단계 몫.

### 2 회차 남은 것

- 2 회차 QA 는 APPROVE — 29 조건 실측 · 음성 대조 8 개 직접 실행, 리포트 `.harness/sprint-feedback-after-0926-kits-reflect-bambu-tone-r2.md` 와 계약 `status: done` 을 `6353e14` 로 커밋했다.
- 독립 검토 결함 하나(막는 것 아님): `bambu-kit/evals/run-gate-fixtures.sh:63-72` 가 FAIL 줄 수 · `RESULT: PASS` 줄 · 종료 코드만 보고 `[미검증]` 줄 수는 판정하지 않는다. 표의 `filament-lattice-fanfix.json`(「`[미검증]` 0 줄」) · `process-thin-baseline.json`(「벽 예산 `[미검증]` 1 줄」) 두 행의 기대 일부가 재지 않는 채 남는다. 검토자가 SKILL.md 사본 완료 검사에 가짜 미검증 줄 하나를 넣어도 `결과: 24 경우 중 불일치 0` 이 나왔다. 리눅스 CI 에서는 설치본이 없어 fanfix 에도 `[미검증]` 이 1 줄 생기므로 일부러 뺀 것으로 보이나, 그 까닭이 스크립트 머리 주석 · 표 문구에 없다. 다음 bambu-kaizen 에서 슬라이서가 있을 때만 `[미검증]` 줄 수를 대조하거나, 빼는 까닭을 주석에 적는다.
- 스키마에 새 판 계약을 가리키는 정식 칸이 없다 — 다음 계약 카이젠 후보(피드백 제안에 적음).
- 위 「남은 것」 의 문서 사이트 재생성 · 버전 올리기 · `G91` 실물 확인 · 바깥 근거 없는 KT-3 세 항목은 그대로 남는다.
