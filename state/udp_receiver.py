import socket       # For transfer over udp 
import json         # For processing accelerometer data
import asyncio      # For concurrency 
import time
import math
import queue
import device_manager
import device_state
<<<<<<< HEAD
=======
import audio
>>>>>>> 4033f2e63c3755690bc4bae040d130392edf8aee


UDP_PORT = 5005

device = device_manager.DeviceManager()

class UDPServer(asyncio.DatagramProtocol):
    """
        UDP Server running that will receive ESP32 data.
        Data should be sent as JSON in the following format:

        {
            "id": 1,
            "ax": 0.12,
            "ay": -0.87,
            "az": 9.81,
            "gx": 0,
            "gy": 0,
            "gz": 0
        }

        Where:
            id: Device ID (1-4)
            ax: x-axis acceleration
            ay: y-axis acceleration
            az: z-axis acceleration
            gx: x-axis gyro
            gy: y-axis gyro
            gz: z-axis gyro


        Hello rory if you ever see this :P
    """

    def datagram_received(self, data, addr):
        try:
            message = json.loads(data.decode())
<<<<<<< HEAD
=======
            print(f"Got data from ID: {message['id']}") # <--- ADD THIS LINE
>>>>>>> 4033f2e63c3755690bc4bae040d130392edf8aee

            device.new_glove_data(
                message["id"],
                message["ax"],
                message["ay"],
                message["az"]
            )

            if device.state == device_state.InstrumentState.INIT:
                device.new_state(device_state.InstrumentState.MOVEMENT)

        except Exception as e:
            print("Bad packet:", e)

async def main():
    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        UDPServer,
        local_addr=('0.0.0.0', UDP_PORT)
    )
    print("Server Starting")
    
    # Start the angle monitoring loop
    asyncio.create_task(device.monitor_state())
    await asyncio.Future()  # run forever

asyncio.run(main())






