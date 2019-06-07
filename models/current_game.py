#!/usr/bin/python3
class CurrentGame:
    # Game setup.
    board_size = 4
    game_choice = None
    machine = None
    player_to_start = None

    # Game engine, state, players
    engine = None
    current_actor = None
    waiting_actor = None
    history = []
