#!/usr/bin/env python3
"""성능 비교 기록(perf.json)을 검사하고 통계 판정 · 비용 환산 · HTML 보고서를 만든다.

사용:
  python3 perf_compare.py check  <perf.json>
  python3 perf_compare.py report <perf.json>   # 같은 폴더에 perf-report.html 을 쓴다

파이썬 표준 라이브러리만 쓴다. 형식은 references/samples-format.md 가 기준 원본이다.
"""
import html
import itertools
import json
import math
import sys
from pathlib import Path

CASE_FIELDS = {"id", "title", "question", "meta", "fixed", "order", "alpha", "metrics",
               "equivalence", "budgets", "cost"}
META_FIELDS = {"date", "device", "a", "b"}
SIDE_FIELDS = {"label", "ref"}
METRIC_FIELDS = {"key", "name", "unit", "better", "role", "warmup", "min_effect_pct", "source", "a", "b"}
EQUIV_FIELDS = {"name", "same", "seen"}
BUDGET_FIELDS = {"metric", "max", "min", "why"}
COST_FIELDS = {"currency", "items"}
COST_ITEM_FIELDS = {"category", "name", "metric", "scale", "volume", "volume_source", "price", "price_source"}

ORDERS = {"randomized", "duet", "interleaved", "blocked"}
BETTER = {"lower", "higher"}
ROLES = {"target", "control"}
CATEGORIES = {"network": "네트워크", "server": "서버 자원", "external_api": "외부 API", "device": "기기"}

EXACT_LIMIT = 20  # 두 쪽 표본 합이 이 수 이하이면 순열을 전부 센다

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
        total = 0
        extreme = 0
        devs = []
        for combo in itertools.combinations(range(n), na):
            dev = abs(sum(ranks[i] for i in combo) - base - mu)
            devs.append(dev)
            total += 1
            if dev >= dev_obs - 1e-9:
                extreme += 1
        top = max(devs)
        p_floor = sum(1 for d in devs if d >= top - 1e-9) / total
        return u_obs, extreme / total, p_floor
    ties = {}
    for v in pooled:
        ties[v] = ties.get(v, 0) + 1
    tie_term = sum(t ** 3 - t for t in ties.values()) / (n * (n - 1))
    var = na * nb / 12 * ((n + 1) - tie_term)
    if var == 0:
        return u_obs, 1.0, 1.0
    z = (dev_obs - 0.5) / math.sqrt(var)
    p = math.erfc(max(z, 0) / math.sqrt(2))
    z_floor = (mu - 0.5) / math.sqrt(var)
    return u_obs, min(p, 1.0), math.erfc(z_floor / math.sqrt(2))


def is_trending(values):
    """예열을 뺀 표본이 4 개 이상이고 모두 같은 방향으로 바뀌면 정상 상태 전으로 본다."""
    if len(values) < 4:
        return False
    steps = [b - a for a, b in zip(values, values[1:])]
    return all(d > 0 for d in steps) or all(d < 0 for d in steps)


def judge(metric, alpha):
    w = metric.get("warmup", 0)
    a = metric["a"][w:]
    b = metric["b"][w:]
    ma, mb = median(a), median(b)
    delta = (mb - ma) / ma * 100 if ma else math.inf
    if max(a) == min(a) and max(b) == min(b):
        # 전송 bytes · 쿼리 수처럼 매번 같은 값이 나오는 결정값 — 검정 없이 차이가 확정된다
        p, p_floor = (1.0, 0.0) if ma == mb else (0.0, 0.0)
    else:
        _, p, p_floor = mann_whitney(a, b)
    min_effect = metric.get("min_effect_pct", 5)
    if p_floor >= alpha:
        verdict = VERDICT_SHORT
    elif p >= alpha:
        verdict = VERDICT_NONE
    elif abs(delta) < min_effect:
        verdict = VERDICT_SMALL
    else:
        improved = (delta < 0) == (metric["better"] == "lower")
        verdict = VERDICT_BETTER if improved else VERDICT_WORSE
    return {
        "a": a, "b": b, "median_a": ma, "median_b": mb,
        "iqr_a": quantile(a, 0.75) - quantile(a, 0.25),
        "iqr_b": quantile(b, 0.75) - quantile(b, 0.25),
        "delta_pct": delta, "p": p, "p_floor": p_floor, "verdict": verdict,
    }


