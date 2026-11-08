"""perf-compare 의 perf_compare.py 단위 테스트. 사용: python3 -m unittest discover -s perf-kit/evals/perf-compare -v

PERF_COMPARE_SCRIPT 환경 변수로 대상 스크립트를 바꿀 수 있다 — 계산을 일부러 틀린 사본으로 돌려 테스트가 떨어지는지 볼 때 쓴다.
손으로 셀 수 있는 작은 입력으로 기대값을 고정한다 (skill-design-guide §3.7 알려진 답 대조).
"""
import copy
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[2] / "skills" / "perf-compare"
SCRIPT = Path(os.environ.get("PERF_COMPARE_SCRIPT", SKILL / "scripts" / "perf_compare.py"))
EXAMPLE = Path(__file__).resolve().parent / "example" / "perf.json"

spec = importlib.util.spec_from_file_location("perf_compare", SCRIPT)
pc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pc)


def metric(a, b, **kw):
    m = {"key": "m", "name": "지표", "unit": "ms", "better": "lower", "role": "target", "source": "손", "a": a, "b": b}
    m.update(kw)
    return m


class Quantile(unittest.TestCase):
    def test_median_odd_even(self):
        self.assertEqual(pc.median([3, 1, 2]), 2)
        self.assertEqual(pc.median([4, 1, 3, 2]), 2.5)

    def test_iqr_linear(self):
        # [1,2,3,4]: q1 = 1 + 0.75 = 1.75, q3 = 3 + 0.25 = 3.25
        self.assertAlmostEqual(pc.quantile([4, 3, 2, 1], 0.25), 1.75)
        self.assertAlmostEqual(pc.quantile([4, 3, 2, 1], 0.75), 3.25)


class MannWhitney(unittest.TestCase):
    def test_three_vs_three_separated(self):
        # 완전히 갈린 3:3 은 C(6,3)=20 중 양 끝 2 개 → p = 0.1, 이 표본 수의 최소 p 도 0.1
        u, p, floor = pc.mann_whitney([1, 2, 3], [4, 5, 6])
        self.assertEqual(u, 0)
        self.assertAlmostEqual(p, 0.1)
        self.assertAlmostEqual(floor, 0.1)

    def test_direction_does_not_change_two_sided_p(self):
        _, p1, _ = pc.mann_whitney([1, 2, 3], [4, 5, 6])
        _, p2, _ = pc.mann_whitney([4, 5, 6], [1, 2, 3])
        self.assertAlmostEqual(p1, p2)

    def test_five_vs_five_separated(self):
        # C(10,5)=252 중 2 개 → 2/252
        _, p, _ = pc.mann_whitney([1, 2, 3, 4, 5], [6, 7, 8, 9, 10])
        self.assertAlmostEqual(p, 2 / 252)

    def test_one_swap(self):
        # a=[1,2,4] b=[3,5,6]: U_a = 1 (4>3). |U-4.5| ≥ 3.5 인 조합은 U∈{0,1,8,9} → 각 1 개씩 = 4/20
        u, p, _ = pc.mann_whitney([1, 2, 4], [3, 5, 6])
        self.assertEqual(u, 1)
        self.assertAlmostEqual(p, 4 / 20)

    def test_documented_example(self):
        # SciPy mannwhitneyu 문서 예제: males 대 females 양측 exact → U1 = 17, p = 0.1111…
        # 문서 주소는 references/experiment-design.md §출처 에 있다
        u, p, _ = pc.mann_whitney([19, 22, 16, 29, 24], [20, 11, 17, 12])
        self.assertEqual(u, 17)
        self.assertAlmostEqual(p, 0.1111111111111111)

    def test_ties_use_permutation_of_midranks(self):
        # a=[1,2,2] b=[2,3,4]: 중간 순위 [1,3,3,3,5,6], 순위합 R 이 7 이하이거나 14 이상인 조합이 극단이다.
        # R=7 은 {1,3,3} 세 가지, R=14 는 {3,5,6} 세 가지 → 6/20. 동순위를 무시하면 다른 값이 나온다
        u, p, _ = pc.mann_whitney([1, 2, 2], [2, 3, 4])
        self.assertEqual(u, 1)
        self.assertAlmostEqual(p, 6 / 20)

    def test_ties_with_tiny_side_stay_exact(self):
        # [1,2] 대 [1]×19 — a 가 2 를 가지는 경우는 210 가지 중 20 가지라 p = 가장 작은 p = 20/210
        _, p, p_floor = pc.mann_whitney([1, 2], [1] * 19)
        self.assertAlmostEqual(p, 20 / 210)
        self.assertAlmostEqual(p_floor, 20 / 210)

    def test_ties_all_equal(self):
        _, p, _ = pc.mann_whitney([5, 5, 5], [5, 5, 5])
        self.assertAlmostEqual(p, 1.0)

    def test_large_separated_sample(self):
        a = list(range(0, 15))
        b = list(range(100, 115))
        _, p, floor = pc.mann_whitney(a, b)
        self.assertLess(p, 0.001)
        self.assertLess(floor, 0.001)


