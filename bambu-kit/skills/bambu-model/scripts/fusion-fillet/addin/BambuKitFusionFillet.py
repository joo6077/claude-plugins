# fillet-job.sh 가 깔아 두면 퓨전이 켜질 때 한 번 돈다. 작업 파일의 STEP 마다 새 문서로 열어 모든 모서리를 둥글리고
# (큰 반지름부터 실패하면 한 단계씩 줄인다) STL · 네 방향 그림을 낸다. 끝 표시는 <out_dir>/fillet-job.log 의 DONE · FAIL 줄
# 부품에 "step" 대신 "join": [바탕, 붙일 것…] 을 주면 붙일 것만 둥글린 뒤 바탕과 합치고, 새로 생긴 이음매 모서리만 seam_radii 로 둥글린다
# 합치기 근거 (2026-11-09 Codex 공식 문서 확인): TemporaryBRepManager.copy · BRepBody.pointContainment(PointOnPointContainment) ·
#   CombineFeatures.createInput + JoinFeatureOperation · 직접 모델링에서 bRepBodies.add(임시 몸체) · 단위 cm
# API 근거 (2026-11-08 Codex 확인): createSTEPImportOptions · importToNewDocument · filletFeatures.createInput ·
#   edgeSetInputs.addConstantRadiusEdgeSet(엔티티, ValueInput, 접선연쇄) — 옛 addConstantRadiusEdgeSet 은 폐기 ·
#   createSTLExportOptions + meshRefinement · viewport.camera 는 복사본이라 고친 뒤 다시 대입 · saveAsImageFile · document.close(False)
import adsk.core, adsk.fusion, hashlib, json, math, os, threading, time, traceback

HERE = os.path.dirname(os.path.abspath(__file__))
EVENT_ID = "BambuKitFusionFilletReady"
handlers = []
VIEWS = {"iso": (1.0, -1.0, 0.8), "front": (0.0, -1.0, 0.05), "side": (1.0, 0.0, 0.05), "top": (0.0, -0.001, 1.0)}


def load_job():
    with open(os.path.join(HERE, "job-path.txt"), encoding="utf-8") as path_file:
        job_path = path_file.read().strip()
    with open(job_path, encoding="utf-8") as job_file:
        return json.load(job_file)


def append_log(job, text):
    with open(os.path.join(job["out_dir"], "fillet-job.log"), "a", encoding="utf-8") as log_file:
        log_file.write(time.strftime("%H:%M:%S ") + text + "\n")


def fillet_all(component, body, radii):
    """몸체의 모든 모서리를 한 번에 둥글린다. 실패(None 또는 예외)하면 다음 반지름. 성공한 반지름 또는 None."""
    return fillet_edges(component, list(body.edges), radii)


def fillet_edges(component, edge_list, radii):
    """주어진 모서리들을 한 번에 둥글린다. 실패하면 다음 반지름. 성공한 반지름 또는 None."""
    for radius in radii:
        try:
            edges = adsk.core.ObjectCollection.create()
            for edge in edge_list:
                edges.add(edge)
            fillet_input = component.features.filletFeatures.createInput()
            edge_set = fillet_input.edgeSetInputs.addConstantRadiusEdgeSet(
                edges, adsk.core.ValueInput.createByString(f"{radius} mm"), True)
            if edge_set and component.features.filletFeatures.add(fillet_input):
                return radius
        except Exception:
            pass
    return None


def fillet_each(design, edge_list, radii):
    """한꺼번에 실패하면 모서리를 하나씩 — 모서리마다 큰 반지름부터 시도. 앞선 둥글리기로 사라진 모서리는 건너뛴다. (성공 수, 전체 수)."""
    tokens = [edge.entityToken for edge in edge_list]
    done = 0
    for token in tokens:
        found = design.findEntityByToken(token)
        if not found:
            continue
        edge = found[0]
        for radius in radii:
            try:
                edges = adsk.core.ObjectCollection.create()
                edges.add(edge)
                fillet_input = edge.body.parentComponent.features.filletFeatures.createInput()
                if fillet_input.edgeSetInputs.addConstantRadiusEdgeSet(edges, adsk.core.ValueInput.createByString(f"{radius} mm"), True) \
                        and edge.body.parentComponent.features.filletFeatures.add(fillet_input):
                    done += 1
                    break
            except Exception:
                pass
    return done, len(tokens)


