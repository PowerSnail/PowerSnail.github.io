from selectolax.lexbor import LexborHTMLParser
import subprocess as sp
import re


def main(input_file: str):
    with open(input_file) as file:
        content = file.read()

    page = LexborHTMLParser(content)
    bib_enabled = page.css_first("#replace-bibliography")
    if not bib_enabled:
        return

    md_file = bib_enabled.attrs.get("data-input-file")

    bib_output = sp.run(
        f"pandoc --citeproc {md_file} --csl tool_scripts/acm-siggraph.csl -t html",
        shell=True,
        capture_output=True,
    ).stdout.decode("utf-8")

    bib_page = LexborHTMLParser(bib_output)

    valid_keys = set()
    for e in bib_page.css(".citation"):
        keys = not_none(e.attrs.get("data-cites", "")).split(" ")
        valid_keys.update(keys)

    filter_at_tags(page, valid_keys)
    for e1, e2 in zip(page.css(".citation"), bib_page.css(".citation")):
        e1.replace_with(e2)

    bib_enabled.replace_with(not_none(bib_page.css_first("#refs")))

    with open(input_file, "w") as file:
        file.write(not_none(page.html))


def filter_at_tags(page: LexborHTMLParser, valid_keys: set[str]):
    valid_key_re = "(" + "|".join(valid_keys) + ")"
    identifiers = []
    for e in not_none(page.root).traverse(include_text=True):
        if e.tag == "-text":
            content = e.text_content
            content = re.sub(
                rf"\[@{valid_key_re}(;\s*{valid_key_re})*\]",
                r"<span class='citation'>\g<0></span>",
                content,
            )
            content = re.sub(
                rf"@{valid_key_re}",
                r"<span class='citation'>\g<0></span>",
                content,
            )
            if content != e.text_content:
                identifiers.append((e, content))

    for e, content in identifiers:
        node = LexborHTMLParser(content)
        for c in not_none(node.body).iter(include_text=True):
            e.insert_before(c)
        e.remove()


def not_none[T](v: T | None) -> T:
    if v is None:
        raise ValueError("Value is None")
    return v


if __name__ == "__main__":
    import sys

    main(sys.argv[1])