def monthly_cost(item, med):
    return med * item["scale"] * item["volume"] * item["price"]


# ── 검사 ──────────────────────────────────────────────

def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def check(rec):
    errs = []

    def need(obj, fields, required, where):
        if not isinstance(obj, dict):
            errs.append(f"{where}: 객체여야 한다")
            return False
        for k in obj:
            if k not in fields:
                errs.append(f"{where}.{k}: 모르는 키")
        for k in required:
            if k not in obj:
                errs.append(f"{where}.{k}: 필수 키 누락")
            elif isinstance(obj[k], str) and not obj[k].strip():
                errs.append(f"{where}.{k}: 빈 문자열")
        return True

    if not need(rec, CASE_FIELDS, ["id", "title", "question", "meta", "fixed", "order", "metrics"], "기록"):
        return errs
    if need(rec.get("meta"), META_FIELDS, ["date", "device", "a", "b"], "meta"):
        for side in ("a", "b"):
            if side in rec["meta"]:
                need(rec["meta"][side], SIDE_FIELDS, ["label", "ref"], f"meta.{side}")
    fixed = rec.get("fixed")
    if not isinstance(fixed, list) or not fixed or not all(isinstance(x, str) and x.strip() for x in fixed):
        errs.append("fixed: 고정한 조건을 문자열 목록으로 하나 이상 적는다")
    if rec.get("order") not in ORDERS:
        errs.append(f"order: {sorted(ORDERS)} 중 하나")
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
        if not need(m, METRIC_FIELDS, ["key", "name", "unit", "better", "role", "source", "a", "b"], where):
            continue
        key = m.get("key")
        if key in keys:
            errs.append(f"{where}.key: '{key}' 가 겹친다")
        keys.add(key)
        if m.get("better") not in BETTER:
            errs.append(f"{where}.better: lower · higher 중 하나")
        if m.get("role") not in ROLES:
            errs.append(f"{where}.role: target · control 중 하나")
        warmup = m.get("warmup", 0)
        if not isinstance(warmup, int) or isinstance(warmup, bool) or warmup < 0:
            errs.append(f"{where}.warmup: 0 이상 정수")
            warmup = 0
        if "min_effect_pct" in m and (not is_num(m["min_effect_pct"]) or m["min_effect_pct"] < 0):
            errs.append(f"{where}.min_effect_pct: 0 이상 숫자")
        for side in ("a", "b"):
            vals = m.get(side)
            if not isinstance(vals, list) or not all(is_num(v) for v in vals or []):
                errs.append(f"{where}.{side}: 숫자 목록이어야 한다")
            elif len(vals) - warmup < 2:
                errs.append(f"{where}.{side}: 예열을 뺀 표본이 2 개 이상이어야 한다 (지금 {len(vals) - warmup})")
        if m.get("better") in BETTER and isinstance(m.get("a"), list) and m["a"][warmup:] \
                and all(is_num(v) for v in m["a"]) and median(m["a"][warmup:]) == 0:
            errs.append(f"{where}.a: 중앙값이 0 이라 변화율을 낼 수 없다")

    for i, e in enumerate(rec.get("equivalence", []) or []):
        if need(e, EQUIV_FIELDS, ["name", "same", "seen"], f"equivalence[{i}]") and not isinstance(e.get("same"), bool):
            errs.append(f"equivalence[{i}].same: true · false")

    for i, b in enumerate(rec.get("budgets", []) or []):
        where = f"budgets[{i}]"
        if not need(b, BUDGET_FIELDS, ["metric", "why"], where):
            continue
        if b.get("metric") not in keys:
            errs.append(f"{where}.metric: metrics 에 없는 key '{b.get('metric')}'")
        bounds = [k for k in ("max", "min") if k in b]
        if len(bounds) != 1 or not is_num(b[bounds[0]] if bounds else None):
            errs.append(f"{where}: max · min 중 하나만 숫자로 적는다")

    cost = rec.get("cost")
    if cost is not None and need(cost, COST_FIELDS, ["currency", "items"], "cost"):
        items = cost.get("items")
        if not isinstance(items, list) or not items:
            errs.append("cost.items: 항목을 하나 이상 적는다")
            items = []
        for i, it in enumerate(items):
            where = f"cost.items[{i}]"
            if not need(it, COST_ITEM_FIELDS, sorted(COST_ITEM_FIELDS), where):
                continue
            if it.get("category") not in CATEGORIES:
                errs.append(f"{where}.category: {sorted(CATEGORIES)} 중 하나")
            if it.get("metric") not in keys:
                errs.append(f"{where}.metric: metrics 에 없는 key '{it.get('metric')}'")
            for k in ("scale", "volume", "price"):
                if k in it and (not is_num(it[k]) or it[k] < 0):
                    errs.append(f"{where}.{k}: 0 이상 숫자")
    return errs


