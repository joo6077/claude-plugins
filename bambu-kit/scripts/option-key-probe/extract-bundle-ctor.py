#!/usr/bin/env python3
"""태그의 PresetBundle.cpp 에서 기본 생성자와 그것이 쓰는 파일 내부 정의만 원문 그대로 잘라낸다.

usage: extract-bundle-ctor.py <PresetBundle.cpp> <출력 .cpp>

PresetBundle.cpp 전체는 Model.hpp → OpenCASCADE 까지 끌어오지만 생성자는 Model 을 쓰지 않는다.
손으로 옮겨 적으면 슬라이서 버전이 바뀔 때 조용히 어긋나므로, 반드시 원문에서 괄호 짝으로 자른다."""
import pathlib
import re
import sys

source = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
out = pathlib.Path(sys.argv[2])


def block_from(start):
    """start 이후 첫 '{' 부터 짝이 맞는 '}' 까지. 문자열·문자 리터럴·주석 안의 괄호는 세지 않는다"""
    cursor = source.index("{", start)
    depth = 0
    while cursor < len(source):
        char = source[cursor]
        if source.startswith("//", cursor):
            cursor = source.index("\n", cursor)
            continue
        if source.startswith("/*", cursor):
            cursor = source.index("*/", cursor) + 2
            continue
        if char in "\"'":
            end = cursor + 1
            while source[end] != char:
                end += 2 if source[end] == "\\" else 1
            cursor = end + 1
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return source[start:cursor + 1]
        cursor += 1
    raise SystemExit("괄호 짝이 안 맞는다")


pieces = []
match = re.search(r"^static std::vector<std::string> s_project_options\s*\{", source, re.M)
if not match:
    raise SystemExit("s_project_options 정의를 못 찾았다")
pieces.append(block_from(match.start()) + ";")
# PresetBundle 의 정적 문자열 상수 정의 — 다른 소스(Preset.cpp)가 참조하므로 전부 가져온다
pieces += re.findall(r"^const (?:char ?\*|std::string) ?PresetBundle::[A-Za-z_]+\s*=.*;$", source, re.M)
match = re.search(r"^PresetBundle::PresetBundle\(\)\s*$", source, re.M)
if not match:
    raise SystemExit("기본 생성자를 못 찾았다")
pieces.append(block_from(match.start()))

out.write_text(
    "// 자동 생성 — " + sys.argv[1] + " 에서 원문 그대로 잘라냈다. 손으로 고치지 마라\n"
    '#include "libslic3r/PresetBundle.hpp"\n#include "libslic3r/PrintConfig.hpp"\n'
    "namespace Slic3r {\n" + "\n\n".join(pieces) + "\n} // namespace Slic3r\n", encoding="utf-8")
print(f"잘라냄 {out} · 조각 {len(pieces)}개 · {sum(piece.count(chr(10)) for piece in pieces)} 줄")
