---
title: Setting Wallpapers for Multiple Monitors through DBus for KDE Plasma
description: 
date: 2023-02-08
slug: set-plasma-wallpaper
tags:
    - Computer Science
    - Python
    - DBus
    - Javascript
    - Plasma
    - KDE
draft: false
---

## The Problem

KDE Plasma is my favorite Linux DE, and it has its quirks and warts.
The support for multiple monitors, for example, is fairly buggy at times,
especially when monitors are turned on and off.
The way it deals with multiple monitors seems to be based on some sort of
numerical index that doesn't map itself to the monitors' UUIDs, so
when the configuration changes, desktop settings can be shifted around.

I have wallpapers of different shapes on each monitor, because my left
monitor is vertical, the right horizontal, and they get messed up when
the machine resumes from sleep or when the monitors are turned off manually.
There appears to be no way of tying a wallpaper to a physical monitor. So, I have
to frequently reset the appropriate wallpapers.

Plasma already provides a command-line tool for setting wallpaper:
`plasma-apply-wallpaperimage`, but it doesn't have the ability to address each
monitor either.

## The Solution

Fortunately, there's a Band-Aid for every wart, if you are comfortable making
your own Band-Aid. And in this case, my problem can be "fixed" by resetting
the wallpapers with a script.

Plasma can be scripted with JavaScript through its DBus interface, and there's
a fairly comprehensive documentation (The KDE Community, 2023).

The first step is getting the desktops in a deterministic order.
Desktops can be retrieved by a global function `desktops()` which "returns an 
array of all desktops that currently exist"(The KDE Community, 2023).
Each `Desktop` object has a `screen` property, a numerical ID of the 
associated monitor, but since Plasma doesn't provide any hardware information or
stable ID of the monitor, the only way to sort the monitors deterministically
seems to be using the screen's position.
We sort them from left to right, which is both deterministic, and fairly
intuitive from the human user's perspective, arguably more so than UUIDs.
Furthermore, since we are setting wallpapers in the order of the monitors, we
can also rule out `Desktop` objects with no associated screen.
These ideas are stolen from the
[superpaper project](https://github.com/hhannine/superpaper/blob/219f00aec19a4f0697e37663875eccbfa19b502b/superpaper/wallpaper_processing.py#L687)
(Hänninen, 2019).

```javascript
function getDesktops() {
    return desktops()
        .filter(d => d.screen != -1)
        .sort((a, b) => screenGeometry(a.screen).left - screenGeometry(b.screen).left);
}
```

The second piece of puzzle is setting the wallpaper to a `Desktop` object: 

```javascript
function setWallpaper(desktop, path) {
    desktop.wallpaperPlugin = "org.kde.image"
    desktop.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General")
    desktop.writeConfig("Image", path)
}
```

To assign a list of images to all the desktops one by one:

```javascript
// Imagine we have a variable called imageList, an array containing the 
// paths of the image files.
getDesktops().forEach(
    (desktop, i) => setWallpaper(desktop, imageList[i % imageList.length])
);
```

To set one wallpaper for one specific desktop:

```javascript
// Assume the variable `desktop_id` is the (0-based) index of the
// monitor, counting from left to right.
// And the variable `image_path` being the path to the image.
setWallpaper(getDesktops()[desktop_id], image_path);
```

## DBus Interface

To run this script, we use the DBus Interface of Plasma, which provides a function
called `evaluateScript`:

```sh
qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript "..."
```

...or invoke it with your favorite DBus tooling.


## Parameterize

`evaluateScript` only accepts a self-contained script.
You can hard code the path of the images, but there's no way to supply the image 
paths as arguments to it, so some sort of string manipulation is required if you
want to point Plasma to some arbitrary image.

For me, someone whose home directory is already filled with various Python
glues and _ad hoc_ scripts, nothing beats some composable _f-strings_, string
replacements, and a nice familiar command-line interface.
Any language good with string manipulation and a convenient DBus interface is
a suitable tool for this step.
Or, alternatively, you could also leave the path hard-coded, and place or link
different images to that path before calling the script.

Here's my script. I can set wallpapers to all the desktops by calling 
`python wallpaper.py all image1.jpg image2.jpg ...`, and set wallpaper for the 2nd
monitor from the left with `python wallpaper.py one 1 image1.jpg`.


```python
import dbus
import typer


SCRIPT_GET_DESKTOPS = """
function getDesktops() {
    return desktops()
        .filter(d => d.screen != -1)
        .sort((a, b) => screenGeometry(a.screen).left - screenGeometry(b.screen).left);
}
"""

SCRIPT_SET_WALLPAPER = """
function setWallpaper(desktop, path) {
    desktop.wallpaperPlugin = "org.kde.image"
    desktop.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General")
    desktop.writeConfig("Image", path)
}
"""

SCRIPT_ALL = f"""
{SCRIPT_GET_DESKTOPS}
{SCRIPT_SET_WALLPAPER}
const imageList = IMAGE_LIST;
getDesktops().forEach((desktop, i) => setWallpaper(desktop, imageList[i % imageList.length]));
"""


SCRIPT_ONE = f"""
{SCRIPT_GET_DESKTOPS}
{SCRIPT_SET_WALLPAPER}
setWallpaper(getDesktops()[DESKTOP_ID], IMAGE);
"""


def quote(s):
    return "'" + s + "'"


def plasma_dbus():
    bus = dbus.SessionBus()
    plasma = dbus.Interface(
        bus.get_object("org.kde.plasmashell", "/PlasmaShell"), dbus_interface="org.kde.PlasmaShell"
    )
    return plasma


app = typer.Typer()


@app.command()
def all(image_path: list[str], generate: bool = False):
    image_list_string = "[" + ",".join(quote(p) for p in image_path) + "]"
    script = SCRIPT_ALL.replace("IMAGE_LIST", image_list_string)
    if generate:
        print(script)
    else:
        plasma_dbus().evaluateScript(script)


@app.command()
def one(desktop_id: int, image_path: str, generate: bool = False):
    script = SCRIPT_ONE.replace("IMAGE", quote(image_path)).replace("DESKTOP_ID", str(desktop_id))
    if generate:
        print(script)
    else:
        plasma_dbus().evaluateScript(script)


if __name__ == "__main__":
    app()
```


## References

Hänninen, H. (2019). *Superpaper* [Python]. [superpaper/wallpaper_processing.py at 219f00aec19a4f0697e37663875eccbfa19b502b · hhannine/superpaper · GitHub](https://github.com/hhannine/superpaper/blob/219f00aec19a4f0697e37663875eccbfa19b502b/superpaper/wallpaper_processing.py) (Original work published 2019)

The KDE Community. (2023). *API documentation for Plasma scripting API*. Developer. [API documentation | Developer](https://develop.kde.org/docs/extend/plasma/scripting/api/)