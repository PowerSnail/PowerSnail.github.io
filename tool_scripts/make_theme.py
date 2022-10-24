import dataclasses
import colour
import more_itertools
import numpy as np
import typer
from dataclasses import dataclass


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

    def invert(self) -> "Color":
        inverted = self.data.copy()
        inverted.data[0] = min(1.2 - inverted.data[0], 1.0)
        return Color(inverted)


class AlphaColor:
    def __init__(self, color: Color, alpha: float):
        self.alpha = alpha
        self.color = color

    def hex(self) -> str:
        return f"{self.color.hex()}{int(self.alpha * 255):02x}"

    def invert(self) -> "AlphaColor":
        return AlphaColor(self.color.invert(), self.alpha)


@dataclass
class Colorscheme:
    accent: Color
    translucent: AlphaColor
    text: Color
    background: Color
    text_alt: Color
    background_alt: Color

    gray: Color
    red: Color
    yellow: Color
    green: Color
    cyan: Color
    blue: Color
    violet: Color

    @classmethod
    def from_accent(cls, accent_hex: str):
        accent = Color.from_hex(accent_hex)
        accent.data[0] = 0.4
        text = Color.from_hex("#000000")
        background = Color.from_hex("#fafafa")

        vibrant = accent.data.copy()
        vibrant[1:] *= 0.22 / np.sqrt(vibrant[1] ** 2 + vibrant[2] ** 2)
        translucent = AlphaColor(Color(vibrant), alpha=0.1)


        light = 0.4
        chroma = 0.25
        terminals = [
            Color(np.array([light, np.cos(angle) * chroma, np.sin(angle) * chroma]))
            for angle in np.linspace(0, 2 * np.pi, 6, endpoint=False)
        ]

        return cls(
            accent=accent,
            translucent=translucent,
            text=text,
            background=background,
            text_alt=Color(text.data * 0.9 + accent.data * 0.1),
            background_alt=Color(background.data * 0.9 + accent.data * 0.1),
            gray=Color(np.array([light, 0.0, 0.0])),
            red=terminals[0],
            yellow=terminals[1],
            green=terminals[2],
            cyan=terminals[3],
            blue=terminals[4],
            violet=terminals[5],
        )

    def __str__(self):
        return "\n".join(f"--{key}: {value.hex()};" for key, value in dataclasses.asdict(self).items())

    def invert(self) -> "Colorscheme":
        return Colorscheme(**{k: v.invert() for k, v in dataclasses.asdict(self).items()})


def main(accent: str):
    color_scheme = Colorscheme.from_accent(accent)
    print(":root {")
    print(str(color_scheme))
    print("}")

    print("@media (prefers-color-scheme: dark) {")
    print("  :root {")
    print(str(color_scheme.invert()))
    print("  }")
    print("}")


if __name__ == "__main__":
    typer.run(main)
