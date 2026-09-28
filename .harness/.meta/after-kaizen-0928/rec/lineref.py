"""경고 정리 병합(c3e45f3 이후 다섯)으로 밀린 .harness 기록의 `파일:줄` 참조를 찾고, 고친 뒤 상태를 잰다.

    python3 lineref.py find  [--base 판]   → 밀린 참조 목록(TSV)을 표준 출력으로
    python3 lineref.py check [--base 판]   → 같은 목록을 작업 폴더와 대조해 어긋난 줄만 출력, 끝에 요약 한 줄
    python3 lineref.py scope --tip 판      → 기준 판과 끝 판 사이 .harness 변경이 목록 줄 · 허용 새 파일뿐인지
    python3 lineref.py files [--base 판]   → 계약마다 정정 파일이 하나씩 있고 모양과 행 수가 맞는지

git 개체만 읽으므로 find 결과는 작업 폴더 상태와 무관하다. 저장소 뿌리에서 부른다.
"""
import argparse
import difflib
import os
import re
import subprocess
import sys

PRE_LINT = "c3e45f3"
LINT_END = "f51bd6e"
LINT_MERGES = ["31859e2", "b8f0995", "ac4def3", "4cc2e61", "f51bd6e"]
DEFAULT_BASE = "e500a63"

# 끝에 숫자·점이 이어지면 소수나 판 번호라 참조가 아니다
REF_RE = re.compile(r"([A-Za-z0-9_./@-]*[A-Za-z0-9_-]\.[A-Za-z0-9]+):(\d+)(?:[-–~](\d+))?(?![0-9.])")
CONDITION_RE = re.compile(r"^- \[[ x]\] [A-Z]{2,}-[0-9]{2}")
RECORD_EXT = (".md", ".yaml", ".yml", ".txt")
# 이 묶음이 새로 쓰는 기록은 대상이 아니다
OWN_PREFIX = ".harness/.meta/after-kaizen-0928/"


HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def hunk_numbers(head):
    """-U0 조각 머리의 (옛 시작, 옛 줄 수, 새 시작, 새 줄 수). 줄 수가 빠지면 1 이다."""
    old_start, old_count, new_start, new_count = head.groups()
    return int(old_start), int(old_count or 1), int(new_start), int(new_count or 1)


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def git_ok(*args):
    return subprocess.run(["git", *args], capture_output=True).returncode == 0


def full(rev):
    return git("rev-parse", rev).strip()


class LineMap:
    """한 파일의 두 판 사이 -U0 조각으로 옛 줄 번호를 새 줄 번호로 옮긴다."""

    def __init__(self, old_rev, new_rev, path):
        self.old = git("show", f"{old_rev}:{path}").split("\n")
        self.new = git("show", f"{new_rev}:{path}").split("\n")
        self.hunks = []
        for line in git("diff", "-U0", "--no-color", old_rev, new_rev, "--", path).split("\n"):
            head = HUNK_RE.match(line)
            if head:
                self.hunks.append(hunk_numbers(head))

    def move(self, old_no):
        """(새 줄 번호, 'moved' | 'changed' | 'deleted' | 'out')"""
        if old_no < 1 or old_no > len(self.old):
            return old_no, "out"
        shift = 0
        for old_start, old_count, new_start, new_count in self.hunks:
            if old_count == 0:
                if old_no > old_start:
                    shift += new_count
                    continue
                break
            if old_no < old_start:
                break
            if old_no < old_start + old_count:
                if new_count == 0:
                    return new_start + 1, "deleted"
                src = self.old[old_no - 1].strip()
                # 줄이 고쳐진 조각이면 새 줄 가운데 글자가 가장 닮은 줄로 보낸다
                best = max(range(new_start, new_start + new_count),
                           key=lambda cand: difflib.SequenceMatcher(None, src, self.new[cand - 1].strip()).ratio())
                return best, "changed"
            shift += new_count - old_count
        return old_no + shift, "moved"


