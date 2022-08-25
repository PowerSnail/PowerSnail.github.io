import pathlib
import re
import sys

content_dir = pathlib.Path(sys.argv[1])
date_re = "\d{4}-\d{2}-\d{2}"


def meta_mark_index(f):
    for i, line in enumerate(f):
        if line.strip() == "---":
            yield i


for path in content_dir.rglob("*.md"):
    if m := re.match(date_re, path.name):
        date = m.group(0)

        with open(path) as f:
            lines = f.readlines()

        meta_lines = list(meta_mark_index(lines))
        if len(meta_lines) < 2:
            print(f"{path}: no meta block found")
            continue

        if any((line.startswith("date:") for line in lines[meta_lines[0] + 1 : meta_lines[1]])):
            print(f"{path}: already contains date in meta block")
            continue

        with open(path, "w") as f:
            for l in lines[: meta_lines[1]]:
                f.write(l)
            f.write(f'date: "{date}"\n')
            for l in lines[meta_lines[1] :]:
                f.write(l)
        print(f"{path}: Added date {date}")

    else:
        print(f"{path}: date not in filename")
