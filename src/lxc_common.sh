# src/lxc_common.sh -- shared unprivileged-LXC helpers for src/{A,B,C,D}/run_in_lxc.sh
#
# The containers run UNPRIVILEGED (your normal user, subuid/subgid + userns; no
# root, no lxd group) and now have INTERNET, so the in-band layer can fetch what
# it needs (packages, data, the Rocq kernel for Use Case D).
#
# Rootless networking, honestly: this host has NO /etc/lxc/lxc-usernet and no
# usable root, so the classic veth/bridge path is unavailable. Instead we use
# slirp4netns -- the same user-mode NAT rootless Podman uses -- to inject a NATed
# tap0 into the container's own network namespace. The container reaches the
# internet through a user-space TCP/IP stack on the host; no bridge, no root, no
# setuid helper. It remains an isolated unprivileged container.
#
# Source this from a run_in_lxc.sh, then call: lxc_prereqs; lxc_up NAME REL;
# lxc_net_up NAME; lxc_assert_internet NAME; lxc_sync NAME SRC_PARENT TOP.

log() { printf '\n=== %s ===\n' "$*"; }

lxc_prereqs() {
  command -v lxc-create  >/dev/null || { echo "lxc tools missing (apt install lxc)"; exit 1; }
  command -v slirp4netns >/dev/null || { echo "slirp4netns missing (apt install slirp4netns)"; exit 1; }
  SUBBASE="$(awk -F: -v u="$USER" '$1==u{print $2; exit}' /etc/subuid || true)"
  [ -n "$SUBBASE" ] || { echo "no subuid range for $USER in /etc/subuid"; exit 1; }
  mkdir -p "$HOME/.config/lxc"
  if ! grep -q 'lxc.net.0.type = empty' "$HOME/.config/lxc/default.conf" 2>/dev/null; then
    cat > "$HOME/.config/lxc/default.conf" <<EOF
lxc.idmap = u 0 $SUBBASE 65536
lxc.idmap = g 0 $SUBBASE 65536
lxc.net.0.type = empty
lxc.net.0.flags = up
EOF
  fi
  command -v setfacl >/dev/null && {
    setfacl -m "u:${SUBBASE}:x" "$HOME"        2>/dev/null || true
    setfacl -m "u:${SUBBASE}:x" "$HOME/.local" 2>/dev/null || true
  }
}

lxc_up() {  # $1=name  $2=ubuntu release (default: host's, for ABI parity)
  local name="$1" rel="${2:-resolute}"
  if ! lxc-info -n "$name" >/dev/null 2>&1; then
    log "creating $name (ubuntu $rel) -- one-time image download on the host"
    lxc-create -n "$name" -t download -- -d ubuntu -r "$rel" -a amd64
  fi
  local cfg="$HOME/.local/share/lxc/$name/config"
  grep -q 'lxc.init.cmd' "$cfg" || printf '\nlxc.init.cmd = /bin/sleep infinity\n' >> "$cfg"
  if [ "$(lxc-info -n "$name" -s -H 2>/dev/null)" != "RUNNING" ]; then
    log "starting $name"; lxc-start -n "$name" -d; sleep 2
  fi
  lxc-info -n "$name" | grep -E 'Name|State'
}

lxc_net_up() {  # $1=name -- rootless internet via slirp4netns (persistent)
  local name="$1"
  local pidf="$HOME/.local/share/lxc/$name/slirp.pid"
  if [ -f "$pidf" ] && kill -0 "$(cat "$pidf" 2>/dev/null)" 2>/dev/null; then
    log "internet already up for $name (slirp4netns pid $(cat "$pidf"))"
  else
    local cpid; cpid="$(lxc-info -n "$name" -p -H)"
    log "bringing up rootless internet (slirp4netns) for $name [pid $cpid]"
    setsid slirp4netns --configure --mtu=65520 --disable-host-loopback "$cpid" tap0 \
      >"$HOME/.local/share/lxc/$name/slirp.log" 2>&1 < /dev/null &
    echo $! > "$pidf"; sleep 3
  fi
  # /etc/resolv.conf is a dangling systemd-resolved symlink under a sleep init;
  # point DNS at slirp4netns's resolver (10.0.2.3), with a public fallback.
  lxc-attach -n "$name" -- /bin/sh -c \
    'rm -f /etc/resolv.conf; printf "nameserver 10.0.2.3\nnameserver 1.1.1.1\n" > /etc/resolv.conf'
}

lxc_assert_internet() {  # $1=name -- positive check (we WANT internet now)
  local name="$1"
  if lxc-attach -n "$name" -- python3 - <<'PY'
import socket, sys
socket.setdefaulttimeout(8)
try: socket.gethostbyname("archive.ubuntu.com"); sys.exit(0)
except OSError: sys.exit(1)
PY
  then echo "confirmed: $name has internet (slirp4netns user-mode NAT)."
  else echo "WARNING: $name has NO internet; see ~/.local/share/lxc/$name/slirp.log"; fi
}

lxc_sync() {  # $1=name $2=src parent (host) $3=top dir (e.g. D)
  local name="$1" parent="$2" top="$3"
  log "syncing $top into $name:/root/$top"
  lxc-attach -n "$name" -- rm -rf "/root/$top"
  tar --exclude='__pycache__' --exclude='*.vo' --exclude='*.glob' --exclude='*.vos' \
      --exclude='*.vok' --exclude='.*.aux' -C "$parent" -cf - "$top" \
    | lxc-attach -n "$name" -- tar -C /root -xf -
}
