#!/usr/bin/env python3
"""
CHRONOS OS // SECURE ENVIRONMENT & CONFIGURATION LOADER
Scans for local .env or production_config.env files, parses variables securely without exposing secrets,
and provides centralized credential and profit threshold management across all modules.
"""

import os
import logging

logger = logging.getLogger("EnvConfig")

def load_env_file(filepath: str = "production_config.env"):
    """Manually parse environment file line by line to avoid external package dependencies."""
    if not os.path.exists(filepath):
        return False
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip("'\"")
                    if key and key not in os.environ:
                        os.environ[key] = value
        return True
    except Exception as e:
        logger.error(f"Error reading environment file: {e}")
        return False

# Attempt to load configuration file on import
load_env_file()

class Config:
    # Blockchain / DeFi
    ETHEREUM_WSS_URL = os.getenv("ETHEREUM_WSS_URL", "wss://mainnet.infura.io/ws/v3/placeholder")
    SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
    
    # Monetization / Billing
    STRIPE_API_KEY = os.getenv("STRIPE_API_KEY", "")
    
    # OSINT & Data Providers
    PDL_API_KEY = os.getenv("PDL_API_KEY", "")
    ENFORMION_API_KEY = os.getenv("ENFORMION_API_KEY", "")
    SEARCHBUG_API_KEY = os.getenv("SEARCHBUG_API_KEY", "")
    RENTCAST_API_KEY = os.getenv("RENTCAST_API_KEY", "")

    # Profit Enforcement Bar (Aligned to MetaMask Gasless Paymaster $200 threshold)
    MIN_NET_PROFIT_USD = float(os.getenv("MIN_NET_PROFIT_USD", "200.00"))
    MAX_FLASH_FEE_BPS = int(os.getenv("MAX_FLASH_FEE_BPS", "5"))

    @classmethod
    def validate_production_readiness(cls) -> list:
        missing = []
        if not cls.STRIPE_API_KEY or "YourStripe" in cls.STRIPE_API_KEY:
            missing.append("STRIPE_API_KEY")
        if "placeholder" in cls.ETHEREUM_WSS_URL or "YOUR_INFURA" in cls.ETHEREUM_WSS_URL:
            missing.append("ETHEREUM_WSS_URL")
        return missing

if __name__ == "__main__":
    print("=" * 76)
    print("      CHRONOS OS // ENVIRONMENT & CONFIGURATION STATUS")
    print("=" * 76)
    print(f"Minimum Net Profit Bar: ${Config.MIN_NET_PROFIT_USD:,.2f} (Gasless Promo Aligned)")
    print(f"Max Flash Loan Fee:     {Config.MAX_FLASH_FEE_BPS} bps")
    missing_keys = Config.validate_production_readiness()
    if missing_keys:
        print(f"[WARNING] Missing production credentials: {', '.join(missing_keys)}")
        print("          Update your production_config.env file with your mainnet keys.")
    else:
        print("[OK] All core production environment variables are configured.")
    print("=" * 76)
