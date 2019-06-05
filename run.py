#!/usr/bin/python3


import re

from gui import Output, ScreenParameters
from input import map_field_text_to_coordinates, read_input
from definitions import Player
from machine import RandomMachine
from bauernschach import Bauernschach
from alquerque import Alquerque
from copy import deepcopy


class Games:
    ALQUERQUE = 0
    BAUERNSCHACH = 1


class States:
    CHOOSE_GAME = 0
    CHOOSE_BOARD_SIZE = 1
    CHOOSE_OPP_HUMAN_OR_MACHINE = 2
    CHOOSE_MACHINE_STRATEGY = 3
    CHOOSE_PLAYER_ORDER = 4
    START_GAME = 5
    TAKE_TURN = 6
    CHOOSE_PAWN = 7
    CHOOSE_MOVE = 8
    SWITCH_TURN = 9
    WIN = 10
    BYE = -1


class Commands:
    QUIT_APP = "X"
    CHOOSE_GAME_ALQUERQUE = "A"
    CHOOSE_GAME_BAUERNSCHACH = "B"
    CHOOSE_FIRST_PLAYER_ME = "M"
    CHOOSE_FIRST_PLAYER_OPPONENT = "P"
    CHOOSE_OPP_AS_HUMAN = "H"
    CHOOSE_OPP_AS_MACHINE = "C"
    CHOOSE_MACHINE_STRATEGY_RANDOM = "R"


class CurrentGame:
    game = None
    gameChoice = None
    playerToStartFirst = None
    boardSize = 4
    machine = None
    actors = {
        Player.USER: None,
        Player.OPP: None
    }
    currentActor = None
    waitingActor = None


class BaseActor:
    """
    Defines the common functionality that all types of player
    share. An actor is anyone who interacts with the gui and the game.
    Can be a human or machine player.
    """

    _state = None
    _name = None
    _game = None
    _history = None
    _gui = None
    # __is_first_player = None
    _feedback = None
    _sharedOptions = {
        Commands.QUIT_APP: "stops app",
    }

    def __init__(self, name, game, gui, history):
        self._name = name
        self._game = game
        self._gui = gui
        # self.__is_first_player = isFirstPlayer
        self._history = history

    def take_turn(self):
        pass

    def _prepare_values_to_be_rendered(self):
        """
        Helper function that initializes a new screen parameter object
        with default values.
        """
        values = ScreenParameters()
        if self._game is not None:
            values.game = self._game
            values.board = self._game.get_bord()
            values.moveHistory = self._game.get_move_history()
        # TODO: add player
        if self._feedback is not None:
            values.feedback = self._name + " " + self._feedback
            self.feedback = None
        values.options = deepcopy(self._sharedOptions)
        return values

    def _get_choosable_fields_as_options(self):
        """
        Helper function that converts fields to options.
        """
        fields = self._game.get_movable_pawns()
        fieldNames = self._gui.map_fields_coordinates_to_text(fields)
        options = {}
        for f in fieldNames:
            options[f] = ""
        return options


class HumanActor(BaseActor):

    __selected_pawn = None
    __selected_move = None

    def __init__(self, name, game, gui, history):
        super().__init__(name, game, gui, history)
        self._state = States.CHOOSE_PAWN

    def take_turn(self):
        """
        The loop of the controller for the human actor.
        Contains the loop of the user interacting with the application.

        return: void.
        """

        self._state = States.CHOOSE_PAWN

        while True:
            try:
                if self._state == States.CHOOSE_PAWN:
                    self.__do_step_choose_pawn()
                    continue
                elif self._state == States.CHOOSE_MOVE:
                    self.__do_step_choose_move()
                    continue
                else:
                    break
            except:
                pass

    def __do_step_choose_pawn(self):
        """
        Part of the game loop, if the human moves.
        The current human player chooses which pawn to move.
        """
        params = self._prepare_values_to_be_rendered()
        params.instruction = self._name + " Which pawn do you want to move? "
        params.options.update(self._get_choosable_fields_as_options())
        self._gui.print_screen(params)

        input = read_input()

        if input == Commands.QUIT_APP:
            self._feedback = None
            self._state = States.BYE
            return

        elif input in params.options:
            self._selected_pawn = input
            self._state = States.CHOOSE_MOVE
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
        params.instruction = self._name + " Where would you like to move the pawn?"
        pawnField = map_field_text_to_coordinates(self._selected_pawn)
        params.options.update(self._get_choosable_fields_as_options())
        params.board = self._game.get_bord_with_moves(pawnField)
        self._gui.print_screen(params)

        input = read_input()

        if input == Commands.QUIT_APP:
            self._feedback = None
            self._state = States.BYE
            return

        elif input in params.options:
            self._selected_move = input
            pawn = map_field_text_to_coordinates(self._selected_pawn)
            move = map_field_text_to_coordinates(self._selected_move)
            self._game.do_move(pawn, move)
            self._history.append("Player " + str(self._game.currentPlayer) +
                                 " moved " + self._selected_pawn + " to " +
                                 self._selected_move)

            if self._game.is_terminal():
                self._state = States.WIN
                self._feedback = "Game finished. "
                self._selected_move = None
                self._selected_pawn = None
                return
            else:
                self._game.to_next_turn()
                self._state = States.TAKE_TURN
                return

        else:
            self._feedback = "Bad input! "
            return


