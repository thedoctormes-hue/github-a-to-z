#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated Link Integrity & Anchor Validator for github-a-to-z
Validates all markdown relative paths, anchors, and cross-references.
Standard library only, zero external dependencies.
"""

import os
import re
import sys
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent

def strip_markdown(text: str) -> str:
    """Strip markdown formatting from heading text."""
    text = re.sub(r'!\[([^\]]*)\]\([^\)]*\)', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^\)]*\)', r'\1', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'\*{1,3}([^*]+)\*{1,3}', r'\1', text)
    return text.strip()

def gh_slugify(text: str) -> str:
    """Compute GitHub markdown heading anchor slug."""
    text = strip_markdown(text).lower()
    chars = []
    for c in text:
        if c.isalnum() or c == ' ' or c == '-' or c == '_':
            chars.append(c)
        elif c in "!\"#$%&'()*+,./:;<=>?@[\\]^`{|}~":
            continue
        elif ord(c) > 127:
            if c.isalnum() or c == '_':
                chars.append(c)
        else:
            continue
    slug = "".join(chars)
    slug = re.sub(r'\s+', '-', slug.strip())
    return slug

def parse_headings_and_anchors(file_path: Path) -> Set[str]:
    """Parse all headings in file and compute their GitHub slug anchors."""
    content = file_path.read_text(encoding="utf-8", errors="ignore")
    anchors = set()
    slug_counts = defaultdict(int)

    # HTML explicit anchors
    for a in re.findall(r'<a\s+[^>]*(?:name|id)=["\']([^"\']+)["\']', content):
        anchors.add(a)

    in_code_block = False
    for line in content.splitlines():
        line_strip = line.strip()
        if line_strip.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            heading_text = m.group(2).strip()
            custom_id = re.search(r'\{#([^}]+)\}\s*$', heading_text)
            if custom_id:
                anchors.add(custom_id.group(1))
                heading_text = heading_text[:custom_id.start()].strip()
            
            base_slug = gh_slugify(heading_text)
            if not base_slug:
                continue
            
            count = slug_counts[base_slug]
            slug_counts[base_slug] += 1
            if count == 0:
                anchors.add(base_slug)
            else:
                anchors.add(f"{base_slug}-{count}")

    return anchors

def find_links_in_file(file_path: Path) -> List[Tuple[int, str, str]]:
    """Extract all markdown and html links from a file."""
    content = file_path.read_text(encoding="utf-8", errors="ignore")
    links = []
    in_code_block = False

    for line_idx, line in enumerate(content.splitlines(), start=1):
        line_strip = line.strip()
        if line_strip.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        for m in re.finditer(r'(?<!!)\[([^\]]*)\]\(([^)]+)\)', line):
            text = m.group(1)
            target = m.group(2).strip()
            target = re.sub(r'\s+"[^"]*"$', '', target)
            target = re.sub(r"\s+'[^']*'$", '', target)
            links.append((line_idx, text, target))

        for m in re.finditer(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', line):
            links.append((line_idx, m.group(2), m.group(1).strip()))

    return links

def validate_repository() -> int:
    """Run full link and anchor validation across all markdown files."""
    md_files = list(REPO_ROOT.glob("**/*.md"))
    md_files = [f for f in md_files if ".git" not in f.parts and "node_modules" not in f.parts and ".system_generated" not in f.parts]
    
    print(f"🔍 Validating {len(md_files)} markdown files in {REPO_ROOT}...")

    file_anchors: Dict[Path, Set[str]] = {}
    for md_file in md_files:
        file_anchors[md_file] = parse_headings_and_anchors(md_file)

    issues = []
    total_links = 0

    for md_file in sorted(md_files):
        rel_src = md_file.relative_to(REPO_ROOT)
        links = find_links_in_file(md_file)

        for line_num, link_text, target in links:
            total_links += 1

            if target in ("#", ""):
                continue

            if target.startswith(("http://", "https://", "mailto:")):
                continue

            # Pure local anchor
            if target.startswith("#"):
                anchor = target[1:]
                if anchor not in file_anchors[md_file]:
                    issues.append({
                        "file": str(rel_src),
                        "line": line_num,
                        "type": "BROKEN_LOCAL_ANCHOR",
                        "target": target
                    })
                continue

            # Relative path
            if "#" in target:
                target_file_str, anchor = target.split("#", 1)
            else:
                target_file_str, anchor = target, None

            if target_file_str.startswith("/"):
                resolved_path = (REPO_ROOT / target_file_str.lstrip("/")).resolve()
            else:
                resolved_path = (md_file.parent / target_file_str).resolve()

            if resolved_path.is_dir():
                readme_inside = resolved_path / "README.md"
                if not readme_inside.exists():
                    issues.append({
                        "file": str(rel_src),
                        "line": line_num,
                        "type": "BROKEN_DIR_LINK",
                        "target": target
                    })
                elif anchor and anchor not in file_anchors.get(readme_inside, set()):
                    issues.append({
                        "file": str(rel_src),
                        "line": line_num,
                        "type": "BROKEN_REMOTE_ANCHOR",
                        "target": target
                    })
            elif not resolved_path.exists():
                issues.append({
                    "file": str(rel_src),
                    "line": line_num,
                    "type": "MISSING_FILE",
                    "target": target
                })
            else:
                if anchor and resolved_path in file_anchors and anchor not in file_anchors[resolved_path]:
                    issues.append({
                        "file": str(rel_src),
                        "line": line_num,
                        "type": "BROKEN_REMOTE_ANCHOR",
                        "target": target
                    })

    print(f"📊 Total links validated: {total_links}")
    if issues:
        print(f"🚨 Found {len(issues)} broken link issues:")
        for iss in issues:
            print(f"  - [{iss['type']}] {iss['file']}:{iss['line']} -> {iss['target']}")
        return 1

    print("✅ All links and anchors are 100% valid. Zero broken transitions found!")
    return 0

if __name__ == "__main__":
    sys.exit(validate_repository())
