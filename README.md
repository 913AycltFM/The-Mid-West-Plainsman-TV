# The Mid West Plainsman TV

Lightweight, IPTV-only playlist and XMLTV programme guide for **The Mid West Plainsman**.

## Channel

| Channel | Number | XMLTV ID |
|---|---:|---|
| The Mid West Plainsman | 1 | `TheMidWestPlainsman` |

## IPTV playlist

**M3U URL**

```text
https://raw.githubusercontent.com/913AycltFM/The-Mid-West-Plainsman-TV/main/The-Mid-West-Plainsman-TV.m3u
```

The playlist contains the single live HLS stream and its channel metadata, including the channel logo and background artwork.

## Electronic programme guide

**XMLTV URL**

```text
https://raw.githubusercontent.com/913AycltFM/The-Mid-West-Plainsman-TV/main/The-Mid-West-Plainsman-TV-Guide.xml
```

**JSON EPG URL**

```text
https://raw.githubusercontent.com/913AycltFM/The-Mid-West-Plainsman-TV/main/epg.json
```

### Guide details

- One IPTV channel: The Mid West Plainsman (Channel 1).
- Seven-day rolling guide with 168 continuous, one-hour programme entries.
- Guide start aligns to the latest five-minute interval.
- GitHub Actions runs the generator every five minutes.
- Time zone: `America/Chicago`, with daylight-saving transitions handled automatically.
- The channel logo is used for the XMLTV channel icon; the background artwork is used for programme artwork.
- XMLTV, JSON, and M3U metadata are validated before the guide can be committed.
- The JSON feed contains the same 168 filler entries, channel metadata, artwork URLs, and ISO 8601 Central Time timestamps as the XMLTV guide.

## Current schedule behavior

No machine-readable programme schedule or schedule API is configured in this repository yet. Until a verified schedule source is connected, the guide uses generic hourly **The Mid West Plainsman** entries. These are placeholders, not a claim that a specific show is airing at those times.

## Artwork

- Channel logo: https://mp3tourl.com/images/1790116393287-639eac7e-fc16-40d4-b39c-3f7378f54dc5.jpg
- Channel background and programme artwork: https://mp3tourl.com/images/1790116455920-0030dd1a-85d7-401a-bb1b-8cdb4160da9a.png

## Repository files

- `The-Mid-West-Plainsman-TV.m3u` — single-channel IPTV playlist.
- `The-Mid-West-Plainsman-TV-Guide.xml` — generated XMLTV guide.
- `epg.json` — generated JSON version of the same guide.
- `generate_epg.py` — Python EPG generator and validation.
- `.github/workflows/update-epg.yml` — five-minute automated refresh.

This repository is designed for IPTV applications and services such as Jellyfin, Plex, and compatible IPTV players. It does not include a website, web player, or PWA.
