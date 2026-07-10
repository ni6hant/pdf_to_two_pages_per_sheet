# AI Assistance Notice

> **This project was developed with significant assistance LLMs**
>
> The application architecture, implementation, documentation, and code comments were generated collaboratively with AI and then reviewed, tested, and modified by the project author. The repository is intended both as a useful utility and as a learning resource demonstrating how PyMuPDF can be used to manipulate PDF layouts while preserving document quality.

---

Version 1.0: ChatGPT (Free Version)

# PDF 2 Pages Per Sheet

A small offline utility that converts a PDF into a new PDF where every output page contains two original pages placed side-by-side.

The application does **not** rasterize pages. Instead, it reuses the original PDF page objects, preserving the quality of text, images, and vector graphics.

---

# Features

- Offline operation
- Preserves searchable/selectable text
- Preserves embedded fonts
- Preserves vector graphics
- Preserves original image quality
- Handles PDFs with an odd number of pages
- Produces a new PDF without modifying the original

---

# Developer Notes

## Why PyMuPDF?

Several Python PDF libraries exist, including:

- pypdf
- PyPDF2
- ReportLab
- pdfrw
- PyMuPDF

PyMuPDF was chosen because it exposes MuPDF's native PDF rendering and manipulation engine while allowing pages to be embedded directly into another PDF.

The key function used by this project is:

```python
page.show_pdf_page(...)
```

Unlike rendering a page into an image and inserting that image into a new PDF, `show_pdf_page()` imports the original page objects directly.

This means:

- Text remains text.
- Fonts remain embedded.
- Images remain embedded.
- Vector graphics remain vector graphics.

No rasterization occurs during the layout process.

---

## How the algorithm works

Suppose the source PDF contains:

```
1
2
3
4
5
6
```

The output becomes:

```
[1][2]

[3][4]

[5][6]
```

Each output page is newly created with a width equal to the combined width of the two source pages.

```
Output Width
=
Width(Page 1)
+
Width(Page 2)
```

The output page height is simply the taller of the two pages.

Each source page is then copied into its corresponding half of the new page.

---

## Why pages are copied instead of rendered

Many PDF manipulation examples found online follow this workflow:

```
PDF Page
    ↓
Render to bitmap
    ↓
Insert bitmap into new PDF
```

While simple, this has several disadvantages:

- Larger output files
- Loss of selectable text
- Loss of vector graphics
- Reduced print quality
- Image resolution limitations

This project instead performs:

```
PDF Page
    ↓
Copy original PDF objects
    ↓
Insert into new page
```

As a result, the output remains effectively identical to the original in terms of visual quality.

---

## Save options

The output PDF is saved using:

```python
dst.save(
    output_path,
    garbage=4,
    deflate=True,
)
```

### `garbage=4`

Performs the highest level of garbage collection.

This removes unused PDF objects and rebuilds internal cross-reference tables.

Benefits include:

- Smaller file size
- Cleaner PDF structure
- Removal of orphaned objects

No document content is removed.

---

### `deflate=True`

Compresses eligible PDF streams using the standard Flate (ZIP) compression algorithm.

This does **not**:

- recompress JPEG images
- reduce image quality
- rasterize pages

Instead, it compresses data streams that support lossless compression.

---

## Complexity

For a document containing **N** pages:

- Time complexity: **O(N)**
- Memory usage: approximately constant for normal documents

Pages are processed sequentially rather than loading every page into memory.

---

## Limitations

Current version:

- Places pages side-by-side only
- Uses the original page dimensions
- Does not target specific paper sizes (A4, Letter, etc.)
- Does not rotate pages automatically

These choices were intentional to preserve the original document geometry.

---

## Building

Install dependencies:

```bash
pip install pymupdf
```

To build a standalone executable:

```bash
pip install pyinstaller
```

Then:

```bash
pyinstaller --onefile --windowed --clean --optimize 2 pdf2up.py
```

The executable will be located in:

```
dist/pdf2up.exe
```

---

## Credits

- MuPDF
- PyMuPDF
- OpenAI ChatGPT (implementation assistance and documentation)