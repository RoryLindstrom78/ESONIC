import device_state
import asyncio
import glove_manager
import math
import audio


class DeviceManager:
    """
    DeviceManager: Handles state, IO updates, and angle calculations

    :param glove1-glove4: glove_manager objects encapsulating glove data (ax, ay, az, button responses)
    :param _angle_semaphore: handles checking whether or not we should calculate angles. Probably over engineered but prevents busy waiting

    """

    def __init__(self):
        self.state = device_state.InstrumentState.INIT

        # Audio
        self.audio = True # Defaults to true, can be set to false for testing without MIDI controller
        #self.scale = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
        self.scale = [36, 38, 40, 41, 43, 45, 47, 48]
        self.PORT_NAME = 'PythonMIDI 1'
        self.ARPEG_PORT_NAME = 'PythonMIDI2 2'
        self.BUTTON_PORT_NAME = 'PythonMIDI3 3'
        self.midi_controller = audio.ContinuousMIDIController(port_name=self.PORT_NAME, arpeg_port_name=self.ARPEG_PORT_NAME, button_port_name=self.BUTTON_PORT_NAME, min_val=-180, max_val=180, scale=self.scale)

        # Gloves (just constructed as a list of GloveManagers)
        self.gloves = {i: glove_manager.GloveManager() for i in range(4)}

        # angle calculations dependent on this semaphore. We only calculate when we release it.
        self._angle_semaphore = asyncio.Semaphore(0)

    async def start(self):
        asyncio.create_task(self.midi_controller.update_arpeggio())

    
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

            while self.state == device_state.InstrumentState.MOVEMENT:
                angle = self.calculate_angle()
                if self.audio and angle is not None:
                    self.midi_controller.update(angle)

                for i in range(len(self.gloves)):
                    glove = self.gloves[i]
                    button_states = glove.check_buttons()
                    for j in range(3):

                        if button_states[j] == 1:
                            if (glove.prev_buttons[j] == 1):
                                continue
                            glove.prev_buttons[j] = 1
                            self.midi_controller.play_button_note_on(glove_id=i+1, note=j)
                        else:
                            if (glove.prev_buttons[j] == 0):
                                continue
                            glove.prev_buttons[j] = 0
                            self.midi_controller.play_button_note_off(glove_id=i+1, note=j)

                await asyncio.sleep(0.01) # slight delay between calculations
                

    def calculate_angle(self):
        # Gonna test by calculating angle between gloves id 1 and id 2 for now
        g0 = self.gloves[0]
        g1 = self.gloves[1]

        # Compute forward tilt for g0
        mag0 = (g0.ax * g0.ax + g0.ay * g0.ay + g0.az * g0.az) ** 0.5
        # Compute forward tilt for g1
        mag1 = (g1.ax * g1.ax + g1.ay * g1.ay + g1.az * g1.az) ** 0.5
        
        # Prevent divide by zero error
        if (mag0 == 0 or mag1 == 0):
            return None
        
        # Compute tilt
        tilt0 = math.atan2(g0.az / mag0, g0.ax / mag0)
        tilt1 = math.atan2(g1.az / mag1, g1.ax / mag1)

        # Compute angle
        angle = tilt0 - tilt1
        angle = math.degrees(angle)
        #print("Angle: ", angle)

        return angle


    def new_glove_data(self, gloveID, ax, ay, az, pinky, ring, middle, index):
        self.gloves[gloveID - 1].update_data(ax, ay, az, pinky, ring, middle, index)
