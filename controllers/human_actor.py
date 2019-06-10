#!/usr/bin/python3
from controllers import BaseActor
from models import States, Commands


class HumanActor(BaseActor):
    """
    This controller takes over during a game play when its the turn
    of a human player. If there are two human players, each one has
    its own controller.
    """

    def __init__(self, name: str, state, playerId):
        super().__init__(name, state, playerId)
        self._state.activity = States.CHOOSE_PAWN

    def take_turn(self):
        """
        Called when its the turn of the actor this controller represents.
        Contains the loop of the user interacting with the application.
        """

        self._state.activity = States.CHOOSE_PAWN

        while True:
            try:
                if self._state.activity == States.CHOOSE_PAWN:
                    self.__do_step_choose_pawn()
                    continue
                elif self._state.activity == States.CHOOSE_MOVE:
                    self.__do_step_choose_move()
                    continue
                else:
                    return
            except:
                pass

    def __do_step_choose_pawn(self):
        """
        The human player chooses which pawn to move.
        """
        params = self._prepare_values_to_be_rendered()
        params.instruction = "Which pawn do you want to move? "
        pawns = self._state.game.engine.get_movable_pawns()
        params.options.update(self._get_choosable_fields_as_options(pawns))
        self._gui.print_screen(params)

        input = self._read_input()

        if not self._handle_common_inputs(input, params.options):
            field = self._map_field_text_to_coordinates(input)
            self._selected_pawn = field
            self._state.activity = States.CHOOSE_MOVE
            self._feedback = "You want to move pawn " + input + ". "

    def __do_step_choose_move(self):
        """
        The human player chooses where to move the chosen pawn to.
        """
        params = self._prepare_values_to_be_rendered()
        params.instruction = "Where would you like to move the pawn?"
        pawn = self._selected_pawn
        moves = self._state.game.engine.get_moves_for_pawn(pawn)
        params.options.update(self._get_choosable_fields_as_options(moves))
        params.board = self._state.game.engine.get_bord_with_moves(pawn)
        self._gui.print_screen(params)

        input = self._read_input()

        if not self._handle_common_inputs(input, params.options):
            field = self._map_field_text_to_coordinates(input)
            self._selected_move = field
            self._do_draw()
