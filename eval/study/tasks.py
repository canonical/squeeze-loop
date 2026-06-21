"""Powered-study task suite (PRE-COMMITTED before any runs; not tuned to results).

8 single-argument tasks chosen to be harder / more error-prone than the pilots
(encoding rather than decoding; compositional parsing; non-obvious tie/edge
conventions). Each has a precise spec, a correct oracle, and edge-targeted probes.

Design: three model tiers (haiku/sonnet/opus) each self-author an implementation
+ its own tests; one independent opus exerciser per task writes spec-only tests.
Holding each self-authored impl fixed, we ask -- among the impls that are actually
buggy -- whether the author's own tests caught the bug vs whether the independent
exerciser caught it (the self-preference / barrier effect), with a paired McNemar
test. The suite is fixed; we report whatever rate of bugs arises.
"""


def merge_intervals(iv):
    out = []
    for a, b in sorted([list(p) for p in iv]):
        if out and a <= out[-1][1]:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out


def spreadsheet_col(n):
    s = ""
    while n > 0:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def expand_ranges(s):
    out = []
    for tok in s.split(","):
        tok = tok.strip()
        if "-" in tok:
            a, b = tok.split("-")
            out += list(range(int(a), int(b) + 1))
        else:
            out.append(int(tok))
    return out


def is_balanced(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    st = []
    for c in s:
        if c in "([{":
            st.append(c)
        elif c in ")]}":
            if not st or st.pop() != pairs[c]:
                return False
    return not st


def int_to_roman(n):
    vals = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"),
            (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"),
            (4, "IV"), (1, "I")]
    r = ""
    for v, sym in vals:
        while n >= v:
            r += sym
            n -= v
    return r


def dedup_adjacent(xs):
    out = []
    for x in xs:
        if not out or out[-1] != x:
            out.append(x)
    return out


def compress_rle(s):
    if not s:
        return ""
    out, prev, cnt = "", s[0], 1
    for c in s[1:]:
        if c == prev:
            cnt += 1
        else:
            out += prev + str(cnt)
            prev, cnt = c, 1
    return out + prev + str(cnt)


def most_common(xs):
    if not xs:
        return None
    counts = {}
    for x in xs:
        counts[x] = counts.get(x, 0) + 1
    m = max(counts.values())
    return min(k for k, v in counts.items() if v == m)


TASKS = [
    {"name": "merge_intervals", "signature": "merge_intervals(intervals) -> list of [a,b]",
     "spec": ("merge_intervals(intervals): given a list of [start,end] intervals "
              "(start<=end, any order), return the merged, sorted list of "
              "non-overlapping intervals. Intervals that merely TOUCH (e.g. [1,2] "
              "and [2,3]) merge into one ([1,3])."),
     "correct": merge_intervals,
     "probes": [[[1, 3], [2, 4]], [[1, 2], [2, 3]], [[1, 2], [3, 4]], [[3, 4], [1, 2]], [[1, 5], [2, 3]]]},
    {"name": "spreadsheet_col", "signature": "spreadsheet_col(n) -> str",
     "spec": ("spreadsheet_col(n): convert a 1-indexed column number to its "
              "spreadsheet letters: 1->A, 26->Z, 27->AA, 28->AB, 52->AZ, 702->ZZ, "
              "703->AAA. (Bijective base-26; there is no zero digit.)"),
     "correct": spreadsheet_col, "probes": [1, 26, 27, 28, 52, 702, 703]},
    {"name": "expand_ranges", "signature": "expand_ranges(s) -> list of int",
     "spec": ("expand_ranges(s): parse a comma-separated string of non-negative "
              "integers and inclusive ascending ranges, returning the expanded "
              "list in order. \"1-3,5,7-9\" -> [1,2,3,5,7,8,9]; \"5\" -> [5]; "
              "\"1-1\" -> [1]."),
     "correct": expand_ranges, "probes": ["1-3,5,7-9", "5", "1-1", "10,12-14", "1-3"]},
    {"name": "is_balanced", "signature": "is_balanced(s) -> bool",
     "spec": ("is_balanced(s): return True iff the brackets in s are balanced and "
              "properly nested, across the three types () [] {}. Other characters "
              "are ignored. \"([])\"->True, \"([)]\"->False, \"((\"->False, "
              "\"\"->True."),
     "correct": is_balanced, "probes": ["([])", "([)]", "((", "", "{[()]}", ")("]},
    {"name": "int_to_roman", "signature": "int_to_roman(n) -> str",
     "spec": ("int_to_roman(n): encode an integer 1..3999 as an uppercase Roman "
              "numeral using standard subtractive forms (4=IV, 9=IX, 40=XL, 90=XC, "
              "400=CD, 900=CM). 1994->MCMXCIV, 58->LVIII, 4->IV."),
     "correct": int_to_roman, "probes": [4, 9, 40, 58, 1994, 3888, 2023, 444]},
    {"name": "dedup_adjacent", "signature": "dedup_adjacent(xs) -> list",
     "spec": ("dedup_adjacent(xs): remove only CONSECUTIVE duplicate elements, "
              "keeping non-adjacent repeats. [1,1,2,1] -> [1,2,1]; [1,1,1] -> [1]; "
              "[1,2,3] -> [1,2,3]."),
     "correct": dedup_adjacent, "probes": [[1, 1, 2, 1], [1, 1, 1], [], [1, 2, 3], [1, 1, 2, 2, 1]]},
    {"name": "compress_rle", "signature": "compress_rle(s) -> str",
     "spec": ("compress_rle(s): run-length encode s as each run's character "
              "followed by its count, with the count ALWAYS written even when 1. "
              "\"aaabb\"->\"a3b2\"; \"abc\"->\"a1b1c1\"; \"\"->\"\"."),
     "correct": compress_rle, "probes": ["aaabb", "abc", "", "aaaa", "aabbaa"]},
    {"name": "most_common", "signature": "most_common(xs) -> element or None",
     "spec": ("most_common(xs): return the element that appears most often; on a "
              "tie return the SMALLEST such element; for an empty list return None. "
              "[1,2,2,3,3] -> 2 (tie between 2 and 3, smallest is 2)."),
     "correct": most_common, "probes": [[1, 2, 2, 3, 3], [1], [], [5, 5, 1], [3, 3, 2, 2, 2]]},
]
