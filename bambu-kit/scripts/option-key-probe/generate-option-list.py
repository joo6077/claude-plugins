#!/usr/bin/env python3
"""판정 프로그램으로 슬라이서 버전별 옵션 목록(TSV)을 만든다.

usage: generate-option-list.py <option_key_probe> <태그 소스 루트> <출력 .tsv>

줄 형식 (탭 구분, 정렬해서 결정적으로 출력):
  canonical     <키>                     JSON 을 불러올 때 그대로 받아들여지는 키 (등록부에 있어도 무시 목록이면 빠진다)
  renamed       <옛 키> <새 키>          불러올 때 이름이 바뀌어 들어간다
  process|filament|machine <키>          그 종류 기본 프리셋에 있는 키. 설정 가져오기는 여기 없는 키를 지운다
  enum          <키> <값>                enum 옵션이 받아들이는 값
  header        <키>                     옵션이 아니라 불러오기가 따로 읽는 파일 머리 키 (name · version · filament_id …)
  renamed-value <키> <옛 값> <새 값>      불러올 때 값이 바뀌어 들어간다. <키> 는 파일에 적힌 원래 키다 (옛 키 포함)

옛 이름은 슬라이서 소스에 전수 목록이 없다. 그래서 후보를 넓게 모아 슬라이서 함수로 판정한다:
옛 이름 처리 함수(handle_legacy) 안의 문자열 리터럴 전부 + 두 슬라이서 번들 프로파일의 키와 값.
번들 프로파일은 이 맥에 설치된 앱에서 읽으므로, 앱 버전이 바뀌면 후보가 달라져 옛 이름 줄이 늘 수 있다."""
import json
import pathlib
import re
import subprocess
import sys

probe, source_root, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3])
PROFILE_ROOTS = ["/Applications/OrcaSlicer.app/Contents/Resources/profiles",
                 "/Applications/BambuStudio.app/Contents/Resources/profiles"]


def run(mode, stdin=""):
    result = subprocess.run([str(probe), mode], input=stdin, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f"{probe} {mode} 실패: {result.stderr[:300]}")
    return [line.split("\t") for line in result.stdout.splitlines() if line]


rows = set()
canonical, enums = set(), {}
for kind, *rest in run("dump"):
    if kind == "canonical":
        canonical.add(rest[0])
    elif kind == "enum":
        enums.setdefault(rest[0], set()).add(rest[1])
        rows.add(("enum", rest[0], rest[1]))
for kind, key in run("presets"):
    rows.add((kind, key))

# 파일 머리 키 — 소스의 *_JSON_KEY_* 정의. load_from_json 이 옵션과 따로 읽으므로 "모르는 키" 가 아니다
for header_file in (source_root / "src/libslic3r").rglob("*.h*"):
    text = header_file.read_text(encoding="utf-8", errors="replace")
    for key in re.findall(r'#define [A-Z_]*JSON_KEY_[A-Z_]+\s+"([A-Za-z_]+)"', text):
        rows.add(("header", key))

print_config = (source_root / "src/libslic3r/PrintConfig.cpp").read_text(encoding="utf-8")
start = print_config.index("void PrintConfigDef::handle_legacy(t_config_option_key &opt_key, std::string &value)")
legacy_body = print_config[start:start + 60000].split("\nvoid PrintConfigDef::handle_legacy_composite")[0]
legacy_literals = set(re.findall(r'"([^"\\\\\n]{1,80})"', legacy_body))
candidate_keys, candidate_values = set(legacy_literals), set(legacy_literals)
for root in PROFILE_ROOTS:
    for profile_path in pathlib.Path(root).rglob("*.json"):
        try:
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(profile, dict):
            continue
        for key, value in profile.items():
            candidate_keys.add(key)
            for item in (value if isinstance(value, list) else [value]):
                if isinstance(item, str) and len(item) <= 80 and "\n" not in item:
                    candidate_values.add(item)
for values in enums.values():
    candidate_values |= values

renamed = {}
key_lines = sorted(key for key in candidate_keys | canonical if re.fullmatch(r"[A-Za-z0-9_]+", key))
for verdict, key, *rest in run("classify", "\n".join(key_lines)):
    if verdict == "accepted" and key in canonical:
        rows.add(("canonical", key))
    elif verdict == "renamed":
        renamed[key] = rest[0]
        rows.add(("renamed", key, rest[0]))

# 값 판정은 슬라이서 함수에 키·값을 함께 넣는다 — 옛 키가 바뀔 때 값도 같이 바뀌는 경우가 있다 (wall_infill_order)
value_keys = set(enums) | {old for old, new in renamed.items() if new in enums}
pairs = [f"{key}\t{value}" for key in sorted(value_keys) for value in sorted(candidate_values | {"nil"}) if "\t" not in value]
for verdict, key, value, new_key, new_value in run("values", "\n".join(pairs)):
    if verdict != "accepted":
        continue
    target = new_key or key
    if new_value != value:
        rows.add(("renamed-value", key, value, new_value))
    elif value == "nil" and target in enums:
        rows.add(("enum", target, "nil"))      # 재정의 옵션의 "값 없음" 표시

counts = {}
for row in rows:
    counts[row[0]] = counts.get(row[0], 0) + 1
# 판정 프로그램이 아무것도 안 내도 빈 목록이 써졌고, 게이트는 그 목록으로 키 검사를 건너뛰었다 — 쓰기 전에 멈춘다
empty = [kind for kind in ("canonical", "process", "filament", "machine", "enum") if not counts.get(kind)]
if empty:
    raise SystemExit(f"{out.name} 을 쓰지 않았다 — {', '.join(empty)} 줄이 0 개다. 판정 프로그램 출력부터 본다: {dict(sorted(counts.items()))}")
out.write_text("".join("\t".join(row) + "\n" for row in sorted(rows)), encoding="utf-8")
print(out.name, dict(sorted(counts.items())))
