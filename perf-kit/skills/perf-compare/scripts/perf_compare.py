#!/usr/bin/env python3
"""성능 비교 기록(perf.json)을 검사하고 통계 판정 · 비용 환산 · HTML 보고서를 만든다.

사용:
  python3 perf_compare.py check  <perf.json>
  python3 perf_compare.py report <perf.json>   # 같은 폴더에 perf-report.html 을 쓴다

파이썬 표준 라이브러리만 쓴다. 형식은 references/samples-format.md 가 기준 원본이다.
"""
import html
import json
import math
import sys
from pathlib import Path

CASE_FIELDS = {"id", "title", "question", "meta", "fixed", "order", "alpha", "metrics",
               "equivalence", "budgets", "cost"}
META_FIELDS = {"date", "device", "a", "b"}
SIDE_FIELDS = {"label", "ref"}
METRIC_FIELDS = {"key", "name", "unit", "better", "role", "warmup", "min_effect_pct", "deterministic", "source", "a", "b"}
EQUIV_FIELDS = {"name", "same", "seen"}
BUDGET_FIELDS = {"metric", "max", "min", "stat", "why"}
COST_FIELDS = {"currency", "items"}
COST_ITEM_FIELDS = {"category", "name", "metric", "scale", "volume", "volume_source", "price", "price_source"}

ORDERS = {"randomized", "duet", "interleaved", "blocked"}
BETTER = {"lower", "higher"}
ROLES = {"target", "control"}
BUDGET_STATS = {"median", "worst"}
CATEGORIES = {"network": "네트워크", "server": "서버 자원", "external_api": "외부 API", "device": "기기"}

EXACT_LIMIT = 60  # 검정에 쓰는 표본 수(독립 표본은 두 쪽 합, 짝 비교는 0 이 아닌 짝 수)가 이 수 이하이면 정확 분포를 센다

VERDICT_BETTER = "개선"
VERDICT_WORSE = "악화"
VERDICT_SMALL = "차이 미미"
VERDICT_NONE = "차이 없음"
VERDICT_SHORT = "표본 부족"


# ── 통계 ──────────────────────────────────────────────

def quantile(values, q):
    """선형 보간 분위수(R type 7 · numpy 기본값과 같다)."""
    s = sorted(values)
    pos = (len(s) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)


def median(values):
    return quantile(values, 0.5)


