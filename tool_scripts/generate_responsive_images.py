from collections import Counter
import toml
import pathlib
import re
from typing import Iterable
import multiprocessing as mp
import more_itertools

import typer
from PIL import Image
from selectolax.lexbor import LexborHTMLParser

RE_EXTERNAL = re.compile(r"[a-z]+:")
RE_UNSAFE = re.compile(r"%(20|22|3C|3E|23|25|7C)")


def is_external(link: str):
    return RE_EXTERNAL.match(link) is not None


def to_path(link: str, root: pathlib.Path, current: pathlib.Path) -> pathlib.Path | None:
    if is_external(link) or link.startswith("#"):
        return None

    link = RE_UNSAFE.sub(lambda m: chr(int(m.group(1), base=16)), link)
    path = pathlib.Path(link)
    if path.is_absolute():
        return root / path.relative_to("/")
    else:
        return current.parent / path


def not_none(i: Iterable):
    return filter(lambda x: x is not None, i)


def generate_image(path) -> list[int]:
    img = Image.open(path)
    output_sizes = []
    with open("config.toml") as file:
        sizes = toml.load(file)["params"]["responsiveImageSizes"]
    for width in sizes:
        if img.width > width:
            img.resize((width, int(img.height / img.width * width))).save(
                path.with_name(path.stem + f"-{width}w" + path.suffix), method=6, quality=70)
            output_sizes.append(width)
    return output_sizes


def main(path):
    root = pathlib.Path(path)

    files = list(root.rglob("*.html"))
    paths = set()
    for html_path in files:
        with open(html_path) as file:
            page = LexborHTMLParser(file.read())
        links = not_none(tag.attrs.get("src") for tag in page.css("img"))
        paths.update(not_none(to_path(link, root, html_path) for link in links if not link.endswith(".svg")))
    
    pool = mp.Pool(8)
    counts = sorted(Counter(more_itertools.flatten(pool.imap_unordered(generate_image, paths))).items())

    print("Generated responsive images: " + ", ".join(f"{k}w: {v}" for k, v in counts))


typer.run(main)
