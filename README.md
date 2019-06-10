# Board Games with some Game Theory Cleverness
Julian Stampfli, Marc Rey, 2019.

## Context
This is a console app developed during the course "Game Theory" by J. Eckerle at University of Applied Sciences Berne in Spring 2019.

The goal of this app is to implement Game Theory strategies in a play of a board game. The user plays against a computer opponent who may either choose his next move randomly or by strategically evaluating his best move.

There are two board games that can be played:
- Pawn Chess / Bauernschach
- Alquerque / Original Checkers

## Board Games

### Pawn Chess / Bauernschach

#### Game Rules

- The game is a simplification of Chess such that there are only the pawns and no other figures.
- Play happens on a square board of 4 to 8 fields in width and height respectively.
- Initially each player has as many pawns as the board is wide, placed in the second row closest to him.
  ```
  - - - - -
  X X X X X
  - - - - -
  - - - - -
  O O O O O
  - - - - -
  ```
- Players move turn by turn and one pawn per turn.
- Pawns may move by:
  - advancing straight ahead 1 field, if this is not blocked.
  - advancing straight ahead 2 fields, if those are unoccupied and the pawn has not been moved yet.
  - advancing straight ahead 1 field then left or right 1 field, if the target field is occupied by the opponent. The opponent's pawn is killed.
  - stepping left or right 1 field, if this field is occupied by the opponent and the occupying pawn has moved once. (en passant) The opponent's pawn is killed.
- The game is won by the player who manages first to get a pawn to the last row on the opposite of the board.

#### Strategy

TBD

### Alquerque / Original version of Checkers

#### Game Rules (according to Mr. Eckerle)

- The game is a simplification of the various versions of Checkers played today.
- Play happens on a square board of 4 to 8 fields in width and height respectively.
- Initially each player has as many pawns as half the number of fields on the board, while 1 (uneven board width) or 2 (even board width) fields at the center must remain empty.
  ```
  X X X X X
  X X X X X
  X X - O O
  O O O O O
  O O O O O
  ```
  ```
  X X X X X X
  X X X X X X
  X X - - O O
  O O O O O O
  O O O O O O
  ```
- Players move turn by turn and one pawn per turn.
- Pawns may move by:
  - moving 1 field in any direction including diagonally, if this field is unoccupied.
  - moving 2 fields in any one direction including diagonally, if the first field is occupied by the opponent and the second field is unoccupied. The opponent's pawn on the first field is killed.
- The game is won by the player who's opponent cannot move:
  - either because he has no more pawns
  - or because he has no possible moves, that is he is blocked.

#### Strategy

TBD

Für die Bewertung der Horizontknoten kann statt einer heuristischen Bewertungsfunktion auch ein Monte-Carlo-Test zum Einsatz kommen. Siehe folgenden Artikel:

## App usage

- Start by running the app.py in this same directory.
- The app is built with Python version 3.7.
- As a user, interact with the app by entering one of the commands shown at each step.
- Note that on the board, you as a user are placed on the bottom side while the opponent is placed on the top side.
