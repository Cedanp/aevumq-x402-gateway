import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="AevumQ ASI · 24/7 Cloud x402 L10 & A2A Gateway")

WALLET = os.getenv("PUBLIC_WALLET_EVM", "0x3528a70Ba71da2f9F5e4c13025950429F59aC3E9")
CHECKOUT = os.getenv("LINK_CHECKOUT_GLOBAL", "https://polar.sh")
TAXA = 0.015

@app.get("/")
def root():
    return {
        "system": "AevumQ ASI · Autonomous Venture OS (24/7 Cloud)",
        "protocol": "x402-Facilitator-Apex-L10",
        "agent_card": "/.well-known/agent.json",
        "x402_endpoint": "/api/x402/gate/{servico}?valor_tx=1000",
        "checkout_global": CHECKOUT
    }

@app.get("/.well-known/agent.json")
def agent_card():
    return {
        "name": "AevumQ ASI",
        "version": "12.0-Apex-Cloud",
        "description": "Autonomous Quantitative Risk, 24/7 Tokenized Assets (RWA), Code-Hygiene MCP & x402 L10 Verification Facilitator.",
        "protocols": ["A2A/1.0", "MCP/1.0", "x402/1.0"],
        "checkout_global": CHECKOUT,
        "settlement_wallet_evm": WALLET,
        "settlement_network": "base-mainnet",
        "settlement_asset": "USDC",
        "capabilities": ["antithetic_monte_carlo", "rwa_24_7_volatility", "mcp_secret_audit", "x402_escrow_verification"],
        "affiliate_bounty": "25% net revenue share (pay-after-settlement)"
    }

@app.get("/api/x402/gate/{servico}")
def x402_gate(servico: str, request: Request, valor_tx: float = 100.0):
    pagamento = request.headers.get("X-PAYMENT", "")
    taxa_usdc = round(max(0.05, valor_tx * TAXA), 4)
    cotacao = {
        "protocol": "x402-Facilitator-Apex-L10",
        "network": "base-mainnet",
        "asset": "USDC",
        "recipient_treasury": WALLET,
        "service_verified": servico,
        "settlement_fee_usdc": taxa_usdc
    }
    if not pagamento:
        return JSONResponse(
            status_code=402,
            content={
                "error": "Payment Required",
                "x402Version": 1,
                "accepts": [{
                    "scheme": "exact",
                    "network": "base",
                    "maxAmountRequired": str(int(taxa_usdc * 1_000_000)),
                    "resource": str(request.url),
                    "description": f"AevumQ Apex L10 Verification & Escrow Fee ({servico})",
                    "payTo": WALLET,
                    "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
                }]
            },
            headers={"X-Payment-Required": json.dumps(cotacao)}
        )
    return {"status": "SETTLED_L10", "tx_header": pagamento[:24]}
