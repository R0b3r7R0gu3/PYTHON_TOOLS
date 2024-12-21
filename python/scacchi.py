import itertools

WHITE = "white"
BLACK = "black"


class Game:
    def __init__(self):
        self.playersturn = BLACK
        self.message = "Scrivi qui sotto"
        self.gameboard = {}
        self.placePieces()
        print("Scacchi by Robert")
        self.main()

    def placePieces(self):

        for i in range(0, 8):
            self.gameboard[(i, 1)] = Pawn(WHITE, uniDict[WHITE][Pawn], 1)
            self.gameboard[(i, 6)] = Pawn(BLACK, uniDict[BLACK][Pawn], -1)

        placers = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        for i in range(0, 8):
            self.gameboard[(i, 0)] = placers[i](WHITE, uniDict[WHITE][placers[i]])
            self.gameboard[((7 - i), 7)] = placers[i](BLACK, uniDict[BLACK][placers[i]])
        placers.reverse()

    def main(self):

        while True:
            self.printBoard()
            print(self.message)
            self.message = ""
            startpos, endpos = self.parseInput()
            try:
                target = self.gameboard[startpos]
            except:
                self.message = "Pezzo non trovato"
                target = None

            if target:
                print("found " + str(target))
                if target.Color != self.playersturn:
                    self.message = "Non puoi muovere il pezzo"
                    continue
                if target.isValid(startpos, endpos, target.Color, self.gameboard):
                    self.message = "Mossa valida"
                    self.gameboard[endpos] = self.gameboard[startpos]
                    del self.gameboard[startpos]
                    self.isCheck()
                    if self.playersturn == BLACK:
                        self.playersturn = WHITE
                    else:
                        self.playersturn = BLACK
                else:
                    self.message = "Mossa invalida" + str(
                        target.availableMoves(startpos[0], startpos[1], self.gameboard))
                    print(target.availableMoves(startpos[0], startpos[1], self.gameboard))
            else:
                self.message = "Nessun pezzo"

    def isCheck(self):
        king = King
        kingDict = {}
        pieceDict = {BLACK: [], WHITE: []}
        for position, piece in self.gameboard.items():
            if type(piece) == King:
                kingDict[piece.Color] = position
            print(piece)
            pieceDict[piece.Color].append((piece, position))
        # white
        if self.canSeeKing(kingDict[WHITE], pieceDict[BLACK]):
            self.message = "Bianco è sotto scacco"
        if self.canSeeKing(kingDict[BLACK], pieceDict[WHITE]):
            self.message = "Nero è sotto scacco"

    def canSeeKing(self, kingpos, piecelist):
        for piece, position in piecelist:
            if piece.isValid(position, kingpos, piece.Color, self.gameboard):
                return True

    def parseInput(self):
        try:
            a, b = input().split()
            a = ((ord(a[0]) - 97), int(a[1]) - 1)
            b = (ord(b[0]) - 97, int(b[1]) - 1)
            print(a, b)
            return (a, b)
        except:
            print("Riprova per favore")
            return ((-1, -1), (-1, -1))

    """def validateInput(self, *kargs):
        for arg in kargs:
            if type(arg[0]) is not type(1) or type(arg[1]) is not type(1):
                return False
        return True"""

    def printBoard(self):
        print("  1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |")
        for i in range(0, 8):
            print("-" * 32)
            print(chr(i + 97), end="|")
            for j in range(0, 8):
                item = self.gameboard.get((i, j), " ")
                print(str(item) + ' |', end=" ")
            print()
        print("-" * 32)

    """La classe game ha due matrici di pezzi per ogni giocatore
un array 8x8 di oggetti Piece che rappresentano i pezzi, ciascuno con un riferimento alla sua posizione sulla scacchiera
una funzione analyze_input che prende in input la mossa dell'utente e restituisce una lista di due tuple che indicano la posizione di partenza e di arrivo del pezzo
una funzione checkmateExists che verifica se uno dei due giocatori è in scacco matto
una funzione checkExists che controlla se uno dei due giocatori è sotto scacco
un ciclo principale che riceve l'input dall'utente, lo analizza attraverso la funzione analyze_input, controlla se la mossa è valida, la esegue e sposta il pezzo. Se la mossa provoca un conflitto con un altro pezzo, il pezzo conflittuale viene rimosso. Viene poi eseguita la funzione ischeck(mate) per controllare se uno dei due giocatori è in scacco o in scacco matto. In caso di scacco matto, viene stampato un messaggio che indica il vincitore della partita.
    """


