#!/usr/bin/env python3
import urllib.request
import json

def run():
    url = "http://ip-api.com/json/"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            print("[LIVE PING TELEMETRY]")
            print("  IP Address: ", data.get("query"))
            print("  ISP/Carrier:", data.get("isp"))
            print("  Coordinates:", f"{data.get('lat')}, {data.get('lon')}")
            print("  Location:   ", f"{data.get('city')}, {data.get('regionName')} {data.get('zip')}")
            print("  Country:    ", data.get("country"))
    except Exception as e:
        print("[FAIL-CLOSED] Telemetry fetch error:", e)

if __name__ == "__main__":
    run()
