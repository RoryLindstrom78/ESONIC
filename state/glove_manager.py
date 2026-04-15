class GloveManager:
    def __init__(self):
        self.ax = 0
        self.ay = 0
        self.az = 0
        self.pinky = 0
        self.ring = 0
        self.middle = 0
        self.index = 0
        # Buttons initialized as an array of 5
        self.buttons = {i: False for i in range(1, 6)}
        self.prev_buttons = [0 for i in range(4)]

    def update_data(self, ax, ay, az, pinky, ring, middle, index):
        self.ax = ax
        self.ay = ay
        self.az = az
        self.pinky = pinky
        self.ring = ring
        self.middle = middle
        self.index = index

    def check_buttons(self, id):
        # call check button function for each respective finger, build an array of 0s or 1s to represent button states, return that array
        button_states = []

        if (id == 1 or id == 3):
            button_states.append(self.ring)
            button_states.append(self.middle)
            button_states.append(self.index)
            button_states.append(self.pinky)
        else:
            button_states.append(self.index)
            button_states.append(self.middle)
            button_states.append(self.ring)
            button_states.append(self.pinky)

        return button_states
    
    
    def num_to_finger(self, num):
        if num == 0:
            return self.ring
        elif num == 1:
            return self.middle
        else:
            return self.index