class Judge(unittest.TestCase):
    def test_warmup_dropped(self):
        r = pc.judge(metric([9999, 1, 2, 3, 4, 5], [9999, 6, 7, 8, 9, 10], warmup=1), 0.05)
        self.assertEqual(r["a"], [1, 2, 3, 4, 5])
        self.assertEqual(r["median_a"], 3)

    def test_short_sample(self):
        r = pc.judge(metric([10, 11, 12], [1, 2, 3]), 0.05)
        self.assertEqual(r["verdict"], pc.VERDICT_SHORT)

    def test_better_lower(self):
        r = pc.judge(metric([10, 11, 12, 13, 14], [1, 2, 3, 4, 5]), 0.05)
        self.assertEqual(r["verdict"], pc.VERDICT_BETTER)
        self.assertAlmostEqual(r["delta_pct"], (3 - 12) / 12 * 100)

    def test_worse_when_higher_is_better(self):
        r = pc.judge(metric([10, 11, 12, 13, 14], [1, 2, 3, 4, 5], better="higher"), 0.05)
        self.assertEqual(r["verdict"], pc.VERDICT_WORSE)

    def test_small_effect(self):
        r = pc.judge(metric([100, 100.1, 100.2, 100.3, 100.4], [101, 101.1, 101.2, 101.3, 101.4]), 0.05)
        self.assertEqual(r["verdict"], pc.VERDICT_SMALL)

    def test_deterministic_values(self):
        # 결정값이라고 표시한 지표는 표본이 2 개씩이어도 검정 없이 확정 판정한다
        r = pc.judge(metric([500, 500], [100, 100], deterministic=True), 0.05)
        self.assertEqual(r["verdict"], pc.VERDICT_BETTER)
        r = pc.judge(metric([500, 500], [500, 500], deterministic=True), 0.05)
        self.assertEqual(r["verdict"], pc.VERDICT_NONE)

    def test_repeated_values_without_flag_are_tested(self):
        # 표시가 없으면 값이 같아도 검정한다 — [100,100] 대 [90,90] 은 순열 6 가지 중 극단 2 → p = 1/3
        r = pc.judge(metric([100, 100], [90, 90]), 0.05)
        self.assertAlmostEqual(r["p"], 1 / 3)
        self.assertEqual(r["verdict"], pc.VERDICT_SHORT)

    def test_negative_values_keep_direction(self):
        # 중앙값 -10.1 → -20.1 은 낮을수록 좋은 지표에서 개선이다. 변화율은 -10 / 10.1
        a, b = [-10, -10.5, -9.8, -10.2, -10.1], [-20, -20.5, -19.8, -20.2, -20.1]
        r = pc.judge(metric(a, b), 0.05)
        self.assertEqual(r["verdict"], pc.VERDICT_BETTER)
        self.assertAlmostEqual(r["delta_pct"], -10 / 10.1 * 100)
        r = pc.judge(metric(a, [-5, -5.5, -4.8, -5.2, -5.1], better="higher"), 0.05)
        self.assertEqual(r["verdict"], pc.VERDICT_BETTER)

    def test_equal_medians_are_small_even_with_zero_min_effect(self):
        # 분포는 갈려도 중앙값이 5 → 5 면 방향을 정할 수 없다
        a, b = [1] * 6 + [5] * 7, [5] * 7 + [9] * 6
        for better in ("lower", "higher"):
            r = pc.judge(metric(a, b, better=better, min_effect_pct=0), 0.05)
            self.assertLess(r["p"], 0.05)
            self.assertEqual(r["verdict"], pc.VERDICT_SMALL)

    def test_paired_signed_rank(self):
        # 여섯 짝이 모두 정확히 -10% — 부호가 전부 같을 확률은 2 / 2^6 = 0.03125
        a = [100, 1000, 200, 2000, 300, 3000]
        b = [x * 0.9 for x in a]
        r = pc.judge(metric(a, b), 0.05, paired=True)
        self.assertAlmostEqual(r["p"], 2 / 64)
        self.assertAlmostEqual(r["delta_pct"], -10)
        self.assertEqual(r["verdict"], pc.VERDICT_BETTER)
        # 같은 수치를 독립 표본으로 보면 갈리지 않는다
        self.assertEqual(pc.judge(metric(a, b), 0.05)["verdict"], pc.VERDICT_NONE)

    def test_no_difference(self):
        r = pc.judge(metric([1, 3, 5, 7, 9], [2, 4, 6, 8, 10]), 0.05)
        self.assertEqual(r["verdict"], pc.VERDICT_NONE)


