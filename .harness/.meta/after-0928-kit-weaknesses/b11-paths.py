#!/usr/bin/env python3
"""B11 대상 파일이 가리키는 레포 전용 docs/ 경로가 그 판에 실제로 있는지 본다 (raw 주소가 404 가 아니려면).

쓰임: python3 b11-paths.py <레포 뿌리> <판> <파일 목록>
파일마다 b11-docs-guidance.py 와 같은 규칙으로 레포 전용 경로 낱말을 뽑아 (../ 는 풀어서)
`git ls-tree -r --name-only <판>` 의 파일이거나 폴더 앞머리인지 본다. 끝의 `.` 은 문장 끝으로 보고 뗀다.
출력: MISSING <파일> <경로> 줄들과 끝 줄 PATHS files=<n> paths=<검사한 경로 수> missing=<없는 수>
종료 코드: 0 없는 경로 0 · 1 있음 · 2 판을 못 읽음
"""
import os, re, subprocess, sys

root, ref, listfile = sys.argv[1], sys.argv[2], sys.argv[3]
os.chdir(root)
try:
    tree = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", ref], text=True).splitlines()
except Exception:
    print(f"STOP 판 {ref} 을 못 읽음")
    sys.exit(2)
files_set = set(tree)
folders = set()
for p in tree:
    d = os.path.dirname(p)
    while d:
        folders.add(d)
        d = os.path.dirname(d)
TOKEN = re.compile(r"(?<![A-Za-z0-9_./-])((?:\.\./)*docs/[A-Za-z0-9_-]+(?:/[A-Za-z0-9_.-]*)*)")
targets = [l.strip() for l in open(listfile, encoding="utf-8") if l.strip()]
n = missing = 0
for f in targets:
    kit = f.split("/")[0]
    text = subprocess.check_output(["git", "show", f"{ref}:{f}"], text=True)
    for m in TOKEN.finditer(text):
        p = m.group(1)
        full = os.path.normpath(os.path.join(os.path.dirname(f), p)) if p.startswith("../") else p
        if not full.startswith("docs/"):
            continue
        seg = full.split("/")[1]
        if os.path.join(kit, "docs", seg) in folders or seg not in {x.split("/")[1] for x in folders if x.startswith("docs/") and x.count("/") >= 1}:
            continue
        full = full.rstrip(".").rstrip("/")
        n += 1
        if full not in files_set and full not in folders:
            missing += 1
            print(f"MISSING {f} {full}")
print(f"PATHS files={len(targets)} paths={n} missing={missing}")
sys.exit(1 if missing else 0)
