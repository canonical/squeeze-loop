"""Pilot task suite for executing the evaluation protocol with real LLM agents.

Each task is a single-argument function with: a plain-English SPEC, a CORRECT
reference implementation (the oracle), and a seeded coherent-and-wrong WRONG
implementation (a plausible, internally consistent bug). An exerciser agent
writes test cases {input, expected}; the scorer judges whether a config "catches"
the seeded defect (a spec-correct expected on a discriminating input).

The CORRECT/WRONG implementations live here for the scorer; they are NEVER shown
to the barrier-on exerciser (which sees only the SPEC).
"""


def net(tx):
    return (sum(a for t, a in tx if t == "credit")
            - sum(a for t, a in tx if t == "debit"))


def net_wrong(tx):
    return sum(a for _t, a in tx)


def median(xs):
    s = sorted(xs)
    n = len(s)
    return (s[n // 2 - 1] + s[n // 2]) / 2 if n % 2 == 0 else float(s[n // 2])


def median_wrong(xs):
    s = sorted(xs)
    return float(s[(len(s) - 1) // 2])


def running_max_count(xs):
    c, m = 0, None
    for x in xs:
        if m is None or x > m:
            c += 1
            m = x
    return c


def running_max_count_wrong(xs):
    c, m = 0, None
    for x in xs:
        if m is None or x >= m:
            c += 1
            m = x
    return c


def dedup_count_ci(ws):
    return len({w.lower() for w in ws})


def dedup_count_ci_wrong(ws):
    return len(set(ws))


TASKS = [
    {
        "name": "net",
        "signature": "net(transactions) -> number",
        "spec": ("net(transactions): transactions is a list of [type, amount] pairs. "
                 "Return the sum of amounts whose type is 'credit' MINUS the sum of "
                 "amounts whose type is 'debit'. Ignore any transaction whose type is "
                 "neither 'credit' nor 'debit'."),
        "correct": net, "wrong": net_wrong,
    },
    {
        "name": "median",
        "signature": "median(nums) -> float",
        "spec": ("median(nums): return the median of a non-empty list of numbers. "
                 "For odd length, the middle element; for EVEN length, the AVERAGE of "
                 "the two middle elements. Return a float."),
        "correct": median, "wrong": median_wrong,
    },
    {
        "name": "running_max_count",
        "signature": "running_max_count(nums) -> int",
        "spec": ("running_max_count(nums): count how many elements are STRICTLY "
                 "greater than every element before them (the first element always "
                 "counts). An element equal to the current maximum does NOT count."),
        "correct": running_max_count, "wrong": running_max_count_wrong,
    },
    {
        "name": "dedup_count_ci",
        "signature": "dedup_count_ci(words) -> int",
        "spec": ("dedup_count_ci(words): return the number of DISTINCT words, "
                 "comparing case-INSENSITIVELY (so 'A' and 'a' are the same word)."),
        "correct": dedup_count_ci, "wrong": dedup_count_ci_wrong,
    },
]

WRONG_SOURCE = {
    "net": "def net(transactions):\n    return sum(a for _t, a in transactions)",
    "median": ("def median(nums):\n    s = sorted(nums)\n"
               "    return float(s[(len(s) - 1) // 2])"),
    "running_max_count": ("def running_max_count(nums):\n    c, m = 0, None\n"
                          "    for x in nums:\n        if m is None or x >= m:\n"
                          "            c += 1\n            m = x\n    return c"),
    "dedup_count_ci": "def dedup_count_ci(words):\n    return len(set(words))",
}
