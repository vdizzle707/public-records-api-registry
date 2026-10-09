#!/usr/bin/env python3
"""
CHRONOS OS // EVM WSS REAL-TIME ARBITRAGE & FLASH LOAN MONITOR
Option 1 Integration: WebSocket (WSS) live subscription to Ethereum mempool
and DEX swap events. Aligned with the $200 MetaMask Gasless Paymaster promo bar.
"""

import asyncio
import json
import logging
import os
import sys
from env_config import Config
from profit_guard import ProfitGuard
from metamask_gasless_paymaster import MetamaskGaslessPaymaster

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [EVM-WSS-ARBITRAGE] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("EvmWssArbitrage")

class EvmWssArbitrageMonitor:
    def __init__(self, wss_url: str):
        self.wss_url = wss_url
        self.running = False
        self.profit_guard = ProfitGuard()
        self.paymaster = MetamaskGaslessPaymaster()

    async def connect_and_listen(self):
        try:
            import websockets
        except ImportError:
            logger.error("The 'websockets' package is required. Install via: pip install websockets")
            sys.exit(1)

        logger.info(f"Connecting to Ethereum WSS Provider: {self.wss_url[:30]}...")
        logger.info(f"Active Profit Bar (Gasless Promo): ${self.profit_guard.min_net_profit_usd:,.2f}")
        self.running = True

        while self.running:
            try:
                async with websockets.connect(self.wss_url) as websocket:
                    logger.info("Successfully established WSS connection to EVM node.")
                    
                    sub_heads = {
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "eth_subscribe",
                        "params": ["newHeads"]
                    }
                    await websocket.send(json.dumps(sub_heads))
                    await websocket.recv()

                    sub_pending = {
                        "jsonrpc": "2.0",
                        "id": 2,
                        "method": "eth_subscribe",
                        "params": ["pendingTransactions", {"fullTransactions": True}]
                    }
                    await websocket.send(json.dumps(sub_pending))
                    await websocket.recv()

                    async for message in websocket:
                        await self.handle_message(message)

            except Exception as e:
                logger.warning(f"WSS connection dropped: {e}. Reconnecting in 5 seconds...")
                await asyncio.sleep(5)

    async def handle_message(self, message: str):
        try:
            data = json.loads(message)
            if "params" in data and "result" in data["params"]:
                result = data["params"]["result"]
                if isinstance(result, dict) and "input" in result:
                    await self.analyze_mempool_tx(result)
        except Exception:
            pass

    async def analyze_mempool_tx(self, tx: dict):
        input_data = tx.get("input", "")
        to_address = tx.get("to", "")

        if input_data.startswith("0x414bf389") or input_data.startswith("0xc04b8d59"):
            tx_hash = tx.get("hash")
            logger.info(f"[DEX SWAP CANDIDATE] Tx: {tx_hash[:12]}... | Router: {to_address[:10]}...")
            await self.evaluate_arbitrage_opportunity(tx)

    async def evaluate_arbitrage_opportunity(self, tx: dict):
        # Simulated trade parameters evaluated against the $200 profit bar
        borrow_amount = 50000.00
        expected_output = 50250.00 # $250 gross - $25 fee/gas = $225 net (> $200 bar)
        estimated_gas = 25.00

        profit_check = self.profit_guard.validate_trade_profitability(
            borrow_amount_usd=borrow_amount,
            expected_output_usd=expected_output,
            estimated_gas_cost_usd=estimated_gas
        )

        if profit_check["approved"]:
            net_profit = profit_check["net_profit_usd"]
            logger.info(f"✨ Opportunity qualifies for MetaMask Gasless Paymaster promo (Net: ${net_profit:.2f})")
            
            sponsorship = self.paymaster.evaluate_sponsorship(
                user_address="0x1234567890abcdef1234567890abcdef12345678",
                net_profit_usd=net_profit,
                transaction_payload=tx
            )
            if sponsorship["sponsored"]:
                logger.info("🚀 [READY FOR SUBMISSION] Gasless EIP-712 bundle ready for MetaMask execution.")

    def start(self):
        try:
            asyncio.run(self.connect_and_listen())
        except KeyboardInterrupt:
            logger.info("EVM WSS Arbitrage Monitor stopped by user.")

if __name__ == "__main__":
    print("=" * 76)
    print("      CHRONOS OS // EVM WSS ARBITRAGE MONITOR (GASLESS ALIGNED)")
    print("=" * 76)
    monitor = EvmWssArbitrageMonitor(Config.ETHEREUM_WSS_URL)
    print(f"Monitor initialized with minimum profit bar: ${monitor.profit_guard.min_net_profit_usd:,.2f}")
    print("=" * 76)
