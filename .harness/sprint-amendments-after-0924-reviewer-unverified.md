---
slug: after-0924-reviewer-unverified
created: "2026-09-26 17:36"
---

# after-0924-reviewer-unverified 개정

계약 본문은 봉인돼 있다(`conditions_digest: sha256:3da851e5d1e58f0e`). 조건 줄도 산문도 고치지 않았다. 아래 개정은 QA 1 회차가 짚은
차단 결함 하나(design-audit 리포트 틀이 새 판정 BLOCKED 를 못 담는다)를 고치면서 생긴 것이고, 「이 조건을 이렇게 읽어라」 를 덧붙일 뿐이다.
방향은 자기신고가 아니라 `harness/references/contract-schema.md` §Amendment 사이드카의 헬퍼로 계산했다.

## AM-01 — relaxing · anchored

- 대상 조건: AR-01 (그리고 `## 범위 경계` 의 sprint-scope 블록 · `m.sh` 의 `SCOPE`)
- 변경: 고치는 파일 집합에 `design-kit/skills/design-audit/templates/audit-report.md` 한 경로를 더해 읽는다(16 경로 → 17 경로).
  새 파일은 여전히 `scripts/check-reviewer-protocol-copies.py` 하나다(이 경로는 원래 있던 파일이다)
- 근거(결함): `design-kit/skills/design-audit/SKILL.md` Step 5 가 이 묶음에서 BLOCKED(`insufficient_verified_coverage`)를 낼 수 있게 됐는데,
  Step 4(`:96`)는 결과를 반드시 `templates/audit-report.md` 틀에 맞춰 쓰라고 한다. 그 틀의 판정 칸이 `{{APPROVE|REJECT}}` 둘뿐이고
  미검증 절에 ENV · INVALID 구분과 두 셈을 적을 자리가 없었다. react 쪽은 같은 결함을 `react-audit/SKILL.md` 에서 고쳤지만 design 쪽 틀은
  계약 작성 때 받아 쓰는 쪽 목록에서 빠졌다. QA 가 「고치는 범위 … 계약 개정이 필요하다」 고 적었다
- direction 산출(`amend_direction`, 허용 집합 헬퍼 — 입력은 고쳐도 되는 경로 집합):
  `relaxing added=1 removed=0` · 더한 원소 `design-kit/skills/design-audit/templates/audit-report.md`
- consent: 사용자 위임 「다음 세션에서 직접할 일을 다 실행하고 이어질것도 실행해」 — 앵커 2026-09-26T01:04:21.505Z ·
  session=de8c7935-a5b6-4df5-9106-fafa73c288a0 · cwd=/Users/jackson/Hub/10_Dev/claude-plugins (세션 기록 `type=user` 줄에서 직접 뽑음).
  이 계약의 Step 5 승인과 같은 근거이고, 이 개정만을 두고 따로 받은 동의는 아니다. 이 개정이 담긴 구현 커밋 `578e119` 보다 앞선다
- 개정 뒤 AR-01 을 읽는 법: 봉인된 `m AR-01` 은 `SCOPE` 가 16 경로라 `impl_files=17 exact=0` 을 낸다. 나머지 값
  (`mixed_commits=0 seal_commit_files=1 seal_before_impl=1 seals=187 seal_broken=0 this=SEAL_OK scope_block=1`)은 조건 그대로 본다.
  `exact` 대신 아래 명령이 `impl_vs_amended: same` 을 내고, 봉인 집합과의 차이가 위 한 경로뿐이어야 한다

```bash
# bash 로 돌린다. W 는 워크트리, CF 는 이 계약
W=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c4b
CF=$W/.harness/sprint-contract-after-0924-reviewer-unverified.md
T=$(mktemp -d)
awk '/^## /{s=($(0) ~ /^## 범위 경계/)} s && /^```text$/{b=1; first=1; next} b && /^```$/{b=0; take=0; next}
     b && first {first=0; take=($(0)=="# sprint-scope"); next} b && take {print}' "$CF" | grep -v '^\.harness/$' | grep . > "$T/orig"
{ cat "$T/orig"; echo design-kit/skills/design-audit/templates/audit-report.md; } | LC_ALL=C sort > "$T/amended"
git -C "$W" log --first-parent --no-merges --format= --name-only f81568d8fbf58382172281388ec5d7756f9f46b2..chore/ak-c4b -- . ':(exclude).harness' \
  | grep . | LC_ALL=C sort -u > "$T/impl"
echo "orig=$(grep -c . "$T/orig") amended=$(grep -c . "$T/amended") impl=$(grep -c . "$T/impl")"
echo "impl_vs_amended: $(cmp -s "$T/impl" "$T/amended" && echo same || echo differ)"
comm -3 "$T/impl" <(LC_ALL=C sort "$T/orig")   # 기대: 위 한 경로만
```

  실측(2026-09-26, 끝 판 `c7f13f0`): `orig=16 amended=17 impl=17` · `impl_vs_amended: same` · 차이 한 줄 `design-kit/skills/design-audit/templates/audit-report.md`

## AM-02 — narrowing · anchored

