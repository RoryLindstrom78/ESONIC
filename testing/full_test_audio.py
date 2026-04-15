import sys
import os
import asyncio
sys.dont_write_bytecode = True #no pycache folders


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from state.audio import ContinuousMIDIController

# if in loopMIDI you created a port called "PythonMIDI", this will connect to it. If you named it something else.
PORT_NAME = 'PythonMIDI 1' # includes a 1 at the end (for some reason neccesary)
ARPEG_PORT_NAME = 'PythonMIDI2 2' #second port for arpeggios, includes a 2 at the end
BUTTON_PORT_NAME = 'PythonMIDI3 3' #third port for button notes(the lead), includes a 3 at the end
    
async def test_bass_only(controller):
    """Simulates turning only the bass knob up and down."""
    print("Starting Bass Sweep Test (Inversion locked)...")
    await asyncio.sleep(2) 
    
    # simulates turning a knob up from -180 to 180
    for angle in range(-180, 180):
        # We only pass bass_angle. Inversion stays at its default.
        controller.update(bass_angle=angle) 
        await asyncio.sleep(0.02) 
            
    # simulates turning it back down to -180
    for angle in range(180, -181, -1):
        controller.update(bass_angle=angle)
        await asyncio.sleep(0.02)
        
    print("Bass Simulation complete.")

async def test_inversion_only(controller):
    """Simulates twisting the wrist while the bass note is locked."""
    print("Starting Inversion Sweep Test (Bass locked)...")
    await asyncio.sleep(2)
    
    fixed_bass_angle = 0
    
    for wrist_angle in range(-180, 181, 2):
        controller.update(bass_angle=fixed_bass_angle, inversion_angle=wrist_angle)
        print(f"Wrist Angle: {wrist_angle:>4} degrees  -->  Inversion State: {controller.current_inversion}")
        await asyncio.sleep(0.05)

    print("Inversion test complete!")

async def test_both(controller):
    """Simulates moving the arm (bass) and twisting the wrist (inversion) simultaneously."""
    print("Starting Combined Sweep Test...")
    await asyncio.sleep(2)
    
    # Here we map both to change over time.
    for angle in range(-180, 180):
        # We make the wrist twist twice as fast as the arm moves so you can 
        # clearly hear the inversions flipping over the changing bass notes!
        wrist_angle = (angle * 2) % 360 - 180
        
        controller.update(bass_angle=angle, inversion_angle=wrist_angle)
        await asyncio.sleep(0.02)

    print("Combined test complete!")

async def main():
    # C major scale from C3 excluding the 7th (B) for a more "modal" sound
    scale = [48, 50, 52, 53, 55, 57]
    
    controller = ContinuousMIDIController(
        port_name=PORT_NAME,
        arpeg_port_name=ARPEG_PORT_NAME,
        button_port_name=BUTTON_PORT_NAME,
        min_val=-180,
        max_val=180,
        scale=scale
    )
    
    try:
        
        # TEST OPTIONS: (uncomment one at a time)
        # test Bass Only
        # simulate_task = asyncio.create_task(test_bass_only(controller))
        
        # test Inversion Only
        simulate_task = asyncio.create_task(test_inversion_only(controller))
        
        # test Both Angles Simultaneously
        #simulate_task = asyncio.create_task(test_both(controller))

        # start the arpeggiator loop
        arpeg_task = asyncio.create_task(controller.update_arpeggio(bpm=500))
        
        # wait for whichever simulation you uncommented to finish
        await simulate_task
        
        # cancel the arpeggio task since the simulation is done
        arpeg_task.cancel()
        
    except KeyboardInterrupt:
        print("\nstopping simulation...")
    finally:
        # closes code (important!)
        controller.close()
        print("complete, port closed")

if __name__ == "__main__":
    asyncio.run(main())