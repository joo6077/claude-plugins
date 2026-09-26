---
feature: "harness 커밋 훅 · 오케스트레이터 · 문서 매핑 후속 (c1b)"
slug: after-0924-harness-orch
created: "2026-09-26 11:57"
complexity: "복잡"
conditions: 27
status: active
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:d65525591fade384
locked_at: "2026-09-26 12:17"
---

## 배경

2026-09-24 카이젠이 다음 사이클로 넘긴 것 가운데 harness 커밋 안전 훅 · 카이젠 오케스트레이터 · 문서 사이트 매핑 다섯 묶음을 고친다.
근거는 `.harness/.meta/kaizen-0924/f1-harness-followups-notes.md` §다음 사이클 메모(F1H-76 · F1H-77 · F1H-91 · F1H-92 · 「구현 중 새로 찾은 것」 첫 줄) ·
`final-notes.md` §다음 사이클 메모(FN-79) · `f2-review-fixes-notes.md` §고치지 않은 항목과 이유(C L2 · C L3 · C L7) · §다음 사이클 메모 · §교차 진단 뒤 기록 둘째 줄,
그리고 핸드오프 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-0110.md` §C1 이다.

사용자 합의(Step 5): 사용자는 2026-09-26T01:04:21.505Z 에 「다음 세션에서 직접할 일을 다 실행하고 이어질것도 실행해」
(세션 기록 `/Users/jackson/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0.jsonl`),
그 전 2026-09-24T04:04:16.964Z 에 「나한테 물어보지 말고 자동으로 끝까지」 라고 지시했다. 이 계약의 합의는 이 위임으로 받은 것으로 적는다.
판단이 갈린 곳은 저장소 안 근거로 정했고, 정한 내용은 아래 `## 범위 경계` 와 구현 기록 파일에 적는다.

공통 전제 — 모든 조건의 측정은 아래 여섯 줄을 먼저 정의한 셸(zsh 또는 bash)에서 돈다. 조건마다 다시 적지 않는다.

- `W=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c1b` (작업 폴더, 가지 `chore/ak-c1b-harness-docs`)
- `T=$W/.harness/.meta/after-0924/harness-orch-tools` (측정 도우미 17 개 — `## 배경 — 측정 도우미` 표)
- `CF=$W/.harness/sprint-contract-after-0924-harness-orch.md`
- `B=f81568d` (가지를 만든 기준, origin/main `#110` 합친 커밋)
- `U=$(git -C "$W" rev-parse --verify -q chore/ak-c1b-harness-docs) || exit 2` (상한 — `HEAD` 로 떨어지지 않고 멈춘다)
- `Given:` 이 스프린트의 커밋이 모두 끝났고 `git -C "$W" rev-parse HEAD` 가 `$U` 와 같다. 커밋 전 작업 폴더 상태를 재는 조건은 없다

복잡도 네 축:

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 계층을 지나는가 | 셋 — 커밋 훅(셸) · 문서 생성 스크립트(파이썬) · 스킬 문서(마크다운) |
| 공개 동작·계약 변경 | 밖에서 보이는 판정 · 출력이 바뀌는가 | 예 — 훅이 막던 커밋을 통과시킨다 · 낡음 감지 결과 · AUTO 범위 줄 · 데이터 풀 §6 이 바뀐다 |
| 소비면 존재 | 반대편이 있는가 | 예 — 훅 시험 · harness README · 오케스트레이터 F2 · docs-site Step 1 · AUTO 영역 · Post-Kaizen 검사 스크립트 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 훅이 진짜 대량 삭제를 놓치면 사고가 난다 |

네 축 모두 예이고 공개 동작 변경 · 소비면이 함께 있으므로 「복잡」 이다. 기능 조건은 19 개다.

## 배경 — 측정 도우미

조건이 부르는 도우미는 `$T` 아래 17 개다. 봉인 뒤에는 고치지 않는다 — `AR-03` 이 아래 sha256 앞 16 자리로 잰다.
도우미는 봉인 커밋(계약 1 개) 바로 다음 커밋으로 올린다.

| 파일 | sha256 앞 16 자리 |
| ---- | ----------------- |
| `accent.py` | `d25695c9e00d8e06` |
| `drift_e2e.sh` | `09d524afb978f73c` |
| `drift_map.py` | `77af52d6484db2df` |
| `guard_probe.sh` | `9af7e1e5317377e1` |
| `guard_test_neg.sh` | `cee472396772d8a3` |
| `lint_new.sh` | `ad22d53d9d601659` |
| `map_tables.py` | `fccbe6f871197970` |
| `perf.sh` | `415d5940b8ac896b` |
| `phase17.py` | `015e321ad4243997` |
| `phase_ref.sh` | `76562247dcf5fcf7` |
| `regress.sh` | `0ebf375b7fb14a48` |
| `rlog_sets.py` | `296b137d00dc5b84` |
| `scope_diff.sh` | `4b0ed6a6ea60be0c` |
| `scope_folders.py` | `d4147ccfb5c9c3a6` |
| `scope_gap.py` | `6f3bef62066f25da` |
| `sync_err.sh` | `f4840169b2eead6b` |
| `validator_neg.sh` | `561c742484899295` |

봉인 전 교차 진단(qa-evaluator) 지적 다섯 곳을 반영했다 — `phase17.py` 는 제목 뒤 괄호 부연을 허용하고, `scope_folders.py` 는 스킬 references 를 구체 경로로 적어도 덮인 것으로 보며,
`perf.sh` 는 훅 · `jq` 가 없으면 `STOP` 으로 멈추고, `map_tables.py` 는 docs-site 를 Step 1 절만 읽는다. 네 파일은 고친 뒤 아래 기준값을 다시 쟀다(값 변화 없음).
양성 대조(고친 뒤): `phase17.py` 는 괄호 부연 제목 · 부연 없는 제목 둘 다 `heading=1 invented=1 missing_paths=1`, `scope_folders.py` 는 bambu 별표 줄을 구체 경로로 바꾼 사본에서 `bambu-kit: miss=[]` ·
api 스킬 references 다섯 중 하나만 적은 사본에서 `api-kit/skills/*/references/` 가 그대로 miss, `perf.sh` 는 없는 훅에 `STOP` · 종료 코드 2.

봉인 전 실측(2026-09-26, `$W` 가 `$B` 와 같은 상태 · 이 맥 bash 3.2 · python 3.14.3):

