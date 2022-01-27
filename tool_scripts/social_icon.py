from colorio.cs import OKLAB, SRGBhex
import typer
import pathlib


def main():
    for icon in pathlib.Path("static/icons/").iterdir():
        print(f".{icon.stem}::before {{")
        print(f"  mask: url(/icons/{icon.name});")
        print("}")


if __name__ == "__main__":
    typer.run(main)