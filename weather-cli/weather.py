#!/usr/bin/env python3
"""weather-cli - current conditions from wttr.in. stdlib only."""

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://wttr.in/{place}?format=j1"


def fetch(place):
    url = BASE.format(place=urllib.parse.quote(place))
    with urllib.request.urlopen(url, timeout=8) as r:
        return json.loads(r.read().decode())


def summarise(data):
    cur = data["current_condition"][0]
    area = data["nearest_area"][0]
    city = area["areaName"][0]["value"]
    region = area["region"][0]["value"]
    return {
        "place": f"{city}, {region}",
        "temp_c": cur["temp_C"],
        "feels_c": cur["FeelsLikeC"],
        "desc": cur["lang_en"][0]["value"] if cur.get("lang_en") else cur["weatherDesc"][0]["value"],
        "humidity": cur["humidity"],
        "wind_kmph": cur["windspeedKmph"],
    }


def render(info, as_json=False):
    if as_json:
        print(json.dumps(info, indent=2))
    else:
        print(f"{info['place']}")
        print(f"{info['desc']}, {info['temp_c']}°C (feels {info['feels_c']}°C)")
        print(f"humidity {info['humidity']}%  ·  wind {info['wind_kmph']} km/h")


def main():
    ap = argparse.ArgumentParser(description="current weather via wttr.in")
    ap.add_argument("place", nargs="?", default="", help="city (default: auto-ip)")
    ap.add_argument("--json", action="store_true", help="raw summary as json")
    a = ap.parse_args()
    try:
        render(summarise(fetch(a.place)), a.json)
    except urllib.error.URLError:
        sys.exit("couldn't reach wttr.in — check your connection and try again")
    except (KeyError, IndexError):
        sys.exit("unexpected response from wttr.in — maybe the place name?")


if __name__ == "__main__":
    main()
