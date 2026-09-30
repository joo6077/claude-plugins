"""경고 정리 병합(c3e45f3 이후 다섯)으로 밀린 .harness 기록의 줄 참조를 찾고, 고친 뒤 상태를 잰다 (2 회차).

    python3 lineref.py find  [--base 판]   → 밀린 참조 목록(TSV)을 표준 출력으로
    python3 lineref.py check [--base 판]   → 같은 목록을 작업 폴더와 대조해 어긋난 행만 출력, 끝에 요약 한 줄
    python3 lineref.py scope --tip 판      → 기준 판과 끝 판 사이 .harness 변경이 목록 줄 · 허용 새 파일뿐인지
    python3 lineref.py files [--base 판]   → 정정 파일 · 사람 확인 목록이 목록과 행 단위로 맞는지

1 회차와 다른 점: 파일 이름 없이 앞 참조에 이어 붙은 번호(`a.md:194` · `:212`)와 범위 끝 번호
(`a.md:1089`~`:1097`)도 참조로 세고, 줄이 고쳐진(changed) 참조는 같은 기록 줄의 인용문으로 새 줄을 고르거나
사람 확인 목록으로 돌린다. git 개체만 읽으므로 find 결과는 작업 폴더 상태와 무관하다. 저장소 뿌리에서 부른다.
"""
import argparse
import collections
import difflib
import os
import re
import subprocess
import sys

PRE_LINT = "c3e45f3"
LINT_END = "f51bd6e"
LINT_MERGES = ["31859e2", "b8f0995", "ac4def3", "4cc2e61", "f51bd6e"]
DEFAULT_BASE = "e500a63"

# 끝에 숫자·점이 이어지면 소수나 판 번호라 참조가 아니다. 범위 끝은 `12-14` · `12`~`:14` 둘 다 받는다
NUMBERS = r"(\d+)(?:`?[-–~]`?:?(\d+))?(?![0-9.])"
FULL_RE = re.compile(r"([A-Za-z0-9_./@-]*[A-Za-z0-9_-]\.[A-Za-z0-9]+):" + NUMBERS)
# 앞 참조 바로 뒤에 구분자만 두고 이어진 번호. 앞 참조의 파일을 물려받는다
CHAIN_RE = re.compile(r"`?[ ]*(?:·|,|/|및|와|과)?[ ]*`?:" + NUMBERS)
QUOTE_RE = re.compile(r"`([^`]+)`|「([^」]+)」")
CONDITION_RE = re.compile(r"^- \[[ x]\] [A-Z]{2,}-[0-9]{2}")
RECORD_EXT = (".md", ".yaml", ".yml", ".txt")
# 이 묶음이 새로 쓰는 기록은 대상이 아니다
OWN_PREFIX = ".harness/.meta/after-kaizen-0928/"
REVIEW_FILE = ".harness/.meta/after-kaizen-0928/rec-review.md"
REVIEW_TABLE_HEAD = "| 기록 | 줄 | 옛 참조 | 후보 참조 | 대상 파일 | 인용 |"
LINEREF_TABLE_HEAD = "| 계약 줄 | 옛 참조 | 새 참조 | 대상 파일 | 처리 |"

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


def line_tokens(line):
    """줄의 참조 토큰: (토큰 시작, 토큰 끝, 쓰인 경로, 번호 자리 목록). 번호 자리는 (시작, 끝, 값)."""
    tokens = []
    for match in FULL_RE.finditer(line):
        if tokens and match.start() < tokens[-1][1]:
            continue
        path = match.group(1)
        tokens.append((match.start(), match.end(), path, number_slots(match, 2)))
        end = match.end()
        while True:
            chained = CHAIN_RE.match(line, end)
            if not chained:
                break
            tokens.append((line.index(":", chained.start()), chained.end(), path, number_slots(chained, 1)))
            end = chained.end()
    return tokens


def number_slots(match, first):
    """first 는 첫 번호 묶음 번호. 범위 끝은 바로 다음 묶음이다."""
    slots = [(match.start(first), match.end(first), int(match.group(first)))]
    if match.group(first + 1) is not None:
        slots.append((match.start(first + 1), match.end(first + 1), int(match.group(first + 1))))
    return slots


def shown(line, start, end, slots, values):
    """표에 적을 참조 글자: 토큰 원문에서 백틱을 빼고 번호 자리만 values 로 바꾼 것."""
    text = line[start:end]
    for (slot_start, slot_end, _), value in sorted(zip(slots, values), reverse=True):
        text = text[:slot_start - start] + str(value) + text[slot_end - start:]
    return text.replace("`", "")