class Piece:

    def __init__(self, color, name):
        self.name = name
        self.position = None
        self.Color = color

    def isValid(self, startpos, endpos, Color, gameboard):
        if endpos in self.availableMoves(startpos[0], startpos[1], gameboard, Color=Color):
            return True
        return False

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def availableMoves(self, x, y, gameboard):
        print("ERROR: Nessuna mossa")

    def AdNauseum(self, x, y, gameboard, Color, intervals):
        """ripete l'intervallo secondo la regola"""
        answers = []
        for xint, yint in intervals:
            xtemp, ytemp = x + xint, y + yint
            while self.isInBounds(xtemp, ytemp):
                # print(str((xtemp,ytemp))+"Nei limiti")

                target = gameboard.get((xtemp, ytemp), None)
                if target is None:
                    answers.append((xtemp, ytemp))
                elif target.Color != Color:
                    answers.append((xtemp, ytemp))
                    break
                else:
                    break

                xtemp, ytemp = xtemp + xint, ytemp + yint
        return answers

    def isInBounds(self, x, y):
        "Controllo"
        if x >= 0 and x < 8 and y >= 0 and y < 8:
            return True
        return False

    def noConflict(self, gameboard, initialColor, x, y):
        "Controllo regole"
        if self.isInBounds(x, y) and (((x, y) not in gameboard) or gameboard[(x, y)].Color != initialColor): return True
        return False


chessCardinals = [(1, 0), (0, 1), (-1, 0), (0, -1)]
chessDiagonals = [(1, 1), (-1, 1), (1, -1), (-1, -1)]


def knightList(x, y, int1, int2):
    """Torre"""
    return [(x + int1, y + int2), (x - int1, y + int2), (x + int1, y - int2), (x - int1, y - int2),
            (x + int2, y + int1), (x - int2, y + int1), (x + int2, y - int1), (x - int2, y - int1)]


def kingList(x, y):
    return [(x + 1, y), (x + 1, y + 1), (x + 1, y - 1), (x, y + 1), (x, y - 1), (x - 1, y), (x - 1, y + 1),
            (x - 1, y - 1)]


class Knight(Piece):
    def availableMoves(self, x, y, gameboard, Color=None):
        if Color is None: Color = self.Color
        return [(xx, yy) for xx, yy in knightList(x, y, 2, 1) if self.noConflict(gameboard, Color, xx, yy)]


class Rook(Piece):
    def availableMoves(self, x, y, gameboard, Color=None):
        if Color is None: Color = self.Color
        return self.AdNauseum(x, y, gameboard, Color, chessCardinals)


class Bishop(Piece):
    def availableMoves(self, x, y, gameboard, Color=None):
        if Color is None: Color = self.Color
        return self.AdNauseum(x, y, gameboard, Color, chessDiagonals)


class Queen(Piece):
    def availableMoves(self, x, y, gameboard, Color=None):
        if Color is None: Color = self.Color
        return self.AdNauseum(x, y, gameboard, Color, chessCardinals + chessDiagonals)


class King(Piece):
    def availableMoves(self, x, y, gameboard, Color=None):
        if Color is None: Color = self.Color
        return [(xx, yy) for xx, yy in kingList(x, y) if self.noConflict(gameboard, Color, xx, yy)]


class Pawn(Piece):
    def __init__(self, color, name, direction):
        self.name = name
        self.Color = color
        self.direction = direction

    def availableMoves(self, x, y, gameboard, Color=None):
        if Color is None: Color = self.Color
        answers = []
        if (x + 1, y + self.direction) in gameboard and self.noConflict(gameboard, Color, x + 1,
                                                                        y + self.direction): answers.append(
            (x + 1, y + self.direction))
        if (x - 1, y + self.direction) in gameboard and self.noConflict(gameboard, Color, x - 1,
                                                                        y + self.direction): answers.append(
            (x - 1, y + self.direction))
        if (x, y + self.direction) not in gameboard and Color == self.Color: answers.append((x, y + self.direction))
        return answers


