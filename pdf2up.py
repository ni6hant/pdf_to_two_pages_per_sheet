import fitz
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox


def convert_pdf(input_file):
    """Create a new PDF with two original pages on each output page."""

    input_path = Path(input_file)

    output_path = input_path.with_name(
        f"{input_path.stem}_2_pages_per_sheet.pdf"
    )

    src = fitz.open(input_file)
    dst = fitz.open()

    for i in range(0, len(src), 2):

        page1 = src[i]
        rect1 = page1.rect

        if i + 1 < len(src):
            page2 = src[i + 1]
            rect2 = page2.rect
        else:
            page2 = None
            rect2 = rect1

        width = 2*max(rect1.width,rect2.width)
        height = max(rect1.height, rect2.height)

        out = dst.new_page(width=width, height=height)

        out.show_pdf_page(
            fitz.Rect(0, 0, width/2, rect1.height),
            src,
            i,
        )

        if page2:
            out.show_pdf_page(
                fitz.Rect(width/2, 0, width, rect2.height),
                src,
                i + 1,
            )

    dst.save(output_path, garbage=4, deflate=True)

    src.close()
    dst.close()

    return output_path


def main():
    root = tk.Tk()
    root.withdraw()

    filename = filedialog.askopenfilename(
        title="Select PDF",
        filetypes=[("PDF files", "*.pdf")],
    )

    if not filename:
        return

    try:
        output = convert_pdf(filename)

        messagebox.showinfo(
            "Done",
            f"Created:\n\n{output}",
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e),
        )


if __name__ == "__main__":
    main()