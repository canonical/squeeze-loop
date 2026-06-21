# lxc-usage.md — running the Use Case A agents in an LXC container, offline

**Goal (as requested):** make all `src/A` agents run inside an LXC container that
cannot reach the internet and can only do the use case; document what was done.

**Status: done.** The Use Case A squeeze (ground truth + upper bound + in-band
implementer/exerciser/runner) runs entirely inside an unprivileged LXC container
with a loopback-only network. One command reproduces it:

```bash
src/A/run_in_lxc.sh
```

---

## 1. Environment, honestly

I am `uid=1000(fabrice)`, **not root**, and **not in the `lxd` group** (the LXD
daemon socket is permission-denied), and `sudo` is not available non-interactively.
So LXD was not usable. What *was* available made **unprivileged LXC** viable:

- `/etc/subuid` + `/etc/subgid`: `fabrice:100000:65536`
- `kernel.unprivileged_userns_clone = 1`
- the classic `lxc-*` tools (`/usr/bin/lxc-create`, `lxc-start`, `lxc-attach`, …)

So the container runs as a normal user via user namespaces: container `root`
(uid 0) maps to host uid `100000`, with no real privilege on the host.

## 2. What was created

| Item | Value |
|---|---|
| Container | `ucA` — `ubuntu noble amd64`, rootfs `~/.local/share/lxc/ucA` (~649 MB) |
| User config | `~/.config/lxc/default.conf` (idmap + network) |
| Container config | `~/.local/share/lxc/ucA/config` |
| In-guest python / sqlite | Python 3.12.3 / sqlite 3.45.1 |

`~/.config/lxc/default.conf`:

```
lxc.idmap = u 0 100000 65536
lxc.idmap = g 0 100000 65536
lxc.net.0.type = empty      # <- only loopback: NO internet
lxc.net.0.flags = up
```

`lxc.net.0.type = empty` gives the container a fresh network namespace with only
`lo` — no veth, no bridge, no route off-box. (`type = none`, by contrast, would
*share the host's* network and was deliberately not used.)

Two adjustments were needed to start it unprivileged:

1. **Path traversal.** The mapped container-root (host uid 100000) could not
   traverse my `0700` home to reach the rootfs. Fixed with **search-only** ACLs
   (no read/list): `setfacl -m u:100000:x ~ ~/.local`.
2. **Init.** Instead of booting `systemd` (which needs cgroup delegation
   unprivileged), the container runs a trivial init —
   `lxc.init.cmd = /bin/sleep infinity` — and the use case is run with
   `lxc-attach`. This matches the requirement "just do the use case": nothing
   else boots.

## 3. How the use case gets in and runs — without a network

`src/A` is streamed into the container over a pipe (not the network):

```bash
tar --exclude=__pycache__ -C src -cf - A | lxc-attach -n ucA -- tar -C /root -xf -
```

Then, inside the container (offline), the agents run:

```
ground-truth/build_ground_truth.py      # lower bound: warehouse + signed ledger
ground-truth/verify_ground_truth.py
upper-bound/validate_handbook.py        # upper bound: the metric handbook
in-band-deliverable/exerciser/build_validation_matrix.py
in-band-deliverable/runner/execute_squeeze.py   # the squeeze (implementer vs exerciser)
```

## 4. Verification

**No internet (the hard gate).** Inside `ucA`: interfaces are `lo` only, there is
no default route, TCP to `1.1.1.1:53` / `8.8.8.8:53` fails with `OSError`, and DNS
(`example.com`) fails with `gaierror`. `run_in_lxc.sh` re-checks this every run and
**refuses to run the use case if the container can reach the internet.**

**The use case passes, offline:**

```
[engine] sqlite 3.45.1
[1] ground truth built
VERIFY OK
VALIDATE OK
[4] matrices built
GATE B SUCCESS: in-band alignment verified across all metrics.
SQUEEZE OK
```

**Negative control (coherent-and-wrong still caught, inside the container):**

```
[FAIL] GATE B CRASH (coherent-and-wrong): TC_M001_2025_Q1_STANDARD_RUN implementer=2047.99 exerciser=1987.21
OK: coherent-and-wrong implementer rejected inside the container.
```

## 5. What is now real vs. still simplified

**Now real (it was not, before):** the agents run inside a genuine LXC container
— kernel user/mount/PID/network namespace isolation from the host, a confined
distro rootfs, and **no internet**. This directly answers the earlier finding
that nothing was actually containerised.

**Still simplified vs. the `*-spec.md` C3 model:** inside the container everything
runs as the single container-`root`. The specs' finer model — three separate
POSIX users (`sentinel`/`implementer`/`exerciser`) with `0700` homes and the data
plane deployed to `/opt/squeeze/shared` as `root:root 0444` — is **not** yet set
up inside the container. The implementer/exerciser isolation is still the
structural one (separate artifacts + the runner's AST/path no-linkage check),
now executing inside the container rather than on the host.

Because the container gives us **root inside**, the existing `provision.sh`
scripts (which need root for `useradd`/`chown root:root`) could now run *in the
container* to realize that full multi-user C3 model. That is the natural next
step; it was left out here to keep this change scoped to exactly what was asked
(container + no internet + the use case).

## 5b. Use Case B (same pattern, a REST service)

`src/B/run_in_lxc.sh` does the same for the Use Case B refund bot, in container
`ucB` (same unprivileged setup, same loopback-only no-internet namespace). The
one difference is that B is a REST service: its `app.py` binds `127.0.0.1:8000`,
which lives entirely on the container's loopback interface — so the app and the
squeeze talk to each other *inside* the container with no route off-box, and the
in-band runner starts and tears the app down itself. Verified offline run:

```
=== asserting NO internet inside ucB ===
confirmed: no internet (loopback-only network namespace).
VERIFY OK
VALIDATE OK
SQUEEZE OK: ISOLATION + GATE C + GATE B + ARCHIVE REGRESSION all green.
negative control -> GATE B CRASH (coherent-and-wrong bot) -> rejected
```

## 6. Caveats

- **Engine version.** The compute-plane pin (README) is sqlite `3.46.1`; the
  noble image ships `3.45.1`. The use case reproduced **identical** results
  (recompute == ledger passed in-container), because the queries use integer
  cents and lexicographic UTC ranges, but a production image should pin the exact
  engine to honour the "frozen compute plane".
- **One-time host internet.** Creating the container downloads the base image on
  the *host* once. After that the container never has network. Re-runs reuse the
  existing container and image cache.
- **ACL grant.** `setfacl -m u:100000:x ~ ~/.local` grants the mapped
  container-root *search-only* access to traverse into the rootfs — not read or
  list. Remove with `setfacl -x u:100000 ~ ~/.local`.

## 7. Reproduce / manage

```bash
src/A/run_in_lxc.sh           # create-if-missing, start, assert no-net, run use case
lxc-info -n ucA               # status
lxc-attach -n ucA -- /bin/sh  # shell inside (offline)
lxc-stop -n ucA               # stop
lxc-destroy -n ucA            # remove
```

Host prerequisites the script cannot self-provide (need a working unprivileged-LXC
host): `/etc/subuid`+`/etc/subgid` ranges, `unprivileged_userns_clone=1`, and
cgroup delegation for the user session.