| 도우미 · 명령 | 기준값 (고치기 전) | 알려진 답 · 대조 |
| ------------- | ----------------- | ---------------- |
| `bash $T/guard_probe.sh $W/harness/scripts/commit-guard.sh` | `mismatch=6/9 mismatch_sc=5/7 mismatch_er=1/2` — MISMATCH 는 G1 · G2 · G3 · G4 · G7 · G8 | 손으로 돌린 같은 아홉 경우와 같다. G7 은 `삭제 120 개`(옮긴 60 + 진짜 삭제 60) |
| `bash $T/guard_test_neg.sh $W $B` | `old_fail=0 old_rc=0 new_pass=44 new_fail=0 new_rc=0` | 기준 훅과 지금 훅이 같아 두 쪽 FAIL 0 |
| `bash $T/perf.sh <훅> 'git commit -o -m x -- d1 d2' add` | `rc=0 sec=0.40` (파일 2000 개 이동, 지금도 목록 사본을 쓰는 경로 지정 커밋) | `-a` · `add -A` 는 `rc=2 sec=0.16` |
| `bash $T/drift_e2e.sh $W` | `expected_hit=1/7 unexpected=1 entries=2 rc=0` — 초안 `docs/howto/drafts/SKILL.md` → `docs/howto-kit/drafts.html` 이 없는 페이지로 나온다 | 대조용 `docs/howto/deep-links.md` 만 맞게 나온다 |
| `python3 $T/drift_map.py <$U 복제본> <$B 복제본>` | `orphan_pages=26 new_targets=44 added_orphan=0 added_new=0` | 짝 없는 페이지 26 을 손으로 셌다(backend 2 · design 8 · flutter 1 · harness 1 · howto 1 · infra 2 · react 8 · reflect 3) |
| `python3 $T/map_tables.py $W` | 두 스킬 파일 모두 `rows=15 script_only=2 table_only=0 ghost=0`, `script_ghost=1` (docs-site 는 Step 1 절만 읽은 값) | 스크립트에만 있는 둘은 `docs/flutter/` · `planning-kit/references/`, 디스크에 없는 하나는 `planning-kit/references/` |
| `python3 $T/scope_gap.py $W` | `uncovered=8 phases=13` | P5 1 · P10 1 · P11 2 · P12 2 · P16 1 · P17 1 을 손으로 셌다 |
| `python3 $T/scope_folders.py $W` | `folder_miss=20 ghost=0 kits=13` | flutter 3 · design 3 · backend 2 · infra 2 · rust 2 · react 1 · planning 1 · reflect 3 · api 2 · howto 1 |
| `bash $T/phase_ref.sh $W` | `orch_missing=[15, 16, 17] pool_missing=[13, 14, 15, 16, 17]` · 나머지 빈 목록 · `collector_rc=0` | 오케스트레이터 표 `:297-312` 가 14 까지, 수집기 `:1698-1711` 이 12 까지인 것과 같다 |
| `python3 $T/rlog_sets.py $W` | Gotcha 5 · F4 6 · 체크리스트 6 · 검사 스크립트 5, `checklist_number=6 want_files_exist=9/9 all_equal=0` | 파일 네 자리를 직접 읽은 값과 같다 |
| `bash $T/validator_neg.sh $W $U` | `caught=5/9` — planning · design · tone · api 를 지워도 PASS | 검사 스크립트 목록 5 개와 같다 |
| `python3 $T/phase17.py $W` | `heading=0 rows=0 urls=0 invented=0 paths=0 missing_paths=0` | 양성 대조: 지어낸 URL 하나 · 없는 경로 하나를 넣은 임시 사본에서 `invented=1 missing_paths=1` |
| `python3 $T/accent.py $W` | `rows=0 pages=7 page_variants=1 match=0`, 쪽 값 `#F59E0B` · `#FBBF24` · `rgba(245,158,11,0.12)` · `rgba(245,158,11,0.06)` | 같은 코드를 API Kit 행 · `docs/api-kit/` 12 쪽에 돌리면 `rows=1 match=1` |
| `bash $T/sync_err.sh $W $U` | `intact=0 no_begin_marker=2 no_marketplace=2` | — |
| `bash $T/regress.sh $W $B $U` | `steps=8 nonzero=0` | — |
| `bash $T/lint_new.sh $W $B $U <markdownlint-cli2> <pyflakes 파이썬>` | `files=0 new_warnings=0` | 양성 대조: 복제본의 `.sh` · `.md` · `.py` 에 경고 한 줄씩 넣고 커밋하면 `files=3 new_warnings=3` |
| `bash $T/scope_diff.sh $W $B $U` | `changed=0 missing=10` | 양성 대조: 복제본에 두 킷 · 영어 제목 커밋을 넣으면 `outside=1 multi_kit=1 no_hangul=1` |

## GAP 분석 — Pre-Edit Audit

