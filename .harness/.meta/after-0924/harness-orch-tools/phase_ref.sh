#!/usr/bin/env bash
# 오케스트레이터 「Phase 별 참조 매핑」 표와 수집기가 실제로 낸 데이터 풀 §6 표의 Phase 번호 집합 · 13~17 행 참조 칸을 잰다.
# 사용: phase_ref.sh <레포 루트>
root=${1:?}; t=$(mktemp -d "${TMPDIR:-/tmp}/phase-ref.XXXXXX"); trap 'rm -rf "$t"' EXIT
( cd "$root" && python3 scripts/collect-kaizen-data.py --skip-validate --output "$t/pool.md" >/dev/null 2>"$t/err" ); rc=$?
python3 - "$root/.claude/skills/kaizen-orchestrator/SKILL.md" "$t/pool.md" "$rc" <<'PY'
import re, sys
orch = open(sys.argv[1], encoding="utf-8").read()
orch_tbl = orch.split("**Phase 별 참조 매핑**", 1)[1].split("**각 Phase 서브에이전트 프롬프트", 1)[0]
pool = open(sys.argv[2], encoding="utf-8").read()
pool_tbl = pool.split("## 6. Phase 별 참조 가이드", 1)[1]
def rows(tbl):
    out = {}
    for line in tbl.splitlines():
        m = re.match(r"^\|\s*(\d+)\s[^|]*\|(.*)\|\s*$", line)
        if m:
            n = int(m.group(1)); cells = [c.strip() for c in m.group(2).split("|")]
            out.setdefault(n, []).append(cells[-1])
    return out
o, p = rows(orch_tbl), rows(pool_tbl)
want = set(range(1, 18))
dup_o = sorted(n for n, v in o.items() if len(v) > 1); dup_p = sorted(n for n, v in p.items() if len(v) > 1)
miss_o = sorted(want - set(o)); miss_p = sorted(want - set(p))
diff = sorted(n for n in range(13, 18) if n in o and n in p and o[n][0] != p[n][0])
print(f"orch={sorted(o)} pool={sorted(p)}")
not_s0 = sorted({n for tbl in (o, p) for n in range(13, 18) if n in tbl and not tbl[n][0].startswith("§0 +")})
print(f"orch_missing={miss_o} pool_missing={miss_p} dup_orch={dup_o} dup_pool={dup_p} ref_13_17_differ={diff} ref_13_17_not_s0={not_s0} collector_rc={sys.argv[3]}")
PY
