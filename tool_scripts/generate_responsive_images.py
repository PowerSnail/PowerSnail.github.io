from collections import Counter
import hashlib
import shutil
import toml
import pathlib
import re
import appdirs
from typing import Iterable
import multiprocessing as mp
import more_itertools

import typer
from PIL import Image
from selectolax.lexbor import LexborHTMLParser

RE_EXTERNAL = re.compile(r"[a-z]+:")
RE_UNSAFE = re.compile(r"%(20|22|3C|3E|23|25|7C)")

CACHE_DIR = pathlib.Path(appdirs.user_cache_dir("com.powersnail.www")) / "images"


with open("config.toml") as file:
    OUTPUT_SIZES = sorted(toml.load(file)["params"]["responsiveImageSizes"])


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


def image_hash(img: Image.Image) -> str:
    img = img.resize((10, 10)).convert("L")
    data = list(img.getdata())
    return hashlib.sha256(bytes(data)).hexdigest()


def generate_image(path) -> list[int]:
    img = Image.open(path)
    hash_value = image_hash(img)
    output_sizes = []
    (CACHE_DIR / hash_value).mkdir(parents=True, exist_ok=True)

    for width in OUTPUT_SIZES:
        if img.width <= width:
            break
        fname = path.stem + f"-{width}w" + path.suffix
        cached_path = CACHE_DIR / hash_value / fname
        if not cached_path.exists():
            img.resize((width, width)).save(cached_path)
        target_path = path.with_name(fname)
        shutil.copyfile(cached_path, target_path)
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
