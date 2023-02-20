---
title: My Config File for Downloading Albums from YouTube Music
description: Download albums from YouTube Music with embedded metadata and properly cropped thumbnail.
date: 2023-02-19
slug: youtube-music-album-download
tags:
    - computer
    - youtube music
    - audio
    - yt-dlp
draft: false
commentid: 109896605187791468
---

## The Config File

Here's the config file:

```sh
# yt-dlp.conf

# Output format: album/tracks.format
-o "%(album,playlist_title)U - [%(playlist_id)s]/%(track_number,playlist_index)s - %(title)U - [%(id)s].%(ext)s"
--windows-filenames 
# --restrict-filenames 

# Extract audio
-f bestaudio
--extract-audio

# Thumbnail squared
--convert-thumbnails png
--ppa "ThumbnailsConvertor+ffmpeg_o:-c:v png -vf crop=\"'if(gt(ih,iw),iw,ih)':'if(gt(iw,ih),ih,iw)'\""
--embed-thumbnail

# Metadata, with playlist number as track number if the latter is missing
--embed-metadata
--parse-metadata "playlist_index:%(track_number)s"

# Misc
--no-overwrites
--concurrent-fragments 4
```

## The Explanation

### Output formats. 

The files are organized into one-directory-per-album, like the following:

```
...
├── Bach, J.S.： Sonatas & Partitas - [OLAK5uy_nd-ZT5mVVQ4tFm_6FsJWbj-u6GypaFYe8]
│   ├── 01 - J.S. Bach： Sonata for Violin Solo No. 1 in G Minor, BWV 1001 - I. Adagio - [ZePaXgWY7-Q].opus
│   ├── 02 - J.S. Bach： Sonata for Violin Solo No. 1 in G Minor, BWV 1001 - II. Fuga. Allegro - [93p59vL87cE].opus
│   ├── 03 - J.S. Bach： Sonata for Violin Solo No. 1 in G Minor, BWV 1001 - III. Siciliana - [BRssao79MDM].opus
│   ├── 04 - J.S. Bach： Sonata for Violin Solo No. 1 in G Minor, BWV 1001 - IV. Presto - [NP_LSvkqLjg].opus
│   ├── 05 - J.S. Bach： Partita for Violin Solo No. 1 in B Minor, BWV 1002 - Ia. Allemanda - [4C8pA-8Hy8Q].opus
│   ├── 06 - J.S. Bach： Partita for Violin Solo No. 1 in B Minor, BWV 1002 - Ib. Double - [vy43_64aax8].opus
│   ├── 07 - J.S. Bach： Partita for Violin Solo No. 1 in B Minor, BWV 1002 - IIa. Corrente - [yiHc8-quDIc].opus
...
```

- The output template: `"%(album,playlist_title)U - [%(playlist_id)s]/%(track_number,playlist_index)s - %(title)U - [%(id)s].%(ext)s"`
  - `%(album,playlist_title)U` tells `yt-dlp` to use the album's name, and if that does not exist, use the playlist's title, the trailing "U" indicating that the string should be normalized. 
  - `%(track_number,playlist_index)s` means that the file name begins with the track number, which makes it easier to sort the files, if the file manager or app is not metadata-aware. 
  - `%(title)U` is the title normalized.
  - `%(ext)s` is the extension.
  - `%(id)s` and `%(playlist_id)s` are the unique ID that YouTube assigns to the file and the playlist respectively, which might be useful if later I need to get more data from YouTube.

- Sanitizing filenames
  
  - `--restrict-filenames` sanitizes the string of illegal characters. Some file systems support more characters than others, so in theory, it makes sense to err on the side of caution. However, this flag replaces all non-ASCII characters and even special ASCII characters with underscores, which is way too aggressive. While it makes file systems very happy, (an incompatibility is basically impossible), all titles, except the pure English ones, get mangled. "Dvořák" becomes "Dvor_k", "Ysaÿe" now read "Ysa_e", and some titles started making funny faces: `-___-` 
  
  - `--windows-filenames` does exactly what it says on the tin: it makes the string Windows-compatible. I'd prefer if it is a little bit more aggressive, for instance, removing `&` which some cloud drives don't support, but it's a good enough trade-off.


### Metadata

`--embed-metadata` tells `yt-dlp` to embed metadata. Some albums don't have the proper track number set up, which means that when you import the files into a music player, the order of the album gets scrambled up. 

`--parse-metadata "playlist_index:%(track_number)s"` uses the playlist index, which should always be present when downloading a playlist, to fill the track number.

### Thumbnails

- `--embed-thumbnail` tells `yt-dlp` to embed a thumbnail;
- `--convert-thumbnails png` indicates that the format of the thumbnail should be `png`. `webp` is possibly the best image format available in `yt-dlp`, but its popularity being so recent, I'm wary of its compatibility with music players. Either `png` or `jpeg` should be fine.

By default, YouTube provides a padded, rectangular image. To cut off the padding, we can use `ffmpeg` in post-processing. In this [Github Issue](https://github.com/yt-dlp/yt-dlp/issues/429), pukkandan(2021) gave a solution: `--ppa "EmbedThumbnail+ffmpeg_o:-c:v mjpeg -vf crop=\"'if(gt(ih,iw),iw,ih)':'if(gt(iw,ih),ih,iw)'\""`. But on my machine, `yt-dlp` seems to ignore this instruction. Even with `--verbose` turned on, I could see no log about cropping the thumbnail, and if I mangle the command deliberately, no error is produced, either. All I get is the same padded rectangular image in the end.

According to `yt-dlp`'s README:

> Supported PP are: Merger, ModifyChapters, SplitChapters, ExtractAudio, VideoRemuxer, VideoConvertor, Metadata, EmbedSubtitle, **EmbedThumbnail**, SubtitlesConvertor, **ThumbnailsConvertor**, FixupStretched, FixupM4a, FixupM3u8, FixupTimestamp and FixupDuration.

`EmbedThumbnail` and `ThumbnailsConvertor` must be the two relevant options, so I gave the latter a try: `--ppa "ThumbnailsConvertor+ffmpeg_o:-c:v png -vf crop=\"'if(gt(ih,iw),iw,ih)':'if(gt(iw,ih),ih,iw)'\""`. And, _hooray_, it works!

My guess is that there's some sort of conflict amongst the sequence of converting the image to the right format, embedding the image, and post-processing the image. In a way, I think it makes sense that thumbnail convertor post processor is the right option here, as it implies that we are processing **after the conversion** and **before the embedding**, whereas post-processing `EmbedThumbnail` would suggest that we are cropping after the embedding occurs, which would be rather not useful. But this is just a speculation. Without digging into the code, it's impossible to tell what exactly is happening here.


### Miscellaneous

`--no-overwrites`: Don't overwrite files.

`--concurrent-fragments 4`: Download 4 fragments concurrently to speed up the process.


## References

pukkandan. (2021, June 23). *Comment on [Feature Request] Crop to square thumbnail when embedding in MP3s*. [[Feature Request] Crop to square thumbnail when embedding in MP3s · Issue #429 · yt-dlp/yt-dlp · GitHub](https://github.com/yt-dlp/yt-dlp/issues/429#issuecomment-866836396)

yt-dlp. (2023). *Yt-dlp* [Python]. yt-dlp. [GitHub - yt-dlp/yt-dlp: A youtube-dl fork with additional features and fixes](https://github.com/yt-dlp/yt-dlp) (Original work published 2020)
