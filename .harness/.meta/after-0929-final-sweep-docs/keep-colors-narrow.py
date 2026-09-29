"""개정 AM-01 — 구조-03 을 두 쪽에 한해 좁혀 잰다. 레포 맨 위 폴더에서 `python3 <이 파일>` 로 부른다.

- 두 쪽(NARROWED)을 뺀 시작 판 쪽은 measure.py 의 구조-03 과 같은 지문 비교(changed=0).
- 두 쪽은 요소마다 [태그 · 글자] 로 시작 판과 짝을 맞춘다. 시작 판 요소는 모두 짝이 있어야 하고(removed=0),
  짝지은 요소의 글자색 · 배경색과 body 색이 시작 판과 같아야 한다(color_diff=0). 짝이 없는 새 판 요소가 새로 더한 요소다.
- `--head-root <폴더>` 는 새 판 쪽을 다른 폴더에서 읽는다(음성 대조용). `--only-narrowed` 는 두 쪽만 잰다.
종료 코드 0 성립 · 1 불성립 · 2 잴 수 없음.
"""
import difflib
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("measure", os.path.join(HERE, "measure.py"))
measure = importlib.util.module_from_spec(spec)
spec.loader.exec_module(measure)

NARROWED = ["docs/index.html", "docs/bambu-kit/bambu-print-profile.html"]
ROWS_JS = os.path.join(HERE, "br-rows.js")


def read_rows(theme, pages, root):
    result = subprocess.run(["node", ROWS_JS, theme, *[os.path.join(root, page) for page in pages]],
                            capture_output=True, text=True)
    by_page = {}
    for line in result.stdout.splitlines():
        record = json.loads(line)
        by_page[os.path.relpath(record["file"], root)] = record
    return result.returncode, by_page


def fingerprint(record):
    """br.js paint 와 같은 식 — 두 도구가 같은 요소를 읽는지 대조한다."""
    lines = record["body"] + [f"{tag}|{color}|{background}" for tag, color, background, _ in record["rows"]]
    return hashlib.sha256("\n".join(lines).encode()).hexdigest()[:16]


def compare(base, head):
    """시작 판 요소마다 새 판에서 [태그 · 글자] 짝을 찾는다. 글자만 바뀐 같은 자리 · 같은 태그 요소도 짝으로 본다."""
    base_keys = [(tag, words) for tag, _, _, words in base["rows"]]
    head_keys = [(tag, words) for tag, _, _, words in head["rows"]]
    pairs, removed, added, edited = [], 0, 0, 0
    matcher = difflib.SequenceMatcher(None, base_keys, head_keys, autojunk=False)
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == "equal":
            pairs += list(zip(range(i1, i2), range(j1, j2)))
        elif op == "insert":
            added += j2 - j1
        elif op == "delete":
            removed += i2 - i1
        elif [key[0] for key in base_keys[i1:i2]] == [key[0] for key in head_keys[j1:j2]]:
            pairs += list(zip(range(i1, i2), range(j1, j2)))
            edited += i2 - i1
        else:
            removed += i2 - i1
            added += j2 - j1
    diffs = [(i, j) for i, j in pairs if base["rows"][i][1:3] != head["rows"][j][1:3]]
    body_same = base["body"] == head["body"]
    return {"base_rows": len(base_keys), "head_rows": len(head_keys), "matched": len(pairs), "edited": edited,
            "added": added, "removed": removed, "color_diff": len(diffs) + (not body_same)}, diffs


def main():
    args = sys.argv[1:]
    head_root = args[args.index("--head-root") + 1] if "--head-root" in args else "."
    only_narrowed = "--only-narrowed" in args
    pages = measure.base_pages()
    dark_only = set(measure.dark_only())
    light_pages = [page for page in pages if page not in dark_only]
    base_dir = measure.base_tree()
    rcs, bad = [], 0
    try:
        full_dark = [page for page in pages if page not in NARROWED]
        full_light = [page for page in light_pages if page not in NARROWED]
        if not only_narrowed:
            for theme, group in (("dark", full_dark), ("light", full_light)):
                rc_base, base_fp = measure.paint(theme, group, base_dir)
                rc_head, head_fp = measure.paint(theme, group, "" if head_root == "." else head_root)
                rcs += [rc_base, rc_head]
                for page in group:
                    before, after = base_fp.get(page, {}).get("fp"), head_fp.get(page, {}).get("fp")
                    if before is None or before != after:
                        bad += 1
                        print(f"BAD {theme} {page} {before} -> {after}")
        narrowed_bad, checks = 0, 0
        for theme in ("dark", "light"):
            group = [page for page in NARROWED if theme == "dark" or page in light_pages]
            if not group:
                continue
            rc_base, base_rows = read_rows(theme, group, base_dir)
            rc_head, head_rows = read_rows(theme, group, head_root)
            rc_fp, base_fp = measure.paint(theme, group, base_dir)
            rcs += [rc_base, rc_head, rc_fp]
            for page in group:
                checks += 1
                if page not in base_rows or page not in head_rows:
                    narrowed_bad += 1
                    print(f"NARROW {theme} {page} MISSING")
                    continue
                stat, diffs = compare(base_rows[page], head_rows[page])
                agree = int(fingerprint(base_rows[page]) == base_fp.get(page, {}).get("fp"))
                ok = stat["removed"] == 0 and stat["color_diff"] == 0 and agree
                narrowed_bad += not ok
                print(f"NARROW {theme} {page} " + " ".join(f"{k}={v}" for k, v in stat.items()) + f" fp_agree={agree}")
                for i, j in diffs[:5]:
                    print(f"  DIFF {base_rows[page]['rows'][i]} -> {head_rows[page]['rows'][j]}")
    finally:
        subprocess.run(["rm", "-rf", base_dir])
    summary = "skipped" if only_narrowed else f"dark_pages={len(full_dark)} light_pages={len(full_light)} changed={bad}"
    print(f"{summary} narrowed_checks={checks} narrowed_bad={narrowed_bad} br_rc={','.join(map(str, rcs))}")
    return 0 if bad == 0 and narrowed_bad == 0 and checks == len(NARROWED) and not any(rcs) else 1


if __name__ == "__main__":
    sys.exit(main())
