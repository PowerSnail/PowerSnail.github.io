import pathlib
import re
from typing import Iterable

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


def main(path):
    root = pathlib.Path(path)

    files = list(root.rglob("*.html"))
    paths = set()
    for html_path in files:
        with open(html_path) as file:
            page = LexborHTMLParser(file.read())
        links = not_none(tag.attrs.get("src") for tag in page.css("img"))
        paths.update(not_none(to_path(link, root, html_path) for link in links))
    
    counts = {480: 0, 800: 0, 1200: 0}
    for p in sorted(paths):
        try:
            img = Image.open(p)
        except:
            continue
        
        for width in counts:
            if img.width > width:
                img.resize((width, int(img.height / img.width * width))).save(p.with_name(p.stem + f"-{width}w" + p.suffix), method=6, quality=95)
                counts[width] += 1
    print(f"Generated {counts[480]} 480w images, {counts[800]} 800w images.")


typer.run(main)