def midranks(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        rank = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = rank
        i = j + 1
    return ranks


def exact_tail(counts, centre, dev_obs):
    """{순위 합 × 2: 경우 수} 분포에서 중심과의 거리가 관측값 이상인 비율과, 낼 수 있는 가장 작은 비율."""
    total = sum(counts.values())
    devs = {s2: abs(s2 / 2 - centre) for s2 in counts}
    extreme = sum(c for s2, c in counts.items() if devs[s2] >= dev_obs - 1e-9)
    top = max(devs.values())
    floor = sum(c for s2, c in counts.items() if devs[s2] >= top - 1e-9)
    return extreme / total, floor / total


def mann_whitney(a, b):
    """양측 Mann-Whitney U. (U_a, p, 이 표본 수로 낼 수 있는 가장 작은 p) 를 돌려준다."""
    na, nb = len(a), len(b)
    pooled = list(a) + list(b)
    ranks = midranks(pooled)
    base = na * (na + 1) / 2
    u_obs = sum(ranks[:na]) - base
    mu = na * nb / 2
    dev_obs = abs(u_obs - mu)
    n = na + nb
    if n <= EXACT_LIMIT:
        # 중간 순위를 두 배 해 정수로 만들고, na 개를 고르는 경우의 순위 합 분포를 차례로 쌓는다 — 동순위가 있어도 정확하다
        ways = [dict() for _ in range(na + 1)]
        ways[0][0] = 1
        for i, r in enumerate(ranks):
            r2 = round(r * 2)
            for k in range(min(i + 1, na), 0, -1):
                row = ways[k]
                for s2, c in ways[k - 1].items():
                    row[s2 + r2] = row.get(s2 + r2, 0) + c
        p, p_floor = exact_tail(ways[na], base + mu, dev_obs)
        return u_obs, p, p_floor
    ties = {}
    for v in pooled:
        ties[v] = ties.get(v, 0) + 1
    tie_term = sum(t ** 3 - t for t in ties.values()) / (n * (n - 1))
    var = na * nb / 12 * ((n + 1) - tie_term)
    if var == 0:
        return u_obs, 1.0, 1.0
    z = (dev_obs - 0.5) / math.sqrt(var)
    p = math.erfc(max(z, 0) / math.sqrt(2))
    s = sorted(ranks)
    dev_top = max(abs(sum(s[-na:]) - base - mu), abs(sum(s[:na]) - base - mu))
    z_floor = (dev_top - 0.5) / math.sqrt(var)
    return u_obs, min(p, 1.0), min(math.erfc(max(z_floor, 0) / math.sqrt(2)), 1.0)


def signed_rank(a, b):
    """짝지은 표본의 양측 Wilcoxon 부호 순위 검정. 차이가 0 인 짝은 뺀다. (p, 가장 작은 p) 를 돌려준다."""
    diffs = [y - x for x, y in zip(a, b) if y != x]
    n = len(diffs)
    if n == 0:
        return 1.0, 0.0
    ranks = midranks([abs(d) for d in diffs])
    t_obs = sum(r for r, d in zip(ranks, diffs) if d > 0)
    centre = sum(ranks) / 2
    dev_obs = abs(t_obs - centre)
    if n <= EXACT_LIMIT:
        # 짝마다 부호가 + 이거나 - 인 2^n 가지에서 + 순위 합 분포를 쌓는다
        counts = {0: 1}
        for r in ranks:
            r2 = round(r * 2)
            nxt = dict(counts)
            for s2, c in counts.items():
                nxt[s2 + r2] = nxt.get(s2 + r2, 0) + c
            counts = nxt
        return exact_tail(counts, centre, dev_obs)
    ties = {}
    for v in (abs(d) for d in diffs):
        ties[v] = ties.get(v, 0) + 1
    var = n * (n + 1) * (2 * n + 1) / 24 - sum(t ** 3 - t for t in ties.values()) / 48
    if var == 0:
        return 1.0, 1.0
    # SciPy wilcoxon 의 기본값처럼 연속성 보정을 하지 않는다
    p = math.erfc(dev_obs / math.sqrt(var) / math.sqrt(2))
    return min(p, 1.0), min(math.erfc(centre / math.sqrt(var) / math.sqrt(2)), 1.0)


def is_trending(values):
    """예열을 뺀 표본이 4 개 이상이고 모두 같은 방향으로 바뀌면 정상 상태 전으로 본다."""
    if len(values) < 4:
        return False
    steps = [b - a for a, b in zip(values, values[1:])]
    return all(d > 0 for d in steps) or all(d < 0 for d in steps)


def measure(metric, paired):
    """판정에 쓸 수치를 모은다. 변화율은 A 의 크기(절댓값)로 나눠 음수 값에서도 방향이 뒤집히지 않는다."""
    w = metric.get("warmup", 0)
    a = metric["a"][w:]
    b = metric["b"][w:]
    ma, mb = median(a), median(b)
    if paired:
        # 짝마다 변화율을 내고 그 중앙값을 쓴다 — 두 버전을 함께 돌린 duet 은 짝끼리의 비율만 믿을 수 있다
        delta = median([(y - x) / abs(x) * 100 for x, y in zip(a, b)])
    else:
        delta = (mb - ma) / abs(ma) * 100 if ma else math.inf
    if metric.get("deterministic"):
        # 전송 bytes · 쿼리 수처럼 매번 같은 값이 나온다고 기록에 표시한 지표 — 검정 없이 차이가 확정된다
        p, p_floor = (1.0, 0.0) if ma == mb else (0.0, 0.0)
    elif paired:
        p, p_floor = signed_rank(a, b)
    else:
        _, p, p_floor = mann_whitney(a, b)
    return {
        "a": a, "b": b, "median_a": ma, "median_b": mb,
        "mean_a": sum(a) / len(a), "mean_b": sum(b) / len(b),
        "iqr_a": quantile(a, 0.75) - quantile(a, 0.25),
        "iqr_b": quantile(b, 0.75) - quantile(b, 0.25),
        "delta_pct": delta, "p": p, "p_floor": p_floor,
    }


def decide(metric, r, alpha):
    min_effect = metric.get("min_effect_pct", 5)
    delta = r["delta_pct"]
    if r["p_floor"] >= alpha:
        return VERDICT_SHORT
    if r["p"] >= alpha:
        return VERDICT_NONE
    if delta == 0 or abs(delta) < min_effect:
        return VERDICT_SMALL
    improved = (delta < 0) == (metric["better"] == "lower")
    return VERDICT_BETTER if improved else VERDICT_WORSE


def judge(metric, alpha, paired=False):
    r = measure(metric, paired)
    r["verdict"] = decide(metric, r, alpha)
    return r


def holm(ps):
    """홀름 보정한 p 목록 (입력 순서 그대로)."""
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    out = [0.0] * len(ps)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(ps) - rank) * ps[i]))
        out[i] = running
    return out


