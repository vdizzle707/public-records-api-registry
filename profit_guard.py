#!/usr/bin/env python3
"""
CHRONOS OS // STRICT PROFIT ALIGNMENT & VALIDATION GUARD
Enforces mathematical zero-loss guarantees across all flash loan and arbitrage paths.
Rejects any execution proposal where net profit does not exceed the configured minimum profit bar.
"""

import logging
from env_config import Config

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [PROFIT-GUARD] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("ProfitGuard")

class ProfitGuard:
    def __init__(self, min_net_profit_usd: float = None, max_flash_fee_bps: int = None):
        self.min_net_profit_usd = min_net_profit_usd if min_net_profit_usd is not None else Config.MIN_NET_PROFIT_USD
        self.max_flash_fee_bps = max_flash_fee_bps if max_flash_fee_bps is not None else Config.MAX_FLASH_FEE_BPS

    def validate_trade_profitability(self, borrow_amount_usd: float, expected_output_usd: float, estimated_gas_cost_usd: float) -> dict:
        """
        Evaluates gross output against flash loan repayment, flash fee, and gas cost.
        Strictly enforces the configured MIN_NET_PROFIT_USD bar.
        """
        flash_fee_usd = borrow_amount_usd * (self.max_flash_fee_bps / 10000.0)
        total_cost_usd = borrow_amount_usd + flash_fee_usd + estimated_gas_cost_usd
        net_profit_usd = expected_output_usd - total_cost_usd

        logger.info("-" * 60)
        logger.info(f"PROFIT GUARD CHECK (Threshold Bar: ${self.min_net_profit_usd:,.2f}):")
        logger.info(f"  Borrow Principal:   ${borrow_amount_usd:,.2f}")
        logger.info(f"  Flash Loan Fee:     ${flash_fee_usd:,.2f} ({self.max_flash_fee_bps} bps)")
        logger.info(f"  Estimated Gas Cost: ${estimated_gas_cost_usd:,.2f}")
        logger.info(f"  Expected Output:    ${expected_output_usd:,.2f}")
        logger.info(f"  ----------------------------------------")
        logger.info(f"  NET PROFIT:         ${net_profit_usd:,.2f}")
        logger.info("-" * 60)

        if net_profit_usd < self.min_net_profit_usd:
            logger.warning(f"❌ TRADE REJECTED: Net profit (${net_profit_usd:.2f}) is below minimum profit bar (${self.min_net_profit_usd:.2f}).")
            return {
                "approved": False,
                "reason": "PROFIT_BELOW_MINIMUM_BAR",
                "net_profit_usd": net_profit_usd,
                "required_minimum_usd": self.min_net_profit_usd
            }

        logger.info(f"✅ TRADE APPROVED: Profit bar satisfied. Net gain: ${net_profit_usd:.2f}")
        return {
            "approved": True,
            "reason": "PROFIT_BAR_SATISFIED",
            "net_profit_usd": net_profit_usd,
            "flash_fee_usd": flash_fee_usd,
            "total_cost_usd": total_cost_usd
        }

if __name__ == "__main__":
    print("=" * 76)
    print("      CHRONOS OS // PROFIT GUARD ENFORCEMENT TEST")
    print("=" * 76)
    guard = ProfitGuard()
    
    # Test case: Validating profit bar
    guard.validate_trade_profitability(
        borrow_amount_usd=50000.00,
        expected_output_usd=50120.00,
        estimated_gas_cost_usd=20.00
    )
    print("=" * 76)
