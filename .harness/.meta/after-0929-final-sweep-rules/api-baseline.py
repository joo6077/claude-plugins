"""api-baseline.py <레포 폴더> — api-kit 예시 계약 users.me 의 baseline 블록을 스냅샷과 맞댄다.

한 줄: block=<0|1> state=<값> nd=<0|1> media=<0|1> mode=<0|1> lineage=<0|1> extra=[<SKILL §10 에 없는 열쇠>] others=<다른 네 계약 중 baseline 블록 있는 수>
종료 코드: 0 잼 · 2 파일을 못 읽음
"""
import json
import pathlib
import sys

import yaml

repo = pathlib.Path(sys.argv[1])
api = repo / "api-kit/evals/fixtures/unjudged/.api"
try:
    contract = yaml.safe_load((api / "contracts/users.me.yaml").read_text(encoding="utf-8"))
    manifest = json.loads((api / "snapshots/dev/users.me.json").read_text(encoding="utf-8"))["manifest"]
except (OSError, ValueError, KeyError) as error:
    print(f"STOP {error}")
    sys.exit(2)

ALLOWED = {"manifestDigest", "rawDigest", "normalizedDigest", "redactionRegistry", "mediaType",
           "extractionMode", "lineage", "state", "expiresAt"}
base = contract.get("baseline")
if not isinstance(base, dict):
    base = None
lineage = (base or {}).get("lineage") or {}
captured = lineage.get("capturedAt")
captured = captured.isoformat() if hasattr(captured, "isoformat") else str(captured)
others = 0
for name in ("auth.token", "orders.list", "products.inventory", "products.list"):
    other = yaml.safe_load((api / f"contracts/{name}.yaml").read_text(encoding="utf-8")) or {}
    others += "baseline" in other
print(" ".join([
    f"block={int(base is not None)}",
    f"state={(base or {}).get('state')}",
    f"nd={int((base or {}).get('normalizedDigest') == manifest.get('normalizedDigest'))}",
    f"media={int((base or {}).get('mediaType') == manifest.get('mediaType'))}",
    f"mode={int((base or {}).get('extractionMode') == contract.get('mode'))}",
    f"lineage={int(lineage.get('env') == manifest['lineage']['env'] and lineage.get('branch') == manifest['lineage']['branch'] and captured == manifest['capturedAt'])}",
    f"extra={sorted(set(base or {}) - ALLOWED)}",
    f"others={others}",
]))
