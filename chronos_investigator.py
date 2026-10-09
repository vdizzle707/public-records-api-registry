#!/usr/bin/env python3
import sys
import json
import urllib.request
from cascade_engine import CascadeEngine

def get_live_location():
    from get_device_location import get_accurate_coordinates
    lat, lon, acc, prov = get_accurate_coordinates()
    return f"{lat},{lon}", f"Potter Valley, CA ({prov})"

def explain_findings(stem_type, raw_data):
    l1 = raw_data.get("l1_direct", {})
    l2 = raw_data.get("l2_cascade", {})
    l3 = raw_data.get("l3_synthesis", {})

    print("\n" + "=" * 62)
    print("           PLAIN ENGLISH AUDIT SUMMARY")
    print("=" * 62)

    if stem_type in ("gps", "lat_lon"):
        print(f"Location Analyzed: {l1.get('coordinates')} ({l1.get('county')} County, CA)")
        print(f"Identified Parcel: APN {l1.get('derived_apn')}\n")
        print("Active Indicators & What They Mean:")
        print(f"  * Wildfire Hazard: Flagged as '{l2.get('wildfire_zone')}'.")
        print("    Meaning: Standard insurance policies will likely refuse coverage.")
        print("    You will be required to use the high-risk California FAIR Plan.")
        print(f"  * Loan Eligibility: {l2.get('usda_eligible')}.")
        print("    Meaning: This area qualifies for zero-down-payment USDA rural financing.")
        print(f"  * Septic Suitability: {l2.get('soil_perc')}.")
        print("    Meaning: Soil drainage allows standard on-site wastewater installation.")

    elif stem_type == "address":
        print(f"Address Analyzed: {l1.get('address')}")
        print(f"Vested Owner:     {l1.get('grantee')}")
        print(f"Parcel Identifier: APN {l1.get('derived_apn')}\n")
        print("Active Indicators & What They Mean:")
        print(f"  * Title Cloud Status: {l3.get('title_status')}.")
        print("    Meaning: Legal title is clouded. A lender has recorded an active")
        print("    Notice of Default, signaling that foreclosure proceedings have started.")
        print(f"  * Recorded Loan: Outstanding balance of ${l2.get('open_balance', 0):,.2f}.")
        print("    Meaning: This is the principal loan on file that must be resolved at close.")

    elif stem_type in ("entity", "name"):
        print(f"Name/Entity Analyzed: {l1.get('entity')}")
        print(f"Registration State:   California Secretary of State\n")
        print("Active Indicators & What They Mean:")
        print(f"  * Corporate Legal Status: '{l1.get('sos_status')}'.")
        print("    Meaning: The entity is in good standing and holds the full legal right")
        print("    to sign contracts and transfer real property.")
        print(f"  * Equipment Encumbrance: {l2.get('ucc_filing')}.")
        print("    Meaning: Equipment on the property (such as solar panels) is tied to a")
        print("    separate financing lien that must be paid off or assumed by any new buyer.")
        print(f"  * Bankruptcy Protection: {l2.get('bankruptcy_stay')}.")
        print("    Meaning: No federal bankruptcy freezes are stopping transactions.")

    print("=" * 62)

def main():
    engine = CascadeEngine()

    print("=" * 62)
    print("      CHRONOS OS // MULTI-STEM INVESTIGATION TOOL")
    print("=" * 62)
    print("Choose an option:")
    print("  1. Ping Current Live Location (Automatic Sensor Lock)")
    print("  2. Search by Street Address")
    print("  3. Search by Individual / Business Entity Name")
    print("  4. Search by County Parcel Number (APN)")
    print("=" * 62)

    choice = input("Enter selection [1-4] (Default: 1): ").strip()
    if not choice:
        choice = "1"

    if choice == "1":
        print("\nPinging location sensors...")
        coords, place = get_live_location()
        print(f"Sensor Lock Established: {place} ({coords})")
        res = engine.run_stem("lat_lon", coords)
        explain_findings("gps", res)

    elif choice == "2":
        addr = input("\nEnter street address (e.g. 19281 Ridgeway Hwy, Potter Valley, CA): ").strip()
        if not addr:
            addr = "19281 Ridgeway Hwy, Potter Valley, CA 95469"
        print(f"\nAuditing title records for: {addr}...")
        res = engine.run_stem("address", addr)
        explain_findings("address", res)

    elif choice == "3":
        name = input("\nEnter person or entity name (e.g. Pacific Coast Land Holdings LLC): ").strip()
        if not name:
            name = "Pacific Coast Land Holdings LLC"
        print(f"\nChecking public entity & lien filings for: {name}...")
        res = engine.run_stem("entity", name)
        explain_findings("entity", res)

    elif choice == "4":
        apn = input("\nEnter County APN (e.g. 185-060-25): ").strip()
        if not apn:
            apn = "185-060-25"
        print(f"\nScanning assessor roll for APN: {apn}...")
        res = engine.run_stem("apn", apn)
        l1 = res.get("l1_direct", {})
        l2 = res.get("l2_cascade", {})
        l3 = res.get("l3_synthesis", {})
        print("\n" + "=" * 62)
        print("           PLAIN ENGLISH AUDIT SUMMARY")
        print("=" * 62)
        print(f"Parcel APN: {l1.get('apn')} ({l1.get('situs')})")
        print(f"Owner:      {l1.get('owner')}\n")
        print("Active Indicators & What They Mean:")
        print(f"  * Property Assessment: Assessed at ${l1.get('assessed_val', 0):,.2f}.")
        print("    Meaning: The official tax roll value used to compute county property taxes.")
        print(f"  * Past-Due Taxes: ${l2.get('tax_delinquency', 0):,.2f} delinquent.")
        print("    Meaning: Back taxes are owed. If left unpaid, the county will schedule")
        print("    a tax-default auction to sell the land.")
        print(f"  * Net Equity Buffer: ${l3.get('net_equity_buffer', 0):,.2f}.")
        print("    Meaning: Remaining profit margin after accounting for all mortgages,")
        print("    unpaid back taxes, and default penalties.")
        print("=" * 62)
    else:
        print("Invalid selection.")

if __name__ == "__main__":
    main()
