#!/usr/bin/env python3
"""예시 ui.html 의 엔드포인트 데이터에서 상태 · 실패 표지를 센다 (A15).

쓰임: python3 a15-ep.py <ui.html> [report.md] [evals.json]
엔드포인트 블록(`  '<id>':{` 로 시작하는 줄부터 다음 블록 앞까지)마다 state 와 failMark 를 읽는다.
출력: EP <id> state=<값> failMark=<값|없음> 줄들과
      SUMMARY fail=<state 'fail' 수> hold=<failMark '보류' 수> flaky=<failMark 'flaky' 수> misplaced=<fail 이 아닌데 표지 있음>
report.md 를 주면 「실행 요약」 표의 보류 · flaky 칸, evals.json 을 주면 api-ui 사례의 expect.FAIL 을 함께 찍고
      MATCH report_hold=<> report_flaky=<> expect_fail=<> ok=<0|1>
종료 코드: 0 · 1 (MATCH ok=0 이거나 misplaced>0) · 2 블록을 못 읽음
"""
import json, re, sys

text = open(sys.argv[1], encoding="utf-8").read()
start = text.find("const EP = {")
if start < 0:
    print("STOP const EP 없음")
    sys.exit(2)
body = text[start:text.find("\n};", start)]
parts = re.split(r"\n  '([a-z0-9._-]+)':\{", body)
eps = list(zip(parts[1::2], parts[2::2]))
if not eps:
    print("STOP 엔드포인트 블록 0 개")
    sys.exit(2)
fail = hold = flaky = misplaced = 0
for ep_id, block in eps:
    st = re.search(r"state:'([a-z]+)'", block)
    fm = re.search(r"failMark:\s*(?:'([^']*)'|null)", block)
    state = st.group(1) if st else "?"
    mark = (fm.group(1) if fm and fm.group(1) is not None else None)
    print(f"EP {ep_id} state={state} failMark={mark or '없음'}")
    fail += state == "fail"
    hold += mark == "보류"
    flaky += mark == "flaky"
    misplaced += bool(mark) and state != "fail"
print(f"SUMMARY eps={len(eps)} fail={fail} hold={hold} flaky={flaky} misplaced={misplaced}")
rc = 1 if misplaced else 0
if len(sys.argv) > 3:
    rep = open(sys.argv[2], encoding="utf-8").read().split("\n")
    head = next(i for i, l in enumerate(rep) if l.startswith("| 대상 |"))
    cols = [c.strip() for c in rep[head].strip("|").split("|")]
    vals = [c.strip() for c in rep[head + 2].strip("|").split("|")]
    row = dict(zip(cols, vals))
    ev = json.load(open(sys.argv[3], encoding="utf-8"))
    case = next(c for c in ev["cases"] if c.get("skill") == "api-ui")
    ok = int(row.get("보류") == str(hold) and row.get("flaky") == str(flaky) and case["expect"]["FAIL"] == fail)
    print(f"MATCH report_hold={row.get('보류')} report_flaky={row.get('flaky')} expect_fail={case['expect']['FAIL']} ok={ok}")
    rc = rc or (0 if ok else 1)
sys.exit(rc)
