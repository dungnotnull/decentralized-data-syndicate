import asyncio
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from protocol_pb2 import DataNeedSpec

async def peer_listener(port, on_message, started_event):
    async def _handle_peer(reader, writer):
        data = await reader.read(4096)
        if data:
            on_message(data)
        writer.close()
        await writer.wait_closed()

    server = await asyncio.start_server(_handle_peer, host='127.0.0.1', port=port)
    started_event.set()
    try:
        await asyncio.Future()
    finally:
        server.close()
        await server.wait_closed()

async def peer_dial(host, port, message_bytes):
    reader, writer = await asyncio.open_connection(host, port)
    writer.write(message_bytes)
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def test_main():
    received = []

    def on_message(data):
        msg = DataNeedSpec()
        msg.ParseFromString(data)
        received.append(msg)

    started = asyncio.Event()
    server_task = asyncio.create_task(peer_listener(19090, on_message, started))
    await started.wait()

    spec = DataNeedSpec()
    spec.request_id = "req-001"
    spec.data_type = "api_behavior_log"
    spec.min_rows = 5000
    spec.max_null_rate_permille = 50
    spec.required_columns.extend(["timestamp", "endpoint", "status_code"])
    spec.budget_usdc_milli = 10000
    spec.description = "NestJS backend behavior logs"
    spec.timestamp = 1717689600

    await peer_dial('127.0.0.1', 19090, spec.SerializeToString())
    await asyncio.sleep(0.3)
    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        pass

    assert len(received) == 1
    r = received[0]
    assert r.data_type == "api_behavior_log"
    assert r.min_rows == 5000
    assert r.request_id == "req-001"
    print("PASS: Two simulated peers exchanged DataNeedSpec over Protobuf")

if __name__ == "__main__":
    asyncio.run(test_main())