class MachineActorRandom(BaseActor):

    def __init__(self, name, game, gui, history):
        super().__init__(name, game, gui, history)

    def take_turn(self):
        pass


class App:
    """
    Contains the loop of printing to screen, getting user input,
    and interacting with the game logic.
    Is agnostic of the specific game (as long as game implements
    required methods).

    loopState: Contains the state as in a automaton.

    feedback: A string containing feedback to be shown to the user when
    entering the next state.

    game: References the game instance that contains all game logic.

    selectedPawn: Describes the currently selected pawn in format A0.

    selectedMove: Describes the currently selected move for the selected pawn
    in format A0.
    """
    loopState = States.CHOOSE_GAME
    currentGameId = None
    feedback = None
    currentGame = None
    game = None
    history = []
    """Pawn in format A0."""
    selectedPawn = None
    selectedMove = None
    gui = Output()
    _player_one = None
    _player_two = None

    sharedOptions = {
        Commands.QUIT_APP: "stops app",
    }

    def __init__(self):
        pass

    def loop(self):
        """
        The main method of the whole application.
        Contains the loop of the user interacting with the application
        and the game loop.

        return: void.
        """
        while True:
            try:
                if self.loopState == States.CHOOSE_GAME:
                    self._do_step_choose_game()
                    continue
                elif self.loopState == States.CHOOSE_BOARD_SIZE:
                    self._do_step_choose_board_size()
                    continue
                elif self.loopState == States.CHOOSE_OPP_HUMAN_OR_MACHINE:
                    self._do_step_choose_opp_human_or_machine()
                    continue
                elif self.loopState == States.CHOOSE_MACHINE_STRATEGY:
                    self._do_step_choose_machine_strategy()
                    continue
                elif self.loopState == States.CHOOSE_PLAYER_ORDER:
                    self._do_step_choose_player_order()
                    continue
                elif self.loopState == States.START_GAME:
                    self._do_step_start_game()
                    continue
                elif self.loopState == States.TAKE_TURN:
                    self.__do_step_take_turn()
                    continue
                elif self.loopState == States.WIN:
                    self._do_step_win()
                    continue
                elif self.loopState == States.BYE:
                    self._do_step_bye()
                    break
            except:
                pass

    def _do_step_choose_game(self):
        """
        The (human) user chooses which game to play.
        """
        params = self._prepare_values_to_be_rendered()
        params.instruction = "Choose which game to play!"
        params.options.update({
            Commands.CHOOSE_GAME_ALQUERQUE: "play Alquerque",
            Commands.CHOOSE_GAME_BAUERNSCHACH: "play Bauernschach",
        })

        self.gui.print_screen(params)

        input = read_input()

        if input == Commands.QUIT_APP:
            self.feedback = None
            self.loopState = States.BYE
            return

        elif input == Commands.CHOOSE_GAME_ALQUERQUE:
            self.currentGame = CurrentGame()
            self.currentGame.gameChoice = Games.ALQUERQUE
            self.loopState = States.CHOOSE_BOARD_SIZE
            self.feedback = "You have chosen to play Alquerque."
            return

        elif input == Commands.CHOOSE_GAME_BAUERNSCHACH:
            self.currentGame = CurrentGame()
            self.currentGame.gameChoice = Games.BAUERNSCHACH
            self.loopState = States.CHOOSE_BOARD_SIZE
            self.feedback = "You have chosen to play Bauernschach."
            return

        else:
            self.feedback = "Bad input! "
            return

    def _do_step_choose_board_size(self):
        """
        The (human) user chooses the width and height of the game board.
        """
        params = self._prepare_values_to_be_rendered()
        params.instruction = "Choose the size of the game board!"
        params.options.update({
            "4": "4x4",
            "5": "5x5",
            "6": "6x6",
            "7": "7x7",
            "8": "8x8"
        })
        self.gui.print_screen(params)

        input = read_input()

        if input in self.sharedOptions:
            if input == Commands.QUIT_APP:
                self.feedback = None
                self.loopState = States.BYE
                return

        elif int(input) in range(4, 8):
            self.currentGame.boardSize = int(input)
            self.feedback = "You have chosen a board of size " + input + "."
            self.loopState = States.CHOOSE_OPP_HUMAN_OR_MACHINE
            return

        else:
            self.feedback = "Bad input! "
            return

    def _do_step_choose_opp_human_or_machine(self):
        """
        The (human) user chooses whether he is going to play
        against another human or against the machine.
        """
        params = self._prepare_values_to_be_rendered()
        params.instruction = "Want to play against human or machine?"
        params.options.update({
            Commands.CHOOSE_OPP_AS_HUMAN: "Human",
            Commands.CHOOSE_OPP_AS_MACHINE: "Machine",
        })
        self.gui.print_screen(params)

        input = read_input()

        if input == Commands.QUIT_APP:
            self.feedback = None
            self.loopState = States.BYE
            return

        elif input == Commands.CHOOSE_OPP_AS_HUMAN:
            self.currentGame.machine = None
            self.loopState = States.CHOOSE_PLAYER_ORDER
            self.feedback = "You have chosen to play against another human."
            return

        elif input == Commands.CHOOSE_OPP_AS_MACHINE:
            self.loopState = States.CHOOSE_MACHINE_STRATEGY
            self.feedback = "You have chosen to play against the machine."
            return

        else:
            self.feedback = "Bad input! "
            return

    def _do_step_choose_machine_strategy(self):
        """
        If the opponent is a machine, the (human) user chooses
        what strategy that machine is going to use.
        """
        params = self._prepare_values_to_be_rendered()
        params.instruction = "What strategy shall the machine use?"
        params.options.update({
            Commands.CHOOSE_MACHINE_STRATEGY_RANDOM: "Random",
        })
        self.gui.print_screen(params)

        input = read_input()

        if input == Commands.QUIT_APP:
            self.feedback = None
            self.loopState = States.BYE
            return

        elif input == Commands.CHOOSE_MACHINE_STRATEGY_RANDOM:
            self.currentGame.machine = RandomMachine()
            self.loopState = States.CHOOSE_PLAYER_ORDER
            self.feedback = "You have chosen the random acting opp."
            return

        else:
            self.feedback = "Bad input! "
            return

    def _do_step_choose_player_order(self):
        """
        The (human) user chooses whether he or his opponent is going to start.
        """
        params = self._prepare_values_to_be_rendered()
        params.instruction = "Which player shall start first?"
        params.options.update({
            Commands.CHOOSE_FIRST_PLAYER_ME: "if you want to start",
            Commands.CHOOSE_FIRST_PLAYER_OPPONENT: "if opponent shall start",
        })
        self.gui.print_screen(params)

        input = read_input()

        if input == Commands.QUIT_APP:
            self.feedback = None
            self.loopState = States.BYE
            return

        elif input == Commands.CHOOSE_FIRST_PLAYER_ME:
            self.currentGame.playerToStartFirst = Player.USER
            self.loopState = States.START_GAME
            return

        elif input == Commands.CHOOSE_FIRST_PLAYER_OPPONENT:
            self.currentGame.playerToStartFirst = Player.OPP
            self.loopState = States.START_GAME
            return

        else:
            self.feedback = "Bad input! "
            return

    def _do_step_start_game(self):
        """
        This starts the actual game loop based on the previous configuration.
        """
        playerToStart = self.currentGame.playerToStartFirst
        boardSize = self.currentGame.boardSize

        if self.currentGame.gameChoice == Games.BAUERNSCHACH:
            self.currentGame.game = Bauernschach(playerToStart, boardSize)
            self.loopState = States.TAKE_TURN
            # self.feedback = self._whos_turn_it_is()
            self._player_user = HumanActor(
                "Player User", self.currentGame.game, self.gui, self.history)
            self._player_opp = HumanActor(
                "Player Opp", self.currentGame.game, self.gui, self.history)
            if (self.currentGame.playerToStartFirst == Player.USER):
                self.currentGame.currentActor = self._player_user
                self.currentGame.waitingActor = self._player_opp
            else:
                self.currentGame.currentActor = self._player_opp
                self.currentGame.waitingActor = self._player_user
            return

        elif self.currentGame.gameChoice == Games.ALQUERQUE:
            self.currentGame.gameChoice = Games.BAUERNSCHACH
            # TODO: not implemented yet!
            return

    def __do_step_take_turn(self):
        """

        """
        # TODO: get the propper actor!! Currently only human actor.
        self.currentGame.currentActor.take_turn()
        temp = self.currentGame.currentActor

        # Switch turn
        self.currentGame.currentActor = self.currentGame.waitingActor
        self.currentGame.waitingActor = temp

    def _do_step_bye(self):
        """
        The user has chosen to quit the application.
        """
        params = self._prepare_values_to_be_rendered()
        params.instruction = "Bye bye!"
        self.gui.print_screen(params)
        return

    def _do_step_win(self):
        """
        Termination of the game loop.
        """
        if self.currentGame.game.player_1_to_win():
            self.feedback = "You have won. Congrats! "
        else:
            self.feedback = "Opponent has won. Better luck next time. "
        self.loopState = States.CHOOSE_GAME

    def _whos_turn_it_is(self):
        """
        Helper function to print whos turn it is.
        """
        if self.currentGame.game.currentPlayer == Player.USER:
            return "Your turn! "
        else:
            return "Opp's turn! "

    def _prepare_values_to_be_rendered(self):
        """
        Helper function that initializes a new screen parameter object
        with default values.
        """
        values = ScreenParameters()
        if self.currentGame is not None and \
                self.currentGame.game is not None:
            values.game = self.currentGame.game
            values.board = self.currentGame.game.get_bord()
            values.moveHistory = self.currentGame.game.get_move_history()
        # TODO: add player
        if self.feedback is not None:
            values.feedback = self.feedback
            self.feedback = None
        values.options = deepcopy(self.sharedOptions)
        return values


# Run the application.
if __name__ == "__main__":
    App().loop()