def monthly_cost(item, mean):
    """한 달 총비용은 모든 요청의 합이라 평균 × 횟수다 — 중앙값을 쓰면 가끔 튀는 요청이 빠진다."""
    return mean * item["scale"] * item["volume"] * item["price"]


# ── 검사 ──────────────────────────────────────────────

def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def check(rec):
    errs = []

    def need(obj, fields, required, where, strings=()):
        """모르는 키 · 빠진 키를 잡는다. strings 의 키는 비지 않은 문자열이어야 한다."""
        if not isinstance(obj, dict):
            errs.append(f"{where}: 객체여야 한다")
            return False
        for k in obj:
            if k not in fields:
                errs.append(f"{where}.{k}: 모르는 키")
        for k in required:
            if k not in obj:
                errs.append(f"{where}.{k}: 필수 키 누락")
            elif k in strings and not isinstance(obj[k], str):
                errs.append(f"{where}.{k}: 문자열이어야 한다")
            elif isinstance(obj[k], str) and not obj[k].strip():
                errs.append(f"{where}.{k}: 빈 문자열")
        return True

    def one_of(v, allowed):
        return isinstance(v, str) and v in allowed

    if not need(rec, CASE_FIELDS, ["id", "title", "question", "meta", "fixed", "order", "metrics"], "기록",
                strings=("id", "title", "question")):
        return errs
    if need(rec.get("meta"), META_FIELDS, ["date", "device", "a", "b"], "meta", strings=("date", "device")):
        for side in ("a", "b"):
            if side in rec["meta"]:
                need(rec["meta"][side], SIDE_FIELDS, ["label", "ref"], f"meta.{side}", strings=("label", "ref"))
    fixed = rec.get("fixed")
    if not isinstance(fixed, list) or not fixed or not all(isinstance(x, str) and x.strip() for x in fixed):
        errs.append("fixed: 고정한 조건을 문자열 목록으로 하나 이상 적는다")
    if not one_of(rec.get("order"), ORDERS):
        errs.append(f"order: {sorted(ORDERS)} 중 하나")
    paired = rec.get("order") == "duet"
    alpha = rec.get("alpha", 0.05)
    if not is_num(alpha) or not 0 < alpha < 1:
        errs.append("alpha: 0 과 1 사이 숫자")

    keys = set()
    metrics = rec.get("metrics")
    if not isinstance(metrics, list) or not metrics:
        errs.append("metrics: 지표를 하나 이상 적는다")
        metrics = []
    for i, m in enumerate(metrics):
        where = f"metrics[{i}]"
        if not need(m, METRIC_FIELDS, ["key", "name", "unit", "better", "role", "source", "a", "b"], where,
                    strings=("key", "name", "unit", "source")):
            continue
        key = m.get("key")
        if isinstance(key, str):
            if key in keys:
                errs.append(f"{where}.key: '{key}' 가 겹친다")
            keys.add(key)
        if not one_of(m.get("better"), BETTER):
            errs.append(f"{where}.better: lower · higher 중 하나")
        if not one_of(m.get("role"), ROLES):
            errs.append(f"{where}.role: target · control 중 하나")
        warmup = m.get("warmup", 0)
        if not isinstance(warmup, int) or isinstance(warmup, bool) or warmup < 0:
            errs.append(f"{where}.warmup: 0 이상 정수")
            warmup = 0
        if "min_effect_pct" in m and (not is_num(m["min_effect_pct"]) or m["min_effect_pct"] < 0):
            errs.append(f"{where}.min_effect_pct: 0 이상 숫자")
        if "deterministic" in m and not isinstance(m["deterministic"], bool):
            errs.append(f"{where}.deterministic: true · false")
        sides_ok = True
        for side in ("a", "b"):
            vals = m.get(side)
            if not isinstance(vals, list) or not all(is_num(v) for v in vals or []):
                errs.append(f"{where}.{side}: 숫자 목록이어야 한다")
                sides_ok = False
            elif len(vals) - warmup < 2:
                errs.append(f"{where}.{side}: 예열을 뺀 표본이 2 개 이상이어야 한다 (지금 {len(vals) - warmup})")
                sides_ok = False
        if not sides_ok:
            continue
        a, b = m["a"][warmup:], m["b"][warmup:]
        if m.get("deterministic") is True:
            for side, vals in (("a", a), ("b", b)):
                if max(vals) != min(vals):
                    errs.append(f"{where}.{side}: deterministic 인데 값이 한 가지가 아니다 — 표시를 빼고 검정을 받는다")
        if paired:
            if len(a) != len(b):
                errs.append(f"{where}: duet 은 짝을 지어 비교하므로 예열을 뺀 a · b 표본 수가 같아야 한다 ({len(a)} · {len(b)})")
            elif any(x == 0 for x in a):
                errs.append(f"{where}.a: duet 짝 변화율을 내려면 a 에 0 이 없어야 한다")
        elif median(a) == 0:
            errs.append(f"{where}.a: 중앙값이 0 이라 변화율을 낼 수 없다")

    for i, e in enumerate(rec.get("equivalence", []) or []):
        if need(e, EQUIV_FIELDS, ["name", "same", "seen"], f"equivalence[{i}]", strings=("name", "seen")) \
                and not isinstance(e.get("same"), bool):
            errs.append(f"equivalence[{i}].same: true · false")

    for i, b in enumerate(rec.get("budgets", []) or []):
        where = f"budgets[{i}]"
        if not need(b, BUDGET_FIELDS, ["metric", "why"], where, strings=("metric", "why")):
            continue
        if not one_of(b.get("metric"), keys):
            errs.append(f"{where}.metric: metrics 에 없는 key '{b.get('metric')}'")
        bounds = [k for k in ("max", "min") if k in b]
        if len(bounds) != 1 or not is_num(b[bounds[0]] if bounds else None):
            errs.append(f"{where}: max · min 중 하나만 숫자로 적는다")
        if "stat" in b and not one_of(b["stat"], BUDGET_STATS):
            errs.append(f"{where}.stat: median · worst 중 하나")

    cost = rec.get("cost")
    if cost is not None and need(cost, COST_FIELDS, ["currency", "items"], "cost", strings=("currency",)):
        items = cost.get("items")
        if not isinstance(items, list) or not items:
            errs.append("cost.items: 항목을 하나 이상 적는다")
            items = []
        for i, it in enumerate(items):
            where = f"cost.items[{i}]"
            if not need(it, COST_ITEM_FIELDS, sorted(COST_ITEM_FIELDS), where,
                        strings=("category", "name", "metric", "volume_source", "price_source")):
                continue
            if not one_of(it.get("category"), CATEGORIES):
                errs.append(f"{where}.category: {sorted(CATEGORIES)} 중 하나")
            if not one_of(it.get("metric"), keys):
                errs.append(f"{where}.metric: metrics 에 없는 key '{it.get('metric')}'")
            for k in ("scale", "volume", "price"):
                if k in it and (not is_num(it[k]) or it[k] < 0):
                    errs.append(f"{where}.{k}: 0 이상 숫자")
    return errs


