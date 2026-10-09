#!/usr/bin/env python3
"""
CHRONOS OS // GOOGLE MAPS SPATIAL INTEGRATOR
Aggregates all audited property points, addresses, and coordinates across the workspace
and generates direct Google Maps navigation links, interactive HTML map views, and GeoJSON exports.
"""

import os
import json
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [GMAPS-INTEGRATOR] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("GMapsIntegrator")

# Core Audited Properties across California Workspace
AUDITED_PROPERTIES = [
    {
        "name": "Luxury Estate / Distressed Parcel",
        "address": "1850 Crystal Springs Rd, Hillsborough, CA",
        "lat": 37.5630,
        "lon": -122.3650,
        "distress_score": 98.5
    },
    {
        "name": "Beverly Hills Luxury Asset",
        "address": "9420 Gloaming Dr, Beverly Hills, CA",
        "lat": 34.1250,
        "lon": -118.4120,
        "distress_score": 97.2
    },
    {
        "name": "Fresno Commercial Plaza",
        "address": "3100 Tulare St, Fresno, CA",
        "lat": 36.7378,
        "lon": -119.7871,
        "distress_score": 96.8
    },
    {
        "name": "San Diego Coastal Asset",
        "address": "7400 La Jolla Blvd, San Diego, CA",
        "lat": 32.8328,
        "lon": -117.2713,
        "distress_score": 95.4
    },
    {
        "name": "Mendocino / Ukiah Operations Hub",
        "address": "615 Talmage Rd, Ukiah, CA",
        "lat": 39.1502,
        "lon": -123.2078,
        "distress_score": 99.0
    }
]

class GoogleMapsIntegrator:
    def __init__(self):
        self.properties = AUDITED_PROPERTIES

    def generate_google_maps_links(self) -> list:
        links = []
        for p in self.properties:
            query = p["address"].replace(" ", "+")
            maps_url = f"https://www.google.com/maps/search/?api=1&query={query}"
            streetview_url = f"https://www.google.com/maps/@{p['lat']},{p['lon']},3a,75y,90t/data=!3m6!1e1!3m4!1s!2s!6s!15s!7i16384!8i8192"
            
            links.append({
                "address": p["address"],
                "maps_url": maps_url,
                "streetview_url": streetview_url
            })
        return links

    def export_geojson(self, output_path: str = "chronos_audit_points.geojson"):
        features = []
        for p in self.properties:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [p["lon"], p["lat"]]
                },
                "properties": {
                    "name": p["name"],
                    "address": p["address"],
                    "distress_score": p["distress_score"],
                    "google_maps": f"https://www.google.com/maps/search/?api=1&query={p['address'].replace(' ', '+')}"
                }
            }
            features.append(feature)

        geojson = {
            "type": "FeatureCollection",
            "features": features
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(geojson, f, indent=2)

        logger.info(f"Successfully exported GeoJSON points to '{output_path}'")
        return output_path

    def export_html_map(self, output_path: str = "chronos_spatial_map.html"):
        html_content = """<!DOCTYPE html>
<html>
<head>
    <title>CHRONOS OS // Spatial Audit & Google Maps Integration</title>
    <meta charset="utf-8" />
    <style>
        body { font-family: monospace; background: #0F172A; color: #F8FAFC; margin: 0; padding: 20px; }
        h1 { color: #38BDF8; text-align: center; }
        .card { background: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 15px; margin-bottom: 15px; }
        a { color: #38BDF8; text-decoration: none; }
        a:hover { text-decoration: underline; }
    s}
    </style>
</head>
<body>
    <h1>CHRONOS OS // AUDITED SPATIAL POINTS & GOOGLE MAPS LINKS</h1>
"""
        for p in self.properties:
            maps_url = f"https://www.google.com/maps/search/?api=1&query={p['address'].replace(' ', '+')}"
            sv_url = f"https://www.google.com/maps/@{p['lat']},{p['lon']},3a,75y,90t/data=!3m6!1e1!3m4!1s!2s!6s!15s!7i16384!8i8192"
            html_content += f"""
    <div class="card">
        <h3>{p['name']}</h3>
        <p><b>Address:</b> {p['address']}</p>
        <p><b>Coordinates:</b> {p['lat']}, {p['lon']} | <b>Distress Score:</b> {p['distress_score']}</p>
        <p>
            <a href="{maps_url}" target="_blank">🗺️ Open in Google Maps</a> | 
            <a href="{sv_url}" target="_blank">📸 Launch Street View</a>
        </p>
    </div>
"""

        html_content += """
</body>
</html>
"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        logger.info(f"Successfully exported interactive HTML map preview to '{output_path}'")
        return output_path

if __name__ == "__main__":
    print("=" * 76)
    print("      CHRONOS OS // GOOGLE MAPS SPATIAL INTEGRATOR")
    print("=" * 76)
    integrator = GoogleMapsIntegrator()
    geojson_file = integrator.export_geojson()
    html_file = integrator.export_html_map()
    print(f"GeoJSON Export: {geojson_file}")
    print(f"HTML Map View:  {html_file}")
    print("=" * 76)