- 대상 조건: SK-07
- 변경: 조건 끝 「react-audit 리포트 틀의 판정 칸이 `BLOCKED` 를 받아야 S3 칸이 맞는다」 를 design-audit 리포트 틀
  (`design-kit/skills/design-audit/templates/audit-report.md`)에도 똑같이 읽는다. QA 는 design-audit 의 S3 칸을 채울 때 그 틀의 판정 칸이
  `BLOCKED` 를 받는지(`:6`)와 미검증 절이 `invalid_evidence` · `env_gaps` · `verified_coverage` 와 `[미검증:ENV]` · `[미검증:INVALID]` 구분을
  적을 자리를 가졌는지도 본다
- direction: 통과 조건이 하나 늘 뿐 줄지 않는다 → PASS 집합이 줄어든다 → `narrowing`
- consent: AM-01 과 같은 앵커

## AM-03 — narrowing · anchored

- 대상 조건: DG-02
- 변경: 마크다운 열셋(`m.sh` 의 `MDF`)에 더해 AM-01 의 틀 파일도 같은 조건(markdownlint-cli2 0.23.2 · MD013 끔)으로 시작 판과 끝 판에서 재어,
  규칙마다 끝 판 경고 수가 시작 판 이하여야 한다. `m DG-02` 의 기대 값은 그대로다
- direction: 재는 파일이 늘고 빠지는 것은 없다 — `amend_direction_oracle` 기준 `measured_removed=0 measured_added=1` → `narrowing`
- consent: AM-01 과 같은 앵커
- 실측(2026-09-26): 틀 파일 시작 판 `MD024 3 · MD060 12` → 끝 판 `MD024 2 · MD060 12`. 늘어난 규칙 0
  (줄인 1 건은 미검증 절 제목이 다른 절 제목과 달라져서다)

## 계약 개정이 필요 없는 함께 고친 것

- QA 비차단 2(planning 에서 FAIL 이 있어도 비율 보류 BLOCKED 가 이기는 순서 문제) — `planning-kit/agents/planning-reviewer.md` 와
  `planning-kit/skills/plan-audit/SKILL.md` 의 비율 보류 항을 「FAIL 0 일 때만」 으로 좁혔다(커밋 `c7f13f0`). 두 파일 모두 원래 범위 안이라
  경로 집합은 그대로이고, 판정 대응표 S1 ~ S4 는 모두 FAIL 0 이라 기대 값이 바뀌지 않는다

## 다시 잰 값 (끝 판 `c7f13f0`, 봉인된 세 블록 그대로)

`SK-01 files=7 a1=7 b1=7 prov1=7 base_a1=0 base_b1=0 guide=[a=1 b=1]` · `SK-02 rust-kit=0/1 backend-kit=0/1 infra-kit=0/1` ·
`SK-03 old_thr=0 num_ref=0 num3_ref=0 three_way=0 gate_ok=7 env_ok=7 invalid_ok=7 base_old_thr=20 base_num_ref=9 base_num3_ref=6 base_three_way=7 base_gate_ok=3` ·
`SK-04 reason_lines=1 reason_na=1 base_reason_na=0` · `SK-05 … labels_ok=7/7` · `SK-06 old_thr=0 num_ref=0 three_way=0 skills_with_gate=6/6 infra_audit=same api_skills_citing_reviewer=0` ·
`SK-07 … labels_ok=6/6` · `SK-08 rows=1 req4=1 script=1` · `SK-09 added_lines=132 g1_hits=0 canon_g1=1` · `SC-00 release_paths=0` ·
`ER-01 end_rc=0 end_ok=7 end_excluded=1 end_stderr_bytes=0 base_rc=1 base_mismatch=7 mut_rc=1 mut_mismatch=1 mut_react=1 mut_ok=6` ·
`ER-02 guide_rc=2 del_mut_applied=1 del_rc=2 del_missing=1 del_mismatch=1 extra_rc=1 extra_unlisted=1 cwd_root_rc=0 cwd_root_ok=7` ·
`AR-01 impl_files=17 exact=0 mixed_commits=0 seal_commit_files=1 seal_before_impl=1 seals=187 seal_broken=0 this=SEAL_OK scope_block=1`(AM-01 로 읽음) ·
`AR-02 in_validate=1 in_file=1 actionlint_end=0 base_in_file=0 actionlint_base=0` · `AP-03` 일곱 모두 0 · `AP-04 files=12 name=12 fm_same=12` ·
`RE-01 added=1 script=1` · `RE-02 plugin_utils=1 guide_path=2 canon_text=0` · `DG-01 release_sh=0` ·
`DG-02 md=13 base_warn=204 end_warn=203 worse=0 py_compile=0 json=0` · `DG-04 rc=0 stderr_bytes=0 traceback=0` · `DG-05` 시작 판 · 끝 판 모두 0(`copies=absent` / `copies=0`)

## 사용자 동의 — AM-01 (2026-09-26 18:03 KST)

- 부모 교차 진단이 AM-01 을 조건을 느슨하게 하는 개정(AR-01)으로 계산했고, 동의 근거가 일반 위임뿐이라 판정을 뒤집었다(contract-schema.md 「완화의 승인 주체는 사용자뿐」).
- 사용자에게 이 개정만 콕 집어 물었고 「승인」 을 받았다: AskUserQuestion 답 `2026-09-26T09:03:30.690Z`, 세션 기록 `/Users/jackson/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72.jsonl`, 작업 폴더 `/Users/jackson/Hub/10_Dev/claude-plugins`.
- 이 줄은 답보다 뒤에 커밋한다. 조건 줄 · 측정은 바꾸지 않는다 — AR-01 의 판정은 이 동의로 성립한다.
