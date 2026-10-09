#!/usr/bin/env python3
"""
CHRONOS OS // LOCAL VAULT QUERY TOOL
Inspects audit dossiers saved in public_apis_registry.db.
"""

import sys
import sqlite3

def query_vault(search_term: str = ""):
    conn = sqlite3.connect("public_apis_registry.db")
    cursor = conn.cursor()
    
    if search_term:
        query = "SELECT id, input_query, input_type, timestamp, summary FROM audit_dossiers WHERE input_query LIKE ? ORDER BY id DESC"
        cursor.execute(query, (f"%{search_term}%",))
    else:
        query = "SELECT id, input_query, input_type, timestamp, summary FROM audit_dossiers ORDER BY id DESC LIMIT 10"
        cursor.execute(query)
        
    rows = cursor.fetchall()
    conn.close()

    print("=" * 76)
    print("            CHRONOS OS // LOCAL AUDIT VAULT RECORDS")
    print("=" * 76)
    if not rows:
        print("No matching audit records found.")
    else:
        for r in rows:
            print(f"ID:        {r[0]}")
            print(f"TARGET:    {r[1]} ({r[2]})")
            print(f"LOGGED:    {r[3]}")
            print(f"SUMMARY:   {r[4]}")
            print("-" * 76)

if __name__ == "__main__":
    term = sys.argv[1] if len(sys.argv) > 1 else ""
    query_vault(term)
