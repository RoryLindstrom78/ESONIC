import json
import asyncio
import serial_asyncio
import device_manager
import device_state


# ============================================================
# Device setup
# ============================================================

device = device_manager.DeviceManager()


# ============================================================
# UDPServer (NOW SERIAL, NAME KEPT FOR COMPATIBILITY)
# ============================================================

class UDPServer(asyncio.Protocol):
    """
    NOTE:
    Class name preserved so existing code does not break.

<<<<<<< HEAD
    This now handles SERIAL input instead of UDP.
    Each ESP32 must send newline-delimited JSON.
=======
        CORRESPONDING HANDS:
        - id 1 is person 1 left hand
        - id 2 is person 2 right hand
        - id 3 is person 2 left hand
        - id 4 is person 1 right hand

        ANY HAND OF ANY PERSON:
        {
            "id": 1,    // changes per person/hand
            "ax": 0.12,
            "ay": -0.87,
            "az": 9.81,
            "gx": 0,
            "gy": 0,
            "gz": 0,
            "index" : 0,
            "middle" : 0, 
            "ring" : 0,
            "pinky" : 0 
        }

        Where:
            id: Device ID (1-4)
            ax: x-axis acceleration
            ay: y-axis acceleration
            az: z-axis acceleration
            gx: x-axis gyro
            gy: y-axis gyro
            gz: z-axis gyro
            index:  index button
            middle: middle button
            ring:   ring button
            pinky:  pinky button
>>>>>>> 8048c46a5d35b984e72a3259b8802b21f76992c2
    """

    def __init__(self, port_name: str):
        self.port_name = port_name
        self.buffer = ""

    # Serial connection opened
    def connection_made(self, transport):
        self.transport = transport
        print(f"[INFO] Connected to {self.port_name}")

    # Data received from serial port
    def data_received(self, data: bytes):
        self.buffer += data.decode(errors="ignore")

        # Serial is a stream → split by newline
        while "\n" in self.buffer:
            line, self.buffer = self.buffer.split("\n", 1)
            line = line.strip()

            if line:
                self.handle_message(line)

    # Same logic you previously had in datagram_received
    def handle_message(self, line: str):
        try:
            message = json.loads(line)

            device.new_glove_data(
                message["id"],
                message["ax"],
                message["ay"],
                message["az"],
                message["pinky"],
                message["ring"],
                message["middle"],
                message["index"]
            )

            if device.state == device_state.InstrumentState.INIT:
                device.new_state(device_state.InstrumentState.MOVEMENT)

        except Exception as e:
            print(f"[{self.port_name}] Bad packet:", e)
            print(f"[{self.port_name}] Raw:", line)

    def connection_lost(self, exc):
        print(f"[INFO] Disconnected from {self.port_name}")


# ============================================================
# Main Async Entry Point
# ============================================================

async def main():
    loop = asyncio.get_running_loop()

    print("[INFO] Starting serial receivers...")

    # ESP32 #1 → COM3
    await serial_asyncio.create_serial_connection(
        loop,
        lambda: UDPServer("COM3"),
        "COM3",
        baudrate=115200
    )



    print("[INFO] Serial connections established")

    # Start device logic
    await device.start()
    asyncio.create_task(device.monitor_state())

    print("[INFO] Device monitoring started")

    # Run forever
    await asyncio.Future()


# ============================================================
# Program Runner
# ============================================================

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\n[INFO] Shutting down...")
    device.midi_controller.close()
