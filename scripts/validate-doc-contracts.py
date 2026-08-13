#!/usr/bin/env python3
"""validate-doc-contracts.py — 문서가 주장하는 스크립트 인터페이스를 실체와 대조한다.

## 왜 있는가 — 실측 (2026-08-13 · Phase 4 kaizen)

`.claude/skills/kaizen-orchestrator/SKILL.md` Step 0 은
`<repo>/.claude/kaizen-input/insights-report.md` 자동 탐색과 `--insights=PATH` 를 자유 서술로
주장했는데, `scripts/collect-kaizen-data.py` 에는 **둘 다 없었다**. 문서와 코드가 갈라진 채로
최소 한 사이클을 돌았고, 그동안 사람이 정리한 §0 델타 분석본이 데이터 풀에 들어가지 못했다.

## 어떻게 막는가

문서에 **기계가 읽는 선언 블록**을 두고, 그 선언을 스크립트의 **살아 있는 객체**와 대조한다.
자연어를 regex 로 추론하지 않는다 — 선언 블록만 파싱한다. 실체(argparse / 모듈 상수)가 SSOT 다.

문서 쪽 선언 블록 형식 (fenced ```yaml · 첫 줄이 `# docs-contract`):

    ```yaml
    # docs-contract
    script: scripts/collect-kaizen-data.py
    options: ["--hub-dir", "--insights", "--output", "--skip-validate"]
    input_candidates:
      - .claude/kaizen-input/insights-report.md
      - ~/.claude/kaizen-input/insights-report.md
      - ~/.claude/usage-data/report.html
    exit_codes: [0, 2]
    ```

스크립트 쪽은 `doc_contract() -> dict` 를 제공한다 (같은 키). 제공하지 않으면 `build_arg_parser()`
에서 `options` 만 유도하고, 선언에 있는 나머지 키는 **검증 불가**로 보고한다 —
검증 불가는 통과가 아니다.

## 종료 코드

harness/evals/gate-exit-codes.md 가 SSOT 다 (여기서 의미를 재정의하지 않는다).
이 스크립트는 0 · 1 · 2 · 3 을 쓴다.

사용법:
    python3 scripts/validate-doc-contracts.py [--verbose]
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml 이 설치되지 않았습니다. pip install pyyaml", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent

MARKER = "# docs-contract"
FENCE_RE = re.compile(r"^(?P<indent>[ \t]*)(?P<fence>`{3,}|~{3,})[ \t]*yaml[ \t]*$")

# 선언에서 검증 가능한 키. 여기 없는 키가 선언에 있으면 "알 수 없는 키" 로 보고한다.
KNOWN_KEYS = {"script", "options", "input_candidates", "exit_codes"}


class Finding:
    """한 건의 결과. kind 는 violation(정책 위반) 또는 error(검증 불가)."""

    def __init__(self, kind: str, where: str, message: str) -> None:
        self.kind = kind
        self.where = where
        self.message = message

    def __str__(self) -> str:
        tag = "VIOLATION" if self.kind == "violation" else "NOT-VERIFIABLE"
        return f"[{tag}] {self.where}: {self.message}"


def tracked_markdown() -> list[Path]:
    """git 이 추적하는 `.md` 파일 목록. git 이 없으면 검증 불가로 올린다."""
    proc = subprocess.run(
        ["git", "ls-files", "*.md"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git ls-files 실패 (rc={proc.returncode}): {proc.stderr.strip()}")
    return [REPO_ROOT / line for line in proc.stdout.splitlines() if line.strip()]


def extract_blocks(path: Path) -> list[tuple[int, str]]:
    """파일에서 `# docs-contract` 로 시작하는 yaml 펜스 블록을 뽑는다.

    여는 펜스와 같은 길이 이상의 닫는 펜스를 찾는다 — 나이브한 ``` 매칭은 중첩 펜스에서 깨진다.
    """
    blocks: list[tuple[int, str]] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        m = FENCE_RE.match(lines[i])
        if not m:
            i += 1
            continue
        fence = m.group("fence")
        closing = re.compile(r"^[ \t]*" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}[ \t]*$")
        j = i + 1
        body: list[str] = []
        while j < len(lines) and not closing.match(lines[j]):
            body.append(lines[j])
            j += 1
        if body and body[0].strip() == MARKER:
            blocks.append((i + 1, "\n".join(body)))
        i = j + 1
    return blocks


def load_module(script_rel: str):
    """선언이 가리키는 스크립트를 모듈로 로드한다."""
    script_path = REPO_ROOT / script_rel
    if not script_path.is_file():
        raise RuntimeError(f"선언이 가리키는 스크립트가 없다: {script_rel}")
    spec = importlib.util.spec_from_file_location(
        "doc_contract_target_" + re.sub(r"\W", "_", script_rel), script_path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"모듈 스펙을 만들 수 없다: {script_rel}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def actual_contract(module, script_rel: str) -> tuple[dict, list[str]]:
    """스크립트 실체에서 계약 값을 뽑는다. (값, 검증 불가 키 목록)"""
    if hasattr(module, "doc_contract"):
        return dict(module.doc_contract()), []
    if not hasattr(module, "build_arg_parser"):
        raise RuntimeError(
            f"{script_rel} 에 doc_contract() 도 build_arg_parser() 도 없다 — 대조할 실체가 없다"
        )
    parser = module.build_arg_parser()
    options = [
        opt
        for action in parser._actions  # noqa: SLF001 — argparse 의 공식 introspection 경로
        for opt in action.option_strings
        if opt not in ("-h", "--help")
    ]
    return {"script": script_rel, "options": sorted(options)}, [
        "input_candidates",
        "exit_codes",
    ]


def compare(where: str, declared: dict, actual: dict, unverifiable: list[str]) -> list[Finding]:
    findings: list[Finding] = []

    unknown = sorted(set(declared) - KNOWN_KEYS)
    if unknown:
        findings.append(Finding("violation", where, f"알 수 없는 선언 키: {unknown}"))

    for key in ("options", "input_candidates", "exit_codes"):
        if key not in declared:
            continue
        if key in unverifiable:
            findings.append(
                Finding(
                    "error",
                    where,
                    f"`{key}` 를 선언했지만 스크립트가 doc_contract() 로 노출하지 않아 대조할 수 없다",
                )
            )
            continue
        want = declared[key]
        got = actual.get(key)
        if key == "options":
            want, got = sorted(map(str, want)), sorted(map(str, got or []))
        elif key == "exit_codes":
            want, got = sorted(map(int, want)), sorted(map(int, got or []))
        else:  # input_candidates — 우선순위가 의미를 가지므로 순서를 유지한다
            want, got = list(map(str, want)), list(map(str, got or []))
        if want != got:
            findings.append(
                Finding(
                    "violation",
                    where,
                    f"`{key}` 불일치 — 문서 선언 {want} / 스크립트 실체 {got}",
                )
            )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="문서의 docs-contract 선언을 스크립트 실체와 대조한다",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="검사한 블록을 모두 출력")
    args = parser.parse_args()

    try:
        md_files = tracked_markdown()
    except RuntimeError as exc:
        print(f"NOT RUN: {exc}", file=sys.stderr)
        return 2

    findings: list[Finding] = []
    checked = 0

    for path in md_files:
        rel = path.relative_to(REPO_ROOT)
        try:
            blocks = extract_blocks(path)
        except OSError as exc:
            findings.append(Finding("error", str(rel), f"읽기 실패: {exc}"))
            continue
        for lineno, body in blocks:
            checked += 1
            where = f"{rel}:{lineno}"
            try:
                declared = yaml.safe_load(body) or {}
            except yaml.YAMLError as exc:
                findings.append(Finding("error", where, f"선언 블록 YAML 파싱 실패: {exc}"))
                continue
            if not isinstance(declared, dict) or "script" not in declared:
                findings.append(Finding("violation", where, "선언 블록에 `script` 키가 없다"))
                continue
            script_rel = str(declared["script"])
            try:
                module = load_module(script_rel)
                actual, unverifiable = actual_contract(module, script_rel)
            except Exception as exc:  # 로드 실패는 "위반 0 건" 이 아니라 "검증 못 함" 이다
                findings.append(Finding("error", where, f"실체 로드 실패: {exc}"))
                continue
            if args.verbose:
                print(f"  검사: {where} → {script_rel}")
            findings.extend(compare(where, declared, actual, unverifiable))

    n_violation = sum(1 for f in findings if f.kind == "violation")
    n_error = sum(1 for f in findings if f.kind == "error")

    for f in findings:
        print(str(f), file=sys.stderr if f.kind == "error" else sys.stdout)

    print(
        f"doc-contracts: {checked} 블록 검사 · violation {n_violation} · not-verifiable {n_error}"
    )

    if checked == 0:
        print(
            "NO DATA: docs-contract 선언 블록이 하나도 없다 — 검사 대상이 없었다 (exit 3)",
            file=sys.stderr,
        )
        return 3
    # 실행이 불완전하면 결과 집합을 완전한 분석으로 보고하지 않는다 (gate-exit-codes.md §규칙)
    if n_error:
        return 2
    if n_violation:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
