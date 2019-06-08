#!/usr/bin/python3

import re
import os
from models import FieldValue, Player


class Output:
    """
    The rendering of the console game.
    """

    def clear(self):
        return os.system('cls' if os.name == 'nt' else 'clear')

    def print_screen(self, params):
        """Renders one screen to the console."""
        self.clear()

        title = self._prepare_title()
        history = self._prepare_history(params.moveHistory)
        board = self._prepare_bord(params.board)
        player = self._prepare_player(params.player)
        feedback = self._prepare_feedback(params.feedback)
        instruction = self._prepare_instruction(params.instruction)
        options = self._prepare_options(params.options)

        screenLines = []
        screenLines.extend(title)
        screenLines.extend(board)
        screenLines.extend(history)
        screenLines.append(player)
        screenLines.append(feedback)
        screenLines.append(instruction)
        screenLines.append(options)

        for line in screenLines:
            print(line)
        return

    def _prepare_title(self):
        """Shows the game title. Returns a list of lines to be rendered."""
        title = [
            " _____                   _  _____                       ",
            "| __  | ___  ___  ___  _| ||   __| ___  _____  ___  ___ ",
            "| __ -|| . || .'||  _|| . ||  |  || .'||     || -_||_ -|",
            "|_____||___||__,||_|  |___||_____||__,||_|_|_||___||___|",
            "                    by Julian Stampfli and Marc Rey 2019",
        ]
        return title

    def _prepare_bord(self, positions):
        """Shows the bord. Returns a list of lines to be rendered."""
        size = len(positions)
        if size < 1:
            return []
        colLabels = "    "
        rowSeparator = "   +"
        for colindex in range(0, size):
            colLabels += " " + str(colindex) + "  "
            rowSeparator += "---+"
        bord = []
        bord.append(colLabels)
        bord.append(rowSeparator)
        for rowindex in range(0, size):
            cells = []
            cells.append(self._get_row_label(rowindex))  # one char in length
            for cellindex in range(0, size):
                # one char in length
                cells.append(self._prepare_cell(
                    positions[rowindex][cellindex]))
            row = (" " + ' | '.join(['%s'] * len(cells)) + " |") % tuple(cells)
            bord.append(row)
            bord.append(rowSeparator)
        return bord

    def _get_row_label(self, rowindex):
        """Returns the letter (A-E) for the desired row."""
        return chr(rowindex + 97).upper()

    def _prepare_cell(self, value):
        """Returns the coin in the color of the respective player."""
        options = {
            Player.OPP: "x",
            0: " ",
            Player.USER: "o",
            FieldValue.POSSIBLE_MOVE: "?",
        }
        return options.get(value, "?")

    def _prepare_history(self, steps):
        """Returns some lines containing the game history."""
        if len(steps) < 1:
            return []
        history = [
            "History:       ",
        ]
        for step in steps:
            fieldFrom = self._map_field_coordinates_to_text(step[0])
            fieldTo = self._map_field_coordinates_to_text(step[1])
            entry = fieldFrom + " to " + fieldTo
            history.append(entry)
        return history

    def _prepare_player(self, player):
        """Returns the player to the user formatted."""
        if player is None or len(player) < 1:
            return ""
        result = "Player:        " + player
        return result

    def _prepare_feedback(self, feedback):
        """Returns a feedback to the user formatted."""
        if feedback is None or len(feedback) < 1:
            return ""
        result = "Feedback:      " + feedback
        return result

    def _prepare_instruction(self, instruction):
        """Returns an instruction to the user formatted."""
        if instruction is None or len(instruction) < 1:
            return ""
        result = "Instruction:   " + instruction
        return result

    def _prepare_options(self, options):
        instruction = ""
        if (len(options) > 0):
            instruction = instruction + "\nChoose:       "
            for key, value in options.items():
                if value is not None and len(value) > 0:
                    instruction = instruction + "  [" + key + "]: " + value
                else:
                    instruction = instruction + "  [" + key + "]"
        return instruction

    def _map_field_coordinates_to_text(self, field):
        return self._get_row_label(field[0]) + str(field[1])

    def map_fields_coordinates_to_text(self, fields):
        result = []
        for field in fields:
            result.append(self._map_field_coordinates_to_text(field))
        return result
