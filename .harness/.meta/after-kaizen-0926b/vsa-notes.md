# vsa 묶음 notes — 검사 스크립트 (validate · sync · 실행기)

- 계약: `.harness/sprint-contract-after-0926-check-scripts.md` (봉인 커밋 `6ee9ea5`, conditions_digest `sha256:ed9ff4a91d3ab1cd`, measurement_digest `sha256:7321baf2bcf86697`)
- 개정: `.harness/sprint-amendments-after-0926-check-scripts.md` A-01 — 동의 칸 비어 있음 (아래 「남은 것」 첫 줄)
- 가지 `chore/ak2-vsa`, 시작 판 `6378948`. 위임 시각 2026-09-26T10:09:00.557Z · 결정 답 2026-09-26T10:30:16.222Z (세션 `bda55d45-296c-491f-89ba-b52042d58e72`)
- 바깥 근거: VS-2 만 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/ex/EX-1.md` ([Hooks reference — Reference scripts by path](https://code.claude.com/docs/en/hooks#reference-scripts-by-path)) 를 인용했다. 나머지 열두 항목은 바깥 근거 없음 — 저장소 안 동작만 다룬다

## 항목별 결과

| 항목 | 결과 | 커밋 |
| --- | --- | --- |
| VS-1 | 회귀 패턴 실행기 — 빈 글에 맞는 패턴은 못 읽은 입력(종료 코드 2), 빈 목록은 FAIL(1), 글자가 아닌 `file` · `pattern` 은 그 항목만 못 읽은 입력으로 알리고 나머지를 끝까지 잰다 | `264206e` |
| VS-2 | V8 이 중괄호 없는 `$CLAUDE_PLUGIN_ROOT` 도 따옴표 · 실행 비트 검사에 넣는다. 가이드 V8 절 갱신. 바깥 근거 EX-1 | `ffd0de7` · `ddbde65` |
| VS-4 | sync-docs 가 빈칸 빠진 AUTO 표지를 짝 없는 표지로 파일 · 줄 번호와 함께 알리고 종료 코드 2 | `5d1edc5` |
| VS-5 | 표 설명 칸 = 설명 전체의 첫 문장. 킷 README 열 개와 루트 README 다시 만듦 (backend · bambu · infra 는 바뀐 칸이 없었다) | `5d1edc5` · `fab45da` · `c1a63ff` · `e414fc4` · `d21f781` · `88eab29` · `74bcd01` · `fc87fa3` · `6a0dad6` · `b8b998b` · `c579c55` · `ddbde65` |
| VS-6 | 표 구분 줄 `\| --- \|` 꼴, 빈 칸은 빈칸 하나. reflect-kit 에이전트 칸은 sync-docs 가 채우지 않는 손 글이라 구분 줄만 손으로 맞췄다. AUTO 블록 안 MD060 107 → 0 | VS-5 와 같음 |
| VS-9 | V3 · V6 · V10 이 CommonMark 코드 블록 판정 하나(`_split_code_blocks`)를 함께 쓴다. V6 범위에 `skills/*/references/**/*.md`, `--fix` 는 여는 줄을 고친다. V10 이 킷의 저장소 원본 폴더를 읽는다(짝은 `scripts/plugin_utils.py` `KIT_RESEARCH_DOCS`). 「언어 힌트 없는 펜스 8 개 먼저 고침」은 처리됨 — 여덟은 `pr-template.md` 의 `~~~markdown` 블록 안 줄이라 새 판정에서 코드다(가지 끝 전체 validate-plugin V6 모두 OK) | `ffd0de7` · `ddbde65` |
| VS-10 | V2 없음 줄 `no templates/ — OK` (결정 UD-8) | `ffd0de7` · `ddbde65` |
| VS-12 | Phase 부트스트랩 1~17. §2 · §3 은 수집기 §6 표 행대로(5 · 9 · 13 은 §2, 10 은 §3), §1 · §5 공통 선언은 유지 | `34703a7` |
| VS-13 | 드리프트 짝 넷(페이지 다섯) 추가, `--check-table` 로 스크립트 매핑 ↔ docs-site Step 1 표 맞대기, CI 단계 추가 | `e09fa91` · `a83b39e` · `e6a7e1c` |
| VS-14 | api-kit 문서 검사가 같은 사이트 상대 경로 `<link>` 를 외부로 세지 않는다 — 0/12 → 12/12 | `4092065` |
| VS-15 | run-evals · sync-evals 가 `cases` 를 읽고 api-kit 을 킷 목록에 넣음. api-kit 스킬 넷 사례 추가, CI 설명 줄 고침 | `874b550` · `39516b7` · `a83b39e` |
| VS-21 | 지운 워크트리는 reflect-kit 도 본 레포로(수집기 규칙), bare 레포 워크트리는 수집기도 워크트리 자신으로(reflect-kit 규칙). 실데이터 영향 0 (facets 18 개 경로 모두 살아 있음, 계약 작성 때 실측) | `05fce44` · `d94af6e` |
| VS-27 | 일부는 처리돼 있었다 — 킷 폴더 `onboarding-kit/` 은 `scripts/check-stale-values.py` `kit_dirs()` 가 2026-09-25 부터 읽는다. 남은 문서 사이트 원본 `docs/onboarding-kit/examples` · `docs/flutter` · `docs/howto` 를 더했다 (범위 26 → 29 폴더) | `157e8a2` |

## 조건별 자기 측정 (가지 끝, 도우미는 계약에서 떼어 낸 판)

| 조건 | 값 | 판단 |
| --- | --- | --- |
| SC-01 · ER-01 | `real rc=0 total=[Total: 14 passed, 0 failed] trace=0` · `empty-match rc=2 named=1` · `empty-list rc=1 named=1` · `nonstr-pattern/file rc=2 named=1 trace=0 others_measured=8` | 기대와 같음 |
| SC-02 | `v8-unquoted rc=2 quote=1` · `v8-quoted644 rc=2 exec=1` · `v8-quoted755 rc=0 checked=1` · `v8-otherVar` · `v8-interp644` `rc=0` | 같음 |
| SC-03 | `v3-tilde/nested rc=0 hit=0` · `v3-plain rc=2 hit=1` · `v6-tilde/nested rc=0 fail=0` · `v6-inline rc=2 fail=1 at_offset=4` · `v6-plain rc=2` · `v6-tildebare rc=0` · `v6-refs rc=2 fail=1` · `v6-fix` 은 여는 줄이 text 힌트를 받고 닫는 줄은 그대로 | 같음 |
| SC-04 | `real rc=0 vlines=140 not_ok=0` · `v2 line=[ V2 templates no templates/ — OK] skip=0` · `v10-research rc=2 hit=1` · `v10-unmapped rc=0 hit=0` | 같음 |
| SC-05 · SC-06 · ER-02 | `real rc=0 need=0` · `desc rows=112 not_first_sentence=0` · `md060_in_auto=0` · 파일별 경고 수 모두 시작 판 이하 · `marker-nospace/halfspace rc=2 lines=22,30 named=1` | 같음 |
| SC-07 | `table_rows=17` · `phases_ok=17/17 common_1_5=17/17 bad=[]` · `phase18 rc=1 help_17=1` | 같음 |
| SC-08 | `drift rc=0` · `pairs=5/5 neg_source_entries=0` | 같음 |
| SC-09 | `ci_lines=1` 은 맞지만 원 도우미로는 `table-real/drop/script-add rc=127` — 도우미 sed 결함. 고친 도우미로 `table-real rc=0` · `table-drop rc=1 named=1 changed=1` · `script-add rc=1 named=1 applied=1` | 개정 A-01 동의 대기 |
| SC-10 | `real rc=0 pass=[12/12 PASS] external=0` · `ext-css/js/import/font rc=1 named=1` | 같음 |
| SC-11 | `run-all total=[Total: 121 passed, 0 failed]` · `run-api line=[  PASS: 5 passed, 0 failed]` · `sync api_block=1 missing=0` · `covered=5 placeholder=0` · `neg-prompt rc=1 fail=1` · `neg-sync rc=1 missing=1` · `ci_stale_comment=0` | 같음 |
| SC-12 · SK-02 | `kinds_same=6/6 names=[repo repo repo repo bare-wt plain]` · `lib_stale=0 digest_line=1` | 같음 (기본 TMPDIR 로 잼) |
| SC-13 | `real rc=0 … 29/29 … missing_dir=0` · 네 파일 모두 `planted rc=1 named=1` | 같음 |
| SC-14 | `skip_word=0 ok_form=1` · `commonmark=1` 둘 · `v6_old_toggle=0 v6_refs=1` · `bare_var=2` · `research_dirs=9/9 stale_v6_sentence=0` · `version=1.5.0 history_row=1 history_names=V10 V2 V3 V6 V8` | 같음 |
| SK-01 | `table_sources=4/4` | 같음 |
| AR-01 · AR-02 | `changed=30 outside=0 required_missing=0` · `commits=24 mixed=0` · `harness_other=0` (notes · 개정 커밋 전 값) | 같음 |
| RE-01 · RE-02 | `old_toggle=0` · `map_in_validate=0 map_in_orchestrator=0 map_in_utils=1` · `v10-coupled rc=2 hit=0 gone=1 applied=1` | 같음 |
| AP-01 · AP-02 · AP-04 | `hardcoded_version=0` · `remote_branch=0` · `frontmatter_name=2/2` | 같음 |
| DG-02 · AP-03 | `md_files=15 md_new_warn=0 py=11/11 sh=2/2 json=1/1 actionlint_rc=0` · `bare_open=0` | 같음 |
| DG-05 | 로컬 CI `steps=25 rc0=25 not0=[]` · SKIP 은 `feedback-agg-test`(yq 없음) 하나 · 도구 밖 `run:` 줄은 설치 다섯과 `python3 scripts/detect-docs-drift.py --check-table` 하나 | 같음 |

## 남은 것

- **개정 A-01 동의** — SC-09 측정 도우미 `drift.sh` 23 번째 줄의 `sed -E 's/^\s+run: //'` 가 맥 BSD sed 에서 공백을 못 떼어 구현과 무관하게 `rc=127` 이 난다. `[[:space:]]` 로 한 글자만 바꾸는 개정인데, 원 측정이 어떤 구현도 통과 못 하므로 방향이 느슨해지는 쪽이라 위임으로 동의 처리하지 않았다. 부모가 사용자에게 묻는다
- 문서 페이지 다시 만들기 — `docs/harness/plugin-validation.html` (V2 없음 줄 글자 · 가이드 1.5.0). 계약 Counterpart 표의 미완 쪽이다. 부모 · 문서 묶음 몫
- 드리프트 도구가 `reflect-kit/skills/reflect-digest/SKILL.md → docs/reflect-kit/reflect-digest.html [NEW]` 를 낸다 — `reflect-kit/skills/` 접두 짝이 스킬마다 페이지를 기대하는데 그 페이지는 원래 없다. 이번 묶음이 만든 결함이 아니고 페이지를 만들지 · 짝을 좁힐지는 문서 묶음이 정한다
- 끝난 옛 계약(P11 · P13 · P14 · P16 · P17 DG-05 등)의 `— SKIP (no templates/)` 측정 꼴은 고치지 않았다 — 끝난 계약이라 다시 재지 않는다 (UD-8)
- 다른 스크립트의 킷 목록 사본 — `scripts/run-evals.py` `ALL_KITS` · `scripts/sync-evals.py` `TARGET_KITS` 는 여전히 손으로 적은 목록이다(이번엔 api-kit 만 더함). marketplace 에서 읽게 바꾸는 일은 범위 밖
- `scripts/sync-orchestrator.py` 는 `:125-148` 함수 말고 맨 위 import 한 줄(`from plugin_utils import KIT_RESEARCH_DOCS`)도 더했다 — 짝을 한 곳에서 읽으려면 필요했다. VS-11 몫인 `:39` 는 건드리지 않았다
- 킷 판 올림과 릴리스는 부모 몫 (아래 판단)
- 커밋 메시지 몇 개에 「게이트」 낱말이 들어갔다 (쉬운 말 목록 위반) — 이미 커밋돼 고치지 않았다

## tone-guide 결과

1 단계: 오버레이 `.claude/tone-project.md` (어댑터 없음 · 주석 언어 ko) 를 읽고 `tone-kit/references/` 의 core-comment · core-naming · core-structure · core-antipatterns · locale-korean 다섯 파일을 Read 로 불렀다. 어댑터가 없어 스택 고유 대조는 꺼져 있다.

5 단계 대조 (대상: 바뀐 스크립트 · 훅의 더한 줄 231 줄, 가이드 · docs-site 표 더한 줄):

| 규칙 | 건수 | 판정 |
| --- | --- | --- |
| C-01 · C-02 what 주석 · 이름 반복 | 0 | 통과 — 더한 주석은 이유 · 실패 모드(빈 글 패턴이 늘 통과, 짝이 한쪽만 늘어남 등) |
| C-04 · F 구분선 · 템플릿 마커 | 0 | 통과 (`#` 뒤 구분선 grep 0) |
| C-07 해설 3 줄 초과 | 0 | 통과 — docstring 최대 4 줄은 계약 설명 |
| C-13 자화자찬 | 0 | 통과 |
| C-15 문체 | 0 | 통과 — 파편형 · 단문 |
| N-07 · E `effective*`/`resolved*` | 0 | 통과 (grep 0) |
| N-08 한 글자 이름 | 2 → 0 | `scripts/detect-docs-drift.py` 맞대기 검사의 `s, o` 를 `source, output` 으로 고침 (`e6a7e1c`) |
| N-09 무역할 파일명 | 0 | 통과 — 새 파일 없음 |
| S-03 · S-04 · S-06 추출 · 래퍼 · 체인 | 0 | 통과 — `_split_code_blocks` 는 V3 · V6 · V10 셋이 쓰는 한 판정, `table_row` 는 표 그리는 함수 여덟이 쓴다. `table_head` 가 `table_row` 를 부르는 한 단계는 칸 모양 규칙을 한 곳에 두려는 것 |
| S-05 1회성 승격 | 0 | 통과 |
| S-07 안 생기는 방어 분기 | 0 | 통과 — 폴더 없음 FAIL 은 v10-coupled 로 실제로 생긴다 |
| K-02 번역투 6종 (G-1) | 0 | 통과 |
| K-11 새 이름 | 0 | 통과 — 「맞대기」는 문서 사이트 표에 기존 낱말 |
| H 보존 | — | 기존 실패 모드 주석(구분선 · 지운 워크트리 등) 삭제 0 — `facets_unmatched` 설명 한 줄은 동작이 바뀌어 새 사실로 바꿨다 |

