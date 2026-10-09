#!/usr/bin/env python3
"""
CHRONOS OS // INDICATOR COMPILER & ENTITY HOLDER MAPPING TOOL
Compiles all canonical data indicators and maps which addresses, parcels, and people
hold or are associated with each indicator across district databases and audit vaults.
"""

import sqlite3
import json
import sys
import argparse
from typing import Dict, List, Any, Optional

DB_FILE = "public_apis_registry.db"

class IndicatorHolderCompiler:
    def __init__(self, db_path: str = DB_FILE):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def get_canonical_indicators(self) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM indicator_master ORDER BY category ASC, name ASC")
        return [dict(r) for r in cursor.fetchall()]

    def get_distress_lead_holders(self) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM distress_leads")
        return [dict(r) for r in cursor.fetchall()]

    def get_audit_dossier_holders(self) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM audit_dossiers")
        return [dict(r) for r in cursor.fetchall()]

    def compile_holders(self, specific_indicator: Optional[str] = None) -> Dict[str, Any]:
        indicators = self.get_canonical_indicators()
        leads = self.get_distress_lead_holders()
        dossiers = self.get_audit_dossier_holders()

        compiled_map = {}

        for ind in indicators:
            name = ind["name"]
            if specific_indicator and specific_indicator.lower() not in name.lower():
                continue

            holders = []

            # 1. Check distress_leads for matches
            for lead in leads:
                match_found = False
                val_desc = ""

                if name == "apn" and lead["apn"]:
                    match_found = True
                    val_desc = f"APN: {lead['apn']}"
                elif name == "fips" and lead["fips"]:
                    match_found = True
                    val_desc = f"FIPS: {lead['fips']}"
                elif name == "assessed_value" and lead["assessed_value"]:
                    match_found = True
                    val_desc = f"Assessed Value: ${lead['assessed_value']:,.2f}"
                elif name == "tax_delinquency" and lead["tax_delinquency"] and lead["tax_delinquency"] > 0:
                    match_found = True
                    val_desc = f"Tax Delinquency: ${lead['tax_delinquency']:,.2f}"
                elif name == "notice_of_default" and lead["default_amount"] and lead["default_amount"] > 0:
                    match_found = True
                    val_desc = f"Default Amount: ${lead['default_amount']:,.2f}"
                elif name == "open_balance" and lead["open_liens_balance"] and lead["open_liens_balance"] > 0:
                    match_found = True
                    val_desc = f"Open Liens Balance: ${lead['open_liens_balance']:,.2f}"
                elif name in lead["distress_triggers"].lower():
                    match_found = True
                    val_desc = f"Trigger Match: {lead['distress_triggers']}"

                if match_found:
                    holders.append({
                        "entity_type": "Property Owner / Lead",
                        "person_or_entity": lead["owner_name"] or "UNKNOWN",
                        "address_or_apn": f"APN {lead['apn']} (State: {lead['state']}, FIPS: {lead['fips']})",
                        "indicator_value": val_desc,
                        "source": "distress_leads"
                    })

            # 2. Check audit_dossiers for matches
            for dossier in dossiers:
                payload_str = dossier["raw_payload"] or ""
                summary_str = dossier["summary"] or ""
                combined_text = (payload_str + " " + summary_str).lower()

                if name in combined_text or name.replace("_", " ") in combined_text:
                    try:
                        payload = json.loads(payload_str) if payload_str.startswith("{") else {}
                    except:
                        payload = {}

                    val_desc = payload.get(name) or summary_str[:120]
                    holders.append({
                        "entity_type": "Audit Dossier Subject",
                        "person_or_entity": payload.get("owner_name") or payload.get("grantee") or "DISCLOSED SUBJECT",
                        "address_or_apn": dossier["input_query"],
                        "indicator_value": str(val_desc),
                        "source": f"audit_dossiers (ID #{dossier['id']})"
                    })

            compiled_map[name] = {
                "category": ind["category"],
                "description": ind["description"],
                "data_type": ind["data_type"],
                "disclosure": ind["disclosure"],
                "holder_count": len(holders),
                "holders": holders
            }

        return compiled_map

    def print_report(self, specific_indicator: Optional[str] = None):
        compiled = self.compile_holders(specific_indicator)
        
        print("=" * 80)
        print("  CHRONOS OS // INDICATOR COMPILATION & ENTITY HOLDER REPORT")
        print("=" * 80)
        
        total_indicators = len(compiled)
        active_indicators = sum(1 for k, v in compiled.items() if v["holder_count"] > 0)
        
        print(f"Total Indicators Scanned: {total_indicators}")
        print(f"Indicators with Linked Holders: {active_indicators}\n")

        for name, data in compiled.items():
            print(f"[{data['category'].upper()}] INDICATOR: `{name}` ({data['data_type']})")
            print(f"  Description: {data['description']}")
            print(f"  Holders Found: {data['holder_count']}")
            if data["holders"]:
                print(f"  Associated Addresses & People:")
                for idx, h in enumerate(data["holders"], 1):
                    print(f"    {idx}. Person/Entity: {h['person_or_entity']}")
                    print(f"       Address/APN:   {h['address_or_apn']}")
                    print(f"       Value/Detail:  {h['indicator_value']}")
                    print(f"       Source:        {h['source']}")
            else:
                print(f"  Associated Addresses & People: None currently indexed in active vaults.")
            print("-" * 80)

    def export_markdown(self, filename: str = "INDICATOR_HOLDERS_REPORT.md"):
        compiled = self.compile_holders()
        md = f"""# Chronos OS // Indicator Compilation & Entity Holder Report
**Generated:** Automated Audit & Compliance Engine  
**Database:** `{DB_FILE}`  

---

## Executive Summary
This report compiles all master indicators and maps which addresses, parcels, and people hold or are associated with each operational indicator across county assessment rolls, distress ledgers, and audit dossiers.

---

"""
        for name, data in compiled.items():
            md += f"## Indicator: `{name}`\n"
            md += f"- **Category:** {data['category']}\n"
            md += f"- **Data Type:** `{data['data_type']}`\n"
            md += f"- **Description:** {data['description']}\n"
            md += f"- **Legal Disclosure:** {data['disclosure']}\n"
            md += f"- **Linked Holders Count:** {data['holder_count']}\n\n"

            if data["holders"]:
                md += "### Associated Addresses & People\n\n"
                md += "| # | Person / Entity | Address / APN | Indicator Value / Detail | Source Dataset |\n"
                md += "|---|---|---|---|---|\n"
                for idx, h in enumerate(data["holders"], 1):
                    md += f"| {idx} | {h['person_or_entity']} | {h['address_or_apn']} | {h['indicator_value']} | {h['source']} |\n"
                md += "\n"
            else:
                md += "*No active entity holders currently indexed for this indicator.*\n\n"

            md += "---\n\n"

        with open(filename, "w") as f:
            f.write(md)
        print(f"[EXPORT SUCCESS] Indicator holders report saved to: {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile indicators and map associated addresses and people.")
    parser.add_argument("--indicator", type=str, help="Filter by specific indicator name")
    parser.add_argument("--export-md", action="store_true", help="Export full compiled holder report to markdown file")
    args = parser.parse_args()

    compiler = IndicatorHolderCompiler()
    compiler.print_report(args.indicator)
    if args.export_md:
        compiler.export_markdown()
