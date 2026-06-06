import yaml
import os
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class WalletConfig(BaseModel):
    address: str
    private_key: str

class P2PConfig(BaseModel):
    listen_port: int = 8000
    topic: str = "data-syndicate-needs"
    peer_id: str

class LLMConfig(BaseModel):
    provider: str = "ollama"
    url: str = "http://localhost:11434"
    model: str = "phi-3-mini"
    api_key: Optional[str] = None

class BlockchainConfig(BaseModel):
    rpc_url: str = "http://127.0.0.1:8545"
    escrow_address: str = ""
    token_address: str = ""
    chain_id: int = 31337

class AppConfig(BaseModel):
    wallet: WalletConfig
    p2p: P2PConfig
    llm: LLMConfig
    blockchain: BlockchainConfig

def load_config(config_path: str = "config.yaml") -> AppConfig:
    """
    Loads and validates the project configuration.
    In a production environment, sensitive keys would be loaded from env vars.
    """
    if not os.path.exists(config_path):
        # Default structure for local development if file missing
        default_data = {
            "wallet": {
                "address": "0x0000000000000000000000000000000000000000",
                "private_key": "0xac0974bec39a1786953646852d36ef146be32383fce1f26627e5beS"
            },
            "p2p": {
                "listen_port": 8000,
                "topic": "data-syndicate-needs",
                "peer_id": "local-node-1"
            },
            "llm": {
                "provider": "ollama",
                "url": "http://localhost:11434",
                "model": "phi-3-mini",
                "api_key": None
            },
            "blockchain": {
                "rpc_url": "http://127.0.0.1:8545",
                "escrow_address": "0x0000000000000000000000000000000000000000",
                "token_address": "0x0000000000000000000000000000000000000000",
                "chain_id": 31337
            }
        }
        return AppConfig(**default_data)

    with open(config_path, "r") as f:
        data = yaml.safe_load(f)
        return AppConfig(**data)
