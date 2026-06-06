import asyncio
import logging
import sqlite3
from typing import Dict, Any, Optional
from web3 import Web3
from eth_account import Account

from .config_loader import load_config, AppConfig
from .p2p_manager import P2PManager
from .crypto_utils import CryptoManager
from .protocol_pb2 import DataNeedSpec, DataOffer, QualityReport, PurchaseRequest

logging.basicConfig(level=logging.INFO)

class SellerAgent:
    def __init__(self, config_path: str = "config.yaml"):
        self.config: AppConfig = load_config(config_path)
        self.logger = logging.getLogger("SellerAgent")
        self.p2p = P2PManager(self.config.p2p.peer_id, self.config.p2p.listen_port + 1)
        self.crypto = CryptoManager()
        self.db = self._init_db()
        self.w3 = Web3(Web3.HTTPProvider(self.config.blockchain.rpc_url))
        self.account = Account.from_key(self.config.wallet.private_key)

    def _init_db(self):
        conn = sqlite3.connect("seller_catalog.db")
        conn.execute("CREATE TABLE IF NOT EXISTS datasets (id TEXT PRIMARY KEY, name TEXT, path TEXT, tags TEXT, price_milli INTEGER)")
        conn.execute("INSERT OR IGNORE INTO datasets VALUES (?,?,?,?,?)", ("ds-1", "Health Records", "data/h.csv", "health,medical", 50000))
        conn.commit()
        return conn

    async def start(self):
        await self.p2p.start()
        self.p2p.subscribe("needs", self.handle_need)
        self.p2p.subscribe(f"direct-{self.p2p.peer_id}", self.handle_direct)
        self.logger.info(f"Seller Agent {self.config.p2p.peer_id} is live.")

    async def handle_need(self, sender_id: str, need: DataNeedSpec):
        self.logger.info(f"Need received: {need.data_type}")
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM datasets WHERE tags LIKE ?", (f"%{need.data_type}%",))
        for match in cursor.fetchall():
            offer = DataOffer()
            offer.offer_id = f"off-{match[0]}-{need.request_id}"
            offer.request_id = need.request_id
            offer.dataset_id = match[0]
            offer.seller_peer_id = self.p2p.peer_id
            offer.seller_wallet = self.account.address
            offer.price_usdc_milli = match[4]
            qr = QualityReport(row_count=1000, null_rate_permille=5, schema_match=True)
            offer.public_quality.CopyFrom(qr)
            await self.p2p.broadcast("offers", offer)

    async def handle_direct(self, sender_id: str, payload: Any):
        msg_type, data = payload
        if msg_type == "PURCHASE_START":
            await self._start_data_transfer(data)

    async def _start_data_transfer(self, req: PurchaseRequest):
        self.logger.info(f"Transferring dataset {req.offer_id} to {req.buyer_wallet}")
        stream = await self.p2p.open_stream(req.buyer_wallet)
        await stream.write(b"ENCRYPTED_DATA_CHUNK")
        await stream.close()

async def main():
    seller = SellerAgent()
    await seller.start()
    while True: await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
