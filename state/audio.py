import asyncio
from logging import root
import mido


class ContinuousMIDIController:
    def __init__(self, port_name, arpeg_port_name, button_port_name, min_val=-180, max_val=180, scale=None, numofinversions=6):
        self.min_val = min_val # minimum angle value expected (e.g., -180 degrees)
        self.max_val = max_val # maximum angle value expected (e.g., 180 degrees)

        # defaults to the C major scale if a scale is not provided
        self.scale = scale if scale is not None else [36, 38, 40, 41, 43, 45, 47, 48] 
        self.starting_note = self.scale[0] # the lowest note in the scale, used for button note calculations
        
        # notes for the buttons 
        self.button_scale_intervals = [12, 14, 16, 19, 21, 23]
        self.prev_button_notes = []
        self.button_notes = [60, 62, 64, 67, 69, 71]
        
        self.port_name = port_name
        self.port = None

        self.arpeg_port_name = arpeg_port_name
        self.arpeg_port = None

        self.button_port_name = button_port_name
        self.button_port = None
        
        # has the current note so it can sustain it until the next change
        self.current_note = None 

        #arpeggio settings
        self.numofinversions = numofinversions
        self.current_inversion = 0
        
        self._connect_midi()
    
    def build_arpeggio(self, root):
        """
        Builds the arpeggio based on the current root note and the defined intervals. 
        The patterns can be changed to create different arpeggio shapes.
        """

        try:
            root_index = self.scale.index(root)
        except ValueError:
            print(f"Root note {root} is not in the scale.")
            return []

        patterns = {
            0: [0, 2, 4, 7, 11],  # 1st Note (I chord): maj9
            1: [0, 3, 5, 7, 10],  # 2nd Note (ii chord): min7 add 11
            2: [0, 3, 5, 7, 10],  # 3rd Note (iii chord): min7 add 11
            3: [0, 2, 4, 7, 11],  # 4th Note (IV chord): maj9 
            4: [0, 2, 4, 5, 7],   # 5th Note (V chord): sus2 add 11
            5: [0, 3, 5, 7, 10],  # 6th Note (vi chord): min7 add 11
        }

        # 5-note bass interval
        intervals = patterns.get(root_index, [0, 2, 4, 7])  # default to a simple major arpeggio if something goes wrong
        
        # extends all the chords by 3 octaves
        extended_intervals = (
            intervals + 
            [i + 12 for i in intervals] +  # octave 2
            [i + 24 for i in intervals] +  # octave 3
            [i + 36 for i in intervals]    # octave 4 (Safety buffer)
        )

        # gets the state of the inversion
        inv = self.current_inversion

        sliced_intervals = extended_intervals[inv:inv + 5]  # Get 5 notes for the arpeggio based on the current inversion        
        
        return [root + interval for interval in sliced_intervals]

    def build_button_notes(self, root):
        return [root + interval for interval in self.button_scale_intervals]

    def _connect_midi(self):
        """
        Connects to the specified MIDI output port. Make sure to have a virtual MIDI port set up (like loopMIDI) and that your DAW is listening to it.
        """
        try:
            self.port = mido.open_output(self.port_name)
            print(f"[{self.port_name}] Successfully connected!")
            self.arpeg_port = mido.open_output(self.arpeg_port_name)
            print(f"[{self.arpeg_port_name}] Successfully connected!")
            self.button_port = mido.open_output(self.button_port_name)
            print(f"[{self.button_port_name}] Successfully connected!")
        except OSError:
            print(f"[{self.port_name}] ERROR: Could not find port.")
            print(f"[{self.arpeg_port_name}] ERROR: Could not find port.")
            print(f"[{self.button_port_name}] ERROR: Could not find port.")

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
    
    def value_to_inversion(self, value):
        """
        Converts the angle value to a number of inversions for the arpeggio based on the defined range and number of inversions
        """
        
        value = max(self.min_val, min(value, self.max_val))
        interval_size = (self.max_val - self.min_val) / self.numofinversions
        
        inversions = int((value - self.min_val) / interval_size)
        inversions = min(inversions, self.numofinversions - 1)
        
        return inversions

    def update(self, bass_angle, inversion_angle=None):
        """
        Updates the current note if it is different from the last one.
        """

        if not self.port:
            return

        # checks for inversion changes
        if inversion_angle is not None:
            self.current_inversion = self.value_to_inversion(inversion_angle)

        # checks what note should be played
        new_note = self.value_to_note(bass_angle)
        reset_notes = False

        # only send MIDI messages if the note has changed
        if new_note != self.current_note:
            reset_notes = True
            # removes old note
            if self.current_note is not None:
                self.port.send(mido.Message('note_off', note=self.current_note, velocity=0))
            
            # plays new note
            self.port.send(mido.Message('note_on', note=new_note, velocity=100))
            
            # test print confirmation
            print(f"Input crossed threshold! Value: {bass_angle:.1f} -> Playing Note: {new_note}")
            
            # updates note
            self.current_note = new_note

        return reset_notes

    async def update_arpeggio(self, bpm=120):
        """
        Continuously plays an arpeggio based on the current note.
        """

        if not self.arpeg_port:
            return

        beat_time = 12.5 / bpm

        while True:
            if self.current_note is None:
                await asyncio.sleep(0.01)
                continue

            notes = self.build_arpeggio(self.current_note)

            for note in notes:
                self.arpeg_port.send(mido.Message('note_on', note=note, velocity=100))
                await asyncio.sleep(beat_time / 2)
                self.arpeg_port.send(mido.Message('note_off', note=note, velocity=0))

    def play_button_note_on(self, glove_id, note):
        print(self.button_notes[note])

        if not self.button_port:
            return
        
        if self.current_note is None:
            return

        #self.button_notes = self.build_button_notes(self.current_note)
       #if (glove_id == 1 or glove_id == 3): 
        if (glove_id == 1 or glove_id == 3):
            # First three notes of scale
            self.button_port.send(mido.Message('note_on', note=self.button_notes[note], velocity=100))
        else:
            # Last three notes of scale
            self.button_port.send(mido.Message('note_on', note=self.button_notes[note + 3], velocity=100))

    def play_button_note_off(self, glove_id, note):
        print(self.button_notes[note])

        if not self.button_port:
            return
        
        if self.current_note is None:
            return

        #self.button_notes = self.build_button_notes(self.current_note)

        if (glove_id == 1 or glove_id == 3):
            # First three notes of scale
            self.button_port.send(mido.Message('note_off', note=self.button_notes[note], velocity=0))
        else:
            # Last three notes of scale
            self.button_port.send(mido.Message('note_off', note=self.button_notes[note + 3], velocity=0))

    def reset_all_buttons(self):
        if not self.button_port:
            return
        
        for note in self.button_notes:
            self.button_port.send(mido.Message('note_off', note=note, velocity=0))




    def stop_all(self):
        """
        Stops the note that is currently playing so it doesn't drone forever
        """
        
        if self.current_note is not None and self.port:
            self.port.send(mido.Message('note_off', note=self.current_note, velocity=0))
            self.arpeg_port.send(mido.Message('note_off', note=self.current_note, velocity=0))
            self.current_note = None
            
    def close(self):
        self.stop_all()
        if self.port: self.port.close()
        if self.arpeg_port: self.arpeg_port.close()
        if self.button_port: self.button_port.close()
