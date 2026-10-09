"""예시 TC-003 을 복사해 시나리오 1 단계 1 에 at 없는 조작을 하나 더한다 — 접힌 조작과 좌표 없는 조작을 브라우저로 확인할 때 쓴다.

사용: python3 fold_fixture.py <예시 폴더> <출력 폴더>   (출력 폴더/TC-003-fold 를 새로 만든다)
"""
import json
import shutil
import sys
from pathlib import Path

source, out = Path(sys.argv[1]), Path(sys.argv[2])
shutil.rmtree(out, ignore_errors=True)
target = out / "TC-003-fold"
shutil.copytree(source / "TC-003-shot-strip", target)
(target / "index.html").unlink()
record = json.loads((target / "record.json").read_text(encoding="utf-8"))
actions = record["scenarios"][0]["steps"][0]["do"]
actions.append({"act": "네 번째 조작", "shot": "02-picker.png"})
(target / "record.json").write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{target} — 조작 {len(actions)}개")
