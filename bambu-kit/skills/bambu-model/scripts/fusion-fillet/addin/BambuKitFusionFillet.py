# fillet-job.sh 가 깔아 두면 퓨전이 켜질 때 한 번 돈다. 작업 파일의 STEP 마다 새 문서로 열어 모든 모서리를 둥글리고
# (큰 반지름부터 실패하면 한 단계씩 줄인다) STL · 네 방향 그림을 낸다. 끝 표시는 <out_dir>/fillet-job.log 의 DONE · FAIL 줄
# API 근거 (2026-11-08 Codex 확인): createSTEPImportOptions · importToNewDocument · filletFeatures.createInput ·
#   edgeSetInputs.addConstantRadiusEdgeSet(엔티티, ValueInput, 접선연쇄) — 옛 addConstantRadiusEdgeSet 은 폐기 ·
#   createSTLExportOptions + meshRefinement · viewport.camera 는 복사본이라 고친 뒤 다시 대입 · saveAsImageFile · document.close(False)
import adsk.core, adsk.fusion, json, os, threading, time, traceback

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
    for radius in radii:
        try:
            edges = adsk.core.ObjectCollection.create()
            for edge in body.edges:
                edges.add(edge)
            fillet_input = component.features.filletFeatures.createInput()
            edge_set = fillet_input.edgeSetInputs.addConstantRadiusEdgeSet(
                edges, adsk.core.ValueInput.createByString(f"{radius} mm"), True)
            if edge_set and component.features.filletFeatures.add(fillet_input):
                return radius
        except Exception:
            pass
    return None


def fillet_each(design, body, radii):
    """한꺼번에 실패하면 모서리를 하나씩 — 모서리마다 큰 반지름부터 시도. 앞선 둥글리기로 사라진 모서리는 건너뛴다. (성공 수, 전체 수)."""
    tokens = [edge.entityToken for edge in body.edges]
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
                document = app.importManager.importToNewDocument(app.importManager.createSTEPImportOptions(part["step"]))
                design = adsk.fusion.Design.cast(document.products.itemByProductType("DesignProductType"))
                component = design.rootComponent
                bodies = list(component.bRepBodies) or [b for occ in component.allOccurrences for b in occ.bRepBodies]
                body = bodies[0]
                radii = part.get("radii", [3.0, 2.5, 2.0, 1.5, 1.0])
                used = fillet_all(body.parentComponent, body, radii)
                if used is None:
                    count, total = fillet_each(design, body, radii)
                    used = f"하나씩 {count}/{total}"
                body = (list(body.parentComponent.bRepBodies) or [body])[0]
                prefix = os.path.join(job["out_dir"], part["name"])
                exporter = design.exportManager
                options = exporter.createSTLExportOptions(body, prefix + ".stl")
                options.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
                exporter.execute(options)
                save_views(app, body, prefix)
                append_log(job, f"PART {part['name']} fillet={used}")
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
        append_log(job, "추가 기능 시작")
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