class Finder:
    def __init__(self, base):
        self.base = full(base)
        self.pre = full(PRE_LINT)
        self.merges = [(full(m), full(m + "^1"), full(m + "^2")) for m in LINT_MERGES]
        self.pre_ancestors = set(git("rev-list", self.pre).split())
        self.targets = set()
        for merge, first, _ in self.merges:
            for row in git("diff", "--name-status", first, merge).splitlines():
                status, path = row.split("\t")[0], row.split("\t")[-1]
                if status == "M":
                    self.targets.add(path)
        self.tracked_pre = git("ls-tree", "-r", "--name-only", self.pre).splitlines()
        self.maps = {}
        self.view_cache = {}

    def linemap(self, old_rev, path):
        key = (old_rev, path)
        if key not in self.maps:
            self.maps[key] = (LineMap(old_rev, self.base, path), LineMap(old_rev, full(LINT_END), path) if old_rev == self.pre else None)
        return self.maps[key]

    def resolve(self, token):
        token = token[2:] if token.startswith("./") else token
        if token in self.targets:
            return token
        if "/" in token:
            # 절대 경로는 뒤쪽이 저장소 경로와 같으면, 상대 경로는 저장소 경로의 뒤쪽과 같으면 같은 파일이다
            rooted = token.startswith(("/", "~"))
            hits = [path for path in self.tracked_pre if (rooted and token.endswith("/" + path)) or path.endswith("/" + token)]
        else:
            hits = [path for path in self.tracked_pre if os.path.basename(path) == token]
        if len(hits) == 1 and hits[0] in self.targets:
            return hits[0]
        return None

    def view_of(self, commit):
        """참조가 가리키는 대상 판. None 이면 경고 정리가 이 참조 뒤에 대상을 바꾸지 않았다."""
        if commit not in self.view_cache:
            if commit in self.pre_ancestors:
                self.view_cache[commit] = (self.pre, None)
            else:
                later = [m for m, _, second in self.merges if not git_ok("merge-base", "--is-ancestor", second, commit)]
                touched = set()
                for merge in later:
                    touched |= set(git("diff", "--name-only", merge + "^1", merge).split())
                self.view_cache[commit] = (commit, touched) if later else (None, None)
        return self.view_cache[commit]

    def records(self):
        for path in git("ls-tree", "-r", "--name-only", self.base, "--", ".harness").splitlines():
            if path.endswith(RECORD_EXT) and not path.startswith(OWN_PREFIX):
                yield path

    def blame(self, path):
        commits, current = [], None
        for line in git("blame", "--porcelain", self.base, "--", path).split("\n"):
            head = re.match(r"^([0-9a-f]{40}) \d+ \d+", line)
            if head:
                current = head.group(1)
            elif line.startswith("\t"):
                commits.append(current)
        return commits

    def rows(self):
        for record in self.records():
            text = git("show", f"{self.base}:{record}").split("\n")
            if not any(REF_RE.search(line) for line in text):
                continue
            zones = contract_zones(text) if "sprint-contract" in os.path.basename(record) else None
            commits = None
            for no, line in enumerate(text, 1):
                for match in REF_RE.finditer(line):
                    target = self.resolve(match.group(1))
                    if not target:
                        continue
                    if commits is None:
                        commits = self.blame(record)
                    view, touched = self.view_of(commits[no - 1])
                    if view is None or (touched is not None and target not in touched):
                        continue
                    row = self.row(record, no, match, target, view, zones)
                    if row:
                        yield row

    def row(self, record, no, match, target, view, zones):
        try:
            to_base, to_lint_end = self.linemap(view, target)
        except subprocess.CalledProcessError:
            return None
        ends = [int(match.group(2))] + ([int(match.group(3))] if match.group(3) else [])
        moved = [to_base.move(end) for end in ends]
        if any(kind == "out" for _, kind in moved):
            return None
        if to_lint_end is not None:
            if all(to_lint_end.move(end)[0] == end for end in ends):
                return None
        elif all(new == end for (new, _), end in zip(moved, ends)):
            return None
        old_ref = match.group(0)
        sep = old_ref[len(match.group(1)) + 1 + len(match.group(2)):][:1] if match.group(3) else ""
        new_ref = f"{match.group(1)}:{moved[0][0]}" + (f"{sep}{moved[1][0]}" if match.group(3) else "")
        kind = "moved" if all(state == "moved" for _, state in moved) else next(state for _, state in moved if state != "moved")
        zone = zones[no - 1] if zones else "record"
        return [record, str(no), old_ref, new_ref, target, kind, zone, view[:7]]


