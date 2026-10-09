#!/usr/bin/env python3
"""
API Registry & Indicator Engine
Ingests, indexes, and surfaces public record, municipal, real estate, and open APIs.
Zero external dependencies (uses Python standard library: sqlite3, json, argparse).
"""

import sqlite3
import json
import re
import argparse
from typing import List, Dict, Any

DB_FILE = "public_apis_registry.db"

SEEDED_APIS: List[Dict[str, Any]] = [
    {
        "provider": "PropMix",
        "domain": "pubrec.propmix.io",
        "category": "Real Estate / Municipal",
        "auth_type": "API Key / OAuth2",
        "doc_url": "https://pubrec.propmix.io",
        "endpoints": [
            {
                "name": "Property Assessment & Tax",
                "path": "/v1/property/assessment",
                "method": "GET",
                "params": ["apn", "fips", "address", "state", "county"],
                "description": "Returns property tax records, assessed values, parcel boundary IDs, and structural specs.",
                "indicators": ["apn", "assessed_value", "tax_delinquency", "lot_size", "zoning_code", "fips"]
            },
            {
                "name": "Deed & Ownership Transfer History",
                "path": "/v1/property/deeds",
                "method": "GET",
                "params": ["apn", "address", "start_date"],
                "description": "Historical chain of title, grantor/grantee records, and transaction sales prices.",
                "indicators": ["grantor", "grantee", "sale_price", "recording_date", "document_type"]
            },
            {
                "name": "Mortgage & Voluntary Liens",
                "path": "/v1/property/liens",
                "method": "GET",
                "params": ["apn", "fips"],
                "description": "Mortgage records, open liens, lender names, and loan amount history.",
                "indicators": ["lender_name", "loan_amount", "lien_type", "open_balance", "maturity_date"]
            }
        ]
    },
    {
        "provider": "Tracers",
        "domain": "tracers.com",
        "category": "Skip Tracing / Public Records",
        "auth_type": "Bearer Token / HMAC",
        "doc_url": "https://www.tracers.com",
        "endpoints": [
            {
                "name": "Comprehensive Person Search",
                "path": "/api/v2/search/person",
                "method": "POST",
                "params": ["name", "ssn_last4", "dob", "address", "phone"],
                "description": "Locates current address, phone numbers, deceased indicators, and immediate associates.",
                "indicators": ["ssn_verified", "phone_carrier", "alias_names", "relatives", "deceased_flag", "dob"]
            },
            {
                "name": "Judgments, Liens & Bankruptcies",
                "path": "/api/v2/records/liens-bankruptcies",
                "method": "POST",
                "params": ["entity_name", "tax_id", "state"],
                "description": "Searches state and federal courts for judgments, tax liens, and bankruptcy filings.",
                "indicators": ["bankruptcy_chapter", "lien_filing_date", "court_docket", "judgment_amount"]
            },
            {
                "name": "Asset & Business Affiliation",
                "path": "/api/v2/records/assets",
                "method": "POST",
                "params": ["individual_id", "business_name"],
                "description": "Surfaces corporate filings, LLC registrations, aircraft, and commercial deeds.",
                "indicators": ["corporate_status", "registered_agent", "ein", "fleet_vehicles", "property_holdings"]
            }
        ]
    },
    {
        "provider": "Record Information Services",
        "domain": "public-record.com",
        "category": "County Records / Foreclosures",
        "auth_type": "API Key",
        "doc_url": "https://public-record.com",
        "endpoints": [
            {
                "name": "County Foreclosure & Pre-Foreclosure Feed",
                "path": "/feed/foreclosures",
                "method": "GET",
                "params": ["county_id", "state", "filing_date_min"],
                "description": "County clerk filings for Lis Pendens, Notice of Default, and Auction dates.",
                "indicators": ["lis_pendens", "notice_of_default", "auction_date", "default_amount", "case_number"]
            },
            {
                "name": "New Business Licenses",
                "path": "/feed/business-filings",
                "method": "GET",
                "params": ["county_id", "jurisdiction"],
                "description": "Newly registered DBAs, LLC incorporations, and municipal trade licenses.",
                "indicators": ["dba_name", "owner_name", "filing_date", "naics_code"]
            }
        ]
    },
    {
        "provider": "Data.gov / api.data.gov",
        "domain": "api.data.gov",
        "category": "Federal Open Data Gateway",
        "auth_type": "x-api-key",
        "doc_url": "https://api.data.gov",
        "endpoints": [
            {
                "name": "Federal Dataset Metadata Search",
                "path": "/api/3/action/package_search",
                "method": "GET",
                "params": ["q", "facet.field", "rows"],
                "description": "Federated discovery endpoint indexing federal agency open datasets.",
                "indicators": ["ckan_package_id", "geospatial_bounds", "agency_name", "update_frequency", "download_url"]
            }
        ]
    },
    {
        "provider": "Zillow Group",
        "domain": "zillowgroup.com",
        "category": "Real Estate / Valuation",
        "auth_type": "API Key / OAuth2",
        "doc_url": "https://www.zillowgroup.com",
        "endpoints": [
            {
                "name": "Valuation & Rent Estimates (Zestimate)",
                "path": "/webservice/GetZestimate.htm",
                "method": "GET",
                "params": ["zpid", "address", "citystatezip"],
                "description": "Automated valuation models (AVM), 30-day valuation ranges, and rental yield index.",
                "indicators": ["zestimate_value", "valuation_range_high", "valuation_range_low", "rent_zestimate"]
            }
        ]
    },
    {
        "provider": "FOIA.gov",
        "domain": "foia.gov",
        "category": "Government Transparency",
        "auth_type": "None / Open",
        "doc_url": "https://www.foia.gov",
        "endpoints": [
            {
                "name": "Agency Annual FOIA Metrics",
                "path": "/api/agency-metrics",
                "method": "GET",
                "params": ["agency_id", "fiscal_year"],
                "description": "Agency processing backlogs, request closure rates, and average response times.",
                "indicators": ["backlog_count", "median_processing_days", "denial_exemptions", "fee_waiver_rate"]
            }
        ]
    },
    {
        "provider": "Library of Congress",
        "domain": "loc.gov",
        "category": "Archives & Legislation",
        "auth_type": "None / API Key",
        "doc_url": "https://www.loc.gov",
        "endpoints": [
            {
                "name": "Historical Collections & Newspapers",
                "path": "/chronicling-america/search/pages/results/",
                "method": "GET",
                "params": ["andtext", "state", "dateFilterType"],
                "description": "Scanned public notice historical newspapers and municipal archives.",
                "indicators": ["ocr_text", "publication_date", "page_sequence", "county_coverage"]
            }
        ]
    }
]

