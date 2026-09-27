# vsb 묶음 메모 — 카이젠 오케스트레이터 · 킷 카이젠 스킬 문서 · 루트 README

- 계약: `.harness/sprint-contract-after-0926-orchestrator-docs.md` (조건 29, 봉인 `sha256:b58978bc9d7b1b4f` · 측정 `sha256:e55ee0c47d0dedbc`, 봉인 커밋 `c36c806`)
- 가지 `chore/ak2-vsb`, 시작 판 `6378948`. 시작할 때 추적 안 된 계약 파일 하나(앞 워크플로가 봉인 전에 멈춘 것)만 있었다. 앞 단계의 QA 리포트 · 계약 status 줄은 없었다
- 봉인 전 교차 진단 지적 다섯을 조건에 반영했다 — SK-02 문장에 Step 0.5 요구 추가, markdownlint 도구가 없으면 설치하거나 `MDL_UNAVAILABLE` 로 멈추기, AP-01 · AP-04 양성 대조, DG-05 대체 절차, SK-04 `종료 코드` 찾기 단독 실측

## 항목별 결과

| 항목 | 처리 | 커밋 | 자기 측정 |
| --- | --- | --- | --- |
| VS-3 | react-kaizen V8 행에 큰따옴표 검사를 더했다 | `5397f42` | `SK01 v8_rows=1 exec_bit=1 quote=1` |
| VS-7 | 같은 날 같은 사이클 항목이면 제목에 차례 번호 `(2)` 를 붙인다. Step 0.5 서술도 맞췄다 | `fe6539c` | `fresh rc=0,0 entries=2 heads=9 dup=0 md024=0 watch=1` · `error phase_only_rc=2 lines_after=1 no_log_rc=2 log_created=0` |
| VS-8 | Final F1 4 번에 `--watch` 감사 기록 호출, 연동 스크립트 줄은 Step F1 을 가리킨다. 옛 이름 「Step 11」 두 곳 정리 | `fe6539c` · `91d1e7d` | `SK02 old_step11=0 link_step=[Step F1] watch_call=1 step05_step11=0` |
| VS-11 | `KIT_SCOPE_DIRS` 에 `scripts/` · `templates/`, 자동 영역 다시 만듦, 의존성 맵 열한 줄 | `fe6539c` | `SC02 check_only_rc=0 want=11 scope_line=11/11 extra=0` · `SK03 dep_map=11/11 extra=0` · `ER02 drift_rc=1` |
| VS-16 | api 조사 지침의 Hurl 단정을 바로잡고 정본 · 종료 코드 `3` · 판정 불가를 적었다 | `fe6539c` | `SK04 cannot=0 verify_ref=1 exit3=1 unjudgeable=2` |
| VS-17 | 조사 입력 넷과 데이터 풀 수집기 표 둘의 앱 이름을 「Flutter 앱」 · 「Rust 서버」 로 바꿨다. 검사는 두지 않았다(아래) | `fe6539c` | `SK05 orch=0 templates=0 collector_table=0` |
| VS-18 | F2 의 「standalone」 을 공통 파일 `docs/assets/site.css` 링크 한 줄 + 인라인 `<style>` 로 | `fe6539c` | `SK06 standalone=0 site_css=1` |
| VS-19 | design · backend · rust-kaizen Gotcha 6 형제 표에 새 행 넷(rust 둘) | `5397f42` | `SK07 design_row=1 backend_row=1 rust_fail_row=1 rust_counter_row=1 rows=9,9,11 old_rows_lost=0` |
| VS-20 | bambu-kaizen 격차 표 fallback 행 · Step 4 음성 대조 실행 줄, bambu-research 를 킷의 「MakerWorld 읽는 순서」 로 | `5397f42` · `86b8862` | `SK08 cloudflare=0 fallback_order=1 step4_neg=1` · `SK09 server_name=0 bypass=0 order_ref=2 skill_ref=2` |
| VS-22 | F1 5 번에 `# 판 번호 원본 목록` 블록 (`BASE` · `END`) | `fe6539c` | bash · zsh 둘 다 `ref=31 got=31 equal=1 seven=7/7 err=0 argsub=0` |
| VS-23 | tone-kaizen Step 2 에 `# 강도 칸 앞머리 판정` 블록 | `5397f42` | `rules=69 read=69 unread=0`, D-04 망가뜨린 사본 `rules=69 read=68 unread=1` · `d04=1` |
| VS-25 | 루트 README 킷 절 열넷 · 스킬 블록 열넷(sync-docs 로 채움) · bambu references 9종 | `62a008f` | `AR03 kits=14 heads=14/14 order=1 blocks=14/14 links=14/14 sync_rc=0 insync=1 bambu_refs=9 old4=0 now=1` |

킷 폴더는 건드리지 않았다. 그래서 킷 판 올림 대상은 없다 — 바뀐 곳은 `.claude/skills/` (레포 전용 스킬) · `scripts/` · 루트 `README.md` 뿐이고, 셋 다 marketplace 판 번호가 없다.

## 앱 이름 검사 판단

「킷 안 앱 이름 0 건」 검사는 두지 않았다. 근거 셋:

1. 앱 이름이 조사 입력으로 다시 들어오는 자리는 오케스트레이터 표 둘 · 조사 지침 둘 · 데이터 풀 수집기 표 둘, 여섯이다. 이 묶음이 여섯 자리를 모두 종류 이름으로 바꿨다 (`SK05` 세 값 0).
2. 검사를 만들면 막을 앱 이름을 나열한 금지 목록이 된다. 목록에 없는 다른 앱 이름은 그대로 통과한다.
3. 저장소 전체로 걸면 harness 40 줄 · reflect-kit 4 줄이 실측 사례로 이미 이름을 써서 켜는 순간 실패한다. rust-kit 하나로 좁히면 이미 0 건인 곳을 지키는 빈 검사다.

데이터 풀 수집기의 프로젝트 이름 별칭 표(`scripts/collect-kaizen-data.py:136-163`)는 해시를 이름으로 되돌리는 실측 기록이라 조사 입력이 아니다 — 그대로 뒀다.

## tone-guide 결과

1 단계 로드 (2026-09-27 10:1x): `tone-kit:tone-guide` 스킬을 불러 오버레이 `.claude/tone-project.md`(어댑터 없음 · 주석 언어 ko)를 읽고, `core-comment.md` · `core-naming.md` · `core-structure.md` · `core-antipatterns.md` · `locale-korean.md` 규칙 표를 실제로 읽었다. 어댑터가 없으므로 스택 고유 대조 목록은 비활성이다.

5 단계 전수 대조 — 시작 판..가지 끝의 더한 줄 161 줄(`.harness` 제외) 기준:

| 규칙 | 건수 | 판정 |
| --- | --- | --- |
| C-01 · C-02 (what 대신 why) | 0 | 통과 — 새 주석 둘(`next_entry_tag` 설명 · `KIT_SCOPE_DIRS` 위 주석)은 왜(시작 · Final 항목이 한 날 겹침, 범위 밖이었던 실측)를 적는다 |
| C-04 · F (템플릿 마커 · 구분선) | 0 | 통과 |
| C-07 (해설 3 줄 초과) | 0 | 통과 |
| C-13 (자화자찬 헤더) | 0 | 통과 |
| C-15 (주석 파편형) | 0 | 통과 |
| N-07 (`effective` · `resolved` 이름) | 0 | 통과 — `grep -cE 'effective\|resolved'` 0 |
| N-08 (한 글자 이름) | 0 | 통과 — 새 셸 블록은 `doc` · `new` · `old` · `verdicts` · `cell` 을 쓴다 (`path` 는 zsh 에서 PATH 를 덮어 피했다) |
| N-09 (무역할 파일명) | 0 | 통과 — 새 파일 없음 |
| S-03 · S-04 (의미 없는 추출 · 그대로 넘기는 래퍼) | 0 | 통과 — 새 함수는 `next_entry_tag` 하나, 차례 번호 규칙에 이름을 준다 |
| S-06 (헬퍼 체인) | 0 | 통과 |
| K-02 G-1 (번역투 여섯) | 0 | 통과 — 더한 줄에 §8 G-1 정규식 0 건 |
| K-04 G-2 (`합니다`체) | 0 | 통과 |
| K-11 (새로 붙인 이름) | 0 | 통과 — 「MakerWorld 읽는 순서」 · 「음성 대조」 는 킷의 원래 절 이름 |
| H (보존 대상) | — | 옛 주석은 지우지 않았다. `KIT_SCOPE_DIRS` 위 주석은 뜻을 넓혀 이었다 |

## 문서 드리프트

`python3 scripts/detect-docs-drift.py --since 6378948` 출력(가지 끝 `86b8862` 기준):

```text
no docs drift since 6378948
```

도구의 매핑표에 오케스트레이터 → `docs/process/kaizen-flow.html` 이 없어 0 건이다. 범위 줄에 킷 `scripts/` · `templates/` 가 더해졌으므로 그 페이지 카드는 실제로는 낡았다 — 아래 「남은 것」.

## 검사 요약

- `python3 scripts/validate-plugin.py` → 14 plugins, 14 OK, exit 0
- `python3 scripts/sync-docs.py --check-only` → 모든 README가 동기화 상태입니다
- `python3 scripts/sync-evals.py --check-only` → 0 added, 0 orphans, 0 missing
- `python3 scripts/sync-orchestrator.py --check-only` → 이미 동기화됨 (13 plugins)
- 로컬 CI 결과는 부모 답에 적는다 (이 파일을 커밋한 뒤 가지 끝에서 돈다)

## 남은 것

- `docs/process/kaizen-flow.html` 범위 줄 카드 다시 만들기 — 문서 페이지는 부모 · 문서 묶음 몫이다. 드리프트 도구가 이 매핑을 모르므로 목록에 저절로 뜨지 않는다
- 루트 README `## 구조` 절 나무 그림 — 계약 범위(`:137-260`) 밖이라 두었다
- `bambu-kit/README.md` 의 「references 4종」 — 킷 README 라 킷 묶음 몫이다
- `.claude/skills/bambu-research/SKILL.md` description · Gotcha 5 의 「references 4종」 — 이 항목(VS-20)이 가리킨 문구가 아니라 두었다. 실제 수는 9 다
- 시각 변경 규약 세 파일의 절 이름 차이(편집 전 확정은 design 에만, 비교 반복 순서는 design · react 에만) — 형제 표 행이 대조 대상으로 적었을 뿐 킷 문서는 고치지 않았다
- 판 올림 — 킷 폴더 변경이 없어 해당 없음. 릴리스는 부모
