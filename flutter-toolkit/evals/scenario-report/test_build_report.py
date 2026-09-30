"""flutter-scenario-report 의 build_report.py 단위 테스트. 사용: python3 -m unittest discover -s flutter-toolkit/evals/scenario-report -v

BUILD_REPORT_SCRIPT 환경 변수로 대상 스크립트를 바꿀 수 있다 — 검사를 지운 사본으로 돌려 테스트가 실제로 떨어지는지 볼 때 쓴다.
스크립트는 자기 폴더 옆 templates/report.html 을 읽으므로 사본을 만들 때 템플릿도 같은 모양으로 옮긴다.
"""
import copy
import importlib.util
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

SKILL = Path(__file__).resolve().parents[2] / "skills" / "flutter-scenario-report"
SCRIPT = Path(os.environ.get("BUILD_REPORT_SCRIPT", SKILL / "scripts" / "build_report.py"))
FORMAT_DOC = SKILL / "references" / "record-format.md"
TEMPLATE = SCRIPT.parent.parent / "templates" / "report.html"
EXAMPLE = Path(__file__).resolve().parent / "example"


def png_bytes(width=1, height=1):
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
    rows = b"".join(b"\x00" + b"\xff\xff\xff" * width for _ in range(height))
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b"")


VALID = {
    "id": "TC-001",
    "title": "방장 넘기기를 중간에 취소하면 아무것도 바뀌지 않는다",
    "summary": "두 번째 시나리오에서 확인 창 제목이 잘렸다.",
    "meta": {"date": "2026-09-24 22:33", "device": "iPhone 17 시뮬레이터 (iOS 26.5)", "commit": "48426a79"},
    "background": ["Bob2 가 방장이다"],
    "scenarios": [
        {"name": "그룹 고르는 창에서 취소한다",
         "steps": [{"kw": "만일", "text": "방장 넘기기를 누른다", "do": [{"act": "⋯ 버튼 탭", "shot": "01-picker.png"},
                                                                          {"act": "방장 넘기기 탭", "shot": "01-picker.png"}]},
                   {"kw": "그리고", "text": "취소를 누른다", "do": [{"act": "취소 탭", "shot": "01-picker.png"}]},
                   {"kw": "그러면", "text": "방장은 그대로다", "result": "pass", "seen": "프로필 방장 표시 Bob2"}],
         "shots": [{"file": "01-picker.png", "caption": "그룹 고르는 창"}]},
        {"name": "확인 창에서 취소한다",
         "steps": [{"kw": "만일", "text": "확인 창을 연다", "do": [{"act": "PGA 브라보 탭", "shot": "02-confirm.png"}]},
                   {"kw": "그러면", "text": "제목이 다 보인다", "result": "fail", "seen": "제목 둘째 줄이 가려졌다",
                    "zoom": {"file": "02-title.png", "caption": "잘린 제목"}}],
         "shots": [{"file": "02-confirm.png", "caption": "확인 창"}]},
        {"name": "다시 연다",
         "steps": [{"kw": "만일", "text": "다시 연다", "do": [{"act": "방장 넘기기 탭"}]}, {"kw": "그러면", "text": "창이 뜬다"}],
         "skipped": "앞 시나리오 결함을 먼저 고친다."},
    ],
    "run": [["MCP 서버", "app-mobile"]],
}
IMAGES = ("01-picker.png", "02-confirm.png", "02-title.png")


class BuildReportTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())

    def make_case(self, record, folder="TC-001-transfer", images=IMAGES):
        case_dir = self.root / folder
        case_dir.mkdir(parents=True, exist_ok=True)
        text = record if isinstance(record, str) else json.dumps(record, ensure_ascii=False)
        (case_dir / "record.json").write_text(text, encoding="utf-8")
        for name in images:
            (case_dir / name).write_bytes(png_bytes(3, 7))
        return case_dir

    def run_script(self, *args, script=SCRIPT):
        done = subprocess.run([sys.executable, str(script), str(self.root), *args],
                              capture_output=True, text=True, encoding="utf-8")
        return done.returncode, done.stdout, done.stderr

    def assert_rejected(self, record, *expected, images=IMAGES):
        self.make_case(record, images=images)
        code, _, stderr = self.run_script()
        self.assertEqual(code, 1, stderr)
        self.assertIn("TC-001-transfer", stderr)
        for text in expected:
            self.assertIn(text, stderr)
        self.assertFalse((self.root / "index.html").exists())

    def copy_script(self, template):
        """스크립트를 임시 폴더로 옮기고 옆에 template 글로 템플릿을 둔다. None 이면 템플릿을 두지 않는다."""
        skill = Path(tempfile.mkdtemp())
        (skill / "scripts").mkdir()
        shutil.copyfile(SCRIPT, skill / "scripts" / SCRIPT.name)
        if template is not None:
            (skill / "templates").mkdir()
            (skill / "templates" / "report.html").write_text(template, encoding="utf-8")
        return skill / "scripts" / SCRIPT.name

    def assert_template_rejected(self, template):
        self.make_case(VALID)
        code, _, stderr = self.run_script(script=self.copy_script(template))
        self.assertEqual(code, 2, stderr)
        self.assertIn("templates/report.html", stderr)
        self.assertFalse((self.root / "index.html").exists())

    def case_page(self, folder="TC-001-transfer"):
        return (self.root / folder / "index.html").read_text(encoding="utf-8")

    def html_pages(self):
        return {path.relative_to(self.root): path.read_bytes() for path in sorted(self.root.rglob("index.html"))}

    def test_builds_report(self):
        self.make_case(VALID)
        code, stdout, stderr = self.run_script()
        self.assertEqual(code, 0, stderr)
        self.assertIn("보고서:", stdout)
        page = self.case_page()
        self.assertIn('src="01-picker.png" width="3" height="7"', page)
        self.assertNotIn("data:image", page)

    def test_status_is_computed_from_steps(self):
        self.make_case(VALID)
        self.run_script()
        page = self.case_page()
        states = re.findall(r'<section class="scn (\w+)"', page)
        self.assertEqual(states, ["pass", "fail", "skip"])
        self.assertIn('<span class="pill fail">❌ 실패</span>', page)
        self.assertIn("시나리오 3개 · 통과 1 · 실패 1 · 미실행 1", page)

    def test_failing_case_comes_first(self):
        passing = copy.deepcopy(VALID)
        passing["id"] = "TC-000"
        passing["scenarios"] = passing["scenarios"][:1]
        self.make_case(passing, folder="TC-000-ok")
        self.make_case(VALID)
        self.run_script()
        page = (self.root / "index.html").read_text(encoding="utf-8")
        self.assertEqual(re.findall(r'<a href="(TC-[^"]+)/index.html"', page), ["TC-001-transfer", "TC-000-ok"])
        self.assertIn('<span class="pill fail">❌ 실패</span><span class="id">TC-001</span>', page)
        self.assertIn(f'<span class="t">{VALID["title"]}</span>', page)

    def test_case_pages_and_list(self):
        passing = copy.deepcopy(VALID)
        passing["id"] = "TC-000"
        passing["scenarios"] = passing["scenarios"][:1]
        self.make_case(passing, folder="TC-000-ok")
        self.make_case(VALID)
        code, _, stderr = self.run_script()
        self.assertEqual(code, 0, stderr)
        for folder, case_id in (("TC-000-ok", "TC-000"), ("TC-001-transfer", "TC-001")):
            page = self.case_page(folder)
            self.assertEqual(re.findall(r'<article class="case" id="([^"]+)"', page), [case_id])
            self.assertIn('src="01-picker.png"', page)
            self.assertNotIn(f'src="{folder}/', page)
        root = (self.root / "index.html").read_text(encoding="utf-8")
        self.assertEqual(root.count('<section class="scn'), 0)
        self.assertEqual(root.count('href="TC-000-ok/index.html"'), 1)
        self.assertEqual(root.count('href="TC-001-transfer/index.html"'), 1)

    def test_error_invalid_json(self):
        self.assert_rejected('{"id": "TC-001",', "JSON 문법 오류")

    def test_error_unknown_key(self):
        record = copy.deepcopy(VALID)
        record["scenarios"][0]["steps"][2]["resutl"] = "pass"
        self.assert_rejected(record, "resutl", "모르는 키다")

    def test_error_missing_key(self):
        record = copy.deepcopy(VALID)
        del record["summary"]
        self.assert_rejected(record, "summary", "빠졌다")

    def test_error_missing_image(self):
        self.assert_rejected(VALID, "02-title.png", "파일이 케이스 폴더에 없다", images=IMAGES[:2])

    def test_error_bad_image_name(self):
        record = copy.deepcopy(VALID)
        record["scenarios"][0]["shots"][0]["file"] = "01 Picker.png"
        self.assert_rejected(record, "01 Picker.png", "소문자")

    def test_error_bad_keyword(self):
        record = copy.deepcopy(VALID)
        record["scenarios"][0]["steps"][0]["kw"] = "When"
        self.assert_rejected(record, ".kw", "Gherkin 한국어 키워드")

    def test_error_bad_result_value(self):
        record = copy.deepcopy(VALID)
        record["scenarios"][0]["steps"][2]["result"] = "ok"
        self.assert_rejected(record, ".result", "pass 나 fail")

    def test_error_result_on_action_step(self):
        record = copy.deepcopy(VALID)
        record["scenarios"][0]["steps"][0].update({"result": "pass", "seen": "눌렀다"})
        self.assert_rejected(record, "단계 1.result", "확인 단계가 아니라")

    def test_error_result_without_seen(self):
        record = copy.deepcopy(VALID)
        del record["scenarios"][0]["steps"][2]["seen"]
        self.assert_rejected(record, ".seen", "실제로 본 것")

    def test_error_no_checked_step(self):
        record = copy.deepcopy(VALID)
        del record["scenarios"][0]["steps"][2]["result"]
        del record["scenarios"][0]["steps"][2]["seen"]
        self.assert_rejected(record, "시나리오 1", "판정한 단계가 없다")

    def test_error_duplicate_id(self):
        self.make_case(VALID, folder="TC-001-copy")
        self.assert_rejected(VALID, "겹친다")

    def test_error_empty_root(self):
        code, _, stderr = self.run_script()
        self.assertEqual(code, 1)
        self.assertIn("record.json 이 있는 케이스 폴더가 없다", stderr)

    def test_warn_unreferenced_png(self):
        case_dir = self.make_case(VALID)
        (case_dir / "03-old.png").write_bytes(png_bytes())
        code, _, stderr = self.run_script()
        self.assertEqual(code, 0, stderr)
        self.assertIn("경고: TC-001-transfer/03-old.png", stderr)

    def test_check_writes_nothing(self):
        self.make_case(VALID)
        before = {path: path.stat().st_mtime_ns for path in self.root.rglob("*")}
        code, stdout, _ = self.run_script("--check")
        self.assertEqual(code, 0)
        self.assertIn("검사 통과", stdout)
        self.assertEqual(before, {path: path.stat().st_mtime_ns for path in self.root.rglob("*")})

    def test_rerun_is_identical(self):
        self.make_case(VALID)
        self.run_script()
        first = self.html_pages()
        files = sorted(self.root.rglob("*"))
        self.run_script()
        self.assertEqual(first, self.html_pages())
        self.assertEqual(files, sorted(self.root.rglob("*")))

    def test_error_template_missing(self):
        self.assert_template_rejected(None)

    def test_error_template_slot_zero(self):
        self.assert_template_rejected(TEMPLATE.read_text(encoding="utf-8").replace("<!-- cases -->", ""))

    def test_error_template_slot_extra(self):
        self.assert_template_rejected(TEMPLATE.read_text(encoding="utf-8").replace("<!-- cases -->", "<!-- cases -->" * 2))

    def test_example_report_is_current(self):
        shutil.copytree(EXAMPLE, self.root, dirs_exist_ok=True)
        committed = self.html_pages()
        for page in self.root.rglob("index.html"):
            page.unlink()
        code, _, stderr = self.run_script()
        self.assertEqual(code, 0, stderr)
        folders = [path for path in EXAMPLE.iterdir() if (path / "record.json").is_file()]
        self.assertEqual(len(committed), len(folders) + 1)
        self.assertEqual(committed, self.html_pages())

    def test_error_action_step_without_do(self):
        record = copy.deepcopy(VALID)
        del record["scenarios"][0]["steps"][0]["do"]
        self.assert_rejected(record, "TC-001-transfer/record.json 시나리오 1 단계 1.do", "조작 순서")

    def test_error_do_not_list(self):
        record = copy.deepcopy(VALID)
        record["scenarios"][0]["steps"][1]["do"] = {"act": "취소 탭", "shot": "01-picker.png"}
        self.assert_rejected(record, "시나리오 1 단계 2.do")

    def test_error_do_empty(self):
        for actions in ([], [{"act": " ", "shot": "01-picker.png"}]):
            with self.subTest(actions=actions):
                record = copy.deepcopy(VALID)
                record["scenarios"][0]["steps"][1]["do"] = actions
                self.assert_rejected(record, "시나리오 1 단계 2.do")

    def test_error_do_on_checked_step(self):
        record = copy.deepcopy(VALID)
        record["scenarios"][0]["steps"][2]["do"] = [{"act": "방장 표시 확인", "shot": "01-picker.png"}]
        self.assert_rejected(record, "시나리오 1 단계 3.do", "판정한 단계")

    def test_do_optional_on_setup(self):
        record = copy.deepcopy(VALID)
        record["scenarios"][0]["steps"].insert(0, {"kw": "조건", "text": "Bob2 가 방장이다"})
        record["scenarios"][1]["steps"].insert(0, {"kw": "먼저", "text": "프로필을 연다", "do": [{"act": "프로필 탭", "shot": "02-confirm.png"}]})
        record["scenarios"][1]["steps"].append({"kw": "그리고", "text": "목록이 보인다"})
        self.make_case(record)
        code, _, stderr = self.run_script("--check")
        self.assertEqual(code, 0, stderr)

    def test_do_rendered_as_list(self):
        self.make_case(VALID)
        self.run_script()
        page = self.case_page()
        self.assertIn('<span class="tx">방장 넘기기를 누른다</span><span class="mk"></span><ol class="do">'
                      '<li><span class="n">1</span><img src="01-picker.png" width="3" height="7" alt="⋯ 버튼 탭"><span class="act">⋯ 버튼 탭</span></li>'
                      '<li><span class="n">2</span><img src="01-picker.png" width="3" height="7" alt="방장 넘기기 탭">'
                      '<span class="act">방장 넘기기 탭</span></li></ol>', page)

    def test_fix_rendered_in_case_header(self):
        record = copy.deepcopy(VALID)
        record["fix"] = {"note": "확인 창 제목을 두 줄로 늘렸다", "commit": "9ab12cd"}
        self.make_case(record)
        self.run_script()
        page = self.case_page()
        self.assertIn('<p class="fix">고친 뒤 다시 돌린 결과 — 확인 창 제목을 두 줄로 늘렸다 · 커밋 9ab12cd</p>', page)
        self.assertLess(page.index('class="fix"'), page.index('class="case-body"'))

    def test_error_fix_without_note(self):
        record = copy.deepcopy(VALID)
        record["fix"] = {"commit": "9ab12cd"}
        self.assert_rejected(record, "fix.note", "빠졌다")

    def test_error_fix_unknown_key(self):
        record = copy.deepcopy(VALID)
        record["fix"] = {"note": "고쳤다", "reason": "제목"}
        self.assert_rejected(record, "fix.reason", "모르는 키다")

    def with_actions(self, count):
        record = copy.deepcopy(VALID)
        record["scenarios"][0]["steps"][0]["do"] = [{"act": f"조작 {number}", "shot": "01-picker.png"} for number in range(1, count + 1)]
        return record

    def test_error_do_string_item(self):
        record = copy.deepcopy(VALID)
        record["scenarios"][0]["steps"][0]["do"][1] = "방장 넘기기 탭"
        self.assert_rejected(record, "시나리오 1 단계 1.do[2]", "객체여야 한다")

    def test_error_do_item_without_shot(self):
        record = copy.deepcopy(VALID)
        del record["scenarios"][0]["steps"][0]["do"][1]["shot"]
        self.assert_rejected(record, "TC-001-transfer/record.json 시나리오 1 단계 1.do[2].shot", "캡처 파일 이름")

    def test_error_do_item_unknown_key(self):
        record = copy.deepcopy(VALID)
        record["scenarios"][0]["steps"][0]["do"][0]["note"] = "메모"
        self.assert_rejected(record, "시나리오 1 단계 1.do[1].note", "모르는 키다")

    def test_error_do_shot_missing_file(self):
        record = copy.deepcopy(VALID)
        record["scenarios"][0]["steps"][0]["do"][0]["shot"] = "09-none.png"
        self.assert_rejected(record, "시나리오 1 단계 1.do[1].shot", "파일이 케이스 폴더에 없다")

    def test_do_shot_counts_as_used(self):
        record = copy.deepcopy(VALID)
        record["scenarios"][0]["steps"][0]["do"][0]["shot"] = "05-op.png"
        self.make_case(record, images=IMAGES + ("05-op.png",))
        code, _, stderr = self.run_script()
        self.assertEqual(code, 0, stderr)
        self.assertNotIn("05-op.png", stderr)

    def test_do_shot_optional_when_skipped(self):
        self.make_case(VALID)
        code, _, stderr = self.run_script("--check")
        self.assertEqual(code, 0, stderr)
        record = copy.deepcopy(VALID)
        del record["scenarios"][2]["skipped"]
        record["scenarios"][2]["steps"][1].update({"result": "pass", "seen": "창이 떴다"})
        self.assert_rejected(record, "시나리오 3 단계 1.do[1].shot")

    def test_do_rendered_with_shots(self):
        self.make_case(VALID)
        self.run_script()
        self.assertIn('<li><span class="n">1</span><img src="02-confirm.png" width="3" height="7" alt="PGA 브라보 탭">'
                      '<span class="act">PGA 브라보 탭</span></li>', self.case_page())

    def test_do_folds_after_three(self):
        self.make_case(self.with_actions(9))
        self.run_script()
        page = self.case_page()
        self.assertEqual(page.count('<details class="more">'), 1)
        self.assertIn('<span class="more-open">조작 6개 더 보기 (모두 9개)</span><span class="more-close">접기</span>', page)
        shown, folded = re.search(r'<ol class="do">(.*?)</ol><details class="more">.*?<ol class="do">(.*?)</ol></details>', page).groups()
        self.assertEqual(re.findall(r'<span class="n">(\d+)</span>', shown), ["1", "2", "3"])
        self.assertEqual(re.findall(r'<span class="n">(\d+)</span>', folded), [str(number) for number in range(4, 10)])
        self.make_case(self.with_actions(3))
        self.run_script()
        self.assertNotIn('<details class="more">', self.case_page())

    def test_warn_many_actions(self):
        self.make_case(self.with_actions(9))
        code, _, stderr = self.run_script()
        self.assertEqual(code, 0, stderr)
        self.assertIn("경고: TC-001-transfer/record.json 시나리오 1 단계 1.do: 조작 9개", stderr)
        self.make_case(self.with_actions(8))
        code, _, stderr = self.run_script()
        self.assertEqual(code, 0, stderr)
        self.assertNotIn("조작 8개", stderr)
        self.assertNotIn(".do: 조작", stderr)

    def with_shots(self, count, size=(3, 7)):
        record = copy.deepcopy(VALID)
        names = [f"0{number}-shot.png" for number in range(1, count + 1)]
        record["scenarios"][0]["shots"] = [{"file": name, "caption": f"사진 {number}"} for number, name in enumerate(names, 1)]
        case_dir = self.make_case(record)
        for name in names:
            (case_dir / name).write_bytes(png_bytes(*size))
        return record

    def test_shots_in_strip(self):
        self.make_case(VALID)
        self.run_script()
        self.assertIn('<div class="body"><div class="shot-strip"><button class="shot-next" type="button" aria-label="다음 사진">›</button>'
                      '<div class="shots"><figure><div class="shot-frame"><img src="01-picker.png" width="3" height="7" alt="그룹 고르는 창">'
                      '</div><figcaption>그룹 고르는 창</figcaption></figure></div></div>', self.case_page())

    def test_wide_shot_takes_two_slots(self):
        for size, wide in (((20, 5), True), ((3, 7), False), ((7, 7), False)):
            with self.subTest(size=size):
                self.with_shots(1, size)
                self.run_script()
                page = self.case_page()
                self.assertEqual('<figure class="wide"><div class="shot-frame"><img src="01-shot.png"' in page, wide)
                self.assertIn('<div class="shot-frame"><img src="01-shot.png"', page)

    def test_shot_count_after_four(self):
        self.with_shots(5)
        self.run_script()
        page = self.case_page()
        self.assertEqual(page.count('<p class="shot-count">사진 5장</p>'), 1)
        self.assertEqual(page.count('<button class="shot-next"'), 2)
        self.with_shots(4)
        self.run_script()
        page = self.case_page()
        self.assertNotIn('class="shot-count"', page)
        self.assertEqual(page.count('<button class="shot-next"'), 2)

    def template_text(self):
        return TEMPLATE.read_text(encoding="utf-8")

    def test_template_strip_rules(self):
        text = self.template_text()
        self.assertEqual(text.count(".body:has("), 0)
        self.assertIn(".body{display:grid;grid-template-columns:minmax(0,1fr);", text)
        self.assertIn("overflow-x:auto", re.search(r"\.shots\{[^}]*\}", text).group(0))
        self.assertIn("--slot:max(160px,calc((100% - 4 * 14px) / 4.3))", text)
        self.assertIn(".shots figure.wide{flex-basis:calc(var(--slot) * 2 + 14px)}", text)
        self.assertIn(".shot-strip.has-more::after{opacity:1}", text)
        self.assertIn(".shot-strip.has-more .shot-next{display:block}", text)

    def test_template_strip_script(self):
        text = self.template_text()
        start = text.index("@media (max-width:900px){")
        depth, end = 0, start
        for end in range(start, len(text)):
            depth += {"{": 1, "}": -1}.get(text[end], 0)
            if depth == 0 and text[end] == "}":
                break
        narrow = text[start:end + 1]
        self.assertEqual(narrow.count(".shots figure{") + narrow.count(".shots img{"), 0)
        self.assertIn('classList.toggle("has-more",row.scrollLeft+row.clientWidth<row.scrollWidth-2)', text)
        self.assertIn("row.clientWidth*0.8", text)

    def test_error_writes_no_page(self):
        good = copy.deepcopy(VALID)
        good["id"] = "TC-000"
        self.make_case(good, folder="TC-000-ok")
        bad = copy.deepcopy(VALID)
        del bad["summary"]
        self.make_case(bad)
        for page in (self.root / "index.html", self.root / "TC-000-ok" / "index.html", self.root / "TC-001-transfer" / "index.html"):
            page.write_text("옛 페이지", encoding="utf-8")
        before = self.html_pages()
        code, _, stderr = self.run_script()
        self.assertEqual(code, 1, stderr)
        self.assertEqual(before, self.html_pages())

    def test_format_doc_example_passes(self):
        doc = FORMAT_DOC.read_text(encoding="utf-8")
        example = json.loads(re.search(r"```json\n(.*?)\n```", doc, re.S).group(1))
        images = {shot["file"] for scenario in example["scenarios"] for shot in scenario.get("shots", [])}
        images |= {step["zoom"]["file"] for scenario in example["scenarios"] for step in scenario["steps"] if "zoom" in step}
        images |= {action["shot"] for scenario in example["scenarios"] for step in scenario["steps"]
                   for action in step.get("do", []) if "shot" in action}
        self.make_case(example, images=sorted(images))
        code, _, stderr = self.run_script("--check")
        self.assertEqual(code, 0, stderr)

    def test_format_doc_lists_every_key(self):
        spec = importlib.util.spec_from_file_location("build_report", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        doc = FORMAT_DOC.read_text(encoding="utf-8")
        keys = set()
        for fields in (module.CASE_FIELDS, module.META_FIELDS, module.FIX_FIELDS, module.SCENARIO_FIELDS, module.STEP_FIELDS,
                       module.ACTION_FIELDS, module.IMAGE_FIELDS):
            keys |= fields.keys()
        self.assertEqual(sorted(key for key in keys if f"`{key}`" not in doc), [])


if __name__ == "__main__":
    unittest.main()
