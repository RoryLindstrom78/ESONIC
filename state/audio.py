import mido

class ContinuousMIDIController:
    def __init__(self, port_name, min_val=-180, max_val=180, scale=None):
        self.min_val = min_val # minimum angle value expected (e.g., -180 degrees)
        self.max_val = max_val # maximum angle value expected (e.g., 180 degrees)

        # defaults to the C major scale if a scale is not provided
        self.scale = scale if scale is not None else [60, 62, 64, 65, 67, 69, 71, 72] 
        
        self.port_name = port_name
        self.port = None
        
        # has the current note so it can sustain it until the next change
        self.current_note = None 
        
        self._connect_midi()

    def _connect_midi(self):
        """
        Connects to the specified MIDI output port. Make sure to have a virtual MIDI port set up (like loopMIDI) and that your DAW is listening to it.
        """
        try:
            self.port = mido.open_output(self.port_name)
            print(f"[{self.port_name}] Successfully connected!")
        except OSError:
            print(f"[{self.port_name}] ERROR: Could not find port.")

    def value_to_note(self, value):
        """
        Converts the angle value to a MIDI note based on the defined range and scale
        """
        
        value = max(self.min_val, min(value, self.max_val))
        num_intervals = len(self.scale)
        interval_size = (self.max_val - self.min_val) / num_intervals
        
        index = int((value - self.min_val) / interval_size)
        index = min(index, num_intervals - 1)
        
        return self.scale[index]

    def update(self, value):
        """
        Updates the current note if it is different from the last one.
        """

        if not self.port:
            return

        # checks what note should be played
        new_note = self.value_to_note(value)

        # only send MIDI messages if the note has changed
        if new_note != self.current_note:
            
            # removes old note
            if self.current_note is not None:
                self.port.send(mido.Message('note_off', note=self.current_note, velocity=0))
            
            # plays new note
            self.port.send(mido.Message('note_on', note=new_note, velocity=100))
            
            # test print confirmation 
            print(f"Input crossed threshold! Value: {value:.1f} -> Playing Note: {new_note}")
            
            # updates note
            self.current_note = new_note

    def stop_all(self):
        """
        Stops the note that is currently playing so it doesn't drone forever
        """
        
        if self.current_note is not None and self.port:
            self.port.send(mido.Message('note_off', note=self.current_note, velocity=0))
            self.current_note = None
            
    def close(self):
        self.stop_all()
        if self.port:
            self.port.close()
