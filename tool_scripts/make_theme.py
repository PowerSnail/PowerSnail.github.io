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


def main(primary: str, alt: str):
    primary = Color.from_hex(primary)
    primary.data[0] = 0.5
    fg = Color.from_hex("#000000")
    bg = Color.from_hex("#fafafa")

    alt = Color.from_hex(alt)
    fg_alt = Color(alt.data * 0.2 + fg.data * 0.8)
    bg_alt = Color(alt.data * 0.2 + bg.data * 0.8)

    print(":root {")
    print(f"  --color: {primary};")
    print(f"  --color-accent: {primary.hex()}15;")
    print(f"  --color-bg: {bg};")
    print(f"  --color-text: {fg};")
    print(f"  --color-bg-secondary: {bg_alt};")
    print(f"  --color-text-secondary: {fg_alt};")
    print(f"  --color-secondary-accent: {alt}15;")
    print(f"  --color-link: {primary};")
    print(f"  --color-shadow: #f4f4f4;")
    print(f"  --color-table: {primary};")
    print(f"  --color-head: {bg};")
    print("}")

    primary.data[0] = 1.2 - primary.data[0]
    bg.data[0] = 1.2 - bg.data[0]
    fg.data[0] = 1.2 - fg.data[0]
    bg_alt.data[0] = 1.2 - bg_alt.data[0]
    fg_alt.data[0] = 1.2 - fg_alt.data[0]

    print("@media (prefers-color-scheme: dark) {")
    print("  :root {")
    print(f"    --color: {primary};")
    print(f"    --color-accent: {primary}15;")
    print(f"    --color-bg: {bg};")
    print(f"    --color-text: {fg};")
    print(f"    --color-bg-secondary: {bg_alt};")
    print(f"    --color-text-secondary: {fg_alt};")
    print(f"    --color-secondary-accent: {alt}15;")
    print(f"    --color-link: {primary};")
    print(f"    --color-shadow: #f4f4f4;")
    print(f"    --color-table: {primary};")
    print("  }")
    print("}")


if __name__ == "__main__":
    typer.run(main)
