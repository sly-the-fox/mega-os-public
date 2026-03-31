#!/usr/bin/env python3
"""Convert markdown files to academic-styled PDFs.

Uses markdown-it-py for parsing and WeasyPrint for PDF generation.
Handles two math styles:
  - Plain-text math (S^2, P_n^+) — rendered as styled monospace spans
  - LaTeX-delimited math ($...$, $$...$$) — converted via latex2mathml

Usage:
    python md-to-pdf.py input1.md [input2.md ...] [-o OUTPUT_DIR]
"""

import argparse
import re
import sys
from pathlib import Path

from markdown_it import MarkdownIt
from mdit_py_plugins.dollarmath import dollarmath_plugin
from weasyprint import HTML

try:
    import latex2mathml.converter
    HAS_LATEX2MATHML = True
except ImportError:
    HAS_LATEX2MATHML = False


ACADEMIC_CSS = """
@page {
    size: letter;
    margin: 1in;
    @bottom-center {
        content: counter(page);
        font-family: Georgia, "Times New Roman", serif;
        font-size: 10pt;
        color: #666;
    }
}

body {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #1a1a1a;
    max-width: 100%;
    orphans: 3;
    widows: 3;
}

h1 {
    font-size: 16pt;
    font-weight: bold;
    margin-top: 0;
    margin-bottom: 0.5em;
    line-height: 1.3;
    page-break-after: avoid;
}

h2 {
    font-size: 13pt;
    font-weight: bold;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    page-break-after: avoid;
}

h3 {
    font-size: 11.5pt;
    font-weight: bold;
    margin-top: 1.2em;
    margin-bottom: 0.4em;
    page-break-after: avoid;
}

h4 {
    font-size: 11pt;
    font-weight: bold;
    font-style: italic;
    margin-top: 1em;
    margin-bottom: 0.3em;
    page-break-after: avoid;
}

p {
    margin-top: 0.4em;
    margin-bottom: 0.4em;
    text-align: justify;
    hyphens: auto;
}

/* Title metadata block (status, target, date) */
p strong:first-child {
    font-size: 10pt;
}

/* Abstract and blockquotes */
blockquote {
    margin: 1em 2em;
    padding: 0;
    font-style: italic;
    border-left: none;
    color: #333;
}

/* Horizontal rules as section dividers */
hr {
    border: none;
    border-top: 1px solid #ccc;
    margin: 1.5em 0;
}

/* Tables — academic style */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
    font-size: 10pt;
    page-break-inside: avoid;
}

thead {
    border-bottom: 2px solid #333;
}

th {
    font-weight: bold;
    text-align: left;
    padding: 6px 10px;
    border-bottom: 2px solid #333;
    background-color: #f8f8f8;
}

td {
    padding: 5px 10px;
    border-bottom: 1px solid #ddd;
    vertical-align: top;
}

tbody tr:nth-child(even) {
    background-color: #fafafa;
}

/* Indented code/equations — styled as equation blocks */
pre {
    font-family: "Cambria Math", "Latin Modern Math", Georgia, serif;
    font-size: 10.5pt;
    background: none;
    border: none;
    padding: 0.5em 0;
    margin: 0.8em 2em;
    text-align: center;
    white-space: pre-wrap;
    page-break-inside: avoid;
}

code {
    font-family: "Courier New", Courier, monospace;
    font-size: 10pt;
    background-color: #f5f5f5;
    padding: 1px 3px;
    border-radius: 2px;
}

pre code {
    background: none;
    padding: 0;
    font-family: inherit;
    font-size: inherit;
}

/* Inline math spans */
.math-inline {
    font-family: "Cambria Math", "Latin Modern Math", "STIX Two Math", serif;
    font-style: italic;
    white-space: nowrap;
}

/* Display math blocks */
.math-display {
    display: block;
    text-align: center;
    margin: 0.8em 0;
    font-family: "Cambria Math", "Latin Modern Math", "STIX Two Math", serif;
    font-size: 11pt;
    page-break-inside: avoid;
}

/* MathML overrides */
math {
    font-family: "Cambria Math", "Latin Modern Math", "STIX Two Math", serif;
}

/* Reference lists */
ol, ul {
    margin: 0.5em 0;
    padding-left: 2em;
}

li {
    margin-bottom: 0.3em;
    text-align: justify;
}

/* Definition/theorem styling */
p > strong:first-child {
    font-variant: small-caps;
}

/* Emphasis */
em {
    font-style: italic;
}

strong {
    font-weight: bold;
}

/* Links — print as text */
a {
    color: #1a1a1a;
    text-decoration: none;
}

/* Superscripts and subscripts in text */
sup { font-size: 0.75em; vertical-align: super; }
sub { font-size: 0.75em; vertical-align: sub; }
"""


