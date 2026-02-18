import device_state
import asyncio

class DeviceManager:
    """
    DeviceManager: Handles state, IO updates, and angle calculations

    :param glove1-glove4: glove_manager objects encapsulating glove data (ax, ay, az, button responses)
    :param _angle_semaphore: handles checking whether or not we should calculate angles. Probably over engineered but prevents busy waiting

    """
    def __init__(self, glove1, glove2, glove3, glove4):
        self.state = device_state.InstrumentState.INIT
        # Gloves (1s angle is calculated with 3, 2s is calculated with 4)
        self.glove1 = glove1
        self.glove2 = glove2
        self.glove3 = glove3
        self.glove4 = glove4

        # angle calculations dependent on this semaphore. We only calculate when we release it.
        self._angle_semaphore = asyncio.Semaphore(0)

    def new_state(self, new_state):
        """
        Docstring for new_state
        
        :param new_state: new state we would like to update DeviceManager to
        """

        # Triggers angle calculation loop
        if new_state == device_state.InstrumentState.MOVEMENT and self.state != device_state.InstrumentState.MOVEMENT:
            self._angle_semaphore.release()
        
        # Regardless we update the state
        self.state = new_state


    async def monitor_state(self):
        """
        Continuously runs, checks if in movement state for angle calculations without busy waiting.
        """
        while True:
            # Wait until there's at least one "ticket"
            await self._angle_semaphore.acquire()
            # Continuously calculate angle while in "MOVEMENT" state
            while self.state == device_state.InstrumentState.MOVEMENT:
                self.calculate_angle()
                await asyncio.sleep(0.01) # slight delay between calculations

    def calculate_angle(self):
        print("Calculating Angle")
            