| 대상 파일 | 읽은 자리 (`파일:줄`) | 찾은 결함 | 조건 |
| --------- | --------------------- | --------- | ---- |
| `harness/scripts/commit-guard.sh` | `:231-235` | `-a` · 같은 명령 `git add -A`/`.`/`-u` 는 `ls-files --deleted` 를 그대로 더해 옮긴 폴더의 옛 경로를 삭제로 센다 | SC-01 |
| `harness/scripts/commit-guard.sh` | `:118-122` · `:221-230` | `-i` 의 작업 폴더 삭제가 `staged` 로 들어가고 셋째 인자 `extra` 가 비어 「작업 폴더 삭제 포함」 설명이 빠진다 (`bfadfbb` 부터) | ER-01 |
| `harness/scripts/commit-guard.sh` | `:161-171` | 목록 사본에 작업 폴더 상태를 얹는 `overlay_deletes` 가 이미 있다 — 경로 지정 · `-i` 만 쓴다 | RE-02 |
| `harness/evals/hooks/commit-guard-test.sh` | `:142-145` · `:165-184` | ㉒ 는 개수만 보고, 이름 바꾸기 경우는 `-o` · `-i` 뿐이다 | SC-02 |
| `harness/README.md` | `:52` | 「이름 바꾸기는 세지 않는다」 가 `-a` · `add -A` 에서는 지금 거짓이다 — 훅을 고치면 참이 되므로 글은 고칠 필요가 없다 | SC-01 (G1~G4) |
| `scripts/detect-docs-drift.py` | `:33-70` | 원본 여섯(아래 SC-03)의 접두나 개별 지정이 없다. `:47` `planning-kit/references/` 는 디스크에 없는 폴더다 | SC-03 · SK-01 |
| `scripts/detect-docs-drift.py` | `:65` · `:202-204` | `docs/howto/` 접두와 SKILL 이름 규칙이 겹쳐 초안 `docs/howto/drafts/SKILL.md` 를 `drafts.html` 새 페이지로 낸다 | SC-03 |
| `.claude/skills/docs-site/SKILL.md` | `:45` · `:47-63` | 「F2 표와 같다 — 한쪽을 고치면 다른 쪽도 고친다」 두 벌 규칙. 표에 `docs/flutter/` 가 없다 | SK-01 · SK-02 |
| `.claude/skills/kaizen-orchestrator/SKILL.md` | `:609-627` | F2 에 같은 표가 한 벌 더 있다 | SK-01 · SK-02 |
| `.claude/skills/docs-site/references/css-tokens.md` | `:25-41` | accent 표에 Howto Kit 행이 없다 (FN-79) | SK-03 |
| `.claude/skills/kaizen-orchestrator/references/phase-research-templates.md` | `:218-265` | Phase 15 · 16 표 다음이 바로 `## 사용 규칙` — Phase 17 절이 없다 (F1H-76) | SK-04 |
| `.claude/skills/kaizen-orchestrator/SKILL.md` | `:25` | 「Phase 1~16 … (Phase 17 표는 아직 없다 …)」 | SK-04 |
| `.claude/skills/kaizen-orchestrator/SKILL.md` | `:297-312` | Phase 별 참조 매핑이 14 까지 (F1H-77) | SK-05 |
| `scripts/collect-kaizen-data.py` | `:1698-1711` | 데이터 풀 §6 표가 12 까지 — 오케스트레이터보다 둘 더 짧다 | SK-05 |
| `.claude/skills/kaizen-orchestrator/SKILL.md` | `:56` · `:741-750` · `:777` | 킷별 리서치 기록 목록이 세 자리에서 5 · 6 · 6 개로 갈리고 design · tone · api 가 없다 (F1H-92) | SK-06 |
| `scripts/validate-post-kaizen.py` | `:354-374` | 검사 목록 5 개(planning 도 없다). `:373` 은 자리표시 없는 f-string (pyflakes 경고) | SK-06 · SC-06 |
| `scripts/sync-orchestrator.py` | `:74-77` · `:95-106` · `:132-142` | 범위 줄은 `skills/*/SKILL.md` + 참조 폴더 하나 + 리서치 폴더만 낸다. 킷 · 스킬 references 둘 다 있으면 하나만, planning 리서치 폴더 없음, `hooks/` · `docs/` · `agents/` 없음 (C L7) | SC-05 |
| `.claude/skills/kaizen-orchestrator/references/phase-dependencies.md` | `:23-86` | Phase 5~17 목록 — AUTO 범위 줄이 덮지 못하는 경로 8 개 | SC-05 |
| `.claude/skills/kaizen-orchestrator/SKILL.md` | `:197` | 「AUTO 줄은 … `hooks/` · `docs/` · `agents/` 가 빠진다」 — 생성기를 고치면 거짓이 된다 | SC-05 |

설정 대조 (`.harness/project.yaml`):

| 설정 키 | project.yaml 값 | 이 계약에 쓴 값 |
| ------- | --------------- | --------------- |
| `commands.analyze` | `bash -n scripts/release.sh` | `bash -n scripts/release.sh` (DG-01 N/A 사유) |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | `bash scripts/release.sh 2>&1 \|\| true` (DG-03 N/A 사유) |
| `diagnostics.ide_exclude` | `[]` | `[]` — 사용자 전역 규칙대로 맞춤법 검사 항목만 뺀다 |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 같다 |
| `anti_patterns[].id` | AP-01 · AP-02 · AP-03 · AP-04 | AP-03 · AP-04 를 골랐다 (AP-01 버전 표기 · AP-02 force push 는 이번 변경 파일에 걸릴 자리가 없다) |

양면 조건(Step 2.5): 훅 판정 ↔ 훅 시험(SC-01 · SC-02), 낡음 감지 매핑 ↔ 두 스킬 표(SC-03 · SK-01 · SK-02), 생성기 ↔ AUTO 영역과 `:197` 설명(SC-05),
수집기 §6 ↔ 오케스트레이터 표(SK-05), F4 체크리스트 ↔ `validate-post-kaizen.py` 목록(SK-06 · SC-06), 리서치 틀 파일 ↔ 오케스트레이터 `:25` 와 `scripts/spawn-kaizen-phase.sh:149` 의 「Phase N 섹션」 읽기(SK-04 의 제목 꼴).

## Skill

- [ ] SK-01: 원본 → 페이지 매핑 표가 `.claude/skills/docs-site/SKILL.md` Step 1 한 곳에만 있고 `scripts/detect-docs-drift.py` 의 매핑과 쌍 집합이 같다 [exact, enumerated]
      (측정: 대상 `.claude/skills/docs-site/SKILL.md` Step 1 표 · `.claude/skills/kaizen-orchestrator/SKILL.md` F2 · `scripts/detect-docs-drift.py` 의 매핑을 `python3 $T/map_tables.py $W` 로 맞대 출력이
       `.claude/skills/docs-site/SKILL.md: rows=` 값 15 이상 · `script_only=0` · `table_only=0` · `ghost=0`(도우미는 docs-site 파일을 `## Step 1:` 절에서 다음 `## ` 제목 앞까지만 읽는다),
       `.claude/skills/kaizen-orchestrator/SKILL.md: rows=0`(이 파일은 전체를 읽는다), 마지막 줄 `script_ghost=0`.
       쌍은 (원본 경로, 출력 폴더) 이고 개별 지정 원본이 같은 출력 폴더의 접두(끝이 `/`) 안에 들면 덮인 것으로 본다.
       예외: `process (공유)` 행처럼 원본 칸에 역따옴표 경로가 없는 행은 쌍을 만들지 않는다 ·
       매핑 밖으로 뺀 경로(`docs/howto/drafts/`)는 출력 폴더 칸에 `docs/` 로 시작하는 역따옴표 경로를 두지 않는다.
       기준값: 두 파일 `rows=15 script_only=2`, `script_ghost=1`)
