#!/usr/bin/env python3
"""check-docs-common-css.py 시험 — 임시 폴더의 사본 쪽으로 일곱 경우를 돌린다. 레포 파일은 건드리지 않는다.

  1. 정상 쪽 + 링크 둘인 쪽 → 종료 코드 1, 둘째 파일 이름만 적힘, 검사한 쪽 2
  2. 본문 `site&#46;css` 쪽 · `prefers&#45;reduced-motion` 쪽, 그리고 이름 글자 참조 `site&period;css` ·
     `prefers&dash;reduced&hyphen;motion` 쪽과 태그를 끼운 `site<span>.</span>css` 쪽 → 각각 종료 코드 1
  3. 링크 하나 + 본문에 원래 글자 이름 + 주석 안 링크 + 작은따옴표 링크 쪽 → 종료 코드 0
  4. 링크 둘인 쪽 + UTF-8 이 아닌 바이트 쪽 → 종료 코드 2, 두 파일 이름이 모두 적힘
  5. 검사 사본을 scripts/ 에 넣은, 추적 HTML 이 0 개인 임시 git 저장소에서 인자 없이 → 종료 코드 3
  6. ① `<style>` 에 움직임 줄이기 블록을 다시 적은 쪽 + 정상 쪽 → 종료 코드 1, 앞 쪽 이름만 적힘
     ② 본문 `<code>` · `<script>` 의 `matchMedia` · `<style>` 안 CSS 주석에만 이름이 있는 쪽 → 종료 코드 0
  7. ① `<style media="(prefers-reduced-motion: reduce)">` 쪽 → 종료 코드 1, 그 쪽 이름 적힘
     ② `<link rel="stylesheet" media="(prefers-reduced-motion: reduce)" href="…">` 쪽 → 종료 코드 1, 그 쪽 이름 적힘
     ③ `media="print"` 인 `<style>` · `<link>` 만 있는 쪽 → 종료 코드 0

사용법:
    python3 scripts/test-check-docs-common-css.py [--check <검사 사본 경로>]

--check 는 음성 대조용이다 — 글자 참조 세기를 지운 사본은 경우 2 가, 주석 빼기를 지운 사본은 경우 3 이 실패해야 한다.
움직임 규칙 세기를 지운 사본은 경우 6 ① 이, CSS 주석 빼기를 지운 사본은 경우 6 ② 가 실패해야 한다.
media 속성 보기를 지운 사본은 경우 7 ① ② 가 실패해야 한다.
종료 코드는 harness/evals/gate-exit-codes.md 를 따른다 (0 통과 · 1 실패 · 2 준비 실패).
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

LINK = '<link rel="stylesheet" href="../assets/site.css">'


def page(head: str, body: str = "<p>본문</p>") -> str:
    return f"<!DOCTYPE html>\n<html><head>{head}</head><body>{body}</body></html>\n"


def run(check: Path, *files: Path, cwd: Path | None = None) -> tuple[int, str]:
    result = subprocess.run(["python3", str(check), *map(str, files)], cwd=cwd,
                            capture_output=True, text=True, encoding="utf-8")
    return result.returncode, result.stdout


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def case_two_links(tmp: Path, check: Path) -> tuple[bool, str]:
    good = write(tmp / "c1/good.html", page(LINK))
    bad = write(tmp / "c1/double.html", page(LINK + LINK))
    rc, out = run(check, good, bad)
    ok = rc == 1 and "double.html" in out and "good.html" not in out and "검사한 쪽 2" in out
    return ok, f"rc={rc}"


SPLIT_BODIES = {
    "dot": "<p>site&#46;css 를 부른다</p>",
    "dash": "<p>prefers&#45;reduced-motion 을 쓴다</p>",
    "named-dot": "<p>site&period;css 를 부른다</p>",
    "named-dash": "<p>prefers&dash;reduced&hyphen;motion 을 쓴다</p>",
    "tag-split": "<p>site<span>.</span>css 를 부른다</p>",
}


def case_split_names(tmp: Path, check: Path) -> tuple[bool, str]:
    codes = [run(check, write(tmp / f"c2/{name}.html", page(LINK, body)))[0] for name, body in SPLIT_BODIES.items()]
    return all(code == 1 for code in codes), "rc=" + ",".join(map(str, codes))


def case_plain_names(tmp: Path, check: Path) -> tuple[bool, str]:
    body = ("<p><code>site.css</code> · <code>prefers-reduced-motion</code></p>"
            "<!-- <link rel=\"stylesheet\" href=\"../assets/site.css\"> -->")
    plain = write(tmp / "c3/plain.html", page("<link rel='stylesheet' href='../assets/site.css'>", body))
    rc, out = run(check, plain)
    return rc == 0, f"rc={rc}"


def case_unreadable(tmp: Path, check: Path) -> tuple[bool, str]:
    double = write(tmp / "c4/double.html", page(LINK + LINK))
    broken = tmp / "c4/broken.html"
    broken.write_bytes(b"<html>\xff\xfe\xfa</html>\n")
    rc, out = run(check, double, broken)
    return rc == 2 and "double.html" in out and "broken.html" in out, f"rc={rc}"


def case_no_pages(tmp: Path, check: Path) -> tuple[bool, str]:
    repo = tmp / "c5"
    (repo / "scripts").mkdir(parents=True)
    shutil.copy(check, repo / "scripts/check-docs-common-css.py")
    init = subprocess.run(["git", "init", "-q"], cwd=repo, capture_output=True, text=True)
    if init.returncode != 0:
        raise RuntimeError(f"git init 실패: {init.stderr.strip()}")
    rc, _ = run(repo / "scripts/check-docs-common-css.py", cwd=repo)
    return rc == 3, f"rc={rc}"


def case_style_motion(tmp: Path, check: Path) -> tuple[bool, str]:
    rule = "<style>@media (prefers-reduced-motion: reduce){*{transition:none!important}}</style>"
    again = write(tmp / "c6/again.html", page(LINK + rule))
    good = write(tmp / "c6/good.html", page(LINK))
    rc_again, out = run(check, again, good)
    body = ("<p><code>prefers-reduced-motion</code> 은 공통 파일이 맡는다</p>"
            "<script>matchMedia('(prefers-reduced-motion: reduce)').matches</script>")
    style = "<style>/* prefers-reduced-motion 은 공통 파일이 맡는다 */ p{color:red}</style>"
    mentions = write(tmp / "c6/mentions.html", page(LINK + style, body))
    rc_mentions, _ = run(check, mentions)
    ok = rc_again == 1 and "again.html" in out and "good.html" not in out and rc_mentions == 0
    return ok, f"rc={rc_again},{rc_mentions}"


def case_media_attr(tmp: Path, check: Path) -> tuple[bool, str]:
    reduce = '"(prefers-reduced-motion: reduce)"'
    style = write(tmp / "c7/style-media.html", page(LINK + f"<style media={reduce}>*{{transition:none}}</style>"))
    link = write(tmp / "c7/link-media.html",
                 page(LINK + f'<link rel="stylesheet" media={reduce} href="../assets/motion.css">'))
    printed = write(tmp / "c7/print-media.html", page(
        LINK + '<style media="print">p{color:black}</style><link rel="stylesheet" media="print" href="print.css">'))
    rc_style, out_style = run(check, style)
    rc_link, out_link = run(check, link)
    rc_print, _ = run(check, printed)
    ok = rc_style == 1 and "style-media.html" in out_style and rc_link == 1 and "link-media.html" in out_link \
        and rc_print == 0
    return ok, f"rc={rc_style},{rc_link},{rc_print}"


CASES = [
    ("1 링크 둘인 쪽만 적는다", case_two_links),
    ("2 글자 참조로 쪼갠 이름을 잡는다", case_split_names),
    ("3 원래 글자 이름 · 주석 안 링크 · 작은따옴표 링크는 통과", case_plain_names),
    ("4 못 읽은 쪽은 종료 코드 2 로 함께 적는다", case_unreadable),
    ("5 추적 쪽이 없으면 종료 코드 3", case_no_pages),
    ("6 쪽 <style> 의 움직임 줄이기 규칙만 잡는다", case_style_motion),
    ("7 태그 media 속성의 움직임 줄이기도 잡고 print 는 통과", case_media_attr),
]


def main() -> int:
    parser = argparse.ArgumentParser(description="check-docs-common-css.py 시험")
    parser.add_argument("--check", type=Path, default=REPO_ROOT / "scripts/check-docs-common-css.py")
    args = parser.parse_args()
    if not args.check.is_file():
        print(f"ERROR: 검사가 없다 — {args.check}")
        return 2
    passed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for label, case in CASES:
            try:
                ok, detail = case(Path(tmp), args.check.resolve())
            except RuntimeError as error:
                print(f"ERROR 경우 {label}: {error}")
                return 2
            passed += ok
            print(f"{'PASS' if ok else 'FAIL'} 경우 {label} ({detail})")
    print(f"경우 {len(CASES)} 개 중 통과 {passed}")
    return 0 if passed == len(CASES) else 1


if __name__ == "__main__":
    sys.exit(main())
