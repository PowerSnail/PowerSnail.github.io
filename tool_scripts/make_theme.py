import typer
import numpy as np
import colour
import more_itertools


class Color:
    def __init__(self, data):
        self.data = data

    @classmethod
    def from_hex(cls, hex: str):
        values = hex.lstrip("#")
        values = more_itertools.chunked(values, 2)
        values = (int("0x{}{}".format(*v), 16) for v in values)
        rgb = np.array([n / 255 for n in values])
        xyz = colour.sRGB_to_XYZ(rgb)
        lab = colour.XYZ_to_Oklab(xyz)
        return cls(np.array(lab))

    def hex(self) -> str:
        xyz = colour.Oklab_to_XYZ(self.data)
        rgb = colour.XYZ_to_sRGB(xyz)
        rgb = (min(1.0, max(0.0, v)) for v in rgb)
        rgb = (int(v * 255) for v in rgb)
        return "#{:02x}{:02x}{:02x}".format(*rgb)

    def __format__(self, __format_spec: str) -> str:
        return self.hex()


DEFAULT = {
    "accent": "#af3000",
    "bg": "#fafafa",
    "text": "#000000",
    "bg-alt": "#efeeee",
    "text-alt": "#645551",
    "bg-attention": "#C6FED2",
    "code": "#1A2D29",
    "link": "#AF3000",
    "shadow": "#AAAAAA",
}


def invert(c: str) -> str:
    inverted = Color.from_hex(c)
    inverted.data[0] = 1.2 - inverted.data[0]
    return inverted.hex()


DARK = {
    key: 
    "#000" if key == "shadow" else
    invert(value)  for key, value in DEFAULT.items()
}


def main():
    print(":root {")
    for key, value in DEFAULT.items():
        print(f"  --{key}: {value};")
    print("}")

    print("@media (prefers-color-scheme: dark) {")
    print("  :root {")
    for key, value in DARK.items():
        print(f"    --{key}: {value};")
    print("  }")
    print("}")


if __name__ == "__main__":
    typer.run(main)