- [ ] SK-02: 두 번째 자리는 표 대신 기준 표를 가리키고, 두 벌 규칙 문장이 없어지고, 초안 폴더가 매핑 밖이라고 적힌다 [exact, enumerated]
      (측정 네 줄, 모두 성립해야 PASS —
       (a) `awk '/^### Step F2:/{f=1;next} f&&/^### /{f=0} f' $W/.claude/skills/kaizen-orchestrator/SKILL.md | grep -cF '.claude/skills/docs-site/SKILL.md'` 1 이상 (기준값 0) ·
       (b) `grep -cF '.claude/skills/docs-site/SKILL.md' $W/scripts/detect-docs-drift.py` 1 이상 (기준값 0) ·
       (c) ``grep -cF '표는 `.claude/skills/kaizen-orchestrator/SKILL.md` Step F2 표와 같다 — 한쪽을 고치면 다른 쪽도 고친다' $W/.claude/skills/docs-site/SKILL.md`` 0 (기준값 1) ·
       (d) `awk '/^## Step 1:/{f=1;next} f&&/^## /{f=0} f' $W/.claude/skills/docs-site/SKILL.md | grep -cF 'docs/howto/drafts/'` 1 이상 (기준값 0))
- [ ] SK-03: `css-tokens.md` accent 표에 Howto Kit 행이 하나 있고 네 값이 `docs/howto-kit/` 일곱 쪽이 실제로 쓰는 값과 같다 [exact]
      (측정: `python3 $T/accent.py $W` 가 `rows=1 pages=7 page_variants=1 … match=1`.
       값은 `#F59E0B` · `#FBBF24` · `rgba(245,158,11,0.12)` · `rgba(245,158,11,0.06)` — 쪽의 첫 `:root` 블록과 배경 첫 `radial-gradient` 에서 뽑는다.
       알려진 답: 같은 코드를 API Kit 행 · `docs/api-kit/` 12 쪽에 돌려 `rows=1 match=1` (봉인 전 실측) · 기준값 `rows=0 match=0`)
- [ ] SK-04: 리서치 틀 파일에 `## Phase 17 — howto-kit` 절이 생기고 출처가 howto-kit 이 이미 쓰는 근거 안에서만 나오며, 오케스트레이터의 「표가 아직 없다」 문장이 없어진다 [exact]
      (측정 — (a) `python3 $T/phase17.py $W` 가 `heading=1` · `rows=` 3 이상 · `urls=` 3 이상 · `invented=0` · `missing_paths=0`.
       제목은 `## Phase 17 — howto-kit` 이고 뒤에 괄호 부연(`(howto-kaizen …)` 꼴)을 붙여도 잡힌다 ·
       `invented` 는 절 안 URL 가운데 `docs/howto/*.md` · `howto-kit/references/*.md` 어디에도 글자 그대로 없는 것, `missing_paths` 는 절 안 `/` 가 든 역따옴표 경로 가운데 디스크에 없는 것 ·
       (b) `grep -cF 'Phase 17 표는 아직 없다 — 표가 생길 때까지 Phase 17 은' $W/.claude/skills/kaizen-orchestrator/SKILL.md` 0 (기준값 1) ·
       (c) `grep -cF '**Phase 1~16 각 의무 리서치 소스 테이블**' $W/.claude/skills/kaizen-orchestrator/SKILL.md` 0 (기준값 1).
       양성 대조: 지어낸 URL `https://example.invalid/made-up` 과 없는 경로 `docs/howto/no-such.md` 를 넣은 임시 사본에서 `invented=1 missing_paths=1` (봉인 전 실측))
- [ ] SK-05: 오케스트레이터 「Phase 별 참조 매핑」 표와 수집기가 실제로 낸 데이터 풀 §6 표가 모두 Phase 1~17 을 한 번씩 담고, 13~17 행의 참조 칸이 두 표에서 글자까지 같다 [exact, enumerated]
      (Given: 공통 전제 ·
       When (측정): `bash $T/phase_ref.sh $W` (수집기를 `--skip-validate --output <임시 파일>` 로 실제 실행한다) ·
       Then: `orch_missing=[] pool_missing=[] dup_orch=[] dup_pool=[] ref_13_17_differ=[] ref_13_17_not_s0=[] collector_rc=0`.
       13~17 은 Bambu · Onboarding · Tone · Api · Howto 다섯 행이고 참조 칸은 다른 행처럼 `§0 +` 로 시작한다.
       알려진 답: 기준값 `orch_missing=[15, 16, 17] pool_missing=[13, 14, 15, 16, 17]` 이 두 파일을 직접 읽은 값과 같다)
- [ ] SK-06: 킷별 리서치 기록 파일 목록이 오케스트레이터 Gotcha · F4 3 번 · Post-Kaizen 체크리스트 · `scripts/validate-post-kaizen.py` 네 자리에서 같은 아홉 개다 [exact, enumerated]
      (측정: `python3 $T/rlog_sets.py $W` 의 네 줄이 모두 `n=9 missing_vs_want=[] extra=[]` 이고 마지막 줄이 `want_files_exist=9/9 all_equal=1`,
       `checklist_number=` 가 `9`(개수를 적은 경우) 또는 `-1`(개수를 적지 않은 경우).
       아홉 개는 `docs/backend/research-log.md` · `docs/infra/research-log.md` · `docs/rust/research-log.md` · `docs/react/research-log.md` · `docs/flutter/research-log.md` ·
       `docs/planning/research-log.md` · `docs/design/research-log.md` · `docs/tone/research-log.md` · `docs/api/research-log.md` 다.
       예외: `docs/kaizen/research-log.md` · `docs/kaizen/flutter-research-log.md` 는 킷별 목록이 아니라 따로 적힌 두 줄이라 셈에서 뺀다 ·
       howto-kit 은 `docs/howto/research-log.md` 가 없고 `.claude/skills/howto-research/SKILL.md` 가 그 파일을 쓰지 않아 넣지 않는다.
       알려진 답: 기준값 Gotcha 5 · F4 6 · 체크리스트 6 · 검사 스크립트 5 가 네 자리를 직접 읽은 값과 같다)

## Script

