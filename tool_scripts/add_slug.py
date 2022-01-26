import pathlib
import re
import sys

content_dir = pathlib.Path(sys.argv[1])
slug_re = "\d{4}-\d{2}-\d{2}-(.*)\.md" 

def meta_mark_index(f):
    for i, line in enumerate(f):
        if line.strip() == "---":
            yield i


for path in content_dir.rglob("*.md"):
    if m := re.match(slug_re, path.name):
        slug = m.group(1)

        with open(path) as f:
            lines = f.readlines()

        meta_lines = list(meta_mark_index(lines))
        if len(meta_lines) < 2:
            print(f"{path}: no meta block found")
            continue

        if any((line.startswith("slug:") for line in lines[meta_lines[0] + 1: meta_lines[1]])):
            print(f"{path}: already contains date in meta block")
            continue

        with open(path, "w") as f:
            for l in lines[:meta_lines[1]]:
                f.write(l)
            f.write(f"slug: \"{slug}\"\n")
            for l in lines[meta_lines[1]:]:
                f.write(l)
        print(f"{path}: Added slug {slug}")
        
    else:
        print(f"{path}: slug not in filename")



        
