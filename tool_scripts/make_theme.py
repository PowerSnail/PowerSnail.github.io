from colorio.cs import OKLAB, SRGBhex
import numpy as np
import typer
import sys


class Color:
    _oklab = OKLAB()
    _hex = SRGBhex(default_mode="clip")

    def __init__(self, data):
        self.data = data

    @classmethod
    def from_hex(cls, hex):
        return cls(cls._oklab.from_xyz100(cls._hex.to_xyz100(hex)))

    def __str__(self):
        return str(self._hex.from_xyz100(self._oklab.to_xyz100(self.data)))


def main(main_color):
    main_color = Color.from_hex(main_color)
    main_color.data[0] = 0.5
    fg = Color.from_hex("#000000")
    bg = Color.from_hex("#f9f9f9")

    alt = Color(main_color.data + np.array([0, 0.2, 0.2]))
    fg_alt = Color(main_color.data * 0.5 + fg.data * 0.5)
    bg_alt = Color(main_color.data * 0.1 + bg.data * 0.9)

    print(":root {")
    print(f"  --color: {main_color};")
    print(f"  --color-accent: {main_color}15;")
    print(f"  --color-bg: {bg};")
    print(f"  --color-text: {fg};")
    print(f"  --color-bg-secondary: {bg_alt};")
    print(f"  --color-text-secondary: {fg_alt};")
    print(f"  --color-secondary-accent: {alt}15;")
    print(f"  --color-link: {main_color};")
    print(f"  --color-shadow: #f4f4f4;")
    print(f"  --color-table: {main_color};")
    print(f"  --color-head: {bg};")
    print("}")

    main_color.data[0] = 1.2 - main_color.data[0]
    bg.data[0] = 1.2 - bg.data[0]
    fg.data[0] = 1.2 - fg.data[0]
    bg_alt.data[0] = 1.2 - bg_alt.data[0]
    fg_alt.data[0] = 1.2 - fg_alt.data[0]

    print("@media (prefers-color-scheme: dark) {")
    print("  :root {")
    print(f"    --color: {main_color};")
    print(f"    --color-accent: {main_color}15;")
    print(f"    --color-bg: {bg};")
    print(f"    --color-text: {fg};")
    print(f"    --color-bg-secondary: {bg_alt};")
    print(f"    --color-text-secondary: {fg_alt};")
    print(f"    --color-secondary-accent: {alt}15;")
    print(f"    --color-link: {main_color};")
    print(f"    --color-shadow: #f4f4f4;")
    print(f"    --color-table: {main_color};")
    print("  }")
    print("}")


if __name__ == "__main__":
    typer.run(main)