## 문서 드리프트

`python3 scripts/detect-docs-drift.py --since 6378948` (가지 끝):

```text
harness/docs/guides/plugin-validation-guide.md → docs/harness/plugin-validation.html
reflect-kit/skills/reflect-digest/SKILL.md → docs/reflect-kit/reflect-digest.html  [NEW — 대응 HTML 없음, 신규 생성 + index.html 등록 필요]
```

페이지는 다시 만들지 않았다 — 부모가 모아서 한다. `python3 scripts/detect-docs-drift.py --check-table` 은 `스크립트 34 짝 · 표 33 짝 · 어긋남 0`.

## 킷별 판 올림 판단

| 킷 | 판 | 이유 |
| --- | --- | --- |
| harness | patch | 검증 가이드 문서(1.5.0) · README 표만. 킷 스킬 · 스크립트 동작 변화 없음 (검사 스크립트는 킷 밖 `scripts/`) |
| reflect-kit | patch | `hooks/_lib-project-id.sh` `project_root` 가 지운 워크트리를 본 레포로 잇는 버그 고침 + digest 설명 + README |
| api-kit | patch | 평가 사례 넷 추가 · README 표 |
| design-kit · flutter-toolkit · howto-kit · onboarding-kit · planning-kit · react-kit · rust-kit · tone-kit | patch | README 표(설명 첫 문장 · 구분 줄)만 |
| backend-kit · bambu-kit · infra-kit | 없음 | 바뀐 파일 없음 |

## 측정 도구

- 계약에서 떼어 낸 도우미: `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/vsa/k2/` (떼기 `…/vsa/extract.sh`, 전부 돌리기 `…/vsa/runall.sh`)
- 개정 A-01 을 적용한 도우미: `…/vsa/kfix/drift.sh` (지문 `6d4b0a25e0f48707`)
- 로컬 CI: `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` (지문 `59fe55125c0dbc77`), 결과 `…/vsa/ci-end/`
- markdownlint: `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/mdlint` (markdownlint-cli2 0.23.2)
