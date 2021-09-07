import pathlib
import sys

content_dir = pathlib.Path(sys.argv[1])

for file in content_dir.rglob("*.markdown"):
    file.rename(file.with_suffix(".md"))
