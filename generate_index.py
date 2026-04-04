#!/usr/bin/env python3
"""Generate a workspace index.html that links to all HTML files recursively.

Usage:
    python generate_index.py
    python generate_index.py --root /path/to/workspace --output /path/to/index.html
"""

from __future__ import annotations

import argparse
import html
from pathlib import Path


def title_from_filename(path: Path) -> str:
    """Build a readable title from filename only."""
    return path.stem.replace("_", " ")


def new_tree_node() -> dict[str, object]:
    """Create an in-memory node for folder tree rendering."""
    return {"folders": {}, "files": []}


def build_tree(root: Path, html_files: list[Path]) -> dict[str, object]:
    """Build a nested tree from discovered HTML paths."""
    tree = new_tree_node()

    for path in html_files:
        rel = path.relative_to(root)
        folders = rel.parts[:-1]
        node = tree

        for folder in folders:
            folder_map = node["folders"]
            if folder not in folder_map:
                folder_map[folder] = new_tree_node()
            node = folder_map[folder]

        node["files"].append(path)

    return tree


def count_files(node: dict[str, object]) -> int:
    """Count files recursively for folder badges."""
    total = len(node["files"])
    for child in node["folders"].values():
        total += count_files(child)
    return total


def render_tree(node: dict[str, object], root: Path, depth: int = 0) -> str:
    """Render nested folder and file entries as collapsible HTML."""
    lines: list[str] = []
    indent = "  " * depth

    folders: dict[str, dict[str, object]] = node["folders"]
    files: list[Path] = node["files"]

    for folder_name in sorted(folders.keys(), key=lambda s: s.lower()):
        child = folders[folder_name]
        file_count = count_files(child)
        escaped_folder = html.escape(folder_name.replace("_", " "))

        lines.append(f'{indent}<details class="folder">')
        lines.append(
            f'{indent}  <summary>{escaped_folder} <span class="count">({file_count})</span></summary>'
        )
        lines.append(f"{indent}  <ul>")
        child_content = render_tree(child, root, depth + 2)
        if child_content:
            lines.append(child_content)
        lines.append(f"{indent}  </ul>")
        lines.append(f"{indent}</details>")

    for path in sorted(files, key=lambda p: p.name.lower()):
        rel = path.relative_to(root).as_posix()
        title = title_from_filename(path)
        escaped_title = html.escape(title)
        escaped_rel = html.escape(rel)
        lines.append(f"{indent}<li>")
        lines.append(f'{indent}  <a href="{escaped_rel}">{escaped_title}</a>')
        lines.append(f"{indent}</li>")

    return "\n".join(lines)


def find_html_files(root: Path, output_file: Path) -> list[Path]:
    """Find all HTML files under root, excluding the generated output file."""
    html_files: list[Path] = []

    for path in root.rglob("*.html"):
        if path.resolve() == output_file.resolve():
            continue
        if path.is_file():
            html_files.append(path)

    # Sort by relative path so output is stable across runs
    html_files.sort(key=lambda p: str(p.relative_to(root)).lower())
    return html_files


def build_index_html(root: Path, html_files: list[Path]) -> str:
    """Create the index page HTML content."""
    tree = build_tree(root, html_files)
    tree_html = render_tree(tree, root, depth=3)

    if not tree_html:
        tree_html = "      <li><em>Khong tim thay file HTML nao.</em></li>"

    return f"""<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>HTML Index</title>
    <style>
      :root {{
        --bg: #f6f8fb;
        --card: #ffffff;
        --text: #1f2937;
        --muted: #6b7280;
        --accent: #0f766e;
        --border: #e5e7eb;
      }}

      body {{
        margin: 0;
        font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
        color: var(--text);
        background: linear-gradient(140deg, #edf2ff 0%, var(--bg) 45%, #ecfeff 100%);
      }}

      .container {{
        max-width: 980px;
        margin: 32px auto;
        padding: 0 16px 32px;
      }}

      .card {{
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 14px;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
        padding: 20px;
      }}

      h1 {{
        margin: 0 0 8px;
        font-size: 28px;
      }}

      .meta {{
        margin: 0 0 18px;
        color: var(--muted);
      }}

      ul {{
        margin: 0;
        padding-left: 20px;
      }}

      details {{
        margin: 10px 0;
      }}

      summary {{
        cursor: pointer;
        font-weight: 700;
        color: #0b4f4a;
        user-select: none;
      }}

      .count {{
        color: var(--muted);
        font-weight: 500;
      }}

      li {{
        margin: 10px 0;
      }}

      a {{
        text-decoration: none;
        color: var(--accent);
        font-weight: 600;
      }}

      a:hover {{
        text-decoration: underline;
      }}

    </style>
  </head>
  <body>
    <main class=\"container\">
      <section class=\"card\">
        <h1>HTML Pages</h1>
        <p class=\"meta\">Tu dong tao theo folder/subfolder. Mac dinh dang collapse.</p>
        <ul>
{tree_html}
        </ul>
      </section>
    </main>
  </body>
</html>
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate index.html for all HTML files.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Workspace root to scan (default: current directory).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output index file path (default: <root>/index.html).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    root = args.root.resolve()
    output = args.output.resolve() if args.output else (root / "index.html")

    html_files = find_html_files(root, output)
    content = build_index_html(root, html_files)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")

    print(f"Da tao index: {output}")
    print(f"Tong so trang HTML: {len(html_files)}")


if __name__ == "__main__":
    main()
