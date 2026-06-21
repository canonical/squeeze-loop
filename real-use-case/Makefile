# Makefile — verify that the Creusot-stripped training-data files compile
# "where they can". Each .rs is type-checked as its own library crate.
#
#   make check        compile every file, print a pass/fail summary
#   make report       re-print the saved summary
#   make list-fails   list just the failing files
#   make clean        remove build artifacts and logs
#
# Override variables, e.g.:  make check JOBS=8 EDITION=2021 TOOLCHAIN=stable

SRCDIR    ?= training-data
BUILDDIR  ?= build/cc
TOOLCHAIN ?= nightly-2026-04-21
EDITION   ?= 2021
RUSTC     ?= rustc +$(TOOLCHAIN)
JOBS      ?= $(shell nproc 2>/dev/null || echo 4)

export SRCDIR BUILDDIR RUSTC EDITION JOBS

.PHONY: check report list-fails clean help

check:
	@bash compile-check.sh

report:
	@cat $(BUILDDIR)/REPORT.txt 2>/dev/null || echo "no report yet — run 'make check'"

list-fails:
	@find $(BUILDDIR) -name '*.err' 2>/dev/null \
	  | sed 's|^$(BUILDDIR)/|$(SRCDIR)/|; s|\.err$$|.rs|' | sort \
	  || echo "no failures recorded — run 'make check'"

clean:
	@rm -rf $(BUILDDIR)
	@echo "removed $(BUILDDIR)"

help:
	@echo "targets: check (default), report, list-fails, clean"
	@echo "vars:    SRCDIR=$(SRCDIR) BUILDDIR=$(BUILDDIR) RUSTC='$(RUSTC)' EDITION=$(EDITION) JOBS=$(JOBS)"

.DEFAULT_GOAL := check
