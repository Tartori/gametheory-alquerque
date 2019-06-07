#!/usr/bin/python3
from controllers import BaseActor
from models import States, Commands


class HumanActor(BaseActor):

    # Describes the currently selected pawn in format A0.
    __selected_pawn = None

    # Describes the currently selected move for the selected pawn
    # in format A0.
    __selected_move = None

    def __init__(self, name, state):
        super().__init__(name, state)
        self._state.activity = States.CHOOSE_PAWN

    def take_turn(self):
        """
        The loop of the controller for the human actor.
        Contains the loop of the user interacting with the application.

        return: void.
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
        Part of the game loop, if the human moves.
        The current human player chooses which pawn to move.
        """
        params = self._prepare_values_to_be_rendered()
        params.instruction = "Which pawn do you want to move? "
        pawns = self._state.game.engine.get_movable_pawns()
        params.options.update(self._get_choosable_fields_as_options(pawns))
        self._gui.print_screen(params)

        input = self._read_input()

        if input == Commands.QUIT_APP:
            self._feedback = None
            self._state.activity = States.BYE
            return

        elif input in params.options:
            self._selected_pawn = input
            self._state.activity = States.CHOOSE_MOVE
            self._feedback = "You want to move pawn " + input + ". "
            return

        else:
            self._feedback = "Bad input! "
            return

    def __do_step_choose_move(self):
        """
        Part of the game loop.
        The current player (human or machine) chooses
        where to move the chosen pawn to.
        """
        params = self._prepare_values_to_be_rendered()
        params.instruction = "Where would you like to move the pawn?"
        pawn = self._selected_pawn
        pawnField = self._map_field_text_to_coordinates(pawn)
        moves = self._state.game.engine.get_moves_for_pawn(pawnField)
        params.options.update(self._get_choosable_fields_as_options(moves))
        params.board = self._state.game.engine.get_bord_with_moves(pawnField)
        self._gui.print_screen(params)

        input = self._read_input()

        if input == Commands.QUIT_APP:
            self._feedback = None
            self._state.activity = States.BYE
            return

        elif input in params.options:
            self._selected_move = input
            pawn = self._map_field_text_to_coordinates(self._selected_pawn)
            move = self._map_field_text_to_coordinates(self._selected_move)
            self._state.game.engine.do_move(pawn, move)
            history_text = "Player " + self._name + " moved " + \
                self._selected_pawn + " to " + self._selected_move
            self._state.game.history.append(history_text)

            self._state.activity = States.TAKE_TURN
            return

        else:
            self._feedback = "Bad input! "
            return