- [ ] SC-01: 옮긴 폴더를 `-a` 나 같은 명령의 `git add -A` · `git add .` · `git add -u` 로 올리는 커밋에서 커밋 안전 훅이 이름 바꾸기를 삭제로 세지 않고, 진짜 삭제는 그대로 막는다 [exact, enumerated]
      (Given: 공통 전제 ·
       When (측정): `bash $T/guard_probe.sh $W/harness/scripts/commit-guard.sh` — 60 개 폴더 `d1` 을 둔 임시 저장소마다 훅 `pre` 를 부른다 ·
       Then: G1~G7 일곱 줄이 모두 `MATCH` 이고 마지막 줄에 `mismatch_sc=0/7`.
       경우 — G1 `mv d1 d2; git add d2` 뒤 `git commit -a -m x` → 종료 0 · 표준 출력 없음 /
       G2 `mv d1 d2` 뒤 `git add -A && git commit -m x` → 0 / G3 `mv d1 d2; git add d2` 뒤 `git add -u && git commit -m x` → 0 /
       G4 `mv d1 d2` 뒤 `git add . && git commit -m x` → 0 /
       G5 `mv d1 d2`(새 경로 안 올림) 뒤 `git commit -am x` → 2 · 표준 오류에 `삭제 60 개` /
       G6 작업 폴더에서 60 개 삭제 뒤 `git commit -a -m x` → 2 · `삭제 60 개` · `작업 폴더 삭제 포함` /
       G7 `d1` 이동 + 따로 커밋한 `d3` 60 개 삭제 뒤 `git add -A && git commit -m x` → 2 · `삭제 60 개`.
       알려진 답: 고치기 전 훅에서 G1 · G2 · G3 · G4 · G7 이 MISMATCH(`mismatch_sc=5/7`, G7 은 `삭제 120 개`), 손으로 돌린 결과와 같다)
- [ ] SC-02: 레포 훅 시험이 SC-01 · ER-01 의 고치기 전 결함 여섯 경우를 저마다 한 줄로 잡고, 지금 훅으로는 전부 통과한다 [goal]
      (측정: `bash $T/guard_test_neg.sh $W $B` 가 `new_fail=0` · `new_rc=0` · `new_pass=` 50 이상 · `old_fail=` 6 이상.
       음성 대조: `old_*` 는 같은 시험을 `$B` 판 훅(`COMMIT_GUARD_HOOK` 로 바꿔 끼움)으로 돌린 값이다 — G1 · G2 · G3 · G4 · G7 · G8 에 해당하는 시험 줄이 저마다 FAIL 해야 6 이상이 된다.
       기준값 `old_fail=0 new_pass=44 new_fail=0`)
- [ ] SC-03: 낡음 감지가 원본 여섯을 제 페이지로 잇고, 초안 파일은 내지 않으며, 원래 잡던 원본은 그대로 잡는다 [exact, enumerated]
      (Given: 공통 전제 ·
       When (측정): `bash $T/drift_e2e.sh $W` — `$W` 복제본에서 원본 여덟 개에 한 줄씩 더해 커밋한 뒤 `detect-docs-drift.py --since HEAD~1 --json` 을 실제로 돌린다 ·
       Then: 마지막 줄 `expected_hit=7/7 unexpected=0` · `rc=0`. 일곱 쌍(대상 글자는 대소문자까지 같고 `registered` · `exists` 가 둘 다 참) —
       `design-kit/references/visual-change-protocol.md` → `docs/design-kit/visual-change-protocol.html` ·
       `design-kit/skills/design-test/SKILL.md` → `docs/design-kit/design-test.html` ·
       `reflect-kit/docs/DESIGN.md` → `docs/reflect-kit/design.html` · `reflect-kit/docs/SCHEMA.md` → `docs/reflect-kit/schema.html` ·
       `reflect-kit/docs/RESEARCH.md` → `docs/reflect-kit/research.html` ·
       `api-kit/skills/api-ui/SKILL.md` → `docs/api-kit/static-evidence-viewer-contract.html` ·
       대조용 `docs/howto/deep-links.md` → `docs/howto-kit/deep-links.html`. 여덟째 원본 `docs/howto/drafts/SKILL.md` 는 줄이 없어야 한다.
       알려진 답: 기준값 `expected_hit=1/7 unexpected=1` — 맞는 것은 대조용 한 줄, 틀린 것은 `drafts.html` 한 줄)
- [ ] SC-04: 매핑을 바꿔도 레포 전체에서 짝 없는 페이지 · 없는 페이지를 가리키는 원본이 새로 생기지 않는다 [exact]
      (측정: `X=$(mktemp -d); git clone -q "$W" "$X/new" && git -C "$X/new" checkout -q "$U" && git clone -q "$W" "$X/base" && git -C "$X/base" checkout -q "$B" && python3 $T/drift_map.py "$X/new" "$X/base"`
       출력이 `added_orphan=0 added_new=0` 이고 첫 줄 `orphan_pages=` 21 이하 · `new_targets=` 43 이하.
       21 은 기준 26 에서 SC-03 의 새 짝 다섯 쪽을 뺀 값(`static-evidence-viewer-contract.html` 은 원래 짝이 있어 빠지지 않는다), 43 은 기준 44 에서 초안 한 줄을 뺀 값이다.
       기준값 `orphan_pages=26 new_targets=44`)
- [ ] SC-05: 오케스트레이터 AUTO 범위 줄이 `phase-dependencies.md` 의 Phase 5~17 목록과 킷에 실제로 있는 참조 · 에이전트 · 훅 · 문서 폴더를 모두 덮고, 그 결과가 생성기에서 나오며, 옛 설명 문장이 없어진다 [exact, enumerated]
      (Given: 공통 전제 ·
       When (측정) · Then 네 줄, 모두 성립해야 PASS —
       (a) `python3 $T/scope_gap.py $W` 마지막 줄 `uncovered=0 phases=13` (기준값 `uncovered=8`) ·
       (b) `python3 $T/scope_folders.py $W` 마지막 줄 `folder_miss=0 ghost=0 kits=13` (기준값 `folder_miss=20`). 폴더는 킷마다 디스크에 있는 `references/` · `skills/*/references/` · `agents/` · `hooks/` · `docs/` 이고, 범위 줄에 그 폴더나 그 안 경로가 있으면 덮인 것으로 본다.
       스킬 references 는 별표를 그대로 둔 `<킷>/skills/*/references/` 한 줄로 적거나, 그 킷의 스킬 references 폴더를 하나도 빼지 않고 구체 경로로 적으면 덮인 것으로 본다 ·
       (c) `cd $W && python3 scripts/sync-orchestrator.py --check-only` 종료 코드 0 — 범위 줄을 손으로 고치면 1 이 되므로 생성기가 낸 결과임을 함께 잰다 ·
       (d) ``grep -cF 'AUTO 줄은 `scripts/sync-orchestrator.py` 가 `skills/` · `references/` 만 보고 만들어 `hooks/` · `docs/` · `agents/` 가 빠진다' $W/.claude/skills/kaizen-orchestrator/SKILL.md`` 0 (기준값 1).
       알려진 답: (a) 기준 8 = P5 1 · P10 1 · P11 2 · P12 2 · P16 1 · P17 1, (b) 기준 20 을 킷마다 손으로 셌다)
