---
title: Firefox 137 Nvidia Hardware Decoding
description: How to enable hardware decoding for Firefox 137 on Linux when using Nvidia GPU
date: 2025-04-29
slug: firefox-137-nvidia-hardware-decoding
tags:
    - nvidia
    - opensuse
    - firefox
draft: false
---

Recently, I've noticed that I don't have hard decoding enabled in Firefox (my machine uses openSUSE Tumbleweed, and proprietary driver 570 for GTX 2080 video card). On `about:support` page, the media section shows the following:

```
Codec   Software    Hardware
H264	Supported	Unsupported
VP9	    Supported	Unsupported
VP8	    Supported	Unsupported
AV1	    Supported	Unsupported
HEVC	Supported	Unsupported
AAC	    Supported	Unsupported
MP3	    Supported	Unsupported
Opus	Supported	Unsupported
Vorbis	Supported	Unsupported
FLAC	Supported	Unsupported
Wave	Supported	Unsupported
```

That's a bit disappointing; GTX 2080 certainly have the capability of doing some hardware decoding, and I use it for my Jellyfin installation hosted on the same machine. See [this post](https://powersnail.com/2023/jellyfin-nvidia-docker/) on how I set it up.

To be fair, videos play fine in Firefox---with software decoding I presume, and I don't often watch YouTube on my PC, so I'm not entirely sure when this has been turned off. Some forum posts say that it is new as of Firefox 137, and some suggest that hardware decoding has been broken since 136. See <https://forum.manjaro.org/t/firefox-137-0-no-longer-plays-any-videos-for-me-after-switching-from-136/176606/1>.

After fiddling around a bit with all the various solutions floating around these posts, I found that what I was missing was the `libva-nvidia-driver` package. This package is not in the default openSUSE repository, nor is it in the proprietary driver repository; instead it is still in an experimental repository: <https://build.opensuse.org/package/show/X11%3AXOrg/libva-nvidia-driver>.

To install it (if you are okay with using an experimental package), run

```sh
opi libva-nvidia-driver
```

...and choose the `X11:XOrg` repository as the source. Obligatory reminder: an experimental package comes with the titular caveat of being experimental, and it is your judgement call whether to trust its reliability and compatibility with other packages in the main repo. Also, keep an eye on whether it gets eventually merged into the main repo.

After getting the package installed, I now see in the Media section:

```
Codec   Software    Hardware
H264	Supported	Supported
VP9	    Supported	Supported
VP8	    Supported	Supported
AV1	    Supported	Unsupported
HEVC	Supported	Supported
AAC	    Supported	Unsupported
MP3	    Supported	Unsupported
Opus	Supported	Unsupported
Vorbis	Supported	Unsupported
FLAC	Supported	Unsupported
Wave	Supported	Unsupported
```

Hooray! Good enough for me, having H264, VP8/9, and HEVC enabled are all I could ask for.

---

There are loads of solutions proposed on forums and Reddit. I did some further experiments on what are the pre-requisite to actually put `libva-nvidia-driver` into use.

1. `ffmpeg` needs to be installed;
2. NVIDIA DRM needs to be enabled (which I enable with a kernel parameter `nvidia_drm.modeset=1`);
3. You need to toggle `media.hardware-video-decoding.force-enabled` to `true` in `about:config`. With this being false, hardware decoding support all revert back to Unsupported.
4. It's not necessary to touch `media.ffmpeg.vaapi.enabled`, `media.av1.enabled`, `gfx.x11-egl.force-enabled`, or `widget.dmabuf.force-enabled`.
5. All the workarounds involving setting environment variables don't seem to be necessary or effective.
