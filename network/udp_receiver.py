import socket       # For transfer over udp 
import json         # For processing accelerometer data
import asyncio      # For concurrency 
import time
import math
import queue


class UDPServer(asyncio.DatagramProtocol):
    """
        UDP Server running that will receive ESP32 data.
        Data should be sent as JSON in the following format:

        {
            "id": 1,
            "t": 1708140034.123,
            "ax": 0.12,
            "ay": -0.87,
            "az": 9.81
        }

        Where:
            id: Device ID (1-4)
            t: timestamp
            ax: x-axis acceleration
            ay: y-axis acceleration
            az: z-axis acceleration
    """

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






