import time
import sys
import os
sys.dont_write_bytecode = True #no pycache folders


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from state.audio import ContinuousMIDIController

# if in loopMIDI you created a port called "PythonMIDI", this will connect to it. If you named it something else.
PORT_NAME = 'PythonMIDI 1' # includes a 1 at the end (for some reason neccesary)
scale = [60, 62, 64, 67, 69, 71, 72] # C Major scale minus 4th (60 = C4, 62 = D4, 64 = E4, 67 = G4, 69 = A4, 71 = B4, 72 = C5)
scale = [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72] # chromatic scale from C4 to C5
controller = ContinuousMIDIController(port_name=PORT_NAME, min_val=-180, max_val=180, scale=scale)
    
time.sleep(2)
    
try:
        # simulates turning a knob up from -180 to 180
    for angle in range(-180, 180):
        controller.update(angle)
        time.sleep(0.02) # simulates data coming in every 20ms (50Hz)
            
        # simulates turning it back down to -180
    for angle in range(180, -181, -1):
        controller.update(angle)
        time.sleep(0.02)
            
except KeyboardInterrupt:
    print("\nstopping simulation...")
finally:
    # closes code (important!)
    controller.close()
    print("complete, port closed")