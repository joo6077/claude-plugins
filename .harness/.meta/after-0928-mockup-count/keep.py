#!/usr/bin/env python3
"""바꾸지 않을 자리 검사 — keep.py <레포 뿌리> <keep-lines.txt>

keep-lines.txt 한 줄: <ID>\t<파일>\t<줄 글자>  (json-id:<n>:<사례 JSON> 이면 evals 사례 전체)
줄마다 뿌리의 그 파일에 같은 글자의 줄이 정확히 1 개 있는지(사례면 같은 JSON 인지) 본다.
줄 모양: KEEP <ID> <파일> ok=<0|1>  · 마지막 줄: KEEP_TOTAL n=<n> ok=<k> missing=<m>
missing=0 이면 종료 코드 0, 아니면 1, 파일을 못 읽으면 2.
"""
import json, os, sys
root, listf = sys.argv[1], sys.argv[2]
ok = miss = 0; err = False
for raw in open(listf, encoding="utf-8").read().split("\n"):
    if not raw:
        continue
    kid, path, text = raw.split("\t", 2)
    p = os.path.join(root, path)
    try:
        body = open(p, encoding="utf-8").read()
    except OSError:
        print(f"KEEP {kid} {path} UNREADABLE"); err = True; continue
    if text.startswith("json-id:"):
        _, n, js = text.split(":", 2)
        d = json.loads(body); ev = d["evals"] if isinstance(d, dict) else d
        hit = [e for e in ev if e.get("id") == int(n)]
        good = int(len(hit) == 1 and json.dumps(hit[0], ensure_ascii=False, sort_keys=True) == js)
        label = f"{path}#id{n}"
    else:
        good = int(body.split("\n").count(text) == 1)
        label = path
    ok += good; miss += 1 - good
    print(f"KEEP {kid} {label} ok={good}")
print(f"KEEP_TOTAL n={ok+miss} ok={ok} missing={miss}")
sys.exit(2 if err else (0 if miss == 0 else 1))
