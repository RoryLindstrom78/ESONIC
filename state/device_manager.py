import device_state
import asyncio

class DeviceManager:
    def __init__(self):
        self.state = device_state.InstrumentState.INIT
        # Gloves (1s angle is calculated with 3, 2s is calculated with 4)
        self.glove1 = None
        self.glove2 = None
        self.glove3 = None
        self.glove4 = None

        # angle calculations dependent on this semaphore. We only calculate when we release it.
        self._angle_semaphore = asyncio.Semaphore(0)

    def new_state(self, new_state):
        # Triggers angle calculation loop
        if new_state == device_state.InstrumentState.MOVEMENT and self.state != device_state.InstrumentState.MOVEMENT:
            self._angle_semaphore.release()
        
        # Regardless we update the state
        self.state = new_state


    async def monitor_state(self):
        while True:
            # Wait until there's at least one "ticket"
            await self._angle_semaphore.acquire()
            # Continuously calculate angle while in "MOVEMENT" state
            while self.state == device_state.InstrumentState.MOVEMENT:
                self.calculate_angle()
                await asyncio.sleep(0.01) # slight delay between calculations

    def calculate_angle(self):
        print("Calculating Angle")
            