def quotes_in(line):
    """참조 · 번호가 아닌 네 글자 이상 인용문."""
    found = []
    for match in QUOTE_RE.finditer(line):
        text = (match.group(1) or match.group(2)).strip()
        if len(text) >= 4 and not FULL_RE.search(text) and not re.fullmatch(r":[0-9`~–-]+", text):
            found.append(text)
    return found


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
            if not any(FULL_RE.search(line) for line in text):
                continue
            zones = contract_zones(text) if "sprint-contract" in os.path.basename(record) else None
            commits = None
            for no, line in enumerate(text, 1):
                for start, end, path, slots in line_tokens(line):
                    target = self.resolve(path)
                    if not target:
                        continue
                    if commits is None:
                        commits = self.blame(record)
                    view, touched = self.view_of(commits[no - 1])
                    if view is None or (touched is not None and target not in touched):
                        continue
                    row = self.row(record, no, line, start, end, slots, target, view, zones)
                    if row:
                        yield row

    def row(self, record, no, line, start, end, slots, target, view, zones):
        try:
            to_base, to_lint_end = self.linemap(view, target)
        except subprocess.CalledProcessError:
            return None
        olds = [value for _, _, value in slots]
        moved = [to_base.move(value) for value in olds]
        if any(kind == "out" for _, kind in moved):
            return None
        if to_lint_end is not None:
            if all(to_lint_end.move(value)[0] == value for value in olds):
                return None
        elif all(new == value for (new, _), value in zip(moved, olds)):
            return None
        news = [new for new, _ in moved]
        # 범위는 끝 두 줄만이 아니라 사이 줄까지 본다. 사이에 끼어든 줄은 괜찮고 고쳐지거나 지워진 줄이 있으면 changed 다
        states = [state for _, state in moved] + [to_base.move(value)[1] for value in range(olds[0] + 1, olds[-1])]
        kind = "moved" if all(state == "moved" for state in states) else next(state for state in states if state != "moved")
        if kind == "changed":
            news, kind = self.by_quote(line, to_base, olds, news)
        zone = zones[no - 1] if zones else "record"
        return [record, str(no), ",".join(str(slot_start) for slot_start, _, _ in slots), shown(line, start, end, slots, olds), shown(line, start, end, slots, news),
                target, kind, zone, view[:7]]

    @staticmethod
    def by_quote(line, to_base, olds, news):
        """줄이 고쳐진 참조: 옛 줄에 있던 인용문이 새 줄에도 있어야 인용이 참으로 남는다."""
        old_block = to_base.old[olds[0] - 1:olds[-1]]
        held = [quote for quote in quotes_in(line) if any(quote in text for text in old_block)]
        if not held:
            return news, "changed"
        if len(olds) == 2:
            new_block = to_base.new[news[0] - 1:news[-1]]
            ok = all(any(quote in text for text in new_block) for quote in held)
            return (news, "quoted") if ok else (news, "unresolved")
        hits = [no for no, text in enumerate(to_base.new, 1) if all(quote in text for quote in held)]
        if not hits:
            return news, "unresolved"
        return [min(hits, key=lambda no: abs(no - news[0]))], "quoted"


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


def table_rows(path, width):
    if not os.path.exists(path):
        return []
    rows = []
    for text in open(path, encoding="utf-8").read().split("\n"):
        if text.lstrip().startswith("|") and not re.match(r"^\|[ -|]*$", text):
            cells = [cell.strip() for cell in text.strip().strip("|").split("|")]
            if len(cells) >= width:
                rows.append(cells)
    return rows


def lineref_key(row):
    return (row[1], f"`{row[3]}`", f"`{row[4]}`")


def review_key(row):
    return (f"`{row[0]}`", row[1], f"`{row[3]}`", f"`{row[4]}`")


def ref_numbers(ref):
    return re.findall(r"\d+", ref[ref.index(":"):])


def expected_line(base_line, rows):
    """옛 줄에서 번호 자리만 새 번호로 바꾼 줄. 사람 확인으로 돌린 행은 옛 번호 그대로다."""
    edits = []
    for row in rows:
        if row[6] == "unresolved":
            continue
        for position, old, new in zip(map(int, row[2].split(",")), ref_numbers(row[3]), ref_numbers(row[4])):
            edits.append((position, position + len(old), new))
    for start, end, new in sorted(edits, reverse=True):
        base_line = base_line[:start] + new + base_line[end:]
    return base_line


