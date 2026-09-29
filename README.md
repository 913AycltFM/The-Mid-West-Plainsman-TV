# The Mid West Plainsman TV

Independent IPTV / Jellyfin / Plex project for **The Mid West Plainsman**.

## Channel

| Channel | Number | Guide ID |
|---|---:|---|
| The Mid West Plainsman | 1.5 | `TheMidWestPlainsman` |

## IPTV playlist

`The-Mid-West-Plainsman-TV.m3u`

XMLTV guide:
`https://raw.githubusercontent.com/913AycltFM/The-Mid-West-Plainsman-TV/main/The-Mid-West-Plainsman-TV.xml`

## Stream

`https://tv.913aycltfm.com/memfs/552ab1b0-d31a-4a5f-a9d7-d58a280deba2.m3u8`

## EPG

The repository maintains a 7-day rolling XMLTV guide in **America/Chicago**. It currently provides hourly filler entries so IPTV clients always have continuous guide coverage.

## Automatic updates

GitHub Actions regenerates the guide every **5 minutes**.

Workflow: `.github/workflows/update-epg.yml`

## Files

- `The-Mid-West-Plainsman-TV.m3u` — IPTV playlist
- `The-Mid-West-Plainsman-TV.xml` — XMLTV guide
- `epg.json` — JSON guide
- `generate_epg.py` — EPG generator
- `.github/workflows/update-epg.yml` — 5-minute updater

## Artwork

Logo: https://mp3tourl.com/images/1790116393287-639eac7e-fc16-40d4-b39c-3f7378f54dc5.jpg

Background: https://mp3tourl.com/images/1790116455920-0030dd1a-85d7-401a-bb1b-8cdb4160da9a.png
