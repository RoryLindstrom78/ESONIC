from enum import Enum


class InstrumentState(Enum):
    """
    Handles the three different "states" of our instrument

    States:
        MOVEMENT: Hands may move freely to change pitch, lead notes may be played
        LOCKED: Hand movements do not effect pitch, lead notes still playable
        MODULATION: Hand movements do not effect pitch, lead notes serve modulation purposes
    """

    MOVEMENT = 1
    LOCKED  = 2
    MODULATION = 3