def contract_zones(text):
    """계약 줄마다 봉인이 덮는 자리: condition(조건 줄) · measure(그 아래 들여쓴 줄) · prose(그 밖)."""
    zones, in_block = [], False
    for line in text:
        if CONDITION_RE.match(line):
            zones.append("condition")
            in_block = True
        elif in_block and re.match(r"^[ \t]+[^ \t]", line):
            zones.append("measure")
        elif in_block and re.match(r"^[ \t]*$", line):
            zones.append("prose")
        else:
            zones.append("prose")
            in_block = False
    return zones


def lineref_path(record):
    return os.path.join(os.path.dirname(record), os.path.basename(record).replace("sprint-contract", "sprint-lineref", 1))


def listed_in(side, no, old_ref, new_ref):
    if not os.path.exists(side):
        return False
    for row in open(side, encoding="utf-8").read().split("\n"):
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")] if row.lstrip().startswith("|") else []
        if len(cells) >= 3 and cells[0] == no and cells[1] == f"`{old_ref}`" and cells[2] == f"`{new_ref}`":
            return True
    return False


def expected_line(base_line, swaps):
    """옛 줄에서 참조 토큰 자리만 새 참조로 바꾼 줄. 토큰 경계로 바꾸므로 `x.md:9` 가 `x.md:95` 를 건드리지 않는다."""
    return REF_RE.sub(lambda ref: swaps.get(ref.group(0), ref.group(0)), base_line)


def check(rows, base):
    """조건 · 측정 줄은 그대로 두고 정정 파일에, 계약 본문 줄은 직접 고치고 정정 파일에도, 그 밖 기록은 직접 고친다."""
    swaps, base_text = {}, {}
    for record, no, old_ref, new_ref, *_ in rows:
        swaps.setdefault((record, no), {})[old_ref] = new_ref
    bad, fixed_in_place, fixed_by_file = 0, 0, 0
    for record, no, old_ref, new_ref, target, kind, zone, view in rows:
        if record not in base_text:
            base_text[record] = git("show", f"{base}:{record}").split("\n")
        before = base_text[record][int(no) - 1]
        lines = open(record, encoding="utf-8").read().split("\n")
        line = lines[int(no) - 1] if int(no) <= len(lines) else ""
        listed = zone != "record" and listed_in(lineref_path(record), no, old_ref, new_ref)
        if zone in ("condition", "measure"):
            reason = None if line == before and listed else ("missing-in-lineref-file" if line == before else "sealed-line-edited")
        else:
            edited = line == expected_line(before, swaps[(record, no)])
            if zone == "prose":
                reason = None if edited and listed else ("missing-in-lineref-file" if edited else "not-fixed-in-place")
            else:
                reason = None if edited else "not-fixed-in-place"
        if reason is None:
            if zone in ("condition", "measure"):
                fixed_by_file += 1
            else:
                fixed_in_place += 1
            continue
        bad += 1
        print("\t".join([reason, record, no, old_ref, new_ref]))
    print(f"SUMMARY rows={len(rows)} in_place={fixed_in_place} lineref_file={fixed_by_file} bad={bad}")
    return 1 if bad else 0


