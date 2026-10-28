# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Audit all tracked repository markdown documents for broken relative links and images."""

import os
import re
import subprocess
import sys
from urllib.parse import unquote


def run_audit() -> None:
    # Only audit markdown files tracked in this repository
    cmd = ["git", "ls-files", "*.md"]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    md_files = [line.strip() for line in res.stdout.splitlines() if line.strip()]

    print(f"Auditing {len(md_files)} repository markdown files for broken links and images...\n")

    md_link_regex = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    html_img_regex = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']')
    html_a_regex = re.compile(r'<a[^>]+href=["\']([^"\']+)["\']')

    broken_links = []
    broken_images = []
    valid_links_count = 0
    valid_images_count = 0

    for md_file in sorted(md_files):
        dir_name = os.path.dirname(md_file)
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Find markdown links [text](url)
        for text, url in md_link_regex.findall(content):
            url_clean = url.strip()
            if url_clean.startswith(("http://", "https://", "mailto:")):
                continue

            # Check anchor fragment
            parts = url_clean.split("#")
            path_part = parts[0]
            anchor_part = parts[1] if len(parts) > 1 else None

            if not path_part:
                target_file = md_file
            else:
                path_part = unquote(path_part)
                target_file = os.path.normpath(os.path.join(dir_name, path_part))

            if not os.path.exists(target_file):
                broken_links.append((md_file, text, url_clean, target_file))
            else:
                valid_links_count += 1
                if anchor_part:
                    with open(target_file, "r", encoding="utf-8") as tf:
                        tf_content = tf.read().lower()
                    headers = re.findall(r"^#+\s+(.+)$", tf_content, re.MULTILINE)
                    slugs = [re.sub(r"[^\w\- ]", "", h).strip().replace(" ", "-") for h in headers]
                    named_anchors = re.findall(
                        r'<a[^>]+(?:id|name)=["\']([^"\']+)["\']', tf_content
                    )
                    all_anchors = set(slugs + named_anchors)
                    if anchor_part.lower() not in all_anchors:
                        broken_links.append(
                            (
                                md_file,
                                text,
                                f"{url_clean} (anchor #{anchor_part} not found)",
                                target_file,
                            )
                        )

        # Find HTML <a href="...">
        for href in html_a_regex.findall(content):
            href_clean = href.strip()
            if href_clean.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_part = href_clean.split("#")[0]
            if not path_part:
                continue
            path_part = unquote(path_part)
            full_path = os.path.normpath(os.path.join(dir_name, path_part))
            if not os.path.exists(full_path):
                broken_links.append((md_file, f"<a href='{href}'>", href_clean, full_path))
            else:
                valid_links_count += 1

        # Find HTML <img src="...">
        for src in html_img_regex.findall(content):
            src_clean = src.strip()
            if src_clean.startswith(("http://", "https://")):
                continue
            path_part = src_clean.split("#")[0]
            path_part = unquote(path_part)
            full_path = os.path.normpath(os.path.join(dir_name, path_part))
            if not os.path.exists(full_path):
                broken_images.append((md_file, src_clean, full_path))
            else:
                valid_images_count += 1

    print("Summary:")
    print(f"  Valid relative links checked: {valid_links_count}")
    print(f"  Valid images checked: {valid_images_count}")
    print(f"  Broken links: {len(broken_links)}")
    print(f"  Broken images: {len(broken_images)}\n")

    if broken_links:
        print("Broken Links:")
        for source_file, text, url, resolved in broken_links:
            print(f"  [LINK] {source_file} -> '{url}' (resolved: {resolved})")

    if broken_images:
        print("Broken Images:")
        for source_file, src, resolved in broken_images:
            print(f"  [IMG]  {source_file} -> '{src}' (resolved: {resolved})")

    if broken_links or broken_images:
        sys.exit(1)

    print("All relative links and image references across all markdown files are 100% valid!")


if __name__ == "__main__":
    run_audit()
