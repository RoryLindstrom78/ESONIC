import socket       # For transfer over udp 
import json         # For processing accelerometer data
import asyncio      # For concurrency 
import time
import math
import queue


class UDPServer(asyncio.DatagramProtocol):
    def datagram_received(self, data, addr):
        message = json.loads(data.decode())
        print(message)

async def main():
    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        UDPServer,
        local_addr=('0.0.0.0', 5005)
    )
    print("Server Starting")
    await asyncio.Future()  # run forever

asyncio.run(main())






