#!/usr/bin/env python3
"""레포의 킷 내용과 설치본이 갈렸는지 본다.

설치본은 버전 번호로만 최신 여부를 판단한다. 그래서 레포에서 스킬을 고치고 커밋해도
plugin.json 의 버전이 그대로면 "이미 최신"으로 보고 내려받지 않는다. 그 상태가 조용히
쌓이면 사용자는 레포에 있는 개선을 못 받은 채 옛 스킬을 쓰게 된다 (2026-09-12 실측: 6개 킷).

이 검사는 CI 에서는 뜻이 없다 — 설치본이 없기 때문이다. 로컬 세션 시작 훅에서 쓴다.

종료 코드는 항상 0 이다. 알림이 목적이지 막는 것이 목적이 아니다.
"""
import hashlib
import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_ROOT = os.path.expanduser("~/.claude/plugins/cache/joo6077-plugins")
WATCHED_DIRS = ("skills", "agents")


def content_digest(base):
    """base 아래 마크다운·JSON 파일들의 내용을 한 값으로 접는다. 경로도 함께 센다."""
    digest = hashlib.sha256()
    for watched in WATCHED_DIRS:
        root = os.path.join(base, watched)
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames.sort()
            for filename in sorted(filenames):
                if not filename.endswith((".md", ".json")):
                    continue
                path = os.path.join(dirpath, filename)
                digest.update(os.path.relpath(path, base).encode())
                try:
                    with open(path, "rb") as handle:
                        digest.update(handle.read())
                except OSError:
                    digest.update(b"<unreadable>")
    return digest.hexdigest()[:16]


def kits():
    for name in sorted(os.listdir(REPO_ROOT)):
        manifest = os.path.join(REPO_ROOT, name, ".claude-plugin", "plugin.json")
        if not os.path.isfile(manifest):
            continue
        try:
            with open(manifest, encoding="utf-8") as handle:
                version = json.load(handle).get("version")
        except Exception:
            continue
        if version:
            yield name, version


def main():
    drifted = []
    for name, version in kits():
        installed = os.path.join(CACHE_ROOT, name, version)
        if not os.path.isdir(installed):
            continue  # 미설치이거나 다른 버전을 쓰는 중 — 이 검사의 대상이 아니다
        if content_digest(os.path.join(REPO_ROOT, name)) != content_digest(installed):
            drifted.append((name, version))

    if not drifted:
        return 0

    print("[킷 동기화] 레포 내용이 설치본보다 앞선 킷이 있습니다 — 버전이 같아서 갱신이 걸리지 않습니다.")
    for name, version in drifted:
        print(f"  - {name} v{version}")
    first = drifted[0][0]
    print(f"  해소: bash scripts/release.sh {first} patch  → PR 머지 → "
          f"claude plugin update {first}@joo6077-plugins")
    return 0


if __name__ == "__main__":
    sys.exit(main())
