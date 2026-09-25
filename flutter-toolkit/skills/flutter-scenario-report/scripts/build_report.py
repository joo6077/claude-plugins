"""케이스 폴더의 record.json 을 모아 시나리오 테스트 보고서 index.html 을 만든다.

사용: python3 build_report.py <test-evidence 폴더> [--check]
  --check  검사만 하고 파일을 쓰지 않는다
종료 코드: 0 성공 · 1 기록 오류 · 2 사용법 오류
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

KEYWORDS = ("먼저", "조건", "만일", "만약", "그러면", "그리고", "하지만", "단")
# 그리고 · 하지만 · 단 은 첫 그러면 뒤에서만 확인 단계다. 앞에 오면 행동 단계라 판정을 붙이지 않는다
SETUP_KEYWORDS = ("먼저", "조건", "만일", "만약")
RESULTS = ("pass", "fail")
ICON = {"pass": "✅", "fail": "❌"}
WORD = {"pass": "통과", "fail": "실패", "skip": "미실행"}
# 대문자·공백이 든 이름은 HTML 경로에서 깨지거나 운영체제마다 다르게 찾힌다
IMAGE_NAME = re.compile(r"[a-z0-9][a-z0-9-]*\.png")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

# 키 → (필수 여부, 형식). 여기 없는 키는 오타로 보고 막는다
CASE_FIELDS = {"id": (True, str), "title": (True, str), "summary": (True, str), "meta": (True, dict),
               "background": (False, list), "scenarios": (True, list), "run": (False, list)}
META_FIELDS = {"date": (True, str), "device": (True, str), "commit": (False, str)}
SCENARIO_FIELDS = {"name": (True, str), "steps": (True, list), "shots": (False, list), "skipped": (False, str)}
STEP_FIELDS = {"kw": (True, str), "text": (True, str), "result": (False, str), "seen": (False, str), "zoom": (False, dict)}
IMAGE_FIELDS = {"file": (True, str), "caption": (True, str)}

TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "report.html"
SLOT = "<!-- cases -->"


def check_fields(value, fields, where, errors):
    """형식이 맞으면 True. 모르는 키 · 빠진 키 · 형식이 틀린 키를 errors 에 더한다."""
    if not isinstance(value, dict):
        errors.append(f"{where}: 객체여야 한다")
        return False
    for key in sorted(value.keys() - fields.keys()):
        errors.append(f"{where}.{key}: 모르는 키다 — 쓸 수 있는 키: {', '.join(fields)}")
    ok = True
    for key, (required, kind) in fields.items():
        if key not in value:
            if required:
                errors.append(f"{where}.{key}: 빠졌다")
                ok = False
        elif not isinstance(value[key], kind) or (kind is str and not value[key].strip()):
            errors.append(f"{where}.{key}: {kind.__name__} 이어야 하고 비어 있으면 안 된다")
            ok = False
    return ok


def png_size(path):
    head = path.read_bytes()[:24]
    if not head.startswith(PNG_SIGNATURE) or head[12:16] != b"IHDR":
        return None
    return int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")


def load_case(folder):
    """record.json 하나를 읽어 검사하고, 시나리오 판정을 계산한 케이스를 돌려준다."""
    errors, used_images = [], set()
    where = f"{folder.name}/record.json"
    try:
        record = json.loads((folder / "record.json").read_text(encoding="utf-8"))
    except json.JSONDecodeError as problem:
        return None, [f"{where}: JSON 문법 오류 — {problem.msg} ({problem.lineno}행 {problem.colno}열)"], []
    if not check_fields(record, CASE_FIELDS, where, errors) or errors:
        return None, errors, []
    check_fields(record["meta"], META_FIELDS, f"{where} meta", errors)
    for index, item in enumerate(record.get("background", []), 1):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{where} background[{index}]: 비어 있지 않은 문자열이어야 한다")
    for index, pair in enumerate(record.get("run", []), 1):
        if not (isinstance(pair, list) and len(pair) == 2 and all(isinstance(part, str) for part in pair)):
            errors.append(f"{where} run[{index}]: [이름, 값] 문자열 두 개여야 한다")
    if not record["scenarios"]:
        errors.append(f"{where} scenarios: 시나리오가 하나 이상 있어야 한다")

    def check_image(image, label):
        if not check_fields(image, IMAGE_FIELDS, label, errors):
            return None
        name = image["file"]
        if not IMAGE_NAME.fullmatch(name):
            errors.append(f"{label}.file: '{name}' — 소문자 · 숫자 · 하이픈으로 된 .png 이름이어야 한다")
            return None
        path = folder / name
        if not path.is_file():
            errors.append(f"{label}.file: '{name}' 파일이 케이스 폴더에 없다")
            return None
        size = png_size(path)
        if size is None:
            errors.append(f"{label}.file: '{name}' 이 PNG 가 아니다")
            return None
        used_images.add(name)
        return {"file": name, "caption": image["caption"], "size": size}

    scenarios = []
    for number, scenario in enumerate(record["scenarios"], 1):
        label = f"{where} 시나리오 {number}"
        if not check_fields(scenario, SCENARIO_FIELDS, label, errors):
            continue
        steps, checked, then_seen = [], [], False
        for step_number, step in enumerate(scenario["steps"], 1):
            step_label = f"{label} 단계 {step_number}"
            if not check_fields(step, STEP_FIELDS, step_label, errors):
                continue
            keyword = step["kw"]
            if keyword not in KEYWORDS:
                errors.append(f"{step_label}.kw: '{keyword}' — Gherkin 한국어 키워드({' · '.join(KEYWORDS)})가 아니다")
            then_seen = then_seen or keyword == "그러면"
            result = step.get("result")
            if result is not None:
                if result not in RESULTS:
                    errors.append(f"{step_label}.result: '{result}' — pass 나 fail 이어야 한다")
                if keyword in SETUP_KEYWORDS or not then_seen:
                    errors.append(f"{step_label}.result: '{keyword}' 단계는 확인 단계가 아니라 판정을 붙일 수 없다")
                if "seen" not in step:
                    errors.append(f"{step_label}.seen: 판정한 단계는 실제로 본 것을 적어야 한다")
                checked.append(result)
            elif "seen" in step or "zoom" in step:
                errors.append(f"{step_label}: 판정이 없는 단계에 seen · zoom 을 붙일 수 없다")
            zoom = check_image(step["zoom"], f"{step_label}.zoom") if "zoom" in step else None
            steps.append({"kw": keyword, "text": step["text"], "result": result, "seen": step.get("seen"), "zoom": zoom})
        if not scenario["steps"]:
            errors.append(f"{label}.steps: 단계가 하나 이상 있어야 한다")
        if "skipped" in scenario:
            status = "skip"
            if checked:
                errors.append(f"{label}: 건너뛴 시나리오에 판정한 단계가 있다")
        elif not checked:
            status = None
            errors.append(f"{label}: 판정한 단계가 없다 — 건너뛰었으면 skipped 에 이유를 적는다")
        else:
            status = "fail" if "fail" in checked else "pass"
        shots = [check_image(image, f"{label} shots[{index}]") for index, image in enumerate(scenario.get("shots", []), 1)]
        scenarios.append({"name": scenario["name"], "status": status, "steps": steps,
                          "shots": [shot for shot in shots if shot], "skipped": scenario.get("skipped")})

    warnings = [f"{folder.name}/{png.name}: 기록이 가리키지 않는 캡처다"
                for png in sorted(folder.glob("*.png")) if png.name not in used_images]
    if errors:
        return None, errors, warnings
    statuses = [scenario["status"] for scenario in scenarios]
    result = "fail" if "fail" in statuses else "pass" if "pass" in statuses else "skip"
    meta = record["meta"]
    case = {"folder": folder.name, "id": record["id"], "title": record["title"], "summary": record["summary"],
            "meta": " · ".join([record["id"], meta["date"], meta["device"]] + ([f"커밋 {meta['commit']}"] if "commit" in meta else [])),
            "background": record.get("background", []), "run": record.get("run", []),
            "scenarios": scenarios, "result": result}
    return case, [], warnings


def steps_html(case, scenario):
    rows, checking = [], False
    for step in scenario["steps"]:
        start = ""
        if step["kw"] == "그러면" and not checking:
            checking = True
            start = " check-start" if rows else ""
        result = step["result"]
        extra = f'<div class="obs">{html.escape(step["seen"])}</div>' if step["seen"] else ""
        if step["zoom"]:
            zoom = step["zoom"]
            extra += (f'<figure class="zoom"><img src="{quote(case["folder"])}/{zoom["file"]}" '
                      f'width="{zoom["size"][0]}" height="{zoom["size"][1]}" alt="{html.escape(zoom["caption"])}"></figure>')
        rows.append(f'<li class="step{start}{" " + result if result else ""}"><span class="kw">{html.escape(step["kw"])}</span>'
                    f'<span class="tx">{html.escape(step["text"])}</span><span class="mk">{ICON.get(result, "")}</span>{extra}</li>')
    return f'<ol class="stepl">{"".join(rows)}</ol>'


def case_html(case):
    anchor = re.sub(r"[^A-Za-z0-9-]", "-", case["id"])
    counts = {status: sum(1 for scenario in case["scenarios"] if scenario["status"] == status) for status in WORD}
    tally = f'시나리오 {len(case["scenarios"])}개 · ' + " · ".join(
        f"{WORD[status]} {counts[status]}" for status in ("pass", "fail", "skip") if counts[status])
    pill = f'{ICON[case["result"]]} {WORD[case["result"]]}' if case["result"] in ICON else WORD[case["result"]]
    head = (f'<p class="meta">{html.escape(case["meta"])}</p><h1>{html.escape(case["title"])}</h1>'
            f'<div class="verdict"><span class="pill {case["result"]}">{pill}</span><span class="tally">{tally}</span></div>'
            f'<p class="reason">{html.escape(case["summary"])}</p>')

    rail_items, sections = [], []
    for number, scenario in enumerate(case["scenarios"], 1):
        status, section_id = scenario["status"], f"{anchor}-s{number}"
        tag = f'<span class="tag">{WORD[status]}</span>' if status not in ICON else ""
        rail_items.append(f'<li><a class="{status}" href="#{section_id}"><span class="m">{ICON.get(status, "–")}</span>'
                          f'<span class="n">{number}</span><span class="t">{html.escape(scenario["name"])}{tag}</span></a></li>')
        shots = "".join(f'<figure><img src="{quote(case["folder"])}/{shot["file"]}" width="{shot["size"][0]}" '
                        f'height="{shot["size"][1]}" alt="{html.escape(shot["caption"])}"><figcaption>{html.escape(shot["caption"])}</figcaption></figure>'
                        for shot in scenario["shots"])
        left = f'<div class="shots">{shots}</div>' if shots else ""
        skipped = f'<p class="skipped">{html.escape(scenario["skipped"])}</p>' if scenario["skipped"] else ""
        state = f'{ICON[status]} {WORD[status]}' if status in ICON else WORD[status]
        sections.append(f'<section class="scn {status}" id="{section_id}">'
                        f'<div class="scn-h"><div><div class="no">시나리오 {number}</div><h2>{html.escape(scenario["name"])}</h2></div>'
                        f'<span class="state {status}">{state}</span></div>'
                        f'<div class="{"body" if shots else "body noshot"}">{left}<div>{steps_html(case, scenario)}{skipped}</div></div></section>')

    background = ("<h3>테스트 전 상태</h3><ul>" + "".join(f"<li>{html.escape(item)}</li>" for item in case["background"]) + "</ul>"
                  if case["background"] else "")
    rail = (f'<section class="pre"><div class="rail-head"><div class="rail-head-in"><div class="rail-head-box">'
            f'<p class="rail-meta">{html.escape(case["id"])}</p><p class="rail-title">{html.escape(case["title"])}</p></div></div></div>'
            f'<div class="rail-scn-wrap"><h3>시나리오</h3><ol class="rail-scn">{"".join(rail_items)}</ol></div>{background}</section>')
    run = ("<details class=\"run\"><summary>실행 정보</summary><dl>"
           + "".join(f"<dt>{html.escape(name)}</dt><dd>{html.escape(value)}</dd>" for name, value in case["run"]) + "</dl></details>"
           if case["run"] else "")
    return (f'<article class="case" id="{anchor}">{head}<div class="case-body">{rail}<div class="scns">{"".join(sections)}</div></div>'
            f'{run}</article>')


def load_template():
    """템플릿 글을 돌려준다. 없거나 자리 표시가 정확히 하나가 아니면 오류 줄을 찍고 None."""
    if not TEMPLATE.is_file():
        print(f"오류: templates/report.html 이 없다 — {TEMPLATE}", file=sys.stderr)
        return None
    template = TEMPLATE.read_text(encoding="utf-8")
    count = template.count(SLOT)
    if count != 1:
        print(f"오류: templates/report.html 에 {SLOT} 가 정확히 하나 있어야 한다 — 지금 {count} 개", file=sys.stderr)
        return None
    return template


def main(argv=None):
    parser = argparse.ArgumentParser(description="record.json 을 모아 시나리오 테스트 보고서를 만든다")
    parser.add_argument("root", type=Path, help="test-evidence 폴더")
    parser.add_argument("--check", action="store_true", help="검사만 하고 파일을 쓰지 않는다")
    args = parser.parse_args(argv)
    if not args.root.is_dir():
        print(f"오류: {args.root} 폴더가 없다", file=sys.stderr)
        return 2
    template = load_template()
    if template is None:
        return 2

    folders = sorted(path.parent for path in args.root.glob("*/record.json"))
    if not folders:
        print(f"오류: {args.root} 아래에 record.json 이 있는 케이스 폴더가 없다", file=sys.stderr)
        return 1
    cases, errors, warnings, ids = [], [], [], {}
    for folder in folders:
        case, case_errors, case_warnings = load_case(folder)
        errors += case_errors
        warnings += case_warnings
        if case:
            if case["id"] in ids:
                errors.append(f"{folder.name}/record.json id: '{case['id']}' 가 {ids[case['id']]} 와 겹친다")
            ids[case["id"]] = folder.name
            cases.append(case)
    for line in warnings:
        print(f"경고: {line}", file=sys.stderr)
    if errors:
        for line in errors:
            print(f"오류: {line}", file=sys.stderr)
        return 1

    # 실패한 케이스를 위로 — 보고서를 연 사람이 먼저 봐야 할 것부터
    cases.sort(key=lambda case: (case["result"] != "fail", case["id"]))
    failed = sum(1 for case in cases if case["result"] == "fail")
    summary = f"케이스 {len(cases)}개 · 실패 {failed} · 통과 {sum(1 for case in cases if case['result'] == 'pass')}"
    if args.check:
        print(f"검사 통과: {summary}")
        return 0
    output = args.root / "index.html"
    output.write_text(template.replace(SLOT, "".join(case_html(case) for case in cases)), encoding="utf-8")
    print(f"보고서: {output} — {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
