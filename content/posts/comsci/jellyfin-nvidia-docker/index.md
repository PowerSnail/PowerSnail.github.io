---
title: Hardware Accelerated Jellyfin, Docker Composed, in openSUSE
description: Get Hardware-accelerated encoding and decoding working with NVIDIA in Jellyfin running inside a Docker container in openSUSE
date: 2023-03-12
slug: jellyfin-nvidia-docker
tags:
    - Docker
    - Jellyfin
    - openSUSE
    - system administration
    - technology
    - NVIDIA
    - FFmpeg
references:
    - id: dockerincComposeFileDeploy2023
      abstract: Compose file deploy reference
      accessed:
          - year: 2023
            month: 3
            day: 10
      author:
          - literal: Docker Inc
      citation-key: dockerincComposeFileDeploy2023
      container-title: Docker Documentation
      issued:
          - year: 2023
            month: 3
            day: 10
      language: en
      title: Compose file deploy reference
      type: webpage
      URL: https://docs.docker.com/compose/compose-file/deploy/

    - id: jellyfincommunityDownloadsJellyfin
      accessed:
          - year: 2023
            month: 3
            day: 10
      author:
          - literal: Jellyfin Community
      citation-key: jellyfincommunityDownloadsJellyfin
      language: en
      title: Downloads | Jellyfin
      type: webpage
      URL: https://jellyfin.org/downloads/docker/

    - id: nvidiacorporationVideoEncodeDecode2020
      abstract: >-
          Find the related video encoding and decoding support for all NVIDIA GPU
          products.
      accessed:
          - year: 2023
            month: 3
            day: 10
      author:
          - literal: NVIDIA Corporation
      citation-key: nvidiacorporationVideoEncodeDecode2020
      container-title: NVIDIA Developer
      issued:
          - year: 2020
            month: 9
            day: 8
      language: en-US
      title: Video Encode and Decode GPU Support Matrix
      type: webpage
      URL: https://developer.nvidia.com/video-encode-and-decode-gpu-support-matrix-new

    - id: opensusecontributors&othersSDBNVIDIADrivers2020
      accessed:
          - year: 2023
            month: 3
            day: 10
      author:
          - literal: openSUSE contributors & others
      citation-key: opensusecontributors&othersSDBNVIDIADrivers2020
      issued:
          - literal: 22 July 2020‎
      title: SDB:NVIDIA drivers - openSUSE Wiki
      type: webpage
      URL: https://en.opensuse.org/SDB:NVIDIA_drivers

    - id: nvidiacorporationInstallationGuideNVIDIA2023
      accessed:
          - year: 2023
            month: 3
            day: 10
      author:
          - literal: NVIDIA Corporation
      citation-key: nvidiacorporationInstallationGuideNVIDIA2023
      issued:
          - year: 2023
            month: 3
            day: 8
      title: Installation Guide — NVIDIA Cloud Native Technologies  documentation
      type: webpage
      URL: >-
          https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html

    - id: nvidiacorporationUserGuideNVIDIA2023
      author:
          - literal: NVIDIA Corporation
      citation-key: nvidiacorporationUserGuideNVIDIA2023
      issued:
          - year: 2023
            month: 3
            day: 8
      title: User Guide — NVIDIA Cloud Native Technologies documentation
      type: webpage
      URL: >-
          https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/user-guide.html
draft: false
link-citations: true
nocite: |
    @*
---

## What is it all about?

Here is what I'm trying to do: I want to watch TV at home. On my hard drive, is a collection of videos, and I'd like to stream them from my PC to mobile devices. The PC runs openSUSE, has an NVIDIA card, and Jellyfin---a sort of self-hosted Netflix---is my choice for managing the multimedia files and the streaming.

## Why am I Running Jellyfin in Docker

You can run Jellyfin just by itself, un-containerized, and tell it to use the dependencies that are installed by your OS's package manager. It would be more space-efficient. You would need one less moving parts (Docker).

I run Jellyfin in a Docker container, mainly for the bundled FFmpeg. Jellyfin uses FFmpeg as the underlying tool that does all the heavy-lifting with regard to processing the videos. The problem is that FFmpeg is one of those programs which come with a huge number of compiling options, some of which are turned off by default, some can't be enabled in certain distributions due to licensing issues. These can't be tweaked at runtime. I can compile FFmpeg myself, but first, that defeats the purpose of saving space, and it would be a pain to keep it up to date and resolve compatibility issues between it, the OS, and Jellyfin. Using the official docker image will likely be less of a headache.

Another reason, applicable to software that deals with the file system, is that there's less of a chance that a bug could affect unrelated files, since Docker only gives it access to specified directories. If Jellyfin messes up, at most my media folder gets obliterated, which I have a backup for, and which is easily rectified when the rest of the file system is left untouched.

At last, it's easy to put constraints on how many cores Jellyfin can use. My machine has 16 cores, and really, to enable the transcoding of videos for one or two users, no more than 2 or 3 cores are necessary. However, for some reason, when I ran it bare metal, I was never able to enact that restriction, whether through Jellyfin's settings, or some other system tools. Docker, on the other hand, can expose a selected set of cores, which as far as all the transcoding processes know, are all the cores existing.

## Installing Dependencies

To install Docker and Docker Compose,

```bash
sudo zypper in docker docker-compose
sudo systemctl enable --now docker
```