class Analyze(unittest.TestCase):
    def setUp(self):
        self.rec = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def test_example_is_valid(self):
        self.assertEqual(pc.check(self.rec), [])

    def test_example_verdicts(self):
        an = pc.analyze(self.rec)
        v = {k: r["verdict"] for k, r in an["results"].items()}
        # 3:3 랜딩은 아무리 갈려도 0.05 를 못 넘는다 — TC-056 의 -23.9% 가 여기에 걸린다
        self.assertEqual(v["landing_ms"], pc.VERDICT_SHORT)
        self.assertEqual(v["burst_ms"], pc.VERDICT_BETTER)
        self.assertEqual(v["landing_bytes"], pc.VERDICT_BETTER)
        self.assertEqual(v["main_ms"], pc.VERDICT_SHORT)
        self.assertEqual(an["invalid"], [])
        # 대조 지표도 3:3 이라 환경 흔들림을 못 본다 — 무효는 아니지만 주의로 드러낸다
        self.assertTrue(any("대조 지표" in c and "표본 부족" in c for c in an["caveats"]))
        self.assertTrue(any("blocked" in c for c in an["caveats"]))
        self.assertFalse(any("한 방향" in c for c in an["caveats"]))

    def test_cost_uses_mean(self):
        # 요청당 사용량 [1,1,100] 의 평균은 34 — 한 달 3 번이면 102. 중앙값(1)으로 치면 3 이 나온다
        rec = copy.deepcopy(self.rec)
        rec["metrics"].append(metric([1, 1, 100], [2, 2, 2], key="u"))
        rec["cost"]["items"] = [{"category": "network", "name": "전송", "metric": "u", "scale": 1, "volume": 3,
                                 "volume_source": "가정 (가정)", "price": 1, "price_source": "예시 (예시 단가)"}]
        c = pc.analyze(rec)["costs"][0]
        self.assertAlmostEqual(c["a"], 102)
        self.assertAlmostEqual(c["b"], 6)

    def test_budget_worst(self):
        # [0,0,0,2,3] 은 중앙값 0 이라 상한 0 을 지키지만, 최악값 3 으로 보면 넘는다
        rec = copy.deepcopy(self.rec)
        rec["metrics"].append(metric([0, 1, 0, 2, 1], [0, 0, 0, 2, 3], key="frozen"))
        rec["budgets"] = [{"metric": "frozen", "max": 0, "why": "멈춤 0"},
                          {"metric": "frozen", "max": 0, "stat": "worst", "why": "멈춤 0"}]
        median_b, worst_b = (b["ok"]["b"] for b in pc.analyze(rec)["budgets"])
        self.assertTrue(median_b)
        self.assertFalse(worst_b)

    def test_controls_are_holm_corrected(self):
        # 대조 지표 둘이 각각 p = 0.0317 — 홀름 보정이면 작은 쪽이 0.0635 라 무효가 아니다. 하나뿐이면 무효
        rec = copy.deepcopy(self.rec)
        ctl = [metric([4, 7, 8, 9, 10], [1, 2, 3, 5, 6], key=k, role="control") for k in ("c1", "c2")]
        rec["metrics"] = [m for m in rec["metrics"] if m["role"] != "control"] + ctl
        an = pc.analyze(rec)
        self.assertAlmostEqual(an["results"]["c1"]["p"], 2 * an["results"]["c1"]["p_raw"])
        self.assertEqual(an["invalid"], [])
        rec["metrics"] = rec["metrics"][:-1]
        self.assertTrue(pc.analyze(rec)["invalid"])

    def test_unchecked_is_not_reported_as_passed(self):
        rec = copy.deepcopy(self.rec)
        rec["equivalence"] = []
        an = pc.analyze(rec)
        self.assertIn("결과 동일성 확인 없음", an["unchecked"])
        self.assertNotIn("통과했다", pc.render(rec, an, "<!-- title --><!-- body -->"))

    def test_cost_known_answer(self):
        # 5,309,776 bytes × 1e-9 × 90,000 × 0.09 = 43.009 USD
        an = pc.analyze(self.rec)
        net = an["costs"][0]
        self.assertAlmostEqual(net["a"], 5309776 * 1e-9 * 90000 * 0.09)
        self.assertAlmostEqual(net["b"], 532775 * 1e-9 * 90000 * 0.09)
        self.assertAlmostEqual(net["a"], 43.0092, places=3)

    def test_budget(self):
        an = pc.analyze(self.rec)
        b = an["budgets"][0]
        self.assertFalse(b["ok"]["a"])  # 1783 > 1500
        self.assertTrue(b["ok"]["b"])   # 1356 ≤ 1500

    def test_trend_is_caveat(self):
        rec = copy.deepcopy(self.rec)
        burst = next(m for m in rec["metrics"] if m["key"] == "burst_ms")
        burst["b"] = [1120, 700, 680, 660, 640, 620]
        cav = pc.analyze(rec)["caveats"]
        self.assertTrue(any("한 방향" in c and "새 서버" in c for c in cav))

    def test_trend_needs_four(self):
        self.assertFalse(pc.is_trending([3, 2, 1]))
        self.assertTrue(pc.is_trending([4, 3, 2, 1]))
        self.assertFalse(pc.is_trending([4, 3, 3, 1]))

    def test_order_caveats(self):
        for order, word in (("interleaved", "주기적"), ("randomized", None), ("duet", None)):
            rec = copy.deepcopy(self.rec)
            rec["order"] = order
            cav = pc.analyze(rec)["caveats"]
            self.assertFalse(any("blocked" in c for c in cav))
            if word:
                self.assertTrue(any(word in c for c in cav))
            else:
                self.assertFalse(any("주기적" in c for c in cav))

    def test_no_control_is_caveat(self):
        rec = copy.deepcopy(self.rec)
        rec["metrics"] = [m for m in rec["metrics"] if m["role"] != "control"]
        self.assertTrue(any("대조 지표가 없다" in c for c in pc.analyze(rec)["caveats"]))

    def test_control_shift_invalidates(self):
        rec = copy.deepcopy(self.rec)
        ctrl = next(m for m in rec["metrics"] if m["role"] == "control")
        ctrl["a"] = [1300, 1002, 990, 1010, 1000, 995]
        ctrl["b"] = [1300, 1402, 1390, 1410, 1400, 1395]
        an = pc.analyze(rec)
        self.assertEqual(len(an["invalid"]), 1)
        self.assertIn("대조 지표", an["invalid"][0])

    def test_equivalence_diff_invalidates(self):
        rec = copy.deepcopy(self.rec)
        rec["equivalence"][0]["same"] = False
        self.assertEqual(len(pc.analyze(rec)["invalid"]), 1)


