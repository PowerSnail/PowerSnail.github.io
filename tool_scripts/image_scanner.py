import sys
import pathlib
import itertools
import re

image_extensions = ["jpg", "jpeg", "png", "svg", "ico", "webp"]
image_extensions = image_extensions + [s.upper() for s in image_extensions]

img_re = re.compile(r"[a-zA-Z0-9_\-/\.:]+\.(" + "|".join(image_extensions) + ")")

doc_globs = ["*.html", "*.md", "*.toml", "*.scss"]
image_globs = ["*." + ext for ext in image_extensions]

content_dir = pathlib.Path(sys.argv[1])
image_dir = pathlib.Path(sys.argv[2])

image_files = {
    "/" + str(img.relative_to(image_dir))
    for img in itertools.chain(*(image_dir.rglob(glob) for glob in image_globs))
}
images_in_docs = set()

for doc in itertools.chain(*(content_dir.rglob(glob) for glob in doc_globs)):
    with doc.open() as file:
        content = file.read()
    for match in img_re.finditer(content):
        if match.group(0).startswith("https://") or match.group(0).startswith("http://"):
            continue
        images_in_docs.add(match.group(0))

print("Unused Images:")
for name in image_files - images_in_docs:
    print("\t" + name)

print("Missing Images:")
for name in images_in_docs - image_files:
    print("\t" + name)