# ── 분석 ──────────────────────────────────────────────

def analyze(rec):
    alpha = rec.get("alpha", 0.05)
    paired = rec["order"] == "duet"
    results = {m["key"]: measure(m, paired) for m in rec["metrics"]}
    controls = [m for m in rec["metrics"] if m["role"] == "control"]
    if len(controls) > 1:
        # 대조 지표 하나라도 움직이면 비교 전체가 무효라 여러 번 검정한 셈이다 — 대조 지표끼리 홀름 보정한다
        for m, p_adj in zip(controls, holm([results[m["key"]]["p"] for m in controls])):
            results[m["key"]]["p_raw"] = results[m["key"]]["p"]
            results[m["key"]]["p"] = p_adj
    for m in rec["metrics"]:
        results[m["key"]]["verdict"] = decide(m, results[m["key"]], alpha)
    reasons = []
    caveats = []
    unchecked = []
    if not controls:
        caveats.append("대조 지표가 없다 — 환경이 흔들렸는지 볼 수 없다")
        unchecked.append("대조 지표 없음")
    if not rec.get("equivalence"):
        caveats.append("결과 동일성을 확인하지 않았다 — 빨라진 대신 결과가 달라졌는지 모른다")
        unchecked.append("결과 동일성 확인 없음")
    if rec["order"] == "blocked":
        caveats.append("한쪽씩 몰아 쟀다(blocked) — 시간에 따른 환경 변화가 차이에 섞일 수 있다")
    elif rec["order"] == "interleaved":
        caveats.append("A·B 를 같은 순서로 번갈아 쟀다(interleaved) — 주기적인 간섭이 한쪽에만 겹칠 수 있다")
    for m in rec["metrics"]:
        r = results[m["key"]]
        if m["role"] == "control" and r["verdict"] in (VERDICT_BETTER, VERDICT_WORSE):
            reasons.append(f"대조 지표 '{m['name']}' 가 {r['verdict']} — 바꾼 변수 밖에서 환경이 흔들렸다")
        for side in ("a", "b"):
            if is_trending(r[side]):
                caveats.append(f"'{m['name']}' {rec['meta'][side]['label']} 표본이 예열 뒤에도 한 방향으로만 움직인다"
                               " — 정상 상태에 이르지 않았을 수 있다")
        if m["role"] == "control" and r["verdict"] == VERDICT_SHORT:
            caveats.append(f"대조 지표 '{m['name']}' 가 표본 부족 — 환경 흔들림을 판정하지 못했다")
    for e in rec.get("equivalence", []) or []:
        if not e["same"]:
            reasons.append(f"동일성 '{e['name']}' 이 다르다 — 결과가 바뀐 비교다")
    budgets = []
    for b in rec.get("budgets", []) or []:
        r = results[b["metric"]]
        bound = "max" if "max" in b else "min"
        limit = b[bound]
        stat = b.get("stat", "median")
        # worst 는 한 번이라도 넘으면 안 되는 예산이다 — 상한이면 가장 큰 값, 하한이면 가장 작은 값으로 본다
        pick = (max if bound == "max" else min) if stat == "worst" else median
        seen = {side: pick(r[side]) for side in ("a", "b")}
        ok = {side: (seen[side] <= limit if bound == "max" else seen[side] >= limit) for side in ("a", "b")}
        budgets.append({**b, "bound": bound, "limit": limit, "stat": stat, "seen": seen, "ok": ok})
    costs = []
    cost = rec.get("cost")
    if cost:
        for it in cost["items"]:
            r = results[it["metric"]]
            ca = monthly_cost(it, r["mean_a"])
            cb = monthly_cost(it, r["mean_b"])
            costs.append({**it, "a": ca, "b": cb, "delta": cb - ca})
    return {"alpha": alpha, "results": results, "invalid": reasons, "caveats": caveats,
            "unchecked": unchecked, "budgets": budgets, "costs": costs}


