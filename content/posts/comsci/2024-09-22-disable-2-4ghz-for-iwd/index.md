---
title: Disable 2.4GHz for IWD
description: |
    I debugged my insanely fluctuating WIFI latency, and found out that the 2.4GHz band had gone rogue. As the router doesn't belong to me, I have to apply a workaround where IWD is configured to not scan 2.4GHz network.

date: 2024-09-22
slug: disable-2-4ghz-for-iwd
tags:
    - wifi
    - iwd
draft: true
references:
    - id: marcelholtmannIwdconfig5ArchManual2019
      accessed:
          - year: 2024
            month: 9
            day: 22
      author:
          - literal: Marcel Holtmann
          - literal: Denis Kenzior
          - literal: Andrew Zaborowski
          - literal: James Prestwood
          - literal: Tim Kourt
      citation-key: marcelholtmannIwdconfig5ArchManual2019
      issued:
          - year: 2019
            month: 9
            day: 22
      title: iwd.config(5) — Arch manual pages
      type: webpage
      URL: https://man.archlinux.org/man/iwd.config.5.en#Rank

    - id: sethSOLVEDHowForce2023
      accessed:
          - year: 2024
            month: 9
            day: 22
      author:
          - literal: seth
      citation-key: sethSOLVEDHowForce2023
      issued:
          - year: 2023
            month: 3
            day: 19
      title: >-
          [SOLVED] How to force IWD to use 2.4GHz network instead of 5GHz? /
          Networking, Server, and Protection / Arch Linux Forums
      type: webpage
      URL: https://bbs.archlinux.org/viewtopic.php?pid=2090864#p2090864
---

## Debugging an Erratic WIFI Connection

Recently, I had a problem with the WIFI connection on my Linux workstation: sometimes, the latency fluctuates quite badly, occasionally to the point of going offline completely. It doesn't happen all the time, though. I could go through a whole day without a single disruption, but when it started acting out, there was seemingly nothing I could do to stop it. Turning the router off and on again, restarting my PC, forgetting and re-adding the network in Network Manager, etc. all ended up futile.

At first, I thought it was a problem with how the network was configured on my machine. After all, it's Linux, and 90% of the time when something does not function as expected, it's because there's a switch buried in `/etc` whose purpose and usage is detailed on ArchWiki that you just need to flip.

That did not seem to be the case this time. After some painstaking tinkering around---reading system logs & dmesg logs, diving into NetworkManager's config files, replacing wpa_supplicant with IWD, switching back to wpa_supplicant, switching to IWD yet again---I made no progress. The fluctuations came and went as it pleased, unaffected by my efforts to adjust the network configurations.

But I noticed two interesting patterns: 1) when the network is stable, I have about 10ms ping to 1.1.1.1, but when the network is unstable, the best I get is about 20ms; and 2) the latency is fine if the signal is weak, and vice versa., which is very counter-intuitive.

This got me thinking about 5GHz vs 2.4GHz. I knew that 2.4GHz is slower but more penetrative, while 5GHz is the opposite. It must be the case that whenever the network fluctuates, I'm connected to the 2.4GHz band. This can be tested by observing the output of `sudo iwctl station wlan0 show | grep Frequency` (`wlan0` is the name of my wifi adapter in IWD). I ran this command whenever I got the erratic pings, and indeed, it only happened when connected to the 2.4GHz band.

The next step was figuring out whether that was the PC's fault or the route's. The first thought was that it must be the PC, because my phone had been connecting to the internet just fine, but of course, there was nothing that I did on my phone that was sensitive to latency, so I might not have noticed it. And more importantly, the phone might have a different strategy choosing which band to connect to, and it favors the 5GHz band more the PC does.

I took my phone, downloaded one of the WIFI analyzer apps, and started towards a corner of the house, watching as 5GHz signal weakened to the point where the phone switched to 2.4GHz. I tried to ping the router, and well, the familiar fluctuations was reproduced on my phone as well.

The router isn't mine, though. It's one of those ISP provided router and it belongs to my landlord. So the most I can do is to simply disable 2.4GHz.

It turns out, when I'm Googling around, that most people want the other way around: they want to connect to 2.4GHz and disable 5GHz, like [this](https://bbs.archlinux.org/viewtopic.php?id=284405). I think that's because if you are at the edge of 5GHz's effective range, 2.4GHz is usually more stable despite being slower. That is if your 2.4GHz has not gone rogue like mine.

## How to disable 5GHz in IWD

Despite sharing the same SSID (the name you usually see in the list of WIFIs), the 2.4GHz and 5GHz bands of a WIFI, are actually two separate things that can be connected to. The fact that they appear as a unified entity and that our devices can switch between them seamlessly is a feature of convenience.

Therefore, the first thing I tried was setting the connection's BSSID (which is not shared by different frequency bands) in NetworkManager to the one used by the 5GHz band. Logically, this should tell NetworkManager to specifically look for that 5GHz connection, and not try to switch to its erratic sibling. But it didn't work; because I had IWD as the WIFI backend, which doesn't have the capability of connecting to a BSSID [@sethSOLVEDHowForce2023].

At the end of the day, there is a switch buried in `/etc` whose purpose and usage is detailed on ArchWiki that I can flip [@marcelholtmannIwdconfig5ArchManual2019]:

```ini
# /etc/iwd/main.conf
[Rank]
BandModifier5GHz=1.0
BandModifier2_4GHz=0.0
```

The **Rank** section sets the priority of each frequency band with which IWD connects to, and setting it to zero disables it completely.

To complete the picture, here's my setup:

1. Machine: A PC that I assembled;
2. OS/Distribution: Linux version 6.10.9-1-default (geeko@buildhost) (gcc (SUSE Linux) 14.2.0, GNU ld (GNU Binutils; openSUSE Tumbleweed) 2.43.1.20240828-2) #1 SMP PREEMPT_DYNAMIC Sun Sep 8 13:43:05 UTC 2024 (5af7788)
3. Network setup: NetworkManager + IWD
4. WIFI adapter: Wireless-AC 3168NGW, which came with the motherboard.

## I probably need a better router, and a better WIFI adapter for the PC

As mentioned above, when I tested the connection with my phone, my hypothesis was that the phone has a different strategy choosing frequency bands, and it adheres to 5GHz more than the PC, but I was wrong.

Seemingly, the phone just receives a stronger signal. I'm not sure whether this is because the WIFI scanner app calculates RSSI differently from IWD, but if I trust the numbers they gave me, the differences are massive:

|       | 2.4GHz | 5GHz   |
| ----- | ------ | ------ |
| PC    | -67dBm | -71dBm |
| Phone | -48dBm | -53dBm |

Perhaps, in addition to getting a better router with a functional 2.4GHz band, I should also consider getting a more competent WIFI adapter for the PC.