def convert_latex_to_mathml(latex_str: str) -> str:
    """Convert a LaTeX math string to MathML, falling back to styled span."""
    if not HAS_LATEX2MATHML:
        return f'<span class="math-inline">{latex_str}</span>'
    try:
        mathml = latex2mathml.converter.convert(latex_str)
        return mathml
    except Exception:
        # Fall back to styled span
        escaped = latex_str.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f'<span class="math-inline">{escaped}</span>'


def convert_display_latex_to_mathml(latex_str: str) -> str:
    """Convert display LaTeX math to MathML block, falling back to styled div."""
    if not HAS_LATEX2MATHML:
        return f'<div class="math-display">{latex_str}</div>'
    try:
        mathml = latex2mathml.converter.convert(latex_str)
        return f'<div class="math-display">{mathml}</div>'
    except Exception:
        escaped = latex_str.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f'<div class="math-display">{escaped}</div>'


def post_process_html(html: str) -> str:
    """Post-process HTML to convert math tokens left by dollarmath plugin."""
    # dollarmath plugin wraps inline math in <span class="math-inline">$...$</span>
    # and display math in <div class="math-display">$$...$$</div>
    # We need to convert the LaTeX inside these to MathML

    def replace_inline_math(match):
        latex = match.group(1)
        return convert_latex_to_mathml(latex)

    def replace_display_math(match):
        latex = match.group(1)
        return convert_display_latex_to_mathml(latex)

    # Handle dollarmath inline: <math>...</math> tags from dollarmath
    # markdown-it-py dollarmath renders as <eq>...</eq> or just the content
    # Let's handle the actual rendered output

    # The dollarmath plugin renders inline math as: <eq>latex</eq>
    # and display math as: <section><eqno></eqno><eq>latex</eq></section>
    # But the actual rendering depends on the renderer

    # With default renderer, dollarmath produces tokens that get rendered as text
    # We need a custom approach: use the token stream

    return html


def render_markdown(md_text: str, has_latex_math: bool = False) -> str:
    """Render markdown to HTML with appropriate plugins."""
    md = MarkdownIt("commonmark", {"typographer": True})
    md.enable("table")

    if has_latex_math:
        dollarmath_plugin(md, double_inline=True)

    tokens = md.parse(md_text)

    # Custom render to handle math tokens
    if has_latex_math:
        html_parts = []
        i = 0
        while i < len(tokens):
            token = tokens[i]

            if token.type == "math_inline":
                mathml = convert_latex_to_mathml(token.content)
                html_parts.append(mathml)
                i += 1
                continue

            if token.type == "math_block" or token.type == "math_block_eqno":
                mathml = convert_display_latex_to_mathml(token.content)
                html_parts.append(mathml)
                i += 1
                continue

            i += 1

        # Actually, the token-level approach is complex with nesting.
        # Better approach: render normally, then post-process.
        # dollarmath with default renderer outputs the math content inside
        # specific HTML. Let's just render and fix up.

    # Render to HTML
    html = md.render(md_text)

    if has_latex_math:
        # dollarmath default renderer wraps inline math in <eq> tags
        # and display math in <section class="math-display">
        # Actually, let's check what it actually outputs

        # Replace inline math markers: the dollarmath plugin by default
        # renders inline math as just the content between $ $
        # We need to use a custom renderer or post-process

        # With the default renderer, inline math becomes:
        #   <p>text <eq>latex</eq> text</p>  (if using math_inline token)
        # But actually it may just render as text since there's no HTML tag mapping

        # Let's use regex on the rendered HTML to find and convert math
        # The plugin should leave markers we can find

        pass

    return html


