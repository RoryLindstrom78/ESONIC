import socket       # For transfer over udp 
import json         # For processing accelerometer data
import asyncio      # For concurrency 
import time
import math
import queue
import device_manager
import device_state


UDP_PORT = 5005

device = device_manager.DeviceManager()

class UDPServer(asyncio.DatagramProtocol):
    """
        UDP Server running that will receive ESP32 data.
        Data should be sent as JSON in the following format:

        CORRESPONDING HANDS:
        - id 1 is person 1 left hand
        - id 2 is person 2 right hand
        - id 3 is person 1 right hand
        - id 4 is person 2 left hand

        LEFT HAND PERSON 1 JSON:

        {
            "id": 1,
            "ax": 0.12,
            "ay": -0.87,
            "az": 9.81,
            "gx": 0,
            "gy": 0,
            "gz": 0,
            "pinkyL" : 0,
            "ringL" : 0, 
            "middleL" : 0,
            "indexL" : 0 
        }

        RIGHT HAND PERSON 2 JSON:

        {
            "id": 2,
            "ax": 0.12,
            "ay": -0.87,
            "az": 9.81,
            "gx": 0,
            "gy": 0,
            "gz": 0,
            "pinkyR" : 0,
            "ringR" : 0, 
            "middleR" : 0,
            "indexR" : 0 
        }

        RIGHT HAND PERSON 1 JSON:

        {
            "id": 3,
            "ax": 0.12,
            "ay": -0.87,
            "az": 9.81,
            "gx": 0,
            "gy": 0,
            "gz": 0,
            "pinkyL" : 0,
            "ringL" : 0, 
            "middleL" : 0,
            "indexL" : 0 
        }

        LEFT HAND PERSON 2 JSON:

        {
            "id": 4,
            "ax": 0.12,
            "ay": -0.87,
            "az": 9.81,
            "gx": 0,
            "gy": 0,
            "gz": 0,
            "pinkyR" : 0,
            "ringR" : 0, 
            "middleR" : 0,
            "indexR" : 0 
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


try:
    asyncio.run(main())
except KeyboardInterrupt:
    device.midi_controller.close()
    print("\nShutting down server...")







