#!/usr/bin/env python3
import sqlite3
import re
from typing import Dict, Any, List, Optional, Tuple

DB_FILE = "public_apis_registry.db"

class IndicatorLibrary:
    def __init__(self, db_path: str = DB_FILE):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()
        self._bootstrap_core_indicators()

    def _init_schema(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS indicator_master (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            disclosure TEXT NOT NULL,
            data_type TEXT NOT NULL,
            aliases TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_indicator_master_name ON indicator_master(name);")
        self.conn.commit()

    def _normalize(self, text: str) -> str:
        return re.sub(r'[^a-z0-9]', '', text.lower().strip())

    def find_duplicate(self, candidate_name: str) -> Optional[Dict[str, Any]]:
        norm_candidate = self._normalize(candidate_name)
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM indicator_master WHERE LOWER(name) = LOWER(?)", (candidate_name,))
        row = cursor.fetchone()
        if row:
            return dict(row)

        cursor.execute("SELECT * FROM indicator_master")
        all_rows = cursor.fetchall()
        for r in all_rows:
            aliases = [self._normalize(a) for a in r["aliases"].split(",") if a.strip()]
            if norm_candidate in aliases:
                return dict(r)

        for r in all_rows:
            norm_existing = self._normalize(r["name"])
            if norm_candidate == norm_existing:
                return dict(r)
            if len(norm_candidate) > 4 and len(norm_existing) > 4:
                if norm_candidate[:5] == norm_existing[:5]:
                    if norm_candidate in norm_existing or norm_existing in norm_candidate:
                        return dict(r)
        return None

    def register_indicator(self, name: str, category: str, description: str, disclosure: str, data_type: str, aliases: List[str] = None) -> Tuple[bool, Dict[str, Any], str]:
        clean_name = name.lower().strip().replace(" ", "_")
        existing = self.find_duplicate(clean_name)
        if existing:
            return False, existing, f"DUPLICATE REJECTED: '{clean_name}' matches canonical indicator '{existing['name']}'."

        aliases_str = ",".join([a.strip().lower() for a in (aliases or [])])
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO indicator_master (name, category, description, disclosure, data_type, aliases)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (clean_name, category, description, disclosure, data_type, aliases_str))
        self.conn.commit()

        cursor.execute("SELECT * FROM indicator_master WHERE name = ?", (clean_name,))
        return True, dict(cursor.fetchone()), f"REGISTERED: '{clean_name}' successfully indexed."

    def get_indicator(self, name: str) -> Optional[Dict[str, Any]]:
        return self.find_duplicate(name)

    def list_all(self) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM indicator_master ORDER BY category ASC, name ASC")
        return [dict(r) for r in cursor.fetchall()]

    def _bootstrap_core_indicators(self):
        seeds = [
            ("apn", "Parcel", "Assessor Parcel Number identifying county tax unit.", "Must verify against county FIPS.", "String", ["parcel_id", "pin", "tax_id"]),
            ("assessed_value", "Valuation", "Statutory ad-valorem tax roll valuation.", "Reflects statutory caps, not FMV.", "Currency", ["tax_value", "assessment"]),
            ("tax_delinquency", "Distress", "Unpaid property tax balance past grace period.", "Triggers statutory tax sale if uncured.", "Currency", ["delinquent_taxes", "back_taxes"]),
            ("lis_pendens", "Distress", "Recorded public notice of pending judicial litigation.", "Constructive legal notice of foreclosure.", "Docket", ["suit_pending", "notice_of_action"]),
            ("notice_of_default", "Distress", "Public notice filed by trustee declaring default.", "Triggers statutory 90-day cure window.", "Document", ["nod", "default_notice"]),
            ("auction_date", "Distress", "Scheduled trustee or tax default auction date.", "Subject to bankruptcy automatic stays.", "Timestamp", ["sale_date", "foreclosure_date"]),
            ("grantee", "Title", "Transferee or buyer acquiring title on deed.", "Must verify against county recorder index.", "String", ["buyer", "new_owner"]),
            ("open_balance", "Debt", "Principal balance on mortgage or judgment liens.", "Payoff demand statement required for per-diem balance.", "Currency", ["loan_balance", "lien_balance"])
        ]
        cursor = self.conn.cursor()
        for name, cat, desc, disc, dtype, aliases in seeds:
            cursor.execute("SELECT id FROM indicator_master WHERE name = ?", (name,))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO indicator_master (name, category, description, disclosure, data_type, aliases)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (name, cat, desc, disc, dtype, ",".join(aliases)))
        self.conn.commit()

if __name__ == "__main__":
    lib = IndicatorLibrary()
    print(f"[MASTER REPOSITORY INITIALIZED] {len(lib.list_all())} canonical indicators indexed.")