# 이 묶음이 새로 만들 수 있는 .harness 파일
NEW_FILE_RE = re.compile(r"^\.harness/((history/)?[^/]*sprint-lineref[^/]*\.md"
                         r"|sprint-(contract|feedback|amendments)-after-0928-record-fixes\.md"
                         r"|\.meta/after-kaizen-0928/.*)$")


def scope(rows, base, tip):
    """기준 판에 있던 .harness 파일은 목록의 record · prose 줄만 바뀌었는가. 새 파일은 정해진 이름뿐인가."""
    allowed = {(r[0], int(r[1])) for r in rows if r[6] in ("record", "prose")}
    bad = 0
    for row in git("diff", "--name-status", "--no-renames", base, tip, "--", ".harness").splitlines():
        status, path = row.split("\t")[0], row.split("\t")[-1]
        problems = []
        if status == "A":
            if not NEW_FILE_RE.match(path):
                problems.append("new-file-outside-allowed-names")
        elif status != "M":
            problems.append(f"status-{status}")
        else:
            for line in git("diff", "-U0", "--no-color", base, tip, "--", path).split("\n"):
                head = HUNK_RE.match(line)
                if not head:
                    continue
                old_start, old_count, _, new_count = hunk_numbers(head)
                if old_count != new_count:
                    problems.append(f"line-count-changed@{old_start}")
                problems += [f"line-not-in-list@{no}" for no in range(old_start, old_start + old_count) if (path, no) not in allowed]
        for problem in problems:
            bad += 1
            print("\t".join([problem, path]))
    print(f"SUMMARY scope_bad={bad}")
    return 1 if bad else 0


LINEREF_TABLE_HEAD = "| 계약 줄 | 옛 참조 | 새 참조 | 대상 파일 | 처리 |"


def files(rows, base):
    """정정 파일이 계약마다 하나씩, 정해진 머리 · 표 머리 · 기준 판 · 목록 행 수를 갖췄는가."""
    want = {}
    for row in rows:
        if row[6] != "record":
            want[row[0]] = want.get(row[0], 0) + 1
    found = set(subprocess.run(["find", ".harness", "-type", "f", "-name", "*sprint-lineref*.md"],
                               capture_output=True, text=True, check=True).stdout.split())
    problems = [f"extra\t{path}" for path in sorted(found - {lineref_path(c) for c in want})]
    for contract, count in sorted(want.items()):
        path = lineref_path(contract)
        if path not in found:
            problems.append(f"missing\t{path}")
            continue
        text = open(path, encoding="utf-8").read().split("\n")
        data_rows = [line for line in text if re.match(r"^\| [0-9]+ \|", line)]
        if text[0] != f"# 줄 번호 정정 — {os.path.basename(contract)}":
            problems.append(f"title\t{path}")
        if LINEREF_TABLE_HEAD not in text:
            problems.append(f"table-head\t{path}")
        if not any(base[:7] in line for line in text):
            problems.append(f"base-commit\t{path}")
        if len(data_rows) != count:
            problems.append(f"row-count-{len(data_rows)}-of-{count}\t{path}")
    for problem in problems:
        print(problem)
    print(f"SUMMARY files_expected={len(want)} files_found={len(found)} bad={len(problems)}")
    return 1 if problems else 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["find", "check", "scope", "files"])
    parser.add_argument("--base", default=DEFAULT_BASE)
    parser.add_argument("--tip")
    args = parser.parse_args()
    rows = list(Finder(args.base).rows())
    if args.mode == "find":
        for row in rows:
            print("\t".join(row))
        return 0
    if args.mode == "scope":
        if not args.tip:
            print("scope 는 --tip 이 필요하다 (HEAD 를 짐작하지 않는다)", file=sys.stderr)
            return 2
        return scope(rows, full(args.base), full(args.tip))
    if args.mode == "files":
        return files(rows, full(args.base))
    return check(rows, full(args.base))


if __name__ == "__main__":
    sys.exit(main())
