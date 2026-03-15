---
name: PowerPoint PPTX
slug: powerpoint-pptx
version: 1.0.0
homepage: https://clawic.com/skills/powerpoint-pptx
description: Create, edit, and automate PowerPoint presentations with python-pptx for slides, layouts, charts, and batch processing.
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}
---

## When to Use

User needs to create or modify PowerPoint (.pptx) files programmatically. Agent handles slide creation, content population, chart generation, and template automation.

## Quick Reference

| Topic | File |
|-------|------|
| Slide patterns | `slides.md` |
| Charts and tables | `charts.md` |
| Design guidelines | `design.md` |
| Thumbnails & conversion | `libreoffice.md` |

## Core Rules

### 1. Use LibreOffice for Thumbnails and Conversion ✅

**For generating slide thumbnails and document conversion, ALWAYS use LibreOffice:**

```bash
# Generate PNG thumbnail from PPTX
libreoffice --headless --invisible --convert-to png presentation.pptx --outdir ./thumbnails

# Generate PNG thumbnail from PDF
libreoffice --headless --invisible --convert-to png file.pdf --outdir ./thumbnails

# Convert PPTX to PDF
libreoffice --headless --invisible --convert-to pdf presentation.pptx --outdir ./output
```

**Why LibreOffice:**
- ✅ Native support for PPTX/PDF formats
- ✅ High-quality rendering (preserves fonts, layouts, colors)
- ✅ Fast headless mode (no GUI required)
- ✅ Batch processing support
- ✅ Cross-platform (Linux, macOS, Windows)

**Install:** `sudo apt-get install libreoffice`

### 2. Use python-pptx Library for Programmatic Editing

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RgbColor
```

Install: `pip install python-pptx`

**Use python-pptx when:**
- Creating presentations from scratch
- Programmatically modifying slide content
- Adding charts, tables, or images
- Automating presentation generation

**Use LibreOffice when:**
- Generating thumbnails for visual validation
- Converting between formats (PPTX ↔ PDF ↔ PNG)
- Quick preview of presentation content

### 2. Presentation Structure
```python
# Create new presentation
prs = Presentation()

# Or load existing template
prs = Presentation('template.pptx')

# Add slide with layout
slide_layout = prs.slide_layouts[1]  # Title and Content
slide = prs.slides.add_slide(slide_layout)

# Save
prs.save('output.pptx')
```

### 3. Slide Layouts (Built-in)
| Index | Layout Name | Use Case |
|-------|-------------|----------|
| 0 | Title Slide | Opening slide |
| 1 | Title and Content | Standard content |
| 2 | Section Header | Chapter dividers |
| 3 | Two Content | Side-by-side |
| 4 | Comparison | Before/after |
| 5 | Title Only | Custom content |
| 6 | Blank | Full control |

### 4. Text Handling
```python
# Access title
title = slide.shapes.title
title.text = "Slide Title"

# Access body placeholder
body = slide.placeholders[1]
tf = body.text_frame
tf.text = "First paragraph"

# Add more paragraphs
p = tf.add_paragraph()
p.text = "Second paragraph"
p.level = 1  # Indent level
```

### 5. Always Verify Output with LibreOffice Thumbnails

After creating presentation, **generate thumbnails for visual validation**:

```bash
# Create thumbnail directory
mkdir -p ./thumbnails

# Generate PNG thumbnails for all slides
libreoffice --headless --invisible --convert-to png presentation.pptx --outdir ./thumbnails

# Optional: Resize thumbnails to standard size (e.g., 400x300)
convert ./thumbnails/*.png -resize 400x300 ./thumbnails/small_
```

**Validation checklist:**
1. ✅ Check slide count matches expectation
2. ✅ Verify text populated correctly (read thumbnails)
3. ✅ Test charts render properly (visual inspection)
4. ✅ Confirm layouts and formatting preserved
5. ✅ Save to user-specified path

## Common Traps

- **Layout index assumption**: Layout indices vary by template. Always check `prs.slide_layouts` first.
- **Missing placeholders**: Not all layouts have body placeholders. Use `slide.shapes` iteration to find shapes.
- **Font not embedding**: python-pptx uses system fonts. Stick to common fonts (Arial, Calibri) for portability.
- **Image sizing**: Always specify dimensions with `Inches()` or `Pt()`. Default sizing can be unpredictable.
- **Chart data mismatch**: Category count must match data series length exactly.
- **Thumbnail generation**: Don't use python-pptx for thumbnails - use LibreOffice instead for accurate rendering.

## Scope

This skill ONLY:
- Creates and modifies local .pptx files
- Uses python-pptx library for manipulation
- Reads templates from local filesystem

This skill NEVER:
- Uploads presentations to cloud services
- Makes network requests
- Accesses files outside the working directory without user permission

## Security & Privacy

**Data that stays local:**
- All presentations created/modified on local filesystem
- No telemetry or external calls
- LibreOffice runs locally (no cloud services)

**This skill does NOT:**
- Send presentation content externally
- Access cloud storage APIs
- Store user data persistently

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `excel-xlsx` — spreadsheet automation
- `word-docx` — document generation
- `report` — structured report creation
- `documents` — document management

## Appendix: LibreOffice Command Reference

### Thumbnail Generation

```bash
# Basic thumbnail generation (all slides)
libreoffice --headless --invisible --convert-to png presentation.pptx --outdir ./thumbnails

# Generate thumbnails for specific slide range (via PDF intermediate)
libreoffice --headless --invisible --convert-to pdf presentation.pptx --outdir ./tmp
pdftoppm -jpeg -r 150 -f 1 -l 5 ./tmp/presentation.pdf ./thumbnails/slide

# Resize thumbnails after generation
convert ./thumbnails/*.png -resize 800x600 ./thumbnails/resized/
```

### Format Conversion

```bash
# PPTX to PDF
libreoffice --headless --invisible --convert-to pdf file.pptx --outdir ./output

# PPTX to PNG (all slides as separate images)
libreoffice --headless --invisible --convert-to png file.pptx --outdir ./output

# PDF to PNG (all pages)
libreoffice --headless --invisible --convert-to png file.pdf --outdir ./output

# ODP to PPTX (OpenDocument to PowerPoint)
libreoffice --headless --invisible --convert-to pptx file.odp --outdir ./output
```

### Batch Processing

```bash
# Convert all PPTX files in directory
for file in *.pptx; do
  libreoffice --headless --invisible --convert-to png "$file" --outdir ./thumbnails
done

# Generate thumbnails with custom output directory
mkdir -p ./output/thumbnails
libreoffice --headless --invisible --convert-to png ./presentations/*.pptx --outdir ./output/thumbnails
```

### Supported Formats

**Input formats:** pptx, ppt, odp, pdf, docx, doc, xlsx, xls
**Output formats:** png, pdf, jpg, svg, emf, wmf, bmp, gif

### Performance Tips

- Use `--headless --invisible` for server/automation environments
- Specify `--outdir` to control output location
- For large presentations, consider converting to PDF first, then to images
- LibreOffice may take 2-5 seconds per slide for PNG conversion