# ── 보고서 ─────────────────────────────────────────────

def fmt(v):
    if not is_num(v):
        return "—"
    if abs(v) >= 1000:
        return f"{v:,.0f}"
    if abs(v) >= 10:
        return f"{v:,.1f}".rstrip("0").rstrip(".")
    return f"{v:,.3f}".rstrip("0").rstrip(".")


def fmt_money(v):
    return f"{v:,.2f}"


def esc(s):
    return html.escape(str(s))


VERDICT_CLASS = {VERDICT_BETTER: "good", VERDICT_WORSE: "bad", VERDICT_SMALL: "muted",
                 VERDICT_NONE: "muted", VERDICT_SHORT: "warn"}


def strip_svg(metric, r, labels):
    """두 줄 점 그림. 점마다 값을 title 로 달고, 중앙값에 세로 막대를 둔다."""
    vals = r["a"] + r["b"]
    lo, hi = min(vals), max(vals)
    if lo == hi:
        lo, hi = lo - 1, hi + 1
    pad = (hi - lo) * 0.08
    lo, hi = lo - pad, hi + pad
    width, left, right = 420, 76, 12

    def x(v):
        return left + (v - lo) / (hi - lo) * (width - left - right)

    rows = []
    for idx, (side, cls) in enumerate((("a", "s1"), ("b", "s2"))):
        y = 20 + idx * 30
        rows.append(f'<text class="axis" x="0" y="{y + 5}">{esc(labels[side])}</text>')
        rows.append(f'<line class="grid" x1="{left}" x2="{width - right}" y1="{y}" y2="{y}"/>')
        for v in r[side]:
            rows.append(f'<circle class="{cls}" cx="{x(v):.1f}" cy="{y}" r="5">'
                        f'<title>{esc(labels[side])} {fmt(v)} {esc(metric["unit"])}</title></circle>')
        med = r[f"median_{side}"]
        rows.append(f'<line class="med {cls}" x1="{x(med):.1f}" x2="{x(med):.1f}" y1="{y - 10}" y2="{y + 10}">'
                    f'<title>중앙값 {fmt(med)} {esc(metric["unit"])}</title></line>')
    rows.append(f'<text class="axis" x="{left}" y="90">{fmt(lo + pad)}</text>')
    rows.append(f'<text class="axis" x="{width - right}" y="90" text-anchor="end">{fmt(hi - pad)} {esc(metric["unit"])}</text>')
    return (f'<svg viewBox="0 0 {width} 96" role="img" aria-label="{esc(metric["name"])} 표본 분포">'
            + "".join(rows) + "</svg>")


