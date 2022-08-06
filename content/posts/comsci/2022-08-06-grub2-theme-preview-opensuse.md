---
title: Fixing Grub2 Theme Preview on Opensuse Tumbleweed
description: To use Grub2 theme preview on openSUSE, two environment variables needs to be overridden.
date: 2022-08-06
slug: grub2-theme-preview-opensuse
tags:
    - computer science
draft: true
---

**TLDR**: To use [grub2-theme-preview](https://github.com/hartwork/grub2-theme-preview) on openSUSE, you need to override the paths of firmware and ovmf:

```sh
G2TP_GRUB_LIB=/usr/share/grub2
G2TP_OVMF_IMAGE=/usr/share/qemu/ovmf-x86_64-code.bin
```

---

Running after installing grub2-theme-preview and it's dependencies on openSUSE Tumbleweed, I was given the following error:

```sh
> grub2-theme-preview .
ERROR: [Errno 2] GRUB platform directory "/usr/lib/grub/x86_64-efi" not found
```

This is because grub2-theme-preview hard codes a few paths for this file, which unfortunately do not include openSUSE's layout.

The path can be overridden with undocumented an environment variables, which isn't mentioned in the help message or REAME.md, but it can be seen in code:

```python
# __main__.py
def _grub2_directory(platform):
    return '{}/{}'.format(os.environ.get('G2TP_GRUB_LIB', '/usr/lib/grub'), platform)
```

Where is it in openSUSE? The error message says that "/usr/lib/grub/x86_64-efi" was not found, so let's find x86-64-efi:

```sh
>  fd x86_64-efi /usr
/usr/share/grub2/x86_64-efi/
```

The code tells us that `G2TP_GRUB_LIB` should refer to the directory that contains `x86_64-efi`, so we can override the environment variable:

```sh
export G2TP_GRUB_LIB=/usr/share/grub2
```

Now, let's run it again:

```sh
> grub2-theme-preview .
ERROR: [Errno 2] OVMF image file "/usr/share/[..]/OVMF_CODE.fd" is missing, please install package 'edk2-ovmf' or 'ovmf'.
```

Okay, so there's another one. Again, digging into the code, we can find another environment variable:

```python
def _grub2_ovmf_tuple():
    ...
    omvf_image = os.environ.get('G2TP_OVMF_IMAGE')
    if omvf_image is not None:  # Support non-standard locations e.g. NixOS
        candidates = [omvf_image]
    else:
        candidates = [
            '/usr/share/edk2-ovmf/OVMF_CODE.fd',  # Gentoo and its derivatives
            '/usr/share/edk2-ovmf/x64/OVMF_CODE.fd',  # Arch Linux and its derivatives
            '/usr/share/OVMF/OVMF_CODE.fd',  # Debian and its derivatives
            '/usr/share/edk2/ovmf/OVMF_CODE.fd',  # Fedora (and its derivatives?)
        ]
    ...
```

`OVMF_CODE.fd`, however, is more elusive. `fd OVMF_CODE` returns nothing. After some Googling and forum digging, it turns out that openSUSE does not name the UEFI firmware as `OVMF_CODE.fd`; rather, `ovmf-[arch]-code.bin`. For my purpose, the x86_64 version is located at `/usr/share/qemu/ovmf-x86_64-code.bin`. This time, `grub2-theme-preview` is looking for the path of the file, rather than the directory, so, we set the environment variable:

```sh
export G2TP_OVMF_IMAGE=/usr/share/qemu/ovmf-x86_64-code.bin
```

Running `grub2-theme-preview` once again:

```sh
> grub2-theme-preview .
INFO: Appending to fonts to load: ascii.pf2
INFO: Appending to fonts to load: DejaVuSans-Bold14.pf2
INFO: Appending to fonts to load: DejaVuSans10.pf2
INFO: Appending to fonts to load: DejaVuSans12.pf2
INFO: Found OVMF image at '/usr/share/qemu/ovmf-x86_64-code.bin'.
INFO: Please give GRUB a moment to show up in QEMU...
```

_Viola!_

![Screenshot of grub2-theme-preview](/images/opensuse-grub-preview.webp)