import itertools
import pathlib
import re

import typer
from rich.console import Console
from rich.tree import Tree
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


def main(path):
    root = pathlib.Path(path)
    broken_links = []
    console = Console()

    files = list(root.rglob("*.html"))
    for html_path in files:
        with open(html_path) as file:
            page = LexborHTMLParser(file.read())
        links = itertools.chain(
            (tag.attrs.get("href") for tag in page.css("a")), (tag.attrs.get("src") for tag in page.css("img"))
        )
        links = [link for link in links if link is not None]
        links = [link for link in links if (path := to_path(link, root, html_path)) and not path.exists()]
        if links:
            broken_links.append((str(html_path), list(links)))

    if broken_links:
        total_count = sum(len(links) for (_, links) in broken_links)
        console.print(f"Found [red]{total_count}[/red] Broken Links")
        for path, links in broken_links:
            tree = Tree(f"{path}")
            for link in links:
                tree.add(f"[red]{link}")
            console.print("")
            console.print(tree)
    else:
        console.print("No missing link")


typer.run(main)