def render(rec, an, template):
    meta = rec["meta"]
    labels = {"a": meta["a"]["label"], "b": meta["b"]["label"]}
    parts = []
    if an["invalid"]:
        parts.append('<section class="banner bad"><strong>비교 무효</strong><ul>'
                     + "".join(f"<li>{esc(x)}</li>" for x in an["invalid"]) + "</ul></section>")
    elif an["unchecked"]:
        parts.append('<section class="banner warn"><strong>비교 유효 · 일부 확인 안 함</strong> — '
                     + " · ".join(esc(x) for x in an["unchecked"]) + "</section>")
    else:
        parts.append('<section class="banner good"><strong>비교 유효</strong> — 대조 지표와 동일성 확인을 통과했다</section>')
    if an["caveats"]:
        parts.append('<ul class="note">' + "".join(f"<li>주의: {esc(x)}</li>" for x in an["caveats"]) + "</ul>")

    parts.append('<h2>지표</h2><table><thead><tr><th>지표</th><th>역할</th>'
                 f'<th>{esc(labels["a"])} 중앙값 (IQR)</th><th>{esc(labels["b"])} 중앙값 (IQR)</th>'
                 '<th>변화</th><th>p</th><th>판정</th></tr></thead><tbody>')
    for m in rec["metrics"]:
        r = an["results"][m["key"]]
        role = "목표" if m["role"] == "target" else "대조"
        p_text = fmt(r["p"]) + (f' <span class="muted">(최소 {fmt(r["p_floor"])})</span>' if r["verdict"] == VERDICT_SHORT else "")
        if "p_raw" in r:
            p_text += f' <span class="muted">(보정 전 {fmt(r["p_raw"])})</span>'
        parts.append(
            f'<tr><td>{esc(m["name"])}<div class="muted">{esc(m["source"])}</div></td><td class="num">{role}</td>'
            f'<td class="num">{fmt(r["median_a"])} {esc(m["unit"])} ({fmt(r["iqr_a"])}) · n={len(r["a"])}</td>'
            f'<td class="num">{fmt(r["median_b"])} {esc(m["unit"])} ({fmt(r["iqr_b"])}) · n={len(r["b"])}</td>'
            f'<td class="num">{r["delta_pct"]:+.1f}%</td><td class="num">{p_text}</td>'
            f'<td><span class="tag {VERDICT_CLASS[r["verdict"]]}">{r["verdict"]}</span></td></tr>')
    parts.append("</tbody></table>")
    parts.append(f'<p class="legend"><span class="key s1"></span>{esc(labels["a"])} '
                 f'<span class="key s2"></span>{esc(labels["b"])} · 세로 막대는 중앙값, 예열 표본은 뺐다</p>')
    parts.append('<div class="strips">')
    for m in rec["metrics"]:
        parts.append(f'<figure><figcaption>{esc(m["name"])}</figcaption>{strip_svg(m, an["results"][m["key"]], labels)}</figure>')
    parts.append("</div>")

    if an["costs"]:
        cur = esc(rec["cost"]["currency"])
        parts.append(f'<h2>월 비용 환산 ({cur}) · 요청당 평균 기준</h2><table><thead><tr><th>분류</th><th>항목</th>'
                     f'<th>{esc(labels["a"])}</th><th>{esc(labels["b"])}</th><th>차이</th><th>근거</th></tr></thead><tbody>')
        total_a = total_b = 0.0
        for c in an["costs"]:
            total_a += c["a"]
            total_b += c["b"]
            parts.append(
                f'<tr><td>{CATEGORIES[c["category"]]}</td><td>{esc(c["name"])}</td>'
                f'<td class="num">{fmt_money(c["a"])}</td><td class="num">{fmt_money(c["b"])}</td>'
                f'<td class="num">{c["delta"]:+,.2f}</td>'
                f'<td class="muted">양 {esc(c["volume_source"])} · 단가 {esc(c["price_source"])}</td></tr>')
        parts.append(f'<tr class="total"><td colspan="2">합계</td><td class="num">{fmt_money(total_a)}</td>'
                     f'<td class="num">{fmt_money(total_b)}</td><td class="num">{total_b - total_a:+,.2f}</td><td></td></tr>')
        parts.append("</tbody></table>")

    if an["budgets"]:
        parts.append('<h2>예산</h2><table><thead><tr><th>지표</th><th>기준</th>'
                     f'<th>{esc(labels["a"])}</th><th>{esc(labels["b"])}</th><th>이유</th></tr></thead><tbody>')
        names = {m["key"]: m for m in rec["metrics"]}
        for b in an["budgets"]:
            m = names[b["metric"]]
            sign = "≤" if b["bound"] == "max" else "≥"
            basis = "최악값" if b["stat"] == "worst" else "중앙값"
            cells = "".join(
                f'<td><span class="tag {"good" if b["ok"][s] else "bad"}">{"지킴" if b["ok"][s] else "넘음"}</span></td>'
                for s in ("a", "b"))
            parts.append(f'<tr><td>{esc(m["name"])}</td><td class="num">{basis} {sign} {fmt(b["limit"])} {esc(m["unit"])}</td>'
                         f'{cells}<td class="muted">{esc(b["why"])}</td></tr>')
        parts.append("</tbody></table>")

    if rec.get("equivalence"):
        parts.append("<h2>결과 동일성</h2><table><tbody>")
        for e in rec["equivalence"]:
            parts.append(f'<tr><td>{esc(e["name"])}</td><td><span class="tag {"good" if e["same"] else "bad"}">'
                         f'{"같음" if e["same"] else "다름"}</span></td><td class="muted">{esc(e["seen"])}</td></tr>')
        parts.append("</tbody></table>")

    parts.append("<h2>고정한 조건</h2><ul>" + "".join(f"<li>{esc(x)}</li>" for x in rec["fixed"]) + "</ul>")
    test = "짝지은 표본의 양측 Wilcoxon 부호 순위 검정" if rec["order"] == "duet" else "양측 Mann-Whitney U"
    parts.append(f'<p class="muted">판정: {test}, 유의수준 {fmt(an["alpha"])}. 대조 지표가 둘 이상이면 홀름 보정한 p 로 판정한다. '
                 '표본 부족은 이 표본 수로 낼 수 있는 가장 작은 p 가 유의수준 이상이라는 뜻이다.</p>')

    head = (f'<header><p class="muted">{esc(rec["id"])} · {esc(meta["date"])} · {esc(meta["device"])}</p>'
            f'<h1>{esc(rec["title"])}</h1><p>{esc(rec["question"])}</p>'
            f'<p class="muted">{esc(labels["a"])} = {esc(meta["a"]["ref"])} · {esc(labels["b"])} = {esc(meta["b"]["ref"])}</p></header>')
    return (template.replace("<!-- title -->", esc(rec["title"]))
            .replace("<!-- body -->", head + "\n".join(parts)))


