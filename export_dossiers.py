#!/usr/bin/env python3
"""
CHRONOS OS // AUDIT VAULT EXPORTER
Extracts all database dossiers into standardized JSON and CSV files.
"""

import csv
import json
import sqlite3
from datetime import datetime

DB_FILE = "public_apis_registry.db"

def export_all():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, input_query, input_type, timestamp, summary FROM audit_dossiers ORDER BY id ASC")
    rows = c.fetchall()
    conn.close()

    if not rows:
        print("[!] No records found in audit_dossiers table.")
        return

    data = [
        {
            "id": r[0],
            "input_query": r[1],
            "input_type": r[2],
            "timestamp": r[3],
            "summary": r[4]
        }
        for r in rows
    ]

    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_filename = f"vault_export_{timestamp_str}.json"
    csv_filename = f"vault_export_{timestamp_str}.csv"

    # Write JSON
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # Write CSV
    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Input Query", "Input Type", "Timestamp", "Summary"])
        for r in rows:
            writer.writerow(r)

    print("=" * 72)
    print("        CHRONOS OS // VAULT EXPORT COMPLETED")
    print("=" * 72)
    print(f"Total Records Exported: {len(data)}")
    print(f"JSON Output File:      {json_filename}")
    print(f"CSV Output File:       {csv_filename}")
    print("=" * 72)

if __name__ == "__main__":
    export_all()
