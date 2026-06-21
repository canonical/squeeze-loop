"""A pool of 100 math exercises of varying difficulty for the D diversity test.

Diversity, not determinism: the level-up ladder is a fixed set of rungs, so
re-running it is a fixed point (no trial happened). Here the "implementer" is a
FIXED WEAK auto-prover -- `intros; lia` (linear integer arithmetic) -- and the pool
spans difficulties: linear goals it can discharge ("found") and nonlinear/structural
goals it cannot ("not found"). Sampling exercises randomly each cycle yields a real,
varying success rate -- an actual trial, not a recomputation.

The pool is calibrated so roughly 20% of exercises are beyond `lia` (not found).
Each exercise is TRUE; "not found" means the weak prover fails, not that the
statement is false.
"""

# --- 80 LINEAR exercises: `intros; lia` discharges these ---------------------
_LINEAR = []
# commutativity / associativity / rearrangements (parametrised by coefficients)
for a in range(1, 7):
    for b in range(1, 7):
        _LINEAR.append((f"forall x y : nat, {a} * x + {b} * y = {b} * y + {a} * x", "linear_comm"))
# monotonic inequalities
for k in range(1, 15):
    _LINEAR.append((f"forall x y : nat, x <= x + {k} * y", "linear_le"))
# concrete identities
for n in range(2, 22):
    _LINEAR.append((f"{n} + {n} = {2*n}", "linear_const"))
# linear cancellation / distribution by constants
for c in range(2, 14):
    _LINEAR.append((f"forall x : nat, {c} * (x + 1) = {c} * x + {c}", "linear_distrib_const"))

_LINEAR = _LINEAR[:80]

# --- 20 NONLINEAR / structural exercises: `lia` cannot ("not found") ----------
# Exponentials (lia treats Nat.pow as an opaque atom -> cannot decide) and var*var
# products (lia atomises each product, so it cannot relate them). All TRUE; all
# beyond `intros; lia`.
_HARD = [
    ("forall n : nat, n <= Nat.pow 2 n", "exp_bound2"),
    ("forall n : nat, Nat.pow 2 n >= 1", "pow2_ge1"),
    ("forall n : nat, 1 <= Nat.pow 3 n", "pow3_ge1"),
    ("forall n : nat, Nat.pow 2 (n + 1) = 2 * Nat.pow 2 n", "pow2_succ"),
    ("forall n : nat, n <= Nat.pow 3 n", "exp_bound3"),
    ("forall n m : nat, Nat.pow 2 (n + m) = Nat.pow 2 n * Nat.pow 2 m", "pow2_add"),
    ("forall n : nat, Nat.pow 2 n >= n + 1", "pow2_ge_succ"),
    ("forall n : nat, 2 <= Nat.pow 2 (n + 1)", "pow2_ge2"),
    ("forall n : nat, Nat.pow 4 n >= 1", "pow4_ge1"),
    ("forall n : nat, Nat.pow 5 n >= 1", "pow5_ge1"),
    ("forall n : nat, n <= Nat.pow 2 (n + 1)", "exp_bound2b"),
    ("forall n : nat, Nat.pow 3 n >= 1", "pow3_ge1b"),
    ("forall a b : nat, (a + b) * (a + b) >= a * a", "square_lb"),
    ("forall a b : nat, (a + b) * (a + b) >= 4 * a * b", "amgm2"),
    ("forall n : nat, n * n * n >= n * n", "cube_ge"),
    ("forall n : nat, Nat.pow 6 n >= 1", "pow6_ge1"),
    ("forall n : nat, n <= n * n", "sq_ge"),
    ("forall n : nat, n * n >= n", "sq_ge2"),
    ("forall x y : nat, x * x + y * y >= 2 * x * y", "amgm"),
    ("forall n : nat, Nat.pow 7 n >= 1", "pow7_ge1"),
]

POOL = [{"id": f"EX_{i:03d}", "kind": k, "stmt": s}
        for i, (s, k) in enumerate(_LINEAR + _HARD)]

assert len(POOL) == 100, len(POOL)
