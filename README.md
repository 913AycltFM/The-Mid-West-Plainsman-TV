# The Mid West Plainsman TV

IPTV-only channel and programme guide for **The Mid West Plainsman**.

## Channel

| Channel | Number | Guide ID |
|---|---:|---|
| The Mid West Plainsman | 1 | `TheMidWestPlainsman` |

## IPTV files

- `The-Mid-West-Plainsman-TV.m3u` — M3U playlist containing the live HLS stream.
- `The-Mid-West-Plainsman-TV-Guide.xml` — XMLTV electronic programme guide.
- `generate_epg.py` — Python generator for the XMLTV guide.
- `.github/workflows/update-epg.yml` — validates and updates the guide automatically.

## XMLTV guide URL

`https://raw.githubusercontent.com/913AycltFM/The-Mid-West-Plainsman-TV-Guide/main/The-Mid-West-Plainsman-TV-Guide.xml`

## M3U playlist URL

`https://raw.githubusercontent.com/913AycltFM/The-Mid-West-Plainsman-TV-Guide/main/The-Mid-West-Plainsman-TV.m3u`

## EPG schedule

- 7-day rolling guide.
- 168 hourly programme entries.
- Time zone: `America/Chicago` (Central Time, including daylight saving time).
- GitHub Actions refreshes the guide every 5 minutes.

The playlist and XMLTV guide are intended for IPTV applications and services such as Jellyfin, Plex, and compatible IPTV players. This repository does not host a website or web app.

## Artwork

- Channel logo: https://mp3tourl.com/images/1790116393287-639eac7e-fc16-40d4-b39c-3f7378f54dc5.jpg
- Channel background: https://mp3tourl.com/images/1790116455920-0030dd1a-85d7-401a-bb1b-8cdb4160da9a.png
