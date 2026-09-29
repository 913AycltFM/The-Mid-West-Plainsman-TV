import json
from datetime import datetime, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET
from zoneinfo import ZoneInfo

TIMEZONE = ZoneInfo("America/Chicago")
DAYS_AHEAD = 7
CHANNEL_ID = "TheMidWestPlainsman"
CHANNEL_DISPLAY = "1"
CHANNEL_NAME = "The Mid West Plainsman"
DESCRIPTION = "The Mid West Plainsman Is A Media Broadcast Content Creator In Waterloo, Iowa Covering Everything In The Cedar Valley Corridor and Central Iowa"
ICON = "https://mp3tourl.com/images/1790116455920-0030dd1a-85d7-401a-bb1b-8cdb4160da9a.png"
XML_OUTPUT = "The-Mid-West-Plainsman-TV.xml"
JSON_OUTPUT = "epg.json"

def xmltv_datetime(dt):
    offset = dt.astimezone(TIMEZONE).utcoffset() or timedelta(0)
    minutes = int(offset.total_seconds() / 60)
    sign = "+" if minutes >= 0 else "-"
    minutes = abs(minutes)
    return f"{dt.astimezone(TIMEZONE):%Y%m%d%H%M%S} {sign}{minutes // 60:02d}{minutes % 60:02d}"

def build_events(start, end):
    events = []
    current = start
    while current < end:
        stop = min(current + timedelta(hours=1), end)
        events.append({"channel_id": CHANNEL_ID, "station_name": CHANNEL_NAME, "title": CHANNEL_NAME, "description": DESCRIPTION, "start": current, "end": stop, "icon": ICON, "fallback": True, "live": False})
        current = stop
    return events

def generate_xml(events):
    root = ET.Element("tv", {"generator-info-name": "MidWestPlainsmanTV"})
    channel = ET.SubElement(root, "channel", {"id": CHANNEL_ID})
    ET.SubElement(channel, "display-name").text = CHANNEL_DISPLAY
    ET.SubElement(channel, "display-name").text = CHANNEL_NAME
    ET.SubElement(channel, "icon", {"src": ICON})
    for event in events:
        programme = ET.SubElement(root, "programme", {"start": xmltv_datetime(event["start"]), "stop": xmltv_datetime(event["end"]), "channel": CHANNEL_ID})
        ET.SubElement(programme, "title", {"lang": "en"}).text = event["title"]
        ET.SubElement(programme, "desc", {"lang": "en"}).text = event["description"]
        ET.SubElement(programme, "icon", {"src": event["icon"]})
    ET.indent(root, space="  ")
    path = Path(XML_OUTPUT)
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)
    xml = path.read_text(encoding="utf-8").replace("<?xml version='1.0' encoding='utf-8'?>", '<?xml version="1.0" encoding="utf-8"?>', 1)
    xml = xml.replace('<?xml version="1.0" encoding="utf-8"?>', '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE tv SYSTEM "xmltv.dtd">', 1)
    path.write_text(xml, encoding="utf-8")

def generate_json(events):
    output = []
    for event in events:
        item = dict(event)
        item["start"] = event["start"].isoformat()
        item["end"] = event["end"].isoformat()
        item["live_badge"] = ""
        item["display_title"] = event["title"]
        output.append(item)
    Path(JSON_OUTPUT).write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")

def main():
    now = datetime.now(TIMEZONE)
    start = now.replace(minute=0, second=0, microsecond=0)
    end = start + timedelta(days=DAYS_AHEAD)
    events = build_events(start, end)
    generate_xml(events)
    generate_json(events)
    ET.parse(XML_OUTPUT)
    print(f"Generated {len(events)} EPG programmes for {CHANNEL_NAME}.")

if __name__ == "__main__":
    main()
