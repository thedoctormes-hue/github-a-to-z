#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated Link Integrity & Anchor Validator for github-a-to-z
Validates all markdown relative paths, anchors, and cross-references.
Optionally verifies external HTTP/HTTPS resources via --check-external.
Standard library only, zero external dependencies.
"""

import os
import re
import sys
import json
import argparse
import urllib.request
import urllib.error
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

        match = re.match(r'^(#{1,6})\s+(.+)$', line_strip)
        if match:
            heading_text = match.group(2).strip()
            # Check for custom anchor in heading e.g. {#custom-id}
            custom_anchor = re.search(r'\{#([^\}]+)\}', heading_text)
            if custom_anchor:
                anchors.add(custom_anchor.group(1))
                heading_text = re.sub(r'\{#[^\}]+\}', '', heading_text).strip()

            base_slug = gh_slugify(heading_text)
            if base_slug:
                count = slug_counts[base_slug]
                slug_counts[base_slug] += 1
                final_slug = base_slug if count == 0 else f"{base_slug}-{count}"
                anchors.add(final_slug)

    return anchors

def find_links_in_file(file_path: Path) -> List[Tuple[int, str, str]]:
    """Return all markdown links in file: (line_num, link_text, link_target)."""
    content = file_path.read_text(encoding="utf-8", errors="ignore")
    links = []
    in_code_block = False

    link_pattern = re.compile(r'(?<!!)\[([^\]]*)\]\(([^)]+)\)')

    for idx, line in enumerate(content.splitlines(), start=1):
        line_strip = line.strip()
        if line_strip.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        for m in link_pattern.finditer(line):
            text = m.group(1).strip()
            target = m.group(2).strip()
            target = target.split()[0]  # Remove optional title
            links.append((idx, text, target))

    return links

def check_external_url(url: str, timeout: int = 5) -> Tuple[bool, str]:
    """Test validity of external URL via HTTP HEAD / GET."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*'
    }
    try:
        req = urllib.request.Request(url, headers=headers, method='HEAD')
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return True, f"HTTP {resp.status}"
    except urllib.error.HTTPError as e:
        if e.code in (403, 405, 429):
            try:
                req = urllib.request.Request(url, headers=headers, method='GET')
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    return True, f"HTTP {resp.status}"
            except Exception as e_get:
                return False, str(e_get)
        elif e.code in (301, 302, 307, 308):
            return True, f"HTTP {e.code}"
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, str(e)

def validate_repository(check_external: bool = False) -> int:
    """Full repository validation of all markdown links."""
    md_files = list(REPO_ROOT.glob("**/*.md"))
    md_files = [f for f in md_files if ".git" not in f.parts and "node_modules" not in f.parts and ".system_generated" not in f.parts and "book" not in f.parts]
    
    print(f"🔍 Validating {len(md_files)} markdown files in {REPO_ROOT} (Check External: {check_external})...")

    file_anchors: Dict[Path, Set[str]] = {}
    for md_file in md_files:
        file_anchors[md_file] = parse_headings_and_anchors(md_file)

    issues = []
    total_links = 0
    external_cache: Dict[str, Tuple[bool, str]] = {}

    for md_file in sorted(md_files):
        rel_src = md_file.relative_to(REPO_ROOT)
        links = find_links_in_file(md_file)

        for line_num, link_text, target in links:
            total_links += 1

            if target in ("#", ""):
                continue

            if target.startswith("mailto:"):
                continue

            if target.startswith(("http://", "https://")):
                if check_external:
                    clean_url = target.split('#')[0]
                    if clean_url not in external_cache:
                        print(f"  🌐 Checking external: {clean_url}...")
                        external_cache[clean_url] = check_external_url(clean_url)
                    is_ok, reason = external_cache[clean_url]
                    if not is_ok:
                        issues.append({
                            "file": str(rel_src),
                            "line": line_num,
                            "type": "BROKEN_EXTERNAL_LINK",
                            "target": f"{target} ({reason})"
                        })
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
    parser = argparse.ArgumentParser(description="Validate markdown links in repository")
    parser.add_argument("--check-external", action="store_true", help="Perform live HTTP checks on external URLs")
    args = parser.parse_args()

    sys.exit(validate_repository(check_external=args.check_external))