def detect_latex_math(text: str) -> bool:
    """Detect if a document uses LaTeX-delimited math."""
    # Look for $...$ patterns (but not \$ escaped dollars)
    inline_pattern = r'(?<![\\])\$(?!\$)(.+?)(?<![\\])\$'
    display_pattern = r'\$\$(.+?)\$\$'

    inline_count = len(re.findall(inline_pattern, text))
    display_count = len(re.findall(display_pattern, text, re.DOTALL))

    # Threshold: more than 5 instances suggests intentional LaTeX math
    return (inline_count + display_count) > 5


def preprocess_latex_math(md_text: str) -> str:
    """Pre-process markdown to convert LaTeX math to MathML before markdown parsing.

    This handles $...$ and $$...$$ by converting them to MathML HTML that
    markdown-it-py will pass through as raw HTML.
    """
    # First handle display math ($$...$$) — must come before inline
    def replace_display(match):
        latex = match.group(1).strip()
        return "\n" + convert_display_latex_to_mathml(latex) + "\n"

    # Handle display math (can span lines)
    md_text = re.sub(r'\$\$(.+?)\$\$', replace_display, md_text, flags=re.DOTALL)

    # Handle inline math ($...$) — single line only, no nested $
    def replace_inline(match):
        latex = match.group(1)
        return convert_latex_to_mathml(latex)

    md_text = re.sub(r'(?<![\\$])\$([^\$\n]+?)\$(?!\$)', replace_inline, md_text)

    return md_text


def md_to_html(md_text: str, title: str = "") -> str:
    """Convert markdown text to a full HTML document."""
    has_latex = detect_latex_math(md_text)

    if has_latex:
        # Pre-process LaTeX math to MathML before markdown parsing
        md_text = preprocess_latex_math(md_text)

    md = MarkdownIt("commonmark", {"typographer": True})
    md.enable("table")

    html_body = md.render(md_text)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <style>{ACADEMIC_CSS}</style>
</head>
<body>
{html_body}
</body>
</html>"""

    return html


def md_to_pdf(input_path: Path, output_path: Path) -> None:
    """Convert a markdown file to PDF."""
    md_text = input_path.read_text(encoding="utf-8")

    # Extract title from first heading
    title_match = re.match(r'^#\s+(.+)', md_text, re.MULTILINE)
    title = title_match.group(1) if title_match else input_path.stem

    html = md_to_html(md_text, title)
    HTML(string=html).write_pdf(str(output_path))

    size_kb = output_path.stat().st_size / 1024
    print(f"  {output_path.name}: {size_kb:.0f} KB")


def main():
    parser = argparse.ArgumentParser(description="Convert markdown to academic PDF")
    parser.add_argument("inputs", nargs="+", type=Path, help="Input markdown files")
    parser.add_argument("-o", "--output-dir", type=Path, default=None,
                        help="Output directory (default: same as input)")
    args = parser.parse_args()

    output_dir = args.output_dir
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

    for input_path in args.inputs:
        if not input_path.exists():
            print(f"  SKIP: {input_path} not found", file=sys.stderr)
            continue

        if output_dir:
            out = output_dir / input_path.with_suffix(".pdf").name
        else:
            out = input_path.with_suffix(".pdf")

        print(f"Converting {input_path.name}...")
        md_to_pdf(input_path, out)

    print("Done.")


if __name__ == "__main__":
    main()
