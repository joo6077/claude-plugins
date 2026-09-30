#!/usr/bin/env python3
"""설치본에서 못 여는 docs/ 경로 안내 검사 (B11).

쓰임: python3 b11-docs-guidance.py <레포 뿌리> [킷 ...]
  킷을 안 주면 marketplace 에 등록된 킷 열네 개를 모두 본다.

킷 파일(evals/ 아래 제외)에서 docs/ 경로 낱말을 찾아, 레포 뿌리 docs/<칸>/ 에만 있고
그 킷 안(<킷>/docs/<칸>) 에는 없는 경로를 「레포 전용」 으로 센다. 설치본 플러그인은 킷 폴더만
담으므로 레포 전용 경로는 설치본에서 열 수 없다.

줄 모양: <판정> <파일> dirs=<레포 전용 칸 목록>
  OK     — 레포 전용 칸마다 「설치본 플러그인에는」 · `docs/<칸>/` · raw 주소가 한 줄에 있다.
           그 칸을 ../ 로 적었으면 같은 줄에 `../` 도 있어야 한다 (떼고 붙이라는 안내)
  NEED   — 그런 줄이 빠진 칸이 하나 이상 있다 (missing=<칸>)
  EXEMPT — 아래 EXEMPT 표에 있는 파일 (사유를 함께 찍는다)
끝 줄: TOTAL files=<레포 전용 경로가 있는 파일 수> ok=<n> need=<n> exempt=<n>
종료 코드: 0 NEED 0 개 · 1 NEED 1 개 이상 · 2 git ls-files 실패
"""
import os, re, subprocess, sys

RAW = "https://raw.githubusercontent.com/joo6077/claude-plugins/main/"
DEFAULT_KITS = ["api-kit", "design-kit", "howto-kit", "planning-kit", "react-kit", "flutter-toolkit",
                "onboarding-kit", "reflect-kit", "tone-kit", "bambu-kit", "harness",
                "backend-kit", "rust-kit", "infra-kit"]
# 설치본 에이전트가 여는 안내가 아닌 파일 — 사유를 같이 적는다
EXEMPT = {
    "api-kit/README.md": "사람이 읽는 소개 — 에이전트가 여는 안내가 아니다",
    "howto-kit/README.md": "사람이 읽는 소개 — 에이전트가 여는 안내가 아니다",
    "planning-kit/README.md": "사람이 읽는 소개 — 에이전트가 여는 안내가 아니다",
    "react-kit/README.md": "사람이 읽는 소개 — 에이전트가 여는 안내가 아니다",
    "tone-kit/README.md": "사람이 읽는 소개 — 에이전트가 여는 안내가 아니다",
    "harness/README.md": "사람이 읽는 소개 — 에이전트가 여는 안내가 아니다",
    "backend-kit/README.md": "사람이 읽는 소개 — 에이전트가 여는 안내가 아니다",
    "rust-kit/README.md": "사람이 읽는 소개 — 에이전트가 여는 안내가 아니다",
    "infra-kit/README.md": "사람이 읽는 소개 — 에이전트가 여는 안내가 아니다",
    "harness/docs/guides/contract-design-guide.md": "docs/react/kit-design/ 는 조건 예시 글자다 — 열라는 안내가 아니다",
    "harness/docs/guides/qa-evaluation-guide.md": "docs/react/kit-design/ 는 지난 REJECT 기록 글자다 — 열라는 안내가 아니다",
    "harness/docs/guides/plugin-validation-guide.md": "레포 검증 도구가 재는 폴더 목록이다 — 레포 안에서만 쓴다",
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
TOKEN = re.compile(r"(?<![A-Za-z0-9_./-])((?:\.\./)*docs/[A-Za-z0-9_-]+(?:/[A-Za-z0-9_.-]*)*)")


def main():
    root = sys.argv[1]
    kits = sys.argv[2:] or DEFAULT_KITS
    os.chdir(root)
    try:
        tracked = set(subprocess.check_output(["git", "ls-files"], text=True).splitlines())
    except Exception:
        print("STOP git ls-files 실패")
        return 2
    dirs = {os.path.dirname(p) for p in tracked}
    folders = set()
    for d in dirs:
        while d:
            folders.add(d)
            d = os.path.dirname(d)

    def exists(path):
        path = path.rstrip("/")
        return path in tracked or path in folders

    n = ok = need = exempt = 0
    for f in sorted(p for p in tracked if p.split("/")[0] in kits and "/evals/" not in p):
        try:
            text = open(f, encoding="utf-8").read()
        except Exception:
            continue
        kit = f.split("/")[0]
        segs = set()
        rel = set()   # ../ 로 적은 칸 — 안내 줄이 「`../` 를 떼고」 를 함께 말해야 한다
        for m in TOKEN.finditer(text):
            p = m.group(1)
            if p.startswith("../"):
                full = os.path.normpath(os.path.join(os.path.dirname(f), p))
                if full.startswith("docs/") and not exists(os.path.join(kit, full)):
                    segs.add(full.split("/")[1])
                    rel.add(full.split("/")[1])
                continue
            seg = p.split("/")[1]
            if exists(os.path.join(kit, "docs", seg)):
                continue
            if exists(os.path.join("docs", seg)):
                segs.add(seg)
        if not segs:
            continue
        n += 1
        label = ",".join(sorted(segs))
        if f in EXEMPT:
            exempt += 1
            print(f"EXEMPT {f} dirs={label} — {EXEMPT[f]}")
            continue
        lines = [ln for ln in text.splitlines() if RAW in ln]
        def guided(s):
            hits = [ln for ln in lines if f"`docs/{s}/`" in ln and "설치본 플러그인에는" in ln]
            if s in rel:
                hits = [ln for ln in hits if "`../`" in ln]
            return bool(hits)
        missing = [s for s in sorted(segs) if not guided(s)]
        if missing:
            need += 1
            print(f"NEED {f} dirs={label} missing={','.join(missing)}")
        else:
            ok += 1
            print(f"OK {f} dirs={label}")
    print(f"TOTAL files={n} ok={ok} need={need} exempt={exempt}")
    return 1 if need else 0


if __name__ == "__main__":
    sys.exit(main())
