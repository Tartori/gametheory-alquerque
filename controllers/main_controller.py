#!/usr/bin/python3
from copy import deepcopy

# from controllers import BaseController, HumanActor, MachineRandomActor
from controllers import BaseController, HumanActor, MachineRandomActor, \
    MachineCleverActor, MachineSimpleHeuristicActor, MachineComplexHeuristicActor
from models import State, CurrentGame, Commands, Games, MachineStrategies, \
    Player, ScreenParameters, States
from games import Bauernschach, Alquerque


class MainController(BaseController):
    """
    Contains the loop of printing to screen, getting user input,
    and interacting with the game logic.
    Is agnostic of the specific game (as long as game implements
    required methods).

    return: void.
    """

    def __init__(self):
        super().__init__("App-User", State())
        self._state.activity = States.CHOOSE_GAME
        pass

    def loop(self) -> None:
        """
        The main method of the whole application.
        From here, the user configures games and the actor controllers
        are called.
        Build as a simple state machine.
        """
        while True:
            try:
                if self._state.activity == States.CHOOSE_GAME:
                    self.__do_step_choose_game()
                    continue
                elif self._state.activity == States.CHOOSE_BOARD_SIZE:
                    self.__do_step_choose_board_size()
                    continue
                elif self._state.activity == States.CHOOSE_OPP:
                    self.__do_step_choose_opp()
                    continue
                elif self._state.activity == States.CHOOSE_MACHINE_STRATEGY:
                    self.__do_step_choose_machine_strategy()
                    continue
                elif self._state.activity == States.CHOOSE_PLAYER_ORDER:
                    self.__do_step_choose_player_order()
                    continue
                elif self._state.activity == States.START_GAME:
                    self.__do_step_start_game()
                    continue
                elif self._state.activity == States.TAKE_TURN:
                    self.__do_step_take_turn()
                    continue
                elif self._state.activity == States.WIN:
                    self.__do_step_win()
                    continue
                elif self._state.activity == States.BYE:
                    self.__do_step_bye()
                    break
            except Exception as e:
                print(e)

    def __do_step_choose_game(self):
        """
        The (human) user chooses which game to play.
        """
        params = self._prepare_values_to_be_rendered()
        params.instruction = "Choose which game to play!"
        params.options.update({
            Commands.CHOOSE_GAME_ALQUERQUE: "play Alquerque",
            Commands.CHOOSE_GAME_BAUERNSCHACH: "play Bauernschach",
        })

        self._gui.print_screen(params)

        input = self._read_input()

        if not self._handle_common_inputs(input, params.options):
            if input == Commands.CHOOSE_GAME_ALQUERQUE:
                self._state.game = CurrentGame()
                self._state.game.engine_choice = Games.ALQUERQUE
                self._state.activity = States.CHOOSE_BOARD_SIZE
                self._state.feedback = "You have chosen to play Alquerque."

            elif input == Commands.CHOOSE_GAME_BAUERNSCHACH:
                self._state.game = CurrentGame()
                self._state.game.engine_choice = Games.BAUERNSCHACH
                self._state.activity = States.CHOOSE_BOARD_SIZE
                self._state.feedback = "You have chosen to play Bauernschach."

    def __do_step_choose_board_size(self):
        """
        The (human) user chooses the width and height of the game board.
        """
        params = self._prepare_values_to_be_rendered()
        params.instruction = "Choose the size of the game board!"
        if self._state.game.engine_choice == Games.ALQUERQUE:
            params.options.update({
                "5": "5x5",
                "7": "7x7"
            })
        elif self._state.game.engine_choice == Games.BAUERNSCHACH:
            params.options.update({
                "4": "4x4",
                "5": "5x5",
                "6": "6x6",
                "7": "7x7",
                "8": "8x8"
            })
        self._gui.print_screen(params)

        input = self._read_input()

        if not self._handle_common_inputs(input, params.options):
            if int(input) in range(4, 9):
                self._state.game.board_size = int(input)
                self._state.feedback = "You have chosen a board of size " \
                    + input + "."
                self._state.activity = States.CHOOSE_OPP

    def __do_step_choose_opp(self):
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
        self._gui.print_screen(params)

        input = self._read_input()

        if not self._handle_common_inputs(input, params.options):
            if input == Commands.CHOOSE_OPP_AS_HUMAN:
                self._state.game.machine = None
                self._state.activity = States.CHOOSE_PLAYER_ORDER
                self._state.feedback = "You have chosen to play " + \
                    "against another human."

            elif input == Commands.CHOOSE_OPP_AS_MACHINE:
                self._state.activity = States.CHOOSE_MACHINE_STRATEGY
                self._state.feedback = "You have chosen to play " + \
                    "against the machine."

    def __do_step_choose_machine_strategy(self):
        """
        If the opponent is a machine, the (human) user chooses
        what strategy that machine is going to use.
        """
        params = self._prepare_values_to_be_rendered()
        params.instruction = "What strategy shall the machine use?"
        if self._state.game.engine_choice == Games.ALQUERQUE:
            params.options.update({
                Commands.CHOOSE_MACHINE_STRATEGY_RANDOM: "Random",
                Commands.CHOOSE_MACHINE_STRATEGY_CLEVER: "Monte Carlo",
                Commands.CHOOSE_MACHINE_STRATEGY_SIMPLE_HEURISTIC: "Simple Heuristic"
            })
        elif self._state.game.engine_choice == Games.BAUERNSCHACH:
            params.options.update({
                Commands.CHOOSE_MACHINE_STRATEGY_RANDOM: "Random",
                Commands.CHOOSE_MACHINE_STRATEGY_CLEVER: "Monte Carlo",
                Commands.CHOOSE_MACHINE_STRATEGY_SIMPLE_HEURISTIC: "Simple Heuristic",
                Commands.CHOOSE_MACHINE_STRATEGY_COMPLEX_HEURISTIC: "Complex Heuristic"
            })
        else:
            raise Exception("No game chosen.")
        self._gui.print_screen(params)

        input = self._read_input()

        if not self._handle_common_inputs(input, params.options):
            if input == Commands.CHOOSE_MACHINE_STRATEGY_RANDOM:
                self._state.game.machine = MachineStrategies.RANDOM
                self._state.activity = States.CHOOSE_PLAYER_ORDER
                self._state.feedback = "You have chosen the random acting opp."

            elif input == Commands.CHOOSE_MACHINE_STRATEGY_CLEVER:
                self._state.game.machine = MachineStrategies.CLEVER
                self._state.activity = States.CHOOSE_PLAYER_ORDER
                self._state.feedback = "You have chosen the opp with Monte Carlo heuristic."

            elif input == Commands.CHOOSE_MACHINE_STRATEGY_SIMPLE_HEURISTIC:
                self._state.game.machine = MachineStrategies.SIMPLE_HEURISTIC
                self._state.activity = States.CHOOSE_PLAYER_ORDER
                self._state.feedback = "You have chosen the opp with a simple heuristic."

            elif input == Commands.CHOOSE_MACHINE_STRATEGY_COMPLEX_HEURISTIC:
                self._state.game.machine = MachineStrategies.COMPLEX_HEURISTIC
                self._state.activity = States.CHOOSE_PLAYER_ORDER
                self._state.feedback = "You have chosen the opp with a complex heuristic."

    def __do_step_choose_player_order(self):
        """
        The (human) user chooses whether he or his opponent is going to start.
        """
        params = self._prepare_values_to_be_rendered()
        params.instruction = "Which player shall start first?"
        params.options.update({
            Commands.CHOOSE_FIRST_PLAYER_ME: "if you want to start",
            Commands.CHOOSE_FIRST_PLAYER_OPPONENT: "if opponent shall start",
        })
        self._gui.print_screen(params)

        input = self._read_input()

        if not self._handle_common_inputs(input, params.options):
            if input == Commands.CHOOSE_FIRST_PLAYER_ME:
                self._state.game.player_to_start = Player.USER
                self._state.activity = States.START_GAME

            elif input == Commands.CHOOSE_FIRST_PLAYER_OPPONENT:
                self._state.game.player_to_start = Player.OPP
                self._state.activity = States.START_GAME

    def __do_step_start_game(self):
        """
        This starts the actual game loop based on the previous configuration.
        """
        playerToStart = self._state.game.player_to_start
        boardSize = self._state.game.board_size

        # Set up the game
        if self._state.game.engine_choice == Games.BAUERNSCHACH:
            self._state.game.engine = Bauernschach(playerToStart, boardSize)

        elif self._state.game.engine_choice == Games.ALQUERQUE:
            self._state.game.engine = Alquerque(playerToStart, boardSize)

        # Set up the actors
        player_user = HumanActor("Player User", self._state, Player.USER)
        if self._state.game.machine is None:
            player_opp = HumanActor("Human Opp", self._state, Player.OPP)
        elif self._state.game.machine == MachineStrategies.RANDOM:
            player_opp = MachineRandomActor(
                "Machine Opp (Random)", self._state, Player.OPP)
        elif self._state.game.machine == MachineStrategies.CLEVER:
            player_opp = MachineCleverActor(
                "Machine Opp (Monte Carlo)", self._state, Player.OPP)
        elif self._state.game.machine == MachineStrategies.SIMPLE_HEURISTIC:
            player_opp = MachineSimpleHeuristicActor(
                "Machine Opp (Simple Heuristic)", self._state, Player.OPP)
        elif self._state.game.machine == MachineStrategies.COMPLEX_HEURISTIC:
            player_opp = MachineComplexHeuristicActor(
                "Machine Opp (Complex Heuristic)", self._state, Player.OPP)
        else:
            raise Exception("No opponent defined.")

        if (self._state.game.player_to_start == Player.USER):
            self._state.game.current_actor = player_user
            self._state.game.waiting_actor = player_opp
        else:
            self._state.game.current_actor = player_opp
            self._state.game.waiting_actor = player_user

        self._state.activity = States.TAKE_TURN

    def __do_step_take_turn(self):
        """
        Alternates between the two players and lets them
        make their moves.
        """
        self._state.game.current_actor.take_turn()

        if not self._state.activity == States.TAKE_TURN:
            return

        if (self._state.game.engine.is_terminal()):
            self._state.activity = States.WIN
        else:
            # Switch turn
            temp = self._state.game.current_actor
            self._state.game.current_actor = self._state.game.waiting_actor
            self._state.game.waiting_actor = temp
            # Tell engine to prepare next turn
            self._state.game.engine.to_next_turn()

    def __do_step_bye(self):
        """
        The user has chosen to quit the application.
        """
        params = self._prepare_values_to_be_rendered()
        params.instruction = "Bye bye!"
        self._gui.print_screen(params)
        return

    def __do_step_win(self):
        """
        Termination of the game loop.
        """
        winner = self._state.game.engine.get_winner()
        if winner == Player.USER:
            self._state.feedback = "You (" + \
                self._state.game.current_actor.get_name() + \
                ") have won. Congrats! "
        else:
            self._state.feedback = "Opponent (" + \
                self._state.game.current_actor.get_name() + \
                ") has won. Better luck next time. "
        self._state.activity = States.CHOOSE_GAME
