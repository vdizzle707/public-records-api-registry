#!/usr/bin/env python3
"""
Conversational Natural Language Interface for Public Record & Municipal APIs.
Translates unstructured operator intent into ranked API routes, parameter mappings,
and indicator chains without requiring external AI APIs or remote dependencies.
"""

import re
import sys
import json
import sqlite3
from typing import List, Dict, Any, Tuple

DB_FILE = "public_apis_registry.db"

# Domain Intent Synonyms mapped to Registry Indicators
INTENT_INDICATOR_MAP = {
    "parcel": ["apn", "lot_size", "zoning_code", "fips"],
    "tax": ["tax_delinquency", "assessed_value", "apn"],
    "lien": ["lien_type", "open_balance", "judgment_amount", "lien_filing_date"],
    "foreclosure": ["lis_pendens", "notice_of_default", "auction_date", "default_amount", "case_number"],
    "owner": ["grantor", "grantee", "owner_name", "corporate_status", "registered_agent"],
    "deed": ["grantor", "grantee", "sale_price", "recording_date", "document_type"],
    "debt": ["judgment_amount", "bankruptcy_chapter", "open_balance", "loan_amount"],
    "person": ["ssn_verified", "phone_carrier", "alias_names", "relatives", "deceased_flag", "dob"],
    "business": ["corporate_status", "registered_agent", "ein", "dba_name", "naics_code"],
    "value": ["zestimate_value", "assessed_value", "valuation_range_high", "sale_price"]
}

class ConversationalEngine:
    def __init__(self, db_path: str = DB_FILE):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def parse_query(self, user_text: str) -> Dict[str, Any]:
        """Extracts parameters, indicators, and matched endpoints from raw conversational input."""
        cleaned = user_text.lower()
        extracted_params = {}

        # 1. Parameter Pattern Recognition
        apn_match = re.search(r'\b\d{3}[-\s]?\d{3}[-\s]?\d{2,3}\b', user_text)
        if apn_match:
            extracted_params["apn"] = apn_match.group(0).replace(" ", "-")

        fips_match = re.search(r'\bfips\s*[:=]?\s*(\d{5})\b', cleaned)
        if fips_match:
            extracted_params["fips"] = fips_match.group(1)

        state_match = re.search(r'\b(al|ak|az|ar|ca|co|ct|de|fl|ga|hi|id|il|in|ia|ks|ky|la|me|md|ma|mi|mn|ms|mo|mt|ne|nv|nh|nj|nm|ny|nc|nd|oh|ok|or|pa|ri|sc|sd|tn|tx|ut|vt|va|wa|wv|wi|wy)\b', cleaned)
        if state_match:
            extracted_params["state"] = state_match.group(1).upper()

        # 2. Extract Matching Target Indicators
        matched_indicators = set()
        for keyword, indicators in INTENT_INDICATOR_MAP.items():
            if re.search(r'\b' + re.escape(keyword) + r'\b', cleaned):
                matched_indicators.update(indicators)

        # 3. Query Registry Database for Matching Routes
        matched_routes = []
        if matched_indicators:
            placeholders = ",".join(["?"] * len(matched_indicators))
            query = f"""
                SELECT 
                    p.name AS provider,
                    p.auth_type,
                    e.name AS endpoint,
                    e.method,
                    e.path,
                    e.params,
                    e.description,
                    GROUP_CONCAT(DISTINCT i.indicator_key) AS matching_indicators,
                    COUNT(DISTINCT i.indicator_key) AS match_score
                FROM endpoints e
                JOIN providers p ON e.provider_id = p.id
                JOIN indicators i ON e.id = i.endpoint_id
                WHERE i.indicator_key IN ({placeholders})
                GROUP BY e.id
                ORDER BY match_score DESC
            """
            cursor = self.conn.cursor()
            cursor.execute(query, list(matched_indicators))
            for row in cursor.fetchall():
                matched_routes.append({
                    "provider": row["provider"],
                    "endpoint": row["endpoint"],
                    "method": row["method"],
                    "path": row["path"],
                    "required_params": json.loads(row["params"]),
                    "matched_indicators": row["matching_indicators"].split(","),
                    "score": row["match_score"]
                })
        else:
            # Fallback to FTS5 search if no rule-based indicators fired
            cursor = self.conn.cursor()
            sanitized = re.sub(r'[^a-zA-Z0-9]', ' ', cleaned).strip()
            if sanitized:
                fts_query = """
                    SELECT 
                        fts.provider_name AS provider,
                        fts.endpoint_name AS endpoint,
                        fts.path,
                        e.method,
                        e.params,
                        fts.indicators,
                        rank
                    FROM fts_api_search fts
                    JOIN endpoints e ON fts.rowid = e.id
                    WHERE fts_api_search MATCH ?
                    ORDER BY rank LIMIT 3
                """
                cursor.execute(fts_query, (sanitized + "*",))
                for row in cursor.fetchall():
                    matched_routes.append({
                        "provider": row["provider"],
                        "endpoint": row["endpoint"],
                        "method": row["method"],
                        "path": row["path"],
                        "required_params": json.loads(row["params"]),
                        "matched_indicators": row["indicators"].split(),
                        "score": 1
                    })

        return {
            "raw_input": user_text,
            "detected_params": extracted_params,
            "target_indicators": list(matched_indicators),
            "suggested_routes": matched_routes
        }

    def chat_loop(self):
        """Interactive REPL session."""
        print("─────────────────────────────────────────────────────────────")
        print("  Conversational API Dispatcher (Type 'exit' to quit)        ")
        print("─────────────────────────────────────────────────────────────")
        while True:
            try:
                user_msg = input("\n[OPERATOR] > ").strip()
                if not user_msg:
                    continue
                if user_msg.lower() in ("exit", "quit", "q"):
                    print("Terminating session.")
                    break

                analysis = self.parse_query(user_msg)
                routes = analysis["suggested_routes"]

                print(f"\n[ENGINE STATUS] Extracted Parameters: {analysis['detected_params'] or 'None detected'}")
                print(f"[ENGINE STATUS] Target Indicators:    {', '.join(analysis['target_indicators']) or 'General Search'}")

                if not routes:
                    print("[RESULT] No direct API endpoints matched your inquiry. Try specifying asset, owner, tax, or lien terms.")
                    continue

                print(f"\n[RECOMMENDED EXECUTION PLAN ({len(routes)} Candidate Endpoints)]:")
                for idx, r in enumerate(routes[:3], start=1):
                    print(f"  {idx}. [{r['provider']}] {r['endpoint']}")
                    print(f"     Route:      {r['method']} {r['path']}")
                    print(f"     Parameters: {r['required_params']}")
                    print(f"     Indicators: {', '.join(r['matched_indicators'])}")

            except (KeyboardInterrupt, EOFError):
                print("\nSession aborted.")
                break

if __name__ == "__main__":
    engine = ConversationalEngine()
    if len(sys.argv) > 1:
        # One-off evaluation
        query = " ".join(sys.argv[1:])
        result = engine.parse_query(query)
        print(json.dumps(result, indent=2))
    else:
        # Interactive mode
        engine.chat_loop()
