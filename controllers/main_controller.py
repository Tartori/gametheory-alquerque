#!/usr/bin/python3


from copy import deepcopy

from controllers import BaseController, HumanActor, MachineRandomActor
from models import CurrentGame, Commands, Games
from models import Player, ScreenParameters, States
from games import Bauernschach


class MainController(BaseController):
    """
    Contains the loop of printing to screen, getting user input,
    and interacting with the game logic.
    Is agnostic of the specific game (as long as game implements
    required methods).

    return: void.
    """

    def __init__(self):
        super().__init__(None)
        self._state = States.CHOOSE_GAME
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
                if self._state == States.CHOOSE_GAME:
                    self.__do_step_choose_game()
                    continue
                elif self._state == States.CHOOSE_BOARD_SIZE:
                    self.__do_step_choose_board_size()
                    continue
                elif self._state == States.CHOOSE_OPP_HUMAN_OR_MACHINE:
                    self.__do_step_choose_opp_human_or_machine()
                    continue
                elif self._state == States.CHOOSE_MACHINE_STRATEGY:
                    self.__do_step_choose_machine_strategy()
                    continue
                elif self._state == States.CHOOSE_PLAYER_ORDER:
                    self.__do_step_choose_player_order()
                    continue
                elif self._state == States.START_GAME:
                    self.__do_step_start_game()
                    continue
                elif self._state == States.TAKE_TURN:
                    self.__do_step_take_turn()
                    continue
                elif self._state == States.WIN:
                    self.__do_step_win()
                    continue
                elif self._state == States.BYE:
                    self.__do_step_bye()
                    break
            except:
                pass

    def __do_step_choose_game(self):
        """
        The (human) user chooses which game to play.
        """
        params = self.__prepare_values_to_be_rendered()
        params.instruction = "Choose which game to play!"
        params.options.update({
            Commands.CHOOSE_GAME_ALQUERQUE: "play Alquerque",
            Commands.CHOOSE_GAME_BAUERNSCHACH: "play Bauernschach",
        })

        self._gui.print_screen(params)

        input = self._read_input()

        if input == Commands.QUIT_APP:
            self._feedback = None
            self._state = States.BYE
            return

        elif input == Commands.CHOOSE_GAME_ALQUERQUE:
            self._current = CurrentGame()
            self._current.game_choice = Games.ALQUERQUE
            self._state = States.CHOOSE_BOARD_SIZE
            self._feedback = "You have chosen to play Alquerque."
            return

        elif input == Commands.CHOOSE_GAME_BAUERNSCHACH:
            self._current = CurrentGame()
            self._current.game_choice = Games.BAUERNSCHACH
            self._state = States.CHOOSE_BOARD_SIZE
            self._feedback = "You have chosen to play Bauernschach."
            return

        else:
            self._feedback = "Bad input! "
            return

    def __do_step_choose_board_size(self):
        """
        The (human) user chooses the width and height of the game board.
        """
        params = self.__prepare_values_to_be_rendered()
        params.instruction = "Choose the size of the game board!"
        params.options.update({
            "4": "4x4",
            "5": "5x5",
            "6": "6x6",
            "7": "7x7",
            "8": "8x8"
        })
        self._gui.print_screen(params)

        input = self._read_input()

        if input in self._shared_options:
            if input == Commands.QUIT_APP:
                self._feedback = None
                self._state = States.BYE
                return

        elif int(input) in range(4, 8):
            self._current.board_size = int(input)
            self._feedback = "You have chosen a board of size " + input + "."
            self._state = States.CHOOSE_OPP_HUMAN_OR_MACHINE
            return

        else:
            self._feedback = "Bad input! "
            return

    def __do_step_choose_opp_human_or_machine(self):
        """
        The (human) user chooses whether he is going to play
        against another human or against the machine.
        """
        params = self.__prepare_values_to_be_rendered()
        params.instruction = "Want to play against human or machine?"
        params.options.update({
            Commands.CHOOSE_OPP_AS_HUMAN: "Human",
            Commands.CHOOSE_OPP_AS_MACHINE: "Machine",
        })
        self._gui.print_screen(params)

        input = self._read_input()

        if input == Commands.QUIT_APP:
            self._feedback = None
            self._state = States.BYE
            return

        elif input == Commands.CHOOSE_OPP_AS_HUMAN:
            self._current.machine = None
            self._state = States.CHOOSE_PLAYER_ORDER
            self._feedback = "You have chosen to play against another human."
            return

        elif input == Commands.CHOOSE_OPP_AS_MACHINE:
            self._state = States.CHOOSE_MACHINE_STRATEGY
            self._feedback = "You have chosen to play against the machine."
            return

        else:
            self._feedback = "Bad input! "
            return

    def __do_step_choose_machine_strategy(self):
        """
        If the opponent is a machine, the (human) user chooses
        what strategy that machine is going to use.
        """
        params = self.__prepare_values_to_be_rendered()
        params.instruction = "What strategy shall the machine use?"
        params.options.update({
            Commands.CHOOSE_MACHINE_STRATEGY_RANDOM: "Random",
        })
        self._gui.print_screen(params)

        input = self._read_input()

        if input == Commands.QUIT_APP:
            self._feedback = None
            self._state = States.BYE
            return

        elif input == Commands.CHOOSE_MACHINE_STRATEGY_RANDOM:
            self._current.machine = MachineRandomActor(
                "random machine", self._current)
            self._state = States.CHOOSE_PLAYER_ORDER
            self._feedback = "You have chosen the random acting opp."
            return

        else:
            self._feedback = "Bad input! "
            return

    def __do_step_choose_player_order(self):
        """
        The (human) user chooses whether he or his opponent is going to start.
        """
        params = self.__prepare_values_to_be_rendered()
        params.instruction = "Which player shall start first?"
        params.options.update({
            Commands.CHOOSE_FIRST_PLAYER_ME: "if you want to start",
            Commands.CHOOSE_FIRST_PLAYER_OPPONENT: "if opponent shall start",
        })
        self._gui.print_screen(params)

        input = self._read_input()

        if input == Commands.QUIT_APP:
            self._feedback = None
            self._state = States.BYE
            return

        elif input == Commands.CHOOSE_FIRST_PLAYER_ME:
            self._current.player_to_start = Player.USER
            self._state = States.START_GAME
            return

        elif input == Commands.CHOOSE_FIRST_PLAYER_OPPONENT:
            self._current.player_to_start = Player.OPP
            self._state = States.START_GAME
            return

        else:
            self._feedback = "Bad input! "
            return

    def __do_step_start_game(self):
        """
        This starts the actual game loop based on the previous configuration.
        """
        playerToStart = self._current.player_to_start
        boardSize = self._current.board_size

        # Set up the game
        if self._current.game_choice == Games.BAUERNSCHACH:
            self._current.game = Bauernschach(playerToStart, boardSize)
            self._state = States.TAKE_TURN
        elif self._current.game_choice == Games.ALQUERQUE:
            self._current.game_choice = Games.BAUERNSCHACH
            # TODO: not implemented yet!

        # Set up the actors
        player_user = HumanActor("Player User", self._current)
        player_opp = HumanActor("Player Opp", self._current)

        if (self._current.player_to_start == Player.USER):
            self._current.current_actor = player_user
            self._current.waiting_actor = player_opp
        else:
            self._current.current_actor = player_opp
            self._current.waiting_actor = player_user

        return

    def __do_step_take_turn(self):
        """

        """
        # TODO: get the propper actor!! Currently only human actor.
        self._current.current_actor.take_turn()
        temp = self._current.current_actor

        # Switch turn
        self._current.current_actor = self._current.waiting_actor
        self._current.waiting_actor = temp

    def __do_step_bye(self):
        """
        The user has chosen to quit the application.
        """
        params = self.__prepare_values_to_be_rendered()
        params.instruction = "Bye bye!"
        self._gui.print_screen(params)
        return

    def __do_step_win(self):
        """
        Termination of the game loop.
        """
        if self._current.game.player_1_to_win():
            self._feedback = "You have won. Congrats! "
        else:
            self._feedback = "Opponent has won. Better luck next time. "
        self._state = States.CHOOSE_GAME

    def __prepare_values_to_be_rendered(self):
        """
        Helper function that initializes a new screen parameter object
        with default values.
        """
        values = ScreenParameters()
        if self._current is not None and \
                self._current.game is not None:
            values.game = self._current.game
            values.board = self._current.game.get_bord()
            values.moveHistory = self._current.game.get_move_history()
        if self._feedback is not None:
            values.feedback = self._feedback
            self._feedback = None
        values.options = deepcopy(self._shared_options)
        return values