def summary_lines(rec, an, out):
    lines = [f"보고서: {out}", f"판정: {'무효 — ' + '; '.join(an['invalid']) if an['invalid'] else '유효'}"]
    lines += [f"주의: {x}" for x in an["caveats"]]
    for m in rec["metrics"]:
        r = an["results"][m["key"]]
        lines.append(f"지표: {m['key']} {fmt(r['median_a'])} → {fmt(r['median_b'])} {m['unit']} "
                     f"({r['delta_pct']:+.1f}%, p={fmt(r['p'])}) {r['verdict']}")
    for c in an["costs"]:
        lines.append(f"비용: {c['name']} {fmt_money(c['a'])} → {fmt_money(c['b'])} {rec['cost']['currency']}/월")
    for b in an["budgets"]:
        lines.append(f"예산: {b['metric']} {'지킴' if b['ok']['b'] else '넘음'}")
    return lines


def main(argv):
    if len(argv) != 3 or argv[1] not in ("check", "report"):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    path = Path(argv[2])
    try:
        rec = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"오류: {path}: {e}", file=sys.stderr)
        return 1
    errs = check(rec)
    for e in errs:
        print(f"오류: {path.name}: {e}", file=sys.stderr)
    if errs:
        return 1
    if argv[1] == "check":
        print(f"검사 통과: 지표 {len(rec['metrics'])}개")
        return 0
    an = analyze(rec)
    template = (Path(__file__).resolve().parent.parent / "templates" / "perf-report.html").read_text(encoding="utf-8")
    out = path.parent / "perf-report.html"
    out.write_text(render(rec, an, template), encoding="utf-8")
    print("\n".join(summary_lines(rec, an, out)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