To install graphics card drivers (this configuration works only with Nvidia's proprietary drivers), openSUSE has an [official guide](https://en.opensuse.org/SDB:NVIDIA_drivers), and I use what they call "the easy way", which means adding a repository that is co-managed by NVIDIA and openSUSE, and installing the driver via `zypper`.

```bash
sudo zypper addrepo --refresh "https://download.nvidia.com/opensuse/tumbleweed" NVIDIA
sudo zypper in nvidia-video-G06 nvidia-gl-G06
```

**Do read the guide carefully**, though, as the instructions differ for different card models. `06` is what works for my card, something else might for yours.

With the proper drivers installed, we also need _NVIDIA's Container Toolkit_ to make it work with Docker. The slight problem is that NVIDIA doesn't package this toolkit for Tumbleweed, only Leap, so I'm taking some risks here to use a library for a not-exactly-compatible distribution. Well, if it works, it works.

Using the [guide for Leap 15](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#installing-on-suse-15):

```bash
sudo zypper ar "https://nvidia.github.io/libnvidia-container/opensuse-leap15.1/libnvidia-container.repo"
sudo zypper ref
sudo zypper in nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
```

And I restart the PC at this point, just to make sure that all the enabled services are running.

## Composing Docker for Jellyfin

Here's what the official Jellyfin guide says:

```bash
docker pull jellyfin/jellyfin:latest
mkdir -p /srv/jellyfin/{config,cache}
docker run -d -v /srv/jellyfin/config:/config \
    -v /srv/jellyfin/cache:/cache \
    -v /media:/media \
    --net=host \
    jellyfin/jellyfin:latest
```

From the host OS's perspective, the configuration files are stored in `/srv/jellyfin/config`, the caches in `/srv/jellyfin/cache`, the media files in a hypothetical `/media` directory. Just use wherever your media is (`-v /path/to/media:/media`). Inside Jellyfin's configuration, all the media files are relative to `/media`.

We have more parameters to pass in and to better manage these options, a compose file is simpler and cleaner in my opinion than a shell script:

```yaml
# docker-compose.yaml

version: "3.3"
services:
    jellyfin:
        volumes:
            - "/srv/jellyfin/config:/config"
            - "/srv/jellyfin/cache:/cache"
            - "/path/to/media:/media"
        network_mode: host
        image: "jellyfin/jellyfin:latest"
        cpuset: "13-15"
        environment:
            - NVIDIA_DRIVER_CAPABILITIES=all
            - NVIDIA_VISIBLE_DEVICES=all
        deploy:
            resources:
                reservations:
                    devices:
                        - driver: nvidia
                          count: 1
                          capabilities: [gpu]
```

To put a restriction on the cores used by Jellyfin, the option `cpuset` is used, and I set it to `13-15` which exposes the last three cores, sufficient for my personally use.

To enable hardware acceleration, we give the container permission to use the cards with environment variables (these are for the NVIDIA Container Toolkit). `NVIDIA_DRIVER_CAPABILITIES=all` grants permission to all capabilities. `NVIDIA_VISIBLE_DEVICES=all` grants permission to all cards. You can fine-tune which card and what capabilities Jellyfin has access to, by following NVIDIA's [guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/user-guide.html).

The rest of the options is the Docker Compose's way of giving access of the GPU to the container [@dockerincComposeFileDeploy2023].

## Configuring NVENC and NVDEC in Jellyfin

The model of my graphics card is RTX 2080, which can be checked by running:

```bash
nvidia-smi -L  # GPU 0: NVIDIA GeForce RTX 2080
```

The encoding and decoding capabilities of the card can be checked on NVIDIA's website: <https://developer.nvidia.com/video-encode-and-decode-gpu-support-matrix-new>. For my 2080, I've gotten a good list of decode-able codecs (MPEG-1, MPEG-2, VC-1, VP8, VP9, H.264, H.265), and H.264 and H.265 for encoding, which are more than enough. The only thing missing is AV1 support, which is at the moment not that widely used, but whose popularity is on the rise.

In Jellyfin, in the section `Dashboad>Playback>Transcoding`, set "Hardware acceleration" to "Nvidia NVENC", check the boxes for the supported codecs listed above, and tick the options "Enable enhanced NVDEC decoder", and "Enable hardware encoding".

It's important to know which codec to enable, because Jellyfin blindly trusts the configuration, and won't test whether the GPU is actually capable of doing a specific transcoding. If an option were to be mis-selected, there wouldn't be a fallback, and the video would fail to load.

## How well does it work?

Here's the CPU usage---specifically the usage of core 13, 14, and 15---when playing a H.265 video, **without** hardware acceleration:

![An image showing that the usages of the three cores are above 80% during transcoding](./cpu-usage-no-gpu.webp "CPU usage without hardware acceleration")

After enabling hardware acceleration, when playing the same video, the core usages drop to below 40%, and you can see from the `nvtop` (a tool which displays GPU usage), that a FFmpeg process is utilizing the GPU. Now, obviously this data is just a snapshot and is noisy, given all the other processes running on the machine. Although I don't have a clean, isolated, long-lasting series of data showing the history of CPU usage, it is my observation that the drop is both significant and consistent through time. For one, it no longer causes FPS to fluctuate, when a video starts to play while I'm in the middle of a game.

![An image showing that the three cores are utilized below 40%](./cpu-usage-with-gpu.webp "CPU usage with hardware acceleration")

![An image showing GPU usage during transcoding, highlighted is a process of FFmpeg utilizing](./gpu-usage.webp "GPU usage during transcoding")

And of course, hardware acceleration isn't just making the GPU busier and the CPU idler; another benefit is that, titularly, the video is transcoded faster. This isn't noticeable in the middle of playing a video, because Jellyfin would, like any competent streaming software, transcode the next chunk when you are still watching the previous one.

It shines when **starting** a video, and more importantly, when I'm **jumping around** the progress bar. What used to be a few seconds of spinning circles, is now only a slight punctuation. The improvement on snappiness simply by moving the work from CPU to GPU is, frankly speaking, astonishing.
