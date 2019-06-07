#!/usr/bin/python3
from controllers import BaseActor
from models import States
from random import random, choice


class MachineRandomActor(BaseActor):
    __selected_pawn = None
    __selected_move = None

    def __init__(self, name, state):
        super().__init__(name, state)

    def take_turn(self):
        self.__do_step_choose_strategically()

    def __do_step_choose_strategically(self):
        pawn = choice(list(self._state.game.engine.get_movable_pawns()))
        move = choice(self._state.game.engine.get_moves_for_pawn(pawn))

        self._state.game.engine.do_move(pawn, move)

        pawnText = self._gui._map_field_coordinates_to_text(pawn)
        moveText = self._gui._map_field_coordinates_to_text(move)
        history_text = "Player " + self._name + " moved " + \
            pawnText + " to " + moveText
        self._state.game.history.append(history_text)

        if self._state.game.engine.is_terminal():
            self._state = States.WIN
            self._state.feedback += " Game finished. "
            return
        else:
            self._state.game.engine.to_next_turn()
            return
