# Running the use-case agents safely in LXC containers

This document explains how the four executable instances (`src/A`, `src/B`,
`src/C`, `src/D`) are run inside Linux containers: the architecture, the script
layout, why we use **LXC** rather than Docker, how networking is provided, and --
the load-bearing constraint -- how all of this works **without `sudo` / without
root**.

---

## 1. What runs, and where

Each use case is a *squeeze*: a coordinator drives an implementer and an
independent exerciser between an **upper bound** (a normative document) and a
**lower bound** (an executable ground truth), and machine gates decide "done".
We run each squeeze inside its own container:

| Container | Use case | Lower-bound engine | Needs network to run? |
|-----------|----------|--------------------|-----------------------|
| `ucA` | A — tabular analytics (transcription) | SQLite warehouse (stdlib) | no |
| `ucB` | B — refund agent (authored authority) | REST app + signed archive (stdlib) | no |
| `ucC` | C — API contract guard (split planes) | OpenAPI + live server (stdlib) | no |
| `ucD` | D — Rocq/Coq proofs (deductive) | the **Coq/Rocq kernel** (`coqc`) | yes — to install the kernel |

A/B/C are pure Python standard library, so they need no packages at all. D's
ground truth *is* a theorem prover, which must be installed; with the containers
networked (Section 4) it is installed in-container with `apt-get install coq`.

One command runs a use case end to end inside its container:

```bash
src/A/run_in_lxc.sh      # or src/B, src/C, src/D
```

---

## 2. Why LXC, not Docker

Both are "Linux containers", but they are built for different jobs, and ours is
the job LXC is built for.

- **System containers vs application containers.** Docker wraps a *single
  process/image* with a layered, immutable filesystem and an entrypoint. LXC
  gives a *full system instance* — an init, a normal filesystem, multiple
  long-lived processes (our coordinator, implementer, exerciser, the prover
  kernel) — which is exactly the multi-actor pipeline a squeeze is.
- **Rootless by design, with no daemon.** Docker's classic model is a
  **root-owned daemon**; talking to `/var/run/docker.sock` is effectively root,
  and on this host that socket is not ours to use. LXC's `lxc-*` tools run
  **directly as your user** with no privileged daemon in the path — see Section 3.
- **We do not want an image build pipeline.** Docker's value is reproducible
  image layers shipped to a registry. We don't ship images; we stream a source
  tree into a throwaway system and run it. LXC's download-template + bind/`tar`
  sync matches that without a Dockerfile/registry.
- **Honest filesystem.** The container's rootfs is a plain directory tree we can
  `tar` into over a pipe; no overlay/registry indirection. That keeps the
  "stream the source in, run, throw away" loop simple and auditable.

This is not "Docker is bad" — it is that a multi-process, rootless, no-registry,
throwaway *system* sandbox is LXC's home turf and Docker's awkward case.

---

## 3. It works without `sudo` (unprivileged containers)

This is the key property. On this host there is **no non-interactive `sudo`, no
membership in the `lxd` group, and the LXD daemon socket is permission-denied.**
Everything below runs as the ordinary user `fabrice` (uid 1000).

What makes that possible:

- **User namespaces + subuid/subgid.** `/etc/subuid` and `/etc/subgid` grant
  `fabrice:100000:65536`. The container's root (uid 0) is **mapped** to host uid
  100000, etc. So a process can be "root" *inside* the container while being an
  unprivileged, un-special host uid *outside* it. A compromise inside the
  container cannot touch anything the host user couldn't already touch — and it
  certainly cannot touch the host as root.
- **`kernel.unprivileged_userns_clone = 1`** lets a non-root user create those
  namespaces.
- **No setuid network helper needed** (Section 4).

The container config (`~/.config/lxc/default.conf`) carries the idmap and a
loopback-only base network:

```
lxc.idmap = u 0 100000 65536
lxc.idmap = g 0 100000 65536
lxc.net.0.type = empty
lxc.net.0.flags = up
```

Net effect: **no root, no daemon, no group membership, no setuid** — just
namespaces the kernel already lets an unprivileged user open.

---

## 4. Networking — rootless internet via slirp4netns

The containers now have **internet**, so the in-band layer can fetch what it
needs (packages, data) and D can install its own kernel.