- [ ] SC-06: Post-Kaizen 검사가 킷별 리서치 기록 아홉 개를 하나씩 지운 경우를 모두 FAIL 로 잡고, 다 있을 때 PASS 줄이 틀린 개수를 적지 않는다 [exact]
      (Given: 공통 전제 ·
       When (측정): `bash $T/validator_neg.sh $W $U` — `$U` 복제본에서 파일을 하나씩 치우고 `validate-post-kaizen.py --since HEAD` 의 `per-kit-research-logs` 줄을 본다 ·
       Then: `caught=9/9` 이고 `intact:` 줄에 `PASS` 가 있으며 그 줄의 숫자는 9 뿐이다(숫자가 없어도 된다).
       음성 대조: 기준값 `caught=5/9` — planning · design · tone · api 를 지워도 PASS 였다)
- [ ] SC-07: 파일 2000 개 폴더를 옮긴 저장소에서 `-a` · `add -A` 커밋 판정이 통과하면서 2 초 안에 끝난다 [exact]
      (측정: `bash $T/perf.sh $W/harness/scripts/commit-guard.sh 'git commit -a -m x' add` 와
       `bash $T/perf.sh $W/harness/scripts/commit-guard.sh 'git add -A && git commit -m x' noadd` 를 저마다 세 번 돌려 여섯 줄 모두 `rc=0` 이고 `sec=` 2.00 이하(가장 느린 값으로 판정).
       비교 기준: 같은 저장소에서 지금도 목록 사본을 쓰는 경로 지정 커밋 `git commit -o -m x -- d1 d2` 가 `rc=0 sec=0.40` (봉인 전 실측).
       기준값: 고치기 전 두 명령은 `rc=2 sec=0.16` 으로 막혔다)
- [ ] SC-08: 이번 변경 파일을 재는 기존 검사 여덟과 바뀐 셸 · 파이썬 파일의 구문 검사가 모두 종료 코드 0 이다 [exact, enumerated]
      (측정: `bash $T/regress.sh $W $B $U` 마지막 줄 `nonzero=0`. 여덟은 `python3 scripts/validate-plugin.py` · `python3 scripts/sync-evals.py --check-only` ·
       `python3 scripts/sync-docs.py --check-only` · `python3 scripts/run-evals.py` · `python3 scripts/check-stale-values.py` · `python3 scripts/test-collect-kaizen-data.py` ·
       `bash harness/evals/hooks/commit-guard-test.sh` · `python3 scripts/validate-doc-contracts.py` 이고, 바뀐 `.sh` 는 `bash -n`, `.py` 는 `python3 -m py_compile` 로 더 잰다.
       뺀 CI 단계와 이유: `check-docs-a11y.js` · playwright · `check-contrast-claims.py` · `check-docs-links.py` 는 `docs/` HTML 을 재는데 이 스프린트는 `docs/` 를 고치지 않는다 ·
       킷별 훅 · 게이트 시험(react · reflect · onboarding · howto · flutter · design)은 그 킷 폴더를 고치지 않는다 · 피드백 저장 시험 둘은 `harness/scripts/save-feedback.sh` 계열을 고치지 않는다.
       기준값 `steps=8 nonzero=0`, 로컬 CI 스물두 단계 전부 종료 코드 0(`feedback-agg-test` 는 yq 가 없어 SKIP))

## Error

- [ ] ER-01: `-i` 커밋이 작업 폴더 삭제를 더해 막힐 때 막힘 설명 첫 줄에 「작업 폴더 삭제 포함」 이 다시 붙고, 목록 삭제만으로 막힐 때는 붙지 않는다 [exact, enumerated]
      (Given: 공통 전제 ·
       When (측정): `bash $T/guard_probe.sh $W/harness/scripts/commit-guard.sh` 의 G8 · G9 ·
       Then: 두 줄 모두 `MATCH` 이고 마지막 줄에 `mismatch_er=0/2`.
       G8 — `git rm` 10 개 + 작업 폴더 삭제 45 개 뒤 `git commit -i d1 -m x` → 종료 2 · 표준 오류에 `삭제 55 개` 와 `작업 폴더 삭제 포함` /
       G9 — `git rm` 51 개만 뒤 `git commit -i d1 -m x` → 종료 2 · `삭제 51 개` · `작업 폴더 삭제 포함` 없음.
       알려진 답: 고치기 전 훅에서 G8 만 MISMATCH(설명 없음), G9 는 MATCH — `mismatch_er=1/2`)
- [ ] ER-02: 생성기를 고친 뒤에도 `sync-orchestrator.py --check-only` 가 구조 오류에서 종료 코드 2 로 멈춘다 [exact]
      (측정: `bash $T/sync_err.sh $W $U` 가 `intact=0 no_begin_marker=2 no_marketplace=2` — AUTO 시작 표지 한 줄을 지운 복제본과 `.claude-plugin/marketplace.json` 을 치운 복제본에서 잰다.
       기준값 같은 줄(고치기 전에도 이 값이다 — 퇴행을 막는 조건))

## Architecture

