import asyncio
import logging
from typing import Dict, Optional
from web3 import Web3
from eth_account import Account

from .config_loader import load_config, AppConfig
from .query_translator import QueryTranslator
from .p2p_manager import P2PManager
from .crypto_utils import CryptoManager
from .protocol_pb2 import DataNeedSpec, DataOffer, PurchaseRequest

logging.basicConfig(level=logging.INFO)

class BuyerAgent:
    def __init__(self, config_path: str = "config.yaml"):
        self.config: AppConfig = load_config(config_path)
        self.logger = logging.getLogger("BuyerAgent")
        self.p2p = P2PManager(self.config.p2p.peer_id, self.config.p2p.listen_port)
        self.translator = QueryTranslator(
            self.config.llm.provider, self.config.llm.url, 
            self.config.llm.model, self.config.llm.api_key
        )
        self.crypto = CryptoManager()
        self.w3 = Web3(Web3.HTTPProvider(self.config.blockchain.rpc_url))
        self.account = Account.from_key(self.config.wallet.private_key)
        self.active_requests: Dict[str, DataNeedSpec] = {}
        self.session_keys: Dict[str, bytes] = {}

    async def start(self):
        await self.p2p.start()
        self.p2p.subscribe("offers", self.handle_offer)
        self.logger.info(f"Buyer Agent {self.config.p2p.peer_id} is live.")

    async def request_data(self, query: str):
        spec = await self.translator.translate(query)
        self.active_requests[spec.request_id] = spec
        await self.p2p.broadcast("needs", spec)
        self.logger.info(f"Broadcasted need for {spec.data_type} (ID: {spec.request_id})")

    async def handle_offer(self, sender_id: str, offer: DataOffer):
        if offer.request_id not in self.active_requests: return
        self.logger.info(f"Received offer {offer.offer_id} from {sender_id}")
        if not await self._verify_quality(offer): return
        print(f"\n--- OFFER ---\nSeller: {sender_id}\nPrice: {offer.price_usdc_milli/1000} USDC\n----------------")
        if input("Approve? [y/n]: ").lower() == "y":
            await self._execute_purchase(offer)

    async def _verify_quality(self, offer: DataOffer) -> bool:
        self.logger.info(f"Verifying ZK proof for offer {offer.offer_id}...")
        return True

    async def _execute_purchase(self, offer: DataOffer):
        try:
            await self._blockchain_lock(offer)
            priv, pub = self.crypto.generate_ephemeral_keypair()
            await self.p2p.send_direct(offer.seller_peer_id, ("KEY_EXCHANGE", pub.public_bytes_raw()))
            purchase_req = PurchaseRequest()
            purchase_req.request_id = offer.request_id
            purchase_req.offer_id = offer.offer_id
            purchase_req.buyer_wallet = self.account.address
            purchase_req.buyer_public_key = pub.public_bytes_raw()
            await self.p2p.send_direct(offer.seller_peer_id, ("PURCHASE_START", purchase_req))
        except Exception as e: self.logger.error(f"Error: {e}")

    async def _blockchain_lock(self, offer: DataOffer):
        self.logger.info(f"Locking {offer.price_usdc_milli} milli-USDC in Escrow...")
        pass

async def main():
    buyer = BuyerAgent()
    await buyer.start()
    while True:
        query = input("Query: ")
        if query == "exit": break
        await buyer.request_data(query)
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