def finish(design, component, edge_list, radii):
    """한꺼번에 둥글리고, 안 되면 하나씩. 기록에 적을 값(반지름 또는 「하나씩 성공/전체」)."""
    used = fillet_edges(component, edge_list, radii)
    if used is None:
        count, total = fillet_each(design, edge_list, radii)
        used = f"하나씩 {count}/{total}"
    return used


def all_bodies(component):
    return list(component.bRepBodies) + [b for occ in component.allOccurrences for b in occ.bRepBodies]


def largest(bodies):
    return max(bodies, key=lambda b: b.volume)


def is_tangent(edge, point, limit_deg=5.0):
    """모서리 양쪽 면의 법선이 거의 같으면(이미 매끈하게 이어짐) True. 이런 모서리는 퓨전이 둥글리지 못해 한꺼번에 둥글리기를 망친다."""
    faces = list(edge.faces)
    if len(faces) != 2:
        return False
    normals = []
    for face in faces:
        ok, normal = face.evaluator.getNormalAtPoint(point)
        if not ok:
            return False
        normals.append(normal)
    return normals[0].angleTo(normals[1]) < math.radians(limit_deg)


def seam_edges(body, base, tools):
    """합친 몸체에서 가운데 점이 바탕 표면과 붙인 것 하나의 표면 위에 함께 있는 모서리 — 합치면서 새로 생긴 이음매다.
    (꺾인 이음매, 이미 매끈한 이음매 수)."""
    on = adsk.fusion.PointContainment.PointOnPointContainment
    found, smooth = [], 0
    for edge in body.edges:
        ok, start, end = edge.evaluator.getParameterExtents()
        if not ok:
            continue
        ok, middle = edge.evaluator.getPointAtParameter((start + end) / 2)
        if ok and base.pointContainment(middle) == on and any(tool.pointContainment(middle) == on for tool in tools):
            if is_tangent(edge, middle):
                smooth += 1
            else:
                found.append(edge)
    return found, smooth


def join_part(app, part):
    """바탕 STEP 을 새 문서로 열고 붙일 STEP 들을 같은 문서에 들인다. 직접 모델링으로 바꿔 몸체 사본을 한 컴포넌트에 모으고,
    붙일 몸체만 둥글린 뒤 바탕과 합쳐 이음매 모서리만 다시 둥글린다. (문서, 디자인, 결과 몸체, 기록 문자열).
    STEP 하나에 몸체가 여럿이면(면으로만 맞닿아 떨어진 조각 등) 모두 쓴다 — 바탕은 첫 STEP 의 가장 큰 몸체, 나머지는 전부 붙일 것.
    가장 큰 것만 쓰면 조각이 조용히 사라진다(2026-11-09 실측)."""
    paths = part["join"]
    manager = app.importManager
    document = manager.importToNewDocument(manager.createSTEPImportOptions(paths[0]))
    design = adsk.fusion.Design.cast(document.products.itemByProductType("DesignProductType"))
    root = design.rootComponent
    groups = [all_bodies(root)]
    for path in paths[1:]:
        before = {body.entityToken for body in all_bodies(root)}
        manager.importToTarget(manager.createSTEPImportOptions(path), root)
        groups.append([body for body in all_bodies(root) if body.entityToken not in before])
    if any(not group for group in groups):
        raise RuntimeError(f"몸체가 없는 STEP 이 있다: {[len(group) for group in groups]}")
    temp = adsk.fusion.TemporaryBRepManager.get()
    base_body = largest(groups[0])
    base_copy = temp.copy(base_body)
    rest_copies = [temp.copy(b) for b in groups[0] if b.entityToken != base_body.entityToken]
    tool_copies = [temp.copy(b) for group in groups[1:] for b in group]
    design.designType = adsk.fusion.DesignTypes.DirectDesignType
    for occurrence in list(root.occurrences):
        occurrence.deleteMe()
    for body in list(root.bRepBodies):
        body.deleteMe()
    base = root.bRepBodies.add(base_copy)
    for copy in rest_copies:
        root.bRepBodies.add(copy)
    added = [root.bRepBodies.add(copy) for copy in tool_copies]
    tool_used = finish(design, root, [edge for body in added for edge in body.edges], part.get("radii", [3.0, 2.5, 2.0, 1.5, 1.0]))
    tool_bodies = [b for b in root.bRepBodies if b.entityToken != base.entityToken]
    base_original = temp.copy(base)
    tool_originals = [temp.copy(b) for b in tool_bodies]
    tools = adsk.core.ObjectCollection.create()
    for body in tool_bodies:
        tools.add(body)
    combine = root.features.combineFeatures.createInput(base, tools)
    combine.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
    root.features.combineFeatures.add(combine)
    merged = largest(list(root.bRepBodies))
    edges, smooth = seam_edges(merged, base_original, tool_originals)
    if not edges and not smooth:
        raise RuntimeError("이음매 모서리 0 개 — 두 몸체가 닿지 않는다")
    seam_used = finish(design, root, edges, part.get("seam_radii", [3.0, 2.5, 2.0, 1.5, 1.0])) if edges else "없음"
    merged = largest(list(root.bRepBodies))
    return document, design, merged, f"fillet={tool_used} seam={len(edges)} seam_smooth={smooth} seam_fillet={seam_used}"


