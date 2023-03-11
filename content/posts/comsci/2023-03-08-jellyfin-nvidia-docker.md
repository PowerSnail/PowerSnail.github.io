---
title: Hardware Accelerated Jellyfin, Docker Composed, in openSUSE
description: Get Hardware-accelerated encoding and decoding working with NVIDIA in Jellyfin running inside a Docker container in openSUSE
date: 2023-03-08
slug: jellyfin-nvidia-docker
tags:
    - Docker
    - Jellyfin
    - openSUSE
    - system administration
    - technology
    - NVIDIA
    - FFmpeg
draft: true
---

## Why am I Running Jellyfin in Docker

I run Jellyfin in a Docker container, mainly for the bundled FFmpeg (it is the underlying library that does all the heavy-lifting with regard to processing the videos). FFmpeg is one of those programs with a huge number of compiling options, some of which are proprietary, and hence doesn't get included in some distros. It would be a pain to manually compile FFmpeg myself while keeping it both up to date and compatible with the version of Jellyfin I use.

Another reason, applicable to software that deals with the file system, is that there's less of a chance that a bug could affect unrelated files, since Docker only gives it access to specified directories. If Jellyfin messes up, at most my media folder gets obliterated, which I have a backup for, and which is easily rectified when the rest of the file system is left untouched.

A third reason is that it's easy to put constraints on how many cores Jellyfin can use. My machine has 16 cores, and really, to enable the transcoding of videos for one or two users, no more than 2 or 3 cores are necessary. However, for some reason, when I ran it bare metal, I was never able to enact that restriction, whether through Jellyfin's settings, or some other system tools. Docker, on the other hand, can expose a selected set of cores, which as far as all the transcoding processes know, are all the cores existing.

## Installing Dependencies

To install Docker and Docker Compose,

```bash
sudo zypper in docker docker-compose
sudo systemctl enable --now docker
```

This configuration works only with Nvidia's proprietary drivers. openSUSE has an [official guide](https://en.opensuse.org/SDB:NVIDIA_drivers), and I used the easy way.

```bash
sudo zypper addrepo --refresh https://download.nvidia.com/opensuse/tumbleweed NVIDIA
sudo zypper in nvidia-video-G06 nvidia-gl-G06
```

Do read the guide carefully, though, as the packages differ for different card models. `06` is what works for my card.

With the proper drivers installed, we also need NVIDIA's Container Toolkit to make it work with Docker. The slight problem is that NVIDIA doesn't package this toolkit for Tumbleweed, only Leap. I'm taking some sort risk here I guess to use a library for a not-exactly-compatible distribution. If it works, it works.

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

We have more parameters to pass in and to better manage these options, a compose file is simpler and cleaner in my opinion than a shell script.

To put a restriction on the cores used by Jellyfin, the option `cpuset` is used, and I set it to `13-15` which exposes the last three cores, sufficient for my personally use. 

To enable hardware acceleration, we give the container permission to use the cards with environment variables. `NVIDIA_DRIVER_CAPABILITIES=all` grants permission to all capabilities. `NVIDIA_VISIBLE_DEVICES=all` grants permission to all cards. You can fine-tune which card and what capabilities Jellyfin has access to, by following NVIDIA's [guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/user-guide.html). 

The rest of the options is the Docker Compose's way of giving access of the GPU to the container: <https://docs.docker.com/compose/compose-file/deploy/>.


