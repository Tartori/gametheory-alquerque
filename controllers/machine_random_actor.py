#!/usr/bin/python3
from controllers import BaseActor


class MachineRandomActor(BaseActor):

    def __init__(self, name, current):
        super().__init__(name, current)

    def take_turn(self):
        pass
