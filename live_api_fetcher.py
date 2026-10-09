#!/usr/bin/env python3
"""
CHRONOS OS // LIVE PUBLIC API FETCHER
Directly queries active public government APIs:
1. US Census Bureau Geocoder (Coordinates, FIPS, Tract)
2. USGS National Map (Elevation / 3DEP)
3. USGS Seismic Hazards API (Fault / Earthquake History)
4. NOAA / National Weather Service (Active Hazard & Fire Warnings)
5. RentCast / Commercial Gateway (Assessor Roll & Valuation)
"""

import os
import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime

class LiveAPIFetcher:
    def __init__(self):
        self.headers = {"User-Agent": "ChronosAuditEngine/1.0 (Public Records & Safety Research)"}
        self.rentcast_key = os.environ.get("RENTCAST_API_KEY")

    def _http_get(self, url: str, extra_headers: dict = None, timeout: int = 10) -> dict:
        headers = self.headers.copy()
        if extra_headers:
            headers.update(extra_headers)
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw)

    def fetch_census_geocoder(self, address: str) -> dict:
        """Pulls exact coordinates, FIPS, and Census Block from US Census Bureau."""
        base_url = "https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress"
        params = urllib.parse.urlencode({
            "address": address,
            "benchmark": "Public_AR_Current",
            "vintage": "Current_Current",
            "format": "json"
        })
        url = f"{base_url}?{params}"
        try:
            data = self._http_get(url)
            matches = data.get("result", {}).get("addressMatches", [])
            if not matches:
                return {"status": "NO_MATCH", "raw_url": url}
            
            top = matches[0]
            coords = top.get("coordinates", {})
            geographies = top.get("geographies", {})
            counties = geographies.get("Counties", [{}])[0]
            tracts = geographies.get("Census Tracts", [{}])[0]

            return {
                "status": "SUCCESS",
                "matched_address": top.get("matchedAddress"),
                "lon": coords.get("x"),
                "lat": coords.get("y"),
                "state_fips": counties.get("STATE"),
                "county_fips": counties.get("COUNTY"),
                "full_fips": f"{counties.get('STATE')}{counties.get('COUNTY')}",
                "county_name": counties.get("NAME"),
                "census_tract": tracts.get("TRACT")
            }
        except Exception as e:
            return {"status": "ERROR", "error": str(e)}

    def fetch_usgs_elevation(self, lat: float, lon: float) -> dict:
        """Queries USGS National Map 3DEP elevation service."""
        url = f"https://epqs.nationalmap.gov/v1/json?x={lon}&y={lat}&units=Feet"
        try:
            data = self._http_get(url)
            elev = data.get("value")
            return {
                "status": "SUCCESS",
                "elevation_feet": float(elev) if elev is not None else None,
                "data_source": "USGS 3D Elevation Program (3DEP)"
            }
        except Exception as e:
            return {"status": "ERROR", "error": str(e)}

    def fetch_usgs_seismic_risk(self, lat: float, lon: float, radius_km: int = 50) -> dict:
        """Queries USGS ComCat for historical and recent seismic activity within radius."""
        base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
        params = urllib.parse.urlencode({
            "format": "geojson",
            "latitude": lat,
            "longitude": lon,
            "maxradiuskm": radius_km,
            "minmagnitude": 3.0,
            "limit": 5
        })
        url = f"{base_url}?{params}"
        try:
            data = self._http_get(url)
            features = data.get("features", [])
            summary = []
            for f in features:
                props = f.get("properties", {})
                summary.append({
                    "place": props.get("place"),
                    "magnitude": props.get("mag"),
                    "time": datetime.fromtimestamp(props.get("time", 0) / 1000).strftime('%Y-%m-%d')
                })
            return {
                "status": "SUCCESS",
                "events_found_within_radius": len(features),
                "radius_km": radius_km,
                "recent_events": summary
            }
        except Exception as e:
            return {"status": "ERROR", "error": str(e)}

    def fetch_noaa_hazard_alerts(self, lat: float, lon: float) -> dict:
        """Queries NOAA / NWS API for active weather and fire danger alerts."""
        try:
            # 1. Get NWS point metadata
            point_url = f"https://api.weather.gov/points/{lat},{lon}"
            point_data = self._http_get(point_url)
            cwa = point_data.get("properties", {}).get("cwa")
            county_zone = point_data.get("properties", {}).get("county")

            # 2. Query active alerts for this zone
            if county_zone:
                zone_id = county_zone.split("/")[-1]
                alerts_url = f"https://api.weather.gov/alerts/active/zone/{zone_id}"
                alerts_data = self._http_get(alerts_url)
                alerts = [a.get("properties", {}).get("headline") for a in alerts_data.get("features", [])]
                return {
                    "status": "SUCCESS",
                    "nws_forecast_office": cwa,
                    "active_hazard_alerts_count": len(alerts),
                    "active_alerts": alerts
                }
            return {"status": "SUCCESS", "active_hazard_alerts_count": 0, "active_alerts": []}
        except Exception as e:
            return {"status": "ERROR", "error": str(e)}

    def fetch_live_property_records(self, address: str) -> dict:
        """Queries commercial real estate APIs (RentCast) if an API key is available."""
        if not self.rentcast_key:
            return {
                "status": "UNCONFIGURED",
                "message": "RENTCAST_API_KEY environment variable is not set. Set export RENTCAST_API_KEY='...' for live deed & valuation payloads."
            }
        
        base_url = "https://api.rentcast.io/v1/properties"
        params = urllib.parse.urlencode({"address": address})
        url = f"{base_url}?{params}"
        try:
            data = self._http_get(url, extra_headers={"X-Api-Key": self.rentcast_key})
            return {"status": "SUCCESS", "data": data}
        except Exception as e:
            return {"status": "ERROR", "error": str(e)}

    def run_live_audit(self, address: str):
        print("=" * 72)
        print("         CHRONOS OS // LIVE PUBLIC API AUDIT ENGINE")
        print("=" * 72)
        print(f"Target Input: {address}")
        print(f"Timestamp:    {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")

        # 1. US Census Bureau Geocoding
        print("[1/4] Querying US Census Bureau Geocoder API...")
        census = self.fetch_census_geocoder(address)
        if census.get("status") != "SUCCESS":
            print(f"  [FAILED] Census geocode failed: {census}")
            return
        
        lat = census["lat"]
        lon = census["lon"]
        fips = census["full_fips"]
        print(f"  -> Matched Situs: {census['matched_address']}")
        print(f"  -> Coordinates:   Lat {lat}, Lon {lon}")
        print(f"  -> Federal FIPS:  {fips} ({census['county_name']} County)")
        print(f"  -> Census Tract:  {census['census_tract']}\n")

        # 2. USGS Elevation
        print("[2/4] Querying USGS National 3DEP Elevation API...")
        elev = self.fetch_usgs_elevation(lat, lon)
        if elev.get("status") == "SUCCESS":
            print(f"  -> Ground Elevation: {elev['elevation_feet']} ft ({elev['data_source']})\n")
        else:
            print(f"  -> Elevation Error: {elev.get('error')}\n")

        # 3. USGS Seismic & Fault Events
        print("[3/4] Querying USGS Real-Time Earthquake / Seismic API...")
        seismic = self.fetch_usgs_seismic_risk(lat, lon, radius_km=50)
        if seismic.get("status") == "SUCCESS":
            print(f"  -> Recorded Events (M3.0+ within 50km): {seismic['events_found_within_radius']}")
            for evt in seismic.get("recent_events", []):
                print(f"     • M{evt['magnitude']} on {evt['time']} - {evt['place']}")
            print()
        else:
            print(f"  -> Seismic Error: {seismic.get('error')}\n")

        # 4. NOAA National Weather Service
        print("[4/4] Querying NOAA / National Weather Service Active Alerts...")
        weather = self.fetch_noaa_hazard_alerts(lat, lon)
        if weather.get("status") == "SUCCESS":
            print(f"  -> NWS Station/CWA: {weather.get('nws_forecast_office')}")
            print(f"  -> Active Hazard Alerts: {weather['active_hazard_alerts_count']}")
            for a in weather.get("active_alerts", []):
                print(f"     • {a}")
            print()
        else:
            print(f"  -> NOAA Error: {weather.get('error')}\n")

        # 5. Commercial Real Estate Gateway
        print("[5/5] Checking Commercial Real Estate Gateway Status...")
        cre = self.fetch_live_property_records(address)
        print(f"  -> Status: {cre['status']}")
        if cre["status"] == "UNCONFIGURED":
            print(f"  -> Note: {cre['message']}")
        elif cre["status"] == "SUCCESS":
            print(f"  -> Live Payload Retrieved: {json.dumps(cre['data'], indent=2)[:300]}...")
        print("=" * 72)

if __name__ == "__main__":
    addr = sys.argv[1] if len(sys.argv) > 1 else "431 Chablis Dr, Ukiah, CA 95482"
    fetcher = LiveAPIFetcher()
    fetcher.run_live_audit(addr)