```yaml
# docker-compose.yaml

version: '3.3'
services:
  jellyfin:
    volumes:
      - '/srv/jellyfin/config:/config'
      - '/srv/jellyfin/cache:/cache'
      - '/path/to/media:/media'
    network_mode: host
    image: 'jellyfin/jellyfin:latest'
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



## Configuring  NVENC and NVDEC

The model of my graphics card is RTX 2080, which can be checked by running:

```bash
nvidia-smi -L  # GPU 0: NVIDIA GeForce RTX 2080
```

The encoding and decoding capabilities of the card can be checked on NVIDIA's website: <https://developer.nvidia.com/video-encode-and-decode-gpu-support-matrix-new>. For my 2080, I've gotten a good list of decodeable codecs (MPEG-1, MPEG-2, VC-1, VP8, VP9, H.264, H.265), and H.264 and H.265 for encoding, which are more than enough. The only thing missing is AV1 support, which is at the moment not that widely used, but whose popularity is on the rise.

In Jellyfin, in the section `Dashboad/Playback/Transcoding`, set "Hardware acceleration" to "Nvidia NVENC", check the boxes for the supported codecs listed above, and tick the options "Enable enhanced NVDEC decoder", and "Enable hardware encoding". 


## References

<div class="csl-entry">Docker Inc. (2023, March 10). <i>Compose file deploy reference</i>. Docker Documentation. <a href="https://docs.docker.com/compose/compose-file/deploy/">https://docs.docker.com/compose/compose-file/deploy/</a></div>
  <span class="Z3988" title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Adc&amp;rft.type=webpage&amp;rft.title=Compose%20file%20deploy%20reference&amp;rft.description=Compose%20file%20deploy%20reference&amp;rft.identifier=https%3A%2F%2Fdocs.docker.com%2Fcompose%2Fcompose-file%2Fdeploy%2F&amp;rft.au=undefined&amp;rft.date=2023-03-10&amp;rft.language=en"></span>
  <div class="csl-entry">Jellyfin Community. (n.d.). <i>Downloads | Jellyfin</i>. Retrieved March 10, 2023, from <a href="https://jellyfin.org/downloads/docker/">https://jellyfin.org/downloads/docker/</a></div>
  <span class="Z3988" title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Adc&amp;rft.type=webpage&amp;rft.title=Downloads%20%7C%20Jellyfin&amp;rft.identifier=https%3A%2F%2Fjellyfin.org%2Fdownloads%2Fdocker%2F&amp;rft.au=undefined&amp;rft.language=en"></span>
  <div class="csl-entry">NVIDIA Corporation. (2020, September 8). <i>Video Encode and Decode GPU Support Matrix</i>. NVIDIA Developer. <a href="https://developer.nvidia.com/video-encode-and-decode-gpu-support-matrix-new">https://developer.nvidia.com/video-encode-and-decode-gpu-support-matrix-new</a></div>
  <span class="Z3988" title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Adc&amp;rft.type=webpage&amp;rft.title=Video%20Encode%20and%20Decode%20GPU%20Support%20Matrix&amp;rft.description=Find%20the%20related%20video%20encoding%20and%20decoding%20support%20for%20all%20NVIDIA%20GPU%20products.&amp;rft.identifier=https%3A%2F%2Fdeveloper.nvidia.com%2Fvideo-encode-and-decode-gpu-support-matrix-new&amp;rft.au=undefined&amp;rft.date=2020-09-08&amp;rft.language=en-US"></span>
  <div class="csl-entry">NVIDIA Corporation. (2023a, March 8). <i>Installation Guide—NVIDIA Cloud Native Technologies&nbsp; documentation</i>. <a href="https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html">https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html</a></div>
  <span class="Z3988" title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Adc&amp;rft.type=webpage&amp;rft.title=Installation%20Guide%20%E2%80%94%20NVIDIA%20Cloud%20Native%20Technologies%20%20documentation&amp;rft.identifier=https%3A%2F%2Fdocs.nvidia.com%2Fdatacenter%2Fcloud-native%2Fcontainer-toolkit%2Finstall-guide.html&amp;rft.au=undefined&amp;rft.date=2023-03-08"></span>
  <div class="csl-entry">NVIDIA Corporation. (2023b, March 8). <i>User Guide—NVIDIA Cloud Native Technologies documentation</i>. <a href="https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/user-guide.html">https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/user-guide.html</a></div>
  <span class="Z3988" title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Adc&amp;rft.type=webpage&amp;rft.title=User%20Guide%20%E2%80%94%20NVIDIA%20Cloud%20Native%20Technologies%20documentation&amp;rft.identifier=https%3A%2F%2Fdocs.nvidia.com%2Fdatacenter%2Fcloud-native%2Fcontainer-toolkit%2Fuser-guide.html&amp;rft.au=undefined&amp;rft.date=2023-03-08"></span>
  <div class="csl-entry">openSUSE contributors &amp; others. (2020, July 22). <i>SDB:NVIDIA drivers—OpenSUSE Wiki</i>. <a href="https://en.opensuse.org/SDB:NVIDIA_drivers">https://en.opensuse.org/SDB:NVIDIA_drivers</a></div>
  <span class="Z3988" title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Adc&amp;rft.type=webpage&amp;rft.title=SDB%3ANVIDIA%20drivers%20-%20openSUSE%20Wiki&amp;rft.identifier=https%3A%2F%2Fen.opensuse.org%2FSDB%3ANVIDIA_drivers&amp;rft.au=undefined&amp;rft.date=2020-07-22"></span>