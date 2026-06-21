"""Pilot-3 task suite: surface the self-preference effect with a WEAKER model.

Same design as pilot-2 (true self-authorship: one agent writes impl + its own
tests), but the self-author is a weaker model so the natural bug rate is nonzero.
Holding the (possibly buggy) self-authored impl fixed, three test-authors are
compared:
  self          the weak self-author's own tests (it wrote the impl)
  indep_weak    independent exerciser, SAME weak model, spec only (barrier,
                capability-controlled)
  indep_strong  independent exerciser, strong model, spec only (confirms the bug
                is catchable at all)

Tasks include two that weak models classically trip on (subtractive Roman
numerals, the 100/400 leap-year rule).
"""


def bankers_round(x):
    return round(x)


def title_case(s):
    return " ".join(w[:1].upper() + w[1:].lower() for w in s.split())


def second_largest(nums):
    d = sorted(set(nums), reverse=True)
    return d[1] if len(d) >= 2 else None


_ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def roman_to_int(s):
    total = 0
    for i, ch in enumerate(s):
        v = _ROMAN[ch]
        if i + 1 < len(s) and v < _ROMAN[s[i + 1]]:
            total -= v
        else:
            total += v
    return total


def is_leap_year(y):
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)


TASKS = [
    {"name": "bankers_round", "signature": "bankers_round(x) -> int",
     "spec": ("bankers_round(x): round x to the nearest integer, ties (exactly .5) "
              "to the nearest EVEN integer: 2.5->2, 3.5->4, 0.5->0, -0.5->0."),
     "correct": bankers_round, "probes": [2.5, 0.5, 3.5, -0.5, 1.5, 2.6]},
    {"name": "title_case", "signature": "title_case(s) -> str",
     "spec": ("title_case(s): split s on whitespace; uppercase each word's first "
              "char and lowercase the rest; join with single spaces; \"don't\" -> "
              "\"Don't\" (not \"Don'T\")."),
     "correct": title_case, "probes": ["don't yell", "hello   world", "ABC def", "a"]},
    {"name": "second_largest", "signature": "second_largest(nums) -> number or None",
     "spec": ("second_largest(nums): the second-largest DISTINCT value; None if "
              "fewer than two distinct values; duplicates of the max don't count."),
     "correct": second_largest, "probes": [[5, 5, 3], [5, 5], [1, 2, 3], [10, 9, 9, 8]]},
    {"name": "roman_to_int", "signature": "roman_to_int(s) -> int",
     "spec": ("roman_to_int(s): convert an uppercase Roman numeral to an integer, "
              "honouring subtractive notation (IV=4, IX=9, XL=40, XC=90, CD=400, "
              "CM=900). E.g. MCMXCIV=1994, LVIII=58."),
     "correct": roman_to_int, "probes": ["IV", "IX", "XL", "MCMXCIV", "LVIII", "III", "XCIX"]},
    {"name": "is_leap_year", "signature": "is_leap_year(y) -> bool",
     "spec": ("is_leap_year(y): a year is a leap year iff it is divisible by 4, "
              "EXCEPT century years (divisible by 100) which are leap only if also "
              "divisible by 400. So 2000 and 2024 are leap; 1900 and 2100 are not."),
     "correct": is_leap_year, "probes": [2000, 1900, 2024, 2023, 2100, 2400]},
]
