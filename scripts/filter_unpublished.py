"""MkDocs hook to exclude Markdown pages marked with `publicar: false`."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

_FRONTMATTER_RE = re.compile(r"^\ufeff?---\r?\n(.*?)\r?\n---(?:\r?\n|$)", re.DOTALL)


def _is_unpublished(path: Path) -> bool:
    """Return True when a Markdown file defines `publicar: false` in YAML frontmatter."""
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return False

    match = _FRONTMATTER_RE.match(content)
    if not match:
        return False

    try:
        metadata: Any = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return False

    if not isinstance(metadata, dict):
        return False

    publish_flag = metadata.get("publicar")
    if publish_flag is False:
        return True
    if isinstance(publish_flag, str) and publish_flag.strip().lower() == "false":
        return True
    return False


def on_files(files, config):
    """Filter out documentation files whose frontmatter sets `publicar: false`."""
    to_remove = []
    for file in files:
        if not file.src_path.endswith(".md"):
            continue
        src_file = Path(file.abs_src_path)
        if _is_unpublished(src_file):
            to_remove.append(file)

    for file in to_remove:
        print(f"[filter_unpublished] Omitiendo página privada: {file.src_path}")
        files.remove(file)

    return files
