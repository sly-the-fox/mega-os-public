---
name: draw
description: Use when generating diagrams, charts, custom graphics, or manipulating images.
user_invocable: true
arguments:
  - name: description
    description: What to draw/create/manipulate
    required: true
  - name: type
    description: "Force a lane: diagram, chart, graphic, image"
    required: false
  - name: format
    description: "Output format: svg, png, pdf (default: svg for diagrams/graphics, png for charts/images)"
    required: false
  - name: output
    description: Custom output path (default: deliverables/visuals/)
    required: false
  - name: data
    description: Path to data file for charts
    required: false
---

# /draw — Visual Generation Skill

Generate diagrams, charts, custom graphics, and manipulate images from natural language descriptions.

## Routing Logic

Analyze the user's description and route to the correct rendering lane. If `--type` is provided, use that lane directly. Otherwise, match keywords:

### Lane 1: Diagram (Mermaid CLI)

**Keywords:** flowchart, sequence, ERD, entity relationship, Gantt, mind map, architecture, class diagram, state diagram, git graph, timeline, journey, pie chart (simple), quadrant, sankey, block

**Process:**
1. Translate the user's description into valid Mermaid syntax
2. Write the `.mmd` file to `drafts/visuals/<kebab-name>.mmd`
3. Determine output format (default: `svg`; respect `--format` if given)
4. Determine output path (default: `deliverables/visuals/<kebab-name>.<format>`; respect `--output` if given)
5. Render using the wrapper script:
   ```bash
   bash engineering/scripts/draw-mermaid.sh drafts/visuals/<name>.mmd <output-path>
   ```
6. Read the output file to confirm it was created successfully
7. Report: source file path, output file path, and what was rendered

### Lane 2: Chart (matplotlib)

**Keywords:** chart, plot, graph, histogram, scatter, bar chart, line chart, pie chart (data-driven), heatmap, data viz, visualization, distribution, trend

**Process:**
1. If `--data` is provided, read the data file first
2. Write a Python script to `drafts/visuals/<kebab-name>.py` that:
   - Imports matplotlib (and numpy if needed)
   - Sets a clean style (`plt.style.use('seaborn-v0_8-darkgrid')` or similar)
   - Creates the chart from provided data or generates sample data if none given
   - Saves to the output path using `plt.savefig(path, dpi=150, bbox_inches='tight')`
3. Determine output format (default: `png`; respect `--format`)
4. Determine output path (default: `deliverables/visuals/<kebab-name>.<format>`; respect `--output`)
5. Run the script:
   ```bash
   python3 drafts/visuals/<name>.py
   ```
6. Confirm output file exists
7. Report: source script path, output file path, and what was rendered

### Lane 3: Custom Graphic (SVG/HTML/CSS)

**Keywords:** logo, icon, infographic, banner, badge, social card, illustration, emblem, seal, pattern, geometric, abstract

**Process:**
1. Determine output format (default: `svg`; respect `--format`)
2. Determine output path (default: `deliverables/visuals/<kebab-name>.svg`; respect `--output`)
3. Write SVG (or HTML for complex layouts) directly to the output path
   - Use clean, well-structured SVG with viewBox for scalability
   - Apply appropriate colors, gradients, and typography
   - For HTML-based graphics, include inline CSS
4. Save a copy of the source to `drafts/visuals/<kebab-name>.svg` if it differs from output
5. Report: output file path and what was created

### Lane 4: Image Manipulation (ImageMagick)

**Keywords:** resize, crop, convert, composite, watermark, thumbnail, rotate, annotate, compress, border, overlay, montage, tile

**Prerequisites:** Requires `magick` or `convert` command. If not available, inform the user:
> ImageMagick is not installed. Install with: `sudo apt-get install -y imagemagick`

**Process:**
1. Validate the source image exists (if operating on an existing image)
2. Construct the ImageMagick command pipeline
3. Determine output path (default: `deliverables/visuals/<kebab-name>.<ext>`; respect `--output`)
4. Run the command:
   ```bash
   magick <input> <operations...> <output>
   ```
   Fall back to `convert` if `magick` is not found.
5. Confirm output file exists
6. Report: command used, output file path, and result

## Output Conventions

- **Source files** (`.mmd`, `.py`, `.svg` drafts) go to `drafts/visuals/`
- **Final output** goes to `deliverables/visuals/` unless `--output` overrides
- **Filenames** use kebab-case derived from the description
- **All file writes happen in the main context** — never delegate to subagents

## Error Handling

- If a tool is not installed, tell the user how to install it
- If Mermaid syntax fails, fix the syntax and retry once
- If matplotlib script errors, fix and retry once
- If the output file is not created after the command runs, report the error clearly

## Examples

```
/draw "flowchart showing user authentication flow"
/draw "bar chart of monthly revenue" --data business/finance/revenue-tracker.md
/draw "Mega-OS agent architecture diagram" --format png
/draw "resize hero.png to 1200x630 for social card" --output deliverables/visuals/hero-social.png
/draw "geometric logo with interlocking triangles" --type graphic
```