def check(rows, base):
    """조건 · 측정 줄은 그대로 두고 정정 파일에, 계약 본문 줄은 직접 고치고 정정 파일에도, 그 밖 기록은 직접 고친다.
    사람 확인으로 돌린 행은 옛 번호를 두고 사람 확인 목록에 적는다."""
    by_line, base_text = {}, {}
    for row in rows:
        by_line.setdefault((row[0], row[1]), []).append(row)
    review = {tuple(cells[:4]) for cells in table_rows(REVIEW_FILE, 6)}
    listed_cache = {}
    bad, fixed_in_place, fixed_by_file, sent_to_review = 0, 0, 0, 0
    for row in rows:
        record, no, _, old_ref, new_ref, target, kind, zone, view = row
        if record not in base_text:
            base_text[record] = git("show", f"{base}:{record}").split("\n")
        if record not in listed_cache:
            listed_cache[record] = {tuple(cells[:3]) for cells in table_rows(lineref_path(record), 5)} if zone != "record" or "sprint-contract" in os.path.basename(record) else set()
        before = base_text[record][int(no) - 1]
        lines = open(record, encoding="utf-8").read().split("\n")
        line = lines[int(no) - 1] if int(no) <= len(lines) else ""
        sealed = zone in ("condition", "measure")
        want = before if sealed else expected_line(before, by_line[(record, no)])
        if line != want:
            reason = "sealed-line-edited" if sealed else "not-fixed-in-place"
        elif kind == "unresolved":
            reason = None if review_key(row) in review else "missing-in-review-file"
        elif zone == "record":
            reason = None
        else:
            reason = None if lineref_key(row) in listed_cache[record] else "missing-in-lineref-file"
        if reason is None:
            if kind == "unresolved":
                sent_to_review += 1
            elif sealed:
                fixed_by_file += 1
            else:
                fixed_in_place += 1
            continue
        bad += 1
        print("\t".join([reason, record, no, old_ref, new_ref]))
    print(f"SUMMARY rows={len(rows)} in_place={fixed_in_place} lineref_file={fixed_by_file} review={sent_to_review} bad={bad}")
    return 1 if bad else 0


# 이 묶음이 새로 만들 수 있는 .harness 파일
NEW_FILE_RE = re.compile(r"^\.harness/((history/)?[^/]*sprint-lineref[^/]*\.md"
                         r"|sprint-(contract|feedback|amendments)-after-0928-record-fixes(-r2)?\.md"
                         r"|\.meta/after-kaizen-0928/.*)$")


def scope(rows, base, tip):
    """기준 판에 있던 .harness 파일은 목록의 record · prose 줄만 바뀌었는가. 새 파일은 정해진 이름뿐인가."""
    allowed = {(r[0], int(r[1])) for r in rows if r[7] in ("record", "prose")}
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


def files(rows, base):
    """정정 파일은 계약마다 하나씩 목록 행과 같은 행 집합을, 사람 확인 목록은 unresolved 행과 같은 행 집합을 갖는가."""
    want = {}
    for row in rows:
        if row[7] != "record" and row[6] != "unresolved":
            want.setdefault(row[0], collections.Counter())[lineref_key(row)] += 1
    found = set(subprocess.run(["find", ".harness", "-type", "f", "-name", "*sprint-lineref*.md"],
                               capture_output=True, text=True, check=True).stdout.split())
    problems = [f"extra\t{path}" for path in sorted(found - {lineref_path(c) for c in want})]
    for contract, keys in sorted(want.items()):
        path = lineref_path(contract)
        if path not in found:
            problems.append(f"missing\t{path}")
            continue
        text = open(path, encoding="utf-8").read().split("\n")
        have = collections.Counter(tuple(cells[:3]) for cells in table_rows(path, 5) if re.fullmatch(r"[0-9]+", cells[0]))
        if text[0] != f"# 줄 번호 정정 — {os.path.basename(contract)}":
            problems.append(f"title\t{path}")
        if LINEREF_TABLE_HEAD not in text:
            problems.append(f"table-head\t{path}")
        if not any(base[:7] in line for line in text):
            problems.append(f"base-commit\t{path}")
        if have != keys:
            problems.append(f"rows-{sum((keys - have).values())}-missing-{sum((have - keys).values())}-extra\t{path}")
    review_want = collections.Counter(review_key(row) for row in rows if row[6] == "unresolved")
    review_have = collections.Counter(tuple(cells[:4]) for cells in table_rows(REVIEW_FILE, 6) if re.fullmatch(r"[0-9]+", cells[1]))
    if review_want or os.path.exists(REVIEW_FILE):
        text = open(REVIEW_FILE, encoding="utf-8").read().split("\n") if os.path.exists(REVIEW_FILE) else []
        if REVIEW_TABLE_HEAD not in text:
            problems.append(f"table-head\t{REVIEW_FILE}")
        if review_have != review_want:
            problems.append(f"rows-{sum((review_want - review_have).values())}-missing-{sum((review_have - review_want).values())}-extra\t{REVIEW_FILE}")
    for problem in problems:
        print(problem)
    print(f"SUMMARY files_expected={len(want)} files_found={len(found)} review_rows={sum(review_want.values())} bad={len(problems)}")
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
