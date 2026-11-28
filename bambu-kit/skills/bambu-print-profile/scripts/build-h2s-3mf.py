"""다른 프린터(P1S · X1C 등)용으로 저장된 제작자 3mf 를 H2S 3mf 로 바꾼다 — 형상은 그대로, 프로젝트 설정만 H2S 것으로.
usage: python3 build-h2s-3mf.py <제작자.3mf> <H2S 템플릿.3mf> <process.json> "<필라멘트 시스템 이름>" <출력.3mf>
  H2S 템플릿 : 뱀부 스튜디오에서 H2S 로 저장한 아무 3mf. 프린터 설정(시작 명령 등)을 여기서 가져온다
  process   : 이 킷이 만든 process JSON. 시스템 부모 사슬을 펼친 값 위에 이 파일 값을 덮는다
  필라멘트   : 시스템 이름 그대로 (예: "Bambu PLA Wood @BBL H2S"). 부모 사슬을 펼쳐 모든 소재 칸에 넣는다
값 박기 블록(SKILL.md Phase 4.4)은 process · filament 키만 박아서 프린터를 못 바꾼다 — 그때 이 스크립트를 쓴다.
부품 위치는 H2S 판 가운데(170, 160)로 옮기고 회전 · 높이는 제작자 값을 둔다."""
import sys, json, re, zipfile, pathlib

if len(sys.argv) != 6:
    sys.exit(__doc__)
creator, template, process_path, filament_name, out = sys.argv[1:]
PROFILES = pathlib.Path("/Applications/BambuStudio.app/Contents/Resources/profiles/BBL")
META = {"type", "name", "version", "from", "inherits", "print_settings_id", "filament_settings_id", "printer_settings_id",
        "compatible_printers", "compatible_printers_condition", "filament_extruder_variant", "instantiation", "setting_id",
        "filament_id", "description", "renamed_from"}
PLATE_CENTER = "170 160"


def load_index():
    index = {}
    for kind in ("process", "filament"):
        for path in (PROFILES / kind).glob("*.json"):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except ValueError:
                continue
            if "name" in data:
                index[(kind, data["name"])] = data
    return index


def resolve(index, kind, name, depth=0):
    """시스템 프로파일 부모 사슬을 펼친다 (BBL 제조사 폴더 안에서만 찾는다)."""
    if (kind, name) not in index:
        if depth == 0:
            sys.exit(f"FAIL 시스템 {kind} 프로파일 {name!r} 이 {PROFILES / kind} 에 없다")
        return {}
    if depth > 12:
        sys.exit(f"FAIL {kind} {name!r} 부모 사슬이 12 단을 넘는다")
    data = index[(kind, name)]
    merged = dict(resolve(index, kind, data["inherits"], depth + 1)) if data.get("inherits") else {}
    merged.update(data)
    return merged


def put(project, key, value, skipped):
    """프로젝트 칸 수에 맞춰 값을 넣는다. 한 값이면 모든 칸에 채운다."""
    if key in META or key.startswith("_"):
        return
    if key not in project:
        skipped.append(key)
        return
    if not isinstance(project[key], list):
        project[key] = value[0] if isinstance(value, list) else value
        return
    cells, width = (value if isinstance(value, list) else [value]), len(project[key])
    if len(cells) == width:
        project[key] = list(cells)
    elif len(set(cells)) == 1:
        project[key] = [cells[0]] * width
    else:
        project[key] = [cells[i % len(cells)] for i in range(width)]


with zipfile.ZipFile(template) as archive:
    project = json.loads(archive.read("Metadata/project_settings.config"))
printer = str(project.get("printer_settings_id", ""))
if "H2S" not in printer:
    sys.exit(f"FAIL 템플릿 프린터가 H2S 가 아니다: {printer!r} — 뱀부 스튜디오에서 H2S 로 저장한 3mf 를 템플릿으로 준다")

preset = json.loads(pathlib.Path(process_path).read_text(encoding="utf-8"))
if preset.get("type") != "process" or not preset.get("inherits"):
    sys.exit(f"FAIL {process_path} 는 inherits 가 있는 process JSON 이어야 한다")
index = load_index()
process_values = resolve(index, "process", preset["inherits"])
filament_values = resolve(index, "filament", filament_name)
process_values.update(preset)

skipped = []
for key, value in process_values.items():
    put(project, key, value, skipped)
slots = len(project["filament_settings_id"])
for key, value in filament_values.items():
    put(project, key, value, skipped)
project["print_settings_id"] = preset["name"]
project["filament_settings_id"] = [filament_name] * slots

with zipfile.ZipFile(creator) as source:
    names = source.namelist()
    if "3D/3dmodel.model" not in names:
        sys.exit(f"FAIL {creator} 에 3D/3dmodel.model 이 없다")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as target:
        for entry in source.infolist():
            data = source.read(entry.filename)
            if entry.filename == "Metadata/project_settings.config":
                data = json.dumps(project, indent=4).encode("utf-8")
            elif entry.filename == "3D/3dmodel.model":
                # build item 변환 12 수 중 마지막 3 개가 위치다 — x · y 만 판 가운데로 바꾼다
                data = re.sub(r'(<item [^>]*transform="(?:\S+ ){9})\S+ \S+', rf"\g<1>{PLATE_CENTER}", data.decode("utf-8")).encode("utf-8")
            target.writestr(entry, data)
print(f"OK {out} · 프린터 {printer} · process {preset['name']} · 필라멘트 {filament_name} × {slots} 칸 · "
      f"프로젝트에 없어 건너뛴 키 {len(set(skipped))} 개")
