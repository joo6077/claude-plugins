#!/usr/bin/env python3
"""설치본에서 못 여는 레포 뿌리 docs/ 경로에 raw 주소 안내가 붙어 있는지 검사한다.

쓰임: python3 scripts/check-install-docs-guidance.py   (레포 어디서 불러도 된다)

설치본 플러그인은 킷 폴더만 담는다. 킷 파일이 레포 뿌리 `docs/<칸>/` 를 가리키면 설치본 에이전트는
그 경로를 열 수 없다. 그런 칸마다 같은 파일 안에 한 줄로 「설치본 플러그인에는」 · `docs/<칸>/` ·
raw 주소가 있어야 하고, `../` 로 적은 칸이면 그 줄에 `../` 도 있어야 한다(떼고 붙이라는 안내).
킷 안(`<킷>/docs/<칸>/`)에 있는 경로는 설치본에서 열리므로 대상이 아니다. evals/ 아래는 보지 않는다.

출력: 빠진 파일마다 `NEED <파일> missing=<칸>` 줄, 못 읽은 파일마다 `UNREADABLE <파일> (<까닭>)` 줄,
끝 줄 `TOTAL files=<n> ok=<n> need=<n> exempt=<n> unreadable=<n>`
종료 코드: 0 빠진 것 없음 · 1 빠진 파일 있음 · 2 git ls-files 실패 또는 킷 파일을 못 읽음 (1 보다 앞선다)
"""
import os
import re
import subprocess
import sys

RAW = "https://raw.githubusercontent.com/joo6077/claude-plugins/main/"
# 설치본 에이전트가 여는 안내가 아닌 파일 — 사유를 같이 적는다
EXEMPT = {
    "api-kit/README.md": "사람이 읽는 소개",
    "howto-kit/README.md": "사람이 읽는 소개",
    "planning-kit/README.md": "사람이 읽는 소개",
    "react-kit/README.md": "사람이 읽는 소개",
    "tone-kit/README.md": "사람이 읽는 소개",
    "harness/README.md": "사람이 읽는 소개",
    "backend-kit/README.md": "사람이 읽는 소개",
    "rust-kit/README.md": "사람이 읽는 소개",
    "infra-kit/README.md": "사람이 읽는 소개",
    "harness/docs/guides/contract-design-guide.md": "docs/react/kit-design/ 는 조건 예시 글자다",
    "harness/docs/guides/qa-evaluation-guide.md": "docs/react/kit-design/ 는 지난 REJECT 기록 글자다",
    "harness/docs/guides/plugin-validation-guide.md": "레포 검증 도구가 재는 폴더 목록 — 레포 안에서만 쓴다",
    "harness/references/contract-schema.md": "docs/react · docs/flutter · docs/kaizen 은 조건 예시 · 기록 글자다",
    "harness/skills/contract-kaizen/SKILL.md": "이 레포를 고치는 카이젠 — 작업 폴더가 레포라 docs/kaizen/ 이 열린다",
    "harness/skills/contract-kaizen/references/search-sources.md": "위와 같은 카이젠 참고",
    "harness/skills/evaluator-kaizen/SKILL.md": "이 레포를 고치는 카이젠 — 작업 폴더가 레포라 docs/kaizen/ 이 열린다",
    "harness/skills/evaluator-kaizen/references/search-sources.md": "위와 같은 카이젠 참고",
    "harness/skills/harness-kaizen/SKILL.md": "이 레포를 고치는 카이젠 — 작업 폴더가 레포라 docs/kaizen/ 이 열린다",
    "harness/skills/harness-kaizen/references/search-sources.md": "위와 같은 카이젠 참고",
    "flutter-toolkit/skills/flutter-kaizen/SKILL.md": "이 레포를 고치는 카이젠 — 작업 폴더가 레포라 docs/kaizen/ 이 열린다",
    "flutter-toolkit/skills/flutter-kaizen/references/search-sources.md": "위와 같은 카이젠 참고",
}
DOCS_PATH = re.compile(r"(?<![A-Za-z0-9_./-])((?:\.\./)*docs/[A-Za-z0-9_-]+(?:/[A-Za-z0-9_.-]*)*)")


def repo_only_dirs(path, text, kit, is_tracked):
    """레포 뿌리에만 있는 docs 칸 전부와, 그중 ../ 로 적은 칸을 돌려준다."""
    dirs, relative_dirs = set(), set()
    for match in DOCS_PATH.finditer(text):
        ref = match.group(1)
        if ref.startswith("../"):
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), ref))
            if resolved.startswith("docs/") and not is_tracked(os.path.join(kit, resolved)):
                dirs.add(resolved.split("/")[1])
                relative_dirs.add(resolved.split("/")[1])
            continue
        dir_name = ref.split("/")[1]
        if not is_tracked(os.path.join(kit, "docs", dir_name)) and is_tracked(os.path.join("docs", dir_name)):
            dirs.add(dir_name)
    return dirs, relative_dirs


def main():
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    try:
        tracked = set(subprocess.check_output(["git", "ls-files"], text=True).splitlines())
    except (OSError, subprocess.CalledProcessError):
        print("STOP git ls-files 실패")
        return 2
    folders = set()
    for tracked_path in tracked:
        folder = os.path.dirname(tracked_path)
        while folder:
            folders.add(folder)
            folder = os.path.dirname(folder)

    def is_tracked(path):
        return path.rstrip("/") in tracked or path.rstrip("/") in folders

    kits = sorted({manifest.split("/")[0] for manifest in tracked
                   if manifest.endswith("/.claude-plugin/plugin.json") and manifest.count("/") == 2})
    total = ok = need = exempt = unreadable = 0
    for path in sorted(candidate for candidate in tracked
                       if candidate.split("/")[0] in kits and "/evals/" not in candidate):
        try:
            text = open(path, encoding="utf-8").read()
        except UnicodeDecodeError as error:
            # 그림 같은 바이너리만 건너뛴다. 글자 파일을 못 읽고 넘기면 안내가 빠져도 통과한다
            with open(path, "rb") as handle:
                if b"\0" in handle.read():
                    continue
            unreadable += 1
            print(f"UNREADABLE {path} ({error})")
            continue
        except OSError as error:
            unreadable += 1
            print(f"UNREADABLE {path} ({error.strerror})")
            continue
        dirs, relative_dirs = repo_only_dirs(path, text, path.split("/")[0], is_tracked)
        if not dirs:
            continue
        total += 1
        if path in EXEMPT:
            exempt += 1
            continue
        guide_lines = [line for line in text.splitlines() if RAW in line and "설치본 플러그인에는" in line]

        def guided(dir_name):
            hits = [line for line in guide_lines if f"`docs/{dir_name}/`" in line]
            if dir_name in relative_dirs:
                hits = [line for line in hits if "`../`" in line]
            return bool(hits)

        missing = [dir_name for dir_name in sorted(dirs) if not guided(dir_name)]
        if missing:
            need += 1
            print(f"NEED {path} missing={','.join(missing)}")
        else:
            ok += 1
    print(f"TOTAL files={total} ok={ok} need={need} exempt={exempt} unreadable={unreadable}")
    if need:
        print(f"안내 줄 모양: 설치본 플러그인에는 `docs/<칸>/` 가 없다 — … `{RAW}` 뒤에 … 붙여 읽고, 그래도 못 읽으면 … 못 읽었다고 적는다.")
    if unreadable:
        return 2
    return 1 if need else 0


if __name__ == "__main__":
    sys.exit(main())