# ── 분석 ──────────────────────────────────────────────

def analyze(rec):
    alpha = rec.get("alpha", 0.05)
    results = {m["key"]: judge(m, alpha) for m in rec["metrics"]}
    reasons = []
    caveats = []
    if not any(m["role"] == "control" for m in rec["metrics"]):
        caveats.append("대조 지표가 없다 — 환경이 흔들렸는지 볼 수 없다")
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
        ok = {side: (r[f"median_{side}"] <= limit if bound == "max" else r[f"median_{side}"] >= limit)
              for side in ("a", "b")}
        budgets.append({**b, "bound": bound, "limit": limit, "ok": ok})
    costs = []
    cost = rec.get("cost")
    if cost:
        for it in cost["items"]:
            r = results[it["metric"]]
            ca = monthly_cost(it, r["median_a"])
            cb = monthly_cost(it, r["median_b"])
            costs.append({**it, "a": ca, "b": cb, "delta": cb - ca})
    return {"alpha": alpha, "results": results, "invalid": reasons, "caveats": caveats,
            "budgets": budgets, "costs": costs}


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
        parts.append(f'<h2>월 비용 환산 ({cur})</h2><table><thead><tr><th>분류</th><th>항목</th>'
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
            cells = "".join(
                f'<td><span class="tag {"good" if b["ok"][s] else "bad"}">{"지킴" if b["ok"][s] else "넘음"}</span></td>'
                for s in ("a", "b"))
            parts.append(f'<tr><td>{esc(m["name"])}</td><td class="num">{sign} {fmt(b["limit"])} {esc(m["unit"])}</td>'
                         f'{cells}<td class="muted">{esc(b["why"])}</td></tr>')
        parts.append("</tbody></table>")

    if rec.get("equivalence"):
        parts.append("<h2>결과 동일성</h2><table><tbody>")
        for e in rec["equivalence"]:
            parts.append(f'<tr><td>{esc(e["name"])}</td><td><span class="tag {"good" if e["same"] else "bad"}">'
                         f'{"같음" if e["same"] else "다름"}</span></td><td class="muted">{esc(e["seen"])}</td></tr>')
        parts.append("</tbody></table>")

    parts.append("<h2>고정한 조건</h2><ul>" + "".join(f"<li>{esc(x)}</li>" for x in rec["fixed"]) + "</ul>")
    parts.append(f'<p class="muted">판정: 양측 Mann-Whitney U, 유의수준 {fmt(an["alpha"])}. '
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
