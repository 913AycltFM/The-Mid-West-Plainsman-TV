from datetime import datetime, timedelta, timezone
from pathlib import Path
import re
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET
from zoneinfo import ZoneInfo

TIMEZONE = ZoneInfo("America/Chicago")
UTC = timezone.utc

DAYS_AHEAD = 7
HOURS_AHEAD = DAYS_AHEAD * 24
REFRESH_MINUTES = 5

CHANNEL_ID = "TheMidWestPlainsman"
CHANNEL_DISPLAY = "1"
CHANNEL_NAME = "The Mid West Plainsman"
DESCRIPTION = (
    "The Mid West Plainsman Is A Media Broadcast Content Creator In Waterloo, "
    "Iowa Covering Everything In The Cedar Valley Corridor and Central Iowa"
)

LOGO = "https://mp3tourl.com/images/1790116393287-639eac7e-fc16-40d4-b39c-3f7378f54dc5.jpg"
BACKGROUND = "https://mp3tourl.com/images/1790116455920-0030dd1a-85d7-401a-bb1b-8cdb4160da9a.png"
STREAM_HOST = "tv.913aycltfm.com"

XML_OUTPUT = Path("The-Mid-West-Plainsman-TV-Guide.xml")
M3U_INPUT = Path("The-Mid-West-Plainsman-TV.m3u")


def xmltv_datetime(value):
    """Format an aware datetime using its correct local UTC offset."""
    local = value.astimezone(TIMEZONE)
    offset = local.utcoffset() or timedelta(0)
    minutes = int(offset.total_seconds() // 60)
    sign = "+" if minutes >= 0 else "-"
    minutes = abs(minutes)
    return (
        f"{local:%Y%m%d%H%M%S} "
        f"{sign}{minutes // 60:02d}{minutes % 60:02d}"
    )


def five_minute_start(now=None):
    """Return the current time rounded down to the latest five-minute mark."""
    current = (now or datetime.now(UTC)).astimezone(UTC)
    minute = current.minute - (current.minute % REFRESH_MINUTES)
    return current.replace(minute=minute, second=0, microsecond=0)


def build_events(start):
    """Build a continuous seven-day guide using real elapsed hours."""
    start_utc = start.astimezone(UTC)
    events = []

    for hour in range(HOURS_AHEAD):
        event_start = start_utc + timedelta(hours=hour)
        event_end = event_start + timedelta(hours=1)
        events.append(
            {
                "channel_id": CHANNEL_ID,
                "title": CHANNEL_NAME,
                "description": DESCRIPTION,
                "start": event_start,
                "end": event_end,
                "icon": BACKGROUND,
            }
        )

    return events


def generate_xml(events):
    root = ET.Element(
        "tv",
        {
            "generator-info-name": "TheMidWestPlainsmanTV",
            "generator-info-url": (
                "https://github.com/913AycltFM/"
                "The-Mid-West-Plainsman-TV-Guide"
            ),
        },
    )

    channel = ET.SubElement(root, "channel", {"id": CHANNEL_ID})
    ET.SubElement(channel, "display-name").text = CHANNEL_DISPLAY
    ET.SubElement(channel, "display-name").text = CHANNEL_NAME
    ET.SubElement(channel, "icon", {"src": LOGO})

    for event in events:
        programme = ET.SubElement(
            root,
            "programme",
            {
                "start": xmltv_datetime(event["start"]),
                "stop": xmltv_datetime(event["end"]),
                "channel": CHANNEL_ID,
            },
        )
        ET.SubElement(programme, "title", {"lang": "en"}).text = event["title"]
        ET.SubElement(programme, "desc", {"lang": "en"}).text = event["description"]
        ET.SubElement(programme, "icon", {"src": event["icon"]})

    ET.indent(root, space="  ")
    body = ET.tostring(root, encoding="unicode")
    document = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<!DOCTYPE tv SYSTEM "xmltv.dtd">\n'
        f"{body}\n"
    )

    temporary = XML_OUTPUT.with_suffix(XML_OUTPUT.suffix + ".tmp")
    temporary.write_text(document, encoding="utf-8")
    temporary.replace(XML_OUTPUT)


def validate_timeline(events):
    if len(events) != HOURS_AHEAD:
        raise ValueError(
            f"Expected {HOURS_AHEAD} programmes, received {len(events)}."
        )

    first = events[0]["start"]
    if first.minute % REFRESH_MINUTES or first.second or first.microsecond:
        raise ValueError("The EPG start time is not aligned to five minutes.")

    for index, event in enumerate(events):
        start = event["start"].astimezone(UTC)
        end = event["end"].astimezone(UTC)
        if end - start != timedelta(hours=1):
            raise ValueError(f"Programme {index + 1} is not exactly one hour.")
        if index:
            previous_end = events[index - 1]["end"].astimezone(UTC)
            if start != previous_end:
                raise ValueError(
                    f"Gap or overlap before programme {index + 1}."
                )