def save_views(app, body, prefix):
    box = body.boundingBox
    center = adsk.core.Point3D.create((box.minPoint.x + box.maxPoint.x) / 2, (box.minPoint.y + box.maxPoint.y) / 2,
                                      (box.minPoint.z + box.maxPoint.z) / 2)
    viewport = app.activeViewport
    try:
        app.userInterface.activeSelections.clear()   # 화면 그림에 선택 표시(노란 면)가 남지 않게
    except Exception:
        pass
    for name, (dx, dy, dz) in VIEWS.items():
        camera = viewport.camera
        camera.target = center
        camera.eye = adsk.core.Point3D.create(center.x + dx * 50, center.y + dy * 50, center.z + dz * 50)
        camera.upVector = adsk.core.Vector3D.create(0, 1, 0) if name == "top" else adsk.core.Vector3D.create(0, 0, 1)
        camera.isFitView = True
        viewport.camera = camera
        adsk.doEvents()
        viewport.saveAsImageFile(f"{prefix}_{name}.png", 1000, 1000)


class ReadyHandler(adsk.core.CustomEventHandler):
    def notify(self, args):
        app = adsk.core.Application.get()
        job = None
        try:
            job = load_job()
            for part in job["parts"]:
                append_log(job, f"열기 {part['name']}")
                if "join" in part:
                    document, design, body, note = join_part(app, part)
                else:
                    document = app.importManager.importToNewDocument(app.importManager.createSTEPImportOptions(part["step"]))
                    design = adsk.fusion.Design.cast(document.products.itemByProductType("DesignProductType"))
                    component = design.rootComponent
                    bodies = list(component.bRepBodies) or [b for occ in component.allOccurrences for b in occ.bRepBodies]
                    body = bodies[0]
                    radii = part.get("radii", [3.0, 2.5, 2.0, 1.5, 1.0])
                    used = fillet_all(body.parentComponent, body, radii)
                    if used is None:
                        count, total = fillet_each(design, list(body.edges), radii)
                        used = f"하나씩 {count}/{total}"
                    body = (list(body.parentComponent.bRepBodies) or [body])[0]
                    note = f"fillet={used}"
                prefix = os.path.join(job["out_dir"], part["name"])
                exporter = design.exportManager
                options = exporter.createSTLExportOptions(body, prefix + ".stl")
                options.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
                exporter.execute(options)
                save_views(app, body, prefix)
                append_log(job, f"PART {part['name']} {note}")
                document.close(False)
            append_log(job, "DONE")
        except Exception:
            if job and "out_dir" in job:
                append_log(job, "FAIL\n" + traceback.format_exc())


def wait_for_startup(app):
    for _ in range(600):
        if app.isStartupComplete:
            break
        time.sleep(1)
    time.sleep(5)
    append_log(load_job(), f"시작 완료={app.isStartupComplete} — 작업 신호")
    app.fireCustomEvent(EVENT_ID)


def run(context):
    job = None
    try:
        job = load_job()
        os.makedirs(job["out_dir"], exist_ok=True)
        with open(os.path.abspath(__file__), "rb") as source_file:
            digest = hashlib.sha256(source_file.read()).hexdigest()[:16]
        append_log(job, f"추가 기능 시작 ADDIN sha256={digest}")
        app = adsk.core.Application.get()
        event = app.registerCustomEvent(EVENT_ID)
        handler = ReadyHandler()
        event.add(handler)
        handlers.append(handler)
        threading.Thread(target=wait_for_startup, args=(app,), daemon=True).start()
    except Exception:
        if job and "out_dir" in job:
            append_log(job, "FAIL\n" + traceback.format_exc())


def stop(context):
    try:
        adsk.core.Application.get().unregisterCustomEvent(EVENT_ID)
    except Exception:
        pass
