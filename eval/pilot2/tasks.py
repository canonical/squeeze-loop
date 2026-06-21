"""Pilot-2 task suite: the STRONGER barrier-off (self-authorship / self-preference).

Each task is a single-argument function with a deliberately easy-to-misread edge
case (a tempting-wrong reading). No seeded implementation: the bug, if any, is the
self-author agent's own. The oracle here (CORRECT) is the reference; PROBES are
discriminating inputs used to decide whether a self-authored implementation is
actually buggy.

Configs compared, holding the self-authored implementation fixed:
  - SELF: the agent's own tests (it wrote the impl and the tests together).
  - INDEPENDENT: a separate exerciser's tests, written from the spec alone.
A config "catches" iff it has a spec-correct test the (buggy) impl fails.
"""


def bankers_round(x):
    return round(x)            # Python round() is round-half-to-even


def second_largest(nums):
    d = sorted(set(nums), reverse=True)
    return d[1] if len(d) >= 2 else None


def title_case(s):
    return " ".join(w[:1].upper() + w[1:].lower() for w in s.split())


def is_sorted_strict(nums):
    return all(nums[i] < nums[i + 1] for i in range(len(nums) - 1))


TASKS = [
    {"name": "bankers_round", "signature": "bankers_round(x) -> int",
     "spec": ("bankers_round(x): round the number x to the nearest integer, with "
              "ties (exactly .5) rounded to the nearest EVEN integer (banker's "
              "rounding): 2.5 -> 2, 3.5 -> 4, 0.5 -> 0, -0.5 -> 0."),
     "correct": bankers_round, "probes": [2.5, 0.5, 3.5, -0.5, 1.5, 2.4, 2.6, -2.5]},
    {"name": "second_largest", "signature": "second_largest(nums) -> number or None",
     "spec": ("second_largest(nums): return the second-largest DISTINCT value in the "
              "list; if there are fewer than two distinct values, return None. "
              "Duplicates of the maximum do not count."),
     "correct": second_largest, "probes": [[5, 5, 3], [5, 5], [1, 2, 3], [3, 3, 3], [10, 9, 9, 8]]},
    {"name": "title_case", "signature": "title_case(s) -> str",
     "spec": ("title_case(s): split s on whitespace; for each word, uppercase the "
              "first character and lowercase the rest; join the words with a single "
              "space. Apostrophes/letters after them are lowercased: \"don't\" -> "
              "\"Don't\" (not \"Don'T\")."),
     "correct": title_case, "probes": ["don't yell", "hello   world", "ABC def", "a", ""]},
    {"name": "is_sorted_strict", "signature": "is_sorted_strict(nums) -> bool",
     "spec": ("is_sorted_strict(nums): return True iff the list is STRICTLY "
              "increasing (each element greater than the previous); equal adjacent "
              "elements make it NOT strictly sorted. Empty and single-element lists "
              "are True."),
     "correct": is_sorted_strict, "probes": [[1, 2, 2], [1, 2, 3], [3, 2, 1], [1], []]},
]