- [ ] AR-01: 커밋 구간의 `.harness` 밖 변경이 허용 13 경로 안에만 있고 필수 10 경로를 모두 담으며, 커밋마다 킷 폴더를 하나 이하로 건드리고 제목이 한국어다 [exact, enumerated]
      (Given: 공통 전제 ·
       측정: `bash $T/scope_diff.sh $W $B $U` 마지막 줄 `outside=0 missing=0 multi_kit=0 no_hangul=0`.
       경로 한정은 `git diff --name-only $B $U -- . ':(exclude).harness'`, 생성물은 없다, 판정은 「허용 집합에 포함 · 필수 집합을 모두 포함」, 상한은 `$U`.
       필수 10 — `harness/scripts/commit-guard.sh` · `harness/evals/hooks/commit-guard-test.sh` · `scripts/detect-docs-drift.py` · `scripts/sync-orchestrator.py` ·
       `scripts/collect-kaizen-data.py` · `scripts/validate-post-kaizen.py` · `.claude/skills/kaizen-orchestrator/SKILL.md` ·
       `.claude/skills/kaizen-orchestrator/references/phase-research-templates.md` · `.claude/skills/docs-site/SKILL.md` · `.claude/skills/docs-site/references/css-tokens.md`.
       선택 3 — `harness/README.md` · `.claude/skills/kaizen-orchestrator/references/phase-dependencies.md` · `scripts/test-collect-kaizen-data.py`.
       킷 폴더는 `.claude-plugin/marketplace.json` 의 플러그인 이름과 같은 최상위 폴더다 — `scripts/` · `.claude/` 는 킷 폴더가 아니라 세지 않으므로 필수 경로를 여러 커밋에 나눠 담아도 된다.
       기준값 `changed=0 missing=10`, 양성 대조는 `## 배경 — 측정 도우미` 표)
- [ ] AR-02: `.harness/` 의 계약 파일이 봉인을 깨지 않고, 구현 기록 파일에 넘긴 것과 톤 대조가 남는다 [structural, enumerated]
      (측정 두 줄, 모두 성립해야 PASS —
       (a) `harness/references/contract-schema.md` §`.harness/` 범위 조건 블록(첫 줄 `type verify_seal fm_get contract_digest sha256_16` 확인 포함)을 `$W` 에서 돌려 `SEAL_BROKEN` 0 개 ·
       (b) `$W/.harness/.meta/after-kaizen-0926/c1b-notes.md` 에 `## 넘김` 절과 `## 톤 대조` 절이 있고,
       `## 넘김` 절에 `## 범위 경계` 의 넘김 표시 `N1` · `N2` · `N3` · `N4` · `N5` · `N6` 여섯이 모두 나오며,
       `## 톤 대조` 절에 AR-01 의 `git diff --name-only $B $U -- . ':(exclude).harness'` 가 내는 경로가 하나도 빠짐없이 글자 그대로 나온다.
       측정은 `awk '/^## 넘김/{f=1;next} /^## /{f=0} f'` · `awk '/^## 톤 대조/{f=1;next} /^## /{f=0} f'` 로 절을 잘라 `grep -cF` 로 센다.
       기준값 (a) `SEAL_OK 73 · SEAL_ABSENT 11 · SEAL_BROKEN 0`, (b) 파일 없음.
       양성 대조 (a): 봉인된 계약 `sprint-contract-kaizen-0924-f2-review-fixes.md` 사본의 첫 조건 줄에 글자 하나를 더하면 `1 SEAL_BROKEN` (봉인 전 실측))
- [ ] AR-03: 측정 도우미 17 개가 봉인 때의 내용 그대로다 [exact, enumerated]
      (측정: ``diff <(cd "$T" && find . -maxdepth 1 -type f -exec shasum -a 256 {} + | awk '{sub(/^\.\//,"",$2); print $2" "substr($1,1,16)}' | LC_ALL=C sort) <(grep -E '^[|] `[a-z0-9_]+[.](sh|py)` [|] `[0-9a-f]{16}` [|]$' "$CF" | tr -d '`|' | awk '{print $1" "$2}' | LC_ALL=C sort)`` 가 출력 없이 종료 코드 0.
       대상 17 개는 `## 배경 — 측정 도우미` 표의 파일 열.
       양성 대조: 도우미 사본 `perf.sh` 끝에 한 줄을 더하면 그 파일 한 줄이 다르게 나오고 종료 코드 1 (봉인 전 실측))

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (측정: `cd $W && python3 scripts/validate-plugin.py harness --check=code-fence` 종료 코드 0 · 기준값 0. 킷 밖 `.claude/skills/` 마크다운의 여는 fence 는 DG-02 의 markdownlint MD040 이 잰다)
- [ ] AP-04: SKILL.md frontmatter 에서 name 필드 누락 금지 (측정: 첫 frontmatter 블록만 읽는 `awk 'NR==1 && /^---[[:space:]]*$/ {fm=1; next} fm && /^---[[:space:]]*$/ {exit} fm && /^name:/'` 가 `$W/.claude/skills/kaizen-orchestrator/SKILL.md` 에서 `name: kaizen-orchestrator`, `$W/.claude/skills/docs-site/SKILL.md` 에서 `name: docs-site` 를 낸다 · 기준값 둘 다 있음)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 (측정: `git -C $W diff -U0 $B $U -- '*.py' | grep -cE '^\+def _'` 0 · 기준값 0 · 양성 대조: `printf '+def _x():\n' | grep -cE '^\+def _'` 가 1)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 (측정: `grep -c '^overlay_deletes() {' $W/harness/scripts/commit-guard.sh` 가 1 이고 `grep -cE 'overlay_deletes "' $W/harness/scripts/commit-guard.sh` 가 3 이상 — 목록 사본 방식을 새 함수로 복제하지 않고 `-a` · 같은 명령 `git add` 경로에서도 부른다 · 기준값 정의 1 · 호출 2)

## Diagnostics

