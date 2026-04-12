#!/usr/bin/env python3
"""Generate a workspace index.html that links to all HTML files recursively.

Usage:
    python generate_index.py
    python generate_index.py --root /path/to/workspace --output /path/to/index.html
"""

from __future__ import annotations

import argparse
import html
import os
import re
import shutil
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


def render_tree(node: dict[str, object], root: Path, base_path: Path, depth: int = 0) -> str:
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
        child_content = render_tree(child, root, base_path, depth + 2)
        if child_content:
            lines.append(child_content)
        lines.append(f"{indent}  </ul>")
        lines.append(f"{indent}</details>")

    for path in sorted(files, key=lambda p: p.name.lower()):
        rel = Path(os.path.relpath(path, start=base_path)).as_posix()
        title = title_from_filename(path)
        escaped_title = html.escape(title)
        escaped_rel = html.escape(rel)
        lines.append(f"{indent}<li>")
        lines.append(f'{indent}  <a href="{escaped_rel}">{escaped_title}</a>')
        lines.append(f"{indent}</li>")

    return "\n".join(lines)


def find_html_files(root: Path, output_file: Path, exclude_dirs: list[Path] | None = None) -> list[Path]:
    """Find all HTML files under root, excluding the generated output file and optional folders."""
    html_files: list[Path] = []
    exclude_dirs = exclude_dirs or []

    for path in root.rglob("*.html"):
        if path.resolve() == output_file.resolve():
            continue
        if any(excluded in path.parents for excluded in exclude_dirs):
            continue
        if path.is_file():
            html_files.append(path)

    # Sort by relative path so output is stable across runs
    html_files.sort(key=lambda p: str(p.relative_to(root)).lower())
    return html_files


def find_markdown_files(root: Path, exclude_dirs: list[Path] | None = None) -> list[Path]:
    """Find all Markdown files under root, excluding optional folders."""
    markdown_files: list[Path] = []
    exclude_dirs = exclude_dirs or []

    for path in root.rglob("*.md"):
        if any(excluded in path.parents for excluded in exclude_dirs):
            continue
        if path.is_file():
            markdown_files.append(path)

    # Sort by relative path so output is stable across runs
    markdown_files.sort(key=lambda p: str(p.relative_to(root)).lower())
    return markdown_files


def extract_markdown_title(markdown_text: str) -> str | None:
    for line in markdown_text.splitlines():
        match = re.match(r"^\s*#\s+(.*)", line)
        if match:
            return match.group(1).strip()
    return None


def inline_markdown(text: str) -> str:
    text = html.escape(text)
    # Images before links so they don't get eaten by link regex
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r"<img alt=\"\1\" src=\"\2\">", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"<a href=\"\2\">\1</a>", text)
    text = re.sub(r"`([^`]+?)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"__(.+?)__", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"_(.+?)_", r"<em>\1</em>", text)
    return text


def markdown_to_html_fallback(markdown_text: str) -> str:
    lines = markdown_text.splitlines()
    html_lines: list[str] = []
    in_code_block = False
    code_lines: list[str] = []
    in_paragraph = False
    in_list = False
    list_tag = ""
    in_blockquote = False

    def close_paragraph() -> None:
        nonlocal in_paragraph
        if in_paragraph:
            html_lines.append("</p>")
            in_paragraph = False

    def close_list() -> None:
        nonlocal in_list, list_tag
        if in_list:
            html_lines.append(f"</{list_tag}>")
            in_list = False
            list_tag = ""

    def close_blockquote() -> None:
        nonlocal in_blockquote
        if in_blockquote:
            html_lines.append("</blockquote>")
            in_blockquote = False

    for line in lines:
        stripped = line.strip()
        if in_code_block:
            if stripped.startswith("```"):
                html_lines.append("<pre><code>")
                html_lines.extend(html.escape(code_line) for code_line in code_lines)
                html_lines.append("</code></pre>")
                in_code_block = False
                code_lines = []
                continue
            code_lines.append(line)
            continue

        if stripped.startswith("```"):
            close_paragraph()
            close_list()
            close_blockquote()
            in_code_block = True
            code_lines = []
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.*)", line)
        if heading_match:
            close_paragraph()
            close_list()
            close_blockquote()
            level = len(heading_match.group(1))
            content = inline_markdown(heading_match.group(2).strip())
            html_lines.append(f"<h{level}>{content}</h{level}>")
            continue

        blockquote_match = re.match(r"^>\s?(.*)", line)
        if blockquote_match:
            close_paragraph()
            close_list()
            if not in_blockquote:
                html_lines.append("<blockquote>")
                in_blockquote = True
            html_lines.append(f"<p>{inline_markdown(blockquote_match.group(1).strip())}</p>")
            continue

        list_match = re.match(r"^\s*([-+*]|\d+\.)\s+(.*)", line)
        if list_match:
            close_paragraph()
            target_tag = "ol" if list_match.group(1).endswith(".") else "ul"
            if not in_list or list_tag != target_tag:
                close_list()
                list_tag = target_tag
                html_lines.append(f"<{list_tag}>")
                in_list = True
            html_lines.append(f"<li>{inline_markdown(list_match.group(2).strip())}</li>")
            continue

        if stripped == "":
            close_paragraph()
            close_list()
            close_blockquote()
            continue

        if not in_paragraph:
            close_list()
            close_blockquote()
            html_lines.append("<p>")
            in_paragraph = True

        html_lines.append(inline_markdown(stripped))

    if in_code_block:
        html_lines.append("<pre><code>")
        html_lines.extend(html.escape(code_line) for code_line in code_lines)
        html_lines.append("</code></pre>")

    close_paragraph()
    close_list()
    close_blockquote()

    return "\n".join(html_lines)