class APIRegistryEngine:
    def __init__(self, db_path: str = DB_FILE):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS providers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            domain TEXT NOT NULL,
            category TEXT NOT NULL,
            auth_type TEXT NOT NULL,
            doc_url TEXT NOT NULL
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS endpoints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            provider_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            path TEXT NOT NULL,
            method TEXT NOT NULL,
            params TEXT NOT NULL,
            description TEXT NOT NULL,
            FOREIGN KEY (provider_id) REFERENCES providers (id) ON DELETE CASCADE
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS indicators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            endpoint_id INTEGER NOT NULL,
            indicator_key TEXT NOT NULL,
            FOREIGN KEY (endpoint_id) REFERENCES endpoints (id) ON DELETE CASCADE
        );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_indicators_key ON indicators(indicator_key);")
        cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS fts_api_search USING fts5(
            provider_name,
            endpoint_name,
            path,
            description,
            params,
            indicators,
            tokenize = 'porter unicode61'
        );
        """)
        self.conn.commit()

    def seed_or_update(self, data: List[Dict[str, Any]]):
        cursor = self.conn.cursor()
        for p in data:
            cursor.execute("""
                INSERT INTO providers (name, domain, category, auth_type, doc_url)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    domain=excluded.domain,
                    category=excluded.category,
                    auth_type=excluded.auth_type,
                    doc_url=excluded.doc_url
            """, (p["provider"], p["domain"], p["category"], p["auth_type"], p["doc_url"]))

            provider_id = cursor.execute("SELECT id FROM providers WHERE name = ?", (p["provider"],)).fetchone()[0]

            for ep in p["endpoints"]:
                existing = cursor.execute(
                    "SELECT id FROM endpoints WHERE provider_id = ? AND path = ? AND method = ?",
                    (provider_id, ep["path"], ep["method"])
                ).fetchone()

                params_json = json.dumps(ep.get("params", []))

                if existing:
                    endpoint_id = existing[0]
                    cursor.execute("""
                        UPDATE endpoints SET name=?, params=?, description=? WHERE id=?
                    """, (ep["name"], params_json, ep["description"], endpoint_id))
                    cursor.execute("DELETE FROM indicators WHERE endpoint_id = ?", (endpoint_id,))
                else:
                    cursor.execute("""
                        INSERT INTO endpoints (provider_id, name, path, method, params, description)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (provider_id, ep["name"], ep["path"], ep["method"], params_json, ep["description"]))
                    endpoint_id = cursor.lastrowid

                indicator_set = set(k.lower().strip() for k in ep.get("indicators", []))
                for ind in indicator_set:
                    cursor.execute("INSERT INTO indicators (endpoint_id, indicator_key) VALUES (?, ?)", (endpoint_id, ind))

                cursor.execute("DELETE FROM fts_api_search WHERE rowid = ?", (endpoint_id,))
                cursor.execute("""
                    INSERT INTO fts_api_search (rowid, provider_name, endpoint_name, path, description, params, indicators)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    endpoint_id,
                    p["provider"],
                    ep["name"],
                    ep["path"],
                    ep["description"],
                    " ".join(ep.get("params", [])),
                    " ".join(indicator_set)
                ))
        self.conn.commit()

    def find_by_indicator(self, indicator: str) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        query = """
            SELECT
                p.name AS provider,
                p.category,
                p.auth_type,
                e.name AS endpoint,
                e.method,
                e.path,
                e.params,
                e.description,
                GROUP_CONCAT(i.indicator_key, ', ') as all_indicators
            FROM indicators i
            JOIN endpoints e ON i.endpoint_id = e.id
            JOIN providers p ON e.provider_id = p.id
            WHERE i.indicator_key LIKE ?
            GROUP BY e.id
            ORDER BY p.name ASC
        """
        cursor.execute(query, (f"%{indicator.lower()}%",))
        return [dict(row) for row in cursor.fetchall()]

    def search_full_text(self, term: str) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        query = """
            SELECT
                fts.provider_name,
                fts.endpoint_name,
                fts.path,
                fts.description,
                fts.params,
                fts.indicators,
                p.auth_type,
                p.doc_url
            FROM fts_api_search fts
            JOIN endpoints e ON fts.rowid = e.id
            JOIN providers p ON e.provider_id = p.id
            WHERE fts_api_search MATCH ?
            ORDER BY rank
        """
        sanitized = re.sub(r'[^a-zA-Z0-9_*]', ' ', term).strip()
        if not sanitized.endswith("*"):
            sanitized += "*"
        cursor.execute(query, (sanitized,))
        return [dict(row) for row in cursor.fetchall()]

    def list_all_indicators(self) -> Dict[str, int]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT indicator_key, COUNT(endpoint_id) as coverage_count
            FROM indicators
            GROUP BY indicator_key
            ORDER BY coverage_count DESC, indicator_key ASC
        """)
        return {row["indicator_key"]: row["coverage_count"] for row in cursor.fetchall()}

    def dump_schema_summary(self):
        cursor = self.conn.cursor()
        p_count = cursor.execute("SELECT COUNT(*) FROM providers").fetchone()[0]
        e_count = cursor.execute("SELECT COUNT(*) FROM endpoints").fetchone()[0]
        i_count = cursor.execute("SELECT COUNT(DISTINCT indicator_key) FROM indicators").fetchone()[0]
        print(f"\n[REGISTRY METRICS] {p_count} Providers | {e_count} Endpoints | {i_count} Unique Data Indicators\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query and index public record, parcel, and open APIs.")
    parser.add_argument("--init", action="store_true", help="Initialize and populate database with source APIs")
    parser.add_argument("--indicator", type=str, help="Search APIs providing a specific indicator (e.g. 'apn', 'lien')")
    parser.add_argument("--search", type=str, help="Full-text search across documentation, routes, and schemas")
    parser.add_argument("--indicators", action="store_true", help="List all registered data indicators and counts")

    args = parser.parse_args()
    engine = APIRegistryEngine()

    if args.init or not any(vars(args).values()):
        engine.seed_or_update(SEEDED_APIS)
        engine.dump_schema_summary()

    if args.indicators:
        indicators = engine.list_all_indicators()
        print("Indexed Indicators & Endpoint Frequency:")
        for ind, count in indicators.items():
            print(f"  • {ind.ljust(25)} -> {count} endpoint(s)")

    if args.indicator:
        results = engine.find_by_indicator(args.indicator)
        print(f"\n--- Indicator Query Results: '{args.indicator}' ({len(results)} found) ---")
        for r in results:
            print(f"\n[{r['provider']} - {r['category']}]")
            print(f"  Endpoint:    {r['method']} {r['path']} ({r['endpoint']})")
            print(f"  Auth:        {r['auth_type']}")
            print(f"  Parameters:  {r['params']}")
            print(f"  Indicators:  {r['all_indicators']}")
            print(f"  Description: {r['description']}")

    if args.search:
        results = engine.search_full_text(args.search)
        print(f"\n--- Full-Text Query Results: '{args.search}' ({len(results)} found) ---")
        for r in results:
            print(f"\n[{r['provider_name']}] {r['endpoint_name']}")
            print(f"  Route:       {r['path']}")
            print(f"  Auth:        {r['auth_type']}")
            print(f"  Doc:         {r['doc_url']}")
            print(f"  Params:      {r['params']}")
            print(f"  Indicators:  {r['indicators']}")
            print(f"  Description: {r['description']}")