- [ ] DG-01: N/A (commands.analyze 는 `bash -n scripts/release.sh` 로 `scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `git -C $W diff --name-only $B $U | grep -cx 'scripts/release.sh'` 가 0. 바뀐 셸 · 파이썬 파일의 구문 검사는 SC-08 이 잰다)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (맞춤법 검사 제외 · `.harness` 밖 변경 파일에서 이번 구간에 더한 줄만 센다 — 계약 · 기록 · 도우미는 뺀다. 측정: `bash $T/lint_new.sh $W $B $U <markdownlint-cli2> <pyflakes 파이썬>` 마지막 줄 `new_warnings=0` — `.sh` 는 shellcheck, `.md` 는 markdownlint-cli2 0.23.2 에 MD013 끔, `.py` 는 pyflakes 4.0.0. 준비: 임시 폴더에서 `npm install --no-save markdownlint-cli2@0.23.2` 와 `python3 -m venv v && v/bin/pip install pyflakes==4.0.0`, `command -v shellcheck` 확인 · 설치가 안 되면 이 세션이 깐 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/c1b/lint/node_modules/.bin/markdownlint-cli2` · `…/c1b/lint/venv/bin/python` 을 쓴다 · 둘 다 없으면 FAIL 이다(`[미검증]` 허용 0 건). 양성 대조: 복제본 세 파일에 경고 한 줄씩 넣으면 `new_warnings=3` (봉인 전 실측))
- [ ] DG-03: N/A (commands.test 는 `bash scripts/release.sh 2>&1 || true` — 릴리스 스크립트라 이번 변경 파일과 교집합 0 개이고 돌리면 실제 릴리스를 시도한다. 측정: DG-01 과 같은 명령이 0. 이번 변경의 시험 실행은 SC-02 · SC-08 이 잰다)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 변경 파일은 셸 훅 · 파이썬 도구 스크립트 · 마크다운이다. 측정: AR-01 의 필수 · 선택 13 경로 확장자가 `.sh` · `.py` · `.md` 뿐. 훅과 스크립트는 SC-01 ~ SC-07 · ER-01 · ER-02 가 실제로 실행한다)

## 범위 경계

- 이 계약이 고치는 것은 과제 다섯 — (1) 커밋 안전 훅 `-a` · 같은 명령 `git add` 의 이동 판정과 `-i` 막힘 설명 (2) 낡음 감지 매핑 여섯 쌍 · 초안 제외 · 매핑 표 한 곳 · Howto Kit accent
  (3) AUTO 범위 줄 생성 (4) Phase 별 참조 표 17 까지 · 킷별 리서치 기록 목록 (5) Phase 17 리서치 틀 — 이다.
- 매핑 표의 기준 자리는 `.claude/skills/docs-site/SKILL.md` Step 1 로 정했다. 근거: 오케스트레이터 F2 가 이미 「docs-site 스킬 Step 1 참조」 로 적고 있고(`:609`), 페이지를 만드는 스킬이 그 표를 읽는다.
  오케스트레이터 F2 는 그 자리를 가리키고, `detect-docs-drift.py` 는 주석으로 그 자리를 가리킨다.
- 원본 여섯 쌍은 f2 계약의 짝(`.harness/sprint-contract-kaizen-0924-f2-review-fixes.md:335-341` 의 DVP↔PVP · DTE↔PDT · RSC↔PRS · RDE↔PRD · AUI↔PAV)에
  `reflect-kit/docs/RESEARCH.md` ↔ `docs/reflect-kit/research.html` 을 더해 실측으로 정했다 — 세 reflect 쪽 제목이 원본 파일 이름과 같고(`<title>Research — Reflect Kit`), `static-evidence-viewer-contract.html` 은 `api-ui/SKILL.md` 를 직접 인용한다.
- 킷별 리서치 기록 목록은 디스크에 있는 아홉 개로 정했다. howto-kit 은 파일이 없고 `howto-research` 가 쓰지 않는다.
- `scripts/validate-post-kaizen.py` 는 과제 문장에 없지만 F4 체크리스트를 기계로 재는 반대편이라 양면 조건(SK-06 · SC-06)으로 넣었다.
- 범위 밖(다른 묶음): `scripts/` 의 `run-evals.py` · `check-insights-tracking.py` · `append-audit-log.py` · `validate-plugin.py` · `sync-docs.py` · `check-stale-values.py` ·
  킷 폴더(harness 제외) · `docs/` HTML 페이지 · 루트 `README.md` · 루트 `CLAUDE.md` · `.claude/skills/tone-kaizen/`.
- 넘김 — 구현 기록 파일 `## 넘김` 절에 같은 표시로 옮긴다.
  - `N1` 짝 원본이 없는 등록 페이지 21 쪽(react-kit 8 · design-kit 6 · backend-kit 2 · infra-kit 2 · flutter-toolkit 1 · harness 1 · howto-kit 1). 쪽마다 원본을 정해야 하고 f2 교차 진단이 짚은 범위 밖이다
  - `N2` 없는 페이지를 가리키는 원본 43 개(리서치 기록 8 · tone-kit references 9 · react-kit `docs/react/kit-design/` 8 과 references 5 · reflect-kit 5 · bambu-kit 3 · harness 2 · flutter 1 · rust 1 · howto `design-brief.md` 1). 원본 ↔ 페이지 이름 규칙을 정하는 일이다
  - `N3` `docs/howto/design-brief.md` ↔ `docs/howto-kit/overview.html` 짝 — overview 가 `howto-kit/README.md` 를 5 회, `design-brief.md` 를 2 회 인용해 원본 하나로 못 정한다
  - `N4` 매핑 표와 스크립트를 상시 맞대는 검사 — 이번에는 이 계약 측정(SK-01)으로 한 번만 잰다. 새 검사를 CI 에 넣는 것은 새 기능이다
  - `N5` `scripts/spawn-kaizen-phase.sh:116-121` 의 Phase 별 데이터 풀 절 배정(5~10 만 §2 · §3) — 과제 목록 밖
  - `N6` howto-kit 리서치 기록 파일 — 만들지 않는다(위 결정). 다음 howto-research 가 기록 파일을 쓰기 시작하면 네 자리 목록에 함께 넣는다
- 오라클 해소: SK-02 — 가리킴 · 두 벌 규칙 문장 · 제외 표기는 문서 구조 자체가 산출물이다. 동작은 SK-01(스크립트 매핑과 표 쌍 대조 실행) · SC-03(낡음 감지 실제 실행)이 잰다
- 오라클 해소: AR-02 — (a) 는 봉인 검사 함수를 실제로 돌리고, (b) 는 구현 기록이라는 기록물 자체가 산출물이다
- 오라클 해소: AR-03 — 도우미 파일을 `shasum` 으로 실제로 계산해 표와 맞댄다. 서술 존재 확인이 아니다
- 커밋 규칙: `git add <경로>` 뒤 `git commit -o <경로>`, 한 커밋에 킷 하나(AR-01), 봉인 커밋은 계약 한 파일, 도우미 17 개는 그다음 커밋. `git add -A` · `git stash` · 푸시 · 가지 바꾸기는 하지 않는다.
