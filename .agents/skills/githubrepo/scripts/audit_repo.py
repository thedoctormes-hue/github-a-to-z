#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GITHUBREPO Wrapper: maintains Single Source of Truth with scripts/audit_repo.py
Official CLI companion and quality standard for «GitHub from A to Z» (TheNovaNodes)
"""
import sys
from pathlib import Path

# Resolve repository root and inject scripts/ into sys.path
_current_dir = Path(__file__).resolve().parent
_repo_root = _current_dir.parents[3]
_scripts_dir = _repo_root / "scripts"

if _scripts_dir.is_dir() and str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))

try:
    from audit_repo import main, audit_repository, format_markdown_report, parse_repo_slug
except ImportError:
    # Fallback to system-wide binary if running standalone in external environment
    if Path("/usr/local/bin/audit_repo.py").is_file():
        sys.path.insert(0, "/usr/local/bin")
        from audit_repo import main, audit_repository, format_markdown_report, parse_repo_slug
    else:
        raise

if __name__ == "__main__":
    main()