def markdown_to_html(markdown_text: str) -> str:
    try:
        import markdown as md
    except ImportError:
        return markdown_to_html_fallback(markdown_text)

    try:
        return md.markdown(
            markdown_text,
            extensions=[
                "fenced_code",
                "tables",
                "nl2br",
                "sane_lists",
                "attr_list",
            ],
        )
    except Exception:
        return markdown_to_html_fallback(markdown_text)


def build_markdown_page(title: str, body_html: str, source_path: Path) -> str:
    display_path = html.escape(str(source_path).replace('\\', '/'))
    return f"""<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>{html.escape(title)}</title>
    <style>
      :root {{
        --bg: #f6f8fb;
        --card: #ffffff;
        --text: #1f2937;
        --muted: #6b7280;
        --accent: #0f766e;
        --border: #e5e7eb;
        --code-bg: #f8fafc;
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
        padding: 28px;
      }}

      h1, h2, h3, h4, h5, h6 {{
        color: #0f766e;
        margin: 1.5rem 0 0.75rem;
      }}

      p {{
        line-height: 1.8;
        margin: 0 0 1rem;
      }}

      blockquote {{
        margin: 1rem 0;
        padding: 1rem 1.25rem;
        background: #e0f2fe;
        border-left: 4px solid #0f766e;
      }}

      pre {{
        background: var(--code-bg);
        padding: 1rem;
        overflow-x: auto;
        border-radius: 10px;
      }}

      code {{
        background: var(--code-bg);
        padding: 0.2rem 0.35rem;
        border-radius: 6px;
      }}

      ul, ol {{
        margin: 0 0 1rem 1.3rem;
      }}

      a {{
        color: var(--accent);
        text-decoration: none;
      }}

      a:hover {{
        text-decoration: underline;
      }}

      .meta {{
        color: var(--muted);
        margin-bottom: 1.25rem;
      }}

      .topbar {{
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        margin-bottom: 1rem;
      }}

      .topbar a {{
        font-weight: 700;
      }}
    </style>
  </head>
  <body>
    <main class="container">
      <section class="card">
        <div class="topbar">
          <div>
            <a href="javascript:history.back()">← Quay lại</a>
          </div>
          <div class="meta">Source: {display_path}</div>
        </div>
        <h1>{html.escape(title)}</h1>
        <article class="markdown-body">
{body_html}
        </article>
      </section>
    </main>
  </body>
</html>
"""


def generate_markdown_html_files(root: Path, markdown_files: list[Path], output_dir: Path) -> list[Path]:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_files: list[Path] = []
    markdown_root = root / "markdown"

    for markdown_path in markdown_files:
        if markdown_path.is_relative_to(markdown_root):
            rel = markdown_path.relative_to(markdown_root)
        else:
            rel = markdown_path.relative_to(root)

        output_path = output_dir / rel.with_suffix(".html")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        source_text = markdown_path.read_text(encoding="utf-8")
        title = extract_markdown_title(source_text) or title_from_filename(markdown_path)
        body_html = markdown_to_html(source_text)
        output_path.write_text(build_markdown_page(title, body_html, markdown_path), encoding="utf-8")
        output_files.append(output_path)

    return output_files


def build_index_html(root: Path, html_files: list[Path], markdown_files: list[Path], base_path: Path) -> str:
    """Create the index page HTML content."""
    # Build separate trees for HTML and Markdown files
    html_tree = build_tree(root, html_files)
    markdown_tree = build_tree(root, markdown_files)
    
    html_tree_html = render_tree(html_tree, root, base_path, depth=4)
    markdown_tree_html = render_tree(markdown_tree, root, base_path, depth=4)

    if not html_tree_html:
        html_tree_html = "        <li><em>Khong tim thay file HTML nao.</em></li>"
    
    if not markdown_tree_html:
        markdown_tree_html = "        <li><em>Khong tim thay file Markdown nao.</em></li>"

    file_count = len(html_files) + len(markdown_files)
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

      .category-summary {{
        font-weight: 700;
        color: #0b4f4a;
        font-size: 1.1em;
      }}

    </style>
  </head>
  <body>
    <main class=\"container\">
      <section class=\"card\">
        <h1>Workspace Index</h1>
        <p class=\"meta\">Tu dong tao theo folder/subfolder. Mac dinh dang collapse.</p>
        <ul>
          <li>
            <details class="folder" open>
              <summary><span class="category-summary">📄 HTML Files</span> <span class="count">({len(html_files)})</span></summary>
              <ul>
{html_tree_html}
              </ul>
            </details>
          </li>
          <li>
            <details class="folder">
              <summary><span class="category-summary">📝 Markdown Files</span> <span class="count">({len(markdown_files)})</span></summary>
              <ul>
{markdown_tree_html}
              </ul>
            </details>
          </li>
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
    output = args.output.resolve() if args.output else (root / "html" / "index.html")
    markdown_output_dir = output.parent / "markdown"

    markdown_source_files = find_markdown_files(root, exclude_dirs=[markdown_output_dir])
    markdown_files = generate_markdown_html_files(root, markdown_source_files, markdown_output_dir)
    html_files = find_html_files(root, output, exclude_dirs=[markdown_output_dir])
    content = build_index_html(root, html_files, markdown_files, output.parent)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")

    print(f"Da tao index: {output}")
    print(f"Tong so trang HTML: {len(html_files)}")
    print(f"Tong so trang Markdown: {len(markdown_files)}")
    print(f"Tong cong: {len(html_files) + len(markdown_files)} trang")


if __name__ == "__main__":
    main()
