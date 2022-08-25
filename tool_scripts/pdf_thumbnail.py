import pathlib

import fitz
import typer

THUMBNAIL_SIZE = (100, 162)


def main(input_path: str):
    doc = fitz.Document(input_path)
    page = doc.load_page(0)
    scale = min(THUMBNAIL_SIZE[0] / page.bound().width, THUMBNAIL_SIZE[1] / page.bound().height)

    pixmap = page.get_pixmap(matrix=fitz.Matrix(fitz.Identity).prescale(scale, scale))
    output_path = pathlib.Path(input_path).with_suffix(".webp")
    pixmap.pil_save(str(output_path))


if __name__ == "__main__":
    typer.run(main)