def validate_xml(events):
    root = ET.parse(XML_OUTPUT).getroot()
    if root.tag != "tv":
        raise ValueError("XMLTV root element must be <tv>.")

    channel = root.find(f"channel[@id='{CHANNEL_ID}']")
    if channel is None:
        raise ValueError(f"Missing XMLTV channel: {CHANNEL_ID}.")

    names = [node.text for node in channel.findall("display-name")]
    if CHANNEL_DISPLAY not in names or CHANNEL_NAME not in names:
        raise ValueError("XMLTV channel display name or number is incorrect.")

    channel_icon = channel.find("icon")
    if channel_icon is None or channel_icon.get("src") != LOGO:
        raise ValueError("XMLTV channel logo is incorrect.")

    programmes = root.findall("programme")
    if len(programmes) != len(events):
        raise ValueError("XMLTV programme count does not match generated events.")

    for index, (programme, event) in enumerate(zip(programmes, events), 1):
        if programme.get("channel") != CHANNEL_ID:
            raise ValueError(f"Programme {index} has the wrong channel ID.")
        if programme.get("start") != xmltv_datetime(event["start"]):
            raise ValueError(f"Programme {index} start time is incorrect.")
        if programme.get("stop") != xmltv_datetime(event["end"]):
            raise ValueError(f"Programme {index} stop time is incorrect.")
        if programme.findtext("title") != event["title"]:
            raise ValueError(f"Programme {index} title is incorrect.")
        if programme.findtext("desc") != event["description"]:
            raise ValueError(f"Programme {index} description is incorrect.")
        icon = programme.find("icon")
        if icon is None or icon.get("src") != BACKGROUND:
            raise ValueError(f"Programme {index} artwork is incorrect.")


def validate_m3u():
    if not M3U_INPUT.is_file():
        raise ValueError(f"Missing IPTV playlist: {M3U_INPUT}.")

    lines = [
        line.strip()
        for line in M3U_INPUT.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]
    if not lines or lines[0] != "#EXTM3U":
        raise ValueError("M3U playlist must begin with #EXTM3U.")

    entries = [line for line in lines if line.startswith("#EXTINF:")]
    urls = [
        line for line in lines
        if not line.startswith("#")
    ]
    if len(entries) != 1 or len(urls) != 1:
        raise ValueError("M3U must contain exactly one channel and one stream URL.")

    metadata = entries[0]
    required_metadata = (
        f'tvg-id="{CHANNEL_ID}"',
        f'tvg-name="{CHANNEL_NAME}"',
        f'tvg-logo="{LOGO}"',
        f'tvg-background="{BACKGROUND}"',
        f'tvg-art="{BACKGROUND}"',
        'tvg-chno="1"',
        'group-title="Live"',
    )
    for item in required_metadata:
        if item not in metadata:
            raise ValueError(f"M3U channel metadata is missing: {item}")

    stream = urlsplit(urls[0])
    stream_id = stream.path.removeprefix("/memfs/").removesuffix(".m3u8")
    if (
        stream.scheme != "https"
        or stream.netloc != STREAM_HOST
        or not stream.path.startswith("/memfs/")
        or not stream.path.endswith(".m3u8")
        or not re.fullmatch(r"[A-Za-z0-9-]+", stream_id)
        or stream.query
        or stream.fragment
    ):
        raise ValueError(f"M3U stream URL is invalid: {urls[0]}")


def validate_dst_handling():
    """Confirm Central Time's spring-forward and fall-back offsets."""
    spring = build_events(datetime(2026, 3, 8, 6, 0, tzinfo=UTC))
    spring_local = [event["start"].astimezone(TIMEZONE) for event in spring[:4]]
    if [value.hour for value in spring_local] != [0, 1, 3, 4]:
        raise ValueError("Central Time spring daylight-saving transition failed.")

    autumn = build_events(datetime(2026, 11, 1, 5, 0, tzinfo=UTC))
    autumn_local = [event["start"].astimezone(TIMEZONE) for event in autumn[:3]]
    if [value.hour for value in autumn_local] != [0, 1, 1]:
        raise ValueError("Central Time fall daylight-saving transition failed.")
    if autumn_local[1].utcoffset() == autumn_local[2].utcoffset():
        raise ValueError("Central Time fall-back UTC offsets were not distinguished.")


def main():
    events = build_events(five_minute_start())
    validate_timeline(events)
    validate_dst_handling()
    generate_xml(events)
    validate_xml(events)
    validate_m3u()

    first = events[0]["start"].astimezone(TIMEZONE)
    last = events[-1]["end"].astimezone(TIMEZONE)
    print(
        f"Validation successful: {len(events)} continuous hourly programmes "
        f"for {CHANNEL_NAME}; seven-day window {first.isoformat()} to "
        f"{last.isoformat()}; five-minute alignment; Central Time DST; "
        "XMLTV and M3U valid."
    )


if __name__ == "__main__":
    main()
