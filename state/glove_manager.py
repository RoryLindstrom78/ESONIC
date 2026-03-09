class GloveManager:
    def __init__(self):
        self.ax = 0
        self.ay = 0
        self.az = 0
        # Buttons initialized as an array of 5
        self.buttons = {i: False for i in range(1, 6)}

    def update_data(self, ax, ay, az):
        self.ax = ax
        self.ay = ay
        self.az = az


