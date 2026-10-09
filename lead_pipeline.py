#!/usr/bin/env python3
"""
CHRONOS OS // AUTOMATED DISTRESS LEAD & EQUITY AUDIT PIPELINE
Ingests parcel records, cross-references encumbrance indicators against market valuation,
computes net equity buffers, and exports qualified acquisition leads.
"""

import sqlite3
import json
import csv
import sys
from typing import List, Dict, Any, Optional

from indicator_master import IndicatorLibrary
from router import UnifiedRouter

DB_FILE = "public_apis_registry.db"

class DistressLeadEngine:
    def __init__(self, db_path: str = DB_FILE):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.indicators = IndicatorLibrary(db_path)
        self.router = UnifiedRouter()
        self._init_leads_schema()

    def _init_leads_schema(self):
        """Initializes tables for scored property leads and audit trails."""
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS distress_leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            apn TEXT NOT NULL,
            fips TEXT NOT NULL,
            state TEXT NOT NULL,
            owner_name TEXT,
            assessed_value REAL,
            open_liens_balance REAL,
            tax_delinquency REAL,
            default_amount REAL,
            net_equity_buffer REAL,
            distress_score INTEGER, -- 0 to 100
            distress_triggers TEXT, -- Comma-separated indicators
            status TEXT DEFAULT 'NEW', -- NEW, QUALIFIED, EXPORTED
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(apn, fips)
        );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_leads_score ON distress_leads(distress_score);")
        self.conn.commit()

    def score_lead(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates parcel indicators to compute Distress Score (0-100) and Equity Buffer.
        Ground rule: A lead is only viable if there is positive net equity covering delinquent amounts.
        """
        score = 0
        triggers = []

        assessed = float(record.get("assessed_value") or 0.0)
        liens = float(record.get("open_balance") or record.get("open_liens_balance") or 0.0)
        tax_due = float(record.get("tax_delinquency") or 0.0)
        default_amt = float(record.get("default_amount") or 0.0)

        # Distress weighting
        if tax_due > 0:
            score += 30
            triggers.append(f"tax_delinquency(${tax_due:,.2f})")
        if default_amt > 0 or record.get("notice_of_default"):
            score += 35
            triggers.append("notice_of_default")
        if record.get("lis_pendens"):
            score += 25
            triggers.append("lis_pendens")

        # Deduct for bankruptcies or corporate suspension (clouds immediate title liquidation)
        if record.get("bankruptcy_chapter"):
            triggers.append(f"bankruptcy_ch_{record['bankruptcy_chapter']}(STAY)")
            score = max(0, score - 20)

        # Net Equity Calculation
        total_encumbrances = liens + tax_due + default_amt
        net_equity = assessed - total_encumbrances

        # Equity viability bonus
        if assessed > 0 and (net_equity / assessed) >= 0.35:
            score += 10
            triggers.append("high_equity_buffer(>35%)")

        score = min(100, score)

        return {
            "apn": record.get("apn"),
            "fips": record.get("fips", "06045"), # Mendocino County default
            "state": record.get("state", "CA"),
            "owner_name": record.get("grantee") or record.get("owner_name", "UNKNOWN"),
            "assessed_value": assessed,
            "open_liens_balance": liens,
            "tax_delinquency": tax_due,
            "default_amount": default_amt,
            "net_equity_buffer": net_equity,
            "distress_score": score,
            "distress_triggers": ",".join(triggers)
        }

    def ingest_and_save(self, records: List[Dict[str, Any]]) -> int:
        """Stores or updates evaluated leads in the database."""
        cursor = self.conn.cursor()
        saved = 0
        for rec in records:
            scored = self.score_lead(rec)
            cursor.execute("""
                INSERT INTO distress_leads (
                    apn, fips, state, owner_name, assessed_value,
                    open_liens_balance, tax_delinquency, default_amount,
                    net_equity_buffer, distress_score, distress_triggers
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(apn, fips) DO UPDATE SET
                    assessed_value=excluded.assessed_value,
                    open_liens_balance=excluded.open_liens_balance,
                    tax_delinquency=excluded.tax_delinquency,
                    default_amount=excluded.default_amount,
                    net_equity_buffer=excluded.net_equity_buffer,
                    distress_score=excluded.distress_score,
                    distress_triggers=excluded.distress_triggers
            """, (
                scored["apn"], scored["fips"], scored["state"], scored["owner_name"],
                scored["assessed_value"], scored["open_liens_balance"], scored["tax_delinquency"],
                scored["default_amount"], scored["net_equity_buffer"], scored["distress_score"],
                scored["distress_triggers"]
            ))
            saved += 1
        self.conn.commit()
        return saved

    def export_qualified_leads(self, min_score: int = 50, output_csv: str = "qualified_leads.csv") -> List[Dict[str, Any]]:
        """Exports high-scoring leads with positive equity to a clean CSV."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM distress_leads
            WHERE distress_score >= ? AND net_equity_buffer > 0
            ORDER BY distress_score DESC, net_equity_buffer DESC
        """, (min_score,))
        rows = [dict(r) for r in cursor.fetchall()]

        if rows:
            keys = rows[0].keys()
            with open(output_csv, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(rows)
            print(f"[EXPORT SUCCESS] {len(rows)} qualified leads exported to '{output_csv}'")
        else:
            print(f"[EXPORT NOTICE] No leads met the threshold criteria (Min Score: {min_score}, Positive Equity).")

        return rows

if __name__ == "__main__":
    engine = DistressLeadEngine()
    
    # Test batch demonstrating scoring and equity calculation
    sample_records = [
        {
            "apn": "014-220-03",
            "fips": "06045",
            "state": "CA",
            "owner_name": "Pacific Coast Land Holdings LLC",
            "assessed_value": 450000.00,
            "open_balance": 180000.00,
            "tax_delinquency": 12450.00,
            "default_amount": 18900.00,
            "notice_of_default": True
        },
        {
            "apn": "028-110-14",
            "fips": "06045",
            "state": "CA",
            "owner_name": "Redwood Trust",
            "assessed_value": 720000.00,
            "open_balance": 680000.00,
            "tax_delinquency": 3400.00,
            "default_amount": 42000.00,
            "lis_pendens": True
        },
        {
            "apn": "005-090-22",
            "fips": "06045",
            "state": "CA",
            "owner_name": "Mendocino Heritage Corp",
            "assessed_value": 310000.00,
            "open_balance": 50000.00,
            "tax_delinquency": 8200.00,
            "default_amount": 0.0,
            "notice_of_default": False
        }
    ]

    print("─────────────────────────────────────────────────────────────")
    print("  RUNNING DISTRESS LEAD INGESTION & SCORING PIPELINE         ")
    print("─────────────────────────────────────────────────────────────")
    count = engine.ingest_and_save(sample_records)
    print(f"Processed and indexed {count} test parcel records.\n")

    leads = engine.export_qualified_leads(min_score=30)
    for lead in leads:
        print(f"\n[LEAD QUALIFIED] APN: {lead['apn']} | Score: {lead['distress_score']}/100")
        print(f"  Owner:       {lead['owner_name']}")
        print(f"  Assessed:    ${lead['assessed_value']:,.2f}")
        print(f"  Encumbered:  ${(lead['open_liens_balance'] + lead['tax_delinquency'] + lead['default_amount']):,.2f}")
        print(f"  Net Equity:  ${lead['net_equity_buffer']:,.2f}")
        print(f"  Triggers:    {lead['distress_triggers']}")