class Check(unittest.TestCase):
    def setUp(self):
        self.rec = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def errs_after(self, mutate):
        rec = copy.deepcopy(self.rec)
        mutate(rec)
        return pc.check(rec)

    def test_unknown_key(self):
        self.assertTrue(any("모르는 키" in e for e in self.errs_after(lambda r: r.update(foo=1))))

    def test_empty_fixed(self):
        self.assertTrue(self.errs_after(lambda r: r.update(fixed=[])))

    def test_warmup_leaves_one_sample(self):
        def mutate(r):
            r["metrics"][0]["a"] = [1, 2]
        self.assertTrue(any("예열을 뺀 표본" in e for e in self.errs_after(mutate)))

    def test_cost_unknown_metric(self):
        def mutate(r):
            r["cost"]["items"][0]["metric"] = "nope"
        self.assertTrue(any("metrics 에 없는 key" in e for e in self.errs_after(mutate)))

    def test_cost_missing_price_source(self):
        def mutate(r):
            r["cost"]["items"].append(dict(r["cost"]["items"][0]))
            del r["cost"]["items"][1]["price_source"]
        # 둘째 항목만 빠뜨려도 잡혀야 한다 (첫 칸만 읽기 방지)
        self.assertTrue(any("items[1].price_source" in e for e in self.errs_after(mutate)))

    def test_wrong_types_are_errors_not_crashes(self):
        for path, value in ((("metrics", 0, "better"), []), (("metrics", 0, "role"), {}), (("order",), ["randomized"]),
                            (("metrics", 0, "key"), ["x"]), (("cost", "items", 0, "volume_source"), None),
                            (("cost", "items", 0, "price_source"), False)):
            rec = copy.deepcopy(self.rec)
            obj = rec
            for k in path[:-1]:
                obj = obj[k]
            obj[path[-1]] = value
            self.assertTrue(pc.check(rec), path)

    def test_deterministic_flag_needs_constant_values(self):
        rec = copy.deepcopy(self.rec)
        rec["metrics"][2]["b"] = [532775, 532776, 532775]
        self.assertTrue(any("deterministic" in e for e in pc.check(rec)))

    def test_duet_needs_equal_pairs(self):
        rec = copy.deepcopy(self.rec)
        rec["order"] = "duet"
        self.assertEqual(pc.check(rec), [])  # 예시는 지표마다 a · b 수가 같다
        rec["metrics"][1]["b"] = rec["metrics"][1]["b"][:-1]
        self.assertTrue(any("duet" in e for e in pc.check(rec)))

    def test_budget_both_bounds(self):
        def mutate(r):
            r["budgets"][0]["min"] = 1
        self.assertTrue(self.errs_after(mutate))

    def test_last_metric_checked(self):
        def mutate(r):
            r["metrics"][-1]["better"] = "faster"
        self.assertTrue(any("metrics[3].better" in e for e in self.errs_after(mutate)))


class Cli(unittest.TestCase):
    def test_report_writes_html_and_summary(self):
        with tempfile.TemporaryDirectory() as d:
            dst = Path(d) / "perf.json"
            dst.write_text(EXAMPLE.read_text(encoding="utf-8"), encoding="utf-8")
            out = subprocess.run([sys.executable, str(SCRIPT), "report", str(dst)], capture_output=True, text=True)
            self.assertEqual(out.returncode, 0, out.stderr)
            self.assertIn("판정: 유효", out.stdout)
            self.assertIn("지표: burst_ms", out.stdout)
            page = (Path(d) / "perf-report.html").read_text(encoding="utf-8")
            self.assertIn("<svg", page)
            self.assertNotIn("<!-- body -->", page)

    def test_check_fails_with_exit_1(self):
        with tempfile.TemporaryDirectory() as d:
            dst = Path(d) / "perf.json"
            dst.write_text("{}", encoding="utf-8")
            out = subprocess.run([sys.executable, str(SCRIPT), "check", str(dst)], capture_output=True, text=True)
            self.assertEqual(out.returncode, 1)
            self.assertFalse((Path(d) / "perf-report.html").exists())


if __name__ == "__main__":
    unittest.main()
