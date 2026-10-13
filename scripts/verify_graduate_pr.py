#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification Script for Graduate Pull Requests in github-a-to-z
Enforces Scope Guard, Anti-Vandalism, and Formatting constraints for GRADUATES.md.

Usage:
  python3 scripts/verify_graduate_pr.py [--base <base_ref>] [--head <head_ref>]
"""

import sys
import os
import re
import subprocess
import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def run_git(args):
    result = subprocess.run(["git"] + args, cwd=REPO_ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Git command failed: git {' '.join(args)}\nError: {result.stderr.strip()}")
    return result.stdout.strip()

def get_changed_files(base_ref, head_ref):
    specs = [f"{base_ref}...{head_ref}", f"{base_ref}..{head_ref}"]
    for spec in specs:
        try:
            output = run_git(["diff", "--name-only", spec])
            files = [f.strip() for f in output.splitlines() if f.strip()]
            if files:
                return files
        except Exception:
            continue
    # Fallback to diffing against base_ref directly (handles working tree in local dev)
    try:
        output = run_git(["diff", "--name-only", base_ref])
        files = [f.strip() for f in output.splitlines() if f.strip()]
        return files
    except Exception:
        pass
    return []

def get_file_diff(base_ref, head_ref, file_path):
    specs = [f"{base_ref}...{head_ref}", f"{base_ref}..{head_ref}"]
    for spec in specs:
        try:
            output = run_git(["diff", "-U0", spec, "--", file_path])
            if output:
                return output
        except Exception:
            continue
    # Fallback to diffing against base_ref directly
    try:
        output = run_git(["diff", "-U0", base_ref, "--", file_path])
        return output
    except Exception:
        pass
    return ""

def verify_graduate_pr(base_ref="origin/main", head_ref="HEAD"):
    print(f"🎓 Checking Pull Request changes (Base: {base_ref}, Head: {head_ref})...")

    # 1. Scope Guard: Check which files were changed
    changed_files = get_changed_files(base_ref, head_ref)
    print(f"📁 Changed files detected ({len(changed_files)}): {changed_files}")

    if not changed_files:
        print("ℹ️ No changed files detected in diff.")
        return True

    # If GRADUATES.md is not among changed files, this is not a graduate PR
    if "GRADUATES.md" not in changed_files:
        print("ℹ️ 'GRADUATES.md' not modified. Skipping graduate verification (not a graduate PR).")
        return True

    # Strict Scope Guard: A graduate submission must ONLY touch GRADUATES.md!
    unexpected_files = [f for f in changed_files if f != "GRADUATES.md"]
    if unexpected_files:
        print(f"🚨 Scope Guard Violation: Graduate Pull Request may ONLY touch 'GRADUATES.md'.")
        print(f"   Unexpected files modified: {unexpected_files}")
        return False

    # 2. Diff inspection for GRADUATES.md
    diff_text = get_file_diff(base_ref, head_ref, "GRADUATES.md")
    
    deleted_lines = []
    added_lines = []
    
    for line in diff_text.splitlines():
        if line.startswith("---") or line.startswith("+++") or line.startswith("@@"):
            continue
        if line.startswith("-"):
            content = line[1:].strip()
            if content:
                deleted_lines.append(content)
        elif line.startswith("+"):
            content = line[1:].strip()
            if content:
                added_lines.append(content)

    # Anti-Vandalism Check: No existing table rows can be removed or altered
    deleted_table_rows = [l for l in deleted_lines if l.startswith("|")]
    if deleted_table_rows:
        print(f"🚨 Anti-Vandalism Violation: Detected deletion or alteration of existing rows in GRADUATES.md:")
        for r in deleted_table_rows:
            print(f"   - {r}")
        return False

    # Check additions: Must add table row(s)
    added_table_rows = [l for l in added_lines if l.startswith("|")]
    if not added_table_rows:
        print("🚨 Format Violation: No new graduate table row found in GRADUATES.md additions.")
        return False

    # Validate each added row format
    valid_rows = 0
    for row in added_table_rows:
        cols = [c.strip() for c in row.split("|")[1:-1]]
        if len(cols) < 5:
            print(f"🚨 Format Violation: Table row has insufficient columns (expected 6, found {len(cols)}):")
            print(f"   Row: {row}")
            return False
            
        first_col = cols[0]
        if not re.search(r"\[@?[\w\-\.]+\]\(https?://github\.com/[\w\-\.]+\)", first_col):
            print(f"🚨 Format Violation: First column must contain markdown link to GitHub profile [@username](https://github.com/username):")
            print(f"   Found: {first_col}")
            return False
            
        valid_rows += 1

    print(f"✅ Success! Validated {valid_rows} graduate table entry row(s).")
    print("🎓 Graduate Pull Request verification passed with 100% compliance!")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify Graduate Pull Request")
    parser.add_argument("--base", default="origin/main", help="Base git ref")
    parser.add_argument("--head", default="HEAD", help="Head git ref")
    args = parser.parse_args()

    success = verify_graduate_pr(base_ref=args.base, head_ref=args.head)
    sys.exit(0 if success else 1)
