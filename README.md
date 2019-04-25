# gametheory-alquerque

An implementation of the alerquerque game in Python with an opponent that tries to play optimally. Written during a course on game theory in the BFH.

Rules from <https://www.mastersofgames.com/rules/alquerque-rules.htm>

## Original version of Checkers (according to Mr. Eckerle)

Für das Projekt ist ein einfaches Spiel, wie beispielsweise die Urform von Dame, zu realisieren.

Spielregeln:

Das Spielbrett ist ein rechtwinkliges Gitter der Grösse 5 x 5. Jeder Gitterpunkt stellt eine mögliche Dameposition dar. Zu Beginn wird das Brett mit einer Initialstellung belegt (siehe unten). Anschliessend machen beide Spieler jeweils abwechselnd einen Zug, der darin besteht einen Damenstein auf ein beliebiges direkt benachbartes freies Feld zu ziehen oder einen gegnerischen Stein zu überspringen (ist möglich, falls das unmittelbar dahinterliegende Feld frei ist). Der übersprungene Stein ist geschlagen und wird vom Brett entfernt. Im Unterschied zu den heutigen Damevarianten dürfen die Steine in beliebiger Richtung ziehen (vorwärts, rückwärts, seitwärts oder auch diagonal). In einem Zug darf maximal ein Stein übersprungen werden (statt mehrmalige zusammenhängende Sprünge wie beim Checker). Es gibt auch keine Umwandlung der Damesteine bei Erreichen der gegnerischen Linie. Eine Partei gewinnt, wenn der Gegner nicht mehr ziehen, sei es weil er keine Steine mehr besitzt oder sei es weil er bockiert ist (d.h. in der aktuellen Stellung keinen zulässigen Zug mehr ausführen kann). In allen anderen Fällen ist das Spiel Unentschieden.

```
S    S    S    S    S
S    S    S    S    S
S    S    .    W    W
W    W    W    W    W
W    W    W    W    W
```

Für die Bewertung der Horizontknoten kann statt einer heuristischen Bewertungsfunktion auch ein Monte-Carlo-Test zum Einsatz kommen. Siehe folgenden Artikel:

Implementationsvorschlag: Querkle.

## Alquerque based on the Alfonso Manuscript

### Equipment

The game of Alquerque is played on a special board of 5 x 5 points with lines between them to indicate allowed moves.  To draw a board is easy.  First draw a 5 x 5 orthogonal grid.  The draw two diagonal lines - from each corner to the opposite corner.  Finally draw four diagonal lines in the form of a square that connects the midpoints of each side.

Alquerque is played with 12 black pieces and 12 white pieces in a similar way to Draughts (Checkers).  The pieces could be any shape but typically are counters or disks.

### Preparation and Objective

Toss a coin to decide who plays first.  Playing first is generally thought to be disadvantageous because of the lack of options.  The player playing black pieces places them on the 10 points of the nearest 2 rows plus the 2 rightmost points on the middle row as the player looks at it.  The other player sets the white pieces up in exactly the same way.  This leaves only the middle point without a piece upon it.

The objective of the game is to take all of the opponent's pieces or to produce a position such that the opponent is unable to move.

### Play

Players take turns to move one of their pieces.  A piece may only move along the lines inscribed upon the board.  For each turn a piece makes either a capturing move or an ordinary move.

Whenever a piece has an opponent's piece adjacent to it and the point immediately beyond the opponent's piece is vacant, the opponent's piece can be captured.  A piece is taken by simply hopping over it into the vacant point beyond and removing it from the board.  Unlike an ordinary move, a capturing move can consist of several such hops - if a piece takes an opponent's piece and the new position allows it to take another piece, then it can do so straight away.  The move finishes when the position of the capturing piece no longer allows it to taken any more pieces or the player could make another capture but decides not to.

An ordinary move is made by simply moving a piece along a line to an adjacent point.

### Finishing

The game is won by the player who first manages to take all his opponent's pieces or by the player who has more pieces when it becomes apparent that no more pieces will be taken.   Alternatively, a player can win by rendering the other player unable to move.

A draw occurs by agreement at any point during the game.  If it becomes apparent that no more pieces will be taken and both players have the same number of pieces left, a draw is agreed.  Draws are very common.

### Alterations

After a capture the capturing player can't continue. There are only single captures allowed at a time.

## Running the code

### Requirements

- "Colorama" for cross platform coloring in terminal. See: <https://github.com/tartley/colorama>
