import asyncio
import logging
from typing import Callable, Awaitable, Dict, List, Any

class P2PManager:
    def __init__(self, peer_id: str, port: int):
        self.peer_id = peer_id
        self.port = port
        self.logger = logging.getLogger(f"P2P-{peer_id}")
        self._subscriptions = {}
        self._bus = getattr(P2PManager, "_global_bus", asyncio.Queue())
        P2PManager._global_bus = self._bus

    async def start(self):
        self.logger.info(f"Node {self.peer_id} listening on port {self.port}")
        asyncio.create_task(self._listen_loop())

    async def _listen_loop(self):
        while True:
            message = await self._bus.get()
            sender_id, topic, payload = message
            if sender_id == self.peer_id: continue
            if topic in self._subscriptions:
                for callback in self._subscriptions[topic]:
                    try: await callback(sender_id, payload)
                    except Exception as e: self.logger.error(f"Error: {e}")
            self._bus.task_done()

    def subscribe(self, topic: str, callback: Callable):
        if topic not in self._subscriptions: self._subscriptions[topic] = []
        self._subscriptions[topic].append(callback)

    async def broadcast(self, topic: str, payload: Any):
        await self._bus.put((self.peer_id, topic, payload))

    async def send_direct(self, target_peer_id: str, payload: Any):
        await self._bus.put((self.peer_id, f"direct-{target_peer_id}", payload))

class P2PStream:
    def __init__(self, manager: P2PManager, target_id: str):
        self.manager = manager
        self.target_id = target_id
    async def write(self, data: bytes):
        await self.manager.send_direct(self.target_id, ("CHUNK", data))
    async def close(self):
        await self.manager.send_direct(self.target_id, ("EOF", None))
