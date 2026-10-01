#!/usr/bin/env python3
"""sync-evals.py 가 깨지거나 못 읽는 evals.json 을 없는 파일처럼 넘기지 않는지 보는 시험.

임시 폴더에 킷 하나짜리 마켓 목록과 도구 사본을 두고 --check-only 로 돌린다.
  1. 깨진 evals.json → 종료 코드 2, 출력에 그 경로
  2. 스킬과 맞는 정상 evals.json → 종료 코드 0
  3. 읽기 권한 없는 evals.json → 종료 코드 2, 출력에 UNREADABLE 과 그 경로
  4. 대상 없는 바로가기 evals.json → 종료 코드 2, 출력에 UNREADABLE 과 그 경로
  5. 평가 파일이 진짜 없는 킷 → 종료 코드 0, 대상 아님으로 넘김
  6. 킷 셋 중 가운데 b 만 못 읽음 → a · c 는 재고 끝에 못 읽은 킷 b 를 적은 뒤 종료 코드 2
  7 ~ 11. 내용이 null · 5 · "x" · [] · true → 종료 코드 2, 경로와 「객체가 아니다」 한 줄, 추적 출력 없음
  12 ~ 13. 목록 열쇠가 tests · cases 인 정상 파일 → 종료 코드 0
  14. 킷 셋 중 가운데 b 만 내용이 null → a · c 는 재고 끝에 못 읽은 킷 b 를 적은 뒤 종료 코드 2
  15. 처음 읽을 때는 되고 다시 읽을 때 못 읽음 → 못 읽은 킷 k 를 적은 뒤 종료 코드 2, 추적 출력 없음
  16 ~ 24. 항목 모양이 허용 목록 밖(항목이 숫자 · 목록 자리에 객체 · 글 · null · prompt 없음 · skill 이 숫자 ·
      assertions 안에 숫자 · 모르는 열쇠 · 두 번째 항목이 숫자) → 종료 코드 2, 경로와 몇 번째 항목 · 까닭 한 줄, 추적 출력 없음
  25. 킷 셋 중 가운데 b 만 항목 모양이 깨짐 → a · c 는 재고 끝에 못 읽은 킷 b 를 적은 뒤 종료 코드 2
  26 ~ 28. 레포 평가 파일이 쓰는 정상 모양(글 id · 글 assertions, expect · example · fixture, agent 항목) → 종료 코드 0

사용법:
    python3 scripts/test-sync-evals.py [--tool <도구 사본 경로>]

--tool 은 음성 대조용이다 — 파싱 실패를 SKIP 으로 넘기는 옛 사본을 주면 경우 1 이, 못 읽는 파일에서 멈추는
(추적 출력 · 종료 코드 1) 옛 사본을 주면 경우 3 이 실패해야 한다.
대상 없는 바로가기를 없는 파일로 치고 못 읽는 킷 하나에서 바로 끝나는 옛 사본(2026-09-30 전)은 경우 4 · 6 이,
바로가기 판정을 늘 참으로 바꿔 진짜 없는 평가 파일까지 못 읽음으로 치는 사본은 경우 5 가 실패해야 한다.
null 을 없는 파일로 치고 숫자 내용 · 다시 읽기 실패에서 추적 출력으로 죽는 옛 사본(2026-10-01 전)은 경우 7 ~ 11 · 14 · 15 가,
어떤 내용이든 객체가 아니라고 치는 지나친 사본은 정상 모양 경우 2 · 12 · 13 이 실패해야 한다.
항목 모양을 보지 않는 옛 사본(2026-10-01 판)은 경우 16 ~ 25 가, 아는 모양도 깨진 것으로 치는 지나친 사본은
정상 모양 경우 2 · 12 · 13 · 26 ~ 28 이 실패해야 한다.
경우 15 는 도구를 모듈로 불러 두 번째 읽기만 못 읽음 표시를 돌려주게 바꿔 흉내 낸다 — 두 읽기 사이에 파일이 바뀌는 경우다.
root 로 돌면 권한을 빼도 읽혀서 경우 3 을 만들 수 없다 — 그때는 준비 실패 2 로 멈춘다.
종료 코드는 harness/evals/gate-exit-codes.md 의 값을 쓴다 (0 통과 · 1 실패 · 2 준비 실패).
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

GOOD_EVALS = (
    '{"evals":[{"id":1,"skill":"s","prompt":"p","expected_output":"e",'
    '"assertions":[{"text":"a","type":"output"}]}]}'
)
GOOD_ITEM = '{"id":1,"skill":"s","prompt":"p","expected_output":"e","assertions":[{"text":"a","type":"output"}]}'
# 항목 모양이 깨진 내용 — 목록 열쇠의 값이 목록이 아니거나, 항목이 허용 목록 밖 모양이다
BROKEN_ITEMS = [
    ("항목이 숫자", "item-number", '{"evals":[1]}', "1 번째 항목|객체가 아니다"),
    ("목록 자리에 객체", "list-object", '{"evals":{"x":1}}', "evals|목록이 아니다"),
    ("목록 자리에 글", "list-string", '{"evals":"abc"}', "evals|목록이 아니다"),
    ("목록 자리에 null", "list-null", '{"evals":null}', "evals|목록이 아니다"),
    ("항목에 prompt 없음", "no-prompt", '{"evals":[' + GOOD_ITEM.replace('"prompt":"p",', "") + ']}', "1 번째 항목|prompt"),
    ("skill 이 숫자", "skill-number", '{"evals":[' + GOOD_ITEM.replace('"skill":"s"', '"skill":5') + ']}', "1 번째 항목|skill"),
    ("assertions 안에 숫자", "assertion-number", '{"evals":[' + GOOD_ITEM.replace('[{"text":"a","type":"output"}]', "[5]") + ']}', "1 번째 항목|assertions"),
    ("모르는 열쇠 promt", "unknown-key", '{"evals":[' + GOOD_ITEM.replace('"prompt":"p"', '"prompt":"p","promt":"p"') + ']}', "1 번째 항목|promt"),
    ("두 번째 항목이 숫자", "second-item", '{"evals":[' + GOOD_ITEM + ',1]}', "2 번째 항목|객체가 아니다"),
]
# 레포 평가 파일이 실제로 쓰는 모양 — 글 id · 글 assertions(react-kit), expect · example · fixture(api-kit), agent 항목
GOOD_SHAPES = [
    ("글 id · 글 assertions", "react-shape", '{"tests":[{"id":"r1","skill":"s","prompt":"p","expected_output":"e","assertions":["a"]}]}'),
    ("expect · example · fixture", "api-shape",
     '{"cases":[{"id":1,"skill":"s","prompt":"p","expect":{"n":1},"assertions":[{"text":"a","type":"output"}],'
     '"example":"x","fixture":"f"}]}'),
    ("agent 항목", "agent-item", '{"evals":[' + GOOD_ITEM + ',{"id":2,"agent":"s","prompt":"p","expected_output":"e","assertions":["a"]}]}'),
]


def make_tree(root: Path, tool: Path, evals_text: str) -> None:
    (root / "scripts").mkdir(parents=True)
    shutil.copy(tool, root / "scripts/sync-evals.py")
    (root / ".claude-plugin").mkdir()
    (root / ".claude-plugin/marketplace.json").write_text('{"plugins":[{"name":"k","source":"./k"}]}\n', encoding="utf-8")
    (root / "k/skills/s").mkdir(parents=True)
    (root / "k/skills/s/SKILL.md").write_text("---\nname: s\ndescription: d\nuser-invocable: true\n---\n\n본문\n", encoding="utf-8")
    (root / "k/evals").mkdir()
    (root / "k/evals/evals.json").write_text(evals_text + "\n", encoding="utf-8")


def shape_tree(root: Path, shape: str) -> list[Path]:
    """경우 모양을 트리에 입힌다. 권한을 뺄 파일 목록을 돌려준다."""
    evals = root / "k/evals/evals.json"
    if shape == "unreadable":
        return [evals]
    if shape == "dangling":
        evals.unlink()
        evals.symlink_to("missing.json")
    elif shape == "absent":
        shutil.rmtree(root / "k/evals")
    elif shape.startswith("multi"):
        # 킷 셋 중 가운데 b 만 못 읽는다. a · c 는 평가에 없는 스킬 extra 를 둬 쟀다는 줄이 나오게 한다
        (root / ".claude-plugin/marketplace.json").write_text(
            '{"plugins":[{"name":"a","source":"./a"},{"name":"b","source":"./b"},{"name":"c","source":"./c"}]}\n',
            encoding="utf-8")
        for kit in ("a", "b", "c"):
            shutil.copytree(root / "k", root / kit)
        for kit in ("a", "c"):
            (root / kit / "skills/extra").mkdir()
            (root / kit / "skills/extra/SKILL.md").write_text(
                "---\nname: extra\ndescription: d\nuser-invocable: true\n---\n", encoding="utf-8")
        if shape == "multi-item":
            (root / "b/evals/evals.json").write_text('{"evals":[1]}\n', encoding="utf-8")
            return []
        if shape == "multi-null":
            (root / "b/evals/evals.json").write_text("null\n", encoding="utf-8")
            return []
        return [root / "b/evals/evals.json"]
    return []


def multi_ok(output: str, mark: str) -> bool:
    """a · c 칸(→ <킷> 줄부터 다음 → 줄 앞까지)마다 쟀다는 줄이 있고, 마지막 칸 뒤에 못 읽은 킷 b 요약 줄이 있다."""
    lines = output.splitlines()
    heads = [i for i, line in enumerate(lines) if line.startswith("→ ")]
    blocks = {lines[start][2:].strip(): "\n".join(lines[start:end])
              for start, end in zip(heads, heads[1:] + [len(lines)])}
    summary = [i for i, line in enumerate(lines) if line.strip() == "못 읽은 킷 1 개: b"]
    measured = all(mark.format(kit) in blocks.get(kit, "") for kit in ("a", "c"))
    return measured and len(summary) == 1 and summary[0] > heads[-1]


# 두 번째 읽기만 못 읽음 표시를 돌려준다 — main 이 읽은 뒤 process_kit 이 다시 읽는 사이에 파일이 바뀐 경우
SECOND_READ_FAILS = '''
import importlib.util, sys
spec = importlib.util.spec_from_file_location("sync_evals", "scripts/sync-evals.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
real_load, calls = mod.load_evals, {}
def second_read_fails(kit):
    calls[kit] = calls.get(kit, 0) + 1
    return real_load(kit) if calls[kit] == 1 else mod.UNREADABLE
mod.load_evals = second_read_fails
sys.argv = ["sync-evals.py", "--check-only"]
sys.exit(mod.main())
'''


def run_case(workdir: Path, name: str, tool: Path, evals_text: str, shape: str) -> tuple[int, str]:
    root = workdir / name
    make_tree(root, tool, evals_text)
    locked = shape_tree(root, shape)
    for path in locked:
        path.chmod(0)
    command = ["python3", "-c", SECOND_READ_FAILS] if shape == "second-read" \
        else ["python3", "scripts/sync-evals.py", "--check-only"]
    try:
        result = subprocess.run(
            command,
            cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8",
            env=dict(os.environ, PYTHONUNBUFFERED="1"),
        )
    finally:
        for path in locked:
            path.chmod(0o644)
    return result.returncode, result.stdout


# (이름표, 폴더, evals.json 내용, 모양, 기대 종료 코드, 출력에 있어야 할 글)
CASES = [
    ("1 깨진 evals.json 은 종료 코드 2", "broken", "{ broken", "good", 2, "k/evals/evals.json"),
    ("2 정상 evals.json 은 종료 코드 0", "good", GOOD_EVALS, "good", 0, ""),
    ("3 못 읽는 evals.json 은 종료 코드 2", "unreadable", GOOD_EVALS, "unreadable", 2, "UNREADABLE"),
    ("4 대상 없는 바로가기 evals.json 은 종료 코드 2", "dangling", GOOD_EVALS, "dangling", 2, "UNREADABLE"),
    ("5 평가 파일이 없는 킷은 대상 아님 · 종료 코드 0", "absent", GOOD_EVALS, "absent", 0, "대상 아님: k"),
    ("6 가운데 킷만 못 읽어도 나머지를 재고 종료 코드 2", "multi", GOOD_EVALS, "multi", 2, "b/evals/evals.json"),
    ("7 내용이 null 이면 종료 코드 2", "null", "null", "content", 2, "객체가 아니다"),
    ("8 내용이 숫자면 종료 코드 2", "number", "5", "content", 2, "객체가 아니다"),
    ("9 내용이 글이면 종료 코드 2", "string", '"x"', "content", 2, "객체가 아니다"),
    ("10 내용이 목록이면 종료 코드 2", "array", "[]", "content", 2, "객체가 아니다"),
    ("11 내용이 참거짓이면 종료 코드 2", "boolean", "true", "content", 2, "객체가 아니다"),
    ("12 목록 열쇠가 tests 면 종료 코드 0", "tests-key", GOOD_EVALS.replace('"evals"', '"tests"'), "good", 0, ""),
    ("13 목록 열쇠가 cases 면 종료 코드 0", "cases-key", GOOD_EVALS.replace('"evals"', '"cases"'), "good", 0, ""),
    ("14 가운데 킷만 null 이어도 나머지를 재고 종료 코드 2", "multi-null", GOOD_EVALS, "multi-null", 2, "b/evals/evals.json"),
    ("15 다시 읽을 때 못 읽으면 종료 코드 2", "second-read", GOOD_EVALS, "second-read", 2, "못 읽은 킷 1 개: k"),
    *[(f"{16 + i} 항목 모양 — {label} 은 종료 코드 2", case, text, "item", 2, words)
      for i, (label, case, text, words) in enumerate(BROKEN_ITEMS)],
    ("25 가운데 킷만 항목 모양이 깨져도 나머지를 재고 종료 코드 2", "multi-item", GOOD_EVALS, "multi-item", 2, "b/evals/evals.json"),
    *[(f"{26 + i} 정상 모양 — {label} 은 종료 코드 0", case, text, "good", 0, "")
      for i, (label, case, text) in enumerate(GOOD_SHAPES)],
]


def main() -> int:
    parser = argparse.ArgumentParser(description="sync-evals.py 깨진 파일 시험")
    parser.add_argument("--tool", type=Path, default=REPO_ROOT / "scripts/sync-evals.py")
    args = parser.parse_args()
    if not args.tool.is_file():
        print(f"ERROR: 도구가 없다 — {args.tool}")
        return 2
    passed = 0
    with tempfile.TemporaryDirectory() as tmp:
        probe = Path(tmp) / "probe"
        probe.write_text("x", encoding="utf-8")
        probe.chmod(0)
        if os.access(probe, os.R_OK):
            print("ERROR: 권한을 빼도 파일이 읽힌다 (root 로 도는가) — 경우 3 을 만들 수 없다")
            return 2
        for label, name, evals_text, shape, want_rc, want_text in CASES:
            rc, output = run_case(Path(tmp), name, args.tool, evals_text, shape)
            ok = rc == want_rc and all(word in output for word in want_text.split("|"))
            if shape in ("unreadable", "dangling"):
                ok = ok and "k/evals/evals.json" in output
            if shape == "content":
                # 경로와 까닭이 한 줄에 있고 추적 출력은 없다
                ok = ok and "Traceback" not in output and any(
                    "k/evals/evals.json" in line and want_text in line for line in output.splitlines())
            if shape == "second-read":
                ok = ok and "Traceback" not in output
            if shape == "item":
                # 경로 · 몇 번째 항목 · 까닭이 한 줄에 있고, 추적 출력 없이 못 읽은 킷 k 로 센다
                ok = ok and "Traceback" not in output and "못 읽은 킷 1 개: k" in output and any(
                    "k/evals/evals.json" in line and all(word in line for word in want_text.split("|"))
                    for line in output.splitlines())
            if shape in ("multi", "multi-null", "multi-item"):
                ok = ok and multi_ok(output, "[{0}] MISSING: extra")
            passed += ok
            print(f"{'PASS' if ok else 'FAIL'} 경우 {label} (rc={rc})")
    print(f"경우 {len(CASES)} 개 중 통과 {passed}")
    return 0 if passed == len(CASES) else 1


if __name__ == "__main__":
    sys.exit(main())