The obvious way — a `veth` pair into the `lxcbr0` bridge — is **not available
without root** here: it requires either the `lxc-user-nic` setuid helper plus an
`/etc/lxc/lxc-usernet` quota (neither is present, and we can't create them), or
direct `CAP_NET_ADMIN`. So we use the rootless path instead:

- **`slirp4netns`** — the same user-mode NAT that rootless Podman uses. It
  attaches to the container's network namespace by PID and injects a NATed `tap0`
  (10.0.2.100/24, gateway 10.0.2.2, DNS 10.0.2.3). TCP/IP to the outside is
  handled by a user-space stack on the host. **No bridge, no root, no setuid.**

The helper `lxc_net_up` starts it persistently (`setsid … &`, PID recorded under
the container's state dir) so the container keeps internet for interactive
enrichment after the script returns, and fixes DNS (the image's
`/etc/resolv.conf` is a dangling systemd-resolved symlink under our `sleep` init,
so we replace it with `nameserver 10.0.2.3`). `lxc_assert_internet` then does a
**positive** check (resolve `archive.ubuntu.com`).

> Design note: earlier these scripts *hard-gated on the absence of internet*
> (an air-gapped run). That was changed deliberately, at the project's request,
> to **enable** internet so the in-band layer can be enriched. The container is
> still an isolated unprivileged namespace; it simply now has a NATed route out.

---

## 5. Script structure

```
src/lxc_common.sh          # shared rootless-LXC helpers (sourced by all four)
src/A/run_in_lxc.sh        # thin per-use-case wrapper
src/B/run_in_lxc.sh
src/C/run_in_lxc.sh
src/D/run_in_lxc.sh        # + installs the Coq/Rocq kernel in-container
```

`src/lxc_common.sh` holds everything generic, so a bug is fixed once, not four
times:

- `lxc_prereqs` — check `lxc-create` + `slirp4netns`, read the subuid base, write
  `default.conf` (idmap + empty net), grant the mapped root traversal ACLs.
- `lxc_up NAME REL` — create the container from the download template if absent
  (defaults to the host's Ubuntu release for ABI parity), give it
  `lxc.init.cmd = /bin/sleep infinity`, start it.
- `lxc_net_up NAME` — bring up rootless internet (slirp4netns) + fix DNS.
- `lxc_assert_internet NAME` — positive connectivity check.
- `lxc_sync NAME SRC_PARENT TOP` — `tar` the source tree in over a pipe
  (excluding `__pycache__` and compiled `*.vo/*.glob` artifacts).

Each `run_in_lxc.sh` is then a short, readable wrapper: source the helpers,
`lxc_prereqs`/`lxc_up`/`lxc_net_up`/`lxc_assert_internet`/`lxc_sync`, then run
that use case's build → verify → squeeze → **negative control**, capturing each
step's real exit code (deliberately *not* through a pipe — a `… | tail` would
mask the real status, which is the kind of fabricated-green bug this project
exists to prevent).

---

## 6. The safety architecture (two layers of isolation)

**Outer layer — the container is the blast-radius boundary.** The use-case agents
run inside an unprivileged LXC namespace: separate mount, pid, and network
namespaces, and a uid map under which "root" is a powerless host uid. Whatever the
implementer or exerciser does — including running a freshly written program or a
proof script — it does to a throwaway rootfs, as a non-privileged host user, with
only a NATed network route. The source is streamed in; nothing of the host is
mounted in except (for D) the read path needed to install the kernel via apt.

**Inner layer — the squeeze's own barriers.** Inside the container, correctness is
still decided the squeeze way:

- The **implementer/prover** and the **exerciser** are kept apart: the exerciser
  is authored from the upper bound only and never sees the implementation; the
  prover never sees the tests. In the current harness this separation is enforced
  by how each actor's working context is constructed plus an isolation check
  (imports/paths), with the per-actor POSIX users described in the specs as the
  stronger form.
- **Gate B is machine-checked and capability-gated.** For D it is the Coq/Rocq
  kernel: the proof must type-check, the axiom audit (`Print Assumptions`) must
  show "Closed under the global context" (an `Admitted` cheat is caught here), and
  every seeded false mutation must be *rejected* by the kernel. If the kernel is
  absent the gate prints `DEPENDENCY UNMET` and **SKIPS** — it never fabricates a
  passing verdict. That honesty rule is absolute.
- Every run ends with a **negative control**: a coherent-and-wrong implementer is
  fed in and the gates must reject it. A green run that cannot fail its own
  negative control is not trusted.

So "safely run the agents" means both: the container caps what a misbehaving
agent can reach, and the squeeze caps what a *plausible-but-wrong* agent can get
past.

---

## 7. Use Case D specifics — the kernel

D's lower bound is a real theorem prover, which surfaced the only hard
dependency. With networking in place it is simply installed in-container:

```sh
apt-get install -y rocq-prover || apt-get install -y coq
```

On Ubuntu *resolute* this yields **Coq 8.20.1** (`coqc` + `coqchk`). The harness's
single kernel-shim (`src/D/ground-truth/rocq_kernel.py`) is version-agnostic: it
invokes `coqc` if present, else `rocq compile` (the Rocq 9.x rebrand), and audits
axioms via `Print Assumptions` (which works on both). Installing in-container also
avoids an ABI trap we hit earlier — the host's Rocq is built against a newer glibc
than an older container image carries, so borrowing the host binary fails; a
kernel installed by the container's own package manager always matches its libc.

A full in-container D run reports real verdicts:

```
[3] gate(good)            ALL GATES PASSED        (kernel type-checked, axiom-clean)
[4] gate(admitted-cheat)  escape hatch detected   (caught by the axiom audit)
[6] measure               defects 2/2 barrier-on, 0/2 barrier-off, coherent-wrong caught
```

---

## 8. Reproduce

```bash
# prerequisites already satisfied on this host: subuid/subgid, userns clone,
# lxc tools, slirp4netns. No sudo required.
src/A/run_in_lxc.sh     # tabular analytics
src/B/run_in_lxc.sh     # refund agent
src/C/run_in_lxc.sh     # API contract guard
src/D/run_in_lxc.sh     # Rocq proofs (installs Coq in-container on first run)
```

Containers are reused across runs (idempotent). Each prints a per-step exit code
and ends with its negative control.

---

## 9. Honest limitations

- **Internet is now on by design.** The air-gapped property of the earlier
  scripts is gone; that was an explicit trade to enrich the in-band layer. If a
  use case must be demonstrated air-gapped, skip `lxc_net_up` and the kernel is
  pre-baked instead.
- **POSIX-user separation is specified, logically enforced.** The specs call for
  four separate accounts (`sentinel`/`formalizer`/`prover`/`exerciser`); the
  current runs enforce the barriers by context construction + isolation checks
  inside one account, with the container as the OS boundary. Running each actor as
  its own in-container uid is the natural hardening step.
- **The build agents ran on the host.** The LLM agents that *wrote* `src/*` ran as
  the host user, not in LXC; the containers sandbox the *use-case execution*, not
  the authoring.
- **slirp4netns is user-mode.** Throughput/latency are lower than a real bridge;
  fine for package installs and fetches, not for benchmarking the network.
