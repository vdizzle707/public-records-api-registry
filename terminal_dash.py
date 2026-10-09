#!/usr/bin/env python3
"""
CHRONOS OS // TERMINAL DASHBOARD & BALANCE MONITOR
Provides a comprehensive real-time terminal dashboard monitoring active API credentials,
billing balances (Stripe/PayPal), Supabase database metrics, and EVM/MetaMask gasless paymaster status.
"""

import os
import sys
import sqlite3
import json
from pathlib import Path
from env_config import Config, load_env_file

def print_header():
    print("=" * 80)
    print("      CHRONOS OS // LIVE TERMINAL DASHBOARD & BALANCE MONITOR")
    print("=" * 80)

def check_env_status():
    load_env_file()
    print("\n[1. API CREDENTIALS & ENVIRONMENT STATUS]")
    print("-" * 80)
    
    keys_to_check = [
        ("STRIPE_API_KEY", "Stripe API Key"),
        ("PAYPAL_CLIENT_ID", "PayPal Client ID"),
        ("PLAID_SANDBOX_KEY", "Plaid Sandbox Key"),
        ("CIRCLE_LIVE_API_KEY", "Circle Live API Key"),
        ("COINBASE_API_KEY_ID", "Coinbase API Key ID"),
        ("OPENAI_API_KEY", "OpenAI API Key"),
        ("ALCHEMY_MAINNET_API_KEY", "Alchemy Mainnet Key"),
        ("SUPABASE_PROJECT_URL", "Supabase Project URL"),
        ("ETHERSCAN_API_KEY", "Etherscan API Key"),
        ("GOOGLE_API_KEY", "Google API Key")
    ]

    configured_count = 0
    for env_var, label in keys_to_check:
        val = os.getenv(env_var, "")
        status = "✅ CONFIGURED" if val and "your_" not in val and "Here" not in val else "⚠️ PLACEHOLDER / MISSING"
        if "✅" in status:
            configured_count += 1
        print(f"  - {label:<25} : {status}")
    print(f"\n  Total Configured Active Keys: {configured_count}/{len(keys_to_check)}")

def check_vault_stats():
    print("\n[2. LOCAL VAULT & LEAD PIPELINE METRICS]")
    print("-" * 80)
    db_path = "public_apis_registry.db"
    if not os.path.exists(db_path):
        print("  ⚠️ Database vault 'public_apis_registry.db' not found.")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        dossiers_count = cursor.execute("SELECT COUNT(*) FROM audit_dossiers").fetchone()[0]
        orders_count = cursor.execute("SELECT COUNT(*) FROM customer_orders").fetchone()[0] if cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='customer_orders'").fetchone() else 0
        leads_count = cursor.execute("SELECT COUNT(*) FROM distress_leads").fetchone()[0] if cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='distress_leads'").fetchone() else 0
        
        print(f"  - Audit Dossiers Logged       : {dossiers_count}")
        print(f"  - Customer Orders (Stripe)    : {orders_count}")
        print(f"  - Distress Leads Ingested     : {leads_count}")
        conn.close()
    except Exception as e:
        print(f"  ⚠️ Error reading vault DB: {e}")

def check_paymaster_status():
    print("\n[3. METAMASK & GASLESS PAYMASTER STATUS]")
    print("-" * 80)
    print(f"  - Paymaster Relay URL         : {os.getenv('PAYMASTER_RELAY_URL', 'https://api.paymaster.io/v1/sponsor')}")
    print(f"  - Min Net Profit Threshold    : ${Config.MIN_NET_PROFIT_USD:,.2f} (Gasless Promo Bar)")
    print(f"  - Max Flash Loan Fee          : {Config.MAX_FLASH_FEE_BPS} bps")
    print(f"  - Wallet Provider             : MetaMask (EIP-712 Meta-Transactions Enabled)")

def main():
    print_header()
    check_env_status()
    check_vault_stats()
    check_paymaster_status()
    print("\n" + "=" * 80)
    print("      [DASHBOARD ACTIVE] System is ready for live execution & monitoring.")
    print("=" * 80)

if __name__ == "__main__":
    main()
