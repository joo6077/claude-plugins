"""flutter-scenario-report 의 build_report.py 단위 테스트. 사용: python3 -m unittest discover -s flutter-toolkit/evals/scenario-report -v

BUILD_REPORT_SCRIPT 환경 변수로 대상 스크립트를 바꿀 수 있다 — 검사를 지운 사본으로 돌려 테스트가 실제로 떨어지는지 볼 때 쓴다.
"""
import copy
import importlib.util
import json
import os
import re
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
         "steps": [{"kw": "만일", "text": "방장 넘기기를 누른다"},
                   {"kw": "그리고", "text": "취소를 누른다"},
                   {"kw": "그러면", "text": "방장은 그대로다", "result": "pass", "seen": "데이터베이스 방장 Bob2"}],
         "shots": [{"file": "01-picker.png", "caption": "그룹 고르는 창"}]},
        {"name": "확인 창에서 취소한다",
         "steps": [{"kw": "만일", "text": "확인 창을 연다"},
                   {"kw": "그러면", "text": "제목이 다 보인다", "result": "fail", "seen": "제목 둘째 줄이 가려졌다",
                    "zoom": {"file": "02-title.png", "caption": "잘린 제목"}}],
         "shots": [{"file": "02-confirm.png", "caption": "확인 창"}]},
        {"name": "다시 연다",
         "steps": [{"kw": "만일", "text": "다시 연다"}, {"kw": "그러면", "text": "창이 뜬다"}],
         "skipped": "앞 시나리오 결함을 먼저 고친다."},
    ],
    "run": [["MCP 서버", "fitpal-mobile"]],
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

    def run_script(self, *args):
        done = subprocess.run([sys.executable, str(SCRIPT), str(self.root), *args],
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

    def test_builds_report(self):
        self.make_case(VALID)
        code, stdout, stderr = self.run_script()
        self.assertEqual(code, 0, stderr)
        self.assertIn("보고서:", stdout)
        page = (self.root / "index.html").read_text(encoding="utf-8")
        self.assertIn('src="TC-001-transfer/01-picker.png" width="3" height="7"', page)
        self.assertNotIn("data:image", page)

    def test_status_is_computed_from_steps(self):
        self.make_case(VALID)
        self.run_script()
        page = (self.root / "index.html").read_text(encoding="utf-8")
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
        self.assertEqual(re.findall(r'<article class="case" id="([^"]+)"', page), ["TC-001", "TC-000"])

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
        first = (self.root / "index.html").read_bytes()
        files = sorted(self.root.rglob("*"))
        self.run_script()
        self.assertEqual(first, (self.root / "index.html").read_bytes())
        self.assertEqual(files, sorted(self.root.rglob("*")))

    def test_format_doc_example_passes(self):
        doc = FORMAT_DOC.read_text(encoding="utf-8")
        example = json.loads(re.search(r"```json\n(.*?)\n```", doc, re.S).group(1))
        images = {shot["file"] for scenario in example["scenarios"] for shot in scenario.get("shots", [])}
        images |= {step["zoom"]["file"] for scenario in example["scenarios"] for step in scenario["steps"] if "zoom" in step}
        self.make_case(example, images=sorted(images))
        code, _, stderr = self.run_script("--check")
        self.assertEqual(code, 0, stderr)

    def test_format_doc_lists_every_key(self):
        spec = importlib.util.spec_from_file_location("build_report", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        doc = FORMAT_DOC.read_text(encoding="utf-8")
        keys = set()
        for fields in (module.CASE_FIELDS, module.META_FIELDS, module.SCENARIO_FIELDS, module.STEP_FIELDS, module.IMAGE_FIELDS):
            keys |= fields.keys()
        self.assertEqual(sorted(key for key in keys if f"`{key}`" not in doc), [])


if __name__ == "__main__":
    unittest.main()
