import dataclasses
import sys
import more_itertools
import numpy as np
import typer
from dataclasses import dataclass


def parse_hex(hex_string: str) -> np.ndarray:
    return np.array([int(hex_string[i:i+2], 16) for i in range(0, len(hex_string), 2)])


class Color:
    M1 = np.array([
        [0.4122214708,0.5363325363,0.0514459929],
        [0.2119034982,0.6806995451,0.1073969566],
        [0.0883024619,0.2817188376,0.6299787005],
    ])
    M2 = np.array([
        [0.2104542553, + 0.7936177850, - 0.0040720468],
        [1.9779984951, - 2.4285922050, + 0.4505937099],
        [0.0259040371, + 0.7827717662, - 0.8086757660],
    ])
    M1_inv = np.linalg.inv(M1)
    M2_inv = np.linalg.inv(M2)

    def __init__(self, data):
        self.data = data
    
    @classmethod
    def from_hex(cls, hex: str):
        rgb = parse_hex(hex.lstrip("#")) / 255.0
        linear_rgb = ((rgb + 0.055) / 1.055) ** 2.4 * (rgb >= 0.04045) + rgb / 12.92 * (rgb < 0.04045)
        lms = np.matmul(Color.M1, linear_rgb.reshape(-1, 1))
        lms = np.cbrt(lms)
        lab = np.matmul(Color.M2, lms)
        
        return cls(lab.reshape(-1))

    def hex(self) -> str:
        lms = np.matmul(Color.M2_inv, self.data.reshape(-1, 1))
        lms = lms ** 3
        linear_rgb = np.matmul(Color.M1_inv, lms)
        linear_rgb = np.clip(linear_rgb, 0.0, 1.0)
        rgb = linear_rgb * 12.92 * (linear_rgb < 0.0031308) + ((1.055 * np.power(linear_rgb, 1. / 2.4)) - 0.055) * (linear_rgb >= 0.0031308)
        rgb = np.clip(rgb, 0.0, 1.0)
        rgb = np.round(rgb * 255).astype(np.uint8)
        rgb = rgb.reshape(-1)
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
        text = Color.from_hex("#000000")
        background = Color.from_hex("#fafafa")

        vibrant = accent.data.copy()
        vibrant[1:] *= 0.25 / np.sqrt(vibrant[1] ** 2 + vibrant[2] ** 2)
        translucent = AlphaColor(Color(accent.data.copy()), alpha=0.15)

        grayed = accent.data.copy()
        grayed[1:] *= 0.01 / np.sqrt(grayed[1] ** 2 + grayed[2] ** 2)

        text_alt = Color(np.array([0.4, grayed[1], grayed[2]]))
        background_alt = Color(np.array([0.95, grayed[1], grayed[2]]))
        
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
            text_alt=text_alt,
            background_alt=background_alt,
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


def main(accent: str, output: str = ""):
    color_scheme = Colorscheme.from_accent(accent)
    out = sys.stdout 
    if output:
        out = open(output, mode="a")

    out.write(":root {")
    out.write(str(color_scheme))
    out.write("}")

    out.write("@media (prefers-color-scheme: dark) {")
    out.write("  :root {")
    out.write(str(color_scheme.invert()))
    out.write("  }")
    out.write("}\n")
    out.flush()


if __name__ == "__main__":
    typer.run(main)