uniDict = {WHITE: {Pawn: "♙", Rook: "♖", Knight: "♘", Bishop: "♗", King: "♔", Queen: "♕"},
           BLACK: {Pawn: "♟", Rook: "♜", Knight: "♞", Bishop: "♝", King: "♚", Queen: "♛"}}
Game()
from turtle import Screen
import patch_turtle_image

import math


class Board:
    def __init__(self, size_x, size_y):
        '''
        posizionamento
        '''
        self.size_x = size_x
        self.size_y = size_y

        self.grid = []
        for x in range(self.size_x):
            self.grid.append([])
            for y in range(self.size_y):
                self.grid[x].append(None)

        hmm = self.grid[1][1]
        print(hmm)

        self.screen = Screen()
        self.screen.setup(width=1.0, height=1.0, startx=None, starty=None)
        self.screen.screensize(400, 400)
        self.screen.bgpic("images/board.png")
        self.screen.register_shape("images/w_pawn.png")
        self.screen.register_shape("images/b_pawn.png")
        self.screen.register_shape("images/w_rook.png")
        self.screen.register_shape("images/b_rook.png")
        self.screen.register_shape("images/w_knight.png")
        self.screen.register_shape("images/b_knight.png")
        self.screen.register_shape("images/w_bishop.png")
        self.screen.register_shape("images/b_bishop.png")
        self.screen.register_shape("images/w_queen.png")
        self.screen.register_shape("images/b_queen.png")
        self.screen.register_shape("images/w_king.png")
        self.screen.register_shape("images/b_king.png")

        self.screen.onscreenclick(self.process_click)

        self.selected_piece = None

    def place_piece(self, piece):
        self.grid[piece.x][piece.y] = piece
        print(piece)

    def is_on_board(self, x, y):
        '''
        Da 0 a -1
        0 1 2 3 4 5 6 7

        x o y?
        '''
        if x < 0 or y < 0:
            return False
        if x >= self.size_x or y >= self.size_y:
            return False

        return True

    def contains_black_piece(self, x, y):
        if not self.is_on_board(x, y):
            return False

        if self.grid[x][y] is None:
            return False

        return self.grid[x][y].color == "black"

    def logic2graphic(self, x, y):
        return x * 50 - 175, y * 50 - 175

    def graphic2logic(self, x, y):
        return math.floor((x + 200) / 50), math.floor((y + 200) / 50)

    def is_spot_occupied(self, x, y):
        pass

    def process_click(self, x, y):
        x, y = self.graphic2logic(x, y)
        p = self.grid[x][y]

        if p is self.selected_piece:
            print("unselect")
            self.selected_piece = None
            return

        if self.selected_piece is None:
            self.selected_piece = p

            if self.selected_piece is None:
                print("Nessun pezzo")
            else:
                print("Hai selezionato ", (x, y))
        else:
            if (x, y) in self.selected_piece.get_valid_moves() and self.grid[x][y] is None:
                self.grid[self.selected_piece.x][self.selected_piece.y] = None
                self.selected_piece.move_to(x, y)
                self.grid[x][y] = self.selected_piece

                self.selected_piece = None

                print("Mossa ", (x, y))
            elif (x, y) in self.selected_piece.get_valid_moves() and self.grid[x][y].color != self.selected_piece.color:
                self.grid[x][y].my_turtle.ht()

                self.grid[self.selected_piece.x][self.selected_piece.y] = None
                self.selected_piece.move_to(x, y)
                self.grid[x][y] = self.selected_piece

                self.selected_piece = None

                print("Mossa ", (x, y))
            else:
                print("Mossa invalida")

    def mainloop(self):
        self.screen.mainloop()
        from turtle import TurtleScreenBase
        from PIL import ImageTk

        @staticmethod
        def _image(filename):
            return ImageTk.PhotoImage(file=filename)

        TurtleScreenBase._image = _image

        from turtle import Shape, TurtleScreen
        def register_shape(self, name, shape=None):
            if shape is None:
                shape = Shape("image", self._image(name))
            elif isinstance(shape, tuple):
                shape = Shape("polygon", shape)

            self._shapes[name] = shape

        TurtleScreen.register_shape = register_shape