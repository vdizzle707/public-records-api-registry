#!/usr/bin/env python3
import sqlite3

MAPPINGS = [
    # Spatial Centroid (lat, lon)
    ("lat_lon", "flood_zone", "FEMA NFIP Maps", "Spatial Intersect"),
    ("lat_lon", "wildfire_hazard_severity", "CAL FIRE VHFHSZ", "Spatial Intersect"),
    ("lat_lon", "earthquake_fault_zone", "USGS / CGS Seismic", "Spatial Intersect"),
    ("lat_lon", "usda_rural_eligible_flag", "USDA Rural Dev GIS", "Spatial Polygon"),
    ("lat_lon", "hud_opportunity_zone_flag", "CDFIFund QOZ Layers", "Census Tract Intersect"),
    ("lat_lon", "coastal_zone_jurisdiction_flag", "Coastal Commission GIS", "Boundary Check"),
    ("lat_lon", "gis_geometry", "County GIS Parcel Layer", "Spatial Centroid Join"),
    ("lat_lon", "soil_percolation_rate_mpi", "USDA NRCS Web Soil", "Geotechnical Point"),

    # Parcel Key (apn)
    ("apn", "assessed_value", "County Tax Assessor Roll", "Exact Match"),
    ("apn", "land_value", "County Tax Assessor Roll", "Exact Match"),
    ("apn", "improvement_value", "County Tax Assessor Roll", "Exact Match"),
    ("apn", "lot_size", "Assessor Plat Map", "Exact Match"),
    ("apn", "tax_delinquency", "County Tax Collector", "Ledger Balance Lookup"),
    ("apn", "tax_delinquent_year", "County Tax Collector", "Default Roll Check"),
    ("apn", "zoning_code", "Municipal Planning GIS", "Attribute Table Join"),
    ("apn", "williamson_act_contract_flag", "County Ag Commissioner", "Contract Index"),

    # Jurisdiction (fips)
    ("fips", "recording_jurisdiction", "State Statutes", "Prefix Code Routing"),
    ("fips", "statutory_redemption_period", "County Tax Collector", "Jurisdiction Rules"),
    ("fips", "case_number", "Superior Court Docket", "Court Routing Key"),
    ("fips", "mello_roos_annual_tax", "County Auditor-Controller", "Special District Tax"),

    # Situs Identifier (address)
    ("address", "grantee", "County Recorder Index", "Deed Records Match"),
    ("address", "grantor", "County Recorder Index", "Grantor Index Search"),
    ("address", "sale_price", "Recorded Deed Stamps", "Documentary Tax Decode"),
    ("address", "recording_date", "County Recorder Roll", "Instrument Timestamp"),
    ("address", "lis_pendens", "County Court / Recorder", "Notice of Action Index"),
    ("address", "notice_of_default", "Trustee / Recorder Filings", "NOD Registry"),
    ("address", "open_balance", "Recorded Deeds of Trust", "Encumbrance Schedule"),

    # Network / IP Telemetry (query_isp)
    ("query_isp", "broadband_carrier_availability", "FCC National Map", "Carrier Match"),
    ("query_isp", "grid_interconnection_status", "Utility Service Records", "Node Tracing")
]

conn = sqlite3.connect("public_apis_registry.db")
c = conn.cursor()
for param, ind, source, res_type in MAPPINGS:
    c.execute("""
        INSERT OR IGNORE INTO input_indicator_matrix (input_param, indicator_name, data_source, resolution_type)
        VALUES (?, ?, ?, ?)
    """, (param, ind, source, res_type))

conn.commit()
count = c.execute("SELECT COUNT(*) FROM input_indicator_matrix").fetchone()[0]
conn.close()
print(f"[SEEDED] {count} input-to-indicator matrix entries registered.")
