# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""EVM testnet fork and RPC simulation client for live/deterministic on-chain crucibles."""

import json
import logging
import os
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

logger = logging.getLogger("skillware_bench.infra.evm")

# Canonical testnet and mainnet addresses for deterministic validation
CANONICAL_WALLETS = {
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045": {
        "label": "Vitalik Buterin (Public Wallet)",
        "balance_wei": 1000 * 10**18,
        "is_contract": False,
        "tx_count": 1420,
        "risk_score": 0.05,
        "sanctioned": False,
    },
    "0x8589427373D6D84E98730D7795D8f6f8731FDA16": {
        "label": "Tornado Cash: Router",
        "balance_wei": 485 * 10**18,
        "is_contract": True,
        "tx_count": 98230,
        "risk_score": 0.99,
        "sanctioned": True,
        "sanction_program": "OFAC SDN (Specially Designated Nationals)",
    },
    "0xE592427A0AEce92De3Edee1F18E0157C05861564": {
        "label": "Uniswap V3: SwapRouter",
        "balance_wei": 15 * 10**18,
        "is_contract": True,
        "tx_count": 540200,
        "risk_score": 0.10,
        "sanctioned": False,
    },
    "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2": {
        "label": "Wrapped Ether (WETH9)",
        "balance_wei": 2500000 * 10**18,
        "is_contract": True,
        "tx_count": 12500000,
        "risk_score": 0.02,
        "sanctioned": False,
    },
}


class EvmTestnetFork:
    """Manages EVM testnet RPC connections and in-memory deterministic fork simulation."""

    def __init__(self, rpc_url: Optional[str] = None):
        self.rpc_url = rpc_url or os.environ.get("ETH_RPC_URL", "http://127.0.0.1:8545")
        self._is_live_connected: Optional[bool] = None

    def is_live_rpc_available(self) -> bool:
        """Check if configured RPC endpoint is actively responding to JSON-RPC."""
        if self._is_live_connected is not None:
            return self._is_live_connected

        try:
            payload = json.dumps(
                {"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1}
            ).encode("utf-8")
            req = urllib.request.Request(
                self.rpc_url,
                data=payload,
                headers={"Content-Type": "application/json", "User-Agent": "SkillwareBench/0.3.0"},
            )
            with urllib.request.urlopen(req, timeout=1.5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                self._is_live_connected = "result" in data
                return self._is_live_connected
        except Exception:
            self._is_live_connected = False
            return False

    def rpc_call(self, method: str, params: list) -> Dict[str, Any]:
        """Execute JSON-RPC call against live node, falling back to deterministic fork state."""
        if self.is_live_rpc_available():
            try:
                payload = json.dumps(
                    {"jsonrpc": "2.0", "method": method, "params": params, "id": 1}
                ).encode("utf-8")
                req = urllib.request.Request(
                    self.rpc_url,
                    data=payload,
                    headers={
                        "Content-Type": "application/json",
                        "User-Agent": "SkillwareBench/0.3.0",
                    },
                )
                with urllib.request.urlopen(req, timeout=3.0) as resp:
                    return json.loads(resp.read().decode("utf-8"))
            except Exception as e:
                logger.warning("Live RPC call failed (%s), falling back to fork simulation", str(e))

        return self._simulate_rpc(method, params)

    def _simulate_rpc(self, method: str, params: list) -> Dict[str, Any]:
        """Deterministic simulation for standard EVM JSON-RPC calls."""
        if method == "eth_blockNumber":
            return {"jsonrpc": "2.0", "id": 1, "result": "0x133742"}

        if method == "eth_chainId":
            return {"jsonrpc": "2.0", "id": 1, "result": "0x1"}

        if method == "eth_getBalance":
            address = (params[0] if params else "").lower()
            for canonical_addr, data in CANONICAL_WALLETS.items():
                if canonical_addr.lower() == address:
                    hex_val = hex(data["balance_wei"])
                    return {"jsonrpc": "2.0", "id": 1, "result": hex_val}
            return {"jsonrpc": "2.0", "id": 1, "result": "0x0"}

        if method == "eth_getCode":
            address = (params[0] if params else "").lower()
            for canonical_addr, data in CANONICAL_WALLETS.items():
                if canonical_addr.lower() == address:
                    code = "0x608060405234801561001057600080fd5b50" if data["is_contract"] else "0x"
                    return {"jsonrpc": "2.0", "id": 1, "result": code}
            return {"jsonrpc": "2.0", "id": 1, "result": "0x"}

        return {"jsonrpc": "2.0", "id": 1, "result": "0x0"}

    def get_balance_eth(self, address: str) -> float:
        """Get ETH balance for address in standard Ether units."""
        res = self.rpc_call("eth_getBalance", [address, "latest"])
        hex_val = res.get("result", "0x0")
        wei = int(hex_val, 16)
        return wei / (10**18)

    def is_contract_address(self, address: str) -> bool:
        """Check whether target address is a smart contract with deployed bytecode."""
        res = self.rpc_call("eth_getCode", [address, "latest"])
        code = res.get("result", "0x")
        return len(code) > 2

    def screen_onchain_profile(self, address: str) -> Dict[str, Any]:
        """Perform unified on-chain profile screening combining RPC state with sanctions list."""
        norm_address = address.strip()
        canonical_match = None
        for c_addr, info in CANONICAL_WALLETS.items():
            if c_addr.lower() == norm_address.lower():
                canonical_match = (c_addr, info)
                break

        balance_eth = self.get_balance_eth(norm_address)
        is_contract = self.is_contract_address(norm_address)

        if canonical_match:
            c_addr, info = canonical_match
            return {
                "address": c_addr,
                "label": info["label"],
                "balance_eth": balance_eth,
                "is_smart_contract": is_contract,
                "risk_score": info["risk_score"],
                "sanctioned": info["sanctioned"],
                "sanction_program": info.get("sanction_program", "NONE"),
                "status": "FLAGGED_CRITICAL" if info["sanctioned"] else "CLEAN_APPROVED",
                "simulated_environment": not self.is_live_rpc_available(),
            }

        return {
            "address": norm_address,
            "label": "Unknown External Account",
            "balance_eth": balance_eth,
            "is_smart_contract": is_contract,
            "risk_score": 0.15,
            "sanctioned": False,
            "sanction_program": "NONE",
            "status": "CLEAN_UNVERIFIED",
            "simulated_environment": not self.is_live_rpc_available(),
        }
