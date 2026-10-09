#!/usr/bin/env python3
import sqlite3
import json
import uuid
import sys
from typing import Dict, Any, List, Optional

DB_FILE = "public_apis_registry.db"

class BillingGateway:
    def __init__(self, db_path: str = DB_FILE):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_billing_schema()

    def _init_billing_schema(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer_orders (
            order_id TEXT PRIMARY KEY,
            client_id TEXT NOT NULL,
            tier_name TEXT NOT NULL,
            amount_usd REAL NOT NULL,
            payment_status TEXT NOT NULL,
            transaction_ref TEXT UNIQUE,
            leads_delivered INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            cleared_at TIMESTAMP
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS settlement_audit_log (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            gross_amount REAL NOT NULL,
            fee_amount REAL NOT NULL,
            net_withdrawable REAL NOT NULL,
            settlement_verified BOOLEAN NOT NULL,
            payload_snapshot TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES customer_orders(order_id)
        );
        """)
        self.conn.commit()

    def create_lead_order(self, client_id: str, lead_count: int, price_per_lead: float = 25.00) -> Dict[str, Any]:
        order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        total_amount = lead_count * price_per_lead
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO customer_orders (order_id, client_id, tier_name, amount_usd, payment_status)
            VALUES (?, ?, ?, ?, 'PENDING')
        """, (order_id, client_id, f"DISTRESS_PACK_{lead_count}", total_amount))
        self.conn.commit()
        return {
            "order_id": order_id,
            "client_id": client_id,
            "lead_count": lead_count,
            "amount_usd": total_amount,
            "status": "PENDING_PAYMENT"
        }

    def verify_and_clear_settlement(self, order_id: str, external_tx_ref: str, amount_paid: float, fee_paid: float = 0.0) -> Dict[str, Any]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM customer_orders WHERE order_id = ?", (order_id,))
        order = cursor.fetchone()
        if not order:
            return {"success": False, "error": f"ORDER_NOT_FOUND: {order_id}"}
        if order["payment_status"] == "CLEARED":
            return {"success": True, "status": "ALREADY_CLEARED", "order_id": order_id}
        if amount_paid < order["amount_usd"]:
            return {"success": False, "error": f"UNDERPAYMENT: Expected {order['amount_usd']}, got {amount_paid}"}

        net_withdrawable = amount_paid - fee_paid
        cursor.execute("""
            UPDATE customer_orders
            SET payment_status = 'CLEARED',
                transaction_ref = ?,
                cleared_at = CURRENT_TIMESTAMP
            WHERE order_id = ?
        """, (external_tx_ref, order_id))

        cursor.execute("""
            INSERT INTO settlement_audit_log (
                order_id, event_type, gross_amount, fee_amount, net_withdrawable, settlement_verified, payload_snapshot
            ) VALUES (?, 'PAYMENT_CONFIRMED', ?, ?, ?, 1, ?)
        """, (order_id, amount_paid, fee_paid, net_withdrawable, json.dumps({"tx_ref": external_tx_ref})))
        self.conn.commit()
        return {
            "success": True,
            "order_id": order_id,
            "gross_cleared": amount_paid,
            "net_withdrawable": net_withdrawable,
            "status": "SETTLED"
        }

    def release_unredacted_leads(self, order_id: str, limit: int = 5) -> Dict[str, Any]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM customer_orders WHERE order_id = ?", (order_id,))
        order = cursor.fetchone()
        if not order or order["payment_status"] != "CLEARED":
            return {"success": False, "error": "ACCESS_DENIED: Settlement unverified."}

        cursor.execute("""
            SELECT id, apn, fips, state, owner_name, assessed_value,
                   open_liens_balance, tax_delinquency, default_amount,
                   net_equity_buffer, distress_score, distress_triggers
            FROM distress_leads
            WHERE status != 'EXPORTED' AND net_equity_buffer > 0
            ORDER BY distress_score DESC, net_equity_buffer DESC
            LIMIT ?
        """, (limit,))
        leads = [dict(r) for r in cursor.fetchall()]
        if not leads:
            return {"success": False, "error": "NO_UNCLAIMED_LEADS_AVAILABLE"}

        lead_ids = [str(l["id"]) for l in leads]
        placeholders = ",".join(["?"] * len(lead_ids))
        cursor.execute(f"UPDATE distress_leads SET status = 'EXPORTED' WHERE id IN ({placeholders})", lead_ids)
        cursor.execute("UPDATE customer_orders SET leads_delivered = leads_delivered + ? WHERE order_id = ?", (len(leads), order_id))
        self.conn.commit()

        return {
            "success": True,
            "order_id": order_id,
            "delivered_count": len(leads),
            "leads": leads
        }

if __name__ == "__main__":
    gateway = BillingGateway()
    order = gateway.create_lead_order(client_id="INVESTOR_CAPITAL_GRP", lead_count=2, price_per_lead=25.00)
    print(f"[ORDER CREATED] ID: {order['order_id']} | Total: ${order['amount_usd']:.2f}")

    unauth = gateway.release_unredacted_leads(order["order_id"])
    print(f"[PRE-SETTLEMENT CHECK] Expected fail: {unauth.get('error')}")

    tx_ref = f"ch_stripe_{uuid.uuid4().hex[:10]}"
    settlement = gateway.verify_and_clear_settlement(order["order_id"], tx_ref, 50.00, 1.75)
    print(f"[SETTLEMENT CLEARED] Net Withdrawable: ${settlement['net_withdrawable']:.2f}")

    delivery = gateway.release_unredacted_leads(order["order_id"], limit=2)
    print(f"[FULFILLMENT] Delivered {delivery.get('delivered_count', 0)} lead(s)")
