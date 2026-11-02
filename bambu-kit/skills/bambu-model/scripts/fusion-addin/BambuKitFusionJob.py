# fusion-job.sh 가 깔아 두면 퓨전이 켜질 때 한 번 돈다. 작업 파일대로 f3d 를 열어 매개변수를 바꾸고 보이는 몸체마다 STL 과 크기 · 작은 원통 구멍을 남긴다
# 작업 파일 경로는 옆의 job-path.txt 에 있다. 끝 표시는 <out_dir>/fusion-job.log 의 DONE · FAIL 줄이다
import adsk.core, adsk.fusion, json, os, re, threading, time, traceback

HERE = os.path.dirname(os.path.abspath(__file__))
EVENT_ID = "BambuKitFusionJobReady"
handlers = []


def load_job():
    with open(os.path.join(HERE, "job-path.txt"), encoding="utf-8") as path_file:
        job_path = path_file.read().strip()
    with open(job_path, encoding="utf-8") as job_file:
        return json.load(job_file)


def append_log(job, text):
    with open(os.path.join(job["out_dir"], "fusion-job.log"), "a", encoding="utf-8") as log_file:
        log_file.write(time.strftime("%H:%M:%S ") + text + "\n")


def file_safe(name):
    return re.sub(r"[^0-9A-Za-z가-힣_-]+", "_", name).strip("_")


def visible_bodies(design):
    root = design.rootComponent
    owners = [(root.name, root.bRepBodies)] + [(occurrence.fullPathName, occurrence.bRepBodies) for occurrence in root.allOccurrences]
    for owner, bodies in owners:
        for body in bodies:
            if body.isVisible:
                yield owner, body


def hole_lines(body, label, limit_mm):
    """지름이 limit_mm 미만인 원통 면마다 지름 · 축 방향 길이 · 축을 적는다. 퓨전 내부 단위는 cm 다."""
    lines = []
    for face in body.faces:
        geometry = face.geometry
        if geometry.surfaceType != adsk.core.SurfaceTypes.CylinderSurfaceType:
            continue
        diameter = geometry.radius * 20
        if diameter >= limit_mm:
            continue
        axis = geometry.axis
        axis.normalize()
        along = [(vertex.geometry.x * axis.x + vertex.geometry.y * axis.y + vertex.geometry.z * axis.z) * 10 for vertex in face.vertices]
        length = (max(along) - min(along)) if along else float("nan")
        lines.append(f"HOLE d={diameter:.2f} len={length:.2f} axis=({axis.x:.2f},{axis.y:.2f},{axis.z:.2f}) body={label}")
    return lines


class ReadyHandler(adsk.core.CustomEventHandler):
    def notify(self, args):
        app = adsk.core.Application.get()
        job = None
        try:
            job = load_job()
            append_log(job, "원본 열기")
            document = app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(job["source"]))
            design = adsk.fusion.Design.cast(document.products.itemByProductType("DesignProductType"))
            append_log(job, "원본 열림")
            report = []
            for name, expression in job.get("params", {}).items():
                parameter = design.userParameters.itemByName(name)
                if parameter is None:
                    report.append(f"WARN 매개변수 없음 {name}")
                    continue
                parameter.expression = expression
                report.append(f"PARAM {name}={parameter.expression}")
            exporter = design.exportManager
            for owner, body in visible_bodies(design):
                label = f"{owner}/{body.name}"
                box = body.boundingBox
                size = [(box.maxPoint.x - box.minPoint.x) * 10, (box.maxPoint.y - box.minPoint.y) * 10, (box.maxPoint.z - box.minPoint.z) * 10]
                report.append(f"BODY {label} {size[0]:.1f}x{size[1]:.1f}x{size[2]:.1f}")
                report += hole_lines(body, label, float(job.get("holes_under_mm", 40)))
                stl_path = os.path.join(job["out_dir"], f"{file_safe(owner)}__{file_safe(body.name)}.stl")
                exporter.execute(exporter.createSTLExportOptions(body, stl_path))
            with open(os.path.join(job["out_dir"], "report.txt"), "w", encoding="utf-8") as report_file:
                report_file.write("\n".join(report) + "\n")
            document.close(False)
            append_log(job, "DONE")
        except Exception:
            if job and "out_dir" in job:
                append_log(job, "FAIL\n" + traceback.format_exc())


def wait_for_startup(app):
    # 로그인 창이 떠 있으면 isStartupComplete 가 늦게 선다. 선 뒤에도 문서를 바로 열면 실패해서 몇 초 더 기다린다
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
