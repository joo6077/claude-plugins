#!/usr/bin/env python3
"""run-evals.py 가 eval 항목 0 개 · 못 읽는 evals.json 과 잘못 준 킷 이름을 통과시키지 않는지 보는 시험.

임시 폴더에 킷 하나짜리 마켓 목록과 도구 사본을 두고 돌린다.
  1. {"evals": []} → 종료 코드 2, 출력에 그 경로
  2. 목록 열쇠가 없는 {} → 종료 코드 2, 출력에 그 경로
  3. 항목 하나가 맞는 evals.json → 종료 코드 0
  4. 없는 킷 이름을 인자로 → 종료 코드 2, 출력에 그 이름
  5. 평가 파일이 없는 킷 이름을 인자로 → 종료 코드 2, 출력에 그 이름
  6. 읽기 권한 없는 evals.json → 종료 코드 2, 출력에 UNREADABLE 과 그 경로
  7. 대상 없는 바로가기 evals.json → 종료 코드 2, 출력에 UNREADABLE 과 그 경로
  8. 평가 파일이 진짜 없는 킷(인자 없이) → 종료 코드 0, 대상 아님으로 넘김
  9. 킷 셋 중 가운데 b 만 못 읽음 → a · c 는 재고 끝에 못 읽은 킷 b 를 적은 뒤 종료 코드 2
  10 ~ 14. 내용이 null · 5 · "x" · [] · true → 종료 코드 2, 경로와 「객체가 아니다」 한 줄, 추적 출력 없음
  15 ~ 16. 목록 열쇠가 tests · cases 인 정상 파일 → 종료 코드 0
  17. 킷 셋 중 가운데 b 만 항목 0 개 → a · c 는 재고 끝에 항목 없는 킷 b 를 적은 뒤 종료 코드 2
  18. 킷 셋 중 가운데 b 만 내용이 null → a · c 는 재고 끝에 못 읽은 킷 b 를 적은 뒤 종료 코드 2
  19. 대상 없는 바로가기 evals.json 을 가진 킷 이름을 인자로 → 종료 코드 2, UNREADABLE 과 그 경로, 「없음」 안내 없음
  20. 평가 파일이 진짜 없는 킷 이름을 인자로 → 종료 코드 2, 「evals/evals.json 없음」 안내
  21 ~ 29. 항목 모양이 허용 목록 밖(항목이 숫자 · 목록 자리에 객체 · 글 · null · prompt 없음 · skill 이 숫자 ·
      assertions 안에 숫자 · 모르는 열쇠 · 두 번째 항목이 숫자) → 종료 코드 2, 경로와 몇 번째 항목 · 까닭 한 줄, 추적 출력 없음
  30. 킷 셋 중 가운데 b 만 항목 모양이 깨짐 → a · c 는 재고 끝에 못 읽은 킷 b 를 적은 뒤 종료 코드 2
  31 ~ 33. 레포 평가 파일이 쓰는 정상 모양(글 id · 글 assertions, expect · example · fixture, agent 항목) → 종료 코드 0

사용법:
    python3 scripts/test-run-evals.py [--tool <도구 사본 경로>]

--tool 은 음성 대조용이다 — 빈 목록을 경고만 하고 넘기는 옛 사본을 주면 경우 1 · 2 가, 이름으로 준 킷을 SKIP 하거나
못 읽는 파일에서 멈추는(추적 출력 · 종료 코드 1) 옛 사본을 주면 경우 4 · 5 · 6 이 실패해야 한다.
대상 없는 바로가기를 없는 파일로 치고 못 읽는 킷 하나에서 바로 끝나는 옛 사본(2026-09-30 전)은 경우 7 · 9 가,
바로가기 판정을 늘 참으로 바꿔 진짜 없는 평가 파일까지 못 읽음으로 치는 사본은 경우 8 이 실패해야 한다.
null 을 없는 파일로 치고 항목 0 개 · 숫자 내용에서 그 자리에서 끝나는 옛 사본(2026-10-01 전)은 경우 10 ~ 14 · 17 ~ 19 가,
어떤 내용이든 객체가 아니라고 치는 지나친 사본은 정상 모양 경우 3 · 15 · 16 이 실패해야 한다.
항목 모양을 보지 않는 옛 사본(2026-10-01 판)은 경우 21 ~ 30 이, 아는 모양도 깨진 것으로 치는 지나친 사본은
정상 모양 경우 3 · 15 · 16 · 31 ~ 33 이 실패해야 한다.
root 로 돌면 권한을 빼도 읽혀서 경우 6 을 만들 수 없다 — 그때는 준비 실패 2 로 멈춘다.
도구 옆의 plugin_utils.py 를 같이 복사한다.
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
    shutil.copy(tool, root / "scripts/run-evals.py")
    shutil.copy(tool.parent / "plugin_utils.py", root / "scripts/plugin_utils.py")
    (root / ".claude-plugin").mkdir()
    (root / ".claude-plugin/marketplace.json").write_text('{"plugins":[{"name":"k","source":"./k"}]}\n', encoding="utf-8")
    (root / "k/skills/s").mkdir(parents=True)
    (root / "k/skills/s/SKILL.md").write_text("---\nname: s\ndescription: d\nuser-invocable: true\n---\n\n본문\n", encoding="utf-8")
    (root / "k/evals").mkdir()
    (root / "k/evals/evals.json").write_text(evals_text + "\n", encoding="utf-8")
    # 평가 파일이 없는 킷 — 이름으로 주면 재지 못하는 킷이다
    (root / "j/skills/s").mkdir(parents=True)


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
        if shape == "multi-empty":
            (root / "b/evals/evals.json").write_text('{"evals":[]}\n', encoding="utf-8")
            return []
        if shape == "multi-item":
            (root / "b/evals/evals.json").write_text('{"evals":[1]}\n', encoding="utf-8")
            return []
        if shape == "multi-null":
            (root / "b/evals/evals.json").write_text("null\n", encoding="utf-8")
            return []
        return [root / "b/evals/evals.json"]
    return []


def multi_ok(output: str, mark: str, summary_line: str = "못 읽은 킷 1 개: b") -> bool:
    """a · c 칸(→ <킷> 줄부터 다음 → 줄 앞까지)마다 쟀다는 줄이 있고, 마지막 칸 뒤에 b 요약 줄이 있다."""
    lines = output.splitlines()
    heads = [i for i, line in enumerate(lines) if line.startswith("→ ")]
    blocks = {lines[start][2:].strip(): "\n".join(lines[start:end])
              for start, end in zip(heads, heads[1:] + [len(lines)])}
    summary = [i for i, line in enumerate(lines) if line.strip() == summary_line]
    measured = all(mark.format(kit) in blocks.get(kit, "") for kit in ("a", "c"))
    return measured and len(summary) == 1 and summary[0] > heads[-1]


def run_case(workdir: Path, name: str, tool: Path, evals_text: str, args: list[str], shape: str) -> tuple[int, str]:
    root = workdir / name
    make_tree(root, tool, evals_text)
    locked = shape_tree(root, shape)
    for path in locked:
        path.chmod(0)
    try:
        result = subprocess.run(
            ["python3", "scripts/run-evals.py", *args],
            cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8",
            env=dict(os.environ, PYTHONUNBUFFERED="1"),
        )
    finally:
        for path in locked:
            path.chmod(0o644)
    return result.returncode, result.stdout


# (이름표, 폴더, evals.json 내용, 인자, 모양, 기대 종료 코드, 출력에 있어야 할 글)
CASES = [
    ('1 {"evals": []} 는 종료 코드 2', "empty-list", '{"evals":[]}', [], "good", 2, "k/evals/evals.json"),
    ("2 목록 열쇠 없는 {} 는 종료 코드 2", "no-key", "{}", [], "good", 2, "k/evals/evals.json"),
    ("3 항목 하나가 맞으면 종료 코드 0", "good", GOOD_EVALS, [], "good", 0, ""),
    ("4 없는 킷 이름은 종료 코드 2", "missing-kit", GOOD_EVALS, ["nope"], "good", 2, "nope"),
    ("5 평가 파일 없는 킷 이름은 종료 코드 2", "no-evals-kit", GOOD_EVALS, ["j"], "good", 2, "j —"),
    ("6 못 읽는 evals.json 은 종료 코드 2", "unreadable", GOOD_EVALS, [], "unreadable", 2, "UNREADABLE"),
    ("7 대상 없는 바로가기 evals.json 은 종료 코드 2", "dangling", GOOD_EVALS, [], "dangling", 2, "UNREADABLE"),
    ("8 평가 파일이 없는 킷은 대상 아님 · 종료 코드 0", "absent", GOOD_EVALS, [], "absent", 0, "대상 아님: k"),
    ("9 가운데 킷만 못 읽어도 나머지를 재고 종료 코드 2", "multi", GOOD_EVALS, [], "multi", 2, "b/evals/evals.json"),
    ("10 내용이 null 이면 종료 코드 2", "null", "null", [], "content", 2, "객체가 아니다"),
    ("11 내용이 숫자면 종료 코드 2", "number", "5", [], "content", 2, "객체가 아니다"),
    ("12 내용이 글이면 종료 코드 2", "string", '"x"', [], "content", 2, "객체가 아니다"),
    ("13 내용이 목록이면 종료 코드 2", "array", "[]", [], "content", 2, "객체가 아니다"),
    ("14 내용이 참거짓이면 종료 코드 2", "boolean", "true", [], "content", 2, "객체가 아니다"),
    ("15 목록 열쇠가 tests 면 종료 코드 0", "tests-key", GOOD_EVALS.replace('"evals"', '"tests"'), [], "good", 0, ""),
    ("16 목록 열쇠가 cases 면 종료 코드 0", "cases-key", GOOD_EVALS.replace('"evals"', '"cases"'), [], "good", 0, ""),
    ("17 가운데 킷만 항목 0 개여도 나머지를 재고 종료 코드 2", "multi-empty", GOOD_EVALS, [], "multi-empty", 2, "b/evals/evals.json"),
    ("18 가운데 킷만 null 이어도 나머지를 재고 종료 코드 2", "multi-null", GOOD_EVALS, [], "multi-null", 2, "b/evals/evals.json"),
    ("19 이름으로 준 킷이 대상 없는 바로가기면 못 읽음 · 종료 코드 2", "named-dangling", GOOD_EVALS, ["k"], "dangling", 2, "UNREADABLE"),
    ("20 이름으로 준 킷의 평가 파일이 없으면 없음 · 종료 코드 2", "named-absent", GOOD_EVALS, ["j"], "good", 2, "j — evals/evals.json 없음"),
    *[(f"{21 + i} 항목 모양 — {label} 은 종료 코드 2", case, text, [], "item", 2, words)
      for i, (label, case, text, words) in enumerate(BROKEN_ITEMS)],
    ("30 가운데 킷만 항목 모양이 깨져도 나머지를 재고 종료 코드 2", "multi-item", GOOD_EVALS, [], "multi-item", 2, "b/evals/evals.json"),
    *[(f"{31 + i} 정상 모양 — {label} 은 종료 코드 0", case, text, [], "good", 0, "")
      for i, (label, case, text) in enumerate(GOOD_SHAPES)],
]


def main() -> int:
    parser = argparse.ArgumentParser(description="run-evals.py 빈 목록 시험")
    parser.add_argument("--tool", type=Path, default=REPO_ROOT / "scripts/run-evals.py")
    args = parser.parse_args()
    if not args.tool.is_file() or not (args.tool.parent / "plugin_utils.py").is_file():
        print(f"ERROR: 도구나 옆의 plugin_utils.py 가 없다 — {args.tool}")
        return 2
    passed = 0
    with tempfile.TemporaryDirectory() as tmp:
        probe = Path(tmp) / "probe"
        probe.write_text("x", encoding="utf-8")
        probe.chmod(0)
        if os.access(probe, os.R_OK):
            print("ERROR: 권한을 빼도 파일이 읽힌다 (root 로 도는가) — 경우 6 을 만들 수 없다")
            return 2
        for label, name, evals_text, tool_args, shape, want_rc, want_text in CASES:
            rc, output = run_case(Path(tmp), name, args.tool, evals_text, tool_args, shape)
            ok = rc == want_rc and all(word in output for word in want_text.split("|"))
            if shape in ("unreadable", "dangling"):
                ok = ok and "k/evals/evals.json" in output
            if shape == "dangling" and tool_args:
                ok = ok and "evals.json 없음" not in output
            if shape == "content":
                # 경로와 까닭이 한 줄에 있고 추적 출력은 없다
                ok = ok and "Traceback" not in output and any(
                    "k/evals/evals.json" in line and want_text in line for line in output.splitlines())
            if shape == "item":
                # 경로 · 몇 번째 항목 · 까닭이 한 줄에 있고, 추적 출력 없이 못 읽은 킷 k 로 센다
                ok = ok and "Traceback" not in output and "못 읽은 킷 1 개: k" in output and any(
                    "k/evals/evals.json" in line and all(word in line for word in want_text.split("|"))
                    for line in output.splitlines())
            if shape in ("multi", "multi-null", "multi-item"):
                ok = ok and multi_ok(output, "PASS: 1 passed, 0 failed")
            if shape == "multi-empty":
                ok = ok and multi_ok(output, "PASS: 1 passed, 0 failed", "항목 없는 킷 1 개: b")
            passed += ok
            print(f"{'PASS' if ok else 'FAIL'} 경우 {label} (rc={rc})")
    print(f"경우 {len(CASES)} 개 중 통과 {passed}")
    return 0 if passed == len(CASES) else 1


if __name__ == "__main__":
    sys.exit(main())